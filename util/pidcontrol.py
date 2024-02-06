# SPDX-License-Identifier: GPL-3.0-or-later
# pidcontrol.py   Based on Introduction to Feedback Control using
#                 Design Studies by Randal W Beard, Timothy W.
#                 McLain, Cammy Peterson, & Marc Killpack
#                 ISBN-13: 978-1073396719
# Copyright (C) 2023-2024 Jeannette Circe <jett@circe.com>
class PID_Control:
    def __init__(self, kp=0.0, ki=0.0, kd=0.0, Ts = 0.02, sigma=0.05, lowerLimit=0, upperLimit=100, errorDotEnabled=False, antiWindupEnabled=False):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.Ts = Ts
        self.sigma = sigma
        self.beta = (2*self.sigma - self.Ts) / ((2*self.sigma) + self.Ts)
        self.lowerLimit = lowerLimit
        self.upperLimit = upperLimit
        self.errorDotEnabled = errorDotEnabled
        self.antiWindupEnabled = antiWindupEnabled
        self.deadband_voltage_lower = 0
        self.deadband_voltage_upper = 0
        self.integrator = 0
        self.error = 0
        self.error_dot = 0
        self.error_d1 = 0
        self.y_dot = 0
        self.y_d1 = 0

    def setGains(self, kp:float, ki:float, kd:float):
        """
        update gains of controller
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def setLimits(self, lower:float, upper:float):
        """
        set limits of controller output
        """
        self.upperLimit = upper
        self.lowerLimit = lower

    def setDeadbands(self, lower:float, upper:float):
        """
        set deadband of controller
        """
        self.deadband_voltage_lower = lower
        self.deadband_voltage_upper = upper

    def setTimeParameters(self, Ts:float, sigma:float):
        """
        set sample time and bandwidth of controller
        """
        self.Ts = Ts
        self.sigma = sigma
        self.beta = (2*self.sigma - self.Ts) / ((2*self.sigma) + self.Ts)

    def deadband_compensation(self, unsat:float):
        """
        shift the output linear scale such that small values are mapped to the deadband values
        but the max value is still mapped to the max value and in-between is linear
        """
        if (unsat > 0):
            return self.deadband_voltage_upper + ((unsat / self.upperLimit)*(self.upperLimit - self.deadband_voltage_upper))
        elif(unsat < 0):
            return self.deadband_voltage_lower + ((unsat / self.lowerLimit)*(self.lowerLimit - self.deadband_voltage_lower))
        else:
            return 0
        
    def saturate(self, unsat:float):
        """
        saturate value to upper/lower limits of the controller
        """
        return max( min(self.upperLimit, unsat), self.lowerLimit)
    
    def setpointReset(self, y_r:float, y:float):
        """
        reset PID controller, setting integrator to 0 and errors based on input args
        y_r is setpoint, used to calculate "previous" error
        y is the "actual" value want to reset the controller with
        """
        self.integrator = 0
        self.error_d1 = y_r - y
        self.error_dot = 0

    def pid(self, y_r:float, y:float) -> float:
        """
        calculate PID output given the reference and the actual signals at this time step
        this class keeps a history in the error_d1, y_d1 and the integrator variables
        y_r is the reference/setpoint/desired
        y is the actual value/system state
        returns controller output after pid, deadband compensation, and saturation
        """
        self.error = y_r - y

        #trapaziodal integration
        self.integrator += ((self.Ts / 2)*(self.error + self.error_d1))

        if (self.antiWindupEnabled and self.ki != 0):
            # generate an unsaturated signal from the integrator only
            # then saturate new integrator to the limit
            self.integrator = self.saturate(self.ki*self.integrator) / self.ki

        #pid control 
        if(self.errorDotEnabled):
            self.error_dot = (self.beta * self.error_dot) + (((1 - self.beta)/self.Ts)*(self.error - self.error_d1))
            self.u_unsat = (self.kp * self.error) + (self.ki* self.integrator) - (self.kd * self.error_dot)
        else:
            self.y_dot = (self.beta * self.y_dot) + (((1 - self.beta)/self.Ts)*(y-self.y_d1))
            self.u_unsat =  (self.kp * self.error) + (self.ki* self.integrator) - (self.kd * self.y_dot)

        self.error_d1 = self.error
        self.y_d1 = y

        return(self.deadband_compensation(self.saturate(self.u_unsat)))
