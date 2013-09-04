## BugConfig
##
## Parses a BUG configuration XML file to initialize BUG and its mod components.
##
## This module contains element handler base classes that other components
## can use to build specific handlers. While reading a file, the parser keeps
## a stack of nested elements and their handlers which other handlers can
## access to pull inherited information.
##
## For example, the root <bug> element can define a "module" attribute that
## can be inherited by child elements that require one. These inherited
## attributes can be overridden by any element in the nesting, and the new
## value will only apply to it and its children.
##
## Inherited attributes can issue a warning when the overriding value
## doesn't make sense given the context, for example lowering the DLL
## API version. Inherited attributes may be cleared by specifying
## an empty value, e.g. <init dll=""/>.
##
## TODO
## 
##   - Remove child attributes from ctor
##   - Change child tags to child handlers and remove from ctor
##   - Register using keys instead of tags
##   - Fallback attributes should create their fallbacks automatically
##   - Don't register root handler
##   - Move elements here closer to where their modules are initialized in XML
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: EmperorFool

import BugCore
import BugDll
import BugInit
import BugTypes
import BugUtil
import CvEventInterface
import types

# BUG - Mac Support - start
BugUtil.fixSets(globals())
# BUG - Mac Support - end


# Constants

BLOCK_SIZE = 512


## Parsing Dispatcher

# block error alert about xmllib deprecation
try:
	import sys
	stderr = sys.stderr
	sys.stderr = sys.stdout
	import xmllib
finally:
	sys.stderr = stderr

class ConfigParser(xmllib.XMLParser):
	
	def __init__(self):
		xmllib.XMLParser.__init__(self)
	
	def parse(self, path):
		self._path = path
		self.start()
		try:
			file = open(path)
			try:
				while True:
					s = file.read(BLOCK_SIZE)
					if not s:
						break
					self.feed(s)
				self.close()
			finally:
				file.close()
		except IOError:
			BugUtil.trace("BugConfig - IOError parsing %s", path)
			raise
		except BugUtil.ConfigError:
			BugUtil.trace("BugConfig - failure parsing %s at line %d", path, self.lineno)
			raise
		except:
			BugUtil.trace("BugConfig - failure parsing %s at line %d", path, self.lineno)
			raise
	
	def start(self):
		self._handler = g_rootHandler
		self._element = g_rootHandler.start()
		self._stack = [(self._handler, self._element)]
	
	def unknown_starttag(self, tag, attrs):
		try:
			#BugUtil.debug("BugConfig - %s", self.format(tag, attrs))
			self._handler, self._element = self._handler.startChild(self._element, tag, attrs)
			self._stack.append((self._handler, self._element))
		except:
			BugUtil.trace("BugConfig - failure parsing %s at line %d" % (self._path, self.lineno))
	
	def unknown_endtag(self, tag):
		try:
			#BugUtil.debug("BugConfig - end <%s>", tag)
			handler, element = self._stack.pop()
			if self._stack:
				self._handler, self._element = self._stack[-1]
				self._handler.endChild(self._element, handler, element)
			else:
				self._handler = None
				self._element = None
				handler.end(element)
		except:
			BugUtil.trace("BugConfig - failure parsing %s at line %d" % (self._path, self.lineno))
	
	def handle_data(self, data):
		self._element.addText(data)
	
	def syntax_error(self, message):
		raise BugUtil.ConfigError("error parsing configuration: %s", message)

	def format(self, tag, attrs):
		xml = "<" + tag
		for key, value in attrs.iteritems():
			xml += " " + key + "=\"" + value + "\""
		xml += ">"
		return xml


## Element State Tracking

class Element:
	
	def __init__(self, handler, parent, tag, attrs={}, saveText=False):
		self.handler = handler
		self.parent = parent
		self.tag = tag
		self.attrs = attrs
		self.flatAttrs = {}
		self.processed = False
		self.state = {}
		if saveText:
			self.text = ""
		else:
			self.text = None
	
	def addText(self, text):
		if self.text is not None:
			self.text += text
	
	def hasAttribute(self, name):
		return name in self.attrs
	
	def getAttribute(self, name, default=None, inherit=False):
		if self.hasAttribute(name):
			return self.attrs[name]
		if inherit:
			return self.getInheritedAttribute(name, default)
		else:
			return default
	
	def getInheritedAttribute(self, name, default=None):
		if self.parent:
			return self.parent.getAttribute(name, default, True)
		else:
			return default
	
	def getRequiredAttribute(self, name, inherit=False):
		value = self.getAttribute(name, None, inherit)
		if value is not None:
			return value
		else:
			raise BugUtil.ConfigError("Element <%s> requires attribute %s", self.tag, name)
	
	def getRequiredInheritedAttribute(self, name):
		value = self.getInheritedAttribute(name, None)
		if value is not None:
			return value
		else:
			raise BugUtil.ConfigError("Element <%s> requires inherited attribute %s", self.tag, name)
	
	def getFlatAttribute(self, name):
		return self.flatAttrs.get(name)
	
	def setFlatAttribute(self, name, value):
		self.flatAttrs[name] = value
	
	def isProcessed(self):
		return self.processed
	
	def setProcessed(self, value):
		self.processed = value
	
	def setState(self, key, value):
		self.state[key] = value
	
	def getState(self, key):
		if key in self.state:
			return self.state[key]
		elif self.parent:
			return self.parent.getState(key)
		else:
			return None

