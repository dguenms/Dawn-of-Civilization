## BugOptions
##
## Provides classes for defining and using options (user preferences)
## within a game. Mod code accesses the settings through the singleton
## Options object, acquired with getOptions().
##
## Object diagram (how object instances relate to each other):
##
##        /----------------------------\
##        |                            |
##        |                            v *
##     Options ----> Option <---- LinkedOption
##        |       *    |    *
##        |            | *
##        v *          |
##     IniFile <-------/
##        |
##        |
##        v
##    ConfigObj ---> File
##
## Class diagram (the Option class hierarchy):
##
##                                     AbstractOption
##                                           |
##                 			 /---------------+---------------\
##                 			 |                               |
##                 			 |                               |
##    UnsavedMixin      BaseOption        IniMixin      LinkedOption
##      |  |             |  |  |             |  |            |
##      |  \------+------/  |  \------+------/  |            |
##      |         |         |         |         |            |
##      |   UnsavedOption   |     IniOption     |     LinkedListOption
##      |                   |                   |
##      |                   |                   |
##      |                   |                   |
##      |             BaseListOption            |
##      |                 |   |                 |
##      \--------+--------/   \--------+--------/
##               |                     |
##       UnsavedListOption       IniListOption
##
## AbstractOption, BaseOption, BaseListOption, UnsavedMixin and IniMixin
## are abstract classes (cannot be instantiated as-is).
## Use <option>.createLinkedOption() for linking options rather than
## instantiating LinkedOption and LinkedListOption yourself.
##
## Unsaved options store their value only while the game is running and do not
## write it to disk. These are good for values that track non-permanent game state,
## for example whether or not the game is being logged. These allow you to link
## them with other options.
##
## TODO:
##
##  ? Create property-like Option accessors on Mod
##    - <Option.ID>: property(Option.getValue, Option.setValue)
##                     or
##                   property(lambda: option, Option.setValue)
##                     Requires Option.__nonzero__()
##                     Can be used in if-test or with () to get its value)
##                     e.g. if Logging.Enabled: ...
##                          if pop >= Civ4lerts.DomPopMinimum(): ...
##                     Might be confusing to new coders
##      e.g. setattr(mod, option.id, property(Option.getValue, Option.setValue))
##
##  * Remove Mod ID from Option ID but keep in Options dictionary keys
##  ? Drop Base from BaseOption and BaseListOption
##
##  * Add fail-over ability to Option
##    If Option/value doesn't exist, uses another Option instead of a default value
##    Most useful for parameterized Options, but for normal Options allows the
##      default for Option X to be Option Y's actual value (or default if no value)
##    e.g.
##      Parameterized:
##        ERA_ANCIENT__WARRIOR -> WARRIOR
##        ERA_ANCIENT__MELEE -> MELEE
##        (This can be accomplished in Python of course)
##      Normal:
##        BetterEspionage.GoodColor -> BetterEspionage.DefaultColor
##        (This way the default for GoodColor is whatever DefaultColor is)
##
## FIXME:
##  * BaseListOption: addGetter() stores index, but createGetter() will need value
##    for int/float lists and color for color lists
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

"""
Options holds all of the options in a map from string ID to Option and the
INI file facades in a map from string ID to IniFile.

Each IniOption belongs to an IniFile and has a section and key within it.

Each IniFile has a file name and provides getters for the options it stores.

Each file can have multiple sections.

  import BugOptions
  g_options = BugOptions.getOptions()
  if g_options.getReminder().isEnabled(): ...
    or
  if g_options.Autolog.LogBuildCompleted: ...

"""

from CvPythonExtensions import *
import BugConfig
import BugDll
import BugInit
import BugPath
import BugUtil
import ColorUtil
from configobj import ConfigObj
import re
import types

# regular expressions used for DLL handling in tooltips

RE_DLL_ALL_TAGS = re.compile(r"(\[DLL\].*\[/DLL\]|\[DLLERR\])", re.DOTALL)
RE_DLL_START_END_TAGS = re.compile(r"\[/?DLL[= ]?[0-9]*\]")
RE_DLL_MSG_TAG = re.compile(r"\[DLLMSG\]")
RE_DLL_CAPTURE_VERSION_MESSAGE = re.compile(r"\[DLL[= ]([0-9]+)\](.*)\[/DLL\]", re.DOTALL)

class Options(object):
	"""Manages maps of Options and IniFiles, each indexed by a unique string ID."""
	
	def __init__(self):
		"""Initializes empty dictionaries of Options and IniFiles."""
		#self.mods = {}
		self.files = {}
		self.options = {}
		self.loaded = True
	
	def getFile(self, id):
		"""Returns the IniFile with the given ID."""
		if (id in self.files):
			return self.files[id]
		else:
			raise BugUtil.ConfigError("Missing file: %s", id)
	
	def addFile(self, file):
		"""Adds the given IniFile to the dictionary."""
		if file.id in self.files:
			BugUtil.error("BugOptions - duplicate INI file: %s", file.id)
		else:
			self.files[file.id] = file
			self.createFileGetter(file)
	
	def isLoaded(self):
		return self.loaded
	
	def read(self):
		"""Reads each IniFile."""
		for file in self.files.itervalues():
			file.read()
		self.loaded = True
	
	def write(self):
		"""Writes each IniFile that is dirty."""
		if self.isLoaded():
			for file in self.files.itervalues():
				file.write()
	

	def findOption(self, id):
		"""Returns the Option with the given ID or returns None of not found."""
		if (id in self.options):
			return self.options[id]
		else:
			return None

	def getOption(self, id):
		"""Returns the Option with the given ID or raises an error if not found."""
		if (id in self.options):
			return self.options[id]
		else:
			raise BugUtil.ConfigError("Missing option: %s", id)

	def addOption(self, option):
		"""Adds an Option to the dictionary if its ID doesn't clash."""
		if option.id in self.options:
			BugUtil.error("BugOptions - duplicate option %s", option.id)
		else:
			self.options[option.id] = option
			BugUtil.debug("BugOptions - added option %s", str(option))

	def clearAllTranslations(self):
		"""Clears the translations of all options in response to the user choosing a language."""
		for option in self.options.itervalues():
			option.clearTranslation()
	
	def resetOptions(self):
		"""Resets all options to their default values."""
		for option in self.options.itervalues():
			option.resetValue()
	
	
	def createFileGetter(self, file):
		"""Creates a getter for the given IniFile."""
		def get():
			return file
		getter = "get" + file.id
		setattr(self, getter, get)
		BugUtil.debug("BugOptions - %s will return IniFile %s", getter, file.id)


