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
		iNubia,
		iGold=50,
		iStateReligion=iOrthodoxy,
		lCivics=[iMonarchy, iVassalage, iSlavery, iRedistribution, iMonasticism],
		techs=techs.column(5).including(iNobility, iArchitecture),
	),
	Civilization(
		iIndia,
		iLeader=iChandragupta,
		iGold=200,
		iStateReligion=iHinduism,
		lCivics=[iMonarchy, iCitizenship, iCasteSystem, iRedistribution, iClergy],
		techs=techs.column(5).including(iArchitecture, iArtisanry, iScholarship, iEthics),
	),
	Civilization(
		iCelts,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iManorialism, iRedistribution, iMonasticism],
		techs=techs.column(4).including(iCurrency, iLaw, iMedicine, iPhilosophy, iEthics),
	),
	Civilization(
		iDravidia,
		iGold=100,
		iStateReligion=iHinduism,
		lCivics=[iMonarchy, iCitizenship, iCasteSystem, iMerchantTrade, iMonasticism],
		techs=techs.column(5).including(iArtisanry, iPolitics, iEthics),
	),
	Civilization(
		iToltecs,
		iGold=50,
		lCivics=[iRedistribution, iDeification],
		techs=techs.column(4).including(iCurrency, iEngineering).without(iNavigation)
	),
	Civilization(
		iKorea,
		iGold=200,
		iStateReligion=iBuddhism,
		lCivics=[iDespotism, iCitizenship, iCasteSystem, iRedistribution, iMonasticism],
		techs=techs.column(6).including(iMachinery).without(iScholarship),
	),
	Civilization(
		iKhmer,
		iGold=50,
		iStateReligion=iHinduism,
		lCivics=[iDespotism, iCitizenship, iCasteSystem, iRedistribution, iMonasticism],
		techs=techs.column(5).including(iArtisanry).without(iLaw, iMedicine),
	),
	Civilization(
		iMali,
		iGold=200,
		lCivics=[iDespotism, iSlavery, iRedistribution],
		techs=techs.column(4).without(iNavigation).including(iAesthetics, iCurrency),
	),
	Civilization(
		iByzantium,
		iGold=400,
		iStateReligion=iOrthodoxy,
		lCivics=[iDespotism, iVassalage, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(6).including(iFortification,iMachinery, iCivilService)
	),
	Civilization(
		iFrance,
		iGold=150,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(6).without(iSteel, iArtisanry, iPolitics)
	),
	Civilization(
		iMalays,
		iGold=100,
		iStateReligion=iBuddhism,
		lCivics=[iDespotism, iCitizenship, iCasteSystem, iMerchantTrade, iDeification],
		techs=techs.column(5).including(iEthics).without(iEngineering)
	),
	Civilization(
		iJapan,
		iGold=300,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iRedistribution, iDeification],
		techs=techs.column(6).without(iPolitics, iScholarship)
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
	# Celts
	capital = plots.capital(iCelts)
	createRoleUnit(iDravidia, capital, iFerry, 1)

	# Dravidia
	capital = plots.capital(iDravidia)
	createRoleUnit(iDravidia, capital, iFerry, 2)
	createRoleUnit(iDravidia, capital, iEscort, 1)
	createRoleUnit(iDravidia, capital, iWorkerSea, 2)
	
	# Korea
	capital = plots.capital(iKorea)
	if not player(iKorea).isHuman():
		makeUnits(iKorea, iHeavySwordsman, capital, 2)
	
	# Khmer
	capital = plots.capital(iKhmer)
	createRoleUnit(iKhmer, capital, iWorkerSea)
	
	# Byzantium
	capital = plots.capital(iByzantium)
	createRoleUnit(iByzantium, capital, iFerry, 2)
	createRoleUnit(iByzantium, capital, iAttackSea, 2)
	
	# Malays
	capital = plots.capital(iMalays)
	createRoleUnit(iMalays, capital, iFerry, 1)
	createRoleUnit(iMalays, capital, iEscort, 1)
	createRoleUnit(iMalays, capital, iWorkerSea, 2)
	
	# Japan
	capital = plots.capital(iJapan)
	if not player(iJapan).isHuman():
		makeUnits(iJapan, iCrossbowman, capital, 2)
		makeUnits(iJapan, iSamurai, capital, 3)
	
	# Norse
	capital = plots.capital(iNorse)
	createRoleUnit(iNorse, capital, iWorkerSea)
	createRoleUnit(iNorse, capital, iExploreSea, player(iNorse).isHuman() and 2 or 3)


def setupGoals(iCiv, goals):
	if iCiv == iKhmer:
		goals[0].requirements[0].succeed()


scenario600AD = Scenario(
	iStartYear = 600,
	fileName = "RFC_600AD",
	
	lCivilizations = lCivilizations,
	lTribalVillages = lTribalVillages,
	
	iOwnerBaseCulture = 20,
	
	dGreatPeopleCreated = {
		iChina: 5,
		iIndia: 4,
		iDravidia: 2,
		iKorea: 1,
		iToltecs: 1,
	},
	dGreatGeneralsCreated = {
		iChina: 1,
		iIndia: 1,
	},
	
	lAllGoalsFailed = [iNubia, iIndia, iCelts, iDravidia, iToltecs],
	setupGoals = setupGoals,
	
	greatWall = GreatWall(
		tGraphicsTL = (118, 54),
		tGraphicsBR = (128, 58),
		lGraphicsExceptions = [(118, 55), (118, 56), (118, 57), (118, 58), (119, 55), (119, 56), (119, 57), (119, 58), (120, 55), (120, 56), (120, 57), (120, 58), (121, 56), (121, 57), (121, 58), (122, 56), (122, 57), (122, 58), (123, 58)],
		lClearCulture = [(127, 59), (128, 59), (129, 57), (129, 58)],
		
		lEffectAreas = [((118, 46), (129, 53)), ((124, 54), (128, 58)), ((121, 54), (123, 55)), ((119, 54), (120, 54)), ((123, 56), (123, 57))],
	),
	
	createStartingUnits = createStartingUnits,
)
		
