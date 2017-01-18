from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import WBBuildingScreen
import WBCityEditScreen
import WBPlayerScreen
import WBTeamScreen
import WBPlotScreen
import WBEventScreen
import WBPlayerUnits
import WBReligionScreen
import WBCorporationScreen
import WBInfoScreen
import CvPlatyBuilderScreen
gc = CyGlobalContext()

iChange = 1
iOwnerType = 0
iPlotType = 2
iSelectedClass = -1
bRemove = False
bWonder = False
iSelectedYield = 0

class WBCityDataScreen:
	def __init__(self):
		self.iTable_Y = 80
		self.lCities = []

	def interfaceScreen(self, pCityX):
		screen = CyGInterfaceScreen( "WBCityDataScreen", CvScreenEnums.WB_CITYDATA)
		global pCity
		global iWidth
		global iPlayer

		pCity = pCityX
		iPlayer = pCity.getOwner()
		iWidth = screen.getXResolution()/4 - 20

		screen.setRenderInterfaceOnly(True)
		screen.addPanel("MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.setText("CityDataExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		screen.addDropDownBoxGFC("CurrentPage", 20, screen.getYResolution() - 42, iWidth - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_CITY_DATA", ()), 0, 0, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_CITY_DATA2", ()), 1, 1, True)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()), 2, 2, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA", ()), 3, 3, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_TEAM_DATA", ()), 4, 4, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ()), 8, 8, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ()), 9, 9, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()) + " + " + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()), 5, 5, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLOT_DATA", ()), 6, 6, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_CONCEPT_EVENTS", ()), 7, 7, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_INFO_SCREEN", ()), 11, 11, False)

		screen.addDropDownBoxGFC("OwnerType", 20, self.iTable_Y - 60, iWidth - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("OwnerType", CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()), 0, 0, 0 == iOwnerType)
		screen.addPullDownString("OwnerType", CyTranslator().getText("TXT_KEY_PITBOSS_TEAM", ()), 2, 2, 2 == iOwnerType)
		screen.addPullDownString("OwnerType", CyTranslator().getText("TXT_KEY_MAIN_MENU_PLAYER", ()), 1, 1, 1 == iOwnerType)

		screen.addDropDownBoxGFC("PlotType", 20, self.iTable_Y - 30, iWidth - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlotType", CyTranslator().getText("TXT_KEY_WB_AREA_PLOTS", ()), 1, 1, iPlotType == 1)
		screen.addPullDownString("PlotType", CyTranslator().getText("TXT_KEY_WB_ALL_PLOTS", ()), 2, 2, iPlotType == 2)

		screen.addDropDownBoxGFC("ChangeType", screen.getXResolution()/4, self.iTable_Y - 60, 150, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_ADD", ()), 1, 1, not bRemove)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_REMOVE", ()), 0, 0, bRemove)

		screen.addDropDownBoxGFC("ChangeBy", screen.getXResolution()/4, self.iTable_Y - 30, 150, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		i = 1
		while i < 10001:
			screen.addPullDownString("ChangeBy", "(+/-) " + str(i), i, i, iChange == i)
			if str(i)[0] == "1":
				i *= 5
			else:
				i *= 2

		screen.addDropDownBoxGFC("BonusClass", screen.getXResolution() * 3/4, self.iTable_Y - 30, 120, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("BonusClass", CyTranslator().getText("TXT_KEY_WB_CITY_ALL",()), -1, -1, True)
		screen.addPullDownString("BonusClass", CyTranslator().getText("TXT_KEY_GLOBELAYER_RESOURCES_GENERAL",()), 0, 0, 0 == iSelectedClass)
		iBonusClass = 1
		while not gc.getBonusClassInfo(iBonusClass) is None:
			sText = gc.getBonusClassInfo(iBonusClass).getType()
			sText = sText[sText.find("_") +1:]
			sText = sText.lower()
			sText = sText.capitalize()
			screen.addPullDownString("BonusClass", sText, iBonusClass, iBonusClass, iBonusClass == iSelectedClass)
			iBonusClass += 1

		global lSpecialist
		global lGreatPeople

		lSpecialist = []
		lGreatPeople = []
		for i in xrange(gc.getNumSpecialistInfos()):
			ItemInfo = gc.getSpecialistInfo(i)
			lSpecialist.append((ItemInfo.getDescription(), i))
			iGPClass = ItemInfo.getGreatPeopleUnitClass()
			if iGPClass == -1: continue
			iGP = gc.getCivilizationInfo(pCity.getCivilizationType()).getCivilizationUnits(iGPClass)
			if iGP == -1: continue
			if not iGP in lGreatPeople:
				lGreatPeople.append(iGP)

		for i in xrange(gc.getNumBuildingInfos()):
			ItemInfo = gc.getBuildingInfo(i)
			iGPClass = ItemInfo.getGreatPeopleUnitClass()
			if iGPClass == -1: continue
			iGP = gc.getCivilizationInfo(pCity.getCivilizationType()).getCivilizationUnits(iGPClass)
			if iGP == -1: continue
			if not iGP in lGreatPeople:
				lGreatPeople.append(iGP)

		for i in xrange(len(lGreatPeople)):
			GPInfo = gc.getUnitInfo(lGreatPeople[i])
			lGreatPeople[i] = [GPInfo.getDescription(), lGreatPeople[i]]
		lSpecialist.sort()
		lGreatPeople.sort()

		self.sortCities()
		self.createBonusList()
		self.placeGreatPeople()
		self.placeBonus()
		self.placeSpecialist()
		self.sortBuildings()

	def sortCities(self):
		self.lCities = []
		for iPlayerX in xrange(gc.getMAX_PLAYERS()):
			pPlayerX = gc.getPlayer(iPlayerX)
			if iOwnerType == 1 and iPlayerX != iPlayer: continue
			if iOwnerType == 2 and pPlayerX.getTeam() != pCity.getTeam(): continue
			(loopCity, iter) = pPlayerX.firstCity(False)
			while(loopCity):
				if iPlotType == 2 or (iPlotType == 1 and loopCity.plot().getArea() == pCity.plot().getArea()):
					sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
					if loopCity.getID() == pCity.getID() and iPlayerX == iPlayer:
						sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
					self.lCities.append([loopCity, iPlayerX, sColor])
				(loopCity, iter) = pPlayerX.nextCity(iter, False)
		self.placeCityTable()

	def placeCityTable(self):
		screen = CyGInterfaceScreen( "WBCityDataScreen", CvScreenEnums.WB_CITYDATA)
		iWidth = screen.getXResolution()/4 - 40
		iHeight = (screen.getYResolution() - 40 - self.iTable_Y) / 24 * 24 + 2
		screen.addTableControlGFC( "CurrentCity", 3, 20, self.iTable_Y, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader("CurrentCity", 0, "", 24)
		screen.setTableColumnHeader("CurrentCity", 1, "", 24)
		screen.setTableColumnHeader("CurrentCity", 2, "", iWidth - 48)

		for (loopCity, iPlayerX, sColor) in self.lCities:
			iRow = screen.appendTableRow("CurrentCity")
			iCiv = loopCity.getCivilizationType()
			screen.setTableText("CurrentCity", 0, iRow, "", gc.getCivilizationInfo(iCiv).getButton(), WidgetTypes.WIDGET_PYTHON, 7872, iCiv, CvUtil.FONT_LEFT_JUSTIFY)
			iLeader = gc.getPlayer(iPlayerX).getLeaderType()
			screen.setTableText("CurrentCity", 1, iRow, "", gc.getLeaderHeadInfo(iLeader).getButton(), WidgetTypes.WIDGET_PYTHON, 7876, iLeader, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("CurrentCity", 2, iRow, "<font=3>" + sColor + loopCity.getName() + "</font></color>", '', WidgetTypes.WIDGET_PYTHON, 7200 + iPlayerX, loopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)

	def sortBuildings(self):
		global lBuilding
		lBuilding = []
		for i in xrange(gc.getNumBuildingClassInfos()):
			if gc.getBuildingClassInfo(i).isGraphicalOnly(): continue
			if bWonder and not isLimitedWonderClass(i): continue
			if not bWonder and isLimitedWonderClass(i): continue
			iBuilding = gc.getCivilizationInfo(pCity.getCivilizationType()).getCivilizationBuildings(i)
			if iBuilding < 0:
				iBuilding = gc.getBuildingClassInfo(i).getDefaultBuildingIndex()
			if iBuilding < 0: continue
			lBuilding.append([gc.getBuildingInfo(iBuilding).getDescription(), iBuilding])
		lBuilding.sort()
		self.placeModify()

	def placeModify(self):
		screen = CyGInterfaceScreen( "WBCityDataScreen", CvScreenEnums.WB_CITYDATA)
		iTableWidth = screen.getXResolution()/2 - 20
		iX = screen.getXResolution()/4
		iY = self.iTable_Y - 30

		sText = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING",())
		screen.setLabel("ModifyHeader", "Background", "<font=3b>" + CyTranslator().getText("TXT_KEY_WB_MODIFY", (sText,)) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, iX + iTableWidth/2, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		screen.addDropDownBoxGFC("BuildingType", iX, iY, 150, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("BuildingType", CyTranslator().getText("TXT_KEY_CONCEPT_BUILDINGS", ()), 0, 0, not bWonder)
		screen.addPullDownString("BuildingType", CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS", ()), 1, 1, bWonder)

		screen.addDropDownBoxGFC("YieldType", iX + iTableWidth - 150, iY, 150, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i in xrange(YieldTypes.NUM_YIELD_TYPES):
			screen.addPullDownString("YieldType", gc.getYieldInfo(i).getDescription(), i, i, iSelectedYield == i)
		for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
			screen.addPullDownString("YieldType", gc.getCommerceInfo(i).getDescription(), i + YieldTypes.NUM_YIELD_TYPES, i + YieldTypes.NUM_YIELD_TYPES, iSelectedYield == i + YieldTypes.NUM_YIELD_TYPES)

	## Disabled because neither is working correctly with BTS dll ##
	#	iTotal = YieldTypes.NUM_YIELD_TYPES + CommerceTypes.NUM_COMMERCE_TYPES
	#	screen.addPullDownString("YieldType", CyTranslator().getText("TXT_KEY_CONCEPT_HAPPINESS", ()), iTotal, iTotal, iSelectedYield == iTotal)
	#	screen.addPullDownString("YieldType", CyTranslator().getText("TXT_KEY_CONCEPT_HEALTH", ()), iTotal + 1, iTotal + 1, iSelectedYield == iTotal + 1)
	## Disabled because neither is working correctly with BTS dll ##

		iY += 30
		iHeight = (screen.getYResolution()/2 - iY) / 24 * 24 + 2
		screen.addTableControlGFC("WBModifyBuilding", 2, iX, iY, iTableWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		for i in xrange(2):
			screen.setTableColumnHeader("WBModifyBuilding", i, "", iTableWidth/2)
		for item in lBuilding:
			ItemInfo = gc.getBuildingInfo(item[1])
			iBuildingClass = ItemInfo.getBuildingClassType()
			iRow = screen.appendTableRow("WBModifyBuilding")
			screen.setTableText("WBModifyBuilding", 0, iRow, "<font=3>" + item[0] + "</font>", ItemInfo.getButton(), WidgetTypes.WIDGET_HELP_BUILDING, item[1], -1, CvUtil.FONT_LEFT_JUSTIFY)
			sText = ""
			iChange = pCity.getBuildingHappyChange(iBuildingClass)
			if iChange > 0:
				sText += u"%d%s" %(iChange, CyTranslator().getText("[ICON_HAPPY]", ()))
			elif iChange < 0:
				sText += u"%d%s" %(-iChange, CyTranslator().getText("[ICON_UNHAPPY]", ()))
			iChange = pCity.getBuildingHealthChange(iBuildingClass)
			if iChange > 0:
				sText += u"%d%s" %(iChange, CyTranslator().getText("[ICON_HEALTHY]", ()))
			elif iChange < 0:
				sText += u"%d%s" %(-iChange, CyTranslator().getText("[ICON_UNHEALTHY]", ()))
			for j in xrange(YieldTypes.NUM_YIELD_TYPES):
				iChange = pCity.getBuildingYieldChange(iBuildingClass, j)
				if iChange != 0:
					sText += u"%d%c" %(iChange, gc.getYieldInfo(j).getChar())
			for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
				iChange = pCity.getBuildingCommerceChange(iBuildingClass, j)
				if iChange != 0:
					sText += u"%d%c" %(iChange, gc.getCommerceInfo(j).getChar())
			screen.setTableInt("WBModifyBuilding", 1, iRow, "<font=3>" + sText + "</font>", "", WidgetTypes.WIDGET_HELP_BUILDING, item[1], -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeSpecialist(self):
		screen = CyGInterfaceScreen( "WBCityDataScreen", CvScreenEnums.WB_CITYDATA)
		iX = screen.getXResolution()/4
		iY = screen.getYResolution()/2

		sText = "<font=3b>" + CyTranslator().getText("TXT_KEY_WB_BASE_RATE", (pCity.getBaseGreatPeopleRate(),)) + "</font>"
		screen.setButtonGFC("GreatPeopleRatePlus", "", "", iX, screen.getYResolution() - 42, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("GreatPeopleRateMinus", "", "", iX + 25, screen.getYResolution() - 42, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		screen.setLabel("GreatPeopleRateText", "Background", sText, CvUtil.FONT_LEFT_JUSTIFY, iX + 50, screen.getYResolution() - 41, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setLabel("SpecialistHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_WB_FREE_SPECIALISTS", ()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, iX + iWidth/2, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iY += 30
		sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + " (+/-)</font></color>"
		screen.setText("SpecialistAll", "Background",  sText, CvUtil.FONT_RIGHT_JUSTIFY, iX + iWidth - 20, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iY += 30
		iHeight = (screen.getYResolution() - iY - 40) /24 * 24 + 2
		screen.addTableControlGFC( "WBSpecialist", 1, screen.getXResolution()/4, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader("WBSpecialist", 0, "", iWidth)

		for item in lSpecialist:
			iRow = screen.appendTableRow("WBSpecialist")
			sItem = item[0]
			ItemInfo = gc.getSpecialistInfo(item[1])
			iNum = pCity.getFreeSpecialistCount(item[1])
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if iNum > 0:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				sItem += " (" + str(iNum) + ")"
			screen.setTableText("WBSpecialist", 0, iRow, "<font=3>" + sColor + sItem + "</font></color>", ItemInfo.getButton(), WidgetTypes.WIDGET_PYTHON, 7879, item[1], CvUtil.FONT_LEFT_JUSTIFY )

	def placeGreatPeople(self):
		screen = CyGInterfaceScreen( "WBCityDataScreen", CvScreenEnums.WB_CITYDATA)
		iX = screen.getXResolution()/2
		iY = screen.getYResolution()/2

		sText = "<font=3b>" + CyTranslator().getText("TXT_KEY_WB_PROGRESS", (pCity.getGreatPeopleProgress(),)) + "/" + str(gc.getPlayer(iPlayer).greatPeopleThreshold(False)) + "</font>"
		screen.setButtonGFC("GreatPeopleFlatPlus", "", "", iX, screen.getYResolution() - 42, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("GreatPeopleFlatMinus", "", "", iX + 25, screen.getYResolution() - 42, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		screen.setLabel("GreatPeopleFlat", "Background", sText, CvUtil.FONT_LEFT_JUSTIFY, iX + 50, screen.getYResolution() - 41, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setLabel("GreatPeopleHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_CONCEPT_GREAT_PEOPLE", ()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, iX + iWidth/2, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iY += 30
		sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + " (+/-)</font></color>"
		screen.setText("GreatPeopleProgressAll", "Background", sText, CvUtil.FONT_RIGHT_JUSTIFY, iX + iWidth - 20, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iY += 30
		iHeight = (screen.getYResolution() - iY - 40) /24 * 24 + 2
		screen.addTableControlGFC("WBGreatPeople", 1, iX, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader("WBGreatPeople", 0, "", iWidth)

		for item in lGreatPeople:
			iRow = screen.appendTableRow("WBGreatPeople")
			sItem = item[0]
			ItemInfo = gc.getUnitInfo(item[1])
			iNum = pCity.getGreatPeopleUnitProgress(item[1])
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if iNum > 0:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				sItem += " (" + str(iNum) + ")"
			screen.setTableText("WBGreatPeople", 0, iRow, "<font=3>" + sColor + sItem + "</font></color>", ItemInfo.getButton(), WidgetTypes.WIDGET_PYTHON, 8202, item[1], CvUtil.FONT_LEFT_JUSTIFY)

	def createBonusList(self):
		global lBonus
		lBonus = []
		for i in xrange(gc.getNumBonusInfos()):
			ItemInfo = gc.getBonusInfo(i)
			if iSelectedClass != ItemInfo.getBonusClassType() and iSelectedClass > -1: continue
			lBonus.append([ItemInfo.getDescription(), i])
		lBonus.sort()

	def placeBonus(self):
		screen = CyGInterfaceScreen( "WBCityDataScreen", CvScreenEnums.WB_CITYDATA)
		iX = screen.getXResolution() * 3/4
		iY = self.iTable_Y
		iHeight = (screen.getYResolution() - 40 - self.iTable_Y) / 24 * 24 + 2

		screen.setLabel("BonusHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, iX + iWidth/2, iY - 60, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + " (+/-)</font></color>"
		screen.setText("BonusAll", "Background", sText, CvUtil.FONT_RIGHT_JUSTIFY, iX + iWidth - 20, iY - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addTableControlGFC( "WBBonus", 2, iX, self.iTable_Y, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader( "WBBonus", 0, "", 24)
		screen.setTableColumnHeader( "WBBonus", 1, "", iWidth - 24)

		for item in lBonus:
			iRow = screen.appendTableRow("WBBonus")
			sItem = item[0]
			iNum = pCity.getFreeBonus(item[1])
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if iNum > 0:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				sItem += " (" + str(iNum) + ")"
			if pCity.isNoBonus(item[1]):
				screen.setTableText("WBBonus", 0, iRow, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), WidgetTypes.WIDGET_PYTHON, 1030, item[1], CvUtil.FONT_LEFT_JUSTIFY)
			else:
				sText = "<font=4>" + CyTranslator().getText("[ICON_TRADE]", ()) + "</font>"
				screen.setTableText("WBBonus", 0, iRow, sText, "", WidgetTypes.WIDGET_PYTHON, 1031, item[1], CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("WBBonus", 1, iRow, "<font=3>" + sColor + sItem + "</font></color>", gc.getBonusInfo(item[1]).getButton(), WidgetTypes.WIDGET_PYTHON, 7878, item[1], CvUtil.FONT_LEFT_JUSTIFY )

	def handleInput(self, inputClass):
		screen = CyGInterfaceScreen( "WBCityDataScreen", CvScreenEnums.WB_CITYDATA)
		global iChange
		global iOwnerType
		global iPlotType
		global bRemove
		global iSelectedClass
		global bWonder
		global iModifyBuilding
		global iSelectedYield

		if inputClass.getFunctionName() == "ChangeBy":
			if bRemove:
				iChange = -screen.getPullDownData("ChangeBy", screen.getSelectedPullDownID("ChangeBy"))
			else:
				iChange = screen.getPullDownData("ChangeBy", screen.getSelectedPullDownID("ChangeBy"))

		elif inputClass.getFunctionName() == "ChangeType":
			bRemove = not bRemove
			iChange = -iChange

		elif inputClass.getFunctionName() == "CurrentCity":
			iPlayerX = inputClass.getData1() - 7200
			pPlayerX = gc.getPlayer(iPlayerX)
			if pPlayerX:
				self.interfaceScreen(pPlayerX.getCity(inputClass.getData2()))

		elif inputClass.getFunctionName() == "CurrentPage":
			iIndex = screen.getPullDownData("CurrentPage", screen.getSelectedPullDownID("CurrentPage"))
			if iIndex == 0:
				WBCityEditScreen.WBCityEditScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).interfaceScreen(pCity)
			elif iIndex == 2:
				WBBuildingScreen.WBBuildingScreen().interfaceScreen(pCity)
			elif iIndex == 3:
				WBPlayerScreen.WBPlayerScreen().interfaceScreen(iPlayer)
			elif iIndex == 4:
				WBTeamScreen.WBTeamScreen().interfaceScreen(pCity.getTeam())
			elif iIndex == 5:
				WBPlayerUnits.WBPlayerUnits().interfaceScreen(iPlayer)
			elif iIndex == 6:
				WBPlotScreen.WBPlotScreen().interfaceScreen(pCity.plot())
			elif iIndex == 7:
				WBEventScreen.WBEventScreen().interfaceScreen(pCity.plot())
			elif iIndex == 8:
				WBReligionScreen.WBReligionScreen().interfaceScreen(iPlayer)
			elif iIndex == 9:
				WBCorporationScreen.WBCorporationScreen().interfaceScreen(iPlayer)
			elif iIndex == 11:
				WBInfoScreen.WBInfoScreen().interfaceScreen(iPlayer)

		elif inputClass.getFunctionName() == "OwnerType":
			iOwnerType = screen.getPullDownData("OwnerType", screen.getSelectedPullDownID("OwnerType"))
			self.sortCities()

		elif inputClass.getFunctionName() == "PlotType":
			iPlotType = screen.getPullDownData("PlotType", screen.getSelectedPullDownID("PlotType"))
			self.sortCities()

		elif inputClass.getFunctionName() == "SpecialistAll":
			for item in xrange(gc.getNumSpecialistInfos()):
				self.editFreeSpecialist(item)
			self.placeSpecialist()

		elif inputClass.getFunctionName() == "WBSpecialist":
			self.editFreeSpecialist(inputClass.getData2())
			self.placeSpecialist()

		elif inputClass.getFunctionName() == "GreatPeopleProgressAll":
			for item in lGreatPeople:
				self.editGreatPeopleProgress(item[1])
			self.placeGreatPeople()

		elif inputClass.getFunctionName().find("GreatPeopleFlat") > -1:
			if inputClass.getData1() == 1030:
				self.editGreatPeopleFlat(abs(iChange))
			elif inputClass.getData1() == 1031:
				self.editGreatPeopleFlat(-abs(iChange))
			self.placeGreatPeople()

		elif inputClass.getFunctionName().find("GreatPeopleRate") > -1:
			if inputClass.getData1() == 1030:
				self.editGreatPeopleRate(abs(iChange))
			elif inputClass.getData1() == 1031:
				self.editGreatPeopleRate(-abs(iChange))
			self.placeSpecialist()

		elif inputClass.getFunctionName() == "WBGreatPeople":
			self.editGreatPeopleProgress(inputClass.getData2())
			self.placeGreatPeople()

		elif inputClass.getFunctionName() == "BonusClass":
			iSelectedClass = inputClass.getData() - 1
			self.createBonusList()
			self.placeBonus()

		elif inputClass.getFunctionName() == "BonusAll":
			for item in lBonus:
				self.editFreeBonus(item[1])
			self.placeBonus()

		elif inputClass.getFunctionName() == "WBBonus":
			if inputClass.getData1() == 7878:
				self.editFreeBonus(inputClass.getData2())
			else:
				self.setNoBonusCB(inputClass.getData2())
			self.placeBonus()

		elif inputClass.getFunctionName() == "BuildingType":
			bWonder = not bWonder
			self.sortBuildings()

		elif inputClass.getFunctionName() == "YieldType":
			iSelectedYield = screen.getPullDownData("YieldType", screen.getSelectedPullDownID("YieldType"))

		elif inputClass.getFunctionName() == "WBModifyBuilding":
			self.modifyBuilding(inputClass.getData1())
			self.placeModify()
		return 1

	def modifyBuilding(self, iBuilding):
		iType  = iSelectedYield
		iCount = iChange
		iClass = gc.getBuildingInfo(iBuilding).getBuildingClassType()
		if iType < YieldTypes.NUM_YIELD_TYPES:
			pCity.setBuildingYieldChange(iClass, iType, pCity.getBuildingYieldChange(iClass, iType) + iCount)
		else:
			iType -= YieldTypes.NUM_YIELD_TYPES
			if iType < CommerceTypes.NUM_COMMERCE_TYPES:
				pCity.setBuildingCommerceChange(iClass, iType, pCity.getBuildingCommerceChange(iClass, iType) + iCount)
			else:
				iType -= CommerceTypes.NUM_COMMERCE_TYPES
				if iType == 0:
					pCity. setBuildingHappyChange(iClass, pCity.getBuildingHappyChange(iClass) + iCount)
				else:
					pCity. setBuildingHealthChange(iClass, pCity.getBuildingHealthChange(iClass) + iCount)


	def editFreeBonus(self, item):
		iCount = max(iChange, - pCity.getFreeBonus(item))
		pCity.changeFreeBonus(item, iCount)

	def setNoBonusCB(self, item):
		if pCity.isNoBonus(item):
			pCity.changeNoBonusCount(item, -1)
		else:
			pCity.changeNoBonusCount(item, 1)

	def editGreatPeopleFlat(self, iCount):
		if iCount < 0:
			iCount = max(iCount, - pCity.getGreatPeopleProgress())
		iCount = min(iCount, gc.getPlayer(iPlayer).greatPeopleThreshold(False) - pCity.getGreatPeopleProgress())
		pCity.changeGreatPeopleProgress(iCount)

	def editGreatPeopleRate(self, iCount):
		if iCount < 0:
			iCount = max(iCount, - pCity.getBaseGreatPeopleRate())
		pCity.changeBaseGreatPeopleRate(iCount)

	def editGreatPeopleProgress(self, item) :
		iCount = max(iChange, - pCity.getGreatPeopleUnitProgress(item))
		pCity.changeGreatPeopleUnitProgress(item, min(iCount, gc.getPlayer(iPlayer).greatPeopleThreshold(False) - pCity.getGreatPeopleUnitProgress(item)))
		self.editGreatPeopleFlat(iCount)

	def editFreeSpecialist(self, item):
		iCount = max(iChange, - pCity.getFreeSpecialistCount(item))
		pCity.changeFreeSpecialistCount(item, iCount)

	def update(self, fDelta):
		return 1