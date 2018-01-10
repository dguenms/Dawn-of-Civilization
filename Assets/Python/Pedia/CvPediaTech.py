from CvPythonExtensions import *
import CvUtil
import CvPediaScreen

gc = CyGlobalContext()



class CvPediaTech(CvPediaScreen.CvPediaScreen):
	def __init__(self, main):
		self.iTech = -1
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
		self.Y_INFO_TEXT = self.Y_ICON + 10
		self.W_INFO_TEXT = 200
		self.H_INFO_TEXT = self.H_INFO_PANE - 20

		self.W_REQUIRES = self.W_INFO_PANE
		self.H_REQUIRES = 110
		self.X_REQUIRES = self.X_INFO_PANE + self.W_INFO_PANE + 10
		self.Y_REQUIRES = self.Y_INFO_PANE + self.H_INFO_PANE - self.H_REQUIRES

		self.X_EFFECTS = self.X_INFO_PANE
		self.Y_EFFECTS = self.Y_INFO_PANE + self.H_INFO_PANE + 10
		self.W_EFFECTS = self.W_INFO_PANE
		self.H_EFFECTS = self.H_REQUIRES

		self.X_LEADS_TO = self.X_EFFECTS + self.W_EFFECTS + 10
		self.Y_LEADS_TO = self.Y_EFFECTS
		self.W_LEADS_TO = self.W_EFFECTS
		self.H_LEADS_TO = self.H_REQUIRES

		self.X_ENABLES = self.X_INFO_PANE
		self.Y_ENABLES = self.Y_EFFECTS + self.H_EFFECTS +10
		self.W_ENABLES = self.top.R_PEDIA_PAGE - self.X_ENABLES
		self.H_ENABLES = self.H_REQUIRES

		self.X_HISTORY = self.X_INFO_PANE
		self.Y_HISTORY = self.Y_ENABLES + self.H_ENABLES + 10
		self.W_HISTORY = self.top.R_PEDIA_PAGE - self.X_HISTORY
		self.H_HISTORY = self.top.B_PEDIA_PAGE - self.Y_HISTORY



	def interfaceScreen(self, iTech):
		if iTech < 0: iTech = gc.getActivePlayer().getCurrentResearch()
	
		self.iTech = iTech
		self.placeInfo()
		self.placePrereqs()
		self.placeLeadsTo()
		self.placeEffects()
		self.placeEnables()
		self.placeHistory()



	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		TechInfo = gc.getTechInfo(self.iTech)
		szEra = gc.getEraInfo(TechInfo.getEra()).getDescription() + " Era"

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), TechInfo.getButton(), self.X_ICON + self.W_ICON / 2 - self.ICON_SIZE / 2, self.Y_ICON + self.H_ICON / 2 - self.ICON_SIZE / 2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addListBoxGFC(panel, "", self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panel, False)
		screen.appendListBoxString(panel, u"<font=4b>" + TechInfo.getDescription() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		screen.appendListBoxString(panel, u"<font=3>" + szEra + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if self.top.iActivePlayer == -1:
			szCost = u"Cost: %d%c" % (TechInfo.getResearchCost(), gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())
		else:
			szCost = u"Cost: %d%c" % (gc.getTeam(CyGame().getActiveTeam()).getResearchCost(self.iTech), gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())

		screen.appendListBoxString(panel, u"<font=3>" + szCost + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)



	def placeLeadsTo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_LEADS_TO", ()), "", False, True, self.X_LEADS_TO, self.Y_LEADS_TO, self.W_LEADS_TO, self.H_LEADS_TO, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")

		for j in xrange(gc.getNumTechInfos()):
			for k in xrange(gc.getNUM_OR_TECH_PREREQS()):
				iPrereq = gc.getTechInfo(j).getPrereqOrTechs(k)
				if iPrereq == self.iTech:
					screen.attachImageButton(panel, "", gc.getTechInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_DERIVED_TECH, j, self.iTech, False)
			for k in xrange(gc.getNUM_AND_TECH_PREREQS()):
				iPrereq = gc.getTechInfo(j).getPrereqAndTechs(k)
				if iPrereq == self.iTech:
					screen.attachImageButton(panel, "", gc.getTechInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_DERIVED_TECH, j, self.iTech, False)



	def placePrereqs(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")

		bFirst = True
		for j in xrange(gc.getNUM_AND_TECH_PREREQS()):
			eTech = gc.getTechInfo(self.iTech).getPrereqAndTechs(j)
			if eTech > -1:
				if not bFirst:
					screen.attachLabel(panel, "", CyTranslator().getText("TXT_KEY_AND", ()))
				else:
					bFirst = False
				screen.attachImageButton(panel, "", gc.getTechInfo(eTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH, eTech, j, False)

		nOrTechs = 0
		for j in xrange(gc.getNUM_OR_TECH_PREREQS()):
			if gc.getTechInfo(self.iTech).getPrereqOrTechs(j) > -1:
				nOrTechs += 1
		szLeftDelimeter = ""
		szRightDelimeter = ""
		if not bFirst:
			if nOrTechs > 1:
				szLeftDelimeter = CyTranslator().getText("TXT_KEY_AND", ()) + "("
				szRightDelimeter = ") "
			elif nOrTechs > 0:
				szLeftDelimeter = CyTranslator().getText("TXT_KEY_AND", ())
			else:
				return

		if len(szLeftDelimeter) > 0:
			screen.attachLabel(panel, "", szLeftDelimeter)

		bFirst = True
		for j in xrange(gc.getNUM_OR_TECH_PREREQS()):
			eTech = gc.getTechInfo(self.iTech).getPrereqOrTechs(j)
			if eTech > -1:
				if not bFirst:
					screen.attachLabel(panel, "", CyTranslator().getText("TXT_KEY_OR", ()))
				else:
					bFirst = False
				screen.attachImageButton(panel, "", gc.getTechInfo(eTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH, eTech, j, False)

		if len(szRightDelimeter) > 0:
			screen.attachLabel(panel, "", szRightDelimeter)



	def placeEffects(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		TechInfo = gc.getTechInfo(self.iTech)

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", False, True, self.X_EFFECTS, self.Y_EFFECTS, self.W_EFFECTS, self.H_EFFECTS, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")

		# Worker Speed
		if TechInfo.getWorkerSpeedModifier() != 0:
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_FEATURE_PRODUCTION").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_WORKER_RATE, self.iTech, -1, False)

		# Irrigation
		if TechInfo.isIrrigation():
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_IRRIGATION").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_IRRIGATION, self.iTech, -1, False)

		# Ignore Irrigation
		if TechInfo.isIgnoreIrrigation():
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_NOIRRIGATION").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_IGNORE_IRRIGATION, self.iTech, -1, False)

		# Improvement Yield
		for j in xrange(gc.getNumImprovementInfos()):
			for k in xrange(YieldTypes.NUM_YIELD_TYPES ):
				if (gc.getImprovementInfo(j).getTechYieldChanges(self.iTech, k)):
					screen.attachImageButton(panel, "", gc.getImprovementInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_YIELD_CHANGE, self.iTech, j, False)

		# Feature Production
		if TechInfo.getFeatureProductionModifier() != 0:
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_FEATURE_PRODUCTION").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_FEATURE_PRODUCTION, self.iTech, -1, False)

		# Route Movement
		for j in xrange(gc.getNumRouteInfos()):
			if gc.getRouteInfo(j).getTechMovementChange(self.iTech) != 0:
				screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MOVE_BONUS").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_MOVE_BONUS, self.iTech, -1, False)

		# Bridge Building
		if TechInfo.isBridgeBuilding():
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_BRIDGEBUILDING").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_BUILD_BRIDGE, self.iTech, -1, False)

		# River Trade
		if TechInfo.isRiverTrade():
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_RIVERTRADE").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, self.iTech, gc.getNumTerrainInfos(), False)

		# Water Trade
		for j in xrange(gc.getNumTerrainInfos()):
			if TechInfo.isTerrainTrade(j):
				screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_WATERTRADE").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, self.iTech, j, False)

		# Water Work
		if TechInfo.isWaterWork():
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_WATERWORK").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_WATER_WORK, self.iTech, -1, False)

		# Water Sight
		if TechInfo.isExtraWaterSeeFrom():
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_LOS").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_LOS_BONUS, self.iTech, -1, False)

		# Water Moves
		for j in xrange(DomainTypes.NUM_DOMAIN_TYPES ):
			if TechInfo.getDomainExtraMoves(j) != 0:
				screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_WATERMOVES").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_DOMAIN_EXTRA_MOVES, self.iTech, j, False)

		# Map Centre
		if TechInfo.isMapCentering():
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MAPCENTER").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_MAP_CENTER, self.iTech, -1, False)

		# Map Reveal
		if TechInfo.isMapVisible():
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MAPREVEAL").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_MAP_REVEAL, self.iTech, -1, False)

		# Map Trading
		if TechInfo.isMapTrading():
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MAPTRADING").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_MAP_TRADE, self.iTech, -1, False)

		# Tech Trading
		if TechInfo.isTechTrading():
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_TECHTRADING").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_TECH_TRADE, self.iTech, -1, False)

		# Wealth Trading
		if TechInfo.isGoldTrading():
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_GOLDTRADING").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_GOLD_TRADE, self.iTech, -1, False)

		# Trade Routes
		if TechInfo.getTradeRoutes() != 0:
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_TRADE_ROUTES").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_TRADE_ROUTES, self.iTech, -1, False)

		# Open Borders
		if TechInfo.isOpenBordersTrading():
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_OPENBORDERS").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_OPEN_BORDERS, self.iTech, -1, False)

		# Defensive Pacts
		if TechInfo.isDefensivePactTrading():
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_DEFENSIVEPACT").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_DEFENSIVE_PACT, self.iTech, -1, False)

		# Permanent Alliances
		if TechInfo.isPermanentAllianceTrading():
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_PERMALLIANCE").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_PERMANENT_ALLIANCE, self.iTech, -1, False)

		# Vassal States
		if TechInfo.isVassalStateTrading():
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_VASSAL").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_VASSAL_STATE, self.iTech, -1, False)

		# Happiness
		if TechInfo.getHappiness() != 0:
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_HAPPINESS").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_HAPPINESS_RATE, self.iTech, -1, False)

		# Health
		if TechInfo.getHealth() != 0:
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_HEALTH").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_HEALTH_RATE, self.iTech, -1, False)

		# Adjustments
		for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES ):
			if TechInfo.isCommerceFlexible(j):
				if j == CommerceTypes.COMMERCE_CULTURE:
					szFileName = "Art/Interface/Buttons/Process/ProcessCulture.dds"
				elif j == CommerceTypes.COMMERCE_ESPIONAGE:
					szFileName = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_DEFENSIVEPACT").getPath()
				else:
					szFileName = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath()

				screen.attachImageButton(panel, "", szFileName, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_ADJUST, self.iTech, j, False)

		# Free Techs
		if TechInfo.getFirstFreeTechs() > 0:
			screen.attachImageButton(panel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_FREETECH").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_FREE_TECH, self.iTech, -1, False)

		# Free Units
		if TechInfo.getFirstFreeUnitClass() != UnitClassTypes.NO_UNITCLASS:
			iCivilization = CyGame().getActiveCivilizationType()
			if iCivilization > -1:
				iUnit = gc.getCivilizationInfo(iCivilization).getCivilizationUnits(TechInfo.getFirstFreeUnitClass())
			else:
				iUnit = gc.getUnitClassInfo(TechInfo.getFirstFreeUnitClass()).getDefaultUnitIndex()

			if iUnit > -1:
				screen.attachImageButton(panel, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_FREE_UNIT, iUnit, self.iTech, False)

		# Obsolete Buildings
		lObsoleteSpecialBuildings = []
		for iBuildingClass in xrange(gc.getNumBuildingClassInfos()):
			iCivilization = CyGame().getActiveCivilizationType()
			if iCivilization > -1:
				iBuilding = gc.getCivilizationInfo(iCivilization).getCivilizationBuildings(iBuildingClass)
				if iBuilding > -1:
					BuildingInfo = gc.getBuildingInfo(iBuilding)
					if BuildingInfo.getObsoleteTech() == self.iTech:
						screen.attachImageButton(panel, "", BuildingInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_OBSOLETE, iBuilding, 1, False)
						
					iSpecial = BuildingInfo.getSpecialBuildingType()
					if iSpecial > -1 and gc.getSpecialBuildingInfo(iSpecial).getObsoleteTech() == self.iTech:
						if iSpecial not in lObsoleteSpecialBuildings: lObsoleteSpecialBuildings.append(iSpecial)
					
		for iSpecial in lObsoleteSpecialBuildings:
			screen.attachImageButton(panel, "", gc.getSpecialBuildingInfo(iSpecial).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_OBSOLETE_SPECIAL, iSpecial, 1, False)

		# Obsolete Resources
		for j in xrange(gc.getNumBonusInfos()):
			if gc.getBonusInfo(j).getTechObsolete() == self.iTech:
				screen.attachImageButton(panel, "", gc.getBonusInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_OBSOLETE_BONUS, j, 1, False)



	def placeEnables(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_BONUS_TRADE", ()), "", False, True, self.X_ENABLES, self.Y_ENABLES, self.W_ENABLES, self.H_ENABLES, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")

		# Civics/Tenets
		for iCivic in xrange(gc.getNumCivicInfos()):
			CivicInfo = gc.getCivicInfo(iCivic)
			if self.iTech == CivicInfo.getTechPrereq():
				screen.attachImageButton(panel, "", CivicInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iCivic, 1, False)


		# Units
		for iUnitClass in xrange(gc.getNumUnitClassInfos()):
			iCivilization = CyGame().getActiveCivilizationType()
			if iCivilization > -1:
				iUnit = gc.getCivilizationInfo(iCivilization).getCivilizationUnits(iUnitClass)
			else:
				iUnit = gc.getUnitClassInfo(iUnitClass).getDefaultUnitIndex()

			if iUnit > -1:
				if isTechRequiredForUnit(self.iTech, iUnit):
					screen.attachImageButton(panel, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False)

		# Promotions
		for iPromotion in xrange(gc.getNumPromotionInfos()):
			PromotionInfo = gc.getPromotionInfo(iPromotion)
			if self.iTech == PromotionInfo.getTechPrereq():
				screen.attachImageButton(panel, "", PromotionInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iPromotion, 1, False)

		# Buildings
		for iBuildingClass in xrange(gc.getNumBuildingClassInfos()):
			iCivilization = CyGame().getActiveCivilizationType()
			if iCivilization > -1:
				iBuilding = gc.getCivilizationInfo(iCivilization).getCivilizationBuildings(iBuildingClass)
			else:
				iBuilding = gc.getBuildingClassInfo(iBuildingClass).getDefaultBuildingIndex()

			if iBuilding > -1:
				if isTechRequiredForBuilding(self.iTech, iBuilding):
					screen.attachImageButton(panel, "", gc.getBuildingInfo(iBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, -1, False)

		# Projects
		for iProject in xrange(gc.getNumProjectInfos()):
			if isTechRequiredForProject(self.iTech, iProject):
				screen.attachImageButton(panel, "", gc.getProjectInfo(iProject).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, iProject, 1, False)

		# Corporations
		for iCorporation in xrange(gc.getNumCorporationInfos()):
			if gc.getCorporationInfo(iCorporation).getTechPrereq() == self.iTech:
				screen.attachImageButton(panel, "", gc.getCorporationInfo(iCorporation).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_FOUND_CORPORATION, self.iTech, iCorporation, False)

		# Improvements/Routes/etc
		for iBuild in xrange(gc.getNumBuildInfos()):
			BuildInfo = gc.getBuildInfo(iBuild)
			bTechFound = False
			
			if BuildInfo.isGraphicalOnly():
				continue
			
			if BuildInfo.getTechPrereq() == self.iTech:
				bTechFound = True
			elif BuildInfo.getTechPrereq() == -1:
				for iFeature in xrange(gc.getNumFeatureInfos()):
					if BuildInfo.getFeatureTech(iFeature) == self.iTech:
						bTechFound = True
						break

			if bTechFound:
				iImprovement = BuildInfo.getImprovement()
				if iImprovement > -1:
					screen.attachImageButton(panel, "", BuildInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, iImprovement, 1, False)
				else:
					screen.attachImageButton(panel, "", BuildInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_IMPROVEMENT, self.iTech, iBuild, False)

		# Resources
		for iResource in xrange(gc.getNumBonusInfos()):
			ResourceInfo = gc.getBonusInfo(iResource)
			if self.iTech == ResourceInfo.getTechReveal():
				screen.attachImageButton(panel, "", ResourceInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iResource, 1, False)

		# Processes
		for iProcess in xrange(gc.getNumProcessInfos()):
			if gc.getProcessInfo(iProcess).getTechPrereq() == self.iTech:
				screen.attachImageButton(panel, "", gc.getProcessInfo(iProcess).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_PROCESS_INFO, self.iTech, iProcess, False)



	def placeHistory(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50)
		szHistory = u"\n" + gc.getTechInfo(self.iTech).getQuote()
		szHistory += u"\n\n\n" + gc.getTechInfo(self.iTech).getCivilopedia()
		screen.addMultilineText(text, szHistory, self.X_HISTORY + 10, self.Y_HISTORY + 30, self.W_HISTORY - 20, self.H_HISTORY - 40, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput (self, inputClass):
		return 0
