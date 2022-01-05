from Civilizations import initScenarioTechs
from Core import *


lInitialCivs = [iEgypt, iBabylonia, iHarappa]


def initScenario():
	initScenarioTechs()
	createStartingUnits()
	

def createStartingUnits():
	for iPlayer in players.major().alive():
		iCiv = civ(iPlayer)
		capital = plots.capital(iCiv)
		
		makeUnit(iPlayer, unique_unit(iCiv, iSettler), capital)
		makeUnit(iPlayer, unique_unit(iCiv, iMilitia), capital)
