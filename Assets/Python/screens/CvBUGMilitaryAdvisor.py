## CvBUGMilitaryAdvisor
##
## Allows grouping units by several factors and adds a Situation Report page
## showing Threat Index, Strategic Advantages and Vassal/DP/PA status of each rival.
##
## TODO:
##
## Deployment Tab
##  * Add unit filter buttons
##
## Sit Rep Tab
##  * Attitude icon
##
## Strat Adv Tab
##  * Allow player to add/remove units and resources to assume a rival has access to
##  * Examine trades for resources; ideally show sources of traded resources
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: Ruff_Hi (Situation Report tab)
##         EmperorFool (Deployment and Strategic Advantages tabs)

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import time
import re

import IconGrid_BUG
import AttitudeUtil
import BugUtil
import BugDll
import PlayerUtil
import UnitGrouper
import UnitUtil

# BUG - Mac Support - start
BugUtil.fixSets(globals())
# BUG - Mac Support - end

PyPlayer = PyHelpers.PyPlayer

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

UNIT_LOCATION_SCREEN = 0
SITUATION_REPORT_SCREEN = 1
STRATEGIC_ADVANTAGES_SCREEN = 2

class CvMilitaryAdvisor:
	"Shows the BUG Version of the Military Advisor"

	def __init__(self, screenId):
		self.screenId = screenId
		self.SCREEN_NAME = "MilitaryScreen-BUG"

		self.UNIT_LOC_TAB_ID = "MilitaryUnitLocTabWidget-BUG"
		self.SIT_REP_TAB_ID = "MilitarySitRepTabWidget-BUG"
		self.STRAT_ADV_TAB_ID = "MilitaryStratAdvTabWidget-BUG"

		self.X_GROUP_LIST = 20
		self.Y_GROUP_LIST = 190
		self.W_GROUP_LIST = 280
		
		self.X_MAP = 20
		self.Y_MAP = 220      # 190
		self.W_MAP = 580
		self.H_MAP_MAX = 470  # 500
		self.MAP_MARGIN = 20

		self.X_TEXT = 625
		self.Y_TEXT = 190
		self.W_TEXT = 380
		self.H_TEXT = 500
						
		self.X_LEADERS = 20
		self.Y_LEADERS = 80
		self.W_LEADERS = 985
		self.H_LEADERS = 90
		self.LEADER_BUTTON_SIZE = 64
		self.LEADER_MARGIN = 12

		self.LEADER_COLUMNS = int(self.W_LEADERS / (self.LEADER_BUTTON_SIZE + self.LEADER_MARGIN))

		self.grouper = UnitGrouper.StandardGrouper()
		self.selectedLeaders = set()
		self.selectedGroups = set()
		self.selectedUnits = set()
		self.groupingKeys = ["loc", "type"]
		
		self.bUnitDetails = False
		self.iShiftKeyDown = 0

		self.X_GREAT_GENERAL_BAR = 0
		self.Y_GREAT_GENERAL_BAR = 0
		self.W_GREAT_GENERAL_BAR = 0
		self.H_GREAT_GENERAL_BAR = 0

		self.UNIT_BUTTON_ID = "MilitaryAdvisorUnitButton-BUG"
		self.UNIT_LIST_ID = "MilitaryAdvisorUnitList-BUG"
		self.UNIT_BUTTON_LABEL_ID = "MilitaryAdvisorUnitButtonLabel-BUG"
		self.LEADER_BUTTON_ID = "MilitaryAdvisorLeaderButton-BUG"
		self.MINIMAP_PANEL = "MilitaryMiniMapPanel-BUG"


		self.iPlayerPower = 0
		self.iDemographicsMission = -1

		# dict for upgrade units
		self.FutureUnitsByUnitClass = {}

		self.EXIT_ID = "MilitaryScreenExit-BUG"
		self.BACKGROUND_ID = "MilitaryScreenBackground-BUG"
		self.HEADER_ID = "MilitaryScreenHeader-BUG"
		self.WIDGET_ID = "MilitaryScreenWidget-BUG"

		self.Z_BACKGROUND = -6.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
#		self.DZ = -0.2

		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Y_TITLE = 12
		self.L_SCREEN = 20

		self.X_EXIT = 994
		self.Y_EXIT = 726

		self.X_LINK = 100
		self.DX_LINK = 220
		self.Y_LINK = 726
		self.MARGIN = 20
		self.SPACING = 40
		
		self.SETTINGS_PANEL_X1 = 50
		self.SETTINGS_PANEL_X2 = 355
		self.SETTINGS_PANEL_X3 = 660
		self.SETTINGS_PANEL_Y = 150
		self.SETTINGS_PANEL_WIDTH = 300
		self.SETTINGS_PANEL_HEIGHT = 500
								
		self.nWidgetCount = 0
		self.iActivePlayer = -1

		self.minimapInitialized = False
		self.iScreen = UNIT_LOCATION_SCREEN

		# icongrid constants
		self.SHOW_LEADER_NAMES = False
		self.SHOW_ROW_BORDERS = True
		self.MIN_TOP_BOTTOM_SPACE = 30
		self.MIN_LEFT_RIGHT_SPACE = 10
		self.GROUP_BORDER = 8
		self.GROUP_LABEL_OFFSET = "   "
		self.MIN_COLUMN_SPACE = 5
		self.MIN_ROW_SPACE = 1
		self.iconGrid = None

		# sit rep constants
		self.SITREP_PANEL_SPACE = 50
		self.TITLE_HEIGHT = 0
		self.TABLE_CONTROL_HEIGHT = 0
