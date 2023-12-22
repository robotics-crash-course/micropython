from include.rcc_library import Pins, Raft
from util.drivecontrol import YawControl
from sensors.odom import Odom
import time

myraft = Raft()
myraft.led_on()
myraft.setup_button()

mycontroller = YawControl(0, 70)

myleftodom = Odom()
myleftodom.setup(Pins.LEFT_ODOM)
myrightodom = Odom()
myrightodom.setup(Pins.RIGHT_ODOM)

state = 0

while True:
    print(state, myleftodom.get_count(), mycontroller.theta, mycontroller.boost)

    if state == 0:
        if myraft.get_button():
            mycontroller.drive()
            state = 1
            myleftodom.reset_count()

    if state == 1:
        if myleftodom.get_count() >= 100:
            mycontroller.stop()
            state = 0


    