import socket

# Server configuration
SERVER_HOST = '18.134.157.253'  # Replace with your server's IP address
SERVER_PORT = 9999

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))

    # Send some data
    client.send(b"Hello, Server!")
    
    # Receive some data
    response = client.recv(4096)
    print(f"[*] Received: {response.decode('utf-8')}")

if __name__ == "__main__":
    connect_to_server()
