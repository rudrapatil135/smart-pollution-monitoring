# pollution/services/weatherapi_service.py
import requests
import pandas as pd
import os

WEATHERAPI_KEY = "38f0847d929b41e1ad663748262001"
WEATHERAPI_URL = "https://api.weatherapi.com/v1/current.json"

NCR_POINTS = [
    {"name": "Connaught Place", "lat": 28.6139, "lon": 77.2090},
    {"name": "Noida Sector 62", "lat": 28.5355, "lon": 77.3910},
    {"name": "Ghaziabad", "lat": 28.6692, "lon": 77.4538},
    {"name": "Gurugram", "lat": 28.4595, "lon": 77.0266},
    {"name": "Faridabad", "lat": 28.4089, "lon": 77.3178},
    {"name": "Greater Noida", "lat": 28.4744, "lon": 77.5040},
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
            r = requests.get(WEATHERAPI_URL, params=params, timeout=6)
            r.raise_for_status()
            data = r.json()
            
            air = data["current"]["air_quality"]
            pm25 = air["pm2_5"]
            pm10 = air["pm10"]

            # Save the location name returned by the API
            location_name = data["location"]["name"]

            records.append({
                "station": location_name,  # <-- use API’s city name here
                "latitude": p["lat"],
                "longitude": p["lon"],
                "pm25": round(pm25, 2),
                "pm10": round(pm10, 2)
            })

        except Exception as e:
            print("WeatherAPI error:", e)

    return records
