from CvPythonExtensions import *
import CvUtil

gc = CyGlobalContext()



class CvPediaTerrain:
	def __init__(self, main):
		self.iTerrain = -1
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

		self.X_DETAILS = self.X_INFO_PANE + self.W_INFO_PANE + 10
		self.W_DETAILS = self.top.R_PEDIA_PAGE - self.X_DETAILS
		self.H_DETAILS = self.H_INFO_PANE
		self.Y_DETAILS = self.Y_INFO_PANE

		self.X_FEATURES = self.X_INFO_PANE
		self.Y_FEATURES = self.Y_INFO_PANE + self.H_INFO_PANE + 10
		self.W_FEATURES = self.W_INFO_PANE
		self.H_FEATURES = 110

		self.X_IMPROVEMENTS = self.X_FEATURES + self.W_FEATURES + 10
		self.Y_IMPROVEMENTS = self.Y_FEATURES
		self.W_IMPROVEMENTS = self.top.R_PEDIA_PAGE - self.X_IMPROVEMENTS
		self.H_IMPROVEMENTS = self.H_FEATURES

		self.X_RESOURCES = self.X_FEATURES
		self.Y_RESOURCES = self.Y_FEATURES + self.H_FEATURES + 10
		self.W_RESOURCES = self.top.R_PEDIA_PAGE - self.X_RESOURCES
		self.H_RESOURCES = 110

		self.X_HISTORY = self.X_RESOURCES
		self.W_HISTORY = self.top.R_PEDIA_PAGE - self.X_HISTORY
		self.Y_HISTORY = self.Y_RESOURCES + self.H_RESOURCES + 10
		self.H_HISTORY = self.top.B_PEDIA_PAGE - self.Y_HISTORY



	def interfaceScreen(self, iTerrain):
		screen = self.top.getScreen()
		self.iTerrain = iTerrain

		self.placeInfo()
		self.placeDetails()
		self.placeFeatures()
		self.placeImprovements()
		self.placeResources()
		self.placeHistory()



	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		info = gc.getTerrainInfo(self.iTerrain)

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), info.getButton(), self.X_ICON + self.W_ICON / 2 - self.ICON_SIZE / 2, self.Y_ICON + self.H_ICON / 2 - self.ICON_SIZE / 2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addListBoxGFC(panel, "", self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panel, False)
		screen.appendListBoxString(panel, u"<font=4b>" + info.getDescription() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		screen.appendListBoxString(panel, "Terrain", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if self.iTerrain == gc.getInfoTypeForString('TERRAIN_HILL'):
			szStats = (u"%d%c  " % (-1, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar()))
			szStats += (u"+%d%c  " % (1, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()))
		else:
			szStats = u""
			for iYield in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = info.getYield(iYield)
				if iYieldChange != 0:
					szStats += (u"%d%c  " % (iYieldChange, gc.getYieldInfo(iYield).getChar()))

		screen.appendListBoxString(panel, szStats, WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)



	def placeDetails(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()
		info = gc.getTerrainInfo(self.iTerrain)

		screen.addPanel(panel, "", "", True, True, self.X_DETAILS, self.Y_DETAILS, self.W_DETAILS, self.H_DETAILS, PanelStyles.PANEL_STYLE_BLUE50)

		if self.iTerrain != gc.getInfoTypeForString('TERRAIN_HILL'):
			szText = info.getHelp()
			szText += CyGameTextMgr().getTerrainHelp(self.iTerrain, True)
			szText = szText.replace("\n\n", "\n").strip()
			screen.addMultilineText(text, szText, self.X_DETAILS + 5, self.Y_DETAILS + 10, self.W_DETAILS - 10, self.H_DETAILS - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeFeatures(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_MISC_FEATURES", ()), "", False, True, self.X_FEATURES, self.Y_FEATURES, self.W_FEATURES, self.H_FEATURES, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")

		for iFeature in xrange(gc.getNumFeatureInfos()):
			FeatureInfo = gc.getFeatureInfo(iFeature)

			if FeatureInfo.isGraphicalOnly():
				continue
			elif FeatureInfo.isTerrain(self.iTerrain):
				screen.attachImageButton(panel, "", FeatureInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, iFeature, 1, False)



	def placeImprovements(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		info = gc.getTerrainInfo(self.iTerrain)

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ()), "", False, True, self.X_IMPROVEMENTS, self.Y_IMPROVEMENTS, self.W_IMPROVEMENTS, self.H_IMPROVEMENTS, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")

		for iImprovement in xrange(gc.getNumImprovementInfos()):
			ImprovementInfo = gc.getImprovementInfo(iImprovement)
			if ImprovementInfo.isGoody():
				continue
			elif ImprovementInfo.getTerrainMakesValid(self.iTerrain):
				screen.attachImageButton(panel, "", ImprovementInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, iImprovement, 1, False)
			elif self.iTerrain == gc.getInfoTypeForString('TERRAIN_HILL') and ImprovementInfo.isHillsMakesValid():
				screen.attachImageButton(panel, "", ImprovementInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, iImprovement, 1, False)



	def placeResources(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_CONCEPT_RESOURCES", ()), "", False, True, self.X_RESOURCES, self.Y_RESOURCES, self.W_RESOURCES, self.H_RESOURCES, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")

		for iResource in xrange(gc.getNumBonusInfos()):
			ResourceInfo = gc.getBonusInfo(iResource)
			if ResourceInfo.isGraphicalOnly():
				continue
			elif ResourceInfo.isTerrain(self.iTerrain):
				screen.attachImageButton(panel, "", ResourceInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iResource, 1, False)
			elif self.iTerrain == gc.getInfoTypeForString('TERRAIN_HILL') and ResourceInfo.isHills():
				screen.attachImageButton(panel, "", ResourceInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iResource, 1, False)


	def placeHistory(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()
		info = gc.getTerrainInfo(self.iTerrain)

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50 )

		szHistory = info.getCivilopedia()
		screen.addMultilineText(text, szHistory, self.X_HISTORY + 10, self.Y_HISTORY + 30, self.W_HISTORY - 20, self.H_HISTORY - 40, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput (self, inputClass):
		return 0
