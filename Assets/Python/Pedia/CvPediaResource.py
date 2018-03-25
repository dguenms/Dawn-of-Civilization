from CvPythonExtensions import *
import CvUtil

gc = CyGlobalContext()



class CvPediaResource:
	def __init__(self, main):
		self.iResource = -1
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

		self.X_ANIMATION = self.X_INFO_PANE + self.W_INFO_PANE + 10
		self.Y_ANIMATION = self.Y_INFO_PANE + 6
		self.W_ANIMATION = self.top.R_PEDIA_PAGE - self.X_ANIMATION
		self.H_ANIMATION = 190
		self.X_ROTATION = -20
		self.Z_ROTATION = 30
		self.ANIMATION_SCALE = 0.6

		self.X_IMPROVEMENTS = self.X_INFO_PANE
		self.Y_IMPROVEMENTS = self.Y_INFO_PANE + self.H_INFO_PANE + 10
		self.W_IMPROVEMENTS = self.W_INFO_PANE
		self.H_IMPROVEMENTS = 186

		self.X_TECH = self.X_IMPROVEMENTS + self.W_IMPROVEMENTS + 10
		self.Y_TECH = self.Y_ANIMATION + self.H_ANIMATION + 10
		self.W_TECH = self.W_ANIMATION
		self.H_TECH = 110

		self.X_USES = self.X_IMPROVEMENTS
		self.Y_USES = self.Y_IMPROVEMENTS + self.H_IMPROVEMENTS + 10
		self.W_USES = self.top.R_PEDIA_PAGE - self.X_USES
		self.H_USES = 110

		self.X_HISTORY = self.X_USES
		self.Y_HISTORY = self.Y_USES + self.H_USES + 10
		self.W_HISTORY = self.top.R_PEDIA_PAGE - self.X_HISTORY
		self.H_HISTORY = self.top.B_PEDIA_PAGE - self.Y_HISTORY



	def interfaceScreen(self, iResource):
		screen = self.top.getScreen()
		self.iResource = iResource

		screen.addBonusGraphicGFC(self.top.getNextWidgetName(), self.iResource, self.X_ANIMATION, self.Y_ANIMATION, self.W_ANIMATION, self.H_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION, self.Z_ROTATION, self.ANIMATION_SCALE, True)

		self.placeInfo()
		self.placeImprovements()
		self.placeTech()
		self.placeUses()
		self.placeHistory()



	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		ResourceInfo = gc.getBonusInfo(self.iResource)

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), ResourceInfo.getButton(), self.X_ICON + self.W_ICON / 2 - self.ICON_SIZE / 2, self.Y_ICON + self.H_ICON / 2 - self.ICON_SIZE / 2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addListBoxGFC(panel, "", self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panel, False)
		screen.appendListBoxString(panel, u"<font=4b>" + ResourceInfo.getDescription() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		szStats = u""
		for iYield in xrange(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = ResourceInfo.getYieldChange(iYield)
			if iYieldChange != 0:
				szSign = ""
				if iYieldChange > 0:
					szSign = "+"
				szStats += (u"%s%d%c  " % (szSign, iYieldChange, gc.getYieldInfo(iYield).getChar()))

		iHappiness = ResourceInfo.getHappiness()
		if iHappiness > 0:
			szStats += u"+%d%c  " % (iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
		elif iHappiness < 0:
			szStats += u"+%d%c  " % (abs(iHappiness), CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))

		iHealth = ResourceInfo.getHealth()
		if iHealth > 0:
			szStats += u"+%d%c  " % (iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR))
		elif iHealth < 0:
			szStats += u"+%d%c  " % (abs(iHealth), CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR))

		screen.appendListBoxString(panel, szStats, WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		
		if iHappiness != 0 or iHealth != 0:
			screen.appendListBoxString(panel, CyTranslator().getText("TXT_KEY_AFFECTED_CITIES", (ResourceInfo.getAffectedCities(),)), WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)


	def placeTech(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_CONCEPT_TECHNOLOGY", ()), "", False, True, self.X_TECH, self.Y_TECH, self.W_TECH, self.H_TECH, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")

		iTech = gc.getBonusInfo(self.iResource).getTechReveal()
		if iTech > -1:
			screen.attachImageButton(panel, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)
			screen.attachLabel(panel, "", u" (" + CyTranslator().getText("TXT_KEY_PEDIA_BONUS_APPEARANCE", ()) + u")   ")

		iTech = gc.getBonusInfo(self.iResource).getTechCityTrade()
		if iTech > -1:
			screen.attachImageButton(panel, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)
			screen.attachLabel(panel, "", u" (" + CyTranslator().getText("TXT_KEY_PEDIA_BONUS_TRADE", ()) + u")   ")

		iTech = gc.getBonusInfo(self.iResource).getTechPlayerTrade()
		if iTech > -1:
			screen.attachImageButton(panel, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)
			screen.attachLabel(panel, "", u" (" + CyTranslator().getText("Trade", ()) + u")   ")
			
		iTech = gc.getBonusInfo(self.iResource).getTechObsolete()
		if iTech > -1:
			screen.attachImageButton(panel, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)
			screen.attachLabel(panel, "", u" (" + CyTranslator().getText("Obsoletes", ()) + u")   ")



	def placeImprovements(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ()), "", True, False, self.X_IMPROVEMENTS, self.Y_IMPROVEMENTS, self.W_IMPROVEMENTS, self.H_IMPROVEMENTS, PanelStyles.PANEL_STYLE_BLUE50)


		for iImprovement in xrange(gc.getNumImprovementInfos()):
			ImprovementInfo = gc.getImprovementInfo(iImprovement)
			bEffect = False
			bFirst = True

			szYield = u"  "
			for iYield in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = ImprovementInfo.getImprovementBonusYield(self.iResource, iYield)
				if iYieldChange != 0:
					bEffect = True
					iYieldChange += ImprovementInfo.getYieldChange(iYield)
					if bFirst:
						bFirst = False
					else:
						szYield += ", "

					if iYieldChange > 0:
						sign = "+"
					else:
						sign = ""

					szYield += (u"%s%i%c" % (sign, iYieldChange, gc.getYieldInfo(iYield).getChar()))

			if bEffect:
				subpanel = self.top.getNextWidgetName()
				screen.attachPanel(panel, subpanel, "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachLabel(subpanel, "", "  ")
				screen.attachImageButton(subpanel, "",ImprovementInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, iImprovement, 1, False)
				screen.attachLabel(subpanel, "", "<font=3>" + szYield + "</font>")



	def placeUses(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_USED_BY", ()), "", False, True, self.X_USES, self.Y_USES, self.W_USES, self.H_USES, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")

		# Units
		for iUnitClass in xrange(gc.getNumUnitClassInfos()):
			iCivilization = CyGame().getActiveCivilizationType()
			if iCivilization > -1:
				iUnit = gc.getCivilizationInfo(iCivilization).getCivilizationUnits(iUnitClass)
			else:
				iUnit = gc.getUnitClassInfo(iUnitClass).getDefaultUnitIndex()

			if iUnit > -1:
				UnitInfo = gc.getUnitInfo(iUnit)
				bFound = False

				if UnitInfo.getBonusProductionModifier(self.iResource) > 0:
					bFound = True

				elif UnitInfo.getPrereqAndBonus() == self.iResource:
					bFound = True
				else:
					for j in xrange(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
						if UnitInfo.getPrereqOrBonuses(j) == self.iResource:
							bFound = True
							break

				if bFound:
					screen.attachImageButton(panel, "", UnitInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False)

		# Buildings
		for iBuildingClass in xrange(gc.getNumBuildingClassInfos()):
			iCivilization = CyGame().getActiveCivilizationType()
			if iCivilization > -1:
				iBuilding = gc.getCivilizationInfo(iCivilization).getCivilizationBuildings(iBuildingClass)
			else:
				iBuilding = gc.getBuildingClassInfo(iBuildingClass).getDefaultBuildingIndex()

			if iBuilding > -1:
				BuildingInfo = gc.getBuildingInfo(iBuilding)
				if BuildingInfo.isGraphicalOnly():
					continue

				bFound = False
				if BuildingInfo.getPrereqAndBonus() == self.iResource:
					bFound = True
				elif BuildingInfo.getBonusHappinessChanges(self.iResource) > 0:
					bFound = True
				elif BuildingInfo.getBonusHealthChanges(self.iResource) > 0:
					bFound = True
				elif BuildingInfo.getBonusProductionModifier(self.iResource) > 0:
					bFound = True
				elif BuildingInfo.getFreeBonus() == self.iResource:
					bFound = True
				elif BuildingInfo.getNoBonus() == self.iResource:
					bFound = True
				elif BuildingInfo.getPowerBonus() == self.iResource:
					bFound = True
				else:
					for iYield in xrange(YieldTypes.NUM_YIELD_TYPES):
						if BuildingInfo.getBonusYieldModifier(self.iResource, iYield) > 0:
							bFound = True
							break

					for j in xrange(gc.getNUM_BUILDING_PREREQ_OR_BONUSES()):
						if BuildingInfo.getPrereqOrBonuses(j) == self.iResource:
							bFound = True
							break

				if bFound:
					screen.attachImageButton(panel, "", BuildingInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, -1, False)

		# Projects
		for iProject in xrange(gc.getNumProjectInfos()):
			ProjectInfo = gc.getProjectInfo(iProject)
			if ProjectInfo.getBonusProductionModifier(self.iResource) > 0:
				screen.attachImageButton(panel, "", ProjectInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, iProject, 1, False)

		# Corporations
		for iCorporation in xrange(gc.getNumCorporationInfos()):
			CorporationInfo = gc.getCorporationInfo(iCorporation)
			for i in xrange(gc.getNUM_CORPORATION_PREREQ_BONUSES ()):
				if CorporationInfo.getPrereqBonus(i) == self.iResource:
					screen.attachImageButton(panel, "", CorporationInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, iCorporation, 1, False)

		# Routes
		for iRoute in xrange(gc.getNumRouteInfos()):
			RouteInfo = gc.getRouteInfo(iRoute)
			bFound = False

			if RouteInfo.getPrereqBonus() == self.iResource:
				bFound = True
			else:
				for i in xrange(gc.getNUM_ROUTE_PREREQ_OR_BONUSES()):
					if RouteInfo.getPrereqOrBonus(i) == self.iResource:
						bFound = True
						break

			if bFound:
				screen.attachImageButton(panel, "", RouteInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_ROUTE, iRoute, -1, False)



	def placeHistory(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		screen.addPanel(panel,CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")
		textName = self.top.getNextWidgetName()
		screen.addMultilineText( textName, gc.getBonusInfo(self.iResource).getCivilopedia(), self.X_HISTORY + 15, self.Y_HISTORY + 40, self.W_HISTORY - (30), self.H_HISTORY - (15 * 2) - 25, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput (self, inputClass):
		return 0
