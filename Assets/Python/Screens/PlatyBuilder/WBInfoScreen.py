from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import WBPlotScreen
import WBUnitScreen
import WBCityEditScreen
import WBPromotionScreen
import WBPlayerScreen
import WBTechScreen
import WBProjectScreen
import CvPlatyBuilderScreen
import Popup as PyPopup
gc = CyGlobalContext()

import Consts as con
import RFCUtils
utils = RFCUtils.RFCUtils()
import MapDrawer as md
import Areas

iMode = 0
iSelectedPlayer = -1
iItem = -1
lItems = []
lSelectedItem = [-1, -1]

# Merijn
iChange = 1
iChangeType = 1
iSetValue = 3
tCurrentPlot = -1
bHideForbidden = True
lSquareSelection = [-1, -1, False]

class WBInfoScreen:

	def __init__(self):
		self.iTable_Y = 80
		self.iMinColWidth = 120
		self.iColorA = "COLOR_YELLOW"
		self.iColorB = "COLOR_BLACK"
		self.Mode = [	gc.getUnitInfo,
				gc.getPromotionInfo,
				gc.getBuildingInfo,
				gc.getSpecialistInfo,
				gc.getReligionInfo,
				gc.getCorporationInfo,
				gc.getTerrainInfo,
				gc.getFeatureInfo,
				gc.getBonusInfo,
				gc.getImprovementInfo,
				gc.getRouteInfo,
				gc.getCivicInfo,
				gc.getTechInfo,
				gc.getProjectInfo,
				]

		# Merijn StabMap colors
		self.iColorSpawn = "COLOR_PLAYER_DARK_PINK"
		self.iColorSpawnWater = "COLOR_PLAYER_GREYISH_CYAN"
		self.lPlotNumberText = ["Core", "Historical", "Contested", "Foreign Core", "Normal Tile", "/AI forbidden"]
		self.lColors = ["COLOR_PLAYER_DARK_GREEN", "COLOR_GREEN", "COLOR_YELLOW", "COLOR_RED", "COLOR_WHITE_TEXT", "COLOR_PLAYER_LIGHT_PURPLE"]
		self.lPresetValues = [3, 20, 90, 200, 500, 700]

	def interfaceScreen(self, iPlayerX):
		screen = CyGInterfaceScreen("WBInfoScreen", CvScreenEnums.WB_INFO)
		global iSelectedPlayer
		global tCurrentPlot

		iSelectedPlayer = iPlayerX

		screen.setRenderInterfaceOnly(True)
		screen.addPanel("MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
	
		screen.setText("WBInfoExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		iX = 20
		iY = 20
		iWidth = screen.getXResolution()/3 - 20

		screen.addDropDownBoxGFC("ItemType", iX, iY, iWidth/2, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("ItemType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()), 0, 0, 0 == iMode)
		screen.addPullDownString("ItemType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ()), 1, 1, 1 == iMode)
		screen.addPullDownString("ItemType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()), 2, 2, 2 == iMode)
		screen.addPullDownString("ItemType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_SPECIALIST", ()), 3, 3, 3 == iMode)
		screen.addPullDownString("ItemType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ()), 4, 4, 4 == iMode)
		screen.addPullDownString("ItemType", CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ()), 5, 5, 5 == iMode)
		screen.addPullDownString("ItemType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TERRAIN", ()), 6, 6, 6 == iMode)
		screen.addPullDownString("ItemType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_FEATURE", ()), 7, 7, 7 == iMode)
		screen.addPullDownString("ItemType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ()), 8, 8, 8 == iMode)
		screen.addPullDownString("ItemType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ()), 9, 9, 9 == iMode)
		screen.addPullDownString("ItemType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_ROUTE", ()), 10, 10, 10 == iMode)
		screen.addPullDownString("ItemType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIVIC", ()), 11, 11, 11 == iMode)
		screen.addPullDownString("ItemType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH", ()), 12, 12, 12 == iMode)
		screen.addPullDownString("ItemType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()), 13, 13, 13 == iMode)
		screen.addPullDownString("ItemType", CyTranslator().getText("TXT_KEY_STABILITY_MAPS", ()), 14, 14, 14 == iMode)
		screen.addPullDownString("ItemType", CyTranslator().getText("TXT_KEY_SPAWN_MAPS", ()), 15, 15, 15 == iMode)

		if iMode < 14:
			screen.addDropDownBoxGFC("CurrentPlayer", iX + iWidth/2, iY, iWidth/2, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for i in xrange(gc.getMAX_PLAYERS()):
				pPlayerX = gc.getPlayer(i)
				if pPlayerX.isAlive():
					sText = pPlayerX.getName()
					screen.addPullDownString("CurrentPlayer", sText, i, i, i == iSelectedPlayer)
		elif iMode == 14:
			screen.addDropDownBoxGFC("ChangeBy", iX + iWidth/2, iY, iWidth/4, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			i = 1
			while i < 1000001:
				screen.addPullDownString("ChangeBy", "(+/-) " + str(i), i, i, iChange == i)
				if str(i)[0] == "1":
					i *= 5
				else:
					i *= 2

			screen.addDropDownBoxGFC("ChangeType", iX + iWidth/4*3, iY, iWidth/4, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_ADD", ()), 1, 1, 1 == iChangeType)
			screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_REMOVE", ()), 0, 0, 0 == iChangeType)
			screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_SET_VALUE", ()), 2, 2, 2 == iChangeType)

		self.placeMap()
		if iMode < 14:
			self.placeItems()
		else:
			if tCurrentPlot == -1: tCurrentPlot = Areas.getCapital(utils.getHumanID())
			self.placeItemsStabMap()
			self.mapButtons()
		self.refreshMap()

	def placePlotData(self):
		screen = CyGInterfaceScreen("WBInfoScreen", CvScreenEnums.WB_INFO)
		iX = screen.getXResolution() * 2/3 + 10
		iY = screen.getYResolution() *2/3
		sText = "<font=3b>" + CyTranslator().getText("[COLOR_SELECTED_TEXT]", ())
		if iMode < 2:
			iPlayer = lSelectedItem[0]
			iUnit = lSelectedItem[1]
			pUnit = gc.getPlayer(iPlayer).getUnit(iUnit)
			if pUnit:
				sText += pUnit.getName()
				sText += u" (%d,%d)" %(pUnit.getX(), pUnit.getY())
		elif iMode < 5:
			iPlayer = lSelectedItem[0]
			iCity = lSelectedItem[1]
			pCity = gc.getPlayer(iPlayer).getCity(iCity)
			if pCity:
				sText += pCity.getName()
				sText += u" (%d,%d)" %(pCity.getX(), pCity.getY())
		elif iMode < 11:
			sText += CyTranslator().getText("TXT_KEY_WB_PLOT_DATA", ())
			if lSelectedItem[0] > -1 and lSelectedItem[1] > -1:
				sText += u" (%d,%d)" %(lSelectedItem[0], lSelectedItem[1])
		elif iMode == 11:
			iPlayer = lSelectedItem[0]
			pPlayer = gc.getPlayer(iPlayer)
			sText += u" %s (%s)" %(pPlayer.getName(), pPlayer.getCivilizationDescription(0))
		elif iMode < 14:
			iTeam = lSelectedItem[0]
			pTeam = gc.getTeam(iTeam)
			sText += pTeam.getName()
		else:
			sText += u" (%d,%d)" %(tCurrentPlot[0], tCurrentPlot[1])

		sText += "</color></font>"
		screen.setText("PlotData", "Background", sText, CvUtil.FONT_CENTER_JUSTIFY, iX, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def mapButtons(self):
		screen = CyGInterfaceScreen("WBInfoScreen", CvScreenEnums.WB_INFO)
		iX = screen.getXResolution()/3 + 20
		iY = self.iTable_Y
		iWidth = screen.getXResolution() * 2/3 - 40
		iMaxHeight = screen.getYResolution() * 2/3 - iY

		iHeight = iWidth * CyMap().getGridHeight() / CyMap().getGridWidth()
		if iHeight > iMaxHeight:
			iWidth = iMaxHeight * CyMap().getGridWidth() / CyMap().getGridHeight()
			iHeight = iMaxHeight

		iButtonSize = 48
		iAdjust = 10
		iGap = iButtonSize + iAdjust
		iXx = iX + iWidth - 5*iGap
		iYy = iY + iHeight + 30
		screen.addPanel("PlotMovePanel", "", "", False, False, iXx - iAdjust, iYy - iAdjust, 5*iGap + iAdjust, 5*iGap + iAdjust, PanelStyles.PANEL_STYLE_IN)
		screen.setButtonGFC("MovePlotUpFive", "", "Art/Interface/Buttons/WorldBuilder/Up5.dds", iXx + 2*iGap, iYy, iButtonSize, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22201, 5, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("MovePlotUpOne", "", "Art/Interface/Buttons/WorldBuilder/Up.dds", iXx + 2*iGap, iYy + iGap, iButtonSize, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22201, 1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("MovePlotDownOne", "", "Art/Interface/Buttons/WorldBuilder/Down.dds", iXx + 2*iGap, iYy + 3*iGap, iButtonSize, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22202, 1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("MovePlotDownFive", "", "Art/Interface/Buttons/WorldBuilder/Down5.dds", iXx + 2*iGap, iYy + 4*iGap, iButtonSize, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22202, 5, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("Sonic", "", "", iXx + 2*iGap, iYy + 2*iGap, iButtonSize, iButtonSize, WidgetTypes.WIDGET_PYTHON, iXx + 2*iGap, iYy + 2*iGap, ButtonStyles.BUTTON_STYLE_TOOL)
		screen.setButtonGFC("MovePlotLeftFive", "", "Art/Interface/Buttons/WorldBuilder/Left5.dds", iXx, iYy + 2*iGap, iButtonSize, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22203, 5, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("MovePlotLeftOne", "", "Art/Interface/Buttons/WorldBuilder/Left.dds", iXx + iGap, iYy + 2*iGap, iButtonSize, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22203, 1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("MovePlotRightOne", "", "Art/Interface/Buttons/WorldBuilder/Right.dds", iXx + 3*iGap, iYy + 2*iGap, iButtonSize, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22204, 1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("MovePlotRightFive", "", "Art/Interface/Buttons/WorldBuilder/Right5.dds", iXx + 4*iGap, iYy + 2*iGap, iButtonSize, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22204, 5, ButtonStyles.BUTTON_STYLE_STANDARD)

		# Multiplot buttons
		iWidthButtons = 100
		iXx = iXx - 2*iWidthButtons - 2*20
		iXxx = iXx + iWidthButtons + iAdjust
		iYy = iYy + iGap
		iPanelWidth = 2*iWidthButtons + 3*iAdjust
		screen.setText("MultiPlotText", "", CyTranslator().getText("TXT_KEY_WB_MULTITILE", ()), -1, iXx - iAdjust + iPanelWidth/2, iYy - 25, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel("MultiPlotPanel", "", "", False, False, iXx - iAdjust, iYy - iAdjust, iPanelWidth, 4*iGap + iAdjust, PanelStyles.PANEL_STYLE_IN)
		screen.setButtonGFC("StartMultiTile", CyTranslator().getText("TXT_KEY_WB_START", ()), "", iXx, iYy, iWidthButtons, iButtonSize, WidgetTypes.WIDGET_PYTHON, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("EndMultiTile", CyTranslator().getText("TXT_KEY_WB_END", ()), "", iXx, iYy + iGap, iWidthButtons, iButtonSize, WidgetTypes.WIDGET_PYTHON, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("ResetMultiTile", CyTranslator().getText("TXT_KEY_WB_RESET", ()), "", iXx, iYy + 2*iGap, iWidthButtons, iButtonSize, WidgetTypes.WIDGET_PYTHON, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

		if iMode == 14:
			screen.setButtonGFC("MultiAdd", CyTranslator().getText("TXT_KEY_WB_CITY_ADD", ()), "", iXxx, iYy, iWidthButtons, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22207, 0, ButtonStyles.BUTTON_STYLE_STANDARD)
			screen.setButtonGFC("MultiRemove", CyTranslator().getText("TXT_KEY_WB_CITY_REMOVE", ()), "", iXxx, iYy + iGap, iWidthButtons, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22207, 1, ButtonStyles.BUTTON_STYLE_STANDARD)
			screen.setButtonGFC("MultiReplace", CyTranslator().getText("TXT_KEY_WB_REPLACE", ()), "", iXxx, iYy + 2*iGap, iWidthButtons, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22207, 2, ButtonStyles.BUTTON_STYLE_STANDARD)
			screen.setButtonGFC("MultiChangeSettlerValue", CyTranslator().getText("TXT_KEY_WB_SETTLERVALUE", ()), "", iXxx, iYy + 3*iGap, iWidthButtons, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22207, 3, ButtonStyles.BUTTON_STYLE_STANDARD)
		else:
			screen.setButtonGFC("MultiAdd", CyTranslator().getText("TXT_KEY_WB_CITY_ADD", ()), "", iXxx, iYy, iWidthButtons, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22208, 0, ButtonStyles.BUTTON_STYLE_STANDARD)
			screen.setButtonGFC("MultiRemove", CyTranslator().getText("TXT_KEY_WB_CITY_REMOVE", ()), "", iXxx, iYy + iGap, iWidthButtons, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22208, 1, ButtonStyles.BUTTON_STYLE_STANDARD)
			screen.setButtonGFC("MultiReplace", CyTranslator().getText("TXT_KEY_WB_REPLACE", ()), "", iXxx, iYy + 2*iGap, iWidthButtons, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22208, 2, ButtonStyles.BUTTON_STYLE_STANDARD)

		# Revert and export buttons
		iXx = iXx - 2*iWidthButtons - 2*20
		iXxx = iXx + iWidthButtons + iAdjust
		screen.setText("RevertChangesText", "", CyTranslator().getText("TXT_KEY_WB_REVERT_CHANGES", ()), -1, iXx - iAdjust + iPanelWidth/2, iYy - 25, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel("UtilsPanel", "", "", False, False, iXx - iAdjust, iYy - iAdjust, 2*iWidthButtons + 3*iAdjust, 4*iGap + iAdjust, PanelStyles.PANEL_STYLE_IN)
		screen.setButtonGFC("ClearCore", CyTranslator().getText("TXT_KEY_WB_CORE", ()), "", iXx, iYy, iWidthButtons, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22350, 1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("ClearCoreAll", CyTranslator().getText("TXT_KEY_WB_CORE", ()), "", iXxx, iYy, iWidthButtons, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22351, 2, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("ClearFlip", CyTranslator().getText("TXT_KEY_WB_IN_SPAWN", ()), "", iXx, iYy + 1*iGap, iWidthButtons, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22350, 3, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("ClearFlipAll", CyTranslator().getText("TXT_KEY_WB_IN_SPAWN", ()), "", iXxx, iYy + 1*iGap, iWidthButtons, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22351, 4, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("ClearSettler", CyTranslator().getText("TXT_KEY_WB_SETTLERVALUE", ()), "", iXx, iYy + 2*iGap, iWidthButtons, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22350, 5, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("ClearSettlerAll", CyTranslator().getText("TXT_KEY_WB_SETTLERVALUE", ()), "", iXxx, iYy + 2*iGap, iWidthButtons, iButtonSize, WidgetTypes.WIDGET_PYTHON, 22351, 6, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("Export", CyTranslator().getText("TXT_KEY_WB_EXPORT", ()), "", iXx, iYy + 3*iGap, 2*iWidthButtons + iAdjust, iButtonSize, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

	def placeMap(self):
		screen = CyGInterfaceScreen("WBInfoScreen", CvScreenEnums.WB_INFO)
		iX = screen.getXResolution()/3 + 20
		iY = self.iTable_Y
		iWidth = screen.getXResolution() * 2/3 - 40
		iMaxHeight = screen.getYResolution() * 2/3 - iY
		
		iHeight = iWidth * CyMap().getGridHeight() / CyMap().getGridWidth()
		if iHeight > iMaxHeight:
			iWidth = iMaxHeight * CyMap().getGridWidth() / CyMap().getGridHeight()
			iHeight = iMaxHeight

		self.replayInfo = CyReplayInfo()
		self.replayInfo.createInfo(iSelectedPlayer)
		screen.setMinimapMap(self.replayInfo, iX, iX + iWidth, iY, iY + iHeight, -2.3)
		screen.updateMinimapSection(True, False)
		screen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_REPLAY)
		for iX in range(self.replayInfo.getMapWidth()):
			for iY in range(self.replayInfo.getMapHeight()):
				pPlot = CyMap().plot(iX, iY)
				if pPlot.isNone(): continue
				iColor = gc.getInfoTypeForString("COLOR_CLEAR")
				iOwner = pPlot.getOwner()
				if iOwner > -1:
					iColor = self.replayInfo.getColor(iOwner)
				screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_REPLAY, iX, iY, iColor, 0.6)

	def refreshMap(self):
		screen = CyGInterfaceScreen("WBInfoScreen", CvScreenEnums.WB_INFO)
		global lSelectedItem
		global tCurrentPlot
		global lSquareSelection
		screen.minimapClearAllFlashingTiles()
		sHeader = ""
		if iItem == -1 and iMode != 14 and iMode != 15:
			screen.hide("InfoHeader")
			return

		iColorA = gc.getInfoTypeForString(self.iColorA)
		iColorB = gc.getInfoTypeForString(self.iColorB)
		iX = screen.getXResolution()/3 + 20
		iY = screen.getYResolution() *2/3 + 30
		iWidth = screen.getXResolution() * 2/3 - 40
		iHeight = (screen.getYResolution() - iY - 40) / 24 * 24 + 2

		nColumns = iWidth / self.iMinColWidth
		if iMode < 14:
			screen.addTableControlGFC("PlotTable", nColumns, iX, iY, iWidth, iHeight, False, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
			for i in xrange(nColumns):
				screen.setTableColumnHeader("PlotTable", i, "", iWidth/nColumns)

		iCount = 0
		iMaxRows = -1
		if iItem != -1 and iMode != 14 and iMode != 15:
			lTemp = lItems[iItem][5]
			if not lSelectedItem in lTemp:
				if len(lTemp) > 0:
					lSelectedItem = lTemp[0]
				else:
					lSelectedItem = [-1, -1]
			sHeader = self.Mode[iMode](iItem).getDescription()
		else:
			if iItem != -1:
				sHeader = gc.getCivilizationInfo(gc.getPlayer(iItem).getCivilizationType()).getShortDescription(0)
			else:
				sHeader = u" (%d,%d)" %(tCurrentPlot[0], tCurrentPlot[1])
		screen.setLabel("InfoHeader", "Background", "<font=4b>" + sHeader + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 20, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.bringMinimapToFront()

		if iItem != -1 and iMode != 14 and iMode != 15:
			if not lSelectedItem in lTemp:
				screen.hide("PlotData")
				return
		self.placePlotData()

		if iMode < 2:
			for lPlots in lTemp:
				iPlayer = lPlots[0]
				iUnit = lPlots[1]
				pPlayer = gc.getPlayer(iPlayer)
				pUnit = pPlayer.getUnit(iUnit)
				if pUnit.isNone(): continue
				pPlot = pUnit.plot()
				iX = pPlot.getX()
				iY = pPlot.getY()
				iColumn = iCount % nColumns
				iRow = iCount / nColumns
				if iRow > iMaxRows:
					screen.appendTableRow("PlotTable")
					iMaxRows = iRow
				iCount += 1
				sColor = u"<color=%d,%d,%d,%d>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA())
				sText = sColor + pUnit.getName()
				screen.setTableText("PlotTable", iColumn, iRow, "<font=3>" + sText + "</color></font>", pUnit.getButton(), WidgetTypes.WIDGET_PYTHON, 8300 + iPlayer, iUnit, CvUtil.FONT_LEFT_JUSTIFY)
				screen.minimapFlashPlot(iX, iY, iColorB, -1)
			pUnit = gc.getPlayer(lSelectedItem[0]).getUnit(lSelectedItem[1])
			if pUnit:
				screen.minimapFlashPlot(pUnit.getX(), pUnit.getY(), iColorA, -1)
		elif iMode < 6:
			for lPlots in lItems[iItem][5]:
				iPlayer = lPlots[0]
				iCity = lPlots[1]
				pPlayer = gc.getPlayer(iPlayer)
				pCity = pPlayer.getCity(iCity)
				if pCity.isNone(): continue
				pPlot = pCity.plot()
				iX = pPlot.getX()
				iY = pPlot.getY()
				iColumn = iCount % nColumns
				iRow = iCount / nColumns
				if iRow > iMaxRows:
					screen.appendTableRow("PlotTable")
					iMaxRows = iRow
				iCount += 1
				sColor = u"<color=%d,%d,%d,%d>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA())
				sText = sColor + pCity.getName()
				sButton = gc.getCivilizationInfo(pCity.getCivilizationType()).getButton()
				screen.setTableText("PlotTable", iColumn, iRow, "<font=3>" + sText + "</color></font>", sButton, WidgetTypes.WIDGET_PYTHON, 7200 + iPlayer, iCity, CvUtil.FONT_LEFT_JUSTIFY)
				screen.minimapFlashPlot(iX, iY, iColorB, -1)
				if lSelectedItem == lPlots:
					screen.minimapFlashPlot(iX, iY, iColorA, -1)
		elif iMode < 11:
			for lPlots in lItems[iItem][5]:
				iX = lPlots[0]
				iY = lPlots[1]
				pPlot = CyMap().plot(iX, iY)
				if pPlot.isNone(): continue
				iColumn = iCount % nColumns
				iRow = iCount / nColumns
				if iRow > iMaxRows:
					screen.appendTableRow("PlotTable")
					iMaxRows = iRow
				iCount += 1
				sColor = ""
				sButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
				iOwner = pPlot.getOwner()
				if iOwner > -1:
					pPlayer = gc.getPlayer(iOwner)
					sColor = u"<color=%d,%d,%d,%d>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA())
					sButton = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getButton()
				sText = u"%s(%d, %d)" % (sColor, iX, iY)
				screen.setTableText("PlotTable", iColumn, iRow, "<font=3>" + sText + "</color></font>", sButton, WidgetTypes.WIDGET_PYTHON, 1027, iX * 10000 + iY, CvUtil.FONT_CENTER_JUSTIFY)
				screen.minimapFlashPlot(iX, iY, iColorB, -1)
				if lSelectedItem == lPlots:
					screen.minimapFlashPlot(iX, iY, iColorA, -1)
		elif iMode < 14:
			for lPlots in lItems[iItem][5]:
				iPlayer = lPlots[0]
				if iMode > 11:
					iPlayer = gc.getTeam(lPlots[0]).getLeaderID()
				iColumn = iCount % nColumns
				iRow = iCount / nColumns
				if iRow > iMaxRows:
					screen.appendTableRow("PlotTable")
					iMaxRows = iRow
				iCount += 1
				pPlayer = gc.getPlayer(iPlayer)
				iLeader = pPlayer.getLeaderType()
				sColor = u"<color=%d,%d,%d,%d>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA())
				sButton = gc.getLeaderHeadInfo(iLeader).getButton()
				sText = u"%s%s" % (sColor, pPlayer.getName())
				screen.setTableText("PlotTable", iColumn, iRow, "<font=3>" + sText + "</color></font>", sButton, WidgetTypes.WIDGET_PYTHON, 7876, iPlayer * 10000 + iLeader, CvUtil.FONT_LEFT_JUSTIFY)
		else:
			if iMode == 14 and iItem != -1:
				iPlayer = iItem
				tCapital = Areas.getCapital(iPlayer)
				for x in range(con.iWorldX):
					for y in range(con.iWorldY):
						plot = gc.getMap().plot(x, y)
						if plot.isWater(): continue
						if gc.getMap().plot(x, y).isCore(iPlayer):
							iPlotType = 0
						else:
							iSettlerValue = md.getSettlerValue(iPlayer, (x, y))
							if iSettlerValue == 3:
								if bHideForbidden: continue
								iPlotType = 5
							elif iSettlerValue >= 90:
								if Areas.isForeignCore(iPlayer, (x, y)):
									iPlotType = 2
								else:
									iPlotType = 1
							else:
								iPlotType = -1
						if iPlotType != -1:
							iColor = gc.getInfoTypeForString(self.lColors[iPlotType])
							screen.minimapFlashPlot(x, y, iColor, -1)

			elif iMode == 15 and iItem != -1:
				iColorS = gc.getInfoTypeForString(self.iColorSpawn)
				iColorSW = gc.getInfoTypeForString(self.iColorSpawnWater)
				iColorC = gc.getInfoTypeForString(self.lColors[2])
				iPlayer = iItem
				for tPlot in Areas.getBirthArea(iPlayer):
					plot = gc.getMap().plot(tPlot[0], tPlot[1])
					if plot.isWater():  screen.minimapFlashPlot(tPlot[0], tPlot[1], iColorSW, -1)
					else: screen.minimapFlashPlot(tPlot[0], tPlot[1], iColorS, -1)
				x, y = Areas.getCapital(iPlayer)
				screen.minimapFlashPlot(x, y, iColorC, -1)

			if lSquareSelection[2]:
				if lSquareSelection[1] == -1:
					tEndPlot = tCurrentPlot
				else:
					tEndPlot = lSquareSelection[1]
				tBL = (min(lSquareSelection[0][0], tEndPlot[0]), min(lSquareSelection[0][1], tEndPlot[1]))
				tTR = (max(lSquareSelection[0][0], tEndPlot[0]), max(lSquareSelection[0][1], tEndPlot[1]))
				lPlotList = utils.getPlotList(tBL, tTR)
				if iMode == 14:
					iColor = gc.getInfoTypeForString(self.iColorSpawn)
				else:
					iColor = gc.getInfoTypeForString(self.lColors[1])
				for tPlot in lPlotList:
					screen.minimapFlashPlot(tPlot[0], tPlot[1], iColor, -1)

			screen.minimapFlashPlot(tCurrentPlot[0], tCurrentPlot[1], iColorB, -1)

	def placeItems(self):
		screen = CyGInterfaceScreen("WBInfoScreen", CvScreenEnums.WB_INFO)
		global iItem
		global lItems

		iX = 20
		iY = self.iTable_Y - 20
		iWidth = screen.getXResolution()/3 - 20
		iHeight = (screen.getYResolution() - iY - 40) / 24 * 24 + 2

		screen.addTableControlGFC("InfoTable", 3, iX, iY, iWidth, iHeight, True, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("InfoTable", 0, "<font=3>" + CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()) + "</font>", iWidth/2)
		screen.setTableColumnHeader("InfoTable", 1, "<font=3>" + gc.getPlayer(iSelectedPlayer).getName() + "</font>", iWidth/4)
		screen.setTableColumnHeader("InfoTable", 2, "<font=3>" + CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + "</font>", iWidth/4)
		screen.enableSort("InfoTable")

		lItems = []
		if iMode == 0:
			iData1 = 8202
			for i in xrange(gc.getNumUnitInfos()):
				Info = gc.getUnitInfo(i)
				lItems.append([Info.getDescription(), 0, 0, i, Info.getButton(), []])
			for iPlayerX in xrange(gc.getMAX_PLAYERS()):
				pPlayerX = gc.getPlayer(iPlayerX)
				if pPlayerX.isAlive():
					(loopUnit, i) = pPlayerX.firstUnit(False)
					while(loopUnit):
						iItemX = loopUnit.getUnitType()
						if iPlayerX == iSelectedPlayer:
							lItems[iItemX][1] += 1
						lItems[iItemX][2] += 1
						if not [loopUnit.getX(), loopUnit.getY()] in lItems[iItemX][5]:
							lItems[iItemX][5].append([iPlayerX, loopUnit.getID()])
						(loopUnit, i) = pPlayerX.nextUnit(i, False)
		elif iMode == 1:
			iData1 = 7873
			for i in xrange(gc.getNumPromotionInfos()):
				Info = gc.getPromotionInfo(i)
				lItems.append([Info.getDescription(), 0, 0, i, Info.getButton(), []])
			for iPlayerX in xrange(gc.getMAX_PLAYERS()):
				pPlayerX = gc.getPlayer(iPlayerX)
				if pPlayerX.isAlive():
					(loopUnit, i) = pPlayerX.firstUnit(False)
					while(loopUnit):
						for iItemX in xrange(gc.getNumPromotionInfos()):
							if loopUnit.isHasPromotion(iItemX):
								if iPlayerX == iSelectedPlayer:
									lItems[iItemX][1] += 1
								lItems[iItemX][2] += 1
								if not [loopUnit.getX(), loopUnit.getY()] in lItems[iItemX][5]:
									lItems[iItemX][5].append([iPlayerX, loopUnit.getID()])
						(loopUnit, i) = pPlayerX.nextUnit(i, False)
		elif iMode == 2:
			iData1 = 7870
			for i in xrange(gc.getNumBuildingInfos()):
				Info = gc.getBuildingInfo(i)
				lItems.append([Info.getDescription(), 0, 0, i, Info.getButton(), []])
			for iPlayerX in xrange(gc.getMAX_PLAYERS()):
				pPlayerX = gc.getPlayer(iPlayerX)
				if pPlayerX.isAlive():
					(loopCity, i) = pPlayerX.firstCity(False)
					while(loopCity):
						for iItemX in xrange(gc.getNumBuildingInfos()):
							if loopCity.isHasBuilding(iItemX):
								if iPlayerX == iSelectedPlayer:
									lItems[iItemX][1] += 1
								lItems[iItemX][2] += 1
								if not [loopCity.getX(), loopCity.getY()] in lItems[iItemX][5]:
									lItems[iItemX][5].append([iPlayerX, loopCity.getID()])
						(loopCity, i) = pPlayerX.nextCity(i, False)
		elif iMode == 3:
			iData1 = 7879
			pPlayer = gc.getPlayer(iSelectedPlayer)
			for i in xrange(gc.getNumSpecialistInfos()):
				Info = gc.getSpecialistInfo(i)
				lItems.append([Info.getDescription(), 0, 0, i, Info.getButton(), []])
			for iPlayerX in xrange(gc.getMAX_PLAYERS()):
				pPlayerX = gc.getPlayer(iPlayerX)
				if pPlayerX.isAlive():
					(loopCity, i) = pPlayerX.firstCity(False)
					while(loopCity):
						for iItemX in xrange(gc.getNumSpecialistInfos()):
							iCount = loopCity.getSpecialistCount(iItemX) + loopCity.getFreeSpecialistCount(iItemX)
							if iCount > 0:
								if iPlayerX == iSelectedPlayer:
									lItems[iItemX][1] += iCount
								lItems[iItemX][2] += iCount
								if not [loopCity.getX(), loopCity.getY()] in lItems[iItemX][5]:
									lItems[iItemX][5].append([iPlayerX, loopCity.getID()])
						(loopCity, i) = pPlayerX.nextCity(i, False)
		elif iMode == 4:
			iData1 = 7869
			pPlayer = gc.getPlayer(iSelectedPlayer)
			for i in xrange(gc.getNumReligionInfos()):
				Info = gc.getReligionInfo(i)
				lItems.append([Info.getDescription(), pPlayer.getHasReligionCount(i), CyGame().countReligionLevels(i), i, Info.getButton(), []])
			for i in xrange(CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if pPlot.isNone(): continue
				if pPlot.isCity():
					pCity = pPlot.getPlotCity()
					for iItemX in xrange(gc.getNumReligionInfos()):
						if pCity.isHasReligion(iItemX):
							if [pPlot.getX(), pPlot.getY()] in lItems[iItemX][5]: continue
							lItems[iItemX][5].append([pCity.getOwner(), pCity.getID()])
		elif iMode == 5:
			iData1 = 8201
			pPlayer = gc.getPlayer(iSelectedPlayer)
			for i in xrange(gc.getNumCorporationInfos()):
				Info = gc.getCorporationInfo(i)
				lItems.append([Info.getDescription(), pPlayer.getHasCorporationCount(i), CyGame().countCorporationLevels(i), i, Info.getButton(), []])
			for i in xrange(CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if pPlot.isNone(): continue
				if pPlot.isCity():
					pCity = pPlot.getPlotCity()
					for iItemX in xrange(gc.getNumCorporationInfos()):
						if pCity.isHasCorporation(iItemX):
							if [pPlot.getX(), pPlot.getY()] in lItems[iItemX][5]: continue
							lItems[iItemX][5].append([pCity.getOwner(), pCity.getID()])
		elif iMode == 6:
			iData1 = 7875
			for i in xrange(gc.getNumTerrainInfos()):
				Info = gc.getTerrainInfo(i)
				lItems.append([Info.getDescription(), 0, 0, i, Info.getButton(), []])
			for i in xrange(CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if pPlot.isNone(): continue
				iItemX = pPlot.getTerrainType()
				if iItemX == -1: continue
				iOwner = pPlot.getOwner()
				if iOwner == iSelectedPlayer:
					lItems[iItemX][1] += 1
				lItems[iItemX][2] += 1
				if [pPlot.getX(), pPlot.getY()] in lItems[iItemX][5]: continue
				lItems[iItemX][5].append([pPlot.getX(), pPlot.getY()])
		elif iMode == 7:
			iData1 = 7874
			for i in xrange(gc.getNumFeatureInfos()):
				Info = gc.getFeatureInfo(i)
				lItems.append([Info.getDescription(), 0, 0, i, Info.getButton(), []])
			for i in xrange(CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if pPlot.isNone(): continue
				iItemX = pPlot.getFeatureType()
				if iItemX == -1: continue
				iOwner = pPlot.getOwner()
				if iOwner == iSelectedPlayer:
					lItems[iItemX][1] += 1
				lItems[iItemX][2] += 1
				if [pPlot.getX(), pPlot.getY()] in lItems[iItemX][5]: continue
				lItems[iItemX][5].append([pPlot.getX(), pPlot.getY()])
		elif iMode == 8:
			iData1 = 7878
			for i in xrange(gc.getNumBonusInfos()):
				Info = gc.getBonusInfo(i)
				lItems.append([Info.getDescription(), 0, 0, i, Info.getButton(), []])
			for i in xrange(CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if pPlot.isNone(): continue
				iItemX = pPlot.getBonusType(-1)
				if iItemX == -1: continue
				iOwner = pPlot.getOwner()
				if iOwner == iSelectedPlayer:
					lItems[iItemX][1] += 1
				lItems[iItemX][2] += 1
				if [pPlot.getX(), pPlot.getY()] in lItems[iItemX][5]: continue
				lItems[iItemX][5].append([pPlot.getX(), pPlot.getY()])
		elif iMode == 9:
			iData1 = 7877
			for i in xrange(gc.getNumImprovementInfos()):
				Info = gc.getImprovementInfo(i)
				lItems.append([Info.getDescription(), 0, 0, i, Info.getButton(), []])
			for i in xrange(CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if pPlot.isNone(): continue
				iItemX = pPlot.getImprovementType()
				if iItemX == -1: continue
				iOwner = pPlot.getOwner()
				if iOwner == iSelectedPlayer:
					lItems[iItemX][1] += 1
				lItems[iItemX][2] += 1
				if [pPlot.getX(), pPlot.getY()] in lItems[iItemX][5]: continue
				lItems[iItemX][5].append([pPlot.getX(), pPlot.getY()])
		elif iMode == 10:
			iData1 = 6788
			for i in xrange(gc.getNumRouteInfos()):
				Info = gc.getRouteInfo(i)
				lItems.append([Info.getDescription(), 0, 0, i, Info.getButton(), []])
			for i in xrange(CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if pPlot.isNone(): continue
				iItemX = pPlot.getRouteType()
				if iItemX == -1: continue
				iOwner = pPlot.getOwner()
				if iOwner == iSelectedPlayer:
					lItems[iItemX][1] += 1
				lItems[iItemX][2] += 1
				if [pPlot.getX(), pPlot.getY()] in lItems[iItemX][5]: continue
				lItems[iItemX][5].append([pPlot.getX(), pPlot.getY()])
		elif iMode == 11:
			iData1 = 8205
			for i in xrange(gc.getNumCivicInfos()):
				Info = gc.getCivicInfo(i)
				lItems.append([Info.getDescription(), 0, 0, i, Info.getButton(), []])
			for iPlayerX in xrange(gc.getMAX_PLAYERS()):
				pPlayerX = gc.getPlayer(iPlayerX)
				if pPlayerX.isAlive():
					for iItemX in xrange(gc.getNumCivicInfos()):
						if pPlayerX.isCivic(iItemX):
							if iPlayerX == iSelectedPlayer:
								lItems[iItemX][1] += 1
							lItems[iItemX][2] += 1
							lItems[iItemX][5].append([iPlayerX, -1])
		elif iMode == 12:
			iData1 = 7871
			for i in xrange(gc.getNumTechInfos()):
				Info = gc.getTechInfo(i)
				lItems.append([Info.getDescription(), 0, 0, i, Info.getButton(), []])
			for iTeamX in xrange(gc.getMAX_TEAMS()):
				pTeamX = gc.getTeam(iTeamX)
				if pTeamX.isAlive():
					for iItemX in xrange(gc.getNumTechInfos()):
						iCount = pTeamX.isHasTech(iItemX)
						if gc.getTechInfo(iItemX).isRepeat():
							iCount = pTeamX.getTechCount(iItemX)
						if iCount > 0:
							if iTeamX == gc.getPlayer(iSelectedPlayer).getTeam():
								lItems[iItemX][1] += iCount
							lItems[iItemX][2] += iCount
							lItems[iItemX][5].append([iTeamX, -1])
		elif iMode == 13:
			iData1 = 6785
			for i in xrange(gc.getNumProjectInfos()):
				Info = gc.getProjectInfo(i)
				lItems.append([Info.getDescription(), 0, 0, i, Info.getButton(), []])
			for iTeamX in xrange(gc.getMAX_TEAMS()):
				pTeamX = gc.getTeam(iTeamX)
				if pTeamX.isAlive():
					for iItemX in xrange(gc.getNumProjectInfos()):
						iCount = pTeamX.getProjectCount(iItemX)
						if iCount > 0:
							if iTeamX == gc.getPlayer(iSelectedPlayer).getTeam():
								lItems[iItemX][1] += iCount
							lItems[iItemX][2] += iCount
							lItems[iItemX][5].append([iTeamX, -1])
		if iItem > -1:
			if lItems[iItem][2] == 0:
				iItem = -1

		for item in lItems:
			if CvPlatyBuilderScreen.bHideInactive and item[2] == 0: continue
			if iItem == -1:
				iItem = item[3]
			iRow = screen.appendTableRow("InfoTable")
			screen.setTableText("InfoTable", 0, iRow, "<font=3>" + item[0] + "</font>", item[4], WidgetTypes.WIDGET_PYTHON, iData1, item[3], CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableInt("InfoTable", 1, iRow, "<font=3>" + str(item[1]) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("InfoTable", 2, iRow, "<font=3>" + str(item[2]) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

	def placeItemsStabMap(self):
		screen = CyGInterfaceScreen("WBInfoScreen", CvScreenEnums.WB_INFO)
		iX = 20
		iY = self.iTable_Y - 20
		iWidth = screen.getXResolution()/3 - 20
		iHeight = (screen.getYResolution() - iY - 40) / 24 * 24 + 2
		global tCurrentPlot
		global iChangeType

		# Merijn StabMap
		if iMode == 14:
			screen.addTableControlGFC("InfoTable", 5, iX, iY, iWidth, iHeight, True, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
			screen.setTableColumnHeader("InfoTable", 0, "<font=3>" + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIV", ()) + "</font>", iWidth/4-18)
			screen.setTableColumnHeader("InfoTable", 1, "<font=3>" + CyTranslator().getText("TXT_KEY_WB_CORE", ()) + "</font>", iWidth/10-5)
			screen.setTableColumnHeader("InfoTable", 2, "<font=3>" + CyTranslator().getText("TXT_KEY_WB_SETTLERVALUE", ()) + "</font>", iWidth/20*3-5)
			screen.setTableColumnHeader("InfoTable", 3, "<font=3>" + CyTranslator().getText("TXT_KEY_WB_RESULT", ()) + "</font>", iWidth/20*7-5)
			screen.setTableColumnHeader("InfoTable", 4, "<font=3>" + CyTranslator().getText("TXT_KEY_WB_EXTENDED_MAP", ()) + "</font>", iWidth/10*3-75)

			for iPlayer in range(con.iNumPlayers):
				iCiv = gc.getPlayer(iPlayer).getCivilizationType()
				iSettlerValue = md.getSettlerValue(iPlayer, tCurrentPlot)
				if gc.getMap().plot(tCurrentPlot[0], tCurrentPlot[1]).isCore(iPlayer):
					sCore = u"%c" %(CyGame().getSymbolID(FontSymbols.SUCCESS_CHAR))
					iPlotType = 0
				else:
					sCore = u"%c" %(CyGame().getSymbolID(FontSymbols.FAILURE_CHAR))
					bForeignCore = Areas.isForeignCore(iPlayer, tCurrentPlot)
					if iSettlerValue >= 90:
						if bForeignCore:
							iPlotType = 2
						else:
							iPlotType = 1
					elif bForeignCore:
						iPlotType = 3
					else:
						iPlotType = 4

				iColor = gc.getInfoTypeForString(self.lColors[iPlotType])
				sPlotText = CyTranslator().changeTextColor(self.lPlotNumberText[iPlotType], iColor)
				if not bHideForbidden and iSettlerValue == 3:
					iColor = gc.getInfoTypeForString(self.lColors[5])
					sPlotText += CyTranslator().changeTextColor(self.lPlotNumberText[5], iColor)

				lExtended = [con.iTurkey, con.iByzantium, con.iCarthage, con.iMongolia, con.iSpain, con.iMoors, con.iItaly, con.iArabia, con.iJapan, con.iGermany, con.iHolyRome, con.iKhmer, con.iGreece, con.iChina] 
				if iPlayer not in lExtended:
					tExtend = ("", 0)
				else:
					if utils.getReborn(iPlayer):
						tExtend = (u"%c" %(CyGame().getSymbolID(FontSymbols.SUCCESS_CHAR)), 1)
					else:
						tExtend = (u"%c" %(CyGame().getSymbolID(FontSymbols.FAILURE_CHAR)), 1)

				iRow = screen.appendTableRow("InfoTable")
				screen.setTableText("InfoTable", 0, iRow, "<font=3>" + gc.getCivilizationInfo(iCiv).getShortDescription(0) + "</font>", gc.getCivilizationInfo(iCiv).getButton(), WidgetTypes.WIDGET_PYTHON, 22100 + iPlayer, 2000, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText("InfoTable", 1, iRow, sCore, "", WidgetTypes.WIDGET_PYTHON, 22171, iPlayer, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableInt("InfoTable", 2, iRow, "<font=3>" + str(iSettlerValue) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 22172, iPlayer, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableText("InfoTable", 3, iRow, "<font=3>" + sPlotText + "</font>", "", WidgetTypes.WIDGET_PYTHON, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableText("InfoTable", 4, iRow, tExtend[0], "", WidgetTypes.WIDGET_PYTHON, 22100 + iPlayer, tExtend[1], CvUtil.FONT_CENTER_JUSTIFY)

			self.placeValueChanger()

		# Merijn Spawnmap
		else:
			screen.addTableControlGFC("InfoTable", 2, iX, iY, iWidth, iHeight, True, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
			screen.setTableColumnHeader("InfoTable", 0, "<font=3>" + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIV", ()) + "</font>", iWidth/2)
			screen.setTableColumnHeader("InfoTable", 1, "<font=3>" + CyTranslator().getText("TXT_KEY_WB_IN_SPAWN", ()) + "</font>", iWidth/2-18)

			for iPlayer in range(con.iNumPlayers):
				iCiv = gc.getPlayer(iPlayer).getCivilizationType()
				if tCurrentPlot in Areas.getBirthArea(iPlayer):
					sSpawn = u"%c" %(CyGame().getSymbolID(FontSymbols.SUCCESS_CHAR))
				else:
					sSpawn = u"%c" %(CyGame().getSymbolID(FontSymbols.FAILURE_CHAR))

				iRow = screen.appendTableRow("InfoTable")
				screen.setTableText("InfoTable", 0, iRow, "<font=3>" + gc.getCivilizationInfo(iCiv).getShortDescription(0) + "</font>", gc.getCivilizationInfo(iCiv).getButton(), WidgetTypes.WIDGET_PYTHON, 22100 + iPlayer, 2001, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText("InfoTable", 1, iRow, sSpawn, "", WidgetTypes.WIDGET_PYTHON, 22176, iPlayer, CvUtil.FONT_CENTER_JUSTIFY)

	def placeValueChanger(self):
		screen = CyGInterfaceScreen("WBInfoScreen", CvScreenEnums.WB_INFO)

		iX = screen.getXResolution()/3 + 20
		iY = self.iTable_Y
		iWidth = screen.getXResolution() * 2/3 - 40
		iMaxHeight = screen.getYResolution() * 2/3 - iY		
		iHeight = iWidth * CyMap().getGridHeight() / CyMap().getGridWidth()
		if iHeight > iMaxHeight:
			iWidth = iMaxHeight * CyMap().getGridWidth() / CyMap().getGridHeight()
			iHeight = iMaxHeight

		iYy = iY + iHeight + 10
		screen.setButtonGFC("HideForbidden", CyTranslator().getText("TXT_KEY_WB_TOGGLE_AI_FORBIDDEN", ()), "", iX, iYy, 160, 35, WidgetTypes.WIDGET_PYTHON, 22206, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

		if iChangeType == 2:
			screen.addTableControlGFC("SetValueBox", 1, iX + 30, iYy + 40, 100, 26, False, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
			screen.setTableColumnHeader("SetValueBox", 1, "", 100)
			screen.setTableText("SetValueBox", 0, 0, str(iSetValue), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

			screen.setButtonGFC("SetValueDecrease", "", "", iX, iYy + 40, 26, 26, WidgetTypes.WIDGET_PYTHON, 22300, iChange, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
			screen.setButtonGFC("SetValueIncrease", "", "", iX + 30 + 100 + 4, iYy + 40, 26, 26, WidgetTypes.WIDGET_PYTHON, 22400, iChange, ButtonStyles.BUTTON_STYLE_CITY_PLUS)

			screen.addDropDownBoxGFC("PresetValue", iX, iYy + 30 + 40, 160, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for i in range(len(self.lPresetValues)):
				screen.addPullDownString("PresetValue", str(self.lPresetValues[i]), i, self.lPresetValues[i], False)

	def handleInput(self, inputClass):
		screen = CyGInterfaceScreen("WBInfoScreen", CvScreenEnums.WB_INFO)
		global iSelectedPlayer
		global iItem
		global iMode
		global lSelectedItem
		
		#Merijn Globals
		global iChange
		global iChangeType
		global tCurrentPlot
		global iSetValue
		global bHideForbidden
		global lSquareSelection

		if inputClass.getFunctionName() == "ChangeBy":
			iChange = screen.getPullDownData("ChangeBy", screen.getSelectedPullDownID("ChangeBy"))
			if iChangeType == 2:
				self.placeValueChanger()
		elif inputClass.getFunctionName() == "ChangeType":
			iChangeType = screen.getPullDownData("ChangeType", screen.getSelectedPullDownID("ChangeType"))
			if iChangeType == 2:
				self.placeValueChanger()
			else:
				screen.hide("SetValueBox")
				screen.hide("SetValueIncrease")
				screen.hide("SetValueDecrease")
				screen.hide("PresetValue")

		elif inputClass.getFunctionName() == "SetValueIncrease":
			iSetValue += iChange
			screen.setTableText("SetValueBox", 0, 0, str(iSetValue), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
		elif inputClass.getFunctionName() == "SetValueDecrease":
			iSetValue = max(iSetValue-iChange,0)
			screen.setTableText("SetValueBox", 0, 0, str(iSetValue), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
		elif inputClass.getFunctionName() == "PresetValue":
			iSetValue = screen.getPullDownData("PresetValue", screen.getSelectedPullDownID("PresetValue"))
			screen.setTableText("SetValueBox", 0, 0, str(iSetValue), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

		elif inputClass.getFunctionName() == "PlotData":
			if iMode == 0:
				pUnit = gc.getPlayer(lSelectedItem[0]).getUnit(lSelectedItem[1])
				if pUnit:
					WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).interfaceScreen(pUnit)
			elif iMode == 1:
				pUnit = gc.getPlayer(lSelectedItem[0]).getUnit(lSelectedItem[1])
				if pUnit:
					WBPromotionScreen.WBPromotionScreen().interfaceScreen(pUnit)
			elif iMode < 6:
				pCity = gc.getPlayer(lSelectedItem[0]).getCity(lSelectedItem[1])
				if pCity:
					WBCityEditScreen.WBCityEditScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).interfaceScreen(pCity)
			elif iMode < 11:
				pPlot = CyMap().plot(lSelectedItem[0], lSelectedItem[1])
				if not pPlot.isNone():
					WBPlotScreen.WBPlotScreen().interfaceScreen(pPlot)
			elif iMode == 11:
				WBPlayerScreen.WBPlayerScreen().interfaceScreen(lSelectedItem[0])
			elif iMode == 12:
				WBTechScreen.WBTechScreen().interfaceScreen(lSelectedItem[0])
			elif iMode == 13:
				WBProjectScreen.WBProjectScreen().interfaceScreen(lSelectedItem[0])
			elif iMode == 14 or iMode == 15:
				WBPlotScreen.WBPlotScreen().interfaceScreen(CyMap().plot(tCurrentPlot[0], tCurrentPlot[1]))

		elif inputClass.getFunctionName() == "ItemType":
			iMode = screen.getPullDownData("ItemType", screen.getSelectedPullDownID("ItemType"))
			iItem = -1
			self.interfaceScreen(iSelectedPlayer)

		elif inputClass.getFunctionName() == "CurrentPlayer":
			iSelectedPlayer = screen.getPullDownData("CurrentPlayer", screen.getSelectedPullDownID("CurrentPlayer"))
			self.interfaceScreen(iSelectedPlayer)

		elif inputClass.getFunctionName() == "InfoTable":
			if iMode < 14:
				iItem = inputClass.getData2()
				self.refreshMap()
			else:
				iData1 = inputClass.getData1()
				if iData1 == 22171:
					iPlayer = inputClass.getData2()
					md.changeCore(iPlayer, tCurrentPlot)
					self.placeItemsStabMap()
					self.refreshMap()
				elif iData1 == 22172:
					iPlayer = inputClass.getData2()
					x, y = tCurrentPlot
					if iChangeType == 0:
						iValue = md.getSettlerValue(iPlayer, (x, y)) - iChange
					elif iChangeType == 1:
						iValue = md.getSettlerValue(iPlayer, (x, y)) + iChange
					elif iChangeType == 2:
						iValue = iSetValue
					md.changeSettlerValue(iPlayer, tCurrentPlot, iValue)
					screen.setTableInt("InfoTable", 2, iPlayer, "<font=3>" + str(iValue) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 22172, iPlayer, CvUtil.FONT_CENTER_JUSTIFY)
					if iItem == iPlayer:
						self.refreshMap()
				elif iData1 == 22176:
					iPlayer = inputClass.getData2()
					md.changeFlip(iPlayer, tCurrentPlot)
					self.placeItemsStabMap()
					self.refreshMap()
				else:
					iPlayer = iData1-22100
					iData2 = inputClass.getData2()
					if iData2 == 1:
						if utils.getReborn(iPlayer) == 0:
							gc.getPlayer(iPlayer).setReborn(True)
						else:
							gc.getPlayer(iPlayer).setReborn(False)
						self.placeItemsStabMap()
						if iItem == iPlayer:
							self.refreshMap()
					elif iData2 == 2000 or iData2 == 2001:
						if iItem == iPlayer:
							iItem = -1
						else:
							iItem = iPlayer
						self.refreshMap()

		elif inputClass.getFunctionName() == "PlotTable":
			iColorA = gc.getInfoTypeForString(self.iColorA)
			iColorB = gc.getInfoTypeForString(self.iColorB)
			if iMode < 2:
				pUnit = gc.getPlayer(lSelectedItem[0]).getUnit(lSelectedItem[1])
				if pUnit:
					screen.minimapFlashPlot(pUnit.getX(), pUnit.getY(), iColorB, -1)
				iPlayer = inputClass.getData1() - 8300
				iUnit = inputClass.getData2()
				pNewUnit = gc.getPlayer(iPlayer).getUnit(iUnit)
				if pNewUnit:
					lSelectedItem = [iPlayer, iUnit]
					screen.minimapFlashPlot(pNewUnit.getX(), pNewUnit.getY(), iColorA, -1)
			elif iMode < 6:
				pCity = gc.getPlayer(lSelectedItem[0]).getCity(lSelectedItem[1])
				if pCity:
					screen.minimapFlashPlot(pCity.getX(), pCity.getY(), iColorB, -1)
				iPlayer = inputClass.getData1() - 7200
				iCity = inputClass.getData2()
				pNewCity = gc.getPlayer(iPlayer).getCity(iCity)
				if pNewCity:
					lSelectedItem = [iPlayer, iCity]
					screen.minimapFlashPlot(pNewCity.getX(), pNewCity.getY(), iColorA, -1)
			elif iMode < 11:
				iX = lSelectedItem[0]
				iY = lSelectedItem[1]
				if iX > -1 and iY > -1:
					screen.minimapFlashPlot(iX, iY, iColorB, -1)
				iX = inputClass.getData2() / 10000
				iY = inputClass.getData2() % 10000
				lSelectedItem = [iX, iY]
				screen.minimapFlashPlot(iX, iY, iColorA, -1)
			elif iMode == 11:
				iPlayerX = inputClass.getData2() /10000
				lSelectedItem = [iPlayerX, -1]
			elif iMode > 11:
				iPlayerX = inputClass.getData2() /10000
				lSelectedItem = [gc.getPlayer(iPlayerX).getTeam(), -1]
			self.placePlotData()

		elif inputClass.getFunctionName() in ["MovePlotUpOne", "MovePlotUpFive", "MovePlotDownOne", "MovePlotDownFive", "MovePlotLeftOne", "MovePlotLeftFive", "MovePlotRightOne", "MovePlotRightFive"]:
			iColorB = gc.getInfoTypeForString(self.iColorB)
			iData1 = inputClass.getData1()
			iData2 = inputClass.getData2()
			if iData1 == 22201:
				tCurrentPlot = (tCurrentPlot[0],min(max(tCurrentPlot[1]+iData2,0),con.iWorldY-1))
			elif iData1 == 22202:
				tCurrentPlot = (tCurrentPlot[0],min(max(tCurrentPlot[1]-iData2,0),con.iWorldY-1))
			elif iData1 == 22203:
				tCurrentPlot = ((tCurrentPlot[0]-iData2) % con.iWorldX,tCurrentPlot[1])
			elif iData1 == 22204:
				tCurrentPlot = ((tCurrentPlot[0]+iData2) % con.iWorldX,tCurrentPlot[1])
			self.placeItemsStabMap()
			self.refreshMap()
		elif inputClass.getFunctionName() == "Sonic":
			popup = PyPopup.PyPopup()
			popup.setBodyString(CyTranslator().getText("TXT_KEY_WB_SONIC", ()))
			popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)
			screen.setButtonGFC("Randomizer", "", gc.getMissionInfo(gc.getInfoTypeForString("MISSION_NUKE")).getButton(), inputClass.getData1(), inputClass.getData2(), 48, 48, WidgetTypes.WIDGET_PYTHON, 22199, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		elif inputClass.getFunctionName() == "StartMultiTile":
			lSquareSelection = [tCurrentPlot, -1, True]
			self.refreshMap()
		elif inputClass.getFunctionName() == "EndMultiTile":
			if lSquareSelection[1] == -1:
				lSquareSelection = [lSquareSelection[0], tCurrentPlot, True]
		elif inputClass.getFunctionName() == "ResetMultiTile":
			lSquareSelection = [-1, -1, False]
			self.refreshMap()
		elif inputClass.getFunctionName()  in ["MultiAdd", "MultiRemove", "MultiReplace", "MultiChangeSettlerValue"]:
			if iItem != -1 and lSquareSelection[1] != -1:
				iData2 = inputClass.getData2()
				tBL = (min(lSquareSelection[0][0], lSquareSelection[1][0]), min(lSquareSelection[0][1], lSquareSelection[1][1]))
				tTR = (max(lSquareSelection[0][0], lSquareSelection[1][0]), max(lSquareSelection[0][1], lSquareSelection[1][1]))
				lPlotList = utils.getPlotList(tBL, tTR)
				if iMode == 14:
					if iData2 == 0:
						for tPlot in lPlotList:
							md.changeCoreForce(iItem, tPlot, True)
					elif iData2 == 1:
						for tPlot in lPlotList:
							md.changeCoreForce(iItem, tPlot, False)
					elif iData2 == 2:
						for x in range(iWorldX):
							for y in range(iWorldY):
								md.changeCoreForce(iItem, (x, y), False)
						for tPlot in lPlotList:
							md.changeCoreForce(iItem, tPlot, True)
					elif iData2 == 3:
						for tPlot in lPlotList:
							x, y = tPlot
							if iChangeType == 0:
								iValue = md.getSettlerValue(iItem, (x, y)) - iChange
							elif iChangeType == 1:
								iValue = md.getSettlerValue(iItem, (x, y)) + iChange
							elif iChangeType == 2:
								iValue = iSetValue
							md.changeSettlerValue(iItem, tPlot, iValue)
				elif iMode == 15:
					if iData2 == 0:
						for tPlot in lPlotList:
							md.changeFlipForce(iItem, tPlot, True)
					elif iData2 == 1:
						for tPlot in lPlotList:
							md.changeFlipForce(iItem, tPlot, False)
					elif iData2 == 2:
						lOldFlip = Areas.getBirthArea(iItem)
						for tPlot in lOldFlip:
							md.changeFlipForce(iItem, tPlot, False)
						for tPlot in lPlotList:
							md.changeFlipForce(iItem, tPlot, True)
				lSquareSelection = [-1, -1, False]
				self.placeItemsStabMap()
				self.refreshMap()

		elif inputClass.getFunctionName() == "HideForbidden":
			bHideForbidden ^= True
			self.placeItemsStabMap()
			if iItem != -1:
				self.refreshMap()
		elif inputClass.getFunctionName() in ["ClearCore", "ClearFlip", "ClearSettler", "ClearCoreAll", "ClearFlipAll", "ClearSettlerAll"]:
			iData2 = inputClass.getData2()
			if iItem != -1 and (iData2 % 2) == 1:
				if iData2 == 1:
					md.resetCore(iItem)
				elif iData2 == 3:
					md.resetFlip(iItem)
				elif iData2 == 5:
					md.resetSettler(iItem)
				self.refreshMap()
			elif (iData2 % 2) == 0:
				for iPlayer in range(con.iNumPlayers):
					if iData2 == 2:
						md.resetCore(iPlayer)
					elif iData2 == 4:
						md.resetFlip(iPlayer)
					elif iData2 == 6:
						md.resetSettler(iPlayer)
				if iItem != -1:
					self.refreshMap()
			self.placeItemsStabMap()
		elif inputClass.getFunctionName() == "Export":
			md.export()

		elif inputClass.getFunctionName() == "Randomizer":
			if iItem != -1:
				# Find  a plot
				bGoodPlot = False
				while not bGoodPlot:
					iX = gc.getGame().getSorenRandNum(con.iWorldX, 'X coord')
					iY = gc.getGame().getSorenRandNum(con.iWorldY, 'Y coord')
					plot = gc.getMap().plot(iX, iY)
					if not plot.isWater() and not plot.isPeak():
						bGoodPlot = True
				# Reset old maps
				for x in range(con.iWorldX):
					for y in range(con.iWorldY):
						gc.getMap().plot(x, y).setCore(iItem, False)
				lOldFlip = Areas.getBirthArea(iItem)
				for tPlot in lOldFlip:
					md.changeFlipForce(iItem, tPlot, False)
				for x in range(con.iWorldX):
					for y in range(con.iWorldY):
						md.changeSettlerValue(iItem, (x, y), 20)
				# Create new maps
				for x in range(con.iWorldX):
					for y in range(con.iWorldY):
						plot = gc.getMap().plot(x, y)
						if plot.isWater() or plot.isPeak(): continue
						iRand = gc.getGame().getSorenRandNum(100, 'PlotValue')
						if iRand == 1 or iRand == 2:
							iGetValue = gc.getGame().getSorenRandNum(4, 'GetValue') + 2
							iValue = self.lPresetValues[iGetValue]
							for xx in range(-1, 2):
								for yy in range(-1, 2):
									plot = gc.getMap().plot(x + xx, y + yy)
									if not plot.isNone() and not plot.isWater() and not plot.isPeak():
										md.changeSettlerValue(iItem, (x + xx, y + yy), iValue)
						elif iRand == 3:
							for xx in range(-1, 2):
								for yy in range(-1, 2):
									plot = gc.getMap().plot(x + xx, y + yy)
									if not plot.isNone() and not plot.isWater() and not plot.isPeak():
										md.changeSettlerValue(iItem, (x + xx, y + yy), 3)
				for x in range(iX-3, iX + 3 + 1):
					for y in range(iY-3, iY + 3 + 1):
						md.changeCoreForce(iItem, (x, y), True)
						md.changeFlipForce(iItem, (x, y), True)
						md.changeSettlerValue(iItem, (x, y), 500)
				md.changeSettlerValue(iItem, (iX, iY), 700)
				self.placeItemsStabMap()
				self.refreshMap()

	def update(self, fDelta):
		return 1