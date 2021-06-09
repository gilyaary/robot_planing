import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import math


#These trajectories will always result in a well fixed pattern
#We can also go segment by segment
#We can decide to make shharp turns or not sharp turns
def __main_():
    
    target_x, target_y = 5, 20
    distance = math.sqrt(target_x*target_x+target_y*target_y) # ruff estimate of distance, actual distance is an integral
    lv = 0.01 # meter/seq
    av = 0.05
    count = 100
    x1 = np.zeros(count)
    y1 = np.zeros(count)
    
    for i in range(1, count):
        dt = float(i) / 1000.00 
        t = dt * i + 0.001
        angle = av * t * t 
        d_distance = lv * dt * t # same at every time frame
        dx = d_distance * math.cos(angle)
        dy = d_distance * math.sin(angle)
        x1[i] = x1[i-1] + dx
        y1[i] = y1[i-1] + dy
        
    plot(x1,y1)


def plot(x1,y1):
    #figure(figsize=(2, 2), dpi=80)
    plt.plot(x1, y1)
    #plt.plot(x2, y2)
    plt.xlim(-0.05,0.1)
    plt.ylim(-0.05,0.1)
    
    plt.xlabel('x - axis')
    plt.ylabel('y - axis')
    plt.title('My first graph!')
    plt.show()

__main_()