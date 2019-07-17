from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import Popup
import WBReligionScreen
import WBCorporationScreen
import WBInfoScreen
import WBStoredDataScreen
import WBPlayerEnabledScreen
gc = CyGlobalContext()

iChange = 1
bHiddenOption = True
bRepeat = False
iSelectedCiv = -1
iSelectedLeader = -1
bRemove = False

from StoredData import data
from Consts import *
import Congresses as cong

class WBGameDataScreen:

	def __init__(self, main):
		self.top = main
		self.iNewPlayer_Y = 80
		self.iScript_Y = 300
		self.iGameOption_Y = self.iScript_Y + 120

	def interfaceScreen(self):
		screen = CyGInterfaceScreen( "WBGameDataScreen", CvScreenEnums.WB_GAMEDATA)

		screen.setRenderInterfaceOnly(True)
		screen.addPanel( "MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.setLabel("GameDataHeader", "Background", "<font=4b>" + CyTranslator().getText("TXT_KEY_PITBOSS_GAME_OPTIONS",()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() /2, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText("GameDataExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		iWidth = screen.getXResolution()/4 - 40
		screen.addDropDownBoxGFC("ChangeBy", 20, 50, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		i = 1
		while i < 100001:
			screen.addPullDownString("ChangeBy", "(+/-) " + str(i), i, i, iChange == i)
			if str(i)[0] == "1":
				i *= 5
			else:
				i *= 2

		screen.addDropDownBoxGFC("ChangeType", 20, 50 + 20 + 15, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_ADD", ()), 1, 1, not bRemove)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_REMOVE", ()), 0, 0, bRemove)

		screen.addDropDownBoxGFC("CurrentPage", 20, screen.getYResolution() - 42, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ()), 8, 8, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ()), 9, 9, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PITBOSS_GAME_OPTIONS", ()), 10, 10, True)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_INFO_SCREEN", ()), 11, 11, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_STOREDDATA", ()), 12, 12, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLAYER_ENABLED", ()), 13, 13, False)

		self.placeStats()
		self.placeGameOptions()
		self.placeScript()
		self.placeNewPlayer()

	def placeStats(self):
		screen = CyGInterfaceScreen( "WBGameDataScreen", CvScreenEnums.WB_GAMEDATA)

		iY = 90 + 35
		screen.setButtonGFC("StartYearPlus", "", "", 20, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("StartYearMinus", "", "", 45, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		iYear = CyGame().getStartYear()
		if iYear < 0:
			sYear = str(-iYear) + " BC"
		else:
			sYear = str(iYear) + " AD"
		sText = CyTranslator().getText("TXT_KEY_WB_START_YEAR", ()) + ": " + sYear
		screen.setLabel("StartYearText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, 75, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setButtonGFC("MaxCityEliminationPlus", "", "", screen.getXResolution() /4 + 20, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("MaxCityEliminationMinus", "", "", screen.getXResolution() /4 + 45, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = CyTranslator().getText("TXT_KEY_WB_MAX_CITY_ELIMINATION", (CyGame().getMaxCityElimination(),))
		screen.setLabel("MaxCityEliminationText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, screen.getXResolution() /4 + 75, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		screen.setButtonGFC("GameTurnPlus", "", "", 20, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("GameTurnMinus", "", "", 45, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = CyTranslator().getText("TXT_KEY_WB_GAME_TURN", (CyGame().getGameTurn(),))
		screen.setLabel("GameTurnText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, 75, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setButtonGFC("TargetScorePlus", "", "", screen.getXResolution() /4 + 20, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("TargetScoreMinus", "", "", screen.getXResolution() /4 + 45, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = CyTranslator().getText("TXT_KEY_WB_TARGET_SCORE", (CyGame().getTargetScore(),))
		screen.setLabel("TargetScoreText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, screen.getXResolution() /4 + 75, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		iYear = CyGame().getGameTurnYear()
		if iYear < 0:
			sYear = str(-iYear) + " BC"
		else:
			sYear = str(iYear) + " AD"
		sText = CyTranslator().getText("TXT_KEY_WB_GAME_YEAR", (sYear,))
		screen.setLabel("GameYearText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, 75, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setButtonGFC("NukesExplodedPlus", "", "", screen.getXResolution() /4 + 20, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("NukesExplodedMinus", "", "", screen.getXResolution() /4 + 45, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = CyTranslator().getText("TXT_KEY_WB_NUKES_EXPLODED", (CyGame().getNukesExploded(),))
		screen.setLabel("NukesExplodedText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, screen.getXResolution() /4 + 75, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		screen.setButtonGFC("EstimateEndTurnPlus", "", "", 20, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("EstimateEndTurnMinus", "", "", 45, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = CyTranslator().getText("TXT_KEY_WB_ESTIMATED_END_TURN", (CyGame().getEstimateEndTurn(),))
		screen.setLabel("EstimateEndTurnText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, 75, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setButtonGFC("TradeRoutesPlus", "", "", screen.getXResolution() /4 + 20, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("TradeRoutesMinus", "", "", screen.getXResolution() /4 + 45, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = CyTranslator().getText("TXT_KEY_HEADING_TRADEROUTE_LIST", ()) + ": " + str(gc.getDefineINT("INITIAL_TRADE_ROUTES") + CyGame().getTradeRoutes())
		screen.setLabel("TradeRoutesText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, screen.getXResolution() /4 + 75, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		screen.setButtonGFC("MaxTurnsPlus", "", "", 20, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("MaxTurnsMinus", "", "", 45, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = CyTranslator().getText("TXT_KEY_WB_MAX_TURNS", (CyGame().getMaxTurns(),))
		screen.setLabel("MaxTurnsText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, 75, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setButtonGFC("AIAutoPlayPlus", "", "", screen.getXResolution() /4 + 20, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("AIAutoPlayMinus", "", "", screen.getXResolution() /4 + 45, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = CyTranslator().getText("TXT_KEY_WB_AI_AUTOPLAY", (CyGame().getAIAutoPlay(),))
		screen.setLabel("AIAutoPlayText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, screen.getXResolution() /4 + 75, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		screen.setLabel("AutoPlayStop", "Background", "<font=3>" + CyTranslator().getText("TXT_KEY_WB_AI_AUTOPLAY_WARNING",()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() /4, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def placeNewPlayer(self):
		if CyGame().countCivPlayersEverAlive() == gc.getMAX_CIV_PLAYERS(): return
		screen = CyGInterfaceScreen( "WBGameDataScreen", CvScreenEnums.WB_GAMEDATA)
		sHeaderText = CyTranslator().getText("TXT_KEY_WB_ADD_NEW_PLAYER",())

		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if bRepeat:
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ()) 
		screen.setText("AllowsRepeat", "Background", "<font=3b>" + sColor + CyTranslator().getText("TXT_KEY_MAIN_MENU_REPEAT_PASSWORD",()) + "</color></font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 20, self.iNewPlayer_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PYTHON, 1029, 30)
		iWidth = screen.getXResolution()/2 - 40
		iHeight = (screen.getYResolution()/2 - self.iNewPlayer_Y - 10) /48 * 24 + 2
		nColumns = 3
		screen.addTableControlGFC("WBNewCiv", nColumns, screen.getXResolution()/2 + 20, self.iNewPlayer_Y, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		for i in xrange(nColumns):
			screen.setTableColumnHeader("WBNewCiv", i, "", iWidth/nColumns)

		lList = []
		for item in xrange(gc.getNumCivilizationInfos()):
			Info = gc.getCivilizationInfo(item)
			if CyGame().isCivEverActive(item) and not bRepeat: continue
			if Info.isAIPlayable():
				lList.append([Info.getShortDescription(0), item])
		lList.sort()
		iNumRows = (len(lList) + nColumns - 1) / nColumns
		for i in xrange(iNumRows):
			screen.appendTableRow("WBNewCiv")

		for i in xrange(len(lList)):
			item = lList[i][1]
			Info = gc.getCivilizationInfo(item)
			iColumn = i / iNumRows
			iRow = i % iNumRows
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if iSelectedCiv == item:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			sText = "<font=3>" + sColor + lList[i][0] + "</font></color>"
			screen.setTableText("WBNewCiv", iColumn, iRow, sText, Info.getButton(), WidgetTypes.WIDGET_PYTHON, 7872, item, CvUtil.FONT_LEFT_JUSTIFY)
		iY = self.iNewPlayer_Y + iHeight + 10
		if iSelectedCiv > -1:
			sHeaderText = gc.getCivilizationInfo(iSelectedCiv).getShortDescription(0)
			screen.addTableControlGFC("WBNewLeader", nColumns, screen.getXResolution()/2 + 20, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
			for i in xrange(nColumns):
				screen.setTableColumnHeader("WBNewLeader", i, "", iWidth/nColumns)

			lList = []
			for item in xrange(gc.getNumLeaderHeadInfos()):
				Info = gc.getLeaderHeadInfo(item)
				if not CyGame().isLeaderEverActive(item) or bRepeat:
					if CyGame().isOption(GameOptionTypes.GAMEOPTION_LEAD_ANY_CIV) or gc.getCivilizationInfo(iSelectedCiv).isLeaders(item):
						lList.append([Info.getDescription(), item])
			lList.sort()
			iNumRows = (len(lList) + nColumns - 1) / nColumns
			for i in xrange(iNumRows):
				screen.appendTableRow("WBNewLeader")

			for i in xrange(len(lList)):
				item = lList[i][1]
				Info = gc.getLeaderHeadInfo(item)
				iColumn = i / iNumRows
				iRow = i % iNumRows
				sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
				if iSelectedLeader == item:
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				sText = "<font=3>" + sColor + lList[i][0] + "</font></color>"
				screen.setTableText("WBNewLeader", iColumn, iRow, sText, Info.getButton(), WidgetTypes.WIDGET_PYTHON, 7876, item, CvUtil.FONT_LEFT_JUSTIFY)
			if iSelectedLeader > -1:
				sHeaderText += ", " + gc.getLeaderHeadInfo(iSelectedLeader).getDescription()
				sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=4b>" + CyTranslator().getText("TXT_KEY_MAIN_MENU_LOADSAVE_CREATE", ()) + "</color></font>"
				screen.setText("CreatePlayer", "Background", sText, CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 20, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabel("NewPlayerHeader", "Background", "<font=3b>" + sHeaderText + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() *3/4, self.iNewPlayer_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def placeScript(self):
		screen = CyGInterfaceScreen( "WBGameDataScreen", CvScreenEnums.WB_GAMEDATA)
		sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=3b>" + CyTranslator().getText("TXT_KEY_WB_SCRIPT_DATA", ()) + "</color></font>"
		screen.setText("GameEditScriptData", "Background", sText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/4, self.iScript_Y, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel( "ScriptPanel", "", "", False, False, 20, self.iScript_Y + 25, screen.getXResolution()/2 - 40, 50, PanelStyles.PANEL_STYLE_IN)
		screen.addMultilineText("GameScriptDataText", CyGame().getScriptData(), 20, self.iScript_Y + 25, screen.getXResolution()/2 - 40, 50, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeGameOptions(self):
		screen = CyGInterfaceScreen( "WBGameDataScreen", CvScreenEnums.WB_GAMEDATA)
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if bHiddenOption:
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ()) 
		screen.setText("HiddenOptions", "Background", "<font=3b>" + sColor + CyTranslator().getText("TXT_KEY_WB_SHOW_HIDDEN",()) + "</color></font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 20, self.iGameOption_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iWidth = screen.getXResolution() - 40
		iHeight = (screen.getYResolution() - self.iGameOption_Y - 40) /24 * 24 + 2
		nColumns = 3
		iWidth1 = 80
		iWidth2 = iWidth / nColumns - iWidth1
		screen.addTableControlGFC("WBGameOptions", nColumns * 2, 20, self.iGameOption_Y, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		for i in xrange(nColumns):
			screen.setTableColumnHeader("WBGameOptions", i * 2, "", iWidth2)
			screen.setTableColumnHeader("WBGameOptions", i * 2 + 1, "", iWidth1)

		lList = []
		for item in xrange(gc.getNumGameOptionInfos()):
			Info = gc.getGameOptionInfo(item)
			if Info.getVisible() or bHiddenOption:
				lList.append([Info.getDescription(), item])
		lList.sort()

		# Merijn: Add extra DoC options
		lList2 = []
		lList2.append([CyTranslator().getText("TXT_KEY_WB_IGNORE_AI_UHV", ()), 2000])
		lList2.append([CyTranslator().getText("TXT_KEY_WB_UNLIMITED_SWITCHING", ()), 2001])
		lList2.append([CyTranslator().getText("TXT_KEY_WB_NO_CONGRESS", ()), 2002])
		lList2.append([CyTranslator().getText("TXT_KEY_WB_NO_PLAGUE", ()), 2003])
		lList2.sort()

		# Stored variables
		lList3 = []
		lList3.append([CyTranslator().getText("TXT_KEY_WB_ALREADY_SWITCHED", ()), 3001])
		lList3.append([CyTranslator().getText("TXT_KEY_WB_CONGRESS_TURNS", ()), 3002])
		lList3.sort()

		iNumRows = (len(lList) + nColumns - 1) / nColumns
		iNumRows2 = iNumRows + 3 + max(len(lSecondaryCivs), len(lList2), len(lList3))
		for i in xrange(iNumRows2):
			screen.appendTableRow("WBGameOptions")

		for i in xrange(len(lList)):
			iColumn = i / iNumRows
			iRow = i % iNumRows
			item = lList[i][1]

			bEnabled = CyGame().isOption(item)
			bDefault = False
			if item in [6, 11]: # Aggressive AI, No Tech Brokering
				bDefault = True

			sText = self.colorText(lList[i][0], bEnabled)
			screen.setTableText("WBGameOptions", iColumn * 2, iRow, sText, "", WidgetTypes.WIDGET_PYTHON, 1028, item, CvUtil.FONT_LEFT_JUSTIFY)
			sText = self.colorText(CyTranslator().getText("TXT_KEY_WB_DEFAULT", ()), bDefault)
			screen.setTableText("WBGameOptions", iColumn * 2 + 1, iRow, sText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

		# Merijn: extra rows for secondary civs and RFC options
		screen.setTableText("WBGameOptions", 0, iNumRows + 2, CyTranslator().getText("TXT_KEY_WB_SECONDARY_CIVS", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText("WBGameOptions", 2, iNumRows + 2, CyTranslator().getText("TXT_KEY_WB_RFC_OPTIONS", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText("WBGameOptions", 4, iNumRows + 2, CyTranslator().getText("TXT_KEY_WB_RFC_VARIABLES", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		iRow = iNumRows + 3
		for iCiv in lSecondaryCivs:
			bEnabled = data.isPlayerEnabled(iCiv)
			bDefault = True
			if iCiv in [iHarappa, iPolynesia]:
				bDefault = False

			sText = self.colorText(gc.getPlayer(iCiv).getCivilizationShortDescription(0), bEnabled)
			screen.setTableText("WBGameOptions", 0, iRow, sText, "", WidgetTypes.WIDGET_PYTHON, 1028, 1000+iCiv, CvUtil.FONT_LEFT_JUSTIFY)
			sText = self.colorText(CyTranslator().getText("TXT_KEY_WB_DEFAULT", ()), bDefault)
			screen.setTableText("WBGameOptions", 1, iRow, sText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			iRow += 1

		for i in xrange(len(lList2)):
			item = lList2[i][1]
			iRow = iNumRows + 3 + i

			bEnabled = False
			bDefault = False

			if item == 2000:
				bEnabled = data.bIgnoreAI
				bDefault = True
			elif item == 2001:
				bEnabled = data.bUnlimitedSwitching
			elif item == 2002:
				bEnabled = data.bNoCongressOption
			elif item == 2003:
				bEnabled = data.bNoPlagues

			sText = self.colorText(lList2[i][0], bEnabled)
			screen.setTableText("WBGameOptions", 2, iRow, sText, "", WidgetTypes.WIDGET_PYTHON, 1028, item, CvUtil.FONT_LEFT_JUSTIFY)
			sText = self.colorText(CyTranslator().getText("TXT_KEY_WB_DEFAULT", ()), bDefault)
			screen.setTableText("WBGameOptions", 3, iRow, sText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

		for i in xrange(len(lList3)):
			item = lList3[i][1]
			iRow = iNumRows + 3 + i

			bEnabled = False
			bWhite = False

			if item == 3001:
				bEnabled = data.bAlreadySwitched
			elif item == 3002:
				bWhite = True

			sText = self.colorText(lList3[i][0], bEnabled, bWhite)
			screen.setTableText("WBGameOptions", 4, iRow, sText, "", WidgetTypes.WIDGET_PYTHON, 1028, item, CvUtil.FONT_LEFT_JUSTIFY)
			if item == 3002:
				if not cong.isCongressEnabled():
					iTurns = -1
				else:
					iTurns = data.iCongressTurns
				sText = self.colorText(str(iTurns), True, True)
				screen.setTableText("WBGameOptions", 5, iRow, sText, "", WidgetTypes.WIDGET_PYTHON, 1028, item, CvUtil.FONT_CENTER_JUSTIFY)

	def handleInput(self, inputClass):
		screen = CyGInterfaceScreen("WBGameDataScreen", CvScreenEnums.WB_GAMEDATA)
		global iChange
		global bHiddenOption
		global bRepeat
		global iSelectedCiv
		global iSelectedLeader
		global bRemove

		if inputClass.getFunctionName() == "CurrentPage":
			iIndex = screen.getPullDownData("CurrentPage", screen.getSelectedPullDownID("CurrentPage"))
			if iIndex == 8:
				WBReligionScreen.WBReligionScreen().interfaceScreen(self.top.m_iCurrentPlayer)
			elif iIndex == 9:
				WBCorporationScreen.WBCorporationScreen().interfaceScreen(self.top.m_iCurrentPlayer)
			elif iIndex == 11:
				WBInfoScreen.WBInfoScreen().interfaceScreen(self.top.m_iCurrentPlayer)
			elif iIndex == 12:
				WBStoredDataScreen.WBStoredDataScreen(self.top).interfaceScreen()
			elif iIndex == 13:
				WBPlayerEnabledScreen.WBPlayerEnabledScreen(self.top).interfaceScreen()

		elif inputClass.getFunctionName() == "ChangeBy":
			if bRemove:
				iChange = -screen.getPullDownData("ChangeBy", screen.getSelectedPullDownID("ChangeBy"))
			else:
				iChange = screen.getPullDownData("ChangeBy", screen.getSelectedPullDownID("ChangeBy"))

		elif inputClass.getFunctionName() == "ChangeType":
			bRemove = not bRemove
			iChange = -iChange

		elif inputClass.getFunctionName().find("StartYear") > -1:
			if inputClass.getData1() == 1030:
				CyGame().setStartYear(CyGame().getStartYear() + abs(iChange))
			elif inputClass.getData1() == 1031:
				CyGame().setStartYear(CyGame().getStartYear() - abs(iChange))
			self.placeStats()

		elif inputClass.getFunctionName().find("MaxCityElimination") > -1:
			if inputClass.getData1() == 1030:
				CyGame().setMaxCityElimination(CyGame().getMaxCityElimination() + abs(iChange))
			elif inputClass.getData1() == 1031:
				CyGame().setMaxCityElimination(max(0, CyGame().getMaxCityElimination() - abs(iChange)))
			self.placeStats()

		elif inputClass.getFunctionName().find("GameTurn") > -1:
			if inputClass.getData1() == 1030:
				iChange = min(abs(iChange), CyGame().getMaxTurns() - CyGame().getElapsedGameTurns())
				CyGame().setGameTurn(CyGame().getGameTurn() + iChange)
				CyGame().changeMaxTurns(- iChange)
			elif inputClass.getData1() == 1031:
				iChange = min(CyGame().getGameTurn(), abs(iChange))
				CyGame().setGameTurn(CyGame().getGameTurn() - iChange)
				CyGame().changeMaxTurns(iChange)
			self.placeStats()

		elif inputClass.getFunctionName().find("TargetScore") > -1:
			if inputClass.getData1() == 1030:
				CyGame().setTargetScore(CyGame().getTargetScore() + abs(iChange))
			elif inputClass.getData1() == 1031:
				CyGame().setTargetScore(max(0, CyGame().getTargetScore() - abs(iChange)))
			self.placeStats()

		elif inputClass.getFunctionName().find("EstimateEndTurn") > -1:
			if inputClass.getData1() == 1030:
				CyGame().setEstimateEndTurn(CyGame().getEstimateEndTurn() + iChange)
			elif inputClass.getData1() == 1031:
				CyGame().setEstimateEndTurn(max(0, CyGame().getEstimateEndTurn() - iChange))
			self.placeStats()

		elif inputClass.getFunctionName().find("NukesExploded") > -1:
			if inputClass.getData1() == 1030:
				CyGame().changeNukesExploded(abs(iChange))
			elif inputClass.getData1() == 1031:
				CyGame().changeNukesExploded(- min(CyGame().getNukesExploded(), abs(iChange)))
			self.placeStats()

		elif inputClass.getFunctionName().find("MaxTurns") > -1:
			if inputClass.getData1() == 1030:
				CyGame().changeMaxTurns(abs(iChange))
			elif inputClass.getData1() == 1031:
				CyGame().changeMaxTurns(- min(CyGame().getMaxTurns(), abs(iChange)))
			self.placeStats()

		elif inputClass.getFunctionName().find("TradeRoutes") > -1:
			if inputClass.getData1() == 1030:
				CyGame().changeTradeRoutes(min(abs(iChange), gc.getDefineINT("MAX_TRADE_ROUTES") - gc.getDefineINT("INITIAL_TRADE_ROUTES") - CyGame().getTradeRoutes()))
			elif inputClass.getData1() == 1031:
				CyGame().changeTradeRoutes(- min(CyGame().getTradeRoutes(), abs(iChange)))
			self.placeStats()

		elif inputClass.getFunctionName().find("AIAutoPlay") > -1:
			if inputClass.getData1() == 1030:
				CyGame().setAIAutoPlay(CyGame().getAIAutoPlay() + abs(iChange))
			elif inputClass.getData1() == 1031:
				CyGame().setAIAutoPlay(max(0, CyGame().getAIAutoPlay() - abs(iChange)))
			self.placeStats()

		elif inputClass.getFunctionName() == "WBGameOptions":
			iGameOption = inputClass.getData2()
			if iGameOption < gc.getNumGameOptionInfos():
				CyGame().setOption(iGameOption, not CyGame().isOption(iGameOption))
				self.checkOptions(iGameOption)
			else:
				# Enabling/disabling secondary civs
				if iGameOption < 2000:
					iItem = iGameOption - 1000
					data.setPlayerEnabled(iItem, not data.isPlayerEnabled(iItem))
				# Enabling/disabling RFC options
				elif iGameOption == 2000:
					data.bIgnoreAI = not data.bIgnoreAI
				elif iGameOption == 2001:
					data.bUnlimitedSwitching = not data.bUnlimitedSwitching
				elif iGameOption == 2002:
					data.bNoCongressOption = not data.bNoCongressOption
				elif iGameOption == 2003:
					data.bNoPlagues = not data.bNoPlagues
				# Stored Variables
				elif iGameOption == 3001:
					data.bAlreadySwitched = not data.bAlreadySwitched
				elif iGameOption == 3002 and cong.isCongressEnabled():
					data.iCongressTurns = max(1, data.iCongressTurns+iChange)
			self.placeGameOptions()

		elif inputClass.getFunctionName() == "HiddenOptions":
			bHiddenOption = not bHiddenOption
			self.placeGameOptions()

		elif inputClass.getFunctionName() == "AllowsRepeat":
			bRepeat = not bRepeat
			iSelectedCiv = -1
			iSelectedLeader = -1
			self.placeNewPlayer()

		elif inputClass.getFunctionName() == "WBNewCiv":
			iSelectedCiv = inputClass.getData2()
			iSelectedLeader = -1
			self.interfaceScreen()

		elif inputClass.getFunctionName() == "WBNewLeader":
			iSelectedLeader = inputClass.getData2()
			self.interfaceScreen()

		elif inputClass.getFunctionName() == "CreatePlayer":
			for i in xrange(gc.getMAX_CIV_PLAYERS()):
				if not gc.getPlayer(i).isEverAlive():
					CyGame().addPlayer(i, iSelectedLeader, iSelectedCiv)
					break
			screen.hideScreen()
			self.top.m_iCurrentPlayer = i
			self.top.normalPlayerTabModeCB()

		elif inputClass.getFunctionName() == "GameEditScriptData":
			popup = Popup.PyPopup(4444, EventContextTypes.EVENTCONTEXT_ALL)
			popup.setHeaderString(CyTranslator().getText("TXT_KEY_WB_SCRIPT", ()))
			popup.createEditBox(CyGame().getScriptData())
			popup.launch()

		return 1

	def checkOptions(self, iGameOption):
		if iGameOption == GameOptionTypes.GAMEOPTION_LEAD_ANY_CIV:
			iSelectedCiv = -1
			iSelectedLeader = -1
			self.interfaceScreen()
		elif iGameOption == GameOptionTypes.GAMEOPTION_NO_GOODY_HUTS and CyGame().isOption(iGameOption):
			CyMapGenerator().eraseGoodies()
		elif iGameOption == GameOptionTypes.GAMEOPTION_NO_VASSAL_STATES and CyGame().isOption(iGameOption):
			for iTeamX in xrange(gc.getMAX_CIV_TEAMS()):
				pTeamX = gc.getTeam(iTeamX)
				for iTeamY in xrange(gc.getMAX_CIV_TEAMS()):
					pTeamX.freeVassal(iTeamY)
		elif iGameOption == GameOptionTypes.GAMEOPTION_ALWAYS_PEACE and CyGame().isOption(iGameOption):
			for iTeamX in xrange(gc.getMAX_CIV_TEAMS()):
				pTeamX = gc.getTeam(iTeamX)
				if CyGame().isOption(GameOptionTypes.GAMEOPTION_ALWAYS_WAR) and pTeamX.isHuman(): continue
				for iTeamY in xrange(gc.getMAX_CIV_TEAMS()):
					if CyGame().isOption(GameOptionTypes.GAMEOPTION_ALWAYS_WAR) and gc.getTeam(iTeamY).isHuman(): continue
					pTeamX.makePeace(iTeamY)
		elif iGameOption == GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE and CyGame().isOption(iGameOption):
			for iPlayerX in xrange(gc.getMAX_CIV_PLAYERS()):
				pPlayerX = gc.getPlayer(iPlayerX)
				if pPlayerX.isHuman():
					(loopCity, iter) = pPlayerX.firstCity(false)
					while(loopCity):
						if not loopCity.isCapital():
							loopCity.kill()
						(loopCity, iter) = pPlayerX.nextCity(iter, false)
		elif iGameOption == GameOptionTypes.GAMEOPTION_NO_BARBARIANS and CyGame().isOption(iGameOption):
			pPlayerBarb = gc.getPlayer(gc.getBARBARIAN_PLAYER ())
			pPlayerBarb.killCities()
			pPlayerBarb.killUnits()

	def colorText(self, sString, bVal, bWhite = False):
		if bWhite:
			sColor = ""
		elif bVal:
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		else:
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		sText = "<font=3>" + sColor + sString + "</font></color>"
		return sText

	def update(self, fDelta):
		return 1