# The singleton Options object that holds all Option and IniFile objects.

g_options = Options()
def getOptions(fileID=None):
#	import BugInit
#	BugInit.init()
	if fileID is None:
		return g_options
	else:
		return g_options.getFile(fileID)

def findOption(id):
	return g_options.findOption(id)

def getOption(id):
	return g_options.getOption(id)

def clearAllTranslations(argsList=None):
	g_options.clearAllTranslations()

def read():
	g_options.read()

def write():
	g_options.write()
	

class IniFile(object):
	"""Controls reading/writing an INI file and getting/setting Option values."""
	
	def __init__(self, id, name):
		self.id = id
		self.name = name
		self.path = None
		self.config = None
		self.dirty = False
		self.options = []
	
	def addOption(self, option):
		self.options.append(option)
	
	def isLoaded(self):
		return self.config is not None
	
	def fileExists(self):
		return self.path is not None
	
	def isDirty(self):
		return self.dirty

	def read(self):
		try:
			self.path = BugPath.findSettingsFile(self.name)
			if not self.path:
				self.create()
			else:
				self.config = ConfigObj(self.path, encoding='utf_8')
		except IOError:
			self.path = None
			self.config = None
			BugUtil.trace("BugOptions - error reading file '%s'", self.name)
	
	def create(self):
		BugUtil.debug("BugOptions - creating INI file '%s'", self.name)
		self.config = ConfigObj(encoding='utf_8')
		for option in self.options:
			if not option.isParameterized():
				option.resetValue()
		self.fillComments()
		self.write()
	
	def fillComments(self):
		print dir(self.config)
		self.config.clearInitialComment()
		self.config.addInitialComment(self.id)
		self.config.addInitialComment("")
		self.config.addInitialComment(BugUtil.getPlainText("TXT_KEY_BUG_CREATED_BY_HEADER"))
		self.config.addInitialComment()
		defaultHeader = BugUtil.getPlainText("TXT_KEY_BUG_DEFAULT") + ": "
		for option in self.options:
			if not option.isParameterized():
				section = self.getSection(option.getSection())
				key = option.getKey()
				section.clearKeyComments(key)
				section.addKeyComment(key)
				for line in option.getTooltip().splitlines():
					section.addKeyComment(key, line)
				section.addKeyComment(key, defaultHeader + str(option.getDefault()))
				section.addKeyComment(key)
		self.config.addFinalComment()
	
	def write(self):
		if self.fileExists():
			if self.isDirty():
				BugUtil.debug("BugOptions - writing INI file '%s'", self.name)
				try:
					self.config.write()
					self.dirty = False
				except IOError:
					BugUtil.trace("BugOptions - failed writing INI file '%s'", self.path)
		elif self.isLoaded():
			self.path = BugPath.createSettingsFile(self.name)
			if self.path:
				BugUtil.debug("BugOptions - writing new INI file '%s'", self.name)
				try:
					file = open(self.path, "w")
					self.config.write(file)
					file.close()
					self.dirty = False
				except IOError:
					BugUtil.trace("BugOptions - failed creating INI file '%s'", self.path)
			else:
				BugUtil.error("BugOptions - Cannot locate settings folder")
		else:
			BugUtil.warn("BugOptions - INI file '%s' was never read", self.name)
	
	
	def exists(self, section, key=None):
		return self.config and section in self.config and (key is None or key in self.config[section])
	
	def getSection(self, section):
		if section not in self.config:
			self.config[section] = {}
		return self.config[section]
	
	def getRawValue(self, section, key, default=None):
		if self.exists(section, key):
			return self.getSection(section)[key]
		return default
	
	def getString(self, section, key, default=None):
		if self.exists(section, key):
			return str(self.getSection(section)[key])
		return default

	def getBoolean(self, section, key, default=None):
		if self.exists(section, key):
			return self.getSection(section).as_bool(key)
		return default

	def getInt(self, section, key, default=None):
		if self.exists(section, key):
			return self.getSection(section).as_int(key)
		return default

	def getFloat(self, section, key, default=None):
		if self.exists(section, key):
			return self.getSection(section).as_float(key)
		return default


	def setString(self, section, key, value):
		return self.setValue(section, key, str(value))

	def setBoolean(self, section, key, value):
		return self.setValue(section, key, bool(value))

	def setInt(self, section, key, value):
		return self.setValue(section, key, int(value))

	def setFloat(self, section, key, value):
		return self.setValue(section, key, float(value))

	def setValue(self, section, key, value):
		"""Sets the value if it is different and returns True, else returns False."""
		if value is not None and self.isLoaded():
			sect = self.getSection(section)
			if key in sect:
				old = sect[key]
			else:
				old = None
			if old is None or old != value:
				sect[key] = value
				self.dirty = True
				BugUtil.debug("BugOptions - option %s.%s changed from %s to %s", 
						section, key, str(old), str(value))
				return True
		#BugUtil.debug("BugOptions - option %s.%s not changed", section, key)
		return False


