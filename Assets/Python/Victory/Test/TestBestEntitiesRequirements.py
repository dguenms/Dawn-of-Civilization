from BestEntitiesRequirements import *

from TestVictoryCommon import *


class TestBestPopulationPlayer(ExtendedTestCase):

	def setUp(self):
		self.requirement = BestPopulationPlayer()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
		
	def test_str(self):
		self.assertEqual(str(self.requirement), "BestPopulationPlayer()")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "BestPopulationPlayer()")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "the largest population in the world")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_best(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setPopulation(10)
		their_city.setPopulation(5)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), [self.SUCCESS + "Most populous: Egypt (1000000)", "Next most populous: Babylonia (125000)"])
		finally:
			cities.kill()
	
	def test_second(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setPopulation(5)
		their_city.setPopulation(10)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [self.FAILURE + "Most populous: Babylonia (1000000)", "Our next most populous: Egypt (125000)"])
		finally:
			cities.kill()
	
	def test_third(self):
		our_city, best_city, runnerup_city = cities = TestCities.owners(0, 1, 2)
		
		our_city.setPopulation(5)
		best_city.setPopulation(10)
		runnerup_city.setPopulation(8)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [self.FAILURE + "Most populous: Babylonia (1000000)", "Our next most populous: Egypt (125000)"])
		finally:
			cities.kill()
	
	def test_multiple_players_fulfilled(self):
		requirement = BestPopulationPlayer(2)
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		our_city, vassal_city, other_city = cities = TestCities.owners(0, 1, 2)
		
		our_city.setPopulation(10)
		vassal_city.setPopulation(8)
		other_city.setPopulation(5)
		
		try:
			self.assertEqual(requirement.fulfilled(evaluator), True)
			self.assertEqual(requirement.progress(evaluator), [self.SUCCESS + "Most populous: Egypt (1000000)", self.SUCCESS + "Second most populous: Babylonia (512000)", "Next most populous: Harappa (125000)"])
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_multiple_players_not_fulfilled(self):
		requirement = BestPopulationPlayer(2)
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		our_city, vassal_city, other_city = cities = TestCities.owners(0, 1, 2)
		
		our_city.setPopulation(5)
		vassal_city.setPopulation(10)
		other_city.setPopulation(8)
		
		try:
			self.assertEqual(requirement.fulfilled(evaluator), False)
			self.assertEqual(requirement.progress(evaluator), [self.SUCCESS + "Most populous: Babylonia (1000000)", self.FAILURE + "Second most populous: Harappa (512000)", "Our next most populous: Egypt (125000)"])
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)


class TestBestPopulationCities(ExtendedTestCase):

	def setUp(self):
		self.requirement = BestPopulationCities(3)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "BestPopulationCities(3)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "BestPopulationCities(3)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "the three largest cities in the world")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_all(self):
		city1, city2, city3, city4 = cities = TestCities.owners(0, 0, 0, 1)
		
		city1.setName("First", False)
		city1.setPopulation(10)
		
		city2.setName("Second", False)
		city2.setPopulation(9)
		
		city3.setName("Third", False)
		city3.setPopulation(8)
		
		city4.setName("Fourth", False)
		city4.setPopulation(7)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Most populous: First (10)",
				self.SUCCESS + "Second most populous: Second (9)",
				self.SUCCESS + "Third most populous: Third (8)",
				"Next most populous: Fourth (7)"
			])
		finally:
			cities.kill()
	
	def test_all_and_next(self):
		city1, city2, city3, city4 = cities = TestCities.owners(0, 0, 0, 0)
		
		city1.setName("First", False)
		city1.setPopulation(10)
		
		city2.setName("Second", False)
		city2.setPopulation(9)
		
		city3.setName("Third", False)
		city3.setPopulation(8)
		
		city4.setName("Fourth", False)
		city4.setPopulation(7)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Most populous: First (10)",
				self.SUCCESS + "Second most populous: Second (9)",
				self.SUCCESS + "Third most populous: Third (8)",
				"Our next most populous: Fourth (7)"
			])
		finally:
			cities.kill()
	
	def test_some(self):
		city1, city2, city3, city4, city5 = cities = TestCities.owners(0, 0, 1, 1, 0)
		
		city1.setName("First", False)
		city1.setPopulation(10)
		
		city2.setName("Second", False)
		city2.setPopulation(9)
		
		city3.setName("Third", False)
		city3.setPopulation(8)
		
		city4.setName("Fourth", False)
		city4.setPopulation(7)
		
		city5.setName("Fifth", False)
		city5.setPopulation(6)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Most populous: First (10)",
				self.SUCCESS + "Second most populous: Second (9)",
				self.FAILURE + "Third most populous: Third (8)",
				"Our next most populous: Fifth (6)"
			])
		finally:
			cities.kill()
	
	def test_some_no_next(self):
		city1, city2, city3 = cities = TestCities.owners(0, 0, 1)
		
		city1.setName("First", False)
		city1.setPopulation(10)
		
		city2.setName("Second", False)
		city2.setPopulation(9)
		
		city3.setName("Third", False)
		city3.setPopulation(8)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Most populous: First (10)",
				self.SUCCESS + "Second most populous: Second (9)",
				self.FAILURE + "Third most populous: Third (8)"
			])
		finally:
			cities.kill()
	
	def test_missing_cities(self):
		city1, city2 = cities = TestCities.owners(0, 0)
		
		city1.setName("First", False)
		city1.setPopulation(10)
		
		city2.setName("Second", False)
		city2.setPopulation(9)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Most populous: First (10)",
				self.SUCCESS + "Second most populous: Second (9)"
			])
		finally:
			cities.kill()
	
	def test_no_cities(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), [self.FAILURE + "Most populous: No City (0)"])
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		our_city1, our_city2, vassal_city, other_city = cities = TestCities.owners(0, 0, 1, 2)
		
		our_city1.setName("First", False)
		our_city1.setPopulation(10)
		
		our_city2.setName("Second", False)
		our_city2.setPopulation(8)
		
		vassal_city.setName("Third", False)
		vassal_city.setPopulation(5)
		
		other_city.setName("Fourth", False)
		other_city.setPopulation(4)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), [
				self.SUCCESS + "Most populous: First (10)",
				self.SUCCESS + "Second most populous: Second (8)",
				self.SUCCESS + "Third most populous: Third (5)",
				"Next most populous: Fourth (4)"
			])
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)


test_cases = [
	TestBestPopulationCities,
	TestBestPopulationPlayer,
]