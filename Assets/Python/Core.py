# coding: utf-8

from CvPythonExtensions import *
from Consts import *
from StoredData import *
from DataStructures import *
from Areas import *

from CoreTypes import Civ

import Popup
import BugCore

import random
import re
import types

from sets import Set
from itertools import groupby
from datetime import datetime

from BugEventManager import g_eventManager as events


gc = CyGlobalContext()
MainOpt = BugCore.game.MainInterface

interface = CyInterface()
translator = CyTranslator()
engine = CyEngine()
game = gc.getGame()
map = gc.getMap()


def civ_name(iCiv):
	return infos.civ(iCiv).getShortDescription(0).replace(" ", "_")


def getArea(area):
	if isinstance(area, (CyPlot, CyCity)):
		return area.getArea()
	elif isinstance(area, CyUnit):
		return getArea(plot(area))
	elif isinstance(area, tuple) and len(area) == 2:
		return plot(area).getArea()
	return area


def mission(unit, iMission, data=(-1, -1), iFlags=0, bAppend=False, bManual=False, iMissionAI=MissionAITypes.NO_MISSIONAI, missionAIPlot=None, missionAIUnit=None):
	data = listify(data) + [-1] * 2
	iData1, iData2 = tuple(data[:2])
	
	if missionAIPlot is not None:
		missionAIPlot = plot(missionAIPlot)
	
	unit.getGroup().pushMission(iMission, iData1, iData2, iFlags, bAppend, bManual, iMissionAI, missionAIPlot, missionAIUnit)


def current_time():
	return datetime.now().strftime("%d/%m/%Y, %H:%M:%S")


def unique(iterable):
	return [key for key, value in groupby(iterable)]


def until(iTurn):
	return iTurn - turn()


def since(iTurn):
	return turn() - iTurn


def getPlayerExperience(unit):
	if not unit.canFight():
		return 0

	iExperience = player(unit).getFreeExperience() + player(unit).getDomainFreeExperience(unit.getDomainType())
	
	if player(unit).isStateReligion():
		iExperience += player(unit).getStateReligionFreeExperience()
	
	return iExperience
	
	
def format_date(year):
	return text(year >= 0 and "TXT_KEY_YEAR_AD" or "TXT_KEY_YEAR_BC", abs(year))


def duplefy(*items):
	if len(items) == 2:
		return (items[0], items[1])
	elif len(items) == 1:
		return items[0]
	raise Exception("Excepted 2 or less values, got: %s" % (items,))


def variadic(*items):
	if len(items) == 1:
		if isinstance(items[0], types.GeneratorType):
			return items[0]
		return listify(items[0])
	return listify(items)


def listify(item):
	if isinstance(item, list):
		return item
	if isinstance(item, (tuple, set)):
		return list(item)
	if isinstance(item, types.GeneratorType):
		return [x for x in item]
	if item is None:
		return []
	return [item]


def concat(*lists):
	return sum((listify(list) for list in lists), [])


def isWonder(iBuilding):
	return isWorldWonderClass(infos.building(iBuilding).getBuildingClassType())


def log_with_trace(context):
	print "%s called near:" % context
	stacktrace()


# TODO: is there a right equal or right not equal to add to Civ so we can do iPlayer == iEgypt and convert iPlayer to Civ implicitly?


def sign(x):
	if x > 0: return 1
	elif x < 0: return -1
	else: return 0


def capital(identifier):
	if identifier is None:
		raise ValueError("identifier cannot be None")

	if player(identifier).getNumCities() == 0 or is_minor(identifier):
		return None
		
	city = player(identifier).getCapitalCity()
	
	if not city or city.isNone():
		return None
	
	return city


def barbarian():
	return gc.getBARBARIAN_PLAYER()
	
	
def called_from():
	previous_line = extract_stack()[-3]
	return 'File "%s", line %d, in %s' % (previous_line[0], previous_line[1], previous_line[2])


def stacktrace():
	print '\n'.join('File "%s", line %d, in %s' % (line[0], line[1], line[2]) for line in extract_stack())


def itemize(iterable, format_func = lambda x: x, item_char = bullet):
	return item_char + (newline + item_char).join(format_func(i) for i in iterable)


def autoplay():
	return year() < year(dBirth[active()])


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


def periodic(interval):
	interval = turns(interval)
	index = data.period_offsets(interval)
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
	if civ(iPlayer) == iOttomans and player(iByzantium).isExisting(): return False
	
	return True


def birthRectangle(identifier, extended = None):
	if extended is None: extended = isExtendedBirth(identifier)
	if identifier in dExtendedBirthArea and extended:
		return dExtendedBirthArea[identifier]
	return dBirthArea[identifier]


def signature(func, *args, **kwargs):
	return signature_name(func.__name__, *args, **kwargs)
	
	
def signature_name(func_name, *args, **kwargs):
	formatted_args = [str(arg) for arg in args]
	formatted_kwargs = ["%s=%s" % (key, value) for key, value in kwargs.items()]
	return "%s(%s)" % (func_name, ", ".join(formatted_args + formatted_kwargs))


def log(func):
	def logged_func(*args, **kwargs):
		print "Begin %s" % signature(func, *args, **kwargs)
		result = func(*args, **kwargs)
		print "Complete %s" % func.__name__
		return result
	
	return logged_func


def owner(entity, identifier):
	if isinstance(identifier, Civ):
		return owner(entity, slot(identifier))
	return entity.getOwner() == identifier


def count(iterable, condition = bool):
	return len([x for x in iterable if condition(x)])


