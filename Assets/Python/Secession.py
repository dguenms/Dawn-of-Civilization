from Core import *
from RFCUtils import *
from Locations import *
from Resurrection import *

	
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
				iClaimantPlayer = slot(iClaimant)
				secedeCity(city, iClaimantPlayer, not bComplete, iArmyPercent)
		
		# if sufficient for resurrection, resurrect civs
		elif isResurrectionPossible() and canResurrectFromCities(iClaimant, claimedCities):
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

def canBeRazed(city):	
	if city.isHolyCity():
		return False

	# always raze Harappan cities, except holy city
	if civ(city) == iHarappa and not player(city).isHuman():
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
	possibleClaims = players.major().alive().without(iOwner).before_fall()
	
	# claim based on core territory
	coreClaims = possibleClaims.where(lambda p: city.isPlayerCore(p))
	if coreClaims:
		return civ(coreClaims.maximum(lambda p: plot(city).getPlayerSettlerValue(p)))
	
	# claim based on original owner, unless lost a long time ago
	iOriginalOwner = possibleClaims.ai().where(city.isOriginalOwner).first()
	if iOriginalOwner is not None:
		if plot(city).getPlayerSettlerValue(iOriginalOwner) >= 90:
			if city.getGameTurnPlayerLost(iOriginalOwner) >= turn() - turns(50):
				return civ(iOriginalOwner)
	
	# claim based on culture
	iTotalCulture = plot(city).countTotalCulture()
	cultureClaims = possibleClaims.ai().where(lambda p: iTotalCulture > 0 and 100 * plot(city).getCulture(p) / iTotalCulture >= 75)
	if cultureClaims:
		iCultureClaim = cultureClaims.maximum(lambda p: plot(city).getCulture(p))
		return civ(iCultureClaim)
	
	# claim based on war targets: needs to be winning the war based on war success, not available to human player
	closest = closestCity(city, same_continent=True)
	warClaims = possibleClaims.without(active()).where(lambda p: team(p).isAtWar(team(iOwner).getID()) and player(p).getWarValue(*location(city)) >= 8 and team(p).AI_getWarSuccess(team(iOwner).getID()) > team(iOwner).AI_getWarSuccess(team(p).getID()))
	warClaims = warClaims.where(lambda p: not closest or closest.getOwner() == p or not team(iOwner).isAtWar(closest.getOwner()))
	warClaims = warClaims.where(lambda p: closestCity(city, owner=p, same_continent=True) and distance(city, closestCity(city, owner=p, same_continent=True)) <= 12)
	if warClaims:
		iWarClaim = warClaims.maximum(lambda p: team(p).AI_getWarSuccess(team(iOwner).getID()) - team(iOwner).AI_getWarSuccess(team(p).getID()))
		return civ(iWarClaim)
	
	# claim for dead civilisation that can be resurrected
	resurrections = civs.major().before_fall().without(iOwner).where(canRespawn).where(lambda c: city in cities.respawn(c))
	if resurrections:
		return resurrections.maximum(lambda c: (city.isCore(c), plot(city).getSettlerValue(c)))
	
	return -1
		
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
		
def getPossibleMinors(iPlayer):
	lPossibleMinors = [iIndependent, iIndependent2]

	if gc.getGame().countKnownTechNumTeams(iNationalism) == 0 and civ(iPlayer) in [iMaya, iAztecs, iInca, iMali, iEthiopia, iCongo]:
		lPossibleMinors = [iNative]
		
	if gc.getGame().getCurrentEra() <= iMedieval:
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