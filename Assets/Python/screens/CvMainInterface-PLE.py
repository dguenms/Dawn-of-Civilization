## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvEventInterface
import time

# BUG - DLL - start
import BugDll
# BUG - DLL - end

# BUG - Options - start
import BugCore
import BugOptions
import BugPath
import BugUtil
import CityUtil
ClockOpt = BugCore.game.NJAGC
ScoreOpt = BugCore.game.Scores
MainOpt = BugCore.game.MainInterface
CityScreenOpt = BugCore.game.CityScreen
# BUG - Options - end

# BUG - Limit/Extra Religions - start
import ReligionUtil
# BUG - Limit/Extra Religions - end

# BUG - PLE - start
import MonkeyTools as mt
import string
from AStarTools import *
import PyHelpers 
import UnitUtil
PyPlayer = PyHelpers.PyPlayer

PleOpt = BugCore.game.PLE
# BUG - PLE - end

# BUG - Align Icons - start
import Scoreboard
import PlayerUtil
# BUG - Align Icons - end

# BUG - Worst Enemy - start
import AttitudeUtil
# BUG - Refuses to Talk - end

# BUG - Refuses to Talk - start
import DiplomacyUtil
# BUG - Refuses to Talk - end

# BUG - Fractional Trade - start
import TradeUtil
# BUG - Fractional Trade - end

import BugUnitPlot

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

# BUG - 3.17 No Espionage - start
import GameUtil
# BUG - 3.17 No Espionage - end

# BUG - Reminders - start
import ReminderEventManager
# BUG - Reminders - end

# BUG - Great General Bar - start
import GGUtil
# BUG - Great General Bar - end

# BUG - Great Person Bar - start
import GPUtil
GP_BAR_WIDTH = 320
# BUG - Great Person Bar - end

# BUG - Progress Bar - Tick Marks - start
import ProgressBarUtil
# BUG - Progress Bar - Tick Marks - end

# PLE Code
import PLE

g_NumEmphasizeInfos = 0
g_NumCityTabTypes = 0
g_NumHurryInfos = 0
g_NumUnitClassInfos = 0
g_NumBuildingClassInfos = 0
g_NumProjectInfos = 0
g_NumProcessInfos = 0
g_NumActionInfos = 0
g_eEndTurnButtonState = -1

# BUG - city specialist - start
g_iSuperSpecialistCount = 0
g_iCitySpecialistCount = 0
g_iAngryCitizensCount = 0
SUPER_SPECIALIST_STACK_WIDTH = 15
SPECIALIST_ROW_HEIGHT = 34
SPECIALIST_ROWS = 3
MAX_SPECIALIST_BUTTON_SPACING = 30
SPECIALIST_AREA_MARGIN = 45
# BUG - city specialist - end

MAX_SELECTED_TEXT = 5
MAX_DISPLAYABLE_BUILDINGS = 15
MAX_DISPLAYABLE_TRADE_ROUTES = 4
MAX_BONUS_ROWS = 10
MAX_CITIZEN_BUTTONS = 8

SELECTION_BUTTON_COLUMNS = 8
SELECTION_BUTTON_ROWS = 2
NUM_SELECTION_BUTTONS = SELECTION_BUTTON_ROWS * SELECTION_BUTTON_COLUMNS

g_iNumBuildingWidgets = MAX_DISPLAYABLE_BUILDINGS
g_iNumTradeRouteWidgets = MAX_DISPLAYABLE_TRADE_ROUTES

# END OF TURN BUTTON POSITIONS
######################
iEndOfTurnButtonSize = 32
iEndOfTurnPosX = 296 # distance from right
iEndOfTurnPosY = 147 # distance from bottom

# MINIMAP BUTTON POSITIONS
######################
iMinimapButtonsExtent = 228
iMinimapButtonsX = 227
iMinimapButtonsY_Regular = 160
iMinimapButtonsY_Minimal = 32
iMinimapButtonWidth = 24
iMinimapButtonHeight = 24

# Globe button
iGlobeButtonX = 48
iGlobeButtonY_Regular = 168
iGlobeButtonY_Minimal = 40
iGlobeToggleWidth = 48
iGlobeToggleHeight = 48

# GLOBE LAYER OPTION POSITIONING
######################
iGlobeLayerOptionsX  = 235
iGlobeLayerOptionsY_Regular  = 170# distance from bottom edge
iGlobeLayerOptionsY_Minimal  = 38 # distance from bottom edge
iGlobeLayerOptionsWidth = 400
iGlobeLayerOptionHeight = 24

# STACK BAR
#####################
iStackBarHeight = 27


# MULTI LIST
#####################
iMultiListXL = 318
iMultiListXR = 332


# TOP CENTER TITLE
#####################
iCityCenterRow1X = 398
iCityCenterRow1Y = 78
iCityCenterRow2X = 398
iCityCenterRow2Y = 104

iCityCenterRow1Xa = 347
iCityCenterRow2Xa = 482


g_iNumTradeRoutes = 0
g_iNumBuildings = 0
g_iNumLeftBonus = 0
g_iNumCenterBonus = 0
g_iNumRightBonus = 0

g_szTimeText = ""

# BUG - NJAGC - start
g_bShowTimeTextAlt = False
g_iTimeTextCounter = -1
# BUG - NJAGC - end

# BUG - Raw Yields - start
import RawYields
g_bRawShowing = False
g_bYieldView, g_iYieldType = RawYields.getViewAndType(0)
g_iYieldTiles = RawYields.WORKED_TILES
RAW_YIELD_HELP = ( "TXT_KEY_RAW_YIELD_VIEW_TRADE",
				   "TXT_KEY_RAW_YIELD_VIEW_FOOD",
				   "TXT_KEY_RAW_YIELD_VIEW_PRODUCTION",
				   "TXT_KEY_RAW_YIELD_VIEW_COMMERCE",
				   "TXT_KEY_RAW_YIELD_TILES_WORKED",
				   "TXT_KEY_RAW_YIELD_TILES_CITY",
				   "TXT_KEY_RAW_YIELD_TILES_OWNED",
				   "TXT_KEY_RAW_YIELD_TILES_ALL" )
# BUG - Raw Yields - end

# BUG - field of view slider - start
DEFAULT_FIELD_OF_VIEW = 42
# BUG - field of view slider - end

HELP_TEXT_MINIMUM_WIDTH = 300

g_pSelectedUnit = 0

# BUG - start
g_mainInterface = None
# BUG - end

class CvMainInterface:
	"Main Interface Screen"
	
	def __init__(self):
	
# BUG - start
		global g_mainInterface
		g_mainInterface = self
# BUG - end

# BUG - draw method
		self.DRAW_METHOD_PLE = "DRAW_METHOD_PLE"
		self.DRAW_METHOD_VAN = "DRAW_METHOD_VAN"
		self.DRAW_METHOD_BUG = "DRAW_METHOD_BUG"
		self.DRAW_METHODS = (self.DRAW_METHOD_PLE, 
							 self.DRAW_METHOD_VAN,
							 self.DRAW_METHOD_BUG)
		self.sDrawMethod = self.DRAW_METHOD_PLE
# BUG - draw method


# BUG - PLE - start
		self.PLE = PLE.PLE()
#		self.PLE.PLE_initialize()
		
		self.MainInterfaceInputMap = {
			self.PLE.PLOT_LIST_BUTTON_NAME	: self.PLE.getPlotListButtonName,
			self.PLE.PLOT_LIST_MINUS_NAME	: self.PLE.getPlotListMinusName,
			self.PLE.PLOT_LIST_PLUS_NAME	: self.PLE.getPlotListPlusName,
			self.PLE.PLOT_LIST_UP_NAME		: self.PLE.getPlotListUpName,
			self.PLE.PLOT_LIST_DOWN_NAME 	: self.PLE.getPlotListDownName,
			
			"PleViewModeStyle1"				: self.PLE.onClickPLEViewMode,
			self.PLE.PLE_VIEW_MODE			: self.PLE.onClickPLEViewMode,
			self.PLE.PLE_MODE_STANDARD		: self.PLE.onClickPLEModeStandard,
			self.PLE.PLE_MODE_MULTILINE		: self.PLE.onClickPLEModeMultiline,
			self.PLE.PLE_MODE_STACK_VERT	: self.PLE.onClickPLEModeStackVert,
			self.PLE.PLE_MODE_STACK_HORIZ	: self.PLE.onClickPLEModeStackHoriz,
			
			self.PLE.PLOT_LIST_PROMO_NAME	: self.PLE.unitPromotion,
			self.PLE.PLOT_LIST_UPGRADE_NAME	: self.PLE.unitUpgrade,
			
			self.PLE.PLE_RESET_FILTERS		: self.PLE.onClickPLEResetFilters,
			self.PLE.PLE_FILTER_CANMOVE		: self.PLE.onClickPLEFilterCanMove,
			self.PLE.PLE_FILTER_CANTMOVE	: self.PLE.onClickPLEFilterCantMove,
			self.PLE.PLE_FILTER_NOTWOUND	: self.PLE.onClickPLEFilterNotWound,
			self.PLE.PLE_FILTER_WOUND		: self.PLE.onClickPLEFilterWound,
			self.PLE.PLE_FILTER_LAND		: self.PLE.onClickPLEFilterLand,
			self.PLE.PLE_FILTER_SEA			: self.PLE.onClickPLEFilterSea,
			self.PLE.PLE_FILTER_AIR			: self.PLE.onClickPLEFilterAir,
			self.PLE.PLE_FILTER_MIL			: self.PLE.onClickPLEFilterMil,
			self.PLE.PLE_FILTER_DOM			: self.PLE.onClickPLEFilterDom,
			self.PLE.PLE_FILTER_OWN			: self.PLE.onClickPLEFilterOwn,
			self.PLE.PLE_FILTER_FOREIGN		: self.PLE.onClickPLEFilterForeign,
			
			self.PLE.PLE_GRP_UNITTYPE		: self.PLE.onClickPLEGrpUnittype,
			self.PLE.PLE_GRP_GROUPS			: self.PLE.onClickPLEGrpGroups,
			self.PLE.PLE_GRP_PROMO			: self.PLE.onClickPLEGrpPromo,
			self.PLE.PLE_GRP_UPGRADE		: self.PLE.onClickPLEGrpUpgrade,
		}

#		self.iVisibleUnits 			= 0
		self.iMaxPlotListIcons 		= 0

		
		self.bPLECurrentlyShowing	= False
		self.bVanCurrentlyShowing	= False
# BUG - draw method
		self.bBUGCurrentlyShowing	= False
# BUG - draw method

		self.xResolution = 0
		self.yResolution = 0
# BUG - PLE - end

# BUG - field of view slider - start
		self.szSliderTextId = "FieldOfViewSliderText"
		self.sFieldOfView_Text = ""
		self.szSliderId = "FieldOfViewSlider"
		self.iField_View_Prev = -1
# BUG - field of view slider - end


		

############## Basic operational functions ###################

#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################

	def numPlotListButtons(self):
		return self.m_iNumPlotListButtons

	def initState (self, screen=None):
		"""
		Initialize screen instance (self.foo) and global variables.
		
		This function is called before drawing the screen (from interfaceScreen() below)
		and anytime the Python modules are reloaded (from CvEventInterface).
		
		THIS FUNCTION MUST NOT ALTER THE SCREEN -- screen.foo()
		"""
		if screen is None:
			screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		self.xResolution = screen.getXResolution()
		self.yResolution = screen.getYResolution()
		
# BUG - Raw Yields - begin
		global g_bYieldView
		global g_iYieldType
		g_bYieldView, g_iYieldType = RawYields.getViewAndType(CityScreenOpt.getRawYieldsDefaultView())
# BUG - Raw Yields - end

# BUG - PLE - begin
		self.PLE.PLE_CalcConstants()
# BUG - PLE - end

		# Set up our global variables...
		global g_NumEmphasizeInfos
		global g_NumCityTabTypes
		global g_NumHurryInfos
		global g_NumUnitClassInfos
		global g_NumBuildingClassInfos
		global g_NumProjectInfos
		global g_NumProcessInfos
		global g_NumActionInfos
		
		g_NumEmphasizeInfos = gc.getNumEmphasizeInfos()
		g_NumCityTabTypes = CityTabTypes.NUM_CITYTAB_TYPES
		g_NumHurryInfos = gc.getNumHurryInfos()
		g_NumUnitClassInfos = gc.getNumUnitClassInfos()
		g_NumBuildingClassInfos = gc.getNumBuildingClassInfos()
		g_NumProjectInfos = gc.getNumProjectInfos()
		g_NumProcessInfos = gc.getNumProcessInfos()
		g_NumActionInfos = gc.getNumActionInfos()
		
# BUG - field of view slider - start
		iBtnY = 27
		self.iX_FoVSlider = self.xResolution - 120
		self.iY_FoVSlider = iBtnY + 30
		self.sFieldOfView_Text = localText.getText("TXT_KEY_BUG_OPT_MAININTERFACE__FIELDOFVIEW_TEXT", ())
		if MainOpt.isRememberFieldOfView():
			self.iField_View = int(MainOpt.getFieldOfView())
		else:
			self.iField_View = DEFAULT_FIELD_OF_VIEW
# BUG - field of view slider - end


# BUG - Progress Bar - Tick Marks - start
		xCoord = 268 + (self.xResolution - 1024) / 2
		self.pBarResearchBar_n = ProgressBarUtil.ProgressBar("ResearchBar-Canvas", xCoord, 2, 487, iStackBarHeight, gc.getInfoTypeForString("COLOR_RESEARCH_RATE"), ProgressBarUtil.TICK_MARKS, True)
		self.pBarResearchBar_n.addBarItem("ResearchBar")
		self.pBarResearchBar_n.addBarItem("ResearchText")
# BUG - Progress Bar - Tick Marks - end
		
# BUG - Progress Bar - Tick Marks - start
		xCoord = 268 + (self.xResolution - 1440) / 2
		xCoord += 6 + 84
		self.pBarResearchBar_w = ProgressBarUtil.ProgressBar("ResearchBar-w-Canvas", xCoord, 2, 487, iStackBarHeight, gc.getInfoTypeForString("COLOR_RESEARCH_RATE"), ProgressBarUtil.TICK_MARKS, True)
		self.pBarResearchBar_w.addBarItem("ResearchBar-w")
		self.pBarResearchBar_w.addBarItem("ResearchText")
# BUG - Progress Bar - Tick Marks - end

# BUG - Progress Bar - Tick Marks - start
		self.pBarPopulationBar = ProgressBarUtil.ProgressBar("PopulationBar-Canvas", iCityCenterRow1X, iCityCenterRow1Y-4, self.xResolution - (iCityCenterRow1X*2), iStackBarHeight, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType(), ProgressBarUtil.SOLID_MARKS, True)
		self.pBarPopulationBar.addBarItem("PopulationBar")
		self.pBarPopulationBar.addBarItem("PopulationText")
		self.pBarProductionBar = ProgressBarUtil.ProgressBar("ProductionBar-Canvas", iCityCenterRow2X, iCityCenterRow2Y-4, self.xResolution - (iCityCenterRow2X*2), iStackBarHeight, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType(), ProgressBarUtil.TICK_MARKS, True)
		self.pBarProductionBar.addBarItem("ProductionBar")
		self.pBarProductionBar.addBarItem("ProductionText")
		self.pBarProductionBar_Whip = ProgressBarUtil.ProgressBar("ProductionBar-Whip-Canvas", iCityCenterRow2X, iCityCenterRow2Y-4, self.xResolution - (iCityCenterRow2X*2), iStackBarHeight, gc.getInfoTypeForString("COLOR_YELLOW"), ProgressBarUtil.CENTER_MARKS, False)
		self.pBarProductionBar_Whip.addBarItem("ProductionBar")
		self.pBarProductionBar_Whip.addBarItem("ProductionText")
# BUG - Progress Bar - Tick Marks - end

		self.m_iNumPlotListButtons = (self.xResolution - (iMultiListXL+iMultiListXR) - 68) / 34

# BUG - BUG unit plot draw method - start
# bug unit panel
		self.BupPanel = BugUnitPlot.BupPanel(screen, screen.getYResolution(), self.numPlotListButtons(), gc.getMAX_PLOT_LIST_ROWS())
