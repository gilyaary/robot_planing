import math
import numpy as np
import random

'''
    Mapping
    1. Start with 10000 particles centered at starting location - particles have similar or identical x,y and pose
    2. Robot Moves
    3. Move particles per the probability of moving by a certain distance and theta:
        For Each Sample:
            delta_distance = take weighted sample from distance distribution per speed (variance propotional to speed)
            delta_theta = take weighted sample from theta distribution
            Move the sample by:
                dx = delta_distance*cos(theta_sample+delta_theta)
                dy = delta_distance*sin(theta_sample+delta_theta)
    4. get sensor measurements
    5. for each sample calculate measurement probability per GLOBAL map. At state x1 we already have mapped measurements from state x0
    6. Assign a weight for each sample per step 5
    7. create new samples in each location per the weight
    8. randomly eliminate samples
    9. Go to step 2        
'''

class GilSlam:
    def __init__(self, initial_x, initial_y, initial_theta, number_of_particles, w, h):
        pass
        self.last_odom_x = initial_x
        self.last_odom_y = initial_y
        self.last_odom_theta = initial_theta
        self.number_of_particles = number_of_particles
        self.w = w
        self.h = h
        #Initialize the distribution of particles.
        #In Mapping we initialize the starting location and in localization we can choose a uniform distribution

        #each particle has: x, y, theta, weight
        self.particles = np.zeros((number_of_particles,4))
        
        mu, sigma = initial_x, 10 # mean and standard deviation
        x_values = np.random.normal(mu, sigma, number_of_particles)
        mu, sigma = initial_y, 10 # mean and standard deviation
        y_values = np.random.normal(mu, sigma, number_of_particles)
        mu, sigma = initial_theta, 10 # mean and standard deviation
        theta_values = np.random.normal(mu, sigma, number_of_particles)
        self.particles[:,0] = x_values
        self.particles[:,1] = y_values
        self.particles[:,2] = theta_values
        #print(self.particles)

    #1700,900,360 width, height, angles
    def get_particles(self):
        return self.particles

    def process_location_change(self, odom_robot_x, odom_robot_y, odom_robot_theta, angle_to_distance_map):
        dx = odom_robot_x - self.last_odom_x
        dy = odom_robot_y - self.last_odom_y
        d_theta = odom_robot_theta - self.last_odom_theta
        self.last_odom_x = odom_robot_x
        self.last_odom_y = odom_robot_y
        self.last_odom_theta = odom_robot_theta
        # Step 1: Update location belief based on odometry changes. We shift the belief per odom changes but we also
        # add some noise to all areas (flatten due to uncertainty and noise in odom)
         
        mu, sigma = dx, 10 # mean and standard deviation
        x_values = np.random.normal(mu, sigma, self.number_of_particles)
        mu, sigma = dy, 10 # mean and standard deviation
        y_values = np.random.normal(mu, sigma, self.number_of_particles)
        mu, sigma = d_theta, 10 # mean and standard deviation
        theta_values = np.random.normal(mu, sigma, self.number_of_particles)
        self.particles[:,0] += x_values
        self.particles[:,1] += y_values
        self.particles[:,2] += theta_values
        mask = (self.particles >= 0) * 1
        self.particles *= mask
        #print(self.particles)




'''
initial_x = 50
initial_y = 60 
initial_theta=90 
number_of_particles = 10
slam = GilSlam(initial_x, initial_y, initial_theta, number_of_particles)
slam.process_location_change(60,70,95, [])
'''