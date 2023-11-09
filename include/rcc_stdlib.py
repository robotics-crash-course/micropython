from machine import Pin, ADC, I2C
from include.rcc_pins import RCC_Pins

class Raft:
    @staticmethod
    def read_pot():
        return ADC(RCC_Pins.RCC_POT).read_u16()

    @staticmethod
    def read_button():
        return Pin(RCC_Pins.RCC_BUTTON, Pin.IN, Pin.PULL_UP).value()

    @staticmethod
    def setup_i2c():
        return I2C(1, sda=Pin(RCC_Pins.RCC_I2C_SDA), scl=Pin(RCC_Pins.RCC_I2C_SCL), freq=400000)


