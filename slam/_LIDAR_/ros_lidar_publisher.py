#Setup:
#On both remote host and local
#export ROS_MASTER_URI=http://192.168.1.118:11311
#export ROS_IP=192.168.1.118


import serial
from lidar_reader2 import *
import numpy as np
import subprocess
import math
import sys
sys.path.insert(1, '../orangepwm/')
from time import sleep
#ROS
sys.path.append('/opt/ros/noetic/lib/python3/dist-packages/')
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String


#rospy.init_node('laser_scan_publisher')
num_readings = 100
laser_frequency = 40
#r = rospy.Rate(1.0)
r = None
scan_pub = None

test = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE)
output = str(test.communicate()[0])
lines = output.split("\\n")
host_ip = None
serial_enabled = False


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
cmd = None


def parser_callback (rpm, measurements):
    global cmd
    global scan_pub
    bytes = measurements.tobytes()

    # ROS
    global rospy
    global scan_pub
    global num_readings
    global laser_frequency
    global count
    global r
    current_time = rospy.Time.now()
    scan = LaserScan()
    scan.header.stamp = current_time
    scan.header.frame_id = 'laser_frame'
    scan.angle_min = 0
    scan.angle_max = math.pi *2
    scan.angle_increment = (math.pi *2) / 360
    scan.time_increment = (1.0 / laser_frequency) / (num_readings)
    scan.range_min = 1.0
    scan.range_max = 5000.0
    scan.ranges = measurements[:, 1]
    scan.intensities = measurements[:, 0]

    scan_pub.publish(scan)
    #r.sleep()


def stop_lidar():
    global serial_enabled
    serial_enabled = False
    print('stop lidar called')

def start_lidar():
    global serial_enabled
    
    if serial_enabled:
        return 

    serial_enabled = True
    print ('start_lidar_called')

    with serial.Serial ( '/dev/ttyUSB0' , 230400 ) as ser :
        parser = FrameStreamParser(parser_callback)
        # create buffer
        buff = [ 0 ] * BUFFSIZE
        print ( 'initiate transfer' )

        try :
            # pass the start byte to the lidar
            ser.write(b'b')
            #ser.write(b'g')
            index = -1

            while serial_enabled :
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


def callback(msg):
    print(msg)
    print(msg.data)
    if msg.data == 'start':
        print('starting')
        start_lidar()
    if msg.data == 'stop':
        print('stopping')
        stop_lidar()


def listener():
    global scan_pub
    global r
    rospy.init_node('lidar_scan_controller', anonymous=True)
    scan_pub = rospy.Publisher('scan', LaserScan, queue_size=50)
    r = rospy.Rate(1.0)

    sub = rospy.Subscriber('/lidar_command', String, callback)
    rospy.spin()
    print('spinning')

if __name__ == '__main__':
    listener()


