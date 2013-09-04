# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005

#
# Sevopedia 2.3
#   sevotastic.blogspot.com
#   sevotastic@yahoo.com
#
# additional work by Gaurav, Progor, Ket, Vovan, Fitchn, LunarMongoose
# see ReadMe for details
#

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import SevoScreenEnums

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class SevoPediaUnitChart:

	def __init__(self, main):
		self.iGroup = -1
		self.top = main

		self.MARGIN = 20
		self.X_UNITS = self.top.X_PEDIA_PAGE
		self.Y_UNITS = self.top.Y_PEDIA_PAGE
		self.W_UNITS = self.top.W_PEDIA_PAGE
		self.H_UNITS = self.top.H_PEDIA_PAGE
		self.DY_UNITS = 40
		self.Y_TEXT_MARGIN = 6



	def interfaceScreen(self, iGroup):
		self.iGroup = iGroup
		screen = self.top.getScreen()
		self.placeUnitTable()



	def placeUnitTable(self):
		screen = self.top.getScreen()

		screen.addPanel(self.top.getNextWidgetName(), "", "", True, True, self.X_UNITS, self.Y_UNITS, self.W_UNITS, self.H_UNITS, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", True, True, self.X_UNITS + self.MARGIN, self.Y_UNITS + self.MARGIN, self.W_UNITS - (self.MARGIN * 2), self.H_UNITS - (self.MARGIN * 2), PanelStyles.PANEL_STYLE_BLUE50)
		szTable = self.top.getNextWidgetName()
		screen.addTableControlGFC(szTable, 4, self.X_UNITS + self.MARGIN, self.Y_UNITS + self.MARGIN + 5, self.W_UNITS - (self.MARGIN * 2), self.H_UNITS - (self.MARGIN * 2) - 5, True, False, 32,32, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSort(szTable)
		iTableWidth = self.W_UNITS - (self.MARGIN * 2)
		iColWidth = int(iTableWidth * (7 / 19.0))
		screen.setTableColumnHeader(szTable, 0, "", iColWidth)
		iColWidth = int(iTableWidth * (4 / 19.0))
		screen.setTableColumnHeader(szTable, 1, u"%c" % CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR), iColWidth)
		screen.setTableColumnHeader(szTable, 2, u"%c" % CyGame().getSymbolID(FontSymbols.MOVES_CHAR), iColWidth)
		screen.setTableColumnHeader(szTable, 3, u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar(), iColWidth)
		nUnits = 0
		for j in range(gc.getNumUnitInfos()):
			if (self.iGroup == gc.getUnitInfo(j).getUnitCombatType() or self.iGroup == gc.getNumUnitCombatInfos()):
				nUnits += 1
		dy = self.DY_UNITS
		yTextMargin = self.Y_TEXT_MARGIN
		if (self.iGroup == gc.getNumUnitCombatInfos()):
			dy = self.DY_UNITS/2
			yTextMargin = 0
		i = 0
		unitsList=[(0,0,0,0,0)]*nUnits
		for j in range(gc.getNumUnitInfos()):
			if (self.iGroup == gc.getUnitInfo(j).getUnitCombatType() or self.iGroup == gc.getNumUnitCombatInfos()):
				if (gc.getUnitInfo(j).getProductionCost() < 0):
					szCost = localText.getText("TXT_KEY_NON_APPLICABLE", ())
				else:
					szCost = unicode(gc.getUnitInfo(j).getProductionCost())# + u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()
				unitsList[i] = (gc.getUnitInfo(j).getCombat(), gc.getUnitInfo(j).getMoves(), szCost, gc.getUnitInfo(j).getDescription(), j)
				i += 1
		for i in range(nUnits):			
			iRow = screen.appendTableRow(szTable)
			screen.setTableText(szTable, 0, iRow, u"<font=3>" + unitsList[i][3] + u"</font>", "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, unitsList[i][4], 1, CvUtil.FONT_LEFT_JUSTIFY)	
			screen.setTableInt(szTable, 1, iRow, u"<font=3>" + unicode(unitsList[i][0]) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableInt(szTable, 2, iRow, u"<font=3>" + unicode(unitsList[i][1]) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableInt(szTable, 3, iRow, u"<font=3>" + unicode(unitsList[i][2]) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput (self, inputClass):
		return 0
