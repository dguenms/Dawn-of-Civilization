from Core import *
from RFCUtils import *
from Civics import *
from Resurrection import *
from Secession import *
from Collapse import *

from Slots import findSlot
from Events import handler, events

from operator import itemgetter
from datetime import date

import Periods as periods
import Logging as log

import BugPath

import math


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
				data.players[iPlayer].iBarbarianLosses -= 1 + data.players[iPlayer].iBarbarianLosses / 5


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
		if not data.players[iPlayer].bDomesticCrisis and data.players[iPlayer].lStabilityCategoryValues[0] >= 0:
			domesticCrisis(iPlayer)
			return
		
		# collapse to core if controlling cities outside of core
		if cities.core(iPlayer).owner(iPlayer) < cities.owner(iPlayer):
			collapseToCore(iPlayer)
			return

	scheduleCollapse(iPlayer)

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
	iOwner = slot(Civ(city.getPreviousCiv()))
	if iOwner < 0:
		return 
	
	if player(iOwner).isBarbarian():
		return

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
	if not pPlayer.isExisting():
		return True
		
	# only for major civs
	if is_minor(iPlayer):
		return True
		
	# immune right after scenario start
	if turn() < scenarioStartTurn() + turns(20):
		return True
		
	# immune if birth protected
	if pPlayer.isBirthProtected():
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
	iLostCities = cities.owner(iBarbarian).where(lambda city: city.isOriginalOwner(iPlayer)).count()
			
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

