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
	
	def test_area(self):
		self.assertEqual(AMOUNT.area(3), None)


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
	
	def test_area(self):
		self.assertEqual(AREA.area(self.area), plots_.of(TestCities.CITY_LOCATIONS))


class TestAttitude(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(ATTITUDE), "Attitude")
	
	def test_repr(self):
		self.assertEqual(repr(ATTITUDE), "Attitude")
	
	def test_equal(self):
		self.assertEqual(ATTITUDE, AttitudeType("Attitude"))
	
	def test_pickle(self):
		self.assertPickleable(ATTITUDE)
	
	def test_validate(self):
		self.assertEqual(ATTITUDE.validate(AttitudeTypes.ATTITUDE_FURIOUS), True)
		self.assertEqual(ATTITUDE.validate(0), False)
		self.assertEqual(ATTITUDE.validate("Furious"), False)
	
	def test_format(self):
		self.assertEqual(ATTITUDE.format(AttitudeTypes.ATTITUDE_FURIOUS), "furious")
		self.assertEqual(ATTITUDE.format(0), "furious")
		
		self.assertEqual(ATTITUDE.format_repr(AttitudeTypes.ATTITUDE_FURIOUS), "Furious")
		self.assertEqual(ATTITUDE.format_repr(0), "Furious")
	
	def test_area(self):
		self.assertEqual(ATTITUDE.area(AttitudeTypes.ATTITUDE_FURIOUS), None)
		self.assertEqual(ATTITUDE.area(0), None)


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
	
	def test_area(self):
		self.assertEqual(BUILDING.area(iGranary), None)


class TestCity(ExtendedTestCase):

	def setUp(self):
		self.location_city = LocationCityDefinition(61, 31).named("Location City")
		self.capital_city = CapitalCityDefinition().named("Capital City")

	def test_str(self):
		self.assertEqual(str(CITY), "City")
	
	def test_repr(self):
		self.assertEqual(repr(CITY), "City")
	
	def test_equal(self):
		self.assertEqual(CITY, CityType("City"))
	
	def test_pickle(self):
		self.assertPickleable(CITY)
	
	def test_validate(self):
		self.assertEqual(CITY.validate(self.location_city), True)
		self.assertEqual(CITY.validate(self.capital_city), True)
		self.assertEqual(CITY.validate(1), False)
	
	def test_format(self):
		self.assertEqual(CITY.format(self.location_city), "Location City")
		self.assertEqual(CITY.format_repr(self.location_city), "Location City")
		
		self.assertEqual(CITY.format(self.capital_city), "Capital City")
		self.assertEqual(CITY.format_repr(self.capital_city), "Capital City")
	
	def test_area(self):
		self.assertEqual(CITY.area(self.location_city), plots_.of([(61, 31)]))
		self.assertEqual(CITY.area(self.capital_city), None)


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
	
	def test_area(self):
		self.assertEqual(CIVS.area(self.civs), None)


class TestCorporation(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(CORPORATION), "Corporation")
	
	def test_repr(self):
		self.assertEqual(repr(CORPORATION), "Corporation")
	
	def test_equal(self):
		self.assertEqual(CORPORATION, InfoType("Corporation", infos.corporation))
	
	def test_pickle(self):
		self.assertPickleable(CORPORATION)
	
	def test_validate(self):
		self.assertEqual(CORPORATION.validate(iTradingCompany), True)
		self.assertEqual(CORPORATION.validate("Trading Company"), False)
	
	def test_format(self):
		self.assertEqual(CORPORATION.format(iTradingCompany), "Trading Company")
		self.assertEqual(CORPORATION.format_repr(iTradingCompany), "Trading Company")
	
	def test_area(self):
		self.assertEqual(CORPORATION.area(iTradingCompany), None)


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
	
	def test_area(self):
		self.assertEqual(COUNT.area(3), None)


class TestCultureLevel(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(CULTURELEVEL), "CultureLevel")
	
	def test_repr(self):
		self.assertEqual(repr(CULTURELEVEL), "CultureLevel")
	
	def test_equal(self):
		self.assertEqual(CULTURELEVEL, CultureLevelType("CultureLevel"))
	
	def test_pickle(self):
		self.assertPickleable(CULTURELEVEL)
	
	def test_validate(self):
		self.assertEqual(CULTURELEVEL.validate(iCultureLevelInfluential), True)
		self.assertEqual(CULTURELEVEL.validate("Influential"), False)
	
	def test_format(self):
		self.assertEqual(CULTURELEVEL.format(iCultureLevelInfluential), "influential")
		self.assertEqual(CULTURELEVEL.format_repr(iCultureLevelInfluential), "Influential")
	
	def test_area(self):
		self.assertEqual(CULTURELEVEL.area(iCultureLevelInfluential), None)


