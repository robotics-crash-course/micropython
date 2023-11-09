from include.rcc_stdlib import Raft
from sensors.vl53l0x import VL53L0X

i2c = Raft.setup_i2c()

lidar = VL53L0X(i2c)

while True:
    print(lidar.get_reading(), "mm")