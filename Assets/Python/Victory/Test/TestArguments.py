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
	

class TestLocalCityArgument(ExtendedTestCase):

	def setUp(self):
		self.location = TestCities.CITY_LOCATIONS[0]
		self.argument = LocationCityArgument(self.location)
		
	def test_str(self):
		self.assertEqual(str(self.argument), "LocationCityArgument(61, 31)")
	
	def test_repr(self):
		self.assertEqual(repr(self.argument), "LocationCityArgument(61, 31)")
	
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
		self.assertEqual(self.argument.get(0), None)


class TestCapitalCityArgument(ExtendedTestCase):

	def setUp(self):
		self.argument = CapitalCityArgument()
	
	def test_str(self):
		self.assertEqual(str(self.argument), "CapitalCityArgument()")
	
	def test_repr(self):
		self.assertEqual(repr(self.argument), "CapitalCityArgument()")
	
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
		self.assertEqual(self.argument.get(0), None)
	

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
	
	def test_without(self):
		self.assertEqual(self.argument.without(iHarappa), CivsArgument(iEgypt, iBabylonia))
	
	def test_where(self):
		self.assertEqual(self.argument.where(lambda p: civ(p) == iEgypt), CivsArgument(iEgypt))
	
	def test_name(self):
		self.assertEqual(self.argument.name(), "Egypt, Babylonia and Harappa")
	
	def test_named(self):
		self.argument.named("Starting Civs")
		
		self.assertEqual(self.argument.name(), "Starting Civs")
	
	def test_group(self):
		argument = CivsArgument.group(iCivGroupAfrica)
		
		self.assertEqual(argument, CivsArgument(iEgypt, iPhoenicia, iEthiopia, iMali, iCongo))
		

test_cases = [
	TestNamedArgument,
	TestAreaArgument,
	TestLocalCityArgument,
	TestCapitalCityArgument,
	TestCivsArgument,
]
