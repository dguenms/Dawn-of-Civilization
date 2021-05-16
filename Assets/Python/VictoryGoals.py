from inspect import ismethod, isfunction, getargspec
import re, heapq

from Core import *
from RFCUtils import *
from Civics import isCommunist
from CityNameManager import getRenameName
from Events import events

import BugCore
AdvisorOpt = BugCore.game.Advisors
AlertsOpt = BugCore.game.MoreCiv4lerts


sum_ = sum
capital_ = capital


POSSIBLE, SUCCESS, FAILURE = range(3)

lGreatPeople = [iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy]


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

	@classmethod
	def ours(cls):
		def applicable(other, iPlayer):
			return other.iPlayer == iPlayer
		return cls(applicable)
	
	@classmethod
	def others(cls):
		def applicable(other, iPlayer):
			return other.iPlayer != iPlayer
		return cls(applicable)
	
	@classmethod
	def any(cls):
		def applicable(other, iPlayer):
			return True
		return cls(applicable)

	def __init__(self, applicable):
		self.applicable = applicable
		
	def get(self, event, func):
		if hasattr(self, event):
			handler_func = getattr(self, event)
			if ismethod(handler_func):
				return handler_func(func)
		
		raise Exception("No handler available for event '%s'" % event)
	
	def BeginPlayerTurn(self, func):
		def BeginPlayerTurn(other, args):
			iGameTurn, iPlayer = args
			if self.applicable(other, iPlayer):
				func(other, iGameTurn)
		
		return BeginPlayerTurn
	
	def techAcquired(self, func):
		def techAcquired(other, args):
			iTech, iTeam, iPlayer, bAnnounce = args
			if self.applicable(other, iPlayer):
				func(other, iTech)
	
		return techAcquired
	
	def combatResult(self, func):
		def combatResult(other, args):
			winningUnit, losingUnit = args
			if self.applicable(other, winningUnit.getOwner()):
				func(other, losingUnit)
		
		return combatResult
	
	def playerGoldTrade(self, func):
		def playerGoldTrade(other, args):
			iFrom, iTo, iGold = args
			if self.applicable(other, iTo):
				func(other, iGold)
		
		return playerGoldTrade
	
	def unitPillage(self, func):
		def unitPillage(other, args):
			unit, iImprovement, iRoute, iPlayer, iGold = args
			if self.applicable(other, iPlayer):
				func(other, iGold)
		
		return unitPillage
	
	def cityCaptureGold(self, func):
		def cityCaptureGold(other, args):
			city, iPlayer, iGold = args
			if self.applicable(other, iPlayer):
				func(other, iGold)
		
		return cityCaptureGold
	
	def cityAcquired(self, func):
		def cityAcquired(other, args):
			iOwner, iPlayer, city, bConquest, bTrade = args
			if self.applicable(other, iPlayer):
				func(other, iOwner, city, bConquest)
		
		return cityAcquired
	
	def cityLost(self, func):
		def cityAcquired(other, args):
			iOwner, iPlayer, city, bConquest, bTrade = args
			if self.applicable(other, iOwner):
				func(other, iPlayer, bConquest)
		
		return cityAcquired
	
	def cityBuilt(self, func):
		def cityBuilt(other, args):
			city = args[0]
			if self.applicable(other, city.getOwner()):
				func(other, city)
		
		return cityBuilt
	
	def blockade(self, func):
		def blockade(other, args):
			iPlayer, iGold = args
			if self.applicable(other, iPlayer):
				func(other, iGold)
		
		return blockade
	
	def cityRazed(self, func):
		def cityRazed(other, args):
			city, iPlayer = args
			if self.applicable(other, iPlayer):
				func(other)
		
		return cityRazed
	
	def playerSlaveTrade(self, func):
		def playerSlaveTrade(other, args):
			iPlayer, iGold = args
			if self.applicable(other, iPlayer):
				func(other, iGold)
		
		return playerSlaveTrade
	
	def greatPersonBorn(self, func):
		def greatPersonBorn(other, args):
			unit, iPlayer, city = args
			if self.applicable(other, iPlayer):
				func(other, unit)
		
		return greatPersonBorn
	
	def peaceBrokered(self, func):
		def peaceBrokered(other, args):
			iBroker, iPlayer1, iPlayer2 = args
			if self.applicable(other, iBroker):
				func(other)
		
		return peaceBrokered
	
	def enslave(self, func):
		def enslave(other, args):
			iPlayer, losingUnit = args
			if self.applicable(other, iPlayer):
				func(other, losingUnit)
		
		return enslave
	
	def firstContact(self, func):
		def firstContact(other, args):
			iTeamX, iHasMetTeamY = args
			if self.applicable(other, team(iTeamX).getLeaderID()):
				func(other, team(iHasMetTeamY).getLeaderID())
		
		return firstContact
	
	def tradeMission(self, func):
		def tradeMission(other, args):
			iUnit, iPlayer, iX, iY, iGold = args
			if self.applicable(other, iPlayer):
				func(other, (iX, iY), iGold)
		
		return tradeMission
	
	def religionFounded(self, func):
		def religionFounded(other, args):
			iReligion, iFounder = args
			if self.applicable(other, iFounder):
				func(other, iReligion)
		
		return religionFounded
	
	def playerChangeStateReligion(self, func):
		def playerChangeStateReligion(other, args):
			iPlayer, iNewReligion, iOldReligion = args
			if self.applicable(other, iPlayer):
				func(other, iNewReligion)
		
		return playerChangeStateReligion
	
	def buildingBuilt(self, func):
		def buildingBuilt(other, args):
			city, iBuilding = args
			if self.applicable(other, city.getOwner()):
				func(other, city, iBuilding)
		
		return buildingBuilt
	
	def projectBuilt(self, func):
		def projectBuilt(other, args):
			city, iProject = args
			if self.applicable(other, city.getOwner()):
				func(other, iProject)
		
		return projectBuilt
	
	def corporationSpread(self, func):
		def corporationSpread(other, args):
			iCorporation, iPlayer, city = args
			if self.applicable(other, iPlayer):
				func(other, iCorporation)
		
		return corporationSpread
	
	def corporationRemove(self, func):
		def corporationRemove(other, args):
			iCorporation, iPlayer, city = args
			if self.applicable(other, iPlayer):
				func(other, iCorporation)
		
		return corporationRemove
	
	def vassalState(self, func):
		def vassalState(other, args):
			iMaster, iVassal, bVassal, bCapitulated = args
			if self.applicable(other, iMaster):
				func(other)
		
		return vassalState
	
	def combatGold(self, func):
		def combatGold(other, args):
			iPlayer, unit, iGold = args
			if self.applicable(other, iPlayer):
				func(other, iGold)
		
		return combatGold
	
	def combatFood(self, func):
		def combatFood(other, args):
			iPlayer, unit, iFood = args
			if self.applicable(other, iPlayer):
				func(other, iFood)
		
		return combatFood
	
	def sacrificeHappiness(self, func):
		def sacrificeHappiness(other, args):
			iPlayer, city = args
			if self.applicable(other, iPlayer):
				func(other)
		
		return sacrificeHappiness
				
	
handlers = EventHandlers.ours()


class classproperty(property):
    def __get__(self, obj, objtype=None):
        return super(classproperty, self).__get__(objtype)
    def __set__(self, obj, value):
        super(classproperty, self).__set__(type(obj), value)
    def __delete__(self, obj):
        super(classproperty, self).__delete__(type(obj))


class Deferred(object):
	
	def __init__(self, type):
		self.type = type
		self._name = ""
	
	def __call__(self, iPlayer=None):
		raise NotImplementedError()
	
	def __str__(self):
		return self.name()
	
	def named(self, name, *args):
		self._name = text("TXT_KEY_UHV_NAME_" + name, *args)
		return self
	
	def name(self):
		return self._name
	
	def area(self):
		return None


class DeferredCapital(Deferred):

	def __init__(self):
		super(DeferredCapital, self).__init__(CyCity)
	
	def __call__(self, iPlayer):
		return capital_(iPlayer)


class DeferredCity(Deferred):

	def __init__(self, tile):
		super(DeferredCity, self).__init__(CyCity)
		self.tile = location(tile)
	
	def __call__(self, iPlayer=None):
		return city_(self.tile)
	
	def area(self):
		return plots.of([self.tile])


class DeferredStateReligion(Deferred):

	def __call__(self, iPlayer):
		if iPlayer is None:
			return None
			
		iStateReligion = player(iPlayer).getStateReligion()
		if iStateReligion < 0:
			return None
			
		return self.religionValue(iStateReligion)
	
	def religionValue(self, iReligion):
		raise NotImplementedError()


class DeferredHolyCity(DeferredStateReligion):

	def __init__(self):
		super(DeferredHolyCity, self).__init__(CyCity)
	
	def religionValue(self, iReligion):
		return game.getHolyCity(iReligion)


class DeferredWonder(Deferred):

	def __init__(self, iWonder):
		super(DeferredWonder, self).__init__(CyCity)
		self.iWonder = iWonder
	
	def __call__(self, iPlayer=None):
		return getBuildingCity(self.iWonder)


class DeferredStateReligionBuilding(DeferredStateReligion):

	def __init__(self, iSpecialBuilding):
		super(DeferredStateReligionBuilding, self).__init__(CvBuildingInfo)
		self.iSpecialBuilding = iSpecialBuilding
	
	def religionValue(self, iReligion):
		return specialbuilding(self.iSpecialBuilding, iReligion)


class DeferredShrine(DeferredStateReligion):

	def __init__(self):
		super(DeferredShrine, self).__init__(CvBuildingInfo)
	
	def religionValue(self, iReligion):
		return shrine(iReligion)


def capital():
	return DeferredCapital().named("CAPITAL")

def city(*tile):
	tile = duplefy(*tile)
	return DeferredCity(tile)
	
def holyCity(iReligion = None):
	deferred = DeferredHolyCity()

	if iReligion is None:
		return deferred.named("HOLY_CITY")
	
	return deferred.named("RELIGION_HOLY_CITY", text(infos.religion(iReligion).getAdjectiveKey()))

def wonder(iWonder):
	return DeferredWonder(iWonder)

def stateReligionBuilding(iSpecialBuilding):
	return DeferredStateReligionBuilding(iSpecialBuilding)

def stateReligionCathedral():
	return stateReligionBuilding(infos.type('SPECIALBUILDING_CATHEDRAL')).named("STATE_RELIGION_CATHEDRAL")

def area(item):
	if isinstance(item, Plots):
		return item
	elif isinstance(item, Deferred):
		return item.area()
	return plots.none()

def simple_name(name):
	if not name:
		return name
	return name.replace("the", "").lstrip()


class Aggregate(object):

	def __init__(self, *items):
		self.items = list(variadic(*items))
		self._name = None
		
		self._join = text("TXT_KEY_AND")
	
	def __iter__(self):
		return iter(self.items)
	
	def __contains__(self, item):
		return item in self.items
	
	def __eq__(self, item):
		return item in self.items
	
	@property
	def name(self):
		return self._name
	
	def aggregate(self, items):
		raise NotImplementedError()
	
	def eval(self, func, *args):
		return self.aggregate([func(*concat(args, item)) for item in self.items])
	
	def format(self, formatter):
		if self._name:
			return self._name
		
		return format_separators_shared(self.items, ",", self._join, formatter)
	
	def named(self, key):
		self._name = text("TXT_KEY_UHV_%s" % key)
		return self
	
	def join(self, key):
		self._join = text("TXT_KEY_%s" % key)
		return self
	
	def isTotal(self):
		return not self._name and len(self.items) > 1


class SumAggregate(Aggregate):

	def aggregate(self, items):
		return sum_(items)


class AverageAggregate(Aggregate):

	def aggregate(self, items):
		if len(items) == 0:
			return 0.0
		return sum_(items) / len(items)


class CountAggregate(Aggregate):

	def aggregate(self, items):
		return count(items)

	
def sum(*items):
	return SumAggregate(*items)

def avg(*items):
	return AverageAggregate(*items)

def different(*items):
	return CountAggregate(*items)


def religious_buildings(func):
	return sum(func(iReligion) for iReligion in infos.religions())

def wonders():
	return sum(iBuilding for iBuilding in infos.buildings() if isWonder(iBuilding)).named("WONDERS")

def pagan_wonders():
	return sum(iBuilding for iBuilding in infos.buildings() if isWonder(iBuilding) and infos.building(iBuilding).isPagan()).named("PAGAN_WONDERS")

def happiness_resources():
	return (iBonus for iBonus in infos.bonuses() if infos.bonus(iBonus).getHappiness() > 0)

def great_people():
	return sum(*lGreatPeople).named("GREAT_PEOPLE")


class NamedList(object):

	def __init__(self, *elements):
		self.elements = variadic(*elements)
		self.name = ""
	
	def named(self, key):
		self.name = text("TXT_KEY_%s" % key)
		return self
	
	def __str__(self):
		if self.name:
			return self.name
		return str(self.elements)
	
	def __len__(self):
		return len(self.elements)
	
	def __iter__(self):
		return iter(self.elements)
	
	def __nonzero__(self):
		return bool(self.elements)
	
	def __eq__(self, other):
		if isinstance(other, NamedList):
			return self.elements == other.elements
		elif isinstance(other, list):
			return self.elements == other
		return False


def group(iGroup):
	return NamedList(dCivGroups[iGroup])


