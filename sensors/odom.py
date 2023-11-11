from machine import Pin
from include.rcc_pins import RCC_Pins

class Odom:
    def __init__(self, side):
        if side == "left":
            self.pin = Pin(RCC_Pins.RCC_LEFT_ENC, Pin.IN)
        elif side == "right":
            self.pin = Pin(RCC_Pins.RCC_RIGHT_ENC, Pin.IN)

        self.count = 0
        self.pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.callback)

    def callback(self, pin):
        self.count +=1

    def getCount(self):
        return self.count

    def setZero(self):
        count = 0


Left_Odom = Odom("left")
Right_Odom = Odom("right")

while True:
    print(Left_Odom.getCount(), Right_Odom.getCount())
