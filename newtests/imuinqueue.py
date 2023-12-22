import _thread
import utime
from machine import Timer
from include.rcc_library import Raft
from sensors.mpu6050 import MPU6050

angvel_queue = []
theta_queue = []
theta = 0.0

myraft = Raft()
myraft.setup_i2c()
myimu = MPU6050(myraft.i2c_bus)


def update_theta(timer):
    global theta
    theta += myimu.get_angvel_z()*0.01
    theta_queue.append(theta)


def imu_thread():
    theta_timer = Timer(mode=Timer.PERIODIC, period=10, callback=update_theta)


second_thread = _thread.start_new_thread(imu_thread, ())

while True:
    # utime.sleep_ms(100)
    if theta_queue:
        most_recent = theta_queue.pop()
        print(most_recent)
    else:
        print("waiting")
