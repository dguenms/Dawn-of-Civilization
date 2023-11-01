# Rhye's and Fall of Civilization - Dynamic resources

from CvPythonExtensions import *
import CvUtil
import PyHelpers
from Core import *
from RFCUtils import * # edead
from StoredData import data

from Events import handler


@handler("GameStart")
def setupOnGameStart():
	setup()
	
@handler("OnLoad")
def setupOnLoad():
	setup()

@handler("PythonReloaded")
def setupOnPythonReloaded():
	setup()

def setup():
	global dResources
	dResources = TileDict(dResourcesDict, year)
	
	global dSpawnResources
	dSpawnResources = TileDict(dSpawnResourcesDict)
	
	global dRemovedResources
	dRemovedResources = TileDict(dRemovedResourcesDict, year)
	
	global dFeatures
	dFeatures = TileDict(dFeaturesDict, year)
	
	global dRemovedFeatures
	dRemovedFeatures = TileDict(dRemovedFeaturesDict, year)
	
	global dConquerorPlotTypes
	dConquerorPlotTypes = TileDict(dConquerorPlotTypesDict)
	

### Constants ###

# initialise bonuses variables

dResourcesDict = {
	(103, 42) : (-1000, iHorse),	# Gujarat
	(78, 44)  : (-600,  iCotton),	# Egypt
	(127, 44) : (-200,  iRice),     # South China
	(125, 46) : (-200,  iRice),     # South China
	(125, 45) : (-200,  iCitrus),   # South China
	(129, 47) : (-200,  iCitrus),   # South China
	(124, 46) : (-200,  iSilk),     # South China
	(124, 43) : (-200,  iSilk),     # South China
	(127, 42) : (-200,  iFish),     # South China
	(129, 45) : (-200,  iClam),     # South China
	(125, 41) : (-200,  iClam),     # South China
	(85, 51)  : (200,   iCitrus),   # Levant
	(83, 45)  : (200,   iCitrus),   # Levant
	(76, 44)  : (200,   iCitrus),   # Egypt
	(98, 58)  : (200,   iSilk),     # Transoxiana
	(99, 54)  : (200,   iSilk),     # Transoxiana
	(113, 45) : (200,   iSilk),     # Assam
	(90, 19)  : (400,   iBanana),   # Madagascar
	(90, 18)  : (400,   iSugar),	# Madagascar
	(99, 43)  : (400,   iCotton),   # Sindh
	(78, 56)  : (550,   iSilk),     # Thrace
	(92, 47)  : (600,   iCitrus),   # Persia
	(81, 30)  : (600,   iBanana),   # Central Africa
	(76, 27)  : (600,   iBanana),   # Central Africa
	(75, 31)  : (600,   iBanana),   # Central Africa
	(0, 43)   : (600,   iSugar),	# Hawaii
	(62, 48)  : (700,   iCitrus),   # Algeria
	(57, 46)  : (700,   iCitrus),   # Morocco
	(57, 48)  : (700,   iCitrus),   # Andalusia
	(59, 50)  : (700,   iCitrus),   # Andalusia
	(89, 46)  : (700,   iSugar),	# Mesopotamia
	(78, 41)  : (700,   iSugar),	# Egypt
	(113, 44) : (800,   iOpium),    # Bengal
	(82, 40)  : (900,   iIron),		# Egypt
	(73, 25)  : (1000,  iBanana),   # Congo
	(70, 30)  : (1000,  iBanana),   # Cameroon
	(62, 32)  : (1000,  iBanana),   # West Africa
	(116, 42) : (1000,  iOpium),    # Burma
	(117, 45) : (1000,  iOpium),    # Burma
	(83, 24)  : (1100,  iSugar),	# Nigeria
	(83, 19)  : (1100,  iSugar),	# Mozambique
	(92, 60)  : (1200,  iSilk),     # Volga Delta
	(121, 47) : (1200,  iOpium),    # Sichuan
	(52, 44)  : (1400,  iSugar),	# Madeira
	(112, 43) : (1400,  iCotton),   # Bengal
	(63, 65)  : (1500,  iCow),      # Netherlands
	(81, 18)  : (1500,  iCitrus),   # Mozambique
	(70, 48)  : (1500,  iCitrus),   # Sicily
	(28, 44)  : (1500,  iSugar),	# Cuba
	(31, 43)  : (1500,  iSugar),	# Hispaniola
	(28, 42)  : (1500,  iSugar),	# Jamaica
	(35, 42)  : (1500,  iSugar),	# Antilles
	(39, 34)  : (1550,  iSugar),	# Guianas
	(48, 27)  : (1550,  iSugar),	# Northern Brazil
	(43, 21)  : (1550,  iSugar),	# Southern Brazil
	(132, 44) : (1600,  iFish),     # Taiwan
	(29, 53)  : (1600,  iCow),      # Carolinas
	(32, 57)  : (1600,  iCow),      # New England
	(31, 61)  : (1600,  iCow),      # Ontario
	(40, 16)  : (1600,  iCow),      # Southern Brazil
	(44, 23)  : (1600,  iCow),      # Southern Brazil
	(33, 37)  : (1600,  iCow),      # Venezuela
	(24, 50)  : (1600,  iCow),      # Alabama
	(15, 46)  : (1600,  iCow),      # Mexico
	(37, 10)  : (1600,  iCow),      # Argentina
	(39, 11)  : (1600,  iCow),      # Argentina
	(16, 48)  : (1600,  iHorse),    # Mexico
	(28, 53)  : (1600,  iHorse),    # Carolinas
	(45, 30)  : (1600,  iHorse),    # Northern Brazil
	(44, 31)  : (1600,  iBanana),   # Northern Brazil
	(49, 29)  : (1600,  iBanana),   # Northern Brazil
	(43, 20)  : (1600,  iBanana),   # Southern Brazil
	(28, 35)  : (1600,  iBanana),   # Colombia
	(25, 37)  : (1600,  iBanana),   # Costa Rica
	(37, 41)  : (1600,  iCocoa),    # Antilles
	(96, 19)  : (1600,  iSugar),	# Mauritius
	(123, 24) : (1600,  iTea),		# Java
	(24, 57)  : (1650,  iPig),      # Midwest
	(29, 61)  : (1650,  iPig),      # Ontario
	(42, 25)  : (1650,  iSugar),	# Central Brazil
	(46, 30)  : (1650,  iCotton),   # Northern Brazil
	(47, 25)  : (1650,  iCocoa),    # Northern Brazil
	(18, 54)  : (1700,  iWheat),    # Nebraska
	(19, 62)  : (1700,  iWheat),    # Manitoba
	(15, 63)  : (1700,  iWheat),    # Alberta
	(20, 57)  : (1700,  iWheat),    # Iowa
	(37, 13)  : (1700,  iWheat),    # Argentina
	(126, 52) : (1700,  iCorn),     # China
	(104, 41) : (1700,  iCorn),     # Rajasthan
	(78, 57)  : (1700,  iCorn),     # Romania
	(60, 58)  : (1700,  iCorn),     # France
	(64, 32)  : (1700,  iCorn),     # West Africa
	(77, 16)  : (1700,  iCorn),     # South Africa
	(53, 66)  : (1700,  iPotato),   # Ireland
	(57, 63)  : (1700,  iPotato),   # England
	(17, 51)  : (1700,  iCow),      # Texas
	(18, 49)  : (1700,  iCow),      # Texas
	(16, 62)  : (1700,  iCow),      # Alberta
	(41, 23)  : (1700,  iCow),      # Central Brazil
	(36, 14)  : (1700,  iCow),      # Patagonia
	(32, 11)  : (1700,  iCow),      # Chile
	(40, 15)  : (1700,  iSheep),    # Uruguay
	(35, 6)   : (1700,  iSheep),    # Patagonia
	(18, 52)  : (1700,  iHorse),    # Comanche
	(20, 55)  : (1700,  iHorse),    # Missouri
	(15, 59)  : (1700,  iHorse),    # Wyoming
	(33, 35)  : (1700,  iHorse),    # Venezuela
	(37, 12)  : (1700,  iHorse),    # Argentina
	(81, 71)  : (1700,  iDeer),     # Ingria
	(79, 70)  : (1700,  iFish),     # Ingria
	(21, 40)  : (1700,  iBanana),   # Guatemala
	(33, 42)  : (1700,  iCoffee),   # Hispaniola
	(46, 25)  : (1700,  iCoffee),	# Eastern Brazil
	(46, 22)  : (1700,  iCoffee),   # Southern Brazil
	(43, 22)  : (1700,  iCoffee),   # Southern Brazil
	(42, 19)  : (1700,  iCoffee),   # Southern Brazil
	(43, 26)  : (1700,  iCoffee),   # Central Brazil
	(125, 24) : (1700,  iCoffee),   # Java
	(78, 55)  : (1700,  iTobacco),  # Thrace
	(103, 38) : (1700,  iTobacco),  # India
	(131, 44) : (1700,  iTea),      # Taiwan
	(87, 60)  : (1750,  iWheat),    # Ukraine
	(58, 66)  : (1750,  iPotato),   # England
	(60, 62)  : (1750,  iPotato),   # France
	(69, 64)  : (1750,  iPotato),   # Germany
	(74, 64)  : (1750,  iPotato),   # Poland
	(25, 51)  : (1750,  iCotton),	# Georgia
	(21, 50)  : (1750,  iCotton),	# Louisiana
	(22, 52)  : (1750,  iCotton),	# Mississippi
	(23, 51)  : (1750,  iCotton),	# Alabama
	(74, 12)  : (1750,  iWine),     # South Africa
	(41, 17)  : (1750,  iWine),     # Southern Brazil
	(128, 62) : (1800,  iCorn),     # Manchuria
	(80, 63)  : (1800,  iPotato),   # Belarus
	(87, 65)  : (1800,  iPotato),   # Russia
	(124, 51) : (1800,  iPotato),   # China
	(139, 11) : (1800,  iSheep),    # Australia
	(140, 13) : (1800,  iSheep),    # Australia
	(47, 22)  : (1800,  iCitrus),   # Southern Brazil
	(41, 18)  : (1800,  iCitrus),   # Southern Brazil
	(78, 16)  : (1800,  iCitrus),   # South Africa
	(80, 14)  : (1800,  iSugar),	# Natal
	(85, 25)  : (1800,  iSpices),   # Zanzibar (nutmeg)
	(37, 39)  : (1800,  iSpices),   # Grenada (nutmeg)
	(93, 27)  : (1800,  iSpices),   # Seychelles (cinnamon)
	(94, 18)  : (1800,  iSpices),   # Reunion (vanilla)
	(90, 21)  : (1800,  iSpices),   # Madagascar (vanilla)
	(88, 18)  : (1800,  iSpices),   # Madagascar (vanilla)
	(30, 32)  : (1800,  iCoffee),   # Colombia
	(32, 33)  : (1800,  iCoffee),   # Colombia
	(30, 38)  : (1800,  iCoffee),   # Colombia
	(10, 51)  : (1800,  iCotton),   # California
	(111, 43) : (1800,  iTea),      # West Bengal
	(149, 4)  : (1800,  iSheep),    # New Zealand
	(1, 8)    : (1800,  iSheep),    # New Zealand
	(8, 55)   : (1850,  iRice),     # California
	(137, 62) : (1850,  iCow),      # Hokkaido
	(8, 53)   : (1850,  iCow),      # California
	(142, 17) : (1850,  iCow),		# Queensland
	(8, 52)   : (1850,  iSheep),    # California
	(8, 54)   : (1850,  iCitrus),   # California
	(4, 41)   : (1850,  iCitrus),   # Hawaii
	(142, 11) : (1850,  iCitrus),   # Australia
	(9, 52)   : (1850,  iDates),    # California
	(10, 22)  : (1850,  iSpices),   # Tahiti (vanilla)
	(83, 27)  : (1850,  iCoffee),   # Kenya
	(81, 24)  : (1850,  iCoffee),   # Tanzania
	(58, 32)  : (1850,  iCocoa),    # Ivory Coast
	(61, 32)  : (1850,  iCocoa),    # Ghana
	(68, 32)  : (1850,  iCocoa),    # Nigeria
	(69, 29)  : (1850,  iCocoa),    # Cameroon
	(82, 20)  : (1850,  iTobacco),  # Malawi
	(122, 48) : (1850,  iTobacco),  # Sichuan
	(128, 61) : (1850,  iTobacco),  # Manchuria
	(105, 35) : (1850,  iTea),      # Tamil Nadu
	(109, 31) : (1850,  iTea),      # Sri Lanka
	(91, 54)  : (1850,  iTea),      # Azerbaijan
	(7, 55)   : (1850,  iWine),     # California
	(35, 13)  : (1850,  iWine),     # Argentina
	(33, 12)  : (1850,  iWine),     # Chile
	(138, 10) : (1850,  iWine),     # Australia
	(38, 33)  : (1850,  iGold),     # Guianas
	(9, 53)   : (1850,  iGold),     # California
	(7, 56)   : (1850,  iGold),     # California
	(10, 54)  : (1850,  iSilver),   # Nevada
	(16, 54)  : (1860,  iGold),     # Colorado
	(12, 60)  : (1860,  iSilver),   # Idaho
	(138, 9)  : (1900,  iWheat),    # Victoria
	(26, 49)  : (1900,  iCitrus),   # Florida
	(83, 29)  : (1900,  iTea),      # Kenya
	(71, 29)  : (1900,  iRubber),   # Cameroon
	(74, 29)  : (1900,  iRubber),   # Congo
	(74, 24)  : (1900,  iRubber),   # Congo
	(118, 36) : (1900,  iRubber),   # Malaysia
	(119, 33) : (1900,  iRubber),   # Thailand
	(125, 29) : (1900,  iRubber),   # Borneo
	(130, 30) : (1900,  iRubber),   # Sulawesi
	(131, 18) : (1900,  iCamel),	# Australia
}

