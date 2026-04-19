from .models import *
import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


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


def update_high_score(game_name, score):
    """Update high score for a game if the new score is higher"""
    game, created = Game.objects.get_or_create(name=game_name)
    if score > game.high_score:
        game.high_score = score
        game.save()
        return True
    return False


def save_user_score(user, game_name, score):
    """Save a user's score for a specific game"""
    from .models import GameScore
    
    # Create the score record
    game_score = GameScore.objects.create(
        user=user,
        game_name=game_name,
        score=score
    )
    
    # Also update global high score if needed
    update_high_score(game_name, score)
    
    return game_score


def update_user_streak(user):
    """Update user's login streak"""
    if not hasattr(user, 'player'):
        return
    
    player = user.player
    now = timezone.localtime().date()
    
    # Get last login date from session or database
    # For simplicity, we'll track via a last_login_date field
    # This would need to be added to the Player model in production
    # For now, we'll increment streak each time (simplified version)
    player.streak += 1
    player.save()
    
    return player.streak
