from CvPythonExtensions import *
import CvUtil

gc = CyGlobalContext()



class CvPediaCorporation:

	def __init__(self, main):
		self.iCorporation = -1
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
		self.W_INFO_TEXT = 220
		self.H_INFO_TEXT = self.H_INFO_PANE - 20

		self.X_REQUIRES = self.X_INFO_PANE + self.W_INFO_PANE + 10
		self.W_REQUIRES = self.top.R_PEDIA_PAGE - self.X_REQUIRES
		self.H_REQUIRES = 110
		self.Y_REQUIRES = self.Y_INFO_PANE + self.H_INFO_PANE - self.H_REQUIRES

		self.X_EFFECTS = self.X_INFO_PANE
		self.Y_EFFECTS = self.Y_REQUIRES + self.H_REQUIRES + 10
		self.W_EFFECTS = self.top.R_PEDIA_PAGE - self.X_EFFECTS
		self.H_EFFECTS = 150

		self.X_RESOURCES = self.X_INFO_PANE
		self.Y_RESOURCES = self.Y_EFFECTS + self.H_EFFECTS + 10
		self.W_RESOURCES = self.top.R_PEDIA_PAGE - self.X_EFFECTS
		self.H_RESOURCES = 110

		self.X_HISTORY = self.X_RESOURCES
		self.Y_HISTORY = self.Y_RESOURCES + self.H_RESOURCES + 10
		self.W_HISTORY = self.top.R_PEDIA_PAGE - self.X_HISTORY
		self.H_HISTORY = self.top.B_PEDIA_PAGE - self.Y_HISTORY



	def interfaceScreen(self, iCorporation):
		screen = self.top.getScreen()

		self.iCorporation = iCorporation
		if gc.getCorporationInfo(self.iCorporation) == None:
			self.iCorporation = gc.getBuildingInfo(iCorporation).getFoundsCorporation()
		else:
			self.iCorporation = iCorporation

		self.placeInfo()
		self.placeRequires()
		self.placeEffects()
		self.placeResources()
		self.placeHistory()



	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		CorporationInfo = gc.getCorporationInfo(self.iCorporation)

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), CorporationInfo.getButton(), self.X_ICON + self.W_ICON / 2 - self.ICON_SIZE / 2, self.Y_ICON + self.H_ICON / 2 - self.ICON_SIZE / 2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addListBoxGFC(panel, "", self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panel, False)
		screen.appendListBoxString(panel, u"<font=4b>" + CorporationInfo.getDescription().replace(" ", "\n") + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		screen.appendListBoxString(panel, u"<font=3>Corporation</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)



	def placeRequires(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")

		iTech = gc.getCorporationInfo(self.iCorporation).getTechPrereq()
		if iTech > -1:
			screen.attachImageButton(panel, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)

		for iBuilding in xrange(gc.getNumBuildingInfos()):
			if gc.getBuildingInfo(iBuilding).getFoundsCorporation() == self.iCorporation:
				iTechHQ = gc.getBuildingInfo(iBuilding).getPrereqAndTech()
				screen.attachImageButton(panel, "", gc.getTechInfo(iTechHQ).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTechHQ, 1, False)

		for iUnit in range(gc.getNumUnitInfos()):
			bRequired = False
			for iBuilding in xrange(gc.getNumBuildingInfos()):
				if gc.getBuildingInfo(iBuilding).getFoundsCorporation() == self.iCorporation:
					if gc.getUnitInfo(iUnit).getBuildings(iBuilding) or gc.getUnitInfo(iUnit).getForceBuildings(iBuilding):
						bRequired = True
						break

			if bRequired:
				screen.attachImageButton(panel, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False)



	def placeEffects(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		list = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", True, False, self.X_EFFECTS, self.Y_EFFECTS, self.W_EFFECTS, self.H_EFFECTS, PanelStyles.PANEL_STYLE_BLUE50)

		szSpecialText = ""
		iWealthHQ = gc.getCorporationInfo(self.iCorporation).getHeadquarterCommerce(0)
		if iWealthHQ > 0:
			szSpecialText += CyTranslator().getText('TXT_KEY_CORPORATION_HQ_WEALTH', (iWealthHQ, ""))
		iResearchHQ = gc.getCorporationInfo(self.iCorporation).getHeadquarterCommerce(1)
		if iResearchHQ > 0:
			szSpecialText += CyTranslator().getText('TXT_KEY_CORPORATION_HQ_RESEARCH', (iResearchHQ, ""))
		iCultureHQ = gc.getCorporationInfo(self.iCorporation).getHeadquarterCommerce(2)
		if iCultureHQ > 0:
			szSpecialText += CyTranslator().getText('TXT_KEY_CORPORATION_HQ_CULTURE', (iCultureHQ, ""))
		iEspionageHQ = gc.getCorporationInfo(self.iCorporation).getHeadquarterCommerce(3)
		if iEspionageHQ > 0:
			szSpecialText += CyTranslator().getText('TXT_KEY_CORPORATION_HQ_ESPIONAGE', (iEspionageHQ, ""))

		if szSpecialText: szSpecialText += "\n"
		szSpecialText += CyGameTextMgr().parseCorporationInfo(self.iCorporation, True)[1:]
		screen.addMultilineText(list, szSpecialText, self.X_EFFECTS + 5, self.Y_EFFECTS + 30, self.W_EFFECTS - 10, self.H_EFFECTS - 35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeResources(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_CONCEPT_RESOURCES", ()), "", False, True, self.X_RESOURCES, self.Y_RESOURCES, self.W_RESOURCES, self.H_RESOURCES, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")

		for i in xrange(gc.getDefineINT("NUM_CORPORATION_PREREQ_BONUSES")):
			iResource = gc.getCorporationInfo(self.iCorporation).getPrereqBonus(i)
			if iResource > -1:
				screen.attachImageButton(panel, "", gc.getBonusInfo(iResource).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iResource, 1, False)



	def placeHistory(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50)
		szHistory = gc.getCorporationInfo(self.iCorporation).getCivilopedia()
		screen.addMultilineText(text, szHistory, self.X_HISTORY + 15, self.Y_HISTORY + 40, self.W_HISTORY - 20, self.H_HISTORY - 55, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput (self, inputClass):
		return 0
