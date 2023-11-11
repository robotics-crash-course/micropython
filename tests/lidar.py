from include.rcc_stdlib import Raft
from sensors.vl53l0x import VL53L0X

i2c = Raft.setup_i2c()

lidar = VL53L0X(i2c)
# lidar.set=20000
# lidar.set_Vcsel_pulse_period(lidar.vcsel_period_type[0], 12)
# lidar.set_Vcsel_pulse_period(lidar.vcsel_period_type[1], 8)

while True:
    print(lidar.ping(), "mm")