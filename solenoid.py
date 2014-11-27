
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT, initial = GPIO.LOW)
time.sleep(3)
print "attempting to switch"
GPIO.output(7, GPIO.HIGH)
time.sleep(3)

