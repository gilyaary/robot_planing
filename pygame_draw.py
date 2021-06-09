from path_planner import *
import numpy as np
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 08:36:26 2021

@author: gil
"""

import pygame
import random
import math

def add_block(x,y,w,h,board):
    board[x:x+w,y:y+h] = 1
    pygame.draw.rect(gameDisplay, red, (x,y,w,h))


pygame.init()

white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

gameDisplay = pygame.display.set_mode((800,600))
gameDisplay.fill(black)

# pygame.draw.line(gameDisplay, blue, (100,200), (300,450),5)
# pygame.draw.rect(gameDisplay, red, (400,400,50,25))
# pygame.draw.circle(gameDisplay, white, (150,150), 75)
# pygame.draw.polygon(gameDisplay, green, ((25,75),(76,125),(250,375),(400,25),(60,540)))

w, h = 500, 500
board = np.zeros((w,h))

for i in range (1,20):
    choice = random.randint(0,2)
    x = random.randint(10,w-12)
    y = random.randint(10,h-12)
    ww = min(random.randint(10,100), w-x-10)
    hh = min(random.randint(10,100), h-y-10)
    add_block(x,y,ww,hh,board)  



# add_block(10,10,20,30,board)
# add_block(30,20,30,10,board)
# add_block(50,40,20,10,board)
# add_block(70,50,25,45,board)
# add_block(10,50,30,45,board)


start = (5,5)
goal = (w-1,h-1)

pp = PathPlanner(board, start, goal)
#pp.set_obstacle()
node = pp.find_best_path()
last_x, last_y = node.location
while node != None:
    x,y = node.location
    pygame.draw.line(gameDisplay, blue, (last_x,last_y), (x,y),5)
    last_x, last_y = x, y
    node = node.parent



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()    