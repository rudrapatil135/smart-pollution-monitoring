from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
from django.utils import timezone
from datetime import timedelta
from .models import PollutantReading
import logging
logger = logging.getLogger(__name__)
from django.http import JsonResponse
# ---------------------------
# Policy Views
# ---------------------------

@login_required
def source_attribution(request):
    """Render source attribution page for policy users."""
    if getattr(request.user, 'profile', None) and request.user.profile.role != "policy":
        return redirect("home")
    return render(request, "policy/source_attribution.html")


@login_required
def policy_simulation(request):
    """Render policy simulation page for policy users."""
    if getattr(request.user, 'profile', None) and request.user.profile.role != "policy":
        return redirect("home")
    return render(request, "policy/policy_simulation.html")


@login_required
def policy_dashboard(request):
    """Render pollutant dashboard for policy users."""
    if getattr(request.user, 'profile', None) and request.user.profile.role != "policy":
        return redirect("home")
    return render(request, "policy/pollutant_dashboard.html")


# ---------------------------
# Live Pollutants API
# ---------------------------

@login_required
def live_pollutants(request):
    """
    Fetch live pollutant data from WAQI API (Delhi example).
    Returns JSON with PM2.5, PM10, NO2, SO2, CO, O3.
    """
    url = "https://api.waqi.info/feed/delhi/?token=32da23f87c9de2c4bfb3421d7d6121869ce8980a"
    pollutants = {"PM2.5": 0, "PM10": 0, "NO2": 0, "SO2": 0, "CO": 0, "O3": 0}

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        iaqi = data.get('data', {}).get('iaqi', {})

        pollutants = {
            "PM2.5": iaqi.get('pm25', {}).get('v', 0),
            "PM10": iaqi.get('pm10', {}).get('v', 0),
            "NO2": iaqi.get('no2', {}).get('v', 0),
            "SO2": iaqi.get('so2', {}).get('v', 0),
            "CO": iaqi.get('co', {}).get('v', 0),
            "O3": iaqi.get('o3', {}).get('v', 0),
        }

    except Exception as e:
        logger.error(f"Error fetching live pollutants: {e}")

    return JsonResponse(pollutants)


# ---------------------------
# Historical Trends API (Last 7 days)
# ---------------------------

@login_required
def last_hour_pollutants(request):
    one_hour_ago = timezone.now() - timedelta(hours=1)
    readings = PollutantReading.objects.filter(timestamp__gte=one_hour_ago)
    
    data = {
        "time": [r.timestamp.strftime("%H:%M") for r in readings],
        "PM2.5": [r.pm25 for r in readings],
        "PM10": [r.pm10 for r in readings],
        "NO2": [r.no2 for r in readings],
        "SO2": [r.so2 for r in readings],
        "CO": [r.co for r in readings],
        "O3": [r.o3 for r in readings],
    }
    return JsonResponse(data)
# ---------------------------
# AI Policy Decision API
# ---------------------------

@csrf_exempt
def ai_policy_decision(request):
    """
    Simple AI logic to suggest policy priority based on sector contribution.
    Input: vehicle, stubble, industry (POST)
    Output: JSON with priority, summary, advice
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        vehicle = float(request.POST.get("vehicle", 0))
        stubble = float(request.POST.get("stubble", 0))
        industry = float(request.POST.get("industry", 0))

        # Simple policy pressure calculation
        policy_pressure = (vehicle * 0.4) + (stubble * 0.35) + (industry * 0.45)

        if policy_pressure < 30:
            result = {
                "priority": "LOW ✅",
                "summary": "Minimal policy intervention detected.",
                "advice": "Maintain monitoring and awareness."
            }
        elif policy_pressure < 70:
            result = {
                "priority": "MODERATE 🟡",
                "summary": "Moderate pollution control in effect.",
                "advice": "Strengthen vehicle and stubble controls."
            }
        else:
            result = {
                "priority": "HIGH ⚠️",
                "summary": "Aggressive pollution control required.",
                "advice": "Enforce strict multi-sector restrictions immediately."
            }

        return JsonResponse(result)

    except ValueError as e:
        logger.error(f"Invalid input for AI policy decision: {e}")
        return JsonResponse({"error": "Invalid numeric input"}, status=400)
