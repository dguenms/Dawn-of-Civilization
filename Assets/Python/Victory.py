# Rhye's and Fall of Civilization - Historical Victory Goals

from CvPythonExtensions import *
from StoredData import data
from Consts import *
from RFCUtils import utils
import heapq
import Areas
import CityNameManager as cnm
import DynamicCivs as dc
import PyHelpers
import BugCore
from operator import itemgetter
AdvisorOpt = BugCore.game.Advisors
AlertsOpt = BugCore.game.MoreCiv4lerts

### GLOBALS ###

gc = CyGlobalContext()
localText = CyTranslator()

PyPlayer = PyHelpers.PyPlayer

### CONSTANTS ###

# general constants
lWonders = [i for i in range(iBeginWonders, iNumBuildings)]
lGreatPeople = [iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy]

# Third Egyptian goal: Control Nubia and the Southern Levant in 1050 BC
tSouthLevantTL = (72, 37)
tSouthLevantBR = (74, 39)

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

# Chimu UP
tChimuBR = (23, 21)
tChimuTL = (27, 30)

# second Roman goal: control Iberia, Gaul, Britain, Africa, Greece, Asia Minor and Egypt in 320 AD
tFranceTL = (51, 47)

# second Roman goal: control Iberia, Gaul, Britain, Africa, Greece, Asia Minor and Egypt in 320 AD
# second Arabian goal: control or vassalize Spain, the Maghreb, Egypt, Mesopotamia and Persia in 1300 AD
tCarthageTL = (50, 36)
tCarthageBR = (61, 39)

tGermaniaTL = (58, 48)
tGermaniaBR = (65, 52)

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

# third Teotihuacan goal: control 100% of Mesoamerica in 1000 AD 
tMesoamericaTL = (15, 32)
tMesoamericaBR = (23, 40)

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

# second Turkic goal: create an overland trade route from a city in China to a Mediterranean port by 1100 AD
lMediterraneanPorts = [(66, 37), (66, 36), (67, 36), (68, 36), (69, 36), (70, 36), (71, 36), (72, 37), (73, 37), (73, 38), (73, 39), (73, 40), (73, 41), (73, 42), (71, 42), (70, 42), (70, 43), (69, 43), (69, 44), (68, 45)]

# first Mississippi goal: Control all tiles along the Mississippi River, Ohio River, and Great Lakes by 500 AD
lMississippiRiver = [(23, 42), (23, 43), (23, 44), (23, 45), (23, 46), (23, 47), (23, 48), (23, 49), (23, 50), (22, 46), (22, 47), (22, 48), (22, 49), (22, 50), (22, 51), (21, 49), (21, 50), (21, 51), (20, 50), (20, 51), (24, 43), (24, 44), (24, 45), (24, 46), (24, 47)]
lOhioRiver = [(24, 45), (24, 46), (24, 47), (25, 46), (25, 47), (26, 47), (27, 46), (27, 47)]
lGreatLakes = [(23, 48), (23, 49), (23, 50), (23, 51), (24, 48), (24, 51), (22, 51), (22, 52), (22, 53), (23, 53), (23, 54), (24, 54), (25, 54), (25, 53), (25, 52), (26, 52), (27, 52), (27, 51), (27, 50), (25, 50), (25, 49), (25, 48), (26, 49), (26, 48), (27, 48), (28, 48), (28, 49), (29, 49), (29, 50), (29, 51), (28, 51)]

# first Inuit goal: Settle Kivalliq, Kalaallit Nunaat, Qikiqtaaluk, and Nunavik by 1300AD

# Hudson Bay
lKivalliq = [(27, 61), (26, 62), (25, 62), (25, 61), (24, 61), (24, 60), (23, 60), (23, 59), (23, 58), (23, 57), (23, 56), (24, 56), (24, 55), (25, 55), (26, 55), (26, 54), (26, 53), (27, 53), (28, 53), (28, 54), (28, 55), (29, 55), (29, 56), (29, 57), (29, 58), (29, 59), (29, 60)]

# Quebec
tNunavikTL = (30, 53)
tNunavikBR = (36, 60)
tNunavikExceptions = ((30, 53), (30, 54))

# Baffin Island
tQikiqtaalukTL = (27, 61)
tQikiqtaalukBR = (34, 67)
tQikiqtaalukExceptions = ((27, 61))

# Greenland
tKalaallitNunaatTL = (37, 60)
tKalaallitNunaatBR = (45, 67)
tKalaallitNunaatExceptions = ((44, 64), (45, 63), (45, 62))

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
tAsiaTL = (73, 24)
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

# first Swedish goal: Control the Baltic Coast, the Kattegat and the Skagerak in 1700 AD
lSkagerrak = [(59, 57), (59, 56), (60, 56), (62, 56), (62, 57), (61, 58), (61, 59), (60, 59), (59, 59)]
lBalticSea = [(59, 56), (59, 55), (60, 56), (59, 54), (60, 54), (61, 54), (62, 54), (63, 54), (64, 54), (65, 54), (65, 55), (65, 56), (66, 56), (66, 57), (67, 57), (68, 57), (69, 57), (69, 58), (69, 59), (68, 59), (67, 59), (66, 59), (66, 60), (66, 61), (66, 62), (65, 62), (64, 62), (64, 61), (63, 61), (63, 60), (63, 59), (63, 58), (63, 57), (62, 56), (62, 57)]

# third Incan goal: control 60% of South America in 1700 AD
# second Colombian goal: control South America in 1920 AD
tSAmericaTL = (24, 3)
tSAmericaBR = (43, 32)
tSouthAmericaExceptions = ((24, 31), (25, 32))

# third Holy Roman goal: settle three great artists in Vienna by 1700 AD
# second Ottoman goal: control the Eastern Mediterranean, the Black Sea, Cairo, Mecca, Baghdad and Vienna by 1700 AD
tVienna = (62, 49)

# second Ottoman goal: control the Eastern Mediterranean, the Black Sea, Cairo, Mecca, Baghdad and Vienna by 1700 AD
tCairo = (69, 34)
tMecca = (75, 33)
tBaghdad = (77, 40)
lEasternMediterranean = [(58, 39), (58, 38), (58, 37), (59, 37), (60, 37), (61, 37), (61, 36), (62, 36), (63, 36), (64, 36), (65, 36), (66, 36), (67, 36), (68, 36), (69, 36), (70, 36), (71, 36), (65, 37), (66, 37), (72, 37), (73, 37), (73, 38), (73, 39), (73, 40), (73, 41), (73, 42), (70, 42), (71, 42), (72, 42), (69, 43), (70, 43), (69, 44), (68, 45), (67, 44), (67, 45), (66, 44), (65, 43), (66, 43), (65, 42), (66, 42), (67, 42), (67, 41), (65, 40), (66, 40)]
lBlackSea = [(69, 44), (70, 44), (71, 44), (71, 45), (72, 45), (73, 45), (73, 44), (74, 44), (75, 44), (76, 44), (76, 45), (76, 46), (76, 47), (75, 47), (74, 48), (75, 48), (72, 48), (74, 49), (73, 49), (71, 49), (69, 49), (69, 50), (70, 50), (71, 50), (72, 50), (73, 50), (68, 49), (68, 48), (67, 45), (67, 46), (67, 47), (67, 48), (68, 45)]

# third Thai goal: allow no foreign powers in South Asia in 1900 AD
tSouthAsiaTL = (88, 24)
tSouthAsiaBR = (110, 38)
lSouthAsianCivs = [iIndia, iTamils, iIndonesia, iKhmer, iMughals, iThailand, iVietnam]

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

# first Boer goal: Allow no European Colonies in South Africa by 1902 AD
tBoerAfricaTL = (61, 10)
tBoerAfricaBR = (72, 21)

# first Canadian goal: connect your capital to an Atlantic and a Pacific port by 1920 AD
lAtlanticCoast = [(34, 50), (33, 51), (35, 51), (30, 52), (31, 52), (32, 52), (30, 53), (35, 53), (30, 54), (31, 54), (32, 54), (35, 54), (36, 54), (32, 55), (33, 55), (34, 55)]
lPacificCoast = [(11, 51), (10, 52), (11, 53), (10, 56)]

# second Canadian goal: control all cities and 90% of the territory in Canada without ever conquering a city by 1950 AD
tCanadaWestTL = (10, 52)
tCanadaWestBR = (26, 61)
tCanadaWestExceptions = ((10, 59), (10, 60), (10, 61), (21, 61), (22, 61), (23, 61), (24, 61), (25, 61))
tCanadaEastTL = (27, 50)
tCanadaEastBR = (36, 59)
tCanadaEastExceptions = ((30, 50), (31, 50), (32, 50), (32, 51))

# first Australian goal: control Australia, New Zealand, New Guinea and 3 pacific islands in 1950 AD
tAustraliaTL = (103, 7)
tAustraliaBR = (118, 22)
tNewGuineaTL = (111, 24)
tNewGuineaBR = (117, 27)
tPacific1TL = (118, 18)
tPacific1BR = (123, 27)
tPacific2TL = (0, 16)
tPacific2BR = (21, 30)
tPacific3TL = (115, 32)
tPacific3BR = (122, 33)

# first Mamluk goal: Control Northern Africa, Hejaz, the Levant and Mesopotamia by 1300 AD
tHejazTL = (73, 30)
tHejazBR = (77, 36)
tHejazExceptions = [(73, 30), (76, 36), (77, 36), (77, 35)]
tLevantTL = (72, 37)
tLevantBR = (74, 41)

# second Mamluk goal: Make Cairo the most populous city in the world and have at least 30 population on the Lower Nile in 1380 AD
tLowerNileTL = (66, 29)
tLowerNileBR = (70, 36)

# first Zimbabwean goal: have monopoly on gold, silver, gems and ivory in sub-Sahara
tSubSaharaTL = (48, 10)
tSubSaharaBR = (79, 30)
tSubSaharaExceptions = ((76, 30), (77, 30))

# second Kievan Rus goal: control a continuous empire from the Barents Sea to the Mediterranean Sea in 1400 AD
lBarents = [(63, 64), (65, 64),  (65, 65), (66, 65), (67, 65), (67, 64), (68, 64), (69, 64),(70, 63), (69, 63), (68, 63), (68, 62), (68, 61), (69, 61), (70, 61), (70, 60), (71, 60), (72, 60), (72, 61), (72, 62), (73, 62), (73, 61), (74, 61), (75, 61), (75, 62), (76, 62), (77, 62), (78, 62), (78, 63), (79, 62)]
tMediterraneanCoastExceptions = ((51,36),(51,46),(52,46),(53,46),(53,47),(67,47),(67,46),(73,44),(73,45),(72,45),(71,45),(71,44),(70,44),(73,36),(51, 42),(51, 43),(51, 44),(51, 45),(52, 36),(52, 37),(52, 42),(52, 43),(52, 44),(52, 45),(53, 36),(53, 37),(53, 43),(53, 44),(53, 45),(54, 36),(54, 37),(54, 45),(54, 46),(54, 47),(55, 36),(55, 37),(55, 38),(55, 47),(56, 36),(56, 37),(56, 38),(56, 47),(57, 36),(57, 37),(57, 38),(57, 47),(58, 36),(58, 47),(59, 36),(59, 47),(60, 36),(64, 47),(65, 45),(65, 46),(65, 47),(66, 45),(66, 46),(66, 47),(71, 43),(72, 43),(72, 44),(73, 43))
lMediterraneanCoast = utils.getPlotList(tMediterraneanTL, tMediterraneanBR, tMediterraneanCoastExceptions)

tDanubeTL = (64, 46)
tDanubeBR = (68, 48)
lDanube = utils.getPlotList(tDanubeTL, tDanubeBR)
tZaysanTL = (89, 50)
tZaysanBR = (91, 53)
lZaysan = utils.getPlotList(tZaysanTL, tZaysanBR)

tLibyaTL = (60, 33)
tLibyaBR = (66, 37)
tNigeriaTL = (56, 25)
tNigeriaBR = (61, 28)
tCameroonTL = (60, 23)
tCameroonBR = (64, 27)

### GOAL CONSTANTS ###

dTechGoals = {
	iNorteChico: (1, [iWriting, iCalendar]),
	iChina: (1, [iCompass, iPaper, iGunpowder, iPrinting]),
	iBabylonia: (0, [iConstruction, iArithmetics, iWriting, iCalendar, iContract]),
	iGreece: (0, [iMathematics, iLiterature, iAesthetics, iPhilosophy, iMedicine]),
	iOlmecs: (2, [iCompass]),
	iRome: (2, [iArchitecture, iPolitics, iScholarship, iMachinery, iCivilService]),
	iKorea: (1, [iPrinting]),
	iPoland: (1, [iCivilLiberties]),
}

dEraGoals = {}

dWonderGoals = {
	iEgypt: (1, [iPyramids, iGreatLibrary, iGreatLighthouse], True),
	iNubia: (0, [iPyramids], False),
	iGreece: (2, [iColossus, iParthenon, iStatueOfZeus, iTempleOfArtemis], True),
	iCarthage: (0, [iGreatCothon], False),
	iPolynesia: (2, [iMoaiStatues], True),
	iMaya: (1, [iTempleOfKukulkan], True),
	iMississippi: (0, [iSerpentMound], False),
	iBurma: (0, [iShwedagonPaya], False),
	iMoors: (1, [iMezquita], False),
	iKhmer: (0, [iWatPreahPisnulok], False),
	iFrance: (2, [iNotreDame, iVersailles, iLouvre, iEiffelTower, iMetropolitain], True),
	iKievanRus: (0, [iSaintSophia], False),
	iMali: (1, [iUniversityOfSankore], False),
	iZimbabwe: (0, [iGreatZimbabwe], False),
	iItaly: (0, [iSanMarcoBasilica, iSistineChapel, iSantaMariaDelFiore], True),
	iMughals: (1, [iTajMahal, iRedFort, iShalimarGardens], True),
	iAmerica: (1, [iStatueOfLiberty, iBrooklynBridge, iEmpireStateBuilding, iGoldenGateBridge, iPentagon, iUnitedNations], True),
	iBrazil: (1, [iWembley, iCristoRedentor, iItaipuDam], True),
}

dReligionGoals = {}
		
### EVENT HANDLING ###

