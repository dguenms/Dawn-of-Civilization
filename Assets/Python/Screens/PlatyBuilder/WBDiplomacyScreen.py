from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import WBPlayerScreen
import CvPlatyBuilderScreen
import CvEventManager
import WBTradeScreen
import DynamicCivs as dc
gc = CyGlobalContext()

iChange = 1
bRemove = False
bTowardsPlayer = False
iSelectedMemory = 0
iSelectedPlayer = 0
iSelectedTeam = 0
lPlayers = []
bHideDead = True
bDiplomacyPage = False

class WBDiplomacyScreen:

	def __init__(self):
		self.iTable_Y = 110
		self.lAttitude = ["COLOR_RED", "COLOR_MAGENTA", "", "COLOR_CYAN", "COLOR_GREEN"]

	def interfaceScreen(self, iPlayerX, bPage):
		screen = CyGInterfaceScreen("WBDiplomacyScreen", CvScreenEnums.WB_DIPLOMACY)
		global bDiplomacyPage
		bDiplomacyPage = bPage

		screen.setRenderInterfaceOnly(True)
		screen.addPanel( "MainBG", "", "", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
	
		screen.setText("DiplomacyExit", "Background", "<font=4b>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 25, screen.getYResolution() - 40, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		
		iWidth = screen.getXResolution()/5
		screen.addDropDownBoxGFC("ChangeType", 20, 50, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_ADD", ()), 1, 1, not bRemove)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_REMOVE", ()), 0, 0, bRemove)
		
		screen.addDropDownBoxGFC("ChangeBy", 20, 80, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		i = 1
		while i < 1000001:
			screen.addPullDownString("ChangeBy", "(+/-) " + str(i), i, i, iChange == i)
			if str(i)[0] == "1":
				i *= 5
			else:
				i *= 2

		screen.addDropDownBoxGFC("CurrentPage", 20, screen.getYResolution() - 42, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_GLOBELAYER_RESOURCES_GENERAL", ()), 0, 0, not bDiplomacyPage)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_ESPIONAGE_CULTURE", ()), 1, 1, bDiplomacyPage)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_CONCEPT_TRADE", ()), 2, 2, False)
		
		sText = "<font=3b>" + CyTranslator().getText("TXT_KEY_WB_HIDE_DEAD", ()) + "</font>"
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if bHideDead:
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setText("HideDead", "Background", sColor + sText + "</color>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 20, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		self.setPlayerList(iPlayerX)

		if bDiplomacyPage:
			self.setEspionagePage()
		else:
			self.setGeneralPage()

	def setPlayerList(self, iPlayer):
		screen = CyGInterfaceScreen("WBDiplomacyScreen", CvScreenEnums.WB_DIPLOMACY)
		global iSelectedPlayer
		global pSelectedPlayer
		global iSelectedTeam
		global pSelectedTeam
		global lPlayers

		iSelectedPlayer = iPlayer
		pSelectedPlayer = gc.getPlayer(iSelectedPlayer)
		iSelectedTeam = pSelectedPlayer.getTeam()

		if bHideDead and not pSelectedPlayer.isAlive():
			iSelectedPlayer = -1
			iSelectedTeam = -1

		iWidth = screen.getXResolution()/5
		screen.addDropDownBoxGFC("CurrentPlayer", 20, 20, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		lPlayers = []
		for iPlayerX in xrange(gc.getMAX_PLAYERS()):
			pPlayerX = gc.getPlayer(iPlayerX)
			if pPlayerX.isEverAlive():
				if bHideDead and not pPlayerX.isAlive(): continue
				if iSelectedPlayer == -1:
					iSelectedPlayer = iPlayerX
					pSelectedPlayer = gc.getPlayer(iSelectedPlayer)
					iSelectedTeam = pPlayerX.getTeam()
				sText = pPlayerX.getName()
				if not pPlayerX.isAlive():
					sText = "*" + sText
				if pPlayerX.isTurnActive():
					sText = "[" + sText + "]"
				screen.addPullDownString("CurrentPlayer", sText, iPlayerX, iPlayerX, iPlayerX == iSelectedPlayer)
				if pPlayerX.getTeam() != iSelectedTeam:
					lPlayers.append(iPlayerX)

		pSelectedTeam = gc.getTeam(iSelectedTeam)
		sText = u"%s >>> %s" %(gc.getPlayer(iSelectedPlayer).getName(), CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()))
		if bTowardsPlayer:
			sText = u"%s >>> %s" %(CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()), gc.getPlayer(iSelectedPlayer).getName())
		sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=3b>" + sText + "</color></font>"
		screen.setText("TowardsPlayer", "Background", sText, CvUtil.FONT_LEFT_JUSTIFY, 20 + iWidth, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
	def setGeneralPage(self):
		screen = CyGInterfaceScreen( "WBDiplomacyScreen", CvScreenEnums.WB_DIPLOMACY)
		sText = "%s: %s\t" %(CyTranslator().getText("[ICON_ANGRYPOP]", ()), CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_CONTACT", ()))
		sText += "%s: %s\t" %(CyTranslator().getText("[ICON_OPENBORDERS]", ()), CyTranslator().getText("TXT_KEY_MISC_OPEN_BORDERS", ()))
		sText += "%s: %s\t" %(CyTranslator().getText("[ICON_DEFENSIVEPACT]", ()), CyTranslator().getText("TXT_KEY_MISC_DEFENSIVE_PACT", ()))
		sText += "%s: %s" %(CyTranslator().getText("[ICON_OCCUPATION]", ()), CyTranslator().getText("TXT_KEY_CONCEPT_WAR", ()))
		screen.setLabel("LegendText", "Background", "<font=3b>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, screen.getXResolution()/5 + 20, screen.getYResolution() - 40, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iWidth = screen.getXResolution() - 40
		iHeight = screen.getYResolution() - self.iTable_Y - 40
		screen.addTableControlGFC( "WBDiplomacy", 10, 20, self.iTable_Y, iWidth, iHeight, True, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		iWidth -= 150
		iWidth1 = iWidth /6
		iWidth2 = iWidth /4
		screen.setTableColumnHeader("WBDiplomacy", 0, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIV", ()), iWidth2)
		screen.setTableColumnHeader("WBDiplomacy", 1, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_LEADER", ()), iWidth2)
		screen.setTableColumnHeader("WBDiplomacy", 2, CyTranslator().getText("TXT_KEY_PITBOSS_TEAM", ()), 50)
		screen.setTableColumnHeader("WBDiplomacy", 3, CyTranslator().getText("TXT_KEY_WB_ATTITUDE", ()), iWidth1)
		screen.setTableColumnHeader("WBDiplomacy", 4, CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_RELATIONS", ()), iWidth1)
		screen.setTableColumnHeader("WBDiplomacy", 5, CyTranslator().getText("[ICON_ANGRYPOP]", ()), 25)
		screen.setTableColumnHeader("WBDiplomacy", 6, CyTranslator().getText("[ICON_OPENBORDERS]", ()), 25)
		screen.setTableColumnHeader("WBDiplomacy", 7, CyTranslator().getText("[ICON_DEFENSIVEPACT]", ()), 25)
		screen.setTableColumnHeader("WBDiplomacy", 8, CyTranslator().getText("[ICON_OCCUPATION]", ()), 25)
		screen.setTableColumnHeader("WBDiplomacy", 9, CyTranslator().getText("TXT_KEY_CONCEPT_WAR_WEARINESS", ()), iWidth1)

		sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + " (+/-)</font></color>"
		iX = 20 + iWidth2 * 2 + 50 + iWidth1
		screen.setText("AttitudeAll", "Background",  sText, CvUtil.FONT_RIGHT_JUSTIFY, iX, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iX += iWidth1
		screen.addTableControlGFC("DiplomacyAll", 4, iX, self.iTable_Y - 30, 125, 50, False, True, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
		screen.appendTableRow("DiplomacyAll")
		for i in xrange(4):
			screen.setTableColumnHeader("DiplomacyAll", i, "", 24)
		screen.setTableText("DiplomacyAll", 0, 0, "<font=4>" + CyTranslator().getText("[ICON_ANGRYPOP]", ()) + "<\font>", "", WidgetTypes.WIDGET_PYTHON, 1030, 0, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText("DiplomacyAll", 1, 0, "<font=4>" + CyTranslator().getText("[ICON_OPENBORDERS]", ()) + "<\font>", "", WidgetTypes.WIDGET_PYTHON, 1030, 1, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText("DiplomacyAll", 2, 0, "<font=4>" + CyTranslator().getText("[ICON_DEFENSIVEPACT]", ()) + "<\font>", "", WidgetTypes.WIDGET_PYTHON, 1030, 2, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText("DiplomacyAll", 3, 0, "<font=4>" + CyTranslator().getText("[ICON_OCCUPATION]", ()) + "<\font>", "", WidgetTypes.WIDGET_PYTHON, 1030, 3, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setLabel("DiplomacyAllText", "Background", "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, iX, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText("WearinessAll", "Background",  sText, CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 20, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		for iPlayer in lPlayers:
			iRow = screen.appendTableRow("WBDiplomacy")
			pPlayer = gc.getPlayer(iPlayer)
			iTeam = pPlayer.getTeam()
			pTeam = gc.getTeam(iTeam)
			sColor = u"<color=%d,%d,%d,%d>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA())
			iCivilization = pPlayer.getCivilizationType()
			sText = pPlayer.getCivilizationShortDescription(0)
			screen.setTableText("WBDiplomacy", 0, iRow, "<font=3>" + sColor + sText + "</font></color>", gc.getCivilizationInfo(iCivilization).getButton(), WidgetTypes.WIDGET_PYTHON, 7872, iPlayer * 10000 + iCivilization, CvUtil.FONT_LEFT_JUSTIFY )
			iLeader = pPlayer.getLeaderType()
			sText = pPlayer.getName()
			if not pPlayer.isAlive():
				sText = "*" + sText
			if pPlayer.isTurnActive():
				sText = "[" + sText + "]"
			screen.setTableText("WBDiplomacy", 1, iRow, "<font=3>" + sColor + sText + "</font></color>", gc.getLeaderHeadInfo(iLeader).getButton(), WidgetTypes.WIDGET_PYTHON, 7876, iPlayer * 10000 + iLeader, CvUtil.FONT_LEFT_JUSTIFY )
			screen.setTableInt("WBDiplomacy", 2, iRow, "<font=3>" + sColor + str(iTeam) + "</font></color>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY )
			
			if bTowardsPlayer:
				iAttitude = pPlayer.AI_getAttitude(iSelectedPlayer)
				sWeariness = str(pTeam.getWarWeariness(iSelectedTeam))
			else:
				iAttitude = gc.getPlayer(iSelectedPlayer).AI_getAttitude(iPlayer)
				sWeariness = str(gc.getTeam(iSelectedTeam).getWarWeariness(iTeam))
			sText = CyTranslator().changeTextColor(gc.getAttitudeInfo(iAttitude).getDescription(), gc.getInfoTypeForString(self.lAttitude[iAttitude]))
			screen.setTableText("WBDiplomacy", 3, iRow, "<font=3>" + sText + "</font>", "", WidgetTypes.WIDGET_PYTHON, 1030, iPlayer, CvUtil.FONT_CENTER_JUSTIFY)
			
			if bTowardsPlayer:
				iRelationshipStatus = self.RelationshipStatus(iTeam, iSelectedTeam)
			else:
				iRelationshipStatus = self.RelationshipStatus(iSelectedTeam, iTeam)
			sText = CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
			if iRelationshipStatus == 0:
				sText = CyTranslator().getText("TXT_KEY_WB_CVASSAL",())
			elif iRelationshipStatus == 1:
				sText = CyTranslator().getText("TXT_KEY_MISC_VASSAL_SHORT",())
			elif iRelationshipStatus == 3:
				sText = CyTranslator().getText("TXT_KEY_MISC_MASTER",())
			screen.setTableText("WBDiplomacy", 4, iRow, "<font=3>" + sText + "</font>", "", WidgetTypes.WIDGET_PYTHON, 1031, iTeam, CvUtil.FONT_CENTER_JUSTIFY)
			
			sText = ""
			if pTeam.isHasMet(iSelectedTeam):
				sText = CyTranslator().getText("[ICON_ANGRYPOP]",())
			screen.setTableText("WBDiplomacy", 5, iRow, "<font=4>" + sText + "</font>", "", WidgetTypes.WIDGET_PYTHON, 1032, iTeam , CvUtil.FONT_CENTER_JUSTIFY)
			sText = ""
			if pTeam.isOpenBorders(iSelectedTeam):
				sText = CyTranslator().getText("[ICON_OPENBORDERS]",())
			screen.setTableText("WBDiplomacy", 6, iRow, "<font=4>" + sText + "</font>", "", WidgetTypes.WIDGET_PYTHON, 1033, iTeam , CvUtil.FONT_CENTER_JUSTIFY)
			sText = ""
			if pTeam.isDefensivePact(iSelectedTeam):
				sText = CyTranslator().getText("[ICON_DEFENSIVEPACT]",())
			screen.setTableText("WBDiplomacy", 7, iRow, "<font=4>" + sText + "</font>", "", WidgetTypes.WIDGET_PYTHON, 1034, iTeam , CvUtil.FONT_CENTER_JUSTIFY)
			sText = ""
			if pTeam.isAtWar(iSelectedTeam):
				sText = CyTranslator().getText("[ICON_OCCUPATION]",())
			screen.setTableText("WBDiplomacy", 8, iRow, "<font=4>" + sText + "</font>", "", WidgetTypes.WIDGET_PYTHON, 1035, iTeam , CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText("WBDiplomacy", 9, iRow, "<font=3>" + sWeariness + "</font>", "", WidgetTypes.WIDGET_PYTHON, 1036, iTeam, CvUtil.FONT_RIGHT_JUSTIFY)
			
	def setEspionagePage(self):
		screen = CyGInterfaceScreen( "WBDiplomacyScreen", CvScreenEnums.WB_DIPLOMACY)
		screen.addDropDownBoxGFC("CurrentMemory", screen.getXResolution()/5 + 20, screen.getYResolution() - 40, 450, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i in xrange(MemoryTypes.NUM_MEMORY_TYPES):
			screen.addPullDownString("CurrentMemory", gc.getMemoryInfo(i).getDescription(), i, i, i == iSelectedMemory)

		iWidth = screen.getXResolution() - 40
		iHeight = screen.getYResolution() - self.iTable_Y - 40
		screen.addTableControlGFC( "WBEspionage", 9, 20, self.iTable_Y, iWidth, iHeight, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		iWidth1 = iWidth /8
		iWidth2 = iWidth *3/16
		screen.setTableColumnHeader("WBEspionage", 0, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIV", ()), iWidth2)
		screen.setTableColumnHeader("WBEspionage", 1, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_LEADER", ()), iWidth2)
		screen.setTableColumnHeader("WBEspionage", 2, CyTranslator().getText("TXT_KEY_ESPIONAGE_CULTURE", ()), iWidth1)
		screen.setTableColumnHeader("WBEspionage", 3, CyTranslator().getText("TXT_KEY_ESPIONAGE_SCREEN_SPENDING_WEIGHT", ()), iWidth1)
		screen.setTableColumnHeader("WBEspionage", 4, CyTranslator().getText("TXT_KEY_REPLAY_SCREEN_TURNS", ()), iWidth1)
		screen.setTableColumnHeader("WBEspionage", 5, CyTranslator().getText("TXT_KEY_WB_MODIFIER", ()), iWidth1)
		screen.setTableColumnHeader("WBEspionage", 6, CyTranslator().getText("TXT_KEY_WB_MEMORY", ()), iWidth1)

		sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + " (+/-)</font></color>"
		iX = screen.getXResolution() - 20 - iWidth1
		screen.setText("CEModifierAll", "Background", sText, CvUtil.FONT_RIGHT_JUSTIFY, iX, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iX -= iWidth1
		screen.setText("CETurnsAll", "Background", sText, CvUtil.FONT_RIGHT_JUSTIFY, iX, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabel("CounterEspionageHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_WB_COUNTER_ESPIONAGE", ()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, iX, self.iTable_Y - 60, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iX -= iWidth1
		screen.setText("WeightAll", "Background", sText, CvUtil.FONT_RIGHT_JUSTIFY, iX, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iX -= iWidth1
		screen.setText("EspionageAll", "Background", sText, CvUtil.FONT_RIGHT_JUSTIFY, iX, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabel("EspionageHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_ESPIONAGE_CULTURE", ()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, iX, self.iTable_Y - 60, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		for iPlayer in lPlayers:
			iRow = screen.appendTableRow("WBEspionage")
			pPlayer = gc.getPlayer(iPlayer)
			iTeam = pPlayer.getTeam()
			pTeam = gc.getTeam(iTeam)
			sColor = u"<color=%d,%d,%d,%d>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA())
			iCivilization = pPlayer.getCivilizationType()
			screen.setTableText("WBEspionage", 0, iRow, "<font=3>" + sColor + pPlayer.getCivilizationShortDescription(0) + "</font></color>", gc.getCivilizationInfo(iCivilization).getButton(), WidgetTypes.WIDGET_PYTHON, 7872, iPlayer * 10000 + iCivilization, CvUtil.FONT_LEFT_JUSTIFY )
			iLeader = pPlayer.getLeaderType()
			sText = pPlayer.getName()
			if not pPlayer.isAlive():
				sText = "*" + sText
			if pPlayer.isTurnActive():
				sText = "[" + sText + "]"
			screen.setTableText("WBEspionage", 1, iRow, "<font=3>" + sColor + sText + "</font></color>", gc.getLeaderHeadInfo(iLeader).getButton(), WidgetTypes.WIDGET_PYTHON, 7876, iPlayer * 10000 + iLeader, CvUtil.FONT_LEFT_JUSTIFY )
			if bTowardsPlayer:
				sMemory = str(pPlayer.AI_getMemoryCount(iSelectedPlayer, iSelectedMemory))
				sEspionage = str(pTeam.getEspionagePointsAgainstTeam(iSelectedTeam))
				sWeight = str(pPlayer.getEspionageSpendingWeightAgainstTeam(iSelectedTeam))
				sTurns = str(pTeam.getCounterespionageTurnsLeftAgainstTeam(iSelectedTeam))
				sModifier = str(pTeam.getCounterespionageModAgainstTeam(iSelectedTeam))
			else:
				sMemory = str(gc.getPlayer(iSelectedPlayer).AI_getMemoryCount(iPlayer, iSelectedMemory))
				sEspionage = str(gc.getTeam(iSelectedTeam).getEspionagePointsAgainstTeam(iTeam))
				sWeight = str(gc.getPlayer(iSelectedPlayer).getEspionageSpendingWeightAgainstTeam(iTeam))
				sTurns = str(gc.getTeam(iSelectedTeam).getCounterespionageTurnsLeftAgainstTeam(iTeam))
				sModifier = str(gc.getTeam(iSelectedTeam).getCounterespionageModAgainstTeam(iTeam))
			screen.setTableInt("WBEspionage", 2, iRow, "<font=3>" + sEspionage + "</font>", "", WidgetTypes.WIDGET_PYTHON, 1030, iTeam, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableInt("WBEspionage", 3, iRow, "<font=3>" + sWeight + "</font>", "", WidgetTypes.WIDGET_PYTHON, 1031, iPlayer, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableInt("WBEspionage", 4, iRow, "<font=3>" + sTurns + "</font>", "", WidgetTypes.WIDGET_PYTHON, 1032, iTeam, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableInt("WBEspionage", 5, iRow, "<font=3>" + sModifier + "</font>", "", WidgetTypes.WIDGET_PYTHON, 1033, iTeam, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableInt("WBEspionage", 6, iRow, "<font=3>" + sMemory + "</font>", "", WidgetTypes.WIDGET_PYTHON, 1034, iPlayer, CvUtil.FONT_RIGHT_JUSTIFY)
			
	def handleInput (self, inputClass):
		screen = CyGInterfaceScreen("WBDiplomacyScreen", CvScreenEnums.WB_DIPLOMACY)
		global iSelectedPlayer
		global iSelectedTeam
		global iChange
		global iSelectedMemory
		global bTowardsPlayer
		global bHideDead
		global bRemove
		global bDiplomacyPage

		if inputClass.getButtonType() == WidgetTypes.WIDGET_PYTHON:
			if inputClass.getData1() == 7876 or inputClass.getData1() == 7872:
				iPlayerX = inputClass.getData2() /10000
				WBPlayerScreen.WBPlayerScreen().interfaceScreen(iPlayerX)

		if inputClass.getFunctionName() == "ChangeBy":
			if bRemove:
				iChange = -screen.getPullDownData("ChangeBy", screen.getSelectedPullDownID("ChangeBy"))
			else:
				iChange = screen.getPullDownData("ChangeBy", screen.getSelectedPullDownID("ChangeBy"))

		elif inputClass.getFunctionName() == "ChangeType":
			bRemove = not bRemove
			iChange = -iChange

		elif inputClass.getFunctionName() == "CurrentPlayer":
			iSelectedPlayer = screen.getPullDownData("CurrentPlayer", screen.getSelectedPullDownID("CurrentPlayer"))
			self.interfaceScreen(iSelectedPlayer, bDiplomacyPage)
		elif inputClass.getFunctionName() == "CurrentPage":
			iIndex = screen.getPullDownData("CurrentPage", screen.getSelectedPullDownID("CurrentPage"))
			if iIndex == 2:
				WBTradeScreen.WBTradeScreen().interfaceScreen()
			elif iIndex != bDiplomacyPage:
				bDiplomacyPage = not bDiplomacyPage
				self.interfaceScreen(iSelectedPlayer, bDiplomacyPage)
		elif inputClass.getFunctionName() == "TowardsPlayer":
			bTowardsPlayer = not bTowardsPlayer
			self.interfaceScreen(iSelectedPlayer, bDiplomacyPage)
		elif inputClass.getFunctionName() == "HideDead":
			bHideDead = not bHideDead
			self.interfaceScreen(iSelectedPlayer, bDiplomacyPage)

		if bDiplomacyPage:
			if inputClass.getFunctionName() == "CurrentMemory":
				iSelectedMemory = inputClass.getData()
			elif inputClass.getFunctionName() == "EspionageAll":
				for iPlayerX in lPlayers:
					pPlayerX = gc.getPlayer(iPlayerX)
					iTeamX = pPlayerX.getTeam()
					if iPlayerX != gc.getTeam(iTeamX).getLeaderID(): continue
					self.editEspionagePoint(iTeamX)
			elif inputClass.getFunctionName() == "WeightAll":
				for iPlayerX in lPlayers:
					if not bTowardsPlayer:
						pPlayerX = gc.getPlayer(iPlayerX)
						iTeamX = pPlayerX.getTeam()
						if iPlayerX != gc.getTeam(iTeamX).getLeaderID(): continue
					self.editEspionageWeight(iPlayerX)
			elif inputClass.getFunctionName() == "CETurnsAll":
				for iPlayerX in lPlayers:
					pPlayerX = gc.getPlayer(iPlayerX)
					iTeamX = pPlayerX.getTeam()
					if iPlayerX != gc.getTeam(iTeamX).getLeaderID(): continue
					self.editCETurns(iTeamX)
			elif inputClass.getFunctionName() == "CEModifierAll":
				for iPlayerX in lPlayers:
					pPlayerX = gc.getPlayer(iPlayerX)
					iTeamX = pPlayerX.getTeam()
					if iPlayerX != gc.getTeam(iTeamX).getLeaderID(): continue
					self.editCEModifier(iTeamX)

			elif inputClass.getData1() == 1030:
				self.editEspionagePoint(inputClass.getData2())
			elif inputClass.getData1() == 1031:
				self.editEspionageWeight(inputClass.getData2())
			elif inputClass.getData1() == 1032:
				self.editCETurns(inputClass.getData2())
			elif inputClass.getData1() == 1033:
				self.editCEModifier(inputClass.getData2())
			elif inputClass.getData1() == 1034:
				self.editMemory(inputClass.getData2())
			self.setEspionagePage()

		else:
			if inputClass.getFunctionName() == "AttitudeAll":
				for iPlayerX in lPlayers:
					self.editAttitude(iPlayerX)
			elif inputClass.getFunctionName() == "DiplomacyAll":
				for iPlayerX in lPlayers:
					pPlayerX = gc.getPlayer(iPlayerX)
					iTeamX = pPlayerX.getTeam()
					if iPlayerX != gc.getTeam(iTeamX).getLeaderID(): continue
					if inputClass.getData2() == 0:
						self.editContact(iTeamX)
					if inputClass.getData2() == 1:
						self.editOpenBorders(iTeamX, bRemove)
					if inputClass.getData2() == 2:
						self.editDefensivePact(iTeamX, bRemove)
					if inputClass.getData2() == 3:
						self.editWarStatus(iTeamX, bRemove)
			elif inputClass.getFunctionName() == "WearinessAll":
				for iPlayerX in lPlayers:
					pPlayerX = gc.getPlayer(iPlayerX)
					iTeamX = pPlayerX.getTeam()
					if iPlayerX != gc.getTeam(iTeamX).getLeaderID(): continue
					self.editWarWeariness(iSelectedTeam, iTeamX)

			elif inputClass.getData1() == 1030:
				self.editAttitude(inputClass.getData2())
			elif inputClass.getData1() == 1031:
				self.editRelationship(inputClass.getData2())
			elif inputClass.getData1() == 1032:
				self.editContact(inputClass.getData2())
			elif inputClass.getData1() == 1033:
				self.editOpenBorders(inputClass.getData2(), pSelectedTeam.isOpenBorders(inputClass.getData2()))
			elif inputClass.getData1() == 1034:
				self.editDefensivePact(inputClass.getData2(), pSelectedTeam.isDefensivePact(inputClass.getData2()))
			elif inputClass.getData1() == 1035:
				self.editWarStatus(inputClass.getData2(), pSelectedTeam.isAtWar(inputClass.getData2()))
			elif inputClass.getData1() == 1036:
				self.editWarWeariness(iSelectedTeam, inputClass.getData2())
			self.setGeneralPage()
		return 1

	def editRelationship(self, iTeam):
		iTeam2 = iTeam
		iTeam1 = iSelectedTeam
		if bTowardsPlayer:
			iTeam1 = iTeam
			iTeam2 = iSelectedTeam
		iOldStatus = self.RelationshipStatus(iTeam1, iTeam2)
		if bRemove:
			iNewStatus = max(0, iOldStatus - 1)
		else:
			iNewStatus = min(3, iOldStatus + 1)
		if iOldStatus == iNewStatus: return
		gc.getTeam(iTeam1).freeVassal(iTeam2)
		gc.getTeam(iTeam2).freeVassal(iTeam1)
		if iNewStatus == 0:
			gc.getTeam(iTeam2).assignVassal(iTeam1, True)
		elif iNewStatus == 1:
			gc.getTeam(iTeam2).assignVassal(iTeam1, False)
		elif iNewStatus == 3:
			gc.getTeam(iTeam1).assignVassal(iTeam2, True)
		if CvPlatyBuilderScreen.bPython:
			if iNewStatus == 2:
				if iOldStatus == 3:
					CvEventManager.CvEventManager().onVassalState([iTeam1, iTeam2, False, False])
				else:
					CvEventManager.CvEventManager().onVassalState([iTeam2, iTeam1, False, False])
			elif iNewStatus == 3:
				CvEventManager.CvEventManager().onVassalState([iTeam1, iTeam2, True, True])
			else:
				CvEventManager.CvEventManager().onVassalState([iTeam2, iTeam1, True, iNewStatus == 0])
		dc.checkName(gc.getTeam(iTeam1).getLeaderID())
		dc.checkName(gc.getTeam(iTeam2).getLeaderID())

	def editContact(self, iTeam):
		if not bRemove:
			pSelectedTeam.meet(iTeam, False)

	def editWarStatus(self, iTeam, bCancel):
		if not pSelectedTeam.isHasMet(iTeam): return
		if gc.getTeam(iTeam).isVassal(iSelectedTeam): return
		if pSelectedTeam.isVassal(iTeam): return
		if bCancel:
			pSelectedTeam.makePeace(iTeam)
		else:
			pSelectedTeam.declareWar(iTeam, True, -1)

	def editDefensivePact(self, iTeam, bCancel):
		if not pSelectedTeam.isHasMet(iTeam): return
		if bCancel:
			for i in xrange(CyGame().getIndexAfterLastDeal()):
				pDeal = CyGame().getDeal(i)
				iPlayer1 = pDeal.getFirstPlayer()
				iPlayer2 = pDeal.getSecondPlayer()
				if iPlayer1 == -1 or iPlayer2 == -1: continue
				iTeam1 = gc.getPlayer(pDeal.getFirstPlayer()).getTeam()
				iTeam2 = gc.getPlayer(pDeal.getSecondPlayer()).getTeam()
				if (iTeam1 == iTeam and iTeam2 == iSelectedTeam) or (iTeam2 == iTeam and iTeam1 == iSelectedTeam):
					for j in xrange(pDeal.getLengthFirstTrades()):
						if pDeal.getFirstTrade(j).ItemType == TradeableItems.TRADE_DEFENSIVE_PACT:	
							pDeal.kill()
							self.interfaceScreen(iSelectedPlayer)
							return
		else:
			pSelectedTeam.signDefensivePact(iTeam)

	def editOpenBorders(self, iTeam, bCancel):
		if not pSelectedTeam.isHasMet(iTeam): return
		if bCancel:
			for i in xrange(CyGame().getIndexAfterLastDeal()):
				pDeal = CyGame().getDeal(i)
				iPlayer1 = pDeal.getFirstPlayer()
				iPlayer2 = pDeal.getSecondPlayer()
				if iPlayer1 == -1 or iPlayer2 == -1: continue
				iTeam1 = gc.getPlayer(pDeal.getFirstPlayer()).getTeam()
				iTeam2 = gc.getPlayer(pDeal.getSecondPlayer()).getTeam()
				if (iTeam1 == iTeam and iTeam2 == iSelectedTeam) or (iTeam2 == iTeam and iTeam1 == iSelectedTeam):
					for j in xrange(pDeal.getLengthFirstTrades()):
						if pDeal.getFirstTrade(j).ItemType == TradeableItems.TRADE_OPEN_BORDERS:	
							pDeal.kill()
							return
		else:
			pSelectedTeam.signOpenBorders(iTeam)

	def editEspionagePoint(self, iTeam):
		if not pSelectedTeam.isHasMet(iTeam): return
		iTeam2 = iTeam
		iTeam1 = iSelectedTeam
		if bTowardsPlayer:
			iTeam1 = iTeam
			iTeam2 = iSelectedTeam
		iCount = max(iChange, - gc.getTeam(iTeam1).getEspionagePointsAgainstTeam(iTeam2))
		gc.getTeam(iTeam1).changeEspionagePointsAgainstTeam(iTeam2, iCount)

	def editEspionageWeight(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iTeam = pPlayer.getTeam()
		if not pSelectedTeam.isHasMet(iTeam): return
		iTeam2 = iTeam
		iPlayer1 = iSelectedPlayer
		if bTowardsPlayer:
			iPlayer1 = iPlayer
			iTeam2 = iSelectedTeam
		iCount = abs(iChange)
		gc.getPlayer(iPlayer1).changeEspionageSpendingWeightAgainstTeam(iTeam2, iCount)

	def editCEModifier(self, iTeam):
		if not pSelectedTeam.isHasMet(iTeam): return
		iTeam2 = iTeam
		iTeam1 = iSelectedTeam
		if bTowardsPlayer:
			iTeam1 = iTeam
			iTeam2 = iSelectedTeam
		iCount = max(iChange, - gc.getTeam(iTeam1).getCounterespionageModAgainstTeam(iTeam2))
		gc.getTeam(iTeam1).changeCounterespionageModAgainstTeam(iTeam2, iCount)

	def editCETurns(self, iTeam):
		if not pSelectedTeam.isHasMet(iTeam): return
		iTeam2 = iTeam
		iTeam1 = iSelectedTeam
		if bTowardsPlayer:
			iTeam1 = iTeam
			iTeam2 = iSelectedTeam
		iCount = max(iChange, - gc.getTeam(iTeam1).getCounterespionageTurnsLeftAgainstTeam(iTeam2))
		gc.getTeam(iTeam1).changeCounterespionageTurnsLeftAgainstTeam(iTeam2, iCount)

	def editAttitude(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isBarbarian(): return
		iPlayer2 = iPlayer
		pPlayer1 = gc.getPlayer(iSelectedPlayer)
		if bTowardsPlayer:
			pPlayer1 = pPlayer
			iPlayer2 = iSelectedPlayer
		if self.RelationshipStatus(pPlayer1.getTeam(), gc.getPlayer(iPlayer2).getTeam()) == 1: return
		iCount = 1
		iNewAttitude = min(pPlayer1.AI_getAttitude(iPlayer2) + 1, AttitudeTypes.NUM_ATTITUDE_TYPES - 1)
		if bRemove:
			iCount = -1
			iNewAttitude = max(0, pPlayer1.AI_getAttitude(iPlayer2) - 1)
		while iNewAttitude != pPlayer1.AI_getAttitude(iPlayer2):
			pPlayer1.AI_changeAttitudeExtra(iPlayer2, iCount)

	def editMemory (self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iTeam = pPlayer.getTeam()
		if not pSelectedTeam.isHasMet(iTeam): return
		iPlayer2 = iPlayer
		pPlayer1 = gc.getPlayer(iSelectedPlayer)
		if bTowardsPlayer:
			pPlayer1 = gc.getPlayer(iPlayer)
			iPlayer2 = iSelectedPlayer
		iCount = max(iChange, - pPlayer1.AI_getMemoryCount(iPlayer2, iSelectedMemory))
		pPlayer1.AI_changeMemoryCount(iPlayer2, iSelectedMemory, iCount)

	def editWarWeariness(self, iTeam1, iTeam2):
		iCount = iChange
		if bTowardsPlayer:
			gc.getTeam(iTeam2).changeWarWeariness(iTeam1, iCount)
		else:
			gc.getTeam(iTeam1).changeWarWeariness(iTeam2, iCount)

	def RelationshipStatus(self, iTeam1, iTeam2):
		if gc.getTeam(iTeam1).isVassal(iTeam2):
			for i in range(CyGame().getIndexAfterLastDeal()):
				pDeal = CyGame().getDeal(i)
				iPlayer1 = pDeal.getFirstPlayer()
				iPlayer2 = pDeal.getSecondPlayer()
				if iPlayer1 == -1 or iPlayer2 == -1: continue
				iTeamX = gc.getPlayer(pDeal.getFirstPlayer()).getTeam()
				iTeamY = gc.getPlayer(pDeal.getSecondPlayer()).getTeam()
				if (iTeam1 == iTeamX and iTeam2 == iTeamY) or (iTeam2 == iTeamX and iTeam1 == iTeamY):
					for j in xrange(pDeal.getLengthFirstTrades()):
						if pDeal.getFirstTrade(j).ItemType == TradeableItems.TRADE_VASSAL:	
							return 1
						if pDeal.getFirstTrade(j).ItemType == TradeableItems.TRADE_SURRENDER:	
							return 0
					for j in xrange(pDeal.getLengthSecondTrades()):
						if pDeal.getSecondTrade(j).ItemType == TradeableItems.TRADE_VASSAL:	
							return 1
						if pDeal.getSecondTrade(j).ItemType == TradeableItems.TRADE_SURRENDER:	
							return 0
		elif gc.getTeam(iTeam2).isVassal(iTeam1):
			return 3
		return 2

	def update(self, fDelta):
		return 1