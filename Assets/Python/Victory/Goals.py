from Core import *
from Evaluators import *
from GoalHandlers import *
from Formatters import *
from Requirements import *
from Types import *

from CityNameManager import getFoundName, getRenameName

import BugCore
AlertsOpt = BugCore.game.MoreCiv4lerts
AdvisorOpt = BugCore.game.Advisors


class Parameters(object):

	def __init__(self, globals, locals):
		self.parameters = concat(globals, locals)
	
	def __iter__(self):
		return iter(self.parameters)
	
	def __repr__(self):
		return "Parameters%s" % (tuple(self.parameters),)
	
	def __eq__(self, other):
		if not isinstance(other, Parameters):
			return False
	
		return self.parameters == other.parameters


class ParameterSet(object):

	def __init__(self, global_types, types, arguments):
		self.global_types = global_types
		self.types = types
		
		self.parameters = self.parse_parameters(arguments)
	
	def __iter__(self):
		return iter(self.parameters)
	
	def __repr__(self):
		return "ParameterSet(%s, %s, %s)" % (self.global_types, self.types, self.parameters)
	
	def __eq__(self, other):
		if not isinstance(other, ParameterSet):
			return False
		
		return (self.global_types, self.types, self.parameters) == (other.global_types, other.types, other.parameters)
	
	def parse_parameters(self, arguments):
		iNumGlobal = len(self.global_types)
		globals, locals = arguments[:iNumGlobal], arguments[iNumGlobal:]
	
		self.validate_types(self.global_types, globals)
		
		locals = self.parse_locals(locals)
		for local_arguments in locals:
			self.validate_types(self.types, local_arguments)
			
		return [Parameters(globals, local_arguments) for local_arguments in locals]
		
	def parse_locals(self, locals):
		if none(isinstance(argument, tuple) for argument in locals):
			if len(self.types) == 1:
				return tuple((argument,) for argument in locals)
			else:
				return (locals,)
		
		if not all(isinstance(argument, tuple) for argument in locals):
			raise ValueError("Expected %d local arguments, or a sequence of tuples containing %d local arguments each, found: %s" % (len(self.types), len(self.types), locals))
		
		return locals
		
	def validate_types(self, types, arguments):
		if len(types) != len(arguments):
			raise ValueError("Expected arguments %s to have %d elements with types %s" % (arguments, len(types), types))

		for type, argument in zip(types, arguments):
			if not type.validate(argument):
				raise ValueError("Expected arguments %s to be of types %s" % (arguments, types))


class GoalDefinition(object):

	def __init__(self, requirement):
		self.requirement = requirement
		
	def __call__(self, *arguments, **options):
		try:
			parameter_set = ParameterSet(global_types=self.requirement.GLOBAL_TYPES, types=self.requirement.TYPES, arguments=arguments)
			requirements = [self.requirement(*parameters, **options) for parameters in parameter_set]
			desc_key = options.pop("desc_key", self.requirement.GOAL_DESC_KEY)
		
			return GoalDescription(requirements, desc_key, **options)
		
		except ValueError, e:
			raise ValueError("Error when parsing arguments for %s: %s" % (self.requirement.__name__, e))
	
	def __repr__(self):
		return "GoalDefinition(%s)" % (self.requirement.__name__)
		
	def __eq__(self, other):
		if not isinstance(other, GoalDefinition):
			return False
	
		return self.requirement == other.requirement


class Describable(object):

	IN_DESC_KEY = None
	BY_DESC_KEY = None
	SUBJECT_DESC_KEYS = {}

	def __init__(self, requirement, desc_key, at=None, by=None, subject=None, iReligion=None, **options):
		self.desc_key = desc_key
		self.iYear = None
		
		self.date_suffix_keys = {}
		self.desc_args = []
		
		if at is not None:
			self.at(at)	
			self.date_suffix_keys["TXT_KEY_VICTORY_IN"] = at
			
			if requirement.IN_DESC_KEY:
				self.desc_key = requirement.IN_DESC_KEY
		
		if by is not None:
			self.by(by)
			self.date_suffix_keys["TXT_KEY_VICTORY_BY"] = by
			
			if requirement.BY_DESC_KEY:
				self.desc_key = requirement.BY_DESC_KEY
		
		if subject is not None:
			subject_desc_key = requirement.SUBJECT_DESC_KEYS.get(subject)
			if subject_desc_key:
				self.desc_key = subject_desc_key
		
		if iReligion is not None:
			self.desc_args.append(RELIGION_ADJECTIVE.format(iReligion))
	
	def create_date_suffixes(self):
		for key, iYear in self.date_suffix_keys.items():
			yield text(key, format_date_turn(iYear, self.show_date_turn()))
	
	def show_date_turn(self):
		return False
	
	def at(self, at):
		pass
	
	def by(self, by):
		pass


