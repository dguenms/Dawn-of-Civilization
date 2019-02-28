from CvPythonExtensions import *
from CvScreenEnums import *
import string

import CvUtil
import ScreenInput

import CvPediaScreen
import CvPediaCivilization
import CvPediaLeader
import CvPediaCivic
import CvPediaReligion
import CvPediaCorporation
import CvPediaSpecialist
import CvPediaTech
import CvPediaUnit
import CvPediaUnitChart
import CvPediaPromotion
import CvPediaBuilding
import CvPediaProject
import CvPediaTerrain
import CvPediaFeature
import CvPediaResource
import CvPediaImprovement
import CvPediaRoute
import CvPediaCultureLevel
import CvPediaConcepts

import BugUtil
import TraitUtil
import UnitUpgradesGraph

from RFCUtils import utils
from Consts import *

gc = CyGlobalContext()
g_TraitUtilInitDone = False



class CvPediaMain(CvPediaScreen.CvPediaScreen):
	def __init__(self):
		self.PEDIA_MAIN_SCREEN	= "PediaMainScreen"
		self.INTERFACE_ART_INFO	= "SCREEN_BG_OPAQUE"

		self.WIDGET_ID			= "PediaMainWidget"
		self.BACKGROUND_ID		= "PediaMainBackground"
		self.TOP_PANEL_ID		= "PediaMainTopPanel"
		self.BOT_PANEL_ID		= "PediaMainBottomPanel"
		self.HEAD_ID			= "PediaMainHeader"
		self.BACK_ID			= "PediaMainBack"
		self.NEXT_ID			= "PediaMainForward"
		self.EXIT_ID			= "PediaMainExit"
		self.CATEGORY_LIST_ID	= "PediaMainCategoryList"
		self.ITEM_LIST_ID		= "PediaMainItemList"
		self.UPGRADES_GRAPH_ID	= "PediaMainUpgradesGraph"

		self.W_SCREEN = 1024
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

		self.X_CATEGORIES = 0
		self.Y_CATEGORIES = self.Y_TOP_PANEL + self.H_TOP_PANEL - 4
		self.W_CATEGORIES = 190
		self.H_CATEGORIES = self.Y_BOTTOM_PANEL + 3 - self.Y_CATEGORIES

		self.X_ITEMS = self.X_CATEGORIES + self.W_CATEGORIES + 2
		self.Y_ITEMS = self.Y_CATEGORIES
		self.W_ITEMS = 190
		self.H_ITEMS = self.H_CATEGORIES

		self.X_PEDIA_PAGE = self.X_ITEMS + self.W_ITEMS + 18
		self.Y_PEDIA_PAGE = self.Y_ITEMS + 13
		self.R_PEDIA_PAGE = self.W_SCREEN - 20
		self.B_PEDIA_PAGE = self.Y_ITEMS + self.H_ITEMS - 16
		self.W_PEDIA_PAGE = self.R_PEDIA_PAGE - self.X_PEDIA_PAGE
		self.H_PEDIA_PAGE = self.B_PEDIA_PAGE - self.Y_PEDIA_PAGE

		self.X_BACK = self.X_BOTTOM_PANEL + 25
		self.Y_BACK = self.Y_BOTTOM_PANEL + 20

		self.X_NEXT = self.X_ITEMS + 25
		self.Y_NEXT = self.Y_BOTTOM_PANEL + 20

		self.X_EXIT = self.W_BOTTOM_PANEL - 25
		self.Y_EXIT = self.Y_BOTTOM_PANEL + 20

		self.tab = None
		self.iActivePlayer = -1
		self.nWidgetCount = 0

		self.categoryList = []
		self.categoryGraphics = []
		self.iCategory = -1
		self.iItem = -1
		self.iItemIndex = -1
		self.pediaHistory = []
		self.pediaFuture = []

		self.mapListGenerators = {
			PEDIA_CIVS			: self.placeCivs,
			PEDIA_LEADERS			: self.placeLeaders,
			PEDIA_CIVICS			: self.placeCivics,
			PEDIA_RELIGIONS			: self.placeReligions,
			PEDIA_CORPORATIONS		: self.placeCorporations,
			PEDIA_SPECIALISTS		: self.placeSpecialists,
			PEDIA_TECHS			: self.placeTechs,
			PEDIA_CULTURE_LEVELS		: self.placeCultureLevels,
			PEDIA_UNITS			: self.placeUnits,
			PEDIA_MILITARY_UNITS		: self.placeMilitaryUnits,
			PEDIA_UNIQUE_UNITS		: self.placeUniqueUnits,
			PEDIA_UNIT_CATEGORIES		: self.placeUnitCharts,
			PEDIA_UNIT_UPGRADES		: self.placeUnitUpgrades,
			PEDIA_PROMOTIONS		: self.placePromotions,
			PEDIA_PROMOTION_TREE		: self.placePromotionTree,
			PEDIA_BUILDINGS			: self.placeBuildings,
			PEDIA_RELIGIOUS_BUILDINGS	: self.placeReligiousBuildings,
			PEDIA_UNIQUE_BUILDINGS		: self.placeUniqueBuildings,
			PEDIA_GREAT_PEOPLE_BUILDINGS	: self.placeGreatPeopleBuildings,
			PEDIA_NATIONAL_WONDERS		: self.placeNationalWonders,
			PEDIA_GREAT_WONDERS		: self.placeGreatWonders,
			PEDIA_PROJECTS			: self.placeProjects,
			PEDIA_TERRAINS			: self.placeTerrains,
			PEDIA_FEATURES			: self.placeFeatures,
			PEDIA_RESOURCES			: self.placeResources,
			PEDIA_IMPROVEMENTS		: self.placeImprovements,
			PEDIA_ROUTES			: self.placeRoutes,
			PEDIA_CONCEPTS			: self.placeConcepts,
			PEDIA_HINTS			: self.placeHints,
			PEDIA_SHORTCUTS  		: self.placeShortcuts,
			}

		self.pediaLeader	= CvPediaLeader.CvPediaLeader(self)
		self.pediaBuilding	= CvPediaBuilding.CvPediaBuilding(self)
		self.pediaUnit		= CvPediaUnit.CvPediaUnit(self)
		self.pediaFeature	= CvPediaFeature.CvPediaFeature(self)

		self.mapScreenFunctions = {
			PEDIA_CIVS			: CvPediaCivilization.CvPediaCivilization(self),
			PEDIA_LEADERS			: self.pediaLeader,
			PEDIA_CIVICS			: CvPediaCivic.CvPediaCivic(self),
			PEDIA_RELIGIONS			: CvPediaReligion.CvPediaReligion(self),
			PEDIA_CORPORATIONS		: CvPediaCorporation.CvPediaCorporation(self),
			PEDIA_SPECIALISTS		: CvPediaSpecialist.CvPediaSpecialist(self),
			PEDIA_TECHS			: CvPediaTech.CvPediaTech(self),
			PEDIA_CULTURE_LEVELS		: CvPediaCultureLevel.CvPediaCultureLevel(self),
			PEDIA_UNITS			: CvPediaUnit.CvPediaUnit(self),
			PEDIA_MILITARY_UNITS		: CvPediaUnit.CvPediaUnit(self),
			PEDIA_UNIQUE_UNITS		: CvPediaUnit.CvPediaUnit(self),
			PEDIA_UNIT_CATEGORIES		: CvPediaUnitChart.CvPediaUnitChart(self),
			PEDIA_PROMOTIONS		: CvPediaPromotion.CvPediaPromotion(self),
			PEDIA_BUILDINGS			: self.pediaBuilding,
			PEDIA_RELIGIOUS_BUILDINGS	: CvPediaBuilding.CvPediaBuilding(self),
			PEDIA_UNIQUE_BUILDINGS		: CvPediaBuilding.CvPediaBuilding(self),
			PEDIA_GREAT_PEOPLE_BUILDINGS	: CvPediaBuilding.CvPediaBuilding(self),
			PEDIA_NATIONAL_WONDERS		: CvPediaBuilding.CvPediaBuilding(self),
			PEDIA_GREAT_WONDERS		: CvPediaBuilding.CvPediaBuilding(self),
			PEDIA_PROJECTS			: CvPediaProject.CvPediaProject(self),
			PEDIA_TERRAINS			: CvPediaTerrain.CvPediaTerrain(self),
			PEDIA_FEATURES			: CvPediaFeature.CvPediaFeature(self),
			PEDIA_RESOURCES			: CvPediaResource.CvPediaResource(self),
			PEDIA_IMPROVEMENTS		: CvPediaImprovement.CvPediaImprovement(self),
			PEDIA_ROUTES			: CvPediaRoute.CvPediaRoute(self),
			PEDIA_CONCEPTS			: CvPediaConcepts.CvPediaConcepts(self),
			PEDIA_HINTS			: CvPediaConcepts.CvPediaConcepts(self),
			PEDIA_SHORTCUTS  		: CvPediaConcepts.CvPediaConcepts(self),
			}



	def getScreen(self):
		return CyGInterfaceScreen(self.PEDIA_MAIN_SCREEN, PEDIA_MAIN)



	def createScreen(self, screen):
		if screen.isActive():
			return

		screen.setRenderInterfaceOnly(True)
		screen.setScreenGroup(1)
		screen.setDimensions((screen.getXResolution() / 2) - (self.W_SCREEN / 2), (screen.getYResolution() / 2) - (self.H_SCREEN / 2), self.W_SCREEN, self.H_SCREEN)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.addDDSGFC(self.BACKGROUND_ID, CyArtFileMgr().getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel(self.TOP_PANEL_ID, u"", u"", True, False, self.X_TOP_PANEL, self.Y_TOP_PANEL, self.W_TOP_PANEL, self.H_TOP_PANEL, PanelStyles.PANEL_STYLE_TOPBAR)
		screen.addPanel(self.BOT_PANEL_ID, u"", u"", True, False, self.X_BOTTOM_PANEL, self.Y_BOTTOM_PANEL, self.W_BOTTOM_PANEL, self.H_BOTTOM_PANEL, PanelStyles.PANEL_STYLE_BOTTOMBAR)

		screen.setText(self.HEAD_ID, "Background", u"<font=4b>CIVILOPEDIA</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_TITLE, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText(self.BACK_ID, "Background", u"<font=4>BACK</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_BACK, self.Y_BACK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_BACK, 1, -1)
		screen.setText(self.NEXT_ID, "Background", u"<font=4>NEXT</font>", CvUtil.FONT_LEFT_JUSTIFY,   self.X_NEXT,  self.Y_NEXT,  0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_FORWARD, 1, -1)
		screen.setText(self.EXIT_ID, "Background", u"<font=4>EXIT</font>", CvUtil.FONT_RIGHT_JUSTIFY,  self.X_EXIT,  self.Y_EXIT,  0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

		self.szCategoryCivs			= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIV", ())
		self.szCategoryLeaders			= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_LEADER", ())
		self.szCategoryCivics			= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIVIC", ())
		self.szCategoryReligions		= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ())
		self.szCategoryCorporations		= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CORPORATIONS", ())
		self.szCategorySpecialists		= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_SPECIALIST", ())
		self.szCategoryTechs			= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH", ())
		self.szCategoryUnits			= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ())
		self.szCategoryMilitaryUnits		= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_MILITARY_UNITS", ())
		self.szCategoryUniqueUnits		= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIQUE_UNITS", ())
		self.szCategoryUnitCategories		= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT_CHARTS", ())
		self.szCategoryUnitUpgrades		= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT_UPGRADES", ())
		self.szCategoryPromotions		= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ())
		self.szCategoryPromotionTree		= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION_TREE", ())
		self.szCategoryBuildings		= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ())
		self.szCategoryReligiousBuildings	= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGIOUS_BUILDINGS", ())
		self.szCategoryUniqueBuildings		= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIQUE_BUILDINGS", ())
		self.szCategoryGreatPeopleBuildings	= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_GREAT_PEOPLE_BUILDINGS", ())
		self.szCategoryNationalWonders		= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_NATIONAL_WONDERS", ())
		self.szCategoryGreatWonders		= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_WORLD_WONDERS", ())
		self.szCategoryProjects			= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ())
		self.szCategoryTerrains			= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TERRAIN", ())
		self.szCategoryFeatures			= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_FEATURE", ())
		self.szCategoryBonuses			= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ())
		self.szCategoryImprovements		= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ())
		self.szCategoryRoutes			= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_ROUTE", ())
		self.szCategoryCultureLevels		= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CULTURE_LEVELS", ())
		self.szCategoryConcepts			= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CONCEPTS", ())
		self.szCategoryHints			= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_HINTS", ())
		self.szCategoryShortcuts		= CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_SHORTCUTS", ())

		self.categoryList = [
			["CIVS",		self.szCategoryCivs],
			["CIVS",		self.szCategoryLeaders],
			["CIVICS",		self.szCategoryCivics],
			["RELIGIONS",		self.szCategoryReligions],
			["CORPORATIONS",	self.szCategoryCorporations],
			["SPECIALISTS",		self.szCategorySpecialists],
			["TECHS",		self.szCategoryTechs],
			["CULTURE",		self.szCategoryCultureLevels],
			["UNITS",		self.szCategoryUnits],
			["UNITS",		self.szCategoryMilitaryUnits],
			["UNITS",		self.szCategoryUniqueUnits],
			["UNITS",		self.szCategoryUnitCategories],
			["UNITS",		self.szCategoryUnitUpgrades],
			["PROMOTIONS",		self.szCategoryPromotions],
			["PROMOTIONS",		self.szCategoryPromotionTree],
			["BUILDINGS",		self.szCategoryBuildings],
			["BUILDINGS",		self.szCategoryReligiousBuildings],
			["BUILDINGS",		self.szCategoryUniqueBuildings],
			["BUILDINGS",		self.szCategoryGreatPeopleBuildings],
			["BUILDINGS",		self.szCategoryNationalWonders],
			["BUILDINGS",		self.szCategoryGreatWonders],
			["BUILDINGS",		self.szCategoryProjects],
			["TERRAINS",		self.szCategoryTerrains],
			["TERRAINS",		self.szCategoryFeatures],
			["TERRAINS",		self.szCategoryBonuses],
			["TERRAINS",		self.szCategoryImprovements],
			["TERRAINS",		self.szCategoryRoutes],
			["HINTS",		self.szCategoryConcepts],
			["HINTS",		self.szCategoryHints],
			["HINTS",		self.szCategoryShortcuts],
			]

		self.categoryGraphics = {
			"CIVS"		: u"%c  " % CyGame().getSymbolID(FontSymbols.MAP_CHAR),
			"CIVICS"	: u"%c  " % CyGame().getSymbolID(FontSymbols.GOLDEN_AGE_CHAR),
			"RELIGIONS"	: u"%c  " % CyGame().getSymbolID(FontSymbols.RELIGION_CHAR),
			"CORPORATIONS"	: u"%c  " % gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar(),
			"SPECIALISTS"	: u"%c  " % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR),
			"TECHS"		: u"%c  " % gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar(),
			"CULTURE"	: u"%c  " % gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(),
			"UNITS"		: u"%c  " % CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR),
			"PROMOTIONS"	: u"%c  " % CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR),
			"BUILDINGS"	: u"%c  " % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar(),
			"TERRAINS"	: u"%c  " % gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar(),
			"HINTS"		: u"%c  " % gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar(),
			}

		BugUtil.debug("Creating screen")
		self.iCategory = -1
		self.tab = None



	def pediaShow(self):
		global g_TraitUtilInitDone
		if not g_TraitUtilInitDone:
			TraitUtil.init()
			g_TraitUtilInitDone = True
		self.iActivePlayer = gc.getGame().getActivePlayer()
		self.iCategory = -1
		if not self.pediaHistory:
			self.pediaHistory.append((PEDIA_MAIN, PEDIA_CIVS))
		current = self.pediaHistory.pop()
		self.pediaFuture = []
		self.pediaHistory = []
		self.pediaJump(current[0], current[1], False, True)



	def pediaJump(self, iCategory, iItem, bRemoveFwdList, bIsLink):
		bAddToHistory = False
		if not self.pediaHistory:
			bAddToHistory = True
		elif iCategory != PEDIA_MAIN or iItem == PEDIA_UNIT_UPGRADES or iItem == PEDIA_PROMOTION_TREE:
			prev = self.pediaHistory[0]
			if prev[0] != iCategory or prev[1] != iItem:
				bAddToHistory = True
		if bAddToHistory:
			self.pediaHistory.append((iCategory, iItem))
		if bRemoveFwdList:
			self.pediaFuture = []

		screen = self.getScreen()
		if not screen.isActive():
			self.createScreen(screen)

		if iCategory == PEDIA_MAIN:
			BugUtil.debug("Main link %d" % iItem)
			self.showContents(bIsLink, iItem)
			screen.setSelectedListBoxStringGFC(self.CATEGORY_LIST_ID, iItem - (PEDIA_MAIN + 1))
			#self.iCategory = iItem
			return

		if iCategory == PEDIA_BUILDINGS:
			iCategory += utils.getBuildingCategory(iItem)
		elif iCategory == PEDIA_UNITS:
			iCategory += self.getUnitCategory(iItem)
		elif iCategory == PEDIA_BTS_CONCEPTS:
			iCategory = self.determineNewConceptSubCategory(iItem)
			BugUtil.debug("Switching to category %d" % iCategory)

		self.showContents(bIsLink, iCategory)
		screen.setSelectedListBoxStringGFC(self.CATEGORY_LIST_ID, iCategory - (PEDIA_MAIN + 1))
		if (iCategory not in (PEDIA_UNIT_UPGRADES, PEDIA_PROMOTION_TREE)):
			screen.enableSelect(self.ITEM_LIST_ID, True)
			if self.iItemIndex != -1:
				BugUtil.debug("Deselecting item %d" % self.iItemIndex)
				screen.selectRow(self.ITEM_LIST_ID, self.iItemIndex, False)
			BugUtil.debug("Selecting item %d" % iItem)
			self.iItem = iItem
			for i, item in enumerate(self.list):
				if (item[1] == iItem):
					BugUtil.debug("Selecting %dth item %d" % (i, iItem))
					#screen.setSelectedListBoxStringGFC(self.ITEM_LIST_ID, i)
					screen.selectRow(self.ITEM_LIST_ID, i, True)
					self.iItemIndex = i
					#break

		#self.iCategory = iCategory
		BugUtil.debug("Drawing screen %d item %d" % (iCategory, iItem))
		self.deleteAllWidgets()
		func = self.mapScreenFunctions.get(iCategory)
		func.interfaceScreen(iItem)



	def determineNewConceptSubCategory(self, iItem):
		info = gc.getNewConceptInfo(iItem)
		BugUtil.debug("NewConcept itme %d is %s" % (iItem, info.getDescription()))
		if (self.isTraitInfo(info)):
			return PEDIA_TRAITS
