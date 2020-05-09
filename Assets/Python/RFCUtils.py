# Rhye's and Fall of Civilization - Utilities

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
from Consts import *
from StoredData import data
import BugCore
import SettlerMaps
import WarMaps
import CvScreenEnums

from Core import *
import Core as core

# globals
MainOpt = BugCore.game.MainInterface

tCol = (
'255,255,255',
'200,200,200',
'150,150,150',
'128,128,128'
)

lChineseCities = [(102, 47), (103, 44), (103, 43), (106, 44), (107, 43), (105, 39), (104, 39)]
# Beijing, Kaifeng, Luoyang, Shanghai, Hangzhou, Guangzhou, Haojing

bStabilityOverlay = False

# Leoreth - finds an adjacent land plot without enemy units that's closest to the player's capital (for the Roman UP)
# TODO: how is that closest to the capital
def findNearestLandPlot(tPlot, iPlayer):
	plot = plots.surrounding(tPlot).where(lambda p: not p.isWater() and not p.isPeak() and not p.isUnit()).random()
	if plot: return plot
	
	# if no plot is found, return that player's capital
	return plots.capital(iPlayer)

# only used in Plague
def isMortalUnit(unit):
	# great leaders
	if unit.getUpgradeDiscount() >= 100: return False
	
	# mechanical units
	if infos.unit(unit).isMechUnit(): return False
	
	# civilian units
	if not unit.canFight(): return False
	
	return True

# used: Plague, RiseAndFall
def isDefenderUnit(unit):
	pUnitInfo = infos.unit(unit)
	
	if not pUnitInfo: return False
	
	# Archery units with city defense
	if pUnitInfo.getUnitCombatType() == infos.type('UNITCOMBAT_ARCHER') and pUnitInfo.getCityDefenseModifier() > 0:
		return True
		
	# Melee units with mounted modifiers
	if pUnitInfo.getUnitCombatType() == infos.type('UNITCOMBAT_MELEE') and pUnitInfo.getUnitCombatModifier(infos.type('UNITCOMBAT_HEAVY_CAVALRY')) > 0:
		return True
		
	# Conscriptable gunpowder units
	if pUnitInfo.getUnitCombatType() == infos.type('UNITCOMBAT_GUN') and pUnitInfo.getConscriptionValue() > 1:
		return True
		
	return False

# other utils functions
def checkUnitsInEnemyTerritory(iPlayer1, iPlayer2):
	return units.owner(iPlayer1).any(lambda u: plot(u).getOwner() == iPlayer2)

# used: AIWars
def restorePeaceAI(iMinorCiv, bOpenBorders):
	teamMinor = team(iMinorCiv)
	for iPlayer in players.major().alive().ai():
		if team(iMinorCiv).isAtWar(player(iPlayer).getTeam()):
			bInvadingIndependents = checkUnitsInEnemyTerritory(iPlayer, iMinorCiv)
			bInvadedByIndependents = checkUnitsInEnemyTerritory(iMinorCiv, iPlayer)
			if not bInvadingIndependents and not bInvadedByIndependents:
				teamMinor.makePeace(iPlayer)
				if bOpenBorders:
					teamMinor.signOpenBorders(iPlayer)

# used: AIWars
def restorePeaceHuman(iMinorCiv, bOpenBorders): 
	teamMinor = team(iMinorCiv)
	iHuman = active()
	if player().isAlive():
		if teamMinor.isAtWar(iHuman):
			bInvadingIndependents = checkUnitsInEnemyTerritory(iHuman, iMinorCiv)
			bInvadedByIndependents = checkUnitsInEnemyTerritory(iMinorCiv, iHuman)
			if not bInvadingIndependents and not bInvadedByIndependents:
				teamMinor.makePeace(iHuman)

# used: AIWars
def minorWars(iMinorCiv):
	teamMinor = team(iMinorCiv)
	for city in cities.owner(iMinorCiv):
		x, y = location(city)
		for iPlayer in players.major().alive().ai():
			if player(iPlayer).getSettlerValue(x, y) >= 90 or player(iPlayer).getWarValue(x, y) >= 6:
				if not teamMinor.isAtWar(iPlayer):
					teamMinor.declareWar(iPlayer, False, WarPlanTypes.WARPLAN_LIMITED)

# used: RiseAndFall
def updateMinorTechs(iMinorCiv, iMajorCiv):
	for iTech in range(iNumTechs):
		if team(iMajorCiv).isHasTech(iTech):
				team(iMajorCiv).setHasTech(iTech, True, iMinorCiv, False, False)


# used: RFCUtils, RiseAndFall, UniquePowers
def flipUnitsInCityBefore(tCityPlot, iNewOwner, iOldOwner):
	plotUnits = units.at(tCityPlot).owner(iOldOwner)
	
	flippingUnits = plotUnits.where(lambda unit: not is_minor(unit) or (not unit.isAnimal() and not unit.isFound()))
	removedUnits = plotUnits.where(lambda unit: not unit.isCargo())
		
	data.lFlippingUnits = [unit.getUnitType() for unit in flippingUnits]
	
	for unit in removedUnits:
		unit.kill(False, -1)

# used: RFCUtils, RiseAndFall, UniquePowers
def flipUnitsInCityAfter(tCityPlot, iPlayer):
	for iUnitType in data.lFlippingUnits:
		makeUnit(iPlayer, iUnitType, tCityPlot)
		
	data.lFlippingUnits = []

# used: RiseAndFall
def killUnitsInArea(iPlayer, area):
	for plot in area:
		killedUnits = units.at(plot).owner(iPlayer)
		for unit in killedUnits:
			unit.kill(False, -1)

