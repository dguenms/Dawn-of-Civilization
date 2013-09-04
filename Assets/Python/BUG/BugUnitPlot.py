## Unit Plot List Utilities
##
## Holds the information used to display the unit plot list
##
## Copyright (c) 2007-2009 The BUG Mod.
##
## Author: Ruff_Hi

from CvPythonExtensions import *
import MonkeyTools as mt
import BugUtil
import UnitUtil

import BugCore
PleOpt = BugCore.game.PLE

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

sBupStringBase = "BUGUnitPlotString"
cBupCellSize = 34
cBupCellSpacing = 3

class BupPanel:
	def __init__(self, screen, xRes, yRes, iMulti, iVanCols, iVanRows):
		self.CellSpacing = cBupCellSpacing
		self.MaxCells = iVanCols * iVanRows
		self.Rows = iVanRows
		self.Cols = iVanCols

#		BugUtil.debug("BupPanel %i %i %i", yRes, iVanCols, iVanRows)

		self.screen = screen

		# we scrapped the panel concept
		# initially, the thought was to put everything on a single panel and then just show / hide
		# the panel for quick showing and hiding
		# however, some of the graphics aren't attached to anything so we just went with throwing them
		# straight onto the main interface screen

		# however, the panel location values are still used to help locate the cells
		# SO DON'T DELETE THEM!
		self.xPanel = 315 - cBupCellSpacing
		self.yPanel = yRes - 169 + (1 - iVanRows) * cBupCellSize - cBupCellSpacing
		self.wPanel = iVanCols * cBupCellSize + cBupCellSpacing
		self.hPanel = iVanRows * cBupCellSize + cBupCellSpacing

#		BugUtil.debug("BupPanel %i %i %i %i", self.xPanel, self.yPanel, self.wPanel, self.hPanel)

		sTexture = getArt("INTERFACE_BUTTONS_GOVERNOR")
		sHiLiteTexture = getArt("BUTTON_HILITE_SQUARE")
		sPromoFrame = getArt("OVERLAY_PROMOTION_FRAME")

		self.BupCell_Displayed = []

		for iIndex in range(self.MaxCells):
			szBupCell = self._getCellWidget(iIndex)
			iX = self._getX(self._getCol(iIndex))
			iY = self._getY(self._getRow(iIndex))

#			BugUtil.debug("BupPanel MaxCells %i %i %i %i %i", iIndex, self._getCol(iIndex), self._getRow(iIndex), self._getX(self._getCol(iIndex)), self._getY(self._getRow(iIndex)))

			# place/init the promotion frame.
			# Important to have it at first place within the for loop
			# so that it sits behind the unit icon button
			szStringPromoFrame = szBupCell + "PromoFrame"
			screen.addDDSGFC(szStringPromoFrame, sPromoFrame, iX, iY, 32, 32, WidgetTypes.WIDGET_GENERAL, iIndex, -1 )
			screen.hide(szStringPromoFrame)


			# unit icon
			screen.addCheckBoxGFC(szBupCell, sTexture, sHiLiteTexture, iX, iY, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, iIndex, -1, ButtonStyles.BUTTON_STYLE_LABEL)
			screen.hide(szBupCell)

			# health bar
			szStringHealth = szBupCell + "Health"
			screen.addStackedBarGFC(szStringHealth, iX, iY + 23, 32, 11, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, iIndex, -1 )
			screen.hide(szStringHealth)

			self.BupCell_Displayed.append(False)


