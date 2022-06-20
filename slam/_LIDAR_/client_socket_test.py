# echo-client.py

import socket
import numpy as np
import matplotlib.pyplot as plt


HOST = "192.168.1.112"  # The server's hostname or IP address
PORT = 8080  # The port used by the server
MSGLEN = 2880

plt.ion()
figure, ax = plt.subplots(figsize=(8,6))
degrees = range(0, 360, 6)
distances = np.zeros((60)) + 10
x = distances * np.sin(np.deg2rad(degrees))
y = distances * np.cos(np.deg2rad(degrees))
sc = ax.scatter(x,y)
plt.xlim(-5500,5500)
plt.ylim(-5500,5500)
#plt.xlim(-4000,4000)
#plt.ylim(-4000,4000)

plt.draw()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #s.sendall(b"Hello, world")

    degrees_in_circle = range(0, 360, 1)
    angle_to_distance = dict()

    while True:
        

        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = s.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        
        data = b''.join(chunks)
        array = np.frombuffer(data, dtype=float)
        measurements = array.reshape(60,6)
        intensities = measurements[:, 0] + measurements[:, 1] * 256 #high_byte << 8 + low_byte
        distances = measurements[:, 2] + measurements[:, 3] * 256 #high_byte << 8 + low_byte
        degrees = measurements[:, 5]
        
        low = np.zeros((len(degrees))) + 175
        high = np.zeros((len(degrees))) + 185
        mask1 = np.logical_and(np.greater(degrees, low), np.less(degrees, high))
        
        low = np.zeros((len(degrees))) + 350
        high = np.zeros((len(degrees))) + 360
        mask2 = np.logical_and(np.greater(degrees, low), np.less(degrees, high))
        
        #distances *= np.logical_or(mask1, mask2)

        x = distances * np.sin(np.deg2rad(degrees))
        y = distances * np.cos(np.deg2rad(degrees))
        
        for i in range (len(degrees)):
            x_in_range = (x[i] > 10 or x[i] < -10) and (x[i] < 5500 or x[i] > -5500)
            y_in_range = (y[i] > 10 or y[i] < -10) and (y[i] < 5500 or y[i] > -5500)  
            if x_in_range and y_in_range:
                angle_to_distance[degrees[i]] = (x[i], y[i])

        xx = []
        yy = []

        for degree in angle_to_distance:
            xx.append(angle_to_distance[degree][0])
            yy.append(angle_to_distance[degree][1])

        sc.set_offsets(np.c_[xx,yy])
        figure.canvas.draw_idle()
        figure.canvas.flush_events()
        
