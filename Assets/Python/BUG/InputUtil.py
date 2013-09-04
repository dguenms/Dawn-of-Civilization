## InputUtil
##
## Utilities for dealing with mouse and keyboard input.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugConfig
import BugDll
import BugUtil
import CvEventInterface
import types

KEY_MAP = {
	"'": "APOSTROPHE",
	"@": "AT",
	"\\": "BACKSLASH",
	"CAPS": "CAPSLOCK",
	":": "COLON",
	",": "COMMA",
	"DEL": "DELETE",
	"=": "EQUALS",
	"`": "GRAVE",
	"[": "LBRACKET",
	"-": "MINUS",
	".": "PERIOD",
	"]": "RBRACKET",
	";": "SEMICOLON",
	"/": "SLASH",
	" ": "SPACE",
	"_": "UNDERLINE",
	"+": "PLUS",  # not a valid key normally -- only with NUMPAD
}

ALT = 0
CONTROL = 1
SHIFT = 2

MODIFIER_MAP = {
	"ALT": ALT,
	"COMMAND": ALT,
	"CMD": ALT,
	"CONTROL": CONTROL,
	"CTRL": CONTROL,
	"SHIFT": SHIFT,
}

MODIFIER_KEYS = (
	InputTypes.KB_LALT, 
	InputTypes.KB_LCONTROL, 
	InputTypes.KB_LSHIFT, 
	InputTypes.KB_RALT, 
	InputTypes.KB_RCONTROL, 
	InputTypes.KB_RSHIFT,
	int(InputTypes.KB_LALT), 
	int(InputTypes.KB_LCONTROL), 
	int(InputTypes.KB_LSHIFT), 
	int(InputTypes.KB_RALT), 
	int(InputTypes.KB_RCONTROL), 
	int(InputTypes.KB_RSHIFT),
)

KEYS_BY_CODE = {}
CODES_BY_KEY = {}

ALT_HASH = 256
CONTROL_HASH = 512
SHIFT_HASH = 1024

def isModifier(key):
	return key in MODIFIER_KEYS

def codeToKey(code):
	return KEYS_BY_CODE[code]

def keyToCode(key):
	return CODES_BY_KEY[key]


def stringToKeystroke(key):
	"""
	Returns a Keystroke created from the given string.
	
	It can contain modifiers (alt, control, shift) separated from the key with spaces.
	"""
	if not isinstance(key, types.StringTypes):
		raise BugUtil.ConfigError("key must be a string")
	keys = key.split()
	input = None
	modifiers = [False, False, False]
	for part in keys:
		k = part.upper()
		if k in MODIFIER_MAP:
			modifiers[MODIFIER_MAP[k]] = True
		else:
			if k.startswith("NUMPAD") or k.startswith("NUM") or k.startswith("NP"):
				if k.startswith("NUMPAD"):
					k = k[6:]
				elif k.startswith("NUM"):
					k = k[3:]
				else:
					k = k[2:]
				if k in KEY_MAP:
					k = KEY_MAP[k]
				k = "KB_NUMPAD" + k
			else:
				if k in KEY_MAP:
					k = KEY_MAP[k]
				k = "KB_" + k
			try:
				input = getattr(InputTypes, k)
			except KeyError:
				raise BugUtil.ConfigError("invalid key %s from %s" % (part, key))
	if input is None:
		raise BugUtil.ConfigError("invalid key %s (only modifiers)" % key)
	return Keystroke(input, *modifiers)

def stringToKeystrokes(keys):
	"""
	Returns a list of Keystrokes created from the given string.
	
	Individual keystrokes must be separated by a vertical bar (|).
	"""
	result = []
	for key in keys.split("|"):
		result.append(stringToKeystroke(key))
	return result


class Keystroke:
	"""
	Holds the information necessary to recognize a single keystroke,
	including modifiers: alt, control, and shift.
	"""
	def __init__(self, keyOrCode, alt=False, control=False, shift=False):
		if isinstance(keyOrCode, int):
			self.code = keyOrCode
		elif isinstance(keyOrCode, InputTypes):
			self.code = int(keyOrCode)
		else:
			raise BugUtil.ConfigError("key %r must be an InputTypes constant or int" % keyOrCode)
		self.alt = alt
		self.control = control
		self.shift = shift
		self.hash = None
	
	def __str__(self):
		s = ""
		if self.alt:
			s += "ALT + "
		if self.control:
			s += "CTRL + "
		if self.shift:
			s += "SHIFT + "
		return "%s%s" % (s, codeToKey(self.code))
	
	def __repr__(self):
		return "<key %s>" % str(self)
	
	def __hash__(self):
		if self.hash is None:
			self.hash = self.code
			if self.alt:
				self.hash ^= ALT_HASH
			if self.control:
				self.hash ^= CONTROL_HASH
			if self.shift:
				self.hash ^= SHIFT_HASH
		return self.hash
	
	def __eq__(self, other):
		if not isinstance(other, Keystroke):
			return NotImplemented
		return (self.code == other.code and self.alt == other.alt and
			    self.control == other.control and self.shift == other.shift)
	
	def __ne__(self, other):
		if not isinstance(other, Keystroke):
			return NotImplemented
		return (self.code != other.code or self.alt != other.alt or
			    self.control != other.control or self.shift != other.shift)


def init():
	for k, c in InputTypes.__dict__.iteritems():
		if k.startswith("KB_"):
			key = k[3:]
			code = int(c)
			KEYS_BY_CODE[code] = key
			CODES_BY_KEY[key] = code
			CODES_BY_KEY[k] = code

# initialize when the module is loaded
init()


## configuration handler

class ShortcutHandler(BugConfig.HandlerWithArgs):
	
	TAG = "shortcut"
	
	def __init__(self):
		BugConfig.HandlerWithArgs.__init__(self, ShortcutHandler.TAG, "key keys module function dll")
		self.addExcludedAttribute("key")
		self.addAttribute("keys", True, False, None, "key")
		self.addAttribute("module", True, True)
		self.addAttribute("function", True)
		self.addAttribute("dll")
	
	def handle(self, element, keys, module, function, dll):
		dll = BugDll.decode(dll)
		if self.isDllOkay(element, dll):
			CvEventInterface.getEventManager().addShortcutHandler(keys, BugUtil.getFunction(module, function, *element.args, **element.kwargs))
		else:
			BugUtil.info("InputUtil - ignoring <%s> %s, requires dll version %s", element.tag, keys, self.resolveDll(element, dll))
