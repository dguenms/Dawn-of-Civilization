## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

import math #Rhye
from Consts import *
import CvUtil
from CvPythonExtensions import *
from RFCUtils import utils

ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()
gc = CyGlobalContext()

## HOF MOD
import Buffy
import BugCore
import GameSetUpCheck
BUFFYOpt = BugCore.game.BUFFY
## end HOF MOD

class CvDawnOfMan:
	"Dawn of man screen"
	def __init__(self, iScreenID):
		self.iScreenID = iScreenID
		
		self.X_SCREEN = 0
		self.Y_SCREEN = 0
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		
		self.X_MAIN_PANEL = 250
		self.Y_MAIN_PANEL = 190 #70
		self.W_MAIN_PANEL = 550
		self.H_MAIN_PANEL = 350 #500
		
		self.iMarginSpace = 15
		
		self.X_HEADER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
		self.Y_HEADER_PANEL = self.Y_MAIN_PANEL + self.iMarginSpace
		self.W_HEADER_PANEL = self.W_MAIN_PANEL - (self.iMarginSpace * 2)
		self.H_HEADER_PANEL = int(self.H_MAIN_PANEL * (2.0 / 5.0))
		
		self.X_LEADER_ICON = self.X_HEADER_PANEL + self.iMarginSpace
		self.Y_LEADER_ICON = self.Y_HEADER_PANEL + self.iMarginSpace
		self.H_LEADER_ICON = self.H_HEADER_PANEL - (15 * 2)#140
		self.W_LEADER_ICON = int(self.H_LEADER_ICON / 1.272727)#110
		
#		iWHeaderPanelRemainingAfterLeader = self.W_HEADER_PANEL - self.W_LEADER_ICON + (self.iMarginSpace * 3)
#		iXHeaderPanelRemainingAfterLeader = self.X_LEADER_ICON + self.W_LEADER_ICON + self.iMarginSpace
		self.X_LEADER_TITLE_TEXT = 505#iXHeaderPanelRemainingAfterLeader + (iWHeaderPanelRemainingAfterLeader / 2)
		self.Y_LEADER_TITLE_TEXT = self.Y_HEADER_PANEL + self.iMarginSpace + 6
		self.W_LEADER_TITLE_TEXT = self.W_HEADER_PANEL / 3 + 10
		self.H_LEADER_TITLE_TEXT = self.H_HEADER_PANEL / 2
		
		self.X_FANCY_ICON1 = self.X_HEADER_PANEL + 170
		self.X_FANCY_ICON2 = self.X_HEADER_PANEL + 430
		self.Y_FANCY_ICON = self.Y_LEADER_TITLE_TEXT - 6
		self.WH_FANCY_ICON = 64
		
		self.X_STATS_TEXT = self.X_FANCY_ICON1# + self.W_LEADER_ICON + (self.iMarginSpace * 2) + 5
		self.Y_STATS_TEXT = self.Y_LEADER_TITLE_TEXT + 75
		self.W_STATS_TEXT = int(self.W_HEADER_PANEL * (5.25 / 7.0))
		self.H_STATS_TEXT =  int(self.H_HEADER_PANEL * (2.25 / 5.0))
		
		self.X_TEXT_PANEL = self.X_HEADER_PANEL
		self.Y_TEXT_PANEL = self.Y_HEADER_PANEL + self.iMarginSpace #10 is the fudge factor  #self.Y_HEADER_PANEL + self.H_HEADER_PANEL + self.iMarginSpace - 10		self.W_TEXT_PANEL = self.W_HEADER_PANEL
		self.W_TEXT_PANEL = self.W_HEADER_PANEL
		self.H_TEXT_PANEL = self.H_MAIN_PANEL - (self.iMarginSpace * 3) + 10 #10 is the fudge factor
		self.iTEXT_PANEL_MARGIN = 35
		
		self.X_EXIT = 460
		self.Y_EXIT = self.Y_MAIN_PANEL + 290 #self.Y_MAIN_PANEL + 440 (240)
		self.W_EXIT = 120
		self.H_EXIT = 30
		
	def interfaceScreen(self):
		'Use a popup to display the opening text'
		if ( CyGame().isPitbossHost() ):
			return
		
		self.player = gc.getPlayer(gc.getGame().getActivePlayer())
		self.EXIT_TEXT = localText.getText("TXT_KEY_SCREEN_CONTINUE", ())
		
		# Create screen
		
		screen = CyGInterfaceScreen( "CvDawnOfMan", self.iScreenID )		
		screen.showScreen(PopupStates.POPUPSTATE_QUEUED, False)
		screen.showWindowBackground( False )
		screen.setDimensions(screen.centerX(self.X_SCREEN), screen.centerY(self.Y_SCREEN), self.W_SCREEN, self.H_SCREEN)
		screen.enableWorldSounds( false )
		
		# Create panels
		
		# Main
		szMainPanel = "DawnOfManMainPanel"
		screen.addPanel( szMainPanel, "", "", true, true,
			self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_MAIN )
