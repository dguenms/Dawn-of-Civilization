from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import WBUnitScreen
import WBPlayerScreen
import WBTeamScreen
import WBPlotScreen
import WBEventScreen
import WBPlayerUnits
import WBInfoScreen
import CvPlatyBuilderScreen
import CvEventManager
gc = CyGlobalContext()

bApplyAll = False
iCopyType = 0
iPlotType = 0
iChangeType = 2
iOwnerType = 0
iSelectedClass = -2

class WBPromotionScreen:

	def __init__(self):
		self.iTable_Y = 110

	def interfaceScreen(self, pUnitX):
		screen = CyGInterfaceScreen( "WBPromotionScreen", CvScreenEnums.WB_PROMOTION)
		global pUnit
		global pPlot
		pUnit = pUnitX
		pPlot = pUnit.plot()
		iWidth = screen.getXResolution()/5 - 20

		screen.setRenderInterfaceOnly(True)
		screen.addPanel( "MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
	
		screen.setText("WBPromotionExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setLabel("PromotionHeader", "Background", "<font=4b>" + pUnit.getName() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 20, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		sText = u"<font=3b>%s ID: %d, %s ID: %d</font>" %(CyTranslator().getText("TXT_KEY_WB_UNIT", ()), pUnit.getID(), CyTranslator().getText("TXT_KEY_WB_GROUP", ()), pUnit.getGroupID())
		screen.setLabel("PromotionHeaderB", "Background", sText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 50, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.addDropDownBoxGFC("OwnerType", 20, 20, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("OwnerType", CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()), 0, 0, 0 == iOwnerType)
		screen.addPullDownString("OwnerType", CyTranslator().getText("TXT_KEY_PITBOSS_TEAM", ()), 2, 2, 2 == iOwnerType)
		screen.addPullDownString("OwnerType", CyTranslator().getText("TXT_KEY_MAIN_MENU_PLAYER", ()), 1, 1, 1 == iOwnerType)

		screen.addDropDownBoxGFC("CopyType", 20, 50, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CopyType", CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()), 0, 0, 0 == iCopyType)
		screen.addPullDownString("CopyType", CyTranslator().getText("TXT_KEY_SPACE_SHIP_SCREEN_TYPE_BUTTON", ()), 1, 1, 1 == iCopyType)
		screen.addPullDownString("CopyType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT_COMBAT", ()), 2, 2, 2 == iCopyType)
		screen.addPullDownString("CopyType", CyTranslator().getText("TXT_KEY_PEDIA_DOMAIN", ()), 3, 3, 3 == iCopyType)
		screen.addPullDownString("CopyType", CyTranslator().getText("TXT_KEY_WB_GROUP", ()), 4, 4, 4 == iCopyType)

		screen.addDropDownBoxGFC("PlotType", 20, 80, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlotType", CyTranslator().getText("TXT_KEY_WB_SINGLE_PLOT", ()), 0, 0, iPlotType == 0)
		screen.addPullDownString("PlotType", CyTranslator().getText("TXT_KEY_WB_AREA_PLOTS", ()), 1, 1, iPlotType == 1)
		screen.addPullDownString("PlotType", CyTranslator().getText("TXT_KEY_WB_ALL_PLOTS", ()), 2, 2, iPlotType == 2)

		screen.addDropDownBoxGFC("CurrentPage", 20, screen.getYResolution() - 42, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_UNIT_DATA", ()), 0, 0, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ()), 1, 1, True)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA", ()), 2, 2, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_TEAM_DATA", ()), 3, 3, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLOT_DATA", ()), 4, 4, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_CONCEPT_EVENTS", ()), 5, 5, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()) + " + " + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()), 6, 6, False)
		screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_INFO_SCREEN", ()), 11, 11, False)

		screen.addDropDownBoxGFC("CombatClass", iWidth + 40, self.iTable_Y - 30, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CombatClass", CyTranslator().getText("TXT_KEY_WB_CITY_ALL",()), -2, -2, -2 == iSelectedClass)
		for iCombatClass in xrange(gc.getNumUnitCombatInfos()):
			screen.addPullDownString("CombatClass", gc.getUnitCombatInfo(iCombatClass).getDescription(), iCombatClass, iCombatClass, iCombatClass == iSelectedClass)

		sText = u"<font=3b>" + CyTranslator().getText("TXT_KEY_WB_COPY_ALL", (CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()),)) + "</font>"
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if bApplyAll:
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setText("ApplyAll", "Background", sColor + sText + "</color>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 20, self.iTable_Y - 60, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		sText = u"<font=3b>" + CyTranslator().getText("TXT_KEY_PEDIA_HIDE_INACTIVE", ()) + "</font>"
		sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
		if CvPlatyBuilderScreen.bHideInactive:
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setText("HideInactive", "Background", sColor + sText + "</color>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 20, self.iTable_Y - 80, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addDropDownBoxGFC("ChangeType", screen.getXResolution() - 120, self.iTable_Y - 30, 100, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_MODIFY", ("",)), 2, 2, 2 == iChangeType)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_ADD", ()), 1, 1, 1 == iChangeType)
		screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_REMOVE", ()), 0, 0, 0 == iChangeType)
		sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + " (+/-)</color></font>"
		screen.setText("PromotionAll", "Background", sText, CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 120, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		self.sortUnits()
		self.sortPromotions()

	def sortUnits(self):
		screen = CyGInterfaceScreen( "WBPromotionScreen", CvScreenEnums.WB_PROMOTION)
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
		screen = CyGInterfaceScreen( "WBPromotionScreen", CvScreenEnums.WB_PROMOTION)

		iMaxRows = (screen.getYResolution() - self.iTable_Y - 42) /24
		iWidth = screen.getXResolution()/5 - 20
		iHeight = iMaxRows * 24 + 2
		screen.addTableControlGFC("WBCurrentUnit", 3, 20, self.iTable_Y, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
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

	def sortPromotions(self):
		screen = CyGInterfaceScreen( "WBPromotionScreen", CvScreenEnums.WB_PROMOTION)
		global lList
		lList = []
		for i in xrange(gc.getNumPromotionInfos()):
			ItemInfo = gc.getPromotionInfo(i)
			if CvPlatyBuilderScreen.bHideInactive and not isPromotionValid(i, pUnit.getUnitType(), True): continue
			if iSelectedClass == -2 or ItemInfo.getUnitCombat(iSelectedClass):
				lList.append([ItemInfo.getDescription(), i])
		lList.sort()
		self.placePromotions()

	def placePromotions(self):
		screen = CyGInterfaceScreen( "WBPromotionScreen", CvScreenEnums.WB_PROMOTION)
		iMaxRows = (screen.getYResolution() - self.iTable_Y - 42) /24
		nColumns = max(1, min(4, (len(lList) + iMaxRows - 1)/iMaxRows))
		iHeight = iMaxRows * 24 + 2
		iWidth = screen.getXResolution() * 4/5 - 40
		screen.addTableControlGFC( "WBPromotion", nColumns, screen.getXResolution()/5 + 20, self.iTable_Y, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		for i in xrange(nColumns):
			screen.setTableColumnHeader("WBPromotion", i, "", iWidth/nColumns)

		nRows = (len(lList) + nColumns - 1) / nColumns
		for i in xrange(nRows):
			screen.appendTableRow("WBPromotion")

		for iCount in xrange(len(lList)):
			item = lList[iCount]
			iRow = iCount % nRows
			iColumn = iCount / nRows
			ItemInfo = gc.getPromotionInfo(item[1])
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if pUnit.isHasPromotion(item[1]):
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			screen.setTableText("WBPromotion", iColumn, iRow, "<font=3>" + sColor + item[0] + "</font></color>", ItemInfo.getButton(), WidgetTypes.WIDGET_PYTHON, 7873, item[1], CvUtil.FONT_LEFT_JUSTIFY )

	def handleInput (self, inputClass):
		screen = CyGInterfaceScreen( "WBPromotionScreen", CvScreenEnums.WB_PROMOTION)
		global bApplyAll
		global iChangeType
		global iPlotType
		global iCopyType
		global iOwnerType
		global iSelectedClass

		if inputClass.getFunctionName() == "CurrentPage":
			iIndex = screen.getPullDownData("CurrentPage", screen.getSelectedPullDownID("CurrentPage"))
			if iIndex == 0:
				WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).interfaceScreen(pUnit)
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

		elif inputClass.getFunctionName() == "ChangeType":
			iChangeType = screen.getPullDownData("ChangeType", screen.getSelectedPullDownID("ChangeType"))

		elif inputClass.getFunctionName() == "OwnerType":
			iOwnerType = screen.getPullDownData("OwnerType", screen.getSelectedPullDownID("OwnerType"))
			self.sortUnits()

		elif inputClass.getFunctionName() == "PlotType":
			iPlotType = screen.getPullDownData("PlotType", screen.getSelectedPullDownID("PlotType"))
			self.sortUnits()

		elif inputClass.getFunctionName() == "CopyType":
			iCopyType = screen.getPullDownData("CopyType", screen.getSelectedPullDownID("CopyType"))
			self.sortUnits()

		elif inputClass.getFunctionName() == "WBCurrentUnit":
			iPlayer = inputClass.getData1() - 8300
			self.interfaceScreen(gc.getPlayer(iPlayer).getUnit(inputClass.getData2()))

		elif inputClass.getFunctionName() == "CombatClass":
			iSelectedClass = screen.getPullDownData("CombatClass", screen.getSelectedPullDownID("CombatClass"))
			self.sortPromotions()

		elif inputClass.getFunctionName() == "WBPromotion":
			self.editPromotion(inputClass.getData2())
			self.placePromotions()

		elif inputClass.getFunctionName() == "PromotionAll":
			for item in lList:
				self.editPromotion(item[1])
			self.placePromotions()

		elif inputClass.getFunctionName() == "ApplyAll":
			bApplyAll = not bApplyAll
			sText = u"<font=3b>" + CyTranslator().getText("TXT_KEY_WB_COPY_ALL", (CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()),)) + "</font>"
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if bApplyAll:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			screen.modifyString("ApplyAll", sColor + sText + "</color>", 0)

		elif inputClass.getFunctionName() == "HideInactive":
			CvPlatyBuilderScreen.bHideInactive = not CvPlatyBuilderScreen.bHideInactive
			CvPlatyBuilderScreen.CvWorldBuilderScreen().refreshSideMenu()
			sText = u"<font=3b>" + CyTranslator().getText("TXT_KEY_PEDIA_HIDE_INACTIVE", ()) + "</font>"
			sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if CvPlatyBuilderScreen.bHideInactive:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			screen.setText("HideInactive", "Background", sColor + sText + "</color>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 20, self.iTable_Y - 80, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			self.sortPromotions()

		return 1

	def editPromotion(self, item):
		iType = iChangeType
		if bApplyAll:
			for i in lUnits:
				loopUnit = gc.getPlayer(i[0]).getUnit(i[1])
				if loopUnit.isNone(): continue
				if iChangeType == 2:
					iType = not loopUnit.isHasPromotion(item)
				self.doEffects(loopUnit, item, iType)
		else:
			if iChangeType == 2:
				iType = not pUnit.isHasPromotion(item)
			self.doEffects(pUnit, item, iType)

	def doEffects(self, pUnit, item, bAdd):
		bEffects = False
		if bAdd and CvPlatyBuilderScreen.bPython and not pUnit.isHasPromotion(item):
			bEffects = True
		pUnit.setHasPromotion(item, bAdd)
		if bEffects:
			CvEventManager.CvEventManager().onUnitPromoted([pUnit, item])

	def update(self, fDelta):
		return 1