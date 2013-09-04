from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvEventInterface

from AStarTools import *
import MonkeyTools as mt
import UnitUtil
import string

import PyHelpers 
PyPlayer = PyHelpers.PyPlayer

import BugUtil
import BugCore
PleOpt = BugCore.game.PLE

import BugUnitPlot

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

# MULTI LIST
#####################
iMultiListXL = 318
iMultiListXR = 332

class PLE:
	def __init__(self):
#	def PLE_initialize(self):

		# filter constants
		self.nPLEFilterModeCanMove		= 0x0001
		self.nPLEFilterModeCantMove		= 0x0002
		self.nPLEFilterModeWound		= 0x0004
		self.nPLEFilterModeNotWound		= 0x0008
		self.nPLEFilterModeAir 			= 0x0010
		self.nPLEFilterModeSea 			= 0x0020
		self.nPLEFilterModeLand			= 0x0040
		self.nPLEFilterModeDom			= 0x0080
		self.nPLEFilterModeMil			= 0x0100
		self.nPLEFilterModeOwn			= 0x0200
		self.nPLEFilterModeForeign		= 0x0400

		self.nPLEFilterGroupHealth		= self.nPLEFilterModeWound | self.nPLEFilterModeNotWound
		self.nPLEFilterGroupDomain		= self.nPLEFilterModeAir | self.nPLEFilterModeSea | self.nPLEFilterModeLand
		self.nPLEFilterGroupType		= self.nPLEFilterModeDom | self.nPLEFilterModeMil
		self.nPLEFilterGroupOwner		= self.nPLEFilterModeOwn | self.nPLEFilterModeForeign
		self.nPLEFilterGroupMove		= self.nPLEFilterModeCanMove | self.nPLEFilterModeCantMove

		self.nPLEAllFilters				= self.nPLEFilterGroupHealth | self.nPLEFilterGroupDomain | self.nPLEFilterGroupType | self.nPLEFilterGroupOwner | self.nPLEFilterGroupMove

		# set all filters to active -> all units 
		self.nPLEFilter 				= self.nPLEAllFilters

		self.PLOT_LIST_BUTTON_NAME		= "MyPlotListButton"
		self.PLOT_LIST_MINUS_NAME		= "MyPlotListMinus"
		self.PLOT_LIST_PLUS_NAME		= "MyPlotListPlus"
		self.PLOT_LIST_UP_NAME			= "MyPlotListUp"
		self.PLOT_LIST_DOWN_NAME		= "MyPlotListDown"
		self.PLOT_LIST_PROMO_NAME		= "MyPlotListPromo"
		self.PLOT_LIST_UPGRADE_NAME		= "MyPlotListUpgrade"

		self.PLE_VIEW_MODE			= "PLE_VIEW_MODE1"
		self.PLE_MODE_STANDARD		= "PLE_MODE_STANDARD1"
		self.PLE_MODE_MULTILINE		= "PLE_MODE_MULTILINE1"
		self.PLE_MODE_STACK_VERT	= "PLE_MODE_STACK_VERT1"
		self.PLE_MODE_STACK_HORIZ	= "PLE_MODE_STACK_HORIZ1"
		self.PLE_VIEW_MODES = (self.PLE_MODE_STANDARD, 
							   self.PLE_MODE_MULTILINE,
							   self.PLE_MODE_STACK_VERT,
							   self.PLE_MODE_STACK_HORIZ )
		self.PLE_VIEW_MODE_CYCLE = {self.PLE_MODE_STANDARD : self.PLE_MODE_MULTILINE,
									self.PLE_MODE_MULTILINE : self.PLE_MODE_STACK_VERT,
									self.PLE_MODE_STACK_VERT : self.PLE_MODE_STACK_HORIZ,
									self.PLE_MODE_STACK_HORIZ : self.PLE_MODE_STANDARD }
		self.PLE_VIEW_MODE_ART = {self.PLE_MODE_STANDARD : "PLE_MODE_STANDARD",
								  self.PLE_MODE_MULTILINE : "PLE_MODE_MULTILINE",
								  self.PLE_MODE_STACK_VERT : "PLE_MODE_STACK_VERT",
								  self.PLE_MODE_STACK_HORIZ : "PLE_MODE_STACK_HORIZ" }

		self.PLE_RESET_FILTERS		= "PLE_RESET_FILTERS1"
		self.PLE_FILTER_NOTWOUND	= "PLE_FILTER_NOTWOUND1"
		self.PLE_FILTER_WOUND		= "PLE_FILTER_WOUND1"
		self.PLE_FILTER_LAND		= "PLE_FILTER_LAND1"
		self.PLE_FILTER_SEA			= "PLE_FILTER_SEA1"
		self.PLE_FILTER_AIR			= "PLE_FILTER_AIR1"
		self.PLE_FILTER_MIL			= "PLE_FILTER_MIL1"
		self.PLE_FILTER_DOM			= "PLE_FILTER_DOM1"
		self.PLE_FILTER_OWN			= "PLE_FILTER_OWN1"
		self.PLE_FILTER_FOREIGN		= "PLE_FILTER_FOREIGN1"
		self.PLE_FILTER_CANMOVE		= "PLE_FILTER_CANMOVE1"
		self.PLE_FILTER_CANTMOVE	= "PLE_FILTER_CANTMOVE1"

		self.PLE_PROMO_BUTTONS_UNITINFO = "PLE_PROMO_BUTTONS_UNITINFO"

		self.PLE_GRP_UNITTYPE		= "PLE_GRP_UNITTYPE1"
		self.PLE_GRP_GROUPS			= "PLE_GRP_GROUPS1"
		self.PLE_GRP_PROMO			= "PLE_GRP_PROMO1"
		self.PLE_GRP_UPGRADE		= "PLE_GRP_UPGRADE1"
		self.PLE_GROUP_MODES = ( self.PLE_GRP_UNITTYPE, 
								 self.PLE_GRP_GROUPS,
								 self.PLE_GRP_PROMO,
								 self.PLE_GRP_UPGRADE )

		self.UNIT_INFO_PANE			= "PLE_UNIT_INFO_PANE_ID"
		self.UNIT_INFO_TEXT			= "PLE_UNIT_INFO_TEXT_ID"
		self.UNIT_INFO_TEXT_SHADOW	= "PLE_UNIT_INFO_TEXT_SHADOW_ID"

		self.iColOffset 			= 0
		self.iRowOffset 			= 0
		self.iVisibleUnits 			= 0
		self.pActPlot 				= 0
		self.pOldPlot 				= self.pActPlot
	#		self.sPLEMode 				= self.PLE_MODE_MULTILINE
		self.iMaxPlotListIcons 		= 0

	#		self.nPLEGrpMode 			= self.PLE_GRP_UNITTYPE
	#		self.nPLELastGrpMode  	    = self.nPLEGrpMode
		self.pActPlotListUnit		= 0
		self.iActPlotListGroup		= 0
	#		self.pLastPlotListUnit		= 0
	#		self.iLastPlotListGroup		= 0

		self.IDX_PLAYER				= 0
		self.IDX_DOMAIN 			= 1
		self.IDX_GROUPID			= 2
		self.IDX_COMBAT				= 3
		self.IDX_UNITTYPE			= 4
		self.IDX_LEVEL				= 5
		self.IDX_XP					= 6
		self.IDX_TRANSPORTID		= 7
		self.IDX_CARGOID			= 8
		self.IDX_UNITID				= 9
		self.IDX_UNIT				= 10

		self.lPLEUnitList 			= []
		self.lPLEUnitListTempOK		= []
		self.lPLEUnitListTempNOK	= []
		self.dPLEUnitInfo 			= {}

		self.iLoopCnt 				= 0

		self.dUnitPromoList			= {}
		self.dUnitUpgradeList		= {}

	#		self.bInit					= False

		self.ASMA 					= AStarMoveArea()

		self.tLastMousePos			= (0,0)
		self.bInfoPaneActive		= False
		self.bUnitPromoButtonsActive = False
		self.iMousePosTol			= 30
		self.iInfoPaneCnt			= 0
		self.iLastInfoPaneCnt		= -1

		self.xResolution = 0
		self.yResolution = 0

		self.bShowWoundedIndicator = False
		self.bShowGreatGeneralIndicator = False
		self.bShowPromotionIndicator = False
		self.bShowUpgradeIndicator = False
		self.bShowMissionInfo = False

		self.bShowHealthBar = False
		self.bHideHealthBarWhileFighting = False
		self.bShowMoveBar = False

		self.bPLEShowing = True

	def PLE_CalcConstants(self, screen):
		self.xResolution = screen.getXResolution()
		self.yResolution = screen.getYResolution()

		self.iMaxPlotListIcons = self.getMaxCol() * self.getMaxRow()
		self.sPLEMode = self.PLE_MODE_MULTILINE
		self.nPLEGrpMode = self.PLE_GRP_UNITTYPE
		self.nPLELastGrpMode = self.nPLEGrpMode
		self.sPLEMode = self.PLE_VIEW_MODES[PleOpt.getDefaultViewMode()]
		self.nPLEGrpMode = self.PLE_GROUP_MODES[PleOpt.getDefaultGroupMode()]
		self.setPLEUnitList(True)

		self.pOldPlot = 0

		self.CFG_INFOPANE_PIX_PER_LINE_1 			= 24
		self.CFG_INFOPANE_PIX_PER_LINE_2 			= 19
		self.CFG_INFOPANE_DX 					    = 290

		self.CFG_INFOPANE_Y		 			= self.yResolution - PleOpt.getInfoPaneY()
		self.CFG_INFOPANE_BUTTON_SIZE		= self.CFG_INFOPANE_PIX_PER_LINE_1 - 2
		self.CFG_INFOPANE_BUTTON_PER_LINE	= self.CFG_INFOPANE_DX / self.CFG_INFOPANE_BUTTON_SIZE
		self.CFG_INFOPANE_Y2				= self.CFG_INFOPANE_Y + 105

		self.listPLEButtons = [(0,0,0)] * self.iMaxPlotListIcons


	def updatePlotListButtons_PLE( self, screen, xResolution, yResolution ):

		self.xResolution = xResolution
		self.yResolution = yResolution

		self.iLoopCnt += 1

		self.pActPlot = CyInterface().getSelectionPlot()
		# if the plot changed, reset plot list offset
		if (self.pOldPlot):
			# check if plot has changed
			if (self.pOldPlot.getX() != self.pActPlot.getX()) or (self.pOldPlot.getY() != self.pActPlot.getY()):
				self.pOldPlot = self.pActPlot
				self.iColOffset = 0
				self.iRowOffset = 0
				self.setPLEUnitList(True)
				# mt.debug("update plot:"+str(self.iLoopCnt))
		else:
			# initialization
			self.pOldPlot = self.pActPlot
			self.setPLEUnitList(True)
			# mt.debug("update init:"+str(self.iLoopCnt))

		# check if the current unit has changed (eg. when it is unloaded). 
		# if so, do a reinit PLE Unit List
		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()
		try:
			id = pHeadSelectedUnit.getID()
			# mt.debug("Sel Unit:"+str(id))
			if (id in self.dPLEUnitInfo):
				lActUnitInfo = self.getPLEUnitInfo( pHeadSelectedUnit )
				if (lActUnitInfo <> self.dPLEUnitInfo[ id ]):
					self.setPLEUnitList(True)
					# mt.debug("update unload:"+str(self.iLoopCnt))
		except:
			# mt.debug("Sel Unit: <fail>")
			pass

		if (self.getPLEUnitList()):
			self.getUnitList(self.pActPlot)
			self.setPLEUnitList(False)
			# mt.debug("Sel Unit: UPDATE!")

		self.listPLEButtons = [(0,0,0)] * self.iMaxPlotListIcons

		for i in range(gc.getNumPromotionInfos()):
			szName = "PromotionButton" + str(i)
			screen.moveToFront( szName )

		# hide all buttons
		self.hidePlotListButtonPLEObjects(screen)

		if ( self.pActPlot and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyEngine().isGlobeviewUp() == False):

			nRow = 0
			nCol = 0
			self.iVisibleUnits = CyInterface().getNumVisibleUnits()
			
			if self.sPLEMode == self.PLE_MODE_STANDARD:
				iCount = -self.iColOffset
				nNumUnits = self.getMaxCol()
			elif self.sPLEMode == self.PLE_MODE_MULTILINE:
				iCount = 0
				nNumUnits = self.iVisibleUnits
			elif self.sPLEMode == self.PLE_MODE_STACK_VERT:
				iCount = 0
				nCol = -self.iColOffset
				nNumUnits = self.iVisibleUnits
			elif self.sPLEMode == self.PLE_MODE_STACK_HORIZ:
				iCount = 0
				nRow = -self.iRowOffset
				nNumUnits = self.iVisibleUnits
				
			bUpArrow = False
			bDownArrow = False
			bFirstLoop = True
			
	# BUG - PLE - end

			bLeftArrow = False
			bRightArrow = False

			iLastUnitType = UnitTypes.NO_UNIT
			iLastGroupID  = 0
			# loop for all units on the plot
			for i in range(len(self.lPLEUnitList)):
				pLoopUnit = self.getInterfacePlotUnit(i)

				if (pLoopUnit):
					# checks if the units matches actual filters
					if (self.checkDisplayFilter(pLoopUnit)):

						if not pLoopUnit.isCargo():
							iActUnitType = pLoopUnit.getUnitType()
							iActGroupID  = pLoopUnit.getGroupID()

						# standard view with scroll arrows
						if (self.sPLEMode == self.PLE_MODE_STANDARD):
							if (self.iColOffset > 0):
								bLeftArrow = True
							if ((self.iVisibleUnits - self.getMaxCol() - self.iColOffset) > 0):
								bRightArrow = True
								
							if ((iCount >= 0) and (iCount < nNumUnits )):
								nCol = iCount
								nRow = 0
								self.displayUnitPlotListObjects(screen, pLoopUnit, nRow, nCol)

						# multiline view
						elif (self.sPLEMode == self.PLE_MODE_MULTILINE):

							if (self.iRowOffset > 0):
								bDownArrow = True
							if ((nRow >= self.getMaxRow()) > 0):
								bUpArrow = True
								
							nCol = self.getCol( iCount ) 
							nRow = self.getRow( iCount ) - self.iRowOffset
							if ((nRow >= 0) and (iCount < nNumUnits ) and (nRow < self.getMaxRow())):
								self.displayUnitPlotListObjects(screen, pLoopUnit, nRow, nCol)
								
						# vertical stack view
						elif (self.sPLEMode == self.PLE_MODE_STACK_VERT):

							if (self.iColOffset > 0):
								bLeftArrow = True
							if (nCol >= self.getMaxCol()):
								bRightArrow = True
								
							if (self.nPLEGrpMode == self.PLE_GRP_UNITTYPE):
								if (iLastUnitType != UnitTypes.NO_UNIT):
									if (iActUnitType != iLastUnitType):
										nCol += 1
										nRow = 0
									else:
										nRow += 1
										if (nRow >= self.getMaxRow()):
											nRow = 0
											nCol += 1
							elif (self.nPLEGrpMode == self.PLE_GRP_GROUPS):
								if (iLastGroupID != 0):
									if (iActGroupID != iLastGroupID):
										nCol += 1
										nRow = 0
									else:
										nRow += 1
										if (nRow >= self.getMaxRow()):
											nRow = 0
											nCol += 1
							elif (self.nPLEGrpMode == self.PLE_GRP_PROMO):
								nRow = 0
								if not bFirstLoop:
									nCol += 1
							elif (self.nPLEGrpMode == self.PLE_GRP_UPGRADE):
								nRow = 0
								if not bFirstLoop:
									nCol += 1

							if ((nCol >= 0) and (iCount < nNumUnits ) and (nCol < self.getMaxCol())):
								self.displayUnitPlotListObjects(screen, pLoopUnit, nRow, nCol)
								if (self.nPLEGrpMode == self.PLE_GRP_PROMO):
									self.displayUnitPromos(screen, pLoopUnit, nRow, nCol)
								elif (self.nPLEGrpMode == self.PLE_GRP_UPGRADE):
									self.displayUnitUpgrades(screen, pLoopUnit, nRow, nCol)

						# horizontal stack view
						elif (self.sPLEMode == self.PLE_MODE_STACK_HORIZ):

							if (self.iRowOffset > 0):
								bDownArrow = True
							if ((nRow >= self.getMaxRow()) > 0):
								bUpArrow = True

							if (self.nPLEGrpMode == self.PLE_GRP_UNITTYPE):
								if ((iLastUnitType != UnitTypes.NO_UNIT)):
									if (iActUnitType != iLastUnitType):
										nRow += 1
										nCol = 0
									else:
										nCol += 1
										if (nCol >= self.getMaxCol()):
											nCol = 0
											nRow += 1
							elif (self.nPLEGrpMode == self.PLE_GRP_GROUPS):
								if (iLastGroupID != 0):
									if (iActGroupID != iLastGroupID):
										nRow += 1
										nCol = 0
									else:
										nCol += 1
										if (nCol >= self.getMaxCol()):
											nCol = 0
											nRow += 1
							elif (self.nPLEGrpMode == self.PLE_GRP_PROMO):
								nCol= 0
								if not bFirstLoop:
									nRow += 1
							elif (self.nPLEGrpMode == self.PLE_GRP_UPGRADE):
								nCol= 0
								if not bFirstLoop:
									nRow += 1

							if ((nRow >= 0) and (iCount < nNumUnits ) and (nRow < self.getMaxRow())):
								self.displayUnitPlotListObjects(screen, pLoopUnit, nRow, nCol)
								if (self.nPLEGrpMode == self.PLE_GRP_PROMO):
									self.displayUnitPromos(screen, pLoopUnit, nRow, nCol)
								elif (self.nPLEGrpMode == self.PLE_GRP_UPGRADE):
									self.displayUnitUpgrades(screen, pLoopUnit, nRow, nCol)

						iCount += 1

						iLastUnitType 	= iActUnitType
						iLastGroupID  	= iActGroupID
						bFirstLoop 		= false

			# left/right scroll buttons
			if 	( ( self.sPLEMode == self.PLE_MODE_STANDARD ) and ( self.iVisibleUnits > self.getMaxCol() ) ) or \
				( ( self.sPLEMode == self.PLE_MODE_STACK_VERT ) and ( ( nCol >= self.getMaxCol() or ( self.iColOffset > 0 ) ) ) ):
				screen.enable( self.PLOT_LIST_MINUS_NAME, bLeftArrow )
				screen.show( self.PLOT_LIST_MINUS_NAME )
				screen.enable( self.PLOT_LIST_PLUS_NAME, bRightArrow )
				screen.show( self.PLOT_LIST_PLUS_NAME )
				
			# up/Down scroll buttons
			if 	( ( self.sPLEMode == self.PLE_MODE_MULTILINE ) and ( ( nRow >= self.getMaxRow() or ( self.iRowOffset > 0 ) ) ) ) or \
				( ( self.sPLEMode == self.PLE_MODE_STACK_HORIZ ) and ( ( nRow >= self.getMaxRow() or ( self.iRowOffset > 0 ) ) ) ):
				screen.enable(self.PLOT_LIST_UP_NAME, bUpArrow )
				screen.show( self.PLOT_LIST_UP_NAME )
				screen.enable( self.PLOT_LIST_DOWN_NAME, bDownArrow )
				screen.show( self.PLOT_LIST_DOWN_NAME )
				
			self.showPlotListButtonObjects(screen)
			
		else:
			self.hidePlotListButtonPLEObjects(screen)
	# BUG - PLE - end

		return 0





	# PLE Mode Switcher functions
	def onClickPLEResetFilters(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.resetPLEFilters()
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ):
			sFullKey = "TXT_KEY_PLE_RESET_FILTERS"
			bSelected = self.isPLEFilter(self.nPLEAllFilters)
			if ( bSelected ):
				sFullKey += "_ON"
			self.displayHelpHover(sFullKey)
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			self.hideInfoPane()
			return 1
		return 0


	# PLE Movement Filters
	def onClickPLEFilterCanMove(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeCanMove, self.nPLEFilterGroupMove)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "CANMOVE", self.nPLEFilterModeCanMove)

	def onClickPLEFilterCantMove(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeCantMove, self.nPLEFilterGroupMove)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "CANTMOVE", self.nPLEFilterModeCantMove)


	# PLE Health Filters
	def onClickPLEFilterNotWound(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeNotWound, self.nPLEFilterGroupHealth)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "HEALTHY", self.nPLEFilterModeNotWound)
			
	def onClickPLEFilterWound(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeWound, self.nPLEFilterGroupHealth)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "WOUNDED", self.nPLEFilterModeWound)


	# PLE Domain Filters
	def onClickPLEFilterLand(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeLand, self.nPLEFilterGroupDomain)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "LAND", self.nPLEFilterModeLand)

	def onClickPLEFilterSea(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeSea, self.nPLEFilterGroupDomain)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "SEA", self.nPLEFilterModeSea)

	def onClickPLEFilterAir(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeAir, self.nPLEFilterGroupDomain)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "AIR", self.nPLEFilterModeAir)


	# PLE Domain Filters
	def onClickPLEFilterMil(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeMil, self.nPLEFilterGroupType)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "MIL", self.nPLEFilterModeMil)

	def onClickPLEFilterDom(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeDom, self.nPLEFilterGroupType)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "DOM", self.nPLEFilterModeDom)
			

	# PLE Ownership Filters
	def onClickPLEFilterOwn(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeOwn, self.nPLEFilterGroupOwner)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "OWN", self.nPLEFilterModeOwn)
			
	def onClickPLEFilterForeign(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeForeign, self.nPLEFilterGroupOwner)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "FOREIGN", self.nPLEFilterModeForeign)


	# PLE Grouping Modes
	def onClickPLEGrpUnittype(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			if (self.nPLEGrpMode == self.PLE_GRP_UNITTYPE):
				self.setPLEGroupMode(self.PLE_GRP_GROUPS)
				self.nPLELastGrpMode = self.PLE_GRP_GROUPS
			elif (self.nPLEGrpMode == self.PLE_GRP_GROUPS):
				self.setPLEGroupMode(self.PLE_GRP_UNITTYPE)
				self.nPLELastGrpMode = self.PLE_GRP_UNITTYPE
			else:
				self.setPLEGroupMode(self.nPLELastGrpMode)
			return 1
		else:
			return self.handleHoverPLEGrpMode(inputClass, "STANDARD", self.PLE_GRP_UNITTYPE)

	def onClickPLEGrpGroups(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEGroupMode(self.PLE_GRP_GROUPS)
			return 1
		else:
			return self.handleHoverPLEGrpMode(inputClass, "GROUPS", self.PLE_GRP_GROUPS)

	def onClickPLEGrpPromo(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			if ( self.nPLEGrpMode == self.PLE_GRP_PROMO ):
				self.setPLEGroupMode(self.nPLELastGrpMode)
			else:
				self.setPLEGroupMode(self.PLE_GRP_PROMO)
			return 1
		else:
			return self.handleHoverPLEGrpMode(inputClass, "PROMO", self.PLE_GRP_PROMO)

	def onClickPLEGrpUpgrade(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			if ( self.nPLEGrpMode == self.PLE_GRP_UPGRADE ):
				self.setPLEGroupMode(self.nPLELastGrpMode)
			else:
				self.setPLEGroupMode(self.PLE_GRP_UPGRADE)
			return 1
		else:
			return self.handleHoverPLEGrpMode(inputClass, "UPGRADE", self.PLE_GRP_UPGRADE)


	# PLE View Modes
	def onClickPLEViewMode(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			if ( self.sPLEMode in self.PLE_VIEW_MODE_CYCLE ):
				self.setPLEViewMode(self.PLE_VIEW_MODE_CYCLE[self.sPLEMode])
			else:
				self.setPLEViewMode(PleOpt.getDefaultViewMode())
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ):
			sFullKey = "TXT_KEY_PLE_VIEW_MODE"
			self.displayHelpHover(sFullKey)
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			self.hideInfoPane()
			return 1
		return 0
				
	def onClickPLEModeStandard(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEViewMode(self.PLE_MODE_STANDARD)
			return 1
		else:
			return self.handleHoverPLEViewMode(inputClass, "STANDARD", self.PLE_MODE_STANDARD)
				
	def onClickPLEModeMultiline(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEViewMode(self.PLE_MODE_MULTILINE)
			return 1
		else:
			return self.handleHoverPLEViewMode(inputClass, "MULTILINE", self.PLE_MODE_MULTILINE)

	def onClickPLEModeStackVert(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEViewMode(self.PLE_MODE_STACK_VERT)
			return 1
		else:
			return self.handleHoverPLEViewMode(inputClass, "STACK_VERT", self.PLE_MODE_STACK_VERT)

	def onClickPLEModeStackHoriz(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEViewMode(self.PLE_MODE_STACK_HORIZ)
			return 1
		else:
			return self.handleHoverPLEViewMode(inputClass, "STACK_HORIZ", self.PLE_MODE_STACK_HORIZ)





	def resetPLEFilters(self):
		self.nPLEFilter = self.nPLEAllFilters
		CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)

	def displayHelpHover(self, sKey):
		sText = u"<font=2>%s</font>" % BugUtil.getPlainText(sKey)
		self.displayInfoPane(sText)

	# hides the info pane
	def hideInfoPane(self):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.hide(self.UNIT_INFO_TEXT)
		screen.hide(self.UNIT_INFO_TEXT_SHADOW)
		screen.hide(self.UNIT_INFO_PANE)
		self.bInfoPaneActive = False
		self.iLastInfoPaneCnt = self.iInfoPaneCnt

	# Returns True if the given filter is active
	# You can pass in a filter group to see if any of its filters is active
	def isPLEFilter(self, nFilter):
		return self.nPLEFilter & nFilter != nFilter

	# Sets or toggles a specific filter button (wounded, air, etc) based on the PLE/BUG mode
	def setPLEFilter(self, nFilter, nFilterGroup):
		self.hideInfoPane()
		if (PleOpt.isBugFilterBehavior()):
			bWasSelected = self.isPLEFilter(nFilter)
			# Clear all filters in group
			self.nPLEFilter |= nFilterGroup
			if (not bWasSelected):
				# Select the specified mode
				self.nPLEFilter ^= nFilter
		else:
			# Toggle the specified mode
			self.nPLEFilter ^= nFilter
		CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)

	# Sets the grouping mode (includes upgrade and promotion modes)
	def setPLEGroupMode(self, nGroupingMode):
		self.hideInfoPane()
		if (self.nPLEGrpMode != nGroupingMode):
			self.nPLEGrpMode = nGroupingMode
			self.setPLEUnitList(True)
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)

	# Sets the view mode
	def setPLEViewMode(self, nViewMode):
		self.hideInfoPane()
		if (self.sPLEMode != nViewMode):
			self.iRowOffset = 0
			self.iColOffset = 0
			self.sPLEMode = nViewMode
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)

	############## input handlers functions ######################

	# Makes the text size small to avoid a scrollbar and displays the help text
	def handleHoverPLEFilter(self, inputClass, sKey, nFilter):
		"Shows or hides the correct hover text for the given filter."
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ):
			sFullKey = "TXT_KEY_PLE_FILTER_"
			if ( PleOpt.isBugFilterBehavior() ):
				sFullKey += "BUG_"
			sFullKey += sKey
			bSelected = self.isPLEFilter(nFilter)
			if ( bSelected ):
				sFullKey += "_ON"
			self.displayHelpHover(sFullKey)
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			self.hideInfoPane()
			return 1
		return 0

	def handleHoverPLEViewMode(self, inputClass, sKey, nViewMode):
		"Shows or hides the hover text for the given view mode."
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ):
			sFullKey = "TXT_KEY_PLE_MODE_" + sKey
			bSelected = self.sPLEMode == nViewMode
			#if ( bSelected ):
			#	sFullKey += "_ON"
			self.displayHelpHover(sFullKey)
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			self.hideInfoPane()
			return 1
		return 0

	def handleHoverPLEGrpMode(self, inputClass, sKey, nGrpMode):
		"Shows or hides the hover text for the given view mode."
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ):
			sFullKey = "TXT_KEY_PLE_GRP_" + sKey
			if ( sKey == "STANDARD" ):
				bSelected = self.nPLEGrpMode in (self.PLE_GRP_UNITTYPE, self.PLE_GRP_GROUPS)
			elif ( sKey == "PROMO" ):
				bSelected = self.nPLEGrpMode == self.PLE_GRP_PROMO
			elif ( sKey == "UPGRADE" ):
				bSelected = self.nPLEGrpMode == self.PLE_GRP_UPGRADE
			if ( bSelected ):
				sFullKey += "_ON"
			self.displayHelpHover(sFullKey)
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			self.hideInfoPane()
			return 1
		return 0



		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEViewMode(self.PLE_MODE_STACK_VERT)
			return 1
		else:
			return self.handleHoverPLEViewMode(inputClass, "STACK_VERT", self.PLE_MODE_STACK_VERT)


	# handles the unit promotion button inputs
	def unitPromotion(self, inputClass):
		id = inputClass.getID()
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ):
			if not CyInterface().isCityScreenUp():
				self.showPromoInfoPane(id)
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			self.hidePromoInfoPane()				
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.doPromotion(id)
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1

	# Arrow Up
	def getPlotListUpName(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.iRowOffset += 1
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1
		return 0
		
	# Arrow Down
	def getPlotListDownName(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			if (self.iRowOffset > 0):
				self.iRowOffset -= 1
				CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
				return 1
		return 0
		
	# Arrow Left
	def getPlotListMinusName(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			if (self.iColOffset > 0):
				self.iColOffset -= 1
				CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
				return 1
		return 0
		
	# Arrow Right
	def getPlotListPlusName(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.iColOffset += 1
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1
		return 0

	# determines the unit button
	def getPlotListButtonName(self, inputClass):
		id = inputClass.getID()
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ):
			if not CyInterface().isCityScreenUp():
				self.showUnitInfoPane(id)
			if mt.bAlt():
				self.highlightMoves(id)
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			self.hideUnitInfoPane()
			if mt.bAlt():
				self.dehighlightMoves()
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			# mt.debug("id:%i;p:(%i;%i)"%(id, self.pActPlot.getX(), self.pActPlot.getY()))
			if (id >= 0) and (id <= self.iMaxPlotListIcons):
				self.selectGroup( id, mt.bShift(), mt.bCtrl(), mt.bAlt())
				CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
				return 1
		return 0

	# handles the unit upgrade button inputs
	def unitUpgrade(self, inputClass):
		id = inputClass.getID()
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ):
			if not CyInterface().isCityScreenUp():
				self.showUpgradeInfoPane(id)
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			self.hideUpgradeInfoPane()
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
	#			mt.debug("upgrade id:"+str(id))
			self.doUpgrade(id)
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1
		
	############## base functions to calculate/transform the number of objects dependent on the screen resolution ######################

	def getMaxCol(self):
		return ((self.xResolution - (iMultiListXL+iMultiListXR) - 68) / 34)
		
	def getMaxRow(self):
		return ((self.yResolution - 160) / PleOpt.getVerticalSpacing()) 
		
	def getRow(self, i):
		return i / self.getMaxCol()

	def getCol(self, i):
		return i % self.getMaxCol()
		
	def getX(self, nCol):
		return 315 + (nCol * PleOpt.getHoriztonalSpacing())
		
	def getY(self, nRow):
		return self.yResolution - 169 - (nRow * PleOpt.getVerticalSpacing())
		
	def getI(self, nRow, nCol):
		return ( nRow * self.getMaxCol() ) + ( nCol % self.getMaxCol() )

	############## functions for visual objects (show and hide) ######################
		
	# PLE Grouping Mode Switcher 
	def setupPLEGroupModeButtons(self, screen):
		if (self.nPLEGrpMode == self.PLE_GRP_UNITTYPE):
			screen.changeImageButton(self.PLE_GRP_UNITTYPE, ArtFileMgr.getInterfaceArtInfo("PLE_GRP_UNITTYPE").getPath())
			screen.setState(self.PLE_GRP_UNITTYPE, True)
		elif (self.nPLEGrpMode == self.PLE_GRP_GROUPS):
			screen.changeImageButton(self.PLE_GRP_UNITTYPE, ArtFileMgr.getInterfaceArtInfo("PLE_GRP_GROUPS").getPath())
			screen.setState(self.PLE_GRP_UNITTYPE, True)
		else:
			screen.setState(self.PLE_GRP_UNITTYPE, False)
		#screen.setState(self.PLE_GRP_UNITTYPE, self.nPLEGrpMode == self.PLE_GRP_UNITTYPE or self.nPLEGrpMode == self.PLE_GRP_GROUPS)
		#screen.setState(self.PLE_GRP_GROUPS, self.nPLEGrpMode == self.PLE_GRP_GROUPS)
		screen.setState(self.PLE_GRP_PROMO, self.nPLEGrpMode == self.PLE_GRP_PROMO)
		screen.setState(self.PLE_GRP_UPGRADE, self.nPLEGrpMode == self.PLE_GRP_UPGRADE)
		
	# PLE View Mode Switcher
	def setupPLEViewModeButtons(self, screen):
		screen.changeImageButton(self.PLE_VIEW_MODE, ArtFileMgr.getInterfaceArtInfo(self.PLE_VIEW_MODE_ART[self.sPLEMode]).getPath())
	#		screen.setState(self.PLE_MODE_STANDARD, self.sPLEMode == self.PLE_MODE_STANDARD)
	#		screen.setState(self.PLE_MODE_MULTILINE, self.sPLEMode == self.PLE_MODE_MULTILINE)
	#		screen.setState(self.PLE_MODE_STACK_VERT, self.sPLEMode == self.PLE_MODE_STACK_VERT)
	#		screen.setState(self.PLE_MODE_STACK_HORIZ, self.sPLEMode == self.PLE_MODE_STACK_HORIZ)

	# PLE Filters
	def setupPLEFilterButtons(self, screen):
		screen.setState(self.PLE_FILTER_CANMOVE, self.isPLEFilter(self.nPLEFilterModeCanMove))
		screen.setState(self.PLE_FILTER_CANTMOVE, self.isPLEFilter(self.nPLEFilterModeCantMove))

		screen.setState(self.PLE_FILTER_NOTWOUND, self.isPLEFilter(self.nPLEFilterModeNotWound))
		screen.setState(self.PLE_FILTER_WOUND, self.isPLEFilter(self.nPLEFilterModeWound))

		screen.setState(self.PLE_FILTER_LAND, self.isPLEFilter(self.nPLEFilterModeLand))
		screen.setState(self.PLE_FILTER_SEA, self.isPLEFilter(self.nPLEFilterModeSea))
		screen.setState(self.PLE_FILTER_AIR, self.isPLEFilter(self.nPLEFilterModeAir))

		screen.setState(self.PLE_FILTER_MIL, self.isPLEFilter(self.nPLEFilterModeMil))
		screen.setState(self.PLE_FILTER_DOM, self.isPLEFilter(self.nPLEFilterModeDom))

		screen.setState(self.PLE_FILTER_OWN, self.isPLEFilter(self.nPLEFilterModeOwn))
		screen.setState(self.PLE_FILTER_FOREIGN, self.isPLEFilter(self.nPLEFilterModeForeign))

		return 0

	# Displays the plot list switches (views, filters, groupings)
	def showPlotListButtonObjects(self, screen):
		if ( PleOpt.isShowButtons() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START ):
			# show PLE modes switches
			self.setupPLEViewModeButtons(screen)
			screen.show(self.PLE_VIEW_MODE)
	#			screen.show(self.PLE_MODE_STANDARD)
	#			screen.show(self.PLE_MODE_MULTILINE)
	#			screen.show(self.PLE_MODE_STACK_VERT)
	#			screen.show(self.PLE_MODE_STACK_HORIZ)

			# show PLE filter switches
			screen.show(self.PLE_RESET_FILTERS)

			self.setupPLEFilterButtons(screen)
			screen.show(self.PLE_FILTER_CANMOVE)
			screen.show(self.PLE_FILTER_CANTMOVE)

			screen.show(self.PLE_FILTER_NOTWOUND)
			screen.show(self.PLE_FILTER_WOUND)

			screen.show(self.PLE_FILTER_LAND)
			screen.show(self.PLE_FILTER_SEA)
			screen.show(self.PLE_FILTER_AIR)

			screen.show(self.PLE_FILTER_MIL)
			screen.show(self.PLE_FILTER_DOM)

			screen.show(self.PLE_FILTER_OWN)
			screen.show(self.PLE_FILTER_FOREIGN)

			# show PLE grouping switches
			self.setupPLEGroupModeButtons(screen)
			screen.show(self.PLE_GRP_UNITTYPE)
			screen.show(self.PLE_GRP_GROUPS)
			screen.show(self.PLE_GRP_PROMO)
			screen.show(self.PLE_GRP_UPGRADE)

			self.bPLEShowing = True


	# hides all plot list switches (views, filters, groupings) and all the other objects
	def hidePlotListButtonPLEObjects(self, screen):
		if not self.bPLEShowing:
			return

		# hides all unit button objects
		for i in range( self.iMaxPlotListIcons ):
			szString = self.PLOT_LIST_BUTTON_NAME + str(i)
			screen.hide( szString )
			screen.hide( szString + "Icon" )
			screen.hide( szString + "HealthBar" )
			screen.hide( szString + "MoveBar" )
			screen.hide( szString + "PromoFrame" )
			screen.hide( szString + "ActionIcon" )
			screen.hide( szString + "Upgrade" )

		# hides all promotion and upgrade button objects
		for nCol in range(self.getMaxCol()+1):
			for nRow in range(self.getMaxRow()+1):
				# 
				szStringUnitPromo = self.PLOT_LIST_PROMO_NAME + string.zfill(str(nRow), 2) + string.zfill(str(nCol), 2)
				screen.hide( szStringUnitPromo )
				# 
				szStringUnitUpgrade = self.PLOT_LIST_UPGRADE_NAME + string.zfill(str(nRow), 2) + string.zfill(str(nCol), 2)
				screen.hide( szStringUnitUpgrade )
		
		# hide PLE modes switches
		screen.hide(self.PLE_VIEW_MODE)
	#		screen.hide(self.PLE_MODE_STANDARD)
	#		screen.hide(self.PLE_MODE_MULTILINE)
	#		screen.hide(self.PLE_MODE_STACK_VERT)
	#		screen.hide(self.PLE_MODE_STACK_HORIZ)
		# hide horizontal scroll buttons
		screen.hide( self.PLOT_LIST_MINUS_NAME )
		screen.hide( self.PLOT_LIST_PLUS_NAME )
		# hide vertical scroll buttons
		screen.hide( self.PLOT_LIST_UP_NAME )
		screen.hide( self.PLOT_LIST_DOWN_NAME )
		# hide reset all filters button
		screen.hide(self.PLE_RESET_FILTERS)
		# hide PLE filter switches
		screen.hide(self.PLE_FILTER_CANMOVE)
		screen.hide(self.PLE_FILTER_CANTMOVE)
		screen.hide(self.PLE_FILTER_NOTWOUND)
		screen.hide(self.PLE_FILTER_WOUND)
		screen.hide(self.PLE_FILTER_LAND)
		screen.hide(self.PLE_FILTER_SEA)
		screen.hide(self.PLE_FILTER_AIR)
		screen.hide(self.PLE_FILTER_MIL)
		screen.hide(self.PLE_FILTER_DOM)
		screen.hide(self.PLE_FILTER_OWN)
		screen.hide(self.PLE_FILTER_FOREIGN)
		# hide PLE group switches
		screen.hide(self.PLE_GRP_UNITTYPE)
		screen.hide(self.PLE_GRP_GROUPS)
		screen.hide(self.PLE_GRP_PROMO)
		screen.hide(self.PLE_GRP_UPGRADE)
		
		self.bPLEShowing = False
		
	# prepares the display of the mode, view, grouping, filter  switches
	def preparePlotListObjects(self, screen):
		xResolution = self.xResolution
		yResolution = self.yResolution

		iHealthyColor = PleOpt.getHealthyColor()
		iWoundedColor = PleOpt.getWoundedColor()
		iMovementColor = PleOpt.getFullMovementColor()
		iHasMovedColor = PleOpt.getHasMovedColor()
		iNoMovementColor = PleOpt.getNoMovementColor()

		szFileNamePromo = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION_FRAME").getPath()
		szFileNameGovernor = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath()
		szFileNameHilite = ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath()
		for i in range( self.iMaxPlotListIcons ):
			# create button name
			szString = self.PLOT_LIST_BUTTON_NAME + str(i)

			x = self.getX( self.getCol( i ) )
			y = self.getY( self.getRow( i ) )

			# place/init the promotion frame. Important to have it at first place within the for loop.
			szStringPromoFrame = szString + "PromoFrame"
			screen.addDDSGFC( szStringPromoFrame, szFileNamePromo, x, y, 32, 32, WidgetTypes.WIDGET_GENERAL, i, -1 )
			screen.hide( szStringPromoFrame )

			# place the plot list unit button
			screen.addCheckBoxGFC( szString, szFileNameGovernor, szFileNameHilite, x, y, 32, 32, WidgetTypes.WIDGET_GENERAL, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
			screen.hide( szString )

			# place/init the health bar. Important to have it at last place within the for loop.
			szStringHealthBar = szString + "HealthBar"
#			screen.addStackedBarGFC( szStringHealthBar, x+7, y-7, 25, 14, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addStackedBarGFC( szStringHealthBar, x+5, y-9, 29, 11, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, i, -1 )
			screen.setStackedBarColors( szStringHealthBar, InfoBarTypes.INFOBAR_STORED, iHealthyColor )
			screen.setStackedBarColors( szStringHealthBar, InfoBarTypes.INFOBAR_RATE, iWoundedColor )
			screen.hide( szStringHealthBar )

			# place/init the movement bar. Important to have it at last place within the for loop.
			szStringMoveBar = szString + "MoveBar"
			screen.addStackedBarGFC( szStringMoveBar, x+5, y-5, 29, 11, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, i, -1 )
			screen.setStackedBarColors( szStringMoveBar, InfoBarTypes.INFOBAR_STORED, iMovementColor )
			screen.setStackedBarColors( szStringMoveBar, InfoBarTypes.INFOBAR_RATE, iHasMovedColor )
			screen.setStackedBarColors( szStringMoveBar, InfoBarTypes.INFOBAR_EMPTY, iNoMovementColor )
			screen.hide( szStringMoveBar )


		nYOff	= 130 + 4
		nXOff	= 290 - 12
		nSize	= 24
		nDist	= 22
		nGap    = 10
		nNum	= 0
		
		# PLE Style-Mode buttons
		#screen.setImageButton( "PleViewModeStyle1", "", 20, 400, 28, 28, WidgetTypes.WIDGET_GENERAL, 1, -1 )
		#screen.setStyle( "PleViewModeStyle1", "Button_BUG_PLE_ViewMode_SingleRow_Style" )
		
		# place the PLE mode switches
		nXOff += nDist
		szString = self.PLE_VIEW_MODE
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_MODE_STANDARD").getPath(), "", nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
		
		# place the PLE grouping mode switches
		nXOff += nDist + nGap
		szString = self.PLE_GRP_UNITTYPE
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_GRP_UNITTYPE").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
		
		# place the promotion and upgrades mode switches
		nXOff += nDist
		szString = self.PLE_GRP_PROMO
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_GRP_PROMO").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
		
		nXOff += nDist
		szString = self.PLE_GRP_UPGRADE
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_GRP_UPGRADE").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
		
		# place the PLE reset filter button
		nXOff += nDist + nGap
		szString = self.PLE_RESET_FILTERS
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_RESET_FILTERS").getPath(), "", nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )

		# place the PLE movement filter switches
		nXOff += nDist + nGap
		szString = self.PLE_FILTER_CANMOVE
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_CANMOVE").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
		
		nXOff += nDist
		szString = self.PLE_FILTER_CANTMOVE
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_CANTMOVE").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )

		# place the PLE health filter switches
		nXOff += nDist + nGap
		szString = self.PLE_FILTER_NOTWOUND
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_NOTWOUND").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )

		nXOff += nDist
		szString = self.PLE_FILTER_WOUND
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_WOUND").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )

		# place the PLE domain filter switches
		nXOff += nDist + nGap
		szString = self.PLE_FILTER_LAND
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_LAND").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )

		nXOff += nDist
		szString = self.PLE_FILTER_SEA
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_SEA").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )

		nXOff += nDist
		szString = self.PLE_FILTER_AIR
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_AIR").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )

		# place the PLE civilian/military filter switches
		nXOff += nDist + nGap
		szString = self.PLE_FILTER_MIL
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_MIL").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
		
		nXOff += nDist
		szString = self.PLE_FILTER_DOM
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_DOM").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
				
		# place the PLE owner filter switches
		nXOff += nDist + nGap
		szString = self.PLE_FILTER_OWN
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_OWN").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
		
		nXOff += nDist
		szString = self.PLE_FILTER_FOREIGN
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_FOREIGN").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
				
	################ functions for normal/shift/ctrl/alt unit selection within the plot list itself #################

	# deselects all units in the plot list
	def deselectAll(self):
		for i in range(len(self.lPLEUnitList)):
			pUnit = self.getInterfacePlotUnit(i)
			if (pUnit.IsSelected()):
				CyInterface().selectUnit(pUnit, False, True, False)	

	# function saves all units not matching actual filter criteria in a temp list by type
	def saveFilteredUnitsByType(self, pCompareUnit, bShift):
		self.lPLEUnitListTempOK = []
		self.lPLEUnitListTempNOK = []
		# save unit type for comparision
		pCompareUnitType = pCompareUnit.getUnitType()
		for i in range(len(self.lPLEUnitList)):
			pLoopUnit = self.getInterfacePlotUnit(i)
			# has the unit the correct type and does the unit NOT match the filter parameters
			if (pLoopUnit.getUnitType() == pCompareUnitType) and (not (self.checkDisplayFilter(pLoopUnit))):
				# unit has to be moved
				self.lPLEUnitListTempNOK.append(pLoopUnit)
			else:
				# unit has to be displayed
				self.lPLEUnitListTempOK.append(pLoopUnit)
		# loop to find all the cargo of units in the OK list. They don't have to be moved away.
		lTempNOK 	= self.lPLEUnitListTempNOK[:]
		lTempOK 	= self.lPLEUnitListTempOK[:]
		for pLoopUnitNOK in lTempNOK:
			# check if unit is cargo
			if pLoopUnitNOK.isCargo():
				# check if the units transport unit is a to be displayed unit
				for pLoopUnitOK in lTempOK:
					if pLoopUnitOK.getID() == pLoopUnitNOK.getTransportUnit().getID():
						# remove cargo unit from NOK array and append it to OK array
						self.lPLEUnitListTempNOK.remove(pLoopUnitNOK)
						self.lPLEUnitListTempOK.append(pLoopUnitNOK)
		# if Shift is pressed, we also have to keep the already selected units 
		if bShift:
			lTempNOK 	= self.lPLEUnitListTempNOK[:]
			lTempOK 	= self.lPLEUnitListTempOK[:]
			for i in range(len(self.lPLEUnitList)):
				pLoopUnit = self.getInterfacePlotUnit(i)
				if (pLoopUnit.IsSelected()):
					if pLoopUnit in lTempNOK:
						self.lPLEUnitListTempNOK.remove(pLoopUnitNOK)
						self.lPLEUnitListTempOK.append(pLoopUnitNOK)
						
					
	# function saves all units not matching actual filter criteria in a temp list by domain
	def saveFilteredUnitsByDomain(self, pCompareUnit):
		self.lPLEUnitListTempOK = []
		self.lPLEUnitListTempNOK = []
		# save unit type for comparision
		pUnitTypeInfo = gc.getUnitInfo(pCompareUnit.getUnitType())
		eCompareDomain = pUnitTypeInfo.getDomainType()
		for i in range(len(self.lPLEUnitList)):
			pLoopUnit = self.getInterfacePlotUnit(i)
			pUnitTypeInfo = gc.getUnitInfo(pLoopUnit.getUnitType())
			eDomainType = pUnitTypeInfo.getDomainType()
			# has the unit the correct domain and ismatching the current filter criteria
			if (eDomainType == eCompareDomain) and (self.checkDisplayFilter(pLoopUnit)):					
				# unit has to be displayed
				self.lPLEUnitListTempOK.append(pLoopUnit)
			else:
				# unit has to be moved
				self.lPLEUnitListTempNOK.append(pLoopUnit)
		# loop to find all the cargo of units in the OK list. They don't have to be moved away.
		lTempNOK 	= self.lPLEUnitListTempNOK[:]
		lTempOK 	= self.lPLEUnitListTempOK[:]
		for pLoopUnitNOK in lTempNOK:
			# check if unit is cargo
			if pLoopUnitNOK.isCargo():
				# check if the units transport unit is a to be displayed unit
				for pLoopUnitOK in lTempOK:
					if pLoopUnitOK.getID() == pLoopUnitNOK.getTransportUnit().getID():
						# remove cargo unit from NOK array and append it to OK array
						self.lPLEUnitListTempNOK.remove(pLoopUnitNOK)
						self.lPLEUnitListTempOK.append(pLoopUnitNOK)

	# finds plots where we can temporarily park some units.
	# the "parking" is needed to avoid that the units are selected by the CyInterface.selectGroup() function.
	def getTempPlot(self):
		# first try : put them into another city
		pPlayer = gc.getActivePlayer()
		iPlayer = CyGame().getActivePlayer()
		lCity = PyPlayer(iPlayer).getCityList()
		pPlot = CyMap().plot(0,0)
		dPlotList = {}
		if not (self.pActPlot.isCity()):
			# if actual plot is not a city -> use first available city to park units
			pPlot = lCity[0].plot()
			for d in range(DomainTypes.NUM_DOMAIN_TYPES):
				dPlotList[d] = pPlot
		elif (pPlayer.getNumCities() > 1):
			# if actual plot is a city -> use next available city to park units
			for i in range(pPlayer.getNumCities()):
				pPlot =  lCity[i].plot()
				if (pPlot.getX() != self.pActPlot.getX()) or (pPlot.getY() != self.pActPlot.getY()):
					break
			for d in range(DomainTypes.NUM_DOMAIN_TYPES):
				dPlotList[d] = pPlot
		else:
			# no city available -> place units around the capital. There is the smallest chance to reveal a plot.
			lList = []
			pCapital = PyPlayer(iPlayer).getCapitalCity()
			for dx in range(-1, 2):
				for dy in range(-1, 2):
					if dx != 0 and dy != 0:
						pPlot = CyMap().plot(pCapital.getX()+dx, pCapital.getY()+dy)
						lList.append(pPlot)
			for d in range(DomainTypes.NUM_DOMAIN_TYPES):
				dPlotList[d] = lList[d]
		return dPlotList
			
	# temporarily moves a unit away, so that the select group works well.
	def tempMove(self, iMode):
		if iMode == 0:
			dTempPlots = self.getTempPlot()
		for i in range(len(self.lPLEUnitListTempNOK)):
			pLoopUnit = self.lPLEUnitListTempNOK[i]
			eDomainType = gc.getUnitInfo(pLoopUnit.getUnitType()).getDomainType()
			# move unit to temp plot. 
			if iMode == 0:
				pTempPlot = dTempPlots[eDomainType]
				pLoopUnit.setXY( pTempPlot.getX(), pTempPlot.getY(), False, True, False )
			else:
				pLoopUnit.setXY( self.pActPlot.getX(), self.pActPlot.getY(), False, True, False )

	# replacement of the civ 4 version
	def selectGroup(self, iID, bShift, bCtrl, bAlt):
		pUnit = self.listPLEButtons[iID][0]
		# check if the unit has been selected from the city screen
		bCityUp = CyInterface().isCityScreenUp()
		if not (self.pActPlotListUnit):
			self.pActPlotListUnit = CyInterface().getHeadSelectedUnit()
			self.pActPlotListGroup = self.pActPlotListUnit.getGroupID()
		if (not (bShift or bCtrl or bAlt)):
	#			# save prev selections
	#			self.pLastPlotListUnit = self.pActPlotListUnit
	#			self.iLastPlotListGroup = self.pActPlotListUnit.getGroupID()
			# save act selection
			self.pActPlotListUnit = pUnit
			self.iActPlotListGroup = pUnit.getGroupID()
			CyInterface().selectGroup( self.pActPlotListUnit, false, false, false )
	#			# check if the group has been changed 
	#			if (self.iLastPlotListGroup != self.iActPlotListGroup):
	#				self.deselectAll()
	#			# deselect last selected unit
	#			elif (self.pLastPlotListUnit):
	#				if (self.pLastPlotListUnit.IsSelected()):
	#					CyInterface().selectUnit(self.pLastPlotListUnit, false, true, false)
	#			# check if the group has not been changed and the unit is selected again -> deselect all other units of the group
	#			if (self.iLastPlotListGroup == self.iActPlotListGroup):
	#				CyInterface().selectUnit(self.pActPlotListUnit, true, true, true)
	#			else:
	#				CyInterface().selectUnit(self.pActPlotListUnit, false, true, true)
		elif bShift and (not (bCtrl or bAlt)):
			self.pActPlotListUnit = pUnit
			self.iActPlotListGroup = pUnit.getGroupID()
	#			CyInterface().selectUnit(self.pActPlotListUnit, false, true, true)
			CyInterface().selectGroup( self.pActPlotListUnit, true, false, false )
		elif bCtrl and (not (bShift or bAlt)):
			self.deselectAll()
			self.pActPlotListUnit = pUnit
			self.iActPlotListGroup = pUnit.getGroupID()
			self.saveFilteredUnitsByType(self.pActPlotListUnit, false)
			self.tempMove(0)
			CyInterface().selectGroup( self.pActPlotListUnit, false, true, false )
			self.tempMove(1)
			self.setPLEUnitList(True)
		elif bCtrl and bShift and (not bAlt):
	#			# self.deselectAll()
			self.pActPlotListUnit = pUnit
			self.iActPlotListGroup = pUnit.getGroupID()
			self.saveFilteredUnitsByType(self.pActPlotListUnit, true)
			self.tempMove(0)
			CyInterface().selectGroup( self.pActPlotListUnit, true, true, false )
			self.tempMove(1)
			self.setPLEUnitList(True)
		elif bAlt and (not (bCtrl or bShift)):
			self.deselectAll()
			self.pActPlotListUnit = pUnit
			self.iActPlotListGroup = pUnit.getGroupID()
			self.saveFilteredUnitsByDomain(self.pActPlotListUnit)
			self.tempMove(0)
			CyInterface().selectGroup( self.pActPlotListUnit, false, false, true )
			self.tempMove(1)
			self.setPLEUnitList(True)
		# if we came from city screen -> focus view on the selected unit
		if bCityUp:
			CyCamera().JustLookAtPlot(self.pActPlot)

	################## general PLE functions ##################

	# resets the colors of the plot list stacked bars
	def resetUnitPlotListStackedBarColors( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		iHealthyColor = PleOpt.getHealthyColor()
		iWoundedColor = PleOpt.getWoundedColor()
		iMovementColor = PleOpt.getFullMovementColor()
		iHasMovedColor = PleOpt.getHasMovedColor()
		iNoMovementColor = PleOpt.getNoMovementColor()
		for i in range( self.iMaxPlotListIcons ):
			# create button name
			szString = self.PLOT_LIST_BUTTON_NAME + str(i)

			szStringHealthBar = szString + "HealthBar"
			screen.setStackedBarColors( szStringHealthBar, InfoBarTypes.INFOBAR_STORED, iHealthyColor )
			screen.setStackedBarColors( szStringHealthBar, InfoBarTypes.INFOBAR_RATE, iWoundedColor )

			# place/init the movement bar. Important to have it at last place within the for loop.
			szStringMoveBar = szString + "MoveBar"
			screen.setStackedBarColors( szStringMoveBar, InfoBarTypes.INFOBAR_STORED, iMovementColor )
			screen.setStackedBarColors( szStringMoveBar, InfoBarTypes.INFOBAR_RATE, iHasMovedColor )
			screen.setStackedBarColors( szStringMoveBar, InfoBarTypes.INFOBAR_EMPTY, iNoMovementColor )

	# displays a single unit icon in the plot list with all its decorations
	def displayUnitPlotListObjects( self, screen, pLoopUnit, nRow, nCol ):
		iCount = self.getI(nRow, nCol)
		self.listPLEButtons[iCount] = ( pLoopUnit, nRow, nCol )
		self.bPLEShowing = True

		x = self.getX( nCol )
		y = self.getY( nRow )

		# create the button name 
		szString = self.PLOT_LIST_BUTTON_NAME + str(iCount)

		# set unit button image
		screen.changeImageButton( szString, gc.getUnitInfo(pLoopUnit.getUnitType()).getButton() )

		# check if it is an player unit or not
		if ( pLoopUnit.getOwner() == gc.getGame().getActivePlayer() ):
			bEnable = True
		else:
			bEnable = False
		# if player unit enable button (->visible, but not selectable)
		screen.enable(szString, bEnable)

		# check if the units is selected
		if (pLoopUnit.IsSelected()):
			screen.setState(szString, True)
		else:
			screen.setState(szString, False)
		# set select state of the unit button
		screen.show( szString )

		if bEnable:
			self._displayUnitPlotList_Dot( screen, pLoopUnit, szString, iCount, x, y )
			self._displayUnitPlotList_Promo( screen, pLoopUnit, szString )
			self._displayUnitPlotList_Upgrade( screen, pLoopUnit, szString, iCount, x, y )
			self._displayUnitPlotList_HealthBar( screen, pLoopUnit, szString )
			self._displayUnitPlotList_MoveBar( screen, pLoopUnit, szString )
			self._displayUnitPlotList_Mission( screen, pLoopUnit, szString, iCount, x, y, 16 )

		return 0

	def UnitPlotList_BUGOptions(self):
		self.bShowWoundedIndicator = PleOpt.isShowWoundedIndicator()
		self.bShowGreatGeneralIndicator = PleOpt.isShowGreatGeneralIndicator()
		self.bShowPromotionIndicator = PleOpt.isShowPromotionIndicator()
		self.bShowUpgradeIndicator = PleOpt.isShowUpgradeIndicator()
		self.bShowMissionInfo = PleOpt.isShowMissionInfo()
		self.bShowHealthBar = PleOpt.isShowHealthBar()
		self.bHideHealthBarWhileFighting = PleOpt.isHideHealthFighting()
		self.bShowMoveBar = PleOpt.isShowMoveBar()

	# checks if the unit matches actual filter conditions
	def checkDisplayFilter(self, pUnit):

		# in case of Promotion or Upgrade Display 
		if (self.nPLEGrpMode == self.PLE_GRP_PROMO):
			# if unit is not promotion ready -> return
			if not pUnit.isPromotionReady():
				return False
		elif (self.nPLEGrpMode == self.PLE_GRP_UPGRADE):
			# if unit is not upgrade ready -> return
			if not mt.checkAnyUpgrade(pUnit):
				return False
		elif pUnit.isCargo():
			# in case the unit is a cargo unit, the decision is made by the tranporting unit. 
			# that ensures, that cargo is always displayed or not displayed together with its tranporting unit
			return self.checkDisplayFilter(pUnit.getTransportUnit())
		
		if (self.isPLEFilter(self.nPLEAllFilters)):
			# At least one filter is active
			if (PleOpt.isPleFilterBehavior()):
				# unit can move and filter active
				if (self.isPLEFilter(self.nPLEFilterModeCanMove)):
					if (pUnit.movesLeft()):
						return False
				# unit cannot move and filter active
				if (self.isPLEFilter(self.nPLEFilterModeCantMove)):
					if (not pUnit.movesLeft()):
						return False
				
				# unit not wounded and filter active
				if (self.isPLEFilter(self.nPLEFilterModeNotWound)):
					if (not pUnit.isHurt()):
						return False
				# unit wounded and filter active
				if (self.isPLEFilter(self.nPLEFilterModeWound)):
					if (pUnit.isHurt()):
						return False
				
				pUnitTypeInfo = gc.getUnitInfo(pUnit.getUnitType())
				# is unit a land unit (or ICBM) and filter active
				if (self.isPLEFilter(self.nPLEFilterModeLand)):
					if (pUnitTypeInfo.getDomainType() == DomainTypes.DOMAIN_LAND) or (pUnitTypeInfo.getDomainType() == DomainTypes.DOMAIN_IMMOBILE):
						return False
				# is unit a sea unit and filter active
				if (self.isPLEFilter(self.nPLEFilterModeSea)):
					if (pUnitTypeInfo.getDomainType() == DomainTypes.DOMAIN_SEA):
						return False
				# is unit a air unit and filter active
				if (self.isPLEFilter(self.nPLEFilterModeAir)):
					if (pUnitTypeInfo.getDomainType() == DomainTypes.DOMAIN_AIR):
						return False
				
				# is unit a combat unit and filter active (combat means -> Combat or AirCombat values > 0!
				if (self.isPLEFilter(self.nPLEFilterModeMil)):
					if ((pUnitTypeInfo.getCombat() > 0) or (pUnitTypeInfo.getAirCombat() > 0)):
						return False
				# is unit a domestic unit and filter active (domestic means -> no Combat or AirCombat values!
				if (self.isPLEFilter(self.nPLEFilterModeDom)):
					if ((pUnitTypeInfo.getCombat() == 0) and (pUnitTypeInfo.getAirCombat() == 0)):
						return False
				
				# is the units owner the active player
				if (self.isPLEFilter(self.nPLEFilterModeOwn)):
					if ( pUnit.getOwner() == gc.getGame().getActivePlayer() ):
						return False
				# # is the units owner another player
				if (self.isPLEFilter(self.nPLEFilterModeForeign)):
					if ( not ( pUnit.getOwner() == gc.getGame().getActivePlayer() )):
						return False
			else:
				# BUG Filter Mode
				if (self.isPLEFilter(self.nPLEFilterModeCanMove)):
					if (not pUnit.movesLeft()):
						return False
				elif (self.isPLEFilter(self.nPLEFilterModeCantMove)):
					if (pUnit.movesLeft()):
						return False
				
				if (self.isPLEFilter(self.nPLEFilterModeNotWound)):
					if (pUnit.isHurt()):
						return False
				elif (self.isPLEFilter(self.nPLEFilterModeWound)):
					if (not pUnit.isHurt()):
						return False
				
				pUnitTypeInfo = gc.getUnitInfo(pUnit.getUnitType())
				if (self.isPLEFilter(self.nPLEFilterModeLand)):
					if (pUnitTypeInfo.getDomainType() != DomainTypes.DOMAIN_LAND) and (gc.getUnitInfo(pUnit.getUnitType()).getDomainType() != DomainTypes.DOMAIN_IMMOBILE):
						return False
				elif (self.isPLEFilter(self.nPLEFilterModeSea)):
					if (pUnitTypeInfo.getDomainType() != DomainTypes.DOMAIN_SEA):
						return False
				elif (self.isPLEFilter(self.nPLEFilterModeAir)):
					if (pUnitTypeInfo.getDomainType() != DomainTypes.DOMAIN_AIR):
						return False
				
				if (self.isPLEFilter(self.nPLEFilterModeMil)):
					if ((pUnitTypeInfo.getCombat() == 0) and (pUnitTypeInfo.getAirCombat() == 0)):
						return False
				elif (self.isPLEFilter(self.nPLEFilterModeDom)):
					if ((pUnitTypeInfo.getCombat() > 0) or (pUnitTypeInfo.getAirCombat() > 0)):
						return False
				
				if (self.isPLEFilter(self.nPLEFilterModeOwn)):
					if ( pUnit.getOwner() != gc.getGame().getActivePlayer() ):
						return False
				elif (self.isPLEFilter(self.nPLEFilterModeForeign)):
					if ( pUnit.getOwner() == gc.getGame().getActivePlayer() ):
						return False
		
		return True
		
	# create an info set for each unit. This set is used to determine the order of the plot list buttons.
	def getPLEUnitInfo(self, pUnit):
		if pUnit.isCargo() and (self.nPLEGrpMode != self.PLE_GRP_PROMO) and (self.nPLEGrpMode != self.PLE_GRP_UPGRADE):
			# if unit is cargo, we do retrieve the transport units characteristics to insert the cargo unit behind the transport unit in the sort list.
			pTransportUnit = pUnit.getTransportUnit()
			setUnit = self.getPLEUnitInfo(pTransportUnit)
			tReturn = (setUnit[self.IDX_PLAYER], setUnit[self.IDX_DOMAIN], setUnit[self.IDX_GROUPID], setUnit[self.IDX_COMBAT], setUnit[self.IDX_UNITTYPE], setUnit[self.IDX_LEVEL], setUnit[self.IDX_XP], pTransportUnit.getID(), pUnit.getID(), pUnit.getID(), pUnit)
			return tReturn
		else:
			# retrieve player info
			iPlayer = pUnit.getOwner()
			# get gproup id of the unit. only when display mode = group
			if (self.nPLEGrpMode == self.PLE_GRP_GROUPS):
				if (pUnit.getGroup().getNumUnits() > 1):
					iGroupID = pUnit.getGroupID()
				else:
					iGroupID = 0
			else:
				iGroupID = 0
			# retrieve domain info
			pUnitTypeInfo = gc.getUnitInfo(pUnit.getUnitType())
			eDomainType = pUnitTypeInfo.getDomainType()
			# retrieve combat strength :
			# - baseCombat is only set for ground units
			# - airBaseCombat is set used for ait units
			# - bombardRate is only set for Artillery 
			# - bombRate is only set for Bombers
			# the following calculation makes artillery/bombers listed before tanks/fighters
			iCombatStr = pUnit.baseCombatStr() + 100 * pUnit.bombardRate() + pUnit.airBaseCombatStr() + 100 * pUnitTypeInfo.getBombRate()
			# retrieve Unit type info
			eUnitType = pUnit.getUnitType()
			# retrieve unit level
			iLevel = pUnit.getLevel()
			# retrieve unit experience
			iXP = pUnit.getExperience()	
			# if unit has cargo...
			if pUnit.cargoSpace() > 0:
				iTransportUnit = pUnit.getID()
			else:
				iTransportUnit = 0
			# in case of promotion view, do not consider combat strngth, unit level and unit experience. Otherise the sorting will change during promotion process
			if (self.nPLEGrpMode == self.PLE_GRP_PROMO):
				# return negatives for some elements for descending sorting of related column.			
				tReturn = (iPlayer, eDomainType, -iGroupID, 0, -eUnitType, 0, 0, iTransportUnit, 0, pUnit.getID(), pUnit)
			else:
				# return negatives for some elements for descending sorting of related column.			
				tReturn = (iPlayer, eDomainType, -iGroupID, -iCombatStr, -eUnitType, -iLevel, -iXP, iTransportUnit, 0, pUnit.getID(), pUnit)
			return tReturn
			
	# creates a sorted unit list of the plot depending on the current grouping
	def getUnitList(self, pPlot):
		# local list to store unit order
		self.lPLEUnitList = []
		# loop for all units on the actual plot
		for i in range(pPlot.getNumUnits()):
			# retrieve single unit
			pUnit = pPlot.getUnit(i)
			# only units which are visible for the player 
			if not pUnit.isInvisible(gc.getPlayer(gc.getGame().getActivePlayer()).getTeam(), true):
				# check if the unit is loaded into any tranporter
				# append empty list element. Each element stores the following information in given order :
				lUnitInfo = self.getPLEUnitInfo(pUnit)
				self.lPLEUnitList.append( lUnitInfo )
				self.dPLEUnitInfo[ pUnit.getID() ] = lUnitInfo
		# sort list
		self.lPLEUnitList.sort()
		
	# replaces the buggy civ 4 version.
	def getInterfacePlotUnit(self, i):
		return self.lPLEUnitList[i][self.IDX_UNIT]

	# displays all the possible promotion buttons for a unit 
	def displayUnitPromos(self, screen, pUnit, nRow, nCol):
		lPromos = mt.getPossiblePromos(pUnit)
		# remove the 'Lead by Warlord' promotion, if any
		for i in range(len(lPromos)):
			if (gc.getPromotionInfo(lPromos[i]).getType() == 'PROMOTION_LEADER'):
				lPromos.pop(i)
				break
		# determine which dimension is the unit and which the promotion
		if (self.sPLEMode == self.PLE_MODE_STACK_HORIZ):
			iU = nRow
		else:
			iU = nCol
		# display the promotions
		for i in range(len(lPromos)):
			if (self.sPLEMode == self.PLE_MODE_STACK_HORIZ):
				nCol += 1
			else:
				nRow += 1
			x = self.getX( nCol )
			y = self.getY( nRow )
			if (self.sPLEMode == self.PLE_MODE_STACK_HORIZ):
				iP = nCol
			else:
				iP = nRow
			iPromo = lPromos[i]
			sID = string.zfill(str(iU), 2) + string.zfill(str(iP), 2)
			szStringUnitPromo = self.PLOT_LIST_PROMO_NAME + sID
			szFileNamePromo = gc.getPromotionInfo(iPromo).getButton()
			screen.setImageButton( szStringUnitPromo, szFileNamePromo, x, y, 32, 32, WidgetTypes.WIDGET_GENERAL, gc.getPromotionInfo(iPromo).getActionInfoIndex(), -1 )
			screen.show( szStringUnitPromo )
		self.dUnitPromoList[iU] = lPromos
		return

	# performs the units promotion
	def doPromotion(self, id):
		idPromo		= id % 100
		idUnit		= id / 100
		if self.sPLEMode == self.PLE_MODE_STACK_HORIZ:
			idButton = self.getI(idUnit, 0)
		else:
			idButton = self.getI(0, idUnit)
		pUnit 		= self.listPLEButtons[idButton][0]
		iPromo		= self.dUnitPromoList[idUnit][idPromo-1]
		pUnit.promote(iPromo, -1)
		
		
	# displays all the possible upgrade buttons for a unit 
	def displayUnitUpgrades(self, screen, pUnit, nRow, nCol):
		lUpgrades 	= []
		lUnits		= []
		
		# reading all upgrades
		lUpgrades = mt.getPossibleUpgrades(pUnit)
		
		# determine which dimension is the unit and which the upgrade
		if (self.sPLEMode == self.PLE_MODE_STACK_HORIZ):
			iU = nRow
		else:
			iU = nCol
		
		# displaying the results
		for i in range(len(lUpgrades)):
			if (self.sPLEMode == self.PLE_MODE_STACK_HORIZ):
				nCol += 1
			else:
				nRow += 1
			x = self.getX( nCol )
			y = self.getY( nRow )
			if (self.sPLEMode == self.PLE_MODE_STACK_HORIZ):
				iP = nCol
			else:
				iP = nRow
			iUnitIndex = lUpgrades[i]
			lUnits.append(iUnitIndex)
			sID = string.zfill(str(iU), 2) + string.zfill(str(iP), 2)
			szStringUnitUpgrade = self.PLOT_LIST_UPGRADE_NAME + sID
			szFileNameUpgrade = gc.getUnitInfo(iUnitIndex).getButton()
			screen.setImageButton( szStringUnitUpgrade, szFileNameUpgrade, x, y, 34, 34, WidgetTypes.WIDGET_GENERAL, iUnitIndex, -1 )
			if pUnit.canUpgrade(iUnitIndex, false):
				screen.enable(szStringUnitUpgrade, true)
			else:
				screen.enable(szStringUnitUpgrade, false)
			screen.show( szStringUnitUpgrade )
		self.dUnitUpgradeList[iU] = lUnits
		return
			
	# performs the unit upgrades
	def doUpgrade(self, id):
		idUpgrade		= id % 100
		idUnit			= id / 100
		if self.sPLEMode == self.PLE_MODE_STACK_HORIZ:
			idButton = self.getI(idUnit, 0)
		else:
			idButton = self.getI(0, idUnit)
		pUnit 			= self.listPLEButtons[idButton][0]
		iUnitType		= self.dUnitUpgradeList[idUnit][idUpgrade-1]		
		if mt.bCtrl():
			pPlot = pUnit.plot()
			iCompUnitType = pUnit.getUnitType()
			for i in range(pPlot.getNumUnits()):
				pLoopUnit = pPlot.getUnit(i)
				if (pLoopUnit.getUnitType() == iCompUnitType):
					pLoopUnit.doCommand(CommandTypes.COMMAND_UPGRADE, iUnitType, 0)
		elif mt.bAlt():
			pActPlayer = gc.getActivePlayer()
			iCompUnitType = pUnit.getUnitType()
			for i in range(pActPlayer.getNumUnits()):
				pLoopUnit = pActPlayer.getUnit(i)
				if (pLoopUnit.getUnitType() == iCompUnitType):
					pLoopUnit.doCommand(CommandTypes.COMMAND_UPGRADE, iUnitType, 0)
		else:
			pUnit.doCommand(CommandTypes.COMMAND_UPGRADE, iUnitType, 0)		

	##################### info pane (mouse over) functions ########################
		
	# handles display of the promotion button info pane
	def showPromoInfoPane(self, id):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		idPromo		= id % 100
		idUnit		= id / 100
		if self.sPLEMode == self.PLE_MODE_STACK_HORIZ:
			idButton = self.getI(idUnit, 0)
		else:
			idButton = self.getI(0, idUnit)
		pUnit 		= self.listPLEButtons[idButton][0]
		iPromo		= self.dUnitPromoList[idUnit][idPromo-1]

		# promo info
		szPromoInfo = u"<font=2>" + mt.removeLinks(CyGameTextMgr().getPromotionHelp(iPromo, false)) + u"</font>\n"

		# unit level 
		iLevel = pUnit.getLevel()
		iMaxLevel = mt.GetPossiblePromotions(pUnit.experienceNeeded(), pUnit.getExperience())
		if iMaxLevel <> iLevel:
			# actual / available (= number of possible promotions)
			szLevel = u"<font=2>" + localText.getText("INTERFACE_PANE_LEVEL", ()) + u"%i / %i" % (iLevel, (iMaxLevel+iLevel)) + u"</font>\n"
		else:
			# actual 
			szLevel = u"<font=2>" + localText.getText("INTERFACE_PANE_LEVEL", ()) + u"%i" % iLevel + u"</font>\n"

		# unit experience (actual / needed)
		iExperience = pUnit.getExperience()
		if (iExperience > 0):
			szExperience = u"<font=2>" + localText.getText("INTERFACE_PANE_EXPERIENCE", ()) + u": %i / %i" %(iExperience, pUnit.experienceNeeded()) + u"</font>\n"
		else:
			szExperience = u""
			
		szText = szPromoInfo + szLevel + szExperience
			
		# display the info pane
		self.displayInfoPane(szText)
		
	def hidePromoInfoPane(self):
		self.hideInfoPane()

	# handles display of the promotion button info pane
	def showUpgradeInfoPane(self, id):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		idUpgrade		= id % 100
		idUnit			= id / 100
		if self.sPLEMode == self.PLE_MODE_STACK_HORIZ:
			idButton = self.getI(idUnit, 0)
		else:
			idButton = self.getI(0, idUnit)
		pUnit 			= self.listPLEButtons[idButton][0]
		iUnitType		= self.dUnitUpgradeList[idUnit][idUpgrade-1]		
		pUnitTypeInfo 	= gc.getUnitInfo(iUnitType)		
		
		# reading attributes
		szUnitName 		= localText.changeTextColor(pUnitTypeInfo.getDescription(), PleOpt.getUnitNameColor()) + u"\n"
		if pUnitTypeInfo.getUnitCombatType() != -1:
			szCombatType	= gc.getUnitCombatInfo(pUnitTypeInfo.getUnitCombatType()).getDescription() + u"\n"
		else:
			szCombatType = u""
		if (pUnitTypeInfo.getAirCombat() > 0):
			iStrength = pUnitTypeInfo.getAirCombat()
		else:
			iStrength = pUnitTypeInfo.getCombat()
		szStrength = u"%i "%iStrength + u"%c" % CyGame().getSymbolID( FontSymbols.STRENGTH_CHAR )
		szMovement = u", %i "%pUnitTypeInfo.getMoves()+ u"%c" % CyGame().getSymbolID(FontSymbols.MOVES_CHAR)
		if (pUnitTypeInfo.getAirRange() > 0):
			szRange = u", " + localText.getText("TXT_KEY_UNIT_AIR_RANGE", ( pUnitTypeInfo.getAirRange(), ) ) + u"\n"
		else:
			szRange = u"\n"
		szSpecialText = mt.removeLinks(CyGameTextMgr().getUnitHelp( iUnitType, True, False, False, None )[1:]) + "\n"
			
		# determining the unit upgrade price
		iUpgradePriceSingle 	= mt.getUpgradePrice(pUnit, iUnitType, 0)
	#		iUpgradePriceGrp 		= mt.getUpgradePrice(pUnit, iUnitType, 1)
		iUpgradePricePlot 		= mt.getUpgradePrice(pUnit, iUnitType, 2)
		iUpgradePriceAll 		= mt.getUpgradePrice(pUnit, iUnitType, 3)
		
		iGold = gc.getActivePlayer().getGold()	
		if iUpgradePriceSingle > iGold:
			szUpgradePriceSingle = localText.changeTextColor(u"%i"%iUpgradePriceSingle, PleOpt.getUpgradeNotPossibleColor())
		else:
			szUpgradePriceSingle = localText.changeTextColor(u"%i"%iUpgradePriceSingle, PleOpt.getUpgradePossibleColor())
		if iUpgradePricePlot > iGold:
			szUpgradePricePlot = localText.changeTextColor(u"%i"%iUpgradePricePlot, PleOpt.getUpgradeNotPossibleColor())
		else:
			szUpgradePricePlot = localText.changeTextColor(u"%i"%iUpgradePricePlot, PleOpt.getUpgradePossibleColor())
		if iUpgradePriceAll > iGold:
			szUpgradePriceAll = localText.changeTextColor(u"%i"%iUpgradePriceAll, PleOpt.getUpgradeNotPossibleColor())
		else:
			szUpgradePriceAll = localText.changeTextColor(u"%i"%iUpgradePriceAll, PleOpt.getUpgradePossibleColor())
		
		szUpgradePrice = szUpgradePriceSingle + u" / " + szUpgradePricePlot + u" / " + szUpgradePriceAll+ u" %c" %  gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar() + u"\n"
		
		szUpgradeHelp = localText.getText("TXT_KEY_PLE_UPGRADE_HELP", () )		

		szText 		= u"<font=2>" + szUnitName + \
						szCombatType  + \
						szStrength  + \
						szMovement + \
						szRange  + \
						szSpecialText + \
						szUpgradePrice + \
						szUpgradeHelp + \
					u"</font>"
					
		# display the info pane
		self.displayInfoPane(szText)
				
	def hideUpgradeInfoPane(self):
		self.hideInfoPane()
				
	# handles the display of the unit's info pane
	def showUnitInfoPane(self, id):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pUnit = self.listPLEButtons[id][0]
		try:
			iUnitType = pUnit.getUnitType()
		except:
			return

		pUnitTypeInfo = gc.getUnitInfo(iUnitType)
		eUnitDomain = pUnitTypeInfo.getDomainType()

		#mt.debug("id:%i; iUnit:%i"%(id, iUnit))

		# get units owner name if its not a player unit
		if (pUnit.getOwner() != gc.getGame().getActivePlayer()):
			pOwner = gc.getPlayer(pUnit.getOwner())
			szOwner = u"<font=2> [" + localText.changeTextColor(pOwner.getName(), pOwner.getPlayerColor()) + u"]</font>"
		else:
			szOwner = u""

		# unit type description + unit name (if given)
		szUnitName = u"<font=2>" + localText.changeTextColor(pUnit.getName(), PleOpt.getUnitNameColor()) + szOwner + u"</font>\n"

		# strength 
		if (eUnitDomain == DomainTypes.DOMAIN_AIR):
			fCurrStrength 	= float(pUnit.airBaseCombatStr() * pUnit.currHitPoints()) / pUnit.maxHitPoints()
			fMaxStrength 	= float(pUnit.airBaseCombatStr())
		else:
			fCurrStrength 	= float(pUnit.baseCombatStr())*float(1.0-pUnit.getDamage()*0.01)
			fMaxStrength 	= float(pUnit.baseCombatStr())
		if fCurrStrength != fMaxStrength:
			if float(fMaxStrength*float(mt.getPlotHealFactor(pUnit))*0.01) == 0:
				iTurnsToHeal = 999
			else:
				iTurnsToHeal 		= int((fMaxStrength-fCurrStrength)/float(fMaxStrength*float(mt.getPlotHealFactor(pUnit))*0.01)+0.999) # force to round upwards
			szCurrStrength 		= u" %.1f" % fCurrStrength
			szMaxStrength 		= u" / %i" % fMaxStrength
			if mt.getPlotHealFactor(pUnit) != 0:
				szTurnsToHeal 		= u" (%i)" % iTurnsToHeal
			else:
				szTurnsToHeal = u" (Not Healing)"
		else: 
			iTurnsToHeal 		= 0
			szCurrStrength 		= u" %i" % fCurrStrength
			szMaxStrength 		= u""		
			szTurnsToHeal 		= u""
		szStrength = u"<font=2>" + szCurrStrength + szMaxStrength + szTurnsToHeal + u"%c" % CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR) + u"</font>\n" 
			
		# movement
		fCurrMoves = float(pUnit.movesLeft()) / gc.getMOVE_DENOMINATOR()
		iMaxMoves = pUnit.baseMoves()
		if (eUnitDomain == DomainTypes.DOMAIN_AIR):
			szAirRange 		= u", " + localText.getText("TXT_KEY_UNIT_AIR_RANGE", ( pUnit.airRange(), ) ) 
		else:
			szAirRange 		= u""
		if ( pUnit.movesLeft() != iMaxMoves * gc.getMOVE_DENOMINATOR() ):
			szCurrMoves = u" %.1f" % fCurrMoves
			szMaxMoves 	= u"/%d" % iMaxMoves
		else:
			szCurrMoves = u" %d" % iMaxMoves
			szMaxMoves 	= u""
		szMovement = u"<font=2>" + szCurrMoves + szMaxMoves + u"%c"%(CyGame().getSymbolID(FontSymbols.MOVES_CHAR)) + szAirRange + u"</font>\n"

		# compressed display for standard display
		szStrengthMovement = u"<font=2>" + szCurrStrength + szMaxStrength + szTurnsToHeal + u"%c" % CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR) + ", " + \
							szCurrMoves + szMaxMoves + u"%c"%(CyGame().getSymbolID(FontSymbols.MOVES_CHAR)) + szAirRange + u"</font>\n"
							
		# civilization type
		szCiv = u""
	#		iCiv = pUnit.getCivilizationType()
	#		for i in range(gc.getMAX_PLAYERS()):
	#			pLoopPlayer = gc.getPlayer(i)
	#			if pLoopPlayer.getCivilizationType() == iCiv:
	#				break
	#		szCiv = u"<font=2>100% " + localText.changeTextColor(pLoopPlayer.getCivilizationAdjective(0), pLoopPlayer.getPlayerColor()) + u"</font>\n"

		# unit level
		iLevel = pUnit.getLevel()
		iMaxLevel = mt.GetPossiblePromotions(pUnit.experienceNeeded(), pUnit.getExperience())
		if (iMaxLevel > 0) or (iLevel > 1):
			if iMaxLevel <> iLevel:
				szLevel = u"<font=2>" + localText.getText("INTERFACE_PANE_LEVEL", ()) + u" %i / %i" % (iLevel, (iMaxLevel+iLevel)) + u"</font>\n"
			else:
				szLevel = u"<font=2>" + localText.getText("INTERFACE_PANE_LEVEL", ()) + u" %i" % iLevel + u"</font>\n"
		else:
			szLevel = u""

		# unit experience (actual / needed (possible promos))
		iExperience = pUnit.getExperience()
		if (iExperience > 0):
			szExperience = u"<font=2>" + localText.getText("INTERFACE_PANE_EXPERIENCE", ()) + u": %i / %i" %(iExperience, pUnit.experienceNeeded()) + u"</font>\n"
		else:
			szExperience = u""

		# cargo space
		iCargoSpace = pUnit.cargoSpace()
		if iCargoSpace > 0:
			iCargo = pUnit.getCargo()
			szCargo = u"<font=2>" + localText.getText("TXT_KEY_UNIT_HELP_CARGO_SPACE", (iCargo, iCargoSpace ) ) + u"</font>\n"
		else:
			szCargo = u""
				
		# fortify bonus
		szFortifyBonus = u"" 
		iFortifyBonus = pUnit.fortifyModifier()
		if iFortifyBonus > 0:
			szFortifyBonus = u"<font=2>" + localText.getText("TXT_KEY_UNIT_HELP_FORTIFY_BONUS", (iFortifyBonus, )) + u"\n" + u"</font>"

		# espionage info; mimic of CvGameTextMgr::setEspionageMissionHelp()
		szEspionage = u""
		if gc.getUnitInfo(pUnit.getUnitType()).isSpy():
			pPlot = pUnit.plot()
			eOwner = pPlot.getOwner()
			pOwner = gc.getPlayer(eOwner)
			if pOwner and not pOwner.isNone():
				eOwnerTeam = pOwner.getTeam()
				if eOwnerTeam != pUnit.getTeam():
					if not pUnit.canEspionage(pPlot):
						szEspionage += localText.getText("TXT_KEY_UNIT_HELP_NO_ESPIONAGE", ())
						if pUnit.hasMoved() or pUnit.isMadeAttack():
							szEspionage += localText.getText("TXT_KEY_UNIT_HELP_NO_ESPIONAGE_REASON_MOVED", ())
						elif not pUnit.isInvisible(eOwnerTeam, False):
							szEspionage += localText.getText("TXT_KEY_UNIT_HELP_NO_ESPIONAGE_REASON_VISIBLE", (pOwner.getNameKey(),))
					elif pUnit.getFortifyTurns() > 0:
						iModifier = - (pUnit.getFortifyTurns() * gc.getDefineINT("ESPIONAGE_EACH_TURN_UNIT_COST_DECREASE"))
						if 0 != iModifier:
							szEspionage += localText.getText("TXT_KEY_ESPIONAGE_COST", (iModifier,))
		if szEspionage:
			szEspionage = u"<font=2>" + szEspionage + u"\n</font>"
		
		# unit type specialities 
		szSpecialText 	= u"<font=2>" + localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()) + u":\n" + CyGameTextMgr().getUnitHelp( iUnitType, true, false, false, None )[1:] + u"</font>"
		szSpecialText = localText.changeTextColor(szSpecialText, PleOpt.getUnitTypeSpecialtiesColor())
		
		if iLevel > 1:
			szSpecialText += "\n" + localText.changeTextColor(mt.getPromotionInfoText(pUnit), PleOpt.getPromotionSpecialtiesColor())
		szSpecialText = mt.removeLinks(szSpecialText)

		# count the promotions
		szPromotion = u""
		iPromotionCount = 0
		for i in range(gc.getNumPromotionInfos()):
			if pUnit.isHasPromotion(i):
				iPromotionCount += 1
		if iPromotionCount > 0:
			szPromotion = u"\n"*((iPromotionCount/self.CFG_INFOPANE_BUTTON_PER_LINE)+1)

		# build text
		szText 	= szUnitName + \
				szPromotion + \
				szStrengthMovement + \
				szLevel + \
				szExperience + \
				szCargo + \
				szCiv + \
				szFortifyBonus + \
				szEspionage + \
				szSpecialText

		# display the info pane
		dy = self.displayInfoPane(szText)
					
		# show promotion buttons
		iTemp = 0
		for i in range(gc.getNumPromotionInfos()):
			if pUnit.isHasPromotion(i):
				szName = self.PLE_PROMO_BUTTONS_UNITINFO + str(i)
				self.displayUnitInfoPromoButtonPos( szName, iTemp, dy - self.CFG_INFOPANE_PIX_PER_LINE_1 + PleOpt.getInfoPanePromoIconOffsetY() )
				screen.show( szName )
				iTemp += 1
							
	def hideUnitInfoPane(self):
		self.hideUnitInfoPromoButtons()
		self.hideInfoPane()
		
	def hideUnitInfoPromoButtons(self):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		for i in range(gc.getNumPromotionInfos()):
			szName = self.PLE_PROMO_BUTTONS_UNITINFO + str(i)
			screen.hide( szName )
		self.bUnitPromoButtonsActive = false

	# displays the unit's promotion buttons in the info pane. They are not part of the info pane.
	def displayUnitInfoPromoButtonPos( self, szName, iPromotionCount, yOffset ):
		self.bUnitPromoButtonsActive = true
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			y = self.CFG_INFOPANE_Y
		else:
			y = self.CFG_INFOPANE_Y2
		screen.moveItem( szName, PleOpt.getInfoPaneX() + 4 + (self.CFG_INFOPANE_BUTTON_SIZE * (iPromotionCount % self.CFG_INFOPANE_BUTTON_PER_LINE)), \
								 y + 4 - yOffset + (self.CFG_INFOPANE_BUTTON_SIZE * (iPromotionCount / self.CFG_INFOPANE_BUTTON_PER_LINE)), -0.3 )
		screen.moveToFront( szName )

	# calculates the height of a text in pixels
	def getTextLines(self, szText):
		szText = mt.removeFonts(szText)
		szText = mt.removeColor(szText)
		szText = mt.removeLinks(szText)
		iNormalLines = 0
		iBulletLines = 0
		lChapters = szText.split('\n')
		sComp = u"%c"%CyGame().getSymbolID(FontSymbols.BULLET_CHAR)
		for i in range(len(lChapters)):
			iLen = len(lChapters[i])
			iWidth = CyInterface().determineWidth(lChapters[i])/(self.CFG_INFOPANE_DX-3)+1
			if (lChapters[i].find(sComp) != -1):
				iBulletLines += iWidth
			else:
				iNormalLines += iWidth
		dy = iNormalLines*self.CFG_INFOPANE_PIX_PER_LINE_1 + (iBulletLines)*self.CFG_INFOPANE_PIX_PER_LINE_2 + 20
		return dy
		
	# base function to display a self sizing info pane
	def displayInfoPane(self, szText):

		self.bInfoPaneActive 	= True
		self.iInfoPaneCnt  		+= 1
		self.tLastMousePos 		= (CyInterface().getMousePos().x, CyInterface().getMousePos().y)

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		# calculate text size
		dy = self.getTextLines(szText)
		
		# draw panel
		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			y = self.CFG_INFOPANE_Y
		else:
			y = self.CFG_INFOPANE_Y2
		dx = 0
		if ( CyInterface().isCityScreenUp()):
			dx = 260
		
		screen.addPanel( self.UNIT_INFO_PANE, u"", u"", True, True, \
						PleOpt.getInfoPaneX() + dx, y - dy, self.CFG_INFOPANE_DX, dy, \
						PanelStyles.PANEL_STYLE_HUD_HELP )
		
		# create shadow text
		szTextBlack = localText.changeTextColor(mt.removeColor(szText), gc.getInfoTypeForString("COLOR_BLACK"))
		
		# display shadow text
		screen.addMultilineText( self.UNIT_INFO_TEXT_SHADOW, szTextBlack, \
								PleOpt.getInfoPaneX() + dx + 5, y - dy + 5, \
								self.CFG_INFOPANE_DX - 3, dy - 3, \
								WidgetTypes.WIDGET_GENERAL, -1, -1, \
								CvUtil.FONT_LEFT_JUSTIFY)
		# display text
		screen.addMultilineText( self.UNIT_INFO_TEXT, szText, \
								PleOpt.getInfoPaneX() + dx + 4, y - dy + 4, \
								self.CFG_INFOPANE_DX - 3, dy - 3, \
								WidgetTypes.WIDGET_GENERAL, -1, -1, \
								CvUtil.FONT_LEFT_JUSTIFY)
					
		return dy

	def checkInfoPane(self, tMousePos):
		if self.bInfoPaneActive and (self.iInfoPaneCnt == (self.iLastInfoPaneCnt+1)): 
			if (tMousePos.x < self.tLastMousePos[0]-self.iMousePosTol) or \
				(tMousePos.x > self.tLastMousePos[0]+self.iMousePosTol) or \
				(tMousePos.y < self.tLastMousePos[1]-self.iMousePosTol) or \
				(tMousePos.y > self.tLastMousePos[1]+self.iMousePosTol):
				self.hideInfoPane()
				if self.bUnitPromoButtonsActive:
					self.hideUnitInfoPromoButtons()


	#################### functions for a units move area #######################
		
	# highlights the move area
	def highlightMoves(self, id):
		if PleOpt.isShowMoveHighlighter():
			pUnit = self.listPLEButtons[id][0]
			self.ASMA.highlightMoveArea(pUnit)

	# hides the move area
	def dehighlightMoves(self):
		if PleOpt.isShowMoveHighlighter():
			self.ASMA.dehighlightMoveArea()
		

	################## set / get PLE values ##################
	def setPLEUnitList(self, bValue):
		self.bUpdatePLEUnitList = bValue

	def getPLEUnitList(self):
		return self.bUpdatePLEUnitList








	def _displayUnitPlotList_Dot( self, screen, pLoopUnit, szString, iCount, x, y ):
		# this if statement and everything inside, handles the display of the colored buttons in the upper left corner of each unit icon.
		xSize = 12
		ySize = 12
		xOffset = 0
		yOffset = 0
		if ((pLoopUnit.getTeam() != gc.getGame().getActiveTeam()) or pLoopUnit.isWaiting()):
			# fortified
			szDotState = "OVERLAY_FORTIFY"
		elif (pLoopUnit.canMove()):
			if (pLoopUnit.hasMoved()):
				# unit moved, but some movement points are left
				szDotState = "OVERLAY_HASMOVED"
			else:
				# unit did not move yet
				szDotState = "OVERLAY_MOVE"
		else:
			# unit has no movement points left
			szDotState = "OVERLAY_NOMOVE"

		# Wounded units will get a darker colored button.
		if (self.bShowWoundedIndicator) and (pLoopUnit.isHurt()):
			szDotState += "_INJURED"

		# Units lead by a GG will get a star instead of a dot.
		if (self.bShowGreatGeneralIndicator):
			# is unit lead by a GG?
			iLeaderPromo = gc.getInfoTypeForString('PROMOTION_LEADER')
			if (iLeaderPromo != -1 and pLoopUnit.isHasPromotion(iLeaderPromo)):
				szDotState += "_GG"
				xSize = 16
				ySize = 16
				xOffset = -3
				yOffset = -3

		szFileNameState = ArtFileMgr.getInterfaceArtInfo(szDotState).getPath()

		# display the colored spot icon
		szStringIcon = szString+"Icon"
		screen.addDDSGFC( szStringIcon, szFileNameState, x-3+xOffset, y-7+yOffset, xSize, ySize, WidgetTypes.WIDGET_GENERAL, iCount, -1 )
		screen.show( szStringIcon )

		return 0

	def _displayUnitPlotList_Promo( self, screen, pLoopUnit, szString ):
		if (self.bShowPromotionIndicator):
			# can unit be promoted ?
			if (pLoopUnit.isPromotionReady()):
				# place the promotion frame
				szStringPromoFrame = szString+"PromoFrame"
				screen.show( szStringPromoFrame )

		return 0

	def _displayUnitPlotList_Upgrade( self, screen, pLoopUnit, szString, iCount, x, y ):
		if (self.bShowUpgradeIndicator):
			# can unit be upgraded ?
			if (mt.checkAnyUpgrade(pLoopUnit)):
				# place the upgrade arrow
				szStringUpgrade = szString+"Upgrade"
				szFileNameUpgrade = ArtFileMgr.getInterfaceArtInfo("OVERLAY_UPGRADE").getPath()	
				screen.addDDSGFC( szStringUpgrade, szFileNameUpgrade, x+2, y+14, 8, 16, WidgetTypes.WIDGET_GENERAL, iCount, -1 )
				screen.show( szStringUpgrade )

		return 0

	def _displayUnitPlotList_HealthBar( self, screen, pLoopUnit, szString ):
		if (self.bShowHealthBar and pLoopUnit.maxHitPoints()
		and not (pLoopUnit.isFighting() and self.bHideHealthBarWhileFighting)):
			# place the health bar
			szStringHealthBar = szString+"HealthBar"
			screen.setBarPercentage( szStringHealthBar, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
			screen.setBarPercentage( szStringHealthBar, InfoBarTypes.INFOBAR_RATE, float(1.0) )

			# EF: Colors are set by user instead
			#if (pLoopUnit.getDamage() >= ((pLoopUnit.maxHitPoints() * 2) / 3)):
			#	screen.setStackedBarColors(szStringHealthBar, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RED"))
			#elif (pLoopUnit.getDamage() >= (pLoopUnit.maxHitPoints() / 3)):
			#	screen.setStackedBarColors(szStringHealthBar, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_YELLOW"))
			#else:
			#	screen.setStackedBarColors(szStringHealthBar, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREEN"))	

			screen.show( szStringHealthBar )

		return 0

	def _displayUnitPlotList_MoveBar( self, screen, pLoopUnit, szString ):
		if (self.bShowMoveBar):
			# place the move bar
			szStringMoveBar = szString+"MoveBar"
			if (pLoopUnit.movesLeft() == 0 or pLoopUnit.baseMoves() == 0):
				screen.setBarPercentage( szStringMoveBar, InfoBarTypes.INFOBAR_STORED, 0.0 )
				screen.setBarPercentage( szStringMoveBar, InfoBarTypes.INFOBAR_RATE, 0.0 )
				screen.setBarPercentage( szStringMoveBar, InfoBarTypes.INFOBAR_EMPTY, 1.0 )
			else:
				fMaxMoves = float(pLoopUnit.baseMoves())
				#fCurrMoves = fMaxMoves - (pLoopUnit.getMoves() / float(gc.getMOVE_DENOMINATOR())) 
				fCurrMoves = float(pLoopUnit.movesLeft()) / float(gc.getMOVE_DENOMINATOR()) 
				# mt.debug("c/m/r:%f/%f/%f"%(fCurrMoves, fMaxMoves, float( fCurrMoves ) / float( fMaxMoves ) ))
				if (fMaxMoves):
					screen.setBarPercentage( szStringMoveBar, InfoBarTypes.INFOBAR_STORED, fCurrMoves / fMaxMoves )
				else:
					screen.setBarPercentage( szStringMoveBar, InfoBarTypes.INFOBAR_STORED, 1.0 )
				screen.setBarPercentage( szStringMoveBar, InfoBarTypes.INFOBAR_RATE, 1.0 )
				screen.setBarPercentage( szStringMoveBar, InfoBarTypes.INFOBAR_EMPTY, 1.0 )
			screen.show( szStringMoveBar )

		return 0

	def _displayUnitPlotList_Mission( self, screen, pLoopUnit, szString, iCount, x, y, iSize ):
		# display the mission or activity info
		if (self.bShowMissionInfo): 
			# TODO: Switch to UnitUtil.getOrder()
			# place the activity info below the unit icon.
			szFileNameAction = ""
			eActivityType = pLoopUnit.getGroup().getActivityType()
			eAutomationType = pLoopUnit.getGroup().getAutomateType()

			# is unit on air intercept mission
			if (eActivityType == ActivityTypes.ACTIVITY_INTERCEPT):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_INTERCEPT").getPath()
			# is unit on boat patrol coast mission
			elif (eActivityType == ActivityTypes.ACTIVITY_PATROL):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_PATROL").getPath()
			# is unit on boat blockade mission
			elif (eActivityType == ActivityTypes.ACTIVITY_PLUNDER):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_PLUNDER").getPath()
			# is unit fortified for healing (wake up when healed)
			elif (eActivityType == ActivityTypes.ACTIVITY_HEAL):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_HEAL").getPath()
			# is unit sentry (wake up when enemy in sight)
			elif (eActivityType == ActivityTypes.ACTIVITY_SENTRY):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_SENTRY").getPath()
			# is the turn for this unit skipped (wake up next turn)
			elif (eActivityType == ActivityTypes.ACTIVITY_HOLD):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_SKIP").getPath()
			# has unit exploration mission
			elif (eAutomationType == AutomateTypes.AUTOMATE_EXPLORE):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_EXPLORE").getPath()
			# is unit automated generally (only worker units)
			elif (eAutomationType == AutomateTypes.AUTOMATE_BUILD):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_AUTO_BUILD").getPath()
			# is unit automated for nearest city (only worker units)
			elif (eAutomationType == AutomateTypes.AUTOMATE_CITY):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_AUTO_CITY").getPath()
			# is unit automated for network (only worker units)
			elif (eAutomationType == AutomateTypes.AUTOMATE_NETWORK):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_AUTO_NETWORK").getPath()
			# is unit automated spread religion (only missionary units)
			elif (eAutomationType == AutomateTypes.AUTOMATE_RELIGION):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_AUTO_RELIGION").getPath()
			# has unit a mission
			elif (pLoopUnit.getGroup().getLengthMissionQueue() > 0):
				eMissionType = pLoopUnit.getGroup().getMissionType(0)
				# is the mission to build an improvement
				if (eMissionType == MissionTypes.MISSION_BUILD):
					szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_BUILD").getPath()
				# is the mission a "move to" mission
				elif (eMissionType in UnitUtil.MOVE_TO_MISSIONS):
					szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_GOTO").getPath()
			# if nothing of above, but unit is waiting -> unit is fortified
			elif (pLoopUnit.isWaiting()):
				if (pLoopUnit.isFortifyable()):
					szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_FORTIFY").getPath()
				else:
					szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_SLEEP").getPath()

			# display the mission icon
			if (szFileNameAction != ""):
				szStringActionIcon = szString+"ActionIcon"
				screen.addDDSGFC( szStringActionIcon, szFileNameAction, x+20, y+20, iSize, iSize, WidgetTypes.WIDGET_GENERAL, iCount, -1 )
				screen.show( szStringActionIcon )

		return 0