from CvPythonExtensions import *
import CvUtil

gc = CyGlobalContext()
localText = CyTranslator()


class CvPediaRoute:

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

		self.X_IMPROVEMENTS = self.X_ANIMATION
		self.Y_IMPROVEMENTS = self.Y_REQUIRES
		self.W_IMPROVEMENTS = self.W_ANIMATION
		self.H_IMPROVEMENTS = self.top.B_PEDIA_PAGE - self.Y_IMPROVEMENTS



	def interfaceScreen(self, iRoute):
		self.iRoute = iRoute
		screen = self.top.getScreen()

		self.placeInfo()
		self.placeRequires()
		self.placeDetails()
		self.placeImprovements()



	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		info = gc.getRouteInfo(self.iRoute)

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), info.getButton(), self.X_ICON + self.W_ICON / 2 - self.ICON_SIZE / 2, self.Y_ICON + self.H_ICON / 2 - self.ICON_SIZE / 2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addListBoxGFC(panel, "", self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panel, False)
		screen.appendListBoxString(panel, u"<font=4b>" + info.getDescription() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		for iBuild in xrange(gc.getNumBuildInfos()):
			BuildInfo = gc.getBuildInfo(iBuild)
			if BuildInfo.getRoute() == self.iRoute:
				szStats = u""
				iTime = BuildInfo.getTime() / gc.getUnitInfo(gc.getInfoTypeForString('UNIT_WORKER')).getWorkRate()
				iTime *= gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getBuildPercent() / 100
				iTime *= gc.getEraInfo(CyGame().getStartEra()).getBuildPercent() / 100
				if iTime > 0:
					szStats += u"%d Turns to Build" % iTime

				iCost = BuildInfo.getCost()
				if iCost > 0:
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

		screen.appendListBoxString(panel, szStats, WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)



	def placeRequires(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		info = gc.getRouteInfo(self.iRoute)

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.attachLabel(panel, "", "  ")

		for iBuild in xrange(gc.getNumBuildInfos()):
			if gc.getBuildInfo(iBuild).getRoute() == self.iRoute and not gc.getBuildInfo(iBuild).isGraphicalOnly():
				iTech = gc.getBuildInfo(iBuild).getTechPrereq()
				if iTech > -1:
					screen.attachImageButton(panel, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)

		iBonusType = info.getPrereqBonus()
		if iBonusType > -1:
			screen.attachImageButton(panel, "", gc.getBonusInfo(iBonusType).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonusType, 1, False)
			
		lPrereqOrBonuses = []
		for i in range(gc.getDefineINT("NUM_ROUTE_PREREQ_OR_BONUSES")):
			iBonusType = info.getPrereqOrBonus(i)
			if iBonusType > 0:
				lPrereqOrBonuses.append(iBonusType)
				
		if lPrereqOrBonuses:
			if info.getPrereqBonus() > -1 and len(lPrereqOrBonuses) > 1:
				screen.attachLabel(panel, "", "(")
				
			for i, iBonusType in enumerate(lPrereqOrBonuses):
				if i > 0:
					screen.attachLabel(panel, "", localText.getText("TXT_KEY_OR", ()))
					
				screen.attachImageButton(panel, "", gc.getBonusInfo(iBonusType).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonusType, 1, False)
				
			if info.getPrereqBonus() > -1 and len(lPrereqOrBonuses) > -1:
				screen.attachLabel(panel, "", ")")


	def placeDetails(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()
		info = gc.getRouteInfo(self.iRoute)

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_DETAILS", ()), "", True, False, self.X_DETAILS, self.Y_DETAILS, self.W_DETAILS, self.H_DETAILS, PanelStyles.PANEL_STYLE_BLUE50)

		szText = u""
		szBullet = CyGame().getSymbolID(FontSymbols.BULLET_CHAR)
		
		iMoveDenominator = gc.getDefineINT("MOVE_DENOMINATOR")
		
		iMovement = iMoveDenominator / info.getMovementCost()
		iFlatMovement = iMoveDenominator / info.getFlatMovementCost()
		
		szText += (u"%cUnits move %d times faster\n" % (szBullet, max(iMovement, iFlatMovement)))
		
		if iFlatMovement > iMovement:
			szText += (u"%cUnit can move at most %d tiles per turn\n" % (szBullet, iFlatMovement))
		
		for iTech in range(gc.getNumTechInfos()):
			iTechMovementChange = info.getTechMovementChange(iTech)
			if iTechMovementChange != 0:
				iTechMovement = iMoveDenominator / (info.getMovementCost() + iTechMovementChange)
				szText += (u"%cUnits move %d times faster with <link=literal>%s</link>\n" % (szBullet, iTechMovement, gc.getTechInfo(iTech).getText()))

		szText += gc.getRouteInfo(self.iRoute).getHelp()
		szText = szText.replace("\n\n", "\n").strip()
		screen.addMultilineText(text, szText, self.X_DETAILS + 5, self.Y_DETAILS + 30, self.W_DETAILS - 10, self.H_DETAILS - 35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeImprovements(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		info = gc.getRouteInfo(self.iRoute)

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_CONCEPT_IMPROVEMENTS", ()), "", True, True, self.X_IMPROVEMENTS, self.Y_IMPROVEMENTS, self.W_IMPROVEMENTS, self.H_IMPROVEMENTS, PanelStyles.PANEL_STYLE_BLUE50)

		for iImprovement in xrange(gc.getNumImprovementInfos()):
			ImprovementInfo = gc.getImprovementInfo(iImprovement)
			bFirst = True
			bEffect = False
			szYield = u""

			for iYieldType in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = ImprovementInfo.getRouteYieldChanges(self.iRoute, iYieldType)
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
				screen.attachImageButton(childpanel, "", gc.getImprovementInfo(iImprovement).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, iImprovement, 1, False )
				screen.attachLabel(childpanel, "", "<font=3>" + szYield + "</font>")



	def handleInput(self, inputClass):
		return 0
