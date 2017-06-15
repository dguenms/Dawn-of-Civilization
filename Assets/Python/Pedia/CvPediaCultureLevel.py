from CvPythonExtensions import *
import CvUtil
from Consts import *

gc = CyGlobalContext()

class CvPediaCultureLevel:

	def __init__(self, main):
		self.iCultureLevel = -1
		self.top = main
		
		self.X_INFO_PANE = self.top.X_PEDIA_PAGE
		self.Y_INFO_PANE = self.top.Y_PEDIA_PAGE
		self.W_INFO_PANE = self.top.R_PEDIA_PAGE - self.X_INFO_PANE
		self.H_INFO_PANE = 120
		
		self.X_INFO_TEXT = self.X_INFO_PANE + 10
		self.Y_INFO_TEXT = self.Y_INFO_PANE + 15
		self.W_INFO_TEXT = 180
		self.H_INFO_TEXT = self.H_INFO_PANE - 20
		
	def interfaceScreen(self, iCultureLevel):
		self.iCultureLevel = iCultureLevel
		
		self.placeInfo()
		self.placeEffects()
		self.placeBuildings()
		self.placeSpecialists()
		
	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		
		CultureLevelInfo = gc.getCultureLevelInfo(self.iCultureLevel)
		
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		
		screen.addListBoxGFC(panel, "", self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panel, False)
		screen.appendListBoxString(panel, u"<font=4b>" + CultureLevelInfo.getDescription() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeEffects(self):
		pass
		
	def placeBuildings(self):
		pass
		
	def placeSpecialists(self):
		pass