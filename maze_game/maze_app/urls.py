from django.urls import path
from . import views

urlpatterns = [
       path('', views.menu, name='menu'),
    path('play/', views.play, name='play'),
    path('options/', views.options, name='options'),
    path('first_maze/', views.first_maze, name='first_maze')
]
