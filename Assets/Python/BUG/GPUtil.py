## GPUtil
##
## Utilities for dealing with Great People.
##
## MODDERS
##
##   There are four places where you must add information about your new great people.
##   This is also necessary if you assign GP points to buildings that don't normally get them,
##   for example GG points to Heroic Epic.
##
##     1. Unit Type
##     2. Named constant
##     3. Color
##     4. Icon (font glyph or string)
##
## Notes
##   - Must be initialized externally by calling init()
##
## Copyright (c) 2007-2009 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugUtil
import FontUtil
import PlayerUtil

gc = CyGlobalContext()

# Generic GP icon
g_gpIcon = None

# Unit Type of each great person that can gain GP points
g_gpBarList = (
	"UNIT_GREAT_SPY",
	"UNIT_ENGINEER",
	"UNIT_MERCHANT",
	"UNIT_SCIENTIST",
	"UNIT_ARTIST",
	"UNIT_PROPHET",
	"UNIT_GREAT_GENERAL",
# MOD: specify the unit type (XML key) for each new great person (1)
	#"UNIT_DOCTOR",
)

# Named constants for each great person and total number of GP types
# These must be in the exact same order as the list above
NUM_GP = len(g_gpBarList)
(
	GP_SPY,
	GP_ENGINEER,
	GP_MERCHANT,
	GP_SCIENTIST,
	GP_ARTIST,
	GP_PROPHET,
	GP_GENERAL,
# MOD: define a constant for each new great person in same order as above (2)
	#GP_DOCTOR,
) = range(NUM_GP)

# Map each GP type to unit ID, color, and icon to show in GP Bar
g_gpUnitTypes = None
g_gpColors = None
g_unitIcons = None


# Information

def init():
	global g_gpIcon
	g_gpIcon = FontUtil.getChar("greatpeople")
	
	global g_gpUnitTypes
	g_gpUnitTypes = [None] * NUM_GP
	for i, s in enumerate(g_gpBarList):
		g_gpUnitTypes[i] = gc.getInfoTypeForString(s)
	
	global g_gpColors
	g_gpColors = [None] * NUM_GP
	g_gpColors[GP_SPY] = gc.getInfoTypeForString("COLOR_WHITE")
	g_gpColors[GP_ENGINEER] = gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType()
	g_gpColors[GP_MERCHANT] = gc.getInfoTypeForString("COLOR_YELLOW")
	g_gpColors[GP_SCIENTIST] = gc.getInfoTypeForString("COLOR_RESEARCH_STORED")
	g_gpColors[GP_ARTIST] = gc.getInfoTypeForString("COLOR_CULTURE_STORED")
	g_gpColors[GP_PROPHET] = gc.getInfoTypeForString("COLOR_BLUE")
	g_gpColors[GP_GENERAL] = gc.getInfoTypeForString("COLOR_RED")
	# MOD: specify color for each new great person (3)
	#g_gpColors[GP_DOCTOR] = gc.getInfoTypeForString("COLOR_WHITE")
	
	global g_unitIcons
	g_unitIcons = {}
	g_unitIcons[g_gpUnitTypes[GP_SPY]] = FontUtil.getChar(FontSymbols.COMMERCE_ESPIONAGE_CHAR)
	g_unitIcons[g_gpUnitTypes[GP_ENGINEER]] = FontUtil.getChar(FontSymbols.YIELD_PRODUCTION_CHAR)
	g_unitIcons[g_gpUnitTypes[GP_MERCHANT]] = FontUtil.getChar(FontSymbols.COMMERCE_GOLD_CHAR)
	g_unitIcons[g_gpUnitTypes[GP_SCIENTIST]] = FontUtil.getChar(FontSymbols.COMMERCE_RESEARCH_CHAR)
	g_unitIcons[g_gpUnitTypes[GP_ARTIST]] = FontUtil.getChar(FontSymbols.COMMERCE_CULTURE_CHAR)
	g_unitIcons[g_gpUnitTypes[GP_PROPHET]] = FontUtil.getChar(FontSymbols.RELIGION_CHAR)
	g_unitIcons[g_gpUnitTypes[GP_GENERAL]] = FontUtil.getChar(FontSymbols.GREAT_GENERAL_CHAR)
	# MOD: specify icon (font glyph) for each new great person (4)
	#g_unitIcons[g_gpUnitTypes[GP_DOCTOR]] = FontUtil.getChar(FontSymbols.HEALTHY_CHAR)

