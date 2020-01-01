# coding: utf-8

from CvPythonExtensions import *
from Consts import *
from StoredData import *

import BugCore
import Popup

import random
from copy import copy


gc = CyGlobalContext()
MainOpt = BugCore.game.MainInterface

interface = CyInterface()
translator = CyTranslator()
game = gc.getGame()
map = gc.getMap()


def closestCity(entity, owner=PlayerTypes.NO_PLAYER, same_continent=False, coastal_only=False, skip_city=None):
	if skip_city is None:
		if isinstance(entity, CyCity):
			skip_city = entity
		else:
			skip_city = CyCity()
			
	x, y = _parse_tile(entity)
	city = map.findCity(x, y, owner, TeamTypes.NO_TEAM, same_continent, coastal_only, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, skip_city)
	
	if city.isNone():
		return None
	return city

def specialbuilding(iType, iReligion):
	lBuildings = [iBuilding for iBuilding in range(iNumBuildings) if infos.building(iBuilding).getSpecialBuildingType() == iType and infos.building(iBuilding).getReligionType() == iReligion]
	if lBuildings:
		return lBuildings[0]
	return None
	
	
def temple(iReligion):
	return specialbuilding(infos.type('SPECIALBUILDING_TEMPLE'), iReligion)
	
	
def monastery(iReligion):
	return specialbuilding(infos.type('SPECIALBUILDING_MONASTERY'), iReligion)
	
	
def cathedral(iReligion):
	return specialbuilding(infos.type('SPECIALBUILDING_CATHEDRAL'), iReligion)


def permutations(first, second):
	return [(first_element, second_element) for first_element in first for second_element in second]


def any(iterable):
	for element in iterable:
		if element:
			return True
	return False
	
	
def all(iterable):
	for element in iterable:
		if not element:
			return False
	return True
	
	
def next(iterator, default = None):
	iterator = iter(iterator)
	try:
		return iterator.next()
	except StopIteration, e:
		return default


def retrieve(dict, key, otherwise=None):
	if key in dict:
		return dict[key]
	return otherwise


def message(iPlayer, key, *format, **settings):
	iColor = retrieve(settings, 'color', otherwise=iWhite)
	iEvent = retrieve(settings, 'event', otherwise=0)
	iButton = retrieve(settings, 'button', otherwise='')
	
	sound = retrieve(settings, 'sound', otherwise='')
	force = retrieve(settings, 'force', otherwise=False)
	
	tile = retrieve(settings, 'location')
	iX, iY = -1, -1
	if tile:
		iX, iY = location(tile)
	
	interface.addMessage(iPlayer, force, iDuration, text(key, *format), sound, iEvent, iButton, ColorTypes(iColor), iX, iY, True, True)


def flatten(iterables):
	for iterable in iterables:
		for element in iterable:
			yield element


def move(unit, destination):
	if destination is None:
		return
	
	if location(unit) >= (0, 0) and location(unit) != location(destination):
		x, y = _parse_tile(destination)
		unit.setXY(x, y, False, True, False)

		
def popup(id, title, message, labels=[]):
	popup = Popup.PyPopup(id, EventContextTypes.EVENTCONTEXT_ALL)
	popup.setHeaderString(title)
	popup.setBodyString(message)
	for label in labels:
		popup.addButton(label)
	popup.launch(labels)


def stability(iPlayer):
	return data.players[iPlayer].iStabilityLevel


def has_civic(identifier, iCivic):
	return player(identifier).getCivics(gc.getCivicInfo(iCivic).getCivicOptionType()) == iCivic


def scenarioStartTurn():
	return getTurnForYear(scenarioStartYear())


def scenarioStartYear():
	lStartYears = [-3000, 600, 1700]
	return lStartYears[scenario()]


def scenario():
	if pEgypt.isPlayable(): return i3000BC
	if pByzantium.isPlayable(): return i600AD
	return i1700AD


def unittype(identifier):
	if isinstance(identifier, CyUnit):
		return identifier.getUnitType()
		
	if isinstance(identifier, int):
		return identifier
		
	raise TypeError("Expected unit type to be CyUnit or int, received: '%s'" % type(identifier))


