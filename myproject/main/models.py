from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class InventoryItem(models.Model):
    itemName = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    itemImage = models.ImageField(upload_to="items/")

    def __str__(self):
        return self.itemName


class Backpack(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(InventoryItem, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Backpack"
    
class GameResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gameName = models.CharField(max_length=64) # like which game, for now there's only 1, but this should be for handling more games in the future.
    lastPlayedTime = models.DateTimeField(null=True, blank=True)
    hasPlayed = models.BooleanField(null=True, blank=True)
    victory = models.BooleanField(null=True, blank=True)
    redeemed = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} {self.gameName} RESULTS"

    class Meta:
        unique_together=('user', 'gameName') # should prevent duplicate rows(?)

# Seems to only be used for the email thing and used for game history tab.
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    most_played_game = models.ForeignKey(
        "Game", on_delete=models.SET_NULL, null=True, blank=True
    )
    streak = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.email_notifications} - {self.user.email}"


class Game(models.Model):
    name = models.CharField(max_length=100)
    high_score = models.IntegerField(default=0)
    times_played = models.IntegerField(default=0)

    def __str__(self):
        return (
            f"{self.name} - High Score: {self.high_score} - Played: {self.times_played}"
        )

# Get rid of this class, we don't need it anymore. If anything just add a new field to GameResult class for "score". This appears to be unnecessarily complicated.
class GameScore(models.Model):
    """Track individual user scores for each game"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_scores')
    game_name = models.CharField(max_length=100)
    score = models.IntegerField()
    date_played = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-score', '-date_played']
        verbose_name = 'Game Score'
        verbose_name_plural = 'Game Scores'
    
    def __str__(self):
        return f"{self.user.username} - {self.game_name}: {self.score}"
    
    @classmethod
    def get_top_scores(cls, game_name, limit=10):
        """Get top scores for a specific game"""
        return cls.objects.filter(game_name=game_name).select_related('user')[:limit]
    
    @classmethod
    def get_user_best(cls, user, game_name):
        """Get user's best score for a specific game"""
        score = cls.objects.filter(user=user, game_name=game_name).first()
        return score.score if score else 0
    
    @classmethod
    def get_user_rank(cls, user, game_name):
        """Get user's rank for a specific game"""
        user_best = cls.get_user_best(user, game_name)
        if user_best == 0:
            return None
        # Count how many unique users have a better score
        better_scores = cls.objects.filter(
            game_name=game_name, 
            score__gt=user_best
        ).values('user').distinct().count()
        return better_scores + 1
