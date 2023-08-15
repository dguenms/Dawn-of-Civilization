from Core import *
from RFCUtils import *
from Slots import *

from Popups import popup
from Events import events, handler


def makePeace(iRebelCiv):
	team().makePeace(iRebelCiv)
	
def declareWar(iRebelCiv):
	team().declareWar(iRebelCiv, False, -1)

RESURRECTION_POPUP = (
	popup.text("TXT_KEY_RESURRECTION_TEXT")
		.option(makePeace, "TXT_KEY_POPUP_YES", button='Art/Interface/Buttons/Actions/Join.dds')
		.option(declareWar, "TXT_KEY_POPUP_NO", button='Art/Interface/Buttons/Actions/Fortify.dds')
		.build()
)


@handler("BeginGameTurn")
def checkResurrection():
	if every(10):
		if not isResurrectionPossible():
			return
	
		iNationalismModifier = min(20, 4 * game.countKnownTechNumTeams(iNationalism))
		possibleResurrections = civs.major().where(canRespawn).sort(lambda c: (-getImpact(c), data.civs[c].iLastTurnAlive))
		
		# civs entirely controlled by minors will always respawn
		for iCiv in possibleResurrections:
			if cities.respawn(iCiv).all(is_minor):
				resurrectionCities = getResurrectionCities(iCiv)
				if canResurrectFromCities(iCiv, resurrectionCities):
					doResurrection(iCiv, resurrectionCities)
					return
					
		# otherwise minimum amount of cities and random chance are required
		for iCiv in possibleResurrections:
			if rand(100) - iNationalismModifier + 10 < dResurrectionProbability[iCiv]:
				resurrectionCities = getResurrectionCities(iCiv)
				if canResurrectFromCities(iCiv, resurrectionCities):
					doResurrection(iCiv, resurrectionCities)
					return


@handler("releasedCivilization")
def onReleasedPlayer(iPlayer, iReleasedCivilization):
	iReleasedCivilization = Civ(iReleasedCivilization)
	releasedCities = cities.owner(iPlayer).core(iReleasedCivilization).where(lambda city: not city.isPlayerCore(iPlayer) and not city.isCapital())

	doResurrection(iReleasedCivilization, releasedCities, bAskFlip=False, bDisplay=True)
	
	if slot(iReleasedCivilization) >= 0:
		player(iReleasedCivilization).AI_changeAttitudeExtra(iPlayer, 2)


def isResurrectionPossible():
	iTakenSlots = getUnavailableSlots()
	iAvailableSlots = iNumPlayers-1	
	return iTakenSlots + 1 < iAvailableSlots

						
def getResurrectionCities(iCiv, bFromCollapse=False):
	potentialCities = cities.respawn(iCiv)
	resurrectionCities = potentialCities.where(lambda city: isPartOfResurrection(iCiv, city, len(potentialCities) == 1))

	# if capital exists and not part of the resurrection, it fails, unless from collapse
	capital = cities.respawnCapital(iCiv)
	if not bFromCollapse and capital and capital not in resurrectionCities:
		return []
		
	# if existing cities sufficient for resurrection and close to including all potential cities, include the rest as well, unless from collapse
	if not bFromCollapse and canResurrectFromCities(iCiv, resurrectionCities):
		if resurrectionCities.count() + 2 >= potentialCities.count() and resurrectionCities.count() * 2 >= potentialCities.count():
			resurrectionCities += potentialCities.where(lambda city: not city.isOwnerCore())
			resurrectionCities = resurrectionCities.unique()
		
	# let civs keep at least two cities
	for iOwner in resurrectionCities.owners():
		iNumCities = cities.owner(iOwner).count()
		iNumFlippedCities = resurrectionCities.owner(iOwner).count()
		if iNumCities - iNumFlippedCities < 2:
			retainedCities = resurrectionCities.owner(iOwner).highest(2 - (iNumCities - iNumFlippedCities), lambda city: (city.isCapital(), city.plot().getPlayerSettlerValue(iOwner)))
			resurrectionCities = resurrectionCities.without(retainedCities)
	
	return resurrectionCities.entities()
					
