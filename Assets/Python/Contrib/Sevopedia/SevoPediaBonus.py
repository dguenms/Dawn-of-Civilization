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
import string

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class SevoPediaBonus:

	def __init__(self, main):
		self.iBonus = -1
		self.top = main

		self.X_BONUS_PANE = self.top.X_PEDIA_PAGE
		self.Y_BONUS_PANE = self.top.Y_PEDIA_PAGE
		self.W_BONUS_PANE = self.top.W_PEDIA_PAGE / 2 - 5
		self.H_BONUS_PANE = 116

		self.W_ICON = 100
		self.H_ICON = 100
		self.X_ICON = self.X_BONUS_PANE + (self.H_BONUS_PANE - self.H_ICON) / 2
		self.Y_ICON = self.Y_BONUS_PANE + (self.H_BONUS_PANE - self.H_ICON) / 2
		self.ICON_SIZE = 64

		self.X_STATS_PANE = self.X_BONUS_PANE + 110
		self.Y_STATS_PANE = self.Y_BONUS_PANE + 33
		self.W_STATS_PANE = 240
		self.H_STATS_PANE = 200

		self.X_BONUS_ANIMATION = self.X_BONUS_PANE + self.W_BONUS_PANE + 10
		self.Y_BONUS_ANIMATION = self.Y_BONUS_PANE + 7
		self.W_BONUS_ANIMATION = self.top.R_PEDIA_PAGE - self.X_BONUS_ANIMATION 
		self.H_BONUS_ANIMATION = self.H_BONUS_PANE
		self.X_ROTATION_BONUS_ANIMATION = -20
		self.Z_ROTATION_BONUS_ANIMATION = 30
		self.SCALE_ANIMATION = 0.7

		self.X_IMPROVEMENTS_PANE = self.X_BONUS_PANE
		self.W_IMPROVEMENTS_PANE = self.W_BONUS_PANE
		self.Y_IMPROVEMENTS_PANE = self.Y_BONUS_PANE + self.H_BONUS_PANE + 10
		self.H_IMPROVEMENTS_PANE = 110

		self.X_EFFECTS_PANE = self.X_BONUS_ANIMATION
		self.W_EFFECTS_PANE = self.W_BONUS_ANIMATION
		self.Y_EFFECTS_PANE = self.Y_IMPROVEMENTS_PANE
		self.H_EFFECTS_PANE = self.H_IMPROVEMENTS_PANE

		self.X_REQUIRES = self.X_BONUS_PANE
		self.W_REQUIRES = self.W_BONUS_PANE
		self.Y_REQUIRES = self.Y_IMPROVEMENTS_PANE + self.H_IMPROVEMENTS_PANE + 10
		self.H_REQUIRES = 110

		self.X_BUILDINGS = self.X_BONUS_ANIMATION
		self.W_BUILDINGS = self.W_BONUS_ANIMATION
		self.Y_BUILDINGS = self.Y_REQUIRES
		self.H_BUILDINGS = self.H_REQUIRES

		self.X_ALLOWS_PANE = self.X_BONUS_PANE
		self.W_ALLOWS_PANE = self.top.R_PEDIA_PAGE - self.X_ALLOWS_PANE
		self.Y_ALLOWS_PANE = self.Y_REQUIRES + self.H_REQUIRES + 10
		self.H_ALLOWS_PANE = 110

		self.X_HISTORY_PANE = self.X_ALLOWS_PANE
		self.W_HISTORY_PANE = self.W_ALLOWS_PANE
		self.Y_HISTORY_PANE = self.Y_ALLOWS_PANE + self.H_ALLOWS_PANE + 10
		self.H_HISTORY_PANE = self.top.B_PEDIA_PAGE - self.Y_HISTORY_PANE



	def interfaceScreen(self, iBonus):
		self.iBonus = iBonus
		screen = self.top.getScreen()

		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.X_BONUS_PANE, self.Y_BONUS_PANE, self.W_BONUS_PANE, self.H_BONUS_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getBonusInfo(self.iBonus).getButton(), self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addBonusGraphicGFC(self.top.getNextWidgetName(), self.iBonus, self.X_BONUS_ANIMATION, self.Y_BONUS_ANIMATION, self.W_BONUS_ANIMATION, self.H_BONUS_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_BONUS_ANIMATION, self.Z_ROTATION_BONUS_ANIMATION, self.SCALE_ANIMATION, True)

		self.placeStats()
		self.placeYield()
		self.placeRequires()
		self.placeBuildings()
		self.placeAllows()
		self.placeSpecial()
		self.placeHistory()



	def placeStats(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
		for k in range(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = gc.getBonusInfo(self.iBonus).getYieldChange(k)
			if (iYieldChange != 0):
				if (iYieldChange > 0):
					sign = "+"
				else:
					sign = ""
				szYield = (u"%s: %s%i " % (gc.getYieldInfo(k).getDescription(), sign, iYieldChange))
				screen.appendListBoxString(panelName, u"<font=3>" + szYield.upper() + (u"%c" % gc.getYieldInfo(k).getChar()) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)



	def placeYield(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ()), "", True, True, self.X_IMPROVEMENTS_PANE, self.Y_IMPROVEMENTS_PANE, self.W_IMPROVEMENTS_PANE, self.H_IMPROVEMENTS_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		bonusInfo = gc.getBonusInfo(self.iBonus)
		for j in range(gc.getNumImprovementInfos()):
			bFirst = True
			szYield = u""
			bEffect = False
			for k in range(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = gc.getImprovementInfo(j).getImprovementBonusYield(self.iBonus, k)
				if (iYieldChange != 0):
					bEffect = True
					iYieldChange += gc.getImprovementInfo(j).getYieldChange(k)
					if (bFirst):
						bFirst = False
					else:
						szYield += ", "
					if (iYieldChange > 0):
						sign = "+"
					else:
						sign = ""
					szYield += (u"%s%i%c" % (sign, iYieldChange, gc.getYieldInfo(k).getChar()))
			if (bEffect):
				childPanelName = self.top.getNextWidgetName()
				screen.attachPanel(panelName, childPanelName, "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachLabel(childPanelName, "", "  ")
				screen.attachImageButton(childPanelName, "", gc.getImprovementInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, j, 1, False )
				screen.attachLabel(childPanelName, "", szYield)



	def placeSpecial(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_EFFECTS", ()), "", True, False,
				 self.X_EFFECTS_PANE, self.Y_EFFECTS_PANE, self.W_EFFECTS_PANE, self.H_EFFECTS_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		listName = self.top.getNextWidgetName()
		screen.attachListBoxGFC( panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY )
		screen.enableSelect(listName, False)
		szSpecialText = CyGameTextMgr().getBonusHelp(self.iBonus, True)
		splitText = string.split( szSpecialText, "\n" )
		for special in splitText:
			if len( special ) != 0:
				screen.appendListBoxString( listName, special, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )



	def placeRequires(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.attachLabel(panelName, "", "  ")
		iTech = gc.getBonusInfo(self.iBonus).getTechReveal()
		if (iTech > -1):
			screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )
			screen.attachLabel(panelName, "", u"(" + localText.getText("TXT_KEY_PEDIA_BONUS_APPEARANCE", ()) + u")")
		iTech = gc.getBonusInfo(self.iBonus).getTechCityTrade()
		if (iTech > -1):
			screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )
			screen.attachLabel(panelName, "", u"(" + localText.getText("TXT_KEY_PEDIA_BONUS_TRADE", ()) + u")")



	def placeHistory(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName,localText.getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_HISTORY_PANE, self.Y_HISTORY_PANE, self.W_HISTORY_PANE, self.H_HISTORY_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")
		textName = self.top.getNextWidgetName()
		screen.addMultilineText( textName, gc.getBonusInfo(self.iBonus).getCivilopedia(), self.X_HISTORY_PANE + 15, self.Y_HISTORY_PANE + 40, self.W_HISTORY_PANE - (30), self.H_HISTORY_PANE - (15 * 2) - 25, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeBuildings(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()), "", False, True, self.X_BUILDINGS, self.Y_BUILDINGS, self.W_BUILDINGS, self.H_BUILDINGS, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.attachLabel(panelName, "", "  ")
		for iBuilding in range(gc.getNumBuildingInfos()):
			info = gc.getBuildingInfo(iBuilding)
			bShow = (info.getFreeBonus() == self.iBonus
					or info.getBonusHealthChanges(self.iBonus) > 0
					or info.getBonusHappinessChanges(self.iBonus) > 0
					or info.getBonusProductionModifier(self.iBonus) > 0)
			if (not bShow):
				for eYield in range(YieldTypes.NUM_YIELD_TYPES):
					if (info.getBonusYieldModifier(self.iBonus, eYield) > 0):
						bShow = True
						break
			if (bShow):
				screen.attachImageButton( panelName, "", gc.getBuildingInfo(iBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, 1, False )



	def placeAllows(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_ALLOWS", ()), "", False, True, self.X_ALLOWS_PANE, self.Y_ALLOWS_PANE, self.W_ALLOWS_PANE, self.H_ALLOWS_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.attachLabel(panelName, "", "  ")
		for eLoopUnit in range(gc.getNumUnitInfos()):
			bFound = False
			if (eLoopUnit >= 0):
				if (gc.getUnitInfo(eLoopUnit).getPrereqAndBonus() == self.iBonus):
					bFound = True	
				else:
					j = 0
					while (not bFound and j < gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
						if (gc.getUnitInfo(eLoopUnit).getPrereqOrBonuses(j) == self.iBonus):
							bFound = True
						j += 1
			if bFound:
				screen.attachImageButton( panelName, "", gc.getUnitInfo(eLoopUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False )

		for eLoopBuilding in range(gc.getNumBuildingInfos()):
			bFound = False
			if (gc.getBuildingInfo(eLoopBuilding).getPrereqAndBonus() == self.iBonus):
				bFound = True
			else:
				j = 0
				while (not bFound and j < gc.getNUM_BUILDING_PREREQ_OR_BONUSES()):
					if (gc.getBuildingInfo(eLoopBuilding).getPrereqOrBonuses(j) == self.iBonus):
						bFound = True
					j += 1
			if bFound:
				screen.attachImageButton( panelName, "", gc.getBuildingInfo(eLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, False )



	def handleInput (self, inputClass):
		return 0
