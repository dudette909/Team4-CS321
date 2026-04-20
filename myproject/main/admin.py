from django.contrib import admin
from .models import InventoryItem, Backpack, GameResult, Player, Game, GameScore
# Register your models here.

admin.site.register(InventoryItem)
admin.site.register(Backpack)
admin.site.register(GameResult)

# Register your models here.
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'streak', 'most_played_game']
    list_filter = ['email_notifications']
    search_fields = ['user__username', 'user__email']

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'high_score', 'times_played']
    list_filter = ['name']
    ordering = ['-times_played']

@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'game_name', 'score', 'date_played']
    list_filter = ['game_name', 'date_played']
    search_fields = ['user__username', 'game_name']
    ordering = ['-score', '-date_played']
    date_hierarchy = 'date_played'