def base_building(iBuilding):
	return gc.getBuildingClassInfo(gc.getBuildingInfo(iBuilding).getBuildingClassType()).getDefaultBuildingIndex()


def base_unit(iUnit):
	return gc.getUnitClassInfo(gc.getUnitInfo(unittype(iUnit)).getUnitClassType()).getDefaultUnitIndex()
	
	
def unique_building_from_class(iPlayer, iBuildingClass):
	return gc.getCivilizationInfo(player(iPlayer).getCivilizationType()).getCivilizationBuildings(iBuildingClass)
	
	
def unique_building(iPlayer, iBuilding):
	if not player(iPlayer): return base_building(iBuilding)
	return unique_building_from_class(iPlayer, gc.getBuildingInfo(iBuilding).getBuildingClassType())


def unique_unit_from_class(iPlayer, iUnitClass):
	return gc.getCivilizationInfo(player(iPlayer).getCivilizationType()).getCivilizationUnits(iUnitClass)


def unique_unit(iPlayer, iUnit):
	if not player(iPlayer): return base_unit(iUnit)
	return unique_unit_from_class(iPlayer, gc.getUnitInfo(unittype(iUnit)).getUnitClassType())


def master(iPlayer):
	return players.all().alive().where(lambda p: team(iPlayer).isVassal(p)).first()


def vassals():
	vassals = appenddict()
	for iPlayer in players.all().alive():
		master_id = master(iPlayer)
		if master_id:
			vassals[master_id].append(iPlayer)
	return vassals
	
	
def deepdict(dictionary = {}):
	return defaultdict(dictionary, {})


def appenddict(dictionary = {}):
	return defaultdict(dictionary, [])


def defaultdict(dictionary, default):
	return DefaultDict(dictionary, default)


def is_minor(identifier):
	return player(identifier).isMinorCiv() or player(identifier).isBarbarian()


def estimate_direction(fromPlot, toPlot):
	fromPlot = plot(fromPlot)
	toPlot = plot(toPlot)
	
	return estimateDirection(dxWrap(toPlot.getX() - fromPlot.getX()), dyWrap(toPlot.getY() - fromPlot.getY()))


def negate(function):
	return lambda x: not function(x)
	
	
def scale(value):
	return turns(value)


def turns(iTurns):
	iModifier = infos.gameSpeed().getGrowthPercent()
	return iTurns * iModifier / 100
	
	
def year(year=None):
	if year is None:
		return Turn(gc.getGame().getGameTurn())
	return Turn(getTurnForYear(year))


def turn(turn = None):
	return year(turn)


def missionary(iReligion):
	if iReligion < 0: return None
	return iMissionary + iReligion


def makeUnit(iPlayer, iUnit, plot, iUnitAI = UnitAITypes.NO_UNITAI):
	return makeUnits(iPlayer, iUnit, plot, 1, iUnitAI).one()


def makeUnits(iPlayer, iUnit, plot, iNumUnits = 1, iUnitAI = UnitAITypes.NO_UNITAI):
	if iNumUnits <= 0:
		return

	x, y = location(plot)
	
	units = []
	for _ in range(iNumUnits):
		unit = player(iPlayer).initUnit(iUnit, x, y, iUnitAI, DirectionTypes.DIRECTION_SOUTH)
		units.append(unit)
		
	return CreatedUnits(units)


def encode(text):
	if isinstance(text, (str, unicode)):
		return str(text.encode('utf-8'))
	return text


def text(key, *format):
	if isinstance(key, unicode) and len(format) == 0:
		return key
	return translator.getText(str(key), tuple([encode(f) for f in format]))
	
	
def text_if_exists(key, *format, **kwargs):
	otherwise = retrieve(kwargs, 'otherwise')
	key_text = text(key, *format)
	if key_text != key:
		return key_text
	elif otherwise:
		return text(otherwise, *format)
	return ''


def debug(message):
	if MainOpt.isShowDebugPopups():
		show(message)


def show(message):
	popup = Popup.PyPopup()
	popup.setBodyString(message)
	popup.launch()


def distance(location1, location2):
	x1, y1 = _parse_tile(location1)
	x2, y2 = _parse_tile(location2)
	return stepDistance(x1, y1, x2, y2)
	
	
def sort(iterable, key = lambda x: x, reverse = False):
	return sorted(iterable, key=key, reverse=reverse)
	

