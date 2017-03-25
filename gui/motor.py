import RPi.GPIO as GPIO
from time import sleep


step = 29
direction = 31
MS1 = 33
MS2 = 35
enable = 37


class Motor:
        def __init__(self):
                GPIO.cleanup()
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(step, GPIO.OUT)
                GPIO.setup(direction, GPIO.OUT)
                GPIO.setup(MS1, GPIO.OUT)
                GPIO.setup(MS2, GPIO.OUT)
                GPIO.setup(enable, GPIO.OUT)
                GPIO.output(enable, GPIO.LOW)
                GPIO.output(MS1, GPIO.LOW)
                GPIO.output(MS2, GPIO.LOW)
                
        def xForward():
                print("forward")
                GPIO.output(direction, GPIO.LOW)
                sleep(0.001)
                GPIO.output(step, GPIO.HIGH)
                sleep(0.001)
                GPIO.output(step, GPIO.LOW)
        	sleep(0.001)

        def cleanup():
                GPIO.output(enable, GPIO.HIGH)

                GPIO.cleanup()


