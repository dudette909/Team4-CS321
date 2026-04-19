from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone


from django.contrib.auth.models import User
from .models import Backpack, GameResult # So it's looking at OUR models.py file, and then imports the CLASS "Backpack" that we defined in there.
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
def pacman(request):
    return render(request, "main/pacman.html")


@login_required
def snake(request):
    return render(request, "main/snake.html")


@login_required
def tictactoe(request):
    return render(request, "main/tictactoe.html")


@login_required
def tiles(request):
    return render(request, "main/tiles.html")

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
    # if result and result.lastPlayedTime:
    #     todaysDate = timezone.now()
    lastTimePlayed = timezone.localtime(result.lastPlayedTime)
    #     print(lastTimePlayed.date())
    #     print(result.lastPlayedTime.date())
    #     if lastTimePlayed.date() == todaysDate.date():
    #         return render(request, "main/blockedGame.html")
    context = {"lastPlayedDate": lastTimePlayed.date(), "dateToday": timezone.localdate()}
    return render(request, "main/mines.html", context)

@login_required
def saveMinesResults(request): # this should be the request from the js file, so the body if it was properly JSON.stringified should be smth like {"victory": true}
    print("Received1: ", request.body)
    if request.method == "POST":
        data = json.loads(request.body) # so data should now be the string dictionary {"victory" : boolean_here}
        victory = data.get("victory") # gets the value of key "victory" in dictionary "data"
        print("Received2: ", victory) # idk how to use print statements to debug in django it doesn't show up in the terminal ):
        GameResult.objects.update_or_create(user=request.user, gameName="mines", defaults={"lastPlayedTime": timezone.now(), "hasPlayed": True, "victory": victory} )
        # It would update any old attempts b/c theyre from days before, or if they haven't attempted this puzzle at all ever, it SHOULD create a new row in database.

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
        