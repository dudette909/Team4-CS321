from django.contrib import admin
from .models import InventoryItem, Backpack
# Register your models here.

admin.site.register(InventoryItem)
admin.site.register(Backpack)