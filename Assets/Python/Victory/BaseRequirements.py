from Core import *
from Types import *
from Formatters import *

from GoalHandlers import Handlers, event_handler_registry


class Requirement(object):

	GLOBAL_TYPES = ()
	TYPES = ()
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_HAVE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_SIMPLE"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_SIMPLE"
	
	BY_DESC_KEY = ""
	IN_DESC_KEY = ""
	SUBJECT_DESC_KEYS = {}

	def __init__(self, *parameters, **options):
		self.parameters = parameters
		
		self.handlers = Handlers()
	
	def __eq__(self, other):
		if not isinstance(other, type(self)):
			return False
			
		return self.parameters == other.parameters
	
	def __repr__(self):
		formatted_parameters = [parameter_type.format_repr(parameter) for parameter_type, parameter in zip(self.GLOBAL_TYPES + self.TYPES, self.parameters)]
		return "%s(%s)" % (type(self).__name__, ", ".join(formatted_parameters))
	
	def init(self, goal):
		pass
	
	def handle(self, event, func):
		self.handlers.add(event, func)
	
	def expire(self, event, func):
		self.handlers.add_other(event, func)
	
	def handle_any(self, event, func):
		self.handlers.add_any(event, func)
	
	def checked(self, event):
		self.handle(event, self.check)
	
	def register_handlers(self, goal):
		if not self.handlers.handlers and not self.handlers.any_handlers:
			self.checked("BeginPlayerTurn")
	
		event_handler_registry.register(self, goal)

	def deregister_handlers(self):
		event_handler_registry.deregister(self)
		
	def check(self, goal, *args):
		goal.check()
		
	def indicator(self, evaluator):
		return indicator(self.fulfilled(evaluator))
		
	def fulfilled(self, evaluator):
		raise NotImplementedError()
	
	def fulfillable(self):
		return True
		
	def additional_formats(self):
		return []
	
	def format_parameters(self, **options):
		return [type.format(type.scale(parameter), **options) for type, parameter in zip(self.GLOBAL_TYPES + self.TYPES, self.parameters)] + self.additional_formats()
		
	def description(self, **options):
		return text(self.DESC_KEY, *self.format_parameters(**options))
	
	def areas(self, **options):
		return dict((type.format_area(parameter, **options), type.area(parameter)) for type, parameter in zip(self.GLOBAL_TYPES + self.TYPES, self.parameters) if type.area(parameter) is not None)
		
	def area_name(self, tile):
		return "\n".join(name for name, area in self.areas().items() if tile in area)
	
	def format_description(self, **options):
		return self.description(**options)
	
	def progress_text(self, **options):
		if self.PROGR_KEY == "TXT_KEY_VICTORY_PROGR_SIMPLE" and not self.parameters:
			return capitalize(text(self.DESC_KEY))
		
		return capitalize(text(self.PROGR_KEY, *self.format_parameters(**options)))
	
	def progress(self, evaluator, **options):
		return "%s %s" % (self.indicator(evaluator), self.progress_text())


class ThresholdRequirement(Requirement):

	def __init__(self, *args, **options):
		Requirement.__init__(self, *args, **options)
		
		self.iRequired = args[-1]
		self.bPlural = self.iRequired > 1

	def value(self, iPlayer):
		raise NotImplementedError()
	
	def required(self):
		return self.TYPES[-1].scale(self.iRequired)
		
	def evaluate(self, evaluator):
		return evaluator.evaluate(self.value, *self.parameters[:-1])
	
	def fulfilled(self, evaluator):
		return self.evaluate(evaluator) >= self.required()
	
	def progress_value(self, evaluator):
		return "%d / %d" % (self.evaluate(evaluator), self.required())
	
	def progress(self, evaluator):
		if not self.bPlural:
			return Requirement.progress(self, evaluator)
	
		return "%s: %s" % (Requirement.progress(self, evaluator), self.progress_value(evaluator))


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


class CityRequirement(Requirement):

	def __init__(self, city, *parameters, **options):
		Requirement.__init__(self, city, *parameters, **options)
		
		self.city = city
		
	def fulfilled(self, evaluator):
		return evaluator.any(self.fulfilled_player)
	
	def progress(self, evaluator, **options):
		city = self.city.get(evaluator.iPlayer)
		
		if not city or city.isNone():
			return "%s %s" % (indicator(False), text("TXT_KEY_VICTORY_NO_CITY"))
		
		progress_key = city.getOwner() in evaluator and "TXT_KEY_VICTORY_PROGRESS_IN_CITY" or "TXT_KEY_VICTORY_PROGRESS_IN_CITY_DIFFERENT_OWNER"
		progress_city = self.progress_city(city)
		
		if progress_city:
			return "%s %s: %s" % (self.indicator(evaluator), text(progress_key, self.progress_text(**options), city.getName(), name(city.getOwner())), progress_city)
		
		return "%s %s" % (self.indicator(evaluator), text(progress_key, self.progress_text(**options), city.getName(), name(city.getOwner())))
	
	def fulfilled_player(self, iPlayer):
		city = self.city.get(iPlayer)
		return city and city.getOwner() == iPlayer and self.fulfilled_city(city)
		
	def fulfilled_city(self, city):
		raise NotImplementedError()
	
	def progress_city(self, city):
		return ""


