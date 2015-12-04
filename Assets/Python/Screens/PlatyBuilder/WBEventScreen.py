from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import WBPlotScreen
import WBCityEditScreen
import WBUnitScreen
import WBPlayerScreen
import WBTeamScreen
import WBInfoScreen
import CvPlatyBuilderScreen
gc = CyGlobalContext()

iSelectedEvent = -1
iEventPlayer = -1
iOtherPlayer = -1
iOtherCity = -1
iSelectedReligion = -1
iSelectedCorporation = -1
iSelectedUnit = -1
iSelectedBuilding = -1

class WBEventScreen:

	def __init__(self):
		self.iTable_Y = 80

	def interfaceScreen(self, pPlotX):
		screen = CyGInterfaceScreen( "WBEventScreen", CvScreenEnums.WB_EVENT)
		
		global pPlot
		global iWidth

		pPlot = pPlotX
		iWidth = screen.getXResolution()/5 - 20
		
		screen.setRenderInterfaceOnly(True)
		screen.addPanel( "MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.setText("PlotExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		screen.addDropDownBoxGFC("CurrentPage", 10, screen.getYResolution() - 42, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLOT_DATA", ()), 0, 0, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_CONCEPT_EVENTS", ()), 1, 1, True)
		if pPlot.isOwned():
			screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA", ()), 2, 2, False)
			screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_TEAM_DATA", ()), 3, 3, False)
			if pPlot.isCity():
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_CITY_DATA", ()), 4, 4, False)
		if pPlot.getNumUnits() > 0:
			screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_UNIT_DATA", ()), 5, 5, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_INFO_SCREEN", ()), 11, 11, False)

		global lEvents
		global lReligions
		global lCorporations
		global lBuildings

		lCorporations = []
		for i in xrange(gc.getNumCorporationInfos()):
			ItemInfo = gc.getCorporationInfo(i)
			lCorporations.append([ItemInfo.getDescription(), i])
		lCorporations.sort()

		lBuildings = []
		for i in xrange(gc.getNumBuildingInfos()):
			ItemInfo = gc.getBuildingInfo(i)
			lBuildings.append([ItemInfo.getDescription(), i])
		lBuildings.sort()

		lEvents = []
		for i in xrange(gc.getNumEventTriggerInfos()):
			sEvent = gc.getEventTriggerInfo(i).getType()[13:]
			sEvent = sEvent.lower()
			sEvent = sEvent.replace("_", " ")
			sEvent = sEvent.capitalize()
			lEvents.append([sEvent, i])
		lEvents.sort()

		lReligions = []
		for i in xrange(gc.getNumReligionInfos()):
			ItemInfo = gc.getReligionInfo(i)
			lReligions.append([ItemInfo.getDescription(), i])
		lReligions.sort()

		self.placeEventPlayers()
		self.placeEvents()
		self.placeOtherPlayers()
		self.placeOtherCities()
		self.placeBuildings()
		self.placeReligions()
		self.placeCorporations()
		self.placeUnits()

	def placeEventPlayers(self):
		screen = CyGInterfaceScreen("WBEventScreen", CvScreenEnums.WB_EVENT)
		global iEventPlayer
		iHeight = (screen.getYResolution()/2 - self.iTable_Y - 2) / 24 * 24 + 2

		sHeader = ""
		screen.addTableControlGFC("WBEventPlayer", 2, screen.getXResolution()/5 + 10, self.iTable_Y, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("WBEventPlayer", 0, "", 24)
		screen.setTableColumnHeader("WBEventPlayer", 1, "", iWidth - 24)

		for iPlayerX in xrange(gc.getMAX_CIV_PLAYERS()):
			pPlayerX = gc.getPlayer(iPlayerX)
			if pPlayerX.isAlive():
				if iEventPlayer == -1:
					iEventPlayer = iPlayerX
				iRow = screen.appendTableRow("WBEventPlayer")
				sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
				if iPlayerX == iEventPlayer:
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
					sHeader = pPlayerX.getName()
				iCivilization = pPlayerX.getCivilizationType()
				iLeader = pPlayerX.getLeaderType()
				screen.setTableText("WBEventPlayer", 0, iRow, "", gc.getCivilizationInfo(iCivilization).getButton(), WidgetTypes.WIDGET_PYTHON, 7872, iPlayerX * 10000 + iCivilization, CvUtil.FONT_LEFT_JUSTIFY )
				screen.setTableText("WBEventPlayer", 1, iRow, "<font=3>" + sColor + pPlayerX.getName() + "</font></color>", gc.getLeaderHeadInfo(iLeader).getButton(), WidgetTypes.WIDGET_PYTHON, 7876, iPlayerX * 10000 + iLeader, CvUtil.FONT_LEFT_JUSTIFY )
		
		screen.setLabel("EventPlayerText", "Background", "<font=3b>" + sHeader + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() * 3/10, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )


	def placeUnits(self):
		screen = CyGInterfaceScreen("WBEventScreen", CvScreenEnums.WB_EVENT)
		iHeight = (screen.getYResolution() - self.iTable_Y - 42) / 24 * 24 + 2

		sHeader = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ())
		nColumns = 3
		screen.addTableControlGFC("WBEventUnit", nColumns, screen.getXResolution() * 4/5 + 10, self.iTable_Y, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("WBEventUnit", 0, "", 24)
		screen.setTableColumnHeader("WBEventUnit", 1, "", 24)
		screen.setTableColumnHeader("WBEventUnit", 2, "", iWidth - 48)

		for i in xrange(pPlot.getNumUnits()):
			pUnitX = pPlot.getUnit(i)
			if pUnitX.isNone(): continue
			iRow = screen.appendTableRow("WBEventUnit")
			sText = pUnitX.getName()
			if len(pUnitX.getNameNoDesc()):
				sText = pUnitX.getNameNoDesc()
			iPlayerX = pUnitX.getOwner()
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if pUnitX.getID() == iSelectedUnit:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				sHeader = sText
			screen.setTableText("WBEventUnit", 2, iRow, "<font=3>" + sColor + sText + "</font></color>", pUnitX.getButton(), WidgetTypes.WIDGET_PYTHON, 8300 + iPlayerX, pUnitX.getID(), CvUtil.FONT_LEFT_JUSTIFY)
			pPlayerX = gc.getPlayer(iPlayerX)
			iLeader = pPlayerX.getLeaderType()
			iCiv = pUnitX.getCivilizationType()
			screen.setTableText("WBEventUnit", 0, iRow, "", gc.getCivilizationInfo(iCiv).getButton(), WidgetTypes.WIDGET_PYTHON, 7872, iCiv, CvUtil.FONT_LEFT_JUSTIFY )
			screen.setTableText("WBEventUnit", 1, iRow, "", gc.getLeaderHeadInfo(iLeader).getButton(), WidgetTypes.WIDGET_PYTHON, 7876, iLeader, CvUtil.FONT_LEFT_JUSTIFY )
		screen.setLabel("EventUnitText", "Background", "<font=3b>" + sHeader + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() *9/10, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	def placeCorporations(self):
		screen = CyGInterfaceScreen("WBEventScreen", CvScreenEnums.WB_EVENT)
		iHeight = (screen.getYResolution()/2 - 72) / 24 * 24 + 2

		sHeader = CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ())
		screen.addTableControlGFC("WBEventCorporation", 1, screen.getXResolution() * 3/5 + 10, screen.getYResolution()/2 + 30, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("WBEventCorporation", 0, "", iWidth)

		for item in lCorporations:
			iRow = screen.appendTableRow("WBEventCorporation")
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if item[1] == iSelectedCorporation:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				sHeader = item[0]
			screen.setTableText("WBEventCorporation", 0, iRow, "<font=3>" + sColor + item[0] + "</font></color>", gc.getCorporationInfo(item[1]).getButton(), WidgetTypes.WIDGET_PYTHON, 8201, item[1], CvUtil.FONT_LEFT_JUSTIFY )
		screen.setLabel("EventCorporationText", "Background", "<font=3b>" + sHeader + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() *7/10, screen.getYResolution()/2, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	def placeReligions(self):
		screen = CyGInterfaceScreen("WBEventScreen", CvScreenEnums.WB_EVENT)
		iHeight = (screen.getYResolution()/2 - 72) / 24 * 24 + 2

		sHeader = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ())
		screen.addTableControlGFC("WBEventReligion", 1, screen.getXResolution() * 2/5 + 10, screen.getYResolution()/2 + 30, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("WBEventReligion", 0, "", iWidth)

		for item in lReligions:
			iRow = screen.appendTableRow("WBEventReligion")
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if item[1] == iSelectedReligion:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				sHeader = item[0]
			screen.setTableText("WBEventReligion", 0, iRow, "<font=3>" + sColor + item[0] + "</font></color>", gc.getReligionInfo(item[1]).getButton(), WidgetTypes.WIDGET_HELP_RELIGION, item[1], -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.setLabel("EventReligionText", "Background", "<font=3b>" + sHeader + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() /2, screen.getYResolution()/2, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	def placeBuildings(self):
		screen = CyGInterfaceScreen("WBEventScreen", CvScreenEnums.WB_EVENT)
		iHeight = (screen.getYResolution()/2 - 72) / 24 * 24 + 2

		sHeader = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ())
		screen.addTableControlGFC("WBEventBuilding", 1, screen.getXResolution()/5 + 10, screen.getYResolution()/2 + 30, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("WBEventBuilding", 0, "", iWidth)

		for item in lBuildings:
			iRow = screen.appendTableRow("WBEventBuilding")
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if item[1] == iSelectedBuilding:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				sHeader = item[0]
			screen.setTableText("WBEventBuilding", 0, iRow, "<font=3>" + sColor + item[0] + "</font></color>", gc.getBuildingInfo(item[1]).getButton(), WidgetTypes.WIDGET_HELP_BUILDING, item[1], -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.setLabel("EventBuildingText", "Background", "<font=3b>" + sHeader + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() * 3/10, screen.getYResolution()/2, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	def placeOtherCities(self):
		screen = CyGInterfaceScreen("WBEventScreen", CvScreenEnums.WB_EVENT)
		if iOtherPlayer == -1:
			screen.hide("WBOtherCity")
			return
		iHeight = (screen.getYResolution()/2 - self.iTable_Y - 2) / 24 * 24 + 2

		sHeader = CyTranslator().getText("TXT_KEY_WB_CITY", ()) + " II"
		screen.addTableControlGFC("WBOtherCity", 1, screen.getXResolution() * 3/5 + 10, self.iTable_Y, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("WBOtherCity", 0, "", iWidth)

		(loopCity, iter) = gc.getPlayer(iOtherPlayer).firstCity(False)
		while(loopCity):
			iRow = screen.appendTableRow("WBOtherCity")
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if loopCity.getID() == iOtherCity:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				sHeader = loopCity.getName()
			screen.setTableText("WBOtherCity", 0, iRow, "<font=3>" + sColor + loopCity.getName() + "</font></color>", "", WidgetTypes.WIDGET_PYTHON, 7200 + iOtherPlayer, loopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
			(loopCity, iter) = gc.getPlayer(iOtherPlayer).nextCity(iter, False)
		screen.setLabel("OtherCityText", "Background", "<font=3b>" + sHeader + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() *7/10, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
	def placeOtherPlayers(self):
		screen = CyGInterfaceScreen("WBEventScreen", CvScreenEnums.WB_EVENT)
		iHeight = (screen.getYResolution()/2 - self.iTable_Y - 2) / 24 * 24 + 2

		sHeader = CyTranslator().getText("TXT_KEY_MAIN_MENU_PLAYER", ()) + " II"
		screen.addTableControlGFC("WBOtherPlayer", 2, screen.getXResolution() * 2/5 + 10, self.iTable_Y, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("WBOtherPlayer", 0, "", 24)
		screen.setTableColumnHeader("WBOtherPlayer", 1, "", iWidth - 24)

		for iPlayerX in xrange(gc.getMAX_CIV_PLAYERS()):
			if iPlayerX == iEventPlayer: continue
			pPlayerX = gc.getPlayer(iPlayerX)
			if pPlayerX.isAlive():
				iRow = screen.appendTableRow("WBOtherPlayer")
				sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
				if iPlayerX == iOtherPlayer:
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
					sHeader = pPlayerX.getName()
				iCivilization = pPlayerX.getCivilizationType()
				iLeader = pPlayerX.getLeaderType()
				screen.setTableText("WBOtherPlayer", 0, iRow, "", gc.getCivilizationInfo(iCivilization).getButton(), WidgetTypes.WIDGET_PYTHON, 7872, iPlayerX * 10000 + iCivilization, CvUtil.FONT_LEFT_JUSTIFY )
				screen.setTableText("WBOtherPlayer", 1, iRow, "<font=3>" + sColor + pPlayerX.getName() + "</font></color>", gc.getLeaderHeadInfo(iLeader).getButton(), WidgetTypes.WIDGET_PYTHON, 7876, iPlayerX * 10000 + iLeader, CvUtil.FONT_LEFT_JUSTIFY )
		
		screen.setLabel("OtherPlayerText", "Background", "<font=3b>" + sHeader + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	def placeEvents(self):
		screen = CyGInterfaceScreen("WBEventScreen", CvScreenEnums.WB_EVENT)
		iHeight = (screen.getYResolution() - self.iTable_Y - 42) / 24 * 24 + 2
		screen.addTableControlGFC( "WBEvent", 1, 10, self.iTable_Y, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader( "WBEvent", 0, "", iWidth)
		sHeader = CyTranslator().getText("TXT_KEY_CONCEPT_EVENTS", ())
		screen.setLabel("EventText", "Background", "<font=3b>" + sHeader + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() /10, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		for item in lEvents:
			iRow = screen.appendTableRow("WBEvent")
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if item[1] == iSelectedEvent:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				sHeader = item[0]
			screen.setTableText("WBEvent", 0, iRow, "<font=3>" + sColor + item[0] + "</font></color>", "", WidgetTypes.WIDGET_PYTHON, 1030, item[1], CvUtil.FONT_LEFT_JUSTIFY )
		if iSelectedEvent > -1:
			sText = "<font=4b>" + CyTranslator().getText("[COLOR_BLACK]", ()) + CyTranslator().getText("TXT_KEY_WB_TRIGGER_EVENT", (sHeader,)).upper() + "</color></font>"
			screen.setButtonGFC("TriggerEvent", sText, "", screen.getXResolution()/4, 20, screen.getXResolution()/2, 30, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)

	def handleInput(self, inputClass):
		screen = CyGInterfaceScreen( "WBEventScreen", CvScreenEnums.WB_EVENT)
		global iSelectedEvent
		global iEventPlayer
		global iOtherPlayer
		global iOtherCity
		global iSelectedReligion
		global iSelectedCorporation
		global iSelectedUnit
		global iSelectedBuilding

		if inputClass.getFunctionName() == "CurrentPage":
			iIndex = screen.getPullDownData("CurrentPage", screen.getSelectedPullDownID("CurrentPage"))
			if iIndex == 0:
				WBPlotScreen.WBPlotScreen().interfaceScreen(pPlot)
			elif iIndex == 2:
				WBPlayerScreen.WBPlayerScreen().interfaceScreen(pPlot.getOwner())
			elif iIndex == 3:
				WBTeamScreen.WBTeamScreen().interfaceScreen(pPlot.getTeam())
			elif iIndex == 4:
				if pPlot.isCity():
					WBCityEditScreen.WBCityEditScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).interfaceScreen(pPlot.getPlotCity())
			elif iIndex == 5:
				if iSelectedUnit > -1 and iEventPlayer > -1:
					pUnit = gc.getPlayer(iEventPlayer).getUnit(iSelectedUnit)
				else:
					pUnit = pPlot.getUnit(0)
				if pUnit:
					WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).interfaceScreen(pUnit)
			elif iIndex == 11:
				iPlayer = pPlot.getOwner()
				if iPlayer == -1:
					iPlayer = CyGame().getActivePlayer()
				WBInfoScreen.WBInfoScreen().interfaceScreen(iPlayer)

		elif inputClass.getFunctionName() == "WBEvent":
			iSelectedEvent = inputClass.getData2()
			self.placeEvents()

		elif inputClass.getFunctionName() == "WBEventPlayer":
			if inputClass.getData1() == 7876 or inputClass.getData1() == 7872:
				iEventPlayer = inputClass.getData2() /10000
				iSelectedUnit = -1
				if iEventPlayer == iOtherPlayer:
					iOtherPlayer = -1
					iOtherCity = -1
				self.placeEventPlayers()
				self.placeOtherPlayers()
				self.placeOtherCities()
				self.placeUnits()

		elif inputClass.getFunctionName() == "WBOtherPlayer":
			if inputClass.getData1() == 7876 or inputClass.getData1() == 7872:
				iTemp = inputClass.getData2() /10000
				if iOtherPlayer == iTemp:
					iOtherPlayer = -1
				else:
					iOtherPlayer = iTemp
				iOtherCity = -1
				self.placeOtherPlayers()
				self.placeOtherCities()

		elif inputClass.getFunctionName() == "WBOtherCity":
			iTemp = inputClass.getData2()
			if iOtherCity == iTemp:
				iOtherCity = -1
			else:
				iOtherCity = iTemp
			self.placeOtherCities()

		elif inputClass.getFunctionName() == "WBEventReligion":
			iTemp = inputClass.getData1()
			if iSelectedReligion == iTemp:
				iSelectedReligion = -1
			else:
				iSelectedReligion = iTemp
			self.placeReligions()

		elif inputClass.getFunctionName() == "WBEventCorporation":
			iTemp = inputClass.getData2()
			if iSelectedCorporation == iTemp:
				iSelectedCorporation = -1
			else:
				iSelectedCorporation = iTemp
			self.placeCorporations()

		elif inputClass.getFunctionName() == "WBEventBuilding":
			iTemp = inputClass.getData1()
			if iSelectedBuilding == iTemp:
				iSelectedBuilding = -1
			else:
				iSelectedBuilding = iTemp
			self.placeBuildings()

		elif inputClass.getFunctionName() == "WBEventUnit":
			if inputClass.getData1() > 8299 and inputClass.getData1() < 8400:
				iUnit = inputClass.getData2()
				if iSelectedUnit == iUnit:
					iSelectedUnit = -1
				else:
					iSelectedUnit = iUnit
				iEventPlayer = inputClass.getData1() - 8300
				if iEventPlayer == iOtherPlayer:
					iOtherPlayer = -1
					iOtherCity = -1
				self.placeEventPlayers()
				self.placeOtherPlayers()
				self.placeOtherCities()
				self.placeUnits()

		elif inputClass.getFunctionName() == "TriggerEvent":
			if iEventPlayer == -1: return
			pPlayer = gc.getPlayer(iEventPlayer)
			iCity = -1
			if pPlot.isCity():
				iCity = pPlot.getPlotCity().getID()
			triggerData = pPlayer.initTriggeredData(iSelectedEvent, True, iCity, pPlot.getX(), pPlot.getY(), iOtherPlayer, iOtherCity, iSelectedReligion, iSelectedCorporation, iSelectedUnit, iSelectedBuilding)
			screen.hideScreen()
		return 1

	def update(self, fDelta):
		return 1