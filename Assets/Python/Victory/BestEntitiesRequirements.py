from Core import *
from VictoryTypes import *
from BaseRequirements import *


# Second Orthodox URV goal
class BestCultureCities(BestCitiesRequirement):

	TYPES = (COUNT,)

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_BEST_CULTURE_CITIES"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BEST_CULTURE"
	
	def metric(self, city):
		return city.getCulture(city.getOwner())


# Third Babylonian UHV goal
# Second Byzantine UHV goal
class BestCultureCity(BestCityRequirement):

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_MAKE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_BEST_CULTURE_CITY"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BEST_CULTURE"
	
	def metric(self, city):
		return city.getCulture(city.getOwner())
	

# Third Hindu URV goal
class BestPopulationCities(BestCitiesRequirement):

	TYPES = (COUNT,)

	DESC_KEY = "TXT_KEY_VICTORY_DESC_BEST_POPULATION_CITIES"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BEST_POPULATION"
	
	def metric(self, city):
		return city.getPopulation()


# Second Babylonian UHV goal
# Second Byzantine UHV goal
# First Aztec UHV goal
# Second Thai UHV goal
# Third Mexican UHV goal
class BestPopulationCity(BestCityRequirement):

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_MAKE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_BEST_POPULATION_CITY"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BEST_POPULATION"
	
	def metric(self, city):
		return city.getPopulation()
	

# First Indonesian UHV goal
class BestPopulationPlayer(BestPlayersRequirement):

	DESC_KEY = "TXT_KEY_VICTORY_DESC_BEST_POPULATION_PLAYER"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BEST_POPULATION"
	
	def metric(self, iPlayer):
		return player(iPlayer).getRealPopulation()


# First Arabian UHV goal
class BestTechPlayer(BestPlayersRequirement):

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_BE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_BEST_TECH_PLAYER"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BEST_TECH"
	
	def __init__(self, *parameters, **options):
		BestPlayersRequirement.__init__(self, *parameters, **options)
		
		self.checked("techAcquired")
	
	def metric(self, iPlayer):
		return infos.techs().where(team(iPlayer).isHasTech).sum(lambda iTech: infos.tech(iTech).getResearchCost())


# Third Secular URV goal
class BestTechPlayers(BestPlayersRequirement):

	TYPES = (COUNT,)

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_MAKE_SURE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_BEST_TECH_PLAYERS"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BEST_TECH"
	
	def __init__(self, iRequired, subject=SELF, **options):
		BestPlayersRequirement.__init__(self, iRequired, **options)
		
		self.iRequired = iRequired
		self.subject = subject
	
		self.checked("techAcquired")
	
	def description(self):
		return text(self.DESC_KEY, COUNT.format(self.iRequired), self.subject.name.lower())
	
	def metric(self, iPlayer):
		return infos.techs().where(team(iPlayer).isHasTech).sum(lambda iTech: infos.tech(iTech).getResearchCost())
