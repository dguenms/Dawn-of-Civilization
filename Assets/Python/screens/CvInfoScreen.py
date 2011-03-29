## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

# Thanks to "Ulf 'ulfn' Norell" from Apolyton for his additions relating to the graph section of this screen

from CvPythonExtensions import *
import CvScreenEnums
import CvUtil
import ScreenInput

import string
import time

import Consts as con #Rhye

from PyHelpers import PyPlayer

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

def iff(b, x, y):
    if b:
	return x
    else:
	return y

class CvInfoScreen:
	"Info Screen! Contains the Demographics, Wonders / Top Cities and Statistics Screens"

	def __init__(self, screenId):

		self.screenId = screenId
		self.DEMO_SCREEN_NAME = "DemographicsScreen"
		self.TOP_CITIES_SCREEN_NAME = "TopCitiesScreen"

		self.INTERFACE_ART_INFO = "TECH_BG"

		self.WIDGET_ID = "DemoScreenWidget"
		self.LINE_ID   = "DemoLine"

		self.Z_BACKGROUND = -6.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.DZ = -0.2
		self.Z_HELP_AREA = self.Z_CONTROLS - 1

		self.X_SCREEN = 0
		self.Y_SCREEN = 0
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.X_TITLE = 512
		self.Y_TITLE = 8
		self.BORDER_WIDTH = 4
		self.W_HELP_AREA = 200

		self.X_EXIT = 994
		self.Y_EXIT = 730

		self.X_GRAPH_TAB	= 30
		self.X_DEMOGRAPHICS_TAB = 165
		self.X_TOP_CITIES_TAB	= 425
		self.X_STATS_TAB	= 663
		self.Y_TABS		= 730
		self.W_BUTTON		= 200
		self.H_BUTTON		= 30

		self.graphEnd	    = CyGame().getGameTurn() - 1
		self.graphZoom	    = self.graphEnd - CyGame().getStartTurn()
		self.nWidgetCount   = 0
		self.nLineCount	    = 0

		# This is used to allow the wonders screen to refresh without redrawing everything
		self.iNumWondersPermanentWidgets = 0

		self.iGraphID		=	0
		self.iDemographicsID	=	1
		self.iTopCitiesID	=	2
		self.iStatsID		=	3

		self.iActiveTab = self.iGraphID

		self.TOTAL_SCORE	= 0
		self.ECONOMY_SCORE	= 1
		self.INDUSTRY_SCORE	= 2
		self.AGRICULTURE_SCORE	= 3
		self.POWER_SCORE	= 4
		self.CULTURE_SCORE	= 5
		self.ESPIONAGE_SCORE	= 6
		self.NUM_SCORES		= 7
		self.RANGE_SCORES	= range(self.NUM_SCORES)

		self.scoreCache	= []
		for t in self.RANGE_SCORES:
		    self.scoreCache.append(None)

		self.GRAPH_H_LINE = "GraphHLine"
		self.GRAPH_V_LINE = "GraphVLine"

		self.xSelPt = 0
		self.ySelPt = 0
		
		self.graphLeftButtonID = ""
		self.graphRightButtonID = ""
		

################################################## GRAPH ###################################################

		self.X_MARGIN	= 45
		self.Y_MARGIN	= 80
		self.H_DROPDOWN	= 35

		self.X_DEMO_DROPDOWN	= self.X_MARGIN
		self.Y_DEMO_DROPDOWN	= self.Y_MARGIN
		self.W_DEMO_DROPDOWN	= 150 #247

		self.X_ZOOM_DROPDOWN	= self.X_DEMO_DROPDOWN
		self.Y_ZOOM_DROPDOWN	= self.Y_DEMO_DROPDOWN + self.H_DROPDOWN
		self.W_ZOOM_DROPDOWN	= self.W_DEMO_DROPDOWN

		self.X_LEGEND		= self.X_DEMO_DROPDOWN
		self.Y_LEGEND		= self.Y_ZOOM_DROPDOWN + self.H_DROPDOWN + 3
		self.W_LEGEND		= self.W_DEMO_DROPDOWN
		#self.H_LEGEND		= 200	this is computed from the number of players

		self.X_GRAPH = self.X_DEMO_DROPDOWN + self.W_DEMO_DROPDOWN + 10
		self.Y_GRAPH = self.Y_MARGIN
		self.W_GRAPH = self.W_SCREEN - self.X_GRAPH - self.X_MARGIN
		self.H_GRAPH = 590

		self.W_LEFT_BUTTON  = 20
		self.H_LEFT_BUTTON  = 20
		self.X_LEFT_BUTTON  = self.X_GRAPH
		self.Y_LEFT_BUTTON  = self.Y_GRAPH + self.H_GRAPH

		self.W_RIGHT_BUTTON  = self.W_LEFT_BUTTON
		self.H_RIGHT_BUTTON  = self.H_LEFT_BUTTON
		self.X_RIGHT_BUTTON  = self.X_GRAPH + self.W_GRAPH - self.W_RIGHT_BUTTON
		self.Y_RIGHT_BUTTON  = self.Y_LEFT_BUTTON

		self.X_LEFT_LABEL   = self.X_LEFT_BUTTON + self.W_LEFT_BUTTON + 10
		self.X_RIGHT_LABEL  = self.X_RIGHT_BUTTON - 10
		self.Y_LABEL	    = self.Y_GRAPH + self.H_GRAPH + 3

		self.X_LEGEND_MARGIN	= 10
		self.Y_LEGEND_MARGIN	= 5
		self.X_LEGEND_LINE	= self.X_LEGEND_MARGIN
		self.Y_LEGEND_LINE	= self.Y_LEGEND_MARGIN + 9  # to center it relative to the text
		self.W_LEGEND_LINE	= 30
		self.X_LEGEND_TEXT	= self.X_LEGEND_LINE + self.W_LEGEND_LINE + 10
		self.Y_LEGEND_TEXT	= self.Y_LEGEND_MARGIN
		self.H_LEGEND_TEXT	= 16

		self.TOTAL_SCORE	= 0
		self.ECONOMY_SCORE	= 1
		self.INDUSTRY_SCORE	= 2
		self.AGRICULTURE_SCORE	= 3
		self.POWER_SCORE	= 4
		self.CULTURE_SCORE	= 5
		self.ESPIONAGE_SCORE	= 6

############################################### DEMOGRAPHICS ###############################################

		self.X_CHART = 45
		self.Y_CHART = 80
		self.W_CHART = 934
		self.H_CHART = 600

		self.BUTTON_SIZE = 20

		self.W_TEXT = 140
		self.H_TEXT = 15
		self.X_TEXT_BUFFER = 0
		self.Y_TEXT_BUFFER = 43

		self.X_COL_1 = 535
		self.X_COL_2 = self.X_COL_1 + self.W_TEXT + self.X_TEXT_BUFFER
		self.X_COL_3 = self.X_COL_2 + self.W_TEXT + self.X_TEXT_BUFFER
		self.X_COL_4 = self.X_COL_3 + self.W_TEXT + self.X_TEXT_BUFFER

		self.Y_ROW_1 = 100
		self.Y_ROW_2 = self.Y_ROW_1 + self.H_TEXT + self.Y_TEXT_BUFFER
		self.Y_ROW_3 = self.Y_ROW_2 + self.H_TEXT + self.Y_TEXT_BUFFER
		self.Y_ROW_4 = self.Y_ROW_3 + self.H_TEXT + self.Y_TEXT_BUFFER
		self.Y_ROW_5 = self.Y_ROW_4 + self.H_TEXT + self.Y_TEXT_BUFFER
		self.Y_ROW_6 = self.Y_ROW_5 + self.H_TEXT + self.Y_TEXT_BUFFER
		self.Y_ROW_7 = self.Y_ROW_6 + self.H_TEXT + self.Y_TEXT_BUFFER
		self.Y_ROW_8 = self.Y_ROW_7 + self.H_TEXT + self.Y_TEXT_BUFFER
		self.Y_ROW_9 = self.Y_ROW_8 + self.H_TEXT + self.Y_TEXT_BUFFER
		self.Y_ROW_10 = self.Y_ROW_9 + self.H_TEXT + self.Y_TEXT_BUFFER

		self.bAbleToShowAllPlayers = false
		self.iShowingPlayer = -1
		self.aiDropdownPlayerIDs = []

############################################### TOP CITIES ###############################################

		self.X_LEFT_PANE = 45
		self.Y_LEFT_PANE = 70
		self.W_LEFT_PANE = 470
		self.H_LEFT_PANE = 620

		# Text

		self.W_TC_TEXT = 280
		self.H_TC_TEXT = 15
		self.X_TC_TEXT_BUFFER = 0
		self.Y_TC_TEXT_BUFFER = 43

		# Animated City thingies

		self.X_CITY_ANIMATION = self.X_LEFT_PANE + 20
		self.Z_CITY_ANIMATION = self.Z_BACKGROUND - 0.5
		self.W_CITY_ANIMATION = 150
		self.H_CITY_ANIMATION = 110
		self.Y_CITY_ANIMATION_BUFFER = self.H_CITY_ANIMATION / 2

		self.X_ROTATION_CITY_ANIMATION = -20
		self.Z_ROTATION_CITY_ANIMATION = 30
		self.SCALE_ANIMATION = 0.5

		# Placement of Cities

		self.X_COL_1_CITIES = self.X_LEFT_PANE + 20
		self.Y_CITIES_BUFFER = 118

		self.Y_ROWS_CITIES = []
		self.Y_ROWS_CITIES.append(self.Y_LEFT_PANE + 20)
		for i in range(1,5):
			self.Y_ROWS_CITIES.append(self.Y_ROWS_CITIES[i-1] + self.Y_CITIES_BUFFER)

		self.X_COL_1_CITIES_DESC = self.X_LEFT_PANE + self.W_CITY_ANIMATION + 30
		self.Y_CITIES_DESC_BUFFER = -4
		self.W_CITIES_DESC = 275
		self.H_CITIES_DESC = 60

		self.Y_CITIES_WONDER_BUFFER = 57
		self.W_CITIES_WONDER = 275
		self.H_CITIES_WONDER = 51

############################################### WONDERS ###############################################

		self.X_RIGHT_PANE = 520
		self.Y_RIGHT_PANE = 70
		self.W_RIGHT_PANE = 460
		self.H_RIGHT_PANE = 620

		# Info about this wonder, e.g. name, cost so on

		self.X_STATS_PANE = self.X_RIGHT_PANE + 20
		self.Y_STATS_PANE = self.Y_RIGHT_PANE + 20
		self.W_STATS_PANE = 210
		self.H_STATS_PANE = 220

		# Wonder mode dropdown Box

		self.X_DROPDOWN = self.X_RIGHT_PANE + 240 + 3 # the 3 is the 'fudge factor' due to the widgets not lining up perfectly
		self.Y_DROPDOWN = self.Y_RIGHT_PANE + 20
		self.W_DROPDOWN = 200

		# List Box that displays all wonders built

		self.X_WONDER_LIST = self.X_RIGHT_PANE + 240 + 6 # the 6 is the 'fudge factor' due to the widgets not lining up perfectly
		self.Y_WONDER_LIST = self.Y_RIGHT_PANE + 60
		self.W_WONDER_LIST = 200 - 6 # the 6 is the 'fudge factor' due to the widgets not lining up perfectly
		self.H_WONDER_LIST = 180

		# Animated Wonder thingies

		self.X_WONDER_GRAPHIC = 540
		self.Y_WONDER_GRAPHIC = self.Y_RIGHT_PANE + 20 + 200 + 35
		self.W_WONDER_GRAPHIC = 420
		self.H_WONDER_GRAPHIC = 190

		self.X_ROTATION_WONDER_ANIMATION = -20
		self.Z_ROTATION_WONDER_ANIMATION = 30

		# Icons used for Projects instead because no on-map art exists
		self.X_PROJECT_ICON = self.X_WONDER_GRAPHIC + self.W_WONDER_GRAPHIC / 2
		self.Y_PROJECT_ICON = self.Y_WONDER_GRAPHIC + self.H_WONDER_GRAPHIC / 2
		self.W_PROJECT_ICON = 128

		# Special Stats about this wonder

		self.X_SPECIAL_TITLE = 540
		self.Y_SPECIAL_TITLE = 310 + 200 + 7

		self.X_SPECIAL_PANE = 540
		self.Y_SPECIAL_PANE = 310 + 200 + 20 + 15
		self.W_SPECIAL_PANE = 420
		self.H_SPECIAL_PANE = 140 - 15

		self.szWonderDisplayMode = "World Wonders"

		self.iWonderID = -1			# BuildingType ID of the active wonder, e.g. Palace is 0, Globe Theater is 66
		self.iActiveWonderCounter = 0		# Screen ID for this wonder (0, 1, 2, etc.) - different from the above variable