class Arguments(object):

	def __init__(self, objectives, subject=None):
		self.subject = subject
		self.objectives = objectives
		
		self.iPlayer = None
		self.owner_included = False
	
	def value(self, item):
		if isinstance(item, Deferred):
			return item(self.iPlayer)
		return item
		
	def produce(self, objective=[]):
		result = []
		
		if self.subject:
			result += [self.value(self.subject)]
		if objective:
			result += list(self.value(obj) for obj in objective)
		if self.owner_included:
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
		
		self.options = FormatOptions()
	
	def withObjectiveTypes(self, *objective_types):
		self.objective_types = list(objective_types)
		return self
	
	def withSubjectType(self, subject_type):
		self.subject_type = subject_type
		return self
	
	def withObjectiveSplit(self, objective_split):
		self.objective_split = objective_split
		return self
		
	def withOptions(self, options):
		self.options = options
		return self
		
	def initialized(self):
		return bool(self.objective_types)
	
	def build(self):
		return ArgumentProcessor(self.objective_types, self.subject_type, self.objective_split, self.options)


class FormatOptionsBuilder(object):

	def objective(self, key):
		return FormatOptions().objective(key)
	
	def entity(self, key):
		return FormatOptions().entity(key)
	
	def city(self):
		return FormatOptions().city()
	
	def singular(self):
		return FormatOptions().singular()
	
	def number_word(self):
		return FormatOptions().number_word()
	
	def noSingularCount(self, func):
		return FormatOptions().noSingularCount(func)
	
	def type(self, type, formatter):
		return FormatOptions().type(type, formatter)


options = FormatOptionsBuilder()

		
class FormatOptions(object):

	def __init__(self):
		self.objective_key = None
		self.entity_key = None
		
		self.bPlural = True
		self.bNumberWord = False
		self.bCount = False
		
		self.no_singular_count = None
		
		self.type_formatters = {}
	
	def objective(self, key):
		self.objective_key = "TXT_KEY_UHV_%s" % key
		return self
	
	def entity(self, key):
		self.entity_key = "TXT_KEY_UHV_%s" % key
		self.count()
		return self
	
	def city(self):
		return self.entity("CITY")
	
	def singular(self):
		self.bPlural = False
		return self
	
	def number_word(self):
		self.bNumberWord = True
		return self
	
	def count(self):
		self.bCount = True
		return self
	
	def noSingularCount(self, func):
		self.no_singular_count = func
		return self
	
	def type(self, type, formatter):
		self.type_formatters[type] = formatter
		return self
	
	def type_formatter(self, type):
		return self.type_formatters.get(type)


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

	def __init__(self, objective_types=[], subject_type=None, objective_split=0, format_options=FormatOptions()):
		if not isinstance(objective_types, list):
			raise ValueError("Objective types need to be a list")
			
		if objective_split > len(objective_types):
			raise ValueError("Objective split cannot exceed number of objective types")
	
		self.objective_types = objective_types
		self.subject_type = subject_type
		self.objective_split = objective_split
		
		self.options = format_options
	
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
		
		return self.transform(self.subject_type, subject)
		
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
		if isinstance(value, Deferred):
			return issubclass(type, value.type)
	
		if issubclass(type, CvInfoBase):
			return isinstance(value, (int, Aggregate))
		elif issubclass(type, UnitCombatTypes):
			return isinstance(value, (UnitCombatTypes, Aggregate))
		elif issubclass(type, Plots):
			return isinstance(value, (Plots, Aggregate))
		return isinstance(value, type)
	
	def transform(self, type, value):
		if isinstance(value, Aggregate):
			value.items = [self.transform(type, item) for item in value]
			return value
		
		if isinstance(value, Deferred):
			return value
	
		if issubclass(type, list):
			return tuple(value)
		
		if issubclass(type, (AttitudeTypes, UnitCombatTypes)):
			return int(value)
		
		return value
	
	def is_count(self):
		return self.options.bCount or (len(self.objective_types) == 2 and self.objective_types[1] == int)
	
	def format_values(self, values):
		return [self.format_value(type, value) for type, value in zip(self.objective_types, values)]
	
	def format_objective(self, values):
		formatted_values = self.format_values(values)
		
		if self.is_count():
			count = values[-1]
			bAggregate = isinstance(values[0], Aggregate)
		
			if self.options.entity_key:
				formatted_values = concat(text(self.options.entity_key), formatted_values)
		
			if not bAggregate and self.options.bPlural and count > 1:
				formatted_values[0] = plural(formatted_values[0])
			
			formatted_values = concat(number_word(formatted_values[-1]), formatted_values[:-1])
		
			if self.options.no_singular_count and not isinstance(values[0], (Deferred, Aggregate)) and count == 1:
				if self.options.no_singular_count(values[0]):
					formatted_values = formatted_values[1:]
			
			if bAggregate and values[0].isTotal():
				if self.options.objective_key:
					return text("TXT_KEY_UHV_TOTAL_OF", text(self.options.objective_key, *formatted_values))
			
				formatted_values = concat(text("TXT_KEY_UHV_TOTAL_OF", *formatted_values[:1]), formatted_values[1:])
		
		if (not isinstance(values[0], Aggregate) or not values[0].isTotal()) and self.options.objective_key:
			return text(self.options.objective_key, *formatted_values)
		
		return " ".join(formatted_values)
	
	def format_resource(self, identifier):
		text = infos.bonus(identifier).getText()
		
		if text.endswith('s'):
			text = text[:-1]
		
		return text
	
	def format_building(self, identifier):
		text = infos.building(identifier).getText()
		
		if text.startswith('The'):
			text = text.replace('The', 'the')
		
		return text
	
	def format_int(self, value):
		value = str(value)
		if self.options.bNumberWord:
			value = number_word(value)
		
		return value
		
	def type_formatter(self, type):
		specific_formatter = self.options.type_formatter(type)
		if specific_formatter:
			return specific_formatter
	
		if issubclass(type, CyCity):
			return lambda city: city and city.getName() or text("TXT_KEY_UHV_NO_CITY")
		if issubclass(type, AttitudeTypes):
			return lambda info: infos.attitude(info).getDescription().lower()
		if issubclass(type, UnitCombatTypes):
			return lambda info: infos.unitCombat(info).getDescription().lower()
		if issubclass(type, CvCultureLevelInfo):
			return lambda info: infos.cultureLevel(info).getText().lower()
		if issubclass(type, CvBuildingInfo):
			return self.format_building
		if issubclass(type, CvBonusInfo):
			return self.format_resource
		if issubclass(type, CvInfoBase):
			return lambda info: infos.text(type, info)
		if issubclass(type, Plots):
			return Plots.name
		if issubclass(type, int):
			return self.format_int
		return lambda item: item
	
	def format_value(self, type, value):
		formatter = self.type_formatter(type)
		
		if isinstance(value, Deferred):
			return str(value)
		if isinstance(value, Aggregate):
			aggregate_formatter = issubclass(type, (Plots, CvFeatureInfo)) and formatter or (lambda item: plural(formatter(item)))
			return value.format(aggregate_formatter)
		
		return formatter(value)
	
	def format_objectives(self, objectives):
		return format_separators(objectives, ",", text("TXT_KEY_AND"), self.format_objective)
	
	def format_subject(self, subject):
		if not self.subject_type:
			return "<no subject type>"
		return self.format_value(self.subject_type, subject)
	
	def format_progress(self, progress_key, *arguments):
		if arguments and self.subject_type:	
			arguments = arguments[1:]
			
		formatted = self.format_values(arguments)
		if progress_key:
			return text(progress_key, *formatted)
			
		if not formatted:
			return ""
		
		progress = formatted[0]
		if progress.lower().startswith('the '):
			progress = progress[4:]
		
		return capitalize(progress)
	
	def format(self, key, arguments, *additional_args):
		return text(key, self.format_objectives(arguments.objectives), self.format_subject(arguments.subject), *additional_args)
	
	def type_values(self, arguments, type):
		values = []
		if self.subject_type and issubclass(self.subject_type, type):
			values.append(arguments.subject)
		
		for objectives in arguments.objectives:
			for objective, objective_type in zip(objectives, self.objective_types):
				if issubclass(objective_type, type):
					if isinstance(objective, Aggregate):
						for item in objective:
							values.append(item.clear_named(objective.name))
					else:
						values.append(objective)
		
		return values


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
	
	def format_options(self, options):
		self.types.withOptions(options)
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


class CheckAt(object):

	def __init__(self, goal, iYear):
		self.goal = goal
		self.iYear = iYear
	
	@property
	def __name__(self):
		return self.__class__.__name__
	
	def __call__(self, args):
		iGameTurn, iPlayer = args
		if self.goal.iPlayer == iPlayer and iGameTurn == year(self.iYear):
			self.goal.finalCheck()


class CheckBy(object):

	def __init__(self, goal, iYear):
		self.goal = goal
		self.iYear = iYear
	
	def __call__(self, args):
		iGameTurn, iPlayer = args
		if self.goal.iPlayer == iPlayer and iGameTurn == year(self.iYear):
			self.goal.expire()
	
	@property
	def __name__(self):
		return self.__class__.__name__


class CheckEvery(object):

	def __init__(self, goal):
		self.goal = goal
	
	def __call__(self, args):
		iGameTurn, iPlayer = args
		if self.goal.iPlayer == iPlayer:
			self.goal.check()
	
	@property
	def __name__(self):
		return self.__class__.__name__


