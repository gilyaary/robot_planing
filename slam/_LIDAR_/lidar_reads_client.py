# echo-client.py

import socket
import numpy as np
import matplotlib.pyplot as plt

HOST = '192.168.1.112'  # The server's hostname or IP address
PORT = 8081  # The port used by the server
MSGLEN = 5760

plt.ion()
figure, ax = plt.subplots(figsize=(8,6))
degrees = range(0, 360, 1)
distances = np.zeros(360)
x = distances * np.sin(np.deg2rad(degrees))
y = distances * np.cos(np.deg2rad(degrees))
sc = ax.scatter(x,y)
plt.xlim(-1500,1500)
plt.ylim(-1500,1500)
#plt.xlim(-1000,1000)
#plt.ylim(-1000,1000)
plt.draw()

def main ():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("connected to host on port 8081")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            #s.sendall(b"Hello, world")
            measurements = np.zeros((360, 2))
            measurements_display = np.zeros((360, 2))

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
                # TODO: Create a copy and put this on a a thread
                measurements_orig = array.reshape(360,2)
            
                #print("received valid frame set")

                #Fixing angle issues:
                
                start = 240
                measurements[0: 360 - start, :] = measurements_orig [start: 360]
                measurements[360 - start:360, :] = measurements_orig [0: start]
                
                intensities = measurements[:, 0]
                distances = measurements[:, 1]
                cmd = get_command(distances, intensities)    
                bytes = str.encode(cmd)
                s.sendall(bytes)
                

                degrees = range(360)
                x = distances * np.cos(np.deg2rad(degrees)) # + xx
                y = distances * np.sin(np.deg2rad(degrees)) # + yy
                sc.set_offsets(np.c_[x,y*-1])
                figure.canvas.draw_idle()
                figure.canvas.flush_events()
                #:(x,y)

            

COMMAND_SIZE = 32
_last_command = " " * COMMAND_SIZE
_call_num = 0

long_short_balance = 0
tc1 = False
tc2 = False

def get_command (distances, intensities):
    distances = np.flip(distances)
    intensities = np.flip(intensities)
    global _last_command
    global _call_num
    global long_short_balance
    global tc1, tc2
    _call_num += 1
       
    #TODO implement obstacle detection and avoidance algorithm here
    cmd = ' ' * COMMAND_SIZE
    
    #too_close = np.any(np.less(distances[355:360], 200))
    start_angle1 = 0
    end_angle1 = 60
    start_angle2 = 300
    end_angle2 = 360
    min_distance = 400
    
    mask = (np.less(distances, 10) * 1) * 5000
    distances += mask

    too_close1 = np.any( np.logical_and(np.less(distances[start_angle1:end_angle1], min_distance), np.greater(intensities[start_angle1:end_angle1], 100) ) )
    too_close2 = np.any( np.logical_and(np.less(distances[start_angle2:end_angle2], min_distance), np.greater(intensities[start_angle2:end_angle2], 100) ) )
    
    if tc1 != too_close1 or tc2 != too_close2:
        print(too_close1,too_close2)
        #print(distances[start_angle1:end_angle1])
    tc1 = too_close1
    tc2 = too_close2
    
    too_close = too_close1 or too_close2
    #print(too_close)
    #print(intensities[355:360])
    if too_close and long_short_balance <= 2:
        long_short_balance += 1
    elif not too_close and long_short_balance >= -2:
        long_short_balance -= 1

    if too_close:# and long_short_balance == 2:
        cmd = 'M,0,0'
        cmd = cmd + ' ' * (COMMAND_SIZE - len(cmd))  
    elif not too_close:# and long_short_balance == -2:
        cmd = 'M,1,1'
        cmd = cmd + ' ' * (COMMAND_SIZE - len(cmd))  
    

    
    #return  ' ' * 32
    
    if cmd != _last_command:
        #print("sending command: ", cmd)
        _last_command = cmd
        return cmd
    else:
        return ' ' * 32
    

if __name__ == "__main__":
    main()


'''
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

        
'''