def isPartOfResurrection(iCiv, city, bOnlyOne):
	iOwner = city.getOwner()
	
	# for humans: not for recently conquered cities to avoid annoying reflips
	if iOwner == active() and city.getGameTurnAcquired() > turn() - turns(5):
		return False
		
	# barbarian and minor cities always flip
	if is_minor(iOwner):
		return True
		
	# not if their core but not our core
	if city.isPlayerCore(iOwner) and not city.isCore(iCiv):
		return False
		
	iOwnerStability = stability(iOwner)
	bCapital = city.atPlot(plots.respawnCapital(iCiv))
	
	# flips are less likely before Nationalism
	if game.countKnownTechNumTeams(iNationalism) == 0:
		iOwnerStability += 1
	
	# flips are more likely between AIs to make the world more dynamic
	# TODO: maybe restore this during autoplay?
	#if not player(iOwner).isHuman() and not player(iPlayer).isHuman():
	#	iOwnerStability -= 1
	
	# if unstable or worse, all cities flip
	if iOwnerStability <= iStabilityUnstable:
		return True
	
	# if shaky, only the prospective capital, colonies or core cities that are not our core flip
	if iOwnerStability <= iStabilityShaky:
		if bCapital or (city.isCore(iCiv) and not city.isPlayerCore(iOwner)) or city.isColony():
			return True
	
	# if stable, only the prospective capital flips
	if iOwnerStability <= iStabilityStable:
		if bCapital and not bOnlyOne:
			return True
			
	return False

def canResurrectFromCities(iCiv, resurrectionCities):
	# cannot resurrect without cities
	if not resurrectionCities:
		return False

	# only one city is not sufficient for resurrection, unless there is only one city available
	if len(resurrectionCities) <= 1 and len(resurrectionCities) < cities.respawn(iCiv).count():
		return False

	# at least one city needs to be in core for the resurrecting civ
	if none(city.isCore(iCiv) for city in resurrectionCities):
		return False
	
	return True
	