#		self.RESOURCE_ICON_SIZE = 34

		self.szMaybeButton = ArtFileMgr.getInterfaceArtInfo("QUESTION_MARK").getPath()

						
	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, self.screenId)

	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()
										
	def interfaceScreen(self):

		self.timer = BugUtil.Timer("MilAdv")
		
		# Create a new screen
		screen = self.getScreen()
		if screen.isActive():
			return

		# over-ride screen width, height
		self.W_SCREEN = screen.getXResolution() - 40
		self.X_SCREEN = (screen.getXResolution() - 24) / 2
		self.L_SCREEN = 20

		if self.W_SCREEN < 1024:
			self.W_SCREEN = 1024
			self.L_SCREEN = 0
		
		self.X_EXIT = self.W_SCREEN - 30
		#self.Y_EXIT = 726
		#self.H_SCREEN = screen.getYResolution()
			
		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.iActivePlayer = CyGame().getActivePlayer()
		if self.iScreen == -1:
			self.iScreen = UNIT_LOCATION_SCREEN

		# Set the background widget and exit button
		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.showWindowBackground( False )
		#screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.setDimensions(self.L_SCREEN, screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.setText(self.EXIT_ID, "Background", u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		# Header...
		screen.setLabel(self.HEADER_ID, "Background", u"<font=4b>" + localText.getText("TXT_KEY_MILITARY_ADVISOR_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		self.iconGrid = None
		self.unitLocationInitDone = False
		if self.iScreen == UNIT_LOCATION_SCREEN:
			self.showUnitLocation()
		elif self.iScreen == SITUATION_REPORT_SCREEN:
			self.showSituationReport()
		elif self.iScreen == STRATEGIC_ADVANTAGES_SCREEN:
			self.showStrategicAdvantages()
		self.timer.logSpan("total")

	def drawTabs(self):
	
		screen = self.getScreen()

		xLink = self.MARGIN
		if (self.iScreen != UNIT_LOCATION_SCREEN):
			szText = u"<font=4>" + localText.getText("TXT_KEY_MILITARY_UNIT_LOCATION", ()).upper() + "</font>"
		else:
			szText = u"<font=4>" + localText.getColorText("TXT_KEY_MILITARY_UNIT_LOCATION", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>"
		screen.setText(self.UNIT_LOC_TAB_ID, "", szText, CvUtil.FONT_LEFT_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		xLink += CyInterface().determineWidth(szText) + self.SPACING

		if (self.iScreen != SITUATION_REPORT_SCREEN):
			szText = u"<font=4>" + localText.getText("TXT_KEY_MILITARY_SITUATION_REPORT", ()).upper() + "</font>"
		else:
			szText = u"<font=4>" + localText.getColorText("TXT_KEY_MILITARY_SITUATION_REPORT", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>"
		screen.setText(self.SIT_REP_TAB_ID, "", szText, CvUtil.FONT_LEFT_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		xLink += CyInterface().determineWidth(szText) + self.SPACING

		if (self.iScreen != STRATEGIC_ADVANTAGES_SCREEN):
			szText = u"<font=4>" + localText.getText("TXT_KEY_MILITARY_STRATEGIC_ADVANTAGES", ()).upper() + "</font>"
		else:
			szText = u"<font=4>" + localText.getColorText("TXT_KEY_MILITARY_STRATEGIC_ADVANTAGES", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>"
		screen.setText(self.STRAT_ADV_TAB_ID, "", szText, CvUtil.FONT_LEFT_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

#### Situation Report Tab ####

	def showSituationReport(self):

		self.timer.start()
		self.deleteAllWidgets()
		screen = self.getScreen()
		
		# get Player arrays
		pVassals = [[]] * gc.getMAX_PLAYERS()
		pDefPacts = [[]] * gc.getMAX_PLAYERS()
		bVassals = False
		bDefPacts = False
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iLoopPlayer)

			if (pPlayer.isAlive()
			and (gc.getTeam(pPlayer.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
			or gc.getGame().isDebugMode())
			and iLoopPlayer != self.iActivePlayer
			and not pPlayer.isBarbarian()
			and not pPlayer.isMinorCiv()):
				pVassals[iLoopPlayer] = PlayerUtil.getVassals(iLoopPlayer, self.iActivePlayer)
				pDefPacts[iLoopPlayer] = PlayerUtil.getDefensivePacts(iLoopPlayer, self.iActivePlayer)

				if len(pVassals[iLoopPlayer]) > 0:
					bVassals = True

				if len(pDefPacts[iLoopPlayer]) > 0:
					bDefPacts = True

		bVassals = True
		bDefPacts = True
		self.initIconGrid(screen, bVassals, bDefPacts)
		self.initPower()
		
		activePlayer = gc.getPlayer(self.iActivePlayer)		
		
		# Assemble the panel
		iPANEL_X = 5
		iPANEL_Y = 60
		iPANEL_WIDTH = self.W_SCREEN - 20
		iPANEL_HEIGHT = self.H_SCREEN - 120

		self.tradePanel = self.getNextWidgetName()
		screen.addPanel(self.tradePanel, "", "", True, True, iPANEL_X, iPANEL_Y, iPANEL_WIDTH, iPANEL_HEIGHT, PanelStyles.PANEL_STYLE_MAIN )
		
		self.iconGrid.createGrid()
		self.iconGrid.clearData()

		iRow = 0
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iLoopPlayer)

			if (pPlayer.isAlive()
			and (gc.getTeam(pPlayer.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
			or gc.getGame().isDebugMode())
			and iLoopPlayer != self.iActivePlayer
			and not pPlayer.isBarbarian()
			and not pPlayer.isMinorCiv()):


#				szPlayerName = pPlayer.getName() + "/" + pPlayer.getCivilizationShortDescription(0)
#				BugUtil.debug("Grid_ThreatIndex - Start %i %s" % (iLoopPlayer, szPlayerName))
#				BugUtil.debug("Grid_ThreatIndex - Start %i" % (iLoopPlayer))

				self.iconGrid.appendRow(pPlayer.getName(), "", 3)

				# add leaderhead icon
				self.iconGrid.addIcon(iRow, self.Col_Leader,
										gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getButton(), 64, 
										WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, self.iActivePlayer)

				# add worst enemy
				self.Grid_WorstEnemy(iRow, iLoopPlayer)

				# add current war opponents
				pActiveWars = PlayerUtil.getActiveWars(iLoopPlayer, self.iActivePlayer)
				bCurrentWar = len(pActiveWars) > 0
				for pLoopPlayer in pActiveWars:
					self.iconGrid.addIcon(iRow, self.Col_Curr_Wars, 
											gc.getLeaderHeadInfo (pLoopPlayer.getLeaderType()).getButton(), 32, 
											*BugDll.widgetVersion(2, "WIDGET_LEADERHEAD_RELATIONS", iLoopPlayer, pLoopPlayer.getID(),
																WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, pLoopPlayer.getID()))

				# show vassals
				if bVassals:
					for pLoopPlayer in pVassals[iLoopPlayer]:
						self.iconGrid.addIcon(iRow, self.Col_Vassals, 
												gc.getLeaderHeadInfo (pLoopPlayer.getLeaderType()).getButton(), 32, 
												*BugDll.widgetVersion(2, "WIDGET_LEADERHEAD_RELATIONS", iLoopPlayer, pLoopPlayer.getID(),
																	WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, pLoopPlayer.getID()))

				# show defensive pacts
				if bDefPacts:
					for pLoopPlayer in pDefPacts[iLoopPlayer]:
						self.iconGrid.addIcon(iRow, self.Col_DefPacts, 
												gc.getLeaderHeadInfo (pLoopPlayer.getLeaderType()).getButton(), 32, 
												*BugDll.widgetVersion(2, "WIDGET_LEADERHEAD_RELATIONS", iLoopPlayer, pLoopPlayer.getID(),
																	WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, pLoopPlayer.getID()))

				# show players that the current player will declare on
				bWHEOOH, pPossibleWars = PlayerUtil.getPossibleWars(iLoopPlayer, self.iActivePlayer)
				for pLoopPlayer in pPossibleWars:
					self.iconGrid.addIcon(iRow, self.Col_WillDeclareOn, 
											gc.getLeaderHeadInfo (pLoopPlayer.getLeaderType()).getButton(), 32, 
											*BugDll.widgetVersion(2, "WIDGET_LEADERHEAD_RELATIONS", iLoopPlayer, pLoopPlayer.getID(),
																WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, pLoopPlayer.getID()))
				# show WHEOOH
				if bWHEOOH:
					sWHEOOH = u" %c" % CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR)
				else:
					sWHEOOH = ""
				
				# show possible trade embargos
				pPossibleEmbargos = PlayerUtil.getPossibleEmbargos(iLoopPlayer, self.iActivePlayer)
				for pLoopPlayer in pPossibleEmbargos:
					self.iconGrid.addIcon(iRow, self.Col_WillEmbargo, 
											gc.getLeaderHeadInfo (pLoopPlayer.getLeaderType()).getButton(), 32, 
											*BugDll.widgetVersion(2, "WIDGET_LEADERHEAD_RELATIONS", iLoopPlayer, pLoopPlayer.getID(),
																WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, pLoopPlayer.getID()))

				self.iconGrid.setText(iRow, self.Col_WHEOOH, sWHEOOH, 3)

				# add the threat index
				self.Grid_ThreatIndex(iRow, iLoopPlayer, bCurrentWar, bWHEOOH)

				iRow += 1

		self.iconGrid.refresh()
		self.drawTabs()
		self.timer.log("SitRep")

	def initIconGrid(self, screen, bVassals, bDefPacts):
		
		(
			self.Col_Leader,
			self.Col_WHEOOH,
			self.Col_WEnemy,
			self.Col_Threat,
			self.Col_Curr_Wars,
			self.Col_WillDeclareOn,
			self.Col_WillEmbargo,
			self.Col_Vassals,
			self.Col_DefPacts,
		) = range(9)
		if (not bVassals):
			# shift over 1 to make room for vassals column
			self.Col_DefPacts -= 1
		
		if (not bVassals and not bDefPacts):
			columns = ( IconGrid_BUG.GRID_ICON_COLUMN,
						IconGrid_BUG.GRID_TEXT_COLUMN,
						IconGrid_BUG.GRID_ICON_COLUMN,
						IconGrid_BUG.GRID_STACKEDBAR_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN)
		if (bVassals and bDefPacts):
			columns = ( IconGrid_BUG.GRID_ICON_COLUMN,
						IconGrid_BUG.GRID_TEXT_COLUMN,
						IconGrid_BUG.GRID_ICON_COLUMN,
						IconGrid_BUG.GRID_STACKEDBAR_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN)
		else:
			columns = ( IconGrid_BUG.GRID_ICON_COLUMN,
						IconGrid_BUG.GRID_TEXT_COLUMN,
						IconGrid_BUG.GRID_ICON_COLUMN,
						IconGrid_BUG.GRID_STACKEDBAR_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN)

		gridX = self.MIN_LEFT_RIGHT_SPACE + 10
		gridY = self.MIN_TOP_BOTTOM_SPACE + self.SITREP_PANEL_SPACE + self.TABLE_CONTROL_HEIGHT + self.TITLE_HEIGHT + 10
		gridWidth = self.W_SCREEN - 10 # - self.MIN_LEFT_RIGHT_SPACE * 2 - 20
		gridHeight = self.H_SCREEN - self.MIN_TOP_BOTTOM_SPACE * 2 - self.SITREP_PANEL_SPACE - self.TITLE_HEIGHT - 20
		self.iconGrid = IconGrid_BUG.IconGrid_BUG(self.getNextWidgetName(), screen, gridX, gridY, gridWidth, gridHeight,
													columns, True, self.SHOW_LEADER_NAMES, self.SHOW_ROW_BORDERS)

		# set constants
		self.iconGrid.setGroupBorder(self.GROUP_BORDER)
		self.iconGrid.setGroupLabelOffset(self.GROUP_LABEL_OFFSET)
		self.iconGrid.setMinColumnSpace(self.MIN_COLUMN_SPACE)
		self.iconGrid.setMinRowSpace(self.MIN_ROW_SPACE)

		# set headings
		self.iconGrid.setHeader(self.Col_Leader, "", 3)
		self.iconGrid.setHeader(self.Col_WHEOOH, "", 3)
		self.iconGrid.setHeader(self.Col_WEnemy, localText.getText("TXT_KEY_MILITARY_SITREP_ENEMY", ()), 3)
		self.iconGrid.setHeader(self.Col_Threat, localText.getText("TXT_KEY_MILITARY_SITREP_THREAT_INDEX", ()), 3)
		self.iconGrid.setHeader(self.Col_Curr_Wars, localText.getText("TXT_KEY_MILITARY_SITREP_WARS_ACTIVE", ()), 3)
		self.iconGrid.setHeader(self.Col_WillDeclareOn, localText.getText("TXT_KEY_MILITARY_SITREP_WARS_OPTIONAL", ()), 3)
		self.iconGrid.setHeader(self.Col_WillEmbargo, localText.getText("TXT_KEY_MILITARY_SITREP_POSSIBLE_EMBARGOS_2", ()), 3)

		if bVassals:
			self.iconGrid.setHeader(self.Col_Vassals, localText.getText("TXT_KEY_MILITARY_SITREP_VASSALS", ()), 3)

		if bDefPacts:
			self.iconGrid.setHeader(self.Col_DefPacts, localText.getText("TXT_KEY_MILITARY_SITREP_DEFPACTS", ()), 3)

		self.iconGrid.createColumnGroup("", 1)
		self.iconGrid.createColumnGroup("", 1)
		self.iconGrid.createColumnGroup(localText.getText("TXT_KEY_MILITARY_SITREP_WORST", ()), 1)
		self.iconGrid.createColumnGroup("", 1)
		self.iconGrid.createColumnGroup(localText.getText("TXT_KEY_MILITARY_SITREP_WARS", ()), 2)
		self.iconGrid.createColumnGroup(localText.getText("TXT_KEY_MILITARY_SITREP_POSSIBLE_EMBARGOS_1", ()), 1)

		self.iconGrid.setTextColWidth(self.Col_WHEOOH, 25)
		self.iconGrid.setStackedBarColWidth(self.Col_Threat, 120)
				
		gridWidth = self.iconGrid.getPrefferedWidth()
		gridHeight = self.iconGrid.getPrefferedHeight()
		self.SITREP_LEFT_RIGHT_SPACE = (self.W_SCREEN - gridWidth - 20) / 2
		self.SITREP_TOP_BOTTOM_SPACE = (self.H_SCREEN - gridHeight - 20) / 2
		gridX = self.SITREP_LEFT_RIGHT_SPACE + 10
		gridY = self.SITREP_TOP_BOTTOM_SPACE + 10

		self.iconGrid.setPosition(gridX, gridY)
		self.iconGrid.setSize(gridWidth, gridHeight)

	def initPower(self):
		# active player power
		self.iPlayerPower = gc.getActivePlayer().getPower()

		# see demographics?		
		self.iDemographicsMission = -1
		for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
			if (gc.getEspionageMissionInfo(iMissionLoop).isSeeDemographics()):
				self.iDemographicsMission = iMissionLoop
				break

		return

	def Grid_ThreatIndex(self, iRow, iPlayer, bCurrentWar, bWHEOOH):

		pPlayer = gc.getPlayer(iPlayer)

#		BugUtil.debug("Grid_ThreatIndex - Start")

		if gc.getTeam(pPlayer.getTeam()).isAVassal():
			self.iconGrid.addStackedBar(iRow, self.Col_Threat, -1, "", localText.getText("TXT_KEY_MILITARY_SITREP_VASSAL", ()), 3)
#			BugUtil.debug("Grid_ThreatIndex - is vassal")
			return

		# initialize threat index
		iThreat = 0

		# add attitude threat value
		iRel = AttitudeUtil.getAttitudeCount(iPlayer, self.iActivePlayer)
		fRel_Threat = float(38) * float(15 - iRel) / float(30)
		if fRel_Threat < 0:
			fRel_Threat = 0.0
		elif fRel_Threat > 38:
			fRel_Threat = 38.0

#		BugUtil.debug("Grid_ThreatIndex - relationships")

		# calculate the power threat value
		fPwr_Threat = 0
		iPower = pPlayer.getPower()
		if (iPower > 0): # avoid divide by zero
			fPowerRatio = float(self.iPlayerPower) / float(iPower)
			fPwr_Threat = float(38) * float(1.5 - fPowerRatio)
			if fPwr_Threat < 0:
				fPwr_Threat = 0.0
			elif fPwr_Threat > 38:
				fPwr_Threat = 38.0

		# set power threat to 75% of max if active player cannot see the demographics
		bCannotSeeDemographics = False
		if not gc.getActivePlayer().canDoEspionageMission(self.iDemographicsMission, iPlayer, None, -1):
			bCannotSeeDemographics = True
			fPwr_Threat = 38.0 * 0.75
#			self.iconGrid.addStackedBar(iRow, self.Col_Threat, -1, "", "n/a", 3)
#			BugUtil.debug("Grid_ThreatIndex - not enough spy points")
#			return

#		BugUtil.debug("Grid_ThreatIndex - power")

		# total threat, pre WHEOOH adjustment
		fThreat = fRel_Threat + fPwr_Threat

		# WHEOOH adjustment
		if bWHEOOH and not bCurrentWar:
			fThreat = fThreat * 1.3

		# reduce the threat if the current player is in a defensive pact with the active player
		if gc.getTeam(pPlayer.getTeam()).isDefensivePact(gc.getPlayer(self.iActivePlayer).getTeam()):
			fThreat = fThreat * 0.2

		BugUtil.debug("Grid_ThreatIndex - threat adjustments - threat index %i" % int(fThreat))

		if fThreat < 15:
			sColour = "COLOR_PLAYER_GREEN"
			sThreat = localText.getText("TXT_KEY_MILITARY_THREAT_INDEX_LOW", ())
		elif  fThreat < 35:
			sColour = "COLOR_PLAYER_BLUE"
			sThreat = localText.getText("TXT_KEY_MILITARY_THREAT_INDEX_GUARDED", ())
		elif  fThreat < 55:
			sColour = "COLOR_PLAYER_YELLOW"
			sThreat = localText.getText("TXT_KEY_MILITARY_THREAT_INDEX_ELEVATED", ())
		elif  fThreat < 75:
			sColour = "COLOR_PLAYER_ORANGE"
			sThreat = localText.getText("TXT_KEY_MILITARY_THREAT_INDEX_HIGH", ())
		else:
			sColour = "COLOR_PLAYER_RED"
			sThreat = localText.getText("TXT_KEY_MILITARY_THREAT_INDEX_SEVERE", ())

		if bCannotSeeDemographics:
			sThreat += " (est)"

		self.iconGrid.addStackedBar(iRow, self.Col_Threat, fThreat, sColour, sThreat, 3)
#		BugUtil.debug("Grid_ThreatIndex - bar placed")
		return

	def Grid_WorstEnemy(self, iRow, iLeader):
		pWorstEnemy = PlayerUtil.getWorstEnemy(iLeader, self.iActivePlayer)
		if pWorstEnemy:
			self.iconGrid.addIcon(iRow, self.Col_WEnemy,
									gc.getLeaderHeadInfo(pWorstEnemy.getLeaderType()).getButton(), 45,  
									*BugDll.widgetVersion(2, "WIDGET_LEADERHEAD_RELATIONS", iLeader, pWorstEnemy.getID(),
														WidgetTypes.WIDGET_LEADERHEAD, iLeader, pWorstEnemy.getID()))
		else:
			pass
			#self.iconGrid.addIcon(iRow, self.Col_WEnemy,
			#						ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), 35, 
			#						WidgetTypes.WIDGET_GENERAL, -1)

	def GetDeclareWar(self, iRow, iPlayer):
		# this module will check if the iPlayer will declare war
		# on the other leaders.  We cannot check if the iPlayer, the iActivePlayer
		# and the iTargetPlayer don't all know each other.
		# However, the code wouldn't have got this far if the iPlayer didn't know the iActivePlayer
		# so we only need to check if the iPlayer and the iActivePlayer both know the iTargetPlayer.

		# also need to check on vassal state - will do that later
		return iLeaderWars


#### Strategic Advantages Tab ####

	def showStrategicAdvantages(self):
		self.timer.start()
		self.deleteAllWidgets()
		screen = self.getScreen()
		
		# Assemble the panel
		iPANEL_X = 5
		iPANEL_Y = 60
		iPANEL_WIDTH = self.W_SCREEN - 20
		iPANEL_HEIGHT = self.H_SCREEN - 120
		self.tradePanel = self.getNextWidgetName()
		screen.addPanel(self.tradePanel, "", "", True, True, iPANEL_X, iPANEL_Y, iPANEL_WIDTH, iPANEL_HEIGHT, PanelStyles.PANEL_STYLE_MAIN )
		
		self.initStratAdvGrid(screen)
		self.fillStratAdvGrid()
		self.drawTabs()
		self.timer.log("StratAdv")

	def initStratAdvGrid(self, screen):
		(
			self.SA_Col_Leader,
			self.SA_Col_Bonus_Us,
			self.SA_Col_Bonus_Them,
			self.SA_Col_Unit_Us_Yes,
			self.SA_Col_Unit_Us_Maybe,
			self.SA_Col_Unit_Them_Yes,
			self.SA_Col_Unit_Them_Maybe,
		) = range(7)
		
		columns = (
			IconGrid_BUG.GRID_ICON_COLUMN,
			IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
			IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
			IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
			IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
			IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
			IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
		)
		
		gridX = self.MIN_LEFT_RIGHT_SPACE + 10
		gridY = self.MIN_TOP_BOTTOM_SPACE + self.SITREP_PANEL_SPACE + self.TABLE_CONTROL_HEIGHT + self.TITLE_HEIGHT + 10
		gridWidth = self.W_SCREEN - 10 # - self.MIN_LEFT_RIGHT_SPACE * 2 - 20
		gridHeight = self.H_SCREEN - self.MIN_TOP_BOTTOM_SPACE * 2 - self.SITREP_PANEL_SPACE - self.TITLE_HEIGHT - 20
		self.iconGrid = IconGrid_BUG.IconGrid_BUG(
				self.getNextWidgetName(), screen, gridX, gridY, gridWidth, gridHeight,
				columns, True, self.SHOW_LEADER_NAMES, self.SHOW_ROW_BORDERS)
		
		# set constants
		self.iconGrid.setGroupBorder(self.GROUP_BORDER)
		self.iconGrid.setGroupLabelOffset(self.GROUP_LABEL_OFFSET)
		self.iconGrid.setMinColumnSpace(self.MIN_COLUMN_SPACE)
		self.iconGrid.setMinRowSpace(self.MIN_ROW_SPACE)
		
		# set headings
		self.iconGrid.setHeader(self.SA_Col_Leader, "", 3)
		self.iconGrid.setHeader(self.SA_Col_Bonus_Us, localText.getText("TXT_KEY_MILITARY_STRATADV_OURS", ()), 3)
		self.iconGrid.setHeader(self.SA_Col_Bonus_Them, localText.getText("TXT_KEY_MILITARY_STRATADV_THEIRS", ()), 3)
		self.iconGrid.setHeader(self.SA_Col_Unit_Us_Yes, localText.getText("TXT_KEY_MILITARY_STRATADV_KNOWN", ()), 3)
		self.iconGrid.setHeader(self.SA_Col_Unit_Us_Maybe, localText.getText("TXT_KEY_MILITARY_STRATADV_POSSIBLE", ()), 3)
		self.iconGrid.setHeader(self.SA_Col_Unit_Them_Yes, localText.getText("TXT_KEY_MILITARY_STRATADV_KNOWN", ()), 3)
		self.iconGrid.setHeader(self.SA_Col_Unit_Them_Maybe, localText.getText("TXT_KEY_MILITARY_STRATADV_POSSIBLE", ()), 3)
		
		self.iconGrid.createColumnGroup("", 1)
		self.iconGrid.createColumnGroup(localText.getText("TXT_KEY_MILITARY_STRATADV_RESOURCES", ()), 2)
		self.iconGrid.createColumnGroup(localText.getText("TXT_KEY_MILITARY_STRATADV_OUR_UNITS", ()), 2)
		self.iconGrid.createColumnGroup(localText.getText("TXT_KEY_MILITARY_STRATADV_THEIR_UNITS", ()), 2)
		
		gridWidth = self.iconGrid.getPrefferedWidth()
		gridHeight = self.iconGrid.getPrefferedHeight()
		self.SITREP_LEFT_RIGHT_SPACE = (self.W_SCREEN - gridWidth - 20) / 2
		self.SITREP_TOP_BOTTOM_SPACE = (self.H_SCREEN - gridHeight - 20) / 2
		gridX = self.SITREP_LEFT_RIGHT_SPACE + 10
		gridY = self.SITREP_TOP_BOTTOM_SPACE + 10

		self.iconGrid.setPosition(gridX, gridY)
		self.iconGrid.setSize(gridWidth, gridHeight)
		self.iconGrid.createGrid()
	
	def fillStratAdvGrid(self):
		self.iconGrid.clearData()
		self.iHumanKnowableUnits = UnitUtil.getKnowableUnits(self.iActivePlayer)
		self.iHumanUnits = UnitUtil.getTrainableUnits(self.iActivePlayer, self.iHumanKnowableUnits, True, True)
		#self.iHumanYesUnits, self.iHumanNoUnits = UnitUtil.getTrainableAndUntrainableUnits(self.iActivePlayer, self.iHumanKnowableUnits, True)
		BugUtil.debug("----------------------- fillStratAdvGrid start")
		self.iHumanObsoleteUnits = UnitUtil.findObsoleteUnits(self.iHumanUnits)
		for eUnit in self.iHumanObsoleteUnits:
			BugUtil.debug("  obs %s", gc.getUnitInfo(eUnit).getDescription())
		
		activePlayer, activeTeam = PlayerUtil.getPlayerAndTeam(self.iActivePlayer)
		iRow = 0
		for player in PlayerUtil.players(alive=True, barbarian=False, minor=False):
			ePlayer = player.getID()
			if (ePlayer != self.iActivePlayer
					and (activeTeam.isHasMet(player.getTeam()) or gc.getGame().isDebugMode())):
				self.iconGrid.appendRow(player.getName(), "", 3)
				
				# add leaderhead icon
				self.iconGrid.addIcon(iRow, self.SA_Col_Leader,
						gc.getLeaderHeadInfo(player.getLeaderType()).getButton(), 64, 
						WidgetTypes.WIDGET_LEADERHEAD, player.getID(), self.iActivePlayer)
				
				# add bonus and unit icons
				self.addStratAdvBonuses(activePlayer, player, iRow)
				self.addStratAdvUnits(activePlayer, player, iRow)
				
				iRow += 1
		
		BugUtil.debug("----------------------- fillStratAdvGrid end")
		self.iconGrid.refresh()
	
	def addStratAdvBonuses(self, activePlayer, player, iRow):
		if activePlayer.canTradeNetworkWith(player.getID()):
			self.iRivalBonuses = set()
			ours = []
			theirs = []
			for eBonus in UnitUtil.strategicBonuses:
				bWeHave = activePlayer.getNumAvailableBonuses(eBonus) > 0
				bTheyHave = player.getNumAvailableBonuses(eBonus) > 0
				if bTheyHave:
					self.iRivalBonuses.add(eBonus)
				if bWeHave and not bTheyHave:
					ours.append(eBonus)
				elif bTheyHave and not bWeHave:
					theirs.append(eBonus)
			self.addStratAdvBonusIcons(iRow, self.SA_Col_Bonus_Us, ours)
			self.addStratAdvBonusIcons(iRow, self.SA_Col_Bonus_Them, theirs)
		else:
			self.iRivalBonuses = None
			szButton = ArtFileMgr.getInterfaceArtInfo("QUESTION_MARK").getPath()
			self.iconGrid.addIcon(iRow, self.SA_Col_Bonus_Us, szButton, 32, WidgetTypes.WIDGET_GENERAL, -1)
			self.iconGrid.addIcon(iRow, self.SA_Col_Bonus_Them, szButton, 32, WidgetTypes.WIDGET_GENERAL, -1)
	
	def addStratAdvBonusIcons(self, iRow, iCol, bonuses):
		bonuses.sort()
		for eBonus in bonuses:
			self.iconGrid.addIcon(iRow, iCol, gc.getBonusInfo(eBonus).getButton(), 
					32, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, eBonus)

	def addStratAdvUnits(self, activePlayer, player, iRow):
		if (not gc.getTeam(activePlayer.getTeam()).isTechTrading()
				and not gc.getTeam(player.getTeam()).isTechTrading()):
			szButton = ArtFileMgr.getInterfaceArtInfo("QUESTION_MARK").getPath()
			self.iconGrid.addIcon(iRow, self.SA_Col_Unit_Us_Yes, szButton, 32, WidgetTypes.WIDGET_GENERAL, -1)
			self.iconGrid.addIcon(iRow, self.SA_Col_Unit_Them_Yes, szButton, 32, WidgetTypes.WIDGET_GENERAL, -1)
			return
		
		iAIUnits, iAIMaybeUnits = UnitUtil.getKnownTrainableUnits(player.getID(), self.iActivePlayer, self.iHumanKnowableUnits, self.iRivalBonuses, True)
		# determine units that human can build that the AI cannot
		yesUnits = set()
		maybeUnits = set()
		for iUnit in self.iHumanUnits:
			if not UnitUtil.isUnitOrUpgradeInSet(iUnit, iAIUnits):
				if UnitUtil.isUnitOrUpgradeInSet(iUnit, iAIMaybeUnits):
					maybeUnits.add(iUnit)
				else:
					yesUnits.add(iUnit)
#		BugUtil.debug("-----------------------")
#		for eUnit in UnitUtil.findObsoleteUnits(yesUnits):
#			BugUtil.debug("  obs %s", gc.getUnitInfo(eUnit).getDescription())
		yesUnits -= self.iHumanObsoleteUnits
		maybeUnits -= self.iHumanObsoleteUnits
		self.addStratAdvUnitIcons(iRow, self.SA_Col_Unit_Us_Yes, yesUnits)
		self.addStratAdvUnitIcons(iRow, self.SA_Col_Unit_Us_Maybe, maybeUnits)
		
		# determine units that AI can build that the human cannot
		yesUnits = set()
		maybeUnits = set()
		for iUnit in iAIUnits:
			if not UnitUtil.isUnitOrUpgradeInSet(iUnit, self.iHumanUnits):
				yesUnits.add(iUnit)
		for iUnit in iAIMaybeUnits:
			if not UnitUtil.isUnitOrUpgradeInSet(iUnit, self.iHumanUnits):
				maybeUnits.add(iUnit)
		BugUtil.debug("-----------------------")
		for eUnit in UnitUtil.findObsoleteUnits(yesUnits):
			BugUtil.debug("  obs %s", gc.getUnitInfo(eUnit).getDescription())
		yesUnits -= UnitUtil.findObsoleteUnits(yesUnits)
		self.addStratAdvUnitIcons(iRow, self.SA_Col_Unit_Them_Yes, yesUnits)
		self.addStratAdvUnitIcons(iRow, self.SA_Col_Unit_Them_Maybe, maybeUnits)
		
#		iRivalYesUnits, iRivalNoUnits = UnitUtil.getKnownTrainableUnits(player.getID(), self.iActivePlayer, self.iHumanKnowableUnits, True)
#		
#		# determine units that both the player and rival can build for sure
#		removeUnits = set()
#		for iUnit in self.iHumanYesUnits:
#			if UnitUtil.isUnitOrUpgradeInSet(iUnit, iRivalYesUnits):
#				removeUnits.add(iUnit)
#		for iUnit in iRivalYesUnits:
#			if UnitUtil.isUnitOrUpgradeInSet(iUnit, self.iHumanYesUnits):
#				removeUnits.add(iUnit)
#		
#		iHumanYesUnits = self.iHumanActualYesUnits - removeUnits
#		self.addStratAdvUnitIcons(iRow, self.SA_Col_Unit_Us_Yes, iHumanYesUnits)
#		self.addStratAdvUnitIcons(iRow, self.SA_Col_Unit_Us_Maybe, self.iHumanNoUnits)
#		
#		BugUtil.debug("-----------------------")
#		for eUnit in UnitUtil.findObsoleteUnits(iRivalYesUnits):
#			BugUtil.debug("  obs %s", gc.getUnitInfo(eUnit).getDescription())
#		iRivalYesUnits -= UnitUtil.findObsoleteUnits(iRivalYesUnits)
#		iRivalYesUnits -= removeUnits
#		self.addStratAdvUnitIcons(iRow, self.SA_Col_Unit_Them_Yes, iRivalYesUnits)
#		self.addStratAdvUnitIcons(iRow, self.SA_Col_Unit_Them_Maybe, iRivalNoUnits)

	def addStratAdvUnitIcons(self, iRow, iCol, iUnits):
		if iUnits:
			iUnitList = [iUnit for iUnit in iUnits]
			iUnitList.sort()
			for iUnit in iUnitList:
				szButton = gc.getUnitInfo(iUnit).getButton()
				self.iconGrid.addIcon(iRow, iCol, szButton, 32, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit)


#### Deployment Tab ####

	def showUnitLocation(self):
		self.deleteAllWidgets()	
		screen = self.getScreen()
		self.UL_drawUnitSelectionControls(screen)
		if not self.unitLocationInitDone:
			self.selectedLeaders.clear()
			self.selectedLeaders.add(self.iActivePlayer)
			self.selectedGroups.clear()
			self.selectedUnits.clear()
			self.UL_initMinimap(screen)
			self.unitLocationInitDone = True
			self.UL_refresh(True, True)
		else:
			self.UL_refresh(False, True)

		self.drawCombatExperience()
		self.drawTabs()

	def UL_initMinimap(self, screen):
		# Minimap initialization
		self.timer.start()
		map = CyMap()
		iMap_W = map.getGridWidth()
		iMap_H = map.getGridHeight()
		self.H_MAP = (self.W_MAP * iMap_H) / iMap_W
		if (self.H_MAP > self.H_MAP_MAX):
			self.W_MAP = (self.H_MAP_MAX * iMap_W) / iMap_H
			self.H_MAP = self.H_MAP_MAX

		szPanel_ID = self.MINIMAP_PANEL
		screen.addPanel(szPanel_ID, u"", "", False, False, self.X_MAP, self.Y_MAP, self.W_MAP, self.H_MAP, PanelStyles.PANEL_STYLE_MAIN)
		screen.initMinimap(self.X_MAP + self.MAP_MARGIN, self.X_MAP + self.W_MAP - self.MAP_MARGIN, self.Y_MAP + self.MAP_MARGIN, self.Y_MAP + self.H_MAP - self.MAP_MARGIN, self.Z_CONTROLS)
		screen.updateMinimapSection(False, False)
		screen.updateMinimapColorFromMap(MinimapModeTypes.MINIMAPMODE_TERRITORY, 0.3)
		screen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_MILITARY)

		self.UL_setMinimapVisibility(screen, True)
		screen.bringMinimapToFront()
		self.timer.log("minimap")

	def UL_setMinimapVisibility(self, screen, bVisibile):
		iOldMode = CyInterface().getShowInterface()

		if bVisibile:
			CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_MINIMAP_ONLY)
		else:
			CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_HIDE)
			
		screen.updateMinimapVisibility()
		CyInterface().setShowInterface(iOldMode)
	
	def UL_drawUnitSelectionControls(self, screen):
		self.szDropdownWidgetGroup1 = self.getNextWidgetName()
		screen.addDropDownBoxGFC(self.szDropdownWidgetGroup1, self.X_GROUP_LIST, self.Y_GROUP_LIST, self.W_GROUP_LIST, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		self.szDropdownWidgetGroup2 = self.getNextWidgetName()
		screen.addDropDownBoxGFC(self.szDropdownWidgetGroup2, self.X_GROUP_LIST + self.W_GROUP_LIST + 20, self.Y_GROUP_LIST, self.W_GROUP_LIST, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		self.groupDropDowns = [self.szDropdownWidgetGroup1, self.szDropdownWidgetGroup2]
		for grouping in self.grouper:
			screen.addPullDownString(self.szDropdownWidgetGroup1, grouping.title, grouping.index, grouping.index, grouping.key == self.groupingKeys[0])
			screen.addPullDownString(self.szDropdownWidgetGroup2, grouping.title, grouping.index, grouping.index, grouping.key == self.groupingKeys[1])

	def UL_refresh(self, bReload, bRedraw):
		if (self.iActivePlayer < 0):
			return
		
		screen = self.getScreen()
		if bRedraw:
			# Set scrollable area for unit buttons
			szPanel_ID = self.getNextWidgetName()
			screen.addPanel(szPanel_ID, "", "", True, True, self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_MAIN)
			
			# Set scrollable area for leaders
			szPanel_ID = self.getNextWidgetName()
			screen.addPanel(szPanel_ID, "", "", False, True, self.X_LEADERS, self.Y_LEADERS, self.W_LEADERS, self.H_LEADERS, PanelStyles.PANEL_STYLE_MAIN)
	
			listLeaders = []
			for iLoopPlayer in range(gc.getMAX_PLAYERS()):
				player = gc.getPlayer(iLoopPlayer)
				if (player.isAlive() and (gc.getTeam(player.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam()) or gc.getGame().isDebugMode())):
					listLeaders.append(iLoopPlayer)
					
			iNumLeaders = len(listLeaders)
			if iNumLeaders >= self.LEADER_COLUMNS:
				iButtonSize = self.LEADER_BUTTON_SIZE / 2
			else:
				iButtonSize = self.LEADER_BUTTON_SIZE
	
			iColumns = int(self.W_LEADERS / (iButtonSize + self.LEADER_MARGIN))
	
			# loop through all players and display leaderheads
			for iIndex in range(iNumLeaders):
				iLoopPlayer = listLeaders[iIndex]
				player = gc.getPlayer(iLoopPlayer)
				
				x = self.X_LEADERS + self.LEADER_MARGIN + (iIndex % iColumns) * (iButtonSize + self.LEADER_MARGIN)
				y = self.Y_LEADERS + self.LEADER_MARGIN + (iIndex // iColumns) * (iButtonSize + self.LEADER_MARGIN)
	
				if player.isBarbarian():
					szButton = "Art/Interface/Buttons/Civilizations/Barbarian.dds"
				else:
					szButton = gc.getLeaderHeadInfo(gc.getPlayer(iLoopPlayer).getLeaderType()).getButton()
	
				szLeaderButton = self.getLeaderButtonWidget(iLoopPlayer)              #self.getNextWidgetName()
				screen.addCheckBoxGFC(szLeaderButton, szButton, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), x, y, iButtonSize, iButtonSize, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 2, iLoopPlayer, ButtonStyles.BUTTON_STYLE_LABEL)
				screen.setState(szLeaderButton, (iLoopPlayer in self.selectedLeaders))				
		
		self.UL_refreshUnitSelection(bReload, bRedraw)

	def UL_refreshUnitSelection(self, bReload, bRedraw):
		screen = self.getScreen()
		screen.minimapClearAllFlashingTiles()
		
		if (bRedraw):
			iBtn_X = self.X_TEXT + self.MAP_MARGIN
			iBtn_Y = self.Y_TEXT + self.MAP_MARGIN / 2
			iTxt_X = iBtn_X + 22
			iTxt_Y = iBtn_Y + 2
			if (self.bUnitDetails):
				szText = localText.getText("TXT_KEY_MILITARY_ADVISOR_UNIT_TOGGLE_OFF", ())
				screen.setButtonGFC(self.UNIT_BUTTON_ID, u"", "", iBtn_X, iBtn_Y, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
				screen.setLabel(self.UNIT_BUTTON_LABEL_ID, "", szText, CvUtil.FONT_LEFT_JUSTIFY, iTxt_X, iTxt_Y, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				szText = localText.getText("TXT_KEY_MILITARY_ADVISOR_UNIT_TOGGLE_ON", ())
				screen.setButtonGFC(self.UNIT_BUTTON_ID, u"", "", iBtn_X, iBtn_Y, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS )
				screen.setLabel(self.UNIT_BUTTON_LABEL_ID, "", szText, CvUtil.FONT_LEFT_JUSTIFY, iTxt_X, iTxt_Y, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		if bReload:
			self.timer.start()
			_, activePlayer, iActiveTeam, activeTeam = PlayerUtil.getActivePlayerAndTeamAndIDs()
			self.stats = UnitGrouper.GrouperStats(self.grouper)
			for player in PlayerUtil.players(alive=True):
				for unit in PlayerUtil.playerUnits(player):
					plot = unit.plot()
					if plot.isNone():
						continue
					bVisible = plot.isVisible(iActiveTeam, False) and not unit.isInvisible(iActiveTeam, False)
					if not bVisible:
						continue
					if unit.getVisualOwner() in self.selectedLeaders:
						self.stats.processUnit(activePlayer, activeTeam, unit)
			self.timer.log("process units")
		
		iGroupID = 1
		szText = localText.getText("TXT_KEY_PEDIA_ALL_UNITS", ()).upper()
		bAllSelected = iGroupID in self.selectedGroups
		if (bAllSelected):
			szText = localText.changeTextColor(u"<u>" + szText + u"</u>", gc.getInfoTypeForString("COLOR_YELLOW"))
		if (bRedraw):
			screen.addListBoxGFC(self.UNIT_LIST_ID, "", self.X_TEXT + self.MAP_MARGIN, self.Y_TEXT + self.MAP_MARGIN + 15, self.W_TEXT - 2 * self.MAP_MARGIN, self.H_TEXT - 2 * self.MAP_MARGIN - 15, TableStyles.TABLE_STYLE_STANDARD)
			screen.enableSelect(self.UNIT_LIST_ID, False)
			screen.setStyle(self.UNIT_LIST_ID, "Table_StandardCiv_Style")
			screen.appendListBoxString(self.UNIT_LIST_ID, szText, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, iGroupID, CvUtil.FONT_LEFT_JUSTIFY)
		else:
			screen.setListBoxStringGFC(self.UNIT_LIST_ID, 0, szText, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, iGroupID, CvUtil.FONT_LEFT_JUSTIFY)
		
#		for grouping in self.stats.itergroupings():
#			for group in grouping.itergroups():
#				BugUtil.debug("%s / %s : %d (%d)" % (grouping.grouping.title, group.group.title, group.size(), group.isEmpty()))
		
		eYellow = gc.getInfoTypeForString("COLOR_YELLOW")
		eRed = gc.getInfoTypeForString("COLOR_RED")
		eWhite = gc.getInfoTypeForString("COLOR_WHITE")
		grouping1 = self.stats.getGrouping(self.groupingKeys[0])
		grouping2 = self.stats.getGrouping(self.groupingKeys[1])
		BugUtil.debug("Grouping 1 is %s" % grouping1.grouping.title)
		BugUtil.debug("Grouping 2 is %s" % grouping2.grouping.title)
		self.timer.start()
		iItem = 1
		for group1 in grouping1.itergroups():
			if (group1.isEmpty()):
				continue
			units1 = group1.units
			iGroupID += 1
			bGroup1Selected = iGroupID in self.selectedGroups
			szDescription = group1.group.title.upper() + u" (%d)" % len(units1)
			if (bGroup1Selected):
				szDescription = u"   <u>" + szDescription + u"</u>"
			else:
				szDescription = u"   " + szDescription
			if (bGroup1Selected or bAllSelected):
				szDescription = localText.changeTextColor(szDescription, eYellow)
			if (bRedraw):
				screen.appendListBoxString(self.UNIT_LIST_ID, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, iGroupID, CvUtil.FONT_LEFT_JUSTIFY)
			else:
				screen.setListBoxStringGFC(self.UNIT_LIST_ID, iItem, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, iGroupID, CvUtil.FONT_LEFT_JUSTIFY)
			iItem += 1
			bGroup1Selected = bGroup1Selected or bAllSelected
			for group2 in grouping2.itergroups():
				units2 = group2.units & units1
				if (not units2):
					continue
				iGroupID += 1
				bGroup2Selected = iGroupID in self.selectedGroups
				szDescription = group2.group.title + u" (%d)" % len(units2)
				if (bGroup2Selected):
					szDescription = u"      <u>" + szDescription + u"</u>"
				else:
					szDescription = u"      " + szDescription
				if (bGroup2Selected or bGroup1Selected):
					szDescription = localText.changeTextColor(szDescription, eYellow)
				if (bRedraw):
					screen.appendListBoxString(self.UNIT_LIST_ID, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, iGroupID, CvUtil.FONT_LEFT_JUSTIFY)
				else:
					screen.setListBoxStringGFC(self.UNIT_LIST_ID, iItem, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, iGroupID, CvUtil.FONT_LEFT_JUSTIFY)
				iItem += 1
				
				bGroup2Selected = bGroup2Selected or bGroup1Selected
				for unit in units2:
					loopUnit = unit.unit
					bUnitSelected = self.isSelectedUnit(loopUnit.getOwner(), loopUnit.getID())
					if (self.bUnitDetails):
						szDescription = CyGameTextMgr().getSpecificUnitHelp(loopUnit, true, false)

						listMatches = re.findall("<.*?color.*?>", szDescription)	
						for szMatch in listMatches:
							szDescription = szDescription.replace(szMatch, u"")
						
						if (loopUnit.isWaiting()):
							szDescription = '*' + szDescription
						
						if (bUnitSelected):
							szDescription = u"         <u>" + szDescription + u"</u>"
						else:
							szDescription = u"         " + szDescription

						if (bUnitSelected or bGroup2Selected):
							szDescription = localText.changeTextColor(szDescription, eYellow)

						if (bRedraw):
							screen.appendListBoxString(self.UNIT_LIST_ID, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, -loopUnit.getOwner(), loopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						else:
							screen.setListBoxStringGFC(self.UNIT_LIST_ID, iItem, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, -loopUnit.getOwner(), loopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						iItem += 1

					iPlayer = loopUnit.getVisualOwner()
					player = PyPlayer(iPlayer)
					iColor = gc.getPlayerColorInfo(gc.getPlayer(iPlayer).getPlayerColor()).getColorTypePrimary()
					screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_MILITARY, loopUnit.getX(), loopUnit.getY(), iColor, 0.6)
					if (bUnitSelected or bGroup2Selected) and iPlayer in self.selectedLeaders:
						
						if (player.getTeam().isAtWar(gc.getPlayer(self.iActivePlayer).getTeam())):
							iColor = eRed
						elif (gc.getPlayer(iPlayer).getTeam() != gc.getPlayer(self.iActivePlayer).getTeam()):
							iColor = eYellow
						else:
							iColor = eWhite
						screen.minimapFlashPlot(loopUnit.getX(), loopUnit.getY(), iColor, -1)
		self.timer.log("draw unit list")

	def refreshSelectedGroup(self, iSelected):
		if (iSelected in self.selectedGroups):
			self.selectedGroups.remove(iSelected)
		else:
			self.selectedGroups.add(iSelected)
		self.UL_refreshUnitSelection(False, False)
			
	def refreshSelectedUnit(self, iPlayer, iUnitId):
		selectedUnit = (iPlayer, iUnitId)
		if (selectedUnit in self.selectedUnits):
			self.selectedUnits.remove(selectedUnit)
		else:
			self.selectedUnits.add(selectedUnit)
		self.UL_refreshUnitSelection(False, False)		

	def refreshSelectedLeader(self, iPlayer):
		if self.iShiftKeyDown == 1:
			if (iPlayer in self.selectedLeaders):
				self.selectedLeaders.remove(iPlayer)
			else:
				self.selectedLeaders.add(iPlayer)
		else:
			self.selectedLeaders.clear()	
			self.selectedLeaders.add(iPlayer)
	
		self.UL_refresh(True, True)
	
	def isSelectedGroup(self, group):
		if not group:
			return -1 in self.selectedGroups
		return group.group.key in self.selectedGroups

	def isSelectedUnit(self, iPlayer, iUnitId):
		return (iPlayer, iUnitId) in self.selectedUnits


	def drawCombatExperience(self):
	
		if (gc.getPlayer(self.iActivePlayer).greatPeopleThreshold(true) > 0):

			screen = self.getScreen()

			# move GG progress bar to lower panel
			# by stmartin 02.18.09
			iPanel_X = self.X_LINK + self.DX_LINK * 5 / 2 + 20
			iPanel_Y = self.Y_EXIT - 5
			iPanel_W = self.X_EXIT - iPanel_X - 100
			iPanel_H = 45
					
#			szPanel_ID = self.getNextWidgetName()
#			screen.addPanel(szPanel_ID, u"", "", False, False, iPanel_X, iPanel_Y, iPanel_W, iPanel_H, PanelStyles.PANEL_STYLE_MAIN)

			self.X_GREAT_GENERAL_BAR = iPanel_X + 25
			self.Y_GREAT_GENERAL_BAR = iPanel_Y + 8
			self.W_GREAT_GENERAL_BAR = iPanel_W - 50
			self.H_GREAT_GENERAL_BAR = 29
			# end

			iExperience = gc.getPlayer(self.iActivePlayer).getCombatExperience()
			
			szGGBar_ID = self.getNextWidgetName()
			szGGTxt_ID = self.getNextWidgetName()

			screen.addStackedBarGFC(szGGBar_ID, self.X_GREAT_GENERAL_BAR, self.Y_GREAT_GENERAL_BAR, self.W_GREAT_GENERAL_BAR, self.H_GREAT_GENERAL_BAR, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)
			screen.setStackedBarColors(szGGBar_ID, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED"))
			screen.setStackedBarColors(szGGBar_ID, InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE"))
			screen.setStackedBarColors(szGGBar_ID, InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
			screen.setStackedBarColors(szGGBar_ID, InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
			screen.setBarPercentage(szGGBar_ID, InfoBarTypes.INFOBAR_STORED, float(iExperience) / float(gc.getPlayer(self.iActivePlayer).greatPeopleThreshold(true)))

			screen.setLabel(szGGTxt_ID, "", localText.getText("TXT_KEY_MISC_COMBAT_EXPERIENCE", ()), CvUtil.FONT_CENTER_JUSTIFY, self.X_GREAT_GENERAL_BAR + self.W_GREAT_GENERAL_BAR/2, self.Y_GREAT_GENERAL_BAR + 6, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)


	def minimapClicked(self):
		self.hideScreen()

	def getLeaderButtonWidget(self, iPlayer):
		szName = self.LEADER_BUTTON_ID + str(iPlayer)
		return szName


	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName
	
	def deleteAllWidgets(self):
		screen = self.getScreen()
		count = self.nWidgetCount
		self.nWidgetCount = 0
		while (self.nWidgetCount < count):
			screen.deleteWidget(self.getNextWidgetName())
		self.nWidgetCount = 0

		# delete widgets with pre-defined names
		screen.deleteWidget(self.UNIT_BUTTON_ID)
		screen.deleteWidget(self.UNIT_LIST_ID)
		screen.deleteWidget(self.UNIT_BUTTON_LABEL_ID)
		#screen.hide(self.MINIMAP_PANEL)

		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			screen.deleteWidget(self.getLeaderButtonWidget(iLoopPlayer))

		# hide the mini-map
		#self.UL_setMinimapVisibility(screen, False)

		# clear the grid
		if self.iconGrid:
			self.iconGrid.hideGrid()
			self.iconGrid = None

	# handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getFunctionName() == self.UNIT_LOC_TAB_ID):
				self.iScreen = UNIT_LOCATION_SCREEN
				self.showUnitLocation()
				return 1

			elif (inputClass.getFunctionName() == self.SIT_REP_TAB_ID):
				self.iScreen = SITUATION_REPORT_SCREEN
				self.showSituationReport()
				return 1

			elif (inputClass.getFunctionName() == self.STRAT_ADV_TAB_ID):
				self.iScreen = STRATEGIC_ADVANTAGES_SCREEN
				self.showStrategicAdvantages()
				return 1

			elif (inputClass.getFunctionName() == self.UNIT_BUTTON_ID):
				self.bUnitDetails = not self.bUnitDetails
				self.UL_refreshUnitSelection(True, True)
				return 1

			# RJG Start - following line added as per RJG (http://forums.civfanatics.com/showpost.php?p=6997192&postcount=16)
			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_LEADERHEAD or BugDll.isWidgetVersion(2, inputClass.getButtonType(), "WIDGET_LEADERHEAD_RELATIONS")):
				if (inputClass.getFlags() & MouseFlags.MOUSE_RBUTTONUP):
					if (self.iActivePlayer != inputClass.getData1()):
						self.getScreen().hideScreen()
						return 1
			# RJG End
		
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER):
			if (inputClass.getData() == int(InputTypes.KB_LSHIFT)
			or  inputClass.getData() == int(InputTypes.KB_RSHIFT)):
				self.iShiftKeyDown = inputClass.getID()
				return 1

		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED ):
			if self.iScreen == UNIT_LOCATION_SCREEN:
				iSelected = inputClass.getData()
				control = inputClass.getFunctionName() + str(inputClass.getID())
				BugUtil.debug("Selected item %d from list %s" % (iSelected, control))
				if control in self.groupDropDowns:
					iGroup = self.groupDropDowns.index(control)
					key = self.grouper[iSelected].key
					self.groupingKeys[iGroup] = key
					self.selectedGroups.clear()
					BugUtil.debug("Switched grouping %d to %s" % (iGroup, key))
					self.UL_refresh(False, True)
					return 1
			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_LEADERHEAD):
				if (self.iActivePlayer != inputClass.getData1()):
					self.getScreen().hideScreen()
					return 1
		
		if self.iconGrid:
			return self.iconGrid.handleInput(inputClass)
		
		return 0


	def update(self, fDelta):
		return
