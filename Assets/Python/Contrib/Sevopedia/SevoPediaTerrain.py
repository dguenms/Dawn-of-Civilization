# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005

#
# Sevopedia 2.3
#   sevotastic.blogspot.com
#   sevotastic@yahoo.com
#
# additional work by Gaurav, Progor, Ket, Vovan, Fitchn, LunarMongoose
# see ReadMe for details
#

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import SevoScreenEnums
import string

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class SevoPediaTerrain:

	def __init__(self, main):
		self.iTerrain = -1
		self.top = main

		self.X_ICON_PANE = self.top.X_PEDIA_PAGE
		self.Y_ICON_PANE = self.top.Y_PEDIA_PAGE
		self.W_ICON_PANE = self.top.W_PEDIA_PAGE
		self.H_ICON_PANE = 210

		self.W_ICON = 150
		self.H_ICON = 150
		self.X_ICON = self.X_ICON_PANE + (self.H_ICON_PANE - self.H_ICON) / 2
		self.Y_ICON = self.Y_ICON_PANE + (self.H_ICON_PANE - self.H_ICON) / 2
		self.ICON_SIZE = 64

		self.X_STATS_PANE = self.X_ICON_PANE + 210
		self.W_STATS_PANE = self.top.R_PEDIA_PAGE - self.X_STATS_PANE
		self.Y_STATS_PANE = 130
		self.H_STATS_PANE = 110

		self.X_SPECIAL_PANE = self.X_ICON_PANE
		self.W_SPECIAL_PANE = self.W_ICON_PANE
		self.Y_SPECIAL_PANE = self.Y_ICON_PANE + self.H_ICON_PANE + 10
		self.H_SPECIAL_PANE = self.top.B_PEDIA_PAGE - self.Y_SPECIAL_PANE



	def interfaceScreen(self, iTerrain):
		self.iTerrain = iTerrain
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON_PANE, self.Y_ICON_PANE, self.W_ICON_PANE, self.H_ICON_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getTerrainInfo(self.iTerrain).getButton(), self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.placeStats()
		self.placeSpecial()



	def placeStats(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
		for k in range(YieldTypes.NUM_YIELD_TYPES):
			iYield = gc.getTerrainInfo(self.iTerrain).getYield(k)
			if (iYield != 0):
				szYield = (u"%s: %i" % (gc.getYieldInfo(k).getDescription().upper(), iYield))
				screen.appendListBoxString(panelName, u"<font=3>" + szYield + (u"%c" % gc.getYieldInfo(k).getChar()) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)



	def placeSpecial(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", True, False, self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		listName = self.top.getNextWidgetName()
		screen.attachListBoxGFC(panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(listName, False)
		szSpecialText = CyGameTextMgr().getTerrainHelp(self.iTerrain, True)
		splitText = string.split(szSpecialText, "\n")
		for special in splitText:
			if len(special) != 0:
				screen.appendListBoxString(listName, special, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput (self, inputClass):
		return 0