class ElementWithArgs(Element):
	
	def __init__(self, handler, parent, tag, attrs={}, saveText=False):
		Element.__init__(self, handler, parent, tag, attrs, saveText)
		self.args = []
		self.kwargs = {}


## Handler Registration

g_handlers = {}

def registerHandler(tag, handler):
	BugUtil.debug("BugConfig - registering %s handler %s", tag, handler.__class__)
	g_handlers[tag] = handler

def isRegistered(tag):
	return tag in g_handlers

def getHandler(tag):
	try:
		return g_handlers[tag]
	except KeyError:
		raise BugUtil.ConfigError("unknown configuration element %s", tag)


## Handler Base Classes

class Handler:
	
	def __init__(self, tag, validAttrs="", validChildren="", elementClass=Element):
		self.tag = tag
		self.attributes = []
		self.validAttrs = set(validAttrs.split())
		if isinstance(validChildren, types.StringTypes):
			validChildren = validChildren.split()
		self.validChildren = set(validChildren)
		self.accumulatedTags = set()
		self.elementClass = elementClass
	
	def addValidAttribute(self, name):
		self.validAttrs.add(name)
	
	def addAttribute(self, name, required=False, inherited=False, default=None, fallback=None, exclude=False):
		self.attributes.append((name, required, inherited, default, fallback, exclude))
	
	def addExcludedAttribute(self, name, inherited=False, default=None, fallback=None):
		self.addAttribute(name, False, inherited, default, fallback, True)
	
	def setAttribute(self, name, *values):
		for i in range(len(self.attributes)):
			attr = self.attributes[i]
			if attr[0] == name:
				attr = list(attr)
				for j in range(len(values)):
					if j > 4:
						break
					attr[j + 1] = values[j]
				break
		else:
			raise BugUtil.ConfigError("Missing attribute %s", name)
	
	def isValidAttribute(self, name):
		return name in self.validAttrs
	
	def addValidChild(self, tag, accumuated=False):
		self.validChildren.add(tag)
		if accumuated:
			self.accumulatedTags.add(tag)
	
	def addAccumulatedChild(self, tag):
		self.addValidChild(tag, True)
	
	def isValidChild(self, tag):
		return tag in self.validChildren
	
	def getChildHandler(self, tag):
		return getHandler(tag)
	
	def start(self, parent=None, tag=None, attrs={}):
		self.validate(parent, tag, attrs)
		element = self.createElement(parent, tag, attrs)
		self.flatten(element)
		return element
	
	def validate(self, parent, tag, attrs):
		for attr in attrs:
			if not self.isValidAttribute(attr):
				BugUtil.warn("BugConfig - invalid <%s> attribute %s", tag, attr)
	
	def createElement(self, parent, tag, attrs):
		return self.elementClass(self, parent, tag, attrs, self.isSaveText(tag, attrs))
	
	def isSaveText(self, tag, attrs):
		return False
	
	def flatten(self, element):
		for (name, required, inherit, default, fallback, exclude) in self.attributes:
			if default is None and fallback:
				default = element.getFlatAttribute(fallback)
			value = element.getAttribute(name, default, inherit)
			if value is None and required:
				raise BugUtil.ConfigError("Element <%s> requires attribute '%s'", element.tag, name)
			element.setFlatAttribute(name, value)
	
	def process(self, element):
		if not element.isProcessed():
			values = []
			for attr in self.attributes:
				if not attr[5]:
					values.append(element.getFlatAttribute(attr[0]))
			self.handle(element, *values)
			element.setProcessed(True)
	
	def handle(self, element, *values):
		pass
	
	def startChild(self, parentElement, tag, attrs):
		if not self.isValidChild(tag):
			raise BugUtil.ConfigError("Element <%s> does not accept child <%s>", parentElement.tag, tag)
		if tag not in self.accumulatedTags:
			self.process(parentElement)
		handler = self.getChildHandler(tag)
		element = handler.start(parentElement, tag, attrs)
		return (handler, element)
	
	def endChild(self, parentElement, handler, element):
		handler.end(element)
	
	def end(self, element):
		self.process(element)
		self.complete(element)
	
	def complete(self, element):
		pass
	
	def isDllOkay(self, element, dll):
		dll = self.resolveDll(element, dll)
		if dll is not None:
			element.setState("dll", dll)
			return BugDll.isVersion(dll)
		return True
	
	def resolveDll(self, element, dll):
		dll = BugDll.decode(dll)
		inherited = element.getState("dll")
		if dll is None:
			return inherited
		if inherited is None:
			return dll
		if inherited > dll:
			BugUtil.warn("BugConfig - element <%s>.dll attribute %s overrides newer inherited dll attribute %s" % (element.tag, dll, inherited))
		return dll
	
	def isTrue(self, value):
		return BugTypes.isTrue(value)
	
	def createValue(self, type, value):
		return BugTypes.to(type, value)

