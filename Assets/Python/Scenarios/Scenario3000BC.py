from Civilizations import initScenarioTechs
from Core import *


lInitialCivs = [iEgypt, iBabylonia, iHarappa]


def initScenario():
	initScenarioTechs()
	createStartingUnits()
	

def createStartingUnits():
	for iPlayer, iCivilization in enumerate(lInitialCivs):
		capital = plots.capital(iCivilization)
		
		makeUnit(iPlayer, unique_unit(iCivilization, iSettler), capital)
		makeUnit(iPlayer, unique_unit(iCivilization, iMilitia), capital)
