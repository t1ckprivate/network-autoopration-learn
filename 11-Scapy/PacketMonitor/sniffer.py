import requests
import socketio
from scapy.all import sniff, IP

# Establish WebSocket client connection
sio = socketio.Client()
sio.connect("http://127.0.0.1:23323" , namespaces=['/'])  # 

# Define the network interface for packet sniffing
iface = "以太网"  # Replace with your actual interface name

# Packet processing function
def packet_callback(pkt):
    """Processes incoming packets, extracts IP information, and sends it via WebSocket."""
    if IP in pkt:
        data = {
            "source_ip": pkt[IP].src,   # Extract source IP address
            "destination_ip": pkt[IP].dst,  # Extract destination IP address
            "size": len(pkt)  # Extract packet size in bytes
        }
        print(f"📡 Sending: {data}")
        sio.emit('send_ip', data)  # Transmit IP data to the WebSocket server

# Start sniffing on the specified network interface
sniff(iface=iface, filter="tcp", prn=packet_callback, store=False)