dSpawnResourcesDict = {
	(82, 54)  : (iHittites,    iIron),
	(107, 61) : (iTurks,       iHorse),
	(113, 47) : (iTibet,       iWheat),
	(115, 49) : (iTibet,       iHorse),
	(55, 52)  : (iPortugal,    iIron),
	(61, 66)  : (iNetherlands, iFish),
	(15, 47)  : (iMexico,      iIron),
	(48, 21)  : (iBrazil,      iFish),
}

dRemovedResourcesDict = {
	(75, 51)  : -50, # Silver in Greece
	(77, 55)  : -50, # Gold in Macedonia
	(81, 44)  : -50, # Gems (turquoise) in Egypt
	(74, 44)  : 200, # Spices (silphium) in Cyrenaica
	(55, 53)  : 400, # Gold in Spain
	(59, 51)  : 400, # Silver in Spain
	(83, 47)  : 500, # Dye (murex) in Phoenicia
	(73, 46)  : 500, # Dye (murex) in Cyrenaica
	(68, 47)  : 500, # Dye (murex) in Tunisia
	(70, 50)  : 500, # Dye (murex) in Italy
	(61, 48)  : 500, # Dye (murex) in Algeria
	(58, 47)  : 500, # Dye (murex) in Morocco
	(66, 46)  : 550, # Ivory in Tunisia
	(58, 45)  : 550, # Ivory in Morocco
	(63, 94)  : 550, # Ivory in Persia
	(100, 50) : 1100, # Silver in Bactria
	(79, 39)  : 1200, # Cotton in Nubia
	(78, 56)  : 1300, # Silk in Thrace
	(75, 58)  : 1400, # Gold in Transylvania
	(32, 42)  : 1600, # Gold in Hispaniola
	(92, 60)  : 1600, # Silk in the Volga Delta
	(47, 24)  : 1650, # Dye (brazilwood) in Brazil
	(53, 66)  : 1850, # Potato in Ireland
}

