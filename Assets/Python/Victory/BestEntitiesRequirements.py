from Core import *
from VictoryTypes import *
from BaseRequirements import *
	
		
class BestPopulationPlayer(BestPlayersRequirement):

	DESC_KEY = "TXT_KEY_VICTORY_DESC_BEST_POPULATION_PLAYER"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BEST_POPULATION"
	
	def metric(self, iPlayer):
		return player(iPlayer).getRealPopulation()
	

class BestPopulationCities(BestCitiesRequirement):

	TYPES = (COUNT,)

	DESC_KEY = "TXT_KEY_VICTORY_DESC_BEST_POPULATION_CITIES"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BEST_POPULATION"
	
	def metric(self, city):
		return city.getPopulation()
