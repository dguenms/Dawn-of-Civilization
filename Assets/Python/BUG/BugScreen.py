## BugScreen
##
## Contains two classes - one for Screens and one for Tabs
##
## BugTab Class
##   Controls the tabs on a screen
##   Note that the screen title is a special form of tab (always shown, never active, no 'draw' or 'refresh' procs associated with it)
##
## setStatus(True / False)
##   sets the tab as the active tab (or not)
##   active tab names are drawn in YELLOW
##
## setEnabled(True / False)
##   sets the tab as enabled or disabled
##   tab names that are disabled are drawn in grey
##   tab names that are enabled are drawn in white
##
## getLabel()
##   returns the formatted tab label
##
##
##
## BugScreen Class
##   Controls the screen, title, background, size
##   Contains the tabs
##
## addBackground(self, sWidgetID, sFile_Key):
##   Contains the tabs
##
## addTitle(self, sWidgetId, sTxt_Key, sFont, bUpper, iX, iY, iZ):
##   Contains the tabs
##
## addTab(self, sWidgetId, sTxt_Key, sFont, bUpper, iX, iY, iZ, bShow, bEnabled, bActive, sDraw, sRefresh, WidgetType):
##   Contains the tabs
##
## evenlySpaceTabs(self):
##   Contains the tabs
##
## updateTabStatus(self, sActiveWidget):
##   Contains the tabs
##
## getActiveTab(self):
##   Contains the tabs
##
## draw(self):
##   Contains the tabs
##
## drawActiveTab(self):
##   Contains the tabs
##
## refreshActiveTab(self):
##   Contains the tabs
##
## drawTabs(self):
##   Contains the tabs
##
##
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: Ruff_Hi

#import BugUtil
from CvPythonExtensions import *
#from PyHelpers import PyPlayer
import CvUtil
#import ScreenInput
#import CvScreenEnums

import BugUtil

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


class BugTab:
	def __init__(self, sWidgetId, sTxt_Key, sFont, bUpper, iX, iY, iZ, bShow, bEnabled, bActive, sDraw, sRefresh, WidgetType):
		self.widget_id = sWidgetId
		self.txt_key = sTxt_Key
		self.font = sFont
		self.upper = bUpper
		self.X = iX
		self.Y = iY
		self.Z = iZ
		self.show = bShow
		self.enabled = bEnabled
		self.active = bActive
		self.DrawProc = sDraw
		self.RefreshProc = sRefresh
		self.WidgetType = WidgetType

	def setStatus(self, bActive):
		self.active = bActive

	def setEnabled(self, bEnabled):
		self.enabled = bEnabled

	def getLabel(self):
		if not self.show:
			return ""

		szText = u"<font=%s>" %(self.font)
		if self.upper:
			szText += localText.getText(self.txt_key, ()).upper()
		else:
			szText += localText.getText(self.txt_key, ())
		szText += u"</font>"
		if not self.enabled:
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_GREY"))
		elif self.active:
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_YELLOW"))
		return szText


class BugScreen:
	def __init__(self, sWidgetId, screen, iWidth, iHeight):
		self.widget_id = sWidgetId
		self.screen = screen
		self.width = iWidth
		self.height = iHeight
		self.tabs = []

	def addBackground(self, sWidgetID, sFile_Key):
		self.BGwidget_Id = sWidgetID
		self.BGkey = sFile_Key

	def addTitle(self, sWidgetId, sTxt_Key, sFont, bUpper, iX, iY, iZ):
		self.Title = BugTab(sWidgetId, sTxt_Key, sFont, bUpper, iX, iY, iZ, True, True, False, None, None, WidgetTypes.WIDGET_GENERAL)

	def addTab(self, sWidgetId, sTxt_Key, sFont, bUpper, iX, iY, iZ, bShow, bEnabled, bActive, sDraw, sRefresh, WidgetType):
		self.tabs.append(BugTab(sWidgetId, sTxt_Key, sFont, bUpper, iX, iY, iZ, bShow, bEnabled, bActive, sDraw, sRefresh, WidgetType))

	def evenlySpaceTabs(self):
		# don't adjust if there are less than 3 tab labels
		if len(self.tabs) <= 2:
			return

		# calculate the total width allowed for the tab labels
		# not the last label is 'right' justified
		sparewidth = self.tabs[len(self.tabs) - 1].X - self.tabs[0].X

