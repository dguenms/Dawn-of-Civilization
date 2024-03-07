from Core import *
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

	TYPES = (RELIGION, TURNS)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONVERT"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CONVERT_AFTER_FOUNDING"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CONVERT_AFTER_FOUNDING"
	
	def __init__(self, iReligion, iTurns, **options):
		StateRequirement.__init__(self, iReligion, iTurns, **options)
		
		self.iReligion = iReligion
		self.iTurns = iTurns
		
		self.handle("playerChangeStateReligion", self.check_convert)
		self.handle("BeginPlayerTurn", self.check_expire)
		
	def check_convert(self, goal, iReligion):
		if self.iReligion == iReligion and game.isReligionFounded(iReligion):
			if turn() <= game.getReligionGameTurnFounded(iReligion) + scale(self.iTurns):
				self.succeed()
				goal.check()
	
	def check_expire(self, goal, iGameTurn, iPlayer):
		if game.isReligionFounded(self.iReligion) and self.state == POSSIBLE:
			if iGameTurn > game.getReligionGameTurnFounded(self.iReligion) + scale(self.iTurns):
				self.fail()
				goal.expire()


# First Mayan UHV goal
class Discover(StateRequirement):

	TYPES = (TECH,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_DISCOVER"
	
	def __init__(self, iTech, **options):
		StateRequirement.__init__(self, iTech, **options)
		
		self.iTech = iTech
		
		self.handle("techAcquired", self.check_discovered)
		
	def check_discovered(self, goal, iTech, iPlayer):
		if self.iTech == iTech:
			self.succeed()
			goal.check()


# Third Congolese UHV goal
class EnterEraBefore(StateRequirement):

	TYPES = (ERA, ERA)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ENTER"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_ENTER_ERA_BEFORE"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_ENTER_ERA_BEFORE"

	def __init__(self, iEra, iExpireEra, **options):
		StateRequirement.__init__(self, iEra, iExpireEra, **options)
		
		self.iEra = iEra
		self.iExpireEra = iExpireEra
		
		self.handle("techAcquired", self.check_enter_era)
		self.expire("techAcquired", self.expire_enter_era)
		
	def check_enter_era(self, goal, iTech, iPlayer):
		iEra = infos.tech(iTech).getEra()
		if self.iEra == iEra and self.state == POSSIBLE:
			self.succeed()
			goal.check()
	
	def expire_enter_era(self, goal, iTech, iPlayer):
		iEra = infos.tech(iTech).getEra()
		if self.iExpireEra == iEra and self.state == POSSIBLE:
			self.fail()
			goal.expire()
	

# First Babylonian UHV goal
# Second Chinese UHV goal
# First Greek UHV goal
# Third Roman UHV goal
# Second Korean UHV goal
# Second Polish UHV goal
# First Protestant URV goal
class FirstDiscover(StateRequirement):

	TYPES = (TECH,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_FIRST_DISCOVER"
	
	def __init__(self, iTech, **options):
		StateRequirement.__init__(self, iTech, **options)
		
		self.iTech = iTech
		
		self.handle("techAcquired", self.check_first_discovered)
		self.expire("techAcquired", self.expire_first_discovered)
	
	def init(self, goal):
		if game.countKnownTechNumTeams(self.iTech) > 0:
			goal.set_state(FAILURE)
	
	def check_first_discovered(self, goal, iTech, iPlayer):
		if self.iTech == iTech and game.countKnownTechNumTeams(iTech) == 1:
			self.succeed()
			goal.check()
	
	def expire_first_discovered(self, goal, iTech, iPlayer):
		if self.iTech == iTech and self.state == POSSIBLE:
			self.fail()
			goal.announce_failure_cause(iPlayer, "TXT_KEY_VICTORY_ANNOUNCE_FIRST_DISCOVER", TECH.format(iTech))
			goal.expire()	


# Third Pesedjet URV goal
class FirstGreatPerson(StateRequirement):

	TYPES = (UNIT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_FIRST_GREAT_PERSON"
	
	def __init__(self, iGreatPerson, **options):
		StateRequirement.__init__(self, iGreatPerson, **options)
		
		self.iGreatPerson = iGreatPerson
		
		self.handle("greatPersonBorn", self.check_great_person_born)
		self.expire("greatPersonBorn", self.expire_great_person_born)
	
	def specialist(self, unit):
		return next(iSpecialist for iSpecialist in infos.specialists() if infos.unit(unit).getGreatPeoples(iSpecialist))
	
	def check_great_person_born(self, goal, unit):
		if self.iGreatPerson == base_unit(unit) and self.state == POSSIBLE:
			self.succeed()
			goal.check()
	
	def expire_great_person_born(self, goal, unit):
		if self.iGreatPerson == base_unit(unit) and self.state == POSSIBLE:
			self.fail()
			
			if goal.possible():
				if goal.required < len(goal.requirements):
					if count(requirement.state != FAILURE for requirement in goal.requirements) < goal.required:
						goal.fail()

					return
			
				goal.announce_failure_cause(unit.getOwner(), "TXT_KEY_VICTORY_ANNOUNCE_FIRST_GREAT_PERSON", UNIT.format(unit.getUnitType()))
				goal.fail()


# Second Viking UHV goal
# First Spanish UHV goal
class FirstSettle(StateRequirement):

	TYPES = (AREA,)

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_FIRST_FOUND"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_FIRST_SETTLE"
	
	def __init__(self, area, allowed=[], **options):
		StateRequirement.__init__(self, area, allowed=allowed, **options)
		
		self.area = area
		self.allowed = allowed
		
		self.handle("cityBuilt", self.check_first_settled)
		self.expire("cityBuilt", self.expire_first_settled)
		
	def check_first_settled(self, goal, city):
		if city in self.area and self.state == POSSIBLE:
			self.succeed()
			goal.check()
	
	def expire_first_settled(self, goal, city):
		if city in self.area and self.state == POSSIBLE:
			if not is_minor(city) and city.getCivilizationType() not in self.allowed:
				self.fail()
				goal.announce_failure_cause(city.getOwner(), "TXT_KEY_VICTORY_ANNOUNCE_FIRST_SETTLE", AREA.format(self.area))
				goal.expire()


class FirstTribute(StateRequirement):

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_BE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_FIRST_TRIBUTE"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_FIRST_TRIBUTE"
	
	def __init__(self, **options):
		StateRequirement.__init__(self, **options)
		
		self.handle("tribute", self.succeed_on_tribute)
		self.expire("tribute", self.fail_on_tribute)
	
	def succeed_on_tribute(self, goal, iTo):
		self.succeed()
		goal.check()
	
	def fail_on_tribute(self, goal, iTo):
		self.fail()
		goal.announce_failure_cause(iTo, "TXT_KEY_VICTORY_ANNOUNCE_FIRST_TRIBUTE")
		goal.fail()


class Found(StateRequirement):

	TYPES = (RELIGION,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_FOUND"
	
	def __init__(self, iReligion, **options):
		StateRequirement.__init__(self, iReligion, **options)
		
		self.iReligion = iReligion
		
		self.handle("religionFounded", self.check_religion_founded)
		self.expire("religionFounded", self.expire_religion_founded)
	
	def check_religion_founded(self, goal, iReligion):
		if self.iReligion == iReligion:
			self.succeed()
			goal.check()
	
	def expire_religion_founded(self, goal, iReligion):
		if self.iReligion == iReligion:
			self.fail()
			goal.expire()


# Second Canadian UHV goal
class NoCityConquered(StateRequirement):

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_SIMPLE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_NO_CITY_CONQUERED"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_NO_CITY_CONQUERED"
	
	def __init__(self, **options):
		StateRequirement.__init__(self, **options)
		
		self.handle("cityAcquired", self.fail_on_city_conquered)
	
	def init(self, goal):
		goal.check()
	
	def fail_on_city_conquered(self, goal, city, bConquest):
		if bConquest and self.state == POSSIBLE:
			self.fail()
			goal.fail()
	
	def fulfilled(self, evaluator):
		return self.state != FAILURE


# First Japanese UHV goal
class NoCityLost(StateRequirement):

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_SIMPLE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_NO_CITY_LOST"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_NO_CITY_LOST"
	
	def __init__(self, **options):
		StateRequirement.__init__(self, **options)
		
		self.handle("cityLost", self.fail_on_city_lost)
	
	def init(self, goal):
		goal.check()
		
	def fail_on_city_lost(self, goal):
		if self.state == POSSIBLE:
			self.fail()
			goal.fail()
		
	def fulfilled(self, evaluator):
		return self.state != FAILURE


# First Polynesian UHV goal
# Second Polynesian UHV goal
class Settle(StateRequirement):

	TYPES = (AREA,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_SETTLE"
	
	def __init__(self, area, **options):
		StateRequirement.__init__(self, area, **options)
		
		self.area = area
		
		self.handle("cityBuilt", self.check_settled)
		#self.expire("cityBuilt", self.expire_settled)
		
	def check_settled(self, goal, city):
		if city in self.area and self.state == POSSIBLE:
			self.succeed()
			goal.check()
	
	def expire_settled(self, goal, city):
		if city in self.area and self.state == POSSIBLE:
			self.fail()
			goal.expire()
	