dFeaturesDict = {
	(8, 55) : (1850, iFloodPlains), # California
	(8, 54) : (1850, iFloodPlains), # California
	(8, 53) : (1850, iFloodPlains), # California
	(9, 52) : (1850, iFloodPlains), # California
}

dRemovedFeaturesDict = {
	(69, 56)  : 400,  # Venice
	(80, 37)  : 550,  # Nubia
	(81, 39)  : 550,  # Nubia
	(81, 38)  : 550,  # Nubia
	(63, 65)  : 1500, # Netherlands
	(62, 64)  : 1500, # Netherlands
	(99, 59)  : 1600, # Transoxiana
	(98, 58)  : 1600, # Transoxiana
	(96, 56)  : 1600, # Transoxiana
	(97, 57)  : 1600, # Transoxiana
	(81, 70)  : 1700, # Ingria
	(80, 69)  : 1700, # Ingria
}

dConquerorPlotTypesDict = {
	(33, 25) : (iInca, PlotTypes.PLOT_HILLS),
	(36, 22) : (iInca, PlotTypes.PLOT_HILLS),
	(29, 29) : (iInca, PlotTypes.PLOT_HILLS),
	(33, 12) : (iInca, PlotTypes.PLOT_HILLS),
}


@handler("BeginGameTurn")
def createResources():
	for (x, y), iResource in dResources[game.getGameTurn()]:
		createResource(x, y, iResource)