NONE_TYPE = "none"
TYPE_REPLACE = { "bool": "boolean",
			 	 "bit": "boolean",
			 	 "str": "string",
				 "integer": "int",
				 "long": "int",
				 "number": "int",
				 "real": "float",
				 "double": "float",
				 "decimal": "float" }
TYPE_DEFAULT = { "boolean": False,
			 	 "string": "",
				 "int": 0,
				 "float": 0.0,
				 "color": "COLOR_WHITE" }
TYPE_MAP = { "boolean": lambda x: bool(isinstance(x, types.StringTypes) and x.lower() in ('true', 't', 'yes', 'y', 'on', '1')) or bool(isinstance(x, bool) and x) or bool(isinstance(x, int) and x),
			 "string": str,
			 "int": int,
			 "float": float,
			 "color": str }

class AbstractOption(object):
	"""Provides a basic interface and minimal abstract implementation for an option."""

	def __init__(self, mod, id, andId=None, dll=None):
		self.mod = mod
		self.id = id
		self.andId = andId
		self.andOption = None
		self.dll = BugDll.decode(dll)
		if self.dll is not None and self.dll <= 0:
			BugUtil.warn("BugOptions - %s has invalid dll value %r, ignoring", id, dll)
			self.dll = None
		self.enabled = True
		if self.dll > 0:
			if not BugDll.isVersion(self.dll):
				self.enabled = False
	
	def createLinkedOption(self, mod, id):
		return LinkedOption(mod, id, self)
	
	def getID(self):
		return self.id
	
	def getFullID(self):
		return self.idFull
	
	def getMod(self):
		return self.mod
	
	def getTrimmedID(self):
		return unqualify(self.id)
	
	def getDll(self):
		return self.dll
	
	def isDll(self):
		return self.dll > 0
	
	def isEnabled(self):
		return self.enabled
	
	def setEnabled(self, enabled):
		self.enabled = enabled
	
	def enable(self):
		self.setEnabled(True)
	
	def disable(self):
		self.setEnabled(False)
	
	def getDefaultGetterName(self):
		if self.isBoolean():
			return "is" + self.getTrimmedID()
		else:
			return "get" + self.getTrimmedID()
	
	def getDefaultComparerName(self):
		if self.isBoolean():
			return "equals" + self.getTrimmedID()
	
	def getDefaultSetterName(self):
		return "set" + self.getTrimmedID()
	
	def getDefaultResetterName(self):
		return "reset" + self.getTrimmedID()
	
	
#	def getType(self):
#		return NONE_TYPE
	
	def isBoolean(self):
		return self.getType() == "boolean"
	
	def isString(self):
		return self.getType() == "string"
	
	def isInt(self):
		return self.getType() == "int"
	
	def isFloat(self):
		return self.getType() == "float"
	
	def isColor(self):
		return self.getType() == "color"

#	def getDefault(self):
#		return None
	
	def __str__(self):
		return "<%s %s [%s]>" % (self.id, self.getType(), str(self.getDefault()))
	

	def createAccessorPair(self, getter=None, setter=None):
		"""Creates a pair of plain accessors (getter and setter) for this Option."""
		self.createGetter(getter)
		self.createSetter(setter)
	
	def createGetter(self, name=None, values=None):
		if not name:
			name = self.getDefaultGetterName()
		self.bindAccessor(name, self.createGetterFunction(values))
	
	def createGetterFunction(self, values=None):
		if self.isColor():
			return self.createColorGetterFunction(values)
		if values is not None:
			return self.createComparerFunction(values)
		else:
			def get(*args):
				return self.getValue(*args)
			return get
	
	def createColorGetterFunction(self, values=None):
		if values is not None:
			return self.createColorComparerFunction(values)
		else:
			def get(*args):
				return self.getColor(*args)
			return get
	
	def createComparer(self, name, values):
		if not name:
			name = self.getDefaultComparerName()
		self.bindAccessor(name, self.createComparerFunction(values))
	
	def createComparerFunction(self, values):
		if self.isColor():
			return self.createColorGetterFunction(values)
		if values is None:
			BugUtil.warn("BugOptions - createComparerFunction() requires one or more values")
			return None
		else:
			if isinstance(values, (types.TupleType, types.ListType)):
				if len(values) == 1:
					return self.createComparerFunction(values[0])
				else:
					def contains(*args):
						return self.getValue(*args) in values
					return contains
			else:
				value = self.asType(values)
				def equals(*args):
					return self.getValue(*args) == value
				return equals
	
	def createColorComparerFunction(self, values):
		if values is None:
			BugUtil.warn("BugOptions - createColorComparerFunction() requires one or more values")
			return None
		else:
			if isinstance(values, (types.TupleType, types.ListType)):
				if len(values) == 1:
					return self.createColorComparerFunction(values[0])
				else:
					def contains(*args):
						return self.getColor(*args) in values
					return contains
			else:
				value = self.asType(values)
				def equals(*args):
					return self.getColor(*args) == value
				return equals
	
	def createSetter(self, name=None, fixedValue=None):
		if not name:
			name = self.getDefaultSetterName()
		self.bindAccessor(name, self.createSetterFunction(fixedValue))
	
	def createSetterFunction(self, fixedValue=None):
		if fixedValue is None:
			def set(value, *args):
				self.setValue(value, *args)
		else:
			def set(*args):
				self.setValue(fixedValue, *args)
		return set
	
	def createResetter(self, name=None):
		if not name:
			name = self.getDefaultResetterName()
		self.bindAccessor(name, self.createResetterFunction())
	
	def createResetterFunction(self):
		def reset(*args):
			self.resetValue(*args)
		return reset
	
	def bindAccessor(self, name, function):
		setattr(self.mod, name, function)
	
	
	def hasValue(self, *args):
		return self.getRawValue() is not None
	
	def getRawValue(self, *args):
		return None
	
	def getRealValue(self, *args):
		if self.hasValue():
			return TYPE_MAP[self.getType()](self.getRawValue())
		else:
			return self.getDefault()
	
	def getValue(self, *args):
		if not self.getAndOptionValue():
			if self.isBoolean():
				return False
			elif self.isColor():
				return -1
			return None
		return self.getRealValue(*args)
	
	def getAndOptionValue(self):
		if self.andId is not None:
			if self.andOption is None:
				self.andOption = g_options.getOption(self.andId)
				if not self.andOption.isBoolean():
					self.andId = None
					return True
			if not self.andOption.getValue():
				return False
		return True
	
	def asType(self, value):
		return TYPE_MAP[self.getType()](value)
	
	def __call__(self, *args):
		return self.getValue(*args)
	
	def __nonzero__(self, *args):
		value = self.getValue(*args)
		if value is None:
			return False
		if self.isColor():
			return value != -1
		if self.isInt():
			return value != 0
		if self.isFloat():
			return value != 0.0
		if value:
			return True
		return False
	
	def getColor(self, *args):
		"""Returns the value as a color type (int) if this is a color or string option,
		the actual value if an int, or -1 otherwise.
		"""
		if self.isColor() or self.isString():
			return ColorUtil.keyToType(self.getValue(*args))
		elif self.isInt():
			return self.getValue(*args)
		return -1
	
	def setValue(self, value, *args):
		"""Sets the value and calls onChanged() if different.
		
		Sets it to the default if value is None.
		"""
		if value is None:
			value = self.getDefault()
			BugUtil.debug("AbstractOption - setting %s to its default %s", self.getID(), value)
		else:
			BugUtil.debug("AbstractOption - setting %s to %s", self.getID(), value)
		if self._setValue(value, *args):
			self.onChanged(*args)
	
