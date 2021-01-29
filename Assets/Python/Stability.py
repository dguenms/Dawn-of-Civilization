# Rhye's and Fall of Civilization - Stability

from CvPythonExtensions import *
from StoredData import data # edead
from Consts import *
from RFCUtils import *
import DynamicCivs as dc
from operator import itemgetter
import math
import Victory as vic
import Periods as periods
from Events import handler, events

import PyHelpers
PyPlayer = PyHelpers.PyPlayer

import BugPath
from datetime import date

from Locations import *
from Core import *

# globals
gc = CyGlobalContext()

tCrisisLevels = (
"TXT_KEY_STABILITY_CRISIS_LEVEL_TERMINAL",
"TXT_KEY_STABILITY_CRISIS_LEVEL_SEVERE",
"TXT_KEY_STABILITY_CRISIS_LEVEL_MODERATE",
"TXT_KEY_STABILITY_CRISIS_LEVEL_MINOR",
"TXT_KEY_STABILITY_CRISIS_LEVEL_MINOR",
)

tCrisisTypes = (
"TXT_KEY_STABILITY_CRISIS_TYPE_EXPANSION",
"TXT_KEY_STABILITY_CRISIS_TYPE_ECONOMY",
"TXT_KEY_STABILITY_CRISIS_TYPE_DOMESTIC",
"TXT_KEY_STABILITY_CRISIS_TYPE_FOREIGN",
"TXT_KEY_STABILITY_CRISIS_TYPE_MILITARY",
)

tEraAdministrationModifier = (
	100, # ancient
	200, # classical
	200, # medieval
	250, # renaissance
	300, # industrial
	350, # modern
	400, # future
)


@handler("BeginGameTurn")
def checkScheduledCollapse():
	for iPlayer in players.major():
		if data.players[iPlayer].iTurnsToCollapse == 0:
			if player(iPlayer).isAlive():
				completeCollapse(iPlayer)
			data.players[iPlayer].iTurnsToCollapse = -1
		elif data.players[iPlayer].iTurnsToCollapse > 0:
			data.players[iPlayer].iTurnsToCollapse -= 1


@handler("BeginGameTurn")
def crisisCountdown():
	for iPlayer in players.major():
		if getCrisisCountdown(iPlayer) > 0:
			changeCrisisCountdown(iPlayer, -1)


@handler("BeginGameTurn")
def updateTrendScores():
	# calculate economic and happiness stability
	if every(3):
		for iPlayer in players.major():
			updateEconomyTrend(iPlayer)
			updateHappinessTrend(iPlayer)
			
		# calculate war stability
		for iPlayer, iEnemy in players.major().permutations():
			if team(iPlayer).isAtWar(iEnemy):
				updateWarTrend(iPlayer, iEnemy)
		
		for iPlayer, iEnemy in players.major().permutations():
				if team(iPlayer).isAtWar(iEnemy):
					data.players[iPlayer].lLastWarSuccess[iEnemy] = team(iPlayer).AI_getWarSuccess(iEnemy)
				else:
					data.players[iPlayer].lLastWarSuccess[iEnemy] = 0


@handler("BeginGameTurn")
def decayPenalties():
	# decay penalties from razing cities and losing to barbarians
	if every(5):
		if data.iHumanRazePenalty < 0:
			data.iHumanRazePenalty += 2
		for iPlayer in players.major():
			if data.players[iPlayer].iBarbarianLosses > 0:
				data.players[iPlayer].iBarbarianLosses -= 1


@handler("BeginGameTurn")
def checkLostCitiesCollapses():
	if every(12):
		for iPlayer in players.major():
			checkLostCitiesCollapse(iPlayer)
	

@handler("BeginGameTurn")
def updateHumanStability(iGameTurn):
	if iGameTurn >= year(dBirth[active()]):
		data.iHumanStability = calculateStability(active())[0]


@handler("EndPlayerTurn")
def checkSecedingCities(iGameTurn, iPlayer):
	secedingCities = data.getSecedingCities(iPlayer)
	
	if secedingCities:
		secedeCities(iPlayer, secedingCities.existing())
		data.setSecedingCities(iPlayer, cities.of([]))


def triggerCrisis(iPlayer):
	if getCrisisCountdown(iPlayer) > 0:
		return
	
	changeCrisisCountdown(iPlayer, turns(10))
	
	bFall = since(year(dFall[iPlayer])) >= 0
	
	# help AI to not immediately collapse
	if not player(iPlayer).isHuman() and not bFall:
		# with no overexpansion at all, just have a domestic crisis (once until back at shaky again)
		if not data.players[iPlayer].bDomesticCrisis and data.players[iPlayer].lStabilityCategoryValues[0] <= 0:
			domesticCrisis(iPlayer)
			return
		
		# collapse to core if controlling cities outside of core
		if cities.core(iPlayer).owner(iPlayer) < cities.owner(iPlayer):
			collapseToCore(iPlayer)
			return

	scheduleCollapse(iPlayer)


def scheduleCollapse(iPlayer):
	data.players[iPlayer].iTurnsToCollapse = 1

@handler("cityAcquired")
def onCityAcquired(iOwner, iPlayer, city, bConquest):
	if not bConquest:
		return
	
	checkStability(iOwner)
	checkLostCoreCollapse(iOwner)
	
	if player(iPlayer).isBarbarian():
		checkBarbarianCollapse(iOwner)

@handler("cityRazed")
def onCityRazed(city, iPlayer):
	iOwner = city.getPreviousOwner()
	
	if player(iOwner).isBarbarian(): return

	if player(iPlayer).isHuman() and civ(iPlayer) != iMongols:
		iRazePenalty = -10
		if city.getHighestPopulation() < 5 and not city.isCapital():
			iRazePenalty = -2 * city.getHighestPopulation()
			
		if is_minor(iOwner): iRazePenalty /= 2
			
		data.iHumanRazePenalty += iRazePenalty
		checkStability(iPlayer)

@handler("techAcquired")
def onTechAcquired(iTech, iTeam, iPlayer):
	if year() == scenarioStartTurn():
		return
	
	checkStability(iPlayer)

@handler("vassalState")
def onVassalState(iMaster, iVassal, bVassal, bCapitulated):
	if bVassal and bCapitulated:
		checkStability(iMaster, True)	
		balanceStability(iVassal, iStabilityShaky)

@handler("changeWar")
def onChangeWar(bWar, iTeam, iOtherTeam):
	if not is_minor(iTeam) and not is_minor(iOtherTeam):
		checkStability(iTeam, not bWar)
		checkStability(iOtherTeam, not bWar)
		
		if bWar:
			startWar(iTeam, iOtherTeam)
			startWar(iOtherTeam, iTeam)

@handler("revolution")
def onRevolution(iPlayer):
	checkStability(iPlayer)

@handler("playerChangeStateReligion")
def onPlayerChangeStateReligion(iPlayer):
	checkStability(iPlayer)

@handler("capitalMoved")
def onCapitalMoved(city):
	checkStability(city.getOwner())

@handler("wonderBuilt")
def onWonderBuilt(city, iWonder):
	checkStability(city.getOwner(), True)

@handler("goldenAge")	
def onGoldenAge(iPlayer):
	checkStability(iPlayer, True)

@handler("greatPersonBorn")
def onGreatPersonBorn(unit, iPlayer):
	checkStability(iPlayer, True)

@handler("combatResult")
def onCombatResult(winningUnit, losingUnit):
	if player(winningUnit).isBarbarian() and not is_minor(losingUnit):
		data.players[losingUnit.getOwner()].iBarbarianLosses += 1

@handler("releasedPlayer")
def onReleasedPlayer(iPlayer, iReleasedPlayer):
	releasedCities = cities.owner(iPlayer).core(iReleasedPlayer).where(lambda city: not city.plot().isCore(iPlayer) and not city.isCapital())

	doResurrection(iReleasedPlayer, releasedCities, bAskFlip=False, bDisplay=True)
	
	player(iReleasedPlayer).AI_changeAttitudeExtra(iPlayer, 2)
	
def onCivSpawn(iPlayer):
	for iOlderNeighbor in players.civs(dNeighbours[iPlayer]):
		if player(iOlderNeighbor).isAlive() and stability(iOlderNeighbor) > iStabilityShaky:
			decrementStability(iOlderNeighbor)
	
def setStabilityLevel(iPlayer, iStabilityLevel):
	if stability(iPlayer) == iStabilityLevel:
		return

	data.setStabilityLevel(iPlayer, iStabilityLevel)
	
	if iStabilityLevel >= iStabilityShaky:
		data.players[iPlayer].bDomesticCrisis = False
	
	if iStabilityLevel == iStabilityCollapsing:
		message(iPlayer, 'TXT_KEY_STABILITY_COLLAPSING_WARNING', color=iRed)
	
def incrementStability(iPlayer):
	setStabilityLevel(iPlayer, min(iStabilitySolid, stability(iPlayer) + 1))
	
def decrementStability(iPlayer):
	setStabilityLevel(iPlayer, max(iStabilityCollapsing, stability(iPlayer) - 1))
	
def getCrisisCountdown(iPlayer):
	return data.players[iPlayer].iCrisisCountdown
	
def changeCrisisCountdown(iPlayer, iChange):
	data.players[iPlayer].iCrisisCountdown += iChange
	
