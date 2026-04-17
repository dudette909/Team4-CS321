from .models import *
import random
from django.core.mail import send_mail
from django.conf import settings


def create_games():
    game_list = ["Snake", "Hangman", "TicTacToe", "MindMosaic"]

    for name in game_list:
        Game.objects.get_or_create(name=name)

    print("Games initialized")


def increment_times_played(game_name):
    game, created = Game.objects.get_or_create(name=game_name)
    game.times_played += 1
    game.save()


def send_email_notification(user):
    if not user.email:
        return "no_email"

    if not hasattr(user, "player"):
        return "no_player"

    if not user.player.email_notifications:
        return "dnd"

    subject = "GameHub"

    messages = [
        "Beat your last score on GameHub.",
        "Bored? Jump into a quick game on GameHub.",
        "Take a quick break and play on GameHub.",
        "Jump back in and set a new high score on GameHub.",
    ]

    message = random.choice(messages)

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

    return "sent"
