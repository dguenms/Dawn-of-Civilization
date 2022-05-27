from Core import *
from VictoryTypes import *
from BaseRequirements import *


# First Egyption UHV goal
# Third Egyptian UHV goal
# First Tamil UHV goal
class CultureAmount(ThresholdRequirement):

	TYPES = (AMOUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CULTURE_AMOUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CULTURE_AMOUNT"
	
	def value(self, iPlayer):
		return player(iPlayer).countTotalCulture()
	
	def required(self):
		return scale(self.iRequired)


# Third Phoenician UHV goal
# First Tamil UHV goal
class GoldAmount(ThresholdRequirement):

	TYPES = (AMOUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_GOLD_AMOUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_GOLD_AMOUNT"
	
	def value(self, iPlayer):
		return player(iPlayer).getGold()
	
	def required(self):
		return scale(self.iRequired)
