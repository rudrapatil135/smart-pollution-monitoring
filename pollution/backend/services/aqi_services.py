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
def calculate_sub_index(concentration, c_low, c_high, i_low, i_high):
    return ((i_high - i_low) / (c_high - c_low)) * (concentration - c_low) + i_low
def calculate_aqi_pm10(pm10):
    pm10 = float(pm10)

    if pm10 <= 50:
        return calculate_sub_index(pm10, 0, 50, 0, 50)

    elif pm10 <= 100:
        return calculate_sub_index(pm10, 51, 100, 51, 100)

    elif pm10 <= 250:
        return calculate_sub_index(pm10, 101, 250, 101, 200)

    elif pm10 <= 350:
        return calculate_sub_index(pm10, 251, 350, 201, 300)

    elif pm10 <= 430:
        return calculate_sub_index(pm10, 351, 430, 301, 400)

    else:
        return calculate_sub_index(pm10, 431, 600, 401, 500)
