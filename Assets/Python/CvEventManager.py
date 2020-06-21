## Sid Meier's Civilization 4
## Copyright Firaxis Games 2006
## 
## CvEventManager
## This class is passed an argsList from CvAppInterface.onEvent
## The argsList can contain anything from mouse location to key info
## The EVENTLIST that are being notified can be found 


from CvPythonExtensions import *
import CvUtil
import CvDebugTools
import PyHelpers
import Popup as PyPopup
import CvCameraControls
import CvTopCivs
import sys
import CvAdvisorUtils
import CvPlatyBuilderSettings

gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo


# globals
###################################################
class CvEventManager(object):
	def __init__(self):
		#################### ON EVENT MAP ######################
		#print "EVENTMANAGER INIT"
				
		self.bCtrl = False
		self.bShift = False
		self.bAlt = False
		self.bAllowCheats = False
		
		# OnEvent Enums
		self.EventLButtonDown=1
		self.EventLcButtonDblClick=2
		self.EventRButtonDown=3
		self.EventBack=4
		self.EventForward=5
		self.EventKeyDown=6
		self.EventKeyUp=7
	
		self.__LOG_MOVEMENT = 0
		self.__LOG_BUILDING = 0
		self.__LOG_COMBAT = 0
		self.__LOG_CONTACT = 0
		self.__LOG_IMPROVEMENT =0
		self.__LOG_CITYLOST = 0
		self.__LOG_CITYBUILDING = 0
		self.__LOG_TECH = 0
		self.__LOG_UNITBUILD = 0
		self.__LOG_UNITKILLED = 0 #Rhye
		self.__LOG_UNITLOST = 0
		self.__LOG_UNITPROMOTED = 0
		self.__LOG_UNITSELECTED = 0
		self.__LOG_UNITPILLAGE = 0
		self.__LOG_GOODYRECEIVED = 0
		self.__LOG_GREATPERSON = 0
		self.__LOG_RELIGION = 0
		self.__LOG_RELIGIONSPREAD = 0
		self.__LOG_GOLDENAGE = 0
		self.__LOG_ENDGOLDENAGE = 0
		self.__LOG_WARPEACE = 0
		self.__LOG_PUSH_MISSION = 0
		
		## EVENTLIST
		self.EventHandlerMap = {
			'mouseEvent'			: self.onMouseEvent,
			'kbdEvent' 				: self.onKbdEvent,
			'ModNetMessage'					: self.onModNetMessage,
			'Init'					: self.onInit,
			'Update'				: self.onUpdate,
			'UnInit'				: self.onUnInit,
			'OnSave'				: self.onSaveGame,
			'OnPreSave'				: self.onPreSave,
			'OnLoad'				: self.onLoadGame,
			'GameStart'				: self.onGameStart,
			'GameEnd'				: self.onGameEnd,
			'plotRevealed' 			: self.onPlotRevealed,
			'plotFeatureRemoved' 	: self.onPlotFeatureRemoved,
			'plotPicked'			: self.onPlotPicked,
			'nukeExplosion'			: self.onNukeExplosion,
			'gotoPlotSet'			: self.onGotoPlotSet,
			'BeginGameTurn'			: self.onBeginGameTurn,
			'EndGameTurn'			: self.onEndGameTurn,
			'BeginPlayerTurn'		: self.onBeginPlayerTurn,
			'EndPlayerTurn'			: self.onEndPlayerTurn,
			'endTurnReady'			: self.onEndTurnReady,
			'combatResult' 			: self.onCombatResult,
		  'combatLogCalc'	 		: self.onCombatLogCalc,
		  'combatLogHit'				: self.onCombatLogHit,
			'improvementBuilt' 		: self.onImprovementBuilt,
			'improvementDestroyed' 		: self.onImprovementDestroyed,
			'routeBuilt' 		: self.onRouteBuilt,
			'firstContact' 			: self.onFirstContact,
			'cityBuilt' 			: self.onCityBuilt,
			'cityRazed'				: self.onCityRazed,
			'cityAcquired' 			: self.onCityAcquired,
			'cityAcquiredAndKept' 	: self.onCityAcquiredAndKept,
			'cityLost'				: self.onCityLost,
			'cultureExpansion' 		: self.onCultureExpansion,
			'cityGrowth' 			: self.onCityGrowth,
			'cityDoTurn' 			: self.onCityDoTurn,
			'cityBuildingUnit'	: self.onCityBuildingUnit,
			'cityBuildingBuilding'	: self.onCityBuildingBuilding,
			'cityRename'				: self.onCityRename,
			'cityHurry'				: self.onCityHurry,
			'selectionGroupPushMission'		: self.onSelectionGroupPushMission,
			'unitMove' 				: self.onUnitMove,
			'unitSetXY' 			: self.onUnitSetXY,
			'unitCreated' 			: self.onUnitCreated,
			'unitBuilt' 			: self.onUnitBuilt,
			'unitKilled'			: self.onUnitKilled,
			'unitLost'				: self.onUnitLost,
			'unitPromoted'			: self.onUnitPromoted,
			'unitSelected'			: self.onUnitSelected, 
			'UnitRename'				: self.onUnitRename,
			'unitPillage'				: self.onUnitPillage,
			'unitSpreadReligionAttempt'	: self.onUnitSpreadReligionAttempt,
			'unitGifted'				: self.onUnitGifted,
			'unitBuildImprovement'				: self.onUnitBuildImprovement,
			'goodyReceived'		: self.onGoodyReceived,
			'greatPersonBorn'      	: self.onGreatPersonBorn,
			'buildingBuilt' 		: self.onBuildingBuilt,
			'projectBuilt' 			: self.onProjectBuilt,
			'techAcquired'			: self.onTechAcquired,
			'techSelected'			: self.onTechSelected,
			'religionFounded'		: self.onReligionFounded,
			'religionSpread'		: self.onReligionSpread, 
			'religionRemove'		: self.onReligionRemove, 
			'corporationFounded'	: self.onCorporationFounded,
			'corporationSpread'		: self.onCorporationSpread, 
			'corporationRemove'		: self.onCorporationRemove, 
			'goldenAge'				: self.onGoldenAge,
			'endGoldenAge'			: self.onEndGoldenAge,
			'chat' 					: self.onChat,
			'victory'				: self.onVictory,
			'vassalState'			: self.onVassalState,
			'changeWar'				: self.onChangeWar,
			'setPlayerAlive'		: self.onSetPlayerAlive,
			'playerChangeStateReligion'		: self.onPlayerChangeStateReligion,
			'playerGoldTrade'		: self.onPlayerGoldTrade,
			'windowActivation'		: self.onWindowActivation,
			'gameUpdate'			: self.onGameUpdate,		# sample generic event
			'playerChangeStateReligion'	: self.onPlayerChangeStateReligion,
			'vassalState'			: self.onVassalState,
			'revolution'			: self.onRevolution,
			'cityCaptureGold'		: self.onCityCaptureGold,
			'tradeMission'			: self.onTradeMission,
			'playerSlaveTrade'		: self.onPlayerSlaveTrade,
			'releasedPlayer'		: self.onReleasedPlayer,
			'blockade'			: self.onBlockade,
			'peaceBrokered'			: self.onPeaceBrokered,
		}

		################## Events List ###############################
		#
		# Dictionary of Events, indexed by EventID (also used at popup context id)
		#   entries have name, beginFunction, applyFunction [, randomization weight...]
		#
		# Normal events first, random events after
		#	
		################## Events List ###############################
		self.Events={
		}	
