from StateRequirements import *

from TestVictoryCommon import *


class TestContactBeforeRevealed(ExtendedTestCase):

	def setUp(self):
		self.civs = CivsArgument(iChina)
		self.area = AreaArgumentFactory().rectangle((35, 25), (40, 30)).named("Rectangle")
	
		self.requirement = ContactBeforeRevealed(self.civs, self.area).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ContactBeforeRevealed(China, Rectangle)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ContactBeforeRevealed(China, Rectangle)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "China before any of them discovers Rectangle")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Rectangle": plots.rectangle((35, 25), (40, 30))})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((35, 25)), "Rectangle")
		self.assertEqual(self.requirement.area_name((42, 42)), "")
	
	def test_contact(self):
		events.fireEvent("firstContact", self.iPlayer, team(iChina).getID())
		
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Contacted China")
		
		self.assertEqual(self.requirement.state, SUCCESS)
		self.assertEqual(self.goal.checked, True)
	
	def test_contact_other(self):
		events.fireEvent("firstContact", self.iPlayer, team(iBabylonia).getID())
		
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Contacted China")
		
		self.assertEqual(self.requirement.state, POSSIBLE)
		self.assertEqual(self.goal.checked, False)
	
	def test_contact_after_revealed(self):
		plot(35, 25).setRevealed(team(iChina).getID(), True, False, team(iChina).getID())
		
		events.fireEvent("firstContact", self.iPlayer, team(iChina).getID())
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Contacted China")
			
			self.assertEqual(self.requirement.state, FAILURE)
			self.assertEqual(self.goal.checked, True)
		finally:
			plot(35, 25).setRevealed(team(iChina).getID(), False, False, team(iChina).getID())
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		try:
			events.fireEvent("firstContact", 1, team(iChina).getID())
		
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Contacted China")
			
			self.assertEqual(self.requirement.state, SUCCESS)
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, False)


