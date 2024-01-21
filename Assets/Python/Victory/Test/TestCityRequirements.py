from CityRequirements import *

from TestVictoryCommon import *


class TestCityCultureLevel(ExtendedTestCase):

	def setUp(self):
		self.requirement = CityCultureLevel(LocationCityArgument(TestCities.CITY_LOCATIONS[0]).named("Test City"), iCultureLevelRefined).create()
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
		self.assertEqual(self.requirement.areas(), {"Test City": plots.of([(57, 35)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((57, 35)), "Test City")
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
		self.requirement = CityDifferentGreatPeopleCount(LocationCityArgument(TestCities.CITY_LOCATIONS[0]).named("Test City"), 2).create()
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
		self.assertEqual(self.requirement.areas(), {"Test City": plots.of([(57, 35)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((57, 35)), "Test City")
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


class TestCityPopulation(ExtendedTestCase):

	def setUp(self):
		self.requirement = CityPopulation(LocationCityArgument(TestCities.CITY_LOCATIONS[0]).named("Test City"), 5).create()
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "CityPopulation(Test City, 5)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "CityPopulation(Test City, 5)")
	
	def test_description(self):
		self.assertEqual(self.requirement.description(), "a population of 5 in Test City")
	
	def test_areas(self):
		self.assertEqual(self.requirement.areas(), {"Test City": plots.of([(57, 35)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((57, 35)), "Test City")
		self.assertEqual(self.requirement.area_name((42, 42)), "")
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)
	
	def test_no_city(self):
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "No city")
	
	def test_less(self):
		city = TestCities.one()
		city.setPopulation(4)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Population in %s: 4 / 5" % city.getName())
		finally:
			city.kill()
	
	def test_more(self):
		city = TestCities.one()
		city.setPopulation(6)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Population in %s: 6 / 5" % city.getName())
		finally:
			city.kill()
	
	def test_different_owner(self):
		city = TestCities.one(1)
		city.setPopulation(6)
		
		try:
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Population in %s (controlled by Babylonia): 6 / 5" % city.getName())
		finally:
			city.kill()
	
	def test_other_evaluator(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		city = TestCities.one(1)
		city.setPopulation(6)
		
		try:
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Population in %s: 6 / 5" % city.getName())
		finally:
			city.kill()
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)


class TestCitySpecialistCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = CitySpecialistCount(LocationCityArgument(TestCities.CITY_LOCATIONS[0]).named("Test City"), iSpecialistGreatArtist, 2).create()
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
		self.assertEqual(self.requirement.areas(), {"Test City": plots.of([(57, 35)])})
	
	def test_area_name(self):
		self.assertEqual(self.requirement.area_name((57, 35)), "Test City")
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
			team(1).setVassal(0, False, False)
	
	def test_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
		
		self.assertEqual(self.goal.checked, True)

test_cases = [
	TestCityCultureLevel,
	TestCityDifferentGreatPeopleCount,
	TestCityPopulation,
	TestCitySpecialistCount,
]