def isImmune(iPlayer):
	pPlayer = player(iPlayer)
	
	# must not be dead
	if not pPlayer.isAlive() or pPlayer.getNumCities() == 0:
		return True
		
	# only for major civs
	if is_minor(iPlayer):
		return True
		
	# immune right after scenario start
	if turn() < scenarioStartTurn() + turns(20):
		return True
		
	# immune right after birth
	if turn() < pPlayer.getInitialBirthTurn() + turns(20):
		return True
		
	# immune right after resurrection
	if turn() < pPlayer.getLastBirthTurn() + turns(10):
		return True
		
	return False
	
def checkBarbarianCollapse(iPlayer):
	pPlayer = player(iPlayer)
		
	if isImmune(iPlayer): return
		
	iNumCities = pPlayer.getNumCities()
	iLostCities = cities.owner(iBarbarian).where(lambda city: city.getOriginalOwner() == iPlayer).count()
			
	# lost more than half of your cities to barbarians: collapse
	if iLostCities > iNumCities:
		debug('Collapse by barbarians: ' + pPlayer.getCivilizationShortDescription(0))
		message(iPlayer, 'TXT_KEY_STABILITY_MAJOR_BARBARIAN_LOSSES', color=iRed)
		completeCollapse(iPlayer)
		
	# lost at least two cities to barbarians: lose stability
	elif iLostCities >= 2:
		debug('Lost stability to barbarians: ' + pPlayer.getCivilizationShortDescription(0))
		message(iPlayer, 'TXT_KEY_STABILITY_MINOR_BARBARIAN_LOSSES', color=iRed)
		decrementStability(iPlayer)
		
def checkLostCitiesCollapse(iPlayer):
	pPlayer = player(iPlayer)
	
	if isImmune(iPlayer): return
		
	iNumCurrentCities = pPlayer.getNumCities()
	iNumPreviousCities = data.players[iPlayer].iNumPreviousCities
	
	# half or less cities than 12 turns ago: collapse (exceptions for civs with very little cities to begin with -> use lost core collapse)
	if iNumPreviousCities > 2 and 2 * iNumCurrentCities <= iNumPreviousCities:
	
		message(iPlayer, 'TXT_KEY_STABILITY_LOST_CITIES_COLLAPSE', color=iRed)
	
		if stability(iPlayer) == iStabilityCollapsing:
			debug('Collapse by lost cities: ' + pPlayer.getCivilizationShortDescription(0))
			scheduleCollapse(iPlayer)
		else:
			debug('Collapse to core by lost cities: ' + pPlayer.getCivilizationShortDescription(0))
			setStabilityLevel(iPlayer, iStabilityCollapsing)
			collapseToCore(iPlayer)
		
	data.players[iPlayer].iNumPreviousCities = iNumCurrentCities
	
def checkLostCoreCollapse(iPlayer):
	pPlayer = player(iPlayer)
	
	if isImmune(iPlayer): return
	
	lCities = cities.core(iPlayer).owner(iPlayer)
	
	# completely pushed out of core: collapse
	if len(lCities) == 0:
		if periods.evacuate(iPlayer):
			return
			
		message(iPlayer, 'TXT_KEY_STABILITY_LOST_CORE_COLLAPSE', color=iRed)
	
		debug('Collapse from lost core: ' + pPlayer.getCivilizationShortDescription(0))
		scheduleCollapse(iPlayer)

def determineStabilityThreshold(iPlayer, iCurrentLevel):
	iThreshold = 10 * iCurrentLevel - 10
	
	if isDecline(iPlayer): iThreshold += 10
	
	return iThreshold
	
def determineStabilityLevel(iPlayer, iCurrentLevel, iStability):
	iThreshold = determineStabilityThreshold(iPlayer, iCurrentLevel)
	
	if iStability >= iThreshold: return min(iStabilitySolid, iCurrentLevel + 1)
	elif isDecline(iPlayer): return max(iStabilityCollapsing, iCurrentLevel - (iThreshold - iStability) / 10)
	elif iStability < iThreshold - 10: return max(iStabilityCollapsing, iCurrentLevel - 1)
	
	return iCurrentLevel

def checkStability(iPlayer, bPositive = False, iMaster = -1):
	pPlayer = player(iPlayer)
	
	bVassal = (iMaster != -1)
	
	# no check if already scheduled for collapse
	if data.players[iPlayer].iTurnsToCollapse >= 0: return
	
	# vassal checks are made for triggers of their master civ
	if team(iPlayer).isAVassal() and not bVassal: return
	
	if isImmune(iPlayer): return
		
	# immune to negative stability checks in golden ages
	if pPlayer.isGoldenAge(): bPositive = True
		
	# immune during anarchy
	if pPlayer.isAnarchy(): return
	
	# no repeated stability checks
	if data.players[iPlayer].iLastStabilityTurn == turn(): return
	
	data.players[iPlayer].iLastStabilityTurn = turn()
		
	iStability, lStabilityTypes, lParameters = calculateStability(iPlayer)
	iStabilityLevel = stability(iPlayer)
	bHuman = player(iPlayer).isHuman()
	bFall = isDecline(iPlayer)
	
	iNewStabilityLevel = determineStabilityLevel(iPlayer, iStabilityLevel, iStability)
	
	if iNewStabilityLevel > iStabilityLevel:
		setStabilityLevel(iPlayer, iNewStabilityLevel)
		
	elif not bPositive:
		if iNewStabilityLevel < iStabilityLevel:
			setStabilityLevel(iPlayer, iNewStabilityLevel)
	
		# if remain on collapsing and stability does not improve, collapse ensues
		elif iNewStabilityLevel == iStabilityCollapsing:
			if iStability <= data.players[iPlayer].iLastStability:
				triggerCrisis(iPlayer)
		
	# update stability information
	data.players[iPlayer].iLastStability = iStability
	for i in range(5):
		data.players[iPlayer].lStabilityCategoryValues[i] = lStabilityTypes[i]
	
	for i in range(iNumStabilityParameters):
		pPlayer.setStabilityParameter(i, lParameters[i])
	
	# check vassals
	for iLoopPlayer in players.major():
		if team(iLoopPlayer).isVassal(iPlayer):
			checkStability(iLoopPlayer, bPositive, iPlayer)
		
def getPossibleMinors(iPlayer):
	lPossibleMinors = [iIndependent, iIndependent2]

	if gc.getGame().countKnownTechNumTeams(iNationalism) == 0 and civ(iPlayer) in [iMaya, iAztecs, iInca, iMali, iEthiopia, iCongo]:
		lPossibleMinors = [iNative]
		
	if gc.getGame().getCurrentEra() <= iMedieval:
		lPossibleMinors = [iBarbarian, iIndependent, iIndependent2]
		
	return players.civs(*lPossibleMinors)
	
def secession(iPlayer, secedingCities):
	data.setSecedingCities(iPlayer, secedingCities)

def canBeRazed(city):
	# always raze Harappan cities
	if civ(city) == iHarappa and not player(city).isHuman():
		return True
	
	if city.getPopulation() >= 10:
		return False
	
	if city.getCultureLevel() >= 3:
		return False
	
	if city.isHolyCity():
		return False
		
	if city.isCapital():
		return False
	
	if city.at(*tJerusalem):
		return False
	
	closest = closestCity(city, city.getOwner(), same_continent=True)
	if closest and distance(city, closest) <= 2:
		if city.getCultureLevel() <= closest.getCultureLevel() and city.getPopulation() < closest.getPopulation():
			return True
	
	return False
	
def getCityClaim(city):
	iOwner = city.getOwner()
	
	possibleClaims = players.major().alive().without(iOwner).before_fall()
	
	# claim based on core territory
	coreClaims = possibleClaims.where(lambda p: city.isCore(p))
	if coreClaims:
		return coreClaims.maximum(lambda p: plot(city).getSettlerValue(p))
	
	# claim based on original owner, unless lost a long time ago
	iOriginalOwner = city.getOriginalOwner()
	if iOriginalOwner in possibleClaims.ai():
		if plot(city).getSettlerValue(iOriginalOwner) >= 90:
			if city.getGameTurnPlayerLost(iOriginalOwner) >= turn() - turns(50):
				return iOriginalOwner
	
	# claim based on culture
	iTotalCulture = plot(city).countTotalCulture()
	cultureClaims = possibleClaims.ai().where(lambda p: iTotalCulture > 0 and 100 * plot(city).getCulture(p) / iTotalCulture >= 75)
	if cultureClaims:
		return cultureClaims.maximum(lambda p: plot(city).getCulture(p))
	
	# claim based on war targets: needs to be winning the war based on war success
	closest = closestCity(city, same_continent=True)
	warClaims = possibleClaims.where(lambda p: team(p).isAtWar(team(iOwner).getID()) and player(p).getWarValue(*location(city)) >= 8 and team(p).AI_getWarSuccess(team(iOwner).getID()) > team(iOwner).AI_getWarSuccess(team(p).getID()))
	warClaims = warClaims.where(lambda p: not closest or closest.getOwner() == p or not team(iOwner).isAtWar(closest.getOwner()))
	warClaims = warClaims.where(lambda p: not closestCity(city, owner=p, same_continent=True) or distance(city, closestCity(city, owner=p, same_continent=True)) >= 12)
	if warClaims:
		return warClaims.maximum(lambda p: team(p).AI_getWarSuccess(team(iOwner).getID()) - team(iOwner).AI_getWarSuccess(team(p).getID()))
	
	# claim for dead civilisation that can be resurrected
	resurrections = players.major().before_fall().without(iOwner).where(canRespawn).where(lambda p: city in cities.respawn(p))
	if resurrections:
		return resurrections.maximum(lambda p: (city.isCore(p), plot(city).getSettlerValue(p)))
	
	return -1

