from util.differentiator import Differentiator
from sensors.odom import Odom
from include.rcc_pins import Pins
from machine import Timer
from include.pwm_helper import Motors
from include.rcc_library import Raft

myraft = Raft()
myraft.setup_pot()

odom = Odom()
odom.setup(Pins.LEFT_ODOM)

vel = Differentiator(0.1, 0.02)

velocity = 0
count = 0

def vel_callback(timer):
    global velocity
    velocity = vel.differentiate(odom.get_count())
    print(odom.get_count(), velocity)

veltimer = Timer(mode=Timer.PERIODIC, period=20, callback=vel_callback)

mymotors = Motors()
mymotors.setup()

while True:
    scaled_power = (myraft.get_pot()/65535)*100
    mymotors.set_power(int(scaled_power), 0)