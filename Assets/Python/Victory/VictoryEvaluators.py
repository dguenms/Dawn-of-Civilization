from Core import *
from VictoryTypes import *


class Evaluators(object):

	def __init__(self):
		self.evaluators = {
			SELF: SelfEvaluator,
			VASSALS: VassalsEvaluator,
			ALLIES: AlliesEvaluator,
			STATE_RELIGION: ReligionEvaluator,
			SECULAR: SecularEvaluator,
			WORLD: WorldEvaluator,
		}
	
	def __eq__(self, other):
		return isinstance(other, Evaluators)
	
	def get(self, subject, iPlayer):
		if subject not in self.evaluators:
			raise ValueError("Invalid subject type: %s" % subject)
	
		evaluator_type = self.evaluators.get(subject)
		return evaluator_type(iPlayer)


class Evaluator(object):

	def __init__(self, iPlayer):
		self.iPlayer = iPlayer
	
	def __eq__(self, other):
		if not isinstance(other, type(self)):
			return False
		
		return self.iPlayer == other.iPlayer
	
	def __iter__(self):
		return iter(self.players())
	
	def __contains__(self, item):
		return item in self.players()
	
	def players(self):
		raise NotImplementedError()
	
	def any(self, condition):
		return any(condition(iPlayer) for iPlayer in self)
		
	def sum(self, func):
		return sum(func(iPlayer) for iPlayer in self)
	
	def max(self, func):
		return max(func(iPlayer) for iPlayer in self)
	
	def evaluate(self, func, *args):
		arguments = list(args)
		
		for i, argument in enumerate(arguments):
			if isinstance(argument, DeferredArgument):
				arguments[i] = argument.get(self.iPlayer)
	
		for i, argument in enumerate(arguments):
			if isinstance(argument, Aggregate):
				left_arguments = arguments[:i]
				right_arguments = arguments[i+1:]
				return argument.evaluate(self.evaluate_func(func), left_arguments, right_arguments)
		
		return self.evaluate_func(func)(*arguments)
	
	def evaluate_func(self, func):
		def evaluate(*args):
			return sum(func(iPlayer, *args) for iPlayer in self.players())
		return evaluate


class SelfEvaluator(Evaluator):

	def players(self):
		yield self.iPlayer


class VassalsEvaluator(Evaluator):

	def players(self):
		yield self.iPlayer
		
		for iVassal in players.vassals(self.iPlayer):
			yield iVassal


class AlliesEvaluator(Evaluator):

	def players(self):
		yield self.iPlayer
		
		for iVassal in players.vassals(self.iPlayer):
			yield iVassal
		
		for iAlly in players.defensivePacts(self.iPlayer):
			yield iAlly
			
			for iAllyVassal in players.vassals(iAlly):
				yield iAllyVassal


class ReligionEvaluator(Evaluator):

	def players(self):
		if player(self.iPlayer).getStateReligion() >= 0:
			for iSameReligion in players.major().alive().where(lambda p: player(p).getStateReligion() == player(self.iPlayer).getStateReligion()):
				yield iSameReligion


class SecularEvaluator(Evaluator):

	def players(self):
		for iSecular in players.major().alive().where(lambda p: not player(p).isStateReligion()):
			yield iSecular


class WorldEvaluator(Evaluator):

	def players(self):
		for iPlayer in players.major().alive():
			yield iPlayer


EVALUATORS = Evaluators()
		