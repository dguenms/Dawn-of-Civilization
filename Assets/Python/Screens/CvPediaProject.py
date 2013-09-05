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
import string

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaProject:
	"Civilopedia Screen for Projects"
	
	def __init__(self, main):
		self.iProject = -1
		self.top = main

		
		self.X_MAIN_PANE = self.top.X_PEDIA_PAGE + 20
		self.Y_MAIN_PANE = 63
		self.W_MAIN_PANE = 270
		self.H_MAIN_PANE = 116

		self.X_ICON = self.X_MAIN_PANE + 8
		self.Y_ICON = self.Y_MAIN_PANE + 8
		self.W_ICON = 100
		self.H_ICON = 100
		self.ICON_SIZE = 64

		self.ICON_SIZE = 64

		self.X_STATS_PANE = self.X_ICON + self.W_ICON
		self.Y_STATS_PANE = 93
		self.W_STATS_PANE = 200
		self.H_STATS_PANE = 200

		self.X_REQUIRES = self.X_MAIN_PANE + self.W_MAIN_PANE + 10
		self.Y_REQUIRES = 63
		self.W_REQUIRES = 1000 - self.X_REQUIRES
		self.H_REQUIRES = 116

		self.X_SPECIAL = self.X_MAIN_PANE
		self.Y_SPECIAL = self.Y_MAIN_PANE + self.H_MAIN_PANE + 10
		self.W_SPECIAL = 1000 - self.X_SPECIAL
		self.H_SPECIAL = 230

		self.X_TEXT = self.X_MAIN_PANE
		self.Y_TEXT = self.Y_SPECIAL + self.H_SPECIAL + 20
		self.W_TEXT = 1000 - self.X_MAIN_PANE
		self.H_TEXT = 700 - self.Y_TEXT
		
	# Screen construction function
	def interfaceScreen(self, iProject):	
			
		self.iProject = iProject
	
		self.top.deleteAllWidgets()						
							
		screen = self.top.getScreen()
		
		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()

		# Header...
		szHeader = u"<font=4b>" + gc.getProjectInfo(self.iProject).getDescription().upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROJECT, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_PROJECT or bNotActive:	
			if self.top.iLastScreen != CvScreenEnums.PEDIA_MAIN:
				self.placeLinks()		
			self.top.iLastScreen = CvScreenEnums.PEDIA_PROJECT
			
		# Icon
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False,
		    self.X_MAIN_PANE, self.Y_MAIN_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false,
		    self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getProjectInfo(self.iProject).getButton(),
		    self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getProjectInfo(self.iProject).getButton(), self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, WidgetTypes.WIDGET_GENERAL, self.iProject, -1 )
		
		self.placeStats()
		self.placeRequires()
		self.placeSpecial()
		self.placeText()
		
		return
			
	# Place happiness/health/commerce/great people modifiers
	def placeStats(self):

		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addListBoxGFC(panelName, "",
		    self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
		
		projectInfo = gc.getProjectInfo(self.iProject)
	
		if (isWorldProject(self.iProject)):
			iMaxInstances = gc.getProjectInfo(self.iProject).getMaxGlobalInstances()
			szProjectType = localText.getText("TXT_KEY_PEDIA_WORLD_PROJECT", ())
			if (iMaxInstances > 1):
				szProjectType += " " + localText.getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
			screen.appendListBoxString(panelName, u"<font=3>" + szProjectType.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
#			screen.attachTextGFC(panelName, "", szProjectType.upper(), FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		if (isTeamProject(self.iProject)):
			iMaxInstances = gc.getProjectInfo(self.iProject).getMaxTeamInstances()
			szProjectType = localText.getText("TXT_KEY_PEDIA_TEAM_PROJECT", ())
			if (iMaxInstances > 1):
				szProjectType += " " + localText.getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
			screen.appendListBoxString(panelName, u"<font=3>" + szProjectType.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
#			screen.attachTextGFC(panelName, "", szProjectType.upper(), FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		if (projectInfo.getProductionCost() > 0):
			if self.top.iActivePlayer == -1:
				szCost = localText.getText("TXT_KEY_PEDIA_COST", ((projectInfo.getProductionCost() * gc.getDefineINT("BUILDING_PRODUCTION_PERCENT"))/100,))
			else:
				szCost = localText.getText("TXT_KEY_PEDIA_COST", (gc.getActivePlayer().getProjectProductionNeeded(self.iProject),))
			screen.appendListBoxString(panelName, u"<font=3>" + szCost.upper() + u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
#			screen.attachTextGFC(panelName, "", szCost.upper() + u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar(), FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
	# Place prereqs (techs, resources)
	def placeRequires(self):

		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true,
				 self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.enableSelect(panelName, False)
		screen.attachLabel(panelName, "", "  ")
									
		# add tech buttons
		iPrereq = gc.getProjectInfo(self.iProject).getTechPrereq()
		if (iPrereq >= 0):
			screen.attachImageButton( panelName, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, 1, False )
		
	# Place Special abilities
	def placeSpecial(self):
		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false,
				 self.X_SPECIAL, self.Y_SPECIAL, self.W_SPECIAL, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )
		
		listName = self.top.getNextWidgetName()
		
		szSpecialText = CyGameTextMgr().getProjectHelp(self.iProject, True, None)
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL+5, self.Y_SPECIAL+5, self.W_SPECIAL-10, self.H_SPECIAL-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
		
	def placeText(self):
		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
				 self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50 )
 
		szText = gc.getProjectInfo(self.iProject).getCivilopedia()
		screen.attachMultilineText( panelName, "Text", szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
	
	def placeLinks(self):

		self.top.placeLinks()
		self.top.placeProjects()

			
	def getProjectType(self, iProject):
		if (isWorldProject(iProject)):
			return (3)			

		if (isTeamProject(iProject)):
			return (2)

		# Regular project
		return (1)

	def getProjectSortedList(self):
		listOfAllTypes = []
		for iBuildingType in range(4):		
			listBuildings = []
			iCount = 0
			for iBuilding in range(gc.getNumProjectInfos()):
				if (self.getProjectType(iBuilding) == iBuildingType):
					listBuildings.append(iBuilding)
					iCount += 1
			
			listSorted = [(0,0)] * iCount
			iI = 0
			for iBuilding in listBuildings:
				listSorted[iI] = (gc.getProjectInfo(iBuilding).getDescription(), iBuilding)
				iI += 1
			listSorted.sort()
			for i in range(len(listSorted)):
				listOfAllTypes.append(listSorted[i])
		return listOfAllTypes

					
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		return 0

