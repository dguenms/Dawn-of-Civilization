## TechWindow
##
## Originally by SirRethcir: Techanzeige hinzugefügt
## Enhanced by Roamty, Caesium, Guarav
##
## Copyright (c) 2008 The BUG Mod.

from CvPythonExtensions import *
import CvUtil

# BUG - Options - end
import BugCore
TechWindowOpt = BugCore.game.TechWindow
# BUG - Options - end

localText = CyTranslator()

class CvTechSplashScreen:
	"Splash screen for techs"
	def __init__(self, iScreenID):
		self.nScreenId = iScreenID
			
		self.iTech = -1
		self.nWidgetCount = 0
		
		# widget names
		self.WIDGET_ID = "TechSplashScreenWidget"
		self.SCREEN_NAME = "TechSplashScreen"
		self.EXIT_ID = "TechSplashExit"
		
		self.X_SCREEN = 205
		self.Y_SCREEN = 27
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Z_BACKGROUND = -1.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.DZ = -0.2
		
		self.Z_HELP_AREA = self.Z_CONTROLS - 2
		self.W_HELP_AREA = 200
		
		# Panels
		
		self.iMarginSpace = 15
		
		self.X_MAIN_PANEL = 205
		self.Y_MAIN_PANEL = 55
		self.W_MAIN_PANEL = 620
		self.H_MAIN_PANEL = 585#545
		
		# Upper Panel
		
		self.X_UPPER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
		self.Y_UPPER_PANEL = self.Y_MAIN_PANEL + self.iMarginSpace
		self.W_UPPER_PANEL = self.W_MAIN_PANEL - (self.iMarginSpace * 2)
		self.H_UPPER_PANEL = 200
		
		self.X_TITLE = self.X_MAIN_PANEL + (self.W_MAIN_PANEL / 2)
		self.Y_TITLE = self.Y_UPPER_PANEL + 12
		
		self.W_ICON = 64#90
		self.H_ICON = 64#90
		self.X_ICON = self.X_UPPER_PANEL + 56#23#42
		self.Y_ICON = self.Y_UPPER_PANEL + (self.H_UPPER_PANEL / 2) - (self.H_ICON / 2) + 17
		
		self.X_ICON_PANEL = self.X_UPPER_PANEL + self.iMarginSpace + 2
		self.Y_ICON_PANEL = self.Y_UPPER_PANEL + self.iMarginSpace + 33
		self.W_ICON_PANEL = 140
		self.H_ICON_PANEL = 135#self.H_MAIN_PANEL - (self.iMarginSpace * 2)
		
		self.X_QUOTE = self.X_UPPER_PANEL + self.W_ICON_PANEL + (self.iMarginSpace * 2)
		self.Y_QUOTE = self.Y_UPPER_PANEL + self.iMarginSpace + 36
		self.W_QUOTE = 400
		self.H_QUOTE = self.H_UPPER_PANEL - (self.iMarginSpace * 2) - 38
		
#---Geändert START - siehe original Datei -----------------		
		# Lower Panel
		
		self.X_LOWER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
		self.Y_LOWER_PANEL = self.Y_UPPER_PANEL + self.H_UPPER_PANEL
		self.W_LOWER_PANEL = self.W_MAIN_PANEL - (self.iMarginSpace * 2)
		self.H_LOWER_PANEL = 360
		
		self.H_ALLOWS_PANEL = 80
		self.H_ALLOWS_SPACE = 22#28

		self.X_SPECIAL_PANEL = self.X_LOWER_PANEL + self.iMarginSpace
		self.Y_SPECIAL_PANEL = self.Y_LOWER_PANEL + self.iMarginSpace + 20
		self.W_SPECIAL_PANEL = self.W_LOWER_PANEL/2 - self.iMarginSpace
		self.H_SPECIAL_PANEL = 2 * self.H_ALLOWS_PANEL + self.H_ALLOWS_SPACE

		self.X_ALLOWS_PANELSIR = self.X_LOWER_PANEL + self.iMarginSpace
		self.Y_ALLOWS_PANELSIR = self.Y_SPECIAL_PANEL + self.H_SPECIAL_PANEL + self.H_ALLOWS_SPACE
		self.W_ALLOWS_PANELSIR = self.W_LOWER_PANEL/2 - (self.iMarginSpace)
		self.H_ALLOWS_PANELSIR = 80

		self.X_ALLOWS_PANEL = self.X_LOWER_PANEL + self.iMarginSpace + self.W_SPECIAL_PANEL
		self.Y_ALLOWS_PANEL = self.Y_SPECIAL_PANEL
		self.W_ALLOWS_PANEL = self.W_LOWER_PANEL/2 - (self.iMarginSpace)
		self.Y_ALLOWS_PANEL2 = self.Y_SPECIAL_PANEL + self.H_ALLOWS_PANEL + self.H_ALLOWS_SPACE
		self.Y_ALLOWS_PANEL3 = self.Y_SPECIAL_PANEL + 2 * (self.H_ALLOWS_PANEL + self.H_ALLOWS_SPACE)
