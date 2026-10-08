import socket

target = input("Target: ")
ports = range(1, 9001)

try:
    ip = socket.gethostbyname(target)
except socket.gaierror:
    raise SystemExit("Could not resolve host")

for port in ports:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)

        if sock.connect_ex((ip, port)) == 0:
            print(f"Port {port} is Open")
