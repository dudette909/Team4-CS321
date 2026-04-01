from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


from django.contrib.auth.models import User


# Create your views here.
def landingPage(request):
    return render(request, "main/landingPage.html")


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "main/login.html")


def registerPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("registerPage")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("registerPage")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("registerPage")

        user = User.objects.create_user(
            username=username, email=email, password=password1
        )

        return redirect("loginPage")

    return render(request, "main/register.html")


@login_required
def dashboard(request):
    return render(request, "main/dashboard.html")
