import _thread
from machine import Timer
from include.rcc_library import Raft
import sensors.mpu6050
from sensors.mpu6050 import MPU6050
from util.pidcontrol import PID_Control
from include.pwm_helper import Motors
import utime

class YawControl():
    def __init__(self, yaw_r=0, bp=70):
        self.desired_yaw = yaw_r
        self.desired_omega = yaw_r
        self.raft = Raft()
        self.raft.setup_i2c()
        self.imu = MPU6050(self.raft.i2c_bus)
        self.motors = Motors()
        self.motors.setup()
        self.base_power = bp
        self.boost_limit = 100-self.base_power
        self.theta = 0.0
        self.boost = 0
        self.stop_flag = False
        # self.theta_lock = _thread.allocate_lock()
        # self.boost_lock = _thread.allocate_lock()
        self.controller = PID_Control(0.5, 0, 0, 0.01, 0.1, -self.boost_limit, self.boost_limit, False, True)
        # self.second_thread = _thread.start_new_thread(self.controller_thread, ())
        # self.second_thread = _thread.start_new_thread(self.omega_controller_thread, ())

    def drive(self):
        self.stop_flag = False
        self.second_thread = _thread.start_new_thread(self.omega_controller_thread, ())

    def stop(self):
        # self.update_base_power(0)
        # self.motors.set_power(0,0)
        # self.second_thread = _thread.exit()
        self.stop_flag = True

    def update_gains(self, kp, ki, kd):
        self.controller.setGains(kp, ki, kd)      

    def update_base_power(self, bp):
        self.base_power = bp
        self.boost_limit = 100-self.base_power
        self.controller.setLimits(-self.boost_limit, self.boost_limit)  

    def update_desired_yaw(self, yaw_r):
        self.desired_yaw = yaw_r

    def update_omega(self, timer):
        self.boost = int(self.controller.pid(self.desired_omega, self.imu.get_angvel_z()))
        if self.stop_flag:
            self.motors.set_power(0,0)
        else:
            self.motors.set_power(self.base_power-self.boost, self.base_power+self.boost)

    def omega_controller_thread(self):
        timer = Timer(mode=Timer.PERIODIC, period=10, callback=self.update_omega)

    # def update(self, timer):
    #     # with self.theta_lock:
    #     #     with self.boost_lock:
    #     self.theta += self.imu.get_angvel_z()*0.01
    #     self.boost = int(self.controller.pid(self.desired_yaw, self.theta))
    #     self.motors.set_power(self.base_power-self.boost, self.base_power+self.boost)

    # def controller_thread(self):
    #     timer = Timer(mode=Timer.PERIODIC, period=10, callback=self.update)





