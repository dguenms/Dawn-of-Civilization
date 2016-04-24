## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Sevopedia ver 1.8
##   sevotastic.blogspot.com
##   sevotastic@yahoo.com
##


from CvPythonExtensions import *
import PyHelpers
import string
import CvUtil
import ScreenInput

import Consts as con

PyPlayer = PyHelpers.PyPlayer
PyCity = PyHelpers.PyCity

import CvScreenEnums
import CvPediaScreen		# base class
import CvPediaTech
import CvPediaUnit
import CvPediaBuilding
import CvPediaPromotion
import CvPediaUnitChart
import CvPediaBonus
import CvPediaTerrain
import CvPediaFeature
import CvPediaImprovement
import CvPediaCivic
import CvPediaCivilization
import CvPediaLeader
import CvPediaSpecialist
import CvPediaHistory
import CvPediaProject
import CvPediaReligion
import CvPediaCorporation

#import UnitUpgradesGraph	  #[MOD] UnitUpgrades  #Rhye

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaMain( CvPediaScreen.CvPediaScreen ):
	"Civilopedia Main Screen"

	def __init__(self):

		#----------------------------------------------------------------
		# SevoPedia -- Animation Toggle
		#
		# The variable below will enable/disable the animation panels
		#   on the civilopedia screens
		# To activate set self.animations = True
		# To disable set self.animations = False
		#

		self.animations = True

		#
		#-----------------------------------------------------------------
	
		self.PEDIA_MAIN_SCREEN_NAME = "PediaMainScreen"
		self.INTERFACE_ART_INFO = "SCREEN_BG_OPAQUE"

		self.WIDGET_ID = "PediaMainWidget"
		self.EXIT_ID = "PediaMainExitWidget"
		self.BACKGROUND_ID = "PediaMainBackground"
		self.TOP_PANEL_ID = "PediaMainTopPanel"
		self.BOTTOM_PANEL_ID = "PediaMainBottomPanel"
		self.BACK_ID = "PediaMainBack"
		self.NEXT_ID = "PediaMainForward"
		self.TOP_ID = "PediaMainTop"
		self.LIST_ID = "PediaMainList"
		self.SUBLIST_ID = "PediaSubList"
		self.UPGRADES_LIST = ""			# Make it accessible

		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Y_TITLE = 8
		self.DY_TEXT = 45
		
		self.X_EXIT = 915 #Rhye 925
		self.Y_EXIT = 730
						
		self.X_BACK = 50 #Rhye #700
		self.Y_BACK = 730 #Rhye #10

		self.X_FORWARD = 200 #Rhye #790
		self.Y_FORWARD = 730 #Rhye #10
		
		self.X_MENU = 450
		self.Y_MENU = 1730	# CHEATING!  Should disable this, but...easier to hide it.

		self.BUTTON_SIZE = 64
		self.BUTTON_COLUMNS = 9
	

		# RESIZE AND ADD ANOTHER PANEL TO THESE BLOCKS...

		self.ITEMS_MARGIN = 18
		self.ITEMS_SEPARATION = 2

		self.X_LINKS = 0 
		self.Y_LINKS = 51
		self.H_LINKS = 665
		self.W_LINKS = 175

		self.X_ITEMS_PANE = self.X_LINKS + self.W_LINKS +2
		self.Y_ITEMS_PANE = self.Y_LINKS
		self.H_ITEMS_PANE = self.H_LINKS
		self.W_ITEMS_PANE = 203

		self.X_PEDIA_PAGE = self.X_ITEMS_PANE + self.W_ITEMS_PANE
		self.Y_PEDIA_PAGE = self.Y_LINKS
		self.W_PEDIA_PAGE = 1024 - self.X_PEDIA_PAGE
		self.H_PEDIA_PAGE = self.H_LINKS
		
		self.nWidgetCount = 0
		
		# screen instances
		self.pediaTechScreen = CvPediaTech.CvPediaTech(self)
		self.pediaUnitScreen = CvPediaUnit.CvPediaUnit(self)
		self.pediaBuildingScreen = CvPediaBuilding.CvPediaBuilding(self)
		self.pediaPromotionScreen = CvPediaPromotion.CvPediaPromotion(self)
		self.pediaUnitChart = CvPediaUnitChart.CvPediaUnitChart(self)
		self.pediaBonus = CvPediaBonus.CvPediaBonus(self)
		self.pediaTerrain = CvPediaTerrain.CvPediaTerrain(self)
		self.pediaFeature = CvPediaFeature.CvPediaFeature(self)
		self.pediaImprovement = CvPediaImprovement.CvPediaImprovement(self)
		self.pediaCivic = CvPediaCivic.CvPediaCivic(self)
		self.pediaCivilization = CvPediaCivilization.CvPediaCivilization(self)
		self.pediaLeader = CvPediaLeader.CvPediaLeader(self)
		self.pediaSpecialist = CvPediaSpecialist.CvPediaSpecialist(self)
		self.pediaProjectScreen = CvPediaProject.CvPediaProject(self)
		self.pediaReligion = CvPediaReligion.CvPediaReligion(self)
		self.pediaCorporation = CvPediaCorporation.CvPediaCorporation(self)
		self.pediaHistorical = CvPediaHistory.CvPediaHistory(self)
				
		# used for navigating "forward" and "back" in civilopedia
		self.pediaHistory = []
		self.pediaFuture = []
		
		self.listCategories = []

		self.iCategory = -1
		self.iLastScreen = -1
		self.iActivePlayer = -1
								
		self.mapCategories = { 
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH	: self.placeTechs, 
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT	: self.placeUnits, 
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING	: self.placeBuildings, 
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_WONDER	: self.placeWonders,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_TERRAIN	: self.placeTerrains,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_FEATURE	: self.placeFeatures,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_BONUS	: self.placeBoni, 
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT	: self.placeImprovements,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPECIALIST	: self.placeSpecialists,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROMOTION	: self.placePromotions,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT_GROUP	: self.placeUnitGroups,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV	: self.placeCivs,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER	: self.placeLeaders,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_RELIGION	: self.placeReligions,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_CORPORATION	: self.placeCorporations,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC	: self.placeCivics,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROJECT	: self.placeProjects,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT	: self.placeConcepts,
 			CivilopediaPageTypes.CIVILOPEDIA_PAGE_HINTS	: self.placeHints, 

			#---------------------- [MOD] UnitUpgrades -----------------------------
#			CivilopediaPageTypes.CIVILOPEDIA_PAGE_HINTS + 1 : self.placeUpgrades, #Rhye
			#-------------------- END [MOD] UnitUpgrades ---------------------------
			}


	def createDictionaries(self):

		# This function cannot be called from __init__ because the gc stuff used
		# in linkListGraphics is not available until after all the inits are called.

		# Create a hash (well, a list of lists)
		# Items are: Original List Order (& therefore Pedia Page Index), New page order, graphic
		# Painful, but I see no other way.
		self.linkList = [	[0,0,"TECH"],				
					[1,1,"UNITS"],
					[2,9,"UNITS"],
					#Rhye - start
##					[3,18,"UNITS"],
##					[4,10,"UNITS"],	
##					[5,2,"BUILDINGS"],
##					[6,3,"BUILDINGS"],
##					[7,15,"BUILDINGS"],
##					[8,4,"TERRAINS"],
##					[9,5,"TERRAINS"],
##					[10,6,"TERRAINS"],
##					[11,7,"TERRAINS"],
##					[12,11,"CIVS"],
##					[13,12,"CIVS"],
##					[14,13,"CIVS"],
##					[15,14,"CIVS"],	
##					[16,8,"SPECIALISTS"],
##					[17,16,"HINTS"], 
##					[18,17,"HINTS"],				
					[3,10,"UNITS"],	
					[4,2,"BUILDINGS"],
					[5,3,"BUILDINGS"],
					[6,16,"BUILDINGS"],
					[7,4,"TERRAINS"],
					[8,5,"TERRAINS"],
					[9,6,"TERRAINS"],
					[10,7,"TERRAINS"],
					[11,11,"CIVS"],
					[12,12,"CIVS"],
					[13,13,"CIVS"],
					[14,14,"CIVS"],	
					[15,8,"SPECIALISTS"],
					[16,15,"HINTS"], 
					[17,17,"HINTS"],
					#Rhye - end
					]
	
		self.linkListGraphics = { 
				"TECH"	: u"%c  " %(gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar()),
				"UNITS"	: u"%c  " %(CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR)),
				"BUILDINGS" : u"%c  " %(gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()),
				"CIVS"	: u"%c  " %(gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar()),
				"TERRAINS" : u"%c  " %(gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar()),
				"SPECIALISTS" : u"%c  " %(CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR)),
				"HINTS" : u"%c  " %(gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar()),
				}

	def getScreen(self):
		return CyGInterfaceScreen(self.PEDIA_MAIN_SCREEN_NAME, CvScreenEnums.PEDIA_MAIN)
		
	def setPediaCommonWidgets(self):
		self.EXIT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"
		self.BACK_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_BACK", ()).upper() + "</font>"
		self.FORWARD_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_FORWARD", ()).upper() + "</font>"
		self.MENU_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_TOP", ()).upper() + "</font>"
		
		self.szCategoryTech = localText.getText("TXT_KEY_PEDIA_CATEGORY_TECH", ())		
		self.szCategoryUnit = localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ())		
		self.szCategoryBuilding = localText.getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ())
		self.szCategoryWonder = localText.getText("TXT_KEY_CONCEPT_WONDERS", ())			
		self.szCategoryBonus = localText.getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ())		
		self.szCategoryTerrain = localText.getText("TXT_KEY_PEDIA_CATEGORY_TERRAIN", ())		
		self.szCategoryFeature = localText.getText("TXT_KEY_PEDIA_CATEGORY_FEATURE", ())		
		self.szCategoryImprovement = localText.getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ())		
		self.szCategorySpecialist = localText.getText("TXT_KEY_PEDIA_CATEGORY_SPECIALIST", ())		
		self.szCategoryPromotion = localText.getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ())		
		self.szCategoryUnitCombat = localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIT_COMBAT", ())		
		self.szCategoryCiv = localText.getText("TXT_KEY_PEDIA_CATEGORY_CIV", ())		
		self.szCategoryLeader = localText.getText("TXT_KEY_PEDIA_CATEGORY_LEADER", ())		
		self.szCategoryReligion = localText.getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ())		
		self.szCategoryCorporation = localText.getText("TXT_KEY_CONCEPT_CORPORATIONS", ())		
		self.szCategoryCivic = localText.getText("TXT_KEY_PEDIA_CATEGORY_CIVIC", ())		
		self.szCategoryProject = localText.getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ())		
		self.szCategoryConcept = localText.getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT", ())
		self.szCategoryHints = localText.getText("TXT_KEY_PEDIA_CATEGORY_HINTS", ())

		#------------------------[MOD] UnitUpgrades ---------------------------------------
