from machine import Pin, PWM
from include.rcc_pins import Pins

class Servo:
    def setup(self, servo_pin_input=Pins.SERVO):
        self.servo_pin = servo_pin_input
        self.pwm = PWM(Pin(self.servo_pin))
        self.pwm.freq(50)
        return f"SERVO SETUP ON {self.servo_pin}"

    def set_position(self, pos_scaled):
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
    def setup(self, ena_input=Pins.ENA, in1_input=Pins.IN1, in2_input=Pins.IN2, in3_input=Pins.IN3, in4_input=Pins.IN4, enb_input=Pins.ENB):
        self.ena_pin = ena_input
        self.in1_pin = in1_input
        self.in2_pin = in2_input
        self.in3_pin = in3_input
        self.in4_pin = in4_input
        self.enb_pin = enb_input
        
        #setup pwm
        self.pwm_a = PWM(Pin(self.ena_pin))
        self.pwm_a.freq(1000)
        self.pwm_b = PWM(Pin(self.enb_pin))
        self.pwm_b.freq(1000)
        #setup gpio
        self.in1 = Pin(self.in1_pin, Pin.OUT)
        self.in2 = Pin(self.in2_pin, Pin.OUT)
        self.in3 = Pin(self.in3_pin, Pin.OUT)
        self.in4 = Pin(self.in4_pin, Pin.OUT)

        return f"LEFT SETUP ON {self.ena_pin},{self.in1_pin},{self.in2_pin}, RIGHT SETUP ON {self.in3_pin},{self.in4_pin},{self.enb_pin}"

    def set_power(self, lp, rp):
        """
        takes in 0-100 -> scaled for 0-65500 (16 bit)
        """
        if (lp > 100 or rp > 100):
            raise ValueError("Motor power cannot go over 100")
        if (lp < -100 or rp < -100):
            raise ValueError("Motor power cannot go below -100")

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





    