#	def _setValue(self, value, *args):
#		return False
	
	def onChanged(self, *args):
		pass
	
	def resetValue(self, *args):
		BugUtil.debug("BugOptions - resetting %s", self.getID())
		self.setValue(self.getDefault(), *args)


class BaseOption(AbstractOption):
	
	"""
	Holds the metadata for a single option.
	- An ID which is used to access the option. This must be unique for all options.
	- A section and key used to store it in an INI file.
	- A default value used when no value is found in the INI file.
	- A title and tooltip (hover text) used to display it in the Options Screen.
	  Both are now stored in an external XML file and accessed using its ID.
	- A Civ4 dirty-bit that is set when the option is changed. This allows changing
	  the option to force certain aspects of the interface to redraw themselves.
	"""

	def __init__(self, mod, id, type, default=None, andId=None, dll=None, 
				 title=None, tooltip=None, dirty=None):
		"""Sets the important fields of the new Option."""
		super(BaseOption, self).__init__(mod, id, andId, dll)
		
		if type in TYPE_REPLACE:
			type = TYPE_REPLACE[type]
		if type not in TYPE_MAP:
			raise BugUtil.ConfigError("Invalid option type: %s", type)
		self.type = type
		if default is not None:
			self.default = self.asType(default)
		else:
			self.default = TYPE_DEFAULT[type]
		
		self.translated = False
		# TODO: Get key prefix from mod
		self.xmlKey = "TXT_KEY_BUG_OPT_" + self.id.upper()
		self.title = title
		self.tooltip = tooltip
		
		self.dirtyBits = None
		self.dirtyFunctions = None
		if dirty:
			self.addDirty(dirty)
	
	
	def getType(self):
		return self.type

	def getDefault(self):
		return self.default
	

	def getTitle(self):
		if (not self.translated):
			self.translate()
		return self.title

	def getTooltip(self):
		if (not self.translated):
			self.translate()
		return self.tooltip
	
	def translate(self):
		self.title = BugUtil.getPlainText(self.xmlKey + "_TEXT", self.title)
		self.tooltip = BugUtil.getPlainText(self.xmlKey + "_HOVER", self.tooltip)
		if self.isDll():
			if BugDll.isVersion(self.dll):
				self.tooltip = RE_DLL_ALL_TAGS.sub("", self.tooltip)
			else:
				if not BugDll.isPresent():
					dllText = BugUtil.getPlainText("TXT_KEY_BULL_REQUIRED")
				else:
					dllText = BugUtil.getPlainText("TXT_KEY_BULL_REQUIRED_NEWER")
				if self.tooltip.find("[DLL") >= 0:
					self.tooltip = RE_DLL_START_END_TAGS.sub("", self.tooltip)
					self.tooltip = RE_DLL_MSG_TAG.sub(dllText, self.tooltip)
				else:
					self.tooltip += "\n" + dllText
		elif self.tooltip.find("[DLL") >= 0:
			if not BugDll.isPresent():
				# no DLL, ignore all minimum versions and use standard error message
				self.tooltip = RE_DLL_START_END_TAGS.sub("", self.tooltip)
				self.tooltip = RE_DLL_MSG_TAG.sub(BugUtil.getPlainText("TXT_KEY_BULL_REQUIRED"), self.tooltip)
			else:
				dllText = BugUtil.getPlainText("TXT_KEY_BULL_REQUIRED_NEWER")
				def repl(matchobj):
					try:
						if BugDll.isVersion(int(matchobj.group(1))):
							return ""
						else:
							return RE_DLL_MSG_TAG.sub(dllText, matchobj.group(2))
					except:
						# invalid version
						return ""
				self.tooltip = RE_DLL_CAPTURE_VERSION_MESSAGE.sub(repl, self.tooltip)
		self.translated = True
	
	def clearTranslation(self):
		"Marks this option so that it will be translated again the next time it is accessed"
		self.translated = False
	
	
	def onChanged(self, *args):
		if not BugInit.g_initRunning:
			self.doDirties(*args)
	
	def addDirty(self, obj):
		if isinstance(obj, types.FunctionType):
			self.addDirtyFunction(obj)
		else:
			self.addDirtyBit(obj)
	
	def addDirtyBit(self, bit):
		"""Adds a dirty function to the list."""
		if self.dirtyBits is None:
			self.dirtyBits = []
		if isinstance(bit, types.StringTypes):
			self.dirtyBits.extend(map(lambda b: getattr(InterfaceDirtyBits, b + "_DIRTY_BIT"), 
									  bit.replace(",", " ").split()))
		else:
			self.dirtyBits.append(bit)
	
	def addDirtyFunction(self, function):
		"""Adds a dirty function to the list."""
		if self.dirtyFunctions is None:
			self.dirtyFunctions = [function]
		else:
			self.dirtyFunctions.append(function)
	
	def doDirties(self, *args):
		"""Sets the dirty bits and calls the dirty functions."""
		self.applyDirtyBits(*args)
		self.callDirtyFunctions(*args)
	
	def applyDirtyBits(self, *args):
		if self.dirtyBits:
			interface = CyInterface()
			for bit in self.dirtyBits:
				interface.setDirty(bit, True)
	
	def callDirtyFunctions(self, *args):
		if self.dirtyFunctions:
			value = self.getValue()
			for func in self.dirtyFunctions:
				func(self, value)


