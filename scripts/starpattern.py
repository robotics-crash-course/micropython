from util.drivecontrol import Controller
from include.rcc_library import Raft
from sensors.vl53l0x import VL53L0X
from include.rcc_pins import Pins
from sensors.odom import Directional_Odom
import utime

myraft = Raft()
myraft.setup_i2c()
mylidar = VL53L0X(myraft.i2c_bus)

mycontroller = Controller()
mycontroller.start()

mycontroller.drive_forwards()
state = 1

while True:
    if state == 1:
        mycontroller.desired_theta -= 36
        utime.sleep_ms(8000)
        state = 2

    if state == 2:
        mycontroller.drive_forwards()
        utime.sleep_ms(4000)
        state = 1