#VOID addDDSGFC(STRING szName, STRING szTexture, INT iX, INT iY, INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1, INT iData2)
#VOID addDDSGFCAt(STRING szName, STRING szAttachTo, STRING szTexture, INT iX, INT iY, INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1, INT iData2, BOOL bOption)
#VOID addCheckBoxGFC(STRING szName, STRING szTexture, STRING szHiliteTexture, INT iX, INT iY, INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1, INT iData2, ButtonStyle eStyle)
#VOID addCheckBoxGFCAt(STRING szName, STRING szTexture, STRING szHiliteTexture, INT iX, INT iY, INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1, INT iData2, ButtonStyle eStyle)
#VOID attachCheckBoxGFC(STRING szAttachTo, STRING szName, STRING szTexture, STRING szHiliteTexture, INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1, INT iData2, ButtonStyle eStyle)
#VOID addStackedBarGFC(STRING szName, INT iX, INT iY, INT iWidth, INT iHeight, INT iNumBars, WidgetType eWidgetType, INT iData1, INT iData2)



		# the little white arrows?
		screen.setButtonGFC(sBupStringBase + "Minus", u"", "", 315 + (xRes - (iMulti) - 68), yRes - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT)
		screen.setButtonGFC(sBupStringBase + "Plus", u"", "",  298 + (xRes - (iMulti) - 34), yRes - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT)
		screen.hide(sBupStringBase + "Minus")
		screen.hide(sBupStringBase + "Plus")

		self.BupUnits = []
		self.BupUnits_Prior = []

		self.PlotListOffset = 0
		self.PlotListOffset_Prior = 0
		self.PlotListColumn_Prior = 0

		self.PlotX_Prior = 0
		self.PlotY_Prior = 0
		self.PlotX = 0
		self.PlotY = 0

		self.CityUp_Prior = False

	def Draw(self):

		BugUtil.debug("BupPanel Draw")

		# set L+R arrows to 'off'
		bLeftArrow = False
		bRightArrow = False
		self.screen.hide(sBupStringBase + "Minus")
		self.screen.hide(sBupStringBase + "Plus")

		# kill off the prior units and delete all of the unit plot list if the plot has changed
		if (self._hasPlotChanged()
		or CyInterface().isCityScreenUp() != self.CityUp_Prior):
#			BugUtil.debug("BupPanel plot has changed or CityScreenUp status has changed - %s %s", CyInterface().isCityScreenUp(), self.CityUp_Prior)
			self.BupUnits_Prior = []
			self.PlotListOffset_Prior = 0
			self.PlotListColumn_Prior = 0
			self.Hide()

		# store the unit plot offset
		self.PlotListOffset = CyInterface().getPlotListOffset()

# todo: still need to put in something to handle the column value (ie when you have more units that can fit on the screen)

		iVisibleUnits = CyInterface().getNumVisibleUnits()
		iIndex = -(CyInterface().getPlotListColumn())

		if (CyInterface().isCityScreenUp()):
			iMaxRows = 1
			iSkippedCells = (self._getMaxRows() - 1) * self._getMaxCols()
			iIndex += iSkippedCells
			iFirstPlot = iSkippedCells
			iLastPlot = iFirstPlot + self._getMaxCols() - 1
		else:
			iMaxRows = self._getMaxRows()
			iSkippedCells = 0
			iIndex += self.PlotListOffset
			iFirstPlot = 0
			iLastPlot = self._getMaxRows() * self._getMaxCols() - 1

		iMaxUnits = max(len(self.BupUnits), \
						len(self.BupUnits_Prior))

#		iMaxUnits = min(iMaxUnits, \
#						iMaxRows * self._getMaxCols())

		BugUtil.debug("BupPanel rows(%i), cols(%i), cells(%i)", self._getMaxRows(), self._getMaxCols(), iMaxRows * self._getMaxCols())
		BugUtil.debug("BupPanel units_c(%i) units_p(%i), units max(%i)", len(self.BupUnits), len(self.BupUnits_Prior), iMaxUnits)
		BugUtil.debug("BupPanel max rows(%i), skipped(%i), index(%i)", iMaxRows, iSkippedCells, iIndex)
		BugUtil.debug("BupPanel plotlistoffset, current(%i), prior(%i)", self.PlotListOffset, self.PlotListOffset_Prior)
		BugUtil.debug("BupPanel plotlistcolumn, current(%i), prior(%i)", CyInterface().getPlotListColumn(), self.PlotListColumn_Prior)
		BugUtil.debug("BupPanel first(%i), last(%i)", iFirstPlot, iLastPlot)




