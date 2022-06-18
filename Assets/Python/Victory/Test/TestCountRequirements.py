from CountRequirements import *

from TestVictoryCommon import *


class TestAttitudeCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "AttitudeCount(Friendly, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "AttitudeCount(Friendly, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "friendly relations with two other civilizations")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Friendly relations: 0 / 2")
	
	def test_insufficient(self):
		players = [1, 2]
		for iPlayer in players:
			team(iPlayer).meet(0, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Friendly relations: 0 / 2")
		finally:
			for iPlayer in players:
				team(iPlayer).cutContact(0)
	
	def test_sufficient(self):
		players = [1, 2]
		for iPlayer in players:
			team(iPlayer).meet(0, False)
			player(iPlayer).AI_setAttitudeExtra(0, 100)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Friendly relations: 2 / 2")
		finally:
			for iPlayer in players:
				team(iPlayer).cutContact(0)
				player(iPlayer).AI_setAttitudeExtra(0, 0)
	
	def test_no_contact(self):
		players = [1, 2]
		for iPlayer in players:
			player(iPlayer).AI_setAttitudeExtra(0, 100)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Friendly relations: 0 / 2")
		finally:
			for iPlayer in players:
				player(iPlayer).AI_setAttitudeExtra(0, 0)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestAttitudeCountCommunist(ExtendedTestCase):

	def setUp(self):
		self.requirement = AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 2, bCommunist=True)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "friendly relations with two other communist civilizations")
	
	def test_communist(self):
		players = [1, 2]
		for iPlayer in players:
			team(iPlayer).meet(0, False)
			player(iPlayer).AI_setAttitudeExtra(0, 100)
			player(iPlayer).setCivics(iCivicsEconomy, iCentralPlanning)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Friendly relations: 2 / 2")
		finally:
			for iPlayer in players:
				team(iPlayer).cutContact(0)
				player(iPlayer).AI_setAttitudeExtra(0, 0)
				player(iPlayer).setCivics(iCivicsEconomy, iRedistribution)
	
	def test_not_communist(self):
		players = [1, 2]
		for iPlayer in players:
			team(iPlayer).meet(0, False)
			player(iPlayer).AI_setAttitudeExtra(0, 100)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Friendly relations: 0 / 2")
		finally:
			for iPlayer in players:
				team(iPlayer).cutContact(0)
				player(iPlayer).AI_setAttitudeExtra(0, 0)


class TestAttitudeCountCivs(ExtendedTestCase):

	def setUp(self):
		self.requirement = AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 2, civs=CivsDefinition(1, 2).named("Test Civs"))
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "friendly relations with two other civilizations in Test Civs")
	
	def test_civs(self):
		players = [1, 2]
		for iPlayer in players:
			team(iPlayer).meet(0, False)
			player(iPlayer).AI_setAttitudeExtra(0, 100)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Friendly relations: 2 / 2")
		finally:
			for iPlayer in players:
				team(iPlayer).cutContact(0)
				player(iPlayer).AI_setAttitudeExtra(0, 0)
	
	def test_other_civs(self):
		players = [7, 8]
		for iPlayer in players:
			team(iPlayer).meet(0, False)
			player(iPlayer).AI_setAttitudeExtra(0, 100)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Friendly relations: 0 / 2")
		finally:
			for iPlayer in players:
				team(iPlayer).cutContact(0)
				player(iPlayer).AI_setAttitudeExtra(0, 0)


