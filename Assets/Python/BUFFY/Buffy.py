## Buffy
##
## Collection of utility functions for dealing with BUFFY.
##
## Notes
##   - Must be initialized externally by calling init()
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: Ruff_Hi, EmperorFool

from CvPythonExtensions import *
import BugCore
import BugPath
import BugUtil
import CvUtil
import GameUtil
import os.path

gc = CyGlobalContext()
options = BugCore.game.BUFFY

IS_ACTIVE = False
IS_DLL_PRESENT = False
IS_DLL_IN_CORRECT_PATH = False


## Checking Status

def isEnabled():
	return options.isEnabled()

def isActive():
	"""
	Returns True if BUFFY is active in this session.
	
	Must be a BUFFY-enabled build with the DLL present and not running on a Mac.
	"""
	return IS_ACTIVE

def isDllPresent():
	"""
	Returns True if this is a BUFFY-enabled build and the BUFFY DLL is present, False otherwise.
	
	Note: If this isn't a BUFFY-enabled build, this function returns False even if the BUFFY DLL is present
	since init() doesn't look for the DLL.
	"""
	return IS_DLL_PRESENT

def isDllInCorrectPath():
	"""
	Returns True if the BUFFY DLL is present and in the correct location (...\<BTS>\Mods\<BUFFY>\Assets\).
	"""
	return IS_DLL_IN_CORRECT_PATH


## Initialization

def init():
	"""
	Checks for the presence of the BUFFY DLL and sets the global flags.
	"""
	if isEnabled():
		if BugPath.isMac():
			BugUtil.debug("BUFFY is not active on Mac (no DLL)")
		else:
			try:
				if gc.isBuffy():
					global IS_DLL_PRESENT, IS_DLL_IN_CORRECT_PATH, IS_ACTIVE
					IS_DLL_PRESENT = True
					IS_ACTIVE = True
					BugUtil.info("BUFFY is active (API version %d)", gc.getBuffyApiVersion())
					try:
						dllPath = gc.getGame().getDLLPath()
						exePath = gc.getGame().getExePath()
						dllPathThenUp3 = os.path.dirname(os.path.dirname(os.path.dirname(dllPath)))
						if dllPathThenUp3 == exePath:
							IS_DLL_IN_CORRECT_PATH = True
					except:
						pass # DLL path is borked
			except:
				BugUtil.info("BUFFY is not active (no DLL)")


## Random Event Changes

def canTriggerTheVedicAryans(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
#   If Barbarians are disabled in this game, this event will not occur.
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
		return false
			
#   At least one civ on the board must know Polytheism.
	bFoundValid = false

# BUFFY 3.19.003 - start
	# changes one of the key techs to Priesthood instead of Polytheism
	if isEnabled():
		iTech = gc.getInfoTypeForString('TECH_PRIESTHOOD')
	else:
		iTech = gc.getInfoTypeForString('TECH_POLYTHEISM')
# BUFFY 3.19.003 - end

	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive():
			if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
				bFoundValid = true
				break
				
	if not bFoundValid:
		return false
					
#   At least one civ on the board must know Archery.
	bFoundValid = false
	iTech = gc.getInfoTypeForString('TECH_ARCHERY')
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):			
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive():
			if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
				bFoundValid = true
				break
				
	if not bFoundValid:
		return false

# BUG - 3.17 - Start
	if (GameUtil.isVersion(317)):
		# rest indented but unchanged
		# Can we build the counter unit?		
		iCounterUnitClass = gc.getInfoTypeForString('UNITCLASS_ARCHER')
		iCounterUnit = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iCounterUnitClass)
		if iCounterUnit == -1:
			return false

		(loopCity, iter) = player.firstCity(false)
		bFound = false
		while(loopCity):
			if (loopCity.canTrain(iCounterUnit, false, false)):
				bFound = true
				break

			(loopCity, iter) = player.nextCity(iter, false)

		if not bFound:
			return false
# BUG - 3.17 - End

#	Find an eligible plot
	map = gc.getMap()	
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true)):
			return true

	return false
