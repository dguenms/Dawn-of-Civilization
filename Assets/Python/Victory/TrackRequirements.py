from Core import *
from VictoryTypes import *
from BaseRequirements import *
		

class BrokeredPeace(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_BROKERED_PEACE"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BROKERED_PEACE"

	def __init__(self, *args, **options):
		TrackRequirement.__init__(self, *args, **options)
		
		self.incremented("peaceBrokered")


# Third Chinese UHV goal
class GoldenAges(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_EXPERIENCE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_GOLDEN_AGES"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_GOLDEN_AGES"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, iRequired, **options)
		
		self.iRequired = scale(infos.constant("GOLDEN_AGE_LENGTH") * iRequired)
		
		self.handle("BeginPlayerTurn", self.increment_golden_ages)
	
	def increment_golden_ages(self, goal, *args):
		if goal.evaluator.any(lambda iPlayer: player(iPlayer).isGoldenAge() and not player(iPlayer).isAnarchy()):
			self.increment()
			goal.check()
	
	def progress_value(self, evaluator):
		iGoldenAgeLength = infos.constant("GOLDEN_AGE_LENGTH")
		return "%d / %d" % (self.evaluate(evaluator) / iGoldenAgeLength, self.required() / iGoldenAgeLength)


# Third Tamil UHV goal
class TradeGold(TrackRequirement):

	TYPES = (AMOUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_TRADE_GOLD"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_TRADE_GOLD"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, iRequired, **options)
		
		self.iRequired = scale(iRequired)
		
		self.handle("playerGoldTrade", self.accumulate_trade_gold)
		self.handle("tradeMission", self.accumulate_trade_mission_gold)
		self.handle("BeginPlayerTurn", self.accumulate_trade_deal_gold)
		self.handle("BeginPlayerTurn", self.accumulate_trade_route_gold)
	
	def accumulate_trade_gold(self, goal, iGold):
		self.accumulate(iGold * 100)
		goal.check()
	
	def accumulate_trade_mission_gold(self, goal, tile, iGold):
		self.accumulate(iGold * 100)
		goal.check()
	
	def accumulate_trade_deal_gold(self, goal, iGameTurn, iPlayer):
		iGold = players.major().alive().sum(lambda p: player(iPlayer).getGoldPerTurnByPlayer(p))
		self.accumulate(iGold * 100)
		goal.check()
	
	def accumulate_trade_route_gold(self, goal, iGameTurn, iPlayer):
		iGold = cities.owner(iPlayer).sum(lambda city: city.getTradeYield(YieldTypes.YIELD_COMMERCE)) * player(iPlayer).getCommercePercent(CommerceTypes.COMMERCE_GOLD)
		self.accumulate(iGold)
		goal.check()

	def evaluate(self, evaluator):
		return self.iValue / 100
	
