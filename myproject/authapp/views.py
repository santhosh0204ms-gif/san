from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Signup with auto-login
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "signup.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already exists"})

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Automatically log the user in
        user = authenticate(request, username=username, password=password1)
        if user is not None:
            login(request, user)
            return redirect("profile")  # Redirect to profile page after signup

    return render(request, "signup.html")

# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile") 
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})
    return render(request, "login.html")

# Profile (protected)
@login_required(login_url='login')
def profile_view(request):
    return render(request, "profile.html")

# Logout
def logout_view(request):
    logout(request)
    return redirect("login")