def getUnitType(gpType):
	return g_gpUnitTypes[gpType]

def getColor(gpType):
	return g_gpColors[gpType]

def getUnitIcon(iUnit):
	try:
		return g_unitIcons[iUnit]
	except:
		BugUtil.warn("no GP icon for unit %d", iUnit)
		return u"%c" % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR)


# Getting Progress

def getDisplayCity():
	"""
	Returns the city to display in the progress bar.
	"""
	pHeadSelectedCity = CyInterface().getHeadSelectedCity()
	if (pHeadSelectedCity and pHeadSelectedCity.getTeam() == gc.getGame().getActiveTeam()):
		city = pHeadSelectedCity
		iTurns = getCityTurns(city)
	else:
		city, iTurns = findNextCity()
		if not city:
			city, iGPP = findMaxCity()
			iTurns = None
	return (city, iTurns)

def findNextCity():
	iMinTurns = None
	iTurns = 0
	player = gc.getPlayer(gc.getGame().getActivePlayer())
	iThreshold = player.greatPeopleThreshold(False)
	bestCity = None
	for city in PlayerUtil.playerCities(player):
		iRate = city.getGreatPeopleRate()
		if (iRate > 0):
			iProgress = city.getGreatPeopleProgress()
			iTurns = (iThreshold - iProgress + iRate - 1) / iRate
			if (iMinTurns is None or iTurns < iMinTurns):
				iMinTurns = iTurns
				bestCity = city
	return (bestCity, iMinTurns)

def findMaxCity():
	iMaxProgress = 0
	player = gc.getPlayer(gc.getGame().getActivePlayer())
	bestCity = None
	for city in PlayerUtil.playerCities(player):
		iProgress = city.getGreatPeopleProgress()
		if (iProgress > iMaxProgress):
			iMaxProgress = iProgress
			bestCity = city
	return (bestCity, iMaxProgress)

def getCityTurns(city):
	if (city):
		player = gc.getPlayer(city.getOwner())
		iThreshold = player.greatPeopleThreshold(False)
		iRate = city.getGreatPeopleRate()
		if (iRate > 0):
			iProgress = city.getGreatPeopleProgress()
			iTurns = (iThreshold - iProgress + iRate - 1) / iRate
			return iTurns
	return None

def calcPercentages(city):
	# Calc total rate
	iTotal = 0
	for iUnit in g_gpUnitTypes:
		iTotal += city.getGreatPeopleUnitProgress(iUnit)
	# Calc individual percentages based on rates and total
	percents = []
	if (iTotal > 0):
		iLeftover = 100
		for iUnit in range(gc.getNumUnitInfos()):
#			iUnit = getUnitType(gpType)
			iProgress = city.getGreatPeopleUnitProgress(iUnit)
			if (iProgress > 0):
				iPercent = 100 * iProgress / iTotal
				iLeftover -= iPercent
				percents.append((iPercent, iUnit))
		# Add remaining from 100 to first in list to match Civ4
		if (iLeftover > 0):
			percents[0] = (percents[0][0] + iLeftover, percents[0][1])
	return percents


# Displaying Progress

def getHoverText(eWidgetType, iData1, iData2, bOption):
	city, iTurns = getDisplayCity()
	if (not city):
		# no rate or progress in any city and no city selected
		return BugUtil.getText("TXT_KEY_MISC_GREAT_PERSON", (0, PlayerUtil.getActivePlayer().greatPeopleThreshold(False)))
	iThreshold = gc.getPlayer(city.getOwner()).greatPeopleThreshold(False)
	iProgress = city.getGreatPeopleProgress()
	iRate = city.getGreatPeopleRate()
	szText = BugUtil.colorText(city.getName(), "COLOR_HIGHLIGHT_TEXT")
	szText += u"\n"
	szText += BugUtil.getText("TXT_KEY_MISC_GREAT_PERSON", (iProgress, iThreshold))
	if (iRate > 0):
		szText += u"\n%d%s%s " % (iRate, g_gpIcon, BugUtil.getPlainText("TXT_KEY_PER_TURN"))
		szText += BugUtil.getText("INTERFACE_CITY_TURNS", (iTurns,))
	
	percents = calcPercentages(city)
	if (len(percents) > 0):
		percents.sort()
		percents.reverse()
		szText += u"\n"
		for iPercent, iUnit in percents:
