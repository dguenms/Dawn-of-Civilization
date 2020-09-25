# Rhye's and Fall of Civilization - Historical Victory Goals

from CvPythonExtensions import *
from StoredData import data
from Consts import *
from RFCUtils import *
import heapq
import CityNameManager as cnm
from Civics import *
import BugCore
from Events import handler, events

from Locations import *
from Core import *

AdvisorOpt = BugCore.game.Advisors
AlertsOpt = BugCore.game.MoreCiv4lerts


### CONSTANTS ###

# general constants
lWonders = [i for i in range(iBeginWonders, iNumBuildings)]
lGreatPeople = [iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy]

# second Portuguese goal: acquire 12 colonial resources by 1650 AD
lColonialResources = [iBanana, iSpices, iSugar, iCoffee, iTea, iTobacco]

# third Thai goal: allow no foreign powers in South Asia in 1900 AD
lSouthAsianCivs = [iIndia, iTamils, iIndonesia, iKhmer, iMughals, iThailand]


### GOALS ###

POSSIBLE, SUCCESS, FAILURE = range(3)

	
def cityAverage(function):
	def average_func(player):
		if player.getNumCities() == 0:
			return 0
		return function(player) / player.getNumCities()
	return average_func
	
def cityValue(tile, function):
	def value_func(player):
		_city = city(tile)
		if not _city: return 0
		
		return function(city)
	return value_func


class GenericGoal(object):

	def __init__(self):
		self.state = POSSIBLE
		
		self.description = "NO DESCRIPTION"
		
		self.progress = None
		self.notifier = None
		
		self.handlers = []
	
	def setup(self, iPlayer, notifier):
		self.iPlayer = iPlayer
		self.iCiv = civ(iPlayer)
		self.player = player(iPlayer)
		
		self.notifier = notifier
		
		for event, handler in self.handlers:
			events.addEventHandler(event, handler)
	
	def addEventHandler(self, event, handler):
		self.handlers.append((event, handler))
		
	def possible(self):
		return self.state == POSSIBLE
		
	def win(self):
		self.setState(SUCCESS)
		
	def lose(self):
		self.setState(FAILURE)
		
	def expire(self):
		if self.possible():
			self.lose()
		
	def progress(self):
		pass
		
	def check(self):
		if self.possible():
			self.progress()
			
			if self.condition():
				self.win()
			
	def finalCheck(self):
		self.check()
		self.expire()
		
	def condition(self):
		raise NotImplementedError()
		
	def notify(self, state):
		if self.notifier:
			self.notifier(state)
		
	def checkFor(self, event):
		def check_handler(*args, **kwargs):
			self.check()
			
		self.addEventHandler(event, check_handler)
		return self
			
	def turnly(self):
		return self.checkFor("BeginGameTurn")
		
	def by(self, iYear):
		def expire_handler(iGameTurn):
			if iGameTurn == year(iYear):
				self.expire()
				
		self.addEventHandler("BeginGameTurn", expire_handler)
		return self
		
	def at(self, iYear):
		def check_handler(iGameTurn):
			if iGameTurn == year(iGameTurn):
				self.finalCheck()
		
		self.addEventHandler("BeginGameTurn", check_handler)
		return self
		
	def forBuilding(self, iBuilding):
		def check_handler(city, iBuiltBuilding):
			if iBuiltBuilding == iBuilding:
				if isWonder(iBuilding):
					self.finalCheck()
				else:
					self.check()
		
		self.addEventHandler("buildingBuilt", check_handler)
		return self
		
	def acquiredCity(self):
		return self.checkFor("cityAcquired")
		
	def builtCity(self):
		return self.checkFor("cityBuilt")
		
	def city(self):
		return self.acquiredCity().builtCity()
	
	def getStateChar(self):
		symbol = FontSymbols.FAILURE_CHAR
		if self.condition():
			symbol = FontSymbols.SUCCESS_CHAR
		
		return u"%c" % game.getSymbolID(symbol)
		
	def getDescription(self):
		return self.description
		
	def getProgress(self):
		return self.getStateChar() + self.progress
		
	def setNotifier(self, notifier):
		self.notifier = notifier
		
	def setState(self, state):
		if self.state != state:
			self.state = state
			self.notify(state)
		

class CombinedGoal(GenericGoal):

	def __init__(self, *subgoals):
		super(CombinedGoal, self).__init__()
		
		self.subgoals = subgoals
		
	def setup(self, iPlayer, notifier):
		for goal in self.subgoals:
			goal.setup(iPlayer, self.handle)
			
		self.notifier = notifier
			
	def handle(self, state):
		if state != POSSIBLE:
			return
	
		if state == FAILURE:
			self.lose()
		elif state == SUCCESS and self.condition():
			self.win()
			
	def check(self):
		for goal in self.subgoals:
			goal.check()
			
	def finalCheck(self):
		for goal in self.subgoals:
			goal.finalCheck()
			
	def expire(self):
		for goal in self.subgoals:
			goal.expire()
			
	def condition(self):
		return all(goal.state == SUCCESS for goal in self.subgoals)
			
	def getProgress(self):
		'\n'.join(goal.getProgress() for goal in self.subgoals)
		
		
class PartialGoal(CombinedGoal):

	def __init__(self, iNumRequired, *subgoals):
		super(PartialGoal, self).__init__(*subgoals)
		
		self.iNumRequired = iNumRequired
		
	def condition(self):
		return count(self.subgoals, lambda subgoal: subgoal.state == SUCCESS) >= self.iNumRequired
		
		
class AnyGoal(CombinedGoal):

	def __init__(self, *subgoals):
		super(AnyGoal, self).__init__(*subgoals)
		
	def condition(self):
		return any(subgoal for subgoal in self.subgoals if subgoal.state == SUCCESS)


class DifferentCities(CombinedGoal):

	def __init__(self, *subgoals):
		super(DifferentCities, self).__init__(*subgoals)
	
	def handle(self, state):
		super(DifferentCities, self).handle(state)
		
		if self.state != POSSIBLE:
			return
		
		excluded = [subgoal.location for subgoal in self.subgoals if subgoal.state == SUCCESS]
		
		for subgoal in self.subgoals:
			if subgoal.state == POSSIBLE:
				subgoal.excluded = excluded[:]


class RequiredCountGoal(GenericGoal):

	def __init__(self, value_function, iRequiredValue):
		super(RequiredCountGoal, self).__init__()
		
		self.value_function = value_function
		self.iRequiredValue = iRequiredValue
		
		self.turnly()
		
	def value(self):
		return self.value_function(self.player)
			
	def required(self):
		return self.iRequiredValue
		
	def condition(self):
		return self.value() >= self.required()


def BuildingCount(iBuilding, iRequiredBuildings):
	return RequiredCountGoal(lambda player: player.countNumBuildings(iBuilding), iRequiredBuildings).forBuilding(iBuilding)
	
def BuildingCounts(*buildings):
	return CombinedGoal(BuildingCount(iBuilding, iNumBuildings) for iBuilding, iNumBuildings in buildings)
	
def BuildingCountSum(iRequiredBuildings, buildings):
	return RequiredCountGoal(lambda player: sum(player.countNumBuildings(iBuilding) for iBuilding in buildings), iRequiredBuildings)
	
def ReligiousBuildingCount(iReligiousBuilding, iRequiredBuildings):
	return BuildingCountSum(iRequiredBuildings, [iReligiousBuilding + 4*iReligion for iReligion in range(iNumReligions)])

def WonderCount(iRequiredWonders):
	return BuildingCountSum(iRequiredWonders, [iBuilding for iBuilding in range(iNumBuildings) if iBuilding >= iFirstWonder])

def TotalPopulation(iRequiredPopulation):
	return RequiredCountGoal(CyPlayer.getTotalPopulation, iRequiredPopulation)
	
def AcquiredResourceCount(iResource, iRequiredResources):
	return RequiredCountGoal(lambda p: p.getNumAvailableBonuses(iResource), iRequiredResources)

def AcquiredResourcesCount(lResources, iRequiredResources):
	return RequiredCountGoal(lambda p: sum(p.getNumAvailableBonuses(iResource) for iResource in lResources), iRequiredResources)

def ControlledResourcesCount(lResources, iRequiredResources):
	def playerResourceCount(iPlayer, iResource):
		return player(iPlayer).getNumAvailableBonuses(iResource) - player(iPlayer).getBonusImport(iResource)
	
	def playerResourcesCount(iPlayer):
		return sum(playerResourceCount(iPlayer, iResource) for iResource in lResources)
	
	def playerVassalResourcesCount(iPlayer):
		return players.major().alive().where(lambda p: p == iPlayer or team(p).isVassal(team(iPlayer).getID())).sum(playerResourcesCount)
	
	return RequiredCountGoal(playerVassalResourcesCount, iRequiredResources)
	
def ControlledResourceCount(iResource, iRequiredResources):
	return ControlledResourcesCount([iResource], iRequiredResources)

def SpecialistCount(iSpecialist, iRequiredSpecialists):
	return RequiredCountGoal(lambda player: cities.owner(player).sum(lambda city: city.getFreeSpecialistCount(iSpecialist)), iRequiredSpecialists)

def WonderSpecialistCount(iWonder, iSpecialist, iRequiredSpecialists):
	def wonder_specialist_count(player):
		wonderCity = getBuildingCity(iWonder, False)
		if not wonderCity or wonderCity.getOwner() != player.getID():
			return 0
		return wonderCity.getFreeSpecialistCount(iSpecialist)
	
	return RequiredCountGoal(wonder_specialist_count, iRequiredSpecialists)

def HappinessResourceCount(iRequiredResources):
	return RequiredCountGoal(lambda player: infos.bonuses().where(lambda iBonus: info.bonus(iBonus).getHappiness() > 0 and player.getNumAvailableBonuses(iBonus) > 0).count(), iRequiredResources)
	
def AverageCityPopulation(iRequiredPopulation):
	return RequiredCountGoal(cityAverage(CyPlayer.getTotalPopulation), iRequiredPopulation)

def UnitsCount(lUnits, iRequiredUnits):
	return RequiredCountGoal(lambda player: sum(player.getUnitClassCount(infos.unit(iUnit).getUnitClassType()) for iUnit in lUnits), iRequiredUnits)

def UnitCount(iUnit, iRequiredUnits):
	return UnitsCount([iUnit], iRequiredUnits)
	
def CorporationCount(iCorporation, iRequiredCorporations):
	return RequiredCountGoal(lambda player: player.countCorporations(iCorporation), iRequiredCorporations)

def OpenBordersCount(iRequiredOpenBorders, lCivs = []):
	def open_borders_count(player):
		contacts = players.major().alive()
		if lCivs:
			contacts = contacts.civs(*lCivs)
			
		return contacts.where(lambda p: team(player).isOpenBorders(p)).count()
	
	return RequiredCountGoal(open_borders_count, iRequiredOpenBorders)

def CapitalWonderCount(iRequiredWonders):
	def capital_wonder_count(player):
		if not capital(player):
			return 0
		return len([iWonder for iWonder in lWonders if capital(iPlayer).isHasBuildingEffect(iWonder)])
	
	return RequiredCountGoal(capital_wonder_count, iRequiredWonders)

def ImprovementCount(iImprovement, iRequiredImprovements):
	return RequiredCountGoal(lambda p: p.getImprovementCount(iImprovement), iRequiredImprovements)

def ImprovementCounts(*improvements):
	return CombinedGoal(ImprovementCount(iImprovement, iRequiredImprovements) for iImprovement, iRequiredImprovements in improvements)


class SunkShips(RequiredCountGoal):

	def __init__(self, iRequiredShips):

		super(SunkShips, self).__init__(lambda p: self.getSunkShips(), iRequiredShips)
		
		self.iSunkShips = 0
		
		self.onCombatResult()
		
	def getSunkShips(self):
		return self.iSunkShips
	
	def onCombatResult(self):
		def check_handler(pWinningUnit, pLosingUnit):
			if pWinningUnit.getOwner() == self.iPlayer and pLosingUnit.getDomainType() == DomainTypes.DOMAIN_SEA:
				self.iSunkShips += 1
				
				self.check()


class AcquiredCities(RequiredCountGoal):

	def __init__(self, iRequiredCities):
		super(AcquiredCities, self).__init__(lambda p: self.getAcquiredCities(), iRequiredCities)
	
		self.iAcquiredCities = 0
		
	def getAcquiredCities(self):
		return self.iAcquiredCities
		
	def onCityAcquired(self):
		def check_handler(iOwner, iPlayer, city, bConquest):
			if self.iPlayer == iPlayer:
				self.iAcquiredCities += 1
		
		self.addEventHandler("cityAcquired", check_handler)
		return self
	
	def onCityBuilt(self):
		def check_handler(city):
			if city.getOwner() == self.iPlayer:
				self.iAcquiredCities += 1
				
		self.addEventHandler("cityBuilt", check_handler)
		return self
		
		
class Vassals(RequiredCountGoal):

	def __init__(self, iRequiredVassals):
		super(Vassals, self).__init__(lambda p: self.countVassals(), iRequiredVassals)
	
		self.lCivs = []
		self.iStateReligion = None
		
	def countVassals(self):
		vassals = player.vassals(self.iPlayer)
		
		if self.lCivs:
			vassals = vassals.where(lambda p: civ(p) in self.lCivs)
			
		if self.iStateReligion is not None:
			vassals = vassals.where(lambda p: p.getStateReligion() == self.iStateReligion)
			
		return vassals.count()
		
	def civs(self, lCivs):
		self.lCivs = lCivs
		return self
		
	def stateReligion(self, iStateReligion):
		self.iStateReligion = iStateReligion
		return self
		
		
class AttitudeCount(RequiredCountGoal):

	def __init__(self, iAttitude, iRequiredRelations):
		super(AttitudeCount, self).__init__(lambda p: self.countRelations(), iRequiredRelations)
		
		self.lCivs = []
		self.bCommunist = False
	
	def countRelations(self):
		relations = players.major().where(lambda p: self.player.canContact(p) and player(p).AI_getAttitude(self.iPlayer) >= self.iAttitude and not team(p).isAVassal())
		
		if self.lCivs:
			relations = relations.where(lambda p: civ(p) in self.lCivs)
		
		if self.bCommunist:
			relations = relations.where(lambda p: isCommunist(p))
		
		return relations.count()
		
	def civs(self, lCivs):
		self.lCivs = lCivs
		return civs
	
	def communist(self):
		self.bCommunist = True
		return self


class PillageCount(RequiredCountGoal):

	def __init__(self, iRequiredPillages):
		super(PillageCount, self).__init__(lambda p: self.getPillageCount(), iRequiredPillages)
		
		self.iPillageCount = 0
		
		self.onUnitPillage()
	
	def getPillageCount(self):
		return self.iPillageCount
		
	def onUnitPillage(self):
		def check_handler(unit, iImprovement, iRoute, iPlayer, iGold):
			if self.iPlayer == iPlayer:
				self.iPillageCount += 1
				self.check()
		
		self.addEventHandler("unitPillage", check_handler)
		return self
		

class RazeCount(RequiredCountGoal):

	def __init__(self, iRequiredRazes):
		super(RazeCount, self).__init__(lambda p: self.getRazeCount(), iRequiredRazes)
		
		self.iRazeCount = 0
		
		self.onCityRazed()
	
	def getRazeCount(self):
		return self.iRazeCount
	
	def onCityRazed(self):
		def check_handler(city, iPlayer):
			if self.iPlayer == iPlayer:
				self.iRazeCount += 1
				self.check()
		
		self.addEventHandler("cityRazed", check_handler)
		return self


class EnslaveCount(RequiredCountGoal):

	def __init__(self, iRequiredEnslaves):
		super(EnslaveCount, self).__init__(lambda p: self.getEnslaveCount(), iRequiredEnslaves)
		
		self.iEnslaveCount = 0
		
		self.lExceptions = []
		
		self.onEnslave()
		
	def exceptions(self, lExceptions):
		self.lExceptions = lExceptions
		return self
	
	def getEnslaveCount(self):
		return self.iEnslaveCount
	
	def onEnslave(self):
		def check_handler(iPlayer, unit):
			if self.iPlayer == iPlayer and not is_minor(unit):
				if not self.lExceptions or civ(unit) not in self.lExceptions:
					self.iEnslaveCount += 1
					self.check()
		
		self.addEventHandler("enslave", check_handler)
		return self


class MoreCultureThan(RequiredCountGoal):

	def __init__(self, lCivs):
		super(MoreCultureThan, self).__init__(CyPlayer.countTotalCulture, None)
	
		self.lCivs = lCivs
	
	def required(self):
		return players.civs(self.lCivs).alive().sum(CyPlayer.countTotalCulture)


class ConquerFrom(RequiredCountGoal):

	def __init__(self, lCivs, iRequiredCities):
		super(ConquerFrom, self).__init__(lambda p: self.getConquerCount(), iRequiredCities)
		
		self.lCivs = lCivs
		self.lExcludedRegions = []
		
		self.iConquerCount = 0
		
		self.onCityAcquired()
	
	def getConquerCount(self):
		return self.iConquerCount
		
	def notin(self, lRegions):
		self.lExcludedRegions = lRegions
		return self
		
	def onCityAcquired(self):
		def check_handler(iOwner, iPlayer, city, bConquest):
			if bConquest and self.iPlayer == iPlayer and civ(iOwner) in self.lCivs and city.getRegionID() not in self.lExcludedRegions:
				self.iConquerCount += 1
				self.check()
		
		self.addEventHandler("cityAcquired", check_handler)
		return self


class StateReligionBuildingCount(RequiredCountGoal):

	def __init__(self, building, iRequiredBuildings):
		super(StateReligionBuildingCount, self).__init__(lambda p: self.getStateReligionBuildingCount(), iRequiredBuildings)
		
		self.building = building
	
	def getStateReligionBuildingCount(self):
		if self.player.getStateReligion() < 0:
			return 0
		return self.player.countNumBuildings(self.building(self.player.getStateReligion()))


class GreatGenerals(RequiredCountGoal):

	def __init__(self, iRequiredGenerals):
		super(GreatGenerals, self).__init__(lambda p: self.getGreatGeneralCount(), iRequiredGenerals)
		
		self.iGreatGeneralCount = 0
		
		self.onGreatPersonBorn()
		
	def getGreatGeneralCount(self):
		return self.iGreatGeneralCount
	
	def onGreatPersonBorn(self):
		def check_handler(unit, iPlayer):
			if self.iPlayer == iPlayer and infos.unit(unit).getGreatPeoples(iSpecialistGreatGeneral):
				self.iGreatGeneralCount += 0
				self.check()
		
		self.addEventHandler("greatPersonBorn", check_handler)
		return self


class BrokeredPeaceCount(RequiredCountGoal):

	def __init__(self, iRequiredPeaceAgreements):
		super(BrokeredPeaceCount, self).__init__(lambda p: self.getBrokeredPeaceCount(), iRequiredPeaceAgreements)
		
		self.iBrokeredPeaceCount = 0
		
		self.onPeaceBrokered()
		
	def getBrokeredPeaceCount(self):
		return self.iBrokeredPeaceCount
	
	def onPeaceBrokered(self):
		def check_handler(iBroker, iPlayer1, iPlayer2):
			if self.iPlayer == iBroker:
				self.iBrokeredPeaceCount += 1
				self.check()
		
		self.addEventHandler("peaceBrokered", check_handler)
		return self


class RequiredValueGoal(RequiredCountGoal):

	def __init__(self, value_function, iRequiredValue):
		super(RequiredValueGoal, self).__init__(value_function, iRequiredValue)
		
	def required(self):
		return scale(self.iRequiredValue)


def PlayerCulture(iRequiredCulture):
	return RequiredValueGoal(CyPlayer.countTotalCulture, iRequiredCulture)

def PlayerGold(iRequiredGold):
	return RequiredValueGoal(CyPlayer.getGold, iRequiredGold)

def AverageCityCulture(iRequiredCulture):
	return RequiredValueGoal(cityAverage(CyPlayer.countTotalCulture), iRequiredCulture)
	
def CityCulture(tile, iRequiredCulture):
	def cityCulture(player):
		if not city(tile):
			return 0
		return city(tile).getCulture(player.getID())
	
	return RequiredValueGoal(cityCulture, iRequiredCulture)
	

class TradeGold(RequiredValueGoal):

	def __init__(self, iRequiredGold):
		super(TradeGold, self).__init__(lambda p: self.getTradeGold(), iRequiredGold)
		
		self.iTradeGold = 0
		
		self.onPlayerGoldTrade()
		
	def getTradeGold(self):
		return self.iTradeGold / 100
		
	def onPlayerGoldTrade(self):
		def check_handler(iFrom, iTo, iGold):
			if self.iPlayer == iTo:
				self.iTradeGold += iGold * 100
				
		self.addEventHandler("playerGoldTrade", check_handler)
		return self
		
	def progress(self):
		# gold from city trade routes
		iTradeCommerce = 0
		for city in cities.owner(self.iPlayer):
			iTradeCommerce += city.getTradeYield(YieldTypes.YIELD_COMMERCE)
		self.iTradeGold += iTradeCommerce * self.player.getCommercePercent(CommerceTypes.COMMERCE_GOLD)
		
		# gold from per turn gold trade
		for iPlayer in players.major():
			self.iTradeGold += self.player.getGoldPerTurnByPlayer(iPlayer) * 100


class RaidGold(RequiredValueGoal):

	def __init__(self, iRequiredGold):
		super(RaidGold, self).__init__(lambda p: self.getRaidGold(), iRequiredGold)
		
		self.iRaidGold = 0
		
		self.onUnitPillage()
		self.onCityCaptureGold()
		
	def getRaidGold(self):
		return self.iRaidGold
		
	def onUnitPillage(self):
		def check_handler(unit, iImprovement, iRoute, iPlayer, iGold):
			if self.iPlayer == iPlayer:
				self.iRaidGold += iGold
				self.check()
				
		self.addEventHandler("unitPillage", check_handler)
		return self
				
	def onCityCaptureGold(self):
		def check_handler(city, iPlayer, iGold):
			if self.iPlayer == iPlayer:
				self.iRaidGold += iGold
				self.check()
		
		self.addEventHandler("cityCaptureGold", check_handler)
		return self


class PiracyGold(RequiredValueGoal):

	def __init__(self, iRequiredGold):
		super(PiracyGold, self).__init__(lambda p: self.getPiracyGold(), iRequiredGold)
		
		self.iPiracyGold = 0
		
		self.onUnitPillage()
		self.onBlockade()
	
	def getPiracyGold(self):
		return self.iPiracyGold
	
	def onUnitPillage(self):
		def check_handler(unit, iImprovement, iRoute, iPlayer, iGold):
			if self.iPlayer == iPlayer and infos.unit(unit).isHiddenNationality():
				self.iPiracyGold += iGold
				self.check()
		
		self.addEventHandler("unitPillage", check_handler)
		return self
	
	def onBlockade(self):
		def check_handler(iPlayer, iGold):
			if self.iPlayer == iPlayer:
				self.iPiracyGold += iGold
				self.check()
		
		self.addEventHandler("blockade", check_handler)
		return self


class SlaveTradeGold(RequiredValueGoal):

	def __init__(self, iRequiredGold):
		super(SlaveTradeGold, self).__init__(lambda p: self.getSlaveTradeGold(), iRequiredGold)
		
		self.iSlaveTradeGold = 0
		
		self.onPlayerSlaveTrade()
		
	def getSlaveTradeGold(self):
		return self.iSlaveTradeGold
		
	def onPlayerSlaveTrade(self):
		def check_handler(iPlayer, iGold):
			if self.iPlayer == iPlayer:
				self.iSlaveTradeGold += iGold
				self.check()
		
		self.addEventHandler("playerSlaveTrade", check_handler)
		return self


class ResourceTradeGold(RequiredValueGoal):

	def __init__(self, iRequiredGold):
		super(ResourceTradeGold, self).__init__(lambda p: self.getResourceTradeGold(), iRequiredGold)
		
		self.iResourceTradeGold = 0
		
		self.onTurn()
		
	def getResourceTradeGold(self):
		return self.iResourceTradeGold
	
	def onTurn(self):
		def check_handler(iGameTurn, iPlayer):
			if self.iPlayer == iPlayer:
				self.iResourceTradeGold += players.major().alive().sum(self.player.getGoldPerTurnByPlayer)
				self.check()
		
		self.addEventHandler("BeginPlayerTurn", check_handler)
		return self


class CityCultureLevel(RequiredValueGoal):

	def __init__(self, tile, iCultureLevel):
		super(CityCultureLevel, self).__init__(lambda p: self.cityCulture(), None)
	
		self.tile = tile
		self.iCultureLevel = iCultureLevel
	
	def cityCulture(self):
		if not city(self.tile):
			return 0
		return city(self.tile).getCulture(self.iPlayer)
	
	def required(self):
		return infos.culture(self.iCultureLevel).getSpeedThreshold(game.getGameSpeedType())


class CapitalCultureLevel(RequiredValueGoal):

	def __init__(self, iCultureLevel):
		super(CapitalCultureLevel, self).__init__(lambda p: self.capitalCulture(), None)
	
		self.excluded = []
	
		self.iCultureLevel = iCultureLevel
		self.location = None
		
	def capitalCulture(self):
		if not capital(self.iPlayer):
			return 0
		return capital(self.iPlayer).getCulture(self.iPlayer)
	
	def required(self):
		return infos.culture(self.iCultureLevel).getSpeedThreshold()
	
	def condition(self):
		return location(capital(self.iPlayer)) not in self.excluded and super(CapitalCultureLevel, self).condition()
	
	def setState(self, state):
		super(CapitalCultureLevel, self).setState(state)
		
		if state == SUCCESS:
			self.location = location(capital(self.iPlayer)) 
	
	def exclude(self, city):
		self.excluded.append(location(city))


class PercentGoal(GenericGoal):

	def __init__(self, value_function, iRequiredPercent):
		super(PercentGoal, self).__init__()
		
		self.value_function = value_function
		self.iRequiredPercent = 1.0 * iRequiredPercent
		
	def value(self):
		return 1.0 * self.value_function()
	
	def required(self):
		return self.iRequiredPercent
	
	def condition(self):
		return self.value() >= self.required()
		
		
def ReligionSpreadPercent(iReligion, iRequiredPercent):
	return PercentGoal(lambda: game.calculateReligionPercent(iReligion), iRequiredPercent)


class PercentOfTotalGoal(PercentGoal):

	def __init__(self, value_function, iRequiredPercent, total_function=None):
		super(PercentOfTotalGoal, self).__init__(value_function, iRequiredPercent)
		
		self.total_function = total_function
			
	def total(self):
		if self.total_function:
			return self.total_function()
		return players.alive().sum(lambda p: self.value_function(player(p)))
			
	def value(self):
		iTotal = self.total()
		if iTotal <= 0: 
			return 0.0
		
		return 100.0 * self.value_function(self.player) / iTotal
		
		
def PopulationPercent(iRequiredPercent):
	return PercentOfTotalGoal(CyPlayer.getTotalPopulation, iRequiredPercent, game.getTotalPopulation)
	
def LandPercent(iRequiredPercent):
	return PercentOfTotalGoal(CyPlayer.getTotalLand, iRequiredPercent, map.getLandPlots)
	
def ReligiousVotePercent(iRequiredPercent):
	return PercentOfTotalGoal(lambda p: p.getVotes(16, 1), iRequiredPercent)


class AlliedPercentOfTotal(PercentOfTotalGoal):

	def __init__(self, value_function, iRequiredPercent, total_function=None):
		return super(AlliedPercentOfTotal, self).__init__(value_function, iRequiredPercent, total_function)
	
	def allies(self):
		allies = players.of(self.iPlayer) + players.vassals(self.iPlayer) + players.defensivePacts(self.iPlayer) + players.vassals(self.iPlayer).defensivePacts()
		return allies.unique()
	
	def value(self):
		iTotal = self.total()
		if iTotal <= 0:
			return 0.0
		
		return 100.0 * self.allies().sum(self.value_function) / 100


def AlliedCommercePercent(iRequiredPercent):
	return AlliedPercentOfTotal(CyPlayer.calculateTotalCommerce, iRequiredPercent)

def AlliedPowerPercent(iRequiredPercent):
	return AlliedPercentOfTotal(CyPlayer.getPower, iRequiredPercent)


class ControlPercentInArea(PercentOfTotalGoal):

	def __init__(self, iRequiredPercent, plots):
		super(ControlPercentInArea, self).__init__(self.controlledArea, iRequiredPercent, self.totalArea)
		
		self.plots = plots
		self.bVassals = False
		self.bCoastalOnly = False
		
	def withVassals(self):
		self.bVassals = True
		return self
		
	def validPlayers(self):
		if self.bVassals:
			return players.vassals(self.iPlayer).including(self.iPlayer)
		return players.of(self.iPlayer)
		
	def controlledArea(self, player):
		return self.plots.where(lambda p: p.getOwner() in self.validPlayers()).count()
	
	def totalArea(self):
		return self.plots.count()


def ControlPercentInAreas(iRequiredPercent, *ps):
	return ControlPercentInArea(iRequiredPercent, sum(ps, plots.none()))


class Wonder(GenericGoal):

	def __init__(self, iWonder):
		super(Wonder, self).__init__()
		
		self.iWonder = iWonder
		
		self.wonderLocation = None
		self.iWonderBuilder = None
		
		def check_handler(city, iBuilding):
			if iBuilding == self.iWonder:
				self.wonderLocation = location(city)
				self.iWonderBuilder = city.getOwner()
				
				self.finalCheck()
			
		self.addEventHandler("buildingBuilt", check_handler)
			
	def condition(self):
		return city(self.wonderLocation).getOwner() == self.iPlayer and self.iWonderBuilder == self.iPlayer
		
		
def Wonders(*wonders):
	return CombinedGoal(Wonder(wonder) for wonder in wonders)


class Project(GenericGoal):

	def __init__(self, iProject):
		super(Project, self).__init__()
		
		self.iProject = iProject
		
		self.iProjectBuilder = None
		
		self.onProjectBuilt()
		
	def onProjectBuilt(self):
		def check_handler(iPlayer, iProject):
			if self.iProject == iProject:
				self.iProjectBuilder = iPlayer
				
				self.finalCheck()
		
		self.addEventHandler("projectBuilt", check_handler)
	
	def condition(self):
		return self.iProjectBuilder == self.iPlayer


def Projects(*projects):
	return CombinedGoal(Project(iProject) for iProject in projects)


class Discover(GenericGoal):

	def __init__(self, iTech):
		super(Discover, self).__init__()
		
		self.iTech = iTech
		
		self.iDiscoverer = None
		
		def check_handler(iTech, iTeam, iPlayer):
			if iTech == self.iTech:
				self.iDiscoverer = iPlayer
				
				self.discoverCheck()
		
		events.addEventHandler("techAcquired", check_handler)
		
	def discoverCheck(self):
		self.check()
	
	def condition(self):
		return self.iDiscoverer == self.iPlayer


class DiscoverFirst(Discover):

	def __init__(self, iTech):
		super(DiscoverFirst, self).__init__(iTech)
	
	def discoverCheck(self):
		self.finalCheck()


def DiscoverFirsts(*techs):
	return CombinedGoal(DiscoverFirst(tech) for tech in techs)


class EnterEra(GenericGoal):

	def __init__(self, iEra):
		super(EnterEra, self).__init__()
		
		self.iEra = iEra
		
		self.turnly()
		
	def condition(self):
		return self.player.getCurrentEra() >= self.iEra
	
	def before(self, iEra):
		def expire_handler(iTech, iTeam, iPlayer):
			if self.iPlayer != iPlayer and player(iPlayer).getCurrentEra() >= iEra:
				self.expire()
				
		self.addEventHandler("techAcquired", expire_handler)
		return self
	
	
class RequiredCityCount(GenericGoal):

	def __init__(self, tile, iRequiredCount, function):
		super(RequiredCityCount, self).__init__()
		
		self.tile = tile
		self.iRequiredCount = iRequiredCount
		self.function = function
		
	def value(self):
		if not city(self.tile):
			return 0
	
		return self.function(city(self.tile))
		
	def required(self):
		return self.iRequiredCount
		
	def condition(self):
		return city(self.tile) and city(self.tile).getOwner() == self.iPlayer and self.value() >= self.required()
		

def CitySpecialistCount(tile, iSpecialist, iRequiredSpecialists):
	return RequiredCityCount(tile, iRequiredSpecialists, lambda city: city.getFreeSpecialistCount(iSpecialist))

def CitySpecialistCounts(tile, lSpecialists, iRequiredSpecialists):
	return RequiredCityCount(tile, iRequiredSpecialists, lambda city: sum(city.getFreeSpecialistCount(iSpecialist) for iSpecialist in lSpecialists))


class BestCity(GenericGoal):

	def __init__(self, tile, metric):
		super(BestCity, self).__init__()
		
		self.tile = tile
		self.metric = metric
		
		self.turnly()
			
	def best(self):
		return cities.all().maximum(lambda city: (self.metric(city), at(city, self.tile)))
			
	def condition(self):
		return at(self.best(), self.tile) and self.best().getOwner() == self.iPlayer
		
		
def MostCultureCity(tile):
	return BestCity(tile, lambda city: city.getCulture(city.getOwner()))

def MostPopulationCity(tile):
	return BestCity(tile, CyCity.getPopulation)


class TradeConnection(GenericGoal):

	def __init__(self):
		super(TradeConnection, self).__init__()
		
		self.turnly()
	
	def condition():
		return players.major().without(self.iPlayer).any(lambda p: self.player.canContact(p) and self.player.canTradeNetworkWith(p))


class GoldenAges(GenericGoal):

	def __init__(self, iNumGoldenAges):
		super(GoldenAges, self).__init__()
		
		self.iNumGoldenAges = iNumGoldenAges
		
		self.iGoldenAgeTurns = 0
		
		self.turnly()
		
	def progress():
		if self.player.isGoldenAge() and not self.player.isAnarchy():
			self.iGoldenAgeTurns += 1
	
	def condition(self):
		return self.iGoldenAgeTurns >= turns(8 * self.iNumGoldenAges)


