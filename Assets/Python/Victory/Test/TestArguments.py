from VictoryArguments import *

from TestVictoryCommon import *
		
		
class TestNamedArgument(ExtendedTestCase):

	def setUp(self):
		self.argument = NamedArgument()
	
	def test_unnamed(self):
		self.assertEqual(self.argument.name(), "")
	
	def test_named(self):
		argument = self.argument.named("Argument")
		
		self.assertType(argument, NamedArgument)
		
		self.assertEqual(self.argument.name(), "Argument")
		self.assertEqual(argument.name(), "Argument")
	
	def test_renamed(self):
		self.argument.named("First")
		self.assertEqual(self.argument.name(), "First")
		
		self.argument.named("Second")
		self.assertEqual(self.argument.name(), "Second")


class TestAggregate(ExtendedTestCase):

	def setUp(self):
		self.aggregate = SumAggregate([1, 2, 3])
	
	def test_str(self):
		self.assertEqual(str(self.aggregate), "SumAggregate(1, 2, 3)")
	
	def test_contains(self):
		self.assertEqual(1 in self.aggregate, True)
		self.assertEqual(0 in self.aggregate, False)
	
	def test_equal(self):
		self.assertEqual(self.aggregate, SumAggregate([1, 2, 3]))
		self.assertNotEqual(self.aggregate, SumAggregate([1, 2]))
		
		self.assertEqual(self.aggregate, 1)
		self.assertNotEqual(self.aggregate, 0)
	
	def test_pickle(self):
		self.assertPickleable(self.aggregate)
	
	def test_validate(self):
		self.assertEqual(self.aggregate.validate(BUILDING.validate), True)
		self.assertEqual(self.aggregate.validate(AREA.validate), False)
	
	def test_validate_mixed(self):
		aggregate = SumAggregate([1, plots.of([(0, 0)])])
		
		self.assertEqual(aggregate.validate(BUILDING.validate), False)
		self.assertEqual(aggregate.validate(AREA.validate), False)
	
	def test_format(self):
		self.assertEqual(self.aggregate.format(COUNT.format), "a, two and three")
		self.assertEqual(self.aggregate.format(BUILDING.format), "Barracks, Ikhanda and Granary")
		self.assertEqual(self.aggregate.format(BUILDING.format, bPlural=True), "Barracks, Ikhandas and Granaries")
	
	def test_format_named(self):
		self.aggregate.named("named aggregate")
		
		self.assertEqual(self.aggregate.format(BUILDING.format), "named aggregate")
	
	def test_evaluate(self):
		self.assertEqual(self.aggregate.evaluate(lambda x: x), 6)
		self.assertEqual(self.aggregate.evaluate(lambda x: x*x), 14)
	
	def test_average_evaluate(self):
		average_aggregate = AverageAggregate([1, 2, 3])
		
		self.assertEqual(average_aggregate.evaluate(lambda x: x), 2)
		self.assertEqual(average_aggregate.evaluate(lambda x: x+1), 3)
	
	def test_count_evaluate(self):
		count_aggregate = CountAggregate([1, 2, 3])
		
		self.assertEqual(count_aggregate.evaluate(lambda x: x), 3)
		self.assertEqual(count_aggregate.evaluate(lambda x: x % 2), 2)
	
	def test_varargs(self):
		aggregate = SumAggregate(1, 2, 3)
		
		self.assertEqual(aggregate.items, [1, 2, 3])
	
	def test_generator(self):
		aggregate = SumAggregate(x for x in xrange(3))
		
		self.assertEqual(aggregate.items, [0, 1, 2])


