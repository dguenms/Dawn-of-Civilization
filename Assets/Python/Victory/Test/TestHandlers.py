from VictoryHandlers import *
from Requirements import *

from TestVictoryCommon import *


class TestHandlers(ExtendedTestCase):

	def setUp(self):
		self.handlers = Handlers()
	
	def test_func(self):
		pass
	
	def test_add(self):
		self.handlers.add("event", self.test_func)
		
		self.assertEqual(self.handlers.handlers, [("event", self.test_func)])
	
	def test_add_other(self):
		self.handlers.add_other("event", self.test_func)
		
		self.assertEqual(self.handlers.other_handlers, [("event", self.test_func)])
	
	def test_add_any(self):
		self.handlers.add_any("event", self.test_func)
		
		self.assertEqual(self.handlers.any_handlers, [("event", self.test_func)])
	
	def test_len(self):
		self.handlers.add("event", self.test_func)
		self.handlers.add_other("event", self.test_func)
		self.handlers.add_any("event", self.test_func)
		
		self.assertEqual(len(self.handlers), 3)


class TestEventHandlerRegistry(ExtendedTestCase):

	def setUp(self):
		self.registry = EventHandlerRegistry()
		self.goal = TestGoal()
	
	def get_num_registered_handlers(self):
		return sum(len(events.EventHandlerMap[event]) for event in events.EventHandlerMap)
	
	def test_applicable(self):
		self.assertEqual(self.registry.applicable(self.goal, self.iPlayer), True)
		self.assertEqual(self.registry.applicable(self.goal, 1), False)
	
	def test_applicable_other(self):
		self.assertEqual(self.registry.applicable_other(self.goal, self.iPlayer), False)
		self.assertEqual(self.registry.applicable_other(self.goal, 1), True)
	
	def test_applicable_any(self):
		self.assertEqual(self.registry.applicable_any(self.goal, self.iPlayer), True)
		self.assertEqual(self.registry.applicable_any(self.goal, 1), True)
	
	def test_applicable_other_evaluator(self):
		self.goal.evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		try:
			self.assertEqual(self.registry.applicable(self.goal, 0), True)
			self.assertEqual(self.registry.applicable(self.goal, 1), True)
			self.assertEqual(self.registry.applicable(self.goal, 2), False)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_applicable_other_other_evaluator(self):
		self.goal.evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		try:
			self.assertEqual(self.registry.applicable_other(self.goal, 0), False)
			self.assertEqual(self.registry.applicable_other(self.goal, 1), False)
			self.assertEqual(self.registry.applicable_other(self.goal, 2), True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_applicable_any_other_evaluator(self):
		self.goal.evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		try:
			self.assertEqual(self.registry.applicable_any(self.goal, 0), True)
			self.assertEqual(self.registry.applicable_any(self.goal, 1), True)
			self.assertEqual(self.registry.applicable_any(self.goal, 2), True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_get(self):
		city = TestCities.one()
		
		def handler(goal, city, iBuilding):
			if iBuilding == iGranary:
				goal.check()
		
		try:
			handler_func = self.registry.get(self.goal, self.registry.applicable, "buildingBuilt", handler)
			
			handler_func((city, iLibrary))
			self.assertEqual(self.goal.checked, False)
			
			handler_func((city, iGranary))
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_get_other(self):
		city = TestCities.one(iOwner = 1)
		
		def handler(goal, city, iBuilding):
			if iBuilding == iGranary:
				goal.check()
		
		try:
			handler_func = self.registry.get(self.goal, self.registry.applicable_other, "buildingBuilt", handler)
			
			handler_func((city, iGranary))
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_get_nonexistent(self):
		def handler(*args):
			pass
		
		self.assertRaises(ValueError, self.registry.get, self.goal, self.registry.applicable, "nonexistentEvent", handler)
	
	def test_register_deregister(self):
		requirement = BuildingCount(iGranary, 3)
		city = TestCities.one()
		
		def handler(goal, city, iBuilding):
			goal.check()

		try:
			iNumHandlers = self.get_num_registered_handlers()
			
			self.registry.register(requirement, self.goal)
			self.assertEqual(self.get_num_registered_handlers(), iNumHandlers + len(requirement.handlers))
			
			self.registry.deregister(requirement)
			self.assertEqual(self.get_num_registered_handlers(), iNumHandlers)
		finally:
			city.kill()
	

class TestEventHandlerRegistryFunctions(ExtendedTestCase):

	def setUp(self):
		self.registry = EventHandlerRegistry()		
		self.goal = TestGoal()
		
		self.iCount = 0
		self.argument = None
	
	def get(self, event, func):
		return self.registry.get(self.goal, self.registry.applicable, event, func)
	
	def increment(self, *args):
		self.iCount += 1
	
	def accumulate(self, goal, iChange):
		self.iCount += iChange
	
	def capture(self, *args):
		self.argument = args
	
	def test_begin_player_turn(self):
		onBeginPlayerTurn = self.get("BeginPlayerTurn", self.capture)
	
		onBeginPlayerTurn((10, 1))
		self.assertEqual(self.argument, None)
		
		onBeginPlayerTurn((10, 0))
		self.assertEqual(self.argument, (self.goal, 10))
		
	def test_building_built(self):
		onBuildingBuilt = self.get("buildingBuilt", self.capture)
		
		ourCity, theirCity = cities = TestCities.owners(0, 1)
		
		try:
			onBuildingBuilt((theirCity, iGranary))
			self.assertEqual(self.argument, None)
			
			onBuildingBuilt((ourCity, iGranary))
			self.assertEqual(self.argument, (self.goal, ourCity, iGranary))
		finally:
			cities.kill()
	
	def test_city_acquired(self):
		onCityAcquired = self.get("cityAcquired", self.increment)
		
		city = TestCities.one()
		
		try:
			onCityAcquired((self.iPlayer, 1, city, True, False))
			self.assertEqual(self.iCount, 0)
			
			onCityAcquired((1, self.iPlayer, city, True, False))
			self.assertEqual(self.iCount, 1)
		finally:
			city.kill()
	
	def test_peace_brokered(self):
		onPeaceBrokered = self.get("peaceBrokered", self.increment)
		
		onPeaceBrokered((1, 2, 3))
		self.assertEqual(self.iCount, 0)
	
		onPeaceBrokered((self.iPlayer, 1, 2))
		self.assertEqual(self.iCount, 1)
	
	def test_tech_acquired(self):
		onTechAcquired = self.get("techAcquired", self.capture)
		
		onTechAcquired((iEngineering, 1, 1, False))
		self.assertEqual(self.argument, None)
		
		onTechAcquired((iEngineering, self.iPlayer, self.iPlayer, False))
		self.assertEqual(self.argument, (self.goal, iEngineering))
		

test_cases = [
	TestHandlers,
	TestEventHandlerRegistry,
	TestEventHandlerRegistryFunctions,
]