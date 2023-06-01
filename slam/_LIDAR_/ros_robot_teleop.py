from pynput import keyboard
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray
import time
import math

class Teleop:

    def __init__(self):
        self.motor_speed_pub = rospy.Publisher("motor_speed", Float64MultiArray, queue_size=10)
        rospy.init_node('ros_robot_teleop', anonymous=True)
        self.values = Float64MultiArray()
        self.values.data = [0,0]
        self.tps_1 = 0
        self.tps_2 = 0
        self.callnum = 0
        self.sum_sqr_error = 0
        self.error_sum_count = 0

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()  # start to listen on a separate thread
        #listener.join()  # remove if main thread is polling self.keys
        rospy.Subscriber("motor_ticks_per_second", Float64MultiArray, self.motor_tps_callback)
        rospy.spin()

    #this is a kind of "servo" feedback mechnism. We check the required tps vs the
    # actual tps from odometry and change the pwm value sent to the motors
    def motor_tps_callback(self, msg: Float64MultiArray):
            self.callnum += 1
            #print ('Message', msg)
            values = msg.data
            layout = msg.layout
            #from odom 
            tps_1, tps_2 = values[0], values[1]
            if self.tps_1 < 0:
                tps_1 *= -1
            if self.tps_2 < 0:
                tps_2 *= -1
            #print('ODOM TPS: ', tps_1, tps_2)
            
            if self.tps_1 != 0 and self.tps_2 != 0:
                diff_1, diff_2 = self.tps_1 - tps_1, self.tps_2 - tps_2
                
                self.sum_sqr_error += ( abs(diff_1) + abs(diff_2)) / 2
                self.error_sum_count += 1
                
                if self.callnum % 100 == 0:
                    #print('ODOM DIFF: ', diff_1, diff_2)
                    #print('Error Avg: ', self.sum_sqr_error / self.error_sum_count)
                    pass

                v_diff_1, v_diff_2 = diff_1, diff_2
                self.values.data[0] += v_diff_1 * 0.01
                self.values.data[1] += v_diff_2 * 0.01 
                #self.motor_speed_pub.publish(self.values)
            
    def get_value_from_tps(self):
        #value = (tps * 3 / 4)
        v1 = self.tps_1 / 2
        v2 = self.tps_2 / 2
        return [v1, v2]
                    
    def on_press(self, key):
        global r,l
        if key == keyboard.Key.esc:
            return False  # stop listener
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
        print('Key pressed: ' + k)
        #return False  # stop listener; remove this if want more keys
        
        if key.name == 'up':
            print('up')
            self.tps_1 = -40
            self.tps_2 = -40
            self.values.data = self.get_value_from_tps()
            self.motor_speed_pub.publish(self.values)
            # time.sleep(0.5)
            # self.tps_1 = -75
            # self.tps_2 = -75
            # self.values.data = self.get_value_from_tps()
            # self.motor_speed_pub.publish(self.values) 
        if key.name == 'down': 
            print('down')
            self.tps_1 = 20
            self.tps_2 = 20
            self.values.data = self.get_value_from_tps()
            self.motor_speed_pub.publish(self.values)
            # time.sleep(0.5)
            # self.tps_1 = 30
            # self.tps_2 = 30
            # self.values.data = self.get_value_from_tps()
            # self.motor_speed_pub.publish(self.values)
        
        
        if key.name == 'left':
            print('left')
            self.tps_1 = -20
            self.tps_2 = 20
            self.values.data = self.get_value_from_tps()
            self.motor_speed_pub.publish(self.values)
        if key.name == 'right':
            print('right')
            self.tps_1 = 20
            self.tps_2 = -20
            self.values.data = self.get_value_from_tps()
            self.motor_speed_pub.publish(self.values)
        
        
        if key.name == 'space':
            print('space')
            self.tps_1 = 0
            self.tps_2 = 0
            self.values.data = [0,0]
            self.motor_speed_pub.publish(self.values)


teleop = Teleop()