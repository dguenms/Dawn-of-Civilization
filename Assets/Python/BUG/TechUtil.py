## TechUtil
##
## Utilities for dealing with Technologies.
##
## Notes
##   - Must be initialized externally by calling init()
##
## TODO
##   - Use PlayerUtil
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *

# BUG - Mac Support - start
import BugUtil
BugUtil.fixSets(globals())
# BUG - Mac Support - end

NUM_TECHS = -1
NUM_AND_PREREQS = -1
NUM_OR_PREREQS = -1

gc = CyGlobalContext()

def init():
	global NUM_TECHS, NUM_AND_PREREQS, NUM_OR_PREREQS
	NUM_TECHS = gc.getNumTechInfos()
	NUM_AND_PREREQS = gc.getNUM_AND_TECH_PREREQS()
	NUM_OR_PREREQS = gc.getNUM_OR_TECH_PREREQS()

def getPlayer(ePlayer):
	"Returns the CyPlayer for the given player ID."
	return gc.getPlayer(ePlayer)

def getTeam(ePlayer):
	"Returns the CyTeam for the given player ID."
	return gc.getTeam(getPlayer(ePlayer).getTeam())

def getPlayerAndTeam(ePlayer):
	"Returns the CyPlayer and CyTeam for the given player ID."
	player = getPlayer(ePlayer)
	return player, gc.getTeam(player.getTeam())

def getKnownTechs(ePlayer):
	"""
	Returns a set of tech IDs that ePlayer knows.
	"""
	knowingTeam = getTeam(ePlayer)
	techs = set()
	for eTech in range(NUM_TECHS):
		if knowingTeam.isHasTech(eTech):
			techs.add(eTech)
	return techs

def getVisibleKnownTechs(ePlayer, eAskingPlayer):
	"""
	Returns a set of tech IDs that eAskingPlayer knows that ePlayer knows.
	
	Any techs that eAskingPlayer doesn't know and cannot research yet are removed
	from the set of all techs that ePlayer knows.
	"""
	knowingTeam = getTeam(ePlayer)
	askingPlayer, askingTeam = getPlayerAndTeam(eAskingPlayer)
	techs = set()
	for eTech in range(NUM_TECHS):
		if knowingTeam.isHasTech(eTech):
			if askingTeam.isHasTech(eTech) or askingPlayer.canResearch(eTech, False):
				techs.add(eTech)
	return techs