# BUG - BUG unit plot draw method - end

	def interfaceScreen (self):
		"""
		Draw all of the screen elements.
		
		This function is called once after starting or loading a game.
		
		THIS FUNCTION MUST NOT CREATE ANY INSTANCE OR GLOBAL VARIABLES.
		It may alter existing ones created in __init__() or initState(), however.
		"""
		if ( CyGame().isPitbossHost() ):
			return
		
		# This is the main interface screen, create it as such
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		self.initState(screen)
		screen.setForcedRedraw(True)
		screen.setDimensions(0, 0, self.xResolution, self.yResolution)
		
		# to avoid changing all the code below
		xResolution = self.xResolution
		yResolution = self.yResolution
		
		# Help Text Area
		screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, HELP_TEXT_MINIMUM_WIDTH )

		# Center Left
		screen.addPanel( "InterfaceCenterLeftBackgroundWidget", u"", u"", True, False, 0, 0, 258, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "InterfaceCenterLeftBackgroundWidget", "Panel_City_Left_Style" )
		screen.hide( "InterfaceCenterLeftBackgroundWidget" )

		# Top Left
		screen.addPanel( "InterfaceTopLeftBackgroundWidget", u"", u"", True, False, 258, 0, xResolution - 516, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "InterfaceTopLeftBackgroundWidget", "Panel_City_Top_Style" )
		screen.hide( "InterfaceTopLeftBackgroundWidget" )

		# Center Right
		screen.addPanel( "InterfaceCenterRightBackgroundWidget", u"", u"", True, False, xResolution - 258, 0, 258, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "InterfaceCenterRightBackgroundWidget", "Panel_City_Right_Style" )
		screen.hide( "InterfaceCenterRightBackgroundWidget" )
		
		screen.addPanel( "CityScreenAdjustPanel", u"", u"", True, False, 10, 44, 238, 105, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "CityScreenAdjustPanel", "Panel_City_Info_Style" )
		screen.hide( "CityScreenAdjustPanel" )
		
		screen.addPanel( "TopCityPanelLeft", u"", u"", True, False, 260, 70, xResolution/2-260, 60, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "TopCityPanelLeft", "Panel_City_TanTL_Style" )
		screen.hide( "TopCityPanelLeft" )
		
		screen.addPanel( "TopCityPanelRight", u"", u"", True, False, xResolution/2, 70, xResolution/2-260, 60, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "TopCityPanelRight", "Panel_City_TanTR_Style" )
		screen.hide( "TopCityPanelRight" )
		
		# Top Bar

		# SF CHANGE		
		screen.addPanel( "CityScreenTopWidget", u"", u"", True, False, 0, -2, xResolution, 41, PanelStyles.PANEL_STYLE_STANDARD )

		screen.setStyle( "CityScreenTopWidget", "Panel_TopBar_Style" )
		screen.hide( "CityScreenTopWidget" )
		
		# Top Center Title
		screen.addPanel( "CityNameBackground", u"", u"", True, False, 260, 31, xResolution - (260*2), 38, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "CityNameBackground", "Panel_City_Title_Style" )
		screen.hide( "CityNameBackground" )

		# Left Background Widget
		screen.addDDSGFC( "InterfaceLeftBackgroundWidget", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BOTTOM_LEFT").getPath(), 0, yResolution - 164, 304, 164, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "InterfaceLeftBackgroundWidget" )

		# Center Background Widget
		screen.addPanel( "InterfaceCenterBackgroundWidget", u"", u"", True, False, 296, yResolution - 133, xResolution - (296*2), 133, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceCenterBackgroundWidget", "Panel_Game_HudBC_Style" )
		screen.hide( "InterfaceCenterBackgroundWidget" )

		# Left Background Widget
		screen.addPanel( "InterfaceLeftBackgroundWidget", u"", u"", True, False, 0, yResolution - 168, 304, 168, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceLeftBackgroundWidget", "Panel_Game_HudBL_Style" )
		screen.hide( "InterfaceLeftBackgroundWidget" )

		# Right Background Widget
		screen.addPanel( "InterfaceRightBackgroundWidget", u"", u"", True, False, xResolution - 304, yResolution - 168, 304, 168, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceRightBackgroundWidget", "Panel_Game_HudBR_Style" )
		screen.hide( "InterfaceRightBackgroundWidget" )
	
		# Top Center Background

		# SF CHANGE
		screen.addPanel( "InterfaceTopCenter", u"", u"", True, False, 257, -2, xResolution-(257*2), 48, PanelStyles.PANEL_STYLE_STANDARD)

		screen.setStyle( "InterfaceTopCenter", "Panel_Game_HudTC_Style" )
		screen.hide( "InterfaceTopCenter" )

		# Top Left Background
		screen.addPanel( "InterfaceTopLeft", u"", u"", True, False, 0, -2, 267, 60, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceTopLeft", "Panel_Game_HudTL_Style" )
		screen.hide( "InterfaceTopLeft" )

		# Top Right Background
		screen.addPanel( "InterfaceTopRight", u"", u"", True, False, xResolution - 267, -2, 267, 60, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceTopRight", "Panel_Game_HudTR_Style" )
		screen.hide( "InterfaceTopRight" )

		iBtnWidth	= 28
		iBtnAdvance = 25
		iBtnY = 27
		iBtnX = 27
		
		# Turn log Button
		screen.setImageButton( "TurnLogButton", "", iBtnX, iBtnY - 2, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TURN_LOG).getActionInfoIndex(), -1 )
		screen.setStyle( "TurnLogButton", "Button_HUDLog_Style" )
		screen.hide( "TurnLogButton" )
		
		iBtnX = xResolution - 277
		
		# Advisor Buttons...
		screen.setImageButton( "DomesticAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_DOMESTIC_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "DomesticAdvisorButton", "Button_HUDAdvisorDomestic_Style" )
		screen.hide( "DomesticAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "FinanceAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FINANCIAL_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "FinanceAdvisorButton", "Button_HUDAdvisorFinance_Style" )
		screen.hide( "FinanceAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "CivicsAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVICS_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "CivicsAdvisorButton", "Button_HUDAdvisorCivics_Style" )
		screen.hide( "CivicsAdvisorButton" )
		
		iBtnX += iBtnAdvance 
		screen.setImageButton( "ForeignAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FOREIGN_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "ForeignAdvisorButton", "Button_HUDAdvisorForeign_Style" )
		screen.hide( "ForeignAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "MilitaryAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_MILITARY_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "MilitaryAdvisorButton", "Button_HUDAdvisorMilitary_Style" )
		screen.hide( "MilitaryAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "TechAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TECH_CHOOSER).getActionInfoIndex(), -1 )
		screen.setStyle( "TechAdvisorButton", "Button_HUDAdvisorTechnology_Style" )
		screen.hide( "TechAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "ReligiousAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_RELIGION_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "ReligiousAdvisorButton", "Button_HUDAdvisorReligious_Style" )
		screen.hide( "ReligiousAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "CorporationAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CORPORATION_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "CorporationAdvisorButton", "Button_HUDAdvisorCorporation_Style" )
		screen.hide( "CorporationAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "VictoryAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_VICTORY_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "VictoryAdvisorButton", "Button_HUDAdvisorVictory_Style" )
		screen.hide( "VictoryAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "InfoAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_INFO).getActionInfoIndex(), -1 )
		screen.setStyle( "InfoAdvisorButton", "Button_HUDAdvisorRecord_Style" )
		screen.hide( "InfoAdvisorButton" )

# BUG - 3.17 No Espionage - start
		if GameUtil.isEspionage():
			iBtnX += iBtnAdvance
			screen.setImageButton( "EspionageAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_ESPIONAGE_SCREEN).getActionInfoIndex(), -1 )
			screen.setStyle( "EspionageAdvisorButton", "Button_HUDAdvisorEspionage_Style" )
			screen.hide( "EspionageAdvisorButton" )
# BUG - 3.17 No Espionage - end

# BUG - field of view slider - start
		self.setFieldofView_Text(screen)
		iW = 100
		iH = 15
		screen.addSlider(self.szSliderId, self.iX_FoVSlider + 5, self.iY_FoVSlider, iW, iH, self.iField_View - 1, 0, 100 - 1, WidgetTypes.WIDGET_GENERAL, -1, -1, False);
		screen.hide(self.szSliderTextId)
		screen.hide(self.szSliderId)
# BUG - field of view slider - end

		# City Tabs
		iBtnX = xResolution - 324
		iBtnY = yResolution - 94
		iBtnWidth = 24
		iBtnAdvance = 24

		screen.setButtonGFC( "CityTab0", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 0, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.setStyle( "CityTab0", "Button_HUDJumpUnit_Style" )
		screen.hide( "CityTab0" )

		iBtnY += iBtnAdvance
		screen.setButtonGFC( "CityTab1", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.setStyle( "CityTab1", "Button_HUDJumpBuilding_Style" )
		screen.hide( "CityTab1" )
		
		iBtnY += iBtnAdvance
		screen.setButtonGFC( "CityTab2", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 2, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.setStyle( "CityTab2", "Button_HUDJumpWonder_Style" )
		screen.hide( "CityTab2" )
		
		# Minimap initialization
		screen.setMainInterface(True)
		
		screen.addPanel( "MiniMapPanel", u"", u"", True, False, xResolution - 214, yResolution - 151, 208, 151, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "MiniMapPanel", "Panel_Game_HudMap_Style" )
		screen.hide( "MiniMapPanel" )

		screen.initMinimap( xResolution - 210, xResolution - 9, yResolution - 131, yResolution - 9, -0.1 )
		gc.getMap().updateMinimapColor()

		self.createMinimapButtons()
	
		# Help button (always visible)
		screen.setImageButton( "InterfaceHelpButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_CIVILOPEDIA_ICON").getPath(), xResolution - 28, 2, 24, 24, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVILOPEDIA).getActionInfoIndex(), -1 )
		screen.hide( "InterfaceHelpButton" )

		screen.setImageButton( "MainMenuButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_MENU_ICON").getPath(), xResolution - 54, 2, 24, 24, WidgetTypes.WIDGET_MENU_ICON, -1, -1 )
		screen.hide( "MainMenuButton" )

		# Globeview buttons
		self.createGlobeviewButtons( )

		screen.addMultiListControlGFC( "BottomButtonContainer", u"", iMultiListXL, yResolution - 113, xResolution - (iMultiListXL+iMultiListXR), 100, 4, 48, 48, TableStyles.TABLE_STYLE_STANDARD )		
		screen.hide( "BottomButtonContainer" )

		# *********************************************************************************
		# PLOT LIST BUTTONS
		# *********************************************************************************

# BUG - PLE - begin
		for j in range(gc.getMAX_PLOT_LIST_ROWS()):
			yRow = (j - gc.getMAX_PLOT_LIST_ROWS() + 1) * 34
			yPixel = yResolution - 169 + yRow - 3
			xPixel = 315 - 3
			xWidth = self.numPlotListButtons() * 34 + 3
			yHeight = 32 + 3
		
			szStringPanel = "PlotListPanel" + str(j)
			screen.addPanel(szStringPanel, u"", u"", True, False, xPixel, yPixel, xWidth, yHeight, PanelStyles.PANEL_STYLE_EMPTY)

			for i in range(self.numPlotListButtons()):
				k = j*self.numPlotListButtons()+i
				
				xOffset = i * 34
				#tjp
				szString = "PlotList_Button" + str(k)

# BUG - plot list - start
				szFileNamePromo = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION_FRAME").getPath()
				szStringPromoFrame  = szString + "PromoFrame"
				screen.addDDSGFCAt( szStringPromoFrame , szStringPanel, szFileNamePromo, xOffset +  2,  2, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False )
				screen.hide( szStringPromoFrame  )
# BUG - plot list - end

				screen.addCheckBoxGFCAt(szStringPanel, szString, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xOffset + 3, 3, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, ButtonStyles.BUTTON_STYLE_LABEL, True )
				screen.hide( szString )

				szStringHealth = szString + "Health"
				screen.addStackedBarGFCAt( szStringHealth, szStringPanel, xOffset + 3, 26, 32, 11, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, k, -1 )
				screen.hide( szStringHealth )

				szStringIcon = szString + "Icon"
				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
				screen.addDDSGFCAt( szStringIcon, szStringPanel, szFileName, xOffset, 0, 12, 12, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False )
				screen.hide( szStringIcon )

		self.PLE.preparePlotListObjects(screen)
# BUG - PLE - end


		# End Turn Text		
		screen.setLabel( "EndTurnText", "Background", u"", CvUtil.FONT_CENTER_JUSTIFY, 0, yResolution - 188, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setHitTest( "EndTurnText", HitTestTypes.HITTEST_NOHIT )

		# Three states for end turn button...
		screen.setImageButton( "EndTurnButton", "", xResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosX, yResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosY, iEndOfTurnButtonSize, iEndOfTurnButtonSize, WidgetTypes.WIDGET_END_TURN, -1, -1 )
		screen.setStyle( "EndTurnButton", "Button_HUDEndTurn_Style" )
		screen.setEndTurnState( "EndTurnButton", "Red" )
		screen.hide( "EndTurnButton" )

		# *********************************************************************************
		# RESEARCH BUTTONS
		# *********************************************************************************

		i = 0
		for i in range( gc.getNumTechInfos() ):
			szName = "ResearchButton" + str(i)
			screen.setImageButton( szName, gc.getTechInfo(i).getButton(), 0, 0, 32, 32, WidgetTypes.WIDGET_RESEARCH, i, -1 )
			screen.hide( szName )

		i = 0
		for i in range(gc.getNumReligionInfos()):
			szName = "ReligionButton" + str(i)
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_PICK_RELIGION):
				szButton = gc.getReligionInfo(i).getGenericTechButton()
			else:
				szButton = gc.getReligionInfo(i).getTechButton()
			screen.setImageButton( szName, szButton, 0, 0, 32, 32, WidgetTypes.WIDGET_RESEARCH, gc.getReligionInfo(i).getTechPrereq(), -1 )
			screen.hide( szName )
		
		# *********************************************************************************
		# CITIZEN BUTTONS
		# *********************************************************************************

		szHideCitizenList = []

		# Angry Citizens
		i = 0
		for i in range(MAX_CITIZEN_BUTTONS):
			szName = "AngryCitizen" + str(i)
			screen.setImageButton( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_ANGRYCITIZEN_TEXTURE").getPath(), xResolution - 74 - (26 * i), yResolution - 238, 24, 24, WidgetTypes.WIDGET_ANGRY_CITIZEN, -1, -1 )
			screen.hide( szName )
			
		iCount = 0

		# Increase Specialists...
		i = 0
		for i in range( gc.getNumSpecialistInfos() ):
			if (gc.getSpecialistInfo(i).isVisible()):
				szName = "IncreaseSpecialist" + str(i)
				screen.setButtonGFC( szName, u"", "", xResolution - 46, (yResolution - 270 - (26 * iCount)), 20, 20, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1, ButtonStyles.BUTTON_STYLE_CITY_PLUS )
				screen.hide( szName )

				iCount = iCount + 1

		iCount = 0

		# Decrease specialists
		i = 0
		for i in range( gc.getNumSpecialistInfos() ):
			if (gc.getSpecialistInfo(i).isVisible()):
				szName = "DecreaseSpecialist" + str(i)
				screen.setButtonGFC( szName, u"", "", xResolution - 24, (yResolution - 270 - (26 * iCount)), 20, 20, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
				screen.hide( szName )

				iCount = iCount + 1

		iCount = 0

		# Citizen Buttons
		i = 0
		for i in range( gc.getNumSpecialistInfos() ):
		
			if (gc.getSpecialistInfo(i).isVisible()):
			
				szName = "CitizenDisabledButton" + str(i)
				screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), xResolution - 74, (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_DISABLED_CITIZEN, i, -1 )
				screen.enable( szName, False )
				screen.hide( szName )

				for j in range(MAX_CITIZEN_BUTTONS):
					szName = "CitizenButton" + str((i * 100) + j)
					screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution - 74 - (26 * j), (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL )
					screen.hide( szName )

# BUG - city specialist - start
		screen.addPanel( "SpecialistBackground", u"", u"", True, False, xResolution - 243, yResolution - 423, 230, 30, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "SpecialistBackground", "Panel_City_Header_Style" )
		screen.hide( "SpecialistBackground" )
		screen.setLabel( "SpecialistLabel", "Background", localText.getText("TXT_KEY_CONCEPT_SPECIALISTS", ()), CvUtil.FONT_CENTER_JUSTIFY, xResolution - 128, yResolution - 415, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "SpecialistLabel" )
# BUG - city specialist - end

		# **********************************************************
		# GAME DATA STRINGS
		# **********************************************************

		szGameDataList = []

		xCoord = 268 + (xResolution - 1024) / 2
		screen.addStackedBarGFC( "ResearchBar", xCoord, 2, 487, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RESEARCH_STORED") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_RESEARCH_RATE") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "ResearchBar" )

# BUG - Great General Bar - start
		screen.addStackedBarGFC( "GreatGeneralBar", xCoord, 27, 100, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1 )
		screen.setStackedBarColors( "GreatGeneralBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_NEGATIVE_RATE") ) #gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatGeneralBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatGeneralBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatGeneralBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatGeneralBar" )
# BUG - Great General Bar - end

# BUG - Great Person Bar - start
		xCoord += 7 + 100
		screen.addStackedBarGFC( "GreatPersonBar", xCoord, 27, 380, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GP_PROGRESS_BAR, -1, -1 )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatPersonBar" )
# BUG - Great Person Bar - end

# BUG - Bars on single line for higher resolution screens - start
		xCoord = 268 + (xResolution - 1440) / 2
		screen.addStackedBarGFC( "GreatGeneralBar-w", xCoord, 2, 84, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1 )
		screen.setStackedBarColors( "GreatGeneralBar-w", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_NEGATIVE_RATE") ) #gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatGeneralBar-w", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatGeneralBar-w", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatGeneralBar-w", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatGeneralBar-w" )

		xCoord += 6 + 84
		screen.addStackedBarGFC( "ResearchBar-w", xCoord, 2, 487, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
		screen.setStackedBarColors( "ResearchBar-w", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RESEARCH_STORED") )
		screen.setStackedBarColors( "ResearchBar-w", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_RESEARCH_RATE") )
		screen.setStackedBarColors( "ResearchBar-w", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "ResearchBar-w", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "ResearchBar-w" )

		xCoord += 6 + 487
		screen.addStackedBarGFC( "GreatPersonBar-w", xCoord, 2, 320, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GP_PROGRESS_BAR, -1, -1 )
		screen.setStackedBarColors( "GreatPersonBar-w", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatPersonBar-w", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
		screen.setStackedBarColors( "GreatPersonBar-w", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatPersonBar-w", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatPersonBar-w" )
# BUG - Bars on single line for higher resolution screens - end

		
		# *********************************************************************************
		# SELECTION DATA BUTTONS/STRINGS
		# *********************************************************************************

		szHideSelectionDataList = []

		screen.addStackedBarGFC( "PopulationBar", iCityCenterRow1X, iCityCenterRow1Y-4, xResolution - (iCityCenterRow1X*2), iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_POPULATION, -1, -1 )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_STORED, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType() )
		screen.setStackedBarColorsAlpha( "PopulationBar", InfoBarTypes.INFOBAR_RATE, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType(), 0.8 )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_NEGATIVE_RATE") )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "PopulationBar" )

		screen.addStackedBarGFC( "ProductionBar", iCityCenterRow2X, iCityCenterRow2Y-4, xResolution - (iCityCenterRow2X*2), iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_PRODUCTION, -1, -1 )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_STORED, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType() )
		screen.setStackedBarColorsAlpha( "ProductionBar", InfoBarTypes.INFOBAR_RATE, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType(), 0.8 )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType() )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "ProductionBar" )

		screen.addStackedBarGFC( "GreatPeopleBar", xResolution - 246, yResolution - 188, 240, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_PEOPLE, -1, -1 )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatPeopleBar" )

		screen.addStackedBarGFC( "CultureBar", 6, yResolution - 188, 240, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_CULTURE, -1, -1 )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_CULTURE_STORED") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_CULTURE_RATE") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "CultureBar" )

# BUG - Limit/Extra Religions - start
#		# Holy City Overlay
#		for i in range( gc.getNumReligionInfos() ):
#			xCoord = xResolution - 242 + (i * 34)
#			yCoord = 42
#			szName = "ReligionHolyCityDDS" + str(i)
#			screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLYCITY_OVERLAY").getPath(), xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_RELIGION_CITY, i, -1 )
#			screen.hide( szName )
# BUG - Limit/Extra Religions - end

# BUG - Limit/Extra Corporations - start
#		for i in range( gc.getNumCorporationInfos() ):
#			xCoord = xResolution - 242 + (i * 34)
#			yCoord = 66
#			szName = "CorporationHeadquarterDDS" + str(i)
#			screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLYCITY_OVERLAY").getPath(), xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_CORPORATION_CITY, i, -1 )
#			screen.hide( szName )
# BUG - Limit/Extra Corporations - end

		screen.addStackedBarGFC( "NationalityBar", 6, yResolution - 214, 240, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_NATIONALITY, -1, -1 )
		screen.hide( "NationalityBar" )

		screen.setButtonGFC( "CityScrollMinus", u"", "", 274, 32, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( "CityScrollMinus" )

		screen.setButtonGFC( "CityScrollPlus", u"", "", 288, 32, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( "CityScrollPlus" )
		
# BUG - City Arrows - start
		screen.setButtonGFC( "MainCityScrollMinus", u"", "", xResolution - 275, yResolution - 165, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( "MainCityScrollMinus" )

		screen.setButtonGFC( "MainCityScrollPlus", u"", "", xResolution - 255, yResolution - 165, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end		

# BUG - PLE - begin
#		screen.setButtonGFC( "PlotListMinus", u"", "", 315 + ( xResolution - (iMultiListXL+iMultiListXR) - 68 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
#		screen.hide( "PlotListMinus" )
#
#		screen.setButtonGFC( "PlotListPlus", u"", "", 298 + ( xResolution - (iMultiListXL+iMultiListXR) - 34 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
#		screen.hide( "PlotListPlus" )
		
		screen.setButtonGFC( self.PLE.PLOT_LIST_MINUS_NAME, u"", "", 315 + ( xResolution - (iMultiListXL+iMultiListXR) - 68 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( self.PLE.PLOT_LIST_MINUS_NAME )
		screen.setButtonGFC( self.PLE.PLOT_LIST_PLUS_NAME, u"", "", 298 + ( xResolution - (iMultiListXL+iMultiListXR) - 34 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( self.PLE.PLOT_LIST_PLUS_NAME )

		screen.setImageButton( self.PLE.PLOT_LIST_UP_NAME, ArtFileMgr.getInterfaceArtInfo("PLE_ARROW_UP").getPath(), 315 + ( xResolution - (iMultiListXL+iMultiListXR) - 68 ) + 5, yResolution - 171 + 5, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( self.PLE.PLOT_LIST_UP_NAME )
		screen.setImageButton( self.PLE.PLOT_LIST_DOWN_NAME, ArtFileMgr.getInterfaceArtInfo("PLE_ARROW_DOWN").getPath(), 298 + ( xResolution - (iMultiListXL+iMultiListXR) - 34 ) + 5, yResolution - 171 + 5, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( self.PLE.PLOT_LIST_DOWN_NAME )
# BUG - PLE - end

		screen.addPanel( "TradeRouteListBackground", u"", u"", True, False, 10, 157, 238, 30, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "TradeRouteListBackground", "Panel_City_Header_Style" )
		screen.hide( "TradeRouteListBackground" )

		screen.setLabel( "TradeRouteListLabel", "Background", localText.getText("TXT_KEY_HEADING_TRADEROUTE_LIST", ()), CvUtil.FONT_CENTER_JUSTIFY, 129, 165, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "TradeRouteListLabel" )
		
# BUG - Raw Yields - start
		nX = 10 + 24
		nY = 157 + 5
		nSize = 24
		nDist = 24
		nGap = 10
		szHighlightButton = ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_HIGHLIGHT").getPath()
		
		# Trade
		screen.addCheckBoxGFC( "RawYieldsTrade0", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_TRADE").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 0, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide("RawYieldsTrade0")
		
		# Yields
		nX += nDist + nGap
		screen.addCheckBoxGFC( "RawYieldsFood1", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_FOOD").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide("RawYieldsFood1")
		nX += nDist
		screen.addCheckBoxGFC( "RawYieldsProduction2", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_PRODUCTION").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 2, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide("RawYieldsProduction2")
		nX += nDist
		screen.addCheckBoxGFC( "RawYieldsCommerce3", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_COMMERCE").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 3, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide("RawYieldsCommerce3")
		
		# Tile Selection
		nX += nDist + nGap
		screen.addCheckBoxGFC( "RawYieldsWorkedTiles4", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_WORKED_TILES").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 4, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide("RawYieldsWorkedTiles4")
		nX += nDist
		screen.addCheckBoxGFC( "RawYieldsCityTiles5", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_CITY_TILES").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 5, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide("RawYieldsCityTiles5")
		nX += nDist
		screen.addCheckBoxGFC( "RawYieldsOwnedTiles6", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_OWNED_TILES").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 6, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide("RawYieldsOwnedTiles6")
# BUG - Raw Yields - end

		screen.addPanel( "BuildingListBackground", u"", u"", True, False, 10, 287, 238, 30, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "BuildingListBackground", "Panel_City_Header_Style" )
		screen.hide( "BuildingListBackground" )

		screen.setLabel( "BuildingListLabel", "Background", localText.getText("TXT_KEY_CONCEPT_BUILDINGS", ()), CvUtil.FONT_CENTER_JUSTIFY, 129, 295, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "BuildingListLabel" )

		# *********************************************************************************
		# UNIT INFO ELEMENTS
		# *********************************************************************************

		i = 0
		for i in range(gc.getNumPromotionInfos()):
			szName = "PromotionButton" + str(i)
			screen.addDDSGFC( szName, gc.getPromotionInfo(i).getButton(), 180, yResolution - 18, 24, 24, WidgetTypes.WIDGET_ACTION, gc.getPromotionInfo(i).getActionInfoIndex(), -1 )
			screen.hide( szName )

# BUG - PLE - begin
			szName = self.PLE.PLE_PROMO_BUTTONS_UNITINFO + str(i)
			screen.addDDSGFC( szName, gc.getPromotionInfo(i).getButton(), \
								180, yResolution - 18, \
								self.PLE.CFG_INFOPANE_BUTTON_SIZE, self.PLE.CFG_INFOPANE_BUTTON_SIZE, \
								WidgetTypes.WIDGET_ACTION, gc.getPromotionInfo(i).getActionInfoIndex(), -1 )
			screen.hide( szName )
# BUG - PLE - end
			
		# *********************************************************************************
		# SCORES
		# *********************************************************************************
		
		screen.addPanel( "ScoreBackground", u"", u"", True, False, 0, 0, 0, 0, PanelStyles.PANEL_STYLE_HUD_HELP )
		screen.hide( "ScoreBackground" )

		for i in range( gc.getMAX_PLAYERS() ):
			szName = "ScoreText" + str(i)
			screen.setText( szName, "Background", u"", CvUtil.FONT_RIGHT_JUSTIFY, 996, 622, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_CONTACT_CIV, i, -1 )
			screen.hide( szName )

		# This should be a forced redraw screen
		screen.setForcedRedraw( True )
		
		# This should show the screen immidiately and pass input to the game
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)
		
		szHideList = []
		
		szHideList.append( "CreateGroup" )
		szHideList.append( "DeleteGroup" )

		# City Tabs
		for i in range( g_NumCityTabTypes ):
			szButtonID = "CityTab" + str(i)
			szHideList.append( szButtonID )
					
		for i in range( g_NumHurryInfos ):
			szButtonID = "Hurry" + str(i)
			szHideList.append( szButtonID )

		szHideList.append( "Hurry0" )
		szHideList.append( "Hurry1" )
		
		screen.registerHideList( szHideList, len(szHideList), 0 )

		return 0

	# Will update the screen (every 250 MS)
	def updateScreen(self):
		
		global g_szTimeText
		global g_iTimeTextCounter

#		BugUtil.debug("update - Turn %d, Player %d, Interface %d, End Turn Button %d ===", 
#				gc.getGame().getGameTurn(), gc.getGame().getActivePlayer(), CyInterface().getShowInterface(), CyInterface().getEndTurnState())

# BUG - Options - start
		BugOptions.write()
# BUG - Options - end

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		self.m_iNumPlotListButtons = (xResolution - (iMultiListXL+iMultiListXR) - 68) / 34
		
		# This should recreate the minimap on load games and returns if already exists -JW
		screen.initMinimap( xResolution - 210, xResolution - 9, yResolution - 131, yResolution - 9, -0.1 )

		messageControl = CyMessageControl()
		
		bShow = False
		
		# Hide all interface widgets		
		#screen.hide( "EndTurnText" )

		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY ):
			if (gc.getGame().isPaused()):
				# Pause overrides other messages
				acOutput = localText.getText("SYSTEM_GAME_PAUSED", (gc.getPlayer(gc.getGame().getPausePlayer()).getNameKey(), ))
				#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
				screen.setEndTurnState( "EndTurnText", acOutput )
				bShow = True
			elif (messageControl.GetFirstBadConnection() != -1):
				# Waiting on a bad connection to resolve
				if (messageControl.GetConnState(messageControl.GetFirstBadConnection()) == 1):
					if (gc.getGame().isMPOption(MultiplayerOptionTypes.MPOPTION_ANONYMOUS)):
						acOutput = localText.getText("SYSTEM_WAITING_FOR_PLAYER", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), 0))
					else:
						acOutput = localText.getText("SYSTEM_WAITING_FOR_PLAYER", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), (messageControl.GetFirstBadConnection() + 1)))
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif (messageControl.GetConnState(messageControl.GetFirstBadConnection()) == 2):
					if (gc.getGame().isMPOption(MultiplayerOptionTypes.MPOPTION_ANONYMOUS)):
						acOutput = localText.getText("SYSTEM_PLAYER_JOINING", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), 0))
					else:
						acOutput = localText.getText("SYSTEM_PLAYER_JOINING", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), (messageControl.GetFirstBadConnection() + 1)))
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
			else:
				# Flash select messages if no popups are present
				if ( CyInterface().shouldDisplayReturn() ):
					acOutput = localText.getText("SYSTEM_RETURN", ())
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayWaitingOthers() ):
					acOutput = localText.getText("SYSTEM_WAITING", ())
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayEndTurn() ):
# BUG - Reminders - start
					if ( ReminderEventManager.g_turnReminderTexts ):
						acOutput = u"%s" % ReminderEventManager.g_turnReminderTexts
					else:
						acOutput = localText.getText("SYSTEM_END_TURN", ())
# BUG - Reminders - end
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayWaitingYou() ):
					acOutput = localText.getText("SYSTEM_WAITING_FOR_YOU", ())
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
# BUG - Options - start
				elif ( MainOpt.isShowOptionsKeyReminder() ):
					if BugPath.isMac():
						acOutput = localText.getText("TXT_KEY_BUG_OPTIONS_KEY_REMINDER_MAC", (BugPath.getModName(),))
					else:
						acOutput = localText.getText("TXT_KEY_BUG_OPTIONS_KEY_REMINDER", (BugPath.getModName(),))
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
# BUG - Options - end

		if ( bShow ):
			screen.showEndTurn( "EndTurnText" )
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isCityScreenUp() ):
				screen.moveItem( "EndTurnText", 0, yResolution - 194, -0.1 )
			else:
				screen.moveItem( "EndTurnText", 0, yResolution - 86, -0.1 )
		else:
			screen.hideEndTurn( "EndTurnText" )

		self.updateEndTurnButton()

# BUG - NJAGC - start
		global g_bShowTimeTextAlt
		if (CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY  and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):
			if (ClockOpt.isEnabled()):
				if (ClockOpt.isShowEra()):
					screen.show( "EraText" )
				else:
					screen.hide( "EraText" )
				
				if (ClockOpt.isAlternateTimeText()):
					#global g_iTimeTextCounter (already done above)
					if (CyUserProfile().wasClockJustTurnedOn() or g_iTimeTextCounter <= 0):
						# reset timer, display primary
						g_bShowTimeTextAlt = False
						g_iTimeTextCounter = ClockOpt.getAlternatePeriod() * 1000
						CyUserProfile().setClockJustTurnedOn(False)
					else:
						# countdown timer
						g_iTimeTextCounter -= 250
						if (g_iTimeTextCounter <= 0):
							# timer elapsed, toggle between primary and alternate
							g_iTimeTextCounter = ClockOpt.getAlternatePeriod() * 1000
							g_bShowTimeTextAlt = not g_bShowTimeTextAlt
				else:
					g_bShowTimeTextAlt = False
				
				self.updateTimeText()
				screen.setLabel( "TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 56, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.show( "TimeText" )
			else:
				screen.hide( "EraText" )
				self.updateTimeText()
				screen.setLabel( "TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 56, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.show( "TimeText" )
		else:
			screen.hide( "TimeText" )
			screen.hide( "EraText" )
# BUG - NJAGC - end

# BUG - PLE - start 			
		# this ensures that the info pane is closed after a greater mouse pos change
		self.PLE.checkInfoPane(CyInterface().getMousePos())
# BUG - PLE - end

		return 0

	# Will redraw the interface
	def redraw( self ):

#		BugUtil.debug("redraw - Turn %d, Player %d, Interface %d, End Turn Button %d", 
#				gc.getGame().getGameTurn(), gc.getGame().getActivePlayer(), CyInterface().getShowInterface(), CyInterface().getEndTurnState())

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

# BUG - Field of View - start
		self.setFieldofView(screen, CyInterface().isCityScreenUp())
# BUG - Field of View - end

		# Check Dirty Bits, see what we need to redraw...
		if (CyInterface().isDirty(InterfaceDirtyBits.PercentButtons_DIRTY_BIT) == True):
			# Percent Buttons
			self.updatePercentButtons()
			CyInterface().setDirty(InterfaceDirtyBits.PercentButtons_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.Flag_DIRTY_BIT) == True):
			# Percent Buttons
			self.updateFlag()
			CyInterface().setDirty(InterfaceDirtyBits.Flag_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT) == True ):
			# Miscellaneous buttons (civics screen, etc)
			self.updateMiscButtons()
			CyInterface().setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT) == True ):
			# Info Pane Dirty Bit
			# This must come before updatePlotListButtons so that the entity widget appears in front of the stats
			self.updateInfoPaneStrings()
			CyInterface().setDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT) == True ):
			# Plot List Buttons Dirty
			self.updatePlotListButtons()
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT) == True ):
			# Selection Buttons Dirty
			self.updateSelectionButtons()
			CyInterface().setDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.ResearchButtons_DIRTY_BIT) == True ):
			# Research Buttons Dirty
			self.updateResearchButtons()
			CyInterface().setDirty(InterfaceDirtyBits.ResearchButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.CitizenButtons_DIRTY_BIT) == True ):
			# Citizen Buttons Dirty

# BUG - city specialist - start
			self.updateCitizenButtons_hide()
			if (CityScreenOpt.isCitySpecialist_Stacker()):
				self.updateCitizenButtons_Stacker()
			elif (CityScreenOpt.isCitySpecialist_Chevron()):
				self.updateCitizenButtons_Chevron()
			else:
				self.updateCitizenButtons()
# BUG - city specialist - end
			
			CyInterface().setDirty(InterfaceDirtyBits.CitizenButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.GameData_DIRTY_BIT) == True ):
			# Game Data Strings Dirty
			self.updateGameDataStrings()
			CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.Help_DIRTY_BIT) == True ):
			# Help Dirty bit
			self.updateHelpStrings()
			CyInterface().setDirty(InterfaceDirtyBits.Help_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT) == True ):
			# Selection Data Dirty Bit
			self.updateCityScreen()
			CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, True)
			CyInterface().setDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.Score_DIRTY_BIT) == True or CyInterface().checkFlashUpdate() ):
			# Scores!
			self.updateScoreStrings()
			CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.GlobeInfo_DIRTY_BIT) == True ):
			# Globeview and Globelayer buttons
			CyInterface().setDirty(InterfaceDirtyBits.GlobeInfo_DIRTY_BIT, False)
			self.updateGlobeviewButtons()

		return 0

	# Will update the percent buttons
	def updatePercentButtons( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		for iI in range( CommerceTypes.NUM_COMMERCE_TYPES ):
			szString = "IncreasePercent" + str(iI)
			screen.hide( szString )
			szString = "DecreasePercent" + str(iI)
			screen.hide( szString )
# BUG - Min/Max Sliders - start
			szString = "MaxPercent" + str(iI)
			screen.hide( szString )
			szString = "MinPercent" + str(iI)
			screen.hide( szString )
# BUG - Min/Max Sliders - start

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if ( not CyInterface().isCityScreenUp() or ( pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer() ) or gc.getGame().isDebugMode() ):
			iCount = 0

			if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):
				for iI in range( CommerceTypes.NUM_COMMERCE_TYPES ):
					# Intentional offset...
					eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES
										
					if (gc.getActivePlayer().isCommerceFlexible(eCommerce) or (CyInterface().isCityScreenUp() and (eCommerce == CommerceTypes.COMMERCE_GOLD))):
# BUG - Min/Max Sliders - start
						bEnable = gc.getActivePlayer().isCommerceFlexible(eCommerce)
						if MainOpt.isShowMinMaxCommerceButtons() and not CyInterface().isCityScreenUp():
							iMinMaxAdjustX = 20
							szString = "MaxPercent" + str(eCommerce)
							screen.setButtonGFC( szString, u"", "", 70, 50 + (19 * iCount), 20, 20, 
												 *BugDll.widget("WIDGET_SET_PERCENT", eCommerce, 100, 
												 				WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, 100, 
												 				ButtonStyles.BUTTON_STYLE_CITY_PLUS) )
							screen.show( szString )
							screen.enable( szString, bEnable )
							szString = "MinPercent" + str(eCommerce)
							screen.setButtonGFC( szString, u"", "", 130, 50 + (19 * iCount), 20, 20, 
												 *BugDll.widget("WIDGET_SET_PERCENT", eCommerce, 0, 
												 				WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, -100, 
												 				ButtonStyles.BUTTON_STYLE_CITY_MINUS) )
							screen.show( szString )
							screen.enable( szString, bEnable )
						else:
							iMinMaxAdjustX = 0
						
						szString = "IncreasePercent" + str(eCommerce)
						screen.setButtonGFC( szString, u"", "", 70 + iMinMaxAdjustX, 50 + (19 * iCount), 20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_PLUS )
						screen.show( szString )
						screen.enable( szString, bEnable )
						szString = "DecreasePercent" + str(eCommerce)
						screen.setButtonGFC( szString, u"", "", 90 + iMinMaxAdjustX, 50 + (19 * iCount), 20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, -gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_MINUS )
						screen.show( szString )
						screen.enable( szString, bEnable )

						iCount = iCount + 1
						# moved enabling above
# BUG - Min/Max Sliders - end
						
		return 0

# BUG - start
	def resetEndTurnObjects(self):
		"""
		Clears the end turn text and hides it and the button.
		"""
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.setEndTurnState( "EndTurnText", u"" )
		screen.hideEndTurn( "EndTurnText" )
		screen.hideEndTurn( "EndTurnButton" )