# used: RiseAndFall
# TODO: accept a Plots instance instead of lPlots
# TODO: lots of shared code with flipUnitsInCityBefore/After
def flipUnitsInArea(lPlots, iNewOwner, iOldOwner, bSkipPlotCity, bKillSettlers):
	"""Creates a list of all flipping units, deletes old ones and places new ones
	If bSkipPlotCity is True, units in a city won't flip. This is to avoid converting barbarian units that would capture a city before the flip delay"""
	for tPlot in lPlots:
		if bSkipPlotCity and plot(tPlot).isCity():
			continue
			
		removedUnits = units.at(tPlot).owner(iOldOwner)
			
		lFlippingUnits = []
		for unit in removedUnits:
			# Leoreth: Italy shouldn't flip so it doesn't get too strong by absorbing French or German armies attacking Rome
			if civ(iNewOwner) == iItaly and not is_minor(iOldOwner):
				oldCapital = player(iOldOwner).getCapitalCity()
				move(unit, oldCapital)
				continue
				
			unit.kill(False, iBarbarianPlayer)
				
			if unit.getDomainType() == DomainTypes.DOMAIN_SEA:
				continue
				
			if unit.workRate(True) > 0 and unit.baseCombatStr() > 0:
				continue
				
			if unit.isFound() and bKillSettlers:
				continue
				
			if unit.isAnimal():
				continue
				
			lFlippingUnits.append(unit.getUnitType())
			
		for iUnitType in lFlippingUnits:
			makeUnit(iNewOwner, iUnitType, tPlot)

# used: RFCUtils, RiseAndFall, UniquePowers
def flipCity(tCityPlot, bConquest, bKillUnits, iNewOwner, lOldOwners = []):
	"""Changes owner of city specified by tCityPlot.
	bConquest specifies if it's conquered or traded.
	If bKillUnits != 0 all the units in the city will be killed.
	lOldOwners is a list. Flip happens only if the old owner is in the list.
	An empty list will cause the flip to always happen."""
	pNewOwner = player(iNewOwner)
	x, y = location(tCityPlot)
	flipCity = city(x, y)
	
	if flipCity:
		iOldOwner = flipCity.getOwner()
		if not lOldOwners or iOldOwner in lOldOwners:
			
			if bKillUnits:
				for unit in units.at(x, y):
					unit.kill(False, iNewOwner)
					
			pNewOwner.acquireCity(flipCity, bConquest, not bConquest)
			
			flippedCity = city(x, y)
			flippedCity.setInfoDirty(True)
			flippedCity.setLayoutDirty(True)
			
			return flippedCity
			
	return None


# used: RFCUtils, RiseAndFall, UniquePowers
def cultureManager(tCityPlot, iCulturePercent, iNewOwner, iOldOwner, bBarbarian2x2Decay, bBarbarian2x2Conversion, bAlwaysOwnPlots):
	"""Converts the culture of the city and of the surrounding plots to the new owner of a city.
	iCulturePercent determine the percentage that goes to the new owner.
	If old owner is barbarian, all the culture is converted"""
	city = city_(tCityPlot)
	
	if city:
		iCulture = city.getCulture(iOldOwner)
		iConvertedCulture = iCulture * iCulturePercent / 100
		
		city.changeCulture(iOldOwner, -iConvertedCulture, False)
		city.changeCulture(iNewOwner, iConvertedCulture, False)
		
		if not player(iNewOwner).isBarbarian():
			city.setCulture(iBarbarianPlayer, 0, True)
			
	if bBarbarian2x2Decay or bBarbarian2x2Conversion:
		if not player(iNewOwner).isBarbarian() and not player(iNewOwner).isMinorCiv():
			for plot in plots.surrounding(tCityPlot, radius=2):
				if location(plot) == tCityPlot or not plot.isCity():
					for iMinor in players.minor().barbarian():
						iMinorCulture = plot.getCulture(iMinor)
						
						if bBarbarian2x2Decay:
							plot.setCulture(iMinor, iMinorCulture/4, True)
							
						if bBarbarian2x2Conversion:
							plot.setCulture(iMinor, 0, True)
							plot.changeCulture(iNewOwner, iMinorCulture, True)
							
	for plot in plots.surrounding(tCityPlot):
		iCulture = plot.getCulture(iOldOwner)
		iConvertedCulture = iCulture * iCulturePercent / 100
		
		if plot.isCity():
			plot.changeCulture(iNewOwner, iConvertedCulture, True)
			plot.changeCulture(iOldOwner, -iConvertedCulture, True)
		else:
			plot.changeCulture(iNewOwner, iConvertedCulture / 3, True)
			plot.changeCulture(iOldOwner, -iConvertedCulture / 3, True)
			
			if bAlwaysOwnPlots:
				plot.setOwner(iNewOwner)

# used: CvRFCEventHandler
def spreadMajorCulture(iMajorCiv, tPlot):
	for city in plots.surrounding(tPlot, radius=3).cities():
		if city.getOwner() in players.minor():
			iOwner = city.getOwner()
			
			iDenominator = 25
			if player(iMajorCiv).getSettlerValue(city.getX(), city.getY()) >= 400:
				iDenominator = 10
			elif player(iMajorCiv).getSettlerValue(city.getX(), city.getY()) >= 150:
				iDenominator = 15
				
			city.changeCulture(iMajorCiv, city.getCulture(city.getOwner()) / iDenominator, True)
			plot(city).changeCulture(iMajorCiv, plot(city).getCulture(city.getOwner()) / iDenominator, True)

# used: Congresses, RFCUtils, RiseAndFall, UniquePowers
def convertPlotCulture(tPlot, iPlayer, iPercent, bOwner):
	plot = plot_(tPlot)
	city = city_(tPlot)
	
	if city:
		iTotalConvertedCulture = 0
		for iLoopPlayer in players.all().without(iPlayer):
			iConvertedCulture = city.getCulture(iLoopPlayer) * iPercent / 100
			city.changeCulture(iLoopPlayer, -iConvertedCulture, True)
			iTotalConvertedCulture += iConvertedCulture
			
		city.changeCulture(iPlayer, iTotalConvertedCulture, True)
		
	iTotalConvertedCulture = 0
	for iLoopPlayer in players.all().without(iPlayer):
		iConvertedCulture = plot.getCulture(iLoopPlayer) * iPercent / 100
		plot.changeCulture(iLoopPlayer, -iConvertedCulture, True)
		iTotalConvertedCulture += iConvertedCulture
		
	plot.changeCulture(iPlayer, iTotalConvertedCulture, True)
	
	if bOwner:
		plot.setOwner(iPlayer)
		
# used: RFCUtils
def convertTemporaryCulture(tPlot, iPlayer, iPercent, bOwner):
	plot = core.plot(tPlot)
	if not plot.isOwned() or not plot.isCore(plot.getOwner()):
		plot.setCultureConversion(iPlayer, iPercent)
	
		if bOwner:
			plot.setOwner(iPlayer)