class BaseGoal(object):

	PLAYER, RELIGION, SECULAR, WORLD = range(4)
	ACTIVE, PASSIVE = range(2)

	SUCCESS_CHAR = game.getSymbolID(FontSymbols.SUCCESS_CHAR)
	FAILURE_CHAR = game.getSymbolID(FontSymbols.FAILURE_CHAR)

	#SUCCESS_CHAR = "Y"
	#FAILURE_CHAR = "N"

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
	def format(cls, options):
		cls.builder.format_options(options)
		return cls
	
	@classmethod
	def build_handler(cls, handler, func):
		event = handler.__name__
		handler.__name__ = "%s_%s" % (handler.__name__, func.__name__)
		cls.builder.handler(event, handler)
		return cls
	
	@classproperty
	def turnly(cls):
		def checkGoal(self, *args):
			self.check()
		return cls.handle("BeginPlayerTurn", checkGoal)
	
	@classmethod
	def handle(cls, event, func):
		handler = handlers.ours().get(event, func)
		return cls.build_handler(handler, func)
	
	@classmethod
	def expired(cls, event, func):
		handler = handlers.others().get(event, func)
		return cls.build_handler(handler, func)
	
	@classmethod
	def any(cls, event, func):
		handler = handlers.any().get(event, func)
		return cls.build_handler(handler, func)
	
	@classmethod
	def desc(cls, text):
		return cls.attribute("_desc", "TXT_KEY_UHV_%s" % text)
	
	@classmethod
	def progr(cls, text):
		return cls.attribute("_progr", "TXT_KEY_UHV_PROGRESS_%s" % text)
	
	@classmethod
	def process_arguments(cls, *arguments):
		if not cls.types:
			return Arguments(((),))
		return cls.types.process(*arguments)
	
	@classmethod
	def process_areas(cls, arguments):
		areas = defaultdict(default=plots.none())
		if not cls.types:
			return areas
		
		for item in cls.types.type_values(arguments, (Plots, CyCity)):
			name = item.name()
			area_plots = area(item)
			if name and area_plots:
				areas[simple_name(name)] += area_plots
		
		return areas

	def __init__(self, *arguments):
		self.reset()
		
		self.arguments = self.process_arguments(*arguments)
		self.arguments.owner_included = self.owner_included
			
		self._title = ""
		self._description = hasattr(self, '_desc') and self.types.format(self._desc, self.arguments) or ""
		self._progress = hasattr(self, '_progr') and self._progr or ""
		
		self._description_suffixes = []
		self._iYear = None
		self._iSuccessTurn = None
		
		self.handlers = self.__class__.handlers[:]
		self.extra_handlers = []
		
		self.areas = self.process_areas(self.arguments)
		
		self.type = self.PLAYER
		self.mode = self.ACTIVE
		
		self.init()
		
	def init(self):
		pass
		
	def __nonzero__(self):
		return all(self.condition(*args) for args in self.arguments)
	
	def __str__(self):
		return '\n'.join([self.display(*args) for args in self.arguments])
	
	@property
	def values(self):
		return [segment(objective) for objective in self.arguments.objectives]
	
	@property
	def _player(self):
		return player(self.iPlayer)
	
	@property
	def _team(self):
		return team(self.iPlayer)
		
	def reset(self):
		self.state = POSSIBLE
		
		self.iPlayer = None
		self.callback = None
	
	def activate(self, iPlayer, callback=None):
		self.iPlayer = iPlayer
		self.callback = callback
		
		self.arguments.iPlayer = iPlayer
		
		for event, handler in self.handlers:
			events.addEventHandler(event, getattr(self, handler))
	
	def deactivate(self):
		for event, handler in self.handlers:
			handler_func = getattr(self, handler)
			if events.hasEventHandler(event, handler_func):
				events.removeEventHandler(event, handler_func)
	
	def passivate(self, iPlayer, callback=None):
		self.mode = self.PASSIVE
		self.activate(iPlayer, callback)
	
	# TODO: test
	def state_string(self):
		if self.state == FAILURE:
			return text("TXT_KEY_UHV_GOAL_FAILURE")
	
		if self.mode == self.PASSIVE:
			if self:
				return text("TXT_KEY_UHV_GOAL_SUCCESS")
			return text("TXT_KEY_UHV_GOAL_POSSIBLE")
	
		if self.state == SUCCESS:
			return text("TXT_KEY_UHV_GOAL_SUCCESS")
		return text("TXT_KEY_UHV_GOAL_POSSIBLE")
	
	# TODO: test
	def accomplished_string(self):
		string = text("TXT_KEY_UHV_GOAL_ACCOMPLISHED")
		
		if self._iSuccessTurn is not None:
			if AdvisorOpt.isUHVFinishDateTurn():
				string += " (%s - %s)" % (format_date(game.getTurnYear(self._iSuccessTurn)), text("TXT_KEY_UHV_TURN", self.iSuccessTurn))
			else:
				string += " (%s)" % format_date(game.getTurnYear(self._iSuccessTurn))
		
		return string
	
	# TODO: test record success turn
	# TODO: should announce be part of the callback so only the top level callback announces? as opposed to subgoals of All() etc.
	def setState(self, state):
		if self.state != state and (self.mode == self.ACTIVE or state != SUCCESS):
			self.state = state
			
			if state == FAILURE:
				self.announceFailure()
				self.deactivate()
			
			if state == SUCCESS:
				self.announceSuccess()
				self.recordSuccessTurn()
			
			if self.callback and hasattr(self.callback, 'stateChange'):
				self.callback.stateChange(self)
	
	def possible(self):
		return self.state == POSSIBLE
	
	def succeeded(self):
		return self.state == SUCCESS
	
	def failed(self):
		return self.state == FAILURE
	
	def succeed(self):
		self.setState(SUCCESS)
	
	def fail(self):
		self.setState(FAILURE)
		
	def expire(self):
		if self.callback and hasattr(self.callback, 'expire'):
			self.callback.expire(self)
			return
	
		if self.possible():
			self.fail()
	
	def check(self):
		if self.callback and hasattr(self.callback, 'check'):
			self.callback.check(self)
			return
	
		if self.possible() and self:
			self.succeed()
	
	def finalCheck(self):
		self.check()
		self.expire()
	
	def announceFailure(self):
		self.announce("TXT_KEY_UHV_ANNOUNCE_FAILURE", AlertsOpt.isShowUHVFailPopup())
	
	def announceSuccess(self):
		self.announce("TXT_KEY_UHV_ANNOUNCE_SUCCESS", AlertsOpt.isShowUHVSuccessPopup())
			
	def announce(self, key, condition=True):
		if self.iPlayer is not None and self._player.isHuman() and since(scenarioStartTurn()) > 0 and condition:
			show(key, goal.description())
	
	# TODO: test
	def recordSuccessTurn(self):
		self._iSuccessTurn = turn()
		
	def condition(self, *objectives):
		raise NotImplementedError()
	
	def valid_player(self, iPlayer):
		if self.type == self.PLAYER:
			return self.iPlayer == iPlayer
		elif self.type == self.RELIGION:
			return self._player.getStateReligion() >= 0 and self._player.getStateReligion() == player(iPlayer).getStateReligion()
		elif self.type == self.SECULAR:
			return not self._player.isStateReligion() and not player(iPlayer).isStateReligion()
		elif self.type == self.WORLD:
			return True
		return False
	
	def religion(self):
		self.type = self.RELIGION
		return self
	
	def secular(self):
		self.type = self.SECULAR
		return self
	
	def world(self):
		self.type = self.WORLD
		return self
	
	def named(self, key):
		full_key = "TXT_KEY_UHV_%s" % key
		self._description = self.types and self.types.format(full_key, self.arguments) or text(full_key)
		return self
		
	@property
	def turn_suffix(self):
		if self.iPlayer is not None and self._iYear is not None:
			if not team(self.iPlayer).isHasTech(iCalendar) or AdvisorOpt.isUHVFinishDateTurn():
				return text("TXT_KEY_UHV_TURN_SUFFIX", year(self._iYear))
	
	def description(self):
		return capitalize(" ".join(concat(self._description, self._description_suffixes, self.turn_suffix)))
	
	def titled(self, key):
		title = text_if_exists("TXT_KEY_UHV_TITLE_%s" % key)
		if title:
			self._title = title
		return self
	
	def title(self):
		return self._title
	
	def full_description(self):
		if self.title():
			return "%s: %s" % (self.title(), self.description())
		return self.description()
		
	# TODO: test accomplished string
	def progress(self, bForceSingle = False):
		if self.succeeded():
			return [self.accomplished_string()]
	
		if len(self.arguments.objectives) == 1 and not bForceSingle and not self.single_objective_progress():
			return []
	
		objective_progress = [self.objective_progress(*arguments) for arguments in self.arguments]
		return [progress for progress in objective_progress if progress]
	
	def single_objective_progress(self):
		return 'by' not in self.extra_handlers
	
	def objective_progress(self, *arguments):
		indicator = self.progress_indicator(*arguments)
		text = self.progress_text(*arguments)
		
		if not text:
			return ""
		
		return "%s %s" % (indicator, text)
	
	def progress_indicator_value(self, *arguments):
		return self.condition(*arguments)
	
	def progress_indicator(self, *arguments):
		return self.format_progress_indicator(self.progress_indicator_value(*arguments))
	
	def format_progress_indicator(self, value):
		return u"%c" % (value and self.SUCCESS_CHAR or self.FAILURE_CHAR,)
	
	def progress_text(self, *arguments):
		return self.types.format_progress(self._progress, *arguments)
	
	def full_display(self):
		return "%s\n%s" % (self.full_description(), "\n".join(self.progress()))
	
	def display(self):
		raise NotImplementedError()
	
	def area_name(self, tile):
		return "\n".join([name for name, area in self.areas.items() if tile in area])
		
	def register(self, event, handler):
		setattr(self, handler.__name__, handler)
		self.handlers.append((event, handler.__name__))
	
	def at(self, iYear):
		self.extra_handlers.append('at')
		
		self.register("BeginPlayerTurn", CheckAt(self, iYear))
		self._description_suffixes.append(text("TXT_KEY_UHV_IN", format_date(iYear)))
		self._iYear = iYear
		
		if self._description.lower().startswith(text("TXT_KEY_UHV_BUILD")):
			self._description = replace_first(self._description, "TXT_KEY_UHV_HAVE")
		
		return self
	
	def by(self, iYear):
		self.extra_handlers.append('by')
		
		self.register("BeginPlayerTurn", CheckBy(self, iYear))
		self._description_suffixes.append(text("TXT_KEY_UHV_BY", format_date(iYear)))
		self._iYear = iYear
		return self
	
	def every(self):
		self.extra_handlers.append('every')
		
		self.register("BeginPlayerTurn", CheckEvery(self))
		return self


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
			return city and func(city, objective) or False
		
		return cls.func(condition)

	@classproperty
	def wonder(cls):
		def checkExpiration(self, city, iWonder):
			if iWonder in self.values:
				self.expire()
		
		def checkWonderBuilt(self, city, iWonder):
			if iWonder in self.values:
				self.check()
	
		return cls.desc("WONDER").objective(CvBuildingInfo).player(CyPlayer.isHasBuilding).expired("buildingBuilt", checkExpiration).handle("buildingBuilt", checkWonderBuilt).subclass("Wonder")
	
	@classproperty
	def control(cls):
		def controlled(self, city):
			return city.getOwner() == self.iPlayer
	
		return cls.desc("CONTROL").objective(Plots).cities(controlled).subclass("Control")
	
	@classproperty
	def controlOrVassalize(cls):
		def controlled_or_vassalized(self, city):
			return city.getOwner() in players.vassals(self.iPlayer).including(self.iPlayer)
		
		return cls.desc("CONTROL_OR_VASSALIZE").objective(Plots).cities(controlled_or_vassalized).subclass("ControlOrVassalize")
	
	@classproperty
	def settle(cls):
		def settled(self, city):
			return city.getOwner() == self.iPlayer and city.getOriginalOwner() == self.iPlayer
		
		def checkCityBuilt(self, city):
			if any(city in area for area in self.values):
				self.check()
		
		return cls.desc("SETTLE").objective(Plots).cities(settled).handle("cityBuilt", checkCityBuilt).subclass("Settle")
	
	@classproperty
	def project(cls):
		def checkProjectBuilt(self, iProject):
			if iProject in self.values:
				self.check()
		
		def expireProjectBuilt(self, iProject):
			if iProject in self.values:
				self.expire()
	
		return cls.desc("PROJECT_COUNT").objective(CvProjectInfo).team(positive(CyTeam.getProjectCount)).handle("projectBuilt", checkProjectBuilt).expired("projectBuilt", expireProjectBuilt).subclass("Project")
	
	@classproperty
	def route(cls):
		def progress_text(self, area, iRoute):
			return text(self._progress, area.name(), infos.route(iRoute).getText())
	
		return cls.desc("ROUTE").progr("ROUTE").subject(Plots).objective(CvRouteInfo).plots(equals(CyPlot.getRouteType)).func(progress_text).turnly.subclass("Route")
		
	@classproperty
	def areaNoStateReligion(cls):
		def no_state_religion(self, city, iReligion):
			return player(city).getStateReligion() != iReligion
		
		def format_religion(identifier):
			return text(infos.religion(identifier).getAdjectiveKey())
		
		def progress_text(self, area, iReligion):
			return text("TXT_KEY_UHV_PROGRESS_AREA_NO_STATE_RELIGION", area.name(), format_religion(iReligion))
	
		return cls.desc("AREA_NO_STATE_RELIGION").format(options.type(CvReligionInfo, format_religion)).subject(Plots).objective(CvReligionInfo).cities(no_state_religion).func(progress_text).subclass("AreaNoStateReligion")
	
	@classproperty
	def cultureCovered(cls):
		def covered(plot, iPlayer):
			return plot.getOwner() == iPlayer
		
		return cls.desc("CULTURE_COVERED").objective(Plots).include_owner.plots(covered).turnly.subclass("CultureCovered")
	
	@classproperty
	def communist(cls):
		def condition(self, *objectives):
			return isCommunist(self.iPlayer)
		
		return cls.desc("COMMUNIST").progr("COMMUNIST").func(condition).subclass("Communist")
	
	@classproperty
	def noForeignCities(cls):
		def init(self):
			self.lOnly = []
			self.lExcluded = []
		
		def only(self, lCivs):
			self.lOnly = lCivs
			return self
		
		def excluding(self, lCivs):
			self.lExcluded = lCivs
			return self
		
		def valid(self, city):
			if city.getOwner() == self.iPlayer:
				return True
			if self.lOnly and civ(city) not in self.lOnly:
				return True
			if self.lExcluded and civ(city) in self.lExcluded:
				return True
			if is_minor(city):
				return True
			return False
		
		return cls.desc("NO_FOREIGN_CITIES").progr("NO_FOREIGN_CITIES").objective(Plots).func(init, only, excluding).cities(valid).subclass("NoForeignCities")
	
	@classproperty
	def tradeConnection(cls):
		def condition(self):
			return players.major().alive().without(self.iPlayer).any(lambda p: self._player.canContact(p) and self._player.canTradeNetworkWith(p))
		
		return cls.desc("TRADE_CONNECTION").func(condition).turnly.subclass("TradeConnection")
	
	@classproperty
	def moreReligion(cls):
		def religionCities(self, plots, iReligion):
			return plots.cities().religion(iReligion).count()
		
		def condition(self, plots, iOurReligion, iOtherReligion):
			return self.religionCities(plots, iOurReligion) > self.religionCities(plots, iOtherReligion)
		
		def display(self, plots, iOurReligion, iOtherReligion):
			return "%d / %d" % (self.religionCities(plots, iOurReligion), self.religionCities(plots, iOtherReligion))
		
		def format_religion(identifier):
			return text(infos.religion(identifier).getAdjectiveKey())
		
		def progress_text(self, area, iOurReligion, iOtherReligion):
			return "%s: %d %s: %d" % (text("TXT_KEY_UHV_PROGRESS_CITIES", format_religion(iOurReligion)), self.religionCities(area, iOurReligion), text("TXT_KEY_UHV_PROGRESS_CITIES", format_religion(iOtherReligion)), self.religionCities(area, iOtherReligion))
		
		return cls.desc("MORE_RELIGION").format(options.objective("MORE_THAN").type(CvReligionInfo, format_religion)).subject(Plots).objectives(CvReligionInfo, CvReligionInfo).func(religionCities, condition, display, progress_text).subclass("MoreReligion")
	
	@classproperty
	def moreCulture(cls):
		def init(self):
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
		
		def progress(self):
			return [text(self._progress, self.value(), self.required())]
		
		return cls.progr("MORE_CULTURE").func(init, than, condition, display, value, required, progress).subclass("MoreCulture")
	
	@classproperty
	def allAttitude(cls):
		def condition(self, iAttitude):
			return self.value(iAttitude) >= self.required()
		
		def display(self, iAttitude):
			return "%d / %d" % (self.value(iAttitude), self.required())
	
		def value(self, iAttitude):
			return players.major().alive().without(self.iPlayer).where(lambda p: player(p).AI_getAttitude(self.iPlayer) >= iAttitude).count()
		
		def required(self):
			return players.major().alive().without(self.iPlayer).count()
		
		def progress_text(self, iAttitude):
			return text(self._progress, infos.attitude(iAttitude).getText(), self.value(iAttitude), self.required())
		
		return cls.desc("ALL_ATTITUDE").progr("ALL_ATTITUDE").objective(AttitudeTypes).func(condition, display, value, required, progress_text).subclass("AllAttitude")
	
	@classproperty
	def noStateReligion(cls):
		def condition(self, iReligion):
			return self.value(iReligion) == 0
		
		def display(self, iReligion):
			return str(self.value(iReligion))
		
		def value(self, iReligion):
			return players.major().alive().religion(iReligion).count()
		
		def progress_text(self, iReligion):
			return text(self._progress, text(infos.religion(iReligion).getAdjectiveKey()), self.value(iReligion))
		
		def format_religion(identifier):
			return text(infos.religion(identifier).getAdjectiveKey())
		
		return cls.desc("NO_STATE_RELIGION").progr("NO_STATE_RELIGION").format(options.type(CvReligionInfo, format_religion)).objective(CvReligionInfo).func(condition, display, value, progress_text).subclass("NoStateReligion")
	
	@classproperty
	def stateReligionPercent(cls):
		def init(self):
			self.bSecular = False
		
		def orSecular(self):
			self.bSecular = True
			return self
	
		def condition(self, iReligion, iPercent):
			return self.value(iReligion) >= self.required(iPercent)
		
		def display(self, iReligion, iPercent):
			return "%d / %d" % (self.value(iReligion), self.required(iPercent))
		
		def value(self, iReligion):
			iCount = players.major().alive().religion(iReligion).count()
			
			if self.bSecular:
				iCount += players.major().alive().where(lambda p: not player(p).isStateReligion()).count()
			
			return iCount
		
		def required(self, iPercent):
			return players.major().alive().count() * iPercent / 100
		
		def progress_text(self, iReligion, iPercent):
			key = self._progress
			if self.bSecular:
				key += "_OR_SECULAR"
			return text(key, text(infos.religion(iReligion).getAdjectiveKey()), self.value(iReligion), self.required(iPercent))
		
		return cls.desc("STATE_RELIGION_PERCENT").progr("STATE_RELIGION_PERCENT").objectives(CvReligionInfo, int).func(init, orSecular, condition, display, value, required, progress_text).subclass("StateReligionPercent")
	
	@classproperty
	def noReligionPercent(cls):
		def condition(self, iPercent):
			return self.value() <= self.required(iPercent)
			
		def display(self, iPercent):
			return "%d / %d" % (self.value(), self.count())
		
		def value(self):
			return cities.owner(self.iPlayer).where(lambda city: city.getReligionCount() > 0).count()
		
		def required(self, iPercent):
			return self.count() * iPercent / 100
			
		def count(self):
			return cities.owner(self.iPlayer).count()
		
		def progress_text(self, iPercent):
			return text(self._progress, self.value(), self.count())
		
		return cls.progr("NO_RELIGION_PERCENT").objectives(int).func(condition, display, value, required, count, progress_text).subclass("NoReligionPercent")
	
	@classproperty
	def goldPercent(cls):
		def condition(self, iPercent):
			return self.value() >= self.required(iPercent)
		
		def display(self, iPercent):
			return "%d / %d" % (self.value(), self.sum())
		
		def value(self):
			return self._player.getGold()
			
		def sum(self):
			return players.major().alive().without(self.iPlayer).sum(lambda p: player(p).getGold())
		
		def required(self, iPercent):
			return self.sum() * iPercent / 100
		
		def progress_text(self, iPercent):
			return text(self._progress, self.value(), self.sum())
		
		return cls.progr("GOLD_PERCENT").objectives(int).func(condition, display, value, sum, required, progress_text).subclass("GoldPercent")
	

