from machine import Pin

class Odom:
    def setup(self, pin_input):
        self.pin = Pin(pin_input, Pin.IN)
        self.count = 0
        self.pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.callback)
        return f"ODOM SETUP ON {pin_input}"

    def callback(self, pin):
        self.count +=1

    def get_count(self):
        return self.count

    def reset_count(self):
        self.count = 0
        return self.count