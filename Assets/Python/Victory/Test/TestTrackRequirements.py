from TrackRequirements import *

from TestVictoryCommon import *
	

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
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
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


class TestEraFirstDiscover(ExtendedTestCase):

	def setUp(self):
		self.requirement = EraFirstDiscover(iClassical, 2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "EraFirstDiscover(Classical, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "EraFirstDiscover(Classical, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Classical era technologies")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 0 / 2 (21 remaining)")
		self.assertEqual(self.goal.checked, False)
	
	def test_fewer(self):
		team(0).setHasTech(iLaw, True, 0, True, False)
	
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 1 / 2 (20 remaining)")
			self.assertEqual(self.goal.checked, True)
		finally:
			team(0).setHasTech(iLaw, False, 0, True, False)
	
	def test_more(self):
		lTechs = [iLaw, iCurrency, iPhilosophy]
		for iTech in lTechs:
			team(0).setHasTech(iTech, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Classical technologies discovered first: 3 / 2 (18 remaining)")
			self.assertEqual(self.goal.checked, True)
		finally:
			for iTech in lTechs:
				team(0).setHasTech(iTech, False, 0, True, False)
	
	def test_other(self):
		team(1).setHasTech(iLaw, True, 1, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 0 / 2 (20 remaining)")
			self.assertEqual(self.goal.checked, False)
		finally:
			team(1).setHasTech(iLaw, False, 1, True, False)
	
	def test_after_other(self):
		team(1).setHasTech(iLaw, True, 1, True, False)
		team(0).setHasTech(iLaw, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 0 / 2 (20 remaining)")
			self.assertEqual(self.goal.checked, False)
		finally:
			team(1).setHasTech(iLaw, False, 1, True, False)
			team(0).setHasTech(iLaw, False, 0, True, False)
	
	def test_different_era(self):
		team(0).setHasTech(iFeudalism, True, 0, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 0 / 2 (21 remaining)")
			self.assertEqual(self.goal.checked, False)
		finally:
			team(0).setHasTech(iFeudalism, False, 0, True, False)
	
	def test_not_enough_remaining(self):
		requirement = EraFirstDiscover(iClassical, 20)
		requirement.register_handlers(self.goal)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		
		try:
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 0 / 20 (20 remaining)")
			self.assertEqual(self.goal.failed, False)
			
			team(1).setHasTech(iCurrency, True, 1, True, False)
			
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 0 / 20 (19 remaining)")
			self.assertEqual(self.goal.failed, True)
		finally:
			for iTech in [iLaw, iCurrency]:
				team(1).setHasTech(iTech, False, 1, True, False)
	
	def test_not_enough_remaining_with_discovered(self):
		requirement = EraFirstDiscover(iClassical, 20)
		requirement.register_handlers(self.goal)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		
		try:
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 1 / 20 (20 remaining)")
			self.assertEqual(self.goal.failed, False)
			
			team(1).setHasTech(iCurrency, True, 1, True, False)
			
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 1 / 20 (19 remaining)")
			self.assertEqual(self.goal.failed, False)
			
			team(1).setHasTech(iPhilosophy, True, 1, True, False)
			
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Classical technologies discovered first: 1 / 20 (18 remaining)")
			self.assertEqual(self.goal.failed, True)
		finally:
			team(0).setHasTech(iLaw, False, 0, True, False)
			for iTech in [iCurrency, iPhilosophy]:
				team(1).setHasTech(iTech, False, 1, True, False)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		lTechs = [iLaw, iCurrency]
		for iTech in lTechs:
			team(1).setHasTech(iTech, True, 1, True, False)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Classical technologies discovered first: 2 / 2 (19 remaining)")
			self.assertEqual(self.goal.checked, True)
		finally:
			for iTech in lTechs:
				team(1).setHasTech(iTech, False, 1, True, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestGoldenAges(ExtendedTestCase):

	def setUp(self):
		self.requirement = GoldenAges(2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "GoldenAges(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "GoldenAges(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Golden Ages")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_no_golden_age(self):
		for _ in range(8):
			events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
	
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Golden Ages: 0 / 2")
		
		self.assertEqual(self.goal.checked, False)
	
	def test_golden_age(self):
		self.player.changeGoldenAgeTurns(1)
		
		try:
			for _ in range(16):
				events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 16)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Golden Ages: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			self.player.changeGoldenAgeTurns(-1)
	
	def test_golden_age_and_anarchy(self):
		self.player.changeGoldenAgeTurns(1)
		self.player.changeAnarchyTurns(1)
		
		try:
			for _ in range(8):
				events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Golden Ages: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			self.player.changeGoldenAgeTurns(-1)
			self.player.changeAnarchyTurns(-1)


class TestSunkShips(ExtendedTestCase):

	def setUp(self):
		self.requirement = SunkShips(2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "SunkShips(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "SunkShips(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two enemy ships")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_sink_enemy_ship(self):
		our_ship = makeUnit(0, iWarGalley, (3, 3))
		their_ship = makeUnit(1, iGalley, (3, 4))
		
		try:
			events.fireEvent("combatResult", our_ship, their_ship)
			events.fireEvent("combatResult", our_ship, their_ship)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Enemy ships sunk: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			our_ship.kill(False, -1)
			their_ship.kill(False, -1)
	
	def test_sink_ship_other_player(self):
		their_ship = makeUnit(1, iWarGalley, (3, 3))
		other_ship = makeUnit(2, iGalley, (3, 4))
		
		try:
			events.fireEvent("combatResult", their_ship, other_ship)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Enemy ships sunk: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			their_ship.kill(False, -1)
			other_ship.kill(False, -1)
	
	def test_defeat_land_unit(self):
		our_unit = makeUnit(0, iSwordsman, (61, 31))
		their_unit = makeUnit(1, iLightSwordsman, (62, 31))
		
		try:
			events.fireEvent("combatResult", our_unit, their_unit)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Enemy ships sunk: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			our_unit.kill(False, -1)
			their_unit.kill(False, -1)
	
	def test_sink_enemy_ship_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		vassal_ship = makeUnit(1, iWarGalley, (3, 3))
		enemy_ship = makeUnit(2, iGalley, (3, 4))
		
		try:
			events.fireEvent("combatResult", vassal_ship, enemy_ship)
			events.fireEvent("combatResult", vassal_ship, enemy_ship)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Enemy ships sunk: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			vassal_ship.kill(False, -1)
			enemy_ship.kill(False, -1)
			
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestTradeGold(ExtendedTestCase):

	def setUp(self):
		self.requirement = TradeGold(100)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tear_down(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "TradeGold(100)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "TradeGold(100)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "100 gold by trade")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_player_gold_trade(self):
		events.fireEvent("playerGoldTrade", 1, 0, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from trade: 100 / 100")
		
		self.assertEqual(self.goal.checked, True)
		
	def test_player_gold_trade_other(self):
		events.fireEvent("playerGoldTrade", 0, 1, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from trade: 0 / 100")
		
		self.assertEqual(self.goal.checked, False)
	
	def test_player_gold_trade_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		try:
			events.fireEvent("playerGoldTrade", 2, 1, 100)
		
			self.assertEqual(self.requirement.evaluate(evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Gold from trade: 100 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_trade_mission(self):
		city = TestCities.one(1)
		events.fireEvent("tradeMission", iGreatMerchant, 0, city.getX(), city.getY(), 100)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from trade: 100 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_trade_mission_other(self):
		city = TestCities.one()
		events.fireEvent("tradeMission", iGreatMerchant, 1, city.getX(), city.getY(), 100)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from trade: 0 / 100")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_trade_mission_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		city = TestCities.one(2)
		
		try:
			events.fireEvent("tradeMission", iGreatMerchant, 1, city.getX(), city.getY(), 100)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Gold from trade: 100 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_trade_deal(self):
		player(0).changeGoldPerTurnByPlayer(1, 100)
		
		try:
			events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from trade: 100 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			player(0).changeGoldPerTurnByPlayer(1, -100)
	
	def test_trade_deal_other(self):
		player(1).changeGoldPerTurnByPlayer(2, 100)
		
		try:
			events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from trade: 0 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			player(1).changeGoldPerTurnByPlayer(2, -100)
	
	def test_trade_deal_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		player(1).changeGoldPerTurnByPlayer(2, 100)
		
		try:
			events.fireEvent("BeginPlayerTurn", 0, 1)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Gold from trade: 100 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			player(1).changeGoldPerTurnByPlayer(2, -100)
			team(1).setVassal(0, False, False)
	
	def test_trade_route(self):
		city1, city2 = cities = TestCities.num(2)
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		player(0).setCivics(iCivicsEconomy, iFreeEnterprise)
		player(0).setCommercePercent(CommerceTypes.COMMERCE_GOLD, 100)
		
		try:
			self.assertEqual(city1.getTradeYield(YieldTypes.YIELD_COMMERCE) > 0, True)
			self.assertEqual(city2.getTradeYield(YieldTypes.YIELD_COMMERCE) > 0, True)
			
			iExpectedCommerce = city1.getTradeYield(YieldTypes.YIELD_COMMERCE) + city2.getTradeYield(YieldTypes.YIELD_COMMERCE)
			iExpectedCommerce *= player(0).getCommercePercent(CommerceTypes.COMMERCE_GOLD)
			iExpectedCommerce /= 100
			
			self.assertEqual(iExpectedCommerce > 0, True)
			
			events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), iExpectedCommerce)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from trade: %d / 100" % iExpectedCommerce)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			player(0).setCivics(iCivicsEconomy, iReciprocity)
			player(0).setCommercePercent(CommerceTypes.COMMERCE_RESEARCH, 100)
			
			plot(62, 31).setRouteType(-1)
			
			cities.kill()
			
	def test_trade_route_other(self):
		city1, city2 = cities = TestCities.owners(1, 1)
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		player(1).setCivics(iCivicsEconomy, iFreeEnterprise)
		player(1).setCommercePercent(CommerceTypes.COMMERCE_GOLD, 100)
		
		try:
			self.assertEqual(city1.getTradeYield(YieldTypes.YIELD_COMMERCE) > 0, True)
			self.assertEqual(city2.getTradeYield(YieldTypes.YIELD_COMMERCE) > 0, True)
			
			events.fireEvent("BeginPlayerTurn", 0, 0)
			events.fireEvent("BeginPlayerTurn", 0, 1)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from trade: 0 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			player(1).setCivics(iCivicsEconomy, iReciprocity)
			player(1).setCommercePercent(CommerceTypes.COMMERCE_RESEARCH, 100)
			
			plot(62, 31).setRouteType(-1)
			
			cities.kill()
			

test_cases = [
	TestBrokeredPeace,
	TestGoldenAges,
	TestEraFirstDiscover,
	TestSunkShips,
	TestTradeGold,
]