# BUG - end

	# Will update the end Turn Button
	def updateEndTurnButton( self ):

		global g_eEndTurnButtonState
		
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		if ( CyInterface().shouldDisplayEndTurnButton() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
		
			eState = CyInterface().getEndTurnState()
			
			bShow = False
			
			if ( eState == EndTurnButtonStates.END_TURN_OVER_HIGHLIGHT ):
				screen.setEndTurnState( "EndTurnButton", u"Red" )
				bShow = True
			elif ( eState == EndTurnButtonStates.END_TURN_OVER_DARK ):
				screen.setEndTurnState( "EndTurnButton", u"Red" )
				bShow = True
			elif ( eState == EndTurnButtonStates.END_TURN_GO ):
				screen.setEndTurnState( "EndTurnButton", u"Green" )
				bShow = True
			
			if ( bShow ):
				screen.showEndTurn( "EndTurnButton" )
			else:
				screen.hideEndTurn( "EndTurnButton" )
			
			if ( g_eEndTurnButtonState == eState ):
				return
				
			g_eEndTurnButtonState = eState
			
		else:
			screen.hideEndTurn( "EndTurnButton" )

		return 0

	# Update the miscellaneous buttons
	def updateMiscButtons( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		xResolution = screen.getXResolution()

# BUG - Great Person Bar - start
		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY  and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):
			self.updateGreatPersonBar(screen)
# BUG - Great Person Bar - end

		if ( CyInterface().shouldDisplayFlag() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			screen.show( "CivilizationFlag" )
			screen.show( "InterfaceHelpButton" )
			screen.show( "MainMenuButton" )
		else:
			screen.hide( "CivilizationFlag" )
			screen.hide( "InterfaceHelpButton" )
			screen.hide( "MainMenuButton" )

		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL or CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_MINIMAP_ONLY ):
			screen.hide( "InterfaceLeftBackgroundWidget" )
			screen.hide( "InterfaceTopBackgroundWidget" )
			screen.hide( "InterfaceCenterBackgroundWidget" )
			screen.hide( "InterfaceRightBackgroundWidget" )
			screen.hide( "MiniMapPanel" )
			screen.hide( "InterfaceTopLeft" )
			screen.hide( "InterfaceTopCenter" )
			screen.hide( "InterfaceTopRight" )
			screen.hide( "TurnLogButton" )
			screen.hide( "EspionageAdvisorButton" )
			screen.hide( "DomesticAdvisorButton" )
			screen.hide( "ForeignAdvisorButton" )
			screen.hide( "TechAdvisorButton" )
			screen.hide( "CivicsAdvisorButton" )
			screen.hide( "ReligiousAdvisorButton" )
			screen.hide( "CorporationAdvisorButton" )
			screen.hide( "FinanceAdvisorButton" )
			screen.hide( "MilitaryAdvisorButton" )
			screen.hide( "VictoryAdvisorButton" )
			screen.hide( "InfoAdvisorButton" )
# BUG - City Arrows - start
			screen.hide( "MainCityScrollMinus" )
			screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end

# BUG - field of view slider - start
			screen.hide(self.szSliderTextId)
			screen.hide(self.szSliderId)
# BUG - field of view slider - end

		elif ( CyInterface().isCityScreenUp() ):
			screen.show( "InterfaceLeftBackgroundWidget" )
			screen.show( "InterfaceTopBackgroundWidget" )
			screen.show( "InterfaceCenterBackgroundWidget" )
			screen.show( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.hide( "InterfaceTopLeft" )
			screen.hide( "InterfaceTopCenter" )
			screen.hide( "InterfaceTopRight" )
			screen.hide( "TurnLogButton" )
			screen.hide( "EspionageAdvisorButton" )
			screen.hide( "DomesticAdvisorButton" )
			screen.hide( "ForeignAdvisorButton" )
			screen.hide( "TechAdvisorButton" )
			screen.hide( "CivicsAdvisorButton" )
			screen.hide( "ReligiousAdvisorButton" )
			screen.hide( "CorporationAdvisorButton" )
			screen.hide( "FinanceAdvisorButton" )
			screen.hide( "MilitaryAdvisorButton" )
			screen.hide( "VictoryAdvisorButton" )
			screen.hide( "InfoAdvisorButton" )
# BUG - City Arrows - start
			screen.hide( "MainCityScrollMinus" )
			screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end
# BUG - field of view slider - start
			screen.hide(self.szSliderTextId)
			screen.hide(self.szSliderId)
# BUG - field of view slider - end

		elif ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE):
			screen.hide( "InterfaceLeftBackgroundWidget" )
			screen.show( "InterfaceTopBackgroundWidget" )
			screen.hide( "InterfaceCenterBackgroundWidget" )
			screen.hide( "InterfaceRightBackgroundWidget" )
			screen.hide( "MiniMapPanel" )
			screen.show( "InterfaceTopLeft" )
			screen.show( "InterfaceTopCenter" )
			screen.show( "InterfaceTopRight" )
			screen.show( "TurnLogButton" )
			screen.show( "EspionageAdvisorButton" )
			screen.show( "DomesticAdvisorButton" )
			screen.show( "ForeignAdvisorButton" )
			screen.show( "TechAdvisorButton" )
			screen.show( "CivicsAdvisorButton" )
			screen.show( "ReligiousAdvisorButton" )
			screen.show( "CorporationAdvisorButton" )
			screen.show( "FinanceAdvisorButton" )
			screen.show( "MilitaryAdvisorButton" )
			screen.show( "VictoryAdvisorButton" )
			screen.show( "InfoAdvisorButton" )
# BUG - City Arrows - start
			screen.hide( "MainCityScrollMinus" )
			screen.hide( "MainCityScrollPlus" )			
# BUG - City Arrows - end
# BUG - field of view slider - start
			screen.hide(self.szSliderTextId)
			screen.hide(self.szSliderId)
# BUG - field of view slider - end

			screen.moveToFront( "TurnLogButton" )
			screen.moveToFront( "EspionageAdvisorButton" )
			screen.moveToFront( "DomesticAdvisorButton" )
			screen.moveToFront( "ForeignAdvisorButton" )
			screen.moveToFront( "TechAdvisorButton" )
			screen.moveToFront( "CivicsAdvisorButton" )
			screen.moveToFront( "ReligiousAdvisorButton" )
			screen.moveToFront( "CorporationAdvisorButton" )
			screen.moveToFront( "FinanceAdvisorButton" )
			screen.moveToFront( "MilitaryAdvisorButton" )
			screen.moveToFront( "VictoryAdvisorButton" )
			screen.moveToFront( "InfoAdvisorButton" )

		elif (CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_ADVANCED_START):		
			screen.hide( "InterfaceLeftBackgroundWidget" )
			screen.hide( "InterfaceTopBackgroundWidget" )
			screen.hide( "InterfaceCenterBackgroundWidget" )
			screen.hide( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.hide( "InterfaceTopLeft" )
			screen.hide( "InterfaceTopCenter" )
			screen.hide( "InterfaceTopRight" )
			screen.hide( "TurnLogButton" )
			screen.hide( "EspionageAdvisorButton" )
			screen.hide( "DomesticAdvisorButton" )
			screen.hide( "ForeignAdvisorButton" )
			screen.hide( "TechAdvisorButton" )
			screen.hide( "CivicsAdvisorButton" )
			screen.hide( "ReligiousAdvisorButton" )
			screen.hide( "CorporationAdvisorButton" )
			screen.hide( "FinanceAdvisorButton" )
			screen.hide( "MilitaryAdvisorButton" )
			screen.hide( "VictoryAdvisorButton" )
			screen.hide( "InfoAdvisorButton" )
# BUG - City Arrows - start
			screen.hide( "MainCityScrollMinus" )
			screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end

		elif ( CyEngine().isGlobeviewUp() ):
			screen.hide( "InterfaceLeftBackgroundWidget" )
			screen.hide( "InterfaceTopBackgroundWidget" )
			screen.hide( "InterfaceCenterBackgroundWidget" )
			screen.show( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.show( "InterfaceTopLeft" )
			screen.show( "InterfaceTopCenter" )
			screen.show( "InterfaceTopRight" )
			screen.show( "TurnLogButton" )
			screen.show( "EspionageAdvisorButton" )
			screen.show( "DomesticAdvisorButton" )
			screen.show( "ForeignAdvisorButton" )
			screen.show( "TechAdvisorButton" )
			screen.show( "CivicsAdvisorButton" )
			screen.show( "ReligiousAdvisorButton" )
			screen.show( "CorporationAdvisorButton" )
			screen.show( "FinanceAdvisorButton" )
			screen.show( "MilitaryAdvisorButton" )
			screen.show( "VictoryAdvisorButton" )
			screen.show( "InfoAdvisorButton" )			
# BUG - City Arrows - start
			screen.hide( "MainCityScrollMinus" )
			screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end
# BUG - field of view slider - start
			screen.hide(self.szSliderTextId)
			screen.hide(self.szSliderId)
# BUG - field of view slider - end

			screen.moveToFront( "TurnLogButton" )
			screen.moveToFront( "EspionageAdvisorButton" )
			screen.moveToFront( "DomesticAdvisorButton" )
			screen.moveToFront( "ForeignAdvisorButton" )
			screen.moveToFront( "TechAdvisorButton" )
			screen.moveToFront( "CivicsAdvisorButton" )
			screen.moveToFront( "ReligiousAdvisorButton" )
			screen.moveToFront( "CorporationAdvisorButton" )
			screen.moveToFront( "FinanceAdvisorButton" )
			screen.moveToFront( "MilitaryAdvisorButton" )
			screen.moveToFront( "VictoryAdvisorButton" )
			screen.moveToFront( "InfoAdvisorButton" )
			
		else:
			screen.show( "InterfaceLeftBackgroundWidget" )
			screen.show( "InterfaceTopBackgroundWidget" )
			screen.show( "InterfaceCenterBackgroundWidget" )
			screen.show( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.show( "InterfaceTopLeft" )
			screen.show( "InterfaceTopCenter" )
			screen.show( "InterfaceTopRight" )
			screen.show( "TurnLogButton" )
			screen.show( "EspionageAdvisorButton" )
			screen.show( "DomesticAdvisorButton" )
			screen.show( "ForeignAdvisorButton" )
			screen.show( "TechAdvisorButton" )
			screen.show( "CivicsAdvisorButton" )
			screen.show( "ReligiousAdvisorButton" )
			screen.show( "CorporationAdvisorButton" )
			screen.show( "FinanceAdvisorButton" )
			screen.show( "MilitaryAdvisorButton" )
			screen.show( "VictoryAdvisorButton" )
			screen.show( "InfoAdvisorButton" )
# BUG - City Arrows - start
			if (MainOpt.isShowCityCycleArrows()):
				screen.show( "MainCityScrollMinus" )
				screen.show( "MainCityScrollPlus" )
			else:
				screen.hide( "MainCityScrollMinus" )
				screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end
# BUG - field of view slider - start
			if (MainOpt.isShowFieldOfView()):
				screen.show(self.szSliderTextId)
				screen.show(self.szSliderId)
			else:
				screen.hide(self.szSliderTextId)
				screen.hide(self.szSliderId)
# BUG - field of view slider - end

			screen.moveToFront( "TurnLogButton" )
			screen.moveToFront( "EspionageAdvisorButton" )
			screen.moveToFront( "DomesticAdvisorButton" )
			screen.moveToFront( "ForeignAdvisorButton" )
			screen.moveToFront( "TechAdvisorButton" )
			screen.moveToFront( "CivicsAdvisorButton" )
			screen.moveToFront( "ReligiousAdvisorButton" )
			screen.moveToFront( "CorporationAdvisorButton" )
			screen.moveToFront( "FinanceAdvisorButton" )
			screen.moveToFront( "MilitaryAdvisorButton" )
			screen.moveToFront( "VictoryAdvisorButton" )
			screen.moveToFront( "InfoAdvisorButton" )
			
		screen.updateMinimapVisibility()

		return 0

	# Update plot List Buttons
	def updatePlotListButtons( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		self.updatePlotListButtons_Hide(screen)

		self.updatePlotListButtons_Common(screen)

# BUG - draw methods
		self.sDrawMethod = self.DRAW_METHODS[PleOpt.getDrawMethod()]
		if self.sDrawMethod == self.DRAW_METHOD_PLE:
			self.PLE.updatePlotListButtons_PLE(screen, self.xResolution, self.yResolution)
			self.bPLECurrentlyShowing = True
		elif self.sDrawMethod == self.DRAW_METHOD_VAN:
			self.updatePlotListButtons_Orig(screen)
			self.bVanCurrentlyShowing = True
		else:  # self.DRAW_METHOD_BUG
			self.updatePlotListButtons_BUG(screen)
			self.bBUGCurrentlyShowing = True
# BUG - draw methods

		return 0

#		if PleOpt.isPLE_Style():
#			self.updatePlotListButtons_PLE(screen)
#			self.bPLECurrentlyShowing = True
#		else:
#			self.updatePlotListButtons_Orig(screen)
#			self.bVanCurrentlyShowing = True
#		return 0

	def updatePlotListButtons_Hide( self, screen ):
		# hide all buttons
		if self.bPLECurrentlyShowing:
			self.PLE.hidePlotListButtonPLEObjects(screen)
			self.PLE.hideUnitInfoPane()
			self.bPLECurrentlyShowing = False

		if self.bVanCurrentlyShowing:
			self.hidePlotListButton_Orig(screen)
			self.bVanCurrentlyShowing = False

# BUG - BUG unit plot draw method - start
		if self.bBUGCurrentlyShowing:
			self.hidePlotListButton_BUG(screen)
			self.bBUGCurrentlyShowing = False
# BUG - BUG unit plot draw method - end

	def updatePlotListButtons_Common( self, screen ):

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		# Capture these for looping over the plot's units
		self.PLE.UnitPlotList_BUGOptions()

		bHandled = False
		if ( CyInterface().shouldDisplayUnitModel() and not CyEngine().isGlobeviewUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL ):
			if ( CyInterface().isCitySelection() ):

				iOrders = CyInterface().getNumOrdersQueued()

				for i in range( iOrders ):
					if ( bHandled == False ):
						eOrderNodeType = CyInterface().getOrderNodeType(i)
						if (eOrderNodeType  == OrderTypes.ORDER_TRAIN ):
							screen.addUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getOrderNodeData1(i), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1,  -20, 30, 1, False )
							bHandled = True
						elif ( eOrderNodeType == OrderTypes.ORDER_CONSTRUCT ):
							screen.addBuildingGraphicGFC( "InterfaceUnitModel", CyInterface().getOrderNodeData1(i), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1,  -20, 30, 0.8, False )
							bHandled = True
						elif ( eOrderNodeType == OrderTypes.ORDER_CREATE ):
							if(gc.getProjectInfo(CyInterface().getOrderNodeData1(i)).isSpaceship()):
								modelType = 0
								screen.addSpaceShipWidgetGFC("InterfaceUnitModel", 175, yResolution - 138, 123, 132, CyInterface().getOrderNodeData1(i), modelType, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1)
							else:
								screen.hide( "InterfaceUnitModel" )
							bHandled = True
						elif ( eOrderNodeType == OrderTypes.ORDER_MAINTAIN ):
							screen.hide( "InterfaceUnitModel" )
							bHandled = True
							
				if ( not bHandled ):
					screen.hide( "InterfaceUnitModel" )
					bHandled = True

				screen.moveToFront("SelectedCityText")

			elif ( CyInterface().getHeadSelectedUnit() ):
				screen.addUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getHeadSelectedUnit().getUnitType(), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_UNIT_MODEL, CyInterface().getHeadSelectedUnit().getUnitType(), -1,  -20, 30, 1, False )
#				screen.addSpecificUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getHeadSelectedUnit(), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_UNIT_MODEL, CyInterface().getHeadSelectedUnit().getUnitType(), -1,  -20, 30, 1, False )
				screen.moveToFront("SelectedUnitText")
			else:
				screen.hide( "InterfaceUnitModel" )
		else:
			screen.hide( "InterfaceUnitModel" )

	# hides all plot list objects
	def hidePlotListButton_Orig(self, screen):
		# hides all unit button objects
		for i in range( self.iMaxPlotListIcons ):
			szString = "PlotList_Button" + str(i)
			screen.hide( szString )
			screen.hide( szString + "Icon" )
			screen.hide( szString + "Health" )
			screen.hide( szString + "MoveBar" )
			screen.hide( szString + "PromoFrame" )
			screen.hide( szString + "ActionIcon" )
			screen.hide( szString + "Upgrade" )

# BUG - draw method
	def hidePlotListButton_BUG(self, screen):
		# hides all unit button objects
		for i in range( self.iMaxPlotListIcons ):
			szString = "PlotList_Button" + str(i)
			screen.hide( szString )
			screen.hide( szString + "Icon" )
			screen.hide( szString + "Health" )
			screen.hide( szString + "MoveBar" )
			screen.hide( szString + "PromoFrame" )
			screen.hide( szString + "ActionIcon" )
			screen.hide( szString + "Upgrade" )
# BUG - draw method


	def updatePlotListButtons_Orig( self, screen ):

# need to put in something similar to 	def displayUnitPlotListObjects( self, screen, pLoopUnit, nRow, nCol ):

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		pPlot = CyInterface().getSelectionPlot()

		for i in range(gc.getNumPromotionInfos()):
			szName = "PromotionButton" + str(i)
			screen.moveToFront( szName )

		screen.hide( "PlotListMinus" )
		screen.hide( "PlotListPlus" )

		if ( pPlot and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyEngine().isGlobeviewUp() == False):

			iVisibleUnits = CyInterface().getNumVisibleUnits()
			iCount = -(CyInterface().getPlotListColumn())

			bLeftArrow = False
			bRightArrow = False

			if (CyInterface().isCityScreenUp()):
				iMaxRows = 1
				iSkipped = (gc.getMAX_PLOT_LIST_ROWS() - 1) * self.numPlotListButtons()
				iCount += iSkipped
			else:
				iMaxRows = gc.getMAX_PLOT_LIST_ROWS()
				iCount += CyInterface().getPlotListOffset()
				iSkipped = 0

			CyInterface().cacheInterfacePlotUnits(pPlot)
			for i in range(CyInterface().getNumCachedInterfacePlotUnits()):
				pLoopUnit = CyInterface().getCachedInterfacePlotUnit(i)
				if (pLoopUnit):

					if ((iCount == 0) and (CyInterface().getPlotListColumn() > 0)):
						bLeftArrow = True
					elif ((iCount == (gc.getMAX_PLOT_LIST_ROWS() * self.numPlotListButtons() - 1)) and ((iVisibleUnits - iCount - CyInterface().getPlotListColumn() + iSkipped) > 1)):
						bRightArrow = True

					if ((iCount >= 0) and (iCount <  self.numPlotListButtons() * gc.getMAX_PLOT_LIST_ROWS())):
						if ((pLoopUnit.getTeam() != gc.getGame().getActiveTeam()) or pLoopUnit.isWaiting()):
							szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_FORTIFY").getPath()

						elif (pLoopUnit.canMove()):
							if (pLoopUnit.hasMoved()):
								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_HASMOVED").getPath()
							else:
								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
						else:
							szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_NOMOVE").getPath()

						szString = "PlotList_Button" + str(iCount)
						screen.changeImageButton( szString, gc.getUnitInfo(pLoopUnit.getUnitType()).getButton() )
						if ( pLoopUnit.getOwner() == gc.getGame().getActivePlayer() ):
							bEnable = True
						else:
							bEnable = False
						screen.enable(szString, bEnable)

						if (pLoopUnit.IsSelected()):
							screen.setState(szString, True)
						else:
							screen.setState(szString, False)
						screen.show( szString )

						# place the health bar
						if (pLoopUnit.isFighting()):
							bShowHealth = False
						elif (pLoopUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
							bShowHealth = pLoopUnit.canAirAttack()
						else:
							bShowHealth = pLoopUnit.canFight()

						if bShowHealth:
							szStringHealth = szString + "Health"
							screen.setBarPercentage( szStringHealth, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
							if (pLoopUnit.getDamage() >= ((pLoopUnit.maxHitPoints() * 2) / 3)):
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RED"))
							elif (pLoopUnit.getDamage() >= (pLoopUnit.maxHitPoints() / 3)):
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_YELLOW"))
							else:
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREEN"))
							screen.show( szStringHealth )

						# Adds the overlay first
						szStringIcon = szString + "Icon"
						screen.changeDDSGFC( szStringIcon, szFileName )
						screen.show( szStringIcon )

						if bEnable:
							x = 315 + ((iCount % self.numPlotListButtons()) * 34)
							y = yResolution - 169 + (iCount / self.numPlotListButtons() - gc.getMAX_PLOT_LIST_ROWS() + 1) * 34

							self.PLE.displayUnitPlotList_Dot( screen, pLoopUnit, szString, iCount, x, y + 4 )
							self.PLE.displayUnitPlotList_Promo( screen, pLoopUnit, szString )
							self.PLE.displayUnitPlotList_Upgrade( screen, pLoopUnit, szString, iCount, x, y )
							self.PLE.displayUnitPlotList_Mission( screen, pLoopUnit, szString, iCount, x, y - 22, 12)

					iCount = iCount + 1

			if (iVisibleUnits > self.numPlotListButtons() * iMaxRows):
				screen.enable("PlotListMinus", bLeftArrow)
				screen.show( "PlotListMinus" )

				screen.enable("PlotListPlus", bRightArrow)
				screen.show( "PlotListPlus" )

		return 0

# BUG - BUG unit plot draw method - start
	def updatePlotListButtons_BUG( self, screen ):

# need to put in something similar to 	def displayUnitPlotListObjects( self, screen, pLoopUnit, nRow, nCol ):

#		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		pPlot = CyInterface().getSelectionPlot()

#		for i in range(gc.getNumPromotionInfos()):
#			szName = "PromotionButton" + str(i)
#			screen.moveToFront( szName )

#		screen.hide( "PlotListMinus" )
#		screen.hide( "PlotListPlus" )

		BugUtil.debug("updatePlotListButtons_BUG - A")

		# skip this if we don't need to display any units
		if not (pPlot
		and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL
		and CyEngine().isGlobeviewUp() == False):
#		if (not pPlot
#		or CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL
#		or CyEngine().isGlobeviewUp() == True):
			return 0

		BugUtil.debug("updatePlotListButtons_BUG - B")

		self.BupPanel.flushUnits()

		CyInterface().cacheInterfacePlotUnits(pPlot)
		for i in range(CyInterface().getNumCachedInterfacePlotUnits()):
			pLoopUnit = CyInterface().getCachedInterfacePlotUnit(i)
			if (pLoopUnit):
				self.BupPanel.addUnit(pLoopUnit)

		BugUtil.debug("updatePlotListButtons_BUG - C")

		self.BupPanel.Draw()



#







#		iVisibleUnits = CyInterface().getNumVisibleUnits()
#		iCount = -(CyInterface().getPlotListColumn())

#		bLeftArrow = False
#		bRightArrow = False

#		if (CyInterface().isCityScreenUp()):
#			iMaxRows = 1
#			iSkipped = (gc.getMAX_PLOT_LIST_ROWS() - 1) * self.numPlotListButtons()
#			iCount += iSkipped
#		else:
#			iMaxRows = gc.getMAX_PLOT_LIST_ROWS()
#			iCount += CyInterface().getPlotListOffset()
#			iSkipped = 0

#		CyInterface().cacheInterfacePlotUnits(pPlot)
#		for i in range(CyInterface().getNumCachedInterfacePlotUnits()):
#			pLoopUnit = CyInterface().getCachedInterfacePlotUnit(i)
#			if (pLoopUnit):

#				if ((iCount == 0) and (CyInterface().getPlotListColumn() > 0)):
#					bLeftArrow = True
#				elif ((iCount == (gc.getMAX_PLOT_LIST_ROWS() * self.numPlotListButtons() - 1)) and ((iVisibleUnits - iCount - CyInterface().getPlotListColumn() + iSkipped) > 1)):
#					bRightArrow = True

#				if ((iCount >= 0) and (iCount <  self.numPlotListButtons() * gc.getMAX_PLOT_LIST_ROWS())):
#					if ((pLoopUnit.getTeam() != gc.getGame().getActiveTeam()) or pLoopUnit.isWaiting()):
#						szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_FORTIFY").getPath()

#					elif (pLoopUnit.canMove()):
#						if (pLoopUnit.hasMoved()):
#							szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_HASMOVED").getPath()
#						else:
#							szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
#					else:
#						szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_NOMOVE").getPath()

#					szString = "PlotListButton" + str(iCount)
#					screen.changeImageButton( szString, gc.getUnitInfo(pLoopUnit.getUnitType()).getButton() )
#					if ( pLoopUnit.getOwner() == gc.getGame().getActivePlayer() ):
#						bEnable = True
#					else:
#						bEnable = False
#					screen.enable(szString, bEnable)

#					if (pLoopUnit.IsSelected()):
#						screen.setState(szString, True)
#					else:
#						screen.setState(szString, False)
#					screen.show( szString )

#					# place the health bar
#					if (pLoopUnit.isFighting()):
#						bShowHealth = False
#					elif (pLoopUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
#						bShowHealth = pLoopUnit.canAirAttack()
#					else:
#						bShowHealth = pLoopUnit.canFight()

#					if bShowHealth:
#						szStringHealth = szString + "Health"
#						screen.setBarPercentage( szStringHealth, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
#						if (pLoopUnit.getDamage() >= ((pLoopUnit.maxHitPoints() * 2) / 3)):
#							screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RED"))
#						elif (pLoopUnit.getDamage() >= (pLoopUnit.maxHitPoints() / 3)):
#							screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_YELLOW"))
#						else:
#							screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREEN"))
#						screen.show( szStringHealth )

#					# Adds the overlay first
#					szStringIcon = szString + "Icon"
#					screen.changeDDSGFC( szStringIcon, szFileName )
#					screen.show( szStringIcon )

#					if bEnable:#
#						x = 315 + ((iCount % self.numPlotListButtons()) * 34)
#						y = yResolution - 169 + (iCount / self.numPlotListButtons() - gc.getMAX_PLOT_LIST_ROWS() + 1) * 34

#						self.displayUnitPlotList_Dot( screen, pLoopUnit, szString, iCount, x, y + 4 )
#						self.displayUnitPlotList_Promo( screen, pLoopUnit, szString )
#						self.displayUnitPlotList_Upgrade( screen, pLoopUnit, szString, iCount, x, y )
#						self.displayUnitPlotList_Mission( screen, pLoopUnit, szString, iCount, x, y - 22, 12)

#				iCount = iCount + 1

#		if (iVisibleUnits > self.numPlotListButtons() * iMaxRows):
#			screen.enable("PlotListMinus", bLeftArrow)
#			screen.show( "PlotListMinus" )

#			screen.enable("PlotListPlus", bRightArrow)
#			screen.show( "PlotListPlus" )
#		else:
#			screen.hide( "PlotListMinus" )
#			screen.hide( "PlotListPlus" )

		return 0
# BUG - BUG unit plot draw method - end


		
	# This will update the flag widget for SP hotseat and dbeugging
	def updateFlag( self ):

		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START ):
			screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
			xResolution = screen.getXResolution()
			yResolution = screen.getYResolution()
			screen.addFlagWidgetGFC( "CivilizationFlag", xResolution - 288, yResolution - 138, 68, 250, gc.getGame().getActivePlayer(), WidgetTypes.WIDGET_FLAG, gc.getGame().getActivePlayer(), -1)
		
	# Will hide and show the selection buttons and their associated buttons
	def updateSelectionButtons( self ):
	
		global SELECTION_BUTTON_COLUMNS
		global MAX_SELECTION_BUTTONS
		global g_pSelectedUnit

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()
		
		global g_NumEmphasizeInfos
		global g_NumCityTabTypes
		global g_NumHurryInfos
		global g_NumUnitClassInfos
		global g_NumBuildingClassInfos
		global g_NumProjectInfos
		global g_NumProcessInfos
		global g_NumActionInfos
		
		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		
		screen.addMultiListControlGFC( "BottomButtonContainer", u"", iMultiListXL, yResolution - 113, xResolution - (iMultiListXL+iMultiListXR), 100, 4, 48, 48, TableStyles.TABLE_STYLE_STANDARD )
		screen.clearMultiList( "BottomButtonContainer" )
		screen.hide( "BottomButtonContainer" )
		
		# All of the hides...	
		self.setMinimapButtonVisibility(False)

		screen.hideList( 0 )

		for i in range (g_NumEmphasizeInfos):
			szButtonID = "Emphasize" + str(i)
			screen.hide( szButtonID )

		# Hurry button show...
		for i in range( g_NumHurryInfos ):
			szButtonID = "Hurry" + str(i)
			screen.hide( szButtonID )

		# Conscript Button Show
		screen.hide( "Conscript" )
		#screen.hide( "Liberate" )
		screen.hide( "AutomateProduction" )
		screen.hide( "AutomateCitizens" )

		if (not CyEngine().isGlobeviewUp() and pHeadSelectedCity):
		
			self.setMinimapButtonVisibility(True)

			if ((pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer()) or gc.getGame().isDebugMode()):
			
				iBtnX = xResolution - 284
				iBtnY = yResolution - 177
				iBtnW = 64
				iBtnH = 30

				# Liberate button
				#szText = "<font=1>" + localText.getText("TXT_KEY_LIBERATE_CITY", ()) + "</font>"
				#screen.setButtonGFC( "Liberate", szText, "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_LIBERATE_CITY, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				#screen.setStyle( "Liberate", "Button_CityT1_Style" )
				#screen.hide( "Liberate" )

				iBtnSX = xResolution - 284
				
				iBtnX = iBtnSX
				iBtnY = yResolution - 140
				iBtnW = 64
				iBtnH = 30

				# Conscript button
				szText = "<font=1>" + localText.getText("TXT_KEY_DRAFT", ()) + "</font>"
				screen.setButtonGFC( "Conscript", szText, "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_CONSCRIPT, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "Conscript", "Button_CityT1_Style" )
				screen.hide( "Conscript" )

				iBtnY += iBtnH
				iBtnW = 32
				iBtnH = 28
				
				# Hurry Buttons		
				screen.setButtonGFC( "Hurry0", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_HURRY, 0, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "Hurry0", "Button_CityC1_Style" )
				screen.hide( "Hurry0" )

				iBtnX += iBtnW

				screen.setButtonGFC( "Hurry1", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_HURRY, 1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "Hurry1", "Button_CityC2_Style" )
				screen.hide( "Hurry1" )
			
				iBtnX = iBtnSX
				iBtnY += iBtnH
			
				# Automate Production Button
				screen.addCheckBoxGFC( "AutomateProduction", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_AUTOMATE_PRODUCTION, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "AutomateProduction", "Button_CityC3_Style" )

				iBtnX += iBtnW

				# Automate Citizens Button
				screen.addCheckBoxGFC( "AutomateCitizens", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_AUTOMATE_CITIZENS, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "AutomateCitizens", "Button_CityC4_Style" )

				iBtnY += iBtnH
				iBtnX = iBtnSX

				iBtnW	= 22
				iBtnWa	= 20
				iBtnH	= 24
				iBtnHa	= 27
			
				# Set Emphasize buttons
				i = 0
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW, iBtnY, iBtnWa, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW+iBtnWa, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				iBtnY += iBtnH
				
				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX, iBtnY, iBtnW, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW, iBtnY, iBtnWa, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW+iBtnWa, iBtnY, iBtnW, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )
				
				g_pSelectedUnit = 0
				screen.setState( "AutomateCitizens", pHeadSelectedCity.isCitizensAutomated() )
				screen.setState( "AutomateProduction", pHeadSelectedCity.isProductionAutomated() )
				
				for i in range (g_NumEmphasizeInfos):
					szButtonID = "Emphasize" + str(i)
					screen.show( szButtonID )
					if ( pHeadSelectedCity.AI_isEmphasize(i) ):
						screen.setState( szButtonID, True )
					else:
						screen.setState( szButtonID, False )

				# City Tabs
				for i in range( g_NumCityTabTypes ):
					szButtonID = "CityTab" + str(i)
					screen.show( szButtonID )

				# Hurry button show...
				for i in range( g_NumHurryInfos ):
					szButtonID = "Hurry" + str(i)
					screen.show( szButtonID )
					screen.enable( szButtonID, pHeadSelectedCity.canHurry(i, False) )

				# Conscript Button Show
				screen.show( "Conscript" )
				if (pHeadSelectedCity.canConscript()):
					screen.enable( "Conscript", True )
				else:
					screen.enable( "Conscript", False )

				# Liberate Button Show
				#screen.show( "Liberate" )
				#if (-1 != pHeadSelectedCity.getLiberationPlayer()):
				#	screen.enable( "Liberate", True )
				#else:
				#	screen.enable( "Liberate", False )

				iCount = 0
				iRow = 0
				bFound = False

				# Units to construct
				for i in range ( g_NumUnitClassInfos ):
					eLoopUnit = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationUnits(i)

					if (pHeadSelectedCity.canTrain(eLoopUnit, False, True)):
						szButton = gc.getPlayer(pHeadSelectedCity.getOwner()).getUnitButton(eLoopUnit)
						screen.appendMultiListButton( "BottomButtonContainer", szButton, iRow, WidgetTypes.WIDGET_TRAIN, i, -1, False )
						screen.show( "BottomButtonContainer" )
						
						if ( not pHeadSelectedCity.canTrain(eLoopUnit, False, False) ):
							screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, szButton)
						
						iCount = iCount + 1
						bFound = True

				iCount = 0
				if (bFound):
					iRow = iRow + 1
				bFound = False

				# Buildings to construct
				for i in range ( g_NumBuildingClassInfos ):
					if (not isLimitedWonderClass(i)):
						eLoopBuilding = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationBuildings(i)

						if (pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False)):
							screen.appendMultiListButton( "BottomButtonContainer", gc.getBuildingInfo(eLoopBuilding).getButton(), iRow, WidgetTypes.WIDGET_CONSTRUCT, i, -1, False )
							screen.show( "BottomButtonContainer" )
							
							if ( not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False) ):
								screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, gc.getBuildingInfo(eLoopBuilding).getButton() )

							iCount = iCount + 1
							bFound = True

				iCount = 0
				if (bFound):
					iRow = iRow + 1
				bFound = False

				# Wonders to construct
				i = 0
				for i in range( g_NumBuildingClassInfos ):
					if (isLimitedWonderClass(i)):
						eLoopBuilding = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationBuildings(i)

						if (pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False)):
							screen.appendMultiListButton( "BottomButtonContainer", gc.getBuildingInfo(eLoopBuilding).getButton(), iRow, WidgetTypes.WIDGET_CONSTRUCT, i, -1, False )
							screen.show( "BottomButtonContainer" )
							
							if ( not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False) ):
								screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, gc.getBuildingInfo(eLoopBuilding).getButton() )

							iCount = iCount + 1
							bFound = True

				iCount = 0
				if (bFound):
					iRow = iRow + 1
				bFound = False

				# Projects
				i = 0
				for i in range( g_NumProjectInfos ):
					if (pHeadSelectedCity.canCreate(i, False, True)):
						screen.appendMultiListButton( "BottomButtonContainer", gc.getProjectInfo(i).getButton(), iRow, WidgetTypes.WIDGET_CREATE, i, -1, False )
						screen.show( "BottomButtonContainer" )
						
						if ( not pHeadSelectedCity.canCreate(i, False, False) ):
							screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, gc.getProjectInfo(i).getButton() )
						
						iCount = iCount + 1
						bFound = True

				# Processes
				i = 0
				for i in range( g_NumProcessInfos ):
					if (pHeadSelectedCity.canMaintain(i, False)):
						screen.appendMultiListButton( "BottomButtonContainer", gc.getProcessInfo(i).getButton(), iRow, WidgetTypes.WIDGET_MAINTAIN, i, -1, False )
						screen.show( "BottomButtonContainer" )
						
						iCount = iCount + 1
						bFound = True

				screen.selectMultiList( "BottomButtonContainer", CyInterface().getCityTabSelectionRow() )
							
		elif (not CyEngine().isGlobeviewUp() and pHeadSelectedUnit and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY):

			self.setMinimapButtonVisibility(True)

			if (CyInterface().getInterfaceMode() == InterfaceModeTypes.INTERFACEMODE_SELECTION):
			
				if ( pHeadSelectedUnit.getOwner() == gc.getGame().getActivePlayer() and g_pSelectedUnit != pHeadSelectedUnit ):
				
					g_pSelectedUnit = pHeadSelectedUnit
					
					iCount = 0

					actions = CyInterface().getActionsToShow()
					for i in actions:
						screen.appendMultiListButton( "BottomButtonContainer", gc.getActionInfo(i).getButton(), 0, WidgetTypes.WIDGET_ACTION, i, -1, False )
						screen.show( "BottomButtonContainer" )
				
						if ( not CyInterface().canHandleAction(i, False) ):
							screen.disableMultiListButton( "BottomButtonContainer", 0, iCount, gc.getActionInfo(i).getButton() )
							
						if ( pHeadSelectedUnit.isActionRecommended(i) ):#or gc.getActionInfo(i).getCommandType() == CommandTypes.COMMAND_PROMOTION ):
							screen.enableMultiListPulse( "BottomButtonContainer", True, 0, iCount )
						else:
							screen.enableMultiListPulse( "BottomButtonContainer", False, 0, iCount )

						iCount = iCount + 1

					if (CyInterface().canCreateGroup()):
						screen.appendMultiListButton( "BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CREATEGROUP").getPath(), 0, WidgetTypes.WIDGET_CREATE_GROUP, -1, -1, False )
						screen.show( "BottomButtonContainer" )
						
						iCount = iCount + 1

					if (CyInterface().canDeleteGroup()):
						screen.appendMultiListButton( "BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_SPLITGROUP").getPath(), 0, WidgetTypes.WIDGET_DELETE_GROUP, -1, -1, False )
						screen.show( "BottomButtonContainer" )
						
						iCount = iCount + 1

		elif (CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY):
		
			self.setMinimapButtonVisibility(True)

		return 0
		
	# Will update the research buttons
	def updateResearchButtons( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		for i in range( gc.getNumTechInfos() ):
			szName = "ResearchButton" + str(i)
			screen.hide( szName )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		#screen.hide( "InterfaceOrnamentLeftLow" )
		#screen.hide( "InterfaceOrnamentRightLow" )
			
		for i in range(gc.getNumReligionInfos()):
			szName = "ReligionButton" + str(i)
			screen.hide( szName )

		i = 0
		if ( CyInterface().shouldShowResearchButtons() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			iCount = 0
			
			for i in range( gc.getNumTechInfos() ):
				if (gc.getActivePlayer().canResearch(i, False)):
					if (iCount < 20):
						szName = "ResearchButton" + str(i)

						bDone = False
						for j in range( gc.getNumReligionInfos() ):
							if ( not bDone ):
								if (gc.getReligionInfo(j).getTechPrereq() == i):
									if not (gc.getGame().isReligionSlotTaken(j)):
										szName = "ReligionButton" + str(j)
										bDone = True

						screen.show( szName )
						self.setResearchButtonPosition(szName, iCount)

					iCount = iCount + 1
					
		return 0
		
# BUG - city specialist - start
	def updateCitizenButtons_hide( self ):

		global MAX_CITIZEN_BUTTONS
		
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		for i in range( MAX_CITIZEN_BUTTONS ):
			szName = "FreeSpecialist" + str(i)
			screen.hide( szName )
			szName = "AngryCitizen" + str(i)
			screen.hide( szName )
			szName = "AngryCitizenChevron" + str(i)
			screen.hide( szName )

		for i in range( gc.getNumSpecialistInfos() ):
			szName = "IncreaseSpecialist" + str(i)
			screen.hide( szName )
			szName = "DecreaseSpecialist" + str(i)
			screen.hide( szName )
			szName = "CitizenDisabledButton" + str(i)
			screen.hide( szName )
			for j in range(MAX_CITIZEN_BUTTONS):
				szName = "CitizenButton" + str((i * 100) + j)
				screen.hide( szName )
				szName = "CitizenButtonHighlight" + str((i * 100) + j)
				screen.hide( szName )
				szName = "CitizenChevron" + str((i * 100) + j)
				screen.hide( szName )

				szName = "IncresseCitizenButton" + str((i * 100) + j)
				screen.hide( szName )
				szName = "IncresseCitizenBanner" + str((i * 100) + j)
				screen.hide( szName )
				szName = "DecresseCitizenButton" + str((i * 100) + j)
				screen.hide( szName )
				szName = "CitizenButtonHighlight" + str((i * 100) + j)
				screen.hide( szName )

		global g_iSuperSpecialistCount
		global g_iCitySpecialistCount
		global g_iAngryCitizensCount

		screen.hide( "SpecialistBackground" )
		screen.hide( "SpecialistLabel" )

		for i in range( g_iSuperSpecialistCount ):
			szName = "FreeSpecialist" + str(i)
			screen.hide( szName )
		for i in range( g_iAngryCitizensCount ):
			szName = "AngryCitizen" + str(i)
			screen.hide( szName )

		for i in range( gc.getNumSpecialistInfos() ):
			for k in range( g_iCitySpecialistCount ):
				szName = "IncresseCitizenBanner" + str((i * 100) + k)					
				screen.hide( szName )
				szName = "IncresseCitizenButton" + str((i * 100) + k)					
				screen.hide( szName )
				szName = "DecresseCitizenButton" + str((i * 100) + k)					
				screen.hide( szName )

		return 0
# BUG - city specialist - end


	# Will update the citizen buttons
	def updateCitizenButtons( self ):

		if not CyInterface().isCityScreenUp(): return 0

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		if not (pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW): return 0
	
		global MAX_CITIZEN_BUTTONS
		
		bHandled = False
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		if ( pHeadSelectedCity.angryPopulation(0) < MAX_CITIZEN_BUTTONS ):
			iCount = pHeadSelectedCity.angryPopulation(0)
		else:
			iCount = MAX_CITIZEN_BUTTONS

		for i in range(iCount):
			bHandled = True
			szName = "AngryCitizen" + str(i)
			screen.show( szName )

		iFreeSpecialistCount = 0
		for i in range(gc.getNumSpecialistInfos()):
			iFreeSpecialistCount += pHeadSelectedCity.getFreeSpecialistCount(i)

		iCount = 0

		bHandled = False
		
		if (iFreeSpecialistCount > MAX_CITIZEN_BUTTONS):
			for i in range(gc.getNumSpecialistInfos()):
				if (pHeadSelectedCity.getFreeSpecialistCount(i) > 0):
					if (iCount < MAX_CITIZEN_BUTTONS):
						szName = "FreeSpecialist" + str(iCount)
						screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - 74  - (26 * iCount)), yResolution - 214, 24, 24, WidgetTypes.WIDGET_FREE_CITIZEN, i, 1 )
						screen.show( szName )
						bHandled = true
					iCount += 1
					
		else:				
			for i in range(gc.getNumSpecialistInfos()):
				for j in range( pHeadSelectedCity.getFreeSpecialistCount(i) ):
					if (iCount < MAX_CITIZEN_BUTTONS):
						szName = "FreeSpecialist" + str(iCount)
						screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - 74  - (26 * iCount)), yResolution - 214, 24, 24, WidgetTypes.WIDGET_FREE_CITIZEN, i, -1 )
						screen.show( szName )
						bHandled = true

					iCount = iCount + 1

		for i in range( gc.getNumSpecialistInfos() ):
		
			bHandled = False

			if (pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer() or gc.getGame().isDebugMode()):
			
				if (pHeadSelectedCity.isCitizensAutomated()):
					iSpecialistCount = max(pHeadSelectedCity.getSpecialistCount(i), pHeadSelectedCity.getForceSpecialistCount(i))
				else:
					iSpecialistCount = pHeadSelectedCity.getSpecialistCount(i)
			
				if (pHeadSelectedCity.isSpecialistValid(i, 1) and (pHeadSelectedCity.isCitizensAutomated() or iSpecialistCount < (pHeadSelectedCity.getPopulation() + pHeadSelectedCity.totalFreeSpecialists()))):
					szName = "IncreaseSpecialist" + str(i)
					screen.show( szName )
					szName = "CitizenDisabledButton" + str(i)
					screen.show( szName )

				if iSpecialistCount > 0:
					szName = "CitizenDisabledButton" + str(i)
					screen.hide( szName )
					szName = "DecreaseSpecialist" + str(i)
					screen.show( szName )
					
			if (pHeadSelectedCity.getSpecialistCount(i) < MAX_CITIZEN_BUTTONS):
				iCount = pHeadSelectedCity.getSpecialistCount(i)
			else:
				iCount = MAX_CITIZEN_BUTTONS

			j = 0
			for j in range( iCount ):
				bHandled = True
				szName = "CitizenButton" + str((i * 100) + j)
				screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution - 74 - (26 * j), (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL )
				screen.show( szName )
				szName = "CitizenButtonHighlight" + str((i * 100) + j)
				screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xResolution - 74 - (26 * j), (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j )
				if ( pHeadSelectedCity.getForceSpecialistCount(i) > j ):
					screen.show( szName )
				else:
					screen.hide( szName )
				
			if ( not bHandled ):
				szName = "CitizenDisabledButton" + str(i)
				screen.show( szName )

		return 0

