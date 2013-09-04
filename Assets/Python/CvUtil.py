## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
#
# for error reporting
import traceback

# for file ops
import os
import sys

# For Civ game code access
from CvPythonExtensions import *

# For exception handling
SHOWEXCEPTIONS = 1

# for C++ compatibility
false=False
true=True

# globals
gc = CyGlobalContext()
FontIconMap = {}
localText = CyTranslator()

#
# Popup context enums, values greater than 999 are reserved for events
#

# DEBUG TOOLS
PopupTypeEntityEventTest = 4
PopupTypeEffectViewer = 5

# HELP SCREENS
PopupTypeMilitaryAdvisor = 103
PopupTypePlayerSelect = 104

# WORLD BUILDER
PopupTypeWBContextStart = 200
PopupTypeWBEditCity = PopupTypeWBContextStart 
PopupTypeWBEditUnit = 201
PopupTypeWBContextEnd	= 299

# EVENT ID VALUES (also used in popup contexts)
EventGetEspionageTarget = 4999
EventEditCityName = 5000
EventEditCity = 5001
EventPlaceObject = 5002
EventAwardTechsAndGold = 5003
EventEditUnitName = 5006
EventCityWarning = 5007
EventWBAllPlotsPopup = 5008
EventWBLandmarkPopup = 5009
EventWBScriptPopup = 5010
EventWBStartYearPopup = 5011
EventShowWonder = 5012

EventLButtonDown=1
EventLcButtonDblClick=2
EventRButtonDown=3
EventBack=4
EventForward=5
EventKeyDown=6
EventKeyUp=7

# List of unreported Events
SilentEvents = [EventEditCityName, EventEditUnitName]

# BUG - Core - start

# Event IDs
BUG_FIRST_EVENT = 5050
g_nextEventID = BUG_FIRST_EVENT
g_bugEvents = {}
def getNewEventID(name=None, silent=True):
	"""
	Defines a new event and returns its unique ID to be passed to BugEventManager.beginEvent(id).
	If name is given, it is stored in a map for lookup by ID later for debugging.
	"""
	global g_nextEventID
	id = g_nextEventID
	g_nextEventID += 1
	if name:
		g_bugEvents[id] = name
	if silent:
		addSilentEvent(id)
	return id

def getEventName(id):
	return g_bugEvents[id]

def addSilentEvent(id):
	if id not in SilentEvents:
		SilentEvents.append(id)

# Screen IDs
BUG_FIRST_SCREEN = 1000
g_nextScreenID = BUG_FIRST_SCREEN
def getNewScreenID():
	"""
	Returns the next unique screen ID to be used with CyGInterfaceScreen.
	"""
	global g_nextScreenID
	id = g_nextScreenID
	g_nextScreenID += 1
	return id
# BUG - Core - end

# Popup defines (TODO: Expose these from C++)
FONT_CENTER_JUSTIFY=1<<2
FONT_RIGHT_JUSTIFY=1<<1
FONT_LEFT_JUSTIFY=1<<0

def convertToUnicode(s):
	"if the string is non unicode, convert it to unicode by decoding it using 8859-1, latin_1"
	if (isinstance(s, str)):
		return s.decode("latin_1")
	return s
	
def convertToStr(s):
	"if the string is unicode, convert it to str by encoding it using 8859-1, latin_1"
	if (isinstance(s, unicode)):
		return s.encode("latin_1")
	return s

class RedirectDebug:
	"""Send Debug Messages to Civ Engine"""
	def __init__(self):
		self.m_PythonMgr = CyPythonMgr()
	def write(self, stuff):
		# if str is non unicode and contains encoded unicode data, supply the right encoder to encode it into a unicode object
		if (isinstance(stuff, unicode)):
			self.m_PythonMgr.debugMsgWide(stuff)
		else:
			self.m_PythonMgr.debugMsg(stuff)
		
class RedirectError:
	"""Send Error Messages to Civ Engine"""
	def __init__(self):
		self.m_PythonMgr = CyPythonMgr()
	def write(self, stuff):
		# if str is non unicode and contains encoded unicode data, supply the right encoder to encode it into a unicode object
		if (isinstance(stuff, unicode)):
			self.m_PythonMgr.errorMsgWide(stuff)
		else:
			self.m_PythonMgr.errorMsg(stuff)

