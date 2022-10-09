## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import time
import re
import CvScreensInterface

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvReplayScreen:
	"Replay Screen for end of game"

	def __init__(self, screenId):
		self.screenId = screenId
		self.REPLAY_SCREEN_NAME = "ReplayScreen"
		self.INTERFACE_ART_INFO = "TECH_BG"

		self.WIDGET_ID = "ReplayScreenWidget"
		self.EXIT_ID = "ReplayScreenExitWidget"
		self.BACKGROUND_ID = "ReplayScreenBackground"

		self.Z_BACKGROUND = -6.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.DZ = -0.2

		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Y_TITLE = 8
		self.BORDER_WIDTH = 4
		self.W_HELP_AREA = 200
		
		self.X_EXIT = 994
		self.Y_EXIT = 726
						
		self.X_PLAY = 50
		self.Y_PLAY = 730

		self.X_FORWARD = 200
		self.Y_FORWARD = 730
		
		self.X_SPEED = 520
		self.Y_SPEED = 745
		
		self.X_SLIDER = 475
		self.Y_SLIDER = 725
		self.W_SLIDER = 100
		self.H_SLIDER = 15
		self.NUM_SLIDER_STOPS = 5
		
		self.nWidgetCount = 0
		
		self.X_MAP = 50
		self.Y_MAP = 100
		self.W_MAP = 550
		self.H_MAP_MAX = 400
		
		self.X_TEXT = 625
		self.Y_TEXT = 100
		self.W_TEXT = 350
		self.H_TEXT = 580
		
		self.TIME_STEP = (1.0, 0.5, 0.25, 0.125, 0.0625)
				
		self.X_GRAPH = 50
		self.W_GRAPH = 550
		
		self.replayInfo = None
		self.bPlaying = False
		
		self.dColors = {}
		
	def setReplayInfo(self, replayInfo):
		self.replayInfo = replayInfo
		
	def getScreen(self):
		return CyGInterfaceScreen(self.REPLAY_SCREEN_NAME, self.screenId)

	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()	
		
	# Screen construction function
	def showScreen(self, bFromHallOfFame):
	
		# Create a new screen
		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.EXIT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + u"</font>"
		self.PLAY_TEXT = u"<font=4>" + localText.getText("TXT_KEY_REPLAY_SCREEN_PLAY", ()).upper() + u"</font>"
		self.FORWARD_TEXT = u"<font=4>" + localText.getText("TXT_KEY_REPLAY_SCREEN_NEXT", ()).upper() + u"</font>"
		self.STOP_TEXT = u"<font=4>" + localText.getText("TXT_KEY_REPLAY_SCREEN_STOP", ()).upper() + u"</font>"
		self.SPEED_TEXT = localText.getText("TXT_KEY_REPLAY_SCREEN_SPEED", ())
			
		self.bPlaying = False
		self.fLastUpdate = 0.
		self.iSpeed = 2
		self.iLastTurnShown = -1
		self.bFromHallOfFame = bFromHallOfFame
		self.bDone = False
		
		if not bFromHallOfFame:
			self.replayInfo = CyGame().getReplayInfo()
			if self.replayInfo.isNone():
				self.replayInfo = CyReplayInfo()
				self.replayInfo.createInfo(gc.getGame().getActivePlayer())
				
		self.iTurn = self.replayInfo.getInitialTurn()
					
		self.deleteAllWidgets()
	
		# Controls
		self.szForwardId = self.getNextWidgetName()
		self.szPlayId = self.getNextWidgetName()
		
		# Set the background widget and exit button
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.showWindowBackground(False)
		screen.setText(self.EXIT_ID, "", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Header...
		self.szHeader = self.getNextWidgetName()
		screen.setLabel(self.szHeader, "Background", u"<font=4b>" + localText.getText("TXT_KEY_REPLAY_SCREEN_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Minimap initialization
		self.H_MAP = (self.W_MAP * self.replayInfo.getMapHeight()) / self.replayInfo.getMapWidth() 
		if (self.H_MAP > self.H_MAP_MAX):
			self.W_MAP = (self.H_MAP_MAX * self.replayInfo.getMapWidth()) / self.replayInfo.getMapHeight()
			self.H_MAP = self.H_MAP_MAX
			
		screen.setMinimapMap(self.replayInfo, self.X_MAP, self.X_MAP + self.W_MAP, self.Y_MAP, self.Y_MAP + self.H_MAP, self.Z_CONTROLS)
		screen.updateMinimapSection(True, False)
		screen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_REPLAY)

		# add pane for text
		#mainPanelName = self.getNextWidgetName()
		#screen.addPanel(mainPanelName, "", "", True, True, self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_IN)
		self.szAreaId = self.getNextWidgetName()
		screen.addListBoxGFC(self.szAreaId, "", self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.szAreaId, False)
				
		self.Y_GRAPH = self.Y_MAP + self.H_MAP + 15
		self.H_GRAPH = 680 - self.Y_GRAPH
		self.szGraph = self.getNextWidgetName()
		screen.addGraphWidget(self.szGraph, "Background", ArtFileMgr.getInterfaceArtInfo("POPUPS_BACKGROUND_TRANSPARENT").getPath(), self.X_GRAPH, self.Y_GRAPH, self.Z_CONTROLS, self.W_GRAPH, self.H_GRAPH, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.initGraph()
		
		# Forward
		screen.setText(self.szForwardId, "Background", self.FORWARD_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.X_FORWARD, self.Y_FORWARD, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Play
		screen.setText(self.szPlayId, "Background", self.PLAY_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.X_PLAY, self.Y_PLAY, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, -1 )		


		# Speed Slider
		self.szSliderTextId = self.getNextWidgetName()
		screen.setLabel(self.szSliderTextId, "Background", self.SPEED_TEXT, CvUtil.FONT_CENTER_JUSTIFY, self.X_SPEED, self.Y_SPEED, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		self.szSliderId = self.getNextWidgetName()
		screen.addSlider(self.szSliderId, self.X_SLIDER, self.Y_SLIDER, self.W_SLIDER, self.H_SLIDER, self.iSpeed - 1, 0, self.NUM_SLIDER_STOPS-1, WidgetTypes.WIDGET_GENERAL, -1, -1, False);

		self.showEvents(self.iTurn, False)
															
		return
	
	def getCivColor(self, iCiv):
		return gc.getPlayerColorInfo(gc.getCivilizationInfo(iCiv).getDefaultPlayerColor()).getColorTypePrimary()
		
	def showEvents(self, iTurn, bSilent):
		self.iTurn = iTurn
		screen = self.getScreen()
				
		if (iTurn < self.replayInfo.getInitialTurn()):
			self.iTurn = self.replayInfo.getInitialTurn()
			self.iLastTurnShown = -1
			return
		elif iTurn > self.replayInfo.getFinalTurn():
			self.iTurn = self.replayInfo.getInitialTurn()
			self.iLastTurnShown = -1
			self.resetData()
			self.showEvents(self.iTurn, False)
			return
		
		szTurnDate = CyGameTextMgr().getDateStr(self.iTurn, false, self.replayInfo.getCalendar(), self.replayInfo.getStartYear(), self.replayInfo.getGameSpeed())
		screen.deleteWidget(self.szHeader)
		screen.setLabel(self.szHeader, "Background", u"<font=4b>" + szTurnDate + u"<font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		events = []
		bFound = False
		bDone = False
		i = 0
		while (i < self.replayInfo.getNumReplayMessages() and not bDone):
			if 	(self.replayInfo.getReplayMessageTurn(i) <= iTurn and self.replayInfo.getReplayMessageTurn(i) > self.iLastTurnShown):
				events.append(i)
				bFound = True
			else:
				if (bFound):
					bDone = True
			i += 1
	
		for iLoopEvent in events:

			szEventDate = CyGameTextMgr().getDateStr(self.replayInfo.getReplayMessageTurn(iLoopEvent), false, self.replayInfo.getCalendar(), self.replayInfo.getStartYear(), self.replayInfo.getGameSpeed())

			szText = self.replayInfo.getReplayMessageText(iLoopEvent)
			iX = self.replayInfo.getReplayMessagePlotX(iLoopEvent)
			iY = self.replayInfo.getReplayMessagePlotY(iLoopEvent)
			eMessageType = self.replayInfo.getReplayMessageType(iLoopEvent)
			eColor = self.replayInfo.getReplayMessageColor(iLoopEvent)
			
			if (szText != "" and not bSilent):			
				szTextNoColor = re.sub("<color=.*?>", "", szText)
				szText = re.sub("</color>", "", szTextNoColor)
						
				szText =  u"<font=2>" + szEventDate + u": " + szText + u"</font>"
				szText =localText.changeTextColor(szText, eColor)
				screen.prependListBoxString(self.szAreaId, szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
			
			if eMessageType == ReplayMessageTypes.REPLAY_MESSAGE_PLOT_OWNER_CHANGE:
				iPlayer = self.replayInfo.getReplayMessagePlayer(iLoopEvent)
				if iPlayer != -1:
					iColor = self.dColors.get(iPlayer, self.replayInfo.getColor(iPlayer))
					screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_REPLAY, iX, iY, iColor, 0.6)
				else:
					screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_REPLAY, iX, iY, gc.getInfoTypeForString("COLOR_CLEAR"), 0.6)
			elif eMessageType == ReplayMessageTypes.REPLAY_MESSAGE_CIV_ASSIGNED:
				iPlayer = self.replayInfo.getReplayMessagePlayer(iLoopEvent)
				iCiv = iX
				
				self.dColors[iPlayer] = self.getCivColor(iCiv)
			else:
				if (iX > -1 and iY > -1 and not bSilent):
					screen.minimapFlashPlot(iX, iY, gc.getInfoTypeForString("COLOR_WHITE"), 10)
		if (self.yMessage > self.H_TEXT):					
			screen.scrollableAreaScrollToBottom(self.szAreaId)
		
		# Power Graph
		iLoopTurn = self.iLastTurnShown
		while (iLoopTurn <= self.iTurn):
			iTotalScore = 0
			for iLoopPlayer in range(self.replayInfo.getNumPlayers()):
				if gc.getPlayer(iLoopPlayer).isMinorCiv(): continue # Leoreth
				iTotalScore += self.replayInfo.getPlayerScore(iLoopPlayer, iLoopTurn)
			if (iTotalScore > 0):
				iScore = iTotalScore
				for iLoopPlayer in range(self.replayInfo.getNumPlayers()):
					if gc.getPlayer(iLoopPlayer).isMinorCiv(): continue # Leoreth
					screen.addGraphData(self.szGraph, iLoopTurn, (1.0 * iScore) / iTotalScore, iLoopPlayer)
					iScore -= self.replayInfo.getPlayerScore(iLoopPlayer, iLoopTurn)
			iLoopTurn += 1
			
		self.iLastTurnShown = iTurn

	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName
		
	def deleteAllWidgets(self):
		screen = self.getScreen()
		i = self.nWidgetCount - 1
		while (i >= 0):
			self.nWidgetCount = i
			screen.deleteWidget(self.getNextWidgetName())
			i -= 1

		self.nWidgetCount = 0		
		self.yMessage = 5
		
	def resetMinimapColor(self):
		screen = self.getScreen()
		for iX in range(self.replayInfo.getMapWidth()):
			for iY in range(self.replayInfo.getMapHeight()):
				screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_REPLAY, iX, iY, gc.getInfoTypeForString("COLOR_CLEAR"), 0.6)

	def resetData(self):
		screen = self.getScreen()
		self.resetMinimapColor()
		for iPlayer in range(self.replayInfo.getNumPlayers()):
			screen.clearGraphData(self.szGraph, iPlayer)
		self.initGraph()			
		screen.clearListBoxGFC(self.szAreaId)
		
		
	def initGraph(self):
		screen = self.getScreen()
		for iPlayer in range(self.replayInfo.getNumPlayers()):
			screen.addGraphLayer(self.szGraph, iPlayer, self.replayInfo.getColor(iPlayer));

		screen.setGraphLabelX(self.szGraph, localText.getText("TXT_KEY_REPLAY_SCREEN_TURNS", ()));
		screen.setGraphLabelY(self.szGraph, localText.getText("TXT_KEY_REPLAY_SCREEN_SCORE", ()));
		screen.setGraphYDataRange(self.szGraph, 0.0, 1.0);
		
	def setPlaying(self, bPlaying):
		if bPlaying != self.bPlaying:
			self.bPlaying = bPlaying
			screen = self.getScreen()
			if (self.bPlaying):
				screen.hide(self.szForwardId)
				screen.modifyString(self.szPlayId, self.STOP_TEXT, 0)
				screen.show(self.szSliderId)
				screen.show(self.szSliderTextId)
			else:
				screen.show(self.szForwardId)
				screen.modifyString(self.szPlayId, self.PLAY_TEXT, 0)		
				screen.hide(self.szSliderId)
				screen.hide(self.szSliderTextId)
																				
	# handle the input for this screen...
	def handleInput (self, inputClass):
	
		szWidgetName = inputClass.getFunctionName() + str(inputClass.getID())

		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getFunctionName() == self.EXIT_ID):
				screen = self.getScreen()
				screen.hideScreen()

			elif (szWidgetName == self.szPlayId):
				self.setPlaying(not self.bPlaying)
				if self.bPlaying:
					if self.iTurn >= self.replayInfo.getFinalTurn():
						self.resetData()
						self.showEvents(self.replayInfo.getInitialTurn()-1, False)
					else:
						self.showEvents(self.iTurn + 1, False)
			elif (szWidgetName == self.szForwardId):
				if (not self.bPlaying):
					self.showEvents(self.iTurn + 1, False)
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_SLIDER_NEWSTOP):
			if (szWidgetName == self.szSliderId):
				screen = self.getScreen()
				self.iSpeed = inputClass.getData() + 1
									
		return 0

	def update(self, fDelta):
	
		screen = self.getScreen()

		screen.updateMinimap(fDelta)

		if self.bPlaying:
			if self.iTurn < self.replayInfo.getFinalTurn():
				self.fLastUpdate += max(fDelta, 0.02)
				iTurnJump = int(self.fLastUpdate / self.TIME_STEP[self.iSpeed - 1])
					
				if (iTurnJump > 0):
					iTurnJump = 1  # we used to allow showing multiple turns at once, but it didn't work very well
					self.fLastUpdate = 0.0
					self.showEvents(self.iTurn + iTurnJump, False)

			elif self.iTurn >= self.replayInfo.getFinalTurn():
				self.setPlaying(False)
				self.fLastUpdate = 0.0

