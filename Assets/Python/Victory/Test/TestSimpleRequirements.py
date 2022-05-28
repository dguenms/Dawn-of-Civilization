from SimpleRequirements import *

from TestVictoryCommon import *


class TestCityBuilding(ExtendedTestCase):

	def setUp(self):
		self.requirement = CityBuilding(CityDefinition(TestCities.CITY_LOCATIONS[0]).named("Test City"), iGranary)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CityBuilding(Test City, Granary)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CityBuilding(Test City, Granary)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "a Granary in Test City")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test City": plots_.of([TestCities.CITY_LOCATIONS[0]])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((61, 31)), "Test City")
		self.assertEqual(self.requirement.area_name((62, 32)), "")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_no_city(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Granary")
	
	def test_city_no_building(self):
		city = TestCities.one()
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Granary")
		finally:
			city.kill()
	
	def test_city_building(self):
		city = TestCities.one()
		city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Granary")
		finally:
			city.kill()
	
	def test_city_building_different_owner(self):
		city = TestCities.one(1)
		city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Granary")
		finally:
			city.kill()
	
	def test_city_building_different_location(self):
		other_city, city = cities = TestCities.num(2)
		
		city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Granary")
		finally:
			cities.kill()
	
	def test_city_unique_building(self):
		requirement = CityBuilding(CityDefinition(TestCities.CITY_LOCATIONS[0]).named("Test City"), iMonument)
		
		city = TestCities.one()
		city.setHasRealBuilding(iObelisk, True)
		
		try:
			self.assertEqual(requirement.fulfilled(self.evaluator), True)
			self.assertEqual(requirement.progress(self.evaluator), self.SUCCESS + "Monument")
		finally:
			city.kill()
	
	def test_different_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
	
		city = TestCities.one(1)
		city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Granary")
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
		requirement = CityBuilding(CityDefinition(TestCities.CITY_LOCATIONS[0]), iPyramids)
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
		requirement = CityBuilding(CityDefinition(TestCities.CITY_LOCATIONS[0]), iPyramids)
		
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
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots_.of(TestCities.CITY_LOCATIONS)})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((61, 31)), "Test Area")
		self.assertEqual(self.requirement.area_name((62, 32)), "")
	
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


class TestMoreReligion(ExtendedTestCase):

	def setUp(self):
		self.requirement = MoreReligion(plots.of(TestCities.CITY_LOCATIONS).named("Test Area"), iOrthodoxy, iCatholicism)
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
		self.assertEqual(self.requirement.areas(), {"Test Area": plots_.of(TestCities.CITY_LOCATIONS)})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((61, 31)), "Test Area")
		self.assertEqual(self.requirement.area_name((62, 32)), "")
	
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


class TestTradeConnection(ExtendedTestCase):

	def setUp(self):
		self.requirement = TradeConnection()
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
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Trade connection with another civilization")
		finally:
			plot(62, 31).setRouteType(-1)
			cities.kill()
			
			team(1).setOpenBorders(0, False)
			team(1).cutContact(0)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).meet(0, False)
		team(1).setVassal(0, True, False)
		team(1).setOpenBorders(0, True)
		
		vassal_city, other_city = cities = TestCities.owners(1, 2)
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Trade connection with another civilization")
		finally:
			plot(62, 31).setRouteType(-1)
			cities.kill()
			
			team(1).setOpenBorders(0, False)
			team(1).setVassal(0, False, False)
			team(1).cutContact(0)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)


class TestWonder(ExtendedTestCase):

	def setUp(self):
		self.requirement = Wonder(iPyramids)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "Wonder(The Pyramids)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "Wonder(The Pyramids)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "The Pyramids")
	
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
	TestCityBuilding,
	TestControl,
	TestMoreReligion,
	TestTradeConnection,
	TestWonder,
]