class Control(GenericGoal):

	def __init__(self, plots):
		super(Control, self).__init__()
		
		self.plots = plots
		
		self.city()
		
	def isControlled(self, city):
		return city.getOwner() == self.iPlayer
	
	def condition(self):
		return self.plots.cities().all(self.isControlled)


def Controls(*plotsList):
	return CombinedGoal(Control(p) for p in plotsList)

def ControlCivs(*civs):
	return CombinedGoal(Control(plots.normal(iCiv)) for iCiv in civs)
	
	
class Settle(GenericGoal):

	def __init__(self, plots):
		super(Settle, self).__init__()
		
		self.plots = plots
		
	def onCityBuilt(self):
		def check_handler(city):
			if city.getOwner() == self.iPlayer:
				self.win()
			else:
				self.lose()
		
	def check(self):
		self.finalCheck()

	
def SettledAll(*plotsList):
	return CombinedGoal(Settle(p) for p in plotsList)

def SettledSome(iNumRequired, *plotsList):
	return PartialGoal(iNumRequired, *tuple(Settle(p) for p in plotsList))
	
	
class ControlOrVassalize(Control):

	def __init__(self, plots):
		super(ControlOrVassalize, self).__init__(plots)
		
	def isControlled(self, city):
		return super(ControlOrVassalize, self).isControlled(city) or team(city.getTeam()).isVassal(team(self.iPlayer).getID())
		

def ControlOrVassalizes(*plotsList):
	return CombinedGoal(ControlOrVassalize(p) for p in plotsList)


class CitiesInArea(GenericGoal):

	def __init__(self, plots, iRequiredCities):
		super(CitiesInArea, self).__init__()
		
		self.plots = plots
		self.iRequiredCities = iRequiredCities
		
		self.city()
		
	def value(self):
		return self.plots.cities().owner(self.iPlayer).count()
		
	def required(self):
		return self.iRequiredCities
		
	def condition(self):
		return self.value() >= self.required()
		

def CitiesInAreas(*areasWithCities):
	return CombinedGoal(CitiesInArea(plots, iRequiredCities) for plots, iRequiredCities in areasWithCities)
	
def CitiesInAreasSum(iRequiredCities, *areas):
	return CitiesInArea(sum(areas, plots.none()), iRequiredCities)


class ConqueredCitiesInArea(CitiesInArea):

	def __init__(self, plots, iRequiredCities):
		super(ConqueredCitiesInArea, self).__init__(plots, iRequiredCities)
		
	def value(self):
		return self.plots.cities().owner(self.iPlayer).where(lambda city: city.getOriginalOwner() != self.iPlayer).count()
		
		
class SettledCitiesInArea(CitiesInArea):

	def __init__(self, plots, iRequiredCities):
		super(SettledCitiesInArea, self).__init__(plots, iRequiredCities)
	
	def value(self):
		return self.plots.cities().owner(self.iPlayer).where(lambda city: city.getOriginalOwner() == self.iPlayer).count()


class CityBuilding(GenericGoal):

	def __init__(self, tile, iBuilding):
		super(CityBuilding, self).__init__()
		
		self.tile = tile
		self.iBuilding = iBuilding
		
		self.forBuilding(iBuilding)
	
	def condition(self):
		return city(self.tile) and city(self.tile).isHasRealBuilding(iBuilding)


def CityBuildings(tile, lBuildings):
	return CombinedGoal(CityBuilding(tile, iBuilding) for iBuilding in lBuildings)


class FirstContact(GenericGoal):

	def __init__(self, contactCivs, *ps):
		super(FirstContact, self).__init__()
		
		self.contactCivs = contactCivs
		self.plots = sum(ps, plots.none()).land()
		
		self.onFirstContact()
		
	def onFirstContact(self):
		def check_handler(iPlayer, iHasMetPlayer):
			if iPlayer == self.iPlayer and civ(iHasMetPlayer) in self.contactCivs:
				self.finalCheck()
		
		self.addEventHandler("firstContact", check_handler)
		return self
	
	def condition(self):
		contacts = players.civs(*self.contactCivs).where(lambda p: team(self.iPlayer).canContact(p))
		return contacts.none(lambda p: self.plots.where_surrounding(lambda plot: plot.isRevealed(p, False), radius=2).any())
		
		
def NewWorldFirstContact():
	return FirstContact(dCivGroups[iCivGroupEurope], plots.rectangle(tSouthAmerica), plots.rectangle(tNorthAfrica))


class ConvertAfterFounding(GenericGoal):

	def __init__(self, iReligion, iNumTurns):
		super(ConvertAfterFounding, self).__init__()
		
		self.iReligion = iReligion
		self.iNumTurns = iNumTurns
		
		self.turnly()
		
	def check(self):
		super(ConvertAfterFounding, self).check()
		
		if game.isReligionFounded(self.iReligion) and turn() > game.getReligionGameTurnFounded(self.iReligion) + turns(self.iNumTurns):
			self.expire()
			
	def condition(self):
		return self.player.getStateReligion() == self.iReligion
		
		
class MoreReligionInArea(GenericGoal):

	def __init__(self, iOurReligion, iOtherReligion, *ps):
		super(MoreReligionInArea, self).__init__()
		
		self.iOurReligion = iOurReligion
		self.iOtherReligion = iOtherReligion
		self.plots = sum(ps, plots.none())
		
		self.turnly()
		
	def value(self):
		return self.plots.cities().religion(self.iOurReligion).count()
		
	def required(self):
		return self.plots.cities().religion(self.iOtherReligion).count()
		
	def condition(self):
		return self.value() > self.required()
		

class NoCitiesLost(GenericGoal):

	def __init__(self):
		super(NoCitiesLost, self).__init__()
		
		self.onCityAcquired()
		
		self.win()
		
	def onCityAcquired(self):
		def check_handler(iOwner, iPlayer, city, bConquest):
			if self.iPlayer == iOwner:
				self.lose()
		
		self.addEventHandler("cityAcquired", check_handler)
		return self


class EraDiscoverFirst(GenericGoal):

	def __init__(self, iEra, iRequiredDiscoveries):
		super(EraDiscoverFirst, self).__init__()
		
		self.iNumEraTechs = 21
		
		self.iEra = iEra
		self.iRequiredDiscoveries = iRequiredDiscoveries
		
		self.iOurDiscoveries = 0
		self.iOtherDiscoveries = 0
		
		self.onTechAcquired()
		
	def onTechAcquired(self):
		def check_handler(iTech, iTeam, iPlayer):
			if infos.tech(iTech).getEra() == self.iEra:
				if self.iPlayer == iPlayer:
					self.iOurDiscoveries = 0
				else:
					self.iOtherDiscoveries = 0
					
			if self.iOtherDiscoveries > self.iNumEraTechs - self.iRequiredDiscoveries:
				self.expire()
				
			self.check()
			
		self.addEventHandler("techAcquired", check_handler)
		return self
			
	def condition(self):
		return self.iOurDiscoveries >= self.iRequiredDiscoveries


def EraDiscoverFirsts(*eraDiscoverFirsts):
	return CombinedGoal(EraDiscoverFirst(iEra, iRequiredDiscoveries) for iEra, iRequiredDiscoveries in eraDiscoverFirsts)


class FirstCity(GenericGoal):

	def __init__(self, plots, exceptCivs):
		super(FirstCity, self).__init__()
		
		self.plots = plots
		self.exceptCivs = exceptCivs
		
		self.onCityBuilt()
		
	def onCityBuilt(self):
		def check_handler(city):
			if city in self.plots:
				if city.getOwner() == self.iPlayer:
					self.win()
				elif civ(city) not in self.exceptCivs:
					self.lose()
		
		self.addEventHandler("cityBuilt", check_handler)
		return self


def FirstNewWorld():
	return FirstCity(plots.regions(*lAmerica), dCivGroups[iCivGroupAmerica])


class BestPlayer(GenericGoal):

	def __init__(self, metric):
		super(BestPlayer, self).__init__()
		
		self.metric = metric
		
	def getBestPlayer(self):
		return players.major().alive().maximum(lambda p: (self.metric(p), int(p == self.iPlayer)))
		
	def condition(self):
		return self.getBestPlayer() == self.iPlayer


def MostAdvanced():
	return BestPlayer(lambda p: infos.techs().where(lambda iTech: team(p).isHasTech(iTech)).sum(lambda iTech: infos.tech(iTech).getResearchCost()))

def LargestPopulation():
	return BestPlayer(lambda p: player(p).getRealPopulation())


class NoStateReligionInArea(GenericGoal):

	def __init__(self, iStateReligion, plots):
		super(NoStateReligionInArea, self).__init__()
		
		self.iStateReligion = iStateReligion
		self.plots = plots
	
	def condition(self):
		return self.plots.cities().none(lambda city: player(city).getStateReligion() == self.iStateReligion)
		
		
def NoStateReligionInAreas(iStateReligion, *ps):
	return NoStateReligionInArea(iStateReligion, sum(ps, plots.none()))


class RouteConnection(GenericGoal):

	def __init__(self, starts, targets, lRoutes):
		super(RouteConnection, self).__init__()
		
		if isinstance(starts, CyPlot):
			starts = plots.of([starts])
		
		self.starts = starts
		self.targets = targets
		self.lRoutes = lRoutes
		
		self.validOwners = set()
		
		self.turnly()
		
	def setup(self, iPlayer, notifier):
		super(RouteConnection, self).__init__(iPlayer, notifier)
		
		self.validOwners.add(iPlayer)
		
	def routeTech(self, iRoute):
		iBuild = infos.builds().where(lambda iBuild: info.build(iBuild).getRoute() == iRoute).first()
		return infos.build(iBuild).getTechPrereq()
		
	def connecting(self, plot):
		return plot.getOwner() in self.validOwners and (plot.isCity() or plot.getRouteType() in self.lRoutes)
		
	def connected(self, start):
		if not self.connecting(start):
			return False
			
		if start in self.targets:
			return True
			
		targets = targets.where(self.connecting)
		
		if not targets:
			return False
			
		nodes = [(targets.closest_distance(start), start)]
		heapq.heapify(nodes)
		
		visited = set()
		
		while nodes:
			heuristic, node = heapq.heappop(nodes)
			visited.add((heuristic, node))
			
			for plot in plots.surrounding(node).where(self.connecting):
				if plot in targets:
					return True
				
				tuple = (targets.closest_distance(plot), plot)
				if not tuple in visited and not tuple in nodes:
					heapq.heappush(nodes, tuple)
		
		return False
	
	def condition(self):
		if none(team(self.iPlayer).isHasTech(self.routeTech(iRoute)) for iRoute in self.lRoutes):
			return False
			
		for start in self.starts.cities():
			if self.connected(start):
				return True
		
		return False
		
	def withStartOwners(self):
		self.validOwners.update(self.starts.cities().owners().entities())
		return self
			

class Communist(GenericGoal):

	def __init__(self):
		super(Communist, self).__init__()
	
	def condition(self):
		return isCommunist(self.iPlayer)


class HolyCityTradeMission(GenericGoal):

	def __init__(self):
		super(HolyCityTradeMission, self).__init__()
	
	def onTradeMission(self):
		def check_handler(iUnit, iPlayer, iX, iY, iGold):
			if self.iPlayer == iPlayer:
				iStateReligion = self.player.getStateReligion()
				if iStateReligion != -1:
					if at(game.getHolyCity(iStateReligion), (iX, iY)):
						self.win()
		
		self.addEventHandler("tradeMission", check_handler)
		return self
		
		
class MatchingCities(GenericGoal):

	def __init__(self, value_func, iRequiredValue, iRequiredCities, sort_func=None):
		super(MatchingCities, self).__init__()
		
		self.value_func = value_func
		self.iRequiredValue = iRequiredValue
		self.iRequiredCities = iRequiredCities
		
		if sort_func:
			self.sort_func = sort_func
		else:
			self.sort_func = value_func
		
	def required(self):
		return self.iRequiredValue
	
	def condition(self):
		return cities.owner(self.iPlayer).sort(sort_func).limit(self.iRequiredCities).all(lambda city: value_func(city) >= self.required())


def PopulationCities(iRequiredPopulation, iNumCities):
	return MatchingCities(CyCity.getPopulation, iRequiredPopulation, iNumCities)
	
def CultureCities(iRequiredCulture, iNumCities):
	return MatchingCities(lambda city: city.getCulture(city.getOwner()), iRequiredCulture, iNumCities)
	
def CultureCity(iRequiredCulture):
	return CultureCities(iRequiredCulture, 1)
	
def CultureLevelCities(iRequiredCultureLevel, iNumCities):
	return MatchingCities(CyCity.getCultureLevel, iRequiredCultureLevel, iNumCities, lambda city: city.getCulture(city.getOwner()))


class Route(GenericGoal):

	def __init__(self, plots, lRoutes):
		super(Route, self).__init__()
		
		self.plots = plots
		self.lRoutes = lRoutes
	
	def condition(self):
		return self.plots.all(lambda plot: plot.getOwner() == self.iPlayer and (plot.isCity() or plot.getRouteType() in self.lRoutes))
		

class NoForeignCities(GenericGoal):

	def __init__(self, plots):
		super(NoForeignCities, self).__init__()
		
		self.plots = plots
		self.exceptions = []
		self.forbidden = []
		
	def of(self, civs):
		if self.exceptions:
			raise Exception("cannot set specific civs if exceptions are already set")
		self.forbidden = civs
		return self
		
	def only(self, civs):
		if self.forbidden:
			raise Exception("cannot set exceptions if specific civs are already set")
		self.exceptions = civs
		return self
		
	def condition(self):
		return self.plots.cities().all(lambda city: city.getOwner() not in self.forbidden or is_minor(city) or city.getOwner() == self.iPlayer or civ(city) in self.exceptions)


class MultipleNoForeignCities(CombinedGoal):

	def __init__(self, *areas):
		super(MultipleNoForeignCities, self).__init__(*(NoForeignCities(area) for area in areas))
	
	def of(self, civs):
		for subgoal in self.subgoals:
			subgoal.of(civs)
		return self
	
	def only(self, civs):
		for subgoal in self.subgoals:
			subgoal.only(civs)
		return self


class CultureCovered(GenericGoal):

	def __init__(self, plots):
		super(CultureCovered, self).__init__()
		
		self.plots = plots
	
	def condition(self):
		return self.plots.all(lambda p: p.getOwner() == self.iPlayer)


def CultureCovereds(*areas):
	return CombinedGoal(CultureCovered(area) for area in areas)


class CapitalBuilding(GenericGoal):

	def __init__(self, iBuilding):
		super(CapitalBuilding, self).__init__()
		
		self.iBuilding = iBuilding
		
	def condition(self):
		return capital(self.iPlayer).isHasRealBuilding(self.iBuilding)


class NeverConquer(GenericGoal):

	def __init__(self):
		super(NeverConquer, self).__init__()
		
		self.win()
		
		self.onCityAcquired()
	
	def onCityAcquired(self):
		def check_handler(iOwner, iPlayer, city, bConquest):
			if self.iPlayer == iPlayer and bConquest:
				self.lose()
		
		self.addEventHandler("cityAcquired", check_handler)
		return self


### CIV GOALS ###

dGoals = {
	iEgypt : (
		PlayerCulture(500).by(-850), 
		Wonders(iPyramids, iGreatLibrary, iGreatLighthouse).by(-100), 
		PlayerCulture(5000).by(170),
	),
	iBabylonia : (
		DiscoverFirsts(iConstruction, iArithmetics, iWriting, iCalendar, iContract),
		MostPopulationCity(tBabylon).at(-850),
		MostCultureCity(tBabylon).at(-700),
	),
	iHarappa : (
		TradeConnection().by(-1600),
		BuildingCounts((iReservoir, 3), (iGranary, 2), (iSmokehouse, 2)).by(-1500),
		TotalPopulation(30).by(-800),
	),
	iChina : (
		BuildingCounts((iConfucianCathedral, 2), (iTaoistCathedral, 2)).by(1000),
		DiscoverFirsts(iCompass, iPaper, iGunpowder, iPrinting),
		GoldenAges(4).by(1800),
	),
	iGreece : (
		DiscoverFirsts(iMathematics, iLiterature, iAesthetics, iPhilosophy, iMedicine),
		ControlCivs(iEgypt, iPhoenicia, iBabylonia, iPersia).at(-330),
		Wonders(iParthenon, iColossus, iStatueOfZeus, iTempleOfArtemis).by(-250),
	),
	iIndia : (
		BuildingCounts((iHinduShrine, 1), (iBuddhistShrine, 1)).at(-100),
		ReligiousBuildingCount(iTemple, 20).by(700),
		PopulationPercent(20).at(1200),
	),
	iPhoenicia : (
		CityBuildings(tCarthage, [iPalace, iGreatCothon]).by(-300),
		Controls(
			plots.rectangle(dNormalArea[iItaly]).without((62, 47), (63, 47), (63, 46)),
			plots.rectangle(tIberia),
		).at(-100),
		PlayerGold(5000),
	),
	iPolynesia : (
		SettledSome(2,
			plots.rectangle(tHawaii),
			plots.rectangle(tNewZealand),
			plots.rectangle(tMarquesas),
			plots.rectangle(tEasterIsland),
		).by(800),
		SettledAll(
			plots.rectangle(tHawaii),
			plots.rectangle(tNewZealand),
			plots.rectangle(tMarquesas),
			plots.rectangle(tEasterIsland),
		).by(1000),
		Wonder(iMoaiStatues).by(1200),
	),
	iPersia : (
		LandPercent(7).by(140),
		WonderCount(7).by(350),
		ReligiousBuildingCount(iShrine, 2).at(350),
	),
	iRome : (
		BuildingCounts((iBarracks, 6), (iAqueduct, 5), (iArena, 4), (iForum, 3)).by(100),
		CitiesInAreas(
			(plots.normal(iSpain), 2),
			(plots.rectangle(tGaul), 2),
			(plots.core(iEngland), 1),
			(plots.rectangle(tAfrica), 2),
			(plots.core(iByzantium), 4),
			(plots.core(iEgypt), 2),
		).at(320),
		DiscoverFirsts(iArchitecture, iPolitics, iScholarship, iMachinery, iCivilService),
	),
	iMaya : (
		Discover(iCalendar).by(200),
		Wonder(iTempleOfKukulkan).by(900),
		NewWorldFirstContact(),
	),
	iTamils : (
		CombinedGoal(
			PlayerGold(3000),
			PlayerCulture(2000),
		).at(800),
		ControlOrVassalizes(
			plots.rectangle(tDeccan), 
			plots.rectangle(tSrivijaya),
		).at(1000),
		TradeGold(4000).by(1200),
	),
	iEthiopia : (
		AcquiredResourceCount(iIncense, 3).by(400),
		CombinedGoal(
			ConvertAfterFounding(iOrthodoxy, 5),
			SpecialistCount(iSpecialistGreatProphet, 3),
			BuildingCount(iOrthodoxCathedral, 1),
		).by(1200),
		MoreReligionInArea(iOrthodoxy, iIslam, plots.regions(*lAfrica)).at(1500),
	),
	iKorea : (
		BuildingCounts((iBuddhistCathedral, 1), (iConfucianCathedral, 1)).by(1200),
		DiscoverFirst(iPrinting),
		SunkShips(20),
	),
	iByzantium : (
		PlayerGold(5000).at(1000),
		CombinedGoal(
			MostPopulationCity(tConstantinople),
			MostCultureCity(tConstantinople),
		).at(1200),
		CitiesInAreas(
			(plots.rectangle(tBalkans), 3),
			(plots.rectangle(tNorthAfrica), 3),
			(plots.rectangle(tNearEast), 3),
		).at(1450),
	),
	iJapan : (
		CombinedGoal(
			AverageCityCulture(6000),
			NoCitiesLost()
		).by(1600),
		ControlOrVassalizes(
			plots.rectangle(tKorea),
			plots.rectangle(tManchuria),
			plots.rectangle(tChina),
			plots.rectangle(tIndochina).without(lIndochinaExceptions),
			plots.rectangle(tIndonesia),
			plots.rectangle(tPhilippines),
		).at(1940),
		EraDiscoverFirsts((iGlobal, 8), (iDigital, 8)),
	),
	iVikings : (
		AnyGoal(Control(plots.core(iCiv)) for iCiv in dCivGroups[iCivGroupEurope] if dSpawn[iCiv] > 1050).at(1050),
		FirstNewWorld().by(1100),
		RaidGold(3000).by(1500),
	),
	iTurks : (
		CombinedGoal(
			LandPercent(6),
			PillageCount(20),
		).by(900),
		CombinedGoal(
			RouteConnection(plots.rectangle(tChina), lMediterraneanPorts, [iRouteRoad, iRouteRomanRoad, iRouteRailroad, iRouteHighway]),
			CorporationCount(iSilkRoute, 10),
		).by(1100),
		DifferentCities(
			CapitalCultureLevel(iCultureLevelDeveloping).by(900),
			CapitalCultureLevel(iCultureLevelRefined).by(1100),
			CapitalCultureLevel(iCultureLevelInfluential).by(1400),
		),
	),
	iArabia : (
		MostAdvanced().at(1300),
		ControlOrVassalizes(
			plots.core(iEgypt),
			plots.rectangle(tAfrica),
			plots.core(iBabylonia),
			plots.core(iPersia),
			plots.normal(iSpain),
		).at(1300),
		ReligionSpreadPercent(iIslam, 30),
	),
	iTibet : (
		AcquiredCities(5).by(1000),
		ReligionSpreadPercent(iBuddhism, 25).by(1400),
		CitySpecialistCount(plots.capital(iTibet), iSpecialistGreatProphet, 5).by(1700),
	),
	iIndonesia : (
		LargestPopulation().at(1300),
		HappinessResourceCount(10).by(1500),
		PopulationPercent(9).at(1940),
	),
	iMoors : (
		CombinedGoal(
			CitiesInArea(plots.rectangle(tMaghreb), 3),
			ConqueredCitiesInArea(plots.rectangle(tIberia), 2),
			ConqueredCitiesInArea(plots.rectangle(tWestAfrica), 2),
		).at(1200),
		CombinedGoal(
			Wonder(iMezquita),
			CitySpecialistCounts(tCordoba, [iSpecialistGreatProphet, iSpecialistGreatScientist, iSpecialistGreatEngineer], 4),
		).by(1300),
		PiracyGold(3000).by(1650),
	),
	iSpain : (
		FirstNewWorld(),
		ControlledResourcesCount([iSilver, iGold], 10).by(1650),
		CombinedGoal(
			ReligionSpreadPercent(iCatholicism, 30),
			NoStateReligionInAreas(iProtestantism,
				plots.rectangle(tEurope),
				plots.rectangle(tEasternEurope),
			),
		).at(1650),
	),
	iFrance : (
		CityCultureLevel(tParis, iCultureLevelLegendary).at(1700),
		CombinedGoal(
			ControlPercentInAreas(40,
				plots.rectangle(tEurope),
				plots.rectangle(tEasternEurope),
			).withVassals(),
			ControlPercentInArea(40, plots.rectangle(tNorthAmerica)).withVassals(),
		).at(1800),
		Wonders(iNotreDame, iVersailles, iLouvre, iEiffelTower, iMetropolitain).by(1900),
	),
	iKhmer : (
		CombinedGoal(
			BuildingCounts((iBuddhistMonastery, 4), (iHinduMonastery, 4)),
			Wonder(iWatPreahPisnulok),
		).at(1200),
		AverageCityPopulation(12).at(1450),
		PlayerCulture(8000).by(1450),
	),
	iEngland : (
		CitiesInAreas(
			(plots.regions(*lNorthAmerica), 5),
			(plots.regions(*lSouthAmerica), 3),
			(plots.regions(*lAfrica), 4),
			(plots.regions(*lAsia), 5),
			(plots.regions(*lOceania), 3),
		).by(1730),
		CombinedGoal(
			UnitsCount([iFrigate, iShipOfTheLine], 25),
			SunkShips(50),
		).by(1800),
		EraDiscoverFirsts((iRenaissance, 8), (iIndustrial, 8)),
	),
	iHolyRome : (
		CombinedGoal(
			BuildingCount(iCatholicShrine, 1).at(1000),
			BuildingCount(iOrthodoxShrine, 1).at(1200),
			BuildingCount(iProtestantShrine, 1).at(1550),
		),
		Vassals(3).civs(dCivGroups[iCivGroupEurope]).stateReligion(iCatholicism).by(1650),
		CombinedGoal(
			CitySpecialistCounts(tVienna, [iSpecialistGreatArtist, iSpecialistGreatStatesman], 10),
			AttitudeCount(AttitudeTypes.ATTITUDE_PLEASED, 8).civs(dCivGroups[iCivGroupEurope]),
		).at(1850),
	),
	iRussia : (
		CombinedGoal(
			SettledCitiesInArea(plots.rectangle(tSiberia), 7).by(1700),
			RouteConnection(plots.capital(iRussia), plots.of(lSiberianCoast), [iRailroad]).by(1920),
		),
		Projects(iManhattanProject, iLunarLanding),
		CombinedGoal(
			Communist(),
			AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 5).communist()
		).by(1950),
	),
	iMali : (
		HolyCityTradeMission().by(1350),
		CombinedGoal(
			Wonder(iUniversityOfSankore),
			WonderSpecialistCount(iUniversityOfSankore, iSpecialistGreatProphet, 1)
		).by(1500),
		CombinedGoal(
			PlayerGold(5000).at(1500),
			PlayerGold(15000).at(1700),
		),
	),
	iPoland : (
		PopulationCities(12, 3).by(1400),
		DiscoverFirst(iCivilLiberties),
		BuildingCountSum(3, [iOrthodoxCathedral, iCatholicCathedral, iProtestantCathedral]).by(1600),
	),
	iPortugal : (
		OpenBordersCount(14).by(1550),
		AcquiredResourcesCount(lColonialResources, 12).by(1650),
		CitiesInAreasSum(15,
			plots.rectangle(tBrazil),
			plots.regions(*lAfrica),
			plots.regions(*lAsia),
		).at(1700),
	),
	iInca : (
		CombinedGoal(
			BuildingCount(iTambo, 5),
			Route(plots.of(lAndeanCoast), [iRouteRoad]),
		).by(1550),
		PlayerGold(2500).at(1550),
		NoForeignCities(plots.rectangle(tSouthAmerica)).at(1700),
	),
	iItaly : (
		Wonders(iSanMarcoBasilica, iSistineChapel, iSantaMariaDelFiore).by(1500),
		CultureLevelCities(iCultureLevelInfluential, 3).by(1600),
		ControlPercentInArea(65, plots.rectangle(tMediterranean).without(lMediterraneanExceptions).coastal()).by(1930),
	),
	iMongols : (
		Control(plots.normal(iChina)).at(1300),
		RazeCount(7),
		LandPercent(12).by(1500),
	),
	iAztecs : (
		MostPopulationCity(tTenochtitlan).at(1520),
		BuildingCounts((iPaganTemple, 6), (iSacrificialAltar, 6)).by(1650),
		EnslaveCount(20).exceptions(dCivGroups[iCivGroupAmerica])
	),
	iMughals : (
		BuildingCount(iIslamicCathedral, 3).by(1500),
		Wonders(iRedFort, iShalimarGardens, iTajMahal).by(1660),
		PlayerCulture(50000).at(1750),
	),
	iOttomans : (
		CapitalWonderCount(4).at(1550),
		CombinedGoal(
			CultureCovereds(
				plots.of(lEasternMediterranean),
				plots.of(lBlackSea),
			),
			Controls(
				plots.surrounding(tCairo),
				plots.surrounding(tMecca),
				plots.surrounding(tBaghdad),
				plots.surrounding(tVienna),
			),
		).by(1700),
		MoreCultureThan(dCivGroups[iCivGroupEurope]).at(1800),
	),
	iThailand : (
		OpenBordersCount(10).at(1650),
		MostPopulationCity(tAyutthaya).at(1700),
		NoForeignCities(plots.rectangle(tSouthAmerica)).only(lSouthAsianCivs).at(1900),
	),
	iCongo : (
		ReligiousVotePercent(15).by(1650),
		SlaveTradeGold(1000).by(1800),
		EnterEra(iIndustrial).before(iGlobal),
	),
	iIran : (
		OpenBordersCount(6, dCivGroups[iCivGroupEurope]).at(1650),
		Controls(
			plots.rectangle(tSafavidMesopotamia),
			plots.rectangle(tTransoxiana),
			plots.rectangle(tNorthWestIndia).without(lNorthWestIndiaExceptions),
		).at(1750),
		CultureCity(20000).at(1800),
	),
	iNetherlands : (
		CitySpecialistCount(plots.capital(iNetherlands), iSpecialistGreatMerchant, 3).by(1745),
		ConquerFrom(dCivGroups[iCivGroupEurope], 4).notin(lEurope).by(1745),
		AcquiredResourceCount(iSpices, 7).by(1775),
	),
	iGermany : (
		CitySpecialistCounts(plots.capital(iGermany), lGreatPeople, 7).at(1900),
		ControlCivs(
			iItaly,
			iFrance,
			iEngland,
			iVikings,
			iRussia,
		).at(1940),
		EraDiscoverFirsts((iIndustrial, 8), (iGlobal, 8)),
	),
	iAmerica : (
		CombinedGoal(
			NoForeignCities(plots.rectangle(tNorthCentralAmerica)).of(dCivGroups[iCivGroupEurope]),
			ControlOrVassalize(plots.core(iMexico)),
		).at(1900),
		Wonders(iStatueOfLiberty, iBrooklynBridge, iEmpireStateBuilding, iGoldenGateBridge, iPentagon, iUnitedNations).by(1950),
		CombinedGoal(
			AlliedCommercePercent(75),
			AlliedPowerPercent(75),
		).by(1990),
	),
	iArgentina : (
		GoldenAges(2).by(1930),
		CityCultureLevel(plots.capital(iArgentina), iCultureLevelLegendary).by(1960),
		GoldenAges(6).by(2000),
	),
	iMexico : (
		StateReligionBuildingCount(cathedral, 3).by(1880),
		GreatGenerals(3).by(1940),
		MostPopulationCity(tMexico).at(1960),
	),
	iColombia : (
		MultipleNoForeignCities(
			plots.rectangle(tPeru),
			plots.rectangle(tGranColombia),
			plots.rectangle(tGuayanas),
			plots.rectangle(tCaribbean),
		).of(dCivGroups[iCivGroupEurope]).at(1870),
		Control(plots.rectangle(tSouthAmerica).without(lSouthAmericaExceptions)).at(1920),
		ResourceTradeGold(3000).by(1950),
	),
	iBrazil : (
		ImprovementCounts((iSlavePlantation, 8), (iPasture, 4)).at(1880),
		Wonders(iWembley, iCristoRedentor, iItaipuDam),
		CombinedGoal(
			ImprovementCount(iForestPreserve, 20),
			CapitalBuilding(iNationalPark),
		).by(1950),
	),
	iCanada : (
		CombinedGoal(
			RouteConnection(plots.lazy().capital(iCanada), plots.of(lAtlanticCoast), [iRailroad]),
			RouteConnection(plots.lazy().capital(iCanada), plots.of(lPacificCoast), [iRailroad]),
		).by(1920),
		CombinedGoal(
			Control(plots.regions(rCanada)),
			ControlPercentInArea(90, plots.regions(rCanada)),
			NeverConquer(),
		).by(1950),
		BrokeredPeaceCount(12).by(2000),
	),
}

### GOAL CONSTANTS ###

dTechGoals = {
	iChina: (1, [iCompass, iPaper, iGunpowder, iPrinting]),
	iBabylonia: (0, [iConstruction, iArithmetics, iWriting, iCalendar, iContract]),
	iGreece: (0, [iMathematics, iLiterature, iAesthetics, iPhilosophy, iMedicine]),
	iRome: (2, [iArchitecture, iPolitics, iScholarship, iMachinery, iCivilService]),
	iKorea: (1, [iPrinting]),
	iPoland: (1, [iCivilLiberties]),
}

dEraGoals = {}

dWonderGoals = {
	iEgypt: (1, [iPyramids, iGreatLibrary, iGreatLighthouse], True),
	iGreece: (2, [iColossus, iParthenon, iStatueOfZeus, iTempleOfArtemis], True),
	iCarthage: (0, [iGreatCothon], False),
	iPolynesia: (2, [iMoaiStatues], True),
	iMaya: (1, [iTempleOfKukulkan], True),
	iMoors: (1, [iMezquita], False),
	iKhmer: (0, [iWatPreahPisnulok], False),
	iFrance: (2, [iNotreDame, iVersailles, iLouvre, iEiffelTower, iMetropolitain], True),
	iMali: (1, [iUniversityOfSankore], False),
	iItaly: (0, [iSanMarcoBasilica, iSistineChapel, iSantaMariaDelFiore], True),
	iMughals: (1, [iTajMahal, iRedFort, iShalimarGardens], True),
	iAmerica: (1, [iStatueOfLiberty, iBrooklynBridge, iEmpireStateBuilding, iGoldenGateBridge, iPentagon, iUnitedNations], True),
	iBrazil: (1, [iWembley, iCristoRedentor, iItaipuDam], True),
}

dReligionGoals = {}
		
### EVENT HANDLING ###

@handler("GameStart")
def setup():

	# 1700 AD scenario: handle dates that have already been passed
	if scenario() == i1700AD:
		for iCiv in [iChina, iIndia, iTamils, iKorea, iVikings, iTurks, iSpain, iHolyRome, iPoland, iPortugal, iMughals, iOttomans, iThailand]:
			loseAll(slot(iCiv))
			
		win(slot(iIran), 0)
		win(slot(iJapan), 0)
		win(slot(iFrance), 0)
		win(slot(iCongo), 0)
		
		# French goal needs to be winnable
		data.setWonderBuilder(iNotreDame, slot(iFrance))
		data.setWonderBuilder(iVersailles, slot(iFrance))
		data.setWonderBuilder(iLouvre, slot(iFrance))
		
		# help Congo
		data.iCongoSlaveCounter += turns(500)
		
		# help Netherlands
		data.iDutchColonies += 2
	
	# ignore AI goals
	bIgnoreAI = infos.constant('NO_AI_UHV_CHECKS')
	data.bIgnoreAI = bIgnoreAI
	
	if bIgnoreAI:
		for iPlayer in players.major().ai():
			loseAll(iPlayer)

