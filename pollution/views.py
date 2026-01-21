from django.http import JsonResponse
from django.shortcuts import render
from project.backend.services.realtime_aqi_service import fetch_realtime_delhi_pm25
import random

# CPCB-style predefined stations (Delhi-NCR)
STATIONS = [
    {"station": "Anand Vihar", "lat": 28.6508, "lon": 77.3025},
    {"station": "RK Puram", "lat": 28.5636, "lon": 77.1865},
    {"station": "Dwarka Sector 8", "lat": 28.5744, "lon": 77.0713},
    {"station": "Punjabi Bagh", "lat": 28.6742, "lon": 77.1296},
    {"station": "Rohini Sector 16", "lat": 28.7435, "lon": 77.1154},
    {"station": "Mundka", "lat": 28.6831, "lon": 77.0202},
    {"station": "Vivek Vihar", "lat": 28.6716, "lon": 77.3152},
    {"station": "Okhla Phase 2", "lat": 28.5310, "lon": 77.2770},
    {"station": "Saket", "lat": 28.5245, "lon": 77.2066},
    {"station": "Nehru Place", "lat": 28.5494, "lon": 77.2509},
    {"station": "Noida Sector 62", "lat": 28.6273, "lon": 77.3724},
    {"station": "Noida Sector 125", "lat": 28.5440, "lon": 77.3337},
    {"station": "Greater Noida", "lat": 28.4744, "lon": 77.5040},
    {"station": "Indirapuram", "lat": 28.6465, "lon": 77.3690},
    {"station": "Vasundhara", "lat": 28.6771, "lon": 77.4526},
    {"station": "Faridabad Sector 15", "lat": 28.4089, "lon": 77.3178},
    {"station": "Faridabad NIT", "lat": 28.3910, "lon": 77.3050},
    {"station": "Gurgaon Sector 29", "lat": 28.4667, "lon": 77.0654},
    {"station": "Udyog Vihar", "lat": 28.5106, "lon": 77.0806},
    {"station": "Manesar", "lat": 28.3547, "lon": 76.9517},
]

def aqi_api(request):
    data = []
    for s in STATIONS:
        pm25 = round(random.uniform(40, 180), 2)
        data.append({
            "station": s["station"],
            "latitude": s["lat"],
            "longitude": s["lon"],
            "pm25": pm25
        })
    return JsonResponse({"data": data})

# Dashboard view
def dashboard(request):
    return render(request, "index.html")
