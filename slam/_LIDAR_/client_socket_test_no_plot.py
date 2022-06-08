# echo-client.py

import socket
import numpy as np
import matplotlib.pyplot as plt


HOST = "192.168.1.87"  # The server's hostname or IP address
PORT = 8080  # The port used by the server
MSGLEN = 2880


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #s.sendall(b"Hello, world")
    while True:
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = s.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        
        #print('buffer full')

        data = b''.join(chunks)
        array = np.frombuffer(data, dtype=float)
        measurements = array.reshape(60,6)
        intensities = measurements[:, 0] + measurements[:, 1] * 256 #high_byte << 8 + low_byte
        distances = measurements[:, 2] + measurements[:, 3] * 256 #high_byte << 8 + low_byte

        
        degrees = measurements[:, 5]
        for i in range (0, len(degrees)):
            if degrees[i] > 179 and degrees[i] < 181 and intensities[i] > 50 and distances[i] < 4000 and distances[i] > 10:
                print(distances[i]) 
            #if angle[i] == 90:
            #    print(measurements[i, : ])
            #if angle[i] == 270:
            #    print(measurements[i, : ])
            #if angle[i] == 0:
            #    print(measurements[i, : ])