class Count(BaseGoal):

	@classmethod
	def objectives(cls, *types):
		types = list(types) + [int]
		return cls.plain_objectives(*types)
	
	@classmethod
	def plain_objectives(cls, *types):
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
	
	def value(self, *arguments):
		if any(argument is None for argument in arguments):
			return 0
			
		aggregate, remainder = self.aggregate(*arguments)
		if aggregate:
			return aggregate.eval(self.value_function, *remainder)
		
		return self.value_function(*arguments)
		
	def aggregate(self, *arguments):
		arglist = list(arguments)
		aggregate = next(item for item in arglist if isinstance(item, Aggregate))
		
		if aggregate is None:
			return None, None
			
		arglist.remove(aggregate)
		return aggregate, arglist
		
	def value_function(self, objective):
		raise NotImplementedError()
		
	def display(self, *arguments):
		remainder, iRequired = arguments[:-1], arguments[-1]
		return "%d / %d" % (self.value(*remainder), self.required(iRequired))
	
	def progress_text(self, *arguments):
		remainder, iRequired = arguments[:-1], arguments[-1]
		progress_text = self.progress_text_format(remainder, iRequired)
		progress_value = self.progress_value(self.value(*remainder), self.required(iRequired))
		
		if iRequired == 1:
			return progress_text
		
		return "%s: %s" % (progress_text, progress_value)
	
	def progress_text_format(self, remainder, iRequired):
		text = self.types.format_progress(self._progress, *remainder)
		
		if iRequired > 1 and not self._progress and len(self.types.objective_types) > 1 and none(isinstance(entry, Aggregate) for entry in remainder) and self.types.objective_types[0] != Plots:
			text = plural(text)
		
		return text
	
	def progress_value(self, value, required):
		return "%d / %d" % (value, required)
	
	def single_objective_progress(self):
		return True
	
	@property
	def values(self):
		return [segment(objective[:-1]) for objective in self.arguments.objectives]
	
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
			return cities.all().where(lambda city: self.valid_player(city.getOwner())).sum(lambda city: func(city, *objectives))
		
		return cls.func(value_function)
	
	@classmethod
	def citiesWith(cls, func):
		def value_function(self, iThreshold):
			def function(city):
				return func(city) >= iThreshold
		
			return cities.owner(self.iPlayer).count(function)
		
		def display_city_value(self, city):
			return func(city)
			
		def display_required(self, iRequired):
			return iRequired
		
		def objective_progress(self, iThreshold, iRequiredCities):
			highest_cities = cities.owner(self.iPlayer).highest(iRequiredCities, func)
			
			if not highest_cities:
				return [u"%c %s" % (self.FAILURE_CHAR, text("TXT_KEY_UHV_PROGRESS_NO_CITIES"))]
			
			rows = []
			for city in highest_cities:
				rows.append("%s %s: %d / %d" % (self.format_progress_indicator(func(city) >= iThreshold), city.getName(), self.display_city_value(city), self.display_required(self.required(iThreshold))))
			
			for index in range(iRequiredCities):
				if index < highest_cities.count():
					continue
				rows.append(u"%c %s" % (self.FAILURE_CHAR, text("TXT_KEY_UHV_PROGRESS_MISSING_CITY", ordinal_word(index+1))))
			
			return rows
		
		def progress(self, bForceSingle=False):
			return list(flatten(super(cls, self).progress(bForceSingle)))
		
		return cls.func(value_function, display_city_value, display_required, objective_progress, progress)
	
	@classmethod
	def city(cls, func):
		def value_function(self, city, *objectives):
			if not city or city.getOwner() != self.iPlayer:
				return 0
			
			return func(city, *objectives)
		
		def display_required(self, iRequired):
			return iRequired
		
		def display_city_value(self, city, *remainder):
			return self.value(city, *remainder)
		
		def progress_text(self, city, *objectives):
			if not city:
				return text("TXT_KEY_UHV_NO_CITY")
		
			remainder, iRequired = objectives[:-1], objectives[-1]
			progress_text = self.progress_text_format(concat(city, remainder), iRequired)
			
			if city.getOwner() == self.iPlayer:
				city_name = city.getName()
			else:
				city_name = text("TXT_KEY_UHV_CITY_DIFFERENT_OWNER", city.getName(), name(city.getOwner()))
			
			progress_text = text("TXT_KEY_UHV_PROGRESS_IN_CITY", progress_text, city_name)
			progress_value = self.progress_value(self.display_city_value(city, *remainder), self.display_required(self.required(iRequired)))
			
			if iRequired == 1:
				return progress_text
			
			return "%s: %s" % (progress_text, progress_value)
		
		return cls.func(value_function, display_city_value, display_required, progress_text)
		
	@classproperty
	def scaled(cls):
		def required_function(self, objective):
			return scale(objective)
			
		return cls.func(required_function)
	
	@classproperty
	def building(cls):
		def base(self, building):
			if isinstance(building, Aggregate):
				building.items = [base_building(item) for item in building]
				return building
			return base_building(building)
	
		def checkBuildingBuilt(self, city, iBuilding):
			if base_building(iBuilding) in [self.base(iBuilding) for iBuilding in self.values]:
				self.check()
		
		def checkCityAcquired(self, *args):
			self.check()
			
		def player_buildings(self, iPlayer, iBuilding):
			return player(iPlayer).countNumBuildings(unique_building(iPlayer, iBuilding))
		
		def value_function(self, iBuilding):
			return players.major().alive().where(self.valid_player).sum(lambda p: self.player_buildings(p, iBuilding))
		
		def world(self):
			self._description = self.types.format("TXT_KEY_UHV_BUILDING_COUNT_WORLD", self.arguments)
			return super(type(self), self).world()
		
		def secular(self):
			self._description = self.types.format("TXT_KEY_UHV_BUILDING_COUNT_SECULAR", self.arguments)
			return super(type(self), self).secular()
	
		return cls.desc("BUILDING_COUNT").format(options.noSingularCount(isWonder)).objective(CvBuildingInfo).func(value_function, base, player_buildings, world, secular).handle("buildingBuilt", checkBuildingBuilt).handle("cityAcquired", checkCityAcquired).subclass("BuildingCount")
	
	@classproperty
	def culture(cls):
		return cls.desc("PLAYER_CULTURE").progr("PLAYER_CULTURE").player(CyPlayer.countTotalCulture).scaled.turnly.subclass("PlayerCulture")
	
	@classproperty
	def gold(cls):
		return cls.desc("PLAYER_GOLD").progr("GOLD").player(CyPlayer.getGold).scaled.subclass("PlayerGold")
	
	@classproperty
	def resource(cls):
		return cls.desc("RESOURCE_COUNT").progr("RESOURCE_COUNT").format(options.singular()).objective(CvBonusInfo).player(CyPlayer.getNumAvailableBonuses).turnly.subclass("ResourceCount")
	
	@classproperty
	def controlledResource(cls):
		def resources(player, objective):
			return player.getNumAvailableBonuses(objective) - player.getBonusImport(objective)
		
		def format_bonus(identifier):
			return text("TXT_KEY_UHV_RESOURCE", infos.bonus(identifier).getText())
	
		return cls.desc("CONTROLLED_RESOURCE_COUNT").format(options.type(CvBonusInfo, format_bonus)).objective(CvBonusInfo).playervassals(resources).subclass("ControlledResourceCount")
		
	@classproperty
	def improvement(cls):
		return cls.desc("IMPROVEMENT_COUNT").objective(CvImprovementInfo).player(CyPlayer.getImprovementCount).subclass("ImprovementCount")
	
	@classproperty
	def population(cls):
		return cls.desc("PLAYER_POPULATION").progr("POPULATION").player(CyPlayer.getTotalPopulation).turnly.subclass("PlayerPopulation")
	
	@classproperty
	def corporation(cls):
		def checkCorporationSpread(self, iCorporation):
			if iCorporation in self.values:
				self.check()
	
		return cls.desc("CORPORATION_COUNT").format(options.objective("TO_YOUR_ENTITY").city()).objective(CvCorporationInfo).player(CyPlayer.countCorporations).handle("corporationSpread", checkCorporationSpread).subclass("CorporationCount")
	
	@classproperty
	def unit(cls):
		def value_function(self, iUnit):
			return self._player.getUnitClassCount(infos.unit(iUnit).getUnitClassType())
		
		return cls.desc("UNIT_COUNT").objective(CvUnitInfo).func(value_function).turnly.subclass("UnitCount")
	
	@classproperty
	def unitCombat(cls):
		def value_function(self, iUnitCombat):
			return units.owner(self.iPlayer).combat(iUnitCombat).where(lambda unit: self._player.canTrain(unit.getUnitType(), False, False)).count()
		
		return cls.desc("UNIT_COMBAT_COUNT").objective(UnitCombatTypes).func(value_function).turnly.subclass("UnitCombatCount")
	
	@classproperty
	def unitLevel(cls):
		def value_function(self, iUnitLevel):
			return units.owner(self.iPlayer).where(lambda unit: unit.getLevel() >= iUnitLevel).count()
		
		return cls.desc("UNIT_LEVEL_COUNT").format(options.objective("UNITS_OF_LEVEL").number_word().singular()).progr("UNIT_LEVEL_COUNT").objective(int).func(value_function).turnly.subclass("UnitLevelCount")
	
	@classproperty
	def numCities(cls):
		def owned(self, cities):
			return cities.owner(self.iPlayer)
	
		return cls.desc("CITY_COUNT").progr("CITY_COUNT").format(options.city().objective("ENTITY_IN")).cities(owned).subclass("CityCount")
	
	@classproperty
	def settledCities(cls):
		def settled(self, cities):
			return cities.owner(self.iPlayer).where(lambda city: city.getOriginalOwner() == self.iPlayer)
		
		return cls.desc("SETTLED_CITY_COUNT").progr("SETTLED_CITY_COUNT").format(options.city().objective("ENTITY_IN")).cities(settled).subclass("SettledCityCount")
	
	@classproperty
	def conqueredCities(cls):
		def init(self):
			self.conquered = plots.none()
			self.lCivs = []
			self.inside_plots = plots.none()
			self.outside_plots = plots.none()
		
		def civs(self, lCivs):
			self.lCivs = lCivs
			return self
		
		def inside(self, area):
			self.inside_plots = area
			self._description_suffixes.append(text("TXT_KEY_UHV_IN", self.inside_plots.name()))
			
			if area.name():
				self.areas[simple_name(area.name())] = area
			
			return self
		
		def outside(self, area):
			self.outside_plots = area
			
			if area.name():
				self.areas[simple_name(area.name())] = plots.all().without(area).land()
			
			return self
		
		def onCityAcquired(self, iOwner, city, bConquest):
			if bConquest and (not self.lCivs or civ(iOwner) in self.lCivs) and (not self.inside_plots or city in self.inside_plots) and (not self.outside_plots or city not in self.outside_plots):
				self.conquered = self.conquered.including(city)
		
		def value_function(self):
			return cities.owner(self.iPlayer).where(lambda city: city in self.conquered).count()
		
		def progress_text_format(self, remainder, iRequired):
			progress_text = text(self._progr)
			if self.inside_plots:
				progress_text = text("TXT_KEY_UHV_PROGRESS_IN_AREA", progress_text, self.inside_plots.name())
			return progress_text
		
		return cls.desc("CONQUERED_CITY_COUNT").progr("CONQUERED_CITY_COUNT").format(options.city()).func(init, civs, inside, outside, value_function, progress_text_format).handle("cityAcquired", onCityAcquired).subclass("ConqueredCityCount")
	
	@classproperty
	def openBorders(cls):
		def init(self):
			self.lCivs = []
			
		def civs(self, lCivs):
			self.lCivs = lCivs
			return self
	
		def valid(self, iPlayer):
			if self.lCivs and civ(iPlayer) not in self.lCivs:
				return False
		
			return self._team.isOpenBorders(player(iPlayer).getTeam())
		
		return cls.desc("OPEN_BORDER_COUNT").progr("OPEN_BORDER_COUNT").format(options.number_word()).func(init, civs).players(valid).subclass("OpenBorderCount")
	
	@classproperty
	def specialist(cls):
		def religion(self, iReligion=None):
			if iReligion is not None:
				self._description = self.types.format("TXT_KEY_UHV_SPECIALIST_COUNT_RELIGION", self.arguments, text(infos.religion(iReligion).getAdjectiveKey()))
			return super(type(self), self).religion()
		
		def secular(self):
			self._description = self.types.format("TXT_KEY_UHV_SPECIALIST_COUNT_SECULAR", self.arguments)
			return super(type(self), self).secular()
	
		return cls.desc("SPECIALIST_COUNT").objective(CvSpecialistInfo).citiesSum(CyCity.getFreeSpecialistCount).func(religion, secular).turnly.subclass("SpecialistCount")
	
	@classproperty
	def averageCulture(cls):
		return cls.desc("AVERAGE_CULTURE").progr("AVERAGE_CULTURE").player(average(CyPlayer.countTotalCulture, CyPlayer.getNumCities)).turnly.subclass("AverageCulture")
	
	@classproperty
	def averagePopulation(cls):
		return cls.desc("AVERAGE_POPULATION").progr("AVERAGE_POPULATION").player(average(CyPlayer.getTotalPopulation, CyPlayer.getNumCities)).subclass("AveragePopulation")
		
	@classproperty
	def populationCities(cls):
		return cls.desc("POPULATION_CITIES").format(options.objective("ENTITY_OF_SIZE").city().number_word()).objective(int).citiesWith(CyCity.getPopulation).turnly.subclass("PopulationCities")
	
	@classproperty
	def cultureCities(cls):
		return cls.desc("CULTURE_CITIES").format(options.objective("ENTITY_WITH").city()).objective(int).citiesWith(lambda city: city.getCulture(city.getOwner())).subclass("CultureCities")
	
	@classproperty
	def cultureLevelCities(cls):
		def display_required(self, iRequired):
			return game.getCultureThreshold(iRequired)
		
		def display_city_value(self, city):
			return city.getCulture(city.getOwner())
	
		return cls.desc("CULTURE_LEVEL_CITIES").format(options.objective("ENTITY_WITH").city()).objective(CvCultureLevelInfo).citiesWith(CyCity.getCultureLevel).func(display_city_value, display_required).subclass("CultureLevelCities")
	
	@classproperty
	def citySpecialist(cls):
		return cls.desc("CITY_SPECIALIST_COUNT").subject(CyCity).objective(CvSpecialistInfo).city(CyCity.getFreeSpecialistCount).turnly.subclass("CitySpecialistCount")
	
	@classproperty
	def cultureLevel(cls):
		def display(self, city, iCultureLevel):
			return "%d / %d" % (city and city.getCulture(city.getOwner()) or 0, game.getCultureThreshold(iCultureLevel))
	
		def display_required(self, iRequired):
			return game.getCultureThreshold(iRequired)
		
		def display_city_value(self, city):
			return city.getCulture(city.getOwner())
	
		return cls.desc("CULTURE_LEVEL").progr("CULTURE_LEVEL").plain_objectives(CvCultureLevelInfo).subject(CyCity).city(CyCity.getCultureLevel).func(display, display_required, display_city_value).turnly.subclass("CultureLevel")
	
	@classproperty
	def attitude(cls):
		def init(self):
			self.lCivs = []
			self.iStateReligion = -1
			self.iMinorityReligion = -1
			self.bCommunist = False
			self.bIndependent = False
		
		def civs(self, lCivs):
			self.lCivs = lCivs
			return self
		
		def religion(self, iStateReligion):
			self.iStateReligion = iStateReligion
			return self
		
		def minority(self, iMinorityReligion):
			self.iMinorityReligion = iMinorityReligion
			return self
		
		def communist(self):
			self.bCommunist = True
			return self
		
		def independent(self):
			self.bIndependent = True
			return self
		
		def valid(self, iPlayer, iAttitude):
			if not self._player.canContact(iPlayer):
				return False
			if self.bIndependent and team(iPlayer).isAVassal():
				return False
			if self.lCivs and civ(iPlayer) not in self.lCivs:
				return False
			if self.iStateReligion >= 0 and player(iPlayer).getStateReligion() != self.iStateReligion:
				return False
			if self.iMinorityReligion >= 0 and not cities.owner(iPlayer).religion(self.iMinorityReligion):
				return False
			if self.bCommunist and not isCommunist(iPlayer):
				return False
			
			return player(iPlayer).AI_getAttitude(self.iPlayer) >= iAttitude
		
		def progress_text_format(self, remainder, iRequired):
			base_text = text(self._progress, infos.attitude(remainder[0]).getDescription())
			civs_text = text("TXT_KEY_UHV_PROGRESS_ATTITUDE_CIVS")
			
			if self.iMinorityReligion >= 0:
				civs_text = text("TXT_KEY_UHV_PROGRESS_ATTITUDE_WITH_MINORITY", civs_text, text(infos.religion(self.iMinorityReligion).getAdjectiveKey()))
			if self.lCivs:
				civs_text = text("TXT_KEY_UHV_PROGRESS_ATTITUDE_IN_AREA", civs_text, str(self.lCivs))
			if self.bCommunist:
				civs_text = text("TXT_KEY_UHV_PROGRESS_ATTITUDE_COMMUNIST", civs_text)
			if self.iStateReligion >= 0:
				civs_text = text("TXT_KEY_UHV_PROGRESS_ATTITUDE_WITH_RELIGION", text(infos.religion(self.iStateReligion).getAdjectiveKey()), civs_text)
			if self.bIndependent:
				civs_text = text("TXT_KEY_UHV_PROGRESS_ATTITUDE_INDEPENDENT", civs_text)
			
			if civs_text != text("TXT_KEY_UHV_PROGRESS_ATTITUDE_CIVS"):
				return text("TXT_KEY_UHV_PROGRESS_ATTITUDE_WITH", base_text, civs_text)
			return base_text
		
		return cls.progr("ATTITUDE_COUNT").subject(AttitudeTypes).format(options.singular().number_word()).func(init, civs, religion, minority, communist, independent, progress_text_format).players(valid).turnly.subclass("AttitudeCount")
	
	@classproperty
	def vassals(cls):
		def init(self):
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
			if self.iStateReligion >= 0 and player(iPlayer).getStateReligion() != self.iStateReligion:
				return False
			
			return team(iPlayer).isVassal(self._team.getID())
		
		def onVassalState(self):
			self.check()
		
		def progress_text_format(self, remainder, iRequired):
			progress_text = text(self._progress, *remainder)
			
			if self.lCivs:
				progress_text = text("TXT_KEY_UHV_PROGRESS_VASSAL_IN_AREA", progress_text, str(self.lCivs))
			
			if self.iStateReligion >= 0:
				progress_text = text("TXT_KEY_UHV_PROGRESS_VASSAL_WITH_RELIGION", text(infos.religion(self.iStateReligion).getAdjectiveKey()), progress_text)
			
			return capitalize(progress_text)
		
		return cls.progr("VASSAL_COUNT").format(options.number_word()).func(init, civs, religion, progress_text_format).players(valid).handle("vassalState", onVassalState).subclass("VassalCount")
	
	@classproperty
	def cityBuilding(cls):
		def checkBuildingBuilt(self, city, iBuilding):
			if at(city, self.arguments.subject()) and iBuilding in self.values:
				self.check()
	
		return cls.desc("CITY_BUILDING").format(options.noSingularCount(isWonder)).subject(CyCity).objective(CvBuildingInfo).city(CyCity.getNumBuilding).handle("buildingBuilt", checkBuildingBuilt).subclass("CityBuilding")

	@classproperty
	def differentSpecialist(cls):
		def different_specialist(city):
			return count(1 for iSpecialist in lGreatPeople if city.getFreeSpecialistCount(iSpecialist) > 0)
	
		return cls.desc("DIFFERENT_SPECIALIST").format(options.number_word()).progr("DIFFERENT_SPECIALIST").subject(CyCity).city(different_specialist).subclass("DifferentSpecialist")

	@classproperty
	def shrineIncome(cls):
		def value_function(self, iReligion):
			return cities.owner(self.iPlayer).sum(lambda city: city.getBuildingCommerceByBuilding(CommerceTypes.COMMERCE_GOLD, shrine(iReligion)))
		
		def format_shrine(iReligion):
			return text("TXT_KEY_UHV_RELIGION_SHRINE", text(infos.religion(iReligion).getAdjectiveKey()))
		
		return cls.desc("SHRINE_INCOME").format(options.type(CvReligionInfo, format_shrine).objective("GOLD_FROM")).progr("SHRINE_INCOME").objective(CvReligionInfo).func(value_function).subclass("ShrineIncome")
	
	@classproperty
	def terrain(cls):
		def value_function(self, iTerrain):
			return plots.owner(self.iPlayer).where(lambda plot: plot.getTerrainType() == iTerrain).count()
		
		return cls.desc("TERRAIN_COUNT").format(options.objective("TILES").singular()).progr("TERRAIN_COUNT").objective(CvTerrainInfo).func(value_function).subclass("TerrainCount")
	
	@classproperty
	def peaks(cls):
		def value_function(self):
			return plots.owner(self.iPlayer).where(lambda plot: plot.isPeak()).count()
		
		return cls.desc("PEAK_COUNT").progr("PEAK_COUNT").func(value_function).subclass("PeakCount")
	
	@classproperty
	def feature(cls):
		def value_function(self, iFeature):
			return plots.owner(self.iPlayer).where(lambda plot: plot.getFeatureType() == iFeature).count()
		
		return cls.desc("FEATURE_COUNT").format(options.objective("TILES").singular()).progr("FEATURE_COUNT").objective(CvFeatureInfo).func(value_function).subclass("FeatureCount")


