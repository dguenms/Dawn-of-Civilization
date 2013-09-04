## SpyUtil
##
## Tracks each player's espionage point values per player to provide access to spending levels.
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: EmperorFool, ruff_hi

from CvPythonExtensions import *
import BugUtil
import PlayerUtil
import BugData

gc = CyGlobalContext()


## Tracking Values for Previous and Current Turns

g_iTurn = None
g_values = None

# gets the total spending over the prior turn by playerOrID
# limits the spending to players known to 'ActiveplayerOrID' if provided
def getSpending(playerOrID, ActiveplayerOrID=None):
	if ActiveplayerOrID != None:
		pActiveTeam = PlayerUtil.getPlayerTeam(ActiveplayerOrID)

	iTotal = 0
	for targetTeam in PlayerUtil.teams(True, None, False):
		if (ActiveplayerOrID == None
		or pActiveTeam.isHasMet(targetTeam.getID())):
			iTotal += getDifferenceByTeam(PlayerUtil.getPlayerTeam(playerOrID), targetTeam.getID())
	return iTotal

def getDifferenceByPlayer(playerOrID, targetPlayerOrID=None):
	if targetPlayerOrID is None:
		return getDifferenceByTeam(PlayerUtil.getPlayerTeam(playerOrID))
	else:
		return getDifferenceByTeam(PlayerUtil.getPlayerTeam(playerOrID), PlayerUtil.getPlayerTeamID(targetPlayerOrID))

def getDifferenceByTeam(teamOrID, targetTeamOrID=None):
	eTeam, team = PlayerUtil.getTeamAndID(teamOrID)
	if targetTeamOrID is None:
		eTargetTeam = PlayerUtil.getActiveTeamID()
	else:
		eTargetTeam = PlayerUtil.getTeamID(targetTeamOrID)
	iPrevious = getPreviousValueByTeam(eTeam, eTargetTeam)
	if iPrevious is not None:
		return team.getEspionagePointsAgainstTeam(eTargetTeam) - iPrevious
	else:
		return 0

def getPreviousValueByTeam(teamOrID, targetTeamOrID=None):
	global g_values, g_iTurn
	if g_iTurn is None:
		load()
	if g_iTurn == gc.getGame().getGameTurn() - 1 and g_values:
		eTeam = PlayerUtil.getTeamID(teamOrID)
		if targetTeamOrID is None:
			eTargetTeam = PlayerUtil.getActiveTeamID()
		else:
			eTargetTeam = PlayerUtil.getTeamID(targetTeamOrID)
		if eTeam in g_values:
			return g_values[eTeam][eTargetTeam]
	return None

def getCurrentValuesByTeam():
	valuesByTeam = {}
	for team in PlayerUtil.teams(True, None, False):
		valuesByTeam[team.getID()] = values = []
		for targetTeam in PlayerUtil.teams():
			values.append(team.getEspionagePointsAgainstTeam(targetTeam.getID()))
	return valuesByTeam


## Storing Values for Previous Turn

STORAGE_VERSION = 1

SD_MOD_ID = "SpyUtil"
SD_VERSION_ID = "version"
SD_TURN_ID = "turn"
SD_VALUES_ID = "values"

def clear():
	global g_values, g_iTurn
	g_iTurn = gc.getGame().getGameTurn() - 1
	g_values = None

def load():
	global g_values, g_iTurn
	clear()
	data = BugData.getTable(SD_MOD_ID).data
	BugUtil.debug("SpyUtil - loaded: %s", data)
	if SD_VERSION_ID in data:
		if data[SD_VERSION_ID] == 1:
			g_iTurn = data[SD_TURN_ID]
			if g_iTurn != gc.getGame().getGameTurn() - 1:
				BugUtil.warn("SpyUtil - incorrect previous game turn found, ignoring")
			else:
				g_values = data[SD_VALUES_ID]
		elif data[SD_VERSION_ID] > 1:
			BugUtil.warn("SpyUtil - newer format version detected, ignoring")
	else:
		BugUtil.debug("SpyUtil - no data found")

def store():
	global g_values, g_iTurn
	g_iTurn = gc.getGame().getGameTurn()
	g_values = getCurrentValuesByTeam()
	data = {
		SD_VERSION_ID: STORAGE_VERSION,
		SD_TURN_ID: g_iTurn,
		SD_VALUES_ID: g_values
	}
	BugData.getTable(SD_MOD_ID).setData(data)
	BugUtil.debug("SpyUtil - stored: %s", data)


## Event Handlers

def onGameStart(argsList):
	clear()

def onGameLoad(argsList):
	load()

def onPythonReloaded(argsList):
	load()

def onBeginPlayerTurn(argsList):
	iGameTurn, iPlayer = argsList
	if iPlayer != PlayerUtil.getActivePlayerID():
		return
	store()
