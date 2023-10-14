from Core import *
from BaseRequirements import *


# First Japanese UHV goal
class AverageCultureAmount(ThresholdRequirement):

	TYPES = (AMOUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_AVERAGE_CULTURE"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_AVERAGE_CULTURE"
	
	def __init__(self, iRequired, **options):
		ThresholdRequirement.__init__(self, iRequired, **options)
		
	def value(self, iPlayer):
		iNumCities = player(iPlayer).getNumCities()
		if iNumCities == 0:
			return 0
		
		return player(iPlayer).countTotalCulture() / iNumCities


# First Egyption UHV goal
# Third Egyptian UHV goal
# First Dravidian UHV goal
# Third Khmer UHV goal
# Third Mughal UHV goal
class CultureAmount(ThresholdRequirement):

	TYPES = (AMOUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CULTURE_AMOUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CULTURE_AMOUNT"
	
	def __init__(self, iRequired, **options):
		ThresholdRequirement.__init__(self, iRequired, **options)
	
	def value(self, iPlayer):
		return player(iPlayer).countTotalCulture()
	

# Third Phoenician UHV goal
# First Dravidian UHV goal
# First Byzantine UHV goal
# Third Mandinka UHV goal
# Second Inca UHV goal
class GoldAmount(ThresholdRequirement):

	TYPES = (AMOUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_GOLD_AMOUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_GOLD_AMOUNT"
	
	def __init__(self, iRequired, **options):
		ThresholdRequirement.__init__(self, iRequired, **options)
	
	def value(self, iPlayer):
		return player(iPlayer).getGold()
	

# Second Taoist URV goal
class ShrineIncome(ThresholdRequirement):

	TYPES = (RELIGION_ADJECTIVE, COUNT)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_SHRINE_INCOME"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_SHRINE_INCOME"
	
	def __init__(self, iReligion, iRequired, **options):
		ThresholdRequirement.__init__(self, iReligion, iRequired, **options)
	
	def value(self, iPlayer, iReligion):
		return cities.owner(iPlayer).sum(lambda city: city.getBuildingCommerceByBuilding(CommerceTypes.COMMERCE_GOLD, shrine(iReligion)))