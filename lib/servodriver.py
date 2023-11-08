from machine import Pin, PWM

class Servo:
    def __init__(self, pin_number):
        self.pin = pin_number
        self.pwm = PWM(Pin(self.pin))
        self.pwm.freq(50)

    def position(self, pos_scaled):
        """
        Takes in values 0-180, scales to left to right of servo
        """
        if (pos_scaled > 180):
            raise ValueError("Servo cannot go past 180 degrees")
        if (pos_scaled < 0):
            raise ValueError("Servo cannot go past 0 degrees")
        pos_raw = round(7500 - (pos_scaled*(7500-1200))/180)
        self.pwm.duty_u16(pos_raw)

# s1 = Servo(16)

# s1.position(90)

