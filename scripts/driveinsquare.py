from include.rcc_library import Pins, Raft
from util.drivecontrol import YawControl
from sensors.odom import Odom
import time

myraft = Raft()
myraft.led_on()
myraft.setup_button()

des_theta = 0

mycontroller = YawControl(des_theta, 70)

myleftodom = Odom()
myleftodom.setup(Pins.LEFT_ODOM)
myrightodom = Odom()
myrightodom.setup(Pins.RIGHT_ODOM)

state = 0

while True:
    print(myleftodom.get_count(), des_theta)

    if state == 0:
        if myraft.get_button():
            mycontroller.drive()
            state = 1

    if state == 1:
        if myleftodom.get_count() >= 200:
            des_theta += 90
            mycontroller.update_desired_yaw(des_theta)
            myleftodom.reset_count()
