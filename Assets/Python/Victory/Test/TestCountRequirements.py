from CountRequirements import *

from TestVictoryCommon import *


class TestAttitudeCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 2).create()
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
		self.requirement = AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 2, bCommunist=True).create()
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
		self.requirement = AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 2, civs=CivsArgument(1, 2).named("Test Civs")).create()
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
		self.requirement = AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 2, bIndependent=True).create()
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


class TestAttitudeCountReligion(ExtendedTestCase):

	def setUp(self):
		self.requirement = AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 2, iReligion=iJudaism).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "friendly relations with two other civilizations with Judaism in their cities")
	
	def test_religion_present(self):
		players = [1, 2]
		for iPlayer in players:
			team(iPlayer).meet(0, False)
			player(iPlayer).AI_setAttitudeExtra(0, 100)
			
		city1, city2 = cities = TestCities.owners(1, 2)
		
		city1.setHasReligion(iJudaism, True, False, False)
		city2.setHasReligion(iJudaism, True, False, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Friendly relations: 2 / 2")
		finally:
			for iPlayer in players:
				team(iPlayer).cutContact(0)
				player(iPlayer).AI_setAttitudeExtra(0, 0)
			
			cities.kill()
	
	def test_religion_not_present(self):
		players = [1, 2]
		for iPlayer in players:
			team(iPlayer).meet(0, False)
			player(iPlayer).AI_setAttitudeExtra(0, 100)
		
		cities = TestCities.owners(1, 2)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Friendly relations: 0 / 2")
		finally:
			for iPlayer in players:
				team(iPlayer).cutContact(0)
				player(iPlayer).AI_setAttitudeExtra(0, 0)
			
			cities.kill()
	
	def test_religion_no_cities(self):
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


class TestAttitudeCountStateReligion(ExtendedTestCase):

	def setUp(self):
		self.requirement = AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 2, iStateReligion=iCatholicism).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "friendly relations with two other Catholic civilizations")
	
	def test_with_state_religion(self):
		players = [1, 2]
		for iPlayer in players:
			team(iPlayer).meet(0, False)
			player(iPlayer).setLastStateReligion(iCatholicism)
			player(iPlayer).AI_setAttitudeExtra(0, 100)
			
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Friendly relations: 2 / 2")
		finally:
			for iPlayer in players:
				team(iPlayer).cutContact(0)
				player(iPlayer).setLastStateReligion(-1)
				player(iPlayer).AI_setAttitudeExtra(0, 100)
	
	def test_without_state_religion(self):
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


