
import time
import RPi.GPIO as GPIO

class SolenoidValve():
	def __init__(self, pin):
		self._pin = pin
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin, GPIO.OUT, initial = GPIO.LOW)


	def open(self):
		GPIO.output(self._pin, GPIO.HIGH)
	def close(self):
		GPIO.output(self._pin, GPIO.LOW)