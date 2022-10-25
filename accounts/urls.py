from django.urls import path
from django.conf.urls import url 
from .views import Home, Result_list
from accounts import views

urlpatterns = [
    path("", Home.as_view(), name="home"),
    url(r'^api/result$', views.Result_list),
]