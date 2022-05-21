from CountRequirements import *

from TestVictoryCommon import *


class TestBuildingCount(ExtendedTestCase):

	def setUp(self):
		self.requirement = BuildingCount(iGranary, 3)
		self.goal = TestGoal()
		
		self.requirement.register_handlers(self.goal)
	
	def tearDown(self):
		self.requirement.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.requirement), "BuildingCount(Granary, 3)")
	
	def test_repr(self):
		self.assertEqual(repr(self.requirement), "BuildingCount(Granary, 3)")
	
	def test_equals(self):
		identical_requirement = BuildingCount(iGranary, 3)
		different_building = BuildingCount(iLibrary, 3)
		different_count = BuildingCount(iGranary, 4)
		
		self.assertEqual(self.requirement, identical_requirement)
		self.assertNotEqual(self.requirement, different_building)
		self.assertNotEqual(self.requirement, different_count)
	
	def test_pickle(self):
		self.assertPickleable(self.requirement)

	def test_description(self):
		self.assertEqual(self.requirement.description(), "three Granaries")

	def test_none(self):
		self.assertEqual(self.requirement.evaluate(self.evaluator), 0)
		self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
		self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Granaries: 0 / 3")

	def test_some(self):
		cities = TestCities.num(2)
	
		for city in cities:
			city.setHasRealBuilding(iGranary, True)

		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), False)
			self.assertEqual(self.requirement.progress(self.evaluator), self.FAILURE + "Granaries: 2 / 3")
		finally:
			cities.kill()
	
	def test_all(self):
		cities = TestCities.num(3)
		
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Granaries: 3 / 3")
		finally:
			cities.kill()
	
	def test_more(self):
		cities = TestCities.num(4)
		
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(self.evaluator), 4)
			self.assertEqual(self.requirement.fulfilled(self.evaluator), True)
			self.assertEqual(self.requirement.progress(self.evaluator), self.SUCCESS + "Granaries: 4 / 3")
		finally:
			cities.kill()
	
	def test_sum(self):
		requirement = BuildingCount(SumAggregate(iGranary, iLibrary), 3)
		
		city1, city2 = cities = TestCities.num(2)
		
		city1.setHasRealBuilding(iGranary, True)
		city1.setHasRealBuilding(iLibrary, True)
		city2.setHasRealBuilding(iLibrary, True)
		
		try:
			self.assertEqual(requirement.evaluate(self.evaluator), 3)
			self.assertEqual(requirement.fulfilled(self.evaluator), True)
			self.assertEqual(requirement.progress(self.evaluator), self.SUCCESS + "Granaries and Libraries: 3 / 3")
		finally:
			cities.kill()
	
	def test_average(self):
		requirement = BuildingCount(AverageAggregate(iGranary, iLibrary), 2)
		
		cities = TestCities.num(2)
		
		for city in cities:
			city.setHasRealBuilding(iLibrary, True)
		
		try:
			self.assertEqual(requirement.evaluate(self.evaluator), 1)
			self.assertEqual(requirement.fulfilled(self.evaluator), False)
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Granaries and Libraries: 1 / 2")
		finally:
			cities.kill()
	
	def test_count(self):
		requirement = BuildingCount(CountAggregate(iGranary, iLibrary), 2)
		
		cities = TestCities.num(2)
		
		for city in cities:
			city.setHasRealBuilding(iLibrary, True)
		
		try:
			self.assertEqual(requirement.evaluate(self.evaluator), 1)
			self.assertEqual(requirement.fulfilled(self.evaluator), False)
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Granaries and Libraries: 1 / 2")
		finally:
			cities.kill()
	
	def test_vassals(self):
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		cities = TestCities.owners(0, 1, 2)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), False)
			self.assertEqual(self.requirement.progress(evaluator), self.FAILURE + "Granaries: 2 / 3")
		finally:
			cities.kill()
			
			team(1).setVassal(0, False, False)
	
	def test_allies(self):
		evaluator = AlliesEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		team(2).setDefensivePact(0, True)
		team(0).setDefensivePact(2, True)
		
		cities = TestCities.owners(0, 1, 2, 3)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Granaries: 3 / 3")
		finally:
			cities.kill()
			
			team(1).setVassal(0, False, False)
			team(2).setDefensivePact(0, False)
			team(0).setDefensivePact(2, False)
	
	def test_religion(self):
		evaluator = ReligionEvaluator(self.iPlayer)
		
		player(0).setLastStateReligion(iOrthodoxy)
		player(1).setLastStateReligion(iOrthodoxy)
		player(2).setLastStateReligion(iCatholicism)
		
		cities = TestCities.owners(0, 1, 2, 3)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), False)
			self.assertEqual(self.requirement.progress(evaluator), self.FAILURE + "Granaries: 2 / 3")
		finally:
			cities.kill()
			
			for iPlayer in [0, 1, 2]:
				player(iPlayer).setLastStateReligion(-1)
	
	def test_secular(self):
		evaluator = SecularEvaluator(self.iPlayer)
		
		player(0).setCivics(iCivicsReligion, iSecularism)
		player(1).setCivics(iCivicsReligion, iSecularism)
		
		cities = TestCities.owners(0, 1, 2)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 2)
			self.assertEqual(self.requirement.fulfilled(evaluator), False)
			self.assertEqual(self.requirement.progress(evaluator), self.FAILURE + "Granaries: 2 / 3")
		finally:
			cities.kill()
			
			for iPlayer in [0, 1]:
				player(iPlayer).setCivics(iCivicsReligion, iAnimism)
	
	def test_world(self):
		evaluator = WorldEvaluator(self.iPlayer)
		
		cities = TestCities.owners(0, 1, 2)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.requirement.evaluate(evaluator), 3)
			self.assertEqual(self.requirement.fulfilled(evaluator), True)
			self.assertEqual(self.requirement.progress(evaluator), self.SUCCESS + "Granaries: 3 / 3")
		finally:
			cities.kill()
	
	def test_vassals_sum(self):
		requirement = BuildingCount(SumAggregate(iGranary, iBarracks), 5)
		evaluator = VassalsEvaluator(self.iPlayer)
		
		team(1).setVassal(0, True, False)
		
		our_city1, our_city2, vassal_city, other_city = cities = TestCities.owners(0, 0, 1, 2)
		
		our_city1.setHasRealBuilding(iGranary, True)
		our_city2.setHasRealBuilding(iBarracks, True)
		vassal_city.setHasRealBuilding(iGranary, True)
		vassal_city.setHasRealBuilding(iBarracks, True)
		other_city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(requirement.evaluate(evaluator), 4)
			self.assertEqual(requirement.fulfilled(evaluator), False)
			self.assertEqual(requirement.progress(evaluator), self.FAILURE + "Granaries and Barracks: 4 / 5")
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_unique_building(self):
		requirement = BuildingCount(iMonument, 2)
		
		city = TestCities.one()
		city.setHasRealBuilding(iObelisk, True)
		
		try:
			self.assertEqual(requirement.evaluate(self.evaluator), 1)
			self.assertEqual(requirement.fulfilled(self.evaluator), False)
			self.assertEqual(requirement.progress(self.evaluator), self.FAILURE + "Monuments: 1 / 2")
		finally:	
			city.kill()
	
	def test_check_city_acquired(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("cityAcquired", 1, self.iPlayer, city, True, False)
		
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
			
	def test_check_city_acquired_other(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("cityAcquired", 1, 2, city, True, False)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_check_building_built(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("buildingBuilt", city, iGranary)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_check_building_built_unique_building(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("buildingBuilt", city, iTerrace)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
	
	def test_check_building_built_other_owner(self):
		city = TestCities.one(1)
		
		try:
			events.fireEvent("buildingBuilt", city, iGranary)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_check_building_built_other_building(self):
		city = TestCities.one()
		
		try:
			events.fireEvent("buildingBuilt", city, iLibrary)
			
			self.assertEqual(self.goal.checked, False)
		finally:
			city.kill()
	
	def test_check_building_built_aggregate(self):
		requirement = BuildingCount(SumAggregate(iGranary, iLibrary), 3)
	
		city = TestCities.one()
		
		try:
			requirement.register_handlers(self.goal)
			
			events.fireEvent("buildingBuilt", city, iGranary)
			
			self.assertEqual(self.goal.checked, True)
		finally:
			city.kill()
			requirement.deregister_handlers()
	
	def test_not_check_turnly(self):
		events.fireEvent("BeginPlayerTurn", self.iPlayer, 0)
		
		self.assertEqual(self.goal.checked, False)


test_cases = [
	TestBuildingCount,
]