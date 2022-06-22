from BestEntitiesRequirements import *

from TestVictoryCommon import *


class TestBestCultureCities(ExtendedTestCase):

	def setUp(self):
		self.requirement = BestCultureCities(3)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "BestCultureCities(3)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "BestCultureCities(3)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "the three most cultured cities in the world")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_all(self):
		city1, city2, city3, city4 = cities = TestCities.owners(0, 0, 0, 1)
		
		city1.setName("First", False)
		city1.setCulture(0, 100, False)
		
		city2.setName("Second", False)
		city2.setCulture(0, 90, False)
		
		city3.setName("Third", False)
		city3.setCulture(0, 80, False)
		
		city4.setName("Fourth", False)
		city4.setCulture(1, 70, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Most cultured: First (100)",
				self.SUCCESS + "Second most cultured: Second (90)",
				self.SUCCESS + "Third most cultured: Third (80)",
				"Next most cultured: Fourth (70)"
			])
		finally:
			cities.kill()
	
	def test_all_and_next(self):
		city1, city2, city3, city4 = cities = TestCities.owners(0, 0, 0, 0)
		
		city1.setName("First", False)
		city1.setCulture(0, 100, False)
		
		city2.setName("Second", False)
		city2.setCulture(0, 90, False)
		
		city3.setName("Third", False)
		city3.setCulture(0, 80, False)
		
		city4.setName("Fourth", False)
		city4.setCulture(0, 70, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Most cultured: First (100)",
				self.SUCCESS + "Second most cultured: Second (90)",
				self.SUCCESS + "Third most cultured: Third (80)",
				"Our next most cultured: Fourth (70)"
			])
		finally:
			cities.kill()
	
	def test_some(self):
		city1, city2, city3, city4, city5 = cities = TestCities.owners(0, 0, 1, 1, 0)
		
		city1.setName("First", False)
		city1.setCulture(0, 100, False)
		
		city2.setName("Second", False)
		city2.setCulture(0, 90, False)
		
		city3.setName("Third", False)
		city3.setCulture(1, 80, False)
		
		city4.setName("Fourth", False)
		city4.setCulture(1, 70, False)
		
		city5.setName("Fifth", False)
		city5.setCulture(0, 60, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Most cultured: First (100)",
				self.SUCCESS + "Second most cultured: Second (90)",
				self.FAILURE + "Third most cultured: Third (80)",
				"Our next most cultured: Fifth (60)"
			])
		finally:
			cities.kill()
	
	def test_some_no_next(self):
		city1, city2, city3 = cities = TestCities.owners(0, 0, 1)
		
		city1.setName("First", False)
		city1.setCulture(0, 100, False)
		
		city2.setName("Second", False)
		city2.setCulture(0, 90, False)
		
		city3.setName("Third", False)
		city3.setCulture(1, 80, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Most cultured: First (100)",
				self.SUCCESS + "Second most cultured: Second (90)",
				self.FAILURE + "Third most cultured: Third (80)"
			])
		finally:
			cities.kill()
	
	def test_missing_cities(self):
		city1, city2 = cities = TestCities.owners(0, 0)
		
		city1.setName("First", False)
		city1.setCulture(0, 100, False)
		
		city2.setName("Second", False)
		city2.setCulture(0, 90, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Most cultured: First (100)",
				self.SUCCESS + "Second most cultured: Second (90)"
			])
		finally:
			cities.kill()
	
	def test_no_cities(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), [self.FAILURE + "Most cultured: No city (0)"])
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		our_city1, our_city2, vassal_city, other_city = cities = TestCities.owners(0, 0, 1, 2)
		
		our_city1.setName("First", False)
		our_city1.setCulture(0, 100, False)
		
		our_city2.setName("Second", False)
		our_city2.setCulture(0, 80, False)
		
		vassal_city.setName("Third", False)
		vassal_city.setCulture(1, 50, False)
		
		other_city.setName("Fourth", False)
		other_city.setCulture(2, 40, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), [
				self.SUCCESS + "Most cultured: First (100)",
				self.SUCCESS + "Second most cultured: Second (80)",
				self.SUCCESS + "Third most cultured: Third (50)",
				"Next most cultured: Fourth (40)"
			])
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)


