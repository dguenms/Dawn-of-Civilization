from inspect import ismethod, isfunction, getargspec
import re

from Core import *
from RFCUtils import *
from Civics import isCommunist
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
		def BeginPlayerTurn(other, args):
			iGameTurn, iPlayer = args
			if other.iPlayer == iPlayer:
				func(other)
		
		return BeginPlayerTurn
	
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
				func(other, iOwner, city, bConquest)
		
		return cityAcquired
	
	def cityLost(self, func):
		def cityAcquired(other, args):
			iOwner, iPlayer, city, bConquest, bTrade = args
			if other.iPlayer == iOwner:
				func(other, iPlayer, bConquest)
		
		return cityAcquired
	
	def cityBuilt(self, func):
		def cityBuilt(other, args):
			city = args[0]
			if other.iPlayer == city.getOwner():
				func(other, city)
		
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
				func(other, losingUnit)
		
		return enslave
	
	def firstContact(self, func):
		def firstContact(other, args):
			iTeamX, iHasMetTeamY = args
			if other._team.getID() == iTeamX:
				func(other, team(iHasMetTeamY).getLeaderID())
		
		return firstContact
	
	def tradeMission(self, func):
		def tradeMission(other, args):
			iUnit, iPlayer, iX, iY, iGold = args
			if other.iPlayer == iPlayer:
				func(other, (iX, iY), iGold)
		
		return tradeMission
	
	def religionFounded(self, func):
		def religionFounded(other, args):
			iReligion, iFounder = args
			func(other, iReligion)
		
		return religionFounded
	
	def playerChangeStateReligion(self, func):
		def playerChangeStateReligion(other, args):
			iPlayer, iNewReligion, iOldReligion = args
			if other.iPlayer == iPlayer:
				func(other, iNewReligion)
		
		return playerChangeStateReligion
				
	
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
	
def holyCity():
	def getHolyCity(iPlayer):
		iStateReligion = player(iPlayer).getStateReligion()
		if iStateReligion < 0:
			return None
		return game.getHolyCity(iStateReligion)
		
	return Deferred(lambda p: getHolyCity(p))

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
		
		self.iPlayer = None
	
	def setPlayer(self, iPlayer):
		self.iPlayer = iPlayer
		
	def produce(self, objective=[]):
		result = []
		
		if self.subject:
			result += [self.subject]
		if objective:
			result += list(objective)
		if self.iPlayer is not None:
			result += [self.iPlayer]
		
		return tuple(result)
		
	def __iter__(self):
		if self.objectives:
			for objective in self.objectives:
				yield self.produce(objective)
		else:
			yield self.produce()


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
		return bool(self.objective_types)
	
	def build(self):
		return ArgumentProcessor(self.objective_types, self.subject_type, self.objective_split)


class ArgumentProcessor(object):

	defaults = {
		int : lambda: 1,
		Players : lambda: players.major().alive(),
	}
	
	@classmethod
	def default(cls, type):
		default = cls.defaults.get(type)
		if default:
			return default()

	def __init__(self, objective_types=[], subject_type=None, objective_split=0, include_owner=False):
		if not isinstance(objective_types, list):
			raise ValueError("Objective types need to be a list")
			
		if objective_split > len(objective_types):
			raise ValueError("Objective split cannot exceed number of objective types")
	
		self.objective_types = objective_types
		self.subject_type = subject_type
		self.objective_split = objective_split
	
	def process(self, *arguments):
		if arguments and not self.objective_types and not self.subject_type:
			raise ValueError("Needs at least one objective type or subject_type")
	
		if self.subject_type:
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
		self.owner_included = False
		
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
	
	def include_owner(self):
		self.owner_included = True
		return self
		
	def members(self):
		members = dict((func.__name__, func) for func in self.funcs)
		members.update(self.attributes)
		members["handlers"] = self.handlers[:]
		members["types"] = self.types.build()
		members["owner_included"] = self.owner_included
		
		return members

	def create(self, cls, name):
		goal = type(name, (cls,), self.members())
		self.reset()
		return goal


