import _thread
from machine import Timer
import utime

from include.rcc_library import Raft
from sensors.mpu6050 import MPU6050

#globals
theta = 0.0
theta_lock = _thread.allocate_lock() #lock object
omega = 0.0
omega_lock = _thread.allocate_lock()
# theta_queue = []

myraft = Raft()
myraft.setup_i2c()

myimu = MPU6050(myraft.i2c_bus)

# def update_theta(timer):
#     global theta
#     with theta_lock:
#         theta += myimu.get_angvel_z()*0.01
#         # theta_queue.append(theta)

# def theta_thread():
#     duration = 10
#     theta_timer = Timer(mode=Timer.PERIODIC, period=duration, callback=update_theta)

def theta_sleep_thread():
    # global theta
    # with theta_lock:
    #     theta += myimu.get_angvel_z()*0.01
    global omega
    # with omega_lock:
    omega = myimu.get_angvel_z()
    utime.sleep_ms(10)


second_thread = _thread.start_new_thread(theta_sleep_thread, ()) 

# while True:
#     # with theta_lock:
#     print(theta)
#     utime.sleep_ms(100)

while True:
    print(omega)