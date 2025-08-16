import socket
import time
import sys

if len(sys.argv) != 3:
    print("Usage: python wait_for_service.py <host> <port>")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            print(f"{host}:{port} is available")
            break
    except OSError:
        print(f"Waiting for {host}:{port}...")
        time.sleep(2)
