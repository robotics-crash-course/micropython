from machine import Timer

class Angle:
    def __init__(self, imu_input):
        self.imu = imu_input
        self.theta = 0
        self.state = 0
        #period is ms
        self.timer = Timer(mode=Timer.PERIODIC, period=10, callback=self.update)

    def update(self, timer):
        self.imu.update_pico()
        self.theta += self.imu.getAngVelZ()*0.01

    def get_angle(self):
        return self.theta




    

