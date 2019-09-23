from Consts import *
from RFCUtils import utils

def getModifier(iPlayer, iModifier):
	iCivilization = gc.getPlayer(iPlayer).getCivilizationType()
	if iCivilization in lOrder:
		return tModifiers[iModifier][lOrder.index(iCivilization)]
	return tDefaults[iModifier]
	
def getAdjustedModifier(iPlayer, iModifier):
	if utils.getScenario() > i3000BC and iPlayer < iVikings:
		if iModifier in dLateScenarioModifiers:
			return getModifier(iPlayer, iModifier) * dLateScenarioModifiers[iModifier] / 100
	return getModifier(iPlayer, iModifier)
	
def setModifier(iPlayer, iModifier, iNewValue):
	gc.getPlayer(iPlayer).setModifier(iModifier, iNewValue)
	
def changeModifier(iPlayer, iModifier, iChange):
	setModifier(iPlayer, iModifier, gc.getPlayer(iPlayer).getModifier(iModifier) + iChange)
	
def adjustModifier(iPlayer, iModifier, iPercent):
	setModifier(iPlayer, iModifier, gc.getPlayer(iPlayer).getModifier(iModifier) * iPercent / 100)
	
def adjustModifiers(iPlayer):
	for iModifier in dLateScenarioModifiers:
		adjustModifier(iPlayer, iModifier, dLateScenarioModifiers[iModifier])
		
def adjustInflationModifier(iPlayer):
	adjustModifier(iPlayer, iModifierInflationRate, dLateScenarioModifiers[iModifierInflationRate])
	
def updateModifier(iPlayer, iModifier):
	setModifier(iPlayer, iModifier, getModifier(iPlayer, iModifier))
	
def updateModifiers(iPlayer):
	for iModifier in range(iNumModifiers):
		updateModifier(iPlayer, iModifier)
		
def init():
	for iPlayer in range(iNumTotalPlayersB):
		updateModifiers(iPlayer)
		
		if utils.getScenario() > i3000BC and iPlayer < iVikings:
			adjustModifiers(iPlayer)
		
		gc.getPlayer(iPlayer).updateMaintenance()
		

### Modifier types ###

iNumModifiers = 13
(iModifierCulture, iModifierUnitUpkeep, iModifierResearchCost, iModifierDistanceMaintenance, iModifierCitiesMaintenance,
iModifierCivicUpkeep, iModifierHealth, iModifierUnitCost, iModifierWonderCost, iModifierBuildingCost,
iModifierInflationRate, iModifierGreatPeopleThreshold, iModifierGrowthThreshold) = range(iNumModifiers)

### Sequence of spawns ###

lOrder = [iCivEgypt, iCivBabylonia, iCivHarappa, iCivChina, iCivGreece, iCivIndia, iCivCarthage, iCivPolynesia, iCivPersia, iCivRome, iCivMaya, iCivTamils, iCivEthiopia, iCivVietnam, iCivKorea, iCivByzantium, iCivJapan, iCivVikings, iCivTurks, iCivArabia, iCivTibet, iCivIndonesia, iCivBurma, iCivMoors, iCivSpain, iCivFrance, iCivKhmer, iCivEngland, iCivHolyRome, iCivKievanRus, iCivHungary, iCivPhilippines, iCivSwahili, iCivMamluks, iCivMali, iCivPoland, iCivZimbabwe, iCivPortugal, iCivInca, iCivItaly, iCivNigeria, iCivMongols, iCivAztecs, iCivMughals, iCivOttomans, iCivRussia, iCivThailand, iCivCongo, iCivIran, iCivSweden, iCivNetherlands, iCivManchuria, iCivGermany, iCivAmerica, iCivArgentina, iCivMexico, iCivColombia, iCivBrazil, iCivAustralia, iCivBoers, iCivCanada, iCivIndependent, iCivIndependent2, iCivNative, iCivCeltia, iCivBarbarian]

### Modifiers (by civilization!) ###

#						(	EGY	BAB	HAR	CHI	GRE	IND	CAR	PLY	PER	ROM	MAY	TAM	ETH	VIE	KOR	BYZ	JAP	VIK	TUR	ARA	TIB	INO	BUR	MOO	SPA	FRA	KHM	ENG	HRE	KRS	HUN	PHI	SWA	MAM	MAL	POL	ZIM	POR	INC	ITA	NIG	MON	AZT	MUG	OTT	RUS	THA	CON	IRA	SWE	NET	MAN	GER	AME	ARG	MEX	COL	BRA	AUS	BOE	CAN		IND	IND	NAT	CEL	SEL	BAR	)

tCulture =				(	 90, 80, 80, 80,100, 80,100,100,100,100,100,110, 90,100, 50,100,110,130,120,110,120,120,120,125,125,160,120,130,150,130,120,130,120,130,130,110,130,147,140,150,120,135,140,125,150,130,130,130,135,140,165,140,150,140,130,140,140,140,140,140,140,	 20, 20, 20, 50, 50, 30	)

