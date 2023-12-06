from util.differentiator import Differentiator
from sensors.odom import Odom
from include.rcc_pins import Pins
from machine import Timer
from include.pwm_helper import Motors
from include.rcc_library import Raft
from util.pidcontrol import PID_Control

myraft = Raft()
myraft.setup_pot()

odom = Odom()
odom.setup(Pins.LEFT_ODOM)

vel = Differentiator(0.1, 0.02)
velcontroller = PID_Control(3, 0.1, 0, 0.02, 0.1, 0, 100, False, True)


velocity = 0
count = 0
controller_output = 0

def vel_callback(timer):
    global velocity, controller_output
    velocity = vel.differentiate(odom.get_count())

    scaled_pot = (myraft.get_pot()/65535)*150
    des_vel = int(scaled_pot)
    controller_output = velcontroller.pid(des_vel, velocity)
    mymotors.set_power(int(controller_output), 0)

    print(odom.get_count(), velocity, des_vel, controller_output)

veltimer = Timer(mode=Timer.PERIODIC, period=20, callback=vel_callback)

mymotors = Motors()
mymotors.setup()


while True:
    pass