class Percentage(Count):

	SELF, VASSALS, ALLIES, RELIGION = range(4)
	
	default_included = SELF

	def __init__(self, *arguments):
		super(Percentage, self).__init__(*arguments)
		
		self.included = self.default_included

	def condition(self, *arguments):
		remainder, iRequired = arguments[:-1], arguments[-1]
		return self.value(*remainder) >= self.required(iRequired) * 1.0 - 0.005
		
	def display(self, *arguments):
		remainder, iRequired = arguments[:-1], arguments[-1]
		return "%.2f%% / %d%%" % (self.value(*remainder), self.required(iRequired))
	
	def progress_value(self, value, required):
		return "%.2f%% / %d%%" % (value, required)
	
	def value(self, *objectives):
		iTotal = self.total(*objectives)
		if iTotal <= 0:
			return 0.0
		return 100.0 * self.player_value(*objectives) / iTotal
	
	@property
	def valid_players(self):
		if self.included == self.SELF:
			return players.of(self.iPlayer)
		elif self.included == self.VASSALS:
			return players.vassals(self.iPlayer).including(self.iPlayer)
		elif self.included == self.ALLIES:
			return players.allies(self.iPlayer)
		elif self.included == self.RELIGION:
			return players.all().religion(self._player.getStateReligion())
		
		raise Exception("self.included set to invalid value")
		
	def player_value(self, *objectives):
		return self.valid_players.sum(lambda p: self.value_function(p, *objectives))
	
	def total(self, *objectives):
		return players.major().alive().sum(lambda p: self.value_function(p, *objectives))
	
	def includeVassals(self):
		self._description = replace_first(self._description, "TXT_KEY_UHV_OR_VASSALISE")
		self.included = self.VASSALS
		return self
	
	def religion(self):
		self.included = self.RELIGION
		return self
	
	@classproperty
	def allied(cls):
		cls.default_included = cls.ALLIES
		return cls
		
	@classproperty
	def areaControl(cls):
		def value_function(self, iPlayer, area):
			return area.land().owner(iPlayer).count()
		
		def total(self, area):
			return area.land().count()
		
		return cls.desc("AREA_PERCENT").progr("AREA_PERCENT").format(options.objective("PERCENT_OF").singular()).objective(Plots).func(value_function, total).subclass("AreaPercent")
	
	@classproperty
	def worldControl(cls):
		def value_function(self, iPlayer):
			return player(iPlayer).getTotalLand()
		
		def total(self):
			return map.getLandPlots()
		
		def religion(self, iReligion=None):
			if iReligion is not None:
				self._description = self.types.format("TXT_KEY_UHV_WORLD_PERCENT_RELIGION", self.arguments, text(infos.religion(iReligion).getAdjectiveKey()))
			return super(type(self), self).religion()
		
		return cls.desc("WORLD_PERCENT").progr("WORLD_PERCENT").func(value_function, total, religion).turnly.subclass("WorldPercent")
	
	@classproperty
	def religionSpread(cls):
		def value(self, iReligion):
			return game.calculateReligionPercent(iReligion)
		
		return cls.desc("RELIGION_SPREAD_PERCENT").progr("RELIGION_SPREAD_PERCENT").format(options.objective("TO_PERCENT").singular()).objective(CvReligionInfo).func(value).turnly.subclass("ReligionSpreadPercent")
	
	@classproperty
	def population(cls):
		def value_function(self, iPlayer):
			return cities.owner(iPlayer).sum(CyCity.getPopulation)
		
		def total(self):
			return game.getTotalPopulation()
		
		return cls.desc("POPULATION_PERCENT").progr("POPULATION_PERCENT").func(value_function, total).subclass("PopulationPercent")
	
	@classproperty
	def religiousVote(cls):
		def value_function(self, iPlayer):
			return player(iPlayer).getVotes(16, 1)
		
		return cls.desc("RELIGIOUS_VOTE_PERCENT").progr("RELIGIOUS_VOTE_PERCENT").func(value_function).turnly.subclass("ReligiousVotePercent")
	
	@classproperty
	def alliedCommerce(cls):
		def value_function(self, iPlayer):
			return player(iPlayer).calculateTotalCommerce()
		
		return cls.desc("ALLIED_COMMERCE_PERCENT").progr("ALLIED_COMMERCE_PERCENT").allied.func(value_function).subclass("AlliedCommercePercent")
	
	@classproperty
	def alliedPower(cls):
		def value_function(self, iPlayer):
			return player(iPlayer).getPower()
		
		return cls.desc("ALLIED_POWER_PERCENT").progr("ALLIED_POWER_PERCENT").allied.func(value_function).subclass("AlliedPowerPercent")


