from AmountRequirements import *

from TestVictoryCommon import *


class TestGoldAmount(ExtendedTestCase):

	def setUp(self):
		self.requirement = GoldAmount(500)
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


class TestCultureAmount(ExtendedTestCase):

	def setUp(self):
		self.requirement = CultureAmount(500)
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


test_cases = [
	TestGoldAmount,
	TestCultureAmount,
]