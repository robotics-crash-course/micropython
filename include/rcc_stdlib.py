from machine import Pin, ADC, I2C
from include.rcc_pins import RCC_Pins
from utime import sleep

class Raft:
    @staticmethod
    def read_pot():
        return ADC(RCC_Pins.RCC_POT).read_u16()

    @staticmethod
    def read_button():
        return Pin(RCC_Pins.RCC_BUTTON, Pin.IN, Pin.PULL_UP).value()

    @staticmethod
    def setup_i2c():
        scl = Pin(RCC_Pins.RCC_I2C_SCL, Pin.OUT, Pin.PULL_UP)
        sda = Pin(RCC_Pins.RCC_I2C_SDA, Pin.OUT, Pin.PULL_UP)
        # Toggle SCL line 16 times to release potential devices waiting to receive/send data
        for i in range(16):
            scl.value(1)
            sleep(0.001)
            scl.value(0)
            sleep(0.001)
        # Generate stop condition (SCL HIGH, SDA RISING EDGE)
        sda.value(0)
        sleep(0.001)
        scl.value(1)
        sleep(0.001)
        sda.value(1)
        sleep(0.001)

        return I2C(1, sda=Pin(RCC_Pins.RCC_I2C_SDA), scl=Pin(RCC_Pins.RCC_I2C_SCL), freq=400000)


