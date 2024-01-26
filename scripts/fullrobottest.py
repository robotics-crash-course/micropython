from include.rcc_library import Raft

myraft = Raft()
myraft.setup_button()
myraft.setup_button_counter()
myraft.setup_pot()

# while True:
#     print(myraft.get_button(), myraft.button_counter(), myraft.get_pot())

from include.pwm_helper import Motors

mymotors = Motors()
mymotors.setup()

mymotors.set_power(50,50)

from sensors.odom import Directional_Odom
from include.rcc_pins import Pins

myleftodom = Directional_Odom()
myleftodom.setup(Pins.LEFT_DIR, Pins.LEFT_INT)

myrightodom = Directional_Odom()
myrightodom.setup(Pins.RIGHT_DIR, Pins.RIGHT_INT)

while True:
    print(myleftodom.get_count(), myrightodom.get_count())

from sensors.mpu6050 import MPU6050
myraft.setup_i2c()
myimu = MPU6050(myraft.i2c_bus)

# while True:
#     print(myimu.get_angvel_z())