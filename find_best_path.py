#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 08:36:26 2021

@author: gil
"""

import pygame

pygame.init()

white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

gameDisplay = pygame.display.set_mode((800,600))


#gameDisplay.fill(black)
#pygame.draw.line(gameDisplay, blue, (100,200), (300,450),5)
#pygame.draw.rect(gameDisplay, red, (400,400,50,25))
#pygame.draw.circle(gameDisplay, white, (150,150), 75)
#pygame.draw.polygon(gameDisplay, green, ((25,75),(76,125),(250,375),(400,25),(60,540)))

gameDisplay.fill(white)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()    