class TestAreaArgument(ExtendedTestCase):

	def setUp(self):
		self.area = AreaArgumentFactory()

	def test(self):
		even = lambda p: (p.getX() + p.getY()) % 2 == 0
		
		area = self.area.rectangle((0, 0), (1, 1)).where(even)
		
		self.assertType(area, AreaArgument)
		self.assertEqual(area.calls, [("rectangle", ((0, 0), (1, 1)), {}), ("where", (even,), {})])
		
		area = area.create()
		
		self.assertType(area, Plots)
		self.assertEqual(len(area), 2)
		self.assertEqual((0, 0) in area, True)
		self.assertEqual((1, 1) in area, True)
	
	def test_equal(self):
		area = self.area.of([(0, 0), (0, 1)])
		
		identical = self.area.of([(0, 1), (0, 0)])
		different_type = PlotFactory().of([(0, 0), (0, 1)])
		different_plots = self.area.of([(0, 0), (1, 1)])
		
		self.assertEqual(area, identical)
		self.assertNotEqual(area, different_type)
		self.assertNotEqual(area, different_plots)
	
	def test_str(self):
		self.assertEqual(str(self.area.rectangle((0, 0), (1, 1)).region(2)), "AreaArgument.rectangle((0, 0), (1, 1)).region(2)")
	
	def test_pickle(self):
		self.assertPickleable(self.area.rectangle((0, 0), (1, 1)).region(2))
	
	def test_without_create(self):
		area = self.area.rectangle((0, 0), (1, 1))
		
		self.assertType(area, AreaArgument)
		
		self.assertEqual(len(area), 4)
		self.assertEqual((0, 0) in area, True)
	
	def test_named(self):
		area = self.area.all().named("Area")
		
		self.assertType(area, AreaArgument)
		self.assertEqual(area.name(), "Area")
		
		area = area.create()
		
		self.assertType(area, Plots)
		self.assertEqual(area.name(), "Area")
	
	def test_multiple_creates(self):
		area = self.area.rectangle((0, 0), (1, 1))
		
		area1 = area.create()
		area2 = area.create()
		
		self.assertNotEqual(id(area1), id(area2))
	
	def test_add(self):
		area = self.area.of([(0, 0)]) + self.area.of([(0, 1)])
		
		self.assertType(area, CombinedAreaArgument)
		self.assertInstance(area, AreaArgument)
		
		created_area = area.create()
		
		self.assertEqual(created_area, plots.of([(0, 0), (0, 1)]))
	

class TestLocationCityArgument(ExtendedTestCase):

	def setUp(self):
		self.location = TestCities.CITY_LOCATIONS[0]
		self.argument = LocationCityArgument(self.location)
		
	def test_str(self):
		self.assertEqual(str(self.argument), "LocationCityArgument(61, 31)")
	
	def test_repr(self):
		self.assertEqual(repr(self.argument), "LocationCityArgument(61, 31)")
	
	def test_hash(self):
		same_location = LocationCityArgument(self.location)
		different_location = LocationCityArgument((63, 31))
		
		self.assertEqual(hash(self.argument), hash(same_location))
		self.assertNotEqual(hash(self.argument), hash(different_location))
	
	def test_pickle(self):
		self.assertPickleable(self.argument)
	
	def test_equal_definition(self):
		identical = LocationCityArgument(self.location)
		different = LocationCityArgument((62, 31))
		
		self.assertEqual(self.argument, identical)
		self.assertNotEqual(self.argument, different)
	
	def test_equal_city(self):
		same_location, different_location = cities = TestCities.num(2)
		
		try:
			self.assertEqual(self.argument, same_location)
			self.assertNotEqual(self.argument, different_location)
		finally:
			cities.kill()
	
	def test_from_varargs(self):
		argument = LocationCityArgument(*self.location)
		self.assertEqual(str(argument), "LocationCityArgument(61, 31)")
	
	def test_get(self):
		city = TestCities.one()
		
		try:
			self.assertEqual(location(self.argument.get(0)), location(city))
		finally:
			city.kill()
	
	def test_get_no_city(self):
		self.assertEqual(self.argument.get(0), NON_EXISTING)


class TestCapitalCityArgument(ExtendedTestCase):

	def setUp(self):
		self.argument = CapitalCityArgument()
	
	def test_str(self):
		self.assertEqual(str(self.argument), "CapitalCityArgument()")
	
	def test_repr(self):
		self.assertEqual(repr(self.argument), "CapitalCityArgument()")
	
	def test_hash(self):
		self.assertEqual(hash(self.argument), 0)
	
	def test_pickle(self):
		self.assertPickleable(self.argument)
	
	def test_equal_definition(self):
		self.assertEqual(self.argument, CapitalCityArgument())
		self.assertNotEqual(self.argument, LocationCityArgument(61, 31))
	
	def test_equal_city(self):
		capital, not_capital = cities = TestCities.num(2)
		capital.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqual(self.argument, capital)
			self.assertNotEqual(self.argument, not_capital)
		finally:
			cities.kill()
	
	def test_get(self):
		capital, not_capital = cities = TestCities.num(2)
		capital.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqual(location(self.argument.get(0)), location(capital))
		finally:
			cities.kill()
	
	def test_get_no_city(self):
		self.assertEqual(self.argument.get(0), NON_EXISTING)


