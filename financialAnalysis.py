"""
Cash Flow Diagram
to retrieve/calculate
PVB, PVC, NPV, BCR, Payback Period, IRR
"""

discountRate = float(input("Enter discount rate in decimal: "))
numYears = int(input("Enter number of years: "))
print("===============================")
benefitsYearly = []
costsYearly = []
nettBenefitsYearly = []
PVfactor = 1
PVB = 0 # present value benefits
PVC = 0 # present value costs

for i in range(numYears+1):
	benefit = int(input("Enter BENEFITS @ year{}: ".format(i)))
	cost = int(input("Enter COSTS    @ year{}: ".format(i)))
	benefitsYearly.append(benefit)
	costsYearly.append(cost)
	
	nettBenefitsYearly.append(benefit-cost)

	PVB = PVB + benefitsYearly[-1] * PVfactor
	PVC = PVC + costsYearly[-1] * PVfactor
	PVfactor = PVfactor * (1/(1+discountRate))


NPV = PVB - PVC
BCR = PVB / PVC

# return i if year i breakeven
# return -1 if cant breakeven
def getPaybackPeriod(nb):
	totalBenefits = 0
	for i in range(len(nb)):
		totalBenefits = totalBenefits + nb[i]
		if(totalBenefits >= 0):
			return i
	return -1

paybackPeriod = getPaybackPeriod(nettBenefitsYearly)

# this function is useful to interpolate
# IRR, internal rate of return where PVB = PVC
def getNPV(nb, dr):
	# ARRAY - nb = nett benefits 
	# DECIMAL - dr = discount rate
	npv = 0
	pvfactor = 1
	for i in range(len(nb)):
		npv = npv + nb[i] * pvfactor
		pvfactor = pvfactor * (1/(1+dr))
	return npv

# assume NPV @ discountRate > 0
# guess IRR = 0.01 (increment slowly)
IRRneg = 0.01
while(getNPV(nettBenefitsYearly,IRRneg) > 0):
	IRRneg = IRRneg + 0.01

if(getNPV(nettBenefitsYearly,IRRneg) == 0):
	IRR = IRRneg
else:
	# NPV @ IRRpost > 0
	# NPV @ IRRneg < 0
	IRRpos = IRRneg - 0.01
	NPVpos = getNPV(nettBenefitsYearly,IRRpos)
	NPVneg = getNPV(nettBenefitsYearly,IRRneg)
	IRR = 100*(IRRpos + NPVpos*(IRRpos-IRRneg)/(NPVneg - NPVpos))

print("===============================")
print("PVB ($): {}".format(PVB))
print("PVC ($): {}".format(PVC))
print("NPV ($): {}".format(NPV))
print("BCR: {}".format(BCR))
print("Payback Period (years): {}".format(paybackPeriod))
print("IRR (%): {}".format(IRR))