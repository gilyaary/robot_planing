import numpy as np
import math as math

#No need to recalculate the b_matrix and m_matrix they stay the same.
#we just need the robot's m and b for each degree and calculating lines 27 for intersect
def find_closest_intersecting_line(robot_xy, robot_theta, lines_matrix):
    
    m_robot = math.tan(robot_theta)
    #print(m_robot)
    
    # y = mx + b
    b_robot = robot_xy[1] - m_robot*robot_xy[0]
    #print(b_robot)
    
    #m_robot = np.tile(m_robot, (2, 1))
    #b_robot = np.tile(b_robot, (2, 1))
    print(m_robot)
    print(b_robot)
    
    m_matrix = (lines_matrix[:,3]-lines_matrix[:,1]) / (lines_matrix[:,2]-lines_matrix[:,0]) #dy/dx
    b_matrix = lines_matrix[:,1] - m_matrix*lines_matrix[:,0] # b = y - mx
    
    print(m_matrix) #x points of intersection
    print(b_matrix) #y points of intersection


    x_intersect = (b_robot - b_matrix) / (m_matrix - m_robot) # from equation for height
    print(x_intersect)
    y_intersect = (m_robot * x_intersect) + b_robot # line formula applied with x_intersect on robot
    print(y_intersect)

    #print(lines_matrix[:,0] > x_intersect)

    
    point_in_lines_x = (x_intersect >= lines_matrix[:,0])*1 * (x_intersect <= lines_matrix[:,2]) # use in() function
    point_in_lines_y = (y_intersect >= lines_matrix[:,3])*1 * (y_intersect <= lines_matrix[:,1]) # use in() function

    print(point_in_lines_x * point_in_lines_y)
    
    
    pass



robot_xy = np.array([7,3])
robot_theta = math.pi*0.25
lines_matrix = np.array([
    [8,6,10,4],
    [5,3,7,1],
    [9,3,11,1],
])

#print(lines_matrix[:,0])


find_closest_intersecting_line(robot_xy, robot_theta, lines_matrix)