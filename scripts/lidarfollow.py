from util.drivecontrol import Controller
from sensors.vl53l0x import VL53L0X

mycontroller = Controller()
mylidar = VL53L0X(mycontroller.raft.i2c_bus)

mycontroller.start()
mycontroller.drive_forwards()

state = 1

while True:
    print(state)
    if state == 1:
        mycontroller.drive_forwards()
        mycontroller.raft.led_off()

        if mylidar.get_distance() <= 300:
            state = 2
    
    if state == 2:
        mycontroller.drive_backwards()
        mycontroller.raft.led_on()

        if mylidar.get_distance() >= 350:
            state = 1

