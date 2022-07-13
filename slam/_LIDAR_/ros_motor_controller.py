import rospy
from std_msgs.msg import Float64MultiArray
import ctypes
import pathlib

class RosMotorController:
    def __init__(self):
        self.left = int(0)
        self.right = int(0)
        # Load the shared library into ctypes
        libname = pathlib.Path().absolute() / "gil_motor_control_with_pwm.so"
        self.c_pwm_motor_driver = ctypes.CDLL(libname)

        pass

    def subscribe(self):
        rospy.init_node('motor_listener', anonymous=True)
        rospy.Subscriber("motor_speed", Float64MultiArray, self.motor_subscriber_callback)
        rospy.spin()


    def motor_subscriber_callback(self, msg: Float64MultiArray):
        print ('Message', msg)
        values = msg.data
        layout = msg.layout
    
        if values[0] < 0:
            self.right = int(values[0]) * -1
            self.right *= -1
        else:
            self.right = int(values[0])
        
        if values[1] < 0:
            self.left = int(values[1]) * -1
            self.left *= -1
        else:
            self.left = int(values[1])
        
        self.c_pwm_motor_driver.runMotors(self.left,self.right)


motorController = RosMotorController()
print('subscribing')
motorController.subscribe()