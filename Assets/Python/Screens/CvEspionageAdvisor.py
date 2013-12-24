## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
## Improvements to this screen by Almightix - thanks
from CvPythonExtensions import *
from PyHelpers import PyPlayer
import CvUtil
import ScreenInput
import CvScreenEnums

# BUG - Better Espionage - start
import BugCore
import BugUtil
import ColorUtil
import FontUtil
import SpyUtil
import BugScreen
EspionageOpt = BugCore.game.BetterEspionage
# BUG - Better Espionage - end

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

CITYMISSION_CITY = 0
CITYMISSION_MISSION = 1

class CvEspionageAdvisor:

	def __init__(self):
		self.SCREEN_NAME = "EspionageAdvisor"
		self.DEBUG_DROPDOWN_ID =  "EspionageAdvisorDropdownWidget"
		self.WIDGET_ID = "EspionageAdvisorWidget"
		self.WIDGET_HEADER = "EspionageAdvisorWidgetHeader"
		self.EXIT_ID = "EspionageAdvisorExitWidget"
		self.BACKGROUND_ID = "EspionageAdvisorBackground"
		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Y_TITLE = 12
		self.BORDER_WIDTH = 4
		self.PANE_HEIGHT = 450
		self.PANE_WIDTH = 283
		self.X_SLIDERS = 50
		self.X_INCOME = 373
		self.X_EXPENSES = 696
		self.Y_TREASURY = 90
		self.H_TREASURY = 100
		self.Y_LOCATION = 230
		self.Y_SPACING = 30
		self.TEXT_MARGIN = 15
		self.Z_BACKGROUND = -2.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.DZ = -0.2

		self.X_EXIT = 994
		self.Y_EXIT = 726

		self.nWidgetCount = 0

		self.iDirtyBit = 0

		self.iTargetPlayer = -1

		self.iActiveCityID = -1
		self.iActiveMissionID = -1

		self.bShowAISpending = True
		self.ShowAISpendingWidget = ""

		self.drawMissionTabConstantsDone = 0
		self.drawSpyvSpyTabConstantsDone = 0
		self.CityMissionToggle = CITYMISSION_CITY

		self.MissionsTabWidget = self.SCREEN_NAME + "MissionTab"
		self.SpyvSpyTabWidget = self.SCREEN_NAME + "SpyvSpyTab"

		self.iIncreaseButtonID = 555
		self.iDecreaseButtonID = 556
		self.iLeaderImagesID = 456

		# mission / city widgets - initialized to avoid errors with 'handle input'
		# they get set to proper values in def drawMissionTab(self)
		self.szMissionsTitleText = ""
		self.szCitiesTitleText = ""

		self.EPScreenTab = -1

	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.ESPIONAGE_ADVISOR)

	def interfaceScreen (self):
		self.iTargetPlayer = -1
		self.iActiveCityID = -1
		self.iActiveMissionID = -1
		self.iActivePlayer = CyGame().getActivePlayer()

		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen( PopupStates.POPUPSTATE_IMMEDIATE, False)

# attempting to call BugScreen class here

		self.EPScreen = BugScreen.BugScreen(self.SCREEN_NAME, screen, self.W_SCREEN, self.H_SCREEN)
		self.EPScreen.addBackground(self.BACKGROUND_ID, "SCREEN_BG_OPAQUE")
		self.EPScreen.addTitle(self.WIDGET_HEADER, "TXT_KEY_ESPIONAGE_SCREEN", "4b", True, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS)

		bShow = EspionageOpt.isEnabled()
		self.EPScreen.addTab(self.MissionsTabWidget, "TXT_KEY_ESPIONAGE_MISSIONS_TAB", "4", True, 50, self.Y_EXIT, 0, bShow, True, True, self.drawMissionTab, self.refreshMissionTab, WidgetTypes.WIDGET_GENERAL)
		self.EPScreen.addTab(self.SpyvSpyTabWidget, "TXT_KEY_ESPIONAGE_SPYVSPY_TAB", "4", False, 350, self.Y_EXIT, 0, bShow, True, False, self.drawSpyvSpyTab, None, WidgetTypes.WIDGET_GENERAL)
		self.EPScreen.addTab(self.EXIT_ID, "TXT_KEY_PEDIA_SCREEN_EXIT", "4", True, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, True, True, False, None, None, WidgetTypes.WIDGET_CLOSE_SCREEN)
		self.EPScreen.evenlySpaceTabs()

		if (self.EPScreenTab == -1
		or self.EPScreenTab == 1):
			self.EPScreen.updateTabStatus(self.MissionsTabWidget)
			self.EPScreenTab = 1
		elif self.EPScreenTab == 2:
			self.EPScreen.updateTabStatus(self.SpyvSpyTabWidget)
			self.EPScreenTab = 2

		self.EPScreen.draw()

		if (CyGame().isDebugMode()):
			self.iDebugDropdownID = 554
			self.szDropdownName = self.DEBUG_DROPDOWN_ID
			screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, self.iDebugDropdownID, -1, FontTypes.GAME_FONT)
			for j in range(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getCivilizationShortDescription(0), j, j, False )

		# draw the contents
		self.drawContents()

	def drawContents(self):

		self.deleteAllWidgets()

		screen = self.getScreen()

		if not EspionageOpt.isEnabled():
			self.CityMissionToggle = CITYMISSION_CITY
			self.EPScreen.updateTabStatus(self.MissionsTabWidget)

		# draw tab details
		self.EPScreen.drawActiveTab()
		self.EPScreen.refreshActiveTab()

		# draw tabs
		self.EPScreen.drawTabs()

	def drawMissionTab(self):
		screen = self.getScreen()

