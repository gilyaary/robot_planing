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
        self.rectangles = []
        self.grid = []
        self.grid = np.zeros((w,h))
        for i in range (1, 25):
            x = random.randint(100,w-100)
            y = random.randint(100,h-100)
            ww = min(random.randint(10,100), w-100-x)
            hh = min(random.randint(10,100), h-100-y)
            #add_block(x,y,ww,hh,board)  
            self.set_rectangle__at(x, y, ww, hh)
        self.display_world(True)
    
    
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
        # TODO: Now add the lines of the rectangle to collection of polygons
        # each polygon has a collection of lines and each line has 2 points

    def on_press(self, event):
        #print('press', event.key)
        sys.stdout.flush()
        #self.display_world(False)
        self.cb(event.key, self)
        

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
            
            #self.ax.imshow(np.flip(image.transpose(), 0))
            self.draw_sensor_reads()
            self.ax.imshow(image.transpose())

            plt.gca().invert_yaxis()
            plt.show()
        else:
            robot_x = self.robot_x
            robot_y = self.robot_y
            #image[robot_x:robot_x+30, robot_y:robot_y+30] = 150
            self.draw_circle(robot_x, robot_y, 20, image)
            self.ax.clear()
            #self.ax.imshow(np.flip(image.transpose(), 0))
            self.draw_sensor_reads()
            self.ax.imshow(image.transpose())
            
            plt.gca().invert_yaxis()
            self.fig.canvas.draw()
            
    
    def draw_circle(self, x, y, r, image):
        for step in range (0, r*50) :
            ddx = step / 50.0
            dy = int (math.sqrt(r*r - ddx*ddx))
            dx = int (ddx)
            x1, x2, y1, y2 = x-dx, x+dx, y-dy, y+dy
            image[x1:x2, y1] = 130
            image[x1:x2, y1] = 130
            image[x1:x2, y2] = 130
            image[x1:x2, y2] = 130
            

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
            image[x1:x2, y1-6:y1+6] = 130
            image[x1:x2, y1-6:y1+6] = 130
            image[x1:x2, y2-6:y2+6] = 130
            image[x1:x2, y2-6:y2+6] = 130

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
            if not math.isnan(x[1]) and x[1] < 300:
                print( '{:0.2f} degrees => {:0.2f}'.format(x[0], x[1]) )
                deg_rad = (x[0]/360)*2*math.pi
                print (deg_rad)
                self.draw_line_from_point(self.robot_x, self.robot_y, deg_rad, x[1])
                pass

        #print(lines)
        
    