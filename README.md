This is the file for the Intelligent Kegerator.

An intelligent kegerator is an automated beverage dispenser that supports user authentification through a mobile login system, user payments via Stripe, and user recipts via Twilio

The code will not truly work without the backend due to the standard protocol for creating post and get requests. We have created a DB utilizing the Django framework all on Google App Engine.  we've created on a private repo for the time being. 

All the files included in the repo are required in order to make the code pseudo run. That includes:
main.py - code entry point. contains meat of code
flowmeter.py - controls the adafruit flowmeter
pricing.py - controls and math needed for pricing
screen.py - library gotten from adafruit to use with the lcd
sms.py - controls all of the texting via the twilio api
solenoid.py - controls the brass solenoid whether it is open or closed 



Dependencies:
python 2.7 - retrieved through apt-get
pip - retrieved through apt-get
requests - retrieved through pip
Adafruit_CharLCD  - retrieved through apt-get

parts used:
solenoid - http://www.adafruit.com/products/996
flowmeter - http://www.adafruit.com/products/828
lcd screen - http://www.adafruit.com/products/399 (blue model)
keypad - http://www.amazon.com/MillionAccessories-Numeric-Keyboard-Notebook-Computer/dp/B007DVM39A/