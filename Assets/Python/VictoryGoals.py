from inspect import ismethod, isfunction, getargspec
import re

from Core import *
from RFCUtils import *
from Events import events


sum_ = sum
capital_ = capital


POSSIBLE, SUCCESS, FAILURE = range(3)


def getnumargs(func):
	if ismethod(func):
		return getnumargs(func.im_func) + 1
	elif isfunction(func):
		return len([arg for arg in getargspec(func)[0] if arg != 'self'])
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
			iOwner, iPlayer, city, bConquest, bTrade = args
			if other.iPlayer == iPlayer:
				func(other, iOwner, bConquest)
		
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
			unit, iPlayer, city = args
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
				func(other)
		
		return enslave
				
	
handlers = EventHandlers()


class classproperty(property):
    def __get__(self, obj, objtype=None):
        return super(classproperty, self).__get__(objtype)
    def __set__(self, obj, value):
        super(classproperty, self).__set__(type(obj), value)
    def __delete__(self, obj):
        super(classproperty, self).__delete__(type(obj))


class Deferred(object):
	
	def __init__(self, provider):
		self.provider = provider
	
	def __call__(self, iPlayer=None):
		return self.provider(iPlayer)

def capital():
	return Deferred(lambda p: capital_(p))

def city(*location):
	return Deferred(lambda p: city_(*location))

def wonder(iWonder):
	return Deferred(lambda p: getBuildingCity(iWonder))


class Aggregate(object):

	def __init__(self, aggregate, generator):
		self.aggregate = aggregate
		self.generator = generator
		
		self._items = None
	
	def __iter__(self):
		return iter(self.items)
	
	def __contains__(self, item):
		return item in self.items
	
	@property
	def items(self):
		if self._items is None:
			self._items = list(self.generator)
		return self._items
	
	def eval(self, func):
		return self.aggregate([func(item) for item in self.items])

def avg_(iterable):
	if len(iterable) == 0:
		return 0.0
	return sum_(iterable) / len(iterable)
	
def sum(generator):
	return Aggregate(sum_, generator)

def avg(generator):
	return Aggregate(avg_, generator)


class Arguments(object):

	def __init__(self, objectives, subject=None):
		self.subject = subject
		self.objectives = objectives
		
	def __iter__(self):
		if self.objectives:
			for objective in self.objectives:
				if self.subject:
					yield [self.subject] + list(objective)
				else:
					yield list(objective)
		else:
			if self.subject:
				yield [self.subject]
			else:
				yield []


class ArgumentProcessorBuilder(object):

	def __init__(self):
		self.objective_types = []
		self.subject_type = None
		self.objective_split = 0
	
	def withObjectiveTypes(self, *objective_types):
		self.objective_types = list(objective_types)
		return self
	
	def withSubjectType(self, subject_type):
		self.subject_type = subject_type
		return self
	
	def withObjectiveSplit(self, objective_split):
		self.objective_split = objective_split
		return self
		
	def initialized(self):
		return bool(self.objective_types or self.subject_type or self.objective_split)
	
	def build(self):
		return ArgumentProcessor(self.objective_types, self.subject_type, self.objective_split)


