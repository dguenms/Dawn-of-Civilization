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

def setup():
	global dResources
	dResources = TileDict(dResourcesDict, year)
	
	global dSpawnResources
	dSpawnResources = TileDict(dSpawnResourcesDict)
	
	global dRemovedResources
	dRemovedResources = TileDict(dRemovedResourcesDict, year)
	
	global dPlotTypes
	dPlotTypes = TileDict(dPlotTypesDict, year)
	
	global dFeatures
	dFeatures = TileDict(dFeaturesDict, year)
	
	for tile in lNewfoundlandCapes:
		dFeatures[tile] = (700, iCape)
	
	global dRemovedFeatures
	dRemovedFeatures = TileDict(dRemovedFeaturesDict, year)
	
	for tile in lNewfoundlandCapes:
		dRemovedFeatures[tile] = 1500


### Constants ###

# initialise bonuses variables

lSilkRoute = [(85,48), (86,49), (87,48), (88,47), (89,46), (90,47), (90,45), (91,47), (91,45), (92,48), (93,48), (93,46), (94,47), (95,47), (96,47), (97,47), (98,47), (99,46)]
lNewfoundlandCapes = [(34, 52), (34, 53), (34, 54), (35, 52), (36, 52), (35, 55), (35, 56), (35, 57), (36, 51), (36, 58), (36, 59)]

dResourcesDict = {
	(88, 37)  : (-1000, iHorse),   # Gujarat
	(78, 42)  : (-800,  iCopper),  # Assyria
	(88, 47)  : (-100,  iSilk),    # Silk Route
	(85, 46)  : (-100,  iSilk),    # Silk Route
	(108, 47) : (-50,   iPig),     # Hanseong
	(71, 34)  : (900,   iIron),    # Egypt
	(72, 24)  : (1100,  iSugar),   # East Africa
	(70, 17)  : (1100,  iSugar),   # Zimbabwe
	(67, 11)  : (1100,  iSugar),   # South Africa
	(66, 23)  : (1100,  iBanana),  # Central Africa
	(64, 20)  : (1100,  iBanana),  # Central Africa
	(57, 46)  : (1100,  iWine),    # Savoy
	(57, 45)  : (1100,  iClam),    # Savoy
	(50, 44)  : (1100,  iIron),    # Portugal
	(96, 36)  : (1250,  iFish),    # Bengal
	(56, 54)  : (1500,  iFish),    # Amsterdam
	(57, 52)  : (1500,  iWheat),   # Amsterdam
	(58, 52)  : (1500,  iCow),     # Amsterdam
	(29, 52)  : (1600,  iCow),     # Montreal
	(18, 53)  : (1600,  iCow),     # Alberta
	(12, 52)  : (1600,  iCow),     # British Columbia
	(28, 46)  : (1600,  iCow),     # Washington area
	(30, 49)  : (1600,  iCow),     # New York area
	(23, 42)  : (1600,  iCow),     # Jacksonville area
	(18, 46)  : (1600,  iCow),     # Colorado
	(20, 45)  : (1600,  iCow),     # Texas
	(37, 14)  : (1600,  iCow),     # Argentina
	(33, 11)  : (1600,  iCow),     # Argentina
	(35, 10)  : (1600,  iCow),     # Pampas
	(24, 43)  : (1600,  iCotton),  # near Florida
	(23, 45)  : (1600,  iCotton),  # Louisiana
	(22, 44)  : (1600,  iCotton),  # Louisiana
	(13, 45)  : (1600,  iCotton),  # California
	(26, 49)  : (1600,  iPig),     # Lakes
	(19, 51)  : (1600,  iSheep),   # Canadian border
	(19, 48)  : (1600,  iWheat),   # Midwest
	(20, 53)  : (1600,  iWheat),   # Manitoba
	(22, 33)  : (1600,  iBanana),  # Guatemala
	(27, 31)  : (1600,  iBanana),  # Colombia
	(43, 23)  : (1600,  iBanana),  # Brazil
	(39, 26)  : (1600,  iBanana),  # Brazil
	(49, 44)  : (1600,  iCorn),    # Galicia
	(54, 48)  : (1600,  iCorn),    # France
	(67, 47)  : (1600,  iCorn),    # Romania
	(106, 50) : (1600,  iCorn),    # Manchuria
	(77, 52)  : (1600,  iCorn),    # Caricyn
	(92, 35)  : (1600,  iSpices),  # Deccan
	(16, 54)  : (1700,  iHorse),   # Alberta
	(26, 45)  : (1700,  iHorse),   # Washington area
	(21, 48)  : (1700,  iHorse),   # Midwest
	(19, 45)  : (1700,  iHorse),   # Texas
	(40, 25)  : (1700,  iHorse),   # Brazil
	(33, 10)  : (1700,  iHorse),   # Buenos Aires area
	(32, 8)   : (1700,  iHorse),   # Pampas
	(30, 30)  : (1700,  iHorse),   # Venezuela
	(27, 36)  : (1700,  iSugar),   # Caribbean
	(39, 25)  : (1700,  iSugar),   # Brazil
	(37, 20)  : (1700,  iSugar),   # inner Brazil
	(29, 37)  : (1700,  iSugar),   # Hispaniola
	(104, 52) : (1700,  iCorn),    # Manchuria
	(89, 36)  : (1700,  iCorn),    # India
	(38, 18)  : (1700,  iCoffee),  # Brazil
	(39, 20)  : (1700,  iCoffee),  # Brazil
	(38, 22)  : (1700,  iCoffee),  # Brazil
	(27, 30)  : (1700,  iCoffee),  # Colombia
	(29, 30)  : (1700,  iCoffee),  # Colombia
	(26, 27)  : (1700,  iCoffee),  # Colombia
	(104, 25) : (1700,  iCoffee),  # Java
	(67, 44)  : (1700,  iTobacco), # Turkey
	(39, 16)  : (1700,  iFish),    # Brazil
	(70, 59)  : (1700,  iDeer),    # St Petersburg
	(12, 45)  : (1850,  iWine),    # California
	(31, 10)  : (1850,  iWine),    # Andes
	(113, 11) : (1850,  iWine),    # Barossa Valley
	(114, 11) : (1850,  iSheep),   # Australia
	(116, 13) : (1850,  iSheep),   # Australia
	(121, 6)  : (1850,  iSheep),   # New Zealand
	(58, 47)  : (1850,  iRice),    # Vercelli
	(12, 49)  : (1850,  iRice),    # California
	(11, 45)  : (1850,  iFish),    # California
	(87, 35)  : (1850,  iFish),    # Mumbai
	(115, 52) : (1850,  iCow),     # Hokkaido
	(1, 38)   : (1850,  iSugar),   # Hawaii
	(5, 36)   : (1850,  iBanana),  # Hawaii
	(108, 18) : (1850,  iCamel),   # Australia
}

