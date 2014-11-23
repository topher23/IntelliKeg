
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
count = 0
GPIO.setup(12, GPIO.IN)


while True:
	prevtest = GPIO.input(12)
	time.sleep(.01)
	test = GPIO.input(12)

	if test == 0 and prevtest == 1:
		count += 1
	elif test == 1 and prevtest == 0:
		count += 1
	
	print prevtest
	print test
	print count
#	time.sleep(.1)
