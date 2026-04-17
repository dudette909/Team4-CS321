from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import random
from django.contrib.auth.models import User
from .models import Player
from .utils import *
from .models import Game
import json
from django.http import JsonResponse


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
        Player.objects.create(user=user)
        return redirect("loginPage")

    return render(request, "main/register.html")


@login_required
def dashboard(request):
    now = timezone.localtime()

    day = now.strftime("%A")
    date = now.strftime("%B %d, %Y")
    time = now.strftime("%I:%M %p")

    return render(
        request, "main/dashboard.html", {"day": day, "date": date, "time": time}
    )


@login_required
def hangman(request):
    return render(request, "main/hangman.html")


@login_required
def snake(request):
    return render(request, "main/snake.html")


@login_required
def tictactoe(request):
    return render(request, "main/tictactoe.html")


@login_required
def virtualBuddy(request):
    return render(request, "main/virtualBuddy.html")


def mindmosaic(request):
    return render(request, "main/mindmosaic.html")


@login_required
def random_game(request):
    games = [
        "main/hangman.html",
        "main/snake.html",
        "main/tictactoe.html",
        "main/mindmosaic.html",
    ]
    return render(request, random.choice(games))


def track_game_click(request):
    if request.method == "POST":
        data = json.loads(request.body)
        game_name = data.get("game_name")

        increment_times_played(game_name)

        return JsonResponse({"status": "ok"})


def play_history(request):
    ranked_games = Game.objects.order_by("-times_played")

    return render(
        request,
        "main/play_history.html",
        {
            "ranked_games": ranked_games,
        },
    )


@login_required
def settings(request):
    player = request.user.player

    if request.method == "POST":
        data = json.loads(request.body)
        do_not_disturb = data.get("do_not_disturb", False)

        player.email_notifications = not do_not_disturb
        player.save()

        return JsonResponse({"status": "ok"})

    return render(request, "main/settings.html", {"player": player})
