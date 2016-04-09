## autologger
## Modified from Ruff Mod 2w
## Modified from HOF MOD V1.61.001
## Modified from autolog by eotinb
## autolog's event handler
## by eotinb
##
## TODO:
## - Use onPlayerChangeStateReligion event

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import autolog
import time
import BugCore
import BugUtil
import TradeUtil

OPEN_LOG_EVENT_ID = CvUtil.getNewEventID("Autolog.OpenLog")
CUSTOM_ENTRY_EVENT_ID = CvUtil.getNewEventID("Autolog.CustomEntry")

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

AutologOpt = BugCore.game.Autolog
Logger = None
lPercent = "%"

iLastPillageGold = None
def doPillageGoldListener(argsList, value):
	global iLastPillageGold
	iLastPillageGold = value

def isLoggingOn():
	return AutologOpt.isLoggingOn()

def setLoggingOn(value):
	AutologOpt.setLoggingOn(value)

def setFileName(option, value):
	Logger.setLogFileName(value)

def setFilePath(option, value):
	Logger.setLogFilePath(value)

def setDefaultFileName(option, value):
	pass

def StartLogger(vsFileName):
	if (not vsFileName):
		vsFileName = Logger.getLogFileName()

	if (AutologOpt.isUseDefaultFileName()
		or not vsFileName):
		ePlayer = gc.getGame().getActivePlayer()
		szfileName = gc.getPlayer(ePlayer).getName()
	else:
		szfileName = vsFileName
	
	ziStyle = AutologOpt.getFormatStyle()
#	' valid styles are plain (0), html (1), forum with " for color(2) or forum without " for color(3)'
	if (ziStyle == 1):
		if not (szfileName.endswith(".html")):
			szfileName = szfileName + ".html"
	else:
		if not (szfileName.endswith(".txt")):
			szfileName = szfileName + ".txt"
	
	Logger.setLogFileName(szfileName)
	if (not AutologOpt.isSilent()):
		message = BugUtil.getText("TXT_KEY_AUTOLOG_LOGGING_GAME", (szfileName, ))
		CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, message, None, 2, None, ColorTypes(8), 0, 0, False, False)

class autologEventManager:

	def __init__(self, eventManager):

		global Logger
		Logger = autolog.autologInstance()
		
		AutoLogEvent(eventManager)

		# additions to self.Events
		moreEvents = {
			OPEN_LOG_EVENT_ID : ('LogOpenPopup', self.__OPEN_LOG_EVENT_IDApply, self.__OPEN_LOG_EVENT_IDBegin),
			CUSTOM_ENTRY_EVENT_ID : ('', self.__CUSTOM_ENTRY_EVENT_IDApply, self.__CUSTOM_ENTRY_EVENT_IDBegin),
		}
		eventManager.Events.update(moreEvents)

	def __OPEN_LOG_EVENT_IDBegin(self, argsList):
		popup = PyPopup.PyPopup(OPEN_LOG_EVENT_ID, EventContextTypes.EVENTCONTEXT_SELF)

		if (AutologOpt.isUseDefaultFileName()):
			popup.setHeaderString(BugUtil.getPlainText("TXT_KEY_AUTOLOG_POPUP_QUESTION"))
			popup.setBodyString(BugUtil.getPlainText("TXT_KEY_AUTOLOG_POPUP_ANSWERS"))
		else:
			popup.setHeaderString(BugUtil.getPlainText("TXT_KEY_AUTOLOG_ENTER_LOG_NAME"))
			popup.createEditBox(AutologOpt.getFileName())
			popup.setEditBoxMaxCharCount( 30 )

		popup.addButton(BugUtil.getPlainText("TXT_KEY_MAIN_MENU_OK"))
		popup.addButton(BugUtil.getPlainText("TXT_KEY_SCREEN_CANCEL"))
		popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

	def __OPEN_LOG_EVENT_IDApply(self, playerID, userData, popupReturn):
		if (popupReturn.getButtonClicked() != 1):
			setLoggingOn(True)
			StartLogger(popupReturn.getEditBoxString(0))
		else:
			setLoggingOn(False)
			message = BugUtil.getPlainText("TXT_KEY_AUTOLOG_NO_LOGGING")
			CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, message, None, 2, None, ColorTypes(8), 0, 0, False, False)

	def __CUSTOM_ENTRY_EVENT_IDBegin(self, argsList):
		if isLoggingOn():
			popup = PyPopup.PyPopup(CUSTOM_ENTRY_EVENT_ID, EventContextTypes.EVENTCONTEXT_SELF)
			popup.setHeaderString(BugUtil.getPlainText("TXT_KEY_AUTOLOG_CUSTOM_ENTRY"))
			popup.createEditBox("")
			popup.addButton(BugUtil.getPlainText("TXT_KEY_MAIN_MENU_OK"))
			popup.addButton(BugUtil.getPlainText("TXT_KEY_SCREEN_CANCEL"))
			popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

	def __CUSTOM_ENTRY_EVENT_IDApply(self, playerID, userData, popupReturn):
		if isLoggingOn():
			message = popupReturn.getEditBoxString(0)
			if (popupReturn.getButtonClicked() != 1):
				Logger.writeLog(message, vPrefix=AutologOpt.getPrefix())

				if (not AutologOpt.isSilent()):
					CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, message, None, 2, None, ColorTypes(8), 0, 0, False, False)

class AbstractAutoLogEvent(object):

	def __init__(self, eventManager, *args, **kwargs):
		super(AbstractAutoLogEvent, self).__init__(*args, **kwargs)

class AutoLogEvent(AbstractAutoLogEvent):

	def __init__(self, eventManager, *args, **kwargs):
		super(AutoLogEvent, self).__init__(eventManager, *args, **kwargs)

		eventManager.addEventHandler("kbdEvent", self.onKbdEvent)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("GameEnd", self.onGameEnd)
		eventManager.addEventHandler("EndGameTurn", self.onEndGameTurn)
		eventManager.addEventHandler("BeginPlayerTurn", self.onBeginPlayerTurn)
		eventManager.addEventHandler("EndPlayerTurn", self.onEndPlayerTurn)
		eventManager.addEventHandler("firstContact", self.onFirstContact)
		eventManager.addEventHandler("combatLogCalc", self.onCombatLogCalc)
		eventManager.addEventHandler("combatResult", self.onCombatResult)
		eventManager.addEventHandler("combatLogHit", self.onCombatLogHit)
		eventManager.addEventHandler("buildingBuilt", self.onBuildingBuilt)
		eventManager.addEventHandler("projectBuilt", self.onProjectBuilt)
		eventManager.addEventHandler("unitBuilt", self.onUnitBuilt)
		eventManager.addEventHandler("unitPromoted", self.onUnitPromoted)
		eventManager.addEventHandler("goodyReceived", self.onGoodyReceived)
		eventManager.addEventHandler("greatPersonBorn", self.onGreatPersonBorn)
		eventManager.addEventHandler("techAcquired", self.onTechAcquired)
		eventManager.addEventHandler("techSelected", self.onTechSelected)
		eventManager.addEventHandler("religionFounded", self.onReligionFounded)
		eventManager.addEventHandler("religionSpread", self.onReligionSpread)
		eventManager.addEventHandler("religionRemove", self.onReligionRemove)
		eventManager.addEventHandler("corporationFounded", self.onCorporationFounded)
		eventManager.addEventHandler("corporationSpread", self.onCorporationSpread)
		eventManager.addEventHandler("corporationRemove", self.onCorporationRemove)
		eventManager.addEventHandler("goldenAge", self.onGoldenAge)
		eventManager.addEventHandler("endGoldenAge", self.onEndGoldenAge)
		eventManager.addEventHandler("changeWar", self.onChangeWar)
		eventManager.addEventHandler("setPlayerAlive", self.onSetPlayerAlive)
		eventManager.addEventHandler("cityBuilt", self.onCityBuilt)
		eventManager.addEventHandler("cityRazed", self.onCityRazed)
		eventManager.addEventHandler("cityAcquired", self.onCityAcquired)
		eventManager.addEventHandler("cityLost", self.onCityLost)
		eventManager.addEventHandler("cultureExpansion", self.onCultureExpansion)
		eventManager.addEventHandler("cityGrowth", self.onCityGrowth)
		eventManager.addEventHandler("cityBuildingUnit", self.onCityBuildingUnit)
		eventManager.addEventHandler("cityBuildingBuilding", self.onCityBuildingBuilding)
		eventManager.addEventHandler("improvementBuilt", self.onImprovementBuilt)
		eventManager.addEventHandler("improvementDestroyed", self.onImprovementDestroyed)
		eventManager.addEventHandler("unitPillage", self.onUnitPillage)
		eventManager.addEventHandler("vassalState", self.onVassalState)
		eventManager.addEventHandler("selectionGroupPushMission", self.onSelectionGroupPushMission)
		eventManager.addEventHandler("DealOffered", self.onDealOffered)
		eventManager.addEventHandler("CityOffered", self.onCityOffered)
		eventManager.addEventHandler("HelpOffered", self.onHelpOffered)
		eventManager.addEventHandler("PeaceOffered", self.onPeaceOffered)
		eventManager.addEventHandler("VassalOffered", self.onVassalOffered)
		eventManager.addEventHandler("DealCanceled", self.onDealCanceled)
		eventManager.addEventHandler("DealAccepted", self.onDealAccepted)
		eventManager.addEventHandler("DealRejected", self.onDealRejected)
		#eventManager.addEventHandler("HelpDemanded", self.onHelpDemanded)
		eventManager.addEventHandler("HelpAccepted", self.onHelpAccepted)
		eventManager.addEventHandler("HelpRejected", self.onHelpRejected)
		#eventManager.addEventHandler("TributeDemanded", self.onTributeDemanded)
		eventManager.addEventHandler("TributeAccepted", self.onTributeAccepted)
		eventManager.addEventHandler("TributeRejected", self.onTributeRejected)
		#eventManager.addEventHandler("ReligionDemanded", self.onReligionDemanded)
		eventManager.addEventHandler("ReligionAccepted", self.onReligionAccepted)
		eventManager.addEventHandler("ReligionRejected", self.onReligionRejected)
		#eventManager.addEventHandler("CivicDemanded", self.onCivicDemanded)
		eventManager.addEventHandler("CivicAccepted", self.onCivicAccepted)
		eventManager.addEventHandler("CivicRejected", self.onCivicRejected)
		#eventManager.addEventHandler("WarDemanded", self.onWarDemanded)
		eventManager.addEventHandler("WarAccepted", self.onWarAccepted)
		eventManager.addEventHandler("WarRejected", self.onWarRejected)
		#eventManager.addEventHandler("EmbargoDemanded", self.onEmbargoDemanded)
		eventManager.addEventHandler("EmbargoAccepted", self.onEmbargoAccepted)
		eventManager.addEventHandler("EmbargoRejected", self.onEmbargoRejected)

		self.eventMgr = eventManager
		self.fOdds = 0.0
		self.iBattleWonDefending = 0
		self.iBattleLostDefending = 0
		self.iBattleWonAttacking = 0
		self.iBattleLostAttacking = 0
		self.iBattleWdlAttacking = 0
		self.iBattleEscAttacking = 0

		self.bHumanPlaying = False
		self.bHumanEndTurn = False
		self.bAIsTurn = False

		self.UnitKilled = 0
		self.WonLastRound = 0
		self.WdlAttacker = None
		self.WdlDefender = None
		
		self.CIVAttitude = None
		self.CIVCivics = None
		self.CIVReligion = None
		self.CityWhipCounter = None
		self.CityConscriptCounter = None

	def onKbdEvent(self, argsList):
		eventType,key,mx,my,px,py = argsList
		if ( eventType == self.eventMgr.EventKeyDown ):
			theKey=int(key)
			'Check if ALT + E was hit == echoes to text log and in-game log'
			if (theKey == int(InputTypes.KB_E)
			and self.eventMgr.bAlt
			and AutologOpt.isEnabled()
			and isLoggingOn()):
				self.eventMgr.beginEvent(CUSTOM_ENTRY_EVENT_ID)
				return 1

			'Check if ALT + L was hit == open in-game log'
			if (theKey == int(InputTypes.KB_L)
			and self.eventMgr.bAlt
			and AutologOpt.isEnabled()):
				if AutologOpt.isSilent():
					setLoggingOn(True)
					StartLogger("")
				else:
					self.eventMgr.beginEvent(OPEN_LOG_EVENT_ID)

				return 1

			'Check if ALT + B was hit == dump battle stats, and reset'
			if (theKey == int(InputTypes.KB_B)
			and self.eventMgr.bAlt
			and AutologOpt.isEnabled()
			and isLoggingOn()):
				Logger.writeLog("")
				Logger.writeLog(BugUtil.getPlainText("TXT_KEY_AUTOLOG_BATTLE_STATS"), vBold=True)
				message = BugUtil.getText("TXT_KEY_AUTOLOG_UNITS_VICTORIOUS_ATTACKING", (self.iBattleWonAttacking, ))
				Logger.writeLog(message, vColor="DarkRed")
				message = BugUtil.getText("TXT_KEY_AUTOLOG_UNITS_VICTORIOUS_DEFENDING", (self.iBattleWonDefending, ))
				Logger.writeLog(message, vColor="DarkRed")
				message = BugUtil.getText("TXT_KEY_AUTOLOG_UNITS_WITHDRAWING_ATTACKING", (self.iBattleWdlAttacking, ))
				Logger.writeLog(message, vColor="DarkRed")
				message = BugUtil.getText("TXT_KEY_AUTOLOG_UNITS_DEFEATED_ATTACKING", (self.iBattleLostAttacking, ))
				Logger.writeLog(message, vColor="Red")
				message = BugUtil.getText("TXT_KEY_AUTOLOG_UNITS_DEFEATED_DEFENDING", (self.iBattleLostDefending, ))
				Logger.writeLog(message, vColor="Red")
				message = BugUtil.getText("TXT_KEY_AUTOLOG_UNITS_ESCAPING_ATTACKING", (self.iBattleEscAttacking, ))
				Logger.writeLog(message, vColor="Red")

				self.iBattleWonDefending = 0
				self.iBattleLostDefending = 0
				self.iBattleWonAttacking = 0
				self.iBattleLostAttacking = 0
				self.iBattleWdlAttacking = 0
				self.iBattleEscAttacking = 0

				message = BugUtil.getPlainText("TXT_KEY_AUTOLOG_BATTLE_STATS_WRITTEN")
				CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, message, None, 2, None, ColorTypes(8), 0, 0, False, False)
				return 1

			'Check if ALT + T was hit == testing!'
