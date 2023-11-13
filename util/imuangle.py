import utime

class Angle:
    def __init__(self, imu_input):
        self.imu = imu_input
        self.cur = utime.ticks_us()
        self.prev = utime.ticks_us()
        self.duration = 10000
        self.theta = 0
        self.state = 0

    def update(self):
        self.cur = utime.ticks_us()
        self.imu.update_pico()

        if self.state == 0:
            if (self.cur - self.prev) >= self.duration:
                self.state = 1

        if self.state == 1:
            self.theta += self.imu.getAngVelZ()*self.duration/1000000
            self.prev = self.cur
            self.state = 0

    def get_angle(self):
        return self.theta




    

