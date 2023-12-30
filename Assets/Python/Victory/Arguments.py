from Core import *
from RFCUtils import *

from Core import base_building as base_building_core


def as_int(value):
	if isinstance(value, Aggregate):
		return value.of(int(item) for item in value.items)
	
	return int(value)


def base_building(building):
	if isinstance(building, Aggregate):
		return building.of(base_building_core(item) for item in building.items).named(building.name_key, building.name_key)
	
	if isinstance(building, NamedArgument):
		return building
	
	return base_building_core(building)


class NonExistingArgument(object):

	def __nonzero__(self):
		return False


NON_EXISTING = NonExistingArgument()


class NamedArgument(object):

	def __init__(self):
		self.name_key = ""
		self.name_args = []
		
	def named(self, key, *args):
		self.name_key = key
		self.name_args = args
		return self
	
	def name(self):
		return text(self.name_key, *self.name_args)


class NamedList(NamedArgument):

	def __init__(self, *items):
		NamedArgument.__init__(self)
		self.items = list(items)
	
	def __iter__(self):
		return iter(self.items)
	
	def __contains__(self, item):
		return item in self.items


class Aggregate(NamedArgument):

	@classmethod
	def of(cls, *items):
		return cls(*items)

	def __init__(self, *items):
		NamedArgument.__init__(self)
		self.items = list(variadic(*items))
	
	def __repr__(self):
		return "%s(%s)" % (type(self).__name__, ", ".join(str(item) for item in self.items))
	
	def __contains__(self, item):
		return item in self.items
	
	def __eq__(self, other):
		if isinstance(other, Aggregate):
			return self.items == other.items
		
		return other in self
	
	def validate(self, validate_func):
		return all(validate_func(item) for item in self.items)
	
	def format(self, format_func, **options):
		if self.name_key:
			return self.name()
	
		return format_separators(self.items, ",", text("TXT_KEY_AND"), lambda item: format_func(item, **options))
	
	def evaluate(self, evaluate_func, left_arguments=None, right_arguments=None):
		return self.aggregate([evaluate_func(*concat(left_arguments, item, right_arguments)) for item in self.items])
	
	def aggregate(self, items):
		raise NotImplementedError()


class SumAggregate(Aggregate):

	def aggregate(self, items):
		return sum(items)


class AverageAggregate(Aggregate):

	def aggregate(self, items):
		if len(items) == 0:
			return 0.0
		return 1.0 * sum(items) / len(items)


class CountAggregate(Aggregate):

	def aggregate(self, items):
		return count(items)


class AreaArgumentFactory(object):

	def __getattr__(self, name):
		area_argument = AreaArgument()
		return getattr(area_argument, name)


