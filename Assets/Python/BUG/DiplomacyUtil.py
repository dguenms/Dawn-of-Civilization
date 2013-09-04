## DiplomacyUtil
##
## Utilities for handling and dispatching Diplomacy events and acquiring
## proposed trades from the (unmoddable) CyDiplomacy screen.
##
## Contacting Rivals
##
##   canContact(playerOrID, toPlayerOrID)
##     Returns True if <player> can attempt to contact <toPlayer> given game settings, 
##     initial contact, and war-time situation.
##
##   isWillingToTalk(playerOrID, toPlayerOrID)
##     Returns True if <player> is willing to talk to <toPlayer>.
##
## TODO: switch to init()
##
## Notes
##   - Must be initialized externally by calling addEvents(eventManager)
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import AttitudeUtil
import BugUtil
import BugDll
import GameUtil
import PlayerUtil
import TradeUtil

MAX_TRADE_DATA = 50  # avoid an infinite loop

gc = CyGlobalContext()
diplo = CyDiplomacy()

# comment-type -> ( event-type , trade-type )
g_eventsByCommentType = {}
g_eventManager = None


## Contacting Rivals

def canContact(playerOrID, toPlayerOrID):
	"""
	Returns True if <player> can attempt to contact <toPlayer> given game settings, 
	initial contact, and war-time situation without regard to willingness to talk.
	
	- They must not be the same player
	- <toPlayer> must be alive, not minor, and not a barbarian
	- Their teams must have met
	- If they are at war, they must be able to sign a peace deal (no Always War or Permanent War/Peace options)
	"""
	playerID, player = PlayerUtil.getPlayerAndID(playerOrID)
	toPlayerID, toPlayer = PlayerUtil.getPlayerAndID(toPlayerOrID)
	if playerID == toPlayerID:
		return False
	if not toPlayer.isAlive() or toPlayer.isBarbarian() or toPlayer.isMinorCiv():
		return False
	if not PlayerUtil.getPlayerTeam(player).isHasMet(toPlayer.getTeam()):
		return False
	if PlayerUtil.getPlayerTeam(player).isAtWar(toPlayer.getTeam()) and (GameUtil.isAlwaysWar() or GameUtil.isPermanentWarPeace()):
		return False
	return True

def isWillingToTalk(playerOrID, toPlayerOrID):
	"""
	Returns True if <player> is willing to talk to <toPlayer>.
	
	- Every player is willing to talk to themselves
	- All human players are willing to talk
	- Uses BUG DLL if present, otherwise scans attitude hover text
	  for "Refuses to Talk!!!" in the current language
	
	Note: This function does not check if the two players can make contact.
	"""
	playerID, player = PlayerUtil.getPlayerAndID(playerOrID)
	toPlayerID = PlayerUtil.getPlayerID(toPlayerOrID)
	if playerID == toPlayerID or player.isHuman():
		# all players talk to themselves, and all humans talk
		return True
	if BugDll.isPresent():
		return player.AI_isWillingToTalk(toPlayerID)
	else:
		hover = AttitudeUtil.getAttitudeString(playerID, toPlayerID)
		if hover:
			return (hover.find(BugUtil.getPlainText("TXT_KEY_MISC_REFUSES_TO_TALK")) == -1)
		else:
			# haven't met yet
			return False


## Event Initialization

