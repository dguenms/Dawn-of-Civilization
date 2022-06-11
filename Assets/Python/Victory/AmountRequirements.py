from Core import *
from VictoryTypes import *
from BaseRequirements import *


# First Japanese UHV goal
class AverageCultureAmount(ThresholdRequirement):

	TYPES = (AMOUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_AVERAGE_CULTURE"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_AVERAGE_CULTURE"
	
	def __init__(self, iRequired, **options):
		ThresholdRequirement.__init__(self, scale(iRequired), **options)
		
		self.iRequired = scale(iRequired)
	
	def value(self, iPlayer):
		iNumCities = player(iPlayer).getNumCities()
		if iNumCities == 0:
			return 0
		
		return player(iPlayer).countTotalCulture() / iNumCities


# First Egyption UHV goal
# Third Egyptian UHV goal
# First Tamil UHV goal
# Third Khmer UHV goal
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
# First Byzantine UHV goal
# Third Mandinka UHV goal
class GoldAmount(ThresholdRequirement):

	TYPES = (AMOUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_GOLD_AMOUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_GOLD_AMOUNT"
	
	def value(self, iPlayer):
		return player(iPlayer).getGold()
	
	def required(self):
		return scale(self.iRequired)