tUnitUpkeep =			(	135,120,200,120,110,135,115,100,100,110,110,100,115,100,100,110,105, 90,100,120,110,100,110,110,110,100, 90,100,100,110,100,100,100,100,100,100,100,100,100,100, 90, 75, 90,110,120,100, 90, 90,110, 90, 90, 90, 75, 80, 80, 90, 90, 80, 80, 80, 75,	  0,  0,100,100, 50,100	)
tResearchCost =			(	140,125,125,120,130,130,110,200,125,120,115,120,120,110,105,140,120, 85,120,110, 90,100,110, 90, 80, 80, 90, 80,100, 85, 80,100,100, 90,110, 80,100, 85, 80, 70, 90, 90, 85,120,120, 85,100, 85,110, 90, 80,100, 70, 75, 70, 90, 90, 90, 75, 80, 70,	110,110,110,350,110,110	)
tDistanceMaintenance =	(	100,110,120,120, 90,120, 60, 50, 90, 70,100, 95,100,110,120, 80, 95, 70, 60, 90,120, 80,110, 80, 55, 65, 80, 55, 70, 80, 75, 65, 80, 80, 80, 90, 80, 80, 60, 70, 80, 75, 70,100,110, 70, 80, 80,100, 70, 70, 70, 80, 60, 50, 70, 70, 80, 60, 80, 70,	 20, 20, 20, 20, 20, 20	)
tCitiesMaintenance =	(	135,135,125,120,125,150,120,100, 90, 60,115,100,115,110,130, 80,110, 75, 90,110,120,100, 90, 70, 50, 70,100, 70, 75, 80, 75, 90, 90, 90, 90, 75, 85, 85, 80, 80, 90, 75, 85,100,120, 70,100, 90,100, 75, 80, 70, 75, 70, 50, 85, 85, 80, 70, 70, 60,	 30, 30, 30, 30, 30, 30	)
tCivicUpkeep =			(	120,110,100,120,110,140, 70, 80, 70, 75, 80, 80, 80, 80, 80, 90, 80, 80,110, 90, 80,100,110, 90, 75, 80,100, 70, 70, 80, 80, 80, 80, 80, 80, 70, 80, 80, 60, 60, 70, 60, 60, 90, 90, 80, 80, 80, 80, 70, 70, 70, 60, 50, 50, 70, 70, 75, 75, 70, 75,	 70, 70, 70, 70, 70, 70	)
tHealth =				(	  2,  1,  1,  1,  3,  1,  3,  3,  3,  3,  3,  2,  3,  3,  3,  3,  2,  3,  2,  2,  3,  3,  3,  2,  2,  2,  3,  2,  2,  2,  2,  2,  2,  2,  2,  2,  3,  2,  3,  2,  4,  3,  3,  4,  4,  2,  4,  4,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,	  0,  0,  0,  0,  0,  0	)

tUnitCost =				(	110,140,200,130,110,120, 90,100, 90,100,105, 85, 90, 90, 80,115, 90, 85,100,100,110,105,110,100, 90, 90, 90,100, 90, 70, 80, 90, 90, 90, 90, 80, 90, 90,100,110, 90, 80,100,100,100, 90, 90, 70, 90, 90, 90, 90, 75, 85, 80, 85, 85, 85, 85, 85, 85,	200,200,150,150,100,140	)
tWonderCost = 			(	 80, 80, 80,120, 80,100, 90,100, 85,100, 90,100,100,100,100,110,100, 90,120, 90,100, 80, 70, 85, 90, 70, 90, 90,100, 80,110, 90, 90, 70, 90,100, 90, 90, 80, 80, 85, 90, 80, 80, 90,100, 90,100, 85, 90,100,100, 90, 70, 70, 90, 90, 90, 80, 90, 80,	150,150,150,100,100,100	)
tBuildingCost =			(	110,110,100,120,100,110, 90, 50,110, 90, 90, 70,100, 90, 80,110,100, 90,100,100, 80, 90, 90, 90, 90, 85,100, 90, 85, 80, 85, 80, 80, 90, 80, 80, 70, 80, 70, 80, 80, 80, 80, 85, 80, 90, 80, 80, 80, 80, 80, 75, 70, 70, 70, 80, 80, 75, 70, 75, 80,	100,100,150,100,100,100	)
tInflationRate =		(	130,130,130,120,130,140,130,130,130,130,125,110,130,120, 90,120, 80, 70, 90, 85,100, 90,120, 85, 90, 75,100, 70, 70, 85, 80,100,115, 75,115, 70, 85, 80, 80, 85, 75, 90, 80,100,100, 75, 75, 75, 85, 75, 85, 90, 70, 65, 60, 65, 65, 60, 60, 60, 60,	 95, 95, 95, 95, 95, 95	)
tGreatPeopleThreshold =	(	140,140,140,140,110,125,120,120,110,110,100,110,110,110,110,120,110, 90, 90, 80, 85, 90, 60, 75, 75, 70, 90, 75, 80, 80, 85, 80, 80, 80, 80, 80, 80, 75, 70, 65, 85, 70, 70, 75, 80, 80, 80, 85, 80, 70, 70, 70, 65, 65, 70, 80, 80, 80, 75, 80, 75,	100,100,100,100,100,100	)
tGrowthThreshold =		(	150,150,150,120,130,150,120,120,130,120,110,110,100,110,112, 80,110, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 70, 80, 60, 80, 80, 75, 75, 75, 80, 80, 80, 70, 70, 75, 75, 70, 70, 70, 80, 75, 75, 70, 75, 75, 65, 70, 70, 70, 70, 70, 70, 70, 70, 70,	125,125,125,125,125,125	)

tModifiers = (tCulture, tUnitUpkeep, tResearchCost, tDistanceMaintenance, tCitiesMaintenance, tCivicUpkeep, tHealth, tUnitCost, tWonderCost, tBuildingCost, tInflationRate, tGreatPeopleThreshold, tGrowthThreshold)

tDefaults = (100, 100, 100, 100, 100, 100, 2, 100, 100, 100, 100, 100, 100)

dLateScenarioModifiers = {
iModifierUnitUpkeep : 90,
iModifierDistanceMaintenance : 85,
iModifierCitiesMaintenance : 80,
iModifierCivicUpkeep : 90,
iModifierInflationRate : 85,
iModifierGreatPeopleThreshold : 85,
iModifierGrowthThreshold : 80,
}