from Events import events, handler
from CvPythonExtensions import *

import CvScreensInterface
import CvWBPopups
import Popup as PyPopup
import CvWorldBuilderScreen
import CvTechChooser
import CvUtil
import CvEspionageAdvisor
import CvDebugTools
import CvCameraControls

## Ultrapack ##
import WBCityEditScreen
import WBUnitScreen
import WBPlayerScreen
import WBGameDataScreen
import WBPlotScreen
import CvPlatyBuilderScreen
import WBStoredDataScreen
## Ultrapack ##


gc = CyGlobalContext()


@handler("kbdEvent")
def onKbdEvent(eventType, key, mx, my, px, py):
	game = gc.getGame()
	
	if (events.bAllowCheats):
		# notify debug tools of input to allow it to override the control
		argsList = (eventType,key,events.bCtrl,events.bShift,events.bAlt,mx,my,px,py,gc.getGame().isNetworkMultiPlayer())
		if ( CvDebugTools.g_CvDebugTools.notifyInput(argsList) ):
			return 0
	
	if ( eventType == events.EventKeyDown ):
		theKey=int(key)
		
		CvCameraControls.g_CameraControls.handleInput( theKey )
					
		if (events.bAllowCheats):
			# Shift - T (Debug - No MP)
			if (theKey == int(InputTypes.KB_T)):
				if ( events.bShift ):
					events.beginEvent(CvUtil.EventAwardTechsAndGold)
					#events.beginEvent(CvUtil.EventCameraControlPopup)
					return 1
						
			elif (theKey == int(InputTypes.KB_W)):
				if ( events.bShift and events.bCtrl):
					events.beginEvent(CvUtil.EventShowWonder)
					return 1
						
			# Shift - ] (Debug - currently mouse-overd unit, health += 10
			elif (theKey == int(InputTypes.KB_LBRACKET) and events.bShift ):
				unit = CyMap().plot(px, py).getUnit(0)
				if ( not unit.isNone() ):
					d = min( unit.maxHitPoints()-1, unit.getDamage() + 10 )
					unit.setDamage( d, PlayerTypes.NO_PLAYER )
				
			# Shift - [ (Debug - currently mouse-overd unit, health -= 10
			elif (theKey == int(InputTypes.KB_RBRACKET) and events.bShift ):
				unit = CyMap().plot(px, py).getUnit(0)
				if ( not unit.isNone() ):
					d = max( 0, unit.getDamage() - 10 )
					unit.setDamage( d, PlayerTypes.NO_PLAYER )
				
			elif (theKey == int(InputTypes.KB_F1)):
				if ( events.bShift ):
					CvScreensInterface.replayScreen.showScreen(False)
					return 1
				# don't return 1 unless you want the input consumed
			
			elif (theKey == int(InputTypes.KB_F2)):
				if ( events.bShift ):
					import CvDebugInfoScreen
					CvScreensInterface.showDebugInfoScreen()
					return 1
			
			elif (theKey == int(InputTypes.KB_F3)):
				if ( events.bShift ):
					CvScreensInterface.showDanQuayleScreen(())
					return 1
					
			elif (theKey == int(InputTypes.KB_F4)):
				if ( events.bShift ):
					CvScreensInterface.showUnVictoryScreen(())
					return 1


@handler("mouseEvent")
def onMouseEvent(eventType, mx, my, px, py, interfaceConsumed, screens):
	if ( px!=-1 and py!=-1 ):
		if ( eventType == events.EventLButtonDown ):
			if (events.bAllowCheats and events.bCtrl and events.bAlt and CyMap().plot(px,py).isCity() and not interfaceConsumed):
				# Launch Edit City Event
				events.beginEvent( CvUtil.EventEditCity, (px,py) )
				return 1
			
			elif (events.bAllowCheats and events.bCtrl and events.bShift and not interfaceConsumed):
				# Launch Place Object Event
				events.beginEvent( CvUtil.EventPlaceObject, (px, py) )
				return 1
		
	if ( eventType == events.EventBack ):
		return CvScreensInterface.handleBack(screens)
	elif ( eventType == events.EventForward ):
		return CvScreensInterface.handleForward(screens)


@handler("ModNetMessage")
def onModNetMessage(iData1, iData2, iData3, iData4, iData5):
	if iData1 == lNetworkEvents["CHANGE_COMMERCE_PERCENT"]:
		CommerceType = [CommerceTypes.COMMERCE_GOLD, CommerceTypes.COMMERCE_RESEARCH, CommerceTypes.COMMERCE_CULTURE, CommerceTypes.COMMERCE_ESPIONAGE]
		gc.getPlayer(iData2).changeCommercePercent(CommerceType[iData3], iData4)
		if iData2 == CyGame().getActivePlayer():
			screen = CvEspionageAdvisor.CvEspionageAdvisor().getScreen()
			if screen.isActive():
				CvEspionageAdvisor.CvEspionageAdvisor().updateEspionageWeights()
		

