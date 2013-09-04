## GameUtil
##
## Collection of utility functions for dealing with the game and its options.
##
## Versions
##
##   getVersion()
##     Returns the running BTS version as an integer (e.g. 317).
##
##   isVersion(version)
##     Returns True if the BTS version is <version> or greater.
##
##   isVersionExactly(version)
##     Returns True if the BTS version is exactly <version>.
##
##   isVersionBetween(min, max)
##     Returns True if the game version is at least <min> but less than <max>.
##
##
##   getSaveVersion()
##     Returns the saved game version as an integer (e.g. 301).
##
##   isSaveVersion(version)
##     Returns True if the saved game version is <version> or greater.
##
##   isSaveVersionExactly(version)
##     Returns True if the saved game version is exactly <version>.
##
##   isSaveVersionBetween(min, max)
##     Returns True if the saved game version is at least <min> but less than <max>.
##
## Game Values
##
##   getCultureThreshold(level)
##     Returns the culture required to achieve the <level> for the current game speed.
##
## Game Options
##
##   isEspionage()
##     Returns True if running at least 3.17 and the No Espionage option is set
##     for the game in progress.
##
##   isTechTrading()
##     Returns True if the No Tech Trading option is disabled.
##
##   isNoTechBrokering()
##     Returns True if the No Tech Brokering option is enabled.
##
##   isAlwaysWar()
##     Returns True if the Always War option is enabled.
##
##   isAlwaysPeace()
##     Returns True if the Always Peace option is enabled.
##
##   isPermanentWarPeace()
##     Returns True if the Permanent War/Peace option is enabled.
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *


## Globals

gc = CyGlobalContext()


## Versions

def getVersion():
	"""
	Returns the game version as an integer times 100 (e.g. 313).
	"""
	return gc.getDefineINT("CIV4_VERSION")

def isVersion(version):
	"""
	Returns True if the game version is at least <version>.
	"""
	return getVersion() >= version

def isVersionExactly(version):
	"""
	Returns True if the game version is exactly <version>.
	"""
	return getVersion() == version

def isVersionBetween(min, max):
	"""
	Returns True if the game version is at least <min> but less than <max>.
	"""
	return isVersion(min) and not isVersion(max)


def getSaveVersion():
	"""
	Returns the save version as an integer times 100 (e.g. 301).
	"""
	return gc.getDefineINT("SAVE_VERSION")

def isSaveVersion(version):
	"""
	Returns True if the save version is at least <version>.
	"""
	return getSaveVersion() >= version

def isSaveVersionExactly(version):
	"""
	Returns True if the save version is exactly <version>.
	"""
	return getSaveVersion() == version

def isSaveVersionBetween(min, max):
	"""
	Returns True if the save version is at least <min> but less than <max>.
	"""
	return isSaveVersion(min) and not isSaveVersion(max)


## Game Values

def getCultureThreshold(level):
	if isVersion(319):
		return gc.getGame().getCultureThreshold(level)
	else:
		return gc.getCultureLevelInfo(level).getSpeedThreshold(gc.getGame().getGameSpeedType())


## Game Options

def isEspionage():
	"""
	Returns True if using at least 3.17 and the 'No Espionage' option is not enabled.
	"""
	if isVersion(317):
		return not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ESPIONAGE)
	return True

def isTechTrading():
	"""
	Returns True if the No Tech Trading option is disabled.
	"""
	return not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_TECH_TRADING)

def isNoTechBrokering():
	"""
	Returns True if the No Tech Brokering option is enabled.
	"""
	return not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_TECH_BROKERING)

def isOCC():
	"""
	Returns True if the One City Challenge option is enabled.
	"""
	return gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE)

def isAlwaysWar():
	"""
	Returns True if the Always War option is enabled.
	"""
	return gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ALWAYS_WAR)

def isAlwaysPeace():
	"""
	Returns True if the Always Peace option is enabled.
	"""
	return gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ALWAYS_PEACE)

def isPermanentWarPeace():
	"""
	Returns True if the Permanent War/Peace option is enabled.
	"""
	return gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_CHANGING_WAR_PEACE)
