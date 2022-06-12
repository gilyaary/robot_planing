#import the library
from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep
from time import sleep
from orangepwm import *

#initialize the gpio module
gpio.init()

#setup the port (same as raspberry pi's gpio.setup() function)
#gpio.setcfg(port.PA6, gpio.OUTPUT)

#now we do something (light up the LED)
#gpio.output(port.PA6, gpio.HIGH)

#turn off the LED after 2 seconds
#sleep(2)
#gpio.output(port.PA6, gpio.LOW)

# Set GPIO pin PA6 as PWM output with a frequency of 100 Hz
#pwm = OrangePwm(100, port.PA6)
pwm0 = OrangePwm(100, port.PA0)
pwm1 = OrangePwm(100, port.PA1)

pwm2 = OrangePwm(100, port.PA2)
pwm3 = OrangePwm(100, port.PA3)
iter = 0

while iter < 10:

# Start PWM output with a duty cycle of 20%. The pulse (HIGH state) will have a duration of
# (1 / 100) * (20 / 100) = 0.002 seconds, followed by a low state with a duration of
# (1 / 100) * ((100 - 20) / 100) = 0.008 seconds.
# If a LED is plugged to with GPIO pin, it will shine at 20% of its capacity.
    pwm0.start(1)
    pwm1.start(1)
    pwm2.start(1)
    pwm3.start(1)
    sleep(2)


    pwm0.start(2)
    pwm1.start(2)
    pwm2.start(2)
    pwm3.start(2)
    sleep(2)

# Change the frequency of the PWM pattern. The pulse (HIGH state) will now have a duration of
# (1 / 10) * (6 / 100) = 0.006 seconds, followed by a low state with a duration of
# (1 / 10) * ((100 - 6) / 100) = 0.094 seconds.
# If a LED is plugged to with GPIO pin, it will shine at 6% of its capacity, but you may
# notice flickering.
#    pwm1.changeFrequency(10)
#    pwm0.changeFrequency(10)


#    pwm0.changeDutyCycle(40)
#    pwm1.changeDutyCycle(40)
#    pwm2.changeDutyCycle(40)
#    pwm3.changeDutyCycle(40)
#    sleep(2)

    iter += 1

# Stop PWM output
pwm0.stop()
pwm1.stop()
pwm2.stop()
pwm3.stop()
                                                                                                                                                                            1,1           Top