# TODO: should be handled by Rise and Fall
# TODO: Rise and Fall needs generic function canSpawn for normal civs and rebirths
dSpawnResourcesDict = {
	(90, 28) : (iTamils,    iFish),
	(95, 43) : (iTibet,     iWheat),
	(97, 44) : (iTibet,     iHorse),
	(78, 51) : (iMongols,   iSilk),
	(61, 22) : (iCongo,     iCotton),
	(63, 19) : (iCongo,     iIvory),
	(61, 24) : (iCongo,     iIvory),
	(17, 41) : (iMexico,    iHorse),
	(16, 42) : (iMexico,    iIron),
	(28, 31) : (iColombia,  iIron),
	(31, 10) : (iArgentina, iWine),
	(31, 6)  : (iArgentina, iSheep),
	(32, 11) : (iArgentina, iIron),
	(36, 18) : (iBrazil,    iCorn),
	(42, 18) : (iBrazil,    iFish),
}

dRemovedResourcesDict = {
	(51, 36) : 550, # Ivory in Morocco
	(58, 37) : 550, # Ivory in Tunisia
}


dRoutes = appenddict({
	-200 : lSilkRoute,
	-100 : [(88, 47)],
})

dSpawnRoutes = {
	iMongols : [(101, 48), (100, 49), (100, 50), (99, 50)],
}

# there must be stuff like this elsewhere, maybe barbs?
dPlotTypesDict = {
	(88, 47) : (-100, PlotTypes.PLOT_HILLS),
}


dFeaturesDict = {
	(35, 54) : (700,  iMud),         # Newfoundland obstacles
	(92, 35) : (1600, iRainforest),  # Deccan
	(11, 46) : (1850, iFloodPlains), # California
	(11, 47) : (1850, iFloodPlains), # California
	(11, 48) : (1850, iFloodPlains), # California
}

dRemovedFeaturesDict = {
	(67, 30)  : 550,  # Sudan
	(67, 31)  : 550,  # Sudan
	(113, 25) : 1000, # allow settling New Guinea
	(102, 35) : 1350, # open up Vietnam
	(35, 54)  : 1500, # Newfoundland blocker
	(116, 24) : 1500, # Port Moresby
	(82, 47)  : 1600, # Transoxiana
	(83, 46)  : 1600, # Transoxiana
	(85, 49)  : 1600, # Transoxiana
}


@handler("BeginGameTurn")
def createResources():
	for (x, y), iResource in dResources[game.getGameTurn()]:
		createResource(x, y, iResource)


@handler("BeginGameTurn")
def createResourcesBeforeSpawn(iGameTurn):
	for iCiv in dSpawnResources:
		if iGameTurn == year(dBirth[iCiv]) - 1 and data.isCivEnabled(iCiv):
			for (x, y), iResource in dSpawnResources[iCiv]:
				createResource(x, y, iResource)


@handler("BeginGameTurn")
def removeResources():
	for x, y in dRemovedResources[game.getGameTurn()]:
		removeResource(x, y)


@handler("BeginGameTurn")
def createRoutes():
	for tile in dRoutes[game.getGameTurn()]:
		plot(tile).setRouteType(iRouteRoad)


@handler("BeginGameTurn")
def createRoutesBeforeSpawn(iGameTurn):
	for iCiv in dSpawnRoutes:
		if iGameTurn == year(dBirth[iCiv]) - 1 and data.isCivEnabled(iCiv):
			for tile in dSpawnRoutes[iCiv]:
				plot(tile).setRouteType(iRouteRoad)


@handler("BeginGameTurn")
def changePlotType():
	for tile, type in dPlotTypes[game.getGameTurn()]:
		plot(tile).setPlotType(type, True, True)


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
		city = closestCity(plot, iOwner, same_continent=not bWater, coastal_only=bWater)
		
		if iRemovedBonus >= 0:
			notifyResource(iOwner, city, iX, iY, iRemovedBonus, removeTextKey)
		
		if iBonus >= 0:
			notifyResource(iOwner, city, iX, iY, iBonus, createTextKey)


def notifyResource(iPlayer, city, iX, iY, iBonus, textKey):
	if not city: return
	
	if infos.bonus(iBonus).getTechReveal() == -1 or team(iPlayer).isHasTech(infos.bonus(iBonus).getTechReveal()):
		message(iPlayer, textKey, infos.bonus(iBonus).getText(), city.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.bonus(iBonus).getButton(), location=(iX, iY))


def removeResource(iX, iY):
	"""Removes a bonus resource and alerts the plot owner"""
	if plot(iX, iY).getBonusType(-1) == -1: return
	createResource(iX, iY, -1)