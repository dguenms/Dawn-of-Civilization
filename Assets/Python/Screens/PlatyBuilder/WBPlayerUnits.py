from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import WBPlayerScreen
import WBTeamScreen
import WBProjectScreen
import WBTechScreen
import WBCityEditScreen
import WBUnitScreen
import WBInfoScreen
import WBCityDataScreen
import WBBuildingScreen
import WBPromotionScreen
import WBPlotScreen
import WBEventScreen
import CvPlatyBuilderScreen

gc = CyGlobalContext()
iCityID = -1
iCityOwner = -1
iUnitID = -1
iUnitOwner = -1
iCopyType = 0
iOwnerType = 1
iPlotType = 2
iActivityType = 0

class WBPlayerUnits:
	def __init__(self):
		self.iTable_Y = 110

	def interfaceScreen(self, iPlayerX):
		screen = CyGInterfaceScreen( "WBPlayerUnits", CvScreenEnums.WB_UNITLIST)
		global iPlayer
		global iMapWidth
		global iMapHeight
		iPlayer = iPlayerX
		iMapWidth = screen.getXResolution()/4
		iMapHeight = iMapWidth * 3/4

		screen.setRenderInterfaceOnly(True)
		screen.addPanel( "MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.setDimensions(0,0, screen.getXResolution(), screen.getYResolution())
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.setText("WBExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		iX = 20
		iY = 20
		iWidth = (screen.getXResolution() - 40)/5
		screen.addDropDownBoxGFC("CurrentPlayer", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i in xrange(gc.getMAX_PLAYERS()):
			pPlayerX = gc.getPlayer(i)
			if pPlayerX.isEverAlive():
				sText = pPlayerX.getName()
				if not pPlayerX.isAlive():
					sText = "*" + sText
				if pPlayerX.isTurnActive():
					sText = "[" + sText + "]"
				screen.addPullDownString("CurrentPlayer", sText, i, i, i == iPlayer)

		iX += iWidth
		screen.addDropDownBoxGFC("OwnerType", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("OwnerType", CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()), 0, 0, 0 == iOwnerType)
		screen.addPullDownString("OwnerType", CyTranslator().getText("TXT_KEY_PITBOSS_TEAM", ()), 2, 2, 2 == iOwnerType)
		screen.addPullDownString("OwnerType", CyTranslator().getText("TXT_KEY_MAIN_MENU_PLAYER", ()), 1, 1, 1 == iOwnerType)

		iX += iWidth
		screen.addDropDownBoxGFC("PlotType", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlotType", CyTranslator().getText("TXT_KEY_WB_SINGLE_PLOT", ()), 0, 0, iPlotType == 0)
		screen.addPullDownString("PlotType", CyTranslator().getText("TXT_KEY_WB_AREA_PLOTS", ()), 1, 1, iPlotType == 1)
		screen.addPullDownString("PlotType", CyTranslator().getText("TXT_KEY_WB_ALL_PLOTS", ()), 2, 2, iPlotType == 2)

		iX += iWidth
		screen.addDropDownBoxGFC("CopyType", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CopyType", CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()), 0, 0, 0 == iCopyType)
		screen.addPullDownString("CopyType", CyTranslator().getText("TXT_KEY_SPACE_SHIP_SCREEN_TYPE_BUTTON", ()), 1, 1, 1 == iCopyType)
		screen.addPullDownString("CopyType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT_COMBAT", ()), 2, 2, 2 == iCopyType)
		screen.addPullDownString("CopyType", CyTranslator().getText("TXT_KEY_PEDIA_DOMAIN", ()), 3, 3, 3 == iCopyType)
		screen.addPullDownString("CopyType", CyTranslator().getText("TXT_KEY_WB_GROUP", ()), 4, 4, 4 == iCopyType)
		screen.addPullDownString("CopyType", CyTranslator().getText("TXT_KEY_WB_ACTIVITY", ()), 5, 5, 5 == iCopyType)

		iX += iWidth
		screen.addDropDownBoxGFC("ActivityType", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i in xrange(len(CvPlatyBuilderScreen.Activities)):
			screen.addPullDownString("ActivityType", CvPlatyBuilderScreen.Activities[i], i, i, i == iActivityType)
		if iCopyType != 5:
			screen.hide("ActivityType")

		iY = self.iTable_Y - 30
		sKillButton = "Art/Interface/Buttons/Actions/Delete.dds"
		sSkipButton = gc.getMissionInfo(MissionTypes.MISSION_SKIP).getButton()

		screen.setImageButton("DeleteCurrentCity", sKillButton, 20, iY, 28, 28, WidgetTypes.WIDGET_PYTHON, 1041, -1)
		screen.setLabel("DeleteCitiesText", "Background", "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution()/2 - 35, iY, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setImageButton("DeleteAllCities", sKillButton, screen.getXResolution()/2 - 35, iY, 28, 28, WidgetTypes.WIDGET_PYTHON, 1041, -1)

		screen.setImageButton("DeleteCurrentUnit", sKillButton, 10 + screen.getXResolution()/2, iY, 28, 28, WidgetTypes.WIDGET_PYTHON, 1041, -1)
		screen.setImageButton("EndCurrentUnit", sSkipButton, 40 + screen.getXResolution()/2, iY, 28, 28, WidgetTypes.WIDGET_PYTHON, 1042, -1)
		screen.setLabel("DeleteUnitsText", "Background", "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 75, iY, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setImageButton("DeleteAllUnits", sKillButton, screen.getXResolution() - 75, iY, 28, 28, WidgetTypes.WIDGET_PYTHON, 1041, -1)
		screen.setImageButton("EndAllUnits", sSkipButton, screen.getXResolution() - 45, iY, 28, 28, WidgetTypes.WIDGET_PYTHON, 1042, -1)

		self.sortUnits()
		self.sortCities()
		self.addPageSwitch()

	def sortUnits(self):
		screen = CyGInterfaceScreen( "WBPlayerUnits", CvScreenEnums.WB_UNITLIST)
		global iUnitID
		global lUnits
		global iUnitOwner
		pPlayer = gc.getPlayer(iPlayer)
		pUnitOwner = gc.getPlayer(iUnitOwner)

		lUnits = []
		pUnit = pPlayer.getUnit(iUnitID)
		if pUnitOwner:
			pUnit = pUnitOwner.getUnit(iUnitID)
		if pUnit.isNone():
			(loopUnit, iter) = pPlayer.firstUnit(False)
			while(loopUnit):
				pUnit = loopUnit
				iUnitID = loopUnit.getID()
				iUnitOwner = loopUnit.getOwner()
				break
				(loopUnit, iter) = pPlayer.nextUnit(iter, False)

		for iPlayerX in xrange(gc.getMAX_PLAYERS()):
			pPlayerX = gc.getPlayer(iPlayerX)
			if iOwnerType == 1 and iPlayerX != iPlayer: continue
			if iOwnerType == 2 and pPlayerX.getTeam() != pPlayer.getTeam(): continue
			if pPlayerX.isAlive():
				(loopUnit, iter) = pPlayerX.firstUnit(False)
				while(loopUnit):
					if pUnit.isNone():
						pUnit = loopUnit
						iUnitID = loopUnit.getID()
						iUnitOwner = loopUnit.getOwner()
					bCopy = True
					if iPlotType == 0:
						if loopUnit.getX() != pUnit.getX() or loopUnit.getY() != pUnit.getY():
							bCopy = False
					elif iPlotType == 1:
						if loopUnit.plot().getArea() != pUnit.plot().getArea():
							bCopy = False
					if iCopyType == 1:
						if loopUnit.getUnitType() != pUnit.getUnitType():
							bCopy = False
					elif iCopyType == 2:
						if loopUnit.getUnitCombatType() != pUnit.getUnitCombatType():
							bCopy = False
					elif iCopyType == 3:
						if loopUnit.getDomainType() != pUnit.getDomainType():
							bCopy = False
					elif iCopyType == 4:
						if loopUnit.getGroupID() != pUnit.getGroupID() or loopUnit.getOwner() != pUnit.getOwner():
							bCopy = False
					elif iCopyType == 5:
						loopGroup = loopUnit.getGroup()
						if loopGroup.getActivityType() != iActivityType:
							bCopy = False
					if bCopy:
						lUnits.append([loopUnit.getOwner(), loopUnit.getID()])
					(loopUnit, iter) = pPlayerX.nextUnit(iter, False)
		lUnits.sort()
		self.placeCurrentUnit()
		
	def sortCities(self):
		screen = CyGInterfaceScreen( "WBPlayerUnits", CvScreenEnums.WB_UNITLIST)
		global iCityID
		global lCities
		global iCityOwner
		pPlayer = gc.getPlayer(iPlayer)
		pCityOwner = gc.getPlayer(iCityOwner)

		lCities = []
		pCity = pPlayer.getCity(iCityID)
		if pCityOwner:
			pCity = pCityOwner.getCity(iCityID)
		if pCity.isNone():
			(loopCity, iter) = pPlayer.firstCity(False)
			while(loopCity):
				pCity = loopCity
				iCityID = loopCity.getID()
				iCityOwner = loopCity.getOwner()
				break
				(loopCity, iter) = pPlayer.nextCity(iter, False)

		for iPlayerX in xrange(gc.getMAX_PLAYERS()):
			pPlayerX = gc.getPlayer(iPlayerX)
			if iOwnerType == 1 and iPlayerX != iPlayer: continue
			if iOwnerType == 2 and pPlayerX.getTeam() != pPlayer.getTeam(): continue
			if pPlayerX.isAlive():
				(loopCity, iter) = pPlayerX.firstCity(False)
				while(loopCity):
					if pCity.isNone():
						pCity = loopCity
						iCityID = loopCity.getID()
						iCityOwner = loopCity.getOwner()
					bCopy = True
					if iPlotType == 0:
						if loopCity.getX() != pCity.getX() or loopCity.getY() != pCity.getY():
							bCopy = False
					elif iPlotType == 1:
						if loopCity.plot().getArea() != pCity.plot().getArea():
							bCopy = False
					if bCopy:
						lCities.append([loopCity.getOwner(), loopCity.getID()])
					(loopCity, iter) = pPlayerX.nextCity(iter, False)
		lCities.sort()
		self.placeCurrentCity()

	def placeCurrentUnit(self):
		screen = CyGInterfaceScreen( "WBPlayerUnits", CvScreenEnums.WB_UNITLIST)
		iY = self.iTable_Y + iMapHeight
		iWidth = screen.getXResolution()/2 - 30
		iHeight = (screen.getYResolution() - iY - 42) / 24 * 24 + 2
		iColWidth = (iWidth - 24*2 - 10) /9

		lStatus = [CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), gc.getMissionInfo(MissionTypes.MISSION_FORTIFY).getButton(), gc.getMissionInfo(MissionTypes.MISSION_SKIP).getButton()]

		screen.addTableControlGFC( "WBUnitList", 8, 10 + screen.getXResolution()/2, iY, iWidth, iHeight, True, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader( "WBUnitList", 0, "", 24)
		screen.setTableColumnHeader( "WBUnitList", 1, "", 24)
		screen.setTableColumnHeader( "WBUnitList", 2, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()), iColWidth * 4)
		screen.setTableColumnHeader( "WBUnitList", 3, "ID", iColWidth * 2)
		screen.setTableColumnHeader( "WBUnitList", 4, CyTranslator().getText("TXT_KEY_WB_XLEVEL", ()), iColWidth * 1)
		screen.setTableColumnHeader( "WBUnitList", 5, CyTranslator().getText("[ICON_STRENGTH]", ()), iColWidth * 1)
		screen.setTableColumnHeader( "WBUnitList", 6, CyTranslator().getText("[ICON_MOVES]", ()), iColWidth * 1)
		screen.setTableColumnHeader( "WBUnitList", 7, "", 10)
		screen.enableSort("WBUnitList")

		for i in lUnits:
			pPlayerX = gc.getPlayer(i[0])
			loopUnit = pPlayerX.getUnit(i[1])
			if loopUnit.isNone(): continue
			iRow = screen.appendTableRow("WBUnitList")
			
			iStatus = 0
			if loopUnit.movesLeft() > 0:
				iStatus = 1
			if loopUnit.getGroup().readyToMove(False):
				iStatus = 2
			sColor = CyTranslator().getText("[COLOR_NEGATIVE_TEXT]", ())
			if iUnitID == loopUnit.getID() and iUnitOwner == loopUnit.getOwner():
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			iCivilization = loopUnit.getCivilizationType()
			screen.setTableText("WBUnitList", 0, iRow, "", gc.getCivilizationInfo(iCivilization).getButton(), WidgetTypes.WIDGET_PYTHON, 7872, i[0] * 10000 + iCivilization, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText("WBUnitList", 1, iRow, str(iStatus), lStatus[iStatus], WidgetTypes.WIDGET_PYTHON, 1043, iStatus, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("WBUnitList", 2, iRow, "<font=3>" + sColor + loopUnit.getName() + "</color></font>", loopUnit.getButton(), WidgetTypes.WIDGET_PYTHON, 8300 + i[0], i[1], CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableInt("WBUnitList", 3, iRow, "<font=3>" + str(loopUnit.getID()) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 8300 + i[0], i[1], CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("WBUnitList", 4, iRow, "<font=3>" + str(loopUnit.getLevel()) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 8300 + i[0], i[1], CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("WBUnitList", 5, iRow, "<font=3>" + str(loopUnit.baseCombatStr()) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 8300 + i[0], i[1], CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("WBUnitList", 6, iRow, "<font=3>" + str(loopUnit.baseMoves()) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 8300 + i[0], i[1], CvUtil.FONT_CENTER_JUSTIFY)
		self.placeUnitMap()

	def placeCurrentCity(self):
		screen = CyGInterfaceScreen( "WBPlayerUnits", CvScreenEnums.WB_UNITLIST)
		iY = self.iTable_Y + iMapHeight
		iWidth = screen.getXResolution()/2 - 30
		iHeight = (screen.getYResolution() - iY - 42) / 24 * 24 + 2
		iColWidth = (iWidth - 24) /10

		screen.addTableControlGFC( "WBCityList", 7, 20, iY, iWidth, iHeight, True, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader( "WBCityList", 0, "", 24)
		screen.setTableColumnHeader( "WBCityList", 1, CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()), iColWidth * 3)
		screen.setTableColumnHeader( "WBCityList", 2,"ID", iColWidth * 2)
		screen.setTableColumnHeader( "WBCityList", 3, CyTranslator().getText("[ICON_CULTURE]", ()), iColWidth * 2)
		screen.setTableColumnHeader( "WBCityList", 4, CyTranslator().getText("[ICON_ANGRYPOP]", ()), iColWidth * 1)
		screen.setTableColumnHeader( "WBCityList", 5, CyTranslator().getText("[ICON_HAPPY]", ()), iColWidth * 1)
		screen.setTableColumnHeader( "WBCityList", 6, CyTranslator().getText("[ICON_HEALTHY]", ()), iColWidth * 1)
		screen.enableSort("WBCityList")

		for i in lCities:
			pPlayerX = gc.getPlayer(i[0])
			loopCity = pPlayerX.getCity(i[1])
			if loopCity.isNone(): continue
			iRow = screen.appendTableRow("WBCityList")
			sColor = CyTranslator().getText("[COLOR_NEGATIVE_TEXT]", ())
			if iCityID == loopCity.getID() and iCityOwner == loopCity.getOwner():
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			iCivilization = loopCity.getCivilizationType()
			screen.setTableText("WBCityList", 0, iRow, "", gc.getCivilizationInfo(iCivilization).getButton(), WidgetTypes.WIDGET_PYTHON, 7872, i[0] * 10000 + iCivilization, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText("WBCityList", 1, iRow, "<font=3>" + sColor + loopCity.getName() + "</color></font>", "", WidgetTypes.WIDGET_PYTHON, 7200 + i[0], i[1], CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableInt("WBCityList", 2, iRow, "<font=3>" + str(loopCity.getID()) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 7200 + i[0], i[1], CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("WBCityList", 3, iRow, "<font=3>" + CvPlatyBuilderScreen.CvWorldBuilderScreen().addComma(loopCity.getCulture(i[0])) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 7200 + i[0], i[1], CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("WBCityList", 4, iRow, "<font=3>" + str(loopCity.getPopulation()) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 7200 + i[0], i[1], CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("WBCityList", 5, iRow, "<font=3>" + str(loopCity.happyLevel() - loopCity.unhappyLevel(0)) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 7200 + i[0], i[1], CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("WBCityList", 6, iRow, "<font=3>" + str(loopCity.goodHealth() - loopCity.badHealth(0)) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 7200 + i[0], i[1], CvUtil.FONT_CENTER_JUSTIFY)
		self.placeCityMap()

	def placeCityMap(self):
		screen = CyGInterfaceScreen("WBPlayerUnits", CvScreenEnums.WB_UNITLIST)
		screen.hide("GoToCity")
		screen.hide("CityView")
		screen.hide("CityDescription")
		pCityOwner = gc.getPlayer(iCityOwner)
		if not pCityOwner: return
		pCity = pCityOwner.getCity(iCityID)
		if pCity.isNone(): return
		sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=4b>" + pCity.getName() + "</color></font>"
		screen.setText("GoToCity", "Background", sText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/4, self.iTable_Y - 60, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iXMap = screen.getXResolution()/4 - 10
		screen.addPlotGraphicGFC("CityView", iXMap, self.iTable_Y, iMapWidth, iMapHeight, pCity.plot(), 350, False, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iX = 20
		screen.addPanel("CityPanel", "", "", False, False, iX, self.iTable_Y, iXMap - iX, iMapHeight, PanelStyles.PANEL_STYLE_IN)
		screen.addMultilineText("CityDescription", self.getCityData(pCity), iX, self.iTable_Y, iXMap - iX, iMapHeight, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeUnitMap(self):
		screen = CyGInterfaceScreen("WBPlayerUnits", CvScreenEnums.WB_UNITLIST)
		screen.hide("GoToUnit")
		screen.hide("UnitView")
		screen.hide("UnitDescription")
		pUnitOwner = gc.getPlayer(iUnitOwner)
		if not pUnitOwner: return
		pUnit = pUnitOwner.getUnit(iUnitID)
		if pUnit.isNone(): return
		sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=4b>" + pUnit.getName() + "</color></font>"
		screen.setText("GoToUnit", "Background", sText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()*3/4, self.iTable_Y - 60, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iXMap = screen.getXResolution() * 3/4 - 20
		screen.addPlotGraphicGFC("UnitView", iXMap, self.iTable_Y, iMapWidth, iMapHeight, pUnit.plot(), 350, True, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iX = screen.getXResolution()/2 + 10
		screen.addPanel("UnitPanel", "", "", False, False, iX, self.iTable_Y, iXMap - iX, iMapHeight, PanelStyles.PANEL_STYLE_IN)
		screen.addMultilineText("UnitDescription", self.getUnitData(pUnit), iX, self.iTable_Y, iXMap - iX, iMapHeight, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def getCityData(self, pCity):
		pPlayer = gc.getPlayer(iCityOwner)
		sText = "<font=3>"
		if pCity.isCapital():
			sText += CyTranslator().getText("[ICON_STAR]", ())
		elif pCity.isGovernmentCenter():
			sText += CyTranslator().getText("[ICON_SILVER_STAR]", ())
		sText += u"%s: %d<font=2>" %(pCity.getName(), pCity.getPopulation())
		sTemp = ""
		if pCity.isConnectedToCapital(iCityOwner):
			sTemp += CyTranslator().getText("[ICON_TRADE]", ())
		for i in xrange(gc.getNumReligionInfos()):
			if pCity.isHolyCityByType(i):
				sTemp += u"%c" %(gc.getReligionInfo(i).getHolyCityChar())
			elif pCity.isHasReligion(i):
				sTemp += u"%c" %(gc.getReligionInfo(i).getChar())

		for i in xrange(gc.getNumCorporationInfos()):
			if pCity.isHeadquartersByType(i):
				sTemp += u"%c" %(gc.getCorporationInfo(i).getHeadquarterChar())
			elif pCity.isHasCorporation(i):
				sTemp += u"%c" %(gc.getCorporationInfo(i).getChar())
		if len(sTemp) > 0:
			sText += "\n" + sTemp

		iMaxDefense = pCity.getTotalDefense(False)
		if iMaxDefense > 0:
			sText += u"\n%s: " %(CyTranslator().getText("[ICON_DEFENSE]", ()))
			iCurrent = pCity.getDefenseModifier(False)
			if iCurrent != iMaxDefense:
				sText += u"%d/" %(iCurrent)
			sText += u"%d%%" %(iMaxDefense)

		sText += u"\n%s: %d/%d" %(CyTranslator().getText("[ICON_FOOD]", ()), pCity.getFood(), pCity.growthThreshold())
		iFoodGrowth = pCity.foodDifference(True)
		if iFoodGrowth != 0:
			sText += u" %+d" %(iFoodGrowth)

		if pCity.isProduction():
			sText += u"\n%s:" %(CyTranslator().getText("[ICON_PRODUCTION]", ()))
			if not pCity.isProductionProcess():
				sText += u" %d/%d" %(pCity.getProduction(), pCity.getProductionNeeded())
				iProduction = pCity.getCurrentProductionDifference(False, True)
				if iProduction != 0:
					sText += u" %+d" %(iProduction)
			sText += u" (%s)" %(pCity.getProductionName())
					
		iGPRate = pCity.getGreatPeopleRate()
		iProgress = pCity.getGreatPeopleProgress()
		if iGPRate > 0 or iProgress > 0:
			sText += u"\n%s: %d/%d %+d" %(CyTranslator().getText("[ICON_GREATPEOPLE]", ()), iProgress, pPlayer.greatPeopleThreshold(False), iGPRate)

		sText += u"\n%s: %d/%d (%s)" %(CyTranslator().getText("[ICON_CULTURE]", ()), pCity.getCulture(iCityOwner), pCity.getCultureThreshold(), gc.getCultureLevelInfo(pCity.getCultureLevel()).getDescription())

		lTemp = []
		for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
			iAmount = pCity.getCommerceRateTimes100(i)
			if iAmount <= 0: continue
			sTemp = u"%d.%02d%c" %(pCity.getCommerceRate(i), pCity.getCommerceRateTimes100(i)%100, gc.getCommerceInfo(i).getChar())
			lTemp.append(sTemp)
		if len(lTemp) > 0:
			sText += "\n"
			for i in xrange(len(lTemp)):
				sText += lTemp[i]
				if i < len(lTemp) - 1:
					sText += ", "

		iMaintenance = pCity.getMaintenanceTimes100()
		if iMaintenance != 0:
			sText += "\n" + CyTranslator().getText("[COLOR_WARNING_TEXT]", ()) + CyTranslator().getText("INTERFACE_CITY_MAINTENANCE", ()) + " </color>"
			sText += u"-%d.%02d%c" %(iMaintenance/100, iMaintenance%100, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())

		sText += "\n" + CyTranslator().getText("TXT_KEY_WB_CITY", ()) + " ID: " + str(pCity.getID())
		sText += "\n" + "X: " + str(pCity.getX()) + ", Y: " + str(pCity.getY())
		sText += "\n" + CyTranslator().getText("TXT_KEY_WB_AREA_ID", ()) + ": "  + str(pCity.plot().getArea())

		sText += "</font>"
		return sText

	def getUnitData(self, pUnit):
		sText = CyGameTextMgr().getSpecificUnitHelp(pUnit, True, False)
		pGroup = pUnit.getGroup()
		iActivity = pGroup.getActivityType()
		if iActivity > -1 and iActivity < len(CvPlatyBuilderScreen.Activities):
			sText += "\n" + CvPlatyBuilderScreen.Activities[iActivity]
		sText += "\n" + CyTranslator().getText("TXT_KEY_WB_UNIT", ()) + " ID: " + str(pUnit.getID())
		sText += "\n" + CyTranslator().getText("TXT_KEY_WB_GROUP", ()) + " ID: " + str(pUnit.getGroupID())
		sText += "\n" + "X: " + str(pUnit.getX()) + ", Y: " + str(pUnit.getY())
		sText += "\n" + CyTranslator().getText("TXT_KEY_WB_AREA_ID", ()) + ": "  + str(pUnit.plot().getArea())
		return sText

	def addPageSwitch(self):
		screen = CyGInterfaceScreen( "WBPlayerUnits", CvScreenEnums.WB_UNITLIST)
		screen.addDropDownBoxGFC("CurrentPage", 20, screen.getYResolution() - 42, screen.getXResolution()/5, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA", ()), 0, 0, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_TEAM_DATA", ()), 1, 1, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()), 2, 2, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH", ()), 3, 3, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()) + " + " + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()), 4, 4, True)
		pCityOwner = gc.getPlayer(iCityOwner)
		if pCityOwner:
			pCity = pCityOwner.getCity(iCityID)
			if not pCity.isNone():
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_CITY_DATA", ()), 9, 9, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_CITY_DATA2", ()), 10, 10, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()), 14, 14, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_CITY", ()) + " " + CyTranslator().getText("TXT_KEY_WB_PLOT_DATA", ()), 12, 12, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_CITY", ()) + " " + CyTranslator().getText("TXT_KEY_CONCEPT_EVENTS", ()), 13, 13, False)
		pUnitOwner = gc.getPlayer(iUnitOwner)
		if pUnitOwner:
			pUnit = pUnitOwner.getUnit(iUnitID)
			if not pUnit.isNone():
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_UNIT_DATA", ()), 5, 5, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ()), 6, 6, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_UNIT", ()) + " " + CyTranslator().getText("TXT_KEY_WB_PLOT_DATA", ()), 7, 7, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_UNIT", ()) + " " + CyTranslator().getText("TXT_KEY_CONCEPT_EVENTS", ()), 8, 8, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_INFO_SCREEN", ()), 11, 11, False)

	def handleInput(self, inputClass):
		screen = CyGInterfaceScreen("WBPlayerUnits", CvScreenEnums.WB_UNITLIST)
		global iCityID
		global iUnitID
		global iCopyType
		global iOwnerType
		global iPlotType
		global iActivityType
		global iPlayer
		global iCityOwner
		global iUnitOwner
		pPlayer = gc.getPlayer(iPlayer)
		pUnitOwner = gc.getPlayer(iUnitOwner)
		pCityOwner = gc.getPlayer(iCityOwner)
		sName = inputClass.getFunctionName()

		if sName == "CurrentPage":
			iIndex = screen.getPullDownData("CurrentPage", screen.getSelectedPullDownID("CurrentPage"))
			if iIndex == 0:
				WBPlayerScreen.WBPlayerScreen().interfaceScreen(iPlayer)
			elif iIndex == 1:
				WBTeamScreen.WBTeamScreen().interfaceScreen(pPlayer.getTeam())
			elif iIndex == 2:
				WBProjectScreen.WBProjectScreen().interfaceScreen(pPlayer.getTeam())
			elif iIndex == 3:
				WBTechScreen.WBTechScreen().interfaceScreen(pPlayer.getTeam())
			elif iIndex == 11:
				WBInfoScreen.WBInfoScreen().interfaceScreen(iPlayer)
			elif iIndex == 5:
				WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).interfaceScreen(pUnitOwner.getUnit(iUnitID))
			elif iIndex == 6:
				WBPromotionScreen.WBPromotionScreen().interfaceScreen(pUnitOwner.getUnit(iUnitID))
			elif iIndex == 7:
				WBPlotScreen.WBPlotScreen().interfaceScreen(pUnitOwner.getUnit(iUnitID).plot())
			elif iIndex == 8:
				WBEventScreen.WBEventScreen().interfaceScreen(pUnitOwner.getUnit(iUnitID).plot())
			elif iIndex == 9:
				WBCityEditScreen.WBCityEditScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).interfaceScreen(pCityOwner.getCity(iCityID))
			elif iIndex == 10:
				WBCityDataScreen.WBCityDataScreen().interfaceScreen(pCityOwner.getCity(iCityID))
			elif iIndex == 14:
				WBBuildingScreen.WBBuildingScreen().interfaceScreen(pCityOwner.getCity(iCityID))
			elif iIndex == 12:
				WBPlotScreen.WBPlotScreen().interfaceScreen(pCityOwner.getCity(iCityID).plot())
			elif iIndex == 13:
				WBEventScreen.WBEventScreen().interfaceScreen(pCityOwner.getCity(iCityID).plot())

		elif sName == "CurrentPlayer":
			iIndex = screen.getPullDownData("CurrentPlayer", screen.getSelectedPullDownID("CurrentPlayer"))
			iCityID = -1
			iUnitID = -1
			self.interfaceScreen(iIndex)

		elif sName == "OwnerType":
			iOwnerType = screen.getPullDownData("OwnerType", screen.getSelectedPullDownID("OwnerType"))
			if iCityOwner != iPlayer:
				iCityID = -1
			if iUnitOwner != iPlayer:
				iUnitID = -1
			self.sortCities()
			self.sortUnits()

		elif sName == "PlotType":
			iPlotType = screen.getPullDownData("PlotType", screen.getSelectedPullDownID("PlotType"))
			if iCityOwner != iPlayer:
				iCityID = -1
			if iUnitOwner != iPlayer:
				iUnitID = -1
			self.sortCities()
			self.sortUnits()

		elif sName == "CopyType":
			iCopyType = screen.getPullDownData("CopyType", screen.getSelectedPullDownID("CopyType"))
			self.sortUnits()
			screen.hide("ActivityType")
			if iCopyType == 5:
				screen.show("ActivityType")

		elif sName == "ActivityType":
			iActivityType = screen.getPullDownData("ActivityType", screen.getSelectedPullDownID("ActivityType"))
			self.sortUnits()

		elif sName == "GoToCity":
			WBCityEditScreen.WBCityEditScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).interfaceScreen(pCityOwner.getCity(iCityID))

		elif sName == "GoToUnit":
			WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).interfaceScreen(pUnitOwner.getUnit(iUnitID))

		elif sName == "WBCityList":
			if inputClass.getData1() == 7872:
				iCityOwner = inputClass.getData2() /10000
				WBPlayerScreen.WBPlayerScreen().interfaceScreen(iCityOwner)
			else:
				iCityID = inputClass.getData2()
				iCityOwner = inputClass.getData1() - 7200
				self.placeCurrentCity()
				self.placeCityMap()

		elif sName == "DeleteCurrentCity":
			if pCityOwner:
				pCity = pCityOwner.getCity(iCityID)
				if not pCity:
					pCity.kill()
					iCityID = -1
					self.sortCities()
					self.addPageSwitch()

		elif sName == "DeleteAllCities":
			for item in lCities:
				pPlayerX = gc.getPlayer(item[0])
				pPlayerX.getCity(item[1]).kill()
			iCityID = -1
			self.sortCities()
			self.addPageSwitch()

		elif sName == "WBUnitList":
			if inputClass.getData1() == 1043: return
			elif inputClass.getData1() == 7872:
				iUnitOwner = inputClass.getData2() /10000
				WBPlayerScreen.WBPlayerScreen().interfaceScreen(iUnitOwner)
			else:
				iUnitID = inputClass.getData2()
				iUnitOwner = inputClass.getData1() - 8300
				self.placeCurrentUnit()
				self.placeUnitMap()

		elif sName == "DeleteCurrentUnit":
			if pUnitOwner:
				pUnit = pUnitOwner.getUnit(iUnitID)
				if not pUnit.isNone():
					pUnit.kill(False, PlayerTypes.NO_PLAYER)
					iUnitID = -1
					self.sortUnits()
					self.addPageSwitch()

		elif sName == "DeleteAllUnits":
			for item in lUnits:
				pPlayerX = gc.getPlayer(item[0])
				pPlayerX.getUnit(item[1]).kill(False, PlayerTypes.NO_PLAYER)
			iUnitID = -1
			self.sortUnits()
			self.addPageSwitch()

		elif sName == "EndCurrentUnit":
			if pUnitOwner:
				pUnit = pUnitOwner.getUnit(iUnitID)
				if not pUnit.isNone():
					pUnit.finishMoves()
					self.placeCurrentUnit()

		elif sName == "EndAllUnits":
			for item in lUnits:
				pPlayerX = gc.getPlayer(item[0])
				pPlayerX.getUnit(item[1]).finishMoves()
			self.placeCurrentUnit()

		return

	def update(self, fDelta):
		return 1