class TestAttitudeCountIndependent(ExtendedTestCase):

	def setUp(self):
		self.requirement = AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 2, bIndependent=True)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "friendly relations with two other independent civilizations")
	
	def test_independent(self):
		players = [1, 2]
		for iPlayer in players:
			team(iPlayer).meet(0, False)
			player(iPlayer).AI_setAttitudeExtra(0, 100)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Friendly relations: 2 / 2")
		finally:
			for iPlayer in players:
				team(iPlayer).cutContact(0)
				player(iPlayer).AI_setAttitudeExtra(0, 0)
	
	def test_not_independent(self):
		players = [1, 2]
		for iPlayer in players:
			team(iPlayer).meet(0, False)
			player(iPlayer).AI_setAttitudeExtra(0, 100)
		
		team(1).setVassal(0, True, False)
		team(2).setVassal(7, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Friendly relations: 0 / 2")
		finally:
			for iPlayer in players:
				team(iPlayer).cutContact(0)
				player(iPlayer).AI_setAttitudeExtra(0, 0)


class TestAveragePopulation(ExtendedTestCase):

	def setUp(self):
		self.requirement = AveragePopulation(4)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "AveragePopulation(4)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "AveragePopulation(4)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "an average city population of four")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Average city population: 0 / 4")
	
	def test_less(self):
		city1, city2 = cities = TestCities.num(2)
		
		city1.setPopulation(4)
		city2.setPopulation(2)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Average city population: 3 / 4")
		finally:
			cities.kill()
	
	def test_more(self):
		city1, city2 = cities = TestCities.num(2)
		
		city1.setPopulation(6)
		city2.setPopulation(4)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 5)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Average city population: 5 / 4")
		finally:
			cities.kill()
	
	def test_different_owner(self):
		city1, city2 = cities = TestCities.owners(1, 1)
		
		city1.setPopulation(6)
		city2.setPopulation(4)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Average city population: 0 / 4")
		finally:
			cities.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		city1, city2 = cities = TestCities.owners(1, 1)
		
		city1.setPopulation(6)
		city2.setPopulation(4)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 5)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Average city population: 5 / 4")
		finally:
			team(1).setVassal(0, False, False)
			cities.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


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
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})

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


class TestCityCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = CityCount(plots.of(TestCities.CITY_LOCATIONS).named("Test Area"), 2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CityCount(Test Area, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CityCount(Test Area, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two cities in Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots_.of(TestCities.CITY_LOCATIONS)})
		
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((61, 31)), "Test Area")
		self.assertEqual(self.requirement.area_name((62, 32)), "")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Cities in Test Area: 0 / 2")
	
	def test_less(self):
		city = TestCities.one()
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Cities in Test Area: 1 / 2")
		finally:
			city.kill()
	
	def test_more(self):
		cities = TestCities.num(3)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Cities in Test Area: 3 / 2")
		finally:
			cities.kill()
	
	def test_other_owner(self):
		cities = TestCities.owners(0, 1, 1)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Cities in Test Area: 1 / 2")
		finally:
			cities.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		cities = TestCities.owners(0, 1, 1)
		team(1).setVassal(0, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Cities in Test Area: 3 / 2")
		finally:
			cities.kill()
	
	def test_city_built(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("cityBuilt", city)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_city_acquired_and_kept(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("cityAcquiredAndKept", self.iPlayer, city)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, False)


class TestControlledResourceCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = ControlledResourceCount(iGold, 2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ControlledResourceCount(Gold, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ControlledResourceCount(Gold, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Gold resources")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold: 0 / 2")
	
	def test_less(self):
		city = TestCities.one()
		
		city.plot().setBonusType(iGold)
		city.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold: 1 / 2")
		finally:
			city.kill()
	
	def test_sufficient(self):
		city1, city2 = cities = TestCities.num(2)
		
		for city in cities:
			city.plot().setBonusType(iGold)
		
		city1.setHasRealBuilding(iPalace, True)
		plot(62, 31).setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold: 2 / 2")
		finally:
			cities.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(2).setVassal(0, True, False)
		
		city1, city2 = cities = TestCities.owners(2, 2)
		
		for city in cities:
			city.plot().setBonusType(iGold)
		
		city1.setHasRealBuilding(iPalace, True)
		plot(62, 31).setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Gold: 2 / 2")
		finally:
			cities.kill()
			team(2).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestCorporationCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = CorporationCount(iTradingCompany, 3)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CorporationCount(Trading Company, 3)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CorporationCount(Trading Company, 3)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Trading Company to three of your cities")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Trading Company: 0 / 3")
	
	def test_fewer(self):
		city = TestCities.one()
		city.setHasCorporation(iTradingCompany, True, False, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Trading Company: 1 / 3")
		finally:
			city.kill()
	
	def test_more(self):
		cities = TestCities.num(4)
		for city in cities:
			city.setHasCorporation(iTradingCompany, True, False, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 4)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Trading Company: 4 / 3")
		finally:
			cities.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		cities = TestCities.owners(1, 1, 1)
		for city in cities:
			city.setHasCorporation(iTradingCompany, True, False, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Trading Company: 3 / 3")
		finally:
			cities.kill()
	
	def test_check_corporation_spread(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("corporationSpread", iTradingCompany, 0, city)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_check_corporation_spread_different_corporation(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("corporationSpread", iSilkRoute, 0, city)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_check_corporation_spread_different_owner(self):
		city = TestCities.one(1)
		
		try:
			events.fireEvent("corporationSpread", iTradingCompany, 1, city)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestCultureCity(ExtendedTestCase):

	def setUp(self):
		self.requirement = CultureCity(1000)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CultureCity(1000)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CultureCity(1000)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "a city with 1000 culture")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "No cities")
	
	def test_less(self):
		city1, city2 = cities = TestCities.num(2)
		
		city1.setName("First", False)
		city2.setName("Second", False)
		
		city1.setCulture(0, 100, True)
		city2.setCulture(0, 200, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 200)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Culture in Second: 200 / 1000")
		finally:
			cities.kill()
	
	def test_more(self):
		city1, city2 = cities = TestCities.num(2)
		
		city1.setName("First", False)
		city2.setName("Second", False)
		
		city1.setCulture(0, 500, True)
		city2.setCulture(0, 1500, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1500)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Culture in Second: 1500 / 1000")
		finally:
			cities.kill()
	
	def test_other_owner(self):
		city = TestCities.one(1)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "No cities")
		finally:
			city.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestCultureLevelCityCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = CultureLevelCityCount(iCultureLevelRefined, 3)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CultureLevelCityCount(Refined, 3)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CultureLevelCityCount(Refined, 3)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "three cities with refined culture")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_no_cities(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), [self.FAILURE + "No cities"])
	
	def test_single_city_insufficient(self):
		city = TestCities.one()
		
		city.setName("First", False)
		city.setCulture(0, game.getCultureThreshold(iCultureLevelDeveloping), True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.FAILURE + "Culture in First: 100 / 1000",
				self.FAILURE + "No second city",
				self.FAILURE + "No third city",
			])
		finally:
			city.kill()
	
	def test_single_city_sufficient(self):
		city = TestCities.one()
		
		city.setName("First", False)
		city.setCulture(0, game.getCultureThreshold(iCultureLevelRefined), True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Culture in First: 1000 / 1000",
				self.FAILURE + "No second city",
				self.FAILURE + "No third city",
			])
		finally:
			city.kill()
	
	def test_enough_cities_some_sufficient(self):
		city1, city2, city3 = cities = TestCities.num(3)
		
		city1.setName("First", False)
		city1.setCulture(0, game.getCultureThreshold(iCultureLevelInfluential), True)
		
		city2.setName("Second", False)
		city2.setCulture(0, game.getCultureThreshold(iCultureLevelRefined), True)
		
		city3.setName("Third", False)
		city3.setCulture(0, game.getCultureThreshold(iCultureLevelDeveloping), True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Culture in First: 5000 / 1000",
				self.SUCCESS + "Culture in Second: 1000 / 1000",
				self.FAILURE + "Culture in Third: 100 / 1000",
			])
		finally:
			cities.kill()
	
	def test_enough_cities_all_sufficient(self):
		city1, city2, city3 = cities = TestCities.num(3)
		
		city1.setName("First", False)
		city1.setCulture(0, game.getCultureThreshold(iCultureLevelInfluential), True)
		
		city2.setName("Second", False)
		city2.setCulture(0, game.getCultureThreshold(iCultureLevelInfluential), True)
		
		city3.setName("Third", False)
		city3.setCulture(0, game.getCultureThreshold(iCultureLevelRefined), True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Culture in First: 5000 / 1000",
				self.SUCCESS + "Culture in Second: 5000 / 1000",
				self.SUCCESS + "Culture in Third: 1000 / 1000",
			])
		finally:
			cities.kill()
	
	def test_different_owner(self):
		city = TestCities.one(1)
		
		city.setName("First", False)
		city.setCulture(0, game.getCultureThreshold(iCultureLevelRefined), True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [self.FAILURE + "No cities"])
		finally:
			city.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestImprovementCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = ImprovementCount(iCottage, 2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ImprovementCount(Cottage, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ImprovementCount(Cottage, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Cottages")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Cottages: 0 / 2")
	
	def test_fewer(self):
		area = plots_.of([(61, 31)])
		for plot in area:
			plot.setOwner(0)
			plot.setImprovementType(iCottage)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Cottages: 1 / 2")
		finally:
			for plot in area:
				plot.setOwner(-1)
				plot.setImprovementType(-1)
	
	def test_more(self):
		area = plots_.rectangle((61, 31), (63, 31))
		for plot in area:
			plot.setOwner(0)
			plot.setImprovementType(iCottage)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Cottages: 3 / 2")
		finally:
			for plot in area:
				plot.setOwner(-1)
				plot.setImprovementType(-1)
	
	def test_other_owner(self):
		area = plots_.rectangle((61, 31), (62, 31))
		for plot in area:
			plot.setOwner(1)
			plot.setImprovementType(iCottage)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Cottages: 0 / 2")
		finally:
			for plot in area:
				plot.setOwner(-1)
				plot.setImprovementType(-1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		area = plots_.rectangle((61, 31), (62, 31))
		for plot in area:
			plot.setOwner(1)
			plot.setImprovementType(iCottage)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Cottages: 2 / 2")
		finally:
			for plot in area:
				plot.setOwner(-1)
				plot.setImprovementType(-1)
			
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestOpenBorderCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = OpenBorderCount(2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "OpenBorderCount(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "OpenBorderCount(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "open border agreements with two civilizations")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})

	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Open border agreements: 0 / 2")
	
	def test_insufficient(self):
		team(0).setOpenBorders(1, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Open border agreements: 1 / 2")
		finally:
			team(0).setOpenBorders(1, False)
	
	def test_sufficient(self):
		players = [1, 2]
		for iPlayer in players:
			team(0).setOpenBorders(iPlayer, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Open border agreements: 2 / 2")
		finally:
			for iPlayer in players:
				team(0).setOpenBorders(iPlayer, False)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		players = [7, 8]
		for iPlayer in players:
			team(0).setOpenBorders(iPlayer, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Open border agreements: 2 / 2")
		finally:
			for iPlayer in players:
				team(0).setOpenBorders(iPlayer, False)
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestOpenBorderCountCivs(ExtendedTestCase):

	def setUp(self):
		self.requirement = OpenBorderCount(2, civs=CivsDefinition(1, 2).named("Test Civs"))
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "OpenBorderCount(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "OpenBorderCount(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "open border agreements with two Test Civs civilizations")
	
	def test_with_civs(self):
		players = [1, 2]
		for iPlayer in players:
			team(0).setOpenBorders(iPlayer, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Open border agreements: 2 / 2")
		finally:
			for iPlayer in players:
				team(0).setOpenBorders(iPlayer, False)
	
	def test_with_other_civs(self):
		players = [7, 8]
		for iPlayer in players:
			team(0).setOpenBorders(iPlayer, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Open border agreements: 0 / 2")
		finally:
			for iPlayer in players:
				team(0).setOpenBorders(iPlayer, False)


class TestPopulationCityCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = PopulationCityCount(10, 3)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
		
	def test_str(self):
		self.assertEqual(str(self.requirement), "PopulationCityCount(10, 3)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "PopulationCityCount(10, 3)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "three cities with a population of ten")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_no_cities(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), [self.FAILURE + "No cities"])
	
	def test_single_city_insufficient(self):
		city = TestCities.one()
		
		city.setName("First", False)
		city.setPopulation(8)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.FAILURE + "Population in First: 8 / 10",
				self.FAILURE + "No second city",
				self.FAILURE + "No third city",
			])
		finally:
			city.kill()
	
	def test_single_city_sufficient(self):
		city = TestCities.one()
		
		city.setName("First", False)
		city.setPopulation(12)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Population in First: 12 / 10",
				self.FAILURE + "No second city",
				self.FAILURE + "No third city",
			])
		finally:
			city.kill()
	
	def test_enough_cities_some_sufficient(self):
		city1, city2, city3 = cities = TestCities.num(3)
		
		city1.setName("First", False)
		city1.setPopulation(12)
		
		city2.setName("Second", False)
		city2.setPopulation(10)
		
		city3.setName("Third", False)
		city3.setPopulation(8)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Population in First: 12 / 10",
				self.SUCCESS + "Population in Second: 10 / 10",
				self.FAILURE + "Population in Third: 8 / 10",
			])
		finally:
			cities.kill()
	
	def test_enough_cities_all_sufficient(self):
		city1, city2, city3 = cities = TestCities.num(3)
		
		city1.setName("First", False)
		city1.setPopulation(14)
		
		city2.setName("Second", False)
		city2.setPopulation(12)
		
		city3.setName("Third", False)
		city3.setPopulation(10)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), [
				self.SUCCESS + "Population in First: 14 / 10",
				self.SUCCESS + "Population in Second: 12 / 10",
				self.SUCCESS + "Population in Third: 10 / 10",
			])
		finally:
			cities.kill()
	
	def test_different_owner(self):
		city = TestCities.one(1)
		
		city.setName("First", False)
		city.setPopulation(12)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), [self.FAILURE + "No cities"])
		finally:
			city.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestPopulationCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = PopulationCount(5)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "PopulationCount(5)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "PopulationCount(5)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "a total population of five")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Total Population: 0 / 5")
	
	def test_less(self):
		city = TestCities.one()
		city.setPopulation(4)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 4)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Total Population: 4 / 5")
		finally:
			city.kill()
	
	def test_more(self):
		city = TestCities.one()
		city.setPopulation(6)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 6)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Total Population: 6 / 5")
		finally:
			city.kill()
	
	def test_multiple_cities(self):
		cities = TestCities.num(2)
		
		for city in cities:
			city.setPopulation(3)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 6)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Total Population: 6 / 5")
		finally:
			cities.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		our_city, vassal_city = cities = TestCities.owners(0, 1)
		
		our_city.setPopulation(4)
		vassal_city.setPopulation(3)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 7)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Total Population: 7 / 5")
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)


class TestResourceCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = ResourceCount(iGold, 2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ResourceCount(Gold, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ResourceCount(Gold, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Gold resources")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Available Gold resources: 0 / 2")
	
	def test_less(self):
		city = TestCities.one()
		
		city.plot().setBonusType(iGold)
		city.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Available Gold resources: 1 / 2")
		finally:
			city.plot().setBonusType(-1)
			city.kill()
	
	def test_sufficient(self):
		city1, city2 = cities = TestCities.num(2)
		
		for city in cities:
			city.plot().setBonusType(iGold)
		
		city1.setHasRealBuilding(iPalace, True)
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Available Gold resources: 2 / 2")
		finally:
			for city in cities:
				city.plot().setBonusType(-1)
			cities.kill()
			
			plot(62, 31).setRouteType(-1)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestSpecialistCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = SpecialistCount(iSpecialistGreatScientist, 2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "SpecialistCount(Great Scientist, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "SpecialistCount(Great Scientist, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Great Scientists in your cities")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
		
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Great Scientists: 0 / 2")
	
	def test_less(self):
		city = TestCities.one()
		city.setFreeSpecialistCount(iSpecialistGreatScientist, 1)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Great Scientists: 1 / 2")
		finally:
			city.kill()
	
	def test_more(self):
		city = TestCities.one()
		city.setFreeSpecialistCount(iSpecialistGreatScientist, 3)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Great Scientists: 3 / 2")
		finally:
			city.kill()
	
	def test_multiple_cities(self):
		cities = TestCities.num(2)
		for city in cities:
			city.setFreeSpecialistCount(iSpecialistGreatScientist, 1)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Great Scientists: 2 / 2")
		finally:
			cities.kill()
	
	def test_different_owner(self):
		city = TestCities.one(1)
		city.setFreeSpecialistCount(iSpecialistGreatScientist, 2)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Great Scientists: 0 / 2")
		finally:
			city.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		city = TestCities.one(1)
		city.setFreeSpecialistCount(iSpecialistGreatScientist, 2)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Great Scientists: 2 / 2")
		finally:
			city.kill()
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestUnitCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = UnitCount(iSwordsman, 3)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "UnitCount(Swordsman, 3)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "UnitCount(Swordsman, 3)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "three Swordsmen")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Swordsmen: 0 / 3")
	
	def test_fewer(self):
		unit = makeUnit(0, iSwordsman, (10, 10))
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Swordsmen: 1 / 3")
		finally:
			unit.kill(False, -1)
	
	def test_more(self):
		units = makeUnits(0, iSwordsman, (10, 10), 4)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 4)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Swordsmen: 4 / 3")
		finally:
			for unit in units:
				unit.kill(False, -1)
	
	def test_unique_unit(self):
		units = makeUnits(0, iLegion, (10, 10), 4)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 4)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Swordsmen: 4 / 3")
		finally:
			for unit in units:
				unit.kill(False, -1)
	
	def test_unique_unit_required(self):
		requirement = UnitCount(iLegion, 3)
		
		units = makeUnits(0, iSwordsman, (10, 10), 4)
		
		try:
			self.assertEqual(requirement.evaluate(self.evaluator), 4)
			self.assertEqual(requirement.fulfilled(self.evaluator), True)
			self.assertEqual(requirement.progress(self.evaluator), self.SUCCESS + "Legions: 4 / 3")
		finally:
			for unit in units:
				unit.kill(False, -1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		units = makeUnits(1, iSwordsman, (10, 10), 4)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 4)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Swordsmen: 4 / 3")
		finally:
			team(1).setVassal(0, False, False)
			for unit in units:
				unit.kill(False, -1)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestVassalCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = VassalCount(2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "VassalCount(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "VassalCount(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two vassals")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Vassals: 0 / 2")
		self.assertEqual(self.goal.checked, False)
	
	def test_fewer(self):
		self.assertEqual(team(1).isVassal(0), False)
		team(1).setVassal(0, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Vassals: 1 / 2")
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_sufficient(self):
		vassals = [1, 2]
		for iVassal in vassals:
			team(iVassal).setVassal(0, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Vassals: 2 / 2")
			self.assertEqual(self.goal.checked, True)
		finally:
			for iVassal in vassals:
				team(iVassal).setVassal(0, False, False)
	
	def test_other_evaluator(self):
		evaluator = ReligionEvaluator(self.iPlayer)
		
		player(0).setLastStateReligion(iOrthodoxy)
		player(1).setLastStateReligion(iOrthodoxy)
		
		team(7).setVassal(1, True, False)
		team(8).setVassal(1, True, False)
		
		try:
			self.assertEqual(team(1).isVassal(0), False)
			self.assertEqual(team(7).isVassal(1), True)
			self.assertEqual(team(8).isVassal(1), True)
		
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Vassals: 2 / 2")
			self.assertEqual(self.goal.checked, True)
		finally:
			team(7).setVassal(1, False, False)
			team(8).setVassal(1, False, False)
			
			player(0).setLastStateReligion(-1)
			player(1).setLastStateReligion(-1)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestVassalCountCivs(ExtendedTestCase):

	def setUp(self):
		self.requirement = VassalCount(2, civs=CivsDefinition(1, 2).named("Test Civs"))
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two vassals in Test Civs")
	
	def test_in_civs(self):
		team(1).setVassal(0, True, False)
		team(2).setVassal(0, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Vassals in Test Civs: 2 / 2")
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setVassal(0, False, False)
			team(2).setVassal(0, False, False)
	
	def test_not_in_civs(self):
		team(7).setVassal(0, True, False)
		team(8).setVassal(0, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Vassals in Test Civs: 0 / 2")
			self.assertEqual(self.goal.checked, True)
		finally:
			team(7).setVassal(0, False, False)
			team(8).setVassal(0, False, False)


class TestVassalCountStateReligion(ExtendedTestCase):

	def setUp(self):
		self.requirement = VassalCount(2, iStateReligion=iOrthodoxy)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Orthodox vassals")
	
	def test_with_state_religion(self):
		vassals = [1, 2]
		for iVassal in vassals:
			team(iVassal).setVassal(0, True, False)
			player(iVassal).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Orthodox vassals: 2 / 2")
			self.assertEqual(self.goal.checked, True)
		finally:
			for iVassal in vassals:
				team(iVassal).setVassal(0, False, False)
				player(iVassal).setLastStateReligion(-1)
	
	def test_without_state_religion(self):
		team(1).setVassal(0, True, False)
		team(2).setVassal(0, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Orthodox vassals: 0 / 2")
		finally:
			team(1).setVassal(0, False, False)
			team(2).setVassal(0, False, False)
	
	def test_check_vassal_before_state_religion(self):
		team(1).setVassal(0, True, False)
		
		try:
			self.assertEqual(self.goal.checked, True)
			
			self.goal.checked = False
			player(1).setLastStateReligion(iOrthodoxy)
			
			try:
				self.assertEqual(self.goal.checked, True)
			finally:
				player(1).setLastStateReligion(-1)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_check_vassal_after_state_religion(self):
		player(1).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(self.goal.checked, True)
			
			self.goal.checked = False
			team(1).setVassal(0, True, False)
			
			try:
				self.assertEqual(self.goal.checked, True)
			finally:
				team(1).setVassal(0, False, False)
		finally:
			player(1).setLastStateReligion(-1)
	
	def test_not_check_different_state_religion(self):
		player(1).setLastStateReligion(iCatholicism)
		
		try:
			self.assertEqual(self.goal.checked, False)
		finally:
			player(1).setLastStateReligion(-1)


test_cases = [
	TestAttitudeCount,
	TestAttitudeCountCivs,
	TestAttitudeCountCommunist,
	TestAttitudeCountIndependent,
	TestAveragePopulation,
	TestBuildingCount,
	TestCityCount,
	TestCorporationCount,
	TestControlledResourceCount,
	TestCultureCity,
	TestCultureLevelCityCount,
	TestImprovementCount,
	TestOpenBorderCount,
	TestOpenBorderCountCivs,
	TestPopulationCityCount,
	TestPopulationCount,
	TestResourceCount,
	TestSpecialistCount,
	TestUnitCount,
	TestVassalCount,
	TestVassalCountCivs,
	TestVassalCountStateReligion,
]