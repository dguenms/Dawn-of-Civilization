from PercentRequirements import *

from TestVictoryCommon import *


class TestLandPercent(ExtendedTestCase):

	def setUp(self):
		self.requirement = LandPercent(10)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "LandPercent(10%)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "LandPercent(10%)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "10% of the world")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_sufficient(self):
		territory = plots_.all().land().limit(11 * 32)
		for plot in territory:
			plot.setOwner(self.iPlayer)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 11 * 32)
			self.assertAlmostEqual(self.requirement.percentage(self.evaluator), 10.89, places=2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "World territory controlled: 10.89% / 10%")
		finally:
			for plot in territory:
				plot.setOwner(-1)
	
	def test_insufficient(self):
		territory = plots_.all().land().limit(32)
		for plot in territory:
			plot.setOwner(self.iPlayer)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 32)
			self.assertAlmostEqual(self.requirement.percentage(self.evaluator), 0.99, places=2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "World territory controlled: 0.99% / 10%")
		finally:
			for plot in territory:
				plot.setOwner(-1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
	
		our_territory, vassal_territory = plots_.all().land().limit(11 * 32).percentage_split(60)
		for plot in our_territory:
			plot.setOwner(self.iPlayer)
		
		for plot in vassal_territory:
			plot.setOwner(1)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 11 * 32)
			self.assertAlmostEqual(self.requirement.percentage(evaluator), 10.89, places=2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "World territory controlled: 10.89% / 10%")
		finally:
			for plot in our_territory + vassal_territory:
				plot.setOwner(-1)
			
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)

	
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
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_sufficient(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setPopulation(10)
		their_city.setPopulation(10)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 10)
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
			self.assertEqual(self.requirement.evaluate(self.evaluator), 5)
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
			self.assertEqual(self.requirement.evaluate(evaluator), 15)
			self.assertEqual(self.requirement.percentage(evaluator), 75.0)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Percentage of world population: 75.00% / 30%")
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)


class TestReligionSpreadPercent(ExtendedTestCase):

	def setUp(self):
		self.requirement = ReligionSpreadPercent(iOrthodoxy, 30)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ReligionSpreadPercent(Orthodoxy, 30%)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ReligionSpreadPercent(Orthodoxy, 30%)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Orthodoxy to 30% of the world's population")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_spread(self):
		city1, city2 = cities = TestCities.num(2)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasReligion(iOrthodoxy, True, False, False)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(self.requirement.percentage(self.evaluator), 50.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Orthodoxy spread: 50.00% / 30%")
		finally:
			cities.kill()
			player(0).setLastStateReligion(-1)
	
	def test_no_state_religion(self):
		city1, city2 = cities = TestCities.num(2)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasReligion(iOrthodoxy, True, False, False)
		
		try:
			self.assertEqual(self.requirement.percentage(self.evaluator), 25.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Orthodoxy spread: 25.00% / 30%")
		finally:
			cities.kill()
	
	def test_additional_religion_present(self):
		city1, city2 = cities = TestCities.num(2)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasReligion(iOrthodoxy, True, False, False)
		city2.setHasReligion(iCatholicism, True, False, False)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(self.requirement.percentage(self.evaluator), 50.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Orthodoxy spread: 50.00% / 30%")
		finally:
			cities.kill()
			player(0).setLastStateReligion(-1)
	
	def test_different_owner(self):
		city1, city2 = cities = TestCities.owners(1, 0)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasReligion(iOrthodoxy, True, False, False)
		
		player(1).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(self.requirement.percentage(self.evaluator), 50.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Orthodoxy spread: 50.00% / 30%")
		finally:
			cities.kill()
			player(1).setLastStateReligion(-1)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


test_cases = [
	TestLandPercent,
	TestPopulationPercent,
	TestReligionSpreadPercent,
]