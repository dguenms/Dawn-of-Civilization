## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Sevopedia
##   sevotastic.blogspot.com
##   sevotastic@yahoo.com
##


from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import string

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaSpecialist:
	"Civilopedia Screen for Specialists"

	def __init__(self, main):
		self.iSpecialist = -1
		self.top = main

		self.X_MAIN_PANEL = self.top.X_PEDIA_PAGE + 40
		self.Y_MAIN_PANEL = self.top.Y_PEDIA_PAGE + 25
		self.W_MAIN_PANEL = 250
		self.H_MAIN_PANEL = 250

		self.W_ICON = 150
		self.H_ICON = 150
		self.X_ICON = self.X_MAIN_PANEL + (self.W_MAIN_PANEL - self.W_ICON) / 2
		self.Y_ICON = self.Y_MAIN_PANEL + (self.H_MAIN_PANEL - self.H_ICON) / 2
		self.ICON_SIZE = 64

		self.X_SPECIAL = self.X_MAIN_PANEL + self.W_MAIN_PANEL + 10
		self.Y_SPECIAL = self.Y_MAIN_PANEL
		self.W_SPECIAL = 1024 - (self.X_MAIN_PANEL + self.W_MAIN_PANEL +10 ) - 30
		self.H_SPECIAL = self.H_MAIN_PANEL

		self.X_TEXT = self.X_MAIN_PANEL
		self.Y_TEXT = self.Y_MAIN_PANEL + self.H_MAIN_PANEL + 20
		self.W_TEXT = 1024 - self.X_MAIN_PANEL - 30
		self.H_TEXT = 330

	# Screen construction function
	def interfaceScreen(self, iSpecialist):	
			
		self.iSpecialist = iSpecialist
	
		self.top.deleteAllWidgets()						
							
		screen = self.top.getScreen()
		
		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()

		# Header...
		szHeader = u"<font=4b>" + gc.getSpecialistInfo(self.iSpecialist).getDescription().upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPECIALIST, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_SPECIALIST or bNotActive:
			if self.top.iLastScreen != CvScreenEnums.PEDIA_MAIN:
				self.placeLinks()	
			self.top.iLastScreen = CvScreenEnums.PEDIA_SPECIALIST
			
		# Icon
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False,
		    self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false,
		    self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getSpecialistInfo(self.iSpecialist).getButton(),
		    self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false,
#		    self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_BLUE50)
#		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getSpecialistInfo(self.iSpecialist).getButton(),
#		    self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		self.placeSpecial()
		self.placeText()
		
	def placeSpecial(self):
		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_YIELDS", ()), "", true, false,
                                 self.X_SPECIAL, self.Y_SPECIAL, self.W_SPECIAL, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )
		
		listName = self.top.getNextWidgetName()
		screen.attachListBoxGFC( panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY )
		screen.enableSelect(listName, False)
		
		szSpecialText = CyGameTextMgr().getSpecialistHelp(self.iSpecialist, True)
		splitText = string.split( szSpecialText, "\n" )
		for special in splitText:
			if len( special ) != 0:
				screen.appendListBoxString( listName, special, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		
	def placeText(self):
		
		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
                                 self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50 )
 
		szText = gc.getSpecialistInfo(self.iSpecialist).getCivilopedia()
		screen.attachMultilineText( panelName, "Text", szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
											
	def placeLinks(self):

		self.top.placeLinks()
		self.top.placeSpecialists()


	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		return 0


