from Core import *
from VictoryTypes import *
from BaseRequirements import *


# Second French UHV goal
class AreaPercent(PercentRequirement):

	TYPES = (AREA, PERCENTAGE)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_AREA_PERCENT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_AREA_PERCENT"
	
	def __init__(self, area, *parameters, **options):
		PercentRequirement.__init__(self, area, *parameters, **options)
		
		self.area = area
		
	def value(self, iPlayer, area):
		return area.create().land().owner(iPlayer).count()
	
	def total(self):
		return self.area.create().land().count()


# Third Inca UHV goal
class AreaPopulationPercent(PercentRequirement):

	TYPES = (AREA, PERCENTAGE)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_AREA_POPULATION_PERCENT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_AREA_POPULATION_PERCENT"
	
	def __init__(self, area, *parameters, **options):
		PercentRequirement.__init__(self, area, *parameters, **options)
		
		self.area = area
	
	def value(self, iPlayer, area):
		return area.create().cities().owner(iPlayer).sum(CyCity.getPopulation)
	
	def total(self):
		return self.area.create().cities().sum(CyCity.getPopulation)


# First Persian UHV goal
# First Turkic UHV goal
class LandPercent(PercentRequirement):

	TYPES = (PERCENTAGE,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_LAND_PERCENT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_LAND_PERCENT"
	
	def value(self, iPlayer):
		return player(iPlayer).getTotalLand()
	
	def total(self):
		return map.getLandPlots()


# Third Indian UHV goal
# Third Indonesian UHV goal
class PopulationPercent(PercentRequirement):

	TYPES = (PERCENTAGE,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_POPULATION_PERCENT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_POPULATION_PERCENT"
	
	def value(self, iPlayer):
		return cities.owner(iPlayer).sum(CyCity.getPopulation)
	
	def total(self):
		return game.getTotalPopulation()


# Third Arabian UHV goal
# Second Tibetan UHV goal
# Third Spanish UHV goal
class ReligionSpreadPercent(PercentRequirement):

	TYPES = (RELIGION, PERCENTAGE)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_SPREAD"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_RELIGION_SPREAD_PERCENT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_RELIGION_SPREAD_PERCENT"
	
	def __init__(self, iReligion, *parameters, **options):
		PercentRequirement.__init__(self, iReligion, *parameters, **options)
		
		self.iReligion = iReligion
	
	def percentage(self, evaluator):
		return game.calculateReligionPercent(self.iReligion)
		
