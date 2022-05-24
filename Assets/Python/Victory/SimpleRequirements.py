from Core import *
from VictoryTypes import *
from BaseRequirements import *


# First Phoenician UHV goal
class CityBuilding(Requirement):

	GLOBAL_TYPES = (CITY,)
	TYPES = (BUILDING,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_BUILD"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CITY_BUILDING"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CITY_BUILDING"
	
	def __init__(self, city, iBuilding, **options):
		Requirement.__init__(self, city, iBuilding, **options)
		
		self.city = city
		self.iBuilding = iBuilding
		
		self.handle("cityAcquired", self.check_city_acquired)
		self.handle("buildingBuilt", self.check_building_built)
		self.expire("buildingBuilt", self.expire_building_built)
	
	def check_city_acquired(self, goal, city, bConquest):
		if self.city == city:
			goal.check()
	
	def check_building_built(self, goal, city, iBuilding):
		if self.city == city and self.iBuilding == base_building(iBuilding):
			goal.check()
	
	def expire_building_built(self, goal, city, iBuilding):
		if self.iBuilding == iBuilding and isWonder(iBuilding):
			goal.expire()
	
	def fulfilled(self, evaluator):
		if not self.city:
			return False
		
		return self.city.getOwner() in evaluator and self.city.isHasBuilding(unique_building(self.city.getOwner(), self.iBuilding))
	

# Second Greek UHV goal
# Second Phoenician UHV goal
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