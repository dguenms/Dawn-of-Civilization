from RFCUtils import *
from Core import *

from Events import handler

import Logging as log


iDuration = 6

tPlagueDates = (170, 500, 1350, 1650, 1850)


@handler("GameStart")
def setup():
	for iPlayer in players.major():
		data.players[iPlayer].iPlagueCountdown = -turns(iImmunity)
		
	data.lGenericPlagueTurns = [iYear > scenarioStartYear() and year(iYear + rand(-50, 50)) or -1 for iYear in tPlagueDates]
	
	undoPlague = rand(5)
	if undoPlague in (0, 3):
		data.lGenericPlagueTurns[undoPlague] = -1
	
	if civ() == iPoland:
		data.lGenericPlagueTurns[2] = year(1400)+1
	

@handler("cityAcquired")
def clearOrSpreadPlague(iOwner, iPlayer, city):
	if city.isHasRealBuilding(iPlague):
		if isVulnerable(iPlayer) and not data.players[iOwner].bFirstContactPlague:
			spreadPlague(iPlayer)
			infectCitiesNear(iPlayer, city)
		else:
			city.setHasRealBuilding(iPlague, False)

@handler("cityRazed")
def clearPlagueIfLastPlagueCityRazed(city, iNewOwner):
	if city.hasBuilding(iPlague):
		if data.players[iNewOwner].iPlagueCountdown > 0:
			if cities.owner(iNewOwner).without(city).none(lambda other: other.hasBuilding(iPlague)):
				data.players[iNewOwner].iPlagueCountdown = 0


@handler("BeginGameTurn")
def progressPlagueCountdown():
	if data.bNoPlagues:
		return

	for iPlayer in players.all().barbarian():
		if player(iPlayer).isExisting():
			if data.players[iPlayer].iPlagueCountdown > 0:
				data.players[iPlayer].iPlagueCountdown -= 1
				if data.players[iPlayer].iPlagueCountdown == 2:
					preStopPlague(iPlayer)
				elif data.players[iPlayer].iPlagueCountdown == 0:
					stopPlague(iPlayer)
			elif data.players[iPlayer].iPlagueCountdown < 0:
				data.players[iPlayer].iPlagueCountdown += 1


@handler("BeginGameTurn")
def startPlagues(iGameTurn):
	if data.bNoPlagues:
		return

	for iPlague, iPlagueDate in enumerate(data.lGenericPlagueTurns):
		if iGameTurn == iPlagueDate:
			startPlague(iPlague)

		if iPlague >= 2:
			#retry if the epidemic is dead too quickly
			if iGameTurn == iPlagueDate + 4:
				iInfectedCounter = 0
				for iPlayer in players.all().barbarian():
					if data.players[iPlayer].iPlagueCountdown > 0:
						iInfectedCounter += 1
				if iInfectedCounter == 1:
					startPlague(iPlague)

		if iPlague == 3 or iPlague == 4:
			if iGameTurn == iPlagueDate + 8:
				iInfectedCounter = 0
				for iPlayer in players.all().barbarian():
					if data.players[iPlayer].iPlagueCountdown > 0:
						iInfectedCounter += 1
				if iInfectedCounter <= 2:
					startPlague(iPlague)


@handler("BeginPlayerTurn")
def processPlague(iGameTurn, iPlayer):
	if data.bNoPlagues:
		return
	
	if is_minor(iPlayer):
		return
	
	if data.players[iPlayer].iPlagueCountdown <= 0:
		return

	# collect cities with and without plague
	infectedCities, uninfectedCities = cities.owner(iPlayer).split(lambda city: city.isHasRealBuilding(iPlague))
		
	for city in infectedCities:
		# let plague affect city
		losePopulation(city)
		
		# let plague spread to vassals
		if city.isCapital():
			spreadToVassals(iPlayer)
			
		# let plague affect surrounding area
		spreadToSurroundings(city)
		
		# let plague damage nearby units
		damageNearbyUnits(city)
		
		# let plague spread through trade routes
		spreadAlongTradeRoutes(city)
		
	# spread within the civilization
	spreadBetweenCities(iPlayer, infectedCities, uninfectedCities)


