from Consts import *
from RFCUtils import utils

def getTakenTilesThreshold(iPlayer):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	return utils.getOrElse(dTakenTilesThreshold, iCiv, 13)
	
def getDistanceSubtrahend(iPlayer):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	return utils.getOrElse(dDistanceSubtrahend, iCiv, 4)
	
def getDistanceFactor(iPlayer):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	return utils.getOrElse(dDistanceFactor, iCiv, 500)
	
def getCompactnessModifier(iPlayer):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	return utils.getOrElse(dCompactnessModifier, iCiv, 40)
	
def getTargetDistanceValueModifier(iPlayer):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	return utils.getOrElse(dTargetDistanceValueModifier, iCiv, 10)

def getReligiousTolerance(iPlayer):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	return utils.getOrElse(dReligiousTolerance, iCiv, 3)
	
def updateParameters(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.setTakenTilesThreshold(getTakenTilesThreshold(iPlayer))
	pPlayer.setDistanceSubtrahend(getDistanceSubtrahend(iPlayer))
	pPlayer.setDistanceFactor(getDistanceFactor(iPlayer))
	pPlayer.setCompactnessModifier(getCompactnessModifier(iPlayer))
	pPlayer.setTargetDistanceValueModifier(getTargetDistanceValueModifier(iPlayer))
	pPlayer.setReligiousTolerance(getReligiousTolerance(iPlayer))
	
def init():
	for iPlayer in range(iNumTotalPlayersB):
		updateParameters(iPlayer)
		
def onTechAcquired(iPlayer, iTech):
	if iTech == iAstronomy:
		pPlayer = gc.getPlayer(iPlayer)
		iCiv = pPlayer.getCivilizationType()
		
		if iCiv in dDistanceSubtrahendAstronomy: pPlayer.setDistanceSubtrahend(dDistanceSubtrahendAstronomy[iCiv])
		if iCiv in dDistanceFactorAstronomy: pPlayer.setDistanceFactor(dDistanceFactorAstronomy[iCiv])
		if iCiv in dCompactnessModifierAstronomy: pPlayer.setCompactnessModifier(dCompactnessModifierAstronomy[iCiv])
	
dTakenTilesThreshold = {
iCivBabylonia : 14,
iCivPhoenicia : 12,
iCivKorea : 20,
iCivMaya : 12,
iCivByzantium : 10,
iCivVikings : 18,
iCivArabia : 12,
iCivHolyRome : 18,
iCivRussia : 7,
iCivMali : 10,
iCivPoland : 18,
iCivPortugal : 15,
iCivInca : 10,
iCivItaly : 18,
iCivMongolia : 10,
iCivMughals : 15,
iCivNetherlands : 15,
iCivGermany : 12,
}

dDistanceSubtrahend = {
iCivBabylonia : 3,
iCivHarappa : 3,
iCivGreece : 3,
iCivIndia : 3,
iCivRome : 3,
iCivKorea : 6,
iCivMaya : 3,
iCivByzantium : 3,
iCivJapan : 3,
iCivVikings : 6,
iCivMoors : 3,
iCivSpain : 3,
iCivFrance : 3,
iCivEngland : 3,
iCivHolyRome : 5,
iCivRussia : 5,
iCivMali : 3,
iCivInca : 3,
iCivItaly : 5,
iCivTurkey : 3,
iCivGermany : 3,
}

dDistanceSubtrahendAstronomy = {
iCivVikings : 4,
iCivMoors : 4,
iCivSpain : 4,
iCivFrance : 4,
iCivEngland : 4,
iCivGermany : 4,
}

dDistanceFactor = {
iCivChina : 350,
iCivGreece : 300,
iCivPhoenicia : 400,
iCivPolynesia : 400,
iCivPersia : 400,
iCivRome : 350,
iCivTamils : 400,
iCivEthiopia : 400,
iCivByzantium : 400,
iCivArabia : 250,
iCivTibet : 400,
iCivIndonesia : 400,
iCivHolyRome : 400,
iCivRussia : 150,
iCivPoland : 150,
iCivPortugal : 150,
iCivMongolia : 200,
iCivMughals : 400,
iCivTurkey : 400,
iCivThailand : 400,
iCivCongo : 300,
iCivNetherlands : 150,
iCivGermany : 300,
iCivAmerica : 200,
iCivArgentina : 150,
iCivBrazil : 150,
iCivCanada : 150,
}

dDistanceFactorAstronomy = {
iCivMoors : 300,
iCivSpain : 150,
iCivFrance : 150,
iCivEngland : 100,
}

dCompactnessModifier = {
iCivChina : 80,
iCivGreece : 10,
iCivIndia : 20,
iCivPhoenicia : 5,
iCivPolynesia : 10,
iCivRome : 30,
iCivTamils : 100,
iCivEthiopia : 30,
iCivKorea : 120,
iCivByzantium : 30,
iCivJapan : 20,
iCivVikings : 5,
iCivArabia : 10,
iCivIndonesia : 35,
iCivHolyRome : 100,
iCivPoland : 30,
iCivPortugal : 5,
iCivItaly : 70,
iCivNetherlands : 5,
iCivAmerica : 20,
}

dCompactnessModifierAstronomy = {
iCivSpain : 10,
iCivFrance : 5,
iCivEngland : 5,
}

dTargetDistanceValueModifier = {
iCivGreece : 5,
iCivPersia : 3,
iCivRome : 3,
iCivTamils : 7,
iCivJapan : 7,
iCivVikings : 7,
iCivArabia : 7,
iCivSpain : 3,
iCivFrance : 3,
iCivEngland : 3,
iCivHolyRome : 7,
iCivRussia : 4,
iCivMongolia : 1,
iCivPortugal : 3,
iCivNetherlands : 3,
iCivGermany : 3,
iCivAmerica : 3,
}

dReligiousTolerance = {
iCivEgypt : 4,
iCivChina : 4,
iCivHarappa : 4,
iCivGreece : 2,
iCivIndia : 4,
iCivPolynesia : 4,
iCivRome : 2,
iCivTamils : 4,
iCivKorea : 4,
iCivByzantium : 2,
iCivTibet : 2,
iCivKhmer : 4,
iCivIndonesia : 4,
iCivSpain : 1,
iCivFrance : 2,
iCivEngland : 2,
iCivHolyRome : 2,
iCivRussia : 1,
iCivMali : 2,
iCivPortugal : 2,
iCivItaly : 2,
iCivMongolia : 4,
iCivMughals : 4,
iCivThailand : 4,
iCivNetherlands : 4,
iCivAmerica : 4,
iCivCanada : 4,
}