#			iUnit = getUnitType(gpType)
			szText += u"\n%s%s - %d%%" % (getUnitIcon(iUnit), gc.getUnitInfo(iUnit).getDescription(), iPercent)
	return szText

def getGreatPeopleText(city, iGPTurns, iGPBarWidth, bGPBarTypesNone, bGPBarTypesOne, bIncludeCityName):
	sGreatPeopleChar = u"%c" % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR)
	if (not city):
		szText = BugUtil.getText("INTERFACE_GREAT_PERSON_NONE", (sGreatPeopleChar, ))
	elif (bGPBarTypesNone):
		if (iGPTurns):
			if (bIncludeCityName):
				szText = BugUtil.getText("INTERFACE_GREAT_PERSON_CITY_TURNS", (sGreatPeopleChar, city.getName(), iGPTurns))
			else:
				szText = BugUtil.getText("INTERFACE_GREAT_PERSON_TURNS", (sGreatPeopleChar, iGPTurns))
		else:
			if (bIncludeCityName):
				szText = BugUtil.getText("INTERFACE_GREAT_PERSON_CITY", (sGreatPeopleChar, city.getName()))
			else:
				szText = sGreatPeopleChar
	else:
		lPercents = calcPercentages(city)
		if (len(lPercents) == 0):
			if (iGPTurns):
				if (bIncludeCityName):
					szText = BugUtil.getText("INTERFACE_GREAT_PERSON_CITY_TURNS", (sGreatPeopleChar, city.getName(), iGPTurns))
				else:
					szText = BugUtil.getText("INTERFACE_GREAT_PERSON_TURNS", (sGreatPeopleChar, iGPTurns))
			else:
				if (bIncludeCityName):
					szText = BugUtil.getText("INTERFACE_GREAT_PERSON_CITY", (sGreatPeopleChar, city.getName()))
				else:
					szText = sGreatPeopleChar
		else:
			lPercents.sort()
			lPercents.reverse()
			if (bGPBarTypesOne or len(lPercents) == 1):
				iPercent, iUnit = lPercents[0]
				pInfo = gc.getUnitInfo(iUnit)
				if (iGPTurns):
					if (bIncludeCityName):
						szText = BugUtil.getText("INTERFACE_GREAT_PERSON_CITY_TURNS", (pInfo.getDescription(), city.getName(), iGPTurns))
					else:
						szText = BugUtil.getText("INTERFACE_GREAT_PERSON_TURNS", (pInfo.getDescription(), iGPTurns))
				else:
					if (bIncludeCityName):
						szText = BugUtil.getText("INTERFACE_GREAT_PERSON_CITY", (pInfo.getDescription(), city.getName()))
					else:
						szText = unicode(pInfo.getDescription())
			else:
				if (iGPTurns):
					if (bIncludeCityName):
						szText = BugUtil.getText("INTERFACE_GREAT_PERSON_CITY_TURNS", (sGreatPeopleChar, city.getName(), iGPTurns))
					else:
						szText = BugUtil.getText("INTERFACE_GREAT_PERSON_TURNS", (sGreatPeopleChar, iGPTurns))
				else:
					if (bIncludeCityName):
						szText = BugUtil.getText("INTERFACE_GREAT_PERSON_CITY", (sGreatPeopleChar, city.getName()))
					else:
						szText = sGreatPeopleChar + u":"
				szTypes = ""
				for iPercent, iUnit in lPercents:
					szNewTypes = szTypes + u" %c%d%%" % (getUnitIcon(iUnit), iPercent)
					szNewText = szText + u"<font=2> -%s</font>" % szTypes
					if (CyInterface().determineWidth(szNewText) > iGPBarWidth - 10):
						# Keep under width
						break
					szTypes = szNewTypes
				if (len(szTypes) > 0):
					szText += u"<font=2> -%s</font>" % szTypes
	return szText
