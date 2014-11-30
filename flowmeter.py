
import time
import datetime
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN)




def flowing(price):
	count = 0
	realtime = time.time()
	prevtime = time.time()

	while True:
		prevtest = GPIO.input(12)
		time.sleep(.01)
		test = GPIO.input(12)

		if (test == 0 and prevtest == 1) or (test == 1 and prevtest == 0):
			count += 1
			prevtime = time.time()
			realtime = time.time()
		else:
			realtime = time.time()

		tdelta = realtime - prevtime
		if tdelta > 2:
			break

	return count





flowing (1)