class BaseGoal(object):

	builder = GoalBuilder()
	handlers = []
	types = None
	owner_included = False
		
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
	def objectives(cls, *types):
		cls.builder.objectives(list(types))
		return cls
	
	@classmethod
	def objective(cls, type):
		return cls.objectives(type)
	
	@classmethod
	def subject(cls, type):
		cls.builder.subject(type)
		return cls
	
	@classmethod
	def split(cls, split):
		cls.builder.split(split)
		return cls
	
	@classproperty
	def include_owner(cls):
		cls.builder.include_owner()
		return cls
	
	@classmethod
	def handle(cls, event, func):
		handler = handlers.get(event, func)
		cls.builder.handler(handler.__name__, handler)
		return cls
	
	@classmethod
	def process_arguments(cls, *arguments):
		return cls.types.process(*arguments)

	def __init__(self, *arguments):
		self.reset()
		
		self.arguments = self.process_arguments(*arguments)
		
	def __nonzero__(self):
		return all(self.condition(*args) for args in self.arguments)
	
	def __str__(self):
		return '\n'.join([self.display(*args) for args in self.arguments])
		
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
		
		if self.owner_included:
			self.arguments.iPlayer = iPlayer
		
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
		def condition(self, plots, *objectives):
			return plots.all(lambda plot: func(plot, *objectives))
		
		return cls.func(condition)
	
	@classmethod
	def cities(cls, func):
		def condition(self, plots, *objectives):
			return plots.cities().all_if_any(lambda city: func(self, city, *objectives))
		
		return cls.func(condition)
	
	@classmethod
	def city(cls, func):
		def condition(self, city, objective):
			return city() and func(city(), objective) or False
		
		return cls.func(condition)

	@classproperty
	def wonder(cls):
		return cls.objective(CvBuildingInfo).player(CyPlayer.isHasBuilding).subclass("Wonder")
	
	@classproperty
	def control(cls):
		def controlled(self, city):
			return city.getOwner() == self.iPlayer
	
		return cls.objective(Plots).cities(controlled).subclass("Control")
	
	@classproperty
	def controlOrVassalize(cls):
		def controlled_or_vassalized(self, city):
			return city.getOwner() in players.vassals(self.iPlayer).including(self.iPlayer)
		
		return cls.objective(Plots).cities(controlled_or_vassalized).subclass("ControlOrVassalize")
	
	@classproperty
	def settle(cls):
		def settled(self, city):
			return city.getOwner() == self.iPlayer and city.getOriginalOwner() == self.iPlayer
		
		return cls.objective(Plots).cities(settled).subclass("Settled")
	
	@classproperty
	def cityBuilding(cls):
		return cls.subject(CyCity).objective(CvBuildingInfo).city(CyCity.isHasRealBuilding).subclass("CityBuilding")
	
	@classproperty
	def project(cls):
		return cls.objective(CvProjectInfo).team(positive(CyTeam.getProjectCount)).subclass("ProjectCount")
	
	@classproperty
	def route(cls):
		return cls.subject(Plots).objective(CvRouteInfo).plots(equals(CyPlot.getRouteType)).subclass("Route")
		
	@classproperty
	def noStateReligion(cls):
		def no_state_religion(self, city, iReligion):
			return player(city).getStateReligion() != iReligion
	
		return cls.subject(Plots).objective(CvReligionInfo).cities(no_state_religion).subclass("NoStateReligion")
	
	@classproperty
	def cultureCovered(cls):
		def covered(plot, iPlayer):
			return plot.getOwner() == iPlayer
		
		return cls.objective(Plots).include_owner.plots(covered).subclass("CultureCovered")
	
	@classproperty
	def communist(cls):
		def condition(self, *objectives):
			return isCommunist(self.iPlayer)
		
		return cls.func(condition).subclass("Communist")
	
	@classproperty
	def noForeignCities(cls):
		oldinit = cls.__init__
		def __init__(self, *arguments):
			oldinit(self, *arguments)
			self.lOf = []
			self.lExcluded = []
		
		def of(self, lCivs):
			self.lOf = lCivs
			return self
		
		def excluding(self, lCivs):
			self.lExcluded = lCivs
			return self
		
		def valid(self, city):
			if city.getOwner() == self.iPlayer:
				return True
			if self.lOf and civ(city) not in self.lOf:
				return True
			if self.lExcluded and civ(city) in self.lExcluded:
				return True
			if is_minor(city):
				return True
			return False
		
		return cls.objective(Plots).func(__init__, of, excluding).cities(valid).subclass("NoForeignCities")
	
	@classproperty
	def tradeConnection(cls):
		def condition(self):
			return players.major().alive().without(self.iPlayer).any(lambda p: self._player.canContact(p) and self._player.canTradeNetworkWith(p))
		
		return cls.func(condition).subclass("TradeConnection")
	
	@classproperty
	def moreReligion(cls):
		def religionCities(self, plots, iReligion):
			return plots.cities().religion(iReligion).count()
		
		def condition(self, plots, iOurReligion, iOtherReligion):
			return self.religionCities(plots, iOurReligion) > self.religionCities(plots, iOtherReligion)
		
		def display(self, plots, iOurReligion, iOtherReligion):
			return "%d / %d" % (self.religionCities(plots, iOurReligion), self.religionCities(plots, iOtherReligion))
		
		return cls.subject(Plots).objectives(CvReligionInfo, CvReligionInfo).func(religionCities, condition, display).subclass("MoreReligion")
	
	@classproperty
	def moreCulture(cls):
		oldinit = cls.__init__
		def __init__(self, *arguments):
			oldinit(self, *arguments)
			self.lCivs = range(iNumCivs)
			
		def than(self, lCivs):
			self.lCivs = lCivs
			return self
			
		def condition(self):
			return self.value() >= self.required()
		
		def display(self):
			return "%d / %d" % (self.value(), self.required())
	
		def value(self):
			return self._player.countTotalCulture()
		
		def required(self):
			return players.major().alive().without(self.iPlayer).civs(*self.lCivs).sum(lambda p: player(p).countTotalCulture())
		
		return cls.func(__init__, than, condition, display, value, required).subclass("MoreCulture")
	

