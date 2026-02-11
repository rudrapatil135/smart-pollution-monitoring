
from pollution.backend.services.realtime_aqi_service import fetch_realtime_delhi_pm25
from pollution.backend.services.aqi_services import calculate_aqi_pm25 as aqi_pm25
from pollution.backend.services.aqi_services import calculate_aqi_pm10 as aqi_pm10
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@csrf_exempt
def station_aqi(request):
    stations = fetch_realtime_delhi_pm25()
    data = []

    for s in stations:
        pm25 = s["pm25"]
        pm10 = s["pm10"]

        # Get AQI values (numeric) only
        aqi_25_value = aqi_pm25(pm25)
        aqi_10_value = aqi_pm10(pm10)

        # If these functions return a tuple like (value, category), pick the first element
        if isinstance(aqi_25_value, tuple):
            aqi_25_value = aqi_25_value[0]
        if isinstance(aqi_10_value, tuple):
            aqi_10_value = aqi_10_value[0]

        data.append({
            "station": s["station"],
            "latitude": s["latitude"],
            "longitude": s["longitude"],
            "pm25": pm25,
            "pm10": pm10,
            "aqi": round(max(aqi_25_value, aqi_10_value), 2)
        })

    return JsonResponse({"data": data})
@login_required(login_url='login')
def pollution_page(request):
    return render(request, "pollution/index.html")
def map_view(request):
    return render(request,'map.html')
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def forecast_api(request):
    data = [
        {
            "name": "Anand Vihar",
            "lat": 28.6469,
            "lon": 77.3159,
            "forecast": [
                {"aqi": 275},
                {"aqi": 280}
            ]
        },
        {
            "name": "RK Puram",
            "lat": 28.5672,
            "lon": 77.2100,
            "forecast": [
                {"aqi": 180},
                {"aqi": 190}
            ]
        }
    ]
    return JsonResponse(data, safe=False)

