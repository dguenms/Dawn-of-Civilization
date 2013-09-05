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
import random
import string

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaLeader:
	"Civilopedia Screen for Leaders"

	def __init__(self, main):
		self.iLeader = -1
		self.top = main

                #Rhye - start
		self.X_LEADERHEAD_PANE = self.top.X_PEDIA_PAGE + 20
		self.Y_LEADERHEAD_PANE = 55
		self.W_LEADERHEAD_PANE = 325
		self.H_LEADERHEAD_PANE = 390
                
		self.W_LEADERHEAD = 320
		self.H_LEADERHEAD = 380
		self.X_LEADERHEAD = self.X_LEADERHEAD_PANE + ((self.W_LEADERHEAD_PANE - self.W_LEADERHEAD) / 2)
		self.Y_LEADERHEAD = self.Y_LEADERHEAD_PANE + ((self.H_LEADERHEAD_PANE - self.H_LEADERHEAD) / 2) +3

		self.W_CIV = 64
		self.H_CIV = 64
		self.X_CIV = self.X_LEADERHEAD_PANE + self.W_LEADERHEAD_PANE + 10
		self.Y_CIV = self.Y_LEADERHEAD_PANE + 5

		self.X_CIVIC = self.X_LEADERHEAD_PANE + self.W_LEADERHEAD_PANE + 10
		self.Y_CIVIC = self.Y_LEADERHEAD_PANE
		self.W_CIVIC = 1000 - self.X_CIVIC
		self.H_CIVIC = 80

		self.X_HISTORY = self.X_LEADERHEAD_PANE
		self.Y_HISTORY = self.Y_LEADERHEAD_PANE + self.H_LEADERHEAD_PANE + 5
		self.W_HISTORY = 1000 - self.X_HISTORY
		self.H_HISTORY = 700 - self.Y_HISTORY

		self.X_TRAITS = self.X_LEADERHEAD_PANE + self.W_LEADERHEAD_PANE + 10
		self.Y_TRAITS = self.Y_CIVIC + self.H_CIVIC
		self.W_TRAITS = 1000 - self.X_TRAITS
		self.H_TRAITS = self.Y_HISTORY - self.Y_TRAITS
		#Rhye - end
                
	# Screen construction function
	def interfaceScreen(self, iLeader):
			
		self.iLeader = iLeader
	
		self.top.deleteAllWidgets()						
							
		screen = self.top.getScreen()
		
		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()

		# Header...
		szHeader = u"<font=4b>" + gc.getLeaderHeadInfo(self.iLeader).getDescription().upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_LEADER or bNotActive:	
			if self.top.iLastScreen != CvScreenEnums.PEDIA_MAIN:
				self.placeLinks()		
			self.top.iLastScreen = CvScreenEnums.PEDIA_LEADER
		
		# Leaderhead
		leaderPanelWidget = self.top.getNextWidgetName()
		screen.addPanel( leaderPanelWidget, "", "", true, true,
                    self.X_LEADERHEAD_PANE, self.Y_LEADERHEAD_PANE, self.W_LEADERHEAD_PANE, self.H_LEADERHEAD_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		self.leaderWidget = self.top.getNextWidgetName()
		screen.addLeaderheadGFC(self.leaderWidget, self.iLeader, AttitudeTypes.ATTITUDE_PLEASED,
                    self.X_LEADERHEAD, self.Y_LEADERHEAD, self.W_LEADERHEAD, self.H_LEADERHEAD, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		self.placeHistory()
		#self.placeCivic() #Rhye
		self.placeCiv()
		#self.placeTraits() #Rhye
													
	def placeCiv(self):
		screen = self.top.getScreen()

		for iCiv in range(gc.getNumCivilizationInfos()):
			civ = gc.getCivilizationInfo(iCiv)
			if civ.isLeaders(self.iLeader):
				screen.setImageButton(self.top.getNextWidgetName(), civ.getButton(), self.X_CIV, self.Y_CIV, self.W_CIV, self.H_CIV, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, 1)
													
	def placeTraits(self):
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_TRAITS", ()), "", true, false,
                                 self.X_TRAITS, self.Y_TRAITS, self.W_TRAITS, self.H_TRAITS, PanelStyles.PANEL_STYLE_BLUE50 )
				
		listName = self.top.getNextWidgetName()
		
		szSpecialText = CyGameTextMgr().parseLeaderTraits(self.iLeader, -1, False, True)
		screen.addMultilineText(listName, szSpecialText, self.X_TRAITS+5, self.Y_TRAITS+5, self.W_TRAITS-10, self.H_TRAITS-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
		
	def placeCivic(self):		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_FAV_CIVIC", ()), "", true, true,
                                 self.X_CIVIC, self.Y_CIVIC, self.W_CIVIC, self.H_CIVIC, PanelStyles.PANEL_STYLE_BLUE50 )
		
		listName = self.top.getNextWidgetName()
		screen.attachListBoxGFC( panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY )
		screen.enableSelect(listName, False)

		iCivic = gc.getLeaderHeadInfo(self.iLeader).getFavoriteCivic()
		if (-1 != iCivic):
			szCivicText = gc.getCivicInfo(iCivic).getDescription()
			screen.appendListBoxString( listName, szCivicText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

	def placeHistory(self):
		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
			self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50 )
		
		historyTextName = self.top.getNextWidgetName()
		CivilopediaText = gc.getLeaderHeadInfo(self.iLeader).getCivilopedia()
		CivilopediaText = u"<font=2>" + CivilopediaText + u"</font>"
		screen.attachMultilineText( panelName, historyTextName, CivilopediaText,
			WidgetTypes.WIDGET_GENERAL,-1,-1, CvUtil.FONT_LEFT_JUSTIFY ) 

			
	def placeLinks(self):
	
		self.top.placeLinks()
		self.top.placeLeaders()



	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getData() == int(InputTypes.KB_RETURN) or inputClass.getData() == int(InputTypes.KB_ESCAPE)):
			self.top.getScreen().hideScreen()
			return 1
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getFunctionName() == self.LEADER_WIDGET):
				if (inputClass.getFlags() & MouseFlags.MOUSE_LBUTTONUP):
					self.top.getScreen().performLeaderheadAction(self.LEADER_WIDGET, 0)
		return 0


