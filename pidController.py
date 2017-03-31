import sys
import time

class pid:
    def __init__(self,Kp,Ki,Kd):

        self.Kp = float(Kp)
        self.Ki = float(Ki) 
        self.Kd = float(Kd)
        
        self.previous_error = 0.0
        self.integral = 0.0
        self.derivative = 0.0

        self.prev_t = time.time()
        self.cur_t = 0.0

        
    def update(self, error):
        #calculate dt and update current time
        self.cur_t = time.time()
        dt = self.cur_t - self.prev_t
        self.prev_t = self.cur_t
        

        self.integral += error*dt
        self.derivative = (error - self.previous_error)/dt
        self.previous_error = error
        frequency = self.Kp*error + self.Ki*self.integral + self.Kd*self.derivative





        return frequency
    

     
