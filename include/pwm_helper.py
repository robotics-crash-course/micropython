from machine import Pin, PWM
from include.rcc_pins import RCC_Pins

class Servo:
    def __init__(self):
        self.pwm = PWM(Pin(RCC_Pins.RCC_SERVO))
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

class Motors:
    def __init__(self):
        #setup pwm
        self.pwm_a = PWM(Pin(RCC_Pins.RCC_ENA))
        self.pwm_a.freq(1000)
        self.pwm_b = PWM(Pin(RCC_Pins.RCC_ENB))
        self.pwm_b.freq(1000)
        #setup gpio
        self.in1 = Pin(RCC_Pins.RCC_IN1, Pin.OUT)
        self.in2 = Pin(RCC_Pins.RCC_IN2, Pin.OUT)
        self.in3 = Pin(RCC_Pins.RCC_IN3, Pin.OUT)
        self.in4 = Pin(RCC_Pins.RCC_IN4, Pin.OUT)

    def MotorPower(self, lp, rp):
        """
        takes in 0-100 -> scaled for 0-65500 (16 bit)
        """
        if (lp > 100 or rp > 100):
            raise ValueError("Motor Power cannot go over 100")
        if (lp < -100 or rp < -100):
            raise ValueError("Motor Power cannot go below -100")

        #handle directionality
        if(lp < 0):
            self.in1.value(0)
            self.in2.value(1)
        else:
            self.in1.value(1)
            self.in2.value(0)
        
        if(rp < 0):
            self.in3.value(0)
            self.in4.value(1)
        else:
            self.in3.value(1)
            self.in4.value(0)

        self.pwm_a.duty_u16(abs(lp*655))
        self.pwm_b.duty_u16(abs(rp*655))





    




