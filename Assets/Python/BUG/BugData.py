## BugData
##
## This module provides functions to efficiently store structured data in the CyGame script data.
##
## The data consists of nested dictionaries called Tables. Each Table is pickled by this
## module to maintain compatibility with SdToolKit. Access to the values (slots) in a Table
## is provided by standard [] notation, and they not pickled individually.
##
## You can nest Tables to any depth and store any value--even dictionaries and objets--into
## individual slots. Tables and slots are located using key chains: lists of string identifiers
## such as ("Reminders", "queues") or ("UnitCnt", "UNITArcher", "tt1").
##
## Notes
##
##   - Must be cleared at the start of the GameStart event
##   - Must be loaded at the start of the OnLoad event
##   - Must be saved at the end of the OnPreSave event
##
##   - The key of the root Table is "root", but you must not include it in your key chains.
##
## This module stores its data in a way that is 100% save compatible with SdToolKit.
## Since BUG's SdToolKit has been modified to use this module you can continue to use
## SdToolKit's API. Switching to use this module could provide a minor speed improvement
## if you modify large data structures at the cost of tying your code to this module.
##
## TODO
##
##   - Drop Mod/Entity
##   - getData(): uses pickle
##   - getValue() or []: direct
##   - Allows arbitrary nesting of pickled dicts, including raw values at the top-level
##
## Copyright (c) 2010 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import CyGame
import BugUtil
import cPickle as pickle


## Data Access

def hasTable(*keys):
	"""
	Returns True if the chain of key(s) leads to a table, False otherwise.
	"""
	return getGameData().hasTable(*keys)

def findTable(*keys):
	"""
	If the key(s) lead to an existing table, it is returned. Otherwise None is returned.
	
	This function will not create any new tables. You must check the return value for None
	or you will get an exception.
	"""
	return getGameData().findTable(*keys)

def getTable(*keys):
	"""
	Returns the table at the end of the chain of key(s), creating any missing tables along the way.
	
	This function always returns a valid table.
	"""
	return getGameData().getTable(*keys)

def deleteTable(*keys):
	"""
	If the chain of key(s) leads to a table, it is deleted and True is returned; otherwise False is returned.
	"""
	return getGameData().delTable(*keys)


## Event Handlers and Internal Access

def getGameData():
	if not g_data:
		BugUtil.warn("BugData not loaded; loading now")
		initGameData().load()
	return g_data

def initGameData():
	global g_data
	g_data = RootTable()
	return g_data


## Event Handlers

def onGameStart(argsList):
	initGameData()

def onGameLoad(argsList):
	initGameData().load()

def save():
	getGameData().save()


## Globals

g_data = None


## Table Classes

class Table(object):
	def __init__(self, key, data):
		self.key = key
		self.data = data
		self.dirty = False
		self.children = dict()
	def __str__(self):
		return self.key
	def load(self):
		pass
	def save(self):
		if self.children:
			BugUtil.debug("BugData - saving %s's children", self)
			for table in self.children.itervalues():
				table.save()
		if self.dirty:
			BugUtil.debug("BugData - saving %s", self)
			self._save()
			self.dirty = False
		else:
			BugUtil.debug("BugData - %s not dirty", self)
	def _save(self):
		pass
	def __del__(self):
		if self.dirty:
			BugUtil.warn("Data not saved: %s", self)
	
	def setData(self, data):
		self.data = data
		self.dirty = True
		BugUtil.debug("BugData - new data for %s: %r", self, self.data)
	def __contains__(self, key):
		BugUtil.debug("BugData - %s in %s: %s", key, self, key in self.data)
		return key in self.data
	def __getitem__(self, key):
		BugUtil.debug("BugData - %s.%s = %r", self, key, self.data[key])
		return self.data[key]
	def __setitem__(self, key, value):
		BugUtil.debug("BugData - %s.%s -> %r", self, key, value)
		self.data[key] = value
		self.dirty = True
	def __delitem__(self, key):
		BugUtil.debug("BugData - del %s.%s", self, key)
		try:
			del self.data[key]
			self.dirty = True
		except:
			pass
	
	def hasValue(self, key):
		return key in self
	def getValue(self, key):
		return self[key]
	def setValue(self, key, value):
		self[key] = value
	def delValue(self, key):
		del self[key]
	
	def hasTable(self, *keys):
		if len(keys) == 1:
			return self._hasTable(keys[0])
		else:
			table = self._findTable(keys[0])
			if table is None:
				return False
			else:
				return table.hasTable(*keys[1:])
	def _hasTable(self, key):
		return key in self.data
	def findTable(self, *keys):
		table = self._findTable(keys[0])
		if table is None or len(keys) == 1:
			return table
		else:
			return table.findTable(*keys[1:])
	def _findTable(self, key):
		if self._hasTable(key):
			BugUtil.debug("BugTable - found %s in %s", key, self)
			return self._getTable(key)
		else:
			BugUtil.debug("BugTable - %s not found in %s", key, self)
			return None
	def getTable(self, *keys):
		if len(keys) == 1:
			return self._getTable(keys[0])
		else:
			return self._getTable(keys[0]).getTable(*keys[1:])
	def _getTable(self, key):
		if self._isOpen(key):
			BugUtil.debug("BugData - returning open table %s.%s", self, key)
			return self.children[key]
		elif self._hasTable(key):
			return self._openTable(key, pickle.loads(self[key]))
		else:
			return self._openTable(key, dict())
	def delTable(self, *keys):
		if len(keys) == 1:
			return self._delTable(keys[0])
		else:
			table = self._findTable(keys[0])
			if table is None:
				return False
			else:
				return table.delTable(*keys[1:])
	def _delTable(self, key):
		self._closeTable(key)
		if self._hasTable(key):
			BugUtil.debug("BugData - deleting %s.%s", self, key)
			del self[key]
	
	def _isOpen(self, key):
		return key in self.children
	def _openTable(self, key, data):
		BugUtil.debug("BugData - opening %s.%s: %r", self, key, data)
		table = ChildTable(self, key, data)
		self.children[key] = table
		return table
	def _closeTable(self, key):
		if self._isOpen(key):
			BugUtil.debug("BugData - closing %s.%s", self, key)
			table = self.children[key]
			table.discard()
			del self.children[key]


class RootTable(Table):
	def __init__(self):
		super(RootTable, self).__init__("root", dict())
		self.game = CyGame()
	def load(self):
		BugUtil.debug("BugData - loading %s", self)
		script = self.game.getScriptData()
		if script:
			self.data = pickle.loads(script)
			BugUtil.debug("BugData - loaded %r", self.data)
	def _save(self):
		self.game.setScriptData(pickle.dumps(self.data))


class ChildTable(Table):
	def __init__(self, parent, key, data):
		super(ChildTable, self).__init__(key, data)
		self.parent = parent
	def __str__(self):
		if self.parent:
			return str(self.parent) + "." + self.key
		else:
			return "detached " + self.key
	def discard(self):
		if self.dirty:
			BugUtil.debug("BugData - discarding dirty %s", self)
		else:
			BugUtil.debug("BugData - discarding %s", self)
		self.parent = None
	def load(self):
		if self.parent:
			self.data = pickle.loads(self.parent[self.key])
	def _save(self):
		if self.parent:
			self.parent[self.key] = pickle.dumps(self.data)
