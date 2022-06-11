from VictoryUtils import *

from TestVictoryCommon import *


class TestTextProcessing(ExtendedTestCase):

	def test_format_articles(self):
		self.assertEqual(format_articles("The Internet"), "the Internet")
		self.assertEqual(format_articles("the Internet"), "the Internet")
		self.assertEqual(format_articles("Swordsman"), "Swordsman")
		
		
class TestNamedDefinition(ExtendedTestCase):

	def setUp(self):
		self.definition = NamedDefinition()
	
	def test_unnamed(self):
		self.assertEqual(self.definition.name(), "")
	
	def test_named(self):
		definition = self.definition.named("Definition")
		
		self.assertType(definition, NamedDefinition)
		
		self.assertEqual(self.definition.name(), "Definition")
		self.assertEqual(definition.name(), "Definition")
	
	def test_renamed(self):
		self.definition.named("First")
		self.assertEqual(self.definition.name(), "First")
		
		self.definition.named("Second")
		self.assertEqual(self.definition.name(), "Second")


class TestAreaDefinition(ExtendedTestCase):

	def setUp(self):
		self.plots = AreaDefinitionFactory()

	def test(self):
		even = lambda p: (p.getX() + p.getY()) % 2 == 0
		
		area = self.plots.rectangle((0, 0), (1, 1)).where(even)
		
		self.assertType(area, AreaDefinition)
		self.assertEqual(area.calls, [("rectangle", ((0, 0), (1, 1)), {}), ("where", (even,), {})])
		
		area = area.create()
		
		self.assertType(area, Plots)
		self.assertEqual(len(area), 2)
		self.assertEqual((0, 0) in area, True)
		self.assertEqual((1, 1) in area, True)
	
	def test_equal(self):
		area = self.plots.of([(0, 0), (0, 1)])
		
		identical = self.plots.of([(0, 1), (0, 0)])
		different_type = PlotFactory().of([(0, 0), (0, 1)])
		different_plots = self.plots.of([(0, 0), (1, 1)])
		
		self.assertEqual(area, identical)
		self.assertNotEqual(area, different_type)
		self.assertNotEqual(area, different_plots)
	
	def test_str(self):
		self.assertEqual(str(plots.rectangle((0, 0), (1, 1)).region(2)), "AreaDefinition.rectangle((0, 0), (1, 1)).region(2)")
	
	def test_pickle(self):
		self.assertPickleable(self.plots.rectangle((0, 0), (1, 1)).region(2))
	
	def test_without_create(self):
		area = self.plots.rectangle((0, 0), (1, 1))
		
		self.assertType(area, AreaDefinition)
		
		self.assertEqual(len(area), 4)
		self.assertEqual((0, 0) in area, True)
	
	def test_named(self):
		area = self.plots.all().named("Area")
		
		self.assertType(area, AreaDefinition)
		self.assertEqual(area.name(), "Area")
		
		area = area.create()
		
		self.assertType(area, Plots)
		self.assertEqual(area.name(), "Area")
	
	def test_multiple_creates(self):
		area = self.plots.rectangle((0, 0), (1, 1))
		
		area1 = area.create()
		area2 = area.create()
		
		self.assertNotEqual(id(area1), id(area2))
	

class TestLocalCityDefinition(ExtendedTestCase):

	def setUp(self):
		self.location = TestCities.CITY_LOCATIONS[0]
		self.definition = LocationCityDefinition(self.location)
		
	def test_str(self):
		self.assertEqual(str(self.definition), "LocationCityDefinition(61, 31)")
	
	def test_repr(self):
		self.assertEqual(repr(self.definition), "LocationCityDefinition(61, 31)")
	
	def test_pickle(self):
		self.assertPickleable(self.definition)
	
	def test_equal_definition(self):
		identical = LocationCityDefinition(self.location)
		different = LocationCityDefinition((62, 31))
		
		self.assertEqual(self.definition, identical)
		self.assertNotEqual(self.definition, different)
	
	def test_equal_city(self):
		same_location, different_location = cities = TestCities.num(2)
		
		try:
			self.assertEqual(self.definition, same_location)
			self.assertNotEqual(self.definition, different_location)
		finally:
			cities.kill()
	
	def test_from_varargs(self):
		definition = LocationCityDefinition(*self.location)
		self.assertEqual(str(definition), "LocationCityDefinition(61, 31)")
	
	def test_get(self):
		city = TestCities.one()
		
		try:
			self.assertEqual(location(self.definition.get(0)), location(city))
		finally:
			city.kill()
	
	def test_get_no_city(self):
		self.assertEqual(self.definition.get(0), None)


