## Ruff statusdump

import codecs
import os
import os.path
import string
import BugCore
import BugOptions
import BugPath
import BugConfigTracker

BugAutolog = BugCore.game.Autolog

class statusdumpInstance:


	def __init__(self):
		self.MsgStore = []
		self.FileName = "StatusDump.txt"  #BugAutolog.getFileName()

	def setFileName(self, FileName, bSaveToOptions=False):
		#if (bSaveToOptions):
		#	BugAutolog.setFileName(LogFileName)
			# TODO: do we need to save this?
		#	BugOptions.write()
		self.FileName = "StatusDump.txt"

	def getFileName(self):
		return self.FileName

#	def isLogging(self):
#		return BugAutolog.isLoggingOn()

	def writeStatusDump(self, vMsg, vColor = "Black", vBold = False, vUnderline = False, vPrefix = ""):

		if len(self.MsgStore) > 0:
			self.openSDFile()
			for sMsg in self.MsgStore:
				self.SDFile.write(sMsg)
			self.closeSDFile()
			self.writeStatusDump_pending_flush()

		zMsg = self.buildMsg(vMsg, vColor, vBold, vUnderline, vPrefix)

		self.openSDFile()
		self.SDFile.write(zMsg)
		self.closeSDFile()

	def writeStatusDump_pending(self, vMsg, vColor = "Black", vBold = False, vUnderline = False, vPrefix = ""):
		zMsg = self.buildMsg(vMsg, vColor, vBold, vUnderline, vPrefix)
		self.MsgStore.append (zMsg)

	def writeStatusDump_pending_flush(self):
		self.MsgStore = []

	def openSDFile(self):
		szPath = BugAutolog.getFilePath()
		if (not szPath or szPath == "Default"):
			szPath = BugPath.findOrMakeDir("Autolog")
		if (not os.path.isdir(szPath)):
			os.makedirs(szPath)
		szFile = os.path.join(szPath, self.FileName)
		self.SDFile = codecs.open(szFile, 'a', 'utf-8')
		BugConfigTracker.add("SDFile_Log", szFile)

	def closeSDFile(self):
		self.SDFile.close()

	def buildMsg(self, vMsg, vColor, vBold, vUnderline, vPrefix):
		if vPrefix != "":
			zMsg = "%s %s" % (vPrefix, vMsg)
		else:
			zMsg = vMsg

		## determine type of message
		zStyle = BugAutolog.getFormatStyle()
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
			and BugAutolog.isColorCoding()):
				zMsg = "<span style=\"color: %s\">%s</span>" % (vColor, zMsg)

			zMsg = "%s<br>" % (zMsg)

		else: # forum formatting
			if vBold:
				zMsg = "[b]%s[/b]" % (zMsg)
			if vUnderline:
				zMsg = "[u]%s[/u]" % (zMsg)
			if (vColor != "Black"
			and BugAutolog.isColorCoding()):
				if zStyle == 2:  # color coding with "
					zMsg = "[color=\"%s\"]%s[/color]" % (vColor, zMsg)
				else:  # color coding without "
					zMsg = "[color=%s]%s[/color]" % (vColor, zMsg)

		return "%s\r\n" % (zMsg)

# EF: What is this unused class for?
#class autologRetain:

#	def __init__(self):
#		bLogFileOpen = False
#		bPlayerHuman = False
#		Counter = 0