def format_separators(list, separator, last_separator, format=lambda x: x):
	separator = separator.rstrip() + ' '
	last_separator = last_separator.rstrip() + ' '
	
	def ascii_format(item):
		formatted = format(item)
		if isinstance(formatted, (str, unicode)):
			return formatted.encode("ascii", "xmlcharrefreplace")
		return str(formatted)

	formatted_list = [ascii_format(item) for item in list]

	if len(formatted_list) > 1:
		return last_separator.join([separator.join(formatted_list[:-1]), formatted_list[-1]])
	return last_separator.join(formatted_list)


def slot(iCiv):
	if not isinstance(iCiv, Civ):
		raise TypeError("Can only pass Civ to determine slot, got: %s of %s" % (iCiv, type(iCiv)))

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
	
	elif isinstance(skip_city, CyPlot):
		skip_city = skip_city.isCity() and city_(skip_city) or CyCity()
	
	if isinstance(owner, Civ):
		owner = slot(owner)
			
	x, y = _parse_tile(entity)
	city = map.findCity(x, y, owner, TeamTypes.NO_TEAM, same_continent, coastal_only, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, skip_city)
	
	if city.isNone():
		return None
	return city


def specialbuilding(iType, iReligion):
	return next(iBuilding for iBuilding in range(iNumBuildings) if infos.building(iBuilding).getSpecialBuildingType() == iType and infos.building(iBuilding).getReligionType() == iReligion)
	
	
def temple(iReligion):
	return specialbuilding(infos.type('SPECIALBUILDING_TEMPLE'), iReligion)
	
	
def monastery(iReligion):
	return specialbuilding(infos.type('SPECIALBUILDING_MONASTERY'), iReligion)
	
	
def cathedral(iReligion):
	return specialbuilding(infos.type('SPECIALBUILDING_CATHEDRAL'), iReligion)


def shrine(iReligion):
	return next(iBuilding for iBuilding in range(iNumBuildings) if infos.building(iBuilding).getGlobalReligionCommerce() == iReligion)


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


def none(iterable):
	return not any(iterable)
	
	
def next(iterator, default = None):
	iterator = iter(iterator)
	try:
		return iterator.next()
	except StopIteration, e:
		return default


def message(iPlayer, key, *format, **settings):
	iColor = settings.get('color', iWhite)
	iEvent = settings.get('event', 0)
	iButton = settings.get('button', '')
	
	sound = settings.get('sound', '')
	force = settings.get('force', False)
	
	tile = settings.get('location')
	iX, iY = -1, -1
	if tile:
		iX, iY = location(tile)
	
	interface.addMessage(iPlayer, force, iDuration, translator.getText(key, format), sound, iEvent, iButton, ColorTypes(iColor), iX, iY, True, True)


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
	popup.launch(not labels)


def stability(identifier):
	return data.players[identifier].iStabilityLevel


def has_civic(identifier, iCivic):
	return player(identifier).getCivics(gc.getCivicInfo(iCivic).getCivicOptionType()) == iCivic


def scenarioStart():
	return turn() == scenarioStartTurn()


def scenarioStartTurn():
	return getTurnForYear(scenarioStartYear())


def scenarioStartYear():
	lStartYears = [-3000, 600, 1700]
	return lStartYears[scenario()]


def scenario():
	return map.getScenario()


def unittype(identifier):
	if isinstance(identifier, CyUnit):
		return identifier.getUnitType()
		
	if isinstance(identifier, int):
		return identifier
		
	raise TypeError("Expected unit type to be CyUnit or int, received: '%s'" % type(identifier))


def base_building(iBuilding):
	if iBuilding is None:
		return iBuilding

	return gc.getBuildingClassInfo(gc.getBuildingInfo(iBuilding).getBuildingClassType()).getDefaultBuildingIndex()


def base_unit(iUnit):
	return gc.getUnitClassInfo(gc.getUnitInfo(unittype(iUnit)).getUnitClassType()).getDefaultUnitIndex()


def unique_building_from_class(identifier, iBuildingClass):
	return gc.getCivilizationInfo(civ(identifier)).getCivilizationBuildings(iBuildingClass)


def unique_building(identifier, iBuilding):
	if not player(identifier): return base_building(iBuilding)
	return unique_building_from_class(identifier, gc.getBuildingInfo(iBuilding).getBuildingClassType())


def unique_unit_from_class(identifier, iUnitClass):
	return gc.getCivilizationInfo(civ(identifier)).getCivilizationUnits(iUnitClass)


def unique_unit(identifier, iUnit):
	if not player(identifier): return base_unit(iUnit)
	return unique_unit_from_class(identifier, gc.getUnitInfo(unittype(iUnit)).getUnitClassType())


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
	if not game.isFinalInitialized():
		return iTurns

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
	return infos.units().where(lambda iUnit: infos.unit(iUnit).getReligionSpreads(iReligion) > 0).first()


def makeUnit(iPlayer, iUnit, plot, iUnitAI = UnitAITypes.NO_UNITAI):
	return makeUnits(iPlayer, iUnit, plot, 1, iUnitAI).one()


def makeUnits(iPlayer, iUnit, plot, iNumUnits = 1, iUnitAI = UnitAITypes.NO_UNITAI):
	if iNumUnits <= 0:
		return CreatedUnits([])
	
	if iUnit < 0:
		raise Exception("Invalid unit")

	x, y = location(plot)
	
	units = []
	for _ in range(iNumUnits):
		unit = player(iPlayer).initUnit(iUnit, x, y, iUnitAI, DirectionTypes.DIRECTION_SOUTH)
		unit.changeExperience(getPlayerExperience(unit), -1, False, False, False)
		unit.testPromotionReady()
		units.append(unit)
		events.fireEvent("unitCreated", unit)

	return CreatedUnits(units)


def encode(text):
	if isinstance(text, (str, unicode)):
		return str(text.encode('utf-8'))
	return text


def text(key, *format):
	return translator.getText(str(key), tuple(format))
	
	