def segment(tuple):
	if len(tuple) == 1:
		return tuple[0]
	return tuple
	
	
class Trigger(Condition):

	def __init__(self, *arguments):
		super(Trigger, self).__init__(*arguments)
		
		self.dCondition = dict((self.process_objectives(arguments), None) for arguments in self.arguments)
	
	def condition(self, *arguments):
		return self.completed(*arguments)
		
	def key(self, *arguments):
		return self.process_objectives(concat(self.arguments.subject, arguments))
	
	def completed(self, *arguments):
		return bool(self.dCondition[self.process_objectives(arguments)])
	
	def completable(self, *arguments):
		return self.dCondition[self.key(*arguments)] is None
		
	def complete(self, *arguments):
		if self.completable(*arguments):
			self.dCondition[self.key(*arguments)] = True
			self.check()
	
	def block(self, *arguments):
		if self.completable(*arguments):
			self.dCondition[self.key(*arguments)] = False
			self.expire()
	
	def hashable(self, item):
		if isinstance(item, CyCity):
			return False
		return item is not None
	
	def process_objectives(self, arguments):
		return tuple(argument for argument in arguments if self.hashable(argument))
	
	@classproperty
	def failable(cls):
		oldinit = cls.__init__
		def __init__(self, *arguments):
			oldinit(self, *arguments)
			self.extra_handlers.append('failable')
			self.complete()
			
		def single_objective_progress(self):
			return False
			
		return cls.func(__init__, single_objective_progress)
	
	@classproperty
	def firstDiscover(cls):
		def checkFirstDiscovered(self, iTech):
			if iTech in self.values:
				if game.countKnownTechNumTeams(iTech) == 1:
					self.complete(iTech)
		
		def expireFirstDiscovered(self, iTech):
			if iTech in self.values:
				self.expire()
		
		def single_objective_progress(self):
			return False
		
		return cls.desc("FIRST_DISCOVERED").objective(CvTechInfo).handle("techAcquired", checkFirstDiscovered).expired("techAcquired", expireFirstDiscovered).func(single_objective_progress).subclass("FirstDiscovered")
	
	@classproperty
	def firstSettle(cls):
		def init(self):
			self.lAllowedCivs = []
			
		def allowed(self, lCivs):
			self.lAllowedCivs = lCivs
			return self
	
		def checkFirstSettled(self, city):
			if city in self.arguments.subject:
				if self.arguments.subject.cities().without(city).none(lambda city: civ(city.getOriginalOwner()) not in self.lAllowedCivs):
					self.complete()
		
		return cls.desc("FIRST_SETTLE").subject(Plots).func(init, allowed).handle("cityBuilt", checkFirstSettled).subclass("FirstSettle")
	
	@classproperty
	def discover(cls):
		def checkDiscovered(self, iTech):
			if iTech in self.values:
				self.complete(iTech)
		
		def single_objective_progress(self):
			return False
		
		return cls.desc("DISCOVERED").objective(CvTechInfo).handle("techAcquired", checkDiscovered).func(single_objective_progress).subclass("Discovered")
	
	@classproperty
	def firstContact(cls):
		def checkFirstContact(self, iOtherPlayer):
			if civ(iOtherPlayer) in self.values:
				if self.arguments.subject.land().none(lambda plot: plot.isRevealed(iOtherPlayer, False)):
					self.complete(civ(iOtherPlayer))
				else:
					self.fail()
		
		def progress(self):
			return []
		
		return cls.subject(Plots).objective(Civ).handle("firstContact", checkFirstContact).func(progress).subclass("FirstContact")
	
	@classproperty
	def noCityLost(cls):
		def checkCityLost(self, iOtherPlayer, bConquest):
			self.fail()
		
		return cls.desc("NO_CITY_LOST").failable.handle("cityLost", checkCityLost).subclass("NoCityLost")
	
	@classproperty
	def tradeMission(cls):
		def checkTradeMission(self, tile, iGold):
			if tile in cities.of([city(self.iPlayer) for city in self.values if city(self.iPlayer) is not None]):
				self.complete()
		
		return cls.desc("TRADE_MISSION").progr("TRADE_MISSION").objective(CyCity).handle("tradeMission", checkTradeMission).subclass("TradeMission")
	
	@classproperty
	def neverConquer(cls):
		def checkCityAcquired(self, iOwner, city, bConquest):
			if bConquest:
				self.fail()
		
		return cls.desc("NEVER_CONQUER").failable.handle("cityAcquired", checkCityAcquired).subclass("NeverConquer")
	
	@classproperty
	def convertAfterFounding(cls):
		def checkConversion(self, iReligion):
			if iReligion in self.values and game.isReligionFounded(iReligion):
				if turn() - game.getReligionGameTurnFounded(iReligion) <= scale(self.arguments.subject):
					self.complete(iReligion)
				else:
					self.fail()
		
		return cls.desc("CONVERT_AFTER_FOUNDING").progr("CONVERT_AFTER_FOUNDING").format(options.number_word()).subject(int).objective(CvReligionInfo).handle("playerChangeStateReligion", checkConversion).subclass("ConvertAfterFounding")
	
	@classproperty
	def enterEra(cls):
		def init(self):
			self.iExpireEra = None
	
		def checkEnterEra(self, iTech):
			iEra = infos.tech(iTech).getEra()
			if iEra in self.values:
				self.complete(iEra)
		
		def checkExpire(self, iTech):
			iEra = infos.tech(iTech).getEra()
			if iEra == self.iExpireEra:
				self.expire()
		
		def before(self, iEra):
			self._description_suffixes.append(text("TXT_KEY_UHV_BEFORE_ENTER_ERA", infos.era(iEra).getText()))
			self.iExpireEra = iEra
			return self
		
		def single_objective_progress(self):
			return False
		
		return cls.desc("ENTER_ERA").objective(CvEraInfo).func(init, before).handle("techAcquired", checkEnterEra).expired("techAcquired", checkExpire).func(single_objective_progress).subclass("EnterEra")
	
	@classproperty
	def firstGreatPerson(cls):
		def specialist(unit):
			return next(iSpecialist for iSpecialist in infos.specialists() if infos.unit(unit).getGreatPeoples(iSpecialist))
			
		def checkGreatPersonBorn(self, unit):
			iGreatSpecialist = specialist(unit)
			if iGreatSpecialist in self.values:
				self.complete(iGreatSpecialist)
		
		def checkExpire(self, unit):
			iGreatSpecialist = specialist(unit)
			if iGreatSpecialist in self.values:
				self.block(iGreatSpecialist)
		
		return cls.objective(CvSpecialistInfo).handle("greatPersonBorn", checkGreatPersonBorn).expired("greatPersonBorn", checkExpire).subclass("FirstGreatPerson")
	

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
		self.check()
	
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
			return scale(infos.constant("GOLDEN_AGE_LENGTH") * objective)
	
		def incrementGoldenAges(self, *args):
			if self._player.isGoldenAge() and not self._player.isAnarchy():
				self.increment()
		
		def progress_value(self, value, required):
			return "%d / %d" % (value, required / infos.constant("GOLDEN_AGE_LENGTH"))
		
		return cls.desc("GOLDEN_AGES").progr("GOLDEN_AGES").format(options.number_word()).handle("BeginPlayerTurn", incrementGoldenAges).func(required, progress_value).subclass("GoldenAges")
	
	@classproperty
	def eraFirsts(cls):
		def incrementFirstDiscovered(self, iTech):
			iEra = infos.tech(iTech).getEra()
			if iEra in self.values:
				if game.countKnownTechNumTeams(iTech) == 1:
					self.increment(iEra)
		
		return cls.desc("ERA_FIRST_DISCOVERED").progr("ERA_FIRST_DISCOVERED").format(options.singular()).objective(CvEraInfo).handle("techAcquired", incrementFirstDiscovered).subclass("EraFirstDiscovered")
	
	@classproperty
	def sunkShips(cls):
		def incrementShipsSunk(self, losingUnit):
			if infos.unit(losingUnit).getDomainType() == DomainTypes.DOMAIN_SEA:
				self.increment()
		
		return cls.desc("SUNK_SHIPS").progr("SUNK_SHIPS").handle("combatResult", incrementShipsSunk).subclass("SunkShips")
	
	@classproperty
	def tradeGold(cls):
		def value_function(self, *objective):
			return self.dCount[objective] / 100
		
		def accumulateTradeGold(self, iGold):
			self.accumulate(iGold * 100)
			
		def accumulateTradeMissionGold(self, tile, iGold):
			self.accumulate(iGold * 100)
		
		def trackTradeGold(self, *args):
			iGold = cities.owner(self.iPlayer).sum(lambda city: city.getTradeYield(YieldTypes.YIELD_COMMERCE)) * self._player.getCommercePercent(CommerceTypes.COMMERCE_GOLD)
			iGold += players.major().alive().sum(self._player.getGoldPerTurnByPlayer) * 100
			self.accumulate(iGold)
		
		return cls.desc("TRADE_GOLD").progr("TRADE_GOLD").handle("playerGoldTrade", accumulateTradeGold).handle("tradeMission", accumulateTradeMissionGold).handle("BeginPlayerTurn", trackTradeGold).func(value_function).subclass("TradeGold")
	
	@classproperty
	def raidGold(cls):
		return cls.desc("RAID_GOLD").progr("RAID_GOLD").accumulated("unitPillage").accumulated("cityCaptureGold").accumulated("combatGold").subclass("RaidGold")
	
	@classproperty
	def pillage(cls):
		return cls.desc("PILLAGE_COUNT").progr("PILLAGED").incremented("unitPillage").subclass("PillageCount")
	
	@classproperty
	def acquiredCities(cls):
		return cls.desc("ACQUIRED_CITIES").progr("ACQUIRED_CITIES").incremented("cityAcquired").incremented("cityBuilt").subclass("AcquiredCities")
	
	@classproperty
	def piracyGold(cls):
		return cls.desc("PIRACY_GOLD").progr("PIRACY_GOLD").accumulated("unitPillage").accumulated("blockade").accumulated("combatGold").subclass("PiracyGold")
	
	@classproperty
	def razes(cls):
		return cls.desc("RAZE_COUNT").progr("RAZE_COUNT").format(options.city()).incremented("cityRazed").subclass("RazeCount")
	
	@classproperty
	def slaveTradeGold(cls):
		return cls.desc("SLAVE_TRADE_GOLD").progr("SLAVE_TRADE_GOLD").accumulated("playerSlaveTrade").subclass("SlaveTradeGold")
	
	@classproperty
	def greatGenerals(cls):
		def incrementGreatGenerals(self, unit):
			if infos.unit(unit).getGreatPeoples(iSpecialistGreatGeneral):
				self.increment()
		
		return cls.desc("GREAT_GENERALS").progr("GREAT_GENERALS").format(options.number_word()).handle("greatPersonBorn", incrementGreatGenerals).subclass("GreatGenerals")
	
	@classproperty
	def resourceTradeGold(cls):
		def accumulateTradeGold(self, *args):
			iGold = players.major().alive().sum(self._player.getGoldPerTurnByPlayer)
			self.accumulate(iGold)
	
		return cls.desc("RESOURCE_TRADE_GOLD").progr("RESOURCE_TRADE_GOLD").handle("BeginPlayerTurn", accumulateTradeGold).scaled.subclass("ResourceTradeGold")
	
	@classproperty
	def brokeredPeace(cls):
		return cls.desc("BROKERED_PEACE").progr("BROKERED_PEACE").format(options.number_word()).incremented("peaceBrokered").subclass("BrokeredPeaceCount")
	
	@classproperty
	def enslaves(cls):
		def init(self):
			self.lExcluded = []
		
		def excluding(self, lCivs):
			self.lExcluded = lCivs
			return self
		
		def incrementEnslaves(self, losingUnit):
			if civ(losingUnit) not in self.lExcluded:
				self.increment()
	
		return cls.progr("ENSLAVE_COUNT").func(init, excluding).handle("enslave", incrementEnslaves).subclass("EnslaveCount")
	
	@classproperty
	def healthiest(cls):
		def calculateHealthRating(iPlayer):
			if not player(iPlayer).isAlive():
				return 0
			
			iHealthy = player(iPlayer).calculateTotalCityHealthiness()
			iUnhealthy = player(iPlayer).calculateTotalCityUnhealthiness()
			
			return (iHealthy * 100) / max(1, iHealthy + iUnhealthy)
	
		def incrementHealthiest(self, *args):
			if players.major().alive().maximum(calculateHealthRating) == self.iPlayer:
				self.increment()
		
		return cls.desc("HEALTHIEST_TURNS").progr("HEALTHIEST_TURNS").handle("BeginPlayerTurn", incrementHealthiest).scaled.subclass("HealthiestTurns")
	
	@classproperty
	def happiest(cls):
		def calculateHappinessRating(iPlayer):
			if not player(iPlayer).isAlive():
				return 0
			
			iHappy = player(iPlayer).calculateTotalCityHappiness()
			iUnhappy = player(iPlayer).calculateTotalCityUnhappiness()
			
			return (iHappy * 100) / max(1, iHappy + iUnhappy)
		
		def incrementHappiest(self, *args):
			if players.major().alive().maximum(calculateHappinessRating) == self.iPlayer:
				self.increment()
		
		return cls.desc("HAPPIEST_TURNS").progr("HAPPIEST_TURNS").handle("BeginPlayerTurn", incrementHappiest).scaled.subclass("HappiestTurns")
	
	@classproperty
	def peace(cls):
		def incrementAtPeace(self, *args):
			if players.major().alive().none(lambda p: team(self.iPlayer).isAtWar(team(p).getID())):
				self.increment()
		
		return cls.desc("PEACE_TURNS").progr("PEACE_TURNS").handle("BeginPlayerTurn", incrementAtPeace).scaled.subclass("PeaceTurns")
	
	@classproperty
	def pope(cls):
		def incrementPope(self, *args):
			if game.getSecretaryGeneral(1) == self.iPlayer:
				self.increment()
		
		return cls.desc("POPE_TURNS").progr("POPE_TURNS").handle("BeginPlayerTurn", incrementPope).scaled.subclass("PopeTurns")
	
	@classproperty
	def combatFood(cls):
		return cls.desc("COMBAT_FOOD").progr("COMBAT_FOOD").accumulated("combatFood").subclass("CombatFood")
	
	@classproperty
	def sacrificeHappiness(cls):
		return cls.desc("SACRIFICE_HAPPINESS").progr("SACRIFICE_HAPPINESS").incremented("sacrificeHappiness").subclass("SacrificeHappiness")
	
	@classproperty
	def celebrate(cls):
		def incrementCelebrate(self, *args):
			iCelebratingCount = cities.owner(self.iPlayer).count(lambda city: city.isWeLoveTheKingDay())
			self.accumulate(iCelebratingCount)
		
		return cls.desc("CELEBRATE_TURNS").progr("CELEBRATE_TURNS").handle("BeginPlayerTurn", incrementCelebrate).scaled.subclass("CelebrateTurns")


