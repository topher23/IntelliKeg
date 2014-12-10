import RPi.GPIO as GPIO
from screen import Adafruit_CharLCD
import solenoid
import pricing
import flowmeter
import time
import requests
import sms
import json

apikey = "hello"
def verifyPin(pin):
	global apikey
	data = {"api_key":apikey, "userid":pin}
#	IDandPHONE = requests.post("http://shaped-pride-770.appspot.com/account/pin/", data)
	IDandPHONE = {"phone" : 7039278262, "userid" : "test@test.com"}
	if "error" in IDandPHONE:
		return False
	else:
		return IDandPHONE
#		return IDandPHONE.json()



class Kegerator:

	def __init__ (self, solenoid, flowmeter, lcd):
		#in reaility we will get these from the db
		self.beer1price = 73
		self.beer1type = "Alewerks"
		self.beer2price = 82
		self.lcd = lcd 
		self.beer2type =  "Shock Top"
		self.solenoid = solenoid
		self.flowmeter = flowmeter


	#turn on gpio pins
	def initialize(self):
		GPIO.setmode(GPIO.BCM)
		


	def beerSelection(self, beer):
		if beer == "*":
			return {"price": self.beer1price, "type": self.beer1type, "amount":0}
		elif beer == "/":
			return {"price": self.beer2price, "type": self.beer2type, "amount":0}
		else:
			return False

	def run(self):
		global apikey
		attempts = 0
		while True:
			beertype = True
			beer = False

			
			#pin checking
			self.lcd.begin(1,16)
			self.lcd.clear()
			self.lcd.message("Please enter \nyour pin.")
			user = False
			while not user:
				user = verifyPin(int(raw_input()))
				if not user:
					self.lcd.clear()
					self.lcd.message("pin incorrect.\ntry again.")
			self.lcd.clear()
			self.lcd.message("User validated.\n Welcome.")
			time.sleep(2)

			
			#beer selection
			while not beer:
				self.lcd.clear()
				self.lcd.message("Choose Beer.\n/=left, *=right")
				beer = self.beerSelection(raw_input())
				if not beer:
					self.lcd.clear()
					self.lcd.message("Invalid choice \n Try again")
					time.sleep(2)


			#actual dispensing of the beer
			self.solenoid.open()
			testamount = beer["amount"] = self.flowmeter.flowing()
			self.solenoid.close()

			#charging & sms state
			ounces = pricing.amountOZ(beer["amount"])
			toChargeTwilio = pricing.calculate(beer["price"], beer["amount"])
			toChargeStripe = int(toChargeTwilio*100)

			chargeData = {"api_key" : apikey, "username" : user["userid"], "price" : toChargeStripe}
			returnval = requests.post("http://shaped-pride-770.appspot.com/account/purchase/", chargeData)			
			if "error" not in returnval:
				new_returnval = sms.send_receipt(user["phone"], ounces, beer["type"], toChargeTwilio)
				if new_returnval:
					self.lcd.message("Transaction completed. Thank You")
					time.sleep(5)
				elif new_returnval == False:
					self.lcd.message("Invalid account info. Abort.")
					time.sleep(2)
				elif attempts >= 5:
					self.lcd.message("Invalid account info. Abort.")
					time.sleep(2)
			else:
				self.lcd.message("Invalid charge info. Abort.")
				time.sleep(2)
								

#so i enter the card, it is tokenized, send all information for creating a customer, 
#get individual customer id, hook that with the pin in my db, user enters pin and i c
#an make a call to stripe with this user id. 


if __name__ == "__main__":
	lcd = Adafruit_CharLCD() #creates new screen object
	lcd.begin(1,16)
	keg = Kegerator(solenoid.SolenoidValve(4), flowmeter.FlowmeterValve(18),lcd)#creates new keg object

	#initializes all gpio pins to make sure everything is working
	keg.initialize()

	#enter loop to wait for user to approach
	keg.run()

