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

class CvPediaReligion:
	"Civilopedia Screen for Religions"

	def __init__(self, main):
		self.iReligion = -1
		self.top = main
		
		self.X_MAIN_PANE = self.top.X_PEDIA_PAGE + 20
		self.Y_MAIN_PANE = 55
		self.W_MAIN_PANE = 250
		self.H_MAIN_PANE = 260


		self.W_ICON = 150
		self.H_ICON = 150
		self.X_ICON = self.X_MAIN_PANE + (self.W_MAIN_PANE-self.W_ICON)/2
		self.Y_ICON = self.Y_MAIN_PANE + (self.H_MAIN_PANE-self.H_ICON)/2
		self.ICON_SIZE = 64
		
		self.X_REQUIRES = self.X_MAIN_PANE + self.W_MAIN_PANE + 10
		self.Y_REQUIRES = 55
		self.W_REQUIRES = 1024 - (self.X_REQUIRES) -24
		self.H_REQUIRES = 110

		self.X_SPECIAL = self.X_MAIN_PANE + self.W_MAIN_PANE + 10
		self.Y_SPECIAL = self.Y_REQUIRES + self.H_REQUIRES
		self.W_SPECIAL = 1024 - (self.X_MAIN_PANE + self.W_MAIN_PANE + 10) - 24
		self.H_SPECIAL = self.Y_MAIN_PANE + self.H_MAIN_PANE - self.Y_SPECIAL

		self.X_TEXT = self.X_MAIN_PANE
		self.Y_TEXT = self.Y_MAIN_PANE + self.H_MAIN_PANE + 20
		self.W_TEXT = 1024 - (self.X_MAIN_PANE) - 24
		self.H_TEXT = 705 - self.Y_TEXT
		
	# Screen construction function
	def interfaceScreen(self, iReligion):	
			
		self.iReligion = iReligion
	
		self.top.deleteAllWidgets()						
							
		screen = self.top.getScreen()
		
		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()
			self.placeLinks()

		# Header...
		szHeader = u"<font=4b>" + gc.getReligionInfo(self.iReligion).getDescription().upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_RELIGION, -1)

		if self.top.iLastScreen != CvScreenEnums.PEDIA_RELIGION or bNotActive:		
			if self.top.iLastScreen != CvScreenEnums.PEDIA_MAIN:
				self.placeLinks()
			self.top.iLastScreen = CvScreenEnums.PEDIA_RELIGION

		# Icon
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False,
		    self.X_MAIN_PANE, self.Y_MAIN_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false,
		    self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getReligionInfo(self.iReligion).getButton(),
		    self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		self.placeSpecial()
		self.placeRequires()
		self.placeText()

	def placeRequires(self):
		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true,
				 self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.attachLabel(panelName, "", "  ")
		
		iTech = gc.getReligionInfo(self.iReligion).getTechPrereq()
		if (iTech > -1):
			screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )
			
	def placeSpecial(self):
		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false,
				 self.X_SPECIAL, self.Y_SPECIAL, self.W_SPECIAL, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )
				
		listName = self.top.getNextWidgetName()
		screen.attachListBoxGFC( panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY )
		screen.enableSelect(listName, False)
		
		szSpecialText = CyGameTextMgr().parseReligionInfo(self.iReligion, True)
		splitText = string.split( szSpecialText, "\n" )
		for special in splitText:
			if len( special ) != 0:
				screen.appendListBoxString( listName, special, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
				
	def placeText(self):
		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
				 self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50 )
 
		szText = gc.getReligionInfo(self.iReligion).getCivilopedia()
		screen.attachMultilineText( panelName, "Text", szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeLinks(self):

		self.top.placeLinks()
		self.top.placeReligions()

		
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		return 0