def find_max(list, metric = lambda x: x):
	return find(list, metric, True)
	
	
def find_min(list, metric = lambda x: x):
	return find(list, metric, False)
	
	
def find(list, metric = lambda x: x, reverse = True):
	if not list: return FindResult(None, None, None)
	result = sort(list, metric, reverse)[0]
	return FindResult(result = result, index = list.index(result), value = metric(result))


def rand(iLeft, iRight = None):
	if iRight is None:
		iLeft = 0
		iRight = iLeft
	
	return iLeft + gc.getGame().getSorenRandNum(iRight - iLeft, 'random number')
	
	
def random_entry(iterable):
	if not iterable:
		return None
		
	return iterable[rand(len(iterable))]
	
	
def name(identifier):
	return player(identifier).getCivilizationShortDescription(0)
	

def fullname(identifier):
	return player(identifier).getCivilizationDescription(0)


def adjective(identifier):
	return player(identifier).getCivilizationAdjective(0)


def _parse_tile(*args):
	if len(args) == 2:
		return args
	elif len(args) == 1:
		if isinstance(args[0], tuple) and len(args[0]) == 2:
			return args[0]
		elif isinstance(args[0], (CyPlot, CyCity, CyUnit)):
			if args[0].getX() < 0 or args[0].getY() < 0:
				return None
			return args[0].getX(), args[0].getY()
	
	raise TypeError("Only accepts two coordinates or a tuple of two coordinates, received: %s %s" % (args, type(args[0])))
		

def _iterate(first, next, getter = lambda x: x):
	list = []
	entity, iter = first(False)
	while entity:
		list.append(getter(entity))
		entity, iter = next(iter, False)
	return list
	
	
def wrap(*args):
	parsed = _parse_tile(*args)
	if parsed is None: 
		return None
	x, y = parsed
	return x % iWorldX, max(0, min(y, iWorldY-1))


def plot(*args):
	x, y = _parse_tile(*args)
	return gc.getMap().plot(x, y)
	
	
def city(*args):
	p = plot(*args)
	if not p.isCity():
		return None
	return p.getPlotCity()
	
	
def unit(key):
	if isinstance(key, UnitKey):
		return gc.getPlayer(key.owner).getUnit(key.id)
		
	raise TypeError("Expected key to be UnitKey, received '%s'" % type(key))
	
	
def location(entity):
	if not entity:
		raise ValueError("Location is None")

	if isinstance(entity, (CyPlot, CyCity, CyUnit)):
		return entity.getX(), entity.getY()

	return _parse_tile(entity)
	
	
def unit_key(unit):
	return UnitKey(unit.getOwner(), unit.getID())
	

def team(identifier = None):
	if identifier is None:
		return gc.getTeam(gc.getActivePlayer().getTeam())

	if isinstance(identifier, CyTeam):
		return identifier
		
	if isinstance(identifier, (CyPlayer, CyUnit, CyCity, CyPlot)):
		return gc.getTeam(identifier.getTeam())
		
	if isinstance(identifier, int):
		return gc.getTeam(gc.getPlayer(identifier).getTeam())
		
	raise TypeError("Expected identifier to be CyTeam, CyPlayer, CyCity, CyUnit, CyPlot or int, received '%s'" % type(identifier))
	
	
def teamtype(iTeam):
	return gc.getTeam(iTeam)
	
	
def player(identifier = None):
	if identifier is None:
		return gc.getActivePlayer()

	if isinstance(identifier, CyPlayer):
		return identifier
		
	if isinstance(identifier, CyTeam):
		return gc.getPlayer(identifier.getLeaderID())
		
	if isinstance(identifier, (CyPlot, CyCity, CyUnit)):
		return gc.getPlayer(identifier.getOwner())
		
	if isinstance(identifier, int):
		if identifier < 0: return None
		return gc.getPlayer(identifier)
		
	raise TypeError("Expected identifier to be CyPlayer, CyTeam, CyPlot, CyCity, CyUnit, or int, received '%s'" % type(identifier))
	

def civ(identifier):
	return player(identifier).getCivilizationType()
	
	
def human():
	return gc.getGame().getActivePlayer()
	
	
