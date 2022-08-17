from PercentRequirements import *

from TestVictoryCommon import *


class TestAreaPercent(ExtendedTestCase):

	def setUp(self):
		self.area = AreaArgumentFactory().rectangle((50, 30), (69, 31)).named("Test Area")
		self.assertEqual(self.area.land().count(), 40)
		
		self.requirement = AreaPercent(self.area, 30)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "AreaPercent(Test Area, 30%)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "AreaPercent(Test Area, 30%)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "30% of Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots.rectangle((50, 30), (69, 31))})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((50, 30)), "Test Area")
		self.assertEqual(self.requirement.area_name((42, 42)), "")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.percentage(self.evaluator), 0.0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Territory in Test Area: 0.00% / 30%")
	
	def test_half(self):
		controlled = plots.rectangle((50, 30), (69, 30))
		for plot in controlled:
			plot.setOwner(0)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 20)
			self.assertEqual(self.requirement.total(), 40)
			self.assertEqual(self.requirement.percentage(self.evaluator), 50.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Territory in Test Area: 50.00% / 30%")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
	
	def test_all(self):
		controlled = plots.rectangle((50, 30), (69, 31))
		for plot in controlled:
			plot.setOwner(0)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 40)
			self.assertEqual(self.requirement.percentage(self.evaluator), 100.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Territory in Test Area: 100.00% / 30%")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
	
	def test_outside(self):
		controlled = plots.rectangle((50, 29), (69, 29))
		for plot in controlled:
			plot.setOwner(0)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.percentage(self.evaluator), 0.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Territory in Test Area: 0.00% / 30%")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		controlled = plots.rectangle((50, 30), (69, 31))
		for plot in controlled:
			plot.setOwner(1)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 40)
			self.assertEqual(self.requirement.percentage(evaluator), 100.0)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Territory in Test Area: 100.00% / 30%")
		finally:
			team(1).setVassal(0, False, False)
			for plot in controlled:
				plot.setOwner(-1)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestAreaPopulationPercent(ExtendedTestCase):

	def setUp(self):
		self.area = AreaArgumentFactory().of([(61, 31), (63, 31)]).named("Test Area")
		self.requirement = AreaPopulationPercent(self.area, 40)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "AreaPopulationPercent(Test Area, 40%)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "AreaPopulationPercent(Test Area, 40%)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "40% of the population in Test Area")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test Area": plots.of([(61, 31), (63, 31)])})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.percentage(self.evaluator), 0.0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Population in Test Area: 0.00% / 40%")
	
	def test_less(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setPopulation(5)
		their_city.setPopulation(15)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 5)
			self.assertEqual(self.requirement.percentage(self.evaluator), 25.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Population in Test Area: 25.00% / 40%")
		finally:
			cities.kill()
	
	def test_more(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setPopulation(10)
		their_city.setPopulation(10)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 10)
			self.assertEqual(self.requirement.percentage(self.evaluator), 50.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Population in Test Area: 50.00% / 40%")
		finally:
			cities.kill()
	
	def test_outside(self):
		our_inside_city, their_city, our_outside_city = cities = TestCities.owners(0, 1, 0)
		
		our_inside_city.setPopulation(5)
		their_city.setPopulation(15)
		our_outside_city.setPopulation(20)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 5)
			self.assertEqual(self.requirement.percentage(self.evaluator), 25.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Population in Test Area: 25.00% / 40%")
		finally:
			cities.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		vassal_city, other_city = cities = TestCities.owners(1, 2)
		
		vassal_city.setPopulation(10)
		other_city.setPopulation(10)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 10)
			self.assertEqual(self.requirement.percentage(evaluator), 50.0)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Population in Test Area: 50.00% / 40%")
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)

	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestCommercePercent(ExtendedTestCase):

	def setUp(self):
		self.requirement = CommercePercent(15)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CommercePercent(15%)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CommercePercent(15%)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "15% of the world's commerce")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_fulfilled(self):
		player(0).changeGoldPerTurnByPlayer(0, 1)
	
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.percentage(self.evaluator), 20.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Global commerce: 20.00% / 15%")
		finally:
			player(0).changeGoldPerTurnByPlayer(0, -1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		player(0).changeGoldPerTurnByPlayer(0, 1)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 3)
			self.assertEqual(self.requirement.percentage(evaluator), 30.0)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Global commerce: 30.00% / 15%")
		finally:
			team(1).setVassal(0, False, False)
			player(0).changeGoldPerTurnByPlayer(0, -1)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestLandPercent(ExtendedTestCase):

	def setUp(self):
		self.requirement = LandPercent(10)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "LandPercent(10%)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "LandPercent(10%)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "10% of the world")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_sufficient(self):
		territory = plots.all().land().limit(11 * 32)
		for plot in territory:
			plot.setOwner(self.iPlayer)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 11 * 32)
			self.assertAlmostEqual(self.requirement.percentage(self.evaluator), 10.89, places=2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "World territory controlled: 10.89% / 10%")
		finally:
			for plot in territory:
				plot.setOwner(-1)
	
	def test_insufficient(self):
		territory = plots.all().land().limit(32)
		for plot in territory:
			plot.setOwner(self.iPlayer)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 32)
			self.assertAlmostEqual(self.requirement.percentage(self.evaluator), 0.99, places=2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "World territory controlled: 0.99% / 10%")
		finally:
			for plot in territory:
				plot.setOwner(-1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
	
		our_territory, vassal_territory = plots.all().land().limit(11 * 32).percentage_split(60)
		for plot in our_territory:
			plot.setOwner(self.iPlayer)
		
		for plot in vassal_territory:
			plot.setOwner(1)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 11 * 32)
			self.assertAlmostEqual(self.requirement.percentage(evaluator), 10.89, places=2)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "World territory controlled: 10.89% / 10%")
		finally:
			for plot in our_territory + vassal_territory:
				plot.setOwner(-1)
			
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)

	
class TestPopulationPercent(ExtendedTestCase):

	def setUp(self):
		self.requirement = PopulationPercent(30)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
		
	def test_str(self):
		self.assertEqual(str(self.requirement), "PopulationPercent(30%)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "PopulationPercent(30%)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "30% of the world's population")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_sufficient(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setPopulation(10)
		their_city.setPopulation(10)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 10)
			self.assertEqual(self.requirement.percentage(self.evaluator), 50.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Percentage of world population: 50.00% / 30%")
		finally:
			cities.kill()
	
	def test_insufficient(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setPopulation(5)
		their_city.setPopulation(15)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 5)
			self.assertEqual(self.requirement.percentage(self.evaluator), 25.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Percentage of world population: 25.00% / 30%")
		finally:
			cities.kill()
			
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
	
		our_city, vassal_city, other_city = cities = TestCities.owners(0, 1, 2)
		
		our_city.setPopulation(10)
		vassal_city.setPopulation(5)
		other_city.setPopulation(5)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 15)
			self.assertEqual(self.requirement.percentage(evaluator), 75.0)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Percentage of world population: 75.00% / 30%")
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, True)


