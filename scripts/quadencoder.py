from sensors.odom import Directional_Odom
from include.rcc_library import Raft
from include.pwm_helper import Motors

mymotors = Motors()
mymotors.setup()
myraft = Raft()
myraft.led_on()

mymotors.set_power(100,100)

leftodom = Directional_Odom()
leftodom.setup(20,21)
rightodom = Directional_Odom()
rightodom.setup(18,19)

while True:
    print(rightodom.count)

