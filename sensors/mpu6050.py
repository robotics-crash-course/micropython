from machine import I2C

def bytes_tosignedint(msb, lsb):
    value = (msb << 8) | lsb
    
    #check the sign
    if value & 0x8000:
        return value - 0x10000
    else:
        return value
        
class MPU6050():
    def __init__(self, i2c_bus):
        self.mpu_addr = 0x68 #104
        self.mpu_i2c = i2c_bus
        self.buf1 = bytearray(1) 
        self.buf14 = bytearray(14)
        self.ACCEL_SENSITIVITY = 16384.0
        self.GYRO_SENSITIVITY = 131.0

        self.ax_sum = 0
        self.ay_sum = 0
        self.az_sum = 0
        self.wx_sum = 0
        self.wy_sum = 0
        self.wz_sum = 0    

        self.begin_pico()
        self.calibrate()
        # print("IMU SETUP ON", i2c_bus)


    #writeto_mem(addr, reg, data)
    def begin_pico(self):
        #power management
        self.mpu_i2c.writeto_mem(self.mpu_addr, 0x6B, self.buf1)

        #gyro sensitivity
        self.mpu_i2c.writeto_mem(self.mpu_addr, 0x1B, self.buf1)

        #accel sensitivity
        self.mpu_i2c.writeto_mem(self.mpu_addr, 0x1C, self.buf1)

    #readfrom_mem_into(addr, memaddr, buf)
    def update_pico(self):
        try:
            """
            Read all data from the mpu6050 and store into class variables 
            (Note: These are the raw values, bias is applied in the get funcs)
            """
            self.mpu_i2c.readfrom_mem_into(self.mpu_addr, 0x3B, self.buf14)

            self.raw_ax = bytes_tosignedint(self.buf14[0], self.buf14[1])
            self.raw_ay = bytes_tosignedint(self.buf14[2], self.buf14[3])
            self.raw_az = bytes_tosignedint(self.buf14[4], self.buf14[5])
            self.raw_temp = bytes_tosignedint(self.buf14[6], self.buf14[7])
            self.raw_wx = bytes_tosignedint(self.buf14[8], self.buf14[9])
            self.raw_wy = bytes_tosignedint(self.buf14[10], self.buf14[11])
            self.raw_wz = bytes_tosignedint(self.buf14[12], self.buf14[13])
        except Exception as e:
            print(e)

    def calibrate(self):
        """
        Measure all values 100 times and calc average, push into bias values.
        """	
        self.n = 1000
        for i in range(self.n):
            self.update_pico()
            self.ax_sum += (self.raw_ax / self.ACCEL_SENSITIVITY) 
            self.ay_sum += (self.raw_ay / self.ACCEL_SENSITIVITY) 
            self.az_sum += (self.raw_az / self.ACCEL_SENSITIVITY) 
            self.wx_sum += (self.raw_wx / self.GYRO_SENSITIVITY)
            self.wy_sum += (self.raw_wy / self.GYRO_SENSITIVITY)
            self.wz_sum += (self.raw_wz / self.GYRO_SENSITIVITY)

        self.ax_bias = self.ax_sum / self.n
        self.ay_bias = self.ay_sum / self.n
        self.az_bias = self.az_sum / self.n
        self.wx_bias = self.wx_sum / self.n
        self.wy_bias = self.wy_sum / self.n
        self.wz_bias = self.wz_sum / self.n

    def get_accel_x(self):
        self.update_pico()
        return (self.raw_ax / self.ACCEL_SENSITIVITY) - self.ax_bias

    def get_accel_y(self):
        self.update_pico()
        return (self.raw_ay / self.ACCEL_SENSITIVITY) - self.ay_bias

    def get_accel_z(self):
        self.update_pico()
        return (self.raw_az / self.ACCEL_SENSITIVITY) - self.az_bias

    def get_angvel_x(self):
        self.update_pico()
        return (self.raw_wx / self.GYRO_SENSITIVITY) - self.wx_bias
    
    def get_angvel_y(self):
        self.update_pico()
        return (self.raw_wy / self.GYRO_SENSITIVITY) - self.wy_bias

    def get_angvel_z(self):
        self.update_pico()
        return (self.raw_wz / self.GYRO_SENSITIVITY) - self.wz_bias

    def get_temp(self):
        #todo: name these constants
        return (self.raw_temp / 340) + 36.53











