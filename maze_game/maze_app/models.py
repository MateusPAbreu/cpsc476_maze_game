from django.db import models
from enum import Enum
import numpy as np
import cv2
import sys
import random
# Create your models here.

class Player(models.Model):
    player1_name = models.CharField(max_length=255)
    player2_name = models.CharField(max_length=255)
    player1_answer_right = models.IntegerField(default=0)
    player1_answer_wrong = models.IntegerField(default=0)
    player2_answer_right = models.IntegerField(default=0)
    player2_answer_wrong = models.IntegerField(default=0)


# class GameLog(models.Model):
#     time = models.DateTimeField()
#     p1_name = Player.player1_name
#     p1_right = Player.answer_right
#     p1_wrong = Player.answer_wrong
#     p2_name = Player.player2_name
#     p2_right = Player.answer_right
#     p2_wrong = Player.answer_wrong
