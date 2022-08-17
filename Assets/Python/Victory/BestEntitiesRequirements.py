from Core import *
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

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_MAKE_CITY_WORLD"
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

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_MAKE_CITY_WORLD"
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


# Third Mugyo URV goal
class BestSpecialistCity(BestCityRequirement):

	TYPES = (SPECIALIST,)

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_MAKE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_BEST_SPECIALIST_CITY"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BEST_SPECIALIST"
	
	def __init__(self, city, iSpecialist, **options):
		BestCityRequirement.__init__(self, city, iSpecialist, **options)
		
		self.iSpecialist = iSpecialist
	
	def metric(self, city):
		return city.getFreeSpecialistCount(self.iSpecialist)


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
	
	def __init__(self, iRequired, **options):
		BestPlayersRequirement.__init__(self, iRequired, **options)
		
		self.iRequired = iRequired
	
		self.checked("techAcquired")
	
	def description(self):
		return text(self.DESC_KEY, COUNT.format(self.iRequired))
	
	def metric(self, iPlayer):
		return infos.techs().where(team(iPlayer).isHasTech).sum(lambda iTech: infos.tech(iTech).getResearchCost())


# Third Baalist URV goal
class BestTradeIncomeCity(BestCityRequirement):

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_MAKE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_BEST_TRADE_INCOME_CITY"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BEST_TRADE_INCOME"
	
	def metric(self, city):
		return city.getTradeYield(YieldTypes.YIELD_COMMERCE)


# Third Anunnaki URV goal
class BestWonderCity(BestCityRequirement):

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_MAKE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_BEST_WONDER_CITY"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BEST_WONDERS"
	
	def metric(self, city):
		return infos.buildings().count(lambda iBuilding: city.isHasRealBuilding(iBuilding) and isWonder(iBuilding))