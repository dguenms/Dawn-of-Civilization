from Core import *
from VictoryTypes import *
from BaseRequirements import *
	

class Control(Requirement):
	
	TYPES = (AREA,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	
	def __init__(self, area, **options):
		Requirement.__init__(self, area, **options)
		
		self.area = area
	
	def fulfilled(self, evaluator):
		return self.area.cities().all_if_any(lambda city: city.getOwner() in evaluator)


# Second Egyptian UHV goal
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