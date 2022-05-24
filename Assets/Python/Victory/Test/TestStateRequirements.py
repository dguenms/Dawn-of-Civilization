from StateRequirements import *

from TestVictoryCommon import *


class TestFirstDiscover(ExtendedTestCase):

	def setUp(self):
		self.requirement = FirstDiscover(iEngineering)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "FirstDiscover(Engineering)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "FirstDiscover(Engineering)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Engineering")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_discover_first(self):
		team(self.iPlayer).setHasTech(iEngineering, True, self.iPlayer, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Engineering")
			
			self.assertEqual(self.requirement.state, SUCCESS)
			self.assertEqual(self.goal.checked, True)
		finally:
			team(self.iPlayer).setHasTech(iEngineering, False, self.iPlayer, True, False)
	
	def test_discover_other(self):
		team(1).setHasTech(iEngineering, True, 1, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Engineering")
			
			self.assertEqual(self.requirement.state, FAILURE)
			self.assertEqual(self.goal.failed, True)
		finally:
			team(1).setHasTech(iEngineering, False, 1, True, False)
	
	def test_discover_after(self):
		team(1).setHasTech(iEngineering, True, 1, True, False)
		team(self.iPlayer).setHasTech(iEngineering, True, self.iPlayer, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Engineering")
			
			self.assertEqual(self.requirement.state, FAILURE)
			self.assertEqual(self.goal.failed, True)
		finally:
			team(self.iPlayer).setHasTech(iEngineering, False, self.iPlayer, True, False)
			team(1).setHasTech(iEngineering, False, 1, True, False)
	
	def test_discover_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		team(1).setHasTech(iEngineering, True, 1, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Engineering")
			
			self.assertEqual(self.requirement.state, SUCCESS)
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setHasTech(iEngineering, False, 1, True, False)
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, False)


class TestSettle(ExtendedTestCase):

	def setUp(self):
		self.requirement = Settle(plots.of(TestCities.CITY_LOCATIONS).named("Test Area"))
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "Settle(Test Area)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "Settle(Test Area)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Test Area")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_settle_first(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("cityBuilt", city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Test Area")
		finally:
			city.kill()
	
	def test_settle_other(self):
		city = TestCities.one(1)
		
		try:
			events.fireEvent("cityBuilt", city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Test Area")
		finally:
			city.kill()
	
	def test_settle_after(self):
		their_city, our_city = cities = TestCities.owners(1, 0)
		
		try:
			events.fireEvent("cityBuilt", their_city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Test Area")
			
			events.fireEvent("cityBuilt", our_city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Test Area")
		finally:
			cities.kill()
	

test_cases = [
	TestFirstDiscover,
	TestSettle,
]