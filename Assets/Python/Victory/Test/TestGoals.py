from VictoryGoalDefinitions import *

from TestVictoryCommon import *


class TestParameters(ExtendedTestCase):

	def test(self):
		parameters = Parameters((1, 2), (3, 4))
		
		self.assertEqual(list(parameters), [1, 2, 3, 4])
	
	def test_only_globals(self):
		parameters = Parameters((1, 2, 3), tuple())
		
		self.assertEqual(list(parameters), [1, 2, 3])
	
	def test_only_locals(self):
		parameters = Parameters(tuple(), (1, 2, 3))
		
		self.assertEqual(list(parameters), [1, 2, 3])
	
	def test_str(self):
		parameters = Parameters((1, 2), (3, 4))
		
		self.assertEqual(str(parameters), "Parameters(1, 2, 3, 4)")
	
	def test_repr(self):
		parameters = Parameters((1, 2), (3, 4))
		
		self.assertEqual(repr(parameters), "Parameters(1, 2, 3, 4)")
	
	def test_equal(self):
		parameters = Parameters((1, 2), (3, 4))
		
		identical = Parameters((1, 2), (3, 4))
		different_globals = Parameters((1, 2, 3), (3, 4))
		different_locals = Parameters((1, 2), (3, 4, 5))
		same_combination = Parameters((1,), (2, 3, 4))
		
		self.assertEqual(parameters, identical)
		self.assertNotEqual(parameters, different_globals)
		self.assertNotEqual(parameters, different_locals)
		self.assertEqual(parameters, same_combination)
	
	def test_pickle(self):
		self.assertPickleable(Parameters((1, 2), (3, 4)))


class TestParameterSet(ExtendedTestCase):

	def test_single_local(self):
		parameter_set = ParameterSet(tuple(), (BUILDING, COUNT), ((iGranary, 3),))
		
		self.assertEqual(list(parameter_set), [Parameters((), (iGranary, 3))])
	
	def test_single_local_flat(self):
		parameter_set = ParameterSet(tuple(), (BUILDING, COUNT), (iGranary, 3))
		
		self.assertEqual(list(parameter_set), [Parameters((), (iGranary, 3))])
	
	def test_multiple_local(self):
		parameter_set = ParameterSet(tuple(), (BUILDING, COUNT), ((iGranary, 3), (iLibrary, 4)))
		
		self.assertEqual(list(parameter_set), [Parameters((), (iGranary, 3)), Parameters((), (iLibrary, 4))])
	
	def test_global_single_local(self):
		parameter_set = ParameterSet((BUILDING,), (BUILDING, COUNT), (iPalace, (iGranary, 3)))
		
		self.assertEqual(list(parameter_set), [Parameters((iPalace,), (iGranary, 3))])
	
	def test_global_single_local_flat(self):
		parameter_set = ParameterSet((BUILDING,), (BUILDING, COUNT), (iPalace, iGranary, 3))
		
		self.assertEqual(list(parameter_set), [Parameters((iPalace,), (iGranary, 3))])
	
	def test_global_multiple_local(self):
		parameter_set = ParameterSet((BUILDING,), (BUILDING, COUNT), (iPalace, (iGranary, 3), (iLibrary, 4)))
		
		self.assertEqual(list(parameter_set), [Parameters((iPalace,), (iGranary, 3)), Parameters((iPalace,), (iLibrary, 4))])
	
	def test_invalid_global_type(self):
		self.assertRaises(ValueError, ParameterSet, (BUILDING,), (BUILDING, COUNT), ("Palace", (iGranary, 3)))
	
	def test_invalid_local_type(self):
		self.assertRaises(ValueError, ParameterSet, tuple(), (BUILDING, COUNT), ((iGranary, "3"),))
	
	def test_invalid_local_type_flat(self):
		self.assertRaises(ValueError, ParameterSet, tuple(), (BUILDING, COUNT), (iGranary, "3"))
	
	def test_invalid_second_local_type(self):
		self.assertRaises(ValueError, ParameterSet, tuple(), (BUILDING, COUNT), ((iGranary, 3), (iLibrary, "4")))
	
	def test_more_global_arguments(self):
		self.assertRaises(ValueError, ParameterSet, (BUILDING,), (BUILDING, COUNT), (iPalace, iWalls, (iGranary, 3)))
	
	def test_fewer_global_arguments(self):
		self.assertRaises(ValueError, ParameterSet, (BUILDING,), (BUILDING, COUNT), ((iGranary, 3),))
	
	def test_more_local_arguments(self):
		self.assertRaises(ValueError, ParameterSet, tuple(), (BUILDING, COUNT), ((iGranary, 3, 4),))
	
	def test_fewer_local_arguments(self):
		self.assertRaises(ValueError, ParameterSet, tuple(), (BUILDING, COUNT), ((iGranary,),))
	
	def test_more_local_arguments_flat(self):
		self.assertRaises(ValueError, ParameterSet, tuple(), (BUILDING, COUNT), (iGranary, 3, 4))
	
	def test_fewer_local_arguments_flat(self):
		self.assertRaises(ValueError, ParameterSet, tuple(), (BUILDING, COUNT), (iGranary,))
	
	def test_more_local_arguments_second(self):
		self.assertRaises(ValueError, ParameterSet, tuple(), (BUILDING, COUNT), ((iGranary, 3), (iLibrary, 4, 5)))
	
	def test_fewer_local_arguments_second(self):
		self.assertRaises(ValueError, ParameterSet, tuple(), (BUILDING, COUNT), ((iGranary, 3), (iLibrary,)))
		
	def test_str(self):
		parameter_set = ParameterSet(tuple(), (BUILDING, COUNT), ((iGranary, 3), (iLibrary, 4)))
		
		self.assertEqual(str(parameter_set), "ParameterSet((), (Building, Count), [Parameters(3, 3), Parameters(18, 4)])")
	
	def test_repr(self):
		parameter_set = ParameterSet(tuple(), (BUILDING, COUNT), ((iGranary, 3), (iLibrary, 4)))
	
		self.assertEqual(repr(parameter_set), "ParameterSet((), (Building, Count), [Parameters(3, 3), Parameters(18, 4)])")
	
	def test_equal(self):
		parameter_set = ParameterSet(tuple(), (BUILDING, COUNT), ((iGranary, 3), (iLibrary, 4)))
		
		identical = ParameterSet(tuple(), (BUILDING, COUNT), ((iGranary, 3), (iLibrary, 4)))
		different_global_types = ParameterSet((BUILDING,), (BUILDING, COUNT), (iPalace, (iGranary, 3), (iLibrary, 4)))
		different_local_types = ParameterSet(tuple(), (BUILDING,), ((iGranary,), (iLibrary,)))
		different_parameters = ParameterSet(tuple(), (BUILDING, COUNT), ((iGranary, 4), (iLibrary, 4)))
		
		self.assertEqual(parameter_set, identical)
		self.assertNotEqual(parameter_set, different_global_types)
		self.assertNotEqual(parameter_set, different_local_types)
		self.assertNotEqual(parameter_set, different_parameters)
	
	def test_pickle(self):
		self.assertPickleable(ParameterSet((BUILDING,), (BUILDING, COUNT), (iPalace, (iGranary, 3), (iLibrary, 4))))
		
		