def myExceptHook(type, value, tb):
	lines=traceback.format_exception(type, value, tb)
	#pre= "---------------------Traceback lines-----------------------\n"
	mid="\n".join(lines)
	#post="-----------------------------------------------------------"
	#total = pre+mid+post
	total=mid
	if SHOWEXCEPTIONS:
		sys.stderr.write(total)
	else:
		sys.stdout.write(total)

def pyPrint(stuff):
	stuff = 'PY:' + stuff + "\n"
	sys.stdout.write(stuff)

def pyAssert(cond, msg):
	if (cond==False):
		sys.stderr.write(msg)
	assert(cond, msg)
	
def getScoreComponent(iRawScore, iInitial, iMax, iFactor, bExponential, bFinal, bVictory):

	if gc.getGame().getEstimateEndTurn() == 0:
		return 0

	if bFinal and bVictory:
		fTurnRatio = float(gc.getGame().getGameTurn()) / float(gc.getGame().getEstimateEndTurn())
		if bExponential and (iInitial != 0):
			fRatio = iMax / iInitial
			iMax = iInitial * pow(fRatio, fTurnRatio)
		else:
			iMax = iInitial + fTurnRatio * (iMax - iInitial)

	iFree = (gc.getDefineINT("SCORE_FREE_PERCENT") * iMax) / 100
	if (iFree + iMax) != 0:
		iScore = (iFactor * (iRawScore + iFree)) / (iFree + iMax)
	else:
		iScore = iFactor
		
	if bVictory:
		iScore = ((100 + gc.getDefineINT("SCORE_VICTORY_PERCENT")) * iScore) / 100

	if bFinal:
		iScore = ((100 + gc.getDefineINT("SCORE_HANDICAP_PERCENT_OFFSET") + (gc.getGame().getHandicapType() * gc.getDefineINT("SCORE_HANDICAP_PERCENT_PER"))) * iScore) / 100

	return int(iScore)
	
def getOppositeCardinalDirection(dir):
	return (dir + 2) % CardinalDirectionTypes.NUM_CARDINALDIRECTION_TYPES

def shuffle(num, rand):
	"returns a tuple of size num of shuffled numbers"	
	piShuffle = [0]*num
	shuffleList(num, rand, piShuffle)	# implemented in C for speed
	return piShuffle

def spawnUnit(iUnit, pPlot, pPlayer):
	pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
	return 1

def findInfoTypeNum(infoGetter, numInfos, typeStr):
	if (typeStr == 'NONE'):
		return -1
	idx = gc.getInfoTypeForString(typeStr)
	pyAssert(idx != -1, "Can't find type enum for type tag %s" %(typeStr,))
	return idx

def getInfo(strInfoType, strInfoName):	# returns info for InfoType
	#set Type to lowercase
	strInfoType = strInfoType.lower()
	strInfoName = strInfoName.capitalize()
	
	#get the appropriate dictionary item
	infoDict = GlobalInfosMap.get(strInfoType)
	#get the number of infos
	numInfos = infoDict['NUM']()
	#loop through each info
	for i in range(numInfos):
		loopInfo = infoDict['GET'](i)
		
		if loopInfo.getDescription() == strInfoName:
			#and return the one requested
			return loopInfo

def AdjustBuilding(add, all, BuildingIdx, pCity): # adds/removes buildings from a city
	"Function for toggling buildings in cities"
	if (BuildingIdx!= -1):  
		if (all):                #Add/Remove ALL
			for i in range(BuildingIdx):
				pCity.setNumRealBuildingIdx(i,add)
		else:
			pCity.setNumRealBuildingIdx(BuildingIdx,add)
	return 0

def getIcon(iconEntry):						# returns Font Icons
	global FontIconMap
	
	iconEntry = iconEntry.lower()
	if (FontIconMap.has_key(iconEntry)):
		return 	FontIconMap.get(iconEntry)
	else:
		return (u"%c" %(191,))

