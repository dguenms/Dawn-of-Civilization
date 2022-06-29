from Core import *

from SettlerMaps import getMap as getSettlerMap
from WarMaps import getMap as getWarMap
from Logging import time


def findSlot(iCiv):
	iSlot = next(iSlot for iSlot in range(iNumPlayers) if civ(iSlot) == iCiv)
	if iSlot is not None:
		return iSlot
	
	iSlot = next(iSlot for iSlot in range(iNumPlayers) if civ(iSlot) == -1)
	if iSlot is not None:
		return iSlot
	
	iSlot = next(iSlot for iSlot in range(iNumPlayers) if not player(iSlot).isAlive() and not player(iSlot).isHuman() and not player(iSlot).isMinorCiv())
	if iSlot is not None:
		return iSlot

	return -1
	
def addPlayer(iPlayer, iCiv, iBirthTurn=-1, bAlive=False, bMinor=False):
	game.addPlayer(iPlayer, 0, iCiv, iBirthTurn, bAlive, bMinor)
	data.dSlots[iCiv] = iPlayer

def updateCivilization(iPlayer, iCiv, iBirthTurn=-1):
	data.dSlots[iCiv] = iPlayer
	
	iCurrentCivilization = player(iPlayer).getCivilizationType()
	if iCiv == iCurrentCivilization:
		return
	
	addPlayer(iPlayer, iCiv, iBirthTurn=iBirthTurn, bAlive=True)
	
	if iCurrentCivilization in data.dSlots:
		del data.dSlots[iCurrentCivilization]
	
	data.players[iPlayer].resetStability()

def getImpact(iCiv):
	iActiveCiv = civ()

	if iActiveCiv == iCiv:
		return iImpactPlayer
	
	if iCiv in dNeighbours[iActiveCiv]:
		return iImpactPlayer
	
	if iCiv in dInfluences[iActiveCiv]:
		return iImpactPlayer
	
	return infos.civ(iCiv).getImpact()

def getNextBirth():
	lUpcomingCivs = [iCiv for iCiv, iYear in dBirth.items() if turn() < year(iYear) - turns(5)]
	return find_min(lUpcomingCivs, dBirth.__getitem__).result

def getActiveSlots():
	return count(1 for iSlot in range(iNumPlayers) if player(iSlot).isAlive() or player(iSlot).isHuman())

def allSlotsTaken():
	return getActiveSlots() >= iNumPlayers-1