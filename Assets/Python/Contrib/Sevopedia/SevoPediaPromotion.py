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

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class SevoPediaPromotion:

	def __init__(self, main):
		self.iPromotion = -1
		self.top = main
	
		self.BUTTON_SIZE = 46
		
		self.X_UNIT_PANE = self.top.X_PEDIA_PAGE
		self.Y_UNIT_PANE = self.top.Y_PEDIA_PAGE
		self.W_UNIT_PANE = 250
		self.H_UNIT_PANE = 116

		self.W_ICON = 100
		self.H_ICON = 100
		self.X_ICON = self.X_UNIT_PANE + (self.H_UNIT_PANE - self.H_ICON) / 2
		self.Y_ICON = self.Y_UNIT_PANE + (self.H_UNIT_PANE - self.H_ICON) / 2
		self.ICON_SIZE = 64

		self.X_PREREQ_PANE = self.X_UNIT_PANE + self.W_UNIT_PANE + 10
		self.Y_PREREQ_PANE = self.Y_UNIT_PANE
		self.W_PREREQ_PANE = self.top.R_PEDIA_PAGE - self.X_PREREQ_PANE
		self.H_PREREQ_PANE = 116

		self.X_LEADS_TO_PANE = self.X_UNIT_PANE
		self.Y_LEADS_TO_PANE = self.Y_UNIT_PANE + self.H_UNIT_PANE + 10
		self.W_LEADS_TO_PANE = self.top.R_PEDIA_PAGE - self.X_LEADS_TO_PANE
		self.H_LEADS_TO_PANE = 110
				
		self.X_SPECIAL_PANE = self.X_UNIT_PANE
		self.Y_SPECIAL_PANE = self.Y_LEADS_TO_PANE + self.H_LEADS_TO_PANE + 10
		self.W_SPECIAL_PANE = self.top.W_PEDIA_PAGE / 2 - 5
		self.H_SPECIAL_PANE = self.top.B_PEDIA_PAGE - self.Y_SPECIAL_PANE

		self.X_UNIT_GROUP_PANE = self.X_SPECIAL_PANE + self.W_SPECIAL_PANE + 10
		self.Y_UNIT_GROUP_PANE = self.Y_SPECIAL_PANE
		self.W_UNIT_GROUP_PANE = self.W_SPECIAL_PANE
		self.H_UNIT_GROUP_PANE = self.H_SPECIAL_PANE

		self.DY_UNIT_GROUP_PANE = 25



	def interfaceScreen(self, iPromotion):
		self.iPromotion = iPromotion
		screen = self.top.getScreen()

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_UNIT_PANE, self.Y_UNIT_PANE, self.W_UNIT_PANE, self.H_UNIT_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getPromotionInfo(self.iPromotion).getButton(), self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.placePrereqs()
		self.placeLeadsTo()
		self.placeSpecial()
		self.placeUnitGroups()



	def placeLeadsTo(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_LEADS_TO", ()), "", False, True, self.X_LEADS_TO_PANE, self.Y_LEADS_TO_PANE, self.W_LEADS_TO_PANE, self.H_LEADS_TO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")
		for j in range(gc.getNumPromotionInfos()):
			iPrereq = gc.getPromotionInfo(j).getPrereqPromotion()
			if (gc.getPromotionInfo(j).getPrereqPromotion() == self.iPromotion or gc.getPromotionInfo(j).getPrereqOrPromotion1() == self.iPromotion or gc.getPromotionInfo(j).getPrereqOrPromotion2() == self.iPromotion):
				screen.attachImageButton(panelName, "", gc.getPromotionInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, j, 1, False)



	def placePrereqs(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_PREREQ_PANE, self.Y_PREREQ_PANE, self.W_PREREQ_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")
		ePromo = gc.getPromotionInfo(self.iPromotion).getPrereqPromotion()
		if (ePromo > -1):
			screen.attachImageButton(panelName, "", gc.getPromotionInfo(ePromo).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, ePromo, 1, False)
		ePromoOr1 = gc.getPromotionInfo(self.iPromotion).getPrereqOrPromotion1()
		ePromoOr2 = gc.getPromotionInfo(self.iPromotion).getPrereqOrPromotion2()
		if (ePromoOr1 > -1):
			if (ePromo > -1):
				screen.attachLabel(panelName, "", localText.getText("TXT_KEY_AND", ()))
				if (ePromoOr2 > -1):
					screen.attachLabel(panelName, "", "(")
			screen.attachImageButton(panelName, "", gc.getPromotionInfo(ePromoOr1).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, ePromoOr1, 1, False)
			if (ePromoOr2 > -1):
				screen.attachLabel(panelName, "", localText.getText("TXT_KEY_OR", ()))
				screen.attachImageButton(panelName, "", gc.getPromotionInfo(ePromoOr2).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, ePromoOr2, 1, False)
				if (ePromo > -1):
					screen.attachLabel(panelName, "", ")")
		eTech = gc.getPromotionInfo(self.iPromotion).getTechPrereq()
		if (eTech > -1):
			screen.attachImageButton(panelName, "", gc.getTechInfo(eTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, eTech, 1, False)
		eReligion = gc.getPromotionInfo(self.iPromotion).getStateReligionPrereq()
		if (eReligion > -1):
			screen.attachImageButton(panelName, "", gc.getReligionInfo(eReligion).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, eReligion, 1, False)



	def placeSpecial(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", True, False, self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		listName = self.top.getNextWidgetName()
		szSpecialText = CyGameTextMgr().getPromotionHelp(self.iPromotion, True)[1:]
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANE+5, self.Y_SPECIAL_PANE+30, self.W_SPECIAL_PANE-10, self.H_SPECIAL_PANE-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeUnitGroups(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_PROMOTION_UNITS", ()), "", True, True, self.X_UNIT_GROUP_PANE, self.Y_UNIT_GROUP_PANE, self.W_UNIT_GROUP_PANE, self.H_UNIT_GROUP_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		szTable = self.top.getNextWidgetName()
		screen.addTableControlGFC(szTable, 1, self.X_UNIT_GROUP_PANE + 10, self.Y_UNIT_GROUP_PANE + 40, self.W_UNIT_GROUP_PANE - 20, self.H_UNIT_GROUP_PANE - 50, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
		i = 0
		for iI in range(gc.getNumUnitCombatInfos()):
			if (0 != gc.getPromotionInfo(self.iPromotion).getUnitCombat(iI)):
				iRow = screen.appendTableRow(szTable)
				screen.setTableText(szTable, 0, i, u"<font=2>" + gc.getUnitCombatInfo(iI).getDescription() + u"</font>", gc.getUnitCombatInfo(iI).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iI, -1, CvUtil.FONT_LEFT_JUSTIFY)
				i += 1



	def handleInput (self, inputClass):
		return 0
