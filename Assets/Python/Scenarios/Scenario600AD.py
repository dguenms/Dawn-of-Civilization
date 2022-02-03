from Civilizations import initScenarioTechs
from Civilization import Civilization
from Core import *


class Scenario(object):
	
	iStartYear = 600
	lInitialCivs = [iChina, iKorea, iByzantium, iJapan, iTurks, iVikings]
	fileName = "RFC_600AD"
	
	lCivilizations = [
		Civilization(
			iChina, 
			iLeader=iTaizong, 
			iGold=300,
			iStateReligion=iConfucianism,
			lCivics = [iDespotism, iCitizenship, iManorialism, iMerchantTrade, iMonasticism]
		),
		Civilization(
			iKorea,
			iGold=200,
			iStateReligion=iBuddhism,
			lCivics = [iDespotism, iCitizenship, iCasteSystem, iRedistribution, iMonasticism]
		),
		Civilization(
			iByzantium,
			iGold=400,
			iStateReligion=iOrthodoxy,
			lCivics = [iDespotism, iVassalage, iManorialism, iMerchantTrade, iClergy]
		),
		Civilization(
			iJapan,
			iGold=300,
			iStateReligion=iBuddhism,
			lCivics = [iMonarchy, iVassalage, iCasteSystem, iRedistribution, iDeification]
		),
		Civilization(
			iVikings,
			iGold=150,
			lCivics = [iElective, iVassalage, iSlavery, iMerchantTrade, iConquest]
		),
		Civilization(
			iTurks,
			iGold=100,
			lCivics = [iDespotism, iVassalage, iSlavery, iMerchantTrade, iConquest]
		),
	]
	
	@classmethod
	def initScenario(cls):
		initScenarioTechs()
		createStartingUnits()
		
		for civilization in cls.lCivilizations:
			civilization.apply()
	

def createStartingUnits():
	for iPlayer in players.major().alive():
		iCiv = civ(iPlayer)
		capital = plots.capital(iCiv)
		
		makeUnit(iPlayer, unique_unit(iCiv, iSettler), capital)
		makeUnit(iPlayer, unique_unit(iCiv, iMilitia), capital)