#		BugUtil.debug("CvEspionage Advisor: evenlySpaceTabs %i %i %i", self.tabs[len(self.tabs) - 1].X, self.tabs[0].X, sparewidth)

		# count the number of 'gaps'
		# deduct the length of the tab labels that are shown
		num_gaps = 0
		for tab in self.tabs:
			if tab.show:
				sparewidth -= CyInterface().determineWidth(tab.getLabel())
				num_gaps += 1
#				BugUtil.debug("CvEspionage Advisor: evenlySpaceTabs %i", CyInterface().determineWidth(tab.getLabel()))

		# don't adjust if there isn't any gap
		if num_gaps <= 1:
			return

		# calculate the gap width
		gapwidth = sparewidth / (num_gaps - 1)
#		BugUtil.debug("CvEspionage Advisor: evenlySpaceTabs %i %i", gapwidth, num_gaps)

		# reset the 'y' location of the tab labels
		iStart = self.tabs[0].X
		for itab in range(len(self.tabs)):
			# don't adjust the final tab label (typically the 'EXIT' label)
			if itab == len(self.tabs) - 1:
				continue

			if self.tabs[itab].show:
				self.tabs[itab].X = iStart
#				BugUtil.debug("CvEspionage Advisor: evenlySpaceTabs %i", iStart)
				iStart += CyInterface().determineWidth(self.tabs[itab].getLabel())
				iStart += gapwidth

	def updateTabStatus(self, sActiveWidget):
		for tab in self.tabs:
			tab.setStatus(tab.widget_id == sActiveWidget)

	def getActiveTab(self):
		for tab in self.tabs:
			if tab.active:
				return tab.widget_id
		return None

	def draw(self):
		self.screen.setDimensions(self.screen.centerX(0), self.screen.centerY(0), self.width, self.height)

		self.screen.addDDSGFC(self.BGwidget_Id, ArtFileMgr.getInterfaceArtInfo(self.BGkey).getPath(), 0, 0, self.width, self.height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.screen.addPanel(self.widget_id + "TopPanel", u"", u"", True, False, 0, 0, self.width, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		self.screen.addPanel(self.widget_id + "BottomPanel", u"", u"", True, False, 0, 713, self.width, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )

		self.screen.showWindowBackground(False)

		# Title
		self.screen.setLabel(self.Title.widget_id, self.widget_id + "TopPanel", self.Title.getLabel(), CvUtil.FONT_CENTER_JUSTIFY,
							 self.Title.X, self.Title.Y, self.Title.Z, FontTypes.TITLE_FONT, self.Title.WidgetType, -1, -1)

	def drawActiveTab(self):
		for tab in self.tabs:
			if tab.active:
				if not tab.DrawProc == None:
					tab.DrawProc ()
				break

	def refreshActiveTab(self):
		for tab in self.tabs:
			if tab.active:
				if not tab.RefreshProc == None:
					tab.RefreshProc ()
				break

	def drawTabs(self):
#		BugUtil.debug("CvEspionage Advisor: drawTabs %i", len(self.tabs))
		itab = 0
		for tab in self.tabs:
			if tab.show:
				if itab + 1 == len(self.tabs):
					justify = CvUtil.FONT_RIGHT_JUSTIFY
				else:
					justify = CvUtil.FONT_LEFT_JUSTIFY
				self.screen.setText(tab.widget_id, self.widget_id + "BottomPanel", tab.getLabel(), justify,
									tab.X, tab.Y, tab.Z, FontTypes.TITLE_FONT, tab.WidgetType, -1, -1 )
			itab += 1
