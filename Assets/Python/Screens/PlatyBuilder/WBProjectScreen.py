from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import WBTeamScreen
import WBTechScreen
import WBPlayerScreen
import WBPlayerUnits
import WBInfoScreen
import CvPlatyBuilderScreen
import CvEventManager
gc = CyGlobalContext()

iChange = 1
bRemove = False
bApplyAll = False
bNoBarb = True
iProjectType = 0

class WBProjectScreen:

	def __init__(self):
		self.iTable_Y = 110

	def interfaceScreen(self, iTeamX):
		screen = CyGInterfaceScreen( "WBProjectScreen", CvScreenEnums.WB_PROJECT)
		global iTeam
		global pTeam
		iTeam = iTeamX
		pTeam = gc.getTeam(iTeam)

		screen.setRenderInterfaceOnly(True)
		screen.addPanel( "MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.setDimensions(0,0, screen.getXResolution(), screen.getYResolution())
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
	
		screen.setText("WBProjectExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setLabel("ProjectHeader", "Background", "<font=4b>" + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addDropDownBoxGFC("CurrentTeam", 20, 20, screen.getXResolution()/5, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i in xrange(gc.getMAX_TEAMS()):
			if gc.getTeam(i).isAlive():
				iLeader = gc.getTeam(i).getLeaderID()
				sName = gc.getPlayer(iLeader).getName()
				if gc.getTeam(i).getNumMembers() > 1:
					sName += " (" + str(gc.getTeam(i).getNumMembers()) + " " + CyTranslator().getText("TXT_KEY_MEMBERS_TITLE", ()) + ")"
				screen.addPullDownString("CurrentTeam", sName, i, i, i == iTeam)

		screen.addDropDownBoxGFC("ChangeBy", 20, 50, screen.getXResolution()/5, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		i = 1
		while i < 101:
			screen.addPullDownString("ChangeBy", "(+/-) " + str(i), i, i, iChange == i)
			if str(i)[0] == "1":
				i *= 5
			else:
				i *= 2

		screen.addDropDownBoxGFC("ProjectType", 20, self.iTable_Y - 30, screen.getXResolution()/5, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("ProjectType", CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()), 0, 0, iProjectType == 0)
		screen.addPullDownString("ProjectType", CyTranslator().getText("TXT_KEY_PEDIA_TEAM_PROJECT", ()), 1, 1, iProjectType == 1)
		screen.addPullDownString("ProjectType", CyTranslator().getText("TXT_KEY_PEDIA_WORLD_PROJECT", ()), 2, 2, iProjectType == 2)

		screen.addDropDownBoxGFC("CurrentPage", 20, screen.getYResolution() - 42, screen.getXResolution()/5, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA", ()), 0, 0, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_TEAM_DATA", ()), 1, 1, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()), 2, 2, True)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH", ()), 3, 3, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()) + " + " + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()), 4, 4, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_INFO_SCREEN", ()), 11, 11, False)

		sText = "<font=3b>" + CyTranslator().getText("TXT_KEY_GAME_OPTION_NO_BARBARIANS", ()) + "</font>"
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if bNoBarb:
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setText("NoBarbarians", "Background", sColor + sText + "</color>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 20, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		sText = "<font=3b>" + CyTranslator().getText("TXT_KEY_WB_COPY_ALL", (CyTranslator().getText("TXT_KEY_MAIN_MENU_PLAYERS", ()),)) + "</font>"
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if bApplyAll:
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setText("ApplyAll", "Background", sColor + sText + "</color>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 20, 50, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.addDropDownBoxGFC("ChangeType", screen.getXResolution() - 120, self.iTable_Y - 30, 100, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_ADD", ()), 1, 1, not bRemove)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_REMOVE", ()), 0, 0, bRemove)
		sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + " (+/-)</color></font>"
		screen.setText("ProjectAll", "Background", sText, CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 120, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		self.sortProjects()

	def sortProjects(self):
		screen = CyGInterfaceScreen( "WBProjectScreen", CvScreenEnums.WB_PROJECT)
		global lProject
		lProject = []
		for i in xrange(gc.getNumProjectInfos()):
			Info = gc.getProjectInfo(i)
			if iProjectType == 1 and not isTeamProject(i): continue
			if iProjectType == 2 and not isWorldProject(i): continue
			iTeam = Info.getMaxTeamInstances()
			iWorld = Info.getMaxGlobalInstances()
			iMax = max(iTeam, iWorld)
			if iTeam > -1 and iWorld > -1:
				iMax = min(iTeam, iWorld)
			lProject.append([Info.getDescription(), i, iMax])
		lProject.sort()
		self.placeProjects()

	def placeProjects(self):
		screen = CyGInterfaceScreen( "WBProjectScreen", CvScreenEnums.WB_PROJECT)
		iMaxRows = (screen.getYResolution() - self.iTable_Y - 42) / 24
		nColumns = max(1, min(5, (len(lProject) + iMaxRows - 1)/iMaxRows))
		iWidth = screen.getXResolution() - 40
		iHeight = iMaxRows * 24 + 2
		screen.hide("CurrentProjectPlus")
		screen.hide("CurrentProjectMinus")
		screen.hide("CurrentProjectText")

		screen.addTableControlGFC("WBProject", nColumns, 20, self.iTable_Y, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		for i in xrange(nColumns):
			screen.setTableColumnHeader("WBProject", i, "", iWidth/nColumns)
		nRows = (len(lProject) + nColumns - 1) / nColumns
		for i in xrange(nRows):
			screen.appendTableRow("WBProject")

		for iCount in xrange(len(lProject)):
			item = lProject[iCount]
			iRow = iCount % nRows
			iColumn = iCount / nRows
			Info = gc.getProjectInfo(item[1])
			iCount = pTeam.getProjectCount(item[1])
			sText = item[0]
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			if item[2] > 1:
				sText = u"%s (%d/%d)" %(sText, iCount, item[2])
				if iCount < item[2]:
					sColor = CyTranslator().getText("[COLOR_YELLOW]", ())
			elif item[2] == -1:
				if iCount > 0:
					sText = u"%s (%d)" %(sText, iCount)
			if iCount == 0:
				sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			screen.setTableText("WBProject", iColumn, iRow, "<font=3>" + sColor + sText + "</font></color>", Info.getButton(), WidgetTypes.WIDGET_PYTHON, 6785, item[1], CvUtil.FONT_LEFT_JUSTIFY )

	def handleInput (self, inputClass):
		screen = CyGInterfaceScreen( "WBProjectScreen", CvScreenEnums.WB_PROJECT)
		global iChange
		global bApplyAll
		global bNoBarb
		global iProjectType
		global bRemove

		if inputClass.getFunctionName() == "ChangeBy":
			if bRemove:
				iChange = -screen.getPullDownData("ChangeBy", screen.getSelectedPullDownID("ChangeBy"))
			else:
				iChange = screen.getPullDownData("ChangeBy", screen.getSelectedPullDownID("ChangeBy"))

		elif inputClass.getFunctionName() == "ChangeType":
			bRemove = not bRemove
			iChange = -iChange

		elif inputClass.getFunctionName() == "CurrentTeam":
			iIndex = screen.getPullDownData("CurrentTeam", screen.getSelectedPullDownID("CurrentTeam"))
			self.interfaceScreen(iIndex)

		elif inputClass.getFunctionName() == "ProjectType":
			iProjectType = screen.getPullDownData("ProjectType", screen.getSelectedPullDownID("ProjectType"))
			self.sortProjects()

		elif inputClass.getFunctionName() == "CurrentPage":
			iIndex = screen.getPullDownData("CurrentPage", screen.getSelectedPullDownID("CurrentPage"))
			if iIndex == 0:
				WBPlayerScreen.WBPlayerScreen().interfaceScreen(pTeam.getLeaderID())
			elif iIndex == 1:
				WBTeamScreen.WBTeamScreen().interfaceScreen(iTeam)
			elif iIndex == 3:
				WBTechScreen.WBTechScreen().interfaceScreen(iTeam)
			elif iIndex == 4:
				WBPlayerUnits.WBPlayerUnits().interfaceScreen(pTeam.getLeaderID())
			elif iIndex == 11:
				WBInfoScreen.WBInfoScreen().interfaceScreen(pTeam.getLeaderID())

		elif inputClass.getFunctionName() == "ProjectAll":
			for item in lProject:
				self.editProject(item[1])
			self.placeProjects()

		elif inputClass.getFunctionName() == "WBProject":
			self.editProject(inputClass.getData2())
			self.placeProjects()

		elif inputClass.getFunctionName() == "ApplyAll":
			bApplyAll = not bApplyAll
			sText = u"<font=3b>" + CyTranslator().getText("TXT_KEY_WB_COPY_ALL", (CyTranslator().getText("TXT_KEY_MAIN_MENU_PLAYERS", ()),)) + "</font>"
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if bApplyAll:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			screen.modifyString("ApplyAll", sColor + sText + "</color>", 0)

		elif inputClass.getFunctionName() == "NoBarbarians":
			bNoBarb = not bNoBarb
			sText = u"<font=3b>" + CyTranslator().getText("TXT_KEY_GAME_OPTION_NO_BARBARIANS", ()) + "</font>"
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if bNoBarb:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			screen.modifyString("NoBarbarians", sColor + sText + "</color>", 0)
		return 1

	def editProject(self, item):
		if bApplyAll:
			for i in xrange(gc.getMAX_TEAMS()):
				pTeamX = gc.getTeam(i)
				if pTeamX.isBarbarian() and bNoBarb: continue
				if pTeamX.isAlive():
					self.modifyCount(item, pTeamX)
		else:
			self.modifyCount(item, pTeam)
		if gc.getProjectInfo(item).isAllowsNukes() and CyGame().getProjectCreatedCount(item) == 0:
			CyGame().makeNukesValid(False)

	def modifyCount(self, item, pTeamX):
		iCount = max(iChange, - pTeamX.getProjectCount(item))
		if bRemove:
			Info = gc.getProjectInfo(item)
			iTeam = Info.getMaxTeamInstances()
			iWorld = Info.getMaxGlobalInstances()
			iMax = max(iTeam, iWorld)
			if iTeam > -1 and iWorld > -1:
				iMax = min(iTeam, iWorld)
			if iMax > -1:
				iCount = min(iCount, iMax - pTeamX.getProjectCount(item))
		pTeamX.changeProjectCount(item, iCount)
		if CvPlatyBuilderScreen.bPython and iCount > 0:
			pCapital = gc.getPlayer(pTeamX.getLeaderID()).getCapitalCity()
			if not pCapital.isNone():
				for i in xrange(iCount):
					CvEventManager.CvEventManager().onProjectBuilt([pCapital, item])

	def update(self, fDelta):
		return 1