from CvPythonExtensions import *
import CvUtil
import ScreenInput

gc = CyGlobalContext()



class CvPediaPromotion:
	def __init__(self, main):
		self.iPromotion = -1
		self.top = main

		self.X_INFO_PANE = self.top.X_PEDIA_PAGE
		self.Y_INFO_PANE = self.top.Y_PEDIA_PAGE
		self.W_INFO_PANE = 290
		self.H_INFO_PANE = 120

		self.W_ICON = 100
		self.H_ICON = 100
		self.X_ICON = self.X_INFO_PANE + 10
		self.Y_ICON = self.Y_INFO_PANE + 10
		self.ICON_SIZE = 64

		self.X_INFO_TEXT = self.X_INFO_PANE + 110
		self.Y_INFO_TEXT = self.Y_ICON + 15
		self.W_INFO_TEXT = 220
		self.H_INFO_TEXT = self.H_INFO_PANE - 20

		self.X_REQUIRES = self.X_INFO_PANE + self.W_INFO_PANE + 10
		self.W_REQUIRES = self.top.R_PEDIA_PAGE - self.X_REQUIRES
		self.H_REQUIRES = 110
		self.Y_REQUIRES = self.Y_INFO_PANE + self.H_INFO_PANE - self.H_REQUIRES

		self.X_LEADS_TO = self.X_INFO_PANE
		self.Y_LEADS_TO = self.Y_INFO_PANE + self.H_INFO_PANE + 10
		self.W_LEADS_TO = self.top.R_PEDIA_PAGE - self.X_LEADS_TO
		self.H_LEADS_TO = 110

		self.X_EFFECTS = self.X_LEADS_TO
		self.Y_EFFECTS = self.Y_LEADS_TO + self.H_LEADS_TO + 10
		self.W_EFFECTS = self.top.W_PEDIA_PAGE / 2 - 5
		self.H_EFFECTS = self.top.B_PEDIA_PAGE - self.Y_EFFECTS

		self.X_UNIT_TYPES = self.X_EFFECTS + self.W_EFFECTS + 10
		self.Y_UNIT_TYPES = self.Y_EFFECTS
		self.W_UNIT_TYPES = self.W_EFFECTS
		self.H_UNIT_TYPES = self.H_EFFECTS



	def interfaceScreen(self, iPromotion):
		self.iPromotion = iPromotion
		screen = self.top.getScreen()

		self.placeInfo()
		self.placePrereqs()
		self.placeLeadsTo()
		self.placeEffects()
		self.placeUnitTypes()



	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		PromotionInfo = gc.getPromotionInfo(self.iPromotion)

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), PromotionInfo.getButton(), self.X_ICON + self.W_ICON / 2 - self.ICON_SIZE / 2, self.Y_ICON + self.H_ICON / 2 - self.ICON_SIZE / 2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addListBoxGFC(panel, "", self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panel, False)
		screen.appendListBoxString(panel, u"<font=4b>" + PromotionInfo.getDescription() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		screen.appendListBoxString(panel, u"<font=3>Promotion</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)



	def placePrereqs(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")

		PromotionInfo = gc.getPromotionInfo(self.iPromotion)
		iPrereq = PromotionInfo.getPrereqPromotion()
		if iPrereq > -1:
			screen.attachImageButton(panel, "", gc.getPromotionInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iPrereq, 1, False)

		iPrereqOr1 = PromotionInfo.getPrereqOrPromotion1()
		iPrereqOr2 = PromotionInfo.getPrereqOrPromotion2()
		if iPrereqOr1 > -1:
			if iPrereq > -1:
				screen.attachLabel(panel, "", CyTranslator().getText("TXT_KEY_AND", ()))
				if iPrereqOr2 > -1:
					screen.attachLabel(panel, "", "(")

			screen.attachImageButton(panel, "", gc.getPromotionInfo(iPrereqOr1).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iPrereqOr1, 1, False)

			if iPrereqOr2 > -1:
				screen.attachLabel(panel, "", CyTranslator().getText("TXT_KEY_OR", ()))
				screen.attachImageButton(panel, "", gc.getPromotionInfo(iPrereqOr2).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iPrereqOr2, 1, False)
				if iPrereq > -1:
					screen.attachLabel(panel, "", ")")

		iTech = gc.getPromotionInfo(self.iPromotion).getTechPrereq()
		if iTech > -1:
			screen.attachImageButton(panel, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)

		iReligion = gc.getPromotionInfo(self.iPromotion).getStateReligionPrereq()
		if iReligion > -1:
			screen.attachImageButton(panel, "", gc.getReligionInfo(iReligion).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iReligion, 1, False)



	def placeLeadsTo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_LEADS_TO", ()), "", False, True, self.X_LEADS_TO, self.Y_LEADS_TO, self.W_LEADS_TO, self.H_LEADS_TO, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")

		for iPromotion in xrange(gc.getNumPromotionInfos()):
			PromotionInfo = gc.getPromotionInfo(iPromotion)
			iPrereq = PromotionInfo.getPrereqPromotion()
			if (PromotionInfo.getPrereqPromotion() == self.iPromotion or PromotionInfo.getPrereqOrPromotion1() == self.iPromotion or PromotionInfo.getPrereqOrPromotion2() == self.iPromotion):
				screen.attachImageButton(panel, "", PromotionInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iPromotion, 1, False)



	def placeEffects(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		list = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", True, False, self.X_EFFECTS, self.Y_EFFECTS, self.W_EFFECTS, self.H_EFFECTS, PanelStyles.PANEL_STYLE_BLUE50)

		szText = CyGameTextMgr().getPromotionHelp(self.iPromotion, True)[1:]
		screen.addMultilineText(list, szText, self.X_EFFECTS + 5, self.Y_EFFECTS + 30, self.W_EFFECTS - 10, self.H_EFFECTS - 35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeUnitTypes(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		table = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_PROMOTION_UNITS", ()), "", True, True, self.X_UNIT_TYPES, self.Y_UNIT_TYPES, self.W_UNIT_TYPES, self.H_UNIT_TYPES, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addTableControlGFC(table, 1, self.X_UNIT_TYPES + 10, self.Y_UNIT_TYPES + 40, self.W_UNIT_TYPES - 20, self.H_UNIT_TYPES - 50, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)

		for iUnitCombat in xrange(gc.getNumUnitCombatInfos()):
			if gc.getPromotionInfo(self.iPromotion).getUnitCombat(iUnitCombat):
				iRow = screen.appendTableRow(table)
				screen.setTableText(table, 0, iRow, "<font=3>" + gc.getUnitCombatInfo(iUnitCombat).getDescription() + "</font>", gc.getUnitCombatInfo(iUnitCombat).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iUnitCombat, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput(self, inputClass):
		return 0
