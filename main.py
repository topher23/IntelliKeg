import RPi.GPIO as GPIO
import screen
import solenoid
import pricing
import flowmeter
import time




class Kegerator:

	def __init__ (self):
		#in reaility we will get these from the db
		self.beer1price = 0.00571
		self.beer1type = "Alewerks"
		self.beer2price = 0.00450
		self.beer2type =  "Shock Top"


	#turn on gpio pins
	def initialize(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(12, GPIO.IN) #flowmeter
		GPIO.setup(7, GPIO.OUT, initial = GPIO.LOW) #solenoid
		
	def run():
		while True:
			state = 1
			beertype = True
			if state == 1:
				lcd.message("Awaiting user\n credentials")
				ident = raw_input()
				#name = getnamefromdb
				#if name is in database with credentials
				#	lcd.message("User Validated\nWelcome %s " % (name))
				#	time.sleep(3)
				#	state = 2
				#else:
				#	lcd.message("incorrect pin\n try again.")
			elif state == 2:
				lcd.message("Choose Beer. \n\ =left, * =right")
				beer = raw_input()
				if beer == "*":
					lcd.message("Dispensing %s" % self.beer1type)
					state = 3
				elif beer == "\\":
					lcd.message("Dispensing %s" % self.beer2type)
					beertype = False
					state = 3
				else:
					lcd.message("Invalid choice \n Try again")
					time.sleep(2)
			elif state == 3:
				solenoid.open()
				amount = flowmeter.flowing()
				solenoid.close()
				if beertype:
					toCharge = pricing.calculate(beer1price, amount)
				else
					toCharge = pricing.calculate(beer2price, amount)
				#charge to stripe code goes here







	


keg = Kegerator()#creates new keg object
lcd = screen.Adafruit_CharLCD() #creates new screen object

#initializes all gpio pins to make sure everything is working
keg.initialize()

#enter loop to wait for user to approach
keg.run()

