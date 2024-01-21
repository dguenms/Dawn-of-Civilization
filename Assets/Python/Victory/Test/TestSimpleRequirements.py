from SimpleRequirements import *

from TestVictoryCommon import *


class TestAllAttitude(ExtendedTestCase):

	def setUp(self):
		self.requirement = AllAttitude(AttitudeTypes.ATTITUDE_PLEASED).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
		
		self.others = [1, 2, 6, 7, 8, 9, 10, 11]
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "AllAttitude(Pleased)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "AllAttitude(Pleased)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "pleased or better relations with all other civilizations")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		for iPlayer in self.others:
			team(iPlayer).meet(0, True)
			player(iPlayer).AI_setAttitudeExtra(0, -100)
	
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Pleased or better relations: 0 / 8")
		finally:
			for iPlayer in self.others:
				team(iPlayer).cutContact(0)
				player(iPlayer).AI_setAttitudeExtra(0, 0)
	
	def test_all(self):
		for iPlayer in self.others:
			team(iPlayer).meet(0, True)
			player(iPlayer).AI_setAttitudeExtra(0, 100)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Pleased or better relations: 8 / 8")
		finally:
			for iPlayer in self.others:
				team(iPlayer).cutContact(0)
				player(iPlayer).AI_setAttitudeExtra(0, 0)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestAllowNone(ExtendedTestCase):

	def setUp(self):
		self.civs = CivsArgument(1).named("Test Civs")
		self.area = AreaArgumentFactory().of([(57, 35), (59, 35)]).named("Test Area")
		self.requirement = AllowNone(self.civs, self.area).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "AllowNone(Test Civs, Test Area)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "AllowNone(Test Civs, Test Area)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots.of([(57, 35), (59, 35)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((57, 35)), "Test Area")
		self.assertEqual(self.requirement.area_name((42, 42)), "")
	
	def test_none(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "No Test Civs civilizations in Test Area")
	
	def test_only_player(self):
		city = TestCities.one()
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "No Test Civs civilizations in Test Area")
		finally:
			city.kill()
	
	def test_allowed(self):
		our_city, allowed_city = cities = TestCities.owners(0, 2)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "No Test Civs civilizations in Test Area")
		finally:
			cities.kill()
	
	def test_not_allowed(self):
		our_city, not_allowed_city = cities = TestCities.owners(0, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "No Test Civs civilizations in Test Area")
		finally:
			cities.kill()
	
	def test_minor(self):
		our_city, minor_city = cities = TestCities.owners(0, iNative)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "No Test Civs civilizations in Test Area")
		finally:
			cities.kill()
	
	def test_outside(self):
		our_city1, our_city2, not_allowed_city = cities = TestCities.owners(0, 0, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "No Test Civs civilizations in Test Area")
		finally:
			cities.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		our_city, vassal_city = cities = TestCities.owners(0, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "No Test Civs civilizations in Test Area")
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestAllowOnly(ExtendedTestCase):

	def setUp(self):
		self.area = AreaArgumentFactory().of([(57, 35), (59, 35)]).named("Test Area")
		self.civs = CivsArgument(1).named("Test Civs")
		self.requirement = AllowOnly(self.area, self.civs).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "AllowOnly(Test Area, Test Civs)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "AllowOnly(Test Area, Test Civs)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "only Test Civs civilizations in Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots.of([(57, 35), (59, 35)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((57, 35)), "Test Area")
		self.assertEqual(self.requirement.area_name((42, 42)), "")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Only Test Civs civilizations in Test Area")
	
	def test_only_player(self):
		city = TestCities.one()
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Only Test Civs civilizations in Test Area")
		finally:
			city.kill()
	
	def test_allowed(self):
		our_city, allowed_city = cities = TestCities.owners(0, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Only Test Civs civilizations in Test Area")
		finally:
			cities.kill()
	
	def test_not_allowed(self):
		our_city, not_allowed_city = cities = TestCities.owners(0, 2)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Only Test Civs civilizations in Test Area")
		finally:
			cities.kill()
	
	def test_minor(self):
		our_city, minor_city = cities = TestCities.owners(0, iIndependent)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Only Test Civs civilizations in Test Area")
		finally:
			cities.kill()
	
	def test_outside(self):
		our_city1, our_city2, not_allowed_city = cities = TestCities.owners(0, 0, 2)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Only Test Civs civilizations in Test Area")
		finally:
			cities.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(2).setVassal(0, True, False)
		
		our_city, vassal_city = cities = TestCities.owners(0, 2)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Only Test Civs civilizations in Test Area")
		finally:
			cities.kill()
			team(2).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestAreaNoStateReligion(ExtendedTestCase):

	def setUp(self):
		self.area = AreaArgumentFactory().of([(57, 35), (59, 35)]).named("Test Area")
		self.requirement = AreaNoStateReligion(self.area, iCatholicism).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "AreaNoStateReligion(Test Area, Catholicism)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "AreaNoStateReligion(Test Area, Catholicism)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "no Catholic civilizations in Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots.of([(57, 35), (59, 35)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((59, 35)), "Test Area")
		self.assertEqual(self.requirement.area_name((42, 42)), "")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_no_cities(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "No Catholic civilizations in Test Area")
	
	def test_no_state_religion(self):
		cities = TestCities.owners(1, 1)
		
		for city in cities:
			city.setHasReligion(iCatholicism, True, False, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "No Catholic civilizations in Test Area")
		finally:
			cities.kill()
	
	def test_no_city_religion(self):
		cities = TestCities.owners(1, 1)
		
		player(1).setLastStateReligion(iCatholicism)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "No Catholic civilizations in Test Area")
		finally:
			player(1).setLastStateReligion(-1)
			cities.kill()
	
	def test_outside_of_area(self):
		cities = TestCities.owners(1, 1, 2)
		
		player(2).setLastStateReligion(iCatholicism)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "No Catholic civilizations in Test Area")
		finally:
			player(2).setLastStateReligion(-1)
			cities.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestCommunist(ExtendedTestCase):

	def setUp(self):
		self.requirement = Communist().create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "Communist()")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "Communist()")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Communism")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_not_communist(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Communist")
	
	def test_communist(self):
		player(0).setCivics(iCivicsEconomy, iCentralPlanning)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Communist")
		finally:
			player(0).setCivics(iCivicsEconomy, iRedistribution)
	
	def test_communist_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		player(1).setCivics(iCivicsEconomy, iCentralPlanning)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Communist")
		finally:
			team(1).setVassal(0, False, False)
			player(1).setCivics(iCivicsEconomy, iRedistribution)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestControl(ExtendedTestCase):

	def setUp(self):
		self.area = AreaArgumentFactory().of(TestCities.CITY_LOCATIONS).named("the Area")
		self.requirement = Control(self.area).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "Control(the Area)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "Control(the Area)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "the Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Area": plots.of(TestCities.CITY_LOCATIONS)})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((57, 35)), "Area")
		self.assertEqual(self.requirement.area_name((58, 36)), "")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "The Area")
	
	def test_some(self):
		cities = TestCities.owners(0, 0, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "The Area")
		finally:
			cities.kill()
	
	def test_all(self):
		cities = TestCities.owners(0, 0, 0)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "The Area")
		finally:
			cities.kill()
	
	def test_other_evaluator_fulfilled(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		cities = TestCities.owners(0, 0, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "The Area")
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_other_evaluator_not_fulfilled(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		cities = TestCities.owners(0, 0, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), False)
			self.assertEqual(self.requirement.progress(evaluator), self.FAILURE + "The Area")
		finally:
			cities.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)


