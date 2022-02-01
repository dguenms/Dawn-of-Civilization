from Civilizations import initScenarioTechs
from Core import *


class Scenario(object):
	
	iStartYear = -3000
	lInitialCivs = [iEgypt, iBabylonia, iHarappa]
	fileName = "RFC_3000BC"
	
	@staticmethod
	def initScenario():
		initScenarioTechs()
		createStartingUnits()
	

def createStartingUnits():
	for iPlayer in players.major().alive():
		iCiv = civ(iPlayer)
		capital = plots.capital(iCiv)
		
		makeUnit(iPlayer, unique_unit(iCiv, iSettler), capital)
		makeUnit(iPlayer, unique_unit(iCiv, iMilitia), capital)
