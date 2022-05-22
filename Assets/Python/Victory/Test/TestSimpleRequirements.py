from SimpleRequirements import *

from TestVictoryCommon import *


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
	TestControl,
	TestTradeConnection,
	TestWonder,
]