def getAdditionalResurrectionCities(iPlayer, secedingCities):
	return [city for city in getResurrectionCities(iPlayer, True) if city not in secedingCities]

def canResurrectFromCities(iPlayer, resurrectionCities):
	# cannot resurrect without cities
	if not resurrectionCities:
		return False

	# only one city is not sufficient for resurrection, unless there is only one city available
	if len(resurrectionCities) <= 1 and len(resurrectionCities) < cities.respawn(iPlayer).count():
		return False

	# at least one city needs to be in core for the resurrecting civ
	if none(city.isCore(iPlayer) for city in resurrectionCities):
		return False
	
	return True

def secedeCities(iPlayer, secedingCities, bRazeMinorCities = False):
	iCiv = civ(iPlayer)
	bComplete = len(secedingCities) == player(iPlayer).getNumCities()
	iArmyPercent = 100 - 100 * len(secedingCities) / player(iPlayer).getNumCities()
	
	if not secedingCities:
		return
	
	if bComplete:
		clearPlague(iPlayer)
	
	# if smaller cities are supposed to be destroyed, do that first
	destroyedCities, cededCities = secedingCities.split(lambda city: bRazeMinorCities and canBeRazed(city))
	
	for city in destroyedCities:
		player(iBarbarian).disband(city)
		plot(city).setCulture(iPlayer, 0, True)
	
	# determine who has the best claim on each city
	dClaimedCities = appenddict()
	for city in cededCities:
		iClaim = getCityClaim(city)
		dClaimedCities[iClaim].append(city)
		
	lMinorCities = dClaimedCities.pop(-1, [])
		
	for iClaimant, claimedCities in dClaimedCities.items():
		# assign cities to living civs
		if player(iClaimant).isAlive():
			for city in claimedCities:
				secedeCity(city, iClaimant, not bComplete, iArmyPercent)
		
		# if sufficient for resurrection, resurrect civs
		elif canResurrectFromCities(iClaimant, claimedCities):
			additionalCities = getAdditionalResurrectionCities(iClaimant, secedingCities)
			resurrectionFromCollapse(iClaimant, claimedCities + additionalCities)
		
		# else cities go to minors
		else:
			lMinorCities.extend(claimedCities)
	
	# secede remaining cities to minors
	lPossibleMinors = getPossibleMinors(iPlayer)
	for iMinor, minorCities in cities.of(lMinorCities).divide(lPossibleMinors):
		for city in minorCities:
			secedeCity(city, iMinor, not bComplete, iArmyPercent)
		
	# notify for partial secessions
	if not bComplete and player().canContact(iPlayer):
		message(active(), 'TXT_KEY_STABILITY_CITIES_SECEDED', fullname(iPlayer), len(secedingCities))
	
	# prevent collapsing downward spiral
	balanceStability(iPlayer, iStabilityUnstable)
		
def secedeCity(city, iNewOwner, bRelocate, iArmyPercent):
	if not city: return
	
	name = city.getName()
	iOldOwner = city.getOwner()
	tile = location(city)
	
	if player(iNewOwner).isMinorCiv():
		for iPlayer in players.major().at_war(city):
			if not team(iPlayer).isAtWar(player(iNewOwner).getTeam()):
				team(iPlayer).declareWar(player(iNewOwner).getTeam(), True, WarPlanTypes.WARPLAN_LIMITED)
	
	iNumDefenders = max(2, player(iNewOwner).getCurrentEra()-1)
	lFlippedUnits, lRelocatedUnits = flipOrRelocateGarrison(city, iNumDefenders)
	
	if bRelocate:
		relocateUnitsToCore(city.getOwner(), lRelocatedUnits, iArmyPercent)
	else:
		killUnits(lRelocatedUnits)
	
	completeCityFlip(city, iNewOwner, city.getOwner(), 50, False, True, True)
	flipOrCreateDefenders(iNewOwner, lFlippedUnits, tile, iNumDefenders)
	
	if is_minor(iNewOwner):
		message(iOldOwner, 'TXT_KEY_STABILITY_CITY_INDEPENDENCE', name, color=iRed)
	else:
		message(iOldOwner, 'TXT_KEY_STABILITY_CITY_CHANGED_OWNER', name, adjective(iNewOwner), color=iRed)
		
	message(iNewOwner, 'TXT_KEY_STABILITY_CITY_CHANGED_OWNER_US', name, color=iRed)
	
def completeCollapse(iPlayer):
	# before cities are seceded, downgrade their cottages
	downgradeCottages(iPlayer)
	
	# secede all cities, destroy close and less important ones
	bRazeMinorCities = (player(iPlayer).getCurrentEra() <= iMedieval)
	secedeCities(iPlayer, cities.owner(iPlayer), bRazeMinorCities)
		
	# take care of the remnants of the civ
	player(iPlayer).killUnits()
	vic.resetAll(iPlayer)
		
	message(active(), 'TXT_KEY_STABILITY_COMPLETE_COLLAPSE', adjective(iPlayer))
	
	events.fireEvent("collapse", iPlayer)
		
def collapseToCore(iPlayer):
	nonCoreCities = cities.owner(iPlayer).where(lambda city: not plot(city).isCore(iPlayer))
	ahistoricalCities = nonCoreCities.where(lambda city: plot(city).getSettlerValue(iPlayer) < 90)
				
	# more than half ahistorical, only secede ahistorical cities
	if 2 * ahistoricalCities.count() > nonCoreCities.count():
	
		# notify owner
		message(iPlayer, 'TXT_KEY_STABILITY_FOREIGN_SECESSION', color=iRed)
				
		# secede all foreign cities
		secession(iPlayer, ahistoricalCities)
		
	# otherwise, secede all cities outside of core
	elif nonCoreCities:
	
		# notify owner
		message(iPlayer, 'TXT_KEY_STABILITY_COLLAPSE_TO_CORE', color=iRed)
			
		# secede all non-core cities
		secession(iPlayer, nonCoreCities)

def domesticCrisis(iPlayer):
	data.players[iPlayer].bDomesticCrisis = True

	iStability = data.players[iPlayer].iLastStability
	iStabilityThreshold = determineStabilityThreshold(iPlayer, iStabilityCollapsing)
	
	iStabilityDifference = iStabilityThreshold - iStability
	if iStabilityDifference >= 0:
		iCrisisTurns = turns(1 + iStabilityDifference / 5)
		
		player(iPlayer).changeAnarchyTurns(iCrisisTurns)
		
		for city in cities.owner(iPlayer):
			city.changeOccupationTimer(iCrisisTurns)
			
		message(iPlayer, 'TXT_KEY_STABILITY_DOMESTIC_CRISIS', iCrisisTurns, color=iRed)
		
def downgradeCottages(iPlayer):
	for plot in plots.all().owner(iPlayer):
		iImprovement = plot.getImprovementType()
		
		if iImprovement == iTown: plot.setImprovementType(iHamlet)
		elif iImprovement == iVillage: plot.setImprovementType(iCottage)
		elif iImprovement == iHamlet: plot.setImprovementType(iCottage)
		elif iImprovement == iCottage: plot.setImprovementType(-1)
		
		# Destroy all Harappan improvements
		if civ(iPlayer) == iHarappa and not player(iPlayer).isHuman():
			if iImprovement >= 0:
				plot.setImprovementType(-1)
				
	message(iPlayer, 'TXT_KEY_STABILITY_DOWNGRADE_COTTAGES', color=iRed)

def calculateAdministration(city):
	iPlayer = city.getOwner()

	if not city.isCore(iPlayer):
		return 0
	
	iPopulation = city.getPopulation()
	iCurrentEra = player(iPlayer).getCurrentEra()
	iAdministrationModifier = getAdministrationModifier(iCurrentEra)
	
	bSingleCoreCity = cities.core(iPlayer).owner(iPlayer).count() == 1

	iAdministration = iAdministrationModifier * iPopulation / 100
	if bSingleCoreCity and iCurrentEra > iAncient: 
		iAdministration *= 2
	
	return iAdministration
	