LIST_TYPES = ("string", "int", "float", "color")
TYPE_DEFAULT_LIST_TYPE = { "int": "int",
						   "float": "float",
						   "string": "color",
						   "color": "color" }
LIST_TYPE_DEFAULT_TYPE = { "string": "int", 
						   "int": "int", 
						   "float": "float", 
						   "color": "color" }

class BaseListOption(BaseOption):
	"""
	Adds a list of possible values to a single option and a display format to use
	when creating the dropdown listbox in the Options Screen.
	"""

	def __init__(self, mod, id, type=None, default=None, andId=None, dll=None, 
				 listType="string", values=None, format=None, 
				 title=None, tooltip=None, dirty=None):
		if listType and listType not in LIST_TYPES:
			raise BugUtil.ConfigError("Invalid option list type: %s", listType)
		if not type:
			if not listType:
				raise BugUtil.ConfigError("Both types for option list are None")
			type = LIST_TYPE_DEFAULT_TYPE[listType]
		if type not in TYPE_DEFAULT_LIST_TYPE:
			raise BugUtil.ConfigError("Invalid option type for list: %s", type)
		
		super(BaseListOption, self).__init__(mod, id, type, default, andId, dll, title, tooltip, dirty)
		if not listType:
			listType = TYPE_DEFAULT_LIST_TYPE[type]
		self.listType = listType
		
		self.valuesXmlKey = None
		if values is not None:
			self.setValues(values)
		else:
			self.values = []
		self.format = format
		self.displayValues = None
		self.getters = None
	
	def createLinkedOption(self, mod, id):
		return LinkedListOption(mod, id, self)
	
	def getListType(self):
		return self.listType
	
	def isStringList(self):
		return self.listType == "string"
	
	def isIntList(self):
		return self.listType == "int"
	
	def isFloatList(self):
		return self.listType == "float"
	
	def isColorList(self):
		return self.listType == "color"
	
	def __str__(self):
		return "<%s %s [%s] list (%d %ss)>" % (self.id, self.type, str(self.default), len(self.values), self.listType)
	
	
	def getValues(self):
		return self.values
	
	def setValues(self, values):
		if isinstance(values, str):
			if self.isStringList():
				if values.find("|") != -1:
					self.values = values.split("|")
				else:
					self.values = []
					self.valuesXmlKey = "TXT_KEY_BUG_OPT_" + values.upper()
			elif self.isIntList():
				self.values = map(lambda x: int(x), values.replace(",", " ").split())
			elif self.isFloatList():
				self.values = map(lambda x: float(x), values.replace(",", " ").split())
			else:
				self.values = None
		else:
			self.values = values
		self.displayValues = None
	
	def addValue(self, value, getter=None, setter=None):
		if value in self.values:
			index = self.values.index(value)
			BugUtil.debug("BugOptions - value %s has index %s", value, index)
		else:
			index = len(self.values)
			self.values.append(value)
			BugUtil.debug("BugOptions - value %s appended at index %s", value, index)
		if self.displayValues is not None:
			self.displayValues.append(value)
		if getter:
			for name in getter.replace(",", " ").split():
				self.addGetter(name, index)
		if setter:
			# TODO: Change to addIndexSetter or pass in value instead of index
			self.addSetter(name, index)
	
	def addGetter(self, name, index):
		if self.getters is None:
			self.getters = {}
		self.getters.setdefault(name, []).append(index)
	
	def addSetter(self, name, value):
		self.createSetter(name, value)
	
	def createComparers(self):
		"""Creates all of the getters assigned to individual BaseListOption indices."""
		if self.getters:
			for name, values in self.getters.iteritems():
				# Munge values based on type or create different comparator functions
				self.createComparer(name, values)
	
	
	def getFormat(self):
		return self.format
	
	def setFormat(self, format):
		self.format = format
		if self.isIntList() or self.isFloatList():
			self.displayValues = None
	
	def getDisplayValues(self):
		if self.isStringList():
			if (not self.translated):
				self.translate()
		elif self.isColorList():
			return ColorUtil.getColorDisplayNames()
		else:
			self.buildDisplayValues()
		return self.displayValues
	
	def buildDisplayValues(self):
		if not self.displayValues:
			if self.format is None:
				if self.isIntList():
					format = "%d"
				else:
					format = "%f"
			else:
				format = self.format
			self.displayValues = map(lambda n: format % n, self.values)
	
	def translate(self):
		if self.isStringList():
			if self.valuesXmlKey:
				list = BugUtil.getPlainText(self.valuesXmlKey + "_LIST")
			else:
				list = BugUtil.getPlainText(self.xmlKey + "_LIST")
			if list:
				self.displayValues = list.split("|")
			else:
				self.displayValues = self.values
		super(BaseListOption, self).translate()
	

	def isValid(self, value):
		return value in self.values
	
	def getIndex(self, *args):
		value = self.getRealValue(*args)
		if self.isStringList():
			return value
		elif self.isColorList():
			return ColorUtil.keyToIndex(value)
		else:
			return self.findClosestIndex(value)
	
	def findClosestIndex(self, value):
		index = -1
		bestDelta = None
		for i, v in enumerate(self.values):
			delta = abs(value - v)
			if (bestDelta is None or delta < bestDelta):
				index = i
				bestDelta = delta
		return index
	
	def setIndex(self, index, *args):
		if self.isStringList():
			self.setValue(index, *args)
		elif self.isColorList():
			self.setValue(ColorUtil.indexToKey(index), *args)
		else:
			self.setValue(self.values[index], *args)


