import sys
import time        
        
maxFreq = 90
     
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
        
        if self.previous_error > 0 and error < 0:
            self.integral = 0
        elif self.previous_error < 0 and error > 0:
            self.integral = 0
        else:
            self.integral += error*dt
        self.derivative = (error - self.previous_error)/dt
        self.previous_error = error
        frequency = self.Kp*error + self.Ki*self.integral + self.Kd*self.derivative

        if frequency > maxFreq:
            return maxFreq
        elif frequency < (-1 * maxFreq):
            return -1 * maxFreq

            
        return frequency   

     
