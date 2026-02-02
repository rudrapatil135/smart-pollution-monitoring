def build_alert(name, forecast):
    peak = max(forecast, key=lambda x: x["aqi"])
    aqi = peak["aqi"]

    if aqi <= 50:
        level = "GOOD"
        msg = "Excellent air quality. Ideal for all outdoor activities."
    elif aqi <= 100:
        level = "MODERATE"
        msg = "Air quality acceptable. Sensitive individuals should be cautious."
    elif aqi <= 200:
        level = "POOR"
        msg = "Poor air quality. Reduce prolonged outdoor exertion."
    elif aqi <= 300:
        level = "VERY POOR"
        msg = "Very poor air quality. Avoid outdoor activity."
    else:
        level = "SEVERE"
        msg = "Severe pollution. Stay indoors and follow health advisories."

    return {
        "location": name,
        "aqi": aqi,
        "level": level,
        "message": msg,
        "time": peak["time"]
    }
