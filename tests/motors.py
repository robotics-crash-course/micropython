from include.rcc_stdlib import Raft
from include.pwm_helper import Motors

# Raft.led_toggle()

mymotors = Motors()

if __name__ == "__main__": 
    mymotors.MotorPower(100, 100)