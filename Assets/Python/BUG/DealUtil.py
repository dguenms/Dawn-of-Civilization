## DealUtil
##
## Utilities for dealing with Deals.
##
##   Deal(CvDeal), ReversedDeal(CvDeal)
##     Wrapper classes that provide a nicer interface than CvDeal.
##     The reversed form makes the second player the primary player.
##
##   playerDeals(ePlayer)
##     Iterates over all deals for <ePlayer>, returning Deal objects where <ePlayer>
##     is always the primary player.
##
##   findDealsByPlayerAndType(ePlayer, type(s))
##     Returns a data structure holding the Deals for <ePlayer> that match the types.
##     This should only be used with symmetrically tradeable types like open borders.
##
## * New events
##
##   - DealCanceled
##       Fired when a player cancels a deal
##
## Notes
##   - Must be initialized externally by calling init()
##   - Add 'gameUpdate' event for onGameUpdate()
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugDll
import PlayerUtil
import TradeUtil


## Constants

GOLD_TRADE_ITEMS = (TradeableItems.TRADE_GOLD, TradeableItems.TRADE_GOLD_PER_TURN)
VASSAL_TRADE_ITEMS = (TradeableItems.TRADE_VASSAL, TradeableItems.TRADE_SURRENDER)


## Globals

gc = CyGlobalContext()

g_eventManager = None
g_lastDealCount = 0


## Deal Functions

def playerDeals(ePlayer):
	"""Generates an iterator of all PlayerDeals in which ePlayer takes part.
	
	PlayerDeal.getPlayer() always returns ePlayer.
	
	# print all open borders deals for active player
	ePlayer = gc.getGame().getActivePlayer()
	for deal in TradeUtil.playerDeals(ePlayer):
		if deal.hasType(TradeableItems.TRADE_OPEN_BORDERS):
			print deal
	"""
	if ePlayer is not None and ePlayer != -1:
		game = gc.getGame()
		for i in range(game.getIndexAfterLastDeal()):
			deal = game.getDeal(i)
			if not deal.isNone():
				if deal.getFirstPlayer() == ePlayer:
					yield Deal(deal)
				if deal.getSecondPlayer() == ePlayer:
					yield ReversedDeal(deal)

def findDealsByPlayerAndType(ePlayer, types):
	"""Returns PlayerDeals in which ePlayer takes part and that match
	one of the given types.
	
	This function only works with symmetric TradeableItem types (OB, DP, PA, PT).
	The returned dictionary maps each unique player ID to a dictionary that
	maps TradeableItem (from types) to PlayerDeal. Only players with at least
	one matching deal get added to the dictionary.
	
	Each deal can be mapped to multiple types, but each type will have at most
	one deal mapped to it per player. This is because you cannot trade open borders
	to the same player in two or more deals.
	"""
	if isinstance(types, int):
		types = (types,)
	found = {}
	for deal in playerDeals(ePlayer):
		matches = deal.findTypes(types)
		for type in matches:
			found.setdefault(deal.getOtherPlayer(), {})[type] = deal
	return found


## TradeableItem Functions

def isAnnual(eItem):
	return eItem in (
		TradeableItems.TRADE_RESOURCES, 
		TradeableItems.TRADE_GOLD_PER_TURN, 
		TradeableItems.TRADE_VASSAL, 
		TradeableItems.TRADE_SURRENDER, 
		TradeableItems.TRADE_OPEN_BORDERS, 
		TradeableItems.TRADE_DEFENSIVE_PACT, 
		TradeableItems.TRADE_PERMANENT_ALLIANCE, 
	)

def isDual(eItem, bExcludePeace=False):
	if bExcludePeace and eItem == TradeableItems.TRADE_PEACE_TREATY:
		return False
	return eItem in (
		TradeableItems.TRADE_OPEN_BORDERS, 
		TradeableItems.TRADE_DEFENSIVE_PACT, 
		TradeableItems.TRADE_PERMANENT_ALLIANCE, 
		TradeableItems.TRADE_PEACE_TREATY, 
	)

def hasData(eItem):
	return eItem not in (
		TradeableItems.TRADE_MAPS, 
		TradeableItems.TRADE_VASSAL, 
		TradeableItems.TRADE_SURRENDER, 
		TradeableItems.TRADE_OPEN_BORDERS, 
		TradeableItems.TRADE_DEFENSIVE_PACT, 
		TradeableItems.TRADE_PERMANENT_ALLIANCE, 
		TradeableItems.TRADE_PEACE_TREATY, 
	)

def isGold(eItem):
	return eItem in GOLD_TRADE_ITEMS

def isVassal(eItem):
	return eItem in VASSAL_TRADE_ITEMS

def isEndWar(eItem):
	return eItem == TradeableItems.TRADE_PEACE_TREATY or isVassal(eItem)


## Initialization and Events

def addEvents(eventManager):
	"""Defines a new 'DealCanceled' event."""
	global g_eventManager
	g_eventManager = eventManager
	g_eventManager.addEvent("DealCanceled")
	g_eventManager.addEventHandler("gameUpdate", onGameUpdate)

def onGameUpdate(argsList):
	"""
	Fires 'DealCanceled' event during update event if the number of deals
	is less than it was during the previous call.
	"""
	global g_lastDealCount
	count = gc.getGame().getNumDeals()
	if count < g_lastDealCount:
		g_lastDealCount = count
		g_eventManager.fireEvent("DealCanceled", -1, -1, None)
	else:
		g_lastDealCount = count


