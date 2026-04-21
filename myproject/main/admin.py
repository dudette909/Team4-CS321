from django.contrib import admin
from .models import Player, Game, InventoryItem, Backpack, GameScore, GameResult

# Register your models here.
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'streak', 'most_played_game']
    list_filter = ['email_notifications']
    search_fields = ['user__username', 'user__email']

@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'game_name', 'score', 'date_played']
    list_filter = ['game_name', 'date_played']
    search_fields = ['user__username', 'game_name']
    ordering = ['-score', '-date_played']
    date_hierarchy = 'date_played'

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['itemName', 'description']
    search_fields = ['itemName']

@admin.register(Backpack)
class BackpackAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_items_count']
    search_fields = ['user__username']
    
    def get_items_count(self, obj):
        return obj.items.count()
    get_items_count.short_description = 'Items Count'

admin.site.register(GameResult) # maybe change to be customized with @admin.register