#		self.szCategoryUpgrades = localText.getText("TXT_KEY_PEDIA_CATEGORY_UPGRADES", ()) #Rhye
		#----------------------END [MOD] UnitUpgrades -------------------------------------

		self.listCategories = [ self.szCategoryTech, 
					self.szCategoryUnit,
					self.szCategoryBuilding,
					self.szCategoryWonder,
					self.szCategoryTerrain, 
					self.szCategoryFeature, 
					self.szCategoryBonus, 
					self.szCategoryImprovement, 
					self.szCategorySpecialist, 
					self.szCategoryPromotion, 
					self.szCategoryUnitCombat,
					self.szCategoryCiv, 
					self.szCategoryLeader,
					self.szCategoryReligion, 
					self.szCategoryCorporation, 
					self.szCategoryCivic, 
					self.szCategoryProject,
					self.szCategoryConcept,
					self.szCategoryHints, #Rhye
#					self.szCategoryUpgrades,   	# [MOD] UnitUpgrades
					]
								
		# Create a new screen
		screen = self.getScreen()
		screen.setRenderInterfaceOnly(True);
		screen.setScreenGroup(1)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		
		# Set background
		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel(self.TOP_PANEL_ID, u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel(self.BOTTOM_PANEL_ID, u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		
		# Exit button
		screen.setText(self.EXIT_ID, "Background", self.EXIT_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.X_EXIT, self.Y_EXIT, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

		# Back
		screen.setText(self.BACK_ID, "Background", self.BACK_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.X_BACK, self.Y_BACK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_BACK, 1, -1)
			
		# Forward
		screen.setText(self.NEXT_ID, "Background", self.FORWARD_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.X_FORWARD, self.Y_FORWARD, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_FORWARD, 1, -1)

		# List on the LEFT!
		screen.addListBoxGFC(self.LIST_ID, "", self.X_LINKS, self.Y_LINKS, self.W_LINKS, self.H_LINKS, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.LIST_ID, True)
		screen.setStyle(self.LIST_ID, "Table_StandardCiv_Style")

		self.createDictionaries()

		
	# Screen construction function
	# Only called on click to FAR LEFT column (LIST_ID)
	def showScreen(self, iCategory):
		self.iCategory = iCategory

		self.deleteAllWidgets()						
							
		screen = self.getScreen()
		
		bNotActive = (not screen.isActive())
		if bNotActive:
			self.setPediaCommonWidgets()

		# Header...
		#szHeader = u"<font=4b>" +localText.getText("TXT_KEY_WIDGET_HELP", ()).upper() + u"</font>"
		szHeader = u"<font=4b>CIVILOPEDIA</font>"
		szHeaderId = self.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_DESCRIPTION, -1, -1)

		self.panelName = self.getNextWidgetName()
		# I can't just disable this panel.
		# Just 0 size it.
		screen.addPanel(self.panelName, "", "", true, true,
			self.X_PEDIA_PAGE, self.Y_PEDIA_PAGE, 0, self.H_PEDIA_PAGE, PanelStyles.PANEL_STYLE_MAIN)

		
		if self.iLastScreen	!= CvScreenEnums.PEDIA_MAIN or bNotActive:
			self.iLastScreen = CvScreenEnums.PEDIA_MAIN

		self.placeLinks()
		
		# Note to self: this is a deceptively important function here.  It actually calls the 
		# subroutines placeUnits, placeTech, etc based on the hash self.mapCategories.
		# The hash returns the function name, which is subsequently called by the command itself.
		# Tricky, but cool.

		if (self.mapCategories.has_key(iCategory)):
			self.mapCategories.get(iCategory)()
			
# BEGIN MAIN RE-WRITE for SEVOPEDIA
# (NOTE: There have been changes throughout the code!)
	
	def placeTechs(self):

		tList = self.getSortedList( gc.getNumTechInfos(), gc.getTechInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, gc.getTechInfo)	
	
	
	def placeUnits(self):

		tList = self.getSortedList( gc.getNumUnitInfos(), gc.getUnitInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, gc.getUnitInfo)	

	
	def placeBuildings(self):

		tList = self.pediaBuildingScreen.getBuildingSortedList(false)
	
		#tList = self.getSortedList( gc.getNumBuildingInfos(), gc.getBuildingInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, gc.getBuildingInfo)	


	def placeWonders(self):

		tList = self.pediaBuildingScreen.getBuildingSortedList(true)

		#tList = self.getSortedList( gc.getNumBuildingInfos(), gc.getBuildingInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, gc.getBuildingInfo)	

	
	def placeBoni(self):

		tList = self.getSortedList( gc.getNumBonusInfos(), gc.getBonusInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, gc.getBonusInfo)	

	
	def placeImprovements(self):

		tList = self.getSortedList( gc.getNumImprovementInfos(), gc.getImprovementInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, gc.getImprovementInfo)
			

	def placePromotions(self):

		tList = self.getSortedList( gc.getNumPromotionInfos(), gc.getPromotionInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, gc.getPromotionInfo)
												

	def placeUnitGroups(self):

		tList = self.getSortedList( gc.getNumUnitCombatInfos(), gc.getUnitCombatInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, gc.getUnitCombatInfo)
									

	def placeCivs(self):

		tList = self.getSortedList( gc.getNumCivilizationInfos(), gc.getCivilizationInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, gc.getCivilizationInfo)


	def placeLeaders(self):
	
		tList = self.getSortedList( gc.getNumLeaderHeadInfos(), gc.getLeaderHeadInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, gc.getLeaderHeadInfo)

			
	def placeReligions(self):

		tList = self.getSortedList( gc.getNumReligionInfos(), gc.getReligionInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, gc.getReligionInfo)
	def placeCorporations(self):

		tList = self.getSortedList( gc.getNumCorporationInfos(), gc.getCorporationInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, gc.getCorporationInfo)

							
	def placeCivics(self):

		tList = self.getSortedList( gc.getNumCivicInfos(), gc.getCivicInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, gc.getCivicInfo)

		
	def placeProjects(self):

		tList = self.getSortedList( gc.getNumProjectInfos(), gc.getProjectInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, gc.getProjectInfo)

	def placeTerrains(self):

		tList = self.getSortedList( gc.getNumTerrainInfos(), gc.getTerrainInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, gc.getTerrainInfo)


	def placeFeatures(self):

		tList = self.getSortedList( gc.getNumFeatureInfos(), gc.getFeatureInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, gc.getFeatureInfo)

							
	def placeSpecialists(self):

		tList = self.getSortedList( gc.getNumSpecialistInfos(), gc.getSpecialistInfo )
		self.displayTopics(tList, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, gc.getSpecialistInfo)


	def displayTopics(self, tList, widgeyType, buttonType):

		screen = self.getScreen()

		nColumns = 1
		screen.addTableControlGFC(self.SUBLIST_ID, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE, self.W_ITEMS_PANE, self.H_ITEMS_PANE, False, False, 16, 16, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(self.SUBLIST_ID, True)
		screen.setStyle(self.SUBLIST_ID, "Table_StandardCiv_Style")

		for i in range(nColumns):
			screen.setTableColumnHeader(self.SUBLIST_ID, i, "", self.W_ITEMS_PANE/nColumns)
		
		iCounter = 0
		iNumRows = 0
		
		#Rhye - start
#		if (widgeyType == WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS):
#			pass
		if (widgeyType == WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER):
			tList.pop(con.iAlpArslan)
			tList.pop(con.iAbuBakr)
			tList.pop(con.iSittingBull)
			tList.pop(con.iNativeLeader)
			tList.pop(con.iIndependentLeader)
			tList.pop(con.iBrennus)
			tList.pop(con.iBoudica)
			tList.pop(con.iBarbarianLeader)
		if (widgeyType == WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV):
			tList.pop(con.iCivNative)
			tList.pop(con.iCivIndependent2)
			tList.pop(con.iCivIndependent)
			tList.pop(con.iCivZulu)
			tList.pop(con.iCivSumeria)
			tList.pop(con.iCivNativeAmericans)
			tList.pop(con.iCivSeljuks)
			tList.pop(con.iCivCeltia)
			tList.pop(con.iCivMinor)
			tList.pop(con.iCivBarbarian)
			pass
		if (widgeyType == WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING): #all -3 because there aren't palaces in the list
			#removed in CvPediaBuilding.py
			pass
		if (widgeyType == WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT):
			pass
		if (widgeyType == WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT):
			tList.pop(1) #water worked
			tList.pop(0) #land worked
			pass
		if (widgeyType == WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN):
			tList.pop(8) #hill
			tList.pop(7) #peak
			pass		  
		    
		tList.sort()
		#Rhye - end

		
		for item in tList:

			# This line disables the popup text on 'pedia scroll over...hopefully it works
			
			iColumn = iCounter % nColumns
			iRow = iCounter // nColumns
			#Rhye - start
##			if iRow >= iNumRows:
##				iNumRows += 1
##				screen.appendTableRow(self.SUBLIST_ID)
##			screen.setTableText(self.SUBLIST_ID, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", buttonType(item[1]).getButton(), widgeyType, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
##			iCounter += 1
			
			if (widgeyType == WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV):			    
				if (gc.getCivilizationInfo(item[1]).isPlayable()):
					if iRow >= iNumRows:
						iNumRows += 1
						screen.appendTableRow(self.SUBLIST_ID)
					screen.setTableText(self.SUBLIST_ID, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getCivilizationInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
					iCounter += 1
			else:
				if iRow >= iNumRows:
					iNumRows += 1
					screen.appendTableRow(self.SUBLIST_ID)
				screen.setTableText(self.SUBLIST_ID, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", buttonType(item[1]).getButton(), widgeyType, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
				iCounter += 1
			#Rhye - end

				    
	
	def placeConcepts(self):

		tList = self.getSortedList( gc.getNumConceptInfos(), gc.getConceptInfo )
				
		screen = self.getScreen()
		screen.clearListBoxGFC(self.SUBLIST_ID)

		screen.addListBoxGFC( self.SUBLIST_ID, "", self.X_ITEMS_PANE, self.Y_ITEMS_PANE, self.W_ITEMS_PANE, self.H_ITEMS_PANE, TableStyles.TABLE_STYLE_STANDARD ) 
		screen.enableSelect(self.SUBLIST_ID, True)
		screen.setStyle(self.SUBLIST_ID, "Table_StandardCiv_Style")
		
		for topic in tList:
			# Not sure why, but when using _NO_HELP, the topic[1] and PageType have to be flipped. Painful...
			screen.appendListBoxString(self.SUBLIST_ID, topic[0], WidgetTypes.WIDGET_PEDIA_DESCRIPTION_NO_HELP, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, topic[1], CvUtil.FONT_LEFT_JUSTIFY)

						
	def placeHints(self):
		screen = self.getScreen()

		screen.deleteWidget("PediaSubList")

		# Lay down some Blooo
		#self.blooPanelName = self.getNextWidgetName()
		#screen.addPanel(self.blooPanelName, "", "", true, true,
		#	self.X_ITEMS_PANE, self.Y_ITEMS_PANE, self.W_ITEMS_PANE + self.W_PEDIA_PAGE-4, self.H_PEDIA_PAGE, PanelStyles.PANEL_STYLE_MAIN)

		self.szHints = self.getNextWidgetName()
		screen.addListBoxGFC( self.szHints, "",
				      self.X_ITEMS_PANE+20, self.Y_ITEMS_PANE, self.W_ITEMS_PANE + self.W_PEDIA_PAGE-40, self.H_ITEMS_PANE, TableStyles.TABLE_STYLE_STANDARD )
		
		szHintsText = CyGameTextMgr().buildHintsList()
		hintText = string.split( szHintsText, "\n" )
		for hint in hintText:
			if len( hint ) != 0:
				screen.appendListBoxStringNoUpdate( self.szHints, hint, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.updateListBox(self.szHints)


	####################### [MOD: VOVAN] UnitUpgrades #######################
		#Rhye - start comment
##	def placeUpgrades(self):
##		screen = self.getScreen()
##
##		if self.iLastScreen != CvScreenEnums.PEDIA_UPGRADES:
##			self.iLastScreen = CvScreenEnums.PEDIA_UPGRADES
##		
##		# Strangely, this command works:
##		self.getScreen().deleteWidget("PediaSubList")
##
##		self.UPGRADES_LIST = self.getNextWidgetName()
##
##		screen.addScrollPanel( self.UPGRADES_LIST, u"", self.X_ITEMS_PANE, self.Y_PEDIA_PAGE, self.W_PEDIA_PAGE + self.W_ITEMS_PANE, self.H_PEDIA_PAGE-50, PanelStyles.PANEL_STYLE_STANDARD )
##		screen.setActivation( self.UPGRADES_LIST, ActivationTypes.ACTIVATE_NORMAL )
##		
##		upgradesGraph = UnitUpgradesGraph.UnitUpgradesGraph(self)
##		graphs = upgradesGraph.getGraph()
##		offset = 0
##		unitWidth = self.BUTTON_SIZE
##		unitHeight = self.BUTTON_SIZE
##		hm = 60
##		vm = 20
##		for graph in graphs:
##			layers = upgradesGraph.layoutLayers(graph, offset, unitWidth, unitHeight, hm, vm)
##			for layer in layers:
##				for unit,position in layer:
##					if unit > -1:
##						screen.setImageButtonAt("", self.UPGRADES_LIST, gc.getUnitInfo(unit).getButton(), position[0], position[1], self.BUTTON_SIZE, self.BUTTON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, unit, 1)
##			upgradesGraph.drawGraphArrows(self, graph, layers)
##			offset += upgradesGraph.calculateLayerHeight(upgradesGraph.maximumLayerSize(layers), unitHeight, vm) + vm
		#Rhye - end comment
	##################### END [MOD: VOVAN] UnitUpgrades #####################



										
	def placeLinks(self):
		
		link = 0
		screen = self.getScreen()
		
		screen.clearListBoxGFC(self.LIST_ID)
	
		for item in self.linkList:
			# Note: This was originally intended to place spacers between subjects...
			# I'm not using it, but I'll leave the code for now just in case I change my mind.
			if item[0] == -1:
				screen.appendListBoxString(self.LIST_ID, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
			else:
				lChar = self.linkListGraphics[item[2]]		
				screen.appendListBoxString(self.LIST_ID, lChar + self.listCategories[item[1]], WidgetTypes.WIDGET_PEDIA_MAIN, item[1], 0, CvUtil.FONT_LEFT_JUSTIFY )
				if item[1] == self.iCategory:
					link = item[0]

		screen.setSelectedListBoxStringGFC(self.LIST_ID, link)

					
	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName
		
	def pediaJump(self, iScreen, iEntry, bRemoveFwdList):
	
		if (iEntry < 0):
			return

		self.iActivePlayer = gc.getGame().getActivePlayer()

		self.pediaHistory.append((iScreen, iEntry))
		if (bRemoveFwdList):
			self.pediaFuture = []

		if (iScreen == CvScreenEnums.PEDIA_MAIN):
			self.showScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_TECH):
			self.pediaTechScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_UNIT):
			self.pediaUnitScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_BUILDING):
			self.pediaBuildingScreen.interfaceScreen(iEntry)	
		elif (iScreen == CvScreenEnums.PEDIA_PROMOTION):
			self.pediaPromotionScreen.interfaceScreen(iEntry)	
		elif (iScreen == CvScreenEnums.PEDIA_UNIT_CHART):
			self.pediaUnitChart.interfaceScreen(iEntry)	
		elif (iScreen == CvScreenEnums.PEDIA_BONUS):
			self.pediaBonus.interfaceScreen(iEntry)	
		elif (iScreen == CvScreenEnums.PEDIA_TERRAIN):
			self.pediaTerrain.interfaceScreen(iEntry)	
		elif (iScreen == CvScreenEnums.PEDIA_FEATURE):
			self.pediaFeature.interfaceScreen(iEntry)	
		elif (iScreen == CvScreenEnums.PEDIA_IMPROVEMENT):
			self.pediaImprovement.interfaceScreen(iEntry)	
		elif (iScreen == CvScreenEnums.PEDIA_CIVIC):
			self.pediaCivic.interfaceScreen(iEntry)	
		elif (iScreen == CvScreenEnums.PEDIA_CIVILIZATION):
			self.pediaCivilization.interfaceScreen(iEntry)	
		elif (iScreen == CvScreenEnums.PEDIA_LEADER):
			self.pediaLeader.interfaceScreen(iEntry)	
		elif (iScreen == CvScreenEnums.PEDIA_SPECIALIST):
			self.pediaSpecialist.interfaceScreen(iEntry)	
		elif (iScreen == CvScreenEnums.PEDIA_PROJECT):
			self.pediaProjectScreen.interfaceScreen(iEntry)	
		elif (iScreen == CvScreenEnums.PEDIA_RELIGION):
			self.pediaReligion.interfaceScreen(iEntry)	
		elif (iScreen == CvScreenEnums.PEDIA_CORPORATION):
			self.pediaCorporation.interfaceScreen(iEntry)	
		elif (iScreen == CvScreenEnums.PEDIA_HISTORY):
			self.pediaHistorical.interfaceScreen(iEntry)	

	def back(self):
		print "pedia back"
		if (len(self.pediaHistory) > 1):
			self.pediaFuture.append(self.pediaHistory.pop())
			current = self.pediaHistory.pop()
			self.pediaJump(current[0], current[1], False)
		return 1
		
	def forward(self):
		print "pedia fwd"
		if (self.pediaFuture):
			current = self.pediaFuture.pop()
			self.pediaJump(current[0], current[1], False)
		return 1
		
	def pediaShow(self):
		if (not self.pediaHistory):
			self.pediaHistory.append((CvScreenEnums.PEDIA_MAIN, 0))
			
		current = self.pediaHistory.pop()
		
		# erase history so it doesn't grow too large during the game
		self.pediaFuture = []
		self.pediaHistory = []
		
		# jump to the last screen that was up
		self.pediaJump(current[0], current[1], False)
		
	def link(self, szLink):
		if (szLink == "PEDIA_MAIN_TECH"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH), True)			
		if (szLink == "PEDIA_MAIN_UNIT"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT), True)			
		if (szLink == "PEDIA_MAIN_BUILDING"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING), True)			
		if (szLink == "PEDIA_MAIN_TERRAIN"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_TERRAIN), True)			
		if (szLink == "PEDIA_MAIN_FEATURE"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_FEATURE), True)			
		if (szLink == "PEDIA_MAIN_BONUS"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_BONUS), True)			
		if (szLink == "PEDIA_MAIN_IMPROVEMENT"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT), True)			
		if (szLink == "PEDIA_MAIN_SPECIALIST"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPECIALIST), True)			
		if (szLink == "PEDIA_MAIN_PROMOTION"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROMOTION), True)			
		if (szLink == "PEDIA_MAIN_UNIT_GROUP"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT_GROUP), True)			
		if (szLink == "PEDIA_MAIN_CIV"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV), True)			
		if (szLink == "PEDIA_MAIN_LEADER"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER), True)			
		if (szLink == "PEDIA_MAIN_RELIGION"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_RELIGION), True)			
		if (szLink == "PEDIA_MAIN_CORPORATION"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CORPORATION), True)			
		if (szLink == "PEDIA_MAIN_CIVIC"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC), True)			
		if (szLink == "PEDIA_MAIN_PROJECT"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROJECT), True)			
		if (szLink == "PEDIA_MAIN_CONCEPT"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT), True)			
		if (szLink == "PEDIA_MAIN_HINTS"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_HINTS), True)			

		for i in range(gc.getNumConceptInfos()):
			if (gc.getConceptInfo(i).isMatchForLink(szLink, False)):
				iEntryId = self.pediaHistorical.getIdFromEntryInfo(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, i)
				return self.pediaJump(CvScreenEnums.PEDIA_HISTORY, iEntryId, True)
		for i in range(gc.getNumTechInfos()):
			if (gc.getTechInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_TECH, i, True)
		for i in range(gc.getNumUnitInfos()):
			if (gc.getUnitInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_UNIT, i, True)
		for i in range(gc.getNumCorporationInfos()):
			if (gc.getCorporationInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_CORPORATION, i, True)
		for i in range(gc.getNumBuildingInfos()):
			if (gc.getBuildingInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_BUILDING, i, True)
		for i in range(gc.getNumPromotionInfos()):
			if (gc.getPromotionInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_PROMOTION, i, True)
		for i in range(gc.getNumUnitCombatInfos()):
			if (gc.getUnitCombatInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_UNIT_CHART, i, True)				
		for i in range(gc.getNumBonusInfos()):
			if (gc.getBonusInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_BONUS, i, True)				
		for i in range(gc.getNumTerrainInfos()):
			if (gc.getTerrainInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_TERRAIN, i, True)
		for i in range(gc.getNumFeatureInfos()):
			if (gc.getFeatureInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_FEATURE, i, True)				
		for i in range(gc.getNumImprovementInfos()):
			if (gc.getImprovementInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_IMPROVEMENT, i, True)
		for i in range(gc.getNumCivicInfos()):
			if (gc.getCivicInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_CIVIC, i, True)
		for i in range(gc.getNumCivilizationInfos()):
			if (gc.getCivilizationInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_CIVILIZATION, i, True)
		for i in range(gc.getNumLeaderHeadInfos()):
			if (gc.getLeaderHeadInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_LEADER, i, True)
		for i in range(gc.getNumSpecialistInfos()):
			if (gc.getSpecialistInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_SPECIALIST, i, True)
		for i in range(gc.getNumProjectInfos()):
			if (gc.getProjectInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_PROJECT, i, True)
		for i in range(gc.getNumReligionInfos()):
			if (gc.getReligionInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_RELIGION, i, True)
																
	def deleteAllWidgets(self):
		screen = self.getScreen()
		iNumWidgets = self.nWidgetCount
		self.nWidgetCount = 0
		for i in range(iNumWidgets):
			screen.deleteWidget(self.getNextWidgetName())
		self.nWidgetCount = 0
		
		
			
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		# redirect to proper screen if necessary
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_TECH):
			return self.pediaTechScreen.handleInput(inputClass)
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_UNIT):
			return self.pediaUnitScreen.handleInput(inputClass)
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_BUILDING):
			return self.pediaBuildingScreen.handleInput(inputClass)
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_PROMOTION):
			return self.pediaPromotionScreen.handleInput(inputClass)
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_UNIT_CHART):
			return self.pediaUnitChart.handleInput(inputClass)
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_BONUS):
			return self.pediaBonus.handleInput(inputClass)
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_TERRAIN):
			return self.pediaTerrain.handleInput(inputClass)
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_FEATURE):
			return self.pediaFeature.handleInput(inputClass)
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_IMPROVEMENT):
			return self.pediaImprovement.handleInput(inputClass)
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_CIVIC):
			return self.pediaCivic.handleInput(inputClass)
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_CIVILIZATION):
			return self.pediaCivilization.handleInput(inputClass)
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_LEADER):
			return self.pediaLeader.handleInput(inputClass)
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_SPECIALIST):
			return self.pediaSpecialist.handleInput(inputClass)
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_PROJECT):
			return self.pediaProjectScreen.handleInput(inputClass)
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_RELIGION):
			return self.pediaReligion.handleInput(inputClass)
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_CORPORATION):
			return self.pediaCorporation.handleInput(inputClass)
		if (inputClass.getPythonFile() == CvScreenEnums.PEDIA_HISTORY):
			return self.pediaHistorical.handleInput(inputClass)
						
		return 0