class FindResult(object):

	def __init__(self, result, index, value):
		self.result = result
		self.index = index
		self.value = value
	
	
class EntityCollection(object):

	def _factory(self, key):
		return key

	def __init__(self, keys):
		self._keys = list(keys)
		
	def __getitem__(self, index):
		return self.entities()[index]
		
	def __add__(self, other):
		if other is None: return self
		if not isinstance(other, type(self)):
			raise TypeError("Cannot combine left '%s' with right '%s'" % (type(self), type(other)))
		return self.__class__(self._keys + other._keys)
		
	def __iter__(self):
		return iter(self.entities())
		
	def __len__(self):
		return len(self.entities())
		
	def __str__(self):
		return str(self.entities())
		
	def __eq__(self, other):
		if isinstance(other, type(self)):
			return self._keys == other._keys
		raise TypeError("Cannot compare '%s' and '%s'" % (type(self), type(other)))
			
	def __ne__(self, other):
		return not self.__eq__(other)
		
	def __gt__(self, other):
		if isinstance(other, type(self)):
			return self.count() > other.count()
		elif isinstance(other, int):
			return self.count() > other
		raise TypeError("Cannot compare '%s' and '%s'" % (type(self), type(other)))
			
	def __ge__(self, other):
		if isinstance(other, type(self)):
			return self.count() >= other.count()
		elif isinstance(other, int):
			return self.count() >= other
		raise TypeError("Cannot compare '%s' and '%s'" % (type(self), type(other)))
		
	def __lt__(self, other):
		if isinstance(other, type(self)):
			return self.count() < other.count()
		elif isinstance(other, int):
			return self.count() < other
		raise TypeError("Cannot compare '%s' and '%s'" % (type(self), type(other)))
		
	def __le__(self, other):
		if isinstance(other, type(self)):
			return self.count() <= other.count()
		elif isinstance(other, int):
			return self.count() <= other
		raise TypeError("Cannot compare '%s' and '%s'" % (type(self), type(other)))
		
	def same(self, other):
		if isinstance(other, type(self)):
			return set(self._keys) == set(other._keys)
		raise TypeError("Cannot compare '%s' and '%s'" % (type(self), type(other)))

	def entities(self):
		return [self._factory(k) for k in self._keys]
		
	def where(self, condition):
		return self.__class__([k for k in self._keys if condition(self._factory(k))])
		
	def any(self, condition = None):
		if condition is None: return bool(self)
		return bool(self.where(condition))
		
	def all(self, condition):
		return not self.any(negate(condition))
		
	def none(self, condition = None):
		return not self.any(condition)
		
	def random(self):
		return random_entry(self.entities())
		
	def get(self, function = lambda x: x):
		return [function(e) for e in self.entities()]
		
	def first(self):
		if not self: return None
		return self.entities()[0]
		
	def one(self):
		if len(self) != 1:
			raise Exception("Only excepted one element in %s, but got: %s" % (type(self), str(self)))
		return self.first()
		
	def sample(self, iSampleSize):
		if not self: return []
		iSampleSize = min(iSampleSize, len(self))
		if iSampleSize <= 0: return None
		return random.sample(self.entities(), iSampleSize)
		
	def buckets(self, *conditions):
		rest = lambda e: not any([condition(e) for condition in conditions])
		buckets = [self.where(condition) for condition in conditions]
		buckets.append(self.where(rest))
		return tuple(buckets)
		
	def split(self, condition):
		return self.buckets(condition)
		
	def sort(self, metric, reverse=False):
		return self.__class__(sort(self._keys, key=lambda k: metric(self._factory(k)), reverse=reverse))
		
	def highest(self, iNum=1, metric=lambda x: x):
		return self.sort(metric, True).limit(iNum)
		
	def lowest(self, iNum=1, metric=lambda x: x):
		return self.sort(metric).limit(iNum)
		
	def including(self, *keys):
		print "keys (%s): %s" % (type(keys), keys)
		if len(keys) == 1:
			if isinstance(keys[0], type(self)):
				keys = keys[0]._keys
			elif isinstance(keys[0], list):
				keys = keys[0]
		combined = list(keys) + list(self._keys)
		print "combined: %s" % combined
		return self.__class__(sorted(set(combined), key=combined.index))
		
	def limit(self, iLimit):
		return self.__class__(self._keys[:iLimit])
		
	def count(self):
		return len(self)
		
	def maximum(self, metric):
		return find_max(self.entities(), metric).result
		
	def rank(self, key, metric):
		sorted_keys = sort(self._keys, lambda k: metric(self._factory(k)), True)
		return sorted_keys.index(key)
		
	def shuffle(self):
		shuffled = self._keys[:]
		random.shuffle(shuffled)
		return self.__class__(shuffled)
		
	def fraction(self, iDenominator):
		return self.limit(self.count() / iDenominator)
		
	def sum(self, value):
		return sum(value(e) for e in self.entities())
		
	def transform(self, cls, map = lambda x: x, condition = lambda x: x):
		return cls([map(k) for k in self._keys if condition(self._factory(k))])


