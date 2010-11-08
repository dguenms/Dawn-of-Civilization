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

class CvPediaPromotion:
	"Civilopedia Screen for Promotions"

	def __init__(self, main):
		self.iPromotion = -1
		self.top = main
	
		self.BUTTON_SIZE = 46
		
		self.X_UNIT_PANE = self.top.X_PEDIA_PAGE + 20
		self.Y_UNIT_PANE = 55
		self.W_UNIT_PANE = 250
		self.H_UNIT_PANE = 116

		self.X_ICON = self.X_UNIT_PANE + 8
		self.Y_ICON = self.Y_UNIT_PANE + 8
		self.W_ICON = 100
		self.H_ICON = 100
		self.ICON_SIZE = 64

		self.X_PREREQ_PANE = self.X_UNIT_PANE + self.W_UNIT_PANE + 10
		self.Y_PREREQ_PANE = 55
		self.W_PREREQ_PANE = 1024 - (self.X_PREREQ_PANE) - 24
		self.H_PREREQ_PANE = 116

		self.X_LEADS_TO_PANE = self.X_UNIT_PANE + 10
		self.Y_LEADS_TO_PANE = 180
		self.W_LEADS_TO_PANE = 1000 - self.X_LEADS_TO_PANE
		self.H_LEADS_TO_PANE = 110
				
		self.X_SPECIAL_PANE = self.X_UNIT_PANE + 10
		self.Y_SPECIAL_PANE = 294
		self.W_SPECIAL_PANE = 250
		self.H_SPECIAL_PANE = 380

		self.X_UNIT_GROUP_PANE = self.X_SPECIAL_PANE + self.W_SPECIAL_PANE + 10
		self.Y_UNIT_GROUP_PANE = 294
		self.W_UNIT_GROUP_PANE = 250
		self.H_UNIT_GROUP_PANE = 380
		self.DY_UNIT_GROUP_PANE = 25
#		self.ITEMS_MARGIN = 18
#		self.ITEMS_SEPARATION = 2

	# Screen construction function
	def interfaceScreen(self, iPromotion):	
			
		self.iPromotion = iPromotion
	
		self.top.deleteAllWidgets()						
							
		screen = self.top.getScreen()
		
		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()

		# Header...
		szHeader = u"<font=4b>" + gc.getPromotionInfo(self.iPromotion).getDescription().upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROMOTION, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_PROMOTION or bNotActive:		
			if self.top.iLastScreen != CvScreenEnums.PEDIA_MAIN:
				self.placeLinks()	
			self.top.iLastScreen = CvScreenEnums.PEDIA_PROMOTION
			
		# Icon
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False,
		    self.X_UNIT_PANE, self.Y_UNIT_PANE, self.W_UNIT_PANE, self.H_UNIT_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false,
		    self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getPromotionInfo(self.iPromotion).getButton(),
		    self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getPromotionInfo(self.iPromotion).getButton(), self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, WidgetTypes.WIDGET_GENERAL, self.iPromotion, -1 )

		# Place Required promotions
		self.placePrereqs()

		# Place Allowing promotions
		self.placeLeadsTo()
				
		# Place the Special abilities block
		self.placeSpecial()
		
		self.placeUnitGroups()
			

	# Place Leads To...
	def placeLeadsTo(self):

		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_LEADS_TO", ()), "", false, true,
				 self.X_LEADS_TO_PANE, self.Y_LEADS_TO_PANE, self.W_LEADS_TO_PANE, self.H_LEADS_TO_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		screen.attachLabel(panelName, "", "  ")
		
		for j in range(gc.getNumPromotionInfos()):
			iPrereq = gc.getPromotionInfo(j).getPrereqOrPromotion1()
			if (iPrereq == self.iPromotion):
				screen.attachImageButton( panelName, "", gc.getPromotionInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, j, 1, False )
			iPrereq = gc.getPromotionInfo(j).getPrereqOrPromotion2()
			if (iPrereq == self.iPromotion):
				screen.attachImageButton( panelName, "", gc.getPromotionInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, j, 1, False )
				
	# Place prereqs...
	def placePrereqs(self):

		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true,
				 self.X_PREREQ_PANE, self.Y_PREREQ_PANE, self.W_PREREQ_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		screen.attachLabel(panelName, "", "  ")

		ePromo = gc.getPromotionInfo(self.iPromotion).getPrereqOrPromotion1()
		if (ePromo > -1):
			screen.attachImageButton( panelName, "", gc.getPromotionInfo(ePromo).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, ePromo, 1, False )

			ePromo = gc.getPromotionInfo(self.iPromotion).getPrereqOrPromotion2()
			if (ePromo > -1):
	        		screen.attachTextGFC(panelName, "", localText.getText("TXT_KEY_OR", ()), FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.attachImageButton( panelName, "", gc.getPromotionInfo(ePromo).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, ePromo, 1, False )
								
		eTech = gc.getPromotionInfo(self.iPromotion).getTechPrereq()
		if (eTech > -1):
			screen.attachImageButton( panelName, "", gc.getTechInfo(eTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, eTech, 1, False )		
						
	def placeSpecial(self):


		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", true, false,
				 self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		listName = self.top.getNextWidgetName()
		
		szSpecialText = CyGameTextMgr().getPromotionHelp(self.iPromotion, True)[1:]
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANE+5, self.Y_SPECIAL_PANE+30, self.W_SPECIAL_PANE-10, self.H_SPECIAL_PANE-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	

	def placeUnitGroups(self):
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_PROMOTION_UNITS", ()), "", true, true,
			self.X_UNIT_GROUP_PANE, self.Y_UNIT_GROUP_PANE, self.W_UNIT_GROUP_PANE, self.H_UNIT_GROUP_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		szTable = self.top.getNextWidgetName()
		screen.addTableControlGFC(szTable, 1,
			self.X_UNIT_GROUP_PANE + 10, self.Y_UNIT_GROUP_PANE + 40, self.W_UNIT_GROUP_PANE - 20, self.H_UNIT_GROUP_PANE - 50, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
		
		i = 0
		for iI in range(gc.getNumUnitCombatInfos()):
			if (0 != gc.getPromotionInfo(self.iPromotion).getUnitCombat(iI)):
				iRow = screen.appendTableRow(szTable)
				screen.setTableText(szTable, 0, i, u"<font=4>" + gc.getUnitCombatInfo(iI).getDescription() + u"</font>", gc.getUnitCombatInfo(iI).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iI, -1, CvUtil.FONT_LEFT_JUSTIFY)
				i += 1

	def placeLinks(self):

		self.top.placeLinks()
		self.top.placePromotions()


	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		return 0

