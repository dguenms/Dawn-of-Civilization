from Core import *
from VictoryTypes import *

from VictoryHandlers import Handlers, event_handler_registry


class Requirement(object):

	TYPES = ()
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_HAVE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_SIMPLE"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_SIMPLE"

	def __init__(self, *parameters, **options):
		self.parameters = parameters
		
		self.handlers = Handlers()
	
	def __eq__(self, other):
		if not isinstance(other, type(self)):
			return False
			
		return self.parameters == other.parameters
	
	def __repr__(self):
		formatted_parameters = [parameter_type.format_repr(parameter) for parameter_type, parameter in zip(self.TYPES, self.parameters)]
		return "%s(%s)" % (type(self).__name__, ", ".join(formatted_parameters))
	
	def handle(self, event, func):
		self.handlers.add(event, func)
	
	def expire(self, event, func):
		self.handlers.add_other(event, func)
	
	def handle_any(self, event, func):
		self.handlers.add_any(event, func)
	
	def register_handlers(self, goal):
		if not self.handlers.handlers:
			self.handle("BeginPlayerTurn", self.check_turnly)
	
		event_handler_registry.register(self, goal)

	def deregister_handlers(self):
		event_handler_registry.deregister(self)
		
	def check_turnly(self, goal, iGameTurn):
		goal.check()
		
	def indicator(self, evaluator):
		return indicator(self.fulfilled(evaluator))
		
	def fulfilled(self, evaluator):
		raise NotImplementedError()
	
	def format_parameters(self, **options):
		return [type.format(parameter, **options) for type, parameter in zip(self.TYPES, self.parameters)]
		
	def description(self, **options):
		return text(self.DESC_KEY, *self.format_parameters(**options))
	
	def format_description(self, **options):
		return self.description(**options)
	
	def progress(self, evaluator, **options):
		return "%s %s" % (self.indicator(evaluator), text(self.PROGR_KEY, *self.format_parameters(**options)))


class ThresholdRequirement(Requirement):

	def __init__(self, *args, **options):
		Requirement.__init__(self, *args, **options)
		
		self.iRequired = args[-1]

	def value(self, iPlayer):
		raise NotImplementedError()
	
	def required(self):
		return self.iRequired
		
	def evaluate(self, evaluator):
		return evaluator.evaluate(self.value, *self.parameters[:-1])
	
	def fulfilled(self, evaluator):
		return self.evaluate(evaluator) >= self.required()
	
	def progress_value(self, evaluator):
		return "%d / %d" % (self.evaluate(evaluator), self.required())
	
	def progress(self, evaluator):
		return "%s: %s" % (Requirement.progress(self, evaluator), self.progress_value(evaluator))


