from machine import Pin, ADC, I2C

class Raft:
    def __init__(self):
        self.pot_pin = 28
        self.button_pin = 22

    def read_pot(self):
        return ADC(self.pot_pin).read_u16()

    def read_button(self):
        return Pin(self.button_pin, Pin.IN, Pin.PULL_UP).value()

    def setup_i2c(self):
        return I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)


# myraft = raft()

# while True:
    # print(myraft.read_button(), myraft.read_pot())

