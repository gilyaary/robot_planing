import numpy as np
import pygame
import random
import math
from world_map2 import * 

#pygame.init()
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
w = 1700
h = 900
#gameDisplay = pygame.display.set_mode((w,h))
#gameDisplay.fill(black)

# initialize a WorldMap object with objects and the current position of the robot
# The worldMap will hold the real location of objects and the current position of the robot.
# It will give measurements with errors and odometry with errors.
# 
# Pressing the arrows will move the robot in the environment left, right. up and down.
# In such a way we simulate the robot being controlled. However the distance and position moved will be with errors.
# We can at any point get measurement of the sensors.
# 
# Speed is not considered. We simply command the robot to go to a direction and it goes there with errors.
# 
# With every step the Map is updated with the true location of the robot. 
# 
# Needs:
# Algo 1: Input: robot [x,y,theta] Output: distance  to closest object (Simulates sonar or LIDAR)
# Also 2: Input: control signal to motors [x,y] Output Odometry [dx,dy,dTheta] 
def cb(key):
    print('callback called with Key: ' + key)
    x,y,theta = wm.get_robot()
    if key == 'left':
        wm.set_robot_at(x - 20 , y, theta)
    if key == 'right':
        wm.set_robot_at(x + 20, y, theta)
    if key == 'up':
        wm.set_robot_at(x, y - 20, theta)
    if key == 'down':
        wm.set_robot_at(x, y + 20, theta)
    wm.display_world(False)
    # TODO: 



wm = WorldMap(w,h,cb)

for i in range (1, 20):
    x = random.randint(100,w-100)
    y = random.randint(100,h-100)
    ww = min(random.randint(10,100), w-100-x)
    hh = min(random.randint(10,100), h-100-y)
    #add_block(x,y,ww,hh,board)  
    wm.set_rectangle__at(x, y, ww, hh)

wm.display_world(True)

