def calculate(cost, amount):
	toCharge = cost * amount
	toCharge = toCharge * 100 #stripe requires money to be sent w/out decimal
	return toCharge

def amountOZ(amount):
	ounces = amount / 32
	return  ounces