# BUG - city specialist - start
	def updateCitizenButtons_Stacker( self ):
	
		if not CyInterface().isCityScreenUp(): return 0

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		if not (pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW): return 0

		global g_iSuperSpecialistCount
		global g_iCitySpecialistCount
		global g_iAngryCitizensCount
		
		bHandled = False
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		currentAngryCitizenCount = pHeadSelectedCity.angryPopulation(0)
		
		if(currentAngryCitizenCount > 0):
			stackWidth = 220 / currentAngryCitizenCount
			if (stackWidth > MAX_SPECIALIST_BUTTON_SPACING):
				stackWidth = MAX_SPECIALIST_BUTTON_SPACING

		for i in range(currentAngryCitizenCount):
			bHandled = True
			szName = "AngryCitizen" + str(i)
			screen.setImageButton( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_ANGRYCITIZEN_TEXTURE").getPath(), xResolution - SPECIALIST_AREA_MARGIN - (stackWidth * i), yResolution - (282- SPECIALIST_ROW_HEIGHT), 30, 30, WidgetTypes.WIDGET_ANGRY_CITIZEN, -1, -1 )
			screen.show( szName )
			
		# update the max ever citizen counts
		if g_iAngryCitizensCount < currentAngryCitizenCount:
			g_iAngryCitizensCount = currentAngryCitizenCount

		iCount = 0
		bHandled = False
		currentSuperSpecialistCount = 0

		for i in range(gc.getNumSpecialistInfos()):
			if(pHeadSelectedCity.getFreeSpecialistCount(i) > 0):
				currentSuperSpecialistCount = currentSuperSpecialistCount + pHeadSelectedCity.getFreeSpecialistCount(i)

		if(currentSuperSpecialistCount > 0):
			stackWidth = 220 / currentSuperSpecialistCount 
			if (stackWidth > MAX_SPECIALIST_BUTTON_SPACING):
				stackWidth = MAX_SPECIALIST_BUTTON_SPACING

		for i in range(gc.getNumSpecialistInfos()):
			for j in range( pHeadSelectedCity.getFreeSpecialistCount(i) ):

				szName = "FreeSpecialist" + str(iCount)
				screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - SPECIALIST_AREA_MARGIN  - (stackWidth * iCount)), yResolution - (282 - SPECIALIST_ROW_HEIGHT * 2), 30, 30, WidgetTypes.WIDGET_FREE_CITIZEN, i, 1 )
				screen.show( szName )
				bHandled = true

				iCount = iCount + 1

		# update the max ever citizen counts
		if g_iSuperSpecialistCount < iCount:
			g_iSuperSpecialistCount = iCount

		iXShiftVal = 0
		iYShiftVal = 0
		iSpecialistCount = 0

		for i in range( gc.getNumSpecialistInfos() ):
		
			bHandled = False
			if( iSpecialistCount > SPECIALIST_ROWS ):
				iXShiftVal = 115
				iYShiftVal = (iSpecialistCount % SPECIALIST_ROWS) + 1
			else:
				iYShiftVal = iSpecialistCount

			if (gc.getSpecialistInfo(i).isVisible()):
				iSpecialistCount = iSpecialistCount + 1					
				
			if (gc.getPlayer(pHeadSelectedCity.getOwner()).isSpecialistValid(i) or i == 0):
				iCount = (pHeadSelectedCity.getPopulation() - pHeadSelectedCity.angryPopulation(0)) +  pHeadSelectedCity.totalFreeSpecialists()
			else:
				iCount = pHeadSelectedCity.getMaxSpecialistCount(i)

			# update the max ever citizen counts
			if g_iCitySpecialistCount < iCount:
				g_iCitySpecialistCount = iCount

			RowLength = 110
			if (i == 0):
			#if (i == gc.getInfoTypeForString(gc.getDefineSTRING("DEFAULT_SPECIALIST"))):
				RowLength *= 2
			
			HorizontalSpacing = MAX_SPECIALIST_BUTTON_SPACING	
			if (iCount > 0):
				HorizontalSpacing = RowLength / iCount
			if (HorizontalSpacing > MAX_SPECIALIST_BUTTON_SPACING):
				HorizontalSpacing = MAX_SPECIALIST_BUTTON_SPACING
									
			for k in range (iCount):
				if (k  >= pHeadSelectedCity.getSpecialistCount(i)):
					szName = "IncresseCitizenBanner" + str((i * 100) + k)					
					screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution - (SPECIALIST_AREA_MARGIN + iXShiftVal) - (HorizontalSpacing * k), (yResolution - 282 - (SPECIALIST_ROW_HEIGHT * iYShiftVal)), 30, 30, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1, ButtonStyles.BUTTON_STYLE_LABEL )
					screen.enable( szName, False )
					screen.show( szName )
					
					szName = "IncresseCitizenButton" + str((i * 100) + k)					
					screen.addCheckBoxGFC( szName, "", "", xResolution - (SPECIALIST_AREA_MARGIN + iXShiftVal) - (HorizontalSpacing * k), (yResolution - 282 - (SPECIALIST_ROW_HEIGHT * iYShiftVal)), 30, 30, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1, ButtonStyles.BUTTON_STYLE_LABEL )					
					screen.show( szName )

				else:
					szName = "DecresseCitizenButton" + str((i * 100) + k)					
					screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution - (SPECIALIST_AREA_MARGIN + iXShiftVal) - (HorizontalSpacing * k), (yResolution - 282 - (SPECIALIST_ROW_HEIGHT * iYShiftVal)), 30, 30, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
					screen.show( szName )
					
		screen.show( "SpecialistBackground" )
		screen.show( "SpecialistLabel" )
	
		return 0
# BUG - city specialist - end

# BUG - city specialist - start
	def updateCitizenButtons_Chevron( self ):
	
		if not CyInterface().isCityScreenUp(): return 0

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		if not (pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW): return 0

		global MAX_CITIZEN_BUTTONS
		
		bHandled = False
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()


		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		iCount = pHeadSelectedCity.angryPopulation(0)

		j = 0
		while (iCount > 0):
			bHandled = True
			szName = "AngryCitizen" + str(j)
			screen.show( szName )

			xCoord = xResolution - 74 - (26 * j)
			yCoord = yResolution - 238

			szName = "AngryCitizenChevron" + str(j)
			if iCount >= 20:
				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON20").getPath()
				iCount -= 20
			elif iCount >= 10:
				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON10").getPath()
				iCount -= 10
			elif iCount >= 5:
				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON5").getPath()
				iCount -= 5
			else:
				szFileName = ""
				iCount -= 1

			if (szFileName != ""):
				screen.addDDSGFC( szName , szFileName, xCoord, yCoord, 10, 10, WidgetTypes.WIDGET_CITIZEN, j, False )
				screen.show( szName )

			j += 1

		iFreeSpecialistCount = 0
		for i in range(gc.getNumSpecialistInfos()):
			iFreeSpecialistCount += pHeadSelectedCity.getFreeSpecialistCount(i)

		iCount = 0

		bHandled = False
		
		if (iFreeSpecialistCount > MAX_CITIZEN_BUTTONS):
			for i in range(gc.getNumSpecialistInfos()):
				if (pHeadSelectedCity.getFreeSpecialistCount(i) > 0):
					if (iCount < MAX_CITIZEN_BUTTONS):
						szName = "FreeSpecialist" + str(iCount)
						screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - 74  - (26 * iCount)), yResolution - 214, 24, 24, WidgetTypes.WIDGET_FREE_CITIZEN, i, 1 )
						screen.show( szName )
						bHandled = True
					iCount += 1
					
		else:				
			for i in range(gc.getNumSpecialistInfos()):
				for j in range( pHeadSelectedCity.getFreeSpecialistCount(i) ):
					if (iCount < MAX_CITIZEN_BUTTONS):
						szName = "FreeSpecialist" + str(iCount)
						screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - 74  - (26 * iCount)), yResolution - 214, 24, 24, WidgetTypes.WIDGET_FREE_CITIZEN, i, -1 )
						screen.show( szName )
						bHandled = True

					iCount = iCount + 1

		for i in range( gc.getNumSpecialistInfos() ):
		
			bHandled = False

			if (pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer() or gc.getGame().isDebugMode()):
			
				if (pHeadSelectedCity.isCitizensAutomated()):
					iSpecialistCount = max(pHeadSelectedCity.getSpecialistCount(i), pHeadSelectedCity.getForceSpecialistCount(i))
				else:
					iSpecialistCount = pHeadSelectedCity.getSpecialistCount(i)
			
				if (pHeadSelectedCity.isSpecialistValid(i, 1) and (pHeadSelectedCity.isCitizensAutomated() or iSpecialistCount < (pHeadSelectedCity.getPopulation() + pHeadSelectedCity.totalFreeSpecialists()))):
					szName = "IncreaseSpecialist" + str(i)
					screen.show( szName )
					szName = "CitizenDisabledButton" + str(i)
					screen.show( szName )

				if iSpecialistCount > 0:
					szName = "CitizenDisabledButton" + str(i)
					screen.hide( szName )
					szName = "DecreaseSpecialist" + str(i)
					screen.show( szName )
					
			iCount = pHeadSelectedCity.getSpecialistCount(i)

			j = 0
			while (iCount > 0):
				bHandled = True

				xCoord = xResolution - 74 - (26 * j)
				yCoord = yResolution - 272 - (26 * i)

				szName = "CitizenButton" + str((i * 100) + j)
				screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL )
				screen.show( szName )

				szName = "CitizenChevron" + str((i * 100) + j)
				if iCount >= 20:
					szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON20").getPath()
					iCount -= 20
				elif iCount >= 10:
					szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON10").getPath()
					iCount -= 10
				elif iCount >= 5:
					szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON5").getPath()
					iCount -= 5
				else:
					szFileName = ""
					iCount -= 1

				if (szFileName != ""):
					screen.addDDSGFC( szName , szFileName, xCoord, yCoord, 10, 10, WidgetTypes.WIDGET_CITIZEN, i, False )
					screen.show( szName )

				j += 1

			if ( not bHandled ):
				szName = "CitizenDisabledButton" + str(i)
				screen.show( szName )

		return 0
