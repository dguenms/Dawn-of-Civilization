from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import Popup
import WBReligionScreen
import WBCorporationScreen
import WBGameDataScreen
import WBInfoScreen
import WBStoredDataScreen
gc = CyGlobalContext()

iChange = 1
bRemove = False

from StoredData import data
from Consts import *

class WBPlayerEnabledScreen:

	def __init__(self, main):
		self.top = main
		self.iGameOption_Y = 250

	def interfaceScreen(self, bWorldBuilderMode = True):
		screen = CyGInterfaceScreen( "WBPlayerEnabledScreen", CvScreenEnums.WB_PLAYER_ENABLED)

		screen.setRenderInterfaceOnly(True)
		screen.addPanel( "MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.setLabel("GameDataHeader", "Background", "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_PLAYER_ENABLED",()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() /2, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText("GameDataExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		iWidth = screen.getXResolution()/4 - 40

		if bWorldBuilderMode:
			screen.addDropDownBoxGFC("CurrentPage", 20, screen.getYResolution() - 42, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ()), 8, 8, False)
			screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ()), 9, 9, False)
			screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PITBOSS_GAME_OPTIONS", ()), 10, 10, False)
			screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_INFO_SCREEN", ()), 11, 11, False)
			screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_STOREDDATA", ()), 12, 12, False)
			screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLAYER_ENABLED", ()), 13, 13, True)

		self.placeGameOptions()

	def placeGameOptions(self):
		screen = CyGInterfaceScreen( "WBPlayerEnabledScreen", CvScreenEnums.WB_PLAYER_ENABLED)
		iWidth = screen.getXResolution() - 40
		iHeight = (screen.getYResolution() - self.iGameOption_Y - 40) /24 * 24 + 2
		
		nColumns = 2
		iWidth1 = 24
		iWidthLeft = iWidth / nColumns - iWidth1
		iWidth2 = iWidthLeft / 5
		iWidth3 = iWidthLeft / 10
		iWidth4 = iWidthLeft / 10
		iWidth5 = iWidthLeft / 5
		screen.addTableControlGFC("WBGameOptions", nColumns * 5, 20, self.iGameOption_Y, iWidth, iHeight, True, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		for i in range(nColumns):
			screen.setTableColumnHeader("WBGameOptions", i*5, "", iWidth1)
			screen.setTableColumnHeader("WBGameOptions", i*5+1, CyTranslator().getText("TXT_KEY_WB_PLAYER_CIVILIZATION", ()), iWidth2)
			screen.setTableColumnHeader("WBGameOptions", i*5+2, CyTranslator().getText("TXT_KEY_WB_PLAYER_BIRTH_YEAR", ()), iWidth3)
			screen.setTableColumnHeader("WBGameOptions", i*5+3, CyTranslator().getText("TXT_KEY_WB_PLAYER_BIRTH_TURN", ()), iWidth4)
			screen.setTableColumnHeader("WBGameOptions", i*5+4, CyTranslator().getText("TXT_KEY_WB_PLAYER_SPAWNTYPE", ()), iWidth5)
		
		iNumRows = (iNumPlayers + nColumns - 1) / nColumns
		for i in xrange(iNumRows):
			screen.appendTableRow("WBGameOptions")
		
		for iPlayer in range(iNumPlayers):
			iColumn = iPlayer / iNumRows
			iRow = iPlayer % iNumRows
			screen.setTableText("WBGameOptions", iColumn*5, iRow, "", gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, gc.getPlayer(iPlayer).getCivilizationType(), -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("WBGameOptions", iColumn*5 + 1, iRow, CyTranslator().getText(str(gc.getPlayer(iPlayer).getCivilizationShortDescriptionKey()), ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("WBGameOptions", iColumn*5 + 2, iRow, self.getYearKey(tBirth[iPlayer]), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("WBGameOptions", iColumn*5 + 3, iRow, CyTranslator().getText("TXT_KEY_SAVEGAME_TURN", (getTurnForYear(tBirth[iPlayer]),)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("WBGameOptions", iColumn*5 + 4, iRow, self.getSpawnTypeText(iPlayer), "", WidgetTypes.WIDGET_PYTHON, 22020, iPlayer, CvUtil.FONT_LEFT_JUSTIFY)

			

	def handleInput(self, inputClass):
		screen = CyGInterfaceScreen("WBPlayerEnabledScreen", CvScreenEnums.WB_PLAYER_ENABLED)
		global iChange
		global bRemove

		if inputClass.getFunctionName() == "CurrentPage":
			iIndex = screen.getPullDownData("CurrentPage", screen.getSelectedPullDownID("CurrentPage"))
			if iIndex == 8:
				WBReligionScreen.WBReligionScreen().interfaceScreen(self.top.m_iCurrentPlayer)
			elif iIndex == 9:
				WBCorporationScreen.WBCorporationScreen().interfaceScreen(self.top.m_iCurrentPlayer)
			elif iIndex == 10:
				WBGameDataScreen.WBGameDataScreen(self.top).interfaceScreen()
			elif iIndex == 11:
				WBInfoScreen.WBInfoScreen().interfaceScreen(self.top.m_iCurrentPlayer)
			elif iIndex == 12:
				WBStoredDataScreen.WBStoredDataScreen(self.top).interfaceScreen()

		elif inputClass.getFunctionName() == "WBGameOptions":
			if inputClass.getData1() == 22020:
				iPlayer = inputClass.getData2()
				data.players[iPlayer].iSpawnType = (data.players[iPlayer].iSpawnType + 1) % 3
				self.placeGameOptions()

		return 1
		
	def getYearKey(self, iYear):
		if iYear > 0:
			return CyTranslator().getText("TXT_KEY_YEAR_AD", (abs(iYear),))
		else:
			return CyTranslator().getText("TXT_KEY_YEAR_BC", (abs(iYear),))

	def getSpawnTypeText(self, iPlayer):
		iSpawnType = data.players[iPlayer].iSpawnType
		sText = ""
		if iSpawnType == iForcedSpawn:
			sText = CyTranslator().getText("TXT_KEY_WB_FORCED_SPAWN", ())
			iColor = gc.getInfoTypeForString("COLOR_GREEN")
		elif iSpawnType == iNoSpawn:
			sText = CyTranslator().getText("TXT_KEY_WB_NO_SPAWN", ())
			iColor = gc.getInfoTypeForString("COLOR_RED")
		elif iSpawnType == iConditionalSpawn:
			sText = CyTranslator().getText("TXT_KEY_WB_CONDITIONAL_SPAWN", ())
			iColor = gc.getInfoTypeForString("COLOR_YELLOW")
			
		if gc.getGame().getGameTurn() >= getTurnForYear(tBirth[iPlayer]):
			iColor = gc.getInfoTypeForString("COLOR_GREY")
			
		sText = CyTranslator().changeTextColor(sText, iColor)
		return sText
			

	def update(self, fDelta):
		return 1