def addEvents(eventManager):
	"""Adds the diplomacy events to BugEventManager."""
	global g_eventManager
	g_eventManager = eventManager
	
	# Trade
	DiploEvent("AI_DIPLOCOMMENT_OFFER_DEAL", "DealOffered", onDealOffered, sendTrade=True)
	DiploEvent("AI_DIPLOCOMMENT_CANCEL_DEAL", "DealCanceled", onDealCanceled, sendTrade=True)
	DiploEvent("USER_DIPLOCOMMENT_ACCEPT_OFFER", "DealAccepted", onDealAccepted, sendTrade=True)
	DiploEvent("USER_DIPLOCOMMENT_REJECT_OFFER", "DealRejected", onDealRejected, sendTrade=True)
	
	# Free Stuff
	DiploEvent("AI_DIPLOCOMMENT_OFFER_CITY", "CityOffered", onCityOffered, tradeType=TradeableItems.TRADE_CITIES)
	DiploEvent("AI_DIPLOCOMMENT_GIVE_HELP", "HelpOffered", onHelpOffered, sendTrade=True)
	DiploEvent("AI_DIPLOCOMMENT_OFFER_PEACE", "PeaceOffered", onPeaceOffered)
	DiploEvent("AI_DIPLOCOMMENT_OFFER_VASSAL", "VassalOffered", onVassalOffered)
	
	# Ask for Help
	DiploEvent("AI_DIPLOCOMMENT_ASK_FOR_HELP", "HelpDemanded", onHelpDemanded, sendTrade=True)
	DiploEvent("USER_DIPLOCOMMENT_GIVE_HELP", "HelpAccepted", onHelpAccepted, sendTrade=True)
	DiploEvent("USER_DIPLOCOMMENT_REFUSE_HELP", "HelpRejected", onHelpRejected, sendTrade=True)
	
	# Demand Tribute
	DiploEvent("AI_DIPLOCOMMENT_DEMAND_TRIBUTE", "TributeDemanded", onTributeDemanded, sendTrade=True)
	DiploEvent("USER_DIPLOCOMMENT_ACCEPT_DEMAND", "TributeAccepted", onTributeAccepted, sendTrade=True)
	DiploEvent("USER_DIPLOCOMMENT_REJECT_DEMAND", "TributeRejected", onTributeRejected, sendTrade=True)
	
	# Religion
	DiploEvent("AI_DIPLOCOMMENT_RELIGION_PRESSURE", "ReligionDemanded", onReligionDemanded, 
			argFunc=lambda eFromPlayer, eToPlayer, args, data: (PlayerUtil.getStateReligion(eFromPlayer), ))
	DiploEvent("USER_DIPLOCOMMENT_CONVERT", "ReligionAccepted", onReligionAccepted,
			argFunc=lambda eFromPlayer, eToPlayer, args, data: (PlayerUtil.getStateReligion(eToPlayer), ))
	DiploEvent("USER_DIPLOCOMMENT_NO_CONVERT", "ReligionRejected", onReligionRejected,
			argFunc=lambda eFromPlayer, eToPlayer, args, data: (PlayerUtil.getStateReligion(eToPlayer), ))
	
	# Civic
	DiploEvent("AI_DIPLOCOMMENT_CIVIC_PRESSURE", "CivicDemanded", onCivicDemanded, 
			argFunc=lambda eFromPlayer, eToPlayer, args, data: (PlayerUtil.getFavoriteCivic(eFromPlayer), ))
	DiploEvent("USER_DIPLOCOMMENT_REVOLUTION", "CivicAccepted", onCivicAccepted, 
			argFunc=lambda eFromPlayer, eToPlayer, args, data: (PlayerUtil.getFavoriteCivic(eToPlayer), ))
	DiploEvent("USER_DIPLOCOMMENT_NO_REVOLUTION", "CivicRejected", onCivicRejected, 
			argFunc=lambda eFromPlayer, eToPlayer, args, data: (PlayerUtil.getFavoriteCivic(eToPlayer), ))
	
	# Join War
	DiploEvent("AI_DIPLOCOMMENT_JOIN_WAR", "WarDemanded", onWarDemanded, sendData=True)
	DiploEvent("USER_DIPLOCOMMENT_JOIN_WAR", "WarAccepted", onWarAccepted, sendData=True)
	DiploEvent("USER_DIPLOCOMMENT_NO_JOIN_WAR", "WarRejected", onWarRejected, sendData=True)
	
	# Trade Embargo
	DiploEvent("AI_DIPLOCOMMENT_STOP_TRADING", "EmbargoDemanded", onEmbargoDemanded, sendData=True)
	DiploEvent("USER_DIPLOCOMMENT_STOP_TRADING", "EmbargoAccepted", onEmbargoAccepted, sendData=True)
	DiploEvent("USER_DIPLOCOMMENT_NO_STOP_TRADING", "EmbargoRejected", onEmbargoRejected, sendData=True)


