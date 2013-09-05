#-------------------------------------------------------------------------------
# Name:        CvDotMapOverlayScreen.py
# Purpose:     Custom Screen for the dot map of the Strategy Overlay
#
# Author:      Del69, EmperorFool
#
# Created:     09/01/2009
#-------------------------------------------------------------------------------

from CvPythonExtensions import *
import BugUtil
import CvStrategyOverlay
import CvUtil
import sys

X, Y = 0, 1    # used in point tuples instead of creating a new class

gc = CyGlobalContext()
g_DotMap = None

class CvDotMapOverlayScreen:
	"""
	Screen for the dot map of the strategy overlay.
	"""
	def __init__(self, screenID):
		self.screenID = screenID
		self.SCREEN_NAME = "DotMapOverlayScreen"
		#---------------------------------------------------------------------------
		# Panel IDS
		#---------------------------------------------------------------------------
		self.PANEL_ID = "DotMapColorPanel"
		#---------------------------------------------------------------------------
		# Color Panel Coordinates
		#---------------------------------------------------------------------------
		self.PANEL_X = 10
		self.PANEL_Y = 110
		self.PANEL_MARGIN = 12
		self.PANEL_EXTRA_W = 1
		self.PANEL_EXTRA_H = 5
		#---------------------------------------------------------------------------
		# Color Panel Widgets
		#---------------------------------------------------------------------------
		self.COLOR_WIDGET_W = 22
		self.COLOR_WIDGET_H = 25
		self.COLOR_WIDGET_ACTUAL_H = 20
		self.COLOR_WIDGET_PREFIX = "DotMapColorWidget"
		self.COLOR_WIDGET_IDS = []
		#-------------------------------------------------------------------------------
		# Constants
		#-------------------------------------------------------------------------------
		self.HIGHLIGHT_CROSS_LAYER = 8
		self.FIRST_CROSS_LAYER = 9
		self.PLOT_LAYER = PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_NUMPAD_HELP
		self.DOT_STYLE = PlotStyles.PLOT_STYLE_DOT_TARGET
		self.NO_DOT_STYLE = PlotStyles.PLOT_STYLE_NONE
		self.BFC_OFFSETS = []
		for x in range(-2, 3):
			for y in range(-2, 3):
				if abs(x) != 2 or abs(y) != 2:
					self.BFC_OFFSETS.append((x, y))
		#---------------------------------------------------------------------------
		# State variables
		#---------------------------------------------------------------------------
		self.currentColor = 0
		self.bLeftMouseDown = False
		self.bRightMouseDown = False
		self.currentLayer = self.FIRST_CROSS_LAYER
		self.currentPoint = None
	#-------------------------------------------------------------------------------
	# Initialization Functions
	#-------------------------------------------------------------------------------
	def initVars(self):
		"""
		Initializes the variables for the screen.
		"""
		global g_DotMap
		g_DotMap = CvStrategyOverlay.getDotMap()
		for index in range(len(CvStrategyOverlay.COLOR_KEYS)):
			self.COLOR_WIDGET_IDS.append(self.COLOR_WIDGET_PREFIX + str(index))

	def isOpen(self):
		"""
		Returns True if the screen is open.
		"""
		return self.getScreen().isActive()
	#-------------------------------------------------------------------------------
	# Required civ4 functions
	#-------------------------------------------------------------------------------
	def getScreen(self):
		"""
		Returns the CyGInterfaceScreen object for this screen.
		"""
		return CyGInterfaceScreen(self.SCREEN_NAME, self.screenID)

	def hideScreen(self):
		"""
		Hides the screen.
		"""
		g_DotMap.unhighlightCity()
		CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_SELECTION)
		screen = self.getScreen()
		screen.hideScreen()

	def update(self, fDelta):
		"""
		Called each update cycle, checks for mouse button clicks when screen is up.
		"""
		if CyInterface().isLeftMouseDown():
			if not self.bLeftMouseDown:
				self.onLeftMouseDown()
			self.bLeftMouseDown = True
		else:
			self.bLeftMouseDown = False
		if CyInterface().isRightMouseDown():
			if not self.bRightMouseDown:
				self.onRightMouseDown()
			self.bRightMouseDown = True
		else:
			self.bRightMouseDown = False

	def handleInput(self, inputClass):
		"""
		Handles widget input.
		"""
		BugUtil.debugInput(inputClass)
		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == self.COLOR_WIDGET_PREFIX:
			self.onColorButton(inputClass.getID())
			return 1
		return 0

	def interfaceScreen(self):
		"""
		Initializes and shows the screen.
		"""
		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setCloseOnEscape(False)
		screen.setAlwaysShown(True)
		screen.setForcedRedraw(True)
		screen.setDimensions(0, 0, screen.getXResolution(), screen.getYResolution())
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)
		self.initVars()
		self.createColorPanel()
		self.onMouseOverPlot()

	#-------------------------------------------------------------------------------
	#   Widget Adding/Updating Functions
	#-------------------------------------------------------------------------------
	def createColorPanel(self):
		"""
	    Creates the color selection panel.
		"""
		screen = self.getScreen()
		count = len(CvStrategyOverlay.COLOR_KEYS)
		width = CvStrategyOverlay.PALETTE_WIDTH
		self.ROWS = (count - 1) / width + 1
		if self.ROWS == 1:
			self.COLUMNS = count
			self.PANEL_W = self.COLOR_WIDGET_W * self.COLUMNS
		else:
			self.COLUMNS = width
			self.PANEL_W = self.COLOR_WIDGET_W * width
		self.PANEL_W += 2 * self.PANEL_MARGIN + self.PANEL_EXTRA_W
		self.PANEL_H = self.ROWS * self.COLOR_WIDGET_ACTUAL_H + 2 * self.PANEL_MARGIN + self.PANEL_EXTRA_H
		#self.PANEL_Y = screen.getYResolution() - self.PANEL_H - 20
		#if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW:
		#	self.PANEL_Y -= 164
		screen.addPanel(self.PANEL_ID, u"", u"", True, False, self.PANEL_X, self.PANEL_Y, self.PANEL_W, self.PANEL_H, PanelStyles.PANEL_STYLE_BLUELARGE)
		for index, color in enumerate(CvStrategyOverlay.COLOR_KEYS):
			row = index / width
			column = index % width
			x = self.PANEL_X + self.PANEL_MARGIN + column * self.COLOR_WIDGET_W
			y = self.PANEL_Y + self.PANEL_MARGIN + row * self.COLOR_WIDGET_ACTUAL_H
			szBar = self.COLOR_WIDGET_IDS[index]
			screen.addStackedBarGFC(szBar, x, y, self.COLOR_WIDGET_W, self.COLOR_WIDGET_H, 1, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setStackedBarColors(szBar, 0, gc.getInfoTypeForString(color))
			screen.setBarPercentage(szBar, 0, 100.0)

	def selectColor(self, index):
		"""
		Updates the selected color and layer given the button index.
		"""
		self.currentColor = gc.getInfoTypeForString(CvStrategyOverlay.COLOR_KEYS[index])  # index
		self.currentLayer = index + self.FIRST_CROSS_LAYER

	#-------------------------------------------------------------------------------
	#   Input handlers
	#-------------------------------------------------------------------------------
	def onColorButton(self, color):
		"""
		Called on Color Button input.
		"""
		g_DotMap.unhighlightCity()
		self.selectColor(color)
		g_DotMap.highlightCity(self.currentPoint, self.currentColor)
	
	def onLeftMouseDown(self):
		"""
		Called on left mouse click on the main ui.
		"""
		if self.currentPoint is not None:
			g_DotMap.unhighlightCity()
			grid = 6
			layer = self.FIRST_CROSS_LAYER + (self.currentPoint[X] % grid) * grid + (self.currentPoint[Y] % grid)
			g_DotMap.addCityAt(self.currentPoint, self.currentColor, layer)
			self.resetInterfaceMode()

	def onRightMouseDown(self):
		"""
		Called on right mouse click on the main ui.
		"""
		if self.currentPoint is not None:
			g_DotMap.unhighlightCity()
			g_DotMap.removeCityAt(self.currentPoint)
			self.resetInterfaceMode()

	def onMouseOverPlot(self, argsList=None):
		"""
		Called from CvOverlayScreenUtils when mousing over a plot when the screen is active.
		Updates the current plot and its x/y location.
		"""
		plot = CyInterface().getMouseOverPlot()
		x = plot.getX()
		y = plot.getY()
		self.currentPoint = (x, y)
		g_DotMap.highlightCity(self.currentPoint, self.currentColor)
		self.resetInterfaceMode()
	
	def resetInterfaceMode(self):
		if CyInterface().getInterfaceMode() != InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT:
			CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)
