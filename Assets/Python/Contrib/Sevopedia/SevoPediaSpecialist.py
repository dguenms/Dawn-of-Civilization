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

class SevoPediaSpecialist:

	def __init__(self, main):
		self.iSpecialist = -1
		self.top = main

		self.X_MAIN_PANEL = self.top.X_PEDIA_PAGE
		self.Y_MAIN_PANEL = self.top.Y_PEDIA_PAGE
		self.W_MAIN_PANEL = 200
		self.H_MAIN_PANEL = 200

		self.W_ICON = 150
		self.H_ICON = 150
		self.X_ICON = self.X_MAIN_PANEL + (self.H_MAIN_PANEL - self.H_ICON) / 2
		self.Y_ICON = self.Y_MAIN_PANEL + (self.H_MAIN_PANEL - self.H_ICON) / 2
		self.ICON_SIZE = 64

		self.X_SPECIAL = self.X_MAIN_PANEL + self.W_MAIN_PANEL + 10
		self.W_SPECIAL = self.top.R_PEDIA_PAGE - self.X_SPECIAL
		self.Y_SPECIAL = self.Y_MAIN_PANEL
		self.H_SPECIAL = self.H_MAIN_PANEL

		self.X_TEXT = self.X_MAIN_PANEL
		self.Y_TEXT = self.Y_MAIN_PANEL + self.H_MAIN_PANEL + 10
		self.W_TEXT = self.top.R_PEDIA_PAGE - self.X_TEXT
		self.H_TEXT = self.top.B_PEDIA_PAGE - self.Y_TEXT



	def interfaceScreen(self, iSpecialist):
		self.iSpecialist = iSpecialist
		screen = self.top.getScreen()

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getSpecialistInfo(self.iSpecialist).getButton(), self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.placeSpecial()
		self.placeText()



	def placeSpecial(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_YIELDS", ()), "", True, False, self.X_SPECIAL, self.Y_SPECIAL, self.W_SPECIAL, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50)
		listName = self.top.getNextWidgetName()
		screen.attachListBoxGFC(panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(listName, False)
		szSpecialText = CyGameTextMgr().getSpecialistHelp(self.iSpecialist, True)
		splitText = string.split(szSpecialText, "\n")
		for special in splitText:
			if len(special) != 0:
				screen.appendListBoxString(listName, special, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeText(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, "", "", True, True, self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50)
		szText = gc.getSpecialistInfo(self.iSpecialist).getCivilopedia()
		screen.attachMultilineText(panelName, "Text", szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput (self, inputClass):
		return 0