class TestGoalDefinition(ExtendedTestCase):

	def setUp(self):
		self.goal_definition = GoalDefinition(BuildingCount)

	def test_str(self):
		self.assertEqual(str(self.goal_definition), "GoalDefinition(BuildingCount, ())")
		
	def test_repr(self):
		self.assertEqual(repr(self.goal_definition), "GoalDefinition(BuildingCount, ())")
		
	def test_equal(self):
		identical = GoalDefinition(BuildingCount)
		different_requirement = GoalDefinition(Control)
		
		self.assertEqual(self.goal_definition, identical)
		self.assertNotEqual(self.goal_definition, different_requirement)
	
	def test_pickle(self):
		self.assertPickleable(self.goal_definition)
	
	def test_create(self):
		goal_description = self.goal_definition(iGranary, 3)
		
		self.assertEqual(goal_description, GoalDescription([BuildingCount(iGranary, 3)], BuildingCount.DESC_KEY))
	
	def test_create_multiple(self):
		goal_description = self.goal_definition((iGranary, 3), (iLibrary, 4))
		
		self.assertEqual(goal_description, GoalDescription([BuildingCount(iGranary, 3), BuildingCount(iLibrary, 4)], BuildingCount.DESC_KEY))
		
	def test_create_fewer_arguments(self):
		self.assertRaises(ValueError, self.goal_definition, iGranary)
	
	def test_create_more_arguments(self):
		self.assertRaises(ValueError, self.goal_definition, iGranary, 3, 4)
	
	def test_create_invalid_type(self):
		self.assertRaises(ValueError, self.goal_definition, "Granary", 3)
	
	def test_create_options(self):
		goal_description = self.goal_definition(iGranary, 3, at=1000, some_option=42, another_option="hello")
		
		self.assertEqual(goal_description, GoalDescription([BuildingCount(iGranary, 3)], BuildingCount.DESC_KEY, at=1000, some_option=42, another_option="hello"))


