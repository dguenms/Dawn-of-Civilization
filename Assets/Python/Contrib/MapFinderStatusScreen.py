## MapFinderStatusScreen
##
## Displays the status for MapFinder while it's running.
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugUtil
import CvUtil
import MapFinder

MAPFINDER_STATUS_SCREEN = CvUtil.getNewScreenID()

gc = CyGlobalContext()
screen = None

def show():
	global screen
	if not screen:
		screen = MapFinderStatusScreen(MAPFINDER_STATUS_SCREEN)
	screen.interfaceScreen()

def hide():
	if screen:
		screen.hideScreen()

def update():
	if screen:
		screen.update()

def setStatus(status):
	if screen:
		screen.setStatus(status)

def resetStatus():
	if screen:
		screen.resetStatus()


class MapFinderStatusScreen:
	def __init__(self, id):
		self.id = id
		self.SCREEN_NAME = "MapFinderStatusScreen"
		
		self.MARGIN_X = 10
		self.MARGIN_Y = 10
		self.LINE_HEIGHT = 20
		
		self.MAIN_PANEL_ID = "MainPanel"
		self.MAIN_PANEL_X = 20
		self.MAIN_PANEL_Y = 100
		self.MAIN_PANEL_W = 200
		self.MAIN_PANEL_H = 5 * self.MARGIN_Y + 5 * self.LINE_HEIGHT
	
	def getScreen(self):
		"""
		Returns the CyGInterfaceScreen object for this screen.
		"""
		return CyGInterfaceScreen(self.SCREEN_NAME, self.id)

	def isOpen(self):
		return self.getScreen().isActive()
	
	def interfaceScreen(self):
		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setCloseOnEscape(False)
		screen.setAlwaysShown(True)
		screen.setForcedRedraw(True)
		self.draw(screen)
		screen.setDimensions(0, 0, screen.getXResolution(), screen.getYResolution())
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)

	def hideScreen(self):
		self.getScreen().hideScreen()
	
	
	def update(self):
		self.drawCounts(self.getScreen())
	
	def setStatus(self, status):
		self.drawStatus(self.getScreen(), status)
	
	def resetStatus(self):
		self.drawStatus(self.getScreen())
	
	
	def draw(self, screen):
		self.drawPanel(screen)
		self.drawCounts(screen)
		self.drawStatus(screen)
	
	def drawPanel(self, screen):
		screen.addPanel(self.MAIN_PANEL_ID, u"", u"", True, False, 
					self.MAIN_PANEL_X, self.MAIN_PANEL_Y, self.MAIN_PANEL_W, self.MAIN_PANEL_H, PanelStyles.PANEL_STYLE_HUD_HELP)
		
		x = self.MAIN_PANEL_X + self.MARGIN_X
		y = self.MAIN_PANEL_Y + self.MARGIN_Y
		z = -0.3
		screen.setLabel("TitleLabel", self.MAIN_PANEL_ID, BugUtil.getPlainText("TXT_KEY_MAPFINDER_SCREEN_TITLE"), CvUtil.FONT_CENTER_JUSTIFY,
					self.MAIN_PANEL_X + self.MAIN_PANEL_W / 2, y, z, FontTypes.SMALL_FONT, 
					WidgetTypes.WIDGET_GENERAL, -1, -1)
		y += self.LINE_HEIGHT + self.MARGIN_Y
		
		screen.setLabel("RegenLabel", self.MAIN_PANEL_ID, BugUtil.getPlainText("TXT_KEY_MAPFINDER_TOTAL_MAPS"), CvUtil.FONT_LEFT_JUSTIFY,
					x, y, z, FontTypes.SMALL_FONT, 
					WidgetTypes.WIDGET_GENERAL, -1, -1)
		y += self.LINE_HEIGHT
		screen.setLabel("SaveLabel", self.MAIN_PANEL_ID, BugUtil.getPlainText("TXT_KEY_MAPFINDER_TOTAL_SAVES"), CvUtil.FONT_LEFT_JUSTIFY,
					x, y, z, FontTypes.SMALL_FONT, 
					WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		y = self.MAIN_PANEL_Y + self.MAIN_PANEL_H - self.MARGIN_Y - self.LINE_HEIGHT
		screen.setLabel("StopMsgLabel", self.MAIN_PANEL_ID, BugUtil.getPlainText("TXT_KEY_MAPFINDER_STOP_SHORTCUT"), CvUtil.FONT_CENTER_JUSTIFY,
					self.MAIN_PANEL_X + self.MAIN_PANEL_W / 2, y, z, FontTypes.SMALL_FONT, 
					WidgetTypes.WIDGET_GENERAL, -1, -1)
	
	def drawCounts(self, screen):
		x = self.MAIN_PANEL_X + self.MAIN_PANEL_W - self.MARGIN_X
		y = self.MAIN_PANEL_Y + self.MARGIN_Y + self.LINE_HEIGHT + self.MARGIN_Y
		z = -0.3
		screen.setLabel("RegenCountLabel", self.MAIN_PANEL_ID, unicode(str(MapFinder.iRegenCount)), CvUtil.FONT_RIGHT_JUSTIFY,
					x, y, z, FontTypes.SMALL_FONT, 
					WidgetTypes.WIDGET_GENERAL, -1, -1)
		y += self.LINE_HEIGHT
		screen.setLabel("SaveCountLabel", self.MAIN_PANEL_ID, unicode(str(MapFinder.iSavedCount)), CvUtil.FONT_RIGHT_JUSTIFY,
					x, y, z, FontTypes.SMALL_FONT, 
					WidgetTypes.WIDGET_GENERAL, -1, -1)
	
	def drawStatus(self, screen, status=u""):
		x = self.MAIN_PANEL_X + self.MAIN_PANEL_W / 2
		y = self.MAIN_PANEL_Y + self.MAIN_PANEL_H - 2 * (self.MARGIN_Y + self.LINE_HEIGHT)
		z = -0.3
		screen.setLabel("StatusLabel", self.MAIN_PANEL_ID, status, CvUtil.FONT_CENTER_JUSTIFY,
					x, y, z, FontTypes.SMALL_FONT, 
					WidgetTypes.WIDGET_GENERAL, -1, -1)
