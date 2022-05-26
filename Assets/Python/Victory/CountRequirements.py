from Core import *
from VictoryTypes import *
from BaseRequirements import *


# Second Harappan UHV goal
# First Chinese UHV goal
# First Indian UHV goal
# Second Indian UHV goal
# Second Persian UHV goal
# Third Persian UHV goal
# First Roman UHV goal
class BuildingCount(ThresholdRequirement):

	TYPES = (BUILDING, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_COUNT"
	
	def __init__(self, iBuilding, *args, **options):
		ThresholdRequirement.__init__(self, iBuilding, *args, **options)
		
		self.iBuilding = iBuilding
		
		self.handle("cityAcquired", self.check)
		self.handle("buildingBuilt", self.check_building_built)
	
	def check_building_built(self, goal, city, iBuilding):
		if base_building(iBuilding) == self.iBuilding:
			goal.check()
	
	def value(self, iPlayer, iBuilding):
		return player(iPlayer).countNumBuildings(unique_building(iPlayer, iBuilding))
	
	def is_plural(self):
		return self.required() > 1
		
	def description(self):
		return Requirement.description(self, bPlural=self.is_plural())
		
	def progress(self, evaluator):
		if not self.is_plural():
			return BUILDING.format(self.iBuilding)
		
		return "%s %s: %s" % (self.indicator(evaluator), text(self.PROGR_KEY, BUILDING.format(self.iBuilding, bPlural=True)), self.progress_value(evaluator))


# Second Roman UHV goal
class CityCount(ThresholdRequirement):

	TYPES = (AREA, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CITY_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CITY_COUNT"
	
	def __init__(self, area, *args, **options):
		ThresholdRequirement.__init__(self, area, *args, **options)
		
		self.area = area
		
		self.handle("cityBuilt", self.check)
		self.handle("cityAcquiredAndKept", self.check)
		
	def value(self, iPlayer, area):
		return area.cities().owner(iPlayer).count()


# Third Harappan UHV goal
class PopulationCount(ThresholdRequirement):

	TYPES = (COUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_POPULATION"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_POPULATION"
	
	def value(self, iPlayer):
		return player(iPlayer).getTotalPopulation()
	

