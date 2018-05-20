from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import WBGameDataScreen
import WBReligionScreen
import WBPlayerScreen
import WBPlayerEnabledScreen
import WBTeamScreen
import WBCityEditScreen
import WBInfoScreen
import CvPlatyBuilderScreen
import WBStoredDataScreen
gc = CyGlobalContext()

bHeadquarter = False
iOwnerType = 0
lCities = []

class WBCorporationScreen:

	def __init__(self):
		self.iTable_Y = 80

	def interfaceScreen(self, iPlayerX):
		screen = CyGInterfaceScreen("WBCorporationScreen", CvScreenEnums.WB_CORPORATION)
		global iSelectedPlayer

		iSelectedPlayer = iPlayerX

		screen.setRenderInterfaceOnly(True)
		screen.addPanel("MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
	
		screen.setText("WBCorporationExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setLabel("CorporationHeader", "Background", "<font=4b>" + CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 20, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabel("HeadquarterHeader", "Background", "<font=3b>" + CyTranslator().getText("TXT_KEY_CORPORATION_HEADQUARTERS", ()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/8, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		iWidth = screen.getXResolution()/4 - 40
		screen.addDropDownBoxGFC("CurrentPage", 20, screen.getYResolution() - 42, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA", ()), 0, 0, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_TEAM_DATA", ()), 1, 1, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ()), 8, 8, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ()), 9, 9, True)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PITBOSS_GAME_OPTIONS", ()), 10, 10, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_INFO_SCREEN", ()), 11, 11, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_STOREDDATA", ()), 12, 12, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLAYER_ENABLED", ()), 13, 13, False)

		screen.addDropDownBoxGFC("OwnerType", screen.getXResolution()/4, self.iTable_Y - 60, 150, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("OwnerType", CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()), 0, 0, 0 == iOwnerType)
		screen.addPullDownString("OwnerType", CyTranslator().getText("TXT_KEY_PITBOSS_TEAM", ()), 2, 2, 2 == iOwnerType)
		screen.addPullDownString("OwnerType", CyTranslator().getText("TXT_KEY_MAIN_MENU_PLAYER", ()), 1, 1, 1 == iOwnerType)

		screen.addDropDownBoxGFC("CurrentPlayer", screen.getXResolution()/4, self.iTable_Y - 30, 150, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i in xrange(gc.getMAX_PLAYERS()):
			pPlayerX = gc.getPlayer(i)
			if pPlayerX.isEverAlive():
				sText = pPlayerX.getName()
				if not pPlayerX.isAlive():
					sText = "*" + sText
				if pPlayerX.isTurnActive():
					sText = "[" + sText + "]"
				screen.addPullDownString("CurrentPlayer", sText, i, i, i == iSelectedPlayer)

		sText = "<font=3b>" + CyTranslator().getText("TXT_KEY_CORPORATION_HEADQUARTERS", ()) + "</font>"
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if bHeadquarter:
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setText("SetHeadquarter", "Background", sColor + sText + "</color>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 20, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		self.placeHeadquarter()
		self.sortCities()

	def sortCities(self):
		global lCities
		lCities = []
		iSelectedTeam = gc.getPlayer(iSelectedPlayer).getTeam()
		for iPlayerX in xrange(gc.getMAX_PLAYERS()):
			pPlayerX = gc.getPlayer(iPlayerX)
			if iOwnerType == 1 and iPlayerX != iSelectedPlayer: continue
			if iOwnerType == 2 and pPlayerX.getTeam() != iSelectedTeam: continue
			(loopCity, iter) = pPlayerX.firstCity(False)
			while(loopCity):
				lCities.append([loopCity, iPlayerX])
				(loopCity, iter) = pPlayerX.nextCity(iter, False)
		self.placeCityTable()

	def placeCityTable(self):
		screen = CyGInterfaceScreen("WBCorporationScreen", CvScreenEnums.WB_CORPORATION)
		iX = screen.getXResolution()/4
		iY = self.iTable_Y
		iWidth = screen.getXResolution() * 3/4 - 20
		iHeight = (screen.getYResolution() - iY - 100) / 24 * 24 + 2

		screen.addTableControlGFC("WBAllCorporations", 1 + gc.getNumCorporationInfos(), iX, iY, iWidth, 50, False, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("WBAllCorporations", 0, "", 150)
		for i in xrange(2):
			screen.appendTableRow("WBAllCorporations")
		sText = CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ())
		screen.setTableText("WBAllCorporations", 0, 0, "<font=3b>" + sText + " (+)</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText("WBAllCorporations", 0, 1, "<font=3b>" + sText + " (-)</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

		for i in xrange(gc.getNumCorporationInfos()):
			sText = u"%c" %(gc.getCorporationInfo(i).getChar())
			screen.setTableColumnHeader("WBAllCorporations", i + 1, "", (iWidth - 150) / gc.getNumCorporationInfos())
			screen.setTableText("WBAllCorporations", i + 1, 0, "<font=4>" + sText + "</font>", "", WidgetTypes.WIDGET_PYTHON, 6782, i, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText("WBAllCorporations", i + 1, 1, "<font=4>" + sText + "</font>", "", WidgetTypes.WIDGET_PYTHON, 8201, i, CvUtil.FONT_CENTER_JUSTIFY)
			
		screen.addTableControlGFC("WBCityCorporations", 3 + gc.getNumCorporationInfos(), iX, iY + 60, iWidth, iHeight, False, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("WBCityCorporations", 0, "", 24)
		screen.setTableColumnHeader("WBCityCorporations", 1, "", 24)
		screen.setTableColumnHeader("WBCityCorporations", 2, "", 102)
		for i in xrange(gc.getNumCorporationInfos()):
			screen.setTableColumnHeader("WBCityCorporations", i + 3, "", (iWidth - 150) / gc.getNumCorporationInfos())

		for (loopCity, iPlayerX) in lCities:
			pPlayerX = gc.getPlayer(iPlayerX)
			iLeader = pPlayerX.getLeaderType()
			iCiv = pPlayerX.getCivilizationType()
			sColor = u"<color=%d,%d,%d,%d>" %(pPlayerX.getPlayerTextColorR(), pPlayerX.getPlayerTextColorG(), pPlayerX.getPlayerTextColorB(), pPlayerX.getPlayerTextColorA())
			iRow = screen.appendTableRow("WBCityCorporations")
			screen.setTableText("WBCityCorporations", 0, iRow, "", gc.getCivilizationInfo(iCiv).getButton(), WidgetTypes.WIDGET_PYTHON, 7872, iCiv, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText("WBCityCorporations", 1, iRow, "", gc.getLeaderHeadInfo(iLeader).getButton(), WidgetTypes.WIDGET_PYTHON, 7876, iLeader, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText("WBCityCorporations", 2, iRow, "<font=3>" + sColor + loopCity.getName() + "</color></font>", "", WidgetTypes.WIDGET_PYTHON, 7200 + iPlayerX, loopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
			for i in xrange(gc.getNumCorporationInfos()):
				sText = " "
				if loopCity.isHasCorporation(i):
					sText = u"%c" %(gc.getCorporationInfo(i).getChar())
				if loopCity.isHeadquartersByType(i):
					sText = u"%c" %(gc.getCorporationInfo(i).getHeadquarterChar())
				screen.setTableText("WBCityCorporations", i + 3, iRow, "<font=4>" + sText + "</font>", "", WidgetTypes.WIDGET_PYTHON, 8201, i, CvUtil.FONT_CENTER_JUSTIFY)

	def placeHeadquarter(self):
		screen = CyGInterfaceScreen("WBCorporationScreen", CvScreenEnums.WB_CORPORATION)
		iX = 20
		iY = self.iTable_Y
		iWidth = screen.getXResolution()/4 - 40
		iHeight = (screen.getYResolution() - iY - 40) / 24 * 24 + 2

		screen.addTableControlGFC("WBHeadquarter", 3, iX, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("WBHeadquarter", 0, "", 24)
		screen.setTableColumnHeader("WBHeadquarter", 1, "", 24)
		screen.setTableColumnHeader("WBHeadquarter", 2, "", iWidth - 48)

		for i in xrange(gc.getNumCorporationInfos()):
			iRow = screen.appendTableRow("WBHeadquarter")
			screen.setTableText("WBHeadquarter", 0, iRow, "", gc.getCorporationInfo(i).getButton(), WidgetTypes.WIDGET_PYTHON, 8201, i, CvUtil.FONT_LEFT_JUSTIFY)
			pHeadquarter = CyGame().getHeadquarters(i)
			if not pHeadquarter.isNone():
				iPlayerX = pHeadquarter.getOwner()
				pPlayerX = gc.getPlayer(iPlayerX)
				sColor = u"<color=%d,%d,%d,%d>" %(pPlayerX.getPlayerTextColorR(), pPlayerX.getPlayerTextColorG(), pPlayerX.getPlayerTextColorB(), pPlayerX.getPlayerTextColorA())
				iLeader = pPlayerX.getLeaderType()
				screen.setTableText("WBHeadquarter", 1, iRow, "", gc.getLeaderHeadInfo(iLeader).getButton(), WidgetTypes.WIDGET_PYTHON, 7876, iPlayerX * 10000 + iLeader, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText("WBHeadquarter", 2, iRow, "<font=3>" + sColor + pHeadquarter.getName() + "</color></font>", gc.getCivilizationInfo(pHeadquarter.getCivilizationType()).getButton(), WidgetTypes.WIDGET_PYTHON, 7200 + iPlayerX, pHeadquarter.getID(), CvUtil.FONT_LEFT_JUSTIFY)
	
	def handleInput(self, inputClass):
		screen = CyGInterfaceScreen("WBCorporationScreen", CvScreenEnums.WB_CORPORATION)
		global iSelectedPlayer
		global bHeadquarter
		global iOwnerType

		if inputClass.getButtonType() == WidgetTypes.WIDGET_PYTHON:
			if inputClass.getData1() > 7199 and inputClass.getData1() < 7300:
				iCityID = inputClass.getData2()
				iPlayerX = inputClass.getData1() - 7200
				WBCityEditScreen.WBCityEditScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).interfaceScreen(gc.getPlayer(iPlayerX).getCity(iCityID))

			elif inputClass.getData1() == 7876 or inputClass.getData1() == 7872:
				iPlayerX = inputClass.getData2() /10000
				WBPlayerScreen.WBPlayerScreen().interfaceScreen(iPlayerX)

		if inputClass.getFunctionName() == "CurrentPage":
			iIndex = screen.getPullDownData("CurrentPage", screen.getSelectedPullDownID("CurrentPage"))
			if iIndex == 0:
				WBPlayerScreen.WBPlayerScreen().interfaceScreen(iSelectedPlayer)
			elif iIndex == 1:
				WBTeamScreen.WBTeamScreen().interfaceScreen(gc.getPlayer(iSelectedPlayer).getTeam())
			elif iIndex == 8:
				WBReligionScreen.WBReligionScreen().interfaceScreen(iSelectedPlayer)
			elif iIndex == 10:
				WBGameDataScreen.WBGameDataScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).interfaceScreen()
			elif iIndex == 11:
				WBInfoScreen.WBInfoScreen().interfaceScreen(iSelectedPlayer)
			elif iIndex == 12:
				WBStoredDataScreen.WBStoredDataScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).interfaceScreen()
			elif iIndex == 13:
				WBPlayerEnabledScreen.WBPlayerEnabledScreen(self.top).interfaceScreen()

		elif inputClass.getFunctionName() == "OwnerType":
			iOwnerType = screen.getPullDownData("OwnerType", screen.getSelectedPullDownID("OwnerType"))
			self.sortCities()

		elif inputClass.getFunctionName() == "CurrentPlayer":
			iSelectedPlayer = screen.getPullDownData("CurrentPlayer", screen.getSelectedPullDownID("CurrentPlayer"))
			self.interfaceScreen(iSelectedPlayer)

		elif inputClass.getFunctionName() == "WBCityCorporations":
			if inputClass.getData1() == 8201:
				pCity = lCities[inputClass.getData()][0]
				if bHeadquarter:
					self.editHeadquarter(inputClass.getData2(), pCity)
				else:
					self.editCorporation(inputClass.getData2(), pCity, 2)
				self.placeCityTable()

		elif inputClass.getFunctionName() == "WBAllCorporations":
			if inputClass.getButtonType() == WidgetTypes.WIDGET_PYTHON:
				for (loopCity, iPlayerX) in lCities:
					self.editCorporation(inputClass.getData2(), loopCity, inputClass.getData1() == 6782)
				self.placeCityTable()

		elif inputClass.getFunctionName() == "SetHeadquarter":
			bHeadquarter = not bHeadquarter
			sText = "<font=3b>" + CyTranslator().getText("TXT_KEY_CORPORATION_HEADQUARTERS", ()) + "</font>"
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if bHeadquarter:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			screen.modifyString("SetHeadquarter", sColor + sText + "</color>", 0)
		return 1

	def editHeadquarter(self, item, pCity):
		if pCity.isHeadquartersByType(item):
			CyGame().clearHeadquarters(item)
		else:
			CyGame().setHeadquarters(item, pCity, False)
		self.placeHeadquarter()

	def editCorporation(self, item, pCity, iType):
		if iType == 2:
			iType = not pCity.isHasCorporation(item)
		if not iType and pCity.isHeadquartersByType(item):
			CyGame().clearHeadquarters(item)
			self.placeHeadquarter()
		pCity.setHasCorporation(item, iType, False, False)

	def update(self, fDelta):
		return 1