## sdToolKit by Stone-D (Laga Mahesa)
## Copyright Laga Mahesa 2005
##
## laga@tbi.co.id
## lmahesa@(yahoo|hotmail|gmail).com
##
## Version 1.22
##
## Rewritten to use BugData by EmperorFool


from CvPythonExtensions import *
import BugUtil
import BugData

GLOBALS_KEY = 'Global'

gc = CyGlobalContext()


################# SD-UTILITY-PACK ###################
#-=-=-=-=-=-=-=-= BASIC-UTILITIES =-=-=-=-=-=-=-=-=-#

def sdEcho( echoString ):
	BugUtil.debug("SdToolKit: %s" %(echoString))
	return 0

def sdGetTimeInt( turn ):
	TurnTable = CyGameTextMgr().getTimeStr(turn, false).split(' ')
	TurnInt   = int(TurnTable[0])
	if (TurnTable[1] == 'BC'):
		TurnInt = 0 - TurnInt
	return TurnInt

def sdGameYearsInt():
	yearsBC = sdGetTimeInt(gc.getGame().getStartTurn())
	if (yearsBC < 0):
		yearsBC = yearsBC - (yearsBC * 2)
	else:
		yearsBC = 0
	yearsAD = 0
	for i in range(gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getNumTurnIncrements()):
		yearsAD += gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGameTurnInfo(i).iNumGameTurnsPerIncrement
	yearsAD = sdGetTimeInt(yearsAD)
	if (yearsAD < sdGetTimeInt(gc.getGame().getGameTurn())):
		yearsAD = sdGetTimeInt(gc.getGame().getGameTurn())
	yearsAL = yearsBC + yearsAD
#	sdEcho('yearsBC : %d, yearsAD : %d, All Years : %d' %(yearsBC, yearsAD, yearsAL))
	return yearsAL


#-=-=-=-=-=-=-=-= SD-DATA-STORAGE =-=-=-=-=-=-=-=-=-#
# Every variable is a string, except for the actual
# value you want to store, which can be anything.

#--------------- INTERNAL USE ONLY -----------------#

#   Initializes a central reservoir of custom variables for your mod's use. 'ModID' should be your mod's name.
def sdModInit( ModID ):
	return sdModLoad(ModID)

#   Loads previously initialized data from the central reservoir.
def sdModLoad( ModID ):
	return BugData.getTable(ModID).data

#   Saves a mod's entire variable data to the central reservoir.
def sdModSave( ModID, mTable ):
	table = BugData.getTable(ModID)
	table.setData(mTable)
	return 0


#----------------- MOD FUNCTIONS -------------------#

#   sdEntityInit( 'MyModName', 'UniqueName', Template_dictionary )
#   Initializes a unique data entity (city, unit, plot).
def sdEntityInit( ModID, entity, eTable ):
	table = BugData.getTable(ModID, entity)
	table.setData(eTable)
	return 0

#   sdEntityWipe( 'MyModName', 'UniqueName' )
#   Removes an entity that has been previously initialized by sdEntityInit.
#   Returns int 0 on failure, int 1 on success.
def sdEntityWipe( ModID, entity ):
	return BugData.deleteTable(ModID)

#   sdEntityExists( 'MyModName', 'UniqueName' )
#   Checks whether or not an entity has been initialized by sdEntityInit.
#   Returns bool False on failure, bool True on success.
def sdEntityExists( ModID, entity ):
	return BugData.hasTable(ModID, entity)

#   sdGetVal( 'MyModName', 'UniqueName', 'VariableName' )
#   Fetches a specific variable's value from the entity's data set.
def sdGetVal( ModID, entity, var ):
	return BugData.getTable(ModID, entity)[var]

#   sdSetVal( 'MyModName', 'UniqueName', 'VariableName', any_value )
#   Stores a specific variable's value within the entity's data set.
#   Returns bool False on failure, bool True on success.
def sdSetVal( ModID, entity, var, val ):
	table = BugData.findTable(ModID, entity)
	if table:
		table[var] = val
		return True
	return False

#   sdDelVal( 'MyModName', 'UniqueName', 'VariableName' )
#   Removes a specific variable from the entity's data set.
#   Returns bool False on failure, bool True on success.
def sdDelVal( ModID, entity, var ):
	table = BugData.findTable(ModID, entity)
	if table and var in table:
		del table[var]
		return True
	return False

#   sdGetGlobal( 'MyModName', 'GlobalVariableName' )
#   Fetches a specific variable's value from the mod's global data set.
def sdGetGlobal( ModID, var ):
	table = BugData.findTable(ModID, GLOBALS_KEY)
	if table and var in table:
		return table[var]
	return None

#   sdSetGlobal( 'MyModName', 'GlobalVariableName', any_value )
#   Stores a specific variable's value within the mod's global data set.
def sdSetGlobal( ModID, var, val ):
	BugData.getTable(ModID, GLOBALS_KEY)[var] = val

#   sdDelGlobal( 'MyModName', 'GlobalVariableName' )
#   Removes a specific variable from the mod's global data set.
#   Returns bool False on failure, bool True on success.
def sdDelGlobal( ModID, var ):
	table = BugData.findTable(ModID, GLOBALS_KEY)
	if table and var in table:
		del table[var]
		return True
	return False
