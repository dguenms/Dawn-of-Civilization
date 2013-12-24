## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvScreensInterface
import Consts as con

TEXTURE_SIZE = 24
X_START = 6
X_INCREMENT = 27
Y_ROW = 32

CIV_HAS_TECH = 0
CIV_IS_RESEARCHING = 1
CIV_NO_RESEARCH = 2
CIV_TECH_AVAILABLE = 3

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

# BUG - GP Tech Prefs - start
import TechPrefs
import BugCore
BugOpt = BugCore.game.Advisors
ClockOpt = BugCore.game.NJAGC

import BugUtil

PREF_ICON_SIZE = 24
PREF_ICON_TOP = 168
PREF_ICON_LEFT = 10

FLAVORS = [ TechPrefs.FLAVOR_PRODUCTION, TechPrefs.FLAVOR_GOLD, TechPrefs.FLAVOR_SCIENCE,
			TechPrefs.FLAVOR_CULTURE, TechPrefs.FLAVOR_RELIGION ]
UNIT_CLASSES = [ "UNITCLASS_ENGINEER", "UNITCLASS_MERCHANT", "UNITCLASS_SCIENTIST",
				 "UNITCLASS_ARTIST", "UNITCLASS_PROPHET" ]
# BUG - GP Tech Prefs - end

# BUG - 3.19 No Espionage - start
import GameUtil
# BUG - 3.19 No Espionage - end

# BUG - Mac Support - start
BugUtil.fixSets(globals())
# BUG - Mac Support - end

# BUG - Tech Era Colors - start
def getEraDescription(eWidgetType, iData1, iData2, bOption):
	return gc.getEraInfo(iData1).getDescription()
# BUG - Tech Era Colors - end

# BUG - GP Tech Prefs - start
def resetTechPrefs(args=[]):
	CvScreensInterface.techChooser.resetTechPrefs()

def getAllTechPrefsHover(widgetType, iData1, iData2, bOption):
	return buildTechPrefsHover("TXT_KEY_BUG_TECH_PREFS_ALL", CvScreensInterface.techChooser.pPrefs.getAllFlavorTechs(iData1))

def getCurrentTechPrefsHover(widgetType, iData1, iData2, bOption):
	return buildTechPrefsHover("TXT_KEY_BUG_TECH_PREFS_CURRENT", CvScreensInterface.techChooser.pPrefs.getCurrentFlavorTechs(iData1))

def getFutureTechPrefsHover(widgetType, iData1, iData2, bOption):
	pPlayer = gc.getPlayer(CvScreensInterface.techChooser.iCivSelected)
	sTechs = set()
	for i in range(gc.getNumTechInfos()):
		if (pPlayer.isResearchingTech(i)):
			sTechs.add(CvScreensInterface.techChooser.pPrefs.getTech(i))
	return buildTechPrefsHover("TXT_KEY_BUG_TECH_PREFS_FUTURE", CvScreensInterface.techChooser.pPrefs.getCurrentWithFlavorTechs(iData1, sTechs))

def buildTechPrefsHover(key, lTechs):
	szText = BugUtil.getPlainText(key) + "\n"
	for pTech in lTechs:
		szText += "<img=%s size=24></img>" % pTech.getInfo().getButton().replace(" ", "_")
	return szText
# BUG - GP Tech Prefs - end

class CvTechChooser:
	"Tech Chooser Screen"

	def __init__(self):
		self.nWidgetCount = 0
		self.iCivSelected = 0
		self.aiCurrentState = []

		# Advanced Start
		self.m_iSelectedTech = -1
		self.m_bSelectedTechDirty = false
		self.m_bTechRecordsDirty = false

# BUG - GP Tech Prefs - start
		self.bPrefsShowing = False
		self.resetTechPrefs()
# BUG - GP Tech Prefs - end

		self.PIXEL_INCREMENT = 7
		self.BOX_INCREMENT_WIDTH = 27 # Used to be 33 #Should be a multiple of 3...
		self.BOX_INCREMENT_HEIGHT = 9 #Should be a multiple of 3...
		self.BOX_INCREMENT_Y_SPACING = 6 #Should be a multiple of 3...
		self.BOX_INCREMENT_X_SPACING = 9 #Should be a multiple of 3...

	def getScreen(self):
		return CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )

	def hideScreen (self):
		# Get the screen
		screen = self.getScreen()

		# Hide the screen
		screen.hideScreen()

	# Screen construction function
	def interfaceScreen(self):
#		BugUtil.debug("CvTechChooser: interfacescreen")
#		self.timer = BugUtil.Timer("CvTechChooser")

		if ( CyGame().isPitbossHost() ):
			return

		# Create a new screen, called TechChooser, using the file CvTechChooser.py for input
		screen = self.getScreen()
		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.hide("AddTechButton")
		screen.hide("ASPointsLabel")
		screen.hide("SelectedTechLabel")

# BUG - GP Tech Prefs - start
		self.NO_TECH_ART = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
