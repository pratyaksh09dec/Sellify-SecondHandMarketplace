from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, RegisterForm
from .models import get_profile

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            get_profile(user)   
            login(request, user)   
            messages.success(request, "Welcome to Sellify! Add your phone and city below.")
            return redirect("profile")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_view(request):
    profile = get_profile(request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile saved.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "accounts/profile.html", {"form": form})
