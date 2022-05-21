from PercentRequirements import *

from TestVictoryCommon import *
	
	
class TestPopulationPercent(ExtendedTestCase):

	def setUp(self):
		self.requirement = PopulationPercent(30)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
		
	def test_str(self):
		self.assertEqual(str(self.requirement), "PopulationPercent(30%)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "PopulationPercent(30%)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "30% of the world's population")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_sufficient(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setPopulation(10)
		their_city.setPopulation(10)
		
		try:
			self.assertEqual(self.requirement.percentage(self.evaluator), 50.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Percentage of world population: 50.00% / 30%")
		finally:
			cities.kill()
	
	def test_insufficient(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setPopulation(5)
		their_city.setPopulation(15)
		
		try:
			self.assertEqual(self.requirement.percentage(self.evaluator), 25.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Percentage of world population: 25.00% / 30%")
		finally:
			cities.kill()
			
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
	
		our_city, vassal_city, other_city = cities = TestCities.owners(0, 1, 2)
		
		our_city.setPopulation(10)
		vassal_city.setPopulation(5)
		other_city.setPopulation(5)
		
		try:
			self.assertEqual(self.requirement.percentage(evaluator), 75.0)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Percentage of world population: 75.00% / 30%")
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)


test_cases = [
	TestPopulationPercent,
]