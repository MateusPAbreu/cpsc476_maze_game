# maze_app/urls.py

from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.home)
]