# BUG - city specialist - end

	# Will update the game data strings
	def updateGameDataStrings( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		screen.hide( "ResearchText" )
		screen.hide( "GoldText" )
		screen.hide( "TimeText" )
		screen.hide( "ResearchBar" )

# BUG - NJAGC - start
		screen.hide( "EraText" )
# BUG - NJAGC - end

# BUG - Great Person Bar - start
		screen.hide( "GreatPersonBar" )
		screen.hide( "GreatPersonBarText" )
# BUG - Great Person Bar - end

# BUG - Great General Bar - start
		screen.hide( "GreatGeneralBar" )
		screen.hide( "GreatGeneralBarText" )
# BUG - Great General Bar - end

# BUG - Bars on single line for higher resolution screens - start
		screen.hide( "GreatGeneralBar-w" )
		screen.hide( "ResearchBar-w" )
		screen.hide( "GreatPersonBar-w" )
# BUG - Bars on single line for higher resolution screens - end

# BUG - Progress Bar - Tick Marks - start
		self.pBarResearchBar_n.hide(screen)
		self.pBarResearchBar_w.hide(screen)
# BUG - Progress Bar - Tick Marks - end

		bShift = CyInterface().shiftKey()
		
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if (pHeadSelectedCity):
			ePlayer = pHeadSelectedCity.getOwner()
		else:
			ePlayer = gc.getGame().getActivePlayer()

		if ( ePlayer < 0 or ePlayer >= gc.getMAX_PLAYERS() ):
			return 0

		for iI in range(CommerceTypes.NUM_COMMERCE_TYPES):
			szString = "PercentText" + str(iI)
			screen.hide(szString)
			szString = "RateText" + str(iI)
			screen.hide(szString)

		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY  and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):

			# Percent of commerce
			if (gc.getPlayer(ePlayer).isAlive()):
				iCount = 0
				for iI in range( CommerceTypes.NUM_COMMERCE_TYPES ):
					eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES
					if (gc.getPlayer(ePlayer).isCommerceFlexible(eCommerce) or (CyInterface().isCityScreenUp() and (eCommerce == CommerceTypes.COMMERCE_GOLD))):
						szOutText = u"<font=2>%c:%d%%</font>" %(gc.getCommerceInfo(eCommerce).getChar(), gc.getPlayer(ePlayer).getCommercePercent(eCommerce))
						szString = "PercentText" + str(iI)
						screen.setLabel( szString, "Background", szOutText, CvUtil.FONT_LEFT_JUSTIFY, 14, 50 + (iCount * 19), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.show( szString )

						if not CyInterface().isCityScreenUp():
							szOutText = u"<font=2>" + localText.getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", (gc.getPlayer(ePlayer).getCommerceRate(CommerceTypes(eCommerce)), )) + u"</font>"
							szString = "RateText" + str(iI)
# BUG - Min/Max Sliders - start
							if MainOpt.isShowMinMaxCommerceButtons():
								iMinMaxAdjustX = 40
							else:
								iMinMaxAdjustX = 0
							screen.setLabel( szString, "Background", szOutText, CvUtil.FONT_LEFT_JUSTIFY, 112 + iMinMaxAdjustX, 50 + (iCount * 19), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
# BUG - Min/Max Sliders - end
							screen.show( szString )

						iCount = iCount + 1;

			self.updateTimeText()
			screen.setLabel( "TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 56, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.show( "TimeText" )
			
			if (gc.getPlayer(ePlayer).isAlive()):
				
# BUG - Gold Rate Warning - start
				if MainOpt.isGoldRateWarning():
					pPlayer = gc.getPlayer(ePlayer)
					iGold = pPlayer.getGold()
					iGoldRate = pPlayer.calculateGoldRate()
					if iGold < 0:
						szText = BugUtil.getText("TXT_KEY_MISC_NEG_GOLD", iGold)
						if iGoldRate != 0:
							if iGold + iGoldRate >= 0:
								szText += BugUtil.getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", iGoldRate)
							elif iGoldRate >= 0:
								szText += BugUtil.getText("TXT_KEY_MISC_POS_WARNING_GOLD_PER_TURN", iGoldRate)
							else:
								szText += BugUtil.getText("TXT_KEY_MISC_NEG_GOLD_PER_TURN", iGoldRate)
					else:
						szText = BugUtil.getText("TXT_KEY_MISC_POS_GOLD", iGold)
						if iGoldRate != 0:
							if iGoldRate >= 0:
								szText += BugUtil.getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", iGoldRate)
							elif iGold + iGoldRate >= 0:
								szText += BugUtil.getText("TXT_KEY_MISC_NEG_WARNING_GOLD_PER_TURN", iGoldRate)
							else:
								szText += BugUtil.getText("TXT_KEY_MISC_NEG_GOLD_PER_TURN", iGoldRate)
					if pPlayer.isStrike():
						szText += BugUtil.getPlainText("TXT_KEY_MISC_STRIKE")
				else:
					szText = CyGameTextMgr().getGoldStr(ePlayer)
# BUG - Gold Rate Warning - end
				screen.setLabel( "GoldText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 12, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.show( "GoldText" )
				
				if (((gc.getPlayer(ePlayer).calculateGoldRate() != 0) and not (gc.getPlayer(ePlayer).isAnarchy())) or (gc.getPlayer(ePlayer).getGold() != 0)):
					screen.show( "GoldText" )

# BUG - NJAGC - start
				if (ClockOpt.isEnabled()
				and ClockOpt.isShowEra()):
					szText = localText.getText("TXT_KEY_BUG_ERA", (gc.getEraInfo(gc.getPlayer(ePlayer).getCurrentEra()).getDescription(), ))
					if(ClockOpt.isUseEraColor()):
						iEraColor = ClockOpt.getEraColor(gc.getEraInfo(gc.getPlayer(ePlayer).getCurrentEra()).getType())
						if (iEraColor >= 0):
							szText = localText.changeTextColor(szText, iEraColor)
					screen.setLabel( "EraText", "Background", szText, CvUtil.FONT_RIGHT_JUSTIFY, 250, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "EraText" )
# BUG - NJAGC - end
				
				if (gc.getPlayer(ePlayer).isAnarchy()):
				
# BUG - Bars on single line for higher resolution screens - start
					if (xResolution >= 1440
					and (MainOpt.isShowGGProgressBar() or MainOpt.isShowGPProgressBar())):
						xCoord = 268 + (xResolution - 1440) / 2 + 84 + 6 + 487 / 2
					else:
						xCoord = screen.centerX(512)

					yCoord = 5  # Ruff: this use to be 3 but I changed it so it lines up with the Great Person Bar
					szText = localText.getText("INTERFACE_ANARCHY", (gc.getPlayer(ePlayer).getAnarchyTurns(), ))
					screen.setText( "ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
# BUG - Bars on single line for higher resolution screens - end

					if ( gc.getPlayer(ePlayer).getCurrentResearch() != -1 ):
						screen.show( "ResearchText" )
					else:
						screen.hide( "ResearchText" )
					
				elif (gc.getPlayer(ePlayer).getCurrentResearch() != -1):

					szText = CyGameTextMgr().getResearchStr(ePlayer)

# BUG - Bars on single line for higher resolution screens - start
					if (xResolution >= 1440
					and (MainOpt.isShowGGProgressBar() or MainOpt.isShowGPProgressBar())):
						szResearchBar = "ResearchBar-w"
						xCoord = 268 + (xResolution - 1440) / 2 + 84 + 6 + 487 / 2
					else:
						szResearchBar = "ResearchBar"
						xCoord = screen.centerX(512)

					yCoord = 5  # Ruff: this use to be 3 but I changed it so it lines up with the Great Person Bar
					screen.setText( "ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
					screen.show( "ResearchText" )
# BUG - Bars on single line for higher resolution screens - end

					researchProgress = gc.getTeam(gc.getPlayer(ePlayer).getTeam()).getResearchProgress(gc.getPlayer(ePlayer).getCurrentResearch())
					overflowResearch = (gc.getPlayer(ePlayer).getOverflowResearch() * gc.getPlayer(ePlayer).calculateResearchModifier(gc.getPlayer(ePlayer).getCurrentResearch()))/100
					researchCost = gc.getTeam(gc.getPlayer(ePlayer).getTeam()).getResearchCost(gc.getPlayer(ePlayer).getCurrentResearch())
					researchRate = gc.getPlayer(ePlayer).calculateResearchRate(-1)
					
					screen.setBarPercentage( szResearchBar, InfoBarTypes.INFOBAR_STORED, float(researchProgress + overflowResearch) / researchCost )
					if ( researchCost >  researchProgress + overflowResearch):
						screen.setBarPercentage( szResearchBar, InfoBarTypes.INFOBAR_RATE, float(researchRate) / (researchCost - researchProgress - overflowResearch))
					else:
						screen.setBarPercentage( szResearchBar, InfoBarTypes.INFOBAR_RATE, 0.0 )

					screen.show( szResearchBar )

# BUG - Progress Bar - Tick Marks - start
					if MainOpt.isShowpBarTickMarks():
						if szResearchBar == "ResearchBar":
							self.pBarResearchBar_n.drawTickMarks(screen, researchProgress + overflowResearch, researchCost, researchRate, researchRate, False)
						else:
							self.pBarResearchBar_w.drawTickMarks(screen, researchProgress + overflowResearch, researchCost, researchRate, researchRate, False)
# BUG - Progress Bar - Tick Marks - end

# BUG - Great Person Bar - start
				self.updateGreatPersonBar(screen)
# BUG - Great Person Bar - end

# BUG - Great General Bar - start
				self.updateGreatGeneralBar(screen)
# BUG - Great General Bar - end
					
		return 0
		
# BUG - Great Person Bar - start
	def updateGreatPersonBar(self, screen):
		if (not CyInterface().isCityScreenUp() and MainOpt.isShowGPProgressBar()):
			pGPCity, iGPTurns = GPUtil.getDisplayCity()
			szText = GPUtil.getGreatPeopleText(pGPCity, iGPTurns, GP_BAR_WIDTH, MainOpt.isGPBarTypesNone(), MainOpt.isGPBarTypesOne(), True)
			szText = u"<font=2>%s</font>" % (szText)
			if (pGPCity):
				iCityID = pGPCity.getID()
			else:
				iCityID = -1
				
# BUG - Bars on single line for higher resolution screens - start
			xResolution = screen.getXResolution()
			if (xResolution >= 1440):
				szGreatPersonBar = "GreatPersonBar-w"
				xCoord = 268 + (xResolution - 1440) / 2 + 84 + 6 + 487 + 6 + 320 / 2
				yCoord = 5
			else:
				szGreatPersonBar = "GreatPersonBar"
				xCoord = 268 + (xResolution - 1024) / 2 + 100 + 7 + 380 / 2
				yCoord = 30

			screen.setText( "GreatPersonBarText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GP_PROGRESS_BAR, -1, -1 )
			if (not pGPCity):
				screen.setHitTest( "GreatPersonBarText", HitTestTypes.HITTEST_NOHIT )
			screen.show( "GreatPersonBarText" )
# BUG - Bars on single line for higher resolution screens - end
			
			if (pGPCity):
				fThreshold = float(gc.getPlayer( pGPCity.getOwner() ).greatPeopleThreshold(False))
				fRate = float(pGPCity.getGreatPeopleRate())
				fFirst = float(pGPCity.getGreatPeopleProgress()) / fThreshold

				screen.setBarPercentage( szGreatPersonBar, InfoBarTypes.INFOBAR_STORED, fFirst )
				if ( fFirst == 1 ):
					screen.setBarPercentage( szGreatPersonBar, InfoBarTypes.INFOBAR_RATE, fRate / fThreshold )
				else:
					screen.setBarPercentage( szGreatPersonBar, InfoBarTypes.INFOBAR_RATE, fRate / fThreshold / ( 1 - fFirst ) )
			else:
				screen.setBarPercentage( szGreatPersonBar, InfoBarTypes.INFOBAR_STORED, 0 )
				screen.setBarPercentage( szGreatPersonBar, InfoBarTypes.INFOBAR_RATE, 0 )

			screen.show( szGreatPersonBar )
# BUG - Great Person Bar - end

# BUG - Great General Bar - start
	def updateGreatGeneralBar(self, screen):
		if (not CyInterface().isCityScreenUp() and MainOpt.isShowGGProgressBar()):
			pPlayer = gc.getActivePlayer()
			iCombatExp = pPlayer.getCombatExperience()
			iThresholdExp = pPlayer.greatPeopleThreshold(True)
			iNeededExp = iThresholdExp - iCombatExp
			
			szText = u"<font=2>%s</font>" %(GGUtil.getGreatGeneralText(iNeededExp))
			
# BUG - Bars on single line for higher resolution screens - start
			xResolution = screen.getXResolution()
			if (xResolution >= 1440):
				szGreatGeneralBar = "GreatGeneralBar-w"
				xCoord = 268 + (xResolution - 1440) / 2 + 84 / 2
				yCoord = 5
			else:
				szGreatGeneralBar = "GreatGeneralBar"
				xCoord = 268 + (xResolution - 1024) / 2 + 100 / 2
				yCoord = 32

			screen.setLabel( "GreatGeneralBarText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1 )
			screen.show( "GreatGeneralBarText" )
# BUG - Bars on single line for higher resolution screens - end

			fProgress = float(iCombatExp) / float(iThresholdExp)
			screen.setBarPercentage( szGreatGeneralBar, InfoBarTypes.INFOBAR_STORED, fProgress )
			screen.show( szGreatGeneralBar )
# BUG - Great General Bar - end
					
	def updateTimeText( self ):
		
		global g_szTimeText
		
		ePlayer = gc.getGame().getActivePlayer()
		
# BUG - NJAGC - start
		if (ClockOpt.isEnabled()):
			"""
			Format: Time - GameTurn/Total Percent - GA (TurnsLeft) Date
			
			Ex: 10:37 - 220/660 33% - GA (3) 1925
			"""
			if (g_bShowTimeTextAlt):
				bShowTime = ClockOpt.isShowAltTime()
				bShowGameTurn = ClockOpt.isShowAltGameTurn()
				bShowTotalTurns = ClockOpt.isShowAltTotalTurns()
				bShowPercentComplete = ClockOpt.isShowAltPercentComplete()
				bShowDateGA = ClockOpt.isShowAltDateGA()
			else:
				bShowTime = ClockOpt.isShowTime()
				bShowGameTurn = ClockOpt.isShowGameTurn()
				bShowTotalTurns = ClockOpt.isShowTotalTurns()
				bShowPercentComplete = ClockOpt.isShowPercentComplete()
				bShowDateGA = ClockOpt.isShowDateGA()
			
			if (not gc.getGame().getMaxTurns() > 0):
				bShowTotalTurns = False
				bShowPercentComplete = False
			
			bFirst = True
			g_szTimeText = ""
			
			if (bShowTime):
				bFirst = False
				g_szTimeText += getClockText()
			
			if (bShowGameTurn):
				if (bFirst):
					bFirst = False
				else:
					g_szTimeText += u" - "
				g_szTimeText += u"%d" %( gc.getGame().getElapsedGameTurns() )
				if (bShowTotalTurns):
					g_szTimeText += u"/%d" %( gc.getGame().getMaxTurns() )
			
			if (bShowPercentComplete):
				if (bFirst):
					bFirst = False
				else:
					if (not bShowGameTurn):
						g_szTimeText += u" - "
					else:
						g_szTimeText += u" "
				g_szTimeText += u"%2.2f%%" %( 100 *(float(gc.getGame().getElapsedGameTurns()) / float(gc.getGame().getMaxTurns())) )
			
			if (bShowDateGA):
				if (bFirst):
					bFirst = False
				else:
					g_szTimeText += u" - "
				szDateGA = unicode(CyGameTextMgr().getInterfaceTimeStr(ePlayer))
				if(ClockOpt.isUseEraColor()):
					iEraColor = ClockOpt.getEraColor(gc.getEraInfo(gc.getPlayer(ePlayer).getCurrentEra()).getType())
					if (iEraColor >= 0):
						szDateGA = localText.changeTextColor(szDateGA, iEraColor)
				g_szTimeText += szDateGA
		else:
			"""
			Original Clock
			Format: Time - 'Turn' GameTurn - GA (TurnsLeft) Date
			
			Ex: 10:37 - Turn 220 - GA (3) 1925
			"""
			g_szTimeText = localText.getText("TXT_KEY_TIME_TURN", (CyGame().getGameTurn(), )) + u" - " + unicode(CyGameTextMgr().getInterfaceTimeStr(ePlayer))
			if (CyUserProfile().isClockOn()):
				g_szTimeText = getClockText() + u" - " + g_szTimeText
# BUG - NJAGC - end
		
	# Will update the selection Data Strings
	def updateCityScreen( self ):
	
		global MAX_DISPLAYABLE_BUILDINGS
		global MAX_DISPLAYABLE_TRADE_ROUTES
		global MAX_BONUS_ROWS
		
		global g_iNumTradeRoutes
		global g_iNumBuildings
		global g_iNumLeftBonus
		global g_iNumCenterBonus
		global g_iNumRightBonus
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		bShift = CyInterface().shiftKey()

		screen.hide( "PopulationBar" )
		screen.hide( "ProductionBar" )
		screen.hide( "GreatPeopleBar" )
		screen.hide( "CultureBar" )
		screen.hide( "MaintenanceText" )
		screen.hide( "MaintenanceAmountText" )

# BUG - Progress Bar - Tick Marks - start
		self.pBarPopulationBar.hide(screen)
		self.pBarProductionBar.hide(screen)
		self.pBarProductionBar_Whip.hide(screen)
# BUG - Progress Bar - Tick Marks - end

# BUG - Raw Commerce - start
		screen.hide("RawYieldsTrade0")
		screen.hide("RawYieldsFood1")
		screen.hide("RawYieldsProduction2")
		screen.hide("RawYieldsCommerce3")
		screen.hide("RawYieldsWorkedTiles4")
		screen.hide("RawYieldsCityTiles5")
		screen.hide("RawYieldsOwnedTiles6")
# BUG - Raw Commerce - end
		
		screen.hide( "NationalityText" )
		screen.hide( "NationalityBar" )
		screen.hide( "DefenseText" )
		screen.hide( "CityScrollMinus" )
		screen.hide( "CityScrollPlus" )
		screen.hide( "CityNameText" )
		screen.hide( "PopulationText" )
		screen.hide( "PopulationInputText" )
		screen.hide( "HealthText" )
		screen.hide( "ProductionText" )
		screen.hide( "ProductionInputText" )
		screen.hide( "HappinessText" )
		screen.hide( "CultureText" )
		screen.hide( "GreatPeopleText" )

		for i in range( gc.getNumReligionInfos() ):
			szName = "ReligionHolyCityDDS" + str(i)
			screen.hide( szName )
			szName = "ReligionDDS" + str(i)
			screen.hide( szName )
			
		for i in range( gc.getNumCorporationInfos() ):
			szName = "CorporationHeadquarterDDS" + str(i)
			screen.hide( szName )
			szName = "CorporationDDS" + str(i)
			screen.hide( szName )
			
		for i in range(CommerceTypes.NUM_COMMERCE_TYPES):
			szName = "CityPercentText" + str(i)
			screen.hide( szName )

		screen.addPanel( "BonusPane0", u"", u"", True, False, xResolution - 244, 94, 57, yResolution - 520, PanelStyles.PANEL_STYLE_CITY_COLUMNL )
		screen.hide( "BonusPane0" )
		screen.addScrollPanel( "BonusBack0", u"", xResolution - 242, 94, 157, yResolution - 536, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.hide( "BonusBack0" )

		screen.addPanel( "BonusPane1", u"", u"", True, False, xResolution - 187, 94, 68, yResolution - 520, PanelStyles.PANEL_STYLE_CITY_COLUMNC )
		screen.hide( "BonusPane1" )
		screen.addScrollPanel( "BonusBack1", u"", xResolution - 191, 94, 184, yResolution - 536, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.hide( "BonusBack1" )

		screen.addPanel( "BonusPane2", u"", u"", True, False, xResolution - 119, 94, 107, yResolution - 520, PanelStyles.PANEL_STYLE_CITY_COLUMNR )
		screen.hide( "BonusPane2" )
		screen.addScrollPanel( "BonusBack2", u"", xResolution - 125, 94, 205, yResolution - 536, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.hide( "BonusBack2" )

		screen.hide( "TradeRouteTable" )
		screen.hide( "BuildingListTable" )
		
		screen.hide( "BuildingListBackground" )
		screen.hide( "TradeRouteListBackground" )
		screen.hide( "BuildingListLabel" )
		screen.hide( "TradeRouteListLabel" )

		i = 0
		for i in range( g_iNumLeftBonus ):
			szName = "LeftBonusItem" + str(i)
			screen.hide( szName )
		
		i = 0
		for i in range( g_iNumCenterBonus ):
			szName = "CenterBonusItemLeft" + str(i)
			screen.hide( szName )
			szName = "CenterBonusItemRight" + str(i)
			screen.hide( szName )
		
		i = 0
		for i in range( g_iNumRightBonus ):
			szName = "RightBonusItemLeft" + str(i)
			screen.hide( szName )
			szName = "RightBonusItemRight" + str(i)
			screen.hide( szName )
			
		i = 0
		for i in range( 3 ):
			szName = "BonusPane" + str(i)
			screen.hide( szName )
			szName = "BonusBack" + str(i)
			screen.hide( szName )

		i = 0
		if ( CyInterface().isCityScreenUp() ):
			if ( pHeadSelectedCity ):
			
				screen.show( "InterfaceTopLeftBackgroundWidget" )
				screen.show( "InterfaceTopRightBackgroundWidget" )
				screen.show( "InterfaceCenterLeftBackgroundWidget" )
				screen.show( "CityScreenTopWidget" )
				screen.show( "CityNameBackground" )
				screen.show( "TopCityPanelLeft" )
				screen.show( "TopCityPanelRight" )
				screen.show( "CityScreenAdjustPanel" )
				screen.show( "InterfaceCenterRightBackgroundWidget" )
				
				if ( pHeadSelectedCity.getTeam() == gc.getGame().getActiveTeam() ):
					if ( gc.getActivePlayer().getNumCities() > 1 ):
						screen.show( "CityScrollMinus" )
						screen.show( "CityScrollPlus" )
				
				# Help Text Area
				screen.setHelpTextArea( 390, FontTypes.SMALL_FONT, 0, 0, -2.2, True, ArtFileMgr.getInterfaceArtInfo("POPUPS_BACKGROUND_TRANSPARENT").getPath(), True, True, CvUtil.FONT_LEFT_JUSTIFY, 0 )

				iFoodDifference = pHeadSelectedCity.foodDifference(True)
				iProductionDiffNoFood = pHeadSelectedCity.getCurrentProductionDifference(True, True)
				iProductionDiffJustFood = (pHeadSelectedCity.getCurrentProductionDifference(False, True) - iProductionDiffNoFood)

				szBuffer = u"<font=4>"
				
				if (pHeadSelectedCity.isCapital()):
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.STAR_CHAR))
				elif (pHeadSelectedCity.isGovernmentCenter()):
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR))

				if (pHeadSelectedCity.isPower()):
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.POWER_CHAR))
					
				szBuffer += u"%s: %d" %(pHeadSelectedCity.getName(), pHeadSelectedCity.getPopulation())

				if (pHeadSelectedCity.isOccupation()):
					szBuffer += u" (%c:%d)" %(CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR), pHeadSelectedCity.getOccupationTimer())

				szBuffer += u"</font>"

				screen.setText( "CityNameText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), 32, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_CITY_NAME, -1, -1 )
				screen.setStyle( "CityNameText", "Button_Stone_Style" )
				screen.show( "CityNameText" )

# BUG - Food Assist - start
				if ( CityUtil.willGrowThisTurn(pHeadSelectedCity) or (iFoodDifference != 0) or not (pHeadSelectedCity.isFoodProduction() ) ):
					if (CityUtil.willGrowThisTurn(pHeadSelectedCity)):
						szBuffer = localText.getText("INTERFACE_CITY_GROWTH", ())
					elif (iFoodDifference > 0):
						szBuffer = localText.getText("INTERFACE_CITY_GROWING", (pHeadSelectedCity.getFoodTurnsLeft(), ))	
					elif (iFoodDifference < 0):
						if (CityScreenOpt.isShowFoodAssist()):
							iTurnsToStarve = pHeadSelectedCity.getFood() / -iFoodDifference + 1
							if iTurnsToStarve > 1:
								szBuffer = localText.getText("INTERFACE_CITY_SHRINKING", (iTurnsToStarve, ))
							else:
								szBuffer = localText.getText("INTERFACE_CITY_STARVING", ()) 
						else:
							szBuffer = localText.getText("INTERFACE_CITY_STARVING", ()) 
# BUG - Food Assist - end
					else:
						szBuffer = localText.getText("INTERFACE_CITY_STAGNANT", ())	

					screen.setLabel( "PopulationText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), iCityCenterRow1Y, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "PopulationText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "PopulationText" )

				if (not pHeadSelectedCity.isDisorder() and not pHeadSelectedCity.isFoodProduction()):
				
# BUG - Food Assist - start
					if (CityScreenOpt.isShowFoodAssist()):
						iFoodYield = pHeadSelectedCity.getYieldRate(YieldTypes.YIELD_FOOD)
						iFoodEaten = pHeadSelectedCity.foodConsumption(False, 0)
						if iFoodYield == iFoodEaten:
							szBuffer = localText.getText("INTERFACE_CITY_FOOD_STAGNATE", (iFoodYield, iFoodEaten))
						elif iFoodYield > iFoodEaten:
							szBuffer = localText.getText("INTERFACE_CITY_FOOD_GROW", (iFoodYield, iFoodEaten, iFoodYield - iFoodEaten))
						else:
							szBuffer = localText.getText("INTERFACE_CITY_FOOD_SHRINK", (iFoodYield, iFoodEaten, iFoodYield - iFoodEaten))
					else:
						szBuffer = u"%d%c - %d%c" %(pHeadSelectedCity.getYieldRate(YieldTypes.YIELD_FOOD), gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar(), pHeadSelectedCity.foodConsumption(False, 0), CyGame().getSymbolID(FontSymbols.EATEN_FOOD_CHAR))
# BUG - Food Assist - end
# BUG - Food Rate Hover - start
					# draw label below
					
				else:

					szBuffer = u"%d%c" %(iFoodDifference, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar())
					# draw label below

				screen.setLabel( "PopulationInputText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iCityCenterRow1X - 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, 
						*BugDll.widget("WIDGET_FOOD_MOD_HELP", -1, -1) )
				screen.show( "PopulationInputText" )
# BUG - Food Rate Hover - end

				if ((pHeadSelectedCity.badHealth(False) > 0) or (pHeadSelectedCity.goodHealth() >= 0)):
					if (pHeadSelectedCity.healthRate(False, 0) < 0):
						szBuffer = localText.getText("INTERFACE_CITY_HEALTH_BAD", (pHeadSelectedCity.goodHealth(), pHeadSelectedCity.badHealth(False), pHeadSelectedCity.healthRate(False, 0)))
					elif (pHeadSelectedCity.badHealth(False) > 0):
						szBuffer = localText.getText("INTERFACE_CITY_HEALTH_GOOD", (pHeadSelectedCity.goodHealth(), pHeadSelectedCity.badHealth(False)))
					else:
						szBuffer = localText.getText("INTERFACE_CITY_HEALTH_GOOD_NO_BAD", (pHeadSelectedCity.goodHealth(), ))
						
					screen.setLabel( "HealthText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - iCityCenterRow1X + 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_HEALTH, -1, -1 )
					screen.show( "HealthText" )

				if (iFoodDifference < 0):

					if ( pHeadSelectedCity.getFood() + iFoodDifference > 0 ):
						iDeltaFood = pHeadSelectedCity.getFood() + iFoodDifference
					else:
						iDeltaFood = 0
					if ( -iFoodDifference < pHeadSelectedCity.getFood() ):
						iExtraFood = -iFoodDifference
					else:
						iExtraFood = pHeadSelectedCity.getFood()
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_STORED, float(iDeltaFood) / pHeadSelectedCity.growthThreshold() )
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, 0.0 )
					if ( pHeadSelectedCity.growthThreshold() > iDeltaFood):
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, float(iExtraFood) / (pHeadSelectedCity.growthThreshold() - iDeltaFood) )
					else:
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, 0.0)
					
				else:

					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_STORED, float(pHeadSelectedCity.getFood()) / pHeadSelectedCity.growthThreshold() )
					if ( pHeadSelectedCity.growthThreshold() >  pHeadSelectedCity.getFood()):
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, float(iFoodDifference) / (pHeadSelectedCity.growthThreshold() - pHeadSelectedCity.getFood()) )
					else:
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, 0.0 )
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, 0.0 )
					
				screen.show( "PopulationBar" )

# BUG - Progress Bar - Tick Marks - start
				if MainOpt.isShowpBarTickMarks():
					self.pBarPopulationBar.drawTickMarks(screen, pHeadSelectedCity.getFood(), pHeadSelectedCity.growthThreshold(), iFoodDifference, iFoodDifference, False)
# BUG - Progress Bar - Tick Marks - end

				if (pHeadSelectedCity.getOrderQueueLength() > 0):
					if (pHeadSelectedCity.isProductionProcess()):
						szBuffer = pHeadSelectedCity.getProductionName()
# BUG - Whip Assist - start
					else:
						HURRY_WHIP = gc.getInfoTypeForString("HURRY_POPULATION")
						HURRY_BUY = gc.getInfoTypeForString("HURRY_GOLD")
						if (CityScreenOpt.isShowWhipAssist() and pHeadSelectedCity.canHurry(HURRY_WHIP, False)):
							iHurryPop = pHeadSelectedCity.hurryPopulation(HURRY_WHIP)
							iOverflow = pHeadSelectedCity.hurryProduction(HURRY_WHIP) - pHeadSelectedCity.productionLeft()
							if CityScreenOpt.isWhipAssistOverflowCountCurrentProduction():
								iOverflow += pHeadSelectedCity.getCurrentProductionDifference(False, True)
							iMaxOverflow = max(pHeadSelectedCity.getProductionNeeded(), pHeadSelectedCity.getCurrentProductionDifference(False, False))
							iLost = max(0, iOverflow - iMaxOverflow)
							iOverflow = min(iOverflow, iMaxOverflow)
							iItemModifier = pHeadSelectedCity.getProductionModifier()
							iBaseModifier = pHeadSelectedCity.getBaseYieldRateModifier(YieldTypes.YIELD_PRODUCTION, 0)
							iTotalModifier = pHeadSelectedCity.getBaseYieldRateModifier(YieldTypes.YIELD_PRODUCTION, iItemModifier)
							iLost *= iBaseModifier
							iLost /= max(1, iTotalModifier)
							iOverflow = (iBaseModifier * iOverflow) / max(1, iTotalModifier)
							if iLost > 0:
								if pHeadSelectedCity.isProductionUnit():
									iGoldPercent = gc.getDefineINT("MAXED_UNIT_GOLD_PERCENT")
								elif pHeadSelectedCity.isProductionBuilding():
									iGoldPercent = gc.getDefineINT("MAXED_BUILDING_GOLD_PERCENT")
								elif pHeadSelectedCity.isProductionProject():
									iGoldPercent = gc.getDefineINT("MAXED_PROJECT_GOLD_PERCENT")
								else:
									iGoldPercent = 0
								iOverflowGold = iLost * iGoldPercent / 100
								szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION_WHIP_PLUS_GOLD", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft(), iHurryPop, iOverflow, iOverflowGold))
							else:
								szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION_WHIP", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft(), iHurryPop, iOverflow))
						elif (CityScreenOpt.isShowWhipAssist() and pHeadSelectedCity.canHurry(HURRY_BUY, False)):
							iHurryCost = pHeadSelectedCity.hurryGold(HURRY_BUY)
							szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION_BUY", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft(), iHurryCost))
						else:
							szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft()))
