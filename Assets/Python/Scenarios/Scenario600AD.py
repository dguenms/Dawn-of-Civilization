from Resources import setupScenarioResources

from Scenario import *
from Locations import *
from RFCUtils import *
from Core import *

lCivilizations = [
	Civilization(
		iChina, 
		iLeader=iTaizong, 
		iGold=300,
		iStateReligion=iConfucianism,
		lCivics=[iDespotism, iCitizenship, iManorialism, iMerchantTrade, iMonasticism],
		techs=techs.column(6).including(iMachinery, iAlchemy, iCivilService).without(iNobility)
	),
	Civilization(
		iKorea,
		iGold=200,
		iStateReligion=iBuddhism,
		lCivics=[iDespotism, iCitizenship, iCasteSystem, iRedistribution, iMonasticism],
		techs=techs.column(6).including(iMachinery).without(iScholarship),
	),
	Civilization(
		iByzantium,
		iGold=400,
		iStateReligion=iOrthodoxy,
		lCivics=[iDespotism, iVassalage, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(6).including(iFortification,iMachinery, iCivilService)
	),
	Civilization(
		iJapan,
		iGold=300,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iRedistribution, iDeification],
		techs=techs.column(6).without(iScholarship)
	),
	Civilization(
		iNorse,
		iGold=150,
		lCivics=[iElective, iVassalage, iSlavery, iMerchantTrade, iConquest],
		lEnemies=[iIndependent, iIndependent2],
		techs=techs.column(6).without(iEthics)
	),
	Civilization(
		iTurks,
		iGold=100,
		lCivics=[iDespotism, iVassalage, iSlavery, iMerchantTrade, iConquest],
		lEnemies=[iIndependent, iIndependent2],
		techs=techs.column(5).including(iNobility, iSteel).without(iNavigation, iMedicine, iPhilosophy)
	),
	Civilization(
		iNative,
		iGold=300,
		techs=techs.column(4)
	),
	Civilization(
		iIndependent2,
		iGold=100,
		techs=techs.column(5)
	),
	Civilization(
		iIndependent,
		iGold=100,
		techs=techs.column(5)
	),
]

lTribalVillages = [
	((54, 48), (61, 54)), # Iberia
	((62, 61), (69, 69)), # North Germany
	((52, 64), (54, 67)), # Ireland
	((55, 62), (59, 71)), # Britain
	((65, 70), (75, 78)), # Scandinavia
	((84, 64), (96, 70)), # Russia
	((96, 53), (104, 58)), # Transoxiana
	((103, 36), (110, 42)), # Deccan
	((134, 46), (136, 51)), # Kyushu
	((137, 59), (140, 62)), # Hokkaido
	((99, 65), (119, 72)), # Siberia
	((122, 24), (132, 32)), # Indonesia
	((79, 19), (84, 28)), # East Africa
	((75, 11), (81, 18)), # South Africa
	((21, 57), (30, 62)), # Great Lakes
	((15, 51), (21, 64)), # Great Plains
	((36, 29), (44, 33)), # Amazon
	((37, 11), (41, 20)), # Parana
	((25, 42), (33, 46)), # Caribbean
]


def createStartingUnits():
	# Japan
	capital = plots.capital(iJapan)
	if not player(iJapan).isHuman():
		makeUnits(iJapan, iCrossbowman, capital, 2)
		makeUnits(iJapan, iSamurai, capital, 3)
	
	# Byzantium
	capital = plots.capital(iByzantium)
	createRoleUnit(iByzantium, capital, iFerry, 2)
	createRoleUnit(iByzantium, capital, iAttackSea, 2)
	
	# Norse
	capital = plots.capital(iNorse)
	createRoleUnit(iNorse, capital, iWorkerSea)
	createRoleUnit(iNorse, capital, iExploreSea, player(iNorse).isHuman() and 2 or 3)
	
	if player(iNorse).isHuman():
		createRoleUnit(iNorse, capital, iSettleSea)
		createRoleUnit(iNorse, capital, iSettle)
		createRoleUnit(iNorse, capital, iDefend, 2)
	else:
		makeUnit(iNorse, iSettler, (60, 56))
		makeUnit(iNorse, iArcher, (60, 56))
		makeUnit(iNorse, iSettler, (63, 59))
		makeUnit(iNorse, iArcher, (63, 59))
	
	# Korea
	capital = plots.capital(iKorea)
	if not player(iKorea).isHuman():
		makeUnits(iKorea, iHeavySwordsman, capital, 2)


scenario600AD = Scenario(
	iStartYear = 600,
	fileName = "RFC_600AD",
	
	lCivilizations = lCivilizations,
	lTribalVillages = lTribalVillages,
	
	iOwnerBaseCulture = 20,
	
	greatWall = GreatWall(
		tGraphicsTL = (99, 46),
		tGraphicsBR = (104, 49),
		lGraphicsExceptions = [(99, 47), (99, 48), (99, 49), (100, 49), (101, 49), (104, 49)],
		lBorderExceptions = [(99, 45)],
		
		lEffectAreas = [((99, 40), (104, 49)), ((103, 39), (107, 45))],
	),
	
	createStartingUnits = createStartingUnits,
)
		