def getSeparatismModifier(iPlayer, city):
	iModifier = 0
	
	iCiv = civ(iPlayer)
	
	plot = city.plot()
	civic = civics(iPlayer)
	
	bHistorical = plot.getSettlerValue(iPlayer) >= 90
	bTotalitarianism = civic.iSociety == iTotalitarianism
	bExpansionExceptions = (bHistorical and iCiv == iMongols) or bTotalitarianism
	
	iTotalCulture = players.major().sum(lambda p: plot.isCore(p) and 2 * plot.getCulture(p) or plot.getCulture(p))
	iCulturePercent = iTotalCulture != 0 and 100 * plot.getCulture(iPlayer) / iTotalCulture or 0
	
	# ahistorical tiles
	if not bHistorical:
		iModifier += 2
	
	# colonies with Totalitarianism
	if city.isColony() and bHistorical and civic.iGovernment == iTotalitarianism:
		iModifier += 1
		
	# not original owner
	if not bExpansionExceptions:
		if city.getOriginalOwner() != iPlayer and since(city.getGameTurnAcquired()) < turns(25):
			iModifier += 1
	
	# not majority culture
	if iCiv != iPersia:
		if iCulturePercent < 50: iModifier += 1
		if iCulturePercent < 20: iModifier += 1
	
	# Courthouse
	if city.hasBuilding(unique_building(iPlayer, iCourthouse)):
		iModifier -= 1
	
	# Jail
	if city.hasBuilding(unique_building(iPlayer, iJail)):
		iModifier -= 1
	
	# overseas colonies with Portuguese UP and Colonialism
	if city.isColony():
		if iCiv == iPortugal: iModifier -= 2
		if civic.iTerritory == iColonialism and bHistorical: iModifier -= 1
	
	# cap
	if iModifier < -1: iModifier = -1
	
	return 100 + iModifier * 50

def calculateSeparatism(city):
	iPlayer = city.getOwner()

	if city.isCore(iPlayer):
		return 0
	
	iModifier = getSeparatismModifier(iPlayer, city)
	iPopulation = city.getPopulation()
	
	if city.isOccupation():
		iPopulation -= city.getPopulationLoss() * city.getOccupationTimer()
	
	return iModifier * iPopulation / 100

