import numpy as np
import random
import math
import matplotlib.pyplot as plt
import sys
#np.set_printoptions(threshold=sys.maxsize)
"""
Created on Tue May  18 08:00:00 2022

@author: Gil Yaary
"""

class WorldMap:
    def __init__(self, w, h, cb):
        #print("init")
        self.w = w
        self.h = h
        self.robot_x  = 40
        self.robot_y  = 40
        self.robot_theta  = 30
        self.rectangles = []
        self.grid = []
        self.grid = np.zeros((w,h))
        self.image_initialized = False
        self.cb = cb
    #theta is degrees
    def set_robot_at(self, x, y, theta):
        self.robot_x  = x
        self.robot_y  = y
        self.robot_theta  = theta

    def get_robot(self):
        return self.robot_x, self.robot_y, self.robot_theta
    
    def set_rectangle__at(self, x, y, w, h):
        self.rectangles.append((x,y,w,h))
        self.grid[x:x+w,y:y+h] = 120

    def on_press(self, event):
        print('press', event.key)
        sys.stdout.flush()
        #self.display_world(False)
        self.cb(event.key)
        

    def display_world(self, Redraw = False):
        #print(self.grid)
        image = self.grid.copy()
        
        if Redraw == True:
            robot_x = self.robot_x
            robot_y = self.robot_y
            #image[robot_x:robot_x+30, robot_y:robot_y+30] = 150
            self.draw_circle(robot_x, robot_y, 20, image)
        
            self.fig, self.ax = plt.subplots()
            self.fig.canvas.mpl_connect('key_press_event', self.on_press)
            self.xl = self.ax.set_xlabel('easy come, easy go')
            self.ax.set_title('Press a key')
            #ax.plot(np.random.rand(12), np.random.rand(12), 'go')
            self.fig.set_figheight(15)
            self.fig.set_figwidth(20)
            self.ax.imshow(image.transpose())

            plt.show()
        else:
            robot_x = self.robot_x
            robot_y = self.robot_y
            #image[robot_x:robot_x+30, robot_y:robot_y+30] = 150
            self.draw_circle(robot_x, robot_y, 20, image)
            self.ax.clear()
            self.ax.imshow(image.transpose())
            self.fig.canvas.draw()
            
    
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

