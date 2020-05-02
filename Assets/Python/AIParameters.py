from Core import *
from RFCUtils import *
from Events import handler

def getTakenTilesThreshold(iPlayer):
	return dTakenTilesThreshold[civ(iPlayer)]
	
def getDistanceSubtrahend(iPlayer):
	return dDistanceSubtrahend[civ(iPlayer)]
	
def getDistanceFactor(iPlayer):
	return dDistanceFactor[civ(iPlayer)]
	
def getCompactnessModifier(iPlayer):
	return dCompactnessModifier[civ(iPlayer)]
	
def getTargetDistanceValueModifier(iPlayer):
	return dTargetDistanceValueModifier[civ(iPlayer)]

def getReligiousTolerance(iPlayer):
	return dReligiousTolerance[civ(iPlayer)]
	
def updateParameters(iPlayer):
	pPlayer = player(iPlayer)
	pPlayer.setTakenTilesThreshold(getTakenTilesThreshold(iPlayer))
	pPlayer.setDistanceSubtrahend(getDistanceSubtrahend(iPlayer))
	pPlayer.setDistanceFactor(getDistanceFactor(iPlayer))
	pPlayer.setCompactnessModifier(getCompactnessModifier(iPlayer))
	pPlayer.setTargetDistanceValueModifier(getTargetDistanceValueModifier(iPlayer))
	pPlayer.setReligiousTolerance(getReligiousTolerance(iPlayer))

@handler("GameStart")
def init():
	for iPlayer in players.all().barbarian():
		updateParameters(iPlayer)
		
def onTechAcquired(iPlayer, iTech):
	if iTech == iExploration:
		iCiv = civ(iPlayer)
		if iCiv in dDistanceSubtrahendExploration: player(iPlayer).setDistanceSubtrahend(dDistanceSubtrahendExploration[iCiv])
		if iCiv in dDistanceFactorExploration: player(iPlayer).setDistanceFactor(dDistanceFactorExploration[iCiv])
		if iCiv in dCompactnessModifierExploration: player(iPlayer).setCompactnessModifier(dCompactnessModifierExploration[iCiv])
	
dTakenTilesThreshold = defaultdict({
iBabylonia : 14,
iCarthage : 12,
iKorea : 20,
iMaya : 12,
iByzantium : 10,
iVikings : 18,
iTurks : 10,
iArabia : 12,
iHolyRome : 18,
iRussia : 7,
iMali : 10,
iPoland : 18,
iPortugal : 15,
iInca : 10,
iItaly : 18,
iMongols : 10,
iMughals : 15,
iNetherlands : 15,
iGermany : 12,
}, default=13)

dDistanceSubtrahend = defaultdict({
iBabylonia : 3,
iHarappa : 3,
iGreece : 3,
iIndia : 3,
iRome : 3,
iKorea : 6,
iMaya : 3,
iByzantium : 3,
iJapan : 3,
iVikings : 6,
iTurks : 3,
iMoors : 3,
iSpain : 3,
iFrance : 3,
iEngland : 3,
iHolyRome : 5,
iRussia : 5,
iMali : 3,
iInca : 3,
iItaly : 5,
iOttomans : 3,
iGermany : 3,
}, default=4)

dDistanceSubtrahendExploration = defaultdict({
iVikings : 4,
iMoors : 4,
iSpain : 4,
iFrance : 4,
iEngland : 4,
iGermany : 4,
}, default=4)

dDistanceFactor = defaultdict({
iChina : 350,
iGreece : 300,
iCarthage : 400,
iPolynesia : 400,
iPersia : 400,
iRome : 350,
iTamils : 400,
iEthiopia : 400,
iByzantium : 400,
iTurks : 200,
iArabia : 250,
iTibet : 400,
iIndonesia : 400,
iHolyRome : 400,
iRussia : 150,
iPoland : 150,
iPortugal : 150,
iMongols : 200,
iMughals : 400,
iOttomans : 400,
iThailand : 400,
iCongo : 300,
iNetherlands : 150,
iGermany : 300,
iAmerica : 200,
iArgentina : 150,
iBrazil : 150,
iCanada : 150,
}, default=500)

dDistanceFactorExploration = defaultdict({
iMoors : 300,
iSpain : 150,
iFrance : 150,
iEngland : 100,
}, default=500)

dCompactnessModifier = defaultdict({
iChina : 80,
iGreece : 10,
iIndia : 20,
iCarthage : 5,
iPolynesia : 10,
iRome : 30,
iTamils : 100,
iEthiopia : 30,
iKorea : 120,
iByzantium : 30,
iJapan : 20,
iVikings : 5,
iArabia : 10,
iIndonesia : 35,
iHolyRome : 100,
iPoland : 30,
iPortugal : 5,
iItaly : 70,
iNetherlands : 5,
iAmerica : 20,
}, default=40)

dCompactnessModifierExploration = defaultdict({
iSpain : 10,
iFrance : 5,
iEngland : 5,
}, default=40)

dTargetDistanceValueModifier = defaultdict({
iGreece : 5,
iPersia : 3,
iRome : 3,
iTamils : 7,
iJapan : 7,
iVikings : 7,
iTurks : 2,
iArabia : 7,
iSpain : 3,
iFrance : 3,
iEngland : 3,
iHolyRome : 7,
iRussia : 4,
iMongols : 1,
iPortugal : 3,
iNetherlands : 3,
iGermany : 3,
iAmerica : 3,
}, default=10)

dReligiousTolerance = defaultdict({
iEgypt : 4,
iChina : 4,
iHarappa : 4,
iGreece : 2,
iIndia : 4,
iPolynesia : 4,
iRome : 2,
iTamils : 4,
iKorea : 4,
iByzantium : 2,
iTibet : 2,
iIndonesia : 4,
iSpain : 1,
iFrance : 2,
iKhmer : 4,
iEngland : 2,
iHolyRome : 2,
iRussia : 1,
iMali : 2,
iPortugal : 2,
iItaly : 2,
iMongols : 4,
iMughals : 4,
iThailand : 4,
iNetherlands : 4,
iAmerica : 4,
iCanada : 4,
}, default=3)