class DiploEvent:
	def __init__(self, comment, event, handler=None, 
				 sendFromPlayer=True, sendToPlayer=True, 
				 sendData=False, sendArgs=False, argFunc=None, 
				 sendTrade=False, tradeType=None):
		self.comment = comment
		self.eComment = gc.getInfoTypeForString(comment)
		if self.eComment == -1:
			raise BugUtil.ConfigError("invalid comment type %s" % comment)
		self.event = event
		self.sendFromPlayer = sendFromPlayer
		self.sendToPlayer = sendToPlayer
		self.sendData = sendData
		self.sendArgs = sendArgs
		self.argFunc = argFunc
		self.sendTrade = sendTrade
		self.tradeType = tradeType
		if tradeType:
			BugUtil.debug("DiplomacyUtil - mapped %s to %s with %s", 
					comment, event, str(tradeType))
		else:
			BugUtil.debug("DiplomacyUtil - mapped %s to %s", comment, event)
		g_eventsByCommentType[self.eComment] = self
		g_eventManager.addEventHandler(event, handler)
	
	def dispatch(self, eFromPlayer, eToPlayer, args):
		data = diplo.getData()
		BugUtil.debug("DiplomacyUtil - %s [%d] from %d to %d with %r",
				self.comment, data, eFromPlayer, eToPlayer, args)
		argList = []
		if self.sendFromPlayer:
			argList.append(eFromPlayer)
		if self.sendToPlayer:
			argList.append(eToPlayer)
		
		if self.argFunc:
			argList.extend(self.argFunc(eFromPlayer, eToPlayer, args, data))
			BugUtil.debug("DiplomacyUtil - firing %s", self.event)
		else:
			if self.sendData:
				argList.append(data)
			if self.sendArgs:
				argList.append(args)
			
			if self.sendTrade or self.tradeType:
				trade = getProposedTrade()
				if self.sendTrade:
					argList.append(trade)
				if self.tradeType:
					trades = trade.findType(self.tradeType)
					if trade and trades:
						iData = trades[0].iData
						BugUtil.debug("DiplomacyUtil - firing %s with %s %d", 
								self.event, str(self.tradeType), iData)
						argList.append(iData)
					else:
						BugUtil.debug("DiplomacyUtil - firing %s without %s", 
								self.event, str(self.tradeType))
						argList.append(-1)
			else:
				BugUtil.debug("DiplomacyUtil - firing %s", self.event)
		g_eventManager.fireEvent(self.event, *argList)


## Event Dispatching

def handleAIComment(argsList):
	eComment = argsList[0]
	commentArgsSize = argsList[1]
	if commentArgsSize:
		args = argsList[2:]
	else:
		args=[]
	dispatchEvent(eComment, diplo.getWhoTradingWith(), 
			PlayerUtil.getActivePlayerID(), args)

def handleUserResponse(argsList):
	eComment = argsList[0]
	commentArgsSize = argsList[1]
	if commentArgsSize:
		args = argsList[2:]
	else:
		args=[]
	dispatchEvent(eComment, PlayerUtil.getActivePlayerID(), 
			diplo.getWhoTradingWith(), args)

def dispatchEvent(eComment, eFromPlayer, eToPlayer, args):
	event = g_eventsByCommentType.get(eComment, None)
	if event:
		event.dispatch(eFromPlayer, eToPlayer, args)
	else:
		key = gc.getDiplomacyInfo(eComment).getType()
		BugUtil.debug("DiplomacyUtil - ignoring %s from %d to %d with %r", 
				key, eFromPlayer, eToPlayer, args)


## Event Handlers

def onDealOffered(argsList):
	#BugUtil.debug("DiplomacyUtil::onDealOffered %s" %(str(argsList)))
	eOfferPlayer, eTargetPlayer, pTrade = argsList
	BugUtil.debug("DiplomacyUtil - %s offers trade to %s: %r",
			PlayerUtil.getPlayer(eOfferPlayer).getName(), 
			PlayerUtil.getPlayer(eTargetPlayer).getName(),
			pTrade)

def onCityOffered(argsList):
	#BugUtil.debug("DiplomacyUtil::onCityOffered %s" %(str(argsList)))
	eOfferPlayer, eTargetPlayer, pTrade = argsList
	BugUtil.debug("DiplomacyUtil - %s offers city to %s: %r",
			PlayerUtil.getPlayer(eOfferPlayer).getName(), 
			PlayerUtil.getPlayer(eTargetPlayer).getName(),
			pTrade)

