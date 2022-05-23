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

        self.odom_robot_x  = 100
        self.odom_robot_y  = 100
        self.odom_robot_theta  = 0

        #self.grid = []
        #self.grid = np.zeros((w,h))
        self.rectangles = []
        self.angle_distance = []
        self.particles = []

        
        for i in range (1, NUMBER_OF_OBJECTS):
            x = random.randint(100,w-100)
            y = random.randint(100,h-100)
            ww = min(random.randint(10,100), w-100-x)
            hh = min(random.randint(10,100), h-100-y)
            self.rectangles.append((x,y,ww,hh))
            
        #self.rectangles.append((150,170,100,120))
        #self.rectangles.append((1000,1200,10,10))
        self.rectangles.append((0,0,50,50))
        self.rectangles.append((w-50,h-50,50,60))

        self.display_world(True)

    #theta is degrees
    #TODO: we need to simulate control not exact location
    #Thus we should have to get command such as right motor, left motor voltage which
    #would be translated to change is robot's pose 
    def move_robot_by(self, dx, dy, d_theta):
        self.robot_x  += dx
        self.robot_y  += dy
        self.robot_theta  += d_theta
 
        #TODO: Add error to odometry changes
        #If we get an error that keeps on growing and do not identify, quantify and compensate for it the inaccuracy gets worse
        self.odom_robot_x  += dx + (random.random() * 10 ) * random.randint(-1,1)
        self.odom_robot_y  += dy + (random.random() * 10 ) * random.randint(-1,1)
        self.odom_robot_theta  += d_theta

    def get_robot(self):
        return self.robot_x, self.robot_y, self.robot_theta
    
    def on_press(self, event):
        #print('press', event.key)
        sys.stdout.flush()
        #self.display_world(False)
        self.cb(event.key, self)
     
    def add_particles(self, particles):
        self.particles = particles
        #print(self.particles)       

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
            self.draw_circle(robot_x, robot_y, 20, 'y')
            self.draw_sensor_reads()
            self.draw_objects()
            self.draw_particles()
            #self.ax.imshow(image.transpose())

            plt.gca().invert_yaxis()
            plt.show()
        else:
            robot_x = self.robot_x
            robot_y = self.robot_y
            #image[robot_x:robot_x+30, robot_y:robot_y+30] = 150
            self.ax.clear()
            #self.ax.imshow(np.flip(image.transpose(), 0))
            self.draw_circle(robot_x, robot_y, 20, 'y')
            self.draw_objects()
            self.draw_sensor_reads()
            self.draw_particles()
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
    
    def draw_circle(self, x, y, r,c):
        circle = plt.Circle((x,y),r, color=c)
        self.ax.add_patch(circle)

    def draw_particles(self):
        for p in self.particles:
            print('particle', p)
            self.draw_circle(p[0], p[1], 2, 'b')

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
        self.angle_distance = find_closest_intersecting_line([self.robot_x, self.robot_y], self.robot_theta, np.array(lines))
        
        print('##################\n',self.robot_x, self.robot_y)
        for x in self.angle_distance:
            #max range is 300
            if not math.isnan(x[1]) and x[1] < 200:
                #print( '{:0.2f} degrees => {:0.2f}'.format(x[0], x[1]) )
                deg_rad = (x[0]/360)*2*math.pi
                #print (deg_rad)
                self.draw_line_from_point(self.robot_x, self.robot_y, deg_rad, x[1])
                pass

        #print(lines)
        
    def get_odom(self):
        return self.odom_robot_x, self.odom_robot_y, self.odom_robot_theta
        
    def get_angle_distances(self):
        return self.angle_distance

