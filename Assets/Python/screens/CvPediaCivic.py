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

class CvPediaCivic:
	"Civilopedia Screen for Civics"

	def __init__(self, main):
		self.iCivic = -1
		self.top = main
		
		self.X_MAIN_PANE = self.top.X_PEDIA_PAGE +20   #470
		self.Y_MAIN_PANE = self.top.Y_PEDIA_PAGE +10   #65
		self.W_MAIN_PANE = 290
		self.H_MAIN_PANE = 150

		self.X_ICON = self.X_MAIN_PANE + 10
		self.Y_ICON = self.Y_MAIN_PANE + 17
		self.W_ICON = 125
		self.H_ICON = 125
		self.ICON_SIZE = 64

		self.X_STATS_PANE = self.X_ICON + self.W_ICON 
		self.Y_STATS_PANE = 105
		self.W_STATS_PANE = 250
		self.H_STATS_PANE = 200

		self.X_REQUIRES = self.X_MAIN_PANE + self.W_MAIN_PANE + 10
		self.W_REQUIRES = 1000 - self.X_REQUIRES
		self.H_REQUIRES = 110
		self.Y_REQUIRES = self.Y_MAIN_PANE + self.H_MAIN_PANE - self.H_REQUIRES

		self.X_SPECIAL = self.X_MAIN_PANE
		self.Y_SPECIAL = self.Y_MAIN_PANE + self.H_MAIN_PANE 
		self.W_SPECIAL = 1000 - self.X_SPECIAL
		self.H_SPECIAL = 160

		self.X_TEXT = self.X_MAIN_PANE
		self.Y_TEXT = self.Y_SPECIAL + self.H_SPECIAL +10 
		self.W_TEXT = 1000 - self.X_TEXT
		self.H_TEXT = 700 - self.Y_TEXT
		
	# Screen construction function
	def interfaceScreen(self, iCivic):	
			
		self.iCivic = iCivic
	
		self.top.deleteAllWidgets()						
							
		screen = self.top.getScreen()
		
		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()
		# Header...
		szHeader = u"<font=4b>" + gc.getCivicInfo(self.iCivic).getDescription().upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_CIVIC or bNotActive:
			if self.top.iLastScreen != CvScreenEnums.PEDIA_MAIN:
				self.placeLinks()		
			self.top.iLastScreen = CvScreenEnums.PEDIA_CIVIC

			
		# Icon
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False,
		    self.X_MAIN_PANE, self.Y_MAIN_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false,
		    self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getCivicInfo(self.iCivic).getButton(),
		    self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getCivicInfo(self.iCivic).getButton(), self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, WidgetTypes.WIDGET_GENERAL, self.iCivic, -1 )
		
		self.placeStats()
		self.placeSpecial()
		self.placeRequires()
		self.placeText()
		
	def placeStats(self):
							
		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()
		screen.addListBoxGFC(panelName, "",
		    self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)

		# Civic Category
		iCivicOptionType = gc.getCivicInfo(self.iCivic).getCivicOptionType()
		if (iCivicOptionType != -1):
			screen.appendListBoxString(panelName, u"<font=3>" + gc.getCivicOptionInfo(iCivicOptionType).getDescription().upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
#			screen.setText(self.top.getNextWidgetName(), "Background", gc.getCivicOptionInfo(iCivicOptionType).getDescription().upper(), CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_PANE, self.Y_STATS_PANE-35, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Upkeep
		pUpkeepInfo = gc.getUpkeepInfo(gc.getCivicInfo(self.iCivic).getUpkeep())
		if (pUpkeepInfo):
			screen.appendListBoxString(panelName, u"<font=3>" + pUpkeepInfo.getDescription().upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
#			screen.setText(self.top.getNextWidgetName(), "Background", pUpkeepInfo.getDescription().upper(), CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_PANE, self.Y_STATS_PANE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
	def placeRequires(self):
		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true,
				 self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.enableSelect(panelName, False)
		screen.attachLabel(panelName, "", "  ")
		
		iTech = gc.getCivicInfo(self.iCivic).getTechPrereq()
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
		
		szSpecialText = CyGameTextMgr().parseCivicInfo(self.iCivic, True, False, True)
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL+5, self.Y_SPECIAL+5, self.W_SPECIAL-10, self.H_SPECIAL-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
		
	def placeText(self):
		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
				 self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50 )
 
		szText = gc.getCivicInfo(self.iCivic).getCivilopedia()
		screen.attachMultilineText( panelName, "Text", szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeLinks(self):

		self.top.placeLinks()
		self.top.placeCivics()
			
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		return 0


