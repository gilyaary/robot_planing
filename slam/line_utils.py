from multiprocessing.connection import answer_challenge
import numpy as np
import math as math

#No need to recalculate the b_matrix and m_matrix they stay the same.
#we just need the robot's m and b for each degree and calculating lines 27 for intersect
def find_closest_intersecting_line(robot_xy, robot_theta_x, lines_matrix):
    debug = False
    
    np.set_printoptions(precision=2)    
    
    m_matrix = (lines_matrix[:,3]-lines_matrix[:,1]) / (lines_matrix[:,2]-lines_matrix[:,0]+0.00000000000000001) #dy/dx
    b_matrix = lines_matrix[:,1] - m_matrix*lines_matrix[:,0] # b = y - mx
    
    if debug:
        print('m_matrix', m_matrix) #x points of intersection
        print('b_matrix', b_matrix) #y points of intersection

    angle_distance = []

    for i in range(0, 360):
        dt = i/360 * (math.pi*2) + 0.00000000001
        current_robot_theta = robot_theta + dt     
        m_robot = math.tan(current_robot_theta)
        #print(m_robot)
        
        # y = mx + b
        b_robot = robot_xy[1] - m_robot*robot_xy[0]
        #print(b_robot)
        
        #m_robot = np.tile(m_robot, (2, 1))
        #b_robot = np.tile(b_robot, (2, 1))
        if debug:
            print('mrobot', m_robot)
            print('brobot', b_robot)
        
        x_intersect = (b_robot - b_matrix) / (m_matrix - m_robot) # from equation for height
        if debug:
            print('x_intersect', x_intersect)
        y_intersect = (m_robot * x_intersect) + b_robot # line formula applied with x_intersect on robot
        if debug:
            print('y_intersect', y_intersect)

        x = np.concatenate(([lines_matrix[:,0]], [lines_matrix[:,2]]), axis=0)
        y = np.concatenate(([lines_matrix[:,1]], [lines_matrix[:,3]]), axis=0)
        
        x_min = x.min(axis=0)
        x_max = x.max(axis=0)
        y_min = y.min(axis=0)
        y_max = y.max(axis=0)

        #print('x_min, x_max, y_min, y_max', x_min, x_max, y_min, y_max)
        
        point_in_lines_x = (x_intersect >= x_min)*1 * (x_intersect <= x_max)*1 # use in() function
        point_in_lines_y = (y_intersect >= y_min)*1 * (y_intersect <= y_max)*1 # use in() function
        
        point_in_correct_direction = 0
        
        if current_robot_theta <= math.pi:
            point_in_correct_direction = y_intersect >= robot_xy[1] *1
        else:
            point_in_correct_direction = y_intersect < robot_xy[1] * 1

        if current_robot_theta <= math.pi * 0.5:
            point_in_correct_direction = x_intersect >= robot_xy[0] *1
        elif current_robot_theta <= math.pi:
            point_in_correct_direction = x_intersect <= robot_xy[0] * 1
        elif current_robot_theta <= math.pi * 1.5:
            point_in_correct_direction = x_intersect <= robot_xy[0] * 1
        else:
            point_in_correct_direction = x_intersect >= robot_xy[0] * 1

        if debug:
            #print(point_in_lines_x)
            #print(point_in_lines_y)
            pass
        mask = (point_in_lines_x * point_in_lines_y * point_in_correct_direction)
        #print(mask)
        
        distances = np.sqrt((x_intersect-robot_xy[0])*(x_intersect-robot_xy[0]) + (y_intersect-robot_xy[1]) * (y_intersect-robot_xy[1]))
        if debug:
            print('distances', distances)
        #print('distances', distances)

        proximities = (1 / (distances)) * mask
        if debug:
            print ('proximities', proximities * mask) 
        distance_to_closest_object = 1 / (np.max(proximities) + 0.0000000001)
        #we may also need the index of the closest line
        if debug:
            print('distances to closest object', distance_to_closest_object)
        
        robot_degrees = ((current_robot_theta/(math.pi*2)) * 360)%360
        #print( '{:0.2f} degrees => {:0.2f}'.format(robot_degrees, distance_to_closest_object) )
        angle_distance.append([robot_degrees, distance_to_closest_object])
        #print('##########################\n')
    #for x in angle_distance:
    #    print( '{:0.2f} degrees => {:0.2f}'.format(x[0], x[1]) )
    #    pass
    return angle_distance

robot_xy = np.array([7,3])
robot_theta = (0 / 360) * 2 * math.pi
lines_matrix = np.array([
    [8,6,10,4],
    [5,3,7,1],
    [9,3,11,1],
])
#print(lines_matrix[:,0])
#find_closest_intersecting_line(robot_xy, robot_theta, lines_matrix)