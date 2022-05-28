import math
import numpy as np
import random
import matplotlib.pyplot as plt
import pygame
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

class Particle:
    def __init__(self,x,y,theta):
        self.x = x
        self.y = y
        self.theta = theta
        pass

    #these are the measurements after we transformed them to the reference frame
    #to find the angle amd distance from the particle to these points just use:
    # distance^2 = (point_x - particle_x)^2 + (point_y - particle_y)^2
    # and use the math.arctan(  (particle_y - point_y)/(particle_x - point_x)   ) to get the angle
    def set_transformed_measurements_xy(self,x,y):
        self.transformed_measured_points_x_locations = x
        self.transformed_measured_points_y_locations = y
    
    def set_weight(self, weight):
        self.weight = weight

class GilSlam:
    def __init__(self, initial_x, initial_y, initial_theta, number_of_particles, w, h):
        
        pass
        self.last_odom_x = initial_x
        self.last_odom_y = initial_y
        self.last_odom_theta = initial_theta
        self.number_of_particles = number_of_particles
        self.w = w
        self.h = h
        self.locations = dict()
        self.map_initialized = False
        self.last_map = []
        #Initialize the distribution of particles.
        #In Mapping we initialize the starting location and in localization we can choose a uniform distribution
        #each particle has: x, y, theta, weight
        self.particles = []
        self.number_of_particles = number_of_particles
        
        mu, sigma = self.last_odom_x, 1 # mean and standard deviation
        x_values = np.random.normal(mu, sigma, number_of_particles)
        mu, sigma = self.last_odom_y, 1 # mean and standard deviation
        y_values = np.random.normal(mu, sigma, number_of_particles)
        mu, sigma = initial_theta, 1 # mean and standard deviation
        theta_values = np.random.normal(mu, sigma, number_of_particles)

        for i in range (0, self.number_of_particles):
            self.particles.append(Particle(x_values[i], y_values[i], theta_values[i]))

    #1700,900,360 width, height, angles
    def get_particles(self):
        return self.particles

    def get_last_map(self):
        return self.last_map

    def add_to_map(self, angle_to_distance_map):
        #initial occupency grid
        measurements_theta_distance = []
        for angle_distance in angle_to_distance_map:
            angle = angle_distance[0]
            distance = angle_distance[1]
            if not math.isnan(distance) and distance < 200:
                measurements_theta_distance.append([angle,distance])
        if len(measurements_theta_distance) == 0:
            return
        angles = self.last_odom_theta + np.array(measurements_theta_distance)[:,0]
        x = self.last_odom_x + np.array(measurements_theta_distance)[:,1] * np.cos( (angles/360) * (math.pi*2) )
        y = self.last_odom_y + np.array(measurements_theta_distance)[:,1] * np.sin( (angles/360) * (math.pi*2) )
        self.map_initialized = True

    

    def process_location_change(self, odom_robot_x, odom_robot_y, odom_robot_theta, angle_to_distance_map):
        dx = odom_robot_x - self.last_odom_x
        dy = odom_robot_y - self.last_odom_y
        d_theta = odom_robot_theta - self.last_odom_theta
        
        self.last_odom_x = odom_robot_x
        self.last_odom_y = odom_robot_y
        self.last_odom_theta = odom_robot_theta
        #print('slam_odom', self.last_odom_x, self.last_odom_y)

        # Step 1: Update location belief based on odometry changes. We shift the belief per odom changes but we also
        # add some noise to all areas (flatten due to uncertainty and noise in odom)
         
        mu, sigma = dx, 3 # mean and standard deviation
        x_values = np.random.normal(mu, sigma, self.number_of_particles)
        print(x_values)
        mu, sigma = dy, 3 # mean and standard deviation
        y_values = np.random.normal(mu, sigma, self.number_of_particles)
        mu, sigma = d_theta, 2 # mean and standard deviation
        theta_values = np.random.normal(mu, sigma, self.number_of_particles)
        weight_map = np.zeros((self.w,self.h))
        for key in self.locations:
            weight_map[key[0], key[1]] = 1 
        
        for i in range(0,5):
            weight_map[0:self.w-2, :] += weight_map[1:self.w-1, :]*0.1
            weight_map[2:self.w, :] += weight_map[1:self.w-1, :]*0.1
            
            weight_map[:, 0:self.h-2] += weight_map[:, 1:self.h-1]*0.1
            weight_map[:, 2:self.h] += weight_map[:, 1:self.h-1]*0.2

        for i in range(len(self.particles)):
            self.particles[i].x += x_values[i]
            self.particles[i].y += y_values[i]
            self.particles[i].theta += theta_values[i]

        #the grid will contain measurements. Each particle sends out a ray in a direction.
        #we need to check if the ray is reflected by an object at that point
        # We do the same thing we did with the robot for each particle in 360 degrees!
        # We check if it breaks a line. So we need to be able to convert the measurements z into
        # LINES and apply the same measurement we did for the robot to each and every sample

        # 3 odom vectors
        # odom_robot_x, odom_robot_y, odom_robot_theta
        measurements_theta_distance = []
        for angle_distance in angle_to_distance_map:
            angle = angle_distance[0]
            distance = angle_distance[1]
            if not math.isnan(distance) and distance < 200 and distance > 1:
                #print(angle, distance)
                measurements_theta_distance.append([angle,distance])
        #print(measurements_xy)
        
        if len(measurements_theta_distance) == 0:
            return

        best_weight = -0.1
        best_particle = None

        for particle in self.particles:
            # transform each measurement to world frame per robot pose
            # for each transformed measurement find the closest one in the self.occupency_grid
            # get the total difference between each transformed measurement and its closest point
            # weight will be calculated as:
            # w = total_diff_all_particles / diff_of_current_particle
            # Use the particle with the largest weight to update the self.occupency_grid
            # We use the dot product to do the transformation
            particle_x = particle.x
            particle_y = particle.y
            particle_theta = particle.theta
            #We save the location of objects (respective to each particle) in x,y vectors
            # Only measurements in range are considered.
            #In mapping we will choose the most likely particle and save their x,y points (from the vectors) in the occupency grid
            mtd = np.array(measurements_theta_distance)
            angles = particle_theta + mtd[:,0]
            dist = mtd[:,1]
            x = particle_x + dist * np.cos( (angles/360) * (math.pi*2) )
            y = particle_y + dist  * np.sin( (angles/360) * (math.pi*2) )
            particle.set_transformed_measurements_xy(x,y)
            weight = 111110
            for i in range(len(x)):
                xx = int (x[i])
                yy = int (y[i])
                weight += weight_map[xx,yy]
            #Now find the difference between the transformed measurements and the occupency_grid
            particle.set_weight(weight)
            if weight > best_weight:
                best_weight = weight
                best_particle = particle
        
        if best_particle is not None:
            xxx = best_particle.transformed_measured_points_x_locations
            yyy = best_particle.transformed_measured_points_y_locations
            #Add the particle's projected map to the reference map
            for i in range (0, len(xxx)):
                x, y = int(xxx[i]),int(yyy[i])
                self.locations[(x,y)] = 1
            
            self.particles = []
            for i in range (0, self.number_of_particles):
                self.particles.append(Particle(best_particle.x, best_particle.y, best_particle.theta))


'''
initial_x = 50
initial_y = 60 
initial_theta=90 
number_of_particles = 10
slam = GilSlam(initial_x, initial_y, initial_theta, number_of_particles)
slam.process_location_change(60,70,95, [])
'''


'''
Points outside of the rectangle must be > radius in distance
if we build another rectangle we can make sure its diagonal is less than the radius of the outer one

x----------

'''