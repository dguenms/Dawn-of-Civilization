from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import WBProjectScreen
import WBTechScreen
import WBPlayerScreen
import WBPlayerUnits
import WBInfoScreen
import DynamicCivs as dc
gc = CyGlobalContext()

iChange = 1
bRemove = False
iSelectedYield = 0

class WBTeamScreen:

	def __init__(self):
		self.iTable_Y = 110

	def interfaceScreen(self, iTeamX):
		screen = CyGInterfaceScreen("WBTeamScreen", CvScreenEnums.WB_TEAM)
		global iTeam
		global pTeam

		iTeam = iTeamX
		pTeam = gc.getTeam(iTeam)
		iWidth = screen.getXResolution() /4 - 20

		screen.setRenderInterfaceOnly(True)
		screen.addPanel( "MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		sText = "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_TEAM_DATA",()).upper() + " (ID: " + str(iTeam) + ")</font>"
		screen.setLabel("TeamHeader", "Background", sText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText("TeamExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		
		screen.addDropDownBoxGFC("CurrentPage", 20, screen.getYResolution() - 42, iWidth - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA", ()), 0, 0, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_TEAM_DATA", ()), 1, 1, True)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()), 2, 2, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH", ()), 3, 3, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()) + " + " + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()), 4, 4, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_INFO_SCREEN", ()), 11, 11, False)

		screen.addDropDownBoxGFC("ChangeType", screen.getXResolution() - 170, 20, 150, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_ADD", ()), 1, 1, not bRemove)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_REMOVE", ()), 0, 0, bRemove)

		screen.addDropDownBoxGFC("ChangeBy", screen.getXResolution() - 170, 50, 150, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		i = 1
		while i < 1000001:
			screen.addPullDownString("ChangeBy", "(+/-) " + str(i), i, i, iChange == i)
			if str(i)[0] == "1":
				i *= 5
			else:
				i *= 2

		screen.addDropDownBoxGFC("CurrentTeam", 20, 20, iWidth - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i in xrange(gc.getMAX_TEAMS()):
			if gc.getTeam(i).isAlive():
				iLeader = gc.getTeam(i).getLeaderID()
				sName = gc.getPlayer(iLeader).getName()
				if gc.getTeam(i).getNumMembers() > 1:
					sName += " (" + str(gc.getTeam(i).getNumMembers()) + " " + CyTranslator().getText("TXT_KEY_MEMBERS_TITLE", ()) + ")"
				screen.addPullDownString("CurrentTeam", sName, i, i, i == iTeam)

		screen.addDropDownBoxGFC("MergeTeam", 20, 50, iWidth - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("MergeTeam", CyTranslator().getText("TXT_KEY_WB_MERGE_TEAM",()), -1, -1, True)
		for i in xrange(gc.getMAX_TEAMS()):
			if gc.getTeam(i).isAlive():
				if i == iTeam: continue
				iLeader = gc.getTeam(i).getLeaderID()
				sName = gc.getPlayer(iLeader).getName()
				if gc.getTeam(i).getNumMembers() > 1:
					sName += " (" + str(gc.getTeam(i).getNumMembers()) + " " + CyTranslator().getText("TXT_KEY_MEMBERS_TITLE", ()) + ")"
				screen.addPullDownString("MergeTeam", sName, i, i, False)

		global lImprovements
		global lRoutes
		global lVoteBuildings
		global lAbilities

		lImprovements = []
		for i in xrange(gc.getNumImprovementInfos()):
			ItemInfo = gc.getImprovementInfo(i)
			if ItemInfo.isGraphicalOnly(): continue
			lImprovements.append([ItemInfo.getDescription(), i])
		lImprovements.sort()

		lRoutes = []
		for i in xrange(gc.getNumRouteInfos()):
			ItemInfo = gc.getRouteInfo(i)
			lRoutes.append([ItemInfo.getDescription(), i])
		lRoutes.sort()

		lVoteBuildings = []
		for i in xrange(gc.getNumVoteSourceInfos()):
			iVoteBuilding = -1
			for j in xrange(gc.getNumBuildingInfos()):
				if gc.getBuildingInfo(j).getVoteSourceType() == i:
					iVoteBuilding = j
					break
			if iVoteBuilding == -1: continue
			lVoteBuildings.append([gc.getBuildingInfo(iVoteBuilding).getDescription(), iVoteBuilding])
		lVoteBuildings.sort()

		lAbilities = []
		for i in xrange(13):
			lAbilities.append([WidgetTypes.WIDGET_GENERAL, -1])
		for i in xrange(gc.getNumTechInfos()):
			ItemInfo = gc.getTechInfo(i)
			if ItemInfo.isMapCentering():
				lAbilities[0][0] = WidgetTypes.WIDGET_HELP_MAP_CENTER
				lAbilities[0][1] = i
			if ItemInfo.isMapTrading():
				lAbilities[1][0] = WidgetTypes.WIDGET_HELP_MAP_TRADE
				lAbilities[1][1] = i
			if ItemInfo.isTechTrading():
				lAbilities[2][0] = WidgetTypes.WIDGET_HELP_TECH_TRADE
				lAbilities[2][1] = i
			if ItemInfo.isGoldTrading():
				lAbilities[3][0] = WidgetTypes.WIDGET_HELP_GOLD_TRADE
				lAbilities[3][1] = i
			if ItemInfo.isOpenBordersTrading():
				lAbilities[4][0] = WidgetTypes.WIDGET_HELP_OPEN_BORDERS
				lAbilities[4][1] = i
			if ItemInfo.isDefensivePactTrading():
				lAbilities[5][0] = WidgetTypes.WIDGET_HELP_DEFENSIVE_PACT
				lAbilities[5][1] = i
			if ItemInfo.isPermanentAllianceTrading():
				lAbilities[6][0] = WidgetTypes.WIDGET_HELP_PERMANENT_ALLIANCE
				lAbilities[6][1] = i
			if ItemInfo.isVassalStateTrading():
				lAbilities[7][0] = WidgetTypes.WIDGET_HELP_VASSAL_STATE
				lAbilities[7][1] = i
			if ItemInfo.isBridgeBuilding():
				lAbilities[8][0] = WidgetTypes.WIDGET_HELP_BUILD_BRIDGE
				lAbilities[8][1] = i
			if ItemInfo.isIrrigation():
				lAbilities[9][0] = WidgetTypes.WIDGET_HELP_IRRIGATION
				lAbilities[9][1] = i
			if ItemInfo.isIgnoreIrrigation():
				lAbilities[10][0]= WidgetTypes.WIDGET_HELP_IGNORE_IRRIGATION
				lAbilities[10][1]= i
			if ItemInfo.isWaterWork():
				lAbilities[11][0] = WidgetTypes.WIDGET_HELP_WATER_WORK
				lAbilities[11][1] = i
			if ItemInfo.isExtraWaterSeeFrom():
				lAbilities[12][0] = WidgetTypes.WIDGET_HELP_LOS_BONUS
				lAbilities[12][1] = i

		self.placeStats()
		self.placeMembers()
		self.placeAbilities()
		self.placeImprovements()
		self.placeDomains()
		self.placeRoutes()
		self.placeVotes()

	def placeStats(self):
		screen = CyGInterfaceScreen("WBTeamScreen", CvScreenEnums.WB_TEAM)
		
		iY = self.iTable_Y
		screen.setButtonGFC("NukeInterceptionPlus", u"", "", 20, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("NukeInterceptionMinus", u"", "", 45, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = "<font=3>" + CyTranslator().getText("TXT_KEY_WB_NUKE_INTERCEPTION",(pTeam.getNukeInterception(),)) + "</font>"
		screen.setLabel("NukeInterceptionText", "Background", sText, CvUtil.FONT_LEFT_JUSTIFY, 75, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		screen.setButtonGFC("EnemyWWPlus", u"", "", 20, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("EnemyWWMinus", u"", "", 45, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = "<font=3>" + CyTranslator().getText("TXT_KEY_WB_ENEMY_WAR_WEARINESS",(pTeam.getEnemyWarWearinessModifier(),)) + "</font>"
		screen.setLabel("EnemyWWText", "Background", sText, CvUtil.FONT_LEFT_JUSTIFY, 75, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		screen.setButtonGFC("MasterPowerPlus", u"", "", 20, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("MasterPowerMinus", u"", "", 45, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = "<font=3>" + CyTranslator().getText("[ICON_STRENGTH]",()) + CyTranslator().getText("TXT_KEY_MISC_MASTER",()) + ": " + str(pTeam.getMasterPower()) + "</font>"
		screen.setLabel("MasterPowerText", "Background", sText, CvUtil.FONT_LEFT_JUSTIFY, 75, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		screen.setButtonGFC("VassalPowerPlus", u"", "", 20, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("VassalPowerMinus", u"", "", 45, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = "<font=3>" + CyTranslator().getText("[ICON_STRENGTH]",()) + CyTranslator().getText("TXT_KEY_MISC_VASSAL_SHORT",()) + ": " + str(pTeam.getVassalPower()) + "</font>"
		screen.setLabel("VassalPowerText", "Background", sText, CvUtil.FONT_LEFT_JUSTIFY, 75, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		screen.setButtonGFC("EspionageEverPlus", u"", "", 20, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("EspionageEverMinus", u"", "", 45, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = "<font=3>" + CyTranslator().getText("[ICON_ESPIONAGE]",()) + CyTranslator().getText("TXT_KEY_WB_EVER",()) + ": " + str(pTeam.getEspionagePointsEver()) + "</font>"
		screen.setLabel("EspionageEverText", "Background", sText, CvUtil.FONT_LEFT_JUSTIFY, 75, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def placeVotes(self):
		screen = CyGInterfaceScreen("WBTeamScreen", CvScreenEnums.WB_TEAM)
		iWidth = screen.getXResolution() /4 - 40
		iX = 20
		iY = self.iTable_Y + 180 + 13 * 24 + 2
		screen.setLabel("VoteHeader", "Background", "<font=3b>" + CyTranslator().getText("TXT_KEY_WB_GUARANTEED_ELIGIBILITY",()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, iX + iWidth/2, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iY += 30
		iHeight = (screen.getYResolution() - iY - 40) /24 * 24 + 2
		screen.addTableControlGFC("WBTeamVotes", 1, iX, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader( "WBTeamVotes", 0, "", iWidth)
		for item in lVoteBuildings:
			iVoteSource = gc.getBuildingInfo(item[1]).getVoteSourceType()
			iRow = screen.appendTableRow("WBTeamVotes")
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if pTeam.isForceTeamVoteEligible(iVoteSource):
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			screen.setTableText("WBTeamVotes", 0, iRow, "<font=3>" + sColor + item[0] + "</font></color>", gc.getBuildingInfo(item[1]).getButton(), WidgetTypes.WIDGET_HELP_BUILDING, item[1], -1, CvUtil.FONT_LEFT_JUSTIFY )
		
	def placeRoutes(self):
		screen = CyGInterfaceScreen("WBTeamScreen", CvScreenEnums.WB_TEAM)
		iWidth = screen.getXResolution() *3/8 - 20
		iX = screen.getXResolution()/4
		iY = screen.getYResolution()/2 + 30 + DomainTypes.NUM_DOMAIN_TYPES * 24 + 2
		sText = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_ROUTE",())
		screen.setLabel("RouteHeader", "Background", "<font=3b>" + CyTranslator().getText("TXT_KEY_WB_MODIFY", (sText,)) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, iX + iWidth/2, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iY += 30
		iHeight = (screen.getYResolution() - 40 - iY) /24 * 24 + 2
		screen.addTableControlGFC("WBTeamRoutes", 2, iX, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("WBTeamRoutes", 0, "", iWidth *2/3)
		screen.setTableColumnHeader("WBTeamRoutes", 1, "", iWidth /3)

		for item in lRoutes:
			iRow = screen.appendTableRow("WBTeamRoutes")
			Info = gc.getRouteInfo(item[1])
			screen.setTableText("WBTeamRoutes", 0, iRow, "<font=3>" + item[0] + "</font>", Info.getButton(), WidgetTypes.WIDGET_PYTHON, 6788, item[1], CvUtil.FONT_LEFT_JUSTIFY)
			iChange = pTeam.getRouteChange(item[1])
			if iChange != 0:
				sText = u"%+d%s %s" %(iChange, CyTranslator().getText("[ICON_MOVES]", ()), CyTranslator().getText("TXT_KEY_ESPIONAGE_SCREEN_COST", ()))
				screen.setTableInt("WBTeamRoutes", 1, iRow, "<font=3>" + sText + "</font>", "", WidgetTypes.WIDGET_PYTHON, 6788, item[1], CvUtil.FONT_RIGHT_JUSTIFY)
		
	def placeDomains(self):
		screen = CyGInterfaceScreen("WBTeamScreen", CvScreenEnums.WB_TEAM)
		iWidth = screen.getXResolution() *3/8 - 20
		iX = screen.getXResolution()/4
		iY = screen.getYResolution()/2
		sText = CyTranslator().getText("TXT_KEY_PEDIA_DOMAIN",())
		screen.setLabel("DomainHeader", "Background", "<font=3b>" + CyTranslator().getText("TXT_KEY_WB_MODIFY", (sText,)) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, iX + iWidth/2, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iY += 30
		screen.addTableControlGFC("WBTeamDomainMoves", 2, iX, iY, iWidth, DomainTypes.NUM_DOMAIN_TYPES * 24 + 2, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader("WBTeamDomainMoves", 0, "", iWidth/2)
		screen.setTableColumnHeader("WBTeamDomainMoves", 1, "", iWidth/2)
		for i in xrange(DomainTypes.NUM_DOMAIN_TYPES):
			Info = gc.getDomainInfo(i)
			screen.appendTableRow("WBTeamDomainMoves")
			screen.setTableText("WBTeamDomainMoves", 0, i, "<font=3>" + Info.getDescription() + "</font>", "", WidgetTypes.WIDGET_PYTHON, 1030, i, CvUtil.FONT_LEFT_JUSTIFY )
			iChange = pTeam.getExtraMoves(i)
			if iChange != 0:
				sText = u"%+d%s" %(iChange, CyTranslator().getText("[ICON_MOVES]", ()))
				screen.setTableInt("WBTeamDomainMoves", 1, i, "<font=3>" + sText + "</font>", "", WidgetTypes.WIDGET_PYTHON, 1030, i, CvUtil.FONT_RIGHT_JUSTIFY )
		
	def placeImprovements(self):
		screen = CyGInterfaceScreen("WBTeamScreen", CvScreenEnums.WB_TEAM)
		iWidth = screen.getXResolution() *3/8 - 20
		iX = screen.getXResolution() *5/8
		iY = self.iTable_Y - 30
		sText = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT",())
		screen.setLabel("ImprovementHeader", "Background", "<font=3b>" + CyTranslator().getText("TXT_KEY_WB_MODIFY", (sText,)) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, iX, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addDropDownBoxGFC("YieldType", iX + iWidth - 150, iY, 150, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i in xrange(YieldTypes.NUM_YIELD_TYPES):
			screen.addPullDownString("YieldType", gc.getYieldInfo(i).getDescription(), i, i, iSelectedYield == i)

		iY += 30
		iHeight = (screen.getYResolution() - 40 - iY) /24 * 24 + 2
		screen.addTableControlGFC("WBTeamYield", 2, iX, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader("WBTeamYield", 0, "", iWidth/2)
		screen.setTableColumnHeader("WBTeamYield", 1, "", iWidth/2)

		for item in lImprovements:
			Info = gc.getImprovementInfo(item[1])
			iRow = screen.appendTableRow("WBTeamYield")
			screen.setTableText("WBTeamYield", 0, iRow, "<font=3>" + item[0] + "</font>", Info.getButton(), WidgetTypes.WIDGET_PYTHON, 7877, item[1], CvUtil.FONT_LEFT_JUSTIFY )
			sText = ""
			for j in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = pTeam.getImprovementYieldChange(item[1], j)
				if iYieldChange != 0:
					sText += u"%d%c" %(iYieldChange, gc.getYieldInfo(j).getChar())
			screen.setTableInt("WBTeamYield", 1, iRow, "<font=3>" + sText + "</font>", "", WidgetTypes.WIDGET_PYTHON, 7877, item[1], CvUtil.FONT_LEFT_JUSTIFY)

	def placeMembers(self):
		screen = CyGInterfaceScreen("WBTeamScreen", CvScreenEnums.WB_TEAM)
		iWidth = screen.getXResolution() *3/8 - 20
		iHeight = (screen.getYResolution()/2 - self.iTable_Y) /24 * 24 + 2
		iX = screen.getXResolution()/4
		screen.setLabel("MemberHeader", "Background", "<font=3b>" + CyTranslator().getText("TXT_KEY_MEMBERS_TITLE",()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, iX + iWidth/2, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addTableControlGFC("WBTeamMembers", 2, iX, self.iTable_Y, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader("WBTeamMembers", 0, "", iWidth/2)
		screen.setTableColumnHeader("WBTeamMembers", 1, "", iWidth/2)
		lMembers = []
		for iPlayerX in xrange(gc.getMAX_PLAYERS()):
			pPlayerX = gc.getPlayer(iPlayerX)
			iTeamX = pPlayerX.getTeam()
			pTeamX = gc.getTeam(iTeamX)
			sText = CyTranslator().getText("[ICON_ANGRYPOP]", ())
			fType = 1
			if iTeamX == iTeam:
				if pTeamX.getLeaderID() == iPlayerX:
					sText = CyTranslator().getText("[ICON_STAR]", ())
					fType = 0
			elif pTeamX.isVassal(iTeam):
				sText = CyTranslator().getText("[ICON_SILVER_STAR]", ())
				fType = 2
			else:
				continue
			if not pPlayerX.isAlive():
				sText += "*"
				fType += 0.5
			sText += pPlayerX.getName()
			if pPlayerX.isTurnActive():
				sText = "[" + sText + "]"
			sColor = u"<color=%d,%d,%d,%d>" %(pPlayerX.getPlayerTextColorR(), pPlayerX.getPlayerTextColorG(), pPlayerX.getPlayerTextColorB(), pPlayerX.getPlayerTextColorA())
			sText = "<font=3>" + sColor + sText + "</font></color>"
			sCiv = "<font=3>" + sColor + pPlayerX.getCivilizationShortDescription(0) + "</font></color>"
			lMembers.append([fType, sText, iPlayerX, pPlayerX.getCivilizationType(), pPlayerX.getLeaderType(), sCiv])
		lMembers.sort()
		for item in lMembers:
			iRow = screen.appendTableRow("WBTeamMembers")
			screen.setTableText("WBTeamMembers", 0, iRow, item[5], gc.getCivilizationInfo(item[3]).getButton(), WidgetTypes.WIDGET_PYTHON, 7872, item[2] * 10000 + item[3], CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("WBTeamMembers", 1, iRow, item[1], gc.getLeaderHeadInfo(item[4]).getButton(), WidgetTypes.WIDGET_PYTHON, 7876, item[2] * 10000 + item[4], CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeAbilities(self):
		screen = CyGInterfaceScreen("WBTeamScreen", CvScreenEnums.WB_TEAM)
		iWidth = screen.getXResolution() /4 - 40
		iX = 20
		iY = self.iTable_Y + 150
		sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + " (+/-)</color></font>"
		screen.setText("AbilitiesAll", "Background", sText, CvUtil.FONT_RIGHT_JUSTIFY, iX + iWidth, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		iY += 30
		screen.addTableControlGFC("WBAbilities", 1, iX, iY, iWidth, 13 * 24 + 2, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader( "WBAbilities", 0, "", iWidth)
	
		iRow = screen.appendTableRow("WBAbilities")
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if pTeam.isMapCentering():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setTableText("WBAbilities", 0, iRow, "<font=3>" + sColor + CyTranslator().getText("TXT_KEY_WB_MAP_CENTERING",()) + "</font></color>", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MAPCENTER").getPath(), lAbilities[0][0], lAbilities[0][1], -1, CvUtil.FONT_LEFT_JUSTIFY )

		iRow = screen.appendTableRow("WBAbilities")
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if pTeam.isMapTrading():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setTableText("WBAbilities", 0, iRow, "<font=3>" + sColor + CyTranslator().getText("TXT_KEY_WB_MAP_TRADING",()) + "</font></color>", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MAPTRADING").getPath(), lAbilities[1][0], lAbilities[1][1], -1, CvUtil.FONT_LEFT_JUSTIFY )

		iRow = screen.appendTableRow("WBAbilities")
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if pTeam.isTechTrading():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setTableText("WBAbilities", 0, iRow, "<font=3>" + sColor + CyTranslator().getText("TXT_KEY_WB_TECH_TRADING",()) + "</font></color>", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_TECHTRADING").getPath(), lAbilities[2][0], lAbilities[2][1], -1, CvUtil.FONT_LEFT_JUSTIFY )

		iRow = screen.appendTableRow("WBAbilities")
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if pTeam.isGoldTrading():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setTableText("WBAbilities", 0, iRow, "<font=3>" + sColor + CyTranslator().getText("TXT_KEY_WB_GOLD_TRADING",()) + "</font></color>", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_GOLDTRADING").getPath(), lAbilities[3][0], lAbilities[3][1], -1, CvUtil.FONT_LEFT_JUSTIFY )

		iRow = screen.appendTableRow("WBAbilities")
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if pTeam.isOpenBordersTrading():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setTableText("WBAbilities", 0, iRow, "<font=3>" + sColor + CyTranslator().getText("TXT_KEY_MISC_OPEN_BORDERS",()) + "</font></color>", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_OPENBORDERS").getPath(), lAbilities[4][0], lAbilities[4][1], -1, CvUtil.FONT_LEFT_JUSTIFY )

		iRow = screen.appendTableRow("WBAbilities")
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if pTeam.isDefensivePactTrading():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setTableText("WBAbilities", 0, iRow, "<font=3>" + sColor + CyTranslator().getText("TXT_KEY_MISC_DEFENSIVE_PACT",()) + "</font></color>", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_DEFENSIVEPACT").getPath(), lAbilities[5][0], lAbilities[5][1], -1, CvUtil.FONT_LEFT_JUSTIFY )

		iRow = screen.appendTableRow("WBAbilities")
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if pTeam.isPermanentAllianceTrading():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setTableText("WBAbilities", 0, iRow, "<font=3>" + sColor + CyTranslator().getText("TXT_KEY_MISC_PERMANENT_ALLIANCE",()) + "</font></color>", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_PERMALLIANCE").getPath(), lAbilities[6][0], lAbilities[6][1], -1, CvUtil.FONT_LEFT_JUSTIFY )

		iRow = screen.appendTableRow("WBAbilities")
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if pTeam.isVassalStateTrading():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setTableText("WBAbilities", 0, iRow, "<font=3>" + sColor + CyTranslator().getText("TXT_KEY_WB_VASSAL_TRADING",()) + "</font></color>", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_VASSAL").getPath(), lAbilities[7][0], lAbilities[7][1], -1, CvUtil.FONT_LEFT_JUSTIFY )

		iRow = screen.appendTableRow("WBAbilities")
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if pTeam.isBridgeBuilding():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setTableText("WBAbilities", 0, iRow, "<font=3>" + sColor + CyTranslator().getText("TXT_KEY_WB_BRIDGE_BUILDING",()) + "</font></color>", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_BRIDGEBUILDING").getPath(), lAbilities[8][0], lAbilities[8][1], -1, CvUtil.FONT_LEFT_JUSTIFY )

		iRow = screen.appendTableRow("WBAbilities")
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if pTeam.isIrrigation():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setTableText("WBAbilities", 0, iRow, "<font=3>" + sColor + CyTranslator().getText("TXT_KEY_CONCEPT_IRRIGATION",()) + "</font></color>", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_IRRIGATION").getPath(), lAbilities[9][0], lAbilities[9][1], -1, CvUtil.FONT_LEFT_JUSTIFY )

		iRow = screen.appendTableRow("WBAbilities")
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if pTeam.isIgnoreIrrigation():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setTableText("WBAbilities", 0, iRow, "<font=3>" + sColor + CyTranslator().getText("TXT_KEY_WB_IGNORE_IRRIGATION",()) + "</font></color>", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_NOIRRIGATION").getPath(), lAbilities[10][0], lAbilities[10][1], -1, CvUtil.FONT_LEFT_JUSTIFY )

		iRow = screen.appendTableRow("WBAbilities")
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if pTeam.isWaterWork():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setTableText("WBAbilities", 0, iRow, "<font=3>" + sColor + CyTranslator().getText("TXT_KEY_WB_WATER_WORK",()) + "</font></color>", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_WATERWORK").getPath(), lAbilities[11][0], lAbilities[11][1], -1, CvUtil.FONT_LEFT_JUSTIFY )

		iRow = screen.appendTableRow("WBAbilities")
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if pTeam.isExtraWaterSeeFrom():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setTableText("WBAbilities", 0, iRow, "<font=3>" + sColor + CyTranslator().getText("TXT_KEY_WB_EXTRA_WATER_SIGHT",()) + "</font></color>", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_LOS").getPath(), lAbilities[12][0], lAbilities[12][1], -1, CvUtil.FONT_LEFT_JUSTIFY )
	
	def handleInput (self, inputClass):
		screen = CyGInterfaceScreen("WBTeamScreen", CvScreenEnums.WB_TEAM)
		global iChange
		global bRemove
		global iSelectedYield

		if inputClass.getFunctionName() == "ChangeBy":
			if bRemove:
				iChange = -screen.getPullDownData("ChangeBy", screen.getSelectedPullDownID("ChangeBy"))
			else:
				iChange = screen.getPullDownData("ChangeBy", screen.getSelectedPullDownID("ChangeBy"))

		elif inputClass.getFunctionName() == "ChangeType":
			bRemove = not bRemove
			iChange = -iChange

		elif inputClass.getFunctionName() == "CurrentPage":
			iIndex = screen.getPullDownData("CurrentPage", screen.getSelectedPullDownID("CurrentPage"))
			if iIndex == 0:
				WBPlayerScreen.WBPlayerScreen().interfaceScreen(pTeam.getLeaderID())
			elif iIndex == 2:
				WBProjectScreen.WBProjectScreen().interfaceScreen(iTeam)
			elif iIndex == 3:
				WBTechScreen.WBTechScreen().interfaceScreen(iTeam)
			elif iIndex == 4:
				WBPlayerUnits.WBPlayerUnits().interfaceScreen(pTeam.getLeaderID())
			elif iIndex == 11:
				WBInfoScreen.WBInfoScreen().interfaceScreen(pTeam.getLeaderID())

		elif inputClass.getFunctionName() == "CurrentTeam":
			iTeamX = screen.getPullDownData("CurrentTeam", screen.getSelectedPullDownID("CurrentTeam"))
			self.interfaceScreen(iTeamX)

		elif inputClass.getFunctionName() == "WBTeamMembers":
			if inputClass.getData1() == 7876 or inputClass.getData1() == 7872:
				iPlayer = inputClass.getData2() /10000
				WBPlayerScreen.WBPlayerScreen().interfaceScreen(iPlayer)

		elif inputClass.getFunctionName() == "MergeTeam":
			pTeam.addTeam(screen.getPullDownData("MergeTeam", screen.getSelectedPullDownID("MergeTeam")))
			self.interfaceScreen(pTeam.getID())
			dc.checkName(iPlayer)

		elif inputClass.getFunctionName().find("NukeInterception") > -1:
			if inputClass.getData1() == 1030:
				pTeam.changeNukeInterception(min(abs(iChange), 100 - pTeam.getNukeInterception()))
			elif inputClass.getData1() == 1031:
				iCount = min(abs(iChange), pTeam.getNukeInterception())
				pTeam.changeNukeInterception(-iCount)
			self.placeStats()

		elif inputClass.getFunctionName().find("EnemyWW") > -1:
			if inputClass.getData1() == 1030:
				pTeam.changeEnemyWarWearinessModifier(abs(iChange))
			elif inputClass.getData1() == 1031:
				iCount = min(abs(iChange), pTeam.getEnemyWarWearinessModifier())
				pTeam.changeEnemyWarWearinessModifier(-iCount)
			self.placeStats()

		elif inputClass.getFunctionName().find("MasterPower") > -1:
			if inputClass.getData1() == 1030:
				pTeam.setMasterPower(pTeam.getMasterPower() + abs(iChange))
			elif inputClass.getData1() == 1031:
				pTeam.setMasterPower(max(0, pTeam.getMasterPower() - abs(iChange)))
			self.placeStats()

		elif inputClass.getFunctionName().find("VassalPower") > -1:
			if inputClass.getData1() == 1030:
				pTeam.setVassalPower(pTeam.getVassalPower() + abs(iChange))
			elif inputClass.getData1() == 1031:
				pTeam.setVassalPower(max(0, pTeam.getVassalPower() - abs(iChange)))
			self.placeStats()

		elif inputClass.getFunctionName().find("EspionageEver") > -1:
			if inputClass.getData1() == 1030:
				pTeam.changeEspionagePointsEver(abs(iChange))
			elif inputClass.getData1() == 1031:
				iCount = min(abs(iChange), pTeam.getEspionagePointsEver())
				pTeam.changeEspionagePointsEver(-iCount)
			self.placeStats()

		elif inputClass.getFunctionName() == "WBTeamRoutes":
			self.editRoute(inputClass.getData2())
			self.placeRoutes()

		elif inputClass.getFunctionName() == "WBTeamDomainMoves":
			self.editDomain(inputClass.getData2())
			self.placeDomains()

		elif inputClass.getFunctionName() == "YieldType":
			iSelectedYield = screen.getPullDownData("YieldType", screen.getSelectedPullDownID("YieldType"))

		elif inputClass.getFunctionName() == "WBTeamYield":
			self.modifyImprovement(inputClass.getData2())
			self.placeImprovements()

		elif inputClass.getFunctionName() == "WBTeamVotes":
			iVote = gc.getBuildingInfo(inputClass.getData1()).getVoteSourceType()
			if pTeam.isForceTeamVoteEligible(iVote):
				pTeam.changeForceTeamVoteEligibilityCount(iVote, - pTeam.getForceTeamVoteEligibilityCount(iVote))
			else:
				pTeam.changeForceTeamVoteEligibilityCount(iVote, 1)
			self.placeVotes()

		elif inputClass.getFunctionName() == "AbilitiesAll":
			for i in xrange(13):
				self.doTeamAbilities(i, not bRemove)
			self.placeAbilities()

		elif inputClass.getFunctionName() == "WBAbilities":
			iButton = inputClass.getButtonType()
			if iButton == WidgetTypes.WIDGET_HELP_MAP_CENTER:
				self.doTeamAbilities(0, -1)
			elif iButton == WidgetTypes.WIDGET_HELP_MAP_TRADE:
				self.doTeamAbilities(1, -1)
			elif iButton == WidgetTypes.WIDGET_HELP_TECH_TRADE:
				self.doTeamAbilities(2, -1)
			elif iButton == WidgetTypes.WIDGET_HELP_GOLD_TRADE:
				self.doTeamAbilities(3, -1)
			elif iButton == WidgetTypes.WIDGET_HELP_OPEN_BORDERS:
				self.doTeamAbilities(4, -1)
			elif iButton == WidgetTypes.WIDGET_HELP_DEFENSIVE_PACT:
				self.doTeamAbilities(5, -1)
			elif iButton == WidgetTypes.WIDGET_HELP_PERMANENT_ALLIANCE:
				self.doTeamAbilities(6, -1)
			elif iButton == WidgetTypes.WIDGET_HELP_VASSAL_STATE:
				self.doTeamAbilities(7, -1)
			elif iButton == WidgetTypes.WIDGET_HELP_BUILD_BRIDGE:
				self.doTeamAbilities(8, -1)
			elif iButton == WidgetTypes.WIDGET_HELP_IRRIGATION:
				self.doTeamAbilities(9, -1)
			elif iButton == WidgetTypes.WIDGET_HELP_IGNORE_IRRIGATION:
				self.doTeamAbilities(10, -1)
			elif iButton == WidgetTypes.WIDGET_HELP_WATER_WORK:
				self.doTeamAbilities(11, -1)
			elif iButton == WidgetTypes.WIDGET_HELP_LOS_BONUS:
				self.doTeamAbilities(12, -1)
			else:
				self.doTeamAbilities(inputClass.getData(), -1)
			self.placeAbilities()
		return 1

	def editDomain(self, item):
		pTeam.changeExtraMoves(item, iChange)

	def editRoute(self, item):
		pTeam.changeRouteChange(item, iChange)

	def modifyImprovement(self, item):
		pTeam.changeImprovementYieldChange(item, iSelectedYield, iChange)

	def doTeamAbilities(self, i, iType):
		if i == 0:
			if iType == -1:
				pTeam.setMapCentering(not pTeam.isMapCentering())
			else:
				pTeam.setMapCentering(iType)
		elif i == 1:
			if pTeam.isMapTrading():
				if iType !=1:
					pTeam.changeMapTradingCount( - pTeam.getMapTradingCount())
			elif iType != 0:
				pTeam.changeMapTradingCount(1)
		elif i == 2:
			if pTeam.isTechTrading():
				if iType !=1:
					pTeam.changeTechTradingCount( - pTeam.getTechTradingCount())
			elif iType != 0:
				pTeam.changeTechTradingCount(1)
		elif i == 3:
			if pTeam.isGoldTrading():
				if iType !=1:
					pTeam.changeGoldTradingCount( - pTeam.getGoldTradingCount())
			elif iType != 0:
				pTeam.changeGoldTradingCount(1)
		elif i == 4:
			if pTeam.isOpenBordersTrading():
				if iType !=1:
					pTeam.changeOpenBordersTradingCount( - pTeam.getOpenBordersTradingCount())
			elif iType != 0:
				pTeam.changeOpenBordersTradingCount(1)
		elif i == 5:
			if pTeam.isDefensivePactTrading():
				if iType !=1:
					pTeam.changeDefensivePactTradingCount( - pTeam.getDefensivePactTradingCount())
			elif iType != 0:
				pTeam.changeDefensivePactTradingCount(1)
		elif i == 6:
			if pTeam.isPermanentAllianceTrading():
				if iType !=1:
					pTeam.changePermanentAllianceTradingCount( - pTeam.getPermanentAllianceTradingCount())
			elif iType != 0:
				pTeam.changePermanentAllianceTradingCount(1)
		elif i == 7:
			if pTeam.isVassalStateTrading():
				if iType !=1:
					pTeam.changeVassalTradingCount( - pTeam.getVassalTradingCount())
			elif iType != 0:
				pTeam.changeVassalTradingCount(1)
		elif i == 8:
			if pTeam.isBridgeBuilding():
				if iType !=1:
					pTeam.changeBridgeBuildingCount( - pTeam.getBridgeBuildingCount())
			elif iType != 0:
				pTeam.changeBridgeBuildingCount(1)
		elif i == 9:
			if pTeam.isIrrigation():
				if iType !=1:
					pTeam.changeIrrigationCount( - pTeam.getIrrigationCount())
			elif iType != 0:
				pTeam.changeIrrigationCount(1)
		elif i == 10:
			if pTeam.isIgnoreIrrigation():
				if iType !=1:
					pTeam.changeIgnoreIrrigationCount( - pTeam.getIgnoreIrrigationCount())
			elif iType != 0:
				pTeam.changeIgnoreIrrigationCount(1)
		elif i == 11:
			if pTeam.isWaterWork():
				if iType !=1:
					pTeam.changeWaterWorkCount( - pTeam.getWaterWorkCount())
			elif iType != 0:
				pTeam.changeWaterWorkCount(1)
		elif i == 12:
			if pTeam.isExtraWaterSeeFrom():
				if iType !=1:
					pTeam.changeExtraWaterSeeFromCount( - pTeam.getExtraWaterSeeFromCount())
			elif iType != 0:
				pTeam.changeExtraWaterSeeFromCount(1)
	def update(self, fDelta):
		return 1