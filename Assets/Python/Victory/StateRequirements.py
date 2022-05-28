from Core import *
from VictoryTypes import *
from BaseRequirements import *


# Third Mayan UHV goal
class ContactBeforeRevealed(StateRequirement):

	TYPES = (CIVS, AREA)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTACT"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTACT_BEFORE_REVEALED"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CONTACT_BEFORE_REVEALED"
	
	def __init__(self, civs, area, **options):
		StateRequirement.__init__(self, civs, area, **options)
		
		self.civs = civs
		self.area = area
		
		self.handle("firstContact", self.check_contacted_before_revealed)
	
	def check_contacted_before_revealed(self, goal, iPlayer):
		if iPlayer in self.civs:
			if self.area.land().none(lambda plot: plot.isRevealed(iPlayer, False)):
				self.succeed()
			else:
				self.fail()
			
			goal.final_check()


# Second Ethiopian UHV goal
class ConvertAfterFounding(StateRequirement):

	TYPES = (RELIGION, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONVERT"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CONVERT_AFTER_FOUNDING"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CONVERT_AFTER_FOUNDING"
	
	def __init__(self, iReligion, iTurns, **options):
		StateRequirement.__init__(self, iReligion, scale(iTurns), **options)
		
		self.iReligion = iReligion
		self.iTurns = scale(iTurns)
		
		self.handle("playerChangeStateReligion", self.check_convert)
		
	def check_convert(self, goal, iReligion):
		if self.iReligion == iReligion and game.isReligionFounded(iReligion):
			if turn() <= game.getReligionGameTurnFounded(iReligion) + self.iTurns:
				self.succeed()
			else:
				self.fail()
			
			goal.final_check()


# First Mayan UHV goal
class Discover(StateRequirement):

	TYPES = (TECH,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_DISCOVER"
	
	def __init__(self, iTech, **options):
		StateRequirement.__init__(self, iTech, **options)
		
		self.iTech = iTech
		
		self.handle("techAcquired", self.check_discovered)
		
	def check_discovered(self, goal, iTech):
		if self.iTech == iTech:
			self.succeed()
			goal.check()
	

# First Babylonian UHV goal
# Second Chinese UHV goal
# First Greek UHV goal
# Third Roman UHV goal
# Second Korean UHV goal
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


# First Polynesian UHV goal
# Second Polynesian UHV goal
class Settle(StateRequirement):

	TYPES = (AREA,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_SETTLE"
	
	def __init__(self, area, **options):
		StateRequirement.__init__(self, area, **options)
		
		self.area = area
		
		self.handle("cityBuilt", self.check_settled)
		self.expire("cityBuilt", self.expire_settled)
		
	def check_settled(self, goal, city):
		if city in self.area and self.state == POSSIBLE:
			self.succeed()
			goal.check()
	
	def expire_settled(self, goal, city):
		if city in self.area and self.state == POSSIBLE:
			self.fail()
			goal.expire()