class AreaArgument(NamedArgument):

	def __init__(self):
		NamedArgument.__init__(self)
		
		self.calls = []
	
	def __contains__(self, item):
		return item in self.create()
	
	def __len__(self):
		return len(self.create())
	
	def __eq__(self, other):
		if not isinstance(other, AreaArgument):
			return False
			
		return self.create().same(other.create())
	
	def __repr__(self):
		return "AreaArgument%s" % "".join(".%s" % signature_name(func_name, *args, **kwargs) for func_name, args, kwargs in self.calls)
	
	def __add__(self, other):
		if not isinstance(other, AreaArgument):
			raise ValueError("Can only add AreaArgument, got: %s" % type(other).__name__)
		
		return CombinedAreaArgument(self, other)
	
	def call(self, func_name, args, kwargs):
		self.calls.append((func_name, args, kwargs))
		return self
	
	def call_for_civ(self, func_name, iCiv):
		self.call(func_name, (iCiv,), {})
		self.named(infos.civ(iCiv).getShortDescription(0))
		return self
	
	def initial(self):
		return PlotFactory()
	
	def create(self):
		instance = self.initial()
		
		for func_name, args, kwargs in self.calls:
			instance = getattr(instance, func_name)(*args, **kwargs)
		
		if isinstance(instance, Plots):
			instance.named(self.name())
		
		return instance
	
	def of(self, *args, **kwargs):
		return self.call("of", args, kwargs)
	
	def all(self, *args, **kwargs):
		return self.call("all", args, kwargs)
	
	def rectangle(self, *args, **kwargs):
		return self.call("rectangle", args, kwargs)
	
	def regions(self, *args, **kwargs):
		return self.call("regions", args, kwargs)

	def region(self, *args, **kwargs):
		return self.call("region", args, kwargs)
	
	def adjacent_regions(self, *args, **kwargs):
		return self.call("adjacent_regions", args, kwargs)

	def adjacent_region(self, *args, **kwargs):
		return self.call("adjacent_region", args, kwargs)
	
	def capital(self, *args, **kwargs):
		return self.call("capital", args, kwargs)
	
	def where(self, *args, **kwargs):
		return self.call("where", args, kwargs)
	
	def land(self, *args, **kwargs):
		return self.call("land", args, kwargs)
	
	def owner(self, *args, **kwargs):
		return self.call("owner", args, kwargs)
	
	def without(self, *args, **kwargs):
		return self.call("without", args, kwargs)
	
	def capitals(self, *args, **kwargs):
		return self.call("capitals", args, kwargs)
	
	def coastal(self, *args, **kwargs):
		return self.call("coastal", args, kwargs)
	
	def surrounding(self, *args, **kwargs):
		return self.call("surrounding", args, kwargs)
	
	def core(self, iCiv):
		return self.call_for_civ("core", iCiv)
	
	def normal(self, iCiv):
		return self.call_for_civ("normal", iCiv)
	
	def none(self, *args, **kwargs):
		return self.create().none(*args, **kwargs)
	
	def cities(self):
		return self.create().cities()
	
	def count(self):
		return self.create().count()
		
	def closest_distance(self, *args, **kwargs):
		return self.create().closest_distance(*args, **kwargs)


class CombinedAreaArgument(AreaArgument):

	def __init__(self, left, right):
		AreaArgument.__init__(self)
		
		self.left = left
		self.right = right
	
	def initial(self):
		return self.left.create() + self.right.create()


class DeferredArgument(NamedArgument):

	def get(self, iPlayer):
		raise NotImplementedError()
		
		
class CityArgument(DeferredArgument):

	def __eq__(self, other):
		if isinstance(other, CyCity):
			return at(self.get(other.getOwner()), other)
		
		return isinstance(other, type(self))

	def area(self):
		return None


class LocationCityArgument(CityArgument):

	def __init__(self, *tile):
		CityArgument.__init__(self)
	
		self.tile = duplefy(*tile)
	
	def __repr__(self):
		return "LocationCityArgument%s" % (self.tile,)
	
	def __eq__(self, other):
		if not isinstance(other, LocationCityArgument):
			return CityArgument.__eq__(self, other)
		
		return self.tile == other.tile
	
	def __hash__(self):
		return hash(self.tile)
	
	def get(self, iPlayer):
		location_city = city(self.tile)
		if not location_city or location_city.isNone():
			return NON_EXISTING
		
		return location_city
	
	def area(self):
		return plots.of([self.tile])


class CapitalCityArgument(CityArgument):

	def __repr__(self):
		return "CapitalCityArgument()"
	
	def __hash__(self):
		return 0
	
	def get(self, iPlayer):
		city = capital(iPlayer)
		if not city or city.isNone():
			return NON_EXISTING
		
		return city
	

class ReligionHolyCityArgument(CityArgument):

	def __init__(self, iReligion):
		CityArgument.__init__(self)
		
		self.iReligion = iReligion
	
	def __repr__(self):
		return "ReligionHolyCityArgument(%s)" % infos.religion(self.iReligion).getText()
	
	def __eq__(self, other):
		if not isinstance(other, ReligionHolyCityArgument):
			return CityArgument.__eq__(self, other)
		
		return self.iReligion == other.iReligion
	
	def get(self, iPlayer):
		city = game.getHolyCity(self.iReligion)
		if not city or city.isNone():
			return NON_EXISTING
		
		return city