# put in an override if the number of units exceeds the screen maximum
# or if the city screen is up (max = units per row)
# also need some code to control those pesky little arrows

		for iUnit in range(iMaxUnits):
			iUnit_Prior = iUnit - (CyInterface().getPlotListColumn() - self.PlotListColumn_Prior)
			BugUtil.debug("BupPanel index(%i), iUnit(%i), iUnit_Prior(%i)", iIndex, iUnit, iUnit_Prior)

			# check if the unit we have is within the display bounds
			if (iIndex < iFirstPlot
			or iIndex > iLastPlot):
				iIndex += 1
				continue

			szBupCell = self._getCellWidget(iIndex)

			if iUnit < len(self.BupUnits):
				BupUnit = self.BupUnits[iUnit]
			else:
				# current unit is blank!
				self._hideCell(iIndex, szBupCell)
				iIndex += 1
				continue

			# do we have to turn the arrows on?
			if iIndex == iFirstPlot: # looking at the top left cell
				if CyInterface().getPlotListColumn() > 0: # still have units to show
					bLeftArrow = True
			elif iIndex == iLastPlot: # the bottom right cell
				if (iVisibleUnits - iIndex - CyInterface().getPlotListColumn() + iSkippedCells) > 1: # more units to show to right
					bRightArrow = True

			# prior unit doesn't exist - just need to draw the new unit
			# this is handled below in the '_update*' functions
			if (len(self.BupUnits_Prior) != 0
			and iUnit_Prior >= 0
			and iUnit_Prior < len(self.BupUnits_Prior)):
#			or  iUnit_Prior < len(self.BupUnits_Prior))):
				BupUnit_Prior = self.BupUnits_Prior[iUnit_Prior]
			else:
				BupUnit_Prior = None

			self._updateUnitIcon(BupUnit, BupUnit_Prior, iIndex, szBupCell)

			iX = self._getX(self._getCol(iIndex))
			iY = self._getY(self._getRow(iIndex))

			BugUtil.debug("BupPanel unit(%i), index(%i), col(%i), row(%i), x(%i), y(%i)", iUnit, iIndex, self._getCol(iIndex), self._getRow(iIndex), iX, iY)

			if BupUnit.Owner == gc.getGame().getActivePlayer():
				self._updatePromo(BupUnit, BupUnit_Prior, szBupCell)
				self._updateUpgrade(BupUnit, BupUnit_Prior, szBupCell, iIndex, iX, iY)
				self._updateMission(BupUnit, BupUnit_Prior, szBupCell, iIndex, iX, iY)

			# the health bar and dot are shown for all units
			# not just the current player's units
			self._updateDot(BupUnit, BupUnit_Prior, szBupCell, iIndex, iX, iY + 4)
			self._updateHealthBar(BupUnit, BupUnit_Prior, szBupCell)

			iIndex += 1


		# phew, finally finished all the units
		# do we have to show the arrows?
		# only if there are more visible units than there are cells
		if iVisibleUnits > iMaxRows * self._getMaxCols():
			self.screen.enable(sBupStringBase + "Minus", bLeftArrow)
			self.screen.enable(sBupStringBase + "Plus", bRightArrow)
			self.screen.show(sBupStringBase + "Minus")
			self.screen.show(sBupStringBase + "Plus")

		# save the current units for next time
#		self.BupUnits_Prior = self.BupUnits
		self.BupUnits_Prior = []
		for iUnit in range(len(self.BupUnits)):
			self.BupUnits_Prior.append(self.BupUnits[iUnit])

		# empty the current units
		# maininterface will reload them prior to calling .Draw()
		self.BupUnits = []

		# save prior stuff
		self.CityUp_Prior = CyInterface().isCityScreenUp()
		self.PlotListOffset_Prior = CyInterface().getPlotListOffset()
		self.PlotListColumn_Prior = CyInterface().getPlotListColumn()


############## plot ##############

	def addPlot(self, X, Y):