class PlotsCorner:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def end(self, *args):
		x, y = _parse_tile(*args)
		return Plots([(i, j) for i in range(min(self.x, x), min(max(self.x, x)+1, iWorldX)) for j in range(min(self.y, y), min(max(self.y, y)+1, iWorldY))])
	

# maybe .owner(iPlayer)? check how often we use all().owner()
class PlotFactory:

	def of(self, list):
		return Plots(list)

	def start(self, *args):
		x, y = _parse_tile(*args)
		return PlotsCorner(x, y)
	
	def rectangle(self, start, end=None):
		if end is None:
			if isinstance(start, tuple) and len(start) == 2:
				start, end = start
			else:
				raise TypeError("If only one argument is provided, it needs to be a tuple of two coordinate pairs, got: '%s'" % type(start))
		return self.start(start).end(end)
		
	def all(self):
		return self.start(0, 0).end(iWorldX, iWorldY)
		
	def regions(self, *regions):
		return self.all().where(lambda p: p.getRegionID() in regions)
		
	def region(self, iRegion):
		return self.regions(iRegion)
		
	def surrounding(self, tile, radius=1):
		if radius < 0: raise ValueError("radius cannot be negative, received: '%d'" % radius)
		x, y = _parse_tile(tile)
		return Plots(sort(list(set([wrap(x+i, y+j) for i in range(-radius, radius+1) for j in range(-radius, radius+1)]))))
		
	def ring(self, tile, radius):
		return self.surrounding(tile, radius=radius).without(self.surrounding(tile, radius=radius-1))

	def owner(self, iPlayer):
		return self.all().owner(iPlayer)


class Plots(EntityCollection):

	def __init__(self, plots):
		super(Plots, self).__init__(plots)
		
	def _factory(self, key):
		return plot(key)
		
	def __contains__(self, item):
		if isinstance(item, (CyPlot, CyCity, CyUnit)):
			return (item.getX(), item.getY()) in self._keys
			
		if isinstance(item, tuple) and len(item) == 2:
			return item in self._keys
			
		raise TypeError("Tried to check if Plots contains '%s', can only contain plots, cities, units or coordinate tuples" % type(item))
		
	def __str__(self):
		return str(self._keys)
		
	def cities(self):
		return self.transform(Cities, condition = lambda p: p.isCity())
		
	def units(self):
		return sum([units.at(p) for p in self.entities()], Units([]))
		
	def without(self, exceptions):
		if not isinstance(exceptions, (list, set, Plots)):
			exceptions = [exceptions]
	
		return self.where(lambda p: location(p) not in [location(e) for e in exceptions])
		
	def _closest(self, *args):
		x, y = _parse_tile(*args)
		return find_min(self.entities(), lambda p: distance(p, (x, y)))
		
	def closest(self, *args):
		return self._closest(*args).result
		
	def closest_distance(self, *args):
		return self._closest(*args).value
		
	def owner(self, iPlayer):
		return self.where(lambda p: p.getOwner() == iPlayer)
		
	def notowner(self, iPlayer):
		return self.where(lambda p: p.getOwner() != iPlayer)
	
	def regions(self, *regions):
		return self.where(lambda p: p.getRegionID() in regions)
	
	def region(self, iRegion):
		return self.regions(iRegion)
		
	def where_surrounding(self, condition, radius=1):
		return self.where(lambda p: plots.surrounding(p, radius).all(condition))
	
	def land(self):
		return self.where(lambda p: not p.isWater())
	
	def water(self):
		return self.where(lambda p: p.isWater())
		
	def core(self, iPlayer):
		return self.where(lambda p: p.isCore(iPlayer))
		
	def passable(self):
		return self.where(lambda p: not p.isImpassable())

		
