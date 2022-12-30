from Victories import *
from Definitions import BuildingCount, Control
from GoalHandlers import event_handler_registry
from Goals import Goal

from TestVictoryCommon import *

import Requirements as req


class TestVictory(ExtendedTestCase):

	def setUp(self):
		self.iRegisteredHandlers = len(event_handler_registry.registered)
	
		self.descriptions = [BuildingCount(iGranary, 3)]
		self.victory = Victory(0, self.descriptions)
		
		self.victory.goal_fail = self.overridden_goal_fail
		self.victory.goal_succeed = self.overridden_goal_succeed
		
		self.on_failure_called = False
		self.on_success_called = False
	
	def overridden_goal_fail(self):
		def fail(goal):
			self.on_failure_called = True
		
		return fail
	
	def overridden_goal_succeed(self):
		def succeed(goal):
			self.on_success_called = True
		
		return succeed
	
	def test_attributes(self):
		self.assertEqual(self.victory.iPlayer, 0)
		self.assertEqual(len(self.victory.goals), 1)
		self.assertEqual(self.victory.goals[0], Goal([req.BuildingCount(iGranary, 3)], req.BuildingCount.GOAL_DESC_KEY, 0))
	
	def test_none_succeeded(self):
		self.assertEqual(self.victory.succeeded_goals(), 0)
	
	def test_all_succeeded(self):
		self.victory.goals[0].succeed()
		
		self.assertEqual(self.victory.succeeded_goals(), 1)
	
	def test_num_goals(self):
		self.assertEqual(self.victory.num_goals(), 1)
	
	def test_area_names(self):
		descriptions = [Control(AreaArgumentFactory().of([(61, 31)]).named("First Area")), Control(AreaArgumentFactory().of([(61, 31)]).named("Second Area"))]
		victory = Victory(0, descriptions)
		
		self.assertEqual(victory.area_names((61, 31)), ["First Area", "Second Area"])
	
	def test_on_failure(self):
		self.victory.enable()
		self.victory.goals[0].fail()
		
		try:
			self.assertEqual(self.on_failure_called, True)
		finally:
			self.victory.disable()
	
	def test_on_success(self):
		self.victory.enable()
		self.victory.goals[0].succeed()
		
		try:
			self.assertEqual(self.on_success_called, True)
		finally:
			self.victory.disable()
	
	def test_handlers(self):
		self.assertEqual(len(event_handler_registry.registered), self.iRegisteredHandlers + 1)
	
	def test_disable(self):
		self.assertEqual(len(event_handler_registry.registered), self.iRegisteredHandlers + 1)
	
		self.victory.disable()
		
		self.assertEqual(len(event_handler_registry.registered), self.iRegisteredHandlers)

	def test_enable(self):
		self.victory.disable()
		self.victory.enable()
		
		self.assertEqual(len(event_handler_registry.registered), self.iRegisteredHandlers + 1)


class TestHistoricalVictory(ExtendedTestCase):

	def setUp(self):
		self.descriptions = [BuildingCount(iGranary, 3), BuildingCount(iLibrary, 3)]
		self.victory = HistoricalVictory(0, self.descriptions)
		
		self.victory.victory = self.mock_victory
		self.victory.golden_age = self.golden_age
		
		self.victory_called = False
		self.golden_age_called = False
	
	def tearDown(self):
		self.victory.disable()
	
	def mock_victory(self):
		self.victory_called = True
	
	def golden_age(self):
		self.golden_age_called = True
	
	def test_succeed_and_checked(self):
		self.victory.goals[0].succeed()
		
		events.fireEvent("BeginGameTurn", 0)
		
		self.assertEqual(self.victory_called, False)
		self.assertEqual(self.golden_age_called, True)
		
		self.victory.goals[1].succeed()
		
		events.fireEvent("BeginGameTurn", 1)
		
		self.assertEqual(self.victory_called, True)
	
	def test_create(self):
		victory = HistoricalVictory.create(0)
		
		try:
			self.assertEqual(victory.iPlayer, 0)
			self.assertEqual(victory.goals, (Goal([req.CultureAmount(500)], req.CultureAmount.GOAL_DESC_KEY, 0), Goal([req.Wonder(iPyramids), req.Wonder(iGreatLibrary), req.Wonder(iGreatLighthouse)], req.Wonder.GOAL_DESC_KEY, 0), Goal([req.CultureAmount(5000)], req.CultureAmount.GOAL_DESC_KEY, 0)))
		finally:
			victory.disable()


class TestReligiousVictory(ExtendedTestCase):

	def setUp(self):
		self.descriptions = [BuildingCount(iGranary, 3)]
		self.victory = ReligiousVictory(0, self.descriptions)
		
		self.victory.victory = self.mock_victory
		
		self.victory_called = False
	
	def tearDown(self):
		self.victory.disable()
	
	def mock_victory(self):
		self.victory_called = True
	
	def test_attributes(self):
		self.assertEqual(self.victory.goals[0].mode, STATELESS)
	
	def test_succeed(self):
		cities = TestCities.num(3)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.victory.check()
			
			self.assertEqual(self.victory_called, False)
			
			events.fireEvent("BeginGameTurn", 0)
			
			self.assertEqual(self.victory_called, True)
		finally:
			cities.kill()
		
	def test_create(self):
		player(0).setLastStateReligion(iBuddhism)
		
		victory = ReligiousVictory.create(0)
		
		try:
			self.assertEqual(victory.iPlayer, 0)
			self.assertEqual(victory.goals, (
				Goal([req.PeaceTurns(100)], req.PeaceTurns.GOAL_DESC_KEY, 0), 
				Goal([req.HappiestTurns(100)], req.HappiestTurns.GOAL_DESC_KEY, 0), 
				Goal([req.AllAttitude(AttitudeTypes.ATTITUDE_CAUTIOUS)], req.AllAttitude.GOAL_DESC_KEY, 0)
			))
		finally:
			player(0).setLastStateReligion(-1)
			victory.disable()


test_cases = [
	TestVictory,
	TestHistoricalVictory,
	TestReligiousVictory,
]
