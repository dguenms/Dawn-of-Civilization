from Core import *
from VictoryTypes import *
from BaseRequirements import *
		

class BrokeredPeace(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_BROKERED_PEACE"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BROKERED_PEACE"

	def __init__(self, *args, **options):
		TrackRequirement.__init__(self, *args, **options)
		
		self.incremented("peaceBrokered")


# Third Chinese UHV goal
class GoldenAges(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_EXPERIENCE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_GOLDEN_AGES"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_GOLDEN_AGES"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, iRequired, **options)
		
		self.iRequired = scale(infos.constant("GOLDEN_AGE_LENGTH") * iRequired)
		
		self.handle("BeginPlayerTurn", self.increment_golden_ages)
	
	def increment_golden_ages(self, goal, *args):
		if goal.evaluator.any(lambda iPlayer: player(iPlayer).isGoldenAge() and not player(iPlayer).isAnarchy()):
			self.increment()
			goal.check()
	
	def progress_value(self, evaluator):
		iGoldenAgeLength = infos.constant("GOLDEN_AGE_LENGTH")
		return "%d / %d" % (self.evaluate(evaluator) / iGoldenAgeLength, self.required() / iGoldenAgeLength)
	
