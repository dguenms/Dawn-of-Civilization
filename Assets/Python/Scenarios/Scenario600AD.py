from Civilizations import initScenarioTechs
from Core import *


class Scenario(object):
	
	iStartYear = 600
	lInitialCivs = [iChina, iKorea, iByzantium, iJapan, iTurks, iVikings]
	fileName = "RFC_600AD"
	
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
