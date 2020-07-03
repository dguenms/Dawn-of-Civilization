# coding: utf-8

from CvPythonExtensions import *
from Consts import *
from StoredData import *
from DataStructures import *
from Areas import *

from Types import Civ

import Popup
import BugCore

import random

from traceback import extract_stack
from sets import Set


gc = CyGlobalContext()
MainOpt = BugCore.game.MainInterface

interface = CyInterface()
translator = CyTranslator()
game = gc.getGame()
map = gc.getMap()


# TODO: is there a right equal or right not equal to add to Civ so we can do iPlayer == iEgypt and convert iPlayer to Civ implicitly?


def capital(identifier):
	if player(identifier).getNumCities() == 0 or is_minor(identifier):
		return None
		
	city = player(identifier).getCapitalCity()
	
	if not city or city.isNone():
		return None
	
	return city


def barbarian():
	return gc.getBARBARIAN_PLAYER()


def stacktrace():
	print '\n'.join('File "%s", line %d, in %s' % (line[0], line[1], line[2]) for line in extract_stack())


def itemize(iterable, format_func = lambda x: x, item_char = bullet):
	return item_char + (newline + item_char).join(format_func(i) for i in iterable)



def autoplay():
	return year() < year(dSpawn[active()])


class Civics(object):

	def __init__(self, identifier):
		self.iGovernment, self.iLegitimacy, self.iSociety, self.iEconomy, self.iReligion, self.iTerritory = (player(identifier).getCivics(i) for i in range(6))


def civics(identifier):
	return Civics(identifier)


def spread(iterable, size, offset=0):
	if len(iterable) <= size:
		return spread_padded(iterable, size, offset)
	else:
		return spread_grouped(iterable, size, offset)


def spread_padded(iterable, size, offset=0):
	result = [None] * size
	for i, element in enumerate(iterable):
		result[(i * ((size+1) / len(iterable)) + offset) % size] = element
	
	return result


def spread_grouped(iterable, size, offset=0):
	result = [tuple(iterable[j] for j in range(i, len(iterable), size)) for i in range(size)]
	return result[-offset%size:] + result[:-offset%size]


def every(interval):
	return turn() % turns(interval) == 0


def periodic_from(entities, interval=None):
	if interval is None:
		interval = len(entities)
	interval = turns(interval)
	offset = hash(tuple(entities)) + data.iSeed
	entities = spread(entities, interval)
	return entities[(turn() + offset) % interval]


def get_calling_module():
	trace = [call[0] for call in extract_stack() if call[0] != 'Core']
	return trace[-1]


def periodic(interval):
	interval = turns(interval)
	index = period_offsets(interval)
	offset = (index / 2 + ((index + interval) % 2) * interval / 2 ) % interval
	return turn() % interval == offset


def matching(condition, *elements):
	return next(element for element in elements if condition(element))


def direction(tile, direction_type):
	x, y = location(tile)
	return plotDirection(x, y, direction_type)


def weighted_random_entry(weighted_elements):
	elements = []
	for element, weight in weighted_elements.items():
		elements += [element] * weight
	return random_entry(elements)


def at(location1, location2):
	return location(location1) == location(location2)


def isExtendedBirth(iPlayer):
	if player(iPlayer).isHuman(): return False
	
	# add special conditions for extended AI flip zones here
	if civ(iPlayer) == iOttomans and player(iByzantium).isAlive(): return False
	
	return True


def birthRectangle(identifier, extended = None):
	if extended is None: extended = isExtendedBirth(identifier)
	if identifier in dExtendedBirthArea and extended:
		return dExtendedBirthArea[identifier]
	return dBirthArea[identifier]


def log(func):
	def logged_func(*args, **kwargs):
		print "Begin %s" % func.__name__
		result = func(*args, **kwargs)
		print "Complete %s" % func.__name__
		return result
	
	return logged_func


def owner(entity, identifier):
	if isinstance(identifier, Civ):
		return owner(entity, slot(identifier))
	return entity.getOwner() == identifier


def count(iterable, condition):
	return len([x for x in iterable if condition(x)])


