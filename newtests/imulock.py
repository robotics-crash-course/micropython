import _thread
from machine import Timer
from include.rcc_library import Raft
from sensors.mpu6050 import MPU6050
from util.pidcontrol import PID_Control


myraft = Raft()
myraft.setup_i2c()

myimu = MPU6050(myraft.i2c_bus)

theta_lock = _thread.allocate_lock()
boost_lock = _thread.allocate_lock()

theta = 0.0
boost = 0

mycontroller = PID_Control(0.5, 0, 0, 0.01, 0.05, -25, 25, False, True)

def update_theta(timer):
    global theta
    with theta_lock:
        theta += myimu.get_angvel_z()*0.01

def calc_pid(timer):
    global theta
    global boost
    with theta_lock:
        with boost_lock:
            boost = mycontroller.pid(des_yaw, theta)

def theta_thread():
    theta_timer = Timer(mode=Timer.PERIODIC, period = 10, callback=update_theta)
    pid_timer = Timer(mode=Timer.PERIODIC, period = 10, callback=calc_pid)

second_thread = _thread.start_new_thread(theta_thread, ())


while True:
    des_yaw = 90
    #make update des_yaw function a method of controller!
    print(theta, boost)
