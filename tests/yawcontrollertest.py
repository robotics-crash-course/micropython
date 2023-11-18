from include.rcc_stdlib import Raft
from sensors.mpu6050 import MPU6050
from include.pwm_helper import Motors
from util.yawcontrol import YawController
import utime

Raft.led_toggle()
i2c = Raft.setup_i2c()

imu = MPU6050(i2c)
imu.begin_pico()
imu.calibrate()
utime.sleep(3)

mymotors = Motors()

myyawcontrol = YawController(mymotors, imu, 0, 75)
# myyawcontrol.start()

while True:
    myyawcontrol.drive()
    print(myyawcontrol.boost)