class StateRequirement(Requirement):

	def __init__(self, *parameters, **options):
		Requirement.__init__(self, *parameters, **options)
		
		self.state = POSSIBLE
	
	def succeed(self):
		self.state = SUCCESS
	
	def fail(self):
		# show("Requirement '%s' failed", self.description())
		self.state = FAILURE
	
	def fulfilled(self, evaluator):
		return self.state == SUCCESS
	
	def fulfillable(self):
		return self.state != FAILURE


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


class BestEntitiesRequirement(Requirement):

	SUBJECT_DESC_KEYS = {
		STATE_RELIGION: "TXT_KEY_VICTORY_DESC_MAKE_SURE_THAT_ARE_RELIGION",
		SECULAR: "TXT_KEY_VICTORY_DESC_MAKE_SURE_THAT_ARE_SECULAR",
	}

	def __init__(self, iNumEntities = 1, **options):
		Requirement.__init__(self, iNumEntities, **options)
		
		self.iNumEntities = iNumEntities
	
	def metric(self, entity):
		raise NotImplementedError()
	
	def entities(self):
		raise NotImplementedError()
	
	def valid_entity(self, entity, evaluator):
		raise NotImplementedError()
	
	def entity_name(self, entity):
		raise NotImplementedError()
	
	def ranked(self, evaluator):
		return self.entities().sort(lambda entity: (self.metric(entity), self.valid_entity(entity, evaluator)), True)
	
	def required_ranks(self, evaluator):
		return self.ranked(evaluator)[0 : self.iNumEntities]
	
	def fulfilled(self, evaluator):
		return count(self.valid_entity(entity, evaluator) for entity in self.required_ranks(evaluator)) >= self.iNumEntities
	
	def next_rank(self, evaluator):
		ranked = self.ranked(evaluator)
		if len(ranked) <= 1:
			return None
		
		return self.fulfilled(evaluator) and ranked[self.iNumEntities] or next(entity for entity in ranked[self.iNumEntities:] if self.valid_entity(entity, evaluator))
	
	def rank_word(self, iRank):
		word = text(self.PROGR_KEY, *self.format_parameters())
		if iRank > 0:
			word = "%s %s" % (ordinal_word(iRank+1), word)
		return word
		
	def entity_progress(self, evaluator, iRank, entity):
		return "%s %s: %s (%d)" % (indicator(self.valid_entity(entity, evaluator)), capitalize(self.rank_word(iRank)), self.entity_name(entity), entity is not None and self.metric(entity) or 0)
	
	def next_entity_progress(self, evaluator, entity):
		next_key = self.valid_entity(entity, evaluator) and "TXT_KEY_VICTORY_PROGRESS_OUR_NEXT" or "TXT_KEY_VICTORY_PROGRESS_NEXT"
		return text(next_key, text(self.PROGR_KEY, *self.format_parameters()), self.entity_name(entity), self.metric(entity))
	
	def progress(self, evaluator):
		required_ranks = self.required_ranks(evaluator)
		
		if not required_ranks:
			return ["%s %s: %s (0)" % (indicator(False), capitalize(text(self.PROGR_KEY, *self.format_parameters())), self.entity_name(None))]
		
		entries = [self.entity_progress(evaluator, iRank, entity) for iRank, entity in enumerate(required_ranks) if entity is not None]
		
		next_entity = self.next_rank(evaluator)
		if next_entity is not None:
			entries.append(self.next_entity_progress(evaluator, next_entity))
		
		return entries
	

class BestPlayersRequirement(BestEntitiesRequirement):

	def entities(self):
		return players.major().alive()
	
	def valid_entity(self, iPlayer, evaluator):
		return iPlayer in evaluator
	
	def entity_name(self, iPlayer):
		if iPlayer is None:
			return text("TXT_KEY_VICTORY_NO_PLAYER")
		return name(iPlayer)


class BestCitiesRequirement(BestEntitiesRequirement):

	def entities(self):
		return cities.all()
	
	def valid_entity(self, city, evaluator):
		return city.getOwner() in evaluator
	
	def entity_name(self, city):
		if city is None:
			return text("TXT_KEY_VICTORY_NO_CITY")
		return city.getName()


class BestCityRequirement(BestCitiesRequirement):

	GLOBAL_TYPES = (CITY,)
	
	def __init__(self, city, *parameters, **options):
		BestCitiesRequirement.__init__(self, **options)
		
		parameters = (city,) + parameters + (1,)
		Requirement.__init__(self, *parameters, **options)
		
		self.required_city = city

	def valid_entity(self, city, evaluator):
		return BestCitiesRequirement.valid_entity(self, city, evaluator) and self.required_city == city

