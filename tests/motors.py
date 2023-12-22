from include.rcc_library import Raft
from include.pwm_helper import Motors

# Raft.led_toggle()

mymotors = Motors()
mymotors.setup()
myraft = Raft()
myraft.led_on()

while True:
    mymotors.set_power(100,100)