def onHelpOffered(argsList):
	#BugUtil.debug("DiplomacyUtil::onHelpOffered %s" %(str(argsList)))
	eOfferPlayer, eTargetPlayer, pTrade = argsList
	BugUtil.debug("DiplomacyUtil - %s offers help to %s: %r",
			PlayerUtil.getPlayer(eOfferPlayer).getName(), 
			PlayerUtil.getPlayer(eTargetPlayer).getName(),
			pTrade)

def onPeaceOffered(argsList):
	#BugUtil.debug("DiplomacyUtil::onPeaceOffered %s" %(str(argsList)))
	eOfferPlayer, eTargetPlayer = argsList
	BugUtil.debug("DiplomacyUtil - %s offers peace to %s",
			PlayerUtil.getPlayer(eOfferPlayer).getName(), 
			PlayerUtil.getPlayer(eTargetPlayer).getName())

def onVassalOffered(argsList):
	#BugUtil.debug("DiplomacyUtil::onVassalOffered %s" %(str(argsList)))
	eOfferPlayer, eTargetPlayer = argsList
	BugUtil.debug("DiplomacyUtil - %s offers vassalage to %s",
			PlayerUtil.getPlayer(eOfferPlayer).getName(), 
			PlayerUtil.getPlayer(eTargetPlayer).getName())

def onDealCanceled(argsList):
	#BugUtil.debug("DiplomacyUtil::onDealCanceled %s" %(str(argsList)))
	eOfferPlayer, eTargetPlayer, pTrade = argsList
	if eOfferPlayer != -1 and eTargetPlayer != -1 and pTrade is not None:
		BugUtil.debug("DiplomacyUtil - %s cancels deal with %s: %r",
				PlayerUtil.getPlayer(eOfferPlayer).getName(), 
				PlayerUtil.getPlayer(eTargetPlayer).getName(),
				pTrade)

def onDealAccepted(argsList):
	#BugUtil.debug("DiplomacyUtil::onDealAccepted %s" %(str(argsList)))
	eTargetPlayer, eOfferPlayer, pTrade = argsList
	BugUtil.debug("DiplomacyUtil - %s accepts trade offered by %s: %r",
			PlayerUtil.getPlayer(eTargetPlayer).getName(),
			PlayerUtil.getPlayer(eOfferPlayer).getName(), 
			pTrade)

def onDealRejected(argsList):
	#BugUtil.debug("DiplomacyUtil::onDealRejected %s" %(str(argsList)))
	eTargetPlayer, eOfferPlayer, pTrade = argsList
	BugUtil.debug("DiplomacyUtil - %s accepts trade offered by %s: %r",
			PlayerUtil.getPlayer(eTargetPlayer).getName(),
			PlayerUtil.getPlayer(eOfferPlayer).getName(), 
			pTrade)


def onHelpDemanded(argsList):
	#BugUtil.debug("DiplomacyUtil::onHelpDemanded %s" %(str(argsList)))
	eDemandPlayer, eTargetPlayer, pTrade = argsList
	szItems = ""
	for i in range(pTrade.getCount()):
		szItems = szItems + TradeUtil.format(eTargetPlayer, pTrade.getTrade(i))
	BugUtil.debug("DiplomacyUtil - %s requests help (%s) from %s",
			PlayerUtil.getPlayer(eDemandPlayer).getName(), 
			szItems,
			PlayerUtil.getPlayer(eTargetPlayer).getName())

def onHelpAccepted(argsList):
	#BugUtil.debug("DiplomacyUtil::onHelpAccepted %s" %(str(argsList)))
	eTargetPlayer, eDemandPlayer, pTrade = argsList
	szItems = ""
	for i in range(pTrade.getCount()):
		szItems = szItems + TradeUtil.format(eTargetPlayer, pTrade.getTrade(i))
	BugUtil.debug("DiplomacyUtil - %s agrees to give help (%s) to %s",
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			szItems,
			PlayerUtil.getPlayer(eDemandPlayer).getName())

