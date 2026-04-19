from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import random
from django.contrib.auth.models import User
from .models import Player
from .utils import *
from .models import Game
import json
from django.http import JsonResponse
from datetime import datetime, timedelta


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
    # Update streak on dashboard visit
    update_user_streak(request.user)
    
    now = timezone.localtime()

    day = now.strftime("%A")
    date = now.strftime("%B %d, %Y")
    time = now.strftime("%I:%M %p")

    return render(
        request, "main/dashboard.html", {"day": day, "date": date, "time": time}
    )


@login_required
def hangman(request):
    if request.method == "POST":
        data = json.loads(request.body)
        score = data.get("score", 0)
        save_user_score(request.user, "Hangman", score)
        return JsonResponse({"status": "ok"})
    return render(request, "main/hangman.html")


@login_required
def snake(request):
    if request.method == "POST":
        data = json.loads(request.body)
        score = data.get("score", 0)
        save_user_score(request.user, "Snake", score)
        return JsonResponse({"status": "ok"})
    return render(request, "main/snake.html")


@login_required
def tictactoe(request):
    if request.method == "POST":
        data = json.loads(request.body)
        score = data.get("score", 0)
        save_user_score(request.user, "TicTacToe", score)
        return JsonResponse({"status": "ok"})
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


@login_required
def logoutPage(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect("landingPage")


@login_required
def leaderboard(request):
    """Display leaderboard for all games"""
    from .models import GameScore
    
    games = ['Hangman', 'Snake', 'TicTacToe']
    leaderboard_data = {}
    user_stats = {}
    
    for game in games:
        # Get top 10 scores for each game
        top_scores = GameScore.get_top_scores(game, limit=10)
        leaderboard_data[game] = top_scores
        
        # Get user's stats for each game
        user_best = GameScore.get_user_best(request.user, game)
        user_rank = GameScore.get_user_rank(request.user, game)
        user_stats[game] = {
            'best_score': user_best,
            'rank': user_rank
        }
    
    return render(request, 'main/leaderboard.html', {
        'leaderboard_data': leaderboard_data,
        'user_stats': user_stats,
        'games': games
    })


@login_required
def game_leaderboard(request, game_name):
    """Display leaderboard for a specific game"""
    from .models import GameScore
    
    # Capitalize first letter of each word for display
    game_display_name = game_name.replace('_', ' ').title()
    
    # Get top 50 scores for the game
    top_scores = GameScore.get_top_scores(game_name, limit=50)
    
    # Get user's stats
    user_best = GameScore.get_user_best(request.user, game_name)
    user_rank = GameScore.get_user_rank(request.user, game_name)
    
    # Get user's recent scores (last 10)
    user_scores = GameScore.objects.filter(
        user=request.user, 
        game_name=game_name
    )[:10]
    
    return render(request, 'main/game_leaderboard.html', {
        'game_name': game_name,
        'game_display_name': game_display_name,
        'top_scores': top_scores,
        'user_best': user_best,
        'user_rank': user_rank,
        'user_scores': user_scores
    })