class CitiesCorner:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def end(self, *args):
		x, y = _parse_tile(*args)
		return PlotsCorner(self.x, self.y).end(x, y).cities()
		
		
class CityFactory:

	def owner(self, identifier):
		owner = player(identifier)
		cities = _iterate(owner.firstCity, owner.nextCity, location)
		return Cities(cities)
		
	def all(self):
		cities = []
		for iPlayer in range(iNumTotalPlayersB):
			cities += self.owner(iPlayer)
		return Cities(cities)
		
	def start(self, *args):
		x, y = _parse_tile(*args)
		return CitiesCorner(x, y)
	
	def rectangle(self, start, end=None):
		if end is None:
			if isinstance(start, tuple) and len(start) == 2:
				start, end = start
			else:
				raise TypeError("If only one argument is provided, it needs to be a tuple of two coordinate pairs, got: '%s'" % type(start))
		return self.start(start).end(end)
		
	def regions(self, *regions):
		return PlotFactory().regions(*regions).cities()
		
	def region(self, iRegion):
		return self.regions(iRegion)
		
	def of(self, list):
		return Plots(list).cities()
		
	def surrounding(self, tile, radius=1):
		return plots.surrounding(tile, radius).cities()


class Cities(EntityCollection):

	def __init__(self, plots):
		super(Cities, self).__init__(plots)
		
	def _factory(self, key):
		return city(key)
		
	def __contains__(self, item):
		if isinstance(item, (CyPlot, CyCity, CyUnit)):
			return (item.getX(), item.getY()) in self._keys
			
		if isinstance(item, tuple) and len(item) == 2:
			return item in self._keys
			
		raise TypeError("Tried to check if Cities contains '%s', can only contain plots, cities, units or coordinate tuples" % type(item))
		
	def __str__(self):
		return str(["%s (%s) at %s" % (city.getName(), adjective(city.getOwner()), (city.getX(), city.getY())) for city in self.entities()])
		
	def without(self, exceptions):
		if not isinstance(exceptions, (list, set, Cities, Plots)):
			exceptions = [exceptions]
	
		return self.where(lambda c: location(c) not in [location(e) for e in exceptions])
		
	def religion(self, iReligion):
		return self.where(lambda city: city.isHasReligion(iReligion))
		
	def owner(self, iPlayer):
		return self.where(lambda city: city.getOwner() == iPlayer)
	
	def notowner(self, iPlayer):
		return self.where(lambda city: city.getOwner() != iPlayer)
	
	def regions(self, *regions):
		return self.where(lambda city: city.getRegionID() in regions)
	
	def region(self, iRegion):
		return self.regions(iRegion)
		
	def building(self, iBuilding):
		return self.where(lambda city: city.isHasRealBuilding(iBuilding))
	
	def building_effect(self, iBuilding):
		return self.where(lambda city: city.isHasBuildingEffect(iBuilding))

	def coastal(self):
		return self.where(lambda city: city.isCoastal(10))

	def core(self, iPlayer):
		return self.where(lambda city: plot(city).isCore(iPlayer))
	
		
class UnitFactory:

	def of(self, units):
		return Units([UnitKey.of(unit) for unit in units])

	def owner(self, identifier):
		units = _iterate(player(identifier).firstUnit, player(identifier).nextUnit, unit_key)
		return Units(units)
		
	def at(self, *args):
		if args is None:
			return Units([])
		units = [unit_key(plot(*args).getUnit(i)) for i in range(plot(*args).getNumUnits())]
		return Units(units)
		
		
class UnitKey:

	def __init__(self, owner, id):
		self.owner = owner
		self.id = id
		
	def __eq__(self, other):
		return isinstance(other, UnitKey) and (self.owner, self.id) == (other.owner, other.id)
		
	def __str__(self):
		return str((self.owner, self.id))
		
	@classmethod
	def of(cls, unit):
		if isinstance(unit, cls):
			return unit
		return cls(unit.getOwner(), unit.getID())
		
		
