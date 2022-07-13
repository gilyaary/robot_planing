import numpy as np
import matplotlib.pyplot as plt
import rospy
from geometry_msgs.msg  import Twist
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan

right_motor_pub: rospy.Publisher = None
left_motor_pub:rospy.Publisher = None
r = None
_last_command = None
_call_num = -1
long_short_balance = 0

def get_command (laserScan: LaserScan):
    distances = np.flip(laserScan.ranges)
    intensities = np.flip(laserScan.intensities)
    global _last_command, long_short_balance, _call_num
    
    #too_close = np.any(np.less(distances[355:360], 200))
    start_angle1 = 90
    end_angle1 = 150
    start_angle2 = 90
    end_angle2 = 150

    #0.5 meter
    min_distance = 4
    
    #too_close1 = np.any( np.logical_and(np.less(distances[start_angle1:end_angle1], min_distance), np.greater(intensities[start_angle1:end_angle1], 100) ) )
    #too_close2 = np.any( np.logical_and(np.less(distances[start_angle2:end_angle2], min_distance), np.greater(intensities[start_angle2:end_angle2], 100) ) )
    too_close1 = np.any( np.logical_and(np.less(distances[start_angle1:end_angle1], min_distance), np.greater(intensities[start_angle1:end_angle1], 100) ) )
    too_close2 = np.any( np.logical_and(np.less(distances[start_angle2:end_angle2], min_distance), np.greater(intensities[start_angle2:end_angle2], 100) ) )
    

    too_close = too_close1 or too_close2
    if too_close and long_short_balance <= 2:
        long_short_balance += 1
    elif not too_close and long_short_balance >= -2:
        long_short_balance -= 1

    if too_close:
        print('too close')
        right_motor_pub.publish(0)
        left_motor_pub.publish(0)
    elif not too_close:
        print('ok')
        right_motor_pub.publish(30)
        left_motor_pub.publish(30)
    
def listener():
    global right_motor_pub, left_motor_pub, r
    rospy.init_node('lidar_scan_changer', anonymous=True)
    right_motor_pub = rospy.Publisher('right_motor', Float64, queue_size=50)
    left_motor_pub = rospy.Publisher('left_motor', Float64, queue_size=50)
    r = rospy.Rate(1.0)

    sub = rospy.Subscriber('/scan2', LaserScan, get_command)
    rospy.spin()
    print('spinning')

if __name__ == '__main__':
    listener()