class ArgumentProcessor(object):

	defaults = {
		int : lambda: 1,
		Players : lambda: players.major().alive()
	}
	
	@classmethod
	def default(cls, type):
		default = cls.defaults.get(type)
		if default:
			return default()

	def __init__(self, objective_types=[], subject_type=None, objective_split=0):
		if not objective_types and not subject_type:
			raise ValueError("Needs at least one objective type or subject type")
		
		if not isinstance(objective_types, list):
			raise ValueError("Objective types need to be a list")
			
		if objective_split > len(objective_types):
			raise ValueError("Objective split cannot exceed number of objective types")
	
		self.objective_types = objective_types
		self.subject_type = subject_type
		self.objective_split = objective_split
	
	def process(self, *arguments):
		if self.subject_type:
			subject = self.default(self.subject_type)

			if not subject:
				if len(arguments) == 0:
					raise ValueError("Need to supply at least one subject type: %s" % self.subject_type.__name__)
				subject = arguments[0]
	
			return Arguments(self.process_objectives(list(arguments[1:])), self.process_subject(subject))
	
		return Arguments(self.process_objectives(list(arguments)))
	
	def process_subject(self, subject):
		if not self.valid_type(self.subject_type, subject):
			raise ValueError("Subject %s does not match required type %s" % (subject, self.subject_type.__name__))
		
		return subject
		
	def process_objectives(self, objectives):
		if not objectives and self.objective_types:
			return self.process_objectives([tuple()])
	
		if isinstance(objectives, list) and len(objectives) == len(self.objective_types) and none(isinstance(elem, tuple) for elem in objectives):
			return self.process_objectives([tuple(objectives)])
			
		processed = list(self.process_objective(objective) for objective in objectives)
		return [objective for objective in processed if objective != tuple()]
			
	def process_objective(self, objective):
		if not isinstance(objective, tuple):
			return self.process_objective((objective,))
		
		if len(objective) > len(self.objective_types):
			raise ValueError("Supplied objectives %s do not match required types %s" % (objective, [type.__name__ for type in self.objective_types]))
		
		values = list((type, self.default(type)) for type in self.objective_types)
		
		index = 0
		for i, (type, default_value) in enumerate(values):
			if index < len(objective) and self.valid_type(type, objective[index]):
				values[i] = (type, self.transform(type, objective[index]))
				index += 1
			elif default_value is None:
				raise ValueError("Supplied objectives %s do not match required types %s" % (objective, [type.__name__ for type in self.objective_types]))
		
		values = tuple(value for _, value in values)
		
		if None in values:
			raise ValueError("Supplied objectives %s do not match required types %s including their defaults" % (objective, [type.__name__ for type in self.objective_types]))
		
		if self.objective_split > 0:
			return (values[:-self.objective_split], values[-self.objective_split:])
		
		return values
	
	def valid_type(self, type, value):
		if issubclass(type, CvInfoBase):
			return isinstance(value, (int, Aggregate))
		elif issubclass(type, Plots):
			return isinstance(value, (Plots, Aggregate))
		elif issubclass(type, CyCity):
			return isinstance(value, Deferred)
		return isinstance(value, type)
	
	def transform(self, type, value):
		if issubclass(type, list):
			return tuple(value)
		return value


class GoalBuilder(object):

	def __init__(self):
		self.reset()
	
	def reset(self):
		self.attributes = {}
		self.funcs = []
		self.handlers = []
		
		self.types = ArgumentProcessorBuilder()
	
	def attribute(self, name, value):
		self.attributes[name] = value
	
	def func(self, *funcs):
		self.funcs.extend([func for func in funcs])
		
	def handler(self, event, handler):
		self.handlers.append((event, handler.__name__))
		self.func(handler)
	
	def objectives(self, types):
		self.types.withObjectiveTypes(*types)
		return self
	
	def subject(self, type):
		self.types.withSubjectType(type)
		return self
	
	def split(self, split):
		self.types.withObjectiveSplit(split)
		return self
		
	def members(self):
		members = dict((func.__name__, func) for func in self.funcs)
		members.update(self.attributes)
		members["handlers"] = self.handlers[:]
		members["_types"] = self.types.build()
		
		return members

	def create(self, cls, name):
		goal = type(name, (cls,), self.members())
		self.reset()
		return goal


class BaseGoal(object):

	builder = GoalBuilder()
	handlers = []
	_types = None
		
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
		cls.builder.objectives(list(types))
		return cls
	
	@classmethod
	def type(cls, type):
		cls.builder.subject(type)
		return cls
	
	@classmethod
	def split(cls, split):
		cls.builder.split(split)
		return cls
	
	@classmethod
	def process_arguments(cls, *arguments):
		return cls._types.process(*arguments)

	def __init__(self, *arguments):
		self.reset()
		
		self.arguments = self.process_arguments(*arguments)
		
	def __nonzero__(self):
		return all(self.condition(*args) for args in self.arguments)
	
	def __str__(self):
		return '\n'.join([self.display(*args) for args in self.arguments])
	
	@property
	def objectives(self):
		return self.arguments.objectives
	
	@property
	def subject(self):
		return self.arguments.subject
		
	def reset(self):
		self.state = POSSIBLE
		
		self.iPlayer = None
		self._player = None
		self._team = None
		self.callback = None
	
	def activate(self, iPlayer, callback=None):
		self.iPlayer = iPlayer
		self._player = player(iPlayer)
		self._team = team(iPlayer)
		self.callback = callback
		
		for event, handler in self.__class__.handlers:
			events.addEventHandler(event, getattr(self, handler))
	
	def deactivate(self):
		for event, handler in self.__class__.handlers:
			events.removeEventHandler(event, getattr(self, handler))
	
	def setState(self, state):
		if self.state != state:
			self.state = state
			if self.callback:
				self.callback(self)
	
	def possible(self):
		return self.state == POSSIBLE
	
	def win(self):
		self.setState(SUCCESS)
	
	def fail(self):
		self.setState(FAILURE)
		
	def expire(self):
		if self.possible():
			self.fail()
	
	def check(self):
		if self.possible() and self:
			self.win()
	
	def finalCheck(self):
		self.check()
		self.expire()
		
	def condition(self, objective=None):
		raise NotImplementedError()
	
	def display(self):
		raise NotImplementedError()


