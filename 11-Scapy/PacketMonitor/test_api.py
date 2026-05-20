"""Quick test: verify ip-api.com geolocation API is reachable."""

import requests

# Test with a known public IP (Google DNS)
test_ip = "8.8.8.8"

# Try both URL formats
urls = [
    f"http://ip-api.com/json/{test_ip}?fields=lat,lon,city,country,query",
    f"http://ip-api.com/{test_ip}/json/",
]

for url in urls:
    print(f"🌐 Trying: {url}")
    try:
        r = requests.get(url, timeout=10)
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"  Response: {data}")
            lat = data.get("lat")
            lon = data.get("lon")
            if lat and lon:
                print(
                    f"  ✅ SUCCESS: lat={lat}, lon={lon}, country={data.get('country')}"
                )
            else:
                print(f"  ⚠ No lat/lon in response - keys: {list(data.keys())}")
        else:
            print(f"  ❌ Failed: {r.text[:200]}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    print()