def text_if_exists(key, *format, **kwargs):
	otherwise = kwargs.get('otherwise')
	key_text = text(key, *format)
	if key_text != key:
		return key_text
	elif otherwise:
		return text(otherwise, *format)
	return ''


def debug(message, *format):
	if MainOpt.isShowDebugPopups():
		show(message, *format)


def show(message, *format):
	if format:
		message = message % tuple(format)

	popup = Popup.PyPopup()
	popup.setBodyString(message)
	popup.launch()


def distance(location1, location2):
	if not location1 or not location2:
		return map.maxStepDistance()
	
	x1, y1 = _parse_tile(location1)
	x2, y2 = _parse_tile(location2)
	return stepDistance(x1, y1, x2, y2)
	

# TOOD: test
def real_distance(location1, location2):
	if not location1 or not location2:
		return map.maxPlotDistance()
	
	x1, y1 = _parse_tile(location1)
	x2, y2 = _parse_tile(location2)
	return plotDistance(x1, y1, x2, y2)
	
	
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


def dict_max(dict):
	if not dict:
		return None
	return sort(dict.items(), lambda item: item[1], True)[0][0]


def rand(iLeft, iRight = None):
	if iRight is None:
		iRight = iLeft
		iLeft = 0
		
	return iLeft + gc.getGame().getSorenRandNum(iRight - iLeft, 'random number')


def chance(iPercentage):
	return rand(100) <= iPercentage
	
	
def random_entry(iterable):
	if not iterable:
		return None
		
	return iterable[rand(len(iterable))]
	

def name(identifier):
	if identifier is None:
		raise ValueError("identifier cannot be None")
	return player(identifier).getCivilizationShortDescription(0)
	

def fullname(identifier):
	if identifier is None:
		raise ValueError("identifier cannot be None")
	return player(identifier).getCivilizationDescription(0)


def adjective(identifier):
	if identifier is None:
		raise ValueError("identifier cannot be None")
	return player(identifier).getCivilizationAdjective(0)