class TestCapitalCityDefinition(ExtendedTestCase):

	def setUp(self):
		self.definition = CapitalCityDefinition()
	
	def test_str(self):
		self.assertEqual(str(self.definition), "CapitalCityDefinition()")
	
	def test_repr(self):
		self.assertEqual(repr(self.definition), "CapitalCityDefinition()")
	
	def test_pickle(self):
		self.assertPickleable(self.definition)
	
	def test_equal_definition(self):
		self.assertEqual(self.definition, CapitalCityDefinition())
		self.assertNotEqual(self.definition, LocationCityDefinition(61, 31))
	
	def test_equal_city(self):
		capital, not_capital = cities = TestCities.num(2)
		capital.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqual(self.definition, capital)
			self.assertNotEqual(self.definition, not_capital)
		finally:
			cities.kill()
	
	def test_get(self):
		capital, not_capital = cities = TestCities.num(2)
		capital.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqual(location(self.definition.get(0)), location(capital))
		finally:
			cities.kill()
	
	def test_get_no_city(self):
		self.assertEqual(self.definition.get(0), None)
	

class TestCivsDefinition(ExtendedTestCase):

	def setUp(self):
		self.definition = CivsDefinition(iEgypt, iBabylonia, iHarappa)
	
	def test_str(self):
		self.assertEqual(str(self.definition), "CivsDefinition(Egypt, Babylonia, Harappa)")
	
	def test_repr(self):
		self.assertEqual(repr(self.definition), "CivsDefinition(Egypt, Babylonia, Harappa)")
	
	def test_pickle(self):
		self.assertPickleable(self.definition)
	
	def test_equal(self):
		identical = CivsDefinition(iEgypt, iBabylonia, iHarappa)
		different_order = CivsDefinition(iHarappa, iEgypt, iBabylonia)
		different_civs = CivsDefinition(iChina, iIndia, iGreece)
		
		self.assertEqual(self.definition, identical)
		self.assertEqual(self.definition, different_order)
		self.assertNotEqual(self.definition, different_civs)
	
	def test_contains_civ(self):
		self.assertEqual(iEgypt in self.definition, True)
		self.assertEqual(iBabylonia in self.definition, True)
		self.assertEqual(iHarappa in self.definition, True)
		self.assertEqual(iChina in self.definition, False)
	
	def test_contains_player(self):
		self.assertEqual(0 in self.definition, True)
		self.assertEqual(1 in self.definition, True)
		self.assertEqual(2 in self.definition, True)
		self.assertEqual(3 in self.definition, False)
	
	def test_iter(self):
		self.assertEqual(list(self.definition), [iEgypt, iBabylonia, iHarappa])
	
	def test_without(self):
		self.assertEqual(self.definition.without(iHarappa), CivsDefinition(iEgypt, iBabylonia))
	
	def test_where(self):
		self.assertEqual(self.definition.where(lambda p: civ(p) == iEgypt), CivsDefinition(iEgypt))
	
	def test_name(self):
		self.assertEqual(self.definition.name(), "Egypt, Babylonia and Harappa")
	
	def test_named(self):
		self.definition.named("Starting Civs")
		
		self.assertEqual(self.definition.name(), "Starting Civs")
	
	def test_group(self):
		definition = CivsDefinition.group(iCivGroupAfrica)
		
		self.assertEqual(definition, CivsDefinition(iEgypt, iPhoenicia, iEthiopia, iMali, iCongo))
		

test_cases = [
	TestTextProcessing,
	TestNamedDefinition,
	TestAreaDefinition,
	TestLocalCityDefinition,
	TestCapitalCityDefinition,
	TestCivsDefinition,
]