class TestCultureCover(ExtendedTestCase):

	def setUp(self):
		self.area = AreaArgumentFactory().of([(61, 31), (63, 31)]).named("Test Area")
		self.requirement = CultureCover(self.area).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
		
		plot(61, 31).setOwner(-1)
		plot(63, 31).setOwner(-1)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CultureCover(Test Area)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CultureCover(Test Area)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots.of([(61, 31), (63, 31)])})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Test Area")
	
	def test_some(self):
		plot(61, 31).setOwner(0)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Test Area")
		finally:
			plot(61, 31).setOwner(-1)
	
	def test_all(self):
		plot(61, 31).setOwner(0)
		plot(63, 31).setOwner(0)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Test Area")
		finally:
			plot(61, 31).setOwner(0)
			plot(63, 31).setOwner(0)
	
	def test_other_owner(self):
		plot(61, 31).setOwner(1)
		plot(63, 31).setOwner(1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Test Area")
		finally:
			plot(61, 31).setOwner(-1)
			plot(63, 31).setOwner(-1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		plot(61, 31).setOwner(1)
		plot(63, 31).setOwner(1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Test Area")
		finally:
			plot(61, 31).setOwner(-1)
			plot(63, 31).setOwner(-1)
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestGoldPercent(ExtendedTestCase):

	def setUp(self):
		self.requirement = GoldPercent(50).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "GoldPercent(50%)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "GoldPercent(50%)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "at least half as much gold as all other civilizations combined")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_less(self):
		player(0).setGold(50)
		player(1).setGold(100)
		player(2).setGold(100)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold: 50 / 200")
		finally:
			for iPlayer in [0, 1, 2]:
				player(iPlayer).setGold(0)
	
	def test_more(self):
		player(0).setGold(150)
		player(1).setGold(100)
		player(2).setGold(100)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold: 150 / 200")
		finally:
			for iPlayer in [0, 1, 2]:
				player(iPlayer).setGold(0)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		player(0).setGold(100)
		player(1).setGold(100)
		player(2).setGold(300)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Gold: 200 / 300")
		finally:
			for iPlayer in [0, 1, 2]:
				player(iPlayer).setGold(0)
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestMoreCulture(ExtendedTestCase):

	def setUp(self):
		self.civs = CivsArgument(1, 2).named("Test Civs")
		self.requirement = MoreCulture(self.civs).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "MoreCulture(Test Civs)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "MoreCulture(Test Civs)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "more culture than Test Civs civilizations combined")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_less(self):
		city0, city1, city2 = cities = TestCities.owners(0, 1, 2)
		
		city0.setCulture(0, 100, True)
		city1.setCulture(1, 75, True)
		city2.setCulture(2, 75, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Total culture: 100 / 150")
		finally:
			cities.kill()
	
	def test_more(self):
		city0, city1, city2 = cities = TestCities.owners(0, 1, 2)
		
		city0.setCulture(0, 200, True)
		city1.setCulture(1, 75, True)
		city2.setCulture(2, 75, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Total culture: 200 / 150")
		finally:
			cities.kill()
	
	def test_other_player(self):
		city0, city1, city7 = cities = TestCities.owners(0, 1, 7)
		
		city0.setCulture(0, 100, True)
		city1.setCulture(1, 75, True)
		city7.setCulture(7, 75, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Total culture: 100 / 75")
		finally:
			cities.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(7).setVassal(0, True, False)
		
		city0, city1, city7 = cities = TestCities.owners(0, 1, 7)
		
		city0.setCulture(0, 75, True)
		city1.setCulture(1, 100, True)
		city7.setCulture(7, 75, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Total culture: 150 / 100")
		finally:
			cities.kill()
			team(7).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestMoreReligion(ExtendedTestCase):

	def setUp(self):
		self.area = AreaArgumentFactory().of(TestCities.CITY_LOCATIONS).named("Test Area")
		self.requirement = MoreReligion(self.area, iOrthodoxy, iCatholicism).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "MoreReligion(Test Area, Orthodoxy, Catholicism)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "MoreReligion(Test Area, Orthodoxy, Catholicism)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "more Orthodox than Catholic cities in Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots.of(TestCities.CITY_LOCATIONS)})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((57, 35)), "Test Area")
		self.assertEqual(self.requirement.area_name((58, 36)), "")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_no_cities(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Orthodox cities: 0 Catholic cities: 0")
	
	def test_more(self):
		city1, city2, city3 = cities = TestCities.num(3)
		city1.setHasReligion(iOrthodoxy, True, False, False)
		city2.setHasReligion(iOrthodoxy, True, False, False)
		city3.setHasReligion(iCatholicism, True, False, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Orthodox cities: 2 Catholic cities: 1")
		finally:
			cities.kill()
	
	def test_equal(self):
		city1, city2 = cities = TestCities.num(2)
		city1.setHasReligion(iOrthodoxy, True, False, False)
		city2.setHasReligion(iCatholicism, True, False, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Orthodox cities: 1 Catholic cities: 1")
		finally:
			cities.kill()
	
	def test_fewer(self):
		city1, city2, city3 = cities = TestCities.num(3)
		city1.setHasReligion(iOrthodoxy, True, False, False)
		city2.setHasReligion(iCatholicism, True, False, False)
		city3.setHasReligion(iCatholicism, True, False, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Orthodox cities: 1 Catholic cities: 2")
		finally:
			cities.kill()
	
	def test_different_owner(self):
		city1, city2, city3 = cities = TestCities.owners(1, 1, 1)
		city1.setHasReligion(iOrthodoxy, True, False, False)
		city2.setHasReligion(iOrthodoxy, True, False, False)
		city3.setHasReligion(iCatholicism, True, False, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Orthodox cities: 2 Catholic cities: 1")
		finally:
			cities.kill()
	
	def test_outside(self):
		requirement = MoreReligion(plots.rectangle((10, 10), (20, 20)).named("Test Area"), iOrthodoxy, iCatholicism)
		
		city1, city2, city3 = cities = TestCities.num(3)
		city1.setHasReligion(iOrthodoxy, True, False, False)
		city2.setHasReligion(iOrthodoxy, True, False, False)
		city3.setHasReligion(iCatholicism, True, False, False)
		
		try:
			self.assertEqual(requirement.fulfilled(self.evaluator), False)
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Orthodox cities: 0 Catholic cities: 0")
		finally:
			cities.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestNoReligionPercent(ExtendedTestCase):

	def setUp(self):
		self.requirement = NoReligionPercent(50).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "NoReligionPercent(50%)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "NoReligionPercent(50%)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "no more than half of your cities to have a religion")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_less(self):
		city1, city2, city3, city4 = cities = TestCities.num(4)
		
		city1.setHasReligion(iBuddhism, True, False, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Cities with no religion: 3 / 4")
		finally:
			cities.kill()
	
	def test_more(self):
		city1, city2, city3, city4 = cities = TestCities.num(4)
		
		city1.setHasReligion(iHinduism, True, False, False)
		city2.setHasReligion(iBuddhism, True, False, False)
		city3.setHasReligion(iConfucianism, True, False, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Cities with no religion: 1 / 4")
		finally:
			cities.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		city1, city2, city3, city4 = cities = TestCities.owners(0, 0, 1, 1)
		
		city1.setHasReligion(iHinduism, True, False, False)
		city3.setHasReligion(iBuddhism, True, False, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Cities with no religion: 2 / 4")
		finally:
			cities.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestNoStateReligion(ExtendedTestCase):

	def setUp(self):
		self.requirement = NoStateReligion(iCatholicism).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "NoStateReligion(Catholicism)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "NoStateReligion(Catholicism)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "make sure there are no Catholic civilizations in the world")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Catholic civilizations: 0")
	
	def test_one(self):
		player(1).setLastStateReligion(iCatholicism)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Catholic civilizations: 1")
		finally:
			player(1).setLastStateReligion(-1)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestProject(ExtendedTestCase):

	def setUp(self):
		self.requirement = Project(iTheInternet).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "Project(The Internet)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "Project(The Internet)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "the Internet")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_not_completed(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "The Internet")
	
	def test_completed(self):
		team(0).changeProjectCount(iTheInternet, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "The Internet")
		finally:
			team(0).changeProjectCount(iTheInternet, -1)
	
	def test_completed_other(self):
		team(1).changeProjectCount(iTheInternet, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "The Internet")
		finally:
			team(1).changeProjectCount(iTheInternet, -1)
	
	def test_completed_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		team(1).changeProjectCount(iTheInternet, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "The Internet")
		finally:
			team(1).changeProjectCount(iTheInternet, -1)
			team(1).setVassal(0, False, False)
	
	def test_check_project_built(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("projectBuilt", city, iTheInternet)
			
			self.assertEqual(self.goal.checked, True)
			self.assertEqual(self.goal.failed, False)
		finally:
			city.kill()
	
	def test_check_project_built_different_project(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("projectBuilt", city, iManhattanProject)
			
			self.assertEqual(self.goal.checked, False)
			self.assertEqual(self.goal.failed, False)
		finally:
			city.kill()
	
	def test_expire_project_built(self):
		city = TestCities.one(1)
		
		try:
			events.fireEvent("projectBuilt", city, iTheInternet)
			
			self.assertEqual(self.goal.checked, False)
			self.assertEqual(self.goal.failed, True)
		finally:
			city.kill()
	
	def test_expire_project_built_different_project(self):
		city = TestCities.one(1)
		
		try:
			events.fireEvent("projectBuilt", city, iManhattanProject)
			
			self.assertEqual(self.goal.checked, False)
			self.assertEqual(self.goal.failed, False)
		finally:
			city.kill()
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestRoute(ExtendedTestCase):

	def setUp(self):
		self.area = AreaArgumentFactory().rectangle((60, 30), (61, 31)).named("Test Area")
		self.actual_area = self.area.create()
		self.requirement = Route(self.area, [iRouteRoad, iRouteRomanRoad]).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "Route(Test Area, Road or Roman Road)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "Route(Test Area, Road or Roman Road)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "a Road or Roman Road along Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots.rectangle((60, 30), (61, 31))})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Road or Roman Road along Test Area in your territory")
	
	def test_fulfilled(self):
		for plot in self.actual_area:
			plot.setOwner(0)
			plot.setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Road or Roman Road along Test Area in your territory")
		finally:
			for plot in self.actual_area:
				plot.setOwner(-1)
				plot.setRouteType(-1)
	
	def test_no_route(self):
		for plot in self.actual_area:
			plot.setOwner(0)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Road or Roman Road along Test Area in your territory")
		finally:
			for plot in self.actual_area:
				plot.setOwner(-1)
	
	def test_not_owned(self):
		for plot in self.actual_area:
			plot.setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Road or Roman Road along Test Area in your territory")
		finally:
			for plot in self.actual_area:
				plot.setRouteType(-1)
	
	def test_different_routes(self):
		for index, plot in enumerate(self.actual_area):
			plot.setOwner(0)
			
			if index % 2 == 0:
				plot.setRouteType(iRouteRoad)
			else:
				plot.setRouteType(iRouteRomanRoad)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Road or Roman Road along Test Area in your territory")
		finally:
			for plot in self.actual_area:
				plot.setOwner(-1)
				plot.setRouteType(-1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		for plot in self.actual_area:
			plot.setOwner(1)
			plot.setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Road or Roman Road along Test Area in your territory")
		finally:
			for plot in self.actual_area:
				plot.setOwner(-1)
				plot.setRouteType(-1)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestRouteConnection(ExtendedTestCase):

	def setUp(self):
		self.start = AreaArgumentFactory().of([(57, 35)]).named("Start Area")
		self.target = AreaArgumentFactory().of([(61, 35)]).named("Target Area")
		self.requirement = RouteConnection([iRouteRailroad], self.start, self.target).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "RouteConnection(Railroad, Start Area, Target Area)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "RouteConnection(Railroad, Start Area, Target Area)")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Target Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Start Area": plots.of([(57, 35)]), "Target Area": plots.of([(61, 35)])})
	
	def test_direct_connection(self):
		start, target = cities = TestCities.owners(0, -1, 0)
		
		route_plots = plots.rectangle((58, 35), (60, 35))
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(0)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Railroad from Start Area to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			cities.kill()
	
	def test_direct_connection_named(self):
		requirement = RouteConnection(NamedList(iRouteRailroad).named("Some route"), self.start, self.target)
	
		start, target = cities = TestCities.owners(0, -1, 0)
		
		route_plots = plots.rectangle((58, 35), (60, 35))
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(0)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(requirement.fulfilled(self.evaluator), True)
			self.assertEqual(requirement.progress(self.evaluator), self.SUCCESS + "Some route from Start Area to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			cities.kill()
	
	def test_no_connection(self):
		start, target = cities = TestCities.owners(0, -1, 0)
		
		culture_plots = plots.rectangle((58, 35), (60, 35))
		for plot in culture_plots:
			plot.setOwner(0)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Railroad from Start Area to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in culture_plots:
				plot.setOwner(-1)
			
			cities.kill()
	
	def test_no_culture(self):
		start, target = cities = TestCities.owners(0, -1, 0)
		
		route_plots = plots.rectangle((58, 35), (60, 35))
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Railroad from Start Area to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
			
			cities.kill()
	
	def test_different_route_type(self):
		start, target = cities = TestCities.owners(0, -1, 0)
		
		route_plots = plots.rectangle((58, 35), (60, 35))
		for plot in route_plots:
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		route_techs = [iLeverage, iRailroad]
		for iTech in route_techs:
			team(0).setHasTech(iTech, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Railroad from Start Area to Target Area")
		finally:
			for iTech in route_techs:
				team(0).setHasTech(iTech, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			cities.kill()
	
	def test_no_route_tech(self):
		start, target = cities = TestCities.owners(0, -1, 0)
		
		route_plots = plots.rectangle((58, 35), (60, 35))
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(0)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Railroad from Start Area to Target Area")
		finally:
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			cities.kill()
	
	def test_no_start_city(self):
		target = TestCities.owners(-1, -1, 0)[0]
		
		route_plots = plots.rectangle((57, 35), (60, 35))
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(0)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Railroad from Start Area to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			target.kill()
	
	def test_different_start_city_owner(self):
		start, target = cities = TestCities.owners(1, -1, 0)
		
		route_plots = plots.rectangle((58, 35), (60, 35))
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(0)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Railroad from Start Area to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			cities.kill()
	
	def test_no_target_city(self):
		start = TestCities.one()
		
		route_plots = plots.rectangle((58, 35), (61, 35))
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(0)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Railroad from Start Area to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			start.kill()
	
	def test_target_city_different_owner(self):
		start, target = cities = TestCities.owners(0, -1, 1)
		
		route_plots = plots.rectangle((58, 35), (60, 35))
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(0)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Railroad from Start Area to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			cities.kill()
	
	def test_indirect_connection(self):
		start, target = cities = TestCities.owners(0, -1, 0)
		
		route_plots = plots.of([(56, 36), (57, 37), (58, 37), (59, 37), (60, 37), (61, 37), (62, 36)])
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(0)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Railroad from Start Area to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			cities.kill()
	
	def test_connection_through_city(self):
		cities = TestCities.num(3)
		
		route_plots = plots.of([(58, 35), (60, 35)])
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(0)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Railroad from Start Area to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			cities.kill()
	
	def test_connection_through_city_different_owner(self):
		cities = TestCities.owners(0, 1, 0)
		
		route_plots = plots.of([(58, 35), (60, 35)])
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(0)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Railroad from Start Area to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			cities.kill()
	
	def test_multiple_start_cities(self):
		requirement = RouteConnection([iRouteRailroad], AreaArgumentFactory().of([(57, 35), (59, 35)]).named("Start Area"), AreaArgumentFactory().of([(61, 35)]).named("Target Area"))
		
		cities = TestCities.num(3)
		
		route_plots = plots.of([(60, 35)])
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(0)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(requirement.fulfilled(self.evaluator), True)
			self.assertEqual(requirement.progress(self.evaluator), self.SUCCESS + "Railroad from Start Area to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			cities.kill()
	
	def test_multiple_target_cities(self):
		requirement = RouteConnection([iRouteRailroad], AreaArgumentFactory().of([(57, 35)]).named("Start Area"), AreaArgumentFactory().of([(59, 35), (61, 35)]).named("Target Area"))
		
		cities = TestCities.num(3)
		
		route_plots = plots.of([(58, 35)])
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(0)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(requirement.fulfilled(self.evaluator), True)
			self.assertEqual(requirement.progress(self.evaluator), self.SUCCESS + "Railroad from Start Area to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			cities.kill()
	
	def test_with_start_owners(self):
		requirement = RouteConnection([iRouteRailroad], AreaArgumentFactory().of([(57, 35)]).named("Start Area"), AreaArgumentFactory().of([(61, 35)]).named("Target Area"), start_owners=True)
		
		cities = TestCities.owners(1, -1, 0)
		
		route_plots = plots.rectangle((58, 35), (60, 35))
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(0)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(requirement.fulfilled(self.evaluator), True)
			self.assertEqual(requirement.progress(self.evaluator), self.SUCCESS + "Railroad from Start Area to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			cities.kill()
	
	def test_with_start_owners_including_target(self):
		requirement = RouteConnection([iRouteRailroad], AreaArgumentFactory().of([(57, 35)]).named("Start Area"), AreaArgumentFactory().of([(61, 35)]).named("Target Area"), start_owners=True)
		
		cities = TestCities.owners(1, -1, 1)
		
		route_plots = plots.rectangle((58, 35), (60, 35))
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(0)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(requirement.fulfilled(self.evaluator), False)
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Railroad from Start Area to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			cities.kill()
	
	def test_city_start(self):
		requirement = RouteConnection([iRouteRailroad], LocationCityArgument((57, 35)).named("Start City"), AreaArgumentFactory().of([(59, 35)]).named("Target Area")).create()
		
		capital, destination = cities = TestCities.num(2)
		
		route_plots = plots.of([(58, 35)])
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(0)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(requirement.areas(), {"Start City": plots.of([(57, 35)]), "Target Area": plots.of([(59, 35)])})
			self.assertEqual(requirement.fulfilled(self.evaluator), True)
			self.assertEqual(requirement.progress(self.evaluator), self.SUCCESS + "Railroad from Start City to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			cities.kill()
	
	def test_city_start_no_city(self):
		requirement = RouteConnection([iRouteRailroad], LocationCityArgument((61, 35)).named("Start City"), AreaArgumentFactory().of([(59, 35)]).named("Target Area")).create()
		
		cities = TestCities.num(2)
		
		route_plots = plots.of([(58, 35), (60, 35)])
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(0)
		
		team(0).setHasTech(iRailroad, True, 0, True, False)
		
		try:
			self.assertEqual(requirement.areas(), {"Start City": plots.of([(61, 35)]), "Target Area": plots.of([(59, 35)])})
			self.assertEqual(requirement.fulfilled(self.evaluator), False)
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Railroad from Start City to Target Area")
		finally:
			team(0).setHasTech(iRailroad, False, 0, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			cities.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		cities = TestCities.owners(1, -1, 1)
		
		route_plots = plots.rectangle((58, 35), (60, 35))
		for plot in route_plots:
			plot.setRouteType(iRouteRailroad)
			plot.setOwner(1)
		
		team(1).setHasTech(iRailroad, True, 1, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Railroad from Start Area to Target Area")
		finally:
			team(1).setHasTech(iRailroad, False, 1, True, False)
			
			for plot in route_plots:
				plot.setRouteType(-1)
				plot.setOwner(-1)
			
			cities.kill()
			
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestStateReligionPercent(ExtendedTestCase):

	def setUp(self):
		self.requirement = StateReligionPercent(iConfucianism, 25).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "StateReligionPercent(Confucianism, 25%)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "StateReligionPercent(Confucianism, 25%)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "at least 25% of all civilizations are Confucian")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.value(), 0)
		self.assertEqual(self.requirement.required(), 2)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Confucian civilizations: 0 / 2")
	
	def test_fewer(self):
		player(0).setLastStateReligion(iConfucianism)
		
		try:
			self.assertEqual(self.requirement.value(), 1)
			self.assertEqual(self.requirement.required(), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Confucian civilizations: 1 / 2")
		finally:
			player(0).setLastStateReligion(-1)
	
	def test_more(self):
		players = [0, 1, 2]
		for iPlayer in players:
			player(iPlayer).setLastStateReligion(iConfucianism)
		
		try:
			self.assertEqual(self.requirement.value(), 3)
			self.assertEqual(self.requirement.required(), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Confucian civilizations: 3 / 2")
		finally:
			for iPlayer in players:
				player(iPlayer).setLastStateReligion(-1)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestStateReligionPercentSecular(ExtendedTestCase):

	def setUp(self):
		self.requirement = StateReligionPercent(iConfucianism, 25, bSecular=True).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "at least 25% of all civilizations are Confucian or secular")
	
	def test_none(self):
		self.assertEqual(self.requirement.value(), 0)
		self.assertEqual(self.requirement.required(), 2)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Confucian or secular civilizations: 0 / 2")
	
	def test_sufficient_religion(self):
		player(0).setLastStateReligion(iConfucianism)
		player(1).setLastStateReligion(iConfucianism)
		
		try:
			self.assertEqual(self.requirement.value(), 2)
			self.assertEqual(self.requirement.required(), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Confucian or secular civilizations: 2 / 2")
		finally:
			player(0).setLastStateReligion(-1)
			player(1).setLastStateReligion(-1)
	
	def test_sufficient_secular(self):
		player(0).setCivics(iCivicsReligion, iSecularism)
		player(1).setCivics(iCivicsReligion, iSecularism)
		
		try:
			self.assertEqual(self.requirement.value(), 2)
			self.assertEqual(self.requirement.required(), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Confucian or secular civilizations: 2 / 2")
		finally:
			player(0).setCivics(iCivicsReligion, iAnimism)
			player(1).setCivics(iCivicsReligion, iAnimism)


class TestTradeConnection(ExtendedTestCase):

	def setUp(self):
		self.requirement = TradeConnection().create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
		
	def test_str(self):
		self.assertEqual(str(self.requirement), "TradeConnection()")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "TradeConnection()")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "trade connection with another civilization")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_not_fulfilled(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Trade connection with another civilization")
	
	def test_fulfilled(self):
		team(1).meet(0, False)
		team(1).setOpenBorders(0, True)
		
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		plot(58, 35).setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Trade connection with another civilization")
		finally:
			plot(58, 35).setRouteType(-1)
			cities.kill()
			
			team(1).setOpenBorders(0, False)
			team(1).cutContact(0)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).meet(0, False)
		team(1).setVassal(0, True, False)
		team(1).setOpenBorders(0, True)
		
		vassal_city, other_city = cities = TestCities.owners(1, 2)
		
		plot(58, 35).setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Trade connection with another civilization")
		finally:
			plot(58, 35).setRouteType(-1)
			cities.kill()
			
			team(1).setOpenBorders(0, False)
			team(1).setVassal(0, False, False)
			team(1).cutContact(0)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)


class TestWonder(ExtendedTestCase):

	def setUp(self):
		self.requirement = Wonder(iPyramids).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "Wonder(The Pyramids)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "Wonder(The Pyramids)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "the Pyramids")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_not_fulfilled(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "The Pyramids")
	
	def test_fulfilled(self):
		city = TestCities.one()
		city.setHasRealBuilding(iPyramids, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "The Pyramids")
		finally:
			city.kill()
	
	def test_fulfilled_different_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		city = TestCities.one(1)
		city.setHasRealBuilding(iPyramids, True)
		
		team(1).setVassal(0, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "The Pyramids")
		finally:
			city.kill()
			team(1).setVassal(0, False, False)
	
	def test_check_building_built(self):
		city = TestCities.one()
		city.setHasRealBuilding(iPyramids, True)
		
		try:
			events.fireEvent("buildingBuilt", city, iPyramids)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_check_building_built_other(self):
		city = TestCities.one()
		city.setHasRealBuilding(iOracle, True)
		
		try:
			events.fireEvent("buildingBuilt", city, iOracle)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_expire_building_built(self):
		city = TestCities.one(1)
		city.setHasRealBuilding(iPyramids, True)
		
		try:
			events.fireEvent("buildingBuilt", city, iPyramids)
			
			self.assertEqual(self.goal.failed, True)
		finally:
			city.kill()
	
	def test_expire_building_built_other(self):
		city = TestCities.one(1)
		city.setHasRealBuilding(iOracle, True)
		
		try:
			events.fireEvent("buildingBuilt", city, iOracle)
			
			self.assertEqual(self.goal.failed, False)
		finally:
			city.kill()


test_cases = [
	TestAllAttitude,
	TestAllowNone,
	TestAllowOnly,
	TestAreaNoStateReligion,
	TestCommunist,
	TestControl,
	TestCultureCover,
	TestGoldPercent,
	TestMoreCulture,
	TestMoreReligion,
	TestNoReligionPercent,
	TestNoStateReligion,
	TestProject,
	TestRoute,
	TestRouteConnection,
	TestStateReligionPercent,
	TestStateReligionPercentSecular,
	TestTradeConnection,
	TestWonder,
]