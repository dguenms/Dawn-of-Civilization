from CoreTypes import *
from CvPythonExtensions import *
from copy import copy
from traceback import extract_stack


gc = CyGlobalContext()


def deepdict(dictionary={}):
	return defaultdict(dictionary, {})


def appenddict(dictionary={}):
	return defaultdict(dictionary, [])


def defaultdict(dictionary={}, default=None):
	return DefaultDict(dictionary, default)


def dictFromEdges(lNodes, lEdges):
	return CivDict(dict((iNode, list(set([iLeft for iLeft, iRight in lEdges if iRight == iNode] + [iRight for iLeft, iRight in lEdges if iLeft == iNode]))) for iNode in lNodes), [])

		
class DefaultDict(dict):

	def __init__(self, dictionary, default):
		self._default = default
		self.update(dictionary)
		
	def __getitem__(self, key):
		if not key in self:
			super(DefaultDict, self).__setitem__(key, copy(self._default))
		return super(DefaultDict, self).__getitem__(key)


class CivDict(dict):

	def __init__(self, elements, default = None):
		self._default = default
		for key, value in elements.items():
			self[key] = value
	
	def __contains__(self, key):
		if isinstance(key, Civ):
			return dict.__contains__(self, key)
		elif isinstance(key, int):
			return self.__contains__(Civ(gc.getPlayer(key).getCivilizationType()))
		raise TypeError("CivDict only accepts keys of type Civ or int, received: %s" % type(key))
			
	def __getitem__(self, key):
		if isinstance(key, Civ):
			if self._default is not None and key not in self:
				dict.__setitem__(self, key, copy(self._default))
			return dict.__getitem__(self, key)
		elif isinstance(key, int):
			return self.__getitem__(Civ(gc.getPlayer(key).getCivilizationType()))
		raise TypeError("CivDict only accepts keys of type Civ or int, received: %s" % type(key))
		
	def __setitem__(self, key, value):
		if not isinstance(key, Civ):
			raise TypeError("CivDict can only have keys of type Civ, received: %s with value %s" % (key, value))
		dict.__setitem__(self, key, value)


class TileDict:

	def __init__(self, elements, transform = lambda x: x):
		self.entries = appenddict()
		self.transform = transform
	
		for tile, values in elements.items():
			self[tile] = values
			
	def __contains__(self, key):
		return key in self.entries
		
	def __getitem__(self, key):
		return self.entries[key]
		
	def __setitem__(self, tile, values):
		if isinstance(values, (set, list, tuple)):
			key = self.transform(values[0])
			remaining_values = values[1:]
			new_values = [tile]
			new_values += remaining_values
			self.entries[key].append(tuple(new_values))
		else:
			self.entries[self.transform(values)].append(tile)
	
	def __iter__(self):
		return iter(self.entries.items())
	
	def __str__(self):
		return str(self.entries)
	
	def keys(self):
		return self.entries.keys()
	
	def values(self):
		return self.entries.values()


def get_calling_module():
	trace = [call[0] for call in extract_stack() if call[0] != 'DataStructures']
	return trace[-1]


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
		if gc.getGame().getGameTurn() > self.turn:
			self._invalidate()
	
	def _invalidate(self):
		self.turn = gc.getGame().getGameTurn()
		self.offsets = defaultdict({}, 0)