def combatDetailMessageBuilder(cdUnit, ePlayer, iChange):
	if (cdUnit.iExtraCombatPercent != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_EXTRA_COMBAT_PERCENT",(cdUnit.iExtraCombatPercent * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iAnimalCombatModifierTA != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_ANIMAL_COMBAT",(cdUnit.iAnimalCombatModifierTA * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iAIAnimalCombatModifierTA != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_AI_ANIMAL_COMBAT",(cdUnit.iAIAnimalCombatModifierTA * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iAnimalCombatModifierAA != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_ANIMAL_COMBAT",(cdUnit.iAnimalCombatModifierAA * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iAIAnimalCombatModifierAA != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_AI_ANIMAL_COMBAT",(cdUnit.iAIAnimalCombatModifierAA * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iBarbarianCombatModifierTB != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_BARBARIAN_COMBAT",(cdUnit.iBarbarianCombatModifierTB * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)
		
	if (cdUnit.iAIBarbarianCombatModifierTB != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_BARBARIAN_AI_COMBAT",(cdUnit.iAIBarbarianCombatModifierTB * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iBarbarianCombatModifierAB != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_BARBARIAN_COMBAT",(cdUnit.iBarbarianCombatModifierAB * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)
		
	if (cdUnit.iAIBarbarianCombatModifierAB != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_BARBARIAN_AI_COMBAT",(cdUnit.iAIBarbarianCombatModifierAB * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iPlotDefenseModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_PLOT_DEFENSE",(cdUnit.iPlotDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iFortifyModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_FORTIFY",(cdUnit.iFortifyModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iCityDefenseModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CITY_DEFENSE",(cdUnit.iCityDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)
		
	if (cdUnit.iHillsAttackModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_HILLS_ATTACK",(cdUnit.iHillsAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)
		
	if (cdUnit.iHillsDefenseModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_HILLS",(cdUnit.iHillsDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)
		
	if (cdUnit.iFeatureAttackModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_FEATURE_ATTACK",(cdUnit.iFeatureAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)
		
	if (cdUnit.iFeatureDefenseModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_FEATURE",(cdUnit.iFeatureDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)
		
	if (cdUnit.iTerrainAttackModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_TERRAIN_ATTACK",(cdUnit.iTerrainAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iTerrainDefenseModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_TERRAIN",(cdUnit.iTerrainDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iCityAttackModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CITY_ATTACK",(cdUnit.iCityAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iDomainDefenseModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CITY_DOMAIN_DEFENSE",(cdUnit.iDomainDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iCityBarbarianDefenseModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CITY_BARBARIAN_DEFENSE",(cdUnit.iCityBarbarianDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iClassDefenseModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_DEFENSE",(cdUnit.iClassDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iClassAttackModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_ATTACK",(cdUnit.iClassAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iCombatModifierT != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_COMBAT",(cdUnit.iCombatModifierT * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iCombatModifierA != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_COMBAT",(cdUnit.iCombatModifierA * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iDomainModifierA != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_DOMAIN",(cdUnit.iDomainModifierA * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iDomainModifierT != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_DOMAIN",(cdUnit.iDomainModifierT * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iAnimalCombatModifierA != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_ANIMAL_COMBAT",(cdUnit.iAnimalCombatModifierA * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iAnimalCombatModifierT != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_ANIMAL_COMBAT",(cdUnit.iAnimalCombatModifierT * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iRiverAttackModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_RIVER_ATTACK",(cdUnit.iRiverAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iAmphibAttackModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_AMPHIB_ATTACK",(cdUnit.iAmphibAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

def combatMessageBuilder(cdAttacker, cdDefender, iCombatOdds):
	combatMessage = ""
	if (cdAttacker.eOwner == cdAttacker.eVisualOwner):
		combatMessage += "%s's " %(gc.getPlayer(cdAttacker.eOwner).getName(),)
	combatMessage += "%s (%.2f)" %(cdAttacker.sUnitName,cdAttacker.iCurrCombatStr/100.0,)
	combatMessage += " " + localText.getText("TXT_KEY_COMBAT_MESSAGE_VS", ()) + " "
	if (cdDefender.eOwner == cdDefender.eVisualOwner):
		combatMessage += "%s's " %(gc.getPlayer(cdDefender.eOwner).getName(),)
	combatMessage += "%s (%.2f)" %(cdDefender.sUnitName,cdDefender.iCurrCombatStr/100.0,)
	CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
	CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
	combatMessage = "%s %.1f%%" %(localText.getText("TXT_KEY_COMBAT_MESSAGE_ODDS", ()),iCombatOdds/10.0,)
	CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
	CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
	combatDetailMessageBuilder(cdAttacker,cdAttacker.eOwner,-1)
	combatDetailMessageBuilder(cdDefender,cdAttacker.eOwner,1)
	combatDetailMessageBuilder(cdAttacker,cdDefender.eOwner,-1)
	combatDetailMessageBuilder(cdDefender,cdDefender.eOwner,1)
	
def initDynamicFontIcons():
	global FontIconMap
	
	info = ""
	desc = ""
	# add Commerce Icons
	for i in range(CommerceTypes.NUM_COMMERCE_TYPES):
		info = gc.getCommerceInfo(i)
		desc = info.getDescription().lower()
		addIconToMap(info.getChar, desc)
	# add Yield Icons
	for i in range(YieldTypes.NUM_YIELD_TYPES):
		info = gc.getYieldInfo(i)
		desc = info.getDescription().lower()
		addIconToMap(info.getChar, desc)
	# add Religion & Holy City Icons
	for i in range(gc.getNumReligionInfos()):
		info = gc.getReligionInfo(i)
		desc = info.getDescription().lower()
		addIconToMap(info.getChar, desc)
		addIconToMap(info.getHolyCityChar, desc)
	for key in OtherFontIcons.keys():
		#print key
		FontIconMap[key] = (u"%c" % CyGame().getSymbolID(OtherFontIcons.get(key)))
	
	#print FontIconMap
	
def addIconToMap(infoChar, desc):
	global FontIconMap
	desc = convertToStr(desc)
	print "%s - %s" %(infoChar(), desc)
	uc = infoChar()
	if (uc>=0):
		FontIconMap[desc] = u"%c" %(uc,)

OtherFontIcons = { 'happy' : FontSymbols.HAPPY_CHAR,
				'unhappy' : FontSymbols.UNHAPPY_CHAR,
				'healthy' : FontSymbols.HEALTHY_CHAR,
				'unhealthy' : FontSymbols.UNHEALTHY_CHAR,
				'bullet' : FontSymbols.BULLET_CHAR,
				'strength' : FontSymbols.STRENGTH_CHAR,
				'moves' : FontSymbols.MOVES_CHAR,
				'religion' : FontSymbols.RELIGION_CHAR,
				'star' : FontSymbols.STAR_CHAR,
				'silver star' : FontSymbols.SILVER_STAR_CHAR,
				'trade' : FontSymbols.TRADE_CHAR,
				'defense' : FontSymbols.DEFENSE_CHAR,
				'greatpeople' : FontSymbols.GREAT_PEOPLE_CHAR,
				'badgold' : FontSymbols.BAD_GOLD_CHAR,
				'badfood' : FontSymbols.BAD_FOOD_CHAR,
				'eatenfood' : FontSymbols.EATEN_FOOD_CHAR,
				'goldenage' : FontSymbols.GOLDEN_AGE_CHAR,
				'angrypop' : FontSymbols.ANGRY_POP_CHAR,
				'openBorders' : FontSymbols.OPEN_BORDERS_CHAR,
				'defensivePact' : FontSymbols.DEFENSIVE_PACT_CHAR,
				'map' : FontSymbols.MAP_CHAR,
				'occupation' : FontSymbols.OCCUPATION_CHAR,
				'power' : FontSymbols.POWER_CHAR,
				}

GlobalInfosMap = {	'bonus': {'NUM': gc.getNumBonusInfos, 'GET': gc.getBonusInfo},
					'improvement': {'NUM': gc.getNumImprovementInfos, 'GET': gc.getImprovementInfo},
					'yield': {'NUM': YieldTypes.NUM_YIELD_TYPES, 'GET': gc.getYieldInfo},
					'religion': {'NUM': gc.getNumReligionInfos, 'GET': gc.getReligionInfo},
					'tech': {'NUM': gc.getNumTechInfos, 'GET': gc.getTechInfo},
					'unit': {'NUM': gc.getNumUnitInfos, 'GET': gc.getUnitInfo},
					'civic': {'NUM': gc.getNumCivicInfos, 'GET': gc.getCivicInfo},
					'building': {'NUM': gc.getNumBuildingInfos, 'GET': gc.getBuildingInfo},
					'terrain': {'NUM': gc.getNumTerrainInfos, 'GET': gc.getTerrainInfo},
					'trait': {'NUM': gc.getNumTraitInfos, 'GET': gc.getTraitInfo},
					'feature' : {'NUM': gc.getNumFeatureInfos, 'GET': gc.getFeatureInfo},
					'route': {'NUM': gc.getNumRouteInfos, 'GET': gc.getRouteInfo},
					'promotion': {'NUM':gc.getNumPromotionInfos, 'GET': gc.getPromotionInfo},
				}