def calculateAdministration(city):
	iPlayer = city.getOwner()

	if not city.isPlayerCore(iPlayer):
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
	
	bHistorical = plot.getPlayerSettlerValue(iPlayer) > 0
	bFall = since(year(dFall[iPlayer])) >= 0
	bTotalitarianism = civic.iSociety == iTotalitarianism
	bExpansionExceptions = (bHistorical and iCiv == iMongols and not bFall) or bTotalitarianism
	
	iTotalCulture = civs.major().sum(lambda c: plot.isCore(c) and 2 * plot.getCivCulture(c) or plot.getCivCulture(c))
	iCulturePercent = iTotalCulture != 0 and 100 * plot.getCulture(iPlayer) / iTotalCulture or 0
	
	# ahistorical tiles
	if not bHistorical:
		iModifier += 2
	
	# colonies with Totalitarianism
	if city.isColony() and bHistorical and civic.iGovernment == iTotalitarianism:
		iModifier += 1
		
	# not original owner
	if not bExpansionExceptions:
		if not city.isOriginalOwner(iPlayer) and since(city.getGameTurnAcquired()) < turns(25):
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

	if city.isPlayerCore(iPlayer):
		return 0
	
	iModifier = getSeparatismModifier(iPlayer, city)
	iPopulation = city.getPopulation()
	
	if city.isOccupation():
		iPopulation -= city.getTotalPopulationLoss()
	
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
	
	civics = Civics.player(iPlayer)
	
	iTotalCoreCities = 0
	iOccupiedCoreCities = 0
	
	iRecentlyFounded = 0
	iRecentlyConquered = 0
	
	iStateReligionPopulation = 0
	iOnlyStateReligionPopulation = 0
	iDifferentReligionPopulation = 0
	iNoReligionPopulation = 0
	
	iAdministration = cities.owner(iPlayer).sum(calculateAdministration) + 10
	iSeparatism = cities.owner(iPlayer).sum(calculateSeparatism)
	
	for city in cities.owner(iPlayer):
		iPopulation = city.getPopulation()
		bHistorical = city.plot().getPlayerSettlerValue(iPlayer) > 0
		bConquest = city.plot().getPlayerWarValue(iPlayer) > 1
		
		# Recent conquests
		if since(city.getGameTurnAcquired()) <= turns(20):
			if city.getPreviousCiv() < 0:
				if bHistorical:
					iRecentlyFounded += 1
			else:
				if bHistorical or bConquest:
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
		iCorePeripheryStability -= int(25 * sigmoid(1.0 * iSeparatismExcess / 100))
		
	lParameters[iParameterCorePeriphery] = iCorePeripheryStability
	lParameters[iParameterAdministration] = iAdministration
	lParameters[iParameterSeparatism] = iSeparatism
		
	iExpansionStability += iCorePeripheryStability
	
	# recent expansion stability
	iConquestModifier = 1
	if iConquest in civics: iConquestModifier += 1
	if iCiv == iPersia: iConquestModifier += 1 # Persian UP
	
	iRecentExpansionStability += iRecentlyFounded
	iRecentExpansionStability += iConquestModifier * iRecentlyConquered
		
	lParameters[iParameterRecentExpansion] = iRecentExpansionStability
	
	iExpansionStability += iRecentExpansionStability
	
	# apply raze city penalty
	if pPlayer.isHuman():
		iRazeCityStability = data.iHumanRazePenalty
	
	lParameters[iParameterRazedCities] = iRazeCityStability
		
	iExpansionStability += iRazeCityStability
	
	# stability if not expanded beyond core with isolationism
	iIsolationismStability = 0
	
	if iIsolationism in civics and iSeparatism <= 10:
		iIsolationismStability = 10
		
	lParameters[iParameterIsolationism] = iIsolationismStability
	
	iExpansionStability += iIsolationismStability
	
	# ECONOMY
	iEconomyStability = 0
	
	# Economic Growth
	iEconomicGrowthModifier = 3
	if iFreeEnterprise in civics: iEconomicGrowthModifier = 4
	
	iEconomicGrowthStability = iEconomicGrowthModifier * calculateTrendScore(data.players[iPlayer].lEconomyTrend)
	if iEconomicGrowthStability < 0 and iPublicWelfare in civics: iEconomicGrowthStability /= 2
	
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
	iCivicCombinationStability = getCivicStability(iPlayer)
		
	if not player(iPlayer).isHuman() and iCivicCombinationStability < 0: iCivicCombinationStability /= 2
	
	lParameters[iParameterCivicCombinations] = iCivicCombinationStability
	
	iCivicEraTechStability = 0
	
	# Civics (eras and techs and religions)
	# note: make sure to reflect this in CvPlayerAI::isUnstableCivic
	if iVassalage in civics:
		if iCurrentEra == iMedieval: iCivicEraTechStability += 2
		elif iCurrentEra >= iIndustrial: iCivicEraTechStability -= 5
		
	if iDeification in civics:
		if iCurrentEra <= iClassical: iCivicEraTechStability += 2
		else: iCivicEraTechStability -= 2 * (iCurrentEra - iClassical)
		
	if iRepublic in civics:
		if iCurrentEra <= iClassical: iCivicEraTechStability += 2
		elif iCurrentEra >= iIndustrial: iCivicEraTechStability -= 5
		
	if iIsolationism in civics:
		if iCurrentEra >= iIndustrial: iCivicEraTechStability -= (iCurrentEra - iRenaissance) * 3
		
	if tPlayer.isHasTech(iRepresentation):
		if (iRepublic, iDemocracy) not in civics and (iRevolutionism, iConstitution) not in civics: iCivicEraTechStability -= 5
		
	if tPlayer.isHasTech(iCivilRights):
		if (iSlavery, iManorialism, iCasteSystem) in civics: iCivicEraTechStability -= 5
		
	if tPlayer.isHasTech(iEconomics):
		if (iReciprocity, iRedistribution, iMerchantTrade) in civics: iCivicEraTechStability -= 5
		
	if tPlayer.isHasTech(iNationalism):
		if (iNationhood, iMultilateralism) in civics: iCivicEraTechStability += 5
		if (iConquest, iTributaries) in civics: iCivicEraTechStability -= 5
		
	if tPlayer.isHasTech(iDoctrine):
		if (iAnimism, iDeification) in civics: iCivicEraTechStability -= 5
	
	if tPlayer.isHasTech(iStatecraft):
		if (iAuthority, iCitizenship, iVassalage) not in civics: iCivicEraTechStability += 5
	
	if iStateReligion == iHinduism:
		if iCasteSystem in civics: iCivicEraTechStability += 3
		
	elif iStateReligion == iConfucianism:
		if iMeritocracy in civics: iCivicEraTechStability += 3
		
	elif iStateReligion in [iZoroastrianism, iOrthodoxy, iCatholicism, iProtestantism]:
		if iSlavery in civics: iCivicEraTechStability -= 3
		
	elif iStateReligion == iIslam:
		if iSlavery in civics: iCivicEraTechStability += 2
		
	elif iStateReligion == iBuddhism:
		if iMonasticism in civics: iCivicEraTechStability += 2
		
	elif iStateReligion == iConfucianism:
		if iIsolationism in civics: iCivicEraTechStability += 3
		
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
			
			if iBelieverStability > 0 and iTolerance in civics: iBelieverStability /= 2
			
			iReligionStability += iBelieverStability
			
			if iTheocracy in civics:
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
			
			if iTributaries in civics: iVassalStability += 2
			
		# relations
		if tPlayer.canContact(iLoopPlayer):
			lContacts.append(iLoopPlayer)
			
		# defensive pacts
		if tPlayer.isDefensivePact(iLoopPlayer):
			if iLoopScore > iPlayerScore: iDefensivePactStability += 3
			if iMultilateralism in civics: iDefensivePactStability += 3
		
		# worst enemies
		if pLoopPlayer.getWorstEnemy() == iPlayer:
			if iLoopScore > iPlayerScore: iRelationStability -= 3
			
		# wars
		if tPlayer.isAtWar(iLoopPlayer):
			if iMultilateralism in civics: iMultilateralismStability -= 2
			
			if game.isNeighbors(iPlayer, iLoopPlayer):
				if iNationhood in civics: iNationhoodStability += 2
				
				if iTheocracy in civics:
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
		
	if iIsolationism in civics:
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
	for iEnemy in players.major().existing():
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
	iBarbarianLossesStability = -min(10, data.players[iPlayer].iBarbarianLosses)
	
	lParameters[iParameterBarbarianLosses] = iBarbarianLossesStability
	
	iMilitaryStability += iBarbarianLossesStability
	
	iStability = iExpansionStability + iEconomyStability + iDomesticStability + iForeignStability + iMilitaryStability
	
	return iStability, [iExpansionStability, iEconomyStability, iDomesticStability, iForeignStability, iMilitaryStability], lParameters
	
