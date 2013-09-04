## AutoSave
##
## Collection of saved game related utility functions.
##
## saveGame(type, variant)
##   Saves the game in the directory for the given type and optional variant.
##
## getSaveDir(type, variant)
##   Returns the full path of the saved games directory for the given type and optional variant.
##
## getSaveFileName(pathName)
##   Returns the full path and name of the save file for the current game.
##   Used by MapFinder and the save events.
##
## The idea for this and much of the code come from HOF Mod.
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: Ruff_Hi, EmperorFool

from CvPythonExtensions import *
import os.path
import time
import CvUtil
import BugCore
import BugPath
import BugUtil
import MapFinder
import PlayerUtil


## Constants

# Save Types

SINGLE = "single"
MULTI = "multi"
PBEM = "pbem"
HOTSEAT = "hotseat"
PITBOSS = "pitboss"
WORLDBUILDER = "WorldBuilder"

# Save Variants

AUTO = "auto"
QUICK = "quick"


## Globals

gc = CyGlobalContext()
options = BugCore.game.AutoSave


## Save Game

def saveGame(type=SINGLE, variant=None):
	"""
	Saves the current game to the folder designated by the type and optional variant
	and returns the full path to it.
	
	All in the types except WORLDBUILDER allow the AUTO variant while only SINGLE allows QUICK.
	"""
	if _saveDir:
		if variant:
			BugUtil.debug("AutoSave - saving %s %s game", type, variant)
		else:
			BugUtil.debug("AutoSave - saving %s game", type)
		(fileName, _) = getSaveFileName(getSaveDir(type, variant))
		if fileName:
			fileName += ".CivBeyondSwordSave"
			gc.getGame().saveGame(fileName)
			return fileName
		else:
			BugUtil.error("Could not build saved game file name")
	return None

def getSaveDir(type=SINGLE, variant=None):
	if variant:
		return BugPath.join(_saveDir, type, variant)
	else:
		return BugPath.join(_saveDir, type)

def getSaveFileName(pathName):
	if pathName:
		activePlayer = PlayerUtil.getActivePlayer()
		if not MapFinder.isActive() and options.isUsePlayerName():
			fileName = activePlayer.getName()
			turnYear = CyGameTextMgr().getTimeStr(gc.getGame().getGameTurn(), False)
			fileName += '_' + turnYear.replace(" ", "-")
		else:
			objLeaderHead = gc.getLeaderHeadInfo (activePlayer.getLeaderType()).getText()
			
			game = gc.getGame()
			map = gc.getMap()
			
			difficulty = gc.getHandicapInfo(activePlayer.getHandicapType()).getText()
			mapType = os.path.basename(map.getMapScriptName())
			mapSize = gc.getWorldInfo(map.getWorldSize()).getText()
			mapClimate = gc.getClimateInfo(map.getClimate()).getText()
			mapLevel = gc.getSeaLevelInfo(map.getSeaLevel()).getText()
			era = gc.getEraInfo(game.getStartEra()).getText()
			speed = gc.getGameSpeedInfo(game.getGameSpeedType()).getText()
			turnYear = CyGameTextMgr().getTimeStr(game.getGameTurn(), False)
			turnYear = turnYear.replace(" ", "-")
			turnYear = turnYear.replace(",", "-")

			fileName = objLeaderHead[0:3]
			fileName += '_' + difficulty[0:3]
			fileName += '_' + mapSize[0:3]
			fileName += '_' + mapType[0:3]
			fileName += '_' + speed[0:3]
			fileName += '_' + era[0:3]
			fileName += '_' + turnYear
			fileName += '_' + mapClimate[0:3]
			fileName += '_' + mapLevel[0:3]

		fileName = BugPath.join(pathName, fileName)
		baseFileName = CvUtil.convertToStr(fileName)
		fileName = CvUtil.convertToStr(fileName + '_' + time.strftime("%b-%d-%Y_%H-%M-%S"))

		return (fileName, baseFileName)


## AutoSave Callbacks

def saveGameStart():
	"""
	Saves the single-player game when the map is generated as long as MapFinder isn't active.
	"""
	if not CyGame().isGameMultiPlayer() and options.isCreateStartSave() and not MapFinder.isActive():
		saveGame()

def saveGameEnd():
	"""
	Saves the single-player game when the game ends.
	"""
	if not CyGame().isGameMultiPlayer() and options.isCreateEndSave() and not MapFinder.isActive():
		saveGame()

def saveGameExit():
	"""
	Saves the single-player game when the player exits to the main menu or desktop.
	"""
	if not CyGame().isGameMultiPlayer() and options.isCreateExitSave() and not MapFinder.isActive():
		saveGame()


## Initialization

_saveDir = None
def init():
	global _saveDir
	_saveDir = BugPath.join(BugPath.getRootDir(), "Saves")
	if not _saveDir:
		BugUtil.error("Could not find Saves directory")