class Condition(BaseGoal):

	@classmethod
	def player(cls, func):
		def condition(self, objective):
			return func(self._player, objective)
		
		return cls.func(condition)
	
	@classmethod
	def team(cls, func):
		def condition(self, objective):
			return func(self._team, objective)
		
		return cls.func(condition)
	
	@classmethod
	def plots(cls, func):
		def condition(self, plots, objective):
			return plots.all(lambda plot: func(plot, objective))
		
		return cls.func(condition)
	
	@classmethod
	def cities(cls, func):
		def condition(self, plots):
			return plots.cities().all_if_any(lambda city: func(city, self.iPlayer))
		
		return cls.types(Plots).func(condition)
	
	@classmethod
	def city(cls, func):
		def condition(self, city, objective):
			return city() and func(city(), objective) or False
		
		return cls.func(condition)

	@classproperty
	def wonder(cls):
		return cls.types(CvBuildingInfo).player(CyPlayer.isHasBuilding).subclass("Wonder")
	
	@classproperty
	def control(cls):
		def owned(city, iPlayer):
			return city.getOwner() == iPlayer
	
		return cls.cities(owned).subclass("Control")
	
	@classproperty
	def controlOrVassalize(cls):
		def owned(city, iPlayer):
			return city.getOwner() in players.vassals(iPlayer).including(iPlayer)
		
		return cls.cities(owned).subclass("ControlOrVassalize")
	
	@classproperty
	def settle(cls):
		def settled(city, iPlayer):
			return city.getOwner() == iPlayer and city.getOriginalOwner() == iPlayer
		
		return cls.cities(settled).subclass("Settled")
	
	@classproperty
	def cityBuilding(cls):
		return cls.type(CyCity).types(CvBuildingInfo).city(CyCity.isHasRealBuilding).subclass("CityBuilding")
	
	@classproperty
	def project(cls):
		return cls.types(CvProjectInfo).team(positive(CyTeam.getProjectCount)).subclass("ProjectCount")
	
	@classproperty
	def route(cls):
		return cls.type(Plots).types(CvRouteInfo).plots(equals(CyPlot.getRouteType)).subclass("Route")
	


