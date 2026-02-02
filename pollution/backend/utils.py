def pm25_to_aqi(pm25):
    if pm25 <= 50:
        return pm25
    elif pm25 <= 100:
        return pm25 * 1.5
    elif pm25 <= 200:
        return pm25 * 1.8
    elif pm25 <= 300:
        return pm25 * 2
    else:
        return pm25 * 2.2
