import numpy as np
import pygame
import random
import math
from world_map3 import * 
from gil_slam import *

#pygame.init()
w = 1700
h = 900
slam = None
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
    ok = False
    if key == 'left':
        wm.move_robot_by(-20 , 0, 0)
        ok = True
        #wm.move_left(10)
    if key == 'right':
        wm.move_robot_by(20, 0, 0)
        #wm.move_right(10)
        ok = True
    if key == 'down':
        wm.move_robot_by(0, - 20, 0)
        #wm.move_up(10)
        ok = True
    if key == 'up':
        wm.move_robot_by(0, 20, 0)
        #wm.move_down(10)
        ok = True
    if key == "A":
        wm.display_world2(slam.locations, True)
        
    if ok == False:
        return
    
    robot_x, robot_y, robot_theta = wm.get_odom()
    angle_to_distance = wm.get_angle_distances()

    old_particles = slam.process_location_change(robot_x, robot_y, robot_theta, angle_to_distance)
    wm.add_particles(slam.get_particles())
    wm.display_world2(slam.locations, True)
    #print('Robot Odom: ', robot_x, robot_y, robot_theta)
    
# NUMBER OF PARTICLES
number_of_particles = 1000

initial_x = 110
initial_y = 110
initial_theta=0 
wm = WorldMap(w,h, initial_x, initial_y, initial_theta, cb)
angle_to_distance = wm.get_angle_distances()
slam = GilSlam(initial_x, initial_y, initial_theta, number_of_particles, w, h)
slam.add_to_map(angle_to_distance)
wm.init_graphics()
wm.display_world2(slam.locations, True)        
