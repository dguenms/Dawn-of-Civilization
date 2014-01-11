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
import ScreenInput
import SevoScreenEnums

import Consts as con

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class SevoPediaBuilding:

	def __init__(self, main):
		self.iBuilding = -1
		self.top = main

		self.BUTTON_SIZE = 46

		self.X_BUILDING_PANE = self.top.X_PEDIA_PAGE
		self.Y_BUILDING_PANE = self.top.Y_PEDIA_PAGE
		self.W_BUILDING_PANE = 323
		self.H_BUILDING_PANE = 116

		self.W_ICON = 100
		self.H_ICON = 100
		self.X_ICON = self.X_BUILDING_PANE + (self.H_BUILDING_PANE - self.H_ICON) / 2
		self.Y_ICON = self.Y_BUILDING_PANE + (self.H_BUILDING_PANE - self.H_ICON) / 2
		self.ICON_SIZE = 64

		self.X_STATS_PANE = self.X_BUILDING_PANE + 110
		self.Y_STATS_PANE = self.Y_BUILDING_PANE + 17
		self.W_STATS_PANE = 190
		self.H_STATS_PANE = 110 - 20

		self.X_PREREQ_PANE = self.X_BUILDING_PANE
		self.W_PREREQ_PANE = self.W_BUILDING_PANE
		self.Y_PREREQ_PANE = self.Y_BUILDING_PANE + self.H_BUILDING_PANE + 10
		self.H_PREREQ_PANE = 110

		self.X_BUILDING_ANIMATION = self.X_BUILDING_PANE + self.W_BUILDING_PANE + 10
		self.Y_BUILDING_ANIMATION = self.Y_BUILDING_PANE + 7
		self.W_BUILDING_ANIMATION = self.top.R_PEDIA_PAGE - self.X_BUILDING_ANIMATION
		self.H_BUILDING_ANIMATION = self.Y_PREREQ_PANE + self.H_PREREQ_PANE - self.Y_BUILDING_ANIMATION
		self.X_ROTATION_BUILDING_ANIMATION = -20
		self.Z_ROTATION_BUILDING_ANIMATION = 30
		self.SCALE_ANIMATION = 0.7

		self.X_SPECIAL_PANE = self.X_BUILDING_PANE
		self.Y_SPECIAL_PANE = self.Y_PREREQ_PANE + self.H_PREREQ_PANE + 10
		self.W_SPECIAL_PANE = self.top.R_PEDIA_PAGE - self.X_SPECIAL_PANE
		self.H_SPECIAL_PANE = 190

		self.X_HISTORY_PANE = self.X_SPECIAL_PANE
		self.W_HISTORY_PANE = self.W_SPECIAL_PANE
		self.Y_HISTORY_PANE = self.Y_SPECIAL_PANE + self.H_SPECIAL_PANE + 10
		self.H_HISTORY_PANE = self.top.B_PEDIA_PAGE - self.Y_HISTORY_PANE



	def interfaceScreen(self, iBuilding):
		self.iBuilding = iBuilding
		screen = self.top.getScreen()

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_BUILDING_PANE, self.Y_BUILDING_PANE, self.W_BUILDING_PANE, self.H_BUILDING_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getBuildingInfo(self.iBuilding).getButton(), self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addBuildingGraphicGFC(self.top.getNextWidgetName(), self.iBuilding, self.X_BUILDING_ANIMATION, self.Y_BUILDING_ANIMATION, self.W_BUILDING_ANIMATION, self.H_BUILDING_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_BUILDING_ANIMATION, self.Z_ROTATION_BUILDING_ANIMATION, self.SCALE_ANIMATION, True)

		self.placeStats()
		self.placeRequires()
		self.placeSpecial()
		self.placeHistory()



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
				screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szBuildingType.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if (isNationalWonderClass(gc.getBuildingInfo(self.iBuilding).getBuildingClassType())):
			iMaxInstances = gc.getBuildingClassInfo(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()).getMaxPlayerInstances()
			szBuildingType = localText.getText("TXT_KEY_PEDIA_NATIONAL_WONDER", ())
			if (iMaxInstances > 1):
				szBuildingType += " " + localText.getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
				screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szBuildingType.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if (buildingInfo.getProductionCost() > 0):
			if self.top.iActivePlayer == -1:
				szCost = localText.getText("TXT_KEY_PEDIA_COST", ((buildingInfo.getProductionCost() * gc.getDefineINT("BUILDING_PRODUCTION_PERCENT"))/100,))
			else:
				szCost = localText.getText("TXT_KEY_PEDIA_COST", (gc.getPlayer(self.top.iActivePlayer).getBuildingProductionNeeded(self.iBuilding),))
			screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szCost.upper() + u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

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



	def placeRequires(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_PREREQ_PANE, self.Y_PREREQ_PANE, self.W_PREREQ_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.attachLabel(panelName, "", "  ")

		for iPrereq in range(gc.getNumTechInfos()):
			if isTechRequiredForBuilding(iPrereq, self.iBuilding):
				screen.attachImageButton( panelName, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, 1, False )

		iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqAndBonus()
		if (iPrereq >= 0):
			screen.attachImageButton( panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )

		for k in range(gc.getNUM_BUILDING_PREREQ_OR_BONUSES()):
			iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqOrBonuses(k)
			if (iPrereq >= 0):
				screen.attachImageButton( panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )

		iCorporation = gc.getBuildingInfo(self.iBuilding).getFoundsCorporation()
		bFirst = True
		if (iCorporation >= 0):
			for k in range(gc.getNUM_CORPORATION_PREREQ_BONUSES()):
				iPrereq = gc.getCorporationInfo(iCorporation).getPrereqBonus(k)
				if (iPrereq >= 0):
					if not bFirst:
						screen.attachLabel(panelName, "", localText.getText("TXT_KEY_OR", ()))
					else:
						bFirst = False
					screen.attachImageButton( panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )

		iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqReligion()
		iOrPrereq = gc.getBuildingInfo(self.iBuilding).getOrPrereqReligion()
		iStatePrereq = gc.getBuildingInfo(self.iBuilding).getStateReligion()
		iOrStatePrereq = gc.getBuildingInfo(self.iBuilding).getOrStateReligion()
		
		if iOrPrereq >= 0 and iStatePrereq >= 0:
			screen.attachLabel(panelName, "", "(")
		
		if (iPrereq >= 0):
			screen.attachImageButton( panelName, "", gc.getReligionInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iPrereq, -1, False )

		if iOrPrereq >= 0:
			screen.attachLabel(panelName, "", localText.getText("TXT_KEY_OR", ()))
			screen.attachImageButton(panelName, "", gc.getReligionInfo(iOrPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iOrPrereq, -1, False )
			
		if iOrPrereq >= 0 and iStatePrereq >= 0:
			screen.attachLabel(panelName, "", ")")
			
		if set([iPrereq, iOrPrereq]) != set([iStatePrereq, iOrStatePrereq]):	
			if iPrereq >= 0 and iStatePrereq >= 0:
				screen.attachLabel(panelName, "", localText.getText("TXT_KEY_AND", ()))
				
			if iPrereq >= 0 and iOrStatePrereq >= 0:
				screen.attachLabel(panelName, "", "(")
				
			if iStatePrereq >= 0:
				screen.attachImageButton(panelName, "", gc.getReligionInfo(iStatePrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iStatePrereq, 1, False )
				
			if iOrStatePrereq >= 0:
				screen.attachLabel(panelName, "", localText.getText("TXT_KEY_OR", ()))
				screen.attachImageButton(panelName, "", gc.getReligionInfo(iOrStatePrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iOrStatePrereq, 1, False)

			if iPrereq >= 0 and iOrStatePrereq >= 0:
				screen.attachLabel(panelName, "", ")")

	def placeSpecial(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", True, False, self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		listName = self.top.getNextWidgetName()
		szSpecialText = CyGameTextMgr().getBuildingHelp(self.iBuilding, True, False, False, None)[1:]
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANE+5, self.Y_SPECIAL_PANE+30, self.W_SPECIAL_PANE-10, self.H_SPECIAL_PANE-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeHistory(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_HISTORY_PANE, self.Y_HISTORY_PANE, self.W_HISTORY_PANE, self.H_HISTORY_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		textName = self.top.getNextWidgetName()
		szText = u""
		if len(gc.getBuildingInfo(self.iBuilding).getStrategy()) > 0:
			szText += localText.getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
			szText += gc.getBuildingInfo(self.iBuilding).getStrategy()
			szText += u"\n\n"
		szText += localText.getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
		szText += gc.getBuildingInfo(self.iBuilding).getCivilopedia()
		screen.addMultilineText( textName, szText, self.X_HISTORY_PANE + 15, self.Y_HISTORY_PANE + 40, self.W_HISTORY_PANE - (15 * 2), self.H_HISTORY_PANE - (15 * 2) - 25, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def getBuildingType(self, iBuilding):
		if (isWorldWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			return 2
		elif (isNationalWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			return 1
		else:
			return 0



	def getBuildingSortedList(self, iBuildingType):
		list1 = []
		numInfos = 0
		for iBuilding in range(gc.getNumBuildingInfos()):
			if gc.getBuildingInfo(iBuilding).isGraphicalOnly() or iBuilding >= con.iNumBuildings: continue
			if iBuilding in [con.iHarappanBath, con.iBabylonGarden, con.iZuluIkhanda, con.iChinesePavillion, con.iIncanTerrace, con.iNativeAmericaTotem]: continue
			if (self.getBuildingType(iBuilding) == iBuildingType):
				list1.append(iBuilding)
				numInfos += 1
		list2 = [(0,0)] * numInfos
		i = 0
		for iBuilding in list1:
			list2[i] = (gc.getBuildingInfo(iBuilding).getDescription(), iBuilding)
			i += 1
		if self.top.isSortLists():
			list2.sort()
		return list2



	def handleInput (self, inputClass):
		return 0
