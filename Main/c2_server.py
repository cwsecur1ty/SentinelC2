import socket

# Server configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 9999       # Port to listen on

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
        request = client_socket.recv(1024)
        print(f"[*] Received: {request.decode('utf-8')}")
        
        # Send a response back to the client
        client_socket.send(b"ACK")

if __name__ == "__main__":
    start_server()