def format_separators(list, separator, last_separator, format=lambda x: x):
	separator = separator.rstrip() + ' '
	last_separator = last_separator.rstrip() + ' '

	formatted_list = [str(format(x)) for x in list]

	if len(formatted_list) > 1:
		return last_separator.join([separator.join(formatted_list[:-1]), formatted_list[-1]])
	return last_separator.join(formatted_list)


def slot(iCiv):
	if not isinstance(iCiv, Civ):
		raise TypeError("Can only pass Civ to determine slot, got: %s" % type(iCiv))

	if iCiv in data.dSlots:
		return data.dSlots[iCiv]

	return -1


def emptymap(x = iWorldX, y = iWorldY):
	return Map([[0 for _ in range(x)] for _ in range(y)])


def deeplist(collection):
	if isinstance(collection, tuple):
		return deeplist(list(collection))
	elif isinstance(collection, (list, set)):
		return [deeplist(element) for element in collection]
	return collection


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

		
def eventpopup(id, title, message, labels=[]):
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
	return game.getStartTurn()


def scenarioStartYear():
	lStartYears = [-3000, 600, 1700]
	return lStartYears[scenario()]


def scenario():
	dScenarioStartTurns = {
		0 : i3000BC,
		181 : i600AD,
		321 : i1700AD,
	}
	
	return dScenarioStartTurns[scenarioStartTurn()]


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
	return gc.getCivilizationInfo(civ(iPlayer)).getCivilizationUnits(iUnitClass)


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
		
	return translator.getText(str(key), tuple(encode(f) for f in format))
	
	
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
	if not location1 or not location2:
		return map.maxStepDistance()
	
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
		iRight = iLeft
		iLeft = 0
		
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
	return [x for x in list if x is not None]
	
	
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
	return UnitKey(unit)
	

def team(identifier = None):
	if identifier is None:
		return gc.getTeam(gc.getActivePlayer().getTeam())

	if isinstance(identifier, CyTeam):
		return identifier
		
	if isinstance(identifier, (CyPlayer, CyUnit, CyCity, CyPlot)):
		return gc.getTeam(identifier.getTeam())
		
	if isinstance(identifier, Civ):
		iPlayer = slot(identifier)
		if iPlayer < 0: return NullTeam()
		return gc.getTeam(gc.getPlayer(iPlayer).getTeam())
		
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
	
	if isinstance(identifier, Civ):
		iPlayer = slot(identifier)
		if iPlayer < 0: return NullPlayer()
		return gc.getPlayer(iPlayer)
		
	if isinstance(identifier, int):
		if identifier < 0: 
			return None
		return gc.getPlayer(identifier)
		
	raise TypeError("Expected identifier to be CyPlayer, CyTeam, CyPlot, CyCity, CyUnit, or int, received '%s'" % type(identifier))
	

def civ(identifier = None):
	if identifier is None:
		return Civ(game.getActiveCivilizationType())

	if isinstance(identifier, Civ):
		return identifier

	if isinstance(identifier, (CyPlayer, CyUnit)):
		return Civ(identifier.getCivilizationType())
		
	if isinstance(identifier, CyPlot):
		if not identifier.isOwned():
			return NoCiv
		return civ(identifier.getOwner())

	return Civ(player(identifier).getCivilizationType())


def civs(*iterable):
	return [civ(element) for element in iterable]


def period(iCiv):
	iPlayer = slot(iCiv)
	if iPlayer >= 0:
		return player(iPlayer).getPeriod()
	return -1
	
	
