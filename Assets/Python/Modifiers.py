from Consts import *
from RFCUtils import utils
from StoredData import data

def getModifier(iPlayer, iModifier):
	iCivilization = gc.getPlayer(iPlayer).getCivilizationType()
	WonderDivisor = 1
	if data.getWonderBuilder(iShwedagonPaya) == iPlayer:
		WonderMod = 2
	if iCivilization in lOrder:
		return tModifiers[iModifier][lOrder.index(iCivilization)] / WonderDivisor
	return tDefaults[iModifier] / WonderDivisor
	
def getAdjustedModifier(iPlayer, iModifier):
	if utils.getScenario() > i3000BC and iPlayer < iVikings and not iPlayer in [iInuit]:
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
		
		if utils.getScenario() > i3000BC and iPlayer < iVikings and not iPlayer in [iInuit]:
			adjustModifiers(iPlayer)
		
		gc.getPlayer(iPlayer).updateMaintenance()
		

### Modifier types ###

iNumModifiers = 13
(iModifierCulture, iModifierUnitUpkeep, iModifierResearchCost, iModifierDistanceMaintenance, iModifierCitiesMaintenance,
iModifierCivicUpkeep, iModifierHealth, iModifierUnitCost, iModifierWonderCost, iModifierBuildingCost,
iModifierInflationRate, iModifierGreatPeopleThreshold, iModifierGrowthThreshold) = range(iNumModifiers)

### Sequence of spawns ###

lOrder = [iCivEgypt, iCivBabylonia, iCivHarappa, iCivNorteChico, iCivNubia, iCivChina, iCivGreece, iCivOlmecs, iCivIndia, iCivCarthage, iCivCeltia, iCivPolynesia, iCivPersia, iCivRome, iCivMaya, iCivTamils, iCivEthiopia, iCivVietnam, iCivTeotihuacan, iCivInuit, iCivMississippi, iCivKorea, iCivTiwanaku, iCivByzantium, iCivWari, iCivJapan, iCivVikings, iCivTurks, iCivArabia, iCivTibet, iCivIndonesia, iCivBurma, iCivKhazars, iCivChad, iCivMoors, iCivSpain, iCivFrance, iCivOman, iCivKhmer, iCivMuisca, iCivYemen, iCivEngland, iCivHolyRome, iCivKievanRus, iCivHungary, iCivPhilippines, iCivChimu, iCivSwahili, iCivMamluks, iCivMali, iCivPoland, iCivZimbabwe, iCivPortugal, iCivInca, iCivItaly, iCivNigeria, iCivMongols, iCivAztecs, iCivMughals, iCivOttomans, iCivRussia, iCivThailand, iCivCongo, iCivIran, iCivSweden, iCivNetherlands, iCivManchuria, iCivGermany, iCivAmerica, iCivArgentina, iCivMexico, iCivColombia, iCivBrazil, iCivAustralia, iCivBoers, iCivCanada, iCivIsrael, iCivIndependent, iCivIndependent2, iCivNative, iCivBarbarian]

### Modifiers (by civilization!) ###

# 						(	EGY	BAB	HAR	NOR	NUB	CHI	GRE	OLM IND	CAR	CEL	PLY	PER	ROM	MAY	TAM	ETH	VIE	TEO	INU	MIS	KOR	TIW	BYZ	WAR	JAP	VIK	TUR	ARA	TIB	INO	BUR	KHA	CHA	MOO	SPA	FRA	OMA	KHM	MUI	YEM	ENG	HRE	KRS	HUN	PHI	CMU	SWA	MAM	MAL	POL	ZIM	POR	INC	ITA	NIG	MON	AZT	MUG	OTT	RUS	THA	CON	IRA	SWE	NET	MAN	GER	AME	ARG	MEX	COL	BRA	AUS	BOE	CAN	ISR			IND	IND	NAT	BAR	)

tCulture =				(	 90, 80, 80, 80, 80, 80,100, 80, 80,100,100,100,100,100,100,110, 90,100,100, 90,110, 50,110,100,120,110,130,120,110,120,120,120,100,120,125,125,160,130,120,140,140,130,150,130,120,130,120,130,130,130,110,130,147,140,150,120,135,140,125,150,130,130,130,135,140,165,140,150,140,130,140,140,140,140,140,140,140,		 20, 20, 20, 30 )