def getCivicStability(iPlayer, civics=None):
	if civics is None:
		civics = Civics.player(iPlayer)

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
		if (iTolerance, iMonasticism) in civics: iStability -= 3
		
	if iCentralPlanning in civics:
		if iEgalitarianism in civics: iStability += 2
		if iStateParty in civics: iStability += 2
		if iCentralism in civics: iStability += 2
		
	if iEgalitarianism in civics:
		if iDemocracy in civics: iStability += 2
		if iConstitution in civics: iStability += 2
		if notcivics(iTolerance, iSecularism) in civics: iStability -= 3
		
	if iIndividualism in civics:
		if (iRepublic, iDemocracy) in civics: iStability += 2
		if iFreeEnterprise in civics: iStability += 3
		if iCentralPlanning in civics: iStability -= 5
		if (iRegulatedTrade, iPublicWelfare) in civics: iStability -= 2
		if iTolerance in civics: iStability += 2
		
	if iTheocracy in civics:
		if (iIndividualism, iEgalitarianism) in civics: iStability -= 3
		
	if iDeification in civics:
		if (iRepublic, iDemocracy) in civics: iStability -= 3
		
		if iCurrentEra <= iClassical:
			if iRedistribution in civics: iStability += 2
			if iSlavery in civics: iStability += 2
		
	if iVassalage in civics:
		if (iIndividualism, iEgalitarianism) in civics: iStability -= 5
		if (iFreeEnterprise, iCentralPlanning, iPublicWelfare) in civics: iStability -= 3
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
		if iMeritocracy in civics: iStability -= 4
		if iClergy in civics: iStability += 2
		if iSecularism in civics: iStability -= 3
		
	if iMultilateralism in civics:
		if iDespotism in civics: iStability -= 3
		if iTotalitarianism in civics: iStability -= 3
		if iEgalitarianism in civics: iStability += 2
		if iTheocracy in civics: iStability -= 3
		
	if iMonarchy in civics:
		if (iClergy, iMonasticism) in civics: iStability += 2
		
	if iElective in civics:
		if iCentralism in civics: iStability -= 5
		
	if iConstitution in civics:
		if iDemocracy in civics: iStability += 2
		
	if iRevolutionism in civics:
		if notcivics(iTolerance, iSecularism) in civics: iStability -= 3
		
	if iRegulatedTrade in civics:
		if iManorialism in civics: iStability += 2
		if iMeritocracy in civics: iStability += 3
		
	if iIsolationism in civics:
		if (iMerchantTrade, iFreeEnterprise) in civics: iStability -= 4
		if (iRegulatedTrade, iCentralPlanning) in civics: iStability += 3
		if iMeritocracy in civics: iStability += 3
		
	return iStability

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
	
	if not pPlayer.isExisting(): return
	
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
	
	if not pPlayer.isExisting(): return
	
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
		iCorporationUnhappinessOffset = min(city.getCorporationBadHappiness(), 3 * city.getCorporationCount())
		
		if city.isWeLoveTheKingDay() or (iPopulation >= iAveragePopulation and iHappiness - iUnhappiness >= iAveragePopulation / 4):
			iHappyCities += 1
		elif iUnhappiness - iOvercrowding - iCorporationUnhappinessOffset > iPopulation / 5 or iUnhappiness - iHappiness > 0:
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
	contacts = players.of(*lContacts).including(iPlayer).sort(game.getPlayerScore, True)
	iPlayerIndex = contacts.index(iPlayer)
	
	iRangeSize = 4
	if iPlayerIndex <= len(contacts) / 5:
		iRangeSize = 3
	
	iRange = len(contacts) / iRangeSize
	iLeft = max(0, iPlayerIndex - iRange/2)
	iRight = min(iLeft + iRange, len(contacts)-1)
	
	lStronger = [calculateAttitude(iLoopPlayer, iPlayer) for iLoopPlayer in contacts[:iLeft] if iLoopPlayer != iPlayer]
	lEqual = [calculateAttitude(iLoopPlayer, iPlayer) for iLoopPlayer in contacts[iLeft:iRight] if iLoopPlayer != iPlayer]
	lWeaker = [calculateAttitude(iLoopPlayer, iPlayer) for iLoopPlayer in contacts[iRight:] if iLoopPlayer != iPlayer]
	
	return lStronger, lEqual, lWeaker
	
def calculateAttitude(iFromPlayer, iToPlayer):
	pPlayer = player(iFromPlayer)

	iAttitude = pPlayer.AI_getAttitudeVal(iToPlayer)
	iAttitude -= pPlayer.AI_getSameReligionAttitude(iToPlayer)
	iAttitude -= pPlayer.AI_getDifferentReligionAttitude(iToPlayer)
	iAttitude -= pPlayer.AI_getFirstImpressionAttitude(iToPlayer)
	
	if team(iFromPlayer).isVassal(team(iToPlayer).getID()) and not team(iFromPlayer).isCapitulated():
		iAttitude -= 100
	
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
	
def getAdministrationModifier(iEra):
	return tEraAdministrationModifier[iEra]
	
def isDecline(iPlayer):
	return not player(iPlayer).isHuman() and year() >= year(dFall[iPlayer])

		