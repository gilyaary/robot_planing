import matplotlib.pyplot as plt
import numpy as np
import math

np.set_printoptions(precision=3)
x = np.zeros(100)
y = np.zeros(100)
l_accl = -0.01 #meter/sec/sec
a_vel = -math.pi/200 #rad/sec
theta_0 = math.pi
x_val = 0
y_val = 100

for t in range (1, 101):
    l_vel = l_accl*t #temporary velocity
    l_change = l_vel * 1 # velocity * time_change
    theta = theta_0 + (a_vel * t)
    x_val += l_change * math.cos(theta)
    y_val += l_change * math.sin(theta)  
    x[t-1] = x_val
    y[t-1] = y_val
print(x)

plt.plot(x, y, 'ro')
plt.axis([0, 120, 0, 120])
plt.show()