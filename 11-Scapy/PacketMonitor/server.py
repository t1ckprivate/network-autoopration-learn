import time

import requests
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__, static_folder="static", template_folder="templates")
socketio = SocketIO(app, cors_allowed_origins="*")

# Cache for IP geolocation (stored in memory)
geo_cache = {}


def get_geolocation(ip):
    """
    Retrieves geolocation data for a given IP address using an external API.
    Uses caching to reduce redundant API requests (24-hour expiration).
    """
    if ip.startswith(("192.", "127.", "10.", "172.", "0.")):
        print(f"⏭ Skipping private IP: {ip}")
        return None

    if ip in geo_cache and (time.time() - geo_cache[ip]["timestamp"]) < 86400:
        print(f"✅ Cache hit: {ip}")
        return geo_cache[ip]["data"]

    url = f"http://ip-api.com/json/{ip}?fields=lat,lon,city,country,query"
    print(f"🌐 Querying API: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"🔁 API response status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📦 API raw response: {data}")
            lat = data.get("lat")
            lon = data.get("lon")
            if lat is None or lon is None:
                print(f"⚠ No coordinates in API response: {data}")
                return None
            geo_data = {
                "ip": data.get("query", ip),
                "lat": lat,
                "lon": lon,
                "city": data.get("city", ""),
                "country": data.get("country", ""),
            }
            geo_cache[ip] = {"data": geo_data, "timestamp": time.time()}
            print(f"✅ Geo resolved: {geo_data}")
            return geo_data
        else:
            print(
                f"⚠ API returned status {response.status_code}: {response.text[:200]}"
            )
    except requests.exceptions.RequestException as e:
        print(f"⚠ Geolocation API error: {e}")

    return None


@socketio.on("send_ip")
def handle_ip(data):
    """
    WebSocket event handler that receives IP data from the sniffer,
    retrieves geolocation information, and forwards it to clients.
    """
    print(f"📡 Received from sniffer: {data}")

    dest_ip = data.get("destination_ip")
    packet_size = data.get("size", 0)

    if dest_ip:
        geo_data = get_geolocation(dest_ip)
        if geo_data:
            geo_data["size"] = packet_size
            print(f"🚀 Emitting update_map: {geo_data}")
            socketio.emit("update_map", geo_data)
        else:
            print(f"⏭ No geo data for {dest_ip}, skipping")
    else:
        print("⚠ No destination_ip in data")


@app.route("/")
def serve_index():
    """
    Serves the index.html file when users access the root URL.
    """
    return render_template("index.html")


# Start Flask WebSocket server
if __name__ == "__main__":
    print("🚀 Starting server on http://0.0.0.0:23323")
    socketio.run(app, host="0.0.0.0", port=23323, debug=True)
