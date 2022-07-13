import rospy
from std_msgs.msg import Float64MultiArray

from std_msgs.msg import Float64MultiArray
import pathlib
#sys.path.insert(0, '/home/gil/code/python/orangepi_PC_gpio_pyH3/')

from pyA20.gpio import gpio
from pyA20.gpio import connector
from pyA20.gpio import port
import time

odom1 = port.PA10
odom2 = port.PA13
gpio.init()
gpio.setcfg(odom1, gpio.INPUT)
gpio.pullup(odom1, gpio.PULLUP)
gpio.setcfg(odom2, gpio.INPUT)
gpio.pullup(odom2, gpio.PULLUP)

last_state_1 = 0
last_state_2 = 0
time_1  = time.time() #micro seconds
time_2 =  time.time() #micro seconds
ticks_per_sec_1 = 0
ticks_per_sec_2 = 0
#gpio.pullup(button, gpio.PULLDOWN)     # Optionally you can use pull-down resistor

try:
    print ("Press CTRL+C to exit")
    motor_odom_pub = rospy.Publisher("motor_ticks_per_second", Float64MultiArray, queue_size=10)
    rospy.init_node('motor_odom_pub', anonymous=True)

    while True:
        state_1 = gpio.input(odom1)
        if state_1 != last_state_1 and state_1 == 1:
            #print('odom_1: ', state_1)
            us  = time.time() - time_1
            ticks_per_sec_1 = 1 / us
            print('TPS-1', ticks_per_sec_1)
            values = Float64MultiArray()
            values.data = [ticks_per_sec_1,ticks_per_sec_2]
            motor_odom_pub.publish(values)
            time_1 = time.time()
        last_state_1 = state_1



        state_2 = gpio.input(odom2)
        if state_2 != last_state_2 and state_2 == 1:
            #print('odom2: ', state_2)
            us  = time.time() - time_2
            ticks_per_sec_2 = 1 / us
            print('TPS-2', ticks_per_sec_2)
            values = Float64MultiArray()
            values.data = [ticks_per_sec_1,ticks_per_sec_2]
            motor_odom_pub.publish(values)
            time_2 = time.time()
        last_state_2 = state_2



        time.sleep(0.0001)

except KeyboardInterrupt:
    print ("Goodbye.")