## ------ UNSAVED OPTIONS -----------------------------------------------------

class UnsavedMixin(object):
	"""
	Stores its value in memory only, never reading it from or writing it to disk.
	"""

	def __init__(self, value):
		"""Sets the value to the one passed in, typically the default value."""
		self.value = value
	
	def getRawValue(self, *args):
		return self.value
	
	def _setValue(self, value, *args):
		value = TYPE_MAP[self.type](value)
		BugUtil.debug("BugOptions - setting %s to %r", self.getID(), value)
		self.value = value
		return True

class UnsavedOption(UnsavedMixin, BaseOption):
	
	def __init__(self, mod, id, type, default=None, andId=None, dll=None, 
				 title=None, tooltip=None, dirty=None):
		BaseOption.__init__(self, mod, id, type, default, andId, dll, title, tooltip, dirty)
		UnsavedMixin.__init__(self, self.default)

class UnsavedListOption(UnsavedMixin, BaseListOption):
	
	def __init__(self, mod, id, type=None, default=None, andId=None, dll=None, 
				 listType="string", values=None, format=None, 
				 title=None, tooltip=None, dirty=None):
		BaseListOption.__init__(self, mod, id, type, default, andId, dll, listType, values, format, title, tooltip, dirty)
		UnsavedMixin.__init__(self, self.default)


## ------ INI FILE OPTIONS ----------------------------------------------------

TYPE_GETTER_MAP = { "boolean": IniFile.getBoolean,
					"string": IniFile.getString,
					"int": IniFile.getInt,
					"float": IniFile.getFloat,
					"color": IniFile.getString }
TYPE_SETTER_MAP = { "boolean": IniFile.setBoolean,
					"string": IniFile.setString,
					"int": IniFile.setInt,
					"float": IniFile.setFloat,
					"color": IniFile.setString }

class IniMixin(object):
	"""
	Stores its value in an INI file.
	"""

	def __init__(self, file, section, key):
		"""Stores the parameters for use with IniFile for accessing the value."""
		self.file = file
		self.section = section
		self.key = key
		file.addOption(self)

	def getFile(self):
		return self.file

	def getSection(self):
		return self.section

	def getKey(self):
		return self.key
	
	def isParameterized(self):
		return "%s" in self.key

	def hasValue(self, *args):
		if args:
			return self.file.exists(self.section, self.key % args)
		else:
			return self.file.exists(self.section, self.key)
	
	def getRawValue(self, *args):
		if args:
			return self.file.getRawValue(self.section, self.key % args)
		else:
			return self.file.getRawValue(self.section, self.key)
	
	def getRealValue(self, *args):
		if args:
			return TYPE_GETTER_MAP[self.type](self.file, self.section, self.key % args, self.default)
		else:
			return TYPE_GETTER_MAP[self.type](self.file, self.section, self.key, self.default)
	
	def _setValue(self, value, *args):
		"""Sets the actual value in the INI file."""
		BugUtil.debug("BugOptions - setting %s to %r", self.getID(), value)
		if args:
			return TYPE_SETTER_MAP[self.type](self.file, self.section, self.key % args, value)
		else:
			return TYPE_SETTER_MAP[self.type](self.file, self.section, self.key, value)

class IniOption(IniMixin, BaseOption):
	
	def __init__(self, mod, id, file, section, key, type, default=None, andId=None, dll=None, 
				 title=None, tooltip=None, dirty=None):
		BaseOption.__init__(self, mod, id, type, default, andId, dll, title, tooltip, dirty)
		IniMixin.__init__(self, file, section, key)

class IniListOption(IniMixin, BaseListOption):
	
	def __init__(self, mod, id, file, section, key, type=None, default=None, andId=None, dll=None, 
				 listType="string", values=None, format=None, 
				 title=None, tooltip=None, dirty=None):
		BaseListOption.__init__(self, mod, id, type, default, andId, dll, listType, values, format, title, tooltip, dirty)
		IniMixin.__init__(self, file, section, key)


