from CvPythonExtensions import *
import CvUtil
import string

import Victories

from Core import *
from RFCUtils import *


class CvPediaPaganReligion:

	def __init__(self, main):
		self.iPaganReligion = -1
		self.top = main

		self.X_INFO_PANE = self.top.X_PEDIA_PAGE
		self.Y_INFO_PANE = self.top.Y_PEDIA_PAGE
		self.W_INFO_PANE = 290
		self.H_INFO_PANE = 120

		self.W_ICON = 100
		self.H_ICON = 100
		self.X_ICON = self.X_INFO_PANE + 10
		self.Y_ICON = self.Y_INFO_PANE + 10
		self.ICON_SIZE = 64

		self.X_INFO_TEXT = self.X_INFO_PANE + 110
		self.Y_INFO_TEXT = self.Y_ICON + 15
		self.W_INFO_TEXT = 180
		self.H_INFO_TEXT = self.H_INFO_PANE - 20

		self.X_REQUIRES = self.X_INFO_PANE + self.W_INFO_PANE + 10
		self.W_REQUIRES = self.top.R_PEDIA_PAGE - self.X_REQUIRES
		self.H_REQUIRES = 110
		self.Y_REQUIRES = self.Y_INFO_PANE + self.H_INFO_PANE - self.H_REQUIRES

		self.X_BUILDINGS = self.X_INFO_PANE
		self.Y_BUILDINGS = self.Y_REQUIRES + self.H_REQUIRES + 10
		self.W_BUILDINGS = self.top.R_PEDIA_PAGE - self.X_BUILDINGS
		self.H_BUILDINGS = self.H_REQUIRES
		
		self.X_HISTORY = self.X_INFO_PANE
		self.Y_HISTORY = self.Y_BUILDINGS + self.H_BUILDINGS + 10
		self.W_HISTORY = self.top.R_PEDIA_PAGE - self.X_HISTORY
		self.H_HISTORY = self.top.B_PEDIA_PAGE - self.Y_HISTORY - 10



	def interfaceScreen(self, iPaganReligion):
		self.iPaganReligion = iPaganReligion
		self.placeInfo()
		self.placeRequires()
		self.placeBuildings()
		self.placeHistory()



	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		PaganReligionInfo = infos.paganReligion(self.iPaganReligion)

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), PaganReligionInfo.getButton(), self.X_ICON + self.W_ICON / 2 - self.ICON_SIZE / 2, self.Y_ICON + self.H_ICON / 2 - self.ICON_SIZE / 2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addListBoxGFC(panel, "", self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panel, False)
		screen.appendListBoxString(panel, u"<font=4b>" + PaganReligionInfo.getDescription() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		
		
		
	def placeRequires(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50)
		screen.enableSelect(panel, False)
		screen.attachLabel(panel, "", "  ")
		
		for iCiv in infos.civs():
			if infos.civ(iCiv).getPaganReligion() == self.iPaganReligion:
				screen.attachImageButton(panel, "", infos.civ(iCiv).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, 1, False)

				
	def placeBuildings(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_BUILDINGS", ()), "", False, True, self.X_BUILDINGS, self.Y_BUILDINGS, self.W_BUILDINGS, self.H_BUILDINGS, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")
		
		paganTemples = set()
		iPaganTempleClass = infos.building(iPaganTemple).getBuildingClassType()
		for iCiv in infos.civs():
			iPaganReligionTemple = infos.civ(iCiv).getCivilizationBuildings(iPaganTempleClass)
			if infos.civ(iCiv).getPaganReligion() == self.iPaganReligion and iPaganReligionTemple != iPaganTemple:
				paganTemples.add(iPaganReligionTemple)
		
		for iPaganReligionTemple in paganTemples:
			screen.attachImageButton(panel, "", infos.building(iPaganReligionTemple).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iPaganReligionTemple, -1, False)
		
		for iBuilding in infos.buildings():
			if isWonder(iBuilding) and infos.building(iBuilding).isPagan():
				screen.attachImageButton(panel, "", infos.building(iBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, -1, False)


	def placeHistory(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50)
		victorytext = CyTranslator().getText("TXT_KEY_PEDIA_RELIGIOUS_VICTORY", ())
		victorytext += "\n".join(u"%c%s" % (game.getSymbolID(FontSymbols.BULLET_CHAR), goal.description()) for goal in list(Victories.dReligiousGoals[iPaganVictory]) + [Victories.dAdditionalPaganGoal[self.iPaganReligion]])
		screen.addMultilineText(text, victorytext, self.X_HISTORY + 10, self.Y_HISTORY + 30, self.W_HISTORY - 20, self.H_HISTORY - 40, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)


	def handleInput (self, inputClass):
		return 0
