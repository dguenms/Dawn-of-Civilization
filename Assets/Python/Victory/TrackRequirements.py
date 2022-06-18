from Core import *
from VictoryTypes import *
from BaseRequirements import *


# First Tibetan UHV goal
class AcquiredCities(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRED_CITIES"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_ACQUIRED_CITIES"
	
	def __init__(self, *parameters, **options):
		TrackRequirement.__init__(self, *parameters, **options)
		
		self.recorded = set()
		
		self.handle("cityAcquired", self.record_city)
		self.handle("cityBuilt", self.record_city)
	
	def record_city(self, goal, city, *args):
		self.recorded.add(location(city))
		goal.check()
	
	def evaluate(self, evaluator):
		return len(self.recorded)
		

class BrokeredPeace(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_BROKERED_PEACE"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BROKERED_PEACE"

	def __init__(self, *parameters, **options):
		TrackRequirement.__init__(self, *parameters, **options)
		
		self.incremented("peaceBrokered")


# First Moorish UHV goal
# Second Dutch UHV goal
class ConqueredCities(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONQUER"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CONQUERED_CITIES"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CONQUERED_CITIES"
	
	def __init__(self, iRequired, civs=None, inside=None, outside=None, **options):
		TrackRequirement.__init__(self, iRequired, civs=civs, inside=inside, outside=outside, **options)
		
		self.recorded = set()
		self.civs = civs
		self.inside = inside
		self.outside = outside
		
		self.handle("cityAcquired", self.record_conquered_city)
		
	def valid_city(self, city):
		if self.civs is not None and Civ(city.getPreviousCiv()) not in self.civs:
			return False
	
		if self.inside is not None and city not in self.inside:
			return False
		
		if self.outside is not None and city in self.outside:
			return False
		
		return True
	
	def record_conquered_city(self, goal, city, bConquest):
		if bConquest and self.valid_city(city):
			self.recorded.add(location(city))
			goal.check()
	
	def evaluate(self, evaluator):
		return evaluator.sum(lambda p: cities.owner(p).where(lambda city: location(city) in self.recorded).count())
	
	def additional_formats(self):
		cities = text("TXT_KEY_VICTORY_CITIES")
		cities = qualify_adjective(cities, CIVS, self.civs)
		cities = in_area(cities, self.inside)
		cities = outside_area(cities, self.outside)
		
		return [cities]
	
	def areas(self):
		areas = {}
		
		if self.inside is not None:
			areas[self.inside.name()] = self.inside.create()
		
		if self.outside is not None:
			areas[self.outside.name()] = plots_.all().without(self.outside.create())
		
		return areas


# Third Aztec UHV goal
class EnslaveCount(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ENSLAVE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_ENSLAVE_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_ENSLAVE_COUNT"
	
	def __init__(self, iRequired, excluding=None, **options):
		TrackRequirement.__init__(self, iRequired, **options)
		
		self.excluding = excluding
		
		self.handle("enslave", self.increment_enslaved)
	
	def increment_enslaved(self, goal, unit):
		if is_minor(unit):
			return
		
		if self.excluding and civ(unit) in self.excluding:
			return
		
		self.increment()
		goal.check()
	
	def additional_formats(self):
		units = text("TXT_KEY_VICTORY_UNITS")
		units = qualify_adjective(units, CIVS, self.excluding)
		
		return [units]
	

# Third Japanese UHV goal
# Third English UHV goal
# Third German UHV goal
class EraFirstDiscover(TrackRequirement):

	TYPES = (ERA, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_FIRST_DISCOVER"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_ERA_FIRST_DISCOVER"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_ERA_FIRST_DISCOVER"
	
	def __init__(self, iEra, iRequired, **options):
		TrackRequirement.__init__(self, iEra, iRequired, **options)
		
		self.iEra = iEra
		self.iRequired = iRequired
		
		self.handle("techAcquired", self.increment_first_discovered)
		self.expire("techAcquired", self.expire_insufficient_techs_left)
		
	def increment_first_discovered(self, goal, iTech):
		if self.iEra == infos.tech(iTech).getEra():
			if game.countKnownTechNumTeams(iTech) == 1:
				self.increment()
				goal.check()
	
	def expire_insufficient_techs_left(self, goal, iTech):
		if self.iEra == infos.tech(iTech).getEra():
			if self.iValue + self.remaining_techs() < self.iRequired:
				goal.expire()
	
	def remaining_techs(self):
		return count(infos.tech(iTech).getEra() == self.iEra and game.countKnownTechNumTeams(iTech) == 0 for iTech in infos.techs())
		
	def progress(self, evaluator):
		return "%s (%s)" % (ThresholdRequirement.progress(self, evaluator), text("TXT_KEY_VICTORY_PROGRESS_REMAINING", self.remaining_techs()))


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


# First Turkic UHV goal
class PillageCount(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_PILLAGE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_PILLAGE_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_PILLAGE_COUNT"
	
	def __init__(self, *parameters, **options):
		TrackRequirement.__init__(self, *parameters, **options)
		
		self.incremented("unitPillage")


# Third Moorish UHV goal
class PiracyGold(TrackRequirement):

	TYPES = (AMOUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_PIRACY_GOLD"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_PIRACY_GOLD"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, scale(iRequired), **options)
		
		self.accumulated("unitPillage")
		self.accumulated("blockade")
		self.accumulated("combatGold")


# Third Viking UHV goal
class RaidGold(TrackRequirement):

	TYPES = (AMOUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_RAID_GOLD"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_RAID_GOLD"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, scale(iRequired), **options)
		
		self.accumulated("unitPillage")
		self.accumulated("cityCaptureGold")
		self.accumulated("combatGold")


# Second Mongol UHV goal
class RazeCount(TrackRequirement):

	TYPES = (COUNT,)

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_RAZE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_RAZE_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_RAZE_COUNT"
	
	def __init__(self, *parameters, **options):
		TrackRequirement.__init__(self, *parameters, **options)
		
		self.incremented("cityRazed")


# First Russian UHV goal
class SettledCities(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_SETTLE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_SETTLED_CITIES"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_SETTLED_CITIES"
	
	def __init__(self, iRequired, area=None, **options):
		TrackRequirement.__init__(self, iRequired, area=area, **options)
		
		self.recorded = set()
		self.area = area
		
		self.handle("cityBuilt", self.record_settled_city)
		
	def valid_city(self, city):
		return self.area is None or city in self.area
	
	def record_settled_city(self, goal, city):
		if self.valid_city(city):
			self.recorded.add(location(city))
			goal.check()
	
	def evaluate(self, evaluator):
		return evaluator.sum(lambda p: cities.owner(p).where(lambda city: location(city) in self.recorded).count())
	
	def additional_formats(self):
		cities = text("TXT_KEY_VICTORY_CITIES")
		cities = in_area(cities, self.area)
		
		return [cities]
	
	def areas(self):
		if self.area is not None:
			return {self.area.name(): self.area.create()}
		return {}


# Second Congolese UHV goal
class SlaveTradeGold(TrackRequirement):

	TYPES = (AMOUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_SLAVE_TRADE_GOLD"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_SLAVE_TRADE_GOLD"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, scale(iRequired), **options)
		
		self.accumulated("playerSlaveTrade")
	

# Third Korean UHV goal
# Second English UHV goal
class SunkShips(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_SINK"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_SUNK_SHIPS"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_SUNK_SHIPS"
	
	def __init__(self, *parameters, **options):
		TrackRequirement.__init__(self, *parameters, **options)
		
		self.handle("combatResult", self.increment_ships_sunk)
		
	def increment_ships_sunk(self, goal, unit):
		if infos.unit(unit).getDomainType() == DomainTypes.DOMAIN_SEA:
			self.increment()
			goal.check()


# Third Tamil UHV goal
class TradeGold(TrackRequirement):

	TYPES = (AMOUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_TRADE_GOLD"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_TRADE_GOLD"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, scale(iRequired), **options)
		
		self.handle("playerGoldTrade", self.accumulate_trade_gold)
		self.handle("tradeMission", self.accumulate_trade_mission_gold)
		self.handle("BeginPlayerTurn", self.accumulate_trade_deal_gold)
		self.handle("BeginPlayerTurn", self.accumulate_trade_route_gold)
	
	def accumulate_trade_gold(self, goal, iGold):
		self.accumulate(iGold * 100)
		goal.check()
	
	def accumulate_trade_mission_gold(self, goal, tile, iGold):
		self.accumulate(iGold * 100)
		goal.check()
	
	def accumulate_trade_deal_gold(self, goal, iGameTurn, iPlayer):
		iGold = players.major().alive().sum(lambda p: player(iPlayer).getGoldPerTurnByPlayer(p))
		self.accumulate(iGold * 100)
		goal.check()
	
	def accumulate_trade_route_gold(self, goal, iGameTurn, iPlayer):
		iGold = cities.owner(iPlayer).sum(lambda city: city.getTradeYield(YieldTypes.YIELD_COMMERCE)) * player(iPlayer).getCommercePercent(CommerceTypes.COMMERCE_GOLD)
		self.accumulate(iGold)
		goal.check()

	def evaluate(self, evaluator):
		return self.iValue / 100
	
