import serial
from lidar_reader import *

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

def parser_callback (rpm, measurements):
    pass

# open serial port with serial . 
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