class TestBestCultureCity(ExtendedTestCase):

	def setUp(self):
		self.city = LocationCityDefinition(TestCities.CITY_LOCATIONS[0]).named("Somecity")
		self.requirement = BestCultureCity(self.city)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "BestCultureCity(Somecity)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "BestCultureCity(Somecity)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Somecity the most culturally advanced city in the world")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Somecity": plots_.of([TestCities.CITY_LOCATIONS[0]])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((61, 31)), "Somecity")
		self.assertEqual(self.requirement.area_name((62, 32)), "")
		
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_no_cities(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), [
			self.FAILURE + "Most cultured: No city (0)"
		])
	
	def test_best_city(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setName("First", False)
		our_city.setCulture(0, 100, False)
		
		their_city.setName("Second", False)
		their_city.setCulture(1, 50, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Most cultured: First (100)",
				"Next most cultured: Second (50)",
			])
		finally:
			cities.kill()
	
	def test_best_city_tied(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setName("First", False)
		our_city.setCulture(0, 100, False)
		
		their_city.setName("Second", False)
		their_city.setCulture(1, 100, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Most cultured: First (100)",
				"Next most cultured: Second (100)",
			])
		finally:
			cities.kill()
	
	def test_not_best_city(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setName("First", False)
		our_city.setCulture(0, 50, False)
		
		their_city.setName("Second", False)
		their_city.setCulture(1, 100, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.FAILURE + "Most cultured: Second (100)",
				"Our next most cultured: First (50)",
			])
		finally:
			cities.kill()
	
	def test_best_different_location(self):
		other_city, our_city, their_city = TestCities.owners(2, 0, 1)
		
		other_city.kill()
		
		our_city.setName("First", False)
		our_city.setCulture(0, 100, False)
		
		their_city.setName("Second", False)
		their_city.setCulture(1, 50, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.FAILURE + "Most cultured: First (100)",
			])
		finally:
			our_city.kill()
			their_city.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		vassal_city, our_city, their_city = cities = TestCities.owners(1, 0, 2)
		
		team(1).setVassal(0, True, False)
		
		vassal_city.setName("First", False)
		vassal_city.setCulture(1, 100, False)
		
		our_city.setName("Second", False)
		our_city.setCulture(0, 50, False)
		
		their_city.setName("Third", False)
		their_city.setCulture(2, 80, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), [
				self.SUCCESS + "Most cultured: First (100)",
				"Next most cultured: Third (80)",
			])
		finally:
			team(1).setVassal(0, False, False)
			cities.kill()
	
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
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
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
		self.assertEqual(self.requirement.progress(self.evaluator), [self.FAILURE + "Most populous: No city (0)"])
	
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


class TestBestPopulationCity(ExtendedTestCase):

	def setUp(self):
		self.city = LocationCityDefinition(TestCities.CITY_LOCATIONS[0]).named("Somecity")
		self.requirement = BestPopulationCity(self.city)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "BestPopulationCity(Somecity)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "BestPopulationCity(Somecity)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Somecity the most populous city in the world")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Somecity": plots_.of([TestCities.CITY_LOCATIONS[0]])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((61, 31)), "Somecity")
		self.assertEqual(self.requirement.area_name((62, 32)), "")
		
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_no_cities(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), [
			self.FAILURE + "Most populous: No city (0)"
		])
	
	def test_best_city(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setName("First", False)
		our_city.setPopulation(10)
		
		their_city.setName("Second", False)
		their_city.setPopulation(5)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Most populous: First (10)",
				"Next most populous: Second (5)",
			])
		finally:
			cities.kill()
	
	def test_best_city_tied(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setName("First", False)
		our_city.setPopulation(10)
		
		their_city.setName("Second", False)
		their_city.setPopulation(10)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Most populous: First (10)",
				"Next most populous: Second (10)",
			])
		finally:
			cities.kill()
	
	def test_not_best_city(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setName("First", False)
		our_city.setPopulation(5)
		
		their_city.setName("Second", False)
		their_city.setPopulation(10)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.FAILURE + "Most populous: Second (10)",
				"Our next most populous: First (5)",
			])
		finally:
			cities.kill()
	
	def test_best_different_location(self):
		other_city, our_city, their_city = TestCities.owners(2, 0, 1)
		
		other_city.kill()
		
		our_city.setName("First", False)
		our_city.setPopulation(10)
		
		their_city.setName("Second", False)
		their_city.setPopulation(5)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.FAILURE + "Most populous: First (10)",
			])
		finally:
			our_city.kill()
			their_city.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		vassal_city, our_city, their_city = cities = TestCities.owners(1, 0, 2)
		
		team(1).setVassal(0, True, False)
		
		vassal_city.setName("First", False)
		vassal_city.setPopulation(10)
		
		our_city.setName("Second", False)
		our_city.setPopulation(5)
		
		their_city.setName("Third", False)
		their_city.setPopulation(8)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), [
				self.SUCCESS + "Most populous: First (10)",
				"Next most populous: Third (8)",
			])
		finally:
			team(1).setVassal(0, False, False)
			cities.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)


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
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
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


