from Core import *
from Events import handler
	
def updateCore(iPlayer):
	coreArea = plots.core(iPlayer)
	for plot in plots.all():
		if plot.isWater() or (plot.isPeak() and location(plot) not in lPeakExceptions): continue
		plot.setCore(iPlayer, location(plot) in coreArea)

@handler("GameStart")
def init():
	for iPlayer in players.major():
		updateCore(iPlayer)
		
@handler("GameStart")
def resetStoredData():
	data.setup()