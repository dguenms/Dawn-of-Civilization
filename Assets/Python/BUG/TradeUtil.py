## TradeUtil
##
## Utilities for dealing with Trades and TradeData.
##
## Trading Partners
##
##   canTrade(playerOrID, withPlayerOrID)
##     Returns True if <player> can open the trade window with <withPlayer>.
##
##   getTechTradePartners(playerOrID)
##     Returns a list of CyPlayers that can trade technologies with <player>.
##
##   getBonusTradePartners(playerOrID)
##     Returns a list of CyPlayers that can trade bonuses with <player>.
##
##   getGoldTradePartners(playerOrID)
##     Returns a list of CyPlayers that can trade gold with <player>.
##
##   getMapTradePartners(playerOrID)
##     Returns a list of CyPlayers that can trade maps with <player>.
##
##
##   getOpenBordersTradePartners(playerOrID)
##     Returns a list of CyPlayers that can sign an Open Borders agreement with <player>.
##
##   getDefensivePactTradePartners(playerOrID)
##     Returns a list of CyPlayers that can sign a Defensive Pact with <player>.
##
##   getPermanentAllianceTradePartners(playerOrID)
##     Returns a list of CyPlayers that can sign a Permanent Alliance with <player>.
##
##
##   getPeaceTradePartners(playerOrID)
##     Returns a list of CyPlayers that can sign a peace treaty with <player>.
##
##   getVassalTradePartners(playerOrID)
##     Returns a list of CyPlayers that can become a vassal of <player>.
##
##   getCapitulationTradePartners(playerOrID)
##     Returns a list of CyPlayers that can capitulate to <player>.
##
##
##   tradeParters(playerOrID)
##     Iterates over all of <player>'s possible trade partners, yielding each CyPlayer in turn.
##
##   getTradePartnersByPlayer(playerOrID, testFunction, args...)
##     Returns a list of CyPlayers that can trade with <player>.
##
##   getTradePartnersByTeam(playerOrID, testFunction, args...)
##     Returns a list of CyPlayers that can trade with <player>.
##
## Trade Items
##
##   getDesiredBonuses(playerOrID)
##     Returns a set of bonus IDs that <player> can receive in trade.
##
##   getCorporationBonuses(playerOrID)
##     Returns the set of bonus IDs that <player> can receive due to their corporations.
##
##   getSurplusBonuses(playerOrID, minimum=1
##     Returns a list of bonus IDs of which <player> has at least <minimum>.
##
##   getTradeableBonuses(fromPlayerOrID, toPlayerOrID)
##     Returns two sets of bonus IDs that <fromPlayer> will and won't trade to <toPlayer>.
##
## Trade Routes
##
##   isFractionalTrade()
##     Returns True of BULL is active with Fractional Trade Routes.
##
##   getTradeProfitFunc()
##     Returns the CyCity function to use to calculate the trade route profit for a single route.
##
##   calculateTradeRouteYield(city, route, yieldType)
##     Returns the total <yieldType> for the <route>th trade route in <city>.
##
##   calculateTotalTradeRouteYield(city, yieldType)
##     Returns the total <yieldType> for all trade routes in <city>.
##
##   calculateTradeRoutes(playerOrID, withPlayerOrID=None)
##     Returns the domestic and foreign trade route yields and counts for <playerOrID>:
##     domestic yield, domestic count, foreign yield, and foreign count.
##     If <withPlayerOrID> is given, only counts trade routes to their cities.
##
## TradeData
##
##   format(player or ID, TradeData(s))
##     Returns a plain text description of the given tradeable item(s).
##
##   Trade(ePlayer, eOtherPlayer)
##     Can be used to create new trades.
##     (not really since implementDeal() not exposed to Python)
##
## Notes
##   - Must be initialized externally by calling init()
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugUtil
import DiplomacyUtil
import GameUtil
import PlayerUtil

# BUG - Mac Support - start
BugUtil.fixSets(globals())
# BUG - Mac Support - end

gc = CyGlobalContext()

CORP_BONUSES = {}

DOMESTIC_TRADE = 0
DOMESTIC_OVERSEAS_TRADE = 1
FOREIGN_TRADE = 2
FOREIGN_OVERSEAS_TRADE = 3

MAX_TRADE_ROUTES = gc.getDefineINT("MAX_TRADE_ROUTES")
FRACTIONAL_TRADE = False
TRADE_PROFIT_FUNC = None