def calculateStability(iPlayer):
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iCiv = civ(iPlayer)

	iExpansionStability = 0
	iEconomyStability = 0
	iDomesticStability = 0
	iForeignStability = 0
	iMilitaryStability = 0
	
	lParameters = [0 for i in range(iNumStabilityParameters)]
	
	# Collect required data
	iStateReligion = pPlayer.getStateReligion()
	iCurrentEra = pPlayer.getCurrentEra()
	iTotalPopulation = pPlayer.getTotalPopulation()
	iPlayerScore = pPlayer.getScoreHistory(turn())
	
	iCivicGovernment = pPlayer.getCivics(0)
	iCivicLegitimacy = pPlayer.getCivics(1)
	iCivicSociety = pPlayer.getCivics(2)
	iCivicEconomy = pPlayer.getCivics(3)
	iCivicReligion = pPlayer.getCivics(4)
	iCivicTerritory = pPlayer.getCivics(5)
	
	iTotalCoreCities = 0
	iOccupiedCoreCities = 0
	
	iRecentlyFounded = 0
	iRecentlyConquered = 0
	
	iStateReligionPopulation = 0
	iOnlyStateReligionPopulation = 0
	iDifferentReligionPopulation = 0
	iNoReligionPopulation = 0
	
	bTotalitarianism = iCivicSociety == iTotalitarianism
	bFreeEnterprise = iCivicEconomy == iFreeEnterprise
	bPublicWelfare = iCivicEconomy == iPublicWelfare
	bTheocracy = iCivicReligion == iTheocracy
	bTolerance = iCivicReligion == iTolerance
	bConquest = iCivicTerritory == iConquest
	bTributaries = iCivicTerritory == iTributaries
	bIsolationism = iCivicTerritory == iIsolationism
	bColonialism = iCivicTerritory == iColonialism
	bNationhood = iCivicTerritory == iNationhood
	bMultilateralism = iCivicTerritory == iMultilateralism
	
	iAdministration = cities.owner(iPlayer).sum(calculateAdministration) + 10
	iSeparatism = cities.owner(iPlayer).sum(calculateSeparatism)
	
	for city in cities.owner(iPlayer):
		iPopulation = city.getPopulation()
		bHistorical = city.plot().getSettlerValue(iPlayer) >= 90
		
		# Recent conquests
		if bHistorical and since(city.getGameTurnAcquired()) <= turns(20):
			if city.getPreviousOwner() < 0:
				iRecentlyFounded += 1
			else:
				iRecentlyConquered += 1
			
		# Religions
		if city.getReligionCount() == 0:
			iNoReligionPopulation += iPopulation
		else:
			bNonStateReligion = False
			for iReligion in range(iNumReligions):
				if iReligion != iStateReligion and city.isHasReligion(iReligion):
					if not isTolerated(iPlayer, iReligion) and not gc.getReligionInfo(iReligion).isLocal():
						bNonStateReligion = True
						break

			if iStateReligion >= 0 and city.isHasReligion(iStateReligion):
				iStateReligionPopulation += iPopulation
				if not bNonStateReligion: iOnlyStateReligionPopulation += iPopulation
					
			if bNonStateReligion: 
				if iStateReligion >= 0 and city.isHasReligion(iStateReligion): iDifferentReligionPopulation += iPopulation / 2
				else: iDifferentReligionPopulation += iPopulation
				
	iAdministrationImprovements = plots.core(iPlayer).owner(iPlayer).where(lambda plot: plot.getWorkingCity() and plot.getImprovementType() in [iVillage, iTown]).count()
	iAdministration += getAdministrationModifier(iCurrentEra) * iAdministrationImprovements / 100
	
	iCurrentPower = pPlayer.getPower()
	iPreviousPower = pPlayer.getPowerHistory(since(turns(10)))
	
	# EXPANSION
	iExpansionStability = 0
	
	iCorePeripheryStability = 0
	iRecentExpansionStability = 0
	iRazeCityStability = 0
	
	# Core vs. Periphery Populations
	iSeparatismExcess = 100 * iSeparatism / iAdministration - 100
	
	if iSeparatismExcess > 200: iSeparatismExcess = 200
		
	if iSeparatismExcess > 0:
		iSeparatismExcess -= int(25 * sigmoid(1.0 * iSeparatismExcess / 100))
		
	lParameters[iParameterCorePeriphery] = iCorePeripheryStability
	lParameters[iParameterAdministration] = iAdministration
	lParameters[iParameterSeparatism] = iSeparatism
		
	iExpansionStability += iCorePeripheryStability
	
	# recent expansion stability
	iConquestModifier = 1
	if bConquest: iConquestModifier += 1
	if iCiv == iPersia: iConquestModifier += 1 # Persian UP
	
	iRecentExpansionStability += iRecentlyFounded
	iRecentExpansionStability += iConquestModifier * iRecentlyConquered
		
	lParameters[iParameterRecentExpansion] = iRecentExpansionStability
	
	iExpansionStability += iRecentExpansionStability
	
	# apply raze city penalty
	iRazeCityStability = data.iHumanRazePenalty
	
	lParameters[iParameterRazedCities] = iRazeCityStability
		
	iExpansionStability += iRazeCityStability
	
	# stability if not expanded beyond core with isolationism
	iIsolationismStability = 0
	
	if bIsolationism and iSeparatism <= 10:
		iIsolationismStability = 10
		
	lParameters[iParameterIsolationism] = iIsolationismStability
	
	iExpansionStability += iIsolationismStability
	
	# ECONOMY
	iEconomyStability = 0
	
	# Economic Growth
	iEconomicGrowthModifier = 3
	if bFreeEnterprise: iEconomicGrowthModifier = 4
	
	iEconomicGrowthStability = iEconomicGrowthModifier * calculateTrendScore(data.players[iPlayer].lEconomyTrend)
	if iEconomicGrowthStability < 0 and bPublicWelfare: iEconomicGrowthStability /= 2
	
	lParameters[iParameterEconomicGrowth] = iEconomicGrowthStability
	iEconomyStability += iEconomicGrowthStability
	
	iTradeStability = 0
	
	lParameters[iParameterTrade] = iTradeStability
	iEconomyStability += iTradeStability
					
	# DOMESTIC
	iDomesticStability = 0
	
	# Happiness
	iHappinessStability = calculateTrendScore(data.players[iPlayer].lHappinessTrend)
	
	if iHappinessStability > 5: iHappinessStability = 5
	if iHappinessStability < -5: iHappinessStability = -5
	
	if not player(iPlayer).isHuman() and iHappinessStability < 0:
		iHappinessStability *= 2
		iHappinessStability /= 3
	
	lParameters[iParameterHappiness] = iHappinessStability
	
	iDomesticStability += iHappinessStability
	
	# Civics (combinations)
	civics = (iCivicGovernment, iCivicLegitimacy, iCivicSociety, iCivicEconomy, iCivicReligion, iCivicTerritory)
	iCivicCombinationStability = getCivicStability(iPlayer, civics)
		
	if not player(iPlayer).isHuman() and iCivicCombinationStability < 0: iCivicCombinationStability /= 2
	
	lParameters[iParameterCivicCombinations] = iCivicCombinationStability
	
	iCivicEraTechStability = 0
	
	# Civics (eras and techs and religions)
	# note: make sure to reflect this in CvPlayerAI::isUnstableCivic
	if iCivicLegitimacy == iVassalage:
		if iCurrentEra == iMedieval: iCivicEraTechStability += 2
		elif iCurrentEra >= iIndustrial: iCivicEraTechStability -= 5
		
	if iCivicReligion == iDeification:
		if iCurrentEra <= iClassical: iCivicEraTechStability += 2
		else: iCivicEraTechStability -= 2 * (iCurrentEra - iClassical)
		
	if iCivicGovernment == iRepublic:
		if iCurrentEra <= iClassical: iCivicEraTechStability += 2
		elif iCurrentEra >= iIndustrial: iCivicEraTechStability -= 5
		
	if iCivicTerritory == iIsolationism:
		if iCurrentEra >= iIndustrial: iCivicEraTechStability -= (iCurrentEra - iRenaissance) * 3
		
	if tPlayer.isHasTech(iRepresentation):
		if iCivicGovernment not in [iRepublic, iDemocracy] and iCivicLegitimacy not in [iRevolutionism, iConstitution]: iCivicEraTechStability -= 5
		
	if tPlayer.isHasTech(iCivilRights):
		if iCivicSociety in [iSlavery, iManorialism, iCasteSystem]: iCivicEraTechStability -= 5
		
	if tPlayer.isHasTech(iEconomics):
		if iCivicEconomy in [iReciprocity, iRedistribution, iMerchantTrade]: iCivicEraTechStability -= 5
		
	if tPlayer.isHasTech(iNationalism):
		if iCivicTerritory in [iNationalism, iMultilateralism]: iCivicEraTechStability += 5
		if iCivicTerritory in [iConquest, iTributaries]: iCivicEraTechStability -= 5
		
	if tPlayer.isHasTech(iDoctrine):
		if iCivicReligion in [iAnimism, iDeification]: iCivicEraTechStability -= 5
	
	if tPlayer.isHasTech(iStatecraft):
		if iCivicLegitimacy not in [iAuthority, iCitizenship, iVassalage]: iCivicEraTechStability += 5
	
	if iStateReligion == iHinduism:
		if iCivicSociety == iCasteSystem: iCivicEraTechStability += 3
		
	elif iStateReligion == iConfucianism:
		if iCivicLegitimacy == iMeritocracy: iCivicEraTechStability += 3
		
	elif iStateReligion in [iZoroastrianism, iOrthodoxy, iCatholicism, iProtestantism]:
		if iCivicSociety == iSlavery: iCivicEraTechStability -= 3
		
	elif iStateReligion == iIslam:
		if iCivicSociety == iSlavery: iCivicEraTechStability += 2
		
	elif iStateReligion == iBuddhism:
		if iCivicReligion == iMonasticism: iCivicEraTechStability += 2
		
	elif iStateReligion == iConfucianism:
		if iCivicTerritory == iIsolationism: iCivicEraTechStability += 3
		
	if not player(iPlayer).isHuman() and iCivicEraTechStability < 0: iCivicEraTechStability /= 2
	
	lParameters[iParameterCivicsEraTech] = iCivicEraTechStability
	
	iDomesticStability += iCivicCombinationStability + iCivicEraTechStability
	
	# Religion
	iReligionStability = 0
	
	if iTotalPopulation > 0:
		iHeathenRatio = 100 * iDifferentReligionPopulation / iTotalPopulation
		iHeathenThreshold = 30
		iBelieverThreshold = 75
		
		if iHeathenRatio > iHeathenThreshold:
			iReligionStability -= (iHeathenRatio - iHeathenThreshold) / 10
			
		if iStateReligion >= 0:
			iStateReligionRatio = 100 * iStateReligionPopulation / iTotalPopulation
			iNoReligionRatio = 100 * iNoReligionPopulation / iTotalPopulation
			
			iBelieverRatio = iStateReligionRatio - iBelieverThreshold
			if iBelieverRatio < 0: iBelieverRatio = min(0, iBelieverRatio + iNoReligionRatio)
			iBelieverStability = iBelieverRatio / 5
			
			# cap at -10 for threshold = 75
			iCap = 2 * (iBelieverThreshold - 100) / 5
			if iBelieverStability < iCap: iBelieverStability = iCap
			
			if iBelieverStability > 0 and bTolerance: iBelieverStability /= 2
			
			iReligionStability += iBelieverStability
			
			if bTheocracy:
				iOnlyStateReligionRatio = 100 * iOnlyStateReligionPopulation / iTotalPopulation
				iReligionStability += iOnlyStateReligionRatio / 20
	
	lParameters[iParameterReligion] = iReligionStability
		
	iDomesticStability += iReligionStability
	
	# FOREIGN
	iForeignStability = 0
	iVassalStability = 0
	iDefensivePactStability = 0
	iRelationStability = 0
	iNationhoodStability = 0
	iTheocracyStability = 0
	iMultilateralismStability = 0
	
	iNumContacts = 0
	iFriendlyRelations = 0
	iFuriousRelations = 0
	
	lContacts = []
	
	for iLoopPlayer in players.major():
		pLoopPlayer = player(iLoopPlayer)
		tLoopPlayer = team(iLoopPlayer)
		iLoopScore = pLoopPlayer.getScoreHistory(turn())
		
		if iLoopPlayer == iPlayer: continue
		if not pLoopPlayer.isAlive(): continue
				
		# master stability
		if tPlayer.isVassal(iLoopPlayer):
			if stability(iPlayer) > stability(iLoopPlayer):
				iVassalStability += 4 * (stability(iPlayer) - stability(iLoopPlayer))
				
		# vassal stability
		if tLoopPlayer.isVassal(iPlayer):
			if stability(iLoopPlayer) == iStabilityCollapsing: iVassalStability -= 3
			elif stability(iLoopPlayer) == iStabilityUnstable: iVassalStability -= 1
			elif stability(iLoopPlayer) == iStabilitySolid: iVassalStability += 2
			
			if bTributaries: iVassalStability += 2
			
		# relations
		if tPlayer.canContact(iLoopPlayer):
			lContacts.append(iLoopPlayer)
			
		# defensive pacts
		if tPlayer.isDefensivePact(iLoopPlayer):
			if iLoopScore > iPlayerScore: iDefensivePactStability += 3
			if bMultilateralism: iDefensivePactStability += 3
		
		# worst enemies
		if pLoopPlayer.getWorstEnemy() == iPlayer:
			if iLoopScore > iPlayerScore: iRelationStability -= 3
			
		# wars
		if tPlayer.isAtWar(iLoopPlayer):
			if bMultilateralism: iMultilateralismStability -= 2
			
			if isNeighbor(iPlayer, iLoopPlayer):
				if bNationhood: iNationhoodStability += 2
				
				if bTheocracy:
					if pLoopPlayer.getStateReligion() != iStateReligion: iTheocracyStability += 3
					else: iTheocracyStability -= 2
		
	# attitude stability
	lStrongerAttitudes, lEqualAttitudes, lWeakerAttitudes = calculateRankedAttitudes(iPlayer, lContacts)
	
	iAttitudeThresholdModifier = pPlayer.getCurrentEra() / 2
	
	iRelationStronger = 0
	iPositiveStronger = count(lStrongerAttitudes, lambda x: x >= 4 + iAttitudeThresholdModifier * 2)
	if iPositiveStronger > len(lStrongerAttitudes) / 2:
		iRelationStronger = 5 * iPositiveStronger / max(1, len(lStrongerAttitudes))
		iRelationStronger = min(iRelationStronger, len(lStrongerAttitudes))
	
	iRelationWeaker = 0
	iNegativeWeaker = max(0, count(lWeakerAttitudes, lambda x: x < -1) - count(lWeakerAttitudes, lambda x: x >= 3 + iAttitudeThresholdModifier))
	
	if iNegativeWeaker > 0:
		iRelationWeaker = -8 * min(iNegativeWeaker, len(lWeakerAttitudes) / 2) / max(1, len(lWeakerAttitudes) / 2)
		iRelationWeaker = max(iRelationWeaker, -len(lWeakerAttitudes))
		
	iRelationEqual = sum(sign(iAttitude) * min(25, abs(iAttitude) / 5) for iAttitude in lEqualAttitudes if abs(iAttitude) > 2)

	iRelationStability = iRelationStronger + iRelationEqual + iRelationWeaker
		
	if bIsolationism:
		if iRelationStability < 0: iRelationStability = 0
		if iRelationStability > 0: iRelationStability /= 2
	
	if not player(iPlayer).isHuman():
		if iRelationStability < 0:
			iRelationStability /= 2
	
	lParameters[iParameterVassals] = iVassalStability
	lParameters[iParameterDefensivePacts] = iDefensivePactStability
	lParameters[iParameterRelations] = iRelationStability
	lParameters[iParameterNationhood] = iNationhoodStability
	lParameters[iParameterTheocracy] = iTheocracyStability
	lParameters[iParameterMultilateralism] = iMultilateralismStability
			
	iForeignStability += iVassalStability + iDefensivePactStability + iRelationStability + iNationhoodStability + iTheocracyStability + iMultilateralismStability
	
	# MILITARY
	
	iMilitaryStability = 0
	
	iWarSuccessStability = 0
	iMilitaryStrengthStability = 0
	iBarbarianLossesStability = 0
	
	iWarSuccessStability = 0 # war success (conquering cities and defeating units)
	iWarWearinessStability = 0 # war weariness in comparison to war length
	iBarbarianLossesStability = 0 # like previously
	
	# iterate ongoing wars
	for iEnemy in players.major().alive():
		pEnemy = player(iEnemy)
		if tPlayer.isAtWar(iEnemy):
			iTempWarSuccessStability = calculateTrendScore(data.players[iPlayer].lWarTrend[iEnemy])
			
			iOurSuccess = tPlayer.AI_getWarSuccess(iEnemy)
			iTheirSuccess = team(iEnemy).AI_getWarSuccess(iPlayer)
			
			if iTempWarSuccessStability > 0 and iTheirSuccess > iOurSuccess: iTempWarSuccessStability /= 2
			elif iTempWarSuccessStability < 0 and iOurSuccess > iTheirSuccess: iTempWarSuccessStability /= 2
			
			if iTempWarSuccessStability > 0: iTempWarSuccessStability /= 2
			
			iWarSuccessStability += iTempWarSuccessStability
			
			iOurWarWeariness = tPlayer.getWarWeariness(iEnemy)
			iTheirWarWeariness = team(iEnemy).getWarWeariness(iPlayer)
			
			iWarTurns = turn() - data.players[iPlayer].lWarStartTurn[iEnemy]
			iDurationModifier = 0
			
			if iWarTurns > turns(20):
				iDurationModifier = min(9, (iWarTurns - turns(20)) / turns(10))
				
			iTempWarWearinessStability = (iTheirWarWeariness - iOurWarWeariness) / (4000 * (iDurationModifier + 1))
			if iTempWarWearinessStability > 0: iTempWarWearinessStability = 0
			
			iWarWearinessStability += iTempWarWearinessStability
			
			debug(pPlayer.getCivilizationAdjective(0) + ' war against ' + pEnemy.getCivilizationShortDescription(0) + '\nWar Success Stability: ' + str(iTempWarSuccessStability) + '\nWar Weariness: ' + str(iTempWarWearinessStability))
	
	lParameters[iParameterWarSuccess] = iWarSuccessStability
	lParameters[iParameterWarWeariness] = iWarWearinessStability
	
	iMilitaryStability = iWarSuccessStability + iWarWearinessStability
	
	# apply barbarian losses
	iBarbarianLossesStability = -data.players[iPlayer].iBarbarianLosses
	
	lParameters[iParameterBarbarianLosses] = iBarbarianLossesStability
	
	iMilitaryStability += iBarbarianLossesStability
	
	iStability = iExpansionStability + iEconomyStability + iDomesticStability + iForeignStability + iMilitaryStability
	
	return iStability, [iExpansionStability, iEconomyStability, iDomesticStability, iForeignStability, iMilitaryStability], lParameters
	