class TestReligionHolyCityArgument(ExtendedTestCase):

	def setUp(self):
		self.argument = ReligionHolyCityArgument(iBuddhism)
	
	def test_str(self):
		self.assertEqual(str(self.argument), "ReligionHolyCityArgument(Buddhism)")
	
	def test_repr(self):
		self.assertEqual(repr(self.argument), "ReligionHolyCityArgument(Buddhism)")
	
	def test_pickle(self):
		self.assertPickleable(self.argument)
	
	def test_equal_definition(self):
		self.assertEqual(self.argument, ReligionHolyCityArgument(iBuddhism))
		self.assertNotEqual(self.argument, ReligionHolyCityArgument(iHinduism))
		self.assertNotEqual(self.argument, CapitalCityArgument())
	
	def test_equal_city(self):
		holy_city, other_city = cities = TestCities.owners(1, 2)
		
		game.setHolyCity(iBuddhism, holy_city, False)
		
		try:
			self.assertEqual(self.argument, holy_city)
			self.assertNotEqual(self.argument, other_city)
		finally:
			game.clearHolyCity(iBuddhism)
			cities.kill()
	
	def test_get(self):
		holy_city, other_city = cities = TestCities.owners(1, 2)
		
		game.setHolyCity(iBuddhism, holy_city, False)
		
		try:
			self.assertEqualCity(self.argument.get(0), holy_city)
		finally:
			game.clearHolyCity(iBuddhism)
			cities.kill()
	
	def test_get_no_city(self):
		self.assertEqual(self.argument.get(0), NON_EXISTING)


class TestStateReligionHolyCityArgument(ExtendedTestCase):

	def setUp(self):
		self.argument = StateReligionHolyCityArgument()
	
	def test_str(self):
		self.assertEqual(str(self.argument), "StateReligionHolyCityArgument()")
	
	def test_repr(self):
		self.assertEqual(repr(self.argument), "StateReligionHolyCityArgument()")
	
	def test_pickle(self):
		self.assertPickleable(self.argument)
	
	def test_equal_definition(self):
		self.assertEqual(self.argument, StateReligionHolyCityArgument())
		self.assertNotEqual(self.argument, CapitalCityArgument())
	
	def test_equal_city(self):
		holy_city, other_city = cities = TestCities.owners(1, 2)
		
		game.setHolyCity(iBuddhism, holy_city, False)
		player(1).setLastStateReligion(iBuddhism)
		
		try:
			self.assertEqual(self.argument, holy_city)
			self.assertNotEqual(self.argument, other_city)
		finally:
			game.clearHolyCity(iBuddhism)
			player(0).setLastStateReligion(-1)
			cities.kill()
	
	def test_get(self):
		holy_city, other_city = cities = TestCities.owners(1, 2)
		
		game.setHolyCity(iBuddhism, holy_city, False)
		player(0).setLastStateReligion(iBuddhism)
		
		try:
			self.assertEqualCity(self.argument.get(0), holy_city)
		finally:
			game.clearHolyCity(iBuddhism)
			player(0).setLastStateReligion(-1)
			cities.kill()
	
	def test_get_no_city(self):
		player(0).setLastStateReligion(iBuddhism)
		
		try:
			self.assertEqual(self.argument.get(0), NON_EXISTING)
		finally:
			player(0).setLastStateReligion(-1)
	
	def test_get_no_state_religion(self):
		holy_city, other_city = cities = TestCities.owners(1, 2)
		
		game.setHolyCity(iBuddhism, holy_city, False)
		
		try:
			self.assertEqual(self.argument.get(0), NON_EXISTING)
		finally:
			game.clearHolyCity(iBuddhism)
			cities.kill()


