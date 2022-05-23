from Core import *
from VictoryTypes import *
from BaseRequirements import *
	

# First Babylonian UHV goal
# Second Chinese UHV goal
# First Greek UHV goal
class FirstDiscover(StateRequirement):

	TYPES = (TECH,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_FIRST_DISCOVER"
	
	def __init__(self, iTech, **options):
		StateRequirement.__init__(self, iTech, **options)
		
		self.iTech = iTech
		
		self.handle("techAcquired", self.check_first_discovered)
		self.expire("techAcquired", self.expire_first_discovered)
	
	def check_first_discovered(self, goal, iTech):
		if self.iTech == iTech and game.countKnownTechNumTeams(iTech) == 1:
			self.succeed()
			goal.check()
	
	def expire_first_discovered(self, goal, iTech):
		if self.iTech == iTech and self.state == POSSIBLE:
			self.fail()
			goal.expire()