#			if (theKey == int(InputTypes.KB_T)
#			and self.eventMgr.bAlt):
#				message = "Civ / Civic %i %i %i" % (0, 0, self.CIVCivics[0])
#				CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, message, None, 2, None, ColorTypes(8), 0, 0, False, False)

#				self.storeStuff()
#				return 1

			'Check if ALT + T was hit == testing!'
			if (theKey == int(InputTypes.KB_T)
			and self.eventMgr.bAlt):
				for i in range(0, 126):   #range(0,1000000):
					ci = gc.getColorInfo(i)
					ci2 = "XML Val %i %s" % (i, ci.getXmlVal())
					print ci2


	def onLoadGame(self, argsList):
		self.bHumanPlaying = True
		self.bHumanEndTurn = False
		self.bAIsTurn = False

		if (AutologOpt.isEnabled()
		and AutologOpt.isSilent()):
			setLoggingOn(True)
			StartLogger("")
		else:
			setLoggingOn(False)

		# initialize storage stuff
		self.initStuff()
		self.storeStuff()
		self.storeWhip()

	def onGameStart(self, argsList):
		self.bHumanPlaying = True
		self.bHumanEndTurn = False
		self.bAIsTurn = False

		if (AutologOpt.isEnabled()
		and AutologOpt.isSilent()):
			setLoggingOn(True)
			StartLogger("")
		else:
			setLoggingOn(False)

		# initialize storage stuff
		self.initStuff()
		self.storeStuff()
		self.storeWhip()

	def onGameEnd(self, argsList):
		'Called at the End of the game'

	def onEndGameTurn(self, argsList):
		iGameTurn = argsList[0]

		if isLoggingOn():
			self.checkStuff()
#			self.dumpStuff()
			self.storeStuff()

			zcurrturn = gc.getGame().getElapsedGameTurns() + 1 + AutologOpt.get4000BCTurn()
			zmaxturn = gc.getGame().getMaxTurns()
			zturn = gc.getGame().getGameTurn() + 1
			zyear = gc.getGame().getTurnYear(zturn)
			if (zyear < 0):
				zyear = str(-zyear) + BugUtil.getPlainText("TXT_KEY_AUTOLOG_BC")
			else:
				zyear = str(zyear) + BugUtil.getPlainText("TXT_KEY_AUTOLOG_AD")
			zCurrDateTime = time.strftime("%d-%b-%Y %H:%M:%S")

			if (zmaxturn == 0):
				zsTurn = "%i" % (zcurrturn)
			else:
				zsTurn = "%i/%i" % (zcurrturn, zmaxturn)
				
			message = BugUtil.getText("TXT_KEY_AUTOLOG_TURN", (zsTurn, zyear, zCurrDateTime))

			Logger.writeLog_pending_flush()
			Logger.writeLog_pending("")
			Logger.writeLog_pending(message, vBold=True, vUnderline=True)

		self.bHumanPlaying = True
		self.bHumanEndTurn = False
		self.bAIsTurn = False

	def onBeginPlayerTurn(self, argsList):
		'Called at the beginning of a players turn'
		iGameTurn, iPlayer = argsList

		if iPlayer == CyGame().getActivePlayer():
			self.bHumanPlaying = False
			self.bHumanEndTurn = True
			self.bAIsTurn = False

		if not self.bHumanEndTurn:
			return

		self.logSliders()

		if AutologOpt.isShowIBT():
#			Logger.writeLog_pending_flush()
			Logger.writeLog_pending("")
			Logger.writeLog_pending(BugUtil.getPlainText("TXT_KEY_AUTOLOG_AFTER_END_TURN"), vBold=True)
#			Logger.writeLog("After End Turn-:", vBold=True)

		if AutologOpt.isLogCityWhipStatus():
			iPlayer = gc.getActivePlayer()
			for i in range(0, iPlayer.getNumCities(), 1):
				iCity = iPlayer.getCity(i)
				iCurrentWhipCounter = iCity.getHurryAngerTimer()
				iCurrentConstrictCounter = iCity.getConscriptAngerTimer()
#				if iCurrentWhipCounter != 0: iCurrentWhipCounter += 1  # onBeginPlayerTurn fires after whip counter has decreased by 1

#				message = "Whip Testing: %s, current(%i), prior(%i), flat(%i)" % (iCity.getName(), iCurrentWhipCounter, self.CityWhipCounter[i], iCity.flatHurryAngerLength())
#				Logger.writeLog(message)

				if iCurrentWhipCounter > self.CityWhipCounter[i]:
					message = BugUtil.getText("TXT_KEY_AUTOLOG_WHIP_APPLIED", (iCity.getName(), ))
					Logger.writeLog(message, vColor="Red")

				if iCurrentConstrictCounter > self.CityConscriptCounter[i]:
					message = BugUtil.getText("TXT_KEY_AUTOLOG_CONSCRIPT", (gc.getUnitInfo(iCity.getConscriptUnit()).getDescription(), iCity.getName()))
					Logger.writeLog(message, vColor="Red")

				if (self.CityWhipCounter[i] != 0
				and iCurrentWhipCounter < self.CityWhipCounter[i]
				and iCurrentWhipCounter % iCity.flatHurryAngerLength() == 0):
					message = BugUtil.getText("TXT_KEY_AUTOLOG_WHIP_ANGER_DECREASED", (iCity.getName(), ))
					Logger.writeLog(message, vColor="DarkRed")

				if (self.CityConscriptCounter[i] != 0
				and iCurrentConstrictCounter < self.CityConscriptCounter[i]
				and iCurrentConstrictCounter % iCity.flatConscriptAngerLength() == 0):
					message = BugUtil.getText("TXT_KEY_AUTOLOG_DRAFT_ANGER_DECREASED", (iCity.getName(), ))
					Logger.writeLog(message, vColor="DarkRed")

			self.storeWhip()

	def onEndPlayerTurn(self, argsList):
		'Called at the end of a players turn'
		iGameTurn, iPlayer = argsList

		if (self.bHumanEndTurn
		and AutologOpt.isShowIBT()):