#		if (self.isStrategyInfo(info)):
#			return PEDIA_STRATEGY
		if (self.isShortcutInfo(info)):
			return PEDIA_SHORTCUTS
		return PEDIA_BTS_CONCEPTS



	def showContents(self, bForce=False, iCategory=PEDIA_TECHS):
		self.deleteAllWidgets()
		BugUtil.debug("Drawing category list")
		self.placeCategories(iCategory)
		screen = self.getScreen()
		screen.show(self.BACK_ID)
		screen.show(self.NEXT_ID)
		if self.iCategory != iCategory or bForce:
			BugUtil.debug("Drawing item list %d" % iCategory)
			self.mapListGenerators.get(iCategory)()
			self.iCategory = iCategory
			self.iItem = -1
			self.iItemIndex = -1



	def placeCategories(self, iCategory=None):
		screen = self.getScreen()
		screen.addListBoxGFC(self.CATEGORY_LIST_ID, "", self.X_CATEGORIES, self.Y_CATEGORIES, self.W_CATEGORIES, self.H_CATEGORIES, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.CATEGORY_LIST_ID, True)
		screen.setStyle(self.CATEGORY_LIST_ID, "Table_StandardCiv_Style")
		screen.clearListBoxGFC(self.CATEGORY_LIST_ID)
		for i, category in enumerate(self.categoryList):
			graphic = self.categoryGraphics[category[0]]
			szText = graphic + category[1]
			screen.appendListBoxStringNoUpdate(self.CATEGORY_LIST_ID, szText, WidgetTypes.WIDGET_PEDIA_MAIN, PEDIA_MAIN + i + 1, 0, CvUtil.FONT_LEFT_JUSTIFY)
		screen.updateListBox(self.CATEGORY_LIST_ID)



	def placeCivs(self):
		lCivilizations = []
		for iCivilization in xrange(gc.getNumCivilizationInfos()):
			CivilizationInfo = gc.getCivilizationInfo(iCivilization)
			
			if not CivilizationInfo.isPlayable():
				continue
			
			lCivilizations.append((CivilizationInfo.getText(), iCivilization))

		lCivilizations.sort()
		self.list = lCivilizations
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, gc.getCivilizationInfo)




	def placeLeaders(self):
		lLeaders = []
		for iLeader in xrange(gc.getNumLeaderHeadInfos()):
			if iLeader == gc.getInfoTypeForString('LEADER_BARBARIAN'):
				continue

			LeaderInfo = gc.getLeaderHeadInfo(iLeader)
			iCiv = utils.getLeaderCiv(iLeader)
			
			if not iCiv is None and gc.getCivilizationInfo(iCiv).isPlayable():
				lLeaders.append((LeaderInfo.getDescription(), iLeader))
			
			

		lLeaders.sort()
		self.list = lLeaders
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, gc.getLeaderHeadInfo)



	def placeTraits(self):
		self.list = self.getSortedList(gc.getNumNewConceptInfos(), self.getTraitInfo, True)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_DESCRIPTION, self.getTraitInfo)



	def placeCivics(self):
		lCivics = []
		iPrevCategory = -1
		for iCivic in xrange(gc.getNumCivicInfos()):
			CivicInfo = gc.getCivicInfo(iCivic)
			iCategory = CivicInfo.getCivicOptionType()
			if iCategory > -1 and iCategory != iPrevCategory:
				if lCivics != []:
					lCivics.append(("", -1))
				lCivics.append((gc.getCivicOptionInfo(iCategory).getDescription(), -1))
			lCivics.append((CivicInfo.getDescription(), iCivic))
			iPrevCategory = iCategory

		self.list = lCivics
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, gc.getCivicInfo)


	def placeReligions(self):
		self.list = self.getSortedList(gc.getNumReligionInfos(), gc.getReligionInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, gc.getReligionInfo)



	def placeCorporations(self):
		self.list = self.getSortedList(gc.getNumCorporationInfos(), gc.getCorporationInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, gc.getCorporationInfo)



	def placeSpecialists(self):
		lSpecialists = []
		hSpecialists = CyTranslator().getText("TXT_KEY_PEDIA_HEADER_SPECIALIST", ())
		lSatellites = []
		hSatellites = CyTranslator().getText("TXT_KEY_PEDIA_HEADER_SATELLITE", ())
		lGreatSpecialists = []
		hGreatSpecialists = CyTranslator().getText("TXT_KEY_PEDIA_HEADER_GREAT_SPECIALIST", ())

		for iSpecialist in xrange(gc.getNumSpecialistInfos()):
			SpecialistInfo = gc.getSpecialistInfo(iSpecialist)
			if SpecialistInfo.isGraphicalOnly():
				continue
			sSpecialist = SpecialistInfo.getType()
			if sSpecialist.find("GREAT_") > -1:
				lGreatSpecialists.append((SpecialistInfo.getDescription(), iSpecialist))
			elif SpecialistInfo.isSatellite():
				lSatellites.append((SpecialistInfo.getDescription(), iSpecialist))
			else:
				lSpecialists.append((SpecialistInfo.getDescription(), iSpecialist))

		lSpecialists.sort()
		lSatellites.sort()
		lGreatSpecialists.sort()
		lSpecialists.insert(0, (hSpecialists, -1))
		lSatellites.insert(0, (hSatellites, -1))
		lSatellites.insert(0, ("", -1))
		lGreatSpecialists.insert(0, (hGreatSpecialists, -1))
		lGreatSpecialists.insert(0, ("", -1))

		self.list = lSpecialists + lSatellites + lGreatSpecialists
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, gc.getSpecialistInfo)



	def placeTechs(self):
		self.list = self.getSortedList(gc.getNumTechInfos(), gc.getTechInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, gc.getTechInfo)



	def placeCultureLevels(self):
		self.list = self.getSortedList(gc.getNumCultureLevelInfos(), gc.getCultureLevelInfo, True)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_CULTURE_LEVEL, gc.getCultureLevelInfo)
		

	def placeUnits(self):
		UnitList 	= [("Support Units", -1)]
		GreatPeopleList	= [("Great People", -1)]
		ReligiousList 	= [("Religious Units", -1)]
		AnimalList	= [("Animals", -1)]

		for iUnit in xrange(gc.getNumUnitInfos()):
			if self.getUnitCategory(iUnit) == 0:
				UnitInfo = gc.getUnitInfo(iUnit)
				if UnitInfo.getBaseDiscover() > 0 or UnitInfo.getEspionagePoints() > 0 or UnitInfo.getLeaderExperience() > 0:
					GreatPeopleList.append((gc.getUnitInfo(iUnit).getDescription(), iUnit))
				elif UnitInfo.getPrereqReligion() > -1 or UnitInfo.isPersecute():
					ReligiousList.append((gc.getUnitInfo(iUnit).getDescription(), iUnit))
				elif UnitInfo.isAnimal():
					AnimalList.append((gc.getUnitInfo(iUnit).getDescription(), iUnit))
				else:
					UnitList.append((gc.getUnitInfo(iUnit).getDescription(), iUnit))

		UnitList.append(("", -1))
		GreatPeopleList.append(("", -1))
		ReligiousList.append(("", -1))

		self.list = UnitList + GreatPeopleList + ReligiousList + AnimalList
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, gc.getUnitInfo)



	def placeMilitaryUnits(self):
		UnitDict = {}
		self.list = []

		for iUnit in xrange(gc.getNumUnitInfos()):
			if self.getUnitCategory(iUnit) == 1:
				UnitInfo = gc.getUnitInfo(iUnit)
				iUnitCombat = UnitInfo.getUnitCombatType()
				if UnitInfo.getDomainType() == 0:
					if UnitInfo.getCargoSpace() == 0 or UnitInfo.getSpecialCargo() != -1:
						iUnitCombat = 97
					else:
						iUnitCombat = 98
				elif UnitInfo.isSuicide():
					iUnitCombat = 99
				if not iUnitCombat in UnitDict.keys():
					UnitDict[iUnitCombat] = []
					if iUnitCombat == -1:
						sHeader = "Needs Sorting"
					elif iUnitCombat == 97:
						sHeader = "Naval Combat Units"
					elif iUnitCombat == 98:
						sHeader = "Naval Transport Units"
					elif iUnitCombat == 99:
						sHeader = "Missiles"
					else:
						sHeader = gc.getUnitCombatInfo(iUnitCombat).getDescription()
					UnitDict[iUnitCombat].append((sHeader, -1))

				UnitDict[iUnitCombat].append((UnitInfo.getDescription(), iUnit))

		keylist = UnitDict.keys()
		keylist.sort()

		for key in keylist:
			self.list += UnitDict[key]
			if key != keylist[-1]:
				self.list.append(("", -1))

		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, gc.getUnitInfo)



	def placeUniqueUnits(self):
		UnitList = []
		for iUnit in xrange(gc.getNumUnitInfos()):
			if self.getUnitCategory(iUnit) == 2:
				UnitList.append((gc.getUnitInfo(iUnit).getDescription(), iUnit))

		UnitList.sort()
		self.list = UnitList
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, gc.getUnitInfo)



	def placeUnitCharts(self):
		self.list = self.getSortedList(gc.getNumUnitCombatInfos(), gc.getUnitCombatInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, gc.getUnitCombatInfo)



	def placeUnitUpgrades(self):
		screen = self.getScreen()
		self.getScreen().deleteWidget("PediaMainItemList")
		self.UPGRADES_GRAPH_ID = self.getNextWidgetName()
		screen.addScrollPanel(self.UPGRADES_GRAPH_ID, u"", self.X_ITEMS, self.Y_PEDIA_PAGE - 13, self.W_SCREEN - self.X_ITEMS, self.H_PEDIA_PAGE + 2, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setActivation(self.UPGRADES_GRAPH_ID, ActivationTypes.ACTIVATE_NORMAL)
		upgradesGraph = UnitUpgradesGraph.UnitUpgradesGraph(self)
		upgradesGraph.getGraph()
		upgradesGraph.drawGraph()



	def placePromotions(self):
		lPromotions = []
		for iPromotion in xrange(gc.getNumPromotionInfos()):
			PromotionInfo = gc.getPromotionInfo(iPromotion)
			if not PromotionInfo.isGraphicalOnly():
				lPromotions.append((PromotionInfo.getDescription(), iPromotion))

		lPromotions.sort()
		self.list = lPromotions
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, gc.getPromotionInfo)



	def placePromotionTree(self):
		screen = self.getScreen()
		self.getScreen().deleteWidget("PediaMainItemList")
		self.UPGRADES_GRAPH_ID = self.getNextWidgetName()
		screen.addScrollPanel(self.UPGRADES_GRAPH_ID, u"", self.X_ITEMS, self.Y_PEDIA_PAGE - 13, self.W_SCREEN - self.X_ITEMS, self.H_PEDIA_PAGE + 2, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setActivation(self.UPGRADES_GRAPH_ID, ActivationTypes.ACTIVATE_NORMAL)
		upgradesGraph = UnitUpgradesGraph.PromotionsGraph(self)
		upgradesGraph.getGraph()
		upgradesGraph.drawGraph()



	def placeBuildings(self):
		lBuildings = []
		for iBuilding in xrange(gc.getNumBuildingInfos()):
			if utils.getBuildingCategory(iBuilding) == 0:
				if iBuilding == utils.getUniqueBuilding(self.iActivePlayer, iBuilding):
					lBuildings.append((gc.getBuildingInfo(iBuilding).getDescription(), iBuilding))
			
		lBuildings.sort()
		self.list = lBuildings
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, gc.getBuildingInfo)



	def placeReligiousBuildings(self):
		lBuildings = []
		prevReligion = -1

		for iBuilding in xrange(gc.getNumBuildingInfos()):
			if utils.getBuildingCategory(iBuilding) == 1:
				iReligion = gc.getBuildingInfo(iBuilding).getReligionType()
				if iReligion != prevReligion:
					hReligion = CyTranslator().getText("TXT_KEY_PEDIA_HEADER_RELIGION", (gc.getReligionInfo(iReligion).getDescription(), ''))
					lBuildings.append(("", -1))
					lBuildings.append((hReligion, -1))

				szDescription = gc.getBuildingInfo(iBuilding).getDescription().replace("The ", "")
				lBuildings.append((szDescription, iBuilding))
				prevReligion = iReligion

		del lBuildings[0]
		self.list = lBuildings
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, gc.getBuildingInfo)



	def placeUniqueBuildings(self):
		lBuildings = []
		for iBuilding in xrange(gc.getNumBuildingInfos()):
			if utils.getBuildingCategory(iBuilding) == 2 and not gc.getBuildingInfo(iBuilding).isGraphicalOnly():
				lBuildings.append((gc.getBuildingInfo(iBuilding).getDescription(), iBuilding))

		lBuildings.sort()
		self.list = lBuildings
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, gc.getBuildingInfo)
		
		
	def placeGreatPeopleBuildings(self):
		lBuildings = []
		for iBuilding in xrange(gc.getNumBuildingInfos()):
			if gc.getBuildingInfo(iBuilding).isGraphicalOnly():
				continue
			if utils.getBuildingCategory(iBuilding) == 3:
				lBuildings.append((gc.getBuildingInfo(iBuilding).getDescription(), iBuilding))
				
		lBuildings.sort()
		self.list = lBuildings
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, gc.getBuildingInfo)



	def placeNationalWonders(self):
		lBuildings = []
		for iBuilding in xrange(gc.getNumBuildingInfos()):
			if gc.getBuildingInfo(iBuilding).isGraphicalOnly():
				continue
			if utils.getBuildingCategory(iBuilding) == 4:
				szDescription = gc.getBuildingInfo(iBuilding).getDescription().replace("The ", "")
				lBuildings.append((szDescription, iBuilding))

		lBuildings.sort()
		self.list = lBuildings
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, gc.getBuildingInfo)



	def placeGreatWonders(self):
		lBuildings = []
		for iBuilding in xrange(gc.getNumBuildingInfos()):
			if utils.getBuildingCategory(iBuilding) == 5:
				szDescription = gc.getBuildingInfo(iBuilding).getDescription().replace("The ", "")
				lBuildings.append((szDescription, iBuilding))

		lBuildings.sort()
		self.list = lBuildings
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, gc.getBuildingInfo)



	def placeProjects(self):
		self.list = self.getSortedList(gc.getNumProjectInfos(), gc.getProjectInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, gc.getProjectInfo)



	def placeTerrains(self):
		self.list = self.getSortedList(gc.getNumTerrainInfos(), gc.getTerrainInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, gc.getTerrainInfo)



	def placeFeatures(self):
		lFeatures = []
		for iFeature in xrange(gc.getNumFeatureInfos()):
			if not gc.getFeatureInfo(iFeature).isGraphicalOnly():
				if not gc.getFeatureInfo(iFeature).getType().startswith("FEATURE_POLLUTION_"):
					if gc.getFeatureInfo(iFeature).getType().find("_NATURAL_WONDER_") == -1:
						lFeatures.append((gc.getFeatureInfo(iFeature).getDescription(), iFeature))

		lFeatures.sort()
		self.list = lFeatures
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, gc.getFeatureInfo)



	def placeResources(self):
		lResources = []
		dResourceMap = {}
		
		for iImprovement in xrange(gc.getNumImprovementInfos()):
			ImprovementInfo = gc.getImprovementInfo(iImprovement)
			lImprovementResources = [iBonus for iBonus in xrange(gc.getNumBonusInfos()) if ImprovementInfo.isBonusTrade(iBonus) and iBonus not in [item for sublist in dResourceMap.values() for item in sublist]]
			
			if lImprovementResources:
				dResourceMap[ImprovementInfo.getText()] = lImprovementResources
		
		lOther = [iBonus for iBonus in xrange(gc.getNumBonusInfos()) if iBonus not in [item for sublist in dResourceMap.values() for item in sublist]]
		if lOther:
			dResourceMap["Media"] = lOther
				
		for sImprovement in sorted(dResourceMap.keys()):
			if lResources:
				lResources.append(("", -1))
				
			lResources.append((sImprovement, -1))
			
			for iBonus in dResourceMap[sImprovement]:
				lResources.append((gc.getBonusInfo(iBonus).getDescription(), iBonus))

		self.list = lResources
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, gc.getBonusInfo)



	def placeImprovements(self):
		self.list = self.getSortedList(gc.getNumImprovementInfos(), gc.getImprovementInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, gc.getImprovementInfo)
		
		
	def placeRoutes(self):
		self.list = self.getSortedList(gc.getNumRouteInfos(), gc.getRouteInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_ROUTE, gc.getRouteInfo)


	def placeConcepts(self):
		self.list = self.getSortedList(gc.getNumConceptInfos(), gc.getConceptInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_DESCRIPTION, gc.getConceptInfo)



	def getNewConceptList(self):
		return self.getSortedList(gc.getNumNewConceptInfos(), self.getNewConceptInfo)



	def getNewConceptInfo(self, id):
		info = gc.getNewConceptInfo(id)
		if not self.isShortcutInfo(info) and not self.isStrategyInfo(info) and not self.isTraitInfo(info):
			return info
		return None



	def placeHints(self):
		screen = self.getScreen()
		self.getScreen().deleteWidget("PediaMainItemList")
		szHintBox = self.getNextWidgetName()
		screen.addListBoxGFC(szHintBox, "", self.X_ITEMS, self.Y_PEDIA_PAGE - 10, self.W_SCREEN - self.X_ITEMS, self.H_PEDIA_PAGE + 23, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(szHintBox, False)
		szHintsText = CyGameTextMgr().buildHintsList()
		hintText = string.split(szHintsText, "\n")
		for hint in hintText:
			if len(hint) != 0:
				screen.appendListBoxStringNoUpdate(szHintBox, hint, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.updateListBox(szHintBox)



	def placeShortcuts(self):
		self.list = self.getSortedList(gc.getNumNewConceptInfos(), self.getShortcutInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_DESCRIPTION, self.getShortcutInfo)



	def getShortcutInfo(self, id):
		info = gc.getNewConceptInfo(id)
		if self.isShortcutInfo(info):
			return info
		return None

	def isShortcutInfo(self, info):
		return info.getType().find("SHORTCUTS") != -1



	def placeStrategy(self):
		self.list = self.getSortedList(gc.getNumNewConceptInfos(), self.getStrategyInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_DESCRIPTION, self.getStrategyInfo)



	def getStrategyInfo(self, id):
		info = gc.getNewConceptInfo(id)
		if self.isStrategyInfo(info):
			return info
		return None



	def isStrategyInfo(self, info):
		return info.getType().find("STRATEGY") != -1



	def placeItems(self, itemwidget, info):
		screen = self.getScreen()
		screen.clearListBoxGFC(self.ITEM_LIST_ID)

		screen.addTableControlGFC(self.ITEM_LIST_ID, 1, self.X_ITEMS, self.Y_ITEMS, self.W_ITEMS, self.H_ITEMS, False, False, 25, 25, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.ITEM_LIST_ID, False)
		screen.setStyle(self.ITEM_LIST_ID, "Table_StandardCiv_Style")
		screen.setTableColumnHeader(self.ITEM_LIST_ID, 0, "", self.W_ITEMS)

		i = 0
		for item in self.list:
			if (info == gc.getConceptInfo):
				data1 = CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT
				data2 = item[1]
			elif (info == self.getNewConceptInfo):
				data1 = CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW
				data2 = item[1]
			elif (info == self.getShortcutInfo):
				data1 = CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW
				data2 = item[1]
			elif (info == self.getStrategyInfo):
				data1 = CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW
				data2 = item[1]
			elif (info == self.getTraitInfo):
				data1 = CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW
				data2 = item[1]
			else:
				data1 = item[1]
				data2 = 1

			if item[1] == -1:
				sTitle = CyTranslator().changeTextColor(item[0], gc.getInfoTypeForString('COLOR_HIGHLIGHT_TEXT'))
				widget = WidgetTypes.WIDGET_GENERAL
				button = ""
			else:
				sTitle = item[0]
				widget = itemwidget
				button = info(item[1]).getButton()

			screen.appendTableRow(self.ITEM_LIST_ID)
			screen.setTableText(self.ITEM_LIST_ID, 0, i, u"<font=3>" + sTitle + u"</font>", button, widget, data1, data2, CvUtil.FONT_LEFT_JUSTIFY)
			i += 1



	def getTraitInfo(self, id):
		info = gc.getNewConceptInfo(id)
		if self.isTraitInfo(info):

			class TraitInfo:
				def __init__(self, conceptInfo):
					self.conceptInfo = conceptInfo
					sKey = conceptInfo.getType()
					sKey = sKey[sKey.find("TRAIT_"):]
					self.eTrait = gc.getInfoTypeForString(sKey)
					self.traitInfo = gc.getTraitInfo(self.eTrait)
				def getDescription(self):
					return u"%c %s" % (TraitUtil.getIcon(self.eTrait), self.traitInfo.getDescription())
				def getButton(self):
					return self.traitInfo.getButton()

			return TraitInfo(info)
		return None



	def isTraitInfo(self, info):
		return info.getType().find("_TRAIT_") != -1



	def getUnitCategory(self, iUnit):
		'0 = Unit'
		'1 = Military Unit'
		'2 = Unique Unit'

		UnitInfo = gc.getUnitInfo(iUnit)
		UnitClassInfo = gc.getUnitClassInfo(UnitInfo.getUnitClassType())
		iDefaultUnit = UnitClassInfo.getDefaultUnitIndex()

		if UnitInfo.isGraphicalOnly() and not utils.getBaseUnit(iUnit) in [iWarrior, iAxeman, iSlave]:
			return -1
		elif iDefaultUnit > -1 and iDefaultUnit != iUnit and not iUnit == iAztecSlave:
			return 2
		elif UnitInfo.getCombat() > 0 or UnitInfo.getAirCombat() != 0 or UnitInfo.isSuicide():
			if not UnitInfo.isAnimal() and not UnitInfo.isFound():
				return 1

		return 0



	def back(self):
		if len(self.pediaHistory) > 1:
			self.pediaFuture.append(self.pediaHistory.pop())
			current = self.pediaHistory.pop()
			self.pediaJump(current[0], current[1], False, True)
		return 1



	def forward(self):
		if self.pediaFuture:
			current = self.pediaFuture.pop()
			self.pediaJump(current[0], current[1], False, True)
		return 1



	def link(self, szLink):
		if szLink == "PEDIA_MAIN_CIV":
			return self.pediaJump(PEDIA_MAIN, PEDIA_CIVS, True, True)
		elif szLink == "PEDIA_MAIN_LEADER":
			return self.pediaJump(PEDIA_MAIN, PEDIA_LEADERS, True, True)
		elif szLink == "PEDIA_MAIN_TRAIT":
			return self.pediaJump(PEDIA_MAIN, PEDIA_TRAITS, True, True)
		elif szLink == "PEDIA_MAIN_CIVIC":
			return self.pediaJump(PEDIA_MAIN, PEDIA_CIVICS, True, True)
		elif szLink == "PEDIA_MAIN_RELIGION":
			return self.pediaJump(PEDIA_MAIN, PEDIA_RELIGIONS, True, True)
		elif szLink == "PEDIA_MAIN_SPECIALIST":
			return self.pediaJump(PEDIA_MAIN, PEDIA_SPECIALISTS, True, True)
		elif szLink == "PEDIA_MAIN_TECH":
			return self.pediaJump(PEDIA_MAIN, PEDIA_TECHS, True, True)
		elif szLink == "PEDIA_MAIN_UNIT":
			return self.pediaJump(PEDIA_MAIN, PEDIA_UNITS, True, True)
		elif szLink == "PEDIA_MAIN_UNIT_GROUP":
			return self.pediaJump(PEDIA_MAIN, PEDIA_UNIT_CATEGORIES, True, True)
		elif szLink == "PEDIA_MAIN_PROMOTION":
			return self.pediaJump(PEDIA_MAIN, PEDIA_PROMOTIONS, True, True)
		elif szLink == "PEDIA_MAIN_BUILDING":
			return self.pediaJump(PEDIA_MAIN, PEDIA_BUILDINGS, True, True)
		elif szLink == "PEDIA_MAIN_PROJECT":
			return self.pediaJump(PEDIA_MAIN, PEDIA_PROJECTS, True, True)
		elif szLink == "PEDIA_MAIN_TERRAIN":
			return self.pediaJump(PEDIA_MAIN, PEDIA_TERRAINS, True, True)
		elif szLink == "PEDIA_MAIN_FEATURE":
			return self.pediaJump(PEDIA_MAIN, PEDIA_FEATURES, True, True)
		elif szLink == "PEDIA_MAIN_BONUS":
			return self.pediaJump(PEDIA_MAIN, PEDIA_RESOURCES, True, True)
		elif szLink == "PEDIA_MAIN_IMPROVEMENT":
			return self.pediaJump(PEDIA_MAIN, PEDIA_IMPROVEMENTS, True, True)
		elif szLink == "PEDIA_MAIN_ROUTE":
			return self.pediaJump(PEDIA_MAIN, PEDIA_ROUTES, True, True)
		elif szLink == "PEDIA_MAIN_CONCEPT":
			return self.pediaJump(PEDIA_MAIN, PEDIA_CONCEPTS, True, True)
		elif szLink == "PEDIA_MAIN_SHORTCUTS":
			return self.pediaJump(PEDIA_MAIN, PEDIA_SHORTCUTS, True, True)


		for i in xrange(gc.getNumCivilizationInfos()):
			if gc.getCivilizationInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_CIVS, i, True, True)
		for i in xrange(gc.getNumLeaderHeadInfos()):
			if gc.getLeaderHeadInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_LEADERS, i, True, True)
		for i in xrange(gc.getNumCivicInfos()):
			if gc.getCivicInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_CIVICS, i, True, True)
		for i in xrange(gc.getNumReligionInfos()):
			if gc.getReligionInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_RELIGIONS, i, True, True)
		for i in xrange(gc.getNumCorporationInfos()):
			if gc.getCorporationInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_CORPORATIONS, i, True, True)
		for i in xrange(gc.getNumSpecialistInfos()):
			if gc.getSpecialistInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_SPECIALISTS, i, True, True)
		for i in xrange(gc.getNumTechInfos()):
			if gc.getTechInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_TECHS, i, True, True)
		for i in xrange(gc.getNumUnitInfos()):
			if gc.getUnitInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_UNITS, i, True, True)
		for i in xrange(gc.getNumUnitCombatInfos()):
			if gc.getUnitCombatInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_UNIT_CATEGORIES, i, True, True)
		for i in xrange(gc.getNumPromotionInfos()):
			if gc.getPromotionInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_PROMOTIONS, i, True, True)
		for i in xrange(gc.getNumBuildingInfos()):
			if gc.getBuildingInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_BUILDINGS, i, True, True)
		for i in xrange(gc.getNumProjectInfos()):
			if gc.getProjectInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_PROJECTS, i, True, True)
		for i in xrange(gc.getNumTerrainInfos()):
			if gc.getTerrainInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_TERRAINS, i, True, True)
		for i in xrange(gc.getNumFeatureInfos()):
			if gc.getFeatureInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_FEATURES, i, True, True)
		for i in xrange(gc.getNumBonusInfos()):
			if gc.getBonusInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_RESOURCES, i, True, True)
		for i in xrange(gc.getNumImprovementInfos()):
			if gc.getImprovementInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_IMPROVEMENTS, i, True, True)
		for i in xrange(gc.getNumRouteInfos()):
			if gc.getImprovementInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_ROUTES, i, True, True)
		for i in xrange(gc.getNumConceptInfos()):
			if gc.getConceptInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(PEDIA_CONCEPTS, i, True, True)



	def handleInput(self, inputClass):
		if inputClass.getPythonFile() == PEDIA_LEADERS:
			return self.pediaLeader.handleInput(inputClass)

		if inputClass.getButtonType() == WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING:
			self.pediaJump(PEDIA_BUILDINGS, inputClass.getData1(), True, False)
		elif inputClass.getButtonType() == WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS:
			self.pediaJump(PEDIA_RESOURCES, inputClass.getData1(), True, True)

		return 0



	def deleteAllWidgets(self):
		screen = self.getScreen()
		iNumWidgets = self.nWidgetCount
		self.nWidgetCount = 0
		for i in xrange(iNumWidgets):
			screen.deleteWidget(self.getNextWidgetName())
		self.nWidgetCount = 0



	def deleteListWidgets(self):
		screen = self.getScreen()
		screen.deleteWidget("PediaMainCategoryList")
		screen.deleteWidget("PediaMainItemList")



	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName



	def getSortedList(self, numInfos, getInfo, noSort = False):
		list = []
		for i in xrange(numInfos):
			item = getInfo(i)
			if item:
				list.append((item.getDescription(), i))

	# BEGIN Filters
		if getInfo == gc.getTechInfo:
			for t in xrange(numInfos - 1, -1, -1):
				if gc.getTechInfo(t).getGridX() <= 0 or gc.getTechInfo(t).getGridY() <= 0:
					list.pop(t)

		if getInfo == gc.getCorporationInfo:
			for c in xrange(numInfos - 1 , -1, -1):
				if gc.getCorporationInfo(c).getSpreadCost() == 0:
					list.pop(c)

		if getInfo == gc.getImprovementInfo:
			for j in xrange(numInfos - 1, -1, -1):
				if gc.getImprovementInfo(j).getDescription() == gc.getImprovementInfo(gc.getInfoTypeForString("IMPROVEMENT_LAND_WORKED")).getDescription():
					list.pop(j)
				if gc.getImprovementInfo(j).getDescription() == gc.getImprovementInfo(gc.getInfoTypeForString("IMPROVEMENT_WATER_WORKED")).getDescription():
					list.pop(j)
				if gc.getImprovementInfo(j).getDescription() == gc.getImprovementInfo(gc.getInfoTypeForString("IMPROVEMENT_CITY_RUINS")).getDescription():
					list.pop(j)
				if gc.getImprovementInfo(j).getDescription() == gc.getImprovementInfo(gc.getInfoTypeForString("IMPROVEMENT_TRIBAL_VILLAGE")).getDescription():
					list.pop(j)
	# END Filters

		if not noSort:
			list.sort()
		return list
