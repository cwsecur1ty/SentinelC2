import socket

# Server configuration
HOST = '0.0.0.0'
PORT = 9999

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        handle_client(client_socket)

def handle_client(client_socket):
    with client_socket:
        while True:
            try:
                command = input("Enter command: ")
                if command.lower() == 'exit':
                    client_socket.sendall(b'exit')
                    break

                client_socket.sendall(command.encode())
                
                # Receive the response from the client
                response = client_socket.recv(4096).decode('utf-8')
                print(f"[*] Received: {response}")

            except Exception as e:
                print(f"[!] Error: {e}")
                break

if __name__ == "__main__":
    start_server()