#---Geändert ENDE ------------------------------------------
		
		# Contents
		
		self.X_EXIT = self.X_MAIN_PANEL + (self.W_MAIN_PANEL / 2) - 55
		self.Y_EXIT = self.Y_MAIN_PANEL + self.H_MAIN_PANEL - 45
		self.W_EXIT = 120
		self.H_EXIT = 30	
		
	def interfaceScreen(self, iTech):
		
		self.EXIT_TEXT = localText.getText("TXT_KEY_SCREEN_CONTINUE", ())
		self.nTechs = CyGlobalContext().getNumTechInfos()
		self.iTech = iTech
		self.nWidgetCount = 0
		
		# Create screen
		
		screen = self.getScreen()
		
		techInfo = CyGlobalContext().getTechInfo(self.iTech)
		
		screen.setSound(techInfo.getSound())
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.enableWorldSounds( false )
	
#		screen.setHelpTextArea(self.W_HELP_AREA, FontTypes.SMALL_FONT, self.X_UNIT_PANE, self.Y_UNIT_PANE, self.Z_HELP_AREA, 1, CyArtFileMgr().getInterfaceArtInfo("POPUPS_BACKGROUND_TRANSPARENT").getPath(), True, True, CvUtil.FONT_LEFT_JUSTIFY, 0 )
#		screen.addDDSGFC( "TechSplashBackground", CyArtFileMgr().getInterfaceArtInfo("TEMP_BG").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.showWindowBackground( False )
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		
		# Create panels
		
		# Main Panel
		szMainPanel = "TechSplashMainPanel"
		screen.addPanel( szMainPanel, "", "", true, true,
			self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_MAIN )
		
		# Top Panel
		szHeaderPanel = "TechSplashHeaderPanel"
		screen.addPanel( szHeaderPanel, "", "", true, true,
			self.X_UPPER_PANEL, self.Y_UPPER_PANEL, self.W_UPPER_PANEL, self.H_UPPER_PANEL, PanelStyles.PANEL_STYLE_DAWNBOTTOM )
		screen.setStyle(szHeaderPanel, "Panel_DawnBottom_Style")
		
		# Icon Panel
		szIconPanel = "IconPanel"
		screen.addPanel( szIconPanel, "", "", true, true,
			self.X_ICON_PANEL, self.Y_ICON_PANEL, self.W_UPPER_PANEL-(self.iMarginSpace * 2), self.H_UPPER_PANEL-(self.iMarginSpace * 4), PanelStyles.PANEL_STYLE_MAIN_TAN15 )
		screen.setStyle(szIconPanel, "Panel_TechDiscover_Style")
		
		# Icon Panel
		szIconPanel = "IconPanelGlow"
		screen.addPanel( szIconPanel, "", "", true, true,
			self.X_ICON_PANEL, self.Y_ICON_PANEL, self.W_ICON_PANEL, self.H_ICON_PANEL, PanelStyles.PANEL_STYLE_MAIN_TAN15 )
		screen.setStyle(szIconPanel, "Panel_TechDiscoverGlow_Style")
		
		# Bottom Panel
		szTextPanel = "TechSplashTextPanel"
		screen.addPanel( szTextPanel, "", "", true, true,
			self.X_LOWER_PANEL+self.iMarginSpace, self.Y_LOWER_PANEL, self.W_LOWER_PANEL-(self.iMarginSpace * 2), self.H_LOWER_PANEL, PanelStyles.PANEL_STYLE_MAIN )
		screen.setStyle(szTextPanel, "Panel_TanT_Style")
		
		# Exit Button
		screen.setButtonGFC("Exit", localText.getText("TXT_KEY_SCREEN_CONTINUE", ()), "", self.X_EXIT, self.Y_EXIT, self.W_EXIT , self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		
		# Special Panel
		szSpecialPanel = "TechSplashSpecialPanel"
		screen.addPanel( szSpecialPanel, "", "", true, true,
				self.X_SPECIAL_PANEL+self.iMarginSpace, self.Y_SPECIAL_PANEL, self.W_SPECIAL_PANEL-(self.iMarginSpace * 2), self.H_SPECIAL_PANEL, PanelStyles.PANEL_STYLE_IN )
		screen.setStyle(szSpecialPanel, "Panel_Black25_Style")
		
#---Eingefügt START - kann komplett gelöscht werden-----------------
		# Allows PanelSIR
		panelNameSIR = "SIR"
		screen.addPanel( panelNameSIR, "", "", false, true,
                                 self.X_ALLOWS_PANELSIR+self.iMarginSpace, self.Y_ALLOWS_PANELSIR, self.W_ALLOWS_PANELSIR-(self.iMarginSpace * 2), self.H_ALLOWS_PANELSIR, PanelStyles.PANEL_STYLE_IN )
		screen.setStyle(panelNameSIR, "Panel_Black25_Style")
#---Eingefügt ENDE -------------------------------------------------

		# Allows Panel
		panelName = self.getNextWidgetName()
		screen.addPanel( panelName, "", "", false, true,
                                 self.X_ALLOWS_PANEL+self.iMarginSpace, self.Y_ALLOWS_PANEL, self.W_ALLOWS_PANEL-(self.iMarginSpace * 2), self.H_ALLOWS_PANEL, PanelStyles.PANEL_STYLE_IN )
		screen.setStyle(panelName, "Panel_Black25_Style")
		
#---Eingefügt START - kann komplett gelöscht werden-----------------
		# Allows Panel2
		panelName2 = "SIR2"
		screen.addPanel( panelName2, "", "", false, true,
                                 self.X_ALLOWS_PANEL+self.iMarginSpace, self.Y_ALLOWS_PANEL2, self.W_ALLOWS_PANEL-(self.iMarginSpace * 2), self.H_ALLOWS_PANEL, PanelStyles.PANEL_STYLE_IN )
		screen.setStyle(panelName2, "Panel_Black25_Style")

		# Allows Panel3
		panelName3 = "SIR3"
		screen.addPanel( panelName3, "", "", false, true,
                                 self.X_ALLOWS_PANEL+self.iMarginSpace, self.Y_ALLOWS_PANEL3, self.W_ALLOWS_PANEL-(self.iMarginSpace * 2), self.H_ALLOWS_PANEL, PanelStyles.PANEL_STYLE_IN )
		screen.setStyle(panelName3, "Panel_Black25_Style")
#---Eingefügt ENDE -------------------------------------------------

		# Add Contents
		
		# Title
		szTech = techInfo.getDescription()
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4>" + szTech.upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY,
			self.X_TITLE, self.Y_TITLE, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Tech Icon
		screen.addDDSGFC(self.getNextWidgetName(), techInfo.getButton(), self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, self.iTech, -1 )
		
		# Tech Quote
		szTechQuote = techInfo.getQuote()
		iTextOffset = 0
		if TechWindowOpt.isShowCivilopediaText():
			szTechQuote += "\n\n" + techInfo.getCivilopedia()
		else:
			iTextOffset = 20
		screen.addMultilineText( "Text", szTechQuote, 
                        self.X_QUOTE, self.Y_QUOTE + iTextOffset, self.W_QUOTE, self.H_QUOTE - iTextOffset, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
		# Special
		szSpecialTitle = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()) + u"</font>"
		szSpecialTitleWidget = "SpecialTitle"
		screen.setText(szSpecialTitleWidget, "", szSpecialTitle, CvUtil.FONT_LEFT_JUSTIFY,
			       self.X_SPECIAL_PANEL+self.iMarginSpace, self.Y_SPECIAL_PANEL - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		listName = self.getNextWidgetName()
		
		szSpecialText = CyGameTextMgr().getTechHelp(self.iTech, True, False, False, True, -1)[1:]
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANEL+10, self.Y_SPECIAL_PANEL+5, self.W_SPECIAL_PANEL-20, self.H_SPECIAL_PANEL-20, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
		
#---Eingefügt START - kann komplett gelöscht werden --------------
		# Allows -> LeadsTo
		szAllowsTitleDescSIR = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_LEADS_TO", ()) + ":" + u"</font>"
		szAllowsTitleWidgetSIR = "AllowsTitleSIR"
		screen.setText(szAllowsTitleWidgetSIR, "", szAllowsTitleDescSIR, CvUtil.FONT_LEFT_JUSTIFY,
			       self.X_ALLOWS_PANELSIR+self.iMarginSpace, self.Y_ALLOWS_PANELSIR - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		for j in range(CyGlobalContext().getNumTechInfos()):
			for k in range(CyGlobalContext().getDefineINT("NUM_OR_TECH_PREREQS")):
				iPrereq = CyGlobalContext().getTechInfo(j).getPrereqOrTechs(k)
				if (iPrereq == self.iTech):
        				screen.attachImageButton( panelNameSIR, "", CyGlobalContext().getTechInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_DERIVED_TECH, j, self.iTech, False )
			for k in range(CyGlobalContext().getDefineINT("NUM_AND_TECH_PREREQS")):
				iPrereq = CyGlobalContext().getTechInfo(j).getPrereqAndTechs(k)
				if (iPrereq == self.iTech):
        				screen.attachImageButton( panelNameSIR, "", CyGlobalContext().getTechInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_DERIVED_TECH, j, self.iTech, False )
#---Eingefügt ENDE ------------------------------------------------
		
                # Allows
		# szAllowsTitleDesc = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_ALLOWS", ()) + ":" + u"</font>"
		# szAllowsTitleWidget = "AllowsTitle"
		# screen.setText(szAllowsTitleWidget, "", szAllowsTitleDesc, CvUtil.FONT_LEFT_JUSTIFY,
		# 	       self.X_ALLOWS_PANEL+self.iMarginSpace, self.Y_ALLOWS_PANEL - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Units Enabled
		szUnitsTitleDesc = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_UNITS_ENABLED", ()) + ":" + u"</font>"
		szUnitsTitleWidget = "UnitsTitle"
		screen.setText(szUnitsTitleWidget, "", szUnitsTitleDesc, CvUtil.FONT_LEFT_JUSTIFY,
			       self.X_ALLOWS_PANEL + self.iMarginSpace, self.Y_ALLOWS_PANEL - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		for j in range( CyGlobalContext().getNumUnitClassInfos() ):
			eLoopUnit = CyGlobalContext().getCivilizationInfo(CyGlobalContext().getGame().getActiveCivilizationType()).getCivilizationUnits(j)
			if (eLoopUnit != -1):
				if (isTechRequiredForUnit(self.iTech, eLoopUnit)):
	        			screen.attachImageButton( panelName, "", CyGlobalContext().getUnitInfo(eLoopUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM,
								  WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False )

		# Buildings Enabled
		szBuildingsTitleDesc = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_BUILDINGS_ENABLED", ()) + ":" + u"</font>"
		szBuildingsTitleWidget = "BuildingsTitle"
		screen.setText(szBuildingsTitleWidget, "", szBuildingsTitleDesc, CvUtil.FONT_LEFT_JUSTIFY,
			       self.X_ALLOWS_PANEL + self.iMarginSpace, self.Y_ALLOWS_PANEL2 - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		for j in range(CyGlobalContext().getNumBuildingClassInfos()):
			bTechFound = 0
			eLoopBuilding = CyGlobalContext().getCivilizationInfo(CyGlobalContext().getGame().getActiveCivilizationType()).getCivilizationBuildings(j)
			if (eLoopBuilding != -1):
				if (isTechRequiredForBuilding(self.iTech, eLoopBuilding)):
	        			screen.attachImageButton( panelName2, "", CyGlobalContext().getBuildingInfo(eLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM,
								  WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, False )

		# Improvements
		szImprovesTitleDesc = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ()) + ":" + u"</font>"
		szImprovesTitleWidget = "ImprovesTitle"
		screen.setText(szImprovesTitleWidget, "", szImprovesTitleDesc, CvUtil.FONT_LEFT_JUSTIFY,
			       self.X_ALLOWS_PANEL + self.iMarginSpace, self.Y_ALLOWS_PANEL3 - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		for j in range(CyGlobalContext().getNumProjectInfos()):
			bTechFound = 0
			if (isTechRequiredForProject(self.iTech, j)):
				screen.attachImageButton( panelName3, "", CyGlobalContext().getProjectInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM,
							  WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, j, 1, False )
							  
		for j in range(CyGlobalContext().getNumPromotionInfos()):
			if (CyGlobalContext().getPromotionInfo(j).getTechPrereq() == self.iTech):
				screen.attachImageButton( panelName3, "", CyGlobalContext().getPromotionInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM,
							  WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, j, 1, False )
		
#---Eingefügt START - kann komplett gelöscht werden --------------
                # Improvements
		for j in range(CyGlobalContext().getNumBuildInfos()):
				bTechFound = 0;
				if (CyGlobalContext().getBuildInfo(j).getTechPrereq() == -1):
					bTechFound = 0
					for k in range(CyGlobalContext().getNumFeatureInfos()):
						if (CyGlobalContext().getBuildInfo(j).getFeatureTech(k) == self.iTech):
							bTechFound = 1
				else:
					if (CyGlobalContext().getBuildInfo(j).getTechPrereq() == self.iTech):
						bTechFound = 1

				if (bTechFound == 1):
					if (CyGlobalContext().getBuildInfo(j).getImprovement() == -1):
						screen.attachImageButton( panelName3, "", CyGlobalContext().getBuildInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_IMPROVEMENT, j, 1, False )
					else:
						screen.attachImageButton( panelName3, "", CyGlobalContext().getBuildInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, CyGlobalContext().getBuildInfo(j).getImprovement(), 1, False )

		# Bonuses
		for j in range(CyGlobalContext().getNumBonusInfos()):
			if (CyGlobalContext().getBonusInfo(j).getTechReveal() == self.iTech):
				screen.attachImageButton( panelName3, "", CyGlobalContext().getBonusInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM,
							  WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, j, 1, False )

		# Civic
		for j in range(CyGlobalContext().getNumCivicInfos()):
			if (CyGlobalContext().getCivicInfo(j).getTechPrereq() == self.iTech):
				screen.attachImageButton( panelName3, "", CyGlobalContext().getCivicInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM,
							  WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, j, 1, False )
#---Eingefügt ENDE ------------------------------------------------		

	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount * self.nTechs + self.iTech)
		self.nWidgetCount += 1
		return szName
		
	# returns a unique ID for this screen
	def getScreen(self):
		screen = CyGInterfaceScreen(self.SCREEN_NAME + str(self.iTech), self.nScreenId)
		return screen
					
	def handleInput( self, inputClass ):
		if ( inputClass.getData() == int(InputTypes.KB_RETURN) ):
			self.getScreen().hideScreen()
			return 1
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getFunctionName() == self.EXIT_ID):
				self.getScreen().hideScreen()
			return 1
		return 0
		
	def update(self, fDelta):
		return