TRADE_FORMATS = {}


## Trading Partners

def canTrade(playerOrID, withPlayerOrID):
	"""
	Returns True if <player> can open the trade window with <withPlayer>.
	"""
	return DiplomacyUtil.canContact(playerOrID, withPlayerOrID) and DiplomacyUtil.isWillingToTalk(withPlayerOrID, playerOrID)

def getTechTradePartners(playerOrID):
	"""
	Returns a list of CyPlayers that can trade technologies with <player>.
	"""
	if not GameUtil.isTechTrading():
		return ()
	return getTradePartnersByTeam(playerOrID, lambda fromTeam, toTeam: fromTeam.isTechTrading() or toTeam.isTechTrading())

def getBonusTradePartners(playerOrID):
	"""
	Returns a list of CyPlayers that can trade bonuses with <player>.
	"""
	return getTradePartnersByPlayer(playerOrID, lambda fromPlayer, toPlayer: fromPlayer.canTradeNetworkWith(toPlayer.getID()))

def getGoldTradePartners(playerOrID):
	"""
	Returns a list of CyPlayers that can trade gold with <player>.
	"""
	return getTradePartnersByTeam(playerOrID, lambda fromTeam, toTeam: fromTeam.isGoldTrading() or toTeam.isGoldTrading())

def getMapTradePartners(playerOrID):
	"""
	Returns a list of CyPlayers that can trade maps with <player>.
	"""
	return getTradePartnersByTeam(playerOrID, lambda fromTeam, toTeam: fromTeam.isMapTrading() or toTeam.isMapTrading())


def getOpenBordersTradePartners(playerOrID):
	"""
	Returns a list of CyPlayers that can sign an Open Borders agreement with <player>.
	"""
	return getTradePartnersByTeam(playerOrID, canSignOpenBorders)

def canSignOpenBorders(fromTeam, toTeam):
	"""
	Returns True if the two CyTeams can sign an Open Borders agreement.
	"""
	if fromTeam.isOpenBorders(toTeam.getID()) or toTeam.isOpenBorders(fromTeam.getID()):
		return False
	return fromTeam.isOpenBordersTrading() or toTeam.isOpenBordersTrading()

def getDefensivePactTradePartners(playerOrID):
	"""
	Returns a list of CyPlayers that can sign a Defensive Pact with <player>.
	"""
	return getTradePartnersByTeam(playerOrID, canSignDefensivePact)

def canSignDefensivePact(fromTeam, toTeam):
	"""
	Returns True if the two CyTeams can sign a Defensive Pact.
	"""
	if fromTeam.isDefensivePact(toTeam.getID()) or toTeam.isDefensivePact(fromTeam.getID()):
		return False
	return fromTeam.isDefensivePactTrading() or toTeam.isDefensivePactTrading()

def getPermanentAllianceTradePartners(playerOrID):
	"""
	Returns a list of CyPlayers that can sign a Permanent Alliance with <player>.
	"""
	return getTradePartnersByTeam(playerOrID, canSignPermanentAlliance)

def canSignPermanentAlliance(fromTeam, toTeam):
	"""
	Returns True if the two CyTeams can sign a Permanent Alliance.
	"""
	if fromTeam.getID() == toTeam.getID():
		return False
	return fromTeam.isPermanentAllianceTrading() or toTeam.isPermanentAllianceTrading()


def getPeaceTradePartners(playerOrID):
	"""
	Returns a list of CyPlayers that can sign a peace treaty with <player>.
	"""
	return getTradePartnersByTeam(playerOrID, lambda fromTeam, toTeam: toTeam.isAtWar(fromTeam.getID()))

def getVassalTradePartners(playerOrID):
	"""
	Returns a list of CyPlayers that can become a vassal of <player>.
	"""
	return getTradePartnersByTeam(playerOrID, canAcceptVassal, False)

def getCapitulationTradePartners(playerOrID):
	"""
	Returns a list of CyPlayers that can capitulate to <player>.
	"""
	return getTradePartnersByTeam(playerOrID, canAcceptVassal, True)