def _parse_tile(*args):
	if len(args) == 2:
		return args
	elif len(args) == 1:
		if isinstance(args[0], tuple) and len(args[0]) == 2:
			return args[0]
		elif isinstance(args[0], (CyPlot, CyCity, CyUnit)):
			if args[0].isNone() or args[0].getX() < 0 or args[0].getY() < 0:
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
	if len(args) == 1 and isinstance(args[0], CyCity):
		return args[0]

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
		return None

	if isinstance(entity, (CyPlot, CyCity, CyUnit)):
		return entity.getX(), entity.getY()

	return _parse_tile(entity)
	

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
	
	def _keyify(self, item):
		return item

	def __init__(self, keys):
		self._keys = list(keys)
		self._name = ""
		
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
		if other is None:
			return False
		if not isinstance(other, type(self)):
			return False
		return self._keys == other._keys
			
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
		
	def copy(self, keys):
		return self.__class__(list(keys)).clear_named(self.name())
		
	def same(self, other):
		if isinstance(other, type(self)):
			return set(self._keys) == set(other._keys)
		raise TypeError("Cannot compare '%s' and '%s'" % (type(self), type(other)))

	def entities(self):
		return [self._factory(k) for k in self._keys]
		
	def where(self, condition):
		return self.copy(k for k in self._keys if condition(self._factory(k)))
		
	def any(self, condition = None):
		if condition is None: return bool(self)
		return bool(self.where(condition))
		
	def all(self, condition):
		return not self.any(negate(condition))
		
	def none(self, condition = None):
		return not self.any(condition)
	
	def all_if_any(self, condition):
		return self.any() and self.all(condition)
		
	def random(self):
		return random_entry(self.entities())
		
	def get(self, function = lambda x: x):
		return [function(e) for e in self.entities()]
		
	def first(self):
		if not self: return None
		return self.entities()[0]
	
	def last(self):
		if not self: return None
		return self.entities()[self.count()-1]
		
	def one(self):
		if len(self) != 1:
			raise Exception("Only excepted one element in %s, but got: %s" % (type(self), str(self)))
		return self.first()
	
	def empty(self):
		return self.copy([])
	
	def sample(self, iSampleSize):
		if not self: return self.empty()
		iSampleSize = min(iSampleSize, len(self))
		if iSampleSize <= 0: return self.empty()
		return self.copy(random.sample(self._keys, iSampleSize))
		
	def buckets(self, *conditions):
		rest = lambda e: not any(condition(e) for condition in conditions)
		buckets = [self.where(condition) for condition in conditions]
		buckets.append(self.where(rest))
		return tuple(buckets)
		
	def split(self, condition):
		return self.buckets(condition)
	
	def percentage_split(self, iPercent):
		iSplit = self.count() * iPercent / 100
		return self.copy(self._keys[:iSplit]), self.copy(self._keys[iSplit:])
	
	def grouped(self, func):
		return [(key, self.copy(group)) for key, group in groupby(self.sort(func)._keys, lambda key: func(self._factory(key)))]
		
	def sort(self, metric, reverse=False):
		return self.copy(sort(self._keys, key=lambda k: metric(self._factory(k)), reverse=reverse))
		
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
		combined = [self._keyify(key) for key in list(self._keys) + list(keys)]
		return self.copy(sorted(set(combined), key=combined.index))
	
	def limit(self, iLimit):
		return self.copy(self._keys[:iLimit])
	
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
		return self.copy(shuffled)
		
	def fraction(self, iDenominator):
		return self.limit(self.count() / iDenominator)
		
	def percentage(self, iPercent):
		return self.limit(self.count() * iPercent / 100)
		
	def sum(self, value):
		return sum(value(e) for e in self.entities())
	
	def average(self, value):
		if not self:
			return 0.0
		return 1.0 * self.sum(value) / self.count()
		
	def transform(self, cls, map = lambda x: x, condition = lambda x: True):
		return cls([map(k) for k in self._keys if condition(self._factory(k))]).clear_named(self.name())

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
		if not keys:
			raise ValueError("Divide among empty keys: %s" % self)
	
		shuffled_keys = self.shuffle()._keys[:]
		return [(key, self.copy(key for j, key in enumerate(shuffled_keys) if j % len(keys) == i)) for i, key in enumerate(keys)]
	
	def index(self, key):
		return self.entities().index(key)
	
	def unique(self):
		return self.copy(k for k in set(self._keys))
	
	def valued(self, func):
		return ((entity, func(entity)) for entity in self)

	def take(self, iNum):
		return self.limit(iNum).entities() + [None] * max(0, iNum-self.count())
	
	def enrich(self, func):
		enrich = self.copy([])
		for key in self._keys:
			enrich += func(key)
		enriched = self + enrich
		return enriched.unique()
	
	def format(self, separator=",", final_separator=None, formatter=lambda x: x):
		if final_separator is None:
			final_separator = text("TXT_KEY_AND")
		return format_separators(self.entities(), separator, final_separator, formatter)
	
	def clear_named(self, name):
		return self.named(name)
	
	def named(self, name):
		self._name = name
		return self
	
	def name(self):
		return self._name



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
		
	def none(self):
		return self.of([])
		
	def regions(self, *regions):
		return self.all().where(lambda p: p.getRegionID() in regions)
		
	def region(self, iRegion):
		return self.regions(iRegion)
		
	def surrounding(self, *args, **kwargs):
		radius = kwargs.get('radius', 1)
		if radius < 0: raise ValueError("radius cannot be negative, received: '%d'" % radius)
		x, y = _parse_tile(*args)
		if not isinstance(x, int): raise Exception("x must be int, is %s" % type(x))
		if not isinstance(y, int): raise Exception("y must be int, is %s" % type(y))
		return Plots(sort(list(set(wrap(x+i, y+j) for i in range(-radius, radius+1) for j in range(-radius, radius+1)))))
		
	def ring(self, *args, **kwargs):
		radius = kwargs.get('radius', 1)
		circle = self.surrounding(*args, **kwargs)
		inside = self.surrounding(*args, **{'radius': radius-1})
		return circle.without(inside)
	
	def circle(self, *args, **kwargs):
		radius = kwargs.get('radius', 1)
		square = self.surrounding(*args, **kwargs)
		x, y = _parse_tile(*args)
		return square.where(lambda p: plotDistance(p.getX(), p.getY(), x, y) <= radius)
	
	def city_radius(self, city):
		if not city or city.isNone():
			raise TypeError("city object is None")
	
		return Plots([location(city.getCityIndexPlot(i)) for i in range(21)])
	
	def owner(self, iPlayer):
		return self.all().owner(iPlayer)

	def area(self, dArea, dExceptions, identifier):
		return self.rectangle(*dArea[identifier]).without(dExceptions[identifier]).clear_named(infos.civ(identifier).getShortDescription(0))

	def sum(self, areas):
		return sum(areas, self.none())

	def birth(self, identifier, extended=None):
		if extended is None: extended = isExtendedBirth(identifier)
		if identifier in dExtendedBirthArea and extended:
			return self.area(dExtendedBirthArea, dBirthAreaExceptions, identifier)
		if identifier not in dBirthArea:
			return self.core(identifier)
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

	def expansion(self, identifier):
		if identifier not in dExpansionArea:
			return self.none()
		return self.area(dExpansionArea, dExpansionAreaExceptions, identifier)

	def respawn(self, identifier):
		if identifier in dRespawnArea:
			return self.area(dRespawnArea, dRespawnAreaExceptions, identifier)
		return self.birth(identifier)
	
	def capital(self, identifier):
		iPeriod = player(identifier).getPeriod()
		if iPeriod in dPeriodCapitals:
			return plot(dPeriodCapitals[iPeriod])
		return plot(dCapitals[identifier])
	
	def capitals(self, identifier):
		return self.of([self.capital(identifier)])
		
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
			
		if len(exceptions) == 1:
			if isinstance(exceptions[0], Locations):
				remaining = set(self._keys) - set(exceptions[0]._keys)
				return self.copy(remaining)
			
			elif isinstance(exceptions[0], (list, set)):
				exceptions = exceptions[0]
			
		remaining = set(self._keys) - set(self._keyify(item) for item in exceptions)
		return self.copy(remaining)
	
	def _closest(self, *args):
		x, y = _parse_tile(*args)
		return find_min(self.entities(), lambda loc: distance(loc, (x, y)))
		
	def closest(self, *args):
		return self._closest(*args).result
		
	def closest_distance(self, *args):
		return self._closest(*args).value
	
	def closest_pair(self, locations):
		if not isinstance(locations, Locations):
			raise Exception("Expected instance of Locations, received: %s" % locations)
			
		permutations = [(x, y) for x in self.shuffle().entities() for y in locations.shuffle().entities()]
		return find_min(permutations, lambda (x, y): distance(x, y)).result
	
	def closest_all(self, locations):
		closest = self.closest_pair(locations)
		
		if closest is None:
			return None
		
		return closest[0]
	
	def closest_within(self, *args, **kwargs):
		closest_distance = self.closest_distance(*args)
		radius = kwargs.get('radius', 1)
		if closest_distance is None or closest_distance > radius:
			return self.empty()
		return self.where(lambda loc: distance(location(*args), loc) == closest_distance)
		
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
	
	def areas(self, *areas):
		return self.where(lambda loc: loc.getArea() in [getArea(area) for area in areas])
	
	def area(self, area):
		return self.areas(area)
	
	def intersect(self, locations):
		return any(loc in locations for loc in self)