#		BugUtil.debug("CvEspionage Advisor: drawMissionsTab")

		pActivePlayer = gc.getPlayer(self.iActivePlayer)
		pActiveTeam = gc.getTeam(pActivePlayer.getTeam())

		self.drawMissionTabConstants()

		self.szLeftPaneWidget = self.getNextWidgetName()
		screen.addPanel( self.szLeftPaneWidget, "", "", true, true,
			self.X_LEFT_PANE, self.Y_LEFT_PANE, self.W_LEFT_PANE, self.H_LEFT_PANE, PanelStyles.PANEL_STYLE_MAIN)

		self.szScrollPanel = self.getNextWidgetName()
		screen.addPanel( self.szScrollPanel, "", "", true, true,
			self.X_SCROLL, self.Y_SCROLL, self.W_SCROLL, self.H_SCROLL, PanelStyles.PANEL_STYLE_EMPTY)

		self.aiKnownPlayers = []
		self.aiUnknownPlayers = []
		self.iNumEntries= 0

		for iLoop in range(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iLoop)
			if (pPlayer.getTeam() != pActivePlayer.getTeam() and not pPlayer.isBarbarian() and not pPlayer.isMinorCiv()):
				if (pPlayer.isAlive()):
					if (pActiveTeam.isHasMet(pPlayer.getTeam())):
						self.aiKnownPlayers.append(iLoop)
						self.iNumEntries = self.iNumEntries + 1

						if (self.iTargetPlayer == -1):
							self.iTargetPlayer = iLoop

		while(self.iNumEntries < 17):
			self.iNumEntries = self.iNumEntries + 1
			self.aiUnknownPlayers.append(self.iNumEntries)

		############################
		#### Total EPs Per Turn Text
		############################

		if not EspionageOpt.isEnabled():
			self.szTotalPaneWidget = self.getNextWidgetName()
			screen.addPanel( self.szTotalPaneWidget, "", "", true, true,
				self.X_TOTAL_PANE, self.Y_TOTAL_PANE, self.W_TOTAL_PANE, self.H_TOTAL_PANE, PanelStyles.PANEL_STYLE_MAIN )

			self.szMakingText = self.getNextWidgetName()
			szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_TOTAL_NUM_EPS", (pActivePlayer.getCommerceRate(CommerceTypes.COMMERCE_ESPIONAGE), )) + "</font>"
			screen.setLabel(self.szMakingText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_MAKING_TEXT, self.Y_MAKING_TEXT, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		############################
		#### Right Panel
		############################

		self.szRightPaneWidget = self.getNextWidgetName()
		screen.addPanel( self.szRightPaneWidget, "", "", true, true,
			self.X_RIGHT_PANE, self.Y_RIGHT_PANE, self.W_RIGHT_PANE, self.H_RIGHT_PANE, PanelStyles.PANEL_STYLE_MAIN )

		if (self.iTargetPlayer != -1):
			self.szCitiesTitleText = self.getNextWidgetName()
			if self.CityMissionToggle == CITYMISSION_CITY:
				szText = u"<font=4>" + localText.getText("TXT_KEY_CONCEPT_CITIES", ()) + "</font>"
			else:
				szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_MISSIONS", ()) + "</font>"

			if EspionageOpt.isEnabled():
				szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_YELLOW"))
				screen.setText(self.szCitiesTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_CITY_LIST, self.Y_CITY_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			else:
				screen.setLabel(self.szCitiesTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_CITY_LIST, self.Y_CITY_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			self.szEffectsTitleText = self.getNextWidgetName()
			szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_PASSIVE_EFFECTS", ()) + "</font>"
			screen.setLabel(self.szEffectsTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_EFFECTS_LIST, self.Y_EFFECTS_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			self.szMissionsTitleText = self.getNextWidgetName()
			if self.CityMissionToggle == CITYMISSION_MISSION:
				szText = u"<font=4>" + localText.getText("TXT_KEY_CONCEPT_CITIES", ()) + "</font>"
			else:
				szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_MISSIONS", ()) + "</font>"

			if EspionageOpt.isEnabled():
				szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_YELLOW"))
				screen.setText(self.szMissionsTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_MISSIONS_LIST, self.Y_MISSIONS_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			else:
				screen.setLabel(self.szMissionsTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_MISSIONS_LIST, self.Y_MISSIONS_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			self.szEffectsCostTitleText = self.getNextWidgetName()
			szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_COST", ()) + "</font>"
			screen.setLabel(self.szEffectsCostTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_EFFECTS_COSTS_LIST, self.Y_EFFECTS_COSTS_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			self.szMissionsCostTitleText = self.getNextWidgetName()
			szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_COST", ()) + "</font>"
			screen.setLabel(self.szMissionsCostTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_MISSIONS_COSTS_LIST, self.Y_MISSIONS_COSTS_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			############################
			#### Left Leaders Panel
			############################

			self.drawMissionTab_LeftLeaderPanal(screen)

		return

	def drawMissionTabConstants(self):

		# skip this is we have already done it
		if EspionageOpt.isEnabled():
			if self.drawMissionTabConstantsDone == 2:
				return
		else:
			if self.drawMissionTabConstantsDone == 1:
				return

		if EspionageOpt.isEnabled():
			self.drawMissionTabConstantsDone = 2
		else:
			self.drawMissionTabConstantsDone = 1

		self.MissionLeaderPanel_X_LeaderIcon = 21
		self.MissionLeaderPanel_X_LeaderNamePanel = 5
		self.MissionLeaderPanel_X_LeaderName = 55
		self.MissionLeaderPanel_X_Multiplier = 190
		self.MissionLeaderPanel_X_CounterEP = 220
		self.MissionLeaderPanel_X_EPoints = 300
		self.MissionLeaderPanel_X_PassiveMissions = 380
		self.MissionLeaderPanel_X_WghtInc = 53
		self.MissionLeaderPanel_X_WghtDec = 68
		self.MissionLeaderPanel_X_Wght = 85
		self.MissionLeaderPanel_X_EPointsTurn = self.MissionLeaderPanel_X_EPoints + 4
		self.MissionLeaderPanel_X_EspionageIcon = 3

		if EspionageOpt.isEnabled():
			self.MissionLeaderPanel_X_EPointsTurn = self.MissionLeaderPanel_X_EPoints + 4
		else:
			self.MissionLeaderPanel_X_EPointsTurn = 247

		self.MissionLeaderPanelTopRow = 0
		self.MissionLeaderPanelBottomRow = 15
		self.MissionLeaderPanelMiddle = 6

		# mission constants
		for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
			pMission = gc.getEspionageMissionInfo(iMissionLoop)
			if (pMission.getCost() != -1
			and pMission.isPassive()):
				if pMission.isInvestigateCity():
					self.MissionInvestigateCity = iMissionLoop
				elif pMission.isSeeDemographics():
					self.MissionSeeDemo = iMissionLoop
				elif pMission.isSeeResearch():
					self.MissionSeeResearch = iMissionLoop
				else:
					self.MissionCityVisibility = iMissionLoop

		if EspionageOpt.isEnabled():
			self.X_LEFT_PANE = 25
			self.Y_LEFT_PANE = 70 - 5
			self.W_LEFT_PANE = 400 + 60
			self.H_LEFT_PANE = 620

			self.X_SCROLL = self.X_LEFT_PANE + 20
			self.Y_SCROLL= 90 - 5
			self.W_SCROLL= 360 + 60
			self.H_SCROLL= 580

			############################
			#### Right Panel
			############################

			self.X_RIGHT_PANE = self.X_LEFT_PANE + self.W_LEFT_PANE + 10
			self.Y_RIGHT_PANE = self.Y_LEFT_PANE
			self.W_RIGHT_PANE = 550 - 50
			self.H_RIGHT_PANE = self.H_LEFT_PANE

			self.X_CITY_LIST = self.X_RIGHT_PANE + 20
			self.Y_CITY_LIST = self.Y_RIGHT_PANE + 60
			self.W_CITY_LIST = 160
			self.H_CITY_LIST = self.H_RIGHT_PANE - 90

			self.X_EFFECTS_LIST = self.X_CITY_LIST + self.W_CITY_LIST + 10
			self.Y_EFFECTS_LIST = self.Y_CITY_LIST
			self.W_EFFECTS_LIST = 210
			self.H_EFFECTS_LIST = 100

			self.X_EFFECTS_COSTS_LIST = self.X_EFFECTS_LIST + self.W_EFFECTS_LIST + 10
			self.Y_EFFECTS_COSTS_LIST = self.Y_EFFECTS_LIST
			self.W_EFFECTS_COSTS_LIST = 60
			self.H_EFFECTS_COSTS_LIST = self.H_EFFECTS_LIST

			self.X_MISSIONS_LIST = self.X_CITY_LIST + self.W_CITY_LIST + 10
			self.Y_MISSIONS_LIST = self.Y_EFFECTS_LIST + self.H_EFFECTS_LIST + 50
			self.W_MISSIONS_LIST = self.W_EFFECTS_LIST
			self.H_MISSIONS_LIST = self.H_CITY_LIST -  + self.H_EFFECTS_LIST - 50

			self.X_MISSIONS_COSTS_LIST = self.X_MISSIONS_LIST + self.W_MISSIONS_LIST + 10
			self.Y_MISSIONS_COSTS_LIST = self.Y_MISSIONS_LIST
			self.W_MISSIONS_COSTS_LIST = self.W_EFFECTS_COSTS_LIST
			self.H_MISSIONS_COSTS_LIST = self.H_MISSIONS_LIST

			############################
			#### Left Leaders Panel
			############################

			self.W_LEADER = 128
			self.H_LEADER = 128

			self.W_NAME_PANEL = 220
			self.H_NAME_PANEL = 30

		else:
			self.X_LEFT_PANE = 25
			self.Y_LEFT_PANE = 70
			self.W_LEFT_PANE = 400
			self.H_LEFT_PANE = 620

			self.X_SCROLL = self.X_LEFT_PANE + 20
			self.Y_SCROLL= 90
			self.W_SCROLL= 360
			self.H_SCROLL= 580

			############################
			#### Total EPs Per Turn Text
			############################

			self.X_TOTAL_PANE = self.X_LEFT_PANE + self.W_LEFT_PANE + 20
			self.Y_TOTAL_PANE = self.Y_LEFT_PANE
			self.W_TOTAL_PANE = 550
			self.H_TOTAL_PANE = 60

			self.X_MAKING_TEXT = 490
			self.Y_MAKING_TEXT = 85

			############################
			#### Right Panel
			############################

			self.X_RIGHT_PANE = self.X_TOTAL_PANE
			self.Y_RIGHT_PANE = self.Y_TOTAL_PANE + self.H_TOTAL_PANE + 20
			self.W_RIGHT_PANE = self.W_TOTAL_PANE
			self.H_RIGHT_PANE = self.H_LEFT_PANE - self.H_TOTAL_PANE - 20

			self.X_CITY_LIST = self.X_RIGHT_PANE + 40
			self.Y_CITY_LIST = self.Y_RIGHT_PANE + 60
			self.W_CITY_LIST = 160
			self.H_CITY_LIST = self.H_RIGHT_PANE - 90

			self.X_EFFECTS_LIST = self.X_CITY_LIST + self.W_CITY_LIST + 20
			self.Y_EFFECTS_LIST = self.Y_CITY_LIST
			self.W_EFFECTS_LIST = 210
			self.H_EFFECTS_LIST = (self.H_CITY_LIST / 3) - 50

			self.X_EFFECTS_COSTS_LIST = self.X_EFFECTS_LIST + self.W_EFFECTS_LIST + 10
			self.Y_EFFECTS_COSTS_LIST = self.Y_EFFECTS_LIST
			self.W_EFFECTS_COSTS_LIST = 60
			self.H_EFFECTS_COSTS_LIST = self.H_EFFECTS_LIST

			self.X_MISSIONS_LIST = self.X_CITY_LIST + self.W_CITY_LIST + 20
			self.Y_MISSIONS_LIST = self.Y_EFFECTS_LIST + self.H_EFFECTS_LIST + 50
			self.W_MISSIONS_LIST = self.W_EFFECTS_LIST
			self.H_MISSIONS_LIST = (self.H_CITY_LIST * 2 / 3) #- 45

			self.X_MISSIONS_COSTS_LIST = self.X_MISSIONS_LIST + self.W_MISSIONS_LIST + 10
			self.Y_MISSIONS_COSTS_LIST = self.Y_MISSIONS_LIST
			self.W_MISSIONS_COSTS_LIST = self.W_EFFECTS_COSTS_LIST
			self.H_MISSIONS_COSTS_LIST = self.H_MISSIONS_LIST

			############################
			#### Left Leaders Panel
			############################

			self.W_LEADER = 128
			self.H_LEADER = 128

			self.W_NAME_PANEL = 220
			self.H_NAME_PANEL = 30

		return

	def drawMissionTab_LeftLeaderPanal(self, screen):
		pActivePlayer = gc.getPlayer(self.iActivePlayer)
		pActiveTeam = gc.getTeam(pActivePlayer.getTeam())

		# the following are needed for each leader
		self.MissionLeaderPanelWidgets = [""] * gc.getMAX_PLAYERS()  # updated by refresh
		self.EPWeightWidgets = [""] * gc.getMAX_PLAYERS()     # updated by refresh
		self.EPSpendingWidgets = [""] * gc.getMAX_PLAYERS()   # updated by refresh
		self.EPIconWidgets = [""] * gc.getMAX_PLAYERS()       # updated by refresh
		self.LeaderImageWidgets = [""] * gc.getMAX_PLAYERS()  # updated by handle input

		# The following only occur once
		self.CityListBoxWidget = self.getNextWidgetName()     # updated by refresh
		self.EffectsTableWidget = self.getNextWidgetName()    # updated by refresh
		self.MissionsTableWidget = self.getNextWidgetName()   # updated by refresh

		# only required for BUG
		if EspionageOpt.isEnabled():
			iRatioColor = EspionageOpt.getDefaultRatioColor()
			iGoodRatioColor = EspionageOpt.getGoodRatioColor()
			iBadRatioColor = EspionageOpt.getBadRatioColor()

			# show AI spending toggle
			self.ShowAISpendingWidget = self.getNextWidgetName()
			szText = u"<font=2>" + localText.getText("TXT_KEY_ESPIONAGE_AI_SPENDING_TOGGLE", ()) + "</font>"
			if self.bShowAISpending:
				szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_YELLOW"))
			screen.setText(self.ShowAISpendingWidget, "Background", szText, CvUtil.FONT_RIGHT_JUSTIFY, self.X_LEFT_PANE + self.W_LEFT_PANE - 20, self.Y_LEFT_PANE + 8, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		for iPlayerID in self.aiKnownPlayers:
			pTargetPlayer = gc.getPlayer(iPlayerID)
			iTargetTeam = pTargetPlayer.getTeam()

			# leader panel / container
			szLeaderPanel = self.getNextWidgetName()
			self.MissionLeaderPanelWidgets[iPlayerID] = szLeaderPanel

			screen.attachPanel(self.szScrollPanel, szLeaderPanel, "", "", True, False, PanelStyles.PANEL_STYLE_STANDARD)

			# EP Spending, Weight. EP Icon - all of these are handled by the 'refresh' procedure
			self.EPWeightWidgets[iPlayerID] = self.getNextWidgetName()
			self.EPSpendingWidgets[iPlayerID] = self.getNextWidgetName()
			self.EPIconWidgets[iPlayerID] = self.getNextWidgetName()

			# leader image
			szName = self.getNextWidgetName()
			screen.attachSeparator(szLeaderPanel, szName, true, 30)

			szName = self.getNextWidgetName()
			self.LeaderImageWidgets[iPlayerID] = szName  # updated by handle input so needs to be stored

			screen.addCheckBoxGFCAt(szLeaderPanel, szName, gc.getLeaderHeadInfo(gc.getPlayer(iPlayerID).getLeaderType()).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				self.MissionLeaderPanel_X_LeaderIcon, self.MissionLeaderPanelTopRow, 32, 32, WidgetTypes.WIDGET_GENERAL, self.iLeaderImagesID, iPlayerID, ButtonStyles.BUTTON_STYLE_LABEL, False)
			if (self.iTargetPlayer == iPlayerID):
				screen.setState(szName, true)

			# leader name
			szName = self.getNextWidgetName()
			screen.attachPanelAt( szLeaderPanel, szName, "", "", true, false, PanelStyles.PANEL_STYLE_MAIN,
				self.MissionLeaderPanel_X_LeaderNamePanel, self.MissionLeaderPanelTopRow, self.W_NAME_PANEL, self.H_NAME_PANEL, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			szName = self.getNextWidgetName()

			if EspionageOpt.isEnabled():
				szTempBuffer = u"<color=%d,%d,%d,%d>%s</color>" %(pTargetPlayer.getPlayerTextColorR(), pTargetPlayer.getPlayerTextColorG(), pTargetPlayer.getPlayerTextColorB(), pTargetPlayer.getPlayerTextColorA(), pTargetPlayer.getCivilizationShortDescription(0))
			else:
				szMultiplier = self.getEspionageMultiplierText(self.iActivePlayer, iPlayerID)
				szTempBuffer = u"<color=%d,%d,%d,%d>%s (%s)</color>" %(pTargetPlayer.getPlayerTextColorR(), pTargetPlayer.getPlayerTextColorG(), pTargetPlayer.getPlayerTextColorB(), pTargetPlayer.getPlayerTextColorA(), pTargetPlayer.getCivilizationShortDescription(0), szMultiplier)

			szText = u"<font=2>" + szTempBuffer + "</font>"
			screen.setLabelAt( szName, szLeaderPanel, szText, 0, self.MissionLeaderPanel_X_LeaderName, self.MissionLeaderPanelTopRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# EPoints Multiplier
			if EspionageOpt.isEnabled():
				iMultiplier = self.getEspionageMultiplier(self.iActivePlayer, iPlayerID)
				szName = self.getNextWidgetName()
				szText = u"<font=2>%i%s</font>" %(iMultiplier, "%")

				if (iBadRatioColor >= 0 and iMultiplier >= EspionageOpt.getBadRatioCutoff()):
					szText = localText.changeTextColor(szText, iBadRatioColor)
				elif (iGoodRatioColor >= 0 and iMultiplier <= EspionageOpt.getGoodRatioCutoff()):
					szText = localText.changeTextColor(szText, iGoodRatioColor)
				elif (iRatioColor >= 0):
					szText = localText.changeTextColor(szText, iRatioColor)

				screen.setLabelAt( szName, szLeaderPanel, szText, CvUtil.FONT_RIGHT_JUSTIFY, self.MissionLeaderPanel_X_Multiplier, self.MissionLeaderPanelTopRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# EPoints Multiplier Against
			if (EspionageOpt.isEnabled()
			and EspionageOpt.isShowCalculatedInformation()
			and self.bShowAISpending):
				iMultiplier = self.getEspionageMultiplier(iPlayerID, self.iActivePlayer)
				szName = self.getNextWidgetName()
				szText = u"<font=2>%i%s</font>" %(iMultiplier, "%")
				screen.setLabelAt( szName, szLeaderPanel, szText, CvUtil.FONT_RIGHT_JUSTIFY, self.MissionLeaderPanel_X_Multiplier, self.MissionLeaderPanelBottomRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# Counter Espionage (both for and against)
			if EspionageOpt.isEnabled():
				# for
				iCounterEsp = self.getCounterEspionageTurnsLeft(self.iActivePlayer, iPlayerID)
				self.showCounterEspionage(screen, szLeaderPanel, iCounterEsp, self.MissionLeaderPanelTopRow)

				# against
				if self.bShowAISpending:
					iCounterEsp = self.getCounterEspionageTurnsLeft(iPlayerID, self.iActivePlayer)
					self.showCounterEspionage(screen, szLeaderPanel, iCounterEsp, self.MissionLeaderPanelBottomRow)

			# EPs
			szName = self.getNextWidgetName()
			iPlayerEPs = self.getPlayerEPs(self.iActivePlayer, iPlayerID)
			szText = u"<font=2>" + localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS", (iPlayerEPs ,)) + "</font>"
			screen.setLabelAt( szName, szLeaderPanel, szText, CvUtil.FONT_RIGHT_JUSTIFY, self.MissionLeaderPanel_X_EPoints, self.MissionLeaderPanelTopRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# EPs Against
			if (EspionageOpt.isEnabled()
			and self.bShowAISpending):
				szName = self.getNextWidgetName()  #"PointsAgainstText%d" %(iPlayerID)
				iTargetEPs = self.getPlayerEPs(iPlayerID, self.iActivePlayer)
				szText = u"<font=2>" + localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS", (iTargetEPs, )) + "</font>"
				screen.setLabelAt( szName, szLeaderPanel, szText, CvUtil.FONT_RIGHT_JUSTIFY, self.MissionLeaderPanel_X_EPoints, self.MissionLeaderPanelBottomRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# EP Spending Against (Points per turn)
			if (EspionageOpt.isEnabled()
			and self.bShowAISpending):
				szName = self.getNextWidgetName()  #"AmountAgainstText%d" %(iPlayerID)
				iSpending = SpyUtil.getDifferenceByPlayer(iPlayerID, self.iActivePlayer)
				if (iSpending is None
				or iSpending == 0):
					szText = u""
				else:
					if iSpending > 0:
						szText = u"<font=2>(+%i)</font>" %(iSpending)
						szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_GREEN"))
					else:
						szText = u"<font=2>(%i)</font>" %(iSpending)
						szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_YELLOW"))
				screen.setLabelAt( szName, szLeaderPanel, szText, CvUtil.FONT_LEFT_JUSTIFY, self.MissionLeaderPanel_X_EPointsTurn, self.MissionLeaderPanelBottomRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# EP Weights
			iSize = 16
			szName = self.getNextWidgetName()
			screen.setImageButtonAt( szName, szLeaderPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_PLUS").getPath(), self.MissionLeaderPanel_X_WghtInc, self.MissionLeaderPanelBottomRow, iSize, iSize, WidgetTypes.WIDGET_GENERAL, self.iIncreaseButtonID, iPlayerID );
			szName = self.getNextWidgetName()
			screen.setImageButtonAt( szName, szLeaderPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_MINUS").getPath(), self.MissionLeaderPanel_X_WghtDec, self.MissionLeaderPanelBottomRow, iSize, iSize, WidgetTypes.WIDGET_GENERAL, self.iDecreaseButtonID, iPlayerID );

			# Symbols for 'Demographics' and 'Research'
			if EspionageOpt.isEnabled():
				# Active Player
				iDemoCost = pActivePlayer.getEspionageMissionCost(self.MissionSeeDemo, iPlayerID, None, -1)
				iTechCost = pActivePlayer.getEspionageMissionCost(self.MissionSeeResearch, iPlayerID, None, -1)
				self.showPassiveMissionIcons(screen, szLeaderPanel, iPlayerEPs, iDemoCost, iTechCost, self.MissionLeaderPanelTopRow)

				# Target Player
				if (EspionageOpt.isShowCalculatedInformation()
				and self.bShowAISpending):
					iDemoCost = pTargetPlayer.getEspionageMissionCost(self.MissionSeeDemo, self.iActivePlayer, None, -1)
					iTechCost = pTargetPlayer.getEspionageMissionCost(self.MissionSeeResearch, self.iActivePlayer, None, -1)
					self.showPassiveMissionIcons(screen, szLeaderPanel, iTargetEPs, iDemoCost, iTechCost, self.MissionLeaderPanelBottomRow)

		for iPlayerID in self.aiUnknownPlayers:
			szLeaderPanel = self.getNextWidgetName()
			szName = self.getNextWidgetName()
			screen.attachPanel(self.szScrollPanel, szLeaderPanel, "", "", True, False, PanelStyles.PANEL_STYLE_STANDARD)
			screen.attachSeparator(szLeaderPanel, szName, true, 30)




	def getEspionageMultiplier(self, iCurrentPlayer, iTargetPlayer):
		pCurrentPlayer = gc.getPlayer(iCurrentPlayer)
		iCurrentTeamID = pCurrentPlayer.getTeam()
		pTargetPlayer = gc.getPlayer(iTargetPlayer)
		iTargetTeamID = pTargetPlayer.getTeam()

		iMultiplier = getEspionageModifier(iCurrentTeamID, iTargetTeamID)
		return iMultiplier

	def getEspionageMultiplierText(self, iCurrentPlayer, iTargetPlayer):
		pCurrentPlayer = gc.getPlayer(iCurrentPlayer)
		iCurrentTeamID = pCurrentPlayer.getTeam()
		pTargetPlayer = gc.getPlayer(iTargetPlayer)
		iTargetTeamID = pTargetPlayer.getTeam()

		iMultiplier = getEspionageModifier(iCurrentTeamID, iTargetTeamID)
		szMultiplier = localText.getText("TXT_KEY_ESPIONAGE_COST", (iMultiplier, ))

		if self.getCounterEspionageTurnsLeft(iCurrentPlayer, iTargetPlayer) > 0:
			szMultiplier += u"*"

		if self.getCounterEspionageTurnsLeft(iTargetPlayer, iCurrentPlayer) > 0:
			szMultiplier += u"+"

		return szMultiplier

	def getCounterEspionageTurnsLeft(self, iCurrentPlayer, iTargetPlayer):
		pCurrentTeam = gc.getTeam(gc.getPlayer(iCurrentPlayer).getTeam())
		iTargetTeamID = gc.getPlayer(iTargetPlayer).getTeam()

		iCurrentCounterEsp = pCurrentTeam.getCounterespionageTurnsLeftAgainstTeam(iTargetTeamID)
		return iCurrentCounterEsp

	def showCounterEspionage(self, screen, szLeaderPanel, iCounterEspTurns, iRow):
		szName = self.getNextWidgetName()
		if iCounterEspTurns > 0:
			szText = u"<font=2>[%i]</font>" %(iCounterEspTurns)
		else:
			szText = u""
		screen.setLabelAt(szName, szLeaderPanel, szText, CvUtil.FONT_RIGHT_JUSTIFY, self.MissionLeaderPanel_X_CounterEP, iRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	def showPassiveMissionIcons(self, screen, szLeaderPanel, iEPoints, iDemoCost, iTechCost, iRow):
		# can see demographics icon
		if iEPoints >= iDemoCost:
			szText = FontUtil.getChar("ss life support")
		else:
			szText = FontUtil.getChar("space")

		# can see research icon
		if iEPoints >= iTechCost:
			szText += FontUtil.getChar("commerce research")
		else:
			szText += FontUtil.getChar("space")

		szName = self.getNextWidgetName()
		screen.setLabelAt(szName, szLeaderPanel, szText, CvUtil.FONT_LEFT_JUSTIFY, self.MissionLeaderPanel_X_PassiveMissions, iRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );






	def refreshMissionTab(self):
		if (self.iTargetPlayer != -1):
			# Create a new screen, called EspionageAdvisor, using the file EspionageAdvisor.py for input
			screen = self.getScreen()

			pActivePlayer = gc.getPlayer(self.iActivePlayer)
			pActiveTeam = gc.getTeam(pActivePlayer.getTeam())

			for iPlayerID in self.aiKnownPlayers:
				self.refreshMissionTab_LeftLeaderPanel(screen, pActivePlayer, iPlayerID)

			# Is there any other players which have been met?
			if (self.iTargetPlayer != -1):
				pTargetPlayer = gc.getPlayer(self.iTargetPlayer)
				pyTargetPlayer = PyPlayer(self.iTargetPlayer)

				# List of Cities
				screen.addListBoxGFC(self.CityListBoxWidget, "", self.X_CITY_LIST, self.Y_CITY_LIST, self.W_CITY_LIST, self.H_CITY_LIST, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(self.CityListBoxWidget, True)
				screen.setStyle(self.CityListBoxWidget, "Table_StandardCiv_Style")

				if self.CityMissionToggle == CITYMISSION_CITY:
					# Loop through target's cities, see which are visible and add them to the list
					apCityList = pyTargetPlayer.getCityList()

					iLoop = 0
					for pyCity in apCityList:
						pCity = pyCity.GetCy()
						szCityName = self.getCityNameText(pCity, self.iActivePlayer, self.iTargetPlayer)

						if ((EspionageOpt.isEnabled()
							and pCity.isRevealed(pActivePlayer.getTeam(), false))
						or (not EspionageOpt.isEnabled()
							and pCity.isRevealed(pActivePlayer.getTeam(), false))):
							screen.appendListBoxString(self.CityListBoxWidget, szCityName, WidgetTypes.WIDGET_GENERAL, pCity.getID(), 0, CvUtil.FONT_LEFT_JUSTIFY )

							if (self.iActiveCityID == -1 or pTargetPlayer.getCity(self.iActiveCityID).isNone()):
								self.iActiveCityID = pCity.getID()

							if (self.iActiveCityID == pCity.getID()):
								screen.setSelectedListBoxStringGFC(self.CityListBoxWidget, iLoop)

							iLoop += 1

				elif self.CityMissionToggle == CITYMISSION_MISSION:
					# active missions only
					iLoop = 0
					for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
						pMission = gc.getEspionageMissionInfo(iMissionLoop)
						if (pMission.getCost() != -1):
							if pMission.isTargetsCity():
								screen.appendListBoxString(self.CityListBoxWidget, pMission.getDescription(), WidgetTypes.WIDGET_GENERAL, iMissionLoop, 0, CvUtil.FONT_LEFT_JUSTIFY )

								if (self.iActiveMissionID == -1):
									self.iActiveMissionID = iMissionLoop

								if (self.iActiveMissionID == iMissionLoop):
									screen.setSelectedListBoxStringGFC(self.CityListBoxWidget, iLoop)

								iLoop += 1

				self.W_TABLE_0 = self.W_EFFECTS_LIST
				self.W_TABLE_1 = 0
				self.W_TABLE_2 = self.W_EFFECTS_COSTS_LIST
				self.W_TABLE_3 = 20

				szHelpText = localText.getText("TXT_KEY_ESPIONAGE_PASSIVE_AUTOMATIC", ())
				screen.addTableControlGFCWithHelp(self.EffectsTableWidget, 4, self.X_EFFECTS_LIST, self.Y_EFFECTS_LIST, self.W_EFFECTS_LIST + self.W_EFFECTS_COSTS_LIST + self.W_TABLE_1 + self.W_TABLE_3, self.H_EFFECTS_LIST, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD, szHelpText)
				screen.setTableColumnHeader(self.EffectsTableWidget, 0, "", self.W_TABLE_0)
				screen.setTableColumnHeader(self.EffectsTableWidget, 1, "", self.W_TABLE_1)
				screen.setTableColumnHeader(self.EffectsTableWidget, 2, "", self.W_TABLE_2)
				screen.setTableColumnHeader(self.EffectsTableWidget, 3, "", self.W_TABLE_3)

				if self.CityMissionToggle == CITYMISSION_CITY:
					szHelpText = localText.getText("TXT_KEY_ESPIONAGE_MISSIONS_SPY", ())
				else:
					szHelpText = ""
				screen.addTableControlGFCWithHelp(self.MissionsTableWidget, 4, self.X_MISSIONS_LIST, self.Y_MISSIONS_LIST, self.W_MISSIONS_LIST + self.W_MISSIONS_COSTS_LIST + self.W_TABLE_1 + self.W_TABLE_3, self.H_MISSIONS_LIST, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD, szHelpText)
				screen.setTableColumnHeader(self.MissionsTableWidget, 0, "", self.W_TABLE_0)
				screen.setTableColumnHeader(self.MissionsTableWidget, 1, "", self.W_TABLE_1)
				screen.setTableColumnHeader(self.MissionsTableWidget, 2, "", self.W_TABLE_2)
				screen.setTableColumnHeader(self.MissionsTableWidget, 3, "", self.W_TABLE_3)

				# Loop through passive Missions
				for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
					pMission = gc.getEspionageMissionInfo(iMissionLoop)
					if (pMission.getCost() != -1):
						if (pMission.isPassive()):
							if (self.CityMissionToggle == CITYMISSION_CITY
							or (self.CityMissionToggle == CITYMISSION_MISSION
							and not pMission.isTargetsCity())):
								szTable = self.EffectsTableWidget
								szText, szCost = self.getTableTextCost(self.iActivePlayer, self.iTargetPlayer, iMissionLoop, self.iActiveCityID)
								iRow = screen.appendTableRow(szTable)
								screen.setTableText(szTable, 0, iRow, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
								screen.setTableText(szTable, 2, iRow, szCost, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

				if self.CityMissionToggle == CITYMISSION_CITY:
					# Loop through active Missions
					# Primary list is cities, secondary list is missions
					for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
						pMission = gc.getEspionageMissionInfo(iMissionLoop)
						if (pMission.getCost() != -1):
							if (not pMission.isPassive()):
								szTable = self.MissionsTableWidget
								szText, szCost = self.getTableTextCost(self.iActivePlayer, self.iTargetPlayer, iMissionLoop, self.iActiveCityID)
								iRow = screen.appendTableRow(szTable)
								screen.setTableText(szTable, 0, iRow, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
								screen.setTableText(szTable, 2, iRow, szCost, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

				elif self.CityMissionToggle == CITYMISSION_MISSION:
					# Loop through target's cities, see which are visible and add them to the list
					# Primary list is missions, secondary list is cities
					apCityList = pyTargetPlayer.getCityList()

					for pyCity in apCityList:
						pCity = pyCity.GetCy()
						if (pCity.isRevealed(pActivePlayer.getTeam(), false)):

							szTable = self.MissionsTableWidget
							szText, szCost = self.getTableTextCost(self.iActivePlayer, self.iTargetPlayer, self.iActiveMissionID, pCity.getID())
							iRow = screen.appendTableRow(szTable)
							screen.setTableText(szTable, 0, iRow, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							if (pCity.isRevealed(pActivePlayer.getTeam(), false)):
								screen.setTableText(szTable, 2, iRow, szCost, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

		return 0

	def refreshMissionTab_LeftLeaderPanel(self, screen, pActivePlayer, iPlayerID):
		pTargetPlayer = gc.getPlayer(iPlayerID)
		iTargetTeam = pTargetPlayer.getTeam()

		szLeaderPanel = self.MissionLeaderPanelWidgets[iPlayerID]
		szEPWeight = self.EPWeightWidgets[iPlayerID]
		szEPSpending = self.EPSpendingWidgets[iPlayerID]
		szEPIcon = self.EPIconWidgets[iPlayerID]

		# EP Weight
		szText = u"<font=2>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_SPENDING_WEIGHT", ()) + ": %d</font>" %(pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam))
		screen.setLabelAt(szEPWeight, szLeaderPanel, szText, 0, self.MissionLeaderPanel_X_Wght, self.MissionLeaderPanelBottomRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

		# EP Spending (Points per turn)
		iSpending = pActivePlayer.getEspionageSpending(iTargetTeam)
		if EspionageOpt.isEnabled():
			iY = self.MissionLeaderPanelTopRow
			if (iSpending > 0):
				szText = u"<font=2>(+%i)</font>" %(iSpending)
				szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_GREEN"))
			else:
				szText = u""
		else:
			iY = self.MissionLeaderPanelBottomRow
			if (iSpending > 0):
				szText = u"<font=2><color=0,255,0,0>%s</color></font>" %(localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS_PER_TURN", (iSpending, )))
			else:
				szText = u"<font=2><color=192,0,0,0>%s</color></font>" %(localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS_PER_TURN", (iSpending, )))
		screen.setLabelAt(szEPSpending, szLeaderPanel, szText, CvUtil.FONT_LEFT_JUSTIFY, self.MissionLeaderPanel_X_EPointsTurn, iY, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

		# Espionage Icon
		if (iSpending > 0):
			szText = u"<font=2>%c</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
		else:
			szText = u""
		screen.setLabelAt(szEPIcon, szLeaderPanel, szText, 0, self.MissionLeaderPanel_X_EspionageIcon, self.MissionLeaderPanelMiddle, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );


	def getCityNameText(self, pCity, iActivePlayer, iTargetPlayer):
		if not EspionageOpt.isEnabled():
			return pCity.getName()

		szCityName = pCity.getName()
		iPlayerEPs = self.getPlayerEPs(iActivePlayer, iTargetPlayer)
		pActivePlayer = gc.getPlayer(iActivePlayer)
		pPlot = pCity.plot()

		if not pCity.isRevealed(pActivePlayer.getTeam(), false):
			szCityName = "-- %s --" %(szCityName)

		return szCityName

	def getPlayerEPs(self, iCurrentPlayer, iTargetPlayer):
		pCurrentPlayer = gc.getPlayer(iCurrentPlayer)
		pCurrentTeam = gc.getTeam(pCurrentPlayer.getTeam())
		pTargetPlayer = gc.getPlayer(iTargetPlayer)
		iTargetTeam = pTargetPlayer.getTeam()
		EPs = pCurrentTeam.getEspionagePointsAgainstTeam(iTargetTeam)
		return EPs

	def getTableTextCost(self, iActivePlayer, iTargetPlayer, iMission, iCity):

		pActivePlayer = gc.getPlayer(iActivePlayer)
		pActiveTeam = gc.getTeam(pActivePlayer.getTeam())
		pTargetPlayer = gc.getPlayer(iTargetPlayer)
		pMission = gc.getEspionageMissionInfo(iMission)

		szText = ""
		szCost = ""

		if pMission.getCost() == -1:
			return szText, szCost

		iTargetTeam = pTargetPlayer.getTeam()
		iPlayerEPs = self.getPlayerEPs(iActivePlayer, iTargetPlayer)
		if (EspionageOpt.isEnabled()):
			iPossibleColor = EspionageOpt.getPossibleMissionColor()
			iCloseColor = EspionageOpt.getCloseMissionColor()
			iClosePercent = EspionageOpt.getCloseMissionPercent()
		else:
			iPossibleColor = -1
			iCloseColor = -1
			iClosePercent = -1

		pPlot = None
		szCityName= ""
		bHideCost = False
		if (iCity != -1
		and pMission.isTargetsCity()):
			pActiveCity = gc.getPlayer(iTargetPlayer).getCity(iCity)
			pPlot = pActiveCity.plot()
			szCityName = pActiveCity.getName()
			szCityName = self.getCityNameText(pActiveCity, iActivePlayer, iTargetPlayer)
			if not pActiveCity.isRevealed(pActivePlayer.getTeam(), false):
				bHideCost = True

		if not bHideCost:
			iCost = pActivePlayer.getEspionageMissionCost(iMission, iTargetPlayer, pPlot, -1)
		else:
			iCost = 0

		if (self.CityMissionToggle == CITYMISSION_CITY # secondary list is mission names
		or (pMission.isPassive()
		and not pMission.isTargetsCity())):
			szTechText = ""
			if (pMission.getTechPrereq() != -1):
				szTechText = " (%s)" %(gc.getTechInfo(pMission.getTechPrereq()).getDescription())

			szText = pMission.getDescription() + szTechText
		else: # secondary list is city names
			szText = szCityName

		if iCost > 0:
			szCost = unicode(str(iCost))
			if (EspionageOpt.isEnabled()):
				if (iPossibleColor >= 0 and iPlayerEPs >= iCost):
					szCost = localText.changeTextColor(szCost, iPossibleColor)
					szText = localText.changeTextColor(szText, iPossibleColor)
				elif (iCloseColor >= 0 and iPlayerEPs >= (iCost * float(100 - iClosePercent) / 100)):
					szCost = localText.changeTextColor(szCost, iCloseColor)
					szText = localText.changeTextColor(szText, iCloseColor)

		if (pMission.getTechPrereq() != -1):
			pTeam = gc.getTeam(pActivePlayer.getTeam())
			if (not pTeam.isHasTech(pMission.getTechPrereq())):
				szText = u"<color=255,0,0,0>%s</color>" %(szText)
				return szText, szCost

		return szText, szCost



	def drawSpyvSpyTab(self):
		screen = self.getScreen()

#		BugUtil.debug("CvEspionage Advisor: drawSpyvSpyTab")

		pActivePlayer = gc.getPlayer(self.iActivePlayer)
		pActiveTeam = gc.getTeam(pActivePlayer.getTeam())

		self.aiKnownPlayers = []
		self.aiUnknownPlayers = []

		# add current player
		self.aiKnownPlayers.append(self.iActivePlayer)
		self.iNumEntries = 1

		# add known players
		for iLoop in range(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iLoop)
			if (self.iActivePlayer != iLoop
			and not pPlayer.isBarbarian() and not pPlayer.isMinorCiv()):
				if (pPlayer.isAlive()):
					if (pActiveTeam.isHasMet(pPlayer.getTeam())):
						self.aiKnownPlayers.append(iLoop)
						self.iNumEntries = self.iNumEntries + 1

		# fill out to 16 possible players
		while(self.iNumEntries < 16):
			self.iNumEntries = self.iNumEntries + 1
			self.aiUnknownPlayers.append(self.iNumEntries)

		self.drawSpyvSpyTabConstants()

		# add background panel
		self.szSvSPaneWidget = self.getNextWidgetName()
		screen.addPanel(self.szSvSPaneWidget, "", "", true, true,
			self.X_SvS_PANE, self.Y_SvS_PANE, self.W_SvS_PANE, self.H_SvS_PANE, PanelStyles.PANEL_STYLE_MAIN)

		# add scrolling panel
		self.szSvSScrollPanel = self.getNextWidgetName()
		screen.addPanel(self.szSvSScrollPanel, "", "", true, true,
			self.X_SvS_SCROLL, self.Y_SvS_SCROLL, self.W_SvS_SCROLL, self.H_SvS_SCROLL, PanelStyles.PANEL_STYLE_EMPTY)

		# add left column leader panel
		self.szLeftLeaderPanel = self.getNextWidgetName()
		screen.addPanel(self.szLeftLeaderPanel, "", "", true, true,
			self.X_SvS_LEFT_LEADER, self.Y_SvS_LEFT_LEADER, self.W_SvS_LEFT_LEADER, self.H_SvS_LEFT_LEADER, PanelStyles.PANEL_STYLE_STANDARD)

		# add top column leader panel
		self.szTopLeaderPanel = self.getNextWidgetName()
		screen.addPanel(self.szTopLeaderPanel, "", "", true, true,
			self.X_SvS_TOP_LEADER, self.Y_SvS_TOP_LEADER, self.W_SvS_TOP_LEADER, self.H_SvS_TOP_LEADER, PanelStyles.PANEL_STYLE_STANDARD)

		iRow = 0
		for iRowPlayerID in self.aiKnownPlayers:
			iRow += 1

			sLeaderButton = gc.getLeaderHeadInfo(gc.getPlayer(iRowPlayerID).getLeaderType()).getButton()

			# left leader icon
			screen.setImageButton(self.getNextWidgetName(), sLeaderButton,
								  self.X_SvS_LEFT_LEADER + 2, self.Y_SvS_LEFT_LEADER + (iRow - 1) * self.H_SvS_CELL + 3, self.SvS_IconSize, self.SvS_IconSize, WidgetTypes.WIDGET_LEADERHEAD, iRowPlayerID, -1)

			# show total EP spending over the last turn
			iSpending = SpyUtil.getSpending(iRowPlayerID, self.iActivePlayer)
			szText = self.formatSpending(iSpending)
			iX = self.X_SvS_LEFT_LEADER + self.W_SvS_LEFT_LEADER - 10
			iY = self.Y_SvS_LEFT_LEADER + (iRow - 1) * self.H_SvS_CELL + self.H_SvS_CELL / 2 - 6
			screen.setLabel(self.getNextWidgetName(), "", szText, CvUtil.FONT_RIGHT_JUSTIFY, iX, iY, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# top leader icon
			screen.setImageButton(self.getNextWidgetName(), sLeaderButton,
								  self.X_SvS_TOP_LEADER + (iRow - 1) * self.W_SvS_CELL + self.W_SvS_CELL / 2 - self.SvS_IconSize / 2, self.Y_SvS_TOP_LEADER + 3, self.SvS_IconSize, self.SvS_IconSize, WidgetTypes.WIDGET_LEADERHEAD, iRowPlayerID, -1)

			# add a horizontal panel to make the table easier to read
			if iRow % 2 == 0: # every even number
				iY = self.Y_SvS_LEFT_LEADER + (iRow - 1) * self.H_SvS_CELL
				screen.addPanel(self.getNextWidgetName(), "", "", true, true,
					self.X_SvS_TOP_LEADER, iY, self.W_SvS_TOP_LEADER, self.H_SvS_TOP_LEADER, PanelStyles.PANEL_STYLE_STANDARD)

			iCol = 0
			for iColPlayerID in self.aiKnownPlayers:
				iCol += 1

				pActivePlayer = gc.getPlayer(self.iActivePlayer)
				pActiveTeamID = pActivePlayer.getTeam()
				pActiveTeam = gc.getTeam(pActiveTeamID)

				pColPlayer = gc.getPlayer(iColPlayerID)
				pColTeamID = pColPlayer.getTeam()
				pColTeam = gc.getTeam(pColTeamID)

				pRowPlayer = gc.getPlayer(iRowPlayerID)
				pRowTeamID = pRowPlayer.getTeam()
				pRowTeam = gc.getTeam(pRowTeamID)

				if pColTeamID == pRowTeamID: # rol and col player are on the same team
					continue

				# check that everyone has met - show the EP spending
				if (pActiveTeam.isHasMet(pColPlayer.getTeam())
				and pActiveTeam.isHasMet(pRowPlayer.getTeam())
				and pColTeam.isHasMet(pRowPlayer.getTeam())):
					# EPs per turn
					iSpending = SpyUtil.getDifferenceByPlayer(iRowPlayerID, iColPlayerID)
					szText = self.formatSpending(iSpending)
					iX = self.X_SvS_TOP_LEADER + (iCol - 1) * self.W_SvS_CELL + self.W_SvS_CELL / 2
					iY = self.Y_SvS_LEFT_LEADER + (iRow - 1) * self.H_SvS_CELL + self.H_SvS_CELL / 2 - 6
					screen.setLabel(self.getNextWidgetName(), "", szText, CvUtil.FONT_CENTER_JUSTIFY, iX, iY, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

		return




	def drawSpyvSpyTabConstants(self):
		# don't skip this segment as some of the constants are dynamic :)

		# skip this is we have already done it
#		if self.drawSpyvSpyTabConstantsDone == 1:
#			return
		self.drawSpyvSpyTabConstantsDone = 1

		self.X_SvS_PANE = 5
		self.Y_SvS_PANE = 45
		self.W_SvS_PANE = self.W_SCREEN - 2 * self.X_SvS_PANE
		self.H_SvS_PANE = self.H_SCREEN - 2 * self.Y_SvS_PANE

#		self.H_SCREEN = 768

		self.X_SvS_SCROLL = self.X_SvS_PANE + 10
		self.Y_SvS_SCROLL = self.Y_SvS_PANE + 10
		self.W_SvS_SCROLL = self.W_SvS_PANE - 20
		self.H_SvS_SCROLL = self.H_SvS_PANE - 20

		iNumPlayers = len(self.aiKnownPlayers)
		if iNumPlayers > 12:
			self.W_SvS_CELL = 50
			self.H_SvS_CELL = 35
			self.SvS_IconSize = 32
		elif iNumPlayers >= 9:
			self.W_SvS_CELL = 70
			self.H_SvS_CELL = 50
			self.SvS_IconSize = 48
		else:
			self.W_SvS_CELL = 100
			self.H_SvS_CELL = 70
			self.SvS_IconSize = 64

		self.X_SvS_LEFT_LEADER = self.X_SvS_SCROLL
		self.Y_SvS_LEFT_LEADER = self.Y_SvS_SCROLL + self.H_SvS_CELL
		self.W_SvS_LEFT_LEADER = 2 * self.W_SvS_CELL
		self.H_SvS_LEFT_LEADER = self.H_SvS_CELL * len(self.aiKnownPlayers)

		self.X_SvS_TOP_LEADER = self.X_SvS_SCROLL + self.W_SvS_LEFT_LEADER
		self.Y_SvS_TOP_LEADER = self.Y_SvS_SCROLL
		self.W_SvS_TOP_LEADER = self.W_SvS_CELL * len(self.aiKnownPlayers)
		self.H_SvS_TOP_LEADER = self.H_SvS_CELL

	def formatSpending(self, iSpending):
		if iSpending == 0:
			return u"<font=2>-</font>"
		elif iSpending > 0:
			return localText.changeTextColor(u"<font=2>+%i</font>" %(iSpending), gc.getInfoTypeForString("COLOR_GREEN"))
		else:
			return localText.changeTextColor(u"<font=2>%i</font>" %(iSpending), gc.getInfoTypeForString("COLOR_YELLOW"))


	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	def deleteAllWidgets(self):
		screen = self.getScreen()
		i = self.nWidgetCount - 1
		while (i >= 0):
			self.nWidgetCount = i
			screen.deleteWidget(self.getNextWidgetName())
			i -= 1

		self.nWidgetCount = 0

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		'Calls function mapped in EspionageAdvisorInputMap'

		screen = self.getScreen()
		pActivePlayer = gc.getPlayer(self.iActivePlayer)
		icFunctionName = inputClass.getFunctionName()

		##### Debug Dropdown #####
		if (CyGame().isDebugMode()):
			if (icFunctionName == self.DEBUG_DROPDOWN_ID):
				iIndex = screen.getSelectedPullDownID(self.DEBUG_DROPDOWN_ID)
				self.iActivePlayer = screen.getPullDownData(self.DEBUG_DROPDOWN_ID, iIndex)
				self.drawContents()
				CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)

		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if self.EPScreen.getActiveTab() == self.MissionsTabWidget:
				if (("%s%d" %(icFunctionName, inputClass.getID()) == self.szMissionsTitleText
				or   "%s%d" %(icFunctionName, inputClass.getID()) == self.szCitiesTitleText)
				and EspionageOpt.isEnabled()):
					if self.CityMissionToggle == CITYMISSION_MISSION:
						self.CityMissionToggle = CITYMISSION_CITY
						self.drawContents()
						return 0
					else:
						self.CityMissionToggle = CITYMISSION_MISSION
						self.drawContents()
						return 0
				if "%s%d" %(icFunctionName, inputClass.getID()) == self.ShowAISpendingWidget:  # toggle show AI spending
#					BugUtil.debug("CvEspionage Advisor: toggle show AI spending")
					self.bShowAISpending = not self.bShowAISpending
					self.drawContents()
					return 0

			if (icFunctionName == self.MissionsTabWidget):
#				BugUtil.debug("CvEspionage Advisor: Change to Mission Tab")
				self.EPScreen.updateTabStatus(self.MissionsTabWidget)
				self.EPScreenTab = 1
				self.drawContents()
				return 0
			elif (icFunctionName == self.SpyvSpyTabWidget):
#				BugUtil.debug("CvEspionage Advisor: Change to Spy v Spy Tab")
				self.EPScreen.updateTabStatus(self.SpyvSpyTabWidget)
				self.EPScreenTab = 2
				self.drawContents()
				return 0

		if (self.iTargetPlayer != -1):
			##### Player Images #####
			if (inputClass.getData1() == self.iLeaderImagesID):
				self.iTargetPlayer = inputClass.getData2()

				# Loop through all images
				for iPlayerID in self.aiKnownPlayers:
					szName = "LeaderImage%d" %(iPlayerID)
					szName = self.LeaderImageWidgets[iPlayerID]
					if (self.iTargetPlayer == iPlayerID):
						screen.setState(szName, true)
					else:
						screen.setState(szName, false)

					self.iActiveCityID = -1

				CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)
				return 0

			##### City Listbox #####
			if ("%s%d" %(icFunctionName, inputClass.getID()) == self.CityListBoxWidget):
				if self.CityMissionToggle == CITYMISSION_CITY:
					iCityID = inputClass.getData1()
					self.iActiveCityID = iCityID
					CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)
				else:
					self.iActiveMissionID = inputClass.getData1()
					CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)
				return 0

			# EP spending weight adjustments
			##### Increase Button #####
			if (inputClass.getData1() == self.iIncreaseButtonID):
				iPlayerID = inputClass.getData2()
				iTargetTeam = gc.getPlayer(iPlayerID).getTeam()

				CyMessageControl().sendEspionageSpendingWeightChange(iTargetTeam, 1)
				CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)
				return 0

			##### Decrease Button #####
			elif (inputClass.getData1() == self.iDecreaseButtonID):
				iPlayerID = inputClass.getData2()
				iTargetTeam = gc.getPlayer(iPlayerID).getTeam()

				if (pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam) > 0):	# Can't reduce weight below 0
					CyMessageControl().sendEspionageSpendingWeightChange(iTargetTeam, -1)
					CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)
				return 0

		return 0

	def update(self, fDelta):
		if (CyInterface().isDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT) == True):
			CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, False)
			self.EPScreen.refreshActiveTab()
		return