#			Logger.writeLog_pending_flush()
			Logger.writeLog_pending("")
			Logger.writeLog_pending(BugUtil.getPlainText("TXT_KEY_AUTOLOG_OTHER_PLAYER_ACTIONS"), vBold=True)
#			Logger.writeLog("Other Player Actions-:", vBold=True)

		if iPlayer == CyGame().getActivePlayer():
			self.bHumanPlaying = False
			self.bHumanEndTurn = False
			self.bAIsTurn = True

	def onFirstContact(self, argsList):
		if (AutologOpt.isLogContact()):
			iTeamX,iHasMetTeamY = argsList
			if (iTeamX == 0
			and gc.getGame().getGameTurn() > 0):

				sMsgArray = []
				sLeader = gc.getTeam(iHasMetTeamY).getName()
				message = BugUtil.getText("TXT_KEY_AUTOLOG_FIRST_CONTACT_TEAM", (sLeader, ))
#				Logger.writeLog(message)
				sMsgArray.append(message)

				for iPlayer in range(gc.getMAX_PLAYERS()):
					if gc.getPlayer(iPlayer).getTeam() == iHasMetTeamY:
						sLeader = gc.getLeaderHeadInfo(gc.getPlayer(iPlayer).getLeaderType()).getDescription()
						sCivName = gc.getPlayer(iPlayer).getCivilizationShortDescription(0)

						message = BugUtil.getText("TXT_KEY_AUTOLOG_FIRST_CONTACT_PLAYER", (sLeader, sCivName))
#						Logger.writeLog(message)
						sMsgArray.append(message)

				iLen = len(sMsgArray)
				if iLen == 2:
					Logger.writeLog(sMsgArray[1], vColor="Brown")
				else:
					for i in range(iLen):
						Logger.writeLog(sMsgArray[i], vColor="Brown")

	def onCombatLogCalc(self, argsList):
		if (AutologOpt.isLogCombat()):
			genericArgs = argsList[0][0]
			cdAttacker = genericArgs[0]
			cdDefender = genericArgs[1]
			iCombatOdds = genericArgs[2]

			self.fOdds = float(iCombatOdds)/10

			self.UnitKilled = 0
			self.WonLastRound = 0

	def onCombatResult(self, argsList):
		if (AutologOpt.isLogCombat()):

			self.UnitKilled = 1

			pWinner,pLoser = argsList
			if (pWinner.getOwner() == CyGame().getActivePlayer()
			or pLoser.getOwner() == CyGame().getActivePlayer()):
				playerX = PyPlayer(pWinner.getOwner())
				playerY = PyPlayer(pLoser.getOwner())
				winnerHealth = float(pWinner.baseCombatStr()) * float(pWinner.currHitPoints()) / float(pWinner.maxHitPoints())
				zsBattleLocn = self.getUnitLocation(pWinner)

				playerXDesc = PyPlayer(pWinner.getVisualOwner()).getCivilizationAdjective()
				playerYDesc = PyPlayer(pLoser.getVisualOwner()).getCivilizationAdjective()

				if (pWinner.getOwner() == CyGame().getActivePlayer()):
					if (self.bHumanPlaying):
						message = BugUtil.getText("TXT_KEY_AUTOLOG_WHILE_ATTACKING_DEFEATS", (zsBattleLocn, pWinner.getNameKey(), BugUtil.formatFloat(winnerHealth, 2), pWinner.baseCombatStr(), playerYDesc, pLoser.getNameKey(), BugUtil.formatFloat(self.fOdds, 1), lPercent))
						self.iBattleWonAttacking = self.iBattleWonAttacking + 1
					else:
						self.fOdds = 100 - self.fOdds
						message = BugUtil.getText("TXT_KEY_AUTOLOG_WHILE_DEFENDING_DEFEATS", (zsBattleLocn, pWinner.getNameKey(), BugUtil.formatFloat(winnerHealth, 2), pWinner.baseCombatStr(), playerYDesc, pLoser.getNameKey(), BugUtil.formatFloat(self.fOdds, 1), lPercent))
						self.iBattleWonDefending = self.iBattleWonDefending + 1

					Logger.writeLog(message, vColor="DarkRed")

				else:
					if (self.bHumanPlaying):
						message = BugUtil.getText("TXT_KEY_AUTOLOG_WHILE_ATTACKING_LOSES", (zsBattleLocn, pLoser.getNameKey(), playerXDesc, pWinner.getNameKey(), BugUtil.formatFloat(winnerHealth, 2), pWinner.baseCombatStr(), BugUtil.formatFloat(self.fOdds, 1), lPercent))
						self.iBattleLostAttacking = self.iBattleLostAttacking + 1
					else:
						self.fOdds = 100 - self.fOdds
						message = BugUtil.getText("TXT_KEY_AUTOLOG_WHILE_DEFENDING_LOSES", (zsBattleLocn, pLoser.getNameKey(), playerXDesc, pWinner.getNameKey(), BugUtil.formatFloat(winnerHealth, 2), pWinner.baseCombatStr(), BugUtil.formatFloat(self.fOdds, 1), lPercent))
						self.iBattleLostDefending = self.iBattleLostDefending + 1

					Logger.writeLog(message, vColor="Red")

	def onCombatLogHit(self, argsList):
		'Combat Message'
		genericArgs = argsList[0][0]
		cdAttacker = genericArgs[0]
		cdDefender = genericArgs[1]
		iIsAttacker = genericArgs[2]
		iDamage = genericArgs[3]

		self.WdlAttacker = cdAttacker
		self.WdlDefender = cdDefender
		
		if (iIsAttacker == 0):
			self.WonLastRound = 0
			
		elif (iIsAttacker == 1):
			self.WonLastRound = 1

	def onSelectionGroupPushMission(self, argsList):
		'selection group mission'
		eOwner = argsList[0]
		eMission = argsList[1]
		iNumUnits = argsList[2]
		listUnitIds = argsList[3]

