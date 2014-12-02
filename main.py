import RPi.GPIO as GPIO
import screen
import solenoid
import pricing
import flowmeter
import time
import requests
import sms




class Kegerator:

	def __init__ (self):
		#in reaility we will get these from the db
		self.price = 0
		self.type = ""
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
				#make request with token.
				#will get reply with users id
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
					self.price = self.beer1price
					self.type = self.beer1type
					state = 3
				elif beer == "\\":
					lcd.message("Dispensing %s" % self.beer2type)
					self.price = self.beer2price
					self.type = self.beer2type
					state = 3
				else:
					lcd.message("Invalid choice \n Try again")
					time.sleep(2)
			elif state == 3:
				solenoid.open()
				amount = flowmeter.flowing()
				solenoid.close()
				toCharge = pricing.calculate(self.beerprice, amount)
				#charge to stripe code goes here
				returnval = request.post()
				sms.send_recipt(phone, quantity, self.beer, toCharge)

				

#so i enter the card, it is tokenized, send all information for creating a customer, get individual customer id, hook that with the pin in my db, user enters pin and i can make a call to stripe with this user id. 






	


keg = Kegerator()#creates new keg object
lcd = screen.Adafruit_CharLCD() #creates new screen object

#initializes all gpio pins to make sure everything is working
keg.initialize()

#enter loop to wait for user to approach
keg.run()

