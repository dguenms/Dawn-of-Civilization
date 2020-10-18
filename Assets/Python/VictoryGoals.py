from inspect import ismethod, isfunction, getargspec
import re

from Core import *
from Events import events


sum_ = sum


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
			iGameTurn, iPlayer = args
			if other.iPlayer == iPlayer:
				func(other)
		
		return beginPlayerTurn
	
	def techAcquired(self, func):
		def techAcquired(other, args):
			iTech, iTeam, iPlayer, bAnnounce = args
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
	
	def enslave(self, func):
		def enslave(other, args):
			iPlayer, losingUnit = args
			if other.iPlayer == iPlayer:
				func()
		
		return enslave
				
	
handlers = EventHandlers()


class classproperty(property):
    def __get__(self, obj, objtype=None):
        return super(classproperty, self).__get__(objtype)
    def __set__(self, obj, value):
        super(classproperty, self).__set__(type(obj), value)
    def __delete__(self, obj):
        super(classproperty, self).__delete__(type(obj))


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


class Aggregate(object):

	def __init__(self, aggregate, *generator):
		self.aggregate = aggregate
		self.generator = unwrap(generator)
		
		self._items = None
		
	def items(self):
		if self._items is None:
			self._items = list(self.generator)
		return self._items
	
	def eval(self, func):
		return self.aggregate(func(item) for item in self.items())

def avg_(iterable):
	if len(iterable) == 0:
		return 0.0
	return sum_(iterable) / len(iterable)
	
def sum(*generator):
	return Aggregate(sum_, *generator)

def avg(*generator):
	return Aggregate(avg_, *generator)





class ObjectiveProcessor(object):

	defaults = {
		Players : lambda: players.major().alive()
	}
	
	@classmethod
	def default(cls, type):
		return cls.defaults.get(type)

	def __init__(self, *types):
		self.types = types
	
	def process(self, *objectives):
		if len(objectives) == len(self.types) and none(isinstance(elem, tuple) for elem in objectives):
			return self.process(tuple(objectives))
			
		return list(self.process_objectives(objectives))
		
	def process_objectives(self, objectives):	
		for objective in objectives:
			yield self.process_objective(objective)
			
	def process_objective(self, objective):
		if not isinstance(objective, tuple):
			return self.process_objective((objective,))
		
		if len(objective) > len(self.types):
			raise ValueError("Expected objectives of length %d" % len(self.types))
		
		elems = []
		index = 0
		for type in self.types:
			if index >= len(objective):
				raise ValueError("Expected objectives of length %d" % len(self.types))
				
			elem = objective[index]
			if self.validate(type, elem):
				elems.append(elem)
				index += 1
			elif self.default(type):
				elems.append(self.default(type)())
			else:
				raise ValueError("Expected element '%s' to be of type %s, was: %s" % (str(elem), type.__name__, elem.__class__.__name__))
				
		if len(elems) != len(self.types):
			raise ValueError("Expected objectives of length %d" % len(self.types))
		
		return tuple(elems)
	
	def validate(self, type, elem):
		if issubclass(type, CvInfoBase):
			return isinstance(elem, (int, Aggregate))
		return isinstance(elem, type)


class GoalBuilder(object):

	def __init__(self):
		self.reset()
	
	def reset(self):
		self.attributes = {}
		self.funcs = []
		self.handlers = []
	
	def attribute(self, name, value):
		self.attributes[name] = value
	
	def func(self, *funcs):
		self.funcs.extend([func for func in funcs])
		
	def handler(self, event, handler):
		self.handlers.append((event, handler.__name__))
		self.of(handler)
		
	def members(self):
		members = dict((func.__name__, func) for func in self.funcs)
		members.update(self.attributes)
		members["handlers"] = self.handlers[:]
		return members
		
	def create(self, cls, name):
		goal = type(name, (cls,), self.members())
		self.reset()
		return goal
	


