from CvPythonExtensions import *
from RFCUtils import utils
import CvUtil
from Consts import *

gc = CyGlobalContext()



class CvPediaUnit:
	def __init__(self, main):
		self.iUnit = -1
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
		self.PROMOTION_ICON_SIZE = 32

		self.X_INFO_TEXT = self.X_INFO_PANE + 110
		self.Y_INFO_TEXT = self.Y_ICON + 10
		self.W_INFO_TEXT = 220
		self.H_INFO_TEXT = self.H_INFO_PANE - 20

		self.X_REQUIRES = self.X_INFO_PANE
		self.Y_REQUIRES = self.Y_INFO_PANE + self.H_INFO_PANE + 10
		self.W_REQUIRES = self.W_INFO_PANE
		self.H_REQUIRES = 110

		self.X_UNIT_ANIMATION = self.X_INFO_PANE + self.W_INFO_PANE + 10
		self.W_UNIT_ANIMATION = self.top.R_PEDIA_PAGE - self.X_UNIT_ANIMATION
		self.Y_UNIT_ANIMATION = self.Y_INFO_PANE + 7
		self.H_UNIT_ANIMATION = self.H_INFO_PANE + self.H_REQUIRES + 3
		self.X_ROTATION_UNIT_ANIMATION = -20
		self.Z_ROTATION_UNIT_ANIMATION = 30
		self.SCALE_ANIMATION = 0.8

		self.X_ABILITIES = self.X_INFO_PANE
		self.Y_ABILITIES = self.Y_REQUIRES + self.H_REQUIRES + 10
		self.W_ABILITIES = self.W_INFO_PANE
		self.H_ABILITIES = 210

		self.X_PROMOTIONS = self.X_ABILITIES + self.W_ABILITIES + 10
		self.Y_PROMOTIONS = self.Y_ABILITIES
		self.W_PROMOTIONS = self.W_UNIT_ANIMATION
		self.H_PROMOTIONS = self.H_ABILITIES
		
		self.X_REPLACEMENTS = self.X_ABILITIES + self.W_ABILITIES + 10
		self.Y_REPLACEMENTS = self.Y_ABILITIES
		self.W_REPLACEMENTS = self.W_UNIT_ANIMATION
		self.H_REPLACEMENTS = self.H_REQUIRES + 5
		
		self.X_UPGRADES = self.X_REPLACEMENTS
		self.W_UPGRADES = self.W_REPLACEMENTS
		self.H_UPGRADES = self.H_REPLACEMENTS
		self.Y_UPGRADES = self.Y_REPLACEMENTS + self.H_ABILITIES - self.H_UPGRADES

		self.X_HISTORY = self.X_INFO_PANE
		self.Y_HISTORY = self.Y_ABILITIES + self.H_ABILITIES + 10
		self.W_HISTORY = self.top.R_PEDIA_PAGE - self.X_HISTORY
		self.H_HISTORY = self.top.B_PEDIA_PAGE - self.Y_HISTORY



	def interfaceScreen(self, iUnit):
		self.iUnit = iUnit
		screen = self.top.getScreen()
		if iUnit == iSatellite:
			self.spaceGraphic(iUnit)
		else:
			screen.addUnitGraphicGFC(self.top.getNextWidgetName(), self.iUnit, self.X_UNIT_ANIMATION, self.Y_UNIT_ANIMATION, self.W_UNIT_ANIMATION, self.H_UNIT_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_UNIT_ANIMATION, self.Z_ROTATION_UNIT_ANIMATION, self.SCALE_ANIMATION, True)

		self.placeInfo()
		self.placeRequires()
		self.placeAbilities()
		#self.placePromotions()
		self.placeReplacements()
		self.placeUpgrades()
		self.placeHistory()

	def spaceGraphic(self, iUnit):
		screen = self.top.getScreen()
		szImage = self.top.getNextWidgetName()
		screen.addModelGraphicGFC(szImage, "Art/Interface/Screens/Civilopedia/Space_Environment.nif", self.X_UNIT_ANIMATION, self.Y_UNIT_ANIMATION, self.W_UNIT_ANIMATION, self.H_UNIT_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_UNIT_ANIMATION,  self.Z_ROTATION_UNIT_ANIMATION, self.SCALE_ANIMATION)
		
		if iUnit == iSatellite: # the satellite has a special nif file because it is so high in the air
			screen.addToModelGraphicGFC(szImage, "Art/Units/Satellite/satellite_pedia.nif")
		else:
			screen.addToModelGraphicGFC(szImage, gc.getUnitInfo(iUnit).getArtInfo(0, EraTypes.NO_ERA, UnitArtStyleTypes.NO_UNIT_ARTSTYLE).getNIF())


	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		UnitInfo = gc.getUnitInfo(self.iUnit)

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), UnitInfo.getButton(), self.X_ICON + self.W_ICON / 2 - self.ICON_SIZE / 2, self.Y_ICON + self.H_ICON / 2 - self.ICON_SIZE / 2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addListBoxGFC(panel, "", self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panel, False)
		screen.appendListBoxString(panel, u"<font=4b>" + UnitInfo.getDescription() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		# Category
		if UnitInfo.getUnitCombatType() > -1:
			szCategory = gc.getUnitCombatInfo(UnitInfo.getUnitCombatType()).getDescription().replace("Units", "Unit")
			screen.appendListBoxString(panel, u"<font=3>" + szCategory + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		elif UnitInfo.isAnimal():
			screen.appendListBoxString(panel, u"<font=3>Animal</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		elif UnitInfo.getPrereqReligion() > -1:
			screen.appendListBoxString(panel, u"<font=3>Missionary</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		# Strength
		if gc.getUnitInfo(self.iUnit).getAirCombat() > 0 and gc.getUnitInfo(self.iUnit).getCombat() == 0:
			iStrength = gc.getUnitInfo(self.iUnit).getAirCombat()
		else:
			iStrength = gc.getUnitInfo(self.iUnit).getCombat()

		szStats = u"%d%c" % (iStrength, CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))

		# Movement
		if UnitInfo.getAirCombat() > 0 and UnitInfo.getAirRange() > 0:
			szStats += u"  %d%c" % (UnitInfo.getAirRange(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
		else:
			szStats += u"  %d%c" % (UnitInfo.getMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR))

		# Cost
		if UnitInfo.getProductionCost() >= 0:
			if self.top.iActivePlayer == -1:
				iCost = (UnitInfo.getProductionCost() * gc.getDefineINT('UNIT_PRODUCTION_PERCENT')) / 100
			else:
				iCost = gc.getActivePlayer().getUnitProductionNeeded(self.iUnit)

			szStats += u"  %d%c" % (iCost, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())

		screen.appendListBoxString(panel, u"<font=3>" + szStats + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

	def placeReplacements(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_REPLACEMENTS_UPGRADES", ()), "", False, True, self.X_REPLACEMENTS, self.Y_REPLACEMENTS, self.W_REPLACEMENTS, self.H_REPLACEMENTS, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")
		
		iUnitClass = gc.getUnitInfo(self.iUnit).getUnitClassType()
		iBaseUnit = gc.getUnitClassInfo(iUnitClass).getDefaultUnitIndex()
		
		if self.iUnit != iBaseUnit:
			screen.attachImageButton(panel, "", gc.getUnitInfo(iBaseUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iBaseUnit, 1, False)
			return
		
		for iUnit in xrange(gc.getNumUnitInfos()):
			if self.iUnit != iUnit and not gc.getUnitInfo(iUnit).isGraphicalOnly():
				if iUnitClass == gc.getUnitInfo(iUnit).getUnitClassType():
					screen.attachImageButton(panel, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False)
					
	def placeUpgrades(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		screen.addPanel(panel, " ", "", False, True, self.X_UPGRADES, self.Y_UPGRADES, self.W_UPGRADES, self.H_UPGRADES, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")
		
		for iUnitClass in xrange(gc.getNumUnitClassInfos()):
			if gc.getUnitInfo(self.iUnit).getUpgradeUnitClass(iUnitClass):
				if self.top.iActivePlayer >= 0 and self.iUnit == utils.getUniqueUnit(self.top.iActivePlayer, self.iUnit):
					iUnit = utils.getUniqueUnitType(self.top.iActivePlayer, iUnitClass)
				else:
					iUnit = gc.getUnitClassInfo(iUnitClass).getDefaultUnitIndex()
				screen.attachImageButton(panel, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False)

	def placeRequires(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panel, "", "  ")
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqAndTech()
		if (iPrereq >= 0):
			screen.attachImageButton(panel, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, 1, False)
		for j in xrange(gc.getDefineINT("NUM_UNIT_AND_TECH_PREREQS")):
			iPrereq = gc.getUnitInfo(self.iUnit).getPrereqAndTechs(j)
			if (iPrereq >= 0):
				screen.attachImageButton(panel, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, -1, False)
		bFirst = True
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqAndBonus()
		if (iPrereq >= 0):
			bFirst = False
			screen.attachImageButton(panel, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False)
		nOr = 0
		for j in xrange(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
			if (gc.getUnitInfo(self.iUnit).getPrereqOrBonuses(j) > -1):
				nOr += 1
		szLeftDelimeter = ""
		szRightDelimeter = ""
		if (not bFirst):
			if (nOr > 1):
				szLeftDelimeter = CyTranslator().getText("TXT_KEY_AND", ()) + "("
				szRightDelimeter = ") "
			elif (nOr > 0):
				szLeftDelimeter = CyTranslator().getText("TXT_KEY_AND", ())
		if len(szLeftDelimeter) > 0:
			screen.attachLabel(panel, "", szLeftDelimeter)
		bFirst = True
		for j in xrange(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
			eBonus = gc.getUnitInfo(self.iUnit).getPrereqOrBonuses(j)
			if (eBonus > -1):
				if not bFirst:
					screen.attachLabel(panel, "", CyTranslator().getText("TXT_KEY_OR", ()))
				else:
					bFirst = False
				screen.attachImageButton(panel, "", gc.getBonusInfo(eBonus).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, eBonus, -1, False)
		if len(szRightDelimeter) > 0:
			screen.attachLabel(panel, "", szRightDelimeter)
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqReligion()
		if (iPrereq >= 0):
			screen.attachImageButton(panel, "", gc.getReligionInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_RELIGION, iPrereq, -1, False)
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqBuilding()
		if (iPrereq >= 0):
			screen.attachImageButton(panel, "", gc.getBuildingInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iPrereq, -1, False)

	


	def placeAbilities(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_ABILITIES", ()), "", True, False, self.X_ABILITIES, self.Y_ABILITIES, self.W_ABILITIES, self.H_ABILITIES, PanelStyles.PANEL_STYLE_BLUE50)
		szText = CyGameTextMgr().getUnitHelp(self.iUnit, True, False, False, None)[1:]

		UnitInfo = gc.getUnitInfo(self.iUnit)
		iMaxUnits = UnitInfo.getCollateralDamageMaxUnits()
		if iMaxUnits > 0 and UnitInfo.getCollateralDamage() > 0:
			szCollateral = u"Collateral Damage (%d Units)" % iMaxUnits
			szText = szText.replace("Collateral Damage", szCollateral)

		# Limited Units
		iMax = 0

		# Leoreth: ?
		
		if iMax > 0:
			szText += u"\n%cMaximum %d Active" % (CyGame().getSymbolID(FontSymbols.BULLET_CHAR), iMax)

		screen.addMultilineText(text, szText, self.X_ABILITIES + 5, self.Y_ABILITIES + 30, self.W_ABILITIES - 10, self.H_ABILITIES - 35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placePromotions(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		list = self.top.getNextWidgetName()

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ()), "", True, True, self.X_PROMOTIONS, self.Y_PROMOTIONS, self.W_PROMOTIONS, self.H_PROMOTIONS, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addMultiListControlGFC(list, "", self.X_PROMOTIONS + 10, self.Y_PROMOTIONS + 30, self.W_PROMOTIONS - 10, self.H_PROMOTIONS - 30, 1, self.PROMOTION_ICON_SIZE, self.PROMOTION_ICON_SIZE, TableStyles.TABLE_STYLE_STANDARD)

		for iPromotion in xrange(gc.getNumPromotionInfos()):
			PromotionInfo = gc.getPromotionInfo(iPromotion)
			if isPromotionValid(iPromotion, self.iUnit, False):
				if not PromotionInfo.isGraphicalOnly():
					screen.appendMultiListButton(list, PromotionInfo.getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iPromotion, -1, False)



	def placeHistory(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		text = self.top.getNextWidgetName()
		UnitInfo = gc.getUnitInfo(self.iUnit)

		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50)

		szHistory = u""
		if len(UnitInfo.getStrategy()) > 0:
			szHistory += gc.getUnitInfo(self.iUnit).getStrategy()
			szHistory += u"\n\n"

		szHistory += UnitInfo.getCivilopedia()
		screen.addMultilineText(text, szHistory, self.X_HISTORY + 10, self.Y_HISTORY + 30, self.W_HISTORY - 20, self.H_HISTORY - 40, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def handleInput (self, inputClass):
		return 0
