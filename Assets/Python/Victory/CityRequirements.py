from Core import *
from VictoryTypes import *
from BaseRequirements import *


# First Phoenician UHV goal
# First Ottoman UHV goal
# Third Brazilian UHV goal
# Second Confucian URV goal
class CityBuilding(CityRequirement):

	GLOBAL_TYPES = (CITY,)
	TYPES = (BUILDING,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_BUILD"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CITY_BUILDING"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CITY_BUILDING"
	
	def __init__(self, city, iBuilding, **options):
		CityRequirement.__init__(self, city, iBuilding, **options)
		
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
	
	def fulfilled_city(self, city):
		return city.isHasBuilding(unique_building(city.getOwner(), self.iBuilding))
	

# Third Turkic UHV goal
# First French UHV goal
# Second Argentine UHV goal
# Third Zoroastrian URV goal
# Second Jewish URV goal
# Third Taoist URV goal
class CityCultureLevel(CityRequirement):

	TYPES = (CITY, CULTURELEVEL)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CITY_CULTURE_LEVEL"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CITY_CULTURE_LEVEL"
	
	def __init__(self, city, iCultureLevel, **options):
		CityRequirement.__init__(self, city, iCultureLevel, **options)
		
		self.iCultureLevel = iCultureLevel
	
	def fulfilled_city(self, city):
		return city.getCultureLevel() >= self.iCultureLevel
	
	def progress_city(self, city):
		return "%d / %d" % (city.getCulture(city.getOwner()), game.getCultureThreshold(self.iCultureLevel))


# First Hindu URV goal
class CityDifferentGreatPeopleCount(CityRequirement):

	TYPES = (CITY, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_SETTLE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CITY_DIFFERENT_GREAT_PEOPLE_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CITY_DIFFERENT_GREAT_PEOPLE_COUNT"
	
	GREAT_PEOPLE = [
		iSpecialistGreatProphet, 
		iSpecialistGreatArtist, 
		iSpecialistGreatScientist, 
		iSpecialistGreatMerchant, 
		iSpecialistGreatEngineer,
		iSpecialistGreatStatesman, 
		iSpecialistGreatGeneral, 
		iSpecialistGreatSpy
	]
	
	def __init__(self, city, iRequired, **options):
		CityRequirement.__init__(self, city, iRequired, **options)
		
		self.iRequired = iRequired
	
	def different_great_people(self, city):
		return count(1 for iGreatSpecialist in self.GREAT_PEOPLE if city.getFreeSpecialistCount(iGreatSpecialist) > 0)
	
	def fulfilled_city(self, city):
		return self.different_great_people(city) >= self.iRequired
	
	def progress_city(self, city):
		return "%d / %d" % (self.different_great_people(city), self.iRequired)


# Third Tibetan UHV goal
# Second Moorish UHV goal
# Third Holy Roman UHV goal
# Second Mandinka UHV goal
# First Dutch UHV goal
# First German UHV goal
# Second Islamic URV goal
# Third Shinto URV goal
class CitySpecialistCount(CityRequirement):

	TYPES = (CITY, SPECIALIST, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_SETTLE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CITY_SPECIALIST_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CITY_SPECIALIST_COUNT"
	
	def __init__(self, city, iSpecialist, iRequired, **options):
		CityRequirement.__init__(self, city, iSpecialist, iRequired, **options)
		
		self.iSpecialist = iSpecialist
		self.iRequired = iRequired
		
		self.bPlural = self.iRequired > 1
		
	def fulfilled_city(self, city):
		return city.getFreeSpecialistCount(self.iSpecialist) >= self.iRequired
	
	def description(self):
		return CityRequirement.description(self, bPlural=self.bPlural)
	
	def progress_city(self, city):
		return "%d / %d" % (city.getFreeSpecialistCount(self.iSpecialist), self.iRequired)
		
	def progress_text(self, **options):
		return CityRequirement.progress_text(self, bPlural=self.bPlural)