class BaseGoal(object):

	builder = GoalBuilder()
	handlers = []
	types = None

	def __init__(self, *objectives):
		self._objectives = self.process_objectives(*objectives)
		
		self.activate(active())
	
	@classmethod
	def process_objectives(cls, *objectives):
		if cls.types:
			return cls.types.process(*objectives)
		return [item for item in objectives]
	
	def activate(self, iPlayer, callback=None):
		self.iPlayer = iPlayer
		self.player = player(iPlayer)
		self.team = team(iPlayer)
		self.callback = callback
		
		for event, handler in self.__class__.handlers:
			events.addEventHandler(event, getattr(self, handler))
	
	def objectives(self):
		return self._objectives
		
	def __nonzero__(self):
		if not self.objectives():
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
	
	def objective_values(self):
		return [values for values, _ in self.objectives()]
	
	def objective_requireds(self):
		return [required for _, required in self.objectives()]

	def condition(self, objective):
		return self.value(objective) >= self.required(objective)
	
	def required(self, objective):
		return self.required_function(objective[1])
	
	def required_function(self, objective):
		return objective
	
	def value(self, objective):
		if isinstance(objective[0], Aggregate):
			return objective[0].eval(self.value_function)
		return self.value_function(objective[0])
		
	def value_function(self, objective):
		raise NotImplementedError()
		
	def display(self, objective):
		return "%d / %d" % (self.value(objective), self.required(objective))
		
	@classmethod
	def func(cls, *funcs):
		cls.builder.func(*funcs)
		return cls
	
	@classmethod
	def attribute(cls, name, value):
		cls.builder.attribute(name, value)
		return cls
		
	@classmethod
	def subclass(cls, name):
		return cls.builder.create(cls, name)
	
	@classmethod
	def types(cls, *types):
		types = list(types) + [int]
		cls.builder.attribute("types", ObjectiveProcessor(*types))
		return cls
	
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
				
		return cls.func(value_function)
	
	@classmethod
	def city(cls, func):
		def value_function(self, plots):
			return func(self, plots.cities()).count()
		
		return cls.types(Plots).func(value_function)
	
	@classmethod
	def players(cls, func):
		def value_function(self, players):
			return players.where(lambda p: func(self, p)).count()
		
		return cls.types(Players).func(value_function)
		
	@classmethod
	def playercities(cls, func):
		def value_function(self, objective):
			return cities.owner(self.iPlayer).sum(func)
		
		return cls.func(value_function)
		
	@classproperty
	def scaled(cls):
		def required_function(self, objective):
			return scale(objective)
			
		return cls.func(required_function)
	
	@classproperty
	def building(cls):
		return cls.types(CvBuildingInfo).player(CyPlayer.countNumBuildings).subclass("BuildingCount")
	
	@classproperty
	def culture(cls):
		return cls.player(CyPlayer.countTotalCulture).scaled.subclass("PlayerCulture")
	
	@classproperty
	def gold(cls):
		return cls.player(CyPlayer.getGold).scaled.subclass("PlayerGold")
	
	@classproperty
	def resource(cls):
		return cls.types(CvBonusInfo).player(CyPlayer.getNumAvailableBonuses).subclass("ResourceCount")
		
	@classproperty
	def improvement(cls):
		return cls.types(CvImprovementInfo).player(CyPlayer.getImprovementCount).subclass("ImprovementCount")
	
	@classproperty
	def population(cls):
		return cls.player(CyPlayer.getTotalPopulation).subclass("PlayerPopulation")
	
	@classproperty
	def corporation(cls):
		return cls.types(CvCorporationInfo).player(CyPlayer.countCorporations).subclass("CorporationCount")
	
	@classproperty
	def unit(cls):
		def value_function(self, objective):
			return self.player.getUnitClassCount(infos.unit(objective).getUnitClassType())
		
		return cls.types(CvUnitInfo).func(value_function).subclass("UnitCount")
		
	@classproperty
	def cities(cls):
		def owned(self, cities):
			return cities.owner(self.iPlayer)
	
		return cls.city(owned).subclass("CityCount")
	
	@classproperty
	def settledCities(cls):
		def settled(self, cities):
			return cities.owner(self.iPlayer).where(lambda city: city.getOwner() == self.iPlayer)
		
		return cls.city(settled).subclass("SettledCityCount")
	
	@classproperty
	def openBorders(cls):
		def withOpenBorders(self, iPlayer):
			return self.team.isOpenBorders(player(iPlayer).getTeam())
		
		return cls.players(withOpenBorders).subclass("OpenBorderCount")
	
	@classproperty
	def specialist(cls):
		# uses sum
		return cls.types(CvSpecialistInfo).playercities(CyCity.getFreeSpecialistCount).subclass("SpecialistCount")


PlayerGold = Count.gold


class Track(Count):

	def __init__(self, *objectives):
		super(Track, self).__init__(*objectives)
		
		self.dCount = dict((objective, 0) for objective, _ in self.objectives())
	
	def value_function(self, objective=None):
		return self.dCount[objective]
	
	def increment(self, objective=None):
		self.accumulate(1, objective)
	
	def accumulate(self, iChange, objective=None):
		self.dCount[objective] += iChange
		
	@classmethod
	def subclass(cls, name):
		return cls.builder.create(cls, name)
	
	@classmethod
	def handle(cls, event, func):
		handler = handlers.get(event, func)
		cls.builder.handler(event, handler)
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
			if self.player.isGoldenAge() and not self.player.isAnarchy():
				self.increment()
		
		return cls.handle("BeginPlayerTurn", incrementGoldenAges).func(required_function).subclass("GoldenAges")
	
	@classproperty
	def eraFirsts(cls):
		def incrementFirstDiscovered(self, iTech):
			iEra = infos.tech(iTech).getEra()
			if iEra in self.objective_values():
				if game.countKnownTechNumTeams(iTech) == 1:
					self.increment(iEra)
		
		return cls.types(CvTechInfo).handle("techAcquired", incrementFirstDiscovered).subclass("EraFirstDiscover")
	
	@classproperty
	def sunkShips(cls):
		def incrementShipsSunk(self, losingUnit):
			if infos.unit(losingUnit).getDomainType() == DomainTypes.DOMAIN_WATER:
				self.increment()
		
		return cls.handle("combatResult", incrementShipsSunk).subclass("SunkShips")
	
	@classproperty
	def tradeGold(cls):
		def value_function(self, objective=None):
			return self.dCount[objective] / 100
		
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
	
	@classproperty
	def enslaves(cls):
		return cls.incremented("enslave").subclass("Enslave")