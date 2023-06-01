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
#w, h = 400, 400
#board = np.zeros((w,h))
#choice = random.randint(0,2)
#x = random.randint(10,w-12)
#add_block(x,y,ww,hh,board)  
#pygame.draw.line(gameDisplay, blue, (last_x,last_y), (x,y),5)

#first draw an image
#now apply gray scale
#now apply canney
#apply edges
#link edges
#find paths

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()    