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
gc = CyGlobalContext()

iMode = 0
iSelectedPlayer = -1
iItem = -1
lItems = []
lSelectedItem = [-1, -1]

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

	def interfaceScreen(self, iPlayerX):
		screen = CyGInterfaceScreen("WBInfoScreen", CvScreenEnums.WB_INFO)
		global iSelectedPlayer

		iSelectedPlayer = iPlayerX

		screen.setRenderInterfaceOnly(True)
		screen.addPanel("MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
	
		screen.setText("WBInfoExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		sText = u"<font=3b>" + CyTranslator().getText("TXT_KEY_PEDIA_HIDE_INACTIVE", ()) + "</font>"
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if CvPlatyBuilderScreen.bHideInactive:
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setText("HideInactive", "Background", sColor + sText + "</color>", CvUtil.FONT_LEFT_JUSTIFY, screen.getXResolution()/3 + 20, self.iTable_Y - 22, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

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
		
		screen.addDropDownBoxGFC("CurrentPlayer", iX + iWidth/2, iY, iWidth/2, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i in xrange(gc.getMAX_PLAYERS()):
			pPlayerX = gc.getPlayer(i)
			if pPlayerX.isAlive():
				sText = pPlayerX.getName()
				screen.addPullDownString("CurrentPlayer", sText, i, i, i == iSelectedPlayer)

		self.placeMap()
		self.placeItems()
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
		else:
			iTeam = lSelectedItem[0]
			pTeam = gc.getTeam(iTeam)
			sText += pTeam.getName()
			
		sText += "</color></font>"
		screen.setText("PlotData", "Background", sText, CvUtil.FONT_CENTER_JUSTIFY, iX, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

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
		screen.minimapClearAllFlashingTiles()
		sHeader = ""
		if iItem == -1:
			screen.hide("InfoHeader")
			return

		iColorA = gc.getInfoTypeForString(self.iColorA)
		iColorB = gc.getInfoTypeForString(self.iColorB)
		iX = screen.getXResolution()/3 + 20
		iY = screen.getYResolution() *2/3 + 30
		iWidth = screen.getXResolution() * 2/3 - 40
		iHeight = (screen.getYResolution() - iY - 40) / 24 * 24 + 2

		nColumns = iWidth / self.iMinColWidth
		screen.addTableControlGFC("PlotTable", nColumns, iX, iY, iWidth, iHeight, False, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		for i in xrange(nColumns):
			screen.setTableColumnHeader("PlotTable", i, "", iWidth/nColumns)

		iCount = 0
		iMaxRows = -1
		lTemp = lItems[iItem][5]
		if not lSelectedItem in lTemp:
			if len(lTemp) > 0:
				lSelectedItem = lTemp[0]
			else:
				lSelectedItem = [-1, -1]
		sHeader = self.Mode[iMode](iItem).getDescription()
		screen.setLabel("InfoHeader", "Background", "<font=4b>" + sHeader + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 20, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.bringMinimapToFront()

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
		else:
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
			
	def handleInput(self, inputClass):
		screen = CyGInterfaceScreen("WBInfoScreen", CvScreenEnums.WB_INFO)
		global iSelectedPlayer
		global iItem
		global iMode
		global lSelectedItem

		if inputClass.getFunctionName() == "PlotData":
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

		elif inputClass.getFunctionName() == "ItemType":
			iMode = screen.getPullDownData("ItemType", screen.getSelectedPullDownID("ItemType"))
			iItem = -1
			self.interfaceScreen(iSelectedPlayer)

		elif inputClass.getFunctionName() == "CurrentPlayer":
			iSelectedPlayer = screen.getPullDownData("CurrentPlayer", screen.getSelectedPullDownID("CurrentPlayer"))
			self.interfaceScreen(iSelectedPlayer)

		elif inputClass.getFunctionName() == "InfoTable":
			iItem = inputClass.getData2()
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

		elif inputClass.getFunctionName() == "HideInactive":
			CvPlatyBuilderScreen.bHideInactive = not CvPlatyBuilderScreen.bHideInactive
			CvPlatyBuilderScreen.CvWorldBuilderScreen().refreshSideMenu()
			sText = u"<font=3b>" + CyTranslator().getText("TXT_KEY_PEDIA_HIDE_INACTIVE", ()) + "</font>"
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if CvPlatyBuilderScreen.bHideInactive:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			screen.setText("HideInactive", "Background", sColor + sText + "</color>", CvUtil.FONT_LEFT_JUSTIFY, screen.getXResolution()/3 + 20, self.iTable_Y - 22, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			self.placeItems()

	def update(self, fDelta):
		return 1