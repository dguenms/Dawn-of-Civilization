from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import WBPromotionScreen
import WBPlayerScreen
import WBTeamScreen
import WBPlotScreen
import WBEventScreen
import WBPlayerUnits
import CvPlatyBuilderScreen
import WBInfoScreen
import Popup
gc = CyGlobalContext()

bRemove = False
iChange = 1
iCopyType = 0
iOwnerType = 0
iPlotType = 0
iChangeType = 0
iCommandUnitType = 0
iSelectedClass = -2
iMissionType = 0
iMissionData1 = -1
bCargo = True
bUnitType = True

class WBUnitScreen:

	def __init__(self, main):
		self.top = main
		self.iTable_Y = 110
		self.iScriptH = 90
		self.lSelectableMissions = {	"MISSION_SPREAD":		[gc.getReligionInfo, 7869],
						"MISSION_SPREAD_CORPORATION":	[gc.getCorporationInfo, 6782],
						"MISSION_JOIN":			[gc.getSpecialistInfo, 7879],
						"MISSION_CONSTRUCT":		[gc.getBuildingInfo, 7870],
						"MISSION_BUILD":		[gc.getBuildInfo, 7882]}

	def interfaceScreen(self, pUnitX):
		screen = CyGInterfaceScreen( "WBUnitScreen", CvScreenEnums.WB_UNIT)
		
		global pUnit
		global pPlot

		pUnit = pUnitX
		pPlot = pUnit.plot()
		iWidth = screen.getXResolution()/5 - 20

		if self.top.iTargetPlotX == -1 or self.top.iTargetPlotY == -1:
			self.top.iTargetPlotX = pPlot.getX()
			self.top.iTargetPlotY = pPlot.getY()
		
		screen.setRenderInterfaceOnly(True)
		screen.addPanel( "MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.setText("UnitExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		
		screen.addDropDownBoxGFC("OwnerType", 20, self.iTable_Y - 90, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("OwnerType", CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()), 0, 0, 0 == iOwnerType)
		screen.addPullDownString("OwnerType", CyTranslator().getText("TXT_KEY_PITBOSS_TEAM", ()), 2, 2, 2 == iOwnerType)
		screen.addPullDownString("OwnerType", CyTranslator().getText("TXT_KEY_MAIN_MENU_PLAYER", ()), 1, 1, 1 == iOwnerType)

		screen.addDropDownBoxGFC("CopyType", 20, self.iTable_Y - 60, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CopyType", CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()), 0, 0, 0 == iCopyType)
		screen.addPullDownString("CopyType", CyTranslator().getText("TXT_KEY_SPACE_SHIP_SCREEN_TYPE_BUTTON", ()), 1, 1, 1 == iCopyType)
		screen.addPullDownString("CopyType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT_COMBAT", ()), 2, 2, 2 == iCopyType)
		screen.addPullDownString("CopyType", CyTranslator().getText("TXT_KEY_PEDIA_DOMAIN", ()), 3, 3, 3 == iCopyType)
		screen.addPullDownString("CopyType", CyTranslator().getText("TXT_KEY_WB_GROUP", ()), 4, 4, 4 == iCopyType)

		screen.addDropDownBoxGFC("PlotType", 20, self.iTable_Y - 30, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlotType", CyTranslator().getText("TXT_KEY_WB_SINGLE_PLOT", ()), 0, 0, iPlotType == 0)
		screen.addPullDownString("PlotType", CyTranslator().getText("TXT_KEY_WB_AREA_PLOTS", ()), 1, 1, iPlotType == 1)
		screen.addPullDownString("PlotType", CyTranslator().getText("TXT_KEY_WB_ALL_PLOTS", ()), 2, 2, iPlotType == 2)

		screen.addDropDownBoxGFC("CurrentPage", 20, screen.getYResolution() - 42, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_UNIT_DATA", ()), 0, 0, True)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ()), 1, 1, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA", ()), 2, 2, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_TEAM_DATA", ()), 3, 3, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLOT_DATA", ()), 4, 4, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_CONCEPT_EVENTS", ()), 5, 5, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()) + " + " + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()), 6, 6, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_INFO_SCREEN", ()), 11, 11, False)

		iX = screen.getXResolution()/5 + 20
		screen.addDropDownBoxGFC("ChangeType", iX, screen.getYResolution() - 42, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_XLEVEL", ()), 0, 0, 0 == iChangeType)
		screen.addPullDownString("ChangeType", CyTranslator().getText("INTERFACE_PANE_EXPERIENCE", ()), 1, 1, 1 == iChangeType)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_DEMO_SCREEN_STRENGTH_TEXT", ()), 2, 2, 2 == iChangeType)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_DAMAGE", ()), 3, 3, 3 == iChangeType)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_MOVES", ()), 4, 4, 4 == iChangeType)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_IMMOBILE_TIMER", ()), 5, 5, 5 == iChangeType)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_PROMOTION_READY", ()), 6, 6, 6 == iChangeType)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_MADE_ATTACK", ()), 7, 7, 7 == iChangeType)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_MADE_INTERCEPT", ()), 8, 8, 8 == iChangeType)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_DIRECTION", ()), 9, 9, 9 == iChangeType)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_UNIT_AI", ()), 10, 10, 10 == iChangeType)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CARGO_SPACE", ()), 11, 11, 11 == iChangeType)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_SCRIPT_DATA", ()), 12, 12, 12 == iChangeType)

		iX += iWidth
		sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=3b>" + CyTranslator().getText("TXT_KEY_WB_COPY_ALL", (CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()),)) + "</color></font>"
		screen.setText("CopyStats", "Background", sText, CvUtil.FONT_LEFT_JUSTIFY, iX, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		sText = u"<font=3b>" + CyTranslator().getText("TXT_KEY_PEDIA_HIDE_INACTIVE", ()) + "</font>"
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if CvPlatyBuilderScreen.bHideInactive:
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setText("HideInactive", "Background", sColor + sText + "</color>", CvUtil.FONT_LEFT_JUSTIFY, screen.getXResolution() * 4/5, self.iTable_Y - 85, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		global lUnitAI
		lUnitAI = []
		for i in xrange(UnitAITypes.NUM_UNITAI_TYPES):
			sText = gc.getUnitAIInfo(i).getDescription()
			sList = ""
			while len(sText):
				sText = sText[sText.find("_") +1:]
				sText = sText.lower()
				sText = sText.capitalize()
				if sText.find("_") == -1:
					sList += sText
					break
				else:
					sList += sText[:sText.find("_")] + " "
					sText = sText[sText.find("_") +1:]
			lUnitAI.append([sList, i])
		lUnitAI.sort()

		self.placeStats()
		self.placeDirection()
		self.sortUnits()
		self.placeUnitType()
		self.placeCargo()
		self.placeScript()

	def placeMap(self):
		screen = CyGInterfaceScreen("WBUnitScreen", CvScreenEnums.WB_UNIT)
		iWidth = screen.getXResolution()/5 - 40
		iY = self.iTable_Y
		iMapHeight = min((screen.getYResolution()/2 - self.iScriptH - 35 - iY), iWidth * 2/3)
		iMapWidth = iMapHeight * 3/2
		screen.addPlotGraphicGFC("PlotView", screen.getXResolution()/2 - iMapWidth/2, iY, iMapWidth, iMapHeight, pUnit.plot(), 250, True, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def placeMissions(self):
		screen = CyGInterfaceScreen("WBUnitScreen", CvScreenEnums.WB_UNIT)
		iX = screen.getXResolution() *3/5
		iY = self.iTable_Y
		iWidth = screen.getXResolution()/5 - 20
		global iMissionType
		global iMissionData1

		screen.setText("PushMission", "Background", "<font=3b>" + CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + CyTranslator().getText("TXT_KEY_WB_PUSH_MISSION", ()) + "</color></font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() *7/10, iY - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		sText = (CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=3>" + CyTranslator().getText("TXT_KEY_WB_TARGET_PLOT", ()) + ": " + "(%d,%d)" + "</color></font>") % (self.top.iTargetPlotX, self.top.iTargetPlotY)
		screen.setText("TargetPlot", "Background", sText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() *7/10, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		iY += 30
		screen.addDropDownBoxGFC("Missions", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		UnitInfo = gc.getUnitInfo(pUnit.getUnitType())
		lMissionData = []
		iFirstMission = -1
		bResetMission = False
		for i in xrange(gc.getNumMissionInfos()):
			MissionInfo = gc.getMissionInfo(i)
			sType = MissionInfo.getType()
			lData1 = []
			iData2 = -1

			if sType == "MISSION_MOVE_TO_UNIT": continue
			elif sType == "MISSION_BUILD":
				for j in xrange(gc.getNumBuildInfos()):
					if UnitInfo.getBuilds(j):
						lData1.append(j)
			elif sType == "MISSION_SPREAD":
				for j in xrange(gc.getNumReligionInfos()):
					if UnitInfo.getReligionSpreads(j) > 0:
						lData1.append(j)
			elif sType == "MISSION_SPREAD_CORPORATION":
				for j in xrange(gc.getNumCorporationInfos()):
					if UnitInfo.getCorporationSpreads(j) > 0:
						lData1.append(j)
			elif sType == "MISSION_JOIN":
				for j in xrange(gc.getNumSpecialistInfos()):
					if UnitInfo.getGreatPeoples(j):
						lData1.append(j)
			elif sType == "MISSION_CONSTRUCT":
				for j in xrange(gc.getNumBuildingInfos()):
					if UnitInfo.getBuildings(j) or UnitInfo.getForceBuildings(j):
						lData1.append(j)
			elif sType == "MISSION_GOLDEN_AGE":
				lData1 = [-1]
			else:
				lData1 = [self.top.iTargetPlotX]
				iData2 = self.top.iTargetPlotY
				pTargetPlot = CyMap().plot(lData1[0], iData2)
				if pTargetPlot.isNone():
					lData1 = [pPlot.getX()]
					iData2 = pPlot.getY()
			bCanDoMission = False
			for iData1 in lData1:
				if pUnit.getGroup().canStartMission(i, iData1, iData2, pPlot, True):
					screen.addPullDownString("Missions", MissionInfo.getDescription(), i, i, i == iMissionType)
					bCanDoMission = True
					if iFirstMission == -1:
						iFirstMission = i
					break
			if iMissionType == i:
				lMissionData = lData1
				if not bCanDoMission:
					bResetMission = True
		if bResetMission:
			iMissionType = max(0, iFirstMission)

		iY += 30
		iHeight = (screen.getYResolution()/2 - iY) /24 * 24 + 2
		screen.addTableControlGFC("MissionInput", 1, iX, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("MissionInput", 0, "", iWidth)

		sMissionType = gc.getMissionInfo(iMissionType).getType()
		screen.hide("MissionInput")
		if sMissionType in self.lSelectableMissions:
			screen.show("MissionInput")
			for i in xrange(len(lMissionData)):
				iData1 = lMissionData[i]
				if iMissionData1 not in lMissionData:
					iMissionData1 = iData1
				if pUnit.getGroup().canStartMission(iMissionType, iData1, -1, pPlot, True):
					ItemInfo = self.lSelectableMissions[sMissionType][0](iData1)
					sDescription = ItemInfo.getDescription()
					if sMissionType == "MISSION_BUILD":
						sText = ItemInfo.getType()
						sDescription = ""
						while len(sText):
							sText = sText[sText.find("_") +1:]
							sText = sText.lower()
							sText = sText.capitalize()
							if sText.find("_") == -1:
								sDescription += sText
								break
							else:
								sDescription += sText[:sText.find("_")] + " "
								sText = sText[sText.find("_") +1:]
					iRow = screen.appendTableRow("MissionInput")
					sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
					if iData1 == iMissionData1:
						sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
					screen.setTableText("MissionInput", 0, iRow, "<font=3>" + sColor + sDescription + "</font></color>", ItemInfo.getButton(), WidgetTypes.WIDGET_PYTHON, self.lSelectableMissions[sMissionType][1], iData1, CvUtil.FONT_LEFT_JUSTIFY)

		elif sMissionType == "MISSION_DISCOVER":
			screen.show("MissionInput")
			iTech = pUnit.getDiscoveryTech()
			if iTech > -1:
				iRow = screen.appendTableRow("MissionInput")
				screen.setTableText("MissionInput", 0, iRow, "<font=3>" + gc.getTechInfo(iTech).getDescription() + "</font>", gc.getTechInfo(iTech).getButton(), WidgetTypes.WIDGET_PYTHON, 7871, iTech, CvUtil.FONT_LEFT_JUSTIFY)
				iRow = screen.appendTableRow("MissionInput")
				sText = u"%c %d / %d" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar(), gc.getTeam(pUnit.getTeam()).getResearchProgress(iTech), gc.getTeam(pUnit.getTeam()).getResearchCost(iTech))
				screen.setTableText("MissionInput", 0, iRow, "<font=3>" + sText + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow = screen.appendTableRow("MissionInput")
				sText = u"%c %s%+d</color>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar(), CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ()), pUnit.getDiscoverResearch(iTech))
				screen.setTableText("MissionInput", 0, iRow, "<font=3>" + sText + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		elif sMissionType == "MISSION_GREAT_WORK":
			screen.show("MissionInput")
			if pPlot.isCity():
				pCity = pPlot.getPlotCity()
				sText = u"%s: %d/%d%c" %(gc.getCultureLevelInfo(pCity.getCultureLevel()).getDescription(), pCity.getCulture(pCity.getOwner()), pCity.getCultureThreshold(), gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar())
				iRow = screen.appendTableRow("MissionInput")
				sText = u"%c %s" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), gc.getCultureLevelInfo(pCity.getCultureLevel()).getDescription())
				screen.setTableText("MissionInput", 0, iRow, "<font=3>" + sText + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow = screen.appendTableRow("MissionInput")
				sText = u"%c %d / %d" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), pCity.getCulture(pCity.getOwner()), pCity.getCultureThreshold())
				screen.setTableText("MissionInput", 0, iRow, "<font=3>" + sText + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow = screen.appendTableRow("MissionInput")
				sText = u"%c %s%+d</color>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ()), pUnit.getGreatWorkCulture(pPlot))
				screen.setTableText("MissionInput", 0, iRow, "<font=3>" + sText + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		elif sMissionType == "MISSION_HURRY":
			screen.show("MissionInput")
			if pPlot.isCity():
				pCity = pPlot.getPlotCity()
				iRow = screen.appendTableRow("MissionInput")
				if pCity.isProductionBuilding():
					iBuilding = pCity.getProductionBuilding()
					screen.setTableText("MissionInput", 0, iRow, "<font=3>" + gc.getBuildingInfo(iBuilding).getDescription() + "</font>", gc.getBuildingInfo(iBuilding).getButton(), WidgetTypes.WIDGET_PYTHON, 7870, iBuilding, CvUtil.FONT_LEFT_JUSTIFY)
				elif pCity.isProductionProject():
					iProject = pCity.getProductionProject()
					screen.setTableText("MissionInput", 0, iRow, "<font=3>" + gc.getProjectInfo(iProject).getDescription() + "</font>", gc.getProjectInfo(iProject).getButton(), WidgetTypes.WIDGET_PYTHON, 6785, iProject, CvUtil.FONT_LEFT_JUSTIFY)
				elif pCity.isProductionUnit():
					iUnit = pCity.getProductionUnit()
					screen.setTableText("MissionInput", 0, iRow, "<font=3>" + gc.getUnitInfo(iUnit).getDescription() + "</font>", gc.getUnitInfo(iUnit).getButton(), WidgetTypes.WIDGET_PYTHON, 8202, iUnit, CvUtil.FONT_LEFT_JUSTIFY)
				iRow = screen.appendTableRow("MissionInput")
				sText = u"%c %d / %d" %(gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar(), pCity.getProduction(), pCity.getProductionNeeded())
				screen.setTableText("MissionInput", 0, iRow, "<font=3>" + sText + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow = screen.appendTableRow("MissionInput")
				sText = u"%c %s%+d</color>" %(gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar(), CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ()), pUnit.getHurryProduction(pPlot))
				screen.setTableText("MissionInput", 0, iRow, "<font=3>" + sText + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeDirection(self):
		screen = CyGInterfaceScreen("WBUnitScreen", CvScreenEnums.WB_UNIT)
		iY = screen.getYResolution()/2
		screen.setLabel("UnitDirectionText", "Background", "<font=3b>" + CyTranslator().getText("TXT_KEY_WB_DIRECTION", ()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		iHeight = 3*24 + 2
		screen.addTableControlGFC("WBUnitDirection", 3, screen.getXResolution()/2 - iHeight/2, iY, iHeight, iHeight, False, True, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
		for i in xrange(3):
			screen.setTableColumnHeader("WBUnitDirection", i, "", iHeight/3)
			screen.appendTableRow("WBUnitDirection")
		screen.setTableText("WBUnitDirection", 1,0 , " ", "", WidgetTypes.WIDGET_PYTHON, 1030, 0, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText("WBUnitDirection", 2,0 , " ", "", WidgetTypes.WIDGET_PYTHON, 1030, 1, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText("WBUnitDirection", 2,1 , " ", "", WidgetTypes.WIDGET_PYTHON, 1030, 2, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText("WBUnitDirection", 2,2 , " ", "", WidgetTypes.WIDGET_PYTHON, 1030, 3, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText("WBUnitDirection", 1,2 , " ", "", WidgetTypes.WIDGET_PYTHON, 1030, 4, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText("WBUnitDirection", 0,2 , " ", "", WidgetTypes.WIDGET_PYTHON, 1030, 5, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText("WBUnitDirection", 0,1 , " ", "", WidgetTypes.WIDGET_PYTHON, 1030, 6, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText("WBUnitDirection", 0,0 , " ", "", WidgetTypes.WIDGET_PYTHON, 1030, 7, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText("WBUnitDirection", 1,1 , " ", "", WidgetTypes.WIDGET_PYTHON, 1030, -1, CvUtil.FONT_CENTER_JUSTIFY)

		if pUnit.getFacingDirection() == DirectionTypes.DIRECTION_NORTH:
			screen.setTableText("WBUnitDirection", 1,0 , "", pUnit.getButton(), WidgetTypes.WIDGET_PYTHON, 1030, 0, CvUtil.FONT_CENTER_JUSTIFY)
		elif pUnit.getFacingDirection() == DirectionTypes.DIRECTION_NORTHEAST:
			screen.setTableText("WBUnitDirection", 2,0 , "", pUnit.getButton(), WidgetTypes.WIDGET_PYTHON, 1030, 1, CvUtil.FONT_CENTER_JUSTIFY)
		elif pUnit.getFacingDirection() == DirectionTypes.DIRECTION_EAST:
			screen.setTableText("WBUnitDirection", 2,1 , "", pUnit.getButton(), WidgetTypes.WIDGET_PYTHON, 1030, 2, CvUtil.FONT_CENTER_JUSTIFY)
		elif pUnit.getFacingDirection() == DirectionTypes.DIRECTION_SOUTHEAST:
			screen.setTableText("WBUnitDirection", 2,2 , "", pUnit.getButton(), WidgetTypes.WIDGET_PYTHON, 1030, 3, CvUtil.FONT_CENTER_JUSTIFY)
		elif pUnit.getFacingDirection() == DirectionTypes.DIRECTION_SOUTH:
			screen.setTableText("WBUnitDirection", 1,2 , "", pUnit.getButton(), WidgetTypes.WIDGET_PYTHON, 1030, 4, CvUtil.FONT_CENTER_JUSTIFY)
		elif pUnit.getFacingDirection() == DirectionTypes.DIRECTION_SOUTHWEST:
			screen.setTableText("WBUnitDirection", 0,2 , "", pUnit.getButton(), WidgetTypes.WIDGET_PYTHON, 1030, 5, CvUtil.FONT_CENTER_JUSTIFY)
		elif pUnit.getFacingDirection() == DirectionTypes.DIRECTION_WEST:
			screen.setTableText("WBUnitDirection", 0,1 , "", pUnit.getButton(), WidgetTypes.WIDGET_PYTHON, 1030, 6, CvUtil.FONT_CENTER_JUSTIFY)
		elif pUnit.getFacingDirection() == DirectionTypes.DIRECTION_NORTHWEST:
			screen.setTableText("WBUnitDirection", 0,0 , "", pUnit.getButton(), WidgetTypes.WIDGET_PYTHON, 1030, 7, CvUtil.FONT_CENTER_JUSTIFY)
		elif pUnit.getFacingDirection() == DirectionTypes.NO_DIRECTION:
			screen.setTableText("WBUnitDirection", 1,1 , "", pUnit.getButton(), WidgetTypes.WIDGET_PYTHON, 1030, -1, CvUtil.FONT_CENTER_JUSTIFY)

		iWidth = screen.getXResolution()/5 - 40
		iX = screen.getXResolution()/2 - iWidth/2
		iY += iHeight
		screen.addDropDownBoxGFC("UnitAIType", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for item in lUnitAI:
			screen.addPullDownString("UnitAIType", item[0], item[1], item[1], item[1] == pUnit.getUnitAIType())

		iY += 30
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if pUnit.isPromotionReady():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		sText = CyTranslator().getText("TXT_KEY_WB_PROMOTION_READY", ())
		screen.setText("PromotionReadyText", "Background", "<font=3>" + sColor + sText + "</color></font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if pUnit.isMadeAttack():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		sText = CyTranslator().getText("TXT_KEY_WB_MADE_ATTACK", ())
		screen.setText("MadeAttackText", "Background", "<font=3>" + sColor + sText + "</color></font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if pUnit.isMadeInterception():
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		sText = CyTranslator().getText("TXT_KEY_WB_MADE_INTERCEPT", ())
		screen.setText("MadeInterceptionText", "Background", "<font=3>" + sColor + sText + "</color></font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		sText = ""
		iActivity = pUnit.getGroup().getActivityType()
		if iActivity > -1 and iActivity < len(CvPlatyBuilderScreen.Activities):
			sText = "<font=3>" + CvPlatyBuilderScreen.Activities[iActivity] + "</font>"
		screen.setLabel("UnitActivity", "Background", sText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def placeScript(self):
		screen = CyGInterfaceScreen("WBUnitScreen", CvScreenEnums.WB_UNIT)
		iWidth = screen.getXResolution()/5 - 40
		iX = screen.getXResolution()/2 - iWidth/2
		iY = screen.getYResolution()/2 - self.iScriptH - 35
		sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=3b>" + CyTranslator().getText("TXT_KEY_WB_SCRIPT_DATA", ()) + "</color></font>"
		screen.setText("UnitEditScriptData", "Background", sText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel( "ScriptPanel", "", "", False, False, iX, iY + 25, iWidth, self.iScriptH, PanelStyles.PANEL_STYLE_IN)
		screen.addMultilineText("GameScriptDataText", pUnit.getScriptData(), iX, iY + 25, iWidth, self.iScriptH, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeStats(self):
		screen = CyGInterfaceScreen("WBUnitScreen", CvScreenEnums.WB_UNIT)
		sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=4b>" + pUnit.getName() + "</color></font>"
		screen.setText("UnitScreenHeader", "Background", sText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 20, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1)
		sText = u"<font=3b>%s ID: %d, %s ID: %d</font>" %(CyTranslator().getText("TXT_KEY_WB_UNIT", ()), pUnit.getID(), CyTranslator().getText("TXT_KEY_WB_GROUP", ()), pUnit.getGroupID())
		screen.setLabel("UnitScreenHeaderB", "Background", sText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 50, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		sText = "<font=3b>%s, X: %d, Y: %d</font>" %(CyTranslator().getText("TXT_KEY_WB_LATITUDE",(pPlot.getLatitude(),)), pPlot.getX(), pPlot.getY())
		screen.setLabel("UnitLocation", "Background", sText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 70, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iX = screen.getXResolution()/5 + 20
		iY = self.iTable_Y
		iWidth = screen.getXResolution()/5 - 20

		screen.addDropDownBoxGFC("UnitOwner", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for iPlayerX in xrange(gc.getMAX_PLAYERS()):
			pPlayerX = gc.getPlayer(iPlayerX)
			if pPlayerX.isEverAlive():
				sName = pPlayerX.getName()
				if not pPlayerX.isAlive():
					sName = "*" + sName
				if pPlayerX.isTurnActive():
					sText = "[" + sText + "]"
				screen.addPullDownString("UnitOwner", sName, iPlayerX, iPlayerX, iPlayerX == pUnit.getOwner())

		iY += 30
		screen.addDropDownBoxGFC("ChangeBy", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		i = 1
		while i < 100001:
			screen.addPullDownString("ChangeBy", "(+/-) " + str(i), i, i, iChange == i)
			if str(i)[0] == "1":
				i *= 5
			else:
				i *= 2

		iY += 30
		screen.addDropDownBoxGFC("CommandUnits", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CommandUnits", CyTranslator().getText("TXT_KEY_WB_UNIT", ()), 0, 0, iCommandUnitType == 0)
		screen.addPullDownString("CommandUnits", CyTranslator().getText("TXT_KEY_SPACE_SHIP_SCREEN_TYPE_BUTTON", ()), 1, 1, iCommandUnitType == 1)
		screen.addPullDownString("CommandUnits", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT_COMBAT", ()), 2, 2, iCommandUnitType == 2)
		screen.addPullDownString("CommandUnits", CyTranslator().getText("TXT_KEY_PEDIA_DOMAIN", ()), 3, 3, 3 == iCommandUnitType == 3)
		screen.addPullDownString("CommandUnits", CyTranslator().getText("TXT_KEY_WB_GROUP", ()), 4, 4, iCommandUnitType == 4)
		screen.addPullDownString("CommandUnits", CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()), 5, 5, iCommandUnitType == 5)

		iY += 30
		screen.addDropDownBoxGFC("Commands", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("Commands", CyTranslator().getText("TXT_KEY_WB_COMMANDS", ()), 0, 0, True)
		screen.addPullDownString("Commands", CyTranslator().getText("TXT_KEY_OPTIONS_RESET", ()), 1, 1, False)
		screen.addPullDownString("Commands", CyTranslator().getText("TXT_KEY_MISSION_MOVE_TO", ()), 2, 2, False)
		screen.addPullDownString("Commands", CyTranslator().getText("TXT_KEY_MAP_SCRIPT_COPY", ()), 3, 3, False)
		screen.addPullDownString("Commands", CyTranslator().getText("TXT_KEY_ESPIONAGE_DESTROY_UNIT", ()), 4, 4, False)

		iY += 30
		screen.setButtonGFC("UnitLevelPlus", "", "", iX, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("UnitLevelMinus", "", "", iX + 25, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = CyTranslator().getText("TXT_KEY_WB_XLEVEL", ()) + ": " + str(pUnit.getLevel())
		screen.setLabel("UnitLevelText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, iX + 55, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		screen.setButtonGFC("UnitExperiencePlus", "", "", iX, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("UnitExperienceMinus", "", "", iX + 25, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = CyTranslator().getText("INTERFACE_PANE_EXPERIENCE", ()) + ": " + str(pUnit.getExperience())
		screen.setLabel("UnitExperienceText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, iX + 55, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		screen.setButtonGFC("UnitBaseStrPlus", "", "", iX, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("UnitBaseStrMinus", "", "", iX + 25, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = CyTranslator().getText("INTERFACE_PANE_STRENGTH", ()) + " " + str(pUnit.baseCombatStr()) + CyTranslator().getText("[ICON_STRENGTH]", ())
		screen.setLabel("UnitBaseStrText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, iX + 55, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		sText = CyTranslator().getText("INTERFACE_PANE_AIR_STRENGTH", ()) + " " + str(pUnit.airBaseCombatStr())
		screen.setLabel("UnitAirStrText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, iX + 55, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		screen.setButtonGFC("UnitDamagePlus", "", "", iX, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("UnitDamageMinus", "", "", iX + 25, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = CyTranslator().getText("TXT_KEY_WB_DAMAGE", ()) + ": " + str(pUnit.getDamage())
		screen.setLabel("UnitDamageText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, iX + 55, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		screen.setButtonGFC("UnitMovesLeftPlus", "", "", iX, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("UnitMovesLeftMinus", "", "", iX + 25, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = u"%s: %.2f" %(CyTranslator().getText("TXT_KEY_WB_MOVES", ()), float(pUnit.movesLeft()) / gc.getDefineINT("MOVE_DENOMINATOR")) + CyTranslator().getText("[ICON_MOVES]", ())
		screen.setLabel("UnitMovesLeftText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, iX + 55, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iY += 30
		screen.setButtonGFC("UnitImmobilePlus", "", "", iX, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		screen.setButtonGFC("UnitImmobileMinus", "", "", iX + 25, iY, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		sText = CyTranslator().getText("TXT_KEY_WB_IMMOBILE_TIMER", ()) + ": " + str(pUnit.getImmobileTimer())
		screen.setLabel("UnitImmobileText", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, iX + 55, iY + 1, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.placeMissions()

	def placeUnitType(self):
		screen = CyGInterfaceScreen("WBUnitScreen", CvScreenEnums.WB_UNIT)

		iX = screen.getXResolution() * 4/5
		iY = self.iTable_Y - 90
		iWidth = screen.getXResolution()/5 - 20

		iY += 30
		screen.addDropDownBoxGFC("LeaderType", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("LeaderType", CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_LEADER",()), 0, 0, not bUnitType)
		screen.addPullDownString("LeaderType", CyTranslator().getText("TXT_KEY_SPACE_SHIP_SCREEN_TYPE_BUTTON",()), 1, 1, bUnitType)

		iY += 30
		screen.addDropDownBoxGFC("CombatClass", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CombatClass", CyTranslator().getText("TXT_KEY_WB_CITY_ALL",()), -2, -2, -2 == iSelectedClass)
		screen.addPullDownString("CombatClass", CyTranslator().getText("TXT_PEDIA_NON_COMBAT",()), -1, -1, -1 == iSelectedClass)
		for iCombatClass in xrange(gc.getNumUnitCombatInfos()):
			screen.addPullDownString("CombatClass", gc.getUnitCombatInfo(iCombatClass).getDescription(), iCombatClass, iCombatClass, iCombatClass == iSelectedClass)

		iY += 30
		iHeight = (screen.getYResolution() - iY - 40) /24 * 24 + 2
		screen.addTableControlGFC("WBUnitType", 1, iX, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("WBUnitType", 0, "", iWidth)

		lUnitType = []
		for i in xrange(gc.getNumUnitInfos()):
			UnitInfo = gc.getUnitInfo(i)
			if UnitInfo.getUnitCombatType() != iSelectedClass and iSelectedClass > -2: continue
			if CvPlatyBuilderScreen.bHideInactive:
				iCivilization = gc.getPlayer(pUnit.getOwner()).getCivilizationType()
				if gc.getCivilizationInfo(iCivilization).getCivilizationUnits(UnitInfo.getUnitClassType()) != i: continue
			lUnitType.append([UnitInfo.getDescription(), i])
		lUnitType.sort()

		for item in lUnitType:
			iRow = screen.appendTableRow("WBUnitType")
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if bUnitType:
				if pUnit.getUnitType() == item[1]:
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			else:
				if pUnit.getLeaderUnitType() == item[1]:
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			screen.setTableText("WBUnitType", 0, iRow, "<font=3>" + sColor + item[0] + "</font></color>", gc.getUnitInfo(item[1]).getButton(), WidgetTypes.WIDGET_PYTHON, 8202, item[1], CvUtil.FONT_LEFT_JUSTIFY)

	def sortUnits(self):
		screen = CyGInterfaceScreen("WBUnitScreen", CvScreenEnums.WB_UNIT)
		global lUnits
		lUnits = []
		for iPlayerX in xrange(gc.getMAX_PLAYERS()):
			pPlayerX = gc.getPlayer(iPlayerX)
			if iOwnerType == 1 and iPlayerX != pUnit.getOwner(): continue
			if iOwnerType == 2 and pPlayerX.getTeam() != pUnit.getTeam(): continue
			if pPlayerX.isAlive():
				(loopUnit, iter) = pPlayerX.firstUnit(False)
				while(loopUnit):
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
						if loopUnit.getGroupID() != pUnit.getGroupID():
							bCopy = False
					if bCopy:
						lUnits.append([loopUnit.getOwner(), loopUnit.getID()])
					(loopUnit, iter) = pPlayerX.nextUnit(iter, False)
		lUnits.sort()
		self.placeCurrentUnit()
		
	def placeCurrentUnit(self):
		screen = CyGInterfaceScreen("WBUnitScreen", CvScreenEnums.WB_UNIT)

		iX = 20
		iWidth = screen.getXResolution()/5 - 20
		iHeight = (screen.getYResolution() - self.iTable_Y - 42) /24 * 24 + 2
		screen.addTableControlGFC("WBCurrentUnit", 3, iX, self.iTable_Y, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("WBCurrentUnit", 0, "", 24)
		screen.setTableColumnHeader("WBCurrentUnit", 1, "", 24)
		screen.setTableColumnHeader("WBCurrentUnit", 2, "", iWidth - 48)

		for i in lUnits:
			pPlayerX = gc.getPlayer(i[0])
			pUnitX = pPlayerX.getUnit(i[1])
			if pUnitX.isNone(): continue
			iRow = screen.appendTableRow("WBCurrentUnit")
			sText = pUnitX.getName()
			if len(pUnitX.getNameNoDesc()):
				sText = pUnitX.getNameNoDesc()
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if pUnitX.getOwner() == pUnit.getOwner():
				if pUnitX.getID() == pUnit.getID():
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				elif pUnitX.getGroupID() == pUnit.getGroupID():
					sColor = CyTranslator().getText("[COLOR_YELLOW]", ())
			screen.setTableText("WBCurrentUnit", 2, iRow, "<font=3>" + sColor + sText + "</font></color>", pUnitX.getButton(), WidgetTypes.WIDGET_PYTHON, 8300 + i[0], i[1], CvUtil.FONT_LEFT_JUSTIFY)
			iLeader = pPlayerX.getLeaderType()
			iCiv = pUnitX.getCivilizationType()
			screen.setTableText("WBCurrentUnit", 0, iRow, "", gc.getCivilizationInfo(iCiv).getButton(), WidgetTypes.WIDGET_PYTHON, 7872, iCiv, CvUtil.FONT_LEFT_JUSTIFY )
			screen.setTableText("WBCurrentUnit", 1, iRow, "", gc.getLeaderHeadInfo(iLeader).getButton(), WidgetTypes.WIDGET_PYTHON, 7876, iLeader, CvUtil.FONT_LEFT_JUSTIFY )

	def placeCargo(self):
		screen = CyGInterfaceScreen("WBUnitScreen", CvScreenEnums.WB_UNIT)
		iX = screen.getXResolution()*3/5
		iY = screen.getYResolution()/2 + 30
		iWidth = screen.getXResolution()/5 - 20
		screen.addDropDownBoxGFC("CargoType", iX, iY - 30, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CargoType", CyTranslator().getText("TXT_KEY_UNIT_TRANSPORT", ()), 0, 0, not bCargo)
		screen.addPullDownString("CargoType", CyTranslator().getText("TXT_KEY_WB_CARGO_SPACE", ()), 1, 1, bCargo)

		iHeight = (screen.getYResolution() - iY - 42) /24 * 24 + 2

		screen.addTableControlGFC("WBCargoUnits", 1, iX, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader("WBCargoUnits", 0, "", iWidth)
		screen.hide("UnitCargoPlus")
		screen.hide("UnitCargoMinus")
		screen.hide("CargoSpaceHeader")

		if bCargo:
			screen.setButtonGFC("UnitCargoPlus", "", "", iX, screen.getYResolution() - 42, 24, 24, WidgetTypes.WIDGET_PYTHON, 1030, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
			screen.setButtonGFC("UnitCargoMinus", "", "", iX + 25, screen.getYResolution() - 42, 24, 24, WidgetTypes.WIDGET_PYTHON, 1031, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
			sText = CyTranslator().getText("TXT_KEY_WB_CARGO_SPACE", ()) + " (" + str(pUnit.getCargo()) + "/" + str(pUnit.cargoSpace()) + ")"
			screen.setLabel("CargoSpaceHeader", "Background", "<font=3b>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, iX + 50, screen.getYResolution() - 41, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			if pUnit.cargoSpace() > 0:
				for i in xrange(pPlot.getNumUnits()):
					pUnitX = pPlot.getUnit(i)
					if pUnitX.isNone(): continue
					if pUnitX.getID() == pUnit.getID(): continue
					if pUnit.domainCargo() > -1:
						if pUnitX.getDomainType() != pUnit.domainCargo(): continue
					if pUnit.specialCargo() > -1:
						if pUnitX.getSpecialUnitType() != pUnit.specialCargo(): continue
					iPlayerX = pUnitX.getOwner()
					if iPlayerX != pUnit.getOwner(): continue
					iRow = screen.appendTableRow("WBCargoUnits")
					sText = pUnitX.getName()
					if len(pUnitX.getNameNoDesc()):
						sText = pUnitX.getNameNoDesc()
					sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
					if pUnitX.isCargo():
						sColor = CyTranslator().getText("[COLOR_YELLOW]", ())
					if pUnitX.getTransportUnit().getID() == pUnit.getID():
						sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
					screen.setTableText("WBCargoUnits", 0, iRow, "<font=3>" + sColor + sText + "</font></color>", pUnitX.getButton(), WidgetTypes.WIDGET_PYTHON, 8300 + iPlayerX, pUnitX.getID(), CvUtil.FONT_LEFT_JUSTIFY)
		else:
			for i in xrange(pPlot.getNumUnits()):
				pUnitX = pPlot.getUnit(i)
				if pUnitX.isNone(): continue
				if pUnitX.getID() == pUnit.getID(): continue
				if pUnitX.cargoSpace() < 1: continue
				if pUnitX.domainCargo() > -1:
					if pUnit.getDomainType() != pUnitX.domainCargo(): continue
				if pUnitX.specialCargo() > -1:
					if pUnit.getSpecialUnitType() != pUnitX.specialCargo(): continue
				iPlayerX = pUnitX.getOwner()
				if iPlayerX != pUnit.getOwner(): continue
				iRow = screen.appendTableRow("WBCargoUnits")
				sText = pUnitX.getName()
				if len(pUnitX.getNameNoDesc()):
					sText = pUnitX.getNameNoDesc()
				sText += " (" + str(pUnitX.getCargo()) + "/" + str(pUnitX.cargoSpace()) + ")"
				sColor = CyTranslator().getText("[COLOR_YELLOW]", ())
				if pUnitX.isFull():
					sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
				if pUnit.getTransportUnit().getID() == pUnitX.getID():
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				screen.setTableText("WBCargoUnits", 0, iRow, "<font=3>" + sColor + sText + "</font></color>", pUnitX.getButton(), WidgetTypes.WIDGET_PYTHON, 8300 + iPlayerX, pUnitX.getID(), CvUtil.FONT_LEFT_JUSTIFY)

	def handleInput(self, inputClass):
		screen = CyGInterfaceScreen( "WBUnitScreen", CvScreenEnums.WB_UNIT)
		global iChange
		global iChangeType
		global iOwnerType
		global iPlotType
		global iCopyType
		global iCommandUnitType
		global iSelectedClass
		global iMissionType
		global iMissionData1
		global bCargo
		global bUnitType
		global bRemove
		sName = inputClass.getFunctionName()

		if sName == "ChangeBy":
			if bRemove:
				iChange = -screen.getPullDownData("ChangeBy", screen.getSelectedPullDownID("ChangeBy"))
			else:
				iChange = screen.getPullDownData("ChangeBy", screen.getSelectedPullDownID("ChangeBy"))

		elif sName == "CurrentPage":
			iIndex = screen.getPullDownData("CurrentPage", screen.getSelectedPullDownID("CurrentPage"))
			if iIndex == 1:
				WBPromotionScreen.WBPromotionScreen().interfaceScreen(pUnit)
			elif iIndex == 2:
				WBPlayerScreen.WBPlayerScreen().interfaceScreen(pUnit.getOwner())
			elif iIndex == 3:
				WBTeamScreen.WBTeamScreen().interfaceScreen(pUnit.getTeam())
			elif iIndex == 4:
				WBPlotScreen.WBPlotScreen().interfaceScreen(pPlot)
			elif iIndex == 5:
				WBEventScreen.WBEventScreen().interfaceScreen(pPlot)
			elif iIndex == 6:
				WBPlayerUnits.WBPlayerUnits().interfaceScreen(pUnit.getOwner())
			elif iIndex == 11:
				WBInfoScreen.WBInfoScreen().interfaceScreen(pUnit.getOwner())

		elif sName == "CargoType":
			bCargo = not bCargo
			self.placeCargo()

		elif sName == "ChangeType":
			iChangeType = screen.getPullDownData("ChangeType", screen.getSelectedPullDownID("ChangeType"))

		elif sName == "OwnerType":
			iOwnerType = screen.getPullDownData("OwnerType", screen.getSelectedPullDownID("OwnerType"))
			self.sortUnits()

		elif sName == "PlotType":
			iPlotType = screen.getPullDownData("PlotType", screen.getSelectedPullDownID("PlotType"))
			self.sortUnits()

		elif sName == "CopyType":
			iCopyType = screen.getPullDownData("CopyType", screen.getSelectedPullDownID("CopyType"))
			self.sortUnits()

		elif sName == "UnitScreenHeader":
			popup = Popup.PyPopup(CvUtil.EventEditUnitName, EventContextTypes.EVENTCONTEXT_ALL)
			popup.setUserData((pUnit.getID(), pUnit.getOwner()))
			popup.setBodyString(CyTranslator().getText("TXT_KEY_RENAME_UNIT", ()))
			popup.createEditBox(pUnit.getNameNoDesc())
			popup.setEditBoxMaxCharCount(25)
			popup.launch()

		elif sName == "WBCurrentUnit":
			if inputClass.getData1() >= 8300:
				iPlayer = inputClass.getData1() - 8300
				self.interfaceScreen(gc.getPlayer(iPlayer).getUnit(inputClass.getData2()))

		elif sName == "UnitOwner":
			self.changeOwner(screen.getPullDownData("UnitOwner", screen.getSelectedPullDownID("UnitOwner")))

		elif sName == "LeaderType":
			bUnitType = not bUnitType
			self.placeUnitType()

		elif sName == "CombatClass":
			iSelectedClass = screen.getPullDownData("CombatClass", screen.getSelectedPullDownID("CombatClass"))
			self.placeUnitType()

		elif sName == "WBUnitType":
			self.changeUnitType(pUnit, inputClass.getData2(), bUnitType)

		elif sName.find("UnitLevel") > -1:
			if inputClass.getData1() == 1030:
				pUnit.setLevel(pUnit.getLevel() + abs(iChange))
			elif inputClass.getData1() == 1031:
				pUnit.setLevel(max(0, pUnit.getLevel() - abs(iChange)))
			self.placeStats()

		elif sName.find("UnitExperience") > -1:
			if inputClass.getData1() == 1030:
				pUnit.changeExperience(abs(iChange), -1, False, False, False)
			elif inputClass.getData1() == 1031:
				pUnit.changeExperience(- min(abs(iChange), pUnit.getExperience()), -1, False, False, False)
			self.placeStats()

		elif sName.find("UnitBaseStr") > -1:
			if inputClass.getData1() == 1030:
				pUnit.setBaseCombatStr(pUnit.baseCombatStr() + abs(iChange))
			elif inputClass.getData1() == 1031:
				pUnit.setBaseCombatStr(max(0, pUnit.baseCombatStr() - abs(iChange)))
			self.placeStats()

		elif sName.find("UnitDamage") > -1:
			if inputClass.getData1() == 1030:
				pUnit.changeDamage(abs(iChange), -1)
			elif inputClass.getData1() == 1031:
				pUnit.changeDamage(- min(abs(iChange), pUnit.getDamage()), -1)
			self.placeStats()

		elif sName.find("UnitMovesLeft") > -1:
			if inputClass.getData1() == 1030:
				pUnit.changeMoves(- abs(iChange) * gc.getDefineINT("MOVE_DENOMINATOR"))
			elif inputClass.getData1() == 1031:
				pUnit.changeMoves(min(abs(iChange) * gc.getDefineINT("MOVE_DENOMINATOR"), pUnit.movesLeft()))
			self.placeStats()

		elif sName.find("UnitImmobile") > -1:
			if inputClass.getData1() == 1030:
				pUnit.setImmobileTimer(pUnit.getImmobileTimer() + abs(iChange))
			elif inputClass.getData1() == 1031:
				pUnit.setImmobileTimer(max(0, pUnit.getImmobileTimer() - abs(iChange)))
			self.placeStats()

		elif sName.find("UnitCargo") > -1:
			if inputClass.getData1() == 1030:
				pUnit.changeCargoSpace(abs(iChange))
			elif inputClass.getData1() == 1031:
				pUnit.changeCargoSpace(- min(abs(iChange), pUnit.cargoSpace()))
			self.placeCargo()

		elif sName == "WBCargoUnits":
			iPlayerX = inputClass.getData1() - 8300
			pUnitX = gc.getPlayer(iPlayerX).getUnit(inputClass.getData2())
			if bCargo:
				if pUnitX.getTransportUnit().getID() == pUnit.getID():
					pUnitX.setTransportUnit(CyUnit())
				else:
					if not pUnit.isFull():
						pUnitX.setTransportUnit(pUnit)
			else:
				if pUnit.getTransportUnit().getID() == pUnitX.getID():
					pUnit.setTransportUnit(CyUnit())
				else:
					if not pUnitX.isFull():
						pUnit.setTransportUnit(pUnitX)
			self.interfaceScreen(pUnit)

		elif sName == "PromotionReadyText":
			pUnit.setPromotionReady(not pUnit.isPromotionReady())
			self.placeDirection()

		elif sName == "MadeAttackText":
			pUnit.setMadeAttack(not pUnit.isMadeAttack())
			self.placeDirection()
			self.placeMissions()

		elif sName == "MadeInterceptionText":
			pUnit.setMadeInterception(not pUnit.isMadeInterception())
			self.placeDirection()
			self.placeMissions()

		elif sName == "UnitAIType":
			pUnit.setUnitAIType(screen.getPullDownData("UnitAIType", screen.getSelectedPullDownID("UnitAIType")))

		elif sName == "WBUnitDirection":
			self.changeDirection(inputClass.getData2(), pUnit)
			self.placeDirection()

		elif sName == "UnitEditScriptData":
			popup = Popup.PyPopup(3333, EventContextTypes.EVENTCONTEXT_ALL)
			popup.setHeaderString(CyTranslator().getText("TXT_KEY_WB_SCRIPT", ()))
			popup.setUserData((pUnit.getOwner(), pUnit.getID()))
			popup.createEditBox(pUnit.getScriptData())
			popup.launch()
			return

		elif sName == "CopyStats":
			self.handleCopyAll()

		elif sName == "CommandUnits":
			iCommandUnitType = screen.getPullDownData("CommandUnits", screen.getSelectedPullDownID("CommandUnits"))

		elif sName == "Commands":
			iIndex = screen.getPullDownData("Commands", screen.getSelectedPullDownID("Commands"))
			lUnits = []
			self.top.lMoveUnit = []
			if iCommandUnitType == 0:
				lUnits.append(pUnit)
			else:
				for i in xrange(pPlot.getNumUnits()):
					pUnitX = pPlot.getUnit(i)
					if pUnitX.isNone(): continue
					if pUnitX.getOwner() != pUnit.getOwner(): continue
					if iCommandUnitType == 1:
						if pUnitX.getUnitType() != pUnit.getUnitType(): continue
					elif iCommandUnitType == 2:
						if pUnitX.getUnitCombatType() != pUnit.getUnitCombatType(): continue
					elif iCommandUnitType == 3:
						if pUnitX.getDomainType() != pUnit.getDomainType(): continue
					elif iCommandUnitType == 4:
						if pUnitX.getGroupID() != pUnit.getGroupID(): continue
					lUnits.append(pUnitX)
			iRefresh = 0
			for pUnitX in lUnits:
				iRefresh = self.doAllCommands(pUnitX, iIndex)
			screen.hideScreen()
			if iRefresh == 1:
				self.interfaceScreen(pPlot.getUnit(0))
			elif iRefresh == 2:
				self.interfaceScreen(pUnit)

		elif sName == "Missions":
			iMissionType = screen.getPullDownData("Missions", screen.getSelectedPullDownID("Missions"))
			iMissionData1 = -1
			self.placeMissions()

		elif sName == "MissionInput":
			iMissionData1 = inputClass.getData2()
			self.placeMissions()

		elif sName == "PushMission":
			self.doMission()

		elif sName == "TargetPlot":
			self.top.iPlayerAddMode = "TargetPlot"
			self.top.TempInfo = [pUnit.getOwner(), pUnit.getID()]
			screen.hideScreen()

		elif sName == "UnitExit":
			self.top.iTargetPlotX = -1
			self.top.iTargetPlotY = -1

		elif sName == "HideInactive":
			CvPlatyBuilderScreen.bHideInactive = not CvPlatyBuilderScreen.bHideInactive
			CvPlatyBuilderScreen.CvWorldBuilderScreen().refreshSideMenu()
			sText = u"<font=3b>" + CyTranslator().getText("TXT_KEY_PEDIA_HIDE_INACTIVE", ()) + "</font>"
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if CvPlatyBuilderScreen.bHideInactive:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			screen.setText("HideInactive", "Background", sColor + sText + "</color>", CvUtil.FONT_LEFT_JUSTIFY, screen.getXResolution() * 4/5, self.iTable_Y - 85, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			self.placeUnitType()

		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER) and inputClass.getData() == int(InputTypes.KB_ESCAPE):
			self.top.iTargetPlotX = -1
			self.top.iTargetPlotY = -1
		return 1

	def doAllCommands(self, pUnitX, iIndex):
		if iIndex == 1:
			Info = gc.getUnitInfo(pUnit.getUnitType())
			pUnitX.setBaseCombatStr(Info.getCombat())
			pUnitX.setDamage(0, -1)
			pUnitX.setMoves(0)
			pUnitX.setImmobileTimer(0)
			pUnitX.setPromotionReady(False)
			pUnitX.setMadeAttack(False)
			pUnitX.setMadeInterception(False)
			self.changeDirection(DirectionTypes.DIRECTION_SOUTH, pUnitX)
			pUnitX.setUnitAIType(Info.getDefaultUnitAIType())
			pUnitX.changeCargoSpace(Info.getCargoSpace() - pUnitX.cargoSpace())
			pUnitX.setScriptData("")
			return 2
		elif iIndex == 2:
			self.top.iPlayerAddMode = "MoveUnits"
			self.top.lMoveUnit.append([pUnitX.getOwner(), pUnitX.getID()])
			return 0
		elif iIndex == 3:
			for i in xrange(iChange + 1):
				pNewUnit = gc.getPlayer(pUnitX.getOwner()).initUnit(pUnitX.getUnitType(), pUnitX.getX(), pUnitX.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
				pNewUnit.convert(pUnitX)
				pNewUnit.setBaseCombatStr(pUnitX.baseCombatStr())
				pNewUnit.changeCargoSpace(pUnitX.cargoSpace() - pNewUnit.cargoSpace())
				pNewUnit.setImmobileTimer(pUnitX.getImmobileTimer())
				pNewUnit.setScriptData(pUnitX.getScriptData())
			pUnitX.kill(False, -1)
			return 1
		elif iIndex == 4:
			pUnitX.kill(False, -1)
			if pPlot.getNumUnits() > 0:
				return 1
			return 0
		return 0

	def doMission(self):
		sType = gc.getMissionInfo(iMissionType).getType()
		UnitInfo = gc.getUnitInfo(pUnit.getUnitType())
		iData1 = -1
		iData2 = -1
		if sType == "MISSION_MOVE_TO_UNIT": return 2
		elif sType in self.lSelectableMissions:
			iData1 = iMissionData1
		elif sType == "MISSION_GOLDEN_AGE":
			iData1 = -1
		else:
			iData1 = self.top.iTargetPlotX
			iData2 = self.top.iTargetPlotY
		pTargetPlot = CyMap().plot(self.top.iTargetPlotX, self.top.iTargetPlotY)
		pUnit.getGroup().pushMission(MissionTypes(iMissionType), iData1, iData2, 0, False, True, MissionAITypes.NO_MISSIONAI, pTargetPlot, pUnit)
		self.interfaceScreen(pUnit)

	def changeDirection(self, iNewDirection, pUnitX):
		if iNewDirection == -1: return
		iOldDirection = pUnitX.getFacingDirection()
		if iNewDirection == iOldDirection: return
		if iOldDirection > iNewDirection:
			for i in xrange(iOldDirection - iNewDirection):
				pUnitX.rotateFacingDirectionCounterClockwise()
		else:
			for i in xrange(iNewDirection - iOldDirection):
				pUnitX.rotateFacingDirectionClockwise()

	def changeOwner(self, iPlayer):
		pNewUnit = gc.getPlayer(iPlayer).initUnit(pUnit.getUnitType(), pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
		pNewUnit.convert(pUnit)
		pNewUnit.setBaseCombatStr(pUnit.baseCombatStr())
		pNewUnit.changeCargoSpace(pUnit.cargoSpace() - pNewUnit.cargoSpace())
		pNewUnit.setImmobileTimer(pUnit.getImmobileTimer())
		pNewUnit.setScriptData(pUnit.getScriptData())
		pUnit.kill(False, -1)
		self.interfaceScreen(pNewUnit)

	def changeUnitType(self, pUnit, iUnitType, bUnitType):
		if bUnitType:
			pNewUnit = gc.getPlayer(pUnit.getOwner()).initUnit(iUnitType, pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
			pNewUnit.convert(pUnit)
			pNewUnit.setScriptData("PlatyUnit" + pUnit.getScriptData())
			pUnit.kill(False, -1)
			for i in xrange(pPlot.getNumUnits()):
				pUnitX = pPlot.getUnit(i)
				if pUnitX.getScriptData().find("PlatyUnit") == 0:
					pUnitX.setScriptData(pUnitX.getScriptData()[9:])
					break
			self.interfaceScreen(pUnitX)
		else:
			if pUnit.getLeaderUnitType() == iUnitType:
				pUnit.setLeaderUnitType(-1)
			else:
				pUnit.setLeaderUnitType(iUnitType)
			self.interfaceScreen(pUnit)

	def handleCopyAll(self):
		for i in lUnits:
			loopUnit = gc.getPlayer(i[0]).getUnit(i[1])
			if loopUnit.isNone(): continue
			if iChangeType == 0:
				loopUnit.setLevel(pUnit.getLevel())
			elif iChangeType == 1:
				loopUnit.setExperience(pUnit.getExperience(), -1)
			elif iChangeType == 2:
				loopUnit.setBaseCombatStr(pUnit.baseCombatStr())
			elif iChangeType == 3:
				loopUnit.setDamage(pUnit.getDamage(), -1)
			elif iChangeType == 4:
				loopUnit.setMoves(pUnit.getMoves())
			elif iChangeType == 5:
				loopUnit.setImmobileTimer(pUnit.getImmobileTimer())
			elif iChangeType == 6:
				loopUnit.setPromotionReady(pUnit.isPromotionReady())
			elif iChangeType == 7:
				loopUnit.setMadeAttack(pUnit.isMadeAttack())
			elif iChangeType == 8:
				loopUnit.setMadeInterception(pUnit.isMadeInterception())
			elif iChangeType == 9:
				self.changeDirection(pUnit.getFacingDirection(), loopUnit)
			elif iChangeType == 10:
				loopUnit.setUnitAIType(pUnit.getUnitAIType())
			elif iChangeType == 11:
				loopUnit.changeCargoSpace(pUnit.cargoSpace() - loopUnit.cargoSpace())
			elif iChangeType == 12:
				loopUnit.setScriptData(pUnit.getScriptData())

	def update(self, fDelta):
		self.placeMap()
		return 1