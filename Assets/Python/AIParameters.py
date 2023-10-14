from Core import *
from RFCUtils import *
from Events import handler

def getTakenTilesThreshold(iPlayer):
	return dTakenTilesThreshold[iPlayer]
	
def getDistanceSubtrahend(iPlayer):
	return dDistanceSubtrahend[iPlayer]
	
def getDistanceFactor(iPlayer):
	return dDistanceFactor[iPlayer]
	
def getCompactnessModifier(iPlayer):
	return dCompactnessModifier[iPlayer]
	
def getTargetDistanceValueModifier(iPlayer):
	return dTargetDistanceValueModifier[iPlayer]

def getReligiousTolerance(iPlayer):
	return dReligiousTolerance[iPlayer]
	
def updateParameters(iPlayer):
	pPlayer = player(iPlayer)
	pPlayer.setTakenTilesThreshold(getTakenTilesThreshold(iPlayer))
	pPlayer.setDistanceSubtrahend(getDistanceSubtrahend(iPlayer))
	pPlayer.setDistanceFactor(getDistanceFactor(iPlayer))
	pPlayer.setCompactnessModifier(getCompactnessModifier(iPlayer))
	pPlayer.setTargetDistanceValueModifier(getTargetDistanceValueModifier(iPlayer))
	pPlayer.setReligiousTolerance(getReligiousTolerance(iPlayer))
		
@handler("playerCivAssigned")
def onPlayerCivAssigned(iPlayer):
	updateParameters(iPlayer)

@handler("techAcquired")
def onTechAcquired(iTech, iTeam, iPlayer):
	if iTech == iExploration:
		if iPlayer in dDistanceSubtrahendExploration: player(iPlayer).setDistanceSubtrahend(dDistanceSubtrahendExploration[iPlayer])
		if iPlayer in dDistanceFactorExploration: player(iPlayer).setDistanceFactor(dDistanceFactorExploration[iPlayer])
		if iPlayer in dCompactnessModifierExploration: player(iPlayer).setCompactnessModifier(dCompactnessModifierExploration[iPlayer])
	
dTakenTilesThreshold = CivDict({
iBabylonia : 14,
iCarthage : 12,
iKorea : 20,
iMaya : 12,
iByzantium : 10,
iVikings : 18,
iTurks : 10,
iArabia : 12,
iHolyRome : 18,
iMali : 10,
iPoland : 18,
iPortugal : 15,
iInca : 10,
iItaly : 18,
iMongols : 10,
iMughals : 15,
iRussia : 7,
iNetherlands : 15,
iGermany : 12,
}, default=13)

dDistanceSubtrahend = CivDict({
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
iMali : 3,
iInca : 3,
iItaly : 5,
iRussia : 5,
iOttomans : 3,
iGermany : 3,
}, default=4)

dDistanceSubtrahendExploration = CivDict({
iVikings : 4,
iMoors : 4,
iSpain : 4,
iFrance : 4,
iEngland : 4,
iGermany : 4,
}, default=4)

dDistanceFactor = CivDict({
iChina : 350,
iGreece : 300,
iCarthage : 400,
iPolynesia : 400,
iPersia : 400,
iRome : 350,
iDravidia : 400,
iEthiopia : 400,
iByzantium : 400,
iTurks : 200,
iArabia : 250,
iTibet : 400,
iHolyRome : 400,
iPoland : 150,
iPortugal : 150,
iMongols : 200,
iMughals : 400,
iRussia : 150,
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

dDistanceFactorExploration = CivDict({
iMoors : 300,
iSpain : 150,
iFrance : 150,
iEngland : 100,
}, default=500)

dCompactnessModifier = CivDict({
iChina : 80,
iGreece : 10,
iIndia : 20,
iCarthage : 5,
iPolynesia : 10,
iRome : 30,
iDravidia : 100,
iEthiopia : 30,
iKorea : 120,
iByzantium : 30,
iJapan : 20,
iVikings : 5,
iArabia : 10,
iHolyRome : 100,
iPoland : 30,
iPortugal : 5,
iItaly : 70,
iNetherlands : 5,
iAmerica : 20,
}, default=40)

dCompactnessModifierExploration = CivDict({
iSpain : 10,
iFrance : 5,
iEngland : 5,
}, default=40)

dTargetDistanceValueModifier = CivDict({
iGreece : 5,
iPersia : 3,
iRome : 3,
iDravidia : 7,
iJapan : 7,
iVikings : 7,
iTurks : 2,
iArabia : 7,
iSpain : 3,
iFrance : 3,
iEngland : 3,
iHolyRome : 7,
iMongols : 1,
iPortugal : 3,
iRussia : 4,
iNetherlands : 3,
iGermany : 3,
iAmerica : 3,
}, default=10)

dReligiousTolerance = CivDict({
iEgypt : 4,
iChina : 4,
iHarappa : 4,
iGreece : 2,
iIndia : 4,
iPolynesia : 4,
iRome : 2,
iDravidia : 4,
iKorea : 4,
iByzantium : 2,
iTibet : 2,
iJava : 4,
iSpain : 1,
iFrance : 2,
iKhmer : 4,
iEngland : 2,
iHolyRome : 2,
iMali : 2,
iPortugal : 2,
iItaly : 2,
iMongols : 4,
iMughals : 4,
iRussia : 1,
iThailand : 4,
iNetherlands : 4,
iAmerica : 4,
iCanada : 4,
}, default=3)