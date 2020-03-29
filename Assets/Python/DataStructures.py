from Types import *
from CvPythonExtensions import *
from copy import copy


gc = CyGlobalContext()


def deepdict(dictionary = {}):
	return defaultdict(dictionary, {})


def appenddict(dictionary = {}):
	return defaultdict(dictionary, [])


def defaultdict(dictionary, default):
	return DefaultDict(dictionary, default)

		
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
			
	def __getitem__(self, key):
		print "get %s from %s" % (key, self)
		if isinstance(key, Civ):
			if self._default is not None: print "default is %s" % self._default
			if key not in self: print "key %s not found" % key
			if self._default is not None and key not in self:
				print "%s not found, set to default of %s" % (key, self._default)
				dict.__setitem__(self, key, copy(self._default))
			return dict.__getitem__(self, key)
		elif isinstance(key, int):
			return self.__getitem__(Civ(gc.getPlayer(key).getCivilizationType()))
		raise TypeError("CivDict only accepts keys of type Civ or int, received: %s" % type(key))
		
	def __setitem__(self, key, value):
		if not isinstance(key, Civ):
			raise TypeError("CivDict can only have keys of type Civ, received: %s with value %s" % (key, value))
		dict.__setitem__(self, key, value)