##Rhye - begin		
##		# Top
##		szHeaderPanel = "DawnOfManHeaderPanel"
##		screen.addPanel( szHeaderPanel, "", "", true, false,
##			self.X_HEADER_PANEL, self.Y_HEADER_PANEL, self.W_HEADER_PANEL, self.H_HEADER_PANEL, PanelStyles.PANEL_STYLE_DAWNTOP )
##Rhye - end			
		# Bottom
		szTextPanel = "DawnOfManTextPanel"
		screen.addPanel( szTextPanel, "", "", true, true,
			self.X_TEXT_PANEL, self.Y_TEXT_PANEL, self.W_TEXT_PANEL, self.H_TEXT_PANEL, PanelStyles.PANEL_STYLE_DAWNBOTTOM )
		
		# Add contents
##Rhye - begin		
##		# Leaderhead graphic
##		szLeaderPanel = "DawnOfManLeaderPanel"
##		screen.addPanel( szLeaderPanel, "", "", true, false,
##			self.X_LEADER_ICON - 3, self.Y_LEADER_ICON - 5, self.W_LEADER_ICON + 6, self.H_LEADER_ICON + 8, PanelStyles.PANEL_STYLE_DAWNTOP )
##		screen.addLeaderheadGFC("LeaderHead", self.player.getLeaderType(), AttitudeTypes.ATTITUDE_PLEASED,
##			self.X_LEADER_ICON + 5, self.Y_LEADER_ICON + 5, self.W_LEADER_ICON - 10, self.H_LEADER_ICON - 10, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
##		# Info/"Stats" text
##		
##		szNameText = "<color=255,255,0,255>" + u"<font=3b>" + gc.getLeaderHeadInfo(self.player.getLeaderType()).getDescription().upper() + u"</font>" + "\n- " + self.player.getCivilizationDescription(0) + " -"
##		screen.addMultilineText( "NameText", szNameText, self.X_LEADER_TITLE_TEXT, self.Y_LEADER_TITLE_TEXT, self.W_LEADER_TITLE_TEXT, self.H_LEADER_TITLE_TEXT, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
##		
##		self.Text_BoxText = CyGameTextMgr().parseLeaderTraits(self.player.getLeaderType(), self.player.getCivilizationType(), True, False)
##		self.Text_BoxText += "\n" + CyGameTextMgr().parseCivInfos(self.player.getCivilizationType(), True)
##		
##		screen.addMultilineText( "HeaderText", self.Text_BoxText, self.X_STATS_TEXT, self.Y_STATS_TEXT, self.W_STATS_TEXT, self.H_STATS_TEXT, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
##		# Fancy icon things
##		screen.addDDSGFC( "IconLeft", gc.getMissionInfo(MissionTypes.MISSION_FORTIFY).getButton(), self.X_FANCY_ICON1 , self.Y_FANCY_ICON , self.WH_FANCY_ICON, self.WH_FANCY_ICON, WidgetTypes.WIDGET_GENERAL, -1, -1 )
##		screen.addDDSGFC( "IconRight", gc.getMissionInfo(MissionTypes.MISSION_FORTIFY).getButton(), self.X_FANCY_ICON2 , self.Y_FANCY_ICON , self.WH_FANCY_ICON, self.WH_FANCY_ICON, WidgetTypes.WIDGET_GENERAL, -1, -1 )

##Rhye - end		
		# Main Body text
		szDawnTitle = u"<font=3>" + localText.getText("TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE", ()).upper() + u"</font>"
		screen.setLabel("DawnTitle", "Background", szDawnTitle, CvUtil.FONT_CENTER_JUSTIFY,
				self.X_TEXT_PANEL + (self.W_TEXT_PANEL / 2), self.Y_TEXT_PANEL + 15, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )


