from django.shortcuts import render
from django.http import HttpResponse
import random
from enum import Enum
import numpy as np
import cv2
import sys
# from models import Backtracking

def home(request):
    # maze = Backtracking(10, 10, )
    # maze = Backtracking(10, 10, "C:\Users\mateu\OneDrive\Documentos\Projects\Django\maze_game", True)
    # maze.create_maze()

    return HttpResponse("Maze!")

def menu(request):
    return render(request, "index.html")