## Wrapper Classes

class Deal(object):
	"""Wraps a CyDeal where either the first or second player is the focus.
	
	All CyDeal functions are provided either directly or mapped to basic and
	'Other' versions. In the main class, the basic functions map to the 'First'
	functions and the 'Other' functions map to 'Second' functions. This is reversed
	in the ReversedDeal subclass.
	
	For example, normally getCount() returns getLengthFirstTrades() and
	getOtherCount() returns getLengthSecondTrades(). The same method applies to
	getPlayer() and getTrade().
	
	hasType() and hasAnyType() search only the focused player's TradeData.ItemType,
	so they work only for symmetric TradeableItems (peace treaty, open borders, 
	and defensive pact).
	"""
	def __init__(self, deal):
		self.deal = deal
	def getID(self):
		return self.deal.getID()
	def isNone(self):
		return self.deal.isNone()
	def getInitialGameTurn(self):
		return self.deal.getInitialGameTurn()
	
	def isCancelable(self, eByPlayer, bIgnoreWaitingPeriod=False):
		if BugDll.isPresent():
			return self.deal.isCancelable(eByPlayer, bIgnoreWaitingPeriod)
		else:
			if self.isUncancelableVassalDeal(eByPlayer):
				return False
			return self.turnsToCancel(eByPlayer) <= 0
	def getCannotCancelReason(self, eByPlayer):
		if BugDll.isPresent():
			return self.deal.getCannotCancelReason(eByPlayer)
		else:
			return ""
	def turnsToCancel(self, eByPlayer=-1):
		if BugDll.isPresent():
			return self.deal.turnsToCancel(eByPlayer)
		else:
			# this is exactly what CvDeal does
			return self.getInitialGameTurn() + gc.getDefineINT("PEACE_TREATY_LENGTH") - gc.getGame().getGameTurn()
	def kill(self):
		self.deal.kill()
	
	def isPeaceDeal(self):
		return self.eitherHasType(TradeableItems.TRADE_PEACE_TREATY)
	def isVassalDeal(self):
		return self.eitherHasAnyType(VASSAL_TRADE_ITEMS)
	def isUncancelableVassalDeal(self, eByPlayer):
		"""
		Note: Doesn't check if a surrendered vassal is not allowed to revolt.
		"""
		return ((eByPlayer == self.getOtherPlayer() and self.hasAnyType(VASSAL_TRADE_ITEMS)) or
				(eByPlayer == self.getPlayer() and self.otherHasAnyType(VASSAL_TRADE_ITEMS)))
	
	def isReversed(self):
		return False
	def getPlayer(self):
		return self.deal.getFirstPlayer()
	def getOtherPlayer(self):
		return self.deal.getSecondPlayer()
	def getCount(self):
		return self.deal.getLengthFirstTrades()
	def getOtherCount(self):
		return self.deal.getLengthSecondTrades()
	def getTrade(self, index):
		return self.deal.getFirstTrade(index)
	def getOtherTrade(self, index):
		return self.deal.getSecondTrade(index)
	
	def trades(self):
		for i in range(self.getCount()):
			yield self.getTrade(i)
	def otherTrades(self):
		for i in range(self.getOtherCount()):
			yield self.getOtherTrade(i)
	def hasType(self, type):
		return self.hasAnyType((type,))
	def hasAnyType(self, types):
		for trade in self.trades():
			if trade.ItemType in types:
				return True
		return False
	def findTypes(self, types):
		found = []
		for trade in self.trades():
			for type in types:
				if type == trade.ItemType:
					found.append(type)
		return found
	
	def __repr__(self):
		return ("<deal %d [trades %d %s] [trades %d %s]>" % 
				(self.getID(), 
				self.getPlayer(), 
				TradeUtil.format(self.getPlayer(), [t for t in self.trades()]), 
				self.getOtherPlayer(), 
				TradeUtil.format(self.getOtherPlayer(), [t for t in self.otherTrades()])))

class ReversedDeal(Deal):
	"""A Deal where the basic and 'Other' functions are reversed."""
	def __init__(self, deal):
		super(ReversedDeal, self).__init__(deal)
	def isReversed(self):
		return True
	def getPlayer(self):
		return self.deal.getSecondPlayer()
	def getOtherPlayer(self):
		return self.deal.getFirstPlayer()
	def getCount(self):
		return self.deal.getLengthSecondTrades()
	def getOtherCount(self):
		return self.deal.getLengthFirstTrades()
	def getTrade(self, index):
		return self.deal.getSecondTrade(index)
	def getOtherTrade(self, index):
		return self.deal.getFirstTrade(index)


## Testing

def test():
	allDeals = findDealsByPlayerAndType(0, 
			(
				TradeableItems.TRADE_PEACE_TREATY,
				TradeableItems.TRADE_OPEN_BORDERS,
				TradeableItems.TRADE_DEFENSIVE_PACT,
				TradeableItems.TRADE_RESOURCES,
				TradeableItems.TRADE_GOLD_PER_TURN,
			))
	for player, deals in allDeals.iteritems():
		print PlayerUtil.getPlayer(player).getName()
		for type, deal in deals.iteritems():
			print "%s: %r" % (TradeUtil.TRADE_FORMATS[type].name, deal)
