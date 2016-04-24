# Rhye's and Fall of Civilization - Historical Victory Goals

from CvPythonExtensions import *
from StoredData import sd
from Consts import *
import RFCUtils
import heapq
import Areas

### GLOBALS ###

gc = CyGlobalContext()
utils = RFCUtils.RFCUtils()
localText = CyTranslator()

### CONSTANTS ###

# general constants
lWonders = [i for i in range(iBeginWonders, iNumBuildings)]
lGreatPeople = [iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy]

# first Polynesian goal: settle two out of the following island groups by 800 AD: Hawaii, New Zealand, Marquesas and Easter Island
# second Polynesian goal: settle Hawaii, New Zealand, Marquesas and Easter Island by 1000 AD
tHawaiiTL = (0, 34)
tHawaiiBR = (6, 39)
tNewZealandTL = (119, 4)
tNewZealandBR = (123, 12)
tMarquesasTL = (14, 22)
tMarquesasBR = (16, 24)
tEasterIslandTL = (20, 15)
tEasterIslandBR = (22, 17)

# second Roman goal: control Iberia, Gaul, Britain, Africa, Greece, Asia Minor and Egypt in 320 AD
tFranceTL = (51, 47)

# second Roman goal: control Iberia, Gaul, Britain, Africa, Greece, Asia Minor and Egypt in 320 AD
# second Arabian goal: control or vassalize Spain, the Maghreb, Egypt, Mesopotamia and Persia in 1300 AD
tCarthageTL = (50, 36)
tCarthageBR = (61, 39)

# second Tamil goal: control or vassalize the Deccan and Srivijaya in 1000 AD
tDeccanTL = (88, 28)
tDeccanBR = (94, 36)
tSrivijayaTL = (98, 25)
tSrivijayaBR = (105, 29)

# third Ethiopian goal: allow no European colonies and East and Subequatorial Africa in 1500 AD and 1910 AD
tSomaliaTL = (73, 24)
tSomaliaBR = (77, 29)
tSubeqAfricaTL = (60, 10)
tSubeqAfricaBR = (72, 29)

# third Byzantine goal: control three cities in the Balkans, Northern Africa and the Near East in 1450 AD
tNearEastTL = (69, 37)
tNearEastBR = (76, 45)
tBalkansTL = (64, 40)
tBalkansBR = (68, 47)
tNorthAfricaTL = (58, 32)
tNorthAfricaBR = (71, 38)

# second Japanese goal: control or vassalize Korea, Manchuria, China, Indochina, Indonesia and the Philippines in 1940
tManchuriaTL = (104, 50)
tManchuriaBR = (112, 55)
tKoreaTL = (108, 45)
tKoreaBR = (110, 49)
tChinaTL = (99, 39)
tChinaBR = (107, 49)
tIndochinaTL = (97, 31)
tIndochinaBR = (104, 38)
tIndochinaExceptions = ((103, 38), (104, 37))
tIndonesiaTL = (98, 24)
tIndonesiaBR = (109, 30)
tPhilippinesTL = (108, 30)
tPhilippinesBR = (110, 36)

# first Moorish goal: control three cities in Iberia, the Maghreb and West Africa in 1200 AD
tIberiaTL = (49, 40)
tIberiaBR = (55, 46)
tMaghrebTL = (49, 35)
tMaghrebBR = (58, 39)
tWestAfricaTL = (48, 26)
tWestAfricaBR = (56, 32)

# third Spanish goal: spread Catholicism to 40% and allow no Protestant civilization in Europe in 1700 AD
# second French goal: control 40% of Europe and North America in 1800 AD
tEuropeTL = (44, 40)
tEuropeBR = (68, 65)

# second French goal: control 40% of Europe and North America in 1800 AD
tEasternEuropeTL = (69, 48)
tEasternEuropeBR = (73, 64)

# second French goal: control 40% of Europe and North America in 1800 AD
# first English goal: colonize every continent by 1730 AD
# third Maya goal: make contact with a European civilization before they have discovered America
tNorthAmericaTL = (10, 40)
tNorthAmericaBR = (37, 58)

# first English goal: colonize every continent by 1730 AD
tOceaniaTL = (99, 5)
tOceaniaBR = (123, 28)

# first English goal: colonize every continent by 1730 AD
# third Maya goal: make contact with a European civilization before they have discovered America
tSouthCentralAmericaTL = (13, 3)
tSouthCentralAmericaBR = (41, 39)

# first English goal: colonize every continent by 1730 AD
# third Portuguese goal: control 15 cities in Brazil, Africa and Asia in 1700 AD
tAfricaTL = (45, 10)
tAfricaBR = (76, 39)
tAsiaTL = (73, 29)
tAsiaBR = (121, 64)

# first Russian goal: found seven cities in Siberia by 1700 AD and build the Trans-Siberian Railway by 1920 AD
tSiberiaTL = (82, 50)
tSiberiaBR = (112, 64)
lSiberianCoast = [(109, 50), (109, 51), (110, 51), (111, 51), (112, 52), (114, 54), (113, 55), (111, 54), (111, 55), (110, 55), (110, 58), (111, 58), (112, 59)]

# second Portuguese goal: acquire 12 colonial resources by 1650 AD
lColonialResources = [iBanana, iSpices, iSugar, iCoffee, iTea, iTobacco]

# third Portuguese goal: control 15 cities in Brazil, Africa and Asia in 1700 AD
tBrazilTL = (32, 14)
tBrazilBR = (43, 30)

# third Italian goal: control 65% of the Mediterranean by 1930 AD
tMediterraneanTL = (51, 36)
tMediterraneanBR = (73, 47)
tMediterraneanExceptions = ((51,36),(51,46),(52,46),(53,46),(53,47),(67,47),(67,46),(73,44),(73,45),(72,45),(71,45),(71,44),(70,44),(73,36))

# first Incan goal: build five Tambos and a road along the Andean coast by 1500 AD
lAndeanCoast = [(25, 29), (24, 28), (24, 27), (24, 26), (24, 25), (25, 24), (25, 23), (26, 22), (27, 21), (28, 20), (29, 19), (30, 18), (30, 17), (30, 16), (30, 15), (30, 14)]

# third Incan goal: control 60% of South America in 1700 AD
# second Colombian goal: control South America in 1920 AD
tSAmericaTL = (24, 3)
tSAmericaBR = (43, 32)
tSouthAmericaExceptions = ((24, 31), (25, 32))

# third Holy Roman goal: settle three great artists in Vienna by 1700 AD
# second Turkish goal: control the Eastern Mediterranean, the Black Sea, Cairo, Mecca, Baghdad and Vienna by 1700 AD
tVienna = (62, 49)

# second Turkish goal: control the Eastern Mediterranean, the Black Sea, Cairo, Mecca, Baghdad and Vienna by 1700 AD
tCairo = (69, 34)
tMecca = (75, 33)
tBaghdad = (77, 40)
lEasternMediterranean = [(58, 39), (58, 38), (58, 37), (59, 37), (60, 37), (61, 37), (61, 36), (62, 36), (63, 36), (64, 36), (65, 36), (66, 36), (67, 36), (68, 36), (69, 36), (70, 36), (71, 36), (65, 37), (66, 37), (72, 37), (73, 37), (73, 38), (73, 39), (73, 40), (73, 41), (73, 42), (70, 42), (71, 42), (72, 42), (69, 43), (70, 43), (69, 44), (68, 45), (67, 44), (67, 45), (66, 44), (65, 43), (66, 43), (65, 42), (66, 42), (67, 42), (67, 41), (65, 40), (66, 40)]
lBlackSea = [(69, 44), (70, 44), (71, 44), (71, 45), (72, 45), (73, 45), (73, 44), (74, 44), (75, 44), (76, 44), (76, 45), (76, 46), (76, 47), (75, 47), (74, 48), (75, 48), (72, 48), (74, 49), (73, 49), (71, 49), (69, 49), (69, 50), (70, 50), (71, 50), (72, 50), (73, 50), (68, 49), (68, 48), (67, 45), (67, 46), (67, 47), (67, 48), (68, 45)]

# third Thai goal: allow no foreign powers in South Asia in 1900 AD
tSouthAsiaTL = (88, 24)
tSouthAsiaBR = (110, 38)
lSouthAsianCivs = [iIndia, iTamils, iKhmer, iIndonesia, iMughals, iThailand]

# second Iranian goal: control Mesopotamia, Transoxania and Northwest India in 1750 AD
tSafavidMesopotamiaTL = (75, 39)
tSafavidMesopotamiaBR = (79, 43)
tTransoxaniaTL = (82, 42)
tTransoxaniaBR = (86, 49)
tNWIndiaTL = (85, 36)
tNWIndiaBR = (91, 43)
tNWIndiaExceptions = ((89, 36), (90, 36), (91, 36), (89, 37), (90, 37), (91, 37), (89, 38), (90, 38), (91, 38))

# first American goal: allow no European colonies in North America, Central America and the Caribbean
tNCAmericaTL = (3, 33)
tNCAmericaBR = (37, 63)

# first Colombian goal: allow no European civilizations in Peru, Gran Colombia, Guayanas and the Caribbean in 1870 AD
tPeruTL = (25, 16)
tPeruBR = (32, 24)
tGranColombiaTL = (21, 25)
tGranColombiaBR = (32, 35)
tGuayanasTL = (33, 27)
tGuayanasBR = (37, 31)
tCaribbeanTL = (25, 33)
tCaribbeanBR = (33, 39)

# first Canadian goal: connect your capital to an Atlantic and a Pacific port by 1920 AD
lAtlanticCoast = [(31, 50), (32, 50), (34, 50), (32, 51), (33, 51), (35, 51), (30, 52), (31, 52), (32, 52), (30, 53), (35, 53), (30, 54), (31, 54), (32, 54), (35, 54), (36, 54), (32, 55), (33, 55), (34, 55)]
lPacificCoast = [(11, 51), (10, 52), (11, 53), (10, 56)]

# second Canadian goal: control all cities and 90% of the territory in Canada without ever conquering a city by 1950 AD
tCanadaWestTL = (10, 52)
tCanadaWestBR = (26, 61)
tCanadaWestExceptions = ((10, 59), (10, 60), (10, 61), (21, 61), (22, 61), (23, 61), (24, 61), (25, 61))
tCanadaEastTL = (27, 50)
tCanadaEastBR = (36, 59)
tCanadaEastExceptions = ((30, 50), (31, 50), (32, 50))

### GOAL CONSTANTS ###

dTechGoals = {
	iChina: (1, [iCompass, iPaper, iGunpowder, iPrintingPress]),
	iBabylonia: (0, [iWriting, iCodeOfLaws, iMonarchy]),
	iGreece: (0, [iLiterature, iDrama, iPhilosophy]),
	iRome: (2, [iTheology, iMachinery, iCivilService]),
	iKorea: (1, [iPrintingPress]),
	iPoland: (1, [iLiberalism]),
}

dEraGoals = {
	iEngland: (2, [iIndustrial, iModern]),
}

dWonderGoals = {
	iEgypt: (1, [iPyramids, iGreatLibrary, iGreatLighthouse], True),
	iGreece: (1, [iOracle, iColossus, iParthenon, iTempleOfArtemis], True),
	iPhoenicia: (0, [iGreatCothon], False),
	iPolynesia: (2, [iMoaiStatues], True),
	iMaya: (1, [iTempleOfKukulkan], True),
	iKhmer: (0, [iAngkorWat], False),
	iFrance: (2, [iNotreDame, iVersailles, iStatueOfLiberty, iEiffelTower], True),
	iMali: (1, [iUniversityofSankore], False),
	iItaly: (0, [iSanMarcoBasilica, iSistineChapel, iLeaningTower], True),
	iMughals: (1, [iTajMahal, iRedFort, iHarmandirSahib], True),
	iAmerica: (1, [iStatueOfLiberty, iEmpireStateBuilding, iPentagon, iUnitedNations], True),
	iBrazil: (1, [iWembley, iCristoRedentor, iThreeGorgesDam], True),
}

dReligionGoals = {
	iEthiopia: (0, [iOrthodoxy]),
	iHolyRome: (1, [iProtestantism]),
}
		
### EVENT HANDLING ###

def setup():

	# 1700 AD scenario: handle dates that have already been passed
	if utils.getScenario() == i1700AD:
		for iPlayer in [iChina, iIndia, iTamils, iKorea, iVikings, iSpain, iHolyRome, iPoland, iPortugal, iMughals, iTurkey, iThailand]:
			loseAll(iPlayer)
			
		win(iPersia, 0)
		win(iJapan, 0)
		win(iFrance, 0)
		win(iCongo, 0)
		
		# French goal needs to be winnable
		sd.setWonderBuilder(iNotreDame, iFrance)
		sd.setWonderBuilder(iVersailles, iFrance)
		
		# help Congo
		sd.changeCongoSlaveCounter(500)
		
		# help Netherlands
		sd.changeDutchColonies(2)
	
	# ignore AI goals
	bIgnoreAI = (gc.getDefineINT("NO_AI_UHV_CHECKS") == 1)
	sd.setIgnoreAI(bIgnoreAI)
	
	if bIgnoreAI:
		for iPlayer in range(iNumPlayers):
			if utils.getHumanID() != iPlayer:
				loseAll(iPlayer)
				