def onHelpRejected(argsList):
	#BugUtil.debug("DiplomacyUtil::onHelpRejected %s" %(str(argsList)))
	eTargetPlayer, eDemandPlayer, pTrade = argsList
	szItems = ""
	for i in range(pTrade.getCount()):
		szItems = szItems + TradeUtil.format(eTargetPlayer, pTrade.getTrade(i))
	BugUtil.debug("DiplomacyUtil - %s refuses to give help (%s) to %s",
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			szItems,
			PlayerUtil.getPlayer(eDemandPlayer).getName())


def onTributeDemanded(argsList):
	#BugUtil.debug("DiplomacyUtil::onTributeDemanded %s" %(str(argsList)))
	eDemandPlayer, eTargetPlayer, pTrade = argsList
	szItems = ""
	for i in range(pTrade.getCount()):
		szItems = szItems + TradeUtil.format(eTargetPlayer, pTrade.getTrade(i))
	BugUtil.debug("DiplomacyUtil - %s demands a tribute (%s) from %s",
			PlayerUtil.getPlayer(eDemandPlayer).getName(), 
			szItems,
			PlayerUtil.getPlayer(eTargetPlayer).getName())

def onTributeAccepted(argsList):
	#BugUtil.debug("DiplomacyUtil::onTributeAccepted %s" %(str(argsList)))
	eTargetPlayer, eDemandPlayer, pTrade = argsList
	szItems = ""
	for i in range(pTrade.getCount()):
		szItems = szItems + TradeUtil.format(eTargetPlayer, pTrade.getTrade(i))
	BugUtil.debug("DiplomacyUtil - %s agrees to give tribute (%s) to %s",
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			szItems,
			PlayerUtil.getPlayer(eDemandPlayer).getName())

def onTributeRejected(argsList):
	#BugUtil.debug("DiplomacyUtil::onTributeRejected %s" %(str(argsList)))
	eTargetPlayer, eDemandPlayer, pTrade = argsList
	szItems = ""
	for i in range(pTrade.getCount()):
		szItems = szItems + TradeUtil.format(eTargetPlayer, pTrade.getTrade(i))
	BugUtil.debug("DiplomacyUtil - %s refuses to give tribute (%s) to %s",
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			szItems,
			PlayerUtil.getPlayer(eDemandPlayer).getName())

def onReligionDemanded(argsList):
	#BugUtil.debug("DiplomacyUtil::onReligionDemanded %s" %(str(argsList)))
	eDemandPlayer, eTargetPlayer, eReligion = argsList
	BugUtil.debug("DiplomacyUtil - %s asks %s to convert to %s",
			PlayerUtil.getPlayer(eDemandPlayer).getName(), 
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			gc.getReligionInfo(eReligion).getDescription())

def onReligionAccepted(argsList):
	#BugUtil.debug("DiplomacyUtil::onReligionAccepted %s" %(str(argsList)))
	eTargetPlayer, eDemandPlayer, eReligion = argsList
	BugUtil.debug("DiplomacyUtil - %s accepts demand from %s to convert to %s",
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			PlayerUtil.getPlayer(eDemandPlayer).getName(), 
			gc.getReligionInfo(eReligion).getDescription())

def onReligionRejected(argsList):
	#BugUtil.debug("DiplomacyUtil::onReligionRejected %s" %(str(argsList)))
	eTargetPlayer, eDemandPlayer, eReligion = argsList
	BugUtil.debug("DiplomacyUtil - %s rejects demand from %s to convert to %s",
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			PlayerUtil.getPlayer(eDemandPlayer).getName(), 
			gc.getReligionInfo(eReligion).getDescription())


def onCivicDemanded(argsList):
	#BugUtil.debug("DiplomacyUtil::onCivicDemanded %s" %(str(argsList)))
	eDemandPlayer, eTargetPlayer, eCivic = argsList
	BugUtil.debug("DiplomacyUtil - %s asks %s to switch to %s",
			PlayerUtil.getPlayer(eDemandPlayer).getName(), 
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			gc.getCivicInfo(eCivic).getDescription())

def onCivicAccepted(argsList):
	#BugUtil.debug("DiplomacyUtil::onCivicAccepted %s" %(str(argsList)))
	eTargetPlayer, eDemandPlayer, eCivic = argsList
	BugUtil.debug("DiplomacyUtil - %s accepts demand from %s to switch to %s",
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			PlayerUtil.getPlayer(eDemandPlayer).getName(), 
			gc.getCivicInfo(eCivic).getDescription())

