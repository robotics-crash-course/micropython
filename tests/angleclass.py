from include.rcc_stdlib import Raft
from sensors.mpu6050 import MPU6050
from util.imuangle import Angle

i2c = Raft.setup_i2c()
imu = MPU6050(i2c)
imu.begin_pico()
imu.calibrate()

theta = Angle(imu)

while True:
    theta.update()
    print(theta.get_angle())

    
        

    