class Plots(Locations):

	def __init__(self, plots):
		super(Plots, self).__init__([self._keyify(p) for p in plots])
		
	def _keyify(self, item):
		if isinstance(item, tuple) and len(item) == 2:
			return item
			
		if isinstance(item, (CyPlot, CyCity, CyUnit)):
			return location(item)
			
		raise Exception("Not a valid plot key: %s" % type(item))
		
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
		return self.transform(Cities, map = lambda key: city(key), condition = lambda p: p.isCity())
	
	def land(self):
		return self.where(lambda p: not p.isWater())
	
	def water(self):
		return self.where(lambda p: p.isWater())
		
	def coastal(self):
		return self.where(lambda p: p.isCoastalLand())
	
	def core(self, identifier):
		if isinstance(identifier, Civ):
			return self.where(lambda p: p.isCore(identifier))
		return self.where(lambda p: p.isPlayerCore(identifier))
		
	def passable(self):
		return self.where(lambda p: not p.isImpassable())
		
	def lake(self):
		return self.where(lambda p: p.isLake())
	
	def sea(self):
		return self.water().where(lambda p: not p.isLake())
	
	def no_enemies(self, iPlayer):
		return self.where(lambda p: units.at(p).atwar(iPlayer).none())
	
	def expand(self, iNumTiles):
		return self.enrich(lambda p: plots.circle(p, radius=iNumTiles))
	
	def edge(self):
		return self.where(lambda p: plots.surrounding(p).any(lambda sp: sp not in self))


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
		cities = _iterate(owner.firstCity, owner.nextCity)
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
		
	def none(self):
		return self.of([])
	
	def ids(self, identifier, ids):
		return Cities([player(identifier).getCity(id) for id in ids])
		
	def surrounding(self, *args, **kwargs):
		return self.plots.surrounding(*args, **kwargs).cities()
	
	def ring(self, *args, **kwargs):
		return self.plots.ring(*args, **kwargs).cities()

	def birth(self, identifier, extended = None):
		return self.plots.birth(identifier, extended).cities()

	def core(self, identifier):
		return self.plots.core(identifier).cities()

	def respawn(self, identifier):
		return self.plots.respawn(identifier).cities()
	
	def capital(self, identifier):
		return city(self.plots.capital(identifier))
		
	def respawnCapital(self, identifier):
		return city(self.plots.respawnCapital(identifier))
		
	def newCapital(self, identifier):
		return city(self.plots.newCapital(identifier))
		
		
class CityKey(object):

	def __init__(self, city):
		self.owner = city.getOwner()
		self.id = city.getID()
		
	def __eq__(self, other):
		return isinstance(other, CityKey) and (self.owner, self.id) == (other.owner, other.id)
		
	def __str__(self):
		return str((self.owner, self.id))
		
	@classmethod
	def of(cls, city):
		if isinstance(city, cls):
			return city
		return cls(city)


class Cities(Locations):

	def __init__(self, cities):
		super(Cities, self).__init__([self._keyify(city) for city in cities])
		
	def _keyify(self, item):
		return CityKey.of(item)
		
	def _factory(self, key):
		if isinstance(key, CityKey):
			return player(key.owner).getCity(key.id)
		
		raise TypeError("Can only use keys of type CityKey in Cities, got: %s" % type(key))
		
	def __contains__(self, item):
		if isinstance(item, (CyCity, CityKey)):
			return CityKey.of(item) in self._keys
		
		elif isinstance(item, CyPlot):
			if not item.isCity():
				return False
			return self.__contains__(item.getPlotCity())
		
		elif isinstance(item, CyUnit):
			return self.__contains__(item.plot())
			
		elif isinstance(item, tuple) and len(item) == 2:
			return self.__contains__(plot(item))
			
		raise TypeError("Tried to check if Cities contains '%s', can only contain plots, cities, units or coordinate tuples" % type(item))
		
	def __str__(self):
		return str(["%s (%s) at %s" % (city.getName(), adjective(city.getOwner()), (city.getX(), city.getY())) for city in self.entities()])
	
	def without(self, *exceptions):
		if not exceptions or none(exceptions):
			return self
		
		if len(exceptions) == 1 and isinstance(exceptions[0], (list, set, Locations)):
			exceptions = exceptions[0]
		
		return self.where(lambda city: location(city) not in [location(loc) for loc in exceptions])
	
	def existing(self):
		return self.where(lambda city: city.getX() >= 0)
	
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

	def core(self, identifier):
		if isinstance(identifier, Civ):
			return self.where(lambda city: city.isCore(identifier))
		return self.where(lambda city: city.isPlayerCore(identifier))
	
	def plots(self):
		return self.transform(Plots, map = lambda key: plot(self._factory(key)))
	
	def plots(self):
		return self.transform(Plots, map = lambda key: plot(self._factory(key)))
	
		
class UnitFactory:

	def of(self, units):
		return Units([UnitKey.of(unit) for unit in units])

	def owner(self, identifier):
		units = _iterate(player(identifier).firstUnit, player(identifier).nextUnit, UnitKey.of)
		return Units(units)
		
	def at(self, *args):
		if args is None:
			return Units([])
			
		return Units([UnitKey.of(plot(*args).getUnit(i)) for i in range(plot(*args).getNumUnits())])
		
		
