def calculate_aqi_pm25(pm25):
    pm25 = float(pm25)
    if pm25 <= 30:
        return pm25 * 50 / 30, "Good"
    elif pm25 <= 60:
        return 51 + (pm25 - 30) * 49 / 30, "Satisfactory"
    elif pm25 <= 90:
        return 101 + (pm25 - 60) * 99 / 30, "Moderate"
    elif pm25 <= 120:
        return 201 + (pm25 - 90) * 99 / 30, "Poor"
    else:
        return 301 + (pm25 - 120) * 100 / 80, "Severe"