class Units(EntityCollection):

	def __init__(self, units):
		super(Units, self).__init__([UnitKey.of(u) for u in units])
		
	def _factory(self, key):
		return unit(key)
		
	def __contains__(self, item):
		if isinstance(item, CyUnit):
			return UnitKey.of(item) in self._keys
			
		raise TypeError("Tried to check if Units contains '%s', can only contain units" % type(item))
		
	def __str__(self):
		return ", ".join(["%s (%s) at %s" % (unit.getName(), adjective(unit.getOwner()), (unit.getX(), unit.getY())) for unit in self.entities()])
		
	def owner(self, iPlayer):
		return self.where(lambda u: u.getOwner() == iPlayer)
		
	def notowner(self, iPlayer):
		return self.where(lambda u: u.getOwner() != iPlayer)
		
	def type(self, iUnitType):
		return self.where(lambda u: u.getUnitType() == iUnitType)
		
	def by_type(self):
		return dict([(iType, self.type(iType)) for iType in set([unit.getUnitType() for unit in self])])
		
	def atwar(self, iPlayer):
		return self.where(lambda u: team(iPlayer).isAtWar(u.getTeam()))
		
	def domain(self, iDomain):
		return self.where(lambda u: u.getDomainType() == iDomain)
	
		
class PlayerFactory:

	def major(self):
		return Players(range(iNumPlayers))
		
	def all(self):
		return Players(range(iNumTotalPlayers))
		
	def withBarbarian(self):
		return Players(range(iNumTotalPlayersB))
		
	def minor(self):
		return Players(range(iNumPlayers, iNumTotalPlayersB))
		
	def vassals(self, iPlayer):
		return self.all().where(lambda p: team(p).isVassal(player(iPlayer).getID()))
		
	def none(self):
		return Players([])
		
		
class Players(EntityCollection):

	def __init__(self, players):
		super(Players, self).__init__(players)
		
	def __contains__(self, item):
		if isinstance(item, CyPlayer):
			return item.getID() in self._keys
			
		# we assume ints are civilization IDs, not player IDs
		if isinstance(item, int):
			return item in [civ(p) for p in self._keys]
			
		raise TypeError("Tried to check if Players contains '%s', can only check CyPlayer or civilization IDs" % type(item))
		
	def __iter__(self):
		return iter(self._keys)
		
	def __str__(self):
		return ','.join([name(p) for p in self.entities()])
		
	def where(self, condition):
		return self.__class__([k for k in self._keys if condition(k)])
		
	def sort(self, metric, reverse=False):
		return self.__class__(sort(self._keys, key=lambda k: metric(k), reverse=reverse))
		
	def players(self):
		return [player(p) for p in self.entities()]
	
	def alive(self):
		return self.where(lambda p: player(p).isAlive())
	
	def notalive(self):
		return self.where(lambda p: not player(p).isAlive())
		
	def ai(self):
		return self.where(lambda p: not player(p).isHuman())
		
	def without(self, exceptions):
		if not isinstance(exceptions, (list, set, Players)):
			exceptions = [exceptions]
		return self.where(lambda p: p not in [player(e).getID() for e in exceptions])
		
	def cities(self):
		return sum([cities.owner(p) for p in self.entities()], Cities([]))
		
	def novassal(self):
		return self.where(lambda p: not team(p).isAVassal())
		
		
class CreatedUnits(object):

	def __init__(self, units):
		self._units = units
		
	def __len__(self):
		return len(self._units)
		
	def __iter__(self):
		return iter(self._units)
		
	def adjective(self, adjective):
		if not adjective:
			return self
	
		for unit in self._units:
			unit.setName('%s %s' % (text(adjective), unit.getName()))
			
		return self
			
	def experience(self, iExperience):
		if iExperience <= 0:
			return self
	
		for unit in self._units:
			unit.changeExperience(iExperience, 100, False, False, False)
			
		return self
		
	def one(self):
		if len(self._units) == 1:
			return self._units[0]
		raise Exception('Can only return one unit if it is a single created unit')
		
		