#################### TRIGGERED EVENTS ##################
				
def __eventEditCityNameBegin(city, bRename):
	popup = PyPopup.PyPopup(CvUtil.EventEditCityName, EventContextTypes.EVENTCONTEXT_ALL)
	popup.setUserData((city.getID(), bRename))
	popup.setHeaderString(localText.getText("TXT_KEY_NAME_CITY", ()))
	popup.setBodyString(localText.getText("TXT_KEY_SETTLE_NEW_CITY_NAME", ()))
	popup.createEditBox(city.getName())
	popup.setEditBoxMaxCharCount( 15 )
	popup.launch()

def __eventEditCityNameApply(playerID, userData, popupReturn):	
	'Edit City Name Event'
	iCityID = userData[0]
	bRename = userData[1]
	player = gc.getPlayer(playerID)
	city = player.getCity(iCityID)
	cityName = popupReturn.getEditBoxString(0)
	if (len(cityName) > 30):
		cityName = cityName[:30]
	city.setName(cityName, not bRename)

def __eventEditCityBegin(argsList):
	'Edit City Event'
	px,py = argsList
	CvWBPopups.CvWBPopups().initEditCity(argsList)

def __eventEditCityApply(playerID, userData, popupReturn):
	'Edit City Event Apply'
	if (getChtLvl() > 0):
		CvWBPopups.CvWBPopups().applyEditCity( (popupReturn, userData) )

def __eventPlaceObjectBegin(argsList):
	'Place Object Event'
	CvDebugTools.CvDebugTools().initUnitPicker(argsList)

def __eventPlaceObjectApply(playerID, userData, popupReturn):
	'Place Object Event Apply'
	if (getChtLvl() > 0):
		CvDebugTools.CvDebugTools().applyUnitPicker( (popupReturn, userData) )

def __eventAwardTechsAndGoldBegin(argsList):
	'Award Techs & Gold Event'
	CvDebugTools.CvDebugTools().cheatTechs()

def __eventAwardTechsAndGoldApply(playerID, netUserData, popupReturn):
	'Award Techs & Gold Event Apply'
	if (getChtLvl() > 0):
		CvDebugTools.CvDebugTools().applyTechCheat( (popupReturn) )

def __eventShowWonderBegin(argsList):
	'Show Wonder Event'
	CvDebugTools.CvDebugTools().wonderMovie()

def __eventShowWonderApply(playerID, netUserData, popupReturn):
	'Wonder Movie Apply'
	if (getChtLvl() > 0):
		CvDebugTools.CvDebugTools().applyWonderMovie( (popupReturn) )

## Platy Builder ##

def __eventEditUnitNameBegin(argsList):
	pUnit = argsList
	popup = PyPopup.PyPopup(CvUtil.EventEditUnitName, EventContextTypes.EVENTCONTEXT_ALL)
	popup.setUserData((pUnit.getID(), CyGame().getActivePlayer()))
	popup.setBodyString(localText.getText("TXT_KEY_RENAME_UNIT", ()))
	popup.createEditBox(pUnit.getNameNoDesc())
	popup.setEditBoxMaxCharCount(25)
	popup.launch()

def __eventEditUnitNameApply(playerID, userData, popupReturn):
	unit = gc.getPlayer(userData[1]).getUnit(userData[0])
	newName = popupReturn.getEditBoxString(0)		
	unit.setName(newName)
	if CyGame().GetWorldBuilderMode():
		WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeStats()
		WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeCurrentUnit()	
			
def __eventEditCityNameBegin(city, bRename):
	popup = PyPopup.PyPopup(CvUtil.EventEditCityName, EventContextTypes.EVENTCONTEXT_ALL)
	popup.setUserData((city.getID(), bRename, CyGame().getActivePlayer()))
	popup.setHeaderString(localText.getText("TXT_KEY_NAME_CITY", ()))
	popup.setBodyString(localText.getText("TXT_KEY_SETTLE_NEW_CITY_NAME", ()))
	popup.createEditBox(city.getName())
	popup.setEditBoxMaxCharCount(15)
	popup.launch()

def __eventEditCityNameApply(playerID, userData, popupReturn):
	city = gc.getPlayer(userData[2]).getCity(userData[0])
	cityName = popupReturn.getEditBoxString(0)
	city.setName(cityName, not userData[1])
	if CyGame().GetWorldBuilderMode() and not CyGame().isInAdvancedStart():
		WBCityEditScreen.WBCityEditScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeStats()