#		BugUtil.debug("BupPanel addPlot 1) %i %i %i %i", self.PlotX, self.PlotY, self.PlotX_Prior, self.PlotY_Prior)
		self.PlotX_Prior = self.PlotX
		self.PlotY_Prior = self.PlotY
		self.PlotX = X
		self.PlotY = Y
#		BugUtil.debug("BupPanel addPlot 2) %i %i %i %i", self.PlotX, self.PlotY, self.PlotX_Prior, self.PlotY_Prior)

	def _hasPlotChanged(self):
#		BugUtil.debug("BupPanel _hasPlotChanged %i %i %i %i %s", self.PlotX, self.PlotY, self.PlotX_Prior, self.PlotY_Prior, not (self.PlotX == self.PlotX_Prior and self.PlotY == self.PlotY_Prior))
		return not (self.PlotX == self.PlotX_Prior and self.PlotY == self.PlotY_Prior)


############## hide ##############

	def Hide(self):
#		BugUtil.debug("BupPanel Hide!")
		iIndex = 0
		while iIndex < self.MaxCells:
			self._hideCell(iIndex, self._getCellWidget(iIndex))
			iIndex += 1

	def _hideCell(self, iIndex, szCell):
		if self.BupCell_Displayed[iIndex]:
#			BugUtil.debug("BupPanel hiding %i", iIndex)

			self.screen.hide(szCell)
			self.screen.hide(szCell + "Dot")
			self.screen.hide(szCell + "PromoFrame")
			self.screen.hide(szCell + "Upgrade")
			self.screen.hide(szCell + "Mission")
			self.screen.hide(szCell + "Health")

			self.BupCell_Displayed[iIndex] = False


############## add and clear units ##############

	def addUnit(self, pUnit):
		self.BupUnits.append(BupUnit(pUnit))

	def clearUnits(self):
		self.BupUnits = []
		self.BupUnits_Prior = []



############## unit icon ##############

	def _updateUnitIcon(self, BupUnit, BupUnit_Prior, iIndex, szCell):
		# note that 'State' is always updated as the unit icon is a check box
		# and clicking on a check box changes the display state, even if the unit state is unchanged
		# ie ctrl-click on a selected unit should highlight all of that type of unit
		# but if we don't update the state, then the highlighted unit would show as unselected (turned off by the click)
		if BupUnit_Prior is None:
			self._drawUnitIcon(BupUnit, iIndex, szCell)
			self.screen.setState(szCell, BupUnit.isSelected)
			return

#		BugUtil.debug("BupPanel _updateUnitIcon %s %s", BupUnit.isSelected, BupUnit_Prior.isSelected)

		# if we get to here, then we have a unit in BupUnit and BupUnit_Prior
		if (BupUnit.UnitType	!= BupUnit_Prior.UnitType
		or BupUnit.Owner		!= BupUnit_Prior.Owner):
			self._drawUnitIcon(BupUnit, iIndex, szCell)

		if self.BupCell_Displayed[iIndex]:
			self.screen.setState(szCell, BupUnit.isSelected)

	def _drawUnitIcon(self, BupUnit, iIndex, szCell):
		self.screen.changeImageButton(szCell, gc.getUnitInfo(BupUnit.UnitType).getButton())
		self.screen.enable(szCell, BupUnit.Owner == gc.getGame().getActivePlayer())
		self.screen.show(szCell)
#		self.screen.setState(szCell, BupUnit.isSelected)

		self.BupCell_Displayed[iIndex] = True


