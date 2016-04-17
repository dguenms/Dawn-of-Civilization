# Rhye's and Fall of Civilization - Stability

from CvPythonExtensions import *
from StoredData import sd # edead
from Consts import *
import RFCUtils
import DynamicCivs as dc
from operator import itemgetter
import math
import Areas

utils = RFCUtils.RFCUtils()

# globals
gc = CyGlobalContext()

localText = CyTranslator()

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

def checkTurn(iGameTurn):
	for iPlayer in range(iNumPlayers):
		if sd.getTurnsToCollapse(iPlayer) == 0:
			sd.setTurnsToCollapse(iPlayer, -1)
			completeCollapse(iPlayer)
		elif sd.getTurnsToCollapse(iPlayer) > 0:
			sd.changeTurnsToCollapse(iPlayer, -1)
	
		if getCrisisCountdown(iPlayer) > 0:
			changeCrisisCountdown(iPlayer, -1)
			
	# calculate economic and happiness stability
	if iGameTurn % utils.getTurns(3) == 0:
		for iPlayer in range(iNumPlayers):
			updateEconomyTrend(iPlayer)
			updateHappinessTrend(iPlayer)
			
	# calculate war stability
	for iPlayer in range(iNumPlayers):
		for iEnemy in range(iNumPlayers):
			if gc.getTeam(iPlayer).isAtWar(iEnemy):
				updateWarTrend(iPlayer, iEnemy)
			
	# decay penalties from razing cities and losing to barbarians
	if iGameTurn % utils.getTurns(5) == 0:
		if sd.getHumanRazePenalty() < 0:
			sd.changeHumanRazePenalty(2)
		for iPlayer in range(iNumPlayers):
			if sd.getBarbarianLosses(iPlayer) > 0:
				sd.changeBarbarianLosses(iPlayer, -1)
			
	if iGameTurn % utils.getTurns(12) == 0:
		for iPlayer in range(iNumPlayers):
			checkLostCitiesCollapse(iPlayer)
			
	if iGameTurn >= getTurnForYear(tBirth[utils.getHumanID()]):
		sd.setHumanStability(calculateStability(utils.getHumanID()))
		
def endTurn(iPlayer):
	lSecedingCities = sd.getSecedingCities(iPlayer)
	
	if lSecedingCities:
		secedeCities(iPlayer, lSecedingCities)
		sd.setSecedingCities(iPlayer, [])
		
def triggerCollapse(iPlayer):
	sd.setTurnsToCollapse(iPlayer, 1)

def onCityAcquired(city, iOwner, iPlayer):
	checkStability(iOwner)
	
	checkLostCoreCollapse(iOwner)
	
	if iPlayer == iBarbarian:
		checkBarbarianCollapse(iOwner)
		
def onCityRazed(iPlayer, city):
	iOwner = city.getOwner()
	
	if iOwner == iBarbarian: return

	if utils.getHumanID() == iPlayer and iPlayer != iMongolia:
		iRazePenalty = -10
		if city.getPopulation() < 5 and not city.isCapital():
			iRazePenalty = -2 * city.getPopulation()
			
		if iOwner >= iNumPlayers: iRazePenalty /= 2
			
		sd.changeHumanRazePenalty(iRazePenalty)
		checkStability(iPlayer)
	
def onTechAcquired(iPlayer, iTech):
	checkStability(iPlayer)
	
def onVassalState(iMaster, iVassal):
	setStabilityLevel(iVassal, max(iStabilityShaky, getStabilityLevel(iVassal)))
	checkStability(iMaster, True)
	
	# update number of cities so vassals survive losing cities
	sd.setNumPreviousCities(iVassal, gc.getPlayer(iVassal).getNumCities())
	
def onChangeWar(bWar, iTeam, iOtherTeam):
	if iTeam < iNumPlayers and iOtherTeam < iNumPlayers:
		checkStability(iTeam, not bWar)
		checkStability(iOtherTeam, not bWar, bWar and utils.getHumanID() == iTeam)
		
		if bWar:
			startWar(iTeam, iOtherTeam)
			startWar(iOtherTeam, iTeam)
	
def onRevolution(iPlayer):
	checkStability(iPlayer)
	
def onPlayerChangeStateReligion(iPlayer):
	checkStability(iPlayer)
	
def onPalaceMoved(iPlayer):
	checkStability(iPlayer)
	
def onWonderBuilt(iPlayer, iBuildingType):
	checkStability(iPlayer, True)
	
def onGoldenAge(iPlayer):
	checkStability(iPlayer, True)
	
def onGreatPersonBorn(iPlayer):
	checkStability(iPlayer, True)
	
def onCombatResult(iWinningPlayer, iLosingPlayer, iLostPower):
	if iWinningPlayer == iBarbarian and iLosingPlayer < iNumPlayers:
		sd.changeBarbarianLosses(iLosingPlayer, 1)
	
def onCivSpawn(iPlayer):
	for iOlderNeighbor in lOlderNeighbours[iPlayer]:
		if gc.getPlayer(iOlderNeighbor).isAlive() and getStabilityLevel(iOlderNeighbor) > iStabilityShaky:
			decrementStability(iOlderNeighbor)
			#utils.debugTextPopup('Lost stability to neighbor spawn: ' + gc.getPlayer(iOlderNeighbor).getCivilizationShortDescription(0))

def getStabilityLevel(iPlayer):
	return sd.getStabilityLevel(iPlayer)
	
def setStabilityLevel(iPlayer, iStabilityLevel):
	sd.setStabilityLevel(iPlayer, iStabilityLevel)
	
def incrementStability(iPlayer):
	sd.setStabilityLevel(iPlayer, min(iStabilitySolid, sd.getStabilityLevel(iPlayer) + 1))
	
def decrementStability(iPlayer):
	sd.setStabilityLevel(iPlayer, max(iStabilityCollapsing, sd.getStabilityLevel(iPlayer) - 1))
	
def getCrisisCountdown(iPlayer):
	return sd.getCrisisCountdown(iPlayer)
	
def changeCrisisCountdown(iPlayer, iChange):
	sd.changeCrisisCountdown(iPlayer, iChange)
	
