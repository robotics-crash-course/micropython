# SPDX-License-Identifier: GPL-3.0-or-later
# drivecontrol.py - velocity & orientation control for RCC
# Copyright (C) 2023-2024  Jeannette Circe <jett@circe.com>
from machine import Timer
from include.rcc_pins import Pins
from include.rcc_library import Raft
from include.pwm_helper import Motors
from util.pidcontrol import PID_Control
from util.differentiator import Differentiator
from sensors.odom import Directional_Odom
from sensors.mpu6050 import MPU6050
import _thread
import utime

class Controller:
    def __init__(self):
        #hardware inits
        self.raft = Raft()
        self.raft.setup_i2c()
        self.motors = Motors()
        self.motors.setup()
        self.left_odom = Directional_Odom()
        self.left_odom.setup(Pins.LEFT_DIR, Pins.LEFT_INT)
        self.right_odom = Directional_Odom()
        self.right_odom.setup(Pins.RIGHT_DIR, Pins.RIGHT_INT)
        self.imu = MPU6050(self.raft.i2c_bus)
        #state init
        self.state = 0
        #variable inits
        self.theta = 0
        self.desired_theta = 0
        self.desired_velocity = 0
        self.left_controller_output = 0
        self.right_controller_output = 0
        #class inits
        self.left_differentiator = Differentiator(0.05, 0.02)
        self.right_differentiator = Differentiator(0.05, 0.02)
        self.left_velocity_control = PID_Control(0.3, 0.01, 0, 0.02, 0.1, -100, 100, False, True)
        self.right_velocity_control = PID_Control(0.3, 0.01, 0, 0.02, 0.1, -100, 100, False, True)
        self.orientation_control = PID_Control(7, 1, 0, 0.02, 0.1, -100, 100, False, True)


    def controller_callback(self, timer):
        '''
        sets motor speed based on desired linear velocity and desired orientation
            - integrates imu angular velocity reading to track theta
            - differentiates encoder count reading to get velocity of each wheel
            - saturates combination of controller outputs and sets motor power
        '''
        #calculate theta and velocities
        self.theta += self.imu.get_angvel_z()*0.02
        self.left_velocity = self.left_differentiator.differentiate(self.left_odom.count)
        self.right_velocity = self.right_differentiator.differentiate(self.right_odom.count)
        #calculate controller outputs
        self.left_controller_output = self.left_velocity_control.pid(self.desired_velocity, self.left_velocity)
        self.right_controller_output = self.right_velocity_control.pid(self.desired_velocity, self.right_velocity)
        self.orientation_controller_output = self.orientation_control.pid(self.desired_theta, self.theta)
        #checks if in a turning state
        if self.state == 0:
            #if not turning, use both vel and orientation controllers
            self.motors.set_power(self.saturate_motor_speed(self.left_controller_output-self.orientation_controller_output), self.saturate_motor_speed(self.right_controller_output+self.orientation_controller_output))
        elif self.state == 1:
            #if turning, use only orientation controller
            self.motors.set_power(self.saturate_motor_speed(-self.orientation_controller_output), self.saturate_motor_speed(self.orientation_controller_output))
            if abs(self.orientation_control.error) < 20:
                self.state = 0


    def saturate_motor_speed(self, unsat):
        '''
        saturates output from the controllers bc motor power takes integer -100 to 100
        '''
        return round(max(min(unsat, 100), -100))

    def drive_thread(self):
        '''
        timer so that controller calcs are done every 20 ms
        '''
        timer = Timer(mode=Timer.PERIODIC, period=20, callback=self.controller_callback)
    
    def start(self):
        '''
        starts control of motors based on odom and imu
        '''
        self.second_thread = _thread.start_new_thread(self.drive_thread, ())
    
    def set_speed(self, vel):
        '''
        changed desired speed of both wheels
        '''
        self.desired_velocity = vel

    def set_theta(self, des_theta):
        '''
        set desired orientation
        '''
        self.desired_theta = des_theta

    def stop(self):
        '''
        stop motors
        '''
        #minimize controller outputs
        self.desired_velocity = 0
        self.desired_theta = self.theta
        #stop pwm whine
        self.motors.set_power(0,0)

    def drive_forwards(self):
        '''
        sets desired velocity to 500
        '''
        self.desired_velocity = 550

    def drive_backwards(self):
        '''
        sets desired velocity to -500
        '''
        self.desired_velocity = -550

    def left_turn(self):
        '''
        sets desired velocity to 0, increases desired orientation by 90 deg
        '''
        self.state = 1
        self.desired_velocity = 0
        self.desired_theta += 90

    def right_turn(self):
        '''
        sets desired velocity to 0, decreases desired orientation by 90 deg
        '''
        self.state = 1
        self.desired_velocity = 0
        self.desired_theta -= 90

    def u_turn(self):
        '''
        sets desired velocity to 0, increases desired orientation by 190 deg
        '''
        self.state = 1
        self.desired_velocity = 0
        self.desired_theta += 180

