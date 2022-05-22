import numpy as np
import random
import math
import matplotlib.pyplot as plt
import sys
from line_utils import *
#np.set_printoptions(threshold=sys.maxsize)
"""
Created on Tue May  18 08:00:00 2022

@author: Gil Yaary
"""

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
NUMBER_OF_OBJECTS = 25

class WorldMap:
    def __init__(self, w, h, cb):
        #print("init")
        self.cb = cb
        print('callback set: ', self.cb)
        self.w = w
        self.h = h
        self.robot_x  = 100
        self.robot_y  = 100
        self.robot_theta  = 0
        #self.grid = []
        #self.grid = np.zeros((w,h))
        self.rectangles = []

        
        for i in range (1, NUMBER_OF_OBJECTS):
            x = random.randint(100,w-100)
            y = random.randint(100,h-100)
            ww = min(random.randint(10,100), w-100-x)
            hh = min(random.randint(10,100), h-100-y)
            self.rectangles.append((x,y,ww,hh))
            
        #self.rectangles.append((150,170,100,120))
        #self.rectangles.append((1000,1200,10,10))

        self.display_world(True)
    
    
    #theta is degrees
    def set_robot_at(self, x, y, theta):
        self.robot_x  = x
        self.robot_y  = y
        self.robot_theta  = theta
        

    def get_robot(self):
        return self.robot_x, self.robot_y, self.robot_theta
    
    def on_press(self, event):
        #print('press', event.key)
        sys.stdout.flush()
        #self.display_world(False)
        self.cb(event.key, self)
        

    def display_world(self, Redraw = False):
        #print(self.grid)
        #image = self.grid.copy()
        
        if Redraw == True:
            robot_x = self.robot_x
            robot_y = self.robot_y
            #image[robot_x:robot_x+30, robot_y:robot_y+30] = 150
            
        
            self.fig, self.ax = plt.subplots()
            self.fig.canvas.mpl_connect('key_press_event', self.on_press)
            self.xl = self.ax.set_xlabel('easy come, easy go')
            self.ax.set_title('Press a key')
            #ax.plot(np.random.rand(12), np.random.rand(12), 'go')
            self.fig.set_figheight(15)
            self.fig.set_figwidth(20)
            
            #self.ax.imshow(np.flip(image.transpose(), 0))
            self.draw_circle(robot_x, robot_y, 20)
            self.draw_sensor_reads()
            self.draw_objects()
            #self.ax.imshow(image.transpose())

            plt.gca().invert_yaxis()
            plt.show()
        else:
            robot_x = self.robot_x
            robot_y = self.robot_y
            #image[robot_x:robot_x+30, robot_y:robot_y+30] = 150
            self.ax.clear()
            #self.ax.imshow(np.flip(image.transpose(), 0))
            self.draw_circle(robot_x, robot_y, 20)
            self.draw_objects()
            self.draw_sensor_reads()
            #self.ax.imshow(image.transpose())
            
            plt.gca().invert_yaxis()
            self.fig.canvas.draw()

    def draw_objects(self):

        self.ax.set_facecolor((1.0, 0.47, 0.42))
        
        for rect in self.rectangles:
            x = rect[0]
            y = rect[1]
            w = rect[2]
            h = rect[3]
            rectangle = plt.Rectangle((x,y),w,h, color='g')
            self.ax.add_patch(rectangle)            
    
    def draw_circle(self, x, y, r):
        circle = plt.Circle((x,y),r, color='y')
        self.ax.add_patch(circle)

    def draw_line_from_point(self, x1, y1, angle, distance):
        x2 = x1 + distance * math.cos(angle)
        y2 = y1 + distance * math.sin(angle)
        self.draw_line(x1,y1,x2,y2)

    
    def draw_line(self,x1,y1,x2,y2):
        #plt.plot(x1, y1, x2, y2)
        self.ax.plot([x1,x2],[y1,y2], color="white", linewidth=1)
        pass

    
    def draw_sensor_reads(self):
        #self.rectangles.append((x,y,w,h))
        lines = []
        for rect in self.rectangles:
            x = rect[0]
            y = rect[1]
            w = rect[2]
            h = rect[3]
            #print(x,y,w,h)
            lines.append([x,y,x+w,y])
            lines.append([x,y,x,y+h])
            lines.append([x,y+h,x+w,y+h])
            lines.append([x+w,y,x+w,y+h])

        

        #self.robot_x, self.robot_y, self.robot_theta            
        angle_distance = find_closest_intersecting_line([self.robot_x, self.robot_y], self.robot_theta, np.array(lines))
        
        print('##################\n',self.robot_x, self.robot_y)
        for x in angle_distance:
            #max range is 300
            if not math.isnan(x[1]) and x[1] < 200:
                #print( '{:0.2f} degrees => {:0.2f}'.format(x[0], x[1]) )
                deg_rad = (x[0]/360)*2*math.pi
                #print (deg_rad)
                self.draw_line_from_point(self.robot_x, self.robot_y, deg_rad, x[1])
                pass

        #print(lines)
        
    