class TestGoalDescription(ExtendedTestCase):

	def setUp(self):
		self.single_goal_description = GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL")
		self.double_goal_description = GoalDescription([BuildingCount(iGranary, 3), BuildingCount(iLibrary, 4)], "TXT_KEY_VICTORY_DESC_CONTROL")
		self.triple_goal_description = GoalDescription([BuildingCount(iGranary, 3), BuildingCount(iLibrary, 4), BuildingCount(iWalls, 5)], "TXT_KEY_VICTORY_DESC_CONTROL")
	
	def test_str(self):
		self.assertEqual(str(self.single_goal_description), "GoalDescription(BuildingCount(Granary, 3))")
		self.assertEqual(str(self.double_goal_description), "GoalDescription(BuildingCount(Granary, 3), BuildingCount(Library, 4))")
		self.assertEqual(str(self.triple_goal_description), "GoalDescription(BuildingCount(Granary, 3), BuildingCount(Library, 4), BuildingCount(Walls, 5))")
	
	def test_repr(self):
		self.assertEqual(repr(self.single_goal_description), "GoalDescription(BuildingCount(Granary, 3))")
		self.assertEqual(repr(self.double_goal_description), "GoalDescription(BuildingCount(Granary, 3), BuildingCount(Library, 4))")
		self.assertEqual(repr(self.triple_goal_description), "GoalDescription(BuildingCount(Granary, 3), BuildingCount(Library, 4), BuildingCount(Walls, 5))")
	
	def test_equals(self):
		identical_description = GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL")
		different_requirement = GoalDescription([BuildingCount(iLibrary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL")
		different_num_requirements = GoalDescription([BuildingCount(iGranary, 3), BuildingCount(iLibrary, 4)], "TXT_KEY_VICTORY_DESC_CONTROL")
		different_desc_key = GoalDescription([BuildingCount(iGranary, 3)], "SOME_OTHER_TXT_KEY")
		different_options = GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", some_option="some_value")
		
		self.assertEqual(self.single_goal_description, identical_description)
		self.assertNotEqual(self.single_goal_description, different_requirement)
		self.assertNotEqual(self.single_goal_description, different_num_requirements)
		self.assertNotEqual(self.single_goal_description, different_desc_key)
		self.assertNotEqual(self.single_goal_description, different_options)
	
	def test_description(self):
		self.assertEqual(self.single_goal_description.description(), "Control three Granaries")
		self.assertEqual(self.double_goal_description.description(), "Control three Granaries and four Libraries")
		self.assertEqual(self.triple_goal_description.description(), "Control three Granaries, four Libraries and five Walls")
	
	def test_description_options(self):
		goal_description = GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", at=1000)
		
		self.assertEqual(goal_description.description(), "Control three Granaries in 1000 AD")
	
	def test_pickle(self):
		self.assertPickleable(self.single_goal_description)
	
	def test_options(self):
		goal = GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", at=1000, some_option=42, another_option="hello")
		
		self.assertEqual(goal.options, {"at": 1000, "some_option": 42, "another_option": "hello"})
	
	def test_create(self):
		single_goal = self.single_goal_description(0)
		double_goal = self.double_goal_description(0)
		triple_goal = self.triple_goal_description(0)
		
		self.assertEqual(single_goal, Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0))
		self.assertEqual(double_goal, Goal([BuildingCount(iGranary, 3), BuildingCount(iLibrary, 4)], "TXT_KEY_VICTORY_DESC_CONTROL", 0))
		self.assertEqual(triple_goal, Goal([BuildingCount(iGranary, 3), BuildingCount(iLibrary, 4), BuildingCount(iWalls, 5)], "TXT_KEY_VICTORY_DESC_CONTROL", 0))
	
	def test_create_options(self):
		goal_description = GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", at=1000, some_option=42, another_option="hello")
		goal = goal_description(0)
		
		try:
			self.assertEqual(goal.iYear, 1000)
		finally:
			goal.deregister_handlers()
	
	def test_create_subject(self):
		goal_description = GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", subject=VASSALS)
		goal = goal_description(0)
		
		try:
			self.assertType(goal.evaluator, VassalsEvaluator)
		finally:
			goal.deregister_handlers()


class TestGoal(ExtendedTestCase):

	def setUp(self):
		self.goal = Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0)
		
		self.double_goal = Goal([BuildingCount(iGranary, 3), BuildingCount(iLibrary, 4)], "TXT_KEY_VICTORY_DESC_CONTROL", 0)
		self.triple_goal = Goal([BuildingCount(iGranary, 3), BuildingCount(iLibrary, 4), BuildingCount(iWalls, 5)], "TXT_KEY_VICTORY_DESC_CONTROL", 0)
		
	def tearDown(self):
		self.goal.deregister_handlers()
		self.double_goal.deregister_handlers()
		self.triple_goal.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.goal), "Goal([BuildingCount(Granary, 3)], 0)")
	
	def test_repr(self):
		self.assertEqual(repr(self.goal), "Goal([BuildingCount(Granary, 3)], 0)")
	
	def test_equal(self):
		identical = Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0)
		different_requirement = Goal([BuildingCount(iGranary, 4)], "TXT_KEY_VICTORY_DESC_CONTROL", 0)
		different_num_requirements = Goal([BuildingCount(iGranary, 3), BuildingCount(iLibrary, 4)], "TXT_KEY_VICTORY_DESC_CONTROL", 0)
		different_description = Goal([BuildingCount(iGranary, 3)], "SOME_OTHER_TXT_KEY", 0)
		different_player = Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 1)
		
		self.assertEqual(self.goal, identical)
		self.assertNotEqual(self.goal, different_requirement)
		self.assertNotEqual(self.goal, different_num_requirements)
		self.assertEqual(self.goal, different_description)
		self.assertNotEqual(self.goal, different_player)
	
	def test_pickle(self):
		self.assertPickleable(self.goal)
	
	def test_possible(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		self.assertEqual(self.goal.possible(), True)
	
	def test_success(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.succeed()
		self.assertEqual(self.goal.state, SUCCESS)
		self.assertEqual(self.goal.succeeded(), True)
	
	def test_failure(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.fail()
		self.assertEqual(self.goal.state, FAILURE)
		self.assertEqual(self.goal.failed(), True)
	
	def test_check_not_fulfilled(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		self.assertEqual(self.goal.fulfilled(), False)
		
		self.goal.check()
		self.assertEqual(self.goal.state, POSSIBLE)
	
	def test_check_fulfilled(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		cities = TestCities.num(3)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.goal.fulfilled(), True)
			
			self.goal.check()
			self.assertEqual(self.goal.state, SUCCESS)
		finally:
			cities.kill()
	
	def test_check_not_fulfilled_already_succeeded(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.succeed()
		self.assertEqual(self.goal.state, SUCCESS)
		self.assertEqual(self.goal.fulfilled(), False)
		
		self.goal.check()
		self.assertEqual(self.goal.state, SUCCESS)
	
	def test_check_fulfilled_already_succeeded(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.succeed()
		self.assertEqual(self.goal.state, SUCCESS)
		
		cities = TestCities.num(3)
		for city in cities:
			city.setHasRealBuilding(iGranary, 3)
		
		try:
			self.assertEqual(self.goal.fulfilled(), True)
		
			self.goal.check()
			self.assertEqual(self.goal.state, SUCCESS)
		finally:
			cities.kill()
	
	def test_check_not_fulfilled_already_failed(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.fail()
		self.assertEqual(self.goal.state, FAILURE)
		self.assertEqual(self.goal.fulfilled(), False)
		
		self.goal.check()
		self.assertEqual(self.goal.state, FAILURE)
		
	def test_check_fulfilled_already_failed(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.fail()
		self.assertEqual(self.goal.state, FAILURE)
		
		cities = TestCities.num(3)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.goal.fulfilled(), True)
		
			self.goal.check()
			self.assertEqual(self.goal.state, FAILURE)
		finally:
			cities.kill()
	
	def test_expire(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.expire()
		self.assertEqual(self.goal.state, FAILURE)
	
	def test_expire_already_failed(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.fail()
		self.assertEqual(self.goal.state, FAILURE)
		
		self.goal.expire()
		self.assertEqual(self.goal.state, FAILURE)
	
	def test_expire_already_succeeded(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.succeed()
		self.assertEqual(self.goal.state, SUCCESS)
		
		self.goal.expire()
		self.assertEqual(self.goal.state, SUCCESS)
	
	def test_final_check_not_fulfilled(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		self.assertEqual(self.goal.fulfilled(), False)
		
		self.goal.final_check()
		self.assertEqual(self.goal.state, FAILURE)
	
	def test_final_check_fulfilled(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		cities = TestCities.num(3)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.goal.fulfilled(), True)
		
			self.goal.final_check()
			self.assertEqual(self.goal.state, SUCCESS)
		finally:
			cities.kill()
	
	def test_final_check_not_fulfilled_already_succeeded(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.succeed()
		self.assertEqual(self.goal.state, SUCCESS)
		self.assertEqual(self.goal.fulfilled(), False)
		
		self.goal.final_check()
		self.assertEqual(self.goal.state, SUCCESS)
	
	def test_final_check_fulfilled_already_succeeded(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.succeed()
		self.assertEqual(self.goal.state, SUCCESS)
		
		cities = TestCities.num(3)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.goal.fulfilled(), True)
		
			self.goal.final_check()
			self.assertEqual(self.goal.state, SUCCESS)
		finally:
			cities.kill()
	
	def test_final_check_not_fulfilled_already_failed(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.fail()
		self.assertEqual(self.goal.state, FAILURE)
		self.assertEqual(self.goal.fulfilled(), False)
		
		self.goal.final_check()
		self.assertEqual(self.goal.state, FAILURE)
	
	def test_final_check_fulfilled_already_failed(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.fail()
		self.assertEqual(self.goal.state, FAILURE)
		
		cities = TestCities.num(3)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.goal.fulfilled(), True)
		
			self.goal.final_check()
			self.assertEqual(self.goal.state, FAILURE)
		finally:
			cities.kill()
			
	def test_check_from_event_fulfilled(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		cities = TestCities.num(3)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(self.goal.fulfilled(), True)
		
			events.fireEvent("cityAcquired", 1, self.iPlayer, cities[0], True, False)
			
			self.assertEqual(self.goal.state, SUCCESS)
		finally:
			cities.kill()
	
	def test_check_from_event_not_fulfilled(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		city = TestCities.one()
		
		try:
			self.assertEqual(self.goal.fulfilled(), False)
		
			events.fireEvent("cityAcquired", 1, self.iPlayer, city, True, False)
			
			self.assertEqual(self.goal.state, POSSIBLE)
		finally:
			city.kill()
	
	def test_check_other_evaluator(self):
		goal = Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", self.iPlayer, subject=VASSALS)
		
		self.assertEqual(goal.state, POSSIBLE)
		
		team(1).setVassal(0, True, False)
		
		cities = TestCities.owners(0, 0, 1)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(goal.fulfilled(), True)
		
			goal.check()			
			self.assertEqual(goal.state, SUCCESS)
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)

	def test_description(self):
		self.assertEqual(self.goal.description(), "Control three Granaries")
		self.assertEqual(self.double_goal.description(), "Control three Granaries and four Libraries")
		self.assertEqual(self.triple_goal.description(), "Control three Granaries, four Libraries and five Walls")
	
	def test_override_description(self):
		self.goal.desc("Override description")
		
		self.assertEqual(self.goal.description(), "Override description")
	
	def test_title(self):
		self.goal.titled("Some title")
		
		self.assertEqual(self.goal.title(), "Some title")
	
	def test_no_title(self):
		self.assertEqual(self.goal.title(), "")
	
	def test_full_description(self):
		self.goal.titled("Some title")
		self.goal.desc("Some description")
		
		self.assertEqual(self.goal.full_description(), "Some title: Some description")
	
	def test_full_description_no_title(self):
		self.assertEqual(self.goal.full_description(), "Control three Granaries")
	
	def test_progress_not_fulfilled(self):
		self.assertEqual(self.goal.progress(), [self.FAILURE + "Granaries: 0 / 3"])
		self.assertEqual(self.double_goal.progress(), [self.FAILURE + "Granaries: 0 / 3 " + self.FAILURE + "Libraries: 0 / 4"])
		self.assertEqual(self.triple_goal.progress(), [self.FAILURE + "Granaries: 0 / 3 " + self.FAILURE + "Libraries: 0 / 4 " + self.FAILURE + "Walls: 0 / 5"])
	
	def test_progress_fulfilled(self):
		cities = TestCities.num(3)
		for city in cities:
			for iBuilding in [iGranary, iLibrary, iWalls]:
				city.setHasRealBuilding(iBuilding, True)
		
		try:
			self.assertEqual(self.goal.progress(), [self.SUCCESS + "Granaries: 3 / 3"])
			self.assertEqual(self.double_goal.progress(), [self.SUCCESS + "Granaries: 3 / 3 " + self.FAILURE + "Libraries: 3 / 4"])
			self.assertEqual(self.triple_goal.progress(), [self.SUCCESS + "Granaries: 3 / 3 " + self.FAILURE + "Libraries: 3 / 4 " + self.FAILURE + "Walls: 3 / 5"])
		finally:
			cities.kill()
	
	def test_progress_other_evaluator(self):
		goal = Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", self.iPlayer, subject=VASSALS)
		
		team(1).setVassal(0, True, False)
		
		cities = TestCities.owners(0, 0, 1)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(goal.progress(), [self.SUCCESS + "Granaries: 3 / 3"])
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
			goal.deregister_handlers()
	
	def test_progress_multiline_requirement(self):
		goal = Goal([BestPopulationCities(3)], BestPopulationCities.GOAL_DESC_KEY, self.iPlayer)
		
		city0, city1, city2 = cities = TestCities.owners(0, 1, 2)
		
		city0.setName("First", False)
		city0.setPopulation(10)
		
		city1.setName("Second", False)
		city1.setPopulation(8)
		
		city2.setName("Third", False)
		city2.setPopulation(5)
		
		try:
			self.assertEqual(goal.progress(), [self.SUCCESS + "Most populous: First (10)", self.FAILURE + "Second most populous: Second (8)", self.FAILURE + "Third most populous: Third (5)"])
		finally:
			cities.kill()
			goal.deregister_handlers()
	
	def test_desc_suffixes(self):
		self.goal.desc_suffixes.append(("and something else",))
		
		self.assertEqual(self.goal.description(), "Control three Granaries and something else")
	
	def test_by_attributes(self):
		goal = Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, by=1000)
		
		try:
			self.assertEqual(goal.iYear, 1000)
			self.assertEqual(goal.desc_suffixes, [("TXT_KEY_VICTORY_BY", "1000 AD")])
			self.assertEqual(goal.description(), "Control three Granaries by 1000 AD")
		finally:
			goal.deregister_handlers()
	
	def test_at_attributes(self):
		goal = Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, at=1000)
		
		try:
			self.assertEqual(goal.iYear, 1000)
			self.assertEqual(goal.desc_suffixes, [("TXT_KEY_VICTORY_IN", "1000 AD")])
			self.assertEqual(goal.description(), "Control three Granaries in 1000 AD")
		finally:
			goal.deregister_handlers()
	
	def test_by_handler(self):
		goal = Goal([BuildingCount(iGranary, 1)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, by=-3000)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			
			events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
			self.assertEqual(goal.state, FAILURE)
		finally:
			goal.deregister_handlers()
	
	def test_by_handler_after_success(self):
		goal = Goal([BuildingCount(iGranary, 1)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, by=-3000)
		
		try:
			goal.succeed()
			self.assertEqual(goal.state, SUCCESS)
			
			events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			goal.deregister_handlers()
	
	def test_by_handler_different_turn(self):
		goal = Goal([BuildingCount(iGranary, 1)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, by=-3000)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			
			events.fireEvent("BeginPlayerTurn", 1, self.iPlayer)
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			goal.deregister_handlers()
	
	def test_at_handler_fulfilled(self):
		goal = Goal([BuildingCount(iGranary, 1)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, at=-3000)
		city = TestCities.one()
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			
			city.setHasRealBuilding(iGranary, True)
			self.assertEqual(goal.fulfilled(), True)
			
			events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			city.kill()
			goal.deregister_handlers()
	
	def test_at_handler_not_fulfilled(self):
		goal = Goal([BuildingCount(iGranary, 1)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, at=-3000)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			self.assertEqual(goal.fulfilled(), False)
			
			events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
			self.assertEqual(goal.state, FAILURE)
		finally:
			goal.deregister_handlers()
	
	def test_at_handler_different_turn(self):
		goal = Goal([BuildingCount(iGranary, 1)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, at=-3000)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			self.assertEqual(goal.fulfilled(), False)
			
			events.fireEvent("BeginPlayerTurn", 1, self.iPlayer)
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			goal.deregister_handlers()
	
	def test_every_fulfilled(self):
		goal = Goal([BuildingCount(iGranary, 1)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, every=True)
		city = TestCities.one()
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			
			city.setHasRealBuilding(iGranary, 1)
			self.assertEqual(goal.fulfilled(), True)
			
			events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			city.kill()
			goal.deregister_handlers()
	
	def test_every_not_fulfilled(self):
		goal = Goal([BuildingCount(iGranary, 1)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, every=True)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			self.assertEqual(goal.fulfilled(), False)
			
			events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			goal.deregister_handlers()
	
	def test_every_different_turn(self):
		goal = Goal([BuildingCount(iGranary, 1)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, every=True)
		city = TestCities.one()
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			
			city.setHasRealBuilding(iGranary, True)
			self.assertEqual(goal.fulfilled(), True)
			
			events.fireEvent("BeginPlayerTurn", 1, self.iPlayer)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			city.kill()
			goal.deregister_handlers()
	
	def test_evaluator(self):
		self.assertEqual(self.goal.evaluator, SelfEvaluator(self.iPlayer))
	
	def test_evaluator_from_subject(self):
		goal = Goal([BuildingCount(iGranary, 1)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, subject=WORLD)
		
		try:
			self.assertEqual(goal.evaluator, WorldEvaluator(0))
		finally:
			goal.deregister_handlers()
	
	def test_required_fulfilled(self):
		goal = Goal([BuildingCount(iGranary, 2), BuildingCount(iLibrary, 2)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, required=1)
		
		cities = TestCities.num(2)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(goal.fulfilled(), True)
			self.assertEqual(goal.progress(), [self.SUCCESS + "Granaries: 2 / 2 " + self.FAILURE + "Libraries: 0 / 2"])
		finally:
			cities.kill()
	
	def test_required_not_fulfilled(self):
		goal = Goal([BuildingCount(iGranary, 2), BuildingCount(iLibrary, 2), BuildingCount(iWalls, 2)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, required=2)
		
		cities = TestCities.num(2)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(goal.fulfilled(), False)
			self.assertEqual(goal.progress(), [self.SUCCESS + "Granaries: 2 / 2 " + self.FAILURE + "Libraries: 0 / 2 " + self.FAILURE + "Walls: 0 / 2"])
		finally:
			cities.kill()
	
	def test_succeed_stateless(self):
		goal = Goal([BuildingCount(iGranary, 2)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, mode=STATELESS)
		
		self.assertEqual(goal.state, POSSIBLE)
		
		goal.succeed()
		self.assertEqual(goal.state, POSSIBLE)
	
	def test_succeeded_stateless_not_fulfilled(self):
		goal = Goal([BuildingCount(iGranary, 2)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, mode=STATELESS)
		
		self.assertEqual(goal.state, POSSIBLE)
		self.assertEqual(goal.succeeded(), False)
	
	def test_succeeded_stateless_fulfilled(self):
		goal = Goal([BuildingCount(iGranary, 2)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, mode=STATELESS)
		
		cities = TestCities.num(2)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			self.assertEqual(goal.fulfilled(), True)
			self.assertEqual(goal.succeeded(), True)
		finally:
			cities.kill()


class TestAll(ExtendedTestCase):

	def setUp(self):
		self.all = All(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"), GoalDescription([BuildingCount(iLibrary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"))
	
	def test_str(self):
		self.assertEqual(str(self.all), "All(GoalDescription(BuildingCount(Granary, 3)), GoalDescription(BuildingCount(Library, 3)))")
	
	def test_repr(self):
		self.assertEqual(repr(self.all), "All(GoalDescription(BuildingCount(Granary, 3)), GoalDescription(BuildingCount(Library, 3)))")
	
	def test_equal(self):
		identical = All(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"), GoalDescription([BuildingCount(iLibrary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"))
		different_description = All(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"), GoalDescription([BuildingCount(iWalls, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"))
		different_num_descriptions = All(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"))
		
		self.assertEqual(self.all, identical)
		self.assertNotEqual(self.all, different_description)
		self.assertNotEqual(self.all, different_num_descriptions)
	
	def test_pickle(self):
		self.assertPickleable(self.all)
	
	def test_description(self):
		self.assertEqual(self.all.description(), "Control three Granaries and control three Libraries")
	
	def test_description_option(self):
		all = All(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"), GoalDescription([BuildingCount(iLibrary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"), by=1000)
		
		self.assertEqual(all.description(), "Control three Granaries and control three Libraries by 1000 AD")
	
	def test_description_subgoal_option(self):
		all = All(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", by=1000), GoalDescription([BuildingCount(iLibrary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"))
		
		self.assertEqual(all.description(), "Control three Granaries by 1000 AD and control three Libraries")
	
	def test_create(self):
		all_goal = self.all(0)
		
		self.assertEqual(all_goal, AllGoal([Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0), Goal([BuildingCount(iLibrary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 0))
	
	def test_create_options(self):
		all = All(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"), by=1000)
		all_goal = all(0)
		
		try:
			self.assertEqual(all_goal, AllGoal([Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 0))
			self.assertEqual(all_goal.iYear, 1000)
			self.assertEqual(all_goal.requirements[0].iYear, 1000)
		finally:
			all_goal.deregister_handlers()
	
	def test_create_subgoal_options(self):
		all = All(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", by=1000))
		all_goal = all(0)
		
		try:
			self.assertEqual(all_goal, AllGoal([Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 0))
			self.assertEqual(all_goal.iYear, None)
			self.assertEqual(all_goal.requirements[0].iYear, 1000)
		finally:
			all_goal.deregister_handlers()


class TestAllGoal(ExtendedTestCase):

	def setUp(self):
		self.first_goal = Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0)
		self.second_goal = Goal([BuildingCount(iLibrary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0)
		self.all = AllGoal([self.first_goal, self.second_goal], 0)
	
	def tearDown(self):
		self.all.deregister_handlers()
	
	def test_str(self):
		self.assertEqual(str(self.all), "AllGoal(Goal([BuildingCount(Granary, 3)], 0), Goal([BuildingCount(Library, 3)], 0))")
	
	def test_repr(self):
		self.assertEqual(repr(self.all), "AllGoal(Goal([BuildingCount(Granary, 3)], 0), Goal([BuildingCount(Library, 3)], 0))")
	
	def test_equal(self):
		identical = AllGoal([Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0), Goal([BuildingCount(iLibrary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 0)
		different_goal = AllGoal([Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0), Goal([BuildingCount(iWalls, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 0)
		different_num_goals = AllGoal([Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 0)
		different_player = AllGoal([Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0), Goal([BuildingCount(iLibrary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 1)
		
		self.assertEqual(self.all, identical)
		self.assertNotEqual(self.all, different_goal)
		self.assertNotEqual(self.all, different_num_goals)
		self.assertNotEqual(self.all, different_player)
	
	def test_pickle(self):
		self.assertPickleable(self.first_goal)
		self.assertPickleable(self.second_goal)
		self.assertPickleable(self.all)
	
	def test_fulfilled_no_success(self):
		self.assertEqual(self.all.fulfilled(), False)
	
	def test_fulfilled_one_success(self):
		self.first_goal.succeed()
		
		self.assertEqual(self.all.fulfilled(), False)
	
	def test_fulfilled_all_success(self):
		self.first_goal.succeed()
		self.second_goal.succeed()
		
		self.assertEqual(self.all.fulfilled(), True)
	
	def test_one_success(self):
		self.first_goal.succeed()
		
		self.assertEqual(self.first_goal.state, SUCCESS)
		self.assertEqual(self.second_goal.state, POSSIBLE)
		self.assertEqual(self.all.state, POSSIBLE)
	
	def test_all_success(self):
		self.first_goal.succeed()
		self.second_goal.succeed()
		
		self.assertEqual(self.first_goal.state, SUCCESS)
		self.assertEqual(self.second_goal.state, SUCCESS)
		self.assertEqual(self.all.state, SUCCESS)
	
	def test_one_failure(self):
		self.first_goal.fail()
		
		self.assertEqual(self.first_goal.state, FAILURE)
		self.assertEqual(self.second_goal.state, POSSIBLE)
		self.assertEqual(self.all.state, FAILURE)
	
	def test_all_failure(self):
		self.first_goal.fail()
		self.second_goal.fail()
	
		self.assertEqual(self.first_goal.state, FAILURE)
		self.assertEqual(self.second_goal.state, FAILURE)
		self.assertEqual(self.all.state, FAILURE)
	
	def test_description(self):
		self.assertEqual(self.all.description(), "Control three Granaries and control three Libraries")
	
	def test_description_by(self):
		all = AllGoal([self.first_goal, self.second_goal], 0, by=1000)
		
		self.assertEqual(all.description(), "Control three Granaries and control three Libraries by 1000 AD")
	
	def test_description_at(self):
		all = AllGoal([self.first_goal, self.second_goal], 0, at=1000)
		
		self.assertEqual(all.description(), "Control three Granaries and control three Libraries in 1000 AD")
	
	def test_description_subgoal_by(self):
		first_goal = Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, by=1000)
		all = AllGoal([first_goal, self.second_goal], 0)
		
		self.assertEqual(all.description(), "Control three Granaries by 1000 AD and control three Libraries")
	
	def test_description_subgoal_at(self):
		first_goal = Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0, at=1000)
		all = AllGoal([first_goal, self.second_goal], 0)
		
		self.assertEqual(all.description(), "Control three Granaries in 1000 AD and control three Libraries")
	
	def test_progress(self):
		self.assertEqual(self.all.progress(), [self.FAILURE + "Granaries: 0 / 3", self.FAILURE + "Libraries: 0 / 3"])


test_cases = [
	TestParameters,
	TestParameterSet,
	TestGoalDefinition,
	TestGoalDescription,
	TestGoal,
	TestAll,
	TestAllGoal,
]