def checkTurn(iGameTurn, iPlayer):

	if not gc.getGame().isVictoryValid(7): return
	
	if iPlayer >= iNumPlayers: return
	
	if iGameTurn == utils.getScenarioStartTurn(): return
	
	if not gc.getPlayer(iPlayer).isAlive(): return
	
	# Don't check AI civilizations to improve speed
	if utils.getHumanID() != iPlayer and sd.isIgnoreAI(): return
	
	pPlayer = gc.getPlayer(iPlayer)
	
	if iPlayer == iEgypt:
	
		# first goal: have 500 culture in 850 BC
		if iGameTurn == getTurnForYear(-850):
			if pEgypt.countTotalCulture() >= utils.getTurns(500):
				win(iEgypt, 0)
			else:
				lose(iEgypt, 0)
				
		# first goal: build the Pyramids, the Great Lighthouse and the Great Library by 100 BC
		if iGameTurn == getTurnForYear(-100):
			expire(iEgypt, 1)
				
		# third goal: have 5000 culture in 170 AD
		if iGameTurn == getTurnForYear(170):
			if pEgypt.countTotalCulture() >= utils.getTurns(5000):
				win(iEgypt, 2)
			else:
				lose(iEgypt, 2)
				
	elif iPlayer == iChina:
	
		# first goal: build two Confucian and Taoist Cathedrals by 1000 AD
		if iGameTurn == getTurnForYear(1000):
			expire(iChina, 0)
			
		# second goal: be first to discover Compass, Gunpowder, Paper and Printing Press
		
		# third goal: experience four golden ages by 1800 AD
		if isPossible(iChina, 2):
			if sd.getChineseGoldenAgeTurns() >= utils.getTurns(32):
				win(iChina, 2)
				
			if pChina.isGoldenAge() and not pChina.isAnarchy():
				sd.changeChineseGoldenAgeTurns(1)
				
		if iGameTurn == getTurnForYear(1800):
			expire(iChina, 2)
				
	elif iPlayer == iBabylonia:
	
		# first goal: be the first to discover Writing, Code of Laws and Monarchy
		
		# second goal: make Babylon the most populous city in the world in 850 BC
		if iGameTurn == getTurnForYear(-850):
			if isBestCity(iBabylonia, (76, 40), cityPopulation):
				win(iBabylonia, 1)
			else:
				lose(iBabylonia, 1)
			
		# third goal: make Babylon the most cultured city in the world in 700 BC
		if iGameTurn == getTurnForYear(-700):
			if isBestCity(iBabylonia, (76, 40), cityCulture):
				win(iBabylonia, 2)
			else:
				lose(iBabylonia, 2)
				
	elif iPlayer == iHarappa:
	
		# first goal: establish a trade connection with another civilization by 1600 BC
		if isPossible(iHarappa, 0):
			if isTradeConnected(iHarappa):
				win(iHarappa, 0)
				
		if iGameTurn == getTurnForYear(-1600):
			expire(iHarappa, 0)
			
		# second goal: build three Baths and two Granaries by 1500 BC
		if iGameTurn == getTurnForYear(-1500):
			expire(iHarappa, 1)
			
		# third goal: have a total population of 20 by 800 BC
		if isPossible(iHarappa, 2):
			if pHarappa.getTotalPopulation() >= 20:
				win(iHarappa, 2)
				
		if iGameTurn == getTurnForYear(-800):
			expire(iHarappa, 2)
			
	elif iPlayer == iGreece:
	
		# first goal: be the first to discover Literature, Drama and Philosophy
		
		# second goal: build the Oracle, the Parthenon, the Colossus and the Temple of Artemis by 250 BC
		if iGameTurn == getTurnForYear(-250):
			expire(iGreece, 1)
			
		# third goal: control Egypt, Phoenicia, Babylonia and Persia in 325 BC
		if iGameTurn == getTurnForYear(-325):
			bEgypt = checkOwnedCiv(iGreece, iEgypt)
			bPhoenicia = checkOwnedCiv(iGreece, iPhoenicia)
			bBabylonia = checkOwnedCiv(iGreece, iBabylonia)
			bPersia = checkOwnedCiv(iGreece, iPersia)
			if bEgypt and bPhoenicia and bBabylonia and bPersia:
				win(iGreece, 2)
			else:
				lose(iGreece, 2)
				
	elif iPlayer == iIndia:
	
		# first goal: control the Hindu and Buddhist shrine in 100 BC
		if iGameTurn == getTurnForYear(-100):
			bBuddhistShrine = getNumBuildings(iIndia, iBuddhistShrine) > 0
			bHinduShrine = getNumBuildings(iIndia, iHinduShrine) > 0
			if bHinduShrine and bBuddhistShrine:
				win(iIndia, 0)
			else:
				lose(iIndia, 0)
				
		# second goal: build 20 temples by 700 AD
		if iGameTurn == getTurnForYear(700):
			expire(iIndia, 1)
			
		# third goal: control 20% of the world's population in 1200 AD
		if iGameTurn == getTurnForYear(1200):
			if getPopulationPercent(iIndia) >= 20.0:
				win(iIndia, 2)
			else:
				lose(iIndia, 2)
				
	elif iPlayer == iPhoenicia:
	
		# first goal: build a Palace and the Great Cothon in Carthagee by 300 BC
		if isPossible(iPhoenicia, 0):
			bPalace = isBuildingInCity((58, 39), iPalace)
			bGreatCothon = isBuildingInCity((58, 39), iGreatCothon)
			if bPalace and bGreatCothon:
				win(iPhoenicia, 0)
		
		if iGameTurn == getTurnForYear(-300):
			expire(iPhoenicia, 0)
				
		# second goal: control Italy and Iberia in 100 BC
		if iGameTurn == getTurnForYear(-100):
			bItaly = isControlled(iPhoenicia, utils.getPlotList(Areas.tNormalArea[iItaly], Areas.tNormalArea[iItaly], [(62, 47), (63, 47), (63, 46)]))
			bIberia = isControlled(iPhoenicia, Areas.getNormalArea(iSpain, False))
			if bItaly and bIberia:
				win(iPhoenicia, 1)
			else:
				lose(iPhoenicia, 1)
				
		# third goal: have 5000 gold in 200 AD
		if iGameTurn == getTurnForYear(200):
			if pPhoenicia.getGold() >= utils.getTurns(5000):
				win(iPhoenicia, 2)
			else:
				lose(iPhoenicia, 2)
				
	elif iPlayer == iPolynesia:
	
		# first goal: settle two of the following island groups by 800 AD: Hawaii, New Zealand, Marquesas and Easter Island
		if iGameTurn == getTurnForYear(800):
			expire(iPolynesia, 0)
			
		# second goal: settle Hawaii, New Zealand, Marquesas and Easter Island by 1000 AD
		if iGameTurn == getTurnForYear(1000):
			expire(iPolynesia, 1)
			
		# third goal: build the Moai Statues by 1200 AD
		if iGameTurn == getTurnForYear(1200):
			expire(iPolynesia, 2)
			
	elif iPlayer == iPersia:
	
		# Persia
		if not pPersia.isReborn():
		
			# first goal: control 7% of world territory by 140 AD
			if isPossible(iPersia, 0):
				if getLandPercent(iPersia) >= 6.995:
					win(iPersia, 0)
			
			if iGameTurn == getTurnForYear(140):
				expire(iPersia, 0)
				
			# second goal: control seven wonders by 350 AD
			if isPossible(iPersia, 1):
				if countWonders(iPersia) >= 7:
					win(iPersia, 1)
					
			if iGameTurn == getTurnForYear(350):
				expire(iPersia, 1)
						
			# third goal: control two holy shrines in 350 AD
			if iGameTurn == getTurnForYear(350):
				if countShrines(iPersia) >= 2:
					win(iPersia, 2)
				else:
					lose(iPersia, 2)
					
		# Iran			
		else:
		
			# first goal: have open borders with 6 European civilizations in 1650
			if iGameTurn == getTurnForYear(1650):
				if countOpenBorders(iPersia, lCivGroups[0]) >= 6:
					win(iPersia, 0)
				else:
					lose(iPersia, 0)
					
			# second goal: control Mesopotamia, Transoxania and Northwest India in 1750 AD
			if iGameTurn == getTurnForYear(1750):
				bMesopotamia = isControlled(iPersia, utils.getPlotList(tSafavidMesopotamiaTL, tSafavidMesopotamiaBR))
				bTransoxania = isControlled(iPersia, utils.getPlotList(tTransoxaniaTL, tTransoxaniaBR))
				bNWIndia = isControlled(iPersia, utils.getPlotList(tNWIndiaTL, tNWIndiaBR, tNWIndiaExceptions))
				if bMesopotamia and bTransoxania and bNWIndia:
					win(iPersia, 1)
				else:
					lose(iPersia, 1)
					
			# third goal: have a city with 20000 culture in 1800 AD
			if iGameTurn == getTurnForYear(1800):
				mostCulturedCity = getMostCulturedCity(iPersia)
				if mostCulturedCity.getCulture(iPersia) >= utils.getTurns(20000):
					win(iPersia, 2)
				else:
					lose(iPersia, 2)
					
	elif iPlayer == iRome:
	
		# first goal: build 6 Barracks, 5 Aqueducts, 4 Amphitheatres and 3 Forums by 100 AD
		if isPossible(iRome, 0):
			iNumBarracks = getNumBuildings(iRome, iBarracks)
			iNumAqueducts = getNumBuildings(iRome, iAqueduct)
			iNumAmphitheatres = getNumBuildings(iRome, iAmphitheatre)
			iNumForums = getNumBuildings(iRome, iRomanForum)
			if iNumBarracks >= 6 and iNumAqueducts >= 5 and iNumAmphitheatres >= 4 and iNumForums >= 3:
				win(iRome, 0)
				
		if iGameTurn == getTurnForYear(100):
			expire(iRome, 0)
			
		# second goal: control Iberia, Gaul, Britain, Africa, Greece, Asia Minor and Egypt in 320 AD
		if iGameTurn == getTurnForYear(320):
			bSpain = getNumCitiesInArea(iRome, Areas.getNormalArea(iSpain, False)) >= 2
			bFrance = getNumCitiesInArea(iRome, utils.getPlotList(tFranceTL, Areas.tNormalArea[iFrance][1])) >= 3
			bEngland = getNumCitiesInArea(iRome, Areas.getCoreArea(iEngland, False)) >= 1
			bCarthage = getNumCitiesInArea(iRome, utils.getPlotList(tCarthageTL, tCarthageBR)) >= 2
			bByzantium = getNumCitiesInArea(iRome, Areas.getCoreArea(iByzantium, False)) >= 4
			bEgypt = getNumCitiesInArea(iRome, Areas.getCoreArea(iEgypt, False)) >= 2
			if bSpain and bFrance and bEngland and bCarthage and bByzantium and bEgypt:
				win(iRome, 1)
			else:
				lose(iRome, 1)
					
		# third goal: be first to discover Theology, Machinery and Civil Service
		
	elif iPlayer == iTamils:
	
		# first goal: have 3000 gold and 2000 culture in 800 AD
		if iGameTurn == getTurnForYear(800):
			if pTamils.getGold() >= utils.getTurns(3000) and pTamils.countTotalCulture() >= utils.getTurns(2000):
				win(iTamils, 0)
			else:
				lose(iTamils, 0)
				
		# second goal: control or vassalize the Deccan and Srivijaya in 1000 AD
		if iGameTurn == getTurnForYear(1000):
			bDeccan = isControlledOrVassalized(iTamils, utils.getPlotList(tDeccanTL, tDeccanBR))
			bSrivijaya = isControlledOrVassalized(iTamils, utils.getPlotList(tSrivijayaTL, tSrivijayaBR))
			if bDeccan and bSrivijaya:
				win(iTamils, 1)
			else:
				lose(iTamils, 1)
				
		# third goal: acquire 4000 gold by trade by 1200 AD
		if isPossible(iTamils, 2):
			iTradeGold = 0
			
			# gold from city trade routes
			iTradeCommerce = 0
			for city in utils.getCityList(iTamils):
				iTradeCommerce += city.getTradeYield(2)
			iTradeGold += iTradeCommerce * pTamils.getCommercePercent(0) / 100
			
			# gold from per turn gold trade
			for iPlayer in range(iNumPlayers):
				iTradeGold += pTamils.getGoldPerTurnByPlayer(iPlayer)
				
			sd.changeTamilTradeGold(iTradeGold)
			
			if sd.getTamilTradeGold() >= utils.getTurns(4000):
				win(iTamils, 2)
				
		if iGameTurn == getTurnForYear(1200):
			expire(iTamils, 2)
					
	elif iPlayer == iEthiopia:
	
		# first goal: found Catholicism
		
		# second goal: acquire three incense resources by 600 AD
		if isPossible(iEthiopia, 1):
			if pEthiopia.getNumAvailableBonuses(iIncense) >= 3:
				win(iEthiopia, 1)
				
		if iGameTurn == getTurnForYear(600):
			expire(iEthiopia, 1)
			
		# third goal: allow no European colonies in East and Subequatorial Africa in 1500 AD and 1910 AD
		if iGameTurn == getTurnForYear(1500):
			bEastAfrica = isAreaFreeOfCivs(utils.getPlotList(tSomaliaTL, tSomaliaBR), lCivGroups[0])
			bSubequatorialAfrica = isAreaFreeOfCivs(utils.getPlotList(tSubeqAfricaTL, tSubeqAfricaBR), lCivGroups[0])
			if not bEastAfrica or not bSubequatorialAfrica:
				lose(iEthiopia, 2)
				
		if iGameTurn == getTurnForYear(1910) and isPossible(iEthiopia, 2):
			bEastAfrica = isAreaFreeOfCivs(utils.getPlotList(tSomaliaTL, tSomaliaBR), lCivGroups[0])
			bSubequatorialAfrica = isAreaFreeOfCivs(utils.getPlotList(tSubeqAfricaTL, tSubeqAfricaBR), lCivGroups[0])
			if bEastAfrica and bSubequatorialAfrica:
				win(iEthiopia, 2)
			else:
				lose(iEthiopia, 2)
				
	elif iPlayer == iKorea:
	
		# first goal: build a Buddhist Stupa and a Confucian Academy by 1200 AD
		if iGameTurn == getTurnForYear(1200):
			expire(iKorea, 0)
			
		# second goal: be first to discover Printing Press
		
		# third goal: sink 20 enemy ships
		
	elif iPlayer == iMaya:
	
		# Maya
		if not pMaya.isReborn():
		
			# first goal: discover Calendar by 600 AD
			if iGameTurn == getTurnForYear(600):
				expire(iMaya, 0)
				
			# second goal: build the Temple of Kukulkan by 900 AD
			if iGameTurn == getTurnForYear(900):
				expire(iMaya, 1)
				
			# third goal: make contact with a European civilization before they discover America
			if isPossible(iMaya, 2):
				for iEuropean in lCivGroups[0]:
					if teamMaya.canContact(iEuropean):
						win(iMaya, 2)
						break
			
		# Colombia
		else:
		
			# first goal: allow no European civilizations in Peru, Gran Colombia, the Guayanas and the Caribbean in 1870 AD
			if iGameTurn == getTurnForYear(1870):
				bPeru = isAreaFreeOfCivs(utils.getPlotList(tPeruTL, tPeruBR), lCivGroups[0])
				bGranColombia = isAreaFreeOfCivs(utils.getPlotList(tGranColombiaTL, tGranColombiaBR), lCivGroups[0])
				bGuayanas = isAreaFreeOfCivs(utils.getPlotList(tGuayanasTL, tGuayanasBR), lCivGroups[0])
				bCaribbean = isAreaFreeOfCivs(utils.getPlotList(tCaribbeanTL, tCaribbeanBR), lCivGroups[0])
				if bPeru and bGranColombia and bGuayanas and bCaribbean:
					win(iMaya, 0)
				else:
					lose(iMaya, 0)
					
			# second goal: control South America in 1920 AD
			if iGameTurn == getTurnForYear(1920):
				if isControlled(iMaya, utils.getPlotList(tSAmericaTL, tSAmericaBR, tSouthAmericaExceptions)):
					win(iMaya, 1)
				else:
					lose(iMaya, 1)
			
			# third goal: acquire 3000 gold by selling resources by 1950 AD
			if isPossible(iMaya, 2):
				iTradeGold = 0
				
				for iLoopPlayer in range(iNumPlayers):
					iTradeGold += pMaya.getGoldPerTurnByPlayer(iLoopPlayer)
					
				sd.changeColombianTradeGold(iTradeGold)
				
				if sd.getColombianTradeGold() >= utils.getTurns(3000):
					win(iMaya, 2)
					
			if iGameTurn == getTurnForYear(1950):
				expire(iMaya, 2)
					
	elif iPlayer == iByzantium:
		
		# first goal: have 5000 gold in 1000 AD
		if iGameTurn == getTurnForYear(1000):
			if pByzantium.getGold() >= utils.getTurns(5000):
				win(iByzantium, 0)
			else:
				lose(iByzantium, 0)
				
		# second goal: make Constantinople the world's largest and most cultured city in 1200 AD
		if iGameTurn == getTurnForYear(1200):
			bLargest = isBestCity(iByzantium, (68, 45), cityPopulation)
			bCulture = isBestCity(iByzantium, (68, 45), cityCulture)
			if bLargest and bCulture:
				win(iByzantium, 1)
			else:
				lose(iByzantium, 1)
				
		# third goal: control three cities in the Balkans, Northern Africa and the Near East in 1450 AD
		if iGameTurn == getTurnForYear(1450):
			bBalkans = getNumCitiesInArea(iByzantium, utils.getPlotList(tBalkansTL, tBalkansBR)) >= 3
			bNorthAfrica = getNumCitiesInArea(iByzantium, utils.getPlotList(tNorthAfricaTL, tNorthAfricaBR)) >= 3
			bNearEast = getNumCitiesInArea(iByzantium, utils.getPlotList(tNearEastTL, tNearEastBR)) >= 3
			if bBalkans and bNorthAfrica and bNearEast:
				win(iByzantium, 2)
			else:
				lose(iByzantium, 2)
					
	elif iPlayer == iJapan:
	
		# first goal: have an average culture of 6000 by 1600 AD without ever losing a city
		if isPossible(iJapan, 0):
			if getAverageCulture(iJapan) >= utils.getTurns(6000):
				win(iJapan, 0)
				
		if iGameTurn == getTurnForYear(1600):
			expire(iJapan, 0)
				
		# second goal: control or vassalize Korea, Manchuria, China, Indochina, Indonesia and the Philippines in 1940 AD
		if iGameTurn == getTurnForYear(1940):
			bKorea = isControlledOrVassalized(iJapan, utils.getPlotList(tKoreaTL, tKoreaBR))
			bManchuria = isControlledOrVassalized(iJapan, utils.getPlotList(tManchuriaTL, tManchuriaBR))
			bChina = isControlledOrVassalized(iJapan, utils.getPlotList(tChinaTL, tChinaBR))
			bIndochina = isControlledOrVassalized(iJapan, utils.getPlotList(tIndochinaTL, tIndochinaBR, tIndochinaExceptions))
			bIndonesia = isControlledOrVassalized(iJapan, utils.getPlotList(tIndonesiaTL, tIndonesiaBR))
			bPhilippines = isControlledOrVassalized(iJapan, utils.getPlotList(tPhilippinesTL, tPhilippinesBR))
			if bKorea and bManchuria and bChina and bIndochina and bIndonesia and bPhilippines:
				win(iJapan, 1)
			else:
				lose(iJapan, 1)
				
		# third goal: be the first to complete the tech tree
		
	elif iPlayer == iVikings:
	
		# first goal: control the core of a European civilization in 1050 AD
		if iGameTurn == getTurnForYear(1050):
			lEuroCivs = [iRome, iByzantium, iSpain, iFrance, iEngland, iHolyRome, iRussia]
			if isCoreControlled(iVikings, lEuroCivs):
				win(iVikings, 0)
			else:
				lose(iVikings, 0)
				
		# second goal: found a city in America by 1100 AD
		if iGameTurn == getTurnForYear(1100):
			expire(iVikings, 1)
			
		# third goal: acquire 3000 gold by pillaging, conquering cities and sinking ships by 1500 AD
		if isPossible(iVikings, 2):
			if sd.getVikingGold() >= utils.getTurns(3000):
				win(iVikings, 2)
				
		if iGameTurn == getTurnForYear(1500):
			expire(iVikings, 2)
			
	elif iPlayer == iArabia:
	
		# first goal: be the most advanced civilization in 1300 AD
		if iGameTurn == getTurnForYear(1300):
			if isBestPlayer(iArabia, playerTechs):
				win(iArabia, 0)
			else:
				lose(iArabia, 0)
				
		# second goal: control or vassalize Spain, the Maghreb, Egypt, Mesopotamia and Persia in 1300 AD
		if iGameTurn == getTurnForYear(1300):
			bEgypt = isControlledOrVassalized(iArabia, Areas.getCoreArea(iEgypt, False))
			bMaghreb = isControlledOrVassalized(iArabia, utils.getPlotList(tCarthageTL, tCarthageBR))
			bMesopotamia = isControlledOrVassalized(iArabia, Areas.getCoreArea(iBabylonia, False))
			bPersia = isControlledOrVassalized(iArabia, Areas.getCoreArea(iPersia, False))
			bSpain = isControlledOrVassalized(iArabia, Areas.getNormalArea(iSpain, False))
			if bSpain and bMaghreb and bEgypt and bMesopotamia and bPersia:
				win(iArabia, 1)
			else:
				lose(iArabia, 1)
		
		# third goal: spread Islam to 40% of the cities in the world
		if isPossible(iArabia, 2):
			if gc.getGame().calculateReligionPercent(iIslam) >= 40.0:
				win(iArabia, 2)
				
	elif iPlayer == iTibet:
	
		# first goal: acquire five cities by 1000 AD
		if iGameTurn == getTurnForYear(1000):
			expire(iTibet, 0)
			
		# second goal: spread Buddhism to 30% by 1400 AD
		if isPossible(iTibet, 1):
			if gc.getGame().calculateReligionPercent(iBuddhism) >= 30.0:
				win(iTibet, 1)
				
		if iGameTurn == getTurnForYear(1400):
			expire(iTibet, 1)
			
		# third goal: settle five great prophets in Lhasa by 1700 AD
		if isPossible(iTibet, 2):
			if countCitySpecialists(iTibet, Areas.getCapital(iPlayer), iSpecialistGreatProphet) >= 5:
				win(iTibet, 2)
				
		if iGameTurn == getTurnForYear(1700):
			expire(iTibet, 2)
			
	elif iPlayer == iKhmer:
	
		# first goal: build four Hindu and Buddhist monasteries and Wat Preah Pisnulok by 1200 AD
		if iGameTurn == getTurnForYear(1200):
			expire(iKhmer, 0)
			
		# second goal: have an average city size of 12 by 1450 AD
		if isPossible(iKhmer, 1):
			if getAverageCitySize(iKhmer) >= 12.0:
				win(iKhmer, 1)
				
		if iGameTurn == getTurnForYear(1450):
			expire(iKhmer, 1)
			
		# third goal: have 8000 culture by 1450 AD
		if isPossible(iKhmer, 2):
			if pKhmer.countTotalCulture() >= utils.getTurns(8000):
				win(iKhmer, 2)
				
		if iGameTurn == getTurnForYear(1450):
			expire(iKhmer, 2)
			
	elif iPlayer == iIndonesia:
	
		# first goal: have the largest population in the world in 1300 AD
		if iGameTurn == getTurnForYear(1300):
			if isBestPlayer(iIndonesia, playerRealPopulation):
				win(iIndonesia, 0)
			else:
				lose(iIndonesia, 0)
				
		# second goal: acquire 10 different happiness resources by 1500 AD
		if isPossible(iIndonesia, 1):
			if countHappinessResources(iIndonesia) >= 10:
				win(iIndonesia, 1)
				
		if iGameTurn == getTurnForYear(1500):
			expire(iIndonesia, 1)
		
		# third goal: control 9% of the world's population in 1940 AD
		if iGameTurn == getTurnForYear(1940):
			if calculatePopulationPercent(iIndonesia) >= 9.0:
				win(iIndonesia, 2)
			else:
				lose(iIndonesia, 2)
				
	elif iPlayer == iMoors:
	
		# first goal: control three cities in Iberia, the Maghreb and West Africa in 1200 AD
		if iGameTurn == getTurnForYear(1200):
			bIberia = getNumCitiesInArea(iMoors, utils.getPlotList(tIberiaTL, tIberiaBR)) >= 3
			bMaghreb = getNumCitiesInArea(iMoors, utils.getPlotList(tMaghrebTL, tMaghrebBR)) >= 3
			bWestAfrica = getNumCitiesInArea(iMoors, utils.getPlotList(tWestAfricaTL, tWestAfricaBR)) >= 3
			
			if bIberia and bMaghreb and bWestAfrica:
				win(iMoors, 0)
			else:
				lose(iMoors, 0)
				
		# second goal: settle five great prophets, scientists or engineers in Cordoba by 1300 AD
		if isPossible(iMoors, 1):
			iCounter = 0
			iCounter += countCitySpecialists(iMoors, (51, 41), iSpecialistGreatProphet)
			iCounter += countCitySpecialists(iMoors, (51, 41), iSpecialistGreatScientist)
			iCounter += countCitySpecialists(iMoors, (51, 41), iSpecialistGreatEngineer)
			
			if iCounter >= 5:
				win(iMoors, 1)
				
		if iGameTurn == getTurnForYear(1300):
			expire(iMoors, 1)
				
		# third goal: acquire 3000 gold through piracy by 1650 AD
		if isPossible(iMoors, 2):
			if sd.getMoorishGold() >= utils.getTurns(3000):
				win(iMoors, 2)
				
		if iGameTurn == getTurnForYear(1650):
			expire(iMoors, 2)
			
	elif iPlayer == iSpain:
	
		# first goal: be the first to found a colony in America
		
		# second goal: secure 10 gold or silver resources by 1650 AD
		if isPossible(iSpain, 1):
			iNumGold = countResources(iSpain, iGold)
			iNumSilver = countResources(iSpain, iSilver)
			
			if iNumGold + iNumSilver >= 10:
				win(iSpain, 1)
				
		if iGameTurn == getTurnForYear(1650):
			expire(iSpain, 1)
			
		# third goal: spread Catholicism to 40% and allow no Protestant civilizations in Europe in 1650 AD
		if iGameTurn == getTurnForYear(1650):
			fReligionPercent = gc.getGame().calculateReligionPercent(iCatholicism)
			
			bProtestantsEurope = isStateReligionInArea(iProtestantism, tEuropeTL, tEuropeBR)
			bProtestantsEasternEurope = isStateReligionInArea(iProtestantism, tEasternEuropeTL, tEasternEuropeBR)
			
			if fReligionPercent >= 40.0 and not bProtestantsEurope and not bProtestantsEasternEurope:
				win(iSpain, 2)
			else:
				lose(iSpain, 2)
				
	elif iPlayer == iFrance:
	
		# first goal: have 25000 culture in Paris in 1700 AD
		if iGameTurn == getTurnForYear(1700):
			if getCityCulture(iFrance, (55, 50)) >= utils.getTurns(25000):
				win(iFrance, 0)
			else:
				lose(iFrance, 0)
				
		# second goal: control 40% of Europe and North America in 1800 AD
		if iGameTurn == getTurnForYear(1800):
			iEurope, iTotalEurope = countControlledTiles(iFrance, tEuropeTL, tEuropeBR, True)
			iEasternEurope, iTotalEasternEurope = countControlledTiles(iFrance, tEasternEuropeTL, tEasternEuropeBR, True)
			iNorthAmerica, iTotalNorthAmerica = countControlledTiles(iFrance, tNorthAmericaTL, tNorthAmericaBR, True)
			
			fEurope = (iEurope + iEasternEurope) * 100.0 / (iTotalEurope + iTotalEasternEurope)
			fNorthAmerica = iNorthAmerica * 100.0 / iTotalNorthAmerica
			
			if fEurope >= 40.0 and fNorthAmerica >= 40.0:
				win(iFrance, 1)
			else:
				lose(iFrance, 1)
				
		# third goal: build Notre Dame, Versailles, the Statue of Liberty and the Eiffel Tower by 1900 AD
		if iGameTurn == getTurnForYear(1900):
			expire(iFrance, 2)
			
	elif iPlayer == iEngland:
	
		# first goal: colonize every continent by 1730 AD
		if iGameTurn == getTurnForYear(1730):
			expire(iEngland, 0)
			
		# second goal: control a total of 25 frigates and ships of the line and sink 50 enemy ships by 1800 AD
		if isPossible(iEngland, 1):
			iEnglishNavy = 0
			iEnglishNavy += pEngland.getUnitClassCount(gc.getUnitInfo(iFrigate).getUnitClassType())
			iEnglishNavy += pEngland.getUnitClassCount(gc.getUnitInfo(iShipOfTheLine).getUnitClassType())
			
			if iEnglishNavy >= 25 and sd.getEnglishSinks() >= 50:
				win(iEngland, 1)
		
		if iGameTurn == getTurnForYear(1800):
			expire(iEngland, 1)
			
		# third goal: be the first to enter the Industrial and Modern eras
		
	elif iPlayer == iHolyRome:
	
		# first goal: control Saint Peter's Basilica and the Church of the Anastasis in 1200 AD
		if iGameTurn == getTurnForYear(1200):
			bSaintPeters = getNumBuildings(iHolyRome, iCatholicShrine) > 0
			bAnastasis = getNumBuildings(iHolyRome, iOrthodoxShrine) > 0
			if bSaintPeters and bAnastasis:
				win(iHolyRome, 0)
			else:
				lose(iHolyRome, 0)
				
		# second goal: found Protestantism
		
		# third goal: settle three great artists in Vienna by 1700 AD
		if isPossible(iHolyRome, 2):
			if countCitySpecialists(iHolyRome, tVienna, iSpecialistGreatArtist) >= 3:
				win(iHolyRome, 2)
				
		if iGameTurn == getTurnForYear(1700):
			expire(iHolyRome, 2)
			
	elif iPlayer == iRussia:
	
		# first goal: found seven cities in Siberia by 1700 AD and build the Trans-Siberian Railway by 1920 AD
		if iGameTurn == getTurnForYear(1700):
			if getNumFoundedCitiesInArea(iRussia, utils.getPlotList(tSiberiaTL, tSiberiaBR)) < 7:
				lose(iRussia, 0)
				
		if isPossible(iRussia, 0):
			if teamRussia.isHasTech(iRailroad):
				if isConnectedByRailroad(iRussia, Areas.getCapital(iRussia), lSiberianCoast):
					win(iRussia, 0)
					
		if iGameTurn == getTurnForYear(1920):
			expire(iRussia, 0)
			
		# second goal: be the first civilization to complete the Manhattan Project and the Apollo Program
		
		# third goal: have friendly relations with five communist civilizations by 1950 AD
		if isPossible(iRussia, 2):
			if countPlayersWithAttitudeAndCivic(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY, (3, iCivicCentralPlanning)) >= 5:
				win(iRussia, 2)
				
		if iGameTurn == getTurnForYear(1950):
			expire(iRussia, 2)
			
	elif iPlayer == iMali:
		
		# first goal: conduct a trade mission to your holy city by 1350 AD
		if iGameTurn == getTurnForYear(1350):
			expire(iMali, 0)
			
		# second goal: build the University of Sankore and settle a great prophet in its city by 1500 AD
		if isPossible(iMali, 1):
			for city in utils.getCityList(iMali):
				if city.isHasRealBuilding(iUniversityofSankore) and city.getFreeSpecialistCount(iSpecialistGreatProphet) >= 1:
					win(iMali, 1)
		
		if iGameTurn == getTurnForYear(1500):
			expire(iMali, 1)
			
		# third goal: have 5000 gold in 1500 AD and 15000 gold in 1700 AD
		if iGameTurn == getTurnForYear(1500):
			if pMali.getGold() < utils.getTurns(5000):
				lose(iMali, 2)
				
		if iGameTurn == getTurnForYear(1700) and isPossible(iMali, 2):
			if pMali.getGold() >= utils.getTurns(15000):
				win(iMali, 2)
			else:
				lose(iMali, 2)
				
	elif iPlayer == iPoland:
	
		# first goal: have three cities with a population of 12 by 1400 AD
		if isPossible(iPoland, 0):
			if countCitiesOfSize(iPoland, 12) >= 3:
				win(iPoland, 0)
				
		if iGameTurn == getTurnForYear(1400):
			expire(iPoland, 0)
			
		# second goal: be the first to discover Liberalism
		
		# third goal: build three Christian Cathedrals by 1600 AD
		if iGameTurn == getTurnForYear(1600):
			expire(iPoland, 2)
			
	elif iPlayer == iPortugal:
	
		# first goal: have open borders with 14 civilizations by 1550 AD
		if isPossible(iPortugal, 0):
			if countOpenBorders(iPortugal) >= 14:
				win(iPortugal, 0)
				
		if iGameTurn == getTurnForYear(1550):
			expire(iPortugal, 0)
			
		# second goal: acquire 12 colonial resources by 1650 AD
		if isPossible(iPortugal, 1):
			if countAcquiredResources(iPortugal, lColonialResources) >= 12:
				win(iPortugal, 1)
				
		if iGameTurn == getTurnForYear(1650):
			expire(iPortugal, 1)
			
		# third goal: control 15 cities in Brazil, Africa and Asia in 1700 AD
		if iGameTurn == getTurnForYear(1700):
			iCount = 0
			iCount += getNumCitiesInArea(iPortugal, utils.getPlotList(tBrazilTL, tBrazilBR))
			iCount += getNumCitiesInArea(iPortugal, utils.getPlotList(tAfricaTL, tAfricaBR))
			iCount += getNumCitiesInArea(iPortugal, utils.getPlotList(tAsiaTL, tAsiaBR))
			if iCount >= 15:
				win(iPortugal, 2)
			else:
				lose(iPortugal, 2)
				
	elif iPlayer == iInca:
	
		# first goal: build five Tambos and a road along the Andean coast by 1500 AD
		if isPossible(iInca, 0):
			if isRoad(iInca, lAndeanCoast) and getNumBuildings(iInca, iIncanTambo) >= 5:
				win(iInca, 0)
				
		if iGameTurn == getTurnForYear(1500):
			expire(iInca, 0)
			
		# second goal: have 2500 gold in 1550 AD
		if iGameTurn == getTurnForYear(1550):
			if pInca.getGold() >= utils.getTurns(2500):
				win(iInca, 1)
			else:
				lose(iInca, 1)
			
		# third goal: control 60% of South America in 1700 AD
		if iGameTurn == getTurnForYear(1700):
			iControl, iTotal = countControlledTiles(iInca, tSAmericaTL, tSAmericaBR, False, tSouthAmericaExceptions)
			fControl = iControl * 100.0 / iTotal
			
			if fControl >= 60.0:
				win(iInca, 2)
			else:
				lose(iInca, 2)
				
	elif iPlayer == iItaly:
	
		# first goal: build San Marco Basilica, the Sistine Chapel and the Leaning Tower by 1500 AD
		if iGameTurn == getTurnForYear(1500):
			expire(iItaly, 0)
			
		# second goal: have three cities with influential culture by 1600 AD
		if isPossible(iItaly, 1):
			if countCitiesWithCultureLevel(iItaly, 5) >= 3:
				win(iItaly, 1)
				
		if iGameTurn == getTurnForYear(1600):
			expire(iItaly, 1)
			
		# third goal: control 65% of the Mediterranean by 1930 AD
		if isPossible(iItaly, 2):
			iMediterranean, iTotalMediterranean = countControlledTiles(iItaly, tMediterraneanTL, tMediterraneanBR, False, tMediterraneanExceptions, True)
			fMediterranean = iMediterranean * 100.0 / iTotalMediterranean
			
			if fMediterranean >= 65.0:
				win(iItaly, 2)
				
		if iGameTurn == getTurnForYear(1930):
			expire(iItaly, 2)
			
	elif iPlayer == iMongolia:
	
		# first goal: control China by 1300 AD
		if isPossible(iMongolia, 0):
			if checkOwnedCiv(iMongolia, iChina):
				win(iMongolia, 0)
				
		if iGameTurn == getTurnForYear(1300):
			expire(iMongolia, 0)
			
		# second goal: raze 7 cities
		
		# third goal: control 12% of world territory by 1500 AD
		if isPossible(iMongolia, 2):
			if getLandPercent(iMongolia) >= 11.995:
				win(iMongolia, 2)
				
		if iGameTurn == getTurnForYear(1500):
			expire(iMongolia, 2)
					
	elif iPlayer == iMughals:
	
		# first goal: build three Muslim Cathedrals by 1500 AD
		if iGameTurn == getTurnForYear(1500):
			expire(iMughals, 0)
			
		# second goal: build the Red Fort, Harmandir Sahib and the Taj Mahal by 1660 AD
		if iGameTurn == getTurnForYear(1660):
			expire(iMughals, 1)
			
		# third goal: have more than 50000 culture in 1750 AD
		if iGameTurn == getTurnForYear(1750):
			if pMughals.countTotalCulture() >= utils.getTurns(50000):
				win(iMughals, 2)
			else:
				lose(iMughals, 2)
			
	elif iPlayer == iAztecs:
	
		# Aztecs
		if not pAztecs.isReborn():
		
			# first goal: make Tenochtitlan the largest city in the world in 1520 AD
			if iGameTurn == getTurnForYear(1520):
				if isBestCity(iAztecs, (18, 37), cityPopulation):
					win(iAztecs, 0)
				else:
					lose(iAztecs, 0)
					
			# second goal: build six pagan temples and sacrificial altars by 1650 AD
			if isPossible(iAztecs, 1):
				if getNumBuildings(iAztecs, iPaganTemple) >= 6 and getNumBuildings(iAztecs, iAztecSacrificialAltar) >= 6:
					win(iAztecs, 1)
			
			if iGameTurn == getTurnForYear(1650):
				expire(iAztecs, 1)
				
			# third goal: enslave 20 old world units
			if isPossible(iAztecs, 2):
				if sd.getAztecSlaves() >= 20:
					win(iAztecs, 2)
					
		# Mexico
		else:
		
			# first goal: build three cathedrals of your state religion by 1880 AD
			if iGameTurn == getTurnForYear(1880):
				expire(iAztecs, 0)
				
			# second goal: create three great generals by 1940 AD
			if iGameTurn == getTurnForYear(1940):
				expire(iAztecs, 1)
				
			# third goal: make Mexico City the largest city in the world in 1960 AD
			if iGameTurn == getTurnForYear(1960):
				if isBestCity(iAztecs, (18, 37), cityPopulation):
					win(iAztecs, 2)
				else:
					lose(iAztecs, 2)
				
	elif iPlayer == iTurkey:
	
		# first goal: have four non-obsolete wonders in your capital in 1550 AD
		if iGameTurn == getTurnForYear(1550):
			capital = pTurkey.getCapitalCity()
			if countCityWonders(iTurkey, (capital.getX(), capital.getY()), False) >= 4:
				win(iTurkey, 0)
			else:
				lose(iTurkey, 0)
				
		# second goal: control the Eastern Mediterranean, the Black Sea, Cairo, Mecca, Baghdad and Vienna by 1700 AD
		if isPossible(iTurkey, 1):
			bEasternMediterranean = isCultureControlled(iTurkey, lEasternMediterranean)
			bBlackSea = isCultureControlled(iTurkey, lBlackSea)
			bCairo = controlsCity(iTurkey, tCairo)
			bMecca = controlsCity(iTurkey, tMecca)
			bBaghdad = controlsCity(iTurkey, tBaghdad)
			bVienna = controlsCity(iTurkey, tVienna)
			
			if bEasternMediterranean and bBlackSea and bCairo and bMecca and bBaghdad and bVienna:
				win(iTurkey, 1)
				
		if iGameTurn == getTurnForYear(1700):
			expire(iTurkey, 1)
			
		# third goal: have more culture than all European civilizations combined in 1800 AD
		if iGameTurn == getTurnForYear(1800):
			if pTurkey.countTotalCulture() > getTotalCulture(lCivGroups[0]):
				win(iTurkey, 2)
			else:
				lose(iTurkey, 2)
				
	elif iPlayer == iThailand:
	
		# first goal: have open borders with 10 civilizations by 1650 AD
		if isPossible(iThailand, 0):
			if countOpenBorders(iThailand) >= 10:
				win(iThailand, 0)
				
		if iGameTurn == getTurnForYear(1650):
			expire(iThailand, 0)
			
		# second goal: make Ayutthaya the most populous city in the world in 1700 AD
		if iGameTurn == getTurnForYear(1700):
			if isBestCity(iThailand, (101, 33), cityPopulation) or isBestCity(iThailand, (102, 33), cityPopulation):
				win(iThailand, 1)
			else:
				lose(iThailand, 1)
				
		# third goal: allow no foreign powers in South Asia in 1900 AD
		if iGameTurn == getTurnForYear(1900):
			if isAreaOnlyCivs(tSouthAsiaTL, tSouthAsiaBR, lSouthAsianCivs):
				win(iThailand, 2)
			else:
				lose(iThailand, 2)
				
	elif iPlayer == iCongo:
	
		# first goal: acquire 15% of the votes in the Apostolic Palace by 1650 AD
		if isPossible(iCongo, 0):
			if getApostolicVotePercent(iCongo) >= 15.0:
				win(iCongo, 0)
				
		if iGameTurn == getTurnForYear(1650):
			expire(iCongo, 0)
			
		# second goal: gain 1000 gold through slave trade by 1800 AD
		if iGameTurn == getTurnForYear(1800):
			expire(iCongo, 1)
			
		# third goal: enter the Industrial Era before anyone enters the Modern Era
		
	elif iPlayer == iNetherlands:
	
		# first goal: settle three great merchants in Amsterdam by 1745 AD
		if isPossible(iNetherlands, 0):
			if countCitySpecialists(iNetherlands, Areas.getCapital(iNetherlands), iSpecialistGreatMerchant) >= 3:
				win(iNetherlands, 0)
				
		if iGameTurn == getTurnForYear(1745):
			expire(iNetherlands, 0)
			
		# second goal: conquer four European colonies by 1745 AD
		if iGameTurn == getTurnForYear(1745):
			expire(iNetherlands, 1)
			
		# third goal: secure or get by trade seven spice resources by 1775 AD
		if isPossible(iNetherlands, 2):
			if pNetherlands.getNumAvailableBonuses(iSpices) >= 7:
				win(iNetherlands, 2)
				
		if iGameTurn == getTurnForYear(1775):
			expire(iNetherlands, 2)
			
	elif iPlayer == iGermany:
	
		# first goal: settle seven great people in Berlin in 1900 AD
		if iGameTurn == getTurnForYear(1900):
			iCount = 0
			for iSpecialist in lGreatPeople:
				iCount += countCitySpecialists(iGermany, Areas.getCapital(iGermany), iSpecialist)
			if iCount >= 7:
				win(iGermany, 0)
			else:
				lose(iGermany, 0)
				
		# second goal: control Italy, France, England, Scandinavia and Russia
		if iGameTurn == getTurnForYear(1940):
			bItaly = checkOwnedCiv(iGermany, iItaly)
			bFrance = checkOwnedCiv(iGermany, iFrance)
			bEngland = checkOwnedCiv(iGermany, iEngland)
			bScandinavia = checkOwnedCiv(iGermany, iVikings)
			bRussia = checkOwnedCiv(iGermany, iRussia)
			if bItaly and bFrance and bEngland and bScandinavia and bRussia:
				win(iGermany, 1)
			else:
				lose(iGermany, 0)
				
		# third goal: be the first to complete the tech tree
		
	elif iPlayer == iAmerica:
	
		# first goal: allow no European colonies in North America, Central America and the Caribbean and control or vassalize Mexico in 1930 AD
		if iGameTurn == getTurnForYear(1900):
			if isAreaFreeOfCivs(utils.getPlotList(tNCAmericaTL, tNCAmericaBR), lCivGroups[0]) and isControlledOrVassalized(iAmerica, Areas.getCoreArea(iAztecs, True)):
				win(iAmerica, 0)
			else:
				lose(iAmerica, 0)
				
		# second goal: build the Statue of Liberty, the Empire State Building, the Pentagon and the United Nations by 1950 AD
		if iGameTurn == getTurnForYear(1950):
			expire(iAmerica, 1)
			
		# third goal: secure 10 oil resources by 2000 AD
		if isPossible(iAmerica, 2):
			if countResources(iAmerica, iOil) >= 10:
				win(iAmerica, 2)
				
		if iGameTurn == getTurnForYear(2000):
			expire(iAmerica, 2)
			
	elif iPlayer == iArgentina:
	
		# first goal: experience two golden ages by 1930 AD
		if isPossible(iArgentina, 0):
			if sd.getArgentineGoldenAgeTurns() >= utils.getTurns(16):
				win(iArgentina, 0)
				
		if iGameTurn == getTurnForYear(1930):
			expire(iArgentina, 0)
			
		# second goal: have 25000 culture in Buenos Aires by 1960 AD
		if isPossible(iArgentina, 1):
			if getCityCulture(iArgentina, Areas.getCapital(iArgentina)) >= utils.getTurns(25000):
				win(iArgentina, 1)
				
		if iGameTurn == getTurnForYear(1960):
			expire(iArgentina, 1)
			
		# third goal: experience five golden ages by 2000 AD
		if isPossible(iArgentina, 2):
			if sd.getArgentineGoldenAgeTurns() >= utils.getTurns(40):
				win(iArgentina, 2)
				
		if iGameTurn == getTurnForYear(2000):
			expire(iArgentina, 2)
			
		if pArgentina.isGoldenAge() and not pArgentina.isAnarchy():
			sd.changeArgentineGoldenAgeTurns(1)
			
	elif iPlayer == iBrazil:
	
		# first goal: control 10 slave plantations and 4 pastures in 1880 AD
		if iGameTurn == getTurnForYear(1880):
			if countImprovements(iBrazil, iSlavePlantation) >= 10 and countImprovements(iBrazil, iPasture) >= 4:
				win(iBrazil, 0)
			else:
				lose(iBrazil, 0)
				
		# second goal: build Wembley, Cristo Redentor and the Three Gorges Dam
		
		# third goal: control 20 forest preserves and have a national park in your capital by 1950 AD
		if isPossible(iBrazil, 2):
			if countImprovements(iBrazil, iForestPreserve) >= 20 and pBrazil.getCapitalCity() and pBrazil.getCapitalCity().isHasRealBuilding(iNationalPark):
				win(iBrazil, 2)
				
		if iGameTurn == getTurnForYear(1950):
			expire(iBrazil, 2)
				
	elif iPlayer == iCanada:
	
		# first goal: connect your capital to an Atlantic and a Pacific port by 1920 AD
		if isPossible(iCanada, 0):
			capital = pCanada.getCapitalCity()
			tCapital = (capital.getX(), capital.getY())
			bAtlantic = isConnectedByRailroad(iCanada, tCapital, lAtlanticCoast)
			bPacific = isConnectedByRailroad(iCanada, tCapital, lPacificCoast)
			if bAtlantic and bPacific:
				win(iCanada, 0)
				
		if iGameTurn == getTurnForYear(1920):
			expire(iCanada, 0)
			
		# second goal: control all cities and 90% of the territory in Canada without ever conquering a city by 1950 AD
		if isPossible(iCanada, 1):
			iEast, iTotalEast = countControlledTiles(iCanada, tCanadaEastTL, tCanadaEastBR, False, tCanadaEastExceptions)
			iWest, iTotalWest = countControlledTiles(iCanada, tCanadaWestTL, tCanadaWestBR, False, tCanadaWestExceptions)
			
			fCanada = (iEast + iWest) * 100.0 / (iTotalEast + iTotalWest)
			
			bAllCitiesEast = controlsAllCities(iCanada, tCanadaEastTL, tCanadaEastBR, tCanadaEastExceptions)
			bAllCitiesWest = controlsAllCities(iCanada, tCanadaWestTL, tCanadaWestBR, tCanadaWestExceptions)
			
			if fCanada >= 90.0 and bAllCitiesEast and bAllCitiesWest:
				win(iCanada, 1)
				
		if iGameTurn == getTurnForYear(1950):
			expire(iCanada, 1)
			
		# third goal: end twelve wars through diplomacy by 2000 AD
		if iGameTurn == getTurnForYear(2000):
			expire(iCanada, 2)
			
			
	# check religious victory (human only)
	if utils.getHumanID() == iPlayer:
		iVictoryType = utils.getReligiousVictoryType(iPlayer)
		
		if iVictoryType == iCatholicism:
			if gc.getGame().getSecretaryGeneral(1) == iPlayer:
				sd.changePopeTurns(1)
				
		elif iVictoryType == iHinduism:
			if pPlayer.isGoldenAge():
				sd.changeHinduGoldenAgeTurns(1)
				
		elif iVictoryType == iBuddhism:
			if isAtPeace(iPlayer):
				sd.changeBuddhistPeaceTurns(1)
				
			if isHappiest(iPlayer):
				sd.changeBuddhistHappinessTurns(1)
				
		elif iVictoryType == iTaoism:
			if isHealthiest(iPlayer):
				sd.changeTaoistHealthTurns(1)
				
		elif iVictoryType == iVictoryPolytheism:
			if 2 * countReligionCities(iPlayer) > pPlayer.getNumCities():
				sd.setPolytheismNeverReligion(False)
				
		if checkReligiousGoals(iPlayer):
			gc.getGame().setWinner(iPlayer, 8)
			
