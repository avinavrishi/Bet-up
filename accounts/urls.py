from django.urls import path
from django.conf.urls import url 
from .views import Home, gameView, finalResults
from accounts import views

urlpatterns = [
    # path("", Home.as_view(), name="home"),
    url("", views.gameView, name = "gameView"),
    url("final", views.finalResults, name = "result")
]
