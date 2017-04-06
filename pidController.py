import sys
import time
import thread
import RPi.GPIO as GPIO
from time import sleep


frequencyGlobal = 0



class squareWave:
    def __init__(self,isX):
        GPIO.setmode(GPIO.BOARD)

        if(isX):
                square_pin = 40
        else:
                square_pin = 22
                
        GPIO.setup(square_pin, GPIO.OUT)

    def run(self):
        global frequencyGlobal
        if(frequencyGlobal == 0):
            return
        else:
            per = 1.0/frequencyGlobal			#period is in seconds
        while 1:
            GPIO.output(square_pin, GPIO.HIGH)
            sleep(per/2)
            GPIO.output(square_pin, GPIO.LOW)
            sleep(per/2)


def generateSignal(isX):
    sq = squareWave(isX)
    sq.run()
        
        
        
class pid:
    def __init__(self,Kp,Ki,Kd,isX):
        
        self.Kp = float(Kp)
        self.Ki = float(Ki) 
        self.Kd = float(Kd)
        
        self.previous_error = 0.0
        self.integral = 0.0
        self.derivative = 0.0

        self.prev_t = time.time()
        self.cur_t = 0.0
        
        thread.start_new_thread(generateSignal, (isX,))
        
        
    def update(self, error):
        global frequencyGlobal
        #calculate dt and update current time
        self.cur_t = time.time()
        dt = self.cur_t - self.prev_t
        self.prev_t = self.cur_t
        

        self.integral += error*dt
        self.derivative = (error - self.previous_error)/dt
        self.previous_error = error
        frequency = self.Kp*error + self.Ki*self.integral + self.Kd*self.derivative
        frequencyGlobal = frequency

        
        return frequency   

     
