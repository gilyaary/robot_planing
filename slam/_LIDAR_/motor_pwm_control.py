from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep
from time import sleep
from orangepwm import *

class MotorPwmControl:
    def __init__ (self):
        gpio.init()
        self.pwm0 = OrangePwm(100, port.PA0)
        self.pwm1 = OrangePwm(100, port.PA1)
        self.pwm2 = OrangePwm(100, port.PA2)
        self.pwm3 = OrangePwm(100, port.PA3)
    
    def stop (self):
        self.pwm0.stop()
        self.pwm1.stop()
        self.pwm2.stop()
        self.pwm3.stop()
    
    def set_speed (left, right)                                                                                                                                                                        1,1           Top
        self.pwm0.start(left)
        self.pwm1.start(right)
        self.pwm2.start(left)
        self.pwm3.start(right)
