from django.contrib import admin
from .models import InventoryItem, Backpack, GameResult
# Register your models here.

admin.site.register(InventoryItem)
admin.site.register(Backpack)
admin.site.register(GameResult)