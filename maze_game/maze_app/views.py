from django.shortcuts import render
from django.http import HttpResponse
import random
from enum import Enum
import numpy as np
import cv2
import sys

def home(request):
    # maze = Backtracking(10, 10, )
    return HttpResponse("Maze!")