class Count(BaseGoal):

	@classmethod
	def objectives(cls, *types):
		types = list(types) + [int]
		cls.builder.objectives(types)
		return cls
	
	@classmethod
	def subclass(cls, name):
		if not cls.builder.types.initialized():
			cls.objectives()
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
		
		return cls.objective(Plots).func(value_function)
	
	@classmethod
	def players(cls, func):
		def value_function(self, *arguments):
			return players.major().alive().where(lambda p: func(self, p, *arguments)).count()
		
		return cls.func(value_function)
		
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
		return cls.objective(CvBuildingInfo).player(CyPlayer.countNumBuildings).subclass("BuildingCount")
	
	@classproperty
	def culture(cls):
		return cls.player(CyPlayer.countTotalCulture).scaled.subclass("PlayerCulture")
	
	@classproperty
	def gold(cls):
		return cls.player(CyPlayer.getGold).scaled.subclass("PlayerGold")
	
	@classproperty
	def resource(cls):
		return cls.objective(CvBonusInfo).player(CyPlayer.getNumAvailableBonuses).subclass("ResourceCount")
	
	@classproperty
	def controlledResource(cls):
		def resources(player, objective):
			return player.getNumAvailableBonuses(objective) - player.getBonusImport(objective)
	
		return cls.objective(CvBonusInfo).playervassals(resources).subclass("ControlledResourceCount")
		
	@classproperty
	def improvement(cls):
		return cls.objective(CvImprovementInfo).player(CyPlayer.getImprovementCount).subclass("ImprovementCount")
	
	@classproperty
	def population(cls):
		return cls.player(CyPlayer.getTotalPopulation).subclass("PlayerPopulation")
	
	@classproperty
	def corporation(cls):
		return cls.objective(CvCorporationInfo).player(CyPlayer.countCorporations).subclass("CorporationCount")
	
	@classproperty
	def unit(cls):
		def value_function(self, objective):
			return self._player.getUnitClassCount(infos.unit(objective).getUnitClassType())
		
		return cls.objective(CvUnitInfo).func(value_function).subclass("UnitCount")
		
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
	def conqueredCities(cls):
		oldinit = cls.__init__
		def __init__(self, *arguments):
			oldinit(self, *arguments)
			self.conquered = plots.none()
			self.lCivs = []
			self.plots = plots.none()
		
		def civs(self, lCivs):
			self.lCivs = lCivs
			return self
		
		def area(self, plots):
			self.plots = plots
			return self
		
		def onCityAcquired(self, iOwner, city, bConquest):
			if bConquest and (not self.lCivs or civ(iOwner) in self.lCivs) and (not self.plots or city in self.plots):
				self.conquered = self.conquered.including(city)
		
		def value_function(self):
			return cities.owner(self.iPlayer).where(lambda city: city in self.conquered).count()
		
		return cls.func(__init__, civs, area, value_function).handle("cityAcquired", onCityAcquired).subclass("ConqueredCityCount")
	
	@classproperty
	def openBorders(cls):
		oldinit = cls.__init__
		def __init__(self, *arguments):
			oldinit(self, *arguments)
			self.lCivs = []
			
		def civs(self, lCivs):
			self.lCivs = lCivs
			return self
	
		def valid(self, iPlayer):
			if self.lCivs and civ(iPlayer) not in self.lCivs:
				return False
		
			return self._team.isOpenBorders(player(iPlayer).getTeam())
		
		return cls.func(__init__, civs).players(valid).subclass("OpenBorderCount")
	
	@classproperty
	def specialist(cls):
		return cls.objective(CvSpecialistInfo).citiesSum(CyCity.getFreeSpecialistCount).subclass("SpecialistCount")
	
	@classproperty
	def averageCulture(cls):
		return cls.player(average(CyPlayer.countTotalCulture, CyPlayer.getNumCities)).subclass("AverageCulture")
	
	@classproperty
	def averagePopulation(cls):
		return cls.player(average(CyPlayer.getTotalPopulation, CyPlayer.getNumCities)).subclass("AveragePopulation")
		
	@classproperty
	def populationCities(cls):
		return cls.objective(int).citiesWith(CyCity.getPopulation).subclass("PopulationCities")
	
	@classproperty
	def cultureCities(cls):
		return cls.objective(int).citiesWith(lambda city: city.getCulture(city.getOwner())).subclass("CultureCities")
	
	@classproperty
	def cultureLevelCities(cls):
		return cls.objective(CvCultureLevelInfo).citiesWith(CyCity.getCultureLevel).subclass("CultureLevelCities")
	
	@classproperty
	def citySpecialist(cls):
		return cls.subject(CyCity).objective(CvSpecialistInfo).city(CyCity.getFreeSpecialistCount).subclass("CitySpecialistCount")
	
	@classproperty
	def cultureLevel(cls):
		def display(self, city, iCultureLevel):
			city = city()
			return "%d / %d" % (city and city.getCulture(city.getOwner()) or 0, game.getCultureThreshold(iCultureLevel))
	
		return cls.subject(CyCity).city(CyCity.getCultureLevel).func(display).subclass("CultureLevel")
	
	@classproperty
	def attitude(cls):
		oldinit = cls.__init__
		def __init__(self, *arguments):
			oldinit(self, *arguments)
			self.lCivs = []
			self.iStateReligion = -1
			self.bCommunist = False
		
		def civs(self, lCivs):
			self.lCivs = lCivs
			return self
		
		def religion(self, iStateReligion):
			self.iStateReligion = iStateReligion
			return self
		
		def communist(self):
			self.bCommunist = True
			return self
		
		def valid(self, iPlayer, iAttitude):
			if not self._player.canContact(iPlayer):
				return False
			if team(iPlayer).isAVassal():
				return False
			if self.lCivs and civ(iPlayer) not in self.lCivs:
				return False
			if self.iStateReligion >= 0 and player(iPlayer).getStateReligion() != self.iStateReligion:
				return False
			if self.bCommunist and not isCommunist(iPlayer):
				return False
			
			return player(iPlayer).AI_getAttitude(self.iPlayer) >= iAttitude
		
		return cls.subject(AttitudeTypes).func(__init__, civs, religion, communist).players(valid).subclass("AttitudeCount")
	
	@classproperty
	def vassals(cls):
		oldinit = cls.__init__
		def __init__(self, *arguments):
			oldinit(self, *arguments)
			self.lCivs = []
			self.iStateReligion = -1
		
		def civs(self, lCivs):
			self.lCivs = lCivs
			return self
		
		def religion(self, iStateReligion):
			self.iStateReligion = iStateReligion
			return self
		
		def valid(self, iPlayer):
			if self.lCivs and civ(iPlayer) not in self.lCivs:
				return False
			if self.iStateReligion and player(iPlayer).getStateReligion() != self.iStateReligion:
				return False
			
			return team(iPlayer).isVassal(self._team.getID())
		
		return cls.func(__init__, civs, religion).players(valid).subclass("VassalCount")


