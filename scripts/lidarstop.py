from util.drivecontrol import Controller
from sensors.vl53l0x import VL53L0X

mycontroller = Controller()
mylidar = VL53L0X(mycontroller.raft.i2c_bus)

mycontroller.start()
mycontroller.drive_forwards()

while True:
    print(mylidar.get_distance())

    if mylidar.get_distance() <= 300:
        mycontroller.raft.led_on()
        mycontroller.stop()
