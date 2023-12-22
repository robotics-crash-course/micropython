from include.rcc_pins import Pins
from include.rcc_library import Raft
from include.pwm_helper import Motors
from sensors.odom import Directional_Odom
from sensors.mpu6050 import MPU6050
from util.differentiator import Differentiator
from util.pidcontrol import PID_Control
from machine import Timer
import time

class DriveControl():
    def __init__(self, desired_velocity, desired_theta):
        self.desired_velocity = desired_velocity
        self.desired_theta = desired_theta
        self.theta = 0.0
        self.raft = Raft()
        # self.raft.setup_i2c()
        # self.imu = MPU6050(self.raft.i2c_bus)
        self.motors = Motors()
        self.motors.setup()
        self.left_odom = Directional_Odom()
        self.left_odom.setup(20, 21)
        self.right_odom = Directional_Odom()
        self.right_odom.setup(18,19)
        self.left_controller_output = 0
        self.right_controller_output = 0
        self.differentiator = Differentiator(0.1, 0.02)
        self.velocity_control = PID_Control(4, 0.5, 0, 0.02, 0.1, 0, 60, False, True)
        self.velocity_control.setDeadbands(0, 35)
        # self.angularvelocity_control = PID_Control(3, 0, 0, 0.02, 0.1, -40, 40, False, True)
        # self.angularvelocity_control.setDeadbands(-35, 35)

    def velocity_callback(self, timer):
        # self.theta += self.imu.get_angvel_z()*0.02
        # self.angvel_output = self.angularvelocity_control.pid(self.desired_theta, self.theta)
        self.left_velocity = self.differentiator.differentiate(self.left_odom.get_count())
        self.right_velocity = self.differentiator.differentiate(self.right_odom.get_count())
        self.left_controller_output = round(self.velocity_control.pid(self.desired_velocity, self.left_velocity))
        self.right_controller_output = round(self.velocity_control.pid(self.desired_velocity, self.right_velocity))
        # self.motors.set_power(round(self.left_controller_output-self.angvel_output), round(self.right_controller_output+self.angvel_output))
        self.motors.set_power(round(self.left_controller_output), round(self.right_controller_output))
        print(time.ticks_ms())

    def start(self):
        timer = Timer(mode=Timer.PERIODIC, period=20, callback=self.velocity_callback)
        self.raft.led_on()


mycontroller = DriveControl(3200, 0)
mycontroller.start()

while True:
    pass