class TestEra(ExtendedTestCase):
	
	def test_str(self):
		self.assertEqual(str(ERA), "Era")
	
	def test_repr(self):
		self.assertEqual(repr(ERA), "Era")
	
	def test_equal(self):
		self.assertEqual(ERA, InfoType("Era", infos.era))
	
	def test_pickle(self):
		self.assertPickleable(ERA)
	
	def test_validate(self):
		self.assertEqual(ERA.validate(iRenaissance), True)
		self.assertEqual(ERA.validate("Renaissance"), False)
	
	def test_format(self):
		self.assertEqual(ERA.format(iRenaissance), "Renaissance")
		self.assertEqual(ERA.format_repr(iRenaissance), "Renaissance")
	
	def test_area(self):
		self.assertEqual(ERA.area(iRenaissance), None)


class TestImprovement(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(IMPROVEMENT), "Improvement")
	
	def test_repr(self):
		self.assertEqual(repr(IMPROVEMENT), "Improvement")
	
	def test_equal(self):
		self.assertEqual(IMPROVEMENT, InfoType("Improvement", infos.improvement))
	
	def test_pickle(self):
		self.assertPickleable(IMPROVEMENT)
	
	def test_validate(self):
		self.assertEqual(IMPROVEMENT.validate(iFarm), True)
		self.assertEqual(IMPROVEMENT.validate("Farm"), False)
	
	def test_format(self):
		self.assertEqual(IMPROVEMENT.format(iFarm), "Farm")
		self.assertEqual(IMPROVEMENT.format_repr(iFarm), "Farm")
	
	def test_area(self):
		self.assertEqual(IMPROVEMENT.area(iFarm), None)


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
	
	def test_area(self):
		self.assertEqual(PERCENTAGE.area(1), None)


class TestProject(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(PROJECT), "Project")
	
	def test_repr(self):
		self.assertEqual(repr(PROJECT), "Project")
	
	def test_equal(self):
		self.assertEqual(PROJECT, InfoType("Project", infos.project))
	
	def test_pickle(self):
		self.assertPickleable(PROJECT)
	
	def test_validate(self):
		self.assertEqual(PROJECT.validate(iTheInternet), True)
		self.assertEqual(PROJECT.validate("The Internet"), False)
	
	def test_format(self):
		self.assertEqual(PROJECT.format(iTheInternet), "the Internet")
		self.assertEqual(PROJECT.format_repr(iTheInternet), "The Internet")
	
	def test_area(self):
		self.assertEqual(PROJECT.area(iTheInternet), None)


class TestReligion(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(RELIGION), "Religion")
	
	def test_repr(self):
		self.assertEqual(repr(RELIGION), "Religion")
	
	def test_equal(self):
		self.assertEqual(RELIGION, InfoType("Religion", infos.religion))
	
	def test_pickle(self):
		self.assertPickleable(RELIGION)
	
	def test_validate(self):
		self.assertEqual(RELIGION.validate(iOrthodoxy), True)
		self.assertEqual(RELIGION.validate("Orthodoxy"), False)
	
	def test_format(self):
		self.assertEqual(RELIGION.format(iOrthodoxy), "Orthodoxy")
		self.assertEqual(RELIGION.format_repr(iOrthodoxy), "Orthodoxy")
	
	def test_area(self):
		self.assertEqual(RELIGION.area(iOrthodoxy), None)
		
		
class TestReligionAdjective(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(RELIGION_ADJECTIVE), "ReligionAdjective")
	
	def test_repr(self):
		self.assertEqual(repr(RELIGION_ADJECTIVE), "ReligionAdjective")
	
	def test_equal(self):
		self.assertEqual(RELIGION_ADJECTIVE, ReligionAdjectiveType("ReligionAdjective"))
	
	def test_pickle(self):
		self.assertPickleable(RELIGION_ADJECTIVE)
	
	def test_validate(self):
		self.assertEqual(RELIGION_ADJECTIVE.validate(iOrthodoxy), True)
		self.assertEqual(RELIGION_ADJECTIVE.validate("Orthodoxy"), False)
	
	def test_format(self):
		self.assertEqual(RELIGION_ADJECTIVE.format(iOrthodoxy), "Orthodox")
		self.assertEqual(RELIGION_ADJECTIVE.format_repr(iOrthodoxy), "Orthodoxy")
	
	def test_area(self):
		self.assertEqual(RELIGION_ADJECTIVE.area(iOrthodoxy), None)