def canAcceptVassal(masterTeam, vassalTeam, bAtWar):
	"""
	Returns True if <vassalTeam> can become a vassal of <masterTeam>.
	
	Pass True for <bAtWar> to test for capitulation and False to test for peaceful vassalage.
	"""
	if masterTeam.getID() == vassalTeam.getID():
		return False
	if masterTeam.isAVassal() or vassalTeam.isAVassal():
		return False
	if masterTeam.isAtWar(vassalTeam.getID()) != bAtWar:
		return False
	# master must possess tech
	return masterTeam.isVassalStateTrading()


def tradeParters(playerOrID):
	"""
	Iterates over all of <player>'s possible trade partners, yielding each CyPlayer in turn.
	"""
	player = PlayerUtil.getPlayer(playerOrID)
	for partner in PlayerUtil.players(alive=True, barbarian=False, minor=False):
		if canTrade(player, partner):
			yield partner

def getTradePartnersByPlayer(playerOrID, testFunction, *args):
	"""
	Returns a list of CyPlayers that can trade with <player>.
	
	<testFunction> is passed two CyPlayers plus <args> for each viable pairing and should return a boolean value.
	"""
	player = PlayerUtil.getPlayer(playerOrID)
	partners = []
	for partner in tradeParters(player):
		if testFunction(player, partner, *args):
			partners.append(partner)
	return partners

def getTradePartnersByTeam(playerOrID, testFunction, *args):
	"""
	Returns a list of CyPlayers that can trade with <player>.
	
	<testFunction> is passed two CyTeams plus <args> for each viable pairing and should return a boolean value.
	"""
	player = PlayerUtil.getPlayer(playerOrID)
	team = PlayerUtil.getTeam(player.getTeam())
	partners = []
	for partner in tradeParters(player):
		if testFunction(team, PlayerUtil.getTeam(partner.getTeam()), *args):
			partners.append(partner)
	return partners


## Trade Items

def getDesiredBonuses(playerOrID):
	"""
	Returns a set of bonus IDs that <player> can receive in trade.
	"""
	player, team = PlayerUtil.getPlayerAndTeam(playerOrID)
	bonuses = set()
	for eBonus in range(gc.getNumBonusInfos()):
		if player.getNumAvailableBonuses(eBonus) == 0:
			eObsoleteTech = gc.getBonusInfo(eBonus).getTechObsolete()
			if eObsoleteTech == -1 or not team.isHasTech(eObsoleteTech):
				bonuses.add(eBonus)
	return bonuses | getCorporationBonuses(player)

def getCorporationBonuses(playerOrID):
	"""
	Returns the set of bonus IDs that <player> can receive due to their corporations.
	
	Takes into account anything (e.g. civics) that alters <player>'s ability to run corporations.
	"""
	player = PlayerUtil.getPlayer(playerOrID)
	bonuses = set()
	for eCorp, inputs in CORP_BONUSES.iteritems():
		if player.getHasCorporationCount(eCorp) > 0:
			bonuses |= inputs
	return bonuses

def initCorporationBonuses():
	"""
	Initializes the CORP_BONUSES dictionary that maps each corporation ID to the set of bonus IDs it uses.
	"""
	for eCorp in range(gc.getNumCorporationInfos()):
		corp = gc.getCorporationInfo(eCorp)
		bonuses = set()
		for i in range(gc.getNUM_CORPORATION_PREREQ_BONUSES()):
			eBonus = corp.getPrereqBonus(i)
			if eBonus != -1:
				bonuses.add(eBonus)
		CORP_BONUSES[eCorp] = bonuses

def getSurplusBonuses(playerOrID, minimum=1):
	"""
	Returns a list of bonus IDs of which <player> has at least <minimum> available to export.
	"""
	player = PlayerUtil.getPlayer(playerOrID)
	available = []
	for eBonus in range(gc.getNumBonusInfos()):
		if player.getNumTradeableBonuses(eBonus) >= minimum:
			available.append(eBonus)
	return available

def getTradeableBonuses(fromPlayerOrID, toPlayerOrID):
	"""
	Returns two sets of bonus IDs that <fromPlayer> will and won't trade to <toPlayer>.
	
	Assumes that the two players can trade bonuses.
	"""
	fromPlayer = PlayerUtil.getPlayer(fromPlayerOrID)
	eToPlayer = PlayerUtil.getPlayerID(toPlayerOrID)
	fromPlayerIsHuman = fromPlayer.isHuman()
	will = set()
	wont = set()
	tradeData = TradeData()
	tradeData.ItemType = TradeableItems.TRADE_RESOURCES
	for eBonus in range(gc.getNumBonusInfos()):
		tradeData.iData = eBonus
		if fromPlayer.canTradeItem(eToPlayer, tradeData, False):
			if fromPlayerIsHuman or fromPlayer.canTradeItem(eToPlayer, tradeData, True):
				will.add(eBonus)
			else:
				wont.add(eBonus)
	return will, wont


