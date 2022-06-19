from CityRequirements import *

from TestVictoryCommon import *


class TestCityBuilding(ExtendedTestCase):

	def setUp(self):
		self.requirement = CityBuilding(LocationCityDefinition(TestCities.CITY_LOCATIONS[0]).named("Test City"), iGranary)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CityBuilding(Test City, Granary)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CityBuilding(Test City, Granary)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "a Granary in Test City")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test City": plots_.of([TestCities.CITY_LOCATIONS[0]])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((61, 31)), "Test City")
		self.assertEqual(self.requirement.area_name((62, 32)), "")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_no_city(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "No city")
	
	def test_city_no_building(self):
		city = TestCities.one()
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Granary in %s" % city.getName())
		finally:
			city.kill()
	
	def test_city_building(self):
		city = TestCities.one()
		city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Granary in %s" % city.getName())
		finally:
			city.kill()
	
	def test_city_building_different_owner(self):
		city = TestCities.one(1)
		city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Granary in %s (controlled by Babylonia)" % city.getName())
		finally:
			city.kill()
	
	def test_city_building_different_location(self):
		other_city, city = cities = TestCities.num(2)
		
		city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Granary in %s" % other_city.getName())
		finally:
			cities.kill()
	
	def test_city_unique_building(self):
		requirement = CityBuilding(LocationCityDefinition(TestCities.CITY_LOCATIONS[0]).named("Test City"), iMonument)
		
		city = TestCities.one()
		city.setHasRealBuilding(iObelisk, True)
		
		try:
			self.assertEqual(requirement.fulfilled(self.evaluator), True)
			self.assertEqual(requirement.progress(self.evaluator), self.SUCCESS + "Monument in %s" % city.getName())
		finally:
			city.kill()
	
	def test_different_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
	
		city = TestCities.one(1)
		city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Granary in %s" % city.getName())
		finally:
			city.kill()
	
	def test_check_city_acquired(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("cityAcquired", 1, self.iPlayer, city, True, False)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_check_city_acquired_different_city(self):
		city, other_city = cities = TestCities.num(2)
		
		try:
			events.fireEvent("cityAcquired", 1, self.iPlayer, other_city, True, False)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			cities.kill()
	
	def test_check_building_built(self):
		city = TestCities.one()
	
		try:
			events.fireEvent("buildingBuilt", city, iGranary)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_check_building_built_different_city(self):
		city, other_city = cities = TestCities.num(2)
		
		try:
			events.fireEvent("buildingBuilt", other_city, iGranary)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			cities.kill()
	
	def test_check_building_built_different_building(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("buildingBuilt", city, iLibrary)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_expire_building_built_wonder(self):
		requirement = CityBuilding(LocationCityDefinition(TestCities.CITY_LOCATIONS[0]), iPyramids)
		goal = TestGoal()
		
		requirement.register_handlers(goal)
	
		city = TestCities.one(1)
		
		try:
			self.assertEqual(city.getOwner(), 1)
			events.fireEvent("buildingBuilt", city, iPyramids)
			
			self.assertEqual(goal.failed, True)
		finally:
			city.kill()
			requirement.deregister_handlers()
	
	def test_expire_building_built_different_wonder(self):
		requirement = CityBuilding(LocationCityDefinition(TestCities.CITY_LOCATIONS[0]), iPyramids)
		
		city = TestCities.one(1)
		
		try:
			events.fireEvent("buildingBuilt", city, iHangingGardens)
			
			self.assertEqual(self.goal.failed, False)
		finally:
			city.kill()
	
	def test_expire_building_built_not_wonder(self):
		city = TestCities.one(1)
		
		try:
			events.fireEvent("buildingBuilt", city, iGranary)
			
			self.assertEqual(self.goal.failed, False)
		finally:
			city.kill()


class TestCityCultureLevel(ExtendedTestCase):

	def setUp(self):
		self.requirement = CityCultureLevel(LocationCityDefinition(TestCities.CITY_LOCATIONS[0]).named("Test City"), iCultureLevelRefined)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CityCultureLevel(Test City, Refined)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CityCultureLevel(Test City, Refined)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "refined culture in Test City")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test City": plots_.of([(61, 31)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((61, 31)), "Test City")
		self.assertEqual(self.requirement.area_name((42, 42)), "")
	
	def test_no_city(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "No city")
	
	def test_less(self):
		city = TestCities.one()
		city.setCulture(0, 500, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Culture in %s: 500 / 1000" % city.getName())
		finally:
			city.kill()
	
	def test_more(self):
		city = TestCities.one()
		city.setCulture(0, 2000, False)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Culture in %s: 2000 / 1000" % city.getName())
		finally:
			city.kill()
	
	def test_different_owner(self):
		city = TestCities.one(1)
		
		city.plot().resetCultureConversion()
		city.setCulture(1, 1000, False)
		city.plot().resetCultureConversion()
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Culture in %s (controlled by Babylonia): 1000 / 1000" % city.getName())
		finally:
			city.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		city = TestCities.one(1)
		city.plot().resetCultureConversion()
		
		city.setCulture(1, 1000, False)
		city.plot().resetCultureConversion()
		
		try:
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Culture in %s: 1000 / 1000" % city.getName())
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
		finally:
			team(1).setVassal(0, False, False)
			city.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestCityDifferentGreatPeopleCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = CityDifferentGreatPeopleCount(LocationCityDefinition(TestCities.CITY_LOCATIONS[0]).named("Test City"), 2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CityDifferentGreatPeopleCount(Test City, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CityDifferentGreatPeopleCount(Test City, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two different great people in Test City")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test City": plots_.of([(61, 31)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((61, 31)), "Test City")
		self.assertEqual(self.requirement.area_name((42, 42)), "")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_none(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "No city")
	
	def test_fewer(self):
		city = TestCities.one()
		
		city.setName("First", False)
		city.setFreeSpecialistCount(iSpecialistGreatArtist, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Different great people in First: 1 / 2")
		finally:
			city.kill()
	
	def test_more(self):
		city = TestCities.one()
		
		city.setName("First", False)
		
		for iSpecialist in [iSpecialistGreatArtist, iSpecialistGreatProphet, iSpecialistGreatScientist]:
			city.setFreeSpecialistCount(iSpecialist, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Different great people in First: 3 / 2")
		finally:
			city.kill()
	
	def test_unique(self):
		city = TestCities.one()
		
		city.setName("First", False)
		city.setFreeSpecialistCount(iSpecialistGreatArtist, 2)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Different great people in First: 1 / 2")
		finally:
			city.kill()
	
	def test_great_people(self):
		city = TestCities.one()
		
		city.setName("First", False)
		
		for iSpecialist in [iSpecialistArtist, iSpecialistPriest, iSpecialistScientist]:
			city.setFreeSpecialistCount(iSpecialist, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Different great people in First: 0 / 2")
		finally:
			city.kill()
	
	def test_different_owner(self):
		city = TestCities.one(1)
		
		city.setName("First", False)
		
		for iSpecialist in [iSpecialistGreatArtist, iSpecialistGreatProphet]:
			city.setFreeSpecialistCount(iSpecialist, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Different great people in First (controlled by Babylonia): 2 / 2")
		finally:
			city.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		team(1).setVassal(0, True, False)
		
		city = TestCities.one(1)
		
		city.setName("First", False)
		
		for iSpecialist in [iSpecialistGreatArtist, iSpecialistGreatProphet]:
			city.setFreeSpecialistCount(iSpecialist, 1)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Different great people in First: 2 / 2")
		finally:
			city.kill()
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestCitySpecialistCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = CitySpecialistCount(LocationCityDefinition(TestCities.CITY_LOCATIONS[0]).named("Test City"), iSpecialistGreatArtist, 2)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CitySpecialistCount(Test City, Great Artist, 2)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CitySpecialistCount(Test City, Great Artist, 2)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "two Great Artists in Test City")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test City": plots_.of([(61, 31)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((61, 31)), "Test City")
		self.assertEqual(self.requirement.area_name((42, 42)), "")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_no_city(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "No city")
	
	def test_no_specialists(self):
		city = TestCities.one()
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Great Artists in %s: 0 / 2" % city.getName())
		finally:
			city.kill()
	
	def test_specialists(self):
		city = TestCities.one()
		city.setFreeSpecialistCount(iSpecialistGreatArtist, 2)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Great Artists in %s: 2 / 2" % city.getName())
		finally:
			city.kill()
	
	def test_different_owner(self):
		city = TestCities.one(1)
		city.setFreeSpecialistCount(iSpecialistGreatArtist, 2)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Great Artists in %s (controlled by Babylonia): 2 / 2" % city.getName())
		finally:
			city.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		city = TestCities.one(1)
		city.setFreeSpecialistCount(iSpecialistGreatArtist, 2)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Great Artists in %s: 2 / 2" % city.getName())
		finally:
			city.kill()
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)

test_cases = [
	TestCityBuilding,
	TestCityCultureLevel,
	TestCityDifferentGreatPeopleCount,
	TestCitySpecialistCount,
]