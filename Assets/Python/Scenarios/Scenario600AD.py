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
		iVikings,
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
		iIndependent,
		iGold=100,
		techs=techs.column(5)
	),
	Civilization(
		iIndependent2,
		iGold=100,
		techs=techs.column(5)
	),
	Civilization(
		iNative,
		iGold=300,
		techs=techs.column(4)
	)
]


def createStartingUnits():
	# Japan
	capital = plots.capital(iJapan)
	if not player(iJapan).isHuman():
		makeUnits(iJapan, iCrossbowman, capital, 2)
		makeUnits(iJapan, iSamurai, capital, 3)
	
	# Byzantium
	capital = plots.capital(iByzantium)
	createRoleUnit(iByzantium, capital, iTransport, 2)
	createRoleUnit(iByzantium, capital, iAttackSea, 2)
	
	# Vikings
	capital = plots.capital(iVikings)
	createRoleUnit(iVikings, capital, iWorkerSea)
	createRoleUnit(iVikings, capital, iExploreSea, player(iVikings).isHuman() and 2 or 3)
	
	if player(iVikings).isHuman():
		createRoleUnit(iVikings, capital, iSettleSea)
		createRoleUnit(iVikings, capital, iSettle)
		createRoleUnit(iVikings, capital, iDefend, 2)
	else:
		makeUnit(iVikings, iSettler, (60, 56))
		makeUnit(iVikings, iArcher, (60, 56))
		makeUnit(iVikings, iSettler, (63, 59))
		makeUnit(iVikings, iArcher, (63, 59))
	
	# Korea
	capital = plots.capital(iKorea)
	if not player(iKorea).isHuman():
		makeUnits(iKorea, iHeavySwordsman, capital, 2)


scenario600AD = Scenario(
	iStartYear = 600,
	fileName = "RFC_600AD",
	
	lCivilizations = lCivilizations,
	
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
		
