#! /usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
import tf
import numpy as np

x, y, z = 0,0,0
speed_x, speed_y, speed_z = 0,0,0
rx,ry,rz,rw = 0,0,0,0
last_time = None
iter = 0

def imu_message_callback(imu: Imu):
    # x = imu.angular_velocity.x
    # y = imu.angular_velocity.y
    # z = imu.angular_velocity.z
    # print(x,y,z)
    #print(imu.orientation.x, imu.orientation.y, imu.orientation.z, imu.orientation.w)
    pass

    NANO = 1 #/ (1000*1000*1000)
    global last_time, iter
    global x,y,z,rx,ry,rz,rw, speed_x, speed_y, speed_z 
    iter += 1
    
    time = rospy.Time.now().secs
    la = imu.linear_acceleration
    av = imu.angular_velocity

    if last_time is not None:
        dt = (time - last_time) * NANO

        #position += speed*deltaTime + 0.5*xfmAccelerometerReading*deltaTime*deltaTime
        speed_x += la.x*dt
        speed_y += la.y*dt
        speed_z += la.z*dt
        x += speed_x * dt
        y += speed_y * dt
        z += speed_z * dt
        rx += av.x*dt
        ry += av.y*dt
        rz += av.z*dt
        if iter%40 == 0:
            #print(x,y,z,rx,ry,rz,rw)
            #print(rx, ry, rz)
            #print(x, y, z)
            #print(la)
            quaternion = (
            imu.orientation.x,
            imu.orientation.y,
            imu.orientation.z,
            imu.orientation.w)
            euler = tf.transformations.euler_from_quaternion(quaternion)
            degrees = np.zeros(3)
            roll = (360 + ((euler[0] / 6.26) * 360)) % 360
            pitch = (360 + ((euler[1] / 6.26) * 360)) % 360
            yaw =  (360 + ((euler[2] / 6.26) * 360)) % 360

            print(roll, pitch, yaw)

    last_time = time
    




def listener():
    rospy.init_node('mpu_6050_test_subscriber', anonymous=True)
    #rospy.Subscriber('/imu/data_raw', Imu, imu_message_callback)
    rospy.Subscriber('/imu/data', Imu, imu_message_callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
