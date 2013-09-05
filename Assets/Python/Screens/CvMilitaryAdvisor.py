## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import time
import PyHelpers
import re
import Consts as con #Rhye

PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvMilitaryAdvisor:
	"Military Advisor"

	def __init__(self, screenId):
		self.screenId = screenId
		self.MILITARY_SCREEN_NAME = "MilitaryAdvisor"
		self.BACKGROUND_ID = "MilitaryAdvisorBackground"
		self.EXIT_ID = "MilitaryAdvisorExitWidget"

		self.WIDGET_ID = "MilitaryAdvisorWidget"
		self.REFRESH_WIDGET_ID = "MilitaryAdvisorRefreshWidget"
		self.ATTACH_WIDGET_ID = "MilitaryAdvisorAttachWidget"
		self.SELECTION_WIDGET_ID = "MilitaryAdvisorSelectionWidget"
		self.ATTACHED_WIDGET_ID = "MilitaryAdvisorAttachedWidget" # no need to explicitly delete these
		self.LEADER_BUTTON_ID = "MilitaryAdvisorLeaderButton"
		self.UNIT_PANEL_ID = "MilitaryAdvisorUnitPanel"
		self.UNIT_BUTTON_ID = "MilitaryAdvisorUnitButton"
		self.UNIT_BUTTON_LABEL_ID = "MilitaryAdvisorUnitButtonLabel"
		self.LEADER_PANEL_ID = "MilitaryAdvisorLeaderPanel"
		self.UNIT_LIST_ID = "MilitaryAdvisorUnitList"
		self.GREAT_GENERAL_BAR_ID = "MilitaryAdvisorGreatGeneralBar"
		self.GREAT_GENERAL_LABEL_ID = "MilitaryAdvisorGreatGeneralLabel"

		self.Z_BACKGROUND = -2.1
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
		
		self.X_GREAT_GENERAL_BAR = 20
		self.Y_GREAT_GENERAL_BAR = 730
		self.W_GREAT_GENERAL_BAR = 300
		self.H_GREAT_GENERAL_BAR = 30
								
		self.nWidgetCount = 0
		self.nRefreshWidgetCount = 0
		self.nAttachedWidgetCount = 0
		self.iActivePlayer = -1
		self.selectedPlayerList = []
		self.selectedGroupList = []
		self.selectedUnitList = []
		
		self.X_MAP = 20
		self.Y_MAP = 190
		self.W_MAP = 580
		self.H_MAP_MAX = 500
		self.MAP_MARGIN = 20
		
		self.X_TEXT = 625
		self.Y_TEXT = 190
		self.W_TEXT = 380
		self.H_TEXT = 500
						
		self.X_LEADERS = 20
		self.Y_LEADERS = 80
		self.W_LEADERS = 985
		self.H_LEADERS = 90
		self.LEADER_BUTTON_SIZE = 64
		self.LEADER_MARGIN = 12
		
		self.LEADER_COLUMNS = int(self.W_LEADERS / (self.LEADER_BUTTON_SIZE + self.LEADER_MARGIN))
		self.bUnitDetails = False
		self.iShiftKeyDown = 0
		
						
	def getScreen(self):
		return CyGInterfaceScreen(self.MILITARY_SCREEN_NAME, self.screenId)

	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()
										
	# Screen construction function
	def interfaceScreen(self):
							
		# Create a new screen
		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.EXIT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"
		self.TITLE = u"<font=4b>" + localText.getText("TXT_KEY_MILITARY_ADVISOR_TITLE", ()).upper() + "</font>"

		self.nWidgetCount = 0
	
		# Set the background and exit button, and show the screen
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.showWindowBackground(False)
		screen.setText(self.EXIT_ID, "Background", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
												
		# Header...
		self.szHeader = self.getNextWidgetName()
		screen.setText(self.szHeader, "Background", self.TITLE, CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Minimap initialization
		self.H_MAP = (self.W_MAP * CyMap().getGridHeight()) / CyMap().getGridWidth()
		if (self.H_MAP > self.H_MAP_MAX):
			self.W_MAP = (self.H_MAP_MAX * CyMap().getGridWidth()) / CyMap().getGridHeight()
			self.H_MAP = self.H_MAP_MAX
		screen.addPanel("", u"", "", False, False, self.X_MAP, self.Y_MAP, self.W_MAP, self.H_MAP, PanelStyles.PANEL_STYLE_MAIN)
		screen.initMinimap(self.X_MAP + self.MAP_MARGIN, self.X_MAP + self.W_MAP - self.MAP_MARGIN, self.Y_MAP + self.MAP_MARGIN, self.Y_MAP + self.H_MAP - self.MAP_MARGIN, self.Z_CONTROLS)
		screen.updateMinimapSection(False, False)

		screen.updateMinimapColorFromMap(MinimapModeTypes.MINIMAPMODE_TERRITORY, 0.3)

		screen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_MILITARY)
		
		iOldMode = CyInterface().getShowInterface()
		CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_MINIMAP_ONLY)
		screen.updateMinimapVisibility()
		CyInterface().setShowInterface(iOldMode)
					
		self.iActivePlayer = gc.getGame().getActivePlayer()

		self.unitsList = [(0, 0, [], 0)] * gc.getNumUnitInfos()
		self.selectedUnitList = []
		self.selectedPlayerList.append(self.iActivePlayer)

		self.drawCombatExperience()

		self.refresh(true)
		
	def drawCombatExperience(self):
	
		if (gc.getPlayer(self.iActivePlayer).greatPeopleThreshold(true) > 0):
		
			iExperience = gc.getPlayer(self.iActivePlayer).getCombatExperience()
			
			screen = self.getScreen()
			screen.addStackedBarGFC(self.GREAT_GENERAL_BAR_ID, self.X_GREAT_GENERAL_BAR, self.Y_GREAT_GENERAL_BAR, self.W_GREAT_GENERAL_BAR, self.H_GREAT_GENERAL_BAR, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)
			screen.setStackedBarColors(self.GREAT_GENERAL_BAR_ID, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED"))
			screen.setStackedBarColors(self.GREAT_GENERAL_BAR_ID, InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE"))
			screen.setStackedBarColors(self.GREAT_GENERAL_BAR_ID, InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
			screen.setStackedBarColors(self.GREAT_GENERAL_BAR_ID, InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
			screen.setBarPercentage(self.GREAT_GENERAL_BAR_ID, InfoBarTypes.INFOBAR_STORED, float(iExperience) / float(gc.getPlayer(self.iActivePlayer).greatPeopleThreshold(true)))
			screen.setLabel(self.GREAT_GENERAL_LABEL_ID, "", localText.getText("TXT_KEY_MISC_COMBAT_EXPERIENCE", ()), CvUtil.FONT_CENTER_JUSTIFY, self.X_GREAT_GENERAL_BAR + self.W_GREAT_GENERAL_BAR/2, self.Y_GREAT_GENERAL_BAR + 6, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)
					
																									
	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName
																	
	def resetMinimapColor(self):
		screen = self.getScreen()
		for iX in range(gc.getMap().getGridWidth()):
			for iY in range(gc.getMap().getGridHeight()):
				screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_MILITARY, iX, iY, -1, 0.6)
																				
	# handle the input for this screen...
	def handleInput (self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == self.UNIT_BUTTON_ID) :
			self.bUnitDetails = not self.bUnitDetails
			self.refreshUnitSelection(True)
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER):
			if (inputClass.getData() == int(InputTypes.KB_LSHIFT) or inputClass.getData() == int(InputTypes.KB_RSHIFT)):
				self.iShiftKeyDown = inputClass.getID() 
		
		return 0

	def update(self, fDelta):
		screen = self.getScreen()
		screen.updateMinimap(fDelta)

	def minimapClicked(self):
		self.hideScreen()
						
	def isSelectedGroup(self, iGroup, bIndirect):
		if (bIndirect):
			if -1 in self.selectedGroupList:
				return True
			if iGroup == -1:
				return False
		return ((iGroup + gc.getNumUnitInfos()) in self.selectedGroupList)
				
	def isSelectedUnitType(self, iUnit, bIndirect):
		if (bIndirect):
			if -1 in self.selectedGroupList:
				return True
			if self.isSelectedGroup(gc.getUnitInfo(iUnit).getUnitCombatType(), True):
				return True
		return (iUnit in self.selectedGroupList)
		
	def isSelectedUnit(self, iPlayer, iUnitId, bIndirect):
		if (bIndirect):
			if -1 in self.selectedGroupList:
				return True
			unit = gc.getPlayer(iPlayer).getUnit(iUnitId)
			if self.isSelectedGroup(gc.getUnitInfo(unit.getUnitType()).getUnitCombatType(), True):
				return True
			if self.isSelectedUnitType(unit.getUnitType(), True):
				return True
		return ((iPlayer, iUnitId) in self.selectedUnitList)
		
	def refreshSelectedLeader(self, iPlayer):
		if self.iShiftKeyDown == 1:
			if (iPlayer in self.selectedPlayerList):
				self.selectedPlayerList.remove(iPlayer)
			else:
				self.selectedPlayerList.append(iPlayer)
		else:
			self.selectedPlayerList = []
			self.selectedPlayerList.append(iPlayer)	
	
		self.refresh(True)
				
	def getLeaderButton(self, iPlayer):
		szName = self.LEADER_BUTTON_ID + str(iPlayer)
		return szName

	def refreshSelectedGroup(self, iSelected):
		if (iSelected in self.selectedGroupList):
			self.selectedGroupList.remove(iSelected)
		else:
			self.selectedGroupList.append(iSelected)
		self.refreshUnitSelection(false)
			
	def refreshSelectedUnit(self, iPlayer, iUnitId):
		selectedUnit = (iPlayer, iUnitId)
		if (selectedUnit in self.selectedUnitList):
			self.selectedUnitList.remove(selectedUnit)
		else:
			self.selectedUnitList.append(selectedUnit)
		self.refreshUnitSelection(false)		
	
	def refreshUnitSelection(self, bReload):
		screen = self.getScreen()
		
		screen.minimapClearAllFlashingTiles()

		if (bReload):
			if (self.bUnitDetails):
				screen.setButtonGFC(self.UNIT_BUTTON_ID, u"", "", self.X_TEXT + self.MAP_MARGIN, self.Y_TEXT + self.MAP_MARGIN/2, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
				screen.setLabel(self.UNIT_BUTTON_LABEL_ID, "", localText.getText("TXT_KEY_MILITARY_ADVISOR_UNIT_TOGGLE_OFF", ()), CvUtil.FONT_LEFT_JUSTIFY, self.X_TEXT + self.MAP_MARGIN + 22, self.Y_TEXT + self.MAP_MARGIN/2 + 2, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				screen.setButtonGFC(self.UNIT_BUTTON_ID, u"", "", self.X_TEXT + self.MAP_MARGIN, self.Y_TEXT + self.MAP_MARGIN/2, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS )
				screen.setLabel(self.UNIT_BUTTON_LABEL_ID, "", localText.getText("TXT_KEY_MILITARY_ADVISOR_UNIT_TOGGLE_ON", ()), CvUtil.FONT_LEFT_JUSTIFY, self.X_TEXT + self.MAP_MARGIN + 22, self.Y_TEXT + self.MAP_MARGIN/2 + 2, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# self.unitsList[iUnit][0] is the UnitCombatGroup (e.g. Melee)
		# self.unitsList[iUnit][1] is the unit type (e.g. Warrior)
		# self.unitsList[iUnit][2] is a list of the active player's actual units
		# self.unitsList[iUnit][3] is the total number of those units seen by the active player (not only his own)
		
		if bReload:
			for iUnit in range(gc.getNumUnitInfos()):
				self.unitsList[iUnit] = (gc.getUnitInfo(iUnit).getUnitCombatType(), iUnit, [], 0)

			for iPlayer in range(gc.getMAX_PLAYERS()):			
				player = PyPlayer(iPlayer)
				if (player.isAlive()):
					unitList = player.getUnitList()
					for loopUnit in unitList:
						unitType = loopUnit.getUnitType()
						
						bVisible = False
						plot = loopUnit.plot()
						if (not plot.isNone()):
							bVisible = plot.isVisible(gc.getPlayer(self.iActivePlayer).getTeam(), False) and not loopUnit.isInvisible(gc.getPlayer(self.iActivePlayer).getTeam(), False)

						if unitType >= 0 and unitType < gc.getNumUnitInfos() and bVisible:
							iNumUnits = self.unitsList[unitType][3]
							if (iPlayer == self.iActivePlayer):
								iNumUnits += 1
							if loopUnit.getVisualOwner() in self.selectedPlayerList:
								self.unitsList[unitType][2].append(loopUnit)							
							
							self.unitsList[unitType] = (self.unitsList[unitType][0], self.unitsList[unitType][1], self.unitsList[unitType][2], iNumUnits)

			# sort by unit combat type
			self.unitsList.sort()
		
		szText = localText.getText("TXT_KEY_PEDIA_ALL_UNITS", ()).upper()
		if (-1 in self.selectedGroupList):
			szText = localText.changeTextColor(u"<u>" + szText + u"</u>", gc.getInfoTypeForString("COLOR_YELLOW"))
		if (bReload):
			screen.addListBoxGFC(self.UNIT_LIST_ID, "", self.X_TEXT+self.MAP_MARGIN, self.Y_TEXT+self.MAP_MARGIN+15, self.W_TEXT-2*self.MAP_MARGIN, self.H_TEXT-2*self.MAP_MARGIN-15, TableStyles.TABLE_STYLE_STANDARD)
			screen.enableSelect(self.UNIT_LIST_ID, False)
			screen.setStyle(self.UNIT_LIST_ID, "Table_StandardCiv_Style")
			screen.appendListBoxString(self.UNIT_LIST_ID, szText, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		else:		
			screen.setListBoxStringGFC(self.UNIT_LIST_ID, 0, szText, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		iPrevUnitCombat = -2
		iItem = 1
		for iUnit in range(gc.getNumUnitInfos()):
			if (len(self.unitsList[iUnit][2]) > 0):
				if (iPrevUnitCombat != self.unitsList[iUnit][0] and self.unitsList[iUnit][0] != -1):
					iPrevUnitCombat = self.unitsList[iUnit][0]
					szDescription = gc.getUnitCombatInfo(self.unitsList[iUnit][0]).getDescription().upper()
					if (self.isSelectedGroup(self.unitsList[iUnit][0], False)):
						szDescription = u"   <u>" + szDescription + u"</u>"
					else:
						szDescription = u"   " + szDescription
					if (self.isSelectedGroup(self.unitsList[iUnit][0], True)):
						szDescription = localText.changeTextColor(szDescription, gc.getInfoTypeForString("COLOR_YELLOW"))
					if (bReload):
						screen.appendListBoxString(self.UNIT_LIST_ID, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, self.unitsList[iUnit][0] + gc.getNumUnitInfos(), CvUtil.FONT_LEFT_JUSTIFY)
					else:
						screen.setListBoxStringGFC(self.UNIT_LIST_ID, iItem, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, self.unitsList[iUnit][0] + gc.getNumUnitInfos(), CvUtil.FONT_LEFT_JUSTIFY)
					iItem += 1
				
				szDescription = gc.getUnitInfo(self.unitsList[iUnit][1]).getDescription() + u" (" + unicode(len(self.unitsList[iUnit][2])) + u")"
				if (self.isSelectedUnitType(self.unitsList[iUnit][1], False)):
					szDescription = u"      <u>" + szDescription + u"</u>"
				else:
					szDescription = u"      " + szDescription
				if (self.isSelectedUnitType(self.unitsList[iUnit][1], True)):
					szDescription = localText.changeTextColor(szDescription, gc.getInfoTypeForString("COLOR_YELLOW"))
				if (bReload):
					screen.appendListBoxString(self.UNIT_LIST_ID, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, self.unitsList[iUnit][1], CvUtil.FONT_LEFT_JUSTIFY)
				else:
					screen.setListBoxStringGFC(self.UNIT_LIST_ID, iItem, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, self.unitsList[iUnit][1], CvUtil.FONT_LEFT_JUSTIFY)
				iItem += 1
				
				for loopUnit in self.unitsList[iUnit][2]:
				
					if (self.bUnitDetails):
						szDescription = CyGameTextMgr().getSpecificUnitHelp(loopUnit, true, false)

						listMatches = re.findall("<.*?color.*?>", szDescription)	
						for szMatch in listMatches:
							szDescription = szDescription.replace(szMatch, u"")
						
						if (loopUnit.isWaiting()):
							szDescription = '*' + szDescription
							
						if (self.isSelectedUnit(loopUnit.getOwner(), loopUnit.getID(), False)):
							szDescription = u"         <u>" + szDescription + u"</u>"
						else:
							szDescription = u"         " + szDescription

						if (self.isSelectedUnit(loopUnit.getOwner(), loopUnit.getID(), True)):
							szDescription = localText.changeTextColor(szDescription, gc.getInfoTypeForString("COLOR_YELLOW"))

						if (bReload):
							screen.appendListBoxString(self.UNIT_LIST_ID, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, -loopUnit.getOwner(), loopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						else:
							screen.setListBoxStringGFC(self.UNIT_LIST_ID, iItem, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, -loopUnit.getOwner(), loopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						iItem += 1

					iPlayer = loopUnit.getVisualOwner()
					player = PyPlayer(iPlayer)
					iColor = gc.getPlayerColorInfo(gc.getPlayer(iPlayer).getPlayerColor()).getColorTypePrimary()
					screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_MILITARY, loopUnit.getX(), loopUnit.getY(), iColor, 0.6)
					if (self.isSelectedUnit(loopUnit.getOwner(), loopUnit.getID(), True) and (iPlayer in self.selectedPlayerList)):
						
						if (player.getTeam().isAtWar(gc.getPlayer(self.iActivePlayer).getTeam())):
							iColor = gc.getInfoTypeForString("COLOR_RED")
						elif (gc.getPlayer(iPlayer).getTeam() != gc.getPlayer(self.iActivePlayer).getTeam()):
							iColor = gc.getInfoTypeForString("COLOR_YELLOW")
						else:
							iColor = gc.getInfoTypeForString("COLOR_WHITE")
						screen.minimapFlashPlot(loopUnit.getX(), loopUnit.getY(), iColor, -1)

					
	
	def refresh(self, bReload):
	
		if (self.iActivePlayer < 0):
			return
						
		screen = self.getScreen()
				
		if (bReload):
			# Set scrollable area for unit buttons
			screen.addPanel(self.UNIT_PANEL_ID, "", "", True, True, self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_MAIN)
			
			# Set scrollable area for leaders
			screen.addPanel(self.LEADER_PANEL_ID, "", "", False, True, self.X_LEADERS, self.Y_LEADERS, self.W_LEADERS, self.H_LEADERS, PanelStyles.PANEL_STYLE_MAIN)

		listLeaders = []
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			player = gc.getPlayer(iLoopPlayer)
			#Rhye - to hide the independents switch the comments
			if (player.isAlive() and (gc.getTeam(player.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam()) or gc.getGame().isDebugMode())):
			#if (player.isAlive() and player.getID() != con.iIndependent and player.getID() != con.iIndependent2 and (gc.getTeam(player.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam()) or gc.getGame().isDebugMode())):
				listLeaders.append(iLoopPlayer)
	    
					
		iNumLeaders = len(listLeaders)
		if iNumLeaders >= self.LEADER_COLUMNS:
			iButtonSize = self.LEADER_BUTTON_SIZE / 2
		else:
			iButtonSize = self.LEADER_BUTTON_SIZE

		iColumns = int(self.W_LEADERS / (iButtonSize + self.LEADER_MARGIN))

		# loop through all players and display leaderheads
		for iIndex in range(iNumLeaders):
			iLoopPlayer = listLeaders[iIndex]
			player = gc.getPlayer(iLoopPlayer)
			
			x = self.X_LEADERS + self.LEADER_MARGIN + (iIndex % iColumns) * (iButtonSize + self.LEADER_MARGIN)
			y = self.Y_LEADERS + self.LEADER_MARGIN + (iIndex // iColumns) * (iButtonSize + self.LEADER_MARGIN)

			if (bReload):
				if player.isBarbarian():
					szButton = "Art/Interface/Buttons/Civilizations/Barbarian.dds"
				else:
					#szButton = gc.getLeaderHeadInfo(gc.getPlayer(iLoopPlayer).getLeaderType()).getButton() #Rhye
					szButton = gc.getCivilizationInfo(gc.getPlayer(iLoopPlayer).getCivilizationType()).getButton() #Rhye
				screen.addCheckBoxGFC(self.getLeaderButton(iLoopPlayer), szButton, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), x, y, iButtonSize, iButtonSize, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 2, iLoopPlayer, ButtonStyles.BUTTON_STYLE_LABEL)
				screen.setState(self.getLeaderButton(iLoopPlayer), (iLoopPlayer in self.selectedPlayerList))				
		
		self.refreshUnitSelection(bReload)
		
		
		
		
		
