from GoalHandlers import *
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
	
	def accumulate(self, goal, *args):
		iChange = args[-1]
		self.iCount += iChange
	
	def capture(self, *args):
		self.argument = args
	
	def test_begin_player_turn(self):
		onBeginPlayerTurn = self.get("BeginPlayerTurn", self.capture)
	
		onBeginPlayerTurn((10, 1))
		self.assertEqual(self.argument, None)
		
		onBeginPlayerTurn((10, 0))
		self.assertEqual(self.argument, (self.goal, 10, 0))
	
	def test_blockade(self):
		onBlockade = self.get("blockade", self.accumulate)
		
		onBlockade((1, 100))
		self.assertEqual(self.iCount, 0)
		
		onBlockade((0, 100))
		self.assertEqual(self.iCount, 100)
		
	def test_building_built(self):
		onBuildingBuilt = self.get("buildingBuilt", self.capture)
		
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		try:
			onBuildingBuilt((their_city, iGranary))
			self.assertEqual(self.argument, None)
			
			onBuildingBuilt((our_city, iGranary))
			self.assertEqual(self.argument, (self.goal, our_city, iGranary))
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
	
	def test_city_acquired_and_kept(self):
		onCityAcquiredAndKept = self.get("cityAcquiredAndKept", self.increment)
		
		city = TestCities.one()
		
		try:
			onCityAcquiredAndKept((self.iPlayer, city))
			self.assertEqual(self.iCount, 1)
			
			onCityAcquiredAndKept((1, city))
			self.assertEqual(self.iCount, 1)
		finally:
			city.kill()
	
	def test_city_built(self):
		onCityBuilt = self.get("cityBuilt", self.increment)
		
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		try:
			onCityBuilt((our_city,))
			self.assertEqual(self.iCount, 1)
			
			onCityBuilt((their_city,))
			self.assertEqual(self.iCount, 1)
		finally:
			cities.kill()
	
	def test_city_capture_gold(self):
		onCityCaptureGold = self.get("cityCaptureGold", self.accumulate)
		
		city = TestCities.one(2)
		
		try:
			onCityCaptureGold((city, 1, 100))
			self.assertEqual(self.iCount, 0)
			
			onCityCaptureGold((city, 0, 100))
			self.assertEqual(self.iCount, 100)
		finally:
			city.kill()
	
	def test_city_lost(self):
		onCityLost = self.get("cityLost", self.capture)
		
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		try:
			onCityLost((their_city,))
			self.assertEqual(self.argument, None)
			
			onCityLost((our_city,))
			self.assertEqual(self.argument, (self.goal,))
		finally:
			cities.kill()
	
	def test_city_razed(self):
		onCityRazed = self.get("cityRazed", self.capture)
		
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		try:
			onCityRazed((our_city, 1))
			self.assertEqual(self.argument, None)
			
			onCityRazed((their_city, 0))
			self.assertEqual(self.argument, (self.goal,))
		finally:
			cities.kill()
	
	def test_combat_food(self):
		onCombatFood = self.get("combatFood", self.accumulate)
		
		unit = makeUnit(2, iSwordsman, (20, 20))
		
		try:
			onCombatFood((1, unit, 10))
			self.assertEqual(self.iCount, 0)
			
			onCombatFood((0, unit, 10))
			self.assertEqual(self.iCount, 10)
		finally:
			unit.kill(False, -1)
	
	def test_combat_gold(self):
		onCombatGold = self.get("combatGold", self.accumulate)
		
		unit = makeUnit(2, iSwordsman, (20, 20))
		
		try:
			onCombatGold((1, unit, 100))
			self.assertEqual(self.iCount, 0)
			
			onCombatGold((0, unit, 100))
			self.assertEqual(self.iCount, 100)
		finally:
			unit.kill(False, -1)
	
	def test_combat_result(self):
		onCombatResult = self.get("combatResult", self.capture)
		
		our_unit = makeUnit(0, 0, (0, 0))
		their_unit = makeUnit(1, 0, (0, 0))
		
		try:
			onCombatResult((their_unit, our_unit))
			self.assertEqual(self.argument, None)
			
			onCombatResult((our_unit, their_unit))
			self.assertEqual(self.argument, (self.goal, their_unit))
		finally:
			our_unit.kill(False, -1)
			their_unit.kill(False, -1)
	
	def test_corporation_spread(self):
		onCorporationSpread = self.get("corporationSpread", self.capture)
		
		city = TestCities.one()
		
		try:
			onCorporationSpread((iTradingCompany, 1, city))
			self.assertEqual(self.argument, None)
			
			onCorporationSpread((iTradingCompany, 0, city))
			self.assertEqual(self.argument, (self.goal, iTradingCompany,))
		finally:
			city.kill()
	
	def test_enslave(self):
		onEnslave = self.get("enslave", self.capture)
		
		unit = makeUnit(0, iSwordsman, (10, 10))
		
		try:
			onEnslave((1, unit))
			self.assertEqual(self.argument, None)
			
			onEnslave((0, unit))
			self.assertEqual(self.argument, (self.goal, unit))
		finally:
			unit.kill(False, -1)
	
	def test_first_contact(self):
		onFirstContact = self.get("firstContact", self.increment)
		
		onFirstContact((0, 1))
		self.assertEqual(self.iCount, 1)
		
		onFirstContact((1, 0))
		self.assertEqual(self.iCount, 1)
	
	def test_great_person_born(self):
		onGreatPersonBorn = self.get("greatPersonBorn", self.capture)
		
		city = TestCities.one()
		unit = makeUnit(0, iGreatArtist, (10, 10))
		
		try:
			onGreatPersonBorn((unit, 1, city))
			self.assertEqual(self.argument, None)
			
			onGreatPersonBorn((unit, 0, city))
			self.assertEqual(self.argument, (self.goal, unit))
		finally:
			city.kill()
			unit.kill(False, -1)
	
	def test_improvement_built(self):
		onImprovementBuilt = self.get("improvementBuilt", self.capture)
		
		own_plot = plot_(68, 45)
		own_plot.setOwner(0)
		own_plot.setImprovementType(iCottage)
		
		other_plot = plot(69, 45)
		other_plot.setOwner(1)
		other_plot.setImprovementType(iCottage)
		
		try:
			onImprovementBuilt((iCottage, 69, 45))
			self.assertEqual(self.argument, None)
			
			onImprovementBuilt((iCottage, 68, 45))
			self.assertEqual(self.argument, (self.goal, iCottage))
		finally:
			own_plot.setOwner(-1)
			own_plot.setImprovementType(-1)
			
			other_plot.setOwner(-1)
			other_plot.setImprovementType(-1)
	
	def test_peace_brokered(self):
		onPeaceBrokered = self.get("peaceBrokered", self.increment)
		
		onPeaceBrokered((1, 2, 3))
		self.assertEqual(self.iCount, 0)
	
		onPeaceBrokered((self.iPlayer, 1, 2))
		self.assertEqual(self.iCount, 1)
	
	def test_player_change_state_religion(self):
		onPlayerStateReligionChange = self.get("playerChangeStateReligion", self.capture)
		
		onPlayerStateReligionChange((1, iCatholicism, iOrthodoxy))
		self.assertEqual(self.argument, None)
		
		onPlayerStateReligionChange((0, iCatholicism, iOrthodoxy))
		self.assertEqual(self.argument, (self.goal, iCatholicism))
	
	def test_player_gold_trade(self):
		onPlayerGoldTrade = self.get("playerGoldTrade", self.accumulate)
		
		onPlayerGoldTrade((0, 1, 100))
		self.assertEqual(self.iCount, 0)
		
		onPlayerGoldTrade((1, 0, 100))
		self.assertEqual(self.iCount, 100)

	def test_player_slave_trade(self):
		onPlayerSlaveTrade = self.get("playerSlaveTrade", self.accumulate)
		
		onPlayerSlaveTrade((1, 100))
		self.assertEqual(self.iCount, 0)
		
		onPlayerSlaveTrade((0, 100))
		self.assertEqual(self.iCount, 100)

	def test_project_built(self):
		onProjectBuilt = self.get("projectBuilt", self.capture)
		
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		try:
			onProjectBuilt((their_city, iTheInternet))
			self.assertEqual(self.argument, None)
			
			onProjectBuilt((our_city, iTheInternet))
			self.assertEqual(self.argument, (self.goal, iTheInternet))
		finally:
			cities.kill()
	
	def test_religion_founded(self):
		onReligionFounded = self.get("religionFounded", self.capture)
		
		onReligionFounded((iBuddhism, 1))
		self.assertEqual(self.argument, None)
		
		onReligionFounded((iBuddhism, self.iPlayer))
		self.assertEqual(self.argument, (self.goal, iBuddhism))
	
	def test_sacrifice_happiness(self):
		onSacrificeHappiness = self.get("sacrificeHappiness", self.increment)
		
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		try:
			onSacrificeHappiness((1, their_city))
			self.assertEqual(self.iCount, 0)
			
			onSacrificeHappiness((0, our_city))
			self.assertEqual(self.iCount, 1)
		finally:
			cities.kill()
	
	def test_tech_acquired(self):
		onTechAcquired = self.get("techAcquired", self.capture)
		
		onTechAcquired((iEngineering, 1, 1, False))
		self.assertEqual(self.argument, None)
		
		onTechAcquired((iEngineering, self.iPlayer, self.iPlayer, False))
		self.assertEqual(self.argument, (self.goal, iEngineering, self.iPlayer))
	
	def test_trade_mission(self):
		onTradeMission = self.get("tradeMission", self.accumulate)
		
		onTradeMission((iGreatMerchant, 1, 20, 20, 100))
		self.assertEqual(self.iCount, 0)
		
		onTradeMission((iGreatMerchant, 0, 20, 20, 100))
		self.assertEqual(self.iCount, 100)
	
	def test_tribute(self):
		onTribute = self.get("tribute", self.capture)
		
		onTribute((2, 1))
		self.assertEqual(self.argument, None)
		
		onTribute((1, self.iPlayer))
		self.assertEqual(self.argument, (self.goal, self.iPlayer))
	
	def test_unit_pillage(self):
		onUnitPillage = self.get("unitPillage", self.accumulate)
		
		our_unit = makeUnit(0, iSwordsman, (20, 20))
		their_unit = makeUnit(1, iSwordsman, (25, 25))
		
		try:
			onUnitPillage((their_unit, iHamlet, -1, 1, 100))
			self.assertEqual(self.iCount, 0)
			
			onUnitPillage((our_unit, iHamlet, -1, 0, 100))
			self.assertEqual(self.iCount, 100)
		finally:
			our_unit.kill(False, -1)
			their_unit.kill(False, -1)
	
	def test_unit_spread_religion_attempt(self):
		onUnitSpreadReligionAttempt = self.get("unitSpreadReligionAttempt", self.capture)
		
		our_unit = makeUnit(0, iSwordsman, (20, 20))
		their_unit = makeUnit(1, iSwordsman, (25, 25))
		
		try:
			onUnitSpreadReligionAttempt((their_unit, iOrthodoxy, True))
			self.assertEqual(self.argument, None)
			
			onUnitSpreadReligionAttempt((our_unit, iOrthodoxy, False))
			self.assertEqual(self.argument, None)
			
			onUnitSpreadReligionAttempt((our_unit, iOrthodoxy, True))
			self.assertEqual(self.argument, (self.goal, iOrthodoxy, our_unit))
		finally:
			our_unit.kill(False, -1)
			their_unit.kill(False, -1)
		

test_cases = [
	TestHandlers,
	TestEventHandlerRegistry,
	TestEventHandlerRegistryFunctions,
]