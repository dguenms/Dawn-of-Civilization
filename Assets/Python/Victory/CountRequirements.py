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
# Second Ethiopian UHV goal
# First Korean UHV goal
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
	
	def description(self):
		return Requirement.description(self, bPlural=self.bPlural)
		
	def progress(self, evaluator):
		if not self.bPlural:
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


# First Ethiopian UHV goal
class ResourceCount(ThresholdRequirement):

	TYPES = (RESOURCE, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_RESOURCE_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_RESOURCE_COUNT"
	
	def value(self, iPlayer, iResource):
		return player(iPlayer).getNumAvailableBonuses(iResource)


# Second Ethiopian UHV goal
class SpecialistCount(ThresholdRequirement):

	TYPES = (SPECIALIST, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_SETTLE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_SPECIALIST_COUNT"
	
	def __init__(self, iSpecialist, iRequired, **options):
		ThresholdRequirement.__init__(self, iSpecialist, iRequired, **options)
		
		self.iSpecialist = iSpecialist
	
	def value(self, iPlayer, iSpecialist):
		return cities.owner(iPlayer).sum(lambda city: city.getFreeSpecialistCount(iSpecialist))
	
	def description(self):
		return Requirement.description(self, bPlural=self.bPlural)
	
	def progress(self, evaluator):
		if not self.bPlural:
			return SPECIALIST.format(self.iSpecialist)
		
		return "%s %s: %s" % (self.indicator(evaluator), text(self.PROGR_KEY, SPECIALIST.format(self.iSpecialist, bPlural=True)), self.progress_value(evaluator))
	