def setup():

	# 600 AD scenario: handle dates that have already been passed
	if utils.getScenario() == i600AD:
		for iPlayer in [iNubia, iEthiopia, iTamils, iCeltia, iMississippi]:
			loseAll(iPlayer)

	# 1700 AD scenario: handle dates that have already been passed
	if utils.getScenario() == i1700AD:
		for iPlayer in [iMoors, iChad, iNubia, iChina, iBurma, iIndia, iTamils, iKorea, iVikings, iTurks, iSpain, iHolyRome, iPoland, iPortugal, iMughals, iOttomans, iThailand, iKhmer, iKazakh, iCeltia]:
			loseAll(iPlayer)
			
		win(iPersia, 0)
		win(iJapan, 0)
		win(iFrance, 0)
		win(iCongo, 0)
		win(iSweden, 0)
		
		# French goal needs to be winnable
		data.setWonderBuilder(iNotreDame, iFrance)
		data.setWonderBuilder(iVersailles, iFrance)
		data.setWonderBuilder(iLouvre, iFrance)
		
		# help Congo
		data.iCongoSlaveCounter += 500
		
		# help Netherlands
		data.iDutchColonies += 2
	
	# ignore AI goals
	bIgnoreAI = (gc.getDefineINT("NO_AI_UHV_CHECKS") == 1)
	data.bIgnoreAI = bIgnoreAI
	
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
	if utils.getHumanID() != iPlayer and data.bIgnoreAI: return
	
	pPlayer = gc.getPlayer(iPlayer)
	
	if iPlayer == iEgypt:
	
		# first goal: have 500 culture in 850 BC and 5000 culture in 170 AD
		if isPossible(iEgypt, 0):
			if iGameTurn == getTurnForYear(-850):
				if pEgypt.countTotalCulture() < utils.getTurns(500):
					lose(iEgypt, 0)
					
			if iGameTurn == getTurnForYear(170):
				if pEgypt.countTotalCulture() >= utils.getTurns(5000):
					win(iEgypt, 0)
				else:
					lose(iEgypt, 0)
				
		# first goal: build the Pyramids, the Great Lighthouse and the Great Library by 100 BC
		if iGameTurn == getTurnForYear(-100):
			expire(iEgypt, 1)
				
		# third goal: Control Nubia and the Levant in 1050 AD
		bLevant = isControlled(iEgypt, utils.getPlotList(tSouthLevantTL, tSouthLevantBR))
		bNubia = isControlled(iEgypt, Areas.getNormalArea(iNubia))
		if iGameTurn == getTurnForYear(-1050):
			if bLevant and bNubia:
				win(iEgypt, 2)
			else:
				lose(iEgypt, 2)
		
				
	elif iPlayer == iBabylonia:
	
		# first goal: be the first to discover Construction, Arithmetics, Writing, Calendar and Contract
		
		# second goal: Make Babylon the most populous and culturally advanced city in the world in 850 BC
		if iGameTurn == getTurnForYear(-850):
			if isBestCity(iBabylonia, (76, 40), cityPopulation) and isBestCity(iBabylonia, (76, 40), cityCulture):
				win(iBabylonia, 1)
			else:
				lose(iBabylonia, 1)
			
		# third goal: Control the Levant in 550 BC
		if iGameTurn == getTurnForYear(-550):
			bLevant = isCultureControlled(iBabylonia, utils.getPlotList(tLevantTL, tLevantBR))
			if bLevant:
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
			
		# second goal: build three Baths and two Walls by 1500 BC
		if iGameTurn == getTurnForYear(-1500):
			expire(iHarappa, 1)
			
		# third goal: have a total population of 30 by 800 BC
		if isPossible(iHarappa, 2):
			if pHarappa.getTotalPopulation() >= 30:
				win(iHarappa, 2)
				
		if iGameTurn == getTurnForYear(-800):
			expire(iHarappa, 2)
				
	elif iPlayer == iNorteChico:
		# first goal: Have a capital with developing culture in 1800 BC
		if iGameTurn == getTurnForYear(-1800):
			if isPossible(iNorteChico, 0):
				if (pNorteChico.getCapitalCity().getCulture(iNorteChico) >= gc.getCultureLevelInfo(3).getSpeedThreshold(gc.getGame().getGameSpeedType())):
					win(iNorteChico, 0)
				else:
					lose(iNorteChico, 0)
		
		# second goal: Be the first to discover Writing and Calendar
		
		# third goal: Have a capital with 5 populations and 6 buildings in 1500 BC
		if iGameTurn == getTurnForYear(-1500):
			if isPossible(iNorteChico, 2):
				if cityPopulation(pNorteChico.getCapitalCity()) >= 5 and pNorteChico.getCapitalCity().getNumBuildings() >= 5:
					win(iNorteChico, 2)
				else:
					lose(iNorteChico, 2)
		
	elif iPlayer == iNubia:
		# first goal: Build the Pyramids in Kerma by 656 BC and Control Egypt for 1000 years
		if isPossible(iNubia, 0):
			bPyramids = isBuildingInCity((66, 31), iPyramids)
			bControlsEgypt = isControlled(iNubia, Areas.getCoreArea(iMamluks, False))
			if bControlsEgypt:
				data.iNubiaEgyptYears += gc.getGame().getTurnYear(iGameTurn) - gc.getGame().getTurnYear(iGameTurn - 1)
				if bPyramids and data.iNubiaEgyptYears >= 1000:
					win(iNubia, 0)
					
			if iGameTurn == getTurnForYear(-656):
				if not bPyramids:
					expire(iNubia, 0)
				
		# second goal: Control 2 Orthodox Cathedrals and have Pleased or better relations with 5 other Christian Civilizations in 1365
		if iGameTurn == getTurnForYear(1365):
			if isPossible(iNubia, 1):
				iNumOrthodoxCathedrals = getNumBuildings(iNubia, iOrthodoxCathedral)
				iNumPleasedOrBetterChristians = countPlayersWithAttitudeInGroup(iNubia, AttitudeTypes.ATTITUDE_PLEASED, getReligionPlayers(dc.lChristianity)) >= 5
				if iNumOrthodoxCathedrals >= 2 and iNumPleasedOrBetterChristians >= 5:
					win(iNubia, 1)
				else:
					lose(iNubia, 1)
					
		# third goal: Have the highest commerce output among Islamic civilizations and make Sennar the greatest city in all Africa by 1821
		if isPossible(iNubia, 2):
			iBestIslamicCommerceOutput = getBestPlayer(iNubia, playerCommerceOutput, getReligionPlayers([iIslam]))
			GreatestAfricanCity = getBestCityInRegion(lAfrica, cityValue)[0]
			bGreatestAfricanCityIsSennar = cnm.getFoundName(GreatestAfricanCity.getOwner(), (GreatestAfricanCity.plot().getX(), GreatestAfricanCity.plot().getY())) == 'Sennar'
			if iBestIslamicCommerceOutput == iNubia and bGreatestAfricanCityIsSennar:
				win(iNubia, 2)
				
			if iGameTurn == getTurnForYear(1821):
				expire(iNubia, 2)
			
	elif iPlayer == iChina:
	
		# first goal: build two Confucian and Taoist Cathedrals by 1000 AD
		if iGameTurn == getTurnForYear(1000):
			expire(iChina, 0)
			
		# second goal: be first to discover Compass, Gunpowder, Paper and Printing Press
		
		# third goal: experience four golden ages by 1800 AD
		if isPossible(iChina, 2):
			if data.iChineseGoldenAgeTurns >= utils.getTurns(32):
				win(iChina, 2)
				
			if pChina.isGoldenAge() and not pChina.isAnarchy():
				data.iChineseGoldenAgeTurns += 1
				
		if iGameTurn == getTurnForYear(1800):
			expire(iChina, 2)
			
	elif iPlayer == iGreece:
	
		# first goal: be the first to discover Mathematics, Literature, Aesthetics, Medicine and Philosophy
			
		# second goal: control Egypt, Phoenicia, Babylonia and Persia in 330 BC
		if iGameTurn == getTurnForYear(-330):
			bEgypt = checkOwnedCiv(iGreece, iEgypt)
			bPhoenicia = checkOwnedCiv(iGreece, iCarthage)
			bBabylonia = checkOwnedCiv(iGreece, iBabylonia)
			bPersia = checkOwnedCiv(iGreece, iPersia)
			if bEgypt and bPhoenicia and bBabylonia and bPersia:
				win(iGreece, 1)
			else:
				lose(iGreece, 1)
		
		# third goal: build the Parthenon, the Colossus, the Statue of Zeus and the Temple of Artemis by 250 BC
		if iGameTurn == getTurnForYear(-250):
			expire(iGreece, 2)
				
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
				
	elif iPlayer == iOlmecs:
		
		# first goal: build 4 culture-producing buildings by 400 BC
		if isPossible(iOlmecs, 0):
			iCultureBuildingCount = 0
			for city in utils.getCityList(iOlmecs):
				iCultureBuildingCount += countCultureBuildings(city)
			iCultureBuildingCount += getNumBuildings(iOlmecs, utils.getUniqueBuilding(iOlmecs, iPaganTemple))
			
			if iCultureBuildingCount >= 4:
				win(iOlmecs, 0)
		
		if iGameTurn == getTurnForYear(-400):
			expire(iOlmecs, 0)
		
		# second goal: discover Arithmetics, Writing and Calendar by 400 BC
		if iGameTurn == getTurnForYear(-400):
			expire(iOlmecs, 1)
		
		# third goal: be the first to discover Compass
	
	elif iPlayer == iCarthage:
	
		# first goal: build a Palace and the Great Cothon in Carthagee by 300 BC
		if isPossible(iCarthage, 0):
			bPalace = isBuildingInCity((58, 39), iPalace)
			bGreatCothon = isBuildingInCity((58, 39), iGreatCothon)
			if bPalace and bGreatCothon:
				win(iCarthage, 0)
		
		if iGameTurn == getTurnForYear(-300):
			expire(iCarthage, 0)
				
		# second goal: control Italy and Iberia in 100 BC
		if iGameTurn == getTurnForYear(-100):
			bItaly = isControlled(iCarthage, utils.getPlotList(Areas.tNormalArea[iItaly][0], Areas.tNormalArea[iItaly][1], [(62, 47), (63, 47), (63, 46)]))
			bIberia = isControlled(iCarthage, Areas.getNormalArea(iSpain, False))
			if bItaly and bIberia:
				win(iCarthage, 1)
			else:
				lose(iCarthage, 1)
				
		# third goal: have 5000 gold in 200 AD
		if iGameTurn == getTurnForYear(200):
			if pCarthage.getGold() >= utils.getTurns(5000):
				win(iCarthage, 2)
			else:
				lose(iCarthage, 2)
				
	elif iPlayer == iCeltia:
		# first goal: Raze 2 Capitals by 200 BC
		if isPossible(iCeltia, 0):
			if iGameTurn == getTurnForYear(-200):
				expire(iCeltia, 0)
		
		# second goal: Control 3 cities in Gallia and Germania and 1 in Italy, Iberia, and Britain in 1 BC
		if iGameTurn == getTurnForYear(-1):
			if isPossible(iCeltia, 1):
				iGallia =  getNumCitiesInArea(iCeltia, utils.getPlotList(tFranceTL, Areas.tNormalArea[iFrance][1]))
				if gc.getMap().plot(56, 46).isCity() and gc.getMap().plot(56, 46).getPlotCity().getOwner() == iCeltia:
					iGallia += 1
				iGermania = getNumCitiesInArea(iCeltia, utils.getPlotList(tGermaniaTL, tGermaniaBR))
				iItalia = getNumCitiesInRegions(iCeltia, [rItaly])
				iIberia = getNumCitiesInRegions(iCeltia, [rIberia])
				iBritannia = getNumCitiesInRegions(iCeltia, [rBritain])
				bControlled = iGallia >= 3 and iGermania >= 3 and iItalia >= 1 and iIberia >= 1 and iBritannia >= 1
				if bControlled:
					win(iCeltia, 1)
				else:
					lose(iCeltia, 1)
		
			# third goal: Be the most cultured Civilization in the world in 200 BC, 1 BC, and 60 AD
		if isPossible(iCeltia, 2):
			if iGameTurn in [getTurnForYear(-200), getTurnForYear(-1), getTurnForYear(60)]:
				if not isBestPlayer(iCeltia, playerTotalCulture):
					lose(iCeltia, 2)
				elif iGameTurn == getTurnForYear(60):
					win(iCeltia, 2)
		
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
	
		# first goal: build 6 Barracks, 5 Aqueducts, 4 Arenas and 3 Forums by 100 AD
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
		
	elif iPlayer == iMaya:
	
		# Maya
		if not pMaya.isReborn():
		
			# first goal: discover Calendar by 200 AD
			if iGameTurn == getTurnForYear(200):
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
				
				data.iColombianTradeGold += iTradeGold
				
				if data.iColombianTradeGold >= utils.getTurns(3000):
					win(iMaya, 2)
					
			if iGameTurn == getTurnForYear(1950):
				expire(iMaya, 2)
				
	elif iPlayer == iOman:
			# third goal: acquire 2000 gold from trade deals
			if isPossible(iOman, 2):
				iTradeGold = 0
				
				for iLoopPlayer in range(iNumPlayers):
					if pOman.getGoldPerTurnByPlayer(iLoopPlayer) > 0:
						iTradeGold += pOman.getGoldPerTurnByPlayer(iLoopPlayer)
				
				data.iOmaniTradeGold += iTradeGold
				
				if data.iOmaniTradeGold >= utils.getTurns(4000):
					win(iOman, 2)
		
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
			iTradeGold += iTradeCommerce * pTamils.getCommercePercent(0)
			
			# gold from per turn gold trade
			for iPlayer in range(iNumPlayers):
				iTradeGold += pTamils.getGoldPerTurnByPlayer(iPlayer) * 100
			
			data.iTamilTradeGold += iTradeGold
			
			if data.iTamilTradeGold / 100 >= utils.getTurns(4000):
				win(iTamils, 2)
				
		if iGameTurn == getTurnForYear(1200):
			expire(iTamils, 2)
					
	elif iPlayer == iEthiopia:
		
		# first goal: acquire three incense resources by 400 AD
		if isPossible(iEthiopia, 0):
			if pEthiopia.getNumAvailableBonuses(iIncense) >= 3:
				win(iEthiopia, 0)
				
		if iGameTurn == getTurnForYear(400):
			expire(iEthiopia, 0)
			
		# second goal: convert to Orthodoxy 5 turns after it is founded and have three settled Great Prophets and an Orthodox Cathedral by 1200 AD
		if isPossible(iEthiopia, 1):
			iNumOrthodoxCathedrals = getNumBuildings(iEthiopia, iOrthodoxCathedral)
			iGreatProphets = countSpecialists(iEthiopia, iSpecialistGreatProphet)
			if data.bEthiopiaConverted and iNumOrthodoxCathedrals >= 1 and iGreatProphets >= 3:
				win(iEthiopia, 1)
		
			if gc.getGame().isReligionFounded(iOrthodoxy) and iGameTurn > gc.getGame().getReligionGameTurnFounded(iOrthodoxy) + utils.getTurns(5):
				if not data.bEthiopiaConverted:
					expire(iEthiopia, 1)
				
		if iGameTurn == getTurnForYear(1200):
			expire(iEthiopia, 1)
			
		# third goal: make sure there are more Orthodox than Muslim cities in Africa in 1500 AD
		if iGameTurn == getTurnForYear(1500):
			iOrthodoxCities = countRegionReligion(iOrthodoxy, lAfrica)
			iMuslimCities = countRegionReligion(iIslam, lAfrica)
			if iOrthodoxCities > iMuslimCities:
				win(iEthiopia, 2)
			else:
				lose(iEthiopia, 2)
				
	elif iPlayer == iVietnam:
		# first goal: have 8000 culture by 1200 AD
		if isPossible(iVietnam, 0):
			if pVietnam.countTotalCulture() >= utils.getTurns(8000):
				win(iVietnam, 0)
				
		if iGameTurn == getTurnForYear(1200):
			expire(iVietnam, 0)
			
		# second goal: create three great generals by 1500 AD
		if iGameTurn == getTurnForYear(1500):
			expire(iVietnam, 1)
			
		# third goal: never lose a single city until 1950 AD and allow no foreign powers in South Asia in 1950 AD
		if iGameTurn == getTurnForYear(1950):
			if isPossible(iVietnam, 2):
				if isAreaOnlyCivs(tSouthAsiaTL, tSouthAsiaBR, lSouthAsianCivs):
					win(iVietnam, 2)
				else:
					lose(iVietnam, 2)
				
	elif iPlayer == iTeotihuacan:
		
		# first goal: have 500 culture in 550
		if iGameTurn == getTurnForYear(550):
			if isPossible(iTeotihuacan, 0):
				if pTeotihuacan.countTotalCulture() >= utils.getTurns(500):
					win(iTeotihuacan, 0)
				else:
					lose(iTeotihuacan, 0)
			
		# second goal: experience a golden age by 550 AD
		if isPossible(iTeotihuacan, 1):
			if data.iTeotihuacanGoldenAgeTurns >= utils.getTurns(8):
				win(iTeotihuacan, 1)
				
			if pTeotihuacan.isGoldenAge() and not pTeotihuacan.isAnarchy():
				data.iTeotihuacanGoldenAgeTurns += 1
				
		if iGameTurn == getTurnForYear(550):
			expire(iTeotihuacan, 1)
		
		# third goal: control all tiles in Mesoamerica in 1000 AD
		if iGameTurn == getTurnForYear(1000):
			if isPossible(iTeotihuacan, 2):
				iMesoamericaTiles, iTotalMesoamericaTiles = countControlledTiles(iTeotihuacan, tMesoamericaTL, tMesoamericaBR, False)
				percentMesoamerica = iMesoamericaTiles * 100.0 / iTotalMesoamericaTiles
				if percentMesoamerica >= 99.5:
					win(iTeotihuacan, 2)
				else: 
					lose(iTeotihuacan, 2)
				
	elif iPlayer == iInuit:
		# first goal: Settle Kivalliq, Kalaallit Nunaat, Qikiqtaaluk, and Nunavik by 900 AD
		if isPossible(iInuit, 0):
			bKivalliq = False
			bNunavik = False
			bKalaallitNunaat = False
			bQikiqtaaluk = False
			
			for city in utils.getCityList(iPlayer):
				tCity = (city.getX(), city.getY)
				
				if (tCity in lKivalliq):
					bKivalliq = True
				
				if utils.isPlotInArea(tCity, tNunavikTL, tNunavikBR, tNunavikExceptions):
					bNunavik = True
					
				if utils.isPlotInArea(tCity, tKalaallitNunaatTL, tKalaallitNunaatBR, tKalaallitNunaatExceptions):
					bKalaallitNunaat = True
					
				if utils.isPlotInArea(tCity, tQikiqtaalukTL, tQikiqtaalukBR, tQikiqtaalukExceptions):
					bQikiqtaaluk = True
					
				if bKivalliq and tNunavik and tKalaallitNunaat and tQikiqtaaluk:
					win(iInuit, 0)
					break
					
		if iGameTurn == getTurnForYear(900):
			expire(iInuit, 0)
			
		
		# second goal: Acquire 25 Resources
		if isPossible(iInuit, 1):
			iNumResources = 0
			for iBonus in range(iNumBonuses):
				iNumResources += countResources(iInuit, iBonus)
				
				if iNumResources >= 25:
					win(iInuit, 1)
					break
					
		# third goal: Control and work more Ocean, Coast, and Lake tiles than any other civilization
		if isPossible(iInuit, 2):
			iBestPlayerOwner = -1
			iBestScoreOwner = -1
			iBestPlayerWorker = -1
			iBestScoreWorker= -1
			
			for iLoopPlayer in range(iNumMajorPlayers):
				lNumWater = countControlledTerrain(iLoopPlayer, [iCoast, iOcean], True)
				if lNumWater[0] > iBestScoreOwner or (lNumWater[0] == iBestScoreOwner and iBestPlayerOwner == iPlayer):
					iBestScoreOwner = lNumWater[0]
					iBestPlayerOwner = iLoopPlayer
					
				if lNumWater[1] > iBestPlayerWorker or (lNumWater[1] == iBestScoreWorker and iBestPlayerWorker == iPlayer):
					iBestScoreWorker = lNumWater[1]
					iBestPlayerWorker = iLoopPlayer
					
			if iBestPlayerOwner == iPlayer and iBestPlayerWorker == iPlayer:
				win(iInuit, 2)
		
	elif iPlayer == iMississippi:
		# first goal: Control all tiles along the Mississippi River, Ohio River, and Great Lakes by 500 AD
		if isPossible(iMississippi, 0):
			bMississippiRiver = isCultureControlled(iMississippi, lMississippiRiver, True, True)
			bOhioRiver = isCultureControlled(iMississippi, lOhioRiver, True, True)
			bGreatLakes = isCultureControlled(iMississippi, lGreatLakes, True, True)
			if bMississippiRiver and bOhioRiver and bGreatLakes:
				win(iMississippi, 0)
				
		if iGameTurn == getTurnForYear(500):
			expire(iMississippi, 0)
				
		# second goal: Build the Serpent Mound and 7 Effigy Mounds by 1070 AD
		if isPossible(iMississippi, 1):
			bEffigyMound = getNumBuildings(iPlayer, iEffigyMound) >= 7
			
			if bEffigyMound:
				win(iMississippi, 1)
				
		if iGameTurn == getTurnForYear(1070):
			expire(iMississippi, 1)
			
		# third goal: Build a palace and settle 2 great merchants in Cahokia by 1400 AD
		if isPossible(iMississippi, 2):
			bPalace = cnm.getFoundName(iMississippi, (pMississippi.getCapitalCity().getX(), pMississippi.getCapitalCity().getY())) == "Cahokia"
			bMerchant = countCitySpecialists(iMississippi, (pMississippi.getCapitalCity().getX(), pMississippi.getCapitalCity().getY()), iSpecialistGreatMerchant) >= 2
			
			if bPalace and bMerchant:
				win(iMississippi, 2)
				
		if iGameTurn == getTurnForYear(1400):
			expire(iMississippi, 2)
			
	elif iPlayer == iKorea:
	
		# first goal: build a Buddhist Stupa and a Confucian Academy by 1200 AD
		if iGameTurn == getTurnForYear(1200):
			expire(iKorea, 0)
			
		# second goal: be first to discover Printing Press
		
		# third goal: sink 20 enemy ships
					
	elif iPlayer == iTiwanaku:
		
		# first goal: Build the Gate of Sun and settle a Great Prophet in your capital by 900 AD
		if isPossible(iTiwanaku, 0):
			bGateOfTheSun = data.getWonderBuilder(iGateOfTheSun) == iTiwanaku
			iGreatProphets = countCitySpecialists(iTiwanaku, (pTiwanaku.getCapitalCity().getX(), pTiwanaku.getCapitalCity().getY()), iSpecialistGreatProphet)
			if bGateOfTheSun and iGreatProphets >= 1:
				win(iTiwanaku, 0)
		
		if iGameTurn == getTurnForYear(900):
			expire(iTiwanaku, 0)
				
		# second goal: Have two cities with refined culture by 1000 AD
		if isPossible(iTiwanaku, 1):
			iRefined = countCitiesWithCultureLevel(iTiwanaku, 4)
			
			if iRefined >= 2:
				win(iTiwanaku, 1)
				
		if iGameTurn == getTurnForYear(1000):
			expire(iTiwanaku, 1)
					
		# third goal: Experiece two golden ages by 1100 AD
		if isPossible(iTiwanaku, 2):
			if pTiwanaku.isGoldenAge() and not pTiwanaku.isAnarchy():
				data.iTiwanakuGoldenAgeTurns += 1
			
			if data.iTiwanakuGoldenAgeTurns >= utils.getTurns(16):
				win(iTiwanaku, 2)
				
		if iGameTurn == getTurnForYear(1100):
			expire(iTiwanaku, 2)
		
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
			
	elif iPlayer == iWari:
		
		# first goal: Acquire gold, dyes, cotton, and sheep and have at least 500 Culture by 900 AD
		if isPossible(iWari, 0):
			bGold = pWari.getNumAvailableBonuses(iGold) >= 1
			bDye = pWari.getNumAvailableBonuses(iDye) >= 1
			bCotton = pWari.getNumAvailableBonuses(iCotton) >= 1
			bSheep = pWari.getNumAvailableBonuses(iSheep) >= 1
			bCulture = pWari.countTotalCulture() >= utils.getTurns(500)
			
			if bGold and bDye and bCotton and bSheep and bCulture:
				win(iWari, 0)
			
		if iGameTurn == getTurnForYear(900):
			expire(iWari, 0)
			
		# second goal: Build 3 barracks and colcas and connect your cities by road by 1000 AD
		if isPossible(iWari, 1):
			iNumBarracks = getNumBuildings(iWari, iBarracks)
			iNumColcas = getNumBuildings(iWari, iColcas)
			bRoute = True
			for city in utils.getCityList(iPlayer):
				if city.getX() == pWari.getCapitalCity().getX() and city.getY() == pWari.getCapitalCity().getY(): continue
				if not isConnectedByRoute(iWari, (pWari.getCapitalCity().getX(), pWari.getCapitalCity().getY()), [(city.getX(), city.getY())]):
					bRoute = False
					break
			if iNumBarracks >= 3 and iNumColcas >= 3 and bRoute:
				win(iWari, 1)
		
		if iGameTurn == getTurnForYear(1000):
			expire(iWari, 1)
			
		# third goal: Have four cities with developing culture and 5 population by 1100 AD
		if isPossible(iWari, 2):
			iDual = countCitiesWithCultureLevelAndSize(iWari, 3, 5)
			if iDual >= 4:
				win(iWari, 2)
		
		if iGameTurn ==getTurnForYear(1100):
			expire(iWari, 2)
					
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
				
		# third goal: be the first to discover 5 modern techs
		
	elif iPlayer == iVikings:
	
		# first goal: control the core of a European civilization in 1050 AD
		if iGameTurn == getTurnForYear(1050):
			lEuroCivs = [iLoopPlayer for iLoopPlayer in lCivGroups[0] if tBirth[iLoopPlayer] < 1050 and iPlayer != iLoopPlayer]
			if isCoreControlled(iVikings, lEuroCivs):
				win(iVikings, 0)
			else:
				lose(iVikings, 0)
				
		# second goal: found a city in America by 1100 AD
		if iGameTurn == getTurnForYear(1100):
			expire(iVikings, 1)
			
		# third goal: acquire 3000 gold by pillaging, conquering cities and sinking ships by 1500 AD
		if isPossible(iVikings, 2):
			if data.iVikingGold >= utils.getTurns(3000):
				win(iVikings, 2)
				
		if iGameTurn == getTurnForYear(1500):
			expire(iVikings, 2)
			
	elif iPlayer == iTurks:
	
		# first goal: control 6% of the world's territory and pillage 20 improvements by 900 AD
		if isPossible(iTurks, 0):
			if getLandPercent(iTurks) >= 5.995 and data.iTurkicPillages >= 20:
				win(iTurks, 0)
				
		if iGameTurn == getTurnForYear(900):
			expire(iTurks, 0)
			
		# second goal: create an overland trade route between a Chinese and a Mediterranean city and spread the Silk Route to ten of your cities by 1100 AD
		if isPossible(iTurks, 1):
			if isConnectedByTradeRoute(iTurks, utils.getPlotList(tChinaTL, tChinaBR), lMediterraneanPorts) and pTurks.countCorporations(iSilkRoute) >= 10:
				win(iTurks, 1)
				
		if iGameTurn == getTurnForYear(1100):
			expire(iTurks, 1)
			
		# third goal: have a capital with developing culture by 900 AD, a different capital with refined culture by 1100 AD and another capital with influential culture by 1400 AD
		if isPossible(iTurks, 2):
			capital = pTurks.getCapitalCity()
			tCapital = (capital.getX(), capital.getY())
			
			if iGameTurn <= getTurnForYear(900):
				if not data.tFirstTurkicCapital and capital.getCulture(iTurks) >= gc.getCultureLevelInfo(3).getSpeedThreshold(gc.getGame().getGameSpeedType()):
					data.tFirstTurkicCapital = tCapital
			
			if iGameTurn <= getTurnForYear(1100):
				if data.tFirstTurkicCapital and not data.tSecondTurkicCapital and tCapital != data.tFirstTurkicCapital and capital.getCulture(iTurks) >= gc.getCultureLevelInfo(4).getSpeedThreshold(gc.getGame().getGameSpeedType()):
					data.tSecondTurkicCapital = tCapital
					
			if iGameTurn <= getTurnForYear(1400):
				if tCapital != data.tFirstTurkicCapital and tCapital != data.tSecondTurkicCapital and data.tFirstTurkicCapital and data.tSecondTurkicCapital and capital.getCulture(iTurks) >= gc.getCultureLevelInfo(5).getSpeedThreshold(gc.getGame().getGameSpeedType()):
					win(iTurks, 2)
					
		if iGameTurn == getTurnForYear(900):
			if not data.tFirstTurkicCapital:
				expire(iTurks, 2)
				
		if iGameTurn == getTurnForYear(1100):
			if not data.tSecondTurkicCapital:
				expire(iTurks, 2)
				
		if iGameTurn == getTurnForYear(1400):
			expire(iTurks, 2)
			
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
		
		# third goal: spread Islam to 30% of the cities in the world
		if isPossible(iArabia, 2):
			if gc.getGame().calculateReligionPercent(iIslam) >= 30.0:
				win(iArabia, 2)
				
	elif iPlayer == iTibet:
	
		# first goal: acquire five cities by 1000 AD
		if iGameTurn == getTurnForYear(1000):
			expire(iTibet, 0)
			
		# second goal: spread Buddhism to 25% by 1400 AD
		if isPossible(iTibet, 1):
			if gc.getGame().calculateReligionPercent(iBuddhism) >= 25.0:
				win(iTibet, 1)
				
		if iGameTurn == getTurnForYear(1400):
			expire(iTibet, 1)
			
		# third goal: settle five great prophets in Lhasa by 1700 AD
		if isPossible(iTibet, 2):
			if countCitySpecialists(iTibet, Areas.getCapital(iPlayer), iSpecialistGreatProphet) >= 5:
				win(iTibet, 2)
				
		if iGameTurn == getTurnForYear(1700):
			expire(iTibet, 2)
			
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
		
		# third goal: Have the largest population among Islamic nations and control Cathedrals of 3 different religions in 1700 AD
		if iGameTurn == getTurnForYear(1700):
			bIslamicPop = isBestPlayer(iIndonesia, playerRealPopulation, getReligionPlayers([iIslam]))
			iNumCathedrals = 0
			
			for iReligion in range(iNumReligions):
				if getNumBuildings(iIndonesia, iJewishCathedral + 4 * iReligion) >= 1:
					iNumCathedrals += 1
				
			if bIslamicPop and iNumCathedrals >= 3:
				win(iIndonesia, 2)
			else:
				lose(iIndonesia, 2)
			
	elif iPlayer == iBurma:
		# first goal: Build the Shwedagon Paya, 2 Buddhist Temples, and 2 Buddhist Monasteries by 1000 AD
		if iGameTurn == getTurnForYear(1000):
			expire(iBurma, 0)
		
		# second goal: Have five Great Priests, Great Scientists, or Great Artists and one of each settled in your cities in 1211 AD
		if iGameTurn == getTurnForYear(1211):
			iProphets = 0
			iScientists = 0
			iArtists = 0
			for city in utils.getCityList(iPlayer):
				iProphets += city.getFreeSpecialistCount(iSpecialistGreatProphet)
				iScientists += city.getFreeSpecialistCount(iSpecialistGreatScientist)
				iArtists += city.getFreeSpecialistCount(iSpecialistGreatArtist)
			iSpecialists = iProphets + iScientists + iArtists
			
			bProphets = iProphets >= 1
			bScientists = iScientists >= 1
			bArtists = iArtists >= 1
			bSpecialists = iSpecialists >= 5
			if bProphets and bScientists and bArtists and bSpecialists:
				win(iBurma, 1)
			else:
				lose(iBurma, 1)
		
		# third goal: Control all of Indochina in 1580 AD
		if iGameTurn == getTurnForYear(1580):
			if isPossible(iBurma, 2):
				bIndochina = isControlled(iBurma, utils.getPlotList(tIndochinaTL, tIndochinaBR, tIndochinaExceptions))
				if bIndochina:
					win(iBurma, 2)
				else:
					lose(iBurma, 2)
				
	elif iPlayer == iKhazars:
		# first goal: Conduct a Diplomatic mission in a European City controlled by a Muslim Civilization by 1031 AD
		if iGameTurn == getTurnForYear(1031):
			expire(iKhazars, 0)
		
		# second goal: Have 10 Religious Happiness and a larger Jewish population than any other nation in 1031 AD
		if iGameTurn == getTurnForYear(1031):
			if isPossible(iKhazars, 1):
				iLeader, iPopulation = getLargestReligionPopulation(iReligion)
				if iLeader == iKhazars and getReligionHappiness(iKhazars) >= 10:
					win(iKhazars, 1)
				else:
					lose(iKhazars, 1)
				
		# third goal: Control a continuous empire from the Danube River to Lake Zaysan in 1241 AD
		if iGameTurn == getTurnForYear(1241):
			if isPossible(iKhazars, 2):
				if isConnectedByLand(iKhazars, lDanube, lZaysan):
					win(iKhazars, 2)
				else:
					lose(iKhazars, 2)
				
	elif iPlayer == iChad:
		if iGameTurn == getTurnForYear(1259):
			expire(iChad, 0)
			
		if iGameTurn == getTurnForYear(1380):
			expire(iChad, 1)
			
		if isPossible(iChad, 2):
			bCameroon = isControlled(iChad, utils.getPlotList(tCameroonTL, tCameroonBR))
			bNigeria = isControlled(iChad, utils.getPlotList(tNigeriaTL, tNigeriaBR))
			bLibya = isControlled(iChad, utils.getPlotList(tLibyaTL, tLibyaBR))
			if bCameroon and bNigeria and bLibya:
				lAfricaCivs = getCivsWithHoldingsInRegion(lAfrica)
				bArmy = isBestPlayer(iChad, playerArmyPower, lAfricaCivs)
				if bArmy:
					win(iChad, 2)
				
		if iGameTurn == getTurnForYear(1603):
			expire(iChad, 2)
				
	elif iPlayer == iMoors:
	
		# first goal: control three cities in the Maghreb and conquer two cities in Iberia and West Africa
		if iGameTurn == getTurnForYear(1200):
			bIberia = getNumConqueredCitiesInArea(iMoors, utils.getPlotList(tIberiaTL, tIberiaBR)) >= 2
			bMaghreb = getNumCitiesInArea(iMoors, utils.getPlotList(tMaghrebTL, tMaghrebBR)) >= 3
			bWestAfrica = getNumConqueredCitiesInArea(iMoors, utils.getPlotList(tWestAfricaTL, tWestAfricaBR)) >= 2
			
			if bIberia and bMaghreb and bWestAfrica:
				win(iMoors, 0)
			else:
				lose(iMoors, 0)
				
		# second goal: build La Mezquita and settle four great prophets, scientists or engineers in Cordoba by 1300 AD
		if isPossible(iMoors, 1):
			bMezquita = data.getWonderBuilder(iMezquita) == iMoors
		
			iCounter = 0
			iCounter += countCitySpecialists(iMoors, (51, 41), iSpecialistGreatProphet)
			iCounter += countCitySpecialists(iMoors, (51, 41), iSpecialistGreatScientist)
			iCounter += countCitySpecialists(iMoors, (51, 41), iSpecialistGreatEngineer)
			
			if bMezquita and iCounter >= 4:
				win(iMoors, 1)
				
		if iGameTurn == getTurnForYear(1300):
			expire(iMoors, 1)
				
		# third goal: acquire 3000 gold through piracy by 1650 AD
		if isPossible(iMoors, 2):
			if data.iMoorishGold >= utils.getTurns(3000):
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
			
		# third goal: spread Catholicism to 30% and allow no Protestant civilizations in Europe in 1650 AD
		if iGameTurn == getTurnForYear(1650):
			fReligionPercent = gc.getGame().calculateReligionPercent(iCatholicism)
			
			bProtestantsEurope = isStateReligionInArea(iProtestantism, tEuropeTL, tEuropeBR)
			bProtestantsEasternEurope = isStateReligionInArea(iProtestantism, tEasternEuropeTL, tEasternEuropeBR)
			
			if fReligionPercent >= 30.0 and not bProtestantsEurope and not bProtestantsEasternEurope:
				win(iSpain, 2)
			else:
				lose(iSpain, 2)
				
	elif iPlayer == iFrance:
	
		# first goal: have legendary culture in Paris in 1700 AD
		if iGameTurn == getTurnForYear(1700):
			if getCityCulture(iFrance, (55, 50)) >= utils.getTurns(50000):
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
				
		# third goal: build Notre Dame, Versailles, the Louvre, the Eiffel Tower and the Metropolitain by 1900 AD
		if iGameTurn == getTurnForYear(1900):
			expire(iFrance, 2)
			
	elif iPlayer == iKhmer:
	
		# first Khmer goal: build four Buddhist and Hindu monasteries and Wat Preah Pisnulok in 1200 AD
		if iGameTurn == getTurnForYear(1200):
			if isPossible(iKhmer, 0):
				iBuddhist = getNumBuildings(iKhmer, iBuddhistMonastery)
				iHindu = getNumBuildings(iKhmer, iHinduMonastery)
				bWatPreahPisnulok = data.getWonderBuilder(iWatPreahPisnulok) == iKhmer
				if iBuddhist >= 4 and iHindu >= 4 and bWatPreahPisnulok:
					win(iKhmer, 0)
				else:
					lose(iKhmer, 0)
				
		# second goal: have an average city size of 12 in 1450 AD
		if iGameTurn == getTurnForYear(1450):
			if isPossible(iKhmer, 1):
				if getAverageCitySize(iKhmer) >= 12.0:
					win(iKhmer, 1)
				else:
					lose(iKhmer, 1)
			
		# third goal: have 8000 culture by 1450 AD
		if isPossible(iKhmer, 2):
			if pKhmer.countTotalCulture() >= utils.getTurns(8000):
				win(iKhmer, 2)
				
		if iGameTurn == getTurnForYear(1450):
			expire(iKhmer, 2)
			
	elif iPlayer == iMuisca:
		# first goal: Spend 1000 Gold in diplomacy by 1540 AD
		if isPossible(iMuisca, 1):
			iTradeGold = 0
			
			for iLoopPlayer in range(iNumPlayers):
				iTradeGold += gc.getPlayer(iLoopPlayer).getGoldPerTurnByPlayer(iMuisca)
			
			data.iMuiscaTradeGold += iTradeGold
			
			if data.iMuiscaTradeGold >= utils.getTurns(2000):
				win(iMuisca, 1)
				
		if iGameTurn == getTurnForYear(1540):
			expire(iMuisca, 1)
			
		# second goal: Control 25% of the New World population and the largest average city population in the New World at the time of Old World contact
		
		# third goal: Ensure no Old World civilization controls a silver or gold resource in South or Central America in 1600 AD
		if iGameTurn == getTurnForYear(1600):
			if isPossible(iMuisca, 2):
				if countControlledResourcesInRegions(lCivBioOldWorld, lSouthAmerica, [iGold, iSilver], iMine) >= 0:
					lose(iMuisca, 2)
				if not isLost(iMuisca, 2):
					win(iMuisca, 2)
					
	elif iPlayer == iYemen:
		# second goal: Control Mecca in 1265
		if iGameTurn == getTurnForYear(1265):
			if isPossible(iYemen, 1):
				if controlsCity(iYemen, tMecca):
					win(iYemen, 1)
				else:
					lose(iYemen, 1)
			
		# first goal: Control more culture producing buildings in your capital than any other nation in 1229
		if iGameTurn == getTurnForYear(1229):
			if isPossible(iYemen, 0):
				if getCapitalCultureBuildingsLeader()[0] == iYemen:
					win(iYemen, 0)
				else:
					lose(iYemen, 0)
				
		
	elif iPlayer == iEngland:
	
		# first goal: colonize every continent by 1730 AD
		if iGameTurn == getTurnForYear(1730):
			expire(iEngland, 0)
			
		# second goal: control a total of 25 frigates and ships of the line and sink 50 enemy ships by 1800 AD
		if isPossible(iEngland, 1):
			iEnglishNavy = 0
			iEnglishNavy += pEngland.getUnitClassCount(gc.getUnitInfo(iFrigate).getUnitClassType())
			iEnglishNavy += pEngland.getUnitClassCount(gc.getUnitInfo(iShipOfTheLine).getUnitClassType())
			
			if iEnglishNavy >= 25 and data.iEnglishSinks >= 50:
				win(iEngland, 1)
		
		if iGameTurn == getTurnForYear(1800):
			expire(iEngland, 1)
			
		# third goal: be the first to enter the Industrial and Modern eras
		
	elif iPlayer == iHolyRome:
	
		# first goal: control Saint Peter's Basilica in 1000 AD, the Church of the Anastasis in 1200 AD and All Saint's Church in 1550 AD
		if iGameTurn == getTurnForYear(1000):
			if isPossible(iHolyRome, 0):
				if getNumBuildings(iHolyRome, iCatholicShrine) > 0:
					data.lHolyRomanShrines[0] = True
				else:
					expire(iHolyRome, 0)
					
		if iGameTurn == getTurnForYear(1200):
			if isPossible(iHolyRome, 0):
				if getNumBuildings(iHolyRome, iOrthodoxShrine) > 0:
					data.lHolyRomanShrines[1] = True
				else:
					expire(iHolyRome, 0)
					
		if iGameTurn == getTurnForYear(1550):
			if isPossible(iHolyRome, 0):
				if getNumBuildings(iHolyRome, iProtestantShrine) > 0:
					data.lHolyRomanShrines[2] = True
					win(iHolyRome, 0)
				else:
					expire(iHolyRome, 0)

		# second goal: have three Catholic vassals in Europe by 1650 AD
		if isPossible(iHolyRome, 1):
			if countVassals(iHolyRome, lCivGroups[0], iCatholicism) >= 3:
				win(iHolyRome, 1)
		
		if iGameTurn == getTurnForYear(1650):
			expire(iHolyRome, 1)
		
		# third goal: settle a total of ten great artists and statesmen in Vienna and have pleased or better relations with eight independent European civilizations by 1850 AD
		if isPossible(iHolyRome, 2):
			iGreatArtists = countCitySpecialists(iHolyRome, tVienna, iSpecialistGreatArtist)
			iGreatStatesmen = countCitySpecialists(iHolyRome, tVienna, iSpecialistGreatStatesman)
			iPleasedOrBetterEuropeans = countPlayersWithAttitudeInGroup(iHolyRome, AttitudeTypes.ATTITUDE_PLEASED, lCivGroups[0])
			
			if iGreatArtists + iGreatStatesmen >= 10 and iPleasedOrBetterEuropeans >= 8:
				win(iHolyRome, 2)
		
		if iGameTurn == getTurnForYear(1850):
			expire(iHolyRome, 2)
			
	elif iPlayer == iKievanRus:
		
		# first goal: build the St. Sophia Cathedral and 1 Orthodox Cathedrals by 1327 AD
		
		if isPossible(iKievanRus, 0):
			iCathedral = getNumBuildings(iKievanRus, iOrthodoxCathedral)
			bSophia = data.getWonderBuilder(iSaintSophia) == iKievanRus
			if iCathedral >= 1 and bSophia:
				win(iKievanRus, 0)
				
		if iGameTurn == getTurnForYear(1327):
			expire(iKievanRus, 0)
			
		# second goal: control a continuous empire from the Barents Sea to the Mediterranean Sea
		if isPossible(iKievanRus, 1):
			if isConnectedByLand(iKievanRus, lMediterraneanCoast, lBarents):
				win(iKievanRus, 1)
			
		# third goal: Conduct two trade or diplomatic missions with the most prominent (top scoring) European civilization by 1327 AD
		if isPossible(iKievanRus, 2):
			if data.iKievanRusMissions >= 2:
				win(iKievanRus, 2)
		
		if iGameTurn == getTurnForYear(1327):
			expire(iKievanRus, 2)
			
	elif iPlayer == iHungary:
		# Control 20% of Europe in 1301 AD
		if iGameTurn == getTurnForYear(1327):
			if isPossible(iHungary, 0):
				iEurope, iTotalEurope = countControlledTilesInRegions(iPlayer, [rIberia, rEurope, rItaly, rBalkans], False, True)
				fEurope = (iEurope) * 100.0 / (iTotalEurope)
				if fEurope >= 19.995:
					win(iHungary, 0)
				else:
					lose(iHungary, 0)
		# Be the first to adopt Tolerance and have Friendly Relations with 5 Catholic Civs in 1867 AD
		if iGameTurn == getTurnForYear(1867):
			if isPossible(iHungary, 1):
				iCount = countPlayersWithAttitudeAndReligion(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY, iCatholicism, True)
				if data.bHungaryTolerance and iCount >= 5:
					win(iHungary, 1)
				else:
					lose(iHungary, 1)
		# Win and attend the congress for two world wars
		if isPossible(iHungary, 2):
			if data.iHungaryGlobalWars >= 2:
				win(iHungary, 2)
			
	elif iPlayer == iRussia:
	
		# first goal: found seven cities in Siberia by 1700 AD and build the Trans-Siberian Railway by 1920 AD
		if iGameTurn == getTurnForYear(1700):
			if getNumFoundedCitiesInArea(iRussia, utils.getPlotList(tSiberiaTL, tSiberiaBR)) < 7:
				lose(iRussia, 0)
				
		if isPossible(iRussia, 0):
			if isConnectedByRailroad(iRussia, Areas.getCapital(iRussia), lSiberianCoast):
				win(iRussia, 0)
					
		if iGameTurn == getTurnForYear(1920):
			expire(iRussia, 0)
			
		# second goal: be the first civilization to complete the Manhattan Project and the Apollo Program
		
		# third goal: have friendly relations with five communist civilizations by 1950 AD
		if isPossible(iRussia, 2):
			if dc.isCommunist(iPlayer) and countPlayersWithAttitudeAndCriteria(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY, dc.isCommunist) >= 5:
				win(iRussia, 2)
				
		if iGameTurn == getTurnForYear(1950):
			expire(iRussia, 2)
			
	elif iPlayer == iPhilippines:
		# first goal: control 7 embassies in 1400 AD
		if iGameTurn == getTurnForYear(1400):
			if isPossible(iPhilippines, 0):
				if len(data.lPhilippineEmbassies) >= 7:
					win(iPhilippines, 0)
				else:
					lose(iPhilippines, 0)
				
		# second goal: acquire 8 different happiness resources by 1550 AD
		if isPossible(iPhilippines, 1):
			if countHappinessResources(iPhilippines) >= 8:
				win(iPhilippines, 1)
				
		if iGameTurn == getTurnForYear(1500):
			expire(iPhilippines, 1)
			
		# third goal: Have 5000 gold in 1600 AD
		if iGameTurn == getTurnForYear(1600):
			if isPossible(iPhilippines, 2):
				if pPhilippines.getGold() >= utils.getTurns(5000):
					win(iPhilippines, 2)
				else:
					lose(iPhilippines, 2)
				
	elif iPlayer == iChimu:
		# first goal: Build two Kanchas by 1300 CE
		
		if isPossible(iChimu, 0):
			bKancha = getNumBuildings(iChimu, iKancha) >= 2
			
			if bKancha:
				win(iChimu, 0)
		
		if iGameTurn == getTurnForYear(1300):
			expire(iChimu, 0)
		
		# second goal: Conquer or vassalize the Inca by 1475 CE
		if isPossible(iChimu, 1):
			bInca = iGameTurn >= getTurnForYear(tBirth[iInca]) and isControlledOrVassalized(iChimu, Areas.getCoreArea(iInca, True))
			
			if bInca:
				win(iChimu, 1)
				
		
		if iGameTurn == getTurnForYear(1475):
			expire(iChimu, 1)
			
		# third goal: Settle three great artists in your capital by 1500 CE
		if isPossible(iChimu, 2):
			bArtist = countCitySpecialists(iChimu, Areas.getCapital(iChimu), iSpecialistGreatArtist) >= 3
			
			if bArtist:
				win(iChimu, 2)
				
		if iGameTurn == getTurnForYear(1500):
			expire(iChimu, 2)
			
	elif iPlayer == iSwahili:
		# first goal: acquire 4000 gold by trade by 1500 AD
		if isPossible(iSwahili, 0):
			iTradeGold = 0
			
			# gold from city trade routes
			iTradeCommerce = 0
			for city in utils.getCityList(iSwahili):
				iTradeCommerce += city.getTradeYield(2)
			iTradeGold += iTradeCommerce * pSwahili.getCommercePercent(0)
			
			# gold from per turn gold trade
			for iPlayer in range(iNumPlayers):
				iTradeGold += pSwahili.getGoldPerTurnByPlayer(iPlayer) * 100
			
			data.iSwahiliTradeGold += iTradeGold
			
			if data.iSwahiliTradeGold / 100 >= utils.getTurns(4000):
				win(iSwahili, 2)
				
		if iGameTurn == getTurnForYear(1500):
			expire(iSwahili, 0)
			expire(iSwahili, 1)
			
		# second goal: build an Islamic Mosque by 1500 AD
		
		# third goal: found a city in Australia by 1650 AD
		if iGameTurn == getTurnForYear(1650):
			expire(iSwahili, 2)
			
	elif iPlayer == iMamluks:
		if isPossible(iMamluks, 0):
			bNorthAfrica = isCultureControlled(iMamluks, utils.getPlotList(tNorthAfricaTL, tNorthAfricaBR), True)
			bHejaz = isCultureControlled(iMamluks, utils.getPlotList(tHejazTL, tHejazBR, tHejazExceptions), True)
			bLevant = isCultureControlled(iMamluks, utils.getPlotList(tLevantTL, tLevantBR), True)
			bMesopotamia = isControlled(iMamluks, Areas.getCoreArea(iBabylonia, False))
			if bNorthAfrica and bHejaz and bLevant and bMesopotamia:
				win(iMamluks, 0)
			
		if iGameTurn == getTurnForYear(1300):
			expire(iMamluks, 0)
	
		# second goal: Make Cairo the most populous city in the world and have at least 30 population on the Lower Nile in 1380 AD
		if iGameTurn == getTurnForYear(1380):
			if isPossible(iMamluks, 1):
				lLowerNile = [(x, y) for (x, y) in utils.getPlotList(tLowerNileTL, tLowerNileBR) if gc.getMap().plot(x, y).isRiver()]
				if isBestCity(iMamluks, (69, 35), cityPopulation) and countPopulationInArea(iMamluks, lLowerNile) >= 30:
					win(iMamluks, 1)
				else:
					lose(iMamluks, 1)
				
		# third goal: Have the highest total culture and science output in 1500 AD
		if iGameTurn == getTurnForYear(1500):
			if isPossible(iMamluks, 2):
				bMostCultureOutput = isBestPlayer(iMamluks, playerCultureOutput)
				bMostResearchOutput = isBestPlayer(iMamluks, playerResearchOutput)
				if bMostCultureOutput and bMostResearchOutput:
					win(iMamluks, 2)
				else:
					lose(iMamluks, 2)
			
	elif iPlayer == iMali:
		
		# first goal: conduct a trade mission to your holy city by 1350 AD
		if iGameTurn == getTurnForYear(1350):
			expire(iMali, 0)
			
		# second goal: build the University of Sankore and settle a great prophet in its city by 1500 AD
		if isPossible(iMali, 1):
			for city in utils.getCityList(iMali):
				if city.isHasRealBuilding(iUniversityOfSankore) and city.getFreeSpecialistCount(iSpecialistGreatProphet) >= 1:
					win(iMali, 1)
		
		if iGameTurn == getTurnForYear(1500):
			expire(iMali, 1)
			
		# third goal: have 7500 gold in 1500 AD and 15000 gold in 1700 AD
		if iGameTurn == getTurnForYear(1500):
			if pMali.getGold() < utils.getTurns(7500):
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
			
	elif iPlayer == iZimbabwe:
	
		# first goal: build four castles and kraals and Great Zimbabwe in 1400 AD
		if iGameTurn == getTurnForYear(1400):
			if isPossible(iZimbabwe, 1):
				iCastles = getNumBuildings(iZimbabwe, iCastle)
				iKraals = getNumBuildings(iZimbabwe, iKraal)
				bGreatZimbabwe = data.getWonderBuilder(iGreatZimbabwe) == iZimbabwe
				if iCastles >= 4 and iKraals >= 4 and bGreatZimbabwe:
					win(iZimbabwe, 0)
				else:
					lose(iZimbabwe, 0)
	
		# second goal: Have a monopoly on Ivory and Gold in Sub-Saharan Africa in 1500 AD
		if iGameTurn == getTurnForYear(1500):
			if isPossible(iZimbabwe, 1):
				lSubSaharanAfrica = utils.getPlotList(tSubSaharaTL, tSubSaharaBR, tSubSaharaExceptions)
				bGoldMonopoly = isMonopoly(iZimbabwe, iGold, lSubSaharanAfrica)
				bSilverMonopoly = isMonopoly(iZimbabwe, iSilver, lSubSaharanAfrica)
				bGemsMonopoly = isMonopoly(iZimbabwe, iGems, lSubSaharanAfrica)
				bIvoryMonopoly = isMonopoly(iZimbabwe, iIvory, lSubSaharanAfrica)
				if bGoldMonopoly and bSilverMonopoly and bGemsMonopoly and bIvoryMonopoly:
					win(iZimbabwe, 1)
				else:
					lose(iZimbabwe, 1)
		
		# third goal: allow no European colonies in Subequatorial Africa in 1700 AD
		if iGameTurn == getTurnForYear(1700):
			if isPossible(iZimbabwe, 2):
				bSubequatorialAfrica = isAreaFreeOfCivs(utils.getPlotList(tSubeqAfricaTL, tSubeqAfricaBR), lCivGroups[0])
				if bSubequatorialAfrica:
					win(iZimbabwe, 2)
				else:
					lose(iZimbabwe, 2)
			
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
			iCount += getNumCitiesInRegions(iPortugal, lAfrica)
			iCount += getNumCitiesInRegions(iPortugal, lAsia)
			if iCount >= 15:
				win(iPortugal, 2)
			else:
				lose(iPortugal, 2)
				
	elif iPlayer == iInca:
	
		# first goal: build five Tambos and a road along the Andean coast by 1500 AD
		if isPossible(iInca, 0):
			if isRoad(iInca, lAndeanCoast) and getNumBuildings(iInca, iTambo) >= 5:
				win(iInca, 0)
				
		if iGameTurn == getTurnForYear(1500):
			expire(iInca, 0)
			
		# second goal: have 2500 gold in 1550 AD
		if iGameTurn == getTurnForYear(1550):
			if pInca.getGold() >= utils.getTurns(2500):
				win(iInca, 1)
			else:
				lose(iInca, 1)
			
		# third goal: allow no other civilisations in South America in 1700 AD
		if iGameTurn == getTurnForYear(1700):
			if isAreaOnlyCivs(tSAmericaTL, tSAmericaBR, [iInca]):
				win(iInca, 2)
			else:
				lose(iInca, 2)
				
	elif iPlayer == iItaly:
	
		# first goal: build San Marco Basilica, the Sistine Chapel and Santa Maria del Fiore by 1500 AD
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
			
	elif iPlayer == iNigeria:
		# first goal: Have the largest army of Africa in 1600 AD
		if iGameTurn == getTurnForYear(1600):
			if isPossible(iNigeria, 0):
				lAfricaCivs = [iLoopPlayer for iLoopPlayer in range(iNumPlayers) if gc.getPlayer(iLoopPlayer).getCapitalCity().getRegionID() in lAfrica]
				if isBestPlayer(iNigeria, playerArmySize, lAfricaCivs):
					win(iNigeria, 0)
				else:
					lose(iNigeria, 0)
		
		# second goal: Acquire 2000 gold by selling resources by 1750 AD
		if isPossible(iNigeria, 1):
			iTradeGold = 0
			
			for iLoopPlayer in range(iNumPlayers):
				iTradeGold += pNigeria.getGoldPerTurnByPlayer(iLoopPlayer)
			
			data.iNigeriaTradeGold += iTradeGold
			
			if data.iNigeriaTradeGold >= utils.getTurns(2000):
				win(iNigeria, 1)
				
		if iGameTurn == getTurnForYear(1750):
			expire(iNigeria, 1)
		
		# third goal: Control a Hit Movie and have Oil Company by 1950 AD
		if isPossible(iNigeria, 2):
			if pNigeria.getNumAvailableBonuses(iMovies) >= 1 and pNigeria.countCorporations(iOilIndustry) >= 1:
				win(iNigeria, 2)
		
		if iGameTurn == getTurnForYear(1950):
			expire(iNigeria, 2)
			
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
			
		# second goal: build the Red Fort, Shalimar Gardens and the Taj Mahal by 1660 AD
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
					
			# second goal: build six step pyramids and sacrificial altars by 1650 AD
			if isPossible(iAztecs, 1):
				if getNumBuildings(iAztecs, utils.getUniqueBuilding(iAztecs, iPaganTemple)) >= 6 and getNumBuildings(iAztecs, iSacrificialAltar) >= 6:
					win(iAztecs, 1)
			
			if iGameTurn == getTurnForYear(1650):
				expire(iAztecs, 1)
				
			# third goal: enslave 20 old world units
			if isPossible(iAztecs, 2):
				if data.iAztecSlaves >= 20:
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
				
	elif iPlayer == iOttomans:
	
		# first goal: have four non-obsolete wonders in your capital in 1550 AD
		if iGameTurn == getTurnForYear(1550):
			capital = pOttomans.getCapitalCity()
			if countCityWonders(iOttomans, (capital.getX(), capital.getY()), False) >= 4:
				win(iOttomans, 0)
			else:
				lose(iOttomans, 0)
				
		# second goal: control the Eastern Mediterranean, the Black Sea, Cairo, Mecca, Baghdad and Vienna by 1700 AD
		if isPossible(iOttomans, 1):
			bEasternMediterranean = isCultureControlled(iOttomans, lEasternMediterranean)
			bBlackSea = isCultureControlled(iOttomans, lBlackSea)
			bCairo = controlsCity(iOttomans, tCairo)
			bMecca = controlsCity(iOttomans, tMecca)
			bBaghdad = controlsCity(iOttomans, tBaghdad)
			bVienna = controlsCity(iOttomans, tVienna)
			
			if bEasternMediterranean and bBlackSea and bCairo and bMecca and bBaghdad and bVienna:
				win(iOttomans, 1)
				
		if iGameTurn == getTurnForYear(1700):
			expire(iOttomans, 1)
			
		# third goal: have more culture than all European civilizations combined in 1800 AD
		if iGameTurn == getTurnForYear(1800):
			if pOttomans.countTotalCulture() > getTotalCulture(lCivGroups[0]):
				win(iOttomans, 2)
			else:
				lose(iOttomans, 2)
				
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
		
	elif iPlayer == iSweden:
		# first goal: Control the Baltic Coast, the Kattegat and the Skagerak by 1700 AD
		if iGameTurn == getTurnForYear(1700):
			bSkagerrak = isCultureControlled(iSweden, lSkagerrak)
			bBalticSea = isCultureControlled(iSweden, lBalticSea)
			if bSkagerrak and bBalticSea:
				win(iSweden, 0)
		
		if iGameTurn == getTurnForYear(1700):
			expire(iSweden, 0)
			
		# second goal: Control 7 fur resources by 1800 AD
		if isPossible(iSweden, 1):
			if pSweden.getNumAvailableBonuses(iFur) >= 7:
				win(iSweden, 1)
				
		if iGameTurn == getTurnForYear(1800):
			expire(iSweden, 1)
		
		# third goal: Have the highest approval rating in the world for 50 turns by 1970 AD
		if isPossible(iSweden, 2):
			if isHappiest(iPlayer):
				data.iSwedenHappinessTurns += 1
			if data.iSwedenHappinessTurns >= utils.getTurns(50):
				win(iSweden, 2)
			
		if iGameTurn == getTurnForYear(1970):
			expire(iSweden, 2)
		
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
			
	elif iPlayer == iManchuria:
		# first goal: Have 20% of the world population in 1850 AD
		if iGameTurn == getTurnForYear(1850):
			if isPossible(iManchuria, 0):
				if getPopulationPercent(iManchuria) >= 20.0:
					win(iManchuria, 0)
				else:
					lose(iManchuria, 0)
				
		# second goal: Have the highest food, production and commerce output in 1850 AD
		if iGameTurn == getTurnForYear(1850):
			if isPossible(iManchuria, 0):
				if isBestPlayer(iManchuria, playerFoodOutput) and isBestPlayer(iManchuria, playerProductionOutput) and isBestPlayer(iManchuria, playerCommerceOutput):
					win(iManchuria, 1)
				else:
					lose(iManchuria, 1)
		
		# third goal: Be the first to discover all Industrial and eight Global technologies
		
	elif iPlayer == iGermany:
	
		# first goal: settle seven great people in Berlin in 1900 AD
		if iGameTurn == getTurnForYear(1900):
			iCount = 0
			for iSpecialist in lGreatPeople:
				iCount += countCitySpecialists(iPrussia, Areas.getCapital(iGermany), iSpecialist)
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
				
		# second goal: build the Statue of Liberty, the Brooklyn Bridge, the Empire State Building, the Golden Gate Bridge, the Pentagon and the United Nations by 1950 AD
		if iGameTurn == getTurnForYear(1950):
			expire(iAmerica, 1)
			
		# third goal: control 75% of the world's commerce output and military power between you, your vassals and allies by 1990 AD
		if isPossible(iAmerica, 2):
			if calculateAlliedCommercePercent(iAmerica) >= 75.0 and calculateAlliedPowerPercent(iAmerica) >= 75.0:
				win(iAmerica, 2)
				
		if iGameTurn == getTurnForYear(1990):
			expire(iAmerica, 2)
			
	elif iPlayer == iArgentina:
	
		# first goal: experience two golden ages by 1930 AD
		if isPossible(iArgentina, 0):
			if data.iArgentineGoldenAgeTurns >= utils.getTurns(16):
				win(iArgentina, 0)
				
		if iGameTurn == getTurnForYear(1930):
			expire(iArgentina, 0)
			
		# second goal: have lengendary culture in Buenos Aires by 1960 AD
		if isPossible(iArgentina, 1):
			if getCityCulture(iArgentina, Areas.getCapital(iArgentina)) >= utils.getTurns(50000):
				win(iArgentina, 1)
				
		if iGameTurn == getTurnForYear(1960):
			expire(iArgentina, 1)
			
		# third goal: experience six golden ages by 2000 AD
		if isPossible(iArgentina, 2):
			if data.iArgentineGoldenAgeTurns >= utils.getTurns(48):
				win(iArgentina, 2)
				
		if iGameTurn == getTurnForYear(2000):
			expire(iArgentina, 2)
			
		if pArgentina.isGoldenAge() and not pArgentina.isAnarchy():
			data.iArgentineGoldenAgeTurns += 1
			
	elif iPlayer == iBrazil:
	
		# first goal: control 8 slave plantations and 4 pastures in 1880 AD
		if iGameTurn == getTurnForYear(1880):
			if countImprovements(iBrazil, iSlavePlantation) >= 8 and countImprovements(iBrazil, iPasture) >= 4:
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
				
	elif iPlayer == iAustralia:
		
		# first Australian goal: control Australia, New Zealand, New Guinea and 3 pacific islands in 1950 AD
		if iGameTurn == getTurnForYear(1950):
			if isPossible(iAustralia, 0):
				bAustralia = getNumCitiesInArea(iAustralia, utils.getPlotList(tAustraliaTL, tAustraliaBR)) >= 7
				bNewZealand = getNumCitiesInArea(iAustralia, utils.getPlotList(tNewZealandTL, tNewZealandBR)) >= 2
				bGuinea = getNumCitiesInArea(iAustralia, utils.getPlotList(tNewGuineaTL, tNewGuineaBR)) >= 1
				bPacific = getNumCitiesInArea(iAustralia, utils.getPlotList(tPacific1TL, tPacific1BR)) + getNumCitiesInArea(iAustralia, utils.getPlotList(tPacific2TL, tPacific2BR)) \
					+ getNumCitiesInArea(iAustralia, utils.getPlotList(tPacific3TL, tPacific3BR)) + getNumCitiesInArea(iAustralia, utils.getPlotList(tHawaiiTL, tHawaiiBR)) >= 3
				if bAustralia and bNewZealand and bGuinea and bPacific:
					win(iAustralia, 0)
				else:
					lose(iAustralia, 0)
		
		# second goal: Gift 25 Digger, Marines or Mechanized Infantry to other civilizations by 1950 AD
		if iGameTurn == getTurnForYear(1950):
			expire(iAustralia, 1)
			
		# third goal: Have the highest approval rating in the world for 25 turns
		if isPossible(iAustralia, 2):
			if isHappiest(iPlayer):
				data.iAustraliaHappinessTurns += 1
				if data.iAustraliaHappinessTurns >= utils.getTurns(25):
					win(iAustralia, 2)
	elif iPlayer == iBoers:
		# first goal: Allow no European Colonies in South Africa by 1920 AD
		if iGameTurn == getTurnForYear(1920):
			if isAreaFreeOfCivs(utils.getPlotList(tBoerAfricaTL, tBoerAfricaBR), lCivGroups[0]):
				win(iBoers, 0)
			else:
				lose(iBoers, 0)
		
		# second goal: Secure or get by trade 5 gems resources by 1947 AD
		if isPossible(iBoers, 1):
			if countResources(iBoers, iGems) >= 5:
				win(iBoers, 1)
		
		if iGameTurn == getTurnForYear(1950):
			expire(iBoers, 1)
		
		# third goal: Build an ICBM by 1979 AD
		if iGameTurn == getTurnForYear(1980):
			expire(iBoers, 2)
				
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
			
		# second goal: control or vassalize all cities and 90% of the territory in Canada without ever conquering a city by 1950 AD
		if isPossible(iCanada, 1):
			iEast, iTotalEast = countControlledTiles(iCanada, tCanadaEastTL, tCanadaEastBR, True, tCanadaEastExceptions)
			iWest, iTotalWest = countControlledTiles(iCanada, tCanadaWestTL, tCanadaWestBR, True, tCanadaWestExceptions)
			
			fCanada = (iEast + iWest) * 100.0 / (iTotalEast + iTotalWest)
			
			bAllCitiesEast = controlsOrVassalizedAllCities(iCanada, tCanadaEastTL, tCanadaEastBR, tCanadaEastExceptions)
			bAllCitiesWest = controlsOrVassalizedAllCities(iCanada, tCanadaWestTL, tCanadaWestBR, tCanadaWestExceptions)
			
			if fCanada >= 90.0 and bAllCitiesEast and bAllCitiesWest:
				win(iCanada, 1)
				
		if iGameTurn == getTurnForYear(1950):
			expire(iCanada, 1)
			
		# third goal: end twelve wars through diplomacy by 2000 AD
		if iGameTurn == getTurnForYear(2000):
			expire(iCanada, 2)
			
	elif iPlayer == iIsrael :

		# first goal: build an ICBM by 1980
		if isPossible(iIsrael, 0):
			iIsraeliNuclearArsenal = pIsrael.getUnitClassCount(gc.getUnitInfo(iICBM).getUnitClassType())
			if iIsraeliNuclearArsenal >= 1:
				win(iIsrael, 0)

		if iGameTurn == getTurnForYear(1980):
			expire(iIsrael, 0)

		# second goal: have the city with the highest research output for 10 turns (no time limit)
		if isPossible(iIsrael, 1):
			if data.iIsraeliResearchTurns >= 10:
				win(iIsrael, 1)
			
			x, y = 0, 0
			capital = pPlayer.getCapitalCity()
			if capital:
				x, y = capital.getX(), capital.getY()
			pBestCity = getBestCity(iPlayer, (x, y), cityResearchOutput)
			if pBestCity.getOwner() == iPlayer: 
				data.iIsraeliResearchTurns += 1

		# third goal: create two great spies (no time limit)
		# see onGreatPersonBorn()
		
			
	# check religious victory (human only)
	if utils.getHumanID() == iPlayer:
		iVictoryType = utils.getReligiousVictoryType(iPlayer)
		
		if iVictoryType == iCatholicism:
			if gc.getGame().getSecretaryGeneral(1) == iPlayer:
				data.iPopeTurns += 1
				
		elif iVictoryType == iHinduism:
			if pPlayer.isGoldenAge():
				data.iHinduGoldenAgeTurns += 1
				
		elif iVictoryType == iBuddhism:
			if isAtPeace(iPlayer):
				data.iBuddhistPeaceTurns += 1
				
			if isHappiest(iPlayer):
				data.iBuddhistHappinessTurns += 1
				
		elif iVictoryType == iTaoism:
			if isHealthiest(iPlayer):
				data.iTaoistHealthTurns += 1
				
		elif iVictoryType == iVictoryPaganism:
			if 2 * countReligionCities(iPlayer) > pPlayer.getNumCities():
				data.bPolytheismNeverReligion = False
				
			if gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getPaganReligionName(0) == "Vedism":
				for city in utils.getCityList(iPlayer):
					if city.isWeLoveTheKingDay():
						data.iVedicHappiness += 1
				
		if checkReligiousGoals(iPlayer):
			gc.getGame().setWinner(iPlayer, 8)
			