@handler("prepareBirth")
def createResourcesBeforeBirth(iCiv):
	for (x, y), iResource in dSpawnResources[iCiv]:
		createResource(x, y, iResource)


@handler("playerDestroyed")
def removeResourcesOnCollapse(iPlayer):
	iCiv = civ(iPlayer)
	for (x, y), iResource in dSpawnResources[iCiv]:
		removeResource(x, y)


@handler("birth")
def removeColombianJungle(iPlayer):
	if civ(iPlayer) == iColombia:
		plot(28, 31).setFeatureType(-1, 0)


@handler("BeginGameTurn")
def removeResources():
	for x, y in dRemovedResources[game.getGameTurn()]:
		removeResource(x, y)


@handler("BeginGameTurn")
def createFeatures():
	for tile, iFeature in dFeatures[game.getGameTurn()]:
		plot(tile).setFeatureType(iFeature, 0)


@handler("BeginGameTurn")
def removeFeatures(iGameTurn):
	for tile in dRemovedFeatures[game.getGameTurn()]:
		plot(tile).setFeatureType(-1, 0)
		
	if iGameTurn == year(700) and player(iVikings).isHuman():
		plot(41, 58).setFeatureType(-1, 0)


@handler("conquerors")
def changeConquerorPlotTypes(iConquerorPlayer, iTargetPlayer):
	iTargetCiv = civ(iTargetPlayer)
	for tile, type in dConquerorPlotTypes[iTargetCiv]:
		plot(tile).setPlotType(type, True, True)


