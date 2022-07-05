from pynput import keyboard
import rospy
from std_msgs.msg import Float64


r = rospy.Publisher("right_motor", Float64, queue_size=1)
l = rospy.Publisher("left_motor", Float64, queue_size=1)
rospy.init_node('ros_robot_teleop', anonymous=True)

def on_press(key):
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
        r.publish(Float64(25))
        l.publish(Float64(25))
    if key.name == 'down': 
        print('down')
    if key.name == 'left':
        print('left')
        r.publish(Float64(0))
        l.publish(Float64(25))
    if key.name == 'right':
        print('right')
        r.publish(Float64(25))
        l.publish(Float64(0))
    if key.name == 'space':
        print('space')
        r.publish(Float64(0))
        l.publish(Float64(0))
        r.publish(Float64(0))
        l.publish(Float64(0))

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
listener.join()  # remove if main thread is polling self.keys