class BuildingCount(ThresholdRequirement):

	TYPES = (BUILDING, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_COUNT"
	
	def __init__(self, iBuilding, *args, **options):
		ThresholdRequirement.__init__(self, iBuilding, *args, **options)
		
		self.iBuilding = iBuilding
		
		self.handle("cityAcquired", self.check_city_acquired)
		self.handle("buildingBuilt", self.check_building_built)
	
	def check_city_acquired(self, goal, city, bConquest):
		goal.check()
	
	def check_building_built(self, goal, city, iBuilding):
		if base_building(iBuilding) == self.iBuilding:
			goal.check()
	
	def value(self, iPlayer, iBuilding):
		return player(iPlayer).countNumBuildings(unique_building(iPlayer, iBuilding))
	
	def is_plural(self):
		return self.required() > 1
		
	def description(self):
		return Requirement.description(self, bPlural=self.is_plural())
		
	def progress(self, evaluator):
		if not self.is_plural():
			return BUILDING.format(self.iBuilding)
		
		return "%s %s: %s" % (self.indicator(evaluator), text(self.PROGR_KEY, BUILDING.format(self.iBuilding, bPlural=True)), self.progress_value(evaluator))


class GoldAmount(ThresholdRequirement):

	TYPES = (AMOUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_PLAYER_GOLD"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_GOLD"
	
	def value(self, iPlayer):
		return player(iPlayer).getGold()
	
	def required(self):
		return scale(self.iRequired)


class PercentRequirement(ThresholdRequirement):

	def total(self):
		return players.major().alive().sum(self.value)
	
	def percentage(self, evaluator):
		iTotal = self.total()
		if iTotal <= 0:
			return 0.0
		return 100.0 * self.evaluate(evaluator) / iTotal
	
	def fulfilled(self, evaluator):
		return self.percentage(evaluator) >= 1.0 * self.required() - 0.005
		
	def progress_value(self, evaluator):
		return "%.2f%% / %d%%" % (self.percentage(evaluator), self.required())


class PopulationPercent(PercentRequirement):

	TYPES = (PERCENTAGE,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_POPULATION_PERCENT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_POPULATION_PERCENT"
	
	def value(self, iPlayer):
		return cities.owner(iPlayer).sum(CyCity.getPopulation)
	
	def total(self):
		return game.getTotalPopulation()
	

class Control(Requirement):
	
	TYPES = (AREA,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTROL"
	
	def __init__(self, area, **options):
		Requirement.__init__(self, area, **options)
		
		self.area = area
	
	def fulfilled(self, evaluator):
		return self.area.cities().all_if_any(lambda city: city.getOwner() in evaluator)


class StateRequirement(Requirement):

	def __init__(self, *parameters, **options):
		Requirement.__init__(self, *parameters, **options)
		
		self.state = POSSIBLE
	
	def succeed(self):
		self.state = SUCCESS
	
	def fail(self):
		self.state = FAILURE
	
	def fulfilled(self, evaluator):
		return self.state == SUCCESS
	
		
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


class TrackRequirement(ThresholdRequirement):

	def __init__(self, *parameters, **options):
		ThresholdRequirement.__init__(self, *parameters, **options)
		
		self.iValue = 0
	
	def accumulate(self, iChange):
		self.iValue += iChange
	
	def increment(self):
		self.accumulate(1)
	
	def accumulate_handler(self, goal, iChange, *args):
		self.accumulate(iChange)
		goal.check()
	
	def increment_handler(self, goal, *args):
		self.increment()
		goal.check()
	
	def accumulated(self, event):
		self.handle(event, self.accumulate_handler)
	
	def incremented(self, event):
		self.handle(event, self.increment_handler)
	
	def evaluate(self, evaluator):
		return self.iValue
		

class BrokeredPeace(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_BROKERED_PEACE"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BROKERED_PEACE"

	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, iRequired, **options)
		
		self.iRequired = iRequired
		
		self.incremented("peaceBrokered")
	
	def required(self):
		return self.iRequired


class BestEntitiesRequirement(Requirement):

	def __init__(self, iNumEntities = 1, **options):
		Requirement.__init__(self, iNumEntities, **options)
		
		self.iNumEntities = iNumEntities
	
	def metric(self, entity):
		raise NotImplementedError()
	
	def entities(self):
		raise NotImplementedError()
	
	def player_entity(self, entity, evaluator):
		raise NotImplementedError()
	
	def entity_name(self, entity):
		raise NotImplementedError()
	
	def ranked(self, evaluator):
		return self.entities().sort(lambda entity: (self.metric(entity), self.player_entity(entity, evaluator)), True)
	
	def required_ranks(self, evaluator):
		return self.ranked(evaluator)[0 : self.iNumEntities]
	
	def fulfilled(self, evaluator):
		return count(self.player_entity(entity, evaluator) for entity in self.required_ranks(evaluator)) >= self.iNumEntities
	
	def next_rank(self, evaluator):
		return self.fulfilled(evaluator) and self.ranked(evaluator)[self.iNumEntities] or next(entity for entity in self.ranked(evaluator)[self.iNumEntities:] if self.player_entity(entity, evaluator))
	
	def rank_word(self, iRank):
		word = text(self.PROGR_KEY)
		if iRank > 0:
			word = "%s %s" % (ordinal_word(iRank+1), word)
		return word
		
	def entity_progress(self, evaluator, iRank, entity):
		return "%s %s: %s (%d)" % (indicator(self.player_entity(entity, evaluator)), capitalize(self.rank_word(iRank)), self.entity_name(entity), entity is not None and self.metric(entity) or 0)
	
	def next_entity_progress(self, evaluator, entity):
		next_key = self.player_entity(entity, evaluator) and "TXT_KEY_VICTORY_PROGRESS_OUR_NEXT" or "TXT_KEY_VICTORY_PROGRESS_NEXT"
		return text(next_key, text(self.PROGR_KEY), self.entity_name(entity), self.metric(entity))
	
	def progress(self, evaluator):
		required_ranks = self.required_ranks(evaluator)
		
		if not required_ranks:
			return ["%s %s: %s (0)" % (indicator(False), capitalize(text(self.PROGR_KEY)), self.entity_name(None))]
		
		entries = [self.entity_progress(evaluator, iRank, entity) for iRank, entity in enumerate(required_ranks) if entity is not None]
		
		next_entity = self.next_rank(evaluator)
		if next_entity is not None:
			entries.append(self.next_entity_progress(evaluator, next_entity))
		
		return entries


class BestPlayersRequirement(BestEntitiesRequirement):

	def entities(self):
		return players.major().alive()
	
	def player_entity(self, iPlayer, evaluator):
		return iPlayer in evaluator
	
	def entity_name(self, iPlayer):
		if iPlayer is None:
			return "No Player"
		return name(iPlayer)


class BestCitiesRequirement(BestEntitiesRequirement):

	def entities(self):
		return cities.all()
	
	def player_entity(self, city, evaluator):
		return city.getOwner() in evaluator
	
	def entity_name(self, city):
		if city is None:
			return "No City"
		return city.getName()
	
		
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
	

