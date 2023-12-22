from util.pidcontrol import PID_Control
from machine import Timer

class YawController:
    def __init__(self, motors_input, imu_input, desired_angle_input, base_power_input):
        self.motors = motors_input
        self.imu = imu_input
        self.base_power = base_power_input
        self.boost_limit = 100-self.base_power
        self.desired_angle = desired_angle_input
        self.theta = 0
        self.boost = 0
        self.int_boost = 0
        self.start()

    def start(self):
        self.controller = PID_Control(0.5,0,0,0.02,0.1,-self.boost_limit,self.boost_limit, False, True)
        self.timer = Timer(mode=Timer.PERIODIC, period=20, callback=self.update)

    def update(self, timer):
        # self.imu.update_pico()
        self.theta += self.imu.get_angvel_z()*0.02
        self.boost = self.controller.pid(self.desired_angle, self.theta)

    def drive(self):
        self.int_boost = int(self.boost)
        self.motors.set_power(self.base_power - self.int_boost, self.base_power+self.int_boost)