# BUG - Whip Assist - end

					screen.setLabel( "ProductionText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), iCityCenterRow2Y, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "ProductionText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "ProductionText" )
				
				if (pHeadSelectedCity.isProductionProcess()):
					szBuffer = u"%d%c" %(pHeadSelectedCity.getYieldRate(YieldTypes.YIELD_PRODUCTION), gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
				elif (pHeadSelectedCity.isFoodProduction() and (iProductionDiffJustFood > 0)):
					szBuffer = u"%d%c + %d%c" %(iProductionDiffJustFood, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar(), iProductionDiffNoFood, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
				else:
					szBuffer = u"%d%c" %(iProductionDiffNoFood, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
					
				screen.setLabel( "ProductionInputText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iCityCenterRow1X - 6, iCityCenterRow2Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_PRODUCTION_MOD_HELP, -1, -1 )
				screen.show( "ProductionInputText" )

				if ((pHeadSelectedCity.happyLevel() >= 0) or (pHeadSelectedCity.unhappyLevel(0) > 0)):
					if (pHeadSelectedCity.isDisorder()):
						szBuffer = u"%d%c" %(pHeadSelectedCity.angryPopulation(0), CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))
					elif (pHeadSelectedCity.angryPopulation(0) > 0):
						szBuffer = localText.getText("INTERFACE_CITY_UNHAPPY", (pHeadSelectedCity.happyLevel(), pHeadSelectedCity.unhappyLevel(0), pHeadSelectedCity.angryPopulation(0)))
					elif (pHeadSelectedCity.unhappyLevel(0) > 0):
						szBuffer = localText.getText("INTERFACE_CITY_HAPPY", (pHeadSelectedCity.happyLevel(), pHeadSelectedCity.unhappyLevel(0)))
					else:
						szBuffer = localText.getText("INTERFACE_CITY_HAPPY_NO_UNHAPPY", (pHeadSelectedCity.happyLevel(), ))

# BUG - Anger Display - start
					if (CityScreenOpt.isShowAngerCounter()
					and pHeadSelectedCity.getTeam() == gc.getGame().getActiveTeam()):
						iAngerTimer = max(pHeadSelectedCity.getHurryAngerTimer(), pHeadSelectedCity.getConscriptAngerTimer())
						if iAngerTimer > 0:
							szBuffer += u" (%i)" % iAngerTimer
# BUG - Anger Display - end

					screen.setLabel( "HappinessText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - iCityCenterRow1X + 6, iCityCenterRow2Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_HAPPINESS, -1, -1 )
					screen.show( "HappinessText" )

				if (not(pHeadSelectedCity.isProductionProcess())):
				
					iNeeded = pHeadSelectedCity.getProductionNeeded()
					iStored = pHeadSelectedCity.getProduction()
					screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_STORED, float(iStored) / iNeeded )
					if iNeeded > iStored:
						screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE, float(iProductionDiffNoFood) / (iNeeded - iStored) )
					else:
						screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE, 0.0 )
					if iNeeded > iStored + iProductionDiffNoFood:
						screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, float(iProductionDiffJustFood) / (iNeeded - iStored - iProductionDiffNoFood) )
					else:
						screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, 0.0)

					screen.show( "ProductionBar" )

# BUG - Progress Bar - Tick Marks - start
					if MainOpt.isShowpBarTickMarks():
						if (pHeadSelectedCity.isProductionProcess()):
							iFirst = 0
							iRate = 0
						elif (pHeadSelectedCity.isFoodProduction() and (iProductionDiffJustFood > 0)):
							iFirst = pHeadSelectedCity.getCurrentProductionDifference(False, True)
							iRate = pHeadSelectedCity.getCurrentProductionDifference(False, False)
						else:
							iFirst = pHeadSelectedCity.getCurrentProductionDifference(True, True)
							iRate = pHeadSelectedCity.getCurrentProductionDifference(True, False)
						self.pBarProductionBar.drawTickMarks(screen, pHeadSelectedCity.getProduction(), pHeadSelectedCity.getProductionNeeded(), iFirst, iRate, False)

						HURRY_WHIP = gc.getInfoTypeForString("HURRY_POPULATION")
						if pHeadSelectedCity.canHurry(HURRY_WHIP, False):
							iRate = pHeadSelectedCity.hurryProduction(HURRY_WHIP) / pHeadSelectedCity.hurryPopulation(HURRY_WHIP)
							self.pBarProductionBar_Whip.drawTickMarks(screen, pHeadSelectedCity.getProduction(), pHeadSelectedCity.getProductionNeeded(), iFirst, iRate, True)
# BUG - Progress Bar - Tick Marks - end

				iCount = 0

				for i in range(CommerceTypes.NUM_COMMERCE_TYPES):
					eCommerce = (i + 1) % CommerceTypes.NUM_COMMERCE_TYPES

					if ((gc.getPlayer(pHeadSelectedCity.getOwner()).isCommerceFlexible(eCommerce)) or (eCommerce == CommerceTypes.COMMERCE_GOLD)):
						szBuffer = u"%d.%02d %c" %(pHeadSelectedCity.getCommerceRate(eCommerce), pHeadSelectedCity.getCommerceRateTimes100(eCommerce)%100, gc.getCommerceInfo(eCommerce).getChar())

						iHappiness = pHeadSelectedCity.getCommerceHappinessByType(eCommerce)

						if (iHappiness != 0):
							if ( iHappiness > 0 ):
								szTempBuffer = u", %d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
							else:
								szTempBuffer = u", %d%c" %(-iHappiness, CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))
							szBuffer = szBuffer + szTempBuffer

						szName = "CityPercentText" + str(iCount)
						screen.setLabel( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 220, 45 + (19 * iCount) + 4, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_COMMERCE_MOD_HELP, eCommerce, -1 )
						screen.show( szName )
						iCount = iCount + 1

				iCount = 0

				screen.addTableControlGFC( "BuildingListTable", 3, 10, 317, 238, yResolution - 541, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
				screen.setStyle( "BuildingListTable", "Table_City_Style" )
				
# BUG - Raw Yields - start
				bShowRawYields = g_bYieldView and CityScreenOpt.isShowRawYields()
				if (bShowRawYields):
					screen.addTableControlGFC( "TradeRouteTable", 4, 10, 187, 238, 98, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
					screen.setStyle( "TradeRouteTable", "Table_City_Style" )
					screen.setTableColumnHeader( "TradeRouteTable", 0, u"", 111 )
					screen.setTableColumnHeader( "TradeRouteTable", 1, u"", 60 )
					screen.setTableColumnHeader( "TradeRouteTable", 2, u"", 55 )
					screen.setTableColumnHeader( "TradeRouteTable", 3, u"", 10 )
					screen.setTableColumnRightJustify( "TradeRouteTable", 1 )
					screen.setTableColumnRightJustify( "TradeRouteTable", 2 )
				else:
					screen.addTableControlGFC( "TradeRouteTable", 3, 10, 187, 238, 98, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
					screen.setStyle( "TradeRouteTable", "Table_City_Style" )
					screen.setTableColumnHeader( "TradeRouteTable", 0, u"", 158 )
					screen.setTableColumnHeader( "TradeRouteTable", 1, u"", 68 )
					screen.setTableColumnHeader( "TradeRouteTable", 2, u"", 10 )
					screen.setTableColumnRightJustify( "TradeRouteTable", 1 )
# BUG - Raw Yields - end

				screen.setTableColumnHeader( "BuildingListTable", 0, u"", 108 )
				screen.setTableColumnHeader( "BuildingListTable", 1, u"", 118 )
				screen.setTableColumnHeader( "BuildingListTable", 2, u"", 10 )
				screen.setTableColumnRightJustify( "BuildingListTable", 1 )

				screen.show( "BuildingListBackground" )
				screen.show( "TradeRouteListBackground" )
				screen.show( "BuildingListLabel" )
				
# BUG - Raw Yields - start
				if (CityScreenOpt.isShowRawYields()):
					screen.setState("RawYieldsTrade0", not g_bYieldView)
					screen.show("RawYieldsTrade0")
					
					screen.setState("RawYieldsFood1", g_bYieldView and g_iYieldType == YieldTypes.YIELD_FOOD)
					screen.show("RawYieldsFood1")
					screen.setState("RawYieldsProduction2", g_bYieldView and g_iYieldType == YieldTypes.YIELD_PRODUCTION)
					screen.show("RawYieldsProduction2")
					screen.setState("RawYieldsCommerce3", g_bYieldView and g_iYieldType == YieldTypes.YIELD_COMMERCE)
					screen.show("RawYieldsCommerce3")
					
					screen.setState("RawYieldsWorkedTiles4", g_iYieldTiles == RawYields.WORKED_TILES)
					screen.show("RawYieldsWorkedTiles4")
					screen.setState("RawYieldsCityTiles5", g_iYieldTiles == RawYields.CITY_TILES)
					screen.show("RawYieldsCityTiles5")
					screen.setState("RawYieldsOwnedTiles6", g_iYieldTiles == RawYields.OWNED_TILES)
					screen.show("RawYieldsOwnedTiles6")
				else:
					screen.show( "TradeRouteListLabel" )
# BUG - Raw Yields - end
				
				for i in range( 3 ):
					szName = "BonusPane" + str(i)
					screen.show( szName )
					szName = "BonusBack" + str(i)
					screen.show( szName )

				i = 0
				iNumBuildings = 0
# BUG - Raw Yields - start
				self.yields = RawYields.Tracker()
# BUG - Raw Yields - end
				for i in range( gc.getNumBuildingInfos() ):
					if (pHeadSelectedCity.getNumBuilding(i) > 0):

						for k in range(pHeadSelectedCity.getNumBuilding(i)):
							
							szLeftBuffer = gc.getBuildingInfo(i).getDescription()
							szRightBuffer = u""
							bFirst = True
							
							if (pHeadSelectedCity.getNumActiveBuilding(i) > 0):
								iHealth = pHeadSelectedCity.getBuildingHealth(i)

								if (iHealth != 0):
									if ( bFirst == False ):
										szRightBuffer = szRightBuffer + ", "
									else:
										bFirst = False
										
									if ( iHealth > 0 ):
										szTempBuffer = u"+%d%c" %( iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR) )
										szRightBuffer = szRightBuffer + szTempBuffer
									else:
										szTempBuffer = u"+%d%c" %( -(iHealth), CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR) )
										szRightBuffer = szRightBuffer + szTempBuffer

								iHappiness = pHeadSelectedCity.getBuildingHappiness(i)

								if (iHappiness != 0):
									if ( bFirst == False ):
										szRightBuffer = szRightBuffer + ", "
									else:
										bFirst = False
										
									if ( iHappiness > 0 ):
										szTempBuffer = u"+%d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) )
										szRightBuffer = szRightBuffer + szTempBuffer
									else:
										szTempBuffer = u"+%d%c" %( -(iHappiness), CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR) )
										szRightBuffer = szRightBuffer + szTempBuffer

								for j in range( YieldTypes.NUM_YIELD_TYPES):
									iYield = gc.getBuildingInfo(i).getYieldChange(j) + pHeadSelectedCity.getNumBuilding(i) * pHeadSelectedCity.getBuildingYieldChange(gc.getBuildingInfo(i).getBuildingClassType(), j)

									if (iYield != 0):
										if ( bFirst == False ):
											szRightBuffer = szRightBuffer + ", "
										else:
											bFirst = False
											
										if ( iYield > 0 ):
											szTempBuffer = u"%s%d%c" %( "+", iYield, gc.getYieldInfo(j).getChar() )
											szRightBuffer = szRightBuffer + szTempBuffer
										else:
											szTempBuffer = u"%s%d%c" %( "", iYield, gc.getYieldInfo(j).getChar() )
											szRightBuffer = szRightBuffer + szTempBuffer
										
# BUG - Raw Yields - start
										self.yields.addBuilding(j, iYield)
