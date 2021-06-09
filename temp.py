# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt
import numpy as np
import torch

def __main_():
    #x = torch.rand(5, 3)
    #print(x)
    # importing the required module
    
    x = np.zeros(20)
    y = np.zeros(20)
    start_x = 0
    start_y = 0
    target_x = 5
    target_y = 20
    lv = 1 # 1 meter / sec
    plot(x,y)

def plot(x, y):
    # plotting the points
    plt.plot(x, y)
    
    # naming the x axis
    plt.xlabel('x - axis')
    # naming the y axis
    plt.ylabel('y - axis')
    
    # giving a title to my graph
    plt.title('My first graph!')
    
    # function to show the plot
    plt.show()


__main_()