def active():
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
		try:
			self._keys = list(keys)
		except Exception, e:
			raise Exception("%s: %s" % (e, type(keys)))
		
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
	
	def empty(self):
		return self.__class__([])
	
	def sample(self, iSampleSize):
		if not self: return self.empty()
		iSampleSize = min(iSampleSize, len(self))
		if iSampleSize <= 0: return self.empty()
		return self.__class__(random.sample(self._keys, iSampleSize))
		
	def buckets(self, *conditions):
		rest = lambda e: not any(condition(e) for condition in conditions)
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
		if len(keys) == 1:
			if isinstance(keys[0], type(self)):
				keys = keys[0]._keys
			elif isinstance(keys[0], list):
				keys = keys[0]
		combined = list(keys) + list(self._keys)
		return self.__class__(sorted(set(combined), key=combined.index))
		
	def limit(self, iLimit):
		try:
			return self.__class__(self._keys[:iLimit])
		except TypeError, e:
			raise TypeError("%s, was: %s" % (e, iLimit))
	
	def count(self, condition = lambda x: True):
		return count(self, condition)
		
	def maximum(self, metric):
		return find_max(self.entities(), metric).result
		
	def minimum(self, metric):
		return find_min(self.entities(), metric).result
		
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

	def periodic(self, iInterval):
		return periodic_from(self.entities(), iInterval)
	
	def periodic_iter(self, iInterval):
		element = self.periodic(iInterval)
		if element is None:
			return ()
		elif isinstance(element, tuple):
			return element
		else:
			return (element,)

	def divide(self, keys):
		shuffled_entities = self.shuffle().entities()
		return [(key, [entity for j, entity in enumerate(shuffled_entities) if j % len(keys) == i]) for i, key in enumerate(keys)]
	
	def index(self, key):
		return self.entities().index(key)

class PlotsCorner:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def end(self, *args):
		x, y = _parse_tile(*args)
		return Plots([(i, j) for i in range(min(self.x, x), min(max(self.x, x)+1, iWorldX)) for j in range(min(self.y, y), min(max(self.y, y)+1, iWorldY))])
	

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
		
	def surrounding(self, *args, **kwargs):
		radius = retrieve(kwargs, 'radius', 1)
		if radius < 0: raise ValueError("radius cannot be negative, received: '%d'" % radius)
		x, y = _parse_tile(*args)
		if not isinstance(x, int): raise Exception("x must be int, is %s" % type(x))
		if not isinstance(y, int): raise Exception("y must be int, is %s" % type(y))
		return Plots(sort(list(set(wrap(x+i, y+j) for i in range(-radius, radius+1) for j in range(-radius, radius+1)))))
		
	def ring(self, *args, **kwargs):
		radius = retrieve(kwargs, 'radius', 1)
		circle = self.surrounding(*args, **kwargs)
		inside = self.surrounding(*args, **{'radius': radius-1})
		return circle.without(inside)
	
	def city_radius(self, city):
		if not city or city.isNone():
			raise TypeError("city object is None")
	
		return Plots([location(city.getCityIndexPlot(i)) for i in range(21)])

	def owner(self, iPlayer):
		return self.all().owner(iPlayer)

	def area(self, dArea, dExceptions, identifier):
		return self.rectangle(*dArea[identifier]).without(dExceptions[identifier])

	def birth(self, identifier, extended=None):
		if extended is None: extended = isExtendedBirth(identifier)
		if identifier in dExtendedBirthArea and extended:
			return self.area(dExtendedBirthArea, dBirthAreaExceptions, identifier)
		return self.area(dBirthArea, dBirthAreaExceptions, identifier)

	def core(self, identifier):
		iPeriod = player(identifier).getPeriod()
		if iPeriod in dPeriodCoreArea:
			return self.area(dPeriodCoreArea, dPeriodCoreAreaExceptions, iPeriod)
		return self.area(dCoreArea, dCoreAreaExceptions, identifier)

	def normal(self, identifier):
		iPeriod = player(identifier).getPeriod()
		if iPeriod in dPeriodNormalArea:
			return self.area(dPeriodNormalArea, dPeriodNormalAreaExceptions, iPeriod)
		return self.area(dNormalArea, dNormalAreaExceptions, identifier)

	def broader(self, identifier):
		iPeriod = player(identifier).getPeriod()
		if iPeriod in dPeriodBroaderArea:
			return self.rectangle(*dPeriodBroaderArea[identifier])
		return self.rectangle(*dBroaderArea[identifier])

	def respawn(self, identifier):
		if identifier in dRespawnArea:
			return self.rectangle(*dRespawnArea[identifier])
		return self.normal(identifier)
	
	def capital(self, identifier):
		iPeriod = player(identifier).getPeriod()
		if iPeriod in dPeriodCapitals:
			return plot(dPeriodCapitals[iPeriod])
		return plot(dCapitals[identifier])
		
	def respawnCapital(self, identifier):
		if identifier in dRespawnCapitals:
			return plot(dRespawnCapitals[identifier])
		return self.capital(identifier)
		
	def newCapital(self, identifier):
		if identifier in dNewCapitals:
			return plot(dNewCapitals[identifier])
		return self.respawnCapital(identifier)