############## dot (or star for GG) ##############

	def _updateDot(self, BupUnit, BupUnit_Prior, szCell, iCount, x, y):
		if BupUnit_Prior is None:
			self._drawDot(BupUnit, szCell, iCount, x, y)
			return

		# if we get to here, then we have a unit in BupUnit and BupUnit_Prior
		if BupUnit.DotStatus != BupUnit_Prior.DotStatus:
			self._drawDot(BupUnit, szCell, iCount, x, y)

	def _drawDot(self, BupUnit, szCell, iCount, x, y):
		# handles the display of the colored buttons in the upper left corner of each unit icon.
		# Units lead by a GG will get a star instead of a dot - and the location and size of star differs
		if (PleOpt.isShowGreatGeneralIndicator()
		and BupUnit.isLeadByGreatGeneral):
			xSize = 16
			ySize = 16
			xOffset = -3
			yOffset = -3
		else:
			xSize = 12
			ySize = 12
			xOffset = 0
			yOffset = 0

		# display the colored spot icon
		self.screen.addDDSGFC(szCell + "Dot", getArt(BupUnit.DotStatus), x-3+xOffset, y-7+yOffset, xSize, ySize, WidgetTypes.WIDGET_GENERAL, iCount, -1 )


############## promotion available ##############

	def _updatePromo(self, BupUnit, BupUnit_Prior, szCell):
		if BupUnit_Prior is None:
			self._drawPromo(BupUnit, szCell)
			return

		# if we get to here, then we have a unit in BupUnit and BupUnit_Prior
		if BupUnit.isPromotionReady != BupUnit_Prior.isPromotionReady:
			self._drawPromo(BupUnit, szCell)

	def _drawPromo(self, BupUnit, szCell):
		if PleOpt.isShowPromotionIndicator():
			if BupUnit.isPromotionReady:
				self.screen.show(szCell + "PromoFrame")
			else:
				self.screen.hide(szCell + "PromoFrame")


############## upgrade ##############

	def _updateUpgrade(self, BupUnit, BupUnit_Prior, szCell, iCount, x, y):
		if BupUnit_Prior is None:
			self._drawUpgrade(BupUnit, szCell, iCount, x, y)
			return

		# if we get to here, then we have a unit in BupUnit and BupUnit_Prior
		if BupUnit.isCanUpgrade != BupUnit_Prior.isCanUpgrade:
			self._drawUpgrade(BupUnit, szCell, iCount, x, y)

	def _drawUpgrade(self, BupUnit, szCell, iCount, x, y):
		if (BupUnit.isCanUpgrade):
			# place the upgrade arrow
			self.screen.addDDSGFC(szCell + "Upgrade", getArt("OVERLAY_UPGRADE"), x+2, y+14, 8, 16, WidgetTypes.WIDGET_GENERAL, iCount, -1 )
		else:
			self.screen.hide(szCell + "Upgrade")


############## mission ##############

	def _updateMission(self, BupUnit, BupUnit_Prior, szCell, iCount, x, y):
		if BupUnit_Prior is None:
			self._drawMission(BupUnit, szCell, iCount, x, y)
			return

		# if we get to here, then we have a unit in BupUnit and BupUnit_Prior
		if BupUnit.Mission != BupUnit_Prior.Mission:
			self._drawMission(BupUnit, szCell, iCount, x, y)

	def _drawMission(self, BupUnit, szCell, iCount, x, y):
		if PleOpt.isShowMissionInfo():
			if BupUnit.Mission != "":
				self.screen.addDDSGFC(szCell + "Mission", getArt(BupUnit.Mission), x+20, y+20, 12, 12, WidgetTypes.WIDGET_GENERAL, iCount, -1)
			else:
				self.screen.hide(szCell + "Mission")