# used: DynamicCivs
def getMaster(identifier):
	masters = players.all().where(lambda p: team(identifier).isVassal(p))	
	if masters:
		return masters.first()
		
	return -1


# used: RFCUtils
# TODO: pushes out all units not just iOldOwner's
def pushOutGarrisons(tCityPlot, iOldOwner):
	destination = plots.surrounding(tCityPlot, radius=2).owner(iOldOwner).without(tCityPlot).land().passable().first()
	
	if destination:
		for unit in units.at(tCityPlot):
			if unit.getDomainType() == DomainTypes.DOMAIN_LAND:
				move(unit, destination)

# used: RFCUtils, RiseAndFall
# TODO: moves all units, not just iOldOwner's
# TODO: should it really be the closest instead of a random city?
def relocateGarrisons(tCityPlot, iOldOwner):
	if not is_minor(iOldOwner):
		city = cities.owner(iOldOwner).without(tCityPlot).random()
		if city:
			for unit in units.at(tCityPlot):
				if unit.getDomainType() == DomainTypes.DOMAIN_LAND:
					move(unit, city)
			return
	
	for unit in units.at(tCityPlot):
		unit.kill(False, iOldOwner)
			
# used: RiseAndFall
# TODO: replace plots.of
def removeCoreUnits(iPlayer):
	for plot in plots.birth(iPlayer):
		if plot.isCity():
			iOwner = city(plot).getOwner()
			if iOwner != iPlayer:
				relocateGarrisons(location(plot), iOwner)
				relocateSeaGarrisons(location(plot), iOwner)
				createGarrisons(location(plot), iOwner, 2)
		else:
			for unit in units.at(plot).notowner(iPlayer):
				iOwner = unit.getOwner()
				if not is_minor(iOwner):
					capital = player(iOwner).getCapitalCity()
					if capital:
						move(unit, capital)
					else:
						unit.kill(False, iPlayer)
			
# used: RFCUtils, RiseAndFall
def relocateSeaGarrisons(tCityPlot, iOldOwner):
	destination = cities.owner(iOldOwner).without(tCityPlot).coastal().first()
			
	if destination:
		for unit in units.at(tCityPlot).owner(iOldOwner):
			if unit.getDomainType() == DomainTypes.DOMAIN_SEA:
				move(unit, destination)


# used: Congresses, CvRFCEventHandler, RFCUtils, RiseAndFall
def createGarrisons(tCityPlot, iNewOwner, iNumUnits):
	iUnitType = getBestDefender(iNewOwner)
	makeUnits(iNewOwner, iUnitType, tCityPlot, iNumUnits)

# used: RiseAndFall, Stability
def clearPlague(iPlayer):
	for city in cities.owner(iPlayer).building(iPlague):
		city.setHasRealBuilding(iPlague, False)

# used: RiseAndFall
def squareSearch(tTopLeft, tBottomRight, function, argsList, tExceptions = ()): #by LOQ
	"""Searches all tile in the square from tTopLeft to tBottomRight and calls function for
	every tile, passing argsList. The function called must return a tuple: (1) a (2) if
	a plot should be painted and (3) if the search should continue."""
	return listSearch(plots.start(tTopLeft).end(tBottomRight).without(tExceptions), function, argsList)
	
# used: RFCUtils, RiseAndFall
def listSearch(lPlots, function, argsList):
	return [tPlot for tPlot in lPlots if function(tPlot, argsList)]

# used: RiseAndFall
def outerInvasion(tCoords, argsList):
	"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
	Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
	return invasion(tCoords, argsList, True)

# used: RFCUtils
def invasion(tCoords, argsList, bOuter):
	plot = plot(tCoords)
	if plot.isWater():
		return False
		
	if plot.isImpassable():
		return False
		
	if plot.getFeatureType() in [iMud, iJungle, iRainforest]:
		return False
		
	if plot.isCity():
		return False
		
	if plot.isUnit():
		return False
		
	if bOuter and plot.isOwned():
		return False
		
	return True
	
# used: RFCUtils
def landSpawn(tCoords, argsList, bOuter):
	plot = plot(tCoords)
	
	if plot.isWater():
		return False
		
	if plot.isImpassable():
		return False
		
	if plot.getFeatureType() in [iMud, iJungle, iRainforest]:
		return False
		
	if bOwner and plot.isOwned():
		return False
		
	if plot.getOwner() not in argsList:
		return False
		
	if plots.surrounding(tCoords).any(lambda p: p.isUnit()):
		return False
	
	return True

# used: RiseAndFall
def innerInvasion(tCoords, argsList):
	"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
	Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
	return invasion(tCoords, argsList, False)

# used: RiseAndFall
def innerSpawn(tCoords, argsList):
	"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
	Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
	return landSpawn(tCoords, argsList, False)