## ------ LINKED OPTIONS ------------------------------------------------------

class LinkedOption(AbstractOption):
	
	"""Facade to an actual Option."""

	def __init__(self, mod, id, option):
		"""Sets the important fields of the new LinkedOption."""
		super(LinkedOption, self).__init__(mod, id)
		self.option = option
	
	def getOption(self):
		return self.option

	def getSection(self):
		return self.option.getSection()

	def getKey(self):
		return self.option.getKey()
	
	def getType(self):
		return self.option.getType()

	def getDefault(self):
		return self.option.getDefault()
	
	def __str__(self):
		return "<%s link: %s>" % (self.id, str(self.option))
	
	def getTitle(self):
		return self.option.getTitle()

	def getTooltip(self):
		return self.option.getTooltip()
	
	def clearTranslation(self):
		pass

	def hasValue(self, *args):
		return self.option.hasValue(*args)
	
	def getRawValue(self, *args):
		return self.option.getRawValue(*args)
	
	def getRealValue(self, *args):
		return self.option.getValue(*args)
	
	def _setValue(self, value, *args):
		return self.option._setValue(value, *args)


class LinkedListOption(LinkedOption):
	
	"""Facade to an actual ListOption."""

	def __init__(self, mod, id, option):
		"""Sets the important fields of the new LinkedListOption."""
		super(LinkedOption, self).__init__(mod, id, option)
	
	def getListType(self):
		return self.option.getListType()
	
	def isStringList(self):
		return self.option.isStringList()
	
	def isIntList(self):
		return self.option.isIntList()
	
	def isFloatList(self):
		return self.option.isFloatList()
	
	def isColorList(self):
		return self.option.isColorList()
	
	def getValues(self):
		return self.option.getValue()
	
	def setValues(self, values):
		pass
	
	def addValue(self, value, function=None):
		pass
	
	def addGetter(self, getter, index):
		pass
	
	def addSetter(self, name, value):
		pass
	
	def createComparers(self):
		pass
	
	def getFormat(self):
		return self.option.getFormat()
	
	def setFormat(self, format):
		pass
	
	def getDisplayValues(self):
		return self.option.getDisplayValues()
	
	def translate(self):
		pass

	def isValid(self, value):
		return self.option.isValid(value)
	
	def getIndex(self, *args):
		return self.option.getIndex(*args)
	
	def findClosestIndex(self, value):
		return self.option.findClosestIndex(value)
	
	def setIndex(self, index, *args):
		self.option.setIndex(index, *args)


## Option IDs

MOD_OPTION_SEP = "__"

def qualify(modId, optionId):
	"""
	Returns a fully qualified option ID by inserting the mod's ID if necessary.
	"""
	if optionId is not None and modId is not None:
		if optionId.find(MOD_OPTION_SEP) == -1:
			return modId + MOD_OPTION_SEP + optionId
	return optionId

def unqualify(optionId):
	"""
	Returns an unqualified option ID by removing the mod's ID if necessary.
	"""
	if optionId is not None:
		pos = optionId.find(MOD_OPTION_SEP)
		if pos >= 0:
			return optionId[pos + 2:]
	return optionId


## Configuration

class OptionsHandler(BugConfig.Handler):
	
	TAG = "options"
	
	def __init__(self):
		BugConfig.Handler.__init__(self, self.TAG, "id file", SectionHandler.TAG)
		self.addAttribute("id", True)
		self.addAttribute("file", True)
	
	def handle(self, element, id, file):
		ini = IniFile(id, file)
		g_options.addFile(ini)
		element.setState("ini", ini)
	
	def complete(self, element):
		ini = element.getState("ini")
		if ini:
			ini.read()


class SectionHandler(BugConfig.Handler):
	
	TAG = "section"
	
	def __init__(self):
		BugConfig.Handler.__init__(self, self.TAG, "id name", (OptionHandler.TAG,))
		self.addExcludedAttribute("id")
		self.addAttribute("name", True, False, None, "id")
	
	def handle(self, element, name):
		element.setState("ini-section", name)


class BaseOptionHandler(BugConfig.Handler):
	
	def __init__(self, tag, validAttrs="", validChildren="", elementClass=BugConfig.Element):
		BugConfig.Handler.__init__(self, tag, validAttrs, validChildren, elementClass)
		self.addAttribute("id", True)
	
	def addOption(self, mod, option, getter, setter):
		# TODO: move next two lines to BaseOption ctor?
		g_options.addOption(option)
		mod._addOption(option)
		# TODO: add to option ctors
		option.createAccessorPair(getter, setter)
	
	def createOption(self, element, id, type, key, default, andId, dll, title, tooltip, dirtyBit, getter, setter):
		if type == "color":
			return self.createListOption(element, id, type, key, default, andId, dll, title, tooltip, dirtyBit, getter, setter, type, None, None)
		mod = element.getState("mod")
		id = qualify(mod._id, id)
		andId = qualify(mod._id, andId)
		dll = self.resolveDll(element, dll)
		option = None
		ini = element.getState("ini")
		if ini and not key:
			key = id
		if key:
			if not ini:
				BugUtil.warn("BugConfig - <option> %s outside <options> element has a key attribute; making it unsaved", id)
			else:
				section = element.getState("ini-section")
				if not section:
					BugUtil.warn("BugConfig - <option> %s inside <options> element must be inside a <section> element; making it unsaved", id)
				else:
					option = IniOption(mod, id, ini, section, key, type, default, andId, dll, title, tooltip, dirtyBit)
		if option is None:
			option = UnsavedOption(mod, id, type, default, andId, dll, title, tooltip, dirtyBit)
		self.addOption(mod, option, getter, setter)
		element.setState("option", option)
		return option
	
	def createListOption(self, element, id, type, key, default, andId, dll, title, tooltip, dirtyBit, getter, setter, listType, values, format):
		mod = element.getState("mod")
		id = qualify(mod._id, id)
		andId = qualify(mod._id, andId)
		dll = self.resolveDll(element, dll)
		option = None
		if key:
			ini = element.getState("ini")
			if not ini:
				BugUtil.warn("BugConfig - <list> %s outside <options> element has a key attribute; making it unsaved", id)
			else:
				section = element.getState("ini-section")
				if not section:
					BugUtil.warn("BugConfig - <list> %s inside <options> element must be inside a <section> element; making it unsaved", id)
				else:
					option = IniListOption(mod, id, ini, section, key, type, default, andId, dll, listType, values, format, title, tooltip, dirtyBit)
		if option is None:
			option = UnsavedListOption(mod, id, type, default, andId, dll, listType, values, format, title, tooltip, dirtyBit)
		self.addOption(mod, option, getter, setter)
		element.setState("option", option)
		return option