############## health bar ##############

	def _updateHealthBar(self, BupUnit, BupUnit_Prior, szCell):
		if BupUnit_Prior is None:
			self._drawHealthBar(BupUnit, szCell)
			return

		# if we get to here, then we have a unit in BupUnit and BupUnit_Prior
		if (BupUnit.currHitPoints != BupUnit_Prior.currHitPoints
		or not BupUnit_Prior.isShowHealth):
			self._drawHealthBar(BupUnit, szCell)

	def _drawHealthBar(self, BupUnit, szCell):
		if (PleOpt.isShowHealthBar()
		and BupUnit.isShowHealth):
			if BupUnit.currHitPoints < (BupUnit.maxHitPoints * 2) / 3:
				sColor = "COLOR_RED"
			elif BupUnit.currHitPoints < BupUnit.maxHitPoints / 3:
				sColor = "COLOR_YELLOW"
			elif BupUnit.currHitPoints < BupUnit.maxHitPoints:
				sColor = "COLOR_PLAYER_LIGHT_GREEN"
			else:
				sColor = "COLOR_GREEN"

			szStringHealth = szCell + "Health"
			self.screen.setBarPercentage(szStringHealth, InfoBarTypes.INFOBAR_STORED, float(BupUnit.currHitPoints) / float(BupUnit.maxHitPoints))
			self.screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString(sColor))
			self.screen.show(szStringHealth)







	def _getMaxCols(self):
		return self.Cols

	def _getMaxRows(self):
		return self.Rows

	def _getMaxCells(self):
		return self.Rows

	def _getRow(self, i):
#		return self._getMaxRows() - i / self._getMaxCols() - 1
		return i / self._getMaxCols()

	def _getCol(self, i):
		return i % self._getMaxCols()

	def _getX(self, nCol): # measures from the top left of screen!
		return nCol * cBupCellSize + self.xPanel

	def _getY(self, nRow): # measures from the top left of screen!
		return nRow * cBupCellSize + self.yPanel

	def _getCellWidget(self, index):
		return sBupStringBase + "Cell" + str(index)

#	def _getIndex(self, nRow, nCol):
#		return ( nRow * self.getMaxCol() ) + ( nCol % self.getMaxCol() )

############## functions for visual objects (show and hide) ######################
		
	# PLE Grouping Mode Switcher 