class HandlerWithArgs(Handler):
	
	def __init__(self, tag, validAttrs="", validChildren=""):
		Handler.__init__(self, tag, validAttrs, validChildren, ElementWithArgs)
		self.addAccumulatedChild(ArgHandler.TAG)


## Core Handlers

class RootHandler(Handler):
	
	TAG = "xml"
	
	def __init__(self):
		Handler.__init__(self, self.TAG, "", (BugHandler.TAG, ModHandler.TAG))

class BugHandler(Handler):
	
	TAG = "bug"
	
	def __init__(self):
		Handler.__init__(self, self.TAG, "module dll", (LoadHandler.TAG, ConfigHandler.TAG, ModHandler.TAG, ))
		self.addAttribute("module")
		self.addAttribute("dll")
	
	def handle(self, element, module, dll):
		dll = BugDll.decode(dll)
		element.setState("dll", dll)
		if module and dll:
			BugUtil.debug("BugConfig - configuration for module %s requires DLL version %s", module, dll)

class LoadHandler(Handler):
	
	TAG = "load"
	
	def __init__(self):
		Handler.__init__(self, self.TAG, "name mod")
		self.addExcludedAttribute("mod")
		self.addAttribute("name", True, False, None, "mod")
	
	def handle(self, element, name):
		BugUtil.debug("BugConfig - loading mod file %s", name)
		BugInit.loadMod(name)

class ConfigHandler(Handler):
	
	TAG = "config"
	
	def __init__(self):
		Handler.__init__(self, self.TAG, 
				"root tag key parents module class", ConfigHandler.TAG)
		self.addAttribute("root")
		self.addAttribute("tag", True, False, None, "root")
		self.addAttribute("key", True, False, None, "tag")
		self.addAttribute("parents")
		self.addAttribute("module", True, True, None, "root")
		self.addAttribute("class", True, False, None, "root")
		#addChildHandler(self)
	
	def handle(self, element, root, tag, key, parents, module, clazz):
		if root:
			element.setState("config-handler", getHandler(root))
		else:
			if isRegistered(key):
				BugUtil.warn("BugConfig - <%s>.key %s handler already registered, ignoring", element.tag, key)
			else:
				handler = BugUtil.callFunction(module, clazz)
				registerHandler(tag, handler)
				# automatically include in enclosing <config> handler
				parent = element.getState("config-handler")
				if parent:
					parentHandlers = [parent]
				else:
					parentHandlers = []
				# add listed parents
				if parents:
					for parent in parents.split():
						if parent == "-":
							parentHandlers = []
						else:
							parentHandlers.append(getHandler(parent))
				# place in bug handler if none specified
				if not parentHandlers:
					parentHandlers.append(g_bugHandler)
				# register with each parent handler
				for parent in parentHandlers:
					parent.addValidChild(tag)
					#parent.addChildHandler(handler)
				element.setState("config-handler", handler)

class ArgHandler(Handler):
	
	TAG = "arg"
	
	def __init__(self):
		Handler.__init__(self, self.TAG, "name type value")
		self.addAttribute("name")
		self.addAttribute("type")
		self.addAttribute("value")
	
	def isSaveText(self, tag, attrs):
		return "value" not in attrs
	
	def handle(self, element, name, type, value):
		# create argument and store on element.parent
		if value is None:
			value = element.text
		arg = self.createValue(type, value)
		if name:
			element.parent.kwargs[name] = arg
		else:
			element.parent.args.append(arg)

class ModHandler(Handler):
	
	TAG = "mod"
	
	def __init__(self):
		Handler.__init__(self, self.TAG, 
				"id module name author version build date url dll", 
				(LoadHandler.TAG))
		self.addAttribute("id")
		self.addAttribute("name")
		self.addAttribute("dll")
		self.addAttribute("author")
		self.addAttribute("version")
		self.addAttribute("build")
		self.addAttribute("date")
		self.addAttribute("url")
	
	def handle(self, element, id, name, dll, author, version, build, date, url):
		dll = BugDll.decode(dll)
		element.setState("mod", BugCore.game._getMod(id))
		element.setState("dll", BugDll.decode(dll))
	
	def complete(self, element):
		mod = element.getState("mod")
		mod._initDone()
		BugCore.game._addMod(mod)