## Trade Routes

def isFractionalTrade():
	"""
	Returns True of BULL is active with Fractional Trade Routes.
	"""
	return FRACTIONAL_TRADE

def getTradeProfitFunc():
	"""
	Returns the CyCity function to use to calculate the trade route profit for a single route.
	"""
	return TRADE_PROFIT_FUNC

def calculateTradeRouteYield(city, route, yieldType):
	"""
	Returns the total <yieldType> for the <route>th trade route in <city>.
	
	If Fractional Trade Routes is active, the value returned is fractional (times 100).
	"""
	return city.calculateTradeYield(yieldType, TRADE_PROFIT_FUNC(city, city.getTradeCity(route)))

def calculateTotalTradeRouteYield(city, yieldType):
	"""
	Returns the total <yieldType> for all trade routes in <city>.
	
	If Fractional Trade Routes is active, the total is rounded down and returned as a regular number.
	"""
	trade = 0
	for route in range(city.getTradeRoutes()):
		trade += calculateTradeRouteYield(city, route, yieldType)
	if isFractionalTrade():
		trade /= 100
	return trade
		
	return city.calculateTradeYield(yieldType, TRADE_PROFIT_FUNC(city, city.getTradeCity(route)))

def calculateTradeRoutes(playerOrID, withPlayerOrID=None):
	"""
	Returns the domestic and foreign trade route yields and counts for <playerOrID>:
	domestic yield, domestic count, foreign yield, and foreign count.
	
	If <withPlayerOrID> is given, only counts trade routes to their cities.
	If Fractional Trade Routes is active, the value returned is fractional (times 100).
	"""
	domesticTrade = domesticCount = foreignTrade = foreignCount = 0
	eTeam = PlayerUtil.getPlayerTeam(playerOrID)
	eWithPlayer = PlayerUtil.getPlayerID(withPlayerOrID)
	for city in PlayerUtil.playerCities(playerOrID):
		for i in range(city.getTradeRoutes()):
			tradeCity = city.getTradeCity(i)
			if tradeCity and tradeCity.getOwner() >= 0 and (eWithPlayer == -1 or eWithPlayer == tradeCity.getOwner()):
				trade = city.calculateTradeYield(YieldTypes.YIELD_COMMERCE, TRADE_PROFIT_FUNC(city, tradeCity))
				if tradeCity.getTeam() == eTeam:
					domesticTrade += trade
					domesticCount += 1
				else:
					foreignTrade += trade
					foreignCount += 1
	return domesticTrade, domesticCount, foreignTrade, foreignCount

def initFractionalTrade():
	"""
	Sets the global fractional trade constants by testing for the function it adds.
	
	Fractional Trade is an optional compile-time feature of BULL.
	"""
	global FRACTIONAL_TRADE, TRADE_PROFIT_FUNC
	try:
		TRADE_PROFIT_FUNC = CyCity.calculateTradeProfitTimes100
		FRACTIONAL_TRADE = True
		BugUtil.debug("TradeUtil - Fractional Trade Routes is active")
	except:
		TRADE_PROFIT_FUNC = CyCity.calculateTradeProfit
		FRACTIONAL_TRADE = False


## Trade Class

