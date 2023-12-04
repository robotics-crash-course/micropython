from machine import Pin, ADC, I2C
from include.rcc_pins import Pins
from utime import sleep

class Raft:
    def __init__(self):
        self.led = Pin("LED", Pin.OUT)
        self.button_pressed = False

    def led_toggle(self):
        self.led.toggle()

        if (self.led.value()):
            return "LED ON"
        else:
            return "LED OFF"

    def led_on(self):
        self.led.value(1)
        return "LED ON"

    def led_off(self):
        self.led.value(0)
        return "LED OFF"

    def setup_button(self, button_pin_input=Pins.BUTTON):
        self.button_pin = button_pin_input
        self.button = Pin(self.button_pin, Pin.IN, Pin.PULL_UP)
        self.button_pressed = False
        self.button.irq(trigger=Pin.IRQ_FALLING, handler=self.button_callback)
        # print("BUTTON SETUP ON ", self.button_pin)
    
    def button_callback(self, pin):
        self.button_pressed = True

    def get_button(self):
        if self.button_pressed:
            self.button_pressed = False #reset button flag
            return True
        else:
            return False

    def setup_pot(self, pot_pin_input=Pins.POT):
        self.pot_pin = pot_pin_input
        self.pot = ADC(self.pot_pin)
        return f"POT SETUP ON {self.pot_pin}" 

    def get_pot(self):
        return self.pot.read_u16()

    def setup_i2c(self, bus_input=Pins.I2C_BUS, scl_input=Pins.I2C_SCL, sda_input=Pins.I2C_SDA):
        self.bus = bus_input
        self.scl_pin = scl_input
        self.sda_pin = sda_input

        self.scl = Pin(self.scl_pin, Pin.OUT, Pin.PULL_UP)
        self.sda = Pin(self.sda_pin, Pin.OUT, Pin.PULL_UP)
        # Toggle SCL line 16 times to release potential devices waiting to receive/send data
        for i in range(16):
            self.scl.value(1)
            sleep(0.001)
            self.scl.value(0)
            sleep(0.001)
        # Generate stop condition (SCL HIGH, SDA RISING EDGE)
        self.sda.value(0)
        sleep(0.001)
        self.scl.value(1)
        sleep(0.001)
        self.sda.value(1)
        sleep(0.001)

        self.i2c_bus = I2C(self.bus, sda=Pin(self.sda_pin), scl=Pin(self.scl_pin), freq=100000)
        return f"I2C{self.bus} SETUP ON SCL={self.scl_pin} AND SDA={self.sda_pin}" 

    



