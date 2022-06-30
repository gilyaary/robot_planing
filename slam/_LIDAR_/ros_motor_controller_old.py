
import rospy
#from sensor_msgs.msg import Joy
from std_msgs.msg import Float64
import sys
sys.path.insert(0, '/home/gil/code/python/orangepwm')
from motor_pwm_control import *


class RosMotorController:
    def __init__(self):
        # pubs
        #self._right_pub = rospy.Publisher('motor_right', Float64, queue_size=1)
        #self._left_pub = rospy.Publisher('motor_left', Float64, queue_size=1)
        self.motors = MotorPwmControl()
        self.left = 0
        self.right = 0
        pass

    def subscribe(self):
        # subs
        rospy.init_node('motor_listener', anonymous=True)
        rospy.Subscriber("right_motor", Float64, self.right_subscriber_callback)
        rospy.Subscriber("left_motor", Float64, self.left_subscriber_callback)
        rospy.spin()

    def right_subscriber_callback(self, data):
        print ('right', data)
        self.right = int(data.data)
        self.motors.set_speed(self.left, self.right)

    def left_subscriber_callback(self, data):
        print ('left', data)
        self.left = int(data.data)
        self.motors.set_speed(self.left, self.right)

motorController = RosMotorController()
motorController.subscribe()

    
