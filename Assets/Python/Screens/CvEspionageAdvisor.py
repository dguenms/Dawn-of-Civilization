from CvPythonExtensions import *
import CvScreenEnums
import CvUtil

from Consts import *

gc = CyGlobalContext()

localText = CyTranslator()

class CvEspionageAdvisor:
	def __init__(self):

		self.W_SCREEN = 1024
		self.H_SCREEN = 640

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

		self.ICON_SIZE = 48
		self.MARGIN_SIZE = 10
		self.WEIGHT_BUTTON_SIZE = self.ICON_SIZE / 3
		self.LINE_SPACING = (self.ICON_SIZE / 3) + 1

		self.X_LEFT_PANE = self.MARGIN_SIZE
		self.Y_LEFT_PANE = self.Y_TOP_PANEL + self.H_TOP_PANEL + self.MARGIN_SIZE + 3
		self.W_LEFT_PANE = 460
		self.H_LEFT_PANE = self.Y_BOTTOM_PANEL - self.Y_LEFT_PANE - self.MARGIN_SIZE - 4

		self.X_PLAYER_INFO = self.ICON_SIZE + 5
		self.Y_PLAYER_INFO = -1
		self.W_PLAYER_INFO = self.W_LEFT_PANE - 40
		self.H_PLAYER_INFO = self.ICON_SIZE + 12

		self.X_RIVAL_STATS = self.W_PLAYER_INFO - 120 	# Left Side
		self.X_PLAYER_STATS = self.W_PLAYER_INFO - 20	# Right Side
		
		self.X_GREAT_SPY_BAR = self.X_LEFT_PANE + self.W_LEFT_PANE
		self.Y_GREAT_SPY_BAR = self.Y_TOP_PANEL + self.H_TOP_PANEL + self.MARGIN_SIZE - 5
		self.W_GREAT_SPY_BAR = self.W_SCREEN - self.X_GREAT_SPY_BAR - 10
		self.H_GREAT_SPY_BAR = 32
		
		self.X_RIGHT_PANE = self.X_GREAT_SPY_BAR
		self.Y_RIGHT_PANE = self.Y_GREAT_SPY_BAR + self.H_GREAT_SPY_BAR
		self.W_RIGHT_PANE = self.W_GREAT_SPY_BAR
		self.H_RIGHT_PANE = self.Y_BOTTOM_PANEL - self.Y_RIGHT_PANE - self.MARGIN_SIZE

		self.X_CITY_LIST = self.X_RIGHT_PANE + 20
		self.Y_CITY_LIST = self.Y_RIGHT_PANE + 20
		self.W_CITY_LIST = 250
		self.H_CITY_LIST = self.H_RIGHT_PANE - 76

		self.X_PASSIVE_MISSIONS = self.X_CITY_LIST + self.W_CITY_LIST + 20
		self.Y_PASSIVE_MISSIONS = self.Y_CITY_LIST
		self.W_PASSIVE_MISSIONS = self.W_RIGHT_PANE - self.W_CITY_LIST - 60
		self.H_PASSIVE_MISSIONS = 144

		self.X_ACTIVE_MISSIONS = self.X_PASSIVE_MISSIONS
		self.Y_ACTIVE_MISSIONS = self.Y_CITY_LIST + self.H_PASSIVE_MISSIONS + 20
		self.W_ACTIVE_MISSIONS = self.W_PASSIVE_MISSIONS
		self.H_ACTIVE_MISSIONS = self.H_RIGHT_PANE - self.H_PASSIVE_MISSIONS - 60

		self.X_GO_TO_CITY = self.X_CITY_LIST - 2
		self.Y_GO_TO_CITY = self.Y_CITY_LIST + self.H_CITY_LIST + 8
		self.W_GO_TO_CITY = 120
		self.H_GO_TO_CITY = 31

		self.W_INVESTIGATE_CITY = self.W_GO_TO_CITY
		self.H_INVESTIGATE_CITY = self.H_GO_TO_CITY
		self.X_INVESTIGATE_CITY = self.X_CITY_LIST + self.W_CITY_LIST - self.W_INVESTIGATE_CITY + 2
		self.Y_INVESTIGATE_CITY = self.Y_GO_TO_CITY

		self.X_WEIGHT_RESET = self.X_BOTTOM_PANEL + self.MARGIN_SIZE + 5
		self.Y_WEIGHT_RESET = self.Y_BOTTOM_PANEL + 17
		self.W_WEIGHT_RESET = 120
		self.H_WEIGHT_RESET = 31

		self.X_WEIGHT_INCREMENT = self.X_WEIGHT_RESET + self.W_WEIGHT_RESET + self.MARGIN_SIZE
		self.Y_WEIGHT_INCREMENT = self.Y_WEIGHT_RESET
		self.W_WEIGHT_INCREMENT = 120

		self.X_EXIT = self.W_BOTTOM_PANEL - 25
		self.Y_EXIT = self.Y_BOTTOM_PANEL + 20

		self.iTargetPlayer = -1
		self.iTargetCity = -1
		self.iMission = 3	# City Visibility
		self.iIncrement = 1
		self.CitySpies = []



	def getScreen(self):
		return CyGInterfaceScreen("EspionageAdvisor", CvScreenEnums.ESPIONAGE_ADVISOR)



	def interfaceScreen (self):
		self.iActivePlayer = CyGame().getActivePlayer()
		self.pActivePlayer = gc.getPlayer(self.iActivePlayer)
		self.iActiveTeam = self.pActivePlayer.getTeam()
		self.pActiveTeam = gc.getTeam(self.iActiveTeam)

		screen = self.getScreen()
		if screen.isActive():
			return

		screen.setRenderInterfaceOnly(True)
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.addDDSGFC("EspionageBackground", CyArtFileMgr().getInterfaceArtInfo('SCREEN_BG_OPAQUE').getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel("EspionageTopPanel", u"", u"", True, False, self.X_TOP_PANEL, self.Y_TOP_PANEL, self.W_TOP_PANEL, self.H_TOP_PANEL, PanelStyles.PANEL_STYLE_TOPBAR)
		screen.addPanel("EspionageBottomPanel", u"", u"", True, False, self.X_BOTTOM_PANEL, self.Y_BOTTOM_PANEL, self.W_BOTTOM_PANEL, self.H_BOTTOM_PANEL, PanelStyles.PANEL_STYLE_BOTTOMBAR)
		screen.setLabel("EspionageTitle", "Background", u"<font=4b>ESPIONAGE ADVISOR</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_TITLE, self.Y_TITLE, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText("EspionageExit", "Background", u"<font=4>EXIT</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

		screen.addPanel("RightPane", "", "", False, False, self.X_RIGHT_PANE, self.Y_RIGHT_PANE, self.W_RIGHT_PANE, self.H_RIGHT_PANE, PanelStyles.PANEL_STYLE_MAIN)

		# Weight Reset
		screen.setButtonGFC("WeightResetButton", "Reset Weights", "", self.X_WEIGHT_RESET, self.Y_WEIGHT_RESET, self.W_WEIGHT_RESET, self.H_WEIGHT_RESET, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

		# Weight Increment
		screen.addDropDownBoxGFC("WeightIncrementSelect", self.X_WEIGHT_INCREMENT, self.Y_WEIGHT_INCREMENT, self.W_WEIGHT_INCREMENT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		i = 1
		while i < 101:
			screen.addPullDownString("WeightIncrementSelect", "(+/-) " + str(i), i, i, self.iIncrement == i)
			if str(i)[0] == "1":
				i *= 5
			else:
				i *= 2

		# Debug Player Select
		if CyGame().isDebugMode():
			screen.addDropDownBoxGFC("DebugPlayerSelect", self.W_SCREEN - 220, 12, 200, WidgetTypes.WIDGET_GENERAL, 554, -1, FontTypes.GAME_FONT)
			for iPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
				if gc.getPlayer(iPlayer).isAlive():
					screen.addPullDownString("DebugPlayerSelect", gc.getPlayer(iPlayer).getName(), iPlayer, iPlayer, False)

		self.updateLeftPanel()
		self.updateRightPanel()
			
		# Leoreth: draw espionage experience bar
		self.drawEspionageExperience()



	def updateLeftPanel(self):
		''
		screen = self.getScreen()
		screen.addPanel("EspionageHeader", u"", u"", True, False, self.X_LEFT_PANE + 8, self.Y_LEFT_PANE, self.W_PLAYER_INFO, 24, PanelStyles.PANEL_STYLE_IN)

		if self.pActivePlayer.isCommerceFlexible(CommerceTypes.COMMERCE_ESPIONAGE):
			screen.setButtonGFC("EspionagePlus", "", "", self.X_LEFT_PANE + 17, self.Y_LEFT_PANE + 1, 20, 20, WidgetTypes.WIDGET_GENERAL, CommerceTypes.COMMERCE_ESPIONAGE, gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_PLUS)
			screen.setButtonGFC("EspionageMinus", "", "", self.X_LEFT_PANE + 37, self.Y_LEFT_PANE + 1, 20, 20, WidgetTypes.WIDGET_GENERAL, CommerceTypes.COMMERCE_ESPIONAGE, -gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_MINUS)

		szRivalLabel = CyTranslator().changeTextColor("vs. You", gc.getInfoTypeForString('COLOR_SELECTED_TEXT'))
		screen.setLabel("EspionageRivalLabel", "EspionageHeader", u"<font=2>" + szRivalLabel + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_RIVAL_STATS + 20, self.Y_LEFT_PANE + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		szPlayerLabel = CyTranslator().changeTextColor("vs. Them", gc.getInfoTypeForString('COLOR_SELECTED_TEXT'))
		screen.setLabel("EspionagePlayerLabel", "EspionageHeader", u"<font=2>" + szPlayerLabel + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_PLAYER_STATS + 20, self.Y_LEFT_PANE + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addScrollPanel("EspionageTable", "", self.X_LEFT_PANE, self.Y_LEFT_PANE + 16, self.W_LEFT_PANE, self.H_LEFT_PANE - 40, PanelStyles.PANEL_STYLE_EXTERNAL)

		iSeeEspionage = gc.getInfoTypeForString('ESPIONAGEMISSION_SEE_ESPIONAGE')

		iCount = 0
		for iRival in range(iNumPlayers):
			pRival = gc.getPlayer(iRival)
			iRivalTeam = pRival.getTeam()
			pRivalTeam = gc.getTeam(iRivalTeam)

			if iRivalTeam == self.iActiveTeam:
				continue

			if pRival.isAlive() and self.pActiveTeam.isHasMet(iRivalTeam):
				if self.iTargetPlayer == -1:
					self.iTargetPlayer = iRival

				PlayerPanel = "PlayerPanel" + str(iRival)
				screen.attachPanelAt("EspionageTable", PlayerPanel, "", "", False, True, PanelStyles.PANEL_STYLE_IN, 0, iCount * self.H_PLAYER_INFO, self.W_PLAYER_INFO, self.H_PLAYER_INFO, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Leader Icon
				LeaderIcon = "LeaderIcon" + str(iRival)
				screen.addCheckBoxGFCAt(PlayerPanel, LeaderIcon, gc.getLeaderHeadInfo(pRival.getLeaderType()).getButton(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 0, 0, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_ESPIONAGE_SELECT_PLAYER, iRival, self.iActivePlayer, ButtonStyles.BUTTON_STYLE_LABEL, False)
				screen.setState(LeaderIcon, self.iTargetPlayer == iRival)

				# Leader Info
				szLeaderName =  u"<font=3b>" + pRival.getName() + u"</font>"
				screen.setLabelAt("LeaderName" + str(iRival), PlayerPanel, szLeaderName, CvUtil.FONT_LEFT_JUSTIFY, self.X_PLAYER_INFO, 0, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				szCivName = u"<font=2>" + pRival.getCivilizationDescription(0) + u"</font>"
				screen.setLabelAt("CivName" + str(iRival), PlayerPanel, szCivName, CvUtil.FONT_LEFT_JUSTIFY, self.X_PLAYER_INFO, self.Y_PLAYER_INFO + self.LINE_SPACING, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Weight Buttons
				screen.setImageButtonAt("WeightIncrease" + str(iRival), PlayerPanel, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_PLUS").getPath(), self.X_PLAYER_INFO, self.Y_PLAYER_INFO + (self.LINE_SPACING * 2), self.WEIGHT_BUTTON_SIZE, self.WEIGHT_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, iRivalTeam + 1, self.iIncrement)
				screen.setImageButtonAt("WeightDecrease" + str(iRival), PlayerPanel, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_MINUS").getPath(), self.X_PLAYER_INFO + self.WEIGHT_BUTTON_SIZE, self.Y_PLAYER_INFO + (self.LINE_SPACING * 2), self.WEIGHT_BUTTON_SIZE, self.WEIGHT_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, iRivalTeam + 1, self.iIncrement)

				# Espionage Accumulated
				iRivalAmount = pRivalTeam.getEspionagePointsAgainstTeam(self.iActiveTeam)
				szRivalAmount = u"%s%c" % (self.addComma(iRivalAmount), gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
				screen.setLabelAt("RivalAccumulated" + str(iRival), PlayerPanel, u"<font=2>" + szRivalAmount + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_RIVAL_STATS, self.Y_PLAYER_INFO, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				iPlayerAmount = self.pActiveTeam.getEspionagePointsAgainstTeam(iRivalTeam)
				szPlayerAmount = u"%s%c" % (self.addComma(iPlayerAmount), gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
				screen.setLabelAt("PlayerAccumulated" + str(iRival), PlayerPanel, u"<font=2>" + szPlayerAmount + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_PLAYER_STATS, self.Y_PLAYER_INFO, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Espionage Cost Modifier
				szCost = CyTranslator().changeTextColor("Cost: ", gc.getInfoTypeForString('COLOR_SELECTED_TEXT'))
				szRivalModifier = " - "

				if self.pActivePlayer.canDoEspionageMission(iSeeEspionage, iRival, pRival.getCapitalCity().plot(), -1):
					iRivalModifier = getEspionageModifier(iRivalTeam, self.iActiveTeam)
					iRivalTurns = self.pActiveTeam.getCounterespionageTurnsLeftAgainstTeam(iRivalTeam)
					if iRivalTurns > 0:
						iRivalModifier *= self.pActiveTeam.getCounterespionageModAgainstTeam(iRivalTeam) / 100
						szRivalModifier = CyTranslator().changeTextColor(str(iRivalModifier) + "%", gc.getInfoTypeForString('COLOR_POSITIVE_TEXT'))
						szRivalModifier += u" (%d)" % iRivalTurns
					elif iRivalModifier < 100:
						szRivalModifier = szCost + CyTranslator().changeTextColor(str(iRivalModifier) + "%", gc.getInfoTypeForString('COLOR_NEGATIVE_TEXT'))
					else:
						szRivalModifier = szCost + u"%d%%" % iRivalModifier

				screen.setLabelAt("RivalEspionageMultiplier" + str(iRival), PlayerPanel, u"<font=2>" + szRivalModifier + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_RIVAL_STATS, self.Y_PLAYER_INFO + (self.LINE_SPACING * 2), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				iPlayerModifier = getEspionageModifier(self.iActiveTeam, iRivalTeam)
				iPlayerTurns = pRivalTeam.getCounterespionageTurnsLeftAgainstTeam(self.iActiveTeam)
				if iPlayerTurns > 0:
					iPlayerModifier *= pRivalTeam.getCounterespionageModAgainstTeam(self.iActiveTeam) / 100
					szPlayerModifier = CyTranslator().changeTextColor(str(iPlayerModifier) + "%", gc.getInfoTypeForString('COLOR_NEGATIVE_TEXT'))
					szPlayerModifier += u" (%d)" % iPlayerTurns
				elif iPlayerModifier > 100:
					szPlayerModifier = szCost + CyTranslator().changeTextColor(str(iPlayerModifier) + "%", gc.getInfoTypeForString('COLOR_NEGATIVE_TEXT'))
				else:
					szPlayerModifier = szCost + u"%d%%" % iPlayerModifier

				screen.setLabelAt("PlayerEspionageMultiplier" + str(iRival), PlayerPanel, u"<font=2>" + szPlayerModifier + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_PLAYER_STATS, self.Y_PLAYER_INFO + (self.LINE_SPACING * 2), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				iCount += 1

		self.updateEspionageWeights()



	def updateRightPanel(self):
		screen = self.getScreen()

		iInvestigate = -1
		for iMission in xrange(gc.getNumEspionageMissionInfos()):
			if gc.getEspionageMissionInfo(iMission).isInvestigateCity():
				iInvestigate = iMission

		if self.iTargetPlayer > -1:
			pTargetPlayer = gc.getPlayer(self.iTargetPlayer)
			iEspionage = self.pActiveTeam.getEspionagePointsAgainstTeam(pTargetPlayer.getTeam())

			# City Table
			screen.addTableControlGFC("CityTable", 3, self.X_CITY_LIST, self.Y_CITY_LIST, self.W_CITY_LIST, self.H_CITY_LIST, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
			screen.setTableColumnHeader("CityTable", 0, u"<font=2>Known Cities</font>", self.W_CITY_LIST - 102)
			screen.setTableColumnHeader("CityTable", 1, u"<font=2>Spies</font>", 50)
			screen.setTableColumnHeader("CityTable", 2, u"<font=2>Cost</font>", 50)
			screen.setStyle("CityTable", "Table_StandardCiv_Style")
			screen.enableSelect("CityTable", True)

			(loopCity, iter) = pTargetPlayer.firstCity(False)
			while(loopCity):
				if loopCity.isRevealed(self.iActiveTeam, False):
					iRow = screen.appendTableRow("CityTable")

					if self.iTargetCity == -1:
						self.iTargetCity = loopCity.getID()

					if self.iTargetCity == loopCity.getID():
						screen.selectRow("CityTable", iRow, True)

					# Status
					if loopCity.isCapital():
						szStatus = u"%c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR)
					elif loopCity.isGovernmentCenter():
						szStatus = u"%c" % CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR)
					else:
						szStatus = u"%c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)

					# Name
					szName = loopCity.getName()
					if self.iTargetCity == loopCity.getID():
						szName = CyTranslator().changeTextColor(szName, gc.getInfoTypeForString('COLOR_HIGHLIGHT_TEXT'))

					screen.setTableText("CityTable", 0, iRow, szStatus + szName, "", WidgetTypes.WIDGET_ESPIONAGE_SELECT_CITY, loopCity.getID(), 0, CvUtil.FONT_LEFT_JUSTIFY)

					# Spies
					if self.iTargetCity == loopCity.getID():
						del self.CitySpies[:]

					iNumSpies = 0
					loopPlot = loopCity.plot()
					for iUnit in xrange(loopPlot.getNumUnits()):
						pUnit = loopPlot.getUnit(iUnit)
						if not pUnit.isNone():
							if pUnit.isCounterSpy() and pUnit.getOwner() == self.iActivePlayer:
								iNumSpies += 1
								if self.iTargetCity == loopCity.getID():
									self.CitySpies.append(pUnit)

					if iNumSpies > 0:
						screen.setTableInt("CityTable", 1, iRow, str(iNumSpies), "", WidgetTypes.WIDGET_ESPIONAGE_SELECT_CITY, loopCity.getID(), 0, CvUtil.FONT_RIGHT_JUSTIFY)

					# Mission Cost
					if self.iMission > -1:
						iCost = self.pActivePlayer.getEspionageMissionCost(self.iMission, self.iTargetPlayer, loopPlot, -1)
						if iCost > -1:
							if iEspionage < iCost:
								szCost = CyTranslator().changeTextColor(str(iCost), gc.getInfoTypeForString('COLOR_NEGATIVE_TEXT'))
							else:
								szCost = CyTranslator().changeTextColor(str(iCost), gc.getInfoTypeForString('COLOR_POSITIVE_TEXT'))

							screen.setTableInt("CityTable", 2, iRow, szCost, "", WidgetTypes.WIDGET_ESPIONAGE_SELECT_CITY, loopCity.getID(), 0, CvUtil.FONT_RIGHT_JUSTIFY)

					iRow += 1
				(loopCity, iter) = pTargetPlayer.nextCity(iter, False)

			# Go to City Button
			screen.setButtonGFC("ViewButton", "Go to City", "", self.X_GO_TO_CITY, self.Y_GO_TO_CITY, self.W_GO_TO_CITY, self.H_GO_TO_CITY, WidgetTypes.WIDGET_GO_TO_CITY, self.iTargetPlayer, self.iTargetCity, ButtonStyles.BUTTON_STYLE_STANDARD)
			screen.enable("ViewButton", False)
			if self.iTargetCity > -1:
				screen.enable("ViewButton", True)

			# Investigate City Button
			screen.setButtonGFC("InvestigateButton", "Investigate City", "", self.X_INVESTIGATE_CITY, self.Y_INVESTIGATE_CITY, self.W_INVESTIGATE_CITY, self.H_INVESTIGATE_CITY, WidgetTypes.WIDGET_ZOOM_CITY, self.iTargetPlayer, self.iTargetCity, ButtonStyles.BUTTON_STYLE_STANDARD)
			screen.enable("InvestigateButton", False)
			if self.iTargetCity > -1 and iInvestigate > -1:
				if self.pActivePlayer.canDoEspionageMission(iInvestigate, self.iTargetPlayer, pTargetPlayer.getCity(self.iTargetCity).plot(), -1):
					screen.enable("InvestigateButton", True)

			# Mission Tables
			screen.addTableControlGFC("PassiveTable", 2, self.X_PASSIVE_MISSIONS, self.Y_PASSIVE_MISSIONS, self.W_PASSIVE_MISSIONS, self.H_PASSIVE_MISSIONS, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
			screen.setTableColumnHeader("PassiveTable", 0, u"<font=2>Passive Missions</font>", self.W_PASSIVE_MISSIONS - 62)
			screen.setTableColumnHeader("PassiveTable", 1, u"<font=2>Cost</font>", 60)

			screen.addTableControlGFC("ActiveTable", 2, self.X_ACTIVE_MISSIONS, self.Y_ACTIVE_MISSIONS, self.W_ACTIVE_MISSIONS, self.H_ACTIVE_MISSIONS, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
			screen.setTableColumnHeader("ActiveTable", 0, u"<font=2>Active Missions</font>", self.W_ACTIVE_MISSIONS - 62)
			screen.setTableColumnHeader("ActiveTable", 1, u"<font=2>Cost</font>", 60)

			for iLoopMission in xrange(gc.getNumEspionageMissionInfos()):
				pMission = gc.getEspionageMissionInfo(iLoopMission)
				if iLoopMission == gc.getInfoTypeForString('ESPIONAGEMISSION_SABOTAGE_PROJECT'):
					continue

				if pMission.getCost() > -1:
					pPlot = None
					if self.iTargetCity > -1 and pMission.isTargetsCity():
						pTargetCity = pTargetPlayer.getCity(self.iTargetCity)
						if not pTargetCity.isNone():
							pPlot = pTargetCity.plot()

					if iLoopMission == self.iMission:
						szMission = CyTranslator().changeTextColor(pMission.getDescription(), gc.getInfoTypeForString('COLOR_HIGHLIGHT_TEXT'))
					else:
						szMission = pMission.getDescription()

					iCost = self.pActivePlayer.getEspionageMissionCost(iLoopMission, self.iTargetPlayer, pPlot, -1)
					szCost = ""
					if iEspionage < iCost:
						szCost = CyTranslator().changeTextColor(str(iCost), gc.getInfoTypeForString('COLOR_NEGATIVE_TEXT'))
					elif iCost > -1:
						szCost = CyTranslator().changeTextColor(str(iCost), gc.getInfoTypeForString('COLOR_POSITIVE_TEXT'))

					if pMission.isPassive():
						iRow = screen.appendTableRow("PassiveTable")
						screen.setTableText("PassiveTable", 0, iRow, "<font=2>" + szMission + "</font>", "", WidgetTypes.WIDGET_ESPIONAGE_SELECT_MISSION, iLoopMission, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableInt("PassiveTable", 1, iRow, "<font=2>" + szCost + "</font>", "", WidgetTypes.WIDGET_ESPIONAGE_SELECT_MISSION, iLoopMission, -1, CvUtil.FONT_RIGHT_JUSTIFY)

					else:
						iRow = screen.appendTableRow("ActiveTable")
						screen.setTableText("ActiveTable", 0, iRow, "<font=2>" + szMission + "</font>", "", WidgetTypes.WIDGET_ESPIONAGE_SELECT_MISSION, iLoopMission, -1, CvUtil.FONT_LEFT_JUSTIFY)
						if iCost > 0:
							screen.setTableInt("ActiveTable", 1, iRow, "<font=2>" + szCost + "   </font>", "", WidgetTypes.WIDGET_ESPIONAGE_SELECT_MISSION, iLoopMission, -1, CvUtil.FONT_RIGHT_JUSTIFY)



	def updateEspionageWeights(self):
		screen = self.getScreen()
		screen.enable("EspionagePlus", True)
		screen.enable("EspionageMinus", True)

		self.iActivePlayer = CyGame().getActivePlayer()
		self.pActivePlayer = gc.getPlayer(self.iActivePlayer)
		self.iActiveTeam = self.pActivePlayer.getTeam()
		self.pActiveTeam = gc.getTeam(self.iActiveTeam)

		iEspionagePercent = self.pActivePlayer.getCommercePercent(CommerceTypes.COMMERCE_ESPIONAGE)
		if iEspionagePercent == 100:
			screen.enable("EspionagePlus", False)
		elif iEspionagePercent == 0:
			screen.enable("EspionageMinus", False)

		szEspionagePercent = u"%c:%d%%" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar(), iEspionagePercent)
		szEspionagePercent += CyTranslator().getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", (self.pActivePlayer.getCommerceRate(CommerceTypes.COMMERCE_ESPIONAGE), ))
		screen.setLabel("EspionageInvestment", "EspionageHeader", u"<font=2>" + szEspionagePercent + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_PLAYER_INFO + 20, self.Y_LEFT_PANE + 3, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iSeeEspionage = gc.getInfoTypeForString('ESPIONAGEMISSION_SEE_ESPIONAGE')

		for iRival in xrange(gc.getMAX_CIV_PLAYERS()):
			pRival = gc.getPlayer(iRival)
			iRivalTeam = pRival.getTeam()
			if iRivalTeam == self.iActiveTeam:
				continue
				
			if pRival.isBarbarian() or pRival.isMinorCiv(): continue

			if pRival.isAlive() and self.pActiveTeam.isHasMet(iRivalTeam):
				PlayerPanel = "PlayerPanel" + str(iRival)

				# Espionage Weight
				szWeight = CyTranslator().changeTextColor("Weight: ", gc.getInfoTypeForString('COLOR_SELECTED_TEXT'))
				iWeight = self.pActivePlayer.getEspionageSpendingWeightAgainstTeam(iRivalTeam)
				if iWeight > 0:
					szWeight += CyTranslator().changeTextColor(str(iWeight), gc.getInfoTypeForString('COLOR_POSITIVE_TEXT'))
				else:
					szWeight += str(iWeight)

				screen.setLabelAt("EspionageWeight" + str(iRival), PlayerPanel, u"<font=2>" + szWeight + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_PLAYER_INFO + (self.WEIGHT_BUTTON_SIZE * 2) + 2, self.Y_PLAYER_INFO + (self.LINE_SPACING * 2), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Espionage Rate
				szRivalRate = " - "
				if self.pActivePlayer.canDoEspionageMission(iSeeEspionage, iRival, pRival.getCapitalCity().plot(), -1):
					iRivalRate = pRival.getEspionageSpending(self.iActiveTeam)
					if iRivalRate > 0:
						szRivalRate = u"+%d/Turn" % iRivalRate

				screen.setLabelAt("RivalEspionageRate" + str(iRival), PlayerPanel, u"<font=2>" + szRivalRate + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_RIVAL_STATS, self.Y_PLAYER_INFO + self.LINE_SPACING, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				szPlayerRate = " - "
				iPlayerRate = self.pActivePlayer.getEspionageSpending(iRivalTeam)
				if iPlayerRate > 0:
					if iWeight > 0:
						szPlayerRate = CyTranslator().changeTextColor(u"+%d/Turn" % iPlayerRate, gc.getInfoTypeForString('COLOR_POSITIVE_TEXT'))
					else:
						szPlayerRate = u"+%d/Turn" % iPlayerRate

				screen.setLabelAt("PlayerEspionageRate" + str(iRival), PlayerPanel, u"<font=2>" + szPlayerRate + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_PLAYER_STATS, self.Y_PLAYER_INFO + self.LINE_SPACING, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)



	def changeEspionageWeight(self, iTargetTeam, iChange):
		if iChange < 0:
			if self.pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam) == 0:
				return
			iChange = min(iChange, self.pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam))

		CyMessageControl().sendEspionageSpendingWeightChange(iTargetTeam, iChange)
		CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)



	def resetEspionageWeights(self):
		iActivePlayer = CyGame().getActivePlayer()
		iActiveTeam = CyGame().getActiveTeam()
	
		for iRival in xrange(gc.getMAX_CIV_PLAYERS()):
			pRival = gc.getPlayer(iRival)
			iRivalTeam = pRival.getTeam()
			if iRivalTeam == iActiveTeam:
				continue

			if pRival.isAlive() and gc.getTeam(iActiveTeam).isHasMet(iRivalTeam):
				iChange = -1 * gc.getPlayer(iActivePlayer).getEspionageSpendingWeightAgainstTeam(iRivalTeam)
				CyMessageControl().sendEspionageSpendingWeightChange(iRivalTeam, iChange)

		CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)



	def addComma(self, iValue):
		sTemp = str(iValue)
		sStart = ""
		while len(sTemp) > 0:
			if sTemp[0].isdigit():
				break
			sStart += sTemp[0]
			sTemp = sTemp[1:]
		sEnd = sTemp[-3:]
		while len(sTemp) > 3:
			sTemp = sTemp[:-3]
			sEnd = sTemp[-3:] + "," + sEnd
		return (sStart + sEnd)



	def handleInput(self, inputClass):
		screen = self.getScreen()
		if self.iTargetPlayer > -1:
			if inputClass.getButtonType() == WidgetTypes.WIDGET_ESPIONAGE_SELECT_PLAYER:
				screen.setState("LeaderIcon" + str(self.iTargetPlayer), False)
				self.iTargetPlayer = inputClass.getData1()
				screen.setState("LeaderIcon" + str(self.iTargetPlayer), True)
				self.iTargetCity = -1
				self.updateRightPanel()

			elif inputClass.getFunctionName().startswith("WeightIncrease"):
				self.changeEspionageWeight(inputClass.getData1() - 1, self.iIncrement)

			elif inputClass.getFunctionName().startswith("WeightDecrease"):
				self.changeEspionageWeight(inputClass.getData1() - 1, -self.iIncrement)

		if inputClass.getFunctionName() == "EspionagePlus" or inputClass.getFunctionName() == "EspionageMinus":
			iChange = inputClass.getData2()
			if CyInterface().shiftKey():
				if iChange > 0:
					iChange = 100
				elif iChange < 0:
					iChange = -100

			CyMessageControl().sendModNetMessage(lNetworkEvents['CHANGE_COMMERCE_PERCENT'],  self.iActivePlayer, inputClass.getData1(), iChange, -1)

		elif inputClass.getButtonType() == WidgetTypes.WIDGET_ESPIONAGE_SELECT_CITY:
			self.iTargetCity = inputClass.getData1()
			self.updateRightPanel()

		elif inputClass.getButtonType() == WidgetTypes.WIDGET_ESPIONAGE_SELECT_MISSION:
			iSelectedMission = inputClass.getData1()
			if self.iMission == iSelectedMission:
				self.iMission = -1
			else:
				self.iMission = iSelectedMission

			self.updateRightPanel()

		elif inputClass.getButtonType() == WidgetTypes.WIDGET_GO_TO_CITY:
			screen.hideScreen()
			pCity = gc.getPlayer(inputClass.getData1()).getCity(inputClass.getData2())
			CyCamera().JustLookAtPlot(pCity.plot())
			if len(self.CitySpies) > 0:
				pSelectedUnit = self.CitySpies[0]
				for pSpy in self.CitySpies:
					if not pSpy.hasMoved():
						pSelectedUnit = pSpy
						break
				CyInterface().selectUnit(pSelectedUnit, True, True, False)

		elif inputClass.getButtonType() == WidgetTypes.WIDGET_ZOOM_CITY:
			screen.hideScreen()
			CyInterface().selectCity(gc.getPlayer(inputClass.getData1()).getCity(inputClass.getData2()), True)

		if inputClass.getFunctionName() == "WeightIncrementSelect":
			iIndex = screen.getSelectedPullDownID("WeightIncrementSelect")
			self.iIncrement = screen.getPullDownData("WeightIncrementSelect", iIndex)

		elif inputClass.getFunctionName() == "WeightResetButton":
			self.resetEspionageWeights()

		elif inputClass.getFunctionName() == "DebugPlayerSelect":
			iIndex = screen.getSelectedPullDownID("DebugPlayerSelect")
			self.iActivePlayer = screen.getPullDownData("DebugPlayerSelect", iIndex)
			self.iTargetPlayer = -1
			self.iTargetCity = -1
			self.updateLeftPanel()
			self.updateRightPanel()

		return 0



	def update(self, fDelta):
		if CyInterface().isDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT):
			self.updateEspionageWeights()
			CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, False)
		return

	def drawEspionageExperience(self):
		if (gc.getPlayer(self.iActivePlayer).greatPeopleThreshold(true) > 0):
			screen = self.getScreen()

			iExperience = gc.getPlayer(self.iActivePlayer).getEspionageExperience()

			screen.addStackedBarGFC("Great Spy Bar", self.X_GREAT_SPY_BAR, self.Y_GREAT_SPY_BAR, self.W_GREAT_SPY_BAR, self.H_GREAT_SPY_BAR, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_SPY, -1, -1)
			screen.setStackedBarColors("Great Spy Bar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED"))
			screen.setStackedBarColors("Great Spy Bar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE"))
			screen.setStackedBarColors("Great Spy Bar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
			screen.setStackedBarColors("Great Spy Bar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
			screen.setBarPercentage("Great Spy Bar", InfoBarTypes.INFOBAR_STORED, float(iExperience) / float(gc.getPlayer(self.iActivePlayer).greatSpyThreshold()))

			screen.setLabel("Great Spy Text", "", localText.getText("TXT_KEY_MISC_ESPIONAGE_EXPERIENCE", ()), CvUtil.FONT_CENTER_JUSTIFY, self.X_GREAT_SPY_BAR + self.W_GREAT_SPY_BAR/2, self.Y_GREAT_SPY_BAR + self.H_GREAT_SPY_BAR/3 - 2, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_GREAT_SPY, -1, -1)