def checkHistoricalVictory(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	
	if iPlayer == iOman:
		if isPossible(iOman, 0) and countAchievedGoals(iPlayer) >= 2:
			win(iOman, 0)
	
	if not data.players[iPlayer].bHistoricalGoldenAge:
		if countAchievedGoals(iPlayer) >= 2:	
			data.players[iPlayer].bHistoricalGoldenAge = True
			
			iGoldenAgeTurns = gc.getPlayer(iPlayer).getGoldenAgeLength()
			if not gc.getPlayer(iPlayer).isAnarchy(): iGoldenAgeTurns += 1
			
			gc.getPlayer(iPlayer).changeGoldenAgeTurns(iGoldenAgeTurns)
			
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

def onUnitBuilt(city, unit):
	if not gc.getGame().isVictoryValid(7): return
	
	iPlayer = city.getOwner()
	
	if utils.getHumanID() != iPlayer and data.bIgnoreAI: return
	
	if iPlayer >= iNumPlayers: return
	
	# third goal: Build an ICBM by 1979 AD
	if iPlayer == iBoers:
		if isPossible(iBoers, 2):
			if unit.getUnitType() == iICBM:
				win(iBoers, 2)
		
def onCityBuilt(iPlayer, city):

	if not gc.getGame().isVictoryValid(7): return
	
	if utils.getHumanID() != iPlayer and data.bIgnoreAI: return
	
	if iPlayer >= iNumPlayers: return
	
	iGameTurn = gc.getGame().getGameTurn()
	
	# record first colony in the Americas for various UHVs
	if not data.isFirstWorldColonized():
		if city.getRegionID() in lNorthAmerica + lSouthAmerica:
			if iPlayer not in lCivGroups[5]:
				data.iFirstNewWorldColony = iPlayer
			
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
			bNAmerica = getNumCitiesInRegions(iEngland, lNorthAmerica) >= 5
			bSCAmerica = getNumCitiesInRegions(iEngland, lSouthAmerica) >= 3
			bAfrica = getNumCitiesInRegions(iEngland, lAfrica) >= 4
			bAsia = getNumCitiesInRegions(iEngland, lAsia) >= 5
			bOceania = getNumCitiesInRegions(iEngland, lOceania) >= 3
			if bNAmerica and bSCAmerica and bAfrica and bAsia and bOceania:
				win(iEngland, 0)

	# third Swahili goal: found a city in Australia by 1650 AD
	elif iPlayer == iSwahili:
		if isPossible(iSwahili, 2):
			if city.getRegionID() == rAustralia:
				win(iSwahili, 2)
				
def onCityAcquired(iPlayer, iOwner, city, bConquest, bCapital):

	if not gc.getGame().isVictoryValid(7): return
	
	if (city.getX(), city.getY()) in data.lCeltiaConqueredCapitals:
		data.lCeltiaConqueredCapitals.remove((city.getX(), city.getY()))
	
	if isPossible(iCeltia, 0):
		if iPlayer == iCeltia:
			if bConquest and bCapital:
				data.lCeltiaConqueredCapitals.append((city.getX(), city.getY()))
	
	# third Yemeni goal: Do not allow any Persian or Turkic nation to conquer a city in the Arabian Peninsula prior to the Collapse of the Ottomans
	if isPossible(iYemen, 2):
		if city.getRegionID() == rArabia and iPlayer in [iMongolia, iTurks, iPersia, iOttomans, iKhazars]:
			lose(iYemen, 2)
		
		if iOwner == iOttomans and pOttomans.getNumCities() < 1:
			win(iYemen, 2)
	
	# first Omani goal: Never lose a city
	if isPossible(iOman, 0) and iOwner == iOman:
		expire(iOman, 0)
	
	# second Omani goal: Conquer 4 cities from civs that have declared war on you
	if isPossible(iOman, 1) and iPlayer == iOman and iOwner in data.lOmaniEnemies:
		data.iOmaniCities += 1
		if data.iOmaniCities >= 4:
			win(iOman, 1)
		
	# first Japanese goal: have an average city culture of 6000 by 1600 AD without ever losing a city
	if iOwner == iJapan:
		expire(iJapan, 0)
	
	# third Vietnamese goal: never lose a single city until 1950 AD
	if iOwner == iVietnam:
		expire(iVietnam, 2)
	
	if utils.getHumanID() != iPlayer and data.bIgnoreAI: return
				
	# first Tibetan goal: acquire five cities by 1000 AD
	if iPlayer == iTibet:
		if isPossible(iTibet, 0):
			if pTibet.getNumCities() >= 5:
				win(iTibet, 0)
					
	# first English goal: colonize every continent by 1730 AD
	elif iPlayer == iEngland:
		if isPossible(iEngland, 0):
			bNAmerica = getNumCitiesInRegions(iEngland, lNorthAmerica) >= 5
			bSCAmerica = getNumCitiesInRegions(iEngland, lSouthAmerica) >= 3
			bAfrica = getNumCitiesInRegions(iEngland, lAfrica) >= 4
			bAsia = getNumCitiesInRegions(iEngland, lAsia) >= 5
			bOceania = getNumCitiesInRegions(iEngland, lOceania) >= 3
			if bNAmerica and bSCAmerica and bAfrica and bAsia and bOceania:
				win(iEngland, 0)
				
	# second Dutch goal: conquer four European colonies by 1745 AD
	elif iPlayer == iNetherlands:
		if isPossible(iNetherlands, 1):
			if iOwner in [iSpain, iFrance, iEngland, iPortugal, iVikings, iItaly, iRussia, iGermany, iHolyRome, iPoland]:
				bColony = city.getRegionID() not in [rBritain, rIberia, rItaly, rBalkans, rEurope, rScandinavia, rRussia]
			
				if bColony and bConquest:
					data.iDutchColonies += 1
					if data.iDutchColonies >= 4:
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
		data.lFirstDiscovered[iTech] = iPlayer
		
		for iLoopPlayer in dTechGoals.keys():
			iGoal = dTechGoals[iLoopPlayer][0]
			lTechs = dTechGoals[iLoopPlayer][1]
			
			if not isPossible(iLoopPlayer, iGoal): continue
			if iLoopPlayer == iMaya and pMaya.isReborn(): continue
			
			if iTech in lTechs:
				if iPlayer != iLoopPlayer: lose(iLoopPlayer, iGoal)
				elif checkTechGoal(iLoopPlayer, lTechs): win(iLoopPlayer, iGoal)
				
		# third Japanese goal: be the first to discover ten Global and ten Digital technologies
		if isPossible(iJapan, 2):
			if iEra in [iGlobal, iDigital]:
				if countFirstDiscovered(iPlayer, iGlobal) >= 8 and countFirstDiscovered(iPlayer, iDigital) >= 8:
					if iPlayer == iJapan: win(iJapan, 2)
					else: lose(iJapan, 2)
				if not isFirstDiscoveredPossible(iJapan, iGlobal, 8) or not isFirstDiscoveredPossible(iJapan, iDigital, 8):
					lose(iJapan, 2)
				
		# third English goal: be the first to discover ten Renaissance and ten Industrial technologies
		if isPossible(iEngland, 2):
			if iEra in [iRenaissance, iIndustrial]:
				if countFirstDiscovered(iPlayer, iRenaissance) >= 8 and countFirstDiscovered(iPlayer, iIndustrial) >= 8:
					if iPlayer == iEngland: win(iEngland, 2)
					else: lose(iEngland, 2)
				if not isFirstDiscoveredPossible(iEngland, iRenaissance, 8) or not isFirstDiscoveredPossible(iEngland, iIndustrial, 8):
					lose(iEngland, 2)
				
		# third German goal: be the first to discover ten Industrial and ten Global technologies
		if isPossible(iGermany, 2):
			if iEra in [iIndustrial, iGlobal]:
				if countFirstDiscovered(iPlayer, iIndustrial) >= 8 and countFirstDiscovered(iPlayer, iGlobal) >= 8:
					if iPlayer == iGermany: win(iGermany, 2)
					else: lose(iGermany, 2)
				if not isFirstDiscoveredPossible(iGermany, iIndustrial, 8) or not isFirstDiscoveredPossible(iGermany, iGlobal, 8):
					lose(iGermany, 2)
				
		# third Manchurian goal: be the first to discover all Industrial Technologies and ten Global technologies
		if isPossible(iManchuria, 2):
			if iEra == iGlobal:
				if countFirstDiscovered(iPlayer, iGlobal) >= 8:
					if iPlayer == iManchuria:
						if data.lFirstCompleted[iIndustrial] == iManchuria:
							win(iManchuria, 2)
					else: lose(iManchuria, 2)
					
	if not isEraCompleted(iEra):
		if checkEraCompleted(iPlayer, iEra):
			data.lFirstCompleted[iEra] = iPlayer
			
			if isPossible(iManchuria, 2):
				if iEra == iIndustrial:
					if iPlayer == iManchuria:
						if countFirstDiscovered(iManchuria, iGlobal) >= 8:
							win(iManchuria, 2)
					else:
						lose(iManchuria, 2)
			
	# handle all "be the first to enter" goals
	if not isEntered(iEra):
		data.lFirstEntered[iEra] = iPlayer
		
		for iLoopPlayer in dEraGoals.keys():
			iGoal = dEraGoals[iLoopPlayer][0]
			lEras = dEraGoals[iLoopPlayer][1]
			
			if not isPossible(iLoopPlayer, iGoal): continue
			
			if iEra in lEras:
				if iPlayer != iLoopPlayer: lose(iLoopPlayer, iGoal)
				elif checkEraGoal(iLoopPlayer, lEras): win(iLoopPlayer, iGoal)
				
	# second Olmec goal: discover two of Arithmetics, Writing and Calendar by 400 BC
	if iPlayer == iOlmecs:
		lRequiredTechs = [iArithmetics, iWriting, iCalendar]
		if isPossible(iOlmecs, 1):
			iCount = 0
			if iTech in lRequiredTechs:
				for iRequiredTech in lRequiredTechs:
					if teamOlmecs.isHasTech(iRequiredTech):
						iCount += 1
				if iCount >= 2:
					win(iOlmecs, 1)

	# first Maya goal: discover Calendar by 200 AD
	if iPlayer == iMaya:
		if not pMaya.isReborn() and isPossible(iMaya, 0):
			if iTech == iCalendar:
				if teamMaya.isHasTech(iCalendar):
					win(iMaya, 0)
				
	# third Congolese goal: enter the Industrial era before anyone enters the Modern era
	if isPossible(iCongo, 2):
		if iEra == iIndustrial and iPlayer == iCongo:
			win(iCongo, 2)
		if iEra == iGlobal and iPlayer != iCongo:
			lose(iCongo, 2)
				
def checkTechGoal(iPlayer, lTechs):
	for iTech in lTechs:
		if data.lFirstDiscovered[iTech] != iPlayer:
			return False
	return True
	
def checkEraGoal(iPlayer, lEras):
	for iEra in lEras:
		if data.lFirstEntered[iEra] != iPlayer:
			return False
	return True
	
def onBuildingBuilt(iPlayer, iBuilding):

	if not gc.getGame().isVictoryValid(7): return False
	
	# handle all "build wonders" goals
	if isWonder(iBuilding) and not isWonderBuilt(iBuilding):
		# Expire Hungarian UHV2 when UN is built (No more Congresses)
		if iBuilding == iUnitedNations:
			expire(iHungary, 2)
		
		data.setWonderBuilder(iBuilding, iPlayer)
		
		for iLoopPlayer in dWonderGoals.keys():
			iGoal, lWonders, bCanWin = dWonderGoals[iLoopPlayer]
			
			if not isPossible(iLoopPlayer, iGoal): continue
			
			if iBuilding in lWonders:
				if iPlayer != iLoopPlayer: lose(iLoopPlayer, iGoal)
				elif bCanWin and checkWonderGoal(iLoopPlayer, lWonders): win(iLoopPlayer, iGoal)
				
	if utils.getHumanID() != iPlayer and data.bIgnoreAI: return
	
	if not gc.getPlayer(iPlayer).isAlive(): return
	
	# first Chinese goal: build two Confucian and Taoist Cathedrals by 1000 AD
	if iPlayer == iChina:
		if isPossible(iChina, 0):
			if iBuilding in [iConfucianCathedral, iTaoistCathedral]:
				iConfucian = getNumBuildings(iChina, iConfucianCathedral)
				iTaoist = getNumBuildings(iChina, iTaoistCathedral)
				if iConfucian >= 2 and iTaoist >= 2:
					win(iChina, 0)
					
	# second Harappan goal: build three Baths, two Granaries and two Smokehouses by 1500 BC
	elif iPlayer == iHarappa:
		if isPossible(iHarappa, 1):
			if iBuilding in [iReservoir, iGranary, iSmokehouse]:
				iNumBaths = getNumBuildings(iHarappa, iReservoir)
				iNumGranaries = getNumBuildings(iHarappa, iGranary)
				iNumSmokehouses = getNumBuildings(iHarappa, iSmokehouse)
				if iNumBaths >= 3 and iNumGranaries >= 2 and iNumSmokehouses >= 2:
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
	
	# first Roman goal: build 6 Barracks, 5 Aqueducts, 4 Arenas and 3 Forums by 100 AD
	elif iPlayer == iRome:
		if isPossible(iRome, 0):
			if iBuilding in [iBarracks, iAqueduct, iArena, iForum]:
				iNumBarracks = getNumBuildings(iRome, iBarracks)
				iNumAqueducts = getNumBuildings(iRome, iAqueduct)
				iNumArenas = getNumBuildings(iRome, iArena)
				iNumForums = getNumBuildings(iRome, iForum)
				if iNumBarracks >= 6 and iNumAqueducts >= 5 and iNumArenas >= 4 and iNumForums >= 3:
					win(iRome, 0)
					
	# first Korean goal: build a Confucian and a Buddhist Cathedral
	elif iPlayer == iKorea:
		if isPossible(iKorea, 0):
			if iBuilding in [iConfucianCathedral, iBuddhistCathedral]:
				bBuddhist = getNumBuildings(iKorea, iBuddhistCathedral) > 0
				bConfucian = getNumBuildings(iKorea, iConfucianCathedral) > 0
				if bBuddhist and bConfucian:
					win(iKorea, 0)
				
	# first Burmese goal: Build the Shwedagon Paya, 2 Buddhist Temples, and 2 Buddhist Monasteries by 1000 AD
	elif iPlayer == iBurma:
		if isPossible(iBurma, 0):
			bShwedagon = data.getWonderBuilder(iShwedagonPaya) == iBurma
			bTemples = getNumBuildings(iBurma, iBuddhistTemple) >= 2
			bMonasteries = getNumBuildings(iBurma, iBuddhistMonastery) >= 2
			if bShwedagon and bTemples and bMonasteries:
				win(iBurma, 0)
					
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
				if iBuilding in [iPaganTemple, iSacrificialAltar]:
					iTemples = getNumBuildings(iAztecs, iPaganTemple)
					iAltars = getNumBuildings(iAztecs, iSacrificialAltar)
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
			if iBuilding == iTambo:
				if isRoad(iInca, lAndeanCoast) and getNumBuildings(iInca, iTambo) >= 5:
					win(iInca, 0)
					
	# second Swahili goal: build an Islamic Mosque by 1500 AD
	elif iPlayer == iSwahili:
		if isPossible(iSwahili, 1):
			if iBuilding == iIslamicCathedral:
				win(iSwahili, 1)
				
def checkWonderGoal(iPlayer, lWonders):
	for iWonder in lWonders:
		if data.getWonderBuilder(iWonder) != iPlayer:
			return False
	return True
				
def onReligionFounded(iPlayer, iReligion):

	if not gc.getGame().isVictoryValid(7): return
	
	# handle all "be the first to found" goals
	if not isFounded(iReligion):
		data.lReligionFounder[iReligion] = iPlayer
		
		for iLoopPlayer in dReligionGoals.keys():
			iGoal = dReligionGoals[iLoopPlayer][0]
			lReligions = dReligionGoals[iLoopPlayer][1]
			
			if not isPossible(iLoopPlayer, iGoal): continue
			
			if iReligion in lReligions:
				if iPlayer != iLoopPlayer: lose(iLoopPlayer, iGoal)
				elif checkReligionGoal(iLoopPlayer, lReligions): win(iLoopPlayer, iGoal)
				
def checkReligionGoal(iPlayer, lReligions):
	for iReligion in lReligions:
		if data.lReligionFounder[iReligion] != iPlayer:
			return False
	return True
				
def onCityRazed(iPlayer, city):
	if not gc.getGame().isVictoryValid(7): return
	
	if utils.getHumanID() != iPlayer and data.bIgnoreAI: return
	
	# first Celtic goal: Raze 2 Capitals by 200 BC
	if iPlayer == iCeltia:
		if isPossible(iCeltia, 0):
			if (city.getX(), city.getY()) in data.lCeltiaConqueredCapitals:
				data.iCeltiaRazedCapitals += 1
				data.lCeltiaConqueredCapitals.remove((city.getX(), city.getY()))
				if data.iCeltiaRazedCapitals >= 2:
					win(iCeltia, 0)
	
	# second Mongol goal: raze seven cities
	if iPlayer == iMongolia:
		if isPossible(iMongolia, 1):
			data.iMongolRazes += 1
			if data.iMongolRazes >= 7:
				win(iMongolia, 1)
				
def onProjectBuilt(iPlayer, iProject):

	if not gc.getGame().isVictoryValid(7): return
	
	# second Russian goal: be the first civilization to complete the Manhattan Project and the Apollo Program
	if isPossible(iRussia, 1):
		if iProject in [iLunarLanding, iManhattanProject]:
			if iPlayer == iRussia:
				bApolloProgram = iProject == iLunarLanding or teamRussia.getProjectCount(iLunarLanding) > 0
				bManhattanProject = iProject == iManhattanProject or teamRussia.getProjectCount(iManhattanProject) > 0
				if bApolloProgram and bManhattanProject:
					win(iRussia, 1)
			else:
				lose(iRussia, 1)
				
def onCombatResult(pWinningUnit, pLosingUnit):

	iWinningPlayer = pWinningUnit.getOwner()
	iLosingPlayer = pLosingUnit.getOwner()
	
	if utils.getHumanID() != iWinningPlayer and data.bIgnoreAI: return
	
	pLosingUnitInfo = gc.getUnitInfo(pLosingUnit.getUnitType())
	iDomainSea = DomainTypes.DOMAIN_SEA
	
	# second English goal: control a total of 25 frigates and ships of the line and sink 50 ships in 1800 AD
	if iWinningPlayer == iEngland:
		if isPossible(iEngland, 1):
			if pLosingUnitInfo.getDomainType() == iDomainSea:
				data.iEnglishSinks += 1
				
	# third Korean goal: sink 20 enemy ships
	elif iWinningPlayer == iKorea:
		if isPossible(iKorea, 2):
			if pLosingUnitInfo.getDomainType() == iDomainSea:
				data.iKoreanSinks += 1
				if data.iKoreanSinks >= 20:
					win(iKorea, 2)
					
def onGreatPersonBorn(iPlayer, unit):
	iUnitType = utils.getBaseUnit(unit.getUnitType())
	pUnitInfo = gc.getUnitInfo(iUnitType)
	
	if not isGreatPersonTypeBorn(iUnitType):
		data.lFirstGreatPeople[lGreatPeopleUnits.index(iUnitType)] = iPlayer
	
	# second Mexican goal: get three great generals by 1940 AD
	if iPlayer == iAztecs:
		if pAztecs.isReborn() and isPossible(iAztecs, 1):
			if pUnitInfo.getGreatPeoples(iSpecialistGreatGeneral):
				data.iMexicanGreatGenerals += 1
				
				if data.iMexicanGreatGenerals >= 3:
					win(iAztecs, 1)
					
	# second Vietnamese goal: get three great generals by 1500 AD
	if iPlayer == iVietnam:
		if isPossible(iVietnam, 1):
			if pUnitInfo.getGreatPeoples(iSpecialistGreatGeneral):
				data.iVietnamGreatGenerals += 1
				
				if data.iVietnamGreatGenerals >= 3:
					win(iVietnam, 1)
					
	# third Israeli goal: get two great spies (no time limit)
	if iPlayer == iIsrael:
		if isPossible(iIsrael, 2):
			if pUnitInfo.getGreatPeoples(iSpecialistGreatSpy):
				if pIsrael.getGreatSpiesCreated() >= 2:
					win(iIsrael, 2)
					
def onUnitPillage(iPlayer, iGold, iUnit):
	if iGold >= 1000: return

	# third Viking goal: acquire 3000 gold by pillaging, conquering cities and sinking ships by 1500 AD
	if iPlayer == iVikings:
		if isPossible(iVikings, 2):
			data.iVikingGold += iGold
			
	# first Turkic goal: pillage 20 improvements by 900 AD
	elif iPlayer == iTurks:
		if isPossible(iTurks, 0):
			data.iTurkicPillages += 1
			
	elif iPlayer == iMoors:
		if isPossible(iMoors, 2) and iUnit == iCorsair:
			data.iMoorishGold += iGold
		
def onCityCaptureGold(iPlayer, iGold):

	# third Viking goal: acquire 3000 gold by pillaging, conquering cities and sinking ships by 1500 AD
	if iPlayer == iVikings:
		if isPossible(iVikings, 2):
			data.iVikingGold += iGold
		
def onPlayerGoldTrade(iPlayer, iBuyer, iGold):

	# third Tamil goal: acquire 4000 gold by trade by 1200 AD
	if iPlayer == iTamils:
		if isPossible(iTamils, 2):
			data.iTamilTradeGold += iGold * 100
			
	# first Swahili goal: acquire 4000 gold by trade by 1500 AD
	elif iPlayer == iSwahili:
		if isPossible(iSwahili, 0):
			data.iSwahiliTradeGold += iGold * 100
			
	# third Omani goal: Acquire 2000 gold from trade deals
	elif iPlayer == iOman:
		if isPossible(iOman, 2):
			if iGold > 0:
				data.iOmaniTradeGold += iGold
				
	# second Muisca goal: Spend 1000 Gold in diplomacy by 1540 AD
	elif iBuyer == iMuisca:
		if isPossible(iMuisca, 1):
			if iGold > 0:
				data.iMuiscaTradeGold += iGold
		
def onPlayerSlaveTrade(iPlayer, iSlaves, iGold):

	# second Congolese goal: gain 1000 gold through slave trade by 1800 AD
	if iPlayer == iCongo:
		if isPossible(iCongo, 1):
			data.iCongoSlaveCounter += iGold
			if data.iCongoSlaveCounter >= utils.getTurns(1000):
				win(iCongo, 1)
				
	if iPlayer == iChad:
		if isPossible(iChad, 1):
			if iGold > 0:
				data.iChadSlaves += iSlaves
				
			if data.iChadSlaves >= 5 and data.iChadStrategicBonuses >= 10:
				win(iChad, 1)
		
def onPlayerBonusTrade(iPlayer, iStrategicBonuses, iGold):

	if iPlayer == iChad:
		if isPossible(iChad, 1):
			if iGold > 0:
				data.iChadStrategicBonuses += iStrategicBonuses
				
			if data.iChadSlaves >= 5 and data.iChadStrategicBonuses >= 10:
				win(iChad, 1)
				
def onTradeMission(iPlayer, iX, iY, iGold):

	# third Tamil goal: acquire 4000 gold by trade by 1200 AD
	if iPlayer == iTamils:
		data.iTamilTradeGold += iGold * 100
		
	# first Swahili goal: acquire 4000 gold by trade by 1500 AD
	elif iPlayer == iSwahili:
		data.iSwahiliTradeGold += iGold * 100
		
	# first Mande goal: conduct a trade mission in your state religion's holy city by 1350 AD
	elif iPlayer == iMali:
		if isPossible(iMali, 0):
			iStateReligion = pMali.getStateReligion()
			if iStateReligion != -1:
				pHolyCity = gc.getGame().getHolyCity(iStateReligion)
				
				if pHolyCity.getX() == iX and pHolyCity.getY() == iY:
					win(iMali, 0)
					
	# first Kievan Rus goal: Conduct two trade or diplomatic missions with the most prominent (top scoring) European civilization by 1327 AD
	elif iPlayer == iKievanRus:
		if isPossible(iKievanRus, 2):
			if gc.getMap().plot(iX, iY).getOwner() in lCivGroups[0]:
				lTopCivs = getTopCivsInGroup(0, [iKievanRus])
				if gc.getMap().plot(iX, iY).getOwner() in lTopCivs:
					data.iKievanRusMissions += 1
					
	elif iPlayer == iChad:
		if isPossible(iChad, 0):
			iStateReligion = pChad.getStateReligion()
			if iStateReligion != -1:
				pHolyCity = gc.getGame().getHolyCity(iStateReligion)
				
				if pHolyCity.getX() == iX and pHolyCity.getY() == iY:
					data.iChadTradeMissions += 1
					
			if data.iChadTradeMissions >= 3 and data.iChadDiplomacyMissions >= 1:
				win(iChad, 0)
					
def onDiplomaticMission(iPlayer, iX, iY, bMadePeace):
	# first Kievan Rus goal: Conduct two trade or diplomatic missions with the most prominent (top scoring) European civilization by 1327 AD
	if iPlayer == iKievanRus:
		if isPossible(iKievanRus, 2):
			if gc.getMap().plot(iX, iY).getOwner() in lCivGroups[0]:
				lTopCivs = getTopCivsInGroup(0, [iKievanRus])
				if gc.getMap().plot(iX, iY).getOwner() in lTopCivs:
					data.iKievanRusMissions += 1
					
	# first Khazar goal: Conduct a Diplomatic mission in a European City controlled by a Muslim Civilization by 1031 AD
	if iPlayer == iKhazars:
		if isPossible(iKhazars, 0):
			plot = gc.getMap().plot(iX, iY)
			if plot.getRegionID() in lEurope:
				if gc.getPlayer(plot.getOwner()).getStateReligion() == iIslam:
					win(iKhazars, 0)
					
	if iPlayer == iChad:
		if isPossible(iChad, 0):
			if (iX, iY) in Areas.getCoreArea(iMamluks, False):
				data.iChadDiplomacyMissions += 1
					
			if data.iChadTradeMissions >= 3 and data.iChadDiplomacyMissions >= 1:
				win(iChad, 0)
					
def onPeaceBrokered(iBroker, iPlayer1, iPlayer2):

	# third Canadian goal: end twelve wars through diplomacy by 2000 AD
	if iBroker == iCanada:
		if isPossible(iCanada, 2):
			data.iCanadianPeaceDeals += 1
			if data.iCanadianPeaceDeals >= 12:
				win(iCanada, 2)

def getTopCivsInGroup(iGroup, lExclude):
	lTopCivs = []
	iTopScore = -1
	iCurrentScore = -1
	for iCiv in lCivGroups[iGroup]:
		if gc.getPlayer(iCiv).isAlive():
			if iCiv not in lExclude:
				iCurrentScore = gc.getPlayer(iCiv).calculateScore(False, False)
				if iCurrentScore == iTopScore:
					lTopCivs.append(iCiv)
				elif iCurrentScore > iTopScore:
					lTopCivs = [iCiv]
					iTopScore = iCurrentScore
	return lTopCivs

def onUnitGifted(unit, iOwner, plot):

	# second Australian goal: Gift 10 Digger, Marines or Mechanized Infantry to three different civilizations by 1950 AD
	if iOwner == iAustralia:
		if isPossible(iAustralia, 1):
			if unit.getUnitType() in [iDigger, iMarine, iMechanizedInfantry]:
				iReceiver = plot.getOwner()
				if iReceiver not in data.lAustralianGiftReceivers:
					data.lAustralianGiftReceivers.append(iReceiver)
				data.iAustraliaGifts += 1
				if data.iAustraliaGifts >= 10 and len(data.lAustralianGiftReceivers) >= 3:
					win(iAustralia, 1)
			
def onBlockade(iPlayer, iGold):

	# third Moorish goal: acquire 3000 gold through piracy by 1650 AD
	if iPlayer == iMoors:
		if isPossible(iMoors, 2):
			data.iMoorishGold += iGold
			
def onFirstContact(iPlayer, iHasMetPlayer):

	# second Muisca goal: Control 25% of the New World population and the largest average city population in the New World at the time of Old World contact
	if isPossible(iMuisca, 0):
		
		if iHasMetPlayer >= iNumPlayers: return
		
		if iPlayer in [iInuit]: return

		if gc.getGame().getGameTurn() > getTurnForYear(tBirth[iAztecs]) + 2 and gc.getGame().getGameTurn() < getTurnForYear(1800):
			iOldWorldCiv = -1
			iNewWorldCiv = -1
			if iPlayer in lCivBioNewWorld and iHasMetPlayer in lCivBioOldWorld:
				iNewWorldCiv = iPlayer
				iOldWorldCiv = iHasMetPlayer
			if iOldWorldCiv != -1 and iNewWorldCiv != -1:
				iAveragePlayer = -1
				iAverageScore = -1
				iLoopScore = -1
				for iLoopPlayer in lCivBioNewWorld:
					iLoopScore = getAverageCitySize(iLoopPlayer)
					if iLoopScore > iAverageScore or (iLoopScore == iAverageScore and iAveragePlayer == iMuisca):
						iAveragePlayer = iLoopPlayer
						iAverageScore = iLoopScore
						
				if iAveragePlayer == iMuisca:
					win(iMuisca, 0)
				else:
					lose(iMuisca, 0)
				

	# third Maya goal: make contact with a European civilization before they have discovered America
	if not pMaya.isReborn() and isPossible(iMaya, 2):
		
		if iPlayer >= iNumPlayers or iHasMetPlayer >= iNumPlayers: return
		
		if iPlayer == iMaya or iHasMetPlayer == iMaya:
			if iPlayer == iMaya and iHasMetPlayer in lCivGroups[0]: iEuropean = iHasMetPlayer
			elif iHasMetPlayer == iMaya and iPlayer in lCivGroups[0]: iEuropean = iPlayer
			else: return
		
			lPlots = utils.getPlotList(tNorthAmericaTL, (tNorthAmericaBR[0]+2, tNorthAmericaBR[1])) + utils.getPlotList(tSouthCentralAmericaTL, (tSouthCentralAmericaBR[0]+2, tSouthCentralAmericaBR[1]))
			for (x, y) in lPlots:
				plot = gc.getMap().plot(x, y)
				if plot.isRevealed(iEuropean, False) and not plot.isWater():
					lose(iMaya, 2)
					return
					
def onPlayerChangeStateReligion(iPlayer, iStateReligion):

	# second Ethiopian goal: convert to Orthodoxy five turns after it is founded
	if iPlayer == iEthiopia:
		if iStateReligion == iOrthodoxy:
			if gc.getGame().isReligionFounded(iOrthodoxy):
				if gc.getGame().getGameTurn() <= gc.getGame().getReligionGameTurnFounded(iOrthodoxy) + utils.getTurns(5):
					data.bEthiopiaConverted = True
			
def onRevolution(iPlayer):
	if gc.getPlayer(iLoopPlayer).getCivics(iCivicsReligion) == iTolerance:
		if isPossible(iHungary, 1):
			if iPlayer == iHungary:
				data.bHungaryTolerance = True
			else: lose(iHungary, 1)
			
def onChangeWar(bWar, iTeam, iOtherTeam):
	if bWar:
		if iOtherTeam == iOman:
			data.lOmaniEnemies.append(iTeam)
	
def onCollapse(iPlayer, bComplete):
	# third Yemeni goal: Do not allow any Persian or Turkic nation to conquer a city in the Arabian Peninsula prior to the Collapse of the Ottomans
	if isPossible(iYemen, 2) and iPlayer == iOttomans:
		win(iYemen, 2)
	
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
			if data.iPopeTurns >= utils.getTurns(100): return 1
			
		# second Catholic goal: control the Catholic shrine and make sure 12 great prophets are settled in Catholic civilizations
		elif iGoal == 1:
			bShrine = getNumBuildings(iPlayer, iCatholicShrine) > 0
			iSaints = countReligionSpecialists(iCatholicism, iSpecialistGreatProphet)
			
			if bShrine and iSaints >= 12: return 1
			
		# third Catholic goal: make sure 50% of world territory is controlled by Catholic civilizations
		elif iGoal == 2:
			if getReligiousLand(iCatholicism) >= 50.0: return 1
	
	elif iVictoryType == iProtestantism:
		
		# first Protestant goal: be first to discover Civil Liberties, Constitution and Economics
		if iGoal == 0:
			lProtestantTechs = [iCivilLiberties, iSocialContract, iLogistics]
			if checkTechGoal(iPlayer, lProtestantTechs): return 1
			elif data.lFirstDiscovered[iCivilLiberties] not in [iPlayer, -1] or data.lFirstDiscovered[iSocialContract] not in [iPlayer, -1] or data.lFirstDiscovered[iLogistics] not in [iPlayer, -1]: return 0
			
		# second Protestant goal: make sure five great merchants and great engineers are settled in Protestant civilizations
		elif iGoal == 1:
			iEngineers = countReligionSpecialists(iProtestantism, iSpecialistGreatEngineer)
			iMerchants = countReligionSpecialists(iProtestantism, iSpecialistGreatMerchant)
			if iEngineers >= 5 and iMerchants >= 5: return 1
			
		# third Protestant goal: make sure at least half of all civilizations are Protestant or Secular
		elif iGoal == 2:
			iProtestantCivs, iTotal = countReligionPlayers(iProtestantism)
			iSecularCivs, iTotal = countCivicPlayers(iCivicsReligion, iSecularism)
			
			if 2 * (iProtestantCivs + iSecularCivs) >= iTotal: return 1
			
	elif iVictoryType == iIslam:
	
		# first Muslim goal: spread Islam to 40%
		if iGoal == 0:
			fReligionPercent = gc.getGame().calculateReligionPercent(iIslam)
			if fReligionPercent >= 40.0: return 1
			
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
			if data.iHinduGoldenAgeTurns >= utils.getTurns(24): return 1
			
		# third Hindu goal: make sure the five largest cities in the world are Hindu
		elif iGoal == 2:
			if countBestCitiesReligion(iHinduism, cityPopulation, 5) >= 5: return 1
			
	elif iVictoryType == iBuddhism:
	
		# first Buddhist goal: be at peace for 100 turns
		if iGoal == 0:
			if data.iBuddhistPeaceTurns >= utils.getTurns(100): return 1
			
		# second Buddhist goal: have the highest approval rating for 100 turns
		elif iGoal == 1:
			if data.iBuddhistHappinessTurns >= utils.getTurns(100): return 1
			
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
			if data.iTaoistHealthTurns >= utils.getTurns(100): return 1
			
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
			
		# second Zoroastrian goal: spread Zoroastrianism to 10%
		if iGoal == 1:
			fReligionPercent = gc.getGame().calculateReligionPercent(iZoroastrianism)
			if fReligionPercent >= 10.0: return 1
			
		# third Zoroastrian goal: have legendary culture in the Zoroastrian holy city
		elif iGoal == 2:
			pHolyCity = gc.getGame().getHolyCity(iZoroastrianism)
			if pHolyCity.getOwner() == iPlayer and pHolyCity.getCultureLevel() >= 6: return 1
			
	elif iVictoryType == iVictoryPaganism:
	
		# first Pagan goal: make sure there are 15 pagan temples in the world
		if iGoal == 0:
			if countWorldBuildings(iPaganTemple) >= 15: return 1
			
		# second Pagan goal: depends on Pagan religion
		elif iGoal == 1:
			paganReligion = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getPaganReligionName(0)
			
			# Anunnaki: have more wonders in your capital than any other city in the world
			if paganReligion == "Anunnaki":
				capital = pPlayer.getCapitalCity()
				
				if capital and isBestCity(iPlayer, (capital.getX(), capital.getY()), cityWonders):
					return 1
					
			# Asatru: have five units of level five
			elif paganReligion == "Asatru":
				if countUnitsOfLevel(iPlayer, 5) >= 5:
					return 1
					
			# Atua: acquire four pearl resources and 50 Ocean tiles
			elif paganReligion == "Atua":
				if pPlayer.getNumAvailableBonuses(iPearls) >= 4 and countControlledTerrain(iPlayer, iOcean) >= 50:
					return 1
			
			# Baalism: make your capital the city with the highest trade income in the world
			elif paganReligion == "Baalism":
				capital = pPlayer.getCapitalCity()
				
				if capital and isBestCity(iPlayer, (capital.getX(), capital.getY()), cityTradeIncome):
					return 1
					
			# Druidism: control 20 unimproved Forest or Marsh tiles
			elif paganReligion == "Druidism":
				if countControlledFeatures(iPlayer, iForest, -1) + countControlledFeatures(iPlayer, iMud, -1) >= 20:
					return 1
					
			# Inti: have more gold in your treasury than the rest of the world combined
			elif paganReligion == "Inti":
				if 2 * pPlayer.getGold() >= getGlobalTreasury():
					return 1
					
			# Mazdaism: acquire six incense resources
			elif paganReligion == "Mazdaism":
				if pPlayer.getNumAvailableBonuses(iIncense) >= 6:
					return 1
					
			# Olympianism: control ten wonders that require no state religion
			elif paganReligion == "Olympianism":
				if countReligionWonders(iPlayer, -1) >= 10:
					return 1
					
			# Pesedjet: be the first to create to three different types of great person
			elif paganReligion == "Pesedjet":
				if countFirstGreatPeople(iPlayer) >= 3:
					return 1
				
			# Rodnovery: acquire seven fur resources
			elif paganReligion == "Rodnovery":
				if pPlayer.getNumAvailableBonuses(iFur) >= 7:
					return 1
					
			# Shendao: control 25% of the world's population
			elif paganReligion == "Shendao":
				if getPopulationPercent(iPlayer) >= 25.0:
					return 1
					
			# Shinto: settle three great spies in your capital
			elif paganReligion == "Shinto":
				capital = pPlayer.getCapitalCity()
				
				if capital and countCitySpecialists(iPlayer, (capital.getX(), capital.getY()), iSpecialistGreatSpy) >= 3:
					return 1
			
			# Tengri: acquire eight horse resources
			elif paganReligion == "Tengri":
				if pPlayer.getNumAvailableBonuses(iHorse) >= 8:
					return 1
				
			# Teotl: sacrifice ten slaves
			elif paganReligion == "Teotl":
				if iPlayer == iTeotihuacan:
					if data.iTeotlSacrifices >= 200:
						return 1
				elif iPlayer == iOlmecs:
					capital = pPlayer.getCapitalCity()
					if capital and countCitySpecialists(iPlayer, (capital.getX(), capital.getY()), iSpecialistGreatArtist) >= 3:
						return 1
				elif data.iTeotlSacrifices >= 10:
					return 1
					
			# Vedism: have 100 turns of cities celebrating "We Love the King" day
			elif paganReligion == "Vedism":
				if data.iVedicHappiness >= 100:
					return 1
					
			# Yoruba: acquire eight ivory resources and six gem resources
			elif paganReligion == "Yoruba":
				if pPlayer.getNumAvailableBonuses(iIvory) >= 8 and pPlayer.getNumAvailableBonuses(iGems) >= 6:
					return 1
			# Midewiwin: Acquire 4 Corn Resources and construct 20 Farms
			elif paganReligion == "Midewiwin":
				bCorn = pPlayer.getNumAvailableBonuses(iCorn) >= 4
				bFarms = countImprovements(iPlayer, iFarm) >= 20
				
				if bCorn and bFarms:
					return 1
					
			# Angakkuq: Acquire and work 3 crab, fish, and whale resources
			elif paganReligion == "Angakkuq":
				bCrab = countResources(iPlayer, iCrab) >= 3
				bFish = countResources(iPlayer, iFish) >= 3
				bWhale = countResources(iPlayer, iWhales) >= 3
				
				if bCrab and bFish and bWhale:
					return 1
			
		# third Pagan goal: don't allow more than half of your cities to have a religion
		elif iGoal == 2:
			if data.bPolytheismNeverReligion: return 1
			
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
			iUniversities = countCivicBuildings(iCivicsReligion, iSecularism, iUniversity)
			iScientists = countCivicSpecialists(iCivicsReligion, iSecularism, iSpecialistGreatScientist)
			iStatesmen = countCivicSpecialists(iCivicsReligion, iSecularism, iSpecialistGreatStatesman)
			if iUniversities >= 25 and iScientists >= 10 and iStatesmen >= 10: return 1
			
		# third Secular goal: make sure the five most advanced civilizations are secular
		elif iGoal == 2:
			iCount = 0
			lAdvancedPlayers = utils.getSortedList([iLoopPlayer for iLoopPlayer in range(iNumPlayers) if gc.getPlayer(iLoopPlayer).isAlive() and not utils.isAVassal(iLoopPlayer)], lambda iLoopPlayer: gc.getTeam(iLoopPlayer).getTotalTechValue(), True)
			for iLoopPlayer in lAdvancedPlayers[:5]:
				if gc.getPlayer(iLoopPlayer).getCivics(iCivicsReligion) == iSecularism:
					iCount += 1
			if iCount >= 5: return 1
			
	return -1

### UTILITY METHODS ###

def lose(iPlayer, iGoal):
	data.players[iPlayer].lGoals[iGoal] = 0
	if utils.getHumanID() == iPlayer and gc.getGame().getGameTurn() > utils.getScenarioStartTurn() and AlertsOpt.isShowUHVFailPopup():
		utils.show(localText.getText("TXT_KEY_VICTORY_GOAL_FAILED_ANNOUNCE", (iGoal+1,)))
	
def win(iPlayer, iGoal):
	data.players[iPlayer].lGoals[iGoal] = 1
	data.players[iPlayer].lGoalTurns[iGoal] = gc.getGame().getGameTurn()
	checkHistoricalVictory(iPlayer)
	
def expire(iPlayer, iGoal):
	if isPossible(iPlayer, iGoal): lose(iPlayer, iGoal)
	
def isWon(iPlayer, iGoal):
	return data.players[iPlayer].lGoals[iGoal] == 1
	
def isLost(iPlayer, iGoal):
	return data.players[iPlayer].lGoals[iGoal] == 0
	
def isPossible(iPlayer, iGoal):
	return data.players[iPlayer].lGoals[iGoal] == -1
	
def loseAll(iPlayer):
	for i in range(3): data.players[iPlayer].lGoals[i] = 0
	
def countAchievedGoals(iPlayer):
	iCount = 0
	for i in range(3):
		if isWon(iPlayer, i): iCount += 1
	return iCount
	
def isFounded(iReligion):
	return data.lReligionFounder[iReligion] != -1
	
def isWonderBuilt(iWonder):
	return data.getWonderBuilder(iWonder) != -1
	
def isDiscovered(iTech):
	return data.lFirstDiscovered[iTech] != -1
	
def isEntered(iEra):
	return data.lFirstEntered[iEra] != -1
	
def isEraCompleted(iEra):
	return data.lFirstCompleted[iEra] != -1
	
def checkEraCompleted(iPlayer, iEra):
	teamPlayer = gc.getTeam(iPlayer)
	for iTech in range(iNumTechs):
		if gc.getTechInfo(iTech).getEra() != iEra: continue
		if not teamPlayer.isHasTech(iTech):
			return False
	return True
	
def isGreatPersonTypeBorn(iGreatPerson):
	if iGreatPerson not in lGreatPeopleUnits: return True
	return getFirstBorn(iGreatPerson) != -1
	
def getFirstBorn(iGreatPerson):
	if iGreatPerson not in lGreatPeopleUnits: return -1
	return data.lFirstGreatPeople[lGreatPeopleUnits.index(iGreatPerson)]
	
	
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
	
def cityWonders(city):
	if not city: return 0
	return len([iWonder for iWonder in lWonders if city.isHasRealBuilding(iWonder)])

def cityTradeIncome(city):
	if not city: return 0
	return city.getTradeYield(YieldTypes.YIELD_COMMERCE)

def cityResearchOutput(city):
	if not city: return 0
	return city.getCommerceRate(CommerceTypes.COMMERCE_RESEARCH)

def cityHappiness(city):
	if not city: return 0
	
	iHappiness = 0
	iHappiness += city.happyLevel()
	iHappiness -= city.unhappyLevel(0)
	iHappiness += city.getPopulation()
	
	return iHappiness
	
def getBestPlayer(iPlayer, function, lPlayers = [iPlayer for iPlayer in range(iNumPlayers)]):
	iBestPlayer = iPlayer
	iBestValue = function(iPlayer)
	
	for iLoopPlayer in lPlayers:
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if function(iLoopPlayer) > iBestValue:
				iBestPlayer = iLoopPlayer
				iBestValue = function(iLoopPlayer)
				
	return iBestPlayer
	
def isBestPlayer(iPlayer, function, lPlayers = [iPlayer for iPlayer in range(iNumPlayers)]):
	return getBestPlayer(iPlayer, function, lPlayers) == iPlayer
	
def playerTechs(iPlayer):
	iValue = 0
	for iTech in range(iNumTechs):
		if gc.getTeam(iPlayer).isHasTech(iTech):
			iValue += gc.getTechInfo(iTech).getResearchCost()
	return iValue
	
def playerRealPopulation(iPlayer):
	return gc.getPlayer(iPlayer).getRealPopulation()
	
def playerCultureOutput(iPlayer):
	return gc.getPlayer(iPlayer).getCommerceRate(CommerceTypes.COMMERCE_CULTURE)
	
def playerTotalCulture(iPlayer):
	iCulture = 0
	for city in utils.getCityList(iPlayer):
		iCulture += cityCulture(city)
	return iCulture
	
def playerResearchOutput(iPlayer):
	return gc.getPlayer(iPlayer).getCommerceRate(CommerceTypes.COMMERCE_RESEARCH)

def playerFoodOutput(iPlayer):
	return gc.getPlayer(iPlayer).calculateTotalYield(YieldTypes.YIELD_FOOD)
	
def playerProductionOutput(iPlayer):
	return gc.getPlayer(iPlayer).calculateTotalYield(YieldTypes.YIELD_PRODUCTION)
	
def playerCommerceOutput(iPlayer):
	return gc.getPlayer(iPlayer).calculateTotalYield(YieldTypes.YIELD_COMMERCE)
	
def playerArmySize(iPlayer):
	iCount = 0
	for unit in PyPlayer(iPlayer).getUnitList():
		if unit.canFight() and unit.getDomainType() == DomainTypes.DOMAIN_LAND:
			iCount += 1
	return iCount
	
def playerArmyPower(iPlayer):
	iCount = 0
	for unit in PyPlayer(iPlayer).getUnitList():
		if unit.canFight() and unit.getDomainType() == DomainTypes.DOMAIN_LAND:
			iCount += gc.getUnitInfo(unit.getUnitType()).getPowerValue()
	return iCount
	
def getNumBuildings(iPlayer, iBuilding):
	return gc.getPlayer(iPlayer).countNumBuildings(iBuilding)
	
def getPopulationPercent(iPlayer, cityFunction = None):
	iTotalPopulation = gc.getGame().getTotalPopulation()
	if iTotalPopulation == 0: return 0.0
	
	iPopulation = 0
	
	if cityFunction is None:
		iPopulation = gc.getTeam(iPlayer).getTotalPopulation()
	else:
		for city in utils.getCityList(iPlayer):
			if cityFunction(city):
				iPopulation += city.getPopulation()
	
	return 100.0 * iPopulation / iTotalPopulation
	
def getPopulationPercentInRegions(iPlayer, lRegions):
	iTotalPopulation = 0
	iPlayerPopulation = 0
	iTempPopulation = 0
	
	for city in utils.getRegionCities(lRegions):
		iTempPopulation = city.getPopulation()
		iTotalPopulation += iTempPopulation
		if city.getOwner() == iPlayer:
			iPlayerPopulation += iTempPopulation
			
	return 100.0 * iPlayerPopulation / iTotalPopulation
	
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
	
def getCitiesInRegions(iPlayer, lRegions):
	return [city for city in utils.getCityList(iPlayer) if city.getRegionID() in lRegions]
	
def getNumCitiesInRegions(iPlayer, lRegions):
	return len(getCitiesInRegions(iPlayer, lRegions))
	
def getNumFoundedCitiesInArea(iPlayer, lPlots):
	return len([city for city in utils.getAreaCitiesCiv(iPlayer, lPlots) if city.getOriginalOwner() == iPlayer])
	
def getNumConqueredCitiesInArea(iPlayer, lPlots):
	return len([city for city in utils.getAreaCitiesCiv(iPlayer, lPlots) if city.getOriginalOwner() != iPlayer])
	
def checkOwnedCiv(iPlayer, iOwnedPlayer):
	iPlayerCities = getNumCitiesInArea(iPlayer, Areas.getNormalArea(iOwnedPlayer, False))
	iOwnedCities = getNumCitiesInArea(iOwnedPlayer, Areas.getNormalArea(iOwnedPlayer, False))
	
	return (iPlayerCities >= 2 and iPlayerCities > iOwnedCities) or (iPlayerCities >= 1 and not gc.getPlayer(iOwnedPlayer).isAlive()) or (iPlayerCities >= 1 and iOwnedPlayer == iCarthage)
	
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
	if lOwners:
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
	
def countControlledTilesInRegion(iPlayer, rRegion, bVassals=False, bCoastalOnly=False):
	lValidOwners = [iPlayer]
	iCount = 0
	iTotal = 0
	
	if bVassals:
		for iLoopPlayer in range(iNumPlayers):
			if gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isVassal(iPlayer):
				lValidOwners.append(iLoopPlayer)
				
	for (x, y) in utils.getRegionPlots(rRegion):
		plot = gc.getMap().plot(x, y)
		if plot.isWater(): continue
		if bCoastalOnly and not plot.isCoastalLand(): continue
		iTotal += 1
		if plot.getOwner() in lValidOwners: iCount += 1
		
	return iCount, iTotal
	
def countControlledTilesInRegions(iPlayer, lRegions, bVassals=False, bCoastalOnly=False):
	iCount = 0
	iTotal = 0
	for rRegion in lRegions:
		iTempCount, iTempTotal = countControlledTilesInRegion(iPlayer, rRegion, bVassals, bCoastalOnly)
		iCount += iTempCount
		iTotal += iTempTotal
		
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

def areRegionsFreeOfCivs(lRegions, lCivs):
	for city in utils.getRegionCities(lRegions):
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
	
def isConnected(tStart, lTargets, plotFunction):
	if not lTargets: return False
	if not plotFunction(tStart): return False
	
	if tStart in lTargets: return True
	if not [tTarget for tTarget in lTargets if plotFunction(tTarget)]: return False
	
	lNodes = [(utils.minimalDistance(tStart, lTargets, plotFunction), tStart)]
	heapq.heapify(lNodes)
	lVisitedNodes = []
	
	while lNodes:
		h, tNode = heapq.heappop(lNodes)
		lVisitedNodes.append((h, tNode))
		
		for tPlot in utils.surroundingPlots(tNode):
			if plotFunction(tPlot):
				if tPlot in lTargets: return True
				
				tTuple = (utils.minimalDistance(tPlot, lTargets, plotFunction), tPlot)
				if not tTuple in lVisitedNodes and not tTuple in lNodes:
					heapq.heappush(lNodes, tTuple)
							
	return False
	
def isConnectedByTradeRoute(iPlayer, lStarts, lTargets):
	for tStart in lStarts:
		startPlot = utils.plot(tStart)
		if not startPlot.isCity(): continue
		
		plotFunction = lambda tPlot: utils.plot(tPlot).getOwner() in [iPlayer, startPlot.getOwner()] and (utils.plot(tPlot).isCity() or utils.plot(tPlot).getRouteType() in [iRouteRoad, iRouteRailroad, iRouteRomanRoad, iRouteHighway])
	
		if isConnected(tStart, lTargets, plotFunction): return True
		
	return False
	
def isConnectedByLand(iPlayer, lStarts, lTargets):
	lValidTargets = lTargets
	for tTarget in lValidTargets:
		if not utils.plot(tTarget).isCity:
			lValidTargets.remove(tTarget)
	
	for tStart in lStarts:
		startPlot = utils.plot(tStart)
		if not startPlot.isCity(): continue
		
		plotFunction = lambda tPlot: utils.plot(tPlot).getOwner() == iPlayer and not utils.plot(tPlot).isWater()
	
		if isConnected(tStart, lTargets, plotFunction): return True
		
	return False
	
def isConnectedByRailroad(iPlayer, tStart, lTargets):
	if not gc.getTeam(iPlayer).isHasTech(iRailroad): return False
	
	startPlot = utils.plot(tStart)
	if not (startPlot.isCity() and startPlot.getOwner() == iPlayer): return False
	
	plotFunction = lambda tPlot: utils.plot(tPlot).getOwner() == iPlayer and (utils.plot(tPlot).isCity() or utils.plot(tPlot).getRouteType() == iRouteRailroad)
	
	return isConnected(tStart, lTargets, plotFunction)
	
def isConnectedByRoute(iPlayer, tStart, lTargets):
	if not gc.getTeam(iPlayer).isHasTech(iLeverage): return False
	
	startPlot = utils.plot(tStart)
	if not (startPlot.isCity() and startPlot.getOwner() == iPlayer): return False
	
	plotFunction = lambda tPlot: utils.plot(tPlot).getOwner() == iPlayer and (utils.plot(tPlot).isCity() or utils.plot(tPlot).getRouteType() != -1)
	
	return isConnected(tStart, lTargets, plotFunction)

def countPlayersWithAttitudeAndCriteria(iPlayer, eAttitude, function):
	return len([iOtherPlayer for iOtherPlayer in range(iNumPlayers) if gc.getPlayer(iPlayer).canContact(iOtherPlayer) and gc.getPlayer(iOtherPlayer).AI_getAttitude(iPlayer) >= eAttitude and function(iOtherPlayer)])
	
def countPlayersWithAttitudeAndReligion(iPlayer, eAttitude, iReligion, bStateReligion = False):
	iCount = 0
	for iLoopPlayer in range(iNumPlayers):
		if iLoopPlayer == iPlayer: continue
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.AI_getAttitude(iPlayer) >= eAttitude:
			if bStateReligion:
				if pLoopPlayer.getStateReligion() == iReligion:
					iCount += 1
					break
			else:
				for city in utils.getCityList(iLoopPlayer):
					if city.isHasReligion(iReligion):
						iCount += 1
						break
	return iCount
	
def countPlayersWithAttitudeInGroup(iPlayer, eAttitude, lOtherPlayers):
	return countPlayersWithAttitudeAndCriteria(iPlayer, eAttitude, lambda x: not gc.getTeam(gc.getPlayer(x).getTeam()).isAVassal())
	
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
	
def countCitiesWithCultureLevelAndSize(iPlayer, iCulture, iPop):
	iCount = 0
	for city in utils.getCityList(iPlayer):
		if city.getPopulation() >= iPop and city.getCultureLevel() >= iCulture:
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
	
def isCultureControlled(iPlayer, lPlots, bIgnoreWater = False, bRequireAll = False):
	for tPlot in lPlots:
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		if bIgnoreWater and plot.isWater(): continue
		if (plot.getOwner() != -1 and plot.getOwner() != iPlayer) or (plot.getOwner() == -1 and bRequireAll):
			return False
	return True
	
def controlsCity(iPlayer, tPlot):
	for (x, y) in utils.surroundingPlots(tPlot):
		plot = gc.getMap().plot(x, y)
		if plot.isCity() and plot.getPlotCity().getOwner() == iPlayer:
			return True
	return False
	
def getTotalCulture(lPlayers):
	iTotalCulture = 0
	for iPlayer in lPlayers:
		iTotalCulture += gc.getPlayer(iPlayer).countTotalCulture()
	return iTotalCulture
	
def countImprovements(iPlayer, iImprovement):
	if iImprovement <= 0: return 0
	return gc.getPlayer(iPlayer).getImprovementCount(iImprovement)
	
def controlsAllCities(iPlayer, tTopLeft, tBottomRight, tExceptions=()):
	for city in utils.getAreaCities(utils.getPlotList(tTopLeft, tBottomRight, tExceptions)):
		if city.getOwner() != iPlayer: return False
	return True
	
def controlsOrVassalizedAllCities(iPlayer, tTopLeft, tBottomRight, tExceptions=()):
	lValidOwners = [iPlayer]
	for iLoopPlayer in range(iNumPlayers):
		if gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isVassal(iPlayer):
			lValidOwners.append(iLoopPlayer)
	for city in utils.getAreaCities(utils.getPlotList(tTopLeft, tBottomRight, tExceptions)):
		if not city.getOwner() in lValidOwners: return False
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
	if gc.getPlayer(iPlayer).getCurrentEra() < iGlobal: return False
	
	tPlayer = gc.getTeam(iPlayer)
	for iTech in range(iNumTechs):
		if not (tPlayer.isHasTech(iTech) or tPlayer.getTechCount(iTech) > 0): return False
		
	return True
	
def countFirstDiscovered(iPlayer, iEra):
	iCount = 0
	for iTech in range(iNumTechs):
		if gc.getTechInfo(iTech).getEra() == iEra and data.lFirstDiscovered[iTech] == iPlayer:
			iCount += 1
	return iCount
	
def isFirstDiscoveredPossible(iPlayer, iEra, iRequired):
	iCount = countFirstDiscovered(iPlayer, iEra)
	iNotYetDiscovered = countFirstDiscovered(-1, iEra)
	return iCount + iNotYetDiscovered >= iRequired
	
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
	
def getBestCities(function):
	lCities = []
	for iLoopPlayer in range(iNumPlayers):
		lCities.extend(utils.getCityList(iLoopPlayer))
	
	return utils.getSortedList(lCities, function, True)
	
def countBestCitiesReligion(iReligion, function, iNumCities):
	lCities = getBestCities(function)
	
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
	if getNumBuildings(iPlayer, iDomeOfTheRock) > 0 and not gc.getTeam(iPlayer).isHasTech(iLiberalism): iThreshold = 40
	
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
	
def countUnitsOfLevel(iPlayer, iLevel):
	pPlayer = gc.getPlayer(iPlayer)
	iCount = 0
	
	for iUnit in range(pPlayer.getNumUnits()):
		unit = pPlayer.getUnit(iUnit)
		if unit.getLevel() >= iLevel:
			iCount += 1
			
	return iCount
	
def countControlledTerrain(iPlayer, lTerrains, bCountWorked = False):
	iCount = 0
	iWorked = 0
	
	if isinstance(lTerrains, int):
		lTerrains = [lTerrains]
	
	for (x, y) in utils.getWorldPlotsList():
		plot = gc.getMap().plot(x, y)
		if plot.getOwner() == iPlayer and plot.getTerrainType() in lTerrains:
			iCount += 1
			if bCountWorked and plot.isBeingWorked():
				iWorked += 1
			
	if bCountWorked:
		return (iCount, iWorked) 
	else:
		return iCount
	
def countControlledFeatures(iPlayer, iFeature, iImprovement):
	iCount = 0
	
	for (x, y) in utils.getWorldPlotsList():
		plot = gc.getMap().plot(x, y)
		if plot.getOwner() == iPlayer and plot.getFeatureType() == iFeature and plot.getImprovementType() == iImprovement:
			iCount += 1
			
	return iCount
	
def countControlledResources(iPlayer, iResource, iImprovement, iWorkedOnly = False):
	iCount = 0
	
	for (x, y) in utils.getWorldPlotsList():
		plot = gc.getMap().plot(x, y)
		if plot.getOwner() == iPlayer and plot.getBonusType(iPlayer) == iResource and plot.getImprovementType() == iImprovement:
			if (not iWorkedOnly) or plot.isBeingWorked():
				iCount += 1
			
	return iCount
	
def countControlledResourcesInRegions(lPlayers, lRegions, lResources, iImprovement, iWorkedOnly = False):
	iCount = 0
	
	for rRegion in lRegions:
		for (x, y) in utils.getRegionPlots(rRegion):
			plot = gc.getMap().plot(x, y)
			if plot.getOwner() in lPlayers and plot.getBonusType(plot.getOwner()) in lResources and plot.getImprovementType() == iImprovement:
				if (not iWorkedOnly) or plot.isBeingWorked():
					iCount += 1
			
	return iCount
	
def getGlobalTreasury():
	iTreasury = 0

	for iPlayer in range(iNumPlayers):
		iTreasury += gc.getPlayer(iPlayer).getGold()
		
	return iTreasury
	
def countFirstGreatPeople(iPlayer):
	return len([iGreatPerson for iGreatPerson in lGreatPeopleUnits if getFirstBorn(iGreatPerson) == iPlayer])
	
def countReligionSpecialistCities(iPlayer, iReligion, iSpecialist):
	iCount = 0
	for city in utils.getCityList(iPlayer):
		if city.isHasReligion(iReligion) and city.getFreeSpecialistCount(iSpecialist) > 0:
			iCount += 1
	return iCount
	
def calculateAlliedPercent(iPlayer, function):
	pTeam = gc.getTeam(gc.getPlayer(iPlayer).getTeam())

	iAlliedValue = 0
	iTotalValue = 0
	
	for iLoopPlayer in range(iNumPlayers):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		pLoopTeam = gc.getTeam(pLoopPlayer.getTeam())
		
		if not pLoopPlayer.isAlive(): continue
		
		iValue = function(iLoopPlayer)
		
		iTotalValue += iValue
		
		if iLoopPlayer == iPlayer or pLoopTeam.isVassal(gc.getPlayer(iPlayer).getTeam()) or pTeam.isDefensivePact(pLoopPlayer.getTeam()):
			iAlliedValue += iValue
			
	if iTotalValue == 0: return 0
	
	return 100.0 * iAlliedValue / iTotalValue
	
def calculateAlliedCommercePercent(iPlayer):
	return calculateAlliedPercent(iPlayer, lambda x: gc.getPlayer(x).calculateTotalCommerce())
	
def calculateAlliedPowerPercent(iPlayer):
	return calculateAlliedPercent(iPlayer, lambda x: gc.getPlayer(x).getPower())
	
def countRegionReligion(iReligion, lRegions):
	lCities = [gc.getMap().plot(x, y).getPlotCity() for (x, y) in utils.getRegionPlots(lRegions) if gc.getMap().plot(x, y).isCity()]
	return len([city for city in lCities if city.isHasReligion(iReligion)])
	
def findBestCityWith(iPlayer, filter, sort):
	lCities = [city for city in utils.getCityList(iPlayer) if filter(city)]
	return utils.getHighestEntry(lCities, sort)
	
def countVassals(iPlayer, lPlayers=None, iReligion=-1):
	lVassals = [iVassal for iVassal in range(iNumPlayers) if gc.getTeam(iVassal).isVassal(iPlayer) and (not lPlayers or iVassal in lPlayers) and (iReligion < 0 or gc.getPlayer(iVassal).getStateReligion() == iReligion)]
	return len(lVassals)
	
def countPopulationInArea(iPlayer, lArea):
	iCount = 0
	for city in utils.getCityList(iPlayer):
		if (city.getX(), city.getY()) in lArea:
			iCount += city.getPopulation()
	return iCount

def isMonopoly(iPlayer, iBonus, lPlots, bIncludeVassals = True):
	if gc.getPlayer(iPlayer).getNumAvailableBonuses(iBonus) <= 0:
		return False
		
	lAllowedOwners = [iPlayer, -1]
	if bIncludeVassals:
		for iLoopPlayer in range(iNumPlayers):
			if gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isVassal(iPlayer):
				lAllowedOwners.append(iLoopPlayer)
		
	for x, y in lPlots:
		plot = gc.getMap().plot(x, y)
		if plot.getBonusType(-1) == iBonus and plot.getImprovementType() >= 0:
			iOwner = plot.getOwner()
			if iOwner < iNumPlayers and iOwner not in lAllowedOwners:
				if gc.getImprovementInfo(plot.getImprovementType()).isImprovementBonusMakesValid(iBonus):
					return False
		
	return True
	
def getCapitalCultureBuildingsLeader(bIncludeWonders = True, bIncludeObsolete = False):
	iLeader = -1
	iLeaderScore = -1
	
	for iPlayer in range(iNumMajorPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if not pPlayer.isAlive(): continue
		capital = pPlayer.getCapitalCity()
		if capital:
			iScore = countCultureBuildings(capital, bIncludeWonders, bIncludeObsolete)
			if iScore > iLeaderScore:
				iLeader = iPlayer
				iLeaderScore = iScore
	return (iLeader, iLeaderScore)
	
def countCultureBuildings(city, bIncludeWonders = True, bIncludeObsolete = False):
	iCount = 0
	for iBuilding in range(iNumBuildings):
		if not bIncludeWonders and iBuilding == iBeginWonders: break
		if not city.isHasRealBuilding(iBuilding): continue
		BuildingInfo = gc.getBuildingInfo(iBuilding)
		iObsoleteTech = BuildingInfo.getObsoleteTech()
		if not bIncludeObsolete and iObsoleteTech != -1 and gc.getTeam(iPlayer).isHasTech(iObsoleteTech): continue
		bIsCulture = False
		if BuildingInfo.getCommerceChange(CommerceTypes.COMMERCE_CULTURE) > 0: bIsCulture = True
		if BuildingInfo.getObsoleteSafeCommerceChange(CommerceTypes.COMMERCE_CULTURE) > 0: bIsCulture = True
		if BuildingInfo.getCommerceModifier(CommerceTypes.COMMERCE_CULTURE) > 0: bIsCulture = True
		if BuildingInfo.getPowerCommerceModifier(CommerceTypes.COMMERCE_CULTURE) > 0: bIsCulture = True
		if not bIsCulture: continue
		iCount += 1
	return iCount
	
def getLargestReligionPopulation(iReligion):
	iLeader = -1
	iPopulation = -1
	for iPlayer in range(iNumMajorPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if not pPlayer.isAlive(): continue
		iCurrent = pPlayer.getReligionPopulation(iReligion)
		if iCurrent > iPopulation:
			iPopulation = iCurrent
			iLeader = iPlayer
	return (iLeader, iPopulation)
	
def getReligionHappiness(iPlayer):
    iStateReligion = gc.getPlayer(iPlayer).getStateReligion()
    iHappiness = 0
    
    for iReligion in range(iNumReligions):
        iTemple = iJewishTemple + 4*iReligion
        iCathedral = iJewishCathedral + 4*iReligion
        
        iHappiness += getNumBuildings(iPlayer, iTemple)
        if iReligion == iStateReligion:
            iHappiness += 2*getNumBuildings(iPlayer, iCathedral)
            
    bTolerant = gc.getPlayer(iPlayer).getCivics(iCivicsReligion) in [iTolerance, iSecularism]
    for city in utils.getCityList(iPlayer):
        if bTolerant:
            iHappiness += city.getReligionCount()
        elif iStateReligion != -1 and city.isHasReligion(iStateReligion):
            iHappiness += 1
            
    return iHappiness
	
def getReligionPlayers(lReligions):
	lPlayers = []
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			if pPlayer.getStateReligion() in lReligions:
				lPlayers.append(iPlayer)
	return lPlayers
	
def getBestCityInRegion(lRegions, function):
	lCities = []
	for iLoopPlayer in range(iNumPlayers):
		for city in getCitiesInRegions(iLoopPlayer, lRegions):
			iValue = function(city)
			lCities.append((city, iValue))
	lCities.sort(key=itemgetter(1), reverse=False)
	return lCities[0]
	
def cityValue(city):
	return ((city.getCulture(city.getOwner()) / 5) + (city.getYieldRate(YieldTypes.YIELD_FOOD) + city.getYieldRate(YieldTypes.YIELD_PRODUCTION) \
				+ city.getYieldRate(YieldTypes.YIELD_COMMERCE))) * city.getPopulation()
	
def getCivsWithHoldingsInRegion(lRegions):
	lAfricaCivs = []
	for iLoopPlayer in range(iNumPlayers):
		if len(getCitiesInRegions(iLoopPlayer, lRegions)) > 0:
			lAfricaCivs.append(iLoopPlayer)
	return lAfricaCivs
	
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
			aHelp.append(getIcon(iOrthodoxCathedrals >= 4) + localText.getText("TXT_KEY_VICTORY_ORTHODOX_CATHEDRALS", ("TXT_KEY_BUILDING_STRING", iOrthodoxCathedrals, 4)))
		elif iGoal == 1:
			lCultureCities = getBestCities(cityCulture)[:5]
			iCultureCities = countBestCitiesReligion(iOrthodoxy, cityCulture, 5)
			for city in lCultureCities:
				aHelp.append(getIcon(city.isHasReligion(iOrthodoxy) and gc.getPlayer(city.getOwner()).getStateReligion() == iOrthodoxy) + city.getName())
		elif iGoal == 2:
			bNoCatholics = countReligionPlayers(iCatholicism)[0] == 0
			aHelp.append(getIcon(bNoCatholics) + localText.getText("TXT_KEY_VICTORY_NO_CATHOLICS", ()))

	elif iVictoryType == iCatholicism:
		if iGoal == 0:
			iPopeTurns = data.iPopeTurns
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
			bCivilLiberties = data.lFirstDiscovered[iCivilLiberties] == iPlayer
			bConstitution = data.lFirstDiscovered[iSocialContract] == iPlayer
			bEconomics = data.lFirstDiscovered[iEconomics] == iPlayer
			aHelp.append(getIcon(bCivilLiberties) + localText.getText("TXT_KEY_TECH_CIVIL_LIBERTIES", ()) + ' ' + getIcon(bConstitution) + localText.getText("TXT_KEY_TECH_CONSTITUTION", ()) + ' ' + getIcon(bEconomics) + localText.getText("TXT_KEY_TECH_ECONOMICS", ()))
		elif iGoal == 1:
			iMerchants = countReligionSpecialists(iProtestantism, iSpecialistGreatMerchant)
			iEngineers = countReligionSpecialists(iProtestantism, iSpecialistGreatEngineer)
			aHelp.append(getIcon(iMerchants >= 5) + localText.getText("TXT_KEY_VICTORY_PROTESTANT_MERCHANTS", (iMerchants, 5)) + ' ' + getIcon(iEngineers >= 5) + localText.getText("TXT_KEY_VICTORY_PROTESTANT_ENGINEERS", (iEngineers, 5)))
		elif iGoal == 2:
			iProtestantCivs, iTotal = countReligionPlayers(iProtestantism)
			iSecularCivs, iTotal = countCivicPlayers(iCivicsReligion, iSecularism)
			iNumProtestantCivs = iProtestantCivs + iSecularCivs
			aHelp.append(getIcon(2 * iNumProtestantCivs >= iTotal) + localText.getText("TXT_KEY_VICTORY_PROTESTANT_CIVS", (iNumProtestantCivs, iTotal)))

	elif iVictoryType == iIslam:
		if iGoal == 0:
			fReligionPercent = gc.getGame().calculateReligionPercent(iIslam)
			aHelp.append(getIcon(fReligionPercent >= 40.0) + localText.getText("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", (gc.getReligionInfo(iIslam).getTextKey(), str(u"%.2f%%" % fReligionPercent), str(40))))
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
			iGoldenAgeTurns = data.iHinduGoldenAgeTurns
			aHelp.append(getIcon(iGoldenAgeTurns >= utils.getTurns(24)) + localText.getText("TXT_KEY_VICTORY_GOLDEN_AGE_TURNS", (iGoldenAgeTurns, utils.getTurns(24))))
		elif iGoal == 2:
			iLargestCities = countBestCitiesReligion(iHinduism, cityPopulation, 5)
			aHelp.append(getIcon(iLargestCities >= 5) + localText.getText("TXT_KEY_VICTORY_HINDU_LARGEST_CITIES", (iLargestCities, 5)))

	elif iVictoryType == iBuddhism:
		if iGoal == 0:
			iPeaceTurns = data.iBuddhistPeaceTurns
			aHelp.append(getIcon(iPeaceTurns >= utils.getTurns(100)) + localText.getText("TXT_KEY_VICTORY_PEACE_TURNS", (iPeaceTurns, utils.getTurns(100))))
		elif iGoal == 1:
			iHappinessTurns = data.iBuddhistHappinessTurns
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
			iHealthTurns = data.iTaoistHealthTurns
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
			aHelp.append(getIcon(fReligionPercent >= 10.0) + localText.getText("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", (gc.getReligionInfo(iZoroastrianism).getTextKey(), str(u"%.2f%%" % fReligionPercent), str(10))))
		elif iGoal == 2:
			holyCity = gc.getGame().getHolyCity(iZoroastrianism)
			aHelp.append(getIcon(holyCity.getOwner() == iPlayer) + localText.getText("TXT_KEY_VICTORY_CONTROL_HOLY_CITY", (holyCity.getName(),)) + ' ' + getIcon(holyCity.getCultureLevel() >= 6) + localText.getText("TXT_KEY_VICTORY_LEGENDARY_CULTURE_CITY", (holyCity.getName(),)))

	elif iVictoryType == iVictoryPaganism:
		if iGoal == 0:
			iCount = countWorldBuildings(iPaganTemple)
			aHelp.append(getIcon(iCount >= 15) + localText.getText("TXT_KEY_VICTORY_NUM_PAGAN_TEMPLES_WORLD", (iCount, 15)))
		elif iGoal == 1:
			aHelp.append(getPaganGoalHelp(iPlayer))
		elif iGoal == 2:
			bPolytheismNeverReligion = data.bPolytheismNeverReligion
			aHelp.append(getIcon(bPolytheismNeverReligion) + localText.getText("TXT_KEY_VICTORY_POLYTHEISM_NEVER_RELIGION", ()))

	elif iVictoryType == iVictorySecularism:
		if iGoal == 0:
			iCount = 0
			for iReligion in range(iNumReligions):
				if getNumBuildings(iPlayer, iCathedral + 4 * iReligion) > 0:
					iCount += 1
			aHelp.append(getIcon(iCount >= iNumReligions) + localText.getText("TXT_KEY_VICTORY_DIFFERENT_CATHEDRALS", (iCount, iNumReligions)))
		elif iGoal == 1:
			iUniversities = countCivicBuildings(iCivicsReligion, iSecularism, iUniversity)
			iScientists = countCivicSpecialists(iCivicsReligion, iSecularism, iSpecialistGreatScientist)
			iStatesmen = countCivicSpecialists(iCivicsReligion, iSecularism, iSpecialistGreatStatesman)
			aHelp.append(getIcon(iUniversities >= 25) + localText.getText("TXT_KEY_VICTORY_SECULAR_UNIVERSITIES", (iUniversities, 25)))
			aHelp.append(getIcon(iScientists >= 10) + localText.getText("TXT_KEY_VICTORY_SECULAR_SCIENTISTS", (iScientists, 10)) + ' ' + getIcon(iStatesmen >= 10) + localText.getText("TXT_KEY_VICTORY_SECULAR_STATESMEN", (iStatesmen, 10)))
		elif iGoal == 2:
			sString = ""
			lAdvancedPlayers = utils.getSortedList([iLoopPlayer for iLoopPlayer in range(iNumPlayers) if gc.getPlayer(iLoopPlayer).isAlive() and not utils.isAVassal(iLoopPlayer)], lambda iLoopPlayer: gc.getTeam(iLoopPlayer).getTotalTechValue(), True)
			for iLoopPlayer in lAdvancedPlayers[:5]:
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				sString += getIcon(pLoopPlayer.getCivics(iCivicsReligion) == iSecularism) + pLoopPlayer.getCivilizationShortDescription(0) + ' '
			aHelp.append(sString)
				
	return aHelp
	
def getPaganGoalHelp(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	paganReligion = gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getPaganReligionName(0)

	if paganReligion == "Anunnaki":
		x, y = 0, 0
		capital = pPlayer.getCapitalCity()
		
		if capital:
			x, y = capital.getX(), capital.getY()
		pBestCity = getBestCity(iPlayer, (x, y), cityWonders)
		bBestCity = isBestCity(iPlayer, (x, y), cityWonders)
		sBestCity = "(none)"
		if pBestCity:
			sBestCity = pBestCity.getName()
		return getIcon(bBestCity) + localText.getText("TXT_KEY_VICTORY_CITY_WITH_MOST_WONDERS", (sBestCity,))
		
	elif paganReligion == "Asatru":
		iCount = countUnitsOfLevel(iPlayer, 5)
		return getIcon(iCount >= 5) + localText.getText("TXT_KEY_VICTORY_UNITS_OF_LEVEL", (5, iCount, 5))
		
	elif paganReligion == "Atua":
		iNumPearls = pPlayer.getNumAvailableBonuses(iPearls)
		iOceanTiles = countControlledTerrain(iPlayer, iOcean)
		return getIcon(iNumPearls >= 4) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", (gc.getBonusInfo(iPearls).getText().lower(), iNumPearls, 4)) + ' ' + getIcon(iOceanTiles >= 50) + localText.getText("TXT_KEY_VICTORY_CONTROLLED_OCEAN_TILES", (iOceanTiles, 50))
		
	elif paganReligion == "Baalism":
		x, y = 0, 0
		capital = pPlayer.getCapitalCity()
		
		if capital:
			x, y = capital.getX(), capital.getY()
		pBestCity = getBestCity(iPlayer, (x, y), cityTradeIncome)
		bBestCity = isBestCity(iPlayer, (x, y), cityTradeIncome)
		return getIcon(bBestCity) + localText.getText("TXT_KEY_VICTORY_HIGHEST_TRADE_CITY", (pBestCity.getName(),))
		
	elif paganReligion == "Druidism":
		iCount = countControlledFeatures(iPlayer, iForest, -1) + countControlledFeatures(iPlayer, iMud, -1)
		return getIcon(iCount >= 20) + localText.getText("TXT_KEY_VICTORY_CONTROLLED_FOREST_AND_MARSH_TILES", (iCount, 20))
	
	elif paganReligion == "Inti":
		iOurTreasury = pPlayer.getGold()
		iWorldTreasury = getGlobalTreasury()
		return getIcon(2 * iOurTreasury >= iWorldTreasury) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iOurTreasury, iWorldTreasury - iOurTreasury))
	
	elif paganReligion == "Mazdaism":
		iCount = pPlayer.getNumAvailableBonuses(iIncense)
		return getIcon(iCount >= 6) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", (gc.getBonusInfo(iIncense).getText().lower(), iCount, 6))
	
	elif paganReligion == "Olympianism":
		iCount = countReligionWonders(iPlayer, -1)
		return getIcon(iCount >= 10) + localText.getText("TXT_KEY_VICTORY_NUM_NONRELIGIOUS_WONDERS", (iCount, 10))
		
	elif paganReligion == "Pesedjet":
		iCount = countFirstGreatPeople(iPlayer)
		return getIcon(iCount >= 3) + localText.getText("TXT_KEY_VICTORY_FIRST_GREAT_PEOPLE", (iCount, 3))
	
	elif paganReligion == "Rodnovery":
		iCount = pPlayer.getNumAvailableBonuses(iFur)
		return getIcon(iCount >= 7) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", (gc.getBonusInfo(iFur).getText().lower(), iCount, 7))
	
	elif paganReligion == "Shendao":
		fPopulationPercent = getPopulationPercent(iPlayer)
		return getIcon(fPopulationPercent >= 25.0) + localText.getText("TXT_KEY_VICTORY_PERCENTAGE_WORLD_POPULATION", (str(u"%.2f%%" % fPopulationPercent), str(25)))
	
	elif paganReligion == "Shinto":
		capital = pPlayer.getCapitalCity()
		iCount = 0
		if capital: iCount = countCitySpecialists(iPlayer, (capital.getX(), capital.getY()), iSpecialistGreatSpy)
		return getIcon(iCount >= 3) + localText.getText("TXT_KEY_VICTORY_CAPITAL_GREAT_SPIES", (iCount, 3))
	
	elif paganReligion == "Tengri":
		iCount = pPlayer.getNumAvailableBonuses(iHorse)
		return getIcon(iCount >= 8) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", (gc.getBonusInfo(iHorse).getText().lower(), iCount, 8))
	
	elif paganReligion == "Teotl":
		iCount = data.iTeotlSacrifices
		if iPlayer == iMaya:
			return getIcon(iCount >= 10) + localText.getText("TXT_KEY_VICTORY_FOOD_FROM_COMBAT", (iCount * 5, 50))
		if iPlayer == iTeotihuacan:
			return getIcon(iCount >= 200) + localText.getText("TXT_KEY_VICTORY_CULTURE_FROM_ARTISANS", (iCount, 200))
		if iPlayer == iOlmecs:
			capital = pPlayer.getCapitalCity()
			iCount = 0
			if capital: iCount = countCitySpecialists(iPlayer, (capital.getX(), capital.getY()), iSpecialistGreatSpy)
			return getIcon(iCount >= 3) + localText.getText("TXT_KEY_VICTORY_CAPITAL_GREAT_ARTISTS", (iCount, 3))
		return getIcon(iCount >= 10) + localText.getText("TXT_KEY_VICTORY_SACRIFICED_SLAVES", (iCount, 10))
	
	elif paganReligion == "Vedism":
		iCount = data.iVedicHappiness
		return getIcon(iCount >= 100) + localText.getText("TXT_KEY_VICTORY_WE_LOVE_RULER_TURNS", (iCount, 100))
	
	elif paganReligion == "Yoruba":
		iNumIvory = pPlayer.getNumAvailableBonuses(iIvory)
		iNumGems = pPlayer.getNumAvailableBonuses(iGems)
		return getIcon(iNumIvory >= 8) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", (gc.getBonusInfo(iIvory).getText().lower(), iNumIvory, 8)) + ' ' + getIcon(iNumGems >= 6) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", (gc.getBonusInfo(iGems).getText().lower(), iNumGems, 6))

	elif paganReligion == "Midewiwin":
		iNumCorn = pPlayer.getNumAvailableBonuses(iCorn)
		iNumFarms = countImprovements(iPlayer, iFarm)
		
		return getIcon(iNumCorn >= 4) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", (gc.getBonusInfo(iCorn).getText().lower(), iNumCorn, 4)) + ' ' + getIcon(iNumFarms >= 20) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_IMPROVEMENT_FARM", iNumFarms, 20))

	elif paganReligion == "Angakkuq":
		iNumCrabs = countResources(iPlayer, iCrab)
		iNumFish = countResources(iPlayer, iFish)
		iNumWhales = countResources(iPlayer, iWhales)
		
		return getIcon(iNumCrabs >= 3) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", (gc.getBonusInfo(iCrab).getText().lower(), iNumCrabs, 3)) + ' ' + getIcon(iNumFish >= 3) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", (gc.getBonusInfo(iFish).getText().lower(), iNumFish, 3)) + ' ' + getIcon(iNumWhales >= 3) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", (gc.getBonusInfo(iWhales).getText().lower(), iNumWhales, 3))
		

