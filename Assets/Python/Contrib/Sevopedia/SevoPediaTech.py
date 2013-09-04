# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005

#
# Sevopedia 2.3
#   sevotastic.blogspot.com
#   sevotastic@yahoo.com
#
# additional work by Gaurav, Progor, Ket, Vovan, Fitchn, LunarMongoose
# see ReadMe for details
#

from CvPythonExtensions import *
import CvUtil
import CvPediaScreen
import ScreenInput
import SevoScreenEnums

import RFCUtils

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

utils = RFCUtils.RFCUtils()

class SevoPediaTech(CvPediaScreen.CvPediaScreen):

	def __init__(self, main):
		self.iTech = -1
		self.top = main

		self.X_TECH_PANE = self.top.X_PEDIA_PAGE
		self.Y_TECH_PANE = self.top.Y_PEDIA_PAGE
		self.W_TECH_PANE = 300
		self.H_TECH_PANE = 116

		self.W_ICON = 100
		self.H_ICON = 100
		self.X_ICON = self.X_TECH_PANE + (self.H_TECH_PANE - self.H_ICON) / 2
		self.Y_ICON = self.Y_TECH_PANE + (self.H_TECH_PANE - self.H_ICON) / 2

		self.ICON_SIZE = 64
		self.BUTTON_SIZE = 64

		self.X_COST = self.X_TECH_PANE + 110
		self.Y_COST = self.Y_TECH_PANE + 47

		self.X_CIVS = self.X_TECH_PANE + self.W_TECH_PANE + 10
		self.Y_CIVS = self.Y_TECH_PANE
		self.W_CIVS = self.top.R_PEDIA_PAGE - self.X_CIVS
		self.H_CIVS = 110

		self.X_QUOTE_PANE = self.X_TECH_PANE
		self.Y_QUOTE_PANE = self.Y_TECH_PANE + self.H_TECH_PANE + 10
		self.W_QUOTE_PANE = self.top.R_PEDIA_PAGE - self.X_QUOTE_PANE
		self.H_QUOTE_PANE = 110

		self.X_PREREQ_PANE = self.X_TECH_PANE
		self.Y_PREREQ_PANE = self.Y_QUOTE_PANE + self.H_QUOTE_PANE + 10
		self.W_PREREQ_PANE = self.top.W_PEDIA_PAGE / 2 - 5
		self.H_PREREQ_PANE = 124

		self.X_LEADS_TO_PANE = self.X_PREREQ_PANE + self.W_PREREQ_PANE + 10
		self.Y_LEADS_TO_PANE = self.Y_PREREQ_PANE
		self.W_LEADS_TO_PANE = self.W_PREREQ_PANE
		self.H_LEADS_TO_PANE = self.H_PREREQ_PANE

		self.X_SPECIAL_PANE = self.X_TECH_PANE
		self.W_SPECIAL_PANE = self.W_PREREQ_PANE
		self.Y_SPECIAL_PANE = self.Y_PREREQ_PANE + self.H_PREREQ_PANE + 10
		self.H_SPECIAL_PANE = self.top.B_PEDIA_PAGE - self.Y_SPECIAL_PANE

		self.X_UNIT_PANE = self.X_LEADS_TO_PANE
		self.W_UNIT_PANE = self.W_LEADS_TO_PANE
		self.Y_UNIT_PANE = self.Y_SPECIAL_PANE
		self.H_UNIT_PANE = self.H_PREREQ_PANE

		self.X_BUILDING_PANE = self.X_UNIT_PANE
		self.W_BUILDING_PANE = self.W_UNIT_PANE
		self.Y_BUILDING_PANE = self.Y_UNIT_PANE + self.H_UNIT_PANE + 10
		self.H_BUILDING_PANE = self.H_PREREQ_PANE



	def interfaceScreen(self, iTech):
		self.iTech = iTech
		screen = self.top.getScreen()

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_TECH_PANE, self.Y_TECH_PANE, self.W_TECH_PANE, self.H_TECH_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getTechInfo(self.iTech).getButton(), self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if (self.top.iActivePlayer == -1):
			szCostText = localText.getText("TXT_KEY_PEDIA_COST", (gc.getTechInfo(iTech).getResearchCost(),)) + u"%c" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())
		else:
			szCostText = localText.getText("TXT_KEY_PEDIA_COST", (gc.getTeam(gc.getGame().getActiveTeam()).getResearchCost(iTech),)) + u"%c" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())
		screen.setLabel(self.top.getNextWidgetName(), "Background", u"<font=4>" + szCostText.upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_COST + 25, self.Y_COST, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.placeCivilizations()
		self.placePrereqs()
		self.placeLeadsTo()
		self.placeUnits()
		self.placeBuildings()
		self.placeSpecial()
		self.placeQuote()



	def placeCivilizations(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_CATEGORY_CIV", ()), "", False, True, self.X_CIVS, self.Y_CIVS, self.W_CIVS, self.H_CIVS, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.attachLabel(panelName, "", "  ")
		for iCiv in range(gc.getNumCivilizationInfos()):
			civ = gc.getCivilizationInfo(iCiv)
			if civ.isCivilizationFreeTechs(self.iTech):
				screen.attachImageButton(panelName, "", civ.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, 1, False)



	def placeLeadsTo(self):
		screen = self.top.getScreen()
		szLeadsTo = localText.getText("TXT_KEY_PEDIA_LEADS_TO", ())
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, szLeadsTo, "", False, True, self.X_LEADS_TO_PANE, self.Y_LEADS_TO_PANE, self.W_LEADS_TO_PANE, self.H_LEADS_TO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")

		for j in range(gc.getNumTechInfos()):
			for k in range(gc.getNUM_OR_TECH_PREREQS()):
				iPrereq = gc.getTechInfo(j).getPrereqOrTechs(k)
				if (iPrereq == self.iTech):
					screen.attachImageButton(panelName, "", gc.getTechInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_DERIVED_TECH, j, self.iTech, False)
			for k in range(gc.getNUM_AND_TECH_PREREQS()):
				iPrereq = gc.getTechInfo(j).getPrereqAndTechs(k)
				if (iPrereq == self.iTech):
					screen.attachImageButton(panelName, "", gc.getTechInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_DERIVED_TECH, j, self.iTech, False)



	def placePrereqs(self):
		screen = self.top.getScreen()
		szRequires = localText.getText("TXT_KEY_PEDIA_REQUIRES", ())
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, szRequires, "", False, True, self.X_PREREQ_PANE, self.Y_PREREQ_PANE, self.W_PREREQ_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")
		bFirst = True
		for j in range(gc.getNUM_AND_TECH_PREREQS()):
			eTech = gc.getTechInfo(self.iTech).getPrereqAndTechs(j)
			if (eTech > -1):
				if (not bFirst):
					screen.attachLabel(panelName, "", localText.getText("TXT_KEY_AND", ()))
				else:
					bFirst = False
				screen.attachImageButton(panelName, "", gc.getTechInfo(eTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH, eTech, j, False)
		nOrTechs = 0
		for j in range(gc.getNUM_OR_TECH_PREREQS()):
			if (gc.getTechInfo(self.iTech).getPrereqOrTechs(j) > -1):
				nOrTechs += 1
		szLeftDelimeter = ""
		szRightDelimeter = ""
		if (not bFirst):
			if (nOrTechs > 1):
				szLeftDelimeter = localText.getText("TXT_KEY_AND", ()) + "("
				szRightDelimeter = ") "
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
				screen.attachImageButton(panelName, "", gc.getTechInfo(eTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH, eTech, j, False)
		if len(szRightDelimeter) > 0:
			screen.attachLabel(panelName, "", szRightDelimeter)



	def placeUnits(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_UNITS_ENABLED", ()), "", False, True, self.X_UNIT_PANE, self.Y_UNIT_PANE, self.W_UNIT_PANE, self.H_UNIT_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")
		for eLoopUnit in range(gc.getNumUnitInfos()):
			if (eLoopUnit != -1):
				if (isTechRequiredForUnit(self.iTech, eLoopUnit) and (self.isUnitAvailableToPlayer(eLoopUnit))):
					screen.attachImageButton(panelName, "", gc.getUnitInfo(eLoopUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False)



	def placeBuildings(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_BUILDINGS_ENABLED", ()), "", False, True, self.X_BUILDING_PANE, self.Y_BUILDING_PANE, self.W_BUILDING_PANE, self.H_BUILDING_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")
		for eLoopBuilding in range(gc.getNumBuildingInfos()):
			if (eLoopBuilding != -1):
				if (isTechRequiredForBuilding(self.iTech, eLoopBuilding) and self.isBuildingAvailableToPlayer(eLoopBuilding)):
						screen.attachImageButton(panelName, "", gc.getBuildingInfo(eLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, False)
						
		for eLoopProject in range(gc.getNumProjectInfos()):
			if (isTechRequiredForProject(self.iTech, eLoopProject)):
				screen.attachImageButton(panelName, "", gc.getProjectInfo(eLoopProject).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, eLoopProject, 1, False)



	def placeSpecial(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", True, False, self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		listName = self.top.getNextWidgetName()
		szSpecialText = CyGameTextMgr().getTechHelp(self.iTech, True, False, False, False, -1)[1:]
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANE+5, self.Y_SPECIAL_PANE+30, self.W_SPECIAL_PANE-35, self.H_SPECIAL_PANE-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeQuote(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, "", "", True, True,
			self.X_QUOTE_PANE, self.Y_QUOTE_PANE, self.W_QUOTE_PANE, self.H_QUOTE_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		szQuote = gc.getTechInfo(self.iTech).getQuote()
		szQuote += u"\n\n" + gc.getTechInfo(self.iTech).getCivilopedia()
		szQuoteTextWidget = self.top.getNextWidgetName()
		screen.addMultilineText(szQuoteTextWidget, szQuote, self.X_QUOTE_PANE + 15, self.Y_QUOTE_PANE + 15,
		    self.W_QUOTE_PANE - (15 * 2), self.H_QUOTE_PANE - (15 * 2), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput (self, inputClass):
		return 0

	def isUnitAvailableToPlayer(self, iUnitType):
		iPlayer = utils.getHumanID()
		
		if iPlayer == -1: return True
		
		return (utils.getUniqueUnitType(iPlayer, gc.getUnitInfo(iUnitType).getUnitClassType()) == iUnitType)
		
	def isBuildingAvailableToPlayer(self, iBuildingType):
		iPlayer = utils.getHumanID()
		
		if iPlayer == -1: return True
		
		return (utils.getUniqueBuilding(iPlayer, iBuildingType) == iBuildingType)