class TestBestTechPlayer(ExtendedTestCase):

	def setUp(self):
		self.requirement = BestTechPlayer()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
		
		self.removed_techs = dict((iPlayer, infos.techs().where(team(iPlayer).isHasTech)) for iPlayer in [0, 1, 2])
		for iPlayer, techs in self.removed_techs.items():
			for iTech in techs:
				team(iPlayer).setHasTech(iTech, False, iPlayer, False, False)
		
	def tearDown(self):
		self.requirement.deregister_handlers()
		
		for iPlayer, techs in self.removed_techs.items():
			for iTech in techs:
				team(iPlayer).setHasTech(iTech, True, iPlayer, False, False)
		
	def test_str(self):
		self.assertEqual(str(self.requirement), "BestTechPlayer()")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "BestTechPlayer()")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "the most advanced civilization")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_best(self):
		team(0).setHasTech(iGenetics, True, 0, False, False)
		team(1).setHasTech(iLaw, True, 1, False, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), [self.SUCCESS + "Most advanced: Egypt (9000)", "Next most advanced: Babylonia (280)"])
		finally:
			team(0).setHasTech(iGenetics, False, 0, False, False)
			team(1).setHasTech(iLaw, False, 0, False, False)
	
	def test_second(self):
		team(0).setHasTech(iLaw, True, 0, False, False)
		team(1).setHasTech(iGenetics, True, 1, False, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [self.FAILURE + "Most advanced: Babylonia (9000)", "Our next most advanced: Egypt (280)"])
		finally:
			team(0).setHasTech(iLaw, False, 0, False, False)
			team(1).setHasTech(iGenetics, False, 0, False, False)
	
	def test_third(self):
		team(0).setHasTech(iLaw, True, 0, False, False)
		team(1).setHasTech(iGenetics, True, 1, False, False)
		team(2).setHasTech(iEconomics, True, 2, False, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [self.FAILURE + "Most advanced: Babylonia (9000)", "Our next most advanced: Egypt (280)"])
		finally:
			team(0).setHasTech(iLaw, False, 0, False, False)
			team(1).setHasTech(iGenetics, False, 1, False, False)
			team(2).setHasTech(iEconomics, False, 2, False, False)
	
	def test_multiple_players_fulfilled(self):
		requirement = BestTechPlayer(2)
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		team(0).setHasTech(iGenetics, True, 0, False, False)
		team(1).setHasTech(iEconomics, True, 1, False, False)
		team(2).setHasTech(iLaw, True, 2, False, False)
		
		try:
			self.assertEqual(requirement.fulfilled(evaluator), True)
			self.assertEqual(requirement.progress(evaluator), [self.SUCCESS + "Most advanced: Egypt (9000)", self.SUCCESS + "Second most advanced: Babylonia (1500)", "Next most advanced: Harappa (280)"])
		finally:
			team(1).setVassal(0, False, False)
			
			team(0).setHasTech(iGenetics, False, 0, False, False)
			team(1).setHasTech(iEconomics, False, 1, False, False)
			team(2).setHasTech(iLaw, False, 2, False, False)
	
	def test_multiple_players_not_fulfilled(self):
		requirement = BestTechPlayer(2)
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		team(0).setHasTech(iLaw, True, 0, False, False)
		team(1).setHasTech(iGenetics, True, 1, False, False)
		team(2).setHasTech(iEconomics, True, 2, False, False)
		
		try:
			self.assertEqual(requirement.fulfilled(evaluator), False)
			self.assertEqual(requirement.progress(evaluator), [self.SUCCESS + "Most advanced: Babylonia (9000)", self.FAILURE + "Second most advanced: Harappa (1500)", "Our next most advanced: Egypt (280)"])
		finally:
			team(1).setVassal(0, False, False)
			
			team(0).setHasTech(iLaw, False, 0, False, False)
			team(1).setHasTech(iGenetics, False, 1, False, False)
			team(2).setHasTech(iEconomics, False, 2, False, False)
	
	def test_check_tech_acquired(self):
		events.fireEvent("techAcquired", iLaw, 0, 0, False)
		
		self.assertEqual(self.goal.checked, True)
	
	def test_check_tech_acquired_other(self):
		events.fireEvent("techAcquired", iLaw, 1, 1, False)
		
		self.assertEqual(self.goal.checked, False)
	
	def test_not_checked_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, False)


test_cases = [
	TestBestCultureCities,
	TestBestCultureCity,
	TestBestPopulationCities,
	TestBestPopulationPlayer,
	TestBestPopulationCity,
	# TestBestTechPlayer,
]