# Rhye's and Fall of Civilization - Historical Victory Goals


from CvPythonExtensions import *
import CvUtil
import PyHelpers
from Consts import *
from StoredData import data #edead
from RFCUtils import *
import random
from Events import handler

from Core import *

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

iDuration = 6

@handler("GameStart")
def setup():
	for iPlayer in players.major():
		data.players[iPlayer].iPlagueCountdown = -turns(iImmunity)
		
	data.lGenericPlagueDates[0] = 80
	data.lGenericPlagueDates[2] = 300 # safe value to prevent plague at start of 1700 AD scenario
	
	if scenario() == i3000BC:
		data.lGenericPlagueDates[0] = year(400).deviate(20)
		
	data.lGenericPlagueDates[1] = year(1300).deviate(20)
	
	# Avoid interfering with the Indian UHV
	if player(iIndia).isHuman() and data.lGenericPlagueDates[1] <= year(1200):
		data.lGenericPlagueDates[1] = year(1200) + 1
	
	if scenario() != i1700AD:
		data.lGenericPlagueDates[2] = year(1650).deviate(20)
		
	data.lGenericPlagueDates[3] = year(1850).deviate(20)

	undoPlague = rand(8)
	if undoPlague <= 3:
		data.lGenericPlagueDates[undoPlague] = -1


@handler("cityAcquired")
def clearOrSpreadPlague(iOwner, iPlayer, city):
	if city.isHasRealBuilding(iPlague):
		if plague.isVulnerable(iPlayer) and not data.players[iOwner].bFirstContactPlague:
			plague.spreadPlague(iPlayer)
			plague.infectCitiesNear(iPlayer, city)
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
		if player(iPlayer).isAlive():
			if data.players[iPlayer].iPlagueCountdown > 0:
				data.players[iPlayer].iPlagueCountdown -= 1
				if data.players[iPlayer].iPlagueCountdown == 2:
					self.preStopPlague(iPlayer)
				elif data.players[iPlayer].iPlagueCountdown == 0:
					self.stopPlague(iPlayer)
			elif data.players[iPlayer].iPlagueCountdown < 0:
				data.players[iPlayer].iPlagueCountdown += 1


@handler("BeginGameTurn")
def startPlagues(iGameTurn):
	if data.bNoPlagues:
		return

	for iPlague, iPlagueDate in enumerate(data.lGenericPlagueDates):
		if iGameTurn == iPlagueDate:
			startPlague(iPlague)

		if iPlague >= 1:
			#retry if the epidemic is dead too quickly
			if iGameTurn == iPlagueDate + 4:
				iInfectedCounter = 0
				for iPlayer in players.all().barbarian():
					if data.players[iPlayer].iPlagueCountdown > 0:
						iInfectedCounter += 1
				if iInfectedCounter == 1:
					startPlague(iPlague)

		if iPlague == 2 or iPlague == 3:
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


def calculateTotalPlagueHealth(iPlayer):
	iHealth = calculateHealth(iPlayer) / 2
	
	if player(iPlayer).calculateTotalCityHealthiness() > 0:
		iHealth += rand(40)
		
		if iPlagueCounter == 2: # medieval Black Death
			if civ(iPlayer) in dCivGroups[iCivGroupEurope]:
				iHealth -= 5
	
	return iHealth


def startPlague(iPlagueCounter):
	iPlayer = players.major().alive().where(isVulnerable).lowest(calculateTotalPlagueHealth)
			
	if calculateTotalPlagueHealth(iPlayer) <= 200:
		city = cities.owner(iPlayer).random()
		if city:
			spreadPlague(iPlayer)
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
	
	if civ(iPlayer) in lBioNewWorld and not data.lFirstContactConquerors[lBioNewWorld.index(civ(iPlayer))]: return False
		
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
	
	for plot in plots.surrounding(city, radius=2):
		if plot.getUpgradeProgress() > 0:
			plot.setUpgradeProgress(0)
			iImprovement = plot.getImprovementType()
			if iImprovement == iTown:
				plot.setImprovementType(iVillage)
			
			if at(plot, city):
				killUnitsByPlague(city, pPlot, 0, 100, 0)


def killUnitsByPlague(city, pPlot, baseValue, iDamage, iPreserveDefenders):
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
	for unit in units.at(pPlot):
		if player(unit).isHuman():
			if iPreserveHumanDefenders > 0:
				if isDefenderUnit(unit):
					iPreserveHumanDefenders -= 1
					if pPlot.getNumUnits() <= iPreserveDefenders:
						iMaxDamage = 50
						if unit.workRate(100) > 0 and not unit.canFight(): iMaxDamage = 100
						unit.setDamage(min(iMaxDamage, unit.getDamage() + iDamage - 20), iBarbarianPlayer)
					continue

		elif iPreserveDefenders > 0:
			if isDefenderUnit(unit):
				iPreserveDefenders -= 1
				if pPlot.getNumUnits() <= iPreserveDefenders and team(unit).isAtWar(active()):
					iMaxDamage = 50
					if unit.workRate(100) > 0 and not unit.canFight(): iMaxDamage = 100
					unit.setDamage(min(iMaxDamage, unit.getDamage() + iDamage - 20), iBarbarianPlayer)
				continue

		if isMortalUnit(unit):
			iThreshold = baseValue + 5 * city.healthRate(False, 0)
			
			if teamOwner.isAtWar(active()) and not is_minor(iOwner):
				if unit.getOwner() == iOwner:
					iDamage *= 3
					iDamage /= 4
				
			if data.players[city.getOwner()].bFirstContactPlague:
				if civ(unit) not in lNewOldWorld and not is_minor(unit):
					iDamage /= 2
					
			if rand(100) > iThreshold:
				iMaxDamage = 50
				if unit.workRate(100) > 0 and not unit.canFight(): iMaxDamage = 100
				unit.setDamage(min(iMaxDamage, unit.getDamage() + iDamage - unit.getExperience()/10 - unit.baseCombatStr()/2), iBarbarianPlayer)
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
	
	for iLoopPlayer in players.major().where(self.isVulnerable):
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
			plotCity = city(plot)
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
			self.killUnitsByPlague(city, plot, 0, 42, 2)
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
			

class Plague:

######################################
### Main methods (Event-Triggered) ###
######################################
			
	


	def checkTurn(self, iGameTurn):
		if data.bNoPlagues:
			return

	def checkPlayerTurn(self, iGameTurn, iPlayer):
		if data.bNoPlagues:
			return

		if iPlayer in players.all():
			if data.players[iPlayer].iPlagueCountdown > 0:
				self.processPlague(iPlayer)


	def preStopPlague(self, iPlayer):
		iModifier = 0
		for city in cities.owner(iPlayer).where(lambda city: city.hasBuilding(iPlague)):
			if rand(100) > 30 - 5 * city.healthRate(False, 0) + iModifier:
				city.setHasRealBuilding(iPlague, False)
				iModifier += 5


	def stopPlague(self, iPlayer):
		data.players[iPlayer].iPlagueCountdown = -turns(iImmunity)
		if data.players[iPlayer].bFirstContactPlague:
			data.players[iPlayer].iPlagueCountdown = -turns(iImmunity-30)
		data.players[iPlayer].bFirstContactPlague = False
		for city in cities.owner(iPlayer):
			city.setHasRealBuilding(iPlague, False)







# make a singleton until we can destroy the class completely
plague = Plague()