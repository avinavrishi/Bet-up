from django.urls import path
from django.conf.urls import url 
from .views import Home, gameView, finalResults, RechargePage,SaveUtr, save_withdrawal_request, ProfileInfo
from accounts import views

urlpatterns = [
    path("home", views.Home, name="home"),
    path("profile", views.ProfileInfo, name="profilePage"),
    path("recharge", views.RechargePage, name="rechargePage"),
    url("gameView", views.gameView, name = "gameView"),
    url("final", views.finalResults, name = "result"),
    url("submitUtr", views.SaveUtr, name = "SubmitUtrPage"),
    path('withdrawal/', views.save_withdrawal_request, name='save_withdrawal_request'),
]