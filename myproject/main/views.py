from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from .utils import *
from .models import InventoryItem, Backpack, GameResult, Player, Game # So it's looking at OUR models.py file, and then imports the CLASS "Backpack" that we defined in there.
import random
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
    backpack, created = Backpack.objects.get_or_create(user=request.user)
    backpack = Backpack.objects.get(user=request.user)
    #results = GameResult.objects.filter(user=request.user)
    #resultsList = list(results)
    return render(request, "main/virtualBuddy.html", {"backpack": backpack})

@login_required
def mines(request):
    result = GameResult.objects.filter(user=request.user, gameName="mines").first()
    if result == None:
        return render(request, "main/mines.html", {"lastPlayedDate": "", "dateToday": timezone.localdate()})

    lastTimePlayed = timezone.localtime(result.lastPlayedTime)
    context = {"lastPlayedDate": lastTimePlayed.date(), "dateToday": timezone.localdate()}
    return render(request, "main/mines.html", context)

@login_required
def saveMinesResults(request): # this should be the request from the js file, so the body if it was properly JSON.stringified should be smth like {"victory": true}
    print("Received1: ", request.body)
    if request.method == "POST":
        data = json.loads(request.body) # so data should now be the string dictionary {"victory" : boolean_here}
        victory = data.get("victory") # gets the value of key "victory" in dictionary "data"
        print("Received2: ", victory) # idk how to use print statements to debug in django it doesn't show up in the terminal ):
        GameResult.objects.update_or_create(user=request.user, gameName="mines", defaults={"lastPlayedTime": timezone.now(), "hasPlayed": True, "victory": victory} ) # It would update any old attempts b/c theyre from days before, or if they haven't attempted this puzzle at all ever, it SHOULD create a new row in database.
        return JsonResponse({"status": "ok"}) # a basic success response to django from js. NOT the SUCCESS of the player, rather a success that the info was saved.
    
@login_required
def checkRewards(request):
    print("kys")
    results = list(GameResult.objects.filter(user=request.user))
    for result in results:
        if result.victory == True:
            if result.redeemed == False:
                # add a new random InventoryItem to user's specific unique backpack here
                print("hi")
                backpack, _ = Backpack.objects.get_or_create(user=request.user)
                unownedItems = InventoryItem.objects.exclude(id__in=backpack.values_list('id', flat=True))

                if unownedItems.exists():
                    newItem = random.choice(list(unownedItems))
                    backpack.items.add(newItem)
                else:
                    print("User already owns all items")



@login_required
def mindmosaic(request):
    if request.method == "POST":
        data = json.loads(request.body)
        score = data.get("score", 0)
        save_user_score(request.user, "MindMosaic", score)
        return JsonResponse({"status": "ok"})
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
    
    games = ['Hangman', 'Snake', 'TicTacToe', 'MindMosaic']
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
