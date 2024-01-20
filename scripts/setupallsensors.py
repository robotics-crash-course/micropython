from include.rcc_pins import Pins
from include.rcc_library import Raft
from include.pwm_helper import Motors, Servo
from sensors.odom import Directional_Odom
from sensors.mpu6050 import MPU6050
from sensors.vl53l0x import VL53L0X

myraft = Raft() #make instance of raft

#setup raft peripherals
myraft.setup_button() 
myraft.setup_pot()
myraft.setup_i2c()

#motor controller
mymotors = Motors()
mymotors.setup()

#servo
myservo = Servo()
myservo.setup()

#odometry
myleftodom = Directional_Odom()
myleftodom.setup(Pins.LEFT_DIR, Pins.LEFT_INT)

myrightodom = Directional_Odom()
myrightodom.setup(Pins.RIGHT_DIR, Pins.RIGHT_INT)

#lidar
mylidar = VL53L0X(myraft.i2c_bus)

#imu
myimu = MPU6050(myraft.i2c_bus)
