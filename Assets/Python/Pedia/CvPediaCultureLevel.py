from CvPythonExtensions import *
import CvUtil
import FontUtil
from Consts import *

gc = CyGlobalContext()
localText = CyTranslator()

class CvPediaCultureLevel:

	def __init__(self, main):
		self.iCultureLevel = -1
		self.top = main
		
		self.X_INFO_PANE = self.top.X_PEDIA_PAGE
		self.Y_INFO_PANE = self.top.Y_PEDIA_PAGE
		self.W_INFO_PANE = self.top.R_PEDIA_PAGE - self.X_INFO_PANE
		self.H_INFO_PANE = 80
		
		self.X_INFO_TEXT = self.X_INFO_PANE + 10
		self.Y_INFO_TEXT = self.Y_INFO_PANE + 15
		self.W_INFO_TEXT = 180
		self.H_INFO_TEXT = self.H_INFO_PANE - 20
		
		self.X_EFFECTS = self.X_INFO_PANE
		self.Y_EFFECTS = self.Y_INFO_PANE + self.H_INFO_PANE + 10
		self.W_EFFECTS = self.W_INFO_PANE
		self.H_EFFECTS = 150
		
		self.X_SPECIALISTS = self.X_INFO_PANE
		self.Y_SPECIALISTS = self.Y_EFFECTS + self.H_EFFECTS + 10
		self.W_SPECIALISTS = self.W_INFO_PANE / 2 - 5
		self.H_SPECIALISTS = self.top.B_PEDIA_PAGE - self.Y_SPECIALISTS
		
		self.X_BUILDINGS = self.X_SPECIALISTS + self.W_SPECIALISTS + 10
		self.Y_BUILDINGS = self.Y_SPECIALISTS
		self.W_BUILDINGS = self.W_SPECIALISTS
		self.H_BUILDINGS = self.H_SPECIALISTS
		
	def interfaceScreen(self, iCultureLevel):
		self.iCultureLevel = iCultureLevel
		
		self.placeInfo()
		self.placeEffects()
		self.placeBuildings()
		self.placeSpecialists()
		
	def placeInfo(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		
		CultureLevelInfo = gc.getCultureLevelInfo(self.iCultureLevel)
		
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_INFO_PANE, self.Y_INFO_PANE, self.W_INFO_PANE, self.H_INFO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		
		screen.addListBoxGFC(panel, "", self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panel, False)
		screen.appendListBoxString(panel, u"<font=4b>" + CultureLevelInfo.getDescription() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		
		if self.top.iActivePlayer == -1:
			iCulture = CultureLevelInfo.getSpeedThreshold(2)
		else:
			iCulture = CultureLevelInfo.getSpeedThreshold(gc.getGame().getGameSpeedType())
			
		szCulture = u"%d%c" % (iCulture, gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar())
		screen.appendListBoxString(panel, u"<font=3>" + szCulture + u"<font=3>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeEffects(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", False, True, self.X_EFFECTS, self.Y_EFFECTS, self.W_EFFECTS, self.H_EFFECTS, PanelStyles.PANEL_STYLE_BLUE50)
		text = self.top.getNextWidgetName()
		screen.attachListBoxGFC(panel, text, "", TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(text, False)
		
		CultureLevelInfo = gc.getCultureLevelInfo(self.iCultureLevel)
		
		szText = ""
		
		iDefense = CultureLevelInfo.getCityDefenseModifier()
		if iDefense > 0:
			szText += u"+%d%s %c\n" % (iDefense, "%", CyGame().getSymbolID(FontSymbols.DEFENSE_CHAR),)
			
		iUnrest = self.iCultureLevel
		if iUnrest > 0:
			szText += u"%d turns of unrest %c on conquest\n" % (iUnrest, CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR),)
		
		iWonderLimit = CultureLevelInfo.getWonderLimit()
		if iWonderLimit > 0:
			szText += localText.getText("TXT_KEY_PEDIA_WONDER_LIMIT", (iWonderLimit,))
			szText += u"\n"
		
		iNationalWonderLimit = CultureLevelInfo.getNationalWonderLimit()
		if iNationalWonderLimit > 0:
			szText += localText.getText("TXT_KEY_PEDIA_NATIONAL_WONDER_LIMIT", (iNationalWonderLimit,))
			szText += u"\n"
		
		screen.addMultilineText(text, szText, self.X_EFFECTS + 20, self.Y_EFFECTS + 40, self.W_EFFECTS - 10, self.H_EFFECTS - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeBuildings(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		screen.addPanel(panel, CyTranslator().getText("TXT_KEY_PEDIA_BUILDINGS", ()), "", False, True, self.X_BUILDINGS, self.Y_BUILDINGS, self.W_BUILDINGS, self.H_BUILDINGS, PanelStyles.PANEL_STYLE_BLUE50)
		text = self.top.getNextWidgetName()
		screen.attachListBoxGFC(panel, text, "", TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(text, False)
		
		if self.iCultureLevel == 0: return
		
		szText = ""
		
		for iBuilding in range(gc.getNumBuildingInfos()):
			BuildingInfo = gc.getBuildingInfo(iBuilding)
			szBuildingEffects = ""
			
			for iCommerce in range(CommerceTypes.NUM_COMMERCE_TYPES):
				iCommerceChange = BuildingInfo.getCultureCommerceModifier(iCommerce)
				
				if iCommerceChange > 0:
					if szBuildingEffects:
						szBuildingEffects += u", "
						
					szBuildingEffects += u"+%d%s %c" % (self.iCultureLevel * iCommerceChange, "%", gc.getCommerceInfo(iCommerce).getChar())
					
			iGreatPeopleRateModifier = BuildingInfo.getCultureGreatPeopleRateModifier()
			
			if iGreatPeopleRateModifier > 0:
				if szBuildingEffects:
					szBuildingEffects += u", "
					
				szBuildingEffects += u"+%d%s %c" % (self.iCultureLevel * iGreatPeopleRateModifier, "%", CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR))
				
			iTradeRouteModifier = BuildingInfo.getCultureTradeRouteModifier()
				
			if iTradeRouteModifier > 0:
				if szBuildingEffects:
					szBuildingEffects += u", "
					
				szBuildingEffects += u"+%d%s %c" % (self.iCultureLevel * iTradeRouteModifier, "%", CyGame().getSymbolID(FontSymbols.TRADE_CHAR))
				
			if szBuildingEffects:
				szText += u"<link=literal>%s</link>: %s\n" % (BuildingInfo.getText(), szBuildingEffects)
		
		screen.addMultilineText(text, szText, self.X_BUILDINGS + 20, self.Y_BUILDINGS + 40, self.W_BUILDINGS - 10, self.H_BUILDINGS - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeSpecialists(self):
		screen = self.top.getScreen()
		panel = self.top.getNextWidgetName()
		screen.addPanel(panel, localText.getText("TXT_KEY_PEDIA_SPECIALISTS", ()), "", False, True, self.X_SPECIALISTS, self.Y_SPECIALISTS, self.W_SPECIALISTS, self.H_SPECIALISTS, PanelStyles.PANEL_STYLE_BLUE50)
		text = self.top.getNextWidgetName()
		screen.attachListBoxGFC(panel, text, "", TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(text, False)
		
		szText = ""
		
		for iSpecialist in range(gc.getNumSpecialistInfos()):
			SpecialistInfo = gc.getSpecialistInfo(iSpecialist)
			szSpecialistEffects = ""
			
			for iYield in range(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = SpecialistInfo.getCultureLevelYieldChange(self.iCultureLevel, iYield)
				
				if iYieldChange > 0:
					if szSpecialistEffects:
						szSpecialistEffects += u" "
						
					szSpecialistEffects += u"+%d%c" % (iYieldChange, gc.getYieldInfo(iYield).getChar())
					
			for iCommerce in range(CommerceTypes.NUM_COMMERCE_TYPES):
				iCommerceChange = SpecialistInfo.getCultureLevelCommerceChange(self.iCultureLevel, iCommerce)
				
				if iCommerceChange > 0:
					if szSpecialistEffects:
						szSpecialistEffects += u" "
						
					szSpecialistEffects += u"+%d%c" % (iCommerceChange, gc.getCommerceInfo(iCommerce).getChar())
					
			iGreatPeopleRateChange = SpecialistInfo.getCultureLevelGreatPeopleRateChange(self.iCultureLevel)
			
			if iGreatPeopleRateChange > 0:
				if szSpecialistEffects:
					szSpecialistEffects += u" "
					
				szSpecialistEffects += u"+%d%c" % (iGreatPeopleRateChange, CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR))
				
			if szSpecialistEffects:
				szText += u"<link=literal>%s</link>: %s\n" % (SpecialistInfo.getText(), szSpecialistEffects)
			
		screen.addMultilineText(text, szText, self.X_SPECIALISTS + 20, self.Y_SPECIALISTS + 40, self.W_SPECIALISTS - 10, self.H_SPECIALISTS - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)