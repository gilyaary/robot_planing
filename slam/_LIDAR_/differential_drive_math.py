import math 

def calc (dl, dr, w2w):
    r1 = (dr/(dl-dr)) * w2w
    dtheta = (dl - dr) / (2 * math.pi)
    dxr2 = (r1 - (r1 * math.cos(dtheta)))
    dyr2 = (r1 * math.sin(dtheta))
    dxl2 = (w2w + r1) - (w2w+r1) * math.cos(dtheta)
    dyl2 = (w2w + r1) * math.sin(dtheta)
    return r1, dtheta, dxl2, dyl2, dxr2, dyr2

def rotate_and_add(x,y,theta,dx,dy):
    x_new = x + math.cos(theta)*dx - math.sin(theta)*dy
    y_new = y + math.sin(theta)*dx + math.cos(theta)*dy
    return x_new, y_new

dl = 12
dr = 2
w2w = 4
r1, dtheta, dxl, dyl, dxr, dyr = calc (dl, dr, w2w)
print(r1, dtheta*360/(2*math.pi), dxl, dyl, dxr, dyr)
x = 0
y = 0
theta = 0
dx = (dxr+dxl) / 2
dy = (dyr+dyl) / 2
x_new, y_new = rotate_and_add(x,y,theta,dx,dy)
print(x_new, y_new)