############################################### STATISTICS ###############################################

		# STATISTICS TAB

		# Top Panel

		self.X_STATS_TOP_PANEL = 45
		self.Y_STATS_TOP_PANEL = 75
		self.W_STATS_TOP_PANEL = 935
		self.H_STATS_TOP_PANEL = 180

		# Leader

		self.X_LEADER_ICON = 250
		self.Y_LEADER_ICON = 95
		self.H_LEADER_ICON = 140
		self.W_LEADER_ICON = 110

		# Top Chart

		self.X_STATS_TOP_CHART = 400
		self.Y_STATS_TOP_CHART = 130
		self.W_STATS_TOP_CHART = 380
		self.H_STATS_TOP_CHART = 102

		self.STATS_TOP_CHART_W_COL_0 = 304
		self.STATS_TOP_CHART_W_COL_1 = 76

		self.iNumTopChartCols = 2
		self.iNumTopChartRows = 4

		self.X_LEADER_NAME = self.X_STATS_TOP_CHART
		self.Y_LEADER_NAME = self.Y_STATS_TOP_CHART - 40

		# Bottom Chart

		self.X_STATS_BOTTOM_CHART = 45
		self.Y_STATS_BOTTOM_CHART = 280
		self.W_STATS_BOTTOM_CHART_UNITS = 545
		self.W_STATS_BOTTOM_CHART_BUILDINGS = 390
		self.H_STATS_BOTTOM_CHART = 410

		self.reset()

	def initText(self):

		###### TEXT ######
		self.SCREEN_TITLE = u"<font=4b>" + localText.getText("TXT_KEY_INFO_SCREEN", ()).upper() + u"</font>"
		self.SCREEN_GRAPH_TITLE = u"<font=4b>" + localText.getText("TXT_KEY_INFO_GRAPH", ()).upper() + u"</font>"
		self.SCREEN_DEMOGRAPHICS_TITLE = u"<font=4b>" + localText.getText("TXT_KEY_DEMO_SCREEN_TITLE", ()).upper() + u"</font>"
		self.SCREEN_TOP_CITIES_TITLE = u"<font=4b>" + localText.getText("TXT_KEY_WONDERS_SCREEN_TOP_CITIES_TEXT", ()).upper() + u"</font>"
		self.SCREEN_STATS_TITLE = u"<font=4b>" + localText.getText("TXT_KEY_INFO_SCREEN_STATISTICS_TITLE", ()).upper() + u"</font>"

		self.EXIT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + u"</font>"

		self.TEXT_GRAPH = u"<font=3>" + localText.getText("TXT_KEY_INFO_GRAPH", ()).upper() + u"</font>"
		self.TEXT_DEMOGRAPHICS = u"<font=3>" + localText.getText("TXT_KEY_DEMO_SCREEN_TITLE", ()).upper() + u"</font>"
		self.TEXT_DEMOGRAPHICS_SMALL = localText.getText("TXT_KEY_DEMO_SCREEN_TITLE", ())
		self.TEXT_TOP_CITIES = u"<font=3>" + localText.getText("TXT_KEY_WONDERS_SCREEN_TOP_CITIES_TEXT", ()).upper() + u"</font>"
		self.TEXT_STATS = u"<font=3>" + localText.getText("TXT_KEY_INFO_SCREEN_STATISTICS_TITLE", ()).upper() + u"</font>"
		self.TEXT_GRAPH_YELLOW = u"<font=3>" + localText.getColorText("TXT_KEY_INFO_GRAPH", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + u"</font>"
		self.TEXT_DEMOGRAPHICS_YELLOW = u"<font=3>" + localText.getColorText("TXT_KEY_DEMO_SCREEN_TITLE", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + u"</font>"
		self.TEXT_TOP_CITIES_YELLOW = u"<font=3>" + localText.getColorText("TXT_KEY_WONDERS_SCREEN_TOP_CITIES_TEXT", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + u"</font>"
		self.TEXT_STATS_YELLOW = u"<font=3>" + localText.getColorText("TXT_KEY_INFO_SCREEN_STATISTICS_TITLE", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + u"</font>"

		self.TEXT_SHOW_ALL_PLAYERS =  localText.getText("TXT_KEY_SHOW_ALL_PLAYERS", ())
		self.TEXT_SHOW_ALL_PLAYERS_GRAY = localText.getColorText("TXT_KEY_SHOW_ALL_PLAYERS", (), gc.getInfoTypeForString("COLOR_PLAYER_GRAY")).upper()
		
		self.TEXT_ENTIRE_HISTORY = localText.getText("TXT_KEY_INFO_ENTIRE_HISTORY", ())
		
		self.TEXT_SCORE = localText.getText("TXT_KEY_GAME_SCORE", ())
		self.TEXT_POWER = localText.getText("TXT_KEY_POWER", ())
		self.TEXT_CULTURE = localText.getObjectText("TXT_KEY_COMMERCE_CULTURE", 0)
		self.TEXT_ESPIONAGE = localText.getObjectText("TXT_KEY_ESPIONAGE_CULTURE", 0)

		self.TEXT_VALUE = localText.getText("TXT_KEY_DEMO_SCREEN_VALUE_TEXT", ())
		self.TEXT_RANK = localText.getText("TXT_KEY_DEMO_SCREEN_RANK_TEXT", ())
		self.TEXT_AVERAGE = localText.getText("TXT_KEY_DEMOGRAPHICS_SCREEN_RIVAL_AVERAGE", ())
		self.TEXT_BEST = localText.getText("TXT_KEY_INFO_RIVAL_BEST", ())
		self.TEXT_WORST = localText.getText("TXT_KEY_INFO_RIVAL_WORST", ())

		self.TEXT_ECONOMY = localText.getText("TXT_KEY_DEMO_SCREEN_ECONOMY_TEXT", ())
		self.TEXT_INDUSTRY = localText.getText("TXT_KEY_DEMO_SCREEN_INDUSTRY_TEXT", ())
		self.TEXT_AGRICULTURE = localText.getText("TXT_KEY_DEMO_SCREEN_AGRICULTURE_TEXT", ())
		self.TEXT_MILITARY = localText.getText("TXT_KEY_DEMO_SCREEN_MILITARY_TEXT", ())
		self.TEXT_LAND_AREA = localText.getText("TXT_KEY_DEMO_SCREEN_LAND_AREA_TEXT", ())
		self.TEXT_POPULATION = localText.getText("TXT_KEY_DEMO_SCREEN_POPULATION_TEXT", ())
		self.TEXT_HAPPINESS = localText.getText("TXT_KEY_DEMO_SCREEN_HAPPINESS_TEXT", ())
		self.TEXT_HEALTH = localText.getText("TXT_KEY_DEMO_SCREEN_HEALTH_TEXT", ())
		self.TEXT_IMP_EXP = localText.getText("TXT_KEY_DEMO_SCREEN_EXPORTS_TEXT", ()) + " - " + localText.getText("TXT_KEY_DEMO_SCREEN_IMPORTS_TEXT", ())

		self.TEXT_ECONOMY_MEASURE = (u"  %c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)) + localText.getText("TXT_KEY_DEMO_SCREEN_ECONOMY_MEASURE", ())
		self.TEXT_INDUSTRY_MEASURE = (u"  %c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)) + localText.getText("TXT_KEY_DEMO_SCREEN_INDUSTRY_MEASURE", ())
		self.TEXT_AGRICULTURE_MEASURE = (u"  %c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)) + localText.getText("TXT_KEY_DEMO_SCREEN_AGRICULTURE_MEASURE", ())
		self.TEXT_MILITARY_MEASURE = ""
		self.TEXT_LAND_AREA_MEASURE = (u"  %c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)) + localText.getText("TXT_KEY_DEMO_SCREEN_LAND_AREA_MEASURE", ())
		self.TEXT_POPULATION_MEASURE = ""
		self.TEXT_HAPPINESS_MEASURE = "%"
		self.TEXT_HEALTH_MEASURE = (u"  %c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)) + localText.getText("TXT_KEY_DEMO_SCREEN_POPULATION_MEASURE", ())
		self.TEXT_IMP_EXP_MEASURE = (u"  %c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)) + localText.getText("TXT_KEY_DEMO_SCREEN_ECONOMY_MEASURE", ())

		self.TEXT_TIME_PLAYED = localText.getText("TXT_KEY_INFO_SCREEN_TIME_PLAYED", ())
		self.TEXT_CITIES_BUILT = localText.getText("TXT_KEY_INFO_SCREEN_CITIES_BUILT", ())
		self.TEXT_CITIES_RAZED = localText.getText("TXT_KEY_INFO_SCREEN_CITIES_RAZED", ())
		self.TEXT_NUM_GOLDEN_AGES = localText.getText("TXT_KEY_INFO_SCREEN_NUM_GOLDEN_AGES", ())
		self.TEXT_NUM_RELIGIONS_FOUNDED = localText.getText("TXT_KEY_INFO_SCREEN_RELIGIONS_FOUNDED", ())

		self.TEXT_CURRENT = localText.getText("TXT_KEY_CURRENT", ())
		self.TEXT_UNITS = localText.getText("TXT_KEY_CONCEPT_UNITS", ())
		self.TEXT_BUILDINGS = localText.getText("TXT_KEY_CONCEPT_BUILDINGS", ())
		self.TEXT_KILLED = localText.getText("TXT_KEY_INFO_SCREEN_KILLED", ())
		self.TEXT_LOST = localText.getText("TXT_KEY_INFO_SCREEN_LOST", ())
		self.TEXT_BUILT = localText.getText("TXT_KEY_INFO_SCREEN_BUILT", ())

	def reset(self):

		# City Members

		self.szCityNames = [    "",
					"",
					"",
					"",
					""	]

		self.iCitySizes = [	-1,
					-1,
					-1,
					-1,
					-1	]

		self.szCityDescs = [    "",
					"",
					"",
					"",
					""	]

		self.aaCitiesXY = [	[-1, -1],
					[-1, -1],
					[-1, -1],
					[-1, -1],
					[-1, -1]	]

		self.iCityValues =   [  0,
					0,
					0,
					0,
					0	]

		self.pCityPointers = [  0,
					0,
					0,
					0,
					0	]

#		self.bShowAllPlayers = false
		self.graphEnd	    = CyGame().getGameTurn() - 1
		self.graphZoom	    = self.graphEnd - CyGame().getStartTurn()
		self.iShowingPlayer = -1

		for t in self.RANGE_SCORES:
		    self.scoreCache[t]	= None

	def resetWonders(self):

		self.szWonderDisplayMode = "World Wonders"

		self.iWonderID = -1			# BuildingType ID of the active wonder, e.g. Palace is 0, Globe Theater is 66
		self.iActiveWonderCounter = 0		# Screen ID for this wonder (0, 1, 2, etc.) - different from the above variable

		self.aiWonderListBoxIDs = []
		self.aiTurnYearBuilt = []
		self.aiWonderBuiltBy = []
		self.aszWonderCity = []

	def getScreen(self):
		return CyGInterfaceScreen(self.DEMO_SCREEN_NAME, self.screenId)

	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()

	def getLastTurn(self):
		return (gc.getGame().getReplayMessageTurn(gc.getGame().getNumReplayMessages()-1))

	# Screen construction function
	def showScreen(self, iTurn, iTabID, iEndGame):

		self.initText();

		self.iStartTurn = 0
		for iI in range(gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getNumTurnIncrements()):
			self.iStartTurn += gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGameTurnInfo(iI).iNumGameTurnsPerIncrement
		self.iStartTurn *= gc.getEraInfo(gc.getGame().getStartEra()).getStartPercent()
		self.iStartTurn /= 100

		self.iTurn = 0

		if (iTurn > self.getLastTurn()):
			return

		# Create a new screen
		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.reset()

		self.deleteAllWidgets()

		# Set the background widget and exit button
		screen.addDDSGFC("DemographicsScreenBackground", ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.showWindowBackground( False )
		screen.setDimensions(screen.centerX(self.X_SCREEN), screen.centerY(self.Y_SCREEN), self.W_SCREEN, self.H_SCREEN)
		self.szExitButtonName = self.getNextWidgetName()
		screen.setText(self.szExitButtonName, "Background", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Header...
		self.szHeaderWidget = self.getNextWidgetName()
		screen.setText(self.szHeaderWidget, "Background", self.SCREEN_TITLE, CvUtil.FONT_CENTER_JUSTIFY, self.X_TITLE, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Help area for tooltips
		screen.setHelpTextArea(self.W_HELP_AREA, FontTypes.SMALL_FONT, self.X_SCREEN, self.Y_SCREEN, self.Z_HELP_AREA, 1, ArtFileMgr.getInterfaceArtInfo("POPUPS_BACKGROUND_TRANSPARENT").getPath(), True, True, CvUtil.FONT_LEFT_JUSTIFY, 0 )

		self.DEBUG_DROPDOWN_ID = ""

		if (CyGame().isDebugMode()):
			self.DEBUG_DROPDOWN_ID = "InfoScreenDropdownWidget"
			self.szDropdownName = self.DEBUG_DROPDOWN_ID
			screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for j in range(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getName(), j, j, False )

		self.iActivePlayer = CyGame().getActivePlayer()
		self.pActivePlayer = gc.getPlayer(self.iActivePlayer)
		self.iActiveTeam = self.pActivePlayer.getTeam()
		self.pActiveTeam = gc.getTeam(self.iActiveTeam)
		
		iDemographicsMission = -1
		# See if Espionage allows graph to be shown for each player
		if not (gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ESPIONAGE)):
			for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
				if (gc.getEspionageMissionInfo(iMissionLoop).isSeeDemographics()):
					iDemographicsMission = iMissionLoop
				
		# Determine who this active player knows
		self.aiPlayersMet = []
		self.iNumPlayersMet = 0
		for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			iLoopPlayerTeam = pLoopPlayer.getTeam()
			if (gc.getTeam(iLoopPlayerTeam).isEverAlive()):
				if (self.pActiveTeam.isHasMet(iLoopPlayerTeam) or CyGame().isDebugMode() or iEndGame != 0):
					if (	iDemographicsMission == -1 or
							self.pActivePlayer.canDoEspionageMission(iDemographicsMission, iLoopPlayer, None, -1) or
							iEndGame != 0 or
							iLoopPlayerTeam == CyGame().getActiveTeam()
                                                        or CyGame().isDebugMode()): #Rhye
						self.aiPlayersMet.append(iLoopPlayer)
						self.iNumPlayersMet += 1

		# "Save" current widgets so they won't be deleted later when changing tabs
		self.iNumPermanentWidgets = self.nWidgetCount

		# Reset variables
		self.graphEnd	= CyGame().getGameTurn() - 1
		self.graphZoom	= self.graphEnd - CyGame().getStartTurn()

		self.iActiveTab = iTabID
		if (self.iNumPlayersMet > 1):
			self.iShowingPlayer = 666#self.iActivePlayer
		else:
			self.iShowingPlayer = self.iActivePlayer

		self.redrawContents()

		return

	def redrawContents(self):

		screen = self.getScreen()
		self.deleteAllWidgets(self.iNumPermanentWidgets)
		self.iNumWondersPermanentWidgets = 0

		self.szGraphTabWidget = self.getNextWidgetName()
		self.szDemographicsTabWidget = self.getNextWidgetName()
		self.szTopCitiesTabWidget = self.getNextWidgetName()
		self.szStatsTabWidget = self.getNextWidgetName()

		# Draw Tab buttons and tabs
		if (self.iActiveTab == self.iGraphID):
			screen.setText(self.szGraphTabWidget, "", self.TEXT_GRAPH_YELLOW, CvUtil.FONT_LEFT_JUSTIFY, self.X_GRAPH_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setText(self.szDemographicsTabWidget, "", self.TEXT_DEMOGRAPHICS, CvUtil.FONT_LEFT_JUSTIFY, self.X_DEMOGRAPHICS_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setText(self.szTopCitiesTabWidget, "", self.TEXT_TOP_CITIES, CvUtil.FONT_LEFT_JUSTIFY, self.X_TOP_CITIES_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setText(self.szStatsTabWidget, "", self.TEXT_STATS, CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			self.drawGraphTab()

		elif (self.iActiveTab == self.iDemographicsID):
			screen.setText(self.szGraphTabWidget, "", self.TEXT_GRAPH, CvUtil.FONT_LEFT_JUSTIFY, self.X_GRAPH_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setText(self.szDemographicsTabWidget, "", self.TEXT_DEMOGRAPHICS_YELLOW, CvUtil.FONT_LEFT_JUSTIFY, self.X_DEMOGRAPHICS_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setText(self.szTopCitiesTabWidget, "", self.TEXT_TOP_CITIES, CvUtil.FONT_LEFT_JUSTIFY, self.X_TOP_CITIES_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setText(self.szStatsTabWidget, "", self.TEXT_STATS, CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			self.drawDemographicsTab()

		elif(self.iActiveTab == self.iTopCitiesID):
			screen.setText(self.szGraphTabWidget, "", self.TEXT_GRAPH, CvUtil.FONT_LEFT_JUSTIFY, self.X_GRAPH_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setText(self.szDemographicsTabWidget, "", self.TEXT_DEMOGRAPHICS, CvUtil.FONT_LEFT_JUSTIFY, self.X_DEMOGRAPHICS_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setText(self.szTopCitiesTabWidget, "", self.TEXT_TOP_CITIES_YELLOW, CvUtil.FONT_LEFT_JUSTIFY, self.X_TOP_CITIES_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setText(self.szStatsTabWidget, "", self.TEXT_STATS, CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			self.drawTopCitiesTab()

		elif(self.iActiveTab == self.iStatsID):
			screen.setText(self.szGraphTabWidget, "", self.TEXT_GRAPH, CvUtil.FONT_LEFT_JUSTIFY, self.X_GRAPH_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setText(self.szDemographicsTabWidget, "", self.TEXT_DEMOGRAPHICS, CvUtil.FONT_LEFT_JUSTIFY, self.X_DEMOGRAPHICS_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setText(self.szTopCitiesTabWidget, "", self.TEXT_TOP_CITIES, CvUtil.FONT_LEFT_JUSTIFY, self.X_TOP_CITIES_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setText(self.szStatsTabWidget, "", self.TEXT_STATS_YELLOW, CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			self.drawStatsTab()

#############################################################################################################
#################################################### GRAPH ##################################################
#############################################################################################################

	def drawGraphTab(self):

	    self.iGraphTabID = self.TOTAL_SCORE
	    self.drawPermanentGraphWidgets()
	    self.drawGraph()

	def drawPermanentGraphWidgets(self):

	    screen = self.getScreen()

	    self.H_LEGEND = 2 * self.Y_LEGEND_MARGIN + self.iNumPlayersMet * self.H_LEGEND_TEXT + 3
	    self.Y_LEGEND = self.Y_GRAPH + self.H_GRAPH - self.H_LEGEND

	    self.LEGEND_PANEL_ID = self.getNextWidgetName()
	    screen.addPanel( self.LEGEND_PANEL_ID, "", "", true, true
			   , self.X_LEGEND, self.Y_LEGEND, self.W_LEGEND, self.H_LEGEND
			   , PanelStyles.PANEL_STYLE_IN
			   )
	    self.LEGEND_CANVAS_ID = self.getNextWidgetName()
	    screen.addDrawControl(self.LEGEND_CANVAS_ID, None, self.X_LEGEND, self.Y_LEGEND, self.W_LEGEND, self.H_LEGEND, WidgetTypes.WIDGET_GENERAL, -1, -1)

	    self.drawLegend()

	    self.graphLeftButtonID = self.getNextWidgetName()
	    screen.setButtonGFC( self.graphLeftButtonID, u"", "", self.X_LEFT_BUTTON, self.Y_LEFT_BUTTON, self.W_LEFT_BUTTON, self.H_LEFT_BUTTON, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
	    self.graphRightButtonID = self.getNextWidgetName()
	    screen.setButtonGFC( self.graphRightButtonID, u"", "", self.X_RIGHT_BUTTON, self.Y_RIGHT_BUTTON, self.W_RIGHT_BUTTON, self.H_RIGHT_BUTTON, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
	    screen.enable(self.graphLeftButtonID, False)
	    screen.enable(self.graphRightButtonID, False)

	    # Dropdown Box
	    self.szGraphDropdownWidget = self.getNextWidgetName()
	    screen.addDropDownBoxGFC(self.szGraphDropdownWidget, self.X_DEMO_DROPDOWN, self.Y_DEMO_DROPDOWN, self.W_DEMO_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
	    screen.addPullDownString(self.szGraphDropdownWidget, self.TEXT_SCORE, 0, 0, False )
	    screen.addPullDownString(self.szGraphDropdownWidget, self.TEXT_ECONOMY, 1, 1, False )
	    screen.addPullDownString(self.szGraphDropdownWidget, self.TEXT_INDUSTRY, 2, 2, False )
	    screen.addPullDownString(self.szGraphDropdownWidget, self.TEXT_AGRICULTURE, 3, 3, False )
	    screen.addPullDownString(self.szGraphDropdownWidget, self.TEXT_POWER, 4, 4, False )
	    screen.addPullDownString(self.szGraphDropdownWidget, self.TEXT_CULTURE, 5, 5, False )
	    screen.addPullDownString(self.szGraphDropdownWidget, self.TEXT_ESPIONAGE, 6, 6, False )

	    self.dropDownTurns = []
	    self.szTurnsDropdownWidget = self.getNextWidgetName()
	    screen.addDropDownBoxGFC(self.szTurnsDropdownWidget, self.X_ZOOM_DROPDOWN, self.Y_ZOOM_DROPDOWN, self.W_ZOOM_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
	    start = CyGame().getStartTurn()
	    now   = CyGame().getGameTurn()
	    nTurns = now - start - 1
	    screen.addPullDownString(self.szTurnsDropdownWidget, self.TEXT_ENTIRE_HISTORY, 0, 0, False)
	    self.dropDownTurns.append(nTurns)
	    iCounter = 1
	    last = 50
	    while (last < nTurns):
		screen.addPullDownString(self.szTurnsDropdownWidget, localText.getText("TXT_KEY_INFO_NUM_TURNS", (last,)), iCounter, iCounter, False)
		self.dropDownTurns.append(last)
		iCounter += 1
		last += 50

	    self.iNumPreDemoChartWidgets = self.nWidgetCount

	def updateGraphButtons(self):
	    screen = self.getScreen()
	    screen.enable(self.graphLeftButtonID, self.graphEnd - self.graphZoom > CyGame().getStartTurn())
	    screen.enable(self.graphRightButtonID, self.graphEnd < CyGame().getGameTurn() - 1)

	def checkGraphBounds(self):
	    start = CyGame().getStartTurn()
	    end   = CyGame().getGameTurn() - 1
	    if (self.graphEnd - self.graphZoom < start):
		self.graphEnd = start + self.graphZoom
	    if (self.graphEnd > end):
		self.graphEnd = end

	def zoomGraph(self, zoom):
	    self.graphZoom = zoom
	    self.checkGraphBounds()
	    self.updateGraphButtons()

	def slideGraph(self, right):
	    self.graphEnd += right
	    self.checkGraphBounds()
	    self.updateGraphButtons()

	def buildScoreCache(self, scoreType):

	    # Check if the scores have already been computed
	    if (self.scoreCache[scoreType]):
		return

	    print("Rebuilding score cache")

	    # Get the player with the highest ID
	    maxPlayer = 0
	    for p in self.aiPlayersMet:
                
                if (not gc.getPlayer(p).isMinorCiv()): #Rhye
                    
                    if (maxPlayer < p):
                        maxPlayer = p

	    # Compute the scores
	    self.scoreCache[scoreType] = []
	    for p in range(maxPlayer + 1):

		if (p not in self.aiPlayersMet):
		    # Don't compute score for people we haven't met
		    self.scoreCache[scoreType].append(None)

		else:

		    self.scoreCache[scoreType].append([])
		    firstTurn	= CyGame().getStartTurn()
		    thisTurn	= CyGame().getGameTurn()
		    turn	= firstTurn
		    while (turn <= thisTurn):
			self.scoreCache[scoreType][p].append(self.computeHistory(scoreType, p, turn))
			turn += 1

	    return

	def computeHistory(self, scoreType, iPlayer, iTurn):

	    iScore = gc.getPlayer(iPlayer).getScoreHistory(iTurn)

	    if (iScore == 0):	# for some reason only the score is 0 when you're dead..?
		return 0

	    if (scoreType == self.TOTAL_SCORE):
		return iScore
	    elif (scoreType == self.ECONOMY_SCORE):
		return gc.getPlayer(iPlayer).getEconomyHistory(iTurn)
	    elif (scoreType == self.INDUSTRY_SCORE):
		return gc.getPlayer(iPlayer).getIndustryHistory(iTurn)
	    elif (scoreType == self.AGRICULTURE_SCORE):
		return gc.getPlayer(iPlayer).getAgricultureHistory(iTurn)
	    elif (scoreType == self.POWER_SCORE):
		return gc.getPlayer(iPlayer).getPowerHistory(iTurn)
	    elif (scoreType == self.CULTURE_SCORE):
		return gc.getPlayer(iPlayer).getCultureHistory(iTurn)
	    elif (scoreType == self.ESPIONAGE_SCORE):
		return gc.getPlayer(iPlayer).getEspionageHistory(iTurn)

	# Requires the cache to be built
	def getHistory(self, scoreType, iPlayer, iRelTurn):
	    return self.scoreCache[scoreType][iPlayer][iRelTurn]

	def drawGraphLines(self):
	    screen = self.getScreen()

	    if (self.xSelPt != 0 or self.ySelPt != 0):
		screen.addLineGFC(self.GRAPH_CANVAS_ID, self.GRAPH_H_LINE, 0, self.ySelPt, self.W_GRAPH, self.ySelPt, gc.getInfoTypeForString("COLOR_GREY"))
		screen.addLineGFC(self.GRAPH_CANVAS_ID, self.GRAPH_V_LINE, self.xSelPt, 0, self.xSelPt, self.H_GRAPH, gc.getInfoTypeForString("COLOR_GREY"))
	    else:
		screen.addLineGFC(self.GRAPH_CANVAS_ID, self.GRAPH_H_LINE, -1, -1, -1, -1, gc.getInfoTypeForString("COLOR_GREY"))
		screen.addLineGFC(self.GRAPH_CANVAS_ID, self.GRAPH_V_LINE, -1, -1, -1, -1, gc.getInfoTypeForString("COLOR_GREY"))


	def drawXLabel(self, screen, turn, x, just = CvUtil.FONT_CENTER_JUSTIFY):
	    screen.setLabel( self.getNextWidgetName(), ""
			   , u"<font=2>" + self.getTurnDate(turn) + u"</font>"
			   , just , x , self.Y_LABEL
			   , 0, FontTypes.TITLE_FONT
			   , WidgetTypes.WIDGET_GENERAL, -1, -1
			   )

	def drawGraph(self):

	    screen = self.getScreen()

	    self.deleteAllLines()
	    self.deleteAllWidgets(self.iNumPreDemoChartWidgets)

	    # Draw the graph widget
	    self.GRAPH_CANVAS_ID = self.getNextWidgetName()
	    screen.addDrawControl(self.GRAPH_CANVAS_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG").getPath(), self.X_GRAPH, self.Y_GRAPH, self.W_GRAPH, self.H_GRAPH, WidgetTypes.WIDGET_GENERAL, -1, -1)

	    # Compute the scores
	    self.buildScoreCache(self.iGraphTabID)

	    # Compute max score
	    max = 0
	    thisTurn    = CyGame().getGameTurn()
	    startTurn   = CyGame().getStartTurn()

	    if (self.graphZoom == 0 or self.graphEnd == 0):
		firstTurn = startTurn
	    else:
		firstTurn = self.graphEnd - self.graphZoom

	    if (self.graphEnd == 0):
		lastTurn  = thisTurn - 1 # all civs haven't neccessarily got a score for the current turn
	    else:
		lastTurn  = self.graphEnd

	    self.drawGraphLines()

	    # Draw x-labels
	    self.drawXLabel( screen, firstTurn, self.X_LEFT_LABEL,  CvUtil.FONT_LEFT_JUSTIFY  )
	    self.drawXLabel( screen, lastTurn,  self.X_RIGHT_LABEL, CvUtil.FONT_RIGHT_JUSTIFY )

	    # Don't draw anything the first turn
	    if (firstTurn >= lastTurn):
		return

	    # Compute max and min
	    max = 1
	    min = 0
	    for p in self.aiPlayersMet:
                
                if (not gc.getPlayer(p).isMinorCiv()): #Rhye
                
                    for turn in range(firstTurn,lastTurn + 1):
                        score = self.getHistory(self.iGraphTabID, p, turn - startTurn)
                        if (max < score):
                            max = score
                        if (min > score):
                            min = score

	    yFactor = (1.0 * self.H_GRAPH / (1.0 * (max - min)))
	    xFactor = (1.0 * self.W_GRAPH / (1.0 * (lastTurn - firstTurn)))

	    if (lastTurn - firstTurn > 10):
		turn = (firstTurn + lastTurn) / 2
		self.drawXLabel ( screen, turn, self.X_GRAPH + int(xFactor * (turn - firstTurn)) )
		if (lastTurn - firstTurn > 20):
		    turn = firstTurn + (lastTurn - firstTurn) / 4
		    self.drawXLabel ( screen, turn, self.X_GRAPH + int(xFactor * (turn - firstTurn)) )
		    turn = firstTurn + 3 * (lastTurn - firstTurn) / 4
		    self.drawXLabel ( screen, turn, self.X_GRAPH + int(xFactor * (turn - firstTurn)) )

	    # Draw the lines
	    for p in self.aiPlayersMet:

                if (not gc.getPlayer(p).isMinorCiv()): #Rhye

                    color = gc.getPlayerColorInfo(gc.getPlayer(p).getPlayerColor()).getColorTypePrimary()
                    oldX = -1
                    oldY = self.H_GRAPH
                    turn = lastTurn
                    while (turn >= firstTurn):

                        score = self.getHistory(self.iGraphTabID, p, turn - startTurn)
                        y = self.H_GRAPH - int(yFactor * (score - min))
                        x = int(xFactor * (turn - firstTurn))

                        if (x < oldX):
                            if (y != self.H_GRAPH or oldY != self.H_GRAPH): # don't draw if score is constant zero
                                self.drawLine(screen, self.GRAPH_CANVAS_ID, oldX, oldY, x, y, color)
                            oldX = x
                            oldY = y
                        elif (oldX == -1):
                            oldX = x
                            oldY = y

                        turn -= 1

	    return

	def drawLegend(self):
	    screen = self.getScreen()

	    yLine = self.Y_LEGEND_LINE
	    yText = self.Y_LEGEND + self.Y_LEGEND_TEXT

	    for p in self.aiPlayersMet:

                if (not gc.getPlayer(p).isMinorCiv()): #Rhye

                        lineColor = gc.getPlayerColorInfo(gc.getPlayer(p).getPlayerColor()).getColorTypePrimary()
                        textColorR = gc.getPlayer(p).getPlayerTextColorR()
                        textColorG = gc.getPlayer(p).getPlayerTextColorG()
                        textColorB = gc.getPlayer(p).getPlayerTextColorB()
                        textColorA = gc.getPlayer(p).getPlayerTextColorA()
                        #Rhye - start
                        #name = gc.getPlayer(p).getName()
                        name = gc.getPlayer(p).getCivilizationShortDescription(0)
                        #Rhye - end

                        str = u"<color=%d,%d,%d,%d>%s</color>" %(textColorR,textColorG,textColorB,textColorA,name)

                        self.drawLine(screen, self.LEGEND_CANVAS_ID, self.X_LEGEND_LINE, yLine, self.X_LEGEND_LINE + self.W_LEGEND_LINE, yLine, lineColor)
                        screen.setLabel( self.getNextWidgetName(), ""
                                       , u"<font=2>" + str + u"</font>"
                                       , CvUtil.FONT_LEFT_JUSTIFY
                                       , self.X_LEGEND + self.X_LEGEND_TEXT, yText
                                       , 0, FontTypes.TITLE_FONT
                                       , WidgetTypes.WIDGET_GENERAL, -1, -1
                                       )
                        yLine += self.H_LEGEND_TEXT
                        yText += self.H_LEGEND_TEXT

#############################################################################################################
################################################# DEMOGRAPHICS ##############################################
#############################################################################################################

	def drawDemographicsTab(self):

	    self.drawTextChart()
	    
	def getHappyValue(self, pPlayer):
		iHappy = pPlayer.calculateTotalCityHappiness()
		iUnhappy = pPlayer.calculateTotalCityUnhappiness()
		return (iHappy * 100) / max(1, iHappy + iUnhappy)	 

	def getHealthValue(self, pPlayer):
		iGood = pPlayer.calculateTotalCityHealthiness()
		iBad = pPlayer.calculateTotalCityUnhealthiness()
		return (iGood * 100) / max(1, iGood + iBad)	 
		
	def getRank(self, aiGroup):
		aiGroup.sort()
		aiGroup.reverse()		
		iRank = 1
		for (iLoopValue, iLoopPlayer) in aiGroup:
			if iLoopPlayer == self.iActivePlayer:
				return iRank
			iRank += 1
		return 0

	def getBest(self, aiGroup):
		bFirst = true
		iBest = 0
		for (iLoopValue, iLoopPlayer) in aiGroup:
			if iLoopPlayer != self.iActivePlayer:
				if bFirst or iLoopValue > iBest:
					iBest = iLoopValue
					bFirst = false
		return iBest

	def getWorst(self, aiGroup):
		bFirst = true
		iWorst = 0
		for (iLoopValue, iLoopPlayer) in aiGroup:
			if iLoopPlayer != self.iActivePlayer:
				if bFirst or iLoopValue < iWorst:
					iWorst = iLoopValue
					bFirst = false
		return iWorst

	def drawTextChart(self):

		######## DATA ########

		iNumActivePlayers = 0

		pPlayer = gc.getPlayer(self.iActivePlayer)

		iEconomyGameAverage = 0
		iIndustryGameAverage = 0
		iAgricultureGameAverage = 0
		iMilitaryGameAverage = 0
		iLandAreaGameAverage = 0
		iPopulationGameAverage = 0
		iHappinessGameAverage = 0
		iHealthGameAverage = 0
		iNetTradeGameAverage = 0

		# Lists of Player values - will be used to determine rank, strength and average per city
		aiGroupEconomy = []
		aiGroupIndustry = []
		aiGroupAgriculture = []
		aiGroupMilitary = []
		aiGroupLandArea = []
		aiGroupPopulation = []
		aiGroupHappiness = []
		aiGroupHealth = []
		aiGroupNetTrade = []

		# Loop through all players to determine Rank and relative Strength
		#for iPlayerLoop in range(gc.getMAX_PLAYERS()): #Rhye
                for iPlayerLoop in range(con.iNumMajorPlayers): #Rhye

			#if (gc.getPlayer(iPlayerLoop).isAlive() and not gc.getPlayer(iPlayerLoop).isBarbarian()): #Rhye
			if (gc.getPlayer(iPlayerLoop).isAlive() and not gc.getPlayer(iPlayerLoop).isBarbarian() and not gc.getPlayer(iPlayerLoop).isMinorCiv()): #Rhye

				iNumActivePlayers += 1

				pCurrPlayer = gc.getPlayer(iPlayerLoop)
				
				iValue = pCurrPlayer.calculateTotalCommerce()
				if iPlayerLoop == self.iActivePlayer:
					iEconomy = iValue
				else:
					iEconomyGameAverage += iValue
				aiGroupEconomy.append((iValue, iPlayerLoop))
				
				iValue = pCurrPlayer.calculateTotalYield(YieldTypes.YIELD_PRODUCTION)
				if iPlayerLoop == self.iActivePlayer:
					iIndustry = iValue
				else:
					iIndustryGameAverage += iValue
				aiGroupIndustry.append((iValue, iPlayerLoop))

				iValue = pCurrPlayer.calculateTotalYield(YieldTypes.YIELD_FOOD)
				if iPlayerLoop == self.iActivePlayer:
					iAgriculture = iValue
				else:
					iAgricultureGameAverage += iValue
				aiGroupAgriculture.append((iValue, iPlayerLoop))

				iValue = pCurrPlayer.getPower() * 1000
				if iPlayerLoop == self.iActivePlayer:
					iMilitary = iValue
				else:
					iMilitaryGameAverage += iValue
				aiGroupMilitary.append((iValue, iPlayerLoop))

				iValue = pCurrPlayer.getTotalLand() * 1000
				if iPlayerLoop == self.iActivePlayer:
					iLandArea = iValue
				else:
					iLandAreaGameAverage += iValue
				aiGroupLandArea.append((iValue, iPlayerLoop))

				iValue = pCurrPlayer.getRealPopulation()
				if iPlayerLoop == self.iActivePlayer:
					iPopulation = iValue
				else:
					iPopulationGameAverage += iValue
				aiGroupPopulation.append((iValue, iPlayerLoop))

				iValue = self.getHappyValue(pCurrPlayer)
				if iPlayerLoop == self.iActivePlayer:
					iHappiness = iValue
				else:
					iHappinessGameAverage += iValue
				aiGroupHappiness.append((iValue, iPlayerLoop))

				iValue = self.getHealthValue(pCurrPlayer)
				if iPlayerLoop == self.iActivePlayer:
					iHealth = iValue
				else:
					iHealthGameAverage += iValue
				aiGroupHealth.append((iValue, iPlayerLoop))
					
				iValue = pCurrPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE) - pCurrPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE)
				if iPlayerLoop == self.iActivePlayer:
					iNetTrade = iValue
				else:
					iNetTradeGameAverage += iValue
				aiGroupNetTrade.append((iValue, iPlayerLoop))
					
		iEconomyRank = self.getRank(aiGroupEconomy)
		iIndustryRank = self.getRank(aiGroupIndustry)
		iAgricultureRank = self.getRank(aiGroupAgriculture)
		iMilitaryRank = self.getRank(aiGroupMilitary)
		iLandAreaRank = self.getRank(aiGroupLandArea)
		iPopulationRank = self.getRank(aiGroupPopulation)
		iHappinessRank = self.getRank(aiGroupHappiness)
		iHealthRank = self.getRank(aiGroupHealth)
		iNetTradeRank = self.getRank(aiGroupNetTrade)

		iEconomyGameBest	= self.getBest(aiGroupEconomy)
		iIndustryGameBest	= self.getBest(aiGroupIndustry)
		iAgricultureGameBest	= self.getBest(aiGroupAgriculture)
		iMilitaryGameBest	= self.getBest(aiGroupMilitary)
		iLandAreaGameBest	= self.getBest(aiGroupLandArea)
		iPopulationGameBest	= self.getBest(aiGroupPopulation)
		iHappinessGameBest	= self.getBest(aiGroupHappiness)
		iHealthGameBest		= self.getBest(aiGroupHealth)
		iNetTradeGameBest	= self.getBest(aiGroupNetTrade)

		iEconomyGameWorst	= self.getWorst(aiGroupEconomy)
		iIndustryGameWorst	= self.getWorst(aiGroupIndustry)
		iAgricultureGameWorst	= self.getWorst(aiGroupAgriculture)
		iMilitaryGameWorst	= self.getWorst(aiGroupMilitary)
		iLandAreaGameWorst	= self.getWorst(aiGroupLandArea)
		iPopulationGameWorst	= self.getWorst(aiGroupPopulation)
		iHappinessGameWorst	= self.getWorst(aiGroupHappiness)
		iHealthGameWorst	= self.getWorst(aiGroupHealth)
		iNetTradeGameWorst	= self.getWorst(aiGroupNetTrade)

		iEconomyGameAverage = iEconomyGameAverage / max(1, iNumActivePlayers - 1)
		iIndustryGameAverage = iIndustryGameAverage / max(1, iNumActivePlayers - 1)
		iAgricultureGameAverage = iAgricultureGameAverage / max(1, iNumActivePlayers - 1)
		iMilitaryGameAverage = iMilitaryGameAverage / max(1, iNumActivePlayers - 1)
		iLandAreaGameAverage = iLandAreaGameAverage / max(1, iNumActivePlayers - 1)
		iPopulationGameAverage = iPopulationGameAverage / max(1, iNumActivePlayers - 1)
		iHappinessGameAverage = iHappinessGameAverage / max(1, iNumActivePlayers - 1)
		iHealthGameAverage = iHealthGameAverage / max(1, iNumActivePlayers - 1)
		iNetTradeGameAverage = iNetTradeGameAverage / max(1, iNumActivePlayers - 1)


		######## TEXT ########

		screen = self.getScreen()

		# Create Table
		szTable = self.getNextWidgetName()
		screen.addTableControlGFC(szTable, 6, self.X_CHART, self.Y_CHART, self.W_CHART, self.H_CHART, true, true, 32,32, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader(szTable, 0, self.TEXT_DEMOGRAPHICS_SMALL, 224) # Total graph width is 430
		screen.setTableColumnHeader(szTable, 1, self.TEXT_VALUE, 155)
		screen.setTableColumnHeader(szTable, 2, self.TEXT_BEST, 155)
		screen.setTableColumnHeader(szTable, 3, self.TEXT_AVERAGE, 155)
		screen.setTableColumnHeader(szTable, 4, self.TEXT_WORST, 155)
		screen.setTableColumnHeader(szTable, 5, self.TEXT_RANK, 90)

		for i in range(18 + 5): # 18 normal items + 5 lines for spacing
			screen.appendTableRow(szTable)
		iNumRows = screen.getTableNumRows(szTable)
		iRow = iNumRows - 1
		iCol = 0
		screen.setTableText(szTable, iCol, 0, self.TEXT_ECONOMY, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 1, self.TEXT_ECONOMY_MEASURE, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 3, self.TEXT_INDUSTRY, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 4, self.TEXT_INDUSTRY_MEASURE, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 6, self.TEXT_AGRICULTURE, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 7, self.TEXT_AGRICULTURE_MEASURE, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 9, self.TEXT_MILITARY, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 11, self.TEXT_LAND_AREA, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 12, self.TEXT_LAND_AREA_MEASURE, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 14, self.TEXT_POPULATION, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 16, self.TEXT_HAPPINESS, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 18, self.TEXT_HEALTH, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 19, self.TEXT_HEALTH_MEASURE, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 21, self.TEXT_IMP_EXP, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 22, self.TEXT_IMP_EXP_MEASURE, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		iCol = 1
		screen.setTableText(szTable, iCol, 0, str(iEconomy), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 3, str(iIndustry), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 6, str(iAgriculture), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 9, str(iMilitary), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 11, str(iLandArea), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 14, str(iPopulation), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 16, str(iHappiness) + self.TEXT_HAPPINESS_MEASURE, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 18, str(iHealth), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 21, str(iNetTrade), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		iCol = 2
		screen.setTableText(szTable, iCol, 0, str(iEconomyGameBest), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 3, str(iIndustryGameBest), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 6, str(iAgricultureGameBest), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 9, str(iMilitaryGameBest), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 11, str(iLandAreaGameBest), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 14, str(iPopulationGameBest), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 16, str(iHappinessGameBest) + self.TEXT_HAPPINESS_MEASURE, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 18, str(iHealthGameBest), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 21, str(iNetTradeGameBest), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		iCol = 3
		screen.setTableText(szTable, iCol, 0, str(iEconomyGameAverage), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 3, str(iIndustryGameAverage), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 6, str(iAgricultureGameAverage), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 9, str(iMilitaryGameAverage), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 11, str(iLandAreaGameAverage), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 14, str(iPopulationGameAverage), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 16, str(iHappinessGameAverage) + self.TEXT_HAPPINESS_MEASURE, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 18, str(iHealthGameAverage), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 21, str(iNetTradeGameAverage), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		iCol = 4
		screen.setTableText(szTable, iCol, 0, str(iEconomyGameWorst), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 3, str(iIndustryGameWorst), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 6, str(iAgricultureGameWorst), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 9, str(iMilitaryGameWorst), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 11, str(iLandAreaGameWorst), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 14, str(iPopulationGameWorst), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 16, str(iHappinessGameWorst) + self.TEXT_HAPPINESS_MEASURE, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 18, str(iHealthGameWorst), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 21, str(iNetTradeGameWorst), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		iCol = 5
		screen.setTableText(szTable, iCol, 0, str(iEconomyRank), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 3, str(iIndustryRank), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 6, str(iAgricultureRank), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 9, str(iMilitaryRank), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 11, str(iLandAreaRank), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 14, str(iPopulationRank), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 16, str(iHappinessRank), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 18, str(iHealthRank), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 21, str(iNetTradeRank), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		return

#############################################################################################################
################################################## TOP CITIES ###############################################
#############################################################################################################

	def drawTopCitiesTab(self):

		screen = self.getScreen()

		# Background Panes
		self.szLeftPaneWidget = self.getNextWidgetName()
		screen.addPanel( self.szLeftPaneWidget, "", "", true, true,
			self.X_LEFT_PANE, self.Y_LEFT_PANE, self.W_LEFT_PANE, self.H_LEFT_PANE, PanelStyles.PANEL_STYLE_MAIN )#PanelStyles.PANEL_STYLE_DAWNTOP )

		self.drawTopCities()
		self.drawWondersTab()

	def drawTopCities(self):

		self.calculateTopCities()
		self.determineCityData()

		screen = self.getScreen()

		self.szCityNameWidgets = []
		self.szCityDescWidgets = []
		self.szCityAnimWidgets = []

		for iWidgetLoop in range(self.iNumCities):

			szTextPanel = self.getNextWidgetName()
			screen.addPanel( szTextPanel, "", "", false, true,
				self.X_COL_1_CITIES_DESC, self.Y_ROWS_CITIES[iWidgetLoop] + self.Y_CITIES_DESC_BUFFER, self.W_CITIES_DESC, self.H_CITIES_DESC, PanelStyles.PANEL_STYLE_DAWNTOP )
			self.szCityNameWidgets.append(self.getNextWidgetName())
#			szProjectDesc = u"<font=3b>" + pProjectInfo.getDescription().upper() + u"</font>"
			szCityDesc = u"<font=4b>" + str(self.iCitySizes[iWidgetLoop]) + u"</font>" + " - " + u"<font=3b>" + self.szCityNames[iWidgetLoop] + u"</font>" + "\n"
			szCityDesc += self.szCityDescs[iWidgetLoop]
			screen.addMultilineText(self.szCityNameWidgets[iWidgetLoop], szCityDesc,
				self.X_COL_1_CITIES_DESC + 6, self.Y_ROWS_CITIES[iWidgetLoop] + self.Y_CITIES_DESC_BUFFER + 3, self.W_CITIES_DESC - 6, self.H_CITIES_DESC - 6, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
#			screen.attachMultilineText( szTextPanel, self.szCityNameWidgets[iWidgetLoop], str(self.iCitySizes[iWidgetLoop]) + " - " + self.szCityNames[iWidgetLoop] + "\n" + self.szCityDescs[iWidgetLoop], WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

			iCityX = self.aaCitiesXY[iWidgetLoop][0]
			iCityY = self.aaCitiesXY[iWidgetLoop][1]
			pPlot = CyMap().plot(iCityX, iCityY)
			pCity = pPlot.getPlotCity()

			iDistance = 200 + (pCity.getPopulation() * 5)
			if (iDistance > 350):
				iDistance = 350

			self.szCityAnimWidgets.append(self.getNextWidgetName())
			
			if (pCity.isRevealed(gc.getGame().getActiveTeam(), false)):			
				screen.addPlotGraphicGFC(self.szCityAnimWidgets[iWidgetLoop], self.X_CITY_ANIMATION, self.Y_ROWS_CITIES[iWidgetLoop] + self.Y_CITY_ANIMATION_BUFFER - self.H_CITY_ANIMATION / 2, self.W_CITY_ANIMATION, self.H_CITY_ANIMATION, pPlot, iDistance, false, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Draw Wonder icons
		self.drawCityWonderIcons();

		return

	def drawCityWonderIcons(self):

		screen = self.getScreen()

		aaiTopCitiesWonders = []
		aiTopCitiesNumWonders = []
		for i in range(self.iNumCities):
			aaiTopCitiesWonders.append(0)
			aiTopCitiesNumWonders.append(0)

		# Loop through top cities and determine if they have any wonders to display
		for iCityLoop in range(self.iNumCities):

			if (self.pCityPointers[iCityLoop]):

				pCity = self.pCityPointers[iCityLoop]

				aiTempWondersList = []

				# Loop through buildings

				for iBuildingLoop in range(gc.getNumBuildingInfos()):

					pBuilding = gc.getBuildingInfo(iBuildingLoop)

					# If this building is a wonder...
					if (isWorldWonderClass(gc.getBuildingInfo(iBuildingLoop).getBuildingClassType())):

						if (pCity.getNumBuilding(iBuildingLoop) > 0):

							aiTempWondersList.append(iBuildingLoop)
							aiTopCitiesNumWonders[iCityLoop] += 1

				aaiTopCitiesWonders[iCityLoop] = aiTempWondersList

		# Create Scrollable areas under each city
		self.szCityWonderScrollArea = []
		for iCityLoop in range (self.iNumCities):

			self.szCityWonderScrollArea.append(self.getNextWidgetName())

			#iScollAreaY = (self.Y_CITIES_BUFFER * iCityLoop) + 90 + self.Y_CITIES_WONDER_BUFFER

			szIconPanel = self.szCityWonderScrollArea[iCityLoop]
			screen.addPanel( szIconPanel, "", "", false, true,
				self.X_COL_1_CITIES_DESC, self.Y_ROWS_CITIES[iCityLoop] + self.Y_CITIES_WONDER_BUFFER + self.Y_CITIES_DESC_BUFFER, self.W_CITIES_DESC, self.H_CITIES_DESC, PanelStyles.PANEL_STYLE_DAWNTOP )

			# Now place the wonder buttons
			for iWonderLoop in range(aiTopCitiesNumWonders[iCityLoop]):

				iBuildingID = aaiTopCitiesWonders[iCityLoop][iWonderLoop]
				screen.attachImageButton( szIconPanel, "", gc.getBuildingInfo(iBuildingID).getButton(),
				    GenericButtonSizes.BUTTON_SIZE_46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuildingID, -1, False )

	def calculateTopCities(self):

		# Calculate the top 5 cities

		for iPlayerLoop in range(gc.getMAX_PLAYERS()):

			apCityList = PyPlayer(iPlayerLoop).getCityList()
			
			for pCity in apCityList:
			
				iTotalCityValue = ((pCity.getCulture() / 5) + (pCity.getFoodRate() + pCity.getProductionRate() \
					+ pCity.calculateGoldRate())) * pCity.getPopulation()

				for iRankLoop in range(5):

					if (iTotalCityValue > self.iCityValues[iRankLoop] and not pCity.isBarbarian()):

						self.addCityToList(iRankLoop, pCity, iTotalCityValue)

						break

	# Recursive
	def addCityToList(self, iRank, pCity, iTotalCityValue):

		if (iRank > 4):

			return

		else:
			pTempCity = self.pCityPointers[iRank]

			# Verify a city actually exists at this rank
			if (pTempCity):

				iTempCityValue = self.iCityValues[iRank]

				self.addCityToList(iRank+1, pTempCity, iTempCityValue)

				self.pCityPointers[iRank] = pCity
				self.iCityValues[iRank] = iTotalCityValue

			else:
				self.pCityPointers[iRank] = pCity
				self.iCityValues[iRank] = iTotalCityValue

				return

	def determineCityData(self):

		self.iNumCities = 0

		for iRankLoop in range(5):

			pCity = self.pCityPointers[iRankLoop]

			# If this city exists and has data we can use
			if (pCity):

				pPlayer = gc.getPlayer(pCity.getOwner())

				iTurnYear = CyGame().getTurnYear(pCity.getGameTurnFounded())


                                #Rhye - start
##				if (iTurnYear < 0):
##					szTurnFounded = localText.getText("TXT_KEY_TIME_BC", (-iTurnYear,))#"%d %s" %(-iTurnYear, self.TEXT_BC)
##				else:
##					szTurnFounded = localText.getText("TXT_KEY_TIME_AD", (iTurnYear,))#"%d %s" %(iTurnYear, self.TEXT_AD)

                                iActivePlayer = CyGame().getActivePlayer()
                                pActivePlayer = gc.getPlayer(iActivePlayer)
                                tActivePlayer = gc.getTeam(pActivePlayer.getTeam())
                                iBronzeWorking = 61
                                iIronWorking = 63
                                iCalendar = 33
                                
                                if (tActivePlayer.isHasTech(iCalendar)):
                                        if (iTurnYear < 0):
                                            szTurnFounded = localText.getText("TXT_KEY_TIME_BC", (-iTurnYear,))
                                        else:
                                            szTurnFounded = localText.getText("TXT_KEY_TIME_AD", (iTurnYear,))
                                elif (iTurnYear >= 1500):
                                        szTurnFounded = localText.getText("TXT_KEY_AGE_RENAISSANCE", ())              
                                elif (iTurnYear >= 450):
                                        szTurnFounded = localText.getText("TXT_KEY_AGE_MEDIEVAL", ())    
                                elif (iTurnYear >= -800):
                                        szTurnFounded = localText.getText("TXT_KEY_AGE_IRON", ())    
                                elif (iTurnYear >= -2000):
                                        szTurnFounded = localText.getText("TXT_KEY_AGE_BRONZE", ())    
                                else:
                                        szTurnFounded = localText.getText("TXT_KEY_AGE_STONE", ())
                                #Rhye - end
  

				if (pCity.isRevealed(gc.getGame().getActiveTeam()) or gc.getTeam(pPlayer.getTeam()).isHasMet(gc.getGame().getActiveTeam())):
					self.szCityNames[iRankLoop] = pCity.getName().upper()
					self.szCityDescs[iRankLoop] = ("%s, %s" %(pPlayer.getCivilizationAdjective(0), localText.getText("TXT_KEY_MISC_FOUNDED_IN", (szTurnFounded,))))
				else:
					self.szCityNames[iRankLoop] = localText.getText("TXT_KEY_UNKNOWN", ()).upper()
					self.szCityDescs[iRankLoop] = ("%s" %(localText.getText("TXT_KEY_MISC_FOUNDED_IN", (szTurnFounded,)), ))
				self.iCitySizes[iRankLoop] = pCity.getPopulation()
				self.aaCitiesXY[iRankLoop] = [pCity.getX(), pCity.getY()]

				self.iNumCities += 1
			else:

				self.szCityNames[iRankLoop] = ""
				self.iCitySizes[iRankLoop] = -1
				self.szCityDescs[iRankLoop] = ""
				self.aaCitiesXY[iRankLoop] = [-1, -1]

		return

#############################################################################################################
################################################### WONDERS #################################################
#############################################################################################################

	def drawWondersTab(self):

		screen = self.getScreen()

		self.szRightPaneWidget = self.getNextWidgetName()
		screen.addPanel( self.szRightPaneWidget, "", "", true, true,
			self.X_RIGHT_PANE, self.Y_RIGHT_PANE, self.W_RIGHT_PANE, self.H_RIGHT_PANE, PanelStyles.PANEL_STYLE_MAIN )#PanelStyles.PANEL_STYLE_DAWNTOP )

		self.drawWondersDropdownBox()
		self.calculateWondersList()
		self.drawWondersList()

	def drawWondersDropdownBox(self):
		"Draws the Wonders Dropdown Box"

		screen = self.getScreen()

		######################### Dropdown Box Widget #########################################

		self.szWondersDropdownWidget = self.getNextWidgetName()

		screen.addDropDownBoxGFC(self.szWondersDropdownWidget,
		    self.X_DROPDOWN, self.Y_DROPDOWN, self.W_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)

		if (self.szWonderDisplayMode == "World Wonders"):
			bDefault = true
		else:
			bDefault = false
		screen.addPullDownString(self.szWondersDropdownWidget, localText.getText("TXT_KEY_TOP_CITIES_SCREEN_WORLD_WONDERS", ()), 0, 0, bDefault )

		if (self.szWonderDisplayMode == "National Wonders"):
			bDefault = true
		else:
			bDefault = false
		screen.addPullDownString(self.szWondersDropdownWidget, localText.getText("TXT_KEY_TOP_CITIES_SCREEN_NATIONAL_WONDERS", ()), 1, 1, bDefault )

		if (self.szWonderDisplayMode == "Projects"):
			bDefault = true
		else:
			bDefault = false
		screen.addPullDownString(self.szWondersDropdownWidget, localText.getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()), 2, 2, bDefault )

		return

	def determineListBoxContents(self):

		screen = self.getScreen()

		# Fill wonders listbox

		iNumWondersBeingBuilt = len(self.aaWondersBeingBuilt)

		szWonderName = ""
		self.aiWonderListBoxIDs = []
		self.aiTurnYearBuilt = []
		self.aiWonderBuiltBy = []
		self.aszWonderCity = []

		if (self.szWonderDisplayMode == "Projects"):

	############### Create ListBox for Projects ###############

			for iWonderLoop in range(iNumWondersBeingBuilt):

				iProjectType = self.aaWondersBeingBuilt[iWonderLoop][0]
				pProjectInfo = gc.getProjectInfo(iProjectType)
				szProjectName = pProjectInfo.getDescription()

				self.aiWonderListBoxIDs.append(iProjectType)
				self.aiTurnYearBuilt.append(-6666)
				szWonderBuiltBy = self.aaWondersBeingBuilt[iWonderLoop][1]
				self.aiWonderBuiltBy.append(szWonderBuiltBy)
				szWonderCity = ""
				self.aszWonderCity.append(szWonderCity)

				screen.appendListBoxString( self.szWondersListBox, szProjectName + " (" + szWonderBuiltBy + ")", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

			for iWonderLoop in range(self.iNumWonders):

				iProjectType = self.aaWondersBuilt[iWonderLoop][1]
				pProjectInfo = gc.getProjectInfo(iProjectType)
				szProjectName = pProjectInfo.getDescription()

				self.aiWonderListBoxIDs.append(iProjectType)
				self.aiTurnYearBuilt.append(-9999)
				szWonderBuiltBy = self.aaWondersBuilt[iWonderLoop][2]
				self.aiWonderBuiltBy.append(szWonderBuiltBy)
				szWonderCity = self.aaWondersBuilt[iWonderLoop][3]
				self.aszWonderCity.append(szWonderCity)

				screen.appendListBoxString( self.szWondersListBox, szProjectName + " (" + szWonderBuiltBy + ")", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		else:

	############### Create ListBox for Wonders ###############

			for iWonderLoop in range(iNumWondersBeingBuilt):

				iWonderType = self.aaWondersBeingBuilt[iWonderLoop][0]
				pWonderInfo = gc.getBuildingInfo(iWonderType)
				szWonderName = pWonderInfo.getDescription()

				self.aiWonderListBoxIDs.append(iWonderType)
				self.aiTurnYearBuilt.append(-9999)
				szWonderBuiltBy = self.aaWondersBeingBuilt[iWonderLoop][1]
				self.aiWonderBuiltBy.append(szWonderBuiltBy)
				szWonderCity = ""
				self.aszWonderCity.append(szWonderCity)

				screen.appendListBoxString( self.szWondersListBox, szWonderName + " (" + szWonderBuiltBy + ")", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

			for iWonderLoop in range(self.iNumWonders):

				iWonderType = self.aaWondersBuilt[iWonderLoop][1]
				pWonderInfo = gc.getBuildingInfo(iWonderType)
				szWonderName = pWonderInfo.getDescription()

				self.aiWonderListBoxIDs.append(iWonderType)
				self.aiTurnYearBuilt.append(self.aaWondersBuilt[iWonderLoop][0])
				szWonderBuiltBy = self.aaWondersBuilt[iWonderLoop][2]
				self.aiWonderBuiltBy.append(szWonderBuiltBy)
				szWonderCity = self.aaWondersBuilt[iWonderLoop][3]
				self.aszWonderCity.append(szWonderCity)

				screen.appendListBoxString( self.szWondersListBox, szWonderName + " (" + szWonderBuiltBy + ")", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

	def drawWondersList(self):

		screen = self.getScreen()

		if (self.iNumWondersPermanentWidgets == 0):

			# Wonders List ListBox
			self.szWondersListBox = self.getNextWidgetName()
			screen.addListBoxGFC(self.szWondersListBox, "",
			    self.X_WONDER_LIST, self.Y_WONDER_LIST, self.W_WONDER_LIST, self.H_WONDER_LIST, TableStyles.TABLE_STYLE_STANDARD )
			screen.setStyle(self.szWondersListBox, "Table_StandardCiv_Style")

			self.determineListBoxContents()

			self.iNumWondersPermanentWidgets = self.nWidgetCount

		# Stats Panel
		panelName = self.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
				 self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, PanelStyles.PANEL_STYLE_IN )

############################################### DISPLAY SINGLE WONDER ###############################################

		# Set default wonder if any exist in this list
		if (len(self.aiWonderListBoxIDs) > 0 and self.iWonderID == -1):
			self.iWonderID = self.aiWonderListBoxIDs[0]

		# Only display/do the following if a wonder is actively being displayed
		if (self.iWonderID > -1):

############################################### DISPLAY PROJECT MODE ###############################################

			if (self.szWonderDisplayMode == "Projects"):

				pProjectInfo = gc.getProjectInfo(self.iWonderID)

				# Stats panel (cont'd) - Name
				szProjectDesc = u"<font=3b>" + pProjectInfo.getDescription().upper() + u"</font>"
				szStatsText = szProjectDesc + "\n\n"

				# Say whether this project is built yet or not

				iTurnYear = self.aiTurnYearBuilt[self.iActiveWonderCounter]
				if (iTurnYear == -6666):	# -6666 used for wonders in progress
					szTempText = localText.getText("TXT_KEY_BEING_BUILT", ())

				else:
					szTempText = localText.getText("TXT_KEY_INFO_SCREEN_BUILT", ())

				szWonderDesc = "%s, %s" %(self.aiWonderBuiltBy[self.iActiveWonderCounter], szTempText)
				szStatsText += szWonderDesc + "\n"
				
				if (self.aszWonderCity[self.iActiveWonderCounter] != ""):
					szStatsText += self.aszWonderCity[self.iActiveWonderCounter] + "\n\n"
				else:
					szStatsText += "\n"

				if (pProjectInfo.getProductionCost() > 0):
					szCost = localText.getText("TXT_KEY_PEDIA_COST", (gc.getActivePlayer().getProjectProductionNeeded(self.iWonderID),))
					szStatsText += szCost.upper() + (u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()) + "\n"

				if (isWorldProject(self.iWonderID)):
					iMaxInstances = gc.getProjectInfo(self.iWonderID).getMaxGlobalInstances()
					szProjectType = localText.getText("TXT_KEY_PEDIA_WORLD_PROJECT", ())
					if (iMaxInstances > 1):
						szProjectType += " " + localText.getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
					szStatsText += szProjectType.upper() + "\n"

				if (isTeamProject(self.iWonderID)):
					iMaxInstances = gc.getProjectInfo(self.iWonderID).getMaxTeamInstances()
					szProjectType = localText.getText("TXT_KEY_PEDIA_TEAM_PROJECT", ())
					if (iMaxInstances > 1):
						szProjectType += " " + localText.getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
					szStatsText += szProjectType.upper()

				screen.addMultilineText(self.getNextWidgetName(), szStatsText, self.X_STATS_PANE + 5, self.Y_STATS_PANE + 15, self.W_STATS_PANE - 10, self.H_STATS_PANE - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

				# Add Graphic
				iIconX = self.X_PROJECT_ICON - self.W_PROJECT_ICON / 2
				iIconY = self.Y_PROJECT_ICON - self.W_PROJECT_ICON / 2

				screen.addDDSGFC(self.getNextWidgetName(), gc.getProjectInfo(self.iWonderID).getButton(),
						 iIconX, iIconY, self.W_PROJECT_ICON, self.W_PROJECT_ICON, WidgetTypes.WIDGET_GENERAL, -1, -1 )

				# Special Abilities ListBox

				szSpecialTitle = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()) + u"</font>"
				self.szSpecialTitleWidget = self.getNextWidgetName()
				screen.setText(self.szSpecialTitleWidget, "", szSpecialTitle, CvUtil.FONT_LEFT_JUSTIFY, self.X_SPECIAL_TITLE, self.Y_SPECIAL_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				panelName = self.getNextWidgetName()
				screen.addPanel( panelName, "", "", true, true,
						 self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_IN)

				listName = self.getNextWidgetName()
				screen.attachListBoxGFC( panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY )
				screen.enableSelect(listName, False)

				szSpecialText = CyGameTextMgr().getProjectHelp(self.iWonderID, True, None)
				splitText = string.split( szSpecialText, "\n" )
				for special in splitText:
					if len( special ) != 0:
						screen.appendListBoxString( listName, special, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

			else:

	############################################### DISPLAY WONDER MODE ###############################################

				pWonderInfo = gc.getBuildingInfo(self.iWonderID)

				# Stats panel (cont'd) - Name
				szWonderDesc = u"<font=3b>" + gc.getBuildingInfo(self.iWonderID).getDescription().upper() + u"</font>"
				szStatsText = szWonderDesc + "\n\n"

				# Wonder built-in year
				iTurnYear = self.aiTurnYearBuilt[self.iActiveWonderCounter]#self.aaWondersBuilt[self.iActiveWonderCounter][0]#.append([0,iProjectLoop,""]

				szDateBuilt = ""

				if (iTurnYear != -9999):	# -9999 used for wonders in progress
                                        #Rhye - start

##					if (iTurnYear < 0):
##						szTurnFounded = localText.getText("TXT_KEY_TIME_BC", (-iTurnYear,))
##					else:
##						szTurnFounded = localText.getText("TXT_KEY_TIME_AD", (iTurnYear,))
##
##					szDateBuilt = (", %s" %(szTurnFounded))
					
                                        iActivePlayer = CyGame().getActivePlayer()
                                        pActivePlayer = gc.getPlayer(iActivePlayer)
                                        tActivePlayer = gc.getTeam(pActivePlayer.getTeam())
                                        iCalendar = 33
                                        
                                        if (tActivePlayer.isHasTech(iCalendar)):
                                                if (iTurnYear < 0):
                                                    szTurnFounded = localText.getText("TXT_KEY_TIME_BC", (-iTurnYear,))
                                                else:
                                                    szTurnFounded = localText.getText("TXT_KEY_TIME_AD", (iTurnYear,))
                                                
                                        elif (iTurnYear >= 1500):
                                                szTurnFounded = localText.getText("TXT_KEY_AGE_RENAISSANCE", ())              
                                        elif (iTurnYear >= 450):
                                                szTurnFounded = localText.getText("TXT_KEY_AGE_MEDIEVAL", ())    
                                        elif (iTurnYear >= -800):
                                                szTurnFounded = localText.getText("TXT_KEY_AGE_IRON", ())    
                                        elif (iTurnYear >= -2000):
                                                szTurnFounded = localText.getText("TXT_KEY_AGE_BRONZE", ())    
                                        else:
                                                szTurnFounded = localText.getText("TXT_KEY_AGE_STONE", ())

                                        szDateBuilt = (", %s" %(szTurnFounded))
                                        #Rhye - end



				else:
					szDateBuilt = (", %s" %(localText.getText("TXT_KEY_BEING_BUILT", ())))

				szWonderDesc = "%s%s" %(self.aiWonderBuiltBy[self.iActiveWonderCounter], szDateBuilt)
				szStatsText += szWonderDesc + "\n"
				
				if (self.aszWonderCity[self.iActiveWonderCounter] != ""):
					szStatsText += self.aszWonderCity[self.iActiveWonderCounter] + "\n\n"
				else:
					szStatsText += "\n"

				# Building attributes

				if (pWonderInfo.getProductionCost() > 0):
					szCost = localText.getText("TXT_KEY_PEDIA_COST", (gc.getActivePlayer().getBuildingProductionNeeded(self.iWonderID),))
					szStatsText += szCost.upper() + (u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()) + "\n"

				for k in range(CommerceTypes.NUM_COMMERCE_TYPES):
					if (pWonderInfo.getObsoleteSafeCommerceChange(k) != 0):
						if (pWonderInfo.getObsoleteSafeCommerceChange(k) > 0):
							szSign = "+"
						else:
							szSign = ""

						szCommerce = gc.getCommerceInfo(k).getDescription() + ": "

						szText1 = szCommerce.upper() + szSign + str(pWonderInfo.getObsoleteSafeCommerceChange(k))
						szText2 = szText1 + (u"%c" % (gc.getCommerceInfo(k).getChar()))
						szStatsText += szText2 + "\n"

				if (pWonderInfo.getHappiness() > 0):
					szText = localText.getText("TXT_KEY_PEDIA_HAPPY", (pWonderInfo.getHappiness(),))
					szStatsText += szText + (u"%c" % CyGame().getSymbolID(FontSymbols.HAPPY_CHAR)) + "\n"

				elif (pWonderInfo.getHappiness() < 0):
					szText = localText.getText("TXT_KEY_PEDIA_UNHAPPY", (-pWonderInfo.getHappiness(),))
					szStatsText += szText + (u"%c" % CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR)) + "\n"

				if (pWonderInfo.getHealth() > 0):
					szText = localText.getText("TXT_KEY_PEDIA_HEALTHY", (pWonderInfo.getHealth(),))
					szStatsText += szText + (u"%c" % CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR)) + "\n"

				elif (pWonderInfo.getHealth() < 0):
					szText = localText.getText("TXT_KEY_PEDIA_UNHEALTHY", (-pWonderInfo.getHealth(),))
					szStatsText += szText + (u"%c" % CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR)) + "\n"

				if (pWonderInfo.getGreatPeopleRateChange() != 0):
					szText = localText.getText("TXT_KEY_PEDIA_GREAT_PEOPLE", (pWonderInfo.getGreatPeopleRateChange(),))
					szStatsText += szText + (u"%c" % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR)) + "\n"

				screen.addMultilineText(self.getNextWidgetName(), szStatsText, self.X_STATS_PANE + 5, self.Y_STATS_PANE + 15, self.W_STATS_PANE - 10, self.H_STATS_PANE - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

				# Add Graphic
				screen.addBuildingGraphicGFC(self.getNextWidgetName(), self.iWonderID,
				    self.X_WONDER_GRAPHIC, self.Y_WONDER_GRAPHIC, self.W_WONDER_GRAPHIC, self.H_WONDER_GRAPHIC,
				    WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_WONDER_ANIMATION, self.Z_ROTATION_WONDER_ANIMATION, self.SCALE_ANIMATION, True)

				# Special Abilities ListBox

				szSpecialTitle = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()) + u"</font>"
				self.szSpecialTitleWidget = self.getNextWidgetName()
				screen.setText(self.szSpecialTitleWidget, "", szSpecialTitle, CvUtil.FONT_LEFT_JUSTIFY, self.X_SPECIAL_TITLE, self.Y_SPECIAL_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				panelName = self.getNextWidgetName()
				screen.addPanel( panelName, "", "", true, true,#localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ())
						 self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_IN)

				listName = self.getNextWidgetName()
				screen.attachListBoxGFC( panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY )
				screen.enableSelect(listName, False)

				szSpecialText = CyGameTextMgr().getBuildingHelp(self.iWonderID, True, False, False, None)
				splitText = string.split( szSpecialText, "\n" )
				for special in splitText:
					if len( special ) != 0:
						screen.appendListBoxString( listName, special, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

	def calculateWondersList(self):

		self.aaWondersBeingBuilt = []
		self.aaWondersBuilt = []
		self.iNumWonders = 0

		self.pActivePlayer = gc.getPlayer(CyGame().getActivePlayer())

		# Loop through players to determine Wonders
		for iPlayerLoop in range(gc.getMAX_PLAYERS()):

			pPlayer = gc.getPlayer(iPlayerLoop)
			iPlayerTeam = pPlayer.getTeam()

			# No barbs and only display national wonders for the active player's team
 			if (pPlayer and not pPlayer.isBarbarian() and ((self.szWonderDisplayMode != "National Wonders") or (iPlayerTeam == gc.getTeam(gc.getPlayer(self.iActivePlayer).getTeam()).getID()))):

				# Loop through this player's cities and determine if they have any wonders to display
				apCityList = PyPlayer(iPlayerLoop).getCityList()
				for pCity in apCityList:

					pCityPlot = CyMap().plot(pCity.getX(), pCity.getY())
					
					# Check to see if active player can see this city
					szCityName = ""
					if (pCityPlot.isActiveVisible(false)):
						szCityName = pCity.getName()
					
					# Loop through projects to find any under construction
					if (self.szWonderDisplayMode == "Projects"):
						for iProjectLoop in range(gc.getNumProjectInfos()):

							iProjectProd = pCity.getProductionProject()
							pProject = gc.getProjectInfo(iProjectLoop)

							# Project is being constructed
							if (iProjectProd == iProjectLoop):

								# Project Mode
								if (iPlayerTeam == gc.getTeam(gc.getPlayer(self.iActivePlayer).getTeam()).getID()):

									self.aaWondersBeingBuilt.append([iProjectProd, pPlayer.getCivilizationShortDescription(0)])

					# Loop through buildings
					else:

						for iBuildingLoop in range(gc.getNumBuildingInfos()):

							iBuildingProd = pCity.getProductionBuilding()

							pBuilding = gc.getBuildingInfo(iBuildingLoop)

							# World Wonder Mode
							if (self.szWonderDisplayMode == "World Wonders" and isWorldWonderClass(gc.getBuildingInfo(iBuildingLoop).getBuildingClassType())):

								# Is this city building a wonder?
								if (iBuildingProd == iBuildingLoop):

									# Only show our wonders under construction
									if (iPlayerTeam == gc.getPlayer(self.iActivePlayer).getTeam()):

										self.aaWondersBeingBuilt.append([iBuildingProd, pPlayer.getCivilizationShortDescription(0)])

								if (pCity.getNumBuilding(iBuildingLoop) > 0):
									if (iPlayerTeam == gc.getPlayer(self.iActivePlayer).getTeam() or gc.getTeam(gc.getPlayer(self.iActivePlayer).getTeam()).isHasMet(iPlayerTeam)):								
										self.aaWondersBuilt.append([pCity.getBuildingOriginalTime(iBuildingLoop),iBuildingLoop,pPlayer.getCivilizationShortDescription(0),szCityName])
									else:
										self.aaWondersBuilt.append([pCity.getBuildingOriginalTime(iBuildingLoop),iBuildingLoop,localText.getText("TXT_KEY_UNKNOWN", ()),localText.getText("TXT_KEY_UNKNOWN", ())])
	#								print("Adding World wonder to list: %s, %d, %s" %(pCity.getBuildingOriginalTime(iBuildingLoop),iBuildingLoop,pPlayer.getCivilizationAdjective(0)))
									self.iNumWonders += 1

							# National/Team Wonder Mode
							elif (self.szWonderDisplayMode == "National Wonders" and (isNationalWonderClass(gc.getBuildingInfo(iBuildingLoop).getBuildingClassType()) or isTeamWonderClass(gc.getBuildingInfo(iBuildingLoop).getBuildingClassType()))):

								# Is this city building a wonder?
								if (iBuildingProd == iBuildingLoop):

									# Only show our wonders under construction
									if (iPlayerTeam == gc.getPlayer(self.iActivePlayer).getTeam()):

										self.aaWondersBeingBuilt.append([iBuildingProd, pPlayer.getCivilizationShortDescription(0)])

								if (pCity.getNumBuilding(iBuildingLoop) > 0):

	#								print("Adding National wonder to list: %s, %d, %s" %(pCity.getBuildingOriginalTime(iBuildingLoop),iBuildingLoop,pPlayer.getCivilizationAdjective(0)))
									if (iPlayerTeam == gc.getPlayer(self.iActivePlayer).getTeam() or gc.getTeam(gc.getPlayer(self.iActivePlayer).getTeam()).isHasMet(iPlayerTeam)):								
										self.aaWondersBuilt.append([pCity.getBuildingOriginalTime(iBuildingLoop),iBuildingLoop,pPlayer.getCivilizationShortDescription(0), szCityName])
									else:
										self.aaWondersBuilt.append([pCity.getBuildingOriginalTime(iBuildingLoop),iBuildingLoop,localText.getText("TXT_KEY_UNKNOWN", ()), localText.getText("TXT_KEY_UNKNOWN", ())])
									self.iNumWonders += 1

		# This array used to store which players have already used up a team's slot so team projects don't get added to list more than once
		aiTeamsUsed = []

		# Project Mode
		if (self.szWonderDisplayMode == "Projects"):

			# Loop through players to determine Projects
			for iPlayerLoop in range(gc.getMAX_PLAYERS()):

				pPlayer = gc.getPlayer(iPlayerLoop)
				iTeamLoop = pPlayer.getTeam()

				# Block duplicates
				if (iTeamLoop not in aiTeamsUsed):

					aiTeamsUsed.append(iTeamLoop)
					pTeam = gc.getTeam(iTeamLoop)

					if (pTeam.isAlive() and not pTeam.isBarbarian()):

						# Loop through projects
						for iProjectLoop in range(gc.getNumProjectInfos()):

							for iI in range(pTeam.getProjectCount(iProjectLoop)):

								if (iTeamLoop == gc.getPlayer(self.iActivePlayer).getTeam() or gc.getTeam(gc.getPlayer(self.iActivePlayer).getTeam()).isHasMet(iTeamLoop)):								
									self.aaWondersBuilt.append([-9999,iProjectLoop,gc.getPlayer(iPlayerLoop).getCivilizationShortDescription(0),szCityName])
								else:
									self.aaWondersBuilt.append([-9999,iProjectLoop,localText.getText("TXT_KEY_UNKNOWN", ()),localText.getText("TXT_KEY_UNKNOWN", ())])
								self.iNumWonders += 1

		# Sort wonders in order of date built
		self.aaWondersBuilt.sort()
		self.aaWondersBuilt.reverse()

#		print("List of wonders/projects Built:")
#		print(self.aaWondersBuilt)

#############################################################################################################
################################################## STATISTICS ###############################################
#############################################################################################################

	def drawStatsTab(self):

		screen = self.getScreen()

		iNumUnits = gc.getNumUnitInfos()
		# edead: start (count GraphicalOnly units and make a dictionary that translates them into basic types)
		iNumUnitTypes = 0
		unitDict = {}
		for i in range(iNumUnits):
			if not gc.getUnitInfo(i).isGraphicalOnly():
				unitDict[i] = iNumUnitTypes
				j = iNumUnitTypes
				iNumUnitTypes += 1
			else:
				unitDict[i] = j
		# edead: end
		iNumBuildings = gc.getNumBuildingInfos()

		self.iNumUnitStatsChartCols = 5
		self.iNumBuildingStatsChartCols = 2
		self.iNumUnitStatsChartRows = iNumUnits
		self.iNumBuildingStatsChartRows = iNumBuildings

################################################### CALCULATE STATS ###################################################

		iMinutesPlayed = CyGame().getMinutesPlayed()
		iHoursPlayed = iMinutesPlayed / 60
		iMinutesPlayed = iMinutesPlayed - (iHoursPlayed * 60)

		szMinutesString = str(iMinutesPlayed)
		if (iMinutesPlayed < 10):
			szMinutesString = "0" + szMinutesString
		szHoursString = str(iHoursPlayed)
		if (iHoursPlayed < 10):
			szHoursString = "0" + szHoursString

		szTimeString = szHoursString + ":" + szMinutesString

		iNumCitiesBuilt = CyStatistics().getPlayerNumCitiesBuilt(self.iActivePlayer)

		iNumCitiesRazed = CyStatistics().getPlayerNumCitiesRazed(self.iActivePlayer)

		iNumReligionsFounded = 0
		for iReligionLoop in range(gc.getNumReligionInfos()):
			if (CyStatistics().getPlayerReligionFounded(self.iActivePlayer, iReligionLoop)):
				iNumReligionsFounded += 1

		aiUnitsBuilt = []
		for iUnitLoop in range(iNumUnits):
			aiUnitsBuilt.append(CyStatistics().getPlayerNumUnitsBuilt(self.iActivePlayer, iUnitLoop))
			if gc.getUnitInfo(iUnitLoop).isGraphicalOnly(): # edead
				aiUnitsBuilt[unitDict[iUnitLoop]] += CyStatistics().getPlayerNumUnitsBuilt(self.iActivePlayer, iUnitLoop) # edead

		aiUnitsKilled = []
		for iUnitLoop in range(iNumUnits):
			aiUnitsKilled.append(CyStatistics().getPlayerNumUnitsKilled(self.iActivePlayer, iUnitLoop))
			if gc.getUnitInfo(iUnitLoop).isGraphicalOnly(): # edead
				aiUnitsKilled[unitDict[iUnitLoop]] += CyStatistics().getPlayerNumUnitsKilled(self.iActivePlayer, iUnitLoop) # edead

		aiUnitsLost = []
		for iUnitLoop in range(iNumUnits):
			aiUnitsLost.append(CyStatistics().getPlayerNumUnitsLost(self.iActivePlayer, iUnitLoop))
			if gc.getUnitInfo(iUnitLoop).isGraphicalOnly(): # edead
				aiUnitsLost[unitDict[iUnitLoop]] += CyStatistics().getPlayerNumUnitsLost(self.iActivePlayer, iUnitLoop) # edead

		aiBuildingsBuilt = []
		for iBuildingLoop in range(iNumBuildings):
			aiBuildingsBuilt.append(CyStatistics().getPlayerNumBuildingsBuilt(self.iActivePlayer, iBuildingLoop))

		aiUnitsCurrent = []
		for iUnitLoop in range(iNumUnits):
			aiUnitsCurrent.append(0)

		apUnitList = PyPlayer(self.iActivePlayer).getUnitList()
		for pUnit in apUnitList:
			iType = pUnit.getUnitType()
			aiUnitsCurrent[iType] += 1
			if gc.getUnitInfo(iUnitLoop).isGraphicalOnly(): # edead
				aiUnitsCurrent[unitDict[iUnitLoop]] += 1 # edead

################################################### TOP PANEL ###################################################

		# Add Panel
		szTopPanelWidget = self.getNextWidgetName()
		screen.addPanel( szTopPanelWidget, u"", u"", True, False, self.X_STATS_TOP_PANEL, self.Y_STATS_TOP_PANEL, self.W_STATS_TOP_PANEL, self.H_STATS_TOP_PANEL,
				 PanelStyles.PANEL_STYLE_DAWNTOP )

		# Leaderhead graphic
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		szLeaderWidget = self.getNextWidgetName()
		screen.addLeaderheadGFC(szLeaderWidget, player.getLeaderType(), AttitudeTypes.ATTITUDE_PLEASED,
			self.X_LEADER_ICON, self.Y_LEADER_ICON, self.W_LEADER_ICON, self.H_LEADER_ICON, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Leader Name
		self.szLeaderNameWidget = self.getNextWidgetName()
		szText = u"<font=4b>" + gc.getPlayer(self.iActivePlayer).getName() + u"</font>"
		screen.setText(self.szLeaderNameWidget, "", szText, CvUtil.FONT_LEFT_JUSTIFY,
			       self.X_LEADER_NAME, self.Y_LEADER_NAME, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Create Table
		szTopChart = self.getNextWidgetName()
		screen.addTableControlGFC(szTopChart, self.iNumTopChartCols, self.X_STATS_TOP_CHART, self.Y_STATS_TOP_CHART, self.W_STATS_TOP_CHART, self.H_STATS_TOP_CHART,
					  False, True, 32,32, TableStyles.TABLE_STYLE_STANDARD)

		# Add Columns
		screen.setTableColumnHeader(szTopChart, 0, "", self.STATS_TOP_CHART_W_COL_0)
		screen.setTableColumnHeader(szTopChart, 1, "", self.STATS_TOP_CHART_W_COL_1)

		# Add Rows
		for i in range(self.iNumTopChartRows - 1):
			screen.appendTableRow(szTopChart)
		iNumRows = screen.getTableNumRows(szTopChart)

		# Graph itself
		iRow = 0
		iCol = 0
		screen.setTableText(szTopChart, iCol, iRow, self.TEXT_TIME_PLAYED, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		iCol = 1
		screen.setTableText(szTopChart, iCol, iRow, szTimeString, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		iRow = 1
		iCol = 0
		screen.setTableText(szTopChart, iCol, iRow, self.TEXT_CITIES_BUILT, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		iCol = 1
		screen.setTableText(szTopChart, iCol, iRow, str(iNumCitiesBuilt), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		iRow = 2
		iCol = 0
		screen.setTableText(szTopChart, iCol, iRow, self.TEXT_CITIES_RAZED, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		iCol = 1
		screen.setTableText(szTopChart, iCol, iRow, str(iNumCitiesRazed), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		iRow = 3
		iCol = 0
		screen.setTableText(szTopChart, iCol, iRow, self.TEXT_NUM_RELIGIONS_FOUNDED, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		iCol = 1
		screen.setTableText(szTopChart, iCol, iRow, str(iNumReligionsFounded), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

################################################### BOTTOM PANEL ###################################################

		# Create Tables
		szUnitsTable = self.getNextWidgetName()
		screen.addTableControlGFC(szUnitsTable, self.iNumUnitStatsChartCols, self.X_STATS_BOTTOM_CHART, self.Y_STATS_BOTTOM_CHART, self.W_STATS_BOTTOM_CHART_UNITS, self.H_STATS_BOTTOM_CHART,
					  True, True, 32,32, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSort(szUnitsTable)

		szBuildingsTable = self.getNextWidgetName()
		screen.addTableControlGFC(szBuildingsTable, self.iNumBuildingStatsChartCols, self.X_STATS_BOTTOM_CHART + self.W_STATS_BOTTOM_CHART_UNITS, self.Y_STATS_BOTTOM_CHART, self.W_STATS_BOTTOM_CHART_BUILDINGS, self.H_STATS_BOTTOM_CHART,
					  True, True, 32,32, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSort(szBuildingsTable)

		
		# Reducing the width a bit to leave room for the vertical scrollbar, preventing a horizontal scrollbar from also being created
		iChartWidth = self.W_STATS_BOTTOM_CHART_UNITS + self.W_STATS_BOTTOM_CHART_BUILDINGS - 24
		
		# Add Columns
		iColWidth = int((iChartWidth / 12 * 3))
		screen.setTableColumnHeader(szUnitsTable, 0, self.TEXT_UNITS, iColWidth)
		iColWidth = int((iChartWidth / 12 * 1))
		screen.setTableColumnHeader(szUnitsTable, 1, self.TEXT_CURRENT, iColWidth)
		iColWidth = int((iChartWidth / 12 * 1))
		screen.setTableColumnHeader(szUnitsTable, 2, self.TEXT_BUILT, iColWidth)
		iColWidth = int((iChartWidth / 12 * 1))
		screen.setTableColumnHeader(szUnitsTable, 3, self.TEXT_KILLED, iColWidth)
		iColWidth = int((iChartWidth / 12 * 1))
		screen.setTableColumnHeader(szUnitsTable, 4, self.TEXT_LOST, iColWidth)
		iColWidth = int((iChartWidth / 12 * 4))
		screen.setTableColumnHeader(szBuildingsTable, 0, self.TEXT_BUILDINGS, iColWidth)
		iColWidth = int((iChartWidth / 12 * 1))
		screen.setTableColumnHeader(szBuildingsTable, 1, self.TEXT_BUILT, iColWidth)
		
		# Add Rows
		for i in range(self.iNumUnitStatsChartRows):
			screen.appendTableRow(szUnitsTable)
		iNumUnitRows = screen.getTableNumRows(szUnitsTable)

		for i in range(self.iNumBuildingStatsChartRows):
			screen.appendTableRow(szBuildingsTable)
		iNumBuildingRows = screen.getTableNumRows(szBuildingsTable)
		
		# Add Units to table
		for iUnitLoop in range(iNumUnits):
			#iRow = iUnitLoop
			iRow = unitDict[iUnitLoop] # edead
			
			if gc.getUnitInfo(iUnitLoop).isGraphicalOnly(): continue # edead
			
			iCol = 0
			szUnitName = gc.getUnitInfo(iUnitLoop).getDescription()
			screen.setTableText(szUnitsTable, iCol, iRow, szUnitName, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			
			iCol = 1
			iNumUnitsCurrent = aiUnitsCurrent[iUnitLoop]
			screen.setTableInt(szUnitsTable, iCol, iRow, str(iNumUnitsCurrent), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			
			iCol = 2
			iNumUnitsBuilt = aiUnitsBuilt[iUnitLoop]
			screen.setTableInt(szUnitsTable, iCol, iRow, str(iNumUnitsBuilt), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			
			iCol = 3
			iNumUnitsKilled = aiUnitsKilled[iUnitLoop]
			screen.setTableInt(szUnitsTable, iCol, iRow, str(iNumUnitsKilled), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			
			iCol = 4
			iNumUnitsLost = aiUnitsLost[iUnitLoop]
			screen.setTableInt(szUnitsTable, iCol, iRow, str(iNumUnitsLost), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
		# Add Buildings to table
		for iBuildingLoop in range(iNumBuildings):
			iRow = iBuildingLoop
			
			iCol = 0
			szBuildingName = gc.getBuildingInfo(iBuildingLoop).getDescription()
			screen.setTableText(szBuildingsTable, iCol, iRow, szBuildingName, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			iCol = 1
			iNumBuildingsBuilt = aiBuildingsBuilt[iBuildingLoop]
			screen.setTableInt(szBuildingsTable, iCol, iRow, str(iNumBuildingsBuilt), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

#############################################################################################################
##################################################### OTHER #################################################
#############################################################################################################

	def drawLine (self, screen, canvas, x0, y0, x1, y1, color):
	    screen.addLineGFC(canvas, self.getNextLineName(), x0, y0 + 1, x1, y1 + 1, color)
	    screen.addLineGFC(canvas, self.getNextLineName(), x0 + 1, y0, x1 + 1, y1, color)
	    screen.addLineGFC(canvas, self.getNextLineName(), x0, y0, x1, y1, color)

	def getTurnDate(self,turn):


                year = CyGame().getTurnYear(turn)

                #Rhye - start
##                if (year < 0):
##                    return localText.getText("TXT_KEY_TIME_BC", (-year,))
##                else:
##                    return localText.getText("TXT_KEY_TIME_AD", (year,))
                    
                iPlayer = CyGame().getActivePlayer()
                pPlayer = gc.getPlayer(iPlayer)
                tPlayer = gc.getTeam(pPlayer.getTeam())
                iBronzeWorking = 61
                iIronWorking = 63
                iCalendar = 33
                
                if (tPlayer.isHasTech(iCalendar)):  
                        if (year < 0):
                            return localText.getText("TXT_KEY_TIME_BC", (-year,))
                        else:
                            return localText.getText("TXT_KEY_TIME_AD", (year,))         
                elif (year >= 1500):
                        return localText.getText("TXT_KEY_AGE_RENAISSANCE", ())  
                elif (year >= 450):
                        return localText.getText("TXT_KEY_AGE_MEDIEVAL", ())    
                elif (year >= -800):
                        return localText.getText("TXT_KEY_AGE_IRON", ())    
                elif (year >= -2000):
                        return localText.getText("TXT_KEY_AGE_BRONZE", ())    
                else:
                        return localText.getText("TXT_KEY_AGE_STONE", ())    
                #Rhye - end


	def lineName(self,i):
	    return self.LINE_ID + str(i)

	def getNextLineName(self):
	    name = self.lineName(self.nLineCount)
	    self.nLineCount += 1
	    return name

	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	def deleteAllLines(self):
	    screen = self.getScreen()
	    i = 0
	    while (i < self.nLineCount):
		screen.deleteWidget(self.lineName(i))
		i += 1
	    self.nLineCount = 0

	def deleteAllWidgets(self, iNumPermanentWidgets = 0):
		self.deleteAllLines()
		screen = self.getScreen()
		i = self.nWidgetCount - 1
		while (i >= iNumPermanentWidgets):
			self.nWidgetCount = i
			screen.deleteWidget(self.getNextWidgetName())
			i -= 1

		self.nWidgetCount = iNumPermanentWidgets
		self.yMessage = 5

	# handle the input for this screen...
	def handleInput (self, inputClass):

		screen = self.getScreen()

		szWidgetName = inputClass.getFunctionName() + str(inputClass.getID())
		code = inputClass.getNotifyCode()

		# Exit
		if ( szWidgetName == self.szExitButtonName and code == NotifyCode.NOTIFY_CLICKED \
				or inputClass.getData() == int(InputTypes.KB_RETURN) ):
			# Reset Wonders so nothing lingers next time the screen is opened
			self.resetWonders()
			screen.hideScreen()

		# Slide graph
		if (szWidgetName == self.graphLeftButtonID and code == NotifyCode.NOTIFY_CLICKED):
		    self.slideGraph(- 2 * self.graphZoom / 5)
		    self.drawGraph()
		    
		elif (szWidgetName == self.graphRightButtonID and code == NotifyCode.NOTIFY_CLICKED):
		    self.slideGraph(2 * self.graphZoom / 5)
		    self.drawGraph()

		# Dropdown Box/ ListBox
		if (code == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):

			# Debug dropdown
			if (inputClass.getFunctionName() == self.DEBUG_DROPDOWN_ID):
				iIndex = screen.getSelectedPullDownID(self.DEBUG_DROPDOWN_ID)
				self.iActivePlayer = screen.getPullDownData(self.DEBUG_DROPDOWN_ID, iIndex)

				self.pActivePlayer = gc.getPlayer(self.iActivePlayer)
				self.iActiveTeam = self.pActivePlayer.getTeam()
				self.pActiveTeam = gc.getTeam(self.iActiveTeam)

				# Determine who this active player knows
				self.aiPlayersMet = []
				self.iNumPlayersMet = 0
				for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
					pLoopPlayer = gc.getPlayer(iLoopPlayer)
					iLoopPlayerTeam = pLoopPlayer.getTeam()
					if (self.pActiveTeam.isHasMet(iLoopPlayerTeam)):
						self.aiPlayersMet.append(iLoopPlayer)
						self.iNumPlayersMet += 1
				# Force recache of all scores
				self.scoreCache = []
				for t in self.RANGE_SCORES:
					self.scoreCache.append(None)
				self.redrawContents()

			iSelected = inputClass.getData()
#			print("iSelected : %d" %(iSelected))

############################### WONDERS / TOP CITIES TAB ###############################

			if (self.iActiveTab == self.iTopCitiesID):

				# Wonder type dropdown box
				if (szWidgetName == self.szWondersDropdownWidget):

					# Reset wonders stuff so that when the type shown changes the old contents don't mess with things

					self.iNumWonders = 0
					self.iActiveWonderCounter = 0
					self.iWonderID = -1
					self.aaWondersBuilt = []

					self.aaWondersBeingBuilt = []

					if (iSelected == 0):
						self.szWonderDisplayMode = "World Wonders"

					elif (iSelected == 1):
						self.szWonderDisplayMode = "National Wonders"

					elif (iSelected == 2):
						self.szWonderDisplayMode = "Projects"

					self.reset()

					self.calculateWondersList()
					self.determineListBoxContents()

					# Change selected wonder to the one at the top of the new list
					if (self.iNumWonders > 0):
						self.iWonderID = self.aiWonderListBoxIDs[0]

					self.redrawContents()

				# Wonders ListBox
				elif (szWidgetName == self.szWondersListBox):

					self.reset()
					self.iWonderID = self.aiWonderListBoxIDs[iSelected]
					self.iActiveWonderCounter = iSelected
					self.deleteAllWidgets(self.iNumWondersPermanentWidgets)
					self.drawWondersList()
#					self.redrawContents()

################################## GRAPH TAB ###################################

			elif (self.iActiveTab == self.iGraphID):

				# Graph dropdown to select what values are being graphed
				if (szWidgetName == self.szGraphDropdownWidget):

					if (iSelected == 0):
						self.iGraphTabID = self.TOTAL_SCORE

					elif (iSelected == 1):
						self.iGraphTabID = self.ECONOMY_SCORE

					elif (iSelected == 2):
						self.iGraphTabID = self.INDUSTRY_SCORE

					elif (iSelected == 3):
						self.iGraphTabID = self.AGRICULTURE_SCORE

					elif (iSelected == 4):
						self.iGraphTabID = self.POWER_SCORE

					elif (iSelected == 5):
						self.iGraphTabID = self.CULTURE_SCORE

					elif (iSelected == 6):
						self.iGraphTabID = self.ESPIONAGE_SCORE

					self.drawGraph()

				elif (szWidgetName == self.szTurnsDropdownWidget):

					self.zoomGraph(self.dropDownTurns[iSelected])
					self.drawGraph()

		# Something Clicked
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):

			######## Screen 'Tabs' for Navigation ########

			if (szWidgetName == self.szGraphTabWidget):
				self.iActiveTab = self.iGraphID
				self.reset()
				self.redrawContents()

			elif (szWidgetName == self.szDemographicsTabWidget):
				self.iActiveTab = self.iDemographicsID
				self.reset()
				self.redrawContents()

			elif (szWidgetName == self.szTopCitiesTabWidget):
				self.iActiveTab = self.iTopCitiesID
				self.reset()
				self.redrawContents()

			elif (szWidgetName == self.szStatsTabWidget):
				self.iActiveTab = self.iStatsID
				self.reset()
				self.redrawContents()

		return 0

	def update(self, fDelta):

		return
