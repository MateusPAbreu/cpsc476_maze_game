from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('right_answer/', views.update_right_answer_player1, name='update_player1'),
    path('wrong_answer/', views.update_wrong_answer_player1, name='update_player1'),
    path('right_answer/', views.update_right_answer_player2, name='update_player2'),
    path('wrong_answer/', views.update_wrong_answer_player2, name='update_player2'),
    path('play/', views.play, name='play'),
    path('options/', views.options, name='options'),
<<<<<<< Updated upstream
    path('first_maze/', views.first_maze, name='first_maze')
=======
    path('maze/', views.maze, name='maze'),
    path("ai/", views.ai_view, name="ai"),
    path('select/', views.select, name="select")

>>>>>>> Stashed changes
]
