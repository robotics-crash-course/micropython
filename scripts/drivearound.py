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
    # distance = mylidar.get_distance()
    # print(mycontroller.left_odom.count, state, mycontroller.theta, mycontroller.desired_theta, mycontroller.desired_velocity)
    if state == 1:
        mycontroller.drive_forwards()
        utime.sleep_ms(3000)
        state = 2

    if state == 2:
        mycontroller.u_turn()
        utime.sleep_ms(6000)
        state = 1
