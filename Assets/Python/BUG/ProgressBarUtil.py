## Progress Bar Utilities
##
## Holds the information used to display tick marks on progress bars
## Also draws the tick marks
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: Ruff_Hi

from CvPythonExtensions import *
import BugUtil

# Constants

SOLID_MARKS = 0
TICK_MARKS = 1
CENTER_MARKS = 2


# Globals

ArtFileMgr = CyArtFileMgr()


# ProgressBar Class

class ProgressBar:
	def __init__(self, id, x, y, w, h, color, marks, forward):
		self.id = id
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.color = color
		self.marks = marks
		self.forward = forward

#		BugUtil.info("drawTickMarks: %s %i %i %i %i %s %i %s", id, x, y, w, h, color, marks, forward)

		self.BG = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTON_NULL").getPath()

		if self.marks == SOLID_MARKS:
			self.m_y1 = 4
			self.m_y2 = self.h - 4
			self.m_y3 = -1
			self.m_y4 = -1
		elif self.marks == TICK_MARKS:
			self.m_y1 = 4
			self.m_y2 = 4 + 5
			self.m_y3 = self.h - 4 - 5
			self.m_y4 = self.h - 4
		else:  # CENTER_MARKS
			self.m_y1 = self.h / 2
			self.m_y2 = self.h - 4
			self.m_y3 = -1
			self.m_y4 = -1

		self.line_cnt = 0
		self.bVisible = False
		self.barItems = []
	
	def addBarItem(self, item):
		self.barItems.append(item)

	def _setLineCount(self, i):
		self.line_cnt = i

	def _resetLineCount(self):
		self.line_cnt = 0

	def _getNextLineName(self):
		self.line_cnt += 1
		return self.id + "-Tick-" + str(self.line_cnt - 1)

	def _setVisible(self, bValue):
		self.bVisible = bValue

	def _deleteCanvas(self, screen):
		if self.bVisible:
			screen.deleteWidget(self.id)
			self._resetLineCount()
			self._setVisible(False)


	def hide(self, screen):
		screen.hide(self.id)

	def drawTickMarks(self, screen, iCurr, iTotal, iFirst, iRate, bDouble):
		if iRate <= 0:
			return

		self._deleteCanvas(screen)

		screen.addDrawControl(self.id, self.BG, self.x, self.y, self.w, self.h, WidgetTypes.WIDGET_GENERAL, -1, -1)
		self._setVisible(True)

		if self.forward:
			self._drawTickMarks_Forward(screen, iCurr, iTotal, iFirst, iRate, bDouble)
		else:
			self._drawTickMarks_Backward(screen, iCurr, iTotal, iFirst, iRate, bDouble)

		for item in self.barItems:
			screen.moveToFront(item)



	def _drawTickMarks_Forward(self, screen, iCurr, iTotal, iFirst, iRate, bDouble):
		i = 1
		iXPrev = self.w * (iCurr + iFirst) / iTotal
		while True:
			iX = self.w * (iCurr + iFirst + i * iRate) / iTotal

			if (iX > self.w
			or  abs(iX - iXPrev) < 5): break

			self._drawline(screen, self.id, iX, self.m_y1, iX, self.m_y2, self.color, bDouble)
			if self.marks == TICK_MARKS:
				self._drawline(screen, self.id, iX, self.m_y3, iX, self.m_y4, self.color, bDouble)

			i += 1
			iXPrev = iX


	def _drawTickMarks_Backward(self, screen, iCurr, iTotal, iFirst, iRate, bDouble):
		i = 1
		iXPrev = self.w
		iMin = iCurr / iTotal + 1
#		BugUtil.debug("tick marks: %i %i %i %i %i %i", iCurr, iTotal, iFirst, iRate, iXPrev, iMin)
		while True:
			iX = self.w * (iTotal - i * iRate) / iTotal
#			BugUtil.debug("tick marks: %i %i %i %i %i %i", iCurr, iTotal, iFirst, iRate, iX, iMin)

			if (iX < iMin
			or  abs(iX - iXPrev) < 5): break

			self._drawline(screen, self.id, iX, self.m_y1, iX, self.m_y2, self.color, bDouble)
			if self.marks == TICK_MARKS:
				self._drawline(screen, self.id, iX, self.m_y3, iX, self.m_y4, self.color, bDouble)

			i += 1
			iXPrev = iX

#		BugUtil.debug("tick marks - done")

	def _drawline(self, screen, id, x1, y1, x2, y2, color, double):
#		BugUtil.debug("tick marks - drawline %s %i %i %i %i", id, x1, y1, x2, y2)
		if double:
			screen.addLineGFC(id, self._getNextLineName(), x1-1, y1, x2, y2, color)
			screen.addLineGFC(id, self._getNextLineName(), x1, y1, x2-1, y2, color)
		else:
			screen.addLineGFC(id, self._getNextLineName(), x1, y1, x2, y2, color)

