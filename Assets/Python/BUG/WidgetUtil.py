## WidgetUtil
##
## Provides functions to create new WidgetTypes and supply hover text for them.
##
## WidgetTypes
##
##   createWidget(name)
##     Creates and returns a new unique WidgetTypes constant named <name>.
##
##       <widget name="<name>"/>
##
## Hover Help Text
##
##   setWidgetHelpText(widget, text)
##     Uses static <text> string for the hover help text of <widget>.
##
##       <widget name="<widget-name>" text="<text>"/>
##
##   setWidgetHelpXml(widget, key)
##     Uses <TEXT> CIV4GameText.xml element matching <key> for the hover text of <widget>.
##     This form allows you to use translated strings as it's looked up each time it's shown.
##
##       <widget name="<widget-name>" xml="<key>"/>
##
##   setWidgetHelpFunction(widget, func)
##     Calls <func> to get the hover text of <widget> each time it's shown.
##     Use this method when you want the displayed text to change based on game conditions.
##     The function should have this signature:
##       func(eWidget, iData1, iData2, bOption)
##
##       <widget name="<widget-name>" module="<module-name>" function="<function-name>"/>
##
## Notes
##
##   Must register setWidgetHelp() as a BugGameUtils handler.
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugConfig
import BugUtil


## Widget Types

g_nextWidget = WidgetTypes.NUM_WIDGET_TYPES

def createWidget(name):
	"""
	Creates and returns the next unique WidgetTypes constant to be used with custom UI widgets.
	
	If <name> already exists, a warning is logged and the widget is returned.
	Otherwise the new widget is assigned to WidgetTypes.<name> and returned.
	"""
	if hasattr(WidgetTypes, name):
		BugUtil.warn("WidgetTypes.%s already exists", name)
		return getattr(WidgetTypes, name)
	else:
		global g_nextWidget
		BugUtil.info("WidgetUtil - WidgetTypes.%s = %d", name, g_nextWidget)
		widget = WidgetTypes(g_nextWidget)
		setattr(WidgetTypes, name, widget)
		g_nextWidget += 1
		return widget


## Hover Help Text

g_widgetHelp = {}

def setWidgetHelpText(widget, text):
	"""
	Assigns the literal <text> to be used as the hover text for <widget>.
	"""
	_setWidgetHelp(widget, "Text", lambda *ignored: text)

def setWidgetHelpXml(widget, key):
	"""
	Assigns the XML <key> to be used to lookup the translated hover text for <widget>.
	"""
	_setWidgetHelp(widget, "XML", lambda *ignored: BugUtil.getPlainText(key))

def setWidgetHelpFunction(widget, func):
	"""
	Assigns the function <func> to be called to get the hover text for <widget>.
	
	The function will be called each time the hover text is needed with these parameters:
	
		eWidgetType         WidgetTypes constant
		data1               int
		data2               int
		bOption             boolean
	
	The first three are the ones used when creating the UI widget.
	I have no idea what <bOption> is or where it comes from as it's supplied by the EXE.
	"""
	_setWidgetHelp(widget, "Function", func)

def _setWidgetHelp(widget, type, func):
	"""
	Registers the hover text <func> for <widget> if it hasn't been already.
	
	Do not call this function as it is used internally by the registration functions above.
	"""
	if widget in g_widgetHelp:
		BugUtil.warn("WidgetTypes %d help already registered", widget)
	else:
		BugUtil.debug("WidgetUtil - registering %s hover help for WidgetTypes %d: %s", type, widget, func)
		g_widgetHelp[widget] = func

	
def getWidgetHelp(argsList):
	"""
	Returns the hover help text for <eWidgetType> if registered, otherwise returns an empty string.
	
	This function is a BugGameUtils handler registered in init.xml.
	"""
	eWidgetType, iData1, iData2, bOption = argsList
	func = g_widgetHelp.get(eWidgetType)
	if func:
		return func(eWidgetType, iData1, iData2, bOption)
	return u""


## Configuration Handler

class WidgetHandler(BugConfig.Handler):
	
	TAG = "widget"
	
	def __init__(self):
		BugConfig.Handler.__init__(self, WidgetHandler.TAG, "name text xml module function")
		self.addAttribute("name", True)
		self.addAttribute("text")
		self.addAttribute("xml")
		self.addAttribute("module", False, True)
		self.addAttribute("function")
	
	def handle(self, element, name, text, xml, module, function):
		widget = createWidget(name)
		if text:
			setWidgetHelpText(widget, text)
		elif xml:
			setWidgetHelpXml(widget, xml)
		elif module and function:
			setWidgetHelpFunction(widget, BugUtil.lookupFunction(module, function))