def getCivicStability(iPlayer, lCivics):
	civics = Civics(lCivics)

	iCurrentEra = player(iPlayer).getCurrentEra()
	iStability = 0
	
	if iTotalitarianism in civics:
		if iStateParty in civics: iStability += 5
		if iDespotism in civics: iStability += 3
		if iRevolutionism in civics: iStability += 3
		if iCentralPlanning in civics: iStability += 3
		if iDemocracy in civics: iStability -= 3
		if iConstitution in civics: iStability -= 5
		if iSecularism in civics: iStability += 2
		if civics.any(iTolerance, iMonasticism): iStability -= 3
		
	if iCentralPlanning in civics:
		if iEgalitarianism in civics: iStability += 2
		if iStateParty in civics: iStability += 2
		if iCentralism in civics: iStability += 2
		
	if iEgalitarianism in civics:
		if iDemocracy in civics: iStability += 2
		if iConstitution in civics: iStability += 2
		if civics.no(iSecularism) and civics.no(iTolerance): iStability -= 3
		
	if iIndividualism in civics:
		if civics.any(iRepublic, iDemocracy): iStability += 2
		if iFreeEnterprise in civics: iStability += 3
		if iCentralPlanning in civics: iStability -= 5
		if civics.any(iRegulatedTrade, iPublicWelfare): iStability -= 2
		if iTolerance in civics: iStability += 2
		
	if iTheocracy in civics:
		if civics.any(iIndividualism, iEgalitarianism): iStability -= 3
		
	if iDeification in civics:
		if civics.any(iRepublic, iDemocracy): iStability -= 3
		
		if iCurrentEra <= iClassical:
			if iRedistribution in civics: iStability += 2
			if iSlavery in civics: iStability += 2
		
	if iVassalage in civics:
		if civics.any(iIndividualism, iEgalitarianism): iStability -= 5
		if civics.any(iFreeEnterprise, iCentralPlanning, iPublicWelfare): iStability -= 3
		if iTributaries in civics: iStability += 5
		
		if iCurrentEra == iMedieval:
			if iMonarchy in civics: iStability += 2
			if iManorialism in civics: iStability += 3
			
	if iRepublic in civics:
		if iCitizenship in civics: iStability += 2
		if iVassalage in civics: iStability -= 3
		if iMerchantTrade in civics: iStability += 2
		
	if iCentralism in civics:
		if iDemocracy in civics: iStability -= 5
		if iRegulatedTrade in civics: iStability += 3
		if iClergy in civics: iStability += 2
		
		if iCurrentEra == iRenaissance:
			if iMonarchy in civics: iStability += 2
			
	if iDespotism in civics:
		if iSlavery in civics: iStability += 2
		if iNationhood in civics: iStability += 3
		
	if iCasteSystem in civics:
		if iCitizenship in civics: iStability -= 4
		if iClergy in civics: iStability += 2
		if iSecularism in civics: iStability -= 3
		
	if iMultilateralism in civics:
		if iDespotism in civics: iStability -= 3
		if iTotalitarianism in civics: iStability -= 3
		if iEgalitarianism in civics: iStability += 2
		if iTheocracy in civics: iStability -= 3
		
	if iMonarchy in civics:
		if civics.any(iClergy, iMonasticism): iStability += 2
		
	if iElective in civics:
		if iCentralism in civics: iStability -= 5
		
	if iConstitution in civics:
		if iDemocracy in civics: iStability += 2
		
	if iRevolutionism in civics:
		if civics.no(iSecularism) and civics.no(iTolerance): iStability -= 3
		
	if iRegulatedTrade in civics:
		if iManorialism in civics: iStability += 2
		if iMeritocracy in civics: iStability += 3
		
	if iIsolationism in civics:
		if civics.any(iMerchantTrade, iFreeEnterprise): iStability -= 4
		if civics.any(iRegulatedTrade, iCentralPlanning): iStability += 3
		if iMeritocracy in civics: iStability += 3
		
	return iStability
	
def only(lCombination, *civics):
	lCivics = [iCivic for iCivic in civics]
	return set(lCivics) & lCombination
	
def other(lCombination, *civics):
	iCategory = gc.getCivicInfo(civics[0]).getCivicOptionType()
	lCivics = [iCivic for iCivic in range(iNumCivics) if gc.getCivicInfo(iCivic).getCivicOptionType() == iCategory and iCivic not in civics]
	return set(lCivics) & lCombination

def sigmoid(x):
	return math.tanh(5 * x / 2)
	
def count(iterable, function = lambda x: True):
	return len([element for element in iterable if function(element)])
	
def calculateTrendScore(lTrend):
	iPositive = 0
	iNeutral = 0
	iNegative = 0
	
	for iEntry in lTrend:
		if iEntry > 0: iPositive += 1
		elif iEntry < 0: iNegative += 1
		else: iNeutral += 1
		
	if iPositive > iNegative: return max(0, iPositive - iNegative - iNeutral / 2)
	
	if iNegative > iPositive: return min(0, iPositive - iNegative + iNeutral / 2)
	
	return 0
	
def calculateSumScore(lScores, iThreshold = 1):
	lThresholdScores = [sign(iScore) for iScore in lScores if abs(iScore) >= iThreshold]
	iSum = sum(lThresholdScores)
	iCap = len(lScores) / 2
	
	if abs(iSum) > iCap: iSum = sign(iSum) * iCap
	
	return iSum
	
def updateEconomyTrend(iPlayer):
	pPlayer = player(iPlayer)
	
	if not pPlayer.isAlive(): return
	
	iPreviousCommerce = data.players[iPlayer].iPreviousCommerce
	iCurrentCommerce = pPlayer.calculateTotalCommerce()
	
	if iPreviousCommerce == 0: 
		data.players[iPlayer].iPreviousCommerce = iCurrentCommerce
		return
	
	iCivicEconomy = pPlayer.getCivics(3)
		
	iPositiveThreshold = 5
	iNegativeThreshold = 0
	
	if isDecline(iPlayer):
		iNegativeThreshold = 2
	
	if iCivicEconomy == iCentralPlanning: iNegativeThreshold = 0
	
	iPercentChange = 100 * iCurrentCommerce / iPreviousCommerce - 100
	
	if iPercentChange > iPositiveThreshold: data.players[iPlayer].pushEconomyTrend(1)
	elif iPercentChange < iNegativeThreshold: data.players[iPlayer].pushEconomyTrend(-1)
	else: data.players[iPlayer].pushEconomyTrend(0)
	
	data.players[iPlayer].iPreviousCommerce = iCurrentCommerce
	
def updateHappinessTrend(iPlayer):
	pPlayer = player(iPlayer)
	
	if not pPlayer.isAlive(): return
	
	iNumCities = pPlayer.getNumCities()
	
	if iNumCities == 0: return
	
	iHappyCities = 0
	iUnhappyCities = 0
	
	iAveragePopulation = pPlayer.getAveragePopulation()
	
	for city in cities.owner(iPlayer):
		iPopulation = city.getPopulation()
		iHappiness = city.happyLevel()
		iUnhappiness = city.unhappyLevel(0)
		iOvercrowding = city.getOvercrowdingPercentAnger(0) * city.getPopulation() / 1000
		
		if city.isWeLoveTheKingDay() or (iPopulation >= iAveragePopulation and iHappiness - iUnhappiness >= iAveragePopulation / 4):
			iHappyCities += 1
		elif iUnhappiness - iOvercrowding > iPopulation / 5 or iUnhappiness - iHappiness > 0:
			iUnhappyCities += 1
			
	iCurrentTrend = 0
			
	if iHappyCities - iUnhappyCities > math.ceil(iNumCities / 5.0): iCurrentTrend = 1
	elif iUnhappyCities - iHappyCities > math.ceil(iNumCities / 5.0): iCurrentTrend = -1
	
	data.players[iPlayer].pushHappinessTrend(iCurrentTrend)
	
