import RPi.GPIO as GPIO
from screen import Adafruit_CharLCD
import solenoid
import pricing
import flowmeter
import time
import requests
import sms
import json
import signal
import sys

apikey = "hello"
def verifyPin(pin):
	global apikey
	data = {"api_key":apikey, "userid":pin}
	IDandPHONE = requests.post("http://shaped-pride-770.appspot.com/account/pin/", data)
#	IDandPHONE = {"phone" : 7039278262, "userid" : "test@test.com"}
	if "error" in IDandPHONE:
		return False
	else:
#		return IDandPHONE
		return IDandPHONE.json()




class Kegerator:

	def __init__ (self, solenoid, flowmeter, lcd):
		#in reaility we will get these from the db
		self.beer1price = 44
		self.beer1type = "Water"
		self.beer2price = 82
		self.lcd = lcd 
		self.beer2type =  "Beer"
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
			self.lcd.message("Welcome \n%d." % user[userid])
			time.sleep(2)
			self.lcd.message("Press '-' key to\nlog out anytime")
			time.sleep(2)
			

			try:
				self.lcd.clear()
				self.lcd.message("Choose Beverage.\n/=left, *=right")
				time.sleep(2)

				#beer selection
				while not beer:
					self.lcd.clear()
					self.lcd.message("/=left=%s\n*=right=%s") % (self.beer1type, self.beer2type)
					beer = self.beerSelection(raw_input())
						if beer == 
					if not beer:
						self.lcd.clear()
						self.lcd.message("Invalid choice \n Try again")
						time.sleep(2)


				#actual dispensing of the beer
				self.solenoid.open()
				beer["amount"] = self.flowmeter.flowing()
				self.solenoid.close()

				#charging & sms state
				ounces = pricing.amountOZ(beer["amount"])
				toChargeTwilio = pricing.calculate(beer["price"], beer["amount"])
				toChargeStripe = int(float(toChargeTwilio)*100)
				self.lcd.clear()
				self.lcd.message("Charging for\n%soz of liquid" % ounces)

				chargeData = {"api_key" : apikey, "username" : user["userid"], "price" : toChargeStripe}
				returnval = requests.post("http://shaped-pride-770.appspot.com/account/purchase/", chargeData)
				self.lcd.clear()			
				if "error" not in returnval:
					new_returnval = sms.send_receipt(user["phone"], ounces, beer["type"], toChargeTwilio)
					if new_returnval:
						self.lcd.message("Thank You\nCome Again")
						time.sleep(5)
					else:
						self.lcd.message("Invalid account\ninfo. Abort.")
						time.sleep(5)
				else:
					self.lcd.message("Invalid charge info. Abort.")
					time.sleep(2)


			except abort:
				self.lcd.clear()
				self.lcd.message("Abort button pressed. Start Over")
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


	signal.signal(signal.SIGINT, signal_handler)
	#enter loop to wait for user to approach
	keg.run()

