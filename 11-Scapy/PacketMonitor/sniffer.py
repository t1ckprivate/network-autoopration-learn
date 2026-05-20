import time

import socketio
from scapy.all import IP, sniff

# ==================== Rate Limiter Config ====================
MAX_PACKETS_PER_SEC = 5  # Max packets to emit per second
# ============================================================


# Establish WebSocket client connection (with auto-retry)
def connect_with_retry(url, retry_delay=2):
    """Keep trying to connect until server is available."""
    while True:
        try:
            sio.connect(url, namespaces=["/"])
            print(f"✅ Connected to {url}")
            return
        except Exception as e:
            print(f"⏳ Server not ready ({e}), retrying in {retry_delay}s...")
            time.sleep(retry_delay)


sio = socketio.Client()
connect_with_retry("http://127.0.0.1:23323")

# Define the network interface for packet sniffing
iface = "以太网"  # Replace with your actual interface name

# Rate limiter state
last_emit = 0.0
dropped = 0
total = 0
last_report = time.time()


def packet_callback(pkt):
    """Processes incoming packets, extracts IP information, and sends it via WebSocket."""
    global last_emit, dropped, total, last_report

    if IP not in pkt:
        return

    total += 1
    now = time.time()
    interval = 1.0 / MAX_PACKETS_PER_SEC

    # Rate limit: skip if not enough time has passed since last emit
    if now - last_emit < interval:
        dropped += 1
        # Periodic stats report every 5 seconds
        if now - last_report >= 5:
            print(
                f"⏱ Rate limit: {dropped}/{total} dropped ({(dropped / total) * 100:.0f}%), {MAX_PACKETS_PER_SEC} pps max"
            )
            last_report = now
        return

    last_emit = now

    data = {
        "source_ip": pkt[IP].src,
        "destination_ip": pkt[IP].dst,
        "size": len(pkt),
    }
    print(f"📡 Sending: {data}")
    sio.emit("send_ip", data)


# Start sniffing on the specified network interface
print(f"🔍 Sniffing on '{iface}' (TCP only, max {MAX_PACKETS_PER_SEC} pps)...")
sniff(iface=iface, filter="tcp", prn=packet_callback, store=False)