@handler("switch")
def onCivSwitch(iPreviousPlayer):
	if infos.constant('NO_AI_UHV_CHECKS') == 1:
		loseAll(iPreviousPlayer)

@handler("BeginGameTurn")
def aztecUHVHelp():
	if year() == year(1500) and player(iAztecs).isHuman():
		city = cities.capital(iEngland)
		if city and city.getPopulation() > 14:
				city.changePopulation(-3)

@handler("cityRazed")
def onCityRazed(city, iPlayer):
	iCiv = civ(iPlayer)

	if not game.isVictoryValid(7): return
	
	if not player(iPlayer).isHuman() and data.bIgnoreAI: return
	
	# second Mongol goal: raze seven cities
	if iCiv == iMongols:
		if isPossible(iPlayer, 1):
			data.iMongolRazes += 1
			if data.iMongolRazes >= 7:
				win(iPlayer, 1)

@handler("BeginPlayerTurn")
def checkTurn(iGameTurn, iPlayer):
	if not game.isVictoryValid(7): return
	
	if is_minor(iPlayer): return
	
	if iGameTurn == scenarioStartTurn(): return
	
	pPlayer = player(iPlayer)
	iCiv = civ(iPlayer)
	
	if not pPlayer.isAlive(): return
	
	# Don't check AI civilizations to improve speed
	if not pPlayer.isHuman() and data.bIgnoreAI: return
	
	if iCiv == iEgypt:
	
		# first goal: have 500 culture in 850 BC
		if iGameTurn == year(-850):
			if pPlayer.countTotalCulture() >= turns(500):
				win(iPlayer, 0)
			else:
				lose(iPlayer, 0)
				
		# first goal: build the Pyramids, the Great Lighthouse and the Great Library by 100 BC
		if iGameTurn == year(-100):
			expire(iPlayer, 1)
				
		# third goal: have 5000 culture in 170 AD
		if iGameTurn == year(170):
			if pPlayer.countTotalCulture() >= turns(5000):
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
				
	elif iCiv == iBabylonia:
	
		# first goal: be the first to discover Construction, Arithmetics, Writing, Calendar and Contract
		
		# second goal: make Babylon the most populous city in the world in 850 BC
		if iGameTurn == year(-850):
			if isBestCity(iPlayer, (76, 40), cityPopulation):
				win(iPlayer, 1)
			else:
				lose(iPlayer, 1)
			
		# third goal: make Babylon the most cultured city in the world in 700 BC
		if iGameTurn == year(-700):
			if isBestCity(iPlayer, (76, 40), cityCulture):
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
				
	elif iCiv == iHarappa:
	
		# first goal: establish a trade connection with another civilization by 1600 BC
		if isPossible(iPlayer, 0):
			if isTradeConnected(iPlayer):
				win(iPlayer, 0)
				
		if iGameTurn == year(-1600):
			expire(iPlayer, 0)
			
		# second goal: build three Baths and two Walls by 1500 BC
		if iGameTurn == year(-1500):
			expire(iPlayer, 1)
			
		# third goal: have a total population of 30 by 800 BC
		if isPossible(iPlayer, 2):
			if pPlayer.getTotalPopulation() >= 30:
				win(iPlayer, 2)
				
		if iGameTurn == year(-800):
			expire(iPlayer, 2)
				
	elif iCiv == iChina:
	
		# first goal: build two Confucian and Taoist Cathedrals by 1000 AD
		if iGameTurn == year(1000):
			expire(iPlayer, 0)
			
		# second goal: be first to discover Compass, Gunpowder, Paper and Printing Press
		
		# third goal: experience four golden ages by 1800 AD
		if isPossible(iPlayer, 2):
			if data.iChineseGoldenAgeTurns >= turns(32):
				win(iPlayer, 2)
				
			if pPlayer.isGoldenAge() and not pPlayer.isAnarchy():
				data.iChineseGoldenAgeTurns += 1
				
		if iGameTurn == year(1800):
			expire(iPlayer, 2)
			
	elif iCiv == iGreece:
	
		# first goal: be the first to discover Mathematics, Literature, Aesthetics, Medicine and Philosophy
			
		# second goal: control Egypt, Phoenicia, Babylonia and Persia in 330 BC
		if iGameTurn == year(-330):
			bEgypt = checkOwnedCiv(iPlayer, iEgypt)
			bPhoenicia = checkOwnedCiv(iPlayer, iCarthage)
			bBabylonia = checkOwnedCiv(iPlayer, iBabylonia)
			bPersia = checkOwnedCiv(iPlayer, iPersia)
			if bEgypt and bPhoenicia and bBabylonia and bPersia:
				win(iPlayer, 1)
			else:
				lose(iPlayer, 1)
		
		# third goal: build the Parthenon, the Colossus, the Statue of Zeus and the Temple of Artemis by 250 BC
		if iGameTurn == year(-250):
			expire(iPlayer, 2)
				
	elif iCiv == iIndia:
	
		# first goal: control the Hindu and Buddhist shrine in 100 BC
		if iGameTurn == year(-100):
			bBuddhistShrine = getNumBuildings(iPlayer, iBuddhistShrine) > 0
			bHinduShrine = getNumBuildings(iPlayer, iHinduShrine) > 0
			if bHinduShrine and bBuddhistShrine:
				win(iPlayer, 0)
			else:
				lose(iPlayer, 0)
				
		# second goal: build 20 temples by 700 AD
		if iGameTurn == year(700):
			expire(iPlayer, 1)
			
		# third goal: control 20% of the world's population in 1200 AD
		if iGameTurn == year(1200):
			if getPopulationPercent(iPlayer) >= 20.0:
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
				
	elif iCiv == iPhoenicia:
	
		# first goal: build a Palace and the Great Cothon in Carthagee by 300 BC
		if isPossible(iPlayer, 0):
			bPalace = isBuildingInCity((58, 39), iPalace)
			bGreatCothon = isBuildingInCity((58, 39), iGreatCothon)
			if bPalace and bGreatCothon:
				win(iPlayer, 0)
		
		if iGameTurn == year(-300):
			expire(iPlayer, 0)
				
		# second goal: control Italy and Iberia in 100 BC
		if iGameTurn == year(-100):
			bItaly = isControlled(iPlayer, plots.rectangle(*dNormalArea[iItaly]).without((62, 47), (63, 47), (63, 46)))
			bIberia = isControlled(iPlayer, plots.rectangle(tIberia))
			if bItaly and bIberia:
				win(iPlayer, 1)
			else:
				lose(iPlayer, 1)
				
		# third goal: have 5000 gold in 200 AD
		if iGameTurn == year(200):
			if pPlayer.getGold() >= turns(5000):
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
				
	elif iCiv == iPolynesia:
	
		# first goal: settle two of the following island groups by 800 AD: Hawaii, New Zealand, Marquesas and Easter Island
		if iGameTurn == year(800):
			expire(iPlayer, 0)
			
		# second goal: settle Hawaii, New Zealand, Marquesas and Easter Island by 1000 AD
		if iGameTurn == year(1000):
			expire(iPlayer, 1)
			
		# third goal: build the Moai Statues by 1200 AD
		if iGameTurn == year(1200):
			expire(iPlayer, 2)
			
	elif iCiv == iPersia:
		
		# first goal: control 7% of world territory by 140 AD
		if isPossible(iPlayer, 0):
			if getLandPercent(iPlayer) >= 6.995:
				win(iPlayer, 0)
		
		if iGameTurn == year(140):
			expire(iPlayer, 0)
			
		# second goal: control seven wonders by 350 AD
		if isPossible(iPlayer, 1):
			if countWonders(iPlayer) >= 7:
				win(iPlayer, 1)
				
		if iGameTurn == year(350):
			expire(iPlayer, 1)
					
		# third goal: control two holy shrines in 350 AD
		if iGameTurn == year(350):
			if countShrines(iPlayer) >= 2:
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
					
	elif iCiv == iRome:
	
		# first goal: build 6 Barracks, 5 Aqueducts, 4 Arenas and 3 Forums by 100 AD
		if iGameTurn == year(100):
			expire(iPlayer, 0)
			
		# second goal: control Iberia, Gaul, Britain, Africa, Greece, Asia Minor and Egypt in 320 AD
		if iGameTurn == year(320):
			bSpain = cities.normal(iSpain).owner(iPlayer) >= 2
			bFrance = cities.rectangle(tGaul).owner(iPlayer) >= 2
			bEngland = cities.core(iEngland).owner(iPlayer) >= 1
			bCarthage = cities.rectangle(tAfrica).owner(iPlayer) >= 2
			bByzantium = cities.core(iByzantium).owner(iPlayer) >= 4
			bEgypt = cities.core(iEgypt).owner(iPlayer) >= 2
			if bSpain and bFrance and bEngland and bCarthage and bByzantium and bEgypt:
				win(iPlayer, 1)
			else:
				lose(iPlayer, 1)
					
		# third goal: be first to discover Theology, Machinery and Civil Service
		
	elif iCiv == iMaya:
		
		# first goal: discover Calendar by 200 AD
		if iGameTurn == year(200):
			expire(iPlayer, 0)
			
		# second goal: build the Temple of Kukulkan by 900 AD
		if iGameTurn == year(900):
			expire(iPlayer, 1)
			
		# third goal: make contact with a European civilization before they discover America
		if isPossible(iPlayer, 2):
			if any(team(iPlayer).canContact(slot(iEuropean)) for iEuropean in dCivGroups[iCivGroupEurope]):
				win(iPlayer, 2)
		
	elif iCiv == iTamils:
	
		# first goal: have 3000 gold and 2000 culture in 800 AD
		if iGameTurn == year(800):
			if pPlayer.getGold() >= turns(3000) and pPlayer.countTotalCulture() >= turns(2000):
				win(iPlayer, 0)
			else:
				lose(iPlayer, 0)
				
		# second goal: control or vassalize the Deccan and Srivijaya in 1000 AD
		if iGameTurn == year(1000):
			bDeccan = isControlledOrVassalized(iPlayer, plots.rectangle(tDeccan))
			bSrivijaya = isControlledOrVassalized(iPlayer, plots.rectangle(tSrivijaya))
			if bDeccan and bSrivijaya:
				win(iPlayer, 1)
			else:
				lose(iPlayer, 1)
				
		# third goal: acquire 4000 gold by trade by 1200 AD
		if isPossible(iPlayer, 2):
			iTradeGold = 0
			
			# gold from city trade routes
			iTradeCommerce = 0
			for city in cities.owner(iPlayer):
				iTradeCommerce += city.getTradeYield(2)
			iTradeGold += iTradeCommerce * pPlayer.getCommercePercent(0)
			
			# gold from per turn gold trade
			for iPlayer in players.major():
				iTradeGold += pPlayer.getGoldPerTurnByPlayer(iPlayer) * 100
			
			data.iTamilTradeGold += iTradeGold
			
			if data.iTamilTradeGold / 100 >= turns(4000):
				win(iPlayer, 2)
				
		if iGameTurn == year(1200):
			expire(iPlayer, 2)
					
	elif iCiv == iEthiopia:
		
		# first goal: acquire three incense resources by 400 AD
		if isPossible(iPlayer, 0):
			if pPlayer.getNumAvailableBonuses(iIncense) >= 3:
				win(iPlayer, 0)
				
		if iGameTurn == year(400):
			expire(iPlayer, 0)
			
		# second goal: convert to Orthodoxy 5 turns after it is founded and have three settled Great Prophets and an Orthodox Cathedral by 1200 AD
		if isPossible(iPlayer, 1):
			iNumOrthodoxCathedrals = getNumBuildings(iPlayer, iOrthodoxCathedral)
			iGreatProphets = countSpecialists(iPlayer, iSpecialistGreatProphet)
			if data.bEthiopiaConverted and iNumOrthodoxCathedrals >= 1 and iGreatProphets >= 3:
				win(iPlayer, 1)
		
			if game.isReligionFounded(iOrthodoxy) and iGameTurn > game.getReligionGameTurnFounded(iOrthodoxy) + turns(5):
				if not data.bEthiopiaConverted:
					expire(iPlayer, 1)
				
		if iGameTurn == year(1200):
			expire(iPlayer, 1)
			
		# third goal: make sure there are more Orthodox than Muslim cities in Africa in 1500 AD
		if iGameTurn == year(1500):
			iOrthodoxCities = countRegionReligion(iOrthodoxy, lAfrica)
			iMuslimCities = countRegionReligion(iIslam, lAfrica)
			if iOrthodoxCities > iMuslimCities:
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
				
	elif iCiv == iKorea:
	
		# first goal: build a Buddhist Stupa and a Confucian Academy by 1200 AD
		if iGameTurn == year(1200):
			expire(iPlayer, 0)
			
		# second goal: be first to discover Printing Press
		
		# third goal: sink 20 enemy ships
					
	elif iCiv == iByzantium:
		
		# first goal: have 5000 gold in 1000 AD
		if iGameTurn == year(1000):
			if pPlayer.getGold() >= turns(5000):
				win(iPlayer, 0)
			else:
				lose(iPlayer, 0)
				
		# second goal: make Constantinople the world's largest and most cultured city in 1200 AD
		if iGameTurn == year(1200):
			bLargest = isBestCity(iPlayer, (68, 45), cityPopulation)
			bCulture = isBestCity(iPlayer, (68, 45), cityCulture)
			if bLargest and bCulture:
				win(iPlayer, 1)
			else:
				lose(iPlayer, 1)
				
		# third goal: control three cities in the Balkans, Northern Africa and the Near East in 1450 AD
		if iGameTurn == year(1450):
			bBalkans = cities.rectangle(tBalkans).owner(iPlayer) >= 3
			bNorthAfrica = cities.rectangle(tNorthAfrica).owner(iPlayer) >= 3
			bNearEast = cities.rectangle(tNearEast).owner(iPlayer) >= 3
			if bBalkans and bNorthAfrica and bNearEast:
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
					
	elif iCiv == iJapan:
	
		# first goal: have an average culture of 6000 by 1600 AD without ever losing a city
		if isPossible(iPlayer, 0):
			if getAverageCulture(iPlayer) >= turns(6000):
				win(iPlayer, 0)
				
		if iGameTurn == year(1600):
			expire(iPlayer, 0)
				
		# second goal: control or vassalize Korea, Manchuria, China, Indochina, Indonesia and the Philippines in 1940 AD
		if iGameTurn == year(1940):
			bKorea = isControlledOrVassalized(iPlayer, plots.rectangle(tKorea))
			bManchuria = isControlledOrVassalized(iPlayer, plots.rectangle(tManchuria))
			bChina = isControlledOrVassalized(iPlayer, plots.rectangle(tChina))
			bIndochina = isControlledOrVassalized(iPlayer, plots.rectangle(tIndochina).without(lIndochinaExceptions))
			bIndonesia = isControlledOrVassalized(iPlayer, plots.rectangle(tIndonesia))
			bPhilippines = isControlledOrVassalized(iPlayer, plots.rectangle(tPhilippines))
			if bKorea and bManchuria and bChina and bIndochina and bIndonesia and bPhilippines:
				win(iPlayer, 1)
			else:
				lose(iPlayer, 1)
				
		# third goal: be the first to discover 5 modern techs
		
	elif iCiv == iVikings:
	
		# first goal: control the core of a European civilization in 1050 AD
		if iGameTurn == year(1050):
			lEuroCivs = [iLoopCiv for iLoopCiv in dCivGroups[iCivGroupEurope] if dBirth[iLoopCiv] < 1050 and iPlayer != slot(iLoopCiv)]
			if isCoreControlled(iPlayer, lEuroCivs):
				win(iPlayer, 0)
			else:
				lose(iPlayer, 0)
				
		# second goal: found a city in America by 1100 AD
		if iGameTurn == year(1100):
			expire(iPlayer, 1)
			
		# third goal: acquire 3000 gold by pillaging, conquering cities and sinking ships by 1500 AD
		if isPossible(iPlayer, 2):
			if data.iVikingGold >= turns(3000):
				win(iPlayer, 2)
				
		if iGameTurn == year(1500):
			expire(iPlayer, 2)
			
	elif iCiv == iTurks:
	
		# first goal: control 6% of the world's territory and pillage 20 improvements by 900 AD
		if isPossible(iPlayer, 0):
			if getLandPercent(iPlayer) >= 5.995 and data.iTurkicPillages >= 20:
				win(iPlayer, 0)
				
		if iGameTurn == year(900):
			expire(iPlayer, 0)
			
		# second goal: create an overland trade route between a Chinese and a Mediterranean city and spread the Silk Route to ten of your cities by 1100 AD
		if isPossible(iPlayer, 1):
			if isConnectedByTradeRoute(iPlayer, plots.rectangle(tChina), lMediterraneanPorts) and pPlayer.countCorporations(iSilkRoute) >= 10:
				win(iPlayer, 1)
				
		if iGameTurn == year(1100):
			expire(iPlayer, 1)
			
		# third goal: have a capital with developing culture by 900 AD, a different capital with refined culture by 1100 AD and another capital with influential culture by 1400 AD
		if isPossible(iPlayer, 2):
			capital = pPlayer.getCapitalCity()
			tCapital = (capital.getX(), capital.getY())
			
			if iGameTurn <= year(900):
				if not data.tFirstTurkicCapital and capital.getCulture(iPlayer) >= infos.culture(3).getSpeedThreshold(game.getGameSpeedType()):
					data.tFirstTurkicCapital = tCapital
			
			if iGameTurn <= year(1100):
				if data.tFirstTurkicCapital and not data.tSecondTurkicCapital and tCapital != data.tFirstTurkicCapital and capital.getCulture(iPlayer) >= infos.culture(4).getSpeedThreshold(game.getGameSpeedType()):
					data.tSecondTurkicCapital = tCapital
					
			if iGameTurn <= year(1400):
				if tCapital != data.tFirstTurkicCapital and tCapital != data.tSecondTurkicCapital and data.tFirstTurkicCapital and data.tSecondTurkicCapital and capital.getCulture(iPlayer) >= infos.culture(5).getSpeedThreshold(game.getGameSpeedType()):
					win(iPlayer, 2)
					
		if iGameTurn == year(900):
			if not data.tFirstTurkicCapital:
				expire(iPlayer, 2)
				
		if iGameTurn == year(1100):
			if not data.tSecondTurkicCapital:
				expire(iPlayer, 2)
				
		if iGameTurn == year(1400):
			expire(iPlayer, 2)
			
	elif iCiv == iArabia:
	
		# first goal: be the most advanced civilization in 1300 AD
		if iGameTurn == year(1300):
			if isBestPlayer(iPlayer, playerTechs):
				win(iPlayer, 0)
			else:
				lose(iPlayer, 0)
				
		# second goal: control or vassalize Spain, the Maghreb, Egypt, Mesopotamia and Persia in 1300 AD
		if iGameTurn == year(1300):
			bEgypt = isControlledOrVassalized(iPlayer, plots.core(iEgypt))
			bMaghreb = isControlledOrVassalized(iPlayer, plots.rectangle(tAfrica))
			bMesopotamia = isControlledOrVassalized(iPlayer, plots.core(iBabylonia))
			bPersia = isControlledOrVassalized(iPlayer, plots.core(iPersia))
			bSpain = isControlledOrVassalized(iPlayer, plots.normal(iSpain))
			if bSpain and bMaghreb and bEgypt and bMesopotamia and bPersia:
				win(iPlayer, 1)
			else:
				lose(iPlayer, 1)
		
		# third goal: spread Islam to 30% of the cities in the world
		if isPossible(iPlayer, 2):
			if game.calculateReligionPercent(iIslam) >= 30.0:
				win(iPlayer, 2)
				
	elif iCiv == iTibet:
	
		# first goal: acquire five cities by 1000 AD
		if iGameTurn == year(1000):
			expire(iPlayer, 0)
			
		# second goal: spread Buddhism to 25% by 1400 AD
		if isPossible(iPlayer, 1):
			if game.calculateReligionPercent(iBuddhism) >= 25.0:
				win(iPlayer, 1)
				
		if iGameTurn == year(1400):
			expire(iPlayer, 1)
			
		# third goal: settle five great prophets in Lhasa by 1700 AD
		if isPossible(iPlayer, 2):
			if countCitySpecialists(iPlayer, plots.capital(iTibet), iSpecialistGreatProphet) >= 5:
				win(iPlayer, 2)
				
		if iGameTurn == year(1700):
			expire(iPlayer, 2)
			
	elif iCiv == iIndonesia:
	
		# first goal: have the largest population in the world in 1300 AD
		if iGameTurn == year(1300):
			if isBestPlayer(iPlayer, playerRealPopulation):
				win(iPlayer, 0)
			else:
				lose(iPlayer, 0)
				
		# second goal: acquire 10 different happiness resources by 1500 AD
		if isPossible(iPlayer, 1):
			if countHappinessResources(iPlayer) >= 10:
				win(iPlayer, 1)
				
		if iGameTurn == year(1500):
			expire(iPlayer, 1)
		
		# third goal: control 9% of the world's population in 1940 AD
		if iGameTurn == year(1940):
			if getPopulationPercent(iPlayer) >= 9.0:
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
				
	elif iCiv == iMoors:
	
		# first goal: control three cities in the Maghreb and conquer two cities in Iberia and West Africa
		if iGameTurn == year(1200):
			bIberia = getNumConqueredCitiesInArea(iPlayer, plots.rectangle(tIberia)) >= 2
			bMaghreb = getNumCitiesInArea(iPlayer, plots.rectangle(tMaghreb)) >= 3
			bWestAfrica = getNumConqueredCitiesInArea(iPlayer, plots.rectangle(tWestAfrica)) >= 2
			
			if bIberia and bMaghreb and bWestAfrica:
				win(iPlayer, 0)
			else:
				lose(iPlayer, 0)
				
		# second goal: build La Mezquita and settle four great prophets, scientists or engineers in Cordoba by 1300 AD
		if isPossible(iPlayer, 1):
			bMezquita = data.getWonderBuilder(iMezquita) == iPlayer
		
			iCounter = 0
			iCounter += countCitySpecialists(iPlayer, (51, 41), iSpecialistGreatProphet)
			iCounter += countCitySpecialists(iPlayer, (51, 41), iSpecialistGreatScientist)
			iCounter += countCitySpecialists(iPlayer, (51, 41), iSpecialistGreatEngineer)
			
			if bMezquita and iCounter >= 4:
				win(iPlayer, 1)
				
		if iGameTurn == year(1300):
			expire(iPlayer, 1)
				
		# third goal: acquire 3000 gold through piracy by 1650 AD
		if isPossible(iPlayer, 2):
			if data.iMoorishGold >= turns(3000):
				win(iPlayer, 2)
				
		if iGameTurn == year(1650):
			expire(iPlayer, 2)
			
	elif iCiv == iSpain:
	
		# first goal: be the first to found a colony in America
		
		# second goal: secure 10 gold or silver resources by 1650 AD
		if isPossible(iPlayer, 1):
			iNumGold = countResources(iPlayer, iGold)
			iNumSilver = countResources(iPlayer, iSilver)
			
			if iNumGold + iNumSilver >= 10:
				win(iPlayer, 1)
				
		if iGameTurn == year(1650):
			expire(iPlayer, 1)
			
		# third goal: spread Catholicism to 30% and allow no Protestant civilizations in Europe in 1650 AD
		if iGameTurn == year(1650):
			fReligionPercent = game.calculateReligionPercent(iCatholicism)
			
			bProtestantsEurope = isStateReligionInArea(iProtestantism, tEurope)
			bProtestantsEasternEurope = isStateReligionInArea(iProtestantism, tEasternEurope)
			
			if fReligionPercent >= 30.0 and not bProtestantsEurope and not bProtestantsEasternEurope:
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
				
	elif iCiv == iFrance:
	
		# first goal: have legendary culture in Paris in 1700 AD
		if iGameTurn == year(1700):
			if getCityCulture(iPlayer, tParis) >= turns(50000):
				win(iPlayer, 0)
			else:
				lose(iPlayer, 0)
				
		# second goal: control 40% of Europe and North America in 1800 AD
		if iGameTurn == year(1800):
			iEurope, iTotalEurope = countControlledTiles(iPlayer, plots.rectangle(tEurope), True)
			iEasternEurope, iTotalEasternEurope = countControlledTiles(iPlayer, plots.rectangle(tEasternEurope), True)
			iNorthAmerica, iTotalNorthAmerica = countControlledTiles(iPlayer, plots.rectangle(tNorthAmerica), True)
			
			fEurope = (iEurope + iEasternEurope) * 100.0 / (iTotalEurope + iTotalEasternEurope)
			fNorthAmerica = iNorthAmerica * 100.0 / iTotalNorthAmerica
			
			if fEurope >= 40.0 and fNorthAmerica >= 40.0:
				win(iPlayer, 1)
			else:
				lose(iPlayer, 1)
				
		# third goal: build Notre Dame, Versailles, the Louvre, the Eiffel Tower and the Metropolitain by 1900 AD
		if iGameTurn == year(1900):
			expire(iPlayer, 2)
			
	elif iCiv == iKhmer:
	
		# first Khmer goal: build four Buddhist and Hindu monasteries and Wat Preah Pisnulok in 1200 AD
		if iGameTurn == year(1200):
			if isPossible(iPlayer, 0):
				iBuddhist = getNumBuildings(iPlayer, iBuddhistMonastery)
				iHindu = getNumBuildings(iPlayer, iHinduMonastery)
				bWatPreahPisnulok = data.getWonderBuilder(iWatPreahPisnulok) == iPlayer
				if iBuddhist >= 4 and iHindu >= 4 and bWatPreahPisnulok:
					win(iPlayer, 0)
				else:
					lose(iPlayer, 0)
				
		# second goal: have an average city size of 12 in 1450 AD
		if iGameTurn == year(1450):
			if isPossible(iPlayer, 1):
				if getAverageCitySize(iPlayer) >= 12.0:
					win(iPlayer, 1)
				else:
					lose(iPlayer, 1)
			
		# third goal: have 8000 culture by 1450 AD
		if isPossible(iPlayer, 2):
			if pPlayer.countTotalCulture() >= turns(8000):
				win(iPlayer, 2)
				
		if iGameTurn == year(1450):
			expire(iPlayer, 2)
			
	elif iCiv == iEngland:
	
		# first goal: colonize every continent by 1730 AD
		if iGameTurn == year(1730):
			expire(iPlayer, 0)
			
		# second goal: control a total of 25 frigates and ships of the line and sink 50 enemy ships by 1800 AD
		if isPossible(iPlayer, 1):
			iEnglishNavy = 0
			iEnglishNavy += pPlayer.getUnitClassCount(infos.unit(iFrigate).getUnitClassType())
			iEnglishNavy += pPlayer.getUnitClassCount(infos.unit(iShipOfTheLine).getUnitClassType())
			
			if iEnglishNavy >= 25 and data.iEnglishSinks >= 50:
				win(iPlayer, 1)
		
		if iGameTurn == year(1800):
			expire(iPlayer, 1)
			
		# third goal: be the first to enter the Industrial and Modern eras
		
	elif iCiv == iHolyRome:
	
		# first goal: control Saint Peter's Basilica in 1000 AD, the Church of the Anastasis in 1200 AD and All Saint's Church in 1550 AD
		if iGameTurn == year(1000):
			if isPossible(iPlayer, 0):
				if getNumBuildings(iPlayer, iCatholicShrine) > 0:
					data.lHolyRomanShrines[0] = True
				else:
					expire(iPlayer, 0)
					
		if iGameTurn == year(1200):
			if isPossible(iPlayer, 0):
				if getNumBuildings(iPlayer, iOrthodoxShrine) > 0:
					data.lHolyRomanShrines[1] = True
				else:
					expire(iPlayer, 0)
					
		if iGameTurn == year(1550):
			if isPossible(iPlayer, 0):
				if getNumBuildings(iPlayer, iProtestantShrine) > 0:
					data.lHolyRomanShrines[2] = True
					win(iPlayer, 0)
				else:
					expire(iPlayer, 0)

		# second goal: have three Catholic vassals in Europe by 1650 AD
		if isPossible(iPlayer, 1):
			if countVassals(iPlayer, dCivGroups[iCivGroupEurope], iCatholicism) >= 3:
				win(iPlayer, 1)
		
		if iGameTurn == year(1650):
			expire(iPlayer, 1)
		
		# third goal: settle a total of ten great artists and statesmen in Vienna and have pleased or better relations with eight independent European civilizations by 1850 AD
		if isPossible(iPlayer, 2):
			iGreatArtists = countCitySpecialists(iPlayer, tVienna, iSpecialistGreatArtist)
			iGreatStatesmen = countCitySpecialists(iPlayer, tVienna, iSpecialistGreatStatesman)
			iPleasedOrBetterEuropeans = countPlayersWithAttitudeInGroup(iPlayer, AttitudeTypes.ATTITUDE_PLEASED, dCivGroups[iCivGroupEurope])
			
			if iGreatArtists + iGreatStatesmen >= 10 and iPleasedOrBetterEuropeans >= 8:
				win(iPlayer, 2)
		
		if iGameTurn == year(1850):
			expire(iPlayer, 2)
			
	elif iCiv == iRussia:
	
		# first goal: found seven cities in Siberia by 1700 AD and build the Trans-Siberian Railway by 1920 AD
		if iGameTurn == year(1700):
			if getNumFoundedCitiesInArea(iPlayer, plots.rectangle(tSiberia)) < 7:
				lose(iPlayer, 0)
				
		if isPossible(iPlayer, 0):
			if isConnectedByRailroad(iPlayer, plots.capital(iRussia), lSiberianCoast):
				win(iPlayer, 0)
					
		if iGameTurn == year(1920):
			expire(iPlayer, 0)
			
		# second goal: be the first civilization to complete the Manhattan Project and the Apollo Program
		
		# third goal: have friendly relations with five communist civilizations by 1950 AD
		if isPossible(iPlayer, 2):
			if isCommunist(iPlayer) and countPlayersWithAttitudeAndCriteria(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY, isCommunist) >= 5:
				win(iPlayer, 2)
				
		if iGameTurn == year(1950):
			expire(iPlayer, 2)
			
	elif iCiv == iMali:
		
		# first goal: conduct a trade mission to your holy city by 1350 AD
		if iGameTurn == year(1350):
			expire(iPlayer, 0)
			
		# second goal: build the University of Sankore and settle a great prophet in its city by 1500 AD
		if isPossible(iPlayer, 1):
			if cities.owner(iPlayer).any(lambda city: city.isHasRealBuilding(iUniversityOfSankore)) and city.getFreeSpecialistCount(iSpecialistGreatProphet) >= 1:
				win(iPlayer, 1)
		
		if iGameTurn == year(1500):
			expire(iPlayer, 1)
			
		# third goal: have 5000 gold in 1500 AD and 15000 gold in 1700 AD
		if iGameTurn == year(1500):
			if pPlayer.getGold() < turns(5000):
				lose(iPlayer, 2)
				
		if iGameTurn == year(1700) and isPossible(iPlayer, 2):
			if pPlayer.getGold() >= turns(15000):
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
				
	elif iCiv == iPoland:
	
		# first goal: have three cities with a population of 12 by 1400 AD
		if isPossible(iPlayer, 0):
			if countCitiesOfSize(iPlayer, 12) >= 3:
				win(iPlayer, 0)
				
		if iGameTurn == year(1400):
			expire(iPlayer, 0)
			
		# second goal: be the first to discover Liberalism
		
		# third goal: build three Christian Cathedrals by 1600 AD
		if iGameTurn == year(1600):
			expire(iPlayer, 2)
			
	elif iCiv == iPortugal:
	
		# first goal: have open borders with 14 civilizations by 1550 AD
		if isPossible(iPlayer, 0):
			if countOpenBorders(iPlayer) >= 14:
				win(iPlayer, 0)
				
		if iGameTurn == year(1550):
			expire(iPlayer, 0)
			
		# second goal: acquire 12 colonial resources by 1650 AD
		if isPossible(iPlayer, 1):
			if countAcquiredResources(iPlayer, lColonialResources) >= 12:
				win(iPlayer, 1)
				
		if iGameTurn == year(1650):
			expire(iPlayer, 1)
			
		# third goal: control 15 cities in Brazil, Africa and Asia in 1700 AD
		if iGameTurn == year(1700):
			iCount = 0
			iCount += getNumCitiesInArea(iPlayer, plots.rectangle(tBrazil))
			iCount += getNumCitiesInRegions(iPlayer, lAfrica)
			iCount += getNumCitiesInRegions(iPlayer, lAsia)
			if iCount >= 15:
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
				
	elif iCiv == iInca:
	
		# first goal: build five Tambos and a road along the Andean coast by 1500 AD
		if isPossible(iPlayer, 0):
			if isRoad(iPlayer, lAndeanCoast) and getNumBuildings(iPlayer, iTambo) >= 5:
				win(iPlayer, 0)
				
		if iGameTurn == year(1500):
			expire(iPlayer, 0)
			
		# second goal: have 2500 gold in 1550 AD
		if iGameTurn == year(1550):
			if pPlayer.getGold() >= turns(2500):
				win(iPlayer, 1)
			else:
				lose(iPlayer, 1)
			
		# third goal: allow no other civilisations in South America in 1700 AD
		if iGameTurn == year(1700):
			if isAreaOnlyCivs(plots.rectangle(tSouthAmerica), [iCiv]):
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
				
	elif iCiv == iItaly:
	
		# first goal: build San Marco Basilica, the Sistine Chapel and Santa Maria del Fiore by 1500 AD
		if iGameTurn == year(1500):
			expire(iPlayer, 0)
			
		# second goal: have three cities with influential culture by 1600 AD
		if isPossible(iPlayer, 1):
			if countCitiesWithCultureLevel(iPlayer, 5) >= 3:
				win(iPlayer, 1)
				
		if iGameTurn == year(1600):
			expire(iPlayer, 1)
			
		# third goal: control 65% of the Mediterranean by 1930 AD
		if isPossible(iPlayer, 2):
			iMediterranean, iTotalMediterranean = countControlledTiles(iPlayer, plots.rectangle(tMediterranean).without(lMediterraneanExceptions), False, True)
			fMediterranean = iMediterranean * 100.0 / iTotalMediterranean
			
			if fMediterranean >= 65.0:
				win(iPlayer, 2)
				
		if iGameTurn == year(1930):
			expire(iPlayer, 2)
			
	elif iCiv == iMongols:
	
		# first goal: control China by 1300 AD
		if isPossible(iPlayer, 0):
			if checkOwnedCiv(iPlayer, iChina):
				win(iPlayer, 0)
				
		if iGameTurn == year(1300):
			expire(iPlayer, 0)
			
		# second goal: raze 7 cities
		
		# third goal: control 12% of world territory by 1500 AD
		if isPossible(iPlayer, 2):
			if getLandPercent(iPlayer) >= 11.995:
				win(iPlayer, 2)
				
		if iGameTurn == year(1500):
			expire(iPlayer, 2)
					
	elif iCiv == iMughals:
	
		# first goal: build three Muslim Cathedrals by 1500 AD
		if iGameTurn == year(1500):
			expire(iPlayer, 0)
			
		# second goal: build the Red Fort, Shalimar Gardens and the Taj Mahal by 1660 AD
		if iGameTurn == year(1660):
			expire(iPlayer, 1)
			
		# third goal: have more than 50000 culture in 1750 AD
		if iGameTurn == year(1750):
			if pPlayer.countTotalCulture() >= turns(50000):
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
			
	elif iCiv == iAztecs:
		
		# first goal: make Tenochtitlan the largest city in the world in 1520 AD
		if iGameTurn == year(1520):
			if isBestCity(iPlayer, (18, 37), cityPopulation):
				win(iPlayer, 0)
			else:
				lose(iPlayer, 0)
				
		# second goal: build six step pyramids and sacrificial altars by 1650 AD
		if isPossible(iPlayer, 1):
			if getNumBuildings(iPlayer, unique_building(iPlayer, iPaganTemple)) >= 6 and getNumBuildings(iPlayer, iSacrificialAltar) >= 6:
				win(iPlayer, 1)
		
		if iGameTurn == year(1650):
			expire(iPlayer, 1)
			
		# third goal: enslave 20 old world units
		if isPossible(iPlayer, 2):
			if data.iAztecSlaves >= 20:
				win(iPlayer, 2)
				
	elif iCiv == iOttomans:
	
		# first goal: have four non-obsolete wonders in your capital in 1550 AD
		if iGameTurn == year(1550):
			capital = pPlayer.getCapitalCity()
			if countCityWonders(iPlayer, (capital.getX(), capital.getY()), False) >= 4:
				win(iPlayer, 0)
			else:
				lose(iPlayer, 0)
				
		# second goal: control the Eastern Mediterranean, the Black Sea, Cairo, Mecca, Baghdad and Vienna by 1700 AD
		if isPossible(iPlayer, 1):
			bEasternMediterranean = isCultureControlled(iPlayer, lEasternMediterranean)
			bBlackSea = isCultureControlled(iPlayer, lBlackSea)
			bCairo = controlsCity(iPlayer, tCairo)
			bMecca = controlsCity(iPlayer, tMecca)
			bBaghdad = controlsCity(iPlayer, tBaghdad)
			bVienna = controlsCity(iPlayer, tVienna)
			
			if bEasternMediterranean and bBlackSea and bCairo and bMecca and bBaghdad and bVienna:
				win(iPlayer, 1)
				
		if iGameTurn == year(1700):
			expire(iPlayer, 1)
			
		# third goal: have more culture than all European civilizations combined in 1800 AD
		if iGameTurn == year(1800):
			if pPlayer.countTotalCulture() > getTotalCulture(dCivGroups[iCivGroupEurope]):
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
				
	elif iCiv == iThailand:
	
		# first goal: have open borders with 10 civilizations by 1650 AD
		if isPossible(iPlayer, 0):
			if countOpenBorders(iPlayer) >= 10:
				win(iPlayer, 0)
				
		if iGameTurn == year(1650):
			expire(iPlayer, 0)
			
		# second goal: make Ayutthaya the most populous city in the world in 1700 AD
		if iGameTurn == year(1700):
			if isBestCity(iPlayer, (101, 33), cityPopulation) or isBestCity(iPlayer, (102, 33), cityPopulation):
				win(iPlayer, 1)
			else:
				lose(iPlayer, 1)
				
		# third goal: allow no foreign powers in South Asia in 1900 AD
		if iGameTurn == year(1900):
			if isAreaOnlyCivs(plots.rectangle(tSouthAsia), lSouthAsianCivs):
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
				
	elif iCiv == iCongo:
	
		# first goal: acquire 15% of the votes in the Apostolic Palace by 1650 AD
		if isPossible(iPlayer, 0):
			if getApostolicVotePercent(iPlayer) >= 15.0:
				win(iPlayer, 0)
				
		if iGameTurn == year(1650):
			expire(iPlayer, 0)
			
		# second goal: gain 1000 gold through slave trade by 1800 AD
		if iGameTurn == year(1800):
			expire(iPlayer, 1)
			
		# third goal: enter the Industrial Era before anyone enters the Modern Era
	
	elif iCiv == iIran:
		
		# first goal: have open borders with 6 European civilizations in 1650
		if iGameTurn == year(1650):
			if countOpenBorders(iPlayer, dCivGroups[iCivGroupEurope]) >= 6:
				win(iPlayer, 0)
			else:
				lose(iPlayer, 0)
				
		# second goal: control Mesopotamia, Transoxania and Northwest India in 1750 AD
		if iGameTurn == year(1750):
			bMesopotamia = isControlled(iPlayer, plots.rectangle(tSafavidMesopotamia))
			bTransoxania = isControlled(iPlayer, plots.rectangle(tTransoxiana))
			bNWIndia = isControlled(iPlayer, plots.rectangle(tNorthWestIndia).without(lNorthWestIndiaExceptions))
			if bMesopotamia and bTransoxania and bNWIndia:
				win(iPlayer, 1)
			else:
				lose(iPlayer, 1)
				
		# third goal: have a city with 20000 culture in 1800 AD
		if iGameTurn == year(1800):
			mostCulturedCity = getMostCulturedCity(iPlayer)
			if mostCulturedCity.getCulture(iPlayer) >= turns(20000):
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
		
	elif iCiv == iNetherlands:
	
		# first goal: settle three great merchants in Amsterdam by 1745 AD
		if isPossible(iPlayer, 0):
			if countCitySpecialists(iPlayer, plots.capital(iNetherlands), iSpecialistGreatMerchant) >= 3:
				win(iPlayer, 0)
				
		if iGameTurn == year(1745):
			expire(iPlayer, 0)
			
		# second goal: conquer four European colonies by 1745 AD
		if iGameTurn == year(1745):
			expire(iPlayer, 1)
			
		# third goal: secure or get by trade seven spice resources by 1775 AD
		if isPossible(iPlayer, 2):
			if pPlayer.getNumAvailableBonuses(iSpices) >= 7:
				win(iPlayer, 2)
				
		if iGameTurn == year(1775):
			expire(iPlayer, 2)
			
	elif iCiv == iGermany:
	
		# first goal: settle seven great people in Berlin in 1900 AD
		if iGameTurn == year(1900):
			iCount = 0
			for iSpecialist in lGreatPeople:
				iCount += countCitySpecialists(iPlayer, plots.capital(iGermany), iSpecialist)
			if iCount >= 7:
				win(iPlayer, 0)
			else:
				lose(iPlayer, 0)
				
		# second goal: control Italy, France, England, Scandinavia and Russia
		if iGameTurn == year(1940):
			bItaly = checkOwnedCiv(iPlayer, iItaly)
			bFrance = checkOwnedCiv(iPlayer, iFrance)
			bEngland = checkOwnedCiv(iPlayer, iEngland)
			bScandinavia = checkOwnedCiv(iPlayer, iVikings)
			bRussia = checkOwnedCiv(iPlayer, iRussia)
			if bItaly and bFrance and bEngland and bScandinavia and bRussia:
				win(iPlayer, 1)
			else:
				lose(iPlayer, 0)
				
		# third goal: be the first to complete the tech tree
		
	elif iCiv == iAmerica:
	
		# first goal: allow no European colonies in North America, Central America and the Caribbean and control or vassalize Mexico in 1930 AD
		if iGameTurn == year(1900):
			if isAreaFreeOfCivs(plots.rectangle(tNorthCentralAmerica), dCivGroups[iCivGroupEurope]) and isControlledOrVassalized(iPlayer, plots.core(iMexico)):
				win(iPlayer, 0)
			else:
				lose(iPlayer, 0)
				
		# second goal: build the Statue of Liberty, the Brooklyn Bridge, the Empire State Building, the Golden Gate Bridge, the Pentagon and the United Nations by 1950 AD
		if iGameTurn == year(1950):
			expire(iPlayer, 1)
			
		# third goal: control 75% of the world's commerce output and military power between you, your vassals and allies by 1990 AD
		if isPossible(iPlayer, 2):
			if calculateAlliedCommercePercent(iPlayer) >= 75.0 and calculateAlliedPowerPercent(iPlayer) >= 75.0:
				win(iPlayer, 2)
				
		if iGameTurn == year(1990):
			expire(iPlayer, 2)
			
	elif iCiv == iArgentina:
	
		# first goal: experience two golden ages by 1930 AD
		if isPossible(iPlayer, 0):
			if data.iArgentineGoldenAgeTurns >= turns(16):
				win(iPlayer, 0)
				
		if iGameTurn == year(1930):
			expire(iPlayer, 0)
			
		# second goal: have lengendary culture in Buenos Aires by 1960 AD
		if isPossible(iPlayer, 1):
			if getCityCulture(iPlayer, plots.capital(iArgentina)) >= turns(50000):
				win(iPlayer, 1)
				
		if iGameTurn == year(1960):
			expire(iPlayer, 1)
			
		# third goal: experience six golden ages by 2000 AD
		if isPossible(iPlayer, 2):
			if data.iArgentineGoldenAgeTurns >= turns(48):
				win(iPlayer, 2)
				
		if iGameTurn == year(2000):
			expire(iPlayer, 2)
			
		if pPlayer.isGoldenAge() and not pPlayer.isAnarchy():
			data.iArgentineGoldenAgeTurns += 1
	
	elif iCiv == iMexico:
		
		# first goal: build three cathedrals of your state religion by 1880 AD
		if iGameTurn == year(1880):
			expire(iPlayer, 0)
			
		# second goal: create three great generals by 1940 AD
		if iGameTurn == year(1940):
			expire(iPlayer, 1)
			
		# third goal: make Mexico City the largest city in the world in 1960 AD
		if iGameTurn == year(1960):
			if isBestCity(iPlayer, (18, 37), cityPopulation):
				win(iPlayer, 2)
			else:
				lose(iPlayer, 2)
				
	elif iCiv == iColombia:
		
		# first goal: allow no European civilizations in Peru, Gran Colombia, the Guayanas and the Caribbean in 1870 AD
		if iGameTurn == year(1870):
			bPeru = isAreaFreeOfCivs(plots.rectangle(tPeru), dCivGroups[iCivGroupEurope])
			bGranColombia = isAreaFreeOfCivs(plots.rectangle(tGranColombia), dCivGroups[iCivGroupEurope])
			bGuayanas = isAreaFreeOfCivs(plots.rectangle(tGuayanas), dCivGroups[iCivGroupEurope])
			bCaribbean = isAreaFreeOfCivs(plots.rectangle(tCaribbean), dCivGroups[iCivGroupEurope])
			if bPeru and bGranColombia and bGuayanas and bCaribbean:
				win(iPlayer, 0)
			else:
				lose(iPlayer, 0)
				
		# second goal: control South America in 1920 AD
		if iGameTurn == year(1920):
			if isControlled(iPlayer, plots.rectangle(tSouthAmerica).without(lSouthAmericaExceptions)):
				win(iPlayer, 1)
			else:
				lose(iPlayer, 1)
		
		# third goal: acquire 3000 gold by selling resources by 1950 AD
		if isPossible(iPlayer, 2):
			iTradeGold = 0
			
			for iLoopPlayer in players.major():
				iTradeGold += pPlayer.getGoldPerTurnByPlayer(iLoopPlayer)
			
			data.iColombianTradeGold += iTradeGold
			
			if data.iColombianTradeGold >= turns(3000):
				win(iPlayer, 2)
				
		if iGameTurn == year(1950):
			expire(iPlayer, 2)
			
	elif iCiv == iBrazil:
	
		# first goal: control 8 slave plantations and 4 pastures in 1880 AD
		if iGameTurn == year(1880):
			if countImprovements(iPlayer, iSlavePlantation) >= 8 and countImprovements(iPlayer, iPasture) >= 4:
				win(iPlayer, 0)
			else:
				lose(iPlayer, 0)
				
		# second goal: build Wembley, Cristo Redentor and the Three Gorges Dam
		
		# third goal: control 20 forest preserves and have a national park in your capital by 1950 AD
		if isPossible(iPlayer, 2):
			if countImprovements(iPlayer, iForestPreserve) >= 20 and pPlayer.getCapitalCity() and pPlayer.getCapitalCity().isHasRealBuilding(iNationalPark):
				win(iPlayer, 2)
				
		if iGameTurn == year(1950):
			expire(iPlayer, 2)
				
	elif iCiv == iCanada:
	
		# first goal: connect your capital to an Atlantic and a Pacific port by 1920 AD
		if isPossible(iPlayer, 0):
			capital = pPlayer.getCapitalCity()
			bAtlantic = isConnectedByRailroad(iPlayer, capital, lAtlanticCoast)
			bPacific = isConnectedByRailroad(iPlayer, capital, lPacificCoast)
			if bAtlantic and bPacific:
				win(iPlayer, 0)
				
		if iGameTurn == year(1920):
			expire(iPlayer, 0)
			
		# second goal: control all cities and 90% of the territory in Canada without ever conquering a city by 1950 AD
		if isPossible(iPlayer, 1):
			iEast, iTotalEast = countControlledTiles(iPlayer, plots.rectangle(tCanadaEast).without(lCanadaEastExceptions), False)
			iWest, iTotalWest = countControlledTiles(iPlayer, plots.rectangle(tCanadaWest).without(lCanadaWestExceptions), False)
			
			fCanada = (iEast + iWest) * 100.0 / (iTotalEast + iTotalWest)
			
			bAllCitiesEast = controlsAllCities(iPlayer, plots.rectangle(tCanadaEast).without(lCanadaEastExceptions))
			bAllCitiesWest = controlsAllCities(iPlayer, plots.rectangle(tCanadaWest).without(lCanadaWestExceptions))
			
			if fCanada >= 90.0 and bAllCitiesEast and bAllCitiesWest:
				win(iPlayer, 1)
				
		if iGameTurn == year(1950):
			expire(iPlayer, 1)
			
		# third goal: end twelve wars through diplomacy by 2000 AD
		if iGameTurn == year(2000):
			expire(iPlayer, 2)
			
			
	# check religious victory (human only)
	if player(iPlayer).isHuman():
		iVictoryType = getReligiousVictoryType(iPlayer)
		
		if iVictoryType == iCatholicism:
			if game.getSecretaryGeneral(1) == iPlayer:
				data.iPopeTurns += 1
				
		elif iVictoryType == iHinduism:
			if pPlayer.isGoldenAge():
				data.iHinduGoldenAgeTurns += 1
				
		elif iVictoryType == iBuddhism:
			if isAtPeace(iPlayer):
				data.iBuddhistPeaceTurns += 1
				
			if isHappiest(iPlayer):
				data.iBuddhistHappinessTurns += 1
				
		elif iVictoryType == iTaoism:
			if isHealthiest(iPlayer):
				data.iTaoistHealthTurns += 1
				
		elif iVictoryType == iVictoryPaganism:
			if 2 * countReligionCities(iPlayer) > pPlayer.getNumCities():
				data.bPolytheismNeverReligion = False
				
			if infos.civ(civ(iPlayer)).getPaganReligionName(0) == "Vedism":
				for city in cities.owner(iPlayer):
					if city.isWeLoveTheKingDay():
						data.iVedicHappiness += 1
				
		if checkReligiousGoals(iPlayer):
			game.setWinner(iPlayer, 8)
			
