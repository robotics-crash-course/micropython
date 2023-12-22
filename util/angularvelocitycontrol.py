from machine import Timer
from include.rcc_library import Raft
from sensors.mpu6050 import MPU6050
from util.pidcontrol import PID_Control
from include.pwm_helper import Motors

myraft = Raft()
myraft.setup_i2c()

imu = MPU6050(myraft.i2c_bus)

myraft.setup_pot()
motors = Motors()
motors.setup()

angvelcontroller = PID_Control(0.06, 0, 0, 0.02, 0.1, -100, 100, False, True)
angvelcontroller.setDeadbands(-35, 35)

theta = 0.0

def angvel_callback(timer):
    global theta
    des_theta = 180
    theta += imu.get_angvel_z()*0.02
    angvel_output = angvelcontroller.pid(des_theta, theta)
    angvelint = round(angvel_output)
    motors.set_power(-angvelint, angvelint)
    print(theta, angvelint)

angvel_timer = Timer(mode=Timer.PERIODIC, period=20, callback=angvel_callback)

while True:
    pass