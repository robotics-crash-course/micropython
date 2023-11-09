from include.rcc_stdlib import Raft
from sensors.imu import MPU6050

i2c = Raft.setup_i2c()
imu = MPU6050(i2c)

while True:
    print(imu.gyro.z)
