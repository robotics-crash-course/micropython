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
    

class Directional_Odom:
    def setup(self, dir_pin_input, int_pin_input):
        self.count = 0
        self.dir_pin = Pin(dir_pin_input)
        self.int_pin = Pin(int_pin_input)
        self.int_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.callback)

    def callback(self, pin):
        self.pin_1 = self.int_pin.value()
        self.pin_2 = self.dir_pin.value()

        if self.pin_1 ^ self.pin_2:
            self.count -= 1
        else:
            self.count += 1

    def get_count(self):
        return self.count
    
    def reset_count(self):
        self.count = 0
        return self.count