@handler("firstContact")
def newWorldPlague(iTeamX, iHasMetTeamY):
	if data.bNoPlagues:
		return
		
	if year() <= year(dBirth[iAztecs]):
		return
	
	if year() >= year(1800):
		return
		
	iOldWorld = matching(lambda iPlayer: civ(iPlayer) not in lBioNewWorld, iTeamX, iHasMetTeamY)
	iNewWorld = matching(lambda iPlayer: civ(iPlayer) in lBioNewWorld, iTeamX, iHasMetTeamY)
	
	if iOldWorld is None or iNewWorld is None:
		return
	
	if is_minor(iOldWorld):
		return
	
	if data.players[iNewWorld].iPlagueCountdown == 0:
		if not team(iNewWorld).isHasTech(iMicrobiology):
			city = cities.owner(iNewWorld).random()
			
			if city:
				iHealth = calculateHealth(iNewWorld)
				if rand(100) > 30 + iHealth / 2:
					data.players[iNewWorld].iPlagueCountdown = iDuration - iHealth / 10
					data.players[iNewWorld].bFirstContactPlague = True
					
					infectCity(city)
					announceForeignPlagueSpread(city)


@handler("techAcquired")
def acquireVaccine(iTech, iTeam, iPlayer):
	if iTech == iMicrobiology:
		if data.players[iPlayer].iPlagueCountdown > 1:
			data.players[iPlayer].iPlagueCountdown = 1


def calculateTotalPlagueHealth(iPlayer, iPlague):
	iHealth = calculateHealth(iPlayer) / 2
	
	if player(iPlayer).calculateTotalCityHealthiness() > 0:
		iHealth += rand(40)
		
		if iPlague == 1: # plague of Justinian
			if civ(iPlayer) in dCivGroups[iCivGroupEurope] + dCivGroups[iCivGroupMiddleEast]:
				iHealth -= 10
		if iPlague == 2: # medieval Black Death
			if civ(iPlayer) in dCivGroups[iCivGroupEurope]:
				iHealth -= 5
	
	return iHealth


def startPlague(iPlague):
	for iCivGroup, lRegions in dCivGroupRegions.items():
		if iCivGroup == iCivGroupAmerica and True not in data.dFirstContactConquerors.values():
			continue
		
		city = cities.regions(*lRegions).where(lambda city: not is_minor(city.getOwner()) and isVulnerable(city.getOwner()) and calculateTotalPlagueHealth(city.getOwner(), iPlague) <= 200).random()
		if city:
			spreadPlague(city.getOwner())
			infectCity(city)
			announceForeignPlagueSpread(city)


def isVulnerable(iPlayer):
	# protect some civs from Plague for more predictable UHVs
	if civ(iPlayer) == iCongo and year() <= year(1650): return
	elif civ(iPlayer) == iMali and year() <= year(1500): return
	
	if is_minor(iPlayer) and -10 < data.players[iPlayer].iPlagueCountdown <= 0: #more vulnerable
		return True
			
	pPlayer = player(iPlayer)
		
	if team(iPlayer).isHasTech(iMicrobiology): return False
	
	if civ(iPlayer) in lBioNewWorld and not data.dFirstContactConquerors[civ(iPlayer)]: return False
		
	if data.players[iPlayer].iPlagueCountdown == 0: #vulnerable
		if not team(iPlayer).isHasTech(iMicrobiology):
			iHealth = calculateHealth(iPlayer)
			if iHealth < 14: #no spread for iHealth >= 74 years
				return True
				
	return False


def calculateHealth(iPlayer):
	pPlayer = player(iPlayer)
	if pPlayer.calculateTotalCityHealthiness() > 0:
		return int((1.0 * pPlayer.calculateTotalCityHealthiness()) / (pPlayer.calculateTotalCityHealthiness() + \
			pPlayer.calculateTotalCityUnhealthiness()) * 100) - 60
	return -30


