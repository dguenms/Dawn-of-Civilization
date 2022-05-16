from Core import *
from VictoryEvaluators import *
from VictoryHandlers import *
from VictoryRequirements import *
from VictoryTypes import *


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
			return (locals,)
		elif not all(isinstance(argument, tuple) for argument in locals):
			raise ValueError("Expected %d local arguments, or a sequence of tuples containing %d local arguments each, found: %s" % (len(self.types), len(self.types), locals))
		
		return locals
		
	def validate_types(self, types, arguments):
		if len(types) != len(arguments):
			raise ValueError("Expected arguments %s to have %d elements with types %s" % (arguments, len(types), types))

		for type, argument in zip(types, arguments):
			if not type.validate(argument):
				raise ValueError("Expected arguments %s to be of types %s" % (arguments, types))


class GoalDefinition(object):

	def __init__(self, requirement, types=tuple()):
		self.requirement = requirement
		self.types = types
		
	def __call__(self, *arguments, **options):
		parameter_set = ParameterSet(global_types=self.types, types=self.requirement.TYPES, arguments=arguments)
		requirements = [self.requirement(*parameters, **options) for parameters in parameter_set]
		
		return GoalDescription(requirements, self.requirement.DESC_KEY, **options)
	
	def __repr__(self):
		return "GoalDefinition(%s, %s)" % (self.requirement.__name__, self.types)
		
	def __eq__(self, other):
		if not isinstance(other, GoalDefinition):
			return False
	
		return (self.requirement, self.types) == (other.requirement, other.types)
		
		
class GoalDescription(object):

	def __init__(self, requirements, desc_key, **options):
		self.requirements = requirements
		self.desc_key = desc_key
		self.options = options
		
		self.desc_suffixes = []
		
		if self.options.get("at") is not None:
			self.desc_suffixes.append(("TXT_KEY_VICTORY_IN", format_date(self.options.get("at"))))
		
		if self.options.get("by") is not None:
			self.desc_suffixes.append(("TXT_KEY_VICTORY_BY", format_date(self.options.get("by"))))
		
	def __call__(self, iPlayer):
		return Goal(self.requirements, self.desc_key, iPlayer, **self.options)
	
	def __repr__(self):
		return "GoalDescription(%s)" % ", ".join(str(requirement) for requirement in self.requirements)
	
	def __eq__(self, other):
		if not isinstance(other, GoalDescription):
			return False
			
		return (self.requirements, self.desc_key, self.options) == (other.requirements, other.desc_key, other.options)
		
	def format_description(self):
		requirement_descriptions = format_separators(self.requirements, ",", text("TXT_KEY_AND"), lambda requirement: requirement.description())
		description_descs = [(self.desc_key, requirement_descriptions)] + self.desc_suffixes
		return " ".join(text(*desc_args) for desc_args in description_descs)
	
	def description(self):
		return capitalize(self.format_description())
		

