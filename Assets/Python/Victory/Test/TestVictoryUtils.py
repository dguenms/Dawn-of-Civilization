from VictoryUtils import *

from TestVictoryCommon import *


class TestTextProcessing(ExtendedTestCase):
	
	def test_number_word_a(self):
		result = number_word(1)
		
		self.assertEqual(result, "a")
	
	def test_number_word_two(self):
		result = number_word(2)
		
		self.assertEqual(result, "two")
	
	def test_number_word_ten(self):
		result = number_word(10)
		
		self.assertEqual(result, "ten")
	
	def test_number_word_twenty(self):
		result = number_word(20)
		
		self.assertEqual(result, "20")
	
	def test_ordinal_word_first(self):
		self.assertEqual(ordinal_word(1), "first")
	
	def test_ordinal_word_100th(self):
		self.assertEqual(ordinal_word(100), "100th")
	
	def test_plural(self):
		result = plural("word")
		
		self.assertEqual(result, "words")
	
	def test_plural_ends_with_s(self):
		result = plural("words")
		
		self.assertEqual(result, "words")
	
	def test_plural_ends_with_y(self):
		result = plural("library")
		
		self.assertEqual(result, "libraries")
	
	def test_plural_ends_with_ch(self):
		self.assertEqual(plural("church"), "churches")
	
	def test_plural_ends_with_sh(self):
		self.assertEqual(plural("marsh"), "marshes")
	
	def test_plural_ends_with_man(self):
		self.assertEqual(plural("swordsman"), "swordsmen")
	
	def test_plural_irregular(self):
		self.assertEqual(plural("Ship of the Line"), "Ships of the Line")
		self.assertEqual(plural("Great Statesman"), "Great Statesmen")
		self.assertEqual(plural("cathedral of your state religion"), "cathedrals of your state religion")
	
	def test_capitalize(self):
		self.assertEqual(capitalize("hello"), "Hello")
	
	def test_capitalize_multiple_words(self):
		self.assertEqual(capitalize("hello world"), "Hello world")
	
	def test_capitalize_already_capital(self):
		self.assertEqual(capitalize("Hello World"), "Hello World")
	
	def test_capitalize_single_character(self):
		self.assertEqual(capitalize("a"), "A")
	
	def test_capitalize_empty(self):
		self.assertEqual(capitalize(""), "")
		
		
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
	

class TestCityDefinition(ExtendedTestCase):

	def setUp(self):
		self.location = TestCities.CITY_LOCATIONS[0]
		self.definition = CityDefinition(self.location)
		
	def test_str(self):
		self.assertEqual(str(self.definition), "CityDefinition(61, 31)")
	
	def test_repr(self):
		self.assertEqual(repr(self.definition), "CityDefinition(61, 31)")
	
	def test_pickle(self):
		self.assertPickleable(self.definition)
	
	def test_equal_definition(self):
		identical = CityDefinition(self.location)
		different = CityDefinition((62, 31))
		
		self.assertEqual(self.definition, identical)
		self.assertNotEqual(self.definition, different)
	
	def test_equal_city(self):
		city_matching, city_different = cities = TestCities.num(2)
		
		try:
			self.assertEqual(self.definition, city_matching)
			self.assertNotEqual(self.definition, city_different)
		finally:
			cities.kill()
	
	def test_nonzero(self):
		city = TestCities.one()
		
		try:
			self.assertEqual(bool(self.definition), True)
		finally:
			city.kill()
	
	def test_nonzero_no_city(self):
		self.assertEqual(bool(self.definition), False)
	
	def test_from_varargs(self):
		definition = CityDefinition(*self.location)
		self.assertEqual(str(definition), "CityDefinition(61, 31)")
	
	def test_city(self):
		city = TestCities.one()
		
		try:
			self.assertEqual(location(self.definition.city), location(city))
		finally:
			city.kill()
	
	def test_city_no_city(self):
		self.assertEqual(self.definition.city, None)
	
	def test_get_owner(self):
		city = TestCities.one()
		
		try:
			self.assertEqual(self.definition.getOwner(), city.getOwner())
		finally:
			city.kill()
	
	def test_get_owner_no_city(self):
		self.assertEqual(self.definition.getOwner(), None)
	
	def test_is_has_building(self):
		city = TestCities.one()
		city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.definition.isHasBuilding(iGranary), True)
		finally:
			city.kill()
	
	def test_is_has_building_no_city(self):
		self.assertEqual(self.definition.isHasBuilding(iGranary), None)
	

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
	TestCityDefinition,
	TestCivsDefinition,
]
