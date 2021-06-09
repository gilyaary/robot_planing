import matplotlib.pyplot as plt
import numpy as np
import math

def __main_():
    
    target_x, target_y = 5, 20
    distance = math.sqrt(target_x*target_x+target_y*target_y) # ruff estimate of distance, actual distance is an integral
    lv = 1 # meter/seq
    est_time_to_traget = distance / lv 
    x1 = np.zeros(20)
    y1 = np.zeros(20)
    #x2 = np.zeros(20)
    #y2 = np.zeros(20)
    
    tg_theta = target_y / target_x
    theta = math.atan(tg_theta)
    
    print(tg_theta)
    
    #estimate the time
    for i in range(0, 20):
        av = float(i) / 20.00
        distance_x = math.sin(theta+av*est_time_to_traget) - math.sin(theta)
        distance_y = math.cos(theta+av*est_time_to_traget) - math.cos(theta)
        distance_y2x = distance_y / (distance_x+0.00001)
        x1[i] = av
        y1[i] = distance_y2x
    plot(x1,y1)


def plot(x1,y1):
    plt.plot(x1, y1)
    #plt.plot(x2, y2)
    
    plt.xlabel('x - axis')
    plt.ylabel('y - axis')
    plt.title('My first graph!')
    plt.show()

__main_()