def setupScenarioResources():
	setup()
	iStartTurn = scenarioStartTurn()
	
	for iTurn, lResources in dResources:
		if iTurn <= iStartTurn:
			for (x, y), iResource in lResources:
				createResource(x, y, iResource)
	
	for iCiv, lResources in dSpawnResources:
		if year(dBirth[iCiv]) <= iStartTurn and any(iEnd >= iStartTurn for iStart, iEnd in dResurrections[iCiv]):
			for (x, y), iResource in lResources:
				createResource(x, y, iResource)
	
	for iTurn, lResources in dRemovedResources:
		if iTurn <= iStartTurn:
			for x, y in lResources:
				removeResource(x, y)
	
	for iTurn, lFeatures in dFeatures:
		if iTurn <= iStartTurn:
			for (x, y), iFeature in lFeatures:
				plot(x, y).setFeatureType(iFeature, 0)
	
	for iTurn, lFeatures in dRemovedFeatures:
		if iTurn <= iStartTurn:
			for x, y in lFeatures:
				plot(x, y).setFeatureType(-1, 0)
	
	if year(700) <= iStartTurn:
		plot(41, 58).setFeatureType(-1, 0)
				
	for iCiv, lPlots in dConquerorPlotTypes:
		if year(dFall[iCiv]) <= iStartTurn:
			for (x, y), iPlotType in lPlots:
				plot(x, y).setPlotType(iPlotType, True, True)
	

# Leoreth: bonus removal alerts by edead
def createResource(iX, iY, iBonus, createTextKey="TXT_KEY_MISC_DISCOVERED_NEW_RESOURCE", removeTextKey="TXT_KEY_MISC_EVENT_RESOURCE_EXHAUSTED"):
	"""Creates a bonus resource and alerts the plot owner"""
	plot = plot_(iX, iY)
	
	iRemovedBonus = plot.getBonusType(-1) # for alert
	
	if iRemovedBonus == iBonus:
		return
	
	plot.setBonusType(iBonus)
			
	if iBonus == -1:
		iImprovement = plot.getImprovementType()
		if iImprovement >= 0:
			if infos.improvement(iImprovement).isImprovementBonusTrade(iRemovedBonus):
				plot.setImprovementType(-1)
		
	iOwner = plot.getOwner()
	if iOwner >= 0: # only show alert to the tile owner
		bWater = plot.isWater()
		closest = closestCity(plot, iOwner, same_continent=not bWater, coastal_only=bWater)
		
		if iRemovedBonus >= 0:
			notifyResource(iOwner, closest, iX, iY, iRemovedBonus, removeTextKey)
		
		if iBonus >= 0:
			notifyResource(iOwner, closest, iX, iY, iBonus, createTextKey)


def notifyResource(iPlayer, city, iX, iY, iBonus, textKey):
	if not city: return
	if scenarioStart(): return
	
	if infos.bonus(iBonus).getTechReveal() == -1 or team(iPlayer).isHasTech(infos.bonus(iBonus).getTechReveal()):
		message(iPlayer, textKey, infos.bonus(iBonus).getText(), city.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.bonus(iBonus).getButton(), location=(iX, iY))


def removeResource(iX, iY):
	"""Removes a bonus resource and alerts the plot owner"""
	if plot(iX, iY).getBonusType(-1) == -1: return
	createResource(iX, iY, -1)