def checkHistoricalVictory(iPlayer):
	pPlayer = player(iPlayer)
	
	if not data.players[iPlayer].bHistoricalGoldenAge:
		if countAchievedGoals(iPlayer) >= 2:	
			data.players[iPlayer].bHistoricalGoldenAge = True
			
			iGoldenAgeTurns = player(iPlayer).getGoldenAgeLength()
			if not player(iPlayer).isAnarchy(): iGoldenAgeTurns += 1
			
			player(iPlayer).changeGoldenAgeTurns(iGoldenAgeTurns)
			
			message(iPlayer, 'TXT_KEY_VICTORY_INTERMEDIATE', color=iPurple)
			
			if pPlayer.isHuman():
				for iLoopPlayer in players.major().alive().without(iPlayer):
					player(iLoopPlayer).AI_changeAttitudeExtra(iPlayer, -2)
			
	if game.getWinner() == -1:
		if countAchievedGoals(iPlayer) == 3:
			game.setWinner(iPlayer, 7)

@handler("cityBuilt")		
def onCityBuilt(city):
	iPlayer = city.getOwner()
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)

	if not game.isVictoryValid(7): return
	
	if is_minor(iPlayer): return
	
	# record first colony in the Americas for various UHVs
	if not data.isNewWorldColonized():
		if city.getRegionID() in lNorthAmerica + lSouthAmerica:
			if civ(iPlayer) not in dCivGroups[iCivGroupAmerica]:
				data.iFirstNewWorldColony = iPlayer
			
				# second Viking goal: found a city in America by 1100 AD
				iVikingPlayer = slot(iVikings)
				if isPossible(iVikingPlayer, 1):
					if iPlayer == iVikingPlayer:
						win(iVikingPlayer, 1)
					else:
						lose(iVikingPlayer, 1)
					
				# first Spanish goal: be the first to found a colony in America
				iSpainPlayer = slot(iSpain)
				if isPossible(iSpainPlayer, 0):
					if iPlayer == iSpainPlayer:
						win(iSpainPlayer, 0)
					else:
						lose(iSpainPlayer, 0)
				
	# first Polynesian goal: settle two of the following island groups by 800 AD: Hawaii, New Zealand, Marquesas, Easter Island
	# second Polynesian goal: control Hawaii, New Zealand, Marquesas and Easter Island by 1000 AD
	if iCiv == iPolynesia:
		iCount = 0
		if getNumCitiesInArea(iPlayer, plots.rectangle(tHawaii)) >= 1: iCount += 1
		if getNumCitiesInArea(iPlayer, plots.rectangle(tNewZealand)) >= 1: iCount += 1
		if getNumCitiesInArea(iPlayer, plots.rectangle(tMarquesas)) >= 1: iCount += 1
		if getNumCitiesInArea(iPlayer, plots.rectangle(tEasterIsland)) >= 1: iCount += 1
		
		if isPossible(iPlayer, 0):
			if iCount >= 2:
				win(iPlayer, 0)
				
		if isPossible(iPlayer, 1):
			if iCount >= 4:
				win(iPlayer, 1)
				
	# first Tibetan goal: acquire five cities by 1000 AD
	elif iCiv == iTibet:
		if isPossible(iPlayer, 0):
			if pPlayer.getNumCities() >= 5:
				win(iPlayer, 0)
					
	# first English goal: colonize every continent by 1730 AD
	elif iCiv == iEngland:
		if isPossible(iPlayer, 0):
			bNAmerica = getNumCitiesInRegions(iPlayer, lNorthAmerica) >= 5
			bSCAmerica = getNumCitiesInRegions(iPlayer, lSouthAmerica) >= 3
			bAfrica = getNumCitiesInRegions(iPlayer, lAfrica) >= 4
			bAsia = getNumCitiesInRegions(iPlayer, lAsia) >= 5
			bOceania = getNumCitiesInRegions(iPlayer, lOceania) >= 3
			if bNAmerica and bSCAmerica and bAfrica and bAsia and bOceania:
				win(iPlayer, 0)

@handler("cityAcquired")	
def onCityAcquired(iOwner, iPlayer, city, bConquest):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)

	iOwnerCiv = civ(iOwner)

	if not game.isVictoryValid(7): return
	
	# first Japanese goal: have an average city culture of 6000 by 1600 AD without ever losing a city
	if iOwnerCiv == iJapan:
		expire(iPlayer, 0)
	
	if not player(iPlayer).isHuman() and data.bIgnoreAI: return
				
	# first Tibetan goal: acquire five cities by 1000 AD
	if iCiv == iTibet:
		if isPossible(iPlayer, 0):
			if pPlayer.getNumCities() >= 5:
				win(iPlayer, 0)
					
	# first English goal: colonize every continent by 1730 AD
	elif iCiv == iEngland:
		if isPossible(iPlayer, 0):
			bNAmerica = getNumCitiesInRegions(iPlayer, lNorthAmerica) >= 5
			bSCAmerica = getNumCitiesInRegions(iPlayer, lSouthAmerica) >= 3
			bAfrica = getNumCitiesInRegions(iPlayer, lAfrica) >= 4
			bAsia = getNumCitiesInRegions(iPlayer, lAsia) >= 5
			bOceania = getNumCitiesInRegions(iPlayer, lOceania) >= 3
			if bNAmerica and bSCAmerica and bAfrica and bAsia and bOceania:
				win(iPlayer, 0)
				
	# second Dutch goal: conquer four European colonies by 1745 AD
	elif iCiv == iNetherlands:
		if isPossible(iPlayer, 1):
			if iOwnerCiv in dCivGroups[iCivGroupEurope]:
				bColony = city.getRegionID() not in lEurope
			
				if bColony and bConquest:
					data.iDutchColonies += 1
					if data.iDutchColonies >= 4:
						win(iPlayer, 1)
				
	# second Canadian goal: control all cities and 90% of the territory in Canada by 1950 AD without ever conquering a city
	elif iCiv == iCanada:
		if bConquest:
			expire(iPlayer, 1)

@handler("techAcquired")
def onTechAcquired(iTech, iTeam, iPlayer):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)

	if not game.isVictoryValid(7):
		return
	
	if is_minor(iPlayer):
		return
	
	if year() <= year(dSpawn[iCiv]):
		return
	
	iEra = infos.tech(iTech).getEra()
	
	# handle all "be the first to discover" goals
	if not isDiscovered(iTech):
		data.lFirstDiscovered[iTech] = iPlayer
		
		for iLoopCiv, (iGoal, lTechs) in dTechGoals.items():
			iLoopPlayer = slot(iLoopCiv)
			if not isPossible(iLoopPlayer, iGoal): continue
			
			if iTech in lTechs:
				if iPlayer != iLoopPlayer: lose(iLoopPlayer, iGoal)
				elif checkTechGoal(iLoopPlayer, lTechs): win(iLoopPlayer, iGoal)
				
		# third Japanese goal: be the first to discover ten Global and ten Digital technologies
		iJapanPlayer = slot(iJapan)
		if isPossible(iJapanPlayer, 2):
			if iEra in [iGlobal, iDigital]:
				if countFirstDiscovered(iPlayer, iGlobal) >= 8 and countFirstDiscovered(iPlayer, iDigital) >= 8:
					if iPlayer == iJapanPlayer:
						win(iJapanPlayer, 2)
					else:
						lose(iJapanPlayer, 2)
				if not isFirstDiscoveredPossible(iJapanPlayer, iGlobal, 8) or not isFirstDiscoveredPossible(iJapanPlayer, iDigital, 8):
					lose(iJapanPlayer, 2)
				
		# third English goal: be the first to discover ten Renaissance and ten Industrial technologies
		iEnglandPlayer = slot(iEngland)
		if isPossible(iEnglandPlayer, 2):
			if iEra in [iRenaissance, iIndustrial]:
				if countFirstDiscovered(iPlayer, iRenaissance) >= 8 and countFirstDiscovered(iPlayer, iIndustrial) >= 8:
					if iPlayer == iEnglandPlayer:
						win(iEnglandPlayer, 2)
					else:
						lose(iEnglandPlayer, 2)
				if not isFirstDiscoveredPossible(iEnglandPlayer, iRenaissance, 8) or not isFirstDiscoveredPossible(iEnglandPlayer, iIndustrial, 8):
					lose(iEnglandPlayer, 2)
				
		# third German goal: be the first to discover ten Industrial and ten Global technologies
		iGermanyPlayer = slot(iGermany)
		if isPossible(iGermanyPlayer, 2):
			if iEra in [iIndustrial, iGlobal]:
				if countFirstDiscovered(iPlayer, iIndustrial) >= 8 and countFirstDiscovered(iPlayer, iGlobal) >= 8:
					if iPlayer == iGermanyPlayer:
						win(iGermanyPlayer, 2)
					else:
						lose(iGermanyPlayer, 2)
				if not isFirstDiscoveredPossible(iGermanyPlayer, iIndustrial, 8) or not isFirstDiscoveredPossible(iGermanyPlayer, iGlobal, 8):
					lose(iGermanyPlayer, 2)
			
	# handle all "be the first to enter" goals
	if not isEntered(iEra):
		data.lFirstEntered[iEra] = iPlayer
		
		for iLoopCiv, (iGoal, lEras) in dEraGoals.items():
			iLoopPlayer = slot(iLoopCiv)
			if not isPossible(iLoopPlayer, iGoal): continue
			
			if iEra in lEras:
				if iPlayer != iLoopPlayer:
					lose(iLoopPlayer, iGoal)
				elif checkEraGoal(iLoopPlayer, lEras):
					win(iLoopPlayer, iGoal)
				
	# first Maya goal: discover Calendar by 200 AD
	if iCiv == iMaya:
		if isPossible(iPlayer, 0):
			if iTech == iCalendar:
				if team(iPlayer).isHasTech(iCalendar):
					win(iPlayer, 0)
				
	# third Congolese goal: enter the Industrial era before anyone enters the Modern era
	iCongoPlayer = slot(iCongo)
	if isPossible(iCongoPlayer, 2):
		if iEra == iIndustrial and iPlayer == iCongoPlayer:
			win(iCongoPlayer, 2)
		if iEra == iGlobal and iPlayer != iCongoPlayer:
			lose(iCongoPlayer, 2)
				
def checkTechGoal(iPlayer, lTechs):
	return all(data.lFirstDiscovered[iTech] == iPlayer for iTech in lTechs)
	
def checkEraGoal(iPlayer, lEras):
	return all(data.lFirstEntered[iEra] == iPlayer for iEra in lEras)

@handler("buildingBuilt")
def onBuildingBuilt(city, iBuilding):
	iPlayer = city.getOwner()
	iCiv = civ(iPlayer)

	if not game.isVictoryValid(7): return False
	
	# handle all "build wonders" goals
	if isWonder(iBuilding) and not isWonderBuilt(iBuilding):
		data.setWonderBuilder(iBuilding, iPlayer)
		
		for iLoopCiv, (iGoal, lWonders, bCanWin) in dWonderGoals.items():
			iLoopPlayer = slot(iLoopCiv)
			if iLoopPlayer < 0: continue
		
			if not isPossible(iLoopPlayer, iGoal): continue
			
			if iBuilding in lWonders:
				if iPlayer != iLoopPlayer: lose(iLoopPlayer, iGoal)
				elif bCanWin and checkWonderGoal(iLoopPlayer, lWonders): win(iLoopPlayer, iGoal)
				
	if not player(iPlayer).isHuman() and data.bIgnoreAI: return
	
	if not player(iPlayer).isAlive(): return
	
	# first Chinese goal: build two Confucian and Taoist Cathedrals by 1000 AD
	if iCiv == iChina:
		if isPossible(iPlayer, 0):
			if iBuilding in [iConfucianCathedral, iTaoistCathedral]:
				iConfucian = getNumBuildings(iPlayer, iConfucianCathedral)
				iTaoist = getNumBuildings(iPlayer, iTaoistCathedral)
				if iConfucian >= 2 and iTaoist >= 2:
					win(iPlayer, 0)
					
	# second Harappan goal: build three Baths, two Granaries and two Smokehouses by 1500 BC
	elif iCiv == iHarappa:
		if isPossible(iPlayer, 1):
			if iBuilding in [iReservoir, iGranary, iSmokehouse]:
				iNumBaths = getNumBuildings(iPlayer, iReservoir)
				iNumGranaries = getNumBuildings(iPlayer, iGranary)
				iNumSmokehouses = getNumBuildings(iPlayer, iSmokehouse)
				if iNumBaths >= 3 and iNumGranaries >= 2 and iNumSmokehouses >= 2:
					win(iPlayer, 1)
					
	# second Indian goal: build 20 temples by 700 AD
	elif iCiv == iIndia:
		if isPossible(iPlayer, 1):
			lTemples = [iTemple + i*4 for i in range(iNumReligions)]
			if iBuilding in lTemples:
				iCounter = 0
				for iGoalTemple in lTemples:
					iCounter += getNumBuildings(iPlayer, iGoalTemple)
				if iCounter >= 20:
					win(iPlayer, 1)
	
	# first Roman goal: build 6 Barracks, 5 Aqueducts, 4 Arenas and 3 Forums by 100 AD
	elif iCiv == iRome:
		if isPossible(iPlayer, 0):
			if iBuilding in [iBarracks, iAqueduct, iArena, iForum]:
				iNumBarracks = getNumBuildings(iPlayer, iBarracks)
				iNumAqueducts = getNumBuildings(iPlayer, iAqueduct)
				iNumArenas = getNumBuildings(iPlayer, iArena)
				iNumForums = getNumBuildings(iPlayer, iForum)
				if iNumBarracks >= 6 and iNumAqueducts >= 5 and iNumArenas >= 4 and iNumForums >= 3:
					win(iPlayer, 0)
					
	# first Korean goal: build a Confucian and a Buddhist Cathedral
	elif iCiv == iKorea:
		if isPossible(iPlayer, 0):
			if iBuilding in [iConfucianCathedral, iBuddhistCathedral]:
				bBuddhist = getNumBuildings(iPlayer, iBuddhistCathedral) > 0
				bConfucian = getNumBuildings(iPlayer, iConfucianCathedral) > 0
				if bBuddhist and bConfucian:
					win(iPlayer, 0)
					
	# third Polish goal: build a total of three Catholic, Orthodox and Protestant Cathedrals by 1600 AD
	elif iCiv == iPoland:
		if isPossible(iPlayer, 2):
			iCatholic = getNumBuildings(iPlayer, iCatholicCathedral)
			iOrthodox = getNumBuildings(iPlayer, iOrthodoxCathedral)
			iProtestant = getNumBuildings(iPlayer, iProtestantCathedral)
			if iCatholic + iOrthodox + iProtestant >= 3:
				win(iPlayer, 2)
				
	# second Aztec goal: build 6 pagan temples and sacrificial altars
	elif iCiv == iAztecs:
		if isPossible(iPlayer, 1):
			if iBuilding in [iPaganTemple, iSacrificialAltar]:
				iTemples = getNumBuildings(iPlayer, iPaganTemple)
				iAltars = getNumBuildings(iPlayer, iSacrificialAltar)
				if iTemples >= 6 and iAltars >= 6:
					win(iPlayer, 1)
	
	# first Mexican goal: build three cathedrals of your state religion by 1880 AD	
	elif iCiv == iMexico:				
		if isPossible(iPlayer, 0):
			iStateReligion = pPlayer.getStateReligion()
			if iStateReligion >= 0:
				iStateReligionCathedral = iCathedral + 4 * iStateReligion
				if iBuilding == iStateReligionCathedral:
					if getNumBuildings(iPlayer, iStateReligionCathedral) >= 3:
						win(iPlayer, 0)
	
	# first Mughal goal: build three Islamic Mosques by 1500 AD
	elif iCiv == iMughals:
		if isPossible(iPlayer, 0):
			if iBuilding == iIslamicCathedral:
				if getNumBuildings(iPlayer, iIslamicCathedral) >= 3:
					win(iPlayer, 0)
		
	# first Incan goal: build 5 tambos and a road along the Andean coast by 1500 AD
	elif iCiv == iInca:
		if isPossible(iPlayer, 0):
			if iBuilding == iTambo:
				if isRoad(iPlayer, lAndeanCoast) and getNumBuildings(iPlayer, iTambo) >= 5:
					win(iPlayer, 0)
				
def checkWonderGoal(iPlayer, lWonders):
	return all(data.getWonderBuilder(iWonder) == iPlayer for iWonder in lWonders)

@handler("religionFounded")
def onReligionFounded(iReligion, iPlayer):

	if not game.isVictoryValid(7): return
	
	# handle all "be the first to found" goals
	if not isFounded(iReligion):
		data.lReligionFounder[iReligion] = iPlayer
		
		for iLoopCiv, (iGoal, lReligion) in dReligionGoals.items():
			iLoopPlayer = slot(iLoopCiv)
			if not isPossible(iLoopPlayer, iGoal): continue
			
			if iReligion in lReligions:
				if iPlayer != iLoopPlayer:
					lose(iLoopPlayer, iGoal)
				elif checkReligionGoal(iLoopPlayer, lReligions):
					win(iLoopPlayer, iGoal)
				
def checkReligionGoal(iPlayer, lReligions):
	return all(data.lReligionFounder[iReligion] == iPlayer for iReligion in lReligion)

@handler("projectBuilt")
def onProjectBuilt(iPlayer, iProject):
	if not game.isVictoryValid(7): return
	
	# second Russian goal: be the first civilization to complete the Manhattan Project and the Apollo Program
	iRussiaPlayer = slot(iRussia)
	if isPossible(iRussiaPlayer, 1):
		if iProject in [iLunarLanding, iManhattanProject]:
			if iPlayer == iRussiaPlayer:
				bApolloProgram = iProject == iLunarLanding or team(iRussiaPlayer).getProjectCount(iLunarLanding) > 0
				bManhattanProject = iProject == iManhattanProject or team(iRussiaPlayer).getProjectCount(iManhattanProject) > 0
				if bApolloProgram and bManhattanProject:
					win(iRussiaPlayer, 1)
			else:
				lose(iRussiaPlayer, 1)

