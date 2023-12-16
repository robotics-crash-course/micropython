from include.rcc_library import Raft 
from sensors.mpu6050 import MPU6050
myraft = Raft()
myraft.setup_i2c()
myimu =  MPU6050(myraft.i2c_bus)

while True:
    print(myimu.get_accel_x())
    print(myimu.get_accel_y())
    print(myimu.get_accel_z())