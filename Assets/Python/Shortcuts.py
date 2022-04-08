import CvUtil

from CvPythonExtensions import *
from Locations import *
from RFCUtils import *
from Events import events, handler, popup_handler

from CvScreenEnums import *


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


@handler("kbdEvent")
def observerModeShortcut(eventType, key):
	if eventType == events.EventKeyDown and key == InputTypes.KB_A and events.bCtrl:
		popup = CyPopup(4568, EventContextTypes.EVENTCONTEXT_ALL, True)
		
		popup.setHeaderString(text("TXT_KEY_INTERFACE_OBSERVER_MODE_HEADER"), CvUtil.FONT_LEFT_JUSTIFY)
		popup.setBodyString(text("TXT_KEY_INTERFACE_OBSERVER_MODE_BODY"), CvUtil.FONT_LEFT_JUSTIFY)
		popup.createEditBox(str(game.getGameTurnYear()), 0)
		
		popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

@popup_handler(4568)
def handleStartObserverMode(iPlayer, netUserData, popupReturn):
	iDestinationYear = int(popupReturn.getEditBoxString(0))
	iAutoplayTurns = year(iDestinationYear) - turn()
	
	if iAutoplayTurns > 0:
		startObserverMode(iAutoplayTurns)


@handler("autoplayEnded")
def observerModeEnds():
	endObserverMode()


@handler("kbdEvent")
def civSwitchShortcut(eventType, key):
	if eventType == events.EventKeyDown and events.bCtrl and key == InputTypes.KB_C:
		popup = CyPopup(4569, EventContextTypes.EVENTCONTEXT_ALL, True)
		
		popup.setHeaderString(text("TXT_KEY_INTERFACE_CIV_SWITCH_HEADER"), CvUtil.FONT_LEFT_JUSTIFY)
		popup.setBodyString(text("TXT_KEY_INTERFACE_CIV_SWITCH_BODY"), CvUtil.FONT_LEFT_JUSTIFY)
		
		popup.createPullDown(0)
		
		for iPlayer in players.major().alive():
			popup.addPullDownString(name(iPlayer), iPlayer, 0)
		
		popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

@popup_handler(4569)
def handleCivSwitch(iPlayer, netUserData, popupReturn):
	iNewPlayer = popupReturn.getSelectedPullDownValue(0)
	
	if iNewPlayer != active():
		game.setActivePlayer(iNewPlayer, False)