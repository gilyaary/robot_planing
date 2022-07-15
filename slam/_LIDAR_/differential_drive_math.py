import math 

def calc (dl, dr, w2w):
    dldr_diff = (dl-dr)
    if dldr_diff == 0:
        dldr_diff = 0.000000000001
    r1 = (dr/dldr_diff) * w2w

    #something wrong here !
    #dtheta = (dl - dr) / (2 * math.pi)
    dtheta = (dl - dr) / w2w

    dxr2 = (r1 - (r1 * math.cos(dtheta)))
    dyr2 = (r1 * math.sin(dtheta))
    dxl2 = (w2w + r1) - (w2w+r1) * math.cos(dtheta)
    dyl2 = (w2w + r1) * math.sin(dtheta)
    return r1, dtheta, dxl2, dyl2, dxr2, dyr2

def rotate_and_add(x,y,theta,dx,dy):
    x_new = x + math.cos(theta)*dx - math.sin(theta)*dy
    y_new = y + math.sin(theta)*dx + math.cos(theta)*dy
    return x_new, y_new

def main():
    #dl = 6.28 # 0.25 circum
    #dr = 0 #6.27999
    dl = 6.28
    dr = 3.14
    w2w = 4 # circum = 25.12
    r1, dtheta, dxl, dyl, dxr, dyr = calc (dl, dr, w2w)
    #print(r1, dtheta*360/(2*math.pi), dxl, dyl, dxr, dyr)

    x = 0
    y = 0
    theta = (10/360) * 2 * math.pi
    dx = (dxr+dxl) / 2
    dy = (dyr+dyl) / 2
    print(x+dx, y+dy)
    x_new, y_new = rotate_and_add(x,y,theta,dx,dy)
    print(x_new, y_new)
