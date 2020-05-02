# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
#
# CvEventInterface.py
#
# These functions are App Entry Points from C++
# WARNING: These function names should not be changed
# WARNING: These functions can not be placed into a class
#
# No other modules should import this
#
import CvUtil
import BugEventManager
from CvPythonExtensions import *

bugEventManager = BugEventManager.BugEventManager()

import Handlers

def getEventManager():
	return bugEventManager

def onEvent(argsList):
	'Called when a game event happens - return 1 if the event was consumed'
	return getEventManager().handleEvent(argsList)

def applyEvent(argsList):
	context, playerID, netUserData, popupReturn = argsList
	return getEventManager().applyEvent(argsList)

def beginEvent(context, argsList=-1):
	return getEventManager().beginEvent(context, argsList)

def initAfterReload():
	"""
	Initialize BUG and fires PythonReloaded event after reloading Python modules while game is still running.
	
	The first time this module is loaded after the game launches, the global context is not yet ready,
	and thus BUG cannot be initialized. When the Python modules are reloaded after being changed, however,
	this will reinitialize BUG and the main interface.
	"""
	import BugInit
	import BugPath
	if not BugPath.isMac() and BugInit.init():
		try:
			import CvScreensInterface
			CvScreensInterface.reinitMainInterface()
		except:
			import BugUtil
			BugUtil.error("BugInit - failure rebuilding main interface after reloading Python modules")
		getEventManager().fireEvent("PythonReloaded")

initAfterReload()