def updateWarTrend(iPlayer, iEnemy):
	iOurCurrentSuccess = team(iPlayer).AI_getWarSuccess(iEnemy)
	iTheirCurrentSuccess = team(iEnemy).AI_getWarSuccess(iPlayer)
	
	iOurLastSuccess = data.players[iPlayer].lLastWarSuccess[iEnemy]
	iTheirLastSuccess = data.players[iEnemy].lLastWarSuccess[iPlayer]
	
	iOurGain = max(0, iOurCurrentSuccess - iOurLastSuccess)
	iTheirGain = max(0, iTheirCurrentSuccess - iTheirLastSuccess)
	
	if iOurGain - iTheirGain > 0:
		iCurrentTrend = 1
	elif iOurGain - iTheirGain < 0:
		iCurrentTrend = -1
	elif abs(iOurCurrentSuccess - iTheirCurrentSuccess) >= max(iOurCurrentSuccess, iTheirCurrentSuccess) / 5:
		iCurrentTrend = sign(iOurCurrentSuccess - iTheirCurrentSuccess)
	else:
		iCurrentTrend = 0
	
	data.players[iPlayer].pushWarTrend(iEnemy, iCurrentTrend)
	
def startWar(iPlayer, iEnemy):
	data.players[iPlayer].lWarTrend[iEnemy] = []
	data.players[iEnemy].lWarTrend[iPlayer] = []
	
	data.players[iPlayer].lWarStartTurn[iEnemy] = turn()
	data.players[iEnemy].lWarStartTurn[iPlayer] = turn()
	
def calculateCommerceRank(iPlayer, iTurn):
	return players.major().rank(iPlayer, lambda p: player(p).getEconomyHistory(iTurn))
	
def calculatePowerRank(iPlayer, iTurn):
	return players.major().rank(iPlayer, lambda p: player(p).getPowerHistory(iTurn))
	
def calculateRankedAttitudes(iPlayer, lContacts):
	lContacts.append(iPlayer)
	lContacts = sort(lContacts, lambda p: gc.getGame().getPlayerScore(iPlayer), True)
	iPlayerIndex = lContacts.index(iPlayer)
	
	iRangeSize = 4
	if iPlayerIndex <= len(lContacts) / 5:
		iRangeSize = 3
	
	iRange = len(lContacts) / iRangeSize
	iLeft = max(0, iPlayerIndex - iRange/2)
	iRight = min(iLeft + iRange, len(lContacts)-1)
	
	lStronger = [calculateAttitude(iLoopPlayer, iPlayer) for iLoopPlayer in lContacts[:iLeft] if iLoopPlayer != iPlayer]
	lEqual = [calculateAttitude(iLoopPlayer, iPlayer) for iLoopPlayer in lContacts[iLeft:iRight] if iLoopPlayer != iPlayer]
	lWeaker = [calculateAttitude(iLoopPlayer, iPlayer) for iLoopPlayer in lContacts[iRight:] if iLoopPlayer != iPlayer]
	
	return lStronger, lEqual, lWeaker
	
def calculateAttitude(iFromPlayer, iToPlayer):
	pPlayer = player(iFromPlayer)

	iAttitude = pPlayer.AI_getAttitudeVal(iToPlayer)
	iAttitude -= pPlayer.AI_getSameReligionAttitude(iToPlayer)
	iAttitude -= pPlayer.AI_getDifferentReligionAttitude(iToPlayer)
	iAttitude -= pPlayer.AI_getFirstImpressionAttitude(iToPlayer)
	
	return iAttitude
	
def isTolerated(iPlayer, iReligion):
	pPlayer = player(iPlayer)
	iStateReligion = pPlayer.getStateReligion()
	
	# should not be asked, but still check
	if iStateReligion == iReligion: return True
	
	# civics
	if pPlayer.getCivics(4) in [iTolerance, iSecularism]: return True
	
	# Exceptions
	if iStateReligion == iConfucianism and iReligion == iTaoism: return True
	if iStateReligion == iTaoism and iReligion == iConfucianism: return True
	if iStateReligion == iHinduism and iReligion == iBuddhism: return True
	if iStateReligion == iBuddhism and iReligion == iHinduism: return True
	
	# Poland
	lChristianity = [iOrthodoxy, iCatholicism, iProtestantism]
	if civ(iPlayer) == iPoland and iStateReligion in lChristianity and iReligion in lChristianity: return True
	
	return False

@handler("BeginGameTurn")
def checkResurrection():
	if every(10):
		iNationalismModifier = min(20, 4 * data.iPlayersWithNationalism)
		possibleResurrections = players.major().where(canRespawn).sort(lambda p: data.players[p].iLastTurnAlive)
		
		# civs entirely controlled by minors will always respawn
		for iPlayer in possibleResurrections:
			if cities.respawn(iPlayer).all(lambda city: is_minor(city)):
				resurrectionCities = getResurrectionCities(iPlayer)
				if canResurrectFromCities(iPlayer, resurrectionCities):
					doResurrection(iPlayer, resurrectionCities)
					return
					
		# otherwise minimum amount of cities and random chance are required
		for iPlayer in possibleResurrections:
			if rand(100) - iNationalismModifier + 10 < dResurrectionProbability[iPlayer]:
				resurrectionCities = getResurrectionCities(iPlayer)
				if canResurrectFromCities(iPlayer, resurrectionCities):
					doResurrection(iPlayer, resurrectionCities)
					return
					
def isPartOfResurrection(iPlayer, city, bOnlyOne):
	iOwner = city.getOwner()
	
	# for humans: not for recently conquered cities to avoid annoying reflips
	if iOwner == active() and city.getGameTurnAcquired() > turn() - turns(5):
		return False
		
	# barbarian and minor cities always flip
	if is_minor(iOwner):
		return True
		
	# not if their core but not our core
	if city.isCore(iOwner) and not city.isCore(iPlayer):
		return False
		
	iOwnerStability = stability(iOwner)
	bCapital = city.atPlot(plots.respawnCapital(iPlayer))
	
	# flips are less likely before Nationalism
	if data.iPlayersWithNationalism == 0:
		iOwnerStability += 1
	
	# flips are more likely between AIs to make the world more dynamic
	if not player(iOwner).isHuman() and not player(iPlayer).isHuman():
		iOwnerStability -= 1
	
	# if unstable or worse, all cities flip
	if iOwnerStability <= iStabilityUnstable:
		return True
	
	# if shaky, only the prospective capital, colonies or core cities that are not our core flip
	if iOwnerStability <= iStabilityShaky:
		if bCapital or (city.isCore(iPlayer) and not city.isCore(iOwner)) or city.isColony():
			return True
	
	# if stable, only the prospective capital flips
	if iOwnerStability <= iStabilityStable:
		if bCapital and not bOnlyOne:
			return True
			
	return False
						
def getResurrectionCities(iPlayer, bFromCollapse = False):
	potentialCities = cities.respawn(iPlayer)
	resurrectionCities = potentialCities.where(lambda city: isPartOfResurrection(iPlayer, city, len(potentialCities) == 1))

	# if capital exists and not part of the resurrection, it fails, unless from collapse
	capital = cities.respawnCapital(iPlayer)
	if not bFromCollapse and capital and capital not in resurrectionCities:
		return []
	
	# if existing cities sufficient for resurrection and close to including all potential cities, include the rest as well, unless from collapse
	if not bFromCollapse and canResurrectFromCities(iPlayer, resurrectionCities):
		if resurrectionCities.count() + 2 >= potentialCities.count() and resurrectionCities.count() * 2 >= potentialCities.count():
			resurrectionCities += potentialCities.where(lambda city: not city.isCore(city.getOwner()))
			resurrectionCities = resurrectionCities.unique()
		
	# let civs keep at least two cities
	for iOwner in resurrectionCities.owners():
		iNumCities = cities.owner(iOwner).count()
		iNumFlippedCities = resurrectionCities.owner(iOwner).count()
		if iNumCities - iNumFlippedCities < 2:
			retainedCities = resurrectionCities.owner(iOwner).highest(2 - (iNumCities - iNumFlippedCities), lambda city: (city.isCapital(), city.plot().getSettlerValue(iOwner)))
			resurrectionCities = resurrectionCities.without(retainedCities)
	
	return resurrectionCities.entities()
	
def resurrectionFromCollapse(iPlayer, lCityList):
	debug('Resurrection: %s', name(iPlayer))
			
	if lCityList:
		doResurrection(iPlayer, lCityList, bAskFlip=False)
	