@handler("combatResult")				
def onCombatResult(pWinningUnit, pLosingUnit):
	iWinningPlayer = pWinningUnit.getOwner()
	iLosingPlayer = pLosingUnit.getOwner()
	
	iWinningCiv = civ(iWinningPlayer)
	
	if not player(iWinningPlayer).isHuman() and data.bIgnoreAI: return
	
	pLosingUnitInfo = infos.unit(pLosingUnit)
	iDomainSea = DomainTypes.DOMAIN_SEA
	
	# second English goal: control a total of 25 frigates and ships of the line and sink 50 ships in 1800 AD
	if iWinningCiv == iEngland:
		if isPossible(iWinningPlayer, 1):
			if pLosingUnitInfo.getDomainType() == iDomainSea:
				data.iEnglishSinks += 1
				
	# third Korean goal: sink 20 enemy ships
	elif iWinningCiv == iKorea:
		if isPossible(iWinningPlayer, 2):
			if pLosingUnitInfo.getDomainType() == iDomainSea:
				data.iKoreanSinks += 1
				if data.iKoreanSinks >= 20:
					win(iWinningPlayer, 2)

@handler("greatPersonBorn")					
def onGreatPersonBorn(unit, iPlayer):
	iUnitType = base_unit(unit)
	pUnitInfo = infos.unit(iUnitType)
	
	iCiv = civ(iPlayer)
	
	if not isGreatPersonTypeBorn(iUnitType):
		data.lFirstGreatPeople[lGreatPeopleUnits.index(iUnitType)] = iPlayer
	
	# second Mexican goal: get three great generals by 1940 AD
	if iCiv == iMexico:
		if isPossible(iPlayer, 1):
			if pUnitInfo.getGreatPeoples(iSpecialistGreatGeneral):
				data.iMexicanGreatGenerals += 1
				
				if data.iMexicanGreatGenerals >= 3:
					win(iPlayer, 1)

@handler("unitPillage")
def onUnitPillage(unit, iImprovement, iRoute, iPlayer, iGold):
	if iImprovement < 0 or iGold >= 1000: return
	
	iCiv = civ(iPlayer)

	# third Viking goal: acquire 3000 gold by pillaging, conquering cities and sinking ships by 1500 AD
	if iCiv == iVikings:
		if isPossible(iPlayer, 2):
			data.iVikingGold += iGold
			
	# first Turkic goal: pillage 20 improvements by 900 AD
	elif iCiv == iTurks:
		if isPossible(iPlayer, 0):
			data.iTurkicPillages += 1
	
	# third Moorish goal: acquire 3000 gold through piracy by 1650 AD
	elif iCiv == iMoors:
		if isPossible(iPlayer, 2) and unit.getUnitType() == iCorsair:
			data.iMoorishGold += iGold

@handler("cityCaptureGold")
def onCityCaptureGold(city, iPlayer, iGold):
	# third Viking goal: acquire 3000 gold by pillaging, conquering cities and sinking ships by 1500 AD
	if civ(iPlayer) == iVikings:
		if isPossible(iPlayer, 2):
			data.iVikingGold += iGold

@handler("playerGoldTrade")
def onPlayerGoldTrade(iFrom, iTo, iGold):
	# third Tamil goal: acquire 4000 gold by trade by 1200 AD
	if civ(iTo) == iTamils:
		if isPossible(iTo, 2):
			data.iTamilTradeGold += iGold * 100

@handler("playerSlaveTrade")
def onPlayerSlaveTrade(iPlayer, iGold):
	# second Congolese goal: gain 1000 gold through slave trade by 1800 AD
	if civ(iPlayer) == iCongo:
		if isPossible(iPlayer, 1):
			data.iCongoSlaveCounter += iGold
			if data.iCongoSlaveCounter >= scale(1000):
				win(iPlayer, 1)

@handler("tradeMission")
def onTradeMission(iUnit, iPlayer, iX, iY, iGold):
	iCiv = civ(iPlayer)

	# third Tamil goal: acquire 4000 gold by trade by 1200 AD
	if iCiv == iTamils:
		data.iTamilTradeGold += iGold * 100
		
	# first Mande goal: conduct a trade mission in your state religion's holy city by 1350 AD
	elif iCiv == iMali:
		if isPossible(iPlayer, 0):
			iStateReligion = player(iPlayer).getStateReligion()
			if iStateReligion != -1:
				pHolyCity = game.getHolyCity(iStateReligion)
				if location(pHolyCity) == (iX, iY):
					win(iPlayer, 0)

@handler("peaceBrokered")
def onPeaceBrokered(iBroker, iPlayer1, iPlayer2):
	iBrokerCiv = civ(iBroker)

	# third Canadian goal: end twelve wars through diplomacy by 2000 AD
	if iBrokerCiv == iCanada:
		if isPossible(iBroker, 2):
			data.iCanadianPeaceDeals += 1
			if data.iCanadianPeaceDeals >= 12:
				win(iBroker, 2)

@handler("blockade")
def onBlockade(iPlayer, iGold):
	iCiv = civ(iPlayer)

	# third Moorish goal: acquire 3000 gold through piracy by 1650 AD
	if iCiv == iMoors:
		if isPossible(iPlayer, 2):
			data.iMoorishGold += iGold

@handler("firstContact")			
def onFirstContact(iPlayer, iHasMetPlayer):
	# third Maya goal: make contact with a European civilization before they have discovered America
	iMayaPlayer = slot(iMaya)
	if isPossible(iMayaPlayer, 2):
		if iMayaPlayer in [iPlayer, iHasMetPlayer]:
			if iPlayer == iMayaPlayer and civ(iHasMetPlayer) in dCivGroups[iCivGroupEurope]:
				iEuropean = iHasMetPlayer
			elif iHasMetPlayer == iMayaPlayer and civ(iPlayer) in dCivGroups[iCivGroupEurope]:
				iEuropean = iPlayer
			else:
				return
			
			for plot in plots.start(tNorthAmerica[0]).end(tNorthAmerica[1][0]+2, tNorthAmerica[1][1]) + plots.start(tSouthCentralAmerica[0]).end(tSouthCentralAmerica[1][0]+2, tSouthCentralAmerica[1][1]):
				if plot.isRevealed(iEuropean, False) and not plot.isWater():
					lose(iMayaPlayer, 2)
					return

@handler("playerChangeStateReligion")					
def onPlayerChangeStateReligion(iPlayer, iStateReligion):
	iCiv = civ(iPlayer)

	# second Ethiopian goal: convert to Orthodoxy five turns after it is founded
	if iCiv == iEthiopia:
		if iStateReligion == iOrthodoxy:
			if game.isReligionFounded(iOrthodoxy):
				if turn() <= game.getReligionGameTurnFounded(iOrthodoxy) + turns(5):
					data.bEthiopiaConverted = True
			
def checkReligiousGoals(iPlayer):
	return all(checkReligiousGoal(iPlayer, i) == 1 for i in range(3))
	
def checkReligiousGoal(iPlayer, iGoal):
	pPlayer = player(iPlayer)
	iVictoryType = getReligiousVictoryType(iPlayer)
	
	if iVictoryType == -1: return -1
	
	elif iVictoryType == iJudaism:
	
		# first Jewish goal: have a total of 15 Great Prophets, Scientists and Statesmen in Jewish cities
		if iGoal == 0:
			iProphets = countReligionSpecialists(iJudaism, iSpecialistGreatProphet)
			iScientists = countReligionSpecialists(iJudaism, iSpecialistGreatScientist)
			iStatesmen = countReligionSpecialists(iJudaism, iSpecialistGreatStatesman)
			if iProphets + iScientists + iStatesmen >= 15: return 1
		
		# second Jewish goal: have legendary culture in the Jewish holy city
		elif iGoal == 1:
			pHolyCity = game.getHolyCity(iJudaism)
			if pHolyCity.getOwner() == iPlayer and pHolyCity.getCultureLevel() >= 6: return 1
			
		# third Jewish goal: have friendly relations with six civilizations with Jewish minorities
		elif iGoal == 2:
			iFriendlyRelations = countPlayersWithAttitudeAndReligion(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY, iJudaism)
			if iFriendlyRelations >= 6: return 1
			
	elif iVictoryType == iOrthodoxy:
	
		# first Orthodox goal: build four Orthodox cathedrals
		if iGoal == 0:
			if getNumBuildings(iPlayer, iOrthodoxCathedral) >= 4: return 1
			
		# second Orthodox goal: make sure the five most cultured cities in the world are Orthodox
		elif iGoal == 1:
			if countBestCitiesReligion(iOrthodoxy, cityCulture, 5) >= 5: return 1
			
		# third Orthodox goal: make sure there are no Catholic civilizations in the world
		elif iGoal == 2:
			if countReligionPlayers(iCatholicism)[0] == 0: return 1
			
	elif iVictoryType == iCatholicism:
	
		# first Catholic goal: be pope for 100 turns
		if iGoal == 0:
			if data.iPopeTurns >= turns(100): return 1
			
		# second Catholic goal: control the Catholic shrine and make sure 12 great prophets are settled in Catholic civilizations
		elif iGoal == 1:
			bShrine = getNumBuildings(iPlayer, iCatholicShrine) > 0
			iSaints = countReligionSpecialists(iCatholicism, iSpecialistGreatProphet)
			
			if bShrine and iSaints >= 12: return 1
			
		# third Catholic goal: make sure 50% of world territory is controlled by Catholic civilizations
		elif iGoal == 2:
			if getReligiousLand(iCatholicism) >= 50.0: return 1
	
	elif iVictoryType == iProtestantism:
		
		# first Protestant goal: be first to discover Civil Liberties, Constitution and Economics
		if iGoal == 0:
			lProtestantTechs = [iCivilLiberties, iSocialContract, iEconomics]
			if checkTechGoal(iPlayer, lProtestantTechs): return 1
			elif data.lFirstDiscovered[iCivilLiberties] not in [iPlayer, -1] or data.lFirstDiscovered[iSocialContract] not in [iPlayer, -1] or data.lFirstDiscovered[iEconomics] not in [iPlayer, -1]: return 0
			
		# second Protestant goal: make sure five great merchants and great engineers are settled in Protestant civilizations
		elif iGoal == 1:
			iEngineers = countReligionSpecialists(iProtestantism, iSpecialistGreatEngineer)
			iMerchants = countReligionSpecialists(iProtestantism, iSpecialistGreatMerchant)
			if iEngineers >= 5 and iMerchants >= 5: return 1
			
		# third Protestant goal: make sure at least half of all civilizations are Protestant or Secular
		elif iGoal == 2:
			iProtestantCivs, iTotal = countReligionPlayers(iProtestantism)
			iSecularCivs, iTotal = countCivicPlayers(iSecularism)
			
			if 2 * (iProtestantCivs + iSecularCivs) >= iTotal: return 1
			
	elif iVictoryType == iIslam:
	
		# first Muslim goal: spread Islam to 40%
		if iGoal == 0:
			fReligionPercent = game.calculateReligionPercent(iIslam)
			if fReligionPercent >= 40.0: return 1
			
		# second Muslim goal: settle seven great people in the Muslim holy city
		elif iGoal == 1:
			iCount = 0
			pHolyCity = game.getHolyCity(iIslam)
			for iGreatPerson in lGreatPeople:
				iCount += pHolyCity.getFreeSpecialistCount(iGreatPerson)
			if iCount >= 7: return 1
			
		# third Muslim goal: control five shrines
		elif iGoal == 2:
			iCount = 0
			for iReligion in range(iNumReligions):
				iCount += getNumBuildings(iPlayer, iShrine + 4*iReligion)
			if iCount >= 5: return 1
			
	elif iVictoryType == iHinduism:
	
		# first Hindu goal: settle five different great people in the Hindu holy city
		if iGoal == 0:
			iCount = 0
			pHolyCity = game.getHolyCity(iHinduism)
			for iGreatPerson in lGreatPeople:
				if pHolyCity.getFreeSpecialistCount(iGreatPerson) > 0:
					iCount += 1
			if iCount >= 5: return 1
		
		# second Hindu goal: experience 24 turns of golden age
		elif iGoal == 1:
			if data.iHinduGoldenAgeTurns >= turns(24): return 1
			
		# third Hindu goal: make sure the five largest cities in the world are Hindu
		elif iGoal == 2:
			if countBestCitiesReligion(iHinduism, cityPopulation, 5) >= 5: return 1
			
	elif iVictoryType == iBuddhism:
	
		# first Buddhist goal: be at peace for 100 turns
		if iGoal == 0:
			if data.iBuddhistPeaceTurns >= turns(100): return 1
			
		# second Buddhist goal: have the highest approval rating for 100 turns
		elif iGoal == 1:
			if data.iBuddhistHappinessTurns >= turns(100): return 1
			
		# third Buddhist goal: have cautious or better relations with all civilizations in the world
		elif iGoal == 2:
			if countGoodRelationPlayers(iPlayer, AttitudeTypes.ATTITUDE_CAUTIOUS) >= countLivingPlayers()-1: return 1
			
	elif iVictoryType == iConfucianism:
	
		# first Confucian goal: have friendly relations with five civilizations
		if iGoal == 0:
			if countGoodRelationPlayers(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY) >= 5: return 1
			
		# second Confucian goal: have five wonders in the Confucian holy city
		elif iGoal == 1:
			pHolyCity = game.getHolyCity(iConfucianism)
			if countCityWonders(iPlayer, (pHolyCity.getX(), pHolyCity.getY()), True) >= 5: return 1
			
		# third Confucian goal: control an army of 200 non-obsolete melee or gunpowder units
		elif iGoal == 2:
			iUnitCombatMelee = infos.type('UNITCOMBAT_MELEE')
			iUnitCombatGunpowder = infos.type('UNITCOMBAT_GUN')
			if countUnitsOfType(iPlayer, [iUnitCombatMelee, iUnitCombatGunpowder]) >= 200: return 1
			
	elif iVictoryType == iTaoism:
	
		# first Taoist goal: have the highest life expectancy in the world for 100 turns
		if iGoal == 0:
			if data.iTaoistHealthTurns >= turns(100): return 1
			
		# second Taoist goal: control the Confucian and Taoist shrine and combine their income to 40 gold
		elif iGoal == 1:
			iConfucianIncome = calculateShrineIncome(iPlayer, iConfucianism)
			iTaoistIncome = calculateShrineIncome(iPlayer, iTaoism)
			if getNumBuildings(iPlayer, iConfucianShrine) > 0 and getNumBuildings(iPlayer, iTaoistShrine) > 0 and iConfucianIncome + iTaoistIncome >= 40: return 1
			
		# third Taoist goal: have legendary culture in the Tao holy city
		elif iGoal == 2:
			pHolyCity = game.getHolyCity(iTaoism)
			if pHolyCity.getOwner() == iPlayer and pHolyCity.getCultureLevel() >= 6: return 1
		
	elif iVictoryType == iZoroastrianism:

		# first Zoroastrian goal: acquire six incense resources
		if iGoal == 0:
			if pPlayer.getNumAvailableBonuses(iIncense) >= 6: return 1
			
		# second Zoroastrian goal: spread Zoroastrianism to 10%
		if iGoal == 1:
			fReligionPercent = game.calculateReligionPercent(iZoroastrianism)
			if fReligionPercent >= 10.0: return 1
			
		# third Zoroastrian goal: have legendary culture in the Zoroastrian holy city
		elif iGoal == 2:
			pHolyCity = game.getHolyCity(iZoroastrianism)
			if pHolyCity.getOwner() == iPlayer and pHolyCity.getCultureLevel() >= 6: return 1
			
	elif iVictoryType == iVictoryPaganism:
	
		# first Pagan goal: make sure there are 15 pagan temples in the world
		if iGoal == 0:
			if countWorldBuildings(iPaganTemple) >= 15: return 1
			
		# second Pagan goal: depends on Pagan religion
		elif iGoal == 1:
			paganReligion = infos.civ(pPlayer).getPaganReligionName(0)
			
			# Anunnaki: have more wonders in your capital than any other city in the world
			if paganReligion == "Anunnaki":
				capital = pPlayer.getCapitalCity()
				
				if capital and isBestCity(iPlayer, (capital.getX(), capital.getY()), cityWonders):
					return 1
					
			# Asatru: have five units of level five
			elif paganReligion == "Asatru":
				if countUnitsOfLevel(iPlayer, 5) >= 5:
					return 1
					
			# Atua: acquire four pearl resources and 50 Ocean tiles
			elif paganReligion == "Atua":
				if pPlayer.getNumAvailableBonuses(iPearls) >= 4 and countControlledTerrain(iPlayer, iOcean) >= 50:
					return 1
			
			# Baalism: make your capital the city with the highest trade income in the world
			elif paganReligion == "Baalism":
				capital = pPlayer.getCapitalCity()
				
				if capital and isBestCity(iPlayer, (capital.getX(), capital.getY()), cityTradeIncome):
					return 1
			
			# Bon: control 50 peaks
			elif paganReligion == "Bon":
				if countControlledPeaks(iPlayer) >= 50:
					return 1
					
			# Druidism: control 20 unimproved Forest or Marsh tiles
			elif paganReligion == "Druidism":
				if countControlledFeatures(iPlayer, iForest, -1) + countControlledFeatures(iPlayer, iMud, -1) >= 20:
					return 1
					
			# Inti: have more gold in your treasury than the rest of the world combined
			elif paganReligion == "Inti":
				if 2 * pPlayer.getGold() >= getGlobalTreasury():
					return 1
					
			# Mazdaism: acquire six incense resources
			elif paganReligion == "Mazdaism":
				if pPlayer.getNumAvailableBonuses(iIncense) >= 6:
					return 1
					
			# Olympianism: control ten wonders that require no state religion
			elif paganReligion == "Olympianism":
				if countReligionWonders(iPlayer, -1) >= 10:
					return 1
					
			# Pesedjet: be the first to create to three different types of great person
			elif paganReligion == "Pesedjet":
				if countFirstGreatPeople(iPlayer) >= 3:
					return 1
				
			# Rodnovery: acquire seven fur resources
			elif paganReligion == "Rodnovery":
				if pPlayer.getNumAvailableBonuses(iFur) >= 7:
					return 1
					
			# Shendao: control 25% of the world's population
			elif paganReligion == "Shendao":
				if getPopulationPercent(iPlayer) >= 25.0:
					return 1
					
			# Shinto: settle three great spies in your capital
			elif paganReligion == "Shinto":
				capital = pPlayer.getCapitalCity()
				
				if capital and countCitySpecialists(iPlayer, capital, iSpecialistGreatSpy) >= 3:
					return 1
			
			# Tengri: acquire eight horse resources
			elif paganReligion == "Tengri":
				if pPlayer.getNumAvailableBonuses(iHorse) >= 8:
					return 1
				
			# Teotl: sacrifice ten slaves
			elif paganReligion == "Teotl":
				if data.iTeotlSacrifices >= 10 or data.iTeotlFood >= scale(50):
					return 1
					
			# Vedism: have 100 turns of cities celebrating "We Love the King" day
			elif paganReligion == "Vedism":
				if data.iVedicHappiness >= 100:
					return 1
					
			# Yoruba: acquire eight ivory resources and six gem resources
			elif paganReligion == "Yoruba":
				if pPlayer.getNumAvailableBonuses(iIvory) >= 8 and pPlayer.getNumAvailableBonuses(iGems) >= 6:
					return 1
			
		# third Pagan goal: don't allow more than half of your cities to have a religion
		elif iGoal == 2:
			if data.bPolytheismNeverReligion: return 1
			
	elif iVictoryType == iVictorySecularism:
	
		# first Secular goal: control the cathedrals of every religion
		if iGoal == 0:
			iCount = 0
			for iReligion in range(iNumReligions):
				if getNumBuildings(iPlayer, iCathedral + 4*iReligion) > 0:
					iCount += 1
			if iCount >= iNumReligions: return 1
			
		# second Secular goal: make sure there are 25 universities, 10 Great Scientists and 10 Great Statesmen in secular civilizations
		elif iGoal == 1:
			iUniversities = countCivicBuildings(iSecularism, iUniversity)
			iScientists = countCivicSpecialists(iSecularism, iSpecialistGreatScientist)
			iStatesmen = countCivicSpecialists(iSecularism, iSpecialistGreatStatesman)
			if iUniversities >= 25 and iScientists >= 10 and iStatesmen >= 10: return 1
			
		# third Secular goal: make sure the five most advanced civilizations are secular
		elif iGoal == 2:
			advancedPlayers = players.major().alive().novassal().highest(5, lambda p: team(p).getTotalTechValue())
			iCount = advancedPlayers.where(lambda p: has_civic(p, iSecularism))
			if iCount >= 5: return 1
			
	return -1

### UTILITY METHODS ###

def lose(iPlayer, iGoal):
	data.players[iPlayer].lGoals[iGoal] = 0
	if player(iPlayer).isHuman() and turn() > scenarioStartTurn() and AlertsOpt.isShowUHVFailPopup():
		show(text("TXT_KEY_VICTORY_GOAL_FAILED_ANNOUNCE", iGoal+1))
	
def win(iPlayer, iGoal):
	data.players[iPlayer].lGoals[iGoal] = 1
	data.players[iPlayer].lGoalTurns[iGoal] = turn()
	checkHistoricalVictory(iPlayer)
	
def expire(iPlayer, iGoal):
	if isPossible(iPlayer, iGoal): lose(iPlayer, iGoal)
	
def isWon(iPlayer, iGoal):
	return data.players[iPlayer].lGoals[iGoal] == 1
	
def isLost(iPlayer, iGoal):
	return data.players[iPlayer].lGoals[iGoal] == 0
	
def isPossible(iPlayer, iGoal):
	if iPlayer < 0: return False
	return data.players[iPlayer].lGoals[iGoal] == -1
	
def loseAll(iPlayer):
	for i in range(3): data.players[iPlayer].lGoals[i] = 0
	
def resetAll(iPlayer):
	for i in range(3): data.players[iPlayer].lGoals[i] = -1
	
def countAchievedGoals(iPlayer):
	iCount = 0
	for i in range(3):
		if isWon(iPlayer, i): iCount += 1
	return iCount
	
def isFounded(iReligion):
	return data.lReligionFounder[iReligion] != -1
	
def isWonderBuilt(iWonder):
	return data.getWonderBuilder(iWonder) != -1
	
def isDiscovered(iTech):
	return data.lFirstDiscovered[iTech] != -1
	
def isEntered(iEra):
	return data.lFirstEntered[iEra] != -1
	
def isGreatPersonTypeBorn(iGreatPerson):
	if iGreatPerson not in lGreatPeopleUnits: return True
	return getFirstBorn(iGreatPerson) != -1
	
def getFirstBorn(iGreatPerson):
	if iGreatPerson not in lGreatPeopleUnits: return -1
	return data.lFirstGreatPeople[lGreatPeopleUnits.index(iGreatPerson)]

def getBestCity(iPlayer, tPlot, function):
	return cities.all().maximum(lambda city: (function(city), int(at(city, tPlot))))
	
def isBestCity(iPlayer, tPlot, function):
	city = getBestCity(iPlayer, tPlot, function)
	return city and city.getOwner() == iPlayer and at(city, tPlot)
	
def cityPopulation(city):
	if not city: return 0
	return city.getPopulation()
	
def cityCulture(city):
	if not city: return 0
	return city.getCulture(city.getOwner())
	
def cityWonders(city):
	if not city: return 0
	return len([iWonder for iWonder in lWonders if city.isHasRealBuilding(iWonder)])

def cityTradeIncome(city):
	if not city: return 0
	return city.getTradeYield(YieldTypes.YIELD_COMMERCE)
	
def cityHappiness(city):
	if not city: return 0
	
	iHappiness = 0
	iHappiness += city.happyLevel()
	iHappiness -= city.unhappyLevel(0)
	iHappiness += city.getPopulation()
	
	return iHappiness
	
def citySettledGreatPeople(city):
	if not city: return 0
	return sum(city.getFreeSpecialistCount(iGreatPerson) for iGreatPerson in lGreatPeople)
	
def getBestPlayer(iPlayer, function):
	return players.major().alive().maximum(lambda p: (function(p), int(p == iPlayer)))
	
def isBestPlayer(iPlayer, function):
	return getBestPlayer(iPlayer, function) == iPlayer
	
def playerTechs(iPlayer):
	iValue = 0
	for iTech in range(iNumTechs):
		if team(iPlayer).isHasTech(iTech):
			iValue += infos.tech(iTech).getResearchCost()
	return iValue
	
def playerRealPopulation(iPlayer):
	return player(iPlayer).getRealPopulation()
	
def getNumBuildings(iPlayer, iBuilding):
	return player(iPlayer).countNumBuildings(iBuilding)
	
def getPopulationPercent(iPlayer):
	iTotalPopulation = game.getTotalPopulation()
	iOurPopulation = team(iPlayer).getTotalPopulation()
	
	if iTotalPopulation <= 0: return 0.0
	
	return iOurPopulation * 100.0 / iTotalPopulation
	
def getLandPercent(iPlayer):
	iTotalLand = map.getLandPlots()
	iOurLand = player(iPlayer).getTotalLand()
	
	if iTotalLand <= 0: return 0.0
	
	return iOurLand * 100.0 / iTotalLand
	
def getReligionLandPercent(iReligion):
	fPercent = 0.0
	for iPlayer in players.major().alive():
		pPlayer = player(iPlayer)
		if pPlayer.getStateReligion() == iReligion:
			fPercent += getLandPercent(iPlayer)
	return fPercent
	
def isBuildingInCity(tPlot, iBuilding):
	plot = plot_(tPlot)
	
	if not plot.isCity(): return False
	
	return plot.getPlotCity().isHasRealBuilding(iBuilding)
	
def getNumCitiesInArea(iPlayer, lPlots):
	return cities.of(lPlots).owner(iPlayer).count()
	
def getNumCitiesInRegions(iPlayer, lRegions):
	return cities.owner(iPlayer).regions(*lRegions).count()
	
def getNumFoundedCitiesInArea(iPlayer, lPlots):
	return cities.of(lPlots).owner(iPlayer).where(lambda city: city.getOriginalOwner() == iPlayer).count()
	
def getNumConqueredCitiesInArea(iPlayer, lPlots):
	return cities.of(lPlots).owner(iPlayer).where(lambda city: city.getOriginalOwner() != iPlayer).count()
	
def checkOwnedCiv(iPlayer, iOwnedCiv):
	iOwnedPlayer = slot(iOwnedCiv)
	iPlayerCities = getNumCitiesInArea(iPlayer, plots.normal(iOwnedCiv))
	iOwnedCities = getNumCitiesInArea(iOwnedPlayer, plots.normal(iOwnedCiv))
	
	return (iPlayerCities >= 2 and iPlayerCities > iOwnedCities) or (iPlayerCities >= 1 and not player(iOwnedCiv).isAlive()) or (iPlayerCities >= 1 and iOwnedCiv == iPhoenicia)
	
def isControlledOrVassalized(iPlayer, lPlots):
	bControlled = False
	lOwners = []
	lValidOwners = [iPlayer]
	for city in cities.of(lPlots):
		iOwner = city.getOwner()
		if iOwner not in lOwners and not is_minor(iOwner):
			lOwners.append(iOwner)
	for iLoopPlayer in players.vassals(iPlayer):
		lValidOwners.append(iLoopPlayer)
	for iLoopPlayer in lValidOwners:
		if iLoopPlayer in lOwners:
			bControlled = True
			lOwners.remove(iLoopPlayer)
	if lOwners:
		bControlled = False
	return bControlled
	
def isCoreControlled(iPlayer, lOtherCivs):
	return any(checkOwnedCiv(iPlayer, iOtherCiv) for iOtherCiv in lOtherCivs)
	
def countControlledTiles(iPlayer, area, bVassals=False, bCoastalOnly=False):
	lValidOwners = [iPlayer]
	iCount = 0
	iTotal = 0
	
	if bVassals:
		for iLoopPlayer in players.vassals(iPlayer):
			lValidOwners.append(iLoopPlayer)
	
	for plot in area:
		if plot.isWater(): continue
		if bCoastalOnly and not plot.isCoastalLand(): continue
		iTotal += 1
		if plot.getOwner() in lValidOwners: iCount += 1
		
	return iCount, iTotal
	
def countWonders(iPlayer):
	iCount = 0
	for iWonder in range(iBeginWonders, iNumBuildings):
		iCount += getNumBuildings(iPlayer, iWonder)
	return iCount
	
def countShrines(iPlayer):
	iCount = 0
	for iReligion in range(iNumReligions):
		iCurrentShrine = iShrine + iReligion * 4
		iCount += getNumBuildings(iPlayer, iCurrentShrine)
	return iCount
	
def countOpenBorders(iPlayer, lCivs = None):
	contacts = players.major()
	if lCivs:
		contacts = contacts.civs(*lCivs)
		
	return contacts.where(lambda p: team(iPlayer).isOpenBorders(p)).count()
	
def getMostCulturedCity(iPlayer):
	return cities.owner(iPlayer).maximum(lambda city: city.getCulture(iPlayer))

def isAreaFreeOfCivs(lPlots, lCivs):
	return cities.of(lPlots).none(lambda city: civ(city) in lCivs)
	
def isAreaOnlyCivs(area, lCivs):
	return area.cities().all(lambda city: is_minor(city) or civ(city) in lCivs)
	
def countCitySpecialists(iPlayer, tPlot, iSpecialist):
	city = city_(tPlot)
	if not city or city.getOwner() != iPlayer: return 0
	
	return city.getFreeSpecialistCount(iSpecialist)
	
def countSpecialists(iPlayer, iSpecialist):
	iCount = 0
	for city in cities.owner(iPlayer):
		iCount += countCitySpecialists(iPlayer, location(city), iSpecialist)
	return iCount
	
def countReligionSpecialists(iReligion, iSpecialist):
	iCount = 0
	for iPlayer in players.major().alive():
		pPlayer = player(iPlayer)
		if pPlayer.getStateReligion() == iReligion:
			iCount += countSpecialists(iPlayer, iSpecialist)
	return iCount
	
def countCivicSpecialists(iCivic, iSpecialist):
	iCount = 0
	for iPlayer in players.major().alive():
		pPlayer = player(iPlayer)
		if has_civic(iPlayer, iCivic):
			iCount += countSpecialists(iPlayer, iSpecialist)
	return iCount
	
def getAverageCitySize(iPlayer):
	pPlayer = player(iPlayer)
	iNumCities = pPlayer.getNumCities()
	
	if iNumCities == 0: return 0.0
	
	return pPlayer.getTotalPopulation() * 1.0 / iNumCities
	
def getAverageCulture(iPlayer):
	pPlayer = player(iPlayer)
	iNumCities = pPlayer.getNumCities()
	
	if iNumCities == 0: return 0
	
	return pPlayer.countTotalCulture() / iNumCities
	
def countHappinessResources(iPlayer):
	iCount = 0
	pPlayer = player(iPlayer)
	for iBonus in range(iNumBonuses):
		if infos.bonus(iBonus).getHappiness() > 0:
			if pPlayer.getNumAvailableBonuses(iBonus) > 0:
				iCount += 1
	return iCount
	
def countResources(iPlayer, iBonus):
	iNumBonus = 0
	pPlayer = player(iPlayer)
	
	iNumBonus += pPlayer.getNumAvailableBonuses(iBonus)
	iNumBonus -= pPlayer.getBonusImport(iBonus)
	
	for iLoopPlayer in players.major().alive().without(iPlayer):
		pLoopPlayer = player(iLoopPlayer)
		if team(iLoopPlayer).isVassal(iPlayer):
			iNumBonus += pLoopPlayer.getNumAvailableBonuses(iBonus)
			iNumBonus -= pLoopPlayer.getBonusImport(iBonus)
				
	return iNumBonus
	
def isStateReligionInArea(iReligion, tRectangle):
	return cities.rectangle(tRectangle).any(lambda city: player(city).getStateReligion() == iReligion)
	
def getCityCulture(iPlayer, tPlot):
	city = city_(tPlot)
	if not city or city.getOwner() != iPlayer: return 0
	
	return city.getCulture(iPlayer)
	
def isConnected(tStart, lTargets, plotFunction):
	if not lTargets: return False
	if not plotFunction(tStart): return False
	
	if tStart in lTargets: return True
	
	targets = plots.of(lTargets).where(plotFunction)
	
	if not targets: return False
	
	lNodes = [(targets.closest_distance(tStart), tStart)]
	heapq.heapify(lNodes)
	lVisitedNodes = []
	
	while lNodes:
		h, tNode = heapq.heappop(lNodes)
		lVisitedNodes.append((h, tNode))
		
		for plot in plots.surrounding(tNode):
			if plotFunction(location(plot)):
				if plot in targets: return True
				
				tTuple = (targets.closest_distance(plot), location(plot))
				if not tTuple in lVisitedNodes and not tTuple in lNodes:
					heapq.heappush(lNodes, tTuple)
							
	return False
	
def isConnectedByTradeRoute(iPlayer, lStarts, lTargets):
	for tStart in lStarts:
		startPlot = plot(tStart)
		if not startPlot.isCity(): continue
		
		plotFunction = lambda tPlot: plot(tPlot).getOwner() in [iPlayer, startPlot.getOwner()] and (plot(tPlot).isCity() or plot(tPlot).getRouteType() in [iRouteRoad, iRouteRailroad, iRouteRomanRoad, iRouteHighway])
	
		if isConnected(tStart, lTargets, plotFunction): return True
		
	return False
	
def isConnectedByRailroad(iPlayer, tStart, lTargets):
	if not team(iPlayer).isHasTech(iRailroad): return False
	
	startPlot = plot(tStart)
	if not (startPlot.isCity() and startPlot.getOwner() == iPlayer): return False
	
	plotFunction = lambda tPlot: plot(tPlot).getOwner() == iPlayer and (plot(tPlot).isCity() or plot(tPlot).getRouteType() == iRouteRailroad)
	
	return isConnected(tStart, lTargets, plotFunction)

