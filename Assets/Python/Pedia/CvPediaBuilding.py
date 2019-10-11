from CvPythonExtensions import *
import CvUtil
from RFCUtils import utils
from Consts import *

gc = CyGlobalContext()



class CvPediaBuilding:
	def __init__(self, main):
		self.iBuilding = -1
		self.top = main

		self.X_INFO_PANE = self.top.X_PEDIA_PAGE
		self.Y_INFO_PANE = self.top.Y_PEDIA_PAGE
		self.W_INFO_PANE = 340
		self.H_INFO_PANE = 120

		self.W_ICON = 100
		self.H_ICON = 100
		self.X_ICON = self.X_INFO_PANE + 10
		self.Y_ICON = self.Y_INFO_PANE + 10
		self.ICON_SIZE = 64

		self.X_INFO_TEXT = self.X_INFO_PANE + 110
		self.Y_INFO_TEXT = self.Y_ICON + 5
		self.W_INFO_TEXT = 220
		self.H_INFO_TEXT = self.H_INFO_PANE - 20

		self.X_REQUIRES = self.X_INFO_PANE
		self.Y_REQUIRES = self.Y_INFO_PANE + self.H_INFO_PANE + 10
		self.W_REQUIRES = self.W_INFO_PANE
		self.H_REQUIRES = 110

		self.X_BUILDING_ANIMATION = self.X_INFO_PANE + self.W_INFO_PANE + 10
		self.Y_BUILDING_ANIMATION = self.Y_INFO_PANE + 7
		self.W_BUILDING_ANIMATION = self.top.R_PEDIA_PAGE - self.X_BUILDING_ANIMATION
		self.H_BUILDING_ANIMATION = self.H_INFO_PANE + self.H_REQUIRES + 3
		self.X_ROTATION_BUILDING_ANIMATION = -20
		self.Z_ROTATION_BUILDING_ANIMATION = 30
		self.SCALE_ANIMATION = 0.7

		self.X_EFFECTS = self.X_REQUIRES
		self.Y_EFFECTS = self.Y_REQUIRES + self.H_REQUIRES + 10
		self.W_EFFECTS = self.top.R_PEDIA_PAGE - self.X_EFFECTS
		self.H_EFFECTS = 190

		self.X_HISTORY = self.X_EFFECTS
		self.W_HISTORY = self.W_EFFECTS
		self.Y_HISTORY = self.Y_EFFECTS + self.H_EFFECTS + 10
		self.H_HISTORY = self.top.B_PEDIA_PAGE - self.Y_HISTORY



	def interfaceScreen(self, iBuilding):
		self.iBuilding = iBuilding
		screen = self.top.getScreen()
		if iBuilding == iHubbleSpaceTelescope:
			self.spaceGraphic(iBuilding)
		else:
			screen.addBuildingGraphicGFC(self.top.getNextWidgetName(), self.iBuilding, self.X_BUILDING_ANIMATION, self.Y_BUILDING_ANIMATION, self.W_BUILDING_ANIMATION, self.H_BUILDING_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_BUILDING_ANIMATION, self.Z_ROTATION_BUILDING_ANIMATION, self.SCALE_ANIMATION, True)

		self.placeInfo()
		self.placeRequires()
		self.placeEffects()
		self.placeHistory()

	def spaceGraphic(self, iBuilding):
		screen = self.top.getScreen()
		szImage = self.top.getNextWidgetName()
		screen.addModelGraphicGFC(szImage, "Art/Interface/Screens/Civilopedia/Space_Environment.nif", self.X_BUILDING_ANIMATION, self.Y_BUILDING_ANIMATION, self.W_BUILDING_ANIMATION, self.H_BUILDING_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_BUILDING_ANIMATION,  self.Z_ROTATION_BUILDING_ANIMATION, 1.0)
		
		if iBuilding == iHubbleSpaceTelescope: #Hubble has a special nif file because it is so high in the air
			screen.addToModelGraphicGFC(szImage, "Art/Structures/Wonders/HubbleSpaceTelescope/Hubble_Pedia.nif")
		else:
			screen.addToModelGraphicGFC(szImage, gc.getBuildingInfo(iBuilding).getArtInfo().getNIF())


	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		BuildingInfo = gc.getBuildingInfo(self.iBuilding)

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), BuildingInfo.getButton(), self.X_ICON + self.W_ICON / 2 - self.ICON_SIZE / 2, self.Y_ICON + self.H_ICON / 2 - self.ICON_SIZE / 2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addListBoxGFC(panel, "", self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panel, False)
		screen.appendListBoxString(panel, u"<font=4b>" + BuildingInfo.getDescription() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		# Category
		iBuildingClass = gc.getBuildingInfo(self.iBuilding).getBuildingClassType()

		if isWorldWonderClass(iBuildingClass):
			szClass = "Wonder"
		elif isNationalWonderClass(iBuildingClass):
			szClass = "National Wonder"
		else:
			szClass = "Building"

		szCategory = utils.getAdvisorString(self.iBuilding) + " " + szClass
		screen.appendListBoxString(panel, u"<font=3>" + szCategory + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		# Yield
		szStats = u""
		for iYieldType in xrange(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = BuildingInfo.getYieldChange(iYieldType)
			if iYieldChange != 0:
				if iYieldChange > 0:
					szSign = "+"
				else:
					szSign = ""
				szStats += u"%s%d%c  " % (szSign, iYieldChange, gc.getYieldInfo(iYieldType).getChar())

		# Commerce
		for iCommerceType in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
			iCommerceChange = BuildingInfo.getCommerceChange(iCommerceType) + BuildingInfo.getObsoleteSafeCommerceChange(iCommerceType)
			if iCommerceChange != 0:
				if iCommerceChange > 0:
					szSign = "+"
				else:
					szSign = ""
				szStats += u"%s%d%c  " % (szSign, iCommerceChange, gc.getCommerceInfo(iCommerceType).getChar())

		# Happiness
		iHappiness = BuildingInfo.getHappiness()
		if self.top.iActivePlayer != -1:
			pPlayer = gc.getPlayer(self.top.iActivePlayer)
			if self.iBuilding == gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationBuildings(BuildingInfo.getBuildingClassType()):
				iHappiness += pPlayer.getExtraBuildingHappiness(self.iBuilding)

		if iHappiness > 0:
			szStats += u"+%d%c  " % (iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
		elif iHappiness < 0:
			szStats += u"+%d%c  " % (abs(iHappiness), CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))

		# Health
		iHealth = BuildingInfo.getHealth()
		if self.top.iActivePlayer != -1:
			pPlayer = gc.getPlayer(self.top.iActivePlayer)
			if self.iBuilding == gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationBuildings(BuildingInfo.getBuildingClassType()):
				iHealth += pPlayer.getExtraBuildingHealth(self.iBuilding)

		if iHealth > 0:
			szStats += u"+%d%c  " % (iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR))
		elif iHealth < 0:
			szStats += u"+%d%c  " % (abs(iHealth), CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR))

		screen.appendListBoxString(panel, u"<font=3>" + szStats + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		# Cost
		if BuildingInfo.getProductionCost() >= 0:
			if self.top.iActivePlayer == -1:
				iCost = (BuildingInfo.getProductionCost() * gc.getDefineINT('BUILDING_PRODUCTION_PERCENT')) / 100
			else:
				iCost = gc.getActivePlayer().getBuildingProductionNeeded(self.iBuilding)

			szCost = u"Cost: %d%c" % (iCost, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
			screen.appendListBoxString(panel, u"<font=3>" + szCost + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)



	def placeRequires(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		screen.addPanel( panel, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.attachLabel(panel, "", "  ")

		for iPrereq in range(gc.getNumTechInfos()):
			if isTechRequiredForBuilding(iPrereq, self.iBuilding):
				screen.attachImageButton(panel, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, 1, False)

		iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqAndBonus()
		if iPrereq >= 0:
			screen.attachImageButton(panel, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False)

		for k in range(gc.getNUM_BUILDING_PREREQ_OR_BONUSES()):
			iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqOrBonuses(k)
			if (iPrereq >= 0):
				screen.attachImageButton( panel, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )

		# Leoreth: civic prereqs
		iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqCivic()
		if iPrereq >= 0:
			screen.attachImageButton(panel, "", gc.getCivicInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iPrereq, -1, False)
					
		# Leoreth: religious prereqs
		iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqReligion()
		iOrPrereq = gc.getBuildingInfo(self.iBuilding).getOrPrereqReligion()
		iStatePrereq = gc.getBuildingInfo(self.iBuilding).getStateReligion()
		iOrStatePrereq = gc.getBuildingInfo(self.iBuilding).getOrStateReligion()
		
		if iOrPrereq >= 0 and iStatePrereq >= 0:
			screen.attachLabel(panel, "", "(")
		
		if iPrereq >= 0:
			screen.attachImageButton( panel, "", gc.getReligionInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iPrereq, self.isStateReligionRequirement([iPrereq, iOrPrereq], [iStatePrereq, iOrStatePrereq]), False )

		if iOrPrereq >= 0:
			screen.attachLabel(panel, "", CyTranslator().getText("TXT_KEY_OR", ()))
			screen.attachImageButton(panel, "", gc.getReligionInfo(iOrPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iOrPrereq, self.isStateReligionRequirement([iPrereq, iOrPrereq], [iStatePrereq, iOrStatePrereq]), False )
			
		if iOrPrereq >= 0 and iStatePrereq >= 0:
			screen.attachLabel(panel, "", ")")
			
		if set([iPrereq, iOrPrereq]) != set([iStatePrereq, iOrStatePrereq]):	
			if iPrereq >= 0 and iStatePrereq >= 0:
				screen.attachLabel(panel, "", CyTranslator().getText("TXT_KEY_AND", ()))
				
			if iPrereq >= 0 and iOrStatePrereq >= 0:
				screen.attachLabel(panel, "", "(")
				
			if iStatePrereq >= 0:
				screen.attachImageButton(panel, "", gc.getReligionInfo(iStatePrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iStatePrereq, 1, False )
				
			if iOrStatePrereq >= 0:
				screen.attachLabel(panel, "", CyTranslator().getText("TXT_KEY_OR", ()))
				screen.attachImageButton(panel, "", gc.getReligionInfo(iOrStatePrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iOrStatePrereq, 1, False)

			if iPrereq >= 0 and iOrStatePrereq >= 0:
				screen.attachLabel(panel, "", ")")
				
		# Leoreth: pagan religion prereqs
		if gc.getBuildingInfo(self.iBuilding).isPagan():
			if self.top.iActivePlayer != -1:
				button = gc.getCivilizationInfo(gc.getPlayer(self.top.iActivePlayer).getCivilizationType()).getPaganReligionButton()
				if button:
					screen.attachImageButton(panel, "", button, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_MINOR_RELIGION, gc.getPlayer(self.top.iActivePlayer).getCivilizationType(), 1, False)

	
	def isStateReligionRequirement(self, lReligions, lStateReligions):
		if set(lReligions) == set(lStateReligions): return 1
		
		return -1

	def placeEffects(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()

		BuildingInfo = gc.getBuildingInfo(self.iBuilding)
		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", True, False, self.X_EFFECTS, self.Y_EFFECTS, self.W_EFFECTS, self.H_EFFECTS, PanelStyles.PANEL_STYLE_BLUE50)
		szText = CyGameTextMgr().getBuildingHelp(self.iBuilding, True, False, False, CyCity()).lstrip()
		screen.addMultilineText(text, szText, self.X_EFFECTS + 10, self.Y_EFFECTS + 30, self.W_EFFECTS - 10, self.H_EFFECTS - 35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeHistory(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()

		screen.addPanel( panel, CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50 )

		szHistory = u""
		if len(gc.getBuildingInfo(self.iBuilding).getStrategy()) > 0:
			szHistory += gc.getBuildingInfo(self.iBuilding).getStrategy()
			szHistory += u"\n\n"
		szHistory += gc.getBuildingInfo(self.iBuilding).getCivilopedia()
		screen.addMultilineText(text, szHistory, self.X_HISTORY + 10, self.Y_HISTORY + 30, self.W_HISTORY - 20, self.H_HISTORY - 40, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput (self, inputClass):
		return 0
