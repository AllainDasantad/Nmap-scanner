# Nmap-scanner

A simple TCP port scanner written in Python using only the built-in `socket` module. It is a small learning project that recreates the most basic feature of [Nmap](https://nmap.org): finding open ports on a host.

> **Disclaimer:** Only scan systems you own or have explicit permission to test. Unauthorized port scanning may be illegal in your country. Safe targets: `127.0.0.1` (your own machine) and `scanme.nmap.org` (provided by the Nmap project for testing).

---

## What is Nmap?

**Nmap** ("Network Mapper") is a free, open-source tool for network discovery and security auditing. It is used by system administrators, penetration testers, and security researchers to understand what is running on a network.

Nmap can:

- **Discover hosts**: find which devices are online on a network
- **Scan ports**: find which ports are open, closed, or filtered
- **Detect services and versions**: identify what software is behind a port (e.g. Apache, OpenSSH)
- **Detect operating systems**: guess the OS of a remote machine
- **Run scripts (NSE)**: the Nmap Scripting Engine automates tasks such as vulnerability checks

### Common Nmap commands

| Command | What it does |
|---|---|
| `nmap 127.0.0.1` | Scan the 1000 most common ports |
| `nmap -p 1-1024 127.0.0.1` | Scan ports 1 to 1024 |
| `nmap -p- 127.0.0.1` | Scan all 65535 ports |
| `nmap -sV 127.0.0.1` | Detect service versions |
| `nmap -O 127.0.0.1` | Detect the operating system (needs root) |
| `nmap -sn 192.168.1.0/24` | Find live hosts without port scanning |

### What is a port scan?

Every network service listens on a numbered **port** (SSH on 22, HTTP on 80, HTTPS on 443, and so on). A port scanner tries to connect to each port and reports which ones answer. Open ports show what a machine is offering to the network, which is why scanning is a core step in security assessments.

---

## What this project does

This script performs a **TCP connect scan**, the simplest scan type:

1. It resolves the target hostname to an IP address.
2. For each port in the list, it tries to open a TCP connection.
3. If the connection succeeds (`connect_ex` returns `0`), the port is **open** and gets printed.
4. Otherwise the port is closed or filtered and is skipped.

### Comparison with real Nmap

| Feature | This script | Nmap |
|---|---|---|
| TCP connect scan | Yes | Yes |
| Hostname resolution | Yes | Yes |
| Speed (multi-threaded / SYN scan) | No | Yes |
| Service/version detection | No | Yes |
| OS detection | No | Yes |
| Scripting engine | No | Yes |
| UDP scanning | No | Yes |

---

## Requirements

- Python 3.8 or newer
- No external libraries (only the standard library `socket` module)

## Installation

```bash
git clone https://github.com/AllainDasantad/Nmap-scanner.git
cd Nmap-scanner
```

## Usage

```bash
python nmap_scan.py
```

(Use `python3` if `python` is not found.)

When prompted, enter a target IP address or hostname:

```
Target: 127.0.0.1
Port 8000 is Open
```

Only open ports are printed. If nothing appears, no open ports were found in the scanned range.

### Changing the port range

Open `nmap_scan.py` and edit the `ports` line:

```python
ports = range(1, 1025)      # well-known ports
ports = range(1, 9001)      # ports 1 to 9000
ports = [22, 80, 443, 8000] # specific ports only
```

## Try it yourself

To get a guaranteed open port on your own machine:

**1.** In a second terminal, start a test web server:

```bash
python -m http.server 8000
```

**2.** Make sure your port range includes 8000 (for example `range(1, 9001)`).

**3.** Run the scanner against `127.0.0.1`. You should see:

```
Port 8000 is Open
```

**4.** Identify what owns a port (Linux):

```bash
ss -ltnp | grep 8000
```

**5.** Compare the result with real Nmap:

```bash
nmap -p 1-9000 127.0.0.1
```

## How the code works

```python
import socket

target = input("Target: ")
ports = range(1, 1025)

try:
    ip = socket.gethostbyname(target)   # hostname -> IP address
except socket.gaierror:
    raise SystemExit("Could not resolve host")

for port in ports:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)                       # don't wait forever
        if sock.connect_ex((ip, port)) == 0:       # 0 means connected
            print(f"Port {port} is Open")
```

- `AF_INET` means IPv4, and `SOCK_STREAM` means TCP.
- `settimeout(0.5)` stops the scan from hanging on filtered ports.
- `connect_ex` returns an error code instead of raising an exception, so `0` means success.
- The `with` block closes each socket automatically.

## Limitations

- Ports are scanned one at a time, so scanning remote hosts is slow.
- Only IPv4 and TCP are supported.
- It cannot tell "closed" apart from "filtered by a firewall".
- It does not identify which service is running on an open port.

## Roadmap

- [ ] Multi-threading with `concurrent.futures.ThreadPoolExecutor`
- [ ] Banner grabbing to show the service behind each open port
- [ ] Command-line arguments with `argparse` (e.g. `-p 1-9000`)
- [ ] Save results to a file
