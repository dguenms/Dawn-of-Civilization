from Core import *

from DynamicCivs import startingLeader

import Logging as log


def addPlayer(iCiv, bAlive=False, bMinor=False):
	iPlayer = findSlot(iCiv)
	iLeader = startingLeader(iCiv)
	game.addPlayer(iPlayer, iLeader, iCiv, bAlive, bMinor)
	
	data.dSlots[iCiv] = iPlayer
	
	return iPlayer

def findSlot(iCiv):
	iSlot = next(iSlot for iSlot in range(iNumPlayers) if civ(iSlot) == iCiv)
	if iSlot is not None:
		log.rise("FIND SLOT: Used slot %d already used by %s\n\n", iSlot, infos.civ(iCiv).getText())
		return iSlot
	
	iSlot = next(iSlot for iSlot in range(iNumPlayers) if civ(iSlot) == -1)
	if iSlot is not None:
		log.rise("FIND SLOT: Used free slot %d for %s\n\n", iSlot, infos.civ(iCiv).getText())
		return iSlot
	
	iSlot = next(iSlot for iSlot in range(iNumPlayers) if not player(iSlot).isAlive() and not player(iSlot).isHuman() and not player(iSlot).isMinorCiv())
	if iSlot is not None:
		log.rise("FIND SLOT: Used slot %d previously of %s for %s\n\n", iSlot, infos.civ(player(iSlot)).getText(), infos.civ(iCiv).getText())
		return iSlot

	log.rise("FIND SLOT: Could not find slot for %s\n\n", infos.civ(iCiv).getText())
	return -1

def updateCivilization(iPlayer, iCiv):
	data.dSlots[iCiv] = iPlayer
	
	iCurrentCivilization = player(iPlayer).getCivilizationType()
	if iCiv == iCurrentCivilization:
		return
	
	if iCurrentCivilization == -1:
		addPlayer(iCiv, bAlive=True)
	else:
		player(iPlayer).setCivilizationType(iCiv)
	
	if iCurrentCivilization in data.dSlots:
		del data.dSlots[iCurrentCivilization]