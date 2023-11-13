from include.rcc_stdlib import Raft
from sensors.mpu6050 import MPU6050

i2c = Raft.setup_i2c()
imu = MPU6050(i2c)
imu.begin_pico()
imu.calibrate()


while True:
    imu.update_pico()
    print(imu.getAngVelZ())

