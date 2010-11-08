## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
## Improvements to this screen by Almightix - thanks
from CvPythonExtensions import *
from PyHelpers import PyPlayer
import CvUtil
import ScreenInput
import CvScreenEnums
import Consts as con #Rhye

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvEspionageAdvisor:

	def __init__(self):
		self.SCREEN_NAME = "EspionageAdvisor"
		self.DEBUG_DROPDOWN_ID =  "EspionageAdvisorDropdownWidget"
		self.WIDGET_ID = "EspionageAdvisorWidget"
		self.WIDGET_HEADER = "EspionageAdvisorWidgetHeader"
		self.EXIT_ID = "EspionageAdvisorExitWidget"
		self.BACKGROUND_ID = "EspionageAdvisorBackground"
		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Y_TITLE = 12
		self.BORDER_WIDTH = 4
		self.PANE_HEIGHT = 450
		self.PANE_WIDTH = 283
		self.X_SLIDERS = 50
		self.X_INCOME = 373
		self.X_EXPENSES = 696
		self.Y_TREASURY = 90
		self.H_TREASURY = 100
		self.Y_LOCATION = 230
		self.Y_SPACING = 30
		self.TEXT_MARGIN = 15
		self.Z_BACKGROUND = -2.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.DZ = -0.2
		
		self.X_EXIT = 994
		self.Y_EXIT = 726
		
		self.nWidgetCount = 0
		
		self.iDirtyBit = 0
		
		self.iTargetPlayer = -1
		
		self.iActiveCityID = -1
		self.iSelectedMission = -1

	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.ESPIONAGE_ADVISOR)

	def interfaceScreen (self):

		self.iTargetPlayer = -1		
		self.iActiveCityID = -1
		self.iSelectedMission = -1
		self.iActivePlayer = CyGame().getActivePlayer()
	
		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen( PopupStates.POPUPSTATE_IMMEDIATE, False)
	
		# Set the background and exit button, and show the screen
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)

		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )

		screen.showWindowBackground(False)
		screen.setText(self.EXIT_ID, "Background", u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		# Header...
		screen.setLabel(self.WIDGET_HEADER, "Background", u"<font=4b>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
		if (CyGame().isDebugMode()):
			self.iDebugDropdownID = 554
			self.szDropdownName = self.DEBUG_DROPDOWN_ID
			screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, self.iDebugDropdownID, -1, FontTypes.GAME_FONT)
			for j in range(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getName(), j, j, False )

		# draw the contents
		self.drawContents()
		
		self.refreshScreen()

	def drawContents(self):
		
		self.deleteAllWidgets()
		
		# Create a new screen, called EspionageAdvisor, using the file EspionageAdvisor.py for input
		screen = self.getScreen()
	
		pActivePlayer = gc.getPlayer(self.iActivePlayer)
		pActiveTeam = gc.getTeam(pActivePlayer.getTeam())
		
		self.X_LEFT_PANE = 25
		self.Y_LEFT_PANE = 70
		self.W_LEFT_PANE = 400
		self.H_LEFT_PANE = 620
		
		self.szLeftPaneWidget = "LeftPane"
		screen.addPanel( self.szLeftPaneWidget, "", "", true, true,
			self.X_LEFT_PANE, self.Y_LEFT_PANE, self.W_LEFT_PANE, self.H_LEFT_PANE, PanelStyles.PANEL_STYLE_MAIN )

		self.X_SCROLL = self.X_LEFT_PANE + 20
		self.Y_SCROLL= 90
		self.W_SCROLL= 360
		self.H_SCROLL= 580
		
		self.szScrollPanel = "ScrollPanel"
		screen.addPanel( self.szScrollPanel, "", "", true, true,
			self.X_SCROLL, self.Y_SCROLL, self.W_SCROLL, self.H_SCROLL, PanelStyles.PANEL_STYLE_EMPTY)
		
		self.aiKnownPlayers = []
		self.aiUnknownPlayers = []
		self.iNumEntries= 0

		for iLoop in range(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iLoop)
			#if (pPlayer.getTeam() != pActivePlayer.getTeam() and not pPlayer.isBarbarian()): #Rhye
                        if (pPlayer.getTeam() != pActivePlayer.getTeam() and iLoop < con.iNumActivePlayers): #Rhye
				if (pPlayer.isAlive()):
					if (pActiveTeam.isHasMet(pPlayer.getTeam())):
						
						self.aiKnownPlayers.append(iLoop)
						self.iNumEntries = self.iNumEntries + 1
						
						if (self.iTargetPlayer == -1):
							self.iTargetPlayer = iLoop

		while(self.iNumEntries < 17): #Rhye - why 17?
			self.iNumEntries = self.iNumEntries + 1
			self.aiUnknownPlayers.append(self.iNumEntries)
		
		############################
		#### Total EPs Per Turn Text
		############################

		self.X_TOTAL_PANE = self.X_LEFT_PANE + self.W_LEFT_PANE + 20
		self.Y_TOTAL_PANE = self.Y_LEFT_PANE
		self.W_TOTAL_PANE = 550
		self.H_TOTAL_PANE = 60
		
		self.szTotalPaneWidget = "TotalPane"
		screen.addPanel( self.szTotalPaneWidget, "", "", true, true,
			self.X_TOTAL_PANE, self.Y_TOTAL_PANE, self.W_TOTAL_PANE, self.H_TOTAL_PANE, PanelStyles.PANEL_STYLE_MAIN )
		
		self.szMakingText = "MakingText"
		self.X_MAKING_TEXT = 490
		self.Y_MAKING_TEXT = 85
		szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_TOTAL_NUM_EPS", (pActivePlayer.getCommerceRate(CommerceTypes.COMMERCE_ESPIONAGE), )) + "</font>"
		screen.setLabel(self.szMakingText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_MAKING_TEXT, self.Y_MAKING_TEXT, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		############################
		#### Right Panel
		############################

		self.X_RIGHT_PANE = self.X_TOTAL_PANE
		self.Y_RIGHT_PANE = self.Y_TOTAL_PANE + self.H_TOTAL_PANE + 20
		self.W_RIGHT_PANE = self.W_TOTAL_PANE
		self.H_RIGHT_PANE = self.H_LEFT_PANE - self.H_TOTAL_PANE - 20
		
		self.szRightPaneWidget = "RightPane"
		screen.addPanel( self.szRightPaneWidget, "", "", true, true,
			self.X_RIGHT_PANE, self.Y_RIGHT_PANE, self.W_RIGHT_PANE, self.H_RIGHT_PANE, PanelStyles.PANEL_STYLE_MAIN )
		
		self.X_CITY_LIST = self.X_RIGHT_PANE + 40
		self.Y_CITY_LIST = self.Y_RIGHT_PANE + 60
		self.W_CITY_LIST = 160
		self.H_CITY_LIST = self.H_RIGHT_PANE - 90
		
		self.X_EFFECTS_LIST = self.X_CITY_LIST + self.W_CITY_LIST + 20
		self.Y_EFFECTS_LIST = self.Y_CITY_LIST
		self.W_EFFECTS_LIST = 210
		self.H_EFFECTS_LIST = (self.H_CITY_LIST / 3) - 50
		
		self.X_EFFECTS_COSTS_LIST = self.X_EFFECTS_LIST + self.W_EFFECTS_LIST + 10
		self.Y_EFFECTS_COSTS_LIST = self.Y_EFFECTS_LIST
		self.W_EFFECTS_COSTS_LIST = 60
		self.H_EFFECTS_COSTS_LIST = self.H_EFFECTS_LIST
		
		self.X_MISSIONS_LIST = self.X_CITY_LIST + self.W_CITY_LIST + 20
		self.Y_MISSIONS_LIST = self.Y_EFFECTS_LIST + self.H_EFFECTS_LIST + 50
		self.W_MISSIONS_LIST = self.W_EFFECTS_LIST
		self.H_MISSIONS_LIST = (self.H_CITY_LIST * 2 / 3) #- 45
		
		self.X_MISSIONS_COSTS_LIST = self.X_MISSIONS_LIST + self.W_MISSIONS_LIST + 10
		self.Y_MISSIONS_COSTS_LIST = self.Y_MISSIONS_LIST
		self.W_MISSIONS_COSTS_LIST = self.W_EFFECTS_COSTS_LIST
		self.H_MISSIONS_COSTS_LIST = self.H_MISSIONS_LIST
		
		self.X_MISSION_BUTTON = self.X_MISSIONS_LIST
		self.Y_MISSION_BUTTON = self.Y_MISSIONS_LIST + self.H_MISSIONS_LIST + 10
		self.W_MISSION_BUTTON = self.W_MISSIONS_LIST + self.W_MISSIONS_COSTS_LIST + 10
		self.H_MISSION_BUTTON = 30
		
		if (self.iTargetPlayer != -1):
			
			self.szCitiesTitleText = "CitiesTitle"
			szText = u"<font=4>" + localText.getText("TXT_KEY_CONCEPT_CITIES", ()) + "</font>"
			screen.setLabel(self.szCitiesTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_CITY_LIST, self.Y_CITY_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			
			self.szEffectsTitleText = "EffectsTitle"
			szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_PASSIVE_EFFECTS", ()) + "</font>"
			screen.setLabel(self.szEffectsTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_EFFECTS_LIST, self.Y_EFFECTS_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			
			self.szMissionsTitleText = "MissionsTitle"
			szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_MISSIONS", ()) + "</font>"
			screen.setLabel(self.szMissionsTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_MISSIONS_LIST, self.Y_MISSIONS_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			
			self.szEffectsCostTitleText = "EffectsCostTitle"
			szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_COST", ()) + "</font>"
			screen.setLabel(self.szEffectsCostTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_EFFECTS_COSTS_LIST, self.Y_EFFECTS_COSTS_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			
			self.szMissionsCostTitleText = "MissionsCostTitle"
			szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_COST", ()) + "</font>"
			screen.setLabel(self.szMissionsCostTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_MISSIONS_COSTS_LIST, self.Y_MISSIONS_COSTS_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			
			############################
			#### Left Leaders Panel
			############################
			
			self.W_LEADER = 128
			self.H_LEADER = 128
			
			self.W_NAME_PANEL = 220
			self.H_NAME_PANEL = 30
			
			iPlayerLoop = 0
			
			self.aszLeaderImages = []
			self.aszLeaderNamePanels = []
			self.aszNameTexts = []
			self.aszPointsTexts = []
			self.aszSpendingTexts = []
			self.aszRelativeTexts = []
			self.aszIncreaseButtons = []
			self.aszDecreaseButtons = []
			self.aszAmountTexts = []
			self.aszEspionageIcons = []
			
			for iPlayerID in self.aiKnownPlayers:
				
				pTargetPlayer = gc.getPlayer(iPlayerID)
				
				iTargetTeam = pTargetPlayer.getTeam()
				
				iX = 0
				iY = 14 #+ (148 * iPlayerLoop)#(110 * iPlayerLoop)
				
				attach = "LeaderContainer%d" % (iPlayerID)
				
				screen.attachPanel(self.szScrollPanel, attach, "", "", True, False, PanelStyles.PANEL_STYLE_STANDARD)
				
				szName = "LeaderImageA%d" %(iPlayerID)
				screen.attachSeparator(attach, szName, true, 30)
				
				self.iLeaderImagesID = 456
				szName = "LeaderImage%d" %(iPlayerID)
				self.aszLeaderImages.append(szName)
	
				#screen.addCheckBoxGFCAt(attach, szName, gc.getLeaderHeadInfo(gc.getPlayer(iPlayerID).getLeaderType()).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), #Rhye
				screen.addCheckBoxGFCAt(attach, szName, gc.getCivilizationInfo(gc.getPlayer(iPlayerID).getCivilizationType()).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), #Rhye
					iX +21 , iY - 14, 32, 32, WidgetTypes.WIDGET_GENERAL, self.iLeaderImagesID, iPlayerID, ButtonStyles.BUTTON_STYLE_LABEL, False)
				if (self.iTargetPlayer == iPlayerID):
					screen.setState(szName, true)
				
				szName = "LeaderNamePanel%d" %(iPlayerID)
				self.aszLeaderNamePanels.append(szName)
				screen.attachPanelAt( attach, szName, "", "", true, false, PanelStyles.PANEL_STYLE_MAIN,
					iX + 5, iY-15, self.W_NAME_PANEL, self.H_NAME_PANEL, WidgetTypes.WIDGET_GENERAL, -1, -1 )

				szName = "NameText%d" %(iPlayerID)
				self.aszNameTexts.append(szName)
				#szTempBuffer = u"<color=%d,%d,%d,%d>%s (%s)</color>" %(pTargetPlayer.getPlayerTextColorR(), pTargetPlayer.getPlayerTextColorG(), pTargetPlayer.getPlayerTextColorB(), pTargetPlayer.getPlayerTextColorA(), pTargetPlayer.getName(), self.getMultiplierAgainstTarget(iPlayerID)) #Rhye
				szTempBuffer = u"<color=%d,%d,%d,%d>%s (%s)</color>" %(pTargetPlayer.getPlayerTextColorR(), pTargetPlayer.getPlayerTextColorG(), pTargetPlayer.getPlayerTextColorB(), pTargetPlayer.getPlayerTextColorA(), pTargetPlayer.getCivilizationDescription(0), self.getMultiplierAgainstTarget(iPlayerID)) #Rhye
				szText = u"<font=2>" + szTempBuffer + "</font>"
				screen.setLabelAt( szName, attach, szText, 0, iX + 55, iY -15, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );
				
				szName = "PointsText%d" %(iPlayerID)
				self.aszPointsTexts.append(szName)
				szText = u"<font=2>" + localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS", (pActiveTeam.getEspionagePointsAgainstTeam(iTargetTeam), )) + "</font>"
				#Rhye
				#screen.setLabelAt( szName, attach, szText, 0, 247, iY - 14, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );
				screen.setLabelAt( szName, attach, szText, 0, 317, iY - 14, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );
				
				szName = "SpendingText%d" %(iPlayerID)
				self.aszSpendingTexts.append(szName)
				szText = u"<font=2>%s: %d</font>" %(localText.getText("TXT_KEY_ESPIONAGE_SCREEN_SPENDING_WEIGHT", ()), pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam))
				screen.setLabelAt( szName, attach, szText, 0, 85, iY - 1, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );
				
				szName = "AmountText%d" %(iPlayerID)
				self.aszAmountTexts.append(szName)
				if (pActivePlayer.getEspionageSpending(iTargetTeam) > 0):
					szText = u"<font=2><color=0,255,0,0>%s</color></font>" %(localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS_PER_TURN", (pActivePlayer.getEspionageSpending(iTargetTeam), )))
				else:
					szText = u"<font=2><color=192,0,0,0>%s</color></font>" %(localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS_PER_TURN", (pActivePlayer.getEspionageSpending(iTargetTeam), )))


				screen.setLabelAt( szName, attach, szText, 0, 247, iY - 1, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

				szName = "SpendingIcon%d" %(iPlayerID)
				self.aszEspionageIcons.append(szName)
				if (pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam) > 0):
					szText = u"<font=2>%c</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
				else:
					szText = u""

				screen.setLabelAt( szName, attach, szText, 0, 3, iY - 9, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );
				
				iSize = 16
				self.iIncreaseButtonID = 555
				szName = "IncreaseButton%d" %(iPlayerID)
				self.aszIncreaseButtons.append(szName)
				screen.setImageButtonAt( szName, attach, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_PLUS").getPath(), 53, iY + 1, iSize, iSize, WidgetTypes.WIDGET_GENERAL, self.iIncreaseButtonID, iPlayerID );
				self.iDecreaseButtonID = 556
				szName = "DecreaseButton%d" %(iPlayerID)
				self.aszDecreaseButtons.append(szName)
				screen.setImageButtonAt( szName, attach, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_MINUS").getPath(), 68, iY + 1, iSize, iSize, WidgetTypes.WIDGET_GENERAL, self.iDecreaseButtonID, iPlayerID );
				
				
				iPlayerLoop += 1
		
			for iPlayerID in self.aiUnknownPlayers:
				attach = "EmptyLeaderContainer%d" % (iPlayerID)
				screen.attachPanel(self.szScrollPanel, attach, "", "", True, False, PanelStyles.PANEL_STYLE_STANDARD)
				screen.attachSeparator(attach, "EmptyLeaderImageA%d" %(iPlayerID), true, 30)

	def getMultiplierAgainstTarget(self, iTargetPlayer=-1):
		
		szMultiplier = ""
		
		if (iTargetPlayer == -1):
			iTargetPlayer = self.iTargetPlayer
		
		pActivePlayer = gc.getPlayer(self.iActivePlayer)
		pActiveTeam = gc.getTeam(pActivePlayer.getTeam())
		pTargetPlayer = gc.getPlayer(iTargetPlayer)
		pTargetTeam = gc.getTeam(pTargetPlayer.getTeam())
		
		szMultiplier = localText.getText("TXT_KEY_ESPIONAGE_COST", (getEspionageModifier(pActivePlayer.getTeam(), pTargetPlayer.getTeam()), ))
			
		if (pActiveTeam.getCounterespionageTurnsLeftAgainstTeam(pTargetPlayer.getTeam()) > 0):
			szMultiplier += u"*"
		
		if (pTargetTeam.getCounterespionageTurnsLeftAgainstTeam(pActivePlayer.getTeam()) > 0):
			szMultiplier += u"+"
		
		return szMultiplier
		
	def refreshScreen(self):
		
		self.deleteAllWidgets()

		if (self.iTargetPlayer != -1):
						
			# Create a new screen, called EspionageAdvisor, using the file EspionageAdvisor.py for input
			screen = self.getScreen()
			
			pActivePlayer = gc.getPlayer(self.iActivePlayer)
			pActiveTeam = gc.getTeam(pActivePlayer.getTeam())
			
			iPlayerLoop = 0
			
			for iPlayerID in self.aiKnownPlayers:
				
				iX = 0
				iY = 15 #+ (148 * iPlayerLoop)#(110 * iPlayerLoop)
				
				pTargetPlayer = gc.getPlayer(iPlayerID)
				iTargetTeam = pTargetPlayer.getTeam()
				
				attach = "LeaderContainer%d" % (iPlayerID)
				
				szName = "SpendingText%d" %(iPlayerID)
				self.aszSpendingTexts.append(szName)
				szText = u"<font=2>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_SPENDING_WEIGHT", ()) + ": %d</font>" %(pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam))
				screen.deleteWidget(szName)
				screen.setLabelAt( szName, attach, szText, 0, 85, iY, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );
				
				szName = "AmountText%d" %(iPlayerID)

				if (pActivePlayer.getEspionageSpending(iTargetTeam) > 0):
					szText = u"<font=2><color=0,255,0,0>%s</color></font>" %(localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS_PER_TURN", (pActivePlayer.getEspionageSpending(iTargetTeam), )))
				else:
					szText = u"<font=2><color=192,0,0,0>%s</color></font>" %(localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS_PER_TURN", (pActivePlayer.getEspionageSpending(iTargetTeam), )))

				screen.deleteWidget(szName)
				#Rhye
				#screen.setLabelAt( szName, attach, szText, 0, 247, iY - 1, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );
				screen.setLabelAt( szName, attach, szText, 0, 281, iY - 1, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

				szName = "SpendingIcon%d" %(iPlayerID)
				if (pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam) > 0):
					szText = u"<font=2>%c</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
				else:
					szText = u""

				screen.deleteWidget(szName)
				screen.setLabelAt( szName, attach, szText, 0, 3, iY - 9, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );
								

				iPlayerLoop += 1
			
			# Is there any other players which have been met?
			if (self.iTargetPlayer != -1):
				
				pTargetPlayer = gc.getPlayer(self.iTargetPlayer)
				pyTargetPlayer = PyPlayer(self.iTargetPlayer)
				
				# List of Cities
				self.szCityListBox = self.getNextWidgetName()
				screen.addListBoxGFC(self.szCityListBox, "", self.X_CITY_LIST, self.Y_CITY_LIST, self.W_CITY_LIST, self.H_CITY_LIST, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(self.szCityListBox, True)
				screen.setStyle(self.szCityListBox, "Table_StandardCiv_Style")
				
				# Loop through target's cities, see which are visible and add them to the list
				apCityList = pyTargetPlayer.getCityList()
				
				iLoop = 0
				
				for pyCity in apCityList:
					
					pCity = pyCity.GetCy()
					
					if (pCity.isRevealed(pActivePlayer.getTeam(), false)):
						screen.appendListBoxString( self.szCityListBox, pCity.getName(), WidgetTypes.WIDGET_GENERAL, pCity.getID(), 0, CvUtil.FONT_LEFT_JUSTIFY )
						
						if (self.iActiveCityID == -1 or pTargetPlayer.getCity(self.iActiveCityID).isNone()):
							self.iActiveCityID = pCity.getID()
							
						if (self.iActiveCityID == pCity.getID()):
							screen.setSelectedListBoxStringGFC(self.szCityListBox, iLoop)
						
						iLoop += 1
						
				#screen.updateListBox(self.szCityListBox)
				
				self.W_TABLE_0 = self.W_EFFECTS_LIST
				self.W_TABLE_1 = 0
				self.W_TABLE_2 = self.W_EFFECTS_COSTS_LIST
				self.W_TABLE_3 = 20
				
				szEffectsTable = self.getNextWidgetName()
				szHelpText = localText.getText("TXT_KEY_ESPIONAGE_PASSIVE_AUTOMATIC", ())
				screen.addTableControlGFCWithHelp(szEffectsTable, 4, self.X_EFFECTS_LIST, self.Y_EFFECTS_LIST, self.W_EFFECTS_LIST + self.W_EFFECTS_COSTS_LIST + self.W_TABLE_1 + self.W_TABLE_3, self.H_EFFECTS_LIST, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD, szHelpText)
				screen.setTableColumnHeader(szEffectsTable, 0, "", self.W_TABLE_0)
				screen.setTableColumnHeader(szEffectsTable, 1, "", self.W_TABLE_1)
				screen.setTableColumnHeader(szEffectsTable, 2, "", self.W_TABLE_2)
				screen.setTableColumnHeader(szEffectsTable, 3, "", self.W_TABLE_3)
				
				szMissionsTable = self.getNextWidgetName()
				szHelpText = localText.getText("TXT_KEY_ESPIONAGE_MISSIONS_SPY", ())
				screen.addTableControlGFCWithHelp(szMissionsTable, 4, self.X_MISSIONS_LIST, self.Y_MISSIONS_LIST, self.W_MISSIONS_LIST + self.W_MISSIONS_COSTS_LIST + self.W_TABLE_1 + self.W_TABLE_3, self.H_MISSIONS_LIST, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD, szHelpText)
				screen.setTableColumnHeader(szMissionsTable, 0, "", self.W_TABLE_0)
				screen.setTableColumnHeader(szMissionsTable, 1, "", self.W_TABLE_1)
				screen.setTableColumnHeader(szMissionsTable, 2, "", self.W_TABLE_2)
				screen.setTableColumnHeader(szMissionsTable, 3, "", self.W_TABLE_3)
												
								
				# Loop through all Missions
				for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
					
					pMission = gc.getEspionageMissionInfo(iMissionLoop)
					
					if (pMission.getCost() != -1):
						
						# Only passive effects
						if (pMission.isPassive()):
							
							pPlot = None
							
							if (self.iActiveCityID != -1 and pMission.isTargetsCity()):
								
								pActiveCity = gc.getPlayer(self.iTargetPlayer).getCity(self.iActiveCityID)
								pPlot = pActiveCity.plot()
								
							
							if (self.iActiveCityID != -1 or not pMission.isTargetsCity()):
								
								iCost = pActivePlayer.getEspionageMissionCost(iMissionLoop, self.iTargetPlayer, pPlot, -1)
								
								szTechText = ""
								if (pMission.getTechPrereq() != -1):
									szTechText = " (%s)" %(gc.getTechInfo(pMission.getTechPrereq()).getDescription())
									
								szText = pMission.getDescription() + szTechText
								
								if (pMission.getTechPrereq() != -1):
									pTeam = gc.getTeam(pActivePlayer.getTeam())
									if (not pTeam.isHasTech(pMission.getTechPrereq())):
										szText = u"<color=255,0,0,0>%s</color>" %(szText)
																
								iRow = screen.appendTableRow(szEffectsTable)
								screen.setTableText(szEffectsTable, 0, iRow, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
								screen.setTableText(szEffectsTable, 2, iRow, str(iCost), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
									
						# Active Mission
						else:
							
							if (self.iSelectedMission == -1):
								self.iSelectedMission = iMissionLoop
							
							pPlot = -1
							if (self.iActiveCityID != -1):
								pPlot = pActiveCity.plot()
							else:
								pPlot = None
							
							iCost = pActivePlayer.getEspionageMissionCost(iMissionLoop, self.iTargetPlayer, pPlot, -1)
							
							szTechText = ""
							if (pMission.getTechPrereq() != -1):
								szTechText = " (%s)" %(gc.getTechInfo(pMission.getTechPrereq()).getDescription())
								
							szText = pMission.getDescription() + szTechText
							
							if (pMission.getTechPrereq() != -1):
								pTeam = gc.getTeam(pActivePlayer.getTeam())
								if (not pTeam.isHasTech(pMission.getTechPrereq())):
									szText = u"<color=255,0,0,0>%s</color>" %(szText)
														
							iRow = screen.appendTableRow(szMissionsTable)
							screen.setTableText(szMissionsTable, 0, iRow, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							if iCost > 0:
								screen.setTableText(szMissionsTable, 2, iRow, str(iCost), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
							
		return 0
		
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
			
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		'Calls function mapped in EspionageAdvisorInputMap'
		
		screen = self.getScreen()		
		pActivePlayer = gc.getPlayer(self.iActivePlayer)
		
		##### Debug Dropdown #####
		if (CyGame().isDebugMode()):
			if (inputClass.getFunctionName() == self.DEBUG_DROPDOWN_ID):
				iIndex = screen.getSelectedPullDownID(self.DEBUG_DROPDOWN_ID)
				self.iActivePlayer = screen.getPullDownData(self.DEBUG_DROPDOWN_ID, iIndex)
				self.drawContents()
				CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)
		
		if (self.iTargetPlayer != -1):
			
			##### Player Images #####
			if (inputClass.getData1() == self.iLeaderImagesID):
				
				self.iTargetPlayer = inputClass.getData2()
				
				# Loop through all images
				for iPlayerID in self.aiKnownPlayers:
					szName = "LeaderImage%d" %(iPlayerID)
					if (self.iTargetPlayer == iPlayerID):
						screen.setState(szName, true)
					else:
						screen.setState(szName, false)
					
					self.iActiveCityID = -1
						
				CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)
				
				
			##### City Listbox #####
			if ("%s%d" %(inputClass.getFunctionName(), inputClass.getID()) == self.szCityListBox):
				iCityID = inputClass.getData1()
				self.iActiveCityID = iCityID#gc.getPlayer(self.iTargetPlayer).getCity(iCityID)
				CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)
				
			# Is there any other players which have been met?
			if (self.iTargetPlayer != -1):
				
				##### Increase Button #####
				if (inputClass.getData1() == self.iIncreaseButtonID):
					
					iPlayerID = inputClass.getData2()
					iTargetTeam = gc.getPlayer(iPlayerID).getTeam()
					
					CyMessageControl().sendEspionageSpendingWeightChange(iTargetTeam, 1)
					
					if (pActivePlayer.getEspionageSpending(iTargetTeam) > 0):
						szText = u"<font=2><color=0,255,0,0>%s</color></font>" %(localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS_PER_TURN", (pActivePlayer.getEspionageSpending(iTargetTeam), )))
					else:
						szText = u"<font=2><color=192,0,0,0>%s</color></font>" %(localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS_PER_TURN", (pActivePlayer.getEspionageSpending(iTargetTeam), )))

					screen.setLabelAt( "AmountText%d" %(iPlayerID), "LeaderContainer%d" % (iPlayerID), szText, 0, 247, 15 - 1, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

					if (pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam) > 0):
						szText = u"<font=2>%c</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
					else:
						szText = u""
					attach = "LeaderContainer%d" % (iPlayerID)
					iY = 15
					screen.setLabelAt( "SpendingIcon%d" %(iPlayerID), attach, szText, 0, 3, iY - 9, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );
					
					CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)
					
				##### Decrease Button #####
				elif (inputClass.getData1() == self.iDecreaseButtonID):
					
					iPlayerID = inputClass.getData2()
					iTargetTeam = gc.getPlayer(iPlayerID).getTeam()
					
					if (pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam) > 0):	# Can't reduce weight below 0
						
						CyMessageControl().sendEspionageSpendingWeightChange(iTargetTeam, -1)
						
						if (pActivePlayer.getEspionageSpending(iTargetTeam) > 0):
							szText = u"<font=2><color=0,255,0,0>%s</color></font>" %(localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS_PER_TURN", (pActivePlayer.getEspionageSpending(iTargetTeam), )))
						else:
							szText = u"<font=2><color=192,0,0,0>%s</color></font>" %(localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS_PER_TURN", (pActivePlayer.getEspionageSpending(iTargetTeam), )))

						screen.setLabelAt( "AmountText%d" %(iPlayerID), "LeaderContainer%d" % (iPlayerID), szText, 0, 247, 15 - 1, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

						if (pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam) > 0):
							szText = u"<font=2>%c</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
						else:
							szText = u""
						attach = "LeaderContainer%d" % (iPlayerID)
						iY = 15
						screen.setLabelAt( "SpendingIcon%d" %(iPlayerID), attach, szText, 0, 3, iY - 9, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );
						
						CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)
		
		return 0

	def update(self, fDelta):
		if (CyInterface().isDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT) == True):
			CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, False)
			self.refreshScreen()
		return
											