class TestAveragePopulation(ExtendedTestCase):

	def setUp(self):
		self.requirement = AveragePopulation(4).create()
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
		self.requirement = BuildingCount(iMarket, 3).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "BuildingCount(Market, 3)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "BuildingCount(Market, 3)")
	
	def test_equals(self):
		identical_requirement = BuildingCount(iMarket, 3)
		different_building = BuildingCount(iGranary, 3)
		different_count = BuildingCount(iMarket, 4)
		
		self.assertEqual(self.requirement, identical_requirement)
		self.assertNotEqual(self.requirement, different_building)
		self.assertNotEqual(self.requirement, different_count)
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)

	def test_description(self):
		self.assertEqual(self.requirement.description(), "three Markets")
	
	def test_description_wonder(self):
		requirement = BuildingCount(iPyramids, 1)
		
		self.assertEqual(requirement.description(), "the Pyramids")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})

	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Markets: 0 / 3")

	def test_some(self):
		cities = TestCities.num(2)
	
		for city in cities:
			city.setHasRealBuilding(iMarket, True)

		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Markets: 2 / 3")
		finally:
			cities.kill()
	
	def test_all(self):
		cities = TestCities.num(3)
		
		for city in cities:
			city.setHasRealBuilding(iMarket, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Markets: 3 / 3")
		finally:
			cities.kill()
	
	def test_more(self):
		cities = TestCities.num(4)
		
		for city in cities:
			city.setHasRealBuilding(iMarket, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 4)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Markets: 4 / 3")
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
	
	def test_state_religion_building(self):
		state_religion_temple = StateReligionBuildingArgument(temple).named("State religion temples")
		requirement = BuildingCount(state_religion_temple, 2)
		
		cities = TestCities.num(2)
		for city in cities:
			city.setHasRealBuilding(iBuddhistTemple, True)
		
		player(0).setLastStateReligion(iBuddhism)
		
		try:
			self.assertEqual(requirement.evaluate(self.evaluator), 2)
			self.assertEqual(requirement.fulfilled(self.evaluator), True)
			self.assertEqual(requirement.progress(self.evaluator), self.SUCCESS + "State religion temples: 2 / 2")
		finally:
			cities.kill()
			player(0).setLastStateReligion(-1)
	
	def test_different_state_religion_building(self):
		state_religion_temple = StateReligionBuildingArgument(temple).named("State religion temples")
		requirement = BuildingCount(state_religion_temple, 2)
		
		cities = TestCities.num(2)
		for city in cities:
			city.setHasRealBuilding(iBuddhistTemple, True)
		
		player(0).setLastStateReligion(iHinduism)
		
		try:
			self.assertEqual(requirement.evaluate(self.evaluator), 0)
			self.assertEqual(requirement.fulfilled(self.evaluator), False)
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "State religion temples: 0 / 2")
		finally:
			cities.kill()
			player(0).setLastStateReligion(-1)
	
	def test_state_religion_building_no_state_religion(self):
		state_religion_temple = StateReligionBuildingArgument(temple).named("State religion temples")
		requirement = BuildingCount(state_religion_temple, 2)
		
		cities = TestCities.num(2)
		for city in cities:
			city.setHasRealBuilding(iBuddhistTemple, 2)
		
		try:
			self.assertEqual(requirement.evaluate(self.evaluator), 0)
			self.assertEqual(requirement.fulfilled(self.evaluator), False)
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "State religion temples: 0 / 2")
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
			city.setHasRealBuilding(iMarket, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), False)
			self.assertEqual(self.requirement.progress(evaluator), self.FAILURE + "Markets: 2 / 3")
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
			city.setHasRealBuilding(iMarket, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Markets: 3 / 3")
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
			city.setHasRealBuilding(iMarket, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), False)
			self.assertEqual(self.requirement.progress(evaluator), self.FAILURE + "Markets: 2 / 3")
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
			city.setHasRealBuilding(iMarket, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), False)
			self.assertEqual(self.requirement.progress(evaluator), self.FAILURE + "Markets: 2 / 3")
		finally:
			cities.kill()
			
			for iPlayer in [0, 1]:
				player(iPlayer).setCivics(iCivicsReligion, iAnimism)
	
	def test_world(self):
		evaluator = WorldEvaluator(self.iPlayer)
		
		cities = TestCities.owners(0, 1, 2)
		for city in cities:
			city.setHasRealBuilding(iMarket, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Markets: 3 / 3")
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
			events.fireEvent("buildingBuilt", city, iMarket)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_check_building_built_unique_building(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("buildingBuilt", city, iForum)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_check_building_built_other_owner(self):
		city = TestCities.one(1)
		
		try:
			events.fireEvent("buildingBuilt", city, iMarket)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_check_building_built_other_building(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("buildingBuilt", city, iGranary)
			
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
		
	def test_check_building_built_unique_building_requirement(self):
		requirement = BuildingCount(iObelisk, 3)
		
		city = TestCities.one()
		
		try:
			requirement.register_handlers(self.goal)
			
			events.fireEvent("buildingBuilt", city, iObelisk)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
			requirement.deregister_handlers()
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, False)


class TestCityBuildingCount(ExtendedTestCase):

	def setUp(self):
		self.city = LocationCityArgument(TestCities.CITY_LOCATIONS[0]).named("Test City")
		self.requirement = CityBuildingCount(self.city, iGranary, 1).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CityBuildingCount(Test City, Granary, 1)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CityBuildingCount(Test City, Granary, 1)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "a Granary")
	
	def test_description_wonder(self):
		requirement = CityBuildingCount(self.city, iPyramids, 1)
		
		self.assertEqual(requirement.description(), "the Pyramids")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test City": plots.of([TestCities.CITY_LOCATIONS[0]])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((57, 35)), "Test City")
		self.assertEqual(self.requirement.area_name((58, 36)), "")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_no_city(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "No city")
	
	def test_city_no_building(self):
		city = TestCities.one()
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Granary in %s" % city.getName())
		finally:
			city.kill()
	
	def test_city_building(self):
		city = TestCities.one()
		city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Granary in %s" % city.getName())
		finally:
			city.kill()
	
	def test_city_building_different_owner(self):
		city = TestCities.one(1)
		city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Granary in %s (controlled by Babylonia)" % city.getName())
		finally:
			city.kill()
	
	def test_city_building_different_location(self):
		other_city, city = cities = TestCities.num(2)
		
		city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Granary in %s" % other_city.getName())
		finally:
			cities.kill()
	
	def test_city_unique_building(self):
		requirement = CityBuildingCount(LocationCityArgument(TestCities.CITY_LOCATIONS[0]).named("Test City"), iMonument, 1)
		
		city = TestCities.one()
		city.setHasRealBuilding(iObelisk, True)
		
		try:
			self.assertEqual(requirement.fulfilled(self.evaluator), True)
			self.assertEqual(requirement.progress(self.evaluator), self.SUCCESS + "Monument in %s" % city.getName())
		finally:
			city.kill()
	
	def test_aggregate(self):
		requirement = CityBuildingCount(LocationCityArgument(TestCities.CITY_LOCATIONS[0]).named("Test City"), SumAggregate(iGranary, iLibrary, iWalls), 3)
		
		city = TestCities.one()
		for iBuilding in [iGranary, iLibrary, iWalls]:
			city.setHasRealBuilding(iBuilding, True)
		
		try:
			self.assertEqual(requirement.fulfilled(self.evaluator), True)
			self.assertEqual(requirement.progress(self.evaluator), self.SUCCESS + "Granary, Library and Walls in %s: 3 / 3" % city.getName())
		finally:
			city.kill()
	
	def test_different_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
	
		city = TestCities.one(1)
		city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Granary in %s" % city.getName())
		finally:
			city.kill()
	
	def test_check_city_acquired(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("cityAcquired", 1, self.iPlayer, city, True, False)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_check_city_acquired_different_city(self):
		city, other_city = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityAcquired", 1, self.iPlayer, other_city, True, False)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			cities.kill()
	
	def test_check_building_built(self):
		city = TestCities.one()
	
		try:
			events.fireEvent("buildingBuilt", city, iGranary)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_check_building_built_different_city(self):
		city, other_city = cities = TestCities.num(2)
		
		try:
			events.fireEvent("buildingBuilt", other_city, iGranary)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			cities.kill()
	
	def test_check_building_built_different_building(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("buildingBuilt", city, iLibrary)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_expire_building_built_wonder(self):
		requirement = CityBuildingCount(LocationCityArgument(TestCities.CITY_LOCATIONS[0]), iPyramids, 1)
		goal = TestGoal()
		
		requirement.register_handlers(goal)
	
		city = TestCities.one(1)
		
		try:
			self.assertEqual(city.getOwner(), 1)
			events.fireEvent("buildingBuilt", city, iPyramids)
			
			self.assertEqual(goal.failed, True)
		finally:
			city.kill()
			requirement.deregister_handlers()
	
	def test_expire_building_built_different_wonder(self):
		requirement = CityBuildingCount(LocationCityArgument(TestCities.CITY_LOCATIONS[0]), iPyramids, 1)
		
		city = TestCities.one(1)
		
		try:
			events.fireEvent("buildingBuilt", city, iHangingGardens)
			
			self.assertEqual(self.goal.failed, False)
		finally:
			city.kill()
	
	def test_expire_building_built_not_wonder(self):
		city = TestCities.one(1)
		
		try:
			events.fireEvent("buildingBuilt", city, iGranary)
			
			self.assertEqual(self.goal.failed, False)
		finally:
			city.kill()


class TestCityCount(ExtendedTestCase):

	def setUp(self):
		self.area = AreaArgumentFactory().of(TestCities.CITY_LOCATIONS).named("Test Area")
		self.requirement = CityCount(self.area, 2).create()
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
	
	def test_description_single(self):
		requirement = CityCount(self.area, 1)
		
		self.assertEqual(requirement.description(), "a city in Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots.of(TestCities.CITY_LOCATIONS)})
		
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((57, 35)), "Test Area")
		self.assertEqual(self.requirement.area_name((58, 36)), "")
	
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
		self.requirement = ControlledResourceCount(iGold, 2).create()
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
		plot(58, 35).setRouteType(iRouteRoad)
		
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
		self.requirement = CorporationCount(iTradingCompany, 3).create()
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
		self.requirement = CultureCity(1000).create()
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
		self.requirement = CultureLevelCityCount(iCultureLevelRefined, 3).create()
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


class TestFeatureCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = FeatureCount(iForest, 20).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "FeatureCount(Forest, 20)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "FeatureCount(Forest, 20)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "20 Forest tiles")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_fewer(self):
		controlled = plots.all().where(lambda plot: plot.getFeatureType() == iForest).limit(10) + plots.all().where(lambda plot: plot.getFeatureType() != iForest).limit(30)
		for plot in controlled:
			plot.setOwner(0)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 10)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Forest tiles: 10 / 20")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
	
	def test_more(self):
		controlled = plots.all().where(lambda plot: plot.getFeatureType() == iForest).limit(30) + plots.all().where(lambda plot: plot.getFeatureType() != iForest).limit(10)
		for plot in controlled:
			plot.setOwner(0)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 30)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Forest tiles: 30 / 20")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
	
		controlled = plots.all().where(lambda plot: plot.getFeatureType() == iForest).limit(30) + plots.all().where(lambda plot: plot.getFeatureType() != iForest).limit(10)
		for plot in controlled:
			plot.setOwner(1)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 30)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Forest tiles: 30 / 20")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestHappyCityPopulation(ExtendedTestCase):

	def setUp(self):
		self.requirement = HappyCityPopulation(5).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "HappyCityPopulation(5)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "HappyCityPopulation(5)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "a population of five in happy cities")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Happy city population: 0 / 5")
	
	def test_insufficient(self):
		city = TestCities.one()
		city.setPopulation(4)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 4)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Happy city population: 4 / 5")
		finally:
			city.kill()
	
	def test_insufficient_happy(self):
		happy_city, unhappy_city = cities = TestCities.num(2)
		
		happy_city.setPopulation(3)
		unhappy_city.setPopulation(10)
		
		try:
			self.assertEqual(happy_city.angryPopulation(0) <= 0, True)
			self.assertEqual(unhappy_city.angryPopulation(0) > 0, True)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Happy city population: 3 / 5")
		finally:
			cities.kill()
	
	def test_sufficient(self):
		first_city, second_city = cities = TestCities.num(2)
		
		first_city.setPopulation(3)
		second_city.setPopulation(3)
		
		try:
			self.assertEqual(first_city.angryPopulation(0) <= 0, True)
			self.assertEqual(second_city.angryPopulation(0) <= 0, True)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 6)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Happy city population: 6 / 5")
		finally:
			cities.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
	
		player_city, vassal_city = cities = TestCities.owners(0, 1)
		
		team(1).setVassal(0, True, False)
		
		player_city.setPopulation(3)
		vassal_city.setPopulation(3)
		
		try:
			self.assertEqual(player_city.angryPopulation(0) <= 0, True)
			self.assertEqual(vassal_city.angryPopulation(0) <= 0, True)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 6)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Happy city population: 6 / 5")
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestImprovementCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = ImprovementCount(iCottage, 2).create()
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
		area = plots.of([(61, 31)])
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
		area = plots.rectangle((61, 31), (63, 31))
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
		area = plots.rectangle((61, 31), (62, 31))
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
		
		area = plots.rectangle((61, 31), (62, 31))
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
	
	def test_check_improvement_built(self):
		plot = plot_(68, 35)
		plot.setOwner(0)
		plot.setImprovementType(iCottage)
		
		try:
			self.assertEqual(self.goal.checked, True)
		finally:
			plot.setOwner(-1)
			plot.setImprovementType(-1)
	
	def test_check_improvement_built_other_owner(self):
		plot = plot_(68, 35)
		plot.setOwner(1)
		plot.setImprovementType(iCottage)
		
		try:
			self.assertEqual(self.goal.checked, False)
		finally:
			plot.setOwner(-1)
			plot.setImprovementType(-1)
	
	def test_check_improvement_built_other_improvement(self):
		plot = plot_(68, 35)
		plot.setOwner(0)
		plot.setImprovementType(iHamlet)
		
		try:
			self.assertEqual(self.goal.checked, False)
		finally:
			plot.setOwner(-1)
			plot.setImprovementType(-1)


class TestOpenBorderCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = OpenBorderCount(2).create()
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
		self.requirement = OpenBorderCount(2, civs=CivsArgument(1, 2).named("Test Civs")).create()
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


class TestPeakCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = PeakCount(20).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "PeakCount(20)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "PeakCount(20)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "20 peaks")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_fewer(self):
		controlled = plots.all().where(CyPlot.isPeak).limit(10) + plots.all().where(lambda plot: not plot.isPeak()).limit(30)
		for plot in controlled:
			plot.setOwner(0)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 10)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Peaks: 10 / 20")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
	
	def test_more(self):
		controlled = plots.all().where(CyPlot.isPeak).limit(30) + plots.all().where(lambda plot: not plot.isPeak()).limit(10)
		for plot in controlled:
			plot.setOwner(0)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 30)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Peaks: 30 / 20")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		controlled = plots.all().where(CyPlot.isPeak).limit(30) + plots.all().where(lambda plot: not plot.isPeak()).limit(10)
		for plot in controlled:
			plot.setOwner(1)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 30)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Peaks: 30 / 20")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestPopulationCity(ExtendedTestCase):

	def setUp(self):
		self.requirement = PopulationCity(10).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "PopulationCity(10)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "PopulationCity(10)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "a city of size ten or larger")
	
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
		
		city1.setPopulation(2)
		city2.setPopulation(5)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 5)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Population in Second: 5 / 10")
		finally:
			cities.kill()
	
	def test_more(self):
		city1, city2 = cities = TestCities.num(2)
		
		city1.setName("First", False)
		city2.setName("Second", False)
		
		city1.setPopulation(5)
		city2.setPopulation(15)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 15)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Population in Second: 15 / 10")
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


class TestPopulationCityCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = PopulationCityCount(10, 3).create()
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
		self.requirement = PopulationCount(5).create()
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


class TestReligionPopulationCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = ReligionPopulationCount(iConfucianism, 5).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ReligionPopulationCount(Confucianism, 5)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ReligionPopulationCount(Confucianism, 5)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "a Confucian population of five")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Confucian Population: 0 / 5")
	
	def test_less(self):
		city = TestCities.one()
		city.setHasReligion(iConfucianism, True, False, False)
		city.setPopulation(4)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 4)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Confucian Population: 4 / 5")
		finally:
			city.kill()
	
	def test_more(self):
		city = TestCities.one()
		city.setHasReligion(iConfucianism, True, False, False)
		city.setPopulation(6)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 6)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Confucian Population: 6 / 5")
		finally:
			city.kill()
	
	def test_multiple_cities(self):
		cities = TestCities.num(2)
		
		for city in cities:
			city.setHasReligion(iConfucianism, True, False, False)
			city.setPopulation(3)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 6)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Confucian Population: 6 / 5")
		finally:
			cities.kill()
	
	def test_other_religion(self):
		city = TestCities.one()
		city.setHasReligion(iTaoism, True, False, False)
		city.setPopulation(6)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Confucian Population: 0 / 5")
		finally:
			city.kill()
	
	def test_other_owner(self):
		city = TestCities.one(1)
		city.setHasReligion(iConfucianism, True, False, False)
		city.setPopulation(6)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Confucian Population: 0 / 5")
		finally:
			city.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		our_city, vassal_city = cities = TestCities.owners(0, 1)
		
		for city in cities:
			city.setHasReligion(iConfucianism, True, False, False)
		
		our_city.setPopulation(4)
		vassal_city.setPopulation(3)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 7)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Confucian Population: 7 / 5")
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)


class TestResourceCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = ResourceCount(iGold, 2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ResourceCount(Gold, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ResourceCount(Gold, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Gold")
	
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
		self.requirement = SpecialistCount(iSpecialistGreatScientist, 2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "SpecialistCount(Great Scientist, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "SpecialistCount(Great Scientist, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Great Scientists")
	
	def test_description_religion(self):
		requirement = SpecialistCount(iSpecialistGreatScientist, 2, iReligion=iJudaism)
		
		self.assertEqual(requirement.description(), "two Great Scientists")
	
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


class TestTerrainCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = TerrainCount(iOcean, 50).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "TerrainCount(Ocean, 50)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "TerrainCount(Ocean, 50)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "50 Ocean tiles")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_fewer(self):
		controlled = plots.all().where(lambda plot: plot.getTerrainType() == iOcean).limit(40) + plots.all().land().limit(60)
		for plot in controlled:
			plot.setOwner(0)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 40)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Ocean tiles: 40 / 50")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
	
	def test_more(self):
		controlled = plots.all().where(lambda plot: plot.getTerrainType() == iOcean).limit(60) + plots.all().land().limit(40)
		for plot in controlled:
			plot.setOwner(0)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 60)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Ocean tiles: 60 / 50")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		controlled = plots.all().where(lambda plot: plot.getTerrainType() == iOcean).limit(60) + plots.all().land().limit(40)
		for plot in controlled:
			plot.setOwner(1)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 60)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Ocean tiles: 60 / 50")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
			
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestTradeRouteCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = TradeRouteCount(3).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "TradeRouteCount(3)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "TradeRouteCount(3)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "three trade routes")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Trade routes: 0 / 3")
	
	def test_fewer(self):
		cities = TestCities.num(2)
		
		plot(58, 35).setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Trade routes: 2 / 3")
		finally:
			cities.kill()
			plot(58, 35).setRouteType(-1)
	
	def test_sufficient(self):
		cities = TestCities.num(3)
		
		plot(58, 35).setRouteType(iRouteRoad)
		plot(60, 35).setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Trade routes: 3 / 3")
		finally:
			cities.kill()
			plot(58, 35).setRouteType(-1)
			plot(60, 35).setRouteType(-1)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestUnitCombatCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = UnitCombatCount(UnitCombatTypes.UNITCOMBAT_ARCHER, 2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
		
	def tearDown(self):
		self.requirement.deregister_handlers()
		
	def test_str(self):
		self.assertEqual(str(self.requirement), "UnitCombatCount(Archery, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "UnitCombatCount(Archery, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "an army of two archery units")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Archery units: 0 / 2")
	
	def test_fewer(self):
		city = TestCities.one()
		city.setHasRealBuilding(iPalace, True)
	
		unit = makeUnit(0, iArcher, (10, 10))
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Archery units: 1 / 2")
		finally:
			unit.kill(False, -1)
			city.kill()
	
	def test_more(self):
		city = TestCities.one()
		city.setHasRealBuilding(iPalace, True)
	
		units = makeUnits(0, iArcher, (10, 10), 3)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Archery units: 3 / 2")
		finally:
			for unit in units:
				unit.kill(False, -1)
			city.kill()
	
	def test_different_combat_type(self):
		city = TestCities.one()
		city.setHasRealBuilding(iPalace, True)
	
		units = makeUnits(0, iMilitia, (10, 10), 2)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Archery units: 0 / 2")
		finally:
			for unit in units:
				unit.kill(False, -1)
			city.kill()
	
	def test_outdated(self):
		city = TestCities.one()
		city.setHasRealBuilding(iPalace, True)
		city.plot().setBonusType(iIron)
	
		team(0).setHasTech(iBloomery, True, 0, False, False)
		team(0).setHasTech(iMachinery, True, 0, False, False)
		
		units = makeUnits(0, iArcher, (10, 10), 2)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Archery units: 0 / 2")
		finally:
			for unit in units:
				unit.kill(False, -1)
			
			team(0).setHasTech(iBloomery, False, 0, False, False)
			team(0).setHasTech(iMachinery, False, 0, False, False)
			
			city.plot().setBonusType(-1)
			city.kill()
	
	def test_different_owner(self):
		city = TestCities.one(2)
		city.setHasRealBuilding(iPalace, True)
	
		units = makeUnits(2, iArcher, (10, 10), 2)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Archery units: 0 / 2")
		finally:
			for unit in units:
				unit.kill(False, -1)
			
			city.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(2).setVassal(0, True, False)
		
		city = TestCities.one(2)
		city.setHasRealBuilding(iPalace, True)
		
		units = makeUnits(2, iArcher, (10, 10), 2)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Archery units: 2 / 2")
		finally:
			for unit in units:
				unit.kill(False, -1)
			
			team(2).setVassal(0, False, False)
			
			city.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestUnitCombatLevelCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = UnitCombatLevelCount(UnitCombatTypes.UNITCOMBAT_ARCHER, 3, 2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
		
	def tearDown(self):
		self.requirement.deregister_handlers()
		
	def test_str(self):
		self.assertEqual(str(self.requirement), "UnitCombatLevelCount(Archery, 3, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "UnitCombatLevelCount(Archery, 3, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two level three archery units")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Level three archery units: 0 / 2")
	
	def test_fewer(self):
		city = TestCities.one()
		city.setHasRealBuilding(iPalace, True)
	
		high_level_unit = makeUnit(0, iArcher, (10, 10))
		low_level_unit = makeUnit(0, iArcher, (10, 10))
		
		low_level_unit.setLevel(3)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Level three archery units: 1 / 2")
		finally:
			high_level_unit.kill(False, -1)
			low_level_unit.kill(False, -1)
			city.kill()
	
	def test_more(self):
		city = TestCities.one()
		city.setHasRealBuilding(iPalace, True)
	
		units = makeUnits(0, iArcher, (10, 10), 3)
		
		for unit in units:
			unit.setLevel(3)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Level three archery units: 3 / 2")
		finally:
			for unit in units:
				unit.kill(False, -1)
			city.kill()
	
	def test_different_combat_type(self):
		city = TestCities.one()
		city.setHasRealBuilding(iPalace, True)
	
		units = makeUnits(0, iMilitia, (10, 10), 2)
		
		for unit in units:
			unit.setLevel(3)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Level three archery units: 0 / 2")
		finally:
			for unit in units:
				unit.kill(False, -1)
			city.kill()
	
	def test_outdated(self):
		city = TestCities.one()
		city.setHasRealBuilding(iPalace, True)
		city.plot().setBonusType(iIron)
	
		team(0).setHasTech(iBloomery, True, 0, False, False)
		team(0).setHasTech(iMachinery, True, 0, False, False)
		
		units = makeUnits(0, iArcher, (10, 10), 2)
		
		for unit in units:
			unit.setLevel(3)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Level three archery units: 0 / 2")
		finally:
			for unit in units:
				unit.kill(False, -1)
			
			team(0).setHasTech(iBloomery, False, 0, False, False)
			team(0).setHasTech(iMachinery, False, 0, False, False)
			
			city.plot().setBonusType(-1)
			city.kill()
	
	def test_different_owner(self):
		city = TestCities.one(2)
		city.setHasRealBuilding(iPalace, True)
	
		units = makeUnits(2, iArcher, (10, 10), 2)
		
		for unit in units:
			unit.setLevel(3)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Level three archery units: 0 / 2")
		finally:
			for unit in units:
				unit.kill(False, -1)
			
			city.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(2).setVassal(0, True, False)
		
		city = TestCities.one(2)
		city.setHasRealBuilding(iPalace, True)
		
		units = makeUnits(2, iArcher, (10, 10), 2)
		
		for unit in units:
			unit.setLevel(3)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Level three archery units: 2 / 2")
		finally:
			for unit in units:
				unit.kill(False, -1)
			
			team(2).setVassal(0, False, False)
			
			city.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)
	

class TestUnitCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = UnitCount(iSwordsman, 3).create()
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


class TestUnitLevelCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = UnitLevelCount(3, 2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "UnitLevelCount(3, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "UnitLevelCount(3, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two level three units")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_fewer(self):
		low_level_unit = makeUnit(0, iSwordsman, (10, 10))
		high_level_unit = makeUnit(0, iSwordsman, (10, 10))
		
		high_level_unit.setLevel(3)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Level three units: 1 / 2")
		finally:
			low_level_unit.kill(False, -1)
			high_level_unit.kill(False, -1)
	
	def test_more(self):
		units = makeUnits(0, iSwordsman, (10, 10), 3)
		
		for unit in units:
			unit.setLevel(3)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Level three units: 3 / 2")
		finally:
			for unit in units:
				unit.kill(False, -1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		units = makeUnits(1, iSwordsman, (10, 10), 2)
		
		for unit in units:
			unit.setLevel(3)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Level three units: 2 / 2")
		finally:
			for unit in units:
				unit.kill(False, -1)
			
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestVassalCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = VassalCount(2).create()
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
		self.requirement = VassalCount(2, civs=CivsArgument(1, 2).named("Test Civs")).create()
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
		self.requirement = VassalCount(2, iStateReligion=iOrthodoxy).create()
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
	TestAttitudeCountReligion,
	TestAttitudeCountStateReligion,
	TestAveragePopulation,
	TestBuildingCount,
	TestCityCount,
	TestCityBuildingCount,
	TestCorporationCount,
	TestControlledResourceCount,
	TestCultureCity,
	TestCultureLevelCityCount,
	TestFeatureCount,
	TestHappyCityPopulation,
	TestImprovementCount,
	TestOpenBorderCount,
	TestOpenBorderCountCivs,
	TestPeakCount,
	TestPopulationCity,
	TestPopulationCityCount,
	TestPopulationCount,
	TestReligionPopulationCount,
	TestResourceCount,
	TestSpecialistCount,
	TestTerrainCount,
	TestTradeRouteCount,
	TestUnitCombatCount,
	TestUnitCombatLevelCount,
	TestUnitCount,
	TestUnitLevelCount,
	TestVassalCount,
	TestVassalCountCivs,
	TestVassalCountStateReligion,
]