def spreadPlague(iPlayer):
	pPlayer = player(iPlayer)
	iHealth = calculateHealth(iPlayer) / 7 # duration range will be -4 to +4 for 30 to 90
	data.players[iPlayer].iPlagueCountdown = min(9, iDuration - iHealth)


def infectCity(city):
	city.setHasRealBuilding(iPlague, True)
	message(city.getOwner(), 'TXT_KEY_PLAGUE_SPREAD_CITY', city.getName(), sound='AS2D_PLAGUE', color=iLime)
	
	dImprovementDowngrade = dict((infos.improvement(iImprovement).getImprovementUpgrade(), iImprovement) for iImprovement in infos.improvements() if infos.improvement(iImprovement).getImprovementUpgrade() >= 0)
	
	for plot in plots.city_radius(city):
		iImprovement = plot.getImprovementType()
		if iImprovement >= 0:
			iUpgradeTime = infos.improvement(iImprovement).getUpgradeTime()
			if plot.getUpgradeProgress() > iUpgradeTime / 2:
				plot.setUpgradeProgress(0)
			elif iImprovement in dImprovementDowngrade:
				plot.setImprovementType(dImprovementDowngrade[iImprovement])
			
	killUnitsByPlague(city, plot_(city), 0, 100, 0)


def killUnitsByPlague(city, plot, baseValue, iDamage, iPreserveDefenders):
	iOwner = city.getOwner()
	pOwner = player(city)
	teamOwner = team(city)
	
	#deadly plague when human player isn't born yet, will speed up the loading
	if turn() < year(dBirth[active()]) + turns(20):
		iDamage += 10
		baseValue -= 5

	iPreserveHumanDefenders = iPreserveDefenders
	if iPreserveDefenders > 0:
		if not pOwner.isHuman():
			if teamOwner.isAtWar(active()):
				iPreserveDefenders += 2
			elif any(civ(iOwner) in lCivGroup and civ() in lCivGroup for lCivGroup in dCivGroups.values()):
				iPreserveDefenders += 1
						
	# TODO: look from overlap
	for unit in units.at(plot):
		if player(unit).isHuman():
			if iPreserveHumanDefenders > 0:
				if isDefenderUnit(unit):
					iPreserveHumanDefenders -= 1
					if plot.getNumUnits() <= iPreserveDefenders:
						iMaxDamage = 50
						if unit.workRate(100) > 0 and not unit.canFight(): iMaxDamage = 100
						unit.setDamage(min(iMaxDamage, unit.getDamage() + iDamage - 20), barbarian())
					continue

		elif iPreserveDefenders > 0:
			if isDefenderUnit(unit):
				iPreserveDefenders -= 1
				if plot.getNumUnits() <= iPreserveDefenders and team(unit).isAtWar(active()):
					iMaxDamage = 50
					if unit.workRate(100) > 0 and not unit.canFight(): iMaxDamage = 100
					unit.setDamage(min(iMaxDamage, unit.getDamage() + iDamage - 20), barbarian())
				continue

		if isMortalUnit(unit):
			iThreshold = baseValue + 5 * city.healthRate(False, 0)
			
			if teamOwner.isAtWar(active()) and not is_minor(iOwner):
				if unit.getOwner() == iOwner:
					iDamage *= 3
					iDamage /= 4
				
			if data.players[city.getOwner()].bFirstContactPlague:
				if civ(unit) not in lNewWorld and not is_minor(unit):
					iDamage /= 2
					
			if rand(100) > iThreshold:
				iMaxDamage = 50
				if unit.workRate(100) > 0 and not unit.canFight(): iMaxDamage = 100
				unit.setDamage(min(iMaxDamage, unit.getDamage() + iDamage - unit.getExperience()/10 - unit.baseCombatStr()/2), barbarian())
				break


def announceForeignPlagueSpread(city):
	iOwner = city.getOwner()
	if player().canContact(iOwner) and active() != iOwner and city.isRevealed(active(), False):
		message(active(), 'TXT_KEY_PLAGUE_SPREAD_CITY', '%s (%s)' % (city.getName(), adjective(iOwner)), sound='AS2D_PLAGUE', color=iLime)

			