#################### EVENT STARTERS ######################
	def handleEvent(self, argsList):
		'EventMgr entry point'
		# extract the last 6 args in the list, the first arg has already been consumed
		self.origArgsList = argsList	# point to original
		tag = argsList[0]				# event type string
		idx = len(argsList)-6
		bDummy = false
		self.bDbg, bDummy, self.bAlt, self.bCtrl, self.bShift, self.bAllowCheats = argsList[idx:]
		ret = 0
		if self.EventHandlerMap.has_key(tag):
			fxn = self.EventHandlerMap[tag]
			ret = fxn(argsList[1:idx])
		return ret
		
#################### EVENT APPLY ######################	
	def beginEvent( self, context, argsList=-1 ):
		'Begin Event'
		entry = self.Events[context]
		return entry[2]( argsList )
	
	def applyEvent( self, argsList ):
		'Apply the effects of an event '
		context, playerID, netUserData, popupReturn = argsList
		
		if context == CvUtil.PopupTypeEffectViewer:
			return CvDebugTools.g_CvDebugTools.applyEffectViewer( playerID, netUserData, popupReturn )
		
		entry = self.Events[context]
				
		if ( context not in CvUtil.SilentEvents ):
			self.reportEvent(entry, context, (playerID, netUserData, popupReturn) )
		return entry[1]( playerID, netUserData, popupReturn )   # the apply function

	def reportEvent(self, entry, context, argsList):
		'Report an Event to Events.log '
		if (gc.getGame().getActivePlayer() != -1):
			message = "DEBUG Event: %s (%s)" %(entry[0], gc.getActivePlayer().getCivilizationShortDescription(0))
			CyInterface().addImmediateMessage(message,"")
			CvUtil.pyPrint(message)
		return 0
		