class Locations(EntityCollection):


	def __init__(self, locations):
		super(Locations, self).__init__(locations)
		
	def without(self, *exceptions):
		if not exceptions or not any(exceptions):
			return self
			
		if len(exceptions) == 1 and isinstance(exceptions[0], (list, set, Locations)):
			exceptions = exceptions[0] 
	
		return self.where(lambda loc: location(loc) not in [location(e) for e in exceptions])
		
	def _closest(self, *args):
		x, y = _parse_tile(*args)
		return find_min(self.entities(), lambda loc: distance(loc, (x, y)))
		
	def closest(self, *args):
		return self._closest(*args).result
		
	def closest_distance(self, *args):
		return self._closest(*args).value
		
	def units(self):
		return sum([units.at(loc) for loc in self.entities()], Units([]))
	
	def owner(self, iPlayer):
		return self.where(lambda loc: owner(loc, iPlayer))
	
	def notowner(self, iPlayer):
		return self.where(lambda loc: not owner(loc, iPlayer))
	
	def regions(self, *regions):
		return self.where(lambda loc: loc.getRegionID() in regions)
	
	def region(self, iRegion):
		return self.regions(iRegion)
		
	def where_surrounding(self, condition, radius=1):
		return self.where(lambda loc: plots.surrounding(loc, radius=radius).all(condition))
	
	def owners(self):
		return Players(set(loc.getOwner() for loc in self.entities() if loc.getOwner() >= 0))
	
	


class Plots(Locations):

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
	
	def land(self):
		return self.where(lambda p: not p.isWater())
	
	def water(self):
		return self.where(lambda p: p.isWater())
		
	def core(self, iPlayer):
		return self.where(lambda p: p.isCore(iPlayer))
		
	def passable(self):
		return self.where(lambda p: not p.isImpassable())
		
	def lake(self):
		return self.where(lambda p: p.isLake())
	
	def sea(self):
		return self.water().where(lambda p: not p.isLake())

		
class CitiesCorner:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def end(self, *args):
		x, y = _parse_tile(*args)
		return PlotsCorner(self.x, self.y).end(x, y).cities()
		
		
class CityFactory:

	def __init__(self):
		self.plots = PlotFactory()

	def owner(self, identifier):
		owner = player(identifier)
		cities = _iterate(owner.firstCity, owner.nextCity, location)
		return Cities(cities)
		
	def all(self):
		cities = []
		for iPlayer in players.all():
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
		return self.plots.regions(*regions).cities()
		
	def region(self, iRegion):
		return self.regions(iRegion)
		
	def of(self, list):
		return self.plots.of(list).cities()
		
	def surrounding(self, *args, **kwargs):
		return self.plots.surrounding(*args, **kwargs).cities()

	def birth(self, identifier, extended = None):
		return self.plots.birth(identifier, extended).cities()

	def core(self, identifier):
		return self.plots.core(identifier).cities()

	def normal(self, identifier):
		return self.plots.normal(identifier).cities()

	def broader(self, identifier):
		return self.plots.broader(identifier).cities()

	def respawn(self, identifier):
		return self.plots.respawn(identifier).cities()
	
	def capital(self, identifier):
		return city(self.plots.capital(identifier))
		
	def respawnCapital(self, identifier):
		return city(self.plots.respawnCapital(identifier))
		
	def newCapital(self, identifier):
		return city(self.plots.newCapital(identifier))


class Cities(Locations):

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
		
	def religion(self, iReligion):
		return self.where(lambda city: city.isHasReligion(iReligion))
	
	def corporation(self, iCorporation):
		return self.where(lambda city: city.isHasCorporation(iCorporation))
	
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
			
		return Units([unit_key(plot(*args).getUnit(i)) for i in range(plot(*args).getNumUnits())])
		
		