def onCivicRejected(argsList):
	#BugUtil.debug("DiplomacyUtil::onCivicRejected %s" %(str(argsList)))
	eTargetPlayer, eDemandPlayer, eCivic = argsList
	BugUtil.debug("DiplomacyUtil - %s rejects demand from %s to switch to %s",
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			PlayerUtil.getPlayer(eDemandPlayer).getName(), 
			gc.getCivicInfo(eCivic).getDescription())


def onWarDemanded(argsList):
	#BugUtil.debug("DiplomacyUtil::onWarDemanded %s" %(str(argsList)))
	eDemandPlayer, eTargetPlayer, eVictim = argsList
	BugUtil.debug("DiplomacyUtil - %s asks %s to declare war on %s",
			PlayerUtil.getPlayer(eDemandPlayer).getName(), 
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			PlayerUtil.getPlayer(eVictim).getName())

def onWarAccepted(argsList):
	#BugUtil.debug("DiplomacyUtil::onWarAccepted %s" %(str(argsList)))
	eTargetPlayer, eDemandPlayer, eVictim = argsList
	BugUtil.debug("DiplomacyUtil - %s agrees to demand from %s to declare war on %s",
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			PlayerUtil.getPlayer(eDemandPlayer).getName(), 
			PlayerUtil.getPlayer(eVictim).getName())

def onWarRejected(argsList):
	#BugUtil.debug("DiplomacyUtil::onWarRejected %s" %(str(argsList)))
	eTargetPlayer, eDemandPlayer, eVictim = argsList
	BugUtil.debug("DiplomacyUtil - %s rejects demand from %s to declare war on %s",
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			PlayerUtil.getPlayer(eDemandPlayer).getName(), 
			PlayerUtil.getPlayer(eVictim).getName())


def onEmbargoDemanded(argsList):
	#BugUtil.debug("DiplomacyUtil::onEmbargoDemanded %s" %(str(argsList)))
	eDemandPlayer, eTargetPlayer, eVictim = argsList
	BugUtil.debug("DiplomacyUtil - %s asks %s to stop trading with %s",
			PlayerUtil.getPlayer(eDemandPlayer).getName(), 
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			PlayerUtil.getPlayer(eVictim).getName())

def onEmbargoAccepted(argsList):
	#BugUtil.debug("DiplomacyUtil::onEmbargoAccepted %s" %(str(argsList)))
	eTargetPlayer, eDemandPlayer, eVictim = argsList
	BugUtil.debug("DiplomacyUtil - %s agrees to demand from %s to stop trading with %s",
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			PlayerUtil.getPlayer(eDemandPlayer).getName(), 
			PlayerUtil.getPlayer(eVictim).getName())

def onEmbargoRejected(argsList):
	#BugUtil.debug("DiplomacyUtil::onEmbargoRejected %s" %(str(argsList)))
	eTargetPlayer, eDemandPlayer, eVictim = argsList
	BugUtil.debug("DiplomacyUtil - %s rejects demand from %s to stop trading with %s",
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			PlayerUtil.getPlayer(eDemandPlayer).getName(), 
			PlayerUtil.getPlayer(eVictim).getName())


## Proposed Trade Functions

def getProposedTrade():
	trade = TradeUtil.Trade(PlayerUtil.getActivePlayerID(), diplo.getWhoTradingWith())
	if not diplo.ourOfferEmpty():
		getProposedTradeData(diplo.getPlayerTradeOffer, trade.addTrade)
	if not diplo.theirOfferEmpty():
		getProposedTradeData(diplo.getTheirTradeOffer, trade.addOtherTrade)
	BugUtil.debug("DiplomacyUtil.getProposedTrade - %r", trade)
	return trade

def getProposedTradeData(getFunc, addFunc):
	for index in range(MAX_TRADE_DATA):
		data = getFunc(index)
		if data:
			addFunc(data)
		else:
			break
	else:
		BugUtil.warn("DiplomacyUtil.getProposedTradeData - reached %d items, ignoring rest",
				MAX_TRADE_DATA)
