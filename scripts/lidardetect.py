from include.rcc_library import Raft
from include.pwm_helper import Servo
from sensors.vl53l0x import VL53L0X

myraft = Raft()
myraft.setup_i2c()

myservo = Servo()
myservo.setup()

mylidar = VL53L0X(myraft.i2c_bus)


distances = []
changes = []
loc_of_interest = []

for i in range(180):
    myservo.set_position(i)
    distances.append(mylidar.get_distance())

for i in range(1, 179):
    changes.append(distances[i] - distances[i-1])
    if changes[i-1] > 7000:
        loc_of_interest.append(i)