class BestEntities(BaseGoal):

	@classmethod
	def objectives(cls, *types):
		types = list(types) + [int]
		return cls.plain_objectives(*types)
	
	@classmethod
	def plain_objectives(cls, *types):
		cls.builder.objectives(types)
		return cls
	
	@classmethod
	def subclass(cls, name):
		if not cls.builder.types.initialized():
			cls.objectives()
		return cls.format(options.number_word()).builder.create(cls, name)

	def __init__(self, *arguments):
		super(BestEntities, self).__init__(*arguments)
		self._progress = self._progress or "TXT_KEY_UHV_PROGRESS_BEST"
	
	def religion(self, iReligion=None):
		if iReligion is not None:
			self._description = replace_first(self._description, "TXT_KEY_UHV_MAKE_SURE") + " " + text("TXT_KEY_UHV_ARE_RELIGION", text(infos.religion(iReligion).getAdjectiveKey()))
		return super(BestEntities, self).religion()
	
	def secular(self):
		self._description = replace_first(self._description, "TXT_KEY_UHV_MAKE_SURE") + " " + text("TXT_KEY_UHV_ARE_SECULAR")
		return super(BestEntities, self).secular()
	
	def metric_func(self, *arguments):
		return lambda item: self.metric_wrapper(item, *arguments)
	
	def metric_wrapper(self, item, *arguments):
		if item is None:
			return 0
		if self.types.subject_type:
			arguments = arguments[1:]
		
		if arguments and isinstance(arguments[0], Aggregate):
			return arguments[0].eval(self.metric, item, *arguments[1:])
		
		return self.metric(item, *arguments)
	
	def condition(self, *arguments):
		arguments, iNumEntities = arguments[:-1], arguments[-1]
		entities = self.sorted(*arguments).limit(iNumEntities)
		return count(self.valid(entity, *arguments) for entity in entities if entity is not None) >= iNumEntities
	
	def sorted(self, *arguments):
		return self.entities().sort(metrics(self.metric_func(*arguments), bool_metric(self.valid, *arguments)), True)
	
	def objective_progress_entities(self, *arguments):
		remainder, iNumEntities = arguments[:-1], arguments[-1]
		entities = self.sorted(*remainder).take(iNumEntities)
		
		if self.condition(*arguments):
			next_entity = self.sorted(*remainder).without(entities).first()
		else:
			next_entity = self.sorted(*remainder).without(entities).where(lambda entity: self.valid(entity, *remainder)).first()
		
		entities.append(next_entity)
		return entities
	
	def rank_word(self, rank):
		if rank > 0:
			return "%s %s" % (capitalize(ordinal_word(rank+1)), text(self._progress))
		return capitalize(text(self._progress))
	
	def objective_progress(self, *arguments):
		entities = self.objective_progress_entities(*arguments)
		entities, next_entity = entities[:-1], entities[-1]
		
		ranks = [
			"%s %s: %s (%d)" % 
			(self.format_progress_indicator(self.valid(entity, *arguments[:-1])), 
			 self.rank_word(rank), 
			 self.entity_name(entity), 
			 self.metric_wrapper(entity, *arguments[:-1])) 
			for rank, entity in enumerate(entities) 
			if rank == 0 or entity is not None
		]
		
		if next_entity is not None:
			next_entity_key = self.condition(*arguments) and "TXT_KEY_UHV_PROGRESS_NEXT" or "TXT_KEY_UHV_PROGRESS_OUR_NEXT"
			ranks.append(text(next_entity_key, text(self._progress), self.entity_name(next_entity), self.metric_wrapper(next_entity, *arguments[:-1])))
		
		return ranks
	
	def progress(self, bForceSingle=False):
		return list(flatten(super(BestEntities, self).progress(bForceSingle)))
	
	def display(self, *arguments):
		ranks = ["%s (%d)" % (self.entity_name(entity), self.metric_wrapper(entity, *arguments[:-1])) for entity in self.objective_progress_entities(*arguments)]
		return "\n".join(ranks)


class BestPlayers(BestEntities):

	def __init__(self, *arguments):
		super(BestPlayers, self).__init__(*arguments)
	
	def entities(self):
		return players.major().alive()
	
	def entity_name(self, iPlayer):
		if iPlayer is None:
			return text("TXT_KEY_UHV_NO_PLAYER")
		return name(iPlayer)
	
	def valid(self, iPlayer, *arguments):
		return self.valid_player(iPlayer)
	
	@classproperty
	def tech(cls):
		def metric(self, iPlayer):
			return infos.techs().where(lambda iTech: team(iPlayer).isHasTech(iTech)).sum(lambda iTech: infos.tech(iTech).getResearchCost())
		
		return cls.desc("BEST_TECH_PLAYERS").progr("BEST_TECHNOLOGY").func(metric).subclass("BestTechPlayers")


class BestPlayer(BestPlayers):
	
	@classproperty
	def tech(cls):
		def metric(self, iPlayer):
			return infos.techs().where(lambda iTech: team(iPlayer).isHasTech(iTech)).sum(lambda iTech: infos.tech(iTech).getResearchCost())
		
		return cls.desc("BEST_TECH_PLAYER").progr("BEST_TECHNOLOGY").func(metric).subclass("BestTech")
	
	@classproperty
	def population(cls):
		def metric(self, iPlayer):
			return player(iPlayer).getRealPopulation()
		
		return cls.desc("BEST_POPULATION_PLAYER").progr("BEST_POPULATION").func(metric).subclass("BestPopulation")



class BestCities(BestEntities):

	def __init__(self, *arguments):
		super(BestCities, self).__init__(*arguments)
	
	def entities(self):
		return cities.all()
	
	def entity_name(self, city):
		if city is None:
			return text("TXT_KEY_UHV_NO_CITY")
		return city.getName()
	
	def valid(self, city, *arguments):
		if not city:
			return False
	
		if self.type == self.PLAYER:
			return city.getOwner() == self.iPlayer
		elif self.type == self.RELIGION:
			return self._player.getStateReligion() >= 0 and city.isHasReligion(self._player.getStateReligion())
		
		return False
	
	@classproperty
	def population(cls):
		def metric(self, city):
			return city.getPopulation()
		
		return cls.desc("BEST_POPULATION_CITIES").format(options.number_word()).progr("BEST_POPULATION").func(metric).subclass("BestPopulationCities")
	
	@classproperty
	def culture(cls):
		def metric(self, city):
			return city.getCulture(city.getOwner())
		
		return cls.desc("BEST_CULTURE_CITIES").format(options.number_word()).progr("BEST_CULTURE").func(metric).subclass("BestCultureCities")
	
	
class BestCity(BestCities):

	def __init__(self, *arguments):
		super(BestCity, self).__init__(*arguments)
	
	def valid(self, city, requiredCity, *arguments):
		if requiredCity is None:
			return False
			
		return super(BestCity, self).valid(city) and at(city, requiredCity)
	
	@classproperty
	def population(cls):
		def metric(self, city):
			return city.getPopulation()
		
		return cls.desc("BEST_POPULATION_CITY").progr("BEST_POPULATION").subject(CyCity).func(metric).subclass("BestPopulationCity")
	
	@classproperty
	def culture(cls):
		def metric(self, city):
			return city.getCulture(city.getOwner())
		
		return cls.desc("BEST_CULTURE_CITY").progr("BEST_CULTURE").subject(CyCity).func(metric).subclass("BestCultureCity")
	
	@classproperty
	def wonders(cls):
		def metric(self, city):
			return infos.buildings().count(lambda iBuilding: city.isHasRealBuilding(iBuilding) and isWonder(iBuilding))
		
		return cls.desc("BEST_WONDER_CITY").progr("BEST_WONDERS").subject(CyCity).func(metric).subclass("BestWonderCity")
	
	@classproperty
	def tradeIncome(cls):
		def metric(self, city):
			return city.getTradeYield(YieldTypes.YIELD_COMMERCE)
		
		return cls.desc("BEST_TRADE_INCOME_CITY").progr("BEST_TRADE_INCOME").subject(CyCity).func(metric).subclass("BestTradeIncomeCity")
	
	@classproperty
	def specialist(cls):
		def metric(self, city, iSpecialist):
			return city.getFreeSpecialistCount(iSpecialist)
		
		return cls.desc("BEST_SPECIALIST_CITY").progr("BEST_SPECIALIST").subject(CyCity).objective(CvSpecialistInfo).func(metric).subclass("BestSpecialistCity")


