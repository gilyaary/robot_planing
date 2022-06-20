import socket
import numpy as np
import subprocess
import sys
sys.path.insert(0, '/home/gil/code/python/orangepwm')
from motor_pwm_control import *
from time import sleep
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
PORT = 8082  # The port used by the server

# buffer size 
BUFFSIZE = 32 # packet 
startCount = 0
conn = None
addr = None
motors = MotorPwmControl()

#SERVER TCP SOCKET THREAD
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # open serial port with serial . 
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        try:
            print(f"Connected by {addr}")
            while True :
                cmd = conn.recv(32).decode()
                print('Received Command: ', cmd)
                if len (cmd) == 32:
                    cmd_clean = cmd.strip()
                    segs = cmd_clean.split(",")
                    op = segs[0]
                    if op == 'M':
                        if len(segs) == 3:
                            pass
                            l = int(segs[1])
                            r = int(segs[2])
                            print ('Motor Command. Left:', l, 'Right:', r)
                            motors.set_speed(l, r)
        except:
            print('exception')
        finally :
            motors.stop()
            conn.close()
