"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.landingPage, name="landingPage"),
    path("login/", views.loginPage, name="loginPage"),
    path("register/", views.registerPage, name="registerPage"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("hangman/", views.hangman, name="hangman"),
    path("snake/", views.snake, name="snake"),
    path("tictactoe/", views.tictactoe, name="tictactoe"),
    path("virtualBuddy/", views.virtualBuddy, name="virtualBuddy"),
    path("mindmosaic/", views.mindmosaic, name="mindmosaic"),
    path("random_game/", views.random_game, name="random_game"),
    path("track-game-click/", views.track_game_click, name="track_game_click"),
    path("play-history/", views.play_history, name="play_history"),
    path("settings/", views.settings, name="settings"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
