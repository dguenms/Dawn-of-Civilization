from Civilizations import initScenarioTechs
from Core import *


class Scenario(object):
	
	iStartYear = 1700
	lInitialCivs = [iChina, iIndia, iTamils, iKorea, iJapan, iVikings, iTurks, iSpain, iFrance, iEngland, iHolyRome, iRussia, iPoland, iPortugal, iMughals, iOttomans, iThailand, iCongo, iIran, iNetherlands, iGermany]
	fileName = "RFC_1700AD"
	
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
