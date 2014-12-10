def calculate(cost, amount):
	toCharge = float(amount) / cost
	toCharge = "%.2f" % toCharge
	return toCharge

def amountOZ(amount):
	ounces = amount / 22.5
	ounces = "%.2f" % ounces
	return  ounces
