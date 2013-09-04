## BUG File stuff

import codecs
import os
import os.path
import string
import BugCore
import BugOptions
import BugPath
import BugConfigTracker

BugFile = BugCore.game.Autolog

class BugFileInstance:

	def __init__(self, bHoldOpen=False):
		self.MsgStore = []
		self.HoldOpen = bHoldOpen

	def setFileName(self, sFileName):
		self.FileName = sFileName

	def write(self, vMsg, bFlush=False, bPending=True):

		if bFlush:
			self.MsgStore = []

		if bPending:
			self.MsgStore.append (vMsg)
			return

		if len(self.MsgStore) > 0:
			self.openFile(self.FileName)
			for sMsg in self.MsgStore:
				self.File.write(sMsg)
			self.closeFile()
			self.MsgStore = []

		self.openFile()
		self.File.write(vMsg)
		self.closeFile()

	def openFile(self, bForce=False, sWrite='a'):
		if (self.HoldOpen and not bForce):
			return

		szPath = BugFile.getFilePath()
		if (not szPath or szPath == "Default"):
			szPath = BugPath.findOrMakeDir("Autolog")
		if (not os.path.isdir(szPath)):
			os.makedirs(szPath)

		szFile = os.path.join(szPath, self.FileName)
		self.File = codecs.open(szFile, sWrite, 'utf-8')
		BugConfigTracker.add("Autolog_Log", szFile)

	def closeFile(self, bForce=False):
		if (self.HoldOpen and not bForce):
			return

		self.File.close()

	def buildMsg(self, vMsg, vColor="Black", vBold=False, vUnderline=False, vPrefix=""):
		if vPrefix != "":
			zMsg = "%s %s" % (vPrefix, vMsg)
		else:
			zMsg = vMsg

		## determine type of message
		zStyle = BugFile.getFormatStyle()
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
			and BugFile.isColorCoding()):
				zMsg = "<span style=\"color: %s\">%s</span>" % (vColor, zMsg)

			zMsg = "%s<br>" % (zMsg)

		else: # forum formatting
			if vBold:
				zMsg = "[b]%s[/b]" % (zMsg)
			if vUnderline:
				zMsg = "[u]%s[/u]" % (zMsg)
			if (vColor != "Black"
			and BugFile.isColorCoding()):
				if zStyle == 2:  # color coding with "
					zMsg = "[color=\"%s\"]%s[/color]" % (vColor, zMsg)
				else:  # color coding without "
					zMsg = "[color=%s]%s[/color]" % (vColor, zMsg)

		return "%s\r\n" % (zMsg)
