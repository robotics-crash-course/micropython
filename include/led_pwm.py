# SPDX-License-Identifier: GPL-3.0-or-later
# led_pwm.py - pwm-ing an LED
# Copyright (C) 2023-2024  Jeannette Circe <jett@circe.com>

from machine import Pin, PWM
class LED:
    def setup(self, pin):
        '''
        Sets PWM frequency (per second) to a GPIO Pin
        '''
        self.led_pin = PWM(Pin(pin)) 
        self.led_pin.freq(50) #not lower than 10

    def set_percent(self, percent):
        '''
        Sets PWM based on percentage input
        '''
        self.led_pin.duty_u16(percent*655)

myled = LED()
myled.setup(13)
