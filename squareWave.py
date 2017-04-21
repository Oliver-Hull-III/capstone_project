import sys
import time
import thread
import RPi.GPIO as GPIO
from time import sleep

class squareWave:
    def __init__(self,isX):
        GPIO.setmode(GPIO.BOARD)
        self.square_pin = 40
        self.direction_pin = 37
        GPIO.setup(self.square_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)

    def run(self,frequency):
            
        if(frequency<0):
            GPIO.output(self.direction_pin, GPIO.LOW)
        else:
            GPIO.output(self.direction_pin, GPIO.HIGH)            

        frequency = abs(frequency)
        per = 1.0/frequency			#period is in seconds

        GPIO.output(self.square_pin, GPIO.HIGH)
        sleep(per/2)
        GPIO.output(self.square_pin, GPIO.LOW)
        sleep(per/2)
