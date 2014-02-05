# Rhye's and Fall of Civilization - Stability


from CvPythonExtensions import *
from StoredData import sd # edead
import Consts as con
import RFCUtils
import DynamicCivs
from operator import itemgetter
import math

utils = RFCUtils.RFCUtils()
dc = DynamicCivs.DynamicCivs()

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
	for iPlayer in range(con.iNumPlayers):
		if getCrisisCountdown(iPlayer) > 0:
			changeCrisisCountdown(iPlayer, -1)
			
	if iGameTurn % utils.getTurns(5) == 0:
		if sd.getHumanRazePenalty() < 0:
			sd.changeHumanRazePenalty(2)
		for iPlayer in range(con.iNumPlayers):
			if sd.getBarbarianLosses(iPlayer) > 0:
				sd.changeBarbarianLosses(iPlayer, -1)
			
	if iGameTurn % utils.getTurns(12) == 0:
		for iPlayer in range(con.iNumPlayers):
			checkLostCitiesCollapse(iPlayer)
			
	if iGameTurn >= getTurnForYear(con.tBirth[utils.getHumanID()]):
		sd.setHumanStability(calculateStability(utils.getHumanID()))

def onCityAcquired(city, iOwner, iPlayer):
	checkStability(iOwner)
	
	checkLostCoreCollapse(iOwner)
	
	if iPlayer == con.iBarbarian:
		checkBarbarianCollapse(iOwner)
	
def onCityRazed(iPlayer, city):
	if utils.getHumanID() == iPlayer:
		iRazePenalty = -10
		if city.getPopulation() < 5 and not city.isCapital():
			iRazePenalty = -2 * city.getPopulation()
		sd.changeHumanRazePenalty(-10)
		checkStability(iPlayer)
	
def onTechAcquired(iPlayer, iTech):
	checkStability(iPlayer)
	
def onVassalState(iMaster, iVassal):
	checkStability(iVassal)
	checkStability(iMaster, True)
	
	# update number of cities so vassals survive losing cities
	sd.setNumPreviousCities(iVassal, gc.getPlayer(iVassal).getNumCities())
	
def onChangeWar(bWar, iTeam, iOtherTeam):
	if iTeam < con.iNumPlayers and iOtherTeam < con.iNumPlayers:
		checkStability(iTeam, not bWar)
		checkStability(iOtherTeam, not bWar)
	
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
	
def onCombatResult(iWinningPlayer, iLosingPlayer):
	if iWinningPlayer == con.iBarbarian and iLosingPlayer < con.iNumPlayers:
		sd.changeBarbarianLosses(iLosingPlayer, 1)
	
def onCivSpawn(iPlayer):
	for iOlderNeighbor in con.lOlderNeighbours[iPlayer]:
		if gc.getPlayer(iOlderNeighbor).isAlive() and getStabilityLevel(iOlderNeighbor) > con.iStabilityShaky:
			decrementStability(iOlderNeighbor)
			#utils.debugTextPopup('Lost stability to neighbor spawn: ' + gc.getPlayer(iOlderNeighbor).getCivilizationShortDescription(0))

def getStabilityLevel(iPlayer):
	return sd.getStabilityLevel(iPlayer)
	
def setStabilityLevel(iPlayer, iStabilityLevel):
	sd.setStabilityLevel(iPlayer, iStabilityLevel)
	
def incrementStability(iPlayer):
	sd.setStabilityLevel(iPlayer, min(con.iStabilitySolid, sd.getStabilityLevel(iPlayer) + 1))
	
def decrementStability(iPlayer):
	sd.setStabilityLevel(iPlayer, max(con.iStabilityCollapsing, sd.getStabilityLevel(iPlayer) - 1))
	
def getCrisisCountdown(iPlayer):
	return sd.getCrisisCountdown(iPlayer)
	
def changeCrisisCountdown(iPlayer, iChange):
	sd.changeCrisisCountdown(iPlayer, iChange)
	