def countPlayersWithAttitudeAndCriteria(iPlayer, eAttitude, function):
	return players.major().without(iPlayer).where(lambda p: player(iPlayer).canContact(p) and player(p).AI_getAttitude(iPlayer) >= eAttitude and function(p))
	
def countPlayersWithAttitudeAndReligion(iPlayer, eAttitude, iReligion):
	return countPlayersWithAttitudeAndCriteria(iPlayer, iAttitude, lambda p: cities.owner(p).religion(iReligion).any())
	
def countPlayersWithAttitudeInGroup(iPlayer, eAttitude, lOtherCivs):
	return countPlayersWithAttitudeAndCriteria(iPlayer, eAttitude, lambda p: civ(p) in lOtherCivs and not team(p).isAVassal())
	
def getLargestCities(iPlayer, iNumCities):
	return cities.owner(iPlayer).highest(iNumCities, lambda city: city.getPopulation())
	
def countCitiesOfSize(iPlayer, iThreshold):
	return cities.owner(iPlayer).where(lambda city: city.getPopulation() >= iThreshold).count()
	
def countCitiesWithCultureLevel(iPlayer, iThreshold):
	return cities.owner(iPlayer).where(lambda city: city.getCultureLevel() >= iThreshold).count()
	
def countAcquiredResources(iPlayer, lResources):
	iCount = 0
	pPlayer = player(iPlayer)
	for iBonus in lResources:
		iCount += pPlayer.getNumAvailableBonuses(iBonus)
	return iCount
	
def isRoad(iPlayer, lPlots):
	for tPlot in lPlots:
		plot = plot_(tPlot)
		if plot.getOwner() != iPlayer: return False
		if not plot.getRouteType() == iRouteRoad and not plot.isCity(): return False
		
	return True
	
def countCityWonders(iPlayer, (x, y), bIncludeObsolete=False):
	iCount = 0
	city = city_(x, y)
	
	if not city: return 0
	if city.getOwner() != iPlayer: return 0
	
	for iWonder in lWonders:
		iObsoleteTech = infos.building(iWonder).getObsoleteTech()
		if not bIncludeObsolete and iObsoleteTech != -1 and team(iPlayer).isHasTech(iObsoleteTech): continue
		
		if city.isHasRealBuilding(iWonder):
			iCount += 1
		
	return iCount
	
def isCultureControlled(iPlayer, lPlots):
	return all(plot(x, y).getOwner() in [iPlayer, -1] for (x, y) in lPlots)
	
def controlsCity(iPlayer, tPlot):
	return cities.surrounding(tPlot).owner(iPlayer)
	
def getTotalCulture(lCivs):
	return players.civs(*lCivs).sum(lambda p: player(p).countTotalCulture())
	
def countImprovements(iPlayer, iImprovement):
	if iImprovement <= 0: return 0
	return player(iPlayer).getImprovementCount(iImprovement)
	
def controlsAllCities(iPlayer, area):
	return area.cities().all(lambda city: city.getOwner() == iPlayer)
	
def isAtPeace(iPlayer):
	return players.major().alive().none(lambda p: team(iPlayer).isAtWar(p))
	
def getHappiest():
	return players.major().alive().maximum(getApprovalRating)
	
def isHappiest(iPlayer):
	return getHappiest() == iPlayer
	
def getHealthiest():
	return players.major().alive().maximum(getLifeExpectancyRating)
	
def isHealthiest(iPlayer):
	return getHealthiest() == iPlayer
	
def countReligionCities(iPlayer):
	return cities.owner(iPlayer).where(lambda city: city.getReligionCount() > 0).count()
	
def isCompleteTechTree(iPlayer):
	if player(iPlayer).getCurrentEra() < iGlobal: return False
	
	tPlayer = team(iPlayer)
	for iTech in range(iNumTechs):
		if not (tPlayer.isHasTech(iTech) or tPlayer.getTechCount(iTech) > 0): return False
		
	return True
	
def countFirstDiscovered(iPlayer, iEra):
	iCount = 0
	for iTech in range(iNumTechs):
		if infos.tech(iTech).getEra() == iEra and data.lFirstDiscovered[iTech] == iPlayer:
			iCount += 1
	return iCount
	
def isFirstDiscoveredPossible(iPlayer, iEra, iRequired):
	iCount = countFirstDiscovered(iPlayer, iEra)
	iNotYetDiscovered = countFirstDiscovered(-1, iEra)
	return iCount + iNotYetDiscovered >= iRequired
	
def isWonder(iBuilding):
	return iBeginWonders <= iBuilding < iNumBuildings
	
def countReligionPlayers(iReligion):
	iReligionPlayers = 0
	iTotalPlayers = 0
	for iPlayer in players.major().alive():
		pPlayer = player(iPlayer)
		iTotalPlayers += 1
		if pPlayer.getStateReligion() == iReligion:
			iReligionPlayers += 1
	return iReligionPlayers, iTotalPlayers
	
def countCivicPlayers(iCivic):
	iCivicPlayers = 0
	iTotalPlayers = 0
	for iPlayer in players.major().alive():
		pPlayer = player(iPlayer)
		iTotalPlayers += 1
		if has_civic(iPlayer, iCivic):
			iCivicPlayers += 1
	return iCivicPlayers, iTotalPlayers
	
def getBestCities(function):
	return cities.all().sort(function, True)
	
def countBestCitiesReligion(iReligion, function, iNumCities):
	lCities = getBestCities(function)
	
	iCount = 0
	for city in lCities[:iNumCities]:
		if city.isHasReligion(iReligion) and player(city).getStateReligion() == iReligion:
			iCount += 1
			
	return iCount
	
def getReligiousLand(iReligion):
	fLandPercent = 0.0
	for iPlayer in players.major().alive():
		pPlayer = player(iPlayer)
		if pPlayer.getStateReligion() == iReligion:
			fLandPercent += getLandPercent(iPlayer)
	return fLandPercent
	
def countLivingPlayers():
	return players.major().alive().count()
	
def countGoodRelationPlayers(iPlayer, iAttitudeThreshold):
	iCount = 0
	tPlayer = team(iPlayer)
	for iLoopPlayer in players.major().without(iPlayer):
		if tPlayer.isHasMet(iLoopPlayer):
			if player(iLoopPlayer).AI_getAttitude(iPlayer) >= iAttitudeThreshold:
				iCount += 1
	return iCount
	
def countUnitsOfType(iPlayer, lTypes, bIncludeObsolete=False):
	iCount = 0
	pPlayer = player(iPlayer)
	for iUnit in range(iNumUnits):
		if bIncludeObsolete or pPlayer.canTrain(iUnit, False, False):
			if infos.unit(iUnit).getUnitCombatType() in lTypes:
				iUnitClass = infos.unit(iUnit).getUnitClassType()
				iCount += pPlayer.getUnitClassCount(iUnitClass)
	return iCount
	
def calculateShrineIncome(iPlayer, iReligion):
	if getNumBuildings(iPlayer, iShrine  + 4*iReligion) == 0: return 0
	
	iThreshold = 20
	if getNumBuildings(iPlayer, iDomeOfTheRock) > 0 and not team(iPlayer).isHasTech(iLiberalism): iThreshold = 40
	
	return min(iThreshold, game.countReligionLevels(iReligion))
	
def countWorldBuildings(iBuilding):
	iCount = 0
	for iPlayer in players.major().alive():
		iCount += getNumBuildings(iPlayer, unique_building(iPlayer, iBuilding))
	return iCount
	
def countReligionWonders(iPlayer, iReligion):
	iCount = 0
	for iWonder in lWonders:
		if infos.building(iWonder).getPrereqReligion() == iReligion and getNumBuildings(iPlayer, iWonder) > 0:
			iCount += 1
	return iCount
	
def countCivicBuildings(iCivic, iBuilding):
	iCount = 0
	for iPlayer in players.major().alive():
		pPlayer = player(iPlayer)
		if has_civic(iPlayer, iCivic):
			iCount += getNumBuildings(iPlayer, unique_building(iPlayer, iBuilding))
	return iCount
	
def getApostolicVotePercent(iPlayer):
	iTotal = 0
	for iLoopPlayer in players.major():
		iTotal += player(iLoopPlayer).getVotes(16, 1)
		
	if iTotal == 0: return 0.0
	
	return player(iPlayer).getVotes(16, 1) * 100.0 / iTotal
	
def countNativeCulture(iPlayer, iPercent):
	iPlayerCulture = 0
	
	for city in cities.owner(iPlayer):
		iCulture = city.getCulture(iPlayer)
		iTotal = 0
		
		for iLoopPlayer in players.all().barbarian():
			iTotal += city.getCulture(iLoopPlayer)
		
		if iTotal > 0 and iCulture * 100 / iTotal >= iPercent:
			iPlayerCulture += iCulture
			
	return iPlayerCulture
	
def isTradeConnected(iPlayer):
	return players.major().without(iPlayer).any(lambda p: player(iPlayer).canContact(p) and player(iPlayer).canTradeNetworkWith(p))
	
def countUnitsOfLevel(iPlayer, iLevel):
	return units.owner(iPlayer).where(lambda unit: unit.getLevel() >= iLevel).count()
	
def countControlledTerrain(iPlayer, iTerrain):
	return plots.all().owner(iPlayer).where(lambda p: p.getTerrainType() == iTerrain).count()
	
def countControlledFeatures(iPlayer, iFeature, iImprovement):
	return plots.all().owner(iPlayer).where(lambda p: p.getFeatureType() == iFeature and p.getImprovementType() == iImprovement).count()
	
def countControlledPeaks(iPlayer):
	return plots.all().owner(iPlayer).where(lambda p: p.isPeak()).count()
	
def getGlobalTreasury():
	iTreasury = 0

	for iPlayer in players.major():
		iTreasury += player(iPlayer).getGold()
		
	return iTreasury
	
def countFirstGreatPeople(iPlayer):
	return len([iGreatPerson for iGreatPerson in lGreatPeopleUnits if getFirstBorn(iGreatPerson) == iPlayer])
	
def countReligionSpecialistCities(iPlayer, iReligion, iSpecialist):
	return cities.owner(iPlayer).where(lambda city: city.isHasReligion(iReligion) and city.getFreeSpecialistCount(iSpecialist) > 0).count()
	
def calculateAlliedPercent(iPlayer, function):
	pTeam = team(iPlayer)

	iAlliedValue = 0
	iTotalValue = 0
	
	for iLoopPlayer in players.major().alive():
		iValue = function(iLoopPlayer)
		iTotalValue += iValue
		
		iMaster = master(iLoopPlayer)
		
		if iLoopPlayer == iPlayer or pTeam.isDefensivePact(player(iLoopPlayer).getTeam()):
			iAlliedValue += iValue
		elif iMaster and (iMaster == iPlayer or pTeam.isDefensivePact(player(iMaster).getTeam())):
			iAlliedValue += iValue
			
	if iTotalValue == 0: return 0
	
	return 100.0 * iAlliedValue / iTotalValue
	
def calculateAlliedCommercePercent(iPlayer):
	return calculateAlliedPercent(iPlayer, lambda x: player(x).calculateTotalCommerce())
	
def calculateAlliedPowerPercent(iPlayer):
	return calculateAlliedPercent(iPlayer, lambda x: player(x).getPower())
	
def countRegionReligion(iReligion, lRegions):
	return cities.regions(*lRegions).religion(iReligion).count()
	
def findBestCityWith(iPlayer, filter, metric):
	return cities.owner(iPlayer).where(filter).maximum(metric)
	
def countVassals(iPlayer, lCivs=None, iReligion=-1):
	return players.vassals(iPlayer).where(lambda p: not lCivs or civ(p) in lCivs).where(lambda p: iReligion < 0 or player(p).getStateReligion() == iReligion).count()
	
### UHV HELP SCREEN ###

def getIcon(bVal):
	if bVal:
		return u"%c" %(CyGame().getSymbolID(FontSymbols.SUCCESS_CHAR))
	else:
		return u"%c" %(CyGame().getSymbolID(FontSymbols.FAILURE_CHAR))

def getURVHelp(iPlayer, iGoal):
	pPlayer = player(iPlayer)
	iVictoryType = getReligiousVictoryType(iPlayer)
	aHelp = []

	if checkReligiousGoal(iPlayer, iGoal) == 1:
		aHelp.append(getIcon(True) + text("TXT_KEY_VICTORY_GOAL_ACCOMPLISHED"))
		return aHelp
	elif checkReligiousGoal(iPlayer, iGoal) == 0:
		aHelp.append(getIcon(False) + text("TXT_KEY_VICTORY_GOAL_FAILED"))
		return aHelp
	
	if iVictoryType == iJudaism:
		if iGoal == 0:
			iProphets = countReligionSpecialists(iJudaism, iSpecialistGreatProphet)
			iScientists = countReligionSpecialists(iJudaism, iSpecialistGreatScientist)
			iStatesmen = countReligionSpecialists(iJudaism, iSpecialistGreatStatesman)
			aHelp.append(getIcon(iProphets + iScientists + iStatesmen) + text("TXT_KEY_VICTORY_JEWISH_SPECIALISTS", iProphets + iScientists + iStatesmen, 15))
		elif iGoal == 1:
			holyCity = game.getHolyCity(iJudaism)
			aHelp.append(getIcon(holyCity.getOwner() == iPlayer) + text("TXT_KEY_VICTORY_CONTROL_HOLY_CITY", holyCity.getName()) + ' ' + getIcon(holyCity.getCultureLevel() >= 6) + text("TXT_KEY_VICTORY_LEGENDARY_CULTURE_CITY", holyCity.getName()))
		elif iGoal == 2:
			iFriendlyRelations = countPlayersWithAttitudeAndReligion(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY, iJudaism)
			aHelp.append(getIcon(iFriendlyRelations >= 6) + text("TXT_KEY_VICTORY_FRIENDLY_RELIGION", infos.religion(iJudaism).getAdjectiveKey(), iFriendlyRelations, 6))

	elif iVictoryType == iOrthodoxy:
		if iGoal == 0:
			iOrthodoxCathedrals = getNumBuildings(iPlayer, iOrthodoxCathedral)
			aHelp.append(getIcon(iOrthodoxCathedrals >= 4) + text("TXT_KEY_VICTORY_ORTHODOX_CATHEDRALS", iOrthodoxCathedrals, 4))
		elif iGoal == 1:
			lCultureCities = getBestCities(cityCulture)[:5]
			iCultureCities = countBestCitiesReligion(iOrthodoxy, cityCulture, 5)
			for city in lCultureCities:
				aHelp.append(getIcon(city.isHasReligion(iOrthodoxy) and player(city).getStateReligion() == iOrthodoxy) + city.getName())
		elif iGoal == 2:
			bNoCatholics = countReligionPlayers(iCatholicism)[0] == 0
			aHelp.append(getIcon(bNoCatholics) + text("TXT_KEY_VICTORY_NO_CATHOLICS"))

	elif iVictoryType == iCatholicism:
		if iGoal == 0:
			iPopeTurns = data.iPopeTurns
			aHelp.append(getIcon(iPopeTurns >= turns(100)) + text("TXT_KEY_VICTORY_POPE_TURNS", iPopeTurns, turns(100)))
		elif iGoal == 1:
			bShrine = pPlayer.countNumBuildings(iCatholicShrine) > 0
			iSaints = countReligionSpecialists(iCatholicism, iSpecialistGreatProphet)
			aHelp.append(getIcon(bShrine) + text("TXT_KEY_BUILDING_CATHOLIC_SHRINE") + ' ' + getIcon(iSaints >= 12) + text("TXT_KEY_VICTORY_CATHOLIC_SAINTS", iSaints, 12))
		elif iGoal == 2:
			fLandPercent = getReligiousLand(iCatholicism)
			aHelp.append(getIcon(fLandPercent >= 50.0) + text("TXT_KEY_VICTORY_CATHOLIC_WORLD_TERRITORY", "%.2f%%" % fLandPercent, '50'))

	elif iVictoryType == iProtestantism:
		if iGoal == 0:
			bCivilLiberties = data.lFirstDiscovered[iCivilLiberties] == iPlayer
			bConstitution = data.lFirstDiscovered[iSocialContract] == iPlayer
			bEconomics = data.lFirstDiscovered[iEconomics] == iPlayer
			aHelp.append(getIcon(bCivilLiberties) + text("TXT_KEY_TECH_CIVIL_LIBERTIES") + ' ' + getIcon(bConstitution) + text("TXT_KEY_TECH_CONSTITUTION") + ' ' + getIcon(bEconomics) + text("TXT_KEY_TECH_ECONOMICS"))
		elif iGoal == 1:
			iMerchants = countReligionSpecialists(iProtestantism, iSpecialistGreatMerchant)
			iEngineers = countReligionSpecialists(iProtestantism, iSpecialistGreatEngineer)
			aHelp.append(getIcon(iMerchants >= 5) + text("TXT_KEY_VICTORY_PROTESTANT_MERCHANTS", iMerchants, 5) + ' ' + getIcon(iEngineers >= 5) + text("TXT_KEY_VICTORY_PROTESTANT_ENGINEERS", iEngineers, 5))
		elif iGoal == 2:
			iProtestantCivs, iTotal = countReligionPlayers(iProtestantism)
			iSecularCivs, iTotal = countCivicPlayers(iSecularism)
			iNumProtestantCivs = iProtestantCivs + iSecularCivs
			aHelp.append(getIcon(2 * iNumProtestantCivs >= iTotal) + text("TXT_KEY_VICTORY_PROTESTANT_CIVS", iNumProtestantCivs, iTotal))

	elif iVictoryType == iIslam:
		if iGoal == 0:
			fReligionPercent = game.calculateReligionPercent(iIslam)
			aHelp.append(getIcon(fReligionPercent >= 40.0) + text("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", infos.religion(iIslam).getTextKey(), "%.2f%%" % fReligionPercent, 40))
		elif iGoal == 1:
			iCount = 0
			pHolyCity = game.getHolyCity(iIslam)
			for iGreatPerson in lGreatPeople:
				iCount += pHolyCity.getFreeSpecialistCount(iGreatPerson)
			aHelp.append(getIcon(iCount >= 7) + text("TXT_KEY_VICTORY_CITY_GREAT_PEOPLE", game.getHolyCity(iIslam).getName(), iCount, 7))
		elif iGoal == 2:
			iCount = 0
			for iReligion in range(iNumReligions):
				iCount += getNumBuildings(iPlayer, iShrine + 4*iReligion)
			aHelp.append(getIcon(iCount >= 5) + text("TXT_KEY_VICTORY_NUM_SHRINES", iCount, 5))

	elif iVictoryType == iHinduism:
		if iGoal == 0:
			iCount = 0
			pHolyCity = game.getHolyCity(iHinduism)
			for iGreatPerson in lGreatPeople:
				if pHolyCity.getFreeSpecialistCount(iGreatPerson) > 0:
					iCount += 1
			aHelp.append(getIcon(iCount >= 5) + text("TXT_KEY_VICTORY_CITY_DIFFERENT_GREAT_PEOPLE", game.getHolyCity(iHinduism).getName(), iCount, 5))
		elif iGoal == 1:
			iGoldenAgeTurns = data.iHinduGoldenAgeTurns
			aHelp.append(getIcon(iGoldenAgeTurns >= turns(24)) + text("TXT_KEY_VICTORY_GOLDEN_AGE_TURNS", iGoldenAgeTurns, turns(24)))
		elif iGoal == 2:
			iLargestCities = countBestCitiesReligion(iHinduism, cityPopulation, 5)
			aHelp.append(getIcon(iLargestCities >= 5) + text("TXT_KEY_VICTORY_HINDU_LARGEST_CITIES", iLargestCities, 5))

	elif iVictoryType == iBuddhism:
		if iGoal == 0:
			iPeaceTurns = data.iBuddhistPeaceTurns
			aHelp.append(getIcon(iPeaceTurns >= turns(100)) + text("TXT_KEY_VICTORY_PEACE_TURNS", iPeaceTurns, turns(100)))
		elif iGoal == 1:
			iHappinessTurns = data.iBuddhistHappinessTurns
			aHelp.append(getIcon(iHappinessTurns >= turns(100)) + text("TXT_KEY_VICTORY_HAPPINESS_TURNS", iHappinessTurns, turns(100)))
		elif iGoal == 2:
			iGoodRelations = countGoodRelationPlayers(iPlayer, AttitudeTypes.ATTITUDE_CAUTIOUS)
			iTotalPlayers = countLivingPlayers()-1
			aHelp.append(getIcon(iGoodRelations >= iTotalPlayers) + text("TXT_KEY_VICTORY_CAUTIOUS_OR_BETTER_RELATIONS", iGoodRelations, iTotalPlayers))

	elif iVictoryType == iConfucianism:
		if iGoal == 0:
			iFriendlyCivs = countGoodRelationPlayers(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY)
			aHelp.append(getIcon(iFriendlyCivs >= 5) + text("TXT_KEY_VICTORY_FRIENDLY_CIVS", iFriendlyCivs, 5))
		elif iGoal == 1:
			holyCity = game.getHolyCity(iConfucianism)
			iCount = countCityWonders(iPlayer, (holyCity.getX(), holyCity.getY()), True)
			aHelp.append(getIcon(holyCity.getOwner() == iPlayer) + text("TXT_KEY_VICTORY_CONTROL_HOLY_CITY", holyCity.getName()) + ' ' + getIcon(iCount >= 5) + text("TXT_KEY_VICTORY_HOLY_CITY_WONDERS", holyCity.getName(), iCount, 5))
		elif iGoal == 2:
			iUnitCombatMelee = infos.type('UNITCOMBAT_MELEE')
			iUnitCombatGunpowder = infos.type('UNITCOMBAT_GUN')
			iCount = countUnitsOfType(iPlayer, [iUnitCombatMelee, iUnitCombatGunpowder])
			aHelp.append(getIcon(iCount >= 200) + text("TXT_KEY_VICTORY_CONTROL_NUM_UNITS", iCount, 200))

	elif iVictoryType == iTaoism:
		if iGoal == 0:
			iHealthTurns = data.iTaoistHealthTurns
			aHelp.append(getIcon(iHealthTurns >= turns(100)) + text("TXT_KEY_VICTORY_HEALTH_TURNS", iHealthTurns, turns(100)))
		elif iGoal == 1:
			bConfucianShrine = getNumBuildings(iPlayer, iConfucianShrine) > 0
			bTaoistShrine = getNumBuildings(iPlayer, iTaoistShrine) > 0

			iConfucianIncome = calculateShrineIncome(iPlayer, iConfucianism)
			iTaoistIncome = calculateShrineIncome(iPlayer, iTaoism)
			
			aHelp.append(getIcon(bConfucianShrine) + text("TXT_KEY_BUILDING_CONFUCIAN_SHRINE") + ' ' + getIcon(bTaoistShrine) + text("TXT_KEY_BUILDING_TAOIST_SHRINE") + ' ' + getIcon(iConfucianIncome + iTaoistIncome >= 40) + text("TXT_KEY_VICTORY_CHINESE_SHRINE_INCOME", iConfucianIncome + iTaoistIncome, 40))
		elif iGoal == 2:
			holyCity = game.getHolyCity(iTaoism)
			aHelp.append(getIcon(holyCity.getOwner() == iPlayer) + text("TXT_KEY_VICTORY_CONTROL_HOLY_CITY", holyCity.getName()) + ' ' + getIcon(holyCity.getCultureLevel() >= 6) + text("TXT_KEY_VICTORY_LEGENDARY_CULTURE_CITY", holyCity.getName()))

	elif iVictoryType == iZoroastrianism:
		if iGoal == 0:
			iNumIncense = pPlayer.getNumAvailableBonuses(iIncense)
			aHelp.append(getIcon(iNumIncense >= 6) + text("TXT_KEY_VICTORY_AVAILABLE_INCENSE_RESOURCES", iNumIncense, 6))
		elif iGoal == 1:
			fReligionPercent = game.calculateReligionPercent(iZoroastrianism)
			aHelp.append(getIcon(fReligionPercent >= 10.0) + text("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", infos.religion(iZoroastrianism).getTextKey(), "%.2f%%" % fReligionPercent, 10))
		elif iGoal == 2:
			holyCity = game.getHolyCity(iZoroastrianism)
			aHelp.append(getIcon(holyCity.getOwner() == iPlayer) + text("TXT_KEY_VICTORY_CONTROL_HOLY_CITY", holyCity.getName()) + ' ' + getIcon(holyCity.getCultureLevel() >= 6) + text("TXT_KEY_VICTORY_LEGENDARY_CULTURE_CITY", holyCity.getName()))

	elif iVictoryType == iVictoryPaganism:
		if iGoal == 0:
			iCount = countWorldBuildings(iPaganTemple)
			aHelp.append(getIcon(iCount >= 15) + text("TXT_KEY_VICTORY_NUM_PAGAN_TEMPLES_WORLD", iCount, 15))
		elif iGoal == 1:
			aHelp.append(getPaganGoalHelp(iPlayer))
		elif iGoal == 2:
			bPolytheismNeverReligion = data.bPolytheismNeverReligion
			aHelp.append(getIcon(bPolytheismNeverReligion) + text("TXT_KEY_VICTORY_POLYTHEISM_NEVER_RELIGION"))

	elif iVictoryType == iVictorySecularism:
		if iGoal == 0:
			iCount = 0
			for iReligion in range(iNumReligions):
				if getNumBuildings(iPlayer, iCathedral + 4 * iReligion) > 0:
					iCount += 1
			aHelp.append(getIcon(iCount >= iNumReligions) + text("TXT_KEY_VICTORY_DIFFERENT_CATHEDRALS", iCount, iNumReligions))
		elif iGoal == 1:
			iUniversities = countCivicBuildings(iSecularism, iUniversity)
			iScientists = countCivicSpecialists(iSecularism, iSpecialistGreatScientist)
			iStatesmen = countCivicSpecialists(iSecularism, iSpecialistGreatStatesman)
			aHelp.append(getIcon(iUniversities >= 25) + text("TXT_KEY_VICTORY_SECULAR_UNIVERSITIES", iUniversities, 25))
			aHelp.append(getIcon(iScientists >= 10) + text("TXT_KEY_VICTORY_SECULAR_SCIENTISTS", iScientists, 10) + ' ' + getIcon(iStatesmen >= 10) + text("TXT_KEY_VICTORY_SECULAR_STATESMEN", iStatesmen, 10))
		elif iGoal == 2:
			advancedPlayers = players.major().alive().novassal().highest(5, lambda p: team(p).getTotalTechValue())
			aHelp.append(' '.join(getIcon(has_civic(p, iSecularism)) + name(p) for p in advancedPlayers))
				
	return aHelp
	
def getPaganGoalHelp(iPlayer):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)
	paganReligion = infos.civ(pPlayer).getPaganReligionName(0)

	if paganReligion == "Anunnaki":
		x, y = 0, 0
		capital = pPlayer.getCapitalCity()
		
		if capital:
			x, y = capital.getX(), capital.getY()
		pBestCity = getBestCity(iPlayer, (x, y), cityWonders)
		bBestCity = isBestCity(iPlayer, (x, y), cityWonders)
		sBestCity = "(none)"
		if pBestCity:
			sBestCity = pBestCity.getName()
		return getIcon(bBestCity) + text("TXT_KEY_VICTORY_CITY_WITH_MOST_WONDERS", sBestCity)
		
	elif paganReligion == "Asatru":
		iCount = countUnitsOfLevel(iPlayer, 5)
		return getIcon(iCount >= 5) + text("TXT_KEY_VICTORY_UNITS_OF_LEVEL", 5, iCount, 5)
		
	elif paganReligion == "Atua":
		iNumPearls = pPlayer.getNumAvailableBonuses(iPearls)
		iOceanTiles = countControlledTerrain(iPlayer, iOcean)
		return getIcon(iNumPearls >= 4) + text("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", infos.bonus(iPearls).getText().lower(), iNumPearls, 4) + ' ' + getIcon(iOceanTiles >= 50) + text("TXT_KEY_VICTORY_CONTROLLED_OCEAN_TILES", iOceanTiles, 50)
		
	elif paganReligion == "Baalism":
		x, y = 0, 0
		capital = pPlayer.getCapitalCity()
		
		if capital:
			x, y = capital.getX(), capital.getY()
		pBestCity = getBestCity(iPlayer, (x, y), cityTradeIncome)
		bBestCity = isBestCity(iPlayer, (x, y), cityTradeIncome)
		return getIcon(bBestCity) + text("TXT_KEY_VICTORY_HIGHEST_TRADE_CITY", pBestCity.getName())
		
	elif paganReligion == "Bon":
		iNumPeaks = countControlledPeaks(iPlayer)
		return getIcon(iNumPeaks >= 50) + text("TXT_KEY_VICTORY_CONTROLLED_PEAKS", iNumPeaks, 50)
		
	elif paganReligion == "Druidism":
		iCount = countControlledFeatures(iPlayer, iForest, -1) + countControlledFeatures(iPlayer, iMud, -1)
		return getIcon(iCount >= 20) + text("TXT_KEY_VICTORY_CONTROLLED_FOREST_AND_MARSH_TILES", iCount, 20)
	
	elif paganReligion == "Inti":
		iOurTreasury = pPlayer.getGold()
		iWorldTreasury = getGlobalTreasury()
		return getIcon(2 * iOurTreasury >= iWorldTreasury) + text("TXT_KEY_VICTORY_TOTAL_GOLD", iOurTreasury, iWorldTreasury - iOurTreasury)
	
	elif paganReligion == "Mazdaism":
		iCount = pPlayer.getNumAvailableBonuses(iIncense)
		return getIcon(iCount >= 6) + text("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", infos.bonus(iIncense).getText().lower(), iCount, 6)
	
	elif paganReligion == "Mugyo":
		x, y = 0, 0
		capital = pPlayer.getCapitalCity()
		
		if capital:
			x, y = capital.getX(), capital.getY()
		pBestCity = getBestCity(iPlayer, (x, y), citySettledGreatPeople)
		bBestCity = isBestCity(iPlayer, (x, y), citySettledGreatPeople)
		sBestCity = "(none)"
		if pBestCity:
			sBestCity = pBestCity.getName()
			
		return getIcon(bBestCity) + text("TXT_KEY_VICTORY_CITY_WITH_MOST_GREAT_PEOPLE", sBestCity)
	
	elif paganReligion == "Olympianism":
		iCount = countReligionWonders(iPlayer, -1)
		return getIcon(iCount >= 10) + text("TXT_KEY_VICTORY_NUM_NONRELIGIOUS_WONDERS", iCount, 10)
		
	elif paganReligion == "Pesedjet":
		iCount = countFirstGreatPeople(iPlayer)
		return getIcon(iCount >= 3) + text("TXT_KEY_VICTORY_FIRST_GREAT_PEOPLE", iCount, 3)
	
	elif paganReligion == "Rodnovery":
		iCount = pPlayer.getNumAvailableBonuses(iFur)
		return getIcon(iCount >= 7) + text("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", infos.bonus(iFur).getText().lower(), iCount, 7)
	
	elif paganReligion == "Shendao":
		fPopulationPercent = getPopulationPercent(iPlayer)
		return getIcon(fPopulationPercent >= 25.0) + text("TXT_KEY_VICTORY_PERCENTAGE_WORLD_POPULATION", "%.2f%%" % fPopulationPercent, 25)
	
	elif paganReligion == "Shinto":
		capital = pPlayer.getCapitalCity()
		iCount = 0
		if capital: iCount = countCitySpecialists(iPlayer, (capital.getX(), capital.getY()), iSpecialistGreatSpy)
		return getIcon(iCount >= 3) + text("TXT_KEY_VICTORY_CAPITAL_GREAT_SPIES", iCount, 3)
	
	elif paganReligion == "Tengri":
		iCount = pPlayer.getNumAvailableBonuses(iHorse)
		return getIcon(iCount >= 8) + text("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", infos.bonus(iHorse).getText().lower(), iCount, 8)
	
	elif paganReligion == "Teotl":
		if iCiv == iMaya:
			iCount = data.iTeotlFood
			return getIcon(iCount >= scale(50)) + text("TXT_KEY_VICTORY_FOOD_FROM_COMBAT", iCount, scale(50))
	
		iCount = data.iTeotlSacrifices
		return getIcon(iCount >= 10) + text("TXT_KEY_VICTORY_SACRIFICED_SLAVES", iCount, 10)
	
	elif paganReligion == "Vedism":
		iCount = data.iVedicHappiness
		return getIcon(iCount >= 100) + text("TXT_KEY_VICTORY_WE_LOVE_RULER_TURNS", iCount, 100)
	
	elif paganReligion == "Yoruba":
		iNumIvory = pPlayer.getNumAvailableBonuses(iIvory)
		iNumGems = pPlayer.getNumAvailableBonuses(iGems)
		return getIcon(iNumIvory >= 8) + text("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", infos.bonus(iIvory).getText().lower(), iNumIvory, 8) + ' ' + getIcon(iNumGems >= 6) + text("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", infos.bonus(iGems).getText().lower(), iNumGems, 6)