class UnitKey(object):

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
		super(Units, self).__init__([self._keyify(u) for u in units])
	
	def _keyify(self, item):
		return UnitKey.of(item)
		
	def _factory(self, key):
		return unit(key)
		
	def __contains__(self, item):
		if isinstance(item, CyUnit):
			return UnitKey.of(item) in self._keys
			
		raise TypeError("Tried to check if Units contains '%s', can only contain units" % type(item))
		
	def __str__(self):
		return ", ".join(["%s (%s) at %s" % (infos.unit(unit.getUnitType()).getText(), adjective(unit.getOwner()), (unit.getX(), unit.getY())) for unit in self.entities()])

	def owner(self, iPlayer):
		return self.where(lambda u: owner(u, iPlayer))

	def notowner(self, iPlayer):
		return self.where(lambda u: not owner(u, iPlayer))
	
	def minor(self):
		return self.where(lambda u: is_minor(u))
		
	def type(self, iUnitType):
		return self.where(lambda u: u.getUnitType() == iUnitType)
		
	def by_type(self):
		return dict([(iType, self.type(iType)) for iType in set(self.types())])
		
	def atwar(self, iPlayer):
		return self.where(lambda u: team(iPlayer).isAtWar(u.getTeam()))
		
	def domain(self, iDomain):
		return self.where(lambda u: u.getDomainType() == iDomain)
	
	def land(self):
		return self.domain(DomainTypes.DOMAIN_LAND)
		
	def water(self):
		return self.domain(DomainTypes.DOMAIN_SEA)
	
	def types(self):
		return [unit.getUnitType() for unit in self]
	
	def combat(self, iUnitCombatType):
		return self.where(lambda u: u.getUnitCombatType() == iUnitCombatType)
	

class PlayerFactory:

	def all(self):
		return Players(range(gc.getMAX_PLAYERS())).where(lambda p: player(p).getCivilizationType() >= 0)
		
	def major(self):
		return self.all().where(lambda p: not is_minor(p))
		
	def minor(self):
		return self.all().where(lambda p: is_minor(p))
		
	def civs(self, *civs):
		return self.all().where(lambda p: civ(p) in civs)
	
	def group(self, iGroup):
		return self.civs(*dCivGroups[iGroup])
		
	def independent(self):
		return self.civs(iIndependent, iIndependent2)
		
	def barbarian(self):
		return self.civs(iBarbarian)
		
	def native(self):
		return self.civs(iNative)
		
	def vassals(self, iPlayer):
		return self.all().where(lambda p: team(p).isVassal(player(iPlayer).getTeam()))
	
	def defensivePacts(self, iPlayer):
		return self.all().where(lambda p: team(p).isDefensivePact(player(iPlayer).getTeam()))
		
	def none(self):
		return Players([])
	
	def of(self, *players):
		if len(players) == 1 and isinstance(players[0], Players):
			return players[0]
	
		return Players(players)
	
	def at_war(self, iPlayer):
		return self.all().at_war(iPlayer)
	
	def allies(self, iPlayer):
		return self.of(iPlayer).enrich(self.defensivePacts).enrich(self.vassals)

		
class Players(EntityCollection):

	def __init__(self, players):
		if all(isinstance(x, Civ) for x in players):
			players = [slot(x) for x in players if slot(x) >= 0]
		elif not all(isinstance(x, int) for x in players):
			raise Exception("All entries in Players need to be either int or Civ")
	
		super(Players, self).__init__(players)
		
	def _keyify(self, item):
		if isinstance(item, Civ):
			return slot(item)
			
		return item

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
	
	def existing(self):
		return self.where(lambda p: player(p).isExisting())
	
	def notalive(self):
		return self.where(lambda p: not player(p).isAlive())
	
	def notexisting(self):
		return self.where(lambda p: not player(p).isExisting())
		
	def ai(self):
		return self.where(lambda p: not player(p).isHuman())

	def human(self):
		return self.where(lambda p: player(p).isHuman())
	
	def major(self):
		return self.where(lambda p: not is_minor(p))
		
	def without(self, exceptions):
		if isinstance(exceptions, types.GeneratorType):
			exceptions = list(exceptions)
		elif not isinstance(exceptions, (list, set, Players)):
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
	
	def before_fall(self):
		return self.where(lambda p: year() < year(dFall[p]))

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
		return [(x, y) for x, y in permutations(self._keys, self._keys) if (identical and x == y) or x < y]
		
	def asCivs(self):
		return [civ(p) for p in self.entities()]
	
	def tech(self, iTech):
		return self.where(lambda p: team(p).isHasTech(iTech))
	
	def at_war(self, iPlayer):
		return self.where(lambda p: team(iPlayer).isAtWar(player(p).getTeam()))
	
	def religion(self, iReligion):
		return self.where(lambda p: player(p).getStateReligion() == iReligion)
	
	def defensivePacts(self):
		return players.all().where(lambda p1: self.any(lambda p2: team(p1).isDefensivePact(player(p2).getTeam())))


class Civilizations(EntityCollection):

	def __init__(self, civs):
		if all(isinstance(x, int) for x in civs):
			try:
				civs = [civ(x) for x in civs]
			except Exception, e:
				raise Exception("error when processing civs: %s: %s" % (civs, e))
		elif not all(isinstance(x, Civ) for x in civs):
			raise Exception("All entries in Civilizations need to be either int or Civ")
	
		super(Civilizations, self).__init__(civs)
		
	def _keyify(self, item):
		if isinstance(item, int):
			return civ(item)
			
		return item

	def __contains__(self, item):
		return civ(item) in self._keys

	def __str__(self):
		return ",".join([infos.civ(item).getText() for item in self.entities()])
		
	def without(self, exceptions):
		if not isinstance(exceptions, (list, set, Players)):
			exceptions = [exceptions]
		return self.where(lambda c: c not in [civ(e) for e in exceptions])
	
	def before_fall(self):
		return self.where(lambda c: year() < year(dFall[c]))
	

class CivFactory(object):

	def all(self):
		return Civilizations([Civ(i) for i in range(iNumCivs)])
	
	def major(self):
		return Civilizations(lBirthOrder)
	
	def of(self, *items):
		return Civilizations([civ(element) for element in items])

		
