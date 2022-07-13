import numpy as np
import math
from time import sleep
#ROS
import rospy
from sensor_msgs.msg import LaserScan


num_readings = 100
laser_frequency = 40
r = None
scan_pub = None

def callback (orig_scan : LaserScan):
    global cmd
    global scan_pub
    
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
    scan.range_min = 0.01
    scan.range_max = 50.0
    #to do change it
    size = len(orig_scan.ranges)
    ranges = np.zeros(size)
    for i in range(size):
        if orig_scan.ranges[i] < 0.0001:
            ranges[i] = math.inf  #50
        else:
            ranges[i] = orig_scan.ranges[i]/1000
    scan.ranges = ranges
    scan.intensities = orig_scan.intensities

    scan_pub.publish(scan)
    #r.sleep()


def listener():
    global scan_pub
    global r
    rospy.init_node('lidar_scan_changer', anonymous=True)
    scan_pub = rospy.Publisher('scan2', LaserScan, queue_size=50)
    r = rospy.Rate(1.0)

    sub = rospy.Subscriber('/scan', LaserScan, callback)
    rospy.spin()
    print('spinning')

if __name__ == '__main__':
    listener()


