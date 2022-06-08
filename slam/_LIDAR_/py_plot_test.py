import matplotlib.pyplot as plt
import numpy as np
from math import *

degrees = range(0, 180, 1)
angle_to_distance = dict()
for degree in degrees:
    angle_to_distance[degree] = 1000


degrees = range(180, 360, 1)
for degree in degrees:
    angle_to_distance[degree] = 1500

x = []
y = []
for angle in angle_to_distance:
    distance = angle_to_distance[angle]
    _x = distance * cos(2*pi*angle/360)
    _y = distance * sin(2*pi*angle/360)
    x.append(_x)
    y.append(_y)

plt.scatter(x, y)
plt.show()