class CreatedUnits(object):

	@staticmethod
	def none():
		return CreatedUnits([])

	def __init__(self, units):
		self._units = units
		
	def __len__(self):
		return len(self._units)
		
	def __iter__(self):
		return iter(self._units)
	
	def __add__(self, other):
		return CreatedUnits(self._units + other._units)
		
	def adjective(self, adjective):
		if not adjective:
			return self
	
		for unit in self:
			unit.setName('%s %s' % (text(adjective), unit.getName()))
			
		return self
			
	def experience(self, iExperience):
		if iExperience <= 0:
			return self
	
		for unit in self:
			unit.changeExperience(iExperience, 100, False, False, False)
			
		return self
	
	def promotion(self, *promotions):
		for iPromotion in promotions:
			for unit in self:
				unit.setHasPromotion(iPromotion, True)
		
		return self
		
	def one(self):
		if len(self) == 1:
			return self._units[0]
		raise Exception('Can only return one unit if it is a single created unit')
	
	def count(self):
		return len(self)

		
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
		return self.__class__([k for k in self._keys if condition(k)], self.info_class)
	
	def copy(self, keys):
		return self.__class__(list(keys), self.info_class)
		
	def sort(self, metric, reverse=False):
		return self.copy(sort(self._keys, key=metric, reverse=reverse))
	
	def __contains__(self, item):
		return item in self._keys
	
	def __str__(self):
		return ','.join([self._factory(i).getText() for i in self])
		
	def _factory(self, key):
		return self.info_class(key)
	
	def entities(self):
		return self._keys
		

class Infos:
	
	def info(self, type):
		return info_types[type][0]
	
	def of(self, type):
		return info_types[type][1](self)
	
	def get(self, type, identifier):
		return self.info(type)(self, identifier)
	
	def text(self, type, identifier):
		return self.get(type, identifier).getText()

	def type(self, string):
		type = gc.getInfoTypeForString(string)
		if type < 0:
			raise ValueError("Type for '%s' does not exist" % string)
		return type
		
	def constant(self, string):
		return gc.getDefineINT(string)
		
	def art(self, string):
		return gc.getInterfaceArtInfo(self.type(string)).getPath()
	
	def attitude(self, identifier):
		return gc.getAttitudeInfo(identifier)
	
	def attitudes(self):
		return InfoCollection.type(gc.getAttitudeInfo, AttitudeTypes.NUM_ATTITUDE_TYPES)
		
	def bonus(self, identifier):
		if isinstance(identifier, CyPlot):
			return gc.getBonusInfo(identifier.getBonusType(-1))
			
		if isinstance(identifier, int):
			return gc.getBonusInfo(identifier)
			
		raise TypeError("Expected identifier to be CyPlot or bonus type ID, got '%s'" % type(identifier))
	
	def bonuses(self):
		return InfoCollection.type(gc.getBonusInfo, gc.getNumBonusInfos())
		
	def build(self, identifier):
		return gc.getBuildInfo(identifier)
	
	def builds(self):
		return InfoCollection.type(gc.getBuildInfo, gc.getNumBuildInfos())
		
	def building(self, identifier):
		return gc.getBuildingInfo(identifier)
	
	def buildings(self):
		return InfoCollection.type(gc.getBuildingInfo, gc.getNumBuildingInfos())
		
	def buildingClass(self, identifier):
		return gc.getBuildingClassInfo(identifier)
	
	def buildingClasses(self):
		return InfoCollection.type(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos())

	def civ(self, identifier):
		if isinstance(identifier, (CyTeam, CyPlayer, CyPlot, CyCity, CyUnit)):
			return gc.getCivilizationInfo(civ(identifier))
	
		return gc.getCivilizationInfo(identifier)
	
	def civs(self):
		return InfoCollection.type(gc.getCivilizationInfo, gc.getNumCivilizationInfos())
	
	def civic(self, identifier):
		return gc.getCivicInfo(identifier)
	
	def civics(self):
		return InfoCollection.type(gc.getCivicInfo, gc.getNumCivicInfos())
		
	def commerce(self, identifier):
		return gc.getCommerceInfo(identifier)
	
	def commerces(self, identifier):
		return InfoCollection.type(gc.getCommerceInfo, CommerceTypes.NUM_COMMERCE_TYPES)
		
	def corporation(self, identifier):
		return gc.getCorporationInfo(identifier)
		
	def corporations(self):
		return InfoCollection.type(gc.getCorporationInfo, gc.getNumCorporationInfos())
	
	def cultureLevel(self, identifier):
		return gc.getCultureLevelInfo(identifier)
	
	def cultureLevels(self):
		return InfoCollection.type(gc.getCultureLevelInfo, gc.getNumCultureLevelInfos())
	
	def era(self, identifier):
		return gc.getEraInfo(identifier)
	
	def eras(self):
		return InfoCollection.type(gc.getEraInfo, gc.getNumEraInfos())
		
	def feature(self, identifier):
		if isinstance(identifier, CyPlot):
			return gc.getFeatureInfo(identifier.getFeatureType())
			
		if isinstance(identifier, int):
			return gc.getFeatureInfo(identifier)
			
		raise TypeError("Expected identifier to be CyPlot or feature type ID, got '%s'" % type(identifier))
	
	def features(self):
		return InfoCollection.type(gc.getFeatureInfo, gc.getNumFeatureInfos())
		
	def gameSpeed(self, iGameSpeed = None):
		if iGameSpeed is None:
			iGameSpeed = game.getGameSpeedType()
		return gc.getGameSpeedInfo(iGameSpeed)
	
	def gameSpeeds(self):
		return InfoCollection.type(gc.getGameSpeedInfo, gc.getNumGameSpeedInfos())
		
	def handicap(self, identifier=None):
		if identifier is None:
			identifier = game.getHandicapType()
		return gc.getHandicapInfo(identifier)
	
	def handicaps(self):
		return InfoCollection.type(gc.getHandicapInfo, gc.getNumHandicapInfos())
		
	def improvement(self, identifier):
		return gc.getImprovementInfo(identifier)
	
	def improvements(self):
		return InfoCollection.type(gc.getImprovementInfo, gc.getNumImprovementInfos())
	
	def leader(self, identifier):
		if isinstance(identifier, CyPlayer):
			return gc.getLeaderHeadInfo(identifier.getLeader())
			
		if isinstance(identifier, int):
			return gc.getLeaderHeadInfo(identifier)
			
		raise TypeError("Expected identifier to be CyPlayer or leaderhead ID, got: '%s'" % type(identifier))
	
	def leaders(self):
		return InfoCollection.type(gc.getLeaderHeadInfo, gc.getNumLeaderHeadInfos())
	
	def paganReligion(self, identifier):
		if isinstance(identifier, Civ):
			return self.paganReligion(self.civ(identifier).getPaganReligion())
	
		return gc.getPaganReligionInfo(identifier)
	
	def paganReligions(self):
		return InfoCollection.type(gc.getPaganReligionInfo, gc.getNumPaganReligionInfos())
		
	def promotion(self, identifier):
		return gc.getPromotionInfo(identifier)
		
	def promotions(self):
		return InfoCollection.type(gc.getPromotionInfo, gc.getNumPromotionInfos())
		
	def project(self, identifier):
		return gc.getProjectInfo(identifier)

	def projects(self):
		return InfoCollection.type(gc.getProjectInfo, gc.getNumProjectInfos())
		
	def religion(self, iReligion):
		return gc.getReligionInfo(iReligion)
	
	def religions(self):
		return InfoCollection.type(gc.getReligionInfo, gc.getNumReligionInfos())
	
	def route(self, identifier):
		return gc.getRouteInfo(identifier)
	
	def routes(self):
		return InfoCollection.type(gc.getRouteInfo, gc.getNumRouteInfos())
	
	def specialist(self, identifier):
		return gc.getSpecialistInfo(identifier)
	
	def specialists(self):
		return InfoCollection.type(gc.getSpecialistInfo, gc.getNumSpecialistInfos())
		
	def tech(self, iTech):
		return gc.getTechInfo(iTech)
	
	def techs(self):
		return InfoCollection.type(gc.getTechInfo, iNumTechs)
	
	def terrain(self, iTerrain):
		return gc.getTerrainInfo(iTerrain)
	
	def terrains(self):
		return InfoCollection.type(gc.getTerrainInfo, gc.getNumTerrainInfos())
		
	def unit(self, identifier):
		if isinstance(identifier, CyUnit):
			return gc.getUnitInfo(identifier.getUnitType())
			
		if isinstance(identifier, int):
			return gc.getUnitInfo(identifier)
			
		raise TypeError("Expected identifier to be CyUnit or unit type ID, got '%s'" % type(identifier))
	
	def units(self):
		return InfoCollection.type(gc.getUnitInfo, gc.getNumUnitInfos())
	
	def unitClasses(self):
		return InfoCollection.type(gc.getUnitClassInfo, gc.getNumUnitClassInfos())
	
	def unitCombat(self, iUnitCombat):
		return gc.getUnitCombatInfo(iUnitCombat)
	
	def unitCombats(self):
		return InfoCollection.type(gc.getUnitCombatInfo, gc.getNumUnitCombatInfos())


