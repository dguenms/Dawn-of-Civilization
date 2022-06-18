from TrackRequirements import *

from TestVictoryCommon import *


class TestAcquiredCities(ExtendedTestCase):

	def setUp(self):
		self.requirement = AcquiredCities(2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "AcquiredCities(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "AcquiredCities(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two cities")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_city_acquired(self):
		city1, city2 = cities = TestCities.owners(1, 1)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
		
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Acquired cities: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			cities.kill()
	
	def test_city_built(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityBuilt", city1)
			events.fireEvent("cityBuilt", city2)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Acquired cities: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			cities.kill()
	
	def test_same_city_twice(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("cityBuilt", city)
			events.fireEvent("cityBuilt", city)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Acquired cities: 1 / 2")
		finally:
			city.kill()
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)
	

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


class TestConqueredCities(ExtendedTestCase):

	def setUp(self):
		self.requirement = ConqueredCities(2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ConqueredCities(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ConqueredCities(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two cities")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_record_conquered(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
		
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Conquered cities: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			cities.kill()
	
	def test_peacefully_acquired(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, False, True)
			events.fireEvent("cityAcquired", 1, 0, city2, False, True)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Conquered cities: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			cities.kill()
	
	def test_different_owner(self):
		city1, city2 = cities = TestCities.owners(1, 1)
		
		try:
			events.fireEvent("cityAcquired", 0, 1, city1, True, False)
			events.fireEvent("cityAcquired", 0, 1, city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Conquered cities: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			cities.kill()
	
	def test_owner_changes_after_conquest(self):
		city1, city2 = cities = TestCities.owners(1, 1)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Conquered cities: 0 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			cities.kill()
			
	def test_city_destroyed_after_conquest(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Conquered cities: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
			
			city2.kill()
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 1)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Conquered cities: 1 / 2")
		finally:
			city1.kill()
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestConqueredCitiesInside(ExtendedTestCase):

	def setUp(self):
		self.area = plots.of([(61, 31), (63, 31)]).named("Test Area")
		self.requirement = ConqueredCities(2, inside=self.area)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two cities in Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots_.of([(61, 31), (63, 31)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((61, 31)), "Test Area")
		self.assertEqual(self.requirement.area_name((10, 10)), "")
	
	def test_conquer_in_area(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Conquered cities in Test Area: 2 / 2")
		finally:
			cities.kill()
	
	def test_conquer_not_in_area(self):
		_, _, city1, city2 = cities = TestCities.num(4)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Conquered cities in Test Area: 0 / 2")
		finally:
			cities.kill()


class TestConqueredCitiesOutside(ExtendedTestCase):

	def setUp(self):
		self.area = plots.all().without([(61, 31), (63, 31)]).named("Test Area")
		self.requirement = ConqueredCities(2, outside=self.area)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two cities outside of Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots_.of([(61, 31), (63, 31)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((61, 31)), "Test Area")
		self.assertEqual(self.requirement.area_name((10, 10)), "")
	
	def test_conquer_outside_area(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Conquered cities outside of Test Area: 2 / 2")
		finally:
			cities.kill()
	
	def test_conquer_not_in_area(self):
		_, _, city1, city2 = cities = TestCities.num(4)
		
		try:
			events.fireEvent("cityAcquired", 1, 0, city1, True, False)
			events.fireEvent("cityAcquired", 1, 0, city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Conquered cities outside of Test Area: 0 / 2")
		finally:
			cities.kill()


class TestConqueredCitiesCivs(ExtendedTestCase):

	def setUp(self):
		self.civs = CivsDefinition(1).named("Test Civs")
		self.requirement = ConqueredCities(2, civs=self.civs)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Test Civs cities")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_conquer_of_civ(self):
		city1, city2 = TestCities.owners(1, 1)
		
		try:
			player(0).acquireCity(city1, True, False)
			player(0).acquireCity(city2, True, False)
			
			self.assertEqual(cities.owner(0).count(), 2)
			self.assertEqual(len(self.requirement.recorded), 2)
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Conquered Test Civs cities: 2 / 2")
		finally:
			city(61, 31).kill()
			city(63, 31).kill()
	
	def test_conquer_not_of_civ(self):
		city1, city2 = cities = TestCities.owners(2, 2)
		
		try:
			player(0).acquireCity(city1, True, False)
			player(0).acquireCity(city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Conquered Test Civs cities: 0 / 2")
		finally:
			city(61, 31).kill()
			city(63, 31).kill()


class TestEnslaveCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = EnslaveCount(2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "EnslaveCount(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "EnslaveCount(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two units")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_enslave(self):
		unit = makeUnit(1, iSwordsman, (10, 10))
		
		try:
			events.fireEvent("enslave", 0, unit)
			events.fireEvent("enslave", 0, unit)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Enslaved units: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			unit.kill(False, -1)
	
	def test_enslave_minor(self):
		unit = makeUnit(iNative, iSwordsman, (10, 10))
		
		try:
			events.fireEvent("enslave", 0, unit)
			events.fireEvent("enslave", 0, unit)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Enslaved units: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			unit.kill(False, -1)
	
	def test_enslave_other(self):
		unit = makeUnit(1, iSwordsman, (10, 10))
		
		try:
			events.fireEvent("enslave", 2, unit)
			events.fireEvent("enslave", 2, unit)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Enslaved units: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			unit.kill(False, -1)
	
	def test_enslave_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		unit = makeUnit(2, iSwordsman, (10, 10))
		
		try:
			events.fireEvent("enslave", 1, unit)
			events.fireEvent("enslave", 1, unit)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Enslaved units: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			unit.kill(False, -1)
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)
		
		
class TestEnslaveCountExcluding(ExtendedTestCase):

	def setUp(self):
		self.requirement = EnslaveCount(2, excluding=CivsDefinition(1).named("Test Civs"))
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Test Civs units")
	
	def test_enslave_excluded(self):
		unit = makeUnit(1, iSwordsman, (10, 10))
		
		try:
			events.fireEvent("enslave", 0, unit)
			events.fireEvent("enslave", 0, unit)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Enslaved Test Civs units: 0 / 2")
		finally:
			unit.kill(False, -1)
	
	def test_enslave_not_excluded(self):
		unit = makeUnit(2, iSwordsman, (10, 10))
		
		try:
			events.fireEvent("enslave", 0, unit)
			events.fireEvent("enslave", 0, unit)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Enslaved Test Civs units: 2 / 2")
		finally:
			unit.kill(False, -1)


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


class TestGreatGenerals(ExtendedTestCase):

	def setUp(self):
		self.requirement = GreatGenerals(2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "GreatGenerals(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "GreatGenerals(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two great generals")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_great_general(self):
		city = TestCities.one()
		unit = makeUnit(0, iGreatGeneral, (10, 10))
		
		try:
			events.fireEvent("greatPersonBorn", unit, 0, city)
			events.fireEvent("greatPersonBorn", unit, 0, city)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Great generals: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
			unit.kill(False, -1)
	
	def test_different_unit(self):
		city = TestCities.one()
		unit = makeUnit(0, iGreatScientist, (10, 10))
		
		try:
			events.fireEvent("greatPersonBorn", unit, 0, city)
			events.fireEvent("greatPersonBorn", unit, 0, city)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Great generals: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
			unit.kill(False, -1)
	
	def test_different_owner(self):
		city = TestCities.one(1)
		unit = makeUnit(1, iGreatGeneral, (10, 10))
		
		try:
			events.fireEvent("greatPersonBorn", unit, 1, city)
			events.fireEvent("greatPersonBorn", unit, 1, city)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Great generals: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
			unit.kill(False, -1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		city = TestCities.one(1)
		unit = makeUnit(1, iGreatGeneral, (10, 10))
		
		try:
			events.fireEvent("greatPersonBorn", unit, 1, city)
			events.fireEvent("greatPersonBorn", unit, 1, city)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Great generals: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
			unit.kill(False, -1)
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestPillageCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = PillageCount(2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
		
		self.unit = makeUnit(self.iPlayer, iSwordsman, (25, 25))
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "PillageCount(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "PillageCount(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two improvements")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pillage(self):
		events.fireEvent("unitPillage", self.unit, iHamlet, -1, self.iPlayer, 100)
		events.fireEvent("unitPillage", self.unit, iHamlet, -1, self.iPlayer, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Improvements pillaged: 2 / 2")
		self.assertEqual(self.goal.checked, True)
	
	def test_pillage_other(self):
		events.fireEvent("unitPillage", self.unit, iHamlet, -1, 1, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Improvements pillaged: 0 / 2")
		self.assertEqual(self.goal.checked, False)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		try:
			events.fireEvent("unitPillage", self.unit, iHamlet, -1, 1, 100)
			events.fireEvent("unitPillage", self.unit, iHamlet, -1, 1, 100)
			
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Improvements pillaged: 2 / 2")
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestPiracyGold(ExtendedTestCase):

	def setUp(self):
		self.requirement = PiracyGold(100)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
		
		self.city = TestCities.one(1)
		self.unit = makeUnit(0, iSwordsman, (25, 25))
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
		self.city.kill()
		self.unit.kill(False, -1)
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "PiracyGold(100)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "PiracyGold(100)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "100 gold through piracy")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_unit_pillage(self):
		events.fireEvent("unitPillage", self.unit, iHamlet, -1, self.iPlayer, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from piracy: 100 / 100")
		self.assertEqual(self.goal.checked, True)
	
	def test_unit_pillage_other(self):
		events.fireEvent("unitPillage", self.unit, iHamlet, -1, 1, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from piracy: 0 / 100")
		self.assertEqual(self.goal.checked, False)
	
	def test_blockade(self):
		events.fireEvent("blockade", 0, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from piracy: 100 / 100")
		self.assertEqual(self.goal.checked, True)
	
	def test_blockade_other(self):
		events.fireEvent("blockade", 1, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from piracy: 0 / 100")
		self.assertEqual(self.goal.checked, False)
	
	def test_combat_gold(self):
		events.fireEvent("combatGold", self.iPlayer, self.unit, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from piracy: 100 / 100")
		self.assertEqual(self.goal.checked, True)
	
	def test_combat_gold_other(self):
		events.fireEvent("combatGold", 1, self.unit, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from piracy: 0 / 100")
		self.assertEqual(self.goal.checked, False)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		try:
			events.fireEvent("combatGold", 1, self.unit, 100)
		
			self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from piracy: 100 / 100")
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestRaidGold(ExtendedTestCase):

	def setUp(self):
		self.requirement = RaidGold(100)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
		
		self.city = TestCities.one(1)
		self.unit = makeUnit(0, iSwordsman, (25, 25))
	
	def tearDown(self):
		self.requirement.deregister_handlers()
		
		self.city.kill()
		self.unit.kill(False, -1)
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "RaidGold(100)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "RaidGold(100)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "100 gold by pillaging, conquering cities and sinking ships")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_unit_pillage(self):
		events.fireEvent("unitPillage", self.unit, iHamlet, -1, self.iPlayer, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from raids: 100 / 100")
		self.assertEqual(self.goal.checked, True)
	
	def test_unit_pillage_other(self):
		events.fireEvent("unitPillage", self.unit, iHamlet, -1, 1, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from raids: 0 / 100")
		self.assertEqual(self.goal.checked, False)
	
	def test_city_capture_gold(self):
		events.fireEvent("cityCaptureGold", self.city, self.iPlayer, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from raids: 100 / 100")
		self.assertEqual(self.goal.checked, True)
	
	def test_city_capture_gold_other(self):
		events.fireEvent("cityCaptureGold", self.city, 1, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from raids: 0 / 100")
		self.assertEqual(self.goal.checked, False)
	
	def test_combat_gold(self):
		events.fireEvent("combatGold", self.iPlayer, self.unit, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from raids: 100 / 100")
		self.assertEqual(self.goal.checked, True)
	
	def test_combat_gold_other(self):
		events.fireEvent("combatGold", 1, self.unit, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from raids: 0 / 100")
		self.assertEqual(self.goal.checked, False)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		try:
			events.fireEvent("combatGold", 1, self.unit, 100)
		
			self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from raids: 100 / 100")
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestRazeCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = RazeCount(2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "RazeCount(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "RazeCount(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two cities")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_raze(self):
		city = TestCities.one(1)
		
		try:
			events.fireEvent("cityRazed", city, 0)
			events.fireEvent("cityRazed", city, 0)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Razed cities: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_raze_other(self):
		city = TestCities.one(2)
		
		try:
			events.fireEvent("cityRazed", city, 1)
			events.fireEvent("cityRazed", city, 1)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Razed cities: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_raze_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		city = TestCities.one(2)
		
		try:
			events.fireEvent("cityRazed", city, 1)
			events.fireEvent("cityRazed", city, 1)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Razed cities: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestResourceTradeGold(ExtendedTestCase):

	def setUp(self):
		self.requirement = ResourceTradeGold(100)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ResourceTradeGold(100)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ResourceTradeGold(100)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "100 gold by selling resources")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_resource_trade_gold(self):
		player(0).changeGoldPerTurnByPlayer(1, 100)
		
		try:
			events.fireEvent("BeginPlayerTurn", 0, 0)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from trading resources: 100 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			player(0).changeGoldPerTurnByPlayer(1, -100)
	
	def test_resource_trade_gold_other_player(self):
		player(1).changeGoldPerTurnByPlayer(2, 100)
		
		try:
			events.fireEvent("BeginPlayerTurn", 0, 1)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from trading resources: 0 / 100")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			player(1).changeGoldPerTurnByPlayer(2, -100)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		player(1).changeGoldPerTurnByPlayer(2, 100)
		
		try:
			events.fireEvent("BeginPlayerTurn", 0, 1)
		
			self.assertEqual(self.requirement.evaluate(evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Gold from trading resources: 100 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			player(1).changeGoldPerTurnByPlayer(2, -100)
			team(1).setVassal(0, False, False)


class TestSettledCities(ExtendedTestCase):

	def setUp(self):
		self.requirement = SettledCities(2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "SettledCities(2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "SettledCities(2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two cities")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_record_settled(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityBuilt", city1)
			events.fireEvent("cityBuilt", city2)
		
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Settled cities: 2 / 2")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			cities.kill()
	
	def test_different_owner(self):
		city1, city2 = cities = TestCities.owners(1, 1)
		
		try:
			events.fireEvent("cityBuilt", city1)
			events.fireEvent("cityBuilt", city2)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Settled cities: 0 / 2")
			
			self.assertEqual(self.goal.checked, False)
		finally:
			cities.kill()
	
	def test_settled_then_lost(self):
		city1, city2 = TestCities.num(2)
		
		try:
			events.fireEvent("cityBuilt", city1)
			events.fireEvent("cityBuilt", city2)
			
			player(1).acquireCity(city1, True, False)
			player(1).acquireCity(city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Settled cities: 0 / 2")
		finally:
			city(61, 31).kill()
			city(63, 31).kill()
	
	def test_conquered(self):
		city1, city2 = TestCities.owners(1, 1)
		
		try:
			events.fireEvent("cityBuilt", city1)
			events.fireEvent("cityBuilt", city2)
			
			player(0).acquireCity(city1, True, False)
			player(0).acquireCity(city2, True, False)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Settled cities: 0 / 2")
		finally:
			city(61, 31).kill()
			city(63, 31).kill()
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


class TestSettledCitiesArea(ExtendedTestCase):

	def setUp(self):
		self.requirement = SettledCities(2, area=plots.of([(61, 31), (63, 31)]).named("Test Area"))
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two cities in Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots_.of([(61, 31), (63, 31)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((61, 31)), "Test Area")
		self.assertEqual(self.requirement.area_name((10, 10)), "")
	
	def test_settle_in_area(self):
		city1, city2 = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityBuilt", city1)
			events.fireEvent("cityBuilt", city2)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Settled cities in Test Area: 2 / 2")
		finally:
			cities.kill()
	
	def test_settle_not_in_area(self):
		city1, city2, city3, city4 = cities = TestCities.num(4)
		
		try:
			events.fireEvent("cityBuilt", city3)
			events.fireEvent("cityBuilt", city4)
			
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Settled cities in Test Area: 0 / 2")
		finally:
			cities.kill()


class TestSlaveTradeGold(ExtendedTestCase):

	def setUp(self):
		self.requirement = SlaveTradeGold(100)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "SlaveTradeGold(100)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "SlaveTradeGold(100)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "100 gold through the slave trade")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_less(self):
		events.fireEvent("playerSlaveTrade", 0, 50)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 50)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from slave trade: 50 / 100")
		
		self.assertEqual(self.goal.checked, True)
	
	def test_more(self):
		events.fireEvent("playerSlaveTrade", 0, 200)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 200)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
		self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Gold from slave trade: 200 / 100")
		
		self.assertEqual(self.goal.checked, True)
	
	def test_other_player(self):
		events.fireEvent("playerSlaveTrade", 1, 100)
		
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Gold from slave trade: 0 / 100")
		
		self.assertEqual(self.goal.checked, False)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		self.goal.evaluator = evaluator
		
		team(1).setVassal(0, True, False)
		
		try:
			events.fireEvent("playerSlaveTrade", 1, 100)
		
			self.assertEqual(self.requirement.evaluate(evaluator), 100)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Gold from slave trade: 100 / 100")
			
			self.assertEqual(self.goal.checked, True)
		finally:
			team(1).setVassal(0, False, False)
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, False)


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
	TestAcquiredCities,
	TestBrokeredPeace,
	TestConqueredCities,
	TestConqueredCitiesInside,
	TestConqueredCitiesOutside,
	TestConqueredCitiesCivs,
	TestEnslaveCount,
	TestEnslaveCountExcluding,
	TestEraFirstDiscover,
	TestGoldenAges,
	TestGreatGenerals,
	TestPillageCount,
	TestPiracyGold,
	TestRaidGold,
	TestRazeCount,
	TestResourceTradeGold,
	TestSettledCities,
	TestSettledCitiesArea,
	TestSlaveTradeGold,
	TestSunkShips,
	TestTradeGold,
]