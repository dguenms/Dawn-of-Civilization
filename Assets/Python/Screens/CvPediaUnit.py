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

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaUnit:
	"Civilopedia Screen for Units"

	def __init__(self, main):
		self.iUnit = -1
		self.top = main
		
		self.X_UNIT_PANE = self.top.X_PEDIA_PAGE + 20
		self.Y_UNIT_PANE = 55
		self.W_UNIT_PANE = 325
		self.H_UNIT_PANE = 145

		self.X_ICON = self.X_UNIT_PANE + 12
		self.Y_ICON = self.Y_UNIT_PANE + 18
		self.W_ICON = 100
		self.H_ICON = 100
		self.ICON_SIZE = 64

		self.X_STATS_PANE = self.X_UNIT_PANE + 130
		self.Y_STATS_PANE = self.Y_UNIT_PANE + 50
		self.W_STATS_PANE = 250
		self.H_STATS_PANE = 200

		self.BUTTON_SIZE = 64
		self.PROMOTION_ICON_SIZE = 32

		self.X_UNIT_ANIMATION = self.X_UNIT_PANE + self.W_UNIT_PANE + 15
		self.Y_UNIT_ANIMATION = 62
		self.W_UNIT_ANIMATION = 1000 - self.X_UNIT_ANIMATION
		self.H_UNIT_ANIMATION = self.H_UNIT_PANE - 8
		self.X_ROTATION_UNIT_ANIMATION = -20
		self.Z_ROTATION_UNIT_ANIMATION = 30
		self.SCALE_ANIMATION = 0.7

		self.X_PREREQ_PANE = self.X_UNIT_PANE
		self.Y_PREREQ_PANE = self.Y_UNIT_PANE + self.H_UNIT_PANE + 5
		self.W_PREREQ_PANE = 280
		self.H_PREREQ_PANE = 110

		self.X_UPGRADES_TO_PANE = self.X_UNIT_PANE + self.W_PREREQ_PANE + 10
		self.Y_UPGRADES_TO_PANE = self.Y_UNIT_PANE + self.H_UNIT_PANE + 5
		self.W_UPGRADES_TO_PANE = 1000 - self.X_UPGRADES_TO_PANE
		self.H_UPGRADES_TO_PANE = 110

		self.X_SPECIAL_PANE = self.X_UNIT_PANE
		self.Y_SPECIAL_PANE = self.Y_UPGRADES_TO_PANE + self.H_UPGRADES_TO_PANE + 5
		self.W_SPECIAL_PANE = 280
		self.H_SPECIAL_PANE = 175

		self.X_PROMO_PANE = self.X_UNIT_PANE + self.W_PREREQ_PANE + 10
		self.Y_PROMO_PANE = self.Y_UPGRADES_TO_PANE + self.H_UPGRADES_TO_PANE + 5
		self.W_PROMO_PANE = 1000 - self.X_PROMO_PANE
		self.H_PROMO_PANE = self.H_SPECIAL_PANE

		self.X_HISTORY_PANE = self.X_UNIT_PANE
		self.Y_HISTORY_PANE = self.Y_SPECIAL_PANE + self.H_SPECIAL_PANE + 5
		self.W_HISTORY_PANE = 1000 - self.X_HISTORY_PANE
		self.H_HISTORY_PANE = 700 - self.Y_HISTORY_PANE

						
	# Screen construction function
	def interfaceScreen(self, iUnit):	
			
		self.iUnit = iUnit
	
		self.top.deleteAllWidgets()						
							
		screen = self.top.getScreen()
		
		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()

		# Header...
		szHeader = u"<font=4b>" + gc.getUnitInfo(self.iUnit).getDescription().upper() + u"</font>"
		screen.setText(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT, iUnit)
		screen.setImageButton(self.top.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_CIVILOPEDIA_ICON").getPath(), self.top.X_EXIT, self.top.Y_TITLE, 32, 32, WidgetTypes.WIDGET_PEDIA_DESCRIPTION,  CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT, iUnit)

		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_UNIT or bNotActive:		
			if self.top.iLastScreen != CvScreenEnums.PEDIA_MAIN:
				self.placeLinks()
			self.top.iLastScreen = CvScreenEnums.PEDIA_UNIT
		
		# Icon
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False,
		    self.X_UNIT_PANE, self.Y_UNIT_PANE, self.W_UNIT_PANE, self.H_UNIT_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false,
		    self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getUnitInfo(self.iUnit).getButton(),
		    self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Unit animation
		screen.addUnitGraphicGFC(self.top.getNextWidgetName(), self.iUnit, self.X_UNIT_ANIMATION, self.Y_UNIT_ANIMATION, self.W_UNIT_ANIMATION, self.H_UNIT_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_UNIT_ANIMATION, self.Z_ROTATION_UNIT_ANIMATION, self.SCALE_ANIMATION, True)

		self.placeStats()

		self.placeUpgradesTo()
		
		self.placeRequires()
				
		self.placeSpecial()

		self.placeHistory()
		
		self.placePromotions()
										
		return

	# Place strength/movement
	def placeStats(self):

		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()

		# Unit combat group
		iCombatType = gc.getUnitInfo(self.iUnit).getUnitCombatType()
		if (iCombatType != -1):
			screen.setImageButton(self.top.getNextWidgetName(), gc.getUnitCombatInfo(iCombatType).getButton(), self.X_STATS_PANE, self.Y_STATS_PANE - 40, 32, 32, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iCombatType, 0)
			screen.setText(self.top.getNextWidgetName(), "", u"<font=3>" + gc.getUnitCombatInfo(iCombatType).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_PANE + 37, self.Y_STATS_PANE - 35, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iCombatType, 0)

		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
		
		if (gc.getUnitInfo(self.iUnit).getAirCombat() > 0 and gc.getUnitInfo(self.iUnit).getCombat() == 0):
			iStrength = gc.getUnitInfo(self.iUnit).getAirCombat()
		else:
			iStrength = gc.getUnitInfo(self.iUnit).getCombat()
			
		szName = self.top.getNextWidgetName()		
		szStrength = localText.getText("TXT_KEY_PEDIA_STRENGTH", ( iStrength, ) )
		screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szStrength.upper() + u"%c" % CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		szName = self.top.getNextWidgetName()
		szMovement = localText.getText("TXT_KEY_PEDIA_MOVEMENT", ( gc.getUnitInfo(self.iUnit).getMoves(), ) )
		screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szMovement.upper() + u"%c" % CyGame().getSymbolID(FontSymbols.MOVES_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if (gc.getUnitInfo(self.iUnit).getProductionCost() >= 0 and not gc.getUnitInfo(self.iUnit).isFound()):
			szName = self.top.getNextWidgetName()
			if self.top.iActivePlayer == -1:
				szCost = localText.getText("TXT_KEY_PEDIA_COST", ((gc.getUnitInfo(self.iUnit).getProductionCost() * gc.getDefineINT("UNIT_PRODUCTION_PERCENT"))/100,))
			else:
				szCost = localText.getText("TXT_KEY_PEDIA_COST", ( gc.getActivePlayer().getUnitProductionNeeded(self.iUnit), ) )
			screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szCost.upper() + u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if (gc.getUnitInfo(self.iUnit).getAirRange() > 0):
			szName = self.top.getNextWidgetName()
			szRange = localText.getText("TXT_KEY_PEDIA_RANGE", ( gc.getUnitInfo(self.iUnit).getAirRange(), ) )
			screen.appendListBoxStringNoUpdate(panelName, u"<font=3>" + szRange.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
			
		screen.updateListBox(panelName)
						
	# Place prereqs (techs, resources)
	def placeRequires(self):

		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true, self.X_PREREQ_PANE, self.Y_PREREQ_PANE, self.W_PREREQ_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		screen.attachLabel(panelName, "", "  ")

		# add tech buttons
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqAndTech()
		if (iPrereq >= 0):
			screen.attachImageButton( panelName, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, 1, False )
				
		for j in range(gc.getDefineINT("NUM_UNIT_AND_TECH_PREREQS")):
			iPrereq = gc.getUnitInfo(self.iUnit).getPrereqAndTechs(j)
			if (iPrereq >= 0):
				screen.attachImageButton( panelName, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, -1, False )

		# add resource buttons
		bFirst = True
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqAndBonus()
		if (iPrereq >= 0):
			bFirst = False
			screen.attachImageButton( panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )

		# count the number of OR resources
		nOr = 0
		for j in range(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
			if (gc.getUnitInfo(self.iUnit).getPrereqOrBonuses(j) > -1):
				nOr += 1

		szLeftDelimeter = ""
		szRightDelimeter = ""
		#  Display a bracket if we have more than one OR resource and an AND resource
		if (not bFirst):
			if (nOr > 1):
				szLeftDelimeter = localText.getText("TXT_KEY_AND", ()) + "( "
				szRightDelimeter = " ) "
			elif (nOr > 0):
				szLeftDelimeter = localText.getText("TXT_KEY_AND", ())

		if len(szLeftDelimeter) > 0:
			screen.attachLabel(panelName, "", szLeftDelimeter)

		bFirst = True
		for j in range(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
			eBonus = gc.getUnitInfo(self.iUnit).getPrereqOrBonuses(j)
			if (eBonus > -1):
				if (not bFirst):
					screen.attachLabel(panelName, "", localText.getText("TXT_KEY_OR", ()))
				else:
					bFirst = False
				screen.attachImageButton( panelName, "", gc.getBonusInfo(eBonus).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, eBonus, -1, False )					

		if len(szRightDelimeter) > 0:
			screen.attachLabel(panelName, "", szRightDelimeter)

		# add religion buttons
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqReligion()
		if (iPrereq >= 0):
			screen.attachImageButton( panelName, "", gc.getReligionInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_RELIGION, iPrereq, -1, False )
		
		# add building buttons
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqBuilding()
		if (iPrereq >= 0):
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iPrereq, -1, False )		
		
	# Place upgrades
	def placeUpgradesTo(self):

		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_UPGRADES_TO", ()), "", false, true, self.X_UPGRADES_TO_PANE, self.Y_UPGRADES_TO_PANE, self.W_UPGRADES_TO_PANE, self.H_UPGRADES_TO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		
		screen.attachLabel(panelName, "", "  ")

		for k in range(gc.getNumUnitClassInfos()):
			if self.top.iActivePlayer == -1:
				eLoopUnit = gc.getUnitClassInfo(k).getDefaultUnitIndex()				
			else:
				eLoopUnit = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(k)
			if (eLoopUnit >= 0 and gc.getUnitInfo(self.iUnit).getUpgradeUnitClass(k)):
				screen.attachImageButton( panelName, "", gc.getUnitInfo(eLoopUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False )

	# Place Special abilities
	def placeSpecial(self):

		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", true, false,
                                 self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		listName = self.top.getNextWidgetName()
		
		szSpecialText = CyGameTextMgr().getUnitHelp( self.iUnit, True, False, False, None )[1:]
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANE+5, self.Y_SPECIAL_PANE+30, self.W_SPECIAL_PANE-10, self.H_SPECIAL_PANE-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
				
	
	def placeLinks(self):

	
		self.top.placeLinks()
		self.top.placeUnits()


					
	def placeHistory(self):
		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True,
						self.X_HISTORY_PANE, self.Y_HISTORY_PANE,
						self.W_HISTORY_PANE, self.H_HISTORY_PANE,
						PanelStyles.PANEL_STYLE_BLUE50 )
		
		textName = self.top.getNextWidgetName()
		screen.addMultilineText( textName, gc.getUnitInfo(self.iUnit).getCivilopedia(), self.X_HISTORY_PANE + 15, self.Y_HISTORY_PANE + 40,
		    self.W_HISTORY_PANE - (15 * 2), self.H_HISTORY_PANE - (15 * 2) - 25, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
	
			
	def placePromotions(self):
		screen = self.top.getScreen()
		
		# add pane and text
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ()), "", true, true, self.X_PROMO_PANE, self.Y_PROMO_PANE, self.W_PROMO_PANE, self.H_PROMO_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
				
		# add promotion buttons
		rowListName = self.top.getNextWidgetName()
		screen.addMultiListControlGFC(rowListName, "", self.X_PROMO_PANE+15, self.Y_PROMO_PANE+40, self.W_PROMO_PANE-20, self.H_PROMO_PANE-40, 1, self.PROMOTION_ICON_SIZE, self.PROMOTION_ICON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
	
		for k in range(gc.getNumPromotionInfos()):
			if (isPromotionValid(k, self.iUnit, false) and not gc.getPromotionInfo(k).isGraphicalOnly()):
				screen.appendMultiListButton( rowListName, gc.getPromotionInfo(k).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, k, -1, false )
								
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		return 0


