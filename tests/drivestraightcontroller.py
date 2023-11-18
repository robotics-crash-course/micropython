from include.rcc_stdlib import Raft
from include.pwm_helper import Motors
from sensors.mpu6050 import MPU6050
from util.pidcontrol import PID_Control
from util.imuangletimer import Angle
from machine import Timer
import utime


#setup i2c
i2c = Raft.setup_i2c()
#turn on led
# Raft.led_toggle()
#setup imu
imu = MPU6050(i2c)
imu.begin_pico()
imu.calibrate()
utime.sleep_ms(1000)

#setup angle to track imu
# angle = Angle(imu)
#setup motors
mymotors = Motors()

#setup driving straight variables
base_power = 50
desired_angle = 0
global theta
theta = 0
global boost_power
boost_power = 0


#setup controller
controller = PID_Control(0.5,0,0,0.02,0.1,-25,25, False, True)

# #calculate boost power
def calculate_controller(timer):
    global theta
    global boost_power
    imu.update_pico()
    theta += imu.getAngVelZ()*0.02
    boost_power = controller.pid(desired_angle, theta)
    # cur = utime.ticks_us()
    # print(cur)

# #calculate boost power on a timer
pid_timer = Timer(mode=Timer.PERIODIC, period=20, callback=calculate_controller)

while True:
    # print(boost_power)
    int_boost = int(boost_power)
    print(int_boost, theta)
    mymotors.MotorPower(base_power-int_boost, base_power+int_boost)








