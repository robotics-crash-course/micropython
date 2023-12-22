from include.rcc_library import Pins, Raft
from util.drivecontrol import YawControl
from sensors.odom import Odom
from sensors.vl53l0x import VL53L0X
import _thread

import time

myraft = Raft()
myraft.led_on()
myraft.setup_button()
myraft.setup_i2c()

des_theta = 0

mycontroller = YawControl(des_theta, 70)

myleftodom = Odom()
myleftodom.setup(Pins.LEFT_ODOM)
myrightodom = Odom()
myrightodom.setup(Pins.RIGHT_ODOM)

mylidar = VL53L0X(myraft.i2c_bus)

state = 0
distance_travelled = 0

while True:
    print(mylidar.get_distance(), myleftodom.get_count())

    if state == 0:
        if myraft.get_button():
            mycontroller.drive()
            state = 1

    if state == 1:
        if mylidar.get_distance() <= 500:
            distance_travelled = myleftodom.get_count() + 70
            myleftodom.reset_count()
            state = 2

    if state == 2:
        mycontroller.update_desired_yaw(180)
        state = 2.5

    if state == 2.5:
        if mycontroller.boost <= 5:
            myleftodom.reset_count()
            state = 3

    if state == 3:
        if myleftodom.get_count() >= distance_travelled:
            mycontroller.stop()
            state = 4

    if state == 4:
        _thread.exit()
