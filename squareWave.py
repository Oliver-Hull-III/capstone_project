import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
class squareWave:
        def __init__(self,isX):
                if(isX):
                        square_pin = 40
                else:
                        square_pin = 20
                        
                GPIO.setup(square_pin, GPIO.OUT)

        def update(freq):	#frequency is in Hertz
                per = 1.0/freq			#period is in seconds
                while 1:
                        GPIO.output(square_pin, GPIO.HIGH)
                	sleep(per/2)
                        GPIO.output(square_pin, GPIO.LOW)
                	sleep(per/2)
        



