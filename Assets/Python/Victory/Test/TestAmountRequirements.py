from AmountRequirements import *

from TestVictoryCommon import *


class TestAverageCultureAmount(ExtendedTestCase):

	def setUp(self):
		self.requirement = AverageCultureAmount(500).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "AverageCultureAmount(500)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "AverageCultureAmount(500)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "an average culture of 500")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Average city culture: 0 / 500")
		
	def test_less(self):
		city1, city2, city3 = cities = TestCities.num(3)
		
		city1.setCulture(0, 100, True)
		city2.setCulture(0, 200, True)
		city3.setCulture(0, 300, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 200)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Average city culture: 200 / 500")
		finally:
			cities.kill()
	
	def test_more(self):
		city1, city2, city3 = cities = TestCities.num(3)
		
		city1.setCulture(0, 500, True)
		city2.setCulture(0, 1000, True)
		city3.setCulture(0, 1500, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1000)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Average city culture: 1000 / 500")
		finally:
			cities.kill()
	
	def test_other(self):
		city = TestCities.one(1)
		
		city.setCulture(1, 500, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Average city culture: 0 / 500")
		finally:
			city.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestCultureAmount(ExtendedTestCase):

	def setUp(self):
		self.requirement = CultureAmount(500).create()
		self.goal = TestGoal()
	
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CultureAmount(500)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CultureAmount(500)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "more than 500 culture")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_less(self):
		city = TestCities.one()
		city.setCulture(self.iPlayer, 100, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Total Culture: 100 / 500")
		finally:
			city.kill()
	
	def test_more(self):
		city = TestCities.one()
		city.setCulture(self.iPlayer, 1000, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1000)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Total Culture: 1000 / 500")
		finally:
			city.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)


class TestGoldAmount(ExtendedTestCase):

	def setUp(self):
		self.requirement = GoldAmount(500).create()
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
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
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


class TestShrineIncome(ExtendedTestCase):

	def setUp(self):
		self.requirement = ShrineIncome(iOrthodoxy, 2).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ShrineIncome(Orthodoxy, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ShrineIncome(Orthodoxy, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "an income of two gold from the Orthodox shrine")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_sufficient(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setHasReligion(iOrthodoxy, True, False, False)
		their_city.setHasReligion(iOrthodoxy, True, False, False)
		
		our_city.setHasRealBuilding(iOrthodoxShrine, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Orthodox shrine income: 2 / 2")
		finally:
			cities.kill()
	
	def test_different_owner(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setHasReligion(iOrthodoxy, True, False, False)
		their_city.setHasReligion(iOrthodoxy, True, False, False)
		
		their_city.setHasRealBuilding(iOrthodoxShrine, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Orthodox shrine income: 0 / 2")
		finally:
			cities.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		our_city, vassal_city = cities = TestCities.owners(0, 1)
		
		our_city.setHasReligion(iOrthodoxy, True, False, False)
		vassal_city.setHasReligion(iOrthodoxy, True, False, False)
		
		vassal_city.setHasRealBuilding(iOrthodoxShrine, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Orthodox shrine income: 2 / 2")
		finally:
			cities.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)
		


test_cases = [
	TestAverageCultureAmount,
	TestCultureAmount,
	TestGoldAmount,
	TestShrineIncome,
]