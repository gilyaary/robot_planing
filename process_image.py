from typing import AsyncContextManager
from scipy import misc
import matplotlib.pyplot as plt
import numpy as np

image = misc.face()[:,:,0]
image = plt.imread('/home/gil/Pictures/cat.jpg')[:,:,0]
w, h = image.shape
print(image.shape)


f, axarr = plt.subplots(1,2)
plt.gray()
axarr[0].axis("off") # removes the axis and the ticks
axarr[0].imshow(image)


ascent_image = image.copy()
dtype = [('row', int), ('col', int), ('level', int)]
pixel_locations_and_levels = []
for row in range(0, w):
    for col in range(0, h):
        pixel_locations_and_levels.append((row, col, ascent_image[row,col])) # add a tuple
pixel_locations_and_levels_numpy = np.array(pixel_locations_and_levels, dtype=dtype)
x = np.sort(pixel_locations_and_levels_numpy, order='level') 


for i in range(0, len(x)):
    row, col = x[i][0], x[i][1]
    level = float(i)/float(len(x)) * 255
    ascent_image[row, col] = int (level)

#print(ascent_image[100:150, 100:150])
axarr[1].axis("off") # removes the axis and the ticks
axarr[1].imshow(ascent_image)
plt.show()