#		print eOwner, eMission, iNumUnits, listUnitIds

		if self.WdlDefender == None: return

		if (AutologOpt.isLogCombat()
		and gc.getPlayer(eOwner).getTeam() == gc.getActivePlayer().getTeam()):

			playerX = PyPlayer(self.WdlDefender.eOwner)
			defCivName = playerX.getCivilizationAdjective()

			if self.UnitKilled == 0:
				if self.WonLastRound == 1:
					message = BugUtil.getText("TXT_KEY_AUTOLOG_WHILE_ATTACKING_ESCAPES", (self.WdlAttacker.sUnitName, defCivName, self.WdlDefender.sUnitName, BugUtil.formatFloat(self.fOdds, 1), lPercent))
					Logger.writeLog(message, vColor="Red")
					self.iBattleEscAttacking = self.iBattleEscAttacking + 1
				else:
					message = BugUtil.getText("TXT_KEY_AUTOLOG_WHILE_ATTACKING_DECIMATES", (self.WdlAttacker.sUnitName, defCivName, self.WdlDefender.sUnitName, BugUtil.formatFloat(self.fOdds, 1), lPercent))
					Logger.writeLog(message, vColor="DarkRed")
					self.iBattleWdlAttacking = self.iBattleWdlAttacking + 1

		self.WdlDefender = None

	def getUnitLocation(self, objUnit):
		iX = objUnit.getX()
		iY = objUnit.getY()
		pPlot = CyMap().plot(iX,iY)
		zOwner = pPlot.getOwner()
		if (zOwner == -1):
			if (pPlot.isWater()):
				if (pPlot.isLake()):
					zsLocn1 = BugUtil.getPlainText("TXT_KEY_AUTOLOG_ON_A_LAKE")
				elif (pPlot.isAdjacentToLand()):
					zsLocn1 = BugUtil.getPlainText("TXT_KEY_AUTOLOG_JUST_OFF_SHORE")
				else:
					zsLocn1 = BugUtil.getPlainText("TXT_KEY_AUTOLOG_ON_THE_HIGH_SEAS")
			else:
				zsLocn1 = BugUtil.getPlainText("TXT_KEY_AUTOLOG_IN_THE_WILD")
		else:
			playerX = PyPlayer(zOwner)
			zsLocn1 = BugUtil.getText("TXT_KEY_AUTOLOG_IN_TERRITORY", (playerX.getCivilizationAdjective(), ))

		for iiX in range(iX-1, iX+2, 1):
			for iiY in range(iY-1, iY+2, 1):
				pPlot = CyMap().plot(iiX,iiY)
				if (pPlot.isCity()):
					zsCity = pPlot.getPlotCity()
					return BugUtil.getText("TXT_KEY_AUTOLOG_IN_TERRITORY_AT", (zsLocn1, zsCity.getName()))

		for iiX in range(iX-4, iX+5, 1):
			for iiY in range(iY-4, iY+5, 1):
				pPlot = CyMap().plot(iiX,iiY)
				if (pPlot.isCity()):
					zsCity = pPlot.getPlotCity()
					return BugUtil.getText("TXT_KEY_AUTOLOG_IN_TERRITORY_NEAR", (zsLocn1, zsCity.getName()))

		return zsLocn1

	def onBuildingBuilt(self, argsList):
		if (AutologOpt.isLogBuildCompleted()):
			pCity, iBuildingType = argsList
			if pCity.getOwner() == CyGame().getActivePlayer():
				message = BugUtil.getText("TXT_KEY_AUTOLOG_FINISH_BUILDING", (pCity.getName(), gc.getBuildingInfo(iBuildingType).getDescription()))
				Logger.writeLog(message, vColor="Purple")

	def onProjectBuilt(self, argsList):
		if (AutologOpt.isLogBuildCompleted()):
			pCity, iProjectType = argsList
			if pCity.getOwner() == CyGame().getActivePlayer():
				message = BugUtil.getText("TXT_KEY_AUTOLOG_FINISH_PROJECT", (pCity.getName(), gc.getProjectInfo(iProjectType).getDescription()))
				Logger.writeLog(message, vColor="Purple")

	def onUnitBuilt(self, argsList):
		if (AutologOpt.isLogBuildCompleted()):
			pCity = argsList[0]
			unit = argsList[1]
			if pCity.getOwner() == CyGame().getActivePlayer():
				message = BugUtil.getText("TXT_KEY_AUTOLOG_FINISH_UNIT", (pCity.getName(), gc.getUnitInfo(unit.getUnitType()).getDescription()))
				Logger.writeLog(message, vColor="Purple")

	def onUnitPromoted(self, argsList):
		if (AutologOpt.isLogPromotion()):
			pUnit, iPromotion = argsList
			if pUnit.getOwner() == CyGame().getActivePlayer():
				message = BugUtil.getText("TXT_KEY_AUTOLOG_PROMOTION", (pUnit.getName(), PyInfo.PromotionInfo(iPromotion).getDescription()))
				Logger.writeLog(message, vColor="DarkOrange")

	def onGoodyReceived(self, argsList):
		if (AutologOpt.isLogTribalVillage()):
			iPlayer, pPlot, pUnit, iGoodyType = argsList
			if iPlayer == CyGame().getActivePlayer():
				GoodyTypeMap = {
						-1: BugUtil.getPlainText("TXT_KEY_AUTOLOG_VILLAGE_RESULT_NOTHING"),
						0:	BugUtil.getPlainText("TXT_KEY_AUTOLOG_VILLAGE_RESULT_LITTLEGOLD"),
						1:	BugUtil.getPlainText("TXT_KEY_AUTOLOG_VILLAGE_RESULT_LOTSOFGOLD"),
						2:	BugUtil.getPlainText("TXT_KEY_AUTOLOG_VILLAGE_RESULT_MAP"),
						3:	BugUtil.getPlainText("TXT_KEY_AUTOLOG_VILLAGE_RESULT_SETTLER"),
						4:	BugUtil.getPlainText("TXT_KEY_AUTOLOG_VILLAGE_RESULT_WARRIOR"),
						5:	BugUtil.getPlainText("TXT_KEY_AUTOLOG_VILLAGE_RESULT_SCOUT"),
						6:	BugUtil.getPlainText("TXT_KEY_AUTOLOG_VILLAGE_RESULT_WORKER"),
						7:	BugUtil.getPlainText("TXT_KEY_AUTOLOG_VILLAGE_RESULT_XP"),
						8:	BugUtil.getPlainText("TXT_KEY_AUTOLOG_VILLAGE_RESULT_HEALING"),
						9:	BugUtil.getPlainText("TXT_KEY_AUTOLOG_VILLAGE_RESULT_TECH"),
						10:	BugUtil.getPlainText("TXT_KEY_AUTOLOG_VILLAGE_RESULT_WEAKHOSTILES"),
						11: BugUtil.getPlainText("TXT_KEY_AUTOLOG_VILLAGE_RESULT_STRONGHOSTILES")
					}
				message = BugUtil.getText("TXT_KEY_AUTOLOG_VILLAGE_RESULT", (GoodyTypeMap[iGoodyType], ))
				Logger.writeLog(message, vColor="Brown")

	def onGreatPersonBorn(self, argsList):
		if (AutologOpt.isLogGreatPeople()):
			pUnit, iPlayer, pCity = argsList
			if iPlayer == CyGame().getActivePlayer():
				message = BugUtil.getText("TXT_KEY_AUTOLOG_GP_BORN", (pUnit.getName(), pCity.getName()))
				Logger.writeLog(message, vColor="Brown")

	def onTechAcquired(self, argsList):
		if gc.getGame().getGameTurn() == 0:
			return
		
		if (AutologOpt.isLogTechnology()):
			iTechType, iTeam, iPlayer, bAnnounce = argsList

			bWrite = False
			if iPlayer == CyGame().getActivePlayer():
				bWrite = True

				if self.bHumanEndTurn:
					message = BugUtil.getText("TXT_KEY_AUTOLOG_TECH_RESEARCHED", (PyInfo.TechnologyInfo(iTechType).getDescription(), ))
				else:
					message = BugUtil.getText("TXT_KEY_AUTOLOG_TECH_ACQUIRED", (PyInfo.TechnologyInfo(iTechType).getDescription(), ))
			else:
				if self.bHumanPlaying:
					bWrite = True
					zsCiv = gc.getPlayer(iPlayer).getName() + " (" + gc.getPlayer(iPlayer).getCivilizationShortDescription(0) + ")"
					message = BugUtil.getText("TXT_KEY_AUTOLOG_TECH_TRADED", (zsCiv, PyInfo.TechnologyInfo(iTechType).getDescription()))

			if bWrite:
				Logger.writeLog(message, vColor="Green")

	def onTechSelected(self, argsList):
		if (AutologOpt.isLogTechnology()):
			iTechType, iPlayer = argsList
			if iPlayer == CyGame().getActivePlayer():
				researchProgress = gc.getTeam(gc.getPlayer(iPlayer).getTeam()).getResearchProgress(gc.getPlayer(iPlayer).getCurrentResearch())
				overflowResearch = (gc.getPlayer(iPlayer).getOverflowResearch() * gc.getPlayer(iPlayer).calculateResearchModifier(gc.getPlayer(iPlayer).getCurrentResearch()))/100
				researchCost = gc.getTeam(gc.getPlayer(iPlayer).getTeam()).getResearchCost(gc.getPlayer(iPlayer).getCurrentResearch())
				researchRate = gc.getPlayer(iPlayer).calculateResearchRate(-1)
				zTurns = (researchCost - researchProgress - overflowResearch) / researchRate + 1
				message = BugUtil.getText("TXT_KEY_AUTOLOG_RESEARCH_BEGUN", (PyInfo.TechnologyInfo(iTechType).getDescription(), zTurns))
				Logger.writeLog(message, vColor="Green")

	def onReligionFounded(self, argsList):
		if (AutologOpt.isLogReligion()):
			iReligion, iFounder = argsList
			player = PyPlayer(iFounder)
			iCityId = gc.getGame().getHolyCity(iReligion).getID()
			if (player.getTeamID() == 0):
				messageEnd = gc.getPlayer(iFounder).getCity(iCityId).getName()
			else:
				messageEnd = BugUtil.getPlainText("TXT_KEY_AUTOLOG_DISTANT_LAND")
			message = BugUtil.getText("TXT_KEY_AUTOLOG_RELIGION_FOUNDED", (gc.getReligionInfo(iReligion).getDescription(), messageEnd))
			Logger.writeLog(message, vColor="DarkOrange")

	def onReligionSpread(self, argsList):
		if (AutologOpt.isLogReligion()):
			iReligion, iOwner, pSpreadCity = argsList
			player = PyPlayer(iOwner)

			if gc.getGame().getHolyCity(iReligion).getOwner() == CyGame().getActivePlayer() or pSpreadCity.getOwner() == CyGame().getActivePlayer():
				if (pSpreadCity.getOwner() == CyGame().getActivePlayer()):
					message = BugUtil.getText("TXT_KEY_AUTOLOG_RELIGION_SPREAD_IN", (gc.getReligionInfo(iReligion).getDescription(), pSpreadCity.getName()))
				else:
					message = BugUtil.getText("TXT_KEY_AUTOLOG_RELIGION_SPREAD_OUT", (gc.getReligionInfo(iReligion).getDescription(), pSpreadCity.getName(), player.getCivilizationName()))
				Logger.writeLog(message, vColor="DarkOrange")

	def onReligionRemove(self, argsList):
		if (AutologOpt.isLogReligion()):
			iReligion, iOwner, pRemoveCity = argsList
			player = PyPlayer(iOwner)

			if gc.getGame().getHolyCity(iReligion).getOwner() == CyGame().getActivePlayer() or pRemoveCity.getOwner() == CyGame().getActivePlayer():
				if (pRemoveCity.getOwner() == CyGame().getActivePlayer()):
					message = BugUtil.getText("TXT_KEY_AUTOLOG_RELIGION_REMOVED_IN", (gc.getReligionInfo(iReligion).getDescription(), pRemoveCity.getName()))
				else:
					message = BugUtil.getText("TXT_KEY_AUTOLOG_RELIGION_REMOVED_OUT", (gc.getReligionInfo(iReligion).getDescription(), pRemoveCity.getName(), player.getCivilizationName()))
				Logger.writeLog(message, vColor="DarkOrange")

	def onCorporationFounded(self, argsList):
		if (AutologOpt.isLogCorporation()):
			iCorporation, iFounder = argsList
			player = PyPlayer(iFounder)
			iCityId = gc.getGame().getHeadquarters(iCorporation).getID()
			if (player.getTeamID() == 0):
				messageEnd = gc.getPlayer(iFounder).getCity(iCityId).getName()
			else:
				messageEnd = BugUtil.getPlainText("TXT_KEY_AUTOLOG_DISTANT_LAND")
			message = BugUtil.getText("TXT_KEY_AUTOLOG_CORP_FOUNDED", (gc.getCorporationInfo(iCorporation).getDescription(), messageEnd))
			Logger.writeLog(message, vColor="DarkOrange")

	def onCorporationSpread(self, argsList):
		if (AutologOpt.isLogCorporation()):
			iCorporation, iOwner, pSpreadCity = argsList
			player = PyPlayer(iOwner)

			if gc.getGame().getHeadquarters(iCorporation).getOwner() == CyGame().getActivePlayer() or pSpreadCity.getOwner() == CyGame().getActivePlayer():
				if (pSpreadCity.getOwner() == CyGame().getActivePlayer()):
					message = BugUtil.getText("TXT_KEY_AUTOLOG_CORP_SPREAD_IN", (gc.getCorporationInfo(iCorporation).getDescription(), pSpreadCity.getName()))
				else:
					message = BugUtil.getText("TXT_KEY_AUTOLOG_CORP_SPREAD_OUT", (gc.getCorporationInfo(iCorporation).getDescription(), pSpreadCity.getName(), player.getCivilizationName()))
				Logger.writeLog(message, vColor="DarkOrange")

	def onCorporationRemove(self, argsList):
		if (AutologOpt.isLogCorporation()):
			iCorporation, iOwner, pRemoveCity = argsList
			player = PyPlayer(iOwner)

			if gc.getGame().getHeadquarters(iCorporation).getOwner() == CyGame().getActivePlayer() or pRemoveCity.getOwner() == CyGame().getActivePlayer():
				if (pRemoveCity.getOwner() == CyGame().getActivePlayer()):
					message = BugUtil.getText("TXT_KEY_AUTOLOG_CORP_REMOVED_IN", (gc.getCorporationInfo(iCorporation).getDescription(), pRemoveCity.getName()))
				else:
					message = BugUtil.getText("TXT_KEY_AUTOLOG_CORP_REMOVED_OUT", (gc.getCorporationInfo(iCorporation).getDescription(), pRemoveCity.getName(), player.getCivilizationName()))
				Logger.writeLog(message, vColor="DarkOrange")

	def onGoldenAge(self, argsList):
		if (AutologOpt.isLogGoldenAge()):
			iPlayer = argsList[0]
			if iPlayer == CyGame().getActivePlayer():
				message = BugUtil.getPlainText("TXT_KEY_AUTOLOG_GOLDENAGE_BEGINS")
				Logger.writeLog(message, vColor="Brown")

	def onEndGoldenAge(self, argsList):
		if (AutologOpt.isLogGoldenAge()):
			iPlayer = argsList[0]
			if iPlayer == CyGame().getActivePlayer():
				message = BugUtil.getPlainText("TXT_KEY_AUTOLOG_GOLDENAGE_ENDS")
				Logger.writeLog(message, vColor="Brown")

	def onChangeWar(self, argsList):
		bIsWar = argsList[0]
		iPlayer = argsList[1]
		iRivalTeam = argsList[2]

		if (gc.getGame().isFinalInitialized()
		and AutologOpt.isLogWar()):