class Count(BaseGoal):

	@classmethod
	def types(cls, *types):
		types = list(types) + [int]
		cls.builder.objectives(types)
		return cls
	
	@classmethod
	def subclass(cls, name):
		if not cls.builder.types.initialized():
			cls.types()
		return cls.builder.create(cls, name)

	def condition(self, *arguments):
		remainder, iRequired = arguments[:-1], arguments[-1]
		return self.value(*remainder) >= self.required(iRequired)
	
	def required(self, iRequired):
		return iRequired
	
	def value(self, *objectives):
		if objectives and isinstance(objectives[0], Aggregate):
			return objectives[0].eval(self.value_function)
		return self.value_function(*objectives)
		
	def value_function(self, objective):
		raise NotImplementedError()
		
	def display(self, *arguments):
		remainder, iRequired = arguments[:-1], arguments[-1]
		return "%d / %d" % (self.value(*remainder), self.required(iRequired))
	
	@classmethod
	def player(cls, func):
		def value_function(self, *objectives):
			return func(self._player, *objectives)
				
		return cls.func(value_function)
	
	@classmethod
	def playervassals(cls, func):
		def value_function(self, objective):
			return players.vassals(self.iPlayer).including(self.iPlayer).sum(lambda p: func(player(p), objective))
		
		return cls.func(value_function)
	
	@classmethod
	def cities(cls, func):
		def value_function(self, plots):
			return func(self, plots.cities()).count()
		
		return cls.types(Plots).func(value_function)
	
	@classmethod
	def players(cls, func):
		def value_function(self, players):
			return players.where(lambda p: func(self, p)).count()
		
		return cls.types(Players).func(value_function)
		
	@classmethod
	def citiesSum(cls, func):
		def value_function(self, *objectives):
			return cities.owner(self.iPlayer).sum(lambda city: func(city, *objectives))
		
		return cls.func(value_function)
	
	@classmethod
	def citiesWith(cls, func):
		def value_function(self, objective):
			def function(city):
				return func(city) >= objective
		
			return cities.owner(self.iPlayer).count(function)
		
		return cls.func(value_function)
	
	@classmethod
	def city(cls, func):
		def value_function(self, city, *objectives):
			city = city()
			if not city or city.getOwner() != self.iPlayer:
				return 0
			
			return func(city, *objectives)
		
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
	def controlledResource(cls):
		def resources(player, objective):
			return player.getNumAvailableBonuses(objective) - player.getBonusImport(objective)
	
		return cls.types(CvBonusInfo).playervassals(resources).subclass("ControlledResourceCount")
		
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
			return self._player.getUnitClassCount(infos.unit(objective).getUnitClassType())
		
		return cls.types(CvUnitInfo).func(value_function).subclass("UnitCount")
		
	@classproperty
	def numCities(cls):
		def owned(self, cities):
			return cities.owner(self.iPlayer)
	
		return cls.cities(owned).subclass("CityCount")
	
	@classproperty
	def settledCities(cls):
		def settled(self, cities):
			return cities.owner(self.iPlayer).where(lambda city: city.getOriginalOwner() == self.iPlayer)
		
		return cls.cities(settled).subclass("SettledCityCount")
	
	@classproperty
	def openBorders(cls):
		def withOpenBorders(self, iPlayer):
			return self._team.isOpenBorders(player(iPlayer).getTeam())
		
		return cls.players(withOpenBorders).subclass("OpenBorderCount")
	
	@classproperty
	def specialist(cls):
		return cls.types(CvSpecialistInfo).citiesSum(CyCity.getFreeSpecialistCount).subclass("SpecialistCount")
	
	@classproperty
	def averageCulture(cls):
		return cls.player(average(CyPlayer.countTotalCulture, CyPlayer.getNumCities)).subclass("AverageCulture")
	
	@classproperty
	def averagePopulation(cls):
		return cls.player(average(CyPlayer.getTotalPopulation, CyPlayer.getNumCities)).subclass("AveragePopulation")
		
	@classproperty
	def populationCities(cls):
		return cls.types(int).citiesWith(CyCity.getPopulation).subclass("PopulationCities")
	
	@classproperty
	def cultureCities(cls):
		return cls.types(int).citiesWith(lambda city: city.getCulture(city.getOwner())).subclass("CultureCities")
	
	@classproperty
	def cultureLevelCities(cls):
		return cls.types(CvCultureLevelInfo).citiesWith(CyCity.getCultureLevel).subclass("CultureLevelCities")
	
	@classproperty
	def citySpecialist(cls):
		return cls.type(CyCity).types(CvSpecialistInfo).city(CyCity.getFreeSpecialistCount).subclass("SpecialistCount")
	
	@classproperty
	def cultureLevel(cls):
		def display(self, city, iCultureLevel):
			city = city()
			return "%d / %d" % (city and city.getCulture(city.getOwner()) or 0, game.getCultureThreshold(iCultureLevel))
	
		return cls.type(CyCity).types().city(CyCity.getCultureLevel).func(display).subclass("CultureLevel")


def segment(tuple, cutoff=None):
	if cutoff:
		tuple = tuple[:cutoff]
	if len(tuple) == 1:
		return tuple[0]
	return tuple


