from Core import *
from Files import *
from Periods import *
from Events import handler


def applyMap(iCivilization, iPeriod=-1):
	for p in plots.all().land():
		p.setWarValue(iCivilization, 0)

	for (x, y), iValue in FileMap.read("War/%s.csv" % civ_name(iCivilization)):
		if iValue and not plot(x, y).isWater():
			plot(x, y).setWarValue(iCivilization, iValue)
	
	if iPeriod != -1:
		for (x, y), iValue in FileMap.read("War/Period/%s.csv" % dPeriodNames[iPeriod]):
			if not plot(x, y).isWater():
				plot(x, y).setWarValue(iCivilization, iValue)
			
def init():
	for iCivilization in lBirthOrder:
		applyMap(iCivilization)

@handler("playerCivAssigned")
def activate(iPlayer, iCivilization):
	if iCivilization in lBirthOrder:
		applyMap(iCivilization)

@handler("periodChange")
def updateMapOnPeriodChange(iCivilization, iPeriod):
	applyMap(iCivilization, iPeriod)
}
