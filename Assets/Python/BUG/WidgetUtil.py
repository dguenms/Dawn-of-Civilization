## WidgetUtil
##
## Provides functions to create new WidgetTypes and supply hover text for them.
##
## WidgetTypes
##
##   createWidget(name)
##     Creates and returns a new unique WidgetTypes constant named <name>.
##
##       <widget name="<name>"/>
##
## Hover Help Text
##
##   setWidgetHelpText(widget, text)
##     Uses static <text> string for the hover help text of <widget>.
##
##       <widget name="<widget-name>" text="<text>"/>
##
##   setWidgetHelpXml(widget, key)
##     Uses <TEXT> CIV4GameText.xml element matching <key> for the hover text of <widget>.
##     This form allows you to use translated strings as it's looked up each time it's shown.
##
##       <widget name="<widget-name>" xml="<key>"/>
##
##   setWidgetHelpFunction(widget, func)
##     Calls <func> to get the hover text of <widget> each time it's shown.
##     Use this method when you want the displayed text to change based on game conditions.
##     The function should have this signature:
##       func(eWidget, iData1, iData2, bOption)
##
##       <widget name="<widget-name>" module="<module-name>" function="<function-name>"/>
##
## Notes
##
##   Must register setWidgetHelp() as a BugGameUtils handler.
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugConfig
import BugUtil
import RFCUtils
gc = CyGlobalContext()

utils = RFCUtils.RFCUtils()

## Widget Types

g_nextWidget = WidgetTypes.NUM_WIDGET_TYPES

def createWidget(name):
	"""
	Creates and returns the next unique WidgetTypes constant to be used with custom UI widgets.
	
	If <name> already exists, a warning is logged and the widget is returned.
	Otherwise the new widget is assigned to WidgetTypes.<name> and returned.
	"""
	if hasattr(WidgetTypes, name):
		BugUtil.warn("WidgetTypes.%s already exists", name)
		return getattr(WidgetTypes, name)
	else:
		global g_nextWidget
		BugUtil.info("WidgetUtil - WidgetTypes.%s = %d", name, g_nextWidget)
		widget = WidgetTypes(g_nextWidget)
		setattr(WidgetTypes, name, widget)
		g_nextWidget += 1
		return widget


## Hover Help Text

g_widgetHelp = {}

def setWidgetHelpText(widget, text):
	"""
	Assigns the literal <text> to be used as the hover text for <widget>.
	"""
	_setWidgetHelp(widget, "Text", lambda *ignored: text)

def setWidgetHelpXml(widget, key):
	"""
	Assigns the XML <key> to be used to lookup the translated hover text for <widget>.
	"""
	_setWidgetHelp(widget, "XML", lambda *ignored: BugUtil.getPlainText(key))

def setWidgetHelpFunction(widget, func):
	"""
	Assigns the function <func> to be called to get the hover text for <widget>.
	
	The function will be called each time the hover text is needed with these parameters:
	
		eWidgetType         WidgetTypes constant
		data1               int
		data2               int
		bOption             boolean
	
	The first three are the ones used when creating the UI widget.
	I have no idea what <bOption> is or where it comes from as it's supplied by the EXE.
	"""
	_setWidgetHelp(widget, "Function", func)

def _setWidgetHelp(widget, type, func):
	"""
	Registers the hover text <func> for <widget> if it hasn't been already.
	
	Do not call this function as it is used internally by the registration functions above.
	"""
	if widget in g_widgetHelp:
		BugUtil.warn("WidgetTypes %d help already registered", widget)
	else:
		BugUtil.debug("WidgetUtil - registering %s hover help for WidgetTypes %d: %s", type, widget, func)
		g_widgetHelp[widget] = func

	
def getWidgetHelp(argsList):
	"""
	Returns the hover help text for <eWidgetType> if registered, otherwise returns an empty string.
	
	This function is a BugGameUtils handler registered in init.xml.
	"""
	eWidgetType, iData1, iData2, bOption = argsList
	
	# Leoreth: Aztec UP: sacrifice slaves
	if iData1 == 10000:
		return CyTranslator().getText("TXT_KEY_BUTTON_SACRIFICE", (utils.getTurns(5), utils.getTurns(5)))
					
	# Leoreth: Byzantine UP: bribe button
	if iData1 == 10001:
		return CyTranslator().getText("TXT_KEY_ACTION_BYZANTINE_UP", ())
	
	func = g_widgetHelp.get(eWidgetType)
	if func:
		return func(eWidgetType, iData1, iData2, bOption)
	