## Standard Handlers

class InitHandler(HandlerWithArgs):
	
	TAG = "init"
	
	def __init__(self):
		HandlerWithArgs.__init__(self, self.TAG, "module function immediate dll")
		self.addAttribute("module", True, True)
		self.addAttribute("function", True, False, "init")
		self.addAttribute("immediate", False, False, "False")
		self.addAttribute("dll")
	
	def handle(self, element, module, function, immediate, dll):
		immediate = self.isTrue(immediate)
		dll = BugDll.decode(dll)
		if self.isDllOkay(element, dll):
			func = BugUtil.getFunction(module, function, True, *element.args, **element.kwargs)
			if immediate:
				func()
			else:
				BugInit.addInit(module, func)
		else:
			BugUtil.info("BugConfig - ignoring <%s> %s.%s, requires dll version %s", element.tag, module, function, self.resolveDll(element, dll))

class EventsHandler(HandlerWithArgs):
	
	TAG = "events"
	
	def __init__(self):
		HandlerWithArgs.__init__(self, self.TAG, "module function class dll")
		self.addAttribute("module", True, True)
		self.addExcludedAttribute("function", False, None, "module")
		self.addAttribute("class", True, False, None, "function")
		self.addAttribute("dll")
	
	def handle(self, element, module, clazz, dll):
		dll = BugDll.decode(dll)
		if self.isDllOkay(element, dll):
			BugUtil.callFunction(module, clazz, CvEventInterface.getEventManager(), *element.args, **element.kwargs)
		else:
			BugUtil.info("BugConfig - ignoring <%s> from %s.%s, requires dll version %s", element.tag, module, clazz, self.resolveDll(element, dll))

class EventHandler(HandlerWithArgs):
	
	TAG = "event"
	
	def __init__(self):
		HandlerWithArgs.__init__(self, self.TAG, "type module function dll")
		self.addAttribute("type", True)
		self.addAttribute("module", True, True)
		self.addAttribute("function", True)
		self.addAttribute("dll")
	
	def handle(self, element, type, module, function, dll):
		dll = BugDll.decode(dll)
		if self.isDllOkay(element, dll):
			CvEventInterface.getEventManager().addEventHandler(type, BugUtil.getFunction(module, function, True, *element.args, **element.kwargs))
		else:
			BugUtil.info("BugConfig - ignoring <%s> %s, requires dll version %s", element.tag, type, self.resolveDll(element, dll))

class ExportHandler(Handler):
	
	TAG = "export"
	
	def __init__(self):
		Handler.__init__(self, self.TAG, "module function to as dll")
		self.addAttribute("module", True, True)
		self.addAttribute("function", True)
		self.addAttribute("to", True)
		self.addAttribute("as", True, False, None, "function")
		self.addAttribute("dll")
	
	def handle(self, element, module, function, toModule, asName, dll):
		dll = BugDll.decode(dll)
		if self.isDllOkay(element, dll):
			BugUtil.exportFunction(module, function, toModule, asName)
		else:
			BugUtil.info("BugConfig - ignoring <%s> %s.%s, requires dll version %s", element.tag, module, function, self.resolveDll(element, dll))

class ExtendHandler(Handler):
	
	TAG = "extend"
	
	def __init__(self):
		Handler.__init__(self, self.TAG, "how module function to as dll")
		self.addAttribute("how", True, False, BugUtil.EXTEND_INSTEAD)
		self.addAttribute("module", True, True)
		self.addAttribute("function", True)
		self.addAttribute("to", True)
		self.addAttribute("as", True, False, None, "function")
		self.addAttribute("dll")
	
	def handle(self, element, how, module, function, toModule, asName, dll):
		dll = BugDll.decode(dll)
		if self.isDllOkay(element, dll):
			BugUtil.extendFunction(module, function, toModule, asName, how)
		else:
			BugUtil.info("BugConfig - ignoring <%s> %s.%s, requires dll version %s", element.tag, module, function, self.resolveDll(element, dll))


## Initialization

g_rootHandler = None
g_bugHandler = None

def init():
	global g_rootHandler, g_bugHandler
	g_rootHandler = RootHandler()
	g_bugHandler = BugHandler()
	
	registerHandler(RootHandler.TAG, g_rootHandler)
	registerHandler(BugHandler.TAG, g_bugHandler)
	registerHandler(LoadHandler.TAG, LoadHandler())
	registerHandler(ConfigHandler.TAG, ConfigHandler())
	registerHandler(ArgHandler.TAG, ArgHandler())
	
#	registerHandler(ModHandler.TAG, ModHandler())
	
#	parser = ConfigParser()
#	parser.parse(r"C:\Coding\Civ\BUG\BUG\CustomAssets\Config\NewConfig.xml")

init()