class TestConvertAfterFounding(ExtendedTestCase):

	def setUp(self):
		self.requirement = ConvertAfterFounding(iOrthodoxy, 5).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ConvertAfterFounding(Orthodoxy, 5)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ConvertAfterFounding(Orthodoxy, 5)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Orthodoxy five turns after its founding")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_convert_after_founding(self):
		game.setReligionGameTurnFounded(iOrthodoxy, 1)
		player(0).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Convert to Orthodoxy")
			
			self.assertEqual(self.requirement.state, SUCCESS)
			self.assertEqual(self.goal.checked, True)
		finally:
			player(0).setLastStateReligion(-1)
			game.setReligionGameTurnFounded(iOrthodoxy, -1)
	
	def test_convert_not_founded(self):
		player(0).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Convert to Orthodoxy")
			
			self.assertEqual(self.requirement.state, POSSIBLE)
			self.assertEqual(self.goal.checked, False)
		finally:
			player(0).setLastStateReligion(-1)
			
	def test_convert_other_religion(self):
		game.setReligionGameTurnFounded(iOrthodoxy, 1)
		game.setReligionGameTurnFounded(iCatholicism, 1)
		
		player(0).setLastStateReligion(iCatholicism)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Convert to Orthodoxy")
			
			self.assertEqual(self.requirement.state, POSSIBLE)
			self.assertEqual(self.goal.checked, False)
		finally:
			player(0).setLastStateReligion(-1)
			
			game.setReligionGameTurnFounded(iOrthodoxy, -1)
			game.setReligionGameTurnFounded(iCatholicism, -1)
	
	def test_convert_early_enough(self):
		game.setReligionGameTurnFounded(iOrthodoxy, turn()-2)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Convert to Orthodoxy")
			
			self.assertEqual(self.requirement.state, SUCCESS)
			self.assertEqual(self.goal.checked, True)
		finally:
			player(0).setLastStateReligion(-1)
			
			game.setReligionGameTurnFounded(iOrthodoxy, -1)
	
	def test_convert_too_late(self):
		game.setReligionGameTurnFounded(iOrthodoxy, turn()-10)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Convert to Orthodoxy")
			
			self.assertEqual(self.requirement.state, POSSIBLE)
			self.assertEqual(self.goal.checked, False)
		finally:
			player(0).setLastStateReligion(-1)
			
			game.setReligionGameTurnFounded(iOrthodoxy, -1)
	
	def test_expire_not_founded(self):
		events.fireEvent("BeginPlayerTurn", turn(), 0)
		
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Convert to Orthodoxy")
		
		self.assertEqual(self.requirement.state, POSSIBLE)
		self.assertEqual(self.goal.failed, False)
	
	def test_expire_too_early(self):
		game.setReligionGameTurnFounded(iOrthodoxy, turn()-1)
		
		try:
			events.fireEvent("BeginPlayerTurn", turn(), 0)
		
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Convert to Orthodoxy")
			
			self.assertEqual(self.requirement.state, POSSIBLE)
			self.assertEqual(self.goal.failed, False)
		finally:
			game.setReligionGameTurnFounded(iOrthodoxy, -1)
	
	def test_expire_too_late(self):
		game.setReligionGameTurnFounded(iOrthodoxy, turn()-10)
		
		try:
			events.fireEvent("BeginPlayerTurn", turn(), 0)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Convert to Orthodoxy")
			
			self.assertEqual(self.requirement.state, FAILURE)
			self.assertEqual(self.goal.failed, True)
		finally:
			game.setReligionGameTurnFounded(iOrthodoxy, -1)
	
	def test_expire_already_succeeded(self):
		game.setReligionGameTurnFounded(iOrthodoxy, turn()-2)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		try:
			events.fireEvent("BeginPlayerTurn", turn(), 0)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Convert to Orthodoxy")
			
			self.assertEqual(self.requirement.state, SUCCESS)
			self.assertEqual(self.goal.checked, True)
			self.assertEqual(self.goal.failed, False)
		finally:
			game.setReligionGameTurnFounded(iOrthodoxy, -1)
			player(0).setLastStateReligion(-1)
	
	def test_convert_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
	
		game.setReligionGameTurnFounded(iOrthodoxy, 1)
		
		player(1).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Convert to Orthodoxy")
			
			self.assertEqual(self.requirement.state, SUCCESS)
			self.assertEqual(self.goal.checked, True)
		finally:
			player(1).setLastStateReligion(-1)
			game.setReligionGameTurnFounded(iOrthodoxy, -1)
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestDiscover(ExtendedTestCase):

	def setUp(self):
		self.requirement = Discover(iEngineering).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "Discover(Engineering)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "Discover(Engineering)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Engineering")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_discover(self):
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
		
			self.assertEqual(self.requirement.state, POSSIBLE)
			self.assertEqual(self.goal.checked, False)
		finally:
			team(1).setHasTech(iEngineering, False, 1, True, False)
	
	def test_discover_after(self):
		team(1).setHasTech(iEngineering, True, 1, True, False)
		team(self.iPlayer).setHasTech(iEngineering, True, self.iPlayer, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Engineering")
			
			self.assertEqual(self.requirement.state, SUCCESS)
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setHasTech(iEngineering, False, 1, True, False)
			team(self.iPlayer).setHasTech(iEngineering, False, self.iPlayer, True, False)
	
	def test_other_evaluator(self):
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


class TestEnterEraBefore(ExtendedTestCase):

	def setUp(self):
		self.requirement = EnterEraBefore(iClassical, iMedieval).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "EnterEraBefore(Classical, Medieval)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "EnterEraBefore(Classical, Medieval)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "the Classical era before anyone enters the Medieval era")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_enter_before(self):
		events.fireEvent("techAcquired", iLaw, 0, 0, False)
		
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Classical era")
		
		self.assertEqual(self.requirement.state, SUCCESS)
		self.assertEqual(self.goal.checked, True)
	
	def test_enter_before_other_player(self):
		events.fireEvent("techAcquired", iLaw, 1, 1, False)
		
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Classical era")
		
		self.assertEqual(self.requirement.state, POSSIBLE)
		self.assertEqual(self.goal.checked, False)
	
	def test_expire(self):
		events.fireEvent("techAcquired", iFeudalism, 1, 1, False)
		
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Classical era")
		
		self.assertEqual(self.requirement.state, FAILURE)
		self.assertEqual(self.goal.failed, True)
	
	def test_enter_after_expire(self):
		events.fireEvent("techAcquired", iFeudalism, 1, 1, False)
		events.fireEvent("techAcquired", iLaw, 0, 0, False)
		
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Classical era")
		
		self.assertEqual(self.requirement.state, FAILURE)
		self.assertEqual(self.goal.failed, True)
	
	def test_expire_after_enter(self):
		events.fireEvent("techAcquired", iLaw, 0, 0, False)
		events.fireEvent("techAcquired", iFeudalism, 1, 1, False)
		
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Classical era")
		
		self.assertEqual(self.requirement.state, SUCCESS)
		self.assertEqual(self.goal.checked, True)
	
	def test_enter_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		try:
			events.fireEvent("techAcquired", iLaw, 1, 1, False)
			
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Classical era")
		finally:
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestFirstDiscover(ExtendedTestCase):

	def setUp(self):
		self.requirement = FirstDiscover(iEngineering).create()
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
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
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