class Trade(object):
	"""
	Encapsulates the player IDs and TradeData for a new or proposed trade.
	
	Implements the same interface as the DealUtil.Deal class.
	"""
	def __init__(self, ePlayer, eOtherPlayer):
		self.ePlayer = ePlayer
		self.eOtherPlayer = eOtherPlayer
		self.tradeList = []
		self.otherTradeList = []
	
	def isReversed(self):
		return False
	def getPlayer(self):
		return self.ePlayer
	def getOtherPlayer(self):
		return self.eOtherPlayer
	
	def getCount(self):
		return len(self.tradeList)
	def getOtherCount(self):
		return len(self.otherTradeList)
	def getTrade(self, index):
		return self.tradeList[index]
	def getOtherTrade(self, index):
		return self.otherTradeList[index]
	def trades(self):
		return self.tradeList
	def otherTrades(self):
		return self.otherTradeList
	
	def addTrade(self, trade):
		self.tradeList.append(trade)
	def addOtherTrade(self, trade):
		self.otherTradeList.append(trade)
	
	def hasType(self, type):
		return self.hasAnyType((type,))
	def hasAnyType(self, types):
		for trade in self.trades():
			if trade.ItemType in types:
				return True
		for trade in self.otherTrades():
			if trade.ItemType in types:
				return True
		return False
	def findType(self, type):
		return self.findTypes((type,))
	def findTypes(self, types):
		found = []
		for trade in self.trades():
			for type in types:
				if type == trade.ItemType:
					found.append(trade)
		for trade in self.otherTrades():
			for type in types:
				if type == trade.ItemType:
					found.append(trade)
		return found
	
	def __repr__(self):
		return ("<trade %d [%s] for %d [%s]>" % 
				(self.getPlayer(), 
				format(self.getPlayer(), self.trades()), 
				self.getOtherPlayer(), 
				format(self.getOtherPlayer(), self.otherTrades())))


## TradeData Formatting

def format(player, trade):
	"""Returns a single string containing all of the trade items separated by commas.
	
	player can be either an ID or CyPlayer and is needed when a city is being traded.
	"""
	if isinstance(trade, list) or isinstance(trade, tuple) or isinstance(trade, set):
		return ", ".join([format(player, t) for t in trade])
	elif trade.ItemType in TRADE_FORMATS:
		return TRADE_FORMATS[trade.ItemType].format(player, trade)
	else:
		BugUtil.warn("TradeUtil - unknown item type %d", trade.ItemType)
		return ""

def initTradeableItems():
	addSimpleTrade("gold", TradeableItems.TRADE_GOLD, "TXT_KEY_TRADE_GOLD_NUM")
	addSimpleTrade("gold per turn", TradeableItems.TRADE_GOLD_PER_TURN, "TXT_KEY_TRADE_GOLD_PER_TURN_NUM")
	addPlainTrade("map", TradeableItems.TRADE_MAPS, "TXT_KEY_TRADE_WORLD_MAP_STRING")
	addPlainTrade("vassal", TradeableItems.TRADE_VASSAL, "TXT_KEY_TRADE_VASSAL_TREATY_STRING")
	addPlainTrade("capitulation", TradeableItems.TRADE_SURRENDER, "TXT_KEY_TRADE_CAPITULATE_STRING")
	addPlainTrade("open borders", TradeableItems.TRADE_OPEN_BORDERS, "TXT_KEY_TRADE_OPEN_BORDERS_STRING")
	addPlainTrade("defensive pact", TradeableItems.TRADE_DEFENSIVE_PACT, "TXT_KEY_TRADE_DEFENSIVE_PACT_STRING")
	addPlainTrade("alliance", TradeableItems.TRADE_PERMANENT_ALLIANCE, "TXT_KEY_TRADE_PERMANENT_ALLIANCE_STRING")
	addComplexTrade("peace treaty", TradeableItems.TRADE_PEACE_TREATY, getTradePeaceDeal)
	addComplexTrade("technology", TradeableItems.TRADE_TECHNOLOGIES, getTradeTech)
	addComplexTrade("resource", TradeableItems.TRADE_RESOURCES, getTradeBonus)
	addComplexTrade("city", TradeableItems.TRADE_CITIES, getTradeCity)
	addAppendingTrade("peace", TradeableItems.TRADE_PEACE, "TXT_KEY_TRADE_PEACE_WITH", getTradePlayer)
	addAppendingTrade("war", TradeableItems.TRADE_WAR, "TXT_KEY_TRADE_WAR_WITH", getTradePlayer)
	addAppendingTrade("trade embargo", TradeableItems.TRADE_EMBARGO, "TXT_KEY_TRADE_STOP_TRADING_WITH", getTradePlayer, " %s")
	addAppendingTrade("civic", TradeableItems.TRADE_CIVIC, "TXT_KEY_TRADE_ADOPT", getTradeCivic)
	addAppendingTrade("religion", TradeableItems.TRADE_RELIGION, "TXT_KEY_TRADE_CONVERT", getTradeReligion)

def addPlainTrade(name, type, key):
	"""Creates a trade using an unparameterized XML <text> tag."""
	return addTrade(type, PlainTradeFormat(name, type, key))

