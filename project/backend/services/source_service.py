def normalize(d):
    total = sum(d.values())
    return {k: round(v / total * 100, 1) for k, v in d.items()}

def estimate_sources(pm25, wind_ms):
    background = 25

    if pm25 > 120 and wind_ms < 2:
        traffic = 55
    elif pm25 > 80:
        traffic = 35
    else:
        traffic = 20

    if pm25 > 100 and wind_ms > 3:
        regional = 45
    elif pm25 > 70:
        regional = 30
    else:
        regional = 15

    return normalize({
        "traffic": traffic,
        "regional_transport": regional,
        "background": background
    })
