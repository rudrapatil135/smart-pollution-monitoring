from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def source_attribution(request):
    if request.user.profile.role != "policy":
        return redirect("home")

    return render(request, "policy/source_attribution.html")
