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
import Consts as con #Rhye

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaBuilding:
	"Civilopedia Screen for Buildings"
	
	def __init__(self, main):
		self.iBuilding = -1
		self.bLastBuildingType = false
		self.top = main

		self.BUTTON_SIZE = 46
		
		self.X_BUILDING_PANE = self.top.X_PEDIA_PAGE + 20
		self.Y_BUILDING_PANE = self.top.Y_PEDIA_PAGE + 4
		self.W_BUILDING_PANE = 323
		self.H_BUILDING_PANE = 116
		
		self.X_BUILDING_ANIMATION = self.X_BUILDING_PANE + self.W_BUILDING_PANE + 13
		self.Y_BUILDING_ANIMATION = 62
		self.W_BUILDING_ANIMATION = 1000 - self.X_BUILDING_ANIMATION
		self.H_BUILDING_ANIMATION = 218
		self.X_ROTATION_BUILDING_ANIMATION = -20
		self.Z_ROTATION_BUILDING_ANIMATION = 30
		self.SCALE_ANIMATION = 0.7
                
		self.X_STATS_PANE = self.X_BUILDING_PANE + 110
		self.Y_STATS_PANE = self.Y_BUILDING_PANE + 17
		self.W_STATS_PANE = 190
		self.H_STATS_PANE = 110
                
		self.X_ICON = self.X_BUILDING_PANE + 8
		self.Y_ICON = self.Y_BUILDING_PANE + 8
		self.W_ICON = 100
		self.H_ICON = 100
		self.ICON_SIZE = 64

		self.X_PREREQ_PANE = self.X_BUILDING_PANE
		self.Y_PREREQ_PANE = 171
		self.W_PREREQ_PANE = 323
		self.H_PREREQ_PANE = 110

		self.X_SPECIAL_PANE = self.X_BUILDING_PANE
		self.Y_SPECIAL_PANE = self.Y_PREREQ_PANE+self.H_PREREQ_PANE
		self.W_SPECIAL_PANE = 1000 - self.X_SPECIAL_PANE
		self.H_SPECIAL_PANE = 190
		
		self.X_HISTORY_PANE = self.X_BUILDING_PANE
		self.Y_HISTORY_PANE = 475
		self.W_HISTORY_PANE = 1000 - self.X_SPECIAL_PANE
		self.H_HISTORY_PANE = 230
		
	# Screen construction function
	def interfaceScreen(self, iBuilding):	
			
		self.iBuilding = iBuilding
	
		self.top.deleteAllWidgets()						
							
		screen = self.top.getScreen()
		
		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()
		
		# Header...
		szHeader = u"<font=4b>" + gc.getBuildingInfo(self.iBuilding).getDescription().upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING, iBuilding)
		
		# Top
		if self.getBuildingType(iBuilding):
			link = CivilopediaPageTypes.CIVILOPEDIA_PAGE_WONDER
		else:
			link = CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, link, -1)

		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_BUILDING or bNotActive:	
			if self.top.iLastScreen != CvScreenEnums.PEDIA_MAIN:
				self.placeLinks()	
			self.top.iLastScreen = CvScreenEnums.PEDIA_BUILDING
					
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.X_BUILDING_PANE, self.Y_BUILDING_PANE, self.W_BUILDING_PANE, self.H_BUILDING_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		
		# Icon
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getBuildingInfo(self.iBuilding).getButton(), self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Unit animation
		screen.addBuildingGraphicGFC(self.top.getNextWidgetName(), self.iBuilding, self.X_BUILDING_ANIMATION, self.Y_BUILDING_ANIMATION, self.W_BUILDING_ANIMATION, self.H_BUILDING_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_BUILDING_ANIMATION, self.Z_ROTATION_BUILDING_ANIMATION, self.SCALE_ANIMATION, True)

		self.placeStats()
		
		self.placeRequires()

		self.placeSpecial()
		
		self.placeHistory()

			
	# Place happiness/health/commerce/great people modifiers
	def placeStats(self):

		screen = self.top.getScreen()
				
		buildingInfo = gc.getBuildingInfo(self.iBuilding)
		
		panelName = self.top.getNextWidgetName()

		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
                
		if (isWorldWonderClass(gc.getBuildingInfo(self.iBuilding).getBuildingClassType())):
			iMaxInstances = gc.getBuildingClassInfo(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()).getMaxGlobalInstances()
			szBuildingType = localText.getText("TXT_KEY_PEDIA_WORLD_WONDER", ())
			if (iMaxInstances > 1):
				szBuildingType += " " + localText.getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
				screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szBuildingType.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if (isTeamWonderClass(gc.getBuildingInfo(self.iBuilding).getBuildingClassType())):
			iMaxInstances = gc.getBuildingClassInfo(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()).getMaxTeamInstances()
			szBuildingType = localText.getText("TXT_KEY_PEDIA_TEAM_WONDER", ())
			if (iMaxInstances > 1):
				szBuildingType += " " + localText.getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
				screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szBuildingType.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if (isNationalWonderClass(gc.getBuildingInfo(self.iBuilding).getBuildingClassType())):
			iMaxInstances = gc.getBuildingClassInfo(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()).getMaxPlayerInstances()
			szBuildingType = localText.getText("TXT_KEY_PEDIA_NATIONAL_WONDER", ())
			if (iMaxInstances > 1):
				szBuildingType += " " + localText.getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
				screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szBuildingType.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if (buildingInfo.getProductionCost() > 0):
			if self.top.iActivePlayer == -1:
				szCost = localText.getText("TXT_KEY_PEDIA_COST", ((buildingInfo.getProductionCost() * gc.getDefineINT("BUILDING_PRODUCTION_PERCENT"))/100,))
			else:
				szCost = localText.getText("TXT_KEY_PEDIA_COST", (gc.getPlayer(self.top.iActivePlayer).getBuildingProductionNeeded(self.iBuilding),))
			screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szCost.upper() + u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		for k in range(YieldTypes.NUM_YIELD_TYPES):
			if (buildingInfo.getYieldChange(k) != 0):
				if (buildingInfo.getYieldChange(k) > 0):
					szSign = "+"
				else:
					szSign = ""
					
				szYield = gc.getYieldInfo(k).getDescription() + ": "
				
				szText1 = szYield.upper() + szSign + str(buildingInfo.getYieldChange(k))
				szText2 = szText1 + (u"%c" % (gc.getYieldInfo(k).getChar()))
				screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szText2 + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

			
		for k in range(CommerceTypes.NUM_COMMERCE_TYPES):
		
			iTotalCommerce = buildingInfo.getObsoleteSafeCommerceChange(k) + buildingInfo.getCommerceChange(k)
			if (iTotalCommerce != 0):
				if (iTotalCommerce > 0):
					szSign = "+"
				else:
					szSign = ""
					
				szCommerce = gc.getCommerceInfo(k).getDescription() + ": "
				
				szText1 = szCommerce.upper() + szSign + str(iTotalCommerce)
				szText2 = szText1 + (u"%c" % (gc.getCommerceInfo(k).getChar()))
				screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szText2 + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		iHappiness = buildingInfo.getHappiness()
		if self.top.iActivePlayer != -1:
			if (self.iBuilding == gc.getCivilizationInfo(gc.getPlayer(self.top.iActivePlayer).getCivilizationType()).getCivilizationBuildings(buildingInfo.getBuildingClassType())):
				iHappiness += gc.getPlayer(self.top.iActivePlayer).getExtraBuildingHappiness(self.iBuilding)
			
		if (iHappiness > 0):
			szText = localText.getText("TXT_KEY_PEDIA_HAPPY", (iHappiness,)).upper()
			screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szText + u"%c" % CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
			
		elif (iHappiness < 0):
			szText = localText.getText("TXT_KEY_PEDIA_UNHAPPY", (-iHappiness,)).upper()
			screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szText + u"%c" % CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		iHealth = buildingInfo.getHealth()
		if self.top.iActivePlayer != -1:
			if (self.iBuilding == gc.getCivilizationInfo(gc.getPlayer(self.top.iActivePlayer).getCivilizationType()).getCivilizationBuildings(buildingInfo.getBuildingClassType())):
				iHealth += gc.getPlayer(self.top.iActivePlayer).getExtraBuildingHealth(self.iBuilding)
			
		if (iHealth > 0):
			szText = localText.getText("TXT_KEY_PEDIA_HEALTHY", (iHealth,)).upper()
			screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szText + u"%c" % CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
			
		elif (iHealth < 0):
			szText = localText.getText("TXT_KEY_PEDIA_UNHEALTHY", (-iHealth,)).upper()
			screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szText + u"%c" % CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		
		if (buildingInfo.getGreatPeopleRateChange() != 0):
			szText = localText.getText("TXT_KEY_PEDIA_GREAT_PEOPLE", (buildingInfo.getGreatPeopleRateChange(),)).upper()
			screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szText + u"%c" % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
			
		screen.updateListBox(panelName)
			
	# Place prereqs (techs, resources)
	def placeRequires(self):

		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true,
                                 self.X_PREREQ_PANE, self.Y_PREREQ_PANE, self.W_PREREQ_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
						
		screen.attachLabel(panelName, "", "  ")

		# add tech buttons
		for iPrereq in range(gc.getNumTechInfos()):
			if isTechRequiredForBuilding(iPrereq, self.iBuilding):
				screen.attachImageButton( panelName, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, 1, False )

		# add resource buttons
		iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqAndBonus()
		if (iPrereq >= 0):
			screen.attachImageButton( panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )
			
		for k in range(gc.getNUM_BUILDING_PREREQ_OR_BONUSES()):
			iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqOrBonuses(k)
			if (iPrereq >= 0):
				screen.attachImageButton( panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )
		
		iCorporation = gc.getBuildingInfo(self.iBuilding).getFoundsCorporation()
		bFirst = true
		if (iCorporation >= 0):
			for k in range(gc.getNUM_CORPORATION_PREREQ_BONUSES()):
				iPrereq = gc.getCorporationInfo(iCorporation).getPrereqBonus(k)
				if (iPrereq >= 0):
					if not bFirst:
						screen.attachLabel(panelName, "", localText.getText("TXT_KEY_OR", ()))
					else:
						bFirst = false
					screen.attachImageButton( panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )
				
		# add religion button
		iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqReligion()
		if (iPrereq >= 0):
			screen.attachImageButton( panelName, "", gc.getReligionInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iPrereq, -1, False )
		
	# Place Special abilities
	def placeSpecial(self):

		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", true, false,
                                 self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		listName = self.top.getNextWidgetName()
		
		szSpecialText = CyGameTextMgr().getBuildingHelp(self.iBuilding, True, False, False, None)[1:]
		
		#Rhye - start
		if (self.iBuilding >= con.iNumBuildingsPlague):
                        szSpecialText = localText.getText("TXT_KEY_BUILDING_EMBASSY_EP", ())
                        szSpecialText += "\n"
                        szSpecialText += localText.getText("TXT_KEY_BUILDING_EMBASSY_ABILITY", ())
		#Rhye - end
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANE+5, self.Y_SPECIAL_PANE+30, self.W_SPECIAL_PANE-10, self.H_SPECIAL_PANE-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	


	def placeHistory(self):
		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "History", "", True, True,
						self.X_HISTORY_PANE, self.Y_HISTORY_PANE,
						self.W_HISTORY_PANE, self.H_HISTORY_PANE,
						PanelStyles.PANEL_STYLE_BLUE50 )
		
		textName = self.top.getNextWidgetName()
