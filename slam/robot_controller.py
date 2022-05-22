import numpy as np
import pygame
import random
import math
from world_map2 import * 

#pygame.init()
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
#
# TODO: we set the x, y and theta here as if we were moving the robot and reading the odometry
# We should get the odomtry for the world_map and give it commands to move right, left, up and down
# We then get back odometry with the estimated location (the map knows the real location and pose)
# We use the odometry to recalculate the prior for location hypothesis
 
    

def cb(key, wm):
    #print('callback called with Key: ' + key) 
    x,y,theta = wm.get_robot()
    if key == 'left':
        wm.set_robot_at(x - 20 , y, theta)
        #wm.move_left(10)
    if key == 'right':
        wm.set_robot_at(x + 20, y, theta)
        #wm.move_right(10)
    if key == 'up':
        wm.set_robot_at(x, y - 20, theta)
        #wm.move_up(10)
    if key == 'down':
        wm.set_robot_at(x, y + 20, theta)
        #wm.move_down(10)
    wm.display_world(False)

wm = WorldMap(w,h, cb)

    #wm.get_pose_from_odometry()
    #wm.get_sensor_readings() #comes as distance from robot. For map we need to translate to world map coordinates
    #Now update the location hypothesis and SAVE the sensor data. 

     