class Percentage(Count):

	def condition(self, *arguments):
		remainder, iRequired = arguments[:-1], arguments[-1]
		return self.value(*remainder) >= self.required(iRequired) * 1.0 - 0.005
		
	def display(self, *arguments):
		remainder, iRequired = arguments[:-1], arguments[-1]
		return "%.2f%% / %d%%" % (self.value(*remainder), self.required(iRequired))
	
	def value(self, *objectives):
		iTotal = self.total(*objectives)
		if iTotal <= 0:
			return 0.0
		return 100.0 * self.player_value(*objectives) / iTotal
		
	def player_value(self, *objectives):
		return self.value_function(self.iPlayer, *objectives)
	
	def total(self, *objectives):
		return players.major().alive().sum(lambda p: self.value_function(p, *objectives))
	
	@classproperty
	def allied(cls):
		def player_value(self, *objectives):
			iPlayerValue = 0
			for iPlayer in players.major().alive():
				iValue = self.value_function(iPlayer, *objectives)
				iMaster = master(iPlayer)
				
				if self.iPlayer == iPlayer or self._team.isDefensivePact(player(iPlayer).getTeam()):
					iPlayerValue += iValue
				elif iMaster is not None and (iMaster == self.iPlayer or self._team.isDefensivePact(player(iMaster).getTeam())):
					iPlayerValue += iValue
			
			return iPlayerValue
		
		return cls.func(player_value)
		
	@classproperty
	def areaControl(cls):
		def value_function(self, iPlayer, area):
			return area.land().owner(iPlayer).count()
		
		def total(self, area):
			return area.land().count()
		
		return cls.objective(Plots).func(value_function, total).subclass("AreaPercent")
	
	@classproperty
	def worldControl(cls):
		def value_function(self, iPlayer):
			return player(iPlayer).getTotalLand()
		
		def total(self):
			return map.getLandPlots()
		
		return cls.func(value_function, total).subclass("WorldPercent")
	
	@classproperty
	def religionSpread(cls):
		def value(self, iReligion):
			return game.calculateReligionPercent(iReligion)
		
		return cls.objective(CvReligionInfo).func(value).subclass("ReligionSpreadPercent")
	
	@classproperty
	def population(cls):
		def value_function(self, iPlayer):
			return team(iPlayer).getTotalPopulation()
		
		def total(self):
			return game.getTotalPopulation()
		
		return cls.func(value_function, total).subclass("PopulationPercent")
	
	@classproperty
	def religiousVote(cls):
		def value_function(self, iPlayer):
			return player(iPlayer).getVotes(16, 1)
		
		return cls.func(value_function).subclass("ReligiousVotePercent")
	
	@classproperty
	def alliedCommerce(cls):
		def value_function(self, iPlayer):
			return player(iPlayer).calculateTotalCommerce()
		
		return cls.allied.func(value_function).subclass("AlliedCommercePercent")
	
	@classproperty
	def alliedPower(cls):
		def value_function(self, iPlayer):
			return player(iPlayer).getPower()
		
		return cls.allied.func(value_function).subclass("AlliedPowerPercent")


