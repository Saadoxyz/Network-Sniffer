# Network Sniffer

[![Project Status](https://img.shields.io/badge/status-experimental-yellow)](https://github.com/)
[![Language](https://img.shields.io/badge/language-Python-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> Lightweight Python-based network sniffer for educational use — captures and displays IP-layer traffic (source/destination IPs, protocol, payload snippets). Designed for learning and demonstration; **not** a production packet-capture appliance.

---

## Overview

This repository contains a compact Python network sniffer intended for learning and demonstration. It inspects **Layer 3 (IP)** traffic, identifying source/destination IPs, protocol (TCP/UDP/ICMP/other) and displays short payload snippets when available.

The project emphasizes:

* clarity of implementation for educational purposes
* portability to restricted environments where driver installation (Npcap/WinPcap) is not possible
* safe and ethical usage guidance

---

## Features

* Capture IP-level traffic on Windows, macOS and Linux
* Identify common protocols (TCP/UDP/ICMP) and display human-friendly names
* Show small payload snippets to illustrate packet contents
* Built-in Layer-3 fallback to avoid dependency on WinPcap/Npcap
* Configurable stop conditions: packet count, timeout or custom stop filter

---

## Architecture & How it Works

The core is a Scapy-based sniffer. When Npcap/WinPcap is available, Scapy can perform Layer-2 captures (Ethernet frames). On restricted systems this project uses Scapy's `L3socket` as an explicit fallback so it can still read IP packets without libpcap.

High-level flow:

1. Prepare socket: prefer native pcap provider; if unavailable, use `conf.L3socket()`.
2. Start `sniff()` with a `packet_callback` that parses `IP`, `TCP`, `UDP`, `ICMP` layers.
3. Format and print concise, human-readable lines with optional payload preview.
4. Stop according to `count`, `timeout` or `stop_filter` (configurable).

---

## Requirements

* Python 3.8+
* scapy

Optional (for Layer-2 capture on Windows):

* Npcap (WinPcap-compatible) installed and configured.

Install Python dependencies:

```bash
pip install scapy
```

> On Windows, Npcap is recommended for Layer-2 Ethernet sniffing. If you cannot install it, the Layer-3 fallback still works and is used by default in this project.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/Network-Sniffer.git
cd Network-Sniffer
```

2. Create a virtual environment (recommended):

```bash
python -m venv .venv
# On Windows
.\.venv\Scripts\activate
# On macOS / Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
# or
pip install scapy
```

4. (Windows only, optional) Install Npcap if you want Ethernet-layer captures.

---

## Usage

Run the sniffer script. Administrator/root privileges are generally required when sniffing network traffic.

Basic run (Layer-3 fallback used if pcap is not available):

```bash
python Network_sniffer.py
```

Recommended run with a short demo timeout (safe for demos):

```bash
python Network_sniffer.py --timeout 30
```

Capture a fixed number of packets and exit:

```bash
python Network_sniffer.py --count 100
```

If the system blocks Layer-2 access, the script automatically uses:

```python
# internal snippet used by this project (simplified)
from scapy.all import conf
conf.use_pcap = False
sniff(prn=packet_callback, store=False, opened_socket=conf.L3socket())
```

### Command-line options (recommended)

* `--count N` — stop after N packets
* `--timeout S` — stop after S seconds
* `--iface NAME` — sniff on specific interface (if supported)
* `--verbose` — print extended packet details

(Hint: the sample script includes an `argparse` wrapper you can enable for these flags.)

---

## Examples (sample output)

```
[+] 192.168.1.5 --> 142.250.190.46 | Protocol: TCP
    Payload: b'GET / HTTP/1.1\r\nHost: www.google.com...'

[+] 192.168.1.5 --> 8.8.8.8 | Protocol: UDP
    Payload: b'\x12\x34\x01\x00...'
```

Include screenshots in `/assets` for visual demonstration. Suggested images:

* `assets/sniffer_terminal.png` — terminal output showing sample packets
* `assets/architecture_diagram.png` — small diagram showing Layer-2 vs Layer-3 behavior

Add those files to the repository and reference them in the README with standard Markdown image links.

---

## Troubleshooting

* **"No libpcap provider available" / WinPcap not installed**: This project supports Layer-3 fallback. If you need Ethernet frames on Windows, install Npcap (WinPcap-compatible) and restart.
* **Permission errors**: Run the terminal as Administrator (Windows) or use `sudo` on macOS/Linux.
* **Too much output**: Use `--timeout` or `--count` to limit capture duration; add filters to the callback to ignore irrelevant traffic.

---

## Ethics, Safety & Legal

This project is for **educational and authorized** use only. Packet sniffing can capture sensitive information (credentials, session tokens, personal data). Do **not** run this tool on networks you do not own or do not have explicit permission to analyze.

By using this code you agree to follow local laws and institutional policies. The author is not responsible for misuse.

---

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Open a pull request with a clear description of the change

Suggested improvements:

* Add argparse CLI and filters (e.g., only show TCP and DNS traffic)
* Add structured logging to file (CSV/JSON)
* Build a small UI dashboard for visualizing packet rates and top talkers

---


## Acknowledgements

* Instagram reel that inspired this weekend project (credit to the original creator)
* Scapy project ([https://scapy.net](https://scapy.net)) — excellent packet manipulation library

---

*Prepared as an educational demo and part of a personal learning project.*
