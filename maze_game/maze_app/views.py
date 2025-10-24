from django.shortcuts import render
from django.http import HttpResponse
import random
from enum import Enum
import numpy as np
import cv2
import sys


def home(request):
   

    return HttpResponse("Maze!")

def home(request):
    return HttpResponse("Maze!")

def menu(request):
    return render(request, "menu.html")

def play(request):
    return render(request, "play.html")

def options(request):
    return render(request, "options.html")


class Backtracking:
    def __init__(self, height, width, path, display_maze):
       
        if width % 2 ==0:
            width += 1
        if height % 2 ==0:
            height += 1
        
        self.width = width
        self.height = height
        self.path = path
        self.display_maze = display_maze
        
    def create_maze(self):
        maze = np.ones((self.height, self.width), dtype=np.float) #Creates a 2D array
        
        for i in range(self.height): #this loop turns all the odd rows and columns to 0, to denote walls
            for j in range(self.width):
                if i%2 == 1 or j%2 == 1:
                    maze [i, j] = 0
                if i == 0 or j ==0 or i == self.height or j == self.width -1:
                    maze[i, j] = 0.5 #this determines the visited cells
                    
        sx = random.choice(range(2, self.width -2, 2))
        sy = random.choice(range(2, self.height -2, 2))
        self.generator(sx, sy, maze)
    
        for i in range(self.height):       
            for j in range(self.width):
                if maze[i, j] == 0.5:
                    maze[i, j] = 1
                    
        maze[1, 2] = 1 #top left
        maze[self.height - 2, self.width - 3] = 1 #bottom right
        
        if self.display_maze:
            # cv2.namedWindow('Math Maze', cv2.WINDOW_NORMAL)
            cv2.imshow('Maze', maze)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        maze = maze * 255.0
        cv2.imwrite(self.path, maze)
        
                    
    def generator(self, cx, cy, grid):
        grid[cy, cx] = 0.5
        
        if (grid[cy-2, cx] == 0.5 and grid[cy+2] == 0.5 and grid[cy, cx-2] == 0.5 and grid[cy, cx+2] == 0.5):
            pass
        else:
            li = [1, 2, 3, 4]
            while len(li) > 0:
                dir = random.choice(li)
                li.remove(dir)
                
                if dir == Directions.UP.value:
                    nx = cx
                    mx = cx
                    ny = cy - 2
                    my = cy - 1
                elif dir == Directions.DOWN.value:
                    nx = cx
                    mx = cx
                    ny = cy + 2
                    my = cy + 1
                elif dir == Directions.DOWN.value:
                    nx = cx - 2
                    mx = cx - 1
                    ny = cy 
                    my = cy 
                elif dir == Directions.RIGHT.value:
                    nx = cx + 2
                    mx = cx + 1
                    ny = cy 
                    my = cy 
                else:
                    nx = cx
                    mx = cx
                    ny = cy
                    my = cy
                
                if grid[ny, nx] != 0.5: #randomly chooses an element and gets directions
                    grid[my, mx] = 0.5
                    self.generator(nx, ny, grid)
            
class Directions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
