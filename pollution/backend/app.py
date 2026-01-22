from flask import Flask, jsonify
from flask_cors import CORS
import requests

from services.realtime_aqi_service import fetch_realtime_delhi_pm25
from services.aqi_services import calculate_aqi_pm25
from services.source_service import estimate_sources

app = Flask(__name__)
CORS(app)

WEATHERAPI_KEY = "8b00b4b61e6c4bf5b05123641261401"
WEATHERAPI_URL = "https://api.weatherapi.com/v1/current.json"


@app.route("/aqi/realtime")
def realtime_aqi():
    df = fetch_realtime_delhi_pm25()
    out = []

    for _, r in df.iterrows():
        aqi, category = calculate_aqi_pm25(r["pm25"])
        out.append({
            "latitude": r["latitude"],
            "longitude": r["longitude"],
            "pm25": r["pm25"],
            "aqi": round(aqi),
            "category": category
        })

    return jsonify({"city": "Delhi-NCR", "data": out})


@app.route("/aqi/source")
def source():
    df = fetch_realtime_delhi_pm25()
    results = []

    for _, r in df.iterrows():
        params = {
            "key": WEATHERAPI_KEY,
            "q": f"{r['latitude']},{r['longitude']}",
            "aqi": "no"
        }

        try:
            w = requests.get(WEATHERAPI_URL, params=params).json()
            wind = w["current"]["wind_kph"] / 3.6
        except Exception:
            wind = 1.5

        sources = estimate_sources(r["pm25"], wind)

        results.append({
            "latitude": r["latitude"],
            "longitude": r["longitude"],
            "pm25": r["pm25"],
            "wind_ms": round(wind, 2),
            "sources": sources
        })

    return jsonify({"city": "Delhi-NCR", "points": results})


if __name__ == "__main__":
    app.run(debug=True)
