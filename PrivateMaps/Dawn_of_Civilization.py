from Core import *
from RFCUtils import *
from Parsers import *
from Scenarios import *
from CityNameManager import determineCapitalLocations

import SettlerMaps, WarMaps, RegionMap


lCustomMapOptions = [
	("Starting Date", ["3000 BC", "600 AD", "1700 AD"], "3000 BC"),
]

lMinorCivs = [iCelts, iNative, iIndependent, iIndependent2]


def getDescription():
	return "Dawn of Civilization"

def getNumCustomMapOptions():
	return len(lCustomMapOptions)

def getCustomMapOptionName(args):
	iOption = args[0]
	
	option_names = dict((i, name) for i, (name, _, _) in enumerate(lCustomMapOptions))
	option_name = option_names[iOption]
	return unicode(option_name)

def getNumCustomMapOptionValues(args):
	iOption = args[0]

	option_values = dict((i, len(options)) for i, (_, options, _) in enumerate(lCustomMapOptions))
	return option_values[iOption]

def getCustomMapOptionDescAt(args):
	iOption, iSelection = args
	
	selection_names = dict((i, dict((j, name) for j, name in enumerate(options))) for i, (_, options, _) in enumerate(lCustomMapOptions))
	selection_name = selection_names[iOption][iSelection]
	return unicode(selection_name)

def getCustomMapOptionDefault(args):
	iOption = args[0]
	
	option_defaults = dict((i, options.index(default)) for i, (_, options, default) in enumerate(lCustomMapOptions))
	return option_defaults[iOption]

def isRandomCustomMapOption(args):
	return 0

def isAdvancedMap():
	return 0

def prepareMap():
	global PARSER
	
	loadScenario()
	PARSER = parseScenarioMap(scenario)

def loadScenario():
	global scenario
	scenario = getScenario()

def getGridSize(args):
	if args[0] == -1:
		return []
	
	prepareMap()
	
	return PARSER.mapDesc.iGridW/4, PARSER.mapDesc.iGridH/4

def beforeGeneration():
	data.setup()
	determineCapitalLocations()
	PARSER.prepare()

def generateRandomMap():
	PARSER.applyPlotTypes()
	PARSER.applyTerrainTypes()

def addFeatures():
	PARSER.applyFeatures()

def addBonuses():
	PARSER.applyBonuses()

def addRivers():
	PARSER.applyRivers()

def addGoodies():
	return

def initRiseAndFall():
	SettlerMaps.init()
	WarMaps.init()
	RegionMap.init()
	
def afterGeneration():
	initRiseAndFall()
	scenario.init()
	PARSER.applyDevelopment()
	scenario.apply()
	
def findStartingPlot(args):
	iPlayer = args[0]
	startingPlot = is_minor(iPlayer) and plot(0, 0) or plots.capital(civ(iPlayer))
	
	return map.plotNum(startingPlot.getX(), startingPlot.getY())

def addLakes():
	return 0

def normalizeRemovePeaks():
	return 0

def normalizeRemoveBadFeatures():
	return 0

def normalizeRemoveBadTerrain():
	return 0
	
def normalizeAddFoodBonuses():
	return 0

def normalizeAddGoodTerrain():
	return 0

def startHumansOnSameTile():
	return 0
	
def normalizeStartingPlotLocations():
	return 0

def normalizeAddRiver():
	return 0

def normalizeAddLakes():
	return 0

def normalizeAddExtras():
	return 0

def isSeaLevelMap():
	return 0

def isClimateMap():
	return 0