def segment(tuple):
	if len(tuple) == 1:
		return tuple[0]
	return tuple
	
	
class Trigger(Condition):

	def __init__(self, *arguments):
		super(Trigger, self).__init__(*arguments)
		
		self.dCondition = dict((self.process_objectives(args), False) for args in self.arguments)
	
	def condition(self, *arguments):
		return self.dCondition[self.process_objectives(arguments)]
		
	def complete(self, *objectives):
		self.dCondition[self.arguments.produce(objectives)] = True
	
	def process_objectives(self, arguments):
		if isinstance(segment(arguments), Deferred):
			return tuple()
		return arguments
	
	@property
	def values(self):
		return [segment(objective) for objective in self.arguments.objectives]
	
	@classproperty
	def failable(cls):
		oldinit = cls.__init__
		def __init__(self, *arguments):
			oldinit(self, *arguments)
			self.complete()
		return cls.func(__init__)
	
	@classproperty
	def firstDiscover(cls):
		def checkFirstDiscovered(self, iTech):
			if iTech in self.values:
				if game.countKnownTechNumTeams(iTech) == 1:
					self.complete(iTech)
		
		return cls.objective(CvTechInfo).handle("techAcquired", checkFirstDiscovered).subclass("FirstDiscovered")
	
	@classproperty
	def firstNewWorld(cls):
		def checkFirstNewWorld(self, city):
			if city in plots.regions(*lAmerica) and cities.regions(*lAmerica).without(city).none(lambda city: civ(city.getOriginalOwner()) not in dCivGroups[iCivGroupAmerica]):
				self.complete()
	
		return cls.handle("cityBuilt", checkFirstNewWorld).subclass("FirstNewWorld")
	
	@classproperty
	def discover(cls):
		def checkDiscovered(self, iTech):
			if iTech in self.values:
				self.complete(iTech)
		
		return cls.objective(CvTechInfo).handle("techAcquired", checkDiscovered).subclass("Discovered")
	
	@classproperty
	def firstContact(cls):
		def checkFirstContact(self, iOtherPlayer):
			if civ(iOtherPlayer) in self.values:
				if self.arguments.subject.land().none(lambda plot: plot.isRevealed(iOtherPlayer, False)):
					self.complete(civ(iOtherPlayer))
				else:
					self.fail()
		
		return cls.subject(Plots).objective(Civ).handle("firstContact", checkFirstContact).subclass("FirstContact")
	
	@classproperty
	def noCityLost(cls):
		def checkCityLost(self, iOtherPlayer, bConquest):
			self.fail()
		
		return cls.failable.handle("cityLost", checkCityLost).subclass("NoCityLost")
	
	@classproperty
	def tradeMission(cls):
		def checkTradeMission(self, tile, iGold):
			if tile in cities.of([city(self.iPlayer) for city in self.values if city(self.iPlayer) is not None]):
				self.complete()
		
		return cls.objective(CyCity).handle("tradeMission", checkTradeMission).subclass("TradeMission")
	
	@classproperty
	def neverConquer(cls):
		def checkCityAcquired(self, iOwner, city, bConquest):
			if bConquest:
				self.fail()
		
		return cls.failable.handle("cityAcquired", checkCityAcquired).subclass("NeverConquer")
	
	@classproperty
	def convertAfterFounding(cls):
		oldinit = cls.__init__
		def __init__(self, *arguments):
			oldinit(self, *arguments)
			self.dFoundingTurn = defaultdict()
		
		def recordFounding(self, iReligion):
			if iReligion in self.values:
				self.dFoundingTurn[iReligion] = turn()
		
		def checkConversion(self, iReligion):
			if iReligion in self.values:
				if turn() - self.dFoundingTurn[iReligion] <= scale(self.arguments.subject):
					self.complete(iReligion)
				else:
					self.fail()
		
		return cls.subject(int).objective(CvReligionInfo).func(__init__).handle("religionFounded", recordFounding).handle("playerChangeStateReligion", checkConversion).subclass("ConvertAfterFounding")
		
		

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
		
		return cls.handle("BeginPlayerTurn", incrementGoldenAges).func(required).subclass("GoldenAges")
	
	@classproperty
	def eraFirsts(cls):
		def incrementFirstDiscovered(self, iTech):
			iEra = infos.tech(iTech).getEra()
			if iEra in self.values:
				if game.countKnownTechNumTeams(iTech) == 1:
					self.increment(iEra)
		
		return cls.objective(CvTechInfo).handle("techAcquired", incrementFirstDiscovered).subclass("EraFirstDiscover")
	
	@classproperty
	def sunkShips(cls):
		def incrementShipsSunk(self, losingUnit):
			if infos.unit(losingUnit).getDomainType() == DomainTypes.DOMAIN_SEA:
				self.increment()
		
		return cls.handle("combatResult", incrementShipsSunk).subclass("SunkShips")
	
	@classproperty
	def tradeGold(cls):
		def value_function(self, *objective):
			return self.dCount[objective] / 100
		
		def accumulateTradeGold(self, iGold):
			self.accumulate(iGold * 100)
			
		def accumulateTradeMissionGold(self, tile, iGold):
			self.accumulate(iGold * 100)
		
		def trackTradeGold(self):
			iGold = cities.owner(self.iPlayer).sum(lambda city: city.getTradeYield(YieldTypes.YIELD_COMMERCE)) * self._player.getCommercePercent(CommerceTypes.COMMERCE_GOLD)
			iGold += players.major().alive().sum(self._player.getGoldPerTurnByPlayer) * 100
			self.accumulate(iGold)
		
		return cls.handle("playerGoldTrade", accumulateTradeGold).handle("tradeMission", accumulateTradeMissionGold).handle("BeginPlayerTurn", trackTradeGold).func(value_function).subclass("TradeGold")
	
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
			iGold = players.major().alive().sum(self._player.getGoldPerTurnByPlayer)
			self.accumulate(iGold)
	
		return cls.handle("BeginPlayerTurn", accumulateTradeGold).scaled.subclass("ResourceTradeGold")
	
	@classproperty
	def brokeredPeace(cls):
		return cls.incremented("peaceBrokered").subclass("BrokeredPeace")
	
	@classproperty
	def enslaves(cls):
		oldinit = cls.__init__
		def __init__(self, *arguments):
			oldinit(self, *arguments)
			self.lExcluded = []
		
		def excluding(self, lCivs):
			self.lExcluded = lCivs
			return self
		
		def incrementEnslaves(self, losingUnit):
			if civ(losingUnit) not in self.lExcluded:
				self.increment()
	
		return cls.func(__init__, excluding).handle("enslave", incrementEnslaves).subclass("Enslave")


