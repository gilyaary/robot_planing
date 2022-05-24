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
    #print('callback called with Key: ' + key) 
    x,y,theta = wm.get_robot()
    if key == 'left':
        wm.move_robot_by(-20 , 0, 0)
        #wm.move_left(10)
    if key == 'right':
        wm.move_robot_by(20, 0, 0)
        #wm.move_right(10)
    if key == 'up':
        wm.move_robot_by(0, - 20, 0)
        #wm.move_up(10)
    if key == 'down':
        wm.move_robot_by(0, 20, 0)
        #wm.move_down(10)
    
    robot_x, robot_y, robot_theta = wm.get_odom()
    angle_to_distance = wm.get_angle_distances()

    slam.process_location_change(robot_x,robot_y,robot_theta, angle_to_distance)
    wm.add_particles(slam.get_particles())
    wm.add_slam_map(slam.get_last_map()) #lets show this as a map on top later

    wm.display_world(False)


    print('Robot Odom: ', robot_x, robot_y, robot_theta)
    

initial_x = 100
initial_y = 100
initial_theta=0 
number_of_particles = 1
slam = GilSlam(initial_x, initial_y, initial_theta, number_of_particles, w, h)
wm = WorldMap(w,h, cb)

    #wm.get_pose_from_odometry()
    #wm.get_sensor_readings() #comes as distance from robot. For map we need to translate to world map coordinates
    #Now update the location hypothesis and SAVE the sensor data. 

     