## Religion Screen ##
	if eWidgetType == WidgetTypes.WIDGET_HELP_RELIGION:
		if iData1 == -1:
			return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())

## Platy WorldBuilder ##
	elif eWidgetType == WidgetTypes.WIDGET_PYTHON:
		if iData1 == 1027:
			return CyTranslator().getText("TXT_KEY_WB_PLOT_DATA",())
		elif iData1 == 1028:
			return gc.getGameOptionInfo(iData2).getHelp()
		elif iData1 == 1029:
			if iData2 == 0:
				sText = CyTranslator().getText("TXT_KEY_WB_PYTHON", ())
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onFirstContact"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onChangeWar"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onVassalState"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCityAcquired"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCityBuilt"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCultureExpansion"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onGoldenAge"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onEndGoldenAge"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onGreatPersonBorn"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onPlayerChangeStateReligion"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionFounded"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionSpread"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionRemove"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationFounded"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationSpread"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationRemove"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitCreated"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitLost"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitPromoted"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onBuildingBuilt"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onProjectBuilt"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onTechAcquired"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onImprovementBuilt"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onImprovementDestroyed"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onRouteBuilt"
				sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onPlotRevealed"
				return sText
			elif iData2 == 1:
				return CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA",())
			elif iData2 == 2:
				return CyTranslator().getText("TXT_KEY_WB_TEAM_DATA",())
			elif iData2 == 3:
				return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH",())
			elif iData2 == 4:
				return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT",())
			elif iData2 == 5:
				return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()) + " + " + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ())
			elif iData2 == 6:
				return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION",())
			elif iData2 == 7:
				return CyTranslator().getText("TXT_KEY_WB_CITY_DATA2",())
			elif iData2 == 8:
				return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING",())
			elif iData2 == 9:
				return "Platy Builder\nVersion: 4.17\nWith merijn_v1 DoC features"
			elif iData2 == 10:
				return CyTranslator().getText("TXT_KEY_CONCEPT_EVENTS",())
			elif iData2 == 11:
				return CyTranslator().getText("TXT_KEY_WB_RIVER_PLACEMENT",())
			elif iData2 == 12:
				return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT",())
			elif iData2 == 13:
				return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS",())
			elif iData2 == 14:
				return CyTranslator().getText("TXT_KEY_WB_PLOT_TYPE",())
			elif iData2 == 15:
				return CyTranslator().getText("TXT_KEY_CONCEPT_TERRAIN",())
			elif iData2 == 16:
				return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_ROUTE",())
			elif iData2 == 17:
				return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_FEATURE",())
			elif iData2 == 18:
				return CyTranslator().getText("TXT_KEY_MISSION_BUILD_CITY",())
			elif iData2 == 19:
				return CyTranslator().getText("TXT_KEY_WB_ADD_BUILDINGS",())
			elif iData2 == 20:
				return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION",())
			elif iData2 == 21:
				return CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS",())
			elif iData2 == 22:
				return CyTranslator().getText("TXT_KEY_ESPIONAGE_CULTURE",())
			elif iData2 == 23:
				return CyTranslator().getText("TXT_KEY_PITBOSS_GAME_OPTIONS",())
			elif iData2 == 24:
				return CyTranslator().getText("TXT_KEY_WB_SENSIBILITY",())
			elif iData2 == 27:
				return CyTranslator().getText("TXT_KEY_WB_ADD_UNITS",())
			elif iData2 == 28:
				return CyTranslator().getText("TXT_KEY_WB_TERRITORY",())
			elif iData2 == 29:
				return CyTranslator().getText("TXT_KEY_WB_ERASE_ALL_PLOTS",())
			elif iData2 == 30:
				return CyTranslator().getText("TXT_KEY_WB_REPEATABLE",())
			elif iData2 == 31:
				return CyTranslator().getText("TXT_KEY_PEDIA_HIDE_INACTIVE", ())
			elif iData2 == 32:
				return CyTranslator().getText("TXT_KEY_WB_STARTING_PLOT", ())
			elif iData2 == 33:
				return CyTranslator().getText("TXT_KEY_INFO_SCREEN", ())
			elif iData2 == 34:
				return CyTranslator().getText("TXT_KEY_CONCEPT_TRADE", ())
			elif iData2 == 35:
				return CyTranslator().getText("TXT_KEY_WB_IN_SPAWN", ())
			elif iData2 == 36:
				return CyTranslator().getText("TXT_KEY_WB_CORE", ())
			elif iData2 == 37:
				return CyTranslator().getText("TXT_KEY_WB_SETTLERVALUE", ())
			elif iData2 == 38:
				return CyTranslator().getText("TXT_KEY_WB_WARVALUE", ())
		elif iData1 > 1029 and iData1 < 1040:
			if iData1 %2:
				return "-"
			return "+"
		elif iData1 == 1041:
			return CyTranslator().getText("TXT_KEY_WB_KILL",())
		elif iData1 == 1042:
			return CyTranslator().getText("TXT_KEY_MISSION_SKIP",())
		elif iData1 == 1043:
			if iData2 == 0:
				return CyTranslator().getText("TXT_KEY_WB_DONE",())
			elif iData2 == 1:
				return CyTranslator().getText("TXT_KEY_WB_FORTIFY",())
			elif iData2 == 2:
				return CyTranslator().getText("TXT_KEY_WB_WAIT",())
		elif iData1 == 6782:
			return CyGameTextMgr().parseCorporationInfo(iData2, False)
		elif iData1 == 6785:
			return CyGameTextMgr().getProjectHelp(iData2, False, CyCity())
		elif iData1 == 6787:
			return gc.getProcessInfo(iData2).getDescription()
		elif iData1 == 6788:
			if iData2 == -1:
				return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
			return gc.getRouteInfo(iData2).getDescription()
