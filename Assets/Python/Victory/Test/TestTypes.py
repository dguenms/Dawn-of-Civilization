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


class TestAmount(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(AMOUNT), "Amount")
	
	def test_repr(self):
		self.assertEqual(repr(AMOUNT), "Amount")
	
	def test_equal(self):
		self.assertEqual(AMOUNT, AmountType("Amount"))
	
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
		self.area = AreaArgument().of(TestCities.CITY_LOCATIONS).named("Test Area")
	
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
		self.assertEqual(AREA.area(self.area), plots.of(TestCities.CITY_LOCATIONS))
	
	def test_area_aggregate(self):
		area1 = AreaArgument().of([(0, 0)])
		area2 = AreaArgument().of([(0, 1)])
		aggregate = SumAggregate(area1, area2)
		
		self.assertEqual(AREA.area(aggregate), plots.of([(0, 0), (0, 1)]))


class TestAreaOrCity(ExtendedTestCase):

	def setUp(self):
		self.area = AreaArgument().of(TestCities.CITY_LOCATIONS).named("Test Area")
		self.city = LocationCityArgument(TestCities.CITY_LOCATIONS[0]).named("Test City")
	
	def test_str(self):
		self.assertEqual(str(AREA_OR_CITY), "AreaOrCity")
	
	def test_repr(self):
		self.assertEqual(repr(AREA_OR_CITY), "AreaOrCity")
	
	def test_equal(self):
		self.assertEqual(AREA_OR_CITY, AreaOrCityType("AreaOrCity"))
	
	def test_pickle(self):
		self.assertPickleable(AREA_OR_CITY)
	
	def test_validate(self):
		self.assertEqual(AREA_OR_CITY.validate(self.area), True)
		self.assertEqual(AREA_OR_CITY.validate(self.city), True)
		self.assertEqual(AREA_OR_CITY.validate("area or city"), False)
	
	def test_format(self):
		self.assertEqual(AREA_OR_CITY.format(self.area), "Test Area")
		self.assertEqual(AREA_OR_CITY.format(self.city), "Test City")
		
		self.assertEqual(AREA_OR_CITY.format_repr(self.area), "Test Area")
		self.assertEqual(AREA_OR_CITY.format_repr(self.city), "Test City")
	
	def test_area(self):
		self.assertEqual(AREA_OR_CITY.area(self.area), plots.of(TestCities.CITY_LOCATIONS))
		self.assertEqual(AREA_OR_CITY.area(self.city), plots.of([TestCities.CITY_LOCATIONS[0]]))


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
		self.assertEqual(BUILDING.validate(StateReligionBuildingArgument(temple)), True)
		
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
		self.location_city = LocationCityArgument(61, 31).named("Location City")
		self.capital_city = CapitalCityArgument().named("Capital City")

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
		self.assertEqual(CITY.area(self.location_city), plots.of([(61, 31)]))
		self.assertEqual(CITY.area(self.capital_city), None)


class TestCivs(ExtendedTestCase):

	def setUp(self):
		self.civs = CivsArgument(iEgypt, iBabylonia, iHarappa)
	
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


class TestFeature(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(FEATURE), "Feature")
	
	def test_repr(self):
		self.assertEqual(repr(FEATURE), "Feature")
	
	def test_equal(self):
		self.assertEqual(FEATURE, InfoType("Feature", infos.feature))
	
	def test_pickle(self):
		self.assertPickleable(FEATURE)
	
	def test_validate(self):
		self.assertEqual(FEATURE.validate(iForest), True)
		self.assertEqual(FEATURE.validate("Forest"), False)
	
	def test_format(self):
		self.assertEqual(FEATURE.format(iForest), "Forest")
		self.assertEqual(FEATURE.format_repr(iForest), "Forest")
	
	def test_area(self):
		self.assertEqual(FEATURE.area(iForest), None)


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
		
		self.assertEqual(PERCENTAGE.format(50), "half")
	
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
		self.assertEqual(ROUTES.validate(NamedList(iRouteRoad, iRouteRailroad)), True)
		
		self.assertEqual(ROUTES.validate(iRouteRoad), False)
		self.assertEqual(ROUTES.validate(["Road"]), False)
	
	def test_format(self):
		self.assertEqual(ROUTES.format([iRouteRoad]), "Road")
		self.assertEqual(ROUTES.format([iRouteRoad, iRouteRomanRoad]), "Road or Roman Road")
		self.assertEqual(ROUTES.format([iRouteRoad, iRouteRomanRoad, iRouteRailroad]), "Road, Roman Road or Railroad")
		self.assertEqual(ROUTES.format(NamedList(iRouteRoad, iRouteRailroad).named("routes")), "routes")
		
		self.assertEqual(ROUTES.format_repr([iRouteRoad, iRouteRomanRoad, iRouteRailroad]), "Road, Roman Road or Railroad")
	
	def test_area(self):
		self.assertEqual(ROUTES.area([iRouteRoad]), None)


