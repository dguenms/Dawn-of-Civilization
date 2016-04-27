from CvPythonExtensions import *
import CvUtil

gc = CyGlobalContext()



class CvPediaUnitChart:
	def __init__(self, main):
		self.iGroup = -1
		self.top = main

		self.X_TABLE = self.top.X_PEDIA_PAGE
		self.Y_TABLE = self.top.Y_PEDIA_PAGE
		self.W_TABLE = self.top.W_PEDIA_PAGE
		self.H_TABLE = self.top.H_PEDIA_PAGE



	def interfaceScreen(self, iGroup):
		self.iGroup = iGroup
		self.placeUnitTable()



	def placeUnitTable(self):
		screen = self.top.getScreen()
		table = self.top.getNextWidgetName()

		nColumns = 7
		screen.addTableControlGFC(table, nColumns, self.X_TABLE, self.Y_TABLE, self.W_TABLE, self.H_TABLE, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.setStyle(table, "Table_StandardCiv_Style")
		screen.enableSort(table)

		if self.iGroup == gc.getInfoTypeForString('UNITCOMBAT_AIR'):
			szMove = "Range"
		else:
			szMove = "Moves"

		if self.iGroup == gc.getInfoTypeForString('UNITCOMBAT_AIR') or self.iGroup == gc.getInfoTypeForString('UNITCOMBAT_NAVAL') or self.iGroup == gc.getInfoTypeForString('UNITCOMBAT_SIEGE'):
			szSpecial = "Bombard"
		else:
			szSpecial = "1st Strike"

		if self.iGroup == gc.getInfoTypeForString('UNITCOMBAT_AIR'):
			szWithdraw = "Evade"
		else:
			szWithdraw = "Withdraw"

		iWidth = ((self.W_TABLE - 180) / (nColumns - 1))
		screen.setTableColumnHeader(table, 0, u"<font=2>" + gc.getUnitCombatInfo(self.iGroup).getDescription() + "</font>", 182)
		screen.setTableColumnHeader(table, 1, u"<font=2>" + "Strength" + "</font>", iWidth)
		screen.setTableColumnHeader(table, 2, u"<font=2>" + szMove + "</font>", iWidth)
		screen.setTableColumnHeader(table, 3, u"<font=2>" + szSpecial + "</font>", iWidth)
		screen.setTableColumnHeader(table, 4, u"<font=2>" + "Collateral" + "</font>", iWidth)
		screen.setTableColumnHeader(table, 5, u"<font=2>" + szWithdraw + "</font>", iWidth)
		screen.setTableColumnHeader(table, 6, u"<font=2>" + "Cost" + "</font>", iWidth)

		for iUnit in xrange(gc.getNumUnitInfos()):
			UnitInfo = gc.getUnitInfo(iUnit)
			if self.iGroup == UnitInfo.getUnitCombatType():
				iRow = screen.appendTableRow(table)

				# Name
				iCol = 0
				screen.setTableText(table, iCol, iRow, u"<font=3>" + UnitInfo.getDescription() + u"</font>", UnitInfo.getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, CvUtil.FONT_LEFT_JUSTIFY)

				# Combat Strength
				iCol += 1
				if UnitInfo.getAirCombat() > 0:
					szCombat = u"%d" % UnitInfo.getAirCombat()
				else:
					szCombat = u"%d" % UnitInfo.getCombat()

				screen.setTableInt(table, iCol, iRow, u"<font=3>" + szCombat + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

				# Movement
				iCol += 1
				if UnitInfo.getAirRange() > 0:
					szMoves = u"%d" % UnitInfo.getAirRange()
				else:
					szMoves = u"%d" % UnitInfo.getMoves()

				screen.setTableInt(table, iCol, iRow, u"<font=3>" + szMoves + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

				# Bombard/First Strikes
				iCol += 1
				if UnitInfo.getBombardRate() > 0:
					szBombard = u"%d%%" % UnitInfo.getBombardRate()
				elif UnitInfo.getBombRate() > 0:
					szBombard = u"%d%%" % UnitInfo.getBombRate()
				elif UnitInfo.getFirstStrikes() > 0 and not (self.iGroup == gc.getInfoTypeForString('UNITCOMBAT_AIR') or self.iGroup == gc.getInfoTypeForString('UNITCOMBAT_NAVAL') or self.iGroup == gc.getInfoTypeForString('UNITCOMBAT_SIEGE')):
					szBombard = u"%d" % UnitInfo.getFirstStrikes()
				else:
					szBombard = u""

				screen.setTableInt(table, iCol, iRow, u"<font=3>" + szBombard + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

				# Collateral
				iCol += 1
				if UnitInfo.getCollateralDamage() > 0:
					szCollateral = u"%d%% (%d)" % (UnitInfo.getCollateralDamageLimit(), UnitInfo.getCollateralDamageMaxUnits())
				else:
					szCollateral = u""

				screen.setTableInt(table, iCol, iRow, u"<font=3>" + szCollateral + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

				# Withdrawal
				iCol += 1
				if self.iGroup == gc.getInfoTypeForString('UNITCOMBAT_AIR') and UnitInfo.getEvasionProbability() > 0:
					szWithdrawal = u"%d%%" % UnitInfo.getEvasionProbability()
				elif UnitInfo.getWithdrawalProbability() > 0:
					szWithdrawal = u"%d%%" % UnitInfo.getWithdrawalProbability()
				else:
					szWithdrawal = u""

				screen.setTableInt(table, iCol, iRow, u"<font=3>" + szWithdrawal + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

				# Cost
				iCol += 1
				if UnitInfo.getProductionCost() < 0:
					szCost = CyTranslator().getText("TXT_KEY_NON_APPLICABLE", ())
				else:
					szCost = u"%d" % UnitInfo.getProductionCost()

				screen.setTableInt(table, iCol, iRow, u"<font=3>" + szCost + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)



	def handleInput(self, inputClass):
		return 0
