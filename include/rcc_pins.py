class Pins:
    def __init__(self):
        #l289n
        self.RCC_ENA = 7
        self.RCC_IN1 = 8
        self.RCC_IN2 = 9
        self.RCC_IN3 = 10
        self.RCC_IN4 = 11
        self.RCC_ENB = 12
        #i2c1 bus 
        self.RCC_I2C_SDA = 14
        self.RCC_I2C_SCL = 15
        # Servo
        self.RCC_SERVO = 16
        # Raft Interfaces
        self.RCC_POT = 28
        self.RCC_BUTTON = 22
        # Optical Interrupt Sensors for Odom
        self.RCC_LEFT_ENC = 21
        self.RCC_RIGHT_ENC = 13