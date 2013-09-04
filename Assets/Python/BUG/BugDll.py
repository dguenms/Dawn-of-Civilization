## BugDll
##
## Collection of utility functions for dealing with the optional BUG DLL.
##
## General
##
##   - isPresent()
##     Returns True if the BUG DLL is present.
##
##   - getVersion()
##     Returns the version number of the BUG DLL if it's present, zero (0) otherwise.
##
##   - isVersion(version)
##     Returns True if the BUG DLL is present and is version <version> or later.
##
## Widgets
##
##   - widget(bugWidget, bugData1=None, bugData2=None, *args)
##     Returns a tuple of arguments for passing to a function that takes a WidgetTypes and parameters.
##     Chooses between two sets of widgets and parameters based on the presence of the BUG DLL.
##
##   - widgetVersion(version, bugWidget, bugData1=None, bugData2=None, *args)
##     Same as widget() but also checks the BUG DLL version as per isVersion().
##
##   - isWidget(widget, bugWidget)
##     Returns True if <bugWidget> exists and matches <widget>
##
##   - isWidgetVersion(version, widget, bugWidget)
##     Same as isWidget() but also checks the BUG DLL version as per isVersion().
##
## Notes
##   - Must be initialized externally by calling init()
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugOptions
import BugUtil

gc = CyGlobalContext()

IS_PRESENT = False
VERSION = -1


## General and Versions

def isBug():
	return True

def isPresent():
	return IS_PRESENT

def getVersion():
	return VERSION

def isVersion(version):
	if version > 0:
		return IS_PRESENT and VERSION >= version
	else:
		return IS_PRESENT

def decode(value, noneIsZero=False):
	if value:
		if isinstance(value, int):
			if value >= 1:
				return value
		else:
			try:
				version = int(value)
				if version >= 1:
					return version
			except ValueError:
				pass
	if noneIsZero:
		return 0
	else:
		return None


## Widgets

def widget(bugWidget, bugData1=None, bugData2=None, *args):
	return widgetVersion(VERSION, bugWidget, bugData1, bugData2, *args)

def widgetVersion(version, bugWidget, bugData1=None, bugData2=None, *args):
	"""
	Picks one of two WidgetTypes and parameters to return based on presence of BUG DLL and <version>.
	
	The bugWidget must be the name of the desired widget, e.g. "WIDGET_SET_PERCENT";
	the other widget should be the WidgetTypes constant, e.g. WidgetTypes.WIDGET_CHANGE_PERCENT.
	
	The default widget values are WidgetTypes.WIDGET_GENERAL, -1, -1. To specify a different set,
	pass them in as the 4th, 5th and 6th arguments.
	
	To return zero or one data values, pass None for the BUG values you want not to have returned;
	the same ones won't be returned if the BUG DLL isn't present. When overriding the non-BUG widget
	type, you must always pass in three values: the WidgetTypes and its two data values. The matching
	BUG ones that are None will not be returned, regardless of their own values.
	
	Any arguments after the widget arguments are added at the end of the returned tuple; use this
	when the function you are passing the arguments to takes more arguments after the widget values.
	
	Make sure to use a * to unpack the returned tuple when passing the arguments to your function.
	
	Example:
		screen.setButtonGFC( "MinCommerceRate", u"", "", 130, 50, 20, 20, 
							 *BugDll.widget("WIDGET_SET_PERCENT", eCommerce, 0, 
							 				WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, -100, 
							 				ButtonStyles.BUTTON_STYLE_CITY_MINUS) )
	"""
	realArgs = []
	if len(args) >= 3 and isinstance(args[0], WidgetTypes):
		normalWidget, normalData1, normalData2 = args[:3]
		args = args[3:]
	else:
		normalWidget=WidgetTypes.WIDGET_GENERAL
		normalData1=-1
		normalData2=-1
	handled = False
	if isVersion(version):
		try:
			if isinstance(bugWidget, WidgetTypes):
				realArgs.append(bugWidget)
			else:
				realArgs.append(getattr(WidgetTypes, bugWidget))
			if bugData1 is not None:
				realArgs.append(bugData1)
			if bugData2 is not None:
				realArgs.append(bugData2)
			handled = True
		except AttributeError:
			BugUtil.warn("WidgetTypes.%s not found", bugWidget)
	if not handled:
		realArgs.append(normalWidget)
		if bugData1 is not None:
			realArgs.append(normalData1)
		if bugData2 is not None:
			realArgs.append(normalData2)
	if args:
		realArgs.extend(args)
	return realArgs


def isWidget(widget, bugWidget):
	return isWidgetVersion(VERSION, widget, bugWidget)

def isWidgetVersion(version, widget, bugWidget):
	"""
	Returns True if <widget> has the same value as <bugWidget>, False otherwise.
	
	If the BUG DLL isn't present, doesn't have the correct version, or the widget
	doesn't exist, False is safely returned.
	"""
	if isVersion(version):
		try:
			return widget == getattr(WidgetTypes, bugWidget)
		except:
			pass
	return False


## Accessing Options

def getOptionBOOL(argsList):
	return castOptionValue(bool, *argsList)

def getOptionINT(argsList):
	return castOptionValue(int, *argsList)

def getOptionFLOAT(argsList):
	return castOptionValue(float, *argsList)

def getOptionSTRING(argsList):
	return castOptionValue(str, *argsList)

def castOptionValue(func, id, default):
	try:
		return func(BugOptions.getOption(id).getValue())
	except:
		return default


def init():
	"""
	Checks for the presence of the BUG DLL and grabs its Python API version if found.
	"""
	try:
		if gc.isBull():
			global IS_PRESENT, VERSION
			IS_PRESENT = True
			VERSION = gc.getBullApiVersion()
			BugUtil.info("BugDll - %s %s, API version %d", gc.getBullName(), gc.getBullVersion(), VERSION)
			if hasattr(CyGlobalContext, "setIsBug"):
				import BugInit
				BugInit.addInit("setIsBug", setIsBug)
			else:
				BugUtil.debug("BugDll - setIsBug() not found")
	except:
		BugUtil.debug("BugDll - BULL not present")

def setIsBug():
	"""
	Tells BULL that BUG is ready to receive queries for options.
	"""
	BugUtil.debug("BugDll - calling setIsBug()")
	gc.setIsBug(True)
