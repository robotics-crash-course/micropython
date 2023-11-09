from machine import Pin, PWM
import include.rcc_pins 
import include.rcc_stdlib

class Servo:
    def __init__(self):
        self.pin = RCC_SERVO
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

class Motors:
    def __init__(self):
        self.ena = RCC_ENA
        self.enb = RCC_ENB
        self.in1_pin = RCC_IN1
        self.in2_pin = RCC_IN2
        self.in3_pin = RCC_IN3
        self.in4_pin = RCC_IN4
        #setup pwm
        self.pwm_a = PWM(Pin(self.ena))
        self.pwm_a.freq(1000)
        self.pwm_b = PWM(Pin(self.enb))
        self.pwm_b.freq(1000)
        #setup gpio
        self.in1 = Pin(self.in1_pin, Pin.OUT)
        self.in2 = Pin(self.in2_pin, Pin.OUT)
        self.in3 = Pin(self.in3_pin, Pin.OUT)
        self.in4 = Pin(self.in4_pin, Pin.OUT)

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





    




