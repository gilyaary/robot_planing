#!/usr/bin/env python  
import roslib
import rospy
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3


import tf


######
##  To get this data we need to run: 
#      rosrun imu_complementary_filter complementary_filter_node &
# This will take the data from:
#    /imu/data_raw (sensor_msgs.msg.Imu) 
#and convert to:
#    /imu/data (sensor_msgs.msg.Imu)
######



#We can do multiple conversions here but we just need to convert from one frame now.
# We call this frame laser_frame (This is what we use in our /scan topic as frame_id)
def imu_message_callback(imu: Imu):

    la = imu.linear_acceleration
    aa = imu.angular_velocity

    time_sec = rospy.Time.now().to_sec() 
    time = rospy.Time.from_sec(time_sec)
    
    #Todo: We need to use acceleration data to calculate location
    #we always assume we start at location 0,0 
    # The actual location on the map must be later determined by GPS or Localization
    # We start by assumeing that location does not change

    #print(imu.orientation.x, imu.orientation.y, imu.orientation.z)
    odom_pub = rospy.Publisher("odom", Odometry, queue_size=50)
    br = tf.TransformBroadcaster()
    br.sendTransform(( 0,0,0 ),
                     tf.transformations.quaternion_from_euler(0, 0, 0),
                     time,
                     "laser_frame",
                     "base_link")
    
    br.sendTransform(( 0,0,0 ),
                     #tf.transformations.quaternion_from_euler(imu.orientation.x, imu.orientation.y, imu.orientation.z),
                     tf.transformations.quaternion_from_euler(0, 0, 0),
                     time,
                     "base_link",
                     "base_footprint")

    #This we should set per odometry
    br.sendTransform(( 0,0,0 ),
                     tf.transformations.quaternion_from_euler(0, 0, 0),
                     time,
                     "base_footprint",
                     "odom")

    br.sendTransform(( 0,0,0 ),
                     tf.transformations.quaternion_from_euler(0, 0, 0),
                     time,
                     "odom",
                     "nav")

    br.sendTransform(( 0,0,0 ),
                     tf.transformations.quaternion_from_euler(0, 0, 0),
                     time,
                     "nav",
                     "map")

    

if __name__ == '__main__':
    rospy.init_node('gil_laser_scan_tf_broadcaster')
    rospy.Subscriber('/imu/data', Imu, imu_message_callback)
    rospy.spin()

#To get the data on /imu/data we need a publisher that listens to /imu/data_raw and converts to quaterians/
