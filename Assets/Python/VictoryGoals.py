from inspect import ismethod, isfunction, getargspec
import re

from Core import *
from Events import events


def getnumargs(func):
	if ismethod(func):
		return getnumargs(func.im_func) + 1
	elif isfunction(func):
		return len(getargspec(func)[0])
	elif hasattr(func, 'func_doc'):
		argstring = re.search(r"\((.*)\)", func.func_doc).group(0).strip()
		if argstring == '()':
			return 0
		return argstring.count(',') + 1
	
	raise ValueError("Expected function or method type, was: %s" % type(func).__name__)


class EventHandlers(object):
		
	def get(self, event, func):
		if hasattr(self, event):
			handler_func = getattr(self, event)
			if ismethod(handler_func):
				return handler_func(func)
		
		raise Exception("No handler available for event '%s'" % event)
	
	def BeginPlayerTurn(self, func):
		def beginPlayerTurn(other, args):
			raise Exception("I wanted to be called")
			iGameTurn, iPlayer = args
			if other.iPlayer == iPlayer:
				func(other)
		
		return beginPlayerTurn
	
	def techAcquired(self, func):
		def techAcquired(other, args):
			iTech, iTeam, iPlayer = args
			if other.iPlayer == iPlayer:
				func(other, iTech)
	
		return techAcquired
	
	def combatResult(self, func):
		def combatResult(other, args):
			winningUnit, losingUnit = args
			if other.iPlayer == winningUnit.getOwner():
				func(other, losingUnit)
		
		return combatResult
	
	def playerGoldTrade(self, func):
		def playerGoldTrade(other, args):
			iFrom, iTo, iGold = args
			if other.iPlayer == iTo:
				func(other, iGold)
		
		return playerGoldTrade
	
	def unitPillage(self, func):
		def unitPillage(other, args):
			unit, iImprovement, iRoute, iPlayer, iGold = args
			if other.iPlayer == iPlayer:
				func(other, iGold)
		
		return unitPillage
	
	def cityCaptureGold(self, func):
		def cityCaptureGold(other, args):
			city, iPlayer, iGold = args
			if other.iPlayer == iPlayer:
				func(other, iGold)
		
		return cityCaptureGold
	
	def cityAcquired(self, func):
		def cityAcquired(other, args):
			iOwner, iPlayer, city, bConquest = args
			if other.iPlayer == iPlayer:
				func(other)
		
		return cityAcquired
	
	def cityBuilt(self, func):
		def cityBuilt(other, args):
			city = args[0]
			if other.iPlayer == city.getOwner():
				func(other)
		
		return cityBuilt
	
	def blockade(self, func):
		def blockade(other, args):
			iPlayer, iGold = args
			if other.iPlayer == iPlayer:
				func(other, iGold)
		
		return blockade
	
	def cityRazed(self, func):
		def cityRazed(other, args):
			city, iPlayer = args
			if other.iPlayer == iPlayer:
				func(other)
		
		return cityRazed
	
	def playerSlaveTrade(self, func):
		def playerSlaveTrade(other, args):
			iPlayer, iGold = args
			if other.iPlayer == iPlayer:
				func(other, iGold)
		
		return playerSlaveTrade
	
	def greatPersonBorn(self, func):
		def greatPersonBorn(other, args):
			unit, iPlayer = args
			if other.iPlayer == iPlayer:
				func(other, unit)
		
		return greatPersonBorn
	
	def peaceBrokered(self, func):
		def peaceBrokered(other, args):
			iBroker, iPlayer1, iPlayer2 = args
			if other.iPlayer == iBroker:
				func(other)
		
		return peaceBrokered
				
	
handlers = EventHandlers()


class classproperty(property):
    def __get__(self, obj, objtype=None):
        return super(classproperty, self).__get__(objtype)
    def __set__(self, obj, value):
        super(classproperty, self).__set__(type(obj), value)
    def __delete__(self, obj):
        super(classproperty, self).__delete__(type(obj))


# Goal has a condition function: if true, goal is met for objective (if any)
# Goal has a display function: shows state and progress for objective (if any)

# no objectives: no arguments in cond()
# single objective: cond(obj) takes one argument
# multiple objectives: multiple cond(obj) with one argument each
#  either true multiple: separate conditions that all need to be met
#  aggregated multiple: values or similar for all


def defer(*items):
	if not items:
		return None
	return Deferred(*items)


