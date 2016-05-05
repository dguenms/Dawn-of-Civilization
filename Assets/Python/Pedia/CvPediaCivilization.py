from CvPythonExtensions import *
import CvUtil
import ScreenInput

gc = CyGlobalContext()



class CvPediaCivilization:
	def __init__(self, main):
		self.iCivilization = -1
		self.top = main

		self.X_INFO_PANE = self.top.X_PEDIA_PAGE
		self.Y_INFO_PANE = self.top.Y_PEDIA_PAGE
		self.W_INFO_PANE = self.top.W_PEDIA_PAGE / 4 - 3
		self.H_INFO_PANE = 120

		self.W_ICON = 100
		self.H_ICON = 100
		self.X_ICON = self.X_INFO_PANE + (self.W_INFO_PANE - self.W_ICON) / 2
		self.Y_ICON = self.Y_INFO_PANE + (self.H_INFO_PANE - self.H_ICON) / 2
		self.ICON_SIZE = 64

		self.X_BUILDINGS = self.top.X_PEDIA_PAGE
		self.Y_BUILDINGS = self.Y_INFO_PANE + self.H_INFO_PANE + 10
		self.W_BUILDINGS = self.W_INFO_PANE
		self.H_BUILDINGS = 110

		self.X_UNITS = self.X_BUILDINGS
		self.Y_UNITS = self.Y_BUILDINGS + self.H_BUILDINGS + 10
		self.W_UNITS = self.W_BUILDINGS
		self.H_UNITS = 110
		
		self.W_DESC = self.top.W_PEDIA_PAGE - self.W_INFO_PANE - 10
		self.Y_DESC = self.Y_INFO_PANE + self.H_INFO_PANE - self.H_BUILDINGS - 10
		self.X_DESC = self.X_INFO_PANE + self.W_INFO_PANE + 10
		self.H_DESC = 360

		self.X_HISTORY = self.X_BUILDINGS
		self.Y_HISTORY = self.Y_UNITS + self.H_UNITS + 10
		self.W_HISTORY = self.top.R_PEDIA_PAGE - self.X_HISTORY
		self.H_HISTORY = self.top.B_PEDIA_PAGE - self.Y_HISTORY



	def interfaceScreen(self, iCivilization):
		self.iCivilization = iCivilization
		self.placeInfo()
		self.placeDescription()
		self.placeBuildings()
		self.placeUnits()
		self.placeHistory()



	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		CivInfo = gc.getCivilizationInfo(self.iCivilization)

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), CivInfo.getButton(), self.X_ICON + self.W_ICON / 2 - self.ICON_SIZE / 2, self.Y_ICON + self.H_ICON / 2 - self.ICON_SIZE / 2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		
	def placeDescription(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()
		
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_DESC, self.Y_DESC, self.W_DESC, self.H_DESC, PanelStyles.PANEL_STYLE_BLUE50)

		szText = u"<font=4b>" + gc.getCivilizationInfo(self.iCivilization).getDescription() + "</font>\n\n"
		szText += CyGameTextMgr().parseCivInfos(self.iCivilization, True)
		screen.addMultilineText(text, szText, self.X_DESC + 10, self.Y_DESC + 10, self.W_DESC - 20, self.H_DESC - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		
		
	def placeLeaders(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_LEADERS", ()), "", False, True, self.X_LEADERS, self.Y_LEADERS, self.W_LEADERS, self.H_LEADERS, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")
		for iLeader in xrange(gc.getNumLeaderHeadInfos()):
			civ = gc.getCivilizationInfo(self.iCivilization)
			if civ.isLeaders(iLeader):
				screen.attachImageButton(panel, "", gc.getLeaderHeadInfo(iLeader).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeader, self.iCivilization, False)



	def placeTechs(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		screen.addPanel(panel, CyTranslator().getText('TXT_KEY_STARTING_TECHS', ()), "", False, True, self.X_TECHS, self.Y_TECHS, self.W_TECHS, self.H_TECHS, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")
		for iTech in xrange(gc.getNumTechInfos()):
			if (gc.getCivilizationInfo(self.iCivilization).isCivilizationFreeTechs(iTech)):
				screen.attachImageButton(panel, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)



	def placeBuildings(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		screen.addPanel(panel, CyTranslator().getText('TXT_KEY_UNIQUE_BUILDINGS', ()), "", False, True, self.X_BUILDINGS, self.Y_BUILDINGS, self.W_BUILDINGS, self.H_BUILDINGS, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")
		for iBuilding in xrange(gc.getNumBuildingClassInfos()):
			iUniqueBuilding = gc.getCivilizationInfo(self.iCivilization).getCivilizationBuildings(iBuilding)
			iDefaultBuilding = gc.getBuildingClassInfo(iBuilding).getDefaultBuildingIndex()
			if (iDefaultBuilding > -1 and iUniqueBuilding > -1 and iDefaultBuilding != iUniqueBuilding and not gc.getBuildingInfo(iUniqueBuilding).isGraphicalOnly()):
				screen.attachImageButton(panel, "", gc.getBuildingInfo(iUniqueBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iUniqueBuilding, -1, False)



	def placeUnits(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		screen.addPanel(panel, CyTranslator().getText('TXT_KEY_FREE_UNITS', ()), "", False, True, self.X_UNITS, self.Y_UNITS, self.W_UNITS, self.H_UNITS, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")
		for iUnit in xrange(gc.getNumUnitClassInfos()):
			iUniqueUnit = gc.getCivilizationInfo(self.iCivilization).getCivilizationUnits(iUnit)
			iDefaultUnit = gc.getUnitClassInfo(iUnit).getDefaultUnitIndex()
			if (iDefaultUnit > -1 and iUniqueUnit > -1 and iDefaultUnit != iUniqueUnit and not gc.getUnitInfo(iUniqueUnit).isGraphicalOnly()):
				screen.attachImageButton(panel, "", gc.getUnitInfo(iUniqueUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUniqueUnit, 1, False)



	def placeHistory(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50)
		szHistory = gc.getCivilizationInfo(self.iCivilization).getCivilopedia()
		screen.addMultilineText(text, szHistory, self.X_HISTORY + 10, self.Y_HISTORY + 30, self.W_HISTORY - 20, self.H_HISTORY - 40, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)




	def handleInput (self, inputClass):
		return 0
