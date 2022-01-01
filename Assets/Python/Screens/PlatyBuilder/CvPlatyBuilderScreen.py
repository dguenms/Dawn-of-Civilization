from CvPythonExtensions import *
import CvUtil
import CvScreensInterface
import ScreenInput
import CvEventInterface
import CvScreenEnums
import time
import WBPlotScreen
import WBEventScreen
import WBCityEditScreen
import WBCityDataScreen
import WBBuildingScreen
import WBUnitScreen
import WBPromotionScreen
import WBGameDataScreen
import WBReligionScreen
import WBCorporationScreen
import WBDiplomacyScreen
import WBPlayerScreen
import WBTeamScreen
import WBTechScreen
import WBProjectScreen
import WBPlayerUnits
import WBInfoScreen
import WBTradeScreen
import CvEventManager
import Popup
import CityNameManager as cnm
import WBStoredDataScreen

from CvPlatyBuilderSettings import *

from Consts import *
from RFCUtils import *
import MapEditorTools as met
import SettlerMaps
import WarMaps
import RegionMap
import DynamicCivs as dc
import GreatPeople as gp

from Core import *

localText = CyTranslator()

gc = CyGlobalContext()

iNumModes = 45
(iModeOwnership, iModeUnits, iModeBuildings, iModeCity, iModeStartingPlot, iModeAddLandMark, iModePlotData, iModeRiver, iModeImprovements, iModeBonus,
iModePlotType, iModeTerrain, iModeRoutes, iModeFeatures, iModeFlip, iModeCore, iModeSettlerValue, iModeWarMap, iModeReligionMap, iModeRegionMap,
iModeVictoryMap, iModeRevealPlot, iModeInvisibleSubmarine, iModeInvisibleStealth, iModeBlockade, iModeInvisibleSatellite, iModeAreaExporter1, iModeAreaExporter2, iModeAreaExporter3, iModeMoveMap,
iModeMoveMap2, iModeEditUnit, iModeEditCity, iModeEraseAll, iModeCityDataI, iModePromotions, iModeCityDataII, iModeCityBuildings, iModeMoveCity, iModeMoveCityPlus,
iModeDuplicateCity, iModeDuplicateCityPlus, iModeTargetPlot, iModeMoveUnits, iModeEvents) = range(iNumModes)

lPlayerModes = [iModeOwnership, iModeUnits, iModeBuildings, iModeCity, iModeStartingPlot]
lMapModes = [iModeAddLandMark, iModePlotData, iModeRiver, iModeImprovements, iModeBonus, iModePlotType, iModeTerrain, iModeRoutes, iModeFeatures]
lDoCMapModes = [iModeFlip, iModeCore, iModeSettlerValue, iModeWarMap, iModeReligionMap, iModeRegionMap, iModeVictoryMap]
lRevealModes = [iModeRevealPlot, iModeInvisibleSubmarine, iModeInvisibleStealth, iModeBlockade, iModeInvisibleSatellite]
lAreaExportModes = [iModeAreaExporter1, iModeAreaExporter2, iModeAreaExporter3]
lMoveMapModes = [iModeMoveMap, iModeMoveMap2]

class CvWorldBuilderScreen:

	def __init__ (self) :
		self.m_advancedStartTabCtrl = None
		self.m_bShowBigBrush = False
		self.m_bChangeFocus = False
		self.m_iAdvancedStartCurrentIndexes = []
		self.m_iAdvancedStartCurrentList = []
		self.m_iCurrentPlayer = 0
		self.m_iCurrentTeam = 0
		self.m_pCurrentPlot = 0
		self.m_pRiverStartPlot = -1
		self.m_iCurrentReligion = 0
		self.m_iReligionMapValue = 0
		self.m_iRegionMapID = 0

		self.m_iASUnitTabID = 2
		self.m_iASUnitListID = 0
		self.m_iASCityTabID = 0
		self.m_iASCityListID = 0
		self.m_iASBuildingsListID = 2
		self.m_iASAutomateListID = 1
		self.m_iASImprovementsTabID = 1
		self.m_iASRoutesListID = 0
		self.m_iASImprovementsListID = 1
		self.m_iASVisibilityTabID = 4
		self.m_iASVisibilityListID = 0
		self.m_iASTechTabID = 5
		self.m_iASTechListID = 0

		self.m_bSideMenuDirty = False
		self.m_bASItemCostDirty = False
		self.m_iCost = 0

## Platy Builder ##
		self.iBrushWidth = 1
		self.iBrushHeight = 1
		self.iPlayerAddMode = iModeUnits
		self.iSelection = -1
		self.iSelectClass = -2
		self.bSensibility = True
		self.bRegion = False
		self.bVictoryRectangle = False
		self.lMoveUnit = []
		self.iMoveCity = -1
		self.TempInfo = []