class Deferred(object):

	def __init__(self, *items):
		items = [item for item in items]
		def provider():
			return items
		
		self.provider = provider
	
	def __iter__(self):
		return iter(self.provider())
	
	def __str__(self):
		return str(self.provider())


class GoalBuilder(object):

	def __init__(self):
		self.reset()
	
	def reset(self):
		self.funcs = []
		self.handlers = []
	
	def of(self, *funcs):
		self.funcs.extend([func for func in funcs])
		
	def handler(self, event, handler):
		self.handlers.append((event, handler))
		self.of(handler)
		
	def attributes(self):
		attributes = dict((func.__name__, func) for func in self.funcs)
		attributes["handlers"] = self.handlers[:]
		return attributes
		
	def create(self, cls, name):
		goal = type(name, (cls,), self.attributes())
		self.reset()
		return goal
	


class BaseGoal(object):

	builder = GoalBuilder()
	handlers = []

	def __init__(self, *objectives):
		self._objectives = defer(*objectives)
		
		self.player = None
		self.callback = None
		
		for event, handler in self.__class__.handlers:
			events.addEventHandler(event, getattr(self, handler.__name__))
		
		self.bind(active())
	
	def bind(self, iPlayer, callback=None):
		self.iPlayer = iPlayer
		self.callback = callback
	
	def objectives(self):
		return self._objectives
		
	def __nonzero__(self):
		if not self.objectives:
			return self.condition()
		else:
			return all(self.condition(objective) for objective in self.objectives())
	
	def __str__(self):
		if not self.objectives:
			return self.display()
		else:
			return '\n'.join([self.display(objective) for objective in self.objectives()])
		
	def condition(self, objective=None):
		raise NotImplementedError()
		


class Count(BaseGoal):

	def objectives(self):
		for objective in self._objectives:
			if isinstance(objective, tuple):
				if len(objective) > 2:
					yield (objective[:-1], objective[-1])
				elif len(objective) == 2:
					yield (objective[0], objective[1])
				else:
					yield (None, objective[0])
			else:
				yield (None, objective)

	def condition(self, objective):
		return self.value(objective) >= self.required(objective)
	
	def required(self, objective):
		return self.required_function(objective[1])
	
	def required_function(self, objective):
		return objective
	
	def value(self, objective):
		return self.value_function(objective[0])
		
	def value_function(self, objective):
		raise NotImplementedError()
		
	def display(self, objective):
		return "%d / %d" % (self.value(objective), self.required(objective))
		
	@classmethod
	def func(cls, *funcs):
		cls.builder.of(*funcs)
		return cls
		
	@classmethod
	def subclass(cls, name):
		return cls.builder.create(cls, name)
	
	@classmethod
	def player(cls, func):
		iNumArgs = getnumargs(func)
		if iNumArgs > 2:
			def value_function(self, objective):
				return func(self.player, *objective)
		elif iNumArgs > 1:
			def value_function(self, objective):
				return func(self.player, objective)
		else:
			def value_function(self, objective):
				return func(self.player)
		
		cls.builder.of(value_function)
		return cls
		
	@classproperty
	def scaled(cls):
		def required_function(self, objective):
			return scale(objective)
		
		cls.builder.of(required_function)
		return cls
	
	@classproperty
	def building(cls):
		return cls.player(CyPlayer.countNumBuildings).subclass("BuildingCount")
	
	@classproperty
	def culture(cls):
		return cls.player(CyPlayer.countTotalCulture).scaled.subclass("PlayerCulture")
	
	@classproperty
	def gold(cls):
		return cls.player(CyPlayer.getGold).scaled.subclass("PlayerGold")
	
	@classproperty
	def resource(cls):
		return cls.player(CyPlayer.getNumAvailableBonuses).subclass("ResourceCount")
		
	@classproperty
	def improvement(cls):
		return cls.player(CyPlayer.getImprovementCount).subclass("ImprovementCount")
	
	@classproperty
	def population(cls):
		return cls.player(CyPlayer.getTotalPopulation).subclass("PlayerPopulation")
	
	@classproperty
	def corporation(cls):
		return cls.player(CyPlayer.countCorporations).subclass("CorporationCount")
	
	@classproperty
	def unit(cls):
		def value_function(self, objective):
			return self.player.getUnitClassCount(infos.unit(objective).getUnitClassType())
		
		return cls.func(value_function).subclass("UnitCount")


