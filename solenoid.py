
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT, initial = GPIO.LOW)


def open():
	GPIO.output(7, GPIO.HIGH)
def close():
	GPIO.output(7, GPIO.LOW)