from Core import *
from RFCUtils import *


def findSlot(iCiv):
	iSlot = next(iSlot for iSlot in range(iNumPlayers) if civ(iSlot) == iCiv)
	if iSlot is not None:
		return iSlot
	
	iSlot = next(iSlot for iSlot in range(iNumPlayers) if civ(iSlot) == -1)
	if iSlot is not None:
		return iSlot
	
	iSlot = next(iSlot for iSlot in range(iNumPlayers) if availableSlot(iSlot))
	if iSlot is not None:
		return iSlot

	return -1

def findMinorSlot(iCiv):
	return next(iSlot for iSlot in reversed(range(iNumPlayers)) if civ(iSlot) == -1)
	
def availableSlot(iSlot):
	if civ(iSlot) == -1:
		return True
	
	if civ(iSlot) == iNative and since(year(1900)) > 0 and player(iSlot).getNumCities() == 0 and player(iSlot).getNumUnits() == 0:
		return True
	
	if player(iSlot).isAlive():
		return False
	
	if player(iSlot).isHuman():
		return False
	
	if player(iSlot).isMinorCiv():
		return False
	
	return True
	
def addPlayer(iPlayer, iCiv, iBirthTurn=-1, bAlive=False, bMinor=False):
	game.addPlayer(iPlayer, 0, iCiv, iBirthTurn, bAlive, bMinor)
	data.dSlots[iCiv] = iPlayer

def updateCivilization(iPlayer, iCiv, iBirthTurn=-1):
	data.dSlots[iCiv] = iPlayer
	data.players[iPlayer].resetStability()
	
	iCurrentCivilization = player(iPlayer).getCivilizationType()
	if iCiv == iCurrentCivilization:
		return
	
	resetRevealedOwner(iPlayer)
	
	addPlayer(iPlayer, iCiv, iBirthTurn=iBirthTurn, bAlive=True)
	
	initWars(iPlayer)
	
	if iCurrentCivilization in data.dSlots:
		del data.dSlots[iCurrentCivilization]

def initWars(iPlayer):
	iCiv = player(iPlayer).getCivilizationType()
	iTeam = player(iPlayer).getTeam()
	
	if iCiv == iNative:
		for iOtherPlayer in players.all().alive():
			if not player(iOtherPlayer).isBarbarian():
				team(gc.getBARBARIAN_TEAM()).declareWar(iTeam, False, WarPlanTypes.WARPLAN_LIMITED)
	
	else:
		team(gc.getBARBARIAN_TEAM()).declareWar(iTeam, False, WarPlanTypes.WARPLAN_LIMITED)
		
		if player(iNative).isExisting():
			team(player(iNative).getTeam()).declareWar(iTeam, False, WarPlanTypes.WARPLAN_LIMITED)

def getImpact(iCiv):
	iActiveCiv = civ()

	if iActiveCiv == iCiv:
		return iImpactPlayer
	
	if iCiv in dNeighbours[iActiveCiv]:
		return iImpactPlayer
	
	if iCiv in dInfluences[iActiveCiv]:
		return iImpactPlayer
	
	iImpact = infos.civ(iCiv).getImpact()
	
	if not canEverRespawn(iCiv):
		iImpact -= 1
	
	if isOutdated(iCiv):
		iImpact -= 1
	
	return max(iImpactMarginal, iImpact)
			
def isOutdated(iCiv):
	if year() < year(dFall[iCiv]):
		return False

	lResurrections = dResurrections[iCiv]
	if not lResurrections:
		return True
	
	iFirstResurrectionStart = lResurrections[0][0]
	iLastResurrectionEnd = lResurrections[-1][1]
		
	if iLastResurrectionEnd < 2025:
		return True
		
	if iFirstResurrectionStart > dFall[iCiv]:
		return True
	
	return False
	
def getBirthsForTurn(iTurn):
	births = [iCiv for iCiv, iYear in dBirth.items() if year(iYear) == iTurn]
	return civs.of(*births).sort(getImpact, reverse=True)

def getNextBirths():
	for iTurns in range(turns(5), turns(10)):
		births = getBirthsForTurn(turn() + iTurns)
		if births:
			return births
	
	return []

def countAvailableSlots():
	return count(1 for iSlot in range(iNumPlayers) if availableSlot(iSlot))

def countUnavailableSlots():
	return count(1 for iSlot in range(iNumPlayers) if not availableSlot(iSlot))


def quickSpawn(iCiv):
	iPlayer = findSlot(iCiv)
	updateCivilization(iPlayer, iCiv)
	capital = plots.capital(iCiv)
	player(iPlayer).found(*location(capital))
	city(capital).setPopulation(20)
	game.setActivePlayer(iPlayer, False)

def advanceEra(iCiv):
	player(iCiv).setCurrentEra(player(iCiv).getCurrentEra()+1)