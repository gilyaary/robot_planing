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
        self.occupency_grid = np.zeros((w,h))
        self.last_map = []
        #Initialize the distribution of particles.
        #In Mapping we initialize the starting location and in localization we can choose a uniform distribution

        #each particle has: x, y, theta, weight
        self.particles = np.zeros((number_of_particles,4))
        
        mu, sigma = initial_x, 1 # mean and standard deviation
        x_values = np.random.normal(mu, sigma, number_of_particles)
        mu, sigma = initial_y, 1 # mean and standard deviation
        y_values = np.random.normal(mu, sigma, number_of_particles)
        mu, sigma = initial_theta, 1 # mean and standard deviation
        theta_values = np.random.normal(mu, sigma, number_of_particles)
        
        #self.particles[:,0] = x_values
        #self.particles[:,1] = y_values
        #self.particles[:,2] = theta_values
        
        self.particles[:,0] = initial_x
        self.particles[:,1] = initial_y
        self.particles[:,2] = initial_theta
        

        #print(self.particles)

    #1700,900,360 width, height, angles
    def get_particles(self):
        return self.particles

    def get_last_map(self):
        return self.last_map
    

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
        #mask = (self.particles >= 0) * 1
        #self.particles *= mask
        #print(self.particles)

        #self.occupency_grid
        #the grid will contain measurements. Each particle sends out a ray in a direction.
        #we need to check if the ray is reflected by an object at that point
        # We do the same thing we did with the robot for each particle in 360 degrees!
        # We check if it breaks a line. So we need to be able to convert the measurements z into
        # LINES and apply the same measurement we did for the robot to each and every sample

        # 3 odom vectors
        # odom_robot_x, odom_robot_y, odom_robot_theta
        measurements_xy = []
        for angle_distance in angle_to_distance_map:
            angle = angle_distance[0]
            distance = angle_distance[1]
            if not math.isnan(distance) and distance < 200:
                #print(angle, distance)
                #translate from polar to cartesian coordinates 
                x = distance * math.cos( (angle/360) * (math.pi*2) )
                y = distance * math.sin( (angle/360) * (math.pi*2) )
                measurements_xy.append([x,y,1])
        #print(measurements_xy)
        
        if len(measurements_xy) == 0:
            return

        for particle in self.particles:
            # transform each measurement to world frame per robot pose
            # for each transformed measurement find the closest one in the self.occupency_grid
            # get the total difference between each transformed measurement and its closest point
            # weight will be calculated as:
            # w = total_diff_all_particles / diff_of_current_particle
            # Use the particle with the largest weight to update the self.occupency_grid
            # We use the dot product to do the transformation
            particle_x = particle[0]
            particle_y = particle[1]
            particle_theta = particle[2]
            transformation_matrix = np.array([
                [math.cos(particle_theta), math.sin(particle_theta),0],
                [math.sin(particle_theta), math.cos(particle_theta),0],
                [0,0,1]
            ])

            #print(np.array(measurements_xy).shape)
            #print(transformation_matrix.shape)
            transformed = np.array(measurements_xy).dot(transformation_matrix)
            #print (transformed)
            self.last_map = transformed

            #Now find the difference between the transformed measurements and the occupency_grid
            pass

'''
initial_x = 50
initial_y = 60 
initial_theta=90 
number_of_particles = 10
slam = GilSlam(initial_x, initial_y, initial_theta, number_of_particles)
slam.process_location_change(60,70,95, [])
'''