class GoalDescription(Describable):

	def __init__(self, requirements, desc_key, **options):
		Describable.__init__(self, requirements[0], desc_key, **options)
	
		self.requirements = requirements
		self.options = options
		
	def __call__(self, iPlayer, **options):
		combined_options = self.options.copy()
		combined_options.update(options)
		return Goal(self.requirements, self.desc_key, iPlayer, **combined_options)
	
	def __repr__(self):
		return "GoalDescription(%s)" % ", ".join(str(requirement) for requirement in self.requirements)
	
	def __eq__(self, other):
		if not isinstance(other, GoalDescription):
			return False
			
		return (self.requirements, self.desc_key, self.options) == (other.requirements, other.desc_key, other.options)
		
	def format_description(self):
		return DESCRIPTION.format([(req, self.desc_key, [], []) for req in self.requirements], self.desc_args, self.create_date_suffixes(), self.options.get("required"))
	
	def description(self):
		return capitalize(self.format_description())
		

class Goal(Describable):

	def __init__(self, requirements, desc_key, iPlayer, subject=SELF, mode=STATEFUL, required=None, title_key="", **options):
		self.handlers = Handlers()
	
		self.requirements = requirements
		self.iPlayer = iPlayer
		
		self.mode = mode
		self.required = required
		self.title_key = title_key
		
		self.state = POSSIBLE
		self.iSuccessTurn = None
		self.bRequirementHandlers = True
		
		Describable.__init__(self, requirements[0], desc_key, subject=subject, **options)
		
		if self.required is None:
			self.required = len(self.requirements)
		
		self.evaluator = EVALUATORS.get(subject, self.iPlayer)
	
		self._areas = dict((name, area) for requirement in self.requirements for name, area in requirement.areas().items())
		
		self.check()
		
	def __repr__(self):
		return "Goal(%s, %s)" % (self.requirements, self.iPlayer)
	
	def __eq__(self, other):
		if not isinstance(other, Goal):
			return False
		
		return (self.requirements, self.iPlayer) == (other.requirements, other.iPlayer)
	
	def enable(self):
		event_handler_registry.register(self, self)
	
		if self.bRequirementHandlers:
			for requirement in self.requirements:
				requirement.register_handlers(self)
	
	def disable(self):
		event_handler_registry.deregister(self)
	
		if self.bRequirementHandlers:
			for requirement in self.requirements:
				requirement.deregister_handlers()
	
	def possible(self):
		return self.state == POSSIBLE
	
	def succeeded(self):
		if self.state == SUCCESS:
			return True
		
		return self.mode == STATELESS and self.fulfilled()
	
	def failed(self):
		return self.state == FAILURE
	
	def set_state(self, state):
		if self.state != state:
			if self.mode == STATEFUL or state != SUCCESS:
				self.state = state
				
				if self.state == SUCCESS:
					self.iSuccessTurn = turn()
	
	def succeed(self):
		self.set_state(SUCCESS)
	
	def fail(self):
		self.set_state(FAILURE)
	
	def override(self, func):
		return func.__get__(self, Goal)
	
	def fulfilled(self):
		return count(requirement.fulfilled(self.evaluator) for requirement in self.requirements) >= self.required
	
	def check(self):
		if not self.possible():
			return
		
		if self.fulfilled():
			self.succeed()
	
	def expire(self):
		if self.possible():
			self.fail()
	
	def final_check(self):
		self.check()
		self.expire()
	
	def handle_at(self, goal, iGameTurn, iPlayer):
		if year(goal.iYear) == iGameTurn:
			goal.final_check()
	
	def handle_by(self, goal, iGameTurn, iPlayer):
		if year(goal.iYear) == iGameTurn:
			goal.final_check()
	
	def at(self, iYear):
		self.iYear = iYear
		self.bRequirementHandlers = False
		self.handlers.add("BeginPlayerTurn", self.handle_at)
		
	def by(self, iYear):
		self.iYear = iYear
		self.handlers.add("BeginPlayerTurn", self.handle_by)
	
	def show_date_turn(self):
		return not team(self.iPlayer).isHasTech(iCalendar) or not AdvisorOpt.isUHVFinishDateNone()
		
	def format_description(self):
		return DESCRIPTION.format([(req, self.desc_key, [], []) for req in self.requirements], self.desc_args, self.create_date_suffixes(), self.required < len(self.requirements) and self.required or None)
	
	def description(self):
		return capitalize(self.format_description())
	
	def title(self):
		return text(self.title_key)
		
	def full_description(self):
		if self.title_key:
			return "%s: %s" % (self.title(), self.description())
		
		return self.description()
		
	def state_string(self):
		if self.failed():
			return text("TXT_KEY_VICTORY_GOAL_FAILURE")
		
		if self.succeeded():
			return text("TXT_KEY_VICTORY_GOAL_SUCCESS")
		
		return text("TXT_KEY_VICTORY_GOAL_POSSIBLE")
	
	def announce(self, key, condition=True):
		if condition and player(self.iPlayer).isHuman() and not scenarioStart():
			show(text(key, self.format_description()))
	
	def announce_success(self):
		self.announce("TXT_KEY_VICTORY_ANNOUNCE_SUCCESS", AlertsOpt.isShowUHVSuccessPopup())
	
	def announce_failure(self):
		self.announce("TXT_KEY_VICTORY_ANNOUNCE_FAILURE", AlertsOpt.isShowUHVFailPopup())
	
	def areas(self):
		return self._areas
		
	def area_name(self, tile):
		return "\n".join(name for name, area in self.areas().items() if tile in area)
	
	def success_string(self):
		success_string = text("TXT_KEY_VICTORY_GOAL_SUCCESS_STRING")
		
		if self.iSuccessTurn is not None:
			if AdvisorOpt.isUHVFinishDateTurn():
				success_string += " (%s - %s)" % (format_date(game.getTurnYear(self.iSuccessTurn)), text("TXT_KEY_VICTORY_TURN", self.iSuccessTurn - scenarioStartTurn()))
			elif AdvisorOpt.isUHVFinishDateDate():
				success_string += " (%s)" % format_date(game.getTurnYear(self.iSuccessTurn))
	
		return "%s %s" % (indicator(True), success_string)
	
	def failure_string(self):
		return "%s %s" % (indicator(False), text("TXT_KEY_VICTORY_GOAL_FAILURE_STRING"))
	
	def format_progress(self):
		return PROGRESS.format(self.requirements, self.evaluator)
	
	def progress(self):
		progress_lines = []
		
		if self.succeeded() and self.mode != STATELESS:
			progress_lines.append(self.success_string())
		elif self.failed():
			progress_lines.append(self.failure_string())
		
		if self.possible() or AdvisorOpt.UHVProgressAfterFinish():
			progress_lines += self.format_progress()
		
		return progress_lines
		
		