class StateReligionHolyCityArgument(CityArgument):

	def __repr__(self):
		return "StateReligionHolyCityArgument()"
	
	def get(self, iPlayer):
		iStateReligion = player(iPlayer).getStateReligion()
		if iStateReligion < 0:
			return NON_EXISTING
		
		city = game.getHolyCity(iStateReligion)
		if not city or city.isNone():
			return NON_EXISTING
		
		return city


class WonderCityArgument(CityArgument):

	def __init__(self, iWonder):
		CityArgument.__init__(self)
		
		self.iWonder = iWonder
	
	def __repr__(self):
		return "WonderCityArgument(%s)" % infos.building(self.iWonder).getText()
	
	def __eq__(self, other):
		if not isinstance(other, WonderCityArgument):
			return CityArgument.__eq__(self, other)
		
		return self.iWonder == other.iWonder
	
	def get(self, iPlayer):
		city = getBuildingCity(self.iWonder)
		if not city or city.isNone():
			return NON_EXISTING
		
		return city


class StateReligionBuildingArgument(DeferredArgument):

	def __init__(self, building_func):
		DeferredArgument.__init__(self)
		
		self.building_func = building_func
	
	def __repr__(self):
		return "StateReligionBuildingArgument(%s)" % self.building_func.__name__
	
	def __eq__(self, other):
		return isinstance(other, StateReligionBuildingArgument) and self.building_func == other.building_func

	def get(self, iPlayer):
		iStateReligion = player(iPlayer).getStateReligion()
		if iStateReligion < 0:
			return NON_EXISTING
		
		return self.building_func(iStateReligion)


class CivsArgument(NamedArgument):

	@classmethod
	def group(cls, iGroup):
		return cls(*dCivGroups[iGroup])

	def __init__(self, *civs):
		NamedArgument.__init__(self)
		
		self.civs = civs
		
	def __repr__(self):
		return "CivsArgument(%s)" % ", ".join(infos.civ(iCiv).getShortDescription(0) for iCiv in self)
		
	def __contains__(self, identifier):
		return identifier in self.players()
	
	def __eq__(self, other):
		if not isinstance(other, CivsArgument):
			return False
		
		return set(self.civs) == set(other.civs)
	
	def __iter__(self):
		return iter(self.civs)
	
	def players(self):
		return players.of(*self.civs)
		
	def name(self):
		if not self.name_key:
			return format_separators(self, ",", text("TXT_KEY_AND"), lambda iCiv: infos.civ(iCiv).getShortDescription(0))
		
		return NamedArgument.name(self)
		

### Wrapper Functions ###


def religious_buildings(func):
	return SumAggregate(func(iReligion) for iReligion in infos.religions())

def wonders():
	return SumAggregate(iBuilding for iBuilding in infos.buildings() if isWonder(iBuilding)).named("TXT_KEY_VICTORY_NAME_WONDERS")
	
def group(iGroup):
	return CivsArgument.group(iGroup)

def start(identifier):
	return LocationCityArgument(dCapitals[identifier])

def happiness_resources():
	return [iResource for iResource in infos.bonuses() if infos.bonus(iResource).getHappiness() > 0]

def holy_city(iReligion = None):
	if iReligion is None:
		return StateReligionHolyCityArgument().named("TXT_KEY_VICTORY_NAME_HOLY_CITY")
	
	return ReligionHolyCityArgument(iReligion).named("TXT_KEY_VICTORY_NAME_RELIGION_HOLY_CITY", text(infos.religion(iReligion).getAdjectiveKey()))

def wonder(iWonder):
	return WonderCityArgument(iWonder)

def great_people():
	return SumAggregate(iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy).named("TXT_KEY_VICTORY_NAME_GREAT_PEOPLE")

def state_religion_building(func):
	return StateReligionBuildingArgument(func)