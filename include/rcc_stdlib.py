from machine import Pin, ADC, I2C
import include.rcc_pins 

class Raft:
    def __init__(self):
        self.pot_pin = RCC_POT
        self.button_pin = RCC_BUTTON
        self.sda_pin = RCC_I2C_SDA
        self.scl_pin = RCC_I2C_SCL

    def read_pot(self):
        return ADC(self.pot_pin).read_u16()

    def read_button(self):
        return Pin(self.button_pin, Pin.IN, Pin.PULL_UP).value()

    def setup_i2c(self):
        return I2C(1, sda=Pin(self.sda_pin), scl=Pin(self.scl_pin), freq=400000)