class AllGoal(Goal):

	def __init__(self, goals, iPlayer, **options):
		Goal.__init__(self, goals, "TXT_KEY_VICTORY_DESC_SIMPLE", iPlayer, **options)
	
	def __repr__(self):
		return "AllGoal(%s)" % ", ".join(str(goal) for goal in self.requirements)

	def __eq__(self, other):
		if not isinstance(other, AllGoal):
			return False
		
		return Goal.__eq__(self, other)
	
	def enable(self):
		for subgoal in self.requirements:
			subgoal.succeed = subgoal.override(self.subgoal_succeed())
			subgoal.fail = subgoal.override(self.subgoal_fail())
			
			subgoal.enable()
	
	def disable(self):
		for subgoal in self.requirements:
			subgoal.disable()
	
	def subgoal_succeed(self):
		def succeed(subgoal):
			subgoal.set_state(SUCCESS)
			self.check()
		
		return succeed
	
	def subgoal_fail(self):
		def fail(subgoal):
			subgoal.set_state(FAILURE)
			self.expire()
		
		return fail
	
	def fulfilled(self):
		return all(goal.succeeded() for goal in self.requirements)
	
	def format_progress(self):
		return sum((goal.format_progress() for goal in self.requirements), [])
	
	def format_description(self):
		date_suffixes = list(self.create_date_suffixes())
		
		if date_suffixes:
			requirement_entries = [(req, goal.desc_key, goal.desc_args, []) for goal in self.requirements for req in goal.requirements]
		else:
			requirement_entries = [(req, goal.desc_key, goal.desc_args, goal.create_date_suffixes()) for goal in self.requirements for req in goal.requirements]
		
		return DESCRIPTION.format(requirement_entries, self.desc_args, date_suffixes)
	

