from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request,"base/dashboard.html")
def home(request):
    return render(request,"accounts/home.html")