from django.db import models
from enum import Enum
import numpy as np
import cv2
import sys
import random
# Create your models here.

class Player1(models.Model):
    # name = models.CharField(max_length=255)
    right_answer = models.DecimalField(max_digits=10, decimal_places=2)
    wrong_answer = models.DecimalField(max_digits=10, decimal_places=2)

class Player2(models.Model):
    # name = models.CharField(max_length=255)
    right_answer = models.DecimalField(max_digits=10, decimal_places=2)
    wrong_answer = models.DecimalField(max_digits=10, decimal_places=2)
