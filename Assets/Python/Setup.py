from Core import *
	
def updateCore(iPlayer):
	coreArea = plots.core(iPlayer)
	for plot in plots.all():
		if plot.isWater() or (plot.isPeak() and location(plot) not in lPeakExceptions): continue
		plot.setCore(iPlayer, location(plot) in coreArea)
			
def init():
	for iPlayer in players.major():
		updateCore(iPlayer)