##Rhye - begin	
		pActivePlayer = gc.getPlayer(CyGame().getActivePlayer())
		iActivePlayer = CyGame().getActivePlayer()
			
		if getTurnForYear(tBirth[iActivePlayer]) <= utils.getScenarioStartTurn():
			iYear = utils.getScenarioStartYear()
		else:
			iYear = tBirth[iActivePlayer]
			
		year = str(abs(iYear)) + ' '
		if iYear >= 0: year += CyTranslator().getText("TXT_KEY_AD", ())
		else: year += CyTranslator().getText("TXT_KEY_BC", ())
		
		#Leoreth: imported individual texts from Sword of Islam (edead)
		pActivePlayer = gc.getPlayer(CyGame().getActivePlayer())
		
		bodyString = utils.getDawnOfManText(iActivePlayer)

		screen.addStackedBarGFC("ProgressBar", 300, 400, 435, 40, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setStackedBarColors("ProgressBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_PLAYER_GREEN"))
		screen.setStackedBarColors("ProgressBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_RESEARCH_RATE"))
		screen.setStackedBarColors("ProgressBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
		screen.setStackedBarColors("ProgressBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
		self.iTurnsRemaining = -1

##Rhye - end		
		screen.addMultilineText( "BodyText", bodyString, self.X_TEXT_PANEL + self.iMarginSpace, self.Y_TEXT_PANEL + self.iMarginSpace + self.iTEXT_PANEL_MARGIN, self.W_TEXT_PANEL - (self.iMarginSpace * 2), self.H_TEXT_PANEL - (self.iMarginSpace * 2) - 75, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
		screen.setButtonGFC("Exit", self.EXIT_TEXT, "", self.X_EXIT, self.Y_EXIT, self.W_EXIT, self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.hide( "Exit" ) #Rhye
		
		pActivePlayer = gc.getPlayer(CyGame().getActivePlayer())
		pLeaderHeadInfo = gc.getLeaderHeadInfo(pActivePlayer.getLeaderType())
		screen.setSoundId(CyAudioGame().Play2DSoundWithId(pLeaderHeadInfo.getDiploPeaceMusicScriptIds(0)))
		
	def handleInput( self, inputClass ):
		return 0
	
	def update(self, fDelta):
##Rhye - begin
		iActivePlayer = CyGame().getActivePlayer()
		if tBirth[iActivePlayer] <= utils.getScenarioStartYear():
			screen = CyGInterfaceScreen( "CvLoadingScreen", self.iScreenID )
			screen.setBarPercentage("ProgressBar", InfoBarTypes.INFOBAR_STORED, 1)
			screen.setLabel("Text", "", CyTranslator().getText("TXT_KEY_AUTOPLAY_TURNS_REMAINING", (0,)), CvUtil.FONT_CENTER_JUSTIFY, 530, 445, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.show( "Exit" )  #Rhye
		else:
			iGameTurn = CyGame().getGameTurn()

			iNumAutoPlayTurns = getTurnForYear(tBirth[CyGame().getActiveTeam()])
			iNumTurnsRemaining = iNumAutoPlayTurns - iGameTurn
			
			#if (iNumTurnsRemaining != self.iTurnsRemaining):
			#	self.iTurnsRemaining = iNumTurnsRemaining
			screen = CyGInterfaceScreen( "CvLoadingScreen", self.iScreenID )

			exponent = 1 + iNumAutoPlayTurns/utils.getTurns(190)
			screen.setBarPercentage("ProgressBar", InfoBarTypes.INFOBAR_STORED, float(math.pow(iGameTurn-utils.getScenarioStartTurn(), exponent)) / float(math.pow(iNumAutoPlayTurns-utils.getScenarioStartTurn(), exponent)))
			screen.setLabel("Text", "", CyTranslator().getText("TXT_KEY_AUTOPLAY_TURNS_REMAINING", (max(0,iNumTurnsRemaining),)), CvUtil.FONT_CENTER_JUSTIFY, 530, 445, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			if (iNumTurnsRemaining <= 0):  #Rhye
				screen.show( "Exit" )  #Rhye
		
##Rhye - end
		return
	    
		
	def onClose(self):
		#CyInterface().DoSoundtrack("AS2D_R_F_C") #Rhye
		CyInterface().setSoundSelectionReady(true)		
		return 0
	