class BupUnit:
	def __init__(self, pUnit):
		self.pUnit = pUnit

		# unit type
		self.UnitType = pUnit.getUnitType()
		self.Owner = pUnit.getOwner()
		self.isSelected = pUnit.IsSelected()
		self.isFortified = pUnit.getTeam() != gc.getGame().getActiveTeam() or pUnit.isWaiting()
		self.isMoved = pUnit.canMove() and pUnit.hasMoved()
		self.isMove = pUnit.canMove() and not pUnit.hasMoved()
		self.isNotMove = not pUnit.canMove()
		self.isHurt = pUnit.isHurt()
		self.isPromotionReady = pUnit.isPromotionReady()

		iLeaderPromo = gc.getInfoTypeForString('PROMOTION_LEADER')
		self.isLeadByGreatGeneral = iLeaderPromo != -1 and pUnit.isHasPromotion(iLeaderPromo)

		self.DotStatus = self._getDotStatus()
		self.Mission = self._getMission(pUnit)

		if PleOpt.isShowUpgradeIndicator():
			self.isCanUpgrade = mt.checkAnyUpgrade(pUnit)
		else:
			self.isCanUpgrade = False

		# health
		self.currHitPoints = pUnit.currHitPoints()
		self.maxHitPoints = pUnit.maxHitPoints()
		if (pUnit.isFighting()):
			self.isShowHealth = False
		elif (pUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
			self.isShowHealth = pUnit.canAirAttack()
		else:
			self.isShowHealth = pUnit.canFight()



#		self.isCanUpgrade = PleOpt.isShowUpgradeIndicator() or mt.checkAnyUpgrade(pUnit)

	def _getDotStatus(self):
		sDotStatus = ""
		if self.isFortified:  # fortified
			sDotStatus = "OVERLAY_FORTIFY"
		elif self.isMoved:  # unit moved, but some movement points are left
			sDotStatus = "OVERLAY_HASMOVED"
		elif self.isMove:  # unit did not move yet
			sDotStatus = "OVERLAY_MOVE"
		else: # unit has no movement points left
			sDotStatus = "OVERLAY_NOMOVE"

		# Wounded units will get a darker colored button.
		if (PleOpt.isShowWoundedIndicator()
		and self.isHurt):
			sDotStatus += "_INJURED"

		# Units lead by a GG will get a star instead of a dot.
		if (PleOpt.isShowGreatGeneralIndicator()
		and self.isLeadByGreatGeneral):
			sDotStatus += "_GG"

		return sDotStatus

	def _getMission(self, pUnit):
		eActivityType = pUnit.getGroup().getActivityType()
		eAutomationType = pUnit.getGroup().getAutomateType()

		# is unit on air intercept mission
		if (eActivityType == ActivityTypes.ACTIVITY_INTERCEPT):
			return "OVERLAY_ACTION_INTERCEPT"
		# is unit on boat patrol coast mission
		elif (eActivityType == ActivityTypes.ACTIVITY_PATROL):
			return "OVERLAY_ACTION_PATROL"
		# is unit on boat blockade mission
		elif (eActivityType == ActivityTypes.ACTIVITY_PLUNDER):
			return "OVERLAY_ACTION_PLUNDER"
		# is unit fortified for healing (wake up when healed)
		elif (eActivityType == ActivityTypes.ACTIVITY_HEAL):
			return "OVERLAY_ACTION_HEAL"
		# is unit sentry (wake up when enemy in sight)
		elif (eActivityType == ActivityTypes.ACTIVITY_SENTRY):
			return "OVERLAY_ACTION_SENTRY"
		# is the turn for this unit skipped (wake up next turn)
		elif (eActivityType == ActivityTypes.ACTIVITY_HOLD):
			return "OVERLAY_ACTION_SKIP"
		# has unit exploration mission
		elif (eAutomationType == AutomateTypes.AUTOMATE_EXPLORE):
			return "OVERLAY_ACTION_EXPLORE"
		# is unit automated generally (only worker units)
		elif (eAutomationType == AutomateTypes.AUTOMATE_BUILD):
			return "OVERLAY_ACTION_AUTO_BUILD"
		# is unit automated for nearest city (only worker units)
		elif (eAutomationType == AutomateTypes.AUTOMATE_CITY):
			return "OVERLAY_ACTION_AUTO_CITY"
		# is unit automated for network (only worker units)
		elif (eAutomationType == AutomateTypes.AUTOMATE_NETWORK):
			return "OVERLAY_ACTION_AUTO_NETWORK"
		# is unit automated spread religion (only missionary units)
		elif (eAutomationType == AutomateTypes.AUTOMATE_RELIGION):
			return "OVERLAY_ACTION_AUTO_RELIGION"
		# has unit a mission
		elif (pUnit.getGroup().getLengthMissionQueue() > 0):
			eMissionType = pUnit.getGroup().getMissionType(0)
			# is the mission to build an improvement
			if (eMissionType == MissionTypes.MISSION_BUILD):
				return "OVERLAY_ACTION_BUILD"
			# is the mission a "move to" mission
			elif (eMissionType in UnitUtil.MOVE_TO_MISSIONS):
				return "OVERLAY_ACTION_GOTO"
		# if nothing of above, but unit is waiting -> unit is fortified
		elif (pUnit.isWaiting()):
			if (pUnit.isFortifyable()):
				return "OVERLAY_ACTION_FORTIFY"
			else:
				return "OVERLAY_ACTION_SLEEP"

		return ""



#		self.bSelected = pUnit.IsSelected()
#		self.eUnit = pUnit.getUnitType()
#		self.sDotState, self.iDotxSize, self.iDotySize, self.iDotxOffset, self.iDotyOffset = _getDOTInfo(pUnit)
#		self.sMission = _getMission(pUnit)
#		self.bPromo = pUnit.isPromotionReady()
#		self.bGG = iLeaderPromo != -1 and pUnit.isHasPromotion(iLeaderPromo)
#		self.bUpgrade = mt.checkAnyUpgrade(pUnit)
#		self.icurrHitPoints = pUnit.currHitPoints()
#		self.imaxHitPoints = pUnit.maxHitPoints()
#		self.iMovesLeft = pUnit.movesLeft()
#		self.iMoves = pUnit.getMoves()








def getArt(sArt):
	return ArtFileMgr.getInterfaceArtInfo(sArt).getPath()




