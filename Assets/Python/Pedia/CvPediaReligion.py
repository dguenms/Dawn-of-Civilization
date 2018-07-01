from CvPythonExtensions import *
import CvUtil
import string

from Consts import *
from RFCUtils import utils

gc = CyGlobalContext()



class CvPediaReligion:
	def __init__(self, main):
		self.iReligion = -1
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

		self.X_EFFECTS = self.X_INFO_PANE
		self.Y_EFFECTS = self.Y_REQUIRES + self.H_REQUIRES + 10
		self.W_EFFECTS = self.top.R_PEDIA_PAGE - self.X_EFFECTS
		self.H_EFFECTS = 110
		
		self.X_HISTORY = self.X_INFO_PANE
		self.Y_HISTORY = self.Y_EFFECTS + self.H_EFFECTS + 10
		self.W_HISTORY = self.top.R_PEDIA_PAGE - self.X_HISTORY
		self.H_HISTORY = self.top.B_PEDIA_PAGE - self.Y_HISTORY - 10



	def interfaceScreen(self, iReligion):
		self.iReligion = iReligion
		self.placeInfo()
		self.placeRequires()
		self.placeEffects()
		self.placeHistory()



	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		ReligionInfo = gc.getReligionInfo(self.iReligion)

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), ReligionInfo.getButton(), self.X_ICON + self.W_ICON / 2 - self.ICON_SIZE / 2, self.Y_ICON + self.H_ICON / 2 - self.ICON_SIZE / 2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addListBoxGFC(panel, "", self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panel, False)
		screen.appendListBoxString(panel, u"<font=4b>" + ReligionInfo.getDescription() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		
		
		
	def placeRequires(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50)
		screen.enableSelect(panel, False)
		screen.attachLabel(panel, "", "  ")

		iTech = gc.getReligionInfo(self.iReligion).getTechPrereq()

		if iTech > -1:
			screen.attachImageButton(panel, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)

		if self.iReligion == iBuddhism:
			screen.attachImageButton(panel, "", gc.getBuildingInfo(iHinduTemple).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iHinduTemple, 1, False)
		elif self.iReligion == iCatholicism:
			screen.attachImageButton(panel, "", gc.getReligionInfo(iOrthodoxy).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iOrthodoxy, 1, False)
			screen.attachImageButton(panel, "", gc.getBuildingInfo(iOrthodoxCathedral).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iOrthodoxCathedral, 1, False)
		elif self.iReligion == iProtestantism:
			screen.attachImageButton(panel, "", gc.getReligionInfo(iCatholicism).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iCatholicism, 1, False)
			screen.attachImageButton(panel, "", gc.getTechInfo(iAcademia).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iAcademia, 1, False)
			
	def placeEffects(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", True, False, self.X_EFFECTS, self.Y_EFFECTS, self.W_EFFECTS, self.H_EFFECTS, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachListBoxGFC(panel, text, "", TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(text, False)
		szSpecialText = CyGameTextMgr().parseReligionInfo(self.iReligion, True)
		splitText = string.split(szSpecialText, "\n")
		for special in splitText:
			if len(special) != 0:
				screen.appendListBoxString(text, special, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeHistory(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50)
		victorytext = CyTranslator().getText("TXT_KEY_PEDIA_RELIGIOUS_VICTORY", ())
		bullet = u"%c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)
		for iGoal in range(3):
			victorytext += bullet + utils.getReligiousGoalText(self.iReligion, iGoal) + "\n"
		szHistory = victorytext + "\n" + gc.getReligionInfo(self.iReligion).getCivilopedia()
		screen.addMultilineText(text, szHistory, self.X_HISTORY + 10, self.Y_HISTORY + 30, self.W_HISTORY - 20, self.H_HISTORY - 40, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput (self, inputClass):
		return 0