class TestFirstGreatPerson(ExtendedTestCase):

	class TestGoalRequired(TestGoal):
	
		def __init__(self, requirement):
			TestGoal.__init__(self)
			
			self.requirements = [requirement]
			self.required = 1

	def setUp(self):
		self.requirement = FirstGreatPerson(iGreatScientist).create()
		self.goal = self.TestGoalRequired(self.requirement)
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "FirstGreatPerson(Great Scientist)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "FirstGreatPerson(Great Scientist)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Great Scientist")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_first(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_scientist = makeUnit(0, iGreatScientist, (10, 10))
		their_scientist = makeUnit(1, iGreatScientist, (11, 11))
		
		try:
			events.fireEvent("greatPersonBorn", our_scientist, 0, our_city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Great Scientist")
			self.assertEqual(self.requirement.state, SUCCESS)
			
			self.assertEqual(self.goal.checked, True)
			
			events.fireEvent("greatPersonBorn", their_scientist, 1, their_city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.state, SUCCESS)
		finally:
			our_scientist.kill(False, -1)
			their_scientist.kill(False, -1)
			cities.kill()
	
	def test_not_first(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_scientist = makeUnit(0, iGreatScientist, (10, 10))
		their_scientist = makeUnit(1, iGreatScientist, (11, 11))
		
		try:
			events.fireEvent("greatPersonBorn", their_scientist, 1, their_city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Great Scientist")
			self.assertEqual(self.requirement.state, FAILURE)
			
			self.assertEqual(self.goal.failed, True)
			
			events.fireEvent("greatPersonBorn", our_scientist, 0, our_city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.state, FAILURE)
		finally:
			our_scientist.kill(False, -1)
			their_scientist.kill(False, -1)
			cities.kill()
	
	def test_different_unit(self):
		city = TestCities.one()
		merchant = makeUnit(0, iGreatMerchant, (10, 10))
		
		try:
			events.fireEvent("greatPersonBorn", merchant, 0, city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Great Scientist")
			self.assertEqual(self.requirement.state, POSSIBLE)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
			merchant.kill(False, -1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		city = TestCities.one(1)
		scientist = makeUnit(1, iGreatScientist, (10, 10))
		
		try:
			events.fireEvent("greatPersonBorn", scientist, 1, city)
			
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Great Scientist")
			self.assertEqual(self.requirement.state, SUCCESS)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			scientist.kill(False, -1)
			city.kill()
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestFirstSettle(ExtendedTestCase):

	def setUp(self):
		self.area = AreaArgumentFactory().of(TestCities.CITY_LOCATIONS).named("Test Area")
		self.requirement = FirstSettle(self.area).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "FirstSettle(Test Area)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "FirstSettle(Test Area)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "a city in Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots.of(TestCities.CITY_LOCATIONS)})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_settle_first(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		try:
			events.fireEvent("cityBuilt", our_city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Test Area")
			self.assertEqual(self.requirement.state, SUCCESS)
			self.assertEqual(self.goal.checked, True)
			
			events.fireEvent("cityBuilt", their_city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Test Area")
			self.assertEqual(self.requirement.state, SUCCESS)
		finally:
			cities.kill()
	
	def test_settle_first_other(self):
		their_city, our_city = cities = TestCities.owners(1, 0)
		
		try:
			events.fireEvent("cityBuilt", their_city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Test Area")
			self.assertEqual(self.requirement.state, FAILURE)
			self.assertEqual(self.goal.failed, True)
			
			events.fireEvent("cityBuilt", our_city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Test Area")
			self.assertEqual(self.requirement.state, FAILURE)
		finally:
			cities.kill()
	
	def test_settle_first_other_minor(self):
		their_city, our_city = cities = TestCities.owners(iNative, self.iPlayer)
		
		try:
			events.fireEvent("cityBuilt", their_city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Test Area")
			self.assertEqual(self.requirement.state, POSSIBLE)
			self.assertEqual(self.goal.failed, False)
			
			events.fireEvent("cityBuilt", our_city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Test Area")
			self.assertEqual(self.requirement.state, SUCCESS)
			self.assertEqual(self.goal.checked, True)
		finally:
			cities.kill()
	
	def test_settle_first_other_allowed(self):
		requirement = FirstSettle(self.area, allowed=[civ(1)])
		goal = TestGoal()
		
		requirement.register_handlers(goal)
		
		their_city, our_city = cities = TestCities.owners(1, 0)
		
		try:
			events.fireEvent("cityBuilt", their_city)
			
			self.assertEqual(requirement.fulfilled(self.evaluator), False)
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Test Area")
			self.assertEqual(requirement.state, POSSIBLE)
			self.assertEqual(goal.failed, False)
			
			events.fireEvent("cityBuilt", our_city)
			
			self.assertEqual(requirement.fulfilled(self.evaluator), True)
			self.assertEqual(requirement.progress(self.evaluator), self.SUCCESS + "Test Area")
			self.assertEqual(requirement.state, SUCCESS)
			self.assertEqual(goal.checked, True)
		finally:
			cities.kill()
			requirement.deregister_handlers()
	
	def test_conquest(self):
		city = TestCities.one(iNative)
		city.setPopulation(2)
		
		self.player.acquireCity(city, True, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Test Area")
			self.assertEqual(self.requirement.state, POSSIBLE)
			self.assertEqual(self.goal.failed, False)
		finally:
			TestCities.city(0).kill()
	
	def test_settle_after_conquest(self):
		their_city, our_city = TestCities.owners(iNative, self.iPlayer)
		their_city.setPopulation(2)
		
		self.player.acquireCity(their_city, True, False)
		
		try:
			events.fireEvent("cityBuilt", our_city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Test Area")
			self.assertEqual(self.requirement.state, SUCCESS)
			self.assertEqual(self.goal.checked, True)
		finally:
			TestCities.city(0).kill()
			our_city.kill()
	
	def test_settle_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		city = TestCities.one(1)
		
		try:
			events.fireEvent("cityBuilt", city)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Test Area")
			self.assertEqual(self.requirement.state, SUCCESS)
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestFirstTribute(ExtendedTestCase):

	def setUp(self):
		self.requirement = FirstTribute().create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "FirstTribute()")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "FirstTribute()")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "the first to receive tribute in a peace treaty")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_initial(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Tribute received")
		self.assertEqual(self.requirement.state, POSSIBLE)
		self.assertEqual(self.goal.checked, False)
	
	def test_first_tribute(self):
		print "test first tribute"
		events.fireEvent("tribute", 1, 0)
		
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Tribute received")
		self.assertEqual(self.requirement.state, SUCCESS)
		self.assertEqual(self.goal.checked, True)
	
	def test_first_tribute_other(self):
		events.fireEvent("tribute", 2, 1)
		
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Tribute received")
		self.assertEqual(self.requirement.state, FAILURE)
		self.assertEqual(self.goal.failed, True)


class TestFound(ExtendedTestCase):

	def setUp(self):
		self.requirement = Found(iBuddhism).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "Found(Buddhism)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "Found(Buddhism)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Buddhism")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_not_founded(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Buddhism")
		self.assertEqual(self.requirement.state, POSSIBLE)
		
		self.assertEqual(self.goal.failed, False)
	
	def test_founded(self):
		events.fireEvent("religionFounded", iBuddhism, self.iPlayer)
		
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Buddhism")
		self.assertEqual(self.requirement.state, SUCCESS)
		
		self.assertEqual(self.goal.checked, True)
	
	def test_founded_other_religion(self):
		events.fireEvent("religionFounded", iHinduism, self.iPlayer)
		
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Buddhism")
		self.assertEqual(self.requirement.state, POSSIBLE)
		
		self.assertEqual(self.goal.failed, False)
	
	def test_founded_other_player(self):
		events.fireEvent("religionFounded", iBuddhism, 1)
		
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Buddhism")
		self.assertEqual(self.requirement.state, FAILURE)
		
		self.assertEqual(self.goal.failed, True)


class TestNoCityConquered(ExtendedTestCase):

	def setUp(self):
		self.requirement = NoCityConquered().create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "NoCityConquered()")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "NoCityConquered()")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "never conquer any cities")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_no_city_conquered(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "No cities conquered")
		self.assertEqual(self.requirement.state, POSSIBLE)
		
		self.assertEqual(self.goal.failed, False)
	
	def test_city_conquered(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city, True, False)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "No cities conquered")
			self.assertEqual(self.requirement.state, FAILURE)
			
			self.assertEqual(self.goal.failed, True)
		finally:
			city.kill()
	
	def test_city_acquired(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city, False, True)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "No cities conquered")
			self.assertEqual(self.requirement.state, POSSIBLE)
			
			self.assertEqual(self.goal.failed, False)
		finally:
			city.kill()
	
	def test_city_conquered_other(self):
		city = TestCities.one(1)
		
		try:
			events.fireEvent("cityAcquired", 0, 1, city, True, False)
			
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "No cities conquered")
			self.assertEqual(self.requirement.state, POSSIBLE)
			
			self.assertEqual(self.goal.failed, False)
		finally:
			city.kill()
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestNoCityLost(ExtendedTestCase):

	def setUp(self):
		self.requirement = NoCityLost().create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "NoCityLost()")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "NoCityLost()")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "never lose a city")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_no_city_lost(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "No city lost")
		self.assertEqual(self.requirement.state, POSSIBLE)
	
	def test_city_lost(self):
		city = TestCities.one()
	
		try:
			events.fireEvent("cityLost", city)
		
			self.assertEqual(self.requirement.state, FAILURE)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "No city lost")
			self.assertEqual(self.requirement.state, FAILURE)
			self.assertEqual(self.goal.failed, True)
		finally:
			city.kill()
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestSettle(ExtendedTestCase):

	def setUp(self):
		self.area = AreaArgumentFactory().of(TestCities.CITY_LOCATIONS).named("Test Area")
		self.requirement = Settle(self.area).create()
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
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots.of(TestCities.CITY_LOCATIONS)})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((57, 35)), "Test Area")
		self.assertEqual(self.requirement.area_name((58, 36)), "")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_settle(self):
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
	

test_cases = [
	TestContactBeforeRevealed,
	TestConvertAfterFounding,
	TestDiscover,
	TestEnterEraBefore,
	TestFirstDiscover,
	TestFirstGreatPerson,
	TestFirstSettle,
	TestFirstTribute,
	TestFound,
	TestNoCityConquered,
	TestNoCityLost,
	TestSettle,
]