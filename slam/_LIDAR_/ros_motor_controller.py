
import rospy
#from sensor_msgs.msg import Joy
from std_msgs.msg import Float64
import sys
# ctypes_test.py
import ctypes
import pathlib
import time


class RosMotorController:
    def __init__(self):
        self.left = 0
        self.right = 0
        # Load the shared library into ctypes
        libname = pathlib.Path().absolute() / "gil_motor_control_with_pwm.so"
        self.c_pwm_motor_driver = ctypes.CDLL(libname)
    
        pass

    def subscribe(self):
        rospy.init_node('motor_listener', anonymous=True)
        rospy.Subscriber("right_motor", Float64, self.right_subscriber_callback)
        rospy.Subscriber("left_motor", Float64, self.left_subscriber_callback)
        rospy.spin()

    def right_subscriber_callback(self, data):
        print ('right', data)
        self.right = int(data.data)
        self.c_pwm_motor_driver.runMotors(self.left,self.right,self.left,self.right)
    

    def left_subscriber_callback(self, data):
        print ('left', data)
        self.left = int(data.data)
        self.c_pwm_motor_driver.runMotors(self.left,self.right,self.left,self.right)

motorController = RosMotorController()
motorController.subscribe()

    