#################### ON EVENTS ######################
	def onKbdEvent(self, argsList):
		'keypress handler - return 1 if the event was consumed'
											
		return 0

	def onModNetMessage(self, argsList):
		'Called whenever CyMessageControl().sendModNetMessage() is called - this is all for you modders!'
		
		print("Modder's net message!")
		
		CvUtil.pyPrint( 'onModNetMessage' )

	def onInit(self, argsList):
		'Called when Civ starts up'
		CvUtil.pyPrint( 'OnInit' )
		
	def onUpdate(self, argsList):
		'Called every frame'
		fDeltaTime = argsList[0]
		
		# allow camera to be updated
		CvCameraControls.g_CameraControls.onUpdate( fDeltaTime )
		
	def onWindowActivation(self, argsList):
		'Called when the game window activates or deactivates'
		bActive = argsList[0]
		
	def onUnInit(self, argsList):
		'Called when Civ shuts down'
		CvUtil.pyPrint('OnUnInit')
	
	def onPreSave(self, argsList):
		"called before a game is actually saved"
		CvUtil.pyPrint('OnPreSave')
	
	def onSaveGame(self, argsList):
		"return the string to be saved - Must be a string"
		return ""

	def onLoadGame(self, argsList):
		CvAdvisorUtils.resetNoLiberateCities()
		return 0

	def onGameStart(self, argsList):
		'Called at the start of the game'
		#Rhye - dawn of map must appear in late starts too
		#if (gc.getGame().getGameTurnYear() == gc.getDefineINT("START_YEAR") and not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_START)):
		if (gc.getGame().getStartEra() == gc.getDefineINT("STANDARD_ERA") or gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_START)):
			for iPlayer in range(gc.getMAX_PLAYERS()):
				player = gc.getPlayer(iPlayer)
				if (player.isAlive() and player.isHuman()):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
					popupInfo.setText(u"showDawnOfMan")
					popupInfo.addPopup(iPlayer)
		else:
			CyInterface().setSoundSelectionReady(true)

		if gc.getGame().isPbem():
			for iPlayer in range(gc.getMAX_PLAYERS()):
				player = gc.getPlayer(iPlayer)
				if (player.isAlive() and player.isHuman()):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_DETAILS)
					popupInfo.setOption1(true)
					popupInfo.addPopup(iPlayer)

		CvAdvisorUtils.resetNoLiberateCities()
																	
	def onGameEnd(self, argsList):
		'Called at the End of the game'
		print("Game is ending")
		return

	def onBeginGameTurn(self, argsList):
		'Called at the beginning of the end of each turn'
		iGameTurn = argsList[0]
		CvTopCivs.CvTopCivs().turnChecker(iGameTurn)

	def onEndGameTurn(self, argsList):
		'Called at the end of the end of each turn'
		iGameTurn = argsList[0]
		
	def onBeginPlayerTurn(self, argsList):
		'Called at the beginning of a players turn'
		iGameTurn, iPlayer = argsList

	def onEndPlayerTurn(self, argsList):
		'Called at the end of a players turn'
		iGameTurn, iPlayer = argsList
		
		if (gc.getGame().getElapsedGameTurns() == 1):
			if (gc.getPlayer(iPlayer).isHuman()):
				if (gc.getPlayer(iPlayer).canRevolution(0)):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_CHANGECIVIC)
					popupInfo.addPopup(iPlayer)
		
		CvAdvisorUtils.resetAdvisorNags()
		CvAdvisorUtils.endTurnFeats(iPlayer)

	def onEndTurnReady(self, argsList):
		iGameTurn = argsList[0]

	def onFirstContact(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Contact'
		iTeamX,iHasMetTeamY = argsList
		if (not self.__LOG_CONTACT):
			return
		CvUtil.pyPrint('Team %d has met Team %d' %(iTeamX, iHasMetTeamY))
	
	def onCombatResult(self, argsList):
		'Combat Result'
		pWinner,pLoser = argsList
		playerX = PyPlayer(pWinner.getOwner())
		unitX = PyInfo.UnitInfo(pWinner.getUnitType())
		playerY = PyPlayer(pLoser.getOwner())
		unitY = PyInfo.UnitInfo(pLoser.getUnitType())
		if (not self.__LOG_COMBAT):
			return
		if playerX and playerX and unitX and playerY:
			CvUtil.pyPrint('Player %d Civilization %s Unit %s has defeated Player %d Civilization %s Unit %s' 
				%(playerX.getID(), playerX.getCivilizationName(), unitX.getDescription(), 
				playerY.getID(), playerY.getCivilizationName(), unitY.getDescription()))

	def onCombatLogCalc(self, argsList):
		'Combat Result'	
		genericArgs = argsList[0][0]
		cdAttacker = genericArgs[0]
		cdDefender = genericArgs[1]
		iCombatOdds = genericArgs[2]
		CvUtil.combatMessageBuilder(cdAttacker, cdDefender, iCombatOdds)
		
	def onCombatLogHit(self, argsList):
		'Combat Message'
		global gCombatMessages, gCombatLog
		genericArgs = argsList[0][0]
		cdAttacker = genericArgs[0]
		cdDefender = genericArgs[1]
		iIsAttacker = genericArgs[2]
		iDamage = genericArgs[3]
		
		if cdDefender.eOwner == cdDefender.eVisualOwner:
			szDefenderName = gc.getPlayer(cdDefender.eOwner).getNameKey()
		else:
			szDefenderName = localText.getText("TXT_KEY_TRAIT_PLAYER_UNKNOWN", ())
		if cdAttacker.eOwner == cdAttacker.eVisualOwner:
			szAttackerName = gc.getPlayer(cdAttacker.eOwner).getNameKey()
		else:
			szAttackerName = localText.getText("TXT_KEY_TRAIT_PLAYER_UNKNOWN", ())

		if (iIsAttacker == 0):				
			combatMessage = localText.getText("TXT_KEY_COMBAT_MESSAGE_HIT", (szDefenderName, cdDefender.sUnitName, iDamage, cdDefender.iCurrHitPoints, cdDefender.iMaxHitPoints))
			CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
			CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
			if (cdDefender.iCurrHitPoints <= 0):
				combatMessage = localText.getText("TXT_KEY_COMBAT_MESSAGE_DEFEATED", (szAttackerName, cdAttacker.sUnitName, szDefenderName, cdDefender.sUnitName))
				CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
				CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
		elif (iIsAttacker == 1):
			combatMessage = localText.getText("TXT_KEY_COMBAT_MESSAGE_HIT", (szAttackerName, cdAttacker.sUnitName, iDamage, cdAttacker.iCurrHitPoints, cdAttacker.iMaxHitPoints))
			CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
			CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
			if (cdAttacker.iCurrHitPoints <= 0):
				combatMessage = localText.getText("TXT_KEY_COMBAT_MESSAGE_DEFEATED", (szDefenderName, cdDefender.sUnitName, szAttackerName, cdAttacker.sUnitName))
				CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
				CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)

	def onImprovementBuilt(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettingsCvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Improvement Built'
		iImprovement, iX, iY = argsList
		if (not self.__LOG_IMPROVEMENT):
			return
		CvUtil.pyPrint('Improvement %s was built at %d, %d'
			%(PyInfo.ImprovementInfo(iImprovement).getDescription(), iX, iY))

	def onImprovementDestroyed(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Improvement Destroyed'
		iImprovement, iOwner, iX, iY = argsList
		if (not self.__LOG_IMPROVEMENT):
			return
		CvUtil.pyPrint('Improvement %s was Destroyed at %d, %d'
			%(PyInfo.ImprovementInfo(iImprovement).getDescription(), iX, iY))

	def onRouteBuilt(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Route Built'
		iRoute, iX, iY = argsList
		if (not self.__LOG_IMPROVEMENT):
			return
		CvUtil.pyPrint('Route %s was built at %d, %d'
			%(gc.getRouteInfo(iRoute).getDescription(), iX, iY))

	def onPlotRevealed(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Plot Revealed'
		pPlot = argsList[0]
		iTeam = argsList[1]

	def onPlotFeatureRemoved(self, argsList):
		'Plot Revealed'
		pPlot = argsList[0]
		iFeatureType = argsList[1]
		pCity = argsList[2] # This can be null

	def onPlotPicked(self, argsList):
		'Plot Picked'
		pPlot = argsList[0]
		CvUtil.pyPrint('Plot was picked at %d, %d'
			%(pPlot.getX(), pPlot.getY()))

	def onNukeExplosion(self, argsList):
		'Nuke Explosion'
		pPlot, pNukeUnit = argsList
		CvUtil.pyPrint('Nuke detonated at %d, %d'
			%(pPlot.getX(), pPlot.getY()))

	def onGotoPlotSet(self, argsList):
		'Nuke Explosion'
		pPlot, iPlayer = argsList

	def onBuildingBuilt(self, argsList):
		'Building Completed'
		pCity, iBuildingType = argsList
		game = gc.getGame()
		if ((not gc.getGame().isNetworkMultiPlayer()) and (pCity.getOwner() == gc.getGame().getActivePlayer()) and (gc.getPlayer(pCity.getOwner()).countNumBuildings(iBuildingType) <= 1)):
			# If this is a wonder...
			if not CyGame().GetWorldBuilderMode():	## Platy Builder ##
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setData1(iBuildingType)
				popupInfo.setData2(pCity.getID())
				popupInfo.setData3(0)
				popupInfo.setText(u"showWonderMovie")
				popupInfo.addPopup(pCity.getOwner())

		CvAdvisorUtils.buildingBuiltFeats(pCity, iBuildingType)

		if (not self.__LOG_BUILDING):
			return
		CvUtil.pyPrint('%s was finished by Player %d Civilization %s' 
			%(PyInfo.BuildingInfo(iBuildingType).getDescription(), pCity.getOwner(), gc.getPlayer(pCity.getOwner()).getCivilizationDescription(0)))
	
	def onProjectBuilt(self, argsList):
		'Project Completed'
		pCity, iProjectType = argsList
		game = gc.getGame()
		if ((not gc.getGame().isNetworkMultiPlayer()) and (pCity.getOwner() == gc.getGame().getActivePlayer())):
			if not CyGame().GetWorldBuilderMode():	#Platy Builder
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setData1(iProjectType)
				popupInfo.setData2(pCity.getID())
				popupInfo.setData3(2)
				popupInfo.setText(u"showWonderMovie")
				popupInfo.addPopup(pCity.getOwner())
				
	def onSelectionGroupPushMission(self, argsList):
		'selection group mission'
		eOwner = argsList[0]
		eMission = argsList[1]
		iNumUnits = argsList[2]
		listUnitIds = argsList[3]
		
		if (not self.__LOG_PUSH_MISSION):
			return
		if pHeadUnit:
			CvUtil.pyPrint("Selection Group pushed mission %d" %(eMission))
	
	def onUnitMove(self, argsList):
		'unit move'
		pPlot,pUnit,pOldPlot = argsList
		player = PyPlayer(pUnit.getOwner())
		unitInfo = PyInfo.UnitInfo(pUnit.getUnitType())
		if (not self.__LOG_MOVEMENT):
			return
		if player and unitInfo:
			CvUtil.pyPrint('Player %d Civilization %s unit %s is moving to %d, %d' 
				%(player.getID(), player.getCivilizationName(), unitInfo.getDescription(), 
				pUnit.getX(), pUnit.getY()))

	def onUnitSetXY(self, argsList):
		'units xy coords set manually'
		pPlot,pUnit = argsList
		player = PyPlayer(pUnit.getOwner())
		unitInfo = PyInfo.UnitInfo(pUnit.getUnitType())
		if (not self.__LOG_MOVEMENT):
			return
		
	def onUnitCreated(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Unit Completed'
		unit = argsList[0]
		player = PyPlayer(unit.getOwner())
		if (not self.__LOG_UNITBUILD):
			return

	def onUnitBuilt(self, argsList):
		'Unit Completed'
		city = argsList[0]
		unit = argsList[1]
		player = PyPlayer(city.getOwner())

		CvAdvisorUtils.unitBuiltFeats(city, unit)
		
		if (not self.__LOG_UNITBUILD):
			return
		CvUtil.pyPrint('%s was finished by Player %d Civilization %s' 
			%(PyInfo.UnitInfo(unit.getUnitType()).getDescription(), player.getID(), player.getCivilizationName()))
	
	def onUnitKilled(self, argsList):
		'Unit Killed'
		unit, iAttacker = argsList
		player = PyPlayer(unit.getOwner())
		attacker = PyPlayer(iAttacker)
		if (not self.__LOG_UNITKILLED):
			return
		CvUtil.pyPrint('Player %d Civilization %s Unit %s was killed by Player %d' 
			%(player.getID(), player.getCivilizationName(), PyInfo.UnitInfo(unit.getUnitType()).getDescription(), attacker.getID()))

	def onUnitLost(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Unit Lost'
		unit = argsList[0]
		player = PyPlayer(unit.getOwner())
		if (not self.__LOG_UNITLOST):
			return
		CvUtil.pyPrint('%s was lost by Player %d Civilization %s' 
			%(PyInfo.UnitInfo(unit.getUnitType()).getDescription(), player.getID(), player.getCivilizationName()))
	
	def onUnitPromoted(self, argsList):
		'Unit Promoted'
		pUnit, iPromotion = argsList
		player = PyPlayer(pUnit.getOwner())
		if (not self.__LOG_UNITPROMOTED):
			return
		CvUtil.pyPrint('Unit Promotion Event: %s - %s' %(player.getCivilizationName(), pUnit.getName(),))
	
	def onUnitSelected(self, argsList):
		'Unit Selected'
		unit = argsList[0]
		player = PyPlayer(unit.getOwner())
		if (not self.__LOG_UNITSELECTED):
			return
		CvUtil.pyPrint('%s was selected by Player %d Civilization %s' 
			%(PyInfo.UnitInfo(unit.getUnitType()).getDescription(), player.getID(), player.getCivilizationName()))
	
	def onUnitRename(self, argsList):
		'Unit is renamed'
		pUnit = argsList[0]
		if (pUnit.getOwner() == gc.getGame().getActivePlayer()):
			self.__eventEditUnitNameBegin(pUnit)
	
	def onUnitPillage(self, argsList):
		'Unit pillages a plot'
		pUnit, iImprovement, iRoute, iOwner, iGold = argsList
		iPlotX = pUnit.getX()
		iPlotY = pUnit.getY()
		pPlot = CyMap().plot(iPlotX, iPlotY)
		
		if (not self.__LOG_UNITPILLAGE):
			return
		CvUtil.pyPrint("Player %d's %s pillaged improvement %d and route %d at plot at (%d, %d)" 
			%(iOwner, PyInfo.UnitInfo(pUnit.getUnitType()).getDescription(), iImprovement, iRoute, iPlotX, iPlotY))
	
	def onUnitSpreadReligionAttempt(self, argsList):
		'Unit tries to spread religion to a city'
		pUnit, iReligion, bSuccess = argsList
		
		iX = pUnit.getX()
		iY = pUnit.getY()
		pPlot = CyMap().plot(iX, iY)
		pCity = pPlot.getPlotCity()
	
	def onUnitGifted(self, argsList):
		'Unit is gifted from one player to another'
		pUnit, iGiftingPlayer, pPlotLocation = argsList
	
	def onUnitBuildImprovement(self, argsList):
		'Unit begins enacting a Build (building an Improvement or Route)'
		pUnit, iBuild, bFinished = argsList

	def onGoodyReceived(self, argsList):
		'Goody received'
		iPlayer, pPlot, pUnit, iGoodyType = argsList
		if (not self.__LOG_GOODYRECEIVED):
			return
		CvUtil.pyPrint('%s received a goody' %(gc.getPlayer(iPlayer).getCivilizationDescription(0)),)
	
	def onGreatPersonBorn(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Unit Promoted'
		pUnit, iPlayer, pCity = argsList
		player = PyPlayer(iPlayer)
		if pUnit.isNone() or pCity.isNone():
			return
		if (not self.__LOG_GREATPERSON):
			return
		CvUtil.pyPrint('A %s was born for %s in %s' %(pUnit.getName(), player.getCivilizationName(), pCity.getName()))
	
	def onTechAcquired(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Tech Acquired'
		iTechType, iTeam, iPlayer, bAnnounce = argsList
		# Note that iPlayer may be NULL (-1) and not a refer to a player object
		
		# Show tech splash when applicable
		if (iPlayer > -1 and bAnnounce and not CyInterface().noTechSplash()):
			if (gc.getGame().isFinalInitialized() and not gc.getGame().GetWorldBuilderMode()):
				if ((not gc.getGame().isNetworkMultiPlayer()) and (iPlayer == gc.getGame().getActivePlayer())):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
					popupInfo.setData1(iTechType)
					popupInfo.setText(u"showTechSplash")
					popupInfo.addPopup(iPlayer)
				
		if (not self.__LOG_TECH):
			return
		CvUtil.pyPrint('%s was finished by Team %d' 
			%(PyInfo.TechnologyInfo(iTechType).getDescription(), iTeam))
	
	def onTechSelected(self, argsList):
		'Tech Selected'
		iTechType, iPlayer = argsList
		if (not self.__LOG_TECH):
			return
		CvUtil.pyPrint('%s was selected by Player %d' %(PyInfo.TechnologyInfo(iTechType).getDescription(), iPlayer))
	
	def onReligionFounded(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Religion Founded'
		iReligion, iFounder = argsList
		player = PyPlayer(iFounder)
		
		iCityId = gc.getGame().getHolyCity(iReligion).getID()
		if (gc.getGame().isFinalInitialized() and not gc.getGame().GetWorldBuilderMode()):
			if ((not gc.getGame().isNetworkMultiPlayer()) and (iFounder == gc.getGame().getActivePlayer())):
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setData1(iReligion)
				popupInfo.setData2(iCityId)
				popupInfo.setData3(1)
				popupInfo.setText(u"showWonderMovie")
				popupInfo.addPopup(iFounder)
		
		if (not self.__LOG_RELIGION):
			return
		CvUtil.pyPrint('Player %d Civilization %s has founded %s'
			%(iFounder, player.getCivilizationName(), gc.getReligionInfo(iReligion).getDescription()))

	def onReligionSpread(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Religion Has Spread to a City'
		iReligion, iOwner, pSpreadCity = argsList
		player = PyPlayer(iOwner)
		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has spread to Player %d Civilization %s city of %s'
			%(gc.getReligionInfo(iReligion).getDescription(), iOwner, player.getCivilizationName(), pSpreadCity.getName()))

	def onReligionRemove(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Religion Has been removed from a City'
		iReligion, iOwner, pRemoveCity = argsList
		player = PyPlayer(iOwner)
		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has been removed from Player %d Civilization %s city of %s'
			%(gc.getReligionInfo(iReligion).getDescription(), iOwner, player.getCivilizationName(), pRemoveCity.getName()))
				
	def onCorporationFounded(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Corporation Founded'
		iCorporation, iFounder = argsList
		player = PyPlayer(iFounder)
		
		if (not self.__LOG_RELIGION):
			return
		CvUtil.pyPrint('Player %d Civilization %s has founded %s'
			%(iFounder, player.getCivilizationName(), gc.getCorporationInfo(iCorporation).getDescription()))

	def onCorporationSpread(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Corporation Has Spread to a City'
		iCorporation, iOwner, pSpreadCity = argsList
		player = PyPlayer(iOwner)
		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has spread to Player %d Civilization %s city of %s'
			%(gc.getCorporationInfo(iCorporation).getDescription(), iOwner, player.getCivilizationName(), pSpreadCity.getName()))

	def onCorporationRemove(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Corporation Has been removed from a City'
		iCorporation, iOwner, pRemoveCity = argsList
		player = PyPlayer(iOwner)
		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has been removed from Player %d Civilization %s city of %s'
			%(gc.getReligionInfo(iReligion).getDescription(), iOwner, player.getCivilizationName(), pRemoveCity.getName()))
				
	def onGoldenAge(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Golden Age'
		iPlayer = argsList[0]
		player = PyPlayer(iPlayer)
		if (not self.__LOG_GOLDENAGE):
			return
		CvUtil.pyPrint('Player %d Civilization %s has begun a golden age'
			%(iPlayer, player.getCivilizationName()))

	def onEndGoldenAge(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'End Golden Age'
		iPlayer = argsList[0]
		player = PyPlayer(iPlayer)
		if (not self.__LOG_ENDGOLDENAGE):
			return
		CvUtil.pyPrint('Player %d Civilization %s golden age has ended'
			%(iPlayer, player.getCivilizationName()))

	def onChangeWar(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'War Status Changes'
		bIsWar = argsList[0]
		iTeam = argsList[1]
		iRivalTeam = argsList[2]
		if (not self.__LOG_WARPEACE):
			return
		if (bIsWar):
			strStatus = "declared war"
		else:
			strStatus = "declared peace"
		CvUtil.pyPrint('Team %d has %s on Team %d'
			%(iTeam, strStatus, iRivalTeam))
	
	def onChat(self, argsList):
		'Chat Message Event'
		chatMessage = "%s" %(argsList[0],)
		
	def onSetPlayerAlive(self, argsList):
		'Set Player Alive Event'
		iPlayerID = argsList[0]
		bNewValue = argsList[1]
		CvUtil.pyPrint("Player %d's alive status set to: %d" %(iPlayerID, int(bNewValue)))
		
	def onPlayerChangeStateReligion(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'Player changes his state religion'
		iPlayer, iNewReligion, iOldReligion = argsList
		
	def onPlayerGoldTrade(self, argsList):
		'Player Trades gold to another player'
		iFromPlayer, iToPlayer, iGoldAmount = argsList
		
	def onCityBuilt(self, argsList):
		'City Built'
		city = argsList[0]
		#if (city.getOwner() == gc.getGame().getActivePlayer()):
 		#	self.__eventEditCityNameBegin(city, False)	    #Rhye
		CvUtil.pyPrint('City Built Event: %s' %(city.getName()))
		
	def onCityRazed(self, argsList):
		'City Razed'
		city, iPlayer = argsList
		iOwner = city.findHighestCulture()
		
		#Rhye - start bugfix
		#owner = PyPlayer(city.getOwner())
		owner = PyPlayer(city.getPreviousOwner())
		#Rhye - end bugfix
		
		razor = PyPlayer(iPlayer)
		CvUtil.pyPrint('Player %d Civilization %s City %s was razed by Player %d' 
			%(owner.getID(), owner.getCivilizationName(), city.getName(), razor.getID()))
		
		# Partisans!
		if city.getPopulation > 1 and iOwner != -1 and iPlayer != -1:
			owner = gc.getPlayer(iOwner)
			if not owner.isBarbarian() and owner.getNumCities() > 0:
				if gc.getTeam(owner.getTeam()).isAtWar(gc.getPlayer(iPlayer).getTeam()):
					if gc.getNumEventTriggerInfos() > 0: # prevents mods that don't have events from getting an error
						iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_PARTISANS')
						if iEvent != -1 and gc.getGame().isEventActive(iEvent) and owner.getEventTriggerWeight(iEvent) < 0:
							triggerData = owner.initTriggeredData(iEvent, true, -1, city.getX(), city.getY(), iPlayer, city.getID(), -1, -1, -1, -1)
			
		CvUtil.pyPrint("City Razed Event: %s" %(city.getName(),))
	
	def onCityAcquired(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'City Acquired'
		iPreviousOwner,iNewOwner,pCity,bConquest,bTrade = argsList
		CvUtil.pyPrint('City Acquired Event: %s' %(pCity.getName()))
	
	def onCityAcquiredAndKept(self, argsList):
		'City Acquired and Kept'
		iOwner,pCity = argsList
		CvUtil.pyPrint('City Acquired and Kept Event: %s' %(pCity.getName()))
	
	def onCityLost(self, argsList):
		'City Lost'
		city = argsList[0]
		player = PyPlayer(city.getOwner())
		if (not self.__LOG_CITYLOST):
			return
		CvUtil.pyPrint('City %s was lost by Player %d Civilization %s' 
			%(city.getName(), player.getID(), player.getCivilizationName()))
	
	def onCultureExpansion(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderSettings.bPython: return
	## Platy Builder ##
		'City Culture Expansion'
		pCity = argsList[0]
		iPlayer = argsList[1]
		CvUtil.pyPrint("City %s's culture has expanded" %(pCity.getName(),))
	
	def onCityGrowth(self, argsList):
		'City Population Growth'
		pCity = argsList[0]
		iPlayer = argsList[1]
		CvUtil.pyPrint("%s has grown" %(pCity.getName(),))
	
	def onCityDoTurn(self, argsList):
		'City Production'
		pCity = argsList[0]
		iPlayer = argsList[1]

		CvAdvisorUtils.cityAdvise(pCity, iPlayer)
	
	def onCityBuildingUnit(self, argsList):
		'City begins building a unit'
		pCity = argsList[0]
		iUnitType = argsList[1]
		if (not self.__LOG_CITYBUILDING):
			return
		CvUtil.pyPrint("%s has begun building a %s" %(pCity.getName(),gc.getUnitInfo(iUnitType).getDescription()))
	
	def onCityBuildingBuilding(self, argsList):
		'City begins building a Building'
		pCity = argsList[0]
		iBuildingType = argsList[1]
		if (not self.__LOG_CITYBUILDING):
			return
		CvUtil.pyPrint("%s has begun building a %s" %(pCity.getName(),gc.getBuildingInfo(iBuildingType).getDescription()))
	
	def onCityRename(self, argsList):
		'City is renamed'
		pCity = argsList[0]
		if (pCity.getOwner() == gc.getGame().getActivePlayer()):
			self.__eventEditCityNameBegin(pCity, True)	
	
	def onCityHurry(self, argsList):
		'City is renamed'
		pCity = argsList[0]
		iHurryType = argsList[1]

	def onVictory(self, argsList):
		'Victory'
		iTeam, iVictory = argsList
		if (iVictory >= 0 and iVictory < gc.getNumVictoryInfos()):
			victoryInfo = gc.getVictoryInfo(int(iVictory))
			CvUtil.pyPrint("Victory!  Team %d achieves a %s victory"
				%(iTeam, victoryInfo.getDescription()))
	
	def onVassalState(self, argsList):
		'Vassal State'
		iMaster, iVassal, bVassal, bCapitulated = argsList
		
		if (bVassal):
			CvUtil.pyPrint("Team %d becomes a Vassal State of Team %d"
				%(iVassal, iMaster))
		else:
			CvUtil.pyPrint("Team %d revolts and is no longer a Vassal State of Team %d"
				%(iVassal, iMaster))
	
	def onGameUpdate(self, argsList):
		'sample generic event, called on each game turn slice'
		genericArgs = argsList[0][0]	# tuple of tuple of my args
		turnSlice = genericArgs[0]
		
	def onPlayerChangeStateReligion(self, argsList):
		'Player changes his state religion'
		iPlayer, iNewReligion, iOldReligion = argsList
	
	def onMouseEvent(self, argsList):
		'mouse handler - returns 1 if the event was consumed'
		
		return 0

	def onRevolution(self, argsList):
		'Revolution has started'
		iPlayer = argsList[0]
		
	def onCityCaptureGold(self, argsList):
		city, iPlayer, iGold = argsList
		
	def onTradeMission(self, argsList):
		iUnitType, iPlayer, iX, iY, iGold = argsList
		
	def onPlayerSlaveTrade(self, argsList):
		iPlayer, iGold = argsList
		
	def onReleasedPlayer(self, argsList):
		iPlayer, iReleasedPlayer = argsList
		
	def onBlockade(self, argsList):
		iPlayer, iGold = argsList
		
	def onPeaceBrokered(self, argsList):
		iBroker, iPlayer1, iPlayer2 = argsList