class DefaultDict(dict):

	def __init__(self, dictionary, default):
		self._default = default
		self.update(dictionary)
		
	def __getitem__(self, key):
		if not key in self:
			super(DefaultDict, self).__setitem__(key, copy(self._default))
		return super(DefaultDict, self).__getitem__(key)

		
class Turn(int):

	def __new__(cls, value, *args, **kwargs):
		return super(cls, cls).__new__(cls, value)
		
	def __add__(self, other):
		return self.__class__(super(Turn, self).__add__(other))
		
	def __sub__(self, other):
		return self.__class__(super(Turn, self).__sub__(other))
		
	def between(self, start, end):
		return turn(start) <= self <= turn(end)
		
	def deviate(self, variation, seed = None):
		variation = turns(variation)
		if seed:
			return self + seed % (2 * variation) - variation
		return self + rand(2 * variation) - variation
		

class Infos:

	def type(self, string):
		type = gc.getInfoTypeForString(string)
		if type < 0:
			raise ValueError("Type for '%s' does not exist" % string)
		return type
		
	def constant(self, string):
		return gc.getDefineINT(string)

	def civ(self, identifier):
		if isinstance(identifier, (CyTeam, CyPlayer, CyPlot, CyCity, CyUnit)):
			return gc.getCivilizationInfo(civ(identifier))
	
		return gc.getCivilizationInfo(identifier)
		
	def religion(self, iReligion):
		return gc.getReligionInfo(iReligion)
		
	def gameSpeed(self, iGameSpeed = None):
		if iGameSpeed is None:
			iGameSpeed = game.getGameSpeedType()
		return gc.getGameSpeedInfo(iGameSpeed)
		
	def unit(self, identifier):
		if isinstance(identifier, CyUnit):
			return gc.getUnitInfo(identifier.getUnitType())
			
		if isinstance(identifier, int):
			return gc.getUnitInfo(identifier)
			
		raise TypeError("Expected identifier to be CyUnit or unit type ID, got '%s'" % type(identifier))
		
	def feature(self, identifier):
		if isinstance(identifier, CyPlot):
			return gc.getFeatureInfo(identifier.getFeatureType())
			
		if isinstance(identifier, int):
			return gc.getFeatureInfo(identifier)
			
		raise TypeError("Expected identifier to be CyPlot or feature type ID, got '%s'" % type(identifier))
		
	def tech(self, iTech):
		return gc.getTechInfo(iTech)
		
	def bonus(self, identifier):
		if isinstance(identifier, CyPlot):
			return gc.getBonusInfo(identifier.getBonusType(-1))
			
		if isinstance(identifier, int):
			return gc.getBonusInfo(identifier)
			
		raise TypeError("Expected identifier to be CyPlot or bonus type ID, got '%s'" % type(identifier))
		
	def handicap(self):
		return gc.getHandicapInfo(game.getHandicapType())
		
	def corporation(self, identifier):
		return gc.getCorporationInfo(identifier)
		
	def building(self, identifier):
		return gc.getBuildingInfo(identifier)
		
	def art(self, string):
		return gc.getInterfaceArtInfo(self.type(string)).getPath()
		
	def commerce(self, identifier):
		return gc.getCommerceInfo(identifier)
		
	def promotions(self):
		return range(gc.getNumPromotionInfos())
		
	def promotion(self, identifier):
		return gc.getPromotionInfo(identifier)
		
	def project(self, identifier):
		return gc.getProjectInfo(identifier)
	
	def leader(self, identifier):
		if isinstance(identifier, CyPlayer):
			return gc.getLeaderHeadInfo(identifier.getLeader())
			
		if isinstance(identifier, int):
			return gc.getLeaderHeadInfo(identifier)
			
		raise TypeError("Expected identifier to be CyPlayer or leaderhead ID, got: '%s'" % type(identifier))
		
	def improvement(self, identifier):
		return gc.getImprovementInfo(identifier)
		
	def buildingClass(self, identifier):
		return gc.getBuildingClassInfo(identifier)
		
	def culture(self, identifier):
		return gc.getCultureLevelInfo(identifier)
	
	def era(self, identifier):
		return gc.getEraInfo(identifier)
		
		
plots = PlotFactory()
cities = CityFactory()
units = UnitFactory()
players = PlayerFactory()
infos = Infos()

plot_ = plot
city_ = city