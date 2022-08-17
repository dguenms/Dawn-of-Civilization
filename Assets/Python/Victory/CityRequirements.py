from Core import *
from BaseRequirements import *
	

# Third Turkic UHV goal
# First French UHV goal
# Second Argentine UHV goal
# Third Zoroastrian URV goal
# Second Jewish URV goal
# Third Taoist URV goal
class CityCultureLevel(CityRequirement):

	GLOBAL_TYPES = (CITY,)
	TYPES = (CULTURELEVEL,)
	
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
		
	def get_specialist_count(self, city):
		if isinstance(self.iSpecialist, Aggregate):
			return self.iSpecialist.evaluate(city.getFreeSpecialistCount)
		
		return city.getFreeSpecialistCount(self.iSpecialist)
		
	def fulfilled_city(self, city):
		return self.get_specialist_count(city) >= self.iRequired
	
	def description(self):
		return CityRequirement.description(self, bPlural=self.bPlural)
	
	def progress_city(self, city):
		return "%d / %d" % (self.get_specialist_count(city), self.iRequired)
		
	def progress_text(self, **options):
		return CityRequirement.progress_text(self, bPlural=self.bPlural)
