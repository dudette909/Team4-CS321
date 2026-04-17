from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class InventoryItem(models.Model):
    itemName = models.CharField(max_length = 100)
    description = models.TextField(blank = True)
    itemImage = models.ImageField(upload_to= "items/")


    def __str__(self):
        return self.itemName

class Backpack(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    items = models.ManyToManyField(InventoryItem, blank = True)

    def __str__(self):
        return f"{self.user.username}'s Backpack"

class GameResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gameName = models.CharField(max_length=64) # like which game, for now there's only 1, but this should be for handling more games in the future.
    lastPlayedTime = models.DateTimeField(null=True, blank=True)
    hasPlayed = models.BooleanField(null=True, blank=True)
    victory = models.BooleanField(null=True, blank=True)

    class Meta:
        unique_together=('user', 'gameName') # should prevent duplicate rows