def addSimpleTrade(name, type, key):
	"""Creates a trade using an XML <text> tag with a int placeholder for iData."""
	return addTrade(type, SimpleTradeFormat(name, type, key))

def addAppendingTrade(name, type, key, argsFunction, text="%s"):
	"""Creates a trade using an XML <text> tag with a single appended string placeholder."""
	format = addTrade(type, AppendingTradeFormat(name, type, key, text))
	if argsFunction is not None:
		format.getParameters = lambda player, trade: argsFunction(player, trade)
	return format

def addComplexTrade(name, type, argsFunction, textFunction=None):
	"""Creates a trade using an XML <text> tag with any number of placeholders."""
	format = addTrade(type, ComplexTradeFormat(name, type))
	if argsFunction is not None:
		format.getParameters = lambda player, trade: argsFunction(player, trade)
	if textFunction is not None:
		format.getText = lambda player, trade: textFunction(player, trade)
	return format

def addTrade(type, format):
	TRADE_FORMATS[type] = format
	return format


## Functions for use as argsFunction: converting TradeData.iData into
## whatever you want to display in the formatted string.

def getTradeTech(player, trade):
	return gc.getTechInfo(trade.iData).getDescription()

def getTradeBonus(player, trade):
	return gc.getBonusInfo(trade.iData).getDescription()

def getTradeCity(player, trade):
	return PlayerUtil.getPlayer(player).getCity(trade.iData).getName()

def getTradeCivic(player, trade):
	return gc.getCivicInfo(trade.iData).getDescription()

def getTradeReligion(player, trade):
	return gc.getReligionInfo(trade.iData).getDescription()

def getTradePlayer(player, trade):
	return PlayerUtil.getPlayer(trade.iData).getName()

def getTradePeaceDeal(player, trade):
	BugUtil.debug("TradeUtil - peace treaty has iData %d", trade.iData)
	return BugUtil.getText("TXT_KEY_TRADE_PEACE_TREATY_STRING", (gc.getDefineINT("PEACE_TREATY_LENGTH"),))


## Classes for Formatting TradeData

class BaseTradeFormat(object):
	def __init__(self, name, type):
		self.name = name
		self.type = type
	def format(self, player, trade):
		pass

class PlainTradeFormat(BaseTradeFormat):
	def __init__(self, name, type, key):
		super(PlainTradeFormat, self).__init__(name, type)
		self.key = key
	def format(self, player, trade):
		return BugUtil.getPlainText(self.key)

class SimpleTradeFormat(BaseTradeFormat):
	def __init__(self, name, type, key):
		super(SimpleTradeFormat, self).__init__(name, type)
		self.key = key
	def format(self, player, trade):
		return BugUtil.getText(self.key, (self.getParameters(player, trade),))
	def getParameters(self, player, trade):
		return trade.iData

class AppendingTradeFormat(BaseTradeFormat):
	def __init__(self, name, type, key, text="%s"):
		super(AppendingTradeFormat, self).__init__(name, type)
		self.key = key
		self.text = text
	def format(self, player, trade):
		return self.getText(player, trade) % (self.getParameters(player, trade),)
	def getText(self, player, trade):
		return BugUtil.getPlainText(self.key) + self.text
	def getParameters(self, player, trade):
		return trade.iData

class ComplexTradeFormat(BaseTradeFormat):
	def __init__(self, name, type):
		super(ComplexTradeFormat, self).__init__(name, type)
	def format(self, player, trade):
		return self.getText(player, trade) % (self.getParameters(player, trade),)
	def getText(self, player, trade):
		return "%s"
	def getParameters(self, player, trade):
		return trade.iData


## Initialization

def init():
	"""
	Performs one-time initialization after the game starts up.
	"""
	initCorporationBonuses()
	initFractionalTrade()
	initTradeableItems()


## Testing

def makeTrade(type, value=-1):
	trade = TradeData()
	trade.ItemType = TradeableItems(type)
	if value != -1:
		trade.iData = value
	return trade

def test(player, type, value):
	print format(player, makeTrade(type, value))

def testAll():
	for i in TRADE_FORMATS.keys():
		test(2, i, 1)

