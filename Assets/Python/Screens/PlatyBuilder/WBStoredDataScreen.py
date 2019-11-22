from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import Popup
import WBReligionScreen
import WBCorporationScreen
import WBGameDataScreen
import WBPlayerEnabledScreen
import WBInfoScreen
import Barbs
import AIWars
import BugData
import DynamicCivs as dc
gc = CyGlobalContext()

iChange = 1
iSelectedCiv = -1
bRemove = False
iSelectedMode = 0

scriptDict = {}
lBools = []
lInts = []
lLists = []
iSelectedList = 0
iWarList = 0

from StoredData import data
from Consts import *
from RFCUtils import utils

class WBStoredDataScreen:

	def __init__(self, main):
		self.top = main

	def interfaceScreen(self):
		screen = CyGInterfaceScreen("WBStoredDataScreen", CvScreenEnums.WB_STOREDDATA)

		screen.setRenderInterfaceOnly(True)
		screen.addPanel( "MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.setLabel("StoredDataHeader", "Background", "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_STOREDDATA",()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() /2, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText("StoredDataExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		iWidth = screen.getXResolution()/4 - 40
		screen.addDropDownBoxGFC("ChangeBy", 20, 50, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		i = 1
		while i < 100001:
			screen.addPullDownString("ChangeBy", "(+/-) " + str(i), i, i, iChange == i)
			if str(i)[0] == "1":
				i *= 5
			else:
				i *= 2

		screen.addDropDownBoxGFC("ChangeType", 20, 50 + 35, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_ADD", ()), 1, 1, not bRemove)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_REMOVE", ()), 0, 0, bRemove)

		# Reset button, loads the storedData saved when opening this screen
		screen.setButtonGFC("RestoreBackup", CyTranslator().getText("TXT_KEY_WB_RESTORE_SD_BACKUP", ()), "", 20, 50 + 2*35, iWidth, 30, WidgetTypes.WIDGET_PYTHON, 22013, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("CreateBackup", CyTranslator().getText("TXT_KEY_WB_CREATE_SD_BACKUP", ()), "", 20, 50 + 3*35, iWidth, 30, WidgetTypes.WIDGET_PYTHON, 22014, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

		# Warning texts
		sWarning = "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_STOREDDATA_WARNING",()).upper() + "</font>"
		screen.addMultilineText ("Warning", sWarning, 20, 50 + 4*35, iWidth, 100, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		# Mode
		screen.addDropDownBoxGFC("SelectMode", 20, 50 + 5*35 + 100, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("SelectMode", CyTranslator().getText("TXT_KEY_WB_GLOBAL", ()), 0, 0, iSelectedMode == 0)
		screen.addPullDownString("SelectMode", CyTranslator().getText("TXT_KEY_WB_CIVS", ()), 1, 1, iSelectedMode == 1)

		# Civ selection
		screen.addDropDownBoxGFC("SelectCiv", 20, 50 + 6*35 + 100, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("SelectCiv", CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ()), -1, -1, iSelectedCiv == -1)
		for i in range(iNumPlayers):
			screen.addPullDownString("SelectCiv", CyTranslator().getText(str(gc.getPlayer(i).getCivilizationShortDescriptionKey()), ()), i, i, iSelectedCiv == i)

		screen.addDropDownBoxGFC("CurrentPage", 20, screen.getYResolution() - 42, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ()), 8, 8, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ()), 9, 9, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PITBOSS_GAME_OPTIONS", ()), 10, 10, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_INFO_SCREEN", ()), 11, 11, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_STOREDDATA", ()), 12, 12, True)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLAYER_ENABLED", ()), 13, 13, False)

		self.loadData()

	def loadData(self):
		global scriptDict
		global lBools
		global lInts
		global lLists
		global iSelectedMode
		global iSelectedCiv

		if iSelectedMode == 0:
			scriptDict = data.__dict__
		else:
			if iSelectedCiv == -1:
				iSelectedCiv = 0
			scriptDict = data.players[iSelectedCiv].__dict__
		lBools = sorted([item for item in scriptDict.keys() if item[0] == "b"])
		lInts = sorted([item for item in scriptDict.keys() if item[0] == "i"])
		lLists = sorted([item for item in scriptDict.keys() if item[0] == "l"])

		self.placeDataTable()
		self.placeListTables()
		self.placeCivButton()

	def placeCivButton(self):
		screen = CyGInterfaceScreen( "WBStoredDataScreen", CvScreenEnums.WB_STOREDDATA)
		global iSelectedCiv

		if iSelectedMode != 0 and iSelectedCiv == -1:
			iSelectedCiv = 0

		iWidth = screen.getXResolution() * 3 / 4 - 40
		iHeight = (screen.getYResolution() - 85 - 50 - 50) / 2
		iSize = 64
		iSize2 = 64 + 20
		iX = screen.getXResolution() / 4 - iSize2 - 20

		screen.addPanel("CivButtonPanel", "", "", True, True, iX, 85 + iHeight - iSize2, iSize2, iSize2, PanelStyles.PANEL_STYLE_MAIN)
		if iSelectedCiv == -1:
			ArtKey = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
			screen.addDDSGFC("CivButtonButton", ArtKey, iX + 10, 85 + iHeight - iSize2 + 10, iSize, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			ArtKey = gc.getCivilizationInfo(gc.getPlayer(iSelectedCiv).getCivilizationType()).getButton()
			screen.addDDSGFC("CivButtonButton", ArtKey, iX + 10, 85 + iHeight - iSize2 + 10, iSize, iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, gc.getPlayer(iSelectedCiv).getCivilizationType(), -1)

	def placeDataTable(self):
		screen = CyGInterfaceScreen( "WBStoredDataScreen", CvScreenEnums.WB_STOREDDATA)
		global scriptDict
		global lBools
		global lInts

		iWidth = screen.getXResolution() * 3 / 4 - 40
		iHeight = self.allignTable((screen.getYResolution() - 85 - 50 - 50) / 2)
		iWidth2 = iWidth / 6

		screen.addTableControlGFC("WBDataTable", 6, screen.getXResolution() / 4, 85, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		for i in range(6):
			screen.setTableColumnHeader("WBDataTable", i, "", iWidth2)

		iNumRows = max(len(lBools), len(lInts)/2)
		for i in range(iNumRows):
			screen.appendTableRow("WBDataTable")

		for i in range(len(lBools)):
			screen.setTableText("WBDataTable", 0, i, lBools[i], "", WidgetTypes.WIDGET_PYTHON, -1, i, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("WBDataTable", 1, i, str(scriptDict[lBools[i]]), "", WidgetTypes.WIDGET_PYTHON, 22007, i, CvUtil.FONT_LEFT_JUSTIFY)

		for i in range(len(lInts)):
			item = lInts[i]
			iColumn = i / iNumRows
			iRow = i % iNumRows
			screen.setTableText("WBDataTable", 2*iColumn+2, iRow, item, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			sText = str(scriptDict[item])
			if item == "iPlayer":
				screen.setTableText("WBDataTable", 2*iColumn+3, iRow, sText, "", WidgetTypes.WIDGET_PYTHON, 22010, i, CvUtil.FONT_LEFT_JUSTIFY)
			else:
				if item == "iStabilityLevel":
					sText += u" (%s)" % CyTranslator().getText(StabilityLevelTexts[scriptDict[item]], ())
				elif item in ["iNextTurnAIWar"]:
					sText += u" (Turn %s)" % getTurnForYear(scriptDict[item])
				elif item == "iFirstNewWorldColony":
					sText = self.getCivName(scriptDict[item])
				screen.setTableText("WBDataTable", 2*iColumn+3, iRow, sText, "", WidgetTypes.WIDGET_PYTHON, 22008, i, CvUtil.FONT_LEFT_JUSTIFY)

	def placeListTables(self):
		screen = CyGInterfaceScreen( "WBStoredDataScreen", CvScreenEnums.WB_STOREDDATA)
		global scriptDict
		global lLists
		global iSelectedList
		global iSelectedCiv
		global iWarList

		bCiv = lLists[iSelectedList] in ["lFirstDiscovered", "lWonderBuilder", "lReligionFounder", "lFirstEntered", "lFirstGreatPeople"]

		iWidth = (screen.getXResolution() * 3 / 4 - 40) / 2 - 40
		iHeightMax = self.allignTable((screen.getYResolution() - 85 - 50 - 50) / 2)
		iHeight = iHeightMax
		iWidth1 = iWidth / 5 * 2
		iWidth2 = iWidth / 5 * 3
		iWidth3 = iWidth / 2

		if lLists[iSelectedList] == "lWarTrend":
			iHeight = self.allignTable(iHeight / 2 - 50)

		# Table with lists
		screen.addTableControlGFC("WBListTable", 2, screen.getXResolution() / 4, screen.getYResolution() - 50 - iHeightMax, iWidth, iHeightMax, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("WBListTable", 0, "", iWidth1)
		screen.setTableColumnHeader("WBListTable", 1, "", iWidth2)

		for i in range(len(lLists)):
			screen.appendTableRow("WBListTable")
			screen.setTableText("WBListTable", 0, i, lLists[i], "", WidgetTypes.WIDGET_PYTHON, 22009, i, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("WBListTable", 1, i, str(scriptDict[lLists[i]]), "", WidgetTypes.WIDGET_PYTHON, 22009, i, CvUtil.FONT_LEFT_JUSTIFY)

		screen.addDDSGFCAt("WBArrow", "MainBG", CyArtFileMgr().getInterfaceArtInfo("LINE_ARROW").getPath(), screen.getXResolution() / 4 + iWidth + 20, screen.getYResolution() - 50 - iHeightMax/2, 60, 24, WidgetTypes.WIDGET_GENERAL, -1, -1, False)

		# Detailed list
		screen.addTableControlGFC("WBListTableTwo", 2, screen.getXResolution() / 4 + iWidth + 2*40, screen.getYResolution() - 50 - iHeightMax, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("WBListTableTwo", 0, "", iWidth3)
		screen.setTableColumnHeader("WBListTableTwo", 1, "", iWidth3)

		item = lLists[iSelectedList]
		lSelectedList = scriptDict[item]
		for i in range(len(lSelectedList)):
			screen.appendTableRow("WBListTableTwo")

			if item == "lWarTrend":
				sText = CyTranslator().getText(str(gc.getPlayer(i).getCivilizationShortDescriptionKey()), ())
				screen.setTableText("WBListTableTwo", 0, i, sText, gc.getCivilizationInfo(gc.getPlayer(i).getCivilizationType()).getButton(), WidgetTypes.WIDGET_PYTHON, 22009, i, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText("WBListTableTwo", 1, i, str(lSelectedList[i]), "", WidgetTypes.WIDGET_PYTHON, 22009, i, CvUtil.FONT_LEFT_JUSTIFY)
				continue

			elif item == "lPlayerEnabled": # Secondary civs
				sText = CyTranslator().getText(str(gc.getPlayer(lSecondaryCivs[i]).getCivilizationShortDescriptionKey()), ())
				screen.setTableText("WBListTableTwo", 0, i, sText, gc.getCivilizationInfo(gc.getPlayer(lSecondaryCivs[i]).getCivilizationType()).getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			elif item == "lFirstContactConquerors": # New world civs conquerors
				sText = CyTranslator().getText(str(gc.getPlayer(lCivBioNewWorld[i]).getCivilizationShortDescriptionKey()), ())
				screen.setTableText("WBListTableTwo", 0, i, sText, gc.getCivilizationInfo(gc.getPlayer(lCivBioNewWorld[i]).getCivilizationType()).getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			elif item == "lFirstContactMongols": # Mongol conquerors
				sText = CyTranslator().getText(str(gc.getPlayer(lMongolCivs[i]).getCivilizationShortDescriptionKey()), ())
				screen.setTableText("WBListTableTwo", 0, i, sText, gc.getCivilizationInfo(gc.getPlayer(lMongolCivs[i]).getCivilizationType()).getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

			elif item == "lMinorCityFounded":
				sText = Barbs.tMinorCities[i][3]
				screen.setTableText("WBListTableTwo", 0, i, sText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

			elif item == "lFirstDiscovered": # Technologies
				sText = gc.getTechInfo(i).getDescription()
				screen.setTableText("WBListTableTwo", 0, i, sText, gc.getTechInfo(i).getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			elif item == "lWonderBuilder": # Wonders
				sText = gc.getBuildingInfo(i+iBeginWonders).getDescription()
				screen.setTableText("WBListTableTwo", 0, i, sText, gc.getBuildingInfo(i+iBeginWonders).getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			elif item == "lReligionFounder": # Religions
				sText = gc.getReligionInfo(i).getDescription()
				screen.setTableText("WBListTableTwo", 0, i, sText, gc.getReligionInfo(i).getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			elif item == "lFirstEntered": # Eras
				sText = gc.getEraInfo(i).getDescription()
				screen.setTableText("WBListTableTwo", 0, i, sText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			elif item == "lFirstGreatPeople": # Great People
				sText = gc.getUnitInfo(lGreatPeopleUnits[i]).getDescription()
				screen.setTableText("WBListTableTwo", 0, i, sText, gc.getUnitInfo(lGreatPeopleUnits[i]).getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			elif item == "lStabilityCategoryValues": # Stability Categories
				sText = CyTranslator().getText(StabilityTypesTexts[i], ())
				screen.setTableText("WBListTableTwo", 0, i, sText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			elif item == "lWarStartTurn":
				sText = CyTranslator().getText(str(gc.getPlayer(i).getCivilizationShortDescriptionKey()), ())
				screen.setTableText("WBListTableTwo", 0, i, sText, gc.getCivilizationInfo(gc.getPlayer(i).getCivilizationType()).getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			elif item == "lConquest":
				sAttacker = CyTranslator().getText(str(gc.getPlayer(AIWars.lConquests[i][1]).getCivilizationShortDescriptionKey()), ())
				sDefender = CyTranslator().getText(str(gc.getPlayer(AIWars.lConquests[i][2]).getCivilizationShortDescriptionKey()), ())
				sText = sAttacker + " - " + sDefender
				screen.setTableText("WBListTableTwo", 0, i, sText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			elif item == "lGoals":
				sText = u"UHV%d: " % (i+1)
				sText += utils.getGoalText(iSelectedCiv, i, True)
				screen.setTableText("WBListTableTwo", 0, i, sText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			else:
				screen.setTableText("WBListTableTwo", 0, i, str(i), "", WidgetTypes.WIDGET_PYTHON, -1, i, CvUtil.FONT_LEFT_JUSTIFY)

			if bCiv:
				sText = self.getCivName(lSelectedList[i])
				if lSelectedList[i] == -1:
					screen.setTableText("WBListTableTwo", 1, i, sText, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), WidgetTypes.WIDGET_PYTHON, 22008, i, CvUtil.FONT_LEFT_JUSTIFY)
				else:
					screen.setTableText("WBListTableTwo", 1, i, sText, gc.getCivilizationInfo(gc.getPlayer(lSelectedList[i]).getCivilizationType()).getButton(), WidgetTypes.WIDGET_PYTHON, 22008, i, CvUtil.FONT_LEFT_JUSTIFY)
			else:
				sText = str(lSelectedList[i])
				if item in ["lGenericPlagueDates", "lWarStartTurn"]:
					iYear = gc.getGame().getTurnYear(lSelectedList[i])
					if iYear < 0:
						sBC = CyTranslator().getText("TXT_KEY_BC", ())
					else:
						sBC = CyTranslator().getText("TXT_KEY_AD", ())
					sText += u" (%d %s)" % (abs(gc.getGame().getTurnYear(lSelectedList[i])), sBC)
				elif item == "lGoals":
					lVicConditionTexts = ["TXT_KEY_VICTORY_SCREEN_NOTYET", "TXT_KEY_VICTORY_GOAL_FAILED", "TXT_KEY_VICTORY_GOAL_ACCOMPLISHED"]
					sText += u" (%s)" % CyTranslator().getText(lVicConditionTexts[lSelectedList[i]+1], ())
				screen.setTableText("WBListTableTwo", 1, i, sText, "", WidgetTypes.WIDGET_PYTHON, 22008, i, CvUtil.FONT_LEFT_JUSTIFY)


		screen.hide("WBListTableThree")
		if lLists[iSelectedList] == "lWarTrend":
			iHeight = 10 * 24 + 2
			screen.addTableControlGFC("WBListTableThree", 2, screen.getXResolution() / 4 + iWidth + 2*40, screen.getYResolution() - 50 - iHeight, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
			screen.setTableColumnHeader("WBListTableThree", 0, "", iWidth3)
			screen.setTableColumnHeader("WBListTableThree", 1, "", iWidth3)

			for i in range(len(lSelectedList[iWarList])):
				screen.appendTableRow("WBListTableThree")
				screen.setTableText("WBListTableThree", 0, i, str(i), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText("WBListTableThree", 1, i, str(lSelectedList[iWarList][i]), "", WidgetTypes.WIDGET_PYTHON, 22008, i, CvUtil.FONT_LEFT_JUSTIFY)


	def changeListTableValue(self, iItem, iValue):
		global lLists
		global iSelectedList
		if iSelectedMode == 0:
			data.__dict__[lLists[iSelectedList]][iItem] = iValue
		else:
			data.players[iSelectedCiv].__dict__[lLists[iSelectedList]][iItem] = iValue
		self.placeListTables()

	def getCivName(self, iCiv):
		if iCiv < 0:
			return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
		return CyTranslator().getText(str(gc.getPlayer(iCiv).getCivilizationShortDescriptionKey()), ())

	def handleInput(self, inputClass):
		screen = CyGInterfaceScreen("WBStoredDataScreen", CvScreenEnums.WB_STOREDDATA)
		global iChange
		global iSelectedCiv
		global bRemove
		global iSelectedMode

		global scriptDict
		global lBools
		global lInts
		global lLists
		global iSelectedList
		global iWarList

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

		elif inputClass.getFunctionName() == "SelectMode":
			iSelectedMode = screen.getPullDownData("SelectMode", screen.getSelectedPullDownID("SelectMode"))
			iSelectedList = 0
			self.loadData()

		elif inputClass.getFunctionName() == "SelectCiv":
			iSelectedCiv = screen.getPullDownData("SelectCiv", screen.getSelectedPullDownID("SelectCiv"))
			self.placeCivButton()
			if iSelectedMode == 1:
				self.loadData()

		elif inputClass.getFunctionName() == "WBDataTable":
			if inputClass.getData1() == 22007:
				item = lBools[inputClass.getData2()]
				if iSelectedMode == 0:
					data.__dict__[item] = not data.__dict__[item]
				else:
					data.players[iSelectedCiv].__dict__[item] = not data.players[iSelectedCiv].__dict__[item]
			elif inputClass.getData1() == 22008:
				item = lInts[inputClass.getData2()]
				if iSelectedMode == 0:
					iValue = data.__dict__[item]
				else:
					iValue = data.players[iSelectedCiv].__dict__[item]

				iValue += iChange

				if item == "iStabilityLevel":
					iValue = max(iStabilityCollapsing, min(iValue, iStabilitySolid))
				elif item == "iFirstNewWorldColony":
					iValue = iSelectedCiv

				if iSelectedMode == 0:
					data.__dict__[item] = iValue
				else:
					data.players[iSelectedCiv].__dict__[item] = iValue
			if iSelectedMode == 0:
				for iPlayer in range(iNumPlayers):
					if not gc.getPlayer(iPlayer).isAlive(): continue
					dc.checkName(iPlayer)
			else:
				dc.checkName(iSelectedCiv)
			self.placeDataTable()

		elif inputClass.getFunctionName() == "WBListTable":
			iSelectedList = inputClass.getData2()
			self.placeListTables()

		elif inputClass.getFunctionName() == "WBListTableTwo":
			iItem = inputClass.getData2()
			sList = lLists[iSelectedList]

			if sList == "lWarTrend":
				iWarList = iItem
			elif isinstance(scriptDict[sList][iItem], bool):
				if iSelectedMode == 0:
					data.__dict__[sList][iItem] = not data.__dict__[sList][iItem]
				else:
					data.players[iSelectedCiv].__dict__[sList][iItem] = not data.players[iSelectedCiv].__dict__[sList][iItem]
			elif isinstance(scriptDict[sList][iItem], int):
				bCiv = sList in ["lFirstDiscovered", "lWonderBuilder", "lReligionFounder", "lFirstEntered", "lFirstGreatPeople"]
				if bCiv:
					data.__dict__[sList][iItem] = iSelectedCiv
				else:
					if sList in ["lGoals", "lEconomyTrend"]:
						iValue = data.players[iSelectedCiv].__dict__[sList][iItem] + abs(iChange) / iChange
						iValue = max(-1, min(iValue, 1))
						data.players[iSelectedCiv].__dict__[sList][iItem] = iValue
					elif sList == "lHappinessTrend":
						if bRemove:
							iValue = -1
						else:
							iValue = 1
						data.players[iSelectedCiv].__dict__[sList][iItem] = iValue
					else:
						popup = Popup.PyPopup(7777, EventContextTypes.EVENTCONTEXT_ALL)
						if iSelectedMode == 0:
							sText = str(data.__dict__[sList][iItem])
						else:
							sText = str(data.players[iSelectedCiv].__dict__[sList][iItem])
						popup.setUserData((iItem, -1))
						popup.createEditBox(sText)
						popup.launch()
						return 1
			if iSelectedMode == 0:
				for iPlayer in range(iNumPlayers):
					if not gc.getPlayer(iPlayer).isAlive(): continue
					dc.checkName(iPlayer)
			else:
				dc.checkName(iSelectedCiv)
			self.placeListTables()


		elif inputClass.getFunctionName() == "WBListTableThree":
			iItem = inputClass.getData2()
			data.players[iSelectedCiv].__dict__["lWarTrend"][iWarList][iItem] += iChange
			self.placeListTables()

		elif inputClass.getFunctionName() == "RestoreBackup":
			BugData.onGameLoad(-1)
			self.loadData()
		elif inputClass.getFunctionName() == "CreateBackup":
			BugData.save()

		return 1

	def update(self, fDelta):
		return 1

	def allignTable(self, x):
		return int(24 * round(float(x-2)/24))+2