class Track(Count):

	def __init__(self, *arguments):
		super(Track, self).__init__(*arguments)
		
		self.dCount = dict((objective[:-1], 0) for objective in self.arguments.objectives)
	
	def value_function(self, *objectives):
		return self.dCount[objectives]
	
	@property
	def values(self):
		return [segment(objective) for objective in self.dCount.keys()]
	
	def increment(self, *objectives):
		self.accumulate(1, *objectives)
	
	def accumulate(self, iChange, *objectives):
		self.dCount[objectives] += iChange
		
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
		def func(self, *args):
			self.increment()
		return cls.handle(event, func)
	
	@classmethod
	def accumulated(cls, event):
		def func(self, iChange):
			self.accumulate(iChange)
		return cls.handle(event, func).scaled
	
	@classproperty
	def goldenAges(cls):
		def required(self, objective):
			return scale(8 * objective)
	
		def incrementGoldenAges(self):
			if self._player.isGoldenAge() and not self._player.isAnarchy():
				self.increment()
		
		return cls.types().handle("BeginPlayerTurn", incrementGoldenAges).func(required).subclass("GoldenAges")
	
	@classproperty
	def eraFirsts(cls):
		def incrementFirstDiscovered(self, iTech):
			iEra = infos.tech(iTech).getEra()
			if iEra in self.values:
				if game.countKnownTechNumTeams(iTech) == 1:
					self.increment(iEra)
		
		return cls.types(CvTechInfo).handle("techAcquired", incrementFirstDiscovered).subclass("EraFirstDiscover")
	
	@classproperty
	def sunkShips(cls):
		def incrementShipsSunk(self, losingUnit):
			if infos.unit(losingUnit).getDomainType() == DomainTypes.DOMAIN_SEA:
				self.increment()
		
		return cls.types().handle("combatResult", incrementShipsSunk).subclass("SunkShips")
	
	@classproperty
	def tradeGold(cls):
		def value_function(self, *objective):
			return self.dCount[objective] / 100
		
		def accumulateTradeGold(self, iGold):
			self.accumulate(iGold * 100)
		
		def trackTradeGold(self):
			iGold = cities.owner(self.iPlayer).sum(lambda city: city.getTradeYield(YieldTypes.YIELD_COMMERCE)) * self._player.getCommercePercent(CommerceTypes.COMMERCE_GOLD)
			iGold += players.major().alive().sum(self._player.getGoldPerTurnByPlayer) * 100
			self.accumulate(iGold)
		
		return cls.types().handle("playerGoldTrade", accumulateTradeGold).handle("BeginPlayerTurn", trackTradeGold).func(value_function).subclass("TradeGold")
	
	@classproperty
	def raidGold(cls):
		return cls.types().accumulated("unitPillage").accumulated("cityCaptureGold").subclass("RaidGold")
	
	@classproperty
	def pillage(cls):
		return cls.types().incremented("unitPillage").subclass("PillageCount")
	
	@classproperty
	def acquiredCities(cls):
		return cls.types().incremented("cityAcquired").incremented("cityBuilt").subclass("AcquiredCities")
	
	@classproperty
	def piracyGold(cls):
		return cls.types().accumulated("unitPillage").accumulated("blockade").subclass("PiracyGold")
	
	@classproperty
	def razes(cls):
		return cls.types().incremented("cityRazed").subclass("RazeCount")
	
	@classproperty
	def slaveTradeGold(cls):
		return cls.types().accumulated("playerSlaveTrade").subclass("SlaveTradeGold")
	
	@classproperty
	def greatGenerals(cls):
		def incrementGreatGenerals(self, unit):
			if infos.unit(unit).getGreatPeoples(iSpecialistGreatGeneral):
				self.increment()
		
		return cls.types().handle("greatPersonBorn", incrementGreatGenerals).subclass("GreatGenerals")
	
	@classproperty
	def resourceTradeGold(cls):
		def accumulateTradeGold(self):
			iGold = players.major().alive().sum(self._player.getGoldPerTurnByPlayer)
			self.accumulate(iGold)
	
		return cls.types().handle("BeginPlayerTurn", accumulateTradeGold).scaled.subclass("ResourceTradeGold")
	
	@classproperty
	def brokeredPeace(cls):
		return cls.types().incremented("peaceBrokered").subclass("BrokeredPeace")
	
	@classproperty
	def enslaves(cls):
		return cls.types().incremented("enslave").subclass("Enslave")
	
	@classproperty
	def conquerFrom(cls):
		def incrementConquests(self, iOwner, bConquest):
			for objective in self.values:
				if bConquest and civ(iOwner) in objective:
					self.increment(objective)
		
		return cls.types(list).handle("cityAcquired", incrementConquests).subclass("ConquerFrom")