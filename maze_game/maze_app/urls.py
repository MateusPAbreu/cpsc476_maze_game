# maze_app/urls.py

from django.urls import include, path
from . import views

urlpatterns = [
<<<<<<< Updated upstream
    path('menu/', views.menu, name='menu'),
]
=======
       path('', views.menu, name='menu'),
    path('play/', views.play, name='play'),
    path('options/', views.options, name='options'),
    path('first_maze/', views.first_maze, name='first_maze')
]
>>>>>>> Stashed changes
