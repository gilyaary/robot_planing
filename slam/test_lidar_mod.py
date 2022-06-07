import serial

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

# open serial port with serial . 
with Serial ( '/dev/serial0' , 230400 ) as ser :

    # create buffer 
    buff = [ 0 ] * BUFFSIZE

    print ( 'initiate transfer' )

    try :

        # pass the start byte to the lidar 
        ser.write(b 'g')

        while True :

            # read bytes into buffer 
            buff [ startCount ] = int.from_bytes (ser.read (), "big" )
            # if the byte is the header of the packet and it is the zero element of the buffer 
            if startCount == 0 and buff [ startCount ] == HEADER : # change the index 
                startCount = 1
            # if the index is changed and the byte read is the first packet 
            if startCount == 1 and buff [ startCount ] == FIRSTPACKET : # reset the index 
                startCount = 0
            # write data to the buffer, starting from the third element 
            i = 2

            while i < BUFFSIZE :
                buff [ i ] = int . from_bytes ( ser . read (), "big" )
                i += 1
            for i in range ( 0 , BUFFSIZE , PACKETSIZE ):
                    # if the packet starts with a header and the packet index is correct 
                    if buff [ i ] == HEADER and buff [ i + 1 ] == int ( FIRSTPACKET + i / PACKETSIZE ):
                        # calculate data in batch 
                        for j in range ( i + DATASTART , i + DATAEND , OFFSETSIZE ):
                            index = int ( NOFFSETS * ( i / PACKETSIZE ) + ( j - DATASTART - i )/ OFFSETSIZE )
                            byte0 = buff [ j ]
                            byte1 = buff [ j + 1 ]
                            byte2 = buff [ j + 2 ]
                            byte3 = buff [ j + 3 ]
                            # intensity (quality) of the probe 
                            intensity = ( byte1 << 8 ) + byte0
                            # distance in mm 
                            distance = ( byte3 << 8 ) + byte2
                            # output data 
                            print ( "r[{}]={}" . format ( 359 - index , distance / 1000 ))
    finally :
        ser.write (b'e') print ( 'end transmission' )
                                                                                                                                                55,1          Bot

