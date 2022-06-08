from cv2 import repeat
import numpy as np

degrees = range(0, 360, 6)
#print(len(degrees))
distances = np.zeros((60)) + 10
x = distances * np.sin(np.deg2rad(degrees))
y = distances * np.cos(np.deg2rad(degrees))
print(x[0:10])
print(y[0:10])
