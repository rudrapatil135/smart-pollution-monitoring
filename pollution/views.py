from django.http import JsonResponse
from django.shortcuts import render
from project.backend.services.realtime_aqi_service import fetch_realtime_delhi_pm25

# API endpoint for AJAX
def aqi_api(request):
    city = request.GET.get('city', 'Delhi')
    data_df = fetch_realtime_delhi_pm25()  # returns a DataFrame

    # Convert to list of dicts
    data_list = data_df.to_dict(orient='records')

    return JsonResponse({"data": data_list}, safe=False)
# Dashboard view
def dashboard(request):
    return render(request, "index.html")