info_types = {
	AttitudeTypes: (Infos.attitude, Infos.attitudes),
	CvBonusInfo: (Infos.bonus, Infos.bonuses),
	CvBuildInfo: (Infos.build, Infos.builds),
	CvBuildingInfo: (Infos.building, Infos.buildings),
	CvBuildingClassInfo: (Infos.buildingClass, Infos.buildingClasses),
	CvCivilizationInfo: (Infos.civ, Infos.civs),
	CvCommerceInfo: (Infos.commerce, Infos.commerces),
	CvCorporationInfo: (Infos.corporation, Infos.corporations),
	CvCultureLevelInfo: (Infos.cultureLevel, Infos.cultureLevels),
	CvEraInfo: (Infos.era, Infos.eras),
	CvFeatureInfo: (Infos.feature, Infos.features),
	CvGameSpeedInfo: (Infos.gameSpeed, Infos.gameSpeeds),
	CvHandicapInfo: (Infos.handicap, Infos.handicaps),
	CvImprovementInfo: (Infos.improvement, Infos.improvements),
	CvLeaderHeadInfo: (Infos.leader, Infos.leaders),
	CvPromotionInfo: (Infos.promotion, Infos.promotions),
	CvProjectInfo: (Infos.project, Infos.projects),
	CvReligionInfo: (Infos.religion, Infos.religions),
	CvRouteInfo: (Infos.route, Infos.routes),
	CvSpecialistInfo: (Infos.specialist, Infos.specialists),
	CvTechInfo: (Infos.tech, Infos.techs),
	CvTerrainInfo: (Infos.terrain, Infos.terrains),
	CvUnitInfo: (Infos.unit, Infos.units),
	UnitCombatTypes: (Infos.unitCombat, Infos.unitCombats),
}


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


class TechFactory(object):

	def none(self):
		return TechCollection()

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
		techs = [i for i in infos.techs().where(lambda iTech: infos.tech(iTech).getEra() <= self.iEra or infos.tech(iTech).getGridX() <= self.iColumn)]
		techs += [i for i in self.included if i not in techs]
		techs = [i for i in techs if i not in self.excluded]
		
		return techs
	
	def __iter__(self):
		return iter(self.techs())
		
		
plots = PlotFactory()
cities = CityFactory()
units = UnitFactory()
players = PlayerFactory()
civs = CivFactory()
techs = TechFactory()
infos = Infos()

plot_ = plot
city_ = city