class RouteConnection(BaseGoal):

	def __init__(self, starts, targets, routes):
		super(RouteConnection, self).__init__()
		
		if isinstance(targets, CyPlot):
			targets = plots.of([targets])
		
		if isinstance(targets, Plots):
			targets = (targets,)
		
		if isinstance(starts, CyPlot):
			starts = plots.of([starts])
		
		self.starts = starts
		self.targets = targets
		self.lRoutes = list(routes)
		
		self.bStartOwners = False
		
		self.update_areas()
		
		self.every()
	
	def __nonzero__(self):
		return all(self.condition(targets) for targets in self.targets)
	
	def update_areas(self):
		if self.starts.name():
			self.areas[simple_name(self.starts.name())] = self.starts
		for target in self.targets:
			if target.name():
				self.areas[simple_name(target.name())] = target
		
	def withStartOwners(self):
		self.bStartOwners = True
		return self
	
	def routeTech(self, iRoute):
		iBuild = infos.builds().where(lambda iBuild: infos.build(iBuild).getRoute() == iRoute).first()
		return infos.build(iBuild).getTechPrereq()
		
	def valid_owner(self, plot):
		if plot.getOwner() == self.iPlayer:
			return True
		
		if self.bStartOwners and plot.getOwner() in self.starts.cities().owners():
			return True
		
		return False
	
	def valid(self, plot):
		return self.valid_owner(plot) and (plot.isCity() or plot.getRouteType() in self.lRoutes)
	
	def connected(self, start, targets):
		if not self.valid(start):
			return False
		
		if start in self.targets:
			return True
		
		targets = targets.where(self.valid)
		
		if not targets:
			return False
		
		nodes = [(targets.closest_distance(start), location(start))]
		heapq.heapify(nodes)
		
		visited = set()
		
		while nodes:
			heuristic, node = heapq.heappop(nodes)
			visited.add((heuristic, node))
			
			for plot in plots.surrounding(node).where(self.valid):
				if plot.isCity() and plot.getOwner() == self.iPlayer and plot in targets:
					return True
				
				tuple = (targets.closest_distance(plot), location(plot))
				if tuple not in visited and tuple not in nodes:
					heapq.heappush(nodes, tuple)
		
		return False
	
	def condition(self, targets):
		if none(self._team.isHasTech(self.routeTech(iRoute)) for iRoute in self.lRoutes):
			return False
		
		return any(self.connected(start.plot(), targets) for start in self.starts.cities())
	
	def progress(self, bForceSingle = False):
		return [self.objective_progress(targets) for targets in self.targets]
	
	def objective_progress(self, targets):
		return "%s %s" % (self.progress_indicator(targets), self.progress_text(targets))
	
	def progress_indicator_value(self, targets):
		return self.condition(targets)
	
	def progress_text(self, targets):
		routes = format_separators(self.lRoutes, ",", text("TXT_KEY_OR"), lambda iRoute: infos.route(iRoute).getText())
		return text("TXT_KEY_UHV_PROGRESS_ROUTE_CONNECTION", routes, self.starts.name(), targets.name())


class SubgoalCallback(object):

	def __init__(self, supergoal):
		self.supergoal = supergoal
	
	def stateChange(self, goal):
		if goal.state == SUCCESS:
			self.supergoal.check()
		elif goal.state == FAILURE:
			self.supergoal.fail()


class CheckedSubgoalCallback(SubgoalCallback):

	def check(self, goal):
		self.supergoal.check()
	
	def expire(self, goal):
		if isinstance(goal, Trigger):
			if count(goal.completed(*args) or goal.completable(*args) for args in goal.arguments) < self.supergoal.iRequired:
				self.supergoal.expire()
		else:
			self.supergoal.expire()


class All(BaseGoal):

	def __init__(self, *goals):
		super(All, self).__init__()
	
		self.goals = goals
		
		self.init_description()
		self.update_areas()
		
		self.subgoal_callback = SubgoalCallback(self)
	
	def update_areas(self):
		for goal in self.goals:
			for name, area in goal.areas.items():
				self.areas[name] += area
	
	def init_description(self):
		self._description = format_separators_shared(self.goals, ",", text("TXT_KEY_AND"), lambda goal: " ".join(concat(goal._description, goal._description_suffixes)))
		
	def activate(self, iPlayer, callback=None):
		super(All, self).activate(iPlayer, callback)
		
		for goal in self.goals:
			goal.activate(iPlayer, self.subgoal_callback)
	
	def deactivate(self):
		super(All, self).deactivate()
		
		for goal in self.goals:
			goal.deactivate()
	
	def setState(self, state):
		super(All, self).setState(state)
		
		if state == FAILURE:
			for goal in self.goals:
				goal.fail()
	
	def religion(self):
		for goal in self.goals:
			goal.religion()
		self.init_description()
		return self
	
	def secular(self):
		for goal in self.goals:
			goal.secular()
		self.init_description()
		return self
	
	def at(self, iYear):
		for goal in self.goals:
			goal.at(iYear)
		self._description_suffixes.append(text("TXT_KEY_UHV_IN", format_date(iYear)))
		self._iYear = iYear
		return self
	
	def by(self, iYear):
		for goal in self.goals:
			goal.by(iYear)
		self._description_suffixes.append(text("TXT_KEY_UHV_BY", format_date(iYear)))
		self._iYear = iYear
		return self
	
	def progress(self):
		subgoal_progress = [self.subgoal_progress(goal) for goal in self.goals if 'failable' not in goal.extra_handlers]
		return list(flatten(progress for progress in subgoal_progress if progress))
	
	def subgoal_progress(self, goal):
		progress_list = goal.progress(True)
		
		if progress_list:
			if goal.state == SUCCESS:
				return [text.replace(u"%c" % self.FAILURE_CHAR, u"%c" % self.SUCCESS_CHAR) for text in progress_list]
			return progress_list
		return ["%s %s" % (self.progress_indicator(goal), capitalize(goal._description))]
	
	def progress_indicator_value(self, goal):
		return goal.state == SUCCESS or (goal.possible() and goal)
	
	def __nonzero__(self):
		return all(goal.state == SUCCESS for goal in self.goals)
	
	def __str__(self):
		return "\n".join([str(goal) for goal in self.goals])


class Some(BaseGoal):

	def __init__(self, goal, iRequired):
		super(Some, self).__init__()
	
		self.goal = goal
		self.iRequired = iRequired
		
		self.init_description()
		self.update_areas()
	
	def init_description(self):
		self._description = replace_first(self.goal.description(), "TXT_KEY_UHV_SOME", number_word(self.iRequired))
	
	def update_areas(self):
		self.areas = copy(self.goal.areas)
	
	def activate(self, iPlayer, callback=None):
		super(Some, self).activate(iPlayer, callback)
		
		self.goal.activate(iPlayer, CheckedSubgoalCallback(self))
	
	def deactivate(self):
		super(Some, self).deactivate()
		self.goal.deactivate()
	
	def setState(self, state):
		super(Some, self).setState(state)
	
		if state == FAILURE:
			self.goal.fail()
	
	def progress(self):
		return self.goal.progress()
		
	def count(self):
		return count(self.goal.condition(*args) for args in self.goal.arguments)
	
	def __nonzero__(self):
		return self.count() >= self.iRequired
	
	def __str__(self):
		return "%d / %d" % (self.count(), self.iRequired)


class Any(Some):

	def __init__(self, goal):
		super(Any, self).__init__(goal, 1)


class DifferentCallback(SubgoalCallback):

	def stateChange(self, goal):
		if goal.state == SUCCESS:
			self.supergoal.record(goal)
			self.supergoal.check()
		elif goal.state == FAILURE:
			self.supergoal.fail()


class Different(BaseGoal):

	def __init__(self, *goals):
		super(Different, self).__init__()
		
		self.dGoals = dict((goal, None) for goal in goals)
		
		self.update_areas()
	
	@property
	def goals(self):
		return self.dGoals.keys()
	
	def update_areas(self):
		for goal in self.goals:
			for name, area in goal.areas.items():
				self.areas[name] += area
		
	def record_value(self, goal):
		raise NotImplementedError()
		
	def record(self, goal):
		self.dGoals[goal] = self.record_value(goal)
		
		if not self.unique_records():
			self.fail()
	
	def recorded(self, goal):
		return self.dGoals[goal]
	
	def display_record(self, record):
		raise NotImplementedError()
	
	def display_subgoal(self, goal):
		text = str(goal)
		record = self.recorded(goal)
		
		if record is None:
			record = self.record_value(goal)
			
		if record is not None:
			text = "%s: %s" % (self.display_record(record), text)
		return text
	
	def activate(self, iPlayer, callback=None):
		super(Different, self).activate(iPlayer, callback)
		
		for goal in self.goals:
			goal.activate(iPlayer, DifferentCallback(self))
	
	def deactivate(self):
		super(Different, self).deactivate()
		
		for goal in self.goals:
			goal.deactivate()
	
	def setState(self, state):
		super(Different, self).setState(state)
		
		if state == FAILURE:
			for goal in self.goals:
				goal.fail()
	
	def unique_records(self):
		records = [self.recorded(goal) for goal in self.goals]
		return len(records) == len(set(records))
	
	def description(self):
		return capitalize(format_separators([goal._description for goal in self.goals], ",", text("TXT_KEY_AND")))
	
	def __nonzero__(self):
		return all(goal.state == SUCCESS or goal for goal in self.goals) and self.unique_records()
	
	def __str__(self):
		return "\n".join([self.display_subgoal(goal) for goal in self.goals])
	
	def progress(self):
		progress_entries = []
		for goal in self.goals:
			if goal.state == SUCCESS:
				progress_entries.append(self.progress_completed(goal))
			elif goal.possible():
				progress_entries.append(goal.progress())
				break
		
		return progress_entries
	
	def progress_completed(self, goal):
		city_name = self.display_record(self.recorded(goal))
		return u"%c %s" % (self.SUCCESS_CHAR, getRenameName(self.iPlayer, city_name) or city_name)


class DifferentCities(Different):

	def record_value(self, goal):
		return location(goal.arguments.subject(self.iPlayer))
	
	def display_record(self, record):
		if city_(record):
			return city_(record).getName()


AttitudeCount = Count.attitude
AverageCulture = Count.averageCulture
AveragePopulation = Count.averagePopulation
BuildingCount = Count.building
CityBuilding = CityBuildings = Count.cityBuilding
CityCount = Count.numCities
CitySpecialistCount = Count.citySpecialist
ConqueredCityCount = Count.conqueredCities
ControlledResourceCount = Count.controlledResource
CorporationCount = Count.corporation
CultureCity = CultureCities = Count.cultureCities
CultureLevel = Count.cultureLevel
CultureLevelCities = Count.cultureLevelCities
DifferentSpecialist = DifferentSpecialists = Count.differentSpecialist
FeatureCount = Count.feature
ImprovementCount = Count.improvement
OpenBorderCount = Count.openBorders
PeakCount = Count.peaks
PlayerCulture = Count.culture
PlayerPopulation = Count.population
PlayerGold = Count.gold
PopulationCities = Count.populationCities
ResourceCount = Count.resource
SettledCityCount = Count.settledCities
ShrineIncome = Count.shrineIncome
SpecialistCount = Count.specialist
TerrainCount = Count.terrain
UnitCombatCount = Count.unitCombat
UnitCount = Count.unit
UnitLevelCount = Count.unitLevel
VassalCount = Count.vassals

AreaNoStateReligion = Condition.areaNoStateReligion
AllAttitude = Condition.allAttitude
Communist = Condition.communist
Control = Condition.control
ControlOrVassalize = Condition.controlOrVassalize
CultureCovered = Condition.cultureCovered
GoldPercent = Condition.goldPercent
MoreCulture = Condition.moreCulture
MoreReligion = Condition.moreReligion
NoForeignCities = Condition.noForeignCities
NoReligionPercent = Condition.noReligionPercent
NoStateReligion = Condition.noStateReligion
Project = Projects = Condition.project
Route = Condition.route
Settle = Condition.settle
StateReligionPercent = Condition.stateReligionPercent
TradeConnection = Condition.tradeConnection
Wonders = Wonder = Condition.wonder

ConvertAfterFounding = Trigger.convertAfterFounding
Discovered = Trigger.discover
EnterEra = Trigger.enterEra
FirstContact = Trigger.firstContact
FirstDiscovered = Trigger.firstDiscover
FirstGreatPerson = Trigger.firstGreatPerson
FirstSettle = Trigger.firstSettle
NeverConquer = Trigger.neverConquer
NoCityLost = Trigger.noCityLost
TradeMission = Trigger.tradeMission

AcquiredCities = Track.acquiredCities
BrokeredPeaceCount = Track.brokeredPeace
CelebrateTurns = Track.celebrate
CombatFood = Track.combatFood
EnslaveCount = Track.enslaves
EraFirstDiscovered = Track.eraFirsts
GoldenAges = Track.goldenAges
GreatGenerals = Track.greatGenerals
HappiestTurns = Track.happiest
HealthiestTurns = Track.healthiest
PeaceTurns = Track.peace
PillageCount = Track.pillage
PiracyGold = Track.piracyGold
PopeTurns = Track.pope
RaidGold = Track.raidGold
RazeCount = Track.razes
ResourceTradeGold = Track.resourceTradeGold
SacrificeHappiness = Track.sacrificeHappiness
SlaveTradeGold = Track.slaveTradeGold
SunkShips = Track.sunkShips
TradeGold = Track.tradeGold

BestCultureCities = BestCities.culture
BestPopulationCities = BestCities.population

BestCultureCity = BestCity.culture
BestPopulationCity = BestCity.population
BestSpecialistCity = BestCity.specialist
BestTradeIncomeCity = BestCity.tradeIncome
BestWonderCity = BestCity.wonders

BestTechPlayers = BestPlayers.tech

BestPopulation = BestPlayer.population
BestTech = BestPlayer.tech

AlliedCommercePercent = Percentage.alliedCommerce
AlliedPowerPercent = Percentage.alliedPower
AreaPercent = Percentage.areaControl
PopulationPercent = Percentage.population
ReligionSpreadPercent = Percentage.religionSpread
ReligiousVotePercent = Percentage.religiousVote
WorldPercent = Percentage.worldControl