class OptionHandler(BaseOptionHandler):
	
	TAG = "option"
	
	def __init__(self):
		BaseOptionHandler.__init__(self, self.TAG, "id type key default and dll title label tooltip help dirty dirtyBit get set args", ())
		self.addAttribute("type", True)
		self.addAttribute("key")
		self.addAttribute("default")
		self.addAttribute("and")
		self.addAttribute("dll")
		self.addExcludedAttribute("title")
		self.addAttribute("label", False, False, None, "title")
		self.addExcludedAttribute("tooltip")
		self.addAttribute("help", False, False, None, "tooltip")
		self.addExcludedAttribute("dirty")
		self.addAttribute("dirtyBit", False, False, None, "dirtyBit")
		self.addAttribute("get")
		self.addAttribute("set")
		self.addExcludedAttribute("args")
	
	def handle(self, element, id, type, key, default, andId, dll, label, help, dirtyBit, getter, setter):
		self.createOption(element, id, type, key, default, andId, dll, label, help, dirtyBit, getter, setter)


class ListOptionHandler(BaseOptionHandler):
	
	TAG = "list"
	
	def __init__(self):
		BaseOptionHandler.__init__(self, self.TAG, "id type key default and dll title label tooltip help dirty dirtyBit get set args listType values format", ())
		self.addAttribute("type")
		self.addAttribute("key")
		self.addAttribute("default")
		self.addAttribute("and")
		self.addAttribute("dll")
		self.addExcludedAttribute("title")
		self.addAttribute("label", False, False, None, "title")
		self.addExcludedAttribute("tooltip")
		self.addAttribute("help", False, False, None, "tooltip")
		self.addExcludedAttribute("dirty")
		self.addAttribute("dirtyBit", False, False, None, "dirtyBit")
		self.addAttribute("get")
		self.addAttribute("set")
		self.addExcludedAttribute("args")
		self.addAttribute("listType")
		self.addAttribute("values")
		self.addAttribute("format")
	
	def handle(self, element, id, type, key, default, andId, dll, label, help, dirtyBit, getter, setter, listType, values, format):
		self.createListOption(element, id, type, key, default, andId, dll, label, help, dirtyBit, getter, setter, listType, values, format)
	
	def complete(self, element):
		element.getState("option").createComparers()


class ListChoiceHandler(BugConfig.Handler):
	
	TAG = "choice"
	
	def __init__(self):
		BugConfig.Handler.__init__(self, self.TAG, "id get set", ())
		self.addAttribute("id", True)
		self.addAttribute("get")
		self.addAttribute("set")
	
	def handle(self, element, id, getter, setter):
		option = element.getState("option")
		option.addValue(id, getter, setter)


class LinkedOptionHandler(BaseOptionHandler):
	
	TAG = "link"
	
	def __init__(self):
		BaseOptionHandler.__init__(self, self.TAG, "id to get set", ())
		self.addAttribute("to", True)
		self.addAttribute("get")
		self.addAttribute("set")
	
	def handle(self, element, id, to, getter, setter):
		mod = element.getState("mod")
		id = qualify(mod._id, id)
		to = qualify(mod._id, to)
		option = g_options.getOption(to)
		if option is not None:
			link = option.createLinkedOption(mod, id)
			self.addOption(mod, link, getter, setter)
		else:
			BugUtil.error("Option ID %s in element <%s> %s not found", to, element.tag, id)


class ChangeHandler(BugConfig.Handler):
	
	TAG = "change"
	
	def __init__(self):
		BugConfig.Handler.__init__(self, self.TAG, "dirtyBit module function")
		self.addAttribute("dirtyBit")
		self.addAttribute("module", False, True)
		self.addAttribute("function")
	
	def handle(self, element, dirtyBit, module, function):
		option = element.getState("option")
		if dirtyBit:
			option.addDirtyBit(dirtyBit)
		elif module and function:
			option.addDirtyFunction(BugUtil.getFunction(module, function, True))
		else:
			raise BugUtil.ConfigError("Element <%s> requires attribute dirtyBit or both module and function", element.tag)


class AccessorHandler(BugConfig.Handler):
	
	TAG = "accessor"
	
	def __init__(self):
		BugConfig.Handler.__init__(self, self.TAG, "id args get set", ())
		self.addAttribute("id", True)
		self.addAttribute("args")
		self.addAttribute("get")
		self.addAttribute("set")
	
	def handle(self, element, id, args, getter, setter):
		mod = element.getState("mod")
		mod._createParameterizedAccessorPair(id, getter, setter)
