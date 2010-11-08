## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Sevopedia 
##   sevotastic.blogspot.com
##   sevotastic@yahoo.com
##


from CvPythonExtensions import *
import CvUtil
import CvPediaScreen
import ScreenInput
import CvScreenEnums
import string

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaTech(CvPediaScreen.CvPediaScreen):
	"Civilopedia Screen for Techs"

	def __init__(self, main):
		self.iTech = -1
		self.top = main
	
		self.X_TECH_PANE = self.top.X_PEDIA_PAGE + 20
		self.Y_TECH_PANE = 55
		self.W_TECH_PANE = 300
		self.H_TECH_PANE = 116

		self.X_ICON = self.X_TECH_PANE + 8
		self.Y_ICON = self.Y_TECH_PANE + 8
		self.W_ICON = 100
		self.H_ICON = 100
		self.ICON_SIZE = 64

		self.X_COST = self.X_TECH_PANE + 110
		self.Y_COST = self.Y_TECH_PANE + 35
		
		self.BUTTON_SIZE = 64

		self.X_QUOTE_PANE = self.X_TECH_PANE
		self.Y_QUOTE_PANE = 186 #Rhye (181)
		self.W_QUOTE_PANE = 530
		self.H_QUOTE_PANE = 102 #Rhye (110)

		self.X_UNIT_PANE = self.X_TECH_PANE + self.W_TECH_PANE 
		self.Y_UNIT_PANE = 430
		self.W_UNIT_PANE = 235
		self.H_UNIT_PANE = 124

		self.X_BUILDING_PANE = self.X_TECH_PANE + self.W_TECH_PANE 
		self.Y_BUILDING_PANE = 568
		self.W_BUILDING_PANE = 235
		self.H_BUILDING_PANE = 124

		self.X_PREREQ_PANE = self.X_TECH_PANE
		self.Y_PREREQ_PANE = 292
		self.W_PREREQ_PANE = 280
		self.H_PREREQ_PANE = 124

		self.X_LEADS_TO_PANE = self.X_TECH_PANE + self.W_TECH_PANE 
		self.Y_LEADS_TO_PANE = 292
		self.W_LEADS_TO_PANE = 235
		self.H_LEADS_TO_PANE = 124

		self.X_SPECIAL_PANE = self.X_TECH_PANE
		self.Y_SPECIAL_PANE = 430
		self.W_SPECIAL_PANE = 265
		self.H_SPECIAL_PANE = 280

	def interfaceScreen(self, iTech):	
						
		self.iTech = iTech
	
		self.top.deleteAllWidgets()						
							
		screen = self.top.getScreen()
		
		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()

		# Header...
		szHeader = u"<font=4b>" + gc.getTechInfo(self.iTech).getDescription().upper() + u"</font>"
		screen.setText(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH, iTech)
		screen.setImageButton(self.top.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_CIVILOPEDIA_ICON").getPath(), self.top.X_EXIT, self.top.Y_TITLE, 32, 32, WidgetTypes.WIDGET_PEDIA_DESCRIPTION,  CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH, iTech)
		
		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_TECH or bNotActive:		
			if self.top.iLastScreen != CvScreenEnums.PEDIA_MAIN:
				self.placeLinks()
			self.top.iLastScreen = CvScreenEnums.PEDIA_TECH

		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.X_TECH_PANE, self.Y_TECH_PANE, self.W_TECH_PANE, self.H_TECH_PANE, PanelStyles.PANEL_STYLE_BLUE50)

		# Icon
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getTechInfo(self.iTech).getButton(), self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		szCostId = self.top.getNextWidgetName()
		if self.top.iActivePlayer == -1:
			szCostText = localText.getText("TXT_KEY_PEDIA_COST", ( gc.getTechInfo(iTech).getResearchCost(), ) ) + u"%c" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())
		else:
			szCostText = localText.getText("TXT_KEY_PEDIA_COST", ( gc.getTeam(gc.getGame().getActiveTeam()).getResearchCost(iTech), ) ) + u"%c" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())
		screen.setLabel(szCostId, "Background", u"<font=3>" + szCostText.upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_COST + 25, self.Y_COST, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						
		# Place Required techs
		self.placePrereqs()

		# Place Allowing techs
		self.placeLeadsTo()
		
		# Place Units
		self.placeUnits()
		
		# Place buildings
		self.placeBuildings()
		
		# Place the Special abilities block
		self.placeSpecial()

		# Place the quote for this technology		
		self.placeQuote()
			

	# Place prereqs...
	def placeLeadsTo(self):

		screen = self.top.getScreen()
		
		# add pane and text
		szLeadsTo = localText.getText("TXT_KEY_PEDIA_LEADS_TO", ())
                
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, szLeadsTo, "", false, true, self.X_LEADS_TO_PANE, self.Y_LEADS_TO_PANE, self.W_LEADS_TO_PANE, self.H_LEADS_TO_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		screen.attachLabel(panelName, "", "  ")

		for j in range(gc.getNumTechInfos()):
			for k in range(gc.getNUM_OR_TECH_PREREQS()):
				iPrereq = gc.getTechInfo(j).getPrereqOrTechs(k)
				if (iPrereq == self.iTech):
        				screen.attachImageButton( panelName, "", gc.getTechInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_DERIVED_TECH, j, self.iTech, False )
			for k in range(gc.getNUM_AND_TECH_PREREQS()):
				iPrereq = gc.getTechInfo(j).getPrereqAndTechs(k)
				if (iPrereq == self.iTech):
        				screen.attachImageButton( panelName, "", gc.getTechInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_DERIVED_TECH, j, self.iTech, False )

	# Place prereqs...
	def placePrereqs(self):
		
		screen = self.top.getScreen()
		
		szRequires = localText.getText("TXT_KEY_PEDIA_REQUIRES", ())
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, szRequires, "", false, true, self.X_PREREQ_PANE, self.Y_PREREQ_PANE, self.W_PREREQ_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		screen.attachLabel(panelName, "", "  ")
		
		bFirst = True
		for j in range(gc.getNUM_AND_TECH_PREREQS()):
			eTech = gc.getTechInfo(self.iTech).getPrereqAndTechs(j)
			if (eTech > -1):
				if (not bFirst):
					screen.attachLabel(panelName, "", localText.getText("TXT_KEY_AND", ()))
				else:
					bFirst = False
				screen.attachImageButton( panelName, "", gc.getTechInfo(eTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH, eTech, j, False )
					
		# count the number of OR techs
		nOrTechs = 0
		for j in range(gc.getNUM_OR_TECH_PREREQS()):
			if (gc.getTechInfo(self.iTech).getPrereqOrTechs(j) > -1):
				nOrTechs += 1
				
		szLeftDelimeter = ""
		szRightDelimeter = ""
		#  Display a bracket if we have more than one OR tech and at least one AND tech
		if (not bFirst):
			if (nOrTechs > 1):
				szLeftDelimeter = localText.getText("TXT_KEY_AND", ()) + "( "
				szRightDelimeter = " ) "
			elif (nOrTechs > 0):
				szLeftDelimeter = localText.getText("TXT_KEY_AND", ())
			else:
				return

		if len(szLeftDelimeter) > 0:
			screen.attachLabel(panelName, "", szLeftDelimeter)
			
		bFirst = True
		for j in range(gc.getNUM_OR_TECH_PREREQS()):
			eTech = gc.getTechInfo(self.iTech).getPrereqOrTechs(j)
			if (eTech > -1):
				if (not bFirst):
					screen.attachLabel(panelName, "", localText.getText("TXT_KEY_OR", ()))
				else:
					bFirst = False
				screen.attachImageButton( panelName, "", gc.getTechInfo(eTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH, eTech, j, False )					
			
		if len(szRightDelimeter) > 0:
			screen.attachLabel(panelName, "", szRightDelimeter)

				
	# Place units...
	def placeUnits(self):

		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_UNITS_ENABLED", ()), "", false, true, self.X_UNIT_PANE, self.Y_UNIT_PANE, self.W_UNIT_PANE, self.H_UNIT_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		screen.attachLabel(panelName, "", "  ")
		
#		for j in range( gc.getNumUnitClassInfos() ):
#			eLoopUnit = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(j)
		for eLoopUnit in range(gc.getNumUnitInfos()):
			if (eLoopUnit != -1):
				if (isTechRequiredForUnit(self.iTech, eLoopUnit)):
        				screen.attachImageButton( panelName, "", gc.getUnitInfo(eLoopUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False )

	# Place buildings...
	def placeBuildings(self):

		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_BUILDINGS_ENABLED", ()), "", false, true, self.X_BUILDING_PANE, self.Y_BUILDING_PANE, self.W_BUILDING_PANE, self.H_BUILDING_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		screen.attachLabel(panelName, "", "  ")
		
#		for j in range(gc.getNumBuildingClassInfos()):
#			eLoopBuilding = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationBuildings(j)
		for eLoopBuilding in range(gc.getNumBuildingInfos()):
			if (eLoopBuilding != -1):
				if (isTechRequiredForBuilding(self.iTech, eLoopBuilding)):
        				screen.attachImageButton( panelName, "", gc.getBuildingInfo(eLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, False )
						
		for eLoopProject in range(gc.getNumProjectInfos()):
			if (isTechRequiredForProject(self.iTech, eLoopProject)):
        			screen.attachImageButton( panelName, "", gc.getProjectInfo(eLoopProject).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, eLoopProject, 1, False )

	def placeSpecial(self):

		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", true, false, self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		listName = self.top.getNextWidgetName()
		
		szSpecialText = CyGameTextMgr().getTechHelp(self.iTech, True, False, False, False, -1)[1:]
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANE+5, self.Y_SPECIAL_PANE+30, self.W_SPECIAL_PANE-35, self.H_SPECIAL_PANE-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
		

	def placeQuote(self):
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, "", "", true, true,
			self.X_QUOTE_PANE, self.Y_QUOTE_PANE, self.W_QUOTE_PANE, self.H_QUOTE_PANE, PanelStyles.PANEL_STYLE_BLUE50)

		szQuote = gc.getTechInfo(self.iTech).getQuote()
		szQuote += u"\n\n" + gc.getTechInfo(self.iTech).getCivilopedia()
		
		szQuoteTextWidget = self.top.getNextWidgetName()
		screen.addMultilineText( szQuoteTextWidget, szQuote, self.X_QUOTE_PANE + 15, self.Y_QUOTE_PANE + 15,
		    self.W_QUOTE_PANE - (15 * 2), self.H_QUOTE_PANE - (15 * 2), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeLinks(self):


		self.top.placeLinks()
		self.top.placeTechs()

								
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		return 0
