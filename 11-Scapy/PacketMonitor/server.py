from flask import Flask, render_template
from flask_socketio import SocketIO
import requests
import time
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
socketio = SocketIO(app, cors_allowed_origins="*")

# Cache for IP geolocation (stored in memory)
geo_cache = {}

def get_geolocation(ip):
    """
    Retrieves geolocation data for a given IP address using an external API.
    Uses caching to reduce redundant API requests (24-hour expiration).
    """
    if ip.startswith(("192.", "127.", "10.")):  # Ignore private/internal IPs
        return None

    if ip in geo_cache and (time.time() - geo_cache[ip]["timestamp"]) < 86400:
        print(f"✅ Cache hit: {ip}")
        return geo_cache[ip]["data"]

    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            geo_data = {
                "ip": ip,
                "lat": data.get("loc").split(",")[0],
                "lon": data.get("loc").split(",")[1],
                "city": data.get("city"),
                "country": data.get("country")
            }
            geo_cache[ip] = {"data": geo_data, "timestamp": time.time()}
            print(f"📡 API response stored: {geo_data}")
            return geo_data
    except requests.exceptions.RequestException as e:
        print(f"⚠ Geolocation API error: {e}")

    return None

@socketio.on('send_ip')
def handle_ip(data):
    """
    WebSocket event handler that receives IP data from the sniffer,
    retrieves geolocation information, and forwards it to clients.
    """
    print(f"📡 Received IP data: {data}")

    dest_ip = data.get("destination_ip")
    packet_size = data.get("size", 0)

    if dest_ip:
        geo_data = get_geolocation(dest_ip)
        if geo_data:
            geo_data["size"] = packet_size
            socketio.emit('update_map', geo_data)

@app.route("/")
def serve_index():
    """
    Serves the index.html file when users access the root URL.
    """
    return render_template("index.html")

# Start Flask WebSocket server
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=23323, debug=True)
