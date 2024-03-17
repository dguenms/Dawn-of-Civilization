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
	pPlayer.setTargetDistanceValueModifier(getTargetDistanceValueModifier(iPlayer))
	pPlayer.setReligiousTolerance(getReligiousTolerance(iPlayer))
		
@handler("playerCivAssigned")
def onPlayerCivAssigned(iPlayer):
	updateParameters(iPlayer)


dTargetDistanceValueModifier = CivDict({
iGreece : 5,
iPersia : 3,
iRome : 3,
iDravidia : 7,
iJapan : 7,
iNorse : 7,
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