## Platy Builder ##

		self.lCurrentFlipZone = []
		self.dFlipZoneEdits = {}
		self.bFlipAI = False
		self.iMoveMapReset = 0
		self.bWaterException = False
		self.bPeaksException = False
		self.bAllRegions = False
		self.dRegionColors = {}

	def interfaceScreen (self):
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN )
		self.__init__()
		self.m_iCurrentPlayer = active()
		self.m_iCurrentTeam = gc.getPlayer(self.m_iCurrentPlayer).getTeam()
		screen.setCloseOnEscape(False)
		screen.setAlwaysShown(True)
		self.setSideMenu()
		self.refreshSideMenu()
		self.refreshAdvancedStartTabCtrl(False)

		if CyInterface().isInAdvancedStart():
			pPlayer = gc.getPlayer(self.m_iCurrentPlayer)
			pPlot = pPlayer.getStartingPlot()
			CyCamera().JustLookAtPlot(pPlot)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)
		screen.setForcedRedraw(True)

	def killScreen(self):
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN )
		screen.hideScreen()
		CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_HIGHLIGHT_PLOT)

	def mouseOverPlot (self, argsList):
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN )
		self.m_pCurrentPlot = CyInterface().getMouseOverPlot()
		x, y = location(self.m_pCurrentPlot)
		iPlayer = self.m_iCurrentPlayer
		if not CyInterface().isInAdvancedStart():
			sText = "<font=3b>%s, X: %d, Y: %d</font>" %(CyTranslator().getText("TXT_KEY_WB_LATITUDE",(self.m_pCurrentPlot.getLatitude(),)), x, y)
			screen.setLabel( "WBCoords", "Background", sText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			if self.iPlayerAddMode in lDoCMapModes + [iModeCity]:
				sDoCText = ""
				if self.iPlayerAddMode == iModeReligionMap:
					iValue = self.m_pCurrentPlot.getSpreadFactor(self.m_iCurrentReligion)
					if iValue != -1:
						sDoCText += "<font=3b>%s</font>" % (gc.getReligionInfo(self.m_iCurrentReligion).getDescription() + ": " + localText.getText(lReligionMapTexts[iValue], ()))
				elif self.iPlayerAddMode == iModeRegionMap:
					iRegion = self.m_pCurrentPlot.getRegionID()
					if iRegion != -1:
						TextKey = u"TXT_KEY_REGION_%d" % iRegion
						sDoCText += "<font=3b>%s</font>" % CyTranslator().getText(str(TextKey), ())
				elif self.iPlayerAddMode == iModeVictoryMap:
					sVictoryText = CvScreensInterface.getVictoryTooltip((iPlayer, x, y))
					if sVictoryText:
						sDoCText += "<font=3b>%s</font>" % sVictoryText
				else:
					# CNM and settlervalue
					if x > -1 and y > -1: #If you move you mouse to fast, I cannot always keep track of the current tile, which can lead to pythex
						sCityName = cnm.getFoundName(iPlayer, (x, y))
						sDoCText += "<font=3b>%s</font>" % sCityName
					if self.iPlayerAddMode == iModeWarMap:
						iPlotWarValue = self.m_pCurrentPlot.getPlayerWarValue(iPlayer)
						sDoCText += "<font=3b>   %s: %d</font>" %(localText.getText("TXT_KEY_WB_WARVALUE", ()), iPlotWarValue)
					else:
						iPlotSettlerValue = self.m_pCurrentPlot.getPlayerSettlerValue(iPlayer)
						sDoCText += "<font=3b>   %s: %d</font>" %(localText.getText("TXT_KEY_WB_SETTLERVALUE", ()), iPlotSettlerValue)
				if sDoCText == "":
					screen.deleteWidget("CNMName")
				else:
					screen.setLabel("CNMName", "Background", sDoCText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 30, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			else:
				screen.deleteWidget("CNMName")

		if self.iPlayerAddMode in lRevealModes:
			if CyInterface().isLeftMouseDown():
				self.setMultipleReveal(True)
			elif CyInterface().isRightMouseDown():
				self.setMultipleReveal(False)

		else:
			if CyInterface().isLeftMouseDown():
				if self.useLargeBrush():
					self.placeMultipleObjects()
				else:
					self.placeObject()
				self.updateOverlay()
			elif CyInterface().isRightMouseDown():
				if self.useLargeBrush():
					self.removeMultipleObjects()
				else:
					self.removeObject()
				self.updateOverlay()
		return

	def getHighlightPlot (self, argsList):
		self.refreshASItemCost()
		if self.m_pCurrentPlot != 0:
			if CyInterface().isInAdvancedStart():
				if self.m_iCost <= 0:
					return []

		if self.m_pCurrentPlot != 0 and not self.m_bShowBigBrush and isMouseOverGameSurface():
			return location(self.m_pCurrentPlot)
		return []

	def update(self, fDelta):
		if not self.m_bChangeFocus and not isMouseOverGameSurface():
			self.m_bChangeFocus = True
		if self.m_bChangeFocus and isMouseOverGameSurface() and self.iPlayerAddMode not in [iModeEditUnit, iModeEditCity]:
			self.m_bChangeFocus = False
			setFocusToCVG()
		return

	# Will update the screen (every 250 MS)
	def updateScreen(self):
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN )

		if CyInterface().isInAdvancedStart():
			if self.m_bSideMenuDirty:
				self.refreshSideMenu()
			if self.m_bASItemCostDirty:
				self.refreshASItemCost()

		if CyInterface().isDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT) and not CyInterface().isFocusedWidget():
			self.refreshAdvancedStartTabCtrl(True)
			CyInterface().setDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT, False)

		self.m_bShowBigBrush = self.useLargeBrush()
		if self.iPlayerAddMode == iModeRiver:
			if self.m_pRiverStartPlot != -1:
				self.setRiverHighlights()
				return 0
		if self.m_bShowBigBrush:
			self.highlightBrush()
		return 0

	def highlightBrush(self):
		if self.iPlayerAddMode == iModeStartingPlot: return
		if self.m_pCurrentPlot == 0: return
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
		lPlots = self.getMultiplePlotData()
		for pPlot in lPlots:
			if pPlot.isNone(): continue
			CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER, "COLOR_GREEN", 1)

	def refreshReveal(self) :
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
		for plot in plots.all():
			self.showRevealed(plot)

	def refreshStartingPlots(self) :
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
		for iPlayer in players.major():
			pPlayer = player(iPlayer)
			plot = pPlayerX.getStartingPlot()
			if not plot.isNone():
				sColor = gc.getColorInfo(gc.getPlayerColorInfo(pPlayer.getPlayerColor()).getColorTypePrimary()).getType()
				CyEngine().fillAreaBorderPlotAlt(plot.getX(), plot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS, sColor, 1.0)

	########################################################
	### Advanced Start Stuff
	########################################################

	def refreshASItemCost(self):
		if CyInterface().isInAdvancedStart():
			self.m_iCost = 0
			if self.m_pCurrentPlot != 0:
				if self.m_pCurrentPlot.isRevealed(CyGame().getActiveTeam(), False):

					# Unit mode
					if self.getASActiveUnit() != -1:
						self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartUnitCost(self.getASActiveUnit(), True, self.m_pCurrentPlot)
					elif self.getASActiveCity() != -1:
						self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartCityCost(True, self.m_pCurrentPlot)
					elif self.getASActivePop() != -1 and self.m_pCurrentPlot.isCity():
						self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartPopCost(True, self.m_pCurrentPlot.getPlotCity())
					elif self.getASActiveCulture() != -1 and self.m_pCurrentPlot.isCity():
						self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartCultureCost(True, self.m_pCurrentPlot.getPlotCity())
					elif self.getASActiveBuilding() != -1 and self.m_pCurrentPlot.isCity():
						self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartBuildingCost(self.getASActiveBuilding(), True, self.m_pCurrentPlot.getPlotCity())
					elif self.getASActiveRoute() != -1:
						self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartRouteCost(self.getASActiveRoute(), True, self.m_pCurrentPlot)
					elif self.getASActiveImprovement() != -1:
						self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartImprovementCost(self.getASActiveImprovement(), True, self.m_pCurrentPlot)

				elif (self.m_pCurrentPlot.isAdjacentNonrevealed(CyGame().getActiveTeam())):
					if self.getASActiveVisibility() != -1:
						self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartVisibilityCost(True, self.m_pCurrentPlot)
			self.m_iCost = max(0, self.m_iCost)
			self.refreshSideMenu()

	def getASActiveUnit(self):
		# Unit Tab
		if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASUnitTabID:
			iUnitType = getASUnit(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
			return iUnitType
		return -1

	def getASActiveCity(self):
		# City Tab
		if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID:
			# City List
			if self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASCityListID:
				iOptionID = self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()]
				# Place City
				if iOptionID == 0:
					return 1
		return -1

	def getASActivePop(self):
		# City Tab
		if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID:
			# City List
			if self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASCityListID:
				iOptionID = self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()]
				# Place Pop
				if iOptionID == 1:
					return 1
		return -1

	def getASActiveCulture(self):
		# City Tab
		if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID:
			# City List
			if self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASCityListID:
				iOptionID = self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()]
				# Place Culture
				if iOptionID == 2:
					return 1
		return -1

	def getASActiveBuilding(self):
		# Building Tab
		if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID:
			# Buildings List
			if self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASBuildingsListID:
				iBuildingType = getASBuilding(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
				return iBuildingType
		return -1

	def getASActiveRoute(self):
		# Improvements Tab
		if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASImprovementsTabID:
			# Routes List
			if self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASRoutesListID:
				iRouteType = getASRoute(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
				if iRouteType == -1:
					self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] = self.m_iASImprovementsListID
				return iRouteType
		return -1

	def getASActiveImprovement(self):
		# Improvements Tab
		if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASImprovementsTabID:
			# Improvements List
			if self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASImprovementsListID:
				iImprovementType = getASImprovement(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
				if iImprovementType == -1:
					self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] = self.m_iASRoutesListID
				return iImprovementType
		return -1

	def getASActiveVisibility(self):
		# Visibility Tab
		if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASVisibilityTabID:
			return 1
		return -1

	def getASActiveTech(self): #unused
		# Tech Tab
		if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASTechTabID:
			return 1
		return -1

	def placeObject( self ) :
		x, y = location(self.m_pCurrentPlot)
		pPlot = self.m_pCurrentPlot
		iPlayer = self.m_iCurrentPlayer
		pPlayer = player(iPlayer)
		
		if x == -1 or y == -1: return
		
		if CyInterface().isInAdvancedStart():
			iActiveTeam = CyGame().getActiveTeam()
			if pPlot.isRevealed(iActiveTeam, False):
				# City Tab
				if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID:
					# City List
					if self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASCityListID:
						iOptionID = self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()]
						# Place City
						if iOptionID == 0:
							if pPlayer.getAdvancedStartCityCost(True, pPlot) > -1:
								CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_CITY, iPlayer, x, y, -1, True)	#Action, Player, X, Y, Data, bAdd

						# City Population
						elif iOptionID == 1:
							if pPlot.isCity():
								pCity = pPlot.getPlotCity()
								if pPlayer.getAdvancedStartPopCost(True, pCity) > -1:
									CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_POP, iPlayer, x, y, -1, True)	#Action, Player, X, Y, Data, bAdd

						# City Culture
						elif iOptionID == 2:
							if pPlot.isCity():
								pCity = pPlot.getPlotCity()
								if pPlayer.getAdvancedStartCultureCost(True, pCity) > -1:
									CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_CULTURE, iPlayer, x, y, -1, True)	#Action, Player, X, Y, Data, bAdd

					# Buildings List
					elif self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASBuildingsListID:
							if pPlot.isCity():
								pCity = pPlot.getPlotCity()
								iBuildingType = getASBuilding(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
								if (iBuildingType != -1 and pPlayer.getAdvancedStartBuildingCost(iBuildingType, True, pCity) != -1):
									CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_BUILDING, iPlayer, x, y, iBuildingType, True)	#Action, Player, X, Y, Data, bAdd

				# Unit Tab
				elif self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASUnitTabID:
					iUnitType = getASUnit(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
					if iUnitType > -1 and pPlayer.getAdvancedStartUnitCost(iUnitType, True, pPlot) > -1:
						CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_UNIT, iPlayer, x, y, iUnitType, True)	#Action, Player, X, Y, Data, bAdd

				# Improvements Tab
				elif self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASImprovementsTabID:
					# Routes List
					if self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASRoutesListID:
						iRouteType = getASRoute(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
						if iRouteType > -1 and pPlayer.getAdvancedStartRouteCost(iRouteType, True, pPlot) > -1:
							CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_ROUTE, iPlayer, x, y, iRouteType, True)	#Action, Player, X, Y, Data, bAdd

					# Improvements List
					elif self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASImprovementsListID:
						iImprovementType = getASImprovement(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
						if iImprovementType > -1 and pPlayer.getAdvancedStartImprovementCost(iImprovementType, True, pPlot) > -1:
							CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_IMPROVEMENT, iPlayer, x, y, iImprovementType, True)	#Action, Player, X, Y, Data, bAdd

			# Adjacent nonrevealed
			else:
				# Visibility Tab
				if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASVisibilityTabID:
					if pPlayer.getAdvancedStartVisibilityCost(True, pPlot) > -1:
						CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_VISIBILITY, iPlayer, x, y, -1, True)	#Action, Player, X, Y, Data, bAdd
			self.m_bSideMenuDirty = True
			self.m_bASItemCostDirty = True
			return 1

		if self.iPlayerAddMode == iModeEraseAll:
			pPlot.erase()
			CyEngine().removeLandmark(pPlot)
			for iLoopPlayer in players.all():
				CyEngine().removeSign(pPlot, iLoopPlayer)
				
		elif self.iPlayerAddMode == iModeAddLandMark:
			iIndex = -1
			for i in xrange(CyEngine().getNumSigns()):
				pSign = CyEngine().getSignByIndex(i)
				if pSign.getPlot().getX() != x: continue
				if pSign.getPlot().getY() != y: continue
				if pSign.getPlayerType() == iPlayer:
					iIndex = i
					break
			sText = ""
			if iIndex > -1:
				sText = CyEngine().getSignByIndex(iIndex).getCaption()
			popup = Popup.PyPopup(CvUtil.EventWBLandmarkPopup, EventContextTypes.EVENTCONTEXT_ALL)
			popup.setHeaderString(CyTranslator().getText("TXT_KEY_WB_LANDMARK_START", ()))
			popup.setUserData((x, y, iPlayer, iIndex))
			popup.createEditBox(sText)
			popup.launch()
			
		elif self.iSelection == -1:
			return
			
		elif self.iPlayerAddMode == iModeOwnership:
			pPlot.setOwner(iPlayer)
			
	## Python Effects ##
		elif self.iPlayerAddMode == iModeUnits:
			for i in xrange(abs(iChange)):
				unit = gc.getPlayer(iPlayer).initUnit(self.iSelection, x, y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
				if self.iSelection in lGreatPeopleUnits or self.iSelection in [iGreatGeneral, iGreatSpy]:
					gp.assignGreatPersonName(unit, iPlayer, -1, False)
					
		elif self.iPlayerAddMode == iModeBuildings:
			if pPlot.isCity():
				pCity = pPlot.getPlotCity()
				bEffects = (bPython and pCity.getNumRealBuilding(self.iSelection) == 0)
				pCity.setNumRealBuilding(self.iSelection, 1)
				if bEffects:
					CvEventManager.CvEventManager().onBuildingBuilt([pCity, self.iSelection])
				
				if self.iSelection == iPalace:
					dc.checkName(self.m_iCurrentPlayer)
		elif self.iPlayerAddMode == iModeCity:
			if self.m_pCurrentPlot.isCity(): return
			pCity = gc.getPlayer(iPlayer).initCity(x, y)
			sName = cnm.getFoundName(iPlayer, (x, y))
			if sName:
				pCity.setName(sName, True)
			if bPython:
				CvEventManager.CvEventManager().onCityBuilt([pCity])
			dc.checkName(iPlayer)
			
	## Python Effects ##
		elif self.iPlayerAddMode == iModeImprovements:
			pPlot.setImprovementType(self.iSelection)
			
		elif self.iPlayerAddMode == iModeBonus:
			pPlot.setBonusType(self.iSelection)
			
		elif self.iPlayerAddMode == iModeRoutes:
			pPlot.setRouteType(self.iSelection)
			
		elif self.iPlayerAddMode == iModeTerrain:
			pPlot.setTerrainType(self.iSelection, True, True)
			
		elif self.iPlayerAddMode == iModePlotType:
			if self.iSelection == gc.getInfoTypeForString("TERRAIN_PEAK"):
				pPlot.setPlotType(PlotTypes.PLOT_PEAK, True, True)
			elif self.iSelection == gc.getInfoTypeForString("TERRAIN_HILL"):
				pPlot.setPlotType(PlotTypes.PLOT_HILLS, True, True)
			elif self.iSelection == gc.getInfoTypeForString("TERRAIN_GRASS"):
				pPlot.setPlotType(PlotTypes.PLOT_LAND, True, True)
			elif self.iSelection == gc.getInfoTypeForString("TERRAIN_OCEAN"):
				pPlot.setPlotType(PlotTypes.PLOT_OCEAN, True, True)
				
		elif self.iPlayerAddMode == iModeFeatures:
			pPlot.setFeatureType(self.iSelection, self.iSelectClass)
			
		elif self.iPlayerAddMode == iModeRiver:
			if self.m_pRiverStartPlot == pPlot:
				self.m_pRiverStartPlot = -1
				CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
			elif self.m_pRiverStartPlot != -1:
				xRiver, yRiver = location(self.m_pRiverStartPlot)
				iXDiff = abs(x - xRiver)
				iYDiff = abs(y - yRiver)
				
				xStartRiverGreater = (xRiver > x)
				yStartRiverGreater = (yRiver > y)
				xStartRiverSmaller = (xRiver < x)
				yStartRiverSmaller = (yRiver < y)

				if (iXDiff == iYDiff == 1) and xStartRiverGreater and yStartRiverSmaller:
					self.placeRiverNW()
					self.m_pRiverStartPlot = plot_(xRiver-1, yRiver+1)
				elif iXDiff == 0 and iYDiff == 1 and yStartRiverSmaller:
					self.placeRiverN()
					self.m_pRiverStartPlot = self.m_pCurrentPlot
				elif (iXDiff == iYDiff == 1) and xStartRiverSmaller and yStartRiverSmaller:
					self.placeRiverNE()
					self.m_pRiverStartPlot = self.m_pCurrentPlot
				elif iXDiff == 1 and iYDiff == 0 and xStartRiverGreater:
					self.placeRiverW()
					self.m_pRiverStartPlot = self.m_pCurrentPlot
				elif iXDiff == 1 and iYDiff == 0 and xStartRiverSmaller:
					self.placeRiverE()
					self.m_pRiverStartPlot = self.m_pCurrentPlot
				elif iXDiff == iYDiff == 1 and xStartRiverGreater and yStartRiverGreater:
					self.placeRiverSW()
					self.m_pRiverStartPlot = self.m_pCurrentPlot
				elif iXDiff == 0 and iYDiff == 1 and yStartRiverGreater:
					self.placeRiverS()
					self.m_pRiverStartPlot = self.m_pCurrentPlot
				elif iXDiff == iYDiff == 1 and xStartRiverSmaller and yStartRiverGreater:
					self.placeRiverSE()
					self.m_pRiverStartPlot = self.m_pCurrentPlot
				else:
					self.m_pRiverStartPlot = self.m_pCurrentPlot
			else:
				self.m_pRiverStartPlot = self.m_pCurrentPlot
		elif self.iPlayerAddMode == iModeFlip:
			if not is_minor(iPlayer):
				self.changeFlipZone(self.m_pCurrentPlot, True)
		elif self.iPlayerAddMode == iModeCore:
			if not is_minor(iPlayer):
				self.m_pCurrentPlot.setCore(civ(iPlayer), True)
		elif self.iPlayerAddMode == iModeSettlerValue:
			if not is_minor(iPlayer):
				self.m_pCurrentPlot.setSettlerValue(civ(iPlayer), iSetValue)
		elif self.iPlayerAddMode == iModeWarMap:
			if not is_minor(iPlayer):
				self.m_pCurrentPlot.setWarValue(civ(iPlayer), iWarValue)
		elif self.iPlayerAddMode == iModeReligionMap:
			if not self.m_pCurrentPlot.isWater():
				self.m_pCurrentPlot.setSpreadFactor(self.m_iCurrentReligion, self.m_iReligionMapValue)
		elif self.iPlayerAddMode == iModeRegionMap:
			pPlot.setRegionID(self.m_iRegionMapID)
		elif self.iPlayerAddMode == iModeAreaExporter1:
			tPlot = (x, y)
			if tPlot not in self.TempInfo:
				self.TempInfo.append(tPlot)
		return 1

	def removeObject( self ):
		x, y = location(self.m_pCurrentPlot)
		pPlot = self.m_pCurrentPlot
		iPlayer = self.m_iCurrentPlayer
		pPlayer = player(iPlayer)
		
		if x == -1 or y == -1: return
		
		# Advanced Start
		if CyInterface().isInAdvancedStart():
			iActiveTeam = CyGame().getActiveTeam()
			if pPlot.isRevealed(iActiveTeam, False):
				# City Tab
				if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID:
					# City List
					if self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASCityListID:
						iOptionID = self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()]
						# City Population
						if iOptionID == 1:
							if pPlot.isCity():
								if pPlot.getPlotCity().getOwner() == iPlayer:
									CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_POP, iPlayer, x, y, -1, False)	#Action, Player, X, Y, Data, bAdd

					# Buildings List
					elif self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASBuildingsListID:
						if pPlot.isCity():
							if pPlot.getPlotCity().getOwner() == iPlayer:
								iBuildingType = getASBuilding(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
								if -1 != iBuildingType:
									CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_BUILDING, iPlayer, x, y, iBuildingType, False)	#Action, Player, X, Y, Data, bAdd

				# Unit Tab
				elif self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASUnitTabID:
					iUnitType = getASUnit(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
					if iUnitType != -1:
						CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_UNIT, iPlayer, x, y, iUnitType, False)	#Action, Player, X, Y, Data, bAdd

				# Improvements Tab
				elif self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASImprovementsTabID:
					# Routes List
					if self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASRoutesListID:
						iRouteType = getASRoute(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
						if iRouteType != -1:
							CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_ROUTE, iPlayer, x, y, iRouteType, False)	#Action, Player, X, Y, Data, bAdd

					# Improvements List
					elif self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASImprovementsListID:
						iImprovementType = getASImprovement(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
						if iImprovementType != -1:
							CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_IMPROVEMENT, iPlayer, x, y, iImprovementType, False)	#Action, Player, X, Y, Data, bAdd

			# Adjacent nonrevealed
			else:
				# Visibility Tab
				if self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASVisibilityTabID:
					return 1
			self.m_bSideMenuDirty = True
			self.m_bASItemCostDirty = True
			return 1

		if self.iPlayerAddMode == iModeEraseAll:
			pPlot.erase()
			CyEngine().removeLandmark(pPlot)
			for iLoopPlayer in players.all():
				CyEngine().removeSign(pPlot, iLoopPlayer)
				
		elif self.iPlayerAddMode == iModeOwnership:
			pPlot.setOwner(-1)
			
		elif self.iPlayerAddMode == iModeUnits:
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getUnitType() == self.iSelection:
					pUnit.kill(False, PlayerTypes.NO_PLAYER)
					return 1
			if pPlot.getNumUnits() > 0:
				pUnit = pPlot.getUnit(0)
				pUnit.kill(False, PlayerTypes.NO_PLAYER)
				return 1
				
		elif self.iPlayerAddMode == iModeBuildings:
			if pPlot.isCity():
				pPlot.getPlotCity().setNumRealBuilding(self.iSelection, 0)
				
		elif self.iPlayerAddMode == iModeCity:
			if pPlot.isCity():
				pCity = pPlot.getPlotCity()
				pCity.kill()
				
		elif self.iPlayerAddMode == iModeImprovements:
			pPlot.setImprovementType(-1)
			return 1
			
		elif self.iPlayerAddMode == iModeBonus:
			pPlot.setBonusType(-1)
			return 1
			
		elif self.iPlayerAddMode == iModeFeatures:
			pPlot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
			
		elif self.iPlayerAddMode == iModeRoutes:
			pPlot.setRouteType(-1)
			
		elif self.iPlayerAddMode == iModeRiver:
			if self.m_pRiverStartPlot != -1:
				self.m_pRiverStartPlot = -1
				CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
			else:
				pPlot.setNOfRiver(False, CardinalDirectionTypes.NO_CARDINALDIRECTION)
				pPlot.setWOfRiver(False, CardinalDirectionTypes.NO_CARDINALDIRECTION)
				
		elif self.iPlayerAddMode == iModeAddLandMark:
			CyEngine().removeSign(pPlot, iPlayer)
			
		elif self.iPlayerAddMode == iModeFlip:
			if not is_minor(iPlayer):
				self.changeFlipZone(pPlot, False)
					
		elif self.iPlayerAddMode == iModeCore:
			if not is_minor(iPlayer):
				pPlot.setCore(civ(iPlayer), False)
					
		elif self.iPlayerAddMode == iModeSettlerValue:
			if not is_minor(iPlayer):
				pPlot.setSettlerValue(civ(iPlayer), 20)
					
		elif self.iPlayerAddMode == iModeWarMap:
			if not is_minor(iPlayer):
				pPlot.setWarValue(civ(iPlayer), 0)
					
		elif self.iPlayerAddMode == iModeReligionMap:
			if not pPlot.isWater():
				pPlot.setSpreadFactor(self.m_iCurrentReligion, 0)
				
		elif self.iPlayerAddMode == iModeRegionMap:
			pPlot.setRegionID(-1)
				
		elif self.iPlayerAddMode == iModeAreaExporter1:
			tPlot = (x, y)
			if tPlot in self.TempInfo:
				self.TempInfo.remove(tPlot)
		return 1

	def placeRiverNW ( self, bUseCurrent = True ):
		if bUseCurrent:
			if not self.m_pRiverStartPlot.isNone():
				self.m_pRiverStartPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_WEST)

		pRiverStepPlot = plot_(self.m_pRiverStartPlot.getX()-1, self.m_pRiverStartPlot.getY())
		if not pRiverStepPlot.isNone():
			pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
		pRiverStepPlot = plot_(self.m_pRiverStartPlot.getX()-1, self.m_pRiverStartPlot.getY()+1)
		if not pRiverStepPlot.isNone():
			pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
		return

	def placeRiverN ( self, bUseCurrent = True ):
		if bUseCurrent:
			if not self.m_pRiverStartPlot.isNone():
				self.m_pRiverStartPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)

		pRiverStepPlot = plot_(self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY()+1)
		if not pRiverStepPlot.isNone():
			pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
		return

	def placeRiverNE ( self, bUseCurrent = True ):
		if bUseCurrent:
			if not self.m_pRiverStartPlot.isNone():
				self.m_pRiverStartPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)

		pRiverStepPlot = plot_(self.m_pRiverStartPlot.getX()+1, self.m_pRiverStartPlot.getY())
		if not pRiverStepPlot.isNone():
			pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)
			pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
		pRiverStepPlot = plot_(self.m_pRiverStartPlot.getX()+1, self.m_pRiverStartPlot.getY()+1)
		if not pRiverStepPlot.isNone():
			pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
		return

	def placeRiverW ( self, bUseCurrent = True ):
		if bUseCurrent:
			if not self.m_pRiverStartPlot.isNone():
				self.m_pRiverStartPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_WEST)

		pRiverStepPlot = plot_(self.m_pRiverStartPlot.getX()-1, self.m_pRiverStartPlot.getY())
		if not pRiverStepPlot.isNone():
			pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_WEST)
		return

	def placeRiverE ( self, bUseCurrent = True ):
		if bUseCurrent:
			if not self.m_pRiverStartPlot.isNone():
				self.m_pRiverStartPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)

		pRiverStepPlot = plot_(self.m_pRiverStartPlot.getX()+1, self.m_pRiverStartPlot.getY())
		if not pRiverStepPlot.isNone():
			pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)
		return

	def placeRiverSW ( self, bUseCurrent = True ):
		if bUseCurrent:
			if not self.m_pRiverStartPlot.isNone():
				self.m_pRiverStartPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_WEST)

		pRiverStepPlot = plot_(self.m_pRiverStartPlot.getX()-1, self.m_pRiverStartPlot.getY()-1)
		if not pRiverStepPlot.isNone():
			pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
		return

	def placeRiverS ( self, bUseCurrent = True ):
		if bUseCurrent:
			if not self.m_pRiverStartPlot.isNone():
				self.m_pRiverStartPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)

		pRiverStepPlot = plot_(self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY()-1)
		if not pRiverStepPlot.isNone():
			pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
		return

	def placeRiverSE ( self, bUseCurrent = True ):
		if bUseCurrent:
			if not self.m_pRiverStartPlot.isNone():
				self.m_pRiverStartPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)

		pRiverStepPlot = plot_(self.m_pRiverStartPlot.getX()+1, self.m_pRiverStartPlot.getY())
		if not pRiverStepPlot.isNone():
			pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)
		pRiverStepPlot = plot_(self.m_pRiverStartPlot.getX()+1, self.m_pRiverStartPlot.getY()-1)
		if not pRiverStepPlot.isNone():
			pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
		return

	def toggleUnitEditCB(self):
		self.iPlayerAddMode = iModeEditUnit
		self.refreshSideMenu()
		return

	def normalPlayerTabModeCB(self):
		self.m_iCurrentTeam = gc.getPlayer(self.m_iCurrentPlayer).getTeam()
		self.iPlayerAddMode = iModeUnits
		self.iSelectClass = -2
		self.iSelection = -1
		self.refreshSideMenu()
		getWBToolNormalPlayerTabCtrl().enable(False)
		getWBToolNormalMapTabCtrl().enable(False)
		return

	def normalMapTabModeCB(self):
		self.iPlayerAddMode = iModePlotData
		self.refreshSideMenu()
		return

	def revealTabModeCB(self):
		self.iPlayerAddMode = iModeRevealPlot
		self.refreshSideMenu()
		self.refreshReveal()
		return

	def toggleCityEditCB(self):
		self.iPlayerAddMode = iModeCityDataI
		self.refreshSideMenu()
		return

	def landmarkModeCB(self):
		self.iPlayerAddMode = iModeAddLandMark
		self.m_iCurrentPlayer = gc.getBARBARIAN_PLAYER()
		self.refreshSideMenu()
		return

	def eraseCB(self):
		self.m_pRiverStartPlot = -1
		self.iPlayerAddMode = iModeEraseAll
		self.refreshSideMenu()
		return

	def setCurrentAdvancedStartIndex(self, argsList):
		iIndex = int(argsList)
		self.m_iAdvancedStartCurrentIndexes [self.m_advancedStartTabCtrl.getActiveTab()] = int(argsList)
		return 1

	def setCurrentAdvancedStartList(self, argsList):
		self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] = int(argsList)
		return 1

	def getASUnitTabID(self):
		return self.m_iASUnitTabID

	def getASUnitListID(self):
		return self.m_iASUnitListID

	def getASCityTabID(self):
		return self.m_iASCityTabID

	def getASCityListID(self):
		return self.m_iASCityListID

	def getASBuildingsListID(self):
		return self.m_iASBuildingsListID

	def getASAutomateListID(self):
		return self.m_iASAutomateListID

	def getASImprovementsTabID(self):
		return self.m_iASImprovementsTabID

	def getASRoutesListID(self):
		return self.m_iASRoutesListID

	def getASImprovementsListID(self):
		return self.m_iASImprovementsListID

	def getASVisibilityTabID(self):
		return self.m_iASVisibilityTabID

	def getASVisibilityListID(self):
		return self.m_iASVisibilityListID

	def getASTechTabID(self):
		return self.m_iASTechTabID

	def getASTechListID(self):
		return self.m_iASTechListID

	def placeMultipleObjects(self):
		permCurrentPlot = self.m_pCurrentPlot
		lPlots = self.getMultiplePlotData()
		for pPlot in lPlots:
			self.m_pCurrentPlot = pPlot
			if self.m_pCurrentPlot.isNone(): continue
			if self.bSensibility and len(lPlots) > 1:
				if self.iPlayerAddMode == iModeImprovements:
					if self.m_pCurrentPlot.canHaveImprovement(self.iSelection, -1, True):
						self.placeObject()
				elif self.iPlayerAddMode == iModeBonus:
					iOldBonus = self.m_pCurrentPlot.getBonusType(-1)
					self.m_pCurrentPlot.setBonusType(-1)
					if self.m_pCurrentPlot.canHaveBonus(self.iSelection, False):
						self.placeObject()
					else:
						self.m_pCurrentPlot.setBonusType(iOldBonus)
				elif self.iPlayerAddMode == iModeFeatures:
					iOldFeature = self.m_pCurrentPlot.getFeatureType()
					iOldVariety = self.m_pCurrentPlot.getFeatureVariety()
					self.m_pCurrentPlot.setFeatureType(-1, 0)
					if self.m_pCurrentPlot.canHaveFeature(self.iSelection):
						self.placeObject()
					else:
						self.m_pCurrentPlot.setFeatureType(iOldFeature, iOldVariety)
				elif self.iPlayerAddMode == iModeRoutes:
					if not (self.m_pCurrentPlot.isImpassable() or self.m_pCurrentPlot.isWater()):
						self.placeObject()
				elif self.iPlayerAddMode == iModeTerrain:
					if self.m_pCurrentPlot.isWater() == gc.getTerrainInfo(self.iSelection).isWater():
						self.placeObject()
				else:
					self.placeObject()
			else:
				self.placeObject()
		if self.iPlayerAddMode == iModeAreaExporter1:
			self.showAreaExportOverlay()
		self.m_pCurrentPlot = permCurrentPlot
		return

	def removeMultipleObjects(self):
		permCurrentPlot = self.m_pCurrentPlot
		lPlots = self.getMultiplePlotData()
		for pPlot in lPlots:
			self.m_pCurrentPlot = pPlot
			if self.m_pCurrentPlot.isNone(): continue
			self.removeObject()
		if self.iPlayerAddMode == iModeAreaExporter1:
			self.showAreaExportOverlay()
		self.m_pCurrentPlot = permCurrentPlot
		return

	def getMultiplePlotData(self):
		if self.bRegion:
			iRegion = self.m_pCurrentPlot.getRegionID()
			if iRegion == -1: return [self.m_pCurrentPlot]
			return plots.region(iRegion)
			
		if self.iPlayerAddMode == iModeAreaExporter3:
			return plots.start(self.TempInfo[-1]).end(self.m_pCurrentPlot)
			
		if self.iBrushWidth == -1 and self.iBrushHeight == -1:
			return plots.all()

		iMinX = self.m_pCurrentPlot.getX()
		iMaxX = self.m_pCurrentPlot.getX() + self.iBrushWidth - 1
		iMinY = self.m_pCurrentPlot.getY() - self.iBrushHeight + 1
		iMaxY = self.m_pCurrentPlot.getY()
		if self.iBrushWidth == -1:
			iMinX = 0
			iMaxX = CyMap().getGridWidth()
		if self.iBrushHeight == -1:
			iMinY = 0
			iMaxY = CyMap().getGridHeight()
		return plots.start((iMinX, iMinY)).end((iMaxX, iMaxY))

	def setMultipleReveal(self, bReveal):
		lPlots = self.getMultiplePlotData()
		for pPlot in lPlots:
			if pPlot.isNone(): continue
			self.RevealCurrentPlot(bReveal, pPlot)
		self.refreshReveal()
		return

	def useLargeBrush(self):
		if self.iPlayerAddMode in lRevealModes:
			return True
		if self.iPlayerAddMode == iModeEraseAll:
			return True
		if self.iPlayerAddMode == iModeImprovements:
			return True
		if self.iPlayerAddMode == iModeBonus:
			return True
		if self.iPlayerAddMode == iModePlotType:
			return True
		if self.iPlayerAddMode == iModeTerrain:
			return True
		if self.iPlayerAddMode == iModeRoutes:
			return True
		if self.iPlayerAddMode == iModeFeatures:
			return True
		if self.iPlayerAddMode in lDoCMapModes:
			return True
		if self.iPlayerAddMode in lMoveMapModes:
			return True
		if self.iPlayerAddMode in [iModeAreaExporter1, iModeAreaExporter3]:
			return True
		return False

	def setSideMenu(self):
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN )
		iButtonWidth = 32
		iAdjust = iButtonWidth + 3

		iScreenWidth = 16 + iAdjust * 6
		iScreenHeight = 16 + iAdjust * 5

		iXStart = screen.getXResolution() - iScreenWidth
		if CyInterface().isInAdvancedStart():
			iXStart = 0
			iScreenWidth = 226
			iScreenHeight = 10 + 37 * 2

		screen.addPanel( "WorldBuilderBackgroundPanel", "", "", True, True, iXStart, 0, iScreenWidth, iScreenHeight, PanelStyles.PANEL_STYLE_MAIN )

		if CyInterface().isInAdvancedStart():

			iX = 50
			iY = 15
			szText = u"<font=4>" + CyTranslator().getText("TXT_KEY_WB_AS_POINTS", (gc.getPlayer(CyGame().getActivePlayer()).getAdvancedStartPoints(), )) + "</font>"
			screen.setLabel("AdvancedStartPointsText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, iX, iY, -2, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			iY += 30
			szText = CyTranslator().getText("TXT_KEY_ADVANCED_START_BEGIN_GAME", ())
			screen.setButtonGFC( "WorldBuilderExitButton", szText, "", iX, iY, 130, 28, WidgetTypes.WIDGET_WB_EXIT_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )

			szText = u"<font=4>" + CyTranslator().getText("TXT_KEY_WB_AS_COST_THIS_LOCATION", (self.m_iCost, )) + u"</font>"
			iY = 85
			screen.setLabel("AdvancedStartCostText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, iX-20, iY, -2, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		else:
			iX = iXStart + 8
			iY = 10

			screen.setImageButton("Version", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath(), iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 9)
			iX += iAdjust
			screen.setImageButton("WorldBuilderRegenerateMap", CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_REVEAL_ALL_TILES").getPath(), iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_WB_REGENERATE_MAP, -1, -1)
			iX += iAdjust
			screen.addCheckBoxGFC("WorldBuilderEraseButton", CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_ERASE").getPath(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_WB_ERASE_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
			iX += iAdjust
			screen.setImageButton("WorldBuilderSaveButton", CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_SAVE").getPath(), iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_WB_SAVE_BUTTON, -1, -1)
			iX += iAdjust
			screen.setImageButton("WorldBuilderLoadButton", CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_LOAD").getPath(), iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_WB_LOAD_BUTTON, -1, -1)
			iX += iAdjust
			screen.setImageButton("WorldBuilderExitButton", CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_EXIT").getPath(), iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_WB_EXIT_BUTTON, -1, -1)

			iX = iXStart + 8
			iY += iAdjust

			screen.setImageButton("EditGameOptions", "", iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 23)
			screen.setStyle("EditGameOptions", "Button_HUDAdvisorVictory_Style")
			iX += iAdjust
			screen.setImageButton("EditReligions", "", iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 20)
			screen.setStyle("EditReligions", "Button_HUDAdvisorReligious_Style")
			iX += iAdjust
			screen.setImageButton("EditCorporations", "", iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 21)
			screen.setStyle("EditCorporations", "Button_HUDAdvisorCorporation_Style")
			iX += iAdjust
			screen.setImageButton("EditDiplomacy", "", iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_WB_DIPLOMACY_MODE_BUTTON, -1, -1)
			screen.setStyle("EditDiplomacy", "Button_HUDAdvisorForeign_Style")
			iX += iAdjust
			screen.setImageButton("EditEspionage", "", iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 22)
			screen.setStyle("EditEspionage", "Button_HUDAdvisorEspionage_Style")
			iX += iAdjust
			screen.setImageButton("TradeScreen", "", iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 34)
			screen.setStyle("TradeScreen", "Button_HUDAdvisorFinance_Style")

			iX = iXStart + 8
			iY += iAdjust
			screen.setImageButton("StoredDataScreen", "", iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 41)
			screen.setStyle("StoredDataScreen", "Button_HUDAdvisorRecord_Style")
			iX += iAdjust
			screen.addCheckBoxGFC("DoCMapsScreen", "Art/Interface/Buttons/DoCMaps.dds", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SMALLCIRCLE").getPath(),
				iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 42, ButtonStyles.BUTTON_STYLE_LABEL)
			iX += iAdjust
			screen.addCheckBoxGFC("MoveMapScreen", "Art/Interface/Buttons/MoveMap.dds", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SMALLCIRCLE").getPath(),
				iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 44, ButtonStyles.BUTTON_STYLE_LABEL)
			iX += iAdjust
			screen.addCheckBoxGFC("AreaExporterScreen", "Art/Interface/Buttons/AreaExport.dds", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SMALLCIRCLE").getPath(),
				iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 48, ButtonStyles.BUTTON_STYLE_LABEL)

			iX = iXStart + 8
			iY += iAdjust
			screen.addCheckBoxGFC("WorldBuilderNormalPlayerModeButton", ",-,Art/Interface/Buttons/FinalFrontier1_Atlas.dds,2,15", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_WB_NORMAL_PLAYER_TAB_MODE_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
			iX += iAdjust
			screen.addCheckBoxGFC("WorldBuilderNormalMapModeButton", ",-,Art/Interface/Buttons/FinalFrontier2_Atlas.dds,3,6", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_WB_NORMAL_MAP_TAB_MODE_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
			iX += iAdjust
			screen.addCheckBoxGFC("WorldBuilderRevealTileModeButton", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_LOS").getPath(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_WB_REVEAL_TAB_MODE_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
			iX += iAdjust
			screen.addCheckBoxGFC("PythonEffectButton", ",-,Art/Interface/Buttons/FinalFrontier2_Atlas.dds,3,4", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 0, ButtonStyles.BUTTON_STYLE_LABEL)
			iX += iAdjust
			screen.addCheckBoxGFC("HideInactive", ",-,Art/Interface/Buttons/GodsOfOld_Atlas.dds,8,3", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 31, ButtonStyles.BUTTON_STYLE_LABEL)
			iX += iAdjust
			screen.setImageButton("InfoScreen", "", iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 33)
			screen.setStyle("InfoScreen", "Button_HUDAdvisorRecord_Style")

			iX = iXStart + 8
			iY += iAdjust

			screen.addCheckBoxGFC("EditUnitData", ",-,Art/Interface/Buttons/Afterworld_Atlas.dds,4,9", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_WB_UNIT_EDIT_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
			iX += iAdjust
			screen.addCheckBoxGFC("EditPromotions", ",-,Art/Interface/Buttons/Promotions_Atlas.dds,8,2", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 6, ButtonStyles.BUTTON_STYLE_LABEL)
			iX += iAdjust
			screen.addCheckBoxGFC("EditCityDataI", CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_TOGGLE_CITY_EDIT_MODE").getPath(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				 iX, iY, iButtonWidth, iButtonWidth,WidgetTypes.WIDGET_WB_CITY_EDIT_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
			iX += iAdjust
			screen.addCheckBoxGFC("EditCityDataII", ",-,Art/Interface/Buttons/FinalFrontier2_Atlas.dds,1,8", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 7, ButtonStyles.BUTTON_STYLE_LABEL)
			iX += iAdjust
			screen.addCheckBoxGFC("EditCityBuildings", ",-,Art/Interface/Buttons/FinalFrontier1_Atlas.dds,5,14", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 8, ButtonStyles.BUTTON_STYLE_LABEL)
			iX += iAdjust
			screen.addCheckBoxGFC("EditEvents", "", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 10, ButtonStyles.BUTTON_STYLE_LABEL)
			screen.setStyle("EditEvents", "Button_HUDLog_Style")

			self.setCurrentModeCheckbox()
		return

	def refreshSideMenu(self):
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN )
		CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
		iButtonWidth = 32
		iAdjust = iButtonWidth + 3
		iScreenWidth = 16 + iAdjust * 6
		iScreenHeight = 16 + iAdjust * 5

		if CyInterface().isInAdvancedStart():
			iX = 50
			iY = 15
			szText = u"<font=4>" + CyTranslator().getText("TXT_KEY_WB_AS_POINTS", (gc.getPlayer(CyGame().getActivePlayer()).getAdvancedStartPoints(), )) + "</font>"
			screen.setLabel("AdvancedStartPointsText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, iX, iY, -2, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			szText = u"<font=4>" + CyTranslator().getText("TXT_KEY_WB_AS_COST_THIS_LOCATION", (self.m_iCost, )) + u"</font>"
			iY = 85
			screen.setLabel("AdvancedStartCostText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, iX-20, iY, -2, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		else:
			screen.deleteWidget("WorldBuilderPlayerChoice")
			screen.deleteWidget("WorldBuilderLandmarkButton")
			screen.deleteWidget("WorldBuilderRevealAll")
			screen.deleteWidget("WorldBuilderUnrevealAll")
			screen.deleteWidget("WorldBuilderRevealPanel")
			screen.deleteWidget("WorldBuilderBackgroundBottomPanel")
			screen.deleteWidget("EditPlayerData")
			screen.deleteWidget("EditTeamData")
			screen.deleteWidget("EditTechnologies")
			screen.deleteWidget("EditProjects")
			screen.deleteWidget("EditUnitsCities")
			screen.deleteWidget("ChangeBy")
			screen.deleteWidget("AddOwnershipButton")
			screen.deleteWidget("AddUnitsButton")
			screen.deleteWidget("AddBuildingsButton")
			screen.deleteWidget("AddCityButton")
			screen.deleteWidget("EditStartingPlot")
			screen.deleteWidget("EditPlotData")
			screen.deleteWidget("AddImprovementButton")
			screen.deleteWidget("AddBonusButton")
			screen.deleteWidget("AddPlotTypeButton")
			screen.deleteWidget("AddTerrainButton")
			screen.deleteWidget("AddRouteButton")
			screen.deleteWidget("AddFeatureButton")
			screen.deleteWidget("AddRiverButton")
			screen.deleteWidget("WBCurrentItem")
			screen.deleteWidget("WBSelectClass")
			screen.deleteWidget("WBSelectItem")
			screen.deleteWidget("RevealMode")
			screen.deleteWidget("WorldBuilderEraseAll")
			screen.deleteWidget("BrushWidth")
			screen.deleteWidget("BrushHeight")
			screen.deleteWidget("SensibilityCheck")
			screen.deleteWidget("RegionButton")
			screen.deleteWidget("FlipButton")
			screen.deleteWidget("CoreButton")
			screen.deleteWidget("SettlerValueButton")
			screen.deleteWidget("WarMapButton")
			screen.deleteWidget("ReligionMapButton")
			screen.deleteWidget("RegionMapButton")
			screen.deleteWidget("VictoryMapButton")
			screen.deleteWidget("PresetValue")
			screen.deleteWidget("UtilButtonPanel")
			screen.deleteWidget("ClearChanges")
			screen.deleteWidget("Export")
			screen.deleteWidget("FlipAIButton")
			screen.deleteWidget("MoveMapReset")
			screen.deleteWidget("VictoryRectangleButton")
			screen.deleteWidget("CancelMoveMap")
			screen.deleteWidget("AreaExportWater")
			screen.deleteWidget("AreaExportPeak")
			screen.deleteWidget("ToolHelp")
			screen.deleteWidget("AllRegionsButton")
			screen.deleteWidget("CheckRegionsButton")

## Panel Screen ##
			nRows = 1
			if self.iPlayerAddMode in lPlayerModes + lRevealModes + lMapModes:
				nRows = 3
			elif self.iPlayerAddMode in [iModeVictoryMap] + lAreaExportModes:
				nRows = 3
			elif self.iPlayerAddMode in lDoCMapModes:
				nRows = 5
			elif self.iPlayerAddMode in lMoveMapModes:
				nRows = 2

			iHeight = 16 + iAdjust * nRows
			iXStart = screen.getXResolution() - iScreenWidth
			screen.addPanel("WorldBuilderBackgroundBottomPanel", "", "", True, True, iXStart, iScreenHeight - 10, iScreenWidth, iHeight, PanelStyles.PANEL_STYLE_MAIN )
			iY = iScreenHeight
			if self.iPlayerAddMode in lPlayerModes:
				iX = iXStart + 8
				screen.addCheckBoxGFC("AddOwnershipButton", gc.getCivilizationInfo(gc.getPlayer(self.m_iCurrentPlayer).getCivilizationType()).getButton(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 28, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addDropDownBoxGFC("WorldBuilderPlayerChoice", iX, iY, screen.getXResolution() - 8 - iX, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for iPlayer in players.all().where(lambda p: player(p).isEverAlive()):
					sName = name(iPlayer)
					if not player(iPlayer).isAlive():
						sName = "*" + sName
					if player(iPlayer).isTurnActive():
						sName = "[" + sName + "]"
					screen.addPullDownString("WorldBuilderPlayerChoice", sName, iPlayer, iPlayer, self.m_iCurrentPlayer == iPlayer)
				iX = screen.getXResolution() - iScreenWidth + 8
				iY += iAdjust
				screen.setImageButton("EditPlayerData", gc.getLeaderHeadInfo(gc.getPlayer(self.m_iCurrentPlayer).getLeaderType()).getButton(), iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 1)
				iX += iAdjust
				screen.setImageButton("EditTeamData", ",-,Art/Interface/Buttons/FinalFrontier2_Atlas.dds,8,7", iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 2)
				iX += iAdjust
				screen.setImageButton("EditTechnologies", ",-,Art/Interface/Buttons/TechTree_Atlas.dds,5,6", iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 3)
				iX += iAdjust
				screen.setImageButton("EditProjects", ",-,Art/Interface/Buttons/Buildings_Atlas.dds,1,6", iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 4)
				iX += iAdjust
				screen.setImageButton("EditUnitsCities", ",-,Art/Interface/Buttons/Warlords_Atlas_1.dds,3,12", iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 5)
				iX += iAdjust
				screen.addCheckBoxGFC("EditStartingPlot", ",-,Art/Interface/Buttons/Warlords_Atlas_1.dds,4,13", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 32, ButtonStyles.BUTTON_STYLE_LABEL)

				iY += iAdjust
				iX = iXStart + 8
				screen.addCheckBoxGFC("AddUnitsButton", ",-,Art/Interface/Buttons/Warlords_Atlas_1.dds,6,10", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 27, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addCheckBoxGFC("AddBuildingsButton", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION").getPath(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 19, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addCheckBoxGFC("AddCityButton", ",-,Art/Interface/Buttons/Charlemagne_Atlas.dds,4,2", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 18, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addDropDownBoxGFC("ChangeBy", iX, iY, screen.getXResolution() - 8 - iX, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				i = 1
				while i < 1001:
					screen.addPullDownString("ChangeBy", str(i), i, i, iChange == i)
					if str(i)[0] == "1":
						i *= 5
					else:
						i *= 2
				sText = "<font=3b>" + CyTranslator().getText("TXT_KEY_PEDIA_HIDE_INACTIVE", ()) + "</font>"

			elif self.iPlayerAddMode in lMapModes:
				iX = iXStart + 8
				screen.addCheckBoxGFC("EditPlotData", ",-,Art/Interface/Buttons/FinalFrontier1_Atlas.dds,4,16", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1027, -1, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addCheckBoxGFC("AddRiverButton", CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_RIVER_PLACEMENT").getPath(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 11, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addCheckBoxGFC("WorldBuilderLandmarkButton", CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_LANDMARK_MODE").getPath(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_WB_LANDMARK_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addDropDownBoxGFC("WorldBuilderPlayerChoice", iX, iY, screen.getXResolution() - 8 - iX, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				screen.addPullDownString("WorldBuilderPlayerChoice", CyTranslator().getText("TXT_KEY_WB_LANDMARKS", ()), gc.getBARBARIAN_PLAYER(), gc.getBARBARIAN_PLAYER(), self.m_iCurrentPlayer == gc.getBARBARIAN_PLAYER())
				for iPlayer in players.all().without(players.barbarian()).where(lambda p: player(p).isEverAlive()):
					sName = name(iPlayer)
					if not player(iPlayer).isAlive():
						sName = "*" + sName
					if player(iPlayer).isTurnActive():
						sName = "[" + sName + "]"
					screen.addPullDownString("WorldBuilderPlayerChoice", sName, iPlayer, iPlayer, self.m_iCurrentPlayer == iPlayer)

				iX = iXStart + 8
				iY += iAdjust
				screen.addCheckBoxGFC("AddImprovementButton", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_FEATURE_PRODUCTION").getPath(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 12, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addCheckBoxGFC("AddBonusButton", ",-,Art/Interface/Buttons/Warlords_Atlas_1.dds,7,9", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 13, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addCheckBoxGFC("AddPlotTypeButton", CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_CHANGE_ALL_PLOTS").getPath(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 14, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addCheckBoxGFC("AddTerrainButton", ",-,Art/Interface/Buttons/BaseTerrain_TerrainFeatures_Atlas.dds,3,1", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 15, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addCheckBoxGFC("AddRouteButton", "Art/Interface/Buttons/Builds/BuildRoad.dds", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 16, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addCheckBoxGFC("AddFeatureButton", ",-,Art/Interface/Buttons/BaseTerrain_TerrainFeatures_Atlas.dds,3,3", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 17, ButtonStyles.BUTTON_STYLE_LABEL)

				iX = iXStart + 8
				iY += iAdjust
				screen.addCheckBoxGFC("RegionButton", ",-,Art/Interface/Buttons/FinalFrontier2_Atlas.dds,1,6", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 43, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addCheckBoxGFC("SensibilityCheck", ",-,Art/Interface/Buttons/FinalFrontier1_Atlas.dds,1,16", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 24, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				iWidth = (screen.getXResolution() - 8 - iX - 3)/2
				screen.addDropDownBoxGFC("BrushWidth", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for i in range(1, 11):
					screen.addPullDownString("BrushWidth", "W: " + str(i), i, i, self.iBrushWidth == i)
				screen.addPullDownString("BrushWidth", "W: " + "--", -1, -1, self.iBrushWidth == -1)
				iX += iWidth
				screen.addDropDownBoxGFC("BrushHeight", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for i in range(1, 11):
					screen.addPullDownString("BrushHeight", "H: " + str(i), i, i, self.iBrushHeight == i)
				screen.addPullDownString("BrushHeight", "H: " + "--", -1, -1, self.iBrushHeight == -1)

			elif self.iPlayerAddMode in lDoCMapModes:
				iX = iXStart + 8
				screen.addCheckBoxGFC("FlipButton", ",-,Art/Interface/Buttons/GodsOfOld_Atlas.dds,1,1", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 
					iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 35, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addCheckBoxGFC("CoreButton", ",-,Art/Interface/Buttons/GodsOfOld_Atlas.dds,5,1", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 
					iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 36, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addCheckBoxGFC("SettlerValueButton", ",-,Art/Interface/Buttons/GodsOfOld_Atlas.dds,7,1", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 
					iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 37, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addCheckBoxGFC("WarMapButton", ",-,Art/Interface/Buttons/GodsOfOld_Atlas.dds,4,1", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 
					iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 38, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addCheckBoxGFC("ReligionMapButton", ",-,Art/Interface/Buttons/GodsOfOld_Atlas.dds,3,1", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 
					iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 39, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addCheckBoxGFC("RegionMapButton", ",-,Art/Interface/Buttons/GodsOfOld_Atlas.dds,2,1", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 
					iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 40, ButtonStyles.BUTTON_STYLE_LABEL)
				iX = iXStart + 8
				iY += iAdjust
				screen.addCheckBoxGFC("VictoryMapButton", ",-,Art/Interface/Buttons/GodsOfOld_Atlas.dds,6,1", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 
					iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 46, ButtonStyles.BUTTON_STYLE_LABEL)

				iX = iXStart + 8
				iY += iAdjust
				screen.setImageButton("ToolHelp", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath(), iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 51)
				iX += iAdjust
				if self.iPlayerAddMode == iModeFlip:
					screen.addCheckBoxGFC("FlipAIButton", "Art/Interface/Buttons/TechTree/Artificial_Intelligence.dds", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
						 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 45, ButtonStyles.BUTTON_STYLE_LABEL)
					iX += iAdjust
				elif self.iPlayerAddMode == iModeVictoryMap:
					screen.addCheckBoxGFC("VictoryRectangleButton", "Art/Interface/Buttons/TechTree/Engineering.dds", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
						 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 47, ButtonStyles.BUTTON_STYLE_LABEL)
					iX += iAdjust
				elif self.iPlayerAddMode == iModeRegionMap:
					screen.addCheckBoxGFC("AllRegionsButton", ",-,Art/Interface/Buttons/FinalFrontier2_Atlas.dds,4,5", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
						 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 52, ButtonStyles.BUTTON_STYLE_LABEL)
					iX += iAdjust
					screen.addCheckBoxGFC("CheckRegionsButton", ",-,Art/Interface/Buttons/FinalFrontier1_Atlas.dds,3,13", "",
						 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 53, ButtonStyles.BUTTON_STYLE_LABEL)
					iX += iAdjust
				elif self.iPlayerAddMode != iModeCore:
					screen.addDropDownBoxGFC("PresetValue", iX, iY, iAdjust * 2 - 3, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
					if self.iPlayerAddMode == iModeReligionMap:
						for i in range(RegionMap.iNumReligionMapTypes):
							sText = CyTranslator().getText(str(lReligionMapTexts[i]), ())
							screen.addPullDownString("PresetValue", sText, i, i, i == self.m_iReligionMapValue)
					elif self.iPlayerAddMode == iModeWarMap:
						for i in range(0, iMaxWarValue+1, 2):
							screen.addPullDownString("PresetValue", str(i), i, i, i == iWarValue)
					if self.iPlayerAddMode == iModeSettlerValue:
						for i in range(len(lPresetValues)):
							screen.addPullDownString("PresetValue", str(lPresetValues[i]), i, lPresetValues[i], lPresetValues[i] == iSetValue)
					iX += 2*iAdjust

				screen.addDropDownBoxGFC("WorldBuilderPlayerChoice", iX, iY, screen.getXResolution() - 8 - iX, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				if self.iPlayerAddMode == iModeReligionMap:
					for iReligion in range(iNumReligions):
						sName = gc.getReligionInfo(iReligion).getDescription()
						screen.addPullDownString("WorldBuilderPlayerChoice", sName, iReligion, iReligion, self.m_iCurrentReligion == iReligion)
				elif self.iPlayerAddMode == iModeRegionMap:
					for iRegion in range(iNumRegions):
						TextKey = u"TXT_KEY_REGION_%d" % iRegion
						sName = CyTranslator().getText(str(TextKey), ())
						screen.addPullDownString("WorldBuilderPlayerChoice", sName, iRegion, iRegion, self.m_iRegionMapID == iRegion)
				else:
					for iPlayer in players.major().where(lambda p: player(p).isEverAlive()):
						sName = name(iPlayer)
						if not player(iPlayer).isAlive():
							sName = "*" + sName
						if player(iPlayer).isTurnActive():
							sName = "[" + sName + "]"
						screen.addPullDownString("WorldBuilderPlayerChoice", sName, iPlayer, iPlayer, self.m_iCurrentPlayer == iPlayer)

				if self.iPlayerAddMode != iModeVictoryMap:
					iX = iXStart + 8
					iY += iAdjust
					screen.addCheckBoxGFC("RegionButton", ",-,Art/Interface/Buttons/FinalFrontier2_Atlas.dds,1,6", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
						 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 43, ButtonStyles.BUTTON_STYLE_LABEL)
					iX += iAdjust
					iWidth = (screen.getXResolution() - 8 - iX - 3)/2
					screen.addDropDownBoxGFC("BrushWidth", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
					for i in range(1, 11):
						screen.addPullDownString("BrushWidth", "W: " + str(i), i, i, self.iBrushWidth == i)
					screen.addPullDownString("BrushWidth", "W: " + "--", -1, -1, self.iBrushWidth == -1)
					iX += iWidth
					screen.addDropDownBoxGFC("BrushHeight", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
					for i in range(1, 11):
						screen.addPullDownString("BrushHeight", "H: " + str(i), i, i, self.iBrushHeight == i)
					screen.addPullDownString("BrushHeight", "H: " + "--", -1, -1, self.iBrushHeight == -1)

					iX = iXStart + 8
					iY += iAdjust
					if self.iPlayerAddMode  == iModeReligionMap:
						screen.setButtonGFC("ClearChanges", CyTranslator().getText("TXT_KEY_WB_REVERT_CHANGES", ()), "", iX, iY, screen.getXResolution() - 8 - iX, iButtonWidth, WidgetTypes.WIDGET_PYTHON, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
					else:
						if self.iPlayerAddMode == iModeRegionMap:
							iSpan = 3
						else:
							iSpan = 2
						screen.setButtonGFC("ClearChanges", CyTranslator().getText("TXT_KEY_WB_REVERT_CHANGES", ()), "", iX, iY, iSpan*iAdjust-3, iButtonWidth, WidgetTypes.WIDGET_PYTHON, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
						iX += iSpan*iAdjust
						screen.setButtonGFC("Export", CyTranslator().getText("TXT_KEY_WB_EXPORT", ()), "", iX, iY, iSpan*iAdjust-3, iButtonWidth, WidgetTypes.WIDGET_PYTHON, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
						iX += iSpan*iAdjust

			elif self.iPlayerAddMode in lMoveMapModes:
				if self.iPlayerAddMode == iModeMoveMap:
					iX = iXStart + 8
					iWidth = (screen.getXResolution() - 8 - iX - 3)/2
					screen.addDropDownBoxGFC("BrushWidth", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
					for i in range(1, iWorldX+1):
						screen.addPullDownString("BrushWidth", "W: " + str(i), i, i, self.iBrushWidth == i)
					screen.addPullDownString("BrushWidth", "W: " + "--", -1, -1, self.iBrushWidth == -1)
					iX += iWidth
					screen.addDropDownBoxGFC("BrushHeight", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
					for i in range(1, iWorldY+1):
						screen.addPullDownString("BrushHeight", "H: " + str(i), i, i, self.iBrushHeight == i)
					screen.addPullDownString("BrushHeight", "H: " + "--", -1, -1, self.iBrushHeight == -1)
				elif self.iPlayerAddMode == iModeMoveMap2:
					iX = iXStart + 8
					iWidth = (screen.getXResolution() - 8 - iX - 3)
					screen.setButtonGFC("CancelMoveMap", CyTranslator().getText("TXT_KEY_SCREEN_CANCEL", ()), "", iX, iY, iWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

				iX = iXStart + 8
				iY += iAdjust
				screen.setImageButton("ToolHelp", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath(), iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 51)
				iX += iAdjust
				iWidth = (screen.getXResolution() - 8 - iX - 3)
				screen.addDropDownBoxGFC("MoveMapReset", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for i in range(3):
					szText = "TXT_KEY_WB_MOVEMAP_RESET%d" % i
					screen.addPullDownString("MoveMapReset", CyTranslator().getText(szText, ()), i, i, self.iMoveMapReset == i)

			elif self.iPlayerAddMode in lAreaExportModes:
				iX = iXStart + 8
				screen.addCheckBoxGFC("AreaExportWater", gc.getTerrainInfo(iOcean).getButton(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 
					iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 49, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				screen.addCheckBoxGFC("AreaExportPeak", gc.getTerrainInfo(iTerrainPeak).getButton(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 
					iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 50, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				
				screen.addDropDownBoxGFC("WorldBuilderPlayerChoice", iX, iY, screen.getXResolution() - 8 - iX, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				screen.addPullDownString("WorldBuilderPlayerChoice", CyTranslator().getText("TXT_KEY_WB_AREA_EXPORTER_CLICK", ()), 0, 0, self.iPlayerAddMode == iModeAreaExporter1)
				screen.addPullDownString("WorldBuilderPlayerChoice", CyTranslator().getText("TXT_KEY_WB_AREA_EXPORTER_TLBR", ()), 1, 1, self.iPlayerAddMode == iModeAreaExporter2)
				
				iX = iXStart + 8
				iY += iAdjust
				screen.setImageButton("ToolHelp", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath(), iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 51)
				iX += iAdjust
				screen.addCheckBoxGFC("RegionButton", ",-,Art/Interface/Buttons/FinalFrontier2_Atlas.dds,1,6", CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					 iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 43, ButtonStyles.BUTTON_STYLE_LABEL)
				iX += iAdjust
				iWidth = (screen.getXResolution() - 8 - iX - 3)/2
				screen.addDropDownBoxGFC("BrushWidth", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for i in range(1, 11):
					screen.addPullDownString("BrushWidth", "W: " + str(i), i, i, self.iBrushWidth == i)
				screen.addPullDownString("BrushWidth", "W: " + "--", -1, -1, self.iBrushWidth == -1)
				iX += iWidth
				screen.addDropDownBoxGFC("BrushHeight", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for i in range(1, 11):
					screen.addPullDownString("BrushHeight", "H: " + str(i), i, i, self.iBrushHeight == i)
				screen.addPullDownString("BrushHeight", "H: " + "--", -1, -1, self.iBrushHeight == -1)
				
				iX = iXStart + 8
				iY += iAdjust
				screen.setButtonGFC("ClearChanges", CyTranslator().getText("TXT_KEY_WB_REVERT_CHANGES", ()), "", iX, iY, 3*iAdjust-3, iButtonWidth, WidgetTypes.WIDGET_PYTHON, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
				iX += 3*iAdjust
				if self.iPlayerAddMode == iModeAreaExporter3:
					screen.setButtonGFC("CancelMoveMap", CyTranslator().getText("TXT_KEY_SCREEN_CANCEL", ()), "", iX, iY, 3*iAdjust-3, iButtonWidth, WidgetTypes.WIDGET_PYTHON, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
				else:
					screen.setButtonGFC("Export", CyTranslator().getText("TXT_KEY_WB_EXPORT", ()), "", iX, iY, 3*iAdjust-3, iButtonWidth, WidgetTypes.WIDGET_PYTHON, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

			elif self.iPlayerAddMode in lRevealModes:
				iX = iXStart + 8
				screen.addDropDownBoxGFC("RevealMode", iX, iY, screen.getXResolution() - 8 - iX, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				screen.addPullDownString("RevealMode", CyTranslator().getText("TXT_KEY_REVEAL_PLOT",()), 0, 0, self.iPlayerAddMode == lRevealModes[0])
				screen.addPullDownString("RevealMode", CyTranslator().getText("TXT_KEY_REVEAL_SUBMARINE",()), 1, 1, self.iPlayerAddMode == lRevealModes[1])
				screen.addPullDownString("RevealMode", CyTranslator().getText("TXT_KEY_REVEAL_STEALTH",()), 2, 2, self.iPlayerAddMode == lRevealModes[2])
				screen.addPullDownString("RevealMode", gc.getMissionInfo(gc.getInfoTypeForString("MISSION_PLUNDER")).getDescription(), 3, 3, self.iPlayerAddMode == lRevealModes[3])
				screen.addPullDownString("RevealMode", CyTranslator().getText("TXT_KEY_REVEAL_SATELLITE",()), 4, 4, self.iPlayerAddMode == lRevealModes[4])

				iY += iAdjust
				screen.setImageButton("WorldBuilderRevealAll", CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_REVEAL_ALL_TILES").getPath(), iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_WB_REVEAL_ALL_BUTTON, -1, -1)
				iX += iAdjust
				screen.addDropDownBoxGFC("WorldBuilderPlayerChoice", iX, iY, screen.getXResolution() - 8 - iX, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for iPlayer in players.all().where(lambda p: player(p).isEverAlive()):
					sName = name(iPlayer)
					if not player(iPlayer).isAlive():
						sName = "*" + sName
					if player(iPlayer).isTurnActive():
						sName = "[" + sName + "]"
					screen.addPullDownString("WorldBuilderPlayerChoice", sName, iPlayer, iPlayer, self.m_iCurrentPlayer == iPlayer)
				iX = iXStart + 8
				iY += iAdjust
				screen.setImageButton("WorldBuilderUnrevealAll", CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_UNREVEAL_ALL_TILES").getPath(), iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_WB_UNREVEAL_ALL_BUTTON, -1, -1)
				iX += iAdjust
				iWidth = (screen.getXResolution() - 8 - iX - 3)/2
				screen.addDropDownBoxGFC("BrushWidth", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for i in range(1, 11):
					screen.addPullDownString("BrushWidth", "W: " + str(i), i, i, self.iBrushWidth == i)
				screen.addPullDownString("BrushWidth", "W: " + "--", -1, -1, self.iBrushWidth == -1)
				iX += iWidth
				screen.addDropDownBoxGFC("BrushHeight", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for i in range(1, 11):
					screen.addPullDownString("BrushHeight", "H: " + str(i), i, i, self.iBrushHeight == i)
				screen.addPullDownString("BrushHeight", "H: " + "--", -1, -1, self.iBrushHeight == -1)

			elif self.iPlayerAddMode == iModeEraseAll:
				iX = iXStart + 8
				screen.setImageButton( "WorldBuilderEraseAll", CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_UNREVEAL_ALL_TILES").getPath(), iX, iY, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_PYTHON, 1029, 29)
				iX += iAdjust
				iWidth = (screen.getXResolution() - 8 - iX - 3)/2
				screen.addDropDownBoxGFC("BrushWidth", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for i in range(1, 11):
					screen.addPullDownString("BrushWidth", "W: " + str(i), i, i, self.iBrushWidth == i)
				screen.addPullDownString("BrushWidth", "W: " + "--", -1, -1, self.iBrushWidth == -1)
				iX += iWidth
				screen.addDropDownBoxGFC("BrushHeight", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for i in range(1, 11):
					screen.addPullDownString("BrushHeight", "H: " + str(i), i, i, self.iBrushHeight == i)
				screen.addPullDownString("BrushHeight", "H: " + "--", -1, -1, self.iBrushHeight == -1)
			else:
				screen.deleteWidget("WorldBuilderBackgroundBottomPanel")
			self.setCurrentModeCheckbox()
			self.setSelectionTable()

	def setCurrentModeCheckbox(self):
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN )
		screen.setState("EditUnitData", self.iPlayerAddMode == iModeEditUnit)
		screen.setState("EditPromotions", self.iPlayerAddMode == iModePromotions)
		screen.setState("WorldBuilderNormalPlayerModeButton", self.iPlayerAddMode in lPlayerModes)
		screen.setState("WorldBuilderNormalMapModeButton", self.iPlayerAddMode in lMapModes)
		screen.setState("WorldBuilderRevealTileModeButton", self.iPlayerAddMode in lRevealModes)
		screen.setState("WorldBuilderLandmarkButton", self.iPlayerAddMode == iModeAddLandMark)
		screen.setState("WorldBuilderEraseButton", self.iPlayerAddMode == iModeEraseAll)
		screen.setState("AddOwnershipButton", self.iPlayerAddMode == iModeOwnership)
		screen.setState("AddUnitsButton", self.iPlayerAddMode == iModeUnits)
		screen.setState("AddBuildingsButton", self.iPlayerAddMode == iModeBuildings)
		screen.setState("AddCityButton", self.iPlayerAddMode == iModeCity)
		screen.setState("EditStartingPlot", self.iPlayerAddMode == iModeStartingPlot)
		screen.setState("EditPlotData", self.iPlayerAddMode == iModePlotData)
		screen.setState("EditEvents", self.iPlayerAddMode == iModeEvents)
		screen.setState("AddRiverButton", self.iPlayerAddMode == iModeRiver)
		screen.setState("AddImprovementButton", self.iPlayerAddMode == iModeImprovements)
		screen.setState("AddBonusButton", self.iPlayerAddMode == iModeBonus)
		screen.setState("AddPlotTypeButton", self.iPlayerAddMode == iModePlotType)
		screen.setState("AddTerrainButton", self.iPlayerAddMode == iModeTerrain)
		screen.setState("AddRouteButton", self.iPlayerAddMode == iModeRoutes)
		screen.setState("AddFeatureButton", self.iPlayerAddMode == iModeFeatures)
		screen.setState("EditCityDataI", self.iPlayerAddMode == iModeCityDataI)
		screen.setState("EditCityDataII", self.iPlayerAddMode == iModeCityDataII)
		screen.setState("EditCityBuildings", self.iPlayerAddMode == iModeCityBuildings)
		screen.setState("PythonEffectButton", bPython)
		screen.setState("HideInactive", bHideInactive)
		screen.setState("SensibilityCheck", self.bSensibility)
		screen.setState("RegionButton", self.bRegion)
		screen.setState("DoCMapsScreen", self.iPlayerAddMode in lDoCMapModes)
		screen.setState("FlipButton", self.iPlayerAddMode == iModeFlip)
		screen.setState("CoreButton", self.iPlayerAddMode == iModeCore)
		screen.setState("SettlerValueButton", self.iPlayerAddMode == iModeSettlerValue)
		screen.setState("WarMapButton", self.iPlayerAddMode == iModeWarMap)
		screen.setState("ReligionMapButton", self.iPlayerAddMode == iModeReligionMap)
		screen.setState("RegionMapButton", self.iPlayerAddMode == iModeRegionMap)
		screen.setState("VictoryMapButton", self.iPlayerAddMode == iModeVictoryMap)
		screen.setState("MoveMapScreen", self.iPlayerAddMode in lMoveMapModes)
		screen.setState("FlipAIButton", self.bFlipAI)
		screen.setState("VictoryRectangleButton", self.bVictoryRectangle)
		screen.setState("AreaExporterScreen", self.iPlayerAddMode in lAreaExportModes)
		screen.setState("AreaExportWater", self.bWaterException)
		screen.setState("AreaExportPeak", self.bPeaksException)
		screen.setState("AllRegionsButton", self.bAllRegions)

	def setSelectionTable(self):
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
		iWidth = 200
		iCivilization = gc.getPlayer(self.m_iCurrentPlayer).getCivilizationType()
		if self.iPlayerAddMode == iModeUnits:
			iY = 25
			screen.addDropDownBoxGFC("WBSelectClass", 0, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			screen.addPullDownString("WBSelectClass", CyTranslator().getText("TXT_KEY_WB_CITY_ALL",()), -2, -2, -2 == self.iSelectClass)
			screen.addPullDownString("WBSelectClass", CyTranslator().getText("TXT_PEDIA_NON_COMBAT",()), -1, -1, -1 == self.iSelectClass)
			for iCombatClass in xrange(gc.getNumUnitCombatInfos()):
				screen.addPullDownString("WBSelectClass", gc.getUnitCombatInfo(iCombatClass).getDescription(), iCombatClass, iCombatClass, iCombatClass == self.iSelectClass)

			lItems = []
			for i in xrange(gc.getNumUnitInfos()):
				ItemInfo = gc.getUnitInfo(i)
				if bHideInactive:
					iClass = ItemInfo.getUnitClassType()
					if gc.getCivilizationInfo(iCivilization).getCivilizationUnits(iClass) != i: continue
				if ItemInfo.getUnitCombatType() != self.iSelectClass and self.iSelectClass > -2: continue
				lItems.append([ItemInfo.getDescription(), i])
			lItems.sort()

			iY += 30
			iHeight = min(len(lItems) * 24 + 2, screen.getYResolution() - iY)
			screen.addTableControlGFC("WBSelectItem", 1, 0, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
			screen.setTableColumnHeader("WBSelectItem", 0, "", iWidth)
			bValid = False
			for item in lItems:
				iRow = screen.appendTableRow("WBSelectItem")
				if self.iSelection == item[1]: bValid = True
				screen.setTableText("WBSelectItem", 0, iRow, "<font=3>" + item[0] + "</font>", gc.getUnitInfo(item[1]).getButton(), WidgetTypes.WIDGET_PYTHON, 8202, item[1], CvUtil.FONT_LEFT_JUSTIFY)
			if not bValid:
				self.iSelection = -1
				if len(lItems) > 0:
					self.iSelection = lItems[0][1]

		elif self.iPlayerAddMode == iModeBuildings:
			iY = 25
			sWonder = CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS", ())
			screen.addDropDownBoxGFC("WBSelectClass", 0, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			screen.addPullDownString("WBSelectClass", CyTranslator().getText("TXT_KEY_WB_CITY_ALL",()), 0, 0, 0 == self.iSelectClass)
			screen.addPullDownString("WBSelectClass", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING",()), 1, 1, 1 == self.iSelectClass)
			screen.addPullDownString("WBSelectClass", CyTranslator().getText("TXT_KEY_PEDIA_NATIONAL_WONDER", ()), 2, 2, 2 == self.iSelectClass)
			screen.addPullDownString("WBSelectClass", CyTranslator().getText("TXT_KEY_PEDIA_TEAM_WONDER", ()), 3, 3, 3 == self.iSelectClass)
			screen.addPullDownString("WBSelectClass", CyTranslator().getText("TXT_KEY_PEDIA_WORLD_WONDER", ()), 4, 4, 4 == self.iSelectClass)

			lItems = []
			for i in xrange(gc.getNumBuildingInfos()):
				ItemInfo = gc.getBuildingInfo(i)
				iClass = ItemInfo.getBuildingClassType()
				if bHideInactive:
					if gc.getCivilizationInfo(iCivilization).getCivilizationBuildings(iClass) != i: continue
				if self.iSelectClass == 1:
					if isLimitedWonderClass(iClass): continue
				elif self.iSelectClass == 2:
					if not isNationalWonderClass(iClass): continue
				elif self.iSelectClass == 3:
					if not isTeamWonderClass(iClass): continue
				elif self.iSelectClass == 4:
					if not isWorldWonderClass(iClass): continue
				lItems.append([ItemInfo.getDescription(), i])
			lItems.sort()

			iY += 30
			iHeight = min(len(lItems) * 24 + 2, screen.getYResolution() - iY)
			screen.addTableControlGFC("WBSelectItem", 1, 0, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
			screen.setTableColumnHeader("WBSelectItem", 0, "", iWidth)
			bValid = False
			for item in lItems:
				iRow = screen.appendTableRow("WBSelectItem")
				if self.iSelection == item[1]: bValid = True
				screen.setTableText("WBSelectItem", 0, iRow, "<font=3>" + item[0] + "</font>", gc.getBuildingInfo(item[1]).getButton(), WidgetTypes.WIDGET_HELP_BUILDING, item[1], item[1], CvUtil.FONT_LEFT_JUSTIFY)
			if not bValid:
				self.iSelection = -1
				if len(lItems) > 0:
					self.iSelection = lItems[0][1]

		elif self.iPlayerAddMode == iModeFeatures:
			iY = 55
			lItems = [[gc.getFeatureInfo(i).getDescription(), i] for i in xrange(gc.getNumFeatureInfos())]
			lItems.sort()

			iHeight = min(len(lItems) * 24 + 2, screen.getYResolution() - iY)
			screen.addTableControlGFC("WBSelectItem", 1, 0, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
			screen.setTableColumnHeader("WBSelectItem", 0, "", iWidth)
			for item in lItems:
				iRow = screen.appendTableRow("WBSelectItem")
				if self.iSelection == -1:
					self.iSelection = item[1]
				screen.setTableText("WBSelectItem", 0, iRow, "<font=3>" + item[0] + "</font>", gc.getFeatureInfo(item[1]).getButton(), WidgetTypes.WIDGET_PYTHON, 7874, item[1], CvUtil.FONT_LEFT_JUSTIFY)

		elif self.iPlayerAddMode == iModeImprovements:
			iY = 25
			lItems = [[gc.getImprovementInfo(i).getDescription(), i] for i in xrange(gc.getNumImprovementInfos()) if not gc.getImprovementInfo(i).isGraphicalOnly()]
			lItems.sort()

			iHeight = min(len(lItems) * 24 + 2, screen.getYResolution() - iY)
			screen.addTableControlGFC("WBSelectItem", 1, 0, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
			screen.setTableColumnHeader("WBSelectItem", 0, "", iWidth)
			for item in lItems:
				iRow = screen.appendTableRow("WBSelectItem")
				if self.iSelection == -1:
					self.iSelection = item[1]
				screen.setTableText("WBSelectItem", 0, iRow, "<font=3>" + item[0] + "</font>", gc.getImprovementInfo(item[1]).getButton(), WidgetTypes.WIDGET_PYTHON, 7877, item[1], CvUtil.FONT_LEFT_JUSTIFY)

		elif self.iPlayerAddMode == iModeBonus:
			iY = 25
			screen.addDropDownBoxGFC("WBSelectClass", 0, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			screen.addPullDownString("WBSelectClass", CyTranslator().getText("TXT_KEY_WB_CITY_ALL",()), -1, -1, -1 == self.iSelectClass)
			screen.addPullDownString("WBSelectClass", CyTranslator().getText("TXT_KEY_GLOBELAYER_RESOURCES_GENERAL",()), 0, 0, 0 == self.iSelectClass)
			iBonusClass = 1
			while not gc.getBonusClassInfo(iBonusClass) is None:
				sText = gc.getBonusClassInfo(iBonusClass).getType()
				sText = sText[sText.find("_") +1:]
				sText = sText.lower()
				sText = sText.capitalize()
				screen.addPullDownString("WBSelectClass", sText, iBonusClass, iBonusClass, iBonusClass == self.iSelectClass)
				iBonusClass += 1

			lItems = [[gc.getBonusInfo(i).getDescription(), i] for i in xrange(gc.getNumBonusInfos()) if not (gc.getBonusInfo(i).getBonusClassType() != self.iSelectClass and self.iSelectClass > -1)]
			lItems.sort()

			iY += 30
			iHeight = min(len(lItems) * 24 + 2, screen.getYResolution() - iY)
			screen.addTableControlGFC("WBSelectItem", 1, 0, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
			screen.setTableColumnHeader("WBSelectItem", 0, "", iWidth)
			for item in lItems:
				iRow = screen.appendTableRow("WBSelectItem")
				if self.iSelection == -1:
					self.iSelection = item[1]
				screen.setTableText("WBSelectItem", 0, iRow, "<font=3>" + item[0] + "</font>", gc.getBonusInfo(item[1]).getButton(), WidgetTypes.WIDGET_PYTHON, 7878, item[1], CvUtil.FONT_LEFT_JUSTIFY)

		elif self.iPlayerAddMode == iModeRoutes:
			iY = 25
			lItems = [[gc.getRouteInfo(i).getDescription(), i] for i in xrange(gc.getNumRouteInfos())]
			lItems.sort()

			iHeight = min(len(lItems) * 24 + 2, screen.getYResolution() - iY)
			screen.addTableControlGFC("WBSelectItem", 1, 0, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
			screen.setTableColumnHeader("WBSelectItem", 0, "", iWidth)
			for item in lItems:
				iRow = screen.appendTableRow("WBSelectItem")
				if self.iSelection == -1:
					self.iSelection = item[1]
				screen.setTableText("WBSelectItem", 0, iRow, "<font=3>" + item[0] + "</font>", gc.getRouteInfo(item[1]).getButton(), WidgetTypes.WIDGET_PYTHON, 6788, item[1], CvUtil.FONT_LEFT_JUSTIFY)

		elif self.iPlayerAddMode == iModeTerrain:
			iY = 25
			lItems = [[gc.getTerrainInfo(i).getDescription(), i] for i in xrange(gc.getNumTerrainInfos()) if not gc.getTerrainInfo(i).isGraphicalOnly()]
			lItems.sort()

			iHeight = min(len(lItems) * 24 + 2, screen.getYResolution() - iY)
			screen.addTableControlGFC("WBSelectItem", 1, 0, iY, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
			screen.setTableColumnHeader("WBSelectItem", 0, "", iWidth)
			for item in lItems:
				iRow = screen.appendTableRow("WBSelectItem")
				if self.iSelection == -1:
					self.iSelection = item[1]
				screen.setTableText("WBSelectItem", 0, iRow, "<font=3>" + item[0] + "</font>", gc.getTerrainInfo(item[1]).getButton(), WidgetTypes.WIDGET_PYTHON, 7875, item[1], CvUtil.FONT_LEFT_JUSTIFY)

		elif self.iPlayerAddMode == iModePlotType:
			iY = 25
			iHeight = 4 * 24 + 2
			screen.addTableControlGFC("WBSelectItem", 1, 0, 25, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
			screen.setTableColumnHeader("WBSelectItem", 0, "", iWidth)
			for i in xrange(PlotTypes.NUM_PLOT_TYPES):
				screen.appendTableRow("WBSelectItem")
			item = gc.getInfoTypeForString("TERRAIN_PEAK")
			if self.iSelection == -1:
				self.iSelection = item
			screen.setTableText("WBSelectItem", 0, 0, "<font=3>" + gc.getTerrainInfo(item).getDescription() + "</font>", gc.getTerrainInfo(item).getButton(), WidgetTypes.WIDGET_PYTHON, 7875, item, CvUtil.FONT_LEFT_JUSTIFY)
			item = gc.getInfoTypeForString("TERRAIN_HILL")
			screen.setTableText("WBSelectItem", 0, 1, "<font=3>" + gc.getTerrainInfo(item).getDescription() + "</font>", gc.getTerrainInfo(item).getButton(), WidgetTypes.WIDGET_PYTHON, 7875, item, CvUtil.FONT_LEFT_JUSTIFY)
			item = gc.getInfoTypeForString("TERRAIN_GRASS")
			screen.setTableText("WBSelectItem", 0, 2, "<font=3>" + gc.getTerrainInfo(item).getDescription() + "</font>", gc.getTerrainInfo(item).getButton(), WidgetTypes.WIDGET_PYTHON, 7875, item, CvUtil.FONT_LEFT_JUSTIFY)
			item = gc.getInfoTypeForString("TERRAIN_OCEAN")
			screen.setTableText("WBSelectItem", 0, 3, "<font=3>" + gc.getTerrainInfo(item).getDescription() + "</font>", gc.getTerrainInfo(item).getButton(), WidgetTypes.WIDGET_PYTHON, 7875, item, CvUtil.FONT_LEFT_JUSTIFY)
		self.refreshSelection()

	def refreshSelection(self):
		if self.iSelection == -1: return
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN)
		iWidth = 200
		screen.addTableControlGFC("WBCurrentItem", 1, 0, 0, iWidth, 25, False, True, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
		screen.setTableColumnHeader("WBCurrentItem", 0, "", iWidth)
		screen.appendTableRow("WBCurrentItem")
		if self.iPlayerAddMode == iModeUnits:
			ItemInfo = gc.getUnitInfo(self.iSelection)
			sText = "<font=3>" + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ()) + ItemInfo.getDescription() + "</color></font>"
			screen.setTableText("WBCurrentItem", 0, 0 , sText, ItemInfo.getButton(), WidgetTypes.WIDGET_PYTHON, 8202, self.iSelection, CvUtil.FONT_LEFT_JUSTIFY)
		elif self.iPlayerAddMode == iModeBuildings:
			ItemInfo = gc.getBuildingInfo(self.iSelection)
			sText = "<font=3>" + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ()) + ItemInfo.getDescription() + "</color></font>"
			screen.setTableText("WBCurrentItem", 0, 0 , sText, ItemInfo.getButton(), WidgetTypes.WIDGET_HELP_BUILDING, self.iSelection, 1, CvUtil.FONT_LEFT_JUSTIFY)
		elif self.iPlayerAddMode == iModeFeatures:
			ItemInfo = gc.getFeatureInfo(self.iSelection)
			sText = "<font=3>" + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ()) + ItemInfo.getDescription() + "</color></font>"
			screen.setTableText("WBCurrentItem", 0, 0 , sText, ItemInfo.getButton(), WidgetTypes.WIDGET_PYTHON, 7874, self.iSelection, CvUtil.FONT_LEFT_JUSTIFY)
			if ItemInfo.getNumVarieties() > 1:
				screen.addDropDownBoxGFC("WBSelectClass", 0, 25, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for i in xrange(ItemInfo.getNumVarieties()):
					screen.addPullDownString("WBSelectClass", CyTranslator().getText("TXT_KEY_WB_FEATURE_VARIETY", (i,)), i, i, i == self.iSelectClass)
			else:
				self.iSelectClass = 0
				screen.hide("WBSelectClass")
		elif self.iPlayerAddMode == iModeImprovements:
			ItemInfo = gc.getImprovementInfo(self.iSelection)
			sText = "<font=3>" + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ()) + ItemInfo.getDescription() + "</color></font>"
			screen.setTableText("WBCurrentItem", 0, 0 , sText, ItemInfo.getButton(), WidgetTypes.WIDGET_PYTHON, 7877, self.iSelection, CvUtil.FONT_LEFT_JUSTIFY)
		elif self.iPlayerAddMode == iModeBonus:
			ItemInfo = gc.getBonusInfo(self.iSelection)
			sText = "<font=3>" + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ()) + ItemInfo.getDescription() + "</color></font>"
			screen.setTableText("WBCurrentItem", 0, 0 , sText, ItemInfo.getButton(), WidgetTypes.WIDGET_PYTHON, 7878, self.iSelection, CvUtil.FONT_LEFT_JUSTIFY)
		elif self.iPlayerAddMode == iModeRoutes:
			ItemInfo = gc.getRouteInfo(self.iSelection)
			sText = "<font=3>" + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ()) + ItemInfo.getDescription() + "</color></font>"
			screen.setTableText("WBCurrentItem", 0, 0 , sText, ItemInfo.getButton(), WidgetTypes.WIDGET_PYTHON, 6788, self.iSelection, CvUtil.FONT_LEFT_JUSTIFY)
		elif self.iPlayerAddMode in [iModeTerrain, iModePlotType]:
			ItemInfo = gc.getTerrainInfo(self.iSelection)
			sText = "<font=3>" + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ()) + ItemInfo.getDescription() + "</color></font>"
			screen.setTableText("WBCurrentItem", 0, 0 , sText, ItemInfo.getButton(), WidgetTypes.WIDGET_PYTHON, 7875, self.iSelection, CvUtil.FONT_LEFT_JUSTIFY)
		else:
			screen.hide("WBCurrentItem")

## Platy Reveal Mode Start ##
	def revealAll(self, bReveal):
		for i in xrange(CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.isNone(): continue
			self.RevealCurrentPlot(bReveal, pPlot)
		self.refreshReveal()
		return

	def RevealCurrentPlot(self, bReveal, pPlot):
		if self.iPlayerAddMode == iModeBlockade: return
		
		dRevealTypes = {iModeRevealPlot : "RevealPlot",
						iModeInvisibleSubmarine :  "INVISIBLE_SUBMARINE",
						iModeInvisibleStealth : "INVISIBLE_STEALTH",
						iModeInvisibleSatellite : "INVISIBLE_SATELLITE"}
		
		iType = gc.getInfoTypeForString(dRevealTypes[self.iPlayerAddMode])
		if iType == -1:
			if bReveal or (not pPlot.isVisible(self.m_iCurrentTeam, False)):
				pPlot.setRevealed(self.m_iCurrentTeam, bReveal, False, -1);
		elif bReveal:
			if pPlot.isInvisibleVisible(self.m_iCurrentTeam, iType): return
			pPlot.changeInvisibleVisibilityCount(self.m_iCurrentTeam, iType, 1)
		else:
			pPlot.changeInvisibleVisibilityCount(self.m_iCurrentTeam, iType, - pPlot.getInvisibleVisibilityCount(self.m_iCurrentTeam, iType))
		return

	def showRevealed(self, pPlot):
		if self.iPlayerAddMode == iModeRevealPlot:
			if not pPlot.isRevealed(self.m_iCurrentTeam, False):
				CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS, "COLOR_BLACK", 1.0)
		elif self.iPlayerAddMode == iModeInvisibleSubmarine:
			if pPlot.getInvisibleVisibilityCount(self.m_iCurrentTeam, gc.getInfoTypeForString("INVISIBLE_SUBMARINE")) == 0:
				CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS, "COLOR_RED", 1.0)
		elif self.iPlayerAddMode == iModeInvisibleStealth:
			if pPlot.getInvisibleVisibilityCount(self.m_iCurrentTeam, gc.getInfoTypeForString("INVISIBLE_STEALTH")) == 0:
				CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS, "COLOR_BLUE", 1.0)
		elif self.iPlayerAddMode == iModeInvisibleSatellite:
			if pPlot.getInvisibleVisibilityCount(self.m_iCurrentTeam, gc.getInfoTypeForString("INVISIBLE_SATELLITE")) == 0:
				CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS, "COLOR_PLAYER_DARK_GREEN", 1.0)
		elif self.iPlayerAddMode == iModeBlockade:
			if pPlot.isTradeNetwork(self.m_iCurrentTeam): return
			if gc.getTeam(self.m_iCurrentTeam).isAtWar(pPlot.getTeam()): return
			if pPlot.isTradeNetworkImpassable(self.m_iCurrentTeam): return
			if not pPlot.isOwned() and not pPlot.isRevealed(self.m_iCurrentTeam, False): return
			if not pPlot.isBonusNetwork(self.m_iCurrentTeam): return
			CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS, "COLOR_MAGENTA", 1.0)
		return
## Platy Reveal Mode End ##

	def updateOverlay(self):
		if self.iPlayerAddMode == iModeFlip:
			self.showFlipZone()
		elif self.iPlayerAddMode in [iModeCore, iModeSettlerValue]:
			self.showStabilityOverlay()
			dc.checkName(self.m_iCurrentPlayer)
		elif self.iPlayerAddMode == iModeWarMap:
			self.showWarOverlay()
		elif self.iPlayerAddMode == iModeReligionMap:
			self.showReligionOverlay()
		elif self.iPlayerAddMode == iModeRegionMap:
			self.showRegionOverlay()
		elif self.iPlayerAddMode == iModeVictoryMap:
			self.showVictoryOverlay()

	def showFlipZone(self):
		removeStabilityOverlay()
		if not is_minor(self.m_iCurrentPlayer):
		
			tSpawn = location(plots.capital(self.m_iCurrentPlayer))
			x, y = tSpawn
			CyEngine().fillAreaBorderPlotAlt(x, y, 1002, "COLOR_CYAN", 0.7)

			lHumanPlotList, lAIPlotList = self.getFlipZone(self.m_iCurrentPlayer)

			for plot in lHumanPlotList:
				x, y = location(plot)
				if (x, y) == tSpawn: continue
				CyEngine().fillAreaBorderPlotAlt(x, y, 1000, "COLOR_MAGENTA", 0.7)
					
			for plot in lAIPlotList:
				x, y = location(plot)
				CyEngine().fillAreaBorderPlotAlt(x, y, 1001, "COLOR_RED", 0.7)


	def changeFlipZone(self, plot, bAdd):
		lHumanPlotList, lAIPlotList	= self.getFlipZone(self.m_iCurrentPlayer)
		
		tPlot = location(plot)
		if bAdd:
			if self.bFlipAI:
				if tPlot in lHumanPlotList:
					lHumanPlotList = lHumanPlotList.including(tPlot)
				if tPlot not in lAIPlotList:
					lAIPlotList = lAIPlotList.including(tPlot)
			else:
				if tPlot not in lHumanPlotList:
					lHumanPlotList = lHumanPlotList.including(tPlot)
				if tPlot in lAIPlotList:
					lAIPlotList = lAIPlotList.including(tPlot)
		else:
			if tPlot in lHumanPlotList:
				lHumanPlotList = lHumanPlotList.without(tPlot)
			if tPlot in lAIPlotList:
				lAIPlotList = lAIPlotList.without(tPlot)
			
		self.dFlipZoneEdits[self.m_iCurrentPlayer] = (lHumanPlotList, lAIPlotList)


	def getFlipZone(self, iPlayer):
		if iPlayer in self.dFlipZoneEdits.keys():
			return self.dFlipZoneEdits[iPlayer]

		# Human flipzone
		humanBirthArea = plots.birth(self.m_iCurrentPlayer)
		
		if self.m_iCurrentPlayer in dExtendedBirthArea:
			aiBirthArea = plots.birth(self.m_iCurrentPlayer, True).without(dBirthAreaExceptions[self.m_iCurrentPlayer]).without(humanBirthArea)
		else:
			aiBirthArea = Plots([])
			
		return (humanBirthArea, aiBirthArea)

	def showStabilityOverlay(self):
		removeStabilityOverlay()
		if not is_minor(self.m_iCurrentPlayer):
			toggleStabilityOverlay(self.m_iCurrentPlayer)

	def showWarOverlay(self):
		removeStabilityOverlay()
		if not is_minor(self.m_iCurrentPlayer):
			for plot in plots.all().land():
				iPlotType = plot.getPlayerWarValue(self.m_iCurrentPlayer) / 2
				if iPlotType > 0:
					szColor = lWarMapColors[iPlotType-1]
					CyEngine().fillAreaBorderPlotAlt(plot.getX(), plot.getY(), 1000+iPlotType-1, szColor, 0.7)

	def showReligionOverlay(self):
		removeStabilityOverlay()
		for plot in plots.all().land():
			iValue = plot.getSpreadFactor(self.m_iCurrentReligion)
			if iValue > 0:
				szColor = lReligionMapColors[iValue-1]
				CyEngine().fillAreaBorderPlotAlt(plot.getX(), plot.getY(), 1000+iValue-1, szColor, 0.7)

	def showRegionOverlay(self):
		removeStabilityOverlay()
		for plot in plots.all().land().where(lambda p: p.getRegionID() != -1):
			iRegion = plot.getRegionID()
			if iRegion == self.m_iRegionMapID:
				CyEngine().fillAreaBorderPlotAlt(plot.getX(), plot.getY(), 1000, "COLOR_BLUE", 0.7)
			elif self.bAllRegions:
				CyEngine().fillAreaBorderPlotAlt(plot.getX(), plot.getY(), 1000+iRegion, self.dRegionColors[iRegion], 0.7)
			
	def determineRegionColors(self):
		lColors = ["COLOR_PLAYER_LIGHT_PURPLE", "COLOR_PLAYER_LIGHT_YELLOW", "COLOR_PLAYER_LIGHT_ORANGE", "COLOR_SILVER"]
		
		dNeighbourRegions = dict([(i, []) for i in range(iNumRegions)])
		dRegionColors = dict([(i, "") for i in range(iNumRegions)])
		
		for plot in plots.all().land().where(lambda p: p.getRegionID() != -1):
			iRegion = plot.getRegionID()
			for surroundingPlot in plots.surrounding(plot).where(lambda p: p.getRegionID() not in [-1, iRegion]):
				iNeighbourRegion = surroundingPlot.getRegionID()
				if iNeighbourRegion not in dNeighbourRegions[iRegion]:
					dNeighbourRegions[iRegion].append(iNeighbourRegion)

		for iRegion in range(iNumRegions):
			for color in lColors:
				for iNeighbourRegion in dNeighbourRegions[iRegion]:
					if dRegionColors[iNeighbourRegion] == color:
						break
				else:
					dRegionColors[iRegion] = color
					break
		self.dRegionColors = dRegionColors

	def showVictoryOverlay(self):
		removeStabilityOverlay()
		lRegions = []
		for index, goal in enumerate(data.players[self.m_iCurrentPlayer].historicalGoals + data.players[self.m_iCurrentPlayer].religiousGoals):
			for name, area in goal.areas.items():
				paintPlots(area.land(), 1000 + 2*index, "COLOR_MAGENTA")
				if self.bVictoryRectangle:
					paintPlots(area.water(), 1001 + 2*index, "COLOR_LIGHT_GREY")

	def showAreaExportOverlay(self):
		removeStabilityOverlay()
		for (x, y) in self.TempInfo:
			plot = gc.getMap().plot(x, y)
			if self.iPlayerAddMode == iModeAreaExporter3 and (x, y) == self.TempInfo[-1]:
				CyEngine().fillAreaBorderPlotAlt(x, y, 1002, "COLOR_RED", 0.7)
			elif plot.isPeak() and self.bPeaksException:
				CyEngine().fillAreaBorderPlotAlt(x, y, 1001, "COLOR_LIGHT_GREY", 0.7)
			elif plot.isWater() and self.bWaterException:
				CyEngine().fillAreaBorderPlotAlt(x, y, 1001, "COLOR_LIGHT_GREY", 0.7)
			else:
				CyEngine().fillAreaBorderPlotAlt(x, y, 1000, "COLOR_MAGENTA", 0.7)

	def showToolHelp(self):
		if self.iPlayerAddMode == iModeFlip:
			sText = CyTranslator().getText("TXT_KEY_WB_FLIPMAP_HELP", ())
		elif self.iPlayerAddMode == iModeCore:
			sText = CyTranslator().getText("TXT_KEY_WB_COREMAP_HELP", ())
		elif self.iPlayerAddMode == iModeSettlerValue:
			sText = CyTranslator().getText("TXT_KEY_WB_SETTLERMAP_HELP", ())
		elif self.iPlayerAddMode == iModeWarMap:
			sText = CyTranslator().getText("TXT_KEY_WB_WARMAP_HELP", ())
		elif self.iPlayerAddMode == iModeReligionMap:
			sText = CyTranslator().getText("TXT_KEY_WB_RELIGIONMAP_HELP", ())
		elif self.iPlayerAddMode == iModeRegionMap:
			sText = CyTranslator().getText("TXT_KEY_WB_REGIONMAP_HELP", ())
		elif self.iPlayerAddMode == iModeVictoryMap:
			sText = CyTranslator().getText("TXT_KEY_WB_VICTORYMAP_HELP", ())
		elif self.iPlayerAddMode in lMoveMapModes:
			sText = CyTranslator().getText("TXT_KEY_WB_MOVEMAP_HELP", ())
		elif self.iPlayerAddMode in lAreaExportModes:
			sText = CyTranslator().getText("TXT_KEY_WB_AREAEXPORT_HELP", ())
		else:
			return
		show(sText)

	def checkRegionTiles(self):
		tiles = plots.all().land().where(lambda p: p.getRegionID() == -1)
		if tiles:
			sText = "Land tiles without a defined region:\n" + str(tiles)
		else:
			sText = "All land tiles have a defined region"
		show(sText)

	def getPlotItems(self, tPlot):
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		lInfo = [tPlot, plot.getPlotType(), plot.getTerrainType(), plot.getRouteType(), (plot.getFeatureType(), plot.getFeatureVariety()), plot.getBonusType(-1), plot.getImprovementType(), (plot.getRiverNSDirection(), plot.getRiverWEDirection())]
		return lInfo

	def placePlotItems(self, tPlot):
		x, y = tPlot
		lInfos = self.TempInfo
		for j in range(len(lInfos)):
			if y-j < 0:
				break
			for i in range(len(lInfos[j])):
				item = lInfos[j][i]
				plot = gc.getMap().plot(x+i, y-j)
				plot.setPlotType(item[1], True, True)
				plot.setTerrainType(item[2], True, True)
				plot.setRouteType(item[3])
				plot.setFeatureType(item[4][0], item[4][1])
				plot.setBonusType(item[5])
				plot.setImprovementType(item[6])
				plot.setWOfRiver(item[7][0] != -1, item[7][0])
				plot.setNOfRiver(item[7][1] != -1, item[7][1])

	def moveMapReset(self):
		if self.iMoveMapReset == 0:
			return
		lInfos = self.TempInfo
		if self.iMoveMapReset == 1:
			for j in range(len(lInfos)):
				for i in range(len(lInfos[j])):
					item = lInfos[j][i]
					plot = gc.getMap().plot(item[0][0], item[0][1])
					plot.erase()
					plot.setPlotType(PlotTypes.PLOT_OCEAN, True, True)
		else:
			for j in range(len(lInfos)):
				for i in range(len(lInfos[j])):
					item = lInfos[j][i]
					plot = gc.getMap().plot(item[0][0], item[0][1])
					plot.erase()
					plot.setPlotType(PlotTypes.PLOT_LAND, True, True)
					plot.setTerrainType(iGrass, True, True)

	def Exit(self):
		CyInterface().setWorldBuilder(False)
		return

	def refreshAdvancedStartTabCtrl(self, bReuse):
		if CyInterface().isInAdvancedStart():
			iActiveTab = 0
			iActiveList = 0
			iActiveIndex = 0

			if self.m_advancedStartTabCtrl and bReuse:
				iActiveTab = self.m_advancedStartTabCtrl.getActiveTab()
				iActiveList = self.m_iAdvancedStartCurrentList[iActiveTab]
				iActiveIndex = self.m_iAdvancedStartCurrentIndexes[iActiveTab]

			self.m_iCurrentPlayer = CyGame().getActivePlayer()
			self.m_iCurrentTeam = CyGame().getActiveTeam()
			self.m_iAdvancedStartCurrentIndexes = []
			self.m_iAdvancedStartCurrentList = []

			initWBToolAdvancedStartControl()

			self.m_advancedStartTabCtrl = getWBToolAdvancedStartTabCtrl()

			self.m_advancedStartTabCtrl.setNumColumns((gc.getNumBuildingInfos()/10)+2);
			self.m_advancedStartTabCtrl.addTabSection(CyTranslator().getText("TXT_KEY_WB_AS_CITIES",()));
			self.m_iAdvancedStartCurrentIndexes.append(0)

			self.m_iAdvancedStartCurrentList.append(self.m_iASCityListID)

			#self.m_advancedStartTabCtrl.setNumColumns((gc.getNumUnitInfos()/10)+2);
			#self.m_advancedStartTabCtrl.addTabSection(CyTranslator().getText("TXT_KEY_WB_AS_UNITS",()));
			#self.m_iAdvancedStartCurrentIndexes.append(0)

			#self.m_iAdvancedStartCurrentList.append(0)

			self.m_advancedStartTabCtrl.setNumColumns((gc.getNumImprovementInfos()/10)+2);
			self.m_advancedStartTabCtrl.addTabSection(CyTranslator().getText("TXT_KEY_WB_AS_IMPROVEMENTS",()));
			self.m_iAdvancedStartCurrentIndexes.append(0)

			self.m_iAdvancedStartCurrentList.append(self.m_iASRoutesListID)

			#self.m_advancedStartTabCtrl.setNumColumns(1);
			#self.m_advancedStartTabCtrl.addTabSection(CyTranslator().getText("TXT_KEY_WB_AS_VISIBILITY",()));
			#self.m_iAdvancedStartCurrentIndexes.append(0)

			#self.m_iAdvancedStartCurrentList.append(0)

			#self.m_advancedStartTabCtrl.setNumColumns(1);
			#self.m_advancedStartTabCtrl.addTabSection(CyTranslator().getText("TXT_KEY_WB_AS_TECH",()));
			#self.m_iAdvancedStartCurrentIndexes.append(0)

			#self.m_iAdvancedStartCurrentList.append(0)

			addWBAdvancedStartControlTabs()

			self.m_advancedStartTabCtrl.setActiveTab(iActiveTab)
			self.setCurrentAdvancedStartIndex(iActiveIndex)
			self.setCurrentAdvancedStartList(iActiveList)
		else:
			self.m_advancedStartTabCtrl = getWBToolAdvancedStartTabCtrl()
			self.m_advancedStartTabCtrl.enable(False)
		return

	def setRiverHighlights(self):
		CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
		CyEngine().addColoredPlotAlt(self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY(), PlotStyles.PLOT_STYLE_RIVER_SOUTH, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS, "COLOR_GREEN", 1)

		for plot in plots.surrounding(self.m_pRiverStartPlot).without(self.m_pRiverStartPlot):
			CyEngine().addColoredPlotAlt(plot.getX(), plot.getY(), PlotStyles.PLOT_STYLE_BOX_FILL, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS, "COLOR_WHITE", .2)
		return

	def leftMouseDown (self, argsList):
		bShift, bCtrl, bAlt = argsList
		pPlayer = gc.getPlayer(self.m_iCurrentPlayer)
		if CyInterface().isInAdvancedStart():
			self.placeObject()
		elif bAlt or self.iPlayerAddMode == iModeEditUnit:
			if self.m_pCurrentPlot.getNumUnits():
				WBUnitScreen.WBUnitScreen(self).interfaceScreen(self.m_pCurrentPlot.getUnit(0))
		elif self.iPlayerAddMode == iModePromotions:
			if self.m_pCurrentPlot.getNumUnits():
				WBPromotionScreen.WBPromotionScreen().interfaceScreen(self.m_pCurrentPlot.getUnit(0))
		elif bCtrl or self.iPlayerAddMode == iModeCityDataI:
			if self.m_pCurrentPlot.isCity():
				WBCityEditScreen.WBCityEditScreen(self).interfaceScreen(self.m_pCurrentPlot.getPlotCity())
		elif self.iPlayerAddMode == iModeCityDataII:
			if self.m_pCurrentPlot.isCity():
				WBCityDataScreen.WBCityDataScreen().interfaceScreen(self.m_pCurrentPlot.getPlotCity())
		elif self.iPlayerAddMode == iModeCityBuildings:
			if self.m_pCurrentPlot.isCity():
				WBBuildingScreen.WBBuildingScreen().interfaceScreen(self.m_pCurrentPlot.getPlotCity())
		elif self.iPlayerAddMode in lRevealModes:
			if not self.m_pCurrentPlot.isNone():
				self.setMultipleReveal(True)
		elif self.iPlayerAddMode == iModePlotData:
			WBPlotScreen.WBPlotScreen().interfaceScreen(self.m_pCurrentPlot)
		elif self.iPlayerAddMode == iModeEvents:
			WBEventScreen.WBEventScreen().interfaceScreen(self.m_pCurrentPlot)
		elif self.iPlayerAddMode == iModeStartingPlot:
			pPlayer.setStartingPlot(self.m_pCurrentPlot, True)
			self.refreshStartingPlots()
		elif self.iPlayerAddMode == iModeTargetPlot:
			self.iPlayerAddMode = iModeEditUnit
			if len(self.TempInfo) >= 2:
				pPlayerX = gc.getPlayer(self.TempInfo[0])
				if pPlayerX:
					pUnitX = pPlayerX.getUnit(self.TempInfo[1])
					if pUnitX:
						WBUnitScreen.WBUnitScreen(self).interfaceScreen(pUnitX)
		elif self.iPlayerAddMode == iModeMoveUnits:
			if len(self.lMoveUnit) > 0:
				for item in self.lMoveUnit:
					loopUnit = gc.getPlayer(item[0]).getUnit(item[1])
					if loopUnit.isNone(): continue
					move(loopUnit, self.m_pCurrentPlot)
				pUnitX = gc.getPlayer(self.lMoveUnit[0][0]).getUnit(self.lMoveUnit[0][1])
				self.lMoveUnit = []
				self.iPlayerAddMode = iModeEditUnit
				WBUnitScreen.WBUnitScreen(self).interfaceScreen(pUnitX)
		elif self.iPlayerAddMode in [iModeMoveCity, iModeMoveCityPlus]:
			if self.m_pCurrentPlot.isCity(): return
			pOldCity = pPlayer.getCity(self.iMoveCity)
			if pOldCity:
				x, y = location(self.m_pCurrentPlot)
				pNewCity = pPlayer.initCity(x, y)
				sName = cnm.getFoundName(self.m_iCurrentPlayer, location(self.m_pCurrentPlot))
				if not sName:
					sName = pOldCity.getName()
				pOldCity.setName("ToBeRazed", False)
				pNewCity.setName(sName, True)
				self.copyCityStats(pOldCity, pNewCity, True)
				pOldPlot = pOldCity.plot()
				pOldCity.kill()
				pOldPlot.setImprovementType(-1)
				if self.iPlayerAddMode == iModeMoveCityPlus:
					for item in self.lMoveUnit:
						loopUnit = gc.getPlayer(item[0]).getUnit(item[1])
						if loopUnit.isNone(): continue
						move(loopUnit, self.m_pCurrentPlot)
					self.lMoveUnit = []
			self.iPlayerAddMode = iModeCityDataI
			self.iMoveCity = -1
			dc.checkName(self.m_iCurrentPlayer)
		elif self.iPlayerAddMode in [iModeDuplicateCity, iModeDuplicateCityPlus]:
			if self.m_pCurrentPlot.isCity(): return
			pOldCity = pPlayer.getCity(self.iMoveCity)
			if pOldCity:
				x, y = location(self.m_pCurrentPlot)
				pNewCity = pPlayer.initCity(x, y)
				sName = cnm.getFoundName(self.m_iCurrentPlayer, (x, y))
				if sName:
					pNewCity.setName(sName, True)
				self.copyCityStats(pOldCity, pNewCity, False)
				if self.iPlayerAddMode == iModeDuplicateCityPlus:
					for item in self.lMoveUnit:
						loopUnit = gc.getPlayer(item[0]).getUnit(item[1])
						if loopUnit.isNone(): continue
						pNewUnit = pPlayer.initUnit(loopUnit.getUnitType(), x, y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
						pNewUnit.setName(loopUnit.getNameNoDesc())
						pNewUnit.setLevel(loopUnit.getLevel())
						pNewUnit.setExperience(loopUnit.getExperience(), -1)
						pNewUnit.setBaseCombatStr(loopUnit.baseCombatStr())
						for iPromotion in xrange(gc.getNumPromotionInfos()):
							pNewUnit.setHasPromotion(iPromotion, loopUnit.isHasPromotion(iPromotion))
						pNewUnit.setDamage(loopUnit.getDamage(), -1)
						pNewUnit.setMoves(loopUnit.getMoves())
						pNewUnit.setLeaderUnitType(loopUnit.getLeaderUnitType())
						pNewUnit.changeCargoSpace(loopUnit.cargoSpace() - pNewUnit.cargoSpace())
						pNewUnit.setImmobileTimer(loopUnit.getImmobileTimer())
						pNewUnit.setScriptData(loopUnit.getScriptData())
			dc.checkName(self.m_iCurrentPlayer)
		elif self.iPlayerAddMode == iModeMoveMap:
			x, y = location(self.m_pCurrentPlot)
			lList = []
			for j in range(self.iBrushHeight):
				if y-j < 0:
					break
				lList2 = []
				for i in range(self.iBrushWidth):
					lList2.append(self.getPlotItems((x+i, y-j)))
					CyEngine().fillAreaBorderPlotAlt(x+i, y-j, 1000, "COLOR_RED", 0.7)
				lList.append(lList2)
			self.TempInfo = lList
			self.iPlayerAddMode = iModeMoveMap2
			self.refreshSideMenu()
		elif self.iPlayerAddMode == iModeMoveMap2:
			removeStabilityOverlay()
			lMoveMapModesReset()
			self.placePlotItems(location(self.m_pCurrentPlot))
			self.iPlayerAddMode = iModeMoveMap
			self.refreshSideMenu()
			self.TempInfo = []
		elif self.iPlayerAddMode == iModeAreaExporter2:
			x, y = location(self.m_pCurrentPlot)
			CyEngine().fillAreaBorderPlotAlt(x, y, 1002, "COLOR_RED", 0.7)
			self.TempInfo.append((x, y))
			self.iPlayerAddMode = iModeAreaExporter3
			self.refreshSideMenu()
		elif self.iPlayerAddMode == iModeAreaExporter3:
			self.iPlayerAddMode = iModeAreaExporter2
			tPlot = self.TempInfo.pop()
			for plot in plots.start(tPlot).end(self.m_pCurrentPlot):
				if location(plot) not in self.TempInfo:
					self.TempInfo.append(location(plot))
			self.showAreaExportOverlay()
			self.refreshSideMenu()
		elif self.useLargeBrush():
			self.placeMultipleObjects()
		else:
			self.placeObject()
		self.updateOverlay()
		return 1

	def copyCityStats(self, pOldCity, pNewCity, bMove):
		pNewCity.setPopulation(pOldCity.getPopulation())
		for iBuilding in xrange(gc.getNumBuildingInfos()):
			pNewCity.setBuildingProduction(iBuilding, pOldCity.getBuildingProduction(iBuilding))
			if gc.getBuildingInfo(iBuilding).isCapital() and not bMove: continue
			pNewCity.setNumRealBuilding(iBuilding, pOldCity.getNumRealBuilding(iBuilding))
		for iClass in xrange(gc.getNumBuildingClassInfos()):
			for iCommerce in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
				pNewCity.setBuildingCommerceChange(iClass, iCommerce, pOldCity.getBuildingCommerceChange(iClass, iCommerce))
			for iYield in xrange(YieldTypes.NUM_YIELD_TYPES):
				pNewCity.setBuildingYieldChange(iClass, iYield, pOldCity.getBuildingYieldChange(iClass, iYield))
	##		pNewCity.setBuildingHappyChange(iClass, pOldCity.getBuildingHappyChange(iClass))
	##		pNewCity.setBuildingHealthChange(iClass, pOldCity.getBuildingHealthChange(iClass))
		for iPlayerX in xrange(gc.getMAX_PLAYERS()):
			pNewCity.setCultureTimes100(iPlayerX, pOldCity.getCultureTimes100(iPlayerX), False)
		for iReligion in xrange(gc.getNumReligionInfos()):
			pNewCity.setHasReligion(iReligion, pOldCity.isHasReligion(iReligion), False, False)
			if bMove and pOldCity.isHolyCityByType(iReligion):
				CyGame().setHolyCity(iReligion, pNewCity, False)
			pNewCity.changeReligionInfluence(iReligion, pOldCity.getReligionInfluence(iReligion) - pNewCity.getReligionInfluence(iReligion))
			pNewCity.changeStateReligionHappiness(iReligion, pOldCity.getStateReligionHappiness(iReligion) - pNewCity.getStateReligionHappiness(iReligion))
		for iCorporation in xrange(gc.getNumCorporationInfos()):
			pNewCity.setHasCorporation(iCorporation, pOldCity.isHasCorporation(iCorporation), False, False)
			if bMove and pOldCity.isHeadquartersByType(iCorporation):
				CyGame().setHeadquarters(iCorporation, pNewCity, False)
		for iImprovement in xrange(gc.getNumImprovementInfos()):
			pNewCity.changeImprovementFreeSpecialists(iImprovement, pOldCity.getImprovementFreeSpecialists(iImprovement) - pNewCity.getImprovementFreeSpecialists(iImprovement))
		for iSpecialist in xrange(gc.getNumSpecialistInfos()):
			pNewCity.setFreeSpecialistCount(iSpecialist, pOldCity.getFreeSpecialistCount(iSpecialist))
			pNewCity.setForceSpecialistCount(iSpecialist, pOldCity.getForceSpecialistCount(iSpecialist))
		for iUnit in xrange(gc.getNumUnitInfos()):
			pNewCity.setUnitProduction(iUnit, pOldCity.getUnitProduction(iUnit))
			pNewCity.setGreatPeopleUnitProgress(iUnit, pOldCity.getGreatPeopleUnitProgress(iUnit))
		for iCommerce in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
			pNewCity.changeSpecialistCommerce(iCommerce, pOldCity.getSpecialistCommerce(iCommerce) - pNewCity.getSpecialistCommerce(iCommerce))
		for iBonus in xrange(gc.getNumBonusInfos()):
			pNewCity.changeFreeBonus(iBonus, pOldCity.getFreeBonus(iBonus) - pNewCity.getFreeBonus(iBonus))
			while pOldCity.isNoBonus(iBonus) != pNewCity.isNoBonus(iBonus):
				if pOldCity.isNoBonus(iBonus):
					pNewCity.changeNoBonusCount(iBonus, 1)
				else:
					pNewCity.changeNoBonusCount(iBonus, -1)
		for iOrder in xrange(pOldCity.getOrderQueueLength()):
			OrderData = pOldCity.getOrderFromQueue(iOrder)
			pNewCity.pushOrder(OrderData.eOrderType, OrderData.iData1, OrderData.iData2, OrderData.bSave, False, True, False)
		pNewCity.changeBaseGreatPeopleRate(pOldCity.getBaseGreatPeopleRate() - pNewCity.getBaseGreatPeopleRate())
		pNewCity.changeConscriptAngerTimer(pOldCity.getConscriptAngerTimer() - pNewCity.getConscriptAngerTimer())
		pNewCity.changeDefenseDamage(pOldCity.getDefenseDamage() - pNewCity.getDefenseDamage())
		pNewCity.changeDefyResolutionAngerTimer(pOldCity.getDefyResolutionAngerTimer() - pNewCity.getDefyResolutionAngerTimer())
		pNewCity.changeEspionageHappinessCounter(pOldCity.getEspionageHappinessCounter() - pNewCity.getEspionageHappinessCounter())
		pNewCity.changeEspionageHealthCounter(pOldCity.getEspionageHealthCounter() - pNewCity.getEspionageHealthCounter())
		pNewCity.changeExtraHappiness(pOldCity.getExtraHappiness() - pNewCity.getExtraHappiness())
		pNewCity.changeExtraHealth(pOldCity.getExtraHealth() - pNewCity.getExtraHealth())
		pNewCity.changeExtraTradeRoutes(pOldCity.getExtraTradeRoutes() - pNewCity.getExtraTradeRoutes())
		pNewCity.changeGreatPeopleProgress(pOldCity.getGreatPeopleProgress() - pNewCity.getGreatPeopleProgress())
		pNewCity.changeHappinessTimer(pOldCity.getHappinessTimer() - pNewCity.getHappinessTimer())
		pNewCity.changeHurryAngerTimer(pOldCity.getHurryAngerTimer() - pNewCity.getHurryAngerTimer())
		pNewCity.setAirliftTargeted(pOldCity.isAirliftTargeted())
		pNewCity.setBombarded(pOldCity.isBombarded())
		pNewCity.setCitizensAutomated(pOldCity.isCitizensAutomated())
		pNewCity.setDrafted(pOldCity.isDrafted())
		pNewCity.setFeatureProduction(pOldCity.getFeatureProduction())
		pNewCity.setFood(pOldCity.getFood())
		pNewCity.setHighestPopulation(pOldCity.getHighestPopulation())
		pNewCity.setNeverLost(pOldCity.isNeverLost())
		pNewCity.setOccupationTimer(pOldCity.getOccupationTimer())
		pNewCity.setOverflowProduction(pOldCity.getOverflowProduction())
		pNewCity.setPlundered(pOldCity.isPlundered())
		pNewCity.setProduction(pOldCity.getProduction())
		pNewCity.setProductionAutomated(pOldCity.isProductionAutomated())
		pNewCity.setScriptData(pOldCity.getScriptData())
		pNewCity.setWallOverride(pOldCity.isWallOverride())

	def rightMouseDown (self, argsList):
		if CyInterface().isInAdvancedStart():
			self.removeObject()
		elif self.iPlayerAddMode in lRevealModes:
			if not self.m_pCurrentPlot.isNone():
				self.setMultipleReveal(False)
		elif self.iPlayerAddMode == iModeAreaExporter3:
			self.iPlayerAddMode = iModeAreaExporter2
			tPlot = self.TempInfo.pop()
			for plot in plots.start(tPlot).end(self.m_pCurrentPlot):
				if location(plot) in self.TempInfo:
					self.TempInfo.remove(location(plot))
			self.showAreaExportOverlay()
			self.refreshSideMenu()
		elif self.useLargeBrush():
			self.removeMultipleObjects()
		else:
			self.removeObject()
		self.updateOverlay()
		return 1

## Add "," ##
	def addComma(self, iValue):
		sTemp = str(iValue)
		sStart = ""
		while len(sTemp) > 0:
			if sTemp[0].isdigit(): break
			sStart += sTemp[0]
			sTemp = sTemp[1:]
		sEnd = sTemp[-3:]
		while len(sTemp) > 3:
			sTemp = sTemp[:-3]
			sEnd = sTemp[-3:] + "," + sEnd
		return (sStart + sEnd)
## Add "," ##

	def handleInput (self, inputClass):
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN )
		global iChange
		global bPython
		global bHideInactive
		global iSetValue
		global iWarValue
		global bRemove

		bDeleteOverlay = True

		if inputClass.getFunctionName() == "WorldBuilderEraseAll":
			for i in xrange(CyMap().numPlots()):
				self.m_pCurrentPlot = CyMap().plotByIndex(i)
				self.placeObject()

		elif inputClass.getFunctionName() == "TradeScreen":
			WBTradeScreen.WBTradeScreen().interfaceScreen()

		elif inputClass.getFunctionName() == "InfoScreen":
			WBInfoScreen.WBInfoScreen().interfaceScreen(self.m_iCurrentPlayer)

		elif inputClass.getFunctionName() == "EditGameOptions":
			WBGameDataScreen.WBGameDataScreen(self).interfaceScreen()

		elif inputClass.getFunctionName() == "EditReligions":
			WBReligionScreen.WBReligionScreen().interfaceScreen(self.m_iCurrentPlayer)

		elif inputClass.getFunctionName() == "EditCorporations":
			WBCorporationScreen.WBCorporationScreen().interfaceScreen(self.m_iCurrentPlayer)

		elif inputClass.getFunctionName() == "EditEspionage":
			WBDiplomacyScreen.WBDiplomacyScreen().interfaceScreen(self.m_iCurrentPlayer, True)

		elif inputClass.getFunctionName() == "EditPlayerData":
			WBPlayerScreen.WBPlayerScreen().interfaceScreen(self.m_iCurrentPlayer)

		elif inputClass.getFunctionName() == "EditTeamData":
			WBTeamScreen.WBTeamScreen().interfaceScreen(self.m_iCurrentTeam)

		elif inputClass.getFunctionName() == "EditTechnologies":
			WBTechScreen.WBTechScreen().interfaceScreen(self.m_iCurrentTeam)

		elif inputClass.getFunctionName() == "EditProjects":
			WBProjectScreen.WBProjectScreen().interfaceScreen(self.m_iCurrentTeam)

		elif inputClass.getFunctionName() == "EditUnitsCities":
			WBPlayerUnits.WBPlayerUnits().interfaceScreen(self.m_iCurrentPlayer)

		elif inputClass.getFunctionName() == "StoredDataScreen":
			WBStoredDataScreen.WBStoredDataScreen(self).interfaceScreen()

		elif inputClass.getFunctionName() == "WorldBuilderPlayerChoice":
			bDeleteOverlay = False
			if self.iPlayerAddMode == iModeReligionMap:
				self.m_iCurrentReligion = screen.getPullDownData("WorldBuilderPlayerChoice", screen.getSelectedPullDownID("WorldBuilderPlayerChoice"))
				self.showReligionOverlay()
			elif self.iPlayerAddMode == iModeRegionMap:
				self.m_iRegionMapID = screen.getPullDownData("WorldBuilderPlayerChoice", screen.getSelectedPullDownID("WorldBuilderPlayerChoice"))
				self.showRegionOverlay()
			elif self.iPlayerAddMode in lAreaExportModes:
				iID = screen.getPullDownData("WorldBuilderPlayerChoice", screen.getSelectedPullDownID("WorldBuilderPlayerChoice"))
				if iID == 0:
					self.iPlayerAddMode = iModeAreaExporter1
				else:
					self.iPlayerAddMode = iModeAreaExporter2
				self.refreshSideMenu()
			else:
				self.m_iCurrentPlayer = screen.getPullDownData("WorldBuilderPlayerChoice", screen.getSelectedPullDownID("WorldBuilderPlayerChoice"))
				self.m_iCurrentTeam = gc.getPlayer(self.m_iCurrentPlayer).getTeam()
				self.refreshSideMenu()
				if self.iPlayerAddMode in lRevealModes:
					self.refreshReveal()
				elif self.iPlayerAddMode == iModeStartingPlot:
					self.refreshStartingPlots()
				elif self.iPlayerAddMode in lDoCMapModes:
					self.updateOverlay()

		elif inputClass.getFunctionName() == "ChangeBy":
			if bRemove:
				iChange = -screen.getPullDownData("ChangeBy", screen.getSelectedPullDownID("ChangeBy"))
			else:
				iChange = screen.getPullDownData("ChangeBy", screen.getSelectedPullDownID("ChangeBy"))

		elif inputClass.getFunctionName() == "AddOwnershipButton":
			self.iPlayerAddMode = iModeOwnership
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "AddUnitsButton":
			self.iPlayerAddMode = iModeUnits
			self.iSelectClass = -2
			self.iSelection = -1
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "AddBuildingsButton":
			self.iPlayerAddMode = iModeBuildings
			self.iSelectClass = 0
			self.iSelection = -1
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "EditStartingPlot":
			self.iPlayerAddMode = iModeStartingPlot
			self.refreshSideMenu()
			self.refreshStartingPlots()

		elif inputClass.getFunctionName() == "EditPromotions":
			self.iPlayerAddMode = iModePromotions
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "AddCityButton":
			self.iPlayerAddMode = iModeCity
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "EditCityDataII":
			self.iPlayerAddMode = iModeCityDataII
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "EditCityBuildings":
			self.iPlayerAddMode = iModeCityBuildings
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "EditPlotData":
			self.iPlayerAddMode = iModePlotData
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "EditEvents":
			self.iPlayerAddMode = iModeEvents
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "AddImprovementButton":
			self.iPlayerAddMode = iModeImprovements
			self.iSelection = -1
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "AddBonusButton":
			self.iPlayerAddMode = iModeBonus
			self.iSelectClass = -1
			self.iSelection = -1
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "AddPlotTypeButton":
			self.iPlayerAddMode = iModePlotType
			self.iSelection = -1
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "AddTerrainButton":
			self.iPlayerAddMode = iModeTerrain
			self.iSelection = -1
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "AddRouteButton":
			self.iPlayerAddMode = iModeRoutes
			self.iSelection = -1
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "AddFeatureButton":
			self.iPlayerAddMode = iModeFeatures
			self.iSelectClass = 0
			self.iSelection = -1
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "AddRiverButton":
			self.iPlayerAddMode = iModeRiver
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "DoCMapsScreen":
			bDeleteOverlay = False
			self.iPlayerAddMode = iModeFlip
			self.refreshSideMenu()
			self.showFlipZone()

		elif inputClass.getFunctionName() == "FlipButton":
			bDeleteOverlay = False
			self.iPlayerAddMode = iModeFlip
			self.refreshSideMenu()
			self.showFlipZone()

		elif inputClass.getFunctionName() == "CoreButton":
			bDeleteOverlay = False
			self.iPlayerAddMode = iModeCore
			self.refreshSideMenu()
			self.showStabilityOverlay()

		elif inputClass.getFunctionName() == "SettlerValueButton":
			bDeleteOverlay = False
			self.iPlayerAddMode = iModeSettlerValue
			self.refreshSideMenu()
			self.showStabilityOverlay()

		elif inputClass.getFunctionName() == "WarMapButton":
			bDeleteOverlay = False
			self.iPlayerAddMode = iModeWarMap
			self.refreshSideMenu()
			self.showWarOverlay()

		elif inputClass.getFunctionName() == "ReligionMapButton":
			bDeleteOverlay = False
			self.iPlayerAddMode = iModeReligionMap
			self.refreshSideMenu()
			self.showReligionOverlay()

		elif inputClass.getFunctionName() == "RegionMapButton":
			bDeleteOverlay = False
			self.iPlayerAddMode = iModeRegionMap
			self.refreshSideMenu()
			self.showRegionOverlay()

		elif inputClass.getFunctionName() == "VictoryMapButton":
			bDeleteOverlay = False
			self.iPlayerAddMode = iModeVictoryMap
			self.refreshSideMenu()
			self.showVictoryOverlay()

		elif inputClass.getFunctionName() == "MoveMapScreen":
			self.iPlayerAddMode = iModeMoveMap
			self.bRegion = False
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "AreaExporterScreen":
			bDeleteOverlay = False
			self.iPlayerAddMode = iModeAreaExporter1
			self.refreshSideMenu()
			self.showAreaExportOverlay()

		elif inputClass.getFunctionName() == "ClearChanges":
			bDeleteOverlay = False
			if self.iPlayerAddMode == iModeFlip:
				if CvEventInterface.getEventManager().bAlt:
					self.dFlipZoneEdits = {}
				elif self.m_iCurrentPlayer in self.dFlipZoneEdits.keys():
					del self.dFlipZoneEdits[self.m_iCurrentPlayer]
			elif self.iPlayerAddMode == iModeCore:
				if CvEventInterface.getEventManager().bAlt:
					for iPlayer in players.major():
						Areas.updateCore(iPlayer)
				else:
					Areas.updateCore(self.m_iCurrentPlayer)
			elif self.iPlayerAddMode == iModeSettlerValue:
				if CvEventInterface.getEventManager().bAlt:
					for iPlayer in players.major():
						SettlerMaps.updateMap(iPlayer)
				else:
					SettlerMaps.updateMap(self.m_iCurrentPlayer)
			elif self.iPlayerAddMode == iModeWarMap:
				if CvEventInterface.getEventManager().bAlt:
					for iPlayer in players.major():
						WarMaps.updateMap(iPlayer)
				else:
					WarMaps.updateMap(self.m_iCurrentPlayer)
			elif self.iPlayerAddMode == iModeReligionMap:
				if CvEventInterface.getEventManager().bAlt:
					for iReligion in range(iNumReligions):
						RegionMap.updateReligionSpread(iReligion)
				else:
					RegionMap.updateReligionSpread(self.m_iCurrentReligion)
			elif self.iPlayerAddMode == iModeRegionMap:
				RegionMap.updateRegionMap()
			elif self.iPlayerAddMode in lAreaExportModes:
				self.TempInfo = []
				if self.iPlayerAddMode == iModeAreaExporter3:
					self.iPlayerAddMode = iModeAreaExporter2
				self.showAreaExportOverlay()
			self.updateOverlay()

		elif inputClass.getFunctionName() == "Export":
			bDeleteOverlay = False
			if self.iPlayerAddMode == iModeFlip:
				met.exportFlip(self.m_iCurrentPlayer, self.getFlipZone(self.m_iCurrentPlayer))
			elif self.iPlayerAddMode == iModeCore:
				met.exportCore(self.m_iCurrentPlayer)
				self.showStabilityOverlay()
			elif self.iPlayerAddMode == iModeSettlerValue:
				met.exportSettlerMap(self.m_iCurrentPlayer)
				self.showStabilityOverlay()
			elif self.iPlayerAddMode == iModeWarMap:
				met.exportWarMap(self.m_iCurrentPlayer)
				self.showWarOverlay()
			elif self.iPlayerAddMode == iModeRegionMap:
				met.exportRegionMap()
				self.showRegionOverlay()
			elif self.iPlayerAddMode in lAreaExportModes:
				met.exportAreaExport(self.TempInfo, self.bWaterException, self.bPeaksException)

		elif inputClass.getFunctionName() == "PresetValue":
			bDeleteOverlay = False
			if self.iPlayerAddMode == iModeReligionMap:
				self.m_iReligionMapValue = screen.getPullDownData("PresetValue", screen.getSelectedPullDownID("PresetValue"))
			elif self.iPlayerAddMode == iModeWarMap:
				iWarValue = screen.getPullDownData("PresetValue", screen.getSelectedPullDownID("PresetValue"))
			else:
				iSetValue = screen.getPullDownData("PresetValue", screen.getSelectedPullDownID("PresetValue"))

		elif inputClass.getFunctionName() == "WBSelectClass":
			self.iSelectClass = screen.getPullDownData("WBSelectClass", screen.getSelectedPullDownID("WBSelectClass"))
			if self.iPlayerAddMode != iModeFeatures:
				self.iSelection = -1
				self.refreshSideMenu()

		elif inputClass.getFunctionName() == "WBSelectItem":
			self.iSelection = inputClass.getData2()
			self.refreshSelection()

		elif inputClass.getFunctionName() == "RevealMode":
			self.iPlayerAddMode = lRevealModes[screen.getPullDownData("RevealMode", screen.getSelectedPullDownID("RevealMode"))]
			self.refreshReveal()

		elif inputClass.getFunctionName() == "BrushWidth":
			bDeleteOverlay = False
			self.iBrushWidth = screen.getPullDownData("BrushWidth", screen.getSelectedPullDownID("BrushWidth"))

		elif inputClass.getFunctionName() == "BrushHeight":
			bDeleteOverlay = False
			self.iBrushHeight = screen.getPullDownData("BrushHeight", screen.getSelectedPullDownID("BrushHeight"))

		elif inputClass.getFunctionName() == "HideInactive":
			bHideInactive = not bHideInactive
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "PythonEffectButton":
			bPython = not bPython
			self.setCurrentModeCheckbox()

		elif inputClass.getFunctionName() == "SensibilityCheck":
			bDeleteOverlay = False
			self.bSensibility = not self.bSensibility
			self.setCurrentModeCheckbox()

		elif inputClass.getFunctionName() == "RegionButton":
			bDeleteOverlay = False
			self.bRegion = not self.bRegion
			self.setCurrentModeCheckbox()

		elif inputClass.getFunctionName() == "CancelMoveMap":
			if self.iPlayerAddMode == iModeMoveMap2:
				self.iPlayerAddMode = iModeMoveMap
			elif self.iPlayerAddMode == iModeAreaExporter3:
				self.iPlayerAddMode = iModeAreaExporter2
				del self.TempInfo[-1]
				bDeleteOverlay = False
				self.showAreaExportOverlay()
			self.refreshSideMenu()

		elif inputClass.getFunctionName() == "FlipAIButton":
			bDeleteOverlay = False
			self.bFlipAI = not self.bFlipAI
			self.setCurrentModeCheckbox()

		elif inputClass.getFunctionName() == "VictoryRectangleButton":
			bDeleteOverlay = False
			self.bVictoryRectangle = not self.bVictoryRectangle
			self.setCurrentModeCheckbox()
			self.showVictoryOverlay()

		elif inputClass.getFunctionName() == "AreaExportWater":
			bDeleteOverlay = False
			self.bWaterException = not self.bWaterException
			self.setCurrentModeCheckbox()
			self.showAreaExportOverlay()

		elif inputClass.getFunctionName() == "AreaExportPeak":
			bDeleteOverlay = False
			self.bPeaksException = not self.bPeaksException
			self.setCurrentModeCheckbox()
			self.showAreaExportOverlay()

		elif inputClass.getFunctionName() == "ToolHelp":
			bDeleteOverlay = False
			self.showToolHelp()

		elif inputClass.getFunctionName() == "AllRegionsButton":
			bDeleteOverlay = False
			if not self.dRegionColors:
				self.determineRegionColors()
			self.bAllRegions = not self.bAllRegions
			self.refreshSideMenu()
			self.showRegionOverlay()

		elif inputClass.getFunctionName() == "CheckRegionsButton":
			bDeleteOverlay = False
			self.checkRegionTiles()

		elif inputClass.getFunctionName() == "MoveMapReset":
			self.iMoveMapReset = screen.getPullDownData("MoveMapReset", screen.getSelectedPullDownID("MoveMapReset"))

		if bDeleteOverlay and inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
			removeStabilityOverlay()

		return 1