class TestWonderCityArgument(ExtendedTestCase):

	def setUp(self):
		self.argument = WonderCityArgument(iHangingGardens)
	
	def test_str(self):
		self.assertEqual(str(self.argument), "WonderCityArgument(The Hanging Gardens)")
	
	def test_repr(self):
		self.assertEqual(repr(self.argument), "WonderCityArgument(The Hanging Gardens)")
	
	def test_pickle(self):
		self.assertPickleable(self.argument)
	
	def test_equal_definition(self):
		self.assertEqual(self.argument, WonderCityArgument(iHangingGardens))
		self.assertNotEqual(self.argument, WonderCityArgument(iPyramids))
		self.assertNotEqual(self.argument, CapitalCityArgument())
	
	def test_get(self):
		wonder_city, other_city = cities = TestCities.owners(1, 2)
		
		wonder_city.setHasRealBuilding(iHangingGardens, True)
		
		try:
			self.assertEqualCity(self.argument.get(0), wonder_city)
		finally:
			cities.kill()
	
	def test_get_no_city(self):
		self.assertEqual(self.argument.get(0), NON_EXISTING)


class TestCivsArgument(ExtendedTestCase):

	def setUp(self):
		self.argument = CivsArgument(iEgypt, iBabylonia, iHarappa)
	
	def test_str(self):
		self.assertEqual(str(self.argument), "CivsArgument(Egypt, Babylonia, Harappa)")
	
	def test_repr(self):
		self.assertEqual(repr(self.argument), "CivsArgument(Egypt, Babylonia, Harappa)")
	
	def test_pickle(self):
		self.assertPickleable(self.argument)
	
	def test_equal(self):
		identical = CivsArgument(iEgypt, iBabylonia, iHarappa)
		different_order = CivsArgument(iHarappa, iEgypt, iBabylonia)
		different_civs = CivsArgument(iChina, iIndia, iGreece)
		
		self.assertEqual(self.argument, identical)
		self.assertEqual(self.argument, different_order)
		self.assertNotEqual(self.argument, different_civs)
	
	def test_contains_civ(self):
		self.assertEqual(iEgypt in self.argument, True)
		self.assertEqual(iBabylonia in self.argument, True)
		self.assertEqual(iHarappa in self.argument, True)
		self.assertEqual(iChina in self.argument, False)
	
	def test_contains_player(self):
		self.assertEqual(0 in self.argument, True)
		self.assertEqual(1 in self.argument, True)
		self.assertEqual(2 in self.argument, True)
		self.assertEqual(3 in self.argument, False)
	
	def test_iter(self):
		self.assertEqual(list(self.argument), [iEgypt, iBabylonia, iHarappa])
	
	def test_name(self):
		self.assertEqual(self.argument.name(), "Egypt, Babylonia and Harappa")
	
	def test_named(self):
		self.argument.named("Starting Civs")
		
		self.assertEqual(self.argument.name(), "Starting Civs")
	
	def test_group(self):
		argument = CivsArgument.group(iCivGroupAfrica)
		
		self.assertEqual(argument, CivsArgument(iEgypt, iPhoenicia, iEthiopia, iMali, iCongo))


class TestStateReligionBuildingArgument(ExtendedTestCase):

	def setUp(self):
		self.argument = StateReligionBuildingArgument(temple)
	
	def test_str(self):
		self.assertEqual(str(self.argument), "StateReligionBuildingArgument(temple)")
	
	def test_repr(self):
		self.assertEqual(repr(self.argument), "StateReligionBuildingArgument(temple)")
	
	def test_pickle(self):
		self.assertPickleable(self.argument)
	
	def test_equal(self):
		self.assertEqual(self.argument, StateReligionBuildingArgument(temple))
		self.assertNotEqual(self.argument, StateReligionBuildingArgument(cathedral))
		self.assertNotEqual(self.argument, CapitalCityArgument)
	
	def test_get(self):
		player(0).setLastStateReligion(iBuddhism)
		
		try:
			self.assertEqual(self.argument.get(0), iBuddhistTemple)
			
			player(0).setLastStateReligion(iHinduism)
			
			self.assertEqual(self.argument.get(0), iHinduTemple)
		finally:
			player(0).setLastStateReligion(-1)
	
	def test_get_no_state_religion(self):
		self.assertEqual(self.argument.get(0), NON_EXISTING)
		

test_cases = [
	TestNamedArgument,
	TestAggregate,
	TestAreaArgument,
	TestLocationCityArgument,
	TestCapitalCityArgument,
	TestReligionHolyCityArgument,
	TestStateReligionHolyCityArgument,
	TestWonderCityArgument,
	TestCivsArgument,
	TestStateReligionBuildingArgument,
]
