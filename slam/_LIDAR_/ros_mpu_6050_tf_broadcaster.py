#!/usr/bin/env python  
import roslib
import rospy
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
from std_msgs.msg import Float64MultiArray
import math
import numpy as np 

import tf

######
##  To get this data we need to run: 
#      rosrun imu_complementary_filter complementary_filter_node &
# This will take the data from:
#    /imu/data_raw (sensor_msgs.msg.Imu) 
#and convert to:
#    /imu/data (sensor_msgs.msg.Imu)
######

######
#  We only get ticks from the wheel but we actually have 2 forces acting the the wheels. Left force and right force
#  The angular velocity whould be the velocity on the X direction (rotation) from the the robot is.
#  angular_velocity = left_velocity - right_velocity
#  When left == right => angular_velocity = 0, left > right => angular_velocity > 0, left < right => angular_velocity < 0
#  The linear velocity is on the current (perpendicular ro current robot orientation) it will be:
#  (right_velocity + left_velocity) *   
######



class BC:

    def __init__(self):
        self.left_dir = 1
        self.right_dir = 1
        rospy.init_node('gil_laser_scan_tf_broadcaster')
        rospy.Subscriber("motor_ticks_per_second", Float64MultiArray, self.motor_tps_callback)
        rospy.Subscriber("motor_speed", Float64MultiArray, self.motor_speed_callback)
        rospy.Subscriber('/imu/data', Imu, self.imu_message_callback)
        self.last_print_time = rospy.Time.now().to_sec()
        self.simulated_yaw = 0
        self.last_x = 0
        self.last_y = 0
        self.last_yaw = 0

        rospy.spin()

    #We can do multiple conversions here but we just need to convert from one frame now.
    # We call this frame laser_frame (This is what we use in our /scan topic as frame_id)
    def imu_message_callback(self, imu: Imu):

        la = imu.linear_acceleration
        aa = imu.angular_velocity

        time_sec = rospy.Time.now().to_sec() 
        time = rospy.Time.from_sec(time_sec)
        
        #Todo: We need to use acceleration data to calculate location
        #we always assume we start at location 0,0 
        # The actual location on the map must be later determined by GPS or Localization
        # We start by assumeing that location does not change

        #print(imu.orientation.x, imu.orientation.y, imu.orientation.z)
        #odom_pub = rospy.Publisher("odom", Odometry, queue_size=50)
        br = tf.TransformBroadcaster()
        #offset = (22 / 360) * 2 * math.pi
        location = ( self.last_x, self.last_y,0 )
        #We are getting the orientation from /imu/data ALREADY as quaternion so no need to change anything
        
        #rotation = (imu.orientation.x,imu.orientation.y,imu.orientation.z,imu.orientation.w)
        #rotation_euler = tf.transformations.euler_from_quaternion(rotation)
        rotation_euler = (0,0, self.last_yaw)
        rotation_euler = (rotation_euler[0],rotation_euler[1],rotation_euler[2])
        rotation_quaternion = tf.transformations.quaternion_from_euler(rotation_euler[0],rotation_euler[1],rotation_euler[2])
        
        
        self.last_yaw = rotation_euler[2]
        

        if rospy.Time.now().to_sec() - self.last_print_time > 3:
            self.simulated_yaw += math.pi / 2
            self.last_print_time = rospy.Time.now().to_sec()
            #self.show_euler(rotation_euler);

        br.sendTransform(( 0,0,0 ),
        tf.transformations.quaternion_from_euler(0, 0, 0),
          time,
          "laser_frame",
          "base_link")

        br.sendTransform(( 0,0,0 ),
          tf.transformations.quaternion_from_euler(0, 0, 0),
            time,
            "base_link",
            "base_footprint")

        # #This we should set per odometry
        br.sendTransform(( 0,0,0 ),
            rotation_quaternion,
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


      ##########################

        
        #this is a kind of "servo" feedback mechnism. We check the required tps vs the
        # actual tps from odometry and change the pwm value sent to the motors
    def motor_tps_callback(self, msg: Float64MultiArray):
        values = msg.data
        layout = msg.layout
        tps_1, tps_2, tick_1, tick_2 = values[0], values[1], values[2], values[3]
        delta_R = 0
        delta_L = 0
        if tick_1 != 0:
          delta_R = self.right_dir
        if tick_2 != 0:
          delta_L = self.left_dir

        wheelradius = 0.033
        w2w = 0.260 #wheel to wheel
        TPR = 20 # 20 ticks per round
        dl = 2 * math.pi * wheelradius * delta_L / TPR
        dr = 2 * math.pi * wheelradius * delta_R / TPR
        
        #self.last_x += dx
        #self.last_y += dy
        #self.last_yaw += dth
        #print(self.last_x, self.last_y)
    
    
    def motor_speed_callback(self, msg: Float64MultiArray):
        values = msg.data
        layout = msg.layout
        l, r = values[0], values[1]
        #print (l,r)
        if l > 0:
          self.left_dir = -1  
        elif l < 0:         
          self.left_dir = 1
        else:
          self.left_dir = 0
        if r > 0:
          self.right_dir = -1  
        elif r < 0:         
          self.right_dir = 1
        else:
          self.right_dir = 0


    def show_euler(self, quaternion):
        euler = tf.transformations.euler_from_quaternion(quaternion)
        degrees = np.zeros(3)
        roll = (360 + ((euler[0] / 6.26) * 360)) % 360
        pitch = (360 + ((euler[1] / 6.26) * 360)) % 360
        yaw =  (360 + ((euler[2] / 6.26) * 360)) % 360
        #print('yaw', yaw, 'yawRad', euler[2])



if __name__ == '__main__':
    bc = BC()

  #To get the data on /imu/data we need a publisher that listens to /imu/data_raw and converts to quaterians/

'''
  /tf
  transforms: 
    - 
      header: 
        seq: 3735
        stamp: 
          secs: 124
          nsecs: 500000000
        frame_id: "odom"
      child_frame_id: "base_footprint"
      transform: 
        translation: 
          x: -19.362049102783203
          y: -8.011297225952148
          z: 0.0
        rotation: 
          x: 0.0
          y: 0.0
          z: -0.7431448410766627
          w: 0.6691305890341149


# br.sendTransform(( 0,0,0 ),
        #     tf.transformations.quaternion_from_euler(0, 0, 0),
        #     time,
        #     "laser_frame",
        #     "base_link")

        # br.sendTransform(( 0,0,0 ),
        #     tf.transformations.quaternion_from_euler(imu.orientation.x, imu.orientation.y, imu.orientation.z),
        #     #tf.transformations.quaternion_from_euler(0, 0, 0),
        #     time,
        #     "base_link",
        #     "base_footprint")

        # #This we should set per odometry
        # br.sendTransform(( 0,0,0 ),
        #     tf.transformations.quaternion_from_euler(0, 0, 0),
        #     time,
        #     "base_footprint",
        #     "odom")

        # br.sendTransform(( 0,0,0 ),
        #     tf.transformations.quaternion_from_euler(0, 0, 0),
        #     time,
        #     "odom",
        #     "nav")

        # br.sendTransform(( 0,0,0 ),
        #     tf.transformations.quaternion_from_euler(0, 0, 0),
        #     time,
        #     "nav",
        #     "map")
          
'''