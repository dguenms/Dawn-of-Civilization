from CvPythonExtensions import *
from Consts import *
import CvUtil

gc = CyGlobalContext()



class CvPediaImprovement:

	def __init__(self, main):
		self.iImprovement = -1
		self.top = main

		self.X_INFO_PANE = self.top.X_PEDIA_PAGE
		self.Y_INFO_PANE = self.top.Y_PEDIA_PAGE
		self.W_INFO_PANE = 340
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

		self.X_REQUIRES = self.X_INFO_PANE
		self.Y_REQUIRES = self.Y_INFO_PANE + self.H_INFO_PANE + 10
		self.W_REQUIRES = self.W_INFO_PANE
		self.H_REQUIRES = 110

		self.X_ANIMATION = self.X_INFO_PANE + self.W_INFO_PANE + 10
		self.Y_ANIMATION = self.Y_INFO_PANE + 6
		self.W_ANIMATION = self.top.R_PEDIA_PAGE - self.X_ANIMATION
		self.H_ANIMATION = self.H_INFO_PANE + self.H_REQUIRES + 3
		self.X_ROTATION = -20
		self.Z_ROTATION = 30
		self.ANIMATION_SCALE = 0.6

		self.X_DETAILS = self.X_REQUIRES
		self.Y_DETAILS = self.Y_REQUIRES + self.H_REQUIRES + 10
		self.W_DETAILS = self.W_REQUIRES
		self.H_DETAILS = self.top.B_PEDIA_PAGE - self.Y_DETAILS

		self.X_RESOURCES = self.X_ANIMATION
		self.Y_RESOURCES = self.Y_ANIMATION + self.H_ANIMATION + 10
		self.W_RESOURCES = self.W_ANIMATION
		self.H_RESOURCES = self.top.B_PEDIA_PAGE - self.Y_RESOURCES



	def interfaceScreen(self, iImprovement):
		self.iImprovement = iImprovement
		screen = self.top.getScreen()

		screen.addImprovementGraphicGFC(self.top.getNextWidgetName(), self.iImprovement, self.X_ANIMATION, self.Y_ANIMATION, self.W_ANIMATION, self.H_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION, self.Z_ROTATION, self.ANIMATION_SCALE, True)

		self.placeInfo()
		self.placeRequires()
		self.placeDetails()
		self.placeResources()



	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		info = gc.getImprovementInfo(self.iImprovement)

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), info.getButton(), self.X_ICON + self.W_ICON / 2 - self.ICON_SIZE / 2, self.Y_ICON + self.H_ICON / 2 - self.ICON_SIZE / 2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addListBoxGFC(panel, "", self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panel, False)
		screen.appendListBoxString(panel, u"<font=4b>" + info.getDescription() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		for iBuild in xrange(gc.getNumBuildInfos()):
			BuildInfo = gc.getBuildInfo(iBuild)
			if BuildInfo.getImprovement() == self.iImprovement:
				szStats = u""
				iTime = BuildInfo.getTime() / gc.getUnitInfo(gc.getInfoTypeForString('UNIT_WORKER')).getWorkRate()
				iTime *= gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getBuildPercent() / 100
				iTime *= gc.getEraInfo(CyGame().getStartEra()).getBuildPercent() / 100
				if iTime > 0:
					szStats += u"%d Turns to Build" % iTime

				iCost = BuildInfo.getCost()
				if iCost > 0:
					if iTime > 0: szStats += u", "
					szStats += u"Cost: %d%c" % (iCost, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())

				screen.appendListBoxString(panel, szStats, WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				break

		szStats = u""
		for iYieldType in xrange(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = info.getYieldChange(iYieldType)
			if iYieldChange != 0:
				szSign = ""
				if iYieldChange > 0:
					szSign = "+"
				szStats += (u"%s%d%c  " % (szSign, iYieldChange, gc.getYieldInfo(iYieldType).getChar()))
				
		iHappinessPercent = info.getHappinessPercent()
		if iHappinessPercent != 0:
			symbol = CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR)
			if iHappinessPercent > 0: 
				symbol = CyGame().getSymbolID(FontSymbols.HAPPY_CHAR)
			szStats += (u"+%.2f%c  " % (0.01 * abs(iHappinessPercent), symbol))
				
		iHealthPercent = info.getHealthPercent()
		if iHealthPercent != 0:
			symbol = CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR)
			if iHealthPercent > 0: 
				symbol = CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR)
			szStats += (u"+%.2f%c  " % (0.01 * abs(iHealthPercent), symbol))

		screen.appendListBoxString(panel, szStats, WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)



	def placeRequires(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		info = gc.getImprovementInfo(self.iImprovement)

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.attachLabel(panel, "", "  ")

		for iBuild in xrange(gc.getNumBuildInfos()):
			if gc.getBuildInfo(iBuild).getImprovement() == self.iImprovement and not gc.getBuildInfo(iBuild).isGraphicalOnly():
				iTech = gc.getBuildInfo(iBuild).getTechPrereq()
				if iTech > -1:
					screen.attachImageButton(panel, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)

		for iTerrain in xrange(gc.getNumTerrainInfos()):
			if info.getTerrainMakesValid(iTerrain):
				screen.attachImageButton(panel, "", gc.getTerrainInfo(iTerrain).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, iTerrain, 1, False)

		if info.isHillsMakesValid():
			iHills = gc.getInfoTypeForString('TERRAIN_HILL')
			screen.attachImageButton(panel, "", gc.getTerrainInfo(iHills).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, iHills, 1, False)

		for iFeature in xrange(gc.getNumFeatureInfos()):
			if info.getFeatureMakesValid(iFeature):
				if not gc.getFeatureInfo(iFeature).getType().startswith('FEATURE_POLLUTION'):
					screen.attachImageButton(panel, "", gc.getFeatureInfo(iFeature).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, iFeature, 1, False)



	def placeDetails(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()
		info = gc.getImprovementInfo(self.iImprovement)

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_DETAILS", ()), "", True, False, self.X_DETAILS, self.Y_DETAILS, self.W_DETAILS, self.H_DETAILS, PanelStyles.PANEL_STYLE_BLUE50)

		szText = u""
		szBullet = CyGame().getSymbolID(FontSymbols.BULLET_CHAR)

		for iYieldType in xrange(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = info.getIrrigatedYieldChange(iYieldType)
			if iYieldChange != 0:
				szSign = ""
				if iYieldChange > 0:
					szSign = "+"
				szText += u"%c%s%d%c with <link=CONCEPT_IRRIGATION>Irrigation</link>\n" % (szBullet, szSign, iYieldChange, gc.getYieldInfo(iYieldType).getChar())

		for iYieldType in xrange(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = info.getHillsYieldChange(iYieldType)
			szSign = u""
			if iYieldChange > 0:
				szSign = u"+"
			if iYieldChange != 0:
				szText += u"%c%s%d%c on <link=literal>Hills</link>\n" % (szBullet, szSign, iYieldChange, gc.getYieldInfo(iYieldType).getChar())

		for iYieldType in xrange(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = info.getRiverSideYieldChange(iYieldType)
			szSign = u""
			if iYieldChange > 0:
				szSign = u"+"
			if iYieldChange != 0:
				szText += u"%c%s%d%c next to River\n" % (szBullet, szSign, iYieldChange, gc.getYieldInfo(iYieldType).getChar())
				
		for iYieldType in xrange(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = info.getCoastalYieldChange(iYieldType)
			szSign = u""
			if iYieldChange > 0:
				szSign = u"+"
			if iYieldChange != 0:
				szText += u"%c%s%d%c on the Coast\n" % (szBullet, szSign, iYieldChange, gc.getYieldInfo(iYieldType).getChar())

		for iRoute in xrange(gc.getNumRouteInfos()):
			for iYieldType in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = info.getRouteYieldChanges(iRoute, iYieldType)
				szSign = u""
				if iYieldChange > 0:
					szSign = u"+"
				if iYieldChange != 0:
					szText += u"%c%s%d%c with <link=literal>%s</link>\n" % (szBullet, szSign, iYieldChange, gc.getYieldInfo(iYieldType).getChar(), gc.getRouteInfo(iRoute).getDescription())

		for iTech in xrange(gc.getNumTechInfos()):
			for iYieldType in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = info.getTechYieldChanges(iTech, iYieldType)
				szSign = u""
				if iYieldChange > 0:
					szSign = u"+"
				if iYieldChange != 0:
					szText += u"%c%s%d%c with <link=literal>%s</link>\n" % (szBullet, szSign, iYieldChange, gc.getYieldInfo(iYieldType).getChar(), gc.getTechInfo(iTech).getDescription())

		for iCivic in xrange(gc.getNumCivicInfos()):
			for iYieldType in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = gc.getCivicInfo(iCivic).getImprovementYieldChanges(self.iImprovement, iYieldType)
				szSign = u""
				if iYieldChange > 0:
					szSign = u"+"
				if iYieldChange != 0:
					szText += u"%c%s%d%c with <link=literal>%s</link>\n" % (szBullet, szSign, iYieldChange, gc.getYieldInfo(iYieldType).getChar(), gc.getCivicInfo(iCivic).getDescription())

		if self.iImprovement == iTown:
			szText += u"%c+1%c with <link=literal>%s</link>\n" % (szBullet, gc.getYieldInfo(0).getChar(), gc.getProjectInfo(iHumanGenome).getText())

		szText += gc.getImprovementInfo(self.iImprovement).getHelp()
		szText += CyGameTextMgr().getImprovementHelp(self.iImprovement, True)
		szText = szText.replace("\n\n", "\n").strip()
		screen.addMultilineText(text, szText, self.X_DETAILS + 5, self.Y_DETAILS + 30, self.W_DETAILS - 10, self.H_DETAILS - 35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeResources(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		info = gc.getImprovementInfo(self.iImprovement)

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_CONCEPT_RESOURCES", ()), "", True, True, self.X_RESOURCES, self.Y_RESOURCES, self.W_RESOURCES, self.H_RESOURCES, PanelStyles.PANEL_STYLE_BLUE50)

		for iResource in xrange(gc.getNumBonusInfos()):
			bFirst = True
			bEffect = False
			szYield = u""

			for iYieldType in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = info.getImprovementBonusYield(iResource, iYieldType)
				if iYieldChange != 0:
					bEffect = True
					if bFirst:
						bFirst = False
					else:
						szYield += u", "

					szSign = u""
					if iYieldChange > 0:
						szSign = u"+"
					szYield += (u"%s%i%c" % (szSign, iYieldChange, gc.getYieldInfo(iYieldType).getChar()))

			if bEffect:
				childpanel = self.top.getNextWidgetName()
				screen.attachPanel(panel, childpanel, "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachLabel(childpanel, "", "  ")
				screen.attachImageButton(childpanel, "", gc.getBonusInfo(iResource).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iResource, 1, False )
				screen.attachLabel(childpanel, "", "<font=3>" + szYield + "</font>")



	def handleInput(self, inputClass):
		return 0