def getUHVHelp(iPlayer, iGoal):
	"Returns an array of help strings used by the Victory Screen table"

	aHelp = []
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)

	# the info is outdated or irrelevant once the goal has been accomplished or failed
	if data.players[iPlayer].lGoals[iGoal] == 1:
		iWinTurn = data.players[iPlayer].lGoalTurns[iGoal]
		iTurnYear = game.getTurnYear(iWinTurn)
		if iTurnYear < 0:
			sWinDate = text("TXT_KEY_TIME_BC", -iTurnYear)
		else:
			sWinDate = text("TXT_KEY_TIME_AD", iTurnYear)
		if AdvisorOpt.isUHVFinishDateNone():
			aHelp.append(getIcon(True) + text("TXT_KEY_VICTORY_GOAL_ACCOMPLISHED"))
		elif AdvisorOpt.isUHVFinishDateDate():
			aHelp.append(getIcon(True) + text("TXT_KEY_VICTORY_GOAL_ACCOMPLISHED_DATE", sWinDate))
		else:
			aHelp.append(getIcon(True) + text("TXT_KEY_VICTORY_GOAL_ACCOMPLISHED_DATE_TURN", sWinDate, iWinTurn - scenarioStartTurn()))
		if not AdvisorOpt.UHVProgressAfterFinish():
			return aHelp
	elif data.players[iPlayer].lGoals[iGoal] == 0:
		aHelp.append(getIcon(False) + text("TXT_KEY_VICTORY_GOAL_FAILED"))
		if not AdvisorOpt.UHVProgressAfterFinish():
			return aHelp

	if iCiv == iEgypt:
		if iGoal == 0:
			iCulture = pPlayer.countTotalCulture()
			aHelp.append(getIcon(iCulture >= turns(500)) + text("TXT_KEY_VICTORY_TOTAL_CULTURE", iCulture, turns(500)))
		elif iGoal == 1:
			bPyramids = data.getWonderBuilder(iPyramids) == iPlayer
			bLibrary = data.getWonderBuilder(iGreatLibrary) == iPlayer
			bLighthouse = data.getWonderBuilder(iGreatLighthouse) == iPlayer
			aHelp.append(getIcon(bPyramids) + text("TXT_KEY_BUILDING_PYRAMIDS") + getIcon(bLibrary) + text("TXT_KEY_BUILDING_GREAT_LIBRARY") + getIcon(bLighthouse) + text("TXT_KEY_BUILDING_GREAT_LIGHTHOUSE"))
		elif iGoal == 2:
			iCulture = pPlayer.countTotalCulture()
			aHelp.append(getIcon(iCulture >= turns(5000)) + text("TXT_KEY_VICTORY_TOTAL_CULTURE", iCulture, turns(5000)))

	elif iCiv == iHarappa:
		if iGoal == 1:
			iNumReservoirs = getNumBuildings(iPlayer, iReservoir)
			iNumGranaries = getNumBuildings(iPlayer, iGranary)
			iNumSmokehouses = getNumBuildings(iPlayer, iSmokehouse)
			aHelp.append(getIcon(iNumReservoirs >= 3) + text("TXT_KEY_VICTORY_NUM_RESERVOIRS", iNumReservoirs, 3) + ' ' + getIcon(iNumGranaries >= 2) + text("TXT_KEY_VICTORY_NUM_GRANARIES", iNumGranaries, 2) + ' ' + getIcon(iNumSmokehouses >= 2) + text("TXT_KEY_VICTORY_NUM_SMOKEHOUSES", iNumSmokehouses, 2))
		elif iGoal == 2:
			iNumPopulation = pPlayer.getTotalPopulation()
			aHelp.append(getIcon(iNumPopulation >= 30) + text("TXT_KEY_VICTORY_TOTAL_POPULATION", iNumPopulation, 30))
			
	elif iCiv == iBabylonia:
		if iGoal == 0:
			bConstruction = data.lFirstDiscovered[iConstruction] == iPlayer
			bArithmetics = data.lFirstDiscovered[iArithmetics] == iPlayer
			bWriting = data.lFirstDiscovered[iWriting] == iPlayer
			bCalendar = data.lFirstDiscovered[iCalendar] == iPlayer
			bContract = data.lFirstDiscovered[iContract] == iPlayer
			aHelp.append(getIcon(bConstruction) + text("TXT_KEY_TECH_CONSTRUCTION") + ' ' + getIcon(bArithmetics) + text("TXT_KEY_TECH_ARITHMETICS") + ' ' + getIcon(bWriting) + text("TXT_KEY_TECH_WRITING"))
			aHelp.append(getIcon(bCalendar) + text("TXT_KEY_TECH_CALENDAR") + ' ' + getIcon(bContract) + text("TXT_KEY_TECH_CONTRACT"))
		elif iGoal == 1:
			pBestCity = getBestCity(iPlayer, (76, 40), cityPopulation)
			bBestCity = isBestCity(iPlayer, (76, 40), cityPopulation)
			aHelp.append(getIcon(bBestCity) + text("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", pBestCity.getName()))
		elif iGoal == 2:
			pBestCity = getBestCity(iPlayer, (76, 40), cityCulture)
			bBestCity = isBestCity(iPlayer, (76, 40), cityCulture)
			aHelp.append(getIcon(bBestCity) + text("TXT_KEY_VICTORY_MOST_CULTURED_CITY", pBestCity.getName()))
			
	elif iCiv == iChina:
		if iGoal == 0:
			iConfucianCounter = getNumBuildings(iPlayer, iConfucianCathedral)
			iTaoistCounter = getNumBuildings(iPlayer, iTaoistCathedral)
			aHelp.append(getIcon(iConfucianCounter >= 2) + text("TXT_KEY_VICTORY_NUM_CONFUCIAN_ACADEMIES", iConfucianCounter, 2) + ' ' + getIcon(iTaoistCounter >= 2) + text("TXT_KEY_VICTORY_NUM_TAOIST_PAGODAS", iTaoistCounter, 2))
		elif iGoal == 1:
			bCompass = data.lFirstDiscovered[iCompass] == iPlayer
			bPaper = data.lFirstDiscovered[iPaper] == iPlayer
			bGunpowder = data.lFirstDiscovered[iGunpowder] == iPlayer
			bPrintingPress = data.lFirstDiscovered[iPrinting] == iPlayer
			aHelp.append(getIcon(bCompass) + text("TXT_KEY_TECH_COMPASS") + ' ' + getIcon(bPaper) + text("TXT_KEY_TECH_PAPER") + ' ' + getIcon(bGunpowder) + text("TXT_KEY_TECH_GUNPOWDER") + ' ' + getIcon(bPrintingPress) + text("TXT_KEY_TECH_PRINTING"))
		elif iGoal == 2:
			iGoldenAgeTurns = data.iChineseGoldenAgeTurns
			aHelp.append(getIcon(iGoldenAgeTurns >= turns(32)) + text("TXT_KEY_VICTORY_GOLDEN_AGES", iGoldenAgeTurns / turns(8), 4))

	elif iCiv == iGreece:
		if iGoal == 0:
			bMathematics = data.lFirstDiscovered[iMathematics] == iPlayer
			bLiterature = data.lFirstDiscovered[iLiterature] == iPlayer
			bAesthetics = data.lFirstDiscovered[iAesthetics] == iPlayer
			bPhilosophy = data.lFirstDiscovered[iPhilosophy] == iPlayer
			bMedicine = data.lFirstDiscovered[iMedicine] == iPlayer
			aHelp.append(getIcon(bMathematics) + text("TXT_KEY_TECH_MATHEMATICS") + ' ' + getIcon(bLiterature) + text("TXT_KEY_TECH_LITERATURE") + ' ' + getIcon(bAesthetics) + text("TXT_KEY_TECH_AESTHETICS"))
			aHelp.append(getIcon(bPhilosophy) + text("TXT_KEY_TECH_PHILOSOPHY") + ' ' + getIcon(bMedicine) + text("TXT_KEY_TECH_MEDICINE"))
		elif iGoal == 1:
			bEgypt = checkOwnedCiv(iPlayer, iEgypt)
			bPhoenicia = checkOwnedCiv(iPlayer, iCarthage)
			bBabylonia = checkOwnedCiv(iPlayer, iBabylonia)
			bPersia = checkOwnedCiv(iPlayer, iPersia)
			aHelp.append(getIcon(bEgypt) + text("TXT_KEY_CIV_EGYPT_SHORT_DESC") + ' ' + getIcon(bPhoenicia) + text("TXT_KEY_CIV_PHOENICIA_SHORT_DESC") + ' ' + getIcon(bBabylonia) + text("TXT_KEY_CIV_BABYLONIA_SHORT_DESC") + ' ' + getIcon(bPersia) + text("TXT_KEY_CIV_PERSIA_SHORT_DESC"))
		elif iGoal == 2:
			bParthenon = (getNumBuildings(iPlayer, iParthenon) > 0)
			bColossus = (getNumBuildings(iPlayer, iColossus) > 0)
			bStatueOfZeus = (getNumBuildings(iPlayer, iStatueOfZeus) > 0)
			bArtemis = (getNumBuildings(iPlayer, iTempleOfArtemis) > 0)
			aHelp.append(getIcon(bParthenon) + text("TXT_KEY_BUILDING_PARTHENON") + ' ' + getIcon(bColossus) + text("TXT_KEY_BUILDING_COLOSSUS") + ' ' + getIcon(bStatueOfZeus) + text("TXT_KEY_BUILDING_STATUE_OF_ZEUS") + ' ' + getIcon(bArtemis) + text("TXT_KEY_BUILDING_TEMPLE_OF_ARTEMIS"))

	elif iCiv == iIndia:
		if iGoal == 0:
			bBuddhistShrine = (getNumBuildings(iPlayer, iBuddhistShrine) > 0)
			bHinduShrine = (getNumBuildings(iPlayer, iHinduShrine) > 0)
			aHelp.append(getIcon(bHinduShrine) + text("TXT_KEY_VICTORY_HINDU_SHRINE") + ' ' + getIcon(bBuddhistShrine) + text("TXT_KEY_VICTORY_BUDDHIST_SHRINE"))
		elif iGoal == 1:
			lTemples = [iTemple + 4 * i for i in range(iNumReligions)]
			iCounter = 0
			for iGoalTemple in lTemples:
				iCounter += getNumBuildings(iPlayer, iGoalTemple)
			aHelp.append(getIcon(iCounter >= 20) + text("TXT_KEY_VICTORY_TEMPLES_BUILT", iCounter, 20))
		elif iGoal == 2:
			popPercent = getPopulationPercent(iPlayer)
			aHelp.append(getIcon(popPercent >= 20.0) + text("TXT_KEY_VICTORY_PERCENTAGE_WORLD_POPULATION", "%.2f%%" % popPercent, 20))

	elif iCiv == iCarthage:
		if iGoal == 0:
			bPalace = isBuildingInCity((58, 39), iPalace)
			bGreatCothon = isBuildingInCity((58, 39), iGreatCothon)
			aHelp.append(getIcon(bPalace) + text("TXT_KEY_BUILDING_PALACE") + ' ' + getIcon(bGreatCothon) + text("TXT_KEY_BUILDING_GREAT_COTHON"))
		elif iGoal == 1:
			bItaly = isControlled(iPlayer, plots.rectangle(dNormalArea[iItaly]).without((62, 47), (63, 47), (63, 46)))
			bIberia = isControlled(iPlayer, plots.rectangle(tIberia))
			aHelp.append(getIcon(bItaly) + text("TXT_KEY_VICTORY_ITALY") + ' ' + getIcon(bIberia) + text("TXT_KEY_VICTORY_IBERIA_CARTHAGE"))
		elif iGoal == 2:
			iTreasury = pPlayer.getGold()
			aHelp.append(getIcon(iTreasury >= turns(5000)) + text("TXT_KEY_VICTORY_TOTAL_GOLD", iTreasury, turns(5000)))

	elif iCiv == iPolynesia:
		if iGoal == 0 or iGoal == 1:
			bHawaii = cities.rectangle(tHawaii).owner(iPlayer).any()
			bNewZealand = cities.rectangle(tNewZealand).owner(iPlayer).any()
			bMarquesas = cities.rectangle(tMarquesas).owner(iPlayer).any()
			bEasterIsland = cities.rectangle(tEasterIsland).owner(iPlayer).any()
			aHelp.append(getIcon(bHawaii) + text("TXT_KEY_VICTORY_HAWAII") + getIcon(bNewZealand) + text("TXT_KEY_VICTORY_NEW_ZEALAND") + getIcon(bMarquesas) + text("TXT_KEY_VICTORY_MARQUESAS") + getIcon(bEasterIsland) + text("TXT_KEY_VICTORY_EASTER_ISLAND"))

	elif iCiv == iPersia:
		if iGoal == 0:
			landPercent = getLandPercent(iPlayer)
			aHelp.append(getIcon(landPercent >= 6.995) + text("TXT_KEY_VICTORY_PERCENTAGE_WORLD_TERRITORY", "%.2f%%" % landPercent, '7'))
		elif iGoal == 1:
			iCounter = countWonders(iPlayer)
			aHelp.append(getIcon(iCounter >= 7) + text("TXT_KEY_VICTORY_NUM_WONDERS", iCounter, 7))
		elif iGoal == 2:
			iCounter = countShrines(iPlayer)
			aHelp.append(getIcon(iCounter >= 2) + text("TXT_KEY_VICTORY_NUM_SHRINES", iCounter, 2))
				
	elif iCiv == iRome:
		if iGoal == 0:
			iNumBarracks = getNumBuildings(iPlayer, iBarracks)
			iNumAqueducts = getNumBuildings(iPlayer, iAqueduct)
			iNumArenas = getNumBuildings(iPlayer, iArena)
			iNumForums = getNumBuildings(iPlayer, iForum)
			aHelp.append(getIcon(iNumBarracks >= 6) + text("TXT_KEY_VICTORY_NUM_BARRACKS", iNumBarracks, 6) + ' ' + getIcon(iNumAqueducts >= 5) + text("TXT_KEY_VICTORY_NUM_AQUEDUCTS", iNumAqueducts, 5) + ' ' + getIcon(iNumArenas >= 4) + text("TXT_KEY_VICTORY_NUM_ARENAS", iNumArenas, 4) + ' ' + getIcon(iNumForums >= 3) + text("TXT_KEY_VICTORY_NUM_FORUMS", iNumForums, 3))
		elif iGoal == 1:
			iCitiesSpain = cities.normal(iSpain).owner(iPlayer).count()
			iCitiesFrance = cities.rectangle(tGaul).owner(iPlayer).count()
			iCitiesEngland = cities.core(iEngland).owner(iPlayer).count()
			iCitiesCarthage = cities.rectangle(tAfrica).owner(iPlayer).count()
			iCitiesByzantium = cities.core(iByzantium).owner(iPlayer).count()
			iCitiesEgypt = cities.core(iEgypt).owner(iPlayer).count()
			aHelp.append(getIcon(iCitiesSpain >= 2) + text("TXT_KEY_VICTORY_ROME_CONTROL_SPAIN", iCitiesSpain, 2) + ' ' + getIcon(iCitiesFrance >= 3) + text("TXT_KEY_VICTORY_ROME_CONTROL_FRANCE", iCitiesFrance, 3) + ' ' + getIcon(iCitiesEngland >= 1) + text("TXT_KEY_VICTORY_ROME_CONTROL_ENGLAND", iCitiesEngland, 1))
			aHelp.append(getIcon(iCitiesCarthage >= 2) + text("TXT_KEY_VICTORY_ROME_CONTROL_CARTHAGE", iCitiesCarthage, 2) + ' ' + getIcon(iCitiesByzantium >= 4) + text("TXT_KEY_VICTORY_ROME_CONTROL_BYZANTIUM", iCitiesByzantium, 4) + ' ' + getIcon(iCitiesEgypt >= 2) + text("TXT_KEY_VICTORY_ROME_CONTROL_EGYPT", iCitiesEgypt, 2))
		elif iGoal == 2:
			bArchitecture = data.lFirstDiscovered[iArchitecture] == iPlayer
			bPolitics = data.lFirstDiscovered[iPolitics] == iPlayer
			bScholarship = data.lFirstDiscovered[iScholarship] == iPlayer
			bMachinery = data.lFirstDiscovered[iMachinery] == iPlayer
			bCivilService = data.lFirstDiscovered[iCivilService] == iPlayer
			aHelp.append(getIcon(bArchitecture) + text("TXT_KEY_TECH_ARCHITECTURE") + ' ' + getIcon(bPolitics) + text("TXT_KEY_TECH_POLITICS") + ' ' + getIcon(bScholarship) + text("TXT_KEY_TECH_SCHOLARSHIP"))
			aHelp.append(getIcon(bMachinery) + text("TXT_KEY_TECH_MACHINERY") + ' ' + getIcon(bCivilService) + text("TXT_KEY_TECH_CIVIL_SERVICE"))

	# Maya goals have no stages

	elif iCiv == iTamils:
		if iGoal == 0:
			iTreasury = pPlayer.getGold()
			iCulture = pPlayer.countTotalCulture()
			aHelp.append(getIcon(iTreasury >= turns(3000)) + text("TXT_KEY_VICTORY_TOTAL_GOLD", iTreasury, turns(3000)))
			aHelp.append(getIcon(iCulture >= turns(2000)) + text("TXT_KEY_VICTORY_TOTAL_CULTURE", iCulture, turns(2000)))
		elif iGoal == 1:
			bDeccan = isControlledOrVassalized(iPlayer, plots.rectangle(tDeccan))
			bSrivijaya = isControlledOrVassalized(iPlayer, plots.rectangle(tSrivijaya))
			aHelp.append(getIcon(bDeccan) + text("TXT_KEY_VICTORY_DECCAN") + ' ' + getIcon(bSrivijaya) + text("TXT_KEY_VICTORY_SRIVIJAYA"))
		elif iGoal == 2:
			iTradeGold = data.iTamilTradeGold / 100
			aHelp.append(getIcon(iTradeGold >= turns(4000)) + text("TXT_KEY_VICTORY_TRADE_GOLD", iTradeGold, turns(4000)))

	elif iCiv == iEthiopia:
		if iGoal == 0:
			iNumIncense = pPlayer.getNumAvailableBonuses(iIncense)
			aHelp.append(getIcon(iNumIncense >= 3) + text("TXT_KEY_VICTORY_AVAILABLE_INCENSE_RESOURCES", iNumIncense, 3))
		elif iGoal == 1:
			bConverted = data.bEthiopiaConverted
			iNumOrthodoxCathedrals = getNumBuildings(iPlayer, iOrthodoxCathedral)
			iGreatProphets = countSpecialists(iPlayer, iSpecialistGreatProphet)
			aHelp.append(getIcon(bConverted) + text("TXT_KEY_VICTORY_CONVERTED_TO_ORTHODOXY"))
			aHelp.append(getIcon(iNumOrthodoxCathedrals >= 1) + text("TXT_KEY_BUILDING_ORTHODOX_CATHEDRAL"))
			aHelp.append(getIcon(iGreatProphets >= 3) + text("TXT_KEY_VICTORY_GREAT_PROPHETS", iGreatProphets, 3))
		elif iGoal == 2:
			iOrthodoxCities = countRegionReligion(iOrthodoxy, lAfrica)
			iMuslimCities = countRegionReligion(iIslam, lAfrica)
			aHelp.append(getIcon(iOrthodoxCities > iMuslimCities) + text("TXT_KEY_VICTORY_ORTHODOX_CITIES", iOrthodoxCities) + ' ' + text("TXT_KEY_VICTORY_MUSLIM_CITIES", iMuslimCities))

	elif iCiv == iKorea:
		if iGoal == 0:
			bConfucianCathedral = (getNumBuildings(iPlayer, iConfucianCathedral) > 0)
			bBuddhistCathedral = (getNumBuildings(iPlayer, iBuddhistCathedral) > 0)
			aHelp.append(getIcon(bBuddhistCathedral) + text("TXT_KEY_BUILDING_BUDDHIST_CATHEDRAL") + ' ' + getIcon(bConfucianCathedral) + text("TXT_KEY_BUILDING_CONFUCIAN_CATHEDRAL"))
		elif iGoal == 2:
			iNumSinks = data.iKoreanSinks
			aHelp.append(getIcon(iNumSinks >= 20) + text("TXT_KEY_VICTORY_ENEMY_SHIPS_SUNK", iNumSinks, 20))

	elif iCiv == iByzantium:
		if iGoal == 0:
			iTreasury = pPlayer.getGold()
			aHelp.append(getIcon(iTreasury >= turns(5000)) + text("TXT_KEY_VICTORY_TOTAL_GOLD", iTreasury, turns(5000)))
		elif iGoal == 1:
			pBestPopCity = getBestCity(iPlayer, (68, 45), cityPopulation)
			bBestPopCity = isBestCity(iPlayer, (68, 45), cityPopulation)
			pBestCultureCity = getBestCity(iPlayer, (68, 45), cityCulture)
			bBestCultureCity = isBestCity(iPlayer, (68, 45), cityCulture)
			aHelp.append(getIcon(bBestPopCity) + text("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", pBestPopCity.getName()) + ' ' + getIcon(bBestCultureCity) + text("TXT_KEY_VICTORY_MOST_CULTURED_CITY", pBestCultureCity.getName()))
		elif iGoal == 2:
			iBalkans = cities.rectangle(tBalkans).owner(iPlayer).count()
			iNorthAfrica = cities.rectangle(tNorthAfrica).owner(iPlayer).count()
			iNearEast = cities.rectangle(tNearEast).owner(iPlayer).count()
			aHelp.append(getIcon(iBalkans >= 3) + text("TXT_KEY_VICTORY_BALKANS", iBalkans, 3) + ' ' + getIcon(iNorthAfrica >= 3) + text("TXT_KEY_VICTORY_NORTH_AFRICA", iNorthAfrica, 3) + ' ' + getIcon(iNearEast >= 3) + text("TXT_KEY_VICTORY_NEAR_EAST", iNearEast, 3))

	elif iCiv == iJapan:
		if iGoal == 0:
			iAverageCulture = getAverageCulture(iPlayer)
			aHelp.append(getIcon(iAverageCulture >= turns(6000)) + text("TXT_KEY_VICTORY_AVERAGE_CULTURE", iAverageCulture, turns(6000)))
		elif iGoal == 1:
			bKorea = isControlledOrVassalized(iPlayer, plots.rectangle(tKorea))
			bManchuria = isControlledOrVassalized(iPlayer, plots.rectangle(tManchuria))
			bChina = isControlledOrVassalized(iPlayer, plots.rectangle(tChina))
			bIndochina = isControlledOrVassalized(iPlayer, plots.rectangle(tIndochina).without(lIndochinaExceptions))
			bIndonesia = isControlledOrVassalized(iPlayer, plots.rectangle(tIndonesia))
			bPhilippines = isControlledOrVassalized(iPlayer, plots.rectangle(tPhilippines))
			aHelp.append(getIcon(bKorea) + text("TXT_KEY_CIV_KOREA_SHORT_DESC") + ' ' + getIcon(bManchuria) + text("TXT_KEY_VICTORY_MANCHURIA") + ' ' + getIcon(bChina) + text("TXT_KEY_CIV_CHINA_SHORT_DESC"))
			aHelp.append(getIcon(bIndochina) + text("TXT_KEY_VICTORY_INDOCHINA") + ' ' + getIcon(bIndonesia) + text("TXT_KEY_CIV_INDONESIA_SHORT_DESC") + ' ' + getIcon(bPhilippines) + text("TXT_KEY_VICTORY_PHILIPPINES"))
		elif iGoal == 2:
			iGlobalTechs = countFirstDiscovered(iPlayer, iGlobal)
			iDigitalTechs = countFirstDiscovered(iPlayer, iDigital)
			aHelp.append(getIcon(iGlobalTechs >= 8) + text("TXT_KEY_VICTORY_TECHS_FIRST_DISCOVERED", infos.era(iGlobal).getText(), iGlobalTechs, 8) + ' ' + getIcon(iDigitalTechs >= 8) + text("TXT_KEY_VICTORY_TECHS_FIRST_DISCOVERED", infos.era(iDigital).getText(), iDigitalTechs, 8))
			
	elif iCiv == iVikings:
		if iGoal == 0:
			lEuroCivs = [iLoopCiv for iLoopCiv in dCivGroups[iCivGroupEurope] if dBirth[iLoopCiv] < 1050 and slot(iLoopCiv) != iPlayer]
			bEuropeanCore = isCoreControlled(iPlayer, lEuroCivs)
			aHelp.append(getIcon(bEuropeanCore) + text("TXT_KEY_VICTORY_EUROPEAN_CORE"))
		elif iGoal == 2:
			iRaidGold = data.iVikingGold
			aHelp.append(getIcon(iRaidGold >= turns(3000)) + text("TXT_KEY_VICTORY_ACQUIRED_GOLD", iRaidGold, turns(3000)))
			
	elif iCiv == iTurks:
		if iGoal == 0:
			fLandPercent = getLandPercent(iPlayer)
			iPillagedImprovements = data.iTurkicPillages
			aHelp.append(getIcon(fLandPercent >= 5.995) + text("TXT_KEY_VICTORY_PERCENTAGE_WORLD_TERRITORY", "%.2f%%" % fLandPercent, '6'))
			aHelp.append(getIcon(iPillagedImprovements >= 20) + text("TXT_KEY_VICTORY_PILLAGED_IMPROVEMENTS", iPillagedImprovements, 20))
		elif iGoal == 1:
			bConnected = isConnectedByTradeRoute(iPlayer, plots.rectangle(tChina), lMediterraneanPorts)
			iSilkRouteCities = pPlayer.countCorporations(iSilkRoute)
			aHelp.append(getIcon(bConnected) + text("TXT_KEY_VICTORY_SILK_ROUTE_CONNECTION"))
			aHelp.append(getIcon(iSilkRouteCities >= 10) + text("TXT_KEY_VICTORY_CITIES_WITH_SILK_ROUTE", iSilkRouteCities, 10))
		elif iGoal == 2:
			iCultureLevel = 3
			for tCapital in [data.tFirstTurkicCapital, data.tSecondTurkicCapital]:
				if tCapital:
					iCultureLevel += 1
					capitalPlot = plot(tCapital)
					if capitalPlot.isCity():
						displayName = capitalPlot.getPlotCity().getName()
						ownName = cnm.getRenameName(iPlayer, displayName)
						if ownName: displayName = ownName
						aHelp.append(getIcon(True) + displayName)
			
			if pPlayer.getNumCities() > 0:
				capital = pPlayer.getCapitalCity()
				iCulture = capital.getCulture(iPlayer)
				iRequiredCulture = infos.culture(iCultureLevel).getSpeedThreshold(game.getGameSpeedType())
			
				if location(capital) in [data.tFirstTurkicCapital, data.tSecondTurkicCapital]:
					aHelp.append(getIcon(False) + text("TXT_KEY_VICTORY_NO_NEW_CAPITAL"))
				else:
					aHelp.append(getIcon(iCulture >= iRequiredCulture) + text("TXT_KEY_VICTORY_CAPITAL_CULTURE", capital.getName(), iCulture, iRequiredCulture))

	elif iCiv == iArabia:
		if iGoal == 0:
			iMostAdvancedCiv = getBestPlayer(iPlayer, playerTechs)
			aHelp.append(getIcon(iMostAdvancedCiv == iPlayer) + text("TXT_KEY_VICTORY_MOST_ADVANCED_CIV", name(iMostAdvancedCiv)))
		elif iGoal == 1:
			bEgypt = isControlledOrVassalized(iPlayer, plots.core(iEgypt))
			bMaghreb = isControlledOrVassalized(iPlayer, plots.rectangle(tAfrica))
			bMesopotamia = isControlledOrVassalized(iPlayer, plots.core(iBabylonia))
			bPersia = isControlledOrVassalized(iPlayer, plots.core(iPersia))
			bSpain = isControlledOrVassalized(iPlayer, plots.normal(iSpain))
			aHelp.append(getIcon(bEgypt) + text("TXT_KEY_CIV_EGYPT_SHORT_DESC") + ' ' + getIcon(bMaghreb) + text("TXT_KEY_VICTORY_MAGHREB") + ' ' + getIcon(bSpain) + text("TXT_KEY_CIV_SPAIN_SHORT_DESC"))
			aHelp.append(getIcon(bMesopotamia) + text("TXT_KEY_VICTORY_MESOPOTAMIA") + ' ' + getIcon(bPersia) + text("TXT_KEY_CIV_PERSIA_SHORT_DESC"))
		elif iGoal == 2:
			fReligionPercent = game.calculateReligionPercent(iIslam)
			aHelp.append(getIcon(fReligionPercent >= 30.0) + text("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", infos.religion(iIslam).getTextKey(), "%.2f%%" % fReligionPercent, 30))

	elif iCiv == iTibet:
		if iGoal == 0:
			iNumCities = pPlayer.getNumCities()
			aHelp.append(getIcon(iNumCities >= 5) + text("TXT_KEY_VICTORY_CITIES_ACQUIRED", iNumCities, 5))
		elif iGoal == 1:
			fReligionPercent = game.calculateReligionPercent(iBuddhism)
			aHelp.append(getIcon(fReligionPercent >= 25.0) + text("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", infos.religion(iBuddhism).getTextKey(), "%.2f%%" % fReligionPercent, 25))
		elif iGoal == 2:
			iCounter = countCitySpecialists(iPlayer, plots.capital(iTibet), iSpecialistGreatProphet)
			aHelp.append(getIcon(iCounter >= 5) + text("TXT_KEY_VICTORY_GREAT_PROPHETS_SETTLED", "Lhasa", iCounter, 5))

	elif iCiv == iIndonesia:
		if iGoal == 0:
			iHighestCiv = getBestPlayer(iPlayer, playerRealPopulation)
			bHighest = (iHighestCiv == iPlayer)
			aHelp.append(getIcon(bHighest) + text("TXT_KEY_VICTORY_HIGHEST_POPULATION_CIV", name(iHighestCiv)))
		elif iGoal == 1:
			iCounter = countHappinessResources(iPlayer)
			aHelp.append(getIcon(iCounter >= 10) + text("TXT_KEY_VICTORY_NUM_HAPPINESS_RESOURCES", iCounter, 10))
		elif iGoal == 2:
			popPercent = getPopulationPercent(iPlayer)
			aHelp.append(getIcon(popPercent >= 9.0) + text("TXT_KEY_VICTORY_PERCENTAGE_WORLD_POPULATION", "%.2f%%" % popPercent, 9))

	elif iCiv == iMoors:
		if iGoal == 0:
			iIberia = getNumConqueredCitiesInArea(iPlayer, plots.rectangle(tIberia))
			iMaghreb = getNumCitiesInArea(iPlayer, plots.rectangle(tMaghreb))
			iWestAfrica = getNumConqueredCitiesInArea(iPlayer, plots.rectangle(tWestAfrica))
			aHelp.append(getIcon(iMaghreb >= 3) + text("TXT_KEY_VICTORY_MAGHREB_MOORS", iMaghreb, 3) + ' ' + getIcon(iIberia >= 2) + text("TXT_KEY_VICTORY_IBERIA", iIberia, 2) + ' ' + getIcon(iWestAfrica >= 2) + text("TXT_KEY_VICTORY_WEST_AFRICA", iWestAfrica, 2))
		elif iGoal == 1:
			bMezquita = data.getWonderBuilder(iMezquita) == iPlayer
			iCounter = 0
			iCounter += countCitySpecialists(iPlayer, (51, 41), iSpecialistGreatProphet)
			iCounter += countCitySpecialists(iPlayer, (51, 41), iSpecialistGreatScientist)
			iCounter += countCitySpecialists(iPlayer, (51, 41), iSpecialistGreatEngineer)
			aHelp.append(getIcon(bMezquita) + text("TXT_KEY_BUILDING_LA_MEZQUITA") + ' ' + getIcon(iCounter >= 4) + text("TXT_KEY_VICTORY_GREAT_PEOPLE_IN_CITY_MOORS", "Cordoba", iCounter, 4))
		elif iGoal == 2:
			iRaidGold = data.iMoorishGold
			aHelp.append(getIcon(iRaidGold >= turns(3000)) + text("TXT_KEY_VICTORY_PIRACY", iRaidGold, turns(3000)))

	elif iCiv == iSpain:
		if iGoal == 1:
			iNumGold = countResources(iPlayer, iGold)
			iNumSilver = countResources(iPlayer, iSilver)
			aHelp.append(getIcon(iNumGold + iNumSilver >= 10) + text("TXT_KEY_VICTORY_GOLD_SILVER_RESOURCES", iNumGold + iNumSilver, 10))
		elif iGoal == 2:
			fReligionPercent = game.calculateReligionPercent(iCatholicism)
			bNoProtestants = not isStateReligionInArea(iProtestantism, tEurope) and not isStateReligionInArea(iProtestantism, tEasternEurope)
			aHelp.append(getIcon(fReligionPercent >= 30.0) + text("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", infos.religion(iCatholicism).getTextKey(), "%.2f%%" % fReligionPercent, 30) + ' ' + getIcon(bNoProtestants) + text("TXT_KEY_VICTORY_NO_PROTESTANTS"))

	elif iCiv == iFrance:
		if iGoal == 0:
			iCulture = getCityCulture(iPlayer, tParis)
			aHelp.append(getIcon(iCulture >= turns(50000)) + text("TXT_KEY_VICTORY_CITY_CULTURE", "Paris", iCulture, turns(50000)))
		elif iGoal == 1:
			iEurope, iTotalEurope = countControlledTiles(iPlayer, plots.rectangle(tEurope), True)
			iEasternEurope, iTotalEasternEurope = countControlledTiles(iPlayer, plots.rectangle(tEasternEurope), True)
			iNorthAmerica, iTotalNorthAmerica = countControlledTiles(iPlayer, plots.rectangle(tNorthAmerica), True)
			fEurope = (iEurope + iEasternEurope) * 100.0 / (iTotalEurope + iTotalEasternEurope)
			fNorthAmerica = iNorthAmerica * 100.0 / iTotalNorthAmerica
			aHelp.append(getIcon(fEurope >= 40.0) + text("TXT_KEY_VICTORY_EUROPEAN_TERRITORY", "%.2f%%" % fEurope, '40') + ' ' + getIcon(fNorthAmerica >= 40.0) + text("TXT_KEY_VICTORY_NORTH_AMERICAN_TERRITORY", "%.2f%%" % fNorthAmerica, '40'))
		elif iGoal == 2:
			bNotreDame = data.getWonderBuilder(iNotreDame) == iPlayer
			bVersailles = data.getWonderBuilder(iVersailles) == iPlayer
			bLouvre = data.getWonderBuilder(iLouvre) == iPlayer
			bEiffelTower = data.getWonderBuilder(iEiffelTower) == iPlayer
			bMetropolitain = data.getWonderBuilder(iMetropolitain) == iPlayer
			aHelp.append(getIcon(bNotreDame) + text("TXT_KEY_BUILDING_NOTRE_DAME") + ' ' + getIcon(bVersailles) + text("TXT_KEY_BUILDING_VERSAILLES") + ' ' + getIcon(bLouvre) + text("TXT_KEY_BUILDING_LOUVRE"))
			aHelp.append(getIcon(bEiffelTower) + text("TXT_KEY_BUILDING_EIFFEL_TOWER") + ' ' + getIcon(bMetropolitain) + text("TXT_KEY_BUILDING_METROPOLITAIN"))

	elif iCiv == iKhmer:
		if iGoal == 0:
			iNumBuddhism = getNumBuildings(iPlayer, iBuddhistMonastery)
			iNumHinduism = getNumBuildings(iPlayer, iHinduMonastery)
			bWatPreahPisnulok = data.getWonderBuilder(iWatPreahPisnulok) == iPlayer
			aHelp.append(getIcon(iNumBuddhism >= 4) + text("TXT_KEY_VICTORY_NUM_BUDDHIST_MONASTERIES", iNumBuddhism, 4) + ' ' + getIcon(iNumHinduism >= 4) + text("TXT_KEY_VICTORY_NUM_HINDU_MONASTERIES", iNumHinduism, 4) + ' ' + getIcon(bWatPreahPisnulok) + text("TXT_KEY_BUILDING_WAT_PREAH_PISNULOK"))
		elif iGoal == 1:
			fPopPerCity = getAverageCitySize(iPlayer)
			aHelp.append(getIcon(fPopPerCity >= 12.0) + text("TXT_KEY_VICTORY_AVERAGE_CITY_POPULATION", "%.2f" % fPopPerCity, "%d" % 12))
		elif iGoal == 2:
			iCulture = pPlayer.countTotalCulture()
			aHelp.append(getIcon(iCulture >= turns(8000)) + text("TXT_KEY_VICTORY_TOTAL_CULTURE", iCulture, turns(8000)))

	elif iCiv == iEngland:
		if iGoal == 0:
			iNAmerica = getNumCitiesInRegions(iPlayer, lNorthAmerica)
			iSCAmerica = getNumCitiesInRegions(iPlayer, lSouthAmerica)
			iAfrica = getNumCitiesInRegions(iPlayer, lAfrica)
			iAsia = getNumCitiesInRegions(iPlayer, lAsia)
			iOceania = getNumCitiesInRegions(iPlayer, lOceania)
			aHelp.append(getIcon(iNAmerica >= 5) + text("TXT_KEY_VICTORY_ENGLAND_CONTROL_NORTH_AMERICA", iNAmerica, 5) + ' ' + getIcon(iAsia >= 5) + text("TXT_KEY_VICTORY_ENGLAND_CONTROL_ASIA", iAsia, 5) + ' ' + getIcon(iAfrica >= 4) + text("TXT_KEY_VICTORY_ENGLAND_CONTROL_AFRICA", iAfrica, 4))
			aHelp.append(getIcon(iSCAmerica >= 3) + text("TXT_KEY_VICTORY_ENGLAND_CONTROL_SOUTH_AMERICA", iSCAmerica, 3))
			aHelp.append(getIcon(iOceania >= 3) + text("TXT_KEY_VICTORY_ENGLAND_CONTROL_OCEANIA", iOceania, 3))
		elif iGoal == 1:
			iEnglishNavy = 0
			iEnglishNavy += pPlayer.getUnitClassCount(infos.unit(iFrigate).getUnitClassType())
			iEnglishNavy += pPlayer.getUnitClassCount(infos.unit(iShipOfTheLine).getUnitClassType())
			iEnglishSinks = data.iEnglishSinks
			aHelp.append(getIcon(iEnglishNavy >= 25) + text("TXT_KEY_VICTORY_NAVY_SIZE", iEnglishNavy, 25) + ' ' + getIcon(iEnglishSinks >= 50) + text("TXT_KEY_VICTORY_ENEMY_SHIPS_SUNK", iEnglishSinks, 50))
		elif iGoal == 2:
			iRenaissanceTechs = countFirstDiscovered(iPlayer, iRenaissance)
			iIndustrialTechs = countFirstDiscovered(iPlayer, iIndustrial)
			aHelp.append(getIcon(iRenaissanceTechs >= 8) + text("TXT_KEY_VICTORY_TECHS_FIRST_DISCOVERED", infos.era(iRenaissance).getText(), iRenaissanceTechs, 8) + ' ' + getIcon(iIndustrialTechs >= 8) + text("TXT_KEY_VICTORY_TECHS_FIRST_DISCOVERED", infos.era(iIndustrial).getText(), iIndustrialTechs, 8))

	elif iCiv == iHolyRome:
		if iGoal == 0:
			bSaintPeters = data.lHolyRomanShrines[0] or getNumBuildings(iPlayer, iCatholicShrine) > 0
			bAnastasis = data.lHolyRomanShrines[1] or getNumBuildings(iPlayer, iOrthodoxShrine) > 0
			bAllSaints = data.lHolyRomanShrines[2] or getNumBuildings(iPlayer, iProtestantShrine) > 0
			aHelp.append(getIcon(bSaintPeters) + text("TXT_KEY_BUILDING_CATHOLIC_SHRINE") + ' ' + getIcon(bAnastasis) + text("TXT_KEY_BUILDING_ORTHODOX_SHRINE") + ' ' + getIcon(bAllSaints) + text("TXT_KEY_BUILDING_PROTESTANT_SHRINE"))
		elif iGoal == 1:
			iNumVassals = countVassals(iPlayer, dCivGroups[iCivGroupEurope], iCatholicism)
			aHelp.append(getIcon(iNumVassals >= 3) + text("TXT_KEY_VICTORY_CATHOLIC_EUROPEAN_VASSALS", iNumVassals, 3))
		elif iGoal == 2:
			iGreatArtists = countCitySpecialists(iPlayer, tVienna, iSpecialistGreatArtist)
			iGreatStatesmen = countCitySpecialists(iPlayer, tVienna, iSpecialistGreatStatesman)
			iPleasedOrBetterEuropeans = countPlayersWithAttitudeInGroup(iPlayer, AttitudeTypes.ATTITUDE_PLEASED, dCivGroups[iCivGroupEurope])
			aHelp.append(getIcon(iGreatArtists + iGreatStatesmen >= 10) + text("TXT_KEY_VICTORY_GREAT_ARTISTS_AND_STATESMEN_SETTLED", 'Vienna', iGreatArtists + iGreatStatesmen, 10))
			aHelp.append(getIcon(iPleasedOrBetterEuropeans >= 8) + text("TXT_KEY_VICTORY_PLEASED_OR_FRIENDLY_EUROPEANS", iPleasedOrBetterEuropeans, 8))

	elif iCiv == iRussia:
		if iGoal == 0:
			iSiberia = getNumFoundedCitiesInArea(iPlayer, plots.rectangle(tSiberia))
			bSiberia = iSiberia >= 7 or scenario() == i1700AD
			siberiaText = text("TXT_KEY_VICTORY_RUSSIA_CONTROL_SIBERIA", iSiberia, 7)
			if bSiberia: siberiaText = text("TXT_KEY_VICTORY_RUSSIA_CONTROL_SIBERIA_COMPLETE") 
			bSiberianRailway = isConnectedByRailroad(iPlayer, plots.capital(iRussia), lSiberianCoast)
			aHelp.append(getIcon(bSiberia) + siberiaText + ' ' + getIcon(bSiberianRailway) + text("TXT_KEY_VICTORY_TRANSSIBERIAN_RAILWAY"))
		elif iGoal == 1:
			bManhattanProject = team(iPlayer).getProjectCount(iManhattanProject) > 0
			bApolloProgram = team(iPlayer).getProjectCount(iLunarLanding) > 0
			aHelp.append(getIcon(bManhattanProject) + text("TXT_KEY_PROJECT_MANHATTAN_PROJECT") + ' ' + getIcon(bApolloProgram) + text("TXT_KEY_PROJECT_LUNAR_LANDING"))
		elif iGoal == 2:
			bCommunism = isCommunist(iPlayer)
			iCount = countPlayersWithAttitudeAndCriteria(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY, isCommunist)
			aHelp.append(getIcon(bCommunism) + text("TXT_KEY_VICTORY_COMMUNISM") + ' ' + getIcon(iCount >= 5) + text("TXT_KEY_VICTORY_FRIENDLY_WITH_COMMUNISM", iCount, 5))

	elif iCiv == iMali:
		if iGoal == 1:
			sankore = cities.owner(iPlayer).where(lambda city: city.isHasRealBuilding(iUniversityOfSankore))
			bSankore = sankore.any()
			iProphets = 0
			if sankore:
				iProphets = sankore.first().getFreeSpecialistCount(iSpecialistGreatProphet)
			aHelp.append(getIcon(bSankore) + text("TXT_KEY_BUILDING_UNIVERSITY_OF_SANKORE") + ' ' + getIcon(iProphets >= 1) + text("TXT_KEY_VICTORY_SANKORE_PROPHETS", iProphets, 1))
		elif iGoal == 2:
			iTreasury = pPlayer.getGold()
			iThreshold = 5000
			if year() > year(1500): iThreshold = 15000
			aHelp.append(getIcon(iTreasury >= turns(iThreshold)) + text("TXT_KEY_VICTORY_TOTAL_GOLD", iTreasury, turns(iThreshold)))
		
	elif iCiv == iPoland:
		if iGoal == 0:
			lCities = getLargestCities(iPlayer, 3)
			bCity1 = len(lCities) > 0
			bCity2 = len(lCities) > 1
			bCity3 = len(lCities) > 2
			if not bCity1: aHelp.append(getIcon(False) + text("TXT_KEY_VICTORY_NO_CITIES"))
			if bCity1: aHelp.append(getIcon(lCities[0].getPopulation() >= 12) + text("TXT_KEY_VICTORY_CITY_SIZE", lCities[0].getName(), lCities[0].getPopulation(), 12))
			if bCity2: aHelp.append(getIcon(lCities[1].getPopulation() >= 12) + text("TXT_KEY_VICTORY_CITY_SIZE", lCities[1].getName(), lCities[1].getPopulation(), 12))
			if bCity3: aHelp.append(getIcon(lCities[2].getPopulation() >= 12) + text("TXT_KEY_VICTORY_CITY_SIZE", lCities[2].getName(), lCities[2].getPopulation(), 12))
		elif iGoal == 2:
			iCatholic = getNumBuildings(iPlayer, iCatholicCathedral)
			iOrthodox = getNumBuildings(iPlayer, iOrthodoxCathedral)
			iProtestant = getNumBuildings(iPlayer, iProtestantCathedral)
			iCathedrals = iCatholic + iOrthodox + iProtestant
			aHelp.append(getIcon(iCathedrals >= 3) + text("TXT_KEY_VICTORY_CHRISTIAN_CATHEDRALS", iCathedrals, 3))

	elif iCiv == iPortugal:
		if iGoal == 0:
			iCount = countOpenBorders(iPlayer)
			aHelp.append(getIcon(iCount >= 14) + text("TXT_KEY_VICTORY_OPEN_BORDERS", iCount, 14))
		elif iGoal == 1:
			iCount = countAcquiredResources(iPlayer, lColonialResources)
			aHelp.append(getIcon(iCount >= 12) + text("TXT_KEY_VICTORY_COLONIAL_RESOURCES", iCount, 12))
		elif iGoal == 2:
			iColonies = getNumCitiesInArea(iPlayer, plots.rectangle(tBrazil))
			iColonies += getNumCitiesInRegions(iPlayer, lAfrica)
			iColonies += getNumCitiesInRegions(iPlayer, lAsia)
			aHelp.append(getIcon(iColonies >= 15) + text("TXT_KEY_VICTORY_EXTRA_EUROPEAN_COLONIES", iColonies, 15))

	elif iCiv == iInca:
		if iGoal == 0:
			bRoad = isRoad(iPlayer, lAndeanCoast)
			iTambos = getNumBuildings(iPlayer, iTambo)
			aHelp.append(getIcon(bRoad) + text("TXT_KEY_VICTORY_ANDEAN_ROAD") + ' ' + getIcon(iTambos >= 5) + text("TXT_KEY_VICTORY_NUM_TAMBOS", iTambos, 5))
		elif iGoal == 1:
			iTreasury = pPlayer.getGold()
			aHelp.append(getIcon(iTreasury >= turns(2500)) + text("TXT_KEY_VICTORY_TOTAL_GOLD", iTreasury, turns(2500)))
		elif iGoal == 2:
			bSouthAmerica = isAreaOnlyCivs(plots.rectangle(tSouthAmerica), [iCiv])
			aHelp.append(getIcon(bSouthAmerica) + text("TXT_KEY_VICTORY_NO_FOREIGN_CITIES_SOUTH_AMERICA"))

	elif iCiv == iItaly:
		if iGoal == 0:
			bSanMarcoBasilica = data.getWonderBuilder(iSanMarcoBasilica) == iPlayer
			bSistineChapel = data.getWonderBuilder(iSistineChapel) == iPlayer
			bSantaMariaDelFiore = data.getWonderBuilder(iSantaMariaDelFiore) == iPlayer
			aHelp.append(getIcon(bSanMarcoBasilica) + text("TXT_KEY_BUILDING_SAN_MARCO_BASILICA") + ' ' + getIcon(bSistineChapel) + text("TXT_KEY_BUILDING_SISTINE_CHAPEL") + ' ' + getIcon(bSantaMariaDelFiore) + text("TXT_KEY_BUILDING_SANTA_MARIA_DEL_FIORE"))
		elif iGoal == 1:
			iCount = countCitiesWithCultureLevel(iPlayer, 5)
			aHelp.append(getIcon(iCount >= 3) + text("TXT_KEY_VICTORY_NUM_CITIES_INFLUENTIAL_CULTURE", iCount, 3))
		elif iGoal == 2:
			iMediterranean, iTotalMediterranean = countControlledTiles(iPlayer, plots.rectangle(tMediterranean).without(lMediterraneanExceptions), False, True)
			fMediterranean = iMediterranean * 100.0 / iTotalMediterranean
			aHelp.append(getIcon(fMediterranean >= 65.0) + text("TXT_KEY_VICTORY_MEDITERRANEAN_TERRITORY", "%.2f%%" % fMediterranean, '65'))

	elif iCiv == iMongols:
		if iGoal == 1:
			iRazedCities = data.iMongolRazes
			aHelp.append(getIcon(iRazedCities >= 7) + text("TXT_KEY_VICTORY_NUM_CITIES_RAZED", iRazedCities, 7))
		elif iGoal == 2:
			landPercent = getLandPercent(iPlayer)
			aHelp.append(getIcon(landPercent >= 11.995) + text("TXT_KEY_VICTORY_PERCENTAGE_WORLD_TERRITORY", "%.2f%%" % landPercent, '12'))

	elif iCiv == iMughals:
		if iGoal == 0:
			iNumMosques = getNumBuildings(iPlayer, iIslamicCathedral)
			aHelp.append(getIcon(iNumMosques >= 3) + text("TXT_KEY_VICTORY_MOSQUES_BUILT", iNumMosques, 3))
		elif iGoal == 1:
			bRedFort = data.getWonderBuilder(iRedFort) == iPlayer
			bShalimarGardens = data.getWonderBuilder(iShalimarGardens) == iPlayer
			bTajMahal = data.getWonderBuilder(iTajMahal) == iPlayer
			aHelp.append(getIcon(bRedFort) + text("TXT_KEY_BUILDING_RED_FORT") + ' ' + getIcon(bShalimarGardens) + text("TXT_KEY_BUILDING_SHALIMAR_GARDENS") + ' ' + getIcon(bTajMahal) + text("TXT_KEY_BUILDING_TAJ_MAHAL"))
		elif iGoal == 2:
			iCulture = pPlayer.countTotalCulture()
			aHelp.append(getIcon(iCulture >= turns(50000)) + text("TXT_KEY_VICTORY_TOTAL_CULTURE", iCulture, turns(50000)))

	elif iCiv == iAztecs:
		if iGoal == 0:
			pBestCity = getBestCity(iPlayer, (18, 37), cityPopulation)
			bBestCity = isBestCity(iPlayer, (18, 37), cityPopulation)
			aHelp.append(getIcon(bBestCity) + text("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", pBestCity.getName()))
		elif iGoal == 1:
			iStepPyramids = getNumBuildings(iPlayer, unique_building(iPlayer, iPaganTemple))
			iAltars = getNumBuildings(iPlayer, iSacrificialAltar)
			aHelp.append(getIcon(iStepPyramids >= 6) + text("TXT_KEY_VICTORY_NUM_STEP_PYRAMIDS", iStepPyramids, 6) + " " + getIcon(iAltars >= 6) + text("TXT_KEY_VICTORY_NUM_ALTARS", iAltars, 6))
		elif iGoal == 2:
			iEnslavedUnits = data.iAztecSlaves
			aHelp.append(getIcon(iEnslavedUnits >= 20) + text("TXT_KEY_VICTORY_ENSLAVED_UNITS", iEnslavedUnits, 20))

	elif iCiv == iOttomans:
		if iGoal == 0:
			capital = pPlayer.getCapitalCity()
			iCounter = countCityWonders(iPlayer, location(capital), False)
			aHelp.append(getIcon(iCounter >= 4) + text("TXT_KEY_VICTORY_NUM_WONDERS_CAPITAL", iCounter, 4))
		elif iGoal == 1:
			bEasternMediterranean = isCultureControlled(iPlayer, lEasternMediterranean)
			bBlackSea = isCultureControlled(iPlayer, lBlackSea)
			bCairo = controlsCity(iPlayer, tCairo)
			bMecca = controlsCity(iPlayer, tMecca)
			bBaghdad = controlsCity(iPlayer, tBaghdad)
			bVienna = controlsCity(iPlayer, tVienna)
			aHelp.append(getIcon(bEasternMediterranean) + text("TXT_KEY_VICTORY_EASTERN_MEDITERRANEAN") + ' ' + getIcon(bBlackSea) + text("TXT_KEY_VICTORY_BLACK_SEA"))
			aHelp.append(getIcon(bCairo) + text("TXT_KEY_VICTORY_CAIRO") + ' ' + getIcon(bMecca) + text("TXT_KEY_VICTORY_MECCA") + ' ' + getIcon(bBaghdad) + text("TXT_KEY_VICTORY_BAGHDAD") + ' ' + getIcon(bVienna) + text("TXT_KEY_VICTORY_VIENNA"))
		elif iGoal == 2:
			iOttomanCulture = pPlayer.countTotalCulture()
			iEuropeanCulture = getTotalCulture(dCivGroups[iCivGroupEurope])
			aHelp.append(getIcon(iOttomanCulture > iEuropeanCulture) + text("TXT_KEY_VICTORY_TOTAL_CULTURE", iOttomanCulture, iEuropeanCulture))

	elif iCiv == iThailand:
		if iGoal == 0:
			iCount = countOpenBorders(iPlayer)
			aHelp.append(getIcon(iCount >= 10) + text("TXT_KEY_VICTORY_OPEN_BORDERS", iCount, 10))
		elif iGoal == 1:
			pBestCity = getBestCity(iPlayer, (101, 33), cityPopulation)
			bBestCity = isBestCity(iPlayer, (101, 33), cityPopulation)
			if not bBestCity:
				pBestCity = getBestCity(iPlayer, (102, 33), cityPopulation)
				bBestCity = isBestCity(iPlayer, (102, 33), cityPopulation)
			aHelp.append(getIcon(bBestCity) + text("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", pBestCity.getName()))
		elif iGoal == 2:
			bSouthAsia = isAreaOnlyCivs(plots.rectangle(tSouthAsia), lSouthAsianCivs)
			aHelp.append(getIcon(bSouthAsia) + text("TXT_KEY_VICTORY_NO_SOUTH_ASIAN_COLONIES"))

	elif iCiv == iCongo:
		if iGoal == 0:
			fPercent = getApostolicVotePercent(iPlayer)
			aHelp.append(getIcon(fPercent >= 15.0) + text("TXT_KEY_VICTORY_APOSTOLIC_VOTE_PERCENT", "%.2f%%" % fPercent, 15))
		elif iGoal == 1:
			iSlaves = data.iCongoSlaveCounter
			aHelp.append(getIcon(iSlaves >= turns(1000)) + text("TXT_KEY_VICTORY_SLAVES_TRADED", iSlaves, turns(1000)))
	
	elif iCiv == iIran:
		if iGoal == 0:
			iCount = countOpenBorders(iPlayer, dCivGroups[iCivGroupEurope])
			aHelp.append(getIcon(iCount >= 6) + text("TXT_KEY_VICTORY_OPEN_BORDERS", iCount, 6))
		elif iGoal == 1:
			bMesopotamia = isControlled(iPlayer, plots.rectangle(tSafavidMesopotamia))
			bTransoxania = isControlled(iPlayer, plots.rectangle(tTransoxiana))
			bNWIndia = isControlled(iPlayer, plots.rectangle(tNorthWestIndia).without(lNorthWestIndiaExceptions))
			aHelp.append(getIcon(bMesopotamia) + text("TXT_KEY_VICTORY_MESOPOTAMIA") + ' ' + getIcon(bTransoxania) + text("TXT_KEY_VICTORY_TRANSOXANIA") + ' ' + getIcon(bNWIndia) + text("TXT_KEY_VICTORY_NORTHWEST_INDIA"))
		elif iGoal == 2:
			pBestCity = getMostCulturedCity(iPlayer)
			iCulture = pBestCity.getCulture(iPlayer)
			aHelp.append(getIcon(iCulture >= turns(20000)) + text("TXT_KEY_VICTORY_MOST_CULTURED_CITY_VALUE", pBestCity.getName(), iCulture, turns(20000)))

	elif iCiv == iNetherlands:
		if iGoal == 0:
			iMerchants = countCitySpecialists(iPlayer, plots.capital(iNetherlands), iSpecialistGreatMerchant)
			aHelp.append(getIcon(iMerchants >= 3) + text("TXT_KEY_VICTORY_GREAT_MERCHANTS_IN_CITY", "Amsterdam", iMerchants, 3))
		elif iGoal == 1:
			iColonies = data.iDutchColonies
			aHelp.append(getIcon(iColonies >= 4) + text("TXT_KEY_VICTORY_EUROPEAN_COLONIES_CONQUERED", iColonies, 4))
		elif iGoal == 2:
			iNumSpices = pPlayer.getNumAvailableBonuses(iSpices)
			aHelp.append(getIcon(iNumSpices >= 7) + text("TXT_KEY_VICTORY_AVAILABLE_SPICE_RESOURCES", iNumSpices, 7))

	elif iCiv == iGermany:
		if iGoal == 0:
			iCounter = 0
			for iSpecialist in lGreatPeople:
				iCounter += countCitySpecialists(iPlayer, plots.capital(iGermany), iSpecialist)
			aHelp.append(getIcon(iCounter >= 7) + text("TXT_KEY_VICTORY_GREAT_PEOPLE_IN_CITY", "Berlin", iCounter, 7))
		elif iGoal == 1:
			bFrance = checkOwnedCiv(iPlayer, iFrance)
			bRome = checkOwnedCiv(iPlayer, iItaly)
			bRussia = checkOwnedCiv(iPlayer, iRussia)
			bEngland = checkOwnedCiv(iPlayer, iEngland)
			bScandinavia = checkOwnedCiv(iPlayer, iVikings)
			aHelp.append(getIcon(bRome) + text("TXT_KEY_CIV_ITALY_SHORT_DESC") + ' ' + getIcon(bFrance) + text("TXT_KEY_CIV_FRANCE_SHORT_DESC") + ' ' + getIcon(bScandinavia) + text("TXT_KEY_VICTORY_SCANDINAVIA"))
			aHelp.append(getIcon(bEngland) + text("TXT_KEY_CIV_ENGLAND_SHORT_DESC") + ' ' + getIcon(bRussia) + text("TXT_KEY_CIV_RUSSIA_SHORT_DESC"))
		elif iGoal == 2:
			iIndustrialTechs = countFirstDiscovered(iPlayer, iIndustrial)
			iGlobalTechs = countFirstDiscovered(iPlayer, iGlobal)
			aHelp.append(getIcon(iIndustrialTechs >= 8) + text("TXT_KEY_VICTORY_TECHS_FIRST_DISCOVERED", infos.era(iIndustrial).getText(), iIndustrialTechs, 8) + ' ' + getIcon(iGlobalTechs >= 8) + text("TXT_KEY_VICTORY_TECHS_FIRST_DISCOVERED", infos.era(iGlobal).getText(), iGlobalTechs, 8))

	elif iCiv == iAmerica:
		if iGoal == 0:
			bAmericas = isAreaFreeOfCivs(plots.rectangle(tNorthCentralAmerica), dCivGroups[iCivGroupEurope])
			bMexico = isControlledOrVassalized(iPlayer, plots.core(iMexico))
			aHelp.append(getIcon(bAmericas) + text("TXT_KEY_VICTORY_NO_NORTH_AMERICAN_COLONIES") + ' ' + getIcon(bMexico) + text("TXT_KEY_CIV_MEXICO_SHORT_DESC"))
		elif iGoal == 1:
			bUnitedNations = data.getWonderBuilder(iUnitedNations) == iPlayer
			bBrooklynBridge = data.getWonderBuilder(iBrooklynBridge) == iPlayer
			bStatueOfLiberty = data.getWonderBuilder(iStatueOfLiberty) == iPlayer
			bGoldenGateBridge = data.getWonderBuilder(iGoldenGateBridge) == iPlayer
			bPentagon = data.getWonderBuilder(iPentagon) == iPlayer
			bEmpireState = data.getWonderBuilder(iEmpireStateBuilding) == iPlayer
			aHelp.append(getIcon(bStatueOfLiberty) + text("TXT_KEY_BUILDING_STATUE_OF_LIBERTY") + ' ' + getIcon(bBrooklynBridge) + text("TXT_KEY_BUILDING_BROOKLYN_BRIDGE") + ' ' + getIcon(bEmpireState) + text("TXT_KEY_BUILDING_EMPIRE_STATE_BUILDING"))
			aHelp.append(getIcon(bGoldenGateBridge) + text("TXT_KEY_BUILDING_GOLDEN_GATE_BRIDGE") + ' ' + getIcon(bPentagon) + text("TXT_KEY_BUILDING_PENTAGON") + ' ' + getIcon(bUnitedNations) + text("TXT_KEY_BUILDING_UNITED_NATIONS"))
		elif iGoal == 2:
			fAlliedCommercePercent = calculateAlliedCommercePercent(iPlayer)
			fAlliedPowerPercent = calculateAlliedPowerPercent(iPlayer)
			aHelp.append(getIcon(fAlliedCommercePercent >= 75.0) + text("TXT_KEY_VICTORY_ALLIED_COMMERCE_PERCENT", "%.2f%%" % fAlliedCommercePercent, 75))
			aHelp.append(getIcon(fAlliedPowerPercent >= 75.0) + text("TXT_KEY_VICTORY_ALLIED_POWER_PERCENT", "%.2f%%" % fAlliedPowerPercent, 75))

	elif iCiv == iArgentina:
		if iGoal == 0:
			iGoldenAgeTurns = data.iArgentineGoldenAgeTurns
			aHelp.append(getIcon(iGoldenAgeTurns >= turns(16)) + text("TXT_KEY_VICTORY_GOLDEN_AGES", iGoldenAgeTurns / turns(8), 2))
		elif iGoal == 1:
			iCulture = getCityCulture(iPlayer, plots.capital(iArgentina))
			aHelp.append(getIcon(iCulture >= turns(50000)) + text("TXT_KEY_VICTORY_CITY_CULTURE", "Buenos Aires", iCulture, turns(50000)))
		elif iGoal == 2:
			iGoldenAgeTurns = data.iArgentineGoldenAgeTurns
			aHelp.append(getIcon(iGoldenAgeTurns >= turns(48)) + text("TXT_KEY_VICTORY_GOLDEN_AGES", iGoldenAgeTurns / turns(8), 6))
			
	elif iCiv == iMexico:
		if iGoal == 0:
			iNumCathedrals = 0
			iStateReligion = pPlayer.getStateReligion()
			if iStateReligion >= 0:
				iStateReligionCathedral = iCathedral + 4*iStateReligion
				iNumCathedrals = getNumBuildings(iPlayer, iStateReligionCathedral)
			aHelp.append(getIcon(iNumCathedrals >= 3) + text("TXT_KEY_VICTORY_STATE_RELIGION_CATHEDRALS", infos.religion(iStateReligion).getAdjectiveKey(), iNumCathedrals, 3))
		elif iGoal == 1:
			iGenerals = data.iMexicanGreatGenerals
			aHelp.append(getIcon(iGenerals >= 3) + text("TXT_KEY_VICTORY_GREAT_GENERALS", iGenerals, 3))
		elif iGoal == 2:
			pBestCity = getBestCity(iPlayer, (18, 37), cityPopulation)
			bBestCity = isBestCity(iPlayer, (18, 37), cityPopulation)
			aHelp.append(getIcon(bBestCity) + text("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", pBestCity.getName()))
	
	elif iCiv == iColombia:
		if iGoal == 0:
			bPeru = isAreaFreeOfCivs(plots.rectangle(tPeru), dCivGroups[iCivGroupEurope])
			bGranColombia = isAreaFreeOfCivs(plots.rectangle(tGranColombia), dCivGroups[iCivGroupEurope])
			bGuayanas = isAreaFreeOfCivs(plots.rectangle(tGuayanas), dCivGroups[iCivGroupEurope])
			bCaribbean = isAreaFreeOfCivs(plots.rectangle(tCaribbean), dCivGroups[iCivGroupEurope])
			aHelp.append(getIcon(bPeru) + text("TXT_KEY_VICTORY_NO_COLONIES_PERU") + ' ' + getIcon(bGranColombia) + text("TXT_KEY_VICTORY_NO_COLONIES_GRAN_COLOMBIA"))
			aHelp.append(getIcon(bGuayanas) + text("TXT_KEY_VICTORY_NO_COLONIES_GUAYANAS") + ' ' + getIcon(bCaribbean) + text("TXT_KEY_VICTORY_NO_COLONIES_CARIBBEAN"))
		elif iGoal == 1:
			bSouthAmerica = isControlled(iPlayer, plots.rectangle(tSouthAmerica).without(lSouthAmericaExceptions))
			aHelp.append(getIcon(bSouthAmerica) + text("TXT_KEY_VICTORY_CONTROL_SOUTH_AMERICA"))
		elif iGoal == 2:
			iTradeGold = data.iColombianTradeGold
			aHelp.append(getIcon(iTradeGold >= turns(3000)) + text("TXT_KEY_VICTORY_TRADE_GOLD_RESOURCES", iTradeGold, turns(3000)))

	elif iCiv == iBrazil:
		if iGoal == 0:
			iSlavePlantations = countImprovements(iPlayer, iSlavePlantation)
			iPastures = countImprovements(iPlayer, iPasture)
			aHelp.append(getIcon(iSlavePlantations >= 8) + text("TXT_KEY_VICTORY_NUM_IMPROVEMENTS", infos.improvement(iSlavePlantation).getText(), iSlavePlantations, 8) + ' ' + getIcon(iPastures >= 4) + text("TXT_KEY_VICTORY_NUM_IMPROVEMENTS", infos.improvement(iPasture).getText(), iPastures, 4))
		elif iGoal == 1:
			bWembley = data.getWonderBuilder(iWembley) == iPlayer
			bCristoRedentor = data.getWonderBuilder(iCristoRedentor) == iPlayer
			bItaipuDam = data.getWonderBuilder(iItaipuDam) == iPlayer
			aHelp.append(getIcon(bWembley) + text("TXT_KEY_BUILDING_WEMBLEY") + ' ' + getIcon(bCristoRedentor) + text("TXT_KEY_BUILDING_CRISTO_REDENTOR") + ' ' + getIcon(bItaipuDam) + text("TXT_KEY_BUILDING_ITAIPU_DAM"))
		elif iGoal == 2:
			iForestPreserves = countImprovements(iPlayer, iForestPreserve)
			bNationalPark = False
			capital = pPlayer.getCapitalCity()
			if capital: bNationalPark = capital.isHasRealBuilding(iNationalPark)
			aHelp.append(getIcon(iForestPreserves >= 20) + text("TXT_KEY_VICTORY_NUM_IMPROVEMENTS", infos.improvement(iForestPreserve).getText(), iForestPreserves, 20) + ' ' + getIcon(bNationalPark) + text("TXT_KEY_VICTORY_NATIONAL_PARK_CAPITAL"))

	elif iCiv == iCanada:
		if iGoal == 0:
			capital = pPlayer.getCapitalCity()
			bAtlantic = capital and isConnectedByRailroad(iPlayer, capital, lAtlanticCoast)
			bPacific = capital and isConnectedByRailroad(iPlayer, capital, lPacificCoast)
			aHelp.append(getIcon(bAtlantic) + text("TXT_KEY_VICTORY_ATLANTIC_RAILROAD") + ' ' + getIcon(bPacific) + text("TXT_KEY_VICTORY_PACIFIC_RAILROAD"))
		elif iGoal == 1:
			iCanadaWest, iTotalCanadaWest = countControlledTiles(iPlayer, plots.rectangle(tCanadaWest).without(lCanadaWestExceptions), False)
			iCanadaEast, iTotalCanadaEast = countControlledTiles(iPlayer, plots.rectangle(tCanadaEast).without(lCanadaEastExceptions), False)
			fCanada = (iCanadaWest + iCanadaEast) * 100.0 / (iTotalCanadaWest + iTotalCanadaEast)
			bAllCities = controlsAllCities(iPlayer, plots.rectangle(tCanadaWest).without(lCanadaWestExceptions)) and controlsAllCities(iPlayer, plots.rectangle(tCanadaEast).without(lCanadaEastExceptions))
			aHelp.append(getIcon(fCanada >= 90.0) + text("TXT_KEY_VICTORY_CONTROL_CANADA", "%.2f%%" % fCanada, 90) + ' ' + getIcon(bAllCities) + text("TXT_KEY_VICTORY_CONTROL_CANADA_CITIES"))
		elif iGoal == 2:
			iPeaceDeals = data.iCanadianPeaceDeals
			aHelp.append(getIcon(iPeaceDeals >= 12) + text("TXT_KEY_VICTORY_CANADIAN_PEACE_DEALS", iPeaceDeals, 12))
			
	return aHelp