class DifferentCitiesGoal(Goal):

	def __init__(self, goals, iPlayer, **options):
		Goal.__init__(self, goals, goals[0].desc_key, iPlayer, **options)
		
		self.recorded = {}
	
	def __repr__(self):
		return "DifferentCitiesGoal(%s)" % ", ".join(str(goal) for goal in self.requirements)
	
	def __eq__(self, other):
		if not isinstance(other, DifferentCitiesGoal):
			return False
		
		return Goal.__eq__(self, other)
	
	def enable(self):
		for subgoal in self.requirements:
			subgoal.succeed = subgoal.override(self.subgoal_succeed())
			subgoal.fail = subgoal.override(self.subgoal_fail())
			
			subgoal.enable()
	
	def disable(self):
		for subgoal in self.requirements:
			subgoal.disable()
	
	def subgoal_succeed(self):
		def succeed(subgoal):
			subgoal.set_state(SUCCESS)
			self.record(subgoal)
		
			if self.failed():
				subgoal.set_state(FAILURE)
		
			self.check()
		
		return succeed
	
	def subgoal_fail(self):
		def fail(subgoal):
			subgoal.set_state(FAILURE)
			self.fail()
		
		return fail
		
	def get_city_parameter(self):
		return next(parameter.get(self.iPlayer) for goal in self.requirements for requirement in goal.requirements for type, parameter in zip(requirement.GLOBAL_TYPES + requirement.TYPES, requirement.parameters) if type == CITY)
	
	def record(self, subgoal):
		city_parameter = self.get_city_parameter()
		if city_parameter:
			self.recorded[subgoal] = location(city_parameter)
			if not self.unique_records():
				self.fail()
			
	def unique_records(self):
		records = [self.recorded.get(subgoal) for subgoal in self.requirements if subgoal in self.recorded]
		return len(records) == len(set(records))
	
	def fulfilled(self):
		return all(goal.succeeded() for goal in self.requirements) and self.unique_records()
	
	def format_description(self):
		return DESCRIPTION.format([(req, goal.desc_key, goal.desc_args, goal.create_date_suffixes()) for goal in self.requirements for req in goal.requirements], self.desc_args, self.create_date_suffixes())
		
	def progress_entries(self):
		for subgoal in self.requirements:
			if subgoal.succeeded():
				recorded_location = self.recorded.get(subgoal)
				recorded_city = city(recorded_location)
				city_name = recorded_city and recorded_city.getName() or getFoundName(self.iPlayer, recorded_location)
				yield "%s %s" % (indicator(True), getRenameName(self.iPlayer, city_name) or city_name)
			else:
				current_city = self.get_city_parameter()
				if current_city and location(current_city) in self.recorded.values():
					yield "%s %s" % (indicator(False), text("TXT_KEY_VICTORY_ALREADY_COMPLETED_FOR", current_city.getName()))
				else:
					for entry in subgoal.format_progress():
						yield entry
				break
	
	def format_progress(self):
		return list(self.progress_entries())
	

class Combined(Describable):

	def __init__(self, *descriptions, **options):
		Describable.__init__(self, descriptions[0], None, **options)
	
		self.descriptions = descriptions
		self.options = options
		
		for description in self.descriptions:
			description.options.update(self.options)
		
	def __call__(self, iPlayer, **options):
		combined_options = self.options.copy()
		combined_options.update(options)
		return self.CLASS([description(iPlayer, **combined_options) for description in self.descriptions], iPlayer, **combined_options)
	
	def __repr__(self):
		return "%s(%s)" % (type(self).__name__, ", ".join(str(description) for description in self.descriptions))
	
	def __eq__(self, other):
		if not isinstance(other, type(self)):
			return False
		
		return self.descriptions == other.descriptions
	
	def format_description(self):
		return DESCRIPTION.format([(req, description.desc_key, description.desc_args, description.create_date_suffixes()) for description in self.descriptions for req in description.requirements], self.desc_args, self.create_date_suffixes(), self.options.get("required"))
	
	def description(self):
		return capitalize(self.format_description())


class All(Combined):

	CLASS = AllGoal
		

class DifferentCities(Combined):

	CLASS = DifferentCitiesGoal
		
