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

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaCivilization:
	"Civilopedia Screen for Civilizations"

	def __init__(self, main):
		self.iCivilization = -1
		self.top = main
		
		self.X_MAIN_PANE = self.top.X_PEDIA_PAGE + 20
		self.Y_MAIN_PANE = self.top.Y_PEDIA_PAGE + 10
		self.W_MAIN_PANE = 160 #200 #Rhye

		self.X_ICON = self.X_MAIN_PANE + 5 # + 25 #Rhye
		self.W_ICON = 150
		self.H_ICON = 150
		self.ICON_SIZE = 128 #64 #Rhye

		self.X_TECH = self.X_MAIN_PANE + self.W_MAIN_PANE + 10
		self.Y_TECH = 65
		self.W_TECH = 1000 - self.X_TECH
		self.H_TECH = 110

		self.X_UNIT = self.X_TECH
		self.Y_UNIT = self.Y_TECH + self.H_TECH
		self.W_UNIT = 200
		self.H_UNIT = 110

		self.X_LEADER = self.X_TECH 
		self.Y_LEADER = self.Y_UNIT + self.H_UNIT
		self.W_LEADER = 1000 - self.X_LEADER
		self.H_LEADER = 250 #110 #Rhye

		self.X_TEXT = self.X_MAIN_PANE
		self.Y_TEXT = self.Y_LEADER + self.H_LEADER
		self.W_TEXT = 1000 - self.X_TEXT
		self.H_TEXT = 700 - self.Y_TEXT

		self.H_MAIN_PANE = (self.Y_LEADER + self.H_LEADER) - self.Y_MAIN_PANE
		self.Y_ICON = self.Y_MAIN_PANE + (self.H_MAIN_PANE - self.H_ICON)/2
		
	# Screen construction function
	def interfaceScreen(self, iCivilization):	
			
		self.iCivilization = iCivilization
	
		self.top.deleteAllWidgets()						
							
		screen = self.top.getScreen()
		
		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()

		# Header...
		szHeader = u"<font=4b>" + gc.getCivilizationInfo(self.iCivilization).getDescription().upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_CIVILIZATION or bNotActive:	
			if self.top.iLastScreen != CvScreenEnums.PEDIA_MAIN:
				self.placeLinks()	
			self.top.iLastScreen = CvScreenEnums.PEDIA_CIVILIZATION
			
		# Icon
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False,
		    self.X_MAIN_PANE, self.Y_MAIN_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false,
		    self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), ArtFileMgr.getCivilizationArtInfo(gc.getCivilizationInfo(self.iCivilization).getArtDefineTag()).getButton(),
		    self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		self.placeTech()
		self.placeUnit()
		self.placeLeader()
		self.placeText()

		return

	def placeTech(self):
		
		screen = self.top.getScreen()
		
		#Rhye - comment
##		panelName = self.top.getNextWidgetName()
##		screen.addPanel( panelName, localText.getText("TXT_KEY_FREE_TECHS", ()), "", false, true,
##				 self.X_TECH, self.Y_TECH, self.W_TECH, self.H_TECH, PanelStyles.PANEL_STYLE_BLUE50 )
##		screen.attachLabel(panelName, "", "  ")
##		for iTech in range(gc.getNumTechInfos()):
##			if (gc.getCivilizationInfo(self.iCivilization).isCivilizationFreeTechs(iTech)):
##				screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )

		#Rhye - start
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
				 self.X_TECH, self.Y_TECH - 4, self.W_LEADER, self.Y_TEXT - self.Y_TECH + 4, PanelStyles.PANEL_STYLE_BLUE50 ) 
		szText = CyGameTextMgr().parseCivInfos(self.iCivilization, True)
		screen.attachMultilineText( panelName, "", szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		#Rhye - end


			
	def placeUnit(self):
		
		screen = self.top.getScreen()
		#Rhye - comment
##		panelName = self.top.getNextWidgetName()
##		screen.addPanel( panelName, localText.getText("TXT_KEY_FREE_UNITS", ()), "", false, true,
##				 self.X_UNIT, self.Y_UNIT, self.W_UNIT, self.H_UNIT, PanelStyles.PANEL_STYLE_BLUE50 )
##		screen.attachLabel(panelName, "", "  ")
##					
##		for iUnit in range(gc.getNumUnitClassInfos()):
##			iUniqueUnit = gc.getCivilizationInfo(self.iCivilization).getCivilizationUnits(iUnit);
##			iDefaultUnit = gc.getUnitClassInfo(iUnit).getDefaultUnitIndex();
##			if (iDefaultUnit > -1 and iUniqueUnit > -1 and iDefaultUnit != iUniqueUnit):
##				screen.attachImageButton( panelName, "", gc.getUnitInfo(iUniqueUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUniqueUnit, 1, False )
##		
	def placeLeader(self):
		
		screen = self.top.getScreen()
		#Rhye - comment
##		panelName = self.top.getNextWidgetName()
##		screen.addPanel( panelName, localText.getText("TXT_KEY_CONCEPT_LEADERS", ()), "", false, true,
##				 self.X_LEADER, self.Y_LEADER, self.W_LEADER, self.H_LEADER, PanelStyles.PANEL_STYLE_BLUE50 )
##		screen.attachLabel(panelName, "", "  ")
##
##		for iLeader in range(gc.getNumLeaderHeadInfos()):
##			civ = gc.getCivilizationInfo(self.iCivilization)
##			if civ.isLeaders(iLeader):
##				screen.attachImageButton( panelName, "", gc.getLeaderHeadInfo(iLeader).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeader, 1, False )
##		
	def placeText(self):
		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
				 self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50 )
 
		szText = gc.getCivilizationInfo(self.iCivilization).getCivilopedia()
		screen.attachMultilineText( panelName, "Text", szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
													
	def placeLinks(self):

		self.top.placeLinks()
		self.top.placeCivs()
			

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		return 0