def testList():
	print format(2, [
		makeTrade(TradeableItems.TRADE_GOLD, 53),
		makeTrade(TradeableItems.TRADE_MAPS),
		makeTrade(TradeableItems.TRADE_PEACE, 1),
		makeTrade(TradeableItems.TRADE_CITY, 1),
		makeTrade(TradeableItems.TRADE_GOLD_PER_TURN, 6),
	])

STATUS_TRADE_ITEMS = (
	(TradeableItems.TRADE_MAPS, "Map"),
	(TradeableItems.TRADE_VASSAL, "Vassal"),
	(TradeableItems.TRADE_SURRENDER, "Surrender"),
	(TradeableItems.TRADE_OPEN_BORDERS, "Borders"),
	(TradeableItems.TRADE_DEFENSIVE_PACT, "Pact"),
	(TradeableItems.TRADE_PERMANENT_ALLIANCE, "Alliance"),
	(TradeableItems.TRADE_PEACE_TREATY, "Peace"),
)
DENIALS = {
	DenialTypes.NO_DENIAL : "None",
	DenialTypes.DENIAL_UNKNOWN : "Unknown",
	DenialTypes.DENIAL_NEVER : "Never",
	DenialTypes.DENIAL_TOO_MUCH : "Too Much",
	DenialTypes.DENIAL_MYSTERY : "Mystery",
	DenialTypes.DENIAL_JOKING : "Joking",
	DenialTypes.DENIAL_ANGER_CIVIC : "Anger Civic",
	DenialTypes.DENIAL_FAVORITE_CIVIC : "Favorite Civic",
	DenialTypes.DENIAL_MINORITY_RELIGION : "Minority Religion",
	DenialTypes.DENIAL_CONTACT_THEM : "Contact Them",
	DenialTypes.DENIAL_VICTORY : "Victory",
	DenialTypes.DENIAL_ATTITUDE : "Attitude",
	DenialTypes.DENIAL_ATTITUDE_THEM : "Attitude Them",
	DenialTypes.DENIAL_TECH_WHORE : "Tech Whore",
	DenialTypes.DENIAL_TECH_MONOPOLY : "Tech Monopoly",
	DenialTypes.DENIAL_POWER_US : "Power Us",
	DenialTypes.DENIAL_POWER_YOU : "Power You",
	DenialTypes.DENIAL_POWER_THEM : "Power Them",
	DenialTypes.DENIAL_TOO_MANY_WARS : "WHEOOH",
	DenialTypes.DENIAL_NO_GAIN : "No Gain",
	DenialTypes.DENIAL_NOT_ALLIED : "Not Allied",
	DenialTypes.DENIAL_RECENT_CANCEL : "Recent Cancel",
	DenialTypes.DENIAL_WORST_ENEMY : "Worst Enemy",
	DenialTypes.DENIAL_POWER_YOUR_ENEMIES : "Power Your Enemies",
	DenialTypes.DENIAL_TOO_FAR : "Too Far",
	# these aren't available during startup (dunno about later)
	#DenialTypes.DENIAL_VASSAL : "Vassal",
	#DenialTypes.DENIAL_WAR_NOT_POSSIBLE_US : "War Not Possible Us",
	#DenialTypes.DENIAL_WAR_NOT_POSSIBLE_THEM : "War Not Possible Them",
	#DenialTypes.DENIAL_PEACE_NOT_POSSIBLE_US : "Peace Not Possible Us",
	#DenialTypes.DENIAL_PEACE_NOT_POSSIBLE_THEM : "Peace Not Possible Them",
}

def printStatus(ePlayer, eAskingPlayer=None):
	player = PlayerUtil.getPlayer(ePlayer)
	if eAskingPlayer is None:
		eAskingPlayer = PlayerUtil.getActivePlayerID()
	print "Trade Status -- %s" % player.getName()
	for eItem, name in STATUS_TRADE_ITEMS:
		tradeData = TradeData()
		tradeData.ItemType = eItem
		can = player.canTradeItem(eAskingPlayer, tradeData, False)
		denial = player.getTradeDenial(eAskingPlayer, tradeData)
		will = denial == DenialTypes.NO_DENIAL
		if denial in DENIALS:
			denial = DENIALS[denial]
		else:
			denial = str(denial)
		if not can:
			if will:
				print "%s: can't but will" % (name)
			else:
				print "%s: can't and won't because %s" % (name, denial)
		else:
			if will:
				print "%s: will" % (name)
			else:
				print "%s: won't because %s" % (name, denial)
