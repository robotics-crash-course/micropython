# SPDX-License-Identifier: GPL-3.0-or-later
# drivecontrol.py - velocity & orientation control for RCC
# Copyright (C) 2023-2024  Jeannette Circe <jett@circe.com>


from util.differentiator import Differentiator
from sensors.odom import Directional_Odom
from include.rcc_pins import Pins
from machine import Timer
from include.pwm_helper import Motors
from include.rcc_library import Raft
from util.pidcontrol import PID_Control
from sensors.mpu6050 import MPU6050
import time
import _thread



class Controller:
    def __init__(self,vel=0):
        self.desired_velocity = vel
        self.raft = Raft()
        self.raft.setup_i2c()
        self.motors = Motors()
        self.motors.setup()
        self.left_odom = Directional_Odom()
        self.left_odom.setup(Pins.LEFT_DIR, Pins.LEFT_INT)
        self.right_odom = Directional_Odom()
        self.right_odom.setup(Pins.RIGHT_DIR, Pins.RIGHT_INT)
        self.imu = MPU6050(self.raft.i2c_bus)
        self.theta = 0
        self.desired_theta = 0
        self.base_power = 0
        self.left_controller_output = 0
        self.right_controller_output = 0
        self.left_differentiator = Differentiator(0.05, 0.02)
        self.right_differentiator = Differentiator(0.05, 0.02)
        self.left_velocity_control = PID_Control(0.3, 0, 0, 0.02, 0.1, -100, 100, False, True)
        self.right_velocity_control = PID_Control(0.3, 0, 0, 0.02, 0.1, -100, 100, False, True)
        self.orientation_control = PID_Control(5, 0, 0, 0.02, 0.05, -100, 100, False, True)

    def vel_callback(self, timer):
        self.theta += self.imu.get_angvel_z()*0.02
        self.left_velocity = self.left_differentiator.differentiate(self.left_odom.count)
        self.right_velocity = self.right_differentiator.differentiate(self.right_odom.count)
        self.left_controller_output = round(self.left_velocity_control.pid(self.desired_velocity, self.left_velocity))
        self.right_controller_output = round(self.right_velocity_control.pid(self.desired_velocity, self.right_velocity))
        self.orientation_controller_output = round(self.orientation_control.pid(self.desired_theta, self.theta))
        self.motors.set_power(self.saturate_motor_speed(self.base_power+self.left_controller_output-self.orientation_controller_output), self.saturate_motor_speed(self.base_power+self.right_controller_output+self.orientation_controller_output))
        # print(self.desired_velocity, self.left_odom.count, self.right_odom.count, self.left_velocity, self.right_velocity, self.left_controller_output, self.right_controller_output)
        # print(self.left_odom.count, self.right_odom.count, self.left_velocity, self.right_velocity)
        # print(self.desired_velocity, self.left_velocity, self.right_velocity, self.left_controller_output, self.right_controller_output)
        print(self.desired_theta, self.theta, self.orientation_controller_output)

    def saturate_motor_speed(self, unsat):
        return max(min(unsat, 100), -100)

    def drive_thread(self):
        timer = Timer(mode=Timer.PERIODIC, period=20, callback=self.vel_callback)
    
    def drive(self):
        self.second_thread = _thread.start_new_thread(self.drive_thread, ())
    
    def set_speed(self, vel):
        self.desired_velocity = vel

    def set_theta(self, des_theta):
        self.desired_theta = des_theta


mycontroller = Controller()
mycontroller.drive()

while True:
    mycontroller.set_speed(400)
    print("forwards")
    time.sleep_ms(3000)
    mycontroller.set_speed(0)
    mycontroller.set_theta(90)
    print("left turn")
    time.sleep_ms(2000)
    mycontroller.set_speed(-400)
    print("backwards")
    time.sleep_ms(3000)
    # mycontroller.set_speed(0)
        
    


      





