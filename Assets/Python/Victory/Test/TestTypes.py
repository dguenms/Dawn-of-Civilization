from VictoryTypes import *

from TestVictoryCommon import *


class TestEnum(ExtendedTestCase):

	def setUp(self):
		self.enum = Enum("EnumType", 0, "Name")
	
	def test_str(self):
		self.assertEqual(str(self.enum), "EnumType.Name")
	
	def test_repr(self):
		self.assertEqual(repr(self.enum), "EnumType.Name")
	
	def test_equal(self):
		identical = Enum("EnumType", 0, "Name")
		different_type = Enum("OtherType", 0, "Name")
		different_value = Enum("EnumType", 1, "Name")
		different_name = Enum("EnumType", 0, "OtherName")
		
		self.assertEqual(self.enum, identical)
		self.assertNotEqual(self.enum, different_type)
		self.assertNotEqual(self.enum, different_value)
		self.assertEqual(self.enum, different_name)
		self.assertNotEqual(self.enum, 0)
	
	def test_pickle(self):
		self.assertPickleable(self.enum)
	
	def test_of(self):
		first, second, third = Enum.of("EnumType", ("First", "Second", "Third"))
		
		self.assertEqual(first, Enum("EnumType", 0, "First"))
		self.assertEqual(second, Enum("EnumType", 1, "Second"))
		self.assertEqual(third, Enum("EnumType", 2, "Third"))
		
		self.assertEqual(str(first), "EnumType.First")
		self.assertEqual(str(second), "EnumType.Second")
		self.assertEqual(str(third), "EnumType.Third")


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


class TestAmount(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(AMOUNT), "Amount")
	
	def test_repr(self):
		self.assertEqual(repr(AMOUNT), "Amount")
	
	def test_equal(self):
		self.assertEqual(AMOUNT, SimpleType("Amount", int))
	
	def test_pickle(self):
		self.assertPickleable(AMOUNT)
	
	def test_validate(self):
		self.assertEqual(AMOUNT.validate(1), True)
		self.assertEqual(AMOUNT.validate("1"), False)
	
	def test_format(self):
		self.assertEqual(AMOUNT.format(3), "3")
		self.assertEqual(AMOUNT.format_repr(3), "3")


class TestArea(ExtendedTestCase):

	def setUp(self):
		self.area = AreaDefinition().of(TestCities.CITY_LOCATIONS).named("Test Area")
	
	def test_str(self):
		self.assertEqual(str(AREA), "Area")
	
	def test_repr(self):
		self.assertEqual(repr(AREA), "Area")
	
	def test_equal(self):
		self.assertEqual(AREA, AreaType("Area"))
	
	def test_pickle(self):
		self.assertPickleable(AREA)
	
	def test_validate(self):
		self.assertEqual(AREA.validate(self.area), True)
		self.assertEqual(AREA.validate(1), False)
	
	def test_format(self):
		self.assertEqual(AREA.format(self.area), "Test Area")
		self.assertEqual(AREA.format(self.area), "Test Area")


class TestBuilding(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(BUILDING), "Building")
	
	def test_repr(self):
		self.assertEqual(repr(BUILDING), "Building")
	
	def test_equal(self):
		self.assertEqual(BUILDING, InfoType("Building", infos.building))
	
	def test_pickle(self):
		self.assertPickleable(BUILDING)
	
	def test_validate(self):
		self.assertEqual(BUILDING.validate(1), True)
		self.assertEqual(BUILDING.validate("1"), False)
		self.assertEqual(BUILDING.validate(plots.of([(0, 0)])), False)
	
	def test_format(self):
		self.assertEqual(BUILDING.format(iGranary, bPlural=False), "Granary")
		self.assertEqual(BUILDING.format(iGranary, bPlural=True), "Granaries")
		
		self.assertEqual(BUILDING.format_repr(iGranary), "Granary")


class TestCity(ExtendedTestCase):

	def setUp(self):
		self.city = CityDefinition(61, 31).named("Test City")

	def test_str(self):
		self.assertEqual(str(CITY), "City")
	
	def test_repr(self):
		self.assertEqual(repr(CITY), "City")
	
	def test_equal(self):
		self.assertEqual(CITY, CityType("City"))
	
	def test_pickle(self):
		self.assertPickleable(CITY)
	
	def test_validate(self):
		self.assertEqual(CITY.validate(self.city), True)
		self.assertEqual(CITY.validate(1), False)
	
	def test_format(self):
		self.assertEqual(CITY.format(self.city), "Test City")
		self.assertEqual(CITY.format_repr(self.city), "Test City")


class TestCivs(ExtendedTestCase):

	def setUp(self):
		self.civs = CivsDefinition(iEgypt, iBabylonia, iHarappa)
	
	def test_str(self):
		self.assertEqual(str(CIVS), "Civs")
	
	def test_repr(self):
		self.assertEqual(repr(CIVS), "Civs")
	
	def test_equal(self):
		self.assertEqual(CIVS, CivsType("Civs"))
	
	def test_pickle(self):
		self.assertPickleable(CIVS)
	
	def test_validate(self):
		self.assertEqual(CIVS.validate(self.civs), True)
		self.assertEqual(CIVS.validate(1), False)
	
	def test_format(self):
		self.assertEqual(CIVS.format(self.civs), "Egypt, Babylonia and Harappa")
		self.assertEqual(CIVS.format_repr(self.civs), "Egypt, Babylonia and Harappa")


class TestCount(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(COUNT), "Count")
	
	def test_repr(self):
		self.assertEqual(repr(COUNT), "Count")
	
	def test_equal(self):
		self.assertEqual(COUNT, CountType("Count"))
	
	def test_pickle(self):
		self.assertPickleable(COUNT)
	
	def test_validate(self):
		self.assertEqual(COUNT.validate(1), True)
		self.assertEqual(COUNT.validate("1"), False)
	
	def test_format(self):
		self.assertEqual(COUNT.format(3), "three")
		self.assertEqual(COUNT.format_repr(3), "3")


class TestPercentage(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(PERCENTAGE), "Percentage")
	
	def test_repr(self):
		self.assertEqual(repr(PERCENTAGE), "Percentage")
	
	def test_equal(self):
		self.assertEqual(PERCENTAGE, PercentageType("Percentage"))
	
	def test_pickle(self):
		self.assertPickleable(PERCENTAGE)
	
	def test_validate(self):
		self.assertEqual(PERCENTAGE.validate(1), True)
		self.assertEqual(PERCENTAGE.validate("1"), False)
	
	def test_format(self):
		self.assertEqual(PERCENTAGE.format(1), "1%")
		self.assertEqual(PERCENTAGE.format_repr(1), "1%")


class TestTech(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(TECH), "Tech")
	
	def test_repr(self):
		self.assertEqual(repr(TECH), "Tech")
	
	def test_equal(self):
		self.assertEqual(TECH, InfoType("Tech", infos.tech))
	
	def test_pickle(self):
		self.assertPickleable(TECH)
	
	def test_validate(self):
		self.assertEqual(TECH.validate(1), True)
		self.assertEqual(TECH.validate("1"), False)
	
	def test_format(self):
		self.assertEqual(TECH.format(iEngineering), "Engineering")
		self.assertEqual(TECH.format_repr(iEngineering), "Engineering")


test_cases = [
	TestEnum,
	TestAggregate,
	TestAmount,
	TestArea,
	TestBuilding,
	TestCity,
	TestCivs,
	TestCount,
	TestPercentage,
	TestTech,
]