from include.rcc_library import Raft
from sensors.vl53l0x import VL53L0X

myraft = Raft()
myraft.setup_i2c()

mylidar = VL53L0X(myraft.i2c_bus)

while True:
    print(mylidar.get_distance())