class UnitKey:

	def __init__(self, unit):
		self.owner = unit.getOwner()
		self.id = unit.getID()
		self.x = unit.getX()
		self.y = unit.getY()
		
	def __eq__(self, other):
		return isinstance(other, UnitKey) and (self.owner, self.id) == (other.owner, other.id)
		
	def __str__(self):
		return str((self.owner, self.id))
		
	def __nonzero__(self):
		return self.x >= 0 and self.y >= 0
		
	@classmethod
	def of(cls, unit):
		if isinstance(unit, cls):
			return unit
		return cls(unit)
		
		
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
		return self.where(lambda u: owner(u, iPlayer))

	def notowner(self, iPlayer):
		return self.where(lambda u: not owner(u, iPlayer))
		
	def type(self, iUnitType):
		return self.where(lambda u: u.getUnitType() == iUnitType)
		
	def by_type(self):
		return dict([(iType, self.type(iType)) for iType in set([unit.getUnitType() for unit in self])])
		
	def atwar(self, iPlayer):
		return self.where(lambda u: team(iPlayer).isAtWar(u.getTeam()))
		
	def domain(self, iDomain):
		return self.where(lambda u: u.getDomainType() == iDomain)
	

class PlayerFactory:

	def all(self):
		return Players(range(gc.getMAX_PLAYERS()))
		
	def major(self):
		return self.all().where(lambda p: not is_minor(p))
		
	def minor(self):
		return self.all().where(lambda p: is_minor(p))
		
	def civs(self, *civs):
		return self.all().where(lambda p: civ(p) in civs)
		
	def independent(self):
		return self.civs(iIndependent, iIndependent2)
		
	def barbarian(self):
		return self.civs(iBarbarian)
		
	def native(self):
		return self.civs(iNative)
		
	def vassals(self, iPlayer):
		return self.all().where(lambda p: team(p).isVassal(player(iPlayer).getTeam()))
		
	def none(self):
		return Players([])
	
	def of(self, *players):
		return Players(players)
	
	def at_war(self, iPlayer):
		return self.all().at_war(iPlayer)

		
class Players(EntityCollection):

	def __init__(self, players):
		super(Players, self).__init__(players)

	def __contains__(self, item):
		if isinstance(item, CyPlayer):
			return item.getID() in self._keys
			
		if isinstance(item, Civ):
			return item in [civ(p) for p in self._keys]
			
		if isinstance(item, int):
			return item in self._keys
			
		raise TypeError("Tried to check if Players contains '%s', can only check CyPlayer, player or civilization IDs" % type(item))
		
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

	def human(self):
		return self.where(lambda p: player(p).isHuman())
		
	def without(self, exceptions):
		if not isinstance(exceptions, (list, set, Players)):
			exceptions = [exceptions]
		return self.where(lambda p: p not in [player(e).getID() for e in exceptions])
		
	def cities(self):
		return sum([cities.owner(p) for p in self.entities()], Cities([]))
		
	def novassal(self):
		return self.where(lambda p: not team(p).isAVassal())
	
	def past_birth(self):
		return self.where(lambda p: year() >= year(dBirth[p]))
		
	def before_birth(self):
		return self.where(lambda p: year() < year(dBirth[p]))

	def civs(self, *civs):
		return self.where(lambda p: civ(p) in civs)
	
	def civ(self, iCiv):
		return self.civs(iCiv)
		
	def barbarian(self):
		return self.including(players.barbarian())
		
	def independent(self):
		return self.including(players.independent())
		
	def native(self):
		return self.including(players.native())
	
	def permutations(self, identical=False):
		return Players([(x, y) for x, y in permutations(self._keys, self._keys) if (identical and x == y) or x < y])
		
	def asCivs(self):
		return [civ(p) for p in self.entities()]
	
	def tech(self, iTech):
		return self.where(lambda p: team(p).isHasTech(iTech))
	
	def at_war(self, iPlayer):
		return self.where(lambda p: team(iPlayer).isAtWar(player(p).getTeam()))
		
		
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


