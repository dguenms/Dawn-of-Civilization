from Core import *

from unittest import *

from VictoryEvaluators import *
from Pickle import pickle


class ExtendedTestCase(TestCase):

	SUCCESS = u"%c " % game.getSymbolID(FontSymbols.SUCCESS_CHAR)
	FAILURE = u"%c " % game.getSymbolID(FontSymbols.FAILURE_CHAR)
	
	def __init__(self, *args, **kwargs):
		TestCase.__init__(self, *args, **kwargs)
		
		self.iPlayer = 0
		self.evaluator = SelfEvaluator(self.iPlayer)

	def assertType(self, object, expectedType):
		self.assertEqual(type(object), expectedType)
	
	def assertPickleable(self, object):
		saved = pickle.dumps(object)
		loaded = pickle.loads(saved)
		self.assertEqual(loaded, object)
		
	@property
	def player(self):
		return player(self.iPlayer)
		

class TestCities(object):

	CITY_LOCATIONS = [(61, 31), (63, 31), (65, 31), (67, 31), (69, 31)]
	
	@staticmethod
	def owners(*owners):
		return TestCities(owners)
	
	@staticmethod
	def num(iNumCities):
		return TestCities([0] * iNumCities)
	
	@staticmethod
	def one(iOwner = 0):
		return player(iOwner).initCity(*TestCities.CITY_LOCATIONS[0])

	def __init__(self, lOwners):
		if len(lOwners) > len(self.CITY_LOCATIONS):
			raise ValueError("Can at most create %d cities" % len(self.CITY_LOCATIONS))
		
		self.cities = [player(iOwner).initCity(*self.CITY_LOCATIONS[i]) for i, iOwner in enumerate(lOwners)]
	
	def __iter__(self):
		return iter(self.cities)
	
	def __getitem__(self, index):
		return self.cities[index]
	
	def kill(self):
		for city in self:
			city.kill()


class TestGoal(object):

	def __init__(self, iPlayer=0):
		self.iPlayer = iPlayer
		self.evaluator = SelfEvaluator(self.iPlayer)
		
		self.checked = False
		self.failed = False

	def check(self):
		self.checked = True
	
	def expire(self):
		self.failed = True