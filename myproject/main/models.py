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