class TestResource(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(RESOURCE), "Resource")
	
	def test_repr(self):
		self.assertEqual(repr(RESOURCE), "Resource")
	
	def test_equal(self):
		self.assertEqual(RESOURCE, InfoType("Resource", infos.bonus))
	
	def test_pickle(self):
		self.assertPickleable(RESOURCE)
	
	def test_validate(self):
		self.assertEqual(RESOURCE.validate(iCopper), True)
		self.assertEqual(RESOURCE.validate("Copper"), False)
	
	def test_format(self):
		self.assertEqual(RESOURCE.format(iCopper), "Copper")
		self.assertEqual(RESOURCE.format_repr(iCopper), "Copper")
	
	def test_area(self):
		self.assertEqual(RESOURCE.area(iCopper), None)


class TestRoutes(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(ROUTES), "Routes")
	
	def test_repr(self):
		self.assertEqual(repr(ROUTES), "Routes")
	
	def test_equal(self):
		self.assertEqual(ROUTES, InfosType("Routes", infos.routes))
	
	def test_pickle(self):
		self.assertPickleable(ROUTES)
	
	def test_validate(self):
		self.assertEqual(ROUTES.validate([iRouteRoad, iRouteRailroad]), True)
		self.assertEqual(ROUTES.validate(iRouteRoad), False)
		self.assertEqual(ROUTES.validate(["Road"]), False)
	
	def test_format(self):
		self.assertEqual(ROUTES.format([iRouteRoad]), "Road")
		self.assertEqual(ROUTES.format([iRouteRoad, iRouteRomanRoad]), "Road or Roman Road")
		self.assertEqual(ROUTES.format([iRouteRoad, iRouteRomanRoad, iRouteRailroad]), "Road, Roman Road or Railroad")
		
		self.assertEqual(ROUTES.format_repr([iRouteRoad, iRouteRomanRoad, iRouteRailroad]), "Road, Roman Road or Railroad")
	
	def test_area(self):
		self.assertEqual(ROUTES.area([iRouteRoad]), None)


class TestSpecialist(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(SPECIALIST), "Specialist")
	
	def test_repr(self):
		self.assertEqual(repr(SPECIALIST), "Specialist")
	
	def test_equal(self):
		self.assertEqual(SPECIALIST, InfoType("Specialist", infos.specialist))
	
	def test_pickle(self):
		self.assertPickleable(SPECIALIST)
	
	def test_validate(self):
		self.assertEqual(SPECIALIST.validate(iSpecialistGreatScientist), True)
		self.assertEqual(SPECIALIST.validate("Great Scientist"), False)
	
	def test_format(self):
		self.assertEqual(SPECIALIST.format(iSpecialistGreatScientist, bPlural=False), "Great Scientist")
		self.assertEqual(SPECIALIST.format(iSpecialistGreatScientist, bPlural=True), "Great Scientists")
		
		self.assertEqual(SPECIALIST.format_repr(iSpecialistGreatScientist), "Great Scientist")
	
	def test_area(self):
		self.assertEqual(SPECIALIST.area(iSpecialistGreatScientist), None)


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
		self.assertEqual(TECH.validate(iEngineering), True)
		self.assertEqual(TECH.validate("Engineering"), False)
	
	def test_format(self):
		self.assertEqual(TECH.format(iEngineering), "Engineering")
		self.assertEqual(TECH.format_repr(iEngineering), "Engineering")
	
	def test_area(self):
		self.assertEqual(TECH.area(iEngineering), None)


class TestUnit(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(UNIT), "Unit")
	
	def test_repr(self):
		self.assertEqual(repr(UNIT), "Unit")
	
	def test_equal(self):
		self.assertEqual(UNIT, InfoType("Unit", infos.unit))
	
	def test_pickle(self):
		self.assertPickleable(UNIT)
	
	def test_validate(self):
		self.assertEqual(UNIT.validate(iSwordsman), True)
		self.assertEqual(UNIT.validate("Swordsman"), False)
	
	def test_format(self):
		self.assertEqual(UNIT.format(iSwordsman), "Swordsman")
		self.assertEqual(UNIT.format_repr(iSwordsman), "Swordsman")
	
	def test_area(self):
		self.assertEqual(UNIT.area(iSwordsman), None)


test_cases = [
	TestEnum,
	TestAggregate,
	TestAmount,
	TestArea,
	TestAttitude,
	TestBuilding,
	TestCity,
	TestCivs,
	TestCorporation,
	TestCount,
	TestCultureLevel,
	TestEra,
	TestImprovement,
	TestPercentage,
	TestProject,
	TestReligion,
	TestReligionAdjective,
	TestResource,
	TestRoutes,
	TestSpecialist,
	TestTech,
	TestUnit,
]