#			Civ1 declares war on Civ2
			iCiv1 = iPlayer
			iCiv2 = gc.getTeam(iRivalTeam).getLeaderID()
			zsCiv1 = gc.getPlayer(iCiv1).getName() + " (" + gc.getPlayer(iCiv1).getCivilizationShortDescription(0) + ")"
			zsCiv2 = gc.getPlayer(iCiv2).getName() + " (" + gc.getPlayer(iCiv2).getCivilizationShortDescription(0) + ")"

			if (gc.getTeam(gc.getPlayer(iCiv1).getTeam()).isHasMet(gc.getActivePlayer().getTeam())
			and gc.getTeam(gc.getPlayer(iCiv2).getTeam()).isHasMet(gc.getActivePlayer().getTeam())):
				if (bIsWar):
					message = BugUtil.getText("TXT_KEY_AUTOLOG_DECLARES_WAR", (zsCiv1, zsCiv2))
					Logger.writeLog(message, vColor="Red")
				else:
					message = BugUtil.getText("TXT_KEY_AUTOLOG_PEACE_TREATY", (zsCiv1, zsCiv2))
					Logger.writeLog(message, vColor="DarkRed")

	def onSetPlayerAlive(self, argsList):
		if (AutologOpt.isLogWar()):
			iPlayerID = argsList[0]
			bNewValue = argsList[1]
			if not (bNewValue):
				if (gc.getTeam(gc.getPlayer(iPlayerID).getTeam()).isHasMet(gc.getActivePlayer().getTeam())):
					message = BugUtil.getText("TXT_KEY_AUTOLOG_CIV_ELIMINATED", (PyPlayer(iPlayerID).getCivDescription(), ))
				else:
					message = BugUtil.getPlainText("TXT_KEY_AUTOLOG_ANOTHER_CIV_ELIMINATED")

				Logger.writeLog(message, vColor="Red")

	def onCityBuilt(self, argsList):
		if (AutologOpt.isLogCityFounded()):
			pCity = argsList[0]
			if pCity.getOwner() == CyGame().getActivePlayer():
				message = BugUtil.getText("TXT_KEY_AUTOLOG_CITY_FOUNDED", (pCity.getName(), ))
				Logger.writeLog(message, vColor="RoyalBlue")

	def onCityRazed(self, argsList):
		if (AutologOpt.isLogCityRazed()):
			city, iPlayer = argsList
			owner = PyPlayer(city.getOwner())
			razor = PyPlayer(iPlayer)
			if (iPlayer == CyGame().getActivePlayer()):
				message = BugUtil.getText("TXT_KEY_AUTOLOG_CITY_RAZED", (city.getName(), ))
				Logger.writeLog(message, vColor="RoyalBlue")

			elif (city.getOwner() == CyGame().getActivePlayer()):
				message = BugUtil.getText("TXT_KEY_AUTOLOG_CITY_RAZED_BY", (city.getName(), razor.getCivilizationName()))
				Logger.writeLog(message, vColor="RoyalBlue")

	def onCityAcquired(self, argsList):
		if (AutologOpt.isLogCityOwner()):
			owner,playerType,pCity,bConquest,bTrade = argsList
			if pCity.getOwner() == CyGame().getActivePlayer():
				if (bConquest):
					message = BugUtil.getText("TXT_KEY_AUTOLOG_CITY_CAPTURED", (pCity.getName(), PyPlayer(owner).getName()))
				elif (bTrade): ## city trade not tested
					message = BugUtil.getText("TXT_KEY_AUTOLOG_CITY_TRADED", (pCity.getName(), PyPlayer(owner).getName()))
				else:
					message = BugUtil.getText("TXT_KEY_AUTOLOG_CITY_FLIPPED", (pCity.getName(), PyPlayer(owner).getName()))

				Logger.writeLog(message, vColor="RoyalBlue")

	def onCityLost(self, argsList):
		if (AutologOpt.isLogCityOwner()):
			pCity = argsList[0]
			if pCity.getOwner() == CyGame().getActivePlayer():
				message = BugUtil.getText("TXT_KEY_AUTOLOG_CITY_LOST", (pCity.getName(), ))
				Logger.writeLog(message, vColor="RoyalBlue")

	def onCultureExpansion(self, argsList):
		if (AutologOpt.isLogCityBorders()):
			pCity = argsList[0]
			iPlayer = argsList[1]
			if pCity.getOwner() == CyGame().getActivePlayer():
				message = BugUtil.getText("TXT_KEY_AUTOLOG_CITY_EXPANDED", (pCity.getName(), ))
				Logger.writeLog(message, vColor="RoyalBlue")

	def onCityGrowth(self, argsList):
		if (AutologOpt.isLogCityGrowth()):
			pCity = argsList[0]
			iPlayer = argsList[1]
			#CvUtil.pyPrint("%s has grown to size %i" %(pCity.getName(),pCity.getPopulation()))
			if pCity.getOwner() == CyGame().getActivePlayer():
				message = BugUtil.getText("TXT_KEY_AUTOLOG_CITY_GROWS", (pCity.getName(), pCity.getPopulation()))
				Logger.writeLog(message, vColor="RoyalBlue")

	def onCityBuildingUnit(self, argsList):
		if (AutologOpt.isLogBuildStarted()):
			pCity = argsList[0]
			iUnitType = argsList[1]
			if pCity.getOwner() == CyGame().getActivePlayer():
				zTurns = pCity.getUnitProductionTurnsLeft(iUnitType, 1)
				message = BugUtil.getText("TXT_KEY_AUTOLOG_CITY_PRODUCES_UNIT", (pCity.getName(),gc.getUnitInfo(iUnitType).getDescription(), zTurns))
				Logger.writeLog(message, vColor="Purple")

	def onCityBuildingBuilding(self, argsList):
		if (AutologOpt.isLogBuildStarted()):
			pCity = argsList[0]
			iBuildingType = argsList[1]
			if pCity.getOwner() == CyGame().getActivePlayer():
				zTurns = pCity.getBuildingProductionTurnsLeft(iBuildingType, 1)
				message = BugUtil.getText("TXT_KEY_AUTOLOG_CITY_PRODUCES_BUILDING", (pCity.getName(),gc.getBuildingInfo(iBuildingType).getDescription(), zTurns))
				Logger.writeLog(message, vColor="Purple")

	def onImprovementBuilt(self, argsList):
		'Improvement Built'
		iImprovement, iX, iY = argsList

		if iImprovement in (-1, gc.getInfoTypeForString("IMPROVEMENT_TRIBAL_VILLAGE"), gc.getInfoTypeForString("IMPROVEMENT_CITY_RUINS")):  
			return

		pPlot = CyMap().plot(iX,iY)

		if (AutologOpt.isLogImprovements()
		and pPlot.getOwner() == CyGame().getActivePlayer()):
			message = BugUtil.getText("TXT_KEY_AUTOLOG_IMPROVEMENT_BUILT", (PyInfo.ImprovementInfo(iImprovement).getDescription(), ))
			zsLocn = ""
			for iiX in range(iX-2, iX+3, 1):
				for iiY in range(iY-2, iY+3, 1):
					pPlot = CyMap().plot(iiX,iiY)
					if (pPlot.isCity()):
						zsCity = pPlot.getPlotCity()
						zsLocn = BugUtil.getText("TXT_KEY_AUTOLOG_NEAR", (zsCity.getName(), ))

			message = message + zsLocn
			Logger.writeLog(message, vColor="RoyalBlue")

	def onImprovementDestroyed(self, argsList):
		'Improvement Destroyed'
		iImprovement, iOwner, iX, iY = argsList

		if iImprovement in (-1, gc.getInfoTypeForString("IMPROVEMENT_TRIBAL_VILLAGE"), gc.getInfoTypeForString("IMPROVEMENT_CITY_RUINS")):  
			return

		pPlot = CyMap().plot(iX,iY)

		if (AutologOpt.isLogImprovements()
		and pPlot.getOwner() == CyGame().getActivePlayer()):
			message = BugUtil.getText("TXT_KEY_AUTOLOG_IMPROVEMENT_DESTROYED", (PyInfo.ImprovementInfo(iImprovement).getDescription(), ))
			zsLocn = ""
			for iiX in range(iX-2, iX+3, 1):
				for iiY in range(iY-2, iY+3, 1):
					pPlot = CyMap().plot(iiX,iiY)
					if (pPlot.isCity()):
						zsCity = pPlot.getPlotCity()
						zsLocn = BugUtil.getText("TXT_KEY_AUTOLOG_NEAR", (zsCity.getName(), ))

			message = message + zsLocn
			Logger.writeLog(message, vColor="RoyalBlue")

	def onUnitPillage(self, argsList):
		'Unit pillages a plot'
		pUnit, iImprovement, iRoute, iOwner, iGold = argsList
		iX = pUnit.getX()
		iY = pUnit.getY()
		pPlot = CyMap().plot(iX,iY)

		if (AutologOpt.isLogPillage()
		and (pPlot.getOwner() == CyGame().getActivePlayer()
		or   pUnit.getOwner() == CyGame().getActivePlayer())):
			if (iImprovement != -1):
				message = BugUtil.getText("TXT_KEY_AUTOLOG_IMPROVEMENT", (gc.getImprovementInfo(iImprovement).getDescription(), ))
			elif (iRoute != -1):
				message = BugUtil.getText("TXT_KEY_AUTOLOG_ROUTE", (gc.getRouteInfo(iRoute).getDescription(), ))
			else:
				message = BugUtil.getPlainText("TXT_KEY_AUTOLOG_IMPROVEMENT_UNKNOWN")
			zsLocn = ""
			for iiX in range(iX-2, iX+3, 1):
				for iiY in range(iY-2, iY+3, 1):
					pPlot = CyMap().plot(iiX,iiY)
					if (pPlot.isCity()):
						zsCity = pPlot.getPlotCity()
						zsLocn = BugUtil.getText("TXT_KEY_AUTOLOG_NEAR", (zsCity.getName(), ))

			message = message + zsLocn

			global iLastPillageGold
			if (iLastPillageGold is None or not self.bHumanPlaying):
				message = message + BugUtil.getText("TXT_KEY_AUTOLOG_IMPROVEMENT_DESTROYED_BY_NOGOLD", (PyPlayer(iOwner).getCivilizationAdjective(), pUnit.getName()))
			else:
				message = message + BugUtil.getText("TXT_KEY_AUTOLOG_IMPROVEMENT_DESTROYED_BY_GOLD", (PyPlayer(iOwner).getCivilizationAdjective(), pUnit.getName(), iLastPillageGold))
			iLastPillageGold = None

			if self.bHumanPlaying:
				Logger.writeLog(message, vColor="DarkRed")
			else:
				Logger.writeLog(message, vColor="Red")

	def onVassalState(self, argsList):
		'Vassal State'
		iMaster, iVassal, bVassal, bCapitulated = argsList
		
		if (AutologOpt.isLogVassals()
		and gc.getTeam(iMaster).isHasMet(gc.getActivePlayer().getTeam())
		and gc.getTeam(iVassal).isHasMet(gc.getActivePlayer().getTeam())):

			zsMaster = gc.getTeam(iMaster).getName()
			zsVassal = gc.getTeam(iVassal).getName()

			if (bVassal):
				message = BugUtil.getText("TXT_KEY_AUTOLOG_VASSAL_BECOMES", (zsVassal, zsMaster))
			else:
				message = BugUtil.getText("TXT_KEY_AUTOLOG_VASSAL_REVOLTS", (zsVassal, zsMaster))

			Logger.writeLog(message, vColor="Red")

	def onDealOffered(self, argsList):
		eOfferPlayer, eTargetPlayer, pTrade = argsList
		if AutologOpt.isLogTradeOffer():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pOfferPlayer = gc.getPlayer(eOfferPlayer)
			szOfferItems = ""
			szTargetItems = ""
			message = ""
			if eOfferPlayer == pTrade.getPlayer():
				for i in range(pTrade.getCount()):
					szOfferItems = szOfferItems + TradeUtil.format(eOfferPlayer, pTrade.getTrade(i)) + ", "
				for i in range(pTrade.getOtherCount()):
					szTargetItems = szTargetItems + TradeUtil.format(eTargetPlayer, pTrade.getOtherTrade(i)) + ", "
			else:
				for i in range(pTrade.getOtherCount()):
					szOfferItems = szOfferItems + TradeUtil.format(eOfferPlayer, pTrade.getOtherTrade(i)) + ", "
				for i in range(pTrade.getCount()):
					szTargetItems = szTargetItems + TradeUtil.format(eTargetPlayer, pTrade.getTrade(i)) + ", "
			szOfferItems = szOfferItems.rstrip(", ")
			szTargetItems = szTargetItems.rstrip(", ")
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_DEAL_OFFER", 
									(pOfferPlayer.getName(), pOfferPlayer.getCivilizationShortDescription(0),
									szOfferItems,
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									szTargetItems))
			Logger.writeLog(message, vColor="Navy")
	
	def onCityOffered(self, argsList):
		eOfferPlayer, eTargetPlayer, iCityID = argsList
		if AutologOpt.isLogTradeOffer():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pOfferPlayer = gc.getPlayer(eOfferPlayer)
			pCityOffered = pOfferPlayer.getCity(iCityID)
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_CITY_OFFER", 
									(pOfferPlayer.getName(), pOfferPlayer.getCivilizationShortDescription(0),
									pCityOffered.getName(),
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0)))
			Logger.writeLog(message, vColor="Navy")
	
	def onHelpOffered(self, argsList):
		eOfferPlayer, eTargetPlayer, pTrade = argsList
		if AutologOpt.isLogTradeOffer():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pOfferPlayer = gc.getPlayer(eOfferPlayer)
			szOfferItems = ""
			message = ""
			if eOfferPlayer == pTrade.getPlayer():
				for i in range(pTrade.getCount()):
					szOfferItems = szOfferItems + TradeUtil.format(eOfferPlayer, pTrade.getTrade(i)) + ", "
			else:
				for i in range(pTrade.getOtherCount()):
					szOfferItems = szOfferItems + TradeUtil.format(eOfferPlayer, pTrade.getOtherTrade(i)) + ", "
			szOfferItems = szOfferItems.rstrip(", ")
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_HELP_OFFER", 
									(pOfferPlayer.getName(), pOfferPlayer.getCivilizationShortDescription(0),
									szOfferItems,
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0)))
			Logger.writeLog(message, vColor="Navy")
	
	def onPeaceOffered(self, argsList):
		eOfferPlayer, eTargetPlayer = argsList
		if AutologOpt.isLogTradeOffer():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pOfferPlayer = gc.getPlayer(eOfferPlayer)
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_PEACE_OFFER", 
									(pOfferPlayer.getName(), pOfferPlayer.getCivilizationShortDescription(0),
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0)))
			Logger.writeLog(message, vColor="Navy")
	
	def onVassalOffered(self, argsList):
		eOfferPlayer, eTargetPlayer = argsList
		if AutologOpt.isLogTradeOffer():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pOfferPlayer = gc.getPlayer(eOfferPlayer)
			message = ""
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_VASSAL_OFFER", 
									(pOfferPlayer.getName(), pOfferPlayer.getCivilizationShortDescription(0),
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0)))
			Logger.writeLog(message, vColor="Navy")
	
	def onDealCanceled(self, argsList):
		eOfferPlayer, eTargetPlayer, pTrade = argsList
		if AutologOpt.isLogTradeOffer() and pTrade != None:
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pOfferPlayer = gc.getPlayer(eOfferPlayer)
			szOfferItems = ""
			szTargetItems = ""
			message = ""
			if eOfferPlayer == pTrade.getPlayer():
				for i in range(pTrade.getCount()):
					szOfferItems = szOfferItems + TradeUtil.format(eOfferPlayer, pTrade.getTrade(i)) + ", "
				for i in range(pTrade.getOtherCount()):
					szTargetItems = szTargetItems + TradeUtil.format(eTargetPlayer, pTrade.getOtherTrade(i)) + ", "
			else:
				for i in range(pTrade.getOtherCount()):
					szOfferItems = szOfferItems + TradeUtil.format(eOfferPlayer, pTrade.getOtherTrade(i)) + ", "
				for i in range(pTrade.getCount()):
					szTargetItems = szTargetItems + TradeUtil.format(eTargetPlayer, pTrade.getTrade(i)) + ", "
			szOfferItems = szOfferItems.rstrip(", ")
			szTargetItems = szTargetItems.rstrip(", ")
			if szTargetItems:
				message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_DEAL_CANCEL", 
										(pOfferPlayer.getName(), pOfferPlayer.getCivilizationShortDescription(0),
										szOfferItems,
										pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
										szTargetItems))
			else:
				message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_GIFT_CANCEL", 
										(pOfferPlayer.getName(), pOfferPlayer.getCivilizationShortDescription(0),
										szOfferItems,
										pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0)))
			Logger.writeLog(message, vColor="Red")
	
	def onDealAccepted(self, argsList):
		eTargetPlayer, eOfferPlayer, pTrade = argsList
		if AutologOpt.isLogTradeOffer():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pOfferPlayer = gc.getPlayer(eOfferPlayer)
			szOfferItems = ""
			szTargetItems = ""
			message = ""
			if eOfferPlayer == pTrade.getPlayer():
				for i in range(pTrade.getCount()):
					szOfferItems = szOfferItems + TradeUtil.format(eOfferPlayer, pTrade.getTrade(i)) + ", "
				for i in range(pTrade.getOtherCount()):
					szTargetItems = szTargetItems + TradeUtil.format(eTargetPlayer, pTrade.getOtherTrade(i)) + ", "
			else:
				for i in range(pTrade.getOtherCount()):
					szOfferItems = szOfferItems + TradeUtil.format(eOfferPlayer, pTrade.getOtherTrade(i)) + ", "
				for i in range(pTrade.getCount()):
					szTargetItems = szTargetItems + TradeUtil.format(eTargetPlayer, pTrade.getTrade(i)) + ", "
			szOfferItems = szOfferItems.rstrip(", ")
			szTargetItems = szTargetItems.rstrip(", ")
			if szTargetItems:
				message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_DEAL_ACCEPT", 
										(pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
										szTargetItems,
										pOfferPlayer.getName(), pOfferPlayer.getCivilizationShortDescription(0),
										szOfferItems))
			else:
				message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_GIFT_ACCEPT", 
										(pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
										szOfferItems,
										pOfferPlayer.getName(), pOfferPlayer.getCivilizationShortDescription(0)))
			Logger.writeLog(message, vColor="Green")
	
	def onDealRejected(self, argsList):
		eTargetPlayer, eOfferPlayer, pTrade = argsList
		if AutologOpt.isLogTradeOffer():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pOfferPlayer = gc.getPlayer(eOfferPlayer)
			szOfferItems = ""
			szTargetItems = ""
			message = ""
			if eOfferPlayer == pTrade.getPlayer():
				for i in range(pTrade.getCount()):
					szOfferItems = szOfferItems + TradeUtil.format(eOfferPlayer, pTrade.getTrade(i)) + ", "
				for i in range(pTrade.getOtherCount()):
					szTargetItems = szTargetItems + TradeUtil.format(eTargetPlayer, pTrade.getOtherTrade(i)) + ", "
			else:
				for i in range(pTrade.getOtherCount()):
					szOfferItems = szOfferItems + TradeUtil.format(eOfferPlayer, pTrade.getOtherTrade(i)) + ", "
				for i in range(pTrade.getCount()):
					szTargetItems = szTargetItems + TradeUtil.format(eTargetPlayer, pTrade.getTrade(i)) + ", "
			szOfferItems = szOfferItems.rstrip(", ")
			szTargetItems = szTargetItems.rstrip(", ")
			if szTargetItems:
				message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_DEAL_REJECT", 
										(pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
										szTargetItems,
										pOfferPlayer.getName(), pOfferPlayer.getCivilizationShortDescription(0),
										szOfferItems))
			else:
				message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_GIFT_REJECT", 
										(pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
										szOfferItems,
										pOfferPlayer.getName(), pOfferPlayer.getCivilizationShortDescription(0)))
			Logger.writeLog(message, vColor="Red")
	
	def onHelpDemanded(self, argsList):
		eDemandPlayer, eTargetPlayer, pTrade = argsList
		if AutologOpt.isLogTributeDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			szItems = ""
			message = ""
			for i in range(pTrade.getCount()):
				szItems = szItems + TradeUtil.format(eTargetPlayer, pTrade.getTrade(i)) + ", "
			szItems = szItems.rstrip(", ")
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_HELP_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									szItems))
			Logger.writeLog(message, vColor="Navy")
	
	def onHelpAccepted(self, argsList):
		eTargetPlayer, eDemandPlayer, pTrade = argsList
		if AutologOpt.isLogTributeDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			szItems = ""
			message = ""
			for i in range(pTrade.getCount()):
				szItems = szItems + TradeUtil.format(eTargetPlayer, pTrade.getTrade(i)) + ", "
			szItems = szItems.rstrip(", ")
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_HELP_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									szItems))
			message = message + BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_GENERIC_ACCEPT", (pTargetPlayer.getName(),))
			Logger.writeLog(message, vColor="Green")
	
	def onHelpRejected(self, argsList):
		eTargetPlayer, eDemandPlayer, pTrade = argsList
		if AutologOpt.isLogTributeDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			szItems = ""
			message = ""
			for i in range(pTrade.getCount()):
				szItems = szItems + TradeUtil.format(eTargetPlayer, pTrade.getTrade(i)) + ", "
			szItems = szItems.rstrip(", ")
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_HELP_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									szItems))
			message = message + BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_GENERIC_REJECT", (pTargetPlayer.getName(),))
			Logger.writeLog(message, vColor="Red")
	
	def onTributeDemanded(self, argsList):
		eDemandPlayer, eTargetPlayer, pTrade = argsList
		if AutologOpt.isLogTributeDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			szItems = ""
			message = ""
			for i in range(pTrade.getCount()):
				szItems = szItems + TradeUtil.format(eTargetPlayer, pTrade.getTrade(i)) + ", "
			szItems = szItems.rstrip(", ")
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_TRIBUTE_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									szItems))
			Logger.writeLog(message, vColor="Navy")
	
	def onTributeAccepted(self, argsList):
		eTargetPlayer, eDemandPlayer, pTrade = argsList
		if AutologOpt.isLogTributeDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			szItems = ""
			message = ""
			for i in range(pTrade.getCount()):
				szItems = szItems + TradeUtil.format(eTargetPlayer, pTrade.getTrade(i)) + ", "
			szItems = szItems.rstrip(", ")
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_TRIBUTE_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									szItems))
			message = message + BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_GENERIC_ACCEPT", (pTargetPlayer.getName(),))
			Logger.writeLog(message, vColor="Green")
	
	def onTributeRejected(self, argsList):
		eTargetPlayer, eDemandPlayer, pTrade = argsList
		if AutologOpt.isLogTributeDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			szItems = ""
			message = ""
			for i in range(pTrade.getCount()):
				szItems = szItems + TradeUtil.format(eTargetPlayer, pTrade.getTrade(i)) + ", "
			szItems = szItems.rstrip(", ")
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_TRIBUTE_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									szItems))
			message = message + BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_GENERIC_REJECT", (pTargetPlayer.getName(),))
			Logger.writeLog(message, vColor="Red")

	def onReligionDemanded(self, argsList):
		eDemandPlayer, eTargetPlayer, eReligion = argsList
		if AutologOpt.isLogReligionDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_RELIGION_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									gc.getReligionInfo(eReligion).getDescription()))
			Logger.writeLog(message, vColor="Navy")
	
	def onReligionAccepted(self, argsList):
		eTargetPlayer, eDemandPlayer, eReligion = argsList
		if AutologOpt.isLogReligionDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_RELIGION_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									gc.getReligionInfo(eReligion).getDescription()))
			message = message + BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_GENERIC_ACCEPT", (pTargetPlayer.getName(),))
			Logger.writeLog(message, vColor="Green")
	
	def onReligionRejected(self, argsList):
		eTargetPlayer, eDemandPlayer, eReligion = argsList
		if AutologOpt.isLogReligionDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_RELIGION_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									gc.getReligionInfo(eReligion).getDescription()))
			message = message + BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_GENERIC_REJECT", (pTargetPlayer.getName(),))
			Logger.writeLog(message, vColor="Red")

	def onCivicDemanded(self, argsList):
		eDemandPlayer, eTargetPlayer, eCivic = argsList
		if AutologOpt.isLogCivicDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_CIVIC_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									gc.getCivicInfo(eCivic).getDescription()))
			Logger.writeLog(message, vColor="Navy")
	
	def onCivicAccepted(self, argsList):
		eTargetPlayer, eDemandPlayer, eCivic = argsList
		if AutologOpt.isLogCivicDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_CIVIC_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									gc.getCivicInfo(eCivic).getDescription()))
			message = message + BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_GENERIC_ACCEPT", (pTargetPlayer.getName(),))
			Logger.writeLog(message, vColor="Green")
	
	def onCivicRejected(self, argsList):
		eTargetPlayer, eDemandPlayer, eCivic = argsList
		if AutologOpt.isLogCivicDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_CIVIC_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									gc.getCivicInfo(eCivic).getDescription()))
			message = message + BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_GENERIC_REJECT", (pTargetPlayer.getName(),))
			Logger.writeLog(message, vColor="Red")

	def onWarDemanded(self, argsList):
		eDemandPlayer, eTargetPlayer, eVictim = argsList
		if AutologOpt.isLogWarDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			pVictim = gc.getPlayer(eVictim)
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_WAR_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									pVictim.getName(), pVictim.getCivilizationShortDescription(0)))
			Logger.writeLog(message, vColor="Navy")
	
	def onWarAccepted(self, argsList):
		eTargetPlayer, eDemandPlayer, eVictim = argsList
		if AutologOpt.isLogWarDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			pVictim = gc.getPlayer(eVictim)
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_WAR_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									pVictim.getName(), pVictim.getCivilizationShortDescription(0)))
			message = message + BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_GENERIC_ACCEPT", (pTargetPlayer.getName(),))
			Logger.writeLog(message, vColor="Green")
	
	def onWarRejected(self, argsList):
		eTargetPlayer, eDemandPlayer, eVictim = argsList
		if AutologOpt.isLogWarDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			pVictim = gc.getPlayer(eVictim)
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_WAR_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									pVictim.getName(), pVictim.getCivilizationShortDescription(0)))
			message = message + BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_GENERIC_REJECT", (pTargetPlayer.getName(),))
			Logger.writeLog(message, vColor="Red")

	def onEmbargoDemanded(self, argsList):
		eDemandPlayer, eTargetPlayer, eVictim = argsList
		if AutologOpt.isLogEmbargoDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			pVictim = gc.getPlayer(eVictim)
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_EMBARGO_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									pVictim.getName(), pVictim.getCivilizationShortDescription(0)))
			Logger.writeLog(message, vColor="Navy")
	
	def onEmbargoAccepted(self, argsList):
		eTargetPlayer, eDemandPlayer, eVictim = argsList
		if AutologOpt.isLogEmbargoDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			pVictim = gc.getPlayer(eVictim)
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_EMBARGO_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									pVictim.getName(), pVictim.getCivilizationShortDescription(0)))
			message = message + BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_GENERIC_ACCEPT", (pTargetPlayer.getName(),))
			Logger.writeLog(message, vColor="Green")
	
	def onEmbargoRejected(self, argsList):
		eTargetPlayer, eDemandPlayer, eVictim = argsList
		if AutologOpt.isLogEmbargoDemand():
			pTargetPlayer = gc.getPlayer(eTargetPlayer)
			pDemandPlayer = gc.getPlayer(eDemandPlayer)
			pVictim = gc.getPlayer(eVictim)
			message = BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_EMBARGO_DEMAND", 
									(pDemandPlayer.getName(), pDemandPlayer.getCivilizationShortDescription(0), 
									pTargetPlayer.getName(), pTargetPlayer.getCivilizationShortDescription(0),
									pVictim.getName(), pVictim.getCivilizationShortDescription(0)))
			message = message + BugUtil.getText("TXT_KEY_AUTOLOG_DIPLO_GENERIC_REJECT", (pTargetPlayer.getName(),))
			Logger.writeLog(message, vColor="Red")

	def initStuff(self):
		#set up variables to hold stuff
		ziMaxCiv = gc.getGame().countCivPlayersEverAlive()

		self.CIVAttitude = [""] * ziMaxCiv * ziMaxCiv
		self.CIVCivics = [0] * ziMaxCiv * 5
		self.CIVReligion = [-1] * ziMaxCiv
		self.CityWhipCounter = [0] * 1000
		self.CityConscriptCounter = [0] * 1000

	def storeStuff(self):
		ziMaxCiv = gc.getGame().countCivPlayersEverAlive()
		if (not self.CIVReligion):
			self.initStuff()

		# store civ state religion
		for iCiv in range(0, ziMaxCiv, 1):
			self.CIVReligion[iCiv] = gc.getPlayer(iCiv).getStateReligion()

		# store civ attitudes
		for iCiv1 in range(0, ziMaxCiv, 1):
			for iCiv2 in range(0, ziMaxCiv, 1):
				# Don't try to get a civ's attitude with itself
				if iCiv1 == iCiv2:
					continue
				zKey = ziMaxCiv * iCiv1 + iCiv2
				self.CIVAttitude[zKey] = gc.getAttitudeInfo(gc.getPlayer(iCiv1).AI_getAttitude(iCiv2)).getDescription()

		# store the civ's civics
		for iCiv in range(0, ziMaxCiv, 1):
			if PyPlayer(iCiv).isAlive():
				for iCivic in range(0, 5, 1):
					zKey = 5 * iCiv + iCivic
					self.CIVCivics[zKey] = gc.getPlayer(iCiv).getCivics(iCivic)

		return 0

	def storeWhip(self):
		# store the city whip counter
		iPlayer = gc.getActivePlayer()
		for i in range(0, iPlayer.getNumCities(), 1):
			iCity = iPlayer.getCity(i)
			self.CityWhipCounter[i] = iCity.getHurryAngerTimer()
			self.CityConscriptCounter[i] = iCity.getConscriptAngerTimer()

	def checkStuff(self):
		ziMaxCiv = gc.getGame().countCivPlayersEverAlive()
		if (not self.CIVReligion):
			self.storeStuff()

		# check if civ state religion has changed
		if (AutologOpt.isLogReligion()):
			for iCiv in range(0, ziMaxCiv, 1):
				if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasMet(gc.getActivePlayer().getTeam())
				and self.CIVReligion[iCiv] != gc.getPlayer(iCiv).getStateReligion()
				and PyPlayer(iCiv).isAlive()):
					zsCiv = gc.getPlayer(iCiv).getName() + " (" + gc.getPlayer(iCiv).getCivilizationShortDescription(0) + ")"
					if self.CIVReligion[iCiv] == -1:
						zsOldRel = BugUtil.getPlainText("TXT_KEY_AUTOLOG_NO_STATE_RELIGION")
					else:
						zsOldRel = gc.getReligionInfo(self.CIVReligion[iCiv]).getDescription()
					if gc.getPlayer(iCiv).getStateReligion() == -1:
						zsNewRel = BugUtil.getPlainText("TXT_KEY_AUTOLOG_NO_STATE_RELIGION")
					else:
						zsNewRel = gc.getReligionInfo(gc.getPlayer(iCiv).getStateReligion()).getDescription()
					message = BugUtil.getText("TXT_KEY_AUTOLOG_RELIGION_CHANGE", (zsCiv, zsOldRel, zsNewRel))
					Logger.writeLog(message, vColor="DarkOrange")

		# check if the attitude has changed
		if (AutologOpt.isLogAttitude()):
			for iCiv1 in range(0, ziMaxCiv, 1):
				for iCiv2 in range(0, ziMaxCiv, 1):
					# Don't try to get a civ's attitude with itself
					if iCiv1 == iCiv2:
						continue
					zKey = ziMaxCiv * iCiv1 + iCiv2
					zsNewAttitude = gc.getAttitudeInfo(gc.getPlayer(iCiv1).AI_getAttitude(iCiv2)).getDescription()

					if (gc.getTeam(gc.getPlayer(iCiv1).getTeam()).isHasMet(gc.getActivePlayer().getTeam())
					and gc.getTeam(gc.getPlayer(iCiv2).getTeam()).isHasMet(gc.getActivePlayer().getTeam())
					and self.CIVAttitude[zKey] != zsNewAttitude
					and iCiv1 != gc.getGame().getActivePlayer()
					and PyPlayer(iCiv1).isAlive()
					and PyPlayer(iCiv2).isAlive()):
						zsCiv1 = gc.getPlayer(iCiv1).getName() + " (" + gc.getPlayer(iCiv1).getCivilizationShortDescription(0) + ")"
						zsCiv2 = gc.getPlayer(iCiv2).getName() + " (" + gc.getPlayer(iCiv2).getCivilizationShortDescription(0) + ")"
						message = BugUtil.getText("TXT_KEY_AUTOLOG_ATTITUDE_CHANGE", (zsCiv1, zsCiv2, self.CIVAttitude[zKey], zsNewAttitude))
						Logger.writeLog(message, vColor="Blue")

		# check if the civ's civics have changed
		if (AutologOpt.isLogCivics()):
			for iCiv in range(0, ziMaxCiv, 1):
				zsCiv = gc.getPlayer(iCiv).getName() + "(" + gc.getPlayer(iCiv).getCivilizationShortDescription(0) + ")"
				if (PyPlayer(iCiv).isAlive()
				and gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasMet(gc.getActivePlayer().getTeam())):
					for iCivic in range(0, 5, 1):
						zKey = 5 * iCiv + iCivic
						if (self.CIVCivics[zKey] != gc.getPlayer(iCiv).getCivics(iCivic)):
							zsOldCiv = gc.getCivicInfo(self.CIVCivics[zKey]).getDescription()
							zsNewCiv = gc.getCivicInfo(gc.getPlayer(iCiv).getCivics(iCivic)).getDescription()
							message = BugUtil.getText("TXT_KEY_AUTOLOG_CIVIC_CHANGE", (zsCiv, zsOldCiv, zsNewCiv))
							Logger.writeLog(message, vColor="SeaGreen")
		return 0

	def dumpStuff(self):
		ziMaxCiv = gc.getGame().countCivPlayersEverAlive()
		if (not self.CIVReligion):
			self.storeStuff()
		
		Logger.writeLog("")
		Logger.writeLog("dumpStuff")
		Logger.writeLog("state religion")

		# dump civ state religion
		for iCiv in range(0, ziMaxCiv, 1):
			zsCiv = gc.getPlayer(iCiv).getCivilizationShortDescription(0)
			message = "zsCiv %s, %i, %i" % (zsCiv, self.CIVReligion[iCiv], gc.getPlayer(iCiv).getStateReligion())
			Logger.writeLog(message)

		Logger.writeLog("")
		Logger.writeLog("attitude")

		# dump attitude
		for iCiv1 in range(0, ziMaxCiv, 1):
			for iCiv2 in range(0, ziMaxCiv, 1):
				# Don't try to get a civ's attitude with itself
				if iCiv1 == iCiv2:
					continue
				zsCiv1 = gc.getPlayer(iCiv1).getCivilizationAdjective(0)  #getCivilizationShortDescription(0)
				zsCiv2 = gc.getPlayer(iCiv2).getCivilizationAdjective(0)  #getCivilizationShortDescription(0)
				zsNewAttitude = gc.getAttitudeInfo(gc.getPlayer(iCiv1).AI_getAttitude(iCiv2)).getDescription()
				zKey = ziMaxCiv * iCiv1 + iCiv2
				message = "Attitude, %s, %s, %s, %s" % (zsCiv1, zsCiv2, self.CIVAttitude[zKey], zsNewAttitude)
				Logger.writeLog(message)

		Logger.writeLog("")
		Logger.writeLog("civics")

		# dump civ's civics
		for iCiv in range(0, ziMaxCiv, 1):
			zsCiv = gc.getPlayer(iCiv).getCivilizationShortDescription(0)
			for iCivic in range(0, 5, 1):
				zKey = 5 * iCiv + iCivic
				zsOldCiv = gc.getCivicInfo(self.CIVCivics[zKey]).getDescription()
				zsNewCiv = gc.getCivicInfo(gc.getPlayer(iCiv).getCivics(iCivic)).getDescription()
				message = "Civics, %s, %s, %s" % (zsCiv, zsOldCiv, zsNewCiv)
				Logger.writeLog(message)

		Logger.writeLog("")
		Logger.writeLog("City Whip Counter")

		# dump the city whip counter
		iPlayer = gc.getActivePlayer()
		for i in range(0, iPlayer.getNumCities(), 1):
			iCity = iPlayer.getCity(i)
			message = "Whip Counter, %s, %s, %s" % (iCity.getName(), self.CityWhipCounter[i], iCity.getHurryAngerTimer())
			Logger.writeLog(message)

		Logger.writeLog("")

		return 0

	def logSliders(self):
		if not AutologOpt.isLogSliders():
			return

		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		for iI in range( CommerceTypes.NUM_COMMERCE_TYPES ):
			eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES

			zDesc = gc.getCommerceInfo(CommerceTypes(eCommerce)).getDescription()
			if (eCommerce == CommerceTypes.COMMERCE_GOLD):
				zPercent = pPlayer.getCommercePercent(eCommerce)
				zRate = pPlayer.calculateGoldRate()
				zTotal = pPlayer.getGold()

				message = BugUtil.getText("TXT_KEY_AUTOLOG_COMMERCE_GOLD_SLIDERS", (zPercent, zDesc, zRate, zTotal))
				Logger.writeLog(message, vColor="Blue")
			else:
				if pPlayer.isCommerceFlexible(eCommerce):
					zPercent = pPlayer.getCommercePercent(eCommerce)
					zRate = pPlayer.getCommerceRate(CommerceTypes(eCommerce))
					zTotal = pPlayer.getGold()

					message = BugUtil.getText("TXT_KEY_AUTOLOG_COMMERCE_OTHER_SLIDERS", (zPercent, zDesc, zRate))
					Logger.writeLog(message, vColor="Blue")

		return
