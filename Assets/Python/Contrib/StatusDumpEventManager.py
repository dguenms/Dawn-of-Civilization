## Ruff StatusDump

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import autolog
import time
import BugCore
import BugUtil
import CvModName
import TradeUtil
import string
import BugFile

import BugUtil

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

BugAutolog = BugCore.game.Autolog
lPercent = "%"

class StatusDumpEventManager:

	def __init__(self, eventManager):

		StatusDumpEvent(eventManager)

		global sDump
		sDump = BugFile.BugFileInstance(bHoldOpen=True)

class AbstractStatusDumpEvent(object):

	def __init__(self, eventManager, *args, **kwargs):
		super(AbstractStatusDumpEvent, self).__init__(*args, **kwargs)

class StatusDumpEvent(AbstractStatusDumpEvent):

	def __init__(self, eventManager, *args, **kwargs):
		super(StatusDumpEvent, self).__init__(eventManager, *args, **kwargs)

		eventManager.addEventHandler("kbdEvent", self.onKbdEvent)
		self.eventMgr = eventManager

		BugUtil.debug("StatusDump-Start-0")

	def onKbdEvent(self, argsList):
		eventType,key,mx,my,px,py = argsList

#		BugUtil.debug("StatusDump-Start-1")

		if (eventType == self.eventMgr.EventKeyDown
		and int(key) == int(InputTypes.KB_D)
		and self.eventMgr.bCtrl
		and self.eventMgr.bAlt):
			BugUtil.debug("StatusDump-Start-2")
			self.DumpStatus()

			return 1

	def DumpStatus(self):

		BugUtil.debug("StatusDump")

		# open the status dump file
		self.StatusDump_OpenFile()

		# Year
		zyear = self._getGameYear()
		zsTurn = self._getGameTurn()
		zCurrDateTime = time.strftime("%d-%b-%Y %H:%M:%S")

		sMsg = BugUtil.getText("TXT_KEY_STATUS_DUMP_TURN", (zsTurn, zyear, zCurrDateTime))
		self._writeMsg(sMsg, vColor="Black", vBold=False, vUnderline=True, vOpenSpoiler=sMsg, vCloseSpoiler=False)

		# basic leader information
		self.StatusDump_Basic()

		# tech, culture, espionage, gold per turn info
		self.StatusDump_Spinners()

		# loop over each city
		self.StatusDump_Player_Cities()

		# loop over each unit
		self.StatusDump_Player_Units()

		# tech, culture, espionage, gold per turn info
		self.StatusDump_AIs()

		self._writeMsg(" ", vColor="Black", vBold=False, vUnderline=False, vOpenSpoiler="", vCloseSpoiler=True)

		self.StatusDump_CloseFile()





	def StatusDump_OpenFile(self):

		BugUtil.debug("StatusDump - openfile")

		sDump.setFileName(self._getFileName())
		sDump.openFile(bForce=True, sWrite='w')

		return

	def StatusDump_CloseFile(self):

		BugUtil.debug("StatusDump - closefile")

		sDump.closeFile(bForce=True)
		return




	def StatusDump_Basic(self):

		BugUtil.debug("StatusDump - basic")

		# dump basic stuff
		# - leader name / civ
		# - current game turn and year
		# - current tech being researched
		# - techs available to research
		# - opponents
		# - scoreboard
		# - number of cities
		# - bank balance

		# player stuff
		ePlayer = gc.getGame().getActivePlayer()
		pPlayer = gc.getPlayer(ePlayer)

		# human / game name
		sMsg = BugUtil.getText("TXT_KEY_STATUS_DUMP_PLAYER_NAME", (pPlayer.getName()))
		self._writeMsg(sMsg, vColor="Black", vBold=False, vUnderline=False, vOpenSpoiler="", vCloseSpoiler=False)

		# leader / civ name
		sMsg = BugUtil.getText("TXT_KEY_STATUS_DUMP_LEADER_CIV", (gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getDescription(), pPlayer.getCivilizationShortDescription(0)))
		self._writeMsg(sMsg, vColor="Black", vBold=False, vUnderline=False, vOpenSpoiler="", vCloseSpoiler=False)





	def StatusDump_Spinners(self):
		# dump spinner stuff
		# - current slider settings (beakes, culture, espionage, gold)
		# - tech rates (0% to 100% in steps of 10%) - show beakers and gold
		# - culture rates (0% to 100% in steps of 10%) - show culture and gold
		# - espionage rates (0% to 100% in steps of 10%) - show espionage and gold

		sMsg = "Spinner stuff here"
		self._writeMsg(sMsg, vColor="Black", vBold=False, vUnderline=False, vOpenSpoiler="Spinners", vCloseSpoiler=False)
		self._writeMsg(" ", vColor="Black", vBold=False, vUnderline=False, vOpenSpoiler="", vCloseSpoiler=True)

	def StatusDump_Player_Cities(self):
		sMsg = "Player Cities here"
		self._writeMsg(sMsg, vColor="Black", vBold=False, vUnderline=False, vOpenSpoiler=sMsg, vCloseSpoiler=False)
		self._writeMsg(" ", vColor="Black", vBold=False, vUnderline=False, vOpenSpoiler="", vCloseSpoiler=True)

	def StatusDump_Player_Units(self):
		sMsg = "Player Units stuff here"
		self._writeMsg(sMsg, vColor="Black", vBold=False, vUnderline=False, vOpenSpoiler=sMsg, vCloseSpoiler=False)
		self._writeMsg(" ", vColor="Black", vBold=False, vUnderline=False, vOpenSpoiler="", vCloseSpoiler=True)

	def StatusDump_AIs(self):
		sMsg = "AIs stuff here"
		self._writeMsg(sMsg, vColor="Black", vBold=False, vUnderline=False, vOpenSpoiler=sMsg, vCloseSpoiler=False)
		self._writeMsg(" ", vColor="Black", vBold=False, vUnderline=False, vOpenSpoiler="", vCloseSpoiler=True)


























	def _getGameYear(self):
		zturn = gc.getGame().getGameTurn() + 1
		zyear = gc.getGame().getTurnYear(zturn)
		if (zyear < 0):
			return str(-zyear) + BugUtil.getPlainText("TXT_KEY_AUTOLOG_BC")
		else:
			return str(zyear) + BugUtil.getPlainText("TXT_KEY_AUTOLOG_AD")

	def _getGameTurn(self):
		zcurrturn = gc.getGame().getElapsedGameTurns() + 1 + BugAutolog.get4000BCTurn()
		zmaxturn = gc.getGame().getMaxTurns()
		if (zmaxturn == 0):
			return "%i" % (zcurrturn)
		else:
			return "%i/%i" % (zcurrturn, zmaxturn)

	def _getFileName(self):
		zsFileName = "%s_%s.txt" % (gc.getActivePlayer().getName(), self._getGameYear())
		return zsFileName

	def _writeMsg(self, sMsg, vColor="Black", vBold=True, vUnderline=True, vOpenSpoiler="", vCloseSpoiler=False):
		sMsg = sDump.buildMsg(sMsg, vColor="Black", vBold=vBold, vUnderline=vUnderline)

		zStyle = BugAutolog.getFormatStyle()
		if (zStyle == 2 or zStyle == 3):  # forum styles
			if vOpenSpoiler != "":
				sMsg = "[spoiler=%s]%s" % (vOpenSpoiler, sMsg)

			if vCloseSpoiler:
				sMsg = "%s[/spoiler]" % (sMsg)

		sDump.write(sMsg, bFlush=False, bPending=False)
