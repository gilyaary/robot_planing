import serial
from lidar_reader2 import *
import socket
import numpy as np

HOST = "192.168.1.87"  # Standard loopback interface address (localhost)
PORT = 8080  # Port to listen on (non-privileged ports are > 1023)

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
    bytes = measurements.tobytes()
    conn.sendall(bytes)
    print (len(bytes))

    
    


#SERVER TCP SOCKET THREAD
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # open serial port with serial . 
    s.bind((HOST, PORT))
    s.listen()
    
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        #data = conn.recv(1024)


        #SERIAL CONNECTION THREAD
        with serial.Serial ( '/dev/ttyUSB0' , 230400 ) as ser :
            parser = FrameStreamParser(parser_callback)
            # create buffer 
            buff = [ 0 ] * BUFFSIZE
            print ( 'initiate transfer' )

            try :
                # pass the start byte to the lidar 
                ser.write(b'b')
                #ser.write(b'b')
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