def isImmune(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iGameTurn = gc.getGame().getGameTurn()
	
	# must not be dead
	if not pPlayer.isAlive() or pPlayer.getNumCities() == 0:
		return True
		
	# only for major civs
	if iPlayer >= iNumPlayers:
		return True
		
	# immune right after scenario start
	if iGameTurn - utils.getScenarioStartTurn() < utils.getTurns(20):
		return True
		
	# immune right after birth
	if iGameTurn - getTurnForYear(tBirth[iPlayer]) < utils.getTurns(20):
		return True
		
	# immune right after resurrection
	if iGameTurn - pPlayer.getLatestRebellionTurn() < utils.getTurns(10):
		return True
		
	return False
	
def checkBarbarianCollapse(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iGameTurn = gc.getGame().getGameTurn()
		
	if isImmune(iPlayer): return
		
	iNumCities = pPlayer.getNumCities()
	iLostCities = 0
	
	for city in utils.getCityList(iBarbarian):
		if city.getOriginalOwner() == iPlayer:
			iLostCities += 1
			
	# lost more than half of your cities to barbarians: collapse
	if iLostCities > iNumCities:
		utils.debugTextPopup('Collapse by barbarians: ' + pPlayer.getCivilizationShortDescription(0))
		completeCollapse(iPlayer)
		
	# lost at least two cities to barbarians: lose stability
	elif iLostCities >= 2:
		utils.debugTextPopup('Lost stability to barbarians: ' + pPlayer.getCivilizationShortDescription(0))
		decrementStability(iPlayer)
		
def checkLostCitiesCollapse(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iGameTurn = gc.getGame().getGameTurn()
	
	if isImmune(iPlayer): return
		
	iNumCurrentCities = pPlayer.getNumCities()
	iNumPreviousCities = sd.getNumPreviousCities(iPlayer)
	
	# half or less cities than 12 turns ago: collapse (exceptions for civs with very little cities to begin with -> use lost core collapse)
	if iNumPreviousCities > 2 and 2 * iNumCurrentCities <= iNumPreviousCities:
	
		if getStabilityLevel(iPlayer) == iStabilityCollapsing:
			utils.debugTextPopup('Collapse by lost cities: ' + pPlayer.getCivilizationShortDescription(0))
			completeCollapse(iPlayer)
		else:
			utils.debugTextPopup('Collapse to core by lost cities: ' + pPlayer.getCivilizationShortDescription(0))
			setStabilityLevel(iPlayer, iStabilityCollapsing)
			collapseToCore(iPlayer)
		
	sd.setNumPreviousCities(iPlayer, iNumCurrentCities)
	
def checkLostCoreCollapse(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iGameTurn = gc.getGame().getGameTurn()
	
	if isImmune(iPlayer): return
	
	lCities = utils.getAreaCitiesCiv(iPlayer, Areas.getCoreArea(iPlayer))
	
	# completely pushed out of core: collapse
	if len(lCities) == 0:
		if iPlayer in [iPhoenicia, iKhmer] and not utils.isReborn(iPlayer):
			pPlayer.setReborn(True)
			return
	
		utils.debugTextPopup('Collapse from lost core: ' + pPlayer.getCivilizationShortDescription(0))
		completeCollapse(iPlayer)
		
def getAverageStabilityLevel(iPlayer):
	iLevel = 0
	iCount = 0
	for iLoopPlayer in range(iNumPlayers):
		if gc.getPlayer(iLoopPlayer).isAlive() and iLoopPlayer != iPlayer:
			iCount += 1
			iLevel += getStabilityLevel(iLoopPlayer)-2
			
	if iCount == 0: return 0
	
	return 1 * iLevel / iCount
		
def getStabilityThreshold(iPlayer):
	iGameTurn = gc.getGame().getGameTurn()
	iStabilityLevel = getStabilityLevel(iPlayer)

	iThreshold = 10 * (iStabilityLevel - 2)
	
	if utils.getHumanID() != iPlayer and iGameTurn > getTurnForYear(tFall[iPlayer]):
		iThreshold += 5 * iStabilityLevel + 5 + max(10, (iGameTurn - getTurnForYear(tFall[iPlayer])) / utils.getTurns(10))
		
	# golden ages make stability increases easier
	if gc.getPlayer(iPlayer).isGoldenAge():
		iThreshold -= 5
		
	# make everyone a bit more stable after the Renaissance -> less collapses
	if gc.getGame().getCurrentEra() >= iRenaissance:
		iThreshold -= 5
		
	# normalization: reduce the threshold if most of the world is unstable and vice versa
	iThreshold += getAverageStabilityLevel(iPlayer) * 5
		
	return iThreshold

def checkStability(iPlayer, bPositive = False, bWar = False, iMaster = -1):
	pPlayer = gc.getPlayer(iPlayer)
	iGameTurn = gc.getGame().getGameTurn()
	iGameEra = gc.getGame().getCurrentEra()
	
	bVassal = (iMaster != -1)
	
	# vassal checks are made for triggers of their master civ
	if gc.getTeam(pPlayer.getTeam()).isAVassal() and not bVassal: return
	
	if isImmune(iPlayer): return
		
	# immune to negative stability checks in golden ages
	if pPlayer.isGoldenAge() and not bPositive:
		return
		
	# immune during anarchy
	if pPlayer.isAnarchy(): return
		
	# immune if there's been a crisis recently
	if getCrisisCountdown(iPlayer) > 0: return
		
	iStability, lStabilityTypes, lParameters = calculateStability(iPlayer)
	iStabilityLevel = getStabilityLevel(iPlayer)
	sd.setLastDifference(iPlayer, 0)
	bHuman = (utils.getHumanID() == iPlayer)
	bHumanVassal = (bVassal and utils.getHumanID() == iMaster)
	bFall = (not bHuman and iGameTurn > getTurnForYear(tFall[iPlayer]))
	bContinue = False
	
	iCrisisLevelLimit = iStabilityCollapsing
	if bVassal: iCrisisLevelLimit = getStabilityLevel(iMaster)
	
	# it's easier to lose stability and harder to gain it at higher levels -> prevent "falling through the levels"
	iThreshold = getStabilityThreshold(iPlayer)
		
	if iStability > iThreshold + 10:
		if iStabilityLevel == iStabilitySolid:
			triggerBonus(iPlayer, lStabilityTypes)
		else:
			incrementStability(iPlayer)
			
		sd.setLastDifference(iPlayer, 1)
		if bHuman: sd.setCrisisImminent(False)
		
	elif iStability >= iThreshold:
		if bHuman: sd.setCrisisImminent(False)
		
		# if stability does not improve on collapsing, a complete collapse ensues
		if iStabilityLevel == iStabilityCollapsing:
			if iStability <= sd.getLastStability(iPlayer):
				#completeCollapse(iPlayer)
				triggerCollapse(iPlayer)
		
	elif not bPositive:
		# humans are immune to first stability drop
		if (bHuman or bHumanVassal) and not sd.isCrisisImminent() and iStabilityLevel > iStabilityCollapsing:
			if bHuman: sd.setCrisisImminent(True)
			changeCrisisCountdown(iPlayer, utils.getTurns(5))
			sText = localText.getText("TXT_KEY_STABILITY_CRISIS_IMMINENT_MESSAGE", (localText.getText(tCrisisLevels[iStabilityLevel], ()),))
			CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
		else:
			decrementStability(iPlayer)
			sd.setLastDifference(iPlayer, -1)
		
			iCrisisType = determineCrisisType(lStabilityTypes)
			iCrisisLevel = iStabilityLevel # PREVIOUS level
			
			# if vassal and master is more stable, prevent worse crises
			if iCrisisLevelLimit > iCrisisLevel: iCrisisLevel = iCrisisLevelLimit
		
			triggerCrisis(iPlayer, iCrisisLevel, iCrisisType, bWar)
			
			if bFall: bContinue = True
		
	# update stability information
	sd.setLastStability(iPlayer, iStability)
	for i in range(5):
		sd.setStabilityCategoryValue(iPlayer, i, lStabilityTypes[i])
	
	for i in range(iNumStabilityParameters):
		pPlayer.setStabilityParameter(i, lParameters[i])
		
	if bContinue: checkStability(iPlayer, bPositive, bWar)
	
	# check vassals
	for iLoopPlayer in range(iNumPlayers):
		if gc.getTeam(iLoopPlayer).isVassal(iPlayer):
			checkStability(iLoopPlayer, bPositive, bWar, iPlayer)
			
def triggerBonus(iPlayer, lStabilityParameters):
	return
	
def triggerCrisis(iPlayer, iCrisisLevel, iCrisisType, bWar):
	if iCrisisLevel >= iStabilityStable: return
	
	sText = localText.getText("TXT_KEY_STABILITY_CRISIS_MESSAGE", (localText.getText(tCrisisLevels[iCrisisLevel], ()), localText.getText(tCrisisTypes[iCrisisType], ())))
	CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
		
	# immune for 10 turns after this crisis
	changeCrisisCountdown(iPlayer, utils.getTurns(10))
	
	if iCrisisLevel == iStabilityCollapsing:
		if not bWar:
			#completeCollapse(iPlayer)
			triggerCollapse(iPlayer)
	
	else:
		if iCrisisType == iStabilityExpansion: territorialCrisis(iPlayer, iCrisisLevel)
		elif iCrisisType == iStabilityEconomy: economicCrisis(iPlayer, iCrisisLevel)
		elif iCrisisType == iStabilityDomestic: domesticCrisis(iPlayer, iCrisisLevel)
		elif iCrisisType == iStabilityForeign: diplomaticCrisis(iPlayer, iCrisisLevel)
		elif iCrisisType == iStabilityMilitary: militaryCrisis(iPlayer, iCrisisLevel)
		
def territorialCrisis(iPlayer, iCrisisLevel):

	# moderate crisis: a single city secedes
	if iCrisisLevel == iStabilityShaky:
		secedeSingleCity(iPlayer)
		
	# severe crisis: collapse to core
	elif iCrisisLevel == iStabilityUnstable:
		collapseToCore(iPlayer)
		
def economicCrisis(iPlayer, iCrisisLevel):
	pPlayer = gc.getPlayer(iPlayer)
	
	# moderate crisis: lose 50% research or gold equivalent
	if iCrisisLevel == iStabilityShaky:
		sText = localText.getText("TXT_KEY_STABILITY_ECONOMIC_CRISIS", ())
		CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
	
		loseCommerce(iPlayer, 50)
		
	# severe crisis: lose 100% research or gold equivalent, cottages and GPP decay
	elif iCrisisLevel == iStabilityUnstable:
		sText = localText.getText("TXT_KEY_STABILITY_ECONOMIC_CRISIS", ())
		CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
		
		loseCommerce(iPlayer, 100)
		downgradeCottages(iPlayer)
		removeGreatPeoplePoints(iPlayer)
		
def domesticCrisis(iPlayer, iCrisisLevel):
	pPlayer = gc.getPlayer(iPlayer)
	lCities = utils.getCityList(iPlayer)

	# moderate crisis: unrest in unhappy cities
	if iCrisisLevel == iStabilityShaky:
		sText = localText.getText("TXT_KEY_STABILITY_DOMESTIC_CRISIS", ())
		CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
		
		for city in lCities:
			if city.happyLevel() < city.unhappyLevel(0): city.setOccupationTimer(2)
			
	# severe crisis: two turns of anarchy, unhappy cities secede
	elif iCrisisLevel == iStabilityUnstable:
		sText = localText.getText("TXT_KEY_STABILITY_DOMESTIC_CRISIS", ())
		CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
		
		pPlayer.changeAnarchyTurns(2)
		secedeUnhappyCities(iPlayer)
		
def diplomaticCrisis(iPlayer, iCrisisLevel):
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(iPlayer)
	#lTradingCivs = []
	#lDefensivePactCivs = []
	lContacts = []
	lPeaceVassalCivs = []
	lCapitulatedCivs = []
	
	for iLoopPlayer in range(iNumPlayers):
		tLoopPlayer = gc.getTeam(iLoopPlayer)
		#if tLoopPlayer.isOpenBorders(iPlayer):
		#	lTradingCivs.append(iLoopPlayer)
		#if tLoopPlayer.isDefensivePact(iPlayer):
		#	lDefensivePactCivs.append(iLoopPlayer)
		if pPlayer.canContact(iLoopPlayer):
			lContacts.append(iLoopPlayer)
		if tLoopPlayer.isVassal(iPlayer):
			if tLoopPlayer.isCapitulated():
				lCapitulatedCivs.append(iLoopPlayer)
			else:
				lPeaceVassalCivs.append(iLoopPlayer)

	# moderate crisis: relations with 2 civilizations damaged
	if iCrisisLevel == iStabilityShaky:
		damageRelations(iPlayer, lContacts, 2)
		
	# severe crisis: relations with 5 civilizations damaged, vassals freed
	elif iCrisisLevel == iStabilityUnstable:
		damageRelations(iPlayer, lContacts, 5)
		cancelVassals(iPlayer, lPeaceVassalCivs, False)
		cancelVassals(iPlayer, lCapitulatedCivs, True)
		
def militaryCrisis(iPlayer, iCrisisLevel):

	# moderate crisis: loss of city defenses
	if iCrisisLevel == iStabilityShaky:
		removeTargetCityDefenses(iPlayer)
	
	# severe crisis: unrest in enemy target cities, immobilized units
	elif iCrisisLevel == iStabilityUnstable:
		targetCityUnrest(iPlayer)
		immobilizeUnits(iPlayer)
		
def getPossibleMinors(iPlayer):

	if gc.getGame().countKnownTechNumTeams(iNationalism) == 0 and iPlayer in [iMaya, iAztecs, iInca, iMali, iEthiopia, iCongo]:
		return [iNative]
		
	if gc.getGame().getCurrentEra() <= iMedieval:
		return [iBarbarian, iIndependent, iIndependent2]
		
	return [iIndependent, iIndependent2]
	
def secession(iPlayer, lCities):
	sd.setSecedingCities(iPlayer, lCities)
	
def secedeCities(iPlayer, lCities, bRazeMinorCities = False):
	lPossibleMinors = getPossibleMinors(iPlayer)
	dPossibleResurrections = {}
	
	utils.clearPlague(iPlayer)
	
	# if smaller cities are supposed to be destroyed, do that first
	lCededCities = []
	lRemovedCities = []
	for city in lCities:
		if bRazeMinorCities:
			bMaxPopulation = (city.getPopulation() < 10)
			bNoHolyCities = (not city.isHolyCity())
			bNoCapitals = (not city.isCapital())
			bNotJerusalem = (not (city.getX() == 73 and city.getY() == 38))
			
			if bMaxPopulation and bNoHolyCities and bNoCapitals and bNotJerusalem:
				closestCity = gc.getMap().findCity(city.getX(), city.getY(), iPlayer, -1, True, False, -1, -1, city)
				
				if closestCity:
					if plotDistance(city.getX(), city.getY(), closestCity.getX(), closestCity.getY()) <= 2:
						bCulture = (city.getCultureLevel() <= closestCity.getCultureLevel())
						bPopulation = (city.getPopulation() < closestCity.getPopulation())
						
						if bCulture and bPopulation:
							lRemovedCities.append(city)
							continue
							
			# always raze Harappan cities
			if iPlayer == iHarappa and utils.getHumanID() != iPlayer:
				lRemovedCities.append(city)
				continue
						
		lCededCities.append(city)
			
	for city in lRemovedCities:
		gc.getPlayer(iBarbarian).disband(city)
	
	for city in lCededCities:
	
		tCityPlot = (city.getX(), city.getY())
		cityPlot = gc.getMap().plot(city.getX(), city.getY())
		iGameTurnYear = gc.getGame().getGameTurnYear()
	
		# three possible behaviors: if living civ has a claim, assign it to them
		# claim based on core territory
		iClaim = -1
		for iLoopPlayer in range(iNumPlayers):
			if iLoopPlayer == iPlayer: continue
			if utils.getHumanID() == iLoopPlayer: continue
			if iGameTurnYear < tBirth[iLoopPlayer]: continue
			if iGameTurnYear > tFall[iLoopPlayer]: continue
			if cityPlot.isCore(iLoopPlayer) and gc.getPlayer(iLoopPlayer).isAlive():
				iClaim = iLoopPlayer
				utils.debugTextPopup('Secede ' + gc.getPlayer(iPlayer).getCivilizationAdjective(0) + ' ' + city.getName() + ' to ' + gc.getPlayer(iClaim).getCivilizationShortDescription(0) + '.\nReason: core territory.')
				break
		
		# claim based on original owner
		if iClaim == -1:
			iOriginalOwner = city.getOriginalOwner()
			if cityPlot.getSettlerValue(iOriginalOwner) >= 90 and gc.getPlayer(iOriginalOwner).isAlive() and iOriginalOwner != iPlayer and utils.getHumanID() != iOriginalOwner:
				if iOriginalOwner < iNumPlayers and iGameTurnYear < tFall[iOriginalOwner]:
					# cities lost too long ago don't return
					if city.getGameTurnPlayerLost(iOriginalOwner) >= gc.getGame().getGameTurn() - utils.getTurns(50):
						iClaim = iOriginalOwner
						utils.debugTextPopup('Secede ' + gc.getPlayer(iPlayer).getCivilizationAdjective(0) + ' ' + city.getName() + ' to ' + gc.getPlayer(iClaim).getCivilizationShortDescription(0) + '.\nReason: original owner.')
				
		# claim based on culture
		if iClaim == -1:
			for iLoopPlayer in range(iNumPlayers):
				if iLoopPlayer == iPlayer: continue
				if utils.getHumanID() == iLoopPlayer: continue
				if iGameTurnYear < tBirth[iLoopPlayer]: continue
				if iGameTurnYear > tFall[iLoopPlayer]: continue
				if gc.getPlayer(iLoopPlayer).isAlive():
					iTotalCulture = cityPlot.countTotalCulture()
					if iTotalCulture > 0:
						iCulturePercent = 100 * cityPlot.getCulture(iLoopPlayer) / cityPlot.countTotalCulture()
						if iCulturePercent >= 75:
							iClaim = iLoopPlayer
							utils.debugTextPopup('Secede ' + gc.getPlayer(iPlayer).getCivilizationAdjective(0) + ' ' + city.getName() + ' to ' + gc.getPlayer(iClaim).getCivilizationShortDescription(0) + '.\nReason: culture.')
							break
						
		# claim based on war target (needs to be winning the war based on war success)
		if iClaim == -1:
			tPlayer = gc.getTeam(iPlayer)
			for iLoopPlayer in range(iNumPlayers):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.isAlive() and tPlayer.isAtWar(iLoopPlayer) and utils.getHumanID() != iLoopPlayer and iGameTurnYear < tFall[iLoopPlayer]:
					if pLoopPlayer.getWarValue(city.getX(), city.getY()) >= 8 and gc.getTeam(iLoopPlayer).AI_getWarSuccess(iPlayer) > tPlayer.AI_getWarSuccess(iLoopPlayer):
						# another enemy with closer city: don't claim the city
						closestCity = gc.getMap().findCity(city.getX(), city.getY(), PlayerTypes.NO_PLAYER, TeamTypes.NO_TEAM, True, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, city)
						if closestCity.getOwner() != iLoopPlayer and tPlayer.isAtWar(closestCity.getOwner()): continue
						iClaim = iLoopPlayer
						utils.debugTextPopup('Secede ' + gc.getPlayer(iPlayer).getCivilizationAdjective(0) + ' ' + city.getName() + ' to ' + gc.getPlayer(iClaim).getCivilizationShortDescription(0) + '.\nReason: war target.')
						break
						
		if iClaim != -1:
			secedeCity(city, iClaim)
			continue

		# if part of the core / resurrection area of a dead civ -> possible resurrection
		bResurrectionFound = False
		for iLoopPlayer in range(iNumPlayers):
			if iLoopPlayer == iPlayer: continue
			if gc.getPlayer(iLoopPlayer).isAlive(): continue
			if gc.getGame().getGameTurn() - utils.getLastTurnAlive(iLoopPlayer) < utils.getTurns(20): continue
			
			# Leoreth: Egyptian respawn on Arabian collapse hurts Ottoman expansion
			if iPlayer == iArabia and iLoopPlayer == iEgypt: continue

			if tCityPlot in Areas.getRespawnArea(iLoopPlayer):
				bPossible = False
				
				for tInterval in tResurrectionIntervals[iLoopPlayer]:
					iStart, iEnd = tInterval
					if iStart <= gc.getGame().getGameTurnYear() <= iEnd:
						bPossible = True
						break
				
				if bPossible:
					if iLoopPlayer in dPossibleResurrections:
						dPossibleResurrections[iLoopPlayer].append(city)
					else:
						dPossibleResurrections[iLoopPlayer] = [city]
					bResurrectionFound = True
					utils.debugTextPopup(gc.getPlayer(iPlayer).getCivilizationAdjective(0) + ' ' + city.getName() + ' is part of the ' + gc.getPlayer(iLoopPlayer).getCivilizationAdjective(0) + ' resurrection.')
					break
				
		if bResurrectionFound: continue

		# assign randomly to possible minors
		secedeCity(city, lPossibleMinors[city.getID() % len(lPossibleMinors)])
		
	# execute possible resurrections
	# might need a more sophisticated approach to also catch minors and other unstable civs in their respawn area
	for iResurrectionPlayer in dPossibleResurrections:
		utils.debugTextPopup('Resurrection: ' + gc.getPlayer(iResurrectionPlayer).getCivilizationShortDescription(0))
		resurrectionFromCollapse(iResurrectionPlayer, dPossibleResurrections[iResurrectionPlayer])
		
def secedeCity(city, iNewOwner):
	if not city: return

	sName = city.getName()
	utils.completeCityFlip(city.getX(), city.getY(), iNewOwner, city.getOwner(), 50, False, True, True)
	
	if city.getOwner() == utils.getHumanID():
		if iNewOwner in [iIndependent, iIndependent2, iNative, iBarbarian]:
			sText = localText.getText("TXT_KEY_STABILITY_CITY_INDEPENDENCE", (sName,))
			CyInterface().addMessage(city.getOwner(), False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
		else:
			sText = localText.getText("TXT_KEY_STABILITY_CITY_CHANGED_OWNER", (sName, gc.getPlayer(iNewOwner).getCivilizationAdjective(0)))
			utils.debugTextPopup(sText)
			CyInterface().addMessage(city.getOwner(), False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
		
	if utils.getHumanID() == iNewOwner:
		sText = localText.getText("TXT_KEY_STABILITY_CITY_CHANGED_OWNER_US", (sName,))
		CyInterface().addMessage(iNewOwner, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
	
def completeCollapse(iPlayer):
	lCities = utils.getCityList(iPlayer)
	
	# before cities are seceded, downgrade their cottages
	downgradeCottages(iPlayer)
	
	# secede all cities, destroy close and less important ones
	bRazeMinorCities = (gc.getPlayer(iPlayer).getCurrentEra() <= iMedieval)
	secedeCities(iPlayer, lCities, bRazeMinorCities)
		
	# take care of the remnants of the civ
	gc.getPlayer(iPlayer).killUnits()
	utils.resetUHV(iPlayer)
	utils.setLastTurnAlive(iPlayer, gc.getGame().getGameTurn())
		
	# special case: Byzantine collapse: remove Christians in the Turkish core
	if iPlayer == iByzantium:
		utils.removeReligionByArea(Areas.getCoreArea(iTurkey), iOrthodoxy)
		
	# Chinese collapse: Mongolia's core moves south
	if iPlayer == iChina:
		utils.setReborn(iMongolia, True)
		
	utils.debugTextPopup('Complete collapse: ' + gc.getPlayer(iPlayer).getCivilizationShortDescription(0))
	
	sText = localText.getText("TXT_KEY_STABILITY_COMPLETE_COLLAPSE", (gc.getPlayer(iPlayer).getCivilizationAdjective(0),))
	CyInterface().addMessage(utils.getHumanID(), False, iDuration, sText, "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
		
def collapseToCore(iPlayer):
	lAhistoricalCities = []
	lNonCoreCities = []
	
	for city in utils.getCityList(iPlayer):
		plot = gc.getMap().plot(city.getX(), city.getY())
		if not plot.isCore(iPlayer):
			lNonCoreCities.append(city)
			if plot.getSettlerValue(iPlayer) < 90:
				lAhistoricalCities.append(city)
				
	# more than half ahistorical, only secede ahistorical cities
	if 2 * len(lAhistoricalCities) > len(lNonCoreCities):
			
		# notify owner
		if utils.getHumanID() == iPlayer:
			sText = localText.getText("TXT_KEY_STABILITY_FOREIGN_SECESSION", ())
			CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
				
		# secede all foreign cities
		secession(iPlayer, lAhistoricalCities)
		
	# otherwise, secede all cities outside of core
	elif lNonCoreCities:
			
		# notify owner
		if utils.getHumanID() == iPlayer:
			sText = localText.getText("TXT_KEY_STABILITY_COLLAPSE_TO_CORE", ())
			CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
			
		# secede all non-core cities
		secession(iPlayer, lNonCoreCities)
	
	# territorial crisis should be impossible while controlling only the core but otherwise lose some territory
	else:
		loseTerritory(iPlayer)
	
def secedeSingleCity(iPlayer):
	lCities = []
	
	for city in utils.getCityList(iPlayer):
		if not gc.getMap().plot(city.getX(), city.getY()).isCore(iPlayer):
			lCities.append(city)
			
	# secede a non-core city with the lowest settler map value
	if lCities:
		secession(iPlayer, [utils.getHighestEntry(lCities, lambda x: -gc.getMap().plot(x.getX(), x.getY()).getSettlerValue(iPlayer))])
	else:
		loseTerritory(iPlayer)
		
def loseTerritory(iPlayer):
	lCities = utils.getCityList(iPlayer)
	lTakenTiles = [[] for i in lCities]
	
	for city in lCities:
		lPlotList = []
		for i in range(21):
			plot = plotCity(city.getX(), city.getY(), i)
			if plot.getOwner() == iPlayer:
				for iLoopPlayer in range(iNumTotalPlayersB):
					if not gc.getTeam(iLoopPlayer).isVassal(iPlayer) and plot.isPlayerCityRadius(iLoopPlayer):
						lPlotList.append(plot)
						break
		lTakenTiles[lCities.index(city)] = lPlotList
		
	lHighestEntry = utils.getHighestEntry(lTakenTiles, lambda x : len(x))
	
	for plot in lTakenTiles[lTakenTiles.index(lHighestEntry)]:
		utils.convertPlotCulture(plot, iPlayer, 0, True)
		
	# notify owner
	if utils.getHumanID() == iPlayer:
		sText = localText.getText("TXT_KEY_STABILITY_LOSE_TERRITORY", (lCities[lTakenTiles.index(lHighestEntry)].getName(),))
		CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)

def secedeUnhappyCities(iPlayer):
	lCities = []
	lRemainingCities = []
	
	for city in utils.getCityList(iPlayer):
		if city.unhappyLevel(0) > city.happyLevel() and not city.isCapital():
			lCities.append(city)
		else:
			lRemainingCities.append(city)
			
	# notify owner
	if utils.getHumanID() == iPlayer:
		sText = localText.getText("TXT_KEY_STABILITY_SECEDE_UNHAPPY", ())
		CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
			
	# secede all unhappy cities
	secession(iPlayer, lCities)
		
def secedeEnemyTargetCities(iPlayer):
	tPlayer = gc.getTeam(iPlayer)
	lEnemies = []
	
	for iLoopPlayer in range(iNumPlayers):
		if tPlayer.isAtWar(iLoopPlayer):
			lEnemies.append(iLoopPlayer)
	
	for city in utils.getCityList(iPlayer):
		for iEnemy in lEnemies:
			lEnemyCities = []
			if gc.getPlayer(iEnemy).getWarValue(city.getX(), city.getY()) >= 8:
				lEnemyCities.append(city)
			if lEnemyCities:
				secedeCity(utils.getRandomEntry(lEnemyCities), iEnemy)
	
def getResearchProgress(iPlayer):
	tPlayer = gc.getTeam(iPlayer)
	iCost = 0
	
	for iTech in range(iNumTechs):
		if not tPlayer.isHasTech(iTech):
			iCost += tPlayer.getResearchProgress(iTech)
		
	return iCost
	
def loseCommerce(iPlayer, iPercentage):
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(iPlayer)

	iTechCost = getResearchProgress(iPlayer)
	iGold = pPlayer.getGold()
	
	iTechReduction = iTechCost * iPercentage / 100
	
	iGold -= iGold * iPercentage / 100
	
	if iGold > iTechReduction:
		iLostGold = iTechReduction
		iLostBeakers = 0
		iGold -= iTechReduction
	else:
		iLostGold = iGold
		iTechReduction -= iGold
		iGold = 0
		
		iLostBeakers = iTechReduction
		
		for iTech in range(iNumTechs):
			if iTechReduction <= 0: break
			
			iTechProgress = tPlayer.getResearchProgress(iTech)
			tPlayer.setResearchProgress(iTech, max(0, iTechProgress - iTechReduction), iPlayer)
			
			iTechReduction = max(0, iTechReduction - iTechProgress)
			
	pPlayer.setGold(iGold)
	
	if utils.getHumanID() == iPlayer:
		sText = localText.getText("TXT_KEY_STABILITY_LOST_COMMERCE", (iLostGold, iLostBeakers))
		CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
	
def downgradeCottages(iPlayer):
	for x in range(128):
		for y in range(64):
			plot = gc.getMap().plot(x, y)
			if plot.getOwner() == iPlayer:
				iImprovement = plot.getImprovementType()
				
				if iImprovement == iTown: plot.setImprovementType(iHamlet)
				elif iImprovement == iVillage: plot.setImprovementType(iCottage)
				elif iImprovement == iHamlet: plot.setImprovementType(iCottage)
				elif iImprovement == iCottage: plot.setImprovementType(-1)
				
	if utils.getHumanID() == iPlayer:
		sText = localText.getText("TXT_KEY_STABILITY_DOWNGRADE_COTTAGES", ())
		CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
				
def removeGreatPeoplePoints(iPlayer):
	for city in utils.getCityList(iPlayer):
		city.changeGreatPeopleProgress(-city.getGreatPeopleProgress())
		
	if utils.getHumanID() == iPlayer:
		sText = localText.getText("TXT_KEY_STABILITY_REMOVE_GPP", ())
		CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
		
def damageRelations(iPlayer, lContacts, iNumOtherPlayers):
	pPlayer = gc.getPlayer(iPlayer)
	
	for i in range(iNumOtherPlayers):
		if lContacts:
			iOtherPlayer = utils.getRandomEntry(lContacts)
			pOtherPlayer = gc.getPlayer(iOtherPlayer)
			
			pOtherPlayer.AI_changeMemoryCount(iPlayer, MemoryTypes.MEMORY_EVENT_BAD_TO_US, 4)
			
			lContacts.remove(iOtherPlayer)
			
			if utils.getHumanID() == iPlayer:
				sText = localText.getText("TXT_KEY_STABILITY_DAMAGE_RELATIONS", (gc.getPlayer(iOtherPlayer).getCivilizationShortDescription(0),))
				CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
				
			if utils.getHumanID() == iOtherPlayer:
				sText = localText.getText("TXT_KEY_STABILITY_DAMAGE_RELATIONS", (gc.getPlayer(iPlayer).getCivilizationShortDescription(0),))
				CyInterface().addMessage(iOtherPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
		
def cancelTrades(iPlayer, lTradingCivs, iNumCancels):
	tPlayer = gc.getTeam(iPlayer)
	pPlayer = gc.getPlayer(iPlayer)

	for i in range(iNumCancels):
		if lTradingCivs:
			iOtherPlayer = utils.getHighestEntry(lTradingCivs, lambda x : -pPlayer.AI_getAttitude(x))
			pOtherPlayer = gc.getPlayer(iOtherPlayer)
			tOtherPlayer = gc.getTeam(iOtherPlayer)
			
			#tPlayer.setOpenBorders(iOtherPlayer, False)
			#tOtherPlayer.setOpenBorders(iPlayer, False)
			
			lDeals = utils.getAllDealsType(iPlayer, iOtherPlayer, TradeableItems.TRADE_OPEN_BORDERS)
			
			if lDeals: 
				lDeals[0].kill()
			else:
				#utils.debugTextPopup('No appropriate deals found.')
				continue
			
			pOtherPlayer.AI_changeMemoryCount(iPlayer, MemoryTypes.MEMORY_STOPPED_TRADING_RECENT, utils.getTurns(10))
			pOtherPlayer.AI_changeAttitudeExtra(iPlayer, -2)
			
			lTradingCivs.remove(iOtherPlayer)
			
			if utils.getHumanID() == iPlayer:
				sText = localText.getText("TXT_KEY_STABILITY_CANCEL_TRADE", (gc.getPlayer(iOtherPlayer).getCivilizationShortDescription(0),))
				CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
				
			if utils.getHumanID() == iOtherPlayer:
				sText = localText.getText("TXT_KEY_STABILITY_CANCEL_TRADE", (gc.getPlayer(iPlayer).getCivilizationShortDescription(0),))
				CyInterface().addMessage(iOtherPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
			
def cancelDefensivePacts(iPlayer, lDefensivePactCivs):
	tPlayer = gc.getTeam(iPlayer)
	
	for iOtherPlayer in lDefensivePactCivs:
		pOtherPlayer = gc.getPlayer(iOtherPlayer)
		tOtherPlayer = gc.getTeam(iOtherPlayer)
		
		#tPlayer.setDefensivePact(iOtherPlayer, False)
		#tOtherPlayer.setDefensivePact(iPlayer, False)
			
		lDeals = utils.getAllDealsType(iPlayer, iOtherPlayer, TradeableItems.TRADE_DEFENSIVE_PACT)
		
		if lDeals: 
			lDeals[0].kill()
		else:
			#utils.debugTextPopup('No appropriate deals found.')
			continue
			
		pOtherPlayer.AI_changeMemoryCount(iPlayer, MemoryTypes.MEMORY_STOPPED_TRADING_RECENT, utils.getTurns(10))
		pOtherPlayer.AI_changeAttitudeExtra(iPlayer, -2)
			
		if utils.getHumanID() == iPlayer:
			sText = localText.getText("TXT_KEY_STABILITY_CANCEL_DEFENSIVE_PACT", (gc.getPlayer(iOtherPlayer).getCivilizationShortDescription(0),))
			CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
			
		if utils.getHumanID() == iOtherPlayer:
			sText = localText.getText("TXT_KEY_STABILITY_CANCEL_DEFENSIVE_PACT", (gc.getPlayer(iPlayer).getCivilizationShortDescription(0),))
			CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
	
def cancelVassals(iPlayer, lVassals, bCapitulated):
	for iOtherPlayer in lVassals:
		pOtherPlayer = gc.getPlayer(iOtherPlayer)
		tOtherPlayer = gc.getTeam(iOtherPlayer)
		
		#tOtherPlayer.setVassal(iPlayer, False, bCapitulated)
		
		if bCapitulated: iTrade = TradeableItems.TRADE_SURRENDER
		else: iTrade = TradeableItems.TRADE_VASSAL
		
		lDeals = utils.getAllDealsType(iPlayer, iOtherPlayer, iTrade)
		
		if lDeals: 
			lDeals[0].kill()
		else:
			#utils.debugTextPopup('No appropriate deals found.')
			continue
		
		pOtherPlayer.AI_changeMemoryCount(iPlayer, MemoryTypes.MEMORY_STOPPED_TRADING_RECENT, utils.getTurns(10))
		pOtherPlayer.AI_changeAttitudeExtra(iPlayer, -2)
			
		if utils.getHumanID() == iPlayer:
			if bCapitulated:
				sText = localText.getText("TXT_KEY_STABILITY_CANCEL_CAPITULATION", (gc.getPlayer(iOtherPlayer).getCivilizationShortDescription(0),))
			else:
				sText = localText.getText("TXT_KEY_STABILITY_CANCEL_PEACE_VASSAL", (gc.getPlayer(iOtherPlayer).getCivilizationShortDescription(0),))
			CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
			
def getEnemyTargetCities(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(iPlayer)
	lEnemies = []
	lTargetCities = []
	
	for iLoopPlayer in range(iNumPlayers):
		if tPlayer.isAtWar(iLoopPlayer):
			lEnemies.append(iLoopPlayer)
			
	for city in utils.getCityList(iPlayer):
		for iEnemy in lEnemies:
			pEnemy = gc.getPlayer(iEnemy)
			
			if 2 * city.getCulture(iEnemy) > city.getCulture(iPlayer):
				lTargetCities.append(city)
				break
				
			if city.getOriginalOwner() == iEnemy:
				lTargetCities.append(city)
				break
				
			if pEnemy.getWarValue(city.getX(), city.getY()) >= 8:
				lTargetCities.append(city)
				break
				
	return lTargetCities
		
def removeTargetCityDefenses(iPlayer):
	lTargetCities = getEnemyTargetCities(iPlayer)
	
	for city in lTargetCities:
		city.changeDefenseDamage(100)
		
	if utils.getHumanID() == iPlayer and len(lTargetCities) > 0:
		sText = localText.getText("TXT_KEY_STABILITY_REMOVE_DEFENSES", ())
		CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
		
def targetCityUnrest(iPlayer):
	lTargetCities = getEnemyTargetCities(iPlayer)
	
	for city in lTargetCities:
		city.setOccupationTimer(2)
		city.changeDefenseDamage(100)
		
	if utils.getHumanID() == iPlayer and len(lTargetCities) > 0:
		sText = localText.getText("TXT_KEY_STABILITY_TARGET_CITY_UNREST", ())
		CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
		
def immobilizeUnits(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	
	for x in range(124):
		for y in range(68):
			plot = gc.getMap().plot(x, y)
			for i in range(plot.getNumUnits()):
				unit = plot.getUnit(i)
				if unit.getOwner() == iPlayer and gc.getUnitInfo(unit.getUnitType()).isMilitaryProduction():
					unit.changeImmobileTimer(1)
			
	if utils.getHumanID() == iPlayer:
		sText = localText.getText("TXT_KEY_STABILITY_IMMOBILIZED_UNITS", ())
		CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
		
def unitDesertion(iPlayer, iDivisor):
	pPlayer = gc.getPlayer(iPlayer)
	lDesertingUnits = []
	
	for x in range(124):
		for y in range(68):
			plot = gc.getMap().plot(x, y)
			lPlotUnits = []
			for i in range(plot.getNumUnits()):
				unit = plot.getUnit(i)
				if unit.getOwner() == iPlayer and gc.getUnitInfo(unit.getUnitType()).isMilitaryProduction():
					lPlotUnits.append(unit)
			for i in range(len(lPlotUnits)):
				if i % iDivisor == 0:
					lDesertingUnits.append(lPlotUnits[i])		
			
	for unit in lDesertingUnits:
		x = unit.getX()
		y = unit.getY()
		plot = gc.getMap().plot(x, y)
		
		unit.kill(False, iBarbarian)#iPlayer)
		
	if utils.getHumanID() == iPlayer:
		sText = localText.getText("TXT_KEY_STABILITY_UNIT_DESERTION", (len(lDesertingUnits),))
		CyInterface().addMessage(iPlayer, False, iDuration, sText, "", 0, "", ColorTypes(iRed), -1, -1, True, True)
	
def calculateStability(iPlayer):
	iGameTurn = gc.getGame().getGameTurn()
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(pPlayer.getTeam())

	iExpansionStability = 0
	iEconomyStability = 0
	iDomesticStability = 0
	iForeignStability = 0
	iMilitaryStability = 0
	
	lParameters = [0 for i in range(iNumStabilityParameters)]
	
	# Collect required data
	iReborn = utils.getReborn(iPlayer)
	iStateReligion = pPlayer.getStateReligion()
	iCurrentEra = pPlayer.getCurrentEra()
	iNumTotalCities = pPlayer.getNumCities()
	iPlayerScore = pPlayer.getScoreHistory(iGameTurn)
	
	iCivicGovernment = pPlayer.getCivics(0)
	iCivicOrganization = pPlayer.getCivics(1)
	iCivicLabor = pPlayer.getCivics(2)
	iCivicEconomy = pPlayer.getCivics(3)
	iCivicReligion = pPlayer.getCivics(4)
	iCivicMilitary = pPlayer.getCivics(5)
	
	iCorePopulation = 10
	iPeripheryPopulation = 10
	iTotalCoreCities = 0
	iOccupiedCoreCities = 0
	
	iStateReligionCities = 0
	iOnlyStateReligionCities = 0
	iNonStateReligionCities = 0
		
	bTotalitarianism = (iCivicOrganization == iCivicTotalitarianism)
	bCityStates = (iCivicGovernment == iCivicCityStates)
	bMercantilism = (iCivicEconomy == iCivicMercantilism)
	bVassalage = (iCivicOrganization == iCivicVassalage)
	bEnvironmentalism = (iCivicEconomy == iCivicEnvironmentalism)
	bFanaticism = (iCivicReligion == iCivicFanaticism)
	bAutocracy = (iCivicGovernment == iCivicAutocracy)
	bMultilateralism = (iCivicMilitary == iCivicMultilateralism)
	
	bSingleCoreCity = (len(utils.getCoreCityList(iPlayer, iReborn)) == 1)
	
	for city in utils.getCityList(iPlayer):
		iPopulation = city.getPopulation()
		iModifier = 0
		x = city.getX()
		y = city.getY()
		plot = gc.getMap().plot(x,y)
		
		bHistorical = (plot.getSettlerValue(iPlayer) >= 90)
		
		iOwnCulture = plot.getCulture(iPlayer)
		iTotalCulture = 0
		
		bForeignCore = False
		for iLoopPlayer in range(iNumPlayers):
			iTempCulture = plot.getCulture(iLoopPlayer)
			if plot.isCore(iLoopPlayer):
				iTempCulture *= 2
				if iLoopPlayer != iPlayer and iGameTurn > getTurnForYear(tBirth[iLoopPlayer]):
					bForeignCore = True
			iTotalCulture += iTempCulture
			
		if iTotalCulture != 0:
			iCulturePercent = 100 * iOwnCulture / iTotalCulture
		else:
			iCulturePercent = 100
				
		bExpansionExceptions = ((bHistorical and iPlayer in [iMongolia]) or bTotalitarianism)
		#bExpansionExceptions = bTotalitarianism
		
		# Expansion
		if plot.isCore(iPlayer):
			iCorePopulation += (iCurrentEra + 1) * iPopulation
			if bSingleCoreCity and iCurrentEra > iAncient: iCorePopulation += iCurrentEra * iPopulation
		else:
			# ahistorical tiles
			if not bHistorical: iModifier += 2
			
			# colonies with Totalitarianism
			if isOverseas(city) and bHistorical and bTotalitarianism: iModifier += 1
			
			# not original owner
			if not bExpansionExceptions:
				if city.getOriginalOwner() != iPlayer and iGameTurn - city.getGameTurnAcquired() < utils.getTurns(25): iModifier += 1
			
			# not majority culture (includes foreign core and Persian UP)
			if iPlayer != iPersia:
				if iCulturePercent < 50: iModifier += 1
				if iCulturePercent < 20: iModifier += 1
			
			# foreign core (includes Persian UP)
			#if bForeignCore and iPlayer != iPersia: iModifier += 1
			
			# City States
			if bCityStates: iModifier += 2
			
			# Courthouse
			if city.hasBuilding(utils.getUniqueBuilding(iPlayer, iCourthouse)): iModifier -= 1
			
			# Jail
			if city.angryPopulation(0) == 0 and city.hasBuilding(utils.getUniqueBuilding(iPlayer, iJail)): iModifier -= 1
			
			# Portuguese UP: reduced instability from overseas colonies
			if isOverseas(city):
				if iPlayer == iPortugal: iModifier -= 1
				if bMercantilism and bHistorical: iModifier -= 1
					
			# cap
			if iModifier < -1: iModifier = -1
			
			#utils.debugTextPopup('City: ' + city.getName() + '\n Modifier: ' + str(iModifier))
			
			iPeripheryPopulation += (100 + iModifier * 50) * iPopulation / 100
			
			#if not bHistorical:
			#	if bForeignCore: iForeignCorePopulation += (100 + iModifier * 50) * iPopulation / 100
			#	else: iForeignPopulation += (100 + iModifier * 50) * iPopulation / 100
			#else:
			#	if bForeignCore: iContestedPopulation += (100 + iModifier * 50) * iPopulation / 100
			#	else: iHistoricalPopulation += (100 + iModifier * 50) * iPopulation / 100

			
		# Religions
		bNonStateReligion = False
		for iReligion in range(iNumReligions):
			if iReligion != iStateReligion and city.isHasReligion(iReligion):
				if not isTolerated(iPlayer, iReligion):
					bNonStateReligion = True
					break
				
		if city.isHasReligion(iStateReligion):
			iStateReligionCities += 1
			if not bNonStateReligion: iOnlyStateReligionCities += 1
			
		if iPlayer == iPoland:
			if iStateReligion in [iCatholicism, iOrthodoxy, iProtestantism]:
				for iReligion in [iCatholicism, iOrthodoxy, iProtestantism]:
					if iReligion != iStateReligion and city.isHasReligion(iReligion) and not city.isHasReligion(iStateReligion):
						iStateReligionCities += 1
						if not bNonStateReligion: iOnlyStateReligionCities += 1
				
		if bNonStateReligion: iNonStateReligionCities += 1
			
	#sPopulationDebug = 'Core Population: ' + str(iCorePopulation) + '\nHistorical population: ' + str(iHistoricalPopulation) + '\nContested population: ' + str(iContestedPopulation) + '\nForeign population: ' + str(iForeignPopulation) + '\nForeign core population: ' + str(iForeignCorePopulation)
	#utils.debugTextPopup(sPopulationDebug)
			
	#iCurrentCommerce = pPlayer.calculateTotalCommerce()
	#iPreviousCommerce = pPlayer.getEconomyHistory(iGameTurn - utils.getTurns(10))
	
	#iCurrentCommerceNeighbors = iPreviousCommerce * 11 / 10
	#iPreviousCommerceNeighbors = iPreviousCommerce
		
	#for iLoopPlayer in range(iNumPlayers):
	#	if pPlayer.canContact(iLoopPlayer):
	#		pLoopPlayer = gc.getPlayer(iLoopPlayer)
	#		iCurrentCommerceNeighbors += pLoopPlayer.calculateTotalCommerce()
	#		iPreviousCommerceNeighbors += pLoopPlayer.getEconomyHistory(iGameTurn - utils.getTurns(10))
			
	#iCurrentCommerceRank = calculateCommerceRank(iPlayer, iGameTurn)
	#iPreviousCommerceRank = calculateCommerceRank(iPlayer, iGameTurn - utils.getTurns(10))
	
	iCurrentPower = pPlayer.getPower()
	iPreviousPower = pPlayer.getPowerHistory(iGameTurn - utils.getTurns(10))
	
	# EXPANSION
	iExpansionStability = 0
	
	iCorePeripheryStability = 0
	iRazeCityStability = 0
	
	# Core vs. Periphery Populations
	if iCorePopulation == 0:
		iPeripheryExcess = 200
	else:
		iPeripheryExcess = 100 * iPeripheryPopulation / iCorePopulation - 100
	
	if iPeripheryExcess > 200: iPeripheryExcess = 200
		
	if iPeripheryExcess > 0:
		iCorePeripheryStability -= int(25 * sigmoid(1.0 * iPeripheryExcess / 100))
		
		iLastExpansionStability = sd.getLastExpansionStability(iPlayer)
		
		# cap changes between checks at +5
		if iLastExpansionStability - iCorePeripheryStability > 5: iCorePeripheryStability = iLastExpansionStability - 5
		
		sd.setLastExpansionStability(iPlayer, iCorePeripheryStability)
		
		utils.debugTextPopup('Expansion rating: ' + pPlayer.getCivilizationShortDescription(0) + '\nCore population: ' + str(iCorePopulation) + '\nPeriphery population: ' + str(iPeripheryPopulation) + '\nExpansion stability: ' + str(iCorePeripheryStability))
		
	lParameters[iParameterCorePeriphery] = iCorePeripheryStability
	lParameters[iParameterCoreScore] = iCorePopulation
	lParameters[iParameterPeripheryScore] = iPeripheryPopulation
		
	iExpansionStability += iCorePeripheryStability
	
	# apply raze city penalty
	iRazeCityStability = sd.getHumanRazePenalty()
	
	lParameters[iParameterRazedCities] = iRazeCityStability
		
	iExpansionStability += iRazeCityStability
	
	# ECONOMY
	iEconomyStability = 0
	
	# Economic Growth
	iEconomicGrowthStability = 3 * calculateTrendScore(sd.getEconomyTrend(iPlayer))
	
	lParameters[iParameterEconomicGrowth] = iEconomicGrowthStability
	
	iEconomyStability += iEconomicGrowthStability
	
	# Trade
	#iImports = pPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE)
	#iExports = pPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
	
	#if bMercantilism:
	#	iTradeVolume = 2 * iExports
	#else:
	#	iTradeVolume = iImports + iExports
	
	#iEraModifier = max(1, iCurrentEra * iCurrentEra)
		
	#if iNumTotalCities > 0:
	#	iTradeStability = iTradeVolume / iNumTotalCities - 2 * iEraModifier
	#else:
	#	iTradeStability = 0
		
	#iTradeStability /= 2
	
	# trade stability cap
	#if iTradeStability > 10: iTradeStability = 10
	#elif iTradeStability < -10: iTradeStability = -10
	
	iTradeStability = 0
	
	lParameters[iParameterTrade] = iTradeStability
	
	iEconomyStability += iTradeStability
	
	# Surplus and Deficit
	#iExpenseStability = 0
	#iTotalCommerce = pPlayer.calculateTotalCommerce()
	#iTotalCosts = pPlayer.calculateInflatedCosts()
	
	#if iTotalCommerce > 0:
	#	iExpenseRatio = 100 * iTotalCosts / iTotalCommerce
	#
	#	iExpenseStability = (25 - iExpenseRatio) / 5
	#	
	#	if iExpenseStability < -5: iExpenseStability = -5
	#	
	#	lParameters[iParameterExpenses] = iExpenseStability
		
	#iEconomyStability += iExpenseStability
	
	#utils.debugTextPopup("Trade stability: " + str(iTradeStability) + "\nExpenseStability: " + str(iExpenseStability))
	
	iTotalCommerce = pPlayer.calculateTotalCommerce()
	
	# Economic systems
	iEconomicSystemStability = 0
	bMercantilism = (iCivicEconomy == iCivicMercantilism)
	bCentralPlanning = (iCivicEconomy == iCivicCentralPlanning)
	if bMercantilism or bCentralPlanning:
		for iLoopPlayer in range(iNumPlayers):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if tPlayer.isOpenBorders(iLoopPlayer):
				if bMercantilism:
					if pLoopPlayer.calculateTotalCommerce() > iTotalCommerce:
						iEconomicSystemStability -= 2
				if bCentralPlanning:
					if pLoopPlayer.getCivics(3) == iCivicFreeMarket:
						iEconomicSystemStability -= 2
	
	if bMercantilism: lParameters[iParameterMercantilism] = iEconomicSystemStability
	if bCentralPlanning: lParameters[iParameterCentralPlanning] = iEconomicSystemStability
						
	iEconomyStability += iEconomicSystemStability
					
	# DOMESTIC
	iDomesticStability = 0
	
	# Happiness
	iHappinessStability = calculateTrendScore(sd.getHappinessTrend(iPlayer))
	
	#if iNumTotalCities > 0:
	#	if iHappyCities > iUnhappyCities:
	#		iHappinessStability += min(iNumTotalCities, 10 * (iHappyCities - iUnhappyCities) / iNumTotalCities)
	#	else:
	#		iHappinessStability -= min(iNumTotalCities, 10 * (iUnhappyCities - iHappyCities) / iNumTotalCities)
	
	#utils.debugTextPopup(pPlayer.getCivilizationShortDescription(0) + ' happiness stability: ' + str(iHappinessStability) + '\nHappy cities: ' + str(iHappyCities) + '\nUnhappy cities: ' + str(iUnhappyCities) + '\nTotal cities: ' + str(iNumTotalCities))
	
	lParameters[iParameterHappiness] = iHappinessStability
	
	iDomesticStability += iHappinessStability
	
	# Civics (combinations)
	iCivicStability = 0
	lCivics = [iCivicGovernment, iCivicOrganization, iCivicLabor, iCivicEconomy, iCivicReligion, iCivicMilitary]
	lCombinations = [(iCivic1, iCivic2) for iCivic1 in lCivics for iCivic2 in lCivics if iCivic1 < iCivic2]
	
	for lCombination in lCombinations:
		iCivicStability += getCivicCombinationStability(iPlayer, lCombination[0], lCombination[1])
		
	if utils.getHumanID() != iPlayer and iCivicStability < 0: iCivicStability /= 2
		
	iCivicCombinationStability = iCivicStability
	
	lParameters[iParameterCivicCombinations] = iCivicCombinationStability
	
	iCivicStability = 0
	
	# Civics (eras and techs)
	if iCivicOrganization == iCivicVassalage:
		if iCurrentEra == iMedieval: iCivicStability += 2
		elif iCurrentEra >= iIndustrial: iCivicStability -= 5
		
	if iCivicGovernment == iCivicTheocracy:
		if iCurrentEra >= iIndustrial: iCivicStability -= 5
		
	if iCivicReligion == iCivicPantheon:
		if iCurrentEra <= iClassical: iCivicStability += 2
		else: iCivicStability -= 2 * iCurrentEra
		
	if iCivicGovernment == iCivicCityStates:
		if iCurrentEra <= iClassical: iCivicStability += 2
		elif iCurrentEra >= iIndustrial: iCivicStability -= 5
		
	if tPlayer.isHasTech(iDemocracy):
		if iCivicOrganization not in [iCivicRepresentation, iCivicEgalitarianism, iCivicTotalitarianism]: iCivicStability -= 5
		if iCivicLabor in [iCivicSlavery, iCivicAgrarianism] and iCivicOrganization != iCivicTotalitarianism: iCivicStability -= 5
		
	if tPlayer.isHasTech(iCommunism):
		if iCivicOrganization not in [iCivicEgalitarianism, iCivicTotalitarianism]: iCivicStability -= 5
		
	if tPlayer.isHasTech(iCorporation):
		if iCivicEconomy in [iCivicSubsistence, iCivicGuilds]: iCivicStability -= 5
		
	if tPlayer.isHasTech(iEconomics):
		if iCivicLabor == iCivicSlavery and iCivicOrganization != iCivicTotalitarianism: iCivicStability -= 5
		
	if tPlayer.isHasTech(iNationalism):
		if iCivicMilitary == iCivicMercenaries: iCivicStability -= 5
		
	if utils.getHumanID() != iPlayer and iCivicStability < 0: iCivicStability /= 2
	
	iCivicEraTechStability = iCivicStability
	
	lParameters[iParameterCivicsEraTech] = iCivicEraTechStability
	
	iDomesticStability += iCivicCombinationStability + iCivicEraTechStability
	
	# Religion
	iReligionStability = 0
	
	if iNumTotalCities > 0:
		iHeathenRatio = 100 * iNonStateReligionCities / iNumTotalCities
		iHeathenThreshold = 30
		iBelieverThreshold = 75
		if iCivicReligion == iCivicFanaticism: iHeathenThreshold = 0
		
		if iHeathenRatio > iHeathenThreshold:
			iReligionStability -= (iHeathenRatio - iHeathenThreshold) / 10
			
		if iStateReligion != -1:
			iStateReligionRatio = 100 * iStateReligionCities / iNumTotalCities
			iBelieverStability = (iStateReligionRatio - iBelieverThreshold) / 5
			
			# cap at -10 for threshold = 75
			iCap = 2 * (iBelieverThreshold - 100) / 5
			if iBelieverStability < iCap: iBelieverStability = iCap
			
			iReligionStability += iBelieverStability
		
			if iCivicGovernment == iCivicTheocracy:
				iOnlyStateReligionRatio = 100 * iOnlyStateReligionCities / iNumTotalCities
				iReligionStability += iOnlyStateReligionRatio / 20
	
	lParameters[iParameterReligion] = iReligionStability
		
	iDomesticStability += iReligionStability
	
	# FOREIGN
	iForeignStability = 0
	iNeighborStability = 0
	iVassalStability = 0
	iDefensivePactStability = 0
	iRelationStability = 0
	iAutocracyStability = 0
	iFanaticismStability = 0
	iMultilateralismStability = 0
	
	iNumContacts = 0
	
	for iLoopPlayer in range(iNumPlayers):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		tLoopPlayer = gc.getTeam(pLoopPlayer.getTeam())
		iLoopScore = pLoopPlayer.getScoreHistory(iGameTurn)
	
		# neighbor stability
		if utils.isNeighbor(iPlayer, iLoopPlayer) or iLoopPlayer in lNeighbours[iPlayer]:
			if tPlayer.isOpenBorders(iLoopPlayer):
				#if getStabilityLevel(iLoopPlayer) == iStabilityUnstable: iNeighborStability -= 3
				#elif getStabilityLevel(iLoopPlayer) == iStabilityCollapsing: iNeighborStability -= 5
				if getStabilityLevel(iLoopPlayer) == iStabilityCollapsing: iNeighborStability -= 3
				
		# vassal stability
		if tLoopPlayer.isVassal(iPlayer):
			if getStabilityLevel(iLoopPlayer) == iStabilityCollapsing: iVassalStability -= 3
			elif getStabilityLevel(iLoopPlayer) == iStabilityUnstable: iVassalStability -= 1
			elif getStabilityLevel(iLoopPlayer) == iStabilitySolid: iVassalStability += 2
			
			if bVassalage: iVassalStability += 2
			
		# defensive pacts
		if tPlayer.isDefensivePact(iLoopPlayer):
			if iLoopScore > iPlayerScore: iDefensivePactStability += 5
			if bMultilateralism: iDefensivePactStability += 3
			
		# open borders
		if tPlayer.canContact(iLoopPlayer):
			#if pLoopPlayer.getStateReligion() == iStateReligion: iRelationStability += 1
			#else: iRelationStability += 2
			
			if tPlayer.isOpenBorders(iLoopPlayer):
				iRelationStability += 1
			
			iNumContacts += 1
			
		# bad relations
		#if pLoopPlayer.AI_getAttitude(iPlayer) == AttitudeTypes.ATTITUDE_FURIOUS and not tPlayer.isAtWar(iLoopPlayer): iRelationStability -= 2
		
		# worst enemies
		if pLoopPlayer.getWorstEnemy() == iPlayer:
			if iLoopScore > iPlayerScore: iRelationStability -= 4
			
		# wars
		if bAutocracy:
			if utils.isNeighbor(iPlayer, iLoopPlayer) and tPlayer.isAtWar(iLoopPlayer): iAutocracyStability += 2
		if bFanaticism:
			if tPlayer.isAtWar(iLoopPlayer):
				if pLoopPlayer.getStateReligion() != iStateReligion: iFanaticismStability += 3
				else: iFanaticismStability -= 2
		if bMultilateralism:
			if tPlayer.isAtWar(iLoopPlayer):
				iMultilateralismStability -= 2
		
	# penalize contacts because they allow more OB treaties
	iRelationStability -= (iNumContacts / 2 + min(4, iNumContacts))
	
	if iNumContacts <= 2 * min(iCurrentEra, 2) + 1:
		iRelationStability = 0
	
	lParameters[iParameterNeighbors] = iNeighborStability
	lParameters[iParameterVassals] = iVassalStability
	lParameters[iParameterDefensivePacts] = iDefensivePactStability
	lParameters[iParameterRelations] = iRelationStability
	lParameters[iParameterAutocracy] = iAutocracyStability
	lParameters[iParameterFanaticism] = iFanaticismStability
	lParameters[iParameterMultilateralism] = iMultilateralismStability
			
	iForeignStability += iNeighborStability + iVassalStability + iDefensivePactStability + iRelationStability + iAutocracyStability + iFanaticismStability + iMultilateralismStability
	
	# MILITARY
	
	iMilitaryStability = 0
	
	iWarSuccessStability = 0
	iMilitaryStrengthStability = 0
	iBarbarianLossesStability = 0
	
	iWarSuccessStability = 0 # war success (conquering cities and defeating units)
	iWarWearinessStability = 0 # war weariness in comparison to war length
	iBarbarianLossesStability = 0 # like previously
	
	# iterate ongoing wars
	for iEnemy in range(iNumPlayers):
		pEnemy = gc.getPlayer(iEnemy)
		if pEnemy.isAlive() and tPlayer.isAtWar(iEnemy):
			iTempWarSuccessStability = calculateTrendScore(sd.getWarTrend(iPlayer, iEnemy))
			if iTempWarSuccessStability > 0: iTempWarSuccessStability /= 2
			
			iWarSuccessStability += iTempWarSuccessStability
			
			iOurWarWeariness = tPlayer.getWarWeariness(iEnemy)
			iTheirWarWeariness = gc.getTeam(iEnemy).getWarWeariness(iPlayer)
			
			iWarTurns = iGameTurn - sd.getWarStartTurn(iPlayer, iEnemy)
			iDurationModifier = 0
			
			if iWarTurns > utils.getTurns(20):
				iDurationModifier = min(9, (iWarTurns - utils.getTurns(20)) / utils.getTurns(10))
				
			iTempWarWearinessStability = (iTheirWarWeariness - iOurWarWeariness) / (5000 * (iDurationModifier + 1))
			if iTempWarWearinessStability > 0: iTempWarWearinessStability = 0
			
			iWarWearinessStability += iTempWarWearinessStability
			
			utils.debugTextPopup(pPlayer.getCivilizationAdjective(0) + ' war against ' + pEnemy.getCivilizationShortDescription(0) + '\nWar Success Stability: ' + str(iTempWarSuccessStability) + '\nWar Weariness: ' + str(iTempWarWearinessStability))
	
	lParameters[iParameterWarSuccess] = iWarSuccessStability
	lParameters[iParameterWarWeariness] = iWarWearinessStability
	
	iMilitaryStability = iWarSuccessStability + iWarWearinessStability
	
	#iNumerator = 0
	#iDenominator = 0
	
	# war success
	#for iLoopPlayer in range(iNumPlayers):
	#	if tPlayer.isAtWar(iLoopPlayer) and gc.getPlayer(iLoopPlayer).isAlive():
	#		# our success = their war weariness and vice versa
	#		iOurSuccess = gc.getTeam(iLoopPlayer).getWarWeariness(iPlayer)  #tPlayer.AI_getWarSuccess(iLoopPlayer)
	#		iTheirSuccess = tPlayer.getWarWeariness(iLoopPlayer)  #gc.getTeam(iLoopPlayer).AI_getWarSuccess(iPlayer)
	#		iCombinedSuccess = iOurSuccess + iTheirSuccess
	#		
	#		# ignore insignificant wars
	#		if iCombinedSuccess < 20: continue
	#		
	#		iThisWarSuccess = 100 * iOurSuccess / iCombinedSuccess - 50
	#		
	#		iNumerator += iThisWarSuccess
	#		iDenominator += 1
				
			#utils.debugTextPopup(pPlayer.getCivilizationAdjective(0) + ' war against ' + gc.getPlayer(iLoopPlayer).getCivilizationShortDescription(0) + '\n' + pPlayer.getCivilizationAdjective(0) + ' success: ' + str(iOurSuccess) + '\n' + gc.getPlayer(iLoopPlayer).getCivilizationAdjective(0) + ' success: ' + str(iTheirSuccess) + '\nResulting stability: ' + str(iThisWarStability))
			
	#if iDenominator > 0:
	#	iTotalSuccess = iNumerator / iDenominator
		
	#	if iTotalSuccess > 0:
	#		iWarSuccessStability = 20 * iTotalSuccess / 100
	#	else:
	#		iWarSuccessStability = int(20 * sigmoid(1.0 * iTotalSuccess / 100))
	#	
	#	sLogString = pPlayer.getCivilizationAdjective(0) + ' total war success: ' + str(iTotalSuccess) + '\nStability: ' + str(iWarSuccessStability)
		
		#utils.debugTextPopup(sLogString)
	
	#lParameters[iParameterWarSuccess] = iWarSuccessStability
				
	#iMilitaryStability += iWarSuccessStability
				
	# military strength
	#if iPreviousPower != 0:
	#	iPowerDifference = iCurrentPower - iPreviousPower
	#	iPercentChange = 100 * iPowerDifference / iPreviousPower
	#	
	#	if iPercentChange < 0:
	#		iMilitaryStrengthStability = iPercentChange / 2
	#		if iMilitaryStrengthStability < -10: iMilitaryStrengthStability = -10
	#	
	#	#utils.debugTextPopup('Military strength: ' + pPlayer.getCivilizationShortDescription(0) + '\nCurrent power: ' + str(iCurrentPower) + '\nPrevious Power: ' + str(iPreviousPower) + '\nPercent change: ' + str(iPercentChange) + '\nStability change: ' + str(iMilitaryStrengthStability))
	#
	#lParameters[iParameterMilitaryStrength] = iMilitaryStrengthStability
	
	#iMilitaryStability += iMilitaryStrengthStability
	
	# apply barbarian losses
	iBarbarianLossesStability = -sd.getBarbarianLosses(iPlayer)
	
	lParameters[iParameterBarbarianLosses] = iBarbarianLossesStability
	
	iMilitaryStability += iBarbarianLossesStability
	
	iStability = iExpansionStability + iEconomyStability + iDomesticStability + iForeignStability + iMilitaryStability
	
	#utils.debugTextPopup(pPlayer.getCivilizationAdjective(0) + ' Stability: ' + str(iStability) + '\nExpansion: ' + str(iExpansionStability) + '\nEconomy: ' + str(iEconomyStability) + '\nDomestic: ' + str(iDomesticStability) + '\nForeign: ' + str(iForeignStability) + '\nMilitary: ' + str(iMilitaryStability))

	return iStability, [iExpansionStability, iEconomyStability, iDomesticStability, iForeignStability, iMilitaryStability], lParameters
	
def getCivicCombinationStability(iPlayer, iCivic1, iCivic2):
	iCurrentEra = gc.getPlayer(iPlayer).getCurrentEra()
	lCivics = set([iCivic1, iCivic2])
	
	if iCivicTotalitarianism in lCivics:
		if iCivicAutocracy in lCivics: return 5
		if iCivicCentralPlanning in lCivics: return 3
		if other(lCivics, iCivicSecularism): return -5
		
	if iCivicCentralPlanning in lCivics:
		if iCivicIndustrialism in lCivics: return 2
		if other(lCivics, iCivicIndustrialism, iCivicPublicWelfare): return -5
		
	if iCivicEgalitarianism in lCivics:
		if iCivicRepublic in lCivics: return 2
		if other(lCivics, iCivicPublicWelfare): return -3
		if iCivicEnvironmentalism in lCivics: return 2
		if iCivicSecularism in lCivics: return 2
		
	if iCivicCapitalism in lCivics:
		if iCivicRepresentation in lCivics: return 2
		if iCivicFreeMarket in lCivics: return 3
		if iCivicGuilds in lCivics: return -5
		
	if iCivicEnvironmentalism in lCivics:
		if iCivicIndustrialism in lCivics: return -5
		
	if iCivicTheocracy in lCivics:
		if iCivicFanaticism in lCivics: return 5
		if iCivicOrganizedReligion in lCivics: return 3
		if iCivicSecularism in lCivics: return -7
		if iCivicEgalitarianism in lCivics: return -3
		
	if iCivicVassalage in lCivics:
		if iCivicLevyArmies in lCivics: return 3
		if other(lCivics, iCivicLevyArmies): return -5
		
		if only(lCivics, iCivicCapitalism, iCivicIndustrialism, iCivicPublicWelfare): return -5
		
		if iCurrentEra == iMedieval:
			if iCivicDynasticism in lCivics: return 2
			if iCivicAgrarianism in lCivics: return 3
			
	if iCivicCityStates in lCivics:
		if only(lCivics, iCivicVassalage, iCivicAbsolutism, iCivicEgalitarianism): return -3
		if iCivicGuilds in lCivics: return 2
		if only(lCivics, iCivicFreeMarket, iCivicCentralPlanning, iCivicEnvironmentalism): return -5
		if only(lCivics, iCivicMilitia, iCivicMercenaries): return 2
		if only(lCivics, iCivicLevyArmies, iCivicStandingArmy, iCivicMultilateralism): return -3
		
	if iCivicAbsolutism in lCivics:
		if iCivicRepublic in lCivics: return -5
		if iCivicMercantilism in lCivics: return 3
		if iCivicOrganizedReligion in lCivics: return 2
		
		if iCurrentEra == iRenaissance:
			if iCivicDynasticism in lCivics: return 2
			
	if iCivicRepublic in lCivics:
		if iCivicRepresentation in lCivics: return 2
		
	if iCivicAutocracy in lCivics:
		if iCivicStandingArmy in lCivics: return 3
		
	if iCivicMultilateralism in lCivics:
		if iCivicAutocracy in lCivics: return -2
		if iCivicTotalitarianism in lCivics: return -3
		if iCivicEgalitarianism in lCivics: return 2
		if iCivicFanaticism in lCivics: return -3
		
	return 0
	
def only(lCombination, *civics):
	lCivics = [iCivic for iCivic in civics]
	return set(lCivics) & lCombination
	
def other(lCombination, *civics):
	iCategory = gc.getCivicInfo(civics[0]).getCivicOptionType()
	lCivics = [iCivic for iCivic in range(iNumCivics) if gc.getCivicInfo(iCivic).getCivicOptionType() == iCategory and iCivic not in civics]
	return set(lCivics) & lCombination

def sigmoid(x):
	#return 2.0 / (1 + math.exp(-5*x)) - 1.0
	return math.tanh(5 * x / 2)
	
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
	
def updateEconomyTrend(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	
	if not pPlayer.isAlive(): return
	
	#iCivicLabor = pPlayer.getCivics(2)
	#iCivicEconomy = pPlayer.getCivics(3)
	
	#bPublicWelfare = (iCivicLabor == iCivicPublicWelfare)
	#bFreeMarket = (iCivicEconomy == iCivicFreeMarket)
	#bEnvironmentalism = (iCivicEconomy == iCivicEnvironmentalism)
	
	iPreviousCommerce = sd.getPreviousCommerce(iPlayer)
	iCurrentCommerce = pPlayer.calculateTotalCommerce()
	
	if iPreviousCommerce == 0: 
		sd.setPreviousCommerce(iPlayer, iCurrentCommerce)
		return
	
	iPercentChange = 100 * iCurrentCommerce / iPreviousCommerce - 100
	
	if iPercentChange > 5: sd.pushEconomyTrend(iPlayer, 1)
	elif iPercentChange < 0: sd.pushEconomyTrend(iPlayer, -1)
	else: sd.pushEconomyTrend(iPlayer, 0)
	
	sd.setPreviousCommerce(iPlayer, iCurrentCommerce)
	
def updateHappinessTrend(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	
	if not pPlayer.isAlive(): return
	
	iNumCities = pPlayer.getNumCities()
	
	if iNumCities == 0: return
	
	iHappyCities = 0
	iUnhappyCities = 0
	
	iAveragePopulation = pPlayer.getAveragePopulation()
	
	for city in utils.getCityList(iPlayer):
		iPopulation = city.getPopulation()
		iHappiness = city.happyLevel()
		iUnhappiness = city.unhappyLevel(0)
		iOvercrowding = city.getOvercrowdingPercentAnger(0) * city.getPopulation() / 1000
		
		if city.isWeLoveTheKingDay() or (iPopulation >= iAveragePopulation and iHappiness - iUnhappiness >= iAveragePopulation / 4):
			iHappyCities += 1
		elif iUnhappiness - iOvercrowding > iPopulation / 5 or iUnhappiness - iHappiness > 0:
			iUnhappyCities += 1
			
	if iHappyCities - iUnhappyCities > math.ceil(iNumCities / 5.0): sd.pushHappinessTrend(iPlayer, 1)
	elif iUnhappyCities - iHappyCities > math.ceil(iNumCities / 5.0): sd.pushHappinessTrend(iPlayer, -1)
	
def updateWarTrend(iPlayer, iEnemy):
	iPreviousTrend = sd.getLastWarTrend(iPlayer, iEnemy)
	
	iWarTurns = gc.getGame().getGameTurn() - sd.getWarStartTurn(iPlayer, iEnemy)
	iDurationModifier = min(5, iWarTurns / utils.getTurns(10))
	
	iOurSuccess = gc.getTeam(iPlayer).AI_getWarSuccess(iEnemy)
	iTheirSuccess = gc.getTeam(iEnemy).AI_getWarSuccess(iPlayer)
	
	if abs(iOurSuccess - iTheirSuccess) > max(iTheirSuccess, iOurSuccess) / (10 - iDurationModifier):
		iCurrentTrend = iPreviousTrend / 2 + iOurSuccess - iTheirSuccess
	else:
		iCurrentTrend = 0
	
	sd.pushWarTrend(iPlayer, iEnemy, iCurrentTrend)
	
def startWar(iPlayer, iEnemy):
	sd.setWarTrend(iPlayer, iEnemy, [])
	sd.setWarTrend(iEnemy, iPlayer, [])
	
	iGameTurn = gc.getGame().getGameTurn()
	sd.setWarStartTurn(iPlayer, iEnemy, iGameTurn)
	sd.setWarStartTurn(iEnemy, iPlayer, iGameTurn)
	
def calculateEconomicGrowth(iPlayer, iNumTurns):
	lHistory = []
	pPlayer = gc.getPlayer(iPlayer)
	iCurrentTurn = gc.getGame().getGameTurn()
	
	for iTurn in range(iCurrentTurn - iNumTurns, iCurrentTurn):
		iHistory = pPlayer.getEconomyHistory(iTurn)
		if iHistory > 1:
			lHistory.append((iTurn - iCurrentTurn + iNumTurns, iHistory))
	
	lHistory.append((iNumTurns, pPlayer.calculateTotalCommerce()))
			
	a, b = utils.linreg(lHistory)
	
	iNormalizedStartTurn = b
	iNormalizedCurrentTurn = a * iNumTurns + b
	
	if iNormalizedStartTurn == 0.0: return 0
	
	iGrowth = int(100 * (iNormalizedCurrentTurn - iNormalizedStartTurn) / iNormalizedStartTurn)
	
	return iGrowth
	
def calculateEconomicGrowthNeighbors(iPlayer, iNumTurns):
	lHistory = []
	lContacts = []
	pPlayer = gc.getPlayer(iPlayer)
	iCurrentTurn = gc.getGame().getGameTurn()
	
	for iLoopPlayer in range(iNumPlayers):
		if pPlayer.canContact(iLoopPlayer):
			lContacts.append(iLoopPlayer)
			
	for iTurn in range(iCurrentTurn - iNumTurns, iCurrentTurn):
		iHistory = pPlayer.getEconomyHistory(iTurn)
		for iLoopPlayer in lContacts:
			iHistory += gc.getPlayer(iLoopPlayer).getEconomyHistory(iTurn)
		if iHistory > 1:
			lHistory.append((iTurn - iCurrentTurn + iNumTurns, iHistory))
			
	iHistory = pPlayer.calculateTotalCommerce()
	for iLoopPlayer in lContacts:
		iHistory += gc.getPlayer(iLoopPlayer).calculateTotalCommerce()
		
	lHistory.append((iCurrentTurn, iHistory))
	
	a, b = utils.linreg(lHistory)
	
	iNormalizedStartTurn = b
	iNormalizedCurrentTurn = a * iNumTurns + b
	
	iGrowth = int(100 * (iNormalizedCurrentTurn - iNormalizedStartTurn) / iNormalizedStartTurn)
	
	return iGrowth

def determineCrisisType(lStabilityTypes):
	iLowestEntry = utils.getHighestEntry(lStabilityTypes, lambda x: -x)
	return lStabilityTypes.index(iLowestEntry)
	
def calculateCommerceRank(iPlayer, iTurn):
	lCommerceValues = utils.getSortedList([i for i in range(iNumPlayers)], lambda x : gc.getPlayer(x).getEconomyHistory(iTurn), True)
	return lCommerceValues.index(iPlayer)
	
def calculatePowerRank(iPlayer, iTurn):
	lPowerValues = utils.getSortedList([i for i in range(iNumPlayers)], lambda x : gc.getPlayer(x).getPowerHistory(iTurn), True)
	return lPowerValues.index(iPlayer)
	
def isTolerated(iPlayer, iReligion):
	pPlayer = gc.getPlayer(iPlayer)
	iStateReligion = pPlayer.getStateReligion()
	
	# should not be asked, but still check
	if iStateReligion == iReligion: return True
	
	# Secularism civic
	if pPlayer.getCivics(4) == iCivicSecularism: return True
	
	# Mughal UP
	if iPlayer == iMughals: return True
	
	# Exceptions
	if iStateReligion == iConfucianism and iReligion == iTaoism: return True
	if iStateReligion == iTaoism and iReligion == iConfucianism: return True
	if iStateReligion == iHinduism and iReligion == iBuddhism: return True
	if iStateReligion == iBuddhism and iReligion == iHinduism: return True
	
	return False
	
def isOverseas(city):
	capital = gc.getPlayer(city.getOwner()).getCapitalCity()
	
	return (capital.plot().getArea() != city.plot().getArea())

def checkResurrection(iGameTurn):

	#print '\nCheck resurrection'

	iNationalismModifier = min(20, 4 * utils.getCivsWithNationalism())
	
	lPossibleResurrections = []
	bDeadCivFound = False
	
	# iterate all civs starting with a random civ
	for iLoopCiv in range(iNumPlayers):
		if utils.canRespawn(iLoopCiv):
			lPossibleResurrections.append(iLoopCiv)
				
	for iLoopCiv in utils.getSortedList(lPossibleResurrections, lambda x: utils.getLastTurnAlive(x)):
		iMinNumCities = 2
		
		# special case Netherlands: need only one city to respawn (Amsterdam)
		if iLoopCiv == iNetherlands:
			iMinNumCities = 1
					
		iRespawnRoll = gc.getGame().getSorenRandNum(100, 'Respawn Roll')
		if iRespawnRoll - iNationalismModifier + 10 < tResurrectionProb[iLoopCiv]:
			#print 'Passed respawn roll'
			lCityList = getResurrectionCities(iLoopCiv)
			if len(lCityList) >= iMinNumCities:
				#print 'Enough cities -> doResurrection()'
				doResurrection(iLoopCiv, lCityList)
				return
						
def getResurrectionCities(iPlayer, bFromCollapse = False):
	pPlayer = gc.getPlayer(iPlayer)
	teamPlayer = gc.getTeam(iPlayer)
	lPotentialCities = []
	lFlippingCities = []
	
	iMinNumCitiesOwner = 3
	tCapital = Areas.getRespawnCapital(iPlayer)
		
	for (x, y) in Areas.getRespawnArea(iPlayer):
		plot = gc.getMap().plot(x, y)
		if plot.isCity():
			city = plot.getPlotCity()
			# for humans: exclude recently conquered cities to avoid annoying reflips
			if city.getOwner() != utils.getHumanID() or city.getGameTurnAcquired() < gc.getGame().getGameTurn() - utils.getTurns(5):
				lPotentialCities.append(city)
					
	for k in range(len(lPotentialCities)):
		city = lPotentialCities[k]
		iOwner = city.getOwner()
		
		# barbarian and minor cities always flip
		if iOwner >= iNumPlayers:
			lFlippingCities.append(city)
			continue
			
		iOwnerStability = utils.getStabilityLevel(iOwner)
		bCapital = ((city.getX(), city.getY()) == tCapital)
		
		# flips are less likely before Nationalism
		if utils.getCivsWithNationalism() == 0:
			iOwnerStability += 1
			
		if utils.getHumanID() != iOwner:
			iMinNumCitiesOwner = 2
			iOwnerStability -= 1
			
		if gc.getPlayer(iOwner).getNumCities() >= iMinNumCitiesOwner:
		
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
				ownerCapital = gc.getPlayer(iOwner).getCapitalCity()
				iDistance = utils.calculateDistance(city.getX(), city.getY(), ownerCapital.getX(), ownerCapital.getY())
				if bCapital or iDistance >= 8:
					lFlippingCities.append(city)
				
			# owner stability below solid: only capital spot flips
			elif iOwnerStability < iStabilitySolid:
				if bCapital:
					lFlippingCities.append(city)
					
		# if only up to two cities wouldn't flip, they flip as well (but at least one city has to flip already, else the respawn fails)
		if len(lFlippingCities) + 2 >= len(lPotentialCities) and len(lFlippingCities) > 0 and len(lFlippingCities) * 2 >= len(lPotentialCities) and not bFromCollapse:
			lFlippingCities = []
			# cities in core are not affected by this
			for city in lPotentialCities:
				if not city.plot().isCore(city.getOwner()):
					lFlippingCities.append(city)
			
	return lFlippingCities
	
def resurrectionFromCollapse(iPlayer, lCityList):

	# collect other cities that could flip
	for city in getResurrectionCities(iPlayer, True):
		if city not in lCityList:
			lCityList.append(city)
			
	doResurrection(iPlayer, lCityList)
	
def doResurrection(iPlayer, lCityList, bAskFlip = True):
	pPlayer = gc.getPlayer(iPlayer)
	teamPlayer = gc.getTeam(iPlayer)

	sd.setRebelCiv(iPlayer)
	
	for iOtherCiv in range(iNumPlayers):
		teamPlayer.makePeace(iOtherCiv)
		
		if teamPlayer.isVassal(iOtherCiv):
			gc.getTeam(iOtherCiv).freeVassal(iPlayer)
			
		if gc.getTeam(iOtherCiv).isVassal(iPlayer):
			teamPlayer.freeVassal(iOtherCiv)
		
	sd.setNumPreviousCities(iPlayer, 0)
	
	pPlayer.AI_reset()
	
	iHuman = utils.getHumanID()
			
	# assign technologies
	lTechs = getResurrectionTechs(iPlayer)
	for iTech in lTechs:
		teamPlayer.setHasTech(iTech, True, iPlayer, False, False)
		
	# determine army size
	iNumCities = len(lCityList)
	iGarrison = 2
	iArmySize = pPlayer.getCurrentEra()
	
	pPlayer.setLatestRebellionTurn(gc.getGame().getGameTurn())
		
	# add former colonies that are still free
	for iMinor in range(iNumPlayers, iNumTotalPlayersB): # including barbarians
		if gc.getPlayer(iMinor).isAlive():
			for city in utils.getCityList(iMinor):
				if city.getOriginalOwner() == iPlayer:
					x = city.getX()
					y = city.getY()
					if pPlayer.getSettlerValue(x, y) >= 90:
						if city not in lCityList:
							lCityList.append(city)

	lOwners = []
	
	for city in lCityList:
		iOwner = city.getOwner()
		pOwner = gc.getPlayer(iOwner)
		
		x = city.getX()
		y = city.getY()
		
		bCapital = city.isCapital()
		
		if pOwner.isBarbarian() or pOwner.isMinorCiv():
			utils.completeCityFlip(x, y, iPlayer, iOwner, 100, False, True, True, True)
			utils.flipUnitsInArea((x-2, y-2), (x+2, y+2), iPlayer, iOwner, True, False)
	
		else:
			utils.completeCityFlip(x, y, iPlayer, iOwner, 75, False, True, True)
			
		newCity = gc.getMap().plot(x, y).getPlotCity()
		
		# Leoreth: rebuild some city infrastructure
		for iBuilding in range(iNumBuildings):
			if pPlayer.canConstruct(iBuilding, True, False, False) and newCity.canConstruct(iBuilding, True, False, False) and pPlayer.getCurrentEra() >= gc.getBuildingInfo(iBuilding).getFreeStartEra() and not utils.isUniqueBuilding(iBuilding) and gc.getBuildingInfo(iBuilding).getPrereqReligion() == -1:
				newCity.setHasRealBuilding(iBuilding, True)
			
		if bCapital and iOwner < iNumPlayers:
			relocateCapital(iOwner)
			
		if iOwner not in lOwners:
			lOwners.append(iOwner)
			
	for iOwner in lOwners:
		teamOwner = gc.getTeam(iOwner)
		bOwnerHumanVassal = teamOwner.isVassal(iHuman)
	
		if iOwner != iHuman and iOwner != iPlayer and iOwner != iBarbarian:
			iRand = gc.getGame().getSorenRandNum(100, 'Stop birth')
			
			if iRand >= tAIStopBirthThreshold[iOwner] and not bOwnerHumanVassal:
				teamOwner.declareWar(iPlayer, False, -1)
			else:
				teamOwner.makePeace(iPlayer)
				
	if len(utils.getCityList(iPlayer)) == 0:
		utils.debugTextPopup('Civ resurrected without any cities')
			
	relocateCapital(iPlayer, True)
	
	# give the new civ a starting army
	capital = pPlayer.getCapitalCity()
	x = capital.getX()
	y = capital.getY()
	
	utils.makeUnit(utils.getBestInfantry(iPlayer), iPlayer, (x,y), 2 * iArmySize + iNumCities)
	utils.makeUnit(utils.getBestCavalry(iPlayer), iPlayer, (x,y), iArmySize)
	utils.makeUnit(utils.getBestCounter(iPlayer), iPlayer, (x,y), iArmySize)
	utils.makeUnit(utils.getBestSiege(iPlayer), iPlayer, (x,y), iArmySize + iNumCities)
	
	# set state religion based on religions in the area
	setStateReligion(iPlayer)
		
	CyInterface().addMessage(iHuman, True, iDuration, CyTranslator().getText("TXT_KEY_INDEPENDENCE_TEXT", (pPlayer.getCivilizationAdjectiveKey(),)), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
	
	if bAskFlip and iHuman in lOwners:
		rebellionPopup(iPlayer)
		
	sd.setStabilityLevel(iPlayer, iStabilityStable)
	
	utils.setPlagueCountdown(iPlayer, -10)
	utils.clearPlague(iPlayer)
	convertBackCulture(iPlayer)
	
	# change the cores of some civs on respawn
	if iPlayer == iGreece:
		utils.setReborn(iGreece, True)
		
	elif iPlayer == iChina:
		if gc.getGame().getGameTurn() > getTurnForYear(tBirth[iMongolia]):
			utils.setReborn(iChina, True)
			
	elif iPlayer == iIndia:
		utils.setReborn(iIndia, gc.getGame().getGameTurn() < getTurnForYear(1900))
	
		
	# others revert to their old cores instead
	if iPlayer in [iArabia, iMongolia]:
		utils.setReborn(iPlayer, False)
	
	# resurrection leaders
	if iPlayer in resurrectionLeaders:
		if pPlayer.getLeader() != resurrectionLeaders[iPlayer]:
			pPlayer.setLeader(resurrectionLeaders[iPlayer])
			
	# Leoreth: report to dynamic civs
	dc.onCivRespawn(iPlayer, lOwners)
	
	return
	
def getResurrectionTechs(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	lTechList = []
	lSourceCivs = [iPlayer]
	
	# same tech group
	for lRegionList in lTechGroups:
		if iPlayer in lRegionList:
			for iPeer in lRegionList:
				if iPeer != iPlayer and gc.getPlayer(iPeer).isAlive():
					lSourceCivs.append(iPeer)
			
	# direct neighbors (India can benefit from England etc)
	for iPeer in range(iNumPlayers):
		if iPeer != iPlayer and iPeer not in lSourceCivs and gc.getPlayer(iPeer).isAlive():
			if utils.isNeighbor(iPlayer, iPeer):
				lSourceCivs.append(iPeer)
				
	# use independents as source civs in case no other can be found
	if len(lSourceCivs) == 0:
		lSourceCivs.append(iIndependent)
		lSourceCivs.append(iIndependent2)
	
	for iTech in range(iNumTechs):
			
		# at least half of the source civs know this technology
		iCount = 0
		for iOtherCiv in lSourceCivs:
			if gc.getTeam(iOtherCiv).isHasTech(iTech):
				iCount += 1
				
		if 2 * iCount >= len(lSourceCivs):
			lTechList.append(iTech)
			
	return lTechList
	
def relocateCapital(iPlayer, bResurrection = False):
	if iPlayer < iNumPlayers: return
	if gc.getPlayer(iPlayer).getNumCities() == 0: return

	tCapital = Areas.getCapital(iPlayer)
	oldCapital = gc.getPlayer(iPlayer).getCapitalCity()
	
	if bResurrection: tCapital = Areas.getRespawnCapital(iPlayer)
		
	x, y = tCapital
	plot = gc.getMap().plot(x, y)
	if plot.isCity() and plot.getPlotCity().getOwner() == iPlayer:
		newCapital = gc.getMap().plot(x, y).getPlotCity()	
	else:
		newCapital = utils.getHighestEntry(utils.getCityList(iPlayer), lambda x: max(0, utils.getTurns(500)-x.getGameTurnFounded()) + x.getPopulation()*5)
		
	oldCapital.setHasRealBuilding(iPalace, False)
	newCapital.setHasRealBuilding(iPalace, True)

def convertBackCulture(iCiv):
	for (x, y) in Areas.getRespawnArea(iCiv):
		plot = gc.getMap().plot(x, y)
		if plot.isCity():
			city = plot.getPlotCity()
			if city.getOwner() == iCiv:
				iCulture = 0
				for iMinor in range(iNumPlayers, iNumTotalPlayersB):
					iCulture += city.getCulture(iMinor)
					city.setCulture(iMinor, 0, True)
				city.changeCulture(iCiv, iCulture, True)
		elif plot.isCityRadius() and plot.getOwner() == iCiv:
			iCulture = 0
			for iMinor in range(iNumPlayers, iNumTotalPlayersB):
				iCulture += plot.getCulture(iMinor)
				plot.setCulture(iMinor, 0, True)
			plot.changeCulture(iCiv, iCulture, True)
		
def setStateReligion(iCiv):
	lCities = utils.getAreaCities(Areas.getCoreArea(iCiv))
	lReligions = [0 for i in range(iNumReligions)]
	
	for city in lCities:
		for iReligion in range(iNumReligions):
			if city.isHasReligion(iReligion): lReligions[iReligion] += 1
			
	iHighestEntry = utils.getHighestEntry(lReligions)
	
	if iHighestEntry > 0:
		gc.getPlayer(iCiv).setLastStateReligion(lReligions.index(iHighestEntry))

def rebellionPopup(iRebelCiv):
	utils.showPopup(7622, CyTranslator().getText("TXT_KEY_REBELLION_TITLE", ()), \
		       CyTranslator().getText("TXT_KEY_REBELLION_TEXT", (gc.getPlayer(iRebelCiv).getCivilizationAdjectiveKey(),)), \
		       (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), \
			CyTranslator().getText("TXT_KEY_POPUP_NO", ())))