# BUG - Raw Yields - end

							for j in range(CommerceTypes.NUM_COMMERCE_TYPES):
								iCommerce = pHeadSelectedCity.getBuildingCommerceByBuilding(j, i) / pHeadSelectedCity.getNumBuilding(i)
	
								if (iCommerce != 0):
									if ( bFirst == False ):
										szRightBuffer = szRightBuffer + ", "
									else:
										bFirst = False
										
									if ( iCommerce > 0 ):
										szTempBuffer = u"%s%d%c" %( "+", iCommerce, gc.getCommerceInfo(j).getChar() )
										szRightBuffer = szRightBuffer + szTempBuffer
									else:
										szTempBuffer = u"%s%d%c" %( "", iCommerce, gc.getCommerceInfo(j).getChar() )
										szRightBuffer = szRightBuffer + szTempBuffer
	
							szBuffer = szLeftBuffer + "  " + szRightBuffer
							
							screen.appendTableRow( "BuildingListTable" )
							screen.setTableText( "BuildingListTable", 0, iNumBuildings, "<font=1>" + szLeftBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_BUILDING, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
							screen.setTableText( "BuildingListTable", 1, iNumBuildings, "<font=1>" + szRightBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_BUILDING, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
							
							iNumBuildings = iNumBuildings + 1
						
				if ( iNumBuildings > g_iNumBuildings ):
					g_iNumBuildings = iNumBuildings
					
				iNumTradeRoutes = 0
				
				for i in range(gc.getDefineINT("MAX_TRADE_ROUTES")):
					pLoopCity = pHeadSelectedCity.getTradeCity(i)

					if (pLoopCity and pLoopCity.getOwner() >= 0):
						player = gc.getPlayer(pLoopCity.getOwner())
						szLeftBuffer = u"<color=%d,%d,%d,%d>%s</color>" %(player.getPlayerTextColorR(), player.getPlayerTextColorG(), player.getPlayerTextColorB(), player.getPlayerTextColorA(), pLoopCity.getName() )
						szRightBuffer = u""

						for j in range( YieldTypes.NUM_YIELD_TYPES ):
# BUG - Fractional Trade - start
							iTradeProfit = TradeUtil.calculateTradeRouteYield(pHeadSelectedCity, i, j)

							if (iTradeProfit != 0):
								if ( iTradeProfit > 0 ):
									if TradeUtil.isFractionalTrade():
										szTempBuffer = u"%s%d.%02d%c" %( "+", iTradeProfit // 100,  iTradeProfit % 100, gc.getYieldInfo(j).getChar() )
									else:
										szTempBuffer = u"%s%d%c" %( "+", iTradeProfit, gc.getYieldInfo(j).getChar() )
									szRightBuffer = szRightBuffer + szTempBuffer
								else:
									if TradeUtil.isFractionalTrade():
										szTempBuffer = u"%s%d.%02d%c" %( "", iTradeProfit // 100,  iTradeProfit % 100, gc.getYieldInfo(j).getChar() )
									else:
										szTempBuffer = u"%s%d%c" %( "", iTradeProfit, gc.getYieldInfo(j).getChar() )
									szRightBuffer = szRightBuffer + szTempBuffer
# BUG - Fractional Trade - end
# BUG - Raw Yields - start
								if (j == YieldTypes.YIELD_COMMERCE):
									if pHeadSelectedCity.getTeam() == pLoopCity.getTeam():
										self.yields.addDomesticTrade(iTradeProfit)
									else:
										self.yields.addForeignTrade(iTradeProfit)

						if (not bShowRawYields):
							screen.appendTableRow( "TradeRouteTable" )
							screen.setTableText( "TradeRouteTable", 0, iNumTradeRoutes, "<font=1>" + szLeftBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_TRADE_ROUTE_CITY, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
							screen.setTableText( "TradeRouteTable", 1, iNumTradeRoutes, "<font=1>" + szRightBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_TRADE_ROUTE_CITY, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
# BUG - Raw Yields - end
						
						iNumTradeRoutes = iNumTradeRoutes + 1
						
				if ( iNumTradeRoutes > g_iNumTradeRoutes ):
					g_iNumTradeRoutes = iNumTradeRoutes

				i = 0  
				iLeftCount = 0
				iCenterCount = 0
				iRightCount = 0

				for i in range( gc.getNumBonusInfos() ):
					bHandled = False
					if ( pHeadSelectedCity.hasBonus(i) ):

						iHealth = pHeadSelectedCity.getBonusHealth(i)
						iHappiness = pHeadSelectedCity.getBonusHappiness(i)
						
						szBuffer = u""
						szLeadBuffer = u""

						szTempBuffer = u"<font=1>%c" %( gc.getBonusInfo(i).getChar() )
						szLeadBuffer = szLeadBuffer + szTempBuffer
						
						if (pHeadSelectedCity.getNumBonuses(i) > 1):
							szTempBuffer = u"(%d)" %( pHeadSelectedCity.getNumBonuses(i) )
							szLeadBuffer = szLeadBuffer + szTempBuffer

						szLeadBuffer = szLeadBuffer + "</font>"
						
						if (iHappiness != 0):
							if ( iHappiness > 0 ):
								szTempBuffer = u"<font=1>+%d%c</font>" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) )
							else:
								szTempBuffer = u"<font=1>+%d%c</font>" %( -iHappiness, CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR) )

							if ( iHealth > 0 ):
								szTempBuffer += u"<font=1>, +%d%c</font>" %( iHealth, CyGame().getSymbolID( FontSymbols.HEALTHY_CHAR ) )

							szName = "RightBonusItemLeft" + str(iRightCount)
							screen.setLabelAt( szName, "BonusBack2", szLeadBuffer, CvUtil.FONT_LEFT_JUSTIFY, 0, (iRightCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							szName = "RightBonusItemRight" + str(iRightCount)
							screen.setLabelAt( szName, "BonusBack2", szTempBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 102, (iRightCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							
							iRightCount = iRightCount + 1

							bHandled = True

						if (iHealth != 0 and bHandled == False):
							if ( iHealth > 0 ):
								szTempBuffer = u"<font=1>+%d%c</font>" %( iHealth, CyGame().getSymbolID( FontSymbols.HEALTHY_CHAR ) )
							else:
								szTempBuffer = u"<font=1>+%d%c</font>" %( -iHealth, CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR) )
								
							szName = "CenterBonusItemLeft" + str(iCenterCount)
							screen.setLabelAt( szName, "BonusBack1", szLeadBuffer, CvUtil.FONT_LEFT_JUSTIFY, 0, (iCenterCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							szName = "CenterBonusItemRight" + str(iCenterCount)
							screen.setLabelAt( szName, "BonusBack1", szTempBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 62, (iCenterCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							
							iCenterCount = iCenterCount + 1

							bHandled = True

						szBuffer = u""
						if ( not bHandled ):
						
							szName = "LeftBonusItem" + str(iLeftCount)
							screen.setLabelAt( szName, "BonusBack0", szLeadBuffer, CvUtil.FONT_LEFT_JUSTIFY, 0, (iLeftCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							
							iLeftCount = iLeftCount + 1

							bHandled = True

				g_iNumLeftBonus = iLeftCount
				g_iNumCenterBonus = iCenterCount
				g_iNumRightBonus = iRightCount
				
				iMaintenance = pHeadSelectedCity.getMaintenanceTimes100()

				szBuffer = localText.getText("INTERFACE_CITY_MAINTENANCE", ())
				
				screen.setLabel( "MaintenanceText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 15, 126, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_MAINTENANCE, -1, -1 )
				screen.show( "MaintenanceText" )
				
				szBuffer = u"-%d.%02d %c" %(iMaintenance/100, iMaintenance%100, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
				screen.setLabel( "MaintenanceAmountText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 220, 125, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_MAINTENANCE, -1, -1 )
				screen.show( "MaintenanceAmountText" )
				
# BUG - Raw Yields - start
				if (bShowRawYields):
					self.yields.processCity(pHeadSelectedCity)
					self.yields.fillTable(screen, "TradeRouteTable", g_iYieldType, g_iYieldTiles)
# BUG - Raw Yields - end

				szBuffer = u""

# BUG - Limit/Extra Religions - start
				if CityScreenOpt.isShowOnlyPresentReligions():
					lReligions = ReligionUtil.getCityReligions(pHeadSelectedCity)
					iCountReligions = len(lReligions)
					iMaxWidth = 250#228
					iMaxButtons = iCountReligions
					if (iCountReligions < 8):
						iButtonSize = 24
						iButtonSpace = 10
					#elif (iCountReligions >= iMaxButtons):
						#iButtonSize = iMaxWidth / iMaxButtons
						#iButtonSpace = 0
					elif (iCountReligions == 8):
						iButtonSize = 24
						iButtonSpace = 5
					elif (iCountReligions == 9):
						iButtonSize = 24
						iButtonSpace = 2
					elif (iCountReligions == 10):
						iButtonSize = 21
						iButtonSpace = 2
					elif (iCountReligions == 11):
						iButtonSize = 20
						iButtonSpace = 1
					elif (iCountReligions == 12):
						iButtonSize = 18
						iButtonSpace = 1
					elif (iCountReligions == 13):
						iButtonSize = 18
						iButtonSpace = 0
					elif (iCountReligions == 14):
						iButtonSize = 16
						iButtonSpace = 0
					elif (iCountReligions == 15):
						iButtonSize = 15
						iButtonSpace = 0
					elif (iCountReligions == 16):
						iButtonSize = 14
						iButtonSpace = 0
					elif (iCountReligions == 17):
						iButtonSize = 13
						iButtonSpace = 0
					elif (iCountReligions == 18):
						iButtonSize = 13
						iButtonSpace = 0
					elif (37 > iCountReligions > 18):
						iMaxButtons = 18
						iButtonSize = 13
						iButtonSpace = 0
					elif (iCountReligions == 37) or (iCountReligions == 38):
						iMaxWidth = 240
						iMaxButtons = int(round(iCountReligions / 2.0, 0))# int(round(gc.getNumReligionInfos() / 2.0, 0))
						iButtonSize = iMaxWidth / iMaxButtons
						iButtonSpace = (iMaxWidth - (iButtonSize * iMaxButtons)) // (iMaxButtons - 1)
					else:
						iMaxButtons = int(round(iCountReligions / 2.0, 0))# int(round(gc.getNumReligionInfos() / 2.0, 0))
						iButtonSize = iMaxWidth / iMaxButtons
						iButtonSpace = (iMaxWidth - (iButtonSize * iMaxButtons)) // (iMaxButtons - 1)
					for ii in range(iCountReligions):
						i = lReligions[ii]
						xCoord = xResolution - 242 + ((ii % iMaxButtons) * (iButtonSize + iButtonSpace))
						#xCoord = xResolution - 242 + (i * 34) # Origional Civ4 Code
						yCoord = 42 + iButtonSize * (ii // iMaxButtons)
						#yCoord = 42 # Origional Civ4 Code
						
						bEnable = True
							
						if (pHeadSelectedCity.isHolyCityByType(i)):
							szTempBuffer = u"%c" %(gc.getReligionInfo(i).getHolyCityChar())
							# < 47 Religions Mod Start >
							# This is now done below since the Holy City Overlay has to be added
							# after the Religion Icon and can not be shown before its added
							#szName = "ReligionHolyCityDDS" + str(i)
							#screen.show( szName )
							# < 47 Religions Mod Start >
						else:
							szTempBuffer = u"%c" %(gc.getReligionInfo(i).getChar())
						szBuffer = szBuffer + szTempBuffer
	
						j = 0
						for j in range(CommerceTypes.NUM_COMMERCE_TYPES):
							iCommerce = pHeadSelectedCity.getReligionCommerceByReligion(j, i)
	
							if (iCommerce != 0):
								if ( iCommerce > 0 ):
									szTempBuffer = u",%s%d%c" %("+", iCommerce, gc.getCommerceInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
								else:
									szTempBuffer = u",%s%d%c" %( "", iCommerce, gc.getCommerceInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
	
						iHappiness = pHeadSelectedCity.getReligionHappiness(i)
	
						if (iHappiness != 0):
							if ( iHappiness > 0 ):
								szTempBuffer = u",+%d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) )
								szBuffer = szBuffer + szTempBuffer
							else:
								szTempBuffer = u",+%d%c" %(-(iHappiness), CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR) )
								szBuffer = szBuffer + szTempBuffer
	
						szBuffer = szBuffer + " "
							
						szButton = gc.getReligionInfo(i).getButton()
	
						szName = "ReligionDDS" + str(i)
						screen.setImageButton( szName, szButton, xCoord, yCoord, iButtonSize, iButtonSize, WidgetTypes.WIDGET_HELP_RELIGION_CITY, i, -1 )
						screen.enable( szName, bEnable )
						screen.show( szName )
						# Holy City Overlay
						if (pHeadSelectedCity.isHolyCityByType(i)):
							szName = "ReligionHolyCityDDS" + str(i)
							screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLYCITY_OVERLAY").getPath(), xCoord, yCoord, iButtonSize, iButtonSize, WidgetTypes.WIDGET_HELP_RELIGION_CITY, i, -1 )
							screen.show( szName )
				
				else:
					
					for i in range(gc.getNumReligionInfos()):
						xCoord = xResolution - 242 + (i * 34)
						yCoord = 42
						
						bEnable = True
							
						if (pHeadSelectedCity.isHasReligion(i)):
							if (pHeadSelectedCity.isHolyCityByType(i)):
								szTempBuffer = u"%c" %(gc.getReligionInfo(i).getHolyCityChar())
								szName = "ReligionHolyCityDDS" + str(i)
								screen.show( szName )
							else:
								szTempBuffer = u"%c" %(gc.getReligionInfo(i).getChar())
							szBuffer = szBuffer + szTempBuffer
	
							j = 0
							for j in range(CommerceTypes.NUM_COMMERCE_TYPES):
								iCommerce = pHeadSelectedCity.getReligionCommerceByReligion(j, i)
	
								if (iCommerce != 0):
									if ( iCommerce > 0 ):
										szTempBuffer = u",%s%d%c" %("+", iCommerce, gc.getCommerceInfo(j).getChar() )
										szBuffer = szBuffer + szTempBuffer
									else:
										szTempBuffer = u",%s%d%c" %( "", iCommerce, gc.getCommerceInfo(j).getChar() )
										szBuffer = szBuffer + szTempBuffer
	
							iHappiness = pHeadSelectedCity.getReligionHappiness(i)
	
							if (iHappiness != 0):
								if ( iHappiness > 0 ):
									szTempBuffer = u",+%d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) )
									szBuffer = szBuffer + szTempBuffer
								else:
									szTempBuffer = u",+%d%c" %(-(iHappiness), CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR) )
									szBuffer = szBuffer + szTempBuffer
	
							szBuffer = szBuffer + " "
							
							szButton = gc.getReligionInfo(i).getButton()
						
						else:
						
							bEnable = False
							szButton = gc.getReligionInfo(i).getButton()
	
						szName = "ReligionDDS" + str(i)
						screen.setImageButton( szName, szButton, xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_RELIGION_CITY, i, -1 )
						screen.enable( szName, bEnable )
						screen.show( szName )
						if (pHeadSelectedCity.isHolyCityByType(i)):
							szName = "ReligionHolyCityDDS" + str(i)
							screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLYCITY_OVERLAY").getPath(), xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_RELIGION_CITY, i, -1 )
							screen.show( szName )
# BUG - Limit/Extra Religions - end

# BUG - Limit/Extra Corporations - start
				if CityScreenOpt.isShowOnlyPresentCorporations():
					lCorporations = []
					for i in range(gc.getNumCorporationInfos()):
						if (not pHeadSelectedCity.isHasCorporation(i)):
							continue
						lCorporations += [i]
					iCountCorporations = len(lCorporations)
					iMaxWidth = 250#228
					iMaxButtons = iCountCorporations
					if (iCountCorporations < 8):
						iButtonSize = 24
						iButtonSpace = 10
					#elif (iCountCorporations >= iMaxButtons):
						#iButtonSize = iMaxWidth / iMaxButtons
						#iButtonSpace = 0
					elif (iCountCorporations == 8):
						iButtonSize = 24
						iButtonSpace = 5
					elif (iCountCorporations == 9):
						iButtonSize = 24
						iButtonSpace = 2
					elif (iCountCorporations == 10):
						iButtonSize = 21
						iButtonSpace = 2
					elif (iCountCorporations == 11):
						iButtonSize = 20
						iButtonSpace = 1
					elif (iCountCorporations == 12):
						iButtonSize = 18
						iButtonSpace = 1
					elif (iCountCorporations == 13):
						iButtonSize = 18
						iButtonSpace = 0
					elif (iCountCorporations == 14):
						iButtonSize = 16
						iButtonSpace = 0
					elif (iCountCorporations == 15):
						iButtonSize = 15
						iButtonSpace = 0
					elif (iCountCorporations == 16):
						iButtonSize = 14
						iButtonSpace = 0
					elif (iCountCorporations == 17):
						iButtonSize = 13
						iButtonSpace = 0
					elif (iCountCorporations == 18):
						iButtonSize = 13
						iButtonSpace = 0
					elif (37 > iCountReligions > 18):
						iMaxButtons = 18
						iButtonSize = 13
						iButtonSpace = 0
					elif (iCountCorporations == 37) or (iCountCorporations == 38):
						iMaxWidth = 240
						iMaxButtons = int(round(iCountCorporations / 2.0, 0))# int(round(gc.getNumCorporationInfos() / 2.0, 0))
						iButtonSize = iMaxWidth / iMaxButtons
						iButtonSpace = (iMaxWidth - (iButtonSize * iMaxButtons)) // (iMaxButtons - 1)
					else:
						iMaxButtons = int(round(iCountCorporations / 2.0, 0))# int(round(gc.getNumCorporationInfos() / 2.0, 0))
						iButtonSize = iMaxWidth / iMaxButtons
						iButtonSpace = (iMaxWidth - (iButtonSize * iMaxButtons)) // (iMaxButtons - 1)
					for ii in range(iCountCorporations):
						i = lCorporations[ii]
						xCoord = xResolution - 242 + ((ii % iMaxButtons) * (iButtonSize + iButtonSpace))
						#xCoord = xResolution - 242 + (i * 34) # Origional Civ4 Code
						yCoord = 66 + iButtonSize * (ii // iMaxButtons)
						#yCoord = 66 # Origional Civ4 Code
						
						bEnable = True
							
						if (pHeadSelectedCity.isHeadquartersByType(i)):
							szTempBuffer = u"%c" %(gc.getCorporationInfo(i).getHeadquarterChar())
							#szName = "CorporationHeadquarterDDS" + str(i)
							#screen.show( szName )
						else:
							szTempBuffer = u"%c" %(gc.getCorporationInfo(i).getChar())
						szBuffer = szBuffer + szTempBuffer
	
						j = 0
						for j in range(YieldTypes.NUM_YIELD_TYPES):
							iYield = pHeadSelectedCity.getCorporationYieldByCorporation(j, i)
	
							if (iYield != 0):
								if ( iYield > 0 ):
									szTempBuffer = u",%s%d%c" %("+", iYield, gc.getYieldInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
								else:
									szTempBuffer = u",%s%d%c" %( "", iYield, gc.getYieldInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
							
						j = 0
						for j in range(CommerceTypes.NUM_COMMERCE_TYPES):
							iCommerce = pHeadSelectedCity.getCorporationCommerceByCorporation(j, i)
	
							if (iCommerce != 0):
								if ( iCommerce > 0 ):
									szTempBuffer = u",%s%d%c" %("+", iCommerce, gc.getCommerceInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
								else:
									szTempBuffer = u",%s%d%c" %( "", iCommerce, gc.getCommerceInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
	
						szBuffer += " "
							
						szButton = gc.getCorporationInfo(i).getButton()
	
						szName = "CorporationDDS" + str(i)
						screen.setImageButton( szName, szButton, xCoord, yCoord, iButtonSize, iButtonSize, WidgetTypes.WIDGET_HELP_CORPORATION_CITY, i, -1 )
						screen.enable( szName, bEnable )
						screen.show( szName )
						# Holy City Overlay
						if (pHeadSelectedCity.isHeadquartersByType(i)):
							szName = "CorporationHeadquarterDDS" + str(i)
							screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLYCITY_OVERLAY").getPath(), xCoord, yCoord, iButtonSize, iButtonSize, WidgetTypes.WIDGET_HELP_CORPORATION_CITY, i, -1 )
							screen.show( szName )
				
				else:
					
					for i in range(gc.getNumCorporationInfos()):
						xCoord = xResolution - 242 + (i * 34)
						yCoord = 66
						
						bEnable = True
							
						if (pHeadSelectedCity.isHasCorporation(i)):
							if (pHeadSelectedCity.isHeadquartersByType(i)):
								szTempBuffer = u"%c" %(gc.getCorporationInfo(i).getHeadquarterChar())
								szName = "CorporationHeadquarterDDS" + str(i)
								screen.show( szName )
							else:
								szTempBuffer = u"%c" %(gc.getCorporationInfo(i).getChar())
							szBuffer = szBuffer + szTempBuffer
	
							for j in range(YieldTypes.NUM_YIELD_TYPES):
								iYield = pHeadSelectedCity.getCorporationYieldByCorporation(j, i)
	
								if (iYield != 0):
									if ( iYield > 0 ):
										szTempBuffer = u",%s%d%c" %("+", iYield, gc.getYieldInfo(j).getChar() )
										szBuffer = szBuffer + szTempBuffer
									else:
										szTempBuffer = u",%s%d%c" %( "", iYield, gc.getYieldInfo(j).getChar() )
										szBuffer = szBuffer + szTempBuffer
							
							for j in range(CommerceTypes.NUM_COMMERCE_TYPES):
								iCommerce = pHeadSelectedCity.getCorporationCommerceByCorporation(j, i)
	
								if (iCommerce != 0):
									if ( iCommerce > 0 ):
										szTempBuffer = u",%s%d%c" %("+", iCommerce, gc.getCommerceInfo(j).getChar() )
										szBuffer = szBuffer + szTempBuffer
									else:
										szTempBuffer = u",%s%d%c" %( "", iCommerce, gc.getCommerceInfo(j).getChar() )
										szBuffer = szBuffer + szTempBuffer
	
							szBuffer += " "
							
							szButton = gc.getCorporationInfo(i).getButton()
						
						else:
						
							bEnable = False
							szButton = gc.getCorporationInfo(i).getButton()
	
						szName = "CorporationDDS" + str(i)
						screen.setImageButton( szName, szButton, xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_CORPORATION_CITY, i, -1 )
						screen.enable( szName, bEnable )
						screen.show( szName )
						if (pHeadSelectedCity.isHeadquartersByType(i)):
							szName = "CorporationHeadquarterDDS" + str(i)
							screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLYCITY_OVERLAY").getPath(), xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_CORPORATION_CITY, i, -1 )
							screen.show( szName )
# BUG - Limit/Extra Corporations - end

				szBuffer = u"%d%% %s" %(pHeadSelectedCity.plot().calculateCulturePercent(pHeadSelectedCity.getOwner()), gc.getPlayer(pHeadSelectedCity.getOwner()).getCivilizationAdjective(0) )
				screen.setLabel( "NationalityText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 210, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.setHitTest( "NationalityText", HitTestTypes.HITTEST_NOHIT )
				screen.show( "NationalityText" )
				iRemainder = 100
				iWhichBar = 0
				for h in range( gc.getMAX_PLAYERS() ):
					if ( gc.getPlayer(h).isAlive() ):
						iPercent = pHeadSelectedCity.plot().calculateCulturePercent(h)
						if ( iPercent > 0 ):
							screen.setStackedBarColorsRGB( "NationalityBar", iWhichBar, gc.getPlayer(h).getPlayerTextColorR(), gc.getPlayer(h).getPlayerTextColorG(), gc.getPlayer(h).getPlayerTextColorB(), gc.getPlayer(h).getPlayerTextColorA() )
							if ( iRemainder <= 0):
								screen.setBarPercentage( "NationalityBar", iWhichBar, 0.0 )
							else:
								screen.setBarPercentage( "NationalityBar", iWhichBar, float(iPercent) / iRemainder)
							iRemainder -= iPercent
							iWhichBar += 1
				screen.show( "NationalityBar" )

				iDefenseModifier = pHeadSelectedCity.getDefenseModifier(False)

				if (iDefenseModifier != 0):
					szBuffer = localText.getText("TXT_KEY_MAIN_CITY_DEFENSE", (CyGame().getSymbolID(FontSymbols.DEFENSE_CHAR), iDefenseModifier))
					
					if (pHeadSelectedCity.getDefenseDamage() > 0):
						szTempBuffer = u" (%d%%)" %( ( ( gc.getMAX_CITY_DEFENSE_DAMAGE() - pHeadSelectedCity.getDefenseDamage() ) * 100 ) / gc.getMAX_CITY_DEFENSE_DAMAGE() )
						szBuffer = szBuffer + szTempBuffer
					szNewBuffer = "<font=4>"
					szNewBuffer = szNewBuffer + szBuffer
					szNewBuffer = szNewBuffer + "</font>"
					screen.setLabel( "DefenseText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 270, 40, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_DEFENSE, -1, -1 )
					screen.show( "DefenseText" )

				if ( pHeadSelectedCity.getCultureLevel != CultureLevelTypes.NO_CULTURELEVEL ):
					iRate = pHeadSelectedCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE)
					if (iRate%100 == 0):
						szBuffer = localText.getText("INTERFACE_CITY_COMMERCE_RATE", (gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), gc.getCultureLevelInfo(pHeadSelectedCity.getCultureLevel()).getTextKey(), iRate/100))
					else:
						szRate = u"+%d.%02d" % (iRate/100, iRate%100)
						szBuffer = localText.getText("INTERFACE_CITY_COMMERCE_RATE_FLOAT", (gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), gc.getCultureLevelInfo(pHeadSelectedCity.getCultureLevel()).getTextKey(), szRate))
						
# BUG - Culture Turns - start
					if CityScreenOpt.isShowCultureTurns() and iRate > 0:
						iCultureTimes100 = pHeadSelectedCity.getCultureTimes100(pHeadSelectedCity.getOwner())
						iCultureLeftTimes100 = 100 * pHeadSelectedCity.getCultureThreshold() - iCultureTimes100
						szBuffer += u" " + localText.getText("INTERFACE_CITY_TURNS", (((iCultureLeftTimes100 + iRate - 1) / iRate),))
# BUG - Culture Turns - end

					screen.setLabel( "CultureText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 184, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "CultureText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "CultureText" )

				if ((pHeadSelectedCity.getGreatPeopleProgress() > 0) or (pHeadSelectedCity.getGreatPeopleRate() > 0)):
# BUG - Great Person Turns - start
					iRate = pHeadSelectedCity.getGreatPeopleRate()
					if CityScreenOpt.isShowCityGreatPersonInfo():
						iGPTurns = GPUtil.getCityTurns(pHeadSelectedCity)
						szBuffer = GPUtil.getGreatPeopleText(pHeadSelectedCity, iGPTurns, 230, MainOpt.isGPBarTypesNone(), MainOpt.isGPBarTypesOne(), False)
					else:
						szBuffer = localText.getText("INTERFACE_CITY_GREATPEOPLE_RATE", (CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR), pHeadSelectedCity.getGreatPeopleRate()))
						if CityScreenOpt.isShowGreatPersonTurns() and iRate > 0:
							iGPTurns = GPUtil.getCityTurns(pHeadSelectedCity)
							szBuffer += u" " + localText.getText("INTERFACE_CITY_TURNS", (iGPTurns, ))
# BUG - Great Person Turns - end

					screen.setLabel( "GreatPeopleText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution - 126, yResolution - 182, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "GreatPeopleText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "GreatPeopleText" )

					iFirst = float(pHeadSelectedCity.getGreatPeopleProgress()) / float( gc.getPlayer( pHeadSelectedCity.getOwner() ).greatPeopleThreshold(false) )
					screen.setBarPercentage( "GreatPeopleBar", InfoBarTypes.INFOBAR_STORED, iFirst )
					if ( iFirst == 1 ):
						screen.setBarPercentage( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, ( float(pHeadSelectedCity.getGreatPeopleRate()) / float( gc.getPlayer( pHeadSelectedCity.getOwner() ).greatPeopleThreshold(false) ) ) )
					else:
						screen.setBarPercentage( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, ( ( float(pHeadSelectedCity.getGreatPeopleRate()) / float( gc.getPlayer( pHeadSelectedCity.getOwner() ).greatPeopleThreshold(false) ) ) ) / ( 1 - iFirst ) )
					screen.show( "GreatPeopleBar" )

				iFirst = float(pHeadSelectedCity.getCultureTimes100(pHeadSelectedCity.getOwner())) / float(100 * pHeadSelectedCity.getCultureThreshold())
				screen.setBarPercentage( "CultureBar", InfoBarTypes.INFOBAR_STORED, iFirst )
				if ( iFirst == 1 ):
					screen.setBarPercentage( "CultureBar", InfoBarTypes.INFOBAR_RATE, ( float(pHeadSelectedCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)) / float(pHeadSelectedCity.getCultureThreshold()) ) )
				else:
					screen.setBarPercentage( "CultureBar", InfoBarTypes.INFOBAR_RATE, ( ( float(pHeadSelectedCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)) / float(pHeadSelectedCity.getCultureThreshold()) ) ) / ( 1 - iFirst ) )
				screen.show( "CultureBar" )
				
		else:
		
			# Help Text Area
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, HELP_TEXT_MINIMUM_WIDTH )
			else:
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, HELP_TEXT_MINIMUM_WIDTH )

			screen.hide( "InterfaceTopLeftBackgroundWidget" )
			screen.hide( "InterfaceTopRightBackgroundWidget" )
			screen.hide( "InterfaceCenterLeftBackgroundWidget" )
			screen.hide( "CityScreenTopWidget" )
			screen.hide( "CityNameBackground" )
			screen.hide( "TopCityPanelLeft" )
			screen.hide( "TopCityPanelRight" )
			screen.hide( "CityScreenAdjustPanel" )
			screen.hide( "InterfaceCenterRightBackgroundWidget" )
			
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
				self.setMinimapButtonVisibility(True)

		return 0
		
	# Will update the info pane strings
	def updateInfoPaneStrings( self ):
	
		iRow = 0
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()
		
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		bShift = CyInterface().shiftKey()

		screen.addPanel( "SelectedUnitPanel", u"", u"", True, False, 8, yResolution - 140, 280, 130, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "SelectedUnitPanel", "Panel_Game_HudStat_Style" )
		screen.hide( "SelectedUnitPanel" )

		screen.addTableControlGFC( "SelectedUnitText", 3, 10, yResolution - 109, 183, 102, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
		screen.setStyle( "SelectedUnitText", "Table_EmptyScroll_Style" )
		screen.hide( "SelectedUnitText" )
		screen.hide( "SelectedUnitLabel" )
		
		screen.addTableControlGFC( "SelectedCityText", 3, 10, yResolution - 139, 183, 128, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
		screen.setStyle( "SelectedCityText", "Table_EmptyScroll_Style" )
		screen.hide( "SelectedCityText" )
		
		for i in range(gc.getNumPromotionInfos()):
			szName = "PromotionButton" + str(i)
			screen.hide( szName )
		
		if CyEngine().isGlobeviewUp():
			return

		if (pHeadSelectedCity):
		
			iOrders = CyInterface().getNumOrdersQueued()

			screen.setTableColumnHeader( "SelectedCityText", 0, u"", 121 )
			screen.setTableColumnHeader( "SelectedCityText", 1, u"", 54 )
			screen.setTableColumnHeader( "SelectedCityText", 2, u"", 10 )
			screen.setTableColumnRightJustify( "SelectedCityText", 1 )
			
			for i in range( iOrders ):
				
				szLeftBuffer = u""
				szRightBuffer = u""
				
				if ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_TRAIN ):
					szLeftBuffer = gc.getUnitInfo(CyInterface().getOrderNodeData1(i)).getDescription()
					szRightBuffer = "(" + str(pHeadSelectedCity.getUnitProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"

					if (CyInterface().getOrderNodeSave(i)):
						szLeftBuffer = u"*" + szLeftBuffer
					
# BUG - Production Decay - start
					if BugDll.isPresent() and CityScreenOpt.isShowProductionDecayQueue():
						eUnit = CyInterface().getOrderNodeData1(i)
						if pHeadSelectedCity.getUnitProduction(eUnit) > 0:
							if pHeadSelectedCity.isUnitProductionDecay(eUnit):
								szLeftBuffer = BugUtil.getText("TXT_KEY_BUG_PRODUCTION_DECAY_THIS_TURN", (szLeftBuffer,))
							elif pHeadSelectedCity.getUnitProductionTime(eUnit) > 0:
								iDecayTurns = pHeadSelectedCity.getUnitProductionDecayTurns(eUnit)
								if iDecayTurns <= CityScreenOpt.getProductionDecayQueueUnitThreshold():
									szLeftBuffer = BugUtil.getText("TXT_KEY_BUG_PRODUCTION_DECAY_WARNING", (szLeftBuffer,))
# BUG - Production Decay - end

				elif ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CONSTRUCT ):
					szLeftBuffer = gc.getBuildingInfo(CyInterface().getOrderNodeData1(i)).getDescription()
					szRightBuffer = "(" + str(pHeadSelectedCity.getBuildingProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"

# BUG - Production Decay - start
					if BugDll.isPresent() and CityScreenOpt.isShowProductionDecayQueue():
						eBuilding = CyInterface().getOrderNodeData1(i)
						if pHeadSelectedCity.getBuildingProduction(eBuilding) > 0:
							if pHeadSelectedCity.isBuildingProductionDecay(eBuilding):
								szLeftBuffer = BugUtil.getText("TXT_KEY_BUG_PRODUCTION_DECAY_THIS_TURN", (szLeftBuffer,))
							elif pHeadSelectedCity.getBuildingProductionTime(eBuilding) > 0:
								iDecayTurns = pHeadSelectedCity.getBuildingProductionDecayTurns(eBuilding)
								if iDecayTurns <= CityScreenOpt.getProductionDecayQueueBuildingThreshold():
									szLeftBuffer = BugUtil.getText("TXT_KEY_BUG_PRODUCTION_DECAY_WARNING", (szLeftBuffer,))
# BUG - Production Decay - end

				elif ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CREATE ):
					szLeftBuffer = gc.getProjectInfo(CyInterface().getOrderNodeData1(i)).getDescription()
					szRightBuffer = "(" + str(pHeadSelectedCity.getProjectProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"

				elif ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_MAINTAIN ):
					szLeftBuffer = gc.getProcessInfo(CyInterface().getOrderNodeData1(i)).getDescription()

				screen.appendTableRow( "SelectedCityText" )
				screen.setTableText( "SelectedCityText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
				screen.setTableText( "SelectedCityText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
				screen.show( "SelectedCityText" )
				screen.show( "SelectedUnitPanel" )
				iRow += 1

		elif (pHeadSelectedUnit and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
		
			screen.setTableColumnHeader( "SelectedUnitText", 0, u"", 100 )
			screen.setTableColumnHeader( "SelectedUnitText", 1, u"", 75 )
			screen.setTableColumnHeader( "SelectedUnitText", 2, u"", 10 )
			screen.setTableColumnRightJustify( "SelectedUnitText", 1 )
			
			if (CyInterface().mirrorsSelectionGroup()):
				pSelectedGroup = pHeadSelectedUnit.getGroup()
			else:
				pSelectedGroup = 0

			if (CyInterface().getLengthSelectionList() > 1):
				
# BUG - Stack Movement Display - start
				szBuffer = localText.getText("TXT_KEY_UNIT_STACK", (CyInterface().getLengthSelectionList(), ))
				if MainOpt.isShowStackMovementPoints():
					iMinMoves = 100000
					iMaxMoves = 0
					for i in range(CyInterface().getLengthSelectionList()):
						pUnit = CyInterface().getSelectionUnit(i)
						if (pUnit is not None):
							iLoopMoves = pUnit.movesLeft()
							if (iLoopMoves > iMaxMoves):
								iMaxMoves = iLoopMoves
							if (iLoopMoves < iMinMoves):
								iMinMoves = iLoopMoves
					if (iMinMoves == iMaxMoves):
						fMinMoves = float(iMinMoves) / gc.getMOVE_DENOMINATOR()
						szBuffer += u" %.1f%c" % (fMinMoves, CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
					else:
						fMinMoves = float(iMinMoves) / gc.getMOVE_DENOMINATOR()
						fMaxMoves = float(iMaxMoves) / gc.getMOVE_DENOMINATOR()
						szBuffer += u" %.1f - %.1f%c" % (fMinMoves, fMaxMoves, CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
				
				screen.setText( "SelectedUnitLabel", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 18, yResolution - 137, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1 )
# BUG - Stack Movement Display - end
				
				if ((pSelectedGroup == 0) or (pSelectedGroup.getLengthMissionQueue() <= 1)):
					if (pHeadSelectedUnit):
						for i in range(gc.getNumUnitInfos()):
							iCount = CyInterface().countEntities(i)

							if (iCount > 0):
								szRightBuffer = u""
								
								szLeftBuffer = gc.getUnitInfo(i).getDescription()

								if (iCount > 1):
									szRightBuffer = u"(" + str(iCount) + u")"

								szBuffer = szLeftBuffer + u"  " + szRightBuffer
								screen.appendTableRow( "SelectedUnitText" )
								screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
								screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
								screen.show( "SelectedUnitText" )
								screen.show( "SelectedUnitPanel" )
								iRow += 1
			else:
			
				if (pHeadSelectedUnit.getHotKeyNumber() == -1):
					szBuffer = localText.getText("INTERFACE_PANE_UNIT_NAME", (pHeadSelectedUnit.getName(), ))
				else:
					szBuffer = localText.getText("INTERFACE_PANE_UNIT_NAME_HOT_KEY", (pHeadSelectedUnit.getHotKeyNumber(), pHeadSelectedUnit.getName()))
				if (len(szBuffer) > 60):
					szBuffer = "<font=2>" + szBuffer + "</font>"
				screen.setText( "SelectedUnitLabel", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 18, yResolution - 137, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1 )
			
				if ((pSelectedGroup == 0) or (pSelectedGroup.getLengthMissionQueue() <= 1)):
					screen.show( "SelectedUnitText" )
					screen.show( "SelectedUnitPanel" )

					szBuffer = u""

					szLeftBuffer = u""
					szRightBuffer = u""
					
					if (pHeadSelectedUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
						if (pHeadSelectedUnit.airBaseCombatStr() > 0):
							szLeftBuffer = localText.getText("INTERFACE_PANE_AIR_STRENGTH", ())
							if (pHeadSelectedUnit.isFighting()):
								szRightBuffer = u"?/%d%c" %(pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
							elif (pHeadSelectedUnit.isHurt()):
								szRightBuffer = u"%.1f/%d%c" %(((float(pHeadSelectedUnit.airBaseCombatStr() * pHeadSelectedUnit.currHitPoints())) / (float(pHeadSelectedUnit.maxHitPoints()))), pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
							else:
								szRightBuffer = u"%d%c" %(pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
					else:
						if (pHeadSelectedUnit.canFight()):
							szLeftBuffer = localText.getText("INTERFACE_PANE_STRENGTH", ())
							if (pHeadSelectedUnit.isFighting()):
								szRightBuffer = u"?/%d%c" %(pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
							elif (pHeadSelectedUnit.isHurt()):
								szRightBuffer = u"%.1f/%d%c" %(((float(pHeadSelectedUnit.baseCombatStr() * pHeadSelectedUnit.currHitPoints())) / (float(pHeadSelectedUnit.maxHitPoints()))), pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
							else:
								szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))

					szBuffer = szLeftBuffer + szRightBuffer
					if ( szBuffer ):
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

					szLeftBuffer = u""
					szRightBuffer = u""
					
# BUG - Unit Movement Fraction - start
					szLeftBuffer = localText.getText("INTERFACE_PANE_MOVEMENT", ())
					if MainOpt.isShowUnitMovementPointsFraction():
						szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
						if (pHeadSelectedUnit.movesLeft() == 0):
							szRightBuffer = u"0/" + szRightBuffer
						elif (pHeadSelectedUnit.movesLeft() == pHeadSelectedUnit.baseMoves() * gc.getMOVE_DENOMINATOR()):
							pass
						else:
							fCurrMoves = float(pHeadSelectedUnit.movesLeft()) / gc.getMOVE_DENOMINATOR()
							szRightBuffer = (u"%.1f/" % fCurrMoves) + szRightBuffer
					else:
						if ( (pHeadSelectedUnit.movesLeft() % gc.getMOVE_DENOMINATOR()) > 0 ):
							iDenom = 1
						else:
							iDenom = 0
						iCurrMoves = ((pHeadSelectedUnit.movesLeft() / gc.getMOVE_DENOMINATOR()) + iDenom )
						if (pHeadSelectedUnit.baseMoves() == iCurrMoves):
							szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR) )
						else:
							szRightBuffer = u"%d/%d%c" %(iCurrMoves, pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR) )
# BUG - Unit Movement Fraction - end

					szBuffer = szLeftBuffer + "  " + szRightBuffer
					screen.appendTableRow( "SelectedUnitText" )
					screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
					screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
					screen.show( "SelectedUnitText" )
					screen.show( "SelectedUnitPanel" )
					iRow += 1

					if (pHeadSelectedUnit.getLevel() > 0):
					
						szLeftBuffer = localText.getText("INTERFACE_PANE_LEVEL", ())
						szRightBuffer = u"%d" %(pHeadSelectedUnit.getLevel())
						
						szBuffer = szLeftBuffer + "  " + szRightBuffer
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

					if ((pHeadSelectedUnit.getExperience() > 0) and not pHeadSelectedUnit.isFighting()):
						szLeftBuffer = localText.getText("INTERFACE_PANE_EXPERIENCE", ())
						szRightBuffer = u"(%d/%d)" %(pHeadSelectedUnit.getExperience(), pHeadSelectedUnit.experienceNeeded())
						szBuffer = szLeftBuffer + "  " + szRightBuffer
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

					iPromotionCount = 0
					i = 0
					for i in range(gc.getNumPromotionInfos()):
						if (pHeadSelectedUnit.isHasPromotion(i)):
							szName = "PromotionButton" + str(i)
							self.setPromotionButtonPosition( szName, iPromotionCount )
							screen.moveToFront( szName )
							screen.show( szName )

							iPromotionCount = iPromotionCount + 1

			if (pSelectedGroup):
			
				iNodeCount = pSelectedGroup.getLengthMissionQueue()

				if (iNodeCount > 1):
					for i in range( iNodeCount ):
						szLeftBuffer = u""
						szRightBuffer = u""
					
						if (gc.getMissionInfo(pSelectedGroup.getMissionType(i)).isBuild()):
							if (i == 0):
								szLeftBuffer = gc.getBuildInfo(pSelectedGroup.getMissionData1(i)).getDescription()
								szRightBuffer = localText.getText("INTERFACE_CITY_TURNS", (pSelectedGroup.plot().getBuildTurnsLeft(pSelectedGroup.getMissionData1(i), 0, 0), ))								
							else:
								szLeftBuffer = u"%s..." %(gc.getBuildInfo(pSelectedGroup.getMissionData1(i)).getDescription())
						else:
							szLeftBuffer = u"%s..." %(gc.getMissionInfo(pSelectedGroup.getMissionType(i)).getDescription())

						szBuffer = szLeftBuffer + "  " + szRightBuffer
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

		return 0
		
	# Will update the scores
	def updateScoreStrings( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		
		screen.hide( "ScoreBackground" )
		
# BUG - Align Icons - start
		for i in range( gc.getMAX_PLAYERS() ):
			szName = "ScoreText" + str(i)
			screen.hide( szName )
			szName = "ScoreTech" + str(i)
			screen.hide( szName )
			for j in range( Scoreboard.NUM_PARTS ):
				szName = "ScoreText%d-%d" %( i, j )
				screen.hide( szName )
# BUG - Align Icons - end

		iWidth = 0
		iCount = 0
		iBtnHeight = 22
		
		if ((CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY)):
			if (CyInterface().isScoresVisible() and not CyInterface().isCityScreenUp() and CyEngine().isGlobeviewUp() == false):

# BUG - Align Icons - start
				bAlignIcons = ScoreOpt.isAlignIcons()
				if (bAlignIcons):
					scores = Scoreboard.Scoreboard()
# BUG - Align Icons - end

# BUG - 3.17 No Espionage - start
				bEspionage = GameUtil.isEspionage()
# BUG - 3.17 No Espionage - end

# BUG - Power Rating - start
				bShowPower = ScoreOpt.isShowPower()
				if (bShowPower):
					iPlayerPower = gc.getActivePlayer().getPower()
					iPowerColor = ScoreOpt.getPowerColor()
					iHighPowerColor = ScoreOpt.getHighPowerColor()
					iLowPowerColor = ScoreOpt.getLowPowerColor()
					
					if (bEspionage):
						iDemographicsMission = -1
						for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
							if (gc.getEspionageMissionInfo(iMissionLoop).isSeeDemographics()):
								iDemographicsMission = iMissionLoop
								break
						if (iDemographicsMission == -1):
							bShowPower = False
# BUG - Power Rating - end

				i = gc.getMAX_CIV_TEAMS() - 1
				while (i > -1):
					eTeam = gc.getGame().getRankTeam(i)

					if (gc.getTeam(gc.getGame().getActiveTeam()).isHasMet(eTeam) or gc.getTeam(eTeam).isHuman() or gc.getGame().isDebugMode()):
# BUG - Align Icons - start
						if (bAlignIcons):
							scores.addTeam(gc.getTeam(eTeam), i)
# BUG - Align Icons - end
						j = gc.getMAX_CIV_PLAYERS() - 1
						while (j > -1):
							ePlayer = gc.getGame().getRankPlayer(j)

							if (not CyInterface().isScoresMinimized() or gc.getGame().getActivePlayer() == ePlayer):
# BUG - Dead Civs - start
								if (gc.getPlayer(ePlayer).isEverAlive() and not gc.getPlayer(ePlayer).isBarbarian()
									and (gc.getPlayer(ePlayer).isAlive() or ScoreOpt.isShowDeadCivs())):
# BUG - Dead Civs - end
# BUG - Minor Civs - start
									if (not gc.getPlayer(ePlayer).isMinorCiv() or ScoreOpt.isShowMinorCivs()):
# BUG - Minor Civs - end
										if (gc.getPlayer(ePlayer).getTeam() == eTeam):
											szBuffer = u"<font=2>"
# BUG - Align Icons - start
											if (bAlignIcons):
												scores.addPlayer(gc.getPlayer(ePlayer), j)
												# BUG: Align Icons continues throughout -- if (bAlignIcons): scores.setFoo(foo)
# BUG - Align Icons - end
	
											if (gc.getGame().isGameMultiPlayer()):
												if (not (gc.getPlayer(ePlayer).isTurnActive())):
													szBuffer = szBuffer + "*"
													if (bAlignIcons):
														scores.setWaiting()
	
# BUG - Dead Civs - start
											if (ScoreOpt.isUsePlayerName()):
												szPlayerName = gc.getPlayer(ePlayer).getName()
											else:
												szPlayerName = gc.getLeaderHeadInfo(gc.getPlayer(ePlayer).getLeaderType()).getDescription()
											if (ScoreOpt.isShowBothNames()):
												szCivName = gc.getPlayer(ePlayer).getCivilizationShortDescription(0)
												szPlayerName = szPlayerName + "/" + szCivName
											elif (ScoreOpt.isShowBothNamesShort()):
												szCivName = gc.getPlayer(ePlayer).getCivilizationDescription(0)
												szPlayerName = szPlayerName + "/" + szCivName
											elif (ScoreOpt.isShowLeaderName()):
												szPlayerName = szPlayerName
											elif (ScoreOpt.isShowCivName()):
												szCivName = gc.getPlayer(ePlayer).getCivilizationShortDescription(0)
												szPlayerName = szCivName
											else:
												szCivName = gc.getPlayer(ePlayer).getCivilizationDescription(0)
												szPlayerName = szCivName
											
											if (not gc.getPlayer(ePlayer).isAlive() and ScoreOpt.isShowDeadTag()):
												szPlayerScore = localText.getText("TXT_KEY_BUG_DEAD_CIV", ())
												if (bAlignIcons):
													scores.setScore(szPlayerScore)
											else:
												iScore = gc.getGame().getPlayerScore(ePlayer)
												szPlayerScore = u"%d" % iScore
												if (bAlignIcons):
													scores.setScore(szPlayerScore)
# BUG - Score Delta - start
												if (ScoreOpt.isShowScoreDelta()):
													iGameTurn = gc.getGame().getGameTurn()
													if (ePlayer >= gc.getGame().getActivePlayer()):
														iGameTurn -= 1
													if (ScoreOpt.isScoreDeltaIncludeCurrentTurn()):
														iScoreDelta = iScore
													elif (iGameTurn >= 0):
														iScoreDelta = gc.getPlayer(ePlayer).getScoreHistory(iGameTurn)
													else:
														iScoreDelta = 0
													iPrevGameTurn = iGameTurn - 1
													if (iPrevGameTurn >= 0):
														iScoreDelta -= gc.getPlayer(ePlayer).getScoreHistory(iPrevGameTurn)
													if (iScoreDelta != 0):
														if (iScoreDelta > 0):
															iColorType = gc.getInfoTypeForString("COLOR_GREEN")
														elif (iScoreDelta < 0):
															iColorType = gc.getInfoTypeForString("COLOR_RED")
														szScoreDelta = "%+d" % iScoreDelta
														if (iColorType >= 0):
															szScoreDelta = localText.changeTextColor(szScoreDelta, iColorType)
														szPlayerScore += szScoreDelta + u" "
														if (bAlignIcons):
															scores.setScoreDelta(szScoreDelta)
# BUG - Score Delta - end
											
											if (not CyInterface().isFlashingPlayer(ePlayer) or CyInterface().shouldFlash(ePlayer)):
												if (ePlayer == gc.getGame().getActivePlayer()):
													szPlayerName = u"[<color=%d,%d,%d,%d>%s</color>]" %(gc.getPlayer(ePlayer).getPlayerTextColorR(), gc.getPlayer(ePlayer).getPlayerTextColorG(), gc.getPlayer(ePlayer).getPlayerTextColorB(), gc.getPlayer(ePlayer).getPlayerTextColorA(), szPlayerName)
												else:
													if (not gc.getPlayer(ePlayer).isAlive() and ScoreOpt.isGreyOutDeadCivs()):
														szPlayerName = u"<color=%d,%d,%d,%d>%s</color>" %(175, 175, 175, gc.getPlayer(ePlayer).getPlayerTextColorA(), szPlayerName)
													else:
														szPlayerName = u"<color=%d,%d,%d,%d>%s</color>" %(gc.getPlayer(ePlayer).getPlayerTextColorR(), gc.getPlayer(ePlayer).getPlayerTextColorG(), gc.getPlayer(ePlayer).getPlayerTextColorB(), gc.getPlayer(ePlayer).getPlayerTextColorA(), szPlayerName)
											szTempBuffer = u"%s: %s" %(szPlayerScore, szPlayerName)
											szBuffer = szBuffer + szTempBuffer
											if (bAlignIcons):
												scores.setName(szPlayerName)
												scores.setID(u"<color=%d,%d,%d,%d>%d</color>" %(gc.getPlayer(ePlayer).getPlayerTextColorR(), gc.getPlayer(ePlayer).getPlayerTextColorG(), gc.getPlayer(ePlayer).getPlayerTextColorB(), gc.getPlayer(ePlayer).getPlayerTextColorA(), ePlayer))
											
											if (gc.getPlayer(ePlayer).isAlive()):
												if (bAlignIcons):
													scores.setAlive()
												# BUG: Rest of Dead Civs change is merely indentation by 1 level ...
												if (gc.getTeam(eTeam).isAlive()):
													if ( not (gc.getTeam(gc.getGame().getActiveTeam()).isHasMet(eTeam)) ):
														szBuffer = szBuffer + (" ?")
														if (bAlignIcons):
															scores.setNotMet()
													if (gc.getTeam(eTeam).isAtWar(gc.getGame().getActiveTeam())):
														szBuffer = szBuffer + "("  + localText.getColorText("TXT_KEY_CONCEPT_WAR", (), gc.getInfoTypeForString("COLOR_RED")).upper() + ")"
														if (bAlignIcons):
															scores.setWar()
													elif (gc.getTeam(gc.getGame().getActiveTeam()).isForcePeace(eTeam)):
														if (bAlignIcons):
															scores.setPeace()
													elif (gc.getTeam(eTeam).isAVassal()):
														for iOwnerTeam in range(gc.getMAX_TEAMS()):
															if (gc.getTeam(eTeam).isVassal(iOwnerTeam) and gc.getTeam(gc.getGame().getActiveTeam()).isForcePeace(iOwnerTeam)):
																if (bAlignIcons):
																	scores.setPeace()
																break
													if (gc.getPlayer(ePlayer).canTradeNetworkWith(gc.getGame().getActivePlayer()) and (ePlayer != gc.getGame().getActivePlayer())):
														szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.TRADE_CHAR))
														szBuffer = szBuffer + szTempBuffer
														if (bAlignIcons):
															scores.setTrade()
													if (gc.getTeam(eTeam).isOpenBorders(gc.getGame().getActiveTeam())):
														szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.OPEN_BORDERS_CHAR))
														szBuffer = szBuffer + szTempBuffer
														if (bAlignIcons):
															scores.setBorders()
													if (gc.getTeam(eTeam).isDefensivePact(gc.getGame().getActiveTeam())):
														szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.DEFENSIVE_PACT_CHAR))
														szBuffer = szBuffer + szTempBuffer
														if (bAlignIcons):
															scores.setPact()
													if (gc.getPlayer(ePlayer).getStateReligion() != -1):
														if (gc.getPlayer(ePlayer).hasHolyCity(gc.getPlayer(ePlayer).getStateReligion())):
															szTempBuffer = u"%c" %(gc.getReligionInfo(gc.getPlayer(ePlayer).getStateReligion()).getHolyCityChar())
														else:
															szTempBuffer = u"%c" %(gc.getReligionInfo(gc.getPlayer(ePlayer).getStateReligion()).getChar())
														szBuffer = szBuffer + szTempBuffer
														if (bAlignIcons):
															scores.setReligion(szTempBuffer)
													
													if (bEspionage and gc.getTeam(eTeam).getEspionagePointsAgainstTeam(gc.getGame().getActiveTeam()) < gc.getTeam(gc.getGame().getActiveTeam()).getEspionagePointsAgainstTeam(eTeam)):
														szTempBuffer = u"%c" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
														szBuffer = szBuffer + szTempBuffer
														if (bAlignIcons):
															scores.setEspionage()
												
												bEspionageCanSeeResearch = False
												if (bEspionage):
													for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
														if (gc.getEspionageMissionInfo(iMissionLoop).isSeeResearch()):
															bEspionageCanSeeResearch = gc.getActivePlayer().canDoEspionageMission(iMissionLoop, ePlayer, None, -1)
															break
												
												if (((gc.getPlayer(ePlayer).getTeam() == gc.getGame().getActiveTeam()) and (gc.getTeam(gc.getGame().getActiveTeam()).getNumMembers() > 1)) or (gc.getTeam(gc.getPlayer(ePlayer).getTeam()).isVassal(gc.getGame().getActiveTeam())) or gc.getGame().isDebugMode() or bEspionageCanSeeResearch):
													if (gc.getPlayer(ePlayer).getCurrentResearch() != -1):
														szTempBuffer = u"-%s (%d)" %(gc.getTechInfo(gc.getPlayer(ePlayer).getCurrentResearch()).getDescription(), gc.getPlayer(ePlayer).getResearchTurnsLeft(gc.getPlayer(ePlayer).getCurrentResearch(), True))
														szBuffer = szBuffer + szTempBuffer
														if (bAlignIcons):
															scores.setResearch(gc.getPlayer(ePlayer).getCurrentResearch(), gc.getPlayer(ePlayer).getResearchTurnsLeft(gc.getPlayer(ePlayer).getCurrentResearch(), True))
												# BUG: ...end of indentation
# BUG - Dead Civs - end
# BUG - Power Rating - start
												# if on, show according to espionage "see demographics" mission
												if (bShowPower 
													and (gc.getGame().getActivePlayer() != ePlayer
														 and (not bEspionage or gc.getActivePlayer().canDoEspionageMission(iDemographicsMission, ePlayer, None, -1)))):
													iPower = gc.getPlayer(ePlayer).getPower()
													if (iPower > 0): # avoid divide by zero
														fPowerRatio = float(iPlayerPower) / float(iPower)
														if (ScoreOpt.isPowerThemVersusYou()):
															if (fPowerRatio > 0):
																fPowerRatio = 1.0 / fPowerRatio
															else:
																fPowerRatio = 99.0
														cPower = gc.getGame().getSymbolID(FontSymbols.STRENGTH_CHAR)
														szTempBuffer = BugUtil.formatFloat(fPowerRatio, ScoreOpt.getPowerDecimals()) + u"%c" % (cPower)
														if (iHighPowerColor >= 0 and fPowerRatio >= ScoreOpt.getHighPowerRatio()):
															szTempBuffer = localText.changeTextColor(szTempBuffer, iHighPowerColor)
														elif (iLowPowerColor >= 0 and fPowerRatio <= ScoreOpt.getLowPowerRatio()):
															szTempBuffer = localText.changeTextColor(szTempBuffer, iLowPowerColor)
														elif (iPowerColor >= 0):
															szTempBuffer = localText.changeTextColor(szTempBuffer, iPowerColor)
														szBuffer = szBuffer + u" " + szTempBuffer
														if (bAlignIcons):
															scores.setPower(szTempBuffer)
# BUG - Power Rating - end
# BUG - Attitude Icons - start
												if (ScoreOpt.isShowAttitude()):
													if (not gc.getPlayer(ePlayer).isHuman()):
														iAtt = gc.getPlayer(ePlayer).AI_getAttitude(gc.getGame().getActivePlayer())
														cAtt =  unichr(ord(unichr(CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 4)) + iAtt)
														szBuffer += cAtt
														if (bAlignIcons):
															scores.setAttitude(cAtt)
# BUG - Attitude Icons - end
# BUG - Refuses to Talk - start
												if (not DiplomacyUtil.isWillingToTalk(ePlayer, gc.getGame().getActivePlayer())):
													cRefusesToTalk = u"!"
													szBuffer += cRefusesToTalk
													if (bAlignIcons):
														scores.setWontTalk()
# BUG - Refuses to Talk - end

# BUG - Worst Enemy - start
												if (ScoreOpt.isShowWorstEnemy()):
													if (AttitudeUtil.isWorstEnemy(ePlayer, gc.getGame().getActivePlayer())):
														cWorstEnemy = u"%c" %(CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))
														szBuffer += cWorstEnemy
														if (bAlignIcons):
															scores.setWorstEnemy()
# BUG - Worst Enemy - end
# BUG - WHEOOH - start
												if (ScoreOpt.isShowWHEOOH()):
													if (PlayerUtil.isWHEOOH(ePlayer, PlayerUtil.getActivePlayerID())):
														szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR))
														szBuffer = szBuffer + szTempBuffer
														if (bAlignIcons):
															scores.setWHEOOH()
# BUG - WHEOOH - end
# BUG - Num Cities - start
												if (ScoreOpt.isShowCountCities()):
													if (PlayerUtil.canSeeCityList(ePlayer)):
														szTempBuffer = u"%d" % PlayerUtil.getNumCities(ePlayer)
													else:
														szTempBuffer = BugUtil.colorText(u"%d" % PlayerUtil.getNumRevealedCities(ePlayer), "COLOR_CYAN")
													szBuffer = szBuffer + " " + szTempBuffer
													if (bAlignIcons):
														scores.setNumCities(szTempBuffer)
# BUG - Num Cities - end
											
											if (CyGame().isNetworkMultiPlayer()):
												szTempBuffer = CyGameTextMgr().getNetStats(ePlayer)
												szBuffer = szBuffer + szTempBuffer
												if (bAlignIcons):
													scores.setNetStats(szTempBuffer)
											
											if (gc.getPlayer(ePlayer).isHuman() and CyInterface().isOOSVisible()):
												szTempBuffer = u" <color=255,0,0>* %s *</color>" %(CyGameTextMgr().getOOSSeeds(ePlayer))
												szBuffer = szBuffer + szTempBuffer
												if (bAlignIcons):
													scores.setNetStats(szTempBuffer)
												
											szBuffer = szBuffer + "</font>"
	
# BUG - Align Icons - start
											if (not bAlignIcons):
												if ( CyInterface().determineWidth( szBuffer ) > iWidth ):
													iWidth = CyInterface().determineWidth( szBuffer )
		
												szName = "ScoreText" + str(ePlayer)
												if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isInAdvancedStart()):
													yCoord = yResolution - 206
												else:
													yCoord = yResolution - 88
		
# BUG - Dead Civs - start
												# Don't try to contact dead civs
												if (gc.getPlayer(ePlayer).isAlive()):
													iWidgetType = WidgetTypes.WIDGET_CONTACT_CIV
													iPlayer = ePlayer
												else:
													iWidgetType = WidgetTypes.WIDGET_GENERAL
													iPlayer = -1
												screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, yCoord - (iCount * iBtnHeight), -0.3, FontTypes.SMALL_FONT, iWidgetType, iPlayer, -1 )
# BUG - Dead Civs - end
												screen.show( szName )
												
												CyInterface().checkFlashReset(ePlayer)
		
												iCount = iCount + 1
# BUG - Align Icons - end
							j = j - 1
					i = i - 1

# BUG - Align Icons - start
				if (bAlignIcons):
					scores.draw(screen)
				else:
					if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isInAdvancedStart()):
						yCoord = yResolution - 186
					else:
						yCoord = yResolution - 68
					screen.setPanelSize( "ScoreBackground", xResolution - 21 - iWidth, yCoord - (iBtnHeight * iCount) - 4, iWidth + 12, (iBtnHeight * iCount) + 8 )
					screen.show( "ScoreBackground" )
# BUG - Align Icons - end

	# Will update the help Strings
	def updateHelpStrings( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL ):
			screen.setHelpTextString( "" )
		else:
			screen.setHelpTextString( CyInterface().getHelpString() )
		
		return 0
		
	# Will set the promotion button position
	def setPromotionButtonPosition( self, szName, iPromotionCount ):
		
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		# Find out our resolution
		yResolution = screen.getYResolution()

		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			screen.moveItem( szName, 266 - (24 * (iPromotionCount / 6)), yResolution - 144 + (24 * (iPromotionCount % 6)), -0.3 )

	# Will set the selection button position
	def setResearchButtonPosition( self, szButtonID, iCount ):
		
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()

# BUG - Bars on single line for higher resolution screens - start
		if (xResolution >= 1440
		and (MainOpt.isShowGGProgressBar() or MainOpt.isShowGPProgressBar())):
			xCoord = 268 + (xResolution - 1440) / 2
			xCoord += 6 + 84
			screen.moveItem( szButtonID, 264 + ( ( xResolution - 1024 ) / 2 ) + ( 34 * ( iCount % 15 ) ), 0 + ( 34 * ( iCount / 15 ) ), -0.3 )
		else:
			xCoord = 264 + ( ( xResolution - 1024 ) / 2 )

		screen.moveItem( szButtonID, xCoord + ( 34 * ( iCount % 15 ) ), 0 + ( 34 * ( iCount / 15 ) ), -0.3 )
# BUG - Bars on single line for higher resolution screens - end

	# Will set the selection button position
	def setScoreTextPosition( self, szButtonID, iWhichLine ):
		
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		yResolution = screen.getYResolution()
		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			yCoord = yResolution - 180
		else:
			yCoord = yResolution - 88
		screen.moveItem( szButtonID, 996, yCoord - (iWhichLine * 18), -0.3 )

	# Will build the globeview UI
	def updateGlobeviewButtons( self ):
		kInterface = CyInterface()
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		kEngine = CyEngine()
		kGLM = CyGlobeLayerManager()
		iNumLayers = kGLM.getNumLayers()
		iCurrentLayerID = kGLM.getCurrentLayerID()
		
		# Positioning things based on the visibility of the globe
		if kEngine.isGlobeviewUp():
			screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, HELP_TEXT_MINIMUM_WIDTH )
		else:
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, HELP_TEXT_MINIMUM_WIDTH )
			else:
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, HELP_TEXT_MINIMUM_WIDTH )

		
		# Set base Y position for the LayerOptions, if we find them	
		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE:
			iY = yResolution - iGlobeLayerOptionsY_Minimal
		else:
			iY = yResolution - iGlobeLayerOptionsY_Regular

		# Hide the layer options ... all of them
		for i in range (20):
			szName = "GlobeLayerOption" + str(i)
			screen.hide(szName)

		# Setup the GlobeLayer panel
		iNumLayers = kGLM.getNumLayers()
		if kEngine.isGlobeviewUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL:
			# set up panel
			if iCurrentLayerID != -1 and kGLM.getLayer(iCurrentLayerID).getNumOptions() != 0:
				bHasOptions = True		
			else:
				bHasOptions = False
				screen.hide( "ScoreBackground" )

			# set up toggle button
			screen.setState("GlobeToggle", True)

			# Set GlobeLayer indicators correctly
			for i in range(kGLM.getNumLayers()):
				szButtonID = "GlobeLayer" + str(i)
				screen.setState( szButtonID, iCurrentLayerID == i )
				
			# Set up options pane
			if bHasOptions:
				kLayer = kGLM.getLayer(iCurrentLayerID)

				iCurY = iY
				iNumOptions = kLayer.getNumOptions()
				iCurOption = kLayer.getCurrentOption()
				iMaxTextWidth = -1
				for iTmp in range(iNumOptions):
					iOption = iTmp # iNumOptions - iTmp - 1
					szName = "GlobeLayerOption" + str(iOption)
					szCaption = kLayer.getOptionName(iOption)			
					if(iOption == iCurOption):
						szBuffer = "  <color=0,255,0>%s</color>  " % (szCaption)
					else:
						szBuffer = "  %s  " % (szCaption)
					iTextWidth = CyInterface().determineWidth( szBuffer )

					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - 9 - iTextWidth, iCurY-iGlobeLayerOptionHeight-10, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GLOBELAYER_OPTION, iOption, -1 )
					screen.show( szName )

					iCurY -= iGlobeLayerOptionHeight

					if iTextWidth > iMaxTextWidth:
						iMaxTextWidth = iTextWidth

				#make extra space
				iCurY -= iGlobeLayerOptionHeight;
				iPanelWidth = iMaxTextWidth + 32
				iPanelHeight = iY - iCurY
				iPanelX = xResolution - 14 - iPanelWidth
				iPanelY = iCurY
				screen.setPanelSize( "ScoreBackground", iPanelX, iPanelY, iPanelWidth, iPanelHeight )
				screen.show( "ScoreBackground" )

		else:
			if iCurrentLayerID != -1:
				kLayer = kGLM.getLayer(iCurrentLayerID)
				if kLayer.getName() == "RESOURCES":
					screen.setState("ResourceIcons", True)
				else:
					screen.setState("ResourceIcons", False)

				if kLayer.getName() == "UNITS":
					screen.setState("UnitIcons", True)
				else:
					screen.setState("UnitIcons", False)
			else:
				screen.setState("ResourceIcons", False)
				screen.setState("UnitIcons", False)
				
			screen.setState("Grid", CyUserProfile().getGrid())
			screen.setState("BareMap", CyUserProfile().getMap())
			screen.setState("Yields", CyUserProfile().getYields())
			screen.setState("ScoresVisible", CyUserProfile().getScores())

			screen.hide( "InterfaceGlobeLayerPanel" )
			screen.setState("GlobeToggle", False )

	# Update minimap buttons
	def setMinimapButtonVisibility( self, bVisible):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		kInterface = CyInterface()
		kGLM = CyGlobeLayerManager()
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		if ( CyInterface().isCityScreenUp() ):
			bVisible = False
		
		kMainButtons = ["UnitIcons", "Grid", "BareMap", "Yields", "ScoresVisible", "ResourceIcons"]
		kGlobeButtons = []
		for i in range(kGLM.getNumLayers()):
			szButtonID = "GlobeLayer" + str(i)
			kGlobeButtons.append(szButtonID)
		
		if bVisible:
			if CyEngine().isGlobeviewUp():
				kHide = kMainButtons
				kShow = kGlobeButtons
			else:
				kHide = kGlobeButtons
				kShow = kMainButtons
			screen.show( "GlobeToggle" )
			
		else:
			kHide = kMainButtons + kGlobeButtons
			kShow = []
			screen.hide( "GlobeToggle" )
		
		for szButton in kHide:
			screen.hide(szButton)
		
		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE:
			iY = yResolution - iMinimapButtonsY_Minimal
			iGlobeY = yResolution - iGlobeButtonY_Minimal 
		else:
			iY = yResolution - iMinimapButtonsY_Regular
			iGlobeY = yResolution - iGlobeButtonY_Regular
			
		iBtnX = xResolution - 39
		screen.moveItem("GlobeToggle", iBtnX, iGlobeY, 0.0)
		
		iBtnAdvance = 28
		iBtnX = iBtnX - len(kShow)*iBtnAdvance - 10
		if len(kShow) > 0:		
			i = 0
			for szButton in kShow:
				screen.moveItem(szButton, iBtnX, iY, 0.0)
				screen.moveToFront(szButton)
				screen.show(szButton)
				iBtnX += iBtnAdvance
				i += 1
				
	
	def createGlobeviewButtons( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		
		kEngine = CyEngine()
		kGLM = CyGlobeLayerManager()
		iNumLayers = kGLM.getNumLayers()

		for i in range (kGLM.getNumLayers()):
			szButtonID = "GlobeLayer" + str(i)

			kLayer = kGLM.getLayer(i)
			szStyle = kLayer.getButtonStyle()
			
			if szStyle == 0 or szStyle == "":
				szStyle = "Button_HUDSmall_Style"
			
			screen.addCheckBoxGFC( szButtonID, "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_GLOBELAYER, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
			screen.setStyle( szButtonID, szStyle )
			screen.hide( szButtonID )
				
			
	def createMinimapButtons( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		screen.addCheckBoxGFC( "UnitIcons", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_UNIT_ICONS).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "UnitIcons", "Button_HUDGlobeUnit_Style" )
		screen.setState( "UnitIcons", False )
		screen.hide( "UnitIcons" )

		screen.addCheckBoxGFC( "Grid", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_GRID).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "Grid", "Button_HUDBtnGrid_Style" )
		screen.setState( "Grid", False )
		screen.hide( "Grid" )

		screen.addCheckBoxGFC( "BareMap", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_BARE_MAP).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "BareMap", "Button_HUDBtnClearMap_Style" )
		screen.setState( "BareMap", False )
		screen.hide( "BareMap" )

		screen.addCheckBoxGFC( "Yields", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_YIELDS).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "Yields", "Button_HUDBtnTileAssets_Style" )
		screen.setState( "Yields", False )
		screen.hide( "Yields" )

		screen.addCheckBoxGFC( "ScoresVisible", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_SCORES).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "ScoresVisible", "Button_HUDBtnRank_Style" )
		screen.setState( "ScoresVisible", True )
		screen.hide( "ScoresVisible" )

		screen.addCheckBoxGFC( "ResourceIcons", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_RESOURCE_ALL).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "ResourceIcons", "Button_HUDBtnResources_Style" )
		screen.setState( "ResourceIcons", False )
		screen.hide( "ResourceIcons" )
		
		screen.addCheckBoxGFC( "GlobeToggle", "", "", -1, -1, 36, 36, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_GLOBELAYER).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "GlobeToggle", "Button_HUDZoom_Style" )
		screen.setState( "GlobeToggle", False )
		screen.hide( "GlobeToggle" )

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		#BugUtil.debugInput(inputClass)
# BUG - PLE - start
		if  (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON) or \
			(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF) or \
			(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (self.MainInterfaceInputMap.has_key(inputClass.getFunctionName())):	
				return self.MainInterfaceInputMap.get(inputClass.getFunctionName())(inputClass)
			if (self.MainInterfaceInputMap.has_key(inputClass.getFunctionName() + "1")):	
				return self.MainInterfaceInputMap.get(inputClass.getFunctionName() + "1")(inputClass)
# BUG - PLE - end

# BUG - Raw Yields - start
		if (inputClass.getFunctionName().startswith("RawYields")):
			return self.handleRawYieldsButtons(inputClass)
# BUG - Raw Yields - end

# BUG - Great Person Bar - start
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName().startswith("GreatPersonBar")):
			# Zoom to next GP city
			iCity = inputClass.getData1()
			if (iCity == -1):
				pCity, _ = GPUtil.findNextCity()
			else:
				pCity = gc.getActivePlayer().getCity(iCity)
			if pCity and not pCity.isNone():
				CyInterface().selectCity(pCity, False)
			return 1
# BUG - Great Person Bar - end

# BUG - field of view slider - start
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_SLIDER_NEWSTOP):
			if (inputClass.getFunctionName() == self.szSliderId):
				screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
				self.iField_View = inputClass.getData() + 1
				self.setFieldofView(screen, False)
				self.setFieldofView_Text(screen)
				MainOpt.setFieldOfView(self.iField_View)
# BUG - field of view slider - end

		return 0
	
# BUG - Raw Yields - start
	def handleRawYieldsButtons(self, inputClass):
		iButton = inputClass.getID()
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON):
			self.PLE.displayHelpHover(RAW_YIELD_HELP[iButton])
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF):
			self.PLE.hideInfoPane()
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			global g_bYieldView
			global g_iYieldType
			global g_iYieldTiles
			if iButton == 0:
				g_bYieldView = False
			elif iButton in (1, 2, 3):
				g_bYieldView = True
				g_iYieldType = RawYields.YIELDS[iButton - 1]
			elif iButton in (4, 5, 6):
				g_bYieldView = True
				g_iYieldTiles = RawYields.TILES[iButton - 4]
			else:
				return 0
			CyInterface().setDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT, True)
			return 1
		return 0
