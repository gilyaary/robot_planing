import serial
from lidar_reader import *
import socket
import matplotlib.pyplot as plt


# buffer size 
BUFFSIZE = 2520 # packet 
HEADER = 0xFA # first packet constant 
FIRSTPACKET = 0xA0 # packet size 
PACKETSIZE = 42 # packet start index 
DATASTART = 4 # bytes in one 
OFFSETSIZE = 6 # number of probes 
NOFFSETS = 6 # end of data in packet 
DATAEND = 40 # null byte 
startCount = 0
conn = None
addr = None

def parser_callback (rpm, measurements):
    pass
    #distance = (measurements[0, 2] + measurements[0, 3] * 256) / 10
    #print(measurements[0, 5], ' degrees: ', distance)
    intensities = measurements[:, 0] + measurements[:, 1] * 256 #high_byte << 8 + low_byte
    distances = measurements[:, 2] + measurements[:, 3] * 256 #high_byte << 8 + low_byte

    degrees = measurements[:, 5]
    x = distances * np.sin(np.deg2rad(degrees))
    y = distances * np.cos(np.deg2rad(degrees))
    sc.set_offsets(np.c_[x,y])
    figure.canvas.draw_idle()
    figure.canvas.flush_events()

    for i in range (0, len(degrees)):
        if degrees[i] == 180:
            print(distances[i])
        
#index = int(NOFFSETS * (i / PACKETSIZE) + (j - DATASTART - i)/OFFSETSIZE)


plt.ion()
figure, ax = plt.subplots(figsize=(8,6))
degrees = range(0, 360, 6)
distances = np.zeros((60)) + 10
x = distances * np.sin(np.deg2rad(degrees))
y = distances * np.cos(np.deg2rad(degrees))
sc = ax.scatter(x,y)
plt.xlim(-60000,60000)
plt.ylim(-60000,60000)
plt.draw()


#SERIAL CONNECTION THREAD
with serial.Serial ( '/dev/ttyUSB0' , 230400 ) as ser :
    parser = FrameStreamParser(parser_callback)
    # create buffer 
    buff = [ 0 ] * BUFFSIZE
    print ( 'initiate transfer' )

    try :
        # pass the start byte to the lidar 
        #ser.write(b'g')
        ser.write(b'b')
        index = -1

        while True :
            index += 1
            value = int.from_bytes ( ser.read(), "big" )
            if value == 250:
                #print('sync found at index', index)
                pass
            else:
                #print(value)
                pass

            parser.add(value)

    finally :
        ser . write ( b'e')
        print ( 'end transmission' )
