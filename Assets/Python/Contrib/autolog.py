## Ruff autologger
## Modified from HOF MOD V1.61.001
## Modified from autolog by eotinb
## contains variables to turn on and off various extra log messages
## Alt+E is always on

from CvPythonExtensions import *
import BugConfigTracker
import BugCore
import BugOptions
import BugPath
import BugUtil
import CvModName
import codecs
import os.path
import time

gc = CyGlobalContext()
AutologOpt = BugCore.game.Autolog

class autologInstance:

	def __init__(self):
		self.MsgStore = []
		self.bStarted = False
		self.LogFileName = None
		self.LogFilePath = None
		self.RealLogFile = None
		self.setLogFileName(AutologOpt.getFileName())
		self.setLogFilePath(AutologOpt.getFilePath())

	def setLogFileName(self, LogFileName, bSaveToOptions=False):
		if (bSaveToOptions):
			AutologOpt.setFileName(LogFileName)
			BugOptions.write()
		self.LogFileName = LogFileName
		self.updateLogFile()
		
	def getLogFileName(self):
		return self.LogFileName
	
	def setLogFilePath(self, LogFilePath, bSaveToOptions=False):
		if (bSaveToOptions):
			AutologOpt.setFilePath(LogFilePath)
			BugOptions.write()
		if (not LogFilePath or LogFilePath == "Default"):
			LogFilePath = BugPath.findOrMakeDir("Autolog")
		self.LogFilePath = LogFilePath
		self.updateLogFile()
		
	def getLogFilePath(self):
		return self.LogFilePath
	
	def updateLogFile(self):
		if self.LogFileName and self.LogFilePath:
			self.bStarted = False
			self.RealLogFile = os.path.join(self.LogFilePath, self.LogFileName)
			BugConfigTracker.add("Autolog_Log", self.RealLogFile)

	def isLogging(self):
		return AutologOpt.isLoggingOn()
	
	def start(self):
		self.writeMsg("")
		self.writeMsg("Logging by " + CvModName.getDisplayNameAndVersion() + " (" + CvModName.getCivNameAndVersion() + ")")
		self.writeMsg("------------------------------------------------")
		zcurrturn = gc.getGame().getElapsedGameTurns() + AutologOpt.get4000BCTurn()
		zmaxturn = gc.getGame().getMaxTurns()
		zyear = gc.getGame().getGameTurnYear()
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
		self.writeMsg(message, vBold=True, vUnderline=True)
		self.bStarted = True

	def writeLog(self, vMsg, vColor = "Black", vBold = False, vUnderline = False, vPrefix = ""):
		self.openLog()
		if len(self.MsgStore) > 0:
			msgs = self.MsgStore
			self.writeLog_pending_flush()
			for sMsg in msgs:
				self.log.write(sMsg)
		self.writeMsg(vMsg, vColor, vBold, vUnderline, vPrefix)
		self.closeLog()

	def writeMsg(self, vMsg, vColor = "Black", vBold = False, vUnderline = False, vPrefix = ""):
		zMsg = self.buildMsg(vMsg, vColor, vBold, vUnderline, vPrefix)
		self.log.write(zMsg)

	def writeLog_pending(self, vMsg, vColor = "Black", vBold = False, vUnderline = False, vPrefix = ""):
		zMsg = self.buildMsg(vMsg, vColor, vBold, vUnderline, vPrefix)
		self.MsgStore.append(zMsg)

	def writeLog_pending_flush(self):
		self.MsgStore = []

	def openLog(self):
		self.log = codecs.open(self.RealLogFile, 'a', 'utf-8')
		if not self.bStarted:
			self.start()

	def closeLog(self):
		self.log.close()

	def buildMsg(self, vMsg, vColor, vBold, vUnderline, vPrefix):
		if vPrefix:
			zMsg = vPrefix + " " + vMsg
		else:
			zMsg = vMsg

		## determine type of message
		zStyle = AutologOpt.getFormatStyle()
		if (zStyle < 0
		or zStyle > 3): zStyle=0

		if zStyle == 0: # no formatting so do nothing
			zMsg = zMsg

		elif zStyle == 1:  # html formatting
			if vBold:
				zMsg = "<b>%s</b>" % (zMsg)
			if vUnderline:
				zMsg = "<u>%s</u>" % (zMsg)
			if (vColor != "Black"
			and AutologOpt.isColorCoding()):
				zMsg = "<span style=\"color: %s\">%s</span>" % (vColor, zMsg)

			zMsg = "%s<br>" % (zMsg)

		else: # forum formatting
			if vBold:
				zMsg = "[b]%s[/b]" % (zMsg)
			if vUnderline:
				zMsg = "[u]%s[/u]" % (zMsg)
			if (vColor != "Black"
			and AutologOpt.isColorCoding()):
				if zStyle == 2:  # color coding with "
					zMsg = "[color=\"%s\"]%s[/color]" % (vColor, zMsg)
				else:  # color coding without "
					zMsg = "[color=%s]%s[/color]" % (vColor, zMsg)

		return "%s\r\n" % (zMsg)
