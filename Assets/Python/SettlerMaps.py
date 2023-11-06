from Core import *
from Files import *
from Periods import *
from Events import handler


def applyMap(iCivilization, iPeriod=-1):
	for p in plots.all().land():
		p.setSettlerValue(iCivilization, 0)

	for (x, y), iValue in FileMap.read("Settler/%s.csv" % civ_name(iCivilization)):
		if iValue and not plot(x, y).isWater():
			plot(x, y).setSettlerValue(iCivilization, iValue)
	
	if iPeriod != -1:
		for (x, y), iValue in FileMap.read("Settler/Period/%s.csv" % dPeriodNames[iPeriod]):
			if not plot(x, y).isWater():
				plot(x, y).setSettlerValue(iCivilization, iValue)
		
def init():
	for iCivilization in lBirthOrder:
		applyMap(iCivilization)


# TODO: we updated this on civ change, is it really still necessary?
@handler("playerCivAssigned")
def activate(iPlayer, iCivilization):
	if iCivilization in lBirthOrder:
		applyMap(iCivilization)

@handler("periodChange")
def updateMapOnPeriodChange(iCivilization, iPeriod):
	applyMap(iCivilization, iPeriod)
