from CvPythonExtensions import *
import CvUtil
import CvScreenEnums
import CvScreensInterface

from Consts import *
from RFCUtils import utils

gc = CyGlobalContext()

CIV_HAS_TECH = 0
CIV_IS_RESEARCHING = 1
CIV_NO_RESEARCH = 2
CIV_TECH_AVAILABLE = 3



class CvTechChooser:
	def __init__(self):
		self.iPlayer = -1
		self.iCivilization = -1
		self.TechEffects = {}
		self.GreatPeopleList = []
		self.iMinX = 1

		self.nWidgetCount = 0
		self.aiCurrentState = []
		for i in xrange(gc.getNumTechInfos()):
			self.aiCurrentState.append(-1)

		# Filters
		self.bResearched = False
		self.bBuilt = False
		self.iFromEra = 0
		self.iHideEra = iDigital

		# Advanced Start
		self.iSelectedTech = -1
		self.bSelectedTechDirty = False
		self.bTechBoxesDirty = False



	def getScreen(self):
		return CyGInterfaceScreen("TechChooser", CvScreenEnums.TECH_CHOOSER)



	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()



	def interfaceScreen(self):
		''
		self.iPlayer = CyGame().getActivePlayer()
		if CyGame().isPitbossHost():
			return

		screen = self.getScreen()
		player = gc.getPlayer(self.iPlayer)
		team = gc.getTeam(player.getTeam())

		self.X_RESOLUTION = screen.getXResolution()
		self.Y_RESOLUTION = screen.getYResolution()

		if self.X_RESOLUTION >= 1280:
			self.W_SCREEN = 1280
			self.H_SCREEN = 740
		else:
			self.W_SCREEN = self.X_RESOLUTION
			self.H_SCREEN = 768

		self.W_TOP_PANEL = self.W_SCREEN
		self.H_TOP_PANEL = 55
		self.X_TOP_PANEL = 0
		self.Y_TOP_PANEL = -2

		self.W_BOTTOM_PANEL = self.W_SCREEN
		self.H_BOTTOM_PANEL = 55
		self.X_BOTTOM_PANEL = 0
		self.Y_BOTTOM_PANEL = self.H_SCREEN - self.H_BOTTOM_PANEL

		self.X_TITLE = self.X_TOP_PANEL + (self.W_TOP_PANEL / 2)
		self.Y_TITLE = self.Y_TOP_PANEL + 14

		self.ICON_SIZE = 24
		self.TECH_ICON_SIZE = 48
		self.GP_ICON_SIZE = 32

		self.X_ITEMS = self.TECH_ICON_SIZE + 8
		self.X_INCREMENT = self.ICON_SIZE + 3
		self.Y_ITEMS = 30
		self.MAX_ITEMS = 5

		self.PIXEL_INCREMENT = 7
		self.BOX_WIDTH = self.PIXEL_INCREMENT * 3 + self.TECH_ICON_SIZE + (self.X_INCREMENT * self.MAX_ITEMS)
		self.BOX_HEIGHT = self.ICON_SIZE * 3
		self.BOX_X_SPACING = self.X_INCREMENT * 2
		self.BOX_Y_SPACING = self.BOX_HEIGHT / 2 + self.PIXEL_INCREMENT

		self.X_ADVANCED_START = 25
		self.Y_ADVANCED_START = self.Y_BOTTOM_PANEL + 22
		self.W_ADVANCED_START = 150
		self.H_ADVANCED_START = 30

		self.X_EXIT = self.W_BOTTOM_PANEL - 25
		self.Y_EXIT = self.Y_BOTTOM_PANEL + 20

		screen.setDimensions((self.X_RESOLUTION / 2) - (self.W_SCREEN / 2), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.addDDSGFC("ScreenBackground", CyArtFileMgr().getInterfaceArtInfo('SCREEN_BG_OPAQUE').getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.moveToBack("ScreenBackground")
		screen.showWindowBackground(False)

		screen.addPanel("TechTopPanel", u"", u"", True, False, self.X_TOP_PANEL, self.Y_TOP_PANEL, self.W_TOP_PANEL, self.H_TOP_PANEL, PanelStyles.PANEL_STYLE_TOPBAR)
		screen.addPanel("TechBottomPanel", u"", u"", True, False, self.X_BOTTOM_PANEL, self.Y_BOTTOM_PANEL, self.W_BOTTOM_PANEL, self.H_BOTTOM_PANEL, PanelStyles.PANEL_STYLE_BOTTOMBAR)
		screen.setLabel("TechTitle", "Background", u"<font=4b>TECHNOLOGY ADVISOR</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_TITLE, self.Y_TITLE, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText("TechExit", "Background", u"<font=4>EXIT</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

		# Filters
		iSize = 28
		szBorder = CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath()

		screen.addCheckBoxGFC("FilterResearched", "Art/Interface/Buttons/Process/ProcessResearch.dds", szBorder, 10, 10, iSize, iSize, WidgetTypes.WIDGET_PYTHON, 7801, 0, ButtonStyles.BUTTON_STYLE_IMAGE)
		screen.setState("FilterResearched", self.bResearched)

		screen.addCheckBoxGFC("FilterBuilt", ",Art/Interface/Buttons/Actions/FoundCity.dds,Art/Interface/Buttons/Charlemagne_Atlas.dds,8,1", szBorder, 10 + iSize, 10, iSize, iSize, WidgetTypes.WIDGET_PYTHON, 7801, 2, ButtonStyles.BUTTON_STYLE_IMAGE)
		screen.setState("FilterBuilt", self.bBuilt)

		self.iMinX = 9999999
		self.iFromEra = min(gc.getNumEraInfos() - 1, max(0, self.iFromEra))
		self.iHideEra = min(gc.getNumEraInfos() - 1, max(0, self.iHideEra))

		for iTech in xrange(gc.getNumTechInfos()):
			TechInfo = gc.getTechInfo(iTech)
			if TechInfo.getEra() < self.iFromEra:
				continue
			if TechInfo.getEra() > self.iHideEra:
				continue
			if self.bResearched and team.isHasTech(iTech):
				continue

			iX = TechInfo.getGridX()
			if iX < 1:
				continue
			self.iMinX = min(self.iMinX, iX)

		screen.addDropDownBoxGFC("FilterFromEra", self.W_SCREEN - 280, 8, 120, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addDropDownBoxGFC("FilterToEra", self.W_SCREEN - 130, 8, 120, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.setButtonGFC("RightArrow", "", "", self.W_SCREEN - 155, 10, 24, 24, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT)
		screen.setHitTest("RightArrow", HitTestTypes.HITTEST_NOHIT)

		for iEra in xrange(iDigital+1):
			if iEra <= self.iHideEra:
				screen.addPullDownString("FilterFromEra", gc.getEraInfo(iEra).getDescription(), iEra, iEra, iEra == self.iFromEra)
			if iEra >= self.iFromEra:
				screen.addPullDownString("FilterToEra", gc.getEraInfo(iEra).getDescription(), iEra, iEra, iEra == self.iHideEra)

		# Tech Effects
		if not self.TechEffects or player.getCivilizationType() != self.iCivilization:
			self.initTechs()

		# Great People Techs
		if not self.GreatPeopleList:
			for iUnitClass in xrange(gc.getNumUnitClassInfos()):
				iUnit = utils.getUniqueUnitType(self.iPlayer, iUnitClass)
				if iUnit > -1:
					if iUnit in self.GreatPeopleList:
						continue
					if gc.getUnitInfo(iUnit).getBaseDiscover() > 0:
						self.GreatPeopleList.append(iUnit)

		self.placeGreatPeople()

		# Advanced Start
		if player.getAdvancedStartPoints() > -1:
			self.bSelectedTechDirty = True
			szText = CyTranslator().getText("TXT_KEY_WB_AS_ADD_TECH", ())
			screen.setButtonGFC("AddTechButton", szText, "", self.X_ADVANCED_START, self.Y_ADVANCED_START - 5, self.W_ADVANCED_START, self.H_ADVANCED_START, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
			screen.hide("AddTechButton")
			screen.hide("AddTechCost")

		# Debug
		screen.hide("CivDropDown")
		if CyGame().isDebugMode():
			screen.addDropDownBoxGFC("CivDropDown", 10 + iSize * 3, 8, 160, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.SMALL_FONT)
			screen.setActivation("CivDropDown", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS)
			for j in xrange(gc.getMAX_PLAYERS()):
				if gc.getPlayer(j).isAlive():
					screen.addPullDownString("CivDropDown", gc.getPlayer(j).getName(), j, j, self.iPlayer == j)

		# Check Redraw
		if screen.isPersistent() and not (self.bResearched or self.bBuilt):
			self.updateTechs(False)
			return

		self.nWidgetCount = 0
		self.aiCurrentState = []
		for i in xrange(gc.getNumTechInfos()):
			self.aiCurrentState.append(-1)

		screen.setPersistent(True)

		# Scrolling Panel
		screen.addScrollPanel("TechList", u"", 0, 60, self.W_SCREEN, self.H_SCREEN - 132, PanelStyles.PANEL_STYLE_EXTERNAL)
		screen.setActivation("TechList", ActivationTypes.ACTIVATE_NORMAL)
		screen.hide("TechList")
		self.placeTechs()



	def scaleScreen(self, xResolution, yResolution):
		''
		self.W_SCREEN = xResolution
		self.H_SCREEN = 740

		self.W_TOP_PANEL = self.W_SCREEN
		self.H_TOP_PANEL = 55
		self.X_TOP_PANEL = 0
		self.Y_TOP_PANEL = -2

		self.W_BOTTOM_PANEL = self.W_SCREEN
		self.H_BOTTOM_PANEL = 55
		self.X_BOTTOM_PANEL = 0
		self.Y_BOTTOM_PANEL = self.H_SCREEN - self.H_BOTTOM_PANEL

		self.X_TITLE = self.X_TOP_PANEL + (self.W_TOP_PANEL / 2)
		self.Y_TITLE = self.Y_TOP_PANEL + 14

		self.X_EXIT = self.W_BOTTOM_PANEL - 25
		self.Y_EXIT = self.Y_BOTTOM_PANEL + 20



	def initTechs(self):
		''
		player = gc.getPlayer(self.iPlayer)
		self.iCivilization = player.getCivilizationType()
		self.TechEffects.clear()
		for iTech in xrange(gc.getNumTechInfos()):
			self.TechEffects[iTech] = []

		# Units
		for iClass in xrange(gc.getNumUnitClassInfos()):
			iUnit = utils.getUniqueUnitType(self.iPlayer, iClass)
			if iUnit > -1 and not gc.getUnitInfo(iUnit).isGraphicalOnly():
				iTech = gc.getUnitInfo(iUnit).getPrereqAndTech()
				if iTech > -1:
					self.TechEffects[iTech].append(("Unit", iUnit))

		# Promotions
		for iPromotion in xrange(gc.getNumPromotionInfos()):
			iTech = gc.getPromotionInfo(iPromotion).getTechPrereq()
			if iTech > -1:
				self.TechEffects[iTech].append(("Promotion", iPromotion))

		# Buildings
		for iClass in xrange(gc.getNumBuildingClassInfos()):
			iBuilding = utils.getUniqueBuildingType(self.iPlayer, iClass)
			if iBuilding > -1:
				BuildingInfo = gc.getBuildingInfo(iBuilding)
				if BuildingInfo.getFoundsCorporation() > -1:
					continue
				iTech = BuildingInfo.getPrereqAndTech()
				if iTech > -1:
					self.TechEffects[iTech].append(("Building", iBuilding))
				#iTech = BuildingInfo.getObsoleteTech()
				#if iTech > -1:
				#	self.TechEffects[iTech].append(("ObsoleteBuilding", iBuilding))

		# Special Buildings
		for iSpecial in xrange(gc.getNumSpecialBuildingInfos()):
			iTech = gc.getSpecialBuildingInfo(iSpecial).getTechPrereq()
			if iTech > -1:
				self.TechEffects[iTech].append(("SpecialBuilding", iSpecial))
			iTech = gc.getSpecialBuildingInfo(iSpecial).getObsoleteTech()
			if iTech > -1:
				self.TechEffects[iTech].append(("ObsoleteSpecialBuilding", iSpecial))

		# Projects
		for iProject in xrange(gc.getNumProjectInfos()):
			iTech = gc.getProjectInfo(iProject).getTechPrereq()
			if iTech > -1:
				self.TechEffects[iTech].append(("Project", iProject))

		# Civics / Tenets
		for iCivic in xrange(gc.getNumCivicInfos()):
			iTech = gc.getCivicInfo(iCivic).getTechPrereq()
			if iTech > -1:
				self.TechEffects[iTech].append(("Civic", iCivic))

		# Corporations
		for iCorporation in xrange(gc.getNumCorporationInfos()):
			iTech = gc.getCorporationInfo(iCorporation).getTechPrereq()
			if iTech > -1:
				self.TechEffects[iTech].append(("Corporation", iCorporation))

		# Improvements
		for iBuild in xrange(gc.getNumBuildInfos()):
			if gc.getBuildInfo(iBuild).isGraphicalOnly(): continue
			bTechFound = False
			iTech = gc.getBuildInfo(iBuild).getTechPrereq()
			if iTech > -1:
				self.TechEffects[iTech].append(("Improvement", iBuild))
			else:
				for iFeature in xrange(gc.getNumFeatureInfos()):
					iTech = gc.getBuildInfo(iBuild).getFeatureTech(iFeature)
					if iTech > -1:
						self.TechEffects[iTech].append(("Improvement", iBuild))

		# Resources
		for iResource in xrange(gc.getNumBonusInfos()):
			iTech = gc.getBonusInfo(iResource).getTechReveal()
			if iTech > -1:
				self.TechEffects[iTech].append(("RevealResource", iResource))
			iTech = gc.getBonusInfo(iResource).getTechObsolete()
			if iTech > -1:
				self.TechEffects[iTech].append(("ObsoleteResource", iResource))
			iTech = gc.getBonusInfo(iResource).getTechPlayerTrade()
			if iTech > -1:
				if ("ResourceTrade", -1) not in self.TechEffects[iTech]:
					self.TechEffects[iTech].append(("ResourceTrade", -1))

		# Other Effects
		for iTech in xrange(gc.getNumTechInfos()):
			TechInfo = gc.getTechInfo(iTech)

			for iImprovement in xrange(gc.getNumImprovementInfos()):
				for iYieldType in xrange(YieldTypes.NUM_YIELD_TYPES):
					if gc.getImprovementInfo(iImprovement).getTechYieldChanges(iTech, iYieldType):
						self.TechEffects[iTech].append(("ImprovementYield", iImprovement))

			if TechInfo.isIrrigation():
				self.TechEffects[iTech].append(("EnableIrrigation", -1))
			if TechInfo.isIgnoreIrrigation():
				self.TechEffects[iTech].append(("IgnoreIrrigation", -1))
			if TechInfo.getWorkerSpeedModifier():
				self.TechEffects[iTech].append(("WorkerSpeed", -1))
			if TechInfo.getFeatureProductionModifier():
				self.TechEffects[iTech].append(("FeatureProduction", -1))

			for iRoute in xrange(gc.getNumRouteInfos()):
				if gc.getRouteInfo(iRoute).getTechMovementChange(iTech) != 0:
					self.TechEffects[iTech].append(("RouteMovement", iRoute))

			if TechInfo.isBridgeBuilding():
				self.TechEffects[iTech].append(("BridgeBuilding", -1))
			if TechInfo.isRiverTrade():
				self.TechEffects[iTech].append(("RiverTrade", -1))

			for iTerrain in xrange(gc.getNumTerrainInfos()):
				if TechInfo.isTerrainTrade(iTerrain):
					self.TechEffects[iTech].append(("WaterTrade", iTerrain))

			if TechInfo.isWaterWork():
				self.TechEffects[iTech].append(("WaterWork", -1))
			if TechInfo.isExtraWaterSeeFrom():
				self.TechEffects[iTech].append(("WaterSight", -1))

			for iDomain in xrange(DomainTypes.NUM_DOMAIN_TYPES):
				if TechInfo.getDomainExtraMoves(iDomain):
					self.TechEffects[iTech].append(("WaterMoves", iDomain))

			if TechInfo.isMapCentering():
				self.TechEffects[iTech].append(("MapCenter", -1))
			if TechInfo.isMapVisible():
				self.TechEffects[iTech].append(("MapReveal", -1))
			if TechInfo.isMapTrading():
				self.TechEffects[iTech].append(("MapTrading", -1))
			if TechInfo.isGoldTrading():
				self.TechEffects[iTech].append(("WealthTrading", -1))
			if TechInfo.isTechTrading():
				self.TechEffects[iTech].append(("TechTrading", -1))
			if TechInfo.getTradeRoutes():
				self.TechEffects[iTech].append(("TradeRoute", -1))
			if TechInfo.isOpenBordersTrading():
				self.TechEffects[iTech].append(("OpenBorders", -1))
			if TechInfo.isDefensivePactTrading():
				self.TechEffects[iTech].append(("DefensivePact", -1))
			if TechInfo.isPermanentAllianceTrading():
				self.TechEffects[iTech].append(("PermanentAlliance", -1))
			if TechInfo.isVassalStateTrading():
				self.TechEffects[iTech].append(("VassalStates", -1))
			if TechInfo.getHappiness():
				self.TechEffects[iTech].append(("Happiness", -1))
			if TechInfo.getHealth():
				self.TechEffects[iTech].append(("Health", -1))

			for iCommerceType in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
				if TechInfo.isCommerceFlexible(iCommerceType):
					self.TechEffects[iTech].append(("CommerceAdjust", iCommerceType))

			if TechInfo.getFirstFreeTechs():
				self.TechEffects[iTech].append(("FreeTech", -1))
			if TechInfo.getFirstFreeUnitClass() > -1:
				iUnit = utils.getUniqueUnitType(self.iPlayer, TechInfo.getFirstFreeUnitClass())
				if iUnit > -1:
					self.TechEffects[iTech].append(("FreeUnit", iUnit))
			if TechInfo.getHelp():
				self.TechEffects[iTech].append(("CustomEffect", -1))

		# Processes
		for iProcess in xrange(gc.getNumProcessInfos()):
			iTech = gc.getProcessInfo(iProcess).getTechPrereq()
			if iTech > -1:
				self.TechEffects[iTech].append(("Process", iProcess))

		# Religions
		for iReligion in xrange(gc.getNumReligionInfos()):
			iTech = gc.getReligionInfo(iReligion).getTechPrereq()
			if iTech > -1:
				self.TechEffects[iTech].append(("Religion", iReligion))
				
		self.TechEffects[iAcademia].append(("Religion", iProtestantism))



	def placeTechs(self):
		''
		if CyGame().isPitbossHost():
			return

		screen = self.getScreen()
		player = gc.getPlayer(self.iPlayer)
		team = gc.getTeam(player.getTeam())
		iCiv = player.getCivilizationType()

		ARROW_X = CyArtFileMgr().getInterfaceArtInfo("ARROW_X").getPath()
		ARROW_Y = CyArtFileMgr().getInterfaceArtInfo("ARROW_Y").getPath()
		ARROW_MXMY = CyArtFileMgr().getInterfaceArtInfo("ARROW_MXMY").getPath()
		ARROW_XY = CyArtFileMgr().getInterfaceArtInfo("ARROW_XY").getPath()
		ARROW_MXY = CyArtFileMgr().getInterfaceArtInfo("ARROW_MXY").getPath()
		ARROW_XMY = CyArtFileMgr().getInterfaceArtInfo("ARROW_XMY").getPath()
		ARROW_HEAD = CyArtFileMgr().getInterfaceArtInfo("ARROW_HEAD").getPath()

		for tech in xrange(gc.getNumTechInfos()):
			TechInfo = gc.getTechInfo(tech)
			if TechInfo.getEra() < self.iFromEra:
				continue
			if TechInfo.getEra() > self.iHideEra:
				continue
			if self.bResearched and team.isHasTech(tech):
				continue

			# Tech Box
			szTechBox = "TechBox" + str(tech)
			iX = (TechInfo.getGridX() - self.iMinX) * (self.BOX_X_SPACING + self.BOX_WIDTH)
			iY = (TechInfo.getGridY() - 1) * self.BOX_Y_SPACING
			screen.attachPanelAt("TechList", szTechBox, u"", u"", True, False, PanelStyles.PANEL_STYLE_TECH, iX, iY, self.BOX_WIDTH, self.BOX_HEIGHT, WidgetTypes.WIDGET_TECH_TREE, tech, -1)
			screen.setActivation(szTechBox, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS)

			# Tech Box Colour
			self.aiCurrentState[tech] = CIV_NO_RESEARCH
			if team.isHasTech(tech):
				self.aiCurrentState[tech] = CIV_HAS_TECH
			elif player.isResearchingTech(tech):
				self.aiCurrentState[tech] = CIV_IS_RESEARCHING
			elif player.canEverResearch(tech):
				self.aiCurrentState[tech] = CIV_TECH_AVAILABLE

			# Tech Icon
			iX = 6
			iY = 6
			szTechIconID = "TechButtonID" + str(tech)
			screen.addDDSGFCAt(szTechIconID, szTechBox, TechInfo.getButton(), iX + 6, iY + 6, self.TECH_ICON_SIZE, self.TECH_ICON_SIZE, WidgetTypes.WIDGET_TECH_TREE, tech, -1, False)
			screen.setActivation(szTechIconID, ActivationTypes.ACTIVATE_NORMAL)

		### Effects
			fX = self.X_ITEMS
			for index in xrange(len(self.TechEffects[tech])):
				type = self.TechEffects[tech][index][0]
				item = self.TechEffects[tech][index][1]
				szItem = "Item" + str(tech * 1000 + index)
				szObsolete = "Obsolete" + str(tech * 1000 + index)

				if type == "Civic":
					screen.addDDSGFCAt(szItem, szTechBox, gc.getCivicInfo(item).getButton(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, item, 1, False)

				elif type == "Tenet":
					screen.addDDSGFCAt(szItem, szTechBox, gc.getCivicInfo(item).getButton(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TENET, item, 1, False)

				elif type == "Religion":
					if CyGame().isOption(GameOptionTypes.GAMEOPTION_PICK_RELIGION):
						szButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_POPUPBUTTON_RELIGION").getPath()
					else:
						szButton = gc.getReligionInfo(item).getButton()
					screen.addDDSGFCAt(szItem, szTechBox, szButton, iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_FOUND_RELIGION, tech, item, False)

				elif type == "Unit":
					if self.bBuilt and not team.isHasTech(tech):
						iClass = gc.getUnitInfo(item).getUnitClassType()
						iLimit = gc.getUnitClassInfo(iClass).getMaxGlobalInstances()
						if iLimit > -1 and CyGame().getUnitClassCreatedCount(iClass) >= iLimit:
							continue

					screen.addDDSGFCAt(szItem, szTechBox, gc.getUnitInfo(item).getButton(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, item, 1, True)

				elif type == "Promotion":
					screen.addDDSGFCAt(szItem, szTechBox, gc.getPromotionInfo(item).getButton(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, item, -1, False)

				elif type == "Building":
					if self.bBuilt and not team.isHasTech(tech):
						iClass = gc.getBuildingInfo(item).getBuildingClassType()
						iLimit = gc.getBuildingClassInfo(iClass).getMaxGlobalInstances()
						if iLimit > -1 and CyGame().getBuildingClassCreatedCount(iClass) >= iLimit:
							continue

					screen.addDDSGFCAt(szItem, szTechBox, gc.getBuildingInfo(item).getButton(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item, -1, True)

				elif type == "ObsoleteBuilding":
					screen.addDDSGFCAt(szItem, szTechBox, gc.getBuildingInfo(item).getButton(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE, item, -1, False)
					screen.addDDSGFCAt(szObsolete, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE, item, -1, False)

				elif type == "SpecialBuilding":
					screen.addDDSGFCAt(szItem, szTechBox, gc.getSpecialBuildingInfo(item).getButton(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_SPECIAL_BUILDING, tech, item, False)

				elif type == "ObsoleteSpecialBuilding":
					screen.addDDSGFCAt(szItem, szTechBox, gc.getSpecialBuildingInfo(item).getButton(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_SPECIAL, item, -1, False)
					screen.addDDSGFCAt(szObsolete, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_SPECIAL, item, -1, False)

				elif type == "Project":
					if self.bBuilt and not team.isHasTech(tech):
						iLimit = gc.getProjectInfo(item).getMaxGlobalInstances()
						if iLimit > -1 and CyGame().getProjectCreatedCount(item) >= iLimit:
							continue

					screen.addDDSGFCAt(szItem, szTechBox, gc.getProjectInfo(item).getButton(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, item, 1, False)

				elif type == "Corporation":
					if self.bBuilt and not team.isHasTech(tech):
						if CyGame().isCorporationFounded(item):
							continue

					screen.addDDSGFCAt(szItem, szTechBox, gc.getCorporationInfo(item).getButton(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, item, 1, False)

				elif type == "Improvement":
					screen.addDDSGFCAt(szItem, szTechBox, gc.getBuildInfo(item).getButton(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_IMPROVEMENT, tech, item, False)

				elif type == "ImprovementYield":
					screen.addDDSGFCAt(szItem, szTechBox, gc.getImprovementInfo(item).getButton(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_YIELD_CHANGE, tech, item, False)

				elif type == "RevealResource":
					screen.addDDSGFCAt(szItem, szTechBox, gc.getBonusInfo(item).getButton(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_BONUS_REVEAL, tech, item, False)

				elif type == "ObsoleteResource":
					screen.addDDSGFCAt(szItem, szTechBox, gc.getBonusInfo(item).getButton(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_BONUS, item, -1, False)
					screen.addDDSGFCAt(szObsolete, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_BONUS, item, -1, False)

				elif type == "ResourceTrade":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_GOLDTRADING").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_BONUS_PLAYER_TRADE, tech, -1, False)
					
				elif type == "EnableIrrigation":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_IRRIGATION").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_IRRIGATION, tech, -1, False)

				elif type == "IgnoreIrrigation":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_NOIRRIGATION").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_IGNORE_IRRIGATION, tech, -1, False)

				elif type == "WorkerSpeed":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_WORKER_SPEED").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_WORKER_RATE, tech, -1, False)

				elif type == "FeatureProduction":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_FEATURE_PRODUCTION").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_FEATURE_PRODUCTION, tech, -1, False)

				elif type == "RouteMovement":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MOVE_BONUS").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_MOVE_BONUS, tech, -1, False)

				elif type == "BridgeBuilding":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_BRIDGEBUILDING").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_BUILD_BRIDGE, tech, -1, False)

				elif type == "RiverTrade":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_RIVERTRADE").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, tech, gc.getNumTerrainInfos(), False)

				elif type == "WaterTrade":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_WATERTRADE").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, tech, item, False)

				elif type == "WaterWork":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_WATERWORK").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_WATER_WORK, tech, -1, False)

				elif type == "WaterSight":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_LOS").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_LOS_BONUS, tech, -1, False)

				elif type == "WaterMoves":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_WATERMOVES").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_DOMAIN_EXTRA_MOVES, tech, item, False)

				elif type == "MapCenter":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MAPCENTER").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_MAP_CENTER, tech, -1, False)

				elif type == "MapReveal":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MAPREVEAL").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_MAP_REVEAL, tech, -1, False)

				elif type == "MapTrading":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MAPTRADING").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_MAP_TRADE, tech, -1, False)

				elif type == "WealthTrading":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_GOLDTRADING").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_GOLD_TRADE, tech, -1, False)

				elif type == "TechTrading":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_TECHTRADING").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_TECH_TRADE, tech, -1, False)

				elif type == "TradeRoute":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_TRADE_ROUTES").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_TRADE_ROUTES, tech, -1, False)

				elif type == "OpenBorders":
					screen.addDDSGFCAt(szItem , szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_OPENBORDERS").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_OPEN_BORDERS, tech, -1, False)

				elif type == "DefensivePact":
					screen.addDDSGFCAt(szItem , szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_DEFENSIVEPACT").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_DEFENSIVE_PACT, tech, -1, False)

				elif type == "PermanentAlliance":
					screen.addDDSGFCAt(szItem , szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_PERMALLIANCE").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_PERMANENT_ALLIANCE, tech, -1, False)

				elif type == "VassalStates":
					screen.addDDSGFCAt(szItem , szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_VASSAL").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_VASSAL_STATE, tech, -1, False)

				elif type == "Happiness":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_HAPPINESS").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_HAPPINESS_RATE, tech, -1, False)

				elif type == "Health":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_HEALTH").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_HEALTH_RATE, tech, -1, False)

				elif type == "CommerceAdjust":
						szFileName = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath()
						if item in [CommerceTypes.COMMERCE_GOLD, CommerceTypes.COMMERCE_RESEARCH, CommerceTypes.COMMERCE_CULTURE]:
							szFileName = gc.getProcessInfo(item).getButton()
						elif item == CommerceTypes.COMMERCE_ESPIONAGE:
							szFileName = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_ESPIONAGE").getPath()
						screen.addDDSGFCAt(szItem, szTechBox, szFileName, iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_ADJUST, tech, item, False)

				elif type == "Process":
					screen.addDDSGFCAt(szItem, szTechBox, gc.getProcessInfo(item).getButton(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_PROCESS_INFO, tech, item, False)

				elif type == "FreeTech":
					screen.addDDSGFCAt(szItem, szTechBox, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_FREETECH").getPath(), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_FREE_TECH, tech, -1, False)

				elif type == "FreeUnit":
					if gc.getUnitInfo(item).getEspionagePoints() == 0 or not CyGame().isOption(GameOptionTypes.GAMEOPTION_NO_ESPIONAGE):
						screen.addDDSGFCAt(szItem, szTechBox, player.getUnitButton(item), iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_FREE_UNIT, item, tech, False)

				elif type == "CustomEffect":
					szFileName = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath()
					screen.addDDSGFCAt(szItem, szTechBox, szFileName, iX + fX, iY + self.Y_ITEMS, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_PYTHON, 7800, tech, False)

				fX += self.X_INCREMENT

			fX = self.BOX_WIDTH - (self.PIXEL_INCREMENT * 2)

		###	Crosslinks
			for j in xrange(gc.getNUM_OR_TECH_PREREQS()):
				iPrereq = TechInfo.getPrereqOrTechs(j)
				if iPrereq == -1:
					break

				fX -= self.X_INCREMENT
				szTechPrereqID = "TechPrereqID" + str((tech * 1000) + j)
				screen.addDDSGFCAt(szTechPrereqID, szTechBox, gc.getTechInfo(iPrereq).getButton(), iX + fX, iY + 5, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_HELP_TECH_PREPREQ, iPrereq, -1, False)

		### Arrows
			for j in xrange(gc.getNUM_AND_TECH_PREREQS()):
				iPrereq = TechInfo.getPrereqAndTechs(j)
				if iPrereq == -1:
					break

				eInfo = gc.getTechInfo(iPrereq)
				if eInfo.getEra() < self.iFromEra:
					continue
				if eInfo.getEra() > self.iHideEra:
					continue
				if self.bResearched and team.isHasTech(iPrereq):
					continue

				iX = (eInfo.getGridX() - self.iMinX) * (self.BOX_X_SPACING + self.BOX_WIDTH) + self.BOX_WIDTH - 6
				iY = (eInfo.getGridY() -1) * self.BOX_Y_SPACING - 6
				xDiff = TechInfo.getGridX() - gc.getTechInfo(iPrereq).getGridX()
				yDiff = TechInfo.getGridY() - gc.getTechInfo(iPrereq).getGridY()

				if yDiff == 0:
					screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX, iY + self.getYStart(3), self.getWidth(xDiff), 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
					screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_HEAD, iX + self.getWidth(xDiff), iY + self.getYStart(3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)

				elif yDiff < 0:
					if yDiff == -6:
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX, iY + self.getYStart(1), self.getWidth(xDiff) / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_XY, iX + (self.getWidth(xDiff) / 2 ), iY + self.getYStart(1), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_Y, iX + (self.getWidth(xDiff) / 2 ), iY + self.getYStart(1) + 8 - self.getHeight(yDiff, 0), 8, self.getHeight(yDiff, 0) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_XMY, iX + (self.getWidth(xDiff) / 2 ), iY + self.getYStart(1) - self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + 8 + (self.getWidth(xDiff) / 2 ), iY + self.getYStart(1) - self.getHeight(yDiff, 0), (self.getWidth(xDiff) / 2 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_HEAD, iX + self.getWidth(xDiff), iY + self.getYStart(1) - self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)

					elif yDiff == -2 and xDiff == 2:
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX, iY + self.getYStart(2), self.getWidth(xDiff) * 5 / 6, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_XY, iX + (self.getWidth(xDiff) * 5 / 6 ), iY + self.getYStart(2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_Y, iX + (self.getWidth(xDiff) * 5 / 6 ), iY + self.getYStart(2) + 8 - self.getHeight(yDiff, 3), 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_XMY, iX + (self.getWidth(xDiff) * 5 / 6 ), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + 8 + (self.getWidth(xDiff) * 5 / 6 ), iY + self.getYStart(2) - self.getHeight(yDiff, 3), (self.getWidth(xDiff) / 6 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_HEAD, iX + self.getWidth(xDiff), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)

					else:
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX, iY + self.getYStart(2), self.getWidth(xDiff) / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_XY, iX + (self.getWidth(xDiff) / 2 ), iY + self.getYStart(2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_Y, iX + (self.getWidth(xDiff) / 2 ), iY + self.getYStart(2) + 8 - self.getHeight(yDiff, 3), 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_XMY, iX + (self.getWidth(xDiff) / 2 ), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + 8 + (self.getWidth(xDiff) / 2 ), iY + self.getYStart(2) - self.getHeight(yDiff, 3), (self.getWidth(xDiff) / 2 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_HEAD, iX + self.getWidth(xDiff), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)

				else:
					if yDiff == 2 and xDiff == 2:
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + self.BOX_WIDTH, iY + self.getYStart(4), self.getWidth(xDiff) / 6, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_MXMY, iX + self.BOX_WIDTH + (self.getWidth(xDiff) / 6 ), iY + self.getYStart(4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_Y, iX + self.BOX_WIDTH + (self.getWidth(xDiff) / 6 ), iY + self.getYStart(4) + 8, 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_MXY, iX + self.BOX_WIDTH + (self.getWidth(xDiff) / 6 ), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + 8 + self.BOX_WIDTH + (self.getWidth(xDiff) / 6 ), iY + self.getYStart(4) + self.getHeight(yDiff, 3), (self.getWidth(xDiff) * 5 / 6 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_HEAD, iX + self.BOX_WIDTH + self.getWidth(xDiff), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)

					elif yDiff == 4 and xDiff == 1:
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX, iY + self.getYStart(5), self.getWidth(xDiff) / 3, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_MXMY, iX + (self.getWidth(xDiff) / 3 ), iY + self.getYStart(5), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_Y, iX + (self.getWidth(xDiff) / 3 ), iY + self.getYStart(5) + 8, 8, self.getHeight(yDiff, 0) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_MXY, iX + (self.getWidth(xDiff) / 3 ), iY + self.getYStart(5) + self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + 8 + (self.getWidth(xDiff) / 3 ), iY + self.getYStart(5) + self.getHeight(yDiff, 0), (self.getWidth(xDiff) * 2 / 3 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_HEAD, iX + self.getWidth(xDiff), iY + self.getYStart(5) + self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)

					else:
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX, iY + self.getYStart(4), self.getWidth(xDiff) / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_MXMY, iX + (self.getWidth(xDiff) / 2 ), iY + self.getYStart(4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_Y, iX + (self.getWidth(xDiff) / 2 ), iY + self.getYStart(4) + 8, 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_MXY, iX + (self.getWidth(xDiff) / 2 ), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + 8 + (self.getWidth(xDiff) / 2 ), iY + self.getYStart(4) + self.getHeight(yDiff, 3), (self.getWidth(xDiff) / 2 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_HEAD, iX + self.getWidth(xDiff), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)

		screen.show("TechList")
		screen.setFocus("TechList")
		self.updateTechs(True)



	def updateTechs(self, bForce):
		if CyGame().isPitbossHost():
			return

		screen = self.getScreen()
		player = gc.getPlayer(self.iPlayer)
		team = gc.getTeam(player.getTeam())

		ChangedList = []
		for tech in xrange(gc.getNumTechInfos()):
			TechInfo = gc.getTechInfo(tech)
			if TechInfo.getEra() < self.iFromEra:
				continue
			if TechInfo.getEra() > self.iHideEra:
				continue
			if self.bResearched and team.isHasTech(tech):
				continue

			if team.isHasTech(tech):
				if self.aiCurrentState[tech] != CIV_HAS_TECH or bForce:
					self.aiCurrentState[tech] = CIV_HAS_TECH
					ChangedList.append(tech)
			elif player.isResearchingTech(tech):
				self.aiCurrentState[tech] = CIV_IS_RESEARCHING
				ChangedList.append(tech)
			elif player.canEverResearch(tech):
				if self.aiCurrentState[tech] != CIV_TECH_AVAILABLE or bForce:
					self.aiCurrentState[tech] = CIV_TECH_AVAILABLE
					ChangedList.append(tech)
			else:
				if self.aiCurrentState[tech] != CIV_NO_RESEARCH or bForce:
					self.aiCurrentState[tech] = CIV_NO_RESEARCH
					ChangedList.append(tech)

		for tech in ChangedList:
			TechInfo = gc.getTechInfo(tech)
			iX = (gc.getTechInfo(tech).getGridX() - self.iMinX) * (self.BOX_X_SPACING + self.BOX_WIDTH)
			iY = (gc.getTechInfo(tech).getGridY() - 1) * self.BOX_Y_SPACING

			# Tech Description
			szTechID = "TechID" + str(tech)
			szText = ""
			iQueue = player.getQueuePosition(tech)
			if player.isResearchingTech(tech):
				szText += str(iQueue) + ". "
			szText += TechInfo.getDescription()
			screen.setTextAt(szTechID, "TechList", szText, CvUtil.FONT_LEFT_JUSTIFY, iX + self.TECH_ICON_SIZE + 12, iY + 12, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_TECH_TREE, tech, -1)
			screen.setActivation(szTechID, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS)
			screen.setHitTest(szTechID, HitTestTypes.HITTEST_NOHIT)

			# Tech Box Colours
			szTechBox = "TechBox" + str(tech)
			if gc.getTeam(player.getTeam()).isHasTech(tech):
				screen.setPanelColor(szTechBox, 100, 150, 200)
			elif player.isResearchingTech(tech):
				screen.setPanelColor(szTechBox, 200, 175, 0)
			elif player.canEverResearch(tech):
				if TechInfo.getEra() == 0:
					screen.setPanelColor(szTechBox, 40, 100, 35)
				if TechInfo.getEra() == 1:
					screen.setPanelColor(szTechBox, 150, 100, 35)
				if TechInfo.getEra() == 2:
					screen.setPanelColor(szTechBox, 80, 70, 60)
				if TechInfo.getEra() == 3:
					screen.setPanelColor(szTechBox, 40, 40, 115)
				if TechInfo.getEra() == 4:
					screen.setPanelColor(szTechBox, 100, 100, 100)
				if TechInfo.getEra() == 5:
					screen.setPanelColor(szTechBox, 80, 40, 100)
				if TechInfo.getEra() == 6:
					screen.setPanelColor(szTechBox, 40, 40, 100)

			# Progress Bars
			szProgress = "Progress" + str(tech)
			screen.hide(szProgress)
			if player.isResearchingTech(tech) and iQueue == 1:
				screen.addStackedBarGFCAt(szProgress, "TechList", iX + 6, iY + self.BOX_HEIGHT - 9, self.BOX_WIDTH - 12, 15, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setStackedBarColors(szProgress, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RESEARCH_STORED"))
				screen.setStackedBarColors(szProgress, InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_RESEARCH_RATE"))
				screen.setStackedBarColors(szProgress, InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))

				iProgress = team.getResearchProgress(tech)
				iThreshold = team.getResearchCost(tech)
				iRate = player.calculateResearchRate(tech)
				iOverflow = player.getOverflowResearch() * player.calculateResearchModifier(tech) / 100
				screen.setBarPercentage(szProgress, InfoBarTypes.INFOBAR_STORED, float(iProgress) / float(iThreshold))
				screen.setBarPercentage(szProgress, InfoBarTypes.INFOBAR_RATE, 0.0)
				if iThreshold > (iProgress + iOverflow):
					screen.setBarPercentage(szProgress, InfoBarTypes.INFOBAR_RATE, float(iRate) / (iThreshold - iProgress - iOverflow))



	def updateSelectedTech(self):
		''
		player = gc.getPlayer(CyGame().getActivePlayer())
		screen = self.getScreen()

		szName = ""
		iCost = 0
		if self.iSelectedTech > -1:
			iCost = gc.getPlayer(CyGame().getActivePlayer()).getAdvancedStartTechCost(self.iSelectedTech, True)

		screen.hide("AddTechButton")
		screen.hide("AddTechCost")
		if iCost > 0:
			szText = u"<font=3b>%d/%d%c</font>" % (iCost, player.getAdvancedStartPoints(), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
			screen.setLabel("AddTechCost", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_ADVANCED_START + self.W_ADVANCED_START + 25, self.Y_ADVANCED_START, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			if player.getAdvancedStartPoints() >= iCost:
				screen.show("AddTechButton")



	def placeGreatPeople(self):
		''
		if CyGame().isInAdvancedStart():
			return

		screen = self.getScreen()
		iGPX = 25

		for iUnit in self.GreatPeopleList:
			for iFlavor in xrange(gc.getNumFlavorTypes()):
				if gc.getUnitInfo(iUnit).getFlavorValue(iFlavor) > 0:
					break
					
			flavor = lambda x: gc.getTechInfo(x).getFlavorValue(iFlavor)

			lTechs = [i for i in xrange(gc.getNumTechInfos()) if gc.getPlayer(self.iPlayer).canResearch(i, False)]
			iFirstDiscovery = utils.getHighestEntry(lTechs, flavor)
			
			iSecondDiscovery = None
			if iFirstDiscovery:
				lTechsGiven = [i for i in xrange(gc.getNumTechInfos()) if gc.getPlayer(self.iPlayer).canResearchGiven(i, False, iFirstDiscovery) and i != iFirstDiscovery]
				iSecondDiscovery = utils.getHighestEntry(lTechsGiven, flavor)

			screen.addDDSGFCAt("GreatPeopleUnit" + str(iUnit),"TechBottomPanel", gc.getUnitInfo(iUnit).getButton(), iGPX, 16, self.GP_ICON_SIZE, self.GP_ICON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, -1, False)
			iGPX += self.GP_ICON_SIZE
			
			for i, iTech in enumerate([iFirstDiscovery, iSecondDiscovery]):
				if iTech:
					screen.addDDSGFCAt("GreatPeoplePrereq" + str(iUnit) + str(i),"TechBottomPanel", gc.getTechInfo(iTech).getButton(), iGPX, 16, self.GP_ICON_SIZE, self.GP_ICON_SIZE, WidgetTypes.WIDGET_TECH_TREE, iTech, -1, False)
				else:
					screen.addDDSGFCAt("GreatPeoplePrereq" + str(iUnit) + str(i),"TechBottomPanel", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), iGPX, 16, self.GP_ICON_SIZE, self.GP_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
				iGPX += self.GP_ICON_SIZE
			
			screen.addDDSGFCAt("GreatPeopleTechList" + str(iUnit),"TechBottomPanel", "Art/Interface/Buttons/TechList.dds", iGPX, 16, self.GP_ICON_SIZE, self.GP_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, 12001, iFlavor, False)
			iGPX += self.GP_ICON_SIZE * 2


	def getWidth(self, xDiff):
		return xDiff * self.BOX_X_SPACING + (xDiff - 1) * self.BOX_WIDTH



	def getHeight(self, yDiff, nFactor):
		return (nFactor + ((abs(yDiff) - 1) * 6)) * self.PIXEL_INCREMENT



	def getYStart(self, iY):
		return self.BOX_HEIGHT * iY / 6



	def getNextWidgetName(self):
		szName = "TechArrow" + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName



	def onClose(self):
		player = gc.getPlayer(self.iPlayer)
		if player.getAdvancedStartPoints() > -1:
			CyInterface().setDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT, True)
		return 0



	def handleInput(self, inputClass):
		screen = self.getScreen()
		player = gc.getPlayer(self.iPlayer)

		if inputClass.getButtonType() == WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC:
			CvScreensInterface.pediaJumpToCivic([inputClass.getData1()])
		elif inputClass.getButtonType() == WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING:
			CvScreensInterface.pediaJumpToBuilding([inputClass.getData1()])

		# Filters
		elif inputClass.getFunctionName().startswith("Filter"):
			if inputClass.getFunctionName() == "FilterFromEra":
				iIndex = screen.getSelectedPullDownID("FilterFromEra")
				self.iFromEra = screen.getPullDownData("FilterFromEra", iIndex)
			elif inputClass.getFunctionName() == "FilterToEra":
				iIndex = screen.getSelectedPullDownID("FilterToEra")
				self.iHideEra = screen.getPullDownData("FilterToEra", iIndex)
			elif inputClass.getFunctionName() == "FilterResearched":
				self.bResearched = not self.bResearched
			elif inputClass.getFunctionName() == "FilterBuilt":
				self.bBuilt = not self.bBuilt
			screen.setPersistent(False)
			self.interfaceScreen()
			return

		# Debug
		elif inputClass.getFunctionName() == "CivDropDown":
			iIndex = screen.getSelectedPullDownID("CivDropDown")
			self.iPlayer = screen.getPullDownData("CivDropDown", iIndex)
			screen.setPersistent(False)
			self.interfaceScreen()
			return

		# Advanced Start
		#if player.getAdvancedStartPoints() > -1:
		#	if inputClass.getFunctionName() == "AddTechButton":
		#		if player.getAdvancedStartTechCost(self.iSelectedTech, True) != -1:
		#			CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_TECH, self.iPlayer, -1, -1, self.iSelectedTech, True)
		#			self.bTechBoxesDirty = True
		#			self.bSelectedTechDirty = True

		#	elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
		#		if inputClass.getButtonType() == WidgetTypes.WIDGET_TECH_TREE:
		#			self.iSelectedTech = inputClass.getData1()
		#			self.updateSelectedTech()

		return 0



	def update(self, fDelta):
		if CyInterface().isDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT):
			CyInterface().setDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT, False)

			if self.bSelectedTechDirty:
				self.bSelectedTechDirty = False
				self.updateSelectedTech()

			if self.bTechBoxesDirty:
				self.bTechBoxesDirty = False
				self.updateTechs(True)

			if gc.getPlayer(self.iPlayer).getAdvancedStartPoints() < 0:
				screen = self.getScreen()
				screen.hide("AddTechButton")
				screen.hide("AddTechCost")

		return
