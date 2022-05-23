from Core import *
from VictoryTypes import *
from BaseRequirements import *
	

# Second Greek UHV goal
class Control(Requirement):
	
	TYPES = (AREA,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	
	def __init__(self, area, **options):
		Requirement.__init__(self, area, **options)
		
		self.area = area
	
	def fulfilled(self, evaluator):
		return self.area.cities().all_if_any(lambda city: city.getOwner() in evaluator)


# First Harappan UHV goal
class TradeConnection(Requirement):

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ESTABLISH"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_TRADE_CONNECTION"
	
	def fulfilled(self, evaluator):
		other_players = players.major().alive().without(evaluator.players())
		return evaluator.any(lambda iPlayer: other_players.any(lambda iOtherPlayer: player(iPlayer).canContact(iOtherPlayer) and player(iPlayer).canTradeNetworkWith(iOtherPlayer)))


# Second Egyptian UHV goal
# Third Greek UHV goal
class Wonder(Requirement):

	TYPES = (BUILDING,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_BUILD"
	
	def __init__(self, iBuilding, **options):
		Requirement.__init__(self, iBuilding, **options)
		
		self.iBuilding = iBuilding
		
		self.handle("buildingBuilt", self.check_building_built)
		self.expire("buildingBuilt", self.expire_building_built)
	
	def check_building_built(self, goal, city, iBuilding):
		if self.iBuilding == iBuilding:
			goal.check()
	
	def expire_building_built(self, goal, city, iBuilding):
		if self.iBuilding == iBuilding:
			goal.expire()
	
	def fulfilled(self, evaluator):
		return evaluator.any(lambda iPlayer: player(iPlayer).isHasBuilding(self.iBuilding))