from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class InventoryItem(models.Model):
    itemName = models.CharField(max_length = 100)
    description = models.TextField(blank = True)

    def __str__(self):
        return self.itemName

class Backpack(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    items = models.ManyToManyField(InventoryItem, blank = True)

    def __str__(self):
        return f"{self.user.username}'s Backpack"