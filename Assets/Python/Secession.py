from Core import *
from RFCUtils import *
from Locations import *
from Resurrection import *

import CityNames as cn

	
def secession(iPlayer, secedingCities):
	data.setSecedingCities(iPlayer, secedingCities)

def secedeCities(iPlayer, secedingCities, bRazeMinorCities = False):
	iNumCities = player(iPlayer).getNumCities()
	if iNumCities <= 0:
		return

	iCiv = civ(iPlayer)
	bComplete = len(secedingCities) == player(iPlayer).getNumCities()
	iArmyPercent = 100 - 100 * len(secedingCities) / iNumCities
	
	if not secedingCities:
		return
	
	if bComplete:
		clearPlague(iPlayer)
	
	# if smaller cities are supposed to be destroyed, do that first
	destroyedCities, cededCities = secedingCities.split(lambda city: bRazeMinorCities and canBeRazed(city))
	
	for city in destroyedCities:
		cityPlot = plot(city)
		cn.clearChanges(city)
		player(iBarbarian).disband(city)
		cityPlot.setCulture(iPlayer, 0, True)
		
		# free up ruins for Indraprastha spawn
		if location(cityPlot) == tDelhi:
			cityPlot.setImprovementType(-1)
	
	# determine who has the best claim on each city
	dClaimedCities = appenddict()
	for city in cededCities:
		iClaim = getCityClaim(city)
		dClaimedCities[iClaim].append(city)
		
	lMinorCities = dClaimedCities.pop(-1, [])
		
	for iClaimant, claimedCities in dClaimedCities.items():
		game.setUpdatePlotGroups(False)
		
		# assign cities to living civs
		if player(iClaimant).isExisting():
			for city in claimedCities:
				iClaimantPlayer = slot(iClaimant)
				secedeCity(city, iClaimantPlayer, not bComplete, iArmyPercent)
		
		# if sufficient for resurrection, resurrect civs
		elif isResurrectionPossible() and canResurrectFromCities(iClaimant, claimedCities):
			additionalCities = getAdditionalResurrectionCities(iClaimant, secedingCities)
			resurrectionFromCollapse(iClaimant, claimedCities + additionalCities)
		
		# else cities go to minors
		else:
			lMinorCities.extend(claimedCities)
			
		game.setUpdatePlotGroups(True)
	
	# secede remaining cities to minors
	lPossibleMinors = getPossibleMinors(iPlayer)
	for iMinor, minorCities in cities.of(lMinorCities).divide(lPossibleMinors):
		game.setUpdatePlotGroups(False)
		for city in minorCities:
			secedeCity(city, iMinor, not bComplete, iArmyPercent)
		
		game.setUpdatePlotGroups(True)

	# notify for partial secessions
	if not bComplete and player().canContact(iPlayer):
		message(active(), 'TXT_KEY_STABILITY_CITIES_SECEDED', fullname(iPlayer), len(secedingCities))
	
	# prevent collapsing downward spiral
	balanceStability(iPlayer, iStabilityUnstable)

