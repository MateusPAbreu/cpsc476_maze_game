from django.urls import path
from . import views

urlpatterns = [
       path('', views.menu, name='menu'),
    path('play/', views.play, name='play'),
    path('options/', views.options, name='options'),
    path('maze/', views.maze, name='maze'),
    path("ai/", views.ai_view, name="ai"),

]
