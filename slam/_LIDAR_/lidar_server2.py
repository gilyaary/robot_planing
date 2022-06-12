import serial
from lidar_reader2 import *
import socket
import numpy as np
import subprocess
import sys
sys.path.insert(1, '../orangepwm/')
from motor_pwm_control import *

test = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE)
output = str(test.communicate()[0])
lines = output.split("\\n")
host_ip = None

for line in lines:
    #print(line)
    if "192." in line:
        start_index = line.index("192.")
        end_index = line.index(' ', start_index)
        print('Host IP:', line[start_index:end_index])
        host_ip = line[start_index:end_index]


HOST = host_ip  # The server's hostname or IP address
PORT = 8081  # The port used by the server

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
motors = None #MotorPwmControl()

def parser_callback (rpm, measurements):
    bytes = measurements.tobytes()
    conn.sendall(bytes)
    print (len(bytes))
    cmd = conn.recv(32).decode().strip()
    print("response command: ", cmd)
    if len (cmd) > 0:
        segs = cmd.split(",")
        op = segs[0]
        if op == 'M':
            if len(segs) == 3:
                pass
                l = int(segs[1])
                r = int(segs[2])
                print ('Motor Command. Left:', l, 'Right:', r)
                motors.set_speed(l, r)
    
#SERVER TCP SOCKET THREAD
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # open serial port with serial . 
    s.bind((HOST, PORT))
    s.listen()
    

    while True:
        conn, addr = s.accept()
        try:
            print(f"Connected by {addr}")
            #data = conn.recv(1024)
            motors = MotorPwmControl()

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
                   
                    #while True:
                    #    v = ser.read(1024)




                finally :
                    ser . write ( b'e')
                    print ( 'end transmission' )
                    motors.stop()
        except:
            print('exception')
            conn.close()
            motors.stop()