## City Hover Text ##
		elif iData1 > 7199 and iData1 < 7300:
			iPlayer = iData1 - 7200
			pPlayer = gc.getPlayer(iPlayer)
			pCity = pPlayer.getCity(iData2)
			if CyGame().GetWorldBuilderMode():
				sText = "<font=3>"
				if pCity.isCapital():
					sText += CyTranslator().getText("[ICON_STAR]", ())
				elif pCity.isGovernmentCenter():
					sText += CyTranslator().getText("[ICON_SILVER_STAR]", ())
				sText += u"%s: %d<font=2>" %(pCity.getName(), pCity.getPopulation())
				sTemp = ""
				if pCity.isConnectedToCapital(iPlayer):
					sTemp += CyTranslator().getText("[ICON_TRADE]", ())
				for i in xrange(gc.getNumReligionInfos()):
					if pCity.isHolyCityByType(i):
						sTemp += u"%c" %(gc.getReligionInfo(i).getHolyCityChar())
					elif pCity.isHasReligion(i):
						sTemp += u"%c" %(gc.getReligionInfo(i).getChar())

				for i in xrange(gc.getNumCorporationInfos()):
					if pCity.isHeadquartersByType(i):
						sTemp += u"%c" %(gc.getCorporationInfo(i).getHeadquarterChar())
					elif pCity.isHasCorporation(i):
						sTemp += u"%c" %(gc.getCorporationInfo(i).getChar())
				if len(sTemp) > 0:
					sText += "\n" + sTemp

				iMaxDefense = pCity.getTotalDefense(False)
				if iMaxDefense > 0:
					sText += u"\n%s: " %(CyTranslator().getText("[ICON_DEFENSE]", ()))
					iCurrent = pCity.getDefenseModifier(False)
					if iCurrent != iMaxDefense:
						sText += u"%d/" %(iCurrent)
					sText += u"%d%%" %(iMaxDefense)

				sText += u"\n%s: %d/%d" %(CyTranslator().getText("[ICON_FOOD]", ()), pCity.getFood(), pCity.growthThreshold())
				iFoodGrowth = pCity.foodDifference(True)
				if iFoodGrowth != 0:
					sText += u" %+d" %(iFoodGrowth)

				if pCity.isProduction():
					sText += u"\n%s:" %(CyTranslator().getText("[ICON_PRODUCTION]", ()))
					if not pCity.isProductionProcess():
						sText += u" %d/%d" %(pCity.getProduction(), pCity.getProductionNeeded())
						iProduction = pCity.getCurrentProductionDifference(False, True)
						if iProduction != 0:
							sText += u" %+d" %(iProduction)
					sText += u" (%s)" %(pCity.getProductionName())

				iGPRate = pCity.getGreatPeopleRate()
				iProgress = pCity.getGreatPeopleProgress()
				if iGPRate > 0 or iProgress > 0:
					sText += u"\n%s: %d/%d %+d" %(CyTranslator().getText("[ICON_GREATPEOPLE]", ()), iProgress, pPlayer.greatPeopleThreshold(False), iGPRate)

				sText += u"\n%s: %d/%d (%s)" %(CyTranslator().getText("[ICON_CULTURE]", ()), pCity.getCulture(iPlayer), pCity.getCultureThreshold(), gc.getCultureLevelInfo(pCity.getCultureLevel()).getDescription())

				lTemp = []
				for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
					iAmount = pCity.getCommerceRateTimes100(i)
					if iAmount <= 0: continue
					sTemp = u"%d.%02d%c" %(pCity.getCommerceRate(i), pCity.getCommerceRateTimes100(i)%100, gc.getCommerceInfo(i).getChar())
					lTemp.append(sTemp)
				if len(lTemp) > 0:
					sText += "\n"
					for i in xrange(len(lTemp)):
						sText += lTemp[i]
						if i < len(lTemp) - 1:
							sText += ", "

				iMaintenance = pCity.getMaintenanceTimes100()
				if iMaintenance != 0:
					sText += "\n" + CyTranslator().getText("[COLOR_WARNING_TEXT]", ()) + CyTranslator().getText("INTERFACE_CITY_MAINTENANCE", ()) + " </color>"
					sText += u"-%d.%02d%c" %(iMaintenance/100, iMaintenance%100, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())

				lBuildings = []
				lWonders = []
				for i in xrange(gc.getNumBuildingInfos()):
					if pCity.isHasBuilding(i):
						Info = gc.getBuildingInfo(i)
						if isLimitedWonderClass(Info.getBuildingClassType()):
							lWonders.append(Info.getDescription())
						else:
							lBuildings.append(Info.getDescription())
				if len(lBuildings) > 0:
					lBuildings.sort()
					sText += "\n" + CyTranslator().getText("[COLOR_BUILDING_TEXT]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()) + ": </color>"
					for i in xrange(len(lBuildings)):
						sText += lBuildings[i]
						if i < len(lBuildings) - 1:
							sText += ", "
				if len(lWonders) > 0:
					lWonders.sort()
					sText += "\n" + CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS", ()) + ": </color>"
					for i in xrange(len(lWonders)):
						sText += lWonders[i]
						if i < len(lWonders) - 1:
							sText += ", "
				sText += "</font>"
				return sText
## Religion Widget Text##
		elif iData1 == 7869:
			return CyGameTextMgr().parseReligionInfo(iData2, False)
## Building Widget Text##
		elif iData1 == 7870:
			return CyGameTextMgr().getBuildingHelp(iData2, False, False, False, None)
## Tech Widget Text##
		elif iData1 == 7871:
			if iData2 == -1:
				return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
			return CyGameTextMgr().getTechHelp(iData2, False, False, False, False, -1)
## Civilization Widget Text##
		elif iData1 == 7872:
			iCiv = iData2 % 10000
			return CyGameTextMgr().parseCivInfos(iCiv, False)
## Promotion Widget Text##
		elif iData1 == 7873:
			return CyGameTextMgr().getPromotionHelp(iData2, False)
## Feature Widget Text##
		elif iData1 == 7874:
			if iData2 == -1:
				return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
			iFeature = iData2 % 10000
			return CyGameTextMgr().getFeatureHelp(iFeature, False)
## Terrain Widget Text##
		elif iData1 == 7875:
			return CyGameTextMgr().getTerrainHelp(iData2, False)
## Leader Widget Text##
		elif iData1 == 7876:
			iLeader = iData2 % 10000
			return CyGameTextMgr().parseLeaderTraits(iLeader, -1, False, False)
## Improvement Widget Text##
		elif iData1 == 7877:
			if iData2 == -1:
				return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
			return CyGameTextMgr().getImprovementHelp(iData2, False)
## Bonus Widget Text##
		elif iData1 == 7878:
			if iData2 == -1:
				return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
			return CyGameTextMgr().getBonusHelp(iData2, False)
## Specialist Widget Text##
		elif iData1 == 7879:
			return CyGameTextMgr().getSpecialistHelp(iData2, False)
## Yield Text##
		elif iData1 == 7880:
			return gc.getYieldInfo(iData2).getDescription()
## Commerce Text##
		elif iData1 == 7881:
			return gc.getCommerceInfo(iData2).getDescription()
## Build Text##
		elif iData1 == 7882:
			return gc.getBuildInfo(iData2).getDescription()
## Corporation Screen ##
		elif iData1 == 8201:
			return CyGameTextMgr().parseCorporationInfo(iData2, False)
## Military Screen ##
		elif iData1 == 8202:
			if iData2 == -1:
				return CyTranslator().getText("TXT_KEY_PEDIA_ALL_UNITS", ())
			return CyGameTextMgr().getUnitHelp(iData2, False, False, False, None)
		elif iData1 > 8299 and iData1 < 8400:
			iPlayer = iData1 - 8300
			pUnit = gc.getPlayer(iPlayer).getUnit(iData2)
			sText = CyGameTextMgr().getSpecificUnitHelp(pUnit, True, False)
			if CyGame().GetWorldBuilderMode():
				sText += "\n" + CyTranslator().getText("TXT_KEY_WB_UNIT", ()) + " ID: " + str(iData2)
				sText += "\n" + CyTranslator().getText("TXT_KEY_WB_GROUP", ()) + " ID: " + str(pUnit.getGroupID())
				sText += "\n" + "X: " + str(pUnit.getX()) + ", Y: " + str(pUnit.getY())
				sText += "\n" + CyTranslator().getText("TXT_KEY_WB_AREA_ID", ()) + ": "  + str(pUnit.plot().getArea())
			return sText
## Civics Screen ##
		elif iData1 == 8205 or iData1 == 8206:
			sText = CyGameTextMgr().parseCivicInfo(iData2, False, True, False)
			if gc.getCivicInfo(iData2).getUpkeep() > -1:
				sText += "\n" + gc.getUpkeepInfo(gc.getCivicInfo(iData2).getUpkeep()).getDescription()
			else:
				sText += "\n" + CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())
			return sText
