## GSpyUtil
##
## Utilities for dealing with Great Spies.
##
## Notes
##   - Must be initialized externally by calling init()
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugUtil
import FontUtil

gc = CyGlobalContext()

g_cGreatSpy = ""

def init():
	global g_cGreatSpy
	g_cGreatSpy = FontUtil.getChar(FontSymbols.COMMERCE_ESPIONAGE_CHAR)

def getGreatSpyText(iNeededExp):
	return BugUtil.getText("INTERFACE_NEXT_GREAT_GENERAL_XP", (g_cGreatSpy, iNeededExp))
