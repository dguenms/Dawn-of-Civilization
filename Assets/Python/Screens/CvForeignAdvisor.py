## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import math

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

# this class is shared by both the resource and technology foreign advisors
FOREIGN_BONUS_SCREEN = 0
FOREIGN_TECH_SCREEN = 1
FOREIGN_RELATIONS_SCREEN = 2
FOREIGN_ACTIVE_TRADE_SCREEN = 3
NUM_FOREIGN_SCREENS = 4

class CvForeignAdvisor:
	"Foreign Advisor Screen"

	def __init__(self):
		self.iScreen = -1
		self.nWidgetCount = 0
		self.nLineCount = 0
		self.WIDGET_ID = "ForeignAdvisorWidget"
		self.LINE_ID = "ForeignAdvisorLine"
		self.SCREEN_NAME = "ForeignAdvisor"
		self.DEBUG_DROPDOWN_ID =  "ForeignAdvisorDropdownWidget"
		self.EXIT_ID = "ForeignAdvisorExitWidget"
		self.BACKGROUND_ID = "ForeignAdvisorBackground"
		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Y_TITLE = 8
		self.X_EXIT = 994
		self.Y_EXIT = 726
		self.X_LEADER = 80
		self.Y_LEADER = 115
		self.H_LEADER = 64
		self.W_LEADER = 64
		self.X_LINK = 50
		self.DX_LINK = 220
		self.Y_LINK = 726
		
		self.X_LEGEND = 20
		self.Y_LEGEND = 530
		self.H_LEGEND = 180
		self.W_LEGEND = 160
		self.MARGIN_LEGEND = 10
		
		self.X_LEADER_CIRCLE_TOP = self.X_SCREEN + 10
		self.Y_LEADER_CIRCLE_TOP = 87
		
		self.RADIUS_LEADER_ARC = 480
		self.LINE_WIDTH = 6
		self.BUTTON_SIZE = 64
		
		
		self.iSelectedLeader = -1
		self.iActiveLeader = -1
		self.listSelectedLeaders = []
		self.iShiftKeyDown = 0
				
		self.iDefaultScreen = FOREIGN_RELATIONS_SCREEN
						
	def killScreen(self):
		if (self.iScreen >= 0):
			screen = self.getScreen()
			screen.hideScreen()
			self.iScreen = -1
		return

	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME + str(self.iScreen), CvScreenEnums.FOREIGN_ADVISOR)

	def interfaceScreen (self, iScreen):
	
		if (iScreen < 0):
			if (self.iScreen < 0):
				iScreen = self.iDefaultScreen
			else:
				iScreen = self.iScreen
		
		self.EXIT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + u"</font>"
		self.SCREEN_TITLE = u"<font=4b>" + localText.getText("TXT_KEY_FOREIGN_ADVISOR_TITLE", ()).upper() + u"</font>"

		if (self.iScreen != iScreen):	
			self.killScreen()
			self.iScreen = iScreen
		
		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen( PopupStates.POPUPSTATE_IMMEDIATE, False)
	
		self.iActiveLeader = CyGame().getActivePlayer()
		self.iSelectedLeader = self.iActiveLeader
		self.listSelectedLeaders = []
		#self.listSelectedLeaders.append(self.iSelectedLeader)

		# Set the background and exit button, and show the screen
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.addDrawControl(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "BottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.showWindowBackground(False)
		screen.setText(self.EXIT_ID, "", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		self.nWidgetCount = 0
		self.nLineCount = 0
		
		if (CyGame().isDebugMode()):
			self.szDropdownName = self.getWidgetName(self.DEBUG_DROPDOWN_ID)
			screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for j in range(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					#screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getName(), j, j, False ) #Rhye
					screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getCivilizationShortDescription(0), j, j, False ) #Rhye
					
		CyInterface().setDirty(InterfaceDirtyBits.Foreign_Screen_DIRTY_BIT, False)
		
		# Draw leader heads
		self.drawContents(True)
				
	# Drawing Leaderheads
	def drawContents(self, bInitial):
	
		if (self.iScreen < 0):
			return
						
		self.deleteAllWidgets()
		
		screen = self.getScreen()

		# Header...
		screen.setLabel(self.getNextWidgetName(), "", self.SCREEN_TITLE, CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
	
		if (self.iScreen == FOREIGN_RELATIONS_SCREEN):
			self.drawRelations(bInitial)
		elif (self.iScreen == FOREIGN_ACTIVE_TRADE_SCREEN):
			self.drawActive()
		else:
			self.drawPossibleDeals()
			
		# Link to other Foreign advisor screens
		xLink = self.X_LINK
		
		szRelationsId = self.getNextWidgetName()
		if (self.iScreen != FOREIGN_RELATIONS_SCREEN):
			screen.setText(szRelationsId, "", u"<font=4>" + localText.getText("TXT_KEY_FOREIGN_ADVISOR_RELATIONS", ()).upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_FOREIGN_ADVISOR, FOREIGN_RELATIONS_SCREEN, -1)
		else:
			screen.setText(szRelationsId, "", u"<font=4>" + localText.getColorText("TXT_KEY_FOREIGN_ADVISOR_RELATIONS", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_FOREIGN_ADVISOR, -1, -1)
		xLink += self.DX_LINK
		
		szBonusId = self.getNextWidgetName()
		if (self.iScreen != FOREIGN_BONUS_SCREEN):
			screen.setText(szBonusId, "", u"<font=4>" + localText.getText("TXT_KEY_FOREIGN_ADVISOR_RESOURCES", ()).upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_FOREIGN_ADVISOR, FOREIGN_BONUS_SCREEN, -1)
		else:
			screen.setText(szBonusId, "", u"<font=4>" + localText.getColorText("TXT_KEY_FOREIGN_ADVISOR_RESOURCES", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_FOREIGN_ADVISOR, -1, -1)
		xLink += self.DX_LINK
			
		szTechId = self.getNextWidgetName()
		if (self.iScreen != FOREIGN_TECH_SCREEN):
			screen.setText(szTechId, "", u"<font=4>" + localText.getText("TXT_KEY_FOREIGN_ADVISOR_TECHS", ()).upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_FOREIGN_ADVISOR, FOREIGN_TECH_SCREEN, -1)
		else:
			screen.setText(szTechId, "", u"<font=4>" + localText.getColorText("TXT_KEY_FOREIGN_ADVISOR_TECHS", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_FOREIGN_ADVISOR, -1, -1)
		xLink += self.DX_LINK
	
		szActiveId = self.getNextWidgetName()
		if (self.iScreen != FOREIGN_ACTIVE_TRADE_SCREEN):
			screen.setText(szActiveId, "", u"<font=4>" + localText.getText("TXT_KEY_FOREIGN_ADVISOR_ACTIVE", ()).upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_FOREIGN_ADVISOR, FOREIGN_ACTIVE_TRADE_SCREEN, -1)
		else:
			screen.setText(szActiveId, "", u"<font=4>" + localText.getColorText("TXT_KEY_FOREIGN_ADVISOR_ACTIVE", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_FOREIGN_ADVISOR, -1, -1)
		xLink += self.DX_LINK

	def drawActive(self):
		screen = self.getScreen()

		# Get the Players
		playerActive = gc.getPlayer(self.iActiveLeader)
					
		# Put everything inside a main panel, so we get vertical scrolling
		mainPanelName = self.getNextWidgetName()
		screen.addPanel(mainPanelName, "", "", True, True, 50, 100, self.W_SCREEN - 100, self.H_SCREEN - 200, PanelStyles.PANEL_STYLE_EMPTY)

		# loop through all players and sort them by number of active deals
		listPlayers = [(0,0)] * gc.getMAX_PLAYERS()
		nNumPLayers = 0
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			if (gc.getPlayer(iLoopPlayer).isAlive() and iLoopPlayer != self.iActiveLeader and not gc.getPlayer(iLoopPlayer).isBarbarian() and  not gc.getPlayer(iLoopPlayer).isMinorCiv()):
				if (gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isHasMet(gc.getPlayer(self.iActiveLeader).getTeam()) or gc.getGame().isDebugMode()):
					nDeals = 0				
					for i in range(gc.getGame().getIndexAfterLastDeal()):
						deal = gc.getGame().getDeal(i)
						if ((deal.getFirstPlayer() == iLoopPlayer and deal.getSecondPlayer() == self.iActiveLeader) or (deal.getSecondPlayer() == iLoopPlayer and deal.getFirstPlayer() == self.iActiveLeader)):
							nDeals += 1
					listPlayers[nNumPLayers] = (nDeals, iLoopPlayer)
					nNumPLayers += 1
		listPlayers.sort()
		listPlayers.reverse()

		# loop through all players and display leaderheads
		for j in range (nNumPLayers):
			iLoopPlayer = listPlayers[j][1]

			# Player panel
			playerPanelName = self.getNextWidgetName()
			screen.attachPanel(mainPanelName, playerPanelName, gc.getPlayer(iLoopPlayer).getName(), "", False, True, PanelStyles.PANEL_STYLE_MAIN)

			screen.attachLabel(playerPanelName, "", "   ")

			screen.attachImageButton(playerPanelName, "", gc.getLeaderHeadInfo(gc.getPlayer(iLoopPlayer).getLeaderType()).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, -1, False)
						
			innerPanelName = self.getNextWidgetName()
			screen.attachPanel(playerPanelName, innerPanelName, "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)

			dealPanelName = self.getNextWidgetName()
			screen.attachListBoxGFC(innerPanelName, dealPanelName, "", TableStyles.TABLE_STYLE_EMPTY)	
			screen.enableSelect(dealPanelName, False)

			iRow = 0
			for i in range(gc.getGame().getIndexAfterLastDeal()):
				deal = gc.getGame().getDeal(i)

				if (deal.getFirstPlayer() == iLoopPlayer and deal.getSecondPlayer() == self.iActiveLeader and not deal.isNone()) or (deal.getSecondPlayer() == iLoopPlayer and deal.getFirstPlayer() == self.iActiveLeader):
					screen.appendListBoxString(dealPanelName, CyGameTextMgr().getDealString(deal, iLoopPlayer), WidgetTypes.WIDGET_DEAL_KILL, deal.getID(), -1, CvUtil.FONT_LEFT_JUSTIFY)
					iRow += 1
																

	def drawPossibleDeals(self):
	
		screen = self.getScreen()

		# Get the Players
		playerActive = gc.getPlayer(self.iActiveLeader)
		playerSelected = gc.getPlayer(self.iSelectedLeader)
					
		# Put everything inside a main panel, so we get vertical scrolling
		mainPanelName = self.getNextWidgetName()
		screen.addPanel( mainPanelName, "", "", True, True, 50, 100, self.W_SCREEN - 100, self.H_SCREEN - 200, PanelStyles.PANEL_STYLE_MAIN )

		# Active player panel
		activePlayerPanelName = self.getNextWidgetName()
		szPlayerName = playerActive.getName()
		
		if (gc.getTeam(playerActive.getTeam()).isGoldTrading() or gc.getTeam(playerSelected.getTeam()).isGoldTrading()):
			if (self.iScreen == FOREIGN_BONUS_SCREEN):
				szPlayerName += u" : " + localText.getText("TXT_KEY_MISC_GOLD_PER_TURN", (playerActive.calculateGoldRate(), ))
			elif (self.iScreen == FOREIGN_TECH_SCREEN):
				szPlayerName += u" : " + localText.getText("TXT_KEY_MISC_GOLD", (playerActive.getGold(), ))
		screen.attachPanel(mainPanelName, activePlayerPanelName, szPlayerName, "", False, True, PanelStyles.PANEL_STYLE_EMPTY )
					
		screen.attachLabel(activePlayerPanelName, "", "                    ")
		screen.attachMultiListControlGFC(activePlayerPanelName, "Child" + activePlayerPanelName, "", 1, self.BUTTON_SIZE, self.BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD)

		if (self.iScreen == FOREIGN_BONUS_SCREEN):
			tradeData = TradeData()
			tradeData.ItemType = TradeableItems.TRADE_RESOURCES
			for iLoopBonus in range(gc.getNumBonusInfos()):
				tradeData.iData = iLoopBonus
				bTradeable = False
				if (self.iSelectedLeader == self.iActiveLeader):
					# loop through all players and display resources that are available to trade to at least one leader
					for iLoopPlayer in range(gc.getMAX_PLAYERS()):
						if (gc.getPlayer(iLoopPlayer).isAlive() and not gc.getPlayer(iLoopPlayer).isBarbarian() and not gc.getPlayer(iLoopPlayer).isMinorCiv() and gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isHasMet(gc.getPlayer(self.iActiveLeader).getTeam())):
							if (iLoopPlayer != self.iActiveLeader and gc.getPlayer(self.iActiveLeader).canTradeItem(iLoopPlayer, tradeData, False)):
								bTradeable = True
								iLoopPlayer = gc.getMAX_PLAYERS() # exit for loop
				else:
					# display resources that you can trade to the selected leader
					bTradeable = gc.getPlayer(self.iActiveLeader).canTradeItem(self.iSelectedLeader, tradeData, False)

				if bTradeable:
					for i in range(playerActive.getNumTradeableBonuses(iLoopBonus)):
						screen.appendMultiListButton("Child" + activePlayerPanelName, gc.getBonusInfo(iLoopBonus).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iLoopBonus, -1, False)

		elif (self.iScreen == FOREIGN_TECH_SCREEN):
			tradeData = TradeData()
			tradeData.ItemType = TradeableItems.TRADE_TECHNOLOGIES
			for iLoopTech in range(gc.getNumTechInfos()):
				bTradeable = False
				tradeData.iData = iLoopTech
				if (self.iSelectedLeader == self.iActiveLeader):
					# loop through all players and display techs that are available to trade to at least one leader
					for iLoopPlayer in range(gc.getMAX_PLAYERS()):
						if (gc.getPlayer(iLoopPlayer).isAlive() and not gc.getPlayer(iLoopPlayer).isBarbarian() and not gc.getPlayer(iLoopPlayer).isMinorCiv() and gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isHasMet(gc.getPlayer(self.iActiveLeader).getTeam())):
							if (iLoopPlayer != self.iActiveLeader and gc.getPlayer(self.iActiveLeader).canTradeItem(iLoopPlayer, tradeData, False)):
								bTradeable = True
								iLoopPlayer = gc.getMAX_PLAYERS() # exit for loop
								
				else:
					# display techs that you can trade to the selected leader
					bTradeable = gc.getPlayer(self.iActiveLeader).canTradeItem(self.iSelectedLeader, tradeData, False)
					
				if bTradeable:
					screen.appendMultiListButton("Child" + activePlayerPanelName, gc.getTechInfo(iLoopTech).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech, -1, False)

		# Add active player leaderhead
		screen.attachLabel(activePlayerPanelName, "", "   ")
		szName = self.getNextWidgetName()			
		screen.addCheckBoxGFCAt(activePlayerPanelName, szName, gc.getLeaderHeadInfo(gc.getPlayer(self.iActiveLeader).getLeaderType()).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 10, 0, self.W_LEADER, self.H_LEADER, WidgetTypes.WIDGET_LEADERHEAD, self.iActiveLeader, -1, ButtonStyles.BUTTON_STYLE_LABEL, False)
		if (self.iSelectedLeader == self.iActiveLeader):
			screen.setState(szName, True)
		else:
			screen.setState(szName, False)

		# Their leaderheads		
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			if (gc.getPlayer(iLoopPlayer).isAlive() and iLoopPlayer != self.iActiveLeader and (gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isHasMet(gc.getPlayer(self.iActiveLeader).getTeam()) or gc.getGame().isDebugMode()) and not gc.getPlayer(iLoopPlayer).isBarbarian() and not gc.getPlayer(iLoopPlayer).isMinorCiv()):

				currentPlayerPanelName = self.getNextWidgetName()
				szPlayerName = gc.getPlayer(iLoopPlayer).getName()
				if (gc.getTeam(playerActive.getTeam()).isGoldTrading() or gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isGoldTrading()):
					if (self.iScreen == FOREIGN_BONUS_SCREEN):
						szPlayerName += u" : " + localText.getText("TXT_KEY_FOREIGN_ADVISOR_GOLD_PER_TURN_FOR_TRADE", (gc.getPlayer(iLoopPlayer).AI_maxGoldPerTurnTrade(self.iActiveLeader), ))
					elif (self.iScreen == FOREIGN_TECH_SCREEN):
						szPlayerName += u" : " + localText.getText("TXT_KEY_FOREIGN_ADVISOR_GOLD_FOR_TRADE", (gc.getPlayer(iLoopPlayer).AI_maxGoldTrade(self.iActiveLeader), ))
				if (not playerActive.canTradeNetworkWith(iLoopPlayer) and self.iScreen == FOREIGN_BONUS_SCREEN):
					szPlayerName += u" : " + localText.getText("TXT_KEY_FOREIGN_ADVISOR_NOT_CONNECTED", ())
				elif (not gc.getTeam(playerActive.getTeam()).isTechTrading() and not gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isTechTrading()):
					szPlayerName += u" : " + localText.getText("TXT_KEY_FOREIGN_ADVISOR_NO_TECH_TRADING", ())
				screen.attachPanel(mainPanelName, currentPlayerPanelName, szPlayerName, "", False, True, PanelStyles.PANEL_STYLE_EMPTY )				

				screen.attachLabel(currentPlayerPanelName, "", "                    ")

				if (self.iScreen == FOREIGN_BONUS_SCREEN):
					if (not playerActive.canTradeNetworkWith(iLoopPlayer) and not gc.getGame().isDebugMode()):
						screen.attachMultiListControlGFC(currentPlayerPanelName, "ChildTrade" + currentPlayerPanelName, "", 1, self.BUTTON_SIZE, self.BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
						screen.appendMultiListButton("ChildTrade" + currentPlayerPanelName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), 0, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
					else:
						listTradeable = []
						listUntradeable = []
						tradeData = TradeData()
						tradeData.ItemType = TradeableItems.TRADE_RESOURCES
						for iLoopBonus in range(gc.getNumBonusInfos()):
							tradeData.iData = iLoopBonus
							if (gc.getPlayer(iLoopPlayer).canTradeItem(self.iActiveLeader, tradeData, False)):
								if (gc.getPlayer(iLoopPlayer).getTradeDenial(self.iActiveLeader, tradeData) == DenialTypes.NO_DENIAL):
									listTradeable.append(iLoopBonus)
								else:
									listUntradeable.append(iLoopBonus)
									
						if len(listTradeable) > 0:
							screen.attachLabel(currentPlayerPanelName, "", u"<font=4>" + localText.getText("TXT_KEY_FOREIGN_ADVISOR_FOR_TRADE", ()) + u"</font>")
										
						screen.attachMultiListControlGFC(currentPlayerPanelName, "ChildTrade" + currentPlayerPanelName, "", 1, self.BUTTON_SIZE, self.BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
						for iLoopBonus in listTradeable:
							screen.appendMultiListButton("ChildTrade" + currentPlayerPanelName, gc.getBonusInfo(iLoopBonus).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iLoopBonus, -1, False)
									
						if len(listUntradeable) > 0:
							screen.attachLabel(currentPlayerPanelName, "", u"<font=4>" + localText.getText("TXT_KEY_FOREIGN_ADVISOR_NOT_FOR_TRADE", ()) + u"</font>")
										
						screen.attachMultiListControlGFC(currentPlayerPanelName, "ChildNoTrade" + currentPlayerPanelName, "", 1, self.BUTTON_SIZE, self.BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
						for iLoopBonus in listUntradeable:
							screen.appendMultiListButton("ChildNoTrade" + currentPlayerPanelName, gc.getBonusInfo(iLoopBonus).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iLoopBonus, -1, False)

				elif (self.iScreen == FOREIGN_TECH_SCREEN):
					if (not gc.getTeam(playerActive.getTeam()).isTechTrading() and not gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isTechTrading() and not gc.getGame().isDebugMode()):
						screen.attachMultiListControlGFC(currentPlayerPanelName, "ChildTrade" + currentPlayerPanelName, "", 1, self.BUTTON_SIZE, self.BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
						screen.appendMultiListButton("ChildTrade" + currentPlayerPanelName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), 0, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
					else:
						listTradeable = []
						listUntradeable = []
						listTradeNotAllowed = []						
						tradeData = TradeData()
						tradeData.ItemType = TradeableItems.TRADE_TECHNOLOGIES
						for iLoopTech in range(gc.getNumTechInfos()):
							tradeData.iData = iLoopTech
							if (gc.getPlayer(iLoopPlayer).canTradeItem(self.iActiveLeader, tradeData, False)):
								if (gc.getPlayer(iLoopPlayer).getTradeDenial(self.iActiveLeader, tradeData) == DenialTypes.NO_DENIAL):
									listTradeable.append(iLoopTech)
								else:
									listUntradeable.append(iLoopTech)
							elif (gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isHasTech(iLoopTech) and playerActive.canResearch(iLoopTech, False)):
								listTradeNotAllowed.append(iLoopTech)
										
						if len(listTradeable) > 0:
							screen.attachLabel(currentPlayerPanelName, "", u"<font=4>" + localText.getText("TXT_KEY_FOREIGN_ADVISOR_FOR_TRADE", ()) + u"</font>")
										
						screen.attachMultiListControlGFC(currentPlayerPanelName, "ChildTrade" + currentPlayerPanelName, "", 1, self.BUTTON_SIZE, self.BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
						for iLoopTech in listTradeable:
							screen.appendMultiListButton("ChildTrade" + currentPlayerPanelName, gc.getTechInfo(iLoopTech).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech, -1, False)

						if len(listUntradeable) > 0:
							screen.attachLabel(currentPlayerPanelName, "", u"<font=4>" + localText.getText("TXT_KEY_FOREIGN_ADVISOR_NOT_FOR_TRADE", ()) + u"</font>")
										
						screen.attachMultiListControlGFC(currentPlayerPanelName, "ChildNoTrade" + currentPlayerPanelName, "", 1, self.BUTTON_SIZE, self.BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
						for iLoopTech in listUntradeable:
							screen.appendMultiListButton("ChildNoTrade" + currentPlayerPanelName, gc.getTechInfo(iLoopTech).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech, -1, False)

						if len(listTradeNotAllowed) > 0:
							screen.attachLabel(currentPlayerPanelName, "", u"<font=4>" + localText.getText("TXT_KEY_FOREIGN_ADVISOR_NOT_ALLOWED_TRADE", ()) + u"</font>")
										
						screen.attachMultiListControlGFC(currentPlayerPanelName, "ChildCantTrade" + currentPlayerPanelName, "", 1, self.BUTTON_SIZE, self.BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
						for iLoopTech in listTradeNotAllowed:
							screen.appendMultiListButton("ChildCantTrade" + currentPlayerPanelName, gc.getTechInfo(iLoopTech).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech, -1, False)

				screen.attachLabel(currentPlayerPanelName, "", "   ")
				szName = self.getNextWidgetName()
				screen.addCheckBoxGFCAt(currentPlayerPanelName, szName, gc.getLeaderHeadInfo(gc.getPlayer(iLoopPlayer).getLeaderType()).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 10, 0, self.W_LEADER, self.H_LEADER, WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, -1, ButtonStyles.BUTTON_STYLE_LABEL, False)
				if (self.iSelectedLeader == iLoopPlayer):
					screen.setState(szName, True)
				else:
					screen.setState(szName, False)
					
	def drawRelations(self, bInitial):
	
		if self.iShiftKeyDown == 1:
			if (self.iSelectedLeader in self.listSelectedLeaders):
				self.listSelectedLeaders.remove(self.iSelectedLeader)
			else:
				self.listSelectedLeaders.append(self.iSelectedLeader)
		else:
			self.listSelectedLeaders = []
			if (not bInitial):
				self.listSelectedLeaders.append(self.iSelectedLeader)	
		
		bNoLeadersSelected = (len(self.listSelectedLeaders) == 0)
		bSingleLeaderSelected = (len(self.listSelectedLeaders) == 1)
		if bSingleLeaderSelected:
			self.iSelectedLeader = self.listSelectedLeaders[0]
		
		# Get the Players
		playerActive = gc.getPlayer(self.iActiveLeader)
		
		# count the leaders
		iCount = 0
		leaderMap = { }
		# Count all other leaders
		for iPlayer in range(gc.getMAX_PLAYERS()):
			player = gc.getPlayer(iPlayer)
			if (player.isAlive() and iPlayer != self.iActiveLeader and (gc.getTeam(player.getTeam()).isHasMet(gc.getPlayer(self.iActiveLeader).getTeam()) or gc.getGame().isDebugMode()) and not player.isBarbarian() and not player.isMinorCiv()):
				leaderMap[iPlayer] = iCount
				iCount = iCount + 1
		fLeaderTop = self.Y_LEADER_CIRCLE_TOP
		fRadius = self.RADIUS_LEADER_ARC - self.H_LEADER
		fLeaderArcTop = fLeaderTop + self.H_LEADER + 10
		
		if iCount < 8:
			iLeaderHeight = int((3 * self.H_LEADER) / 2)
			iLeaderWidth = int((3 * self.W_LEADER) / 2)
		else:
			iLeaderHeight = self.H_LEADER
			iLeaderWidth = self.W_LEADER
			

		screen = self.getScreen()

		#screen.addPanel(self.getNextWidgetName(), "", "", False, False, 0, 50, self.W_SCREEN, 667, PanelStyles.PANEL_STYLE_MAIN_WHITE)
		#screen.addPanel(self.getNextWidgetName(), "", "", False, False, 0, 50, self.W_SCREEN, 667, PanelStyles.PANEL_STYLE_MAIN_WHITE)
		#screen.addPanel(self.getNextWidgetName(), "", "", False, False, 0, 50, self.W_SCREEN, 667, PanelStyles.PANEL_STYLE_MAIN_WHITE)

		# legend
		screen.addPanel(self.getNextWidgetName(), u"", u"", True, False, self.X_LEGEND, self.Y_LEGEND, self.W_LEGEND, self.H_LEGEND, PanelStyles.PANEL_STYLE_IN)
		x = self.X_LEGEND + self.MARGIN_LEGEND
		y = self.Y_LEGEND + self.MARGIN_LEGEND
		screen.setLabel(self.getNextWidgetName(), "", u"<font=2>" + localText.getText("TXT_KEY_FOREIGN_ADVISOR_CONTACT", ()) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, x, y-10, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		y += self.MARGIN_LEGEND
		screen.addLineGFC(self.BACKGROUND_ID, self.getNextLineName(), x, y, x + self.W_LEGEND - 2*self.MARGIN_LEGEND, y, gc.getInfoTypeForString("COLOR_WHITE"))
		y += 2 * self.MARGIN_LEGEND
		screen.setLabel(self.getNextWidgetName(), "", u"<font=2>" + localText.getText("TXT_KEY_CONCEPT_WAR", ()) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, x, y-10, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		y += self.MARGIN_LEGEND
		screen.addLineGFC(self.BACKGROUND_ID, self.getNextLineName(), x, y, x + self.W_LEGEND - 2*self.MARGIN_LEGEND, y, gc.getInfoTypeForString("COLOR_RED"))
		y += 2 * self.MARGIN_LEGEND
		screen.setLabel(self.getNextWidgetName(), "", u"<font=2>" + localText.getText("TXT_KEY_TRADE_DEFENSIVE_PACT_STRING", ()) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, x, y-10, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		y += self.MARGIN_LEGEND
		screen.addLineGFC(self.BACKGROUND_ID, self.getNextLineName(), x, y, x + self.W_LEGEND - 2*self.MARGIN_LEGEND, y, gc.getInfoTypeForString("COLOR_BLUE"))
		y += 2 * self.MARGIN_LEGEND
		screen.setLabel(self.getNextWidgetName(), "", u"<font=2>" + localText.getText("TXT_KEY_TRADE_OPEN_BORDERS_STRING", ()) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, x, y-10, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		y += self.MARGIN_LEGEND
		screen.addLineGFC(self.BACKGROUND_ID, self.getNextLineName(), x, y, x + self.W_LEGEND - 2*self.MARGIN_LEGEND, y, gc.getInfoTypeForString("COLOR_CITY_GREEN"))
		y += 2 * self.MARGIN_LEGEND
		screen.setLabel(self.getNextWidgetName(), "", u"<font=2>" + localText.getText("TXT_KEY_PITBOSS_TEAM", ()) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, x, y-10, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		y += self.MARGIN_LEGEND
		screen.addLineGFC(self.BACKGROUND_ID, self.getNextLineName(), x, y, x + self.W_LEGEND - 2*self.MARGIN_LEGEND, y, gc.getInfoTypeForString("COLOR_YELLOW"))
		y += 2 * self.MARGIN_LEGEND
		screen.setLabel(self.getNextWidgetName(), "", u"<font=2>" + localText.getText("TXT_KEY_MISC_VASSAL_SHORT", ()) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, x, y-10, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		y += self.MARGIN_LEGEND
		screen.addLineGFC(self.BACKGROUND_ID, self.getNextLineName(), x, y, x + self.W_LEGEND - 2*self.MARGIN_LEGEND, y, gc.getInfoTypeForString("COLOR_CYAN"))
	
		# Our leader head
		szLeaderHead = self.getNextWidgetName()
		#screen.addCheckBoxGFC(szLeaderHead, gc.getLeaderHeadInfo(gc.getPlayer(self.iActiveLeader).getLeaderType()).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), self.X_LEADER_CIRCLE_TOP - iLeaderWidth/2, int(fLeaderTop), iLeaderWidth, iLeaderHeight, WidgetTypes.WIDGET_LEADERHEAD, self.iActiveLeader, -1, ButtonStyles.BUTTON_STYLE_LABEL) #Rhye
		screen.addCheckBoxGFC(szLeaderHead, gc.getCivilizationInfo(gc.getPlayer(self.iActiveLeader).getCivilizationType()).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), self.X_LEADER_CIRCLE_TOP - iLeaderWidth/2, int(fLeaderTop), iLeaderWidth, iLeaderHeight, WidgetTypes.WIDGET_LEADERHEAD, self.iActiveLeader, -1, ButtonStyles.BUTTON_STYLE_LABEL) #Rhye
		if (self.iActiveLeader in self.listSelectedLeaders):
			screen.setState(szLeaderHead, True)
		else:
			screen.setState(szLeaderHead, False)
		szName = self.getNextWidgetName()
		#Rhye - start
		#szLeaderName = u"<font=3>" + playerActive.getName() + u"</font>"
		#szLeaderName = u"<font=3>" + playerActive.getCivilizationShortDescription(0) + u"</font>"
		if (len(leaderMap.keys()) >= 16):
			szLeaderName = u"<font=1>" + playerActive.getCivilizationDescription(0) + u"</font>"
			iDist = -4
		elif (len(leaderMap.keys()) >= 12):
			szLeaderName = u"<font=2>" + playerActive.getCivilizationDescription(0) + u"</font>"
			iDist = 1
		else:
			szLeaderName = u"<font=3>" + playerActive.getCivilizationDescription(0) + u"</font>"
			iDist = 5
		#screen.setLabel(szName, "", szLeaderName, CvUtil.FONT_CENTER_JUSTIFY, self.X_LEADER_CIRCLE_TOP, fLeaderTop + iLeaderHeight + 5, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabel(szName, "", szLeaderName, CvUtil.FONT_CENTER_JUSTIFY, self.X_LEADER_CIRCLE_TOP, fLeaderTop + iLeaderHeight + iDist, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		#Rhye - end
		
				
		# angle increment in radians (180 degree range)
		if (iCount < 2):
			deltaTheta = 0
		else:
			deltaTheta = 3.1415927 / (iCount - 1)

		iTot = 0 #Rhye
		# draw other leaderheads
		for iPlayer in leaderMap.keys():
			player = gc.getPlayer(iPlayer)
			iTot += 1 #Rhye

			if bSingleLeaderSelected:
				# attitudes shown are towards single selected leader
				iBaseLeader = self.iSelectedLeader
			else:
				# attitudes shown are towards active leader
				iBaseLeader = self.iActiveLeader
			playerBase = gc.getPlayer(iBaseLeader)

			fX = int(self.X_LEADER_CIRCLE_TOP - fRadius * math.cos(deltaTheta * leaderMap[iPlayer]) - iLeaderWidth/2) 
			fY = int(fLeaderArcTop + fRadius * math.sin(deltaTheta * leaderMap[iPlayer]) - iLeaderHeight/2)

			szLeaderHead = self.getNextWidgetName()
			#screen.addCheckBoxGFC(szLeaderHead, gc.getLeaderHeadInfo(player.getLeaderType()).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), int(fX), int(fY), iLeaderWidth, iLeaderHeight, WidgetTypes.WIDGET_LEADERHEAD, iPlayer, iBaseLeader, ButtonStyles.BUTTON_STYLE_LABEL) #Rhye
			screen.addCheckBoxGFC(szLeaderHead, gc.getCivilizationInfo(player.getCivilizationType()).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), int(fX), int(fY), iLeaderWidth, iLeaderHeight, WidgetTypes.WIDGET_LEADERHEAD, iPlayer, iBaseLeader, ButtonStyles.BUTTON_STYLE_LABEL) #Rhye
			if (iPlayer in self.listSelectedLeaders):
				screen.setState(szLeaderHead, True)
			else:
				screen.setState(szLeaderHead, False)
				
			szName = self.getNextWidgetName()
			#Rhye - start
			iOffsetX = 0
			#szText = u"<font=3>" + player.getName() + u"</font>"
			#szText = u"<font=3>" + player.getCivilizationShortDescription(0) + u"</font>"
			if (len(leaderMap.keys()) >= 16):
				szText = u"<font=1>" + player.getCivilizationDescription(0) + u"</font>"
				iDist = -4
				iOffsetX = (min(5, max(-5, iTot - len(leaderMap.keys())/2)))*6
			elif (len(leaderMap.keys()) >= 12):
				szText = u"<font=2>" + player.getCivilizationDescription(0) + u"</font>"
				iDist = 1
				iOffsetX = (min(5, max(-5, iTot - len(leaderMap.keys())/2)))*3
			else:
				szText = u"<font=3>" + player.getCivilizationDescription(0) + u"</font>"
				iDist = 5
                        #screen.setLabel(szName, "", szText, CvUtil.FONT_CENTER_JUSTIFY, fX + iLeaderWidth/2, fY + iLeaderHeight + 5, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setLabel(szName, "", szText, CvUtil.FONT_CENTER_JUSTIFY, fX + iLeaderWidth/2 + iOffsetX, fY + iLeaderHeight + iDist, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			#Rhye - end

			# Leader attitude towards active player
			szName = self.getNextWidgetName()
			if (gc.getTeam(player.getTeam()).isHasMet(playerBase.getTeam()) and iBaseLeader != iPlayer):		
				#Rhye - start
				#szText = " (" + gc.getAttitudeInfo(gc.getPlayer(iPlayer).AI_getAttitude(iBaseLeader)).getDescription()
				#if (iBaseLeader != iPlayer):
				#	if (gc.getTeam(player.getTeam()).isVassal(playerBase.getTeam())):
				#		szText += ", " + localText.getText("TXT_KEY_MISC_VASSAL_SHORT", ())
				#	elif (gc.getTeam(playerBase.getTeam()).isVassal(player.getTeam())):
				#		szText += ", " + localText.getText("TXT_KEY_MISC_MASTER", ())
				#szText += ")"
				if (len(leaderMap.keys()) >= 16):
					szText = u"<font=1>" + " (" + gc.getAttitudeInfo(gc.getPlayer(iPlayer).AI_getAttitude(iBaseLeader)).getDescription() + u"</font>"
					if (iBaseLeader != iPlayer):
						if (gc.getTeam(player.getTeam()).isVassal(playerBase.getTeam())):
							szText += (u"<font=1>" + ", " + localText.getText("TXT_KEY_MISC_VASSAL_SHORT", ()) + u"</font>")
						elif (gc.getTeam(playerBase.getTeam()).isVassal(player.getTeam())):
							szText += (u"<font=1>" + ", " + localText.getText("TXT_KEY_MISC_MASTER", ()) + u"</font>")
					szText += (u"<font=1>" + ")" + u"</font>")
				else:
					szText = " (" + gc.getAttitudeInfo(gc.getPlayer(iPlayer).AI_getAttitude(iBaseLeader)).getDescription()
					if (iBaseLeader != iPlayer):
						if (gc.getTeam(player.getTeam()).isVassal(playerBase.getTeam())):
							szText += ", " + localText.getText("TXT_KEY_MISC_VASSAL_SHORT", ())
						elif (gc.getTeam(playerBase.getTeam()).isVassal(player.getTeam())):
							szText += ", " + localText.getText("TXT_KEY_MISC_MASTER", ())
					szText += ")"
				#Rhye - end
			else:
				szText = u""
			#Rhye - start
			iOffsetY = 0
			if (len(leaderMap.keys()) >= 16):
				iOffsetY = -16
			elif (len(leaderMap.keys()) >= 12):
				iOffsetY = -8
			#screen.setLabel(szName, "", szText, CvUtil.FONT_CENTER_JUSTIFY, fX + iLeaderWidth/2, fY + iLeaderHeight + 25, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setLabel(szName, "", szText, CvUtil.FONT_CENTER_JUSTIFY, fX + iLeaderWidth/2 + iOffsetX, fY + iLeaderHeight + 25 + iOffsetY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			#Rhye - end
			
		# draw lines
		for iSelectedLeader in range(gc.getMAX_PLAYERS()):
			bDisplayed = (not gc.getPlayer(iSelectedLeader).isBarbarian() and not gc.getPlayer(iSelectedLeader).isMinorCiv() and gc.getPlayer(iSelectedLeader).isAlive() and (gc.getGame().isDebugMode() or gc.getTeam(playerActive.getTeam()).isHasMet(gc.getPlayer(iSelectedLeader).getTeam())))
			if iSelectedLeader in self.listSelectedLeaders or (bNoLeadersSelected and bDisplayed):
				# get selected player and location
				if (iSelectedLeader in leaderMap):
					thetaSelected = deltaTheta * leaderMap[iSelectedLeader]
					fXSelected = self.X_LEADER_CIRCLE_TOP - fRadius * math.cos(thetaSelected)
					fYSelected = fLeaderArcTop + fRadius * math.sin(thetaSelected)
				else:
					fXSelected = self.X_LEADER_CIRCLE_TOP
					fYSelected = fLeaderTop + iLeaderHeight/2
				
				for iPlayer in leaderMap.keys():
					player = gc.getPlayer(iPlayer)

					fX = self.X_LEADER_CIRCLE_TOP - fRadius * math.cos(deltaTheta * leaderMap[iPlayer])
					fY = fLeaderArcTop + fRadius * math.sin(deltaTheta * leaderMap[iPlayer])
					
					# draw lines
					if (iSelectedLeader != iPlayer):
						if (player.getTeam() == gc.getPlayer(iSelectedLeader).getTeam()):
							szName = self.getNextLineName()
							screen.addLineGFC(self.BACKGROUND_ID, szName, int(fXSelected), int(fYSelected), int(fX), int(fY), gc.getInfoTypeForString("COLOR_YELLOW") )						
						elif (gc.getTeam(player.getTeam()).isVassal(gc.getPlayer(iSelectedLeader).getTeam()) or gc.getTeam(gc.getPlayer(iSelectedLeader).getTeam()).isVassal(player.getTeam())):
							szName = self.getNextLineName()
							screen.addLineGFC(self.BACKGROUND_ID, szName, int(fXSelected), int(fYSelected), int(fX), int(fY), gc.getInfoTypeForString("COLOR_CYAN") )						
						elif (gc.getTeam(player.getTeam()).isHasMet(gc.getPlayer(iSelectedLeader).getTeam())):
							if (gc.getTeam(player.getTeam()).isAtWar(gc.getPlayer(iSelectedLeader).getTeam())):
								szName = self.getNextLineName()
								screen.addLineGFC(self.BACKGROUND_ID, szName, int(fXSelected), int(fYSelected), int(fX), int(fY), gc.getInfoTypeForString("COLOR_RED") )
							else:
								bJustPeace = True
								if (gc.getTeam(player.getTeam()).isOpenBorders(gc.getPlayer(iSelectedLeader).getTeam())):
									fDy = fYSelected - fY
									fDx = fXSelected - fX
									fTheta = math.atan2(fDy, fDx)
									if (fTheta > 0.5 * math.pi):
										fTheta -= math.pi
									elif (fTheta < -0.5 * math.pi):
										fTheta += math.pi
									fSecondLineOffsetY = self.LINE_WIDTH * math.cos(fTheta)
									fSecondLineOffsetX = -self.LINE_WIDTH * math.sin(fTheta)
									szName = self.getNextLineName()
									screen.addLineGFC(self.BACKGROUND_ID, szName, int(fXSelected + fSecondLineOffsetX), int(fYSelected + fSecondLineOffsetY), int(fX + fSecondLineOffsetX), int(fY + fSecondLineOffsetY), gc.getInfoTypeForString("COLOR_CITY_GREEN") )
									bJustPeace = False
								if (gc.getTeam(player.getTeam()).isDefensivePact(gc.getPlayer(iSelectedLeader).getTeam())):
									szName = self.getNextLineName()
									screen.addLineGFC(self.BACKGROUND_ID, szName, int(fXSelected), int(fYSelected), int(fX), int(fY), gc.getInfoTypeForString("COLOR_BLUE") )
									bJustPeace = False
								if (bJustPeace):
									szName = self.getNextLineName()
									screen.addLineGFC(self.BACKGROUND_ID, szName, int(fXSelected), int(fYSelected), int(fX), int(fY), gc.getInfoTypeForString("COLOR_WHITE") )
		
				player = gc.getPlayer(self.iActiveLeader)
				if (player.getTeam() == gc.getPlayer(iSelectedLeader).getTeam()):
					szName = self.getNextLineName()
					screen.addLineGFC(self.BACKGROUND_ID, szName, int(fXSelected), int(fYSelected), self.X_LEADER_CIRCLE_TOP, fLeaderTop + iLeaderHeight/2, gc.getInfoTypeForString("COLOR_YELLOW") )
				elif (gc.getTeam(player.getTeam()).isVassal(gc.getPlayer(iSelectedLeader).getTeam()) or gc.getTeam(gc.getPlayer(iSelectedLeader).getTeam()).isVassal(player.getTeam())):
					szName = self.getNextLineName()
					screen.addLineGFC(self.BACKGROUND_ID, szName, int(fXSelected), int(fYSelected), self.X_LEADER_CIRCLE_TOP, fLeaderTop + iLeaderHeight/2, gc.getInfoTypeForString("COLOR_CYAN") )
				elif (gc.getTeam(player.getTeam()).isHasMet(gc.getPlayer(iSelectedLeader).getTeam())):
					if (gc.getTeam(player.getTeam()).isAtWar(gc.getPlayer(iSelectedLeader).getTeam())):
						szName = self.getNextLineName()
						screen.addLineGFC(self.BACKGROUND_ID, szName, int(fXSelected), int(fYSelected), self.X_LEADER_CIRCLE_TOP, fLeaderTop + iLeaderHeight/2, gc.getInfoTypeForString("COLOR_RED") )
					else:
						bJustPeace = True
						if (gc.getTeam(player.getTeam()).isOpenBorders(gc.getPlayer(iSelectedLeader).getTeam())):
							fDy = fLeaderTop + iLeaderHeight/2 - fYSelected
							fDx = self.X_LEADER_CIRCLE_TOP - fXSelected
							fTheta = math.atan2(fDy, fDx)
							if (fTheta > 0.5 * math.pi):
								fTheta -= math.pi
							elif (fTheta < -0.5 * math.pi):
								fTheta += math.pi
							fSecondLineOffsetY = self.LINE_WIDTH * math.cos(fTheta)
							fSecondLineOffsetX = -self.LINE_WIDTH * math.sin(fTheta)
							szName = self.getNextLineName()
							screen.addLineGFC(self.BACKGROUND_ID, szName, int(fXSelected + fSecondLineOffsetX), int(fYSelected + fSecondLineOffsetY), int(self.X_LEADER_CIRCLE_TOP + fSecondLineOffsetX), int(fLeaderTop + iLeaderHeight/2 + fSecondLineOffsetY), gc.getInfoTypeForString("COLOR_CITY_GREEN") )
							bJustPeace = False
						if (gc.getTeam(player.getTeam()).isDefensivePact(gc.getPlayer(iSelectedLeader).getTeam())):
							szName = self.getNextLineName()
							screen.addLineGFC(self.BACKGROUND_ID, szName, int(fXSelected), int(fYSelected), int(self.X_LEADER_CIRCLE_TOP), int(fLeaderTop + iLeaderHeight/2), gc.getInfoTypeForString("COLOR_BLUE") )
							bJustPeace = False
						if (bJustPeace):
							szName = self.getNextLineName()
							screen.addLineGFC(self.BACKGROUND_ID, szName, int(fXSelected), int(fYSelected), int(self.X_LEADER_CIRCLE_TOP), int(fLeaderTop + iLeaderHeight/2), gc.getInfoTypeForString("COLOR_WHITE") )

															
	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount * NUM_FOREIGN_SCREENS + self.iScreen)
		self.nWidgetCount += 1
		return szName
											
	def getNextLineName(self):
		szName = self.LINE_ID + str(self.nLineCount * NUM_FOREIGN_SCREENS + self.iScreen)
		self.nLineCount += 1
		return szName
											
	def getWidgetName(self, szBaseName):
		szName = szBaseName + str(self.iScreen)
		return szName
		
	def clearAllLines(self):
		screen = self.getScreen()
		nLines = self.nLineCount
		self.nLineCount = 0
		for i in range(nLines):
			screen.removeLineGFC(self.BACKGROUND_ID, self.getNextLineName())
		self.nLineCount = 0	

		
	def deleteAllWidgets(self):
		screen = self.getScreen()
		i = self.nWidgetCount - 1
		while (i >= 0):
			self.nWidgetCount = i
			screen.deleteWidget(self.getNextWidgetName())
			i -= 1

		self.nWidgetCount = 0
		self.clearAllLines()			
			
	# Handles the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getButtonType() == WidgetTypes.WIDGET_LEADERHEAD):
				if (inputClass.getFlags() & MouseFlags.MOUSE_LBUTTONUP):
					self.iSelectedLeader = inputClass.getData1()
					self.drawContents(False)
				elif (inputClass.getFlags() & MouseFlags.MOUSE_RBUTTONUP):
					if (self.iActiveLeader != inputClass.getData1()):
						self.getScreen().hideScreen()
			 
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			if (inputClass.getFunctionName() + str(inputClass.getID()) == self.getWidgetName(self.DEBUG_DROPDOWN_ID)):
				szName = self.getWidgetName(self.DEBUG_DROPDOWN_ID)
				iIndex = self.getScreen().getSelectedPullDownID(szName)
				self.iActiveLeader = self.getScreen().getPullDownData(szName, iIndex)
				self.drawContents(False)
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER):
			if (inputClass.getData() == int(InputTypes.KB_LSHIFT) or inputClass.getData() == int(InputTypes.KB_RSHIFT)):
				self.iShiftKeyDown = inputClass.getID() 

		return 0

	def update(self, fDelta):
		if (CyInterface().isDirty(InterfaceDirtyBits.Foreign_Screen_DIRTY_BIT) == True):
			CyInterface().setDirty(InterfaceDirtyBits.Foreign_Screen_DIRTY_BIT, False)
			self.drawContents(False)
		return

