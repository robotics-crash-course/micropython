from include.rcc_stdlib import Raft
from sensors.mpu6050 import MPU6050
import utime

i2c = Raft.setup_i2c()
imu = MPU6050(i2c)
imu.begin_pico()
imu.calibrate()

class State:
    DWELL = 0
    INTEGRATE = 1

state = State.DWELL
print(state)

cur =  utime.ticks_us()
prev = utime.ticks_us()
duration = 10000
theta = 0

while True:
    cur = utime.ticks_us()
    imu.update_pico()
    print(theta)


    if state == State.DWELL:
        if (cur - prev) >= duration:
            state = State.INTEGRATE
    
    if state == State.INTEGRATE:
        # print("math")
        theta += imu.getAngVelZ()*duration/1000000
        prev = cur
        state = 0
    