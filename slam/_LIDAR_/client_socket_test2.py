# echo-client.py

import socket
import numpy as np
import matplotlib.pyplot as plt


HOST = "192.168.1.87"  # The server's hostname or IP address
PORT = 8080  # The port used by the server
MSGLEN = 5760

plt.ion()
figure, ax = plt.subplots(figsize=(8,6))
degrees = range(0, 360, 1)
distances = np.zeros(360)
x = distances * np.sin(np.deg2rad(degrees))
y = distances * np.cos(np.deg2rad(degrees))
sc = ax.scatter(x,y)
plt.xlim(-4200,4200)
plt.ylim(-4200,4200)
#plt.xlim(-1000,1000)
#plt.ylim(-1000,1000)

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
        measurements = array.reshape(360,2)
        intensities = measurements[:, 0]
        distances = measurements[:, 1]
        degrees = range(360)

        #print(intensities[180])
        
        # low = np.zeros((len(degrees))) + 175
        # high = np.zeros((len(degrees))) + 185
        # mask1 = np.logical_and(np.greater(degrees, low), np.less(degrees, high))
        
        # low = np.zeros((len(degrees))) + 350
        # high = np.zeros((len(degrees))) + 360
        # mask2 = np.logical_and(np.greater(degrees, low), np.less(degrees, high))
        
        #distances *= np.logical_or(mask1, mask2)

        #mask = np.logical_and(np.greater(distances, -5),np.less(distances, 5))
        #xx = x * mask
        #yy = y * mask

        x = distances * np.sin(np.deg2rad(degrees)) # + xx
        y = distances * np.cos(np.deg2rad(degrees)) # + yy
        
        sc.set_offsets(np.c_[x,y])
        figure.canvas.draw_idle()
        figure.canvas.flush_events()
        
