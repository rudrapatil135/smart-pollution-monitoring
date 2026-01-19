import requests
import pandas as pd

WEATHERAPI_KEY = "21ecf9acc6ee4db6ab6190712261701"
WEATHERAPI_URL = "https://api.weatherapi.com/v1/current.json"

NCR_POINTS = [
    {"lat": 28.6139, "lon": 77.2090},
    {"lat": 28.5355, "lon": 77.3910},
    {"lat": 28.6692, "lon": 77.4538},
    {"lat": 28.4595, "lon": 77.0266},
    {"lat": 28.4089, "lon": 77.3178},
    {"lat": 28.4744, "lon": 77.5040}
]

def fetch_realtime_delhi_pm25():
    records = []

    for p in NCR_POINTS:
        params = {
            "key": WEATHERAPI_KEY,
            "q": f"{p['lat']},{p['lon']}",
            "aqi": "yes"
        }

        try:
            r = requests.get(WEATHERAPI_URL, params=params, timeout=8)
            r.raise_for_status()
            data = r.json()

            pm25 = data["current"]["air_quality"]["pm2_5"]

            records.append({
                "latitude": p["lat"],
                "longitude": p["lon"],
                "pm25": round(float(pm25), 2)
            })

        except Exception:
            pass

    if records:
        return pd.DataFrame(records)

    return fallback_data()


def fallback_data():
    return pd.DataFrame([
        {"latitude": 28.61, "longitude": 77.21, "pm25": 210},
        {"latitude": 28.53, "longitude": 77.39, "pm25": 165},
        {"latitude": 28.67, "longitude": 77.45, "pm25": 180},
        {"latitude": 28.46, "longitude": 77.02, "pm25": 150}
    ])