#		screen.attachMultilineText( panelName, textName, gc.getBuildingInfo(self.iBuilding).getCivilopedia(),WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.addMultilineText( textName, gc.getBuildingInfo(self.iBuilding).getCivilopedia(), self.X_HISTORY_PANE + 15, self.Y_HISTORY_PANE + 40,
		    self.W_HISTORY_PANE - (15 * 2), self.H_HISTORY_PANE - (15 * 2) - 25, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		

	def placeLinks(self):
		
		screen = self.top.getScreen()

		self.top.placeLinks()


		if self.getBuildingType(self.iBuilding):
			self.top.placeWonders()
		else:
			self.top.placeBuildings()


			
	def getBuildingType(self, iBuilding):
		if (isWorldWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			return true			

		if (isTeamWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			return true

		if (isNationalWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())): #Rhye - should be changed to move embassies to regular buildings
			return true

		# Regular building
		return false
		
	def getBuildingSortedList(self, bWonder):
		listBuildings = []
		iCount = 0
		#for iBuilding in range(gc.getNumBuildingInfos()): #Rhye
		for iBuilding in range(con.iNumBuildingsEmbassy): #Leoreth
			if (self.getBuildingType(iBuilding) == bWonder and not gc.getBuildingInfo(iBuilding).isGraphicalOnly()):
                                #Rhye - start
				#listBuildings.append(iBuilding)
				#iCount += 1
				# Leoreth: don't display embassies and corporation headquarters
                                if (iBuilding != con.iPlague and iBuilding not in range(con.iEgyEmbassy,con.iAmeEmbassy+1)):
                                        listBuildings.append(iBuilding)
                                        iCount += 1
				#Rhye - end
		
		listSorted = [(0,0)] * iCount
		iI = 0
		for iBuilding in listBuildings:
			listSorted[iI] = (gc.getBuildingInfo(iBuilding).getDescription(), iBuilding)
			iI += 1
		#Rhye - start
		#if (not bWonder):
                        #listSorted.pop(67) #ziggurat
                        #listSorted.pop(66) #rathaus
                        #listSorted.pop(54) #garden
                        #listSorted.pop(50) #hippodrome
                        #listSorted.pop(42) #seowon
                        #listSorted.pop(37) #totem                        
                        #listSorted.pop(5) #ikhanda                        
                        #listSorted.pop(1) #dun
                #Rhye - end
		#listSorted.sort() #Rhye
		return listSorted
		
													
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		return 0

