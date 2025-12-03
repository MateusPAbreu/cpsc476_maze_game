from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('right_answer/', views.right_answer, name='right_answer'),
    path('wrong_answer/', views.wrong_answer, name='wrong_Answer'),
    # path('player_name/', views.player_name, name='player_name'),
    path('play/', views.play, name='play'),
    path('options/', views.options, name='options'),
    path('maze/', views.maze, name='maze'),
    path("ai/", views.ai_view, name="ai"),
    path('select/', views.select, name="select"),
    path('tutorial/', views.tutorial, name ='tutorial'),
    path('name/', views.name, name ='name')
]
