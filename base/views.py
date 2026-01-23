from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Profile
from base.forms import SignUpForm


def home(request):
    return render(request, "accounts/home.html")


@login_required
def dashboard(request):
    return render(request, "accounts/home.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 ROLE CHECK
            if user.profile.role == "policy":
                return redirect("source_attribution")
            else:
                return redirect("home")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            Profile.objects.create(
                user=user,
                city=form.cleaned_data["city"],
                role=form.cleaned_data["role"],
            )

            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")

    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
