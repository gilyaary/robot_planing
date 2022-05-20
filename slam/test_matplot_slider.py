import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
fig, ax = plt.subplots()
image = np.random.rand(3, 3)
img = ax.imshow(image)
axcolor = 'yellow'
ax_slider = plt.axes([0.20, 0.01, 0.65, 0.03], facecolor=axcolor)
slider = Slider(ax_slider, 'Slide->', 0.1, 30.0, valinit=2)
def update(val):
   ax.imshow(np.random.rand(3, 3))
   fig.canvas.draw_idle()
slider.on_changed(update)
plt.show()