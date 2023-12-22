import _thread
from machine import Timer
from include.rcc_library import Raft
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
        #20 ms for loop
        self.controller = PID_Control(0.6, 0.01, 0, 0.02, 0.1, -self.boost_limit, self.boost_limit, False, True)

    def drive(self):
        self.stop_flag = False
        self.second_thread = _thread.start_new_thread(self.controller_thread, ())

    def stop(self):
        self.motors.set_power(0,0)
        self.stop_flag = True

    def update_gains(self, kp, ki, kd):
        self.controller.setGains(kp, ki, kd)      

    def update_base_power(self, bp):
        self.base_power = bp
        self.boost_limit = 100-self.base_power
        self.controller.setLimits(-self.boost_limit, self.boost_limit)  

    def update_desired_yaw(self, yaw_r):
        self.desired_yaw = yaw_r

    def update(self, timer):
        if self.stop_flag:
            _thread.exit()
        else:
            self.theta += self.imu.get_angvel_z()*0.02
            self.boost = int(self.controller.pid(self.desired_yaw, self.theta))
            self.motors.set_power(self.base_power-self.boost, self.base_power+self.boost)

    def controller_thread(self):
        timer = Timer(mode=Timer.PERIODIC, period=20, callback=self.update)





