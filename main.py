import RPi.GPIO as GPIO
import screen
import solenoid
import pricing
import flowmeter
import time
import requests
import sms
import json




class Kegerator:

	def __init__ (self, solenoid, flowmeter):
		#in reaility we will get these from the db
		self.beer1price = 0.00571
		self.beer1type = "Alewerks"
		self.beer2price = 0.00450
		self.beer2type =  "Shock Top"
		self.apikey = "intellikeg123"
		self.solenoid = solenoid
		self.flowmeter = flowmeter


	#turn on gpio pins
	def initialize(self):
		GPIO.setmode(GPIO.BOARD)
		
	def pinChecking(pin):
		data = {"apikey":self.apikey, "userid":ident}
		IDandPHONE = requests.post("shaped-pride-770.appspot.com/account/user", params=data)
		if IDandPHONE == 0:
			return False
		else:
			return IDandPHONE.json()


	def beerSelection(beer):
		if beer == "*":
			return {"price": self.beer1price, "type": self.beer1type, "amount":0}
		elif beer == "\\":
			return {"price": self.beer2price, "type": self.beer2type, "amount":0}
		else:
			return False

	def run(self):
		attempts = 0
		while True:
			beertype = True
			beer = False

			
			#pin checking
			lcd.message("Please enter your pin.")
			user = False
			while not user:
				user = pinChecking(raw_input())
				if not user:
					lcd.message("pin incorrect. try again.")
			lcd.message("User validate. Welcome.")
			time.sleep(2)

			
			#beer selection
			lcd.message("Choose Beer. \n\ =left, * =right")
			while not beer:
				beer = beerSelection(raw_input())
				if not beer:
					lcd.message("Invalid choice \n Try again")
					time.sleep(2)


			#actual dispensing of the beer
			keg.solenoid.open()
			beer["amount"] = keg.flowmeter.flowing()
			keg.solenoid.close()


			#charging & sms state
			ounces = pricing.amountOZ(beer["amount"])
			toCharge = pricing.calculate(beer["price"], beer["amount"])
			chargeData = {self.apikey, user["id"], toCharge}
			returnval = requests.post("shaped-pride-770.appspot.com/account/user/charge", params=chargeData)
			if returnval:
				new_returnval = sms.send_recipt(user["phone"], ounces, beer["type"], toCharge)
				if new_returnval:
					lcd.message("Transaction completed. Thank You")
					time.sleep(5)
				elif new_returnval == False:
					lcd.message("Invalid account info. Abort.")
					time.sleep(2)
				elif attempts >= 5:
					lcd.message("Invalid account info. Abort.")
					time.sleep(2)
			else:
				lcd.message("Invalid charge info. Abort.")
				time.sleep(2)
								

#so i enter the card, it is tokenized, send all information for creating a customer, 
#get individual customer id, hook that with the pin in my db, user enters pin and i c
#an make a call to stripe with this user id. 


keg = Kegerator(SolenoidValve(7), FlowmeterValve(12))#creates new keg object
lcd = screen.Adafruit_CharLCD() #creates new screen object

#initializes all gpio pins to make sure everything is working
keg.initialize()

#enter loop to wait for user to approach
keg.run()