class InfoCollection(EntityCollection):

	@staticmethod
	def type(infoClass, iNumInfos):
		return InfoCollection(range(iNumInfos), infoClass)

	def __init__(self, infos, infoClass):
		super(InfoCollection, self).__init__(infos)
		self.info_class = infoClass
		
	def where(self, condition):
		return self.__class__([k for k in self._keys if condition(self._factory(k))], self.info_class)
	
	def __contains__(self, item):
		return item in self._keys
	
	def __str__(self):
		return ','.join([self._factory(i).getText() for i in self])
		
	def _factory(self, key):
		return self.info_class(key)
	
	def entities(self):
		return self._keys
		

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
	
	def techs(self):
		return InfoCollection.type(gc.getTechInfo, iNumTechs)
		
	def bonus(self, identifier):
		if isinstance(identifier, CyPlot):
			return gc.getBonusInfo(identifier.getBonusType(-1))
			
		if isinstance(identifier, int):
			return gc.getBonusInfo(identifier)
			
		raise TypeError("Expected identifier to be CyPlot or bonus type ID, got '%s'" % type(identifier))
		
	def handicap(self):
		return gc.getHandicapInfo(game.getHandicapType())
		
	def corporations(self):
		return InfoCollection.type(gc.getCorporationInfo, iNumCorporations)
		
	def corporation(self, identifier):
		return gc.getCorporationInfo(identifier)
		
	def building(self, identifier):
		return gc.getBuildingInfo(identifier)
		
	def art(self, string):
		return gc.getInterfaceArtInfo(self.type(string)).getPath()
		
	def commerce(self, identifier):
		return gc.getCommerceInfo(identifier)
		
	def promotions(self):
		return InfoCollection.type(gc.getPromotionInfo, gc.getNumPromotionInfos())
		
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


class Map(object):

	def __init__(self, map):
		if isinstance(map, tuple):
			map = deeplist(map)
	
		if not isinstance(map, list):
			raise ValueError("Map argument must be list, was %s" % type(map))
		
		self.height = len(map)
		
		if self.height == 0:
			raise ValueError("Map may not be empty")
			
		self.width = len(map[0])
		
		if not all(len(row) == self.width for row in map):
			raise ValueError("All rows in the map must be of the same width")
		
		self.map = map
		
	def __getitem__(self, (x, y)):
		return self.map[self.height-1-y][x]
		
	def __setitem__(self, (x, y), value):
		self.map[self.height-1-y][x] = value
		
	def __iter__(self):
		for x in range(self.width):
			for y in range(self.height):
				yield (x, y), self[x, y]
	
	def apply(self, map, (originX, originY) = (0, 0)):
		if not isinstance(map, Map):
			raise ValueError("Can only apply another Map")
		
		for (x, y), value in map:
			self[originX + x, originY + y] = value


class PeriodOffsets(object):

	def __init__(self):
		self.turn = 0
		self.offsets = defaultdict({}, 0)
		
	def __call__(self, interval):
		self._check_invalidate()
		calling = get_calling_module()
		offset = self.offsets[(calling, interval)]
		self.offsets[(calling, interval)] += 1
		return offset
		
	def _check_invalidate(self):
		if turn() > self.turn:
			self._invalidate()
	
	def _invalidate(self):
		self.turn = turn()
		self.offsets = defaultdict({}, 0)


class TechFactory(object):

	def of(self, *techs):
		return TechCollection().including(*techs)

	def era(self, iEra):
		return TechCollection().era(iEra)
		
	def column(self, iColumn):
		return TechCollection().column(iColumn)


class TechCollection(object):

	def __init__(self):
		self.included = []
		self.excluded = []
		self.iEra = -1
		self.iColumn = 0
	
	def era(self, iEra):
		self.iEra = iEra
		return self
	
	def column(self, iColumn):
		self.iColumn = iColumn
		return self
	
	def without(self, *techs):
		self.excluded += [i for i in techs if i not in self.excluded]
		return self
	
	def including(self, *techs):
		self.included += [i for i in techs if i not in self.included]
		return self
		
	def techs(self):
		techs = [i for i in infos.techs().where(lambda tech: tech.getEra() <= self.iEra or tech.getGridX() <= self.iColumn)]
		techs += [i for i in self.included if i not in techs]
		techs = [i for i in techs if i not in self.excluded]
		
		return techs
	
	def __iter__(self):
		return iter(self.techs())
		
		
plots = PlotFactory()
cities = CityFactory()
units = UnitFactory()
players = PlayerFactory()
techs = TechFactory()
infos = Infos()
period_offsets = PeriodOffsets()

plot_ = plot
city_ = city