def doResurrection(iPlayer, lCityList, bAskFlip=True, bDisplay=False):
	pPlayer = player(iPlayer)
	teamPlayer = team(iPlayer)
	iCiv = civ(iPlayer)
	
	pPlayer.setAlive(True)

	data.iRebelCiv = iPlayer
	
	for iOtherPlayer in players.major().without(iPlayer):
		teamPlayer.makePeace(iOtherPlayer)
		
		if teamPlayer.isVassal(iOtherPlayer):
			team(iOtherPlayer).freeVassal(iPlayer)
			
		if team(iOtherPlayer).isVassal(iPlayer):
			teamPlayer.freeVassal(iOtherPlayer)
		
	data.players[iPlayer].iNumPreviousCities = 0
	
	pPlayer.AI_reset()
	
	# reset player espionage weight
	player().setEspionageSpendingWeightAgainstTeam(pPlayer.getTeam(), 0)
			
	# assign technologies
	lTechs = getResurrectionTechs(iPlayer)
	for iTech in lTechs:
		teamPlayer.setHasTech(iTech, True, iPlayer, False, False)
		
	# determine army size
	iNumCities = len(lCityList)
	iGarrison = 2
	iArmySize = pPlayer.getCurrentEra()
	
	pPlayer.setLastBirthTurn(turn())
		
	# add former colonies that are still free
	for city in players.minor().alive().cities().where(lambda city: city.getOriginalOwner() == iPlayer):
		if pPlayer.getSettlerValue(city.getX(), city.getY()) >= 90:
			if city not in lCityList:
				lCityList.append(city)

	lOwners = []
	dRelocatedUnits = {}
	
	# determine prevalent religion in the resurrection area
	iNewStateReligion = getPrevalentReligion(plots.of(lCityList))
	
	for city in lCityList:
		iOwner = city.getOwner()
		pOwner = player(iOwner)
		
		x = city.getX()
		y = city.getY()
		
		bCapital = city.isCapital()
		
		iNumDefenders = max(2, player(iPlayer).getCurrentEra()-1)
		lFlippedUnits, lRelocatedUnits = flipOrRelocateGarrison(city, iNumDefenders)
		
		if iOwner in dRelocatedUnits:
			dRelocatedUnits[iOwner].extend(lRelocatedUnits)
		else:
			dRelocatedUnits[iOwner] = lRelocatedUnits
		
		if pOwner.isBarbarian() or pOwner.isMinorCiv():
			completeCityFlip(city, iPlayer, iOwner, 100, False, True, True, True)
		else:
			completeCityFlip(city, iPlayer, iOwner, 75, False, True, True)
			
		flipOrCreateDefenders(iPlayer, lFlippedUnits, (x, y), iNumDefenders)
			
		newCity = city_(x, y)
		
		# Leoreth: rebuild some city infrastructure
		for iBuilding in range(iNumBuildings):
			if pPlayer.canConstruct(iBuilding, True, False, False) and newCity.canConstruct(iBuilding, True, False, False) and pPlayer.getCurrentEra() >= gc.getBuildingInfo(iBuilding).getFreeStartEra() and not isGreatBuilding(iBuilding) and gc.getBuildingInfo(iBuilding).getPrereqReligion() == -1:
				newCity.setHasRealBuilding(iBuilding, True)
			
		if bCapital and not is_minor(iOwner):
			relocateCapital(iOwner, cities.capital(iOwner))
			
		if iOwner not in lOwners:
			lOwners.append(iOwner)
			
	for iOwner in dRelocatedUnits:
		if not is_minor(iOwner):
			relocateUnitsToCore(iOwner, dRelocatedUnits[iOwner])
		else:
			killUnits(dRelocatedUnits[iOwner])
			
	for iOwner in lOwners:
		teamOwner = team(iOwner)
		bOwnerHumanVassal = teamOwner.isVassal(active())
	
		if not player(iOwner).isHuman() and iOwner != iPlayer and not player(iOwner).isBarbarian():
			if rand(100) >= dAIStopBirthThreshold[iOwner] and not bOwnerHumanVassal:
				teamOwner.declareWar(iPlayer, False, -1)
			else:
				teamOwner.makePeace(iPlayer)
			
	relocateCapital(iPlayer, cities.respawnCapital(iPlayer))
	
	# give the new civ a starting army
	capital = pPlayer.getCapitalCity()
	
	makeUnits(iPlayer, getBestInfantry(iPlayer), capital, 2 * iArmySize + iNumCities)
	makeUnits(iPlayer, getBestCavalry(iPlayer), capital, iArmySize)
	makeUnits(iPlayer, getBestCounter(iPlayer), capital, iArmySize)
	makeUnits(iPlayer, getBestSiege(iPlayer), capital, iArmySize + iNumCities)
	
	# set state religion based on religions in the area
	if iNewStateReligion >= 0:
		pPlayer.setLastStateReligion(iNewStateReligion)
	
	switchCivics(iPlayer)
		
	message(active(), 'TXT_KEY_INDEPENDENCE_TEXT', adjective(iPlayer), color=iGreen, force=True)
	
	if bAskFlip and active() in lOwners:
		rebellionPopup(iPlayer)
		
	setStabilityLevel(iPlayer, iStabilityStable)
	
	data.players[iPlayer].iPlagueCountdown = -10
	clearPlague(iPlayer)
	convertBackCulture(iPlayer)
	
	# resurrection leaders
	if iCiv in dResurrectionLeaders:
		if pPlayer.getLeader() != dResurrectionLeaders[iCiv]:
			pPlayer.setLeader(dResurrectionLeaders[iCiv])
	
	if bDisplay:
		plot(capital).cameraLookAt()
	
	events.fireEvent("resurrection", iPlayer)
	
def getResurrectionTechs(iPlayer):
	pPlayer = player(iPlayer)
	lTechList = []
	lSourcePlayers = []
	
	# same tech group
	for lRegionList in dTechGroups.values():
		if iPlayer in lRegionList:
			for iPeer in lRegionList:
				if iPeer != iPlayer and player(iPeer).isAlive():
					lSourcePlayers.append(iPeer)
			
	# direct neighbors (India can benefit from England etc)
	for iPeer in players.major().alive().without(iPlayer).without(lSourcePlayers):
		if isNeighbor(iPlayer, iPeer):
			lSourcePlayers.append(iPeer)
				
	# use independents as source civs in case no other can be found
	if not lSourcePlayers:
		lSourcePlayers += players.independent().entities()
		
	for iTech in range(iNumTechs):
			
		# at least half of the source civs know this technology
		iCount = 0
		for iOtherPlayer in lSourcePlayers:
			if team(iOtherPlayer).isHasTech(iTech):
				iCount += 1
				
		if 2 * iCount >= len(lSourcePlayers):
			lTechList.append(iTech)
			
	return lTechList

def convertBackCulture(iPlayer):
	for plot in plots.respawn(iPlayer):
		city = city_(plot)
		if city:
			if city.getOwner() == iPlayer:
				iCulture = 0
				for iMinor in players.minor():
					iCulture += city.getCulture(iMinor)
					city.setCulture(iMinor, 0, True)
				city.changeCulture(iPlayer, iCulture, True)
		elif plot.isCityRadius() and plot.getOwner() == iPlayer:
			iCulture = 0
			for iMinor in players.minor():
				iCulture += plot.getCulture(iMinor)
				plot.setCulture(iMinor, 0, True)
			plot.changeCulture(iPlayer, iCulture, True)
		
def switchCivics(iPlayer):
	pPlayer = player(iPlayer)

	for iCategory in range(iNumCivicCategories):
		iBestCivic = pPlayer.AI_bestCivic(iCategory)
		
		if iBestCivic >= 0:
			pPlayer.setCivics(iCategory, iBestCivic)
			
	pPlayer.setRevolutionTimer(gc.getDefineINT("MIN_REVOLUTION_TURNS"))

def rebellionPopup(iRebelCiv):
	eventpopup(7622, text("TXT_KEY_REBELLION_TITLE"), text("TXT_KEY_REBELLION_TEXT", adjective(iRebelCiv)), (text("TXT_KEY_POPUP_YES"), text("TXT_KEY_POPUP_NO")))
	
def getAdministrationModifier(iEra):
	return tEraAdministrationModifier[iEra]
	
def balanceStability(iPlayer, iNewStabilityLevel):
	debug("Balance stability: %s", name(iPlayer))

	playerData = data.players[iPlayer]
	
	# set stability to at least the specified level
	setStabilityLevel(iPlayer, max(iNewStabilityLevel, stability(iPlayer)))

	# prevent collapse if they were going to
	playerData.iTurnsToCollapse = -1
	
	# update number of cities so vassals survive losing cities
	playerData.iNumPreviousCities = player(iPlayer).getNumCities()
	
	# reset previous commerce
	playerData.iPreviousCommerce = 0
	
	# reset war, economy and happiness trends to give them a breather
	playerData.resetEconomyTrend()
	playerData.resetHappinessTrend()
	playerData.resetWarTrends()
	
def isDecline(iPlayer):
	return not player(iPlayer).isHuman() and year() >= year(dFall[iPlayer])
	
class Civics:

	def __init__(self, lActiveCivics):
		self.activeCivics = set(lActiveCivics)
		
	def __contains__(self, civic):
		return civic in self.activeCivics
		
	def any(self, *civics):
		return self.activeCivics & set([civic for civic in civics])
		
	def no(self, civic):
		if gc.getCivicInfo(civic).getCivicOptionType() not in [gc.getCivicInfo(i).getCivicOptionType() for i in self.activeCivics]: return False
		return not self.any(civic)

		