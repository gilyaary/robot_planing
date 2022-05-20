from geometrical_shapes import Frame, Point
import math
import pygame
import random
import numpy as np
import json

w = 800
h = 600
display = (w,h)
pygame.init()
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
gameDisplay = pygame.display.set_mode((w,h))
gameDisplay.fill(black)


def draw_line(gameDisplay, color, p1, p2, size):
    p11 = (p1[0],h-p1[1])
    p22 = (p2[0],h-p2[1])
    pygame.draw.line(gameDisplay, color, p11, p22 ,size)

def draw_frame(frame: Frame):
    draw_recursive(frame)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()    


def draw_recursive(frame: Frame):
    print("draw recursive")
    #draw_line(gameDisplay, blue, (0,0), (100,200),5)
    #draw_line(gameDisplay, white, (0,0), (0,200),5)
    #draw_line(gameDisplay, white, (0,0), (200,0),5)
    if frame.parent_frame is None:
        #draw world frame axis
        draw_line(gameDisplay, white, (0,0), (0,h),5)
        draw_line(gameDisplay, white, (0,0), (w,0),5)
    else:
        #Go back to the parent and calc the transformation to the world frame
        #We can use homogeneous coordinates to calc with martix multiplications
        rotation_matrix = frame.rotation_matrix
        translation_vector = frame.translation_vector
        print(translation_vector)
        current_parent: Frame = frame.parent_frame
        while current_parent.parent_frame is not None:
            parent_rotation_matrix = current_parent.rotation_matrix
            parent_translation_vector = current_parent.translation_vector
            print(parent_translation_vector)
            current_parent = current_parent.parent_frame
    
cos_45 = math.cos(math.radians(45))
sin_45 = math.sin(math.radians(45))

wf = Frame(None, None, None)
f1 = Frame(wf, [[cos_45,-sin_45],[sin_45, cos_45]], [5,5])
f1_1 = Frame(f1, [[cos_45,-sin_45],[sin_45, cos_45]], [6,6])
f1_1_1 = Frame(f1_1, [[cos_45,-sin_45],[sin_45, cos_45]], [7,7])
f1_1_1_1 = Frame(f1_1_1, [[cos_45,-sin_45],[sin_45, cos_45]], [8,8])
p_f1_1 = Point(f1, [3,6])
p_wf_1 = Point(f1, [3,6])
p_f11_1 = Point(f1, [3,6])
#draw_frame(wf)
draw_frame(f1_1_1_1)
#draw_point(p_f1_1)
#draw_point(p_wf_1)
#print(json.dumps(wf,default=lambda x: x.__dict__))

