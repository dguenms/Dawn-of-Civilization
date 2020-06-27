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

tEraCorePopulationModifiers = (
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
			data.players[iPlayer].iTurnsToCollapse = -1
			completeCollapse(iPlayer)
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
		data.iHumanStability = calculateStability(active())


@handler("EndPlayerTurn")
def checkSecedingCities(iGameTurn, iPlayer):
	lSecedingCities = data.getSecedingCities(iPlayer)
	
	if lSecedingCities:
		secedeCities(iPlayer, lSecedingCities)
		data.setSecedingCities(iPlayer, [])
		
def triggerCollapse(iPlayer):
	# help overexpanding AI: collapse to core, unless fall date
	if not player(iPlayer).isHuman():
		if gc.getGame().getGameTurnYear() < dFall[iPlayer]:
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

@handler("palaceMoved")
def onPalaceMoved(city):
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

	doResurrection(iReleasedPlayer, releasedCities, False)
	
	player(iReleasedPlayer).AI_changeAttitudeExtra(iPlayer, 2)
	
def onCivSpawn(iPlayer):
	for iOlderNeighbor in players.civs(dNeighbours[iPlayer]):
		if player(iOlderNeighbor).isAlive() and stability(iOlderNeighbor) > iStabilityShaky:
			decrementStability(iOlderNeighbor)
	
def setStabilityLevel(iPlayer, iStabilityLevel):
	data.setStabilityLevel(iPlayer, iStabilityLevel)
	
	if iStabilityLevel == iStabilityCollapsing:
		message(iPlayer, 'TXT_KEY_STABILITY_COLLAPSING_WARNING', color=iRed)
	
def incrementStability(iPlayer):
	data.setStabilityLevel(iPlayer, min(iStabilitySolid, stability(iPlayer) + 1))
	
def decrementStability(iPlayer):
	data.setStabilityLevel(iPlayer, max(iStabilityCollapsing, stability(iPlayer) - 1))
	
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
	if turn() < pPlayer.getInitialBirthTurn() + turn(20):
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
		completeCollapse(iPlayer)
		
	# lost at least two cities to barbarians: lose stability
	elif iLostCities >= 2:
		debug('Lost stability to barbarians: ' + pPlayer.getCivilizationShortDescription(0))
		decrementStability(iPlayer)
		
def checkLostCitiesCollapse(iPlayer):
	pPlayer = player(iPlayer)
	
	if isImmune(iPlayer): return
		
	iNumCurrentCities = pPlayer.getNumCities()
	iNumPreviousCities = data.players[iPlayer].iNumPreviousCities
	
	# half or less cities than 12 turns ago: collapse (exceptions for civs with very little cities to begin with -> use lost core collapse)
	if iNumPreviousCities > 2 and 2 * iNumCurrentCities <= iNumPreviousCities:
	
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
	
		debug('Collapse from lost core: ' + pPlayer.getCivilizationShortDescription(0))
		scheduleCollapse(iPlayer)
	
def determineStabilityLevel(iCurrentLevel, iStability, bFall = False):
	iThreshold = 10 * iCurrentLevel - 10
	
	if bFall: iThreshold += 10
	
	if iStability >= iThreshold: return min(iStabilitySolid, iCurrentLevel + 1)
	elif bFall: return max(iStabilityCollapsing, iCurrentLevel - (iThreshold - iStability) / 10)
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
	
	iNewStabilityLevel = determineStabilityLevel(iStabilityLevel, iStability, bFall)
	
	if iNewStabilityLevel > iStabilityLevel:
		data.setStabilityLevel(iPlayer, iNewStabilityLevel)
		
	elif not bPositive:
		# if remain on collapsing and stability does not improve, collapse ensues
		if iNewStabilityLevel == iStabilityCollapsing:
			if iStability <= data.players[iPlayer].iLastStability:
				triggerCollapse(iPlayer)
		
		if iNewStabilityLevel < iStabilityLevel:
			data.setStabilityLevel(iPlayer, iNewStabilityLevel)
		
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
	
def secession(iPlayer, lCities):
	data.setSecedingCities(iPlayer, lCities)
	
def secedeCities(iPlayer, lCities, bRazeMinorCities = False):
	iCiv = civ(iPlayer)

	lPossibleMinors = getPossibleMinors(iPlayer)
	dPossibleResurrections = appenddict()
	
	bComplete = len(lCities) == player(iPlayer).getNumCities()
	
	clearPlague(iPlayer)
	
	# if smaller cities are supposed to be destroyed, do that first
	lCededCities = []
	lRemovedCities = []
	lRelocatedUnits = []
	
	for city in lCities:
		if bRazeMinorCities:
			bMaxPopulation = (city.getPopulation() < 10)
			bMaxCulture = (city.getCultureLevel() < 3)
			bNoHolyCities = (not city.isHolyCity())
			bNoCapitals = (not city.isCapital())
			bNotJerusalem = (not (city.getX() == 73 and city.getY() == 38))
			
			if bMaxPopulation and bMaxCulture and bNoHolyCities and bNoCapitals and bNotJerusalem:
				closest = closestCity(city, iPlayer, same_continent=True)
				
				if closest:
					if distance(city, closest) <= 2:
						bCulture = (city.getCultureLevel() <= closest.getCultureLevel())
						bPopulation = (city.getPopulation() < closest.getPopulation())
						
						if bCulture and bPopulation:
							lRemovedCities.append(city)
							continue
							
			# always raze Harappan cities
			if iCiv == iHarappa and not player(iPlayer).isHuman():
				lRemovedCities.append(city)
				continue
						
		lCededCities.append(city)
			
	for city in lRemovedCities:
		plot = city.plot()
		player(iBarbarian).disband(city)
		plot.setCulture(iPlayer, 0, True)
	
	for city in lCededCities:
		cityPlot = plot_(city)
	
		# three possible behaviors: if living civ has a claim, assign it to them
		# claim based on core territory
		iClaim = -1
		for iLoopPlayer in players.major():
			if iLoopPlayer == iPlayer: continue
			if player(iLoopPlayer).isHuman(): continue
			if not year().between(year(dBirth[iLoopPlayer]), year(dFall[iLoopPlayer])): continue
			if cityPlot.isCore(iLoopPlayer) and player(iLoopPlayer).isAlive():
				iClaim = iLoopPlayer
				debug('Secede ' + adjective(iPlayer) + ' ' + city.getName() + ' to ' + name(iClaim) + '.\nReason: core territory.')
				break
		
		# claim based on original owner
		if iClaim == -1:
			iOriginalOwner = city.getOriginalOwner()
			if cityPlot.getSettlerValue(iOriginalOwner) >= 90 and not cityPlot.isCore(iPlayer) and not cityPlot in plots.birth(iCiv) and player(iOriginalOwner).isAlive() and iOriginalOwner != iPlayer and active() != iOriginalOwner:
				if not is_minor(iOriginalOwner) and year() < year(dFall[iOriginalOwner]):
					# cities lost too long ago don't return
					if city.getGameTurnPlayerLost(iOriginalOwner) >= turn() - turns(25):
						iClaim = iOriginalOwner
						debug('Secede ' + adjective(iPlayer) + ' ' + city.getName() + ' to ' + name(iClaim) + '.\nReason: original owner.')
				
		# claim based on culture
		if iClaim == -1:
			for iLoopPlayer in players.major():
				if iLoopPlayer == iPlayer: continue
				if player(iLoopPlayer).isHuman(): continue
				if not year().between(year(dBirth[iLoopPlayer]), year(dFall[iLoopPlayer])): continue
				if player(iLoopPlayer).isAlive():
					iTotalCulture = cityPlot.countTotalCulture()
					if iTotalCulture > 0:
						iCulturePercent = 100 * cityPlot.getCulture(iLoopPlayer) / cityPlot.countTotalCulture()
						if iCulturePercent >= 75:
							iClaim = iLoopPlayer
							debug('Secede ' + adjective(iPlayer) + ' ' + city.getName() + ' to ' + name(iClaim) + '.\nReason: culture.')
							break
						
		# claim based on war target (needs to be winning the war based on war success)
		if iClaim == -1:
			tPlayer = team(iPlayer)
			for iLoopPlayer in players.major().alive().alive():
				pLoopPlayer = player(iLoopPlayer)
				if tPlayer.isAtWar(iLoopPlayer) and year() < year(dFall[iLoopPlayer]):
					if pLoopPlayer.getWarValue(city.getX(), city.getY()) >= 8 and team(iLoopPlayer).AI_getWarSuccess(iPlayer) > tPlayer.AI_getWarSuccess(iLoopPlayer):
						# another enemy with closer city: don't claim the city
						closest = closestCity(city, same_continent=True)
						if not closest or closest.getOwner() != iLoopPlayer and tPlayer.isAtWar(closest.getOwner()): continue
						iClaim = iLoopPlayer
						debug('Secede ' + adjective(iPlayer) + ' ' + city.getName() + ' to ' + name(iClaim) + '.\nReason: war target.')
						break
						
		if iClaim != -1:
			secedeCity(city, iClaim, not is_minor(iPlayer) and not bComplete)
			continue

		# if part of the core / resurrection area of a dead civ -> possible resurrection
		bResurrectionFound = False
		for iLoopPlayer in players.major():
			if iLoopPlayer == iPlayer: continue
			if player(iLoopPlayer).isAlive(): continue
			if not data.players[iLoopPlayer].bSpawned: continue
			if turn() - data.players[iLoopPlayer].iLastTurnAlive < turns(20): continue
			
			# Leoreth: Egyptian respawn on Arabian collapse hurts Ottoman expansion
			if iCiv == iArabia and civ(iLoopPlayer) == iEgypt: continue

			if city in cities.respawn(iLoopPlayer):
				bPossible = False
				
				if any(year().between(iStart, iEnd) for iStart, iEnd in dResurrections[iLoopPlayer]):
					bPossible = True
						
				# make respawns on collapse more likely
				if dBirth[iLoopPlayer] <= gc.getGame().getGameTurnYear() <= dFall[iLoopPlayer]:
					bPossible = True
				
				if bPossible:
					dPossibleResurrections[iLoopPlayer].append(city)
					bResurrectionFound = True
					debug(adjective(iPlayer) + ' ' + city.getName() + ' is part of the ' + adjective(iLoopPlayer) + ' resurrection.')
					break
				
		if bResurrectionFound: continue

		# assign randomly to possible minors
		print "Possible minors: %s" % [name(iMinor) for iMinor in lPossibleMinors]
		secedeCity(city, lPossibleMinors[city.getID() % len(lPossibleMinors)], not is_minor(iPlayer) and not bComplete)
		
	# notify for partial secessions
	if not bComplete:
		if player().canContact(iPlayer):
			message(active(), 'TXT_KEY_STABILITY_CITIES_SECEDED', fullname(iPlayer), len(lCededCities))
		
	# collect additional cities that can be part of the resurrection
	lCededTiles = [(city.getX(), city.getY()) for city in lCededCities]
	for iResurrectionPlayer in dPossibleResurrections:
		for city in getResurrectionCities(iResurrectionPlayer, True):
			if (city.getX(), city.getY()) not in lCededTiles:
				dPossibleResurrections[iResurrectionPlayer].append(city)

	# execute possible resurrections
	for iResurrectionPlayer in dPossibleResurrections:
		debug('Resurrection: ' + name(iResurrectionPlayer))
		resurrectionFromCollapse(iResurrectionPlayer, dPossibleResurrections[iResurrectionPlayer])
		
	if len(lCities) > 1:
		balanceStability(iPlayer, iStabilityUnstable)
		
def secedeCity(city, iNewOwner, bRelocate):
	if not city: return
	
	if player(iNewOwner).isMinorCiv():
		for iPlayer in players.at_war(city):
			if not team(iPlayer).isAtWar(player(iNewOwner).getTeam()):
				team(iPlayer).declareWar(player(iNewOwner).getTeam(), True, WarPlanTypes.WARPLAN_LIMITED)
	
	iNumDefenders = max(2, player(iNewOwner).getCurrentEra()-1)
	lFlippedUnits, lRelocatedUnits = flipOrRelocateGarrison(city, iNumDefenders)
	
	if bRelocate:
		relocateUnitsToCore(city.getOwner(), lRelocatedUnits)
	else:
		killUnits(lRelocatedUnits)
	
	completeCityFlip(city, iNewOwner, city.getOwner(), 50, False, True, True)
	flipOrCreateDefenders(iNewOwner, lFlippedUnits, city, iNumDefenders)
	
	if is_minor(iNewOwner):
		message(city.getOwner(), 'TXT_KEY_STABILITY_CITY_INDEPENDENCE', city.getName(), color=iRed)
	else:
		message(city.getOwner(), 'TXT_KEY_STABILITY_CITY_CHANGED_OWNER', city.getName(), adjective(iNewOwner), color=iRed)
		
	message(iNewOwner, 'TXT_KEY_STABILITY_CITY_CHANGED_OWNER_US', city.getName(), color=iRed)
	
def completeCollapse(iPlayer):
	# before cities are seceded, downgrade their cottages
	downgradeCottages(iPlayer)
	
	# secede all cities, destroy close and less important ones
	bRazeMinorCities = (player(iPlayer).getCurrentEra() <= iMedieval)
	secedeCities(iPlayer, cities.owner(iPlayer), bRazeMinorCities)
		
	# take care of the remnants of the civ
	player(iPlayer).killUnits()
	vic.resetAll(iPlayer)
	data.players[iPlayer].iLastTurnAlive = turn()
		
	# special case: Byzantine collapse: remove Christians in the Turkish core
	if civ(iPlayer) == iByzantium:
		removeReligionByArea(plots.core(iOttomans), iOrthodoxy)
	
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
	
	iCorePopulation = 10
	iPeripheryPopulation = 10
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
	
	bSingleCoreCity = cities.core(iPlayer).owner(iPlayer).count() == 1
	
	iCorePopulationModifier = getCorePopulationModifier(iCurrentEra)
	
	for city in cities.owner(iPlayer):
		iPopulation = city.getPopulation()
		iModifier = 0
		plot = plot_(city)
		
		bHistorical = (plot.getSettlerValue(iPlayer) >= 90)
		
		iTotalCulture = 0
		
		# Expansion
		if plot.isCore(iPlayer):
			iStabilityPopulation = iCorePopulationModifier * iPopulation / 100
			if bSingleCoreCity and iCurrentEra > iAncient: iStabilityPopulation += iCorePopulationModifier * iPopulation / 100
			
			iCorePopulation += iStabilityPopulation
			city.setStabilityPopulation(iStabilityPopulation)
		else:
			iOwnCulture = plot.getCulture(iPlayer)
			
			for iLoopPlayer in players.major():
				iTempCulture = plot.getCulture(iLoopPlayer)
				if plot.isCore(iLoopPlayer):
					iTempCulture *= 2
				iTotalCulture += iTempCulture
				
			if iTotalCulture != 0:
				iCulturePercent = 100 * iOwnCulture / iTotalCulture
			else:
				iCulturePercent = 100
					
			bExpansionExceptions = ((bHistorical and iCiv == iMongols) or bTotalitarianism)
		
			# ahistorical tiles
			if not bHistorical: iModifier += 2
			
			# colonies with Totalitarianism
			if city.isColony() and bHistorical and bTotalitarianism: iModifier += 1
			
			# not original owner
			if not bExpansionExceptions:
				if city.getOriginalOwner() != iPlayer and turn() - city.getGameTurnAcquired() < turns(25): iModifier += 1
			
			# not majority culture (includes foreign core and Persian UP)
			if iCiv != iPersia:
				if iCulturePercent < 50: iModifier += 1
				if iCulturePercent < 20: iModifier += 1
			
			# Courthouse
			if city.hasBuilding(unique_building(iPlayer, iCourthouse)): iModifier -= 1
			
			# Jail
			if city.hasBuilding(unique_building(iPlayer, iJail)): iModifier -= 1
			
			# Portuguese UP: reduced instability from overseas colonies
			if city.isColony():
				if iCiv == iPortugal: iModifier -= 2
				if bColonialism and bHistorical: iModifier -= 1
					
			# cap
			if iModifier < -1: iModifier = -1
			
			iStabilityPopulation = (100 + iModifier * 50) * iPopulation / 100
			
			iPeripheryPopulation += iStabilityPopulation
			city.setStabilityPopulation(-iStabilityPopulation)
			
		# Recent conquests
		if bHistorical and turn() - city.getGameTurnAcquired() <= turns(20):
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
		
	iPopulationImprovements = 0
	for plot in plots.core(iCiv):
		if plot.getOwner() == iPlayer and plot.getWorkingCity():
			if plot.getImprovementType() in [iVillage, iTown]:
				iPopulationImprovements += 1
			
	iCorePopulation += iCorePopulationModifier * iPopulationImprovements / 100
	
	iCurrentPower = pPlayer.getPower()
	iPreviousPower = pPlayer.getPowerHistory(turn() - turns(10))
	
	# EXPANSION
	iExpansionStability = 0
	
	iCorePeripheryStability = 0
	iRecentExpansionStability = 0
	iRazeCityStability = 0
	
	# Core vs. Periphery Populations
	if iCorePopulation == 0:
		iPeripheryExcess = 200
	else:
		iPeripheryExcess = 100 * iPeripheryPopulation / iCorePopulation - 100
	
	if iPeripheryExcess > 200: iPeripheryExcess = 200
		
	if iPeripheryExcess > 0:
		iCorePeripheryStability -= int(25 * sigmoid(1.0 * iPeripheryExcess / 100))
		
		debug('Expansion rating: ' + pPlayer.getCivilizationShortDescription(0) + '\nCore population: ' + str(iCorePopulation) + '\nPeriphery population: ' + str(iPeripheryPopulation) + '\nExpansion stability: ' + str(iCorePeripheryStability))
		
	lParameters[iParameterCorePeriphery] = iCorePeripheryStability
	lParameters[iParameterCoreScore] = iCorePopulation
	lParameters[iParameterPeripheryScore] = iPeripheryPopulation
		
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
	
	if bIsolationism and iPeripheryPopulation <= 10:
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
	
	iTotalCommerce = pPlayer.calculateTotalCommerce()
					
	# DOMESTIC
	iDomesticStability = 0
	
	# Happiness
	iHappinessStability = calculateTrendScore(data.players[iPlayer].lHappinessTrend)
	
	if iHappinessStability > 5: iHappinessStability = 5
	if iHappinessStability < -5: iHappinessStability = -5
	
	lParameters[iParameterHappiness] = iHappinessStability
	
	iDomesticStability += iHappinessStability
	
	# Civics (combinations)
	civics = (iCivicGovernment, iCivicLegitimacy, iCivicSociety, iCivicEconomy, iCivicReligion, iCivicTerritory)
	iCivicCombinationStability = getCivicStability(iPlayer, civics)
		
	if not player(iPlayer).isHuman() and iCivicCombinationStability < 0: iCivicCombinationStability /= 2
	
	lParameters[iParameterCivicCombinations] = iCivicCombinationStability
	
	iCivicEraTechStability = 0
	
	# Civics (eras and techs and religions)
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
		if iCivicTerritory in [iConquest, iTributaries]: iCivicEraTechStability -= 5
		
	if tPlayer.isHasTech(iTheology):
		if iCivicReligion in [iAnimism, iDeification]: iCivicEraTechStability -= 5
	
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
			if turn() < data.players[iPlayer].iLastTurnAlive + turns(15):
				continue
			
			if cities.respawn(iPlayer).all(lambda city: is_minor(city)):
				resurrectionCities = getResurrectionCities(iPlayer)
				if resurrectionCities:
					doResurrection(iPlayer, resurrectionCities)
					return
					
		# otherwise minimum amount of cities and random chance are required
		for iPlayer in possibleResurrections:
			if turn() < data.players[iPlayer].iLastTurnAlive + turns(15):
				continue
			
			iMinNumCities = 2
				
			if rand(100) - iNationalismModifier + 10 < dResurrectionProbability[iPlayer]:
				resurrectionCities = getResurrectionCities(iPlayer)
				if len(resurrectionCities) >= iMinNumCities or len(resurrectionCities) >= len(cities.respawn(iPlayer)):
					doResurrection(iPlayer, resurrectionCities)
					return
						
def getResurrectionCities(iPlayer, bFromCollapse = False):
	pPlayer = player(iPlayer)
	teamPlayer = team(iPlayer)
	iCiv = civ(iPlayer)
	
	lPotentialCities = []
	lFlippingCities = []
	
	tCapital = plots.respawnCapital(iCiv)
	
	for city in cities.respawn(iCiv):
		# for humans: exclude recently conquered cities to avoid annoying reflips
		if city.getOwner() != active() or city.getGameTurnAcquired() < turn() - turns(5):
			lPotentialCities.append(city)
					
	for city in lPotentialCities:
		iOwner = city.getOwner()
		iMinNumCitiesOwner = 3
		
		# barbarian and minor cities always flip
		if is_minor(iOwner):
			lFlippingCities.append(city)
			continue
			
		iOwnerStability = stability(iOwner)
		bCapital = (location(city) == tCapital)
		
		# flips are less likely before Nationalism
		if data.iPlayersWithNationalism == 0:
			iOwnerStability += 1
			
		if not player(iOwner).isHuman():
			iMinNumCitiesOwner = 2
			iOwnerStability -= 1
			
		if player(iOwner).getNumCities() >= iMinNumCitiesOwner:
		
			# special case for civs returning from collapse: be more strict
			if bFromCollapse:
				if iOwnerStability < iStabilityShaky:
					lFlippingCities.append(city)
				continue
		
			# owner stability below shaky: city always flips
			if iOwnerStability < iStabilityShaky:
				lFlippingCities.append(city)
				
			# owner stability below stable: city flips if far away from their capital, or is capital spot of the dead civ
			elif iOwnerStability < iStabilityStable:
				ownerCapital = player(iOwner).getCapitalCity()
				iDistance = distance(city, ownerCapital)
				if bCapital or iDistance >= 8:
					lFlippingCities.append(city)
				
			# owner stability below solid: only capital spot flips
			elif iOwnerStability < iStabilitySolid:
				if bCapital:
					lFlippingCities.append(city)
					
	# if capital exists and does not flip, the respawn fails
	if city_(tCapital):
		if tCapital not in [location(city) for city in lFlippingCities]:
			return []
					
	# if only up to two cities wouldn't flip, they flip as well (but at least one city has to flip already, else the respawn fails)
	if len(lFlippingCities) + 2 >= len(lPotentialCities) and len(lFlippingCities) > 0 and len(lFlippingCities) * 2 >= len(lPotentialCities) and not bFromCollapse:
		# cities in core are not affected by this
		for city in lPotentialCities:
			if not city.plot().isCore(city.getOwner()) and city not in lFlippingCities:
				lFlippingCities.append(city)
			
	return lFlippingCities
	
def resurrectionFromCollapse(iPlayer, lCityList):
	if lCityList:
		doResurrection(iPlayer, lCityList)
	
def doResurrection(iPlayer, lCityList, bAskFlip = True):
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
	iNewStateReligion = getPrevalentReligion(plots.of(lCityList))
	
	if iNewStateReligion >= 0:
		pPlayer.setLastStateReligion(iNewStateReligion)
	
	switchCivics(iPlayer)
		
	message(active(), 'TXT_KEY_INDEPENDENCE_TEXT', adjective(iPlayer), color=iGreen, force=True)
	
	if bAskFlip and active() in lOwners:
		rebellionPopup(iPlayer)
		
	data.setStabilityLevel(iPlayer, iStabilityStable)
	
	data.players[iPlayer].iPlagueCountdown = -10
	clearPlague(iPlayer)
	convertBackCulture(iPlayer)
	
	# change the cores of some civs on respawn
	periods.onResurrection(iPlayer)
	
	# resurrection leaders
	if iCiv in dResurrectionLeaders:
		if pPlayer.getLeader() != dResurrectionLeaders[iCiv]:
			pPlayer.setLeader(dResurrectionLeaders[iCiv])
			
	# Leoreth: report to dynamic civs
	dc.onCivRespawn(iPlayer, lOwners)
	
	return
	
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
	eventpopup(7622, text("TXT_KEY_REBELLION_TITLE"), text("TXT_KEY_REBELLION_TEXT", adjective(iRebelCiv)), text("TXT_KEY_POPUP_YES"), text("TXT_KEY_POPUP_NO"))
			
def sign(x):
	if x > 0: return 1
	elif x < 0: return -1
	else: return 0
	
def getCorePopulationModifier(iEra):
	return tEraCorePopulationModifiers[iEra]
	
def balanceStability(iPlayer, iNewStabilityLevel):
	debug("Balance stability: %s" % name(iPlayer))

	playerData = data.players[iPlayer]
	
	# set stability to at least the specified level
	data.setStabilityLevel(iPlayer, max(iNewStabilityLevel, stability(iPlayer)))

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

		