## Ultrapack ##
		
		#Merijn functions
		elif iData1 == 22001:
			if iData2 == 0:
				sText = CyTranslator().getText("TXT_KEY_WB_ENABLE_CIV", ())
			else:
				sText = CyTranslator().getText("TXT_KEY_WB_DISABLE_CIV", ())
			return sText
			
		elif iData1 == 22011:
			return CyTranslator().getText("TXT_KEY_WB_CORE_ADD", ())
		elif iData1 == 22012:
			return CyTranslator().getText("TXT_KEY_WB_CORE_REMOVE", ())
		elif iData1 == 22003:
			return CyTranslator().getText("TXT_KEY_WB_CHANGE_SETTLERVALUE", ())
			
		elif iData1 >= 22300 and iData1 < 22325:
			sText = "-" + str(iData2)
			return sText
		elif iData1 >= 22400 and iData1 < 22425:
			sText = "+" + str(iData2)
			return sText
			
		elif iData1 == 22005:
			return " "
		elif iData1 == 22006:
			if iData2 == 1:
				return CyTranslator().getText("TXT_KEY_WB_SHOW", ())
			else:
				return CyTranslator().getText("TXT_KEY_WB_HIDE", ())

	return u""

## Configuration Handler

class WidgetHandler(BugConfig.Handler):
	
	TAG = "widget"
	
	def __init__(self):
		BugConfig.Handler.__init__(self, WidgetHandler.TAG, "name text xml module function")
		self.addAttribute("name", True)
		self.addAttribute("text")
		self.addAttribute("xml")
		self.addAttribute("module", False, True)
		self.addAttribute("function")
	
	def handle(self, element, name, text, xml, module, function):
		widget = createWidget(name)
		if text:
			setWidgetHelpText(widget, text)
		elif xml:
			setWidgetHelpXml(widget, xml)
		elif module and function:
			setWidgetHelpFunction(widget, BugUtil.lookupFunction(module, function))