tUnitUpkeep =			(	135,120,200,200,135,120,110,200,135,115,135,100,100,110,110,100,115,100,100,200,110,100,100,110, 90,105, 90,100,120,110,100, 90, 90,110,110,110,100, 90, 90,100,100,100,100,100,100,100,110,100,100,100,100,100,100,100,100, 90, 75, 90,110,120,100, 90, 90,110, 90, 90, 90, 75, 80, 80, 90, 90, 80, 80, 80, 75, 75,		  0,  0,100,100 )
tResearchCost =			(	140,125,125,140,125,120,130,125,130,110,140,200,125,120,115,120,120,110,105,200,120,105, 90,140,110,120, 85,120,110, 90,100,120, 90, 90, 90, 80, 80, 90, 90,100, 80, 80,100, 85,100,100, 80,100, 90,110, 80,100, 85, 80, 70, 90, 90, 85,120,120, 85,100, 85,110, 90, 80,100, 70, 75, 70, 90, 90, 90, 75, 80, 70, 70,		110,110,110,110 )
tDistanceMaintenance =	(	100,110,120,150,135,120, 90,120,120, 60, 60, 50, 90, 70,100, 95,100,110,120, 50, 70,120, 90, 80, 80, 95, 70, 60, 90,120, 80, 70,100, 80, 80, 55, 65,100, 80,120, 55, 55, 70, 75, 65, 65, 90, 80, 80, 80, 90, 80, 80, 60, 70, 80, 75, 70,100,110, 70, 80, 80,100, 70, 70, 70, 80, 60, 50, 70, 70, 80, 60, 80, 70, 70,		 20, 20, 20, 20 )
tCitiesMaintenance =	(	135,135,125,150,100,120,125,130,150,120, 80,100, 90, 60,115,100,115,110,130, 50, 80,130,100, 80, 80,110, 75, 90,110,120,100, 90, 90, 70, 70, 50, 70,120,100,120, 70, 70, 75, 75, 90, 90,100, 90, 90, 90, 75, 85, 85, 80, 80, 90, 75, 85,100,120, 70,100, 90,100, 75, 80, 70, 75, 70, 50, 85, 85, 80, 70, 70, 60, 60,		 30, 30, 30, 30 )
tCivicUpkeep =			(	120,110,100, 70,120,120,110, 80,140, 70,110, 80, 70, 75, 80, 80, 80, 80, 80, 50, 90, 80, 70, 90, 80, 80, 80,110, 90, 80,100, 80, 70, 90, 90, 75, 80,100,100, 80, 70, 70, 70, 80, 80, 80, 90, 80, 80, 80, 70, 80, 80, 60, 60, 70, 60, 60, 90, 90, 80, 80, 80, 80, 70, 70, 70, 60, 50, 50, 70, 70, 75, 75, 70, 75, 75,		 70, 70, 70, 70 )
tHealth =				(	  2,  1,  1,  1,  2,  1,  3,  2,  1,  3,  3,  3,  3,  3,  3,  2,  3,  3,  3,  1,  2,  3,  2,  3,  2,  2,  3,  2,  2,  3,  3,  2,  3,  2,  2,  2,  2,  3,  3,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  3,  2,  3,  2,  4,  3,  3,  4,  4,  2,  4,  4,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,		  0,  0,  0,  0 )

tUnitCost =				(	110,140,200,100, 90,130,110,115,120, 90, 90,100, 90,100,105, 85, 90, 90,115, 80, 90, 80,100,115, 90, 90, 85,100,100,110,105,110,140, 80,100, 90, 90, 80, 90, 90, 80,100, 90, 70, 80, 90, 90, 90, 90, 90, 80, 90, 90,100,110, 90, 80,100,100,100, 90, 90, 70, 90, 90, 90, 90, 75, 85, 80, 85, 85, 85, 85, 85, 85, 85,		200,200,150,140 )
tWonderCost =			(	 80, 80, 80,120, 90,120, 80,120,100, 90,150,100, 85,100, 90,100,100,100, 90,120, 90,100, 90,110,110,100, 90,120, 90,100, 80, 70,110,100, 85, 90, 70,110, 90,100,100, 90,100, 80,110, 90,100, 90, 70, 90,100, 90, 90, 80, 80, 85, 90, 80, 80, 90,100, 90,100, 85, 90,100,100, 90, 70, 70, 90, 90, 90, 80, 90, 80, 80,		150,150,150,100 )
tBuildingCost =			(	110,110,100,100,100,120,100,100,110, 90, 90, 50,110, 90, 90, 70,100, 90, 90, 80, 80, 80, 90,110, 80,100, 90,100,100, 80, 90, 90, 80, 70, 90, 90, 85,100,100, 80, 90, 90, 85, 80, 85, 80, 80, 80, 90, 80, 80, 70, 80, 70, 80, 80, 80, 80, 85, 80, 90, 80, 80, 80, 80, 80, 75, 70, 70, 70, 80, 80, 75, 70, 75, 80, 80,		100,100,150,100 )
tInflationRate =		(	130,130,130,130,140,120,130,130,140,130,140,130,130,130,125,110,130,120,125,120,140, 90,130,120,110, 80, 70, 90, 85,100, 90,120, 90, 75, 85, 90, 75, 70,100,100, 90, 70, 70, 85, 80,100, 90,115, 75,115, 70, 85, 80, 80, 85, 75, 90, 80,100,100, 75, 75, 75, 85, 75, 85, 90, 70, 65, 60, 65, 65, 60, 60, 60, 60, 60,		 95, 95, 95, 95 )
tGreatPeopleThreshold =	(	140,140,140,140,140,140,110,140,125,120,140,120,110,110,100,110,110,110,100,140, 90,110, 90,120, 90,110, 90, 90, 80, 85, 90, 60, 80, 70, 75, 75, 70,110, 90,110,110, 75, 80, 80, 85, 80, 70, 80, 80, 80, 80, 80, 75, 70, 65, 85, 70, 70, 75, 80, 80, 80, 85, 80, 80, 70, 70, 65, 65, 70, 80, 80, 80, 75, 80, 75, 75,		100,100,100,100 )
tGrowthThreshold =		(	150,150,150,150,150,120,130,150,150,120,110,120,130,120,110,110,100,110,110, 60,100,112, 90, 80, 80,110, 80, 80, 80, 80, 80, 60, 70, 60, 80, 80, 80, 60, 80, 70, 60, 70, 80, 60, 80, 80, 70, 75, 75, 75, 80, 80, 80, 70, 70, 75, 75, 70, 70, 70, 80, 75, 75, 70, 75, 75, 65, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70,		125,125,125,125 )

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