PlayerGold = Count.gold


class Track(Count):

	def __init__(self, *objectives):
		super(Track, self).__init__(*objectives)
		
		self.iCount = 0
	
	def value_function(self, objective=None):
		return self.iCount
	
	def increment(self):
		self.accumulate(1)
	
	def accumulate(self, iChange):
		self.iCount += iChange
		
	@classmethod
	def subclass(cls, name):
		return cls.builder.create(cls, name)
	
	@classmethod
	def handle(cls, event, func):
		handler = handlers.get(event, func)
		cls.builder.handler(event, handler.__name__)
		return cls
	
	@classmethod
	def incremented(cls, event):
		def func(self):
			self.increment()
		return cls.handle(event, func)
	
	@classmethod
	def accumulated(cls, event):
		def func(self, iChange):
			self.accumulate(iChange)
		return cls.handle(event, func).scaled
	
	@classproperty
	def goldenAges(cls):
		def required_function(self, objective):
			return scale(8 * objective)
	
		def incrementGoldenAges(self):
			show("check golden age")
			if self.player.isGoldenAge() and not self.player.isAnarchy():
				self.increment()
		
		return cls.handle("BeginPlayerTurn", incrementGoldenAges).func(required_function).subclass("GoldenAges")
	
	@classproperty
	def eraFirsts(cls):
		def incrementFirstDiscovered(self, iTech):
			if infos.tech(iTech).getEra() == self.entity:
				if game.countKnownTechNumTeams(iTech) == 1:
					self.increment()
		
		return cls.entity.handle("techAcquired", incrementFirstDiscovered).subclass("EraFirstDiscover")
	
	@classproperty
	def sunkShips(cls):
		def incrementShipsSunk(self, losingUnit):
			if infos.unit(losingUnit).getDomainType() == DomainTypes.DOMAIN_WATER:
				self.increment()
		
		return cls.handle("combatResult", incrementShipsSunk).subclass("SunkShips")
	
	@classproperty
	def tradeGold(cls):
		def value_function(self):
			return self.iCount / 100
		
		def accumulateTradeGold(self, iGold):
			self.accumulate(iGold * 100)
		
		def trackTradeGold(self):
			self.iCount += cities.owner(self.iPlayer).sum(lambda city: city.getTradeYield(YieldTypes.YIELD_COMMERCE)) * self.player.getCommercePercent(CommerceTypes.COMMERCE_GOLD)
			self.iCount += players.major().alive().sum(self.player.getGoldPerTurnByPlayer) * 100
		
		return cls.handle("playerGoldTrade", accumulateTradeGold).handle("beginPlayerTurn", trackTradeGold).func(value_function).subclass("TradeGold")
	
	@classproperty
	def raidGold(cls):
		return cls.accumulated("unitPillage").accumulated("cityCaptureGold").subclass("RaidGold")
	
	@classproperty
	def pillage(cls):
		return cls.incremented("unitPillage").subclass("PillageCount")
	
	@classproperty
	def acquiredCities(cls):
		return cls.incremented("cityAcquired").incremented("cityBuilt").subclass("AcquiredCities")
	
	@classproperty
	def piracyGold(cls):
		return cls.accumulated("unitPillage").accumulated("blockade").subclass("PiracyGold")
	
	@classproperty
	def razes(cls):
		return cls.incremented("cityRazed").subclass("RazeCount")
	
	@classproperty
	def slaveTradeGold(cls):
		return cls.accumulated("playerSlaveTrade").subclass("SlaveTradeGold")
	
	@classproperty
	def greatGenerals(cls):
		def incrementGreatGenerals(self, unit):
			if infos.unit(unit).getGreatPeoples(iSpecialistGreatGeneral):
				self.increment()
		
		return cls.handle("greatPersonBorn", incrementGreatGenerals).subclass("GreatGenerals")
	
	@classproperty
	def resourceTradeGold(cls):
		def accumulateTradeGold(self):
			self.iCount += players.major().alive().sum(self.player.getGoldPerTurnByPlayer)
	
		return cls.handle("beginPlayerTurn", accumulateTradeGold).scaled.subclass("ResourceTradeGold")
	
	@classproperty
	def brokeredPeace(cls):
		return cls.incremented("peaceBrokered").subclass("BrokeredPeace")
		
		
		