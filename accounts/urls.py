from django.urls import path
from django.conf.urls import url 
from .views import Home, gameView, finalResults, RechargePage
from accounts import views

urlpatterns = [
    path("", views.Home, name="home"),
    path("recharge", views.RechargePage, name="rechargePage"),
    url("gameView", views.gameView, name = "gameView"),
    url("final", views.finalResults, name = "result"),
]