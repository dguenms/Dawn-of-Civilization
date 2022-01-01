from Core import *
from Events import handler
	

def updateCore(iCivilization):
	coreArea = plots.core(iCivilization)
	for plot in plots.all():
		if plot.isWater() or (plot.isPeak() and location(plot) not in lPeakExceptions): continue
		plot.setCore(iCivilization, plot in coreArea)

@handler("GameStart")
def init():
	for iCivilization in civs.major():
		updateCore(iCivilization)
		
@handler("GameStart")
def resetStoredData():
	data.setup()

@handler("periodChange")
def updateCoreOnPeriodChange(iCivilization):
	updateCore(iCivilization)