class Best(BaseGoal):

	def __init__(self, *arguments):
		super(Best, self).__init__(*arguments)
		
	def metric_wrapper(self, item):
		if item is None:
			return 0
		return self.metric(item)
		
	def sorted(self, *arguments):
		return self.entities().sort(lambda item: (self.metric_wrapper(item), int(self.valid(item, *arguments))), True)
		
	def condition(self, *arguments):
		first = self.sorted(*arguments).first()
		return self.valid(first, *arguments)
	
	def display(self, *arguments):
		if self.condition(*arguments):
			first, second = self.sorted(*arguments).take(2)
		else:
			sorted = self.sorted(*arguments)
			first = sorted.first()
			second = sorted.where(lambda item: self.valid(item, *arguments)).first()
		
		return "%s (%d)\n%s (%d)" % (self.entity_name(first), self.metric_wrapper(first), self.entity_name(second), self.metric_wrapper(second))
	
	
class BestCity(Best):

	def __init__(self, *arguments):
		return super(BestCity, self).__init__(*arguments)
		
	def entities(self):
		return cities.all()
	
	def entity_name(self, city):
		if city is None:
			return "(No City)"
		return city.getName()
	
	def valid(self, city, requiredCity):
		if city is None:
			return False
		if requiredCity() is None:
			return False
		return city.getOwner() == self.iPlayer and at(city, requiredCity())
	
	@classproperty
	def population(cls):
		def metric(self, city):
			return city.getPopulation()
		
		return cls.subject(CyCity).func(metric).subclass("BestPopulationCity")
	
	@classproperty
	def culture(cls):
		def metric(self, city):
			return city.getCulture(city.getOwner())
		
		return cls.subject(CyCity).func(metric).subclass("BestCultureCity")
	

class BestPlayer(Best):

	def __init__(self, *arguments):
		super(BestPlayer, self).__init__(*arguments)
	
	def entities(self):
		return players.major().alive()
	
	def entity_name(self, iPlayer):
		return name(iPlayer)
	
	def valid(self, iPlayer):
		return self.iPlayer == iPlayer
	
	@classproperty
	def tech(cls):
		def metric(self, iPlayer):
			return infos.techs().where(lambda iTech: team(iPlayer).isHasTech(iTech)).sum(lambda iTech: infos.tech(iTech).getResearchCost())
		
		return cls.func(metric).subclass("BestTechPlayer")
	
	@classproperty
	def population(cls):
		def metric(self, iPlayer):
			return player(iPlayer).getRealPopulation()
		
		return cls.func(metric).subclass("BestPopulationPlayer")
	
	