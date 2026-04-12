from Core import *
from Resources import *
from Events import handler
	

def updateCore(iCivilization):
	coreArea = plots.core(iCivilization)
	for plot in plots.all():
		if plot.isWater() or (plot.isPeak() and location(plot) not in dConquerorPlotTypesDict): continue
		plot.setCore(iCivilization, plot in coreArea)

@handler("GameStart")
def init():
	for iCivilization in civs.major():
		updateCore(iCivilization)

@handler("GameStart")
def validatePeriodConstants():
	if not validatePeriodConstant(iNumPeriods):
		raise Exception("Invalid DLL period constants")
		
@handler("periodChange")
def updateCoreOnPeriodChange(iCivilization):
	updateCore(iCivilization)