
import time
import datetime
import RPi.GPIO as GPIO
import main
import pricing
import screen

class FlowmeterValve():

	def __init__(self, pin):
		self._pin = pin
		GPIO.setup(pin, GPIO.IN)


	def flowing(self):
		count = 0
		realtime = time.time()
		prevtime = time.time()

		while True:
			prevtest = GPIO.input(self._pin)
			time.sleep(.01)
			test = GPIO.input(self._pin)

			if (test == 0 and prevtest == 1) or (test == 1 and prevtest == 0):
				count += 1
				prevtime = time.time()
				realtime = time.time()
				if (count % 25) == 0:
					self.lcd.clear()
					ounces = pricing.amountOZ(count))
					self.lcd.message("%s ounces\ntot: $%s" % (ounces, pricing.calculate(44, ounces))

			else:
				realtime = time.time()

			tdelta = realtime - prevtime
			if tdelta > 2 and count > 1:
				break

		return count
