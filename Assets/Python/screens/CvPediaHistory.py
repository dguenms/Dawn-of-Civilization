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

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaHistory:
	"Civilopedia Screen for Historical Info"

	def __init__(self, main):
		self.iEntryId = -1
		self.iCivilopediaPageType = -1
		self.iEntry = -1
		self.top = main
	
		self.BUTTON_SIZE = 48

		self.X_TEXT = self.top.X_PEDIA_PAGE + 20
		self.Y_TEXT = 95
		self.H_TEXT = 700-self.Y_TEXT
		self.W_TEXT = 970-self.X_TEXT

	# Screen construction function
	def interfaceScreen(self, iEntryId):
				
		self.iEntryId = iEntryId
		self.getEntryInfoFromId(iEntryId)
	
		self.top.deleteAllWidgets()						
							
		screen = self.top.getScreen()
		
		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()

		# Header...
		szHeader = u"<font=4b>" + self.getDescription(self.iEntry).upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		if self.getLink() == WidgetTypes.WIDGET_GENERAL:
			screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, self.getLink(),  self.iEntry, -1)
		else:
			screen.setText(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, self.getLink(),  self.iEntry, -1)
			screen.setImageButton(self.top.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_CIVILOPEDIA_ICON").getPath(), self.top.X_EXIT, self.top.Y_TITLE, 32, 32, self.getLink(),  self.iEntry, -1)
		
		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.iCivilopediaPageType, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_HISTORY or bNotActive:	
			if self.top.iLastScreen != CvScreenEnums.PEDIA_MAIN:
				self.placeLinks()	
			self.top.iLastScreen = CvScreenEnums.PEDIA_HISTORY

		self.placeText()
			
	def placeText(self):
	
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
                                 self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50 )
 
		szText = self.getCivilopedia()
		screen.attachMultilineText( panelName, "Text", szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
	
	def placeLinks(self):

		self.top.placeLinks()
		self.top.placeBuildings()


	def getNumInfos(self):
		if (CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH == self.iCivilopediaPageType):
			iNum = gc.getNumTechInfos()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT == self.iCivilopediaPageType):
			iNum = gc.getNumUnitInfos()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING == self.iCivilopediaPageType):
			iNum = gc.getNumBuildingInfos()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_BONUS == self.iCivilopediaPageType):
			iNum = gc.getNumBonusInfos()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT == self.iCivilopediaPageType):
			iNum = gc.getNumImprovementInfos()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROMOTION == self.iCivilopediaPageType):
			iNum = gc.getNumPromotionInfos()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT_GROUP == self.iCivilopediaPageType):
			iNum = gc.getNumUnitCombatInfos()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV == self.iCivilopediaPageType):
			iNum = gc.getNumCivilizationInfos()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER == self.iCivilopediaPageType):
			iNum = gc.getNumLeaderHeadInfos()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_RELIGION == self.iCivilopediaPageType):
			iNum = gc.getNumReligionInfos()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC == self.iCivilopediaPageType):
			iNum = gc.getNumCivicInfos()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROJECT == self.iCivilopediaPageType):
			iNum = gc.getNumProjectInfos()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT == self.iCivilopediaPageType):
			iNum = gc.getNumConceptInfos()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPECIALIST == self.iCivilopediaPageType):
			iNum = gc.getNumSpecialistInfos()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_TERRAIN == self.iCivilopediaPageType):
			iNum = gc.getNumTerrainInfos()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_FEATURE == self.iCivilopediaPageType):
			iNum = gc.getNumFeatureInfos()
		else:
			iNum = ""
		return iNum
		
	def getDescription(self, iEntry):
		if (CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH == self.iCivilopediaPageType):
			szDescription = gc.getTechInfo(iEntry).getDescription()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT == self.iCivilopediaPageType):
			szDescription = gc.getUnitInfo(iEntry).getDescription()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING == self.iCivilopediaPageType):
			szDescription = gc.getBuildingInfo(iEntry).getDescription()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_BONUS == self.iCivilopediaPageType):
			szDescription = gc.getBonusInfo(iEntry).getDescription()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT == self.iCivilopediaPageType):
			szDescription = gc.getImprovementInfo(iEntry).getDescription()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROMOTION == self.iCivilopediaPageType):
			szDescription = gc.getPromotionInfo(iEntry).getDescription()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT_GROUP == self.iCivilopediaPageType):
			szDescription = gc.getUnitCombatInfo(iEntry).getDescription()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV == self.iCivilopediaPageType):
			szDescription = gc.getCivilizationInfo(iEntry).getDescription()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER == self.iCivilopediaPageType):
			szDescription = gc.getLeaderHeadInfo(iEntry).getDescription()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_RELIGION == self.iCivilopediaPageType):
			szDescription = gc.getReligionInfo(iEntry).getDescription()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC == self.iCivilopediaPageType):
			szDescription = gc.getCivicInfo(iEntry).getDescription()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROJECT == self.iCivilopediaPageType):
			szDescription = gc.getProjectInfo(iEntry).getDescription()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT == self.iCivilopediaPageType):
			szDescription = gc.getConceptInfo(iEntry).getDescription()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPECIALIST == self.iCivilopediaPageType):
			szDescription = gc.getSpecialistInfo(iEntry).getDescription()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_TERRAIN == self.iCivilopediaPageType):
			szDescription = gc.getTerrainInfo(iEntry).getDescription()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_FEATURE == self.iCivilopediaPageType):
			szDescription = gc.getFeatureInfo(iEntry).getDescription()
		else:
			szDescription = ""
		return szDescription
										
	def getLink(self):
		if (CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH == self.iCivilopediaPageType):
			iLink = WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT == self.iCivilopediaPageType):
			iLink = WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING == self.iCivilopediaPageType):
			iLink = WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_BONUS == self.iCivilopediaPageType):
			iLink = WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT == self.iCivilopediaPageType):
			iLink = WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROMOTION == self.iCivilopediaPageType):
			iLink = WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT_GROUP == self.iCivilopediaPageType):
			iLink = WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV == self.iCivilopediaPageType):
			iLink = WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER == self.iCivilopediaPageType):
			iLink = WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_RELIGION == self.iCivilopediaPageType):
			iLink = WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC == self.iCivilopediaPageType):
			iLink = WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROJECT == self.iCivilopediaPageType):
			iLink = WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPECIALIST == self.iCivilopediaPageType):
			iLink = WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_TERRAIN == self.iCivilopediaPageType):
			iLink = WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_FEATURE == self.iCivilopediaPageType):
			iLink = WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE
		else:
			iLink = WidgetTypes.WIDGET_GENERAL
		return iLink
										
	def getCivilopedia(self):
		if (CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH == self.iCivilopediaPageType):
			szDescription = gc.getTechInfo(self.iEntry).getCivilopedia()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT == self.iCivilopediaPageType):
			szDescription = gc.getUnitInfo(self.iEntry).getCivilopedia()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING == self.iCivilopediaPageType):
			szDescription = gc.getBuildingInfo(self.iEntry).getCivilopedia()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_BONUS == self.iCivilopediaPageType):
			szDescription = gc.getBonusInfo(self.iEntry).getCivilopedia()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT == self.iCivilopediaPageType):
			szDescription = gc.getImprovementInfo(self.iEntry).getCivilopedia()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROMOTION == self.iCivilopediaPageType):
			szDescription = gc.getPromotionInfo(self.iEntry).getCivilopedia()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT_GROUP == self.iCivilopediaPageType):
			szDescription = gc.getUnitCombatInfo(self.iEntry).getCivilopedia()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV == self.iCivilopediaPageType):
			szDescription = gc.getCivilizationInfo(self.iEntry).getCivilopedia()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER == self.iCivilopediaPageType):
			szDescription = gc.getLeaderHeadInfo(self.iEntry).getCivilopedia()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_RELIGION == self.iCivilopediaPageType):
			szDescription = gc.getReligionInfo(self.iEntry).getCivilopedia()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC == self.iCivilopediaPageType):
			szDescription = gc.getCivicInfo(self.iEntry).getCivilopedia()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROJECT == self.iCivilopediaPageType):
			szDescription = gc.getProjectInfo(self.iEntry).getCivilopedia()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT == self.iCivilopediaPageType):
			szDescription = gc.getConceptInfo(self.iEntry).getCivilopedia()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPECIALIST == self.iCivilopediaPageType):
			szDescription = gc.getSpecialistInfo(self.iEntry).getCivilopedia()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_TERRAIN == self.iCivilopediaPageType):
			szDescription = gc.getTerrainInfo(self.iEntry).getCivilopedia()
		elif (CivilopediaPageTypes.CIVILOPEDIA_PAGE_FEATURE == self.iCivilopediaPageType):
			szDescription = gc.getFeatureInfo(self.iEntry).getCivilopedia()
		else:
			szDescription = ""
		return szDescription

	def getEntryInfoFromId(self, iEntryId):
		self.iCivilopediaPageType = iEntryId % CivilopediaPageTypes.NUM_CIVILOPEDIA_PAGE_TYPES
		self.iEntry = iEntryId // CivilopediaPageTypes.NUM_CIVILOPEDIA_PAGE_TYPES

	def getIdFromEntryInfo(self, iCivilopediaPageType, iEntry):
		return (iEntry * CivilopediaPageTypes.NUM_CIVILOPEDIA_PAGE_TYPES + iCivilopediaPageType)
										
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		return 0