def checkHistoricalVictory(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	
	if not sd.isHistoricalGoldenAge(iPlayer):
		if countAchievedGoals(iPlayer) == 2:
		
			sd.setHistoricalGoldenAge(iPlayer, True)
			
			capital = pPlayer.getCapitalCity()
			capital.setHasRealBuilding(iTriumphalArch, True)
			
			if pPlayer.isHuman():
				CyInterface().addMessage(iPlayer, False, iDuration, CyTranslator().getText("TXT_KEY_VICTORY_INTERMEDIATE", ()), "", 0, "", ColorTypes(iPurple), -1, -1, True, True)
				
				for iLoopPlayer in range(iNumPlayers):
					if iLoopPlayer != iPlayer:
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							pLoopPlayer.AI_changeAttitudeExtra(iPlayer, -2)
			
	if gc.getGame().getWinner() == -1:
		if countAchievedGoals(iPlayer) == 3:
			gc.getGame().setWinner(iPlayer, 7)
		
def onCityBuilt(iPlayer, city):

	if not gc.getGame().isVictoryValid(7): return
	
	if utils.getHumanID() != iPlayer and sd.isIgnoreAI(): return
	
	if iPlayer >= iNumPlayers: return
	
	iGameTurn = gc.getGame().getGameTurn()
	
	# record first colony in the Americas for various UHVs
	if not sd.isFirstWorldColonized():
		if utils.isPlotInArea((city.getX(), city.getY()), tAmericasTL, tAmericasBR):
			if iPlayer not in lCivGroups[5]:
				sd.setFirstNewWorldColony(iPlayer)
			
				# second Viking goal: found a city in America by 1100 AD
				if isPossible(iVikings, 1):
					if iPlayer == iVikings:
						win(iVikings, 1)
					else:
						lose(iVikings, 1)
					
				# first Spanish goal: be the first to found a colony in America
				if isPossible(iSpain, 0):
					if iPlayer == iSpain:
						win(iSpain, 0)
					else:
						lose(iSpain, 0)
				
	# first Polynesian goal: settle two of the following island groups by 800 AD: Hawaii, New Zealand, Marquesas, Easter Island
	# second Polynesian goal: control Hawaii, New Zealand, Marquesas and Easter Island by 1000 AD
	if iPlayer == iPolynesia:
		iCount = 0
		if getNumCitiesInArea(iPolynesia, utils.getPlotList(tHawaiiTL, tHawaiiBR)) >= 1: iCount += 1
		if getNumCitiesInArea(iPolynesia, utils.getPlotList(tNewZealandTL, tNewZealandBR)) >= 1: iCount += 1
		if getNumCitiesInArea(iPolynesia, utils.getPlotList(tMarquesasTL, tMarquesasBR)) >= 1: iCount += 1
		if getNumCitiesInArea(iPolynesia, utils.getPlotList(tEasterIslandTL, tEasterIslandBR)) >= 1: iCount += 1
		
		if isPossible(iPolynesia, 0):
			if iCount >= 2:
				win(iPolynesia, 0)
				
		if isPossible(iPolynesia, 1):
			if iCount >= 4:
				win(iPolynesia, 1)
				
	# first Tibetan goal: acquire five cities by 1000 AD
	elif iPlayer == iTibet:
		if isPossible(iTibet, 0):
			if pTibet.getNumCities() >= 5:
				win(iTibet, 0)
					
	# first English goal: colonize every continent by 1730 AD
	elif iPlayer == iEngland:
		if isPossible(iEngland, 0):
			bNAmerica = getNumCitiesInArea(iEngland, utils.getPlotList(tNorthAmericaTL, tNorthAmericaBR)) >= 5
			bSCAmerica = getNumCitiesInArea(iEngland, utils.getPlotList(tSouthCentralAmericaTL, tSouthCentralAmericaBR)) >= 3
			bAfrica = getNumCitiesInArea(iEngland, utils.getPlotList(tAfricaTL, tAfricaBR)) >= 4
			bAsia = getNumCitiesInArea(iEngland, utils.getPlotList(tAsiaTL, tAsiaBR)) >= 5
			bOceania = getNumCitiesInArea(iEngland, utils.getPlotList(tOceaniaTL, tOceaniaBR)) >= 3
			if bNAmerica and bSCAmerica and bAfrica and bAsia and bOceania:
				win(iEngland, 0)
				
def onCityAcquired(iPlayer, iOwner, city, bConquest):

	if not gc.getGame().isVictoryValid(7): return
	
	if utils.getHumanID() != iPlayer and sd.isIgnoreAI(): return
	
	# first Japanese goal: have an average city culture of 6000 by 1600 AD without ever losing a city
	if iOwner == iJapan:
		expire(iJapan, 0)
				
	# first Tibetan goal: acquire five cities by 1000 AD
	if iPlayer == iTibet:
		if isPossible(iTibet, 0):
			if pTibet.getNumCities() >= 5:
				win(iTibet, 0)
					
	# first English goal: colonize every continent by 1730 AD
	elif iPlayer == iEngland:
		if isPossible(iEngland, 0):
			bNAmerica = getNumCitiesInArea(iEngland, utils.getPlotList(tNorthAmericaTL, tNorthAmericaBR)) >= 5
			bSCAmerica = getNumCitiesInArea(iEngland, utils.getPlotList(tSouthCentralAmericaTL, tSouthCentralAmericaBR)) >= 3
			bAfrica = getNumCitiesInArea(iEngland, utils.getPlotList(tAfricaTL, tAfricaBR)) >= 4
			bAsia = getNumCitiesInArea(iEngland, utils.getPlotList(tAsiaTL, tAsiaBR)) >= 5
			bOceania = getNumCitiesInArea(iEngland, utils.getPlotList(tOceaniaTL, tOceaniaBR)) >= 3
			if bNAmerica and bSCAmerica and bAfrica and bAsia and bOceania:
				win(iEngland, 0)
				
	# second Dutch goal: conquer four European colonies by 1745 AD
	elif iPlayer == iNetherlands:
		if isPossible(iNetherlands, 1):
			if iOwner in [iSpain, iFrance, iEngland, iPortugal, iVikings, iItaly, iRussia, iGermany, iHolyRome, iPoland]:
				bColony = city.getRegionID() not in [rBritain, rIberia, rItaly, rBalkans, rEurope, rScandinavia, rRussia]
			
				if bColony and bConquest:
					sd.changeDutchColonies(1)
					if sd.getDutchColonies() >= 4:
						win(iNetherlands, 1)
				
	# second Canadian goal: control all cities and 90% of the territory in Canada by 1950 AD without ever conquering a city
	elif iPlayer == iCanada:
		if bConquest:
			expire(iCanada, 1)
			
def onTechAcquired(iPlayer, iTech):
	if not gc.getGame().isVictoryValid(7): return
	
	if iPlayer >= iNumPlayers: return
	
	iGameTurn = gc.getGame().getGameTurn()
	iEra = gc.getTechInfo(iTech).getEra()
	
	# handle all "be the first to discover" goals
	if not isDiscovered(iTech):
		sd.setFirstDiscovered(iTech, iPlayer)
		
		for iLoopPlayer in dTechGoals.keys():
			iGoal = dTechGoals[iLoopPlayer][0]
			lTechs = dTechGoals[iLoopPlayer][1]
			
			if not isPossible(iLoopPlayer, iGoal): continue
			if iLoopPlayer == iMaya and pMaya.isReborn(): continue
			
			if iTech in lTechs:
				if iPlayer != iLoopPlayer: lose(iLoopPlayer, iGoal)
				elif checkTechGoal(iLoopPlayer, lTechs): win(iLoopPlayer, iGoal)
				
		# third Japanese goal: be the first to discover five modern technologies
		if isPossible(iJapan, 2):
			if countFirstDiscovered(iPlayer, iModern) >= 5:
				if iPlayer == iJapan: win(iJapan, 2)
				else: lose(iJapan, 2)
	
	# handle complete tech tree goals (final tech may not be discovered for the first time)
	if isCompleteTechTree(iPlayer):
				
		# third German goal: be the first to finish the tech tree
		if isPossible(iGermany, 2):
			if iPlayer == iGermany: win(iGermany, 2)
			else: lose(iGermany, 2)
			
	# handle all "be the first to enter" goals
	if not isEntered(iEra):
		sd.setFirstEntered(iEra, iPlayer)
		
		for iLoopPlayer in dEraGoals.keys():
			iGoal = dEraGoals[iLoopPlayer][0]
			lEras = dEraGoals[iLoopPlayer][1]
			
			if not isPossible(iLoopPlayer, iGoal): continue
			
			if iEra in lEras:
				if iPlayer != iLoopPlayer: lose(iLoopPlayer, iGoal)
				elif checkEraGoal(iLoopPlayer, lEras): win(iLoopPlayer, iGoal)
				
	# first Maya goal: discover Calendar by 600 AD
	if iPlayer == iMaya:
		if not pMaya.isReborn() and isPossible(iMaya, 0):
			if iTech == iCalendar:
				win(iMaya, 0)
				
	# third Congolese goal: enter the Industrial era before anyone enters the Modern era
	if isPossible(iCongo, 2):
		if iEra == iIndustrial and iPlayer == iCongo:
			win(iCongo, 2)
		if iEra == iModern and iPlayer != iCongo:
			lose(iCongo, 2)
				
def checkTechGoal(iPlayer, lTechs):
	for iTech in lTechs:
		if sd.getFirstDiscovered(iTech) != iPlayer:
			return False
	return True
	
def checkEraGoal(iPlayer, lEras):
	for iEra in lEras:
		if sd.getFirstEntered(iEra) != iPlayer:
			return False
	return True
	
def onBuildingBuilt(iPlayer, iBuilding):

	if not gc.getGame().isVictoryValid(7): return False
	
	# handle all "build wonders" goals
	if isWonder(iBuilding) and not isWonderBuilt(iBuilding):
		sd.setWonderBuilder(iBuilding, iPlayer)
		
		for iLoopPlayer in dWonderGoals.keys():
			iGoal = dWonderGoals[iLoopPlayer][0]
			lWonders = dWonderGoals[iLoopPlayer][1]
			bCanWin = dWonderGoals[iLoopPlayer][2]
			
			if not isPossible(iLoopPlayer, iGoal): continue
			
			if iBuilding in lWonders:
				if iPlayer != iLoopPlayer: lose(iLoopPlayer, iGoal)
				elif bCanWin and checkWonderGoal(iLoopPlayer, lWonders): win(iLoopPlayer, iGoal)
				
	if utils.getHumanID() != iPlayer and sd.isIgnoreAI(): return
	
	if not gc.getPlayer(iPlayer).isAlive(): return
	
	# first Chinese goal: build two Confucian and Taoist Cathedrals by 1000 AD
	if iPlayer == iChina:
		if isPossible(iChina, 0):
			if iBuilding in [iConfucianCathedral, iTaoistCathedral]:
				iConfucian = getNumBuildings(iChina, iConfucianCathedral)
				iTaoist = getNumBuildings(iChina, iTaoistCathedral)
				if iConfucian >= 2 and iTaoist >= 2:
					win(iChina, 0)
					
	# second Harappan goal: build three Baths and two Granaries by 1500 BC
	elif iPlayer == iHarappa:
		if isPossible(iHarappa, 1):
			if iBuilding in [iHarappanBath, iWalls]:
				iNumBaths = getNumBuildings(iHarappa, iHarappanBath)
				iNumWalls = getNumBuildings(iHarappa, iWalls)
				if iNumBaths >= 3 and iNumWalls >= 2:
					win(iHarappa, 1)
					
	# second Indian goal: build 20 temples by 700 AD
	elif iPlayer == iIndia:
		if isPossible(iIndia, 1):
			lTemples = [iTemple + i*4 for i in range(iNumReligions)]
			if iBuilding in lTemples:
				iCounter = 0
				for iGoalTemple in lTemples:
					iCounter += getNumBuildings(iIndia, iGoalTemple)
				if iCounter >= 20:
					win(iIndia, 1)
					
	# first Korean goal: build a Confucian and a Buddhist Cathedral
	elif iPlayer == iKorea:
		if isPossible(iKorea, 0):
			if iBuilding in [iConfucianCathedral, iBuddhistCathedral]:
				bBuddhist = getNumBuildings(iKorea, iBuddhistCathedral) > 0
				bConfucian = getNumBuildings(iKorea, iConfucianCathedral) > 0
				if bBuddhist and bConfucian:
					win(iKorea, 0)
					
	# first Khmer goal: build four Buddhist and Hindu monasteries and Wat Preah Pisnulok by 1200 AD
	elif iPlayer == iKhmer:
		if isPossible(iKhmer, 0):
			if iBuilding in [iAngkorWat, iBuddhistMonastery, iHinduMonastery]:
				iBuddhist = getNumBuildings(iKhmer, iBuddhistMonastery)
				iHindu = getNumBuildings(iKhmer, iHinduMonastery)
				bAngkorWat = sd.getWonderBuilder(iAngkorWat) == iKhmer
				if iBuddhist >= 4 and iHindu >= 4 and bAngkorWat:
					win(iKhmer, 0)
					
	# third Polish goal: build a total of three Catholic, Orthodox and Protestant Cathedrals by 1600 AD
	elif iPlayer == iPoland:
		if isPossible(iPoland, 2):
			iCatholic = getNumBuildings(iPoland, iCatholicCathedral)
			iOrthodox = getNumBuildings(iPoland, iOrthodoxCathedral)
			iProtestant = getNumBuildings(iPoland, iProtestantCathedral)
			if iCatholic + iOrthodox + iProtestant >= 3:
				win(iPoland, 2)
				
	elif iPlayer == iAztecs:
	
		# second Aztec goal: build 6 pagan temples and sacrificial altars
		if not pAztecs.isReborn():
			if isPossible(iAztecs, 1):
				if iBuilding in [iPaganTemple, iAztecSacrificialAltar]:
					iTemples = getNumBuildings(iAztecs, iPaganTemple)
					iAltars = getNumBuildings(iAztecs, iAztecSacrificialAltar)
					if iTemples >= 6 and iAltars >= 6:
						win(iAztecs, 1)
						
		# first Mexican goal: build three cathedrals of your state religion by 1880 AD
		else:
			if isPossible(iAztecs, 0):
				iStateReligion = pAztecs.getStateReligion()
				if iStateReligion >= 0:
					iStateReligionCathedral = iCathedral + 4 * iStateReligion
					if iBuilding == iStateReligionCathedral:
						if getNumBuildings(iAztecs, iStateReligionCathedral) >= 3:
							win(iAztecs, 0)
	
	# first Mughal goal: build three Islamic Mosques by 1500 AD
	elif iPlayer == iMughals:
		if isPossible(iMughals, 0):
			if iBuilding == iIslamicCathedral:
				if getNumBuildings(iMughals, iIslamicCathedral) >= 3:
					win(iMughals, 0)
		
	# first Incan goal: build 5 tambos and a road along the Andean coast by 1500 AD
	elif iPlayer == iInca:
		if isPossible(iInca, 0):
			if iBuilding == iIncanTambo:
				if isRoad(iInca, lAndeanCoast) and getNumBuildings(iInca, iIncanTambo) >= 5:
					win(iInca, 0)
				
def checkWonderGoal(iPlayer, lWonders):
	for iWonder in lWonders:
		if sd.getWonderBuilder(iWonder) != iPlayer:
			return False
	return True
				
def onReligionFounded(iPlayer, iReligion):

	if not gc.getGame().isVictoryValid(7): return
	
	# handle all "be the first to found" goals
	if not isFounded(iReligion):
		sd.setReligionFounder(iReligion, iPlayer)
		
		for iLoopPlayer in dReligionGoals.keys():
			iGoal = dReligionGoals[iLoopPlayer][0]
			lReligions = dReligionGoals[iLoopPlayer][1]
			
			if not isPossible(iLoopPlayer, iGoal): continue
			
			if iReligion in lReligions:
				if iPlayer != iLoopPlayer: lose(iLoopPlayer, iGoal)
				elif checkReligionGoal(iLoopPlayer, lReligions): win(iLoopPlayer, iGoal)
				
def checkReligionGoal(iPlayer, lReligions):
	for iReligion in lReligions:
		if sd.getReligionFounder(iReligion) != iPlayer:
			return False
	return True
				
def onCityRazed(iPlayer, city):

	if not gc.getGame().isVictoryValid(7): return
	
	if utils.getHumanID() != iPlayer and sd.isIgnoreAI(): return
	
	# second Mongol goal: raze seven cities
	if iPlayer == iMongolia:
		if isPossible(iMongolia, 1):
			sd.changeMongolRazes(1)
			if sd.getMongolRazes() >= 7:
				win(iMongolia, 1)
				
def onProjectBuilt(iPlayer, iProject):

	if not gc.getGame().isVictoryValid(7): return
	
	# second Russian goal: be the first civilization to complete the Manhattan Project and the Apollo Program
	if isPossible(iRussia, 1):
		if iProject in [iApolloProgram, iManhattanProject]:
			if iPlayer == iRussia:
				bApolloProgram = iProject == iApolloProgram or teamRussia.getProjectCount(iApolloProgram) > 0
				bManhattanProject = iProject == iManhattanProject or teamRussia.getProjectCount(iManhattanProject) > 0
				if bApolloProgram and bManhattanProject:
					win(iRussia, 1)
			else:
				lose(iRussia, 1)
				
def onCombatResult(pWinningUnit, pLosingUnit):

	iWinningPlayer = pWinningUnit.getOwner()
	iLosingPlayer = pLosingUnit.getOwner()
	
	if utils.getHumanID() != iWinningPlayer and sd.isIgnoreAI(): return
	
	pLosingUnitInfo = gc.getUnitInfo(pLosingUnit.getUnitType())
	iDomainSea = gc.getInfoTypeForString("DOMAIN_SEA")
	
	# second English goal: control a total of 25 frigates and ships of the line and sink 50 ships in 1800 AD
	if iWinningPlayer == iEngland:
		if isPossible(iEngland, 1):
			if pLosingUnitInfo.getDomainType() == iDomainSea:
				sd.changeEnglishSinks(1)
				
	# third Korean goal: sink 20 enemy ships
	elif iWinningPlayer == iKorea:
		if isPossible(iKorea, 2):
			if pLosingUnitInfo.getDomainType() == iDomainSea:
				sd.changeKoreanSinks(1)
				if sd.getKoreanSinks() >= 20:
					win(iKorea, 2)
					
def onGreatPersonBorn(iPlayer, unit):

	if utils.getHumanID() != iPlayer and sd.isIgnoreAI(): return
	
	pUnitInfo = gc.getUnitInfo(unit.getUnitType())
	
	# second Mexican goal: get three great generals by 1940 AD
	if iPlayer == iAztecs:
		if pAztecs.isReborn() and isPossible(iAztecs, 1):
			if pUnitInfo.getGreatPeoples(iSpecialistGreatGeneral):
				if pAztecs.getGreatGeneralsCreated() >= 3:
					win(iAztecs, 1)
					
def onUnitPillage(iPlayer, iGold, iUnit):

	# third Viking goal: acquire 3000 gold by pillaging, conquering cities and sinking ships by 1500 AD
	if iPlayer == iVikings:
		if isPossible(iVikings, 2):
			sd.changeVikingGold(iGold)
			
	elif iPlayer == iMoors:
		if isPossible(iMoors, 2) and iUnit == iMoorishCorsair:
			sd.changeMoorishGold(iGold)
		
def onCityCaptureGold(iPlayer, iGold):

	# third Viking goal: acquire 3000 gold by pillaging, conquering cities and sinking ships by 1500 AD
	if iPlayer == iVikings:
		if isPossible(iVikings, 2):
			sd.changeVikingGold(iGold)
		
def onPlayerGoldTrade(iPlayer, iGold):

	# third Tamil goal: acquire 4000 gold by trade by 1200 AD
	if iPlayer == iTamils:
		if isPossible(iTamils, 2):
			sd.changeTamilTradeGold(iGold)
		
def onPlayerSlaveTrade(iPlayer, iGold):

	# second Congolese goal: gain 1000 gold through slave trade by 1800 AD
	if iPlayer == iCongo:
		if isPossible(iCongo, 1):
			sd.changeCongoSlaveCounter(iGold)
			if sd.getCongoSlaveCounter() >= utils.getTurns(1000):
				win(iCongo, 1)
				
def onTradeMission(iPlayer, iX, iY, iGold):

	# third Tamil goal: acquire 4000 gold by trade by 1200 AD
	if iPlayer == iTamils:
		sd.changeTamilTradeGold(iGold)
		
	# first Mande goal: conduct a trade mission in your state religion's holy city by 1350 AD
	elif iPlayer == iMali:
		if isPossible(iMali, 0):
			iStateReligion = pMali.getStateReligion()
			if iStateReligion != -1:
				pHolyCity = gc.getGame().getHolyCity(iStateReligion)
				
				if pHolyCity.getX() == iX and pHolyCity.getY() == iY:
					win(iMali, 0)
					
def onPeaceBrokered(iBroker, iPlayer1, iPlayer2):

	# third Canadian goal: end twelve wars through diplomacy by 2000 AD
	if iBroker == iCanada:
		sd.changeCanadianPeaceDeals(1)
		if sd.getCanadianPeaceDeals() >= 12:
			win(iCanada, 2)
			
def onBlockade(iPlayer, iGold):

	# third Moorish goal: acquire 3000 gold through piracy by 1650 AD
	if iPlayer == iMoors:
		if isPossible(iMoors, 2):
			sd.changeMoorishGold(iGold)
			
def onFirstContact(iPlayer, iHasMetPlayer):

	# third Maya goal: make contact with a European civilization before they have discovered America
	if not pMaya.isReborn() and isPossible(iMaya, 2):
		if iPlayer == iMaya or iHasMetPlayer == iMaya:
			if iPlayer == iMaya and iHasMetPlayer in lCivGroups[0]: iEuropean = iHasMetPlayer
			elif iHasMetPlayer == iMaya and iPlayer in lCivGroups[0]: iEuropean = iPlayer
			else: return
		
			for x in range(iWorldX):
				for y in range(iWorldY):
					if utils.isPlotInArea((x, y), tNorthAmericaTL, tNorthAmericaBR) or utils.isPlotInArea((x, y), tSouthCentralAmericaTL, tSouthCentralAmericaBR):
						if gc.getMap().plot(x, y).isRevealed(iEuropean, False):
							lose(iMaya, 2)
							return
			
def checkReligiousGoals(iPlayer):
	for i in range(3):
		if checkReligiousGoal(iPlayer, i) != 1:
			return False
	return True
	
def checkReligiousGoal(iPlayer, iGoal):
	pPlayer = gc.getPlayer(iPlayer)
	iVictoryType = utils.getReligiousVictoryType(iPlayer)
	
	if iVictoryType == -1: return -1
	
	elif iVictoryType == iJudaism:
	
		# first Jewish goal: have a total of 15 Great Prophets, Scientists and Statesmen in Jewish cities
		if iGoal == 0:
			iProphets = countSpecialists(iJudaism, iSpecialistGreatProphet)
			iScientists = countSpecialists(iJudaism, iSpecialistGreatScientist)
			iStatesmen = countSpecialists(iJudaism, iSpecialistGreatStatesman)
			if iProphets + iScientists + iStatesmen >= 15: return 1
		
		# second Jewish goal: have legendary culture in the Jewish holy city
		elif iGoal == 1:
			pHolyCity = gc.getGame().getHolyCity(iJudaism)
			if pHolyCity.getOwner() == iPlayer and pHolyCity.getCultureLevel() >= 6: return 1
			
		# third Jewish goal: have friendly relations with six civilizations with Jewish minorities
		elif iGoal == 2:
			iFriendlyRelations = countPlayersWithAttitudeAndReligion(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY, iJudaism)
			if iFriendlyRelations >= 6: return 1
			
	elif iVictoryType == iOrthodoxy:
	
		# first Orthodox goal: build four Orthodox cathedrals
		if iGoal == 0:
			if getNumBuildings(iPlayer, iOrthodoxCathedral) >= 4: return 1
			
		# second Orthodox goal: make sure the five most cultured cities in the world are Orthodox
		elif iGoal == 1:
			if countBestCitiesReligion(iOrthodoxy, cityCulture, 5) >= 5: return 1
			
		# third Orthodox goal: make sure there are no Catholic civilizations in the world
		elif iGoal == 2:
			if countReligionPlayers(iCatholicism)[0] == 0: return 1
			
	elif iVictoryType == iCatholicism:
	
		# first Catholic goal: be pope for 100 turns
		if iGoal == 0:
			if sd.getPopeTurns() >= utils.getTurns(100): return 1
			
		# second Catholic goal: control the Catholic shrine and make sure 12 great prophets are settled in Catholic civilizations
		elif iGoal == 1:
			bShrine = getNumBuildings(iPlayer, iCatholicShrine) > 0
			iSaints = countReligionSpecialists(iCatholicism, iSpecialistGreatProphet)
			
			if bShrine and iSaints >= 12: return 1
			
		# third Catholic goal: make sure 50% of world territory is controlled by Catholic civilizations
		elif iGoal == 2:
			if getReligiousLand(iCatholicism) >= 50.0: return 1
	
	elif iVictoryType == iProtestantism:
		
		# first Protestant goal: be first to discover Liberalism, Constitution and Economics
		if iGoal == 0:
			lProtestantTechs = [iLiberalism, iConstitution, iEconomics]
			if checkTechGoal(iPlayer, lProtestantTechs): return 1
			elif sd.getFirstDiscovered(iLiberalism) not in [iPlayer, -1] or sd.getFirstDiscovered(iConstitution) not in [iPlayer, -1] or sd.getFirstDiscovered(iEconomics) not in [iPlayer, -1]: return 0
			
		# second Protestant goal: make sure five great merchants and great engineers are settled in Protestant civilizations
		elif iGoal == 1:
			iEngineers = countReligionSpecialists(iProtestantism, iSpecialistGreatEngineer)
			iMerchants = countReligionSpecialists(iProtestantism, iSpecialistGreatMerchant)
			if iEngineers >= 5 and iMerchants >= 5: return 1
			
		# third Protestant goal: make sure at least half of all civilizations are Protestant or Secular
		elif iGoal == 2:
			iProtestantCivs, iTotal = countReligionPlayers(iProtestantism)
			iSecularCivs, iTotal = countCivicPlayers(4, iCivicSecularism)
			
			if 2 * (iProtestantCivs + iSecularCivs) >= iTotal: return 1
			
	elif iVictoryType == iIslam:
	
		# first Muslim goal: spread Islam to 50%
		if iGoal == 0:
			fReligionPercent = gc.getGame().calculateReligionPercent(iIslam)
			if fReligionPercent >= 50.0: return 1
			
		# second Muslim goal: settle seven great people in the Muslim holy city
		elif iGoal == 1:
			iCount = 0
			pHolyCity = gc.getGame().getHolyCity(iIslam)
			for iGreatPerson in lGreatPeople:
				iCount += pHolyCity.getFreeSpecialistCount(iGreatPerson)
			if iCount >= 7: return 1
			
		# third Muslim goal: control five shrines
		elif iGoal == 2:
			iCount = 0
			for iReligion in range(iNumReligions):
				iCount += getNumBuildings(iPlayer, iShrine + 4*iReligion)
			if iCount >= 5: return 1
			
	elif iVictoryType == iHinduism:
	
		# first Hindu goal: settle five different great people in the Hindu holy city
		if iGoal == 0:
			iCount = 0
			pHolyCity = gc.getGame().getHolyCity(iHinduism)
			for iGreatPerson in lGreatPeople:
				if pHolyCity.getFreeSpecialistCount(iGreatPerson) > 0:
					iCount += 1
			if iCount >= 5: return 1
		
		# second Hindu goal: experience 24 turns of golden age
		elif iGoal == 1:
			if sd.getHinduGoldenAgeTurns() >= utils.getTurns(24): return 1
			
		# third Hindu goal: make sure the five largest cities in the world are Hindu
		elif iGoal == 2:
			if countBestCitiesReligion(iHinduism, cityPopulation, 5) >= 5: return 1
			
	elif iVictoryType == iBuddhism:
	
		# first Buddhist goal: be at peace for 100 turns
		if iGoal == 0:
			if sd.getBuddhistPeaceTurns() >= utils.getTurns(100): return 1
			
		# second Buddhist goal: have the highest approval rating for 100 turns
		elif iGoal == 1:
			if sd.getBuddhistHappinessTurns() >= utils.getTurns(100): return 1
			
		# third Buddhist goal: have cautious or better relations with all civilizations in the world
		elif iGoal == 2:
			if countGoodRelationPlayers(iPlayer, AttitudeTypes.ATTITUDE_CAUTIOUS) >= countLivingPlayers()-1: return 1
			
	elif iVictoryType == iConfucianism:
	
		# first Confucian goal: have friendly relations with five civilizations
		if iGoal == 0:
			if countGoodRelationPlayers(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY) >= 5: return 1
			
		# second Confucian goal: have five wonders in the Confucian holy city
		elif iGoal == 1:
			pHolyCity = gc.getGame().getHolyCity(iConfucianism)
			if countCityWonders(iPlayer, (pHolyCity.getX(), pHolyCity.getY()), True) >= 5: return 1
			
		# third Confucian goal: control an army of 200 non-obsolete melee or gunpowder units
		elif iGoal == 2:
			iUnitCombatMelee = gc.getInfoTypeForString("UNITCOMBAT_MELEE")
			iUnitCombatGunpowder = gc.getInfoTypeForString("UNITCOMBAT_GUN")
			if countUnitsOfType(iPlayer, [iUnitCombatMelee, iUnitCombatGunpowder]) >= 200: return 1
			
	elif iVictoryType == iTaoism:
	
		# first Taoist goal: have the highest life expectancy in the world for 100 turns
		if iGoal == 0:
			if sd.getTaoistHealthTurns() >= utils.getTurns(100): return 1
			
		# second Taoist goal: control the Confucian and Taoist shrine and combine their income to 40 gold
		elif iGoal == 1:
			iConfucianIncome = calculateShrineIncome(iPlayer, iConfucianism)
			iTaoistIncome = calculateShrineIncome(iPlayer, iTaoism)
			if getNumBuildings(iPlayer, iConfucianShrine) > 0 and getNumBuildings(iPlayer, iTaoistShrine) > 0 and iConfucianIncome + iTaoistIncome >= 40: return 1
			
		# third Taoist goal: have legendary culture in the Tao holy city
		elif iGoal == 2:
			pHolyCity = gc.getGame().getHolyCity(iTaoism)
			if pHolyCity.getOwner() == iPlayer and pHolyCity.getCultureLevel() >= 6: return 1
		
	elif iVictoryType == iZoroastrianism:

		# first Zoroastrian goal: acquire six incense resources
		if iGoal == 0:
			if pPlayer.getNumAvailableBonuses(iIncense) >= 6: return 1
			
		# second Zoroastrian goal: spread Zoroastrianism to 20%
		if iGoal == 1:
			fReligionPercent = gc.getGame().calculateReligionPercent(iZoroastrianism)
			if fReligionPercent >= 20.0: return 1
			
		# third Zoroastrian goal: have legendary culture in the Zoroastrian holy city
		elif iGoal == 2:
			pHolyCity = gc.getGame().getHolyCity(iZoroastrianism)
			if pHolyCity.getOwner() == iPlayer and pHolyCity.getCultureLevel() >= 6: return 1
			
	elif iVictoryType == iVictoryPolytheism:
	
		# first Polytheist goal: make sure there are 15 pagan temples in the world
		if iGoal == 0:
			if countWorldBuildings(iPaganTemple) >= 15: return 1
			
		# second Polytheist goal: control ten wonders that require no state religion
		elif iGoal == 1:
			if countReligionWonders(iPlayer, -1) >= 10: return 1
			
		# third Polytheist goal: don't allow more than half of your cities to have a religion
		elif iGoal == 2:
			if sd.isPolytheismNeverReligion(): return 1
			
	elif iVictoryType == iVictorySecularism:
	
		# first Secular goal: control the cathedrals of every religion
		if iGoal == 0:
			iCount = 0
			for iReligion in range(iNumReligions):
				if getNumBuildings(iPlayer, iCathedral + 4*iReligion) > 0:
					iCount += 1
			if iCount >= iNumReligions: return 1
			
		# second Secular goal: make sure there are 25 universities, 10 Great Scientists and 10 Great Statesmen in secular civilizations
		elif iGoal == 1:
			iUniversities = countCivicBuildings(4, iCivicSecularism, iUniversity)
			iScientists = countCivicSpecialists(4, iCivicSecularism, iSpecialistGreatScientist)
			iStatesmen = countCivicSpecialists(4, iCivicSecularism, iSpecialistGreatStatesman)
			if iUniversities >= 25 and iScientists >= 10 and iStatesmen >= 10: return 1
			
		# third Secular goal: make sure the five most advanced civilizations are secular
		elif iGoal == 2:
			iCount = 0
			lAdvancedPlayers = utils.getSortedList([iLoopPlayer for iLoopPlayer in range(iNumPlayers) if gc.getPlayer(iLoopPlayer).isAlive() and not utils.isAVassal(iLoopPlayer)], lambda iLoopPlayer: gc.getTeam(iLoopPlayer).getTotalTechValue(), True)
			for iLoopPlayer in lAdvancedPlayers[:5]:
				if gc.getPlayer(iLoopPlayer).getCivics(4) == iCivicSecularism:
					iCount += 1
			if iCount >= 5: return 1
			
	return -1

### UTILITY METHODS ###

def lose(iPlayer, iGoal):
	sd.setGoal(iPlayer, iGoal, 0)
	if utils.getHumanID() == iPlayer:
		utils.show(localText.getText("TXT_KEY_VICTORY_GOAL_FAILED_ANNOUNCE", (iGoal+1,)))
	
def win(iPlayer, iGoal):
	sd.setGoal(iPlayer, iGoal, 1)
	checkHistoricalVictory(iPlayer)
	
def expire(iPlayer, iGoal):
	if isPossible(iPlayer, iGoal): lose(iPlayer, iGoal)
	
def isWon(iPlayer, iGoal):
	return sd.getGoal(iPlayer, iGoal) == 1
	
def isLost(iPlayer, iGoal):
	return sd.getGoal(iPlayer, iGoal) == 0
	
def isPossible(iPlayer, iGoal):
	return sd.getGoal(iPlayer, iGoal) == -1
	
def loseAll(iPlayer):
	for i in range(3): sd.setGoal(iPlayer, i, 0)
	
def countAchievedGoals(iPlayer):
	iCount = 0
	for i in range(3):
		if isWon(iPlayer, i): iCount += 1
	return iCount
	
def isFounded(iReligion):
	return sd.getReligionFounder(iReligion) != -1
	
def isWonderBuilt(iWonder):
	return sd.getWonderBuilder(iWonder) != -1
	
def isDiscovered(iTech):
	return sd.getFirstDiscovered(iTech) != -1
	
def isEntered(iEra):
	return sd.getFirstEntered(iEra) != -1
	
	
def getBestCity(iPlayer, tPlot, function):
	x, y = tPlot
	#if not gc.getMap().plot(x, y).isCity(): return None
	
	bestCity = gc.getMap().plot(x, y).getPlotCity()
	iBestValue = function(bestCity)
	
	for city in utils.getAllCities():
		if function(city) > iBestValue:
			bestCity = city
			iBestValue = function(city)
	
	return bestCity
	
def isBestCity(iPlayer, tPlot, function):
	x, y = tPlot
	city = getBestCity(iPlayer, tPlot, function)
	if not city: return False
	
	return (city.getOwner() == iPlayer and city.getX() == x and city.getY() == y)
	
def cityPopulation(city):
	if not city: return 0
	return city.getPopulation()
	
def cityCulture(city):
	if not city: return 0
	return city.getCulture(city.getOwner())
	
def getBestPlayer(iPlayer, function):
	iBestPlayer = iPlayer
	iBestValue = function(iPlayer)
	
	for iLoopPlayer in range(iNumPlayers):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if function(iLoopPlayer) > iBestValue:
				iBestPlayer = iLoopPlayer
				iBestValue = function(iLoopPlayer)
				
	return iBestPlayer
	
def isBestPlayer(iPlayer, function):
	return getBestPlayer(iPlayer, function) == iPlayer
	
def playerTechs(iPlayer):
	iValue = 0
	for iTech in range(iNumTechs):
		if gc.getTeam(iPlayer).isHasTech(iTech):
			iValue += gc.getTechInfo(iTech).getResearchCost()
	return iValue
	
def playerRealPopulation(iPlayer):
	return gc.getPlayer(iPlayer).getRealPopulation()
	
def getNumBuildings(iPlayer, iBuilding):
	return gc.getPlayer(iPlayer).countNumBuildings(iBuilding)
	
def getPopulationPercent(iPlayer):
	iTotalPopulation = gc.getGame().getTotalPopulation()
	iOurPopulation = gc.getTeam(iPlayer).getTotalPopulation()
	
	if iTotalPopulation <= 0: return 0.0
	
	return iOurPopulation * 100.0 / iTotalPopulation
	
def getLandPercent(iPlayer):
	iTotalLand = gc.getMap().getLandPlots()
	iOurLand = gc.getPlayer(iPlayer).getTotalLand()
	
	if iTotalLand <= 0: return 0.0
	
	return iOurLand * 100.0 / iTotalLand
	
def getReligionLandPercent(iReligion):
	fPercent = 0.0
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive() and pPlayer.getStateReligion() == iReligion:
			fPercent += getLandPercent(iPlayer)
	return fPercent
	
def isBuildingInCity(tPlot, iBuilding):
	x, y = tPlot
	plot = gc.getMap().plot(x, y)
	
	if not plot.isCity(): return False
	
	return plot.getPlotCity().isHasRealBuilding(iBuilding)
	
def getNumCitiesInArea(iPlayer, lPlots):
	return len(utils.getAreaCitiesCiv(iPlayer, lPlots))
	
def getNumFoundedCitiesInArea(iPlayer, lPlots):
	iCount = 0
	for city in utils.getAreaCitiesCiv(iPlayer, lPlots):
		if city.getOriginalOwner() == iPlayer:
			iCount += 1
	return iCount
	
def checkOwnedCiv(iPlayer, iOwnedPlayer):
	iPlayerCities = getNumCitiesInArea(iPlayer, Areas.getNormalArea(iOwnedPlayer, False))
	iOwnedCities = getNumCitiesInArea(iOwnedPlayer, Areas.getNormalArea(iOwnedPlayer, False))
	
	return (iPlayerCities >= 2 and iPlayerCities > iOwnedCities) or (iPlayerCities >= 1 and not gc.getPlayer(iOwnedPlayer).isAlive()) or (iPlayerCities >= 1 and iOwnedPlayer == iPhoenicia)
	
def isControlled(iPlayer, lPlots):
	lOwners = []
	for city in utils.getAreaCities(lPlots):
		iOwner = city.getOwner()
		if iOwner not in lOwners and iOwner < iNumPlayers:
			lOwners.append(iOwner)
	
	return iPlayer in lOwners and len(lOwners) == 1
	
def isControlledOrVassalized(iPlayer, lPlots):
	bControlled = False
	lOwners = []
	lValidOwners = [iPlayer]
	for city in utils.getAreaCities(lPlots):
		iOwner = city.getOwner()
		if iOwner not in lOwners and iOwner < iNumPlayers:
			lOwners.append(iOwner)
	for iLoopPlayer in range(iNumPlayers):
		if gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isVassal(iPlayer):
			lValidOwners.append(iLoopPlayer)
	for iLoopPlayer in lValidOwners:
		if iLoopPlayer in lOwners:
			bControlled = True
			lOwners.remove(iLoopPlayer)
	if len(lOwners):
		bControlled = False
	return bControlled
	
def isCoreControlled(iPlayer, lOtherPlayers):
	for iOtherPlayer in lOtherPlayers:
		if checkOwnedCiv(iPlayer, iOtherPlayer):
			return True
	return False
	
def countControlledTiles(iPlayer, tTopLeft, tBottomRight, bVassals=False, lExceptions=[], bCoastalOnly=False):
	lValidOwners = [iPlayer]
	iCount = 0
	iTotal = 0
	
	if bVassals:
		for iLoopPlayer in range(iNumPlayers):
			if gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isVassal(iPlayer):
				lValidOwners.append(iLoopPlayer)
				
	for (x, y) in utils.getPlotList(tTopLeft, tBottomRight, lExceptions):
		plot = gc.getMap().plot(x, y)
		if plot.isWater(): continue
		if bCoastalOnly and not plot.isCoastalLand(): continue
		iTotal += 1
		if plot.getOwner() in lValidOwners: iCount += 1
		
	return iCount, iTotal
	
def countWonders(iPlayer):
	iCount = 0
	for iWonder in range(iBeginWonders, iNumBuildings):
		iCount += getNumBuildings(iPlayer, iWonder)
	return iCount
	
def countShrines(iPlayer):
	iCount = 0
	for iReligion in range(iNumReligions):
		iCurrentShrine = iShrine + iReligion * 4
		iCount += getNumBuildings(iPlayer, iCurrentShrine)
	return iCount
	
def countOpenBorders(iPlayer, lContacts = [i for i in range(iNumPlayers)]):
	tPlayer = gc.getTeam(iPlayer)
	iCount = 0
	for iContact in lContacts:
		if tPlayer.isOpenBorders(iContact):
			iCount += 1
	return iCount
	
def getMostCulturedCity(iPlayer):
	return utils.getHighestEntry(utils.getCityList(iPlayer), lambda x: x.getCulture(iPlayer))

def isAreaFreeOfCivs(lPlots, lCivs):
	for city in utils.getAreaCities(lPlots):
		if city.getOwner() in lCivs: return False
	return True
	
def isAreaOnlyCivs(tTopLeft, tBottomRight, lCivs):
	for city in utils.getAreaCities(utils.getPlotList(tTopLeft, tBottomRight)):
		iOwner = city.getOwner()
		if iOwner < iNumPlayers and iOwner not in lCivs: return False
	return True
	
def countCitySpecialists(iPlayer, tPlot, iSpecialist):
	x, y = tPlot
	plot = gc.getMap().plot(x, y)
	if not plot.isCity(): return 0
	if plot.getPlotCity().getOwner() != iPlayer: return 0
	
	return plot.getPlotCity().getFreeSpecialistCount(iSpecialist)
	
def countSpecialists(iPlayer, iSpecialist):
	iCount = 0
	for city in utils.getCityList(iPlayer):
		iCount += countCitySpecialists(iPlayer, (city.getX(), city.getY()), iSpecialist)
	return iCount
	
def countReligionSpecialists(iReligion, iSpecialist):
	iCount = 0
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive() and pPlayer.getStateReligion() == iReligion:
			iCount += countSpecialists(iPlayer, iSpecialist)
	return iCount
	
def countCivicSpecialists(iCategory, iCivic, iSpecialist):
	iCount = 0
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive() and pPlayer.getCivics(iCategory) == iCivic:
			iCount += countSpecialists(iPlayer, iSpecialist)
	return iCount
	
def getAverageCitySize(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iNumCities = pPlayer.getNumCities()
	
	if iNumCities == 0: return 0.0
	
	return pPlayer.getTotalPopulation() * 1.0 / iNumCities
	
def getAverageCulture(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iNumCities = pPlayer.getNumCities()
	
	if iNumCities == 0: return 0
	
	return pPlayer.countTotalCulture() / iNumCities
	
def countHappinessResources(iPlayer):
	iCount = 0
	pPlayer = gc.getPlayer(iPlayer)
	for iBonus in range(iNumBonuses):
		if gc.getBonusInfo(iBonus).getHappiness() > 0:
			if pPlayer.getNumAvailableBonuses(iBonus) > 0:
				iCount += 1
	return iCount
	
def calculatePopulationPercent(iPlayer):
	iTotalPopulation = gc.getGame().getTotalPopulation()
	if iTotalPopulation == 0: return 0.0
	
	return 100.0 * gc.getTeam(iPlayer).getTotalPopulation() / iTotalPopulation
	
def countResources(iPlayer, iBonus):
	iNumBonus = 0
	pPlayer = gc.getPlayer(iPlayer)
	
	iNumBonus += pPlayer.getNumAvailableBonuses(iBonus)
	iNumBonus -= pPlayer.getBonusImport(iBonus)
	
	for iLoopPlayer in range(iNumPlayers):
		if iLoopPlayer != iPlayer:
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if pLoopPlayer.isAlive() and gc.getTeam(pLoopPlayer.getTeam()).isVassal(iPlayer):
				iNumBonus += pLoopPlayer.getNumAvailableBonuses(iBonus)
				iNumBonus -= pLoopPlayer.getBonusImport(iBonus)
				
	return iNumBonus
	
def isStateReligionInArea(iReligion, tTopLeft, tBottomRight):
	lPlots = utils.getPlotList(tTopLeft, tBottomRight)
	
	for iPlayer in range(iNumPlayers):
		if gc.getPlayer(iPlayer).getStateReligion() == iReligion:
			for city in utils.getCityList(iPlayer):
				if (city.getX(), city.getY()) in utils.getPlotList(tTopLeft, tBottomRight):
					return True
					
	return False
	
def getCityCulture(iPlayer, tPlot):
	x, y = tPlot
	plot = gc.getMap().plot(x, y)
	if not plot.isCity(): return 0
	if plot.getPlotCity().getOwner() != iPlayer: return 0
	
	return plot.getPlotCity().getCulture(iPlayer)
	
def isConnectedByRailroad(iPlayer, tStart, lTargetList):
	if len(lTargetList) == 0: return False
	
	iStartX, iStartY = tStart
	iTargetX, iTargetY = lTargetList[0]
	startPlot = gc.getMap().plot(iStartX, iStartY)
	
	if not (startPlot.isCity() and startPlot.getOwner() == iPlayer): return False
	
	if tStart in lTargetList: return True
	
	iRailroad = gc.getInfoTypeForString("ROUTE_RAILROAD")
	lNodes = [(utils.calculateDistance(iStartX, iStartY, iTargetX, iTargetY), iStartX, iStartY)]
	heapq.heapify(lNodes)
	lVisitedNodes = []
	
	while len(lNodes) > 0:
		h, x, y = heapq.heappop(lNodes)
		lVisitedNodes.append((h, x, y))
		
		for i in range(x-1, x+2):
			for j in range(y-1, y+2):
				plot = gc.getMap().plot(i, j)
				if plot.getOwner() == iPlayer and (plot.isCity() or plot.getRouteType() == iRailroad):
					if (i, j) in lTargetList: return True
					tTuple = (utils.calculateDistance(i, j, iTargetX, iTargetY), i, j)
					if not tTuple in lVisitedNodes:
						if not tTuple in lNodes:
							heapq.heappush(lNodes, tTuple)
							
	return False
	
def countPlayersWithAttitudeAndCivic(iPlayer, eAttitude, tCivic):
	iCivicType, iCivic = tCivic
	iCount = 0
	for iLoopPlayer in range(iNumPlayers):
		if iLoopPlayer == iPlayer: continue
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.AI_getAttitude(iPlayer) >= eAttitude and pLoopPlayer.getCivics(iCivicType) == iCivic:
			iCount += 1
	return iCount
	
def countPlayersWithAttitudeAndReligion(iPlayer, eAttitude, iReligion):
	iCount = 0
	for iLoopPlayer in range(iNumPlayers):
		if iLoopPlayer == iPlayer: continue
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.AI_getAttitude(iPlayer) >= eAttitude:
			for city in utils.getCityList(iLoopPlayer):
				if city.isHasReligion(iReligion):
					iCount += 1
					break
	return iCount
	
def getLargestCities(iPlayer, iNumCities):
	lCities = utils.getSortedList(utils.getCityList(iPlayer), lambda x: x.getPopulation(), True)
	return lCities[:iNumCities]
	
def countCitiesOfSize(iPlayer, iThreshold):
	iCount = 0
	for city in utils.getCityList(iPlayer):
		if city.getPopulation() >= iThreshold:
			iCount += 1
	return iCount
	
def countCitiesWithCultureLevel(iPlayer, iThreshold):
	iCount = 0
	for city in utils.getCityList(iPlayer):
		if city.getCultureLevel() >= iThreshold:
			iCount += 1
	return iCount
	
def countAcquiredResources(iPlayer, lResources):
	iCount = 0
	pPlayer = gc.getPlayer(iPlayer)
	for iBonus in lResources:
		iCount += pPlayer.getNumAvailableBonuses(iBonus)
	return iCount
	
def isRoad(iPlayer, lPlots):
	iRoad = gc.getInfoTypeForString("ROUTE_ROAD")
	
	for tPlot in lPlots:
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		if plot.getOwner() != iPlayer: return False
		if not plot.getRouteType() == iRoad and not plot.isCity(): return False
		
	return True
	
def countCityWonders(iPlayer, tPlot, bIncludeObsolete=False):
	iCount = 0
	x, y = tPlot
	plot = gc.getMap().plot(x, y)
	if not plot.isCity(): return 0
	if plot.getPlotCity().getOwner() != iPlayer: return 0
	
	for iWonder in lWonders:
		iObsoleteTech = gc.getBuildingInfo(iWonder).getObsoleteTech()
		if not bIncludeObsolete and iObsoleteTech != -1 and gc.getTeam(iPlayer).isHasTech(iObsoleteTech): continue
		if plot.getPlotCity().isHasRealBuilding(iWonder): iCount += 1
		
	return iCount
	
def isCultureControlled(iPlayer, lPlots):
	for tPlot in lPlots:
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		if plot.getOwner() != -1 and plot.getOwner() != iPlayer:
			return False
	return True
	
def controlsCity(iPlayer, tPlot):
	x, y = tPlot
	for i in range(x-1, x+2):
		for j in range(y-1, y+2):
			plot = gc.getMap().plot(i, j)
			if plot.isCity() and plot.getPlotCity().getOwner() == iPlayer:
				return True
	return False
	
def getTotalCulture(lPlayers):
	iTotalCulture = 0
	for iPlayer in lPlayers:
		iTotalCulture += gc.getPlayer(iPlayer).countTotalCulture()
	return iTotalCulture
	
def countImprovements(iPlayer, iImprovement):
	iCount = 0
	for x in range(iWorldX):
		for y in range(iWorldY):
			plot = gc.getMap().plot(x, y)
			if plot.getOwner() == iPlayer and plot.getImprovementType() == iImprovement:
				iCount += 1
	return iCount
	
def controlsAllCities(iPlayer, tTopLeft, tBottomRight, tExceptions=()):
	for city in utils.getAreaCities(utils.getPlotList(tTopLeft, tBottomRight, tExceptions)):
		if city.getOwner() != iPlayer: return False
	return True
	
def isAtPeace(iPlayer):
	for iLoopPlayer in range(iNumPlayers):
		if gc.getPlayer(iLoopPlayer).isAlive() and gc.getTeam(iPlayer).isAtWar(iLoopPlayer):
			return False
	return True
	
def getHappiest():
	lApprovalList = [utils.getApprovalRating(i) for i in range(iNumPlayers)]
	return utils.getHighestIndex(lApprovalList)
	
def isHappiest(iPlayer):
	return getHappiest() == iPlayer
	
def getHealthiest():
	lLifeExpectancyList = [utils.getLifeExpectancyRating(i) for i in range(iNumPlayers)]
	return utils.getHighestIndex(lLifeExpectancyList)
	
def isHealthiest(iPlayer):
	return getHealthiest() == iPlayer
	
def countReligionCities(iPlayer):
	iCount = 0
	for city in utils.getCityList(iPlayer):
		if city.getReligionCount() > 0:
			iCount += 1
	return iCount
	
def isCompleteTechTree(iPlayer):
	if gc.getPlayer(iPlayer).getCurrentEra() < iModern: return False
	
	tPlayer = gc.getTeam(iPlayer)
	for iTech in range(iNumTechs):
		if not (tPlayer.isHasTech(iTech) or tPlayer.getTechCount(iTech) > 0): return False
		
	return True
	
def countFirstDiscovered(iPlayer, iEra):
	iCount = 0
	for iTech in range(iNumTechs):
		if gc.getTechInfo(iTech).getEra() == iEra and sd.getFirstDiscovered(iTech) == iPlayer:
			iCount += 1
	return iCount
	
def isWonder(iBuilding):
	return iBeginWonders <= iBuilding < iNumBuildings
	
def countReligionPlayers(iReligion):
	iReligionPlayers = 0
	iTotalPlayers = 0
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			iTotalPlayers += 1
			if pPlayer.getStateReligion() == iReligion:
				iReligionPlayers += 1
	return iReligionPlayers, iTotalPlayers
	
def countCivicPlayers(iCivicType, iCivic):
	iCivicPlayers = 0
	iTotalPlayers = 0
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			iTotalPlayers += 1
			if pPlayer.getCivics(iCivicType) == iCivic:
				iCivicPlayers += 1
	return iCivicPlayers, iTotalPlayers
	
def countBestCitiesReligion(iReligion, function, iNumCities):
	lCities = []
	for iLoopPlayer in range(iNumPlayers):
		lCities.extend(utils.getCityList(iLoopPlayer))
	lCities = utils.getSortedList(lCities, function, True)
	
	iCount = 0
	for city in lCities[:iNumCities]:
		if city.isHasReligion(iReligion) and gc.getPlayer(city.getOwner()).getStateReligion() == iReligion:
			iCount += 1
			
	return iCount
	
def getReligiousLand(iReligion):
	fLandPercent = 0.0
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive() and pPlayer.getStateReligion() == iReligion:
			fLandPercent += getLandPercent(iPlayer)
	return fLandPercent
	
def countLivingPlayers():
	iCount = 0
	for iPlayer in range(iNumPlayers):
		if gc.getPlayer(iPlayer).isAlive():
			iCount += 1
	return iCount
	
def countGoodRelationPlayers(iPlayer, iAttitudeThreshold):
	iCount = 0
	tPlayer = gc.getTeam(iPlayer)
	for iLoopPlayer in range(iNumPlayers):
		if iPlayer != iLoopPlayer and tPlayer.isHasMet(iLoopPlayer):
			if gc.getPlayer(iLoopPlayer).AI_getAttitude(iPlayer) >= iAttitudeThreshold:
				iCount += 1
	return iCount
	
def countUnitsOfType(iPlayer, lTypes, bIncludeObsolete=False):
	iCount = 0
	pPlayer = gc.getPlayer(iPlayer)
	for iUnit in range(iNumUnits):
		if bIncludeObsolete or pPlayer.canTrain(iUnit, False, False):
			if gc.getUnitInfo(iUnit).getUnitCombatType() in lTypes:
				iUnitClass = gc.getUnitInfo(iUnit).getUnitClassType()
				iCount += pPlayer.getUnitClassCount(iUnitClass)
	return iCount
	
def calculateShrineIncome(iPlayer, iReligion):
	if getNumBuildings(iPlayer, iShrine  + 4*iReligion) == 0: return 0
	
	iThreshold = 20
	if getNumBuildings(iPlayer, iTempleOfSolomon) > 0 and not gc.getTeam(iPlayer).isHasTech(iLiberalism): iThreshold = 40
	
	return min(iThreshold, gc.getGame().countReligionLevels(iReligion))
	
def countWorldBuildings(iBuilding):
	iCount = 0
	for iPlayer in range(iNumPlayers):
		if gc.getPlayer(iPlayer).isAlive():
			iCount += getNumBuildings(iPlayer, utils.getUniqueBuilding(iPlayer, iBuilding))
	return iCount
	
def countReligionWonders(iPlayer, iReligion):
	iCount = 0
	for iWonder in lWonders:
		if gc.getBuildingInfo(iWonder).getPrereqReligion() == iReligion and getNumBuildings(iPlayer, iWonder) > 0:
			iCount += 1
	return iCount
	
def countCivicBuildings(iCivicType, iCivic, iBuilding):
	iCount = 0
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive() and pPlayer.getCivics(iCivicType) == iCivic:
			iCount += getNumBuildings(iPlayer, utils.getUniqueBuilding(iPlayer, iBuilding))
	return iCount
	
def getApostolicVotePercent(iPlayer):
	iTotal = 0
	for iLoopPlayer in range(iNumPlayers):
		iTotal += gc.getPlayer(iLoopPlayer).getVotes(16, 1)
		
	if iTotal == 0: return 0.0
	
	return gc.getPlayer(iPlayer).getVotes(16, 1) * 100.0 / iTotal
	
def countNativeCulture(iPlayer, iPercent):
	iPlayerCulture = 0
	
	for city in utils.getCityList(iPlayer):
		iCulture = city.getCulture(iPlayer)
		iTotal = 0
		
		for iLoopPlayer in range(iNumTotalPlayersB): iTotal += city.getCulture(iLoopPlayer)
		
		if iTotal > 0 and iCulture * 100 / iTotal >= iPercent:
			iPlayerCulture += iCulture
			
	return iPlayerCulture
	
def isTradeConnected(iPlayer):
	for iOtherPlayer in range(iNumPlayers):
		if iPlayer != iOtherPlayer and gc.getPlayer(iPlayer).canContact(iOtherPlayer) and gc.getPlayer(iPlayer).canTradeNetworkWith(iOtherPlayer):
			return True
			
	return False
	
### UHV HELP SCREEN ###

def getIcon(bVal):
	if bVal:
		return u"%c" %(CyGame().getSymbolID(FontSymbols.SUCCESS_CHAR))
	else:
		return u"%c" %(CyGame().getSymbolID(FontSymbols.FAILURE_CHAR))

def getURVHelp(iPlayer, iGoal):
	pPlayer = gc.getPlayer(iPlayer)
	iVictoryType = utils.getReligiousVictoryType(iPlayer)
	aHelp = []

	if checkReligiousGoal(iPlayer, iGoal) == 1:
		aHelp.append(getIcon(True) + localText.getText("TXT_KEY_VICTORY_GOAL_ACCOMPLISHED", ()))
		return aHelp
	elif checkReligiousGoal(iPlayer, iGoal) == 0:
		aHelp.append(getIcon(False) + localText.getText("TXT_KEY_VICTORY_GOAL_FAILED", ()))
		return aHelp
	
	if iVictoryType == iJudaism:
		if iGoal == 0:
			iProphets = countSpecialists(iPlayer, iSpecialistGreatProphet)
			iScientists = countSpecialists(iPlayer, iSpecialistGreatScientist)
			iStatesmen = countSpecialists(iPlayer, iSpecialistGreatStatesman)
			aHelp.append(getIcon(iProphets + iScientists + iStatesmen) + localText.getText("TXT_KEY_VICTORY_JEWISH_SPECIALISTS", (iProphets + iScientists + iStatesmen, 15)))
		elif iGoal == 1:
			holyCity = gc.getGame().getHolyCity(iJudaism)
			aHelp.append(getIcon(holyCity.getOwner() == iPlayer) + localText.getText("TXT_KEY_VICTORY_CONTROL_HOLY_CITY", (holyCity.getName(),)) + ' ' + getIcon(holyCity.getCultureLevel() >= 6) + localText.getText("TXT_KEY_VICTORY_LEGENDARY_CULTURE_CITY", (holyCity.getName(),)))
		elif iGoal == 2:
			iFriendlyRelations = countPlayersWithAttitudeAndReligion(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY, iJudaism)
			aHelp.append(getIcon(iFriendlyRelations >= 6) + localText.getText("TXT_KEY_VICTORY_FRIENDLY_RELIGION", (gc.getReligionInfo(iJudaism).getAdjectiveKey(), iFriendlyRelations, 6)))

	elif iVictoryType == iOrthodoxy:
		if iGoal == 0:
			iOrthodoxCathedrals = getNumBuildings(iPlayer, iOrthodoxCathedral)
			aHelp.append(getIcon(iOrthodoxCathedrals >= 4) + localText.getText("TXT_KEY_VICTORY_ORTHODOX_CATHEDRALS", (iOrthodoxCathedrals, 4)))
		elif iGoal == 1:
			iCultureCities = countBestCitiesReligion(iOrthodoxy, cityCulture, 5)
			aHelp.append(getIcon(iCultureCities >= 5) + localText.getText("TXT_KEY_VICTORY_ORTHODOX_CULTURE_CITIES", (iCultureCities, 5)))
		elif iGoal == 2:
			bNoCatholics = countReligionPlayers(iCatholicism)[0] == 0
			aHelp.append(getIcon(bNoCatholics) + localText.getText("TXT_KEY_VICTORY_NO_CATHOLICS", ()))

	elif iVictoryType == iCatholicism:
		if iGoal == 0:
			iPopeTurns = sd.getPopeTurns()
			aHelp.append(getIcon(iPopeTurns >= utils.getTurns(100)) + localText.getText("TXT_KEY_VICTORY_POPE_TURNS", (iPopeTurns, utils.getTurns(100))))
		elif iGoal == 1:
			bShrine = pPlayer.countNumBuildings(iCatholicShrine) > 0
			iSaints = countReligionSpecialists(iCatholicism, iSpecialistGreatProphet)
			aHelp.append(getIcon(bShrine) + localText.getText("TXT_KEY_BUILDING_CATHOLIC_SHRINE", ()) + ' ' + getIcon(iSaints >= 12) + localText.getText("TXT_KEY_VICTORY_CATHOLIC_SAINTS", (iSaints, 12)))
		elif iGoal == 2:
			fLandPercent = getReligiousLand(iCatholicism)
			aHelp.append(getIcon(fLandPercent >= 50.0) + localText.getText("TXT_KEY_VICTORY_CATHOLIC_WORLD_TERRITORY", (str(u"%.2f%%" % fLandPercent), str(50))))

	elif iVictoryType == iProtestantism:
		if iGoal == 0:
			bLiberalism = sd.getFirstDiscovered(iLiberalism) == iPlayer
			bConstitution = sd.getFirstDiscovered(iConstitution) == iPlayer
			bEconomics = sd.getFirstDiscovered(iEconomics) == iPlayer
			aHelp.append(getIcon(bLiberalism) + localText.getText("TXT_KEY_TECH_LIBERALISM", ()) + ' ' + getIcon(bConstitution) + localText.getText("TXT_KEY_TECH_CONSTITUTION", ()) + ' ' + getIcon(bEconomics) + localText.getText("TXT_KEY_TECH_ECONOMICS", ()))
		elif iGoal == 1:
			iMerchants = countReligionSpecialists(iProtestantism, iSpecialistGreatMerchant)
			iEngineers = countReligionSpecialists(iProtestantism, iSpecialistGreatEngineer)
			aHelp.append(getIcon(iMerchants >= 5) + localText.getText("TXT_KEY_VICTORY_PROTESTANT_MERCHANTS", (iMerchants, 5)) + ' ' + getIcon(iEngineers >= 5) + localText.getText("TXT_KEY_VICTORY_PROTESTANT_ENGINEERS", (iEngineers, 5)))
		elif iGoal == 2:
			iProtestantCivs, iTotal = countReligionPlayers(iProtestantism)
			iSecularCivs, iTotal = countCivicPlayers(4, iCivicSecularism)
			iNumProtestantCivs = iProtestantCivs + iSecularCivs
			aHelp.append(getIcon(2 * iNumProtestantCivs >= iTotal) + localText.getText("TXT_KEY_VICTORY_PROTESTANT_CIVS", (iNumProtestantCivs, iTotal)))

	elif iVictoryType == iIslam:
		if iGoal == 0:
			fReligionPercent = gc.getGame().calculateReligionPercent(iIslam)
			aHelp.append(getIcon(fReligionPercent >= 50.0) + localText.getText("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", (gc.getReligionInfo(iIslam).getTextKey(), str(u"%.2f%%" % fReligionPercent), str(50))))
		elif iGoal == 1:
			iCount = 0
			pHolyCity = gc.getGame().getHolyCity(iIslam)
			for iGreatPerson in lGreatPeople:
				iCount += pHolyCity.getFreeSpecialistCount(iGreatPerson)
			aHelp.append(getIcon(iCount >= 7) + localText.getText("TXT_KEY_VICTORY_CITY_GREAT_PEOPLE", (gc.getGame().getHolyCity(iIslam).getName(), iCount, 7)))
		elif iGoal == 2:
			iCount = 0
			for iReligion in range(iNumReligions):
				iCount += getNumBuildings(iPlayer, iShrine + 4*iReligion)
			aHelp.append(getIcon(iCount >= 5) + localText.getText("TXT_KEY_VICTORY_NUM_SHRINES", (iCount, 5)))

	elif iVictoryType == iHinduism:
		if iGoal == 0:
			iCount = 0
			pHolyCity = gc.getGame().getHolyCity(iHinduism)
			for iGreatPerson in lGreatPeople:
				if pHolyCity.getFreeSpecialistCount(iGreatPerson) > 0:
					iCount += 1
			aHelp.append(getIcon(iCount >= 5) + localText.getText("TXT_KEY_VICTORY_CITY_DIFFERENT_GREAT_PEOPLE", (gc.getGame().getHolyCity(iHinduism).getName(), iCount, 5)))
		elif iGoal == 1:
			iGoldenAgeTurns = sd.getHinduGoldenAgeTurns()
			aHelp.append(getIcon(iGoldenAgeTurns >= utils.getTurns(24)) + localText.getText("TXT_KEY_VICTORY_GOLDEN_AGE_TURNS", (iGoldenAgeTurns, utils.getTurns(24))))
		elif iGoal == 2:
			iLargestCities = countBestCitiesReligion(iHinduism, cityPopulation, 5)
			aHelp.append(getIcon(iLargestCities >= 5) + localText.getText("TXT_KEY_VICTORY_HINDU_LARGEST_CITIES", (iLargestCities, 5)))

	elif iVictoryType == iBuddhism:
		if iGoal == 0:
			iPeaceTurns = sd.getBuddhistPeaceTurns()
			aHelp.append(getIcon(iPeaceTurns >= utils.getTurns(100)) + localText.getText("TXT_KEY_VICTORY_PEACE_TURNS", (iPeaceTurns, utils.getTurns(100))))
		elif iGoal == 1:
			iHappinessTurns = sd.getBuddhistHappinessTurns()
			aHelp.append(getIcon(iHappinessTurns >= utils.getTurns(100)) + localText.getText("TXT_KEY_VICTORY_HAPPINESS_TURNS", (iHappinessTurns, utils.getTurns(100))))
		elif iGoal == 2:
			iGoodRelations = countGoodRelationPlayers(iPlayer, AttitudeTypes.ATTITUDE_CAUTIOUS)
			iTotalPlayers = countLivingPlayers()-1
			aHelp.append(getIcon(iGoodRelations >= iTotalPlayers) + localText.getText("TXT_KEY_VICTORY_CAUTIOUS_OR_BETTER_RELATIONS", (iGoodRelations, iTotalPlayers)))

	elif iVictoryType == iConfucianism:
		if iGoal == 0:
			iFriendlyCivs = countGoodRelationPlayers(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY)
			aHelp.append(getIcon(iFriendlyCivs >= 5) + localText.getText("TXT_KEY_VICTORY_FRIENDLY_CIVS", (iFriendlyCivs, 5)))
		elif iGoal == 1:
			holyCity = gc.getGame().getHolyCity(iConfucianism)
			iCount = countCityWonders(iPlayer, (holyCity.getX(), holyCity.getY()), True)
			aHelp.append(getIcon(holyCity.getOwner() == iPlayer) + localText.getText("TXT_KEY_VICTORY_CONTROL_HOLY_CITY", (holyCity.getName(),)) + ' ' + getIcon(iCount >= 5) + localText.getText("TXT_KEY_VICTORY_HOLY_CITY_WONDERS", (holyCity.getName(), iCount, 5)))
		elif iGoal == 2:
			iUnitCombatMelee = gc.getInfoTypeForString("UNITCOMBAT_MELEE")
			iUnitCombatGunpowder = gc.getInfoTypeForString("UNITCOMBAT_GUN")
			iCount = countUnitsOfType(iPlayer, [iUnitCombatMelee, iUnitCombatGunpowder])
			aHelp.append(getIcon(iCount >= 200) + localText.getText("TXT_KEY_VICTORY_CONTROL_NUM_UNITS", (iCount, 200)))

	elif iVictoryType == iTaoism:
		if iGoal == 0:
			iHealthTurns = sd.getTaoistHealthTurns()
			aHelp.append(getIcon(iHealthTurns >= utils.getTurns(100)) + localText.getText("TXT_KEY_VICTORY_HEALTH_TURNS", (iHealthTurns, utils.getTurns(100))))
		elif iGoal == 1:
			bConfucianShrine = getNumBuildings(iPlayer, iConfucianShrine) > 0
			bTaoistShrine = getNumBuildings(iPlayer, iTaoistShrine) > 0

			iConfucianIncome = calculateShrineIncome(iPlayer, iConfucianism)
			iTaoistIncome = calculateShrineIncome(iPlayer, iTaoism)
			
			aHelp.append(getIcon(bConfucianShrine) + localText.getText("TXT_KEY_BUILDING_CONFUCIAN_SHRINE", ()) + ' ' + getIcon(bTaoistShrine) + localText.getText("TXT_KEY_BUILDING_TAOIST_SHRINE", ()) + ' ' + getIcon(iConfucianIncome + iTaoistIncome >= 40) + localText.getText("TXT_KEY_VICTORY_CHINESE_SHRINE_INCOME", (iConfucianIncome + iTaoistIncome, 40)))
		elif iGoal == 2:
			holyCity = gc.getGame().getHolyCity(iTaoism)
			aHelp.append(getIcon(holyCity.getOwner() == iPlayer) + localText.getText("TXT_KEY_VICTORY_CONTROL_HOLY_CITY", (holyCity.getName(),)) + ' ' + getIcon(holyCity.getCultureLevel() >= 6) + localText.getText("TXT_KEY_VICTORY_LEGENDARY_CULTURE_CITY", (holyCity.getName(),)))

	elif iVictoryType == iZoroastrianism:
		if iGoal == 0:
			iNumIncense = pPlayer.getNumAvailableBonuses(iIncense)
			aHelp.append(getIcon(iNumIncense >= 6) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_INCENSE_RESOURCES", (iNumIncense, 6)))
		elif iGoal == 1:
			fReligionPercent = gc.getGame().calculateReligionPercent(iZoroastrianism)
			aHelp.append(getIcon(fReligionPercent >= 20.0) + localText.getText("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", (gc.getReligionInfo(iZoroastrianism).getTextKey(), str(u"%.2f%%" % fReligionPercent), str(20))))
		elif iGoal == 2:
			holyCity = gc.getGame().getHolyCity(iZoroastrianism)
			aHelp.append(getIcon(holyCity.getOwner() == iPlayer) + localText.getText("TXT_KEY_VICTORY_CONTROL_HOLY_CITY", (holyCity.getName(),)) + ' ' + getIcon(holyCity.getCultureLevel() >= 6) + localText.getText("TXT_KEY_VICTORY_LEGENDARY_CULTURE_CITY", (holyCity.getName(),)))

	elif iVictoryType == iVictoryPolytheism:
		if iGoal == 0:
			iCount = countWorldBuildings(iPaganTemple)
			aHelp.append(getIcon(iCount >= 15) + localText.getText("TXT_KEY_VICTORY_NUM_PAGAN_TEMPLES_WORLD", (iCount, 15)))
		elif iGoal == 1:
			iCount = countReligionWonders(iPlayer, -1)
			aHelp.append(getIcon(iCount >= 10) + localText.getText("TXT_KEY_VICTORY_NUM_NONRELIGIOUS_WONDERS", (iCount, 10)))
		elif iGoal == 2:
			bPolytheismNeverReligion = sd.isPolytheismNeverReligion()
			aHelp.append(getIcon(bPolytheismNeverReligion) + localText.getText("TXT_KEY_VICTORY_POLYTHEISM_NEVER_RELIGION", ()))

	elif iVictoryType == iVictorySecularism:
		if iGoal == 0:
			iCount = 0
			for iReligion in range(iNumReligions):
				if getNumBuildings(iPlayer, iCathedral + 4 * iReligion) > 0:
					iCount += 1
			aHelp.append(getIcon(iCount >= iNumReligions) + localText.getText("TXT_KEY_VICTORY_DIFFERENT_CATHEDRALS", (iCount, iNumReligions)))
		elif iGoal == 1:
			iUniversities = countCivicBuildings(4, iCivicSecularism, iUniversity)
			iScientists = countCivicSpecialists(4, iCivicSecularism, iSpecialistGreatScientist)
			iStatesmen = countCivicSpecialists(4, iCivicSecularism, iSpecialistGreatStatesman)
			aHelp.append(getIcon(iUniversities >= 25) + localText.getText("TXT_KEY_VICTORY_SECULAR_UNIVERSITIES", (iUniversities, 25)))
			aHelp.append(getIcon(iScientists >= 10) + localText.getText("TXT_KEY_VICTORY_SECULAR_SCIENTISTS", (iScientists, 10)) + ' ' + getIcon(iStatesmen >= 10) + localText.getText("TXT_KEY_VICTORY_SECULAR_STATESMEN", (iStatesmen, 10)))
		elif iGoal == 2:
			sString = ""
			lAdvancedPlayers = utils.getSortedList([iLoopPlayer for iLoopPlayer in range(iNumPlayers) if gc.getPlayer(iLoopPlayer).isAlive() and not utils.isAVassal(iLoopPlayer)], lambda iLoopPlayer: gc.getTeam(iLoopPlayer).getTotalTechValue(), True)
			for iLoopPlayer in lAdvancedPlayers[:5]:
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				sString += getIcon(pLoopPlayer.getCivics(4) == iCivicSecularism) + pLoopPlayer.getCivilizationShortDescription(0) + ' '
			aHelp.append(sString)
				
	return aHelp

def getUHVHelp(iPlayer, iGoal):
	"Returns an array of help strings used by the Victory Screen table"

	aHelp = [];

	# the info is outdated or irrelevant once the goal has been accomplished or failed
	if sd.getGoal(iPlayer, iGoal) == 1:
		aHelp.append(getIcon(True) + localText.getText("TXT_KEY_VICTORY_GOAL_ACCOMPLISHED", ()))
		return aHelp
	elif sd.getGoal(iPlayer, iGoal) == 0:
		aHelp.append(getIcon(False) + localText.getText("TXT_KEY_VICTORY_GOAL_FAILED", ()))
		return aHelp

	if iPlayer == iEgypt:
		if iGoal == 0:
			iCulture = pEgypt.countTotalCulture()
			aHelp.append(getIcon(iCulture >= utils.getTurns(500)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(500))))
		elif iGoal == 1:
			bPyramids = sd.getWonderBuilder(iPyramids) == iEgypt
			bLibrary = sd.getWonderBuilder(iGreatLibrary) == iEgypt
			bLighthouse = sd.getWonderBuilder(iGreatLighthouse) == iEgypt
			aHelp.append(getIcon(bPyramids) + localText.getText("TXT_KEY_BUILDING_PYRAMIDS", ()) + getIcon(bLibrary) + localText.getText("TXT_KEY_BUILDING_GREAT_LIBRARY", ()) + getIcon(bLighthouse) + localText.getText("TXT_KEY_BUILDING_GREAT_LIGHTHOUSE", ()))
		elif iGoal == 2:
			iCulture = pEgypt.countTotalCulture()
			aHelp.append(getIcon(iCulture >= utils.getTurns(5000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(5000))))
			
	elif iPlayer == iChina:
		if iGoal == 0:
			iConfucianCounter = getNumBuildings(iChina, iConfucianCathedral)
			iTaoistCounter = getNumBuildings(iChina, iTaoistCathedral)
			aHelp.append(getIcon(iConfucianCounter >= 2) + localText.getText("TXT_KEY_VICTORY_NUM_CONFUCIAN_ACADEMIES", (iConfucianCounter, 2)) + ' ' + getIcon(iTaoistCounter >= 2) + localText.getText("TXT_KEY_VICTORY_NUM_TAOIST_PAGODAS", (iTaoistCounter, 2)))
		elif iGoal == 1:
			bCompass = sd.getFirstDiscovered(iCompass) == iChina
			bPaper = sd.getFirstDiscovered(iPaper) == iChina
			bGunpowder = sd.getFirstDiscovered(iGunpowder) == iChina
			bPrintingPress = sd.getFirstDiscovered(iPrintingPress) == iChina
			aHelp.append(getIcon(bCompass) + localText.getText("TXT_KEY_TECH_COMPASS", ()) + ' ' + getIcon(bPaper) + localText.getText("TXT_KEY_TECH_PAPER", ()) + ' ' + getIcon(bGunpowder) + localText.getText("TXT_KEY_TECH_GUNPOWDER", ()) + ' ' + getIcon(bPrintingPress) + localText.getText("TXT_KEY_TECH_PRINTING_PRESS", ()))
		elif iGoal == 2:
			iGoldenAgeTurns = sd.getChineseGoldenAgeTurns()
			aHelp.append(getIcon(iGoldenAgeTurns >= utils.getTurns(32)) + localText.getText("TXT_KEY_VICTORY_GOLDEN_AGES", (iGoldenAgeTurns / utils.getTurns(8), 4)))

	elif iPlayer == iHarappa:
		if iGoal == 1:
			iNumBaths = getNumBuildings(iHarappa, iHarappanBath)
			iNumWalls = getNumBuildings(iHarappa, iWalls)
			aHelp.append(getIcon(iNumBaths >= 3) + localText.getText("TXT_KEY_VICTORY_NUM_BATHS", (iNumBaths, 3)) + ' ' + getIcon(iNumWalls >= 2) + localText.getText("TXT_KEY_VICTORY_NUM_WALLS", (iNumWalls, 2)))
		elif iGoal == 2:
			iNumPopulation = pHarappa.getTotalPopulation()
			aHelp.append(getIcon(iNumPopulation >= 20) + localText.getText("TXT_KEY_VICTORY_TOTAL_POPULATION", (iNumPopulation, 20)))
			
	elif iPlayer == iBabylonia:
		if iGoal == 0:
			bWriting = sd.getFirstDiscovered(iWriting) == iBabylonia
			bCodeOfLaws = sd.getFirstDiscovered(iCodeOfLaws) == iBabylonia
			bMonarchy = sd.getFirstDiscovered(iMonarchy) == iBabylonia
			aHelp.append(getIcon(bWriting) + localText.getText("TXT_KEY_TECH_WRITING", ()) + ' ' + getIcon(bCodeOfLaws) + localText.getText("TXT_KEY_TECH_CODE_OF_LAWS", ()) + ' ' + getIcon(bMonarchy) + localText.getText("TXT_KEY_TECH_MONARCHY", ()))
		elif iGoal == 1:
			pBestCity = getBestCity(iBabylonia, (76, 40), cityPopulation)
			bBestCity = isBestCity(iBabylonia, (76, 40), cityPopulation)
			aHelp.append(getIcon(bBestCity) + localText.getText("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", (pBestCity.getName(),)))
		elif iGoal == 2:
			pBestCity = getBestCity(iBabylonia, (76, 40), cityCulture)
			bBestCity = isBestCity(iBabylonia, (76, 40), cityCulture)
			aHelp.append(getIcon(bBestCity) + localText.getText("TXT_KEY_VICTORY_MOST_CULTURED_CITY", (pBestCity.getName(),)))

	elif iPlayer == iGreece:
		if iGoal == 0:
			bLiterature = sd.getFirstDiscovered(iLiterature) == iGreece
			bDrama = sd.getFirstDiscovered(iDrama) == iGreece
			bPhilosophy = sd.getFirstDiscovered(iPhilosophy) == iGreece
			aHelp.append(getIcon(bLiterature) + localText.getText("TXT_KEY_TECH_LITERATURE", ()) + ' ' + getIcon(bDrama) + localText.getText("TXT_KEY_TECH_DRAMA", ()) + ' ' + getIcon(bPhilosophy) + localText.getText("TXT_KEY_TECH_PHILOSOPHY", ()))
		elif iGoal == 1:
			bOracle = (getNumBuildings(iGreece, iOracle) > 0)
			bParthenon = (getNumBuildings(iGreece, iParthenon) > 0)
			bColossus = (getNumBuildings(iGreece, iColossus) > 0)
			bArtemis = (getNumBuildings(iGreece, iTempleOfArtemis) > 0)
			aHelp.append(getIcon(bOracle) + localText.getText("TXT_KEY_BUILDING_ORACLE", ()) + ' ' + getIcon(bParthenon) + localText.getText("TXT_KEY_BUILDING_PARTHENON", ()) + ' ' + getIcon(bColossus) + localText.getText("TXT_KEY_BUILDING_COLOSSUS", ()) + ' ' + getIcon(bArtemis) + localText.getText("TXT_KEY_BUILDING_TEMPLE_OF_ARTEMIS", ()))
		elif iGoal == 2:
			bEgypt = checkOwnedCiv(iGreece, iEgypt)
			bPhoenicia = checkOwnedCiv(iGreece, iPhoenicia)
			bBabylonia = checkOwnedCiv(iGreece, iBabylonia)
			bPersia = checkOwnedCiv(iGreece, iPersia)
			aHelp.append(getIcon(bEgypt) + localText.getText("TXT_KEY_CIV_EGYPT_SHORT_DESC", ()) + ' ' + getIcon(bPhoenicia) + localText.getText("TXT_KEY_CIV_PHOENICIA_SHORT_DESC", ()) + ' ' + getIcon(bBabylonia) + localText.getText("TXT_KEY_CIV_BABYLONIA_SHORT_DESC", ()) + ' ' + getIcon(bPersia) + localText.getText("TXT_KEY_CIV_PERSIA_SHORT_DESC", ()))

	elif iPlayer == iIndia:
		if iGoal == 0:
			bBuddhistShrine = (getNumBuildings(iIndia, iBuddhistShrine) > 0)
			bHinduShrine = (getNumBuildings(iIndia, iHinduShrine) > 0)
			aHelp.append(getIcon(bHinduShrine) + localText.getText("TXT_KEY_VICTORY_HINDU_SHRINE", ()) + ' ' + getIcon(bBuddhistShrine) + localText.getText("TXT_KEY_VICTORY_BUDDHIST_SHRINE", ()))
		elif iGoal == 1:
			lTemples = [iTemple + 4 * i for i in range(iNumReligions)]
			iCounter = 0
			for iGoalTemple in lTemples:
				iCounter += getNumBuildings(iIndia, iGoalTemple)
			aHelp.append(getIcon(iCounter >= 20) + localText.getText("TXT_KEY_VICTORY_TEMPLES_BUILT", (iCounter, 20)))
		elif iGoal == 2:
			popPercent = getPopulationPercent(iIndia)
			aHelp.append(getIcon(popPercent >= 20.0) + localText.getText("TXT_KEY_VICTORY_PERCENTAGE_WORLD_POPULATION", (str(u"%.2f%%" % popPercent), str(20))))

	elif iPlayer == iPhoenicia:
		if iGoal == 0:
			bPalace = isBuildingInCity((58, 39), iPalace)
			bGreatCothon = isBuildingInCity((58, 39), iGreatCothon)
			aHelp.append(getIcon(bPalace) + localText.getText("TXT_KEY_BUILDING_PALACE", ()) + ' ' + getIcon(bGreatCothon) + localText.getText("TXT_KEY_BUILDING_GREAT_COTHON", ()))
		elif iGoal == 1:
			bItaly = isControlled(iPhoenicia, utils.getPlotList(Areas.tNormalArea[iItaly][0], Areas.tNormalArea[iItaly][1], [(62, 47), (63, 47), (63, 46)]))
			bIberia = isControlled(iPhoenicia, Areas.getNormalArea(iSpain, False))
			aHelp.append(getIcon(bItaly) + localText.getText("TXT_KEY_VICTORY_ITALY", ()) + ' ' + getIcon(bIberia) + localText.getText("TXT_KEY_VICTORY_IBERIA_CARTHAGE", ()))
		elif iGoal == 2:
			iTreasury = pPhoenicia.getGold()
			aHelp.append(getIcon(iTreasury >= utils.getTurns(5000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iTreasury, utils.getTurns(5000))))

	elif iPlayer == iPolynesia:
		if iGoal == 0 or iGoal == 1:
			bHawaii = getNumCitiesInArea(iPolynesia, utils.getPlotList(tHawaiiTL, tHawaiiBR)) > 0
			bNewZealand = getNumCitiesInArea(iPolynesia, utils.getPlotList(tNewZealandTL, tNewZealandBR)) > 0
			bMarquesas = getNumCitiesInArea(iPolynesia, utils.getPlotList(tMarquesasTL, tMarquesasBR)) > 0
			bEasterIsland = getNumCitiesInArea(iPolynesia, utils.getPlotList(tEasterIslandTL, tEasterIslandBR)) > 0
			aHelp.append(getIcon(bHawaii) + localText.getText("TXT_KEY_VICTORY_HAWAII", ()) + getIcon(bNewZealand) + localText.getText("TXT_KEY_VICTORY_NEW_ZEALAND", ()) + getIcon(bMarquesas) + localText.getText("TXT_KEY_VICTORY_MARQUESAS", ()) + getIcon(bEasterIsland) + localText.getText("TXT_KEY_VICTORY_EASTER_ISLAND", ()))

	elif iPlayer == iPersia:
		if not pPersia.isReborn():
			if iGoal == 0:
				landPercent = getLandPercent(iPersia)
				aHelp.append(getIcon(landPercent >= 6.995) + localText.getText("TXT_KEY_VICTORY_PERCENTAGE_WORLD_TERRITORY", (str(u"%.2f%%" % landPercent), str(7))))
			elif iGoal == 1:
				iCounter = countWonders(iPersia)
				aHelp.append(getIcon(iCounter >= 7) + localText.getText("TXT_KEY_VICTORY_NUM_WONDERS", (iCounter, 7)))
			elif iGoal == 2:
				iCounter = countShrines(iPersia)
				aHelp.append(getIcon(iCounter >= 2) + localText.getText("TXT_KEY_VICTORY_NUM_SHRINES", (iCounter, 2)))
		else:
			if iGoal == 0:
				iCount = countOpenBorders(iPersia, lCivGroups[0])
				aHelp.append(getIcon(iCount >= 6) + localText.getText("TXT_KEY_VICTORY_OPEN_BORDERS", (iCount, 6)))
			elif iGoal == 1:
				bMesopotamia = isControlled(iPersia, utils.getPlotList(tSafavidMesopotamiaTL, tSafavidMesopotamiaBR))
				bTransoxania = isControlled(iPersia, utils.getPlotList(tTransoxaniaTL, tTransoxaniaBR))
				bNWIndia = isControlled(iPersia, utils.getPlotList(tNWIndiaTL, tNWIndiaBR, tNWIndiaExceptions))
				aHelp.append(getIcon(bMesopotamia) + localText.getText("TXT_KEY_VICTORY_MESOPOTAMIA", ()) + ' ' + getIcon(bTransoxania) + localText.getText("TXT_KEY_VICTORY_TRANSOXANIA", ()) + ' ' + getIcon(bNWIndia) + localText.getText("TXT_KEY_VICTORY_NORTHWEST_INDIA", ()))
			elif iGoal == 2:
				pBestCity = getMostCulturedCity(iPersia)
				iCulture = pBestCity.getCulture(iPersia)
				aHelp.append(getIcon(iCulture >= utils.getTurns(20000)) + localText.getText("TXT_KEY_VICTORY_MOST_CULTURED_CITY_VALUE", (pBestCity.getName(), iCulture, utils.getTurns(20000))))
				
	elif iPlayer == iRome:
		if iGoal == 0:
			iNumBarracks = getNumBuildings(iRome, iBarracks)
			iNumAqueducts = getNumBuildings(iRome, iAqueduct)
			iNumAmphitheatres = getNumBuildings(iRome, iAmphitheatre)
			iNumForums = getNumBuildings(iRome, iRomanForum)
			aHelp.append(getIcon(iNumBarracks >= 6) + localText.getText("TXT_KEY_VICTORY_NUM_BARRACKS", (iNumBarracks, 6)) + ' ' + getIcon(iNumAqueducts >= 5) + localText.getText("TXT_KEY_VICTORY_NUM_AQUEDUCTS", (iNumAqueducts, 5)) + ' ' + getIcon(iNumAmphitheatres >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_AMPHITHEATRES", (iNumAmphitheatres, 4)) + ' ' + getIcon(iNumForums >= 3) + localText.getText("TXT_KEY_VICTORY_NUM_FORUMS", (iNumForums, 3)))
		elif iGoal == 1:
			iCitiesSpain = getNumCitiesInArea(iRome, Areas.getNormalArea(iSpain, False))
			iCitiesFrance = getNumCitiesInArea(iRome, utils.getPlotList(tFranceTL, Areas.tNormalArea[iFrance][1]))
			iCitiesEngland = getNumCitiesInArea(iRome, Areas.getCoreArea(iEngland, False))
			iCitiesCarthage = getNumCitiesInArea(iRome, utils.getPlotList(tCarthageTL, tCarthageBR))
			iCitiesByzantium = getNumCitiesInArea(iRome, Areas.getCoreArea(iByzantium, False))
			iCitiesEgypt = getNumCitiesInArea(iRome, Areas.getCoreArea(iEgypt, False))
			aHelp.append(getIcon(iCitiesSpain >= 2) + localText.getText("TXT_KEY_VICTORY_ROME_CONTROL_SPAIN", (iCitiesSpain, 2)) + ' ' + getIcon(iCitiesFrance >= 3) + localText.getText("TXT_KEY_VICTORY_ROME_CONTROL_FRANCE", (iCitiesFrance, 3)) + ' ' + getIcon(iCitiesEngland >= 1) + localText.getText("TXT_KEY_VICTORY_ROME_CONTROL_ENGLAND", (iCitiesEngland, 1)))
			aHelp.append(getIcon(iCitiesCarthage >= 2) + localText.getText("TXT_KEY_VICTORY_ROME_CONTROL_CARTHAGE", (iCitiesCarthage, 2)) + ' ' + getIcon(iCitiesByzantium >= 4) + localText.getText("TXT_KEY_VICTORY_ROME_CONTROL_BYZANTIUM", (iCitiesByzantium, 4)) + ' ' + getIcon(iCitiesEgypt >= 2) + localText.getText("TXT_KEY_VICTORY_ROME_CONTROL_EGYPT", (iCitiesEgypt, 2)))
		elif iGoal == 2:
			bTheology = sd.getFirstDiscovered(iTheology) == iRome
			bMachinery = sd.getFirstDiscovered(iMachinery) == iRome
			bCivilService = sd.getFirstDiscovered(iCivilService) == iRome
			aHelp.append(getIcon(bTheology) + localText.getText("TXT_KEY_TECH_THEOLOGY", ()) + ' ' + getIcon(bMachinery) + localText.getText("TXT_KEY_TECH_MACHINERY", ()) + ' ' + getIcon(bCivilService) + localText.getText("TXT_KEY_TECH_CIVIL_SERVICE", ()))

	elif iPlayer == iTamils:
		if iGoal == 0:
			iTreasury = pTamils.getGold()
			iCulture = pTamils.countTotalCulture()
			aHelp.append(getIcon(iTreasury >= utils.getTurns(3000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iTreasury, utils.getTurns(3000))))
			aHelp.append(getIcon(iCulture >= utils.getTurns(2000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(2000))))
		elif iGoal == 1:
			bDeccan = isControlledOrVassalized(iTamils, utils.getPlotList(tDeccanTL, tDeccanBR))
			bSrivijaya = isControlledOrVassalized(iTamils, utils.getPlotList(tSrivijayaTL, tSrivijayaBR))
			aHelp.append(getIcon(bDeccan) + localText.getText("TXT_KEY_VICTORY_DECCAN", ()) + ' ' + getIcon(bSrivijaya) + localText.getText("TXT_KEY_VICTORY_SRIVIJAYA", ()))
		elif iGoal == 2:
			iTradeGold = sd.getTamilTradeGold()
			aHelp.append(getIcon(iTradeGold >= utils.getTurns(4000)) + localText.getText("TXT_KEY_VICTORY_TRADE_GOLD", (iTradeGold, utils.getTurns(4000))))

	elif iPlayer == iEthiopia:
		if iGoal == 1:
			iNumIncense = pEthiopia.getNumAvailableBonuses(iIncense)
			aHelp.append(getIcon(iNumIncense >= 3) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_INCENSE_RESOURCES", (iNumIncense, 3)))
		elif iGoal == 2:
			bAfrica = isAreaFreeOfCivs(utils.getPlotList(tSomaliaTL, tSomaliaBR), lCivGroups[0]) and isAreaFreeOfCivs(utils.getPlotList(tSubeqAfricaTL, tSubeqAfricaBR), lCivGroups[0])
			aHelp.append(getIcon(bAfrica) + localText.getText("TXT_KEY_VICTORY_NO_AFRICAN_COLONIES_CURRENT", ()))

	elif iPlayer == iKorea:
		if iGoal == 0:
			bConfucianCathedral = (getNumBuildings(iKorea, iConfucianCathedral) > 0)
			bBuddhistCathedral = (getNumBuildings(iKorea, iBuddhistCathedral) > 0)
			aHelp.append(getIcon(bBuddhistCathedral) + localText.getText("TXT_KEY_BUILDING_BUDDHIST_CATHEDRAL", ()) + ' ' + getIcon(bConfucianCathedral) + localText.getText("TXT_KEY_BUILDING_CONFUCIAN_CATHEDRAL", ()))
		elif iGoal == 2:
			iNumSinks = sd.getKoreanSinks()
			aHelp.append(getIcon(iNumSinks >= 20) + localText.getText("TXT_KEY_VICTORY_ENEMY_SHIPS_SUNK", (iNumSinks, 20)))

	# Maya goals have no stages
	elif iPlayer == iMaya:
		if pMaya.isReborn():
			if iGoal == 0:
				bPeru = isAreaFreeOfCivs(utils.getPlotList(tPeruTL, tPeruBR), lCivGroups[0])
				bGranColombia = isAreaFreeOfCivs(utils.getPlotList(tGranColombiaTL, tGranColombiaBR), lCivGroups[0])
				bGuayanas = isAreaFreeOfCivs(utils.getPlotList(tGuayanasTL, tGuayanasBR), lCivGroups[0])
				bCaribbean = isAreaFreeOfCivs(utils.getPlotList(tCaribbeanTL, tCaribbeanBR), lCivGroups[0])
				aHelp.append(getIcon(bPeru) + localText.getText("TXT_KEY_VICTORY_NO_COLONIES_PERU", ()) + ' ' + getIcon(bGranColombia) + localText.getText("TXT_KEY_VICTORY_NO_COLONIES_GRAN_COLOMBIA", ()))
				aHelp.append(getIcon(bGuayanas) + localText.getText("TXT_KEY_VICTORY_NO_COLONIES_GUAYANAS", ()) + ' ' + getIcon(bCaribbean) + localText.getText("TXT_KEY_VICTORY_NO_COLONIES_CARIBBEAN", ()))
			elif iGoal == 1:
				bSouthAmerica = isControlled(iMaya, utils.getPlotList(tSAmericaTL, tSAmericaBR, tSouthAmericaExceptions))
				aHelp.append(getIcon(bSouthAmerica) + localText.getText("TXT_KEY_VICTORY_CONTROL_SOUTH_AMERICA", ()))
			elif iGoal == 2:
				iTradeGold = sd.getColombianTradeGold()
				aHelp.append(getIcon(iTradeGold >= utils.getTurns(3000)) + localText.getText("TXT_KEY_VICTORY_TRADE_GOLD_RESOURCES", (iTradeGold, utils.getTurns(3000))))

	elif iPlayer == iByzantium:
		if iGoal == 0:
			iTreasury = pByzantium.getGold()
			aHelp.append(getIcon(iTreasury >= utils.getTurns(5000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iTreasury, utils.getTurns(5000))))
		elif iGoal == 1:
			pBestPopCity = getBestCity(iByzantium, (68, 45), cityPopulation)
			bBestPopCity = isBestCity(iByzantium, (68, 45), cityPopulation)
			pBestCultureCity = getBestCity(iByzantium, (68, 45), cityCulture)
			bBestCultureCity = isBestCity(iByzantium, (68, 45), cityCulture)
			aHelp.append(getIcon(bBestPopCity) + localText.getText("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", (pBestPopCity.getName(),)) + ' ' + getIcon(bBestCultureCity) + localText.getText("TXT_KEY_VICTORY_MOST_CULTURED_CITY", (pBestCultureCity.getName(),)))
		elif iGoal == 2:
			iBalkans = getNumCitiesInArea(iByzantium, utils.getPlotList(tBalkansTL, tBalkansBR))
			iNorthAfrica = getNumCitiesInArea(iByzantium, utils.getPlotList(tNorthAfricaTL, tNorthAfricaBR))
			iNearEast = getNumCitiesInArea(iByzantium, utils.getPlotList(tNearEastTL, tNearEastBR))
			aHelp.append(getIcon(iBalkans >= 3) + localText.getText("TXT_KEY_VICTORY_BALKANS", (iBalkans, 3)) + ' ' + getIcon(iNorthAfrica >= 3) + localText.getText("TXT_KEY_VICTORY_NORTH_AFRICA", (iNorthAfrica, 3)) + ' ' + getIcon(iNearEast >= 3) + localText.getText("TXT_KEY_VICTORY_NEAR_EAST", (iNearEast, 3)))

	elif iPlayer == iJapan:
		if iGoal == 0:
			iAverageCulture = getAverageCulture(iJapan)
			aHelp.append(getIcon(iAverageCulture >= utils.getTurns(6000)) + localText.getText("TXT_KEY_VICTORY_AVERAGE_CULTURE", (iAverageCulture, utils.getTurns(6000))))
		elif iGoal == 1:
			bKorea = isControlledOrVassalized(iJapan, utils.getPlotList(tKoreaTL, tKoreaBR))
			bManchuria = isControlledOrVassalized(iJapan, utils.getPlotList(tManchuriaTL, tManchuriaBR))
			bChina = isControlledOrVassalized(iJapan, utils.getPlotList(tChinaTL, tChinaBR))
			bIndochina = isControlledOrVassalized(iJapan, utils.getPlotList(tIndochinaTL, tIndochinaBR, tIndochinaExceptions))
			bIndonesia = isControlledOrVassalized(iJapan, utils.getPlotList(tIndonesiaTL, tIndonesiaBR))
			bPhilippines = isControlledOrVassalized(iJapan, utils.getPlotList(tPhilippinesTL, tPhilippinesBR))
			aHelp.append(getIcon(bKorea) + localText.getText("TXT_KEY_CIV_KOREA_SHORT_DESC", ()) + ' ' + getIcon(bManchuria) + localText.getText("TXT_KEY_VICTORY_MANCHURIA", ()) + ' ' + getIcon(bChina) + localText.getText("TXT_KEY_CIV_CHINA_SHORT_DESC", ()))
			aHelp.append(getIcon(bIndochina) + localText.getText("TXT_KEY_VICTORY_INDOCHINA", ()) + ' ' + getIcon(bIndonesia) + localText.getText("TXT_KEY_CIV_INDONESIA_SHORT_DESC", ()) + ' ' + getIcon(bPhilippines) + localText.getText("TXT_KEY_VICTORY_PHILIPPINES", ()))
		elif iGoal == 2:
			iTechsFirstDiscovered = countFirstDiscovered(iJapan, iModern)
			aHelp.append(getIcon(iTechsFirstDiscovered >= 5) + localText.getText("TXT_KEY_VICTORY_TECHS_FIRST_DISCOVERED", (gc.getEraInfo(iModern).getText(), iTechsFirstDiscovered, 5)))
			
	elif iPlayer == iVikings:
		if iGoal == 0:
			lEuroCivs = [iRome, iByzantium, iSpain, iFrance, iEngland, iHolyRome, iRussia]
			bEuropeanCore = isCoreControlled(iVikings, lEuroCivs)
			aHelp.append(getIcon(bEuropeanCore) + localText.getText("TXT_KEY_VICTORY_EUROPEAN_CORE", ()))
		elif iGoal == 2:
			iRaidGold = sd.getVikingGold()
			aHelp.append(getIcon(iRaidGold >= utils.getTurns(3000)) + localText.getText("TXT_KEY_VICTORY_ACQUIRED_GOLD", (iRaidGold, utils.getTurns(3000))))


	elif iPlayer == iArabia:
		if iGoal == 0:
			iMostAdvancedCiv = getBestPlayer(iArabia, playerTechs)
			aHelp.append(getIcon(iMostAdvancedCiv == iArabia) + localText.getText("TXT_KEY_VICTORY_MOST_ADVANCED_CIV", (str(gc.getPlayer(iMostAdvancedCiv).getCivilizationShortDescriptionKey()),)))
		elif iGoal == 1:
			bEgypt = isControlledOrVassalized(iArabia, Areas.getCoreArea(iEgypt, False))
			bMaghreb = isControlledOrVassalized(iArabia, utils.getPlotList(tCarthageTL, tCarthageBR))
			bMesopotamia = isControlledOrVassalized(iArabia, Areas.getCoreArea(iBabylonia, False))
			bPersia = isControlledOrVassalized(iArabia, Areas.getCoreArea(iPersia, False))
			bSpain = isControlledOrVassalized(iArabia, Areas.getNormalArea(iSpain, False))
			aHelp.append(getIcon(bEgypt) + localText.getText("TXT_KEY_CIV_EGYPT_SHORT_DESC", ()) + ' ' + getIcon(bMaghreb) + localText.getText("TXT_KEY_VICTORY_MAGHREB", ()) + ' ' + getIcon(bSpain) + localText.getText("TXT_KEY_CIV_SPAIN_SHORT_DESC", ()))
			aHelp.append(getIcon(bMesopotamia) + localText.getText("TXT_KEY_VICTORY_MESOPOTAMIA", ()) + ' ' + getIcon(bPersia) + localText.getText("TXT_KEY_CIV_PERSIA_SHORT_DESC", ()))
		elif iGoal == 2:
			fReligionPercent = gc.getGame().calculateReligionPercent(iIslam)
			aHelp.append(getIcon(fReligionPercent >= 40.0) + localText.getText("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", (gc.getReligionInfo(iIslam).getTextKey(), str(u"%.2f%%" % fReligionPercent), str(40))))

	elif iPlayer == iTibet:
		if iGoal == 0:
			iNumCities = pTibet.getNumCities()
			aHelp.append(getIcon(iNumCities >= 5) + localText.getText("TXT_KEY_VICTORY_CITIES_ACQUIRED", (iNumCities, 5)))
		elif iGoal == 1:
			fReligionPercent = gc.getGame().calculateReligionPercent(iBuddhism)
			aHelp.append(getIcon(fReligionPercent >= 30.0) + localText.getText("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", (gc.getReligionInfo(iBuddhism).getTextKey(), str(u"%.2f%%" % fReligionPercent), str(30))))
		elif iGoal == 2:
			iCounter = countCitySpecialists(iTibet, Areas.getCapital(iTibet), iSpecialistGreatProphet)
			aHelp.append(getIcon(iCounter >= 5) + localText.getText("TXT_KEY_VICTORY_GREAT_PROPHETS_SETTLED", ("Lhasa", iCounter, 5)))

	elif iPlayer == iKhmer:
		if iGoal == 0:
			iNumBuddhism = getNumBuildings(iKhmer, iBuddhistMonastery)
			iNumHinduism = getNumBuildings(iKhmer, iHinduMonastery)
			bAngkorWat = sd.getWonderBuilder(iAngkorWat) == iKhmer
			aHelp.append(getIcon(iNumBuddhism >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_BUDDHIST_MONASTERIES", (iNumBuddhism, 4)) + ' ' + getIcon(iNumHinduism >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_HINDU_MONASTERIES", (iNumHinduism, 4)) + ' ' + getIcon(bAngkorWat) + localText.getText("TXT_KEY_BUILDING_WAT_PREAH_PISNULOK", ()))
		elif iGoal == 1:
			fPopPerCity = getAverageCitySize(iKhmer)
			aHelp.append(getIcon(fPopPerCity >= 12.0) + localText.getText("TXT_KEY_VICTORY_AVERAGE_CITY_POPULATION", (str(u"%.2f" % fPopPerCity), str(12))))
		elif iGoal == 2:
			iCulture = pKhmer.countTotalCulture()
			aHelp.append(getIcon(iCulture >= utils.getTurns(8000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(8000))))

	elif iPlayer == iIndonesia:
		if iGoal == 0:
			iHighestCiv = getBestPlayer(iIndonesia, playerRealPopulation)
			bHighest = (iHighestCiv == iIndonesia)
			aHelp.append(getIcon(bHighest) + localText.getText("TXT_KEY_VICTORY_HIGHEST_POPULATION_CIV", ()) + localText.getText(str(gc.getPlayer(iHighestCiv).getCivilizationShortDescriptionKey()),()))
		elif iGoal == 1:
			iCounter = countHappinessResources(iIndonesia)
			aHelp.append(getIcon(iCounter >= 10) + localText.getText("TXT_KEY_VICTORY_NUM_HAPPINESS_RESOURCES", (iCounter, 10)))
		elif iGoal == 2:
			popPercent = calculatePopulationPercent(iIndonesia)
			aHelp.append(getIcon(popPercent >= 9.0) + localText.getText("TXT_KEY_VICTORY_PERCENTAGE_WORLD_POPULATION", (str(u"%.2f%%" % popPercent), str(9))))

	elif iPlayer == iMoors:
		if iGoal == 0:
			iIberia = getNumCitiesInArea(iMoors, utils.getPlotList(tIberiaTL, tIberiaBR))
			iMaghreb = getNumCitiesInArea(iMoors, utils.getPlotList(tMaghrebTL, tMaghrebBR))
			iWestAfrica = getNumCitiesInArea(iMoors, utils.getPlotList(tWestAfricaTL, tWestAfricaBR))
			aHelp.append(getIcon(iIberia >= 3) + localText.getText("TXT_KEY_VICTORY_IBERIA", (iIberia, 3)) + ' ' + getIcon(iMaghreb >= 3) + localText.getText("TXT_KEY_VICTORY_MAGHREB_MOORS", (iMaghreb, 3)) + ' ' + getIcon(iWestAfrica >= 3) + localText.getText("TXT_KEY_VICTORY_WEST_AFRICA", (iWestAfrica, 3)))
		elif iGoal == 1:
			iCounter = 0
			iCounter += countCitySpecialists(iMoors, (51, 41), iSpecialistGreatProphet)
			iCounter += countCitySpecialists(iMoors, (51, 41), iSpecialistGreatScientist)
			iCounter += countCitySpecialists(iMoors, (51, 41), iSpecialistGreatEngineer)
			aHelp.append(getIcon(iCounter >= 5) + localText.getText("TXT_KEY_VICTORY_GREAT_PEOPLE_IN_CITY_MOORS", ("Cordoba", iCounter, 5)))
		elif iGoal == 2:
			iRaidGold = sd.getMoorishGold()
			aHelp.append(getIcon(iRaidGold >= utils.getTurns(3000)) + localText.getText("TXT_KEY_VICTORY_PIRACY", (iRaidGold, utils.getTurns(3000))))

	elif iPlayer == iSpain:
		if iGoal == 1:
			iNumGold = countResources(iSpain, iGold)
			iNumSilver = countResources(iSpain, iSilver)
			aHelp.append(getIcon(iNumGold + iNumSilver >= 10) + localText.getText("TXT_KEY_VICTORY_GOLD_SILVER_RESOURCES", (iNumGold + iNumSilver, 10)))
		elif iGoal == 2:
			fReligionPercent = gc.getGame().calculateReligionPercent(iCatholicism)
			bNoProtestants = not isStateReligionInArea(iProtestantism, tEuropeTL, tEuropeBR) and not isStateReligionInArea(iProtestantism, tEasternEuropeTL, tEasternEuropeBR)
			aHelp.append(getIcon(fReligionPercent >= 40.0) + localText.getText("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", (gc.getReligionInfo(iCatholicism).getTextKey(), str(u"%.2f%%" % fReligionPercent), str(40))) + ' ' + getIcon(bNoProtestants) + localText.getText("TXT_KEY_VICTORY_NO_PROTESTANTS", ()))

	elif iPlayer == iFrance:
		if iGoal == 0:
			iCulture = getCityCulture(iFrance, (55, 50))
			aHelp.append(getIcon(iCulture >= utils.getTurns(25000)) + localText.getText("TXT_KEY_VICTORY_CITY_CULTURE", ("Paris", iCulture, utils.getTurns(25000))))
		elif iGoal == 1:
			iEurope, iTotalEurope = countControlledTiles(iFrance, tEuropeTL, tEuropeBR, True)
			iEasternEurope, iTotalEasternEurope = countControlledTiles(iFrance, tEasternEuropeTL, tEasternEuropeBR, True)
			iNorthAmerica, iTotalNorthAmerica = countControlledTiles(iFrance, tNorthAmericaTL, tNorthAmericaBR, True)
			fEurope = (iEurope + iEasternEurope) * 100.0 / (iTotalEurope + iTotalEasternEurope)
			fNorthAmerica = iNorthAmerica * 100.0 / iTotalNorthAmerica
			aHelp.append(getIcon(fEurope >= 40.0) + localText.getText("TXT_KEY_VICTORY_EUROPEAN_TERRITORY", (str(u"%.2f%%" % fEurope), str(40))) + ' ' + getIcon(fNorthAmerica >= 40.0) + localText.getText("TXT_KEY_VICTORY_NORTH_AMERICAN_TERRITORY", (str(u"%.2f%%" % fNorthAmerica), str(40))))
		elif iGoal == 2:	# not entirely correct, this counts conquered ones as well
			bNotreDame = sd.getWonderBuilder(iNotreDame) == iFrance
			bVersailles = sd.getWonderBuilder(iVersailles) == iFrance
			bStatueOfLiberty = sd.getWonderBuilder(iStatueOfLiberty) == iFrance
			bEiffelTower = sd.getWonderBuilder(iEiffelTower) == iFrance
			aHelp.append(getIcon(bNotreDame) + localText.getText("TXT_KEY_BUILDING_NOTRE_DAME", ()) + ' ' + getIcon(bVersailles) + localText.getText("TXT_KEY_BUILDING_VERSAILLES", ()) + ' ' + getIcon(bStatueOfLiberty) + localText.getText("TXT_KEY_BUILDING_STATUE_OF_LIBERTY", ()) + ' ' + getIcon(bEiffelTower) + localText.getText("TXT_KEY_BUILDING_EIFFEL_TOWER", ()))

	elif iPlayer == iEngland:
		if iGoal == 0:
			iNAmerica = getNumCitiesInArea(iEngland, utils.getPlotList(tNorthAmericaTL, tNorthAmericaBR))
			iSCAmerica = getNumCitiesInArea(iEngland, utils.getPlotList(tSouthCentralAmericaTL, tSouthCentralAmericaBR))
			iAfrica = getNumCitiesInArea(iEngland, utils.getPlotList(tAfricaTL, tAfricaBR))
			iAsia = getNumCitiesInArea(iEngland, utils.getPlotList(tAsiaTL, tAsiaBR))
			iOceania = getNumCitiesInArea(iEngland, utils.getPlotList(tOceaniaTL, tOceaniaBR))
			aHelp.append(getIcon(iNAmerica >= 5) + localText.getText("TXT_KEY_VICTORY_ENGLAND_CONTROL_NORTH_AMERICA", (iNAmerica, 5)) + ' ' + getIcon(iAsia >= 5) + localText.getText("TXT_KEY_VICTORY_ENGLAND_CONTROL_ASIA", (iAsia, 5)) + ' ' + getIcon(iAfrica >= 4) + localText.getText("TXT_KEY_VICTORY_ENGLAND_CONTROL_AFRICA", (iAfrica, 4)))
			aHelp.append(getIcon(iSCAmerica >= 3) + localText.getText("TXT_KEY_VICTORY_ENGLAND_CONTROL_SOUTH_AMERICA", (iSCAmerica, 3)))
			aHelp.append(getIcon(iOceania >= 3) + localText.getText("TXT_KEY_VICTORY_ENGLAND_CONTROL_OCEANIA", (iOceania, 3)))
		elif iGoal == 1:
			iEnglishNavy = 0
			iEnglishNavy += pEngland.getUnitClassCount(gc.getUnitInfo(iFrigate).getUnitClassType())
			iEnglishNavy += pEngland.getUnitClassCount(gc.getUnitInfo(iShipOfTheLine).getUnitClassType())
			iEnglishSinks = sd.getEnglishSinks()
			aHelp.append(getIcon(iEnglishNavy >= 25) + localText.getText("TXT_KEY_VICTORY_NAVY_SIZE", (iEnglishNavy, 25)) + ' ' + getIcon(iEnglishSinks >= 50) + localText.getText("TXT_KEY_VICTORY_ENEMY_SHIPS_SUNK", (iEnglishSinks, 50)))
		elif iGoal == 2:
			bIndustrial = sd.getFirstEntered(iIndustrial) == iEngland
			bModern = sd.getFirstEntered(iModern) == iEngland
			aHelp.append(getIcon(bIndustrial) + localText.getText("TXT_KEY_VICTORY_FIRST_ENTER_INDUSTRIAL", ()) + ' ' + getIcon(bModern) + localText.getText("TXT_KEY_VICTORY_FIRST_ENTER_MODERN", ()))

	elif iPlayer == iHolyRome:
		if iGoal == 0:
			bSaintPeters = getNumBuildings(iHolyRome, iCatholicShrine) > 0
			bAnastasis = getNumBuildings(iHolyRome, iCatholicShrine) > 0
			aHelp.append(getIcon(bSaintPeters) + localText.getText("TXT_KEY_BUILDING_CATHOLIC_SHRINE", ()) + ' ' + getIcon(bAnastasis) + localText.getText("TXT_KEY_BUILDING_ORTHODOX_SHRINE", ()))
		elif iGoal == 2:
			iGreatArtists = countCitySpecialists(iHolyRome, tVienna, iSpecialistGreatArtist)
			aHelp.append(getIcon(iGreatArtists >= 3) + localText.getText("TXT_KEY_VICTORY_GREAT_ARTISTS_SETTLED", ('Vienna', iGreatArtists, 3)))

	elif iPlayer == iRussia:
		if iGoal == 0:
			iSiberia = getNumFoundedCitiesInArea(iRussia, utils.getPlotList(tSiberiaTL, tSiberiaBR))
			bSiberianRailway = isConnectedByRailroad(iRussia, Areas.getCapital(iRussia), lSiberianCoast)
			aHelp.append(getIcon(iSiberia >= 7) + localText.getText("TXT_KEY_VICTORY_RUSSIA_CONTROL_SIBERIA", (iSiberia, 7)) + ' ' + getIcon(bSiberianRailway) + localText.getText("TXT_KEY_VICTORY_TRANSSIBERIAN_RAILWAY", ()))
		elif iGoal == 1:
			bManhattanProject = teamRussia.getProjectCount(iManhattanProject) > 0
			bApolloProgram = teamRussia.getProjectCount(iApolloProgram) > 0
			aHelp.append(getIcon(bManhattanProject) + localText.getText("TXT_KEY_PROJECT_MANHATTAN_PROJECT", ()) + ' ' + getIcon(bApolloProgram) + localText.getText("TXT_KEY_PROJECT_APOLLO_PROGRAM", ()))
		elif iGoal == 2:
			iCount = countPlayersWithAttitudeAndCivic(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY, (3, iCivicCentralPlanning))
			aHelp.append(getIcon(iCount >= 5) + localText.getText("TXT_KEY_VICTORY_COMMUNIST_BROTHERS", (iCount, 5)))

	elif iPlayer == iMali:
		if iGoal == 1:
			bSankore = False
			iProphets = 0
			for city in utils.getCityList(iMali):
				if city.isHasRealBuilding(iUniversityofSankore):
					bSankore = True
					iProphets = city.getFreeSpecialistCount(iSpecialistGreatProphet)
					break
			aHelp.append(getIcon(bSankore) + localText.getText("TXT_KEY_BUILDING_UNIVERSITY_OF_SANKORE", ()) + ' ' + getIcon(iProphets >= 1) + localText.getText("TXT_KEY_VICTORY_SANKORE_PROPHETS", (iProphets, 1)))
		elif iGoal == 2:
			iTreasury = pMali.getGold()
			iThreshold = 5000
			if gc.getGame().getGameTurn() > getTurnForYear(1500): iThreshold = 15000
			aHelp.append(getIcon(iTreasury >= utils.getTurns(iThreshold)) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iTreasury, utils.getTurns(iThreshold))))
		
	elif iPlayer == iPoland:
		if iGoal == 0:
			lCities = getLargestCities(iPlayer, 3)
			bCity1 = len(lCities) > 0
			bCity2 = len(lCities) > 1
			bCity3 = len(lCities) > 2
			if not bCity1: aHelp.append(getIcon(False) + localText.getText("TXT_KEY_VICTORY_NO_CITIES", ()))
			if bCity1: aHelp.append(getIcon(lCities[0].getPopulation() >= 12) + localText.getText("TXT_KEY_VICTORY_CITY_SIZE", (lCities[0].getName(), lCities[0].getPopulation(), 12)))
			if bCity2: aHelp.append(getIcon(lCities[1].getPopulation() >= 12) + localText.getText("TXT_KEY_VICTORY_CITY_SIZE", (lCities[1].getName(), lCities[1].getPopulation(), 12)))
			if bCity3: aHelp.append(getIcon(lCities[2].getPopulation() >= 12) + localText.getText("TXT_KEY_VICTORY_CITY_SIZE", (lCities[2].getName(), lCities[2].getPopulation(), 12)))
		elif iGoal == 2:
			iCatholic = getNumBuildings(iPoland, iCatholicCathedral)
			iOrthodox = getNumBuildings(iPoland, iOrthodoxCathedral)
			iProtestant = getNumBuildings(iPoland, iProtestantCathedral)
			iCathedrals = iCatholic + iOrthodox + iProtestant
			aHelp.append(getIcon(iCathedrals >= 3) + localText.getText("TXT_KEY_VICTORY_CHRISTIAN_CATHEDRALS", (iCathedrals, 3)))

	elif iPlayer == iPortugal:
		if iGoal == 0:
			iCount = countOpenBorders(iPortugal)
			aHelp.append(getIcon(iCount >= 14) + localText.getText("TXT_KEY_VICTORY_OPEN_BORDERS", (iCount, 14)))
		elif iGoal == 1:
			iCount = countAcquiredResources(iPortugal, lColonialResources)
			aHelp.append(getIcon(iCount >= 12) + localText.getText("TXT_KEY_VICTORY_COLONIAL_RESOURCES", (iCount, 12)))
		elif iGoal == 2:
			iColonies = getNumCitiesInArea(iPortugal, utils.getPlotList(tBrazilTL, tBrazilBR))
			iColonies += getNumCitiesInArea(iPortugal, utils.getPlotList(tAfricaTL, tAfricaBR))
			iColonies += getNumCitiesInArea(iPortugal, utils.getPlotList(tAsiaTL, tAsiaBR))
			aHelp.append(getIcon(iColonies >= 15) + localText.getText("TXT_KEY_VICTORY_EXTRA_EUROPEAN_COLONIES", (iColonies, 15)))

	elif iPlayer == iInca:
		if iGoal == 0:
			bRoad = isRoad(iInca, lAndeanCoast)
			iTambos = getNumBuildings(iInca, iIncanTambo)
			aHelp.append(getIcon(bRoad) + localText.getText("TXT_KEY_VICTORY_ANDEAN_ROAD", ()) + ' ' + getIcon(iTambos >= 5) + localText.getText("TXT_KEY_VICTORY_NUM_TAMBOS", (iTambos, 5)))
		elif iGoal == 1:
			iTreasury = pInca.getGold()
			aHelp.append(getIcon(iTreasury >= utils.getTurns(2500)) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iTreasury, utils.getTurns(2500))))
		elif iGoal == 2:
			iControl, iTotal = countControlledTiles(iInca, tSAmericaTL, tSAmericaBR, False, tSouthAmericaExceptions)
			fControl = iControl * 100.0 / iTotal
			aHelp.append(getIcon(fControl >= 60.0) + localText.getText("TXT_KEY_VICTORY_SOUTH_AMERICAN_TERRITORY", (str(u"%.2f%%" % fControl), str(60))))

	elif iPlayer == iItaly:
		if iGoal == 0:
			bSanMarcoBasilica = sd.getWonderBuilder(iSanMarcoBasilica) == iItaly
			bSistineChapel = sd.getWonderBuilder(iSistineChapel) == iItaly
			bLeaningTower = sd.getWonderBuilder(iLeaningTower) == iItaly
			aHelp.append(getIcon(bSanMarcoBasilica) + localText.getText("TXT_KEY_BUILDING_SAN_MARCO_BASILICA", ()) + ' ' + getIcon(bSistineChapel) + localText.getText("TXT_KEY_BUILDING_SISTINE_CHAPEL", ()) + ' ' + getIcon(bLeaningTower) + localText.getText("TXT_KEY_BUILDING_LEANING_TOWER", ()))
		elif iGoal == 1:
			iCount = countCitiesWithCultureLevel(iItaly, 5)
			aHelp.append(getIcon(iCount >= 3) + localText.getText("TXT_KEY_VICTORY_NUM_CITIES_INFLUENTIAL_CULTURE", (iCount, 3)))
		elif iGoal == 2:
			iMediterranean, iTotalMediterranean = countControlledTiles(iItaly, tMediterraneanTL, tMediterraneanBR, False, tMediterraneanExceptions, True)
			fMediterranean = iMediterranean * 100.0 / iTotalMediterranean
			aHelp.append(getIcon(fMediterranean >= 65.0) + localText.getText("TXT_KEY_VICTORY_MEDITERRANEAN_TERRITORY", (str(u"%.2f%%" % fMediterranean), str(65))))

	elif iPlayer == iMongolia:
		if iGoal == 1:
			iRazedCities = sd.getMongolRazes()
			aHelp.append(getIcon(iRazedCities >= 7) + localText.getText("TXT_KEY_VICTORY_NUM_CITIES_RAZED", (iRazedCities, 7)))
		elif iGoal == 2:
			landPercent = getLandPercent(iMongolia)
			aHelp.append(getIcon(landPercent >= 11.995) + localText.getText("TXT_KEY_VICTORY_PERCENTAGE_WORLD_TERRITORY", (str(u"%.2f%%" % landPercent), str(12))))

	elif iPlayer == iMughals:
		if iGoal == 0:
			iNumMosques = getNumBuildings(iMughals, iIslamicCathedral)
			aHelp.append(getIcon(iNumMosques >= 3) + localText.getText("TXT_KEY_VICTORY_MOSQUES_BUILT", (iNumMosques, 3)))
		elif iGoal == 1:
			bRedFort = sd.getWonderBuilder(iRedFort) == iMughals
			bHarmandirSahib = sd.getWonderBuilder(iHarmandirSahib) == iMughals
			bTajMahal = sd.getWonderBuilder(iTajMahal) == iMughals
			aHelp.append(getIcon(bRedFort) + localText.getText("TXT_KEY_BUILDING_RED_FORT", ()) + ' ' + getIcon(bHarmandirSahib) + localText.getText("TXT_KEY_BUILDING_HARMANDIR_SAHIB", ()) + ' ' + getIcon(bTajMahal) + localText.getText("TXT_KEY_BUILDING_TAJ_MAHAL", ()))
		elif iGoal == 2:
			iCulture = pMughals.countTotalCulture()
			aHelp.append(getIcon(iCulture >= utils.getTurns(50000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(50000))))

	elif iPlayer == iAztecs:
		if not pAztecs.isReborn():
			if iGoal == 0:
				pBestCity = getBestCity(iAztecs, (18, 37), cityPopulation)
				bBestCity = isBestCity(iAztecs, (18, 37), cityPopulation)
				aHelp.append(getIcon(bBestCity) + localText.getText("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", (pBestCity.getName(),)))
			elif iGoal == 1:
				iTemples = getNumBuildings(iAztecs, iPaganTemple)
				iAltars = getNumBuildings(iAztecs, iAztecSacrificialAltar)
				aHelp.append(getIcon(iTemples >= 6) + localText.getText("TXT_KEY_VICTORY_NUM_TEMPLES", (iTemples, 6)) + " " + getIcon(iAltars >= 6) + localText.getText("TXT_KEY_VICTORY_NUM_ALTARS", (iAltars, 6)))
			elif iGoal == 2:
				iEnslavedUnits = sd.getAztecSlaves()
				aHelp.append(getIcon(iEnslavedUnits >= 20) + localText.getText("TXT_KEY_VICTORY_ENSLAVED_UNITS", (iEnslavedUnits, 20)))
		else:
			if iGoal == 0:
				iNumCathedrals = 0
				iStateReligion = pAztecs.getStateReligion()
				if iStateReligion >= 0:
					iStateReligionCathedral = iCathedral + 4*iStateReligion
					iNumCathedrals = getNumBuildings(iAztecs, iStateReligionCathedral)
				aHelp.append(getIcon(iNumCathedrals >= 3) + localText.getText("TXT_KEY_VICTORY_STATE_RELIGION_CATHEDRALS", (gc.getReligionInfo(iStateReligion).getAdjectiveKey(), iNumCathedrals, 3)))
			elif iGoal == 1:
				iGenerals = pAztecs.getGreatGeneralsCreated()
				aHelp.append(getIcon(iGenerals >= 3) + localText.getText("TXT_KEY_VICTORY_GREAT_GENERALS", (iGenerals, 3)))
			elif iGoal == 2:
				pBestCity = getBestCity(iAztecs, (18, 37), cityPopulation)
				bBestCity = isBestCity(iAztecs, (18, 37), cityPopulation)
				aHelp.append(getIcon(bBestCity) + localText.getText("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", (pBestCity.getName(),)))

	elif iPlayer == iTurkey:
		if iGoal == 0:
			capital = pTurkey.getCapitalCity()
			iCounter = countCityWonders(iTurkey, (capital.getX(), capital.getY()), False)
			aHelp.append(getIcon(iCounter >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_WONDERS_CAPITAL", (iCounter, 4)))
		elif iGoal == 1:
			bEasternMediterranean = isCultureControlled(iTurkey, lEasternMediterranean)
			bBlackSea = isCultureControlled(iTurkey, lBlackSea)
			bCairo = controlsCity(iTurkey, tCairo)
			bMecca = controlsCity(iTurkey, tMecca)
			bBaghdad = controlsCity(iTurkey, tBaghdad)
			bVienna = controlsCity(iTurkey, tVienna)
			aHelp.append(getIcon(bEasternMediterranean) + localText.getText("TXT_KEY_VICTORY_EASTERN_MEDITERRANEAN", ()) + ' ' + getIcon(bBlackSea) + localText.getText("TXT_KEY_VICTORY_BLACK_SEA", ()))
			aHelp.append(getIcon(bCairo) + localText.getText("TXT_KEY_VICTORY_CAIRO", ()) + ' ' + getIcon(bMecca) + localText.getText("TXT_KEY_VICTORY_MECCA", ()) + ' ' + getIcon(bBaghdad) + localText.getText("TXT_KEY_VICTORY_BAGHDAD", ()) + ' ' + getIcon(bVienna) + localText.getText("TXT_KEY_VICTORY_VIENNA", ()))
		elif iGoal == 2:
			iTurkishCulture = pTurkey.countTotalCulture()
			iEuropeanCulture = getTotalCulture(lCivGroups[0])
			aHelp.append(getIcon(iTurkishCulture > iEuropeanCulture) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iTurkishCulture, iEuropeanCulture)))

	elif iPlayer == iThailand:
		if iGoal == 0:
			iCount = countOpenBorders(iThailand)
			aHelp.append(getIcon(iCount >= 10) + localText.getText("TXT_KEY_VICTORY_OPEN_BORDERS", (iCount, 10)))
		elif iGoal == 1:
			pBestCity = getBestCity(iThailand, (101, 33), cityPopulation)
			bBestCity = isBestCity(iThailand, (101, 33), cityPopulation)
			if not bBestCity:
				pBestCity = getBestCity(iThailand, (102, 33), cityPopulation)
				bBestCity = isBestCity(iThailand, (102, 33), cityPopulation)
			aHelp.append(getIcon(bBestCity) + localText.getText("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", (pBestCity.getName(),)))
		elif iGoal == 2:
			bSouthAsia = isAreaOnlyCivs(tSouthAsiaTL, tSouthAsiaBR, lSouthAsianCivs)
			aHelp.append(getIcon(bSouthAsia) + localText.getText("TXT_KEY_VICTORY_NO_SOUTH_ASIAN_COLONIES", ()))

	elif iPlayer == iCongo:
		if iGoal == 0:
			fPercent = getApostolicVotePercent(iCongo)
			aHelp.append(getIcon(fPercent >= 15.0) + localText.getText("TXT_KEY_VICTORY_APOSTOLIC_VOTE_PERCENT", (str(u"%.2f%%" % fPercent), str(15))))
		elif iGoal == 1:
			iSlaves = sd.getCongoSlaveCounter()
			aHelp.append(getIcon(iSlaves >= utils.getTurns(1000)) + localText.getText("TXT_KEY_VICTORY_SLAVES_TRADED", (iSlaves, utils.getTurns(1000))))

	elif iPlayer == iNetherlands:
		if iGoal == 0:
			iMerchants = countCitySpecialists(iNetherlands, Areas.getCapital(iNetherlands), iSpecialistGreatMerchant)
			aHelp.append(getIcon(iMerchants >= 3) + localText.getText("TXT_KEY_VICTORY_GREAT_MERCHANTS_IN_CITY", ("Amsterdam", iMerchants, 3)))
		elif iGoal == 1:
			iColonies = sd.getDutchColonies()
			aHelp.append(getIcon(iColonies >= 4) + localText.getText("TXT_KEY_VICTORY_EUROPEAN_COLONIES_CONQUERED", (iColonies, 4)))
		elif iGoal == 2:
			iNumSpices = pNetherlands.getNumAvailableBonuses(iSpices)
			aHelp.append(getIcon(iNumSpices >= 7) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_SPICE_RESOURCES", (iNumSpices, 7)))

	elif iPlayer == iGermany:
		if iGoal == 0:
			iCounter = 0
			for iSpecialist in lGreatPeople:
				iCounter += countCitySpecialists(iGermany, Areas.getCapital(iGermany), iSpecialist)
			aHelp.append(getIcon(iCounter >= 7) + localText.getText("TXT_KEY_VICTORY_GREAT_PEOPLE_IN_CITY", ("Berlin", iCounter, 7)))
		elif iGoal == 1:
			bFrance = checkOwnedCiv(iGermany, iFrance)
			bRome = checkOwnedCiv(iGermany, iItaly)
			bRussia = checkOwnedCiv(iGermany, iRussia)
			bEngland = checkOwnedCiv(iGermany, iEngland)
			bScandinavia = checkOwnedCiv(iGermany, iVikings)
			aHelp.append(getIcon(bRome) + localText.getText("TXT_KEY_CIV_ITALY_SHORT_DESC", ()) + ' ' + getIcon(bFrance) + localText.getText("TXT_KEY_CIV_FRANCE_SHORT_DESC", ()) + ' ' + getIcon(bScandinavia) + localText.getText("TXT_KEY_VICTORY_SCANDINAVIA", ()))
			aHelp.append(getIcon(bEngland) + localText.getText("TXT_KEY_CIV_ENGLAND_SHORT_DESC", ()) + ' ' + getIcon(bRussia) + localText.getText("TXT_KEY_CIV_RUSSIA_SHORT_DESC", ()))

	elif iPlayer == iAmerica:
		if iGoal == 0:
			bAmericas = isAreaFreeOfCivs(utils.getPlotList(tNCAmericaTL, tNCAmericaBR), lCivGroups[0])
			bMexico = isControlledOrVassalized(iAmerica, Areas.getCoreArea(iAztecs, True))
			aHelp.append(getIcon(bAmericas) + localText.getText("TXT_KEY_VICTORY_NO_NORTH_AMERICAN_COLONIES", ()) + ' ' + getIcon(bMexico) + localText.getText("TXT_KEY_CIV_MEXICO_SHORT_DESC", ()))
		elif iGoal == 1:
			bUnitedNations = sd.getWonderBuilder(iUnitedNations) == iAmerica
			bStatueOfLiberty = sd.getWonderBuilder(iStatueOfLiberty) == iAmerica
			bPentagon = sd.getWonderBuilder(iPentagon) == iAmerica
			bEmpireState = sd.getWonderBuilder(iEmpireStateBuilding) == iAmerica
			aHelp.append(getIcon(bStatueOfLiberty) + localText.getText("TXT_KEY_BUILDING_STATUE_OF_LIBERTY", ()) + ' ' + getIcon(bEmpireState) + localText.getText("TXT_KEY_BUILDING_EMPIRE_STATE_BUILDING", ()) + ' ' + getIcon(bPentagon) + localText.getText("TXT_KEY_BUILDING_PENTAGON", ()) + ' ' + getIcon(bUnitedNations) + localText.getText("TXT_KEY_BUILDING_UNITED_NATIONS", ()))
		elif iGoal == 2:
			iCounter = countResources(iAmerica, iOil)
			aHelp.append(getIcon(iCounter >= 10) + localText.getText("TXT_KEY_VICTORY_OIL_SECURED", (iCounter, 10)))

	elif iPlayer == iArgentina:
		if iGoal == 0:
			iGoldenAgeTurns = sd.getArgentineGoldenAgeTurns()
			aHelp.append(getIcon(iGoldenAgeTurns >= utils.getTurns(16)) + localText.getText("TXT_KEY_VICTORY_GOLDEN_AGES", (iGoldenAgeTurns / utils.getTurns(8), 2)))
		elif iGoal == 1:
			iCulture = getCityCulture(iArgentina, Areas.getCapital(iArgentina))
			aHelp.append(getIcon(iCulture >= utils.getTurns(25000)) + localText.getText("TXT_KEY_VICTORY_CITY_CULTURE", ("Buenos Aires", iCulture, utils.getTurns(25000))))
		elif iGoal == 2:
			iGoldenAgeTurns = sd.getArgentineGoldenAgeTurns()
			aHelp.append(getIcon(iGoldenAgeTurns >= utils.getTurns(40)) + localText.getText("TXT_KEY_VICTORY_GOLDEN_AGES", (iGoldenAgeTurns / utils.getTurns(8), 5)))

	elif iPlayer == iBrazil:
		if iGoal == 0:
			iSlavePlantations = countImprovements(iBrazil, iSlavePlantation)
			iPastures = countImprovements(iBrazil, iPasture)
			aHelp.append(getIcon(iSlavePlantations >= 10) + localText.getText("TXT_KEY_VICTORY_NUM_IMPROVEMENTS", (gc.getImprovementInfo(iSlavePlantation).getText(), iSlavePlantations, 10)) + ' ' + getIcon(iPastures >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_IMPROVEMENTS", (gc.getImprovementInfo(iPasture).getText(), iPastures, 4)))
		elif iGoal == 1:
			bWembley = sd.getWonderBuilder(iWembley) == iBrazil
			bCristoRedentor = sd.getWonderBuilder(iCristoRedentor) == iBrazil
			bThreeGorgesDam = sd.getWonderBuilder(iThreeGorgesDam) == iBrazil
			aHelp.append(getIcon(bWembley) + localText.getText("TXT_KEY_BUILDING_WEMBLEY", ()) + ' ' + getIcon(bCristoRedentor) + localText.getText("TXT_KEY_BUILDING_CRISTO_REDENTOR", ()) + ' ' + getIcon(bThreeGorgesDam) + localText.getText("TXT_KEY_BUILDING_THREE_GORGES_DAM", ()))
		elif iGoal == 2:
			iForestPreserves = countImprovements(iBrazil, iForestPreserve)
			bNationalPark = False
			capital = pBrazil.getCapitalCity()
			if capital: bNationalPark = capital.isHasRealBuilding(iNationalPark)
			aHelp.append(getIcon(iForestPreserves >= 20) + localText.getText("TXT_KEY_VICTORY_NUM_IMPROVEMENTS", (gc.getImprovementInfo(iForestPreserve).getText(), iForestPreserves, 20)) + ' ' + getIcon(bNationalPark) + localText.getText("TXT_KEY_VICTORY_NATIONAL_PARK_CAPITAL", ()))

	elif iPlayer == iCanada:
		if iGoal == 0:
			capital = pCanada.getCapitalCity()
			bAtlantic = capital and isConnectedByRailroad(iCanada, (capital.getX(), capital.getY()), lAtlanticCoast)
			bPacific = capital and isConnectedByRailroad(iCanada, (capital.getX(), capital.getY()), lPacificCoast)
			aHelp.append(getIcon(bAtlantic) + localText.getText("TXT_KEY_VICTORY_ATLANTIC_RAILROAD", ()) + ' ' + getIcon(bPacific) + localText.getText("TXT_KEY_VICTORY_PACIFIC_RAILROAD", ()))
		elif iGoal == 1:
			iCanadaWest, iTotalCanadaWest = countControlledTiles(iCanada, tCanadaWestTL, tCanadaWestBR, False, tCanadaWestExceptions)
			iCanadaEast, iTotalCanadaEast = countControlledTiles(iCanada, tCanadaEastTL, tCanadaEastBR, False, tCanadaEastExceptions)
			fCanada = (iCanadaWest + iCanadaEast) * 100.0 / (iTotalCanadaWest + iTotalCanadaEast)
			bAllCities = controlsAllCities(iCanada, tCanadaWestTL, tCanadaWestBR, tCanadaWestExceptions) and controlsAllCities(iCanada, tCanadaEastTL, tCanadaEastBR, tCanadaEastExceptions)
			aHelp.append(getIcon(fCanada >= 90.0) + localText.getText("TXT_KEY_VICTORY_CONTROL_CANADA", (str(u"%.2f%%" % fCanada), str(90))) + ' ' + getIcon(bAllCities) + localText.getText("TXT_KEY_VICTORY_CONTROL_CANADA_CITIES", ()))
		elif iGoal == 2:
			iPeaceDeals = sd.getCanadianPeaceDeals()
			aHelp.append(getIcon(iPeaceDeals >= 12) + localText.getText("TXT_KEY_VICTORY_CANADIAN_PEACE_DEALS", (iPeaceDeals, 12)))
			
	return aHelp