from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import login as auth_login 
from base.forms import SignUpForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def dashboard(request):
    return render(request,"accounts/home.html")
def home(request):
    return render(request,"accounts/home.html")
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('dashboard')  # <- redirect prevents resubmission
        else:
            messages.error(request, "Invalid username or password")
            return redirect('home')
    return render(request, "accounts/login.html")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # saves User
            
            # Create Profile immediately after creating user
            Profile.objects.create(
                user=user,
                city=form.cleaned_data.get('city'),
                role=form.cleaned_data.get('role')
            )

            messages.success(request, 'Account created successfully! Please login.')
            login(request)  # optional: log the user in directly
            return redirect('login')  # redirect to homepage
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