def __eventWBPlayerScriptPopupApply(playerID, userData, popupReturn):
	sScript = popupReturn.getEditBoxString(0)
	gc.getPlayer(userData[0]).setScriptData(CvUtil.convertToStr(sScript))
	WBPlayerScreen.WBPlayerScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
	return

def __eventWBCityScriptPopupApply(playerID, userData, popupReturn):
	sScript = popupReturn.getEditBoxString(0)
	pCity = gc.getPlayer(userData[0]).getCity(userData[1])
	pCity.setScriptData(CvUtil.convertToStr(sScript))
	WBCityEditScreen.WBCityEditScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
	return

def __eventWBUnitScriptPopupApply(playerID, userData, popupReturn):
	sScript = popupReturn.getEditBoxString(0)
	pUnit = gc.getPlayer(userData[0]).getUnit(userData[1])
	pUnit.setScriptData(CvUtil.convertToStr(sScript))
	WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
	return

def __eventWBScriptPopupBegin():
	return

def __eventWBGameScriptPopupApply(playerID, userData, popupReturn):
	sScript = popupReturn.getEditBoxString(0)
	CyGame().setScriptData(CvUtil.convertToStr(sScript))
	WBGameDataScreen.WBGameDataScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
	return

def __eventWBPlotScriptPopupApply(playerID, userData, popupReturn):
	sScript = popupReturn.getEditBoxString(0)
	pPlot = CyMap().plot(userData[0], userData[1])
	pPlot.setScriptData(CvUtil.convertToStr(sScript))
	WBPlotScreen.WBPlotScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
	return

def __eventWBStoredDataValuePopupApply(playerID, userData, popupReturn):
	sScript = popupReturn.getEditBoxString(0)
	try:
		int(sScript)
		bInt = True
	except ValueError:
		bInt = False
	if bInt:
		iValue = int(sScript)
		WBStoredDataScreen.WBStoredDataScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).changeListTableValue(userData[0], iValue)
	return

def __eventWBLandmarkPopupApply(playerID, userData, popupReturn):
	sScript = popupReturn.getEditBoxString(0)
	pPlot = CyMap().plot(userData[0], userData[1])
	iPlayer = userData[2]
	if userData[3] > -1:
		pSign = CyEngine().getSignByIndex(userData[3])
		iPlayer = pSign.getPlayerType()
		CyEngine().removeSign(pPlot, iPlayer)
	if len(sScript):
		if iPlayer == gc.getBARBARIAN_PLAYER():
			CyEngine().addLandmark(pPlot, CvUtil.convertToStr(sScript))
		else:
			CyEngine().addSign(pPlot, iPlayer, CvUtil.convertToStr(sScript))
	WBPlotScreen.iCounter = 10
	return


### REGISTER POPUP HANDLERS ###


events.setPopupHandlers(CvUtil.EventEditCityName, 'EditCityName', __eventEditCityNameApply, __eventEditCityNameBegin)
events.setPopupHandlers(CvUtil.EventPlaceObject, 'PlaceObject', __eventPlaceObjectApply, __eventPlaceObjectBegin)
events.setPopupHandlers(CvUtil.EventAwardTechsAndGold, 'AwardTechsAndGold', __eventAwardTechsAndGoldApply, __eventAwardTechsAndGoldBegin)
events.setPopupHandlers(CvUtil.EventEditUnitName, 'EditUnitName', __eventEditUnitNameApply, __eventEditUnitNameBegin)

## Platy Builder ##
events.setPopupHandlers(CvUtil.EventWBLandmarkPopup, 'WBLandmarkPopup', __eventWBLandmarkPopupApply, __eventWBScriptPopupBegin)
events.setPopupHandlers(CvUtil.EventShowWonder, 'ShowWonder', __eventShowWonderApply, __eventShowWonderBegin)
events.setPopupHandlers(1111, 'WBPlayerScript', __eventWBPlayerScriptPopupApply, __eventWBScriptPopupBegin)
events.setPopupHandlers(2222, 'WBCityScript', __eventWBCityScriptPopupApply, __eventWBScriptPopupBegin)
events.setPopupHandlers(3333, 'WBUnitScript', __eventWBUnitScriptPopupApply, __eventWBScriptPopupBegin)
events.setPopupHandlers(4444, 'WBGameScript', __eventWBGameScriptPopupApply, __eventWBScriptPopupBegin)
events.setPopupHandlers(5555, 'WBPlotScript', __eventWBPlotScriptPopupApply, __eventWBScriptPopupBegin)
events.setPopupHandlers(7777, 'WBStoredDataValue', __eventWBStoredDataValuePopupApply, __eventWBScriptPopupBegin),
## Platy Builder ##