class Goal(object):

	def __init__(self, requirements, desc_key, iPlayer, subject=SELF, required=None, by=None, at=None, every=None, **options):
		self.requirements = requirements
		self.desc_key = desc_key
		self.iPlayer = iPlayer
		
		self.required = required
		
		self.state = POSSIBLE
		self.title_key = ""
		self.iYear = None
		self.desc_suffixes = []
		
		self.evaluator = EVALUATORS.get(subject, self.iPlayer)
		
		self.handlers = Handlers()
		
		if self.required is None:
			self.required = len(self.requirements)
		
		if by is not None:
			self.by(by)
		
		if at is not None:
			self.at(at)
		
		if every is not None:
			self.every()
		
		self.register_handlers()
	
	def __repr__(self):
		return "Goal(%s, %s)" % (self.requirements, self.iPlayer)
	
	def __eq__(self, other):
		if not isinstance(other, Goal):
			return False
		
		return (self.requirements, self.iPlayer) == (other.requirements, other.iPlayer)
	
	def register_handlers(self):
		event_handler_registry.register(self, self)
	
		for requirement in self.requirements:
			requirement.register_handlers(self)
	
	def deregister_handlers(self):
		for requirement in self.requirements:
			requirement.deregister_handlers()
	
	def possible(self):
		return self.state == POSSIBLE
	
	def succeeded(self):
		return self.state == SUCCESS
	
	def failed(self):
		return self.state == FAILURE
	
	def succeed(self):
		self.state = SUCCESS
	
	def fail(self):
		self.state = FAILURE
	
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
	
	def handle_at(self, goal, iGameTurn):
		if year(goal.iYear) == iGameTurn:
			goal.final_check()
	
	def handle_by(self, goal, iGameTurn):
		if year(goal.iYear) == iGameTurn:
			goal.expire()
	
	def handle_every(self, goal, iGameTurn):
		goal.check()
	
	def at(self, iYear):
		self.iYear = iYear
		self.handlers.add("BeginPlayerTurn", self.handle_at)
		
		self.desc_suffixes.append(("TXT_KEY_VICTORY_IN", format_date(iYear)))
	
	def by(self, iYear):
		self.iYear = iYear
		self.handlers.add("BeginPlayerTurn", self.handle_by)
		
		self.desc_suffixes.append(("TXT_KEY_VICTORY_BY", format_date(iYear)))
	
	def every(self):
		self.handlers.add("BeginPlayerTurn", self.handle_every)
	
	def format_description(self):
		requirement_descriptions = format_separators(self.requirements, ",", text("TXT_KEY_AND"), lambda requirement: requirement.format_description())
		description_descs = [(self.desc_key, requirement_descriptions)] + self.desc_suffixes
		return " ".join(text(*desc_args) for desc_args in description_descs)
	
	def description(self):
		return capitalize(self.format_description())
	
	def title(self):
		return text(self.title_key)
		
	def full_description(self):
		if self.title_key:
			return "%s: %s" % (self.title(), self.description())
		
		return self.description()
		
	def titled(self, key):
		self.title_key = key
		return self
	
	def desc(self, key):
		self.desc_key = key
		return self
	
	def progress(self):
		return [requirement.progress(self.evaluator) for requirement in self.requirements]


class All(object):

	def __init__(self, *descriptions, **options):
		self.descriptions = descriptions
		self.options = options
		
		for description in self.descriptions:
			description.options.update(self.options)
		
		self.desc_suffixes = []
		
		if self.options.get("at") is not None:
			self.desc_suffixes.append(("TXT_KEY_VICTORY_IN", format_date(self.options.get("at"))))
		
		if self.options.get("by") is not None:
			self.desc_suffixes.append(("TXT_KEY_VICTORY_BY", format_date(self.options.get("by"))))
	
	def __call__(self, iPlayer):
		return AllGoal([description(iPlayer) for description in self.descriptions], iPlayer, **self.options)
	
	def __repr__(self):
		return "All(%s)" % ", ".join(str(description) for description in self.descriptions)
	
	def __eq__(self, other):
		if not isinstance(other, All):
			return False
		
		return self.descriptions == other.descriptions
		
	def format_description(self):
		requirement_descriptions = format_separators(self.descriptions, ",", text("TXT_KEY_AND"), GoalDescription.format_description)
		description_descs = [("TXT_KEY_VICTORY_DESC_SIMPLE", requirement_descriptions)] + self.desc_suffixes
		return " ".join(text(*desc_args) for desc_args in description_descs)
	
	def description(self):
		return capitalize(self.format_description())
		
		
class AllGoal(Goal):

	def __init__(self, goals, iPlayer, **options):
		Goal.__init__(self, goals, "TXT_KEY_VICTORY_DESC_SIMPLE", iPlayer, **options)
		
		for goal in goals:
			self.add_subgoal(goal)
	
	def __repr__(self):
		return "AllGoal(%s)" % ", ".join(str(goal) for goal in self.requirements)

	def __eq__(self, other):
		if not isinstance(other, AllGoal):
			return False
		
		return Goal.__eq__(self, other)
	
	def register_handlers(self):
		pass
	
	def fulfilled(self):
		return all(goal.succeeded() for goal in self.requirements)
			
	def add_subgoal(self, goal):
		def fail(subgoal):
			subgoal.state = FAILURE
			self.fail()
		
		def succeed(subgoal):
			subgoal.state = SUCCESS
			self.check()
		
		goal.fail = fail.__get__(goal, Goal)
		goal.succeed = succeed.__get__(goal, Goal)
		
		
