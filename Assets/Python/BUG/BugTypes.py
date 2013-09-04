## BugTypes
##
## Provides functions for dealing with types and values in XML and INI files.
##
## normalize(type)
##   Returns the canonical type or raises an exception if not found.
##
## default(type)
##   Returns the default value for <type> after normalizing it.
##
## isTrue(value, noneIsFalse=True)
##   Returns True if <value> is one of the valid string representations for True.
##
## to(type, value, noneIsDefault=True, emptyIsDefault=True)
##   Converts <value> from a string to <type>.
##
## TODO
##
##   Create ability to add new types. Add "key" type.
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: EmperorFool

import BugUtil

# BUG - Mac Support - start
BugUtil.fixSets(globals())
# BUG - Mac Support - end


## Type Constants

NONE = "none"

BOOL = "boolean"
BOOLEAN = BOOL
INT = "int"
INTEGER = INT
FLOAT = "float"
REAL = FLOAT
STRING = "string"
COLOR = "color"

TUPLE = "tuple"
LIST = "list"
SET = "set"
DICT = "dict"


## Normalizing Types

NORMALIZED_TYPES = {
	BOOL: BOOL,
	"bool": BOOL,
	"bit": BOOL,
	INT: INT,
	"integer": INT,
	"long": INT,
	"number": INT,
	FLOAT: FLOAT,
	"real": FLOAT,
	"double": FLOAT,
	"decimal": FLOAT,
	STRING: STRING,
	"str": STRING,
	COLOR: COLOR,
	
	TUPLE: TUPLE,
	"vector": TUPLE,
	LIST: LIST,
	"array": LIST,
	SET: SET,
	DICT: DICT,
	"map": DICT,
}

def normalize(type):
	"""
	Returns the canonical type or raises an exception if not found.
	
	If <type> is None or empty (""), returns None.
	"""
	if not type:
		return None
	try:
		return NORMALIZED_TYPES[type.lower()]
	except:
		raise BugUtil.ConfigError("Invalid type %s", type)


## Defaults

DEFAULT_CONSTANT = 0
DEFAULT_FUNCTION = 1

DEFAULTS = {
	BOOL: (DEFAULT_CONSTANT, False),
	INT: (DEFAULT_CONSTANT, 0),
	FLOAT: (DEFAULT_CONSTANT, 0.0),
	STRING: (DEFAULT_CONSTANT, ""),
	COLOR: (DEFAULT_CONSTANT, "COLOR_WHITE"),
	TUPLE: (DEFAULT_CONSTANT, ()),
	LIST: (DEFAULT_FUNCTION, list),
	SET: (DEFAULT_FUNCTION, set),
	DICT: (DEFAULT_FUNCTION, dict),
}

def default(type):
	"""
	Returns the default value for <type> after normalizing it.
	
	If <type> is None or empty (""), None is returned.
	"""
	type = normalize(type)
	if not type:
		return None
	try:
		form, default = DEFAULTS[type]
	except KeyError:
		raise BugUtil.ConfigError("Invalid type %s", type)
	else:
		if form == DEFAULT_CONSTANT:
			return default
		else:
			return default()


## Converting Values

TRUE_STRINGS = ('true', 't', 'yes', 'y', 'on', '1')

CONVERT_FROM_STRING = {
	BOOL: lambda x: x.lower() in TRUE_STRINGS,
	STRING: lambda x: x,
	INT: lambda x: int(x),
	FLOAT: lambda x: float(x),
	COLOR: lambda x: x,
	TUPLE: lambda x: eval("(%s,)" % x),
	LIST: lambda x: eval("[%s]" % x),
	SET: lambda x: eval("set([%s])" % x),
	DICT: lambda x: eval("{%s}" % x),
}

def isTrue(value, noneIsFalse=True):
	"""
	Returns True if <value> is one of the valid string representations for True.
	
	By default, None is considered False.
	"""
	if not value:
		if noneIsFalse:
			return False
		else:
			return None
	else:
		return value.lower() in TRUE_STRINGS

def to(type, value, noneIsDefault=True, emptyIsDefault=True):
	"""
	Converts <value> from a string to <type>.
	
	If <type> is None or empty (""), the value is evaluated directly using eval();
	otherwise <type> is normalized first. If <value> is None or empty ("") as well,
	the special value None is returned.
	
	If <value> is None or empty (""), the default is used based on the optional parameters.
	
	The <type> is normalized first, and line endings (\r\n) are replaced with spaces in <value>.
	"""
	if type:
		if not value:
			if (value is None and noneIsDefault) or (value == "" and emptyIsDefault):
				return default(type)
			else:
				return None
		else:
			try:
				return CONVERT_FROM_STRING[normalize(type)](value.replace("\r\n", " "))
			except KeyError:
				raise BugUtil.ConfigError("Invalid type %s", type)
			except:
				raise BugUtil.ConfigError("Invalid %s: %s", type, value)
	else:
		if value:
			try:
				return eval(value)
			except:
				raise BugUtil.ConfigError("Invalid expression %s", value)
		else:
			return None