def doResurrection(iCiv, lCityList, bAskFlip=True, bDisplay=False):
	iPlayer = findSlot(iCiv)
	if iPlayer == -1:
		log.rise("RESURRECTION ABORTED: NO FREE SLOT FOR: %s", infos.civ(iCiv).getText())
		return

	updateCivilization(iPlayer, iCiv)

	resurrectionCities = cities.of(lCityList)
	pPlayer = player(iPlayer)
	teamPlayer = team(iPlayer)
	iCiv = civ(iPlayer)
	
	pPlayer.setAlive(True, False)

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
	iNumCities = resurrectionCities.count()
	iGarrison = 2
	iArmySize = pPlayer.getCurrentEra()
	
	pPlayer.setLastBirthTurn(turn())
		
	# add former colonies that are still free
	for city in players.minor().existing().cities().where(lambda city: city.isOriginalOwner(iPlayer)):
		if pPlayer.getSettlerValue(city.getX(), city.getY()) >= 90:
			if city not in resurrectionCities:
				resurrectionCities = resurrectionCities.including(city)

	lOwners = []
	dRelocatedUnits = appenddict()
	
	# determine prevalent religion in the resurrection area
	iNewStateReligion = getPrevalentReligion(plots.of(resurrectionCities))
	
	# set state religion based on religions in the area
	if iNewStateReligion >= 0:
		pPlayer.setLastStateReligion(iNewStateReligion)
	
	for city in resurrectionCities:
		iOwner = city.getOwner()
		pOwner = player(iOwner)
		
		x = city.getX()
		y = city.getY()
		
		bCapital = city.isCapital()
		
		iNumDefenders = max(2, player(iPlayer).getCurrentEra()-1)
		lFlippedUnits, lRelocatedUnits = flipOrRelocateGarrison(city, iNumDefenders)
		dRelocatedUnits[iOwner].extend(lRelocatedUnits)
		
		iCultureChange = is_minor(iOwner) and 100 or 75
		completeCityFlip(city, iPlayer, iOwner, iCultureChange, False, True, True)
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
			if chance(dWarOnFlipProbability[iOwner]) and not bOwnerHumanVassal:
				teamOwner.declareWar(iPlayer, False, -1)
			else:
				teamOwner.makePeace(iPlayer)
			
	relocateCapital(iPlayer, cities.respawnCapital(iPlayer))
	
	# give the new civ a starting army
	capital = pPlayer.getCapitalCity()
	
	dStartingUnits = {
		iAttack: 2 * iArmySize + iNumCities,
		iShock: iArmySize,
		iCounter: iArmySize,
		iSiege: iArmySize + iNumCities,
	}
	createRoleUnits(iPlayer, capital, dStartingUnits.items())
	
	switchCivics(iPlayer)
		
	message(active(), 'TXT_KEY_INDEPENDENCE_TEXT', adjective(iPlayer), color=iGreen, force=True)
	
	if bAskFlip and active() in lOwners:
		resurrectionPopup(iPlayer)
		
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
	for lTechGroup in dTechGroups.values():
		if civ(iPlayer) in lTechGroup:
			for iPeer in lTechGroup:
				if civ(iPlayer) != iPeer and player(iPeer).isExisting():
					lSourcePlayers.append(iPeer)
			
	# direct neighbors (India can benefit from England etc)
	for iPeer in players.major().existing().without(iPlayer).without(lSourcePlayers):
		if game.isNeighbors(iPlayer, iPeer):
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
		
def switchCivics(iPlayer):
	pPlayer = player(iPlayer)

	for iCategory in range(iNumCivicCategories):
		iBestCivic = pPlayer.AI_bestCivic(iCategory)
		
		if iBestCivic >= 0:
			pPlayer.setCivics(iCategory, iBestCivic)
			
	pPlayer.setRevolutionTimer(gc.getDefineINT("MIN_REVOLUTION_TURNS"))

def resurrectionPopup(iResurrectionPlayer):
	RESURRECTION_POPUP.text(adjective(iResurrectionPlayer)).makePeace().declareWar().launch(iResurrectionPlayer)

def convertBackCulture(iPlayer):
	for city in cities.respawn(iPlayer).owner(iPlayer):
		iMinorCulture = players.minor().sum(city.getCulture)
		city.changeCulture(iPlayer, iMinorCulture, True)
	
		for iMinor in players.minor():
			city.setCulture(iMinor, 0, True)
	
	for plot in plots.respawn(iPlayer).owner(iPlayer):
		if plot.isCityRadius():
			iMinorCulture = players.minor().sum(plot.getCulture)
			plot.changeCulture(iPlayer, iMinorCulture, True)
			
			for iMinor in players.minor():
				plot.setCulture(iMinor, 0, True)

def getAdditionalResurrectionCities(iCiv, secedingCities):
	return [city for city in getResurrectionCities(iCiv, True) if city not in secedingCities]
	
def resurrectionFromCollapse(iCiv, lCityList):
	debug('Resurrection: %s', infos.civ(iCiv).getText())
			
	if lCityList:
		doResurrection(iCiv, lCityList, bAskFlip=False)
	
def setStabilityLevel(iPlayer, iStabilityLevel):
	if stability(iPlayer) == iStabilityLevel:
		return

	data.setStabilityLevel(iPlayer, iStabilityLevel)
	
	if iStabilityLevel >= iStabilityShaky:
		data.players[iPlayer].bDomesticCrisis = False
	
	if iStabilityLevel == iStabilityCollapsing:
		message(iPlayer, 'TXT_KEY_STABILITY_COLLAPSING_WARNING', color=iRed)