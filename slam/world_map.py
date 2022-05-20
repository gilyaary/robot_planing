import numpy as np
import random
import math
import matplotlib.pyplot as plt
#import sys
#np.set_printoptions(threshold=sys.maxsize)
"""
Created on Tue May  18 08:00:00 2022

@author: Gil Yaary
"""

class WorldMap:
    def __init__(self, w, h):
        #print("init")
        self.w = w
        self.h = h
        self.robot_x  = 40
        self.robot_y  = 40
        self.robot_theta  = 30
        self.rectangles = []
        self.grid = []
        self.grid = np.zeros((w,h))
    #theta is degrees
    def setRobotAt(self, x, y, theta):
        self.robot = (x,y,theta)
    
    def set_rectangle__at(self, x, y, w, h):
        self.rectangles.append((x,y,w,h))
        self.grid[x:x+w,y:y+h] = 120

    def display_world(self):
        #print(self.grid)
        image = self.grid.copy()
        robot_x = self.robot_x
        robot_y = self.robot_y
        #image[robot_x:robot_x+30, robot_y:robot_y+30] = 150
        self.draw_circle(robot_x, robot_y, 20, image)
        fig = plt.figure(figsize=(20, 15))
        # importing packages
        # set the spacing between subplots
        plt.subplots_adjust(
            left=0.05,
            bottom=0.05,
            right=0.95,
            top=0.95, 
            wspace=0.1, 
            hspace=0.1)

        fig.set_figheight(15)
        fig.set_figwidth(20)
        
        imgplot = plt.imshow(image.transpose())
        
        plt.show()
        
    
    def draw_circle(self, x, y, r, image):
        for step in range (0, r*50) :
            ddx = step / 50.0
            dy = int (math.sqrt(r*r - ddx*ddx))
            dx = int (ddx)
            x1, x2, y1, y2 = x-dx, x+dx, y-dy, y+dy
            image[x1:x2, y1] = 150
            image[x1:x2, y1] = 150
            image[x1:x2, y2] = 150
            image[x1:x2, y2] = 150
            

    def draw_circle2(self, x, y, r, image):
        for dx in range (0, r) :
            dy = int (math.sqrt(r*r - dx*dx))
            print(dy)
            x1, x2, y1, y2 = x-dx, x+dx, y-dy, y+dy
            '''
            ww = 4
            image[x1-ww:x1+ww, y1-ww:y1+ww] = 150
            image[x1-ww:x1+ww, y2-ww:y2+ww] = 150
            image[x2-ww:x2+ww,y1-ww:y1+ww] = 150
            image[x2-ww:x2+ww, y2-ww:y2+ww] = 150
            '''
            image[x1:x2, y1-6:y1+6] = 150
            image[x1:x2, y1-6:y1+6] = 150
            image[x1:x2, y2-6:y2+6] = 150
            image[x1:x2, y2-6:y2+6] = 150

