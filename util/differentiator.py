# SPDX-License-Identifier: GPL-3.0-or-later
# differentiator.py - Differentiates a value
# Copyright (C) 2023-2024 Jeannette Circe <jett@circe.com>
class Differentiator():
    def __init__(self, sigma:float, ts:float):
        self.sigma = sigma
        self.ts = ts
       
        self.beta = (2*sigma - ts) / (2*sigma + ts)
        self.y_dot = 0
        self.y_d1 = 0

    def differentiate(self, y:float)->float:
        """
        y is incoming sample to use for differentiation
        returns band limited derivative at this sample
        """
        #calculate derivative
        self.y_dot = (self.beta * self.y_dot) + (((1 - self.beta) / self.ts)* (y - self.y_d1))

        self.y_d1 = y

        return self.y_dot
    
    def reset(self, degrees:float):
        """
        degrees is the value we want the "previous sample" to have after the reset
        """
        self.y_dot = 0
        self.y_d1 = degrees

    def setTimeParameters(self, ts:float, sigma:float):
        """
        ts is sample time
        sigma is bandwidth of low pass filter applied (1/cutoff-freq)
        """
        self.ts = ts
        self.sigma  = sigma
        self.beta = (2*sigma - ts) / (2*sigma + ts)





 