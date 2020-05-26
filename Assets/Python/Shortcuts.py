from CvPythonExtensions import *
from Events import events, handler


tThebes = (68, 33)


@handler("kbdEvent")
def checkUnitArt(eventType, key):
	key = int(key)

	if eventType == events.EventKeyDown and key == int(InputTypes.KB_V) and events.bCtrl and events.bShift:
		for iPlayer in players.all().barbarian():
			pPlayer = player(iPlayer)
			
			lEras = [iAncient, iMedieval, iIndustrial]
			for iEra in lEras:
				pPlayer.setCurrentEra(iEra)
				for iUnit in range(iNumUnits):
					unit = makeUnit(iPlayer, iUnit, tThebes)
					unit.kill(False, -1)