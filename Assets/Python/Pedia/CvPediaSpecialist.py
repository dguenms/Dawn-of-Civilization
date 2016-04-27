from CvPythonExtensions import *
import CvUtil
import string

gc = CyGlobalContext()



class CvPediaSpecialist:
	def __init__(self, main):
		self.iSpecialist = -1
		self.top = main

		self.X_INFO_PANE = self.top.X_PEDIA_PAGE
		self.Y_INFO_PANE = self.top.Y_PEDIA_PAGE
		self.W_INFO_PANE = (self.top.W_PEDIA_PAGE / 2) - 5
		self.H_INFO_PANE = 120

		self.W_ICON = 100
		self.H_ICON = 100
		self.X_ICON = self.X_INFO_PANE + 10
		self.Y_ICON = self.Y_INFO_PANE + 10
		self.ICON_SIZE = 64

		self.X_INFO_TEXT = self.X_INFO_PANE + 110
		self.Y_INFO_TEXT = self.Y_ICON + 15
		self.W_INFO_TEXT = 200
		self.H_INFO_TEXT = self.H_INFO_PANE - 20

		self.X_EFFECTS = self.X_INFO_PANE + self.W_INFO_PANE + 10
		self.W_EFFECTS = self.top.R_PEDIA_PAGE - self.X_EFFECTS
		self.H_EFFECTS = 110
		self.Y_EFFECTS = self.Y_INFO_PANE + self.H_INFO_PANE - self.H_EFFECTS

		self.X_SOURCES = self.X_INFO_PANE
		self.Y_SOURCES = self.Y_INFO_PANE + self.H_INFO_PANE + 10
		self.W_SOURCES = self.top.R_PEDIA_PAGE - self.X_SOURCES
		self.H_SOURCES = 110

		self.X_HISTORY = self.X_INFO_PANE
		self.Y_HISTORY = self.Y_SOURCES + self.H_SOURCES + 10
		self.W_HISTORY = self.top.R_PEDIA_PAGE - self.X_HISTORY
		self.H_HISTORY = self.top.B_PEDIA_PAGE - self.Y_HISTORY



	def interfaceScreen(self, iSpecialist):
		self.iSpecialist = iSpecialist

		self.placeInfo()
		self.placeEffects()
		self.placeSources()
		self.placeHistory()



	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		SpecialistInfo = gc.getSpecialistInfo(self.iSpecialist)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), SpecialistInfo.getButton(), self.X_ICON + self.W_ICON / 2 - self.ICON_SIZE / 2, self.Y_ICON + self.H_ICON / 2 - self.ICON_SIZE / 2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addListBoxGFC(panel, "", self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panel, False)
		screen.appendListBoxString(panel, u"<font=4b>" + SpecialistInfo.getDescription() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		screen.appendListBoxString(panel, u"<font=3>Specialist</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)



	def placeEffects(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", True, False, self.X_EFFECTS, self.Y_EFFECTS, self.W_EFFECTS, self.H_EFFECTS, PanelStyles.PANEL_STYLE_BLUE50)
		SpecialistInfo = gc.getSpecialistInfo(self.iSpecialist)
		iGPClass = SpecialistInfo.getGreatPeopleUnitClass()
		szGP = ""
		if iGPClass > -1:
			szGP = "(" + gc.getUnitClassInfo(iGPClass).getDescription() + ")"

		szEffects = CyGameTextMgr().getSpecialistHelp(self.iSpecialist, True)[1:]
		szEffects = szEffects.replace("Birth Rate", szGP)
		if iGPClass == gc.getInfoTypeForString('UNITCLASS_PROPHET'):
			szEffects = szEffects.replace(u"%c" % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR), u"%c" % CyGame().getSymbolID(FontSymbols.RELIGION_CHAR))

		screen.addMultilineText(text, szEffects, self.X_EFFECTS + 10, self.Y_EFFECTS + 30, self.W_EFFECTS - 10, self.H_EFFECTS - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeSources(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_SOURCES", ()), "", False, True, self.X_SOURCES, self.Y_SOURCES, self.W_SOURCES, self.H_SOURCES, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")

		for iCivic in xrange(gc.getNumCivicInfos()):
			CivicInfo = gc.getCivicInfo(iCivic)
			if CivicInfo.isSpecialistValid(self.iSpecialist):
				screen.attachImageButton(panel, "", CivicInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iCivic, 1, False)

		for iUnitClass in xrange(gc.getNumUnitClassInfos()):
			iCivilization = CyGame().getActiveCivilizationType()
			if iCivilization > -1:
				iUnit = gc.getCivilizationInfo(iCivilization).getCivilizationUnits(iUnitClass)
			else:
				iUnit = gc.getUnitClassInfo(iUnitClass).getDefaultUnitIndex()

			if iUnit > -1:
				UnitInfo = gc.getUnitInfo(iUnit)
				if UnitInfo.getGreatPeoples(self.iSpecialist):
					screen.attachImageButton(panel, "", UnitInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False)

		for iBuildingClass in xrange(gc.getNumBuildingClassInfos()):
			iCivilization = CyGame().getActiveCivilizationType()
			if iCivilization > -1:
				iBuilding = gc.getCivilizationInfo(iCivilization).getCivilizationBuildings(iBuildingClass)
			else:
				iBuilding = gc.getBuildingClassInfo(iBuildingClass).getDefaultBuildingIndex()

			if iBuilding > -1:
				BuildingInfo = gc.getBuildingInfo(iBuilding)
				if BuildingInfo.getSpecialistCount(self.iSpecialist) > 0 or BuildingInfo.getFreeSpecialistCount(self.iSpecialist) > 0:
					screen.attachImageButton(panel, "", BuildingInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, -1, False)



	def placeHistory(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()

		screen.addPanel(panel, "", "", True, True, self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50)
		szHistory = gc.getSpecialistInfo(self.iSpecialist).getCivilopedia()
		screen.addMultilineText(text, szHistory, self.X_HISTORY + 10, self.Y_HISTORY + 10, self.W_HISTORY - 20, self.H_HISTORY - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput (self, inputClass):
		return 0