# BUG - Raw Yields - end
	
	def update(self, fDelta):
		return
	
	def forward(self):
		if (not CyInterface().isFocused() or CyInterface().isCityScreenUp()):
			if (CyInterface().isCitySelection()):
				CyGame().doControl(ControlTypes.CONTROL_NEXTCITY)
			else:
				CyGame().doControl(ControlTypes.CONTROL_NEXTUNIT)
		
	def back(self):
		if (not CyInterface().isFocused() or CyInterface().isCityScreenUp()):
			if (CyInterface().isCitySelection()):
				CyGame().doControl(ControlTypes.CONTROL_PREVCITY)
			else:
				CyGame().doControl(ControlTypes.CONTROL_PREVUNIT)

# BUG - field of view slider - start
	def setFieldofView(self, screen, bDefault):
		if bDefault or not MainOpt.isShowFieldOfView():
			self._setFieldofView(screen, DEFAULT_FIELD_OF_VIEW)
		else:
			self._setFieldofView(screen, self.iField_View)

	def _setFieldofView(self, screen, iFoV):
		if self.iField_View_Prev != iFoV:
			gc.setDefineFLOAT("FIELD_OF_VIEW", float(iFoV))
			self.iField_View_Prev = iFoV

	def setFieldofView_Text(self, screen):
		zsFieldOfView_Text = "%s [%i]" % (self.sFieldOfView_Text, self.iField_View)
		screen.setLabel(self.szSliderTextId, "", zsFieldOfView_Text, CvUtil.FONT_RIGHT_JUSTIFY, self.iX_FoVSlider, self.iY_FoVSlider + 6, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
# BUG - field of view slider - end