def losePopulation(city):
	if city.getPopulation() <= 1: return
	
	iHealth = city.healthRate(False, 0)	
	if rand(100) > 40 + 5 * iHealth:
		city.changePopulation(-1)


def spreadToVassals(iPlayer):
	if data.players[iPlayer].bFirstContactPlague: return
	
	for iLoopPlayer in players.major().where(isVulnerable):
		if team(iPlayer).isVassal(iLoopPlayer) or team(iLoopPlayer).isVassal(iPlayer):
			if data.players[iLoopPlayer].iPlagueCountdown > 2:
				if player(iLoopPlayer).getNumCities() > 0:
					capital = player(iLoopPlayer).getCapitalCity()
					spreadPlague(iLoopPlayer)
					infectCity(capital)


def spreadToSurroundings(city):
	iPlayer = city.getOwner()
	
	# do not spread if plague is almost over
	if data.players[iPlayer].iPlagueCountdown <= 2:
		return

	for plot in plots.surrounding(city, radius=2):
		if not plot.isOwned():
			continue
			
		if at(city, plot):
			continue
		
		if plot.getOwner() == iPlayer:
			plotCity = city_(plot)
			if plotCity:
				if not plotCity.isHasRealBuilding(iPlague):
					infectCity(plotCity)
		
		else:
			if data.players[iPlayer].bFirstContactPlague:
				continue
			
			if isVulnerable(plot.getOwner()):
				spreadPlague(plot.getOwner())
				infectCitiesNear(plot.getOwner(), plot)


def infectCitiesNear(iPlayer, tile):
	for city in cities.owner(iPlayer):
		if distance(city, tile) <= 3:
			infectCity(city)
			announceForeignPlagueSpread(city)


def damageNearbyUnits(city):
	for plot in plots.surrounding(city, radius=2):
		iDistance = distance(city, plot)
		
		if iDistance == 0:
			killUnitsByPlague(city, plot, 0, 42, 2)
		elif not plot.isCity():
			if iDistance < 3:
				if plot.isRoute():
					killUnitsByPlague(city, plot, 10, 35, 0)
				else:
					killUnitsByPlague(city, plot, 30, 35, 0)
			else:
				if plot.isRoute() or plot.isWater():
					killUnitsByPlague(city, plot, 30, 35, 0)


def spreadAlongTradeRoutes(city):
	iPlayer = city.getOwner()
	
	if data.players[iPlayer].bFirstContactPlague: return
	if data.players[iPlayer].iPlagueCountdown <= 2: return
	
	for iTradeRoute in range(city.getTradeRoutes()):
		tradeCity = city.getTradeCity(iTradeRoute)
		if not tradeCity.isNone():
			iOwner = tradeCity.getOwner()
			if not tradeCity.isHasRealBuilding(iPlague):
				if iPlayer == iOwner:
					infectCity(tradeCity)
				elif isVulnerable(iOwner):
					spreadPlague(iOwner)
					infectCity(tradeCity)
					announceForeignPlagueSpread(city)


def spreadBetweenCities(iPlayer, sourceCities, targetCities):
	if data.players[iPlayer].iPlagueCountdown <= 2: return
	
	target = targetCities.where(lambda city: sourceCities.any(lambda source: source.isConnectedTo(city) and distance(source, city) <= 6)).random()
	if target:
		infectCity(target)


def preStopPlague(iPlayer):
	iModifier = 0
	for city in cities.owner(iPlayer).where(lambda city: city.hasBuilding(iPlague)):
		if rand(100) > 30 - 5 * city.healthRate(False, 0) + iModifier:
			city.setHasRealBuilding(iPlague, False)
			iModifier += 5


def stopPlague(iPlayer):
	data.players[iPlayer].iPlagueCountdown = -turns(iImmunity)
	
	if data.players[iPlayer].bFirstContactPlague:
		data.players[iPlayer].iPlagueCountdown = -turns(iImmunity-30)
		
	data.players[iPlayer].bFirstContactPlague = False
	
	for city in cities.owner(iPlayer):
		city.setHasRealBuilding(iPlague, False)