def canBeRazed(city):	
	if city.isHolyCity():
		return False
	
	if city.getNumActiveWorldWonders() > 0:
		return False

	# always raze Harappan, Hittite cities, except holy city
	if city.getCivilizationType() in [iHarappa, iHittites] and city.getOriginalCiv() in [iHarappa, iHittites] and not player(city).isHuman():
		return True
	
	if city.getPopulation() >= 10:
		return False
	
	if city.getCultureLevel() >= 3:
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
	possibleClaims = players.major().existing().without(iOwner).past_birth().before_fall()
	
	# claim based on core territory
	coreClaims = possibleClaims.where(lambda p: city.isPlayerCore(p))
	if coreClaims:
		return civ(coreClaims.maximum(lambda p: plot(city).getPlayerSettlerValue(p)))
	
	# claim based on original owner, unless lost a long time ago
	iOriginalOwner = possibleClaims.ai().where(city.isOriginalOwner).first()
	if iOriginalOwner is not None:
		if plot(city).getPlayerSettlerValue(iOriginalOwner) > 0:
			if city.getGameTurnPlayerLost(iOriginalOwner) >= turn() - turns(50):
				return civ(iOriginalOwner)
	
	# claim based on culture
	iTotalCulture = plot(city).countTotalCulture()
	cultureClaims = possibleClaims.ai().where(lambda p: iTotalCulture > 0 and 100 * plot(city).getCulture(p) / iTotalCulture >= 75)
	if cultureClaims:
		iCultureClaim = cultureClaims.maximum(lambda p: plot(city).getCulture(p))
		return civ(iCultureClaim)
	
	# claim based on war targets: needs to be winning the war based on war success, not available to human player
	warClaims = possibleClaims.where(lambda p: hasWarClaim(p, city))
	if warClaims:
		iWarClaim = warClaims.maximum(lambda p: team(p).AI_getWarSuccess(team(iOwner).getID()) - team(iOwner).AI_getWarSuccess(team(p).getID()))
		return civ(iWarClaim)
	
	# claim for dead civilisation that can be resurrected
	resurrections = civs.major().before_fall().without(iOwner).where(canRespawn).where(lambda c: city in cities.respawn(c))
	if resurrections:
		return resurrections.maximum(lambda c: (city.isCore(c), plot(city).getSettlerValue(c)))
	
	# holy cities are always assigned to independents
	if city.isHolyCity():
		return iIndependent
	
	return -1

def hasWarClaim(iPlayer, city):
	pPlayer = player(iPlayer)
	tPlayer = team(pPlayer.getTeam())
	
	iOwner = city.getOwner()
	pOwner = player(iOwner)
	tOwner = team(pOwner.getTeam())
	
	if pPlayer.isHuman():
		return False
	
	if not tPlayer.isAtWar(pOwner.getTeam()):
		return False
	
	if plot(city).getPlayerWarValue(iPlayer) < 4:
		return False
	
	if tPlayer.AI_getAtWarCounter(pOwner.getTeam()) < turns(10):
		return False
	
	if tPlayer.AI_getWarSuccess(pOwner.getTeam()) - tOwner.AI_getWarSuccess(pPlayer.getTeam()) < (autoplay() and 0 or tPlayer.AI_getAtWarCounter(pOwner.getTeam())):
		return False
	
	closest = closestCity(city, owner=iPlayer)
	if not closest:
		return False
	
	# if someone else owns a closer city and are also at war, leave it to them
	if closest.getOwner() != iPlayer and tOwner.isAtWar(closest.getOwner()):
		return False
	

	if distance(city, closest) > 12:
		return False
		
	return True
		
def secedeCity(city, iNewOwner, bRelocate, iArmyPercent):
	if not city: 
		return
	
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
	
	flipped_city = completeCityFlip(city, iNewOwner, city.getOwner(), 50, False, True, True)
	
	if flipped_city and civ(iOldOwner) == iToltecs:
		removeBuildings(flipped_city)
	
	if not player(iNewOwner).isMinorCiv():
		flipOrCreateDefenders(iNewOwner, lFlippedUnits, tile, iNumDefenders)
	else:
		killUnits(lFlippedUnits)
	
	if is_minor(iNewOwner):
		message(iOldOwner, 'TXT_KEY_STABILITY_CITY_INDEPENDENCE', name, color=iRed)
	else:
		message(iOldOwner, 'TXT_KEY_STABILITY_CITY_CHANGED_OWNER', name, adjective(iNewOwner), color=iRed)
		
	message(iNewOwner, 'TXT_KEY_STABILITY_CITY_CHANGED_OWNER_US', name, color=iRed)
		
def getPossibleMinors(iPlayer):
	lPossibleMinors = [iIndependent, iIndependent2]

	if gc.getGame().countKnownTechNumTeams(iNationalism) == 0 and civ(iPlayer) in [iMaya, iToltecs, iAztecs, iInca, iMali, iEthiopia, iCongo]:
		lPossibleMinors = [iNative]
		
	elif gc.getGame().getCurrentEra() <= iMedieval:
		lPossibleMinors = [iBarbarian, iIndependent, iIndependent2]
		
	return players.civs(*lPossibleMinors)
	
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