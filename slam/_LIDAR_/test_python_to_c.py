# ctypes_test.py
import ctypes
import pathlib
import time

if __name__ == "__main__":

    #L=Left, R=Right, F=Front, R=Rear
    #LF, RF, LR, RR

    # Load the shared library into ctypes
    libname = pathlib.Path().absolute() / "gil_motor_control_with_pwm.so"
    c_lib = ctypes.CDLL(libname)
    c_lib.runMotors(10,0,0,0)
    time.sleep(10)
    c_lib.runMotors(0,10,0,0)
    time.sleep(10)
    c_lib.runMotors(0,0,10,0)
    time.sleep(4)
    c_lib.runMotors(0,0,0,10)
    time.sleep(4)
    c_lib.runMotors(0,0,0,0)
    time.sleep(4)