class TestSpecialist(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(SPECIALIST), "Specialist")
	
	def test_repr(self):
		self.assertEqual(repr(SPECIALIST), "Specialist")
	
	def test_equal(self):
		self.assertEqual(SPECIALIST, SpecialistType("Specialist"))
	
	def test_pickle(self):
		self.assertPickleable(SPECIALIST)
	
	def test_validate(self):
		self.assertEqual(SPECIALIST.validate(iSpecialistGreatScientist), True)
		self.assertEqual(SPECIALIST.validate("Great Scientist"), False)
	
	def test_format(self):
		self.assertEqual(SPECIALIST.format(iSpecialistGreatScientist, bPlural=False), "Great Scientist")
		self.assertEqual(SPECIALIST.format(iSpecialistGreatScientist, bPlural=True), "Great Scientists")
		
		self.assertEqual(SPECIALIST.format_repr(iSpecialistGreatScientist), "Great Scientist")
	
	def test_format_aggregate(self):
		normal_specialists = SumAggregate(iSpecialistScientist, iSpecialistEngineer, iSpecialistMerchant)
		great_specialists = SumAggregate(iSpecialistGreatScientist, iSpecialistGreatEngineer, iSpecialistGreatMerchant)
		mixed_specialists = SumAggregate(iSpecialistGreatScientist, iSpecialistGreatEngineer, iSpecialistMerchant)
		named = SumAggregate(iSpecialistGreatScientist, iSpecialistGreatEngineer).named("Inventors")
		
		self.assertEqual(SPECIALIST.format(normal_specialists, bPlural=True), "Scientists, Engineers and Merchants")
		self.assertEqual(SPECIALIST.format(great_specialists, bPlural=True), "Great Scientists, Engineers and Merchants")
		self.assertEqual(SPECIALIST.format(mixed_specialists, bPlural=True), "Great Scientists, Great Engineers and Merchants")
		self.assertEqual(SPECIALIST.format(named, bPlural=True), "Inventors")
	
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


class TestTerrain(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(TERRAIN), "Terrain")
	
	def test_repr(self):
		self.assertEqual(repr(TERRAIN), "Terrain")
	
	def test_equal(self):
		self.assertEqual(TERRAIN, InfoType("Terrain", infos.terrain))
	
	def test_pickle(self):
		self.assertPickleable(TERRAIN)
	
	def test_validate(self):
		self.assertEqual(TERRAIN.validate(iOcean), True)
		self.assertEqual(TERRAIN.validate("Ocean"), False)
	
	def test_format(self):
		self.assertEqual(TERRAIN.format(iOcean), "Ocean")
		self.assertEqual(TERRAIN.format_repr(iOcean), "Ocean")
	
	def test_area(self):
		self.assertEqual(TERRAIN.area(iOcean), None)


class TestTurns(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(TURNS), "Turns")
	
	def test_repr(self):
		self.assertEqual(repr(TURNS), "Turns")
	
	def test_equal(self):
		self.assertEqual(TURNS, TurnsType("Turns"))
	
	def test_pickle(self):
		self.assertPickleable(TURNS)
	
	def test_validate(self):
		self.assertEqual(TURNS.validate(10), True)
		self.assertEqual(TURNS.validate("ten"), False)
	
	def test_format(self):
		self.assertEqual(TURNS.format(10), "ten")
		self.assertEqual(TURNS.format_repr(10), "10")
	
	def test_area(self):
		self.assertEqual(TURNS.area(10), None)


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


class TestUnitCombat(ExtendedTestCase):

	def test_str(self):
		self.assertEqual(str(UNITCOMBAT), "UnitCombat")
	
	def test_repr(self):
		self.assertEqual(repr(UNITCOMBAT), "UnitCombat")
	
	def test_equal(self):
		self.assertEqual(UNITCOMBAT, UnitCombatType("UnitCombat"))
	
	def test_pickle(self):
		self.assertPickleable(UNITCOMBAT)
	
	def test_validate(self):
		self.assertEqual(UNITCOMBAT.validate(UnitCombatTypes.UNITCOMBAT_MELEE), True)
		self.assertEqual(UNITCOMBAT.validate("Melee"), False)
		self.assertEqual(UNITCOMBAT.validate(1), False)
	
	def test_format(self):
		self.assertEqual(UNITCOMBAT.format(UnitCombatTypes.UNITCOMBAT_MELEE), "melee units")
		self.assertEqual(UNITCOMBAT.format_repr(UnitCombatTypes.UNITCOMBAT_MELEE), "Melee")
	
	def test_area(self):
		self.assertEqual(UNITCOMBAT.area(UnitCombatTypes.UNITCOMBAT_MELEE), None)


test_cases = [
	TestEnum,
	TestAmount,
	TestArea,
	TestAreaOrCity,
	TestAttitude,
	TestBuilding,
	TestCity,
	TestCivs,
	TestCorporation,
	TestCount,
	TestCultureLevel,
	TestEra,
	TestFeature,
	TestImprovement,
	TestPercentage,
	TestProject,
	TestReligion,
	TestReligionAdjective,
	TestResource,
	TestRoutes,
	TestSpecialist,
	TestTerrain,
	TestTech,
	TestTurns,
	TestUnit,
	TestUnitCombat,
]