# used: RiseAndFall
def goodPlots(tCoords, argsList):
	"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
	Plot is valid if it's hill or flatlands, it isn't desert, tundra, marsh or jungle; it isn't occupied by a unit or city and if it isn't a civ's territory.
	Unit check extended to adjacent plots"""
	plot = plot(tCoords)
	
	if plot.isWater():
		return False
		
	if plot.isImpassable():
		return False
		
	if plot.isUnit():
		return False
		
	if plot.getTerrainType() in [iDesert, iTundra, iMarsh]:
		return False
		
	if plot.getFeatureType() in [iJungle, iRainforest]:
		return False
		
	if plot.isOwned():
		return False
		
	return True

# used: RiseAndFall
def ownedCityPlots(tCoords, iOwner):
	"""Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
	Plot is valid if it contains a city belonging to the civ"""
	city = city_(tCoords)
	return city and city.getOwner() == iOwner

# used: RiseAndFall
def clearCatapult(iPlayer):
	catapult = units.at(0, 0).first()
	if catapult:
		catapult.kill(False, -1)
		
	for plot in plots.surrounding((0, 0), radius=2):
		plot.setRevealed(iPlayer, False, True, -1)

# used: RFCUtils, RiseAndFall
# TODO: remove plots.of
def getCitiesInCore(iPlayer):
	return cities.core(iPlayer)
	
# used: CvRFCEventHandler, RFCUtils, Stability
def getOwnedCoreCities(iPlayer):
	return getCitiesInCore(iPlayer).owner(iPlayer)

# used: Stability
def removeReligionByArea(lPlotList, iReligion):
	for city in cities.of(lPlotList):
		removeReligion(city, iReligion)
			
# used: RFCUtils
def removeReligion(city, iReligion):
	if city.isHasReligion(iReligion) and not city.isHolyCity():
		city.setHasReligion(iReligion, False, False, False)
		
	if city.hasBuilding(temple(iReligion)):
		city.setHasRealBuilding(temple(iReligion), False)
		
	if city.hasBuilding(monastery(iReligion)):
		city.setHasRealBuilding(monastery(iReligion), False)
		
	if city.hasBuilding(cathedral(iReligion)):
		city.setHasRealBuilding(cathedral(iReligion), False)

# used: CvRandomEventInterface, RiseAndFall
def colonialConquest(iPlayer, tPlot):
	iCiv = civ(iPlayer)
	city = city_(tPlot)
	target = player(city.getOwner())
	
	if player and not team(target).isAtWar(iPlayer):
		team(iPlayer).declareWar(target.getID(), True, WarPlanTypes.WARPLAN_TOTAL)
		
	# independents too so the conquerors don't get pushed out in case the target collapses
	# TODO: instead properly establish war against independents on collapse
	for iMinor in players.civs([iIndependent, iIndependent2]):
		if not team(iPlayer).isAtWar(iMinor):
			team(iPlayer).declareWar(iMinor, True, WarPlanTypes.WARPLAN_LIMITED)
			
	targetPlot = plots.surrounding(tPlot).where(lambda p: not p.isCity() and not p.isPeak() and not p.isWater()).random()
	
	if iCiv in [iSpain, iPortugal, iNetherlands]:
		iNumUnits = 2
	elif iCiv in [iFrance, iEngland]:
		iNumUnits = 3
		
	iSiege = getBestSiege(iPlayer)
	iInfantry = getBestInfantry(iPlayer)
	
	iExp = 0
	if not player(iPlayer).isHuman(): iExp = 2
	
	if iSiege:
		makeUnits(iPlayer, iSiege, targetPlot, iNumUnits).experience(2)
		
	if iInfantry:
		makeUnits(iPlayer, iInfantry, targetPlot, 2*iNumUnits).experience(2)

# used: CvRandomEventInterface, RiseAndFall
def colonialAcquisition(iPlayer, tPlot):
	iCiv = civ(iPlayer)

	if iCiv in [iSpain, iPortugal]:
		iNumUnits = 1
	elif iCiv in [iFrance, iEngland, iNetherlands]:
		iNumUnits = 2
		
	plot = plot_(tPlot)
	if plot.isCity():
		flipCity(plot, False, True, iPlayer)
	else:
		plot.setCulture(iPlayer, 10, True)
		plot.setOwner(iPlayer)
		
		for current in plots.surrounding(plot):
			if location(plot) == location(current):
				convertPlotCulture(current, iPlayer, 80, True)
			else:
				convertPlotCulture(current, iPlayer, 60, True)
				
		player(iPlayer).found(*tPlot)
		
	makeUnits(iPlayer, iWorker, tPlot, iNumUnits)
	
	iInfantry = getBestInfantry(iPlayer)
	if iInfantry:
		makeUnits(iPlayer, iInfantry, plot, iNumUnits)
		
	iMissionary = missionary(player(iPlayer).getStateReligion())
	if iMissionary:
		makeUnit(iPlayer, iMissionary, plot)

# used: CvRandomEventInterface, RiseAndFall
def getColonialTargets(iPlayer, bEmpty=False):
	iCiv = civ(iPlayer)

	if iCiv in [iSpain, iFrance]:
		iNumCities = 1
	elif iCiv == iPortugal and not player(iPortugal).isHuman():
		iNumCities = 5
	else:
		iNumCities = 3

	index = list([iSpain, iFrance, iEngland, iPortugal, iNetherlands]).index(iCiv)
	lPlotList = tTradingCompanyPlotLists[index][:]
	
	cityPlots, emptyPlots = plots.of(lPlotList).split(lambda p: p.isCity())
	targetCities = cityPlots.notowner(iPlayer).sample(iNumCities)
	
	if bEmpty:
		targetPlots = emptyPlots.where_surrounding(lambda p: not p.isCity()).sample(iNumCities - len(targetCities))
		if targetPlots:
			return targetCities + targetPlots
		
	return targetCities
	
# used: RFCUtils
def getBorderPlots(iPlayer, tTL, tBR, iDirection = DirectionTypes.NO_DIRECTION, iNumPlots = 1):
	dMetrics = {
		DirectionTypes.NO_DIRECTION : lambda plot: 0,
		DirectionTypes.DIRECTION_EAST : lambda plot: plot.getX(),
		DirectionTypes.DIRECTION_WEST : lambda plot: -plot.getX(),
		DirectionTypes.DIRECTION_NORTH : lambda plot: plot.getY(),
		DirectionTypes.DIRECTION_SOUTH : lambda plot: -plot.getY()
	}
	
	metric = dMetrics[iDirection]
	lTargetCities = cities.start(tTL).end(tBR).owner(iPlayer).highest(iNumPlots, metric)
	
	return filter(None, [getPlotNearCityInDirection(city, iDirection) for city in lTargetCities])
	
# used: RFCUtils
def getPlotNearCityInDirection(city, iDirection):
	firstRing = plots.surrounding(city)
	secondRing = plots.surrounding(city, radius=2).without(firstRing).where(lambda p: not p.isCity() and not p.isWater())
	
	return secondRing.where(lambda p: estimate_direction(city, p) == iDirection).random()
	
# used: CvRFCEventHandler, Stability
def relocateCapital(iPlayer, newCapital):
	oldCapital = player(iPlayer).getCapitalCity()
	
	if location(oldCapital) == location(plots.newCapital(iPlayer)): return
	
	newCapital.setHasRealBuilding(iPalace, True)
	oldCapital.setHasRealBuilding(iPalace, False)
	
# used: RFCUtils
def hasEnemyUnit(iPlayer, tPlot):
	return units.at(tPlot).notowner(iPlayer).atwar(iPlayer).any()
	
# used: RFCUtils, RiseAndFall
# TODO: overlap with function in Barbs
def isFree(iPlayer, tPlot, bNoCity=False, bNoEnemyUnit=False, bCanEnter=False):
	plot = plot_(tPlot)
	
	if bNoCity:
		if cities.surrounding(plot):
			return False
			
	if bNoEnemyUnit:
		if plots.surrounding(plot).any(lambda p: hasEnemyUnit(iPlayer, p)):
			return False
		
	if bCanEnter:
		if plot.isPeak(): return False
		if plot.isWater(): return False
		if plot.getFeatureType() in [iMud, iJungle, iRainforest]: return False
		
	return True
	
# used: RiseAndFall
def isIsland(plot, iIslandLimit = 3):
	return map.getArea(plot_(plot).getArea()).getNumTiles <= iIslandLimit
			
# used: RiseAndFall
def foundCapital(iPlayer, tPlot, sName, iSize, iCulture, lBuildings=[], lReligions=[], iScenario=None):
	if iScenario is not None:
		if scenario() != iScenario: return
		
	x, y = tPlot
	player(iPlayer).found(x, y)
	
	city = city_(tPlot)
	if city:
		city.setCulture(iPlayer, iCulture, True)
		city.setName(sName, False)
		
		if city.getPopulation() < iSize:
			city.setPopulation(iSize)
			
		for iReligion in lReligions:
			city.setHasReligion(iReligion, True, False, False)
			
		for iBuilding in lBuildings:
			city.setHasRealBuilding(iBuilding, True)
			
	return city
	
# used: RFCUtils
def freeSlaves(city, iPlayer):
	iNumSlaves = city.getFreeSpecialistCount(iSpecialistSlave)
	if iNumSlaves:
		city.setFreeSpecialistCount(iSpecialistSlave, 0)
		makeUnits(iPlayer, base_unit(iSlave), city, iNumSlaves)
	
# used: GreatPeople
def replace(unit, iUnitType):
	replaced = makeUnit(unit.getOwner(), iUnitType, unit)
	replaced.convert(unit)
	return replaced
	
# used: RFCUtils
def getBestTrainable(iPlayer, lUnits, iDefault = iMilitia):
	return next([unique_unit(iPlayer, iUnit) for iUnit in lUnits if player(iPlayer).canTrain(unique_unit(iPlayer, iUnit), False, False)], iDefault)
	
# used: AIWars, RFCUtils, RiseAndFall, Stability
# TODO: update list or make dynamic
def getBestInfantry(iPlayer):
	lInfantryList = [iInfantry, iRifleman, iMusketeer, iArquebusier, iPikeman, iHeavySwordsman, iCrossbowman, iSwordsman, iLightSwordsman, iMilitia]
	return getBestTrainable(iPlayer, lInfantryList)
	
# used: AIWars, RiseAndFalls, Stability
# TODO: update list or make dynamic
def getBestCavalry(iPlayer):
	lCavalryList = [iCavalry, iDragoon, iHussar, iCuirassier, iPistolier, iLancer, iHorseArcher, iHorseman, iChariot]
	return getBestTrainable(iPlayer, lCavalryList)
	
# used: AIWars, RFCUtils, RiseAndFall, Stability
# TODO: update list or make dynamic
def getBestSiege(iPlayer):
	lSiegeList = [iHowitzer, iArtillery, iCannon, iBombard, iTrebuchet, iCatapult]
	return getBestTrainable(iPlayer, lSiegeList)

# used: RiseAndFall, Stability
# TODO: update list or make dynamic
def getBestCounter(iPlayer):
	lCounterList = [iMarine, iGrenadier, iPikeman, iHeavySpearman, iSpearman]
	return getBestTrainable(iPlayer, lCounterList)
	
# used: RFCUtils, RiseAndFall
# TODO: update list or make dynamic
def getBestDefender(iPlayer):
	# Leoreth: there is a C++ error for barbarians for some reason, workaround by simply using independents
	if player(iPlayer).isBarbarian(): iPlayer = players.independent().random()
	lDefenderList = [iInfantry, iMachineGun, iRifleman, iMusketeer, iArquebusier, iCrossbowman, iArcher, iMilitia]
	return getBestTrainable(iPlayer, lDefenderList)
	
# used: CvRFCEventHandler
# TODO: update list or make dynamic
def getBestWorker(iPlayer):
	lWorkerList = [iLabourer, iWorker]
	return getBestTrainable(iPlayer, lWorkerList, iWorker)
	
# used: Congresses, RiseAndFall, Stability
def completeCityFlip(tPlot, iPlayer, iOwner, iCultureChange, bBarbarianDecay = True, bBarbarianConversion = False, bAlwaysOwnPlots = False, bFlipUnits = False, bPermanentCultureChange = True):
	plot = plot_(tPlot)
	
	plot.setRevealed(iPlayer, False, True, -1)

	if bPermanentCultureChange:
		cultureManager(plot, iCultureChange, iPlayer, iOwner, bBarbarianDecay, bBarbarianConversion, bAlwaysOwnPlots)
	
	if bFlipUnits: 
		flipUnitsInCityBefore(plot, iPlayer, iOwner)
	else:
		pushOutGarrisons(plot, iOwner)
		relocateSeaGarrisons(plot, iOwner)
	
	flipCity(plot, False, False, iPlayer, [iOwner])
	
	if bFlipUnits: 
		flipUnitsInCityAfter(plot, iPlayer)
	else:
		createGarrisons(tPlot, iPlayer, 2)
	
	plot.setRevealed(iPlayer, True, True, -1)
	
	return city(tPlot)

# TODO: unused but should be
def isPastBirth(iPlayer):
	return year() >= year(dBirth[iPlayer])
	
# used: Congresses, Stability
def isNeighbor(iPlayer1, iPlayer2):
	return game.isNeighbors(iPlayer1, iPlayer2)
		
# used: Stability
def isGreatBuilding(iBuilding):
	if isWorldWonderClass(infos.building(iBuilding).getBuildingClassType()):
		return True			

	if isTeamWonderClass(infos.building(iBuilding).getBuildingClassType()):
		return True

	if isNationalWonderClass(infos.building(iBuilding).getBuildingClassType()):
		return True

	# Regular building
	return True
	
# used: CvRFCEventHandler, RiseAndFall
# TODO: overlaps with relocateCapital
def moveCapital(iPlayer, tPlot):
	newCapital = city(tPlot)
	if not newCapital or newCapital.getOwner() != iPlayer:
		return
		
	oldCapital = player(iPlayer).getCapitalCity()
	if oldCapital == newCapital:
		return
	
	oldCapital.setHasRealBuilding(iPalace, False)
	newCapital.setHasRealBuilding(iPalace, True)
	
# used: RiseAndFall
def createSettlers(iPlayer, iTargetCities):
	capital = plots.capital(iPlayer)

	iNumCities = cities.birth(iPlayer).count()
	
	if iNumCities < iTargetCities:
		makeUnits(iPlayer, unique_unit(iPlayer, iSettler), capital, iTargetCities - iNumCities)
	elif not city(capital):
		makeUnit(iPlayer, unique_unit(iPlayer, iSettler), capital)
		
# used: RiseAndFall
def createMissionaries(iPlayer, iNumUnits, iReligion=None):
	if not iReligion:
		iReligion = player(iPlayer).getStateReligion()
		
	if iReligion < 0:
		return
		
	if not game.isReligionFounded(iReligion):
		return
	
	makeUnits(iPlayer, missionary(iReligion), plots.capital(iPlayer), iNumUnits)
	
# used: RiseAndFall
# TODO: name is misleading, it has nothing inherently to do with colonies
def getColonyPlayer(iPlayer):
	return players.major().maximum(lambda p: cities.birth(iPlayer).owner(p).count())
	
# used: CvVictoryScreen, Victory
def getReligiousVictoryType(iPlayer):
	pPlayer = player(iPlayer)
	iStateReligion = pPlayer.getStateReligion()
	
	if iStateReligion >= 0:
		return iStateReligion
	elif pPlayer.getLastStateReligion() == -1:
		return iVictoryPaganism
	elif not pPlayer.isStateReligion():
		return iVictorySecularism
		
	return -1
	
# used: Victory
def getApprovalRating(iPlayer):
	pPlayer = player(iPlayer)
	
	if not pPlayer.isAlive(): return 0
	
	iHappy = pPlayer.calculateTotalCityHappiness()
	iUnhappy = pPlayer.calculateTotalCityUnhappiness()
	
	return (iHappy * 100) / max(1, iHappy + iUnhappy)
	
# used: Victory
def getLifeExpectancyRating(iPlayer):
	pPlayer = player(iPlayer)
	
	if not pPlayer.isAlive(): return 0
	
	iHealthy = pPlayer.calculateTotalCityHealthiness()
	iUnhealthy = pPlayer.calculateTotalCityUnhealthiness()
	
	return (iHealthy * 100) / max(1, iHealthy + iUnhealthy)
	
# used: RFCUtils
def getByzantineBriberyUnits(spy):
	iTreasury = player(spy).getGold()
	return units.at(spy).owner(iBarbarian).where(lambda unit: infos.unit(unit).getProductionCost() * 2 <= iTreasury)
	
# used: CvMainInterface
def canDoByzantineBribery(spy):
	if spy.getMoves() >= spy.maxMoves(): return False
	if not getByzantineBriberyUnits(spy): return False
	return True

# used: CvMainInterface
def doByzantineBribery(spy):
	lTargets = getByzantineBriberyUnits(spy)
			
	# only once per turn
	spy.finishMoves()
			
	# launch popup
	popup = Popup.PyPopup(7629, EventContextTypes.EVENTCONTEXT_ALL)
	data.lByzantineBribes = lTargets
	popup.setHeaderString(text("TXT_KEY_BYZANTINE_UP_TITLE"))
	popup.setBodyString(text("TXT_KEY_BYZANTINE_UP_BODY"))
	
	for unit, iCost in lTargets:
		popup.addButton(text("TXT_KEY_BYZANTINE_UP_BUTTON", unit.getName(), iCost))
		
	popup.addButton(text("TXT_KEY_BYZANTINE_UP_BUTTON_NONE"))
	popup.launch(False)
	
# used: CvScreensInterface, Stability
def canRespawn(iPlayer):
	iCiv = civ(iPlayer)

	# no respawn before spawn
	if year() < dBirth[iCiv] + 10: return False
	
	# only dead civ need to check for resurrection
	if player(iPlayer).isAlive(): return False
		
	# check if only recently died
	if turn() - data.players[iPlayer].iLastTurnAlive < turns(10): return False
	
	# check if the civ can be reborn at this date
	if not any(year().between(iStart, iEnd) for iStart, iEnd in dResurrections[iPlayer]):
		return False
				
	# TODO: function like exclusive(iCiv1, iCiv2) to simplify this
	# Thailand cannot respawn when Khmer is alive and vice versa
	if iCiv == iThailand and player(iKhmer).isAlive(): return False
	if iCiv == iKhmer and player(iThailand).isAlive(): return False
	
	# Rome cannot respawn when Italy is alive and vice versa
	if iCiv == iRome and player(iItaly).isAlive(): return False
	if iCiv == iItaly and player(iRome).isAlive(): return False
	
	# Greece cannot respawn when Byzantium is alive and vice versa
	if iCiv == iGreece and player(iByzantium).isAlive(): return False
	if iCiv == iByzantium and player(iGreece).isAlive(): return False
	
	# India cannot respawn when Mughals are alive (not vice versa -> Pakistan)
	if iCiv == iIndia and player(iMughals).isAlive(): return False
	
	# Exception during Japanese UHV
	if player(iJapan).isHuman() and year().between(1920, 1945):
		if iCiv in [iChina, iKorea, iIndonesia, iThailand]:
			return False
	
	if not player(iPlayer).isAlive() and turn() > data.players[iPlayer].iLastTurnAlive + turns(20):
		if iCiv not in dRebirth or year() > year(dRebirth[iCiv]) + turns(10):
			return True
			
	return False
	
# used: CvScreensInterface, MapDrawer, RFCUtils
def canEverRespawn(iPlayer, iGameTurn = None):
	if iGameTurn is None:
		iGameTurn = turn()
		
	return not any(turn(iEnd) > iGameTurn for _, iEnd in dResurrections[iPlayer])
	
# used: Barbs
def evacuate(iPlayer, tPlot):
	for plot in plots.surrounding(tPlot):
		for unit in units.at(plot).notowner(iPlayer):
			target = plots.surrounding(plot, radius=2).without(tPlot).where(lambda p: isFree(unit.getOwner(), p, bNoEnemyUnit=True, bCanEnter=True)).random()
			move(unit, target)

# used: CvScreensInterface, CvPlatyBuilderScreen
def toggleStabilityOverlay(iPlayer = -1):
	bReturn = bStabilityOverlay
	removeStabilityOverlay()

	if bReturn:
		return

	bWB = (iPlayer != -1)
	if iPlayer == -1:
		iPlayer = active()

	bStabilityOverlay = True
	CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).setState("StabilityOverlay", True)

	iTeam = player(iPlayer).getTeam()

	engine = CyEngine()

	# apply the highlight
	for plot in plots.all():
		if game.isDebugMode() or plot.isRevealed(iTeam, False):
			if plot.isWater(): continue
			if plot.isCore(iPlayer):
				iPlotType = iCore
			else:
				iSettlerValue = plot.getSettlerValue(iPlayer)
				if bWB and iSettlerValue == 3:
					iPlotType = iAIForbidden
				elif iSettlerValue >= 90:
					if isPossibleForeignCore(iPlayer, plot):
						iPlotType = iContest
					else:
						iPlotType = iHistorical
				elif isPossibleForeignCore(iPlayer, plot):
					iPlotType = iForeignCore
				else:
					iPlotType = -1
			if iPlotType != -1:
				szColor = lStabilityColors[iPlotType]
				engine.fillAreaBorderPlotAlt(plot.getX(), plot.getY(), 1000+iPlotType, szColor, 0.7)
				
# used: CvScreensInterface, RFCUtils, CvPlatyBuilderScreen
def removeStabilityOverlay():
	engine = CyEngine()
	# clear the highlight
	for i in range(50):
		engine.clearAreaBorderPlots(1000+i)
	bStabilityOverlay = False
	CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).setState("StabilityOverlay", False)
	
# used: CvPediaBuilding
def getAdvisorString(iBuilding):
	iAdvisor = infos.building(iBuilding).getAdvisorType()
	
	dAdvisors = defaultdict({
		0 : 'Military',
		1 : 'Religious',
		2 : 'Economy',
		3 : 'Science',
		4 : 'Culture',
		5 : 'Growth',
	}, default='')
	
	return dAdvisors[iAdvisor]
	
# used: RFCUtils
def isGreatPeopleBuilding(iBuilding):
	return any(infos.unit(iUnit).getBuildings(iBuilding) for iUnit in lGreatPeopleUnits + [iGreatGeneral, iGreatSpy])
	
# used: CvPediaMain
def getBuildingCategory(iBuilding):
	'0 = Building'
	'1 = Religious Building'
	'2 = Unique Building'
	'3 = Great People Building'
	'4 = National Wonder'
	'5 = World Wonder'

	BuildingInfo = infos.building(iBuilding)
	if BuildingInfo.getReligionType() > -1:
		return 1
	elif isWorldWonderClass(BuildingInfo.getBuildingClassType()):
		return 5
	else:
		iBuildingClass = BuildingInfo.getBuildingClassType()
		iDefaultBuilding = infos.buildingClass(iBuildingClass).getDefaultBuildingIndex()
		if isNationalWonderClass(iBuildingClass):
			return 4
		elif isGreatPeopleBuilding(iBuilding):
			return 3
		else:
			if iDefaultBuilding > -1 and iDefaultBuilding != iBuilding:
				if infos.building(iBuilding).isGraphicalOnly():
					return 0
				return 2
			else:
				if infos.building(iBuilding).isGraphicalOnly():
					return -1
				return 0
				
# used: CvPediaLeader, CvPediaMain
def getLeaderCiv(iLeader):
	return next([iCiv for iCiv in range(iNumCivilizations) if infos.civ(iCiv).isLeaders(iLeader)], None)
	
# used: Religions, RiseAndFall
def setStateReligionBeforeBirth(lCivs, iReligion):
	for iCiv in lCivs:
		if year() < dBirth[iCiv] and player(iCiv).getStateReligion() != iReligion:
			player(iCiv).setLastStateReligion(iReligion)
	
# used: CvRFCEventHandler
def captureUnit(pLosingUnit, pWinningUnit, iUnit, iChance):
	if pLosingUnit.isAnimal(): return
	
	if pLosingUnit.getDomainType() != DomainTypes.DOMAIN_LAND: return
	
	if infos.unit(pLosingUnit).getCombat() == 0: return
	
	iPlayer = pWinningUnit.getOwner()
	
	if rand(100) < iChance:
		makeUnit(iPlayer, iUnit, pWinningUnit, UnitAITypes.UNITAI_WORKER)
		message(pWinningUnit.getOwner(), 'TXT_KEY_UP_ENSLAVE_WIN', sound='SND_REVOLTEND', event=1, button=infos.unit(iUnit).getButton(), color=8, location=pWinningUnit)
		message(pLosingUnit.getOwner(), 'TXT_KEY_UP_ENSLAVE_LOSE', sound='SND_REVOLTEND', event=1, button=infos.unit(iUnit).getButton(), color=7, location=pWinningUnit)
		
		if civ(iPlayer) == iAztecs:
			if civ(pLosingUnit) not in dCivGroups[iCivGroupAmerica] and not is_minor(pLosingUnit):
				data.iAztecSlaves += 1
		
# used: CvRandomEventInterface
# TODO: just move there?
def triggerMeltdown(iPlayer, iCity):
	print "trigger meltdown"
	
	pCity = player(iPlayer).getCity(iCity)
	pCity.triggerMeltdown(iNuclearPlant)
	
# unused
# kept for scripted settler AI later
def getCitySiteList(iPlayer):
	pPlayer = player(iPlayer)
	return [pPlayer.AI_getCitySite(i) for i in range(pPlayer.AI_getNumCitySites())]

# used: Congresses, Stability
def flipOrRelocateGarrison(city, iNumDefenders):
	lRelocatedUnits = []
	lFlippedUnits = []
	
	for plot in plots.surrounding(city, radius=2).where(lambda p: not p.isCity() or location(p) == location(city)):
		for unit in units.at(plot).owner(city.getOwner()).domain(DomainTypes.DOMAIN_LAND):
			if unit.canFight() and len(lFlippedUnits) < iNumDefenders:
				lFlippedUnits.append(unit)
			else:
				lRelocatedUnits.append(unit)
					
	return lFlippedUnits, lRelocatedUnits
		
# used: RFCUtils
# TODO: must overlap with SOMETHING
def flipUnit(unit, iNewOwner, plot):
	if location(unit) >= (0, 0):
		iUnitType = unit.getUnitType()
		unit.kill(False, iBarbarianPlayer)
		makeUnit(iNewOwner, iUnitType, plot)
	
# used: Congresses, Stability
def relocateUnitsToCore(iPlayer, lUnits):
	print "relocateUnitsToCore: %s" % lUnits
	coreCities = getOwnedCoreCities(iPlayer)
	if not coreCities:
		killUnits(lUnits)
		return
	
	dUnits = units.of(lUnits).where(lambda unit: unit.plot() and unit.plot().getOwner() not in [iPlayer, -1]).by_type()
	
	for iUnitType in dUnits:
		for i, unit in enumerate(dUnits[iUnitType]):
			index = i % (coreCities.count() * 2)
			if index < coreCities.count():
				city = coreCities[index]
				move(unit, city)
				
# used: Congresses, Stability
def flipOrCreateDefenders(iNewOwner, units, tPlot, iNumDefenders):
	for unit in units:
		flipUnit(unit, iNewOwner, tPlot)

	if len(units) < iNumDefenders and active() != iNewOwner:
		makeUnits(iNewOwner, getBestDefender(iNewOwner), tPlot, iNumDefenders - len(units))
		
# used: Congresses, Stability
def killUnits(lUnits):
	for unit in lUnits:
		if location(unit) >= (0, 0):
			unit.kill(False, iBarbarianPlayer)
			
# used: RiseAndFall
def ensureDefenders(iPlayer, tPlot, iNumDefenders):
	presentUnits = units.at(tPlot).owner(iPlayer).where(lambda u: u.canFight())
	if len(presentUnits) < iNumDefenders:
		makeUnits(iPlayer, getBestDefender(iPlayer), tPlot, iNumDefenders - len(presentUnits))
		
def getGoalText(baseKey, bTitle = False):
	fullKey = baseKey
	iGameSpeed = game.getGameSpeedType()
	
	if bTitle:
		fullKey += '_TITLE'
	elif iGameSpeed < 2:
		fullKey += '_' + infos.gameSpeed().getText().upper()
		
	return text_if_exists(fullKey, otherwise=baseKey)
		
# used: CvVictoryScreen, WBStoredDataScreen
def getHistoricalGoalText(iPlayer, iGoal, bTitle = False):
	iCiv = player(iPlayer).getCivilizationType()
	iGameSpeed = game.getGameSpeedType()
	
	baseKey = "TXT_KEY_UHV_%s%d" % (infos.civ(iCiv).getIdentifier(), iGoal + 1)
	
	return getGoalText(baseKey, bTitle)
	
def getReligiousGoalText(iReligion, iGoal, bTitle = False):
	iGameSpeed = game.getGameSpeedType()

	if iReligion < iNumReligions:
		religionKey = infos.religion(iReligion).getText()[:3].upper()
	elif iReligion == iNumReligions:
		religionKey = "POL"
	elif iReligion == iNumReligions+1:
		religionKey = "SEC"
		
	baseKey = "TXT_KEY_URV_%s%d" % (religionKey, iGoal + 1)
	
	return getGoalText(baseKey, bTitle)
	
# used: CvDawnOfMan
def getDawnOfManText(iPlayer):
	iScenario = scenario()
	baseKey = 'TXT_KEY_DOM_%s' % str(name(iPlayer).replace(' ', '_').upper())
	
	fullKey = baseKey
	if iScenario == i600AD: fullKey += "_600AD"
	elif iScenario == i1700AD: fullKey += "_1700AD"
	
	return text_if_exists(fullKey, otherwise=baseKey)
	
# used: CvRFCEventHandler
# TODO: this overlaps with isControlled and isAreaControlled in DynamicCivs
def isAreaControlled(iPlayer, tTL, tBR, tExceptions=[]):
	areaCities = cities.start(tTL).end(tBR).without(tExceptions)
	return areaCities.owner(iPlayer) >= areaCities
	
# unused
# keep for Rise and Fall refactoring
def breakAutoplay():
	if year() < year(dBirth[active()]):
		makeUnit(active(), iSettler, (0, 0))
		
# used: CvRFCEventHandler
# TODO: use more, e.g. wonder implementations -> check Wonders module
def getBuildingEffectCity(iBuilding):
	if game.getBuildingClassCreatedCount(infos.building(iBuilding).getBuildingClassType()) == 0:
		return None
		
	return cities.all().building_effect(iBuilding).first()
	
# used: BUG/UnitGrouper.py, CvRFCEventHandler
def getDefaultGreatPerson(iGreatPersonType):
	if iGreatPersonType in dFemaleGreatPeople.values():
		return dict((v, k) for k, v in dFemaleGreatPeople.items())[iGreatPersonType]
	return iGreatPersonType

# used: RFCUtils
def isPossibleForeignCore(iPlayer, tPlot):
	plot = plot(tPlot)
	return players.major().alive().without(iPlayer).any(lambda p: canEverRespawn(p) and plot.isCore(p))
	
# used: RiseAndFall
def canSwitch(iPlayer, iBirthTurn):
	if turn() != iBirthTurn + data.players[iPlayer].iSpawnDelay:
		return False
		
	if not player(iPlayer).isAlive():
		return False
		
	if data.bAlreadySwitched and not data.bUnlimitedSwitching:
		return False
		
	if dSpawn[iPlayer] <= dSpawn[active()]:
		return False
		
	if civ() in dNeighbours[iPlayer] and year(dSpawn[iPlayer]) < year(dSpawn[active()]) + turns(25):
		return False
		
	return True
	
# used: RiseAndFall
def setCivilization(iPlayer, iNewCivilization):
	iOldCivilization = civ(iPlayer)
	if iOldCivilization == iNewCivilization:
		return

	player(iPlayer).setCivilizationType(iNewCivilization)
	del data.dSlots[iOldCivilization]
	data.dSlots[iNewCivilization] = iPlayer