from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('play/', views.play, name='play'),
    path('options/', views.options, name='options'),
    path('maze/', views.maze, name='maze'),
    path('ai/', views.ai_view, name='ai'),
    path('select/', views.select_level, name='select'),
    path('tutorial/', views.tutorial, name='tutorial'),

    # API endpoint for live game updates
    path('api/game/<int:session_id>/update/', views.update_game_session,
         name='update_game_session'),
]
