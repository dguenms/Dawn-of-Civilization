from VictoryRequirements import *

from TestVictoryCommon import *


class TestBuildingCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = BuildingCount(iGranary, 3)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "BuildingCount(Granary, 3)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "BuildingCount(Granary, 3)")
	
	def test_equals(self):
		identical_requirement = BuildingCount(iGranary, 3)
		different_building = BuildingCount(iLibrary, 3)
		different_count = BuildingCount(iGranary, 4)
		
		self.assertEqual(self.requirement, identical_requirement)
		self.assertNotEqual(self.requirement, different_building)
		self.assertNotEqual(self.requirement, different_count)
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)

	def test_description(self):
		self.assertEqual(self.requirement.description(), "three Granaries")

	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Granaries: 0 / 3")

	def test_some(self):
		cities = TestCities.num(2)
	
		for city in cities:
			city.setHasRealBuilding(iGranary, True)

		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Granaries: 2 / 3")
		finally:
			cities.kill()
	
	def test_all(self):
		cities = TestCities.num(3)
		
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Granaries: 3 / 3")
		finally:
			cities.kill()
	
	def test_more(self):
		cities = TestCities.num(4)
		
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 4)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Granaries: 4 / 3")
		finally:
			cities.kill()
	
	def test_sum(self):
		requirement = BuildingCount(SumAggregate(iGranary, iLibrary), 3)
		
		city1, city2 = cities = TestCities.num(2)
		
		city1.setHasRealBuilding(iGranary, True)
		city1.setHasRealBuilding(iLibrary, True)
		city2.setHasRealBuilding(iLibrary, True)
		
		try:
			self.assertEqual(requirement.evaluate(self.evaluator), 3)
			self.assertEqual(requirement.fulfilled(self.evaluator), True)
			self.assertEqual(requirement.progress(self.evaluator), self.SUCCESS + "Granaries and Libraries: 3 / 3")
		finally:
			cities.kill()
	
	def test_average(self):
		requirement = BuildingCount(AverageAggregate(iGranary, iLibrary), 2)
		
		cities = TestCities.num(2)
		
		for city in cities:
			city.setHasRealBuilding(iLibrary, True)
		
		try:
			self.assertEqual(requirement.evaluate(self.evaluator), 1)
			self.assertEqual(requirement.fulfilled(self.evaluator), False)
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Granaries and Libraries: 1 / 2")
		finally:
			cities.kill()
	
	def test_count(self):
		requirement = BuildingCount(CountAggregate(iGranary, iLibrary), 2)
		
		cities = TestCities.num(2)
		
		for city in cities:
			city.setHasRealBuilding(iLibrary, True)
		
		try:
			self.assertEqual(requirement.evaluate(self.evaluator), 1)
			self.assertEqual(requirement.fulfilled(self.evaluator), False)
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Granaries and Libraries: 1 / 2")
		finally:
			cities.kill()
	
	def test_vassals(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		cities = TestCities.owners(0, 1, 2)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), False)
			self.assertEqual(self.requirement.progress(evaluator), self.FAILURE + "Granaries: 2 / 3")
		finally:
			cities.kill()
			
			team(1).setVassal(0, False, False)
	
	def test_allies(self):
		evaluator = AlliesEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		team(2).setDefensivePact(0, True)
		team(0).setDefensivePact(2, True)
		
		cities = TestCities.owners(0, 1, 2, 3)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Granaries: 3 / 3")
		finally:
			cities.kill()
			
			team(1).setVassal(0, False, False)
			team(2).setDefensivePact(0, False)
			team(0).setDefensivePact(2, False)
	
	def test_religion(self):
		evaluator = ReligionEvaluator(self.iPlayer)
		
		player(0).setLastStateReligion(iOrthodoxy)
		player(1).setLastStateReligion(iOrthodoxy)
		player(2).setLastStateReligion(iCatholicism)
		
		cities = TestCities.owners(0, 1, 2, 3)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), False)
			self.assertEqual(self.requirement.progress(evaluator), self.FAILURE + "Granaries: 2 / 3")
		finally:
			cities.kill()
			
			for iPlayer in [0, 1, 2]:
				player(iPlayer).setLastStateReligion(-1)
	
	def test_secular(self):
		evaluator = SecularEvaluator(self.iPlayer)
		
		player(0).setCivics(iCivicsReligion, iSecularism)
		player(1).setCivics(iCivicsReligion, iSecularism)
		
		cities = TestCities.owners(0, 1, 2)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), False)
			self.assertEqual(self.requirement.progress(evaluator), self.FAILURE + "Granaries: 2 / 3")
		finally:
			cities.kill()
			
			for iPlayer in [0, 1]:
				player(iPlayer).setCivics(iCivicsReligion, iAnimism)
	
	def test_world(self):
		evaluator = WorldEvaluator(self.iPlayer)
		
		cities = TestCities.owners(0, 1, 2)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Granaries: 3 / 3")
		finally:
			cities.kill()
	
	def test_vassals_sum(self):
		requirement = BuildingCount(SumAggregate(iGranary, iBarracks), 5)
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		our_city1, our_city2, vassal_city, other_city = cities = TestCities.owners(0, 0, 1, 2)
		
		our_city1.setHasRealBuilding(iGranary, True)
		our_city2.setHasRealBuilding(iBarracks, True)
		vassal_city.setHasRealBuilding(iGranary, True)
		vassal_city.setHasRealBuilding(iBarracks, True)
		other_city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(requirement.evaluate(evaluator), 4)
			self.assertEqual(requirement.fulfilled(evaluator), False)
			self.assertEqual(requirement.progress(evaluator), self.FAILURE + "Granaries and Barracks: 4 / 5")
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_unique_building(self):
		requirement = BuildingCount(iMonument, 2)
		
		city = TestCities.one()
		city.setHasRealBuilding(iObelisk, True)
		
		try:
			self.assertEqual(requirement.evaluate(self.evaluator), 1)
			self.assertEqual(requirement.fulfilled(self.evaluator), False)
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Monuments: 1 / 2")
		finally:	
			city.kill()
	
	def test_check_city_acquired(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("cityAcquired", 1, self.iPlayer, city, True, False)
		
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
			
	def test_check_city_acquired_other(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("cityAcquired", 1, 2, city, True, False)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_check_building_built(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("buildingBuilt", city, iGranary)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_check_building_built_unique_building(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("buildingBuilt", city, iTerrace)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_check_building_built_other_owner(self):
		city = TestCities.one(1)
		
		try:
			events.fireEvent("buildingBuilt", city, iGranary)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_check_building_built_other_building(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("buildingBuilt", city, iLibrary)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_check_building_built_aggregate(self):
		requirement = BuildingCount(SumAggregate(iGranary, iLibrary), 3)
	
		city = TestCities.one()
		
		try:
			requirement.register_handlers(self.goal)
			
			events.fireEvent("buildingBuilt", city, iGranary)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
			requirement.deregister_handlers()
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, False)


class TestControl(ExtendedTestCase):

	def setUp(self):
		self.requirement = Control(plots.of(TestCities.CITY_LOCATIONS).named("Test Area"))
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "Control(Test Area)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "Control(Test Area)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Test Area")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Test Area")
	
	def test_some(self):
		cities = TestCities.owners(0, 0, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Test Area")
		finally:
			cities.kill()
	
	def test_all(self):
		cities = TestCities.owners(0, 0, 0)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Test Area")
		finally:
			cities.kill()
	
	def test_other_evaluator_fulfilled(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		cities = TestCities.owners(0, 0, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Test Area")
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_other_evaluator_not_fulfilled(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		cities = TestCities.owners(0, 0, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), False)
			self.assertEqual(self.requirement.progress(evaluator), self.FAILURE + "Test Area")
		finally:
			cities.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)


class TestGoldAmount(ExtendedTestCase):

	def setUp(self):
		self.requirement = GoldAmount(500)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "GoldAmount(500)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "GoldAmount(500)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "500 gold")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_less(self):
		self.player.setGold(100)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold in treasury: 100 / 500")
		finally:
			self.player.setGold(0)
			
	def test_more(self):
		self.player.setGold(1000)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1000)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold in treasury: 1000 / 500")
		finally:
			self.player.setGold(0)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		player(0).setGold(100)
		player(1).setGold(200)
		player(2).setGold(500)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 300)
			self.assertEqual(self.requirement.fulfilled(evaluator), False)
			self.assertEqual(self.requirement.progress(evaluator), self.FAILURE + "Gold in treasury: 300 / 500")
		finally:
			for iPlayer in [0, 1, 2]:
				player(iPlayer).setGold(0)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)


class TestFirstDiscover(ExtendedTestCase):

	def setUp(self):
		self.requirement = FirstDiscover(iEngineering)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "FirstDiscover(Engineering)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "FirstDiscover(Engineering)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Engineering")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_discover_first(self):
		team(self.iPlayer).setHasTech(iEngineering, True, self.iPlayer, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Engineering")
			
			self.assertEqual(self.requirement.state, SUCCESS)
			self.assertEqual(self.goal.checked, True)
		finally:
			team(self.iPlayer).setHasTech(iEngineering, False, self.iPlayer, True, False)
	
	def test_discover_other(self):
		team(1).setHasTech(iEngineering, True, 1, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Engineering")
			
			self.assertEqual(self.requirement.state, FAILURE)
			self.assertEqual(self.goal.failed, True)
		finally:
			team(1).setHasTech(iEngineering, False, 1, True, False)
	
	def test_discover_after(self):
		team(1).setHasTech(iEngineering, True, 1, True, False)
		team(self.iPlayer).setHasTech(iEngineering, True, self.iPlayer, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Engineering")
			
			self.assertEqual(self.requirement.state, FAILURE)
			self.assertEqual(self.goal.failed, True)
		finally:
			team(self.iPlayer).setHasTech(iEngineering, False, self.iPlayer, True, False)
			team(1).setHasTech(iEngineering, False, 1, True, False)
	
	def test_discover_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		team(1).setHasTech(iEngineering, True, 1, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Engineering")
			
			self.assertEqual(self.requirement.state, SUCCESS)
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setHasTech(iEngineering, False, 1, True, False)
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, False)
	

class TestBrokeredPeace(ExtendedTestCase):

	def setUp(self):
		self.requirement = BrokeredPeace(2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "BrokeredPeace(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "BrokeredPeace(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_peace_brokered(self):
		events.fireEvent("peaceBrokered", self.iPlayer, 1, 2)
		events.fireEvent("peaceBrokered", self.iPlayer, 1, 2)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Peace deals brokered: 2 / 2")
		self.assertEqual(self.goal.checked, True)
	
	def test_peace_brokered_other(self):
		events.fireEvent("peaceBrokered", 1, 2, 3)
		events.fireEvent("peaceBrokered", 1, 2, 3)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Peace deals brokered: 0 / 2")
		self.assertEqual(self.goal.checked, False)
	
	def test_peace_brokered_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		try:
			events.fireEvent("peaceBrokered", 0, 2, 3)
			events.fireEvent("peaceBrokered", 1, 4, 5)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Peace deals brokered: 2 / 2")
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, False)
	
	
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
	TestBuildingCount,
	TestGoldAmount,
	TestControl,
	TestFirstDiscover,
	TestBrokeredPeace,
	TestPopulationPercent,
	TestBestPopulationPlayer,
	TestBestPopulationCities,
]