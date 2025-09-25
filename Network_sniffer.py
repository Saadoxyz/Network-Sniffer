from scapy.all import sniff, IP, TCP, UDP, conf

# Force Scapy to use Layer 3 sockets (skip pcap requirement)
conf.use_pcap = False

def packet_callback(packet):
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        proto = packet[IP].proto

        # Detect protocol
        if proto == 6:
            protocol = "TCP"
        elif proto == 17:
            protocol = "UDP"
        elif proto == 1:
            protocol = "ICMP"
        else:
            protocol = f"Other ({proto})"

        print(f"[+] {ip_src} --> {ip_dst} | Protocol: {protocol}")

        # Show small part of payload if available
        if packet.haslayer(TCP) or packet.haslayer(UDP):
            payload = bytes(packet[TCP].payload) if packet.haslayer(TCP) else bytes(packet[UDP].payload)
            if payload:
                print(f"    Payload: {payload[:50]}...")  # First 50 bytes

print("Starting packet sniffer (Layer 3 only)... Press Ctrl+C to stop")

# 👇 The key change: tell sniff() to use Layer 3 socket
sniff(prn=packet_callback, store=False, opened_socket=conf.L3socket())
