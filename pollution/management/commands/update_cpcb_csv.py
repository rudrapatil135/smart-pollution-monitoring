from django.core.management.base import BaseCommand
import requests
import pandas as pd
import os
from datetime import datetime
from django.conf import settings

# ================= CONFIG =================
WEATHER_API_KEY = "8b00b4b61e6c4bf5b05123641261401"

CSV_PATH = os.path.join(
    settings.BASE_DIR,
    "pollution",
    "data",
    "cpcb_delhi_stations.csv"
)

STATIONS = {
    "Anand Vihar": (28.6469, 77.3159),
    "Rohini": (28.7499, 77.0565),
    "Dwarka": (28.5921, 77.0460),
    "Punjabi Bagh": (28.6741, 77.1310),
    "Noida Sector 62": (28.6271, 77.3731),
    "Gurugram Sector 29": (28.4675, 77.0723),
}

# ================= COMMAND =================
class Command(BaseCommand):
    help = "Update CPCB AQI CSV using WeatherAPI (near real-time)"

    def handle(self, *args, **kwargs):
        rows = []

        for station, (lat, lon) in STATIONS.items():
            url = (
                "http://api.weatherapi.com/v1/current.json"
                f"?key={WEATHER_API_KEY}&q={lat},{lon}&aqi=yes"
            )

            try:
                r = requests.get(url, timeout=10)
                data = r.json()

                air = data["current"]["air_quality"]

                pm25 = air["pm2_5"]
                pm10 = air["pm10"]

                rows.append({
                    "station": station,
                    "lat": lat,
                    "lon": lon,
                    "pm25": round(pm25, 2),
                    "pm10": round(pm10, 2),
                    "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M")
                })

            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"Skipping {station}: {e}")
                )

        if rows:
            df = pd.DataFrame(rows)
            df.to_csv(CSV_PATH, index=False)
            self.stdout.write(
                self.style.SUCCESS("WeatherAPI AQI CSV updated successfully")
            )
        else:
            self.stdout.write(
                self.style.ERROR("No AQI data fetched — CSV unchanged")
            )
