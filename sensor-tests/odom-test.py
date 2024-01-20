# SPDX-License-Identifier: GPL-3.0-or-later
# odom-test.py - testing functionality of directional encoders
# Copyright (C) 2023-2024 Jeannette Circe <jett@circe.com>

from include.rcc_pins import Pins
from sensors.odom import Directional_Odom
from include.pwm_helper import Motors

myleftodom = Directional_Odom()
myleftodom.setup(Pins.LEFT_DIR, Pins.LEFT_INT)

myrightodom = Directional_Odom()
myrightodom.setup(Pins.RIGHT_DIR, Pins.RIGHT_INT)

mymotors = Motors()
mymotors.setup()

mymotors.set_power(-50,-50)

while True:
    # print(myleftodom.int_pin.value(), myleftodom.dir_pin.value(), myrightodom.int_pin.value(), myrightodom.dir_pin.value())
    print(myleftodom.get_count(), myrightodom.get_count())