def checkBarbarianCollapse(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iGameTurn = gc.getGame().getGameTurn()
	
	# must not be dead
	if not pPlayer.isAlive() or pPlayer.getNumCities() == 0:
		return
		
	# only for major civs
	if iPlayer >= con.iNumPlayers:
		return
		
	# immune right after scenario start
	if iGameTurn - utils.getScenarioStartTurn() < utils.getTurns(20):
		return
		
	# immune right after birth
	if iGameTurn - getTurnForYear(con.tBirth[iPlayer]) < utils.getTurns(20):
		return
		
	# immune right after resurrection
	if iGameTurn - pPlayer.getLatestRebellionTurn() < utils.getTurns(10):
		return
		
	iNumCities = pPlayer.getNumCities()
	iLostCities = 0
	
	for city in utils.getCityList(con.iBarbarian):
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
	
	# must not be dead
	if not pPlayer.isAlive() or pPlayer.getNumCities() == 0:
		return
		
	# only for major civs
	if iPlayer >= con.iNumPlayers:
		return
		
	# immune right after scenario start
	if iGameTurn - utils.getScenarioStartTurn() < utils.getTurns(20):
		return
		
	# immune right after birth
	if iGameTurn - getTurnForYear(con.tBirth[iPlayer]) < utils.getTurns(20):
		return
		
	# immune right after resurrection
	if iGameTurn - pPlayer.getLatestRebellionTurn() < utils.getTurns(10):
		return
		
	iNumCurrentCities = pPlayer.getNumCities()
	iNumPreviousCities = sd.getNumPreviousCities(iPlayer)
	
	# half or less cities than 12 turns ago: collapse (exceptions for civs with very little cities to begin with -> use lost core collapse)
	if iNumPreviousCities > 2 and 2 * iNumCurrentCities <= iNumPreviousCities:
		utils.debugTextPopup('Collapse by lost cities: ' + pPlayer.getCivilizationShortDescription(0))
		completeCollapse(iPlayer)
		
	sd.setNumPreviousCities(iPlayer, iNumCurrentCities)
	
def checkLostCoreCollapse(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iGameTurn = gc.getGame().getGameTurn()
	
	# must not be dead
	if not pPlayer.isAlive() or pPlayer.getNumCities() == 0:
		return
		
	# only for major civs
	if iPlayer >= con.iNumPlayers:
		return
		
	# immune right after scenario start
	if iGameTurn - utils.getScenarioStartTurn() < utils.getTurns(20):
		return
		
	# immune right after birth
	if iGameTurn - getTurnForYear(con.tBirth[iPlayer]) < utils.getTurns(20):
		return
		
	# immune right after resurrection
	if iGameTurn - pPlayer.getLatestRebellionTurn() < utils.getTurns(10):
		return
		
	iReborn = utils.getReborn(iPlayer)
	lCities = utils.getAreaCitiesCiv(iPlayer, con.tCoreAreasTL[iReborn][iPlayer], con.tCoreAreasBR[iReborn][iPlayer], con.tExceptions[iReborn][iPlayer])
	
	# completely pushed out of core: collapse
	if len(lCities) == 0:
	
		if iPlayer in [con.iPhoenicia, con.iKhmer] and not utils.isReborn(iPlayer):
			pPlayer.setReborn()
			return
	
		utils.debugTextPopup('Collapse from lost core: ' + pPlayer.getCivilizationShortDescription(0))
		completeCollapse(iPlayer)

def checkStability(iPlayer, bPositive = False):
	pPlayer = gc.getPlayer(iPlayer)
	iGameTurn = gc.getGame().getGameTurn()
	iGameEra = gc.getGame().getCurrentEra()
	
	# must not be dead
	if not pPlayer.isAlive():
		return
		
	# I mean it
	if pPlayer.getNumCities() == 0:
		return
	
	# only for major civs
	if iPlayer >= con.iNumPlayers:
		return
		
	# immune to stability checks right after scenario start
	if iGameTurn - utils.getScenarioStartTurn() < utils.getTurns(20):
		return

	# immune to stability checks right after birth
	if iGameTurn - getTurnForYear(con.tBirth[iPlayer]) < utils.getTurns(20):
		return
		
	# immune right after resurrection
	if iGameTurn - pPlayer.getLatestRebellionTurn() < utils.getTurns(10):
		return
		
	# immune to stability checks in golden ages and anarchy
	if pPlayer.isGoldenAge() or pPlayer.isAnarchy():
		return
		
	# immune if there's been a crisis recently
	if getCrisisCountdown(iPlayer) > 0:
		return
		
	iStability, lStabilityTypes, lParameters = calculateStability(iPlayer)
	iStabilityLevel = getStabilityLevel(iPlayer)
	sd.setLastDifference(0)
	
	bFall = (utils.getHumanID() != iPlayer and iGameTurn > getTurnForYear(con.tFall[iPlayer]))
	
	# it's easier to lose stability and harder to gain it at higher levels -> prevent "falling through the levels"
	iThreshold = 5 * (iStabilityLevel - 2) - 5
	
	if bFall:
		iThreshold += 5 * iStabilityLevel + 5 + max(10, (iGameTurn - getTurnForYear(con.tFall[iPlayer])) / utils.getTurns(10))
		
	# make everyone a bit more stable after the Renaissance -> less collapses
	if iGameEra >= con.iRenaissance:
		iThreshold -= 5
		
	iCrisisThreshold = max(-5, iThreshold)
	
	if iStability > iThreshold + 10:
		iStabilityLevel = min(iStabilityLevel + 1, con.iStabilitySolid)
		sd.setLastDifference(1)
		sd.setCrisisImminent(False)
		
	elif iStability >= iCrisisThreshold:
		sd.setCrisisImminent(False)
		
	elif not bPositive:
		if iStability < iThreshold - 10:
			iStabilityLevel = iStabilityLevel - 1#max(iStabilityLevel - 1, con.iStabilityCollapsing)
			sd.setLastDifference(-1)
			
		if iStability < iCrisisThreshold:
			iCrisisType = determineCrisisType(lStabilityTypes)
			iCrisisLevel = iStabilityLevel
			if not bFall: iCrisisLevel += 1
			triggerCrisis(iPlayer, iCrisisLevel, iCrisisType, lStabilityTypes)
			
	setStabilityLevel(iPlayer, max(iStabilityLevel, con.iStabilityCollapsing))
	
	# update stability information
	if utils.getHumanID() == iPlayer:
		for i in range(5):
			sd.setLastStability(iStability)
			sd.setStabilityCategoryValue(i, lStabilityTypes[i])
		
		for i in range(con.iNumStabilityParameters):
			gc.getGame().setStabilityParameter(i, lParameters[i])
	
def triggerCrisis(iPlayer, iStabilityLevel, iCrisisType, lStabilityTypes):

	if iStabilityLevel < 0: iStabilityLevel = 0
	elif iStabilityLevel > 4: iStabilityLevel = 4
	
	# human players: receive a warning before the first crisis
	if utils.getHumanID() == iPlayer and not sd.isCrisisImminent():
		sd.setCrisisImminent(True)
		changeCrisisCountdown(iPlayer, utils.getTurns(5))
		sText = localText.getText("TXT_KEY_STABILITY_CRISIS_IMMINENT_MESSAGE", (localText.getText(tCrisisLevels[iStabilityLevel], ()),))
		CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
		return

	if iStabilityLevel < con.iStabilitySolid:
		sText = localText.getText("TXT_KEY_STABILITY_CRISIS_MESSAGE", (localText.getText(tCrisisLevels[iStabilityLevel], ()), localText.getText(tCrisisTypes[iCrisisType], ())))
		CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
		#utils.debugTextPopup(gc.getPlayer(iPlayer).getCivilizationShortDescription(0) + ' is experiencing a ' + localText.getText(tCrisisLevels[iStabilityLevel], ()) + ' ' + localText.getText(tCrisisTypes[iCrisisType], ()) + ' crisis!' + '\nYear: ' + str(gc.getGame().getGameTurnYear()))
	
	if iStabilityLevel > con.iStabilityShaky:
		changeCrisisCountdown(iPlayer, utils.getTurns(5))
	else:
		changeCrisisCountdown(iPlayer, utils.getTurns(10))
		
	if iStabilityLevel == con.iStabilityCollapsing:
		completeCollapse(iPlayer)
		
	elif iStabilityLevel < con.iStabilitySolid:
		if iCrisisType == con.iStabilityExpansion: territorialCrisis(iPlayer, iStabilityLevel)
		elif iCrisisType == con.iStabilityEconomy: economicCrisis(iPlayer, iStabilityLevel)
		elif iCrisisType == con.iStabilityDomestic: domesticCrisis(iPlayer, iStabilityLevel)
		elif iCrisisType == con.iStabilityForeign: diplomaticCrisis(iPlayer, iStabilityLevel)
		elif iCrisisType == con.iStabilityMilitary: militaryCrisis(iPlayer, iStabilityLevel)
		
def territorialCrisis(iPlayer, iCrisisLevel):

	# minor crisis: lose territorial control
	if iCrisisLevel == con.iStabilityStable:
		#secedeRandomCity(iPlayer)
		loseTerritory(iPlayer)
		
	# moderate crisis: a single city secedes
	elif iCrisisLevel == con.iStabilityShaky:
		#secedeForeignCities(iPlayer)
		secedeSingleCity(iPlayer)
		
	# severe crisis: collapse to core
	elif iCrisisLevel == con.iStabilityUnstable:
		collapseToCore(iPlayer)
		
def economicCrisis(iPlayer, iCrisisLevel):
	pPlayer = gc.getPlayer(iPlayer)
	
	# minor crisis: lose 10% research or gold equivalent
	if iCrisisLevel == con.iStabilityStable:
		loseCommerce(iPlayer, 10)
		
	# moderate crisis: one turn of anarchy, lose 50% research or gold equivalent
	elif iCrisisLevel == con.iStabilityShaky:
		sText = localText.getText("TXT_KEY_STABILITY_ECONOMIC_CRISIS", ())
		CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
	
		pPlayer.changeAnarchyTurns(1)
		loseCommerce(iPlayer, 50)
		
	# severe crisis: three turns of anarchy, lose 100% research or gold equivalent, cottages and GPP decay
	elif iCrisisLevel == con.iStabilityUnstable:
		sText = localText.getText("TXT_KEY_STABILITY_ECONOMIC_CRISIS", ())
		CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
		
		pPlayer.changeAnarchyTurns(3)
		loseCommerce(iPlayer, 100)
		downgradeCottages(iPlayer)
		removeGreatPeoplePoints(iPlayer)
		
def domesticCrisis(iPlayer, iCrisisLevel):
	pPlayer = gc.getPlayer(iPlayer)
	lCities = utils.getCityList(iPlayer)

	# minor crisis: one turn of anarchy, unrest in unhappy cities
	if iCrisisLevel == con.iStabilityStable:
		sText = localText.getText("TXT_KEY_STABILITY_DOMESTIC_CRISIS", ())
		CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
		
		pPlayer.changeAnarchyTurns(1)
		for city in lCities:
			if city.happyLevel() < city.unhappyLevel(0): city.setOccupationTimer(2)
			
	# moderate crisis: two turns of anarchy, more unrest in unhappy cities
	elif iCrisisLevel == con.iStabilityShaky:
		sText = localText.getText("TXT_KEY_STABILITY_DOMESTIC_CRISIS", ())
		CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
		
		pPlayer.changeAnarchyTurns(2)
		for city in lCities:
			if city.happyLevel() < city.unhappyLevel(0): city.setOccupationTimer(4)
			
	# severe crisis: three turns of anarchy, unhappy cities secede
	elif iCrisisLevel == con.iStabilityUnstable:
		sText = localText.getText("TXT_KEY_STABILITY_DOMESTIC_CRISIS", ())
		CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
		
		pPlayer.changeAnarchyTurns(3)
		secedeUnhappyCities(iPlayer)
		
def diplomaticCrisis(iPlayer, iCrisisLevel):
	tPlayer = gc.getTeam(iPlayer)
	lTradingCivs = []
	lDefensivePactCivs = []
	lPeaceVassalCivs = []
	lCapitulatedCivs = []
	
	for iLoopPlayer in range(con.iNumPlayers):
		tLoopPlayer = gc.getTeam(iLoopPlayer)
		if tLoopPlayer.isOpenBorders(iPlayer):
			lTradingCivs.append(iLoopPlayer)
		if tLoopPlayer.isDefensivePact(iPlayer):
			lDefensivePactCivs.append(iLoopPlayer)
		if tLoopPlayer.isVassal(iPlayer):
			if tLoopPlayer.isCapitulated():
				lCapitulatedCivs.append(iLoopPlayer)
			else:
				lPeaceVassalCivs.append(iLoopPlayer)

	# minor crisis: two open border agreements canceled
	if iCrisisLevel == con.iStabilityStable:
		cancelTrades(iPlayer, lTradingCivs, 2)
	
	# moderate crisis: five open border agreements canceled, defensive pacts canceled, peace vassals freed
	elif iCrisisLevel == con.iStabilityShaky:
		cancelTrades(iPlayer, lTradingCivs, 5)
		cancelDefensivePacts(iPlayer, lDefensivePactCivs)
		cancelVassals(iPlayer, lPeaceVassalCivs, False)
		
	# severe crisis: all open border agreements canceled, defensive pacts canceled, vassals freed
	elif iCrisisLevel == con.iStabilityUnstable:
		cancelTrades(iPlayer, lTradingCivs, len(lTradingCivs))
		cancelDefensivePacts(iPlayer, lDefensivePactCivs)
		cancelVassals(iPlayer, lPeaceVassalCivs, False)
		cancelVassals(iPlayer, lCapitulatedCivs, True)
		
def militaryCrisis(iPlayer, iCrisisLevel):

	# minor crisis: loss of city defenses
	if iCrisisLevel == con.iStabilityStable:
		removeCityDefenses(iPlayer)
	
	# moderate crisis: 25% chance of military unit desertion, loss of city defenses
	elif iCrisisLevel == con.iStabilityShaky:
		removeCityDefenses(iPlayer)
		unitDesertion(iPlayer, 4)
	
	# severe crisis: 50% chance of military unit desertion, loss of city defenses, secession of enemy target cities
	elif iCrisisLevel == con.iStabilityUnstable:
		removeCityDefenses(iPlayer)
		unitDesertion(iPlayer, 2)
		secedeEnemyTargetCities(iPlayer)
		
def getPossibleMinors(iPlayer):

	if utils.getCivsWithNationalism() == 0 and iPlayer in [con.iMaya, con.iAztecs, con.iInca, con.iMali, con.iEthiopia, con.iCongo]:
		return [con.iNative, con.iBarbarian, con.iIndependent]
		
	if gc.getGame().getCurrentEra() <= con.iMedieval:
		return [con.iBarbarian, con.iIndependent, con.iIndependent2]
		
	return [con.iIndependent, con.iIndependent2]
	
def secedeCities(iPlayer, lCities):
	lPossibleMinors = getPossibleMinors(iPlayer)
	dPossibleResurrections = {}
	
	utils.clearPlague(iPlayer)
	
	for city in lCities:
	
		tCityPlot = (city.getX(), city.getY())
		cityPlot = gc.getMap().plot(city.getX(), city.getY())
		iGameTurnYear = gc.getGame().getGameTurnYear()
	
		# three possible behaviors: if living civ has a claim, assign it to them
		# claim based on core territory
		iClaim = -1
		for iLoopPlayer in range(con.iNumPlayers):
			if iLoopPlayer == iPlayer: continue
			if utils.getHumanID() == iLoopPlayer: continue
			if iGameTurnYear < con.tBirth[iLoopPlayer]: continue
			if iGameTurnYear > con.tFall[iLoopPlayer]: continue
			if cityPlot.isCore(iLoopPlayer) and gc.getPlayer(iLoopPlayer).isAlive():
				iClaim = iLoopPlayer
				utils.debugTextPopup('Secede ' + gc.getPlayer(iPlayer).getCivilizationAdjective(0) + ' ' + city.getName() + ' to ' + gc.getPlayer(iClaim).getCivilizationShortDescription(0) + '.\nReason: core territory.')
				break
		
		# claim based on original owner
		if iClaim == -1:
			iOriginalOwner = city.getOriginalOwner()
			if cityPlot.getSettlerMapValue(iOriginalOwner) >= 90 and gc.getPlayer(iOriginalOwner).isAlive() and iOriginalOwner != iPlayer and utils.getHumanID() != iOriginalOwner:
				if iOriginalOwner < con.iNumPlayers and iGameTurnYear < con.tFall[iOriginalOwner]:
					# cities lost too long ago doesn't return
					if city.getGameTurnPlayerLost(iOriginalOwner) >= gc.getGame().getGameTurn() - utils.getTurns(50):
						iClaim = iOriginalOwner
						utils.debugTextPopup('Secede ' + gc.getPlayer(iPlayer).getCivilizationAdjective(0) + ' ' + city.getName() + ' to ' + gc.getPlayer(iClaim).getCivilizationShortDescription(0) + '.\nReason: original owner.')
				
		# claim based on culture
		if iClaim == -1:
			for iLoopPlayer in range(con.iNumPlayers):
				if iLoopPlayer == iPlayer: continue
				if utils.getHumanID() == iLoopPlayer: continue
				if iGameTurnYear < con.tBirth[iLoopPlayer]: continue
				if iGameTurnYear > con.tFall[iLoopPlayer]: continue
				if gc.getPlayer(iLoopPlayer).isAlive():
					iCulturePercent = 100 * cityPlot.getCulture(iLoopPlayer) / cityPlot.countTotalCulture()
					if iCulturePercent >= 75:
						iClaim = iLoopPlayer
						utils.debugTextPopup('Secede ' + gc.getPlayer(iPlayer).getCivilizationAdjective(0) + ' ' + city.getName() + ' to ' + gc.getPlayer(iClaim).getCivilizationShortDescription(0) + '.\nReason: culture.')
						break
						
		# claim based on war target (needs to be winning the war based on war success)
		if iClaim == -1:
			tPlayer = gc.getTeam(iPlayer)
			for iLoopPlayer in range(con.iNumPlayers):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.isAlive() and tPlayer.isAtWar(iLoopPlayer) and utils.getHumanID() != iLoopPlayer and iGameTurnYear < con.tFall[iLoopPlayer]:
					if pLoopPlayer.getWarMapValue(city.getX(), city.getY()) >= 8 and gc.getTeam(iLoopPlayer).AI_getWarSuccess(iPlayer) > tPlayer.AI_getWarSuccess(iLoopPlayer):
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
		for iLoopPlayer in range(con.iNumPlayers):
			if iLoopPlayer == iPlayer: continue
			if gc.getPlayer(iLoopPlayer).isAlive(): continue
			if gc.getGame().getGameTurn() - getLastTurnAlive(iLoopPlayer) < utils.getTurns(20): continue
		
			tRespawnTL, tRespawnBR, tRespawnExceptions = utils.getRespawnArea(iLoopPlayer)
			if utils.isPlotInArea(tCityPlot, tRespawnTL, tRespawnBR, tRespawnExceptions):
				bPossible = False
				
				for tInterval in con.tResurrectionIntervals[iLoopPlayer]:
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
	sName = city.getName()
	utils.completeCityFlip(city.getX(), city.getY(), iNewOwner, city.getOwner(), 50, False, True, True)
	
	if city.getOwner() == utils.getHumanID():
		if iNewOwner in [con.iIndependent, con.iIndependent2, con.iNative, con.iBarbarian]:
			sText = localText.getText("TXT_KEY_STABILITY_CITY_INDEPENDENCE", (sName,))
			CyInterface().addMessage(city.getOwner(), False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
		else:
			sText = localText.getText("TXT_KEY_STABILITY_CITY_CHANGED_OWNER", (sName, gc.getPlayer(iNewOwner).getCivilizationAdjective(0)))
			utils.debugTextPopup(sText)
			CyInterface().addMessage(city.getOwner(), False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
		
	if utils.getHumanID() == iNewOwner:
		sText = localText.getText("TXT_KEY_STABILITY_CITY_CHANGED_OWNER_US", (sName,))
		CyInterface().addMessage(iNewOwner, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
	
def completeCollapse(iPlayer):
	lCities = utils.getCityList(iPlayer)
	
	# secede all cities
	secedeCities(iPlayer, lCities)
		
	# take care of the remnants of the civ
	utils.killUnitsInArea((0, 0), (127, 63), iPlayer)
	utils.resetUHV(iPlayer)
	utils.setLastTurnAlive(iPlayer, gc.getGame().getGameTurn())
	
	if iPlayer < con.iNumPlayers:
		utils.clearEmbassies(iPlayer)
		
	# special case: Byzantine collapse: remove Christians in the Turkish core
	if iPlayer == con.iByzantium:
		utils.removeReligionByArea(con.tCoreAreasTL[0][con.iTurkey], con.tCoreAreasBR[0][con.iTurkey], con.iChristianity)
		
	utils.debugTextPopup('Complete collapse: ' + gc.getPlayer(iPlayer).getCivilizationShortDescription(0))
	
	sText = localText.getText("TXT_KEY_STABILITY_COMPLETE_COLLAPSE", (gc.getPlayer(iPlayer).getCivilizationAdjective(0),))
	CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, sText, "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
		
def collapseToCore(iPlayer):
	lAhistoricalCities = []
	lNonCoreCities = []
	
	for city in utils.getCityList(iPlayer):
		plot = gc.getMap().plot(city.getX(), city.getY())
		if not plot.isCore(iPlayer):
			lNonCoreCities.append(city)
			if plot.getSettlerMapValue(iPlayer) < 90:
				lAhistoricalCities.append(city)
			
	# start by seceding ahistorical cities
	if len(lAhistoricalCities) > 2:
			
		# notify owner
		if utils.getHumanID() == iPlayer:
			sText = localText.getText("TXT_KEY_STABILITY_FOREIGN_SECESSION", ())
			CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
				
		# secede all foreign cities
		secedeCities(iPlayer, lAhistoricalCities)
		
	# if almost all cities are historical, secede non core cities
	elif lNonCoreCities:
			
		# notify owner
		if utils.getHumanID() == iPlayer:
			sText = localText.getText("TXT_KEY_STABILITY_COLLAPSE_TO_CORE", ())
			CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
			
		# secede all non-core cities
		secedeCities(iPlayer, lNonCoreCities)
	
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
		secedeCities(iPlayer, [utils.getHighestEntry(lCities, lambda x: -gc.getMap().plot(x.getX(), x.getY()).getSettlerMapValue(iPlayer))])
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
				for iLoopPlayer in range(con.iNumTotalPlayersB):
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
		CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)

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
		CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
			
	# secede all unhappy cities
	secedeCities(iPlayer, lCities)
	
	# five turns of unrest in all remaining cities
	for city in lRemainingCities:
		city.setOccupationTimer(5)
		
def secedeEnemyTargetCities(iPlayer):
	tPlayer = gc.getTeam(iPlayer)
	lEnemies = []
	
	for iLoopPlayer in range(con.iNumPlayers):
		if tPlayer.isAtWar(iLoopPlayer):
			lEnemies.append(iLoopPlayer)
	
	for city in utils.getCityList(iPlayer):
		for iEnemy in lEnemies:
			lEnemyCities = []
			if gc.getPlayer(iEnemy).getWarMapValue(city.getX(), city.getY()) >= 8:
				lEnemyCities.append(city)
			if lEnemyCities:
				secedeCity(utils.getRandomEntry(lEnemyCities), iEnemy)
	
def getResearchProgress(iPlayer):
	tPlayer = gc.getTeam(iPlayer)
	iCost = 0
	
	for iTech in range(con.iNumTechs):
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
		
		for iTech in range(con.iNumTechs):
			if iTechReduction <= 0: break
			
			iTechProgress = tPlayer.getResearchProgress(iTech)
			tPlayer.setResearchProgress(iTech, max(0, iTechProgress - iTechReduction), iPlayer)
			
			iTechReduction = max(0, iTechReduction - iTechProgress)
			
	pPlayer.setGold(iGold)
	
	if utils.getHumanID() == iPlayer:
		sText = localText.getText("TXT_KEY_STABILITY_LOST_COMMERCE", (iLostGold, iLostBeakers))
		CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
	
def downgradeCottages(iPlayer):
	for x in range(128):
		for y in range(64):
			plot = gc.getMap().plot(x, y)
			if plot.getOwner() == iPlayer:
				iImprovement = plot.getImprovementType()
				
				if iImprovement == con.iTown: plot.setImprovementType(con.iHamlet)
				elif iImprovement == con.iVillage: plot.setImprovementType(con.iCottage)
				elif iImprovement == con.iHamlet: plot.setImprovementType(con.iCottage)
				elif iImprovement == con.iCottage: plot.setImprovementType(-1)
				
	if utils.getHumanID() == iPlayer:
		sText = localText.getText("TXT_KEY_STABILITY_DOWNGRADE_COTTAGES", ())
		CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
				
def removeGreatPeoplePoints(iPlayer):
	for city in utils.getCityList(iPlayer):
		city.changeGreatPeopleProgress(-city.getGreatPeopleProgress())
		
	if utils.getHumanID() == iPlayer:
		sText = localText.getText("TXT_KEY_STABILITY_REMOVE_GPP", ())
		CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
		
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
				CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
				
			if utils.getHumanID() == iOtherPlayer:
				sText = localText.getText("TXT_KEY_STABILITY_CANCEL_TRADE", (gc.getPlayer(iPlayer).getCivilizationShortDescription(0),))
				CyInterface().addMessage(iOtherPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
			
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
			utils.debugTextPopup('No appropriate deals found.')
			continue
			
		pOtherPlayer.AI_changeMemoryCount(iPlayer, MemoryTypes.MEMORY_STOPPED_TRADING_RECENT, utils.getTurns(10))
		pOtherPlayer.AI_changeAttitudeExtra(iPlayer, -2)
			
		if utils.getHumanID() == iPlayer:
			sText = localText.getText("TXT_KEY_STABILITY_CANCEL_DEFENSIVE_PACT", (gc.getPlayer(iOtherPlayer).getCivilizationShortDescription(0),))
			CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
			
		if utils.getHumanID() == iOtherPlayer:
			sText = localText.getText("TXT_KEY_STABILITY_CANCEL_DEFENSIVE_PACT", (gc.getPlayer(iPlayer).getCivilizationShortDescription(0),))
			CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
	
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
			utils.debugTextPopup('No appropriate deals found.')
			continue
		
		pOtherPlayer.AI_changeMemoryCount(iPlayer, MemoryTypes.MEMORY_STOPPED_TRADING_RECENT, utils.getTurns(10))
		pOtherPlayer.AI_changeAttitudeExtra(iPlayer, -2)
			
		if utils.getHumanID() == iPlayer:
			if bCapitulated:
				sText = localText.getText("TXT_KEY_STABILITY_CANCEL_CAPITULATION", (gc.getPlayer(iOtherPlayer).getCivilizationShortDescription(0),))
			else:
				sText = localText.getText("TXT_KEY_STABILITY_CANCEL_PEACE_VASSAL", (gc.getPlayer(iOtherPlayer).getCivilizationShortDescription(0),))
			CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
		
def removeCityDefenses(iPlayer):
	for city in utils.getCityList(iPlayer):
		city.changeDefenseDamage(100)
		
	if utils.getHumanID() == iPlayer:
		sText = localText.getText("TXT_KEY_STABILITY_REMOVE_DEFENSES", ())
		CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
		
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
					lPlotUnits = []
			for i in range(len(lPlotUnits)):
				if i % iDivisor == 0:
					lDesertingUnits.append(lPlotUnits[i])		
			
	for unit in lDesertingUnits:
		x = unit.getX()
		y = unit.getY()
		plot = gc.getMap().plot(x, y)
		
		unit.kill(False, con.iBarbarian)#iPlayer)
		
	if utils.getHumanID() == iPlayer:
		sText = localText.getText("TXT_KEY_STABILITY_UNIT_DESERTION", (len(lDesertingUnits),))
		CyInterface().addMessage(iPlayer, False, con.iDuration, sText, "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
	
def calculateStability(iPlayer):
	iGameTurn = gc.getGame().getGameTurn()
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(pPlayer.getTeam())

	iExpansionStability = 0
	iEconomyStability = 0
	iDomesticStability = 0
	iForeignStability = 0
	iMilitaryStability = 0
	
	lParameters = [0 for i in range(con.iNumStabilityParameters)]
	
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
	iPeripheryPopulation = 0
	iTotalCoreCities = 0
	iOccupiedCoreCities = 0
	
	iStateReligionCities = 0
	iOnlyStateReligionCities = 0
	iNonStateReligionCities = 0
	
	iHappyCities = 0
	iUnhappyCities = 0
		
	bTotalitarianism = (iCivicOrganization == con.iCivicTotalitarianism)
	bCityStates = (iCivicGovernment == con.iCivicCityStates)
	bMercantilism = (iCivicEconomy == con.iCivicMercantilism)
	bVassalage = (iCivicOrganization == con.iCivicVassalage)
	bWarriorCode = (iCivicMilitary == con.iCivicWarriorCode)
	bEnvironmentalism = (iCivicEconomy == con.iCivicEnvironmentalism)
	bFanaticism = (iCivicGovernment == con.iCivicFanaticism)
	bAutocracy = (iCivicGovernment == con.iCivicAutocracy)
	
	for city in utils.getCityList(iPlayer):
		iPopulation = city.getPopulation()
		iModifier = 0
		x = city.getX()
		y = city.getY()
		plot = gc.getMap().plot(x,y)
		
		bHistorical = (plot.getSettlerMapValue(iPlayer) >= 90)
		
		bForeignCore = False
		for iLoopPlayer in range(con.iNumPlayers):
			if iLoopPlayer != iPlayer and iGameTurn > getTurnForYear(con.tBirth[iLoopPlayer]) and plot.isCore(iLoopPlayer):
				bForeignCore = True
				break
				
		#bExpansionExceptions = ((bHistorical and iPlayer in [con.iMongolia]) or bTotalitarianism)
		bExpansionExceptions = bTotalitarianism
		
		# Expansion
		if plot.isCore(iPlayer):
			iCorePopulation += (2 + iCurrentEra) * iPopulation
		else:
			# ahistorical tiles
			if not bHistorical: iModifier += 2
			
			# colonies with Totalitarianism
			if isOverseas(city) and bHistorical and bTotalitarianism: iModifier += 1
			
			# not original owner
			if city.getOriginalOwner() != iPlayer and not bExpansionExceptions and not bWarriorCode: iModifier += 1
			
			# not majority culture
			if plot.getCulture(iPlayer) * 2 < plot.countTotalCulture() and not bExpansionExceptions: iModifier += 1
			
			# foreign core (includes Persian UP)
			if bForeignCore and iPlayer != con.iPersia: iModifier += 1
			
			# City States
			if bCityStates: iModifier += 2
			
			# Courthouse
			if city.hasBuilding(utils.getUniqueBuilding(iPlayer, con.iCourthouse)): iModifier -= 1
			
			# Jail
			if city.hasBuilding(utils.getUniqueBuilding(iPlayer, con.iJail)): iModifier -= 1
			
			# cap
			if iModifier < 1: iModifier = 1
			
			# Portuguese UP: reduced instability from overseas colonies
			if isOverseas(city):
				if iPlayer == con.iPortugal: iModifier -= 1
				elif bMercantilism and iModifier > 1: iModifier -= 1
			
			iPeripheryPopulation += iModifier * iPopulation
			
		# Religions
		bNonStateReligion = False
		for iReligion in range(con.iNumReligions):
			if iReligion != iStateReligion and city.isHasReligion(iReligion):
				if not isTolerated(iPlayer, iReligion):
					bNonStateReligion = True
					break
				
		if city.isHasReligion(iStateReligion):
			iStateReligionCities += 1
			if not bNonStateReligion: iOnlyStateReligionCities += 1
			
		if iPlayer == con.iPoland:
			if iStateReligion in [con.iCatholicism, con.iOrthodoxy, con.iProtestantism]:
				for iReligion in [con.iCatholicism, con.iOrthodoxy, con.iProtestantism]:
					if iReligion != iStateReligion and city.isHasReligion(iReligion) and not city.isHasReligion(iStateReligion):
						iStateReligionCities += 1
						if not bNonStateReligion: iOnlyStateReligionCities += 1
				
		if bNonStateReligion: iNonStateReligionCities += 1
		
		# Happiness
		iHappiness = city.happyLevel()
		iUnhappiness = city.unhappyLevel(0)
		iOvercrowding = city.getOvercrowdingPercentAnger(0) * city.getPopulation() / 1000
		
		if city.isWeLoveTheKingDay() or (iPopulation >= pPlayer.getAveragePopulation() and iHappiness - iUnhappiness >= iPopulation / 4):
			iHappyCities += 1
		elif iUnhappiness - iOvercrowding > iPopulation / 5 or iUnhappiness - iHappiness > 0:
			iUnhappyCities += 1
			
	#for city in utils.getAreaCities(con.tCoreAreasTL[iReborn][iPlayer], con.tCoreAreasBR[iReborn][iPlayer], con.tExceptions[iReborn][iPlayer]):
	#	iTotalCoreCities += 1
	#	if city.getOwner() != iPlayer:
	#		iOccupiedCoreCities += 1
			
	iCurrentCommerce = pPlayer.calculateTotalCommerce()
	iPreviousCommerce = pPlayer.getEconomyHistory(iGameTurn - utils.getTurns(10))
	
	iCurrentCommerceNeighbors = iPreviousCommerce * 11 / 10
	iPreviousCommerceNeighbors = iPreviousCommerce
		
	for iLoopPlayer in range(con.iNumPlayers):
		if pPlayer.canContact(iLoopPlayer):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			iCurrentCommerceNeighbors += pLoopPlayer.calculateTotalCommerce()
			iPreviousCommerceNeighbors += pLoopPlayer.getEconomyHistory(iGameTurn - utils.getTurns(10))
			
	iCurrentCommerceRank = calculateCommerceRank(iPlayer, iGameTurn)
	iPreviousCommerceRank = calculateCommerceRank(iPlayer, iGameTurn - utils.getTurns(10))
	
	iCurrentPower = pPlayer.getPower()#pPlayer.getPowerHistory(iGameTurn)
	iPreviousPower = pPlayer.getPowerHistory(iGameTurn - utils.getTurns(10))
	
	#iCurrentPowerRank = calculatePowerRank(iPlayer, iGameTurn)
	#iPreviousPowerRank = calculatePowerRank(iPlayer, iGameTurn - 10)
	
	# EXPANSION
	iExpansionStability = 0
	
	iCorePeripheryStability = 0
	iRazeCityStability = 0
	iOwnCoreStability = 0
	
	# help Tibet
	#if iPlayer == con.iTibet and iGameTurn <= getTurnForYear(1000):
	#	iPeripheryPopulation /= 2
	
	# Core vs. Periphery Populations
	iCombinedPopulation = iCorePopulation + iPeripheryPopulation
	
	#if iCombinedPopulation == 0:
	#	iCorePercentage = 0
	#else:
	#	iCorePercentage = 100 * iCorePopulation / iCombinedPopulation - 50
		
	if iCorePopulation == 0:
		iPeripheryExcess = 200
	else:
		iPeripheryExcess = 100 * iPeripheryPopulation / iCorePopulation - 100
	
	if iPeripheryExcess > 100: iPeripheryExcess = 100
		
	if iPeripheryExcess > 0:
		iCorePeripheryStability -= int(25 * sigmoid(1.0 * iPeripheryExcess / 100))
		
		utils.debugTextPopup('Expansion rating: ' + pPlayer.getCivilizationShortDescription(0) + '\nCore population: ' + str(iCorePopulation) + '\nPeriphery population: ' + str(iPeripheryPopulation) + '\nExpansion stability: ' + str(iCorePeripheryStability))
		
	#if iCorePeripheryStability > 0:
	#	sExpansionString += localText.getText('TXT_KEY_STABILITY_CORE_PERIPHERY_POSITIVE', (iCorePeripheryStability,))
	#elif iCorePeripheryStability < 0:
	#	sExpansionString += localText.getText('TXT_KEY_STABILITY_CORE_PERIPHERY_NEGATIVE', (iCorePeripheryStability,))
	
	lParameters[con.iParameterCorePeriphery] = iCorePeripheryStability
		
	iExpansionStability += iCorePeripheryStability
	
	# apply raze city penalty
	iRazeCityStability = sd.getHumanRazePenalty()
	
	lParameters[con.iParameterRazedCities] = iRazeCityStability
		
	iExpansionStability += iRazeCityStability
	
	# Control over own core - even necessary? already weighs in above - disable for now and see how it goes
	#iExpansionStability -= 20 * iOccupiedCoreCities / iTotalCoreCities
	
	# ECONOMY
	iEconomyStability = 0
	
	iEconomicGrowthStability = 0
	
	# Economic growth
	if iPreviousCommerce != 0:
		#iCommerceDifference = iCurrentCommerce - iPreviousCommerce
		#iPercentChange = 100 * iCommerceDifference / iPreviousCommerce
		
		#iNeighborCommerceDifference = iCurrentCommerceNeighbors - iPreviousCommerceNeighbors
		#iBaselinePercentChange = 100 * iNeighborCommerceDifference / iPreviousCommerceNeighbors
		
		iPercentChange = calculateEconomicGrowth(iPlayer, 10)
		iBaselinePercentChange = 20 #calculateEconomicGrowthNeighbors(iPlayer, 10)
		
		iDifference = iPercentChange - iBaselinePercentChange
		
		if iDifference > 20:
			iEconomicGrowthStability = 10 + (iDifference - 20) / 5
		elif iDifference < -20:
			iEconomicGrowthStability = -10 + (iDifference + 20) / 5
		else:
			iEconomicGrowthStability = iDifference / 2
		
		if iEconomicGrowthStability > 20: iEconomicGrowthStability = 20
		elif iEconomicGrowthStability < -20: iEconomicGrowthStability = -20
		
		#utils.debugTextPopup(pPlayer.getCivilizationAdjective(0) + " Economic Stability\nGrowth: " + str(iPercentChange) + "\nBaseline Percent: " + str(iBaselinePercentChange) + "\nStability: " + str(iEconomicGrowthStability))
		
		# Environmentalism
		if bEnvironmentalism and iPercentChange >= 0 and iEconomicGrowthStability < 0:
			iEconomicGrowthStability = 0
		
		#if iPercentChange > iBaselinePercentChange:
		#	sEconomyString += localText.getText('TXT_KEY_STABILITY_ECONOMIC_GROWTH', (iEconomicGrowthStability,))
		#elif iPercentChange >= 0 and iPercentChange != iBaselinePercentChange:
		#	sEconomyString += localText.getText('TXT_KEY_STABILITY_ECONOMIC_STAGNATION', (iEconomicGrowthStability,))
		#else:
		#	sEconomyString += localText.getText('TXT_KEY_STABILITY_ECONOMIC_DECLINE', (iEconomicGrowthStability,))
		
		lParameters[con.iParameterEconomicGrowth] = iEconomicGrowthStability
		lParameters[con.iParameterPercentChange] = iPercentChange
		lParameters[con.iParameterBaselinePercent] = iBaselinePercentChange
	
	iEconomyStability += iEconomicGrowthStability
	
	# Relative wealth
	#iRankDifference = iCurrentCommerceRank - iPreviousCommerceRank
	
	#if iRankDifference > 0:
	#	sEconomyString += localText.getText('TXT_KEY_STABILITY_RELATIVE_WEALTH_GAIN', (iRankDifference,))
	#elif iRankDifference < 0:
	#	sEconomyString += localText.getText('TXT_KEY_STABILITY_RELATIVE_WEALTH_LOSS', (iRankDifference,))
		
	#iEconomyStability += iRankDifference
	
	# Economic systems
	iEconomicSystemStability = 0
	bMercantilism = (iCivicEconomy == con.iCivicMercantilism)
	bCentralPlanning = (iCivicEconomy == con.iCivicCentralPlanning)
	if bMercantilism or bCentralPlanning:
		for iLoopPlayer in range(con.iNumPlayers):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if tPlayer.isOpenBorders(iLoopPlayer):
				if bMercantilism:
					if pLoopPlayer.getEconomyHistory(iGameTurn) > iCurrentCommerce:
						iEconomicSystemStability -= 3
				if bCentralPlanning:
					if pLoopPlayer.getCivics(3) == con.iCivicFreeMarket:
						iEconomicSystemStability -= 3
						
	#if iEconomicSystemStability != 0:
	#	if bMercantilism:
	#		sEconomyString += localText.getText('TXT_KEY_STABILITY_MERCANTILISM_TRADE_RICHER', (iEconomicSystemPenalty,))
	#	if bCentralPlanning:
	#		sEconomyString += localText.getText('TXT_KEY_STABILITY_CENTRAL_PLANNING_TRADE_FREE_MARKET', (iEconomicSystemPenalty,))
	
	if bMercantilism: lParameters[con.iParameterMercantilism] = iEconomicSystemStability
	if bCentralPlanning: lParameters[con.iParameterCentralPlanning] = iEconomicSystemStability
						
	iEconomyStability += iEconomicSystemStability
					
	# DOMESTIC
	iDomesticStability = 0
	
	# Happiness
	iHappinessStability = 0
	
	if iNumTotalCities > 0:
		iHappinessStability += min(iNumTotalCities, 5 * iHappyCities / iNumTotalCities)
		iHappinessStability -= min(iNumTotalCities, 10 * iUnhappyCities / iNumTotalCities)
	
	#utils.debugTextPopup(pPlayer.getCivilizationShortDescription(0) + ' happiness stability: ' + str(iHappinessStability) + '\nHappy cities: ' + str(iHappyCities) + '\nUnhappy cities: ' + str(iUnhappyCities) + '\nTotal cities: ' + str(iNumTotalCities))
	
	#if iNumTotalCities > 0: 
	#	iHappinessStability += (iHappiness - iUnhappiness) / iNumTotalCities
	#iHappinessStability -= 2 * iUnhappyCities
	
	#if iHappinessStability > 0:
	#	sDomesticString += localText.getText('TXT_KEY_STABILITY_HAPPINESS', (iHappinessStability,))
	#elif iHappinessStability < 0:
	#	sDomesticString += localText.getText('TXT_KEY_STABILITY_UNHAPPINESS', (iHappinessStability,))
	
	lParameters[con.iParameterHappiness] = iHappinessStability
	
	iDomesticStability += iHappinessStability
	
	# Civics (combinations)
	iCivicStability = 0
	
	if iCivicOrganization == con.iCivicTotalitarianism:
		if iCivicGovernment == con.iCivicAutocracy: iCivicStability += 5
		if iCivicEconomy == con.iCivicCentralPlanning: CivicStability += 3
		if iCivicReligion != con.iCivicSecularism: iCivicStability -= 5
	
	if iCivicEconomy == con.iCivicCentralPlanning:
		if iCivicLabor == con.iCivicIndustrialism: iCivicStability += 2
		elif iCivicLabor != con.iCivicPublicWelfare: iCivicStability -= 5
		
	if iCivicOrganization == con.iCivicEgalitarianism:
		if iCivicGovernment == con.iCivicRepublic: iCivicStability += 1
		if iCivicLabor != con.iCivicPublicWelfare: iCivicStability -= 5
		if iCivicEconomy == con.iCivicEnvironmentalism: iCivicStability += 2
		if iCivicReligion == con.iCivicSecularism: iCivicStability += 2
		
	if iCivicLabor == con.iCivicCapitalism:	
		if iCivicEconomy == con.iCivicFreeMarket: iCivicStability += 3
		if iCivicEconomy == con.iCivicGuilds: iCivicStability -= 5
		
	if iCivicEconomy == con.iCivicEnvironmentalism:
		if iCivicLabor == con.iCivicIndustrialism: iCivicStability -= 5
		
	if iCivicGovernment == con.iCivicTheocracy:
		if iCivicReligion == con.iCivicFanaticism: iCivicStability += 3
		if iCivicReligion == con.iCivicSecularism: iCivicStability -= 7
		if iCivicOrganization == con.iCivicEgalitarianism: iCivicStability -= 3
		
	if iCivicOrganization == con.iCivicVassalage:
		if iCivicMilitary in [con.iCivicWarriorCode, con.iCivicLevyArmies]: iCivicStability += 3
		else: iCivicStability -= 5
		if iCivicEconomy in [con.iCivicCapitalism, con.iCivicIndustrialism, con.iCivicPublicWelfare]: iCivicStability -= 5
	
		if iCurrentEra == con.iMedieval:
			if iCivicGovernment == con.iCivicDynasticism: iCivicStability += 2
			if iCivicLabor == con.iCivicAgrarianism: iCivicStability += 3
			
	if iCivicGovernment == con.iCivicCityStates:
		if iCivicOrganization in [con.iCivicVassalage, con.iCivicAbsolutism, con.iCivicEgalitarianism]: iCivicStability -= 3
		if iCivicEconomy == con.iCivicGuilds: iCivicStability += 2
		elif iCivicEconomy != con.iCivicMercantilism: iCivicStability -= 5
		if iCivicMilitary in [con.iCivicMilitia, con.iCivicMercenaries]: iCivicStability += 2
		else: iCivicStability -= 3
		
	if iCivicOrganization == con.iCivicAbsolutism:
		if iCivicGovernment == con.iCivicRepublic: iCivicStability -= 5
		if iCivicEconomy == con.iCivicMercantilism: iCivicStability += 3
		
	iCivicCombinationStability = iCivicStability
	
	#if iCivicCombinationStability > 0:
	#	sDomesticString += localText.getText('TXT_KEY_STABILITY_CIVIC_COMBINATIONS_POSITIVE', (iCivicCombinationStability,))
	#elif iCivicCombinationStability < 0:
	#	sDomesticString += localText.getText('TXT_KEY_STABILITY_CIVIC_COMBINATIONS_NEGATIVE', (iCivicCombinationStability,))
	
	lParameters[con.iParameterCivicCombinations] = iCivicCombinationStability
	
	iCivicStability = 0
	
	# Civics (eras and techs)
	if iCivicOrganization == con.iCivicVassalage:
		if iCurrentEra == con.iMedieval: iCivicStability += 2
		else: iCivicStability -= 5
		
	if iCivicGovernment == con.iCivicTheocracy:
		if iCurrentEra >= con.iIndustrial: iCivicStability -= 5
		
	if iCivicReligion == con.iCivicPantheon:
		if iCurrentEra <= con.iClassical: iCivicStability += 2
		else: iCivicStability -= 2 * iCurrentEra
		
	if iCivicGovernment == con.iCivicCityStates:
		if iCurrentEra <= con.iClassical: iCivicStability += 2
		elif iCurrentEra >= con.iIndustrial: iCivicStability -= 5
		
	if tPlayer.isHasTech(con.iDemocracy):
		if iCivicOrganization not in [con.iCivicRepresentation, con.iCivicEgalitarianism, con.iCivicTotalitarianism]: iCivicStability -= 5
		if iCivicLabor in [con.iCivicSlavery, con.iCivicAgrarianism] and iCivicOrganization != con.iCivicTotalitarianism: iCivicStability -= 5
		
	if tPlayer.isHasTech(con.iUtopia):
		if iCivicOrganization not in [con.iCivicEgalitarianism, con.iCivicTotalitarianism]: iCivicStability -= 5
		
	if tPlayer.isHasTech(con.iEconomics):
		if iCivicEconomy in [con.iCivicSelfSufficiency, con.iCivicGuilds]: iCivicStability -= 5
		if iCivicLabor == con.iCivicSlavery and iCivicOrganization != con.iCivicTotalitarianism: iCivicStability -= 5
		
	if tPlayer.isHasTech(con.iNationalism):
		if iCivicMilitary == con.iCivicMercenaries: iCivicStability -= 7
		
	if tPlayer.isHasTech(con.iMilitaryScience):
		if iCivicMilitary == con.iCivicWarriorCode: iCivicStability -= 10
	
	iCivicEraTechStability = iCivicStability
	
	#if iCivicEraTechStability > 0:
	#	sDomesticString += localText.getText('TXT_KEY_STABILITY_CIVIC_ERA_TECH_POSITIVE', (iCivicEraTechStability,))
	#elif iCivicEraTechStability < 0:
	#	sDomesticString += localText.getText('TXT_KEY_STABILITY_CIVIC_ERA_TECH_NEGATIVE', (iCivicEraTechStability,))
	
	lParameters[con.iParameterCivicsEraTech] = iCivicEraTechStability
	
	iDomesticStability += iCivicCombinationStability + iCivicEraTechStability
	
	# Religion
	iReligionStability = 0
	
	if iNumTotalCities > 0:
		iHeathenRatio = 100 * iNonStateReligionCities / iNumTotalCities
		iHeathenThreshold = 30
		if iCivicReligion == con.iCivicFanaticism: iHeathenThreshold = 0
		
		if iHeathenRatio > iHeathenThreshold:
			iReligionStability -= (iHeathenRatio - iHeathenThreshold) / 10
			
		if iStateReligion != -1:
			iStateReligionRatio = 100 * iStateReligionCities / iNumTotalCities
			iReligionStability += (iStateReligionRatio - 70) / 10
		
			if iCivicGovernment == con.iCivicTheocracy:
				iOnlyStateReligionRatio = 100 * iOnlyStateReligionCities / iNumTotalCities
				iReligionStability += iOnlyStateReligionRatio / 20
			
	#if iReligionStability > 0:
	#	sDomesticString += localText.getText('TXT_KEY_STABILITY_RELIGIOUS_UNITY', (iReligionStability,))
	#elif iReligionStability < 0:
	#	sDomesticString += localText.getText('TXT_KEY_STABILITY_RELIGIOUS_DISUNITY', (iReligionStability,))
	
	lParameters[con.iParameterReligion] = iReligionStability
		
	iDomesticStability += iReligionStability
	
	# FOREIGN
	iForeignStability = 0
	iNeighborStability = 0
	iVassalStability = 0
	iDefensivePactStability = 0
	iRelationStability = 0
	iAutocracyStability = 0
	iFanaticismStability = 0
	
	for iLoopPlayer in range(con.iNumPlayers):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		tLoopPlayer = gc.getTeam(pLoopPlayer.getTeam())
		iLoopScore = pLoopPlayer.getScoreHistory(iGameTurn)
	
		# neighbor stability
		if utils.isNeighbor(iPlayer, iLoopPlayer) or iLoopPlayer in con.lNeighbours[iPlayer]:
			if tPlayer.isOpenBorders(iLoopPlayer):
				#if getStabilityLevel(iLoopPlayer) == con.iStabilityUnstable: iNeighborStability -= 3
				#elif getStabilityLevel(iLoopPlayer) == con.iStabilityCollapsing: iNeighborStability -= 5
				if getStabilityLevel(iLoopPlayer) == con.iStabilityCollapsing: iNeighborStability -= 3
				
		# vassal stability
		if tLoopPlayer.isVassal(iPlayer):
			if getStabilityLevel(iLoopPlayer) == con.iStabilityCollapsing: iVassalStability -= 5
			elif getStabilityLevel(iLoopPlayer) == con.iStabilitySolid: iVassalStability += 3
			
			if bVassalage: iVassalStability += 2
			
		# defensive pacts
		if tPlayer.isDefensivePact(iLoopPlayer):
			if iLoopScore > iPlayerScore: iDefensivePactStability += 5
			
		# bad relations
		if pLoopPlayer.AI_getAttitude(iPlayer) == AttitudeTypes.ATTITUDE_FURIOUS and not tPlayer.isAtWar(iLoopPlayer): iRelationStability -= 2
		
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
			
	#if iNeighborStability < 0:
	#	sForeignString += localText.getText('TXT_KEY_STABILITY_NEIGHBORS', (iNeighborStability,))
		
	#if iVassalStability > 0:
	#	sForeignString += localText.getText('TXT_KEY_STABILITY_VASSALS_POSITIVE', (iVassalStability,))
	#elif iVassalStability < 0:
	#	sForeignString += localText.getText('TXT_KEY_STABILITY_VASSALS_NEGATIVE', (iVassalStability,))
		
	#if iDefensivePactStability > 0:
	#	sForeignString += localText.getText('TXT_KEY_STABILITY_DEFENSIVE_PACTS', (iDefensivePactStability,))
		
	#if iRelationStability < 0:
	#	sForeignString += localText.getText('TXT_KEY_STABILITY_BAD_RELATIONS', (iRelationStability,))
		
	#if iWarStability > 0:
	#	if bAutocracy and bFanaticism:
	#		sForeignString += localText.getText('TXT_KEY_STABILITY_WARS_BOTH', (iWarStability,))
	#	elif bAutocracy:
	#		sForeignString += localText.getText('TXT_KEY_STABILITY_WARS_NEIGHBORS', (iWarStability,))
	#	elif bFanaticism:
	#		sForeignString += localText.getText('TXT_KEY_STABILITY_WARS_HEATHENS', (iWarStability,))
	
	lParameters[con.iParameterNeighbors] = iNeighborStability
	lParameters[con.iParameterVassals] = iVassalStability
	lParameters[con.iParameterDefensivePacts] = iDefensivePactStability
	lParameters[con.iParameterRelations] = iRelationStability
	lParameters[con.iParameterAutocracy] = iAutocracyStability
	lParameters[con.iParameterFanaticism] = iFanaticismStability
			
	iForeignStability += iNeighborStability + iVassalStability + iDefensivePactStability + iRelationStability + iAutocracyStability + iFanaticismStability
	
	# MILITARY
	
	iMilitaryStability = 0
	
	iWarSuccessStability = 0
	iMilitaryStrengthStability = 0
	iBarbarianLossesStability = 0
	
	iNumerator = 0
	iDenominator = 0
	
	# war success
	for iLoopPlayer in range(con.iNumPlayers):
		if tPlayer.isAtWar(iLoopPlayer) and gc.getPlayer(iLoopPlayer).isAlive():
			iOurSuccess = tPlayer.AI_getWarSuccess(iLoopPlayer)
			iTheirSuccess = gc.getTeam(iLoopPlayer).AI_getWarSuccess(iPlayer)
			iCombinedSuccess = iOurSuccess + iTheirSuccess
			
			# ignore insignificant wars
			if iCombinedSuccess < 20: continue
			
			iThisWarSuccess = 100 * iOurSuccess / iCombinedSuccess - 50
			
			#fThisWarSuccess = 1.0 * (1.0 * iOurSuccess/iCombinedSuccess - 1.0/2)
			
			iNumerator += iThisWarSuccess
			iDenominator += 1
				
			#utils.debugTextPopup(pPlayer.getCivilizationAdjective(0) + ' war against ' + gc.getPlayer(iLoopPlayer).getCivilizationShortDescription(0) + '\n' + pPlayer.getCivilizationAdjective(0) + ' success: ' + str(iOurSuccess) + '\n' + gc.getPlayer(iLoopPlayer).getCivilizationAdjective(0) + ' success: ' + str(iTheirSuccess) + '\nResulting stability: ' + str(iThisWarStability))
			
	if iDenominator > 0:
		iTotalSuccess = iNumerator / iDenominator
		
		if iTotalSuccess > 0:
			iWarSuccessStability = 10 * iTotalSuccess / 100
		else:
			iWarSuccessStability = int(20 * sigmoid(1.0 * iTotalSuccess / 100))
		
		#sLogString = pPlayer.getCivilizationAdjective(0) + ' total war success: ' + str(iTotalSuccess) + '\nStability: ' + str(iWarSuccessStability)
		
		#utils.debugTextPopup(sLogString)
			
	#if iWarSuccessStability > 0:
	#	sMilitaryString += localText.getText('TXT_KEY_STABILITY_WINNING_WARS', (iWarSuccessStability,))
	#elif iWarSuccessStability < 0:
	#	sMilitaryString += localText.getText('TXT_KEY_STABILITY_LOSING_WARS', (iWarSuccessStability,))
	
	lParameters[con.iParameterWarSuccess] = iWarSuccessStability
				
	iMilitaryStability += iWarSuccessStability
				
	# military strength
	if iPreviousPower != 0:
		iPowerDifference = iCurrentPower - iPreviousPower
		iPercentChange = 100 * iPowerDifference / iPreviousPower
		
		if iPercentChange < 0:
			iMilitaryStrengthStability = iPercentChange / 2
			if iMilitaryStrengthStability < -10: iMilitaryStrengthStability = -10
		
		#utils.debugTextPopup('Military strength: ' + pPlayer.getCivilizationShortDescription(0) + '\nCurrent power: ' + str(iCurrentPower) + '\nPrevious Power: ' + str(iPreviousPower) + '\nPercent change: ' + str(iPercentChange) + '\nStability change: ' + str(iMilitaryStrengthStability))
	
	#if iMilitaryStrengthStability < 0:
	#	sMilitaryString += localText.getText('TXT_KEY_STABILITY_LOSING_STRENGTH', (iMilitaryStrengthStability,))
	
	lParameters[con.iParameterMilitaryStrength] = iMilitaryStrengthStability
	
	iMilitaryStability += iMilitaryStrengthStability
	
	# apply barbarian losses
	iBarbarianLossesStability = -sd.getBarbarianLosses(iPlayer)
	
	lParameters[con.iParameterBarbarianLosses] = iBarbarianLossesStability
	
	iMilitaryStability += iBarbarianLossesStability
	
	iStability = iExpansionStability + iEconomyStability + iDomesticStability + iForeignStability + iMilitaryStability
	
	#utils.debugTextPopup(pPlayer.getCivilizationAdjective(0) + ' Stability: ' + str(iStability) + '\nExpansion: ' + str(iExpansionStability) + '\nEconomy: ' + str(iEconomyStability) + '\nDomestic: ' + str(iDomesticStability) + '\nForeign: ' + str(iForeignStability) + '\nMilitary: ' + str(iMilitaryStability))

	return iStability, [iExpansionStability, iEconomyStability, iDomesticStability, iForeignStability, iMilitaryStability], lParameters

def sigmoid(x):
	return 2.0 / (1 + math.exp(-5*x)) - 1.0
	
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
	
	for iLoopPlayer in range(con.iNumPlayers):
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
	lCommerceValues = utils.getSortedList([i for i in range(con.iNumPlayers)], lambda x : gc.getPlayer(x).getEconomyHistory(iTurn), True)
	return lCommerceValues.index(iPlayer)
	
def calculatePowerRank(iPlayer, iTurn):
	lPowerValues = utils.getSortedList([i for i in range(con.iNumPlayers)], lambda x : gc.getPlayer(x).getPowerHistory(iTurn), True)
	return lPowerValues.index(iPlayer)
	
def isTolerated(iPlayer, iReligion):
	pPlayer = gc.getPlayer(iPlayer)
	iStateReligion = pPlayer.getStateReligion()
	lChristianity = [con.iCatholicism, con.iOrthodoxy, con.iProtestantism]
	
	# Secularism civic
	if pPlayer.getCivics(4) == con.iCivicSecularism: return True
	
	# Mughal UP
	if iPlayer == con.iMughals: return True
	
	# Polish UP
	if iPlayer == con.iPoland:
		if pPlayer.getStateReligion() in lChristianity and iReligion in lChristianity:
			return True
	
	# Exceptions
	if iStateReligion == con.iConfucianism and iReligion == con.iTaoism: return True
	if iStateReligion == con.iTaoism and iReligion == con.iConfucianism: return True
	if iStateReligion == con.iHinduism and iReligion == con.iBuddhism: return True
	if iStateReligion == con.iBuddhism and iReligion == con.iHinduism: return True
	
	return False
	
def isOverseas(city):
	capital = gc.getPlayer(city.getOwner()).getCapitalCity()
	
	return (capital.plot().getArea() != city.plot().getArea())
	
# use score history to determine last turn the civ was alive
def getLastTurnAlive(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iCurrentTurn = gc.getGame().getGameTurn()
	
	if pPlayer.isAlive(): return iCurrentTurn
	
	for iTurn in range(iCurrentTurn, 0, -1):
		if pPlayer.getScoreHistory(iTurn) > 0:
			return iTurn
			
	return 0

def checkResurrection(iGameTurn):

	iNationalismModifier = min(20, 4 * utils.getCivsWithNationalism())
	
	iRand = gc.getGame().getSorenRandNum(con.iNumPlayers, 'random starting civ')
	bDeadCivFound = False
	
	# iterate all civs starting with a random civ
	for i in range(iRand, iRand + con.iNumPlayers):
		iLoopCiv = i % con.iNumPlayers
		bPossible = False
		iMinNumCities = 2
		
		# special case Netherlands: need only one city to respawn (Amsterdam)
		if iLoopCiv == con.iNetherlands:
			iMinNumCities = 1
			
		# check if only recently died
		if iGameTurn - getLastTurnAlive(iLoopCiv) < utils.getTurns(20): continue
		
		# check if the civ can be reborn at this date
		if len(con.tResurrectionIntervals[iLoopCiv]) > 0:
			for tInterval in con.tResurrectionIntervals[iLoopCiv]:
				iStart, iEnd = tInterval
				if getTurnForYear(iStart) <= iGameTurn <= getTurnForYear(iEnd):
					bPossible = True
					break
					
		# Thailand cannot respawn when Khmer is alive and vice versa
		if iLoopCiv == con.iThailand and gc.getPlayer(con.iKhmer).isAlive(): bPossible = False
		if iLoopCiv == con.iKhmer and gc.getPlayer(con.iThailand).isAlive(): bPossible = False
		
		# Rome cannot respawn when Italy is alive and vice versa
		if iLoopCiv == con.iRome and gc.getPlayer(con.iItaly).isAlive(): bPossible = False
		if iLoopCiv == con.iItaly and gc.getPlayer(con.iRome).isAlive(): bPossible = False
		
		# Greece cannot respawn when Byzantium is alive and vice versa
		if iLoopCiv == con.iGreece and gc.getPlayer(con.iByzantium).isAlive(): bPossible = False
		if iLoopCiv == con.iByzantium and gc.getPlayer(con.iGreece).isAlive(): bPossible = False
		
		# India cannot respawn when Mughals are alive (not vice versa -> Pakistan)
		if iLoopCiv == con.iIndia and gc.getPlayer(con.iMughals).isAlive(): bPossible = False
		
		if bPossible and not gc.getPlayer(iLoopCiv).isAlive() and iGameTurn > utils.getLastTurnAlive(iLoopCiv) + utils.getTurns(20):
			if con.tRebirth[iLoopCiv] == -1:
				iRespawnRoll = gc.getGame().getSorenRandNum(100, 'Respawn Roll')
				if iRespawnRoll + iNationalismModifier - 10 >= con.tResurrectionProb[iLoopCiv]:
					lCityList = getResurrectionCities(iLoopCiv)
					if len(lCityList) >= iMinNumCities:
						doResurrection(iLoopCiv, lCityList)
						return
						
def getResurrectionCities(iPlayer, bFromCollapse = False):

	pPlayer = gc.getPlayer(iPlayer)
	teamPlayer = gc.getTeam(iPlayer)
	iReborn = utils.getReborn(iPlayer)
	lPotentialCities = []
	lFlippingCities = []
	
	iMinNumCitiesOwner = 3
	
	tTopLeft = con.tNormalAreasTL[iReborn][iPlayer]
	tBottomRight = con.tNormalAreasBR[iReborn][iPlayer]
	tExceptions = con.tNormalAreasSubtract[iReborn][iPlayer]
	tCapital = con.tCapitals[iReborn][iPlayer]
	
	if con.tRespawnTL[iPlayer] != -1:
		tTopLeft = con.tRespawnTL[iPlayer]
		tBottomRight = con.tRespawnBR[iPlayer]
		tExceptions = ()
		
	if con.tRespawnCapitals[iPlayer] != -1:
		tCapital = con.tRespawnCapitals[iPlayer]
		
	for x in range(tTopLeft[0], tBottomRight[0]+1):
		for y in range(tTopLeft[1], tBottomRight[1]+1):
			if (x, y) not in tExceptions:
				plot = gc.getMap().plot(x, y)
				if plot.isCity():
					city = plot.getPlotCity()
					# for humans: exclude recently conquered cities to avoid annoying reflips
					if city.getOwner() != utils.getHumanID() or city.getGameTurnAcquired() < gc.getGame().getGameTurn() - utils.getTurns(5):
						lPotentialCities.append(city)
					
	for k in range(len(lPotentialCities)):
		city = lPotentialCities[k]
		iOwner = city.getOwner()
		
		print str(city.getName())
		
		# barbarian and minor cities always flip
		if iOwner >= con.iNumPlayers:
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
				if iOwnerStability < con.iStabilityShaky:
					lFlippingCities.append(city)
				continue
		
			# owner stability below -10: city always flips
			if iOwnerStability < con.iStabilityShaky:
				lFlippingCities.append(city)
				
			# owner stability below 10: city flips if far away from their capital, or is capital spot of the dead civ
			elif iOwnerStability < con.iStabilityStable:
				ownerCapital = gc.getPlayer(iOwner).getCapitalCity()
				iDistance = utils.calculateDistance(city.getX(), city.getY(), ownerCapital.getX(), ownerCapital.getY())
				if bCapital or iDistance >= 8:
					lFlippingCities.append(city)
				
			# owner stability below 20: only capital spot flips
			elif iOwnerStability < con.iStabilitySolid:
				if bCapital:
					lFlippingCities.append(city)
					
		# if only up to two cities wouldn't flip, they flip as well (but at least one city has to flip already, else the respawn fails)
		if len(lFlippingCities) + 2 >= len(lPotentialCities) and len(lFlippingCities) > 0 and not bFromCollapse:
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
	
	for iOtherCiv in range(con.iNumPlayers):
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
	for iMinor in range(con.iNumPlayers, con.iNumTotalPlayersB): # including barbarians
		if gc.getPlayer(iMinor).isAlive():
			for city in utils.getCityList(iMinor):
				if city.getOriginalOwner() == iPlayer:
					x = city.getX()
					y = city.getY()
					if pPlayer.getSettlersMaps(67-y, x) >= 90:
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
			utils.completeCityFlip(x, y, iPlayer, iOwner, 100, False, True, True)
			utils.flipUnitsInArea((x-2, y-2), (x+2, y+2), iPlayer, iOwner, True, False)
	
		else:
			utils.cultureManager((x, y), 75, iPlayer, iOwner, False, True, True)
			utils.pushOutGarrisons((x, y), iOwner)
			utils.relocateSeaGarrisons((x, y), iOwner)
			sd.setTempFlippingCity((x, y))
			utils.flipCity((x, y), 0, 0, iPlayer, [iOwner])
			utils.createGarrisons(sd.getTempFlippingCity(), iPlayer, iGarrison)
			
		newCity = gc.getMap().plot(x, y).getPlotCity()
		
		# Leoreth: rebuild some city infrastructure
		for iBuilding in range(con.iNumBuildings):
			if pPlayer.canConstruct(iBuilding, True, False, False) and pPlayer.getCurrentEra() >= gc.getBuildingInfo(iBuilding).getFreeStartEra() and not utils.isUniqueBuilding(iBuilding) and gc.getBuildingInfo(iBuilding).getPrereqReligion() == -1:
				newCity.setHasRealBuilding(iBuilding, True)
			
		if bCapital:
			relocateCapital(iOwner)
			
		if iOwner not in lOwners:
			lOwners.append(iOwner)
			
	for iOwner in lOwners:
		teamOwner = gc.getTeam(iOwner)
		bOwnerHumanVassal = teamOwner.isVassal(iHuman)
	
		if iOwner != iHuman and iOwner != iPlayer and iOwner != con.iBarbarian:
			iRand = gc.getGame().getSorenRandNum(100, 'Stop birth')
			
			if iRand >= con.tAIStopBirthThreshold[iOwner] and not bOwnerHumanVassal:
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
		
	CyInterface().addMessage(iHuman, True, con.iDuration, CyTranslator().getText("TXT_KEY_INDEPENDENCE_TEXT", (pPlayer.getCivilizationAdjectiveKey(),)), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
	
	if bAskFlip and iHuman in lOwners:
		rebellionPopup(iPlayer)
		
	sd.setStabilityLevel(iPlayer, con.iStabilityStable)
	
	utils.setPlagueCountdown(iPlayer, -10)
	utils.clearPlague(iPlayer)
	convertBackCulture(iPlayer)
	
	# resurrection leaders
	if iPlayer in con.resurrectionLeaders:
		if pPlayer.getLeader() != con.resurrectionLeaders[iPlayer]:
			pPlayer.setLeader(con.resurrectionLeaders[iPlayer])
			
	# Leoreth: report to dynamic civs
	dc.onCivRespawn(iPlayer, lOwners)
	
	return
	
def getResurrectionTechs(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iCurrentEra = gc.getGame().getCurrentEra()
	lTechList = []
	lSourceCivs = []
	
	# same tech group
	for lRegionList in con.lTechGroups:
		if iPlayer in lRegionList:
			for iPeer in lRegionList:
				if iPeer != iPlayer and gc.getPlayer(iPeer).isAlive():
					lSourceCivs.append(iPeer)
			
	# direct neighbors (India can benefit from England etc), can count twice
	for iPeer in range(con.iNumPlayers):
		if iPeer != iPlayer and gc.getPlayer(iPeer).isAlive():
			if utils.isNeighbor(iPlayer, iPeer):
				lSourceCivs.append(iPeer)
				
	# use independents as source civs in case no other can be found
	if len(lSourceCivs) == 0:
		lSourceCivs.append(con.iIndependent)
		lSourceCivs.append(con.iIndependent2)
	
	for iTech in range(con.iNumTechs):
		
		# all techs from previous eras for free
		if gc.getTechInfo(iTech).getEra() < iCurrentEra:
			lTechList.append(iTech)
			continue
			
		# at least half of the source civs know this technology
		iCount = 0
		for iOtherCiv in lSourceCivs:
			if gc.getTeam(iOtherCiv).isHasTech(iTech):
				iCount += 1
				
		if 2 * iCount >= len(lSourceCivs):
			lTechList.append(iTech)
			
	return lTechList
	
def relocateCapital(iPlayer, bResurrection = False):
	if gc.getPlayer(iPlayer).getNumCities() == 0: return

	tCapital = con.tCapitals[utils.getReborn(iPlayer)][iPlayer]
	oldCapital = gc.getPlayer(iPlayer).getCapitalCity()
	
	if bResurrection and con.tRespawnCapitals[iPlayer] != -1:
		tCapital = con.tRespawnCapitals[iPlayer]
		
	x, y = tCapital
	plot = gc.getMap().plot(x, y)
	if plot.isCity() and plot.getPlotCity().getOwner() == iPlayer:
		newCapital = gc.getMap().plot(x, y).getPlotCity()	
	else:
		newCapital = utils.getHighestEntry(utils.getCityList(iPlayer), lambda x: max(0, utils.getTurns(500)-x.getGameTurnFounded()) + x.getPopulation()*5)
		
	oldCapital.setHasRealBuilding(con.iPalace, False)
	newCapital.setHasRealBuilding(con.iPalace, True)

def convertBackCulture(iCiv):
	tTopLeft = con.tNormalAreasTL[utils.getReborn(iCiv)][iCiv]
	tBottomRight = con.tNormalAreasBR[utils.getReborn(iCiv)][iCiv]  

	if con.tRespawnTL[iCiv] != -1:
		tTopLeft = con.tRespawnTL[iCiv]
		tBottomRight = con.tRespawnBR[iCiv]
		
	for x in range(tTopLeft[0], tBottomRight[0]+1):
		for y in range(tTopLeft[1], tBottomRight[1]+1):
			plot = gc.getMap().plot(x, y)
			if plot.isCity():
				city = plot.getPlotCity()
				if city.getOwner() == iCiv:
					iCulture = 0
					for iMinor in range(con.iNumPlayers, con.iNumTotalPlayersB):
						iCulture += city.getCulture(iMinor)
						city.setCulture(iMinor, 0, True)
					city.changeCulture(iCiv, iCulture, True)
			elif plot.isCityRadius() and plot.getOwner() == iCiv:
				iCulture = 0
				for iMinor in range(iNumPlayers, con.iNumTotalPlayersB):
					iCulture += plot.getCulture(iMinor)
					plot.setCulture(iMinor, 0, True)
				plot.changeCulture(iCiv, iCulture, True)
		
def setStateReligion(iCiv):
	iReborn = utils.getReborn(iCiv)
	lCities = utils.getAreaCities(con.tCoreAreasTL[iReborn][iCiv], con.tCoreAreasBR[iReborn][iCiv], con.tExceptions[iReborn][iCiv])
	lReligions = [0 for i in range(con.iNumReligions)]
	
	for city in lCities:
		for iReligion in range(con.iNumReligions):
			if city.isHasReligion(iReligion): lReligions[iReligion] += 1
			
	iHighestEntry = utils.getHighestEntry(lReligions)
	
	if iHighestEntry > 0:
		gc.getPlayer(iCiv).setLastStateReligion(lReligions.index(iHighestEntry))                                                       
                                
def rebellionPopup(iRebelCiv):
	utils.showPopup(7622, CyTranslator().getText("TXT_KEY_REBELLION_TITLE", ()), \
		       CyTranslator().getText("TXT_KEY_REBELLION_TEXT", (gc.getPlayer(iRebelCiv).getCivilizationAdjectiveKey(),)), \
		       (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), \
			CyTranslator().getText("TXT_KEY_POPUP_NO", ())))