# BUG - GP Tech Prefs - end
			
		if ( CyGame().isDebugMode() ):
			screen.addDropDownBoxGFC( "CivDropDown", 22, 12, 192, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.SMALL_FONT )
			screen.setActivation( "CivDropDown", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )
			for j in range(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString( "CivDropDown", gc.getPlayer(j).getCivilizationShortDescription(0), j, j, False )
		else:
			screen.hide( "CivDropDown" )

		if ( screen.isPersistent() and self.iCivSelected == gc.getGame().getActivePlayer()):
			self.updateTechRecords(false)
			return

		self.nWidgetCount = 0
		self.sWidgets = []

		self.iCivSelected = gc.getGame().getActivePlayer()
		self.aiCurrentState = []
		screen.setPersistent( True )

		# Advanced Start
		if (gc.getPlayer(self.iCivSelected).getAdvancedStartPoints() >= 0):

			self.m_bSelectedTechDirty = true

			self.X_ADD_TECH_BUTTON = 10
			self.Y_ADD_TECH_BUTTON = 731
			self.W_ADD_TECH_BUTTON = 150
			self.H_ADD_TECH_BUTTON = 30
			self.X_ADVANCED_START_TEXT = self.X_ADD_TECH_BUTTON + self.W_ADD_TECH_BUTTON + 20

			szText = localText.getText("TXT_KEY_WB_AS_ADD_TECH", ())
			screen.setButtonGFC( "AddTechButton", szText, "", self.X_ADD_TECH_BUTTON, self.Y_ADD_TECH_BUTTON, self.W_ADD_TECH_BUTTON, self.H_ADD_TECH_BUTTON, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
			screen.hide("AddTechButton")

# BUG - Tech Screen Resolution - start
		if (BugOpt.isWideTechScreen() and screen.getXResolution() > 1024):
			xPanelWidth = screen.getXResolution() - 60
		else:
			xPanelWidth = 1024
		yPanelHeight = 768

		screen.showWindowBackground( False )
		screen.setDimensions((screen.getXResolution() - xPanelWidth) / 2, screen.centerY(0), xPanelWidth, yPanelHeight)
# BUG - Tech Screen Resolution - end

		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, xPanelWidth, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addDDSGFC("TechBG", ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 51, xPanelWidth, yPanelHeight - 96, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, yPanelHeight - 55, xPanelWidth, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.setText( "TechChooserExit", "Background", u"<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, xPanelWidth - 30, yPanelHeight - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setActivation( "TechChooserExit", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )

		# Header...
		szText = u"<font=4>"
		szText = szText + localText.getText("TXT_KEY_TECH_CHOOSER_TITLE", ()).upper()
		szText = szText + u"</font>"
		screen.setLabel( "TechTitleHeader", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xPanelWidth / 2, 8, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Make the scrollable area for the city list...
		if BugOpt.isShowGPTechPrefs():
			iX = 80
			iW = xPanelWidth - 80
		else:
			iX = 0
			iW = xPanelWidth

		self.TabPanels = ["TechList", "TechTrade"]

#		screen.addScrollPanel(self.TabPanels[0], u"", iX, 64, iW, yPanelHeight - 142, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.addScrollPanel(self.TabPanels[0], u"", iX, 56, iW, yPanelHeight - 134, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.setActivation(self.TabPanels[0], ActivationTypes.ACTIVATE_NORMAL )

		screen.addScrollPanel(self.TabPanels[1], u"", 80, 64, xPanelWidth - 80, yPanelHeight - 142, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.setActivation(self.TabPanels[1], ActivationTypes.ACTIVATE_NORMAL )

# BUG - GP Tech Prefs - start
		if BugOpt.isShowGPTechPrefs():
			screen.addPanel("GPTechPref", u"", u"", True, False, 0, 51, 80, yPanelHeight - 95, PanelStyles.PANEL_STYLE_MAIN_WHITE )
# BUG - GP Tech Prefs - end

		# Add the Highlight
		#screen.addDDSGFC( "TechHighlight", ArtFileMgr.getInterfaceArtInfo("TECH_HIGHLIGHT").getPath(), 0, 0, self.getXStart() + 6, 12 + ( self.BOX_INCREMENT_HEIGHT * self.PIXEL_INCREMENT ), WidgetTypes.WIDGET_GENERAL, -1, -1 )
		#screen.hide( "TechHighlight" )

		self.X_SELECT_TAB = 30
		self.X_TRADE_TAB = 165
		self.Y_TABS = 730

		self.sTechSelectTab = self.getNextWidgetName("TechSelectTab")
		self.sTechTradeTab = self.getNextWidgetName("TechTradeTab")
		self.sTechTabID = self.sTechSelectTab

		# reset widget array so that the above never get deleted
		self.nWidgetCount = 0
		self.sWidgets = []

		self.ConstructTabs()

		self.ShowTab()

		return

	def ConstructTabs(self):
#		BugUtil.debug("cvTechChooser: ConstructTabs")

		screen = self.getScreen()

		self.BOX_INCREMENT_WIDTH = 27 # Used to be 33 #Should be a multiple of 3...
		self.DrawTechChooser(screen, self.TabPanels[0], True, True, True, True, True, True)

		self.BOX_INCREMENT_WIDTH = 12 # Used to be 33 #Should be a multiple of 3...
		self.DrawTechChooser(screen, self.TabPanels[1], True, False, True, False, False, True)
		self.BOX_INCREMENT_WIDTH = 27 # Used to be 33 #Should be a multiple of 3...

	def ShowTab(self):
#		BugUtil.debug("cvTechChooser: ShowTab")

		screen = self.getScreen()

		for tp in self.TabPanels:
			screen.hide(tp)

		# remove these 2 lines when we return to multi-tab screen and uncomment out the 10 below.
		screen.show(self.TabPanels[0])
		screen.setFocus(self.TabPanels[0])

#		if(self.sTechTabID == self.sTechSelectTab):
#			screen.setText(self.sTechSelectTab, "", "Tech Select", CvUtil.FONT_LEFT_JUSTIFY, self.X_SELECT_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
#			screen.setText(self.sTechTradeTab, "", "Tech Trade - under development", CvUtil.FONT_LEFT_JUSTIFY, self.X_TRADE_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
#			screen.show(self.TabPanels[0])
#			screen.setFocus(self.TabPanels[0])

#		elif(self.sTechTabID == self.sTechTradeTab):
#			screen.setText(self.sTechSelectTab, "", "Tech Select", CvUtil.FONT_LEFT_JUSTIFY, self.X_SELECT_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
#			screen.setText(self.sTechTradeTab, "", "Tech Trade - under development", CvUtil.FONT_LEFT_JUSTIFY, self.X_TRADE_TAB, self.Y_TABS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
#			screen.show(self.TabPanels[1])
#			screen.setFocus(self.TabPanels[1])


	def DrawTechChooser(self, screen, sPanel, bTechPanel, bTechName, bTechIcon, bTechDetails, bANDPreReq, bORPreReq):
#		BugUtil.debug("cvTechChooser: DrawTechChooser (%s)", sPanel)
#		self.timer.reset()
#		self.timer.start()

		# Place the tech blocks
		self.placeTechs(screen, sPanel, bTechPanel, bTechName, bTechIcon, bTechDetails)

		# Draw the arrows
		self.drawArrows(screen, sPanel, bANDPreReq, bORPreReq)

		self.updateTechPrefs()

		screen.moveToFront( "CivDropDown" )

		screen.moveToFront( "AddTechButton" )

#		self.timer.logSpan("total")

	def placeTechs(self, screen, sPanel, bTechPanel, bTechName, bTechIcon, bTechDetails):
#		BugUtil.debug("cvTechChooser: placeTechs")

		iMaxX = 0
		iMaxY = 0

		if sPanel == self.TabPanels[0]:
			sPanelWidget = ""
		else:
			sPanelWidget = sPanel

		# If we are the Pitboss, we don't want to put up an interface at all
		if ( CyGame().isPitbossHost() ):
			return

		# Go through all the techs
		for i in range(gc.getNumTechInfos()):

			# Create and place a tech in its proper location
			iX = 30 + ( (gc.getTechInfo(i).getGridX() - 1) * ( ( self.BOX_INCREMENT_X_SPACING + self.BOX_INCREMENT_WIDTH ) * self.PIXEL_INCREMENT ) )
			iY = ( gc.getTechInfo(i).getGridY() - 1 ) * ( self.BOX_INCREMENT_Y_SPACING * self.PIXEL_INCREMENT ) + 5
			szTechRecord = sPanelWidget + "TechRecord" + str(i)

			if ( iMaxX < iX + self.getXStart() ):
				iMaxX = iX + self.getXStart()
			if ( iMaxY < iY + ( self.BOX_INCREMENT_HEIGHT * self.PIXEL_INCREMENT ) ):
				iMaxY = iY + ( self.BOX_INCREMENT_HEIGHT * self.PIXEL_INCREMENT )

# BUG - Tech Era Colors - start
			szTechRecordShadow = sPanelWidget + "TechRecordShadow" + str(i)
			iShadowOffset = 9
			screen.attachPanelAt( sPanel, szTechRecordShadow, u"", u"", True, False, PanelStyles.PANEL_STYLE_TECH, iX - 6 + iShadowOffset, iY - 6 + iShadowOffset, self.getXStart() + 6, 12 + ( self.BOX_INCREMENT_HEIGHT * self.PIXEL_INCREMENT ), WidgetTypes.WIDGET_TECH_CHOOSER_ERA, gc.getTechInfo(i).getEra(), -1 )
			self.setTechPanelShadowColor(screen, szTechRecordShadow, gc.getTechInfo(i).getEra())
			screen.hide( szTechRecordShadow )
# BUG - Tech Era Colors - end

			screen.attachPanelAt( sPanel, szTechRecord, u"", u"", True, False, PanelStyles.PANEL_STYLE_TECH, iX - 6, iY - 6, self.getXStart() + 6, 12 + ( self.BOX_INCREMENT_HEIGHT * self.PIXEL_INCREMENT ), WidgetTypes.WIDGET_TECH_TREE, i, -1 )
			screen.setActivation( szTechRecord, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS)
			screen.hide( szTechRecord )

			#reset so that it offsets from the tech record's panel
			iX = 6
			iY = 6

			if ( gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i) ):
				screen.setPanelColor(szTechRecord, 85, 150, 87)
				self.aiCurrentState.append(CIV_HAS_TECH)
			elif ( gc.getPlayer(self.iCivSelected).getCurrentResearch() == i ):
				screen.setPanelColor(szTechRecord, 104, 158, 165)
				self.aiCurrentState.append(CIV_IS_RESEARCHING)
			elif ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
				screen.setPanelColor(szTechRecord, 104, 158, 165)
				self.aiCurrentState.append(CIV_IS_RESEARCHING)
			elif ( gc.getPlayer(self.iCivSelected).canEverResearch(i) ):
				screen.setPanelColor(szTechRecord, 100, 104, 160)
				self.aiCurrentState.append(CIV_NO_RESEARCH)
			else:
				screen.setPanelColor(szTechRecord, 206, 65, 69)
				self.aiCurrentState.append(CIV_TECH_AVAILABLE)

			if bTechName:
				szTechID = sPanelWidget + "TechID" + str(i)
				szTechString = "<font=1>"
				if ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
					szTechString = szTechString + str(gc.getPlayer(self.iCivSelected).getQueuePosition(i)) + ". "
				szTechString += gc.getTechInfo(i).getDescription()
				szTechString = szTechString + "</font>"
				screen.setTextAt( szTechID, szTechRecord, szTechString, CvUtil.FONT_LEFT_JUSTIFY, iX + 6 + X_INCREMENT, iY + 6, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_TECH_TREE, i, -1 )
				screen.setActivation( szTechID, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )

			if bTechIcon:
				szTechButtonID = sPanelWidget + "TechButtonID" + str(i)
				screen.addDDSGFCAt( szTechButtonID, szTechRecord, gc.getTechInfo(i).getButton(), iX + 6, iY + 6, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_TECH_TREE, i, -1, False )

			if bTechDetails:
				self.addIconsToTechPanel(screen, i, X_START, iX, iY, szTechRecord)

			if bTechPanel:
				if BugOpt.isShowTechEra():
					screen.show( szTechRecordShadow )
				else:
					screen.hide( szTechRecordShadow )
				screen.show( szTechRecord )
			else:
				screen.hide( szTechRecordShadow )
				screen.hide( szTechRecord )

		screen.setViewMin( sPanel, iMaxX + 20, iMaxY + 20 )

		return

	def addIconsToTechPanel(self, screen, i, fX, iX, iY, szTechRecord):
#		BugUtil.debug("cvTechChooser: addIconsToTechPanel")

		j = 0
		k = 0

		# Unlockable units...
		for j in range( gc.getNumUnitClassInfos() ):
			eLoopUnit = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(j)
			if (eLoopUnit != -1):
				if (gc.getUnitInfo(eLoopUnit).getPrereqAndTech() == i):
					szUnitButton = self.getNextWidgetName("Unit")
					screen.addDDSGFCAt( szUnitButton, szTechRecord, gc.getPlayer(gc.getGame().getActivePlayer()).getUnitButton(eLoopUnit), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, True )
					fX += X_INCREMENT

		j = 0
		k = 0

		# Unlockable Buildings...
		for j in range(gc.getNumBuildingClassInfos()):
			bTechFound = 0
			eLoopBuilding = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationBuildings(j)
			
			# Leoreth: don't show all embassies
			if eLoopBuilding > con.iNumBuildingsPlague: continue

			if (eLoopBuilding != -1):
				if (gc.getBuildingInfo(eLoopBuilding).getPrereqAndTech() == i):
					szBuildingButton = self.getNextWidgetName("Building")
					screen.addDDSGFCAt( szBuildingButton, szTechRecord, gc.getBuildingInfo(eLoopBuilding).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, True )
					fX += X_INCREMENT

		j = 0
		k = 0

		# Obsolete Buildings...
		for j in range(gc.getNumBuildingClassInfos()):
			eLoopBuilding = gc.getCivilizationInfo(gc.getPlayer(self.iCivSelected).getCivilizationType()).getCivilizationBuildings(j)

			if (eLoopBuilding != -1):
				if (gc.getBuildingInfo(eLoopBuilding).getObsoleteTech() == i):
					# Add obsolete picture here...
					szObsoleteButton = self.getNextWidgetName("Obsolete")
					szObsoleteX = self.getNextWidgetName("ObsoleteX")
					screen.addDDSGFCAt( szObsoleteButton, szTechRecord, gc.getBuildingInfo(eLoopBuilding).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE, eLoopBuilding, -1, False )
					screen.addDDSGFCAt( szObsoleteX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE, eLoopBuilding, -1, False )
					fX += X_INCREMENT

		j = 0
		k = 0

		# Obsolete Bonuses...
		for j in range(gc.getNumBonusInfos()):
			if (gc.getBonusInfo(j).getTechObsolete() == i):
				# Add obsolete picture here...
				szObsoleteButton = self.getNextWidgetName("ObsoleteBonus")
				szObsoleteX = self.getNextWidgetName("ObsoleteXBonus")
				screen.addDDSGFCAt( szObsoleteButton, szTechRecord, gc.getBonusInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_BONUS, j, -1, False )
				screen.addDDSGFCAt( szObsoleteX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_BONUS, j, -1, False )
				fX += X_INCREMENT
					
		j = 0
		k = 0

		# Obsolete Monastaries...
		for j in range (gc.getNumSpecialBuildingInfos()):
			if (gc.getSpecialBuildingInfo(j).getObsoleteTech() == i):
					# Add obsolete picture here...
					szObsoleteSpecialButton = self.getNextWidgetName("ObsoleteSpecial")
					szObsoleteSpecialX = self.getNextWidgetName("ObsoleteSpecialX")
					screen.addDDSGFCAt( szObsoleteSpecialButton, szTechRecord, gc.getSpecialBuildingInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_SPECIAL, j, -1, False )
					screen.addDDSGFCAt( szObsoleteSpecialX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_SPECIAL, j, -1, False )
					fX += X_INCREMENT

		j = 0
		k = 0

		# Route movement change
		for j in range(gc.getNumRouteInfos()):
			if ( gc.getRouteInfo(j).getTechMovementChange(i) != 0 ):
				szMoveButton = self.getNextWidgetName("Move")
				screen.addDDSGFCAt( szMoveButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MOVE_BONUS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MOVE_BONUS, i, -1, False )
				fX += X_INCREMENT

		j = 0
		k = 0

		# Promotion Info
		for j in range( gc.getNumPromotionInfos() ):
			if ( gc.getPromotionInfo(j).getTechPrereq() == i ):
				szPromotionButton = self.getNextWidgetName("Promotion")
				screen.addDDSGFCAt( szPromotionButton, szTechRecord, gc.getPromotionInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, j, -1, False )
				fX += X_INCREMENT

		j = 0
		k = 0

		# Free unit
		if ( gc.getTechInfo(i).getFirstFreeUnitClass() != UnitClassTypes.NO_UNITCLASS ):
			szFreeUnitButton = self.getNextWidgetName("FreeUnit")
			eLoopUnit = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(gc.getTechInfo(i).getFirstFreeUnitClass())
			if (eLoopUnit != -1):
# BUG - 3.19 No Espionage - start
				# CvUnitInfo.getEspionagePoints() was added in 319
				if (GameUtil.getVersion() < 319 or gc.getUnitInfo(eLoopUnit).getEspionagePoints() == 0 or not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ESPIONAGE)):				
# BUG - 3.19 No Espionage - end
					screen.addDDSGFCAt( szFreeUnitButton, szTechRecord, gc.getPlayer(gc.getGame().getActivePlayer()).getUnitButton(eLoopUnit), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FREE_UNIT, eLoopUnit, i, False )
					fX += X_INCREMENT

		j = 0
		k = 0

		# Feature production modifier
		if ( gc.getTechInfo(i).getFeatureProductionModifier() != 0 ):
			szFeatureProductionButton = self.getNextWidgetName("FeatureProduction")
			screen.addDDSGFCAt( szFeatureProductionButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_FEATURE_PRODUCTION").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FEATURE_PRODUCTION, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Worker speed
		if ( gc.getTechInfo(i).getWorkerSpeedModifier() != 0 ):
			szWorkerModifierButton = self.getNextWidgetName("Worker")
			screen.addDDSGFCAt( szWorkerModifierButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WORKER_SPEED").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_WORKER_RATE, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Trade Routes per City change
		if ( gc.getTechInfo(i).getTradeRoutes() != 0 ):
			szTradeRouteButton = self.getNextWidgetName("TradeRoutes")
			screen.addDDSGFCAt( szTradeRouteButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_TRADE_ROUTES").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TRADE_ROUTES, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Health Rate bonus from this tech...
		if ( gc.getTechInfo(i).getHealth() != 0 ):
			szHealthRateButton = self.getNextWidgetName("HealthRate")
			screen.addDDSGFCAt( szHealthRateButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_HEALTH").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_HEALTH_RATE, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Happiness Rate bonus from this tech...
		if ( gc.getTechInfo(i).getHappiness() != 0 ):
			szHappinessRateButton = self.getNextWidgetName("HappinessRate")
			screen.addDDSGFCAt( szHappinessRateButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_HAPPINESS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_HAPPINESS_RATE, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Free Techs
		if ( gc.getTechInfo(i).getFirstFreeTechs() > 0 ):
			szFreeTechButton = self.getNextWidgetName("FreeTech")
			screen.addDDSGFCAt( szFreeTechButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_FREETECH").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FREE_TECH, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Line of Sight bonus...
		if ( gc.getTechInfo(i).isExtraWaterSeeFrom() ):
			szLOSButton = self.getNextWidgetName("LOS")
			screen.addDDSGFCAt( szLOSButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_LOS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_LOS_BONUS, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Map Center Bonus...
		if ( gc.getTechInfo(i).isMapCentering() ):
			szMapCenterButton = self.getNextWidgetName("MapCenter")
			screen.addDDSGFCAt( szMapCenterButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MAPCENTER").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_CENTER, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Map Reveal...
		if ( gc.getTechInfo(i).isMapVisible() ):
			szMapRevealButton = self.getNextWidgetName("MapReveal")
			screen.addDDSGFCAt( szMapRevealButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MAPREVEAL").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_REVEAL, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Map Trading
		if ( gc.getTechInfo(i).isMapTrading() == True ):
			szMapTradeButton = self.getNextWidgetName("MapTrade")
			screen.addDDSGFCAt( szMapTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MAPTRADING").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_TRADE, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Tech Trading
		if ( gc.getTechInfo(i).isTechTrading() ):
			szTechTradeButton = self.getNextWidgetName("TechTrade")
			screen.addDDSGFCAt( szTechTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_TECHTRADING").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TECH_TRADE, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Gold Trading
		if ( gc.getTechInfo(i).isGoldTrading() ):
			szGoldTradeButton = self.getNextWidgetName("GoldTrade")
			screen.addDDSGFCAt( szGoldTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_GOLDTRADING").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_GOLD_TRADE, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Open Borders
		if ( gc.getTechInfo(i).isOpenBordersTrading() ):
			szOpenBordersButton = self.getNextWidgetName("OpenBorders")
			screen.addDDSGFCAt( szOpenBordersButton , szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_OPENBORDERS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OPEN_BORDERS, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Defensive Pact
		if ( gc.getTechInfo(i).isDefensivePactTrading() ):
			szDefensivePactButton = self.getNextWidgetName("DefensivePact")
			screen.addDDSGFCAt( szDefensivePactButton , szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_DEFENSIVEPACT").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_DEFENSIVE_PACT, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Permanent Alliance
		if ( gc.getTechInfo(i).isPermanentAllianceTrading() ):
			szPermanentAllianceButton = self.getNextWidgetName("PermanentAlliance")
			screen.addDDSGFCAt( szPermanentAllianceButton , szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_PERMALLIANCE").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_PERMANENT_ALLIANCE, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Vassal States
		if ( gc.getTechInfo(i).isVassalStateTrading() ):
			szVassalStateButton = self.getNextWidgetName("VassalState")
			screen.addDDSGFCAt( szVassalStateButton , szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_VASSAL").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_VASSAL_STATE, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Bridge Building
		if ( gc.getTechInfo(i).isBridgeBuilding() ):
			szBuildBridgeButton = self.getNextWidgetName("BuildBridge")
			screen.addDDSGFCAt( szBuildBridgeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_BRIDGEBUILDING").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_BUILD_BRIDGE, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Irrigation unlocked...
		if ( gc.getTechInfo(i).isIrrigation() ):
			szIrrigationButton = self.getNextWidgetName("Irrigation")
			screen.addDDSGFCAt( szIrrigationButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_IRRIGATION").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IRRIGATION, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Ignore Irrigation unlocked...
		if ( gc.getTechInfo(i).isIgnoreIrrigation() ):
			szIgnoreIrrigationButton = self.getNextWidgetName("IgnoreIrrigation")
			screen.addDDSGFCAt( szIgnoreIrrigationButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_NOIRRIGATION").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IGNORE_IRRIGATION, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Coastal Work unlocked...
		if ( gc.getTechInfo(i).isWaterWork() ):
			szWaterWorkButton = self.getNextWidgetName("WaterWork")
			screen.addDDSGFCAt( szWaterWorkButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WATERWORK").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_WATER_WORK, i, -1, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Improvements
		for j in range(gc.getNumBuildInfos()):
			if gc.getBuildInfo(j).isGraphicalOnly(): continue
		
			bTechFound = 0;

			if (gc.getBuildInfo(j).getTechPrereq() == -1):
				bTechFound = 0
				for k in range(gc.getNumFeatureInfos()):
					if (gc.getBuildInfo(j).getFeatureTech(k) == i):
						bTechFound = 1
			else:
				if (gc.getBuildInfo(j).getTechPrereq() == i):
					bTechFound = 1

			if (bTechFound == 1):
				szImprovementButton = self.getNextWidgetName("Improvement")
				screen.addDDSGFCAt( szImprovementButton, szTechRecord, gc.getBuildInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IMPROVEMENT, i, j, False )
				fX += X_INCREMENT

		j = 0
		k = 0

		# Domain Extra Moves
		for j in range( DomainTypes.NUM_DOMAIN_TYPES ):
			if (gc.getTechInfo(i).getDomainExtraMoves(j) != 0):
				szDomainExtraMovesButton = self.getNextWidgetName("DomainExtraMoves")
				screen.addDDSGFCAt( szDomainExtraMovesButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WATERMOVES").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_DOMAIN_EXTRA_MOVES, i, j, False )
				fX += X_INCREMENT

		j = 0
		k = 0

		# Adjustments
		for j in range( CommerceTypes.NUM_COMMERCE_TYPES ):
			if (gc.getTechInfo(i).isCommerceFlexible(j) and not (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isCommerceFlexible(j))):
				szAdjustButton = self.getNextWidgetName("AdjustButton")
				if ( j == CommerceTypes.COMMERCE_CULTURE ):
					szFileName = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_CULTURE").getPath()
				elif ( j == CommerceTypes.COMMERCE_ESPIONAGE ):
					szFileName = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_ESPIONAGE").getPath()
				else:
					szFileName = ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath()
				screen.addDDSGFCAt( szAdjustButton, szTechRecord, szFileName, iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_ADJUST, i, j, False )
				fX += X_INCREMENT

		j = 0
		k = 0

		# Terrain opens up as a trade route
		for j in range( gc.getNumTerrainInfos() ):
			if (gc.getTechInfo(i).isTerrainTrade(j) and not (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isTerrainTrade(j))):
				szTerrainTradeButton = self.getNextWidgetName("TerrainTradeButton")
				screen.addDDSGFCAt( szTerrainTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WATERTRADE").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, i, j, False )
				fX += X_INCREMENT

		j = gc.getNumTerrainInfos()	
		if (gc.getTechInfo(i).isRiverTrade() and not (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isRiverTrade())):
			szTerrainTradeButton = self.getNextWidgetName("TerrainTradeButton")
			screen.addDDSGFCAt( szTerrainTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_RIVERTRADE").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, i, j, False )
			fX += X_INCREMENT

		j = 0
		k = 0

		# Special buildings like monestaries...
		for j in range( gc.getNumSpecialBuildingInfos() ):
			if (gc.getSpecialBuildingInfo(j).getTechPrereq() == i):
				szSpecialBuilding = self.getNextWidgetName("SpecialBuildingButton")
				screen.addDDSGFCAt( szSpecialBuilding, szTechRecord, gc.getSpecialBuildingInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_SPECIAL_BUILDING, i, j, False )
				fX += X_INCREMENT

		j = 0
		k = 0

		# Yield change
		for j in range( gc.getNumImprovementInfos() ):
			bFound = False
			for k in range( YieldTypes.NUM_YIELD_TYPES ):
				if (gc.getImprovementInfo(j).getTechYieldChanges(i, k)):
					if ( bFound == False ):
						szYieldChange = self.getNextWidgetName("YieldChangeButton")
						screen.addDDSGFCAt( szYieldChange, szTechRecord, gc.getImprovementInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_YIELD_CHANGE, i, j, False )
						fX += X_INCREMENT
						bFound = True

		j = 0
		k = 0

		# Bonuses revealed
		for j in range( gc.getNumBonusInfos() ):
			if (gc.getBonusInfo(j).getTechReveal() == i):
				szBonusReveal = self.getNextWidgetName("BonusRevealButton")
				screen.addDDSGFCAt( szBonusReveal, szTechRecord, gc.getBonusInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_BONUS_REVEAL, i, j, False )
				fX += X_INCREMENT

		j = 0
		k = 0

		# Civic options
		for j in range( gc.getNumCivicInfos() ):
			if (gc.getCivicInfo(j).getTechPrereq() == i):
				szCivicReveal = self.getNextWidgetName("CivicRevealButton")
				screen.addDDSGFCAt( szCivicReveal, szTechRecord, gc.getCivicInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_CIVIC_REVEAL, i, j, False )
				fX += X_INCREMENT

		j = 0
		k = 0

		# Projects possible
		for j in range( gc.getNumProjectInfos() ):
			if (gc.getProjectInfo(j).getTechPrereq() == i):
				szProjectInfo = self.getNextWidgetName("ProjectInfoButton")
				screen.addDDSGFCAt( szProjectInfo, szTechRecord, gc.getProjectInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, j, 1, False )
				fX += X_INCREMENT

		j = 0
		k = 0

		# Processes possible
		for j in range( gc.getNumProcessInfos() ):
			if (gc.getProcessInfo(j).getTechPrereq() == i):
				szProcessInfo = self.getNextWidgetName("ProcessInfoButton")
				screen.addDDSGFCAt( szProcessInfo, szTechRecord, gc.getProcessInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_PROCESS_INFO, i, j, False )
				fX += X_INCREMENT

		j = 0
		k = 0

		# Religions unlocked
		for j in range( gc.getNumReligionInfos() ):
			if ( gc.getReligionInfo(j).getTechPrereq() == i ):
				szFoundReligion = self.getNextWidgetName("FoundReligionButton")
				if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_PICK_RELIGION):
					szButton = ArtFileMgr.getInterfaceArtInfo("INTERFACE_POPUPBUTTON_RELIGION").getPath()
				else:
					szButton = gc.getReligionInfo(j).getButton()
				screen.addDDSGFCAt( szFoundReligion, szTechRecord, szButton, iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FOUND_RELIGION, i, j, False )
				fX += X_INCREMENT

		for j in range( gc.getNumCorporationInfos() ):
			if ( gc.getCorporationInfo(j).getTechPrereq() == i ):
				szFoundCorporation = self.getNextWidgetName("FoundCorporationButton")
				screen.addDDSGFCAt( szFoundCorporation, szTechRecord, gc.getCorporationInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FOUND_CORPORATION, i, j, False )
				fX += X_INCREMENT

	# Will update the tech records based on color, researching, researched, queued, etc.
	def updateTechRecords (self, bForce):
#		BugUtil.debug("cvTechChooser: updateTechRecords")

		# If we are the Pitboss, we don't want to put up an interface at all
		if ( CyGame().isPitbossHost() ):
			return

		if (self.sTechTabID == self.sTechSelectTab):
			bTechName = True
			sPanel = self.TabPanels[0]
			self.BOX_INCREMENT_WIDTH = 27 # Used to be 33 #Should be a multiple of 3...
		else:
			bTechName = False
			sPanel = self.TabPanels[1]
			self.BOX_INCREMENT_WIDTH = 12 # Used to be 33 #Should be a multiple of 3...

		# Get the screen
		screen = self.getScreen()

		abChanged = []
		bAnyChanged = 0

		# Go through all the techs
		for i in range(gc.getNumTechInfos()):

			abChanged.append(0)

			if ( gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i) ):
				if ( self.aiCurrentState[i] != CIV_HAS_TECH ):
					self.aiCurrentState[i] = CIV_HAS_TECH
					abChanged[i] = 1
					bAnyChanged = 1
			elif ( gc.getPlayer(self.iCivSelected).getCurrentResearch() == i ):
				if ( self.aiCurrentState[i] != CIV_IS_RESEARCHING ):
					self.aiCurrentState[i] = CIV_IS_RESEARCHING
					abChanged[i] = 1
					bAnyChanged = 1
			elif ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
				if ( self.aiCurrentState[i] != CIV_IS_RESEARCHING ):
					self.aiCurrentState[i] = CIV_IS_RESEARCHING
					abChanged[i] = 1
					bAnyChanged = 1
			elif ( gc.getPlayer(self.iCivSelected).canEverResearch(i) ):
				if ( self.aiCurrentState[i] != CIV_NO_RESEARCH ):
					self.aiCurrentState[i] = CIV_NO_RESEARCH
					abChanged[i] = 1
					bAnyChanged = 1
			else:
				if ( self.aiCurrentState[i] != CIV_TECH_AVAILABLE ):
					self.aiCurrentState[i] = CIV_TECH_AVAILABLE
					abChanged[i] = 1
					bAnyChanged = 1

		for i in range(gc.getNumTechInfos()):
			if (abChanged[i] or bForce or (bAnyChanged and gc.getPlayer(self.iCivSelected).isResearchingTech(i))):
				# Create and place a tech in its proper location
				szTechRecord = "TechRecord" + str(i)
				szTechID = "TechID" + str(i)
				szTechString = "<font=1>"

				if ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
					szTechString = szTechString + unicode(gc.getPlayer(self.iCivSelected).getQueuePosition(i)) + ". "

				iX = 30 + ( (gc.getTechInfo(i).getGridX() - 1) * ( ( self.BOX_INCREMENT_X_SPACING + self.BOX_INCREMENT_WIDTH ) * self.PIXEL_INCREMENT ) )
				iY = ( gc.getTechInfo(i).getGridY() - 1 ) * ( self.BOX_INCREMENT_Y_SPACING * self.PIXEL_INCREMENT ) + 5

				if bTechName:
					szTechString += gc.getTechInfo(i).getDescription()
					if ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
						szTechString += " ("
						szTechString += str(gc.getPlayer(self.iCivSelected).getResearchTurnsLeft(i, ( gc.getPlayer(self.iCivSelected).getCurrentResearch() == i )))
						szTechString += ")"
					szTechString = szTechString + "</font>"
					screen.setTextAt( szTechID, sPanel, szTechString, CvUtil.FONT_LEFT_JUSTIFY, iX + 6 + X_INCREMENT, iY + 6, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_TECH_TREE, i, -1 )
					screen.setActivation( szTechID, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )

				if ( gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i) ):
					screen.setPanelColor(szTechRecord, 85, 150, 87)
				elif ( gc.getPlayer(self.iCivSelected).getCurrentResearch() == i ):
					screen.setPanelColor(szTechRecord, 104, 158, 165)
				elif ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
					screen.setPanelColor(szTechRecord, 104, 158, 165)
				elif ( gc.getPlayer(self.iCivSelected).canEverResearch(i) ):
					screen.setPanelColor(szTechRecord, 100, 104, 160)
				else:
					screen.setPanelColor(szTechRecord, 206, 65, 69)

# BUG - GP Tech Prefs - start
		self.updateTechPrefs()
# BUG - GP Tech Prefs - end

# BUG - Tech Era Colors - start
	def setTechPanelShadowColor(self, screen, sPanel, iEra):
		szEra = gc.getEraInfo(iEra).getType()
		iColor = ClockOpt.getEraColor(szEra)
		if iColor != -1:
			color = gc.getColorInfo(iColor)
			if color:
				rgb = color.getColor() # NiColorA object
				if rgb:
					screen.setPanelColor(sPanel, int(100 * rgb.r), int(100 * rgb.g), int(100 * rgb.b))
# BUG - Tech Era Colors - end

	# Will draw the arrows
	def drawArrows(self, screen, sPanel, bANDPreReq, bORPreReq):
#		BugUtil.debug("cvTechChooser: drawArrows")

		iLoop = 0

		ARROW_X = ArtFileMgr.getInterfaceArtInfo("ARROW_X").getPath()
		ARROW_Y = ArtFileMgr.getInterfaceArtInfo("ARROW_Y").getPath()
		ARROW_MXMY = ArtFileMgr.getInterfaceArtInfo("ARROW_MXMY").getPath()
		ARROW_XY = ArtFileMgr.getInterfaceArtInfo("ARROW_XY").getPath()
		ARROW_MXY = ArtFileMgr.getInterfaceArtInfo("ARROW_MXY").getPath()
		ARROW_XMY = ArtFileMgr.getInterfaceArtInfo("ARROW_XMY").getPath()
		ARROW_HEAD = ArtFileMgr.getInterfaceArtInfo("ARROW_HEAD").getPath()

		for i in range(gc.getNumTechInfos()):
			bFirst = 1
			fX = (self.BOX_INCREMENT_WIDTH * self.PIXEL_INCREMENT) - 8

			if bANDPreReq:
				for j in range( gc.getNUM_AND_TECH_PREREQS() ):
					eTech = gc.getTechInfo(i).getPrereqAndTechs(j)
					if ( eTech > -1 ):
						fX = fX - X_INCREMENT
						iX = 30 + ( (gc.getTechInfo(i).getGridX() - 1) * ( ( self.BOX_INCREMENT_X_SPACING + self.BOX_INCREMENT_WIDTH ) * self.PIXEL_INCREMENT ) )
						iY = ( gc.getTechInfo(i).getGridY() - 1 ) * ( self.BOX_INCREMENT_Y_SPACING * self.PIXEL_INCREMENT ) + 5

						szTechPrereqID = "TechPrereqID" + str((i * 1000) + j)
						screen.addDDSGFCAt( szTechPrereqID, sPanel, gc.getTechInfo(eTech).getButton(), iX + fX, iY + 6, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TECH_PREPREQ, eTech, -1, False )

						#szTechPrereqBorderID = "TechPrereqBorderID" + str((i * 1000) + j)
						#screen.addDDSGFCAt( szTechPrereqBorderID, sPanel, ArtFileMgr.getInterfaceArtInfo("TECH_TREE_BUTTON_BORDER").getPath(), iX + fX + 4, iY + 22, 32, 32, WidgetTypes.WIDGET_HELP_TECH_PREPREQ, eTech, -1, False )

			j = 0

			if bORPreReq:
				for j in range( gc.getNUM_OR_TECH_PREREQS() ):
					eTech = gc.getTechInfo(i).getPrereqOrTechs(j)
					if ( eTech > -1 ):
						iX = 24 + ( (gc.getTechInfo(eTech).getGridX() - 1) * ( ( self.BOX_INCREMENT_X_SPACING + self.BOX_INCREMENT_WIDTH ) * self.PIXEL_INCREMENT ) )
						iY = ( gc.getTechInfo(eTech).getGridY() - 1 ) * ( self.BOX_INCREMENT_Y_SPACING * self.PIXEL_INCREMENT ) + 5

						# j is the pre-req, i is the tech...
						xDiff = gc.getTechInfo(i).getGridX() - gc.getTechInfo(eTech).getGridX()
						yDiff = gc.getTechInfo(i).getGridY() - gc.getTechInfo(eTech).getGridY()

						if (yDiff == 0):
							screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + self.getXStart(), iY + self.getYStart(3), self.getWidth(xDiff), 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						elif (yDiff < 0):
							if ( yDiff == -6 ):
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + self.getXStart(), iY + self.getYStart(1), self.getWidth(xDiff) / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_XY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(1), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(1) + 8 - self.getHeight(yDiff, 0), 8, self.getHeight(yDiff, 0) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_XMY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(1) - self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(1) - self.getHeight(yDiff, 0), ( self.getWidth(xDiff) / 2 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(1) - self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							elif ( yDiff == -2 and xDiff == 2 ):
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + self.getXStart(), iY + self.getYStart(2), self.getWidth(xDiff) * 5 / 6, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_XY, iX + self.getXStart() + ( self.getWidth(xDiff) * 5 / 6 ), iY + self.getYStart(2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) * 5 / 6 ), iY + self.getYStart(2) + 8 - self.getHeight(yDiff, 3), 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_XMY, iX + self.getXStart() + ( self.getWidth(xDiff) * 5 / 6 ), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) * 5 / 6 ), iY + self.getYStart(2) - self.getHeight(yDiff, 3), ( self.getWidth(xDiff) / 6 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							else:
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + self.getXStart(), iY + self.getYStart(2), self.getWidth(xDiff) / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_XY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(2) + 8 - self.getHeight(yDiff, 3), 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_XMY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(2) - self.getHeight(yDiff, 3), ( self.getWidth(xDiff) / 2 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						elif (yDiff > 0):
							if ( yDiff == 2 and xDiff == 2):
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + self.getXStart(), iY + self.getYStart(4), self.getWidth(xDiff) / 6, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_MXMY, iX + self.getXStart() + ( self.getWidth(xDiff) / 6 ), iY + self.getYStart(4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) / 6 ), iY + self.getYStart(4) + 8, 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_MXY, iX + self.getXStart() + ( self.getWidth(xDiff) / 6 ), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 6 ), iY + self.getYStart(4) + self.getHeight(yDiff, 3), ( self.getWidth(xDiff) * 5 / 6 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							elif ( yDiff == 4 and xDiff == 1):
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + self.getXStart(), iY + self.getYStart(5), self.getWidth(xDiff) / 3, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_MXMY, iX + self.getXStart() + ( self.getWidth(xDiff) / 3 ), iY + self.getYStart(5), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) / 3 ), iY + self.getYStart(5) + 8, 8, self.getHeight(yDiff, 0) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_MXY, iX + self.getXStart() + ( self.getWidth(xDiff) / 3 ), iY + self.getYStart(5) + self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 3 ), iY + self.getYStart(5) + self.getHeight(yDiff, 0), ( self.getWidth(xDiff) * 2 / 3 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(5) + self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							else:
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + self.getXStart(), iY + self.getYStart(4), self.getWidth(xDiff) / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_MXMY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_Y, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(4) + 8, 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_MXY, iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_X, iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 2 ), iY + self.getYStart(4) + self.getHeight(yDiff, 3), ( self.getWidth(xDiff) / 2 ) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
								screen.addDDSGFCAt( self.getNextWidgetName("TechArrow"), sPanel, ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff), iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )

		return

# BUG - GP Tech Prefs - start
	def resetTechPrefs (self):
		self.pPrefs = TechPrefs.TechPrefs()
	
	def updateTechPrefs (self):
#		BugUtil.debug("cvTechChooser: updateTechPrefs")

		# If we are the Pitboss, we don't want to put up an interface at all
		if ( CyGame().isPitbossHost() ):
			return

		# These don't seem to be setup when screen is first opened
		if (gc.getNumTechInfos() <= 0 or gc.getNumFlavorTypes() <= 0):
			return

		# Get the screen and player
		screen = self.getScreen()
		pPlayer = gc.getPlayer(self.iCivSelected)

		# Don't show tech prefs during advanced start setup
		if (pPlayer.getAdvancedStartPoints() >= 0):
			return

		# Check to see if option is disabled
		if (not BugOpt.isShowGPTechPrefs()):
			if (self.bPrefsShowing):
				# ... and if so, remove icons if they are currently showing
				screen.hide( "GreatPersonHeading")
				for i, f in enumerate(FLAVORS):
					screen.hide( "GreatPerson" + str(f) )
					screen.hide( "GreatPersonTech" + str(f) )
					screen.hide( "GreatPersonTechNext" + str(f) )
				self.bPrefsShowing = False
			return
		# Always redraw the GP icons because otherwise they are prone to disappearing
		# discover icon heading
		iIconSize = 48
		iX = PREF_ICON_LEFT + 5 * PREF_ICON_SIZE / 4 - iIconSize / 2
		iY = PREF_ICON_TOP - iIconSize - 40
		screen.addDDSGFC( "GreatPersonHeading", ArtFileMgr.getInterfaceArtInfo("DISCOVER_TECHNOLOGY_BUTTON").getPath(), iX, iY, iIconSize, iIconSize, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		for i, f in enumerate(FLAVORS):
			# GP icon
			iUnitClass = gc.getInfoTypeForString(UNIT_CLASSES[i])
			iUnitType = gc.getUnitClassInfo(iUnitClass).getDefaultUnitIndex()
			pUnitInfo = gc.getUnitInfo(iUnitType)
			iX = PREF_ICON_LEFT
			iY = PREF_ICON_TOP + 4 * i * PREF_ICON_SIZE
			screen.addDDSGFC( "GreatPerson" + str(f), pUnitInfo.getButton(), iX, iY, PREF_ICON_SIZE, PREF_ICON_SIZE, WidgetTypes.WIDGET_TECH_PREFS_ALL, f, -1 )
		self.bPrefsShowing = True

		# Remove any techs researched since last call, creating tree if necessary
		if (not self.pPrefs):
			self.resetTechPrefs()
		self.pPrefs.removeKnownTechs()

		# Add all techs in research queue to set of soon-to-be-known techs
		sTechs = set()
		for i in range(gc.getNumTechInfos()):
			if (pPlayer.isResearchingTech(i)):
				sTechs.add(self.pPrefs.getTech(i))

		# Update the buttons to reflect the new tech prefs
		for i, f in enumerate(FLAVORS):
			# GP button
			screen.show( "GreatPerson" + str(f) )

			# Current tech GP will pop
			szButtonName = "GreatPersonTech" + str(f)
			pTech = self.pPrefs.getNextResearchableFlavorTech(f)
			iX = PREF_ICON_LEFT + 3 * PREF_ICON_SIZE / 2
			iY = PREF_ICON_TOP + 4 * i * PREF_ICON_SIZE
			if (pTech):
				screen.addDDSGFC( szButtonName, pTech.getInfo().getButton(), iX, iY, PREF_ICON_SIZE, PREF_ICON_SIZE, WidgetTypes.WIDGET_TECH_PREFS_CURRENT, f, -1 )
			else:
				screen.addDDSGFC( szButtonName, self.NO_TECH_ART, iX, iY, PREF_ICON_SIZE, PREF_ICON_SIZE, WidgetTypes.WIDGET_TECH_PREFS_CURRENT, f, -1 )
			screen.show( szButtonName )

			# Tech GP will pop once selected techs are researched
			szButtonName = "GreatPersonTechNext" + str(f)
			pTech = self.pPrefs.getNextResearchableWithFlavorTech(f, sTechs)
			iX = PREF_ICON_LEFT + 3 * PREF_ICON_SIZE / 2
			iY = PREF_ICON_TOP + 4 * i * PREF_ICON_SIZE + 3 * PREF_ICON_SIZE / 2
			if (pTech):
				screen.addDDSGFC( szButtonName, pTech.getInfo().getButton(), iX, iY, PREF_ICON_SIZE, PREF_ICON_SIZE, WidgetTypes.WIDGET_TECH_PREFS_FUTURE, f, -1 )
			else:
				screen.addDDSGFC( szButtonName, self.NO_TECH_ART, iX, iY, PREF_ICON_SIZE, PREF_ICON_SIZE, WidgetTypes.WIDGET_TECH_PREFS_FUTURE, f, -1 )
			screen.show( szButtonName )
# BUG - GP Tech Prefs - end

	def TechRecord (self, inputClass):
		return 0

	# Clicked the parent?
	def ParentClick (self, inputClass):
		return 0

	def CivDropDown( self, inputClass ):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED ):
			screen = self.getScreen()
			iIndex = screen.getSelectedPullDownID("CivDropDown")
			self.iCivSelected = screen.getPullDownData("CivDropDown", iIndex)
			self.updateTechRecords(false)

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
#		BugUtil.debug("cvTechChooser: handleInput")
#		BugUtil.debugInput(inputClass)

		# Get the screen
		screen = self.getScreen()

		szWidgetName = inputClass.getFunctionName() + str(inputClass.getID())

		# Advanced Start Stuff
		pPlayer = gc.getPlayer(self.iCivSelected)
		if (pPlayer.getAdvancedStartPoints() >= 0):
#			BugUtil.debug("cvTechChooser: handleInput - advancedstart")
			# Add tech button
			if (inputClass.getFunctionName() == "AddTechButton"):
				if (pPlayer.getAdvancedStartTechCost(self.m_iSelectedTech, true) != -1):
					CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_TECH, self.iCivSelected, -1, -1, self.m_iSelectedTech, true)	#Action, Player, X, Y, Data, bAdd
					self.m_bTechRecordsDirty = true
					self.m_bSelectedTechDirty = true

			# Tech clicked on
			elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
				if (inputClass.getButtonType() == WidgetTypes.WIDGET_TECH_TREE):
					self.m_iSelectedTech = inputClass.getData1()
					self.updateSelectedTech()

		' Calls function mapped in TechChooserInputMap'
		# only get from the map if it has the key
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED ):
#			BugUtil.debug("cvTechChooser: handleInput - dropdown")
			self.CivDropDown( inputClass )
			return 1

		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if szWidgetName == self.sTechSelectTab:
				self.sTechTabID = self.sTechSelectTab
				self.ShowTab()

			elif szWidgetName == self.sTechTradeTab:
				self.sTechTabID = self.sTechTradeTab
				self.ShowTab()



		return 0

	def getNextWidgetName(self, sName):
#		BugUtil.debug("cvTechChooser: getNextWidgetName %i %i", self.nWidgetCount, len(self.sWidgets))
		szName = sName + str(self.nWidgetCount)
		self.nWidgetCount += 1
		self.sWidgets.append(szName)
		return szName

	def deleteWidgets(self):
#		BugUtil.debug("cvTechChooser: deleteWidgets %i %i", self.nWidgetCount, len(self.sWidgets))
		screen = self.getScreen()
		for w in self.sWidgets:
#			BugUtil.debug("cvTechChooser: deleteWidgets '%s'", w)
			screen.deleteWidget(w)

		self.nWidgetCount = 0
		self.sWidgets = []
		return





	def getXStart(self):
		return ( self.BOX_INCREMENT_WIDTH * self.PIXEL_INCREMENT )

	def getXSpacing(self):
		return ( self.BOX_INCREMENT_X_SPACING * self.PIXEL_INCREMENT )

	def getYStart(self, iY):
		return int((((self.BOX_INCREMENT_HEIGHT * self.PIXEL_INCREMENT ) / 6.0) * iY) - self.PIXEL_INCREMENT )

	def getWidth(self, xDiff):
		return ( ( xDiff * self.getXSpacing() ) + ( ( xDiff - 1 ) * self.getXStart() ) )

	def getHeight(self, yDiff, nFactor):
		return ( ( nFactor + ( ( abs( yDiff ) - 1 ) * 6 ) ) * self.PIXEL_INCREMENT )

	def update(self, fDelta):
		if (CyInterface().isDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT, false)

			if (self.m_bSelectedTechDirty):
				self.m_bSelectedTechDirty = false
				self.updateSelectedTech()

			if (self.m_bTechRecordsDirty):
				self.m_bTechRecordsDirty = false
				self.updateTechRecords(true)

			if (gc.getPlayer(self.iCivSelected).getAdvancedStartPoints() < 0):
				# hide the screen
				screen = self.getScreen()
				screen.hide("AddTechButton")
				screen.hide("ASPointsLabel")
				screen.hide("SelectedTechLabel")

		return

	def updateSelectedTech(self):
		pPlayer = gc.getPlayer(CyGame().getActivePlayer())

		# Get the screen
		screen = self.getScreen()

		szName = ""
		iCost = 0

		if (self.m_iSelectedTech != -1):
			szName = gc.getTechInfo(self.m_iSelectedTech).getDescription()
			iCost = gc.getPlayer(CyGame().getActivePlayer()).getAdvancedStartTechCost(self.m_iSelectedTech, true)

		if iCost > 0:
			szText = u"<font=4>" + localText.getText("TXT_KEY_WB_AS_SELECTED_TECH_COST", (iCost, pPlayer.getAdvancedStartPoints())) + u"</font>"
			screen.setLabel( "ASPointsLabel", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_ADVANCED_START_TEXT, self.Y_ADD_TECH_BUTTON + 3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		else:
			screen.hide("ASPointsLabel")

		szText = u"<font=4>"
		szText += localText.getText("TXT_KEY_WB_AS_SELECTED_TECH", (szName,))
		szText += u"</font>"
		screen.setLabel( "SelectedTechLabel", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_ADVANCED_START_TEXT + 250, self.Y_ADD_TECH_BUTTON + 3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Want to add
		if (pPlayer.getAdvancedStartTechCost(self.m_iSelectedTech, true) != -1):
			screen.show("AddTechButton")
		else:
			screen.hide("AddTechButton")

	def onClose(self):
		pPlayer = gc.getPlayer(self.iCivSelected)
		if (pPlayer.getAdvancedStartPoints() >= 0):
			CyInterface().setDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT, true)
		return 0

class TechChooserMaps:

	TechChooserInputMap = {
		'TechRecord'			: CvTechChooser().TechRecord,
		'TechID'				: CvTechChooser().ParentClick,
		'TechPane'				: CvTechChooser().ParentClick,
		'TechButtonID'			: CvTechChooser().ParentClick,
		'TechButtonBorder'		: CvTechChooser().ParentClick,
		'Unit'					: CvTechChooser().ParentClick,
		'Building'				: CvTechChooser().ParentClick,
		'Obsolete'				: CvTechChooser().ParentClick,
		'ObsoleteX'				: CvTechChooser().ParentClick,
		'Move'					: CvTechChooser().ParentClick,
		'FreeUnit'				: CvTechChooser().ParentClick,
		'FeatureProduction'			: CvTechChooser().ParentClick,
		'Worker'				: CvTechChooser().ParentClick,
		'TradeRoutes'			: CvTechChooser().ParentClick,
		'HealthRate'			: CvTechChooser().ParentClick,
		'HappinessRate'			: CvTechChooser().ParentClick,
		'FreeTech'				: CvTechChooser().ParentClick,
		'LOS'					: CvTechChooser().ParentClick,
		'MapCenter'				: CvTechChooser().ParentClick,
		'MapReveal'				: CvTechChooser().ParentClick,
		'MapTrade'				: CvTechChooser().ParentClick,
		'TechTrade'				: CvTechChooser().ParentClick,
		'OpenBorders'		: CvTechChooser().ParentClick,
		'BuildBridge'			: CvTechChooser().ParentClick,
		'Irrigation'			: CvTechChooser().ParentClick,
		'Improvement'			: CvTechChooser().ParentClick,
		'DomainExtraMoves'			: CvTechChooser().ParentClick,
		'AdjustButton'			: CvTechChooser().ParentClick,
		'TerrainTradeButton'	: CvTechChooser().ParentClick,
		'SpecialBuildingButton'	: CvTechChooser().ParentClick,
		'YieldChangeButton'		: CvTechChooser().ParentClick,
		'BonusRevealButton'		: CvTechChooser().ParentClick,
		'CivicRevealButton'		: CvTechChooser().ParentClick,
		'ProjectInfoButton'		: CvTechChooser().ParentClick,
		'ProcessInfoButton'		: CvTechChooser().ParentClick,
		'FoundReligionButton'	: CvTechChooser().ParentClick,
		'CivDropDown'			: CvTechChooser().CivDropDown,
		}