class TestPowerPercent(ExtendedTestCase):

	def setUp(self):
		self.requirement = PowerPercent(25)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "PowerPercent(25%)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "PowerPercent(25%)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "25% of the world's military power")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_fulfilled(self):
		units = makeUnits(0, iMilitia, (10, 10), 2)
	
		try:
			self.assertEqual(self.requirement.total(), 10)
			self.assertEqual(self.requirement.evaluate(self.evaluator), 6)
			self.assertEqual(self.requirement.percentage(self.evaluator), 60.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Global military power: 60.00% / 25%")
		finally:
			for unit in units:
				unit.kill(False, -1)
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		our_unit = makeUnit(0, iMilitia, (10, 10))
		vassal_unit = makeUnit(0, iMilitia, (10, 10))
		
		try:
			self.assertEqual(self.requirement.total(), 10)
			self.assertEqual(self.requirement.evaluate(evaluator), 8)
			self.assertEqual(self.requirement.percentage(evaluator), 80.0)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Global military power: 80.00% / 25%")
		finally:
			our_unit.kill(False, -1)
			vassal_unit.kill(False, -1)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestReligionSpreadPercent(ExtendedTestCase):

	def setUp(self):
		self.requirement = ReligionSpreadPercent(iOrthodoxy, 30)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ReligionSpreadPercent(Orthodoxy, 30%)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ReligionSpreadPercent(Orthodoxy, 30%)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "Orthodoxy to 30% of the world's population")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_spread(self):
		city1, city2 = cities = TestCities.num(2)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasReligion(iOrthodoxy, True, False, False)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(self.requirement.percentage(self.evaluator), 50.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Orthodoxy spread: 50.00% / 30%")
		finally:
			cities.kill()
			player(0).setLastStateReligion(-1)
	
	def test_no_state_religion(self):
		city1, city2 = cities = TestCities.num(2)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasReligion(iOrthodoxy, True, False, False)
		
		try:
			self.assertEqual(self.requirement.percentage(self.evaluator), 25.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Orthodoxy spread: 25.00% / 30%")
		finally:
			cities.kill()
	
	def test_additional_religion_present(self):
		city1, city2 = cities = TestCities.num(2)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasReligion(iOrthodoxy, True, False, False)
		city2.setHasReligion(iCatholicism, True, False, False)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(self.requirement.percentage(self.evaluator), 50.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Orthodoxy spread: 50.00% / 30%")
		finally:
			cities.kill()
			player(0).setLastStateReligion(-1)
	
	def test_different_owner(self):
		city1, city2 = cities = TestCities.owners(1, 0)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasReligion(iOrthodoxy, True, False, False)
		
		player(1).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(self.requirement.percentage(self.evaluator), 50.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Orthodoxy spread: 50.00% / 30%")
		finally:
			cities.kill()
			player(1).setLastStateReligion(-1)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestReligiousVotePercent(ExtendedTestCase):

	def setUp(self):
		self.requirement = ReligiousVotePercent(30)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "ReligiousVotePercent(30%)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "ReligiousVotePercent(30%)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "30% of the votes in the Apostolic Palace")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {})
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_less(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setPopulation(5)
		their_city.setPopulation(36)
		
		our_city.setHasReligion(iCatholicism, True, False, False)
		their_city.setHasReligion(iCatholicism, True, False, False)
		
		our_city.setHasRealBuilding(iCatholicShrine, True)
		
		player(0).setLastStateReligion(iCatholicism)
		player(1).setLastStateReligion(iCatholicism)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 4)
			self.assertEqual(self.requirement.percentage(self.evaluator), 25.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Votes in the Apostolic Palace: 25.00% / 30%")
		finally:
			player(0).setLastStateReligion(-1)
			player(1).setLastStateReligion(-1)
			
			cities.kill()
	
	def test_more(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setPopulation(10)
		their_city.setPopulation(10)
		
		our_city.setHasReligion(iCatholicism, True, False, False)
		their_city.setHasReligion(iCatholicism, True, False, False)
		
		our_city.setHasRealBuilding(iCatholicShrine, True)
		
		player(0).setLastStateReligion(iCatholicism)
		player(1).setLastStateReligion(iCatholicism)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 6)
			self.assertEqual(self.requirement.percentage(self.evaluator), 50.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Votes in the Apostolic Palace: 50.00% / 30%")
		finally:
			player(0).setLastStateReligion(-1)
			player(1).setLastStateReligion(-1)
			cities.kill()
	
	def test_not_state_religion(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setPopulation(10)
		their_city.setPopulation(10)
		
		our_city.setHasReligion(iCatholicism, True, False, False)
		their_city.setHasReligion(iCatholicism, True, False, False)
		
		our_city.setHasRealBuilding(iCatholicShrine, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.percentage(self.evaluator), 0.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Votes in the Apostolic Palace: 0.00% / 30%")
		finally:
			cities.kill()
	
	def test_not_city_religion(self):
		our_city, their_city = cities = TestCities.owners(0, 1)
		
		our_city.setPopulation(10)
		their_city.setPopulation(10)
		
		our_city.setHasRealBuilding(iCatholicShrine, True)
		
		player(0).setLastStateReligion(iCatholicism)
		player(1).setLastStateReligion(iCatholicism)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
			self.assertEqual(self.requirement.percentage(self.evaluator), 0.0)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Votes in the Apostolic Palace: 0.00% / 30%")
		finally:
			player(0).setLastStateReligion(-1)
			player(1).setLastStateReligion(-1)
			cities.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		vassal_city, other_city = cities = TestCities.owners(1, 2)
		
		vassal_city.setPopulation(10)
		other_city.setPopulation(10)
		
		vassal_city.setHasReligion(iCatholicism, True, False, False)
		other_city.setHasReligion(iCatholicism, True, False, False)
		
		vassal_city.setHasRealBuilding(iCatholicShrine, True)
		
		player(1).setLastStateReligion(iCatholicism)
		player(2).setLastStateReligion(iCatholicism)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 6)
			self.assertEqual(self.requirement.percentage(evaluator), 50.0)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Votes in the Apostolic Palace: 50.00% / 30%")
		finally:
			player(0).setLastStateReligion(-1)
			player(1).setLastStateReligion(-1)
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


test_cases = [
	TestAreaPercent,
	TestAreaPopulationPercent,
	TestCommercePercent,
	TestLandPercent,
	TestPopulationPercent,
	TestPowerPercent,
	TestReligionSpreadPercent,
	TestReligiousVotePercent,
]