def getUHVHelp(iPlayer, iGoal):
	"Returns an array of help strings used by the Victory Screen table"

	aHelp = []

	# the info is outdated or irrelevant once the goal has been accomplished or failed
	if data.players[iPlayer].lGoals[iGoal] == 1:
		iWinTurn = data.players[iPlayer].lGoalTurns[iGoal]
		iTurnYear = gc.getGame().getTurnYear(iWinTurn)
		if iTurnYear < 0:
			sWinDate = localText.getText("TXT_KEY_TIME_BC", (-iTurnYear,))
		else:
			sWinDate = localText.getText("TXT_KEY_TIME_AD", (iTurnYear,))
		if AdvisorOpt.isUHVFinishDateNone():
			aHelp.append(getIcon(True) + localText.getText("TXT_KEY_VICTORY_GOAL_ACCOMPLISHED", ()))
		elif AdvisorOpt.isUHVFinishDateDate():
			aHelp.append(getIcon(True) + localText.getText("TXT_KEY_VICTORY_GOAL_ACCOMPLISHED_DATE", (sWinDate,)))
		else:
			aHelp.append(getIcon(True) + localText.getText("TXT_KEY_VICTORY_GOAL_ACCOMPLISHED_DATE_TURN", (sWinDate, iWinTurn - utils.getScenarioStartTurn())))
		if not AdvisorOpt.UHVProgressAfterFinish():
			return aHelp
	elif data.players[iPlayer].lGoals[iGoal] == 0:
		aHelp.append(getIcon(False) + localText.getText("TXT_KEY_VICTORY_GOAL_FAILED", ()))
		if not AdvisorOpt.UHVProgressAfterFinish():
			return aHelp

	if iPlayer == iEgypt:
		if iGoal == 0:
			iCulture = pEgypt.countTotalCulture()
			aHelp.append(getIcon(iCulture >= utils.getTurns(500)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(500))) + ' ' + getIcon(iCulture >= utils.getTurns(5000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(5000))))
		elif iGoal == 1:
			bPyramids = data.getWonderBuilder(iPyramids) == iEgypt
			bLibrary = data.getWonderBuilder(iGreatLibrary) == iEgypt
			bLighthouse = data.getWonderBuilder(iGreatLighthouse) == iEgypt
			aHelp.append(getIcon(bPyramids) + localText.getText("TXT_KEY_BUILDING_PYRAMIDS", ()) + getIcon(bLibrary) + localText.getText("TXT_KEY_BUILDING_GREAT_LIBRARY", ()) + getIcon(bLighthouse) + localText.getText("TXT_KEY_BUILDING_GREAT_LIGHTHOUSE", ()))
		elif iGoal == 2:
			bLevant = isControlled(iEgypt, utils.getPlotList(tSouthLevantTL, tSouthLevantBR))
			bNubia = isControlled(iEgypt, Areas.getNormalArea(iNubia))
			aHelp.append(getIcon(bNubia) + localText.getText("TXT_KEY_CIV_NUBIA_SHORT_DESC", ()) + ' ' + getIcon(bLevant) + localText.getText("TXT_KEY_VICTORY_SOUTH_LEVANT", ()))
		
	elif iPlayer == iHarappa:
		if iGoal == 1:
			iNumReservoirs = getNumBuildings(iHarappa, iReservoir)
			iNumGranaries = getNumBuildings(iHarappa, iGranary)
			iNumSmokehouses = getNumBuildings(iHarappa, iSmokehouse)
			aHelp.append(getIcon(iNumReservoirs >= 3) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("BUILDING_HARAPPAN_RESERVOIR", iNumReservoirs, 3)) + ' ' + getIcon(iNumGranaries >= 2) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_BUILDING_GRANARY", iNumGranaries, 2)) + ' ' + getIcon(iNumSmokehouses >= 2) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_BUILDING_SMOKEHOUSE", iNumSmokehouses, 2)))
		elif iGoal == 2:
			iNumPopulation = pHarappa.getTotalPopulation()
			aHelp.append(getIcon(iNumPopulation >= 30) + localText.getText("TXT_KEY_VICTORY_TOTAL_POPULATION", (iNumPopulation, 30)))
			
	elif iPlayer == iNorteChico:
		if iGoal == 0:
			capital = pNorteChico.getCapitalCity()
			iCulture = capital.getCulture(iNorteChico)
			iRequiredCulture = gc.getCultureLevelInfo(3).getSpeedThreshold(gc.getGame().getGameSpeedType())
			aHelp.append(getIcon(iCulture >= iRequiredCulture) + localText.getText("TXT_KEY_VICTORY_CAPITAL_CULTURE", (capital.getName(), iCulture, iRequiredCulture)))
			
		elif iGoal == 1:
			bWriting = data.lFirstDiscovered[iWriting] == iNorteChico
			bCalendar = data.lFirstDiscovered[iCalendar] == iNorteChico
			aHelp.append(getIcon(bWriting) + localText.getText("TXT_KEY_TECH_WRITING", ()) + ' ' + getIcon(bCalendar) + localText.getText("TXT_KEY_TECH_CALENDAR", ()))
			
		elif iGoal == 2:
			capital = pNorteChico.getCapitalCity()
			iPop = capital.getPopulation()
			iBuildings = capital.getNumBuildings()
			aHelp.append(getIcon(iPop >= 5) + localText.getText("TXT_KEY_VICTORY_CAPITAL_POPULATION", (capital.getName(), iPop, 5)) + ' ' + getIcon(iBuildings >= 5) + localText.getText("TXT_KEY_VICTORY_CAPITAL_BUILDINGS", (capital.getName(), iBuildings + 1, 6)))
			
	elif iPlayer == iBabylonia:
		if iGoal == 0:
			bConstruction = data.lFirstDiscovered[iConstruction] == iBabylonia
			bArithmetics = data.lFirstDiscovered[iArithmetics] == iBabylonia
			bWriting = data.lFirstDiscovered[iWriting] == iBabylonia
			bCalendar = data.lFirstDiscovered[iCalendar] == iBabylonia
			bContract = data.lFirstDiscovered[iContract] == iBabylonia
			aHelp.append(getIcon(bConstruction) + localText.getText("TXT_KEY_TECH_CONSTRUCTION", ()) + ' ' + getIcon(bArithmetics) + localText.getText("TXT_KEY_TECH_ARITHMETICS", ()) + ' ' + getIcon(bWriting) + localText.getText("TXT_KEY_TECH_WRITING", ()))
			aHelp.append(getIcon(bCalendar) + localText.getText("TXT_KEY_TECH_CALENDAR", ()) + ' ' + getIcon(bContract) + localText.getText("TXT_KEY_TECH_CONTRACT", ()))
		elif iGoal == 1:
			pBestPopCity = getBestCity(iBabylonia, (76, 40), cityPopulation)
			bBestPopCity = isBestCity(iBabylonia, (76, 40), cityPopulation)
			pBestCulCity = getBestCity(iBabylonia, (76, 40), cityCulture)
			bBestCulCity = isBestCity(iBabylonia, (76, 40), cityCulture)
			aHelp.append(getIcon(bBestPopCity) + localText.getText("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", (pBestPopCity.getName(),)) + ' ' + getIcon(bBestCulCity) + localText.getText("TXT_KEY_VICTORY_MOST_CULTURED_CITY", (pBestCulCity.getName(),)))
		elif iGoal == 2:
			bLevant = isCultureControlled(iBabylonia, utils.getPlotList(tLevantTL, tLevantBR))
			aHelp.append(getIcon(bLevant) + localText.getText("TXT_KEY_VICTORY_LEVANT", ()))
			
	elif iPlayer == iNubia:
		if iGoal == 0:
			bPyramids = isBuildingInCity((66, 31), iPyramids)
			bEgypt = isControlled(iNubia, Areas.getCoreArea(iMamluks, False))
			aHelp.append(getIcon(bPyramids) + localText.getText("TXT_KEY_BUILDING_PYRAMIDS", ()) + ' ' + getIcon(bEgypt) + localText.getText("TXT_KEY_CIV_EGYPT_SHORT_DESC", ()) + ' ' + getIcon(data.iNubiaEgyptYears >= 1000) + localText.getText("TXT_KEY_UHV_YEARS", (data.iNubiaEgyptYears, 1000)))
		elif iGoal == 1:
			iNumOrthodoxCathedrals = getNumBuildings(iNubia, iOrthodoxCathedral)
			iNumPleasedOrBetterChristians = countPlayersWithAttitudeInGroup(iNubia, AttitudeTypes.ATTITUDE_PLEASED, getReligionPlayers(dc.lChristianity))
			aHelp.append(getIcon(iNumOrthodoxCathedrals >= 2) + localText.getText("TXT_KEY_VICTORY_ORTHODOX_CATHEDRALS", (iNumOrthodoxCathedrals, 2)) + ' ' + getIcon(iNumPleasedOrBetterChristians >= 5) + localText.getText("TXT_KEY_VICTORY_PLEASED_OR_FRIENDLY_CHRISTIANS", (iNumPleasedOrBetterChristians, 5)))
		elif iGoal == 2:
			iBestIslamicCommerceOutput = getBestPlayer(iNubia, playerCommerceOutput, getReligionPlayers([iIslam]))
			GreatestAfricanCity = getBestCityInRegion(lAfrica, cityValue)[0]
			bGreatestAfricanCityIsSennar = cnm.getFoundName(GreatestAfricanCity.getOwner(), (GreatestAfricanCity.plot().getX(), GreatestAfricanCity.plot().getY())) == 'Sennar'
			aHelp.append(getIcon(iBestIslamicCommerceOutput == iNubia) + localText.getText("TXT_KEY_VICTORY_MOST_AFRICAN_COMMERCE_CIV", (str(gc.getPlayer(iBestIslamicCommerceOutput).getCivilizationShortDescriptionKey()),)) + ' ' + getIcon(bGreatestAfricanCityIsSennar) + localText.getText("TXT_KEY_VICTORY_GREATEST_AFRICAN_CITY", (str(GreatestAfricanCity.getName()),)))
			
	elif iPlayer == iChina:
		if iGoal == 0:
			iConfucianCounter = getNumBuildings(iChina, iConfucianCathedral)
			iTaoistCounter = getNumBuildings(iChina, iTaoistCathedral)
			aHelp.append(getIcon(iConfucianCounter >= 2) + localText.getText("TXT_KEY_VICTORY_NUM_CONFUCIAN_ACADEMIES", ("TXT_KEY_BUILDING_STRING", iConfucianCounter, 2)) + ' ' + getIcon(iTaoistCounter >= 2) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_BUILDING_TAOIST_CATHEDRAL", iTaoistCounter, 2)))
		elif iGoal == 1:
			bCompass = data.lFirstDiscovered[iCompass] == iChina
			bPaper = data.lFirstDiscovered[iPaper] == iChina
			bGunpowder = data.lFirstDiscovered[iGunpowder] == iChina
			bPrintingPress = data.lFirstDiscovered[iPrinting] == iChina
			aHelp.append(getIcon(bCompass) + localText.getText("TXT_KEY_TECH_COMPASS", ()) + ' ' + getIcon(bPaper) + localText.getText("TXT_KEY_TECH_PAPER", ()) + ' ' + getIcon(bGunpowder) + localText.getText("TXT_KEY_TECH_GUNPOWDER", ()) + ' ' + getIcon(bPrintingPress) + localText.getText("TXT_KEY_TECH_PRINTING", ()))
		elif iGoal == 2:
			iGoldenAgeTurns = data.iChineseGoldenAgeTurns
			aHelp.append(getIcon(iGoldenAgeTurns >= utils.getTurns(32)) + localText.getText("TXT_KEY_VICTORY_GOLDEN_AGES", (iGoldenAgeTurns / utils.getTurns(8), 4)))

	elif iPlayer == iGreece:
		if iGoal == 0:
			bMathematics = data.lFirstDiscovered[iMathematics] == iGreece
			bLiterature = data.lFirstDiscovered[iLiterature] == iGreece
			bAesthetics = data.lFirstDiscovered[iAesthetics] == iGreece
			bPhilosophy = data.lFirstDiscovered[iPhilosophy] == iGreece
			bMedicine = data.lFirstDiscovered[iMedicine] == iGreece
			aHelp.append(getIcon(bMathematics) + localText.getText("TXT_KEY_TECH_MATHEMATICS", ()) + ' ' + getIcon(bLiterature) + localText.getText("TXT_KEY_TECH_LITERATURE", ()) + ' ' + getIcon(bAesthetics) + localText.getText("TXT_KEY_TECH_AESTHETICS", ()))
			aHelp.append(getIcon(bPhilosophy) + localText.getText("TXT_KEY_TECH_PHILOSOPHY", ()) + ' ' + getIcon(bMedicine) + localText.getText("TXT_KEY_TECH_MEDICINE", ()))
		elif iGoal == 1:
			bEgypt = checkOwnedCiv(iGreece, iEgypt)
			bPhoenicia = checkOwnedCiv(iGreece, iCarthage)
			bBabylonia = checkOwnedCiv(iGreece, iBabylonia)
			bPersia = checkOwnedCiv(iGreece, iPersia)
			aHelp.append(getIcon(bEgypt) + localText.getText("TXT_KEY_CIV_EGYPT_SHORT_DESC", ()) + ' ' + getIcon(bPhoenicia) + localText.getText("TXT_KEY_CIV_PHOENICIA_SHORT_DESC", ()) + ' ' + getIcon(bBabylonia) + localText.getText("TXT_KEY_CIV_BABYLONIA_SHORT_DESC", ()) + ' ' + getIcon(bPersia) + localText.getText("TXT_KEY_CIV_PERSIA_SHORT_DESC", ()))
		elif iGoal == 2:
			bParthenon = (getNumBuildings(iGreece, iParthenon) > 0)
			bColossus = (getNumBuildings(iGreece, iColossus) > 0)
			bStatueOfZeus = (getNumBuildings(iGreece, iStatueOfZeus) > 0)
			bArtemis = (getNumBuildings(iGreece, iTempleOfArtemis) > 0)
			aHelp.append(getIcon(bParthenon) + localText.getText("TXT_KEY_BUILDING_PARTHENON", ()) + ' ' + getIcon(bColossus) + localText.getText("TXT_KEY_BUILDING_COLOSSUS", ()) + ' ' + getIcon(bStatueOfZeus) + localText.getText("TXT_KEY_BUILDING_STATUE_OF_ZEUS", ()) + ' ' + getIcon(bArtemis) + localText.getText("TXT_KEY_BUILDING_TEMPLE_OF_ARTEMIS", ()))

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
			aHelp.append(getIcon(popPercent >= 20.0) + localText.getText("TXT_KEY_VICTORY_PERCENTAGE_WORLD_POPULATION", (str(u"%.2f%%" % popPercent), str(25))))

	elif iPlayer == iOlmecs:
		if iGoal == 0:
			iCultureBuildingCount = 0
			for city in utils.getCityList(iOlmecs):
				iCultureBuildingCount += countCultureBuildings(city)
			iCultureBuildingCount += getNumBuildings(iOlmecs, utils.getUniqueBuilding(iOlmecs, iPaganTemple))
			aHelp.append(getIcon(iCultureBuildingCount >= 4) + localText.getText("TXT_KEY_VICTORY_CULTURE_BUILDINGS_BUILT", (iCultureBuildingCount, 4)))
		if iGoal == 1:
			bArithmetics = teamOlmecs.isHasTech(iArithmetics)
			bWriting = teamOlmecs.isHasTech(iWriting)
			bCalendar = teamOlmecs.isHasTech(iCalendar)
			aHelp.append(getIcon(bArithmetics) + localText.getText("TXT_KEY_TECH_ARITHMETICS", ()) + ' ' + getIcon(bWriting) + localText.getText("TXT_KEY_TECH_WRITING", ()) + ' ' + getIcon(bCalendar) + localText.getText("TXT_KEY_TECH_CALENDAR", ()))
		
	elif iPlayer == iCarthage:
		if iGoal == 0:
			bPalace = isBuildingInCity((58, 39), iPalace)
			bGreatCothon = isBuildingInCity((58, 39), iGreatCothon)
			aHelp.append(getIcon(bPalace) + localText.getText("TXT_KEY_BUILDING_PALACE", ()) + ' ' + getIcon(bGreatCothon) + localText.getText("TXT_KEY_BUILDING_GREAT_COTHON", ()))
		elif iGoal == 1:
			bItaly = isControlled(iCarthage, utils.getPlotList(Areas.tNormalArea[iItaly][0], Areas.tNormalArea[iItaly][1], [(62, 47), (63, 47), (63, 46)]))
			bIberia = isControlled(iCarthage, Areas.getNormalArea(iSpain, False))
			aHelp.append(getIcon(bItaly) + localText.getText("TXT_KEY_VICTORY_ITALY", ()) + ' ' + getIcon(bIberia) + localText.getText("TXT_KEY_VICTORY_IBERIA_CARTHAGE", ()))
		elif iGoal == 2:
			iTreasury = pCarthage.getGold()
			aHelp.append(getIcon(iTreasury >= utils.getTurns(5000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iTreasury, utils.getTurns(5000))))

	elif iPlayer == iCeltia:
		if iGoal == 0:
			aHelp.append(getIcon(isWon(iPlayer, 0)) + localText.getText("TXT_KEY_VICTORY_CAPITALS_RAZED", (data.iCeltiaRazedCapitals, 2)))
			
		if iGoal == 1:
			iGallia =  getNumCitiesInArea(iPlayer, utils.getPlotList(tFranceTL, Areas.tNormalArea[iFrance][1]))
			if gc.getMap().plot(56, 46).isCity() and gc.getMap().plot(56, 46).getPlotCity().getOwner() == iCeltia:
				iGallia += 1
			iGermania = getNumCitiesInArea(iPlayer, utils.getPlotList(tGermaniaTL, tGermaniaBR))
			iItalia = getNumCitiesInRegions(iPlayer, [rItaly])
			iIberia = getNumCitiesInRegions(iPlayer, [rIberia])
			iBritannia = getNumCitiesInRegions(iPlayer, [rBritain])
			bControlled = iGallia >= 3 and iGermania >= 3 and iItalia >= 1 and iIberia >= 1 and iBritannia >= 1
			
			aHelp.append(getIcon(bControlled) + localText.getText("TXT_KEY_VICTORY_CELTIA_CONTROL_GALLIA", (iGallia, 3)) + ' ' + localText.getText("TXT_KEY_VICTORY_CELTIA_CONTROL_GERMANIA", (iGermania, 3)) + ' ' + localText.getText("TXT_KEY_VICTORY_CELTIA_CONTROL_ITALIA", (iItalia, 1)) + ' ' + localText.getText("TXT_KEY_VICTORY_IBERIA", (iIberia, 1)) + ' ' + localText.getText("TXT_KEY_VICTORY_CELTIA_CONTROL_BRITANNIA", (iBritannia, 1)))

		if iGoal == 2:
			iBestCiv = getBestPlayer(iPlayer, playerTotalCulture)
			aHelp.append(getIcon(iBestCiv == iPlayer) + localText.getText("TXT_KEY_VICTORY_MOST_CULTURED_CIVILIZATION", (str(gc.getPlayer(iBestCiv).getCivilizationShortDescriptionKey()),)))

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
			iNumArenas = getNumBuildings(iRome, iArena)
			iNumForums = getNumBuildings(iRome, iForum)
			aHelp.append(getIcon(iNumBarracks >= 6) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_BUILDING_BARRACKS", iNumBarracks, 6)) + ' ' + getIcon(iNumAqueducts >= 5) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_BUILDING_AQUEDUCT", iNumAqueducts, 5)) + ' ' + getIcon(iNumArenas >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_BUILDING_ARENA", iNumArenas, 4)) + ' ' + getIcon(iNumForums >= 3) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_BUILDING_ROMAN_FORUM", iNumForums, 3)))
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
			bArchitecture = data.lFirstDiscovered[iArchitecture] == iRome
			bPolitics = data.lFirstDiscovered[iPolitics] == iRome
			bScholarship = data.lFirstDiscovered[iScholarship] == iRome
			bMachinery = data.lFirstDiscovered[iMachinery] == iRome
			bCivilService = data.lFirstDiscovered[iCivilService] == iRome
			aHelp.append(getIcon(bArchitecture) + localText.getText("TXT_KEY_TECH_ARCHITECTURE", ()) + ' ' + getIcon(bPolitics) + localText.getText("TXT_KEY_TECH_POLITICS", ()) + ' ' + getIcon(bScholarship) + localText.getText("TXT_KEY_TECH_SCHOLARSHIP", ()))
			aHelp.append(getIcon(bMachinery) + localText.getText("TXT_KEY_TECH_MACHINERY", ()) + ' ' + getIcon(bCivilService) + localText.getText("TXT_KEY_TECH_CIVIL_SERVICE", ()))

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
				iTradeGold = data.iColombianTradeGold
				aHelp.append(getIcon(iTradeGold >= utils.getTurns(3000)) + localText.getText("TXT_KEY_VICTORY_TRADE_GOLD_RESOURCES", (iTradeGold, utils.getTurns(3000))))

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
			iTradeGold = data.iTamilTradeGold / 100
			aHelp.append(getIcon(iTradeGold >= utils.getTurns(4000)) + localText.getText("TXT_KEY_VICTORY_TRADE_GOLD", (iTradeGold, utils.getTurns(4000))))

	elif iPlayer == iEthiopia:
		if iGoal == 0:
			iNumIncense = pEthiopia.getNumAvailableBonuses(iIncense)
			aHelp.append(getIcon(iNumIncense >= 3) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_INCENSE_RESOURCES", (iNumIncense, 3)))
		elif iGoal == 1:
			bConverted = data.bEthiopiaConverted
			iNumOrthodoxCathedrals = getNumBuildings(iEthiopia, iOrthodoxCathedral)
			iGreatProphets = countSpecialists(iEthiopia, iSpecialistGreatProphet)
			aHelp.append(getIcon(bConverted) + localText.getText("TXT_KEY_VICTORY_CONVERTED_TO_ORTHODOXY", ()))
			aHelp.append(getIcon(iNumOrthodoxCathedrals >= 1) + localText.getText("TXT_KEY_BUILDING_ORTHODOX_CATHEDRAL", ()))
			aHelp.append(getIcon(iGreatProphets >= 3) + localText.getText("TXT_KEY_VICTORY_GREAT_PROPHETS", (iGreatProphets, 3)))
		elif iGoal == 2:
			iOrthodoxCities = countRegionReligion(iOrthodoxy, lAfrica)
			iMuslimCities = countRegionReligion(iIslam, lAfrica)
			aHelp.append(getIcon(iOrthodoxCities > iMuslimCities) + localText.getText("TXT_KEY_VICTORY_ORTHODOX_CITIES", (iOrthodoxCities,)) + ' ' + localText.getText("TXT_KEY_VICTORY_MUSLIM_CITIES", (iMuslimCities,)))

	elif iPlayer == iVietnam:
		if iGoal == 0:
			iCulture = pVietnam.countTotalCulture()
			aHelp.append(getIcon(iCulture >= utils.getTurns(8000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(8000))))
		elif iGoal == 1:
			iGenerals = data.iVietnamGreatGenerals
			aHelp.append(getIcon(iGenerals >= 3) + localText.getText("TXT_KEY_VICTORY_GREAT_GENERALS", (iGenerals, 3)))
		elif iGoal == 2:
			bSouthAsia = isAreaOnlyCivs(tSouthAsiaTL, tSouthAsiaBR, lSouthAsianCivs)
			aHelp.append(getIcon(bSouthAsia) + localText.getText("TXT_KEY_VICTORY_NO_SOUTH_ASIAN_COLONIES", ()))

	elif iPlayer == iTeotihuacan:
		if iGoal == 0:
			iCulture = pTeotihuacan.countTotalCulture()
			aHelp.append(getIcon(iCulture >= utils.getTurns(500)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(500))))
		elif iGoal == 2: 
			iMesoamericaTiles, iTotalMesoamericaTiles = countControlledTiles(iTeotihuacan, tMesoamericaTL, tMesoamericaBR, False)
			percentMesoamerica = iMesoamericaTiles * 100.0 / iTotalMesoamericaTiles
			aHelp.append(getIcon(percentMesoamerica >= 99.5) + localText.getText("TXT_KEY_VICTORY_CONTROL_TEOTIHUACAN", (str(u"%.2f%%" % percentMesoamerica), str(100))))
	
	elif iPlayer == iInuit:
		if iGoal == 0:
			bKivalliq = False
			bNunavik = False
			bKalaallitNunaat = False
			bQikiqtaaluk = False
			
			for city in utils.getCityList(iPlayer):
				tCity = (city.getX(), city.getY())
				
				if (tCity in lKivalliq):
					bKivalliq = True
				
				if utils.isPlotInArea(tCity, tNunavikTL, tNunavikBR, tNunavikExceptions):
					bNunavik = True
					
				if utils.isPlotInArea(tCity, tKalaallitNunaatTL, tKalaallitNunaatBR, tKalaallitNunaatExceptions):
					bKalaallitNunaat = True
					
				if utils.isPlotInArea(tCity, tQikiqtaalukTL, tQikiqtaalukBR, tQikiqtaalukExceptions):
					bQikiqtaaluk = True
					
				if bKivalliq and bNunavik and bKalaallitNunaat and bQikiqtaaluk:
					break
					
			aHelp.append(getIcon(bKivalliq) + localText.getText("TXT_KEY_VICTORY_KIVALLIQ", ()) + ' ' + getIcon(bKalaallitNunaat) + localText.getText("TXT_KEY_VICTORY_KALAALLIT_NUNAAT", ()) + ' ' +  getIcon(bQikiqtaaluk) + localText.getText("TXT_KEY_VICTORY_QIKIQTAALUK", ()) + ' ' + getIcon(bNunavik) + localText.getText("TXT_KEY_VICTORY_NUNAVIK", ()))
			
		if iGoal == 1:
			iNumResources = 0
			for iBonus in range(iNumBonuses):
				iNumResources += countResources(iInuit, iBonus)
			
			aHelp.append(getIcon(iNumResources >= 25) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_VICTORY_RESOURCES", iNumResources, 25)))
			
		if iGoal == 2:
			iBestPlayerOwner = -1
			iBestScoreOwner = -1
			iBestPlayerWorker = -1
			iBestScoreWorker= -1
			
			for iLoopPlayer in range(iNumMajorPlayers):
				lNumWater = countControlledTerrain(iLoopPlayer, [iCoast, iOcean], True)
				if lNumWater[0] > iBestScoreOwner or (lNumWater[0] == iBestScoreOwner and iBestPlayerOwner == iPlayer):
					iBestScoreOwner = lNumWater[0]
					iBestPlayerOwner = iLoopPlayer
					
				if lNumWater[1] > iBestPlayerWorker or (lNumWater[1] == iBestScoreWorker and iBestPlayerWorker == iPlayer):
					iBestScoreWorker = lNumWater[1]
					iBestPlayerWorker = iLoopPlayer
					
			aHelp.append(getIcon(iBestPlayerOwner == iPlayer) + localText.getText("TXT_KEY_VICTORY_MOST_WATER_OWN_CIV", (gc.getPlayer(iBestPlayerOwner).getCivilizationShortDescription(0),)) + " (" + str(iBestScoreOwner) + ")" + ' ' + getIcon(iBestPlayerWorker == iLoopPlayer) + localText.getText("TXT_KEY_VICTORY_MOST_WATER_WORK_CIV", (gc.getPlayer(iBestPlayerWorker).getCivilizationShortDescription(0),)) + " (" + str(iBestScoreWorker) + ")")
			
	elif iPlayer == iMississippi:
		if iGoal == 0:
			bMississippiRiver = isCultureControlled(iMississippi, lMississippiRiver, True, True)
			bOhioRiver = isCultureControlled(iMississippi, lOhioRiver, True, True)
			bGreatLakes = isCultureControlled(iMississippi, lGreatLakes, True, True)
			
			aHelp.append(getIcon(bMississippiRiver) + localText.getText("TXT_KEY_VICTORY_MISSISSIPPI_RIVER", ()) + ' ' + getIcon(bOhioRiver) + localText.getText("TXT_KEY_VICTORY_OHIO_RIVER", ()) + ' ' + getIcon(bGreatLakes) + localText.getText("TXT_KEY_VICTORY_GREAT_LAKES", ()))
		elif iGoal == 1:
			bSerpentMound = data.getWonderBuilder(iSerpentMound) == iMississippi
			iNumEffigyMound = getNumBuildings(iPlayer, iEffigyMound)
			
			aHelp.append(getIcon(bSerpentMound) + localText.getText("TXT_KEY_BUILDING_SERPENT_MOUND", ()) + ' ' + getIcon(iNumEffigyMound >= 7) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_BUILDING_MISSISSIPPI_EFFIGY_MOUND", iNumEffigyMound, 7)))
			
		elif iGoal == 2:
			bPalace = cnm.getFoundName(iMississippi, (pMississippi.getCapitalCity().getX(), pMississippi.getCapitalCity().getY())) == "Cahokia"
			iNumMerchant = countCitySpecialists(iMississippi, (pMississippi.getCapitalCity().getX(), pMississippi.getCapitalCity().getY()), iSpecialistGreatMerchant) >= 2
			
			aHelp.append(getIcon(bPalace) + localText.getText("TXT_KEY_BUILDING_PALACE", ()) + ' ' + getIcon(iNumMerchant >= 2) + localText.getText("TXT_KEY_VICTORY_GREAT_MERCHANTS_IN_CITY", (pMississippi.getCapitalCity().getName(), iNumMerchant, 2)))
			
	elif iPlayer == iKorea:
		if iGoal == 0:
			bConfucianCathedral = (getNumBuildings(iKorea, iConfucianCathedral) > 0)
			bBuddhistCathedral = (getNumBuildings(iKorea, iBuddhistCathedral) > 0)
			aHelp.append(getIcon(bBuddhistCathedral) + localText.getText("TXT_KEY_BUILDING_BUDDHIST_CATHEDRAL", ()) + ' ' + getIcon(bConfucianCathedral) + localText.getText("TXT_KEY_BUILDING_CONFUCIAN_CATHEDRAL", ()))
		elif iGoal == 2:
			iNumSinks = data.iKoreanSinks
			aHelp.append(getIcon(iNumSinks >= 20) + localText.getText("TXT_KEY_VICTORY_ENEMY_SHIPS_SUNK", (iNumSinks, 20)))

	elif iPlayer == iTiwanaku:
		if iGoal == 0:
			bGateOfTheSun = data.getWonderBuilder(iGateOfTheSun) == iTiwanaku
			iGreatProphets = countCitySpecialists(iTiwanaku, (pTiwanaku.getCapitalCity().getX(), pTiwanaku.getCapitalCity().getY()), iSpecialistGreatProphet)
			aHelp.append(getIcon(bGateOfTheSun) + localText.getText("TXT_KEY_BUILDING_GATE_OF_THE_SUN", ()) + ' ' + getIcon(iGreatProphets >= 1) + localText.getText("TXT_KEY_VICTORY_GREAT_PROPHETS_SETTLED", (pTiwanaku.getCapitalCity().getName(), iGreatProphets, 1)))
			
		elif iGoal == 1:
			iRefined = countCitiesWithCultureLevel(iTiwanaku, 4)
			
			aHelp.append(getIcon(iRefined >= 2) + localText.getText("TXT_KEY_VICTORY_NUM_CITIES_REFINED_CULTURE", (iRefined, 2)))
			
		elif iGoal == 2:
			iGoldenAgeTurns = data.iTiwanakuGoldenAgeTurns
			aHelp.append(getIcon(iGoldenAgeTurns >= utils.getTurns(16)) + localText.getText("TXT_KEY_VICTORY_GOLDEN_AGES", (iGoldenAgeTurns / utils.getTurns(8), 2)))

	elif iPlayer == iWari:
		if iGoal == 0:
			bGold = pWari.getNumAvailableBonuses(iGold) >= 1
			bDye = pWari.getNumAvailableBonuses(iDye) >= 1
			bCotton = pWari.getNumAvailableBonuses(iCotton) >= 1
			bSheep = pWari.getNumAvailableBonuses(iSheep) >= 1
			iCulture = pWari.countTotalCulture()
			
			aHelp.append(getIcon(bGold) + localText.getText("TXT_KEY_BONUS_GOLD", ()) + ' ' + getIcon(bDye) + localText.getText("TXT_KEY_BONUS_DYE", ()) + ' ' + getIcon(bCotton) + localText.getText("TXT_KEY_BONUS_COTTON", ()) + ' ' + getIcon(bSheep) + localText.getText("TXT_KEY_BONUS_SHEEP", ()) + getIcon(iCulture >= utils.getTurns(500)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(500))))

		elif iGoal == 1:
			iNumBarracks = getNumBuildings(iWari, iBarracks)
			iNumColcas = getNumBuildings(iWari, iColcas)
			bRoute = True
			for city in utils.getCityList(iPlayer):
				if city.getX() == pWari.getCapitalCity().getX() and city.getY() == pWari.getCapitalCity().getY(): continue
				if not isConnectedByRoute(iWari, (pWari.getCapitalCity().getX(), pWari.getCapitalCity().getY()), [(city.getX(), city.getY())]):
					bRoute = False
					break
			
			aHelp.append(getIcon(iNumBarracks >= 3) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_BUILDING_BARRACKS", iNumBarracks, 3)) + ' ' + getIcon(iNumColcas >= 3) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_BUILDING_WARI_COLCAS", iNumColcas, 3)) + ' ' + getIcon(bRoute) + localText.getText("TXT_KEY_VICTORY_CONNECTED", ()))

		elif iGoal == 2:
			iDual = countCitiesWithCultureLevelAndSize(iWari, 3, 5)
			
			aHelp.append(getIcon(iDual >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_REFINED_7POP_CITIES", (iDual, 4)))

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
			iGlobalTechs = countFirstDiscovered(iJapan, iGlobal)
			iDigitalTechs = countFirstDiscovered(iJapan, iDigital)
			aHelp.append(getIcon(iGlobalTechs >= 8) + localText.getText("TXT_KEY_VICTORY_TECHS_FIRST_DISCOVERED", (gc.getEraInfo(iGlobal).getText(), iGlobalTechs, 8)) + ' ' + getIcon(iDigitalTechs >= 8) + localText.getText("TXT_KEY_VICTORY_TECHS_FIRST_DISCOVERED", (gc.getEraInfo(iDigital).getText(), iDigitalTechs, 8)))
			
	elif iPlayer == iVikings:
		if iGoal == 0:
			lEuroCivs = [iLoopPlayer for iLoopPlayer in lCivGroups[0] if tBirth[iLoopPlayer] < 1050 and iLoopPlayer != iPlayer]
			bEuropeanCore = isCoreControlled(iVikings, lEuroCivs)
			aHelp.append(getIcon(bEuropeanCore) + localText.getText("TXT_KEY_VICTORY_EUROPEAN_CORE", ()))
		elif iGoal == 2:
			iRaidGold = data.iVikingGold
			aHelp.append(getIcon(iRaidGold >= utils.getTurns(3000)) + localText.getText("TXT_KEY_VICTORY_ACQUIRED_GOLD", (iRaidGold, utils.getTurns(3000))))
			
	elif iPlayer == iTurks:
		if iGoal == 0:
			fLandPercent = getLandPercent(iTurks)
			iPillagedImprovements = data.iTurkicPillages
			aHelp.append(getIcon(fLandPercent >= 5.995) + localText.getText("TXT_KEY_VICTORY_PERCENTAGE_WORLD_TERRITORY", (str(u"%.2f%%" % fLandPercent), str(6))))
			aHelp.append(getIcon(iPillagedImprovements >= 20) + localText.getText("TXT_KEY_VICTORY_PILLAGED_IMPROVEMENTS", (iPillagedImprovements, 20)))
		elif iGoal == 1:
			bConnected = isConnectedByTradeRoute(iTurks, utils.getPlotList(tChinaTL, tChinaBR), lMediterraneanPorts)
			iSilkRouteCities = pTurks.countCorporations(iSilkRoute)
			aHelp.append(getIcon(bConnected) + localText.getText("TXT_KEY_VICTORY_SILK_ROUTE_CONNECTION", ()))
			aHelp.append(getIcon(iSilkRouteCities >= 10) + localText.getText("TXT_KEY_VICTORY_CITIES_WITH_SILK_ROUTE", (iSilkRouteCities, 10)))
		elif iGoal == 2:
			iCultureLevel = 3
			for tCapital in [data.tFirstTurkicCapital, data.tSecondTurkicCapital]:
				if tCapital:
					iCultureLevel += 1
					capitalPlot = utils.plot(tCapital)
					if capitalPlot.isCity():
						name = capitalPlot.getPlotCity().getName()
						ownName = cnm.getRenameName(iTurks, name)
						if ownName: name = ownName
						aHelp.append(getIcon(True) + name)
			
			if pTurks.getNumCities() > 0:
				capital = pTurks.getCapitalCity()
				iCulture = capital.getCulture(iTurks)
				iRequiredCulture = gc.getCultureLevelInfo(iCultureLevel).getSpeedThreshold(gc.getGame().getGameSpeedType())
			
				if (capital.getX(), capital.getY()) in [data.tFirstTurkicCapital, data.tSecondTurkicCapital]:
					aHelp.append(getIcon(False) + localText.getText("TXT_KEY_VICTORY_NO_NEW_CAPITAL", ()))
				else:
					aHelp.append(getIcon(iCulture >= iRequiredCulture) + localText.getText("TXT_KEY_VICTORY_CAPITAL_CULTURE", (capital.getName(), iCulture, iRequiredCulture)))

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
			aHelp.append(getIcon(fReligionPercent >= 30.0) + localText.getText("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", (gc.getReligionInfo(iIslam).getTextKey(), str(u"%.2f%%" % fReligionPercent), str(30))))

	elif iPlayer == iTibet:
		if iGoal == 0:
			iNumCities = pTibet.getNumCities()
			aHelp.append(getIcon(iNumCities >= 5) + localText.getText("TXT_KEY_VICTORY_CITIES_ACQUIRED", (iNumCities, 5)))
		elif iGoal == 1:
			fReligionPercent = gc.getGame().calculateReligionPercent(iBuddhism)
			aHelp.append(getIcon(fReligionPercent >= 25.0) + localText.getText("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", (gc.getReligionInfo(iBuddhism).getTextKey(), str(u"%.2f%%" % fReligionPercent), str(25))))
		elif iGoal == 2:
			iCounter = countCitySpecialists(iTibet, Areas.getCapital(iTibet), iSpecialistGreatProphet)
			aHelp.append(getIcon(iCounter >= 5) + localText.getText("TXT_KEY_VICTORY_GREAT_PROPHETS_SETTLED", ("Lhasa", iCounter, 5)))

	elif iPlayer == iIndonesia:
		if iGoal == 0:
			iHighestCiv = getBestPlayer(iIndonesia, playerRealPopulation)
			bHighest = (iHighestCiv == iIndonesia)
			aHelp.append(getIcon(bHighest) + localText.getText("TXT_KEY_VICTORY_HIGHEST_POPULATION_CIV", (gc.getPlayer(iHighestCiv).getCivilizationShortDescription(0),)))
		elif iGoal == 1:
			iCounter = countHappinessResources(iIndonesia)
			aHelp.append(getIcon(iCounter >= 10) + localText.getText("TXT_KEY_VICTORY_NUM_HAPPINESS_RESOURCES", (iCounter, 10)))
		elif iGoal == 2:
			iIslamicPop = getBestPlayer(iIndonesia, playerRealPopulation, getReligionPlayers([iIslam]))
			iNumCathedrals = 0
			
			for iReligion in range(iNumReligions):
				if getNumBuildings(iIndonesia, iJewishCathedral + 4 * iReligion) >= 1:
					iNumCathedrals += 1
					
			aHelp.append(getIcon(iIslamicPop == iIndonesia) + localText.getText("TXT_KEY_VICTORY_ISLAMIC_CIV_HIGHEST_POPULATION", (gc.getPlayer(iIslamicPop).getCivilizationShortDescription(0),)) + ' ' + getIcon(iNumCathedrals >= 3) + localText.getText("TXT_KEY_VICTORY_DIFFERENT_CATHEDRALS", (iNumCathedrals, 3)))

	elif iPlayer == iBurma:
		if iGoal == 0:
			bShwedagon = data.getWonderBuilder(iShwedagonPaya) == iBurma
			iTemples = getNumBuildings(iBurma, iBuddhistTemple)
			iMonasteries = getNumBuildings(iBurma, iBuddhistMonastery)
			aHelp.append(getIcon(bShwedagon) + localText.getText("TXT_KEY_BUILDING_SHWEDAGON_PAYA", ()) + ' ' + getIcon(iTemples >= 2) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_BUILDING_BUDDHIST_TEMPLE", iTemples, 2)) + ' ' + getIcon(iMonasteries >= 2) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_BUILDING_BUDDHIST_MONASTERY", iMonasteries, 2)))
		if iGoal == 1:
			iProphets = 0
			iScientists = 0
			iArtists = 0
			for city in utils.getCityList(iPlayer):
				iProphets += city.getFreeSpecialistCount(iSpecialistGreatProphet)
				iScientists += city.getFreeSpecialistCount(iSpecialistGreatScientist)
				iArtists += city.getFreeSpecialistCount(iSpecialistGreatArtist)
			iSpecialists = iProphets + iScientists + iArtists
			
			aHelp.append(getIcon(iProphets >= 1) + localText.getText("TXT_KEY_UNIT_GREAT_PROPHET", ()) + ' ' + getIcon(iScientists >= 1) + localText.getText("TXT_KEY_UNIT_GREAT_SCIENTIST", ()) + ' ' + getIcon(iArtists >= 1) + localText.getText("TXT_KEY_UNIT_GREAT_ARTIST", ()) + ' ' + getIcon(iSpecialists >= 5) + localText.getText("TXT_KEY_VICTORY_PROPHETS_SCIENTISTS_ARTISTS", (iSpecialists, 5)))
		if iGoal == 2:
			bIndochina = isControlled(iBurma, utils.getPlotList(tIndochinaTL, tIndochinaBR, tIndochinaExceptions))
			aHelp.append(getIcon(bIndochina) + localText.getText("TXT_KEY_VICTORY_INDOCHINA", ()))

	elif iPlayer == iKhazars:
		if iGoal == 0:
			aHelp.append(getIcon(isWon(iPlayer, 0)) + localText.getText("TXT_KEY_VICTORY_DIPLOMATIC_MISSIONS", (isWon(iPlayer, 0), 1)))
		if iGoal == 1:
			iHappiness = getReligionHappiness(iKhazars)
			iLeader, iPopulation = getLargestReligionPopulation(iJudaism)
			aHelp.append(getIcon(iHappiness >= 10) + localText.getText("TXT_KEY_VICTORY_RELIGION_HAPPINESS", (iHappiness, 10)) + ' ' + getIcon(iLeader == iPlayer) + localText.getText("TXT_KEY_VICTORY_JEWISH_POPULATION", (gc.getPlayer(iLeader).getCivilizationShortDescription(0),)) + " (" + str(iPopulation) + ")")
		if iGoal == 2:
			bConnected = isConnectedByLand(iKhazars, lDanube, lZaysan)
			aHelp.append(getIcon(bConnected) + localText.getText("TXT_KEY_VICTORY_DANUBE_TO_ZAYSAN", ()))
			
	elif iPlayer == iChad:
		if iGoal == 0:
			aHelp.append(getIcon(data.iChadDiplomacyMissions >= 1) + localText.getText("TXT_KEY_VICTORY_DIPLOMATIC_MISSIONS", (data.iChadDiplomacyMissions, 1)) + ' ' + getIcon(data.iChadTradeMissions >= 3) + localText.getText("TXT_KEY_VICTORY_TRADE_MISSIONS", (data.iChadTradeMissions, 3)))
		if iGoal == 1:
			aHelp.append(getIcon(data.iChadSlaves >= 5) + localText.getText("TXT_KEY_VICTORY_SLAVES_SOLD", (data.iChadSlaves, 5)) + ' ' + getIcon(data.iChadStrategicBonuses >= 10) + localText.getText("TXT_KEY_VICTORY_STRATEGIC_BONUSES_BOUGHT", (data.iChadStrategicBonuses, 10)))
		if iGoal == 2:
			lAfricaCivs = getCivsWithHoldingsInRegion(lAfrica)
			iBestAfricanHoldingArmy = getBestPlayer(iChad, playerArmyPower, lAfricaCivs)
			bCameroon = isControlled(iChad, utils.getPlotList(tCameroonTL, tCameroonBR))
			bNigeria = isControlled(iChad, utils.getPlotList(tNigeriaTL, tNigeriaBR))
			bLibya = isControlled(iChad, utils.getPlotList(tLibyaTL, tLibyaBR))
			aHelp.append(getIcon(iBestAfricanHoldingArmy == iChad) + localText.getText("TXT_KEY_VICTORY_STRONGEST_ARMY_AFRICA_HOLDINGS", (str(gc.getPlayer(iBestAfricanHoldingArmy).getCivilizationShortDescriptionKey()),)) + ' ' + getIcon(bLibya) + localText.getText("TXT_KEY_VICTORY_LIBYA", ()) + ' ' + getIcon(bNigeria) + localText.getText("TXT_KEY_VICTORY_NIGERIA", ()) + ' ' + getIcon(bCameroon) + localText.getText("TXT_KEY_VICTORY_CAMEROON", ()))
			
	elif iPlayer == iMoors:
		if iGoal == 0:
			iIberia = getNumConqueredCitiesInArea(iMoors, utils.getPlotList(tIberiaTL, tIberiaBR))
			iMaghreb = getNumCitiesInArea(iMoors, utils.getPlotList(tMaghrebTL, tMaghrebBR))
			iWestAfrica = getNumConqueredCitiesInArea(iMoors, utils.getPlotList(tWestAfricaTL, tWestAfricaBR))
			aHelp.append(getIcon(iMaghreb >= 3) + localText.getText("TXT_KEY_VICTORY_MAGHREB_MOORS", (iMaghreb, 3)) + ' ' + getIcon(iIberia >= 2) + localText.getText("TXT_KEY_VICTORY_IBERIA", (iIberia, 2)) + ' ' + getIcon(iWestAfrica >= 2) + localText.getText("TXT_KEY_VICTORY_WEST_AFRICA", (iWestAfrica, 2)))
		elif iGoal == 1:
			bMezquita = data.getWonderBuilder(iMezquita) == iMoors
			iCounter = 0
			iCounter += countCitySpecialists(iMoors, (51, 41), iSpecialistGreatProphet)
			iCounter += countCitySpecialists(iMoors, (51, 41), iSpecialistGreatScientist)
			iCounter += countCitySpecialists(iMoors, (51, 41), iSpecialistGreatEngineer)
			aHelp.append(getIcon(bMezquita) + localText.getText("TXT_KEY_BUILDING_LA_MEZQUITA", ()) + ' ' + getIcon(iCounter >= 4) + localText.getText("TXT_KEY_VICTORY_GREAT_PEOPLE_IN_CITY_MOORS", ("Cordoba", iCounter, 4)))
		elif iGoal == 2:
			iRaidGold = data.iMoorishGold
			aHelp.append(getIcon(iRaidGold >= utils.getTurns(3000)) + localText.getText("TXT_KEY_VICTORY_PIRACY", (iRaidGold, utils.getTurns(3000))))

	elif iPlayer == iSpain:
		if iGoal == 1:
			iNumGold = countResources(iSpain, iGold)
			iNumSilver = countResources(iSpain, iSilver)
			aHelp.append(getIcon(iNumGold + iNumSilver >= 10) + localText.getText("TXT_KEY_VICTORY_GOLD_SILVER_RESOURCES", (iNumGold + iNumSilver, 10)))
		elif iGoal == 2:
			fReligionPercent = gc.getGame().calculateReligionPercent(iCatholicism)
			bNoProtestants = not isStateReligionInArea(iProtestantism, tEuropeTL, tEuropeBR) and not isStateReligionInArea(iProtestantism, tEasternEuropeTL, tEasternEuropeBR)
			aHelp.append(getIcon(fReligionPercent >= 30.0) + localText.getText("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", (gc.getReligionInfo(iCatholicism).getTextKey(), str(u"%.2f%%" % fReligionPercent), str(30))) + ' ' + getIcon(bNoProtestants) + localText.getText("TXT_KEY_VICTORY_NO_PROTESTANTS", ()))

	elif iPlayer == iFrance:
		if iGoal == 0:
			iCulture = getCityCulture(iFrance, (55, 50))
			aHelp.append(getIcon(iCulture >= utils.getTurns(50000)) + localText.getText("TXT_KEY_VICTORY_CITY_CULTURE", ("Paris", iCulture, utils.getTurns(50000))))
		elif iGoal == 1:
			iEurope, iTotalEurope = countControlledTiles(iFrance, tEuropeTL, tEuropeBR, True)
			iEasternEurope, iTotalEasternEurope = countControlledTiles(iFrance, tEasternEuropeTL, tEasternEuropeBR, True)
			iNorthAmerica, iTotalNorthAmerica = countControlledTiles(iFrance, tNorthAmericaTL, tNorthAmericaBR, True)
			fEurope = (iEurope + iEasternEurope) * 100.0 / (iTotalEurope + iTotalEasternEurope)
			fNorthAmerica = iNorthAmerica * 100.0 / iTotalNorthAmerica
			aHelp.append(getIcon(fEurope >= 40.0) + localText.getText("TXT_KEY_VICTORY_EUROPEAN_TERRITORY", (str(u"%.2f%%" % fEurope), str(40))) + ' ' + getIcon(fNorthAmerica >= 40.0) + localText.getText("TXT_KEY_VICTORY_NORTH_AMERICAN_TERRITORY", (str(u"%.2f%%" % fNorthAmerica), str(40))))
		elif iGoal == 2:
			bNotreDame = data.getWonderBuilder(iNotreDame) == iFrance
			bVersailles = data.getWonderBuilder(iVersailles) == iFrance
			bLouvre = data.getWonderBuilder(iLouvre) == iFrance
			bEiffelTower = data.getWonderBuilder(iEiffelTower) == iFrance
			bMetropolitain = data.getWonderBuilder(iMetropolitain) == iFrance
			aHelp.append(getIcon(bNotreDame) + localText.getText("TXT_KEY_BUILDING_NOTRE_DAME", ()) + ' ' + getIcon(bVersailles) + localText.getText("TXT_KEY_BUILDING_VERSAILLES", ()) + ' ' + getIcon(bLouvre) + localText.getText("TXT_KEY_BUILDING_LOUVRE", ()))
			aHelp.append(getIcon(bEiffelTower) + localText.getText("TXT_KEY_BUILDING_EIFFEL_TOWER", ()) + ' ' + getIcon(bMetropolitain) + localText.getText("TXT_KEY_BUILDING_METROPOLITAIN", ()))

	elif iPlayer == iOman:
		if iGoal == 0:
			aHelp.append(getIcon(isPossible(iOman, 0)) + localText.getText("TXT_KEY_NEVER_LOST_A_CITY", ()))
		if iGoal == 1:
			aHelp.append(getIcon(data.iOmaniCities >= 4) + localText.getText("TXT_KEY_CITIES_CONQUERED", (data.iOmaniCities, 4)))
		if iGoal == 2:
			aHelp.append(getIcon(data.iOmaniTradeGold >= utils.getTurns(4000)) + localText.getText("TXT_KEY_VICTORY_ACQUIRED_GOLD", (data.iOmaniTradeGold, utils.getTurns(4000))))

	elif iPlayer == iYemen:
		if iGoal == 1:
			bMecca = controlsCity(iYemen, tMecca)
			aHelp.append(getIcon(bMecca) + localText.getText("TXT_KEY_VICTORY_CONTROLS_CITY", ("Mecca",)))
		if iGoal == 0:
			iLeader, iLeaderScore = getCapitalCultureBuildingsLeader()
			aHelp.append(getIcon(iLeader == iYemen) + localText.getText("TXT_KEY_VICTORY_MOST_CAPITAL_CULTURE_BUILDINGS_CIV", (gc.getPlayer(iLeader).getCivilizationShortDescription(0),)) + " (" + str(iLeaderScore) + ")")

	elif iPlayer == iKhmer:
		if iGoal == 0:
			iNumBuddhism = getNumBuildings(iKhmer, iBuddhistMonastery)
			iNumHinduism = getNumBuildings(iKhmer, iHinduMonastery)
			bWatPreahPisnulok = data.getWonderBuilder(iWatPreahPisnulok) == iKhmer
			aHelp.append(getIcon(iNumBuddhism >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_BUILDING_BUDDHIST_MONASTERY", iNumBuddhism, 4)) + ' ' + getIcon(iNumHinduism >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_BUILDING_HINDU_MONASTERY", iNumHinduism, 4)) + ' ' + getIcon(bWatPreahPisnulok) + localText.getText("TXT_KEY_BUILDING_WAT_PREAH_PISNULOK", ()))
		elif iGoal == 1:
			fPopPerCity = getAverageCitySize(iKhmer)
			aHelp.append(getIcon(fPopPerCity >= 12.0) + localText.getText("TXT_KEY_VICTORY_AVERAGE_CITY_POPULATION", (str(u"%.2f" % fPopPerCity), str(12))))
		elif iGoal == 2:
			iCulture = pKhmer.countTotalCulture()
			aHelp.append(getIcon(iCulture >= utils.getTurns(8000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(8000))))

	elif iPlayer == iMuisca:
		if iGoal == 1:
			aHelp.append(getIcon(data.iMuiscaTradeGold >= utils.getTurns(2000)) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_VICTORY_TRADE_GOLD_SPENT", data.iMuiscaTradeGold, utils.getTurns(2000))))
			
		elif iGoal == 0:
			iAveragePlayer = -1
			iAverageScore = -1
			iLoopScore = -1
			for iLoopPlayer in lCivBioNewWorld:
				iLoopScore = getAverageCitySize(iLoopPlayer)
				if iLoopScore > iAverageScore or (iLoopScore == iAverageScore and iAveragePlayer == iMuisca):
					iAveragePlayer = iLoopPlayer
					iAverageScore = iLoopScore
			
			aHelp.append(getIcon(iAveragePlayer == iMuisca) + localText.getText("TXT_KEY_VICTORY_HIGHEST_AVERAGE_POPULATION_NEW_WORLD", (gc.getPlayer(iAveragePlayer).getCivilizationShortDescription(0),)) + " (" + str(int(iAverageScore)) + ")")

		elif iGoal == 2:
			iCount = countControlledResourcesInRegions(lCivBioOldWorld, lSouthAmerica, [iGold, iSilver], iMine)
			aHelp.append(getIcon(iCount == 0) + localText.getText("TXT_KEY_VICTORY_NUM_STRING_SINGLE", (gc.getBonusInfo(iGold).getDescription(), iCount)))

	elif iPlayer == iEngland:
		if iGoal == 0:
			iNAmerica = getNumCitiesInRegions(iEngland, lNorthAmerica)
			iSCAmerica = getNumCitiesInRegions(iEngland, lSouthAmerica)
			iAfrica = getNumCitiesInRegions(iEngland, lAfrica)
			iAsia = getNumCitiesInRegions(iEngland, lAsia)
			iOceania = getNumCitiesInRegions(iEngland, lOceania)
			aHelp.append(getIcon(iNAmerica >= 5) + localText.getText("TXT_KEY_VICTORY_ENGLAND_CONTROL_NORTH_AMERICA", (iNAmerica, 5)) + ' ' + getIcon(iAsia >= 5) + localText.getText("TXT_KEY_VICTORY_ENGLAND_CONTROL_ASIA", (iAsia, 5)) + ' ' + getIcon(iAfrica >= 4) + localText.getText("TXT_KEY_VICTORY_ENGLAND_CONTROL_AFRICA", (iAfrica, 4)))
			aHelp.append(getIcon(iSCAmerica >= 3) + localText.getText("TXT_KEY_VICTORY_ENGLAND_CONTROL_SOUTH_AMERICA", (iSCAmerica, 3)))
			aHelp.append(getIcon(iOceania >= 3) + localText.getText("TXT_KEY_VICTORY_ENGLAND_CONTROL_OCEANIA", (iOceania, 3)))
		elif iGoal == 1:
			iEnglishNavy = 0
			iEnglishNavy += pEngland.getUnitClassCount(gc.getUnitInfo(iFrigate).getUnitClassType())
			iEnglishNavy += pEngland.getUnitClassCount(gc.getUnitInfo(iShipOfTheLine).getUnitClassType())
			iEnglishSinks = data.iEnglishSinks
			aHelp.append(getIcon(iEnglishNavy >= 25) + localText.getText("TXT_KEY_VICTORY_NAVY_SIZE", (iEnglishNavy, 25)) + ' ' + getIcon(iEnglishSinks >= 50) + localText.getText("TXT_KEY_VICTORY_ENEMY_SHIPS_SUNK", (iEnglishSinks, 50)))
		elif iGoal == 2:
			iRenaissanceTechs = countFirstDiscovered(iEngland, iRenaissance)
			iIndustrialTechs = countFirstDiscovered(iEngland, iIndustrial)
			aHelp.append(getIcon(iRenaissanceTechs >= 8) + localText.getText("TXT_KEY_VICTORY_TECHS_FIRST_DISCOVERED", (gc.getEraInfo(iRenaissance).getText(), iRenaissanceTechs, 8)) + ' ' + getIcon(iIndustrialTechs >= 8) + localText.getText("TXT_KEY_VICTORY_TECHS_FIRST_DISCOVERED", (gc.getEraInfo(iIndustrial).getText(), iIndustrialTechs, 8)))

	elif iPlayer == iHolyRome:
		if iGoal == 0:
			bSaintPeters = data.lHolyRomanShrines[0] or getNumBuildings(iHolyRome, iCatholicShrine) > 0
			bAnastasis = data.lHolyRomanShrines[1] or getNumBuildings(iHolyRome, iOrthodoxShrine) > 0
			bAllSaints = data.lHolyRomanShrines[2] or getNumBuildings(iHolyRome, iProtestantShrine) > 0
			aHelp.append(getIcon(bSaintPeters) + localText.getText("TXT_KEY_BUILDING_CATHOLIC_SHRINE", ()) + ' ' + getIcon(bAnastasis) + localText.getText("TXT_KEY_BUILDING_ORTHODOX_SHRINE", ()) + ' ' + getIcon(bAllSaints) + localText.getText("TXT_KEY_BUILDING_PROTESTANT_SHRINE", ()))
		elif iGoal == 1:
			iNumVassals = countVassals(iHolyRome, lCivGroups[0], iCatholicism)
			aHelp.append(getIcon(iNumVassals >= 3) + localText.getText("TXT_KEY_VICTORY_CATHOLIC_EUROPEAN_VASSALS", (iNumVassals, 3)))
		elif iGoal == 2:
			iGreatArtists = countCitySpecialists(iHolyRome, tVienna, iSpecialistGreatArtist)
			iGreatStatesmen = countCitySpecialists(iHolyRome, tVienna, iSpecialistGreatStatesman)
			iPleasedOrBetterEuropeans = countPlayersWithAttitudeInGroup(iHolyRome, AttitudeTypes.ATTITUDE_PLEASED, lCivGroups[0])
			aHelp.append(getIcon(iGreatArtists + iGreatStatesmen >= 10) + localText.getText("TXT_KEY_VICTORY_GREAT_ARTISTS_AND_STATESMEN_SETTLED", ('Vienna', iGreatArtists + iGreatStatesmen, 10)))
			aHelp.append(getIcon(iPleasedOrBetterEuropeans >= 8) + localText.getText("TXT_KEY_VICTORY_PLEASED_OR_FRIENDLY_EUROPEANS", (iPleasedOrBetterEuropeans, 8)))

	elif iPlayer == iKievanRus:
		# first goal: build the St. Sophia Cathedral and 1 Orthodox Cathedral by 1327 AD
		if iGoal == 0:
			iCathedral = getNumBuildings(iKievanRus, iOrthodoxCathedral)
			bSophia = data.getWonderBuilder(iSaintSophia) == iKievanRus
			aHelp.append(getIcon(bSophia) + localText.getText("TXT_KEY_BUILDING_SAINT_SOPHIA", ()) + ' ' + getIcon(iCathedral >= 1) + localText.getText("TXT_KEY_BUILDING_ORTHODOX_CATHEDRAL", ()))
			
		# second goal: control a continuous empire from the Barents Sea to the Mediterranean Sea
		if iGoal == 1:
			bContinuous = isConnectedByLand(iKievanRus, lMediterraneanCoast, lBarents)
			aHelp.append(getIcon(bContinuous) + localText.getText("TXT_KEY_VICTORY_BLACK_TO_BARENTS", ()))
			
		# third goal: Conduct two trade or diplomatic missions with the most prominent (top scoring) European civilization by 1327 AD
		if iGoal == 2:
			iMissions = data.iKievanRusMissions
			aHelp.append(getIcon(iMissions >= 2) + localText.getText("TXT_KEY_VICTORY_TRADE_OR_DIPLOMATIC_MISSIONS", (iMissions, 2)))

	elif iPlayer == iHungary:
		# Control 20% of Europe in 1301 AD
		if iGoal == 0:
			iEurope, iTotalEurope = countControlledTilesInRegions(iPlayer, [rIberia, rEurope, rItaly, rBalkans], False, True)
			fEurope = (iEurope) * 100.0 / (iTotalEurope)
			aHelp.append(getIcon(fEurope >= 19.995) + localText.getText("TXT_KEY_VICTORY_MAINLAND_EUROPEAN_TERRITORY", (str(u"%.2f%%" % fEurope), "?")))
			
		# Be the first to adopt Tolerance and have Friendly Relations with 5 Catholic Civs in 1867 AD
		if iGoal == 1:
			iCount = countPlayersWithAttitudeAndReligion(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY, iCatholicism, True)
			aHelp.append(getIcon(data.bHungaryTolerance) + localText.getText("TXT_KEY_CIVIC_TOLERANCE", ()) + '' + getIcon(iCount >= 5) + localText.getText("TXT_KEY_VICTORY_FRIENDLY_CATHOLICS", (iCount, 5)))
		# Win and attend the congress for two world wars
		if iGoal == 2:
			aHelp.append(getIcon(data.iHungaryGlobalWars >= 2) + localText.getText("TXT_KEY_VICTORY_GLOBAL_WARS", (data.iHungaryGlobalWars, 2)))

	elif iPlayer == iRussia:
		if iGoal == 0:
			iSiberia = getNumFoundedCitiesInArea(iRussia, utils.getPlotList(tSiberiaTL, tSiberiaBR))
			bSiberia = iSiberia >= 7 or utils.getScenario() == i1700AD
			siberiaText = localText.getText("TXT_KEY_VICTORY_RUSSIA_CONTROL_SIBERIA", (iSiberia, 7))
			if bSiberia: siberiaText = localText.getText("TXT_KEY_VICTORY_RUSSIA_CONTROL_SIBERIA_COMPLETE", ()) 
			bSiberianRailway = isConnectedByRailroad(iRussia, Areas.getCapital(iRussia), lSiberianCoast)
			aHelp.append(getIcon(bSiberia) + siberiaText + ' ' + getIcon(bSiberianRailway) + localText.getText("TXT_KEY_VICTORY_TRANSSIBERIAN_RAILWAY", ()))
		elif iGoal == 1:
			bManhattanProject = teamRussia.getProjectCount(iManhattanProject) > 0
			bApolloProgram = teamRussia.getProjectCount(iLunarLanding) > 0
			aHelp.append(getIcon(bManhattanProject) + localText.getText("TXT_KEY_PROJECT_MANHATTAN_PROJECT", ()) + ' ' + getIcon(bApolloProgram) + localText.getText("TXT_KEY_PROJECT_LUNAR_LANDING", ()))
		elif iGoal == 2:
			bCommunism = dc.isCommunist(iPlayer)
			iCount = countPlayersWithAttitudeAndCriteria(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY, dc.isCommunist)
			aHelp.append(getIcon(bCommunism) + localText.getText("TXT_KEY_VICTORY_COMMUNISM", ()) + ' ' + getIcon(iCount >= 5) + localText.getText("TXT_KEY_VICTORY_FRIENDLY_WITH_COMMUNISM", (iCount, 5)))

	elif iPlayer == iPhilippines:
		if iGoal == 0:
			iNumEmbassies = len(data.lPhilippineEmbassies)
			aHelp.append(getIcon(iNumEmbassies >= 7) + localText.getText("TXT_KEY_VICTORY_NUM_EMBASSIES", (iNumEmbassies, 7)))
		elif iGoal == 1:
			iCounter = countHappinessResources(iPhilippines)
			aHelp.append(getIcon(iCounter >= 8) + localText.getText("TXT_KEY_VICTORY_NUM_HAPPINESS_RESOURCES", (iCounter, 8)))
		elif iGoal == 2:
			iTreasury = pPhilippines.getGold()
			aHelp.append(getIcon(iTreasury >= utils.getTurns(5000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iTreasury, utils.getTurns(5000))))

	elif iPlayer == iChimu:
		if iGoal == 0:
			iNumKancha = getNumBuildings(iChimu, iKancha)
			aHelp.append(getIcon(iNumKancha >= 2) + localText.getText("TXT_KEY_VICTORY_NUM_STRING" , ("TXT_KEY_BUILDING_CHIMU_KANCHA", iNumKancha, 2)))
			
		if iGoal == 1:
			bInca = isControlledOrVassalized(iChimu, Areas.getCoreArea(iInca, True))
			aHelp.append(getIcon(bInca) + localText.getText("TXT_KEY_CIV_INCA_SHORT_DESC", ()))
			
		if iGoal == 2:
			iArtist = countCitySpecialists(iChimu, Areas.getCapital(iChimu), iSpecialistGreatArtist)
			aHelp.append(getIcon(iArtist >= 3) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_SPECIALIST_GREAT_ARTIST", iArtist, 3)))

	elif iPlayer == iSwahili:
		if iGoal == 0:
			iTradeGold = data.iSwahiliTradeGold / 100
			aHelp.append(getIcon(iTradeGold >= utils.getTurns(4000)) + localText.getText("TXT_KEY_VICTORY_TRADE_GOLD", (iTradeGold, utils.getTurns(4000))))

	elif iPlayer == iMamluks:
		if iGoal == 0:
			bNorthAfrica = isCultureControlled(iMamluks, utils.getPlotList(tNorthAfricaTL, tNorthAfricaBR), True)
			bHejaz = isCultureControlled(iMamluks, utils.getPlotList(tHejazTL, tHejazBR, tHejazExceptions), True)
			bLevant = isCultureControlled(iMamluks, utils.getPlotList(tLevantTL, tLevantBR), True)
			bMesopotamia = isControlled(iMamluks, Areas.getCoreArea(iBabylonia, False))
			aHelp.append(getIcon(bNorthAfrica) + localText.getText("TXT_KEY_VICTORY_NORTH_AFRICA_MAM", ()) + ' ' + getIcon(bHejaz) + localText.getText("TXT_KEY_VICTORY_HEJAZ", ()) + ' ' + getIcon(bLevant) + localText.getText("TXT_KEY_VICTORY_LEVANT", ()) + ' ' + getIcon(bMesopotamia) + localText.getText("TXT_KEY_VICTORY_MESOPOTAMIA", ()))
		elif iGoal == 1:
			lLowerNile = [(x, y) for (x, y) in utils.getPlotList(tLowerNileTL, tLowerNileBR) if gc.getMap().plot(x, y).isRiver()]
			pBestCity = getBestCity(iMamluks, (69, 35), cityPopulation)
			bBestCity = isBestCity(iMamluks, (69, 35), cityPopulation)
			iPopCount = countPopulationInArea(iMamluks, lLowerNile)
			aHelp.append(getIcon(bBestCity) + localText.getText("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", (pBestCity.getName(),)) + ' ' + getIcon(iPopCount >= 30) + localText.getText("TXT_KEY_VICTORY_NILE_POPULATION", (iPopCount, 30)))
		elif iGoal == 2:
			iMostCultureOutputCiv = getBestPlayer(iMamluks, playerCultureOutput)
			iMostResearchOutputCiv = getBestPlayer(iMamluks, playerResearchOutput)
			aHelp.append(getIcon(iMostCultureOutputCiv == iMamluks) + localText.getText("TXT_KEY_VICTORY_HIGHEST_CULTURE_OUTPUT_CIV", (str(gc.getPlayer(iMostCultureOutputCiv).getCivilizationShortDescriptionKey()),)) + ' ' + getIcon(iMostResearchOutputCiv == iMamluks) + localText.getText("TXT_KEY_VICTORY_HIGHEST_RESEARCH_OUTPUT_CIV", (str(gc.getPlayer(iMostResearchOutputCiv).getCivilizationShortDescriptionKey()),)))

	elif iPlayer == iMali:
		if iGoal == 1:
			bSankore = False
			iProphets = 0
			for city in utils.getCityList(iMali):
				if city.isHasRealBuilding(iUniversityOfSankore):
					bSankore = True
					iProphets = city.getFreeSpecialistCount(iSpecialistGreatProphet)
					break
			aHelp.append(getIcon(bSankore) + localText.getText("TXT_KEY_BUILDING_UNIVERSITY_OF_SANKORE", ()) + ' ' + getIcon(iProphets >= 1) + localText.getText("TXT_KEY_VICTORY_SANKORE_PROPHETS", (iProphets, 1)))
		elif iGoal == 2:
			iTreasury = pMali.getGold()
			iThreshold = 7500
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

	elif iPlayer == iZimbabwe:
		if iGoal == 0:
			iNumCastles = getNumBuildings(iZimbabwe, iCastle)
			iNumKraals = getNumBuildings(iZimbabwe, iKraal)
			bGreatZimbabwe = data.getWonderBuilder(iGreatZimbabwe) == iZimbabwe
			aHelp.append(getIcon(iNumCastles >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_BUILDING_CASTLE", iNumCastles, 4)) + ' ' + getIcon(iNumKraals >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("TXT_KEY_BUILDING_ZIMBABWE_KRAAL", iNumKraals, 4)) + ' ' + getIcon(bGreatZimbabwe) + localText.getText("TXT_KEY_BUILDING_GREAT_ZIMBABWE", ()))
		elif iGoal == 1:
			lSubSaharanAfrica = utils.getPlotList(tSubSaharaTL, tSubSaharaBR, tSubSaharaExceptions)
			bGoldMonopoly = isMonopoly(iZimbabwe, iGold, lSubSaharanAfrica)
			bSilverMonopoly = isMonopoly(iZimbabwe, iSilver, lSubSaharanAfrica)
			bGemsMonopoly = isMonopoly(iZimbabwe, iGems, lSubSaharanAfrica)
			bIvoryMonopoly = isMonopoly(iZimbabwe, iIvory, lSubSaharanAfrica)
			aHelp.append(getIcon(bGoldMonopoly) + localText.getText("TXT_KEY_VICTORY_MONOPOLY", (gc.getBonusInfo(iGold).getDescription(),)) + ' ' + getIcon(bSilverMonopoly) + localText.getText("TXT_KEY_VICTORY_MONOPOLY", (gc.getBonusInfo(iSilver).getDescription(),)) + ' ' + getIcon(bGemsMonopoly) + localText.getText("TXT_KEY_VICTORY_MONOPOLY", (gc.getBonusInfo(iGems).getDescription(),)) + ' ' + getIcon(bIvoryMonopoly) + localText.getText("TXT_KEY_VICTORY_MONOPOLY", (gc.getBonusInfo(iIvory).getDescription(),)))
		elif iGoal == 2:
			bAfrica = isAreaFreeOfCivs(utils.getPlotList(tSubeqAfricaTL, tSubeqAfricaBR), lCivGroups[0])
			aHelp.append(getIcon(bAfrica) + localText.getText("TXT_KEY_VICTORY_NO_AFRICAN_COLONIES_CURRENT_ZIMBABWE", ()))

	elif iPlayer == iPortugal:
		if iGoal == 0:
			iCount = countOpenBorders(iPortugal)
			aHelp.append(getIcon(iCount >= 14) + localText.getText("TXT_KEY_VICTORY_OPEN_BORDERS", (iCount, 14)))
		elif iGoal == 1:
			iCount = countAcquiredResources(iPortugal, lColonialResources)
			aHelp.append(getIcon(iCount >= 12) + localText.getText("TXT_KEY_VICTORY_COLONIAL_RESOURCES", (iCount, 12)))
		elif iGoal == 2:
			iColonies = getNumCitiesInArea(iPortugal, utils.getPlotList(tBrazilTL, tBrazilBR))
			iColonies += getNumCitiesInRegions(iPortugal, lAfrica)
			iColonies += getNumCitiesInRegions(iPortugal, lAsia)
			aHelp.append(getIcon(iColonies >= 15) + localText.getText("TXT_KEY_VICTORY_EXTRA_EUROPEAN_COLONIES", (iColonies, 15)))

	elif iPlayer == iInca:
		if iGoal == 0:
			bRoad = isRoad(iInca, lAndeanCoast)
			iTambos = getNumBuildings(iInca, iTambo)
			aHelp.append(getIcon(bRoad) + localText.getText("TXT_KEY_VICTORY_ANDEAN_ROAD", ()) + ' ' + getIcon(iTambos >= 5) + localText.getText("TXT_KEY_VICTORY_STRING", ("TXT_KEY_BUILDING_INCAN_TAMBO", iTambos, 5)))
		elif iGoal == 1:
			iTreasury = pInca.getGold()
			aHelp.append(getIcon(iTreasury >= utils.getTurns(2500)) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iTreasury, utils.getTurns(2500))))
		elif iGoal == 2:
			bSouthAmerica = isAreaOnlyCivs(tSAmericaTL, tSAmericaBR, [iInca])
			aHelp.append(getIcon(bSouthAmerica) + localText.getText("TXT_KEY_VICTORY_NO_FOREIGN_CITIES_SOUTH_AMERICA", ()))

	elif iPlayer == iItaly:
		if iGoal == 0:
			bSanMarcoBasilica = data.getWonderBuilder(iSanMarcoBasilica) == iItaly
			bSistineChapel = data.getWonderBuilder(iSistineChapel) == iItaly
			bSantaMariaDelFiore = data.getWonderBuilder(iSantaMariaDelFiore) == iItaly
			aHelp.append(getIcon(bSanMarcoBasilica) + localText.getText("TXT_KEY_BUILDING_SAN_MARCO_BASILICA", ()) + ' ' + getIcon(bSistineChapel) + localText.getText("TXT_KEY_BUILDING_SISTINE_CHAPEL", ()) + ' ' + getIcon(bSantaMariaDelFiore) + localText.getText("TXT_KEY_BUILDING_SANTA_MARIA_DEL_FIORE", ()))
		elif iGoal == 1:
			iCount = countCitiesWithCultureLevel(iItaly, 5)
			aHelp.append(getIcon(iCount >= 3) + localText.getText("TXT_KEY_VICTORY_NUM_CITIES_INFLUENTIAL_CULTURE", (iCount, 3)))
		elif iGoal == 2:
			iMediterranean, iTotalMediterranean = countControlledTiles(iItaly, tMediterraneanTL, tMediterraneanBR, False, tMediterraneanExceptions, True)
			fMediterranean = iMediterranean * 100.0 / iTotalMediterranean
			aHelp.append(getIcon(fMediterranean >= 65.0) + localText.getText("TXT_KEY_VICTORY_MEDITERRANEAN_TERRITORY", (str(u"%.2f%%" % fMediterranean), str(65))))

	elif iPlayer == iNigeria:
		if iGoal == 0:
			lAfricaCivs = [iLoopPlayer for iLoopPlayer in range(iNumPlayers) if gc.getPlayer(iLoopPlayer).getCapitalCity().getRegionID() in lAfrica]
			iLargestArmy = getBestPlayer(iNigeria, playerArmySize, lAfricaCivs)
			aHelp.append(getIcon(iLargestArmy == iNigeria) + localText.getText("TXT_KEY_VICTORY_LARGEST_ARMY_AFRICA", (str(gc.getPlayer(iLargestArmy).getCivilizationShortDescriptionKey()),)))
		elif iGoal == 1:
			iTradeGold = data.iNigeriaTradeGold
			aHelp.append(getIcon(iTradeGold >= utils.getTurns(2000)) + localText.getText("TXT_KEY_VICTORY_TRADE_GOLD_RESOURCES", (iTradeGold, utils.getTurns(2000))))
		elif iGoal == 2:
			bMovies = pNigeria.getNumAvailableBonuses(iMovies) >= 1
			bOilIndustry = pNigeria.countCorporations(iOilIndustry) >= 1
			aHelp.append(getIcon(bMovies) + gc.getBonusInfo(iMovies).getDescription() + ' ' + getIcon(bOilIndustry) + gc.getCorporationInfo(iOilIndustry).getDescription())

	elif iPlayer == iMongolia:
		if iGoal == 1:
			iRazedCities = data.iMongolRazes
			aHelp.append(getIcon(iRazedCities >= 7) + localText.getText("TXT_KEY_VICTORY_NUM_CITIES_RAZED", (iRazedCities, 7)))
		elif iGoal == 2:
			landPercent = getLandPercent(iMongolia)
			aHelp.append(getIcon(landPercent >= 11.995) + localText.getText("TXT_KEY_VICTORY_PERCENTAGE_WORLD_TERRITORY", (str(u"%.2f%%" % landPercent), str(12))))

	elif iPlayer == iMughals:
		if iGoal == 0:
			iNumMosques = getNumBuildings(iMughals, iIslamicCathedral)
			aHelp.append(getIcon(iNumMosques >= 3) + localText.getText("TXT_KEY_VICTORY_MOSQUES_BUILT", (iNumMosques, 3)))
		elif iGoal == 1:
			bRedFort = data.getWonderBuilder(iRedFort) == iMughals
			bShalimarGardens = data.getWonderBuilder(iShalimarGardens) == iMughals
			bTajMahal = data.getWonderBuilder(iTajMahal) == iMughals
			aHelp.append(getIcon(bRedFort) + localText.getText("TXT_KEY_BUILDING_RED_FORT", ()) + ' ' + getIcon(bShalimarGardens) + localText.getText("TXT_KEY_BUILDING_SHALIMAR_GARDENS", ()) + ' ' + getIcon(bTajMahal) + localText.getText("TXT_KEY_BUILDING_TAJ_MAHAL", ()))
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
				iStepPyramids = getNumBuildings(iAztecs, utils.getUniqueBuilding(iAztecs, iPaganTemple))
				iAltars = getNumBuildings(iAztecs, iSacrificialAltar)
				aHelp.append(getIcon(iStepPyramids >= 6) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("BUILDING_TEOTL_STEP_PYRAMID", iStepPyramids, 6)) + " " + getIcon(iAltars >= 6) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", ("BUILDING_AZTEC_SACRIFICIAL_ALTAR", iAltars, 6)))
			elif iGoal == 2:
				iEnslavedUnits = data.iAztecSlaves
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
				iGenerals = data.iMexicanGreatGenerals
				aHelp.append(getIcon(iGenerals >= 3) + localText.getText("TXT_KEY_VICTORY_GREAT_GENERALS", (iGenerals, 3)))
			elif iGoal == 2:
				pBestCity = getBestCity(iAztecs, (18, 37), cityPopulation)
				bBestCity = isBestCity(iAztecs, (18, 37), cityPopulation)
				aHelp.append(getIcon(bBestCity) + localText.getText("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", (pBestCity.getName(),)))

	elif iPlayer == iOttomans:
		if iGoal == 0:
			capital = pOttomans.getCapitalCity()
			iCounter = countCityWonders(iOttomans, (capital.getX(), capital.getY()), False)
			aHelp.append(getIcon(iCounter >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_WONDERS_CAPITAL", (iCounter, 4)))
		elif iGoal == 1:
			bEasternMediterranean = isCultureControlled(iOttomans, lEasternMediterranean)
			bBlackSea = isCultureControlled(iOttomans, lBlackSea)
			bCairo = controlsCity(iOttomans, tCairo)
			bMecca = controlsCity(iOttomans, tMecca)
			bBaghdad = controlsCity(iOttomans, tBaghdad)
			bVienna = controlsCity(iOttomans, tVienna)
			aHelp.append(getIcon(bEasternMediterranean) + localText.getText("TXT_KEY_VICTORY_EASTERN_MEDITERRANEAN", ()) + ' ' + getIcon(bBlackSea) + localText.getText("TXT_KEY_VICTORY_BLACK_SEA", ()))
			aHelp.append(getIcon(bCairo) + localText.getText("TXT_KEY_VICTORY_CAIRO", ()) + ' ' + getIcon(bMecca) + localText.getText("TXT_KEY_VICTORY_MECCA", ()) + ' ' + getIcon(bBaghdad) + localText.getText("TXT_KEY_VICTORY_BAGHDAD", ()) + ' ' + getIcon(bVienna) + localText.getText("TXT_KEY_VICTORY_VIENNA", ()))
		elif iGoal == 2:
			iOttomanCulture = pOttomans.countTotalCulture()
			iEuropeanCulture = getTotalCulture(lCivGroups[0])
			aHelp.append(getIcon(iOttomanCulture > iEuropeanCulture) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iOttomanCulture, iEuropeanCulture)))

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
			iSlaves = data.iCongoSlaveCounter
			aHelp.append(getIcon(iSlaves >= utils.getTurns(1000)) + localText.getText("TXT_KEY_VICTORY_SLAVES_TRADED", (iSlaves, utils.getTurns(1000))))

	elif iPlayer == iSweden:
		if iGoal == 0:
			bSkagerrak = isCultureControlled(iSweden, lSkagerrak)
			bBalticSea = isCultureControlled(iSweden, lBalticSea)
			aHelp.append(getIcon(bSkagerrak) + localText.getText("TXT_KEY_UHV_SWE1_SKAGERRAK_HELP", ()) + ' ' + getIcon(bBalticSea) + localText.getText("TXT_KEY_UHV_SWE1_BALTIC_SEA_HELP", ()))
		elif iGoal == 1:
			iNumFur = pSweden.getNumAvailableBonuses(iFur)
			aHelp.append(getIcon(iNumFur >= 7) + localText.getText("TXT_KEY_UHV_SWE2_HELP", (iNumFur, 7)))
		elif iGoal == 2:
			iHappinessTurns = data.iSwedenHappinessTurns
			aHelp.append(getIcon(iHappinessTurns >= utils.getTurns(50)) + localText.getText("TXT_KEY_VICTORY_HAPPINESS_TURNS", (iHappinessTurns, utils.getTurns(50))))

	elif iPlayer == iNetherlands:
		if iGoal == 0:
			iMerchants = countCitySpecialists(iNetherlands, Areas.getCapital(iNetherlands), iSpecialistGreatMerchant)
			aHelp.append(getIcon(iMerchants >= 3) + localText.getText("TXT_KEY_VICTORY_GREAT_MERCHANTS_IN_CITY", ("Amsterdam", iMerchants, 3)))
		elif iGoal == 1:
			iColonies = data.iDutchColonies
			aHelp.append(getIcon(iColonies >= 4) + localText.getText("TXT_KEY_VICTORY_EUROPEAN_COLONIES_CONQUERED", (iColonies, 4)))
		elif iGoal == 2:
			iNumSpices = pNetherlands.getNumAvailableBonuses(iSpices)
			aHelp.append(getIcon(iNumSpices >= 7) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_SPICE_RESOURCES", (iNumSpices, 7)))

	elif iPlayer == iManchuria:
		if iGoal == 0:
			popPercent = getPopulationPercent(iManchuria)
			aHelp.append(getIcon(popPercent >= 20.0) + localText.getText("TXT_KEY_VICTORY_PERCENTAGE_WORLD_POPULATION", (str(u"%.2f%%" % popPercent), str(25))))
		elif iGoal == 1:
			iMostFoodCiv = getBestPlayer(iManchuria, playerFoodOutput)
			iMostProductionCiv = getBestPlayer(iManchuria, playerProductionOutput)
			iMostCommerceCiv = getBestPlayer(iManchuria, playerCommerceOutput)
			aHelp.append(getIcon(iMostFoodCiv == iManchuria) + localText.getText("TXT_KEY_VICTORY_MOST_FOOD_CIV", (str(gc.getPlayer(iMostFoodCiv).getCivilizationShortDescriptionKey()),)) + ' ' + getIcon(iMostProductionCiv == iManchuria) + localText.getText("TXT_KEY_VICTORY_MOST_PRODUCTION_CIV", (str(gc.getPlayer(iMostProductionCiv).getCivilizationShortDescriptionKey()),)) + ' ' + getIcon(iMostCommerceCiv == iManchuria) + localText.getText("TXT_KEY_VICTORY_MOST_COMMERCE_CIV", (str(gc.getPlayer(iMostCommerceCiv).getCivilizationShortDescriptionKey()),)))
		elif iGoal == 2:
			bAllIndustrialTechs = data.lFirstCompleted[iIndustrial] == iManchuria
			iGlobalTechs = countFirstDiscovered(iGermany, iGlobal)
			aHelp.append(getIcon(bAllIndustrialTechs) + localText.getText("TXT_KEY_VICTORY_ALL_ERA_TECHS", (gc.getEraInfo(iIndustrial).getText(),)) + ' ' + getIcon(iGlobalTechs >= 8) + localText.getText("TXT_KEY_VICTORY_TECHS_FIRST_DISCOVERED", (gc.getEraInfo(iGlobal).getText(), iGlobalTechs, 8)))

	elif iPlayer == iGermany:
		if iGoal == 0:
			iCounter = 0
			for iSpecialist in lGreatPeople:
				iCounter += countCitySpecialists(iPrussia, Areas.getCapital(iGermany), iSpecialist)
			aHelp.append(getIcon(iCounter >= 7) + localText.getText("TXT_KEY_VICTORY_GREAT_PEOPLE_IN_CITY", ("Berlin", iCounter, 7)))
		elif iGoal == 1:
			bFrance = checkOwnedCiv(iGermany, iFrance)
			bRome = checkOwnedCiv(iGermany, iItaly)
			bRussia = checkOwnedCiv(iGermany, iRussia)
			bEngland = checkOwnedCiv(iGermany, iEngland)
			bScandinavia = checkOwnedCiv(iGermany, iVikings)
			aHelp.append(getIcon(bRome) + localText.getText("TXT_KEY_CIV_ITALY_SHORT_DESC", ()) + ' ' + getIcon(bFrance) + localText.getText("TXT_KEY_CIV_FRANCE_SHORT_DESC", ()) + ' ' + getIcon(bScandinavia) + localText.getText("TXT_KEY_VICTORY_SCANDINAVIA", ()))
			aHelp.append(getIcon(bEngland) + localText.getText("TXT_KEY_CIV_ENGLAND_SHORT_DESC", ()) + ' ' + getIcon(bRussia) + localText.getText("TXT_KEY_CIV_RUSSIA_SHORT_DESC", ()))
		elif iGoal == 2:
			iIndustrialTechs = countFirstDiscovered(iGermany, iIndustrial)
			iGlobalTechs = countFirstDiscovered(iGermany, iGlobal)
			aHelp.append(getIcon(iIndustrialTechs >= 8) + localText.getText("TXT_KEY_VICTORY_TECHS_FIRST_DISCOVERED", (gc.getEraInfo(iIndustrial).getText(), iIndustrialTechs, 8)) + ' ' + getIcon(iGlobalTechs >= 8) + localText.getText("TXT_KEY_VICTORY_TECHS_FIRST_DISCOVERED", (gc.getEraInfo(iGlobal).getText(), iGlobalTechs, 8)))

	elif iPlayer == iAmerica:
		if iGoal == 0:
			bAmericas = isAreaFreeOfCivs(utils.getPlotList(tNCAmericaTL, tNCAmericaBR), lCivGroups[0])
			bMexico = isControlledOrVassalized(iAmerica, Areas.getCoreArea(iAztecs, True))
			aHelp.append(getIcon(bAmericas) + localText.getText("TXT_KEY_VICTORY_NO_NORTH_AMERICAN_COLONIES", ()) + ' ' + getIcon(bMexico) + localText.getText("TXT_KEY_CIV_MEXICO_SHORT_DESC", ()))
		elif iGoal == 1:
			bUnitedNations = data.getWonderBuilder(iUnitedNations) == iAmerica
			bBrooklynBridge = data.getWonderBuilder(iBrooklynBridge) == iAmerica
			bStatueOfLiberty = data.getWonderBuilder(iStatueOfLiberty) == iAmerica
			bGoldenGateBridge = data.getWonderBuilder(iGoldenGateBridge) == iAmerica
			bPentagon = data.getWonderBuilder(iPentagon) == iAmerica
			bEmpireState = data.getWonderBuilder(iEmpireStateBuilding) == iAmerica
			aHelp.append(getIcon(bStatueOfLiberty) + localText.getText("TXT_KEY_BUILDING_STATUE_OF_LIBERTY", ()) + ' ' + getIcon(bBrooklynBridge) + localText.getText("TXT_KEY_BUILDING_BROOKLYN_BRIDGE", ()) + ' ' + getIcon(bEmpireState) + localText.getText("TXT_KEY_BUILDING_EMPIRE_STATE_BUILDING", ()))
			aHelp.append(getIcon(bGoldenGateBridge) + localText.getText("TXT_KEY_BUILDING_GOLDEN_GATE_BRIDGE", ()) + ' ' + getIcon(bPentagon) + localText.getText("TXT_KEY_BUILDING_PENTAGON", ()) + ' ' + getIcon(bUnitedNations) + localText.getText("TXT_KEY_BUILDING_UNITED_NATIONS", ()))
		elif iGoal == 2:
			fAlliedCommercePercent = calculateAlliedCommercePercent(iAmerica)
			fAlliedPowerPercent = calculateAlliedPowerPercent(iAmerica)
			aHelp.append(getIcon(fAlliedCommercePercent >= 75.0) + localText.getText("TXT_KEY_VICTORY_ALLIED_COMMERCE_PERCENT", (str(u"%.2f%%" % fAlliedCommercePercent), str(75))))
			aHelp.append(getIcon(fAlliedPowerPercent >= 75.0) + localText.getText("TXT_KEY_VICTORY_ALLIED_POWER_PERCENT", (str(u"%.2f%%" % fAlliedPowerPercent), str(75))))

	elif iPlayer == iArgentina:
		if iGoal == 0:
			iGoldenAgeTurns = data.iArgentineGoldenAgeTurns
			aHelp.append(getIcon(iGoldenAgeTurns >= utils.getTurns(16)) + localText.getText("TXT_KEY_VICTORY_GOLDEN_AGES", (iGoldenAgeTurns / utils.getTurns(8), 2)))
		elif iGoal == 1:
			iCulture = getCityCulture(iArgentina, Areas.getCapital(iArgentina))
			aHelp.append(getIcon(iCulture >= utils.getTurns(50000)) + localText.getText("TXT_KEY_VICTORY_CITY_CULTURE", ("Buenos Aires", iCulture, utils.getTurns(50000))))
		elif iGoal == 2:
			iGoldenAgeTurns = data.iArgentineGoldenAgeTurns
			aHelp.append(getIcon(iGoldenAgeTurns >= utils.getTurns(48)) + localText.getText("TXT_KEY_VICTORY_GOLDEN_AGES", (iGoldenAgeTurns / utils.getTurns(8), 6)))

	elif iPlayer == iBrazil:
		if iGoal == 0:
			iSlavePlantations = countImprovements(iBrazil, iSlavePlantation)
			iPastures = countImprovements(iBrazil, iPasture)
			aHelp.append(getIcon(iSlavePlantations >= 8) + localText.getText("TXT_KEY_VICTORY_NUM_STRING", (gc.getImprovementInfo(iSlavePlantation).getText(), iSlavePlantations, 8)) + ' ' + getIcon(iPastures >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_IMPROVEMENTS", (gc.getImprovementInfo(iPasture).getText(), iPastures, 4)))
		elif iGoal == 1:
			bWembley = data.getWonderBuilder(iWembley) == iBrazil
			bCristoRedentor = data.getWonderBuilder(iCristoRedentor) == iBrazil
			bItaipuDam = data.getWonderBuilder(iItaipuDam) == iBrazil
			aHelp.append(getIcon(bWembley) + localText.getText("TXT_KEY_BUILDING_WEMBLEY", ()) + ' ' + getIcon(bCristoRedentor) + localText.getText("TXT_KEY_BUILDING_CRISTO_REDENTOR", ()) + ' ' + getIcon(bItaipuDam) + localText.getText("TXT_KEY_BUILDING_ITAIPU_DAM", ()))
		elif iGoal == 2:
			iForestPreserves = countImprovements(iBrazil, iForestPreserve)
			bNationalPark = False
			capital = pBrazil.getCapitalCity()
			if capital: bNationalPark = capital.isHasRealBuilding(iNationalPark)
			aHelp.append(getIcon(iForestPreserves >= 20) + localText.getText("TXT_KEY_VICTORY_NUM_IMPROVEMENTS", (gc.getImprovementInfo(iForestPreserve).getText(), iForestPreserves, 20)) + ' ' + getIcon(bNationalPark) + localText.getText("TXT_KEY_VICTORY_NATIONAL_PARK_CAPITAL", ()))

	elif iPlayer == iAustralia:
		if iGoal == 0:
			iAustraliaCities = getNumCitiesInArea(iAustralia, utils.getPlotList(tAustraliaTL, tAustraliaBR))
			iNewZealandCities = getNumCitiesInArea(iAustralia, utils.getPlotList(tNewZealandTL, tNewZealandBR))
			iGuineaCities = getNumCitiesInArea(iAustralia, utils.getPlotList(tNewGuineaTL, tNewGuineaBR))
			iPacificCities = getNumCitiesInArea(iAustralia, utils.getPlotList(tPacific1TL, tPacific1BR)) + getNumCitiesInArea(iAustralia, utils.getPlotList(tPacific2TL, tPacific2BR)) \
				+ getNumCitiesInArea(iAustralia, utils.getPlotList(tPacific3TL, tPacific3BR)) + getNumCitiesInArea(iAustralia, utils.getPlotList(tHawaiiTL, tHawaiiBR))
			aHelp.append(getIcon(iAustraliaCities >= 7) + localText.getText("TXT_KEY_VICTORY_AUSTRALIA_CONTROL_AUSTRALIA", (iAustraliaCities, 7)) + ' ' + getIcon(iNewZealandCities >= 2) + localText.getText("TXT_KEY_VICTORY_AUSTRALIA_CONTROL_NEW_ZEALAND", (iNewZealandCities, 2)) + ' ' + getIcon(iGuineaCities >= 1) + localText.getText("TXT_KEY_VICTORY_AUSTRALIA_CONTROL_GUINEA", (iGuineaCities, 1)) + ' ' + getIcon(iPacificCities >= 3) + localText.getText("TXT_KEY_VICTORY_AUSTRALIA_CONTROL_PACIFIC", (iPacificCities, 3)))
		elif iGoal == 1:
			iGifts = data.iAustraliaGifts
			iReceivers = len(data.lAustralianGiftReceivers)
			aHelp.append(getIcon(iGifts >= 10) + localText.getText("TXT_KEY_VICTORY_GIVEN_UNITS", (iGifts, 10)) + ' ' + getIcon(iReceivers >= 3) + localText.getText("TXT_KEY_VICTORY_UNIT_RECEIVERS", (iReceivers, 3)))
		elif iGoal == 2:
			iHappinessTurns = data.iAustraliaHappinessTurns
			aHelp.append(getIcon(iHappinessTurns >= utils.getTurns(25)) + localText.getText("TXT_KEY_VICTORY_HAPPINESS_TURNS", (iHappinessTurns, utils.getTurns(25))))

	elif iPlayer == iBoers:
		if iGoal == 0:
			bAfrica = isAreaFreeOfCivs(utils.getPlotList(tBoerAfricaTL, tBoerAfricaBR), lCivGroups[0])
			aHelp.append(getIcon(bAfrica) + localText.getText("TXT_KEY_VICTORY_NO_SOUTH_AFRICAN_COLONIES", ()))
		elif iGoal == 1:
			iCounter = countResources(iBoers, iGems)
			aHelp.append(getIcon(iCounter >= 5) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_GEMS_RESOURCES", (iCounter, 5)))

	elif iPlayer == iCanada:
		if iGoal == 0:
			capital = pCanada.getCapitalCity()
			bAtlantic = capital and isConnectedByRailroad(iCanada, (capital.getX(), capital.getY()), lAtlanticCoast)
			bPacific = capital and isConnectedByRailroad(iCanada, (capital.getX(), capital.getY()), lPacificCoast)
			aHelp.append(getIcon(bAtlantic) + localText.getText("TXT_KEY_VICTORY_ATLANTIC_RAILROAD", ()) + ' ' + getIcon(bPacific) + localText.getText("TXT_KEY_VICTORY_PACIFIC_RAILROAD", ()))
		elif iGoal == 1:
			iCanadaWest, iTotalCanadaWest = countControlledTiles(iCanada, tCanadaWestTL, tCanadaWestBR, True, tCanadaWestExceptions)
			iCanadaEast, iTotalCanadaEast = countControlledTiles(iCanada, tCanadaEastTL, tCanadaEastBR, True, tCanadaEastExceptions)
			fCanada = (iCanadaWest + iCanadaEast) * 100.0 / (iTotalCanadaWest + iTotalCanadaEast)
			bAllCities = controlsOrVassalizedAllCities(iCanada, tCanadaWestTL, tCanadaWestBR, tCanadaWestExceptions) and controlsOrVassalizedAllCities(iCanada, tCanadaEastTL, tCanadaEastBR, tCanadaEastExceptions)
			aHelp.append(getIcon(fCanada >= 90.0) + localText.getText("TXT_KEY_VICTORY_CONTROL_CANADA", (str(u"%.2f%%" % fCanada), str(90))) + ' ' + getIcon(bAllCities) + localText.getText("TXT_KEY_VICTORY_CONTROL_CANADA_CITIES", ()))
		elif iGoal == 2:
			iPeaceDeals = data.iCanadianPeaceDeals
			aHelp.append(getIcon(iPeaceDeals >= 12) + localText.getText("TXT_KEY_VICTORY_CANADIAN_PEACE_DEALS", (iPeaceDeals, 12)))
	
	elif iPlayer == iIsrael:
		if iGoal == 0:
			iIsraeliNuclearArsenal = pIsrael.getUnitClassCount(gc.getUnitInfo(iICBM).getUnitClassType())
			aHelp.append(getIcon(iIsraeliNuclearArsenal >= 1) + localText.getText("TXT_KEY_VICTORY_NUCLEAR_ARSENAL", (iIsraeliNuclearArsenal, 1)))
		elif iGoal == 1:
			x, y = 0, 0
			capital = pIsrael.getCapitalCity()
			if capital:
				x, y = capital.getX(), capital.getY()
			pBestCity = getBestCity(iPlayer, (x, y), cityResearchOutput)
			iResearchTurns = data.iIsraeliResearchTurns
			aHelp.append(getIcon(pBestCity.getOwner() == iPlayer) + localText.getText("TXT_KEY_VICTORY_MOST_RESEARCH_CITY", (pBestCity.getName(),)) + ' ' + getIcon(iResearchTurns >= 10) + localText.getText("TXT_KEY_VICTORY_MOST_RESEARCH_TURNS", (iResearchTurns, 10)))
		elif iGoal == 2:
			iSpies = pIsrael.getGreatSpiesCreated()
			aHelp.append(getIcon(iSpies >= 2) + localText.getText("TXT_KEY_VICTORY_GREAT_SPIES", (iSpies, 2)))
			
	return aHelp