## FontUtil
##
## Utilities for dealing with FontSymbols, "XXX_CHAR" keys, and "[ICON_XXX]" tags in XML messages.
## "init.xml" adds most of the built-in and BUG-related symbol keys by using this module's functions.
## You can add your own using the <symbol> XML entity.
##
## Getting Symbols
##
##   getSymbol(symbolOrKey)
##     Returns a FontSymbols instance matching the given symbol or key.
##     If passed a FontSymbols instance, it is returned. If a string, it is looked
##     up in this modules list of known symbols.
##
##   getChar(symbolOrKey)
##     Returns a string containing a single-character for the desired <symbolOrKey>.
##
##   getOrdinal(symbolOrKey)
##     Returns the Unicode ordinal for the desired <symbolOrKey>.
##
## Message Processing
##
##   replaceSymbols(text, unknownReplacement)
##     Returns a copy of <text> after replacing all occurrances of "[ICON_XXX]" with
##     the symbols registered in this module. Any symbol that isn't found is replaced
##     with <unknownReplacement> (default "").
##
## Notes
##   - Must be initialized externally by calling init()
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugConfig
import BugDll
import BugUtil
import CvUtil
import re

## constants

UNKNOWN_CHAR = "?"
SYMBOL_REGEXP = re.compile(r"\[ICON_([a-zA-Z0-9_]+)\]")

## globals

gc = CyGlobalContext()
nextSymbolID = int(FontSymbols.MAX_NUM_SYMBOLS)

# key -> symbol (FontSymbols)
keySymbols = {}

# symbol -> primary key (string)
symbolPrimaryKeys = {}

# symbol -> ordinal (int)
symbolOrdinals = {}

# symbol -> character (unicode string)
symbolChars = {}

## initialization and registration

def init():
	symbolNames = {}
	for name, symbol in FontSymbols.__dict__.iteritems():
		if name.endswith("_CHAR") and isinstance(symbol, FontSymbols):
			symbolNames[symbol] = name
	for key, symbol in CvUtil.OtherFontIcons.iteritems():
		addBuiltinSymbol(key, symbol)
		if symbol in symbolNames:
			name = symbolNames[symbol]
			registerSymbolSynonym(key, symbol, name[:-5])
			registerSymbolSynonym(key, symbol, name)
#			del symbolNames[symbol]
	# add the FontSymbols that aren't in CvUtil
#	for symbol, name in symbolNames:
#		addBuiltinSymbol()
	
	for count, getInfo in (
		(YieldTypes.NUM_YIELD_TYPES, gc.getYieldInfo),
		(CommerceTypes.NUM_COMMERCE_TYPES, gc.getCommerceInfo),
	):
		for enum in range(count):
			info = getInfo(enum)
			addSymbol(info.getType().lower().replace("_", " "), 
					info.getChar(), info.getType())

def addBuiltinSymbol(key, symbol):
	registerSymbol(key, symbol, gc.getGame().getSymbolID(symbol))

def addOffsetSymbol(key, symbolOrKey, offset, name=None):
	return addSymbol(key, getOrdinal(symbolOrKey) + offset, name)

def addSymbol(key, ordinal, name=None):
	if not name:
		name = key.upper().replace(" ", "_")
	else:
		name = name.upper().replace(" ", "_")
	symbolName = name + "_CHAR"
	symbol = findOrCreateSymbol(symbolName)
	registerSymbol(key, symbol, ordinal)
	registerSymbolSynonym(key, symbol, name)
	registerSymbolSynonym(key, symbol, symbolName)
	return symbol

def findOrCreateSymbol(name):
	try:
		symbol = getattr(FontSymbols, name)
		if isinstance(symbol, FontSymbols):
			BugUtil.debug("FontUtil - found FontSymbols name %s", name)
			return symbol
	except AttributeError:
		pass
	# create a FontSymbols enum for it
	global nextSymbolID
	symbol = FontSymbols(nextSymbolID)
	nextSymbolID += 1
	BugUtil.debug("FontUtil - created FontSymbols.%s", name)
	setattr(FontSymbols, name, symbol)
	return symbol

def registerSymbol(key, symbol, ordinal):
	BugUtil.info("FontUtil - registering symbol '%s' for %d", key, ordinal)
	if key in keySymbols:
		raise BugUtil.ConfigError("duplicate font symbol key '%s'" % key)
	if symbol in symbolPrimaryKeys:
		raise BugUtil.ConfigError("duplicate font symbol for key '%s'" % key)
	keySymbols[key] = symbol
	symbolPrimaryKeys[symbol] = key
	symbolOrdinals[symbol] = ordinal
	symbolChars[symbol] = u"%c" % ordinal
	
def registerSymbolSynonym(key, symbol, synonym):
	if synonym in keySymbols:
		BugUtil.warn("FontUtil - ignoring duplicate synonym '%s' for key '%s'", synonym, key)
	else:
		BugUtil.debug("FontUtil - registering synonym '%s'", synonym)
		keySymbols[synonym] = symbol


## symbol lookup

def getSymbol(symbolOrKey):
	if isinstance(symbolOrKey, FontSymbols):
		return symbolOrKey
	try:
		return keySymbols[symbolOrKey]
	except KeyError:
		try:
			return keySymbols[symbolOrKey.upper() + "_CHAR"]
		except KeyError:
			raise BugUtil.ConfigError("unknown font symbol or key '%s'" % str(symbolOrKey))

def getOrdinal(symbolOrKey):
	try:
		return symbolOrdinals[getSymbol(symbolOrKey)]
	except KeyError:
		raise BugUtil.ConfigError("unknown font symbol or key '%s'" % str(symbolOrKey))

def getChar(symbolOrKey):
	try:
		return symbolChars[getSymbol(symbolOrKey)]
	except KeyError:
		raise BugUtil.ConfigError("unknown font symbol or key '%s'" % str(symbolOrKey))


## message processing

def replaceSymbols(text, unknownReplacement=""):
	def replace(match):
		try:
			return getChar(match.group(1))
		except BugUtil.ConfigError:
			return unknownReplacement
	return SYMBOL_REGEXP.sub(replace, text)


## configuration handler

class SymbolHandler(BugConfig.Handler):
	
	TAG = "symbol"
	
	def __init__(self):
		BugConfig.Handler.__init__(self, SymbolHandler.TAG, "id name from offset dll")
		self.addAttribute("id", True)
		self.addAttribute("name")
		self.addAttribute("from")
		self.addAttribute("offset")
		self.addAttribute("dll")
		self.lastSymbol = None
	
	def handle(self, element, id, name, fromKey, offset, dll):
		dll = BugDll.decode(dll)
		if self.isDllOkay(element, dll):
			if not fromKey:
				if not self.lastSymbol:
					raise BugUtil.ConfigError("<%s> %s requires an offset symbol" % (element.tag, id))
				fromKey = self.lastSymbol
			if offset is None:
				offset = 1
			else:
				offset = int(offset)
			self.lastSymbol = addOffsetSymbol(id, fromKey, offset, name)
		else:
			BugUtil.info("FontUtil - ignoring <%s> %s, requires dll version %s", element.tag, id, self.resolveDll(element, dll))
