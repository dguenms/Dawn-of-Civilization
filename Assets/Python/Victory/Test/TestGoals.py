from Goals import *

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
		
	def test_multiple_local_single_type(self):
		parameter_set = ParameterSet(tuple(), (BUILDING,), (iGranary, iLibrary))
		
		self.assertEqual(list(parameter_set), [Parameters((), (iGranary,)), Parameters((), (iLibrary,))])
	
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
		
		self.assertEqual(str(parameter_set), "ParameterSet((), (Building, Count), [Parameters(4, 3), Parameters(23, 4)])")
	
	def test_repr(self):
		parameter_set = ParameterSet(tuple(), (BUILDING, COUNT), ((iGranary, 3), (iLibrary, 4)))
	
		self.assertEqual(repr(parameter_set), "ParameterSet((), (Building, Count), [Parameters(4, 3), Parameters(23, 4)])")
	
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
		self.assertEqual(str(self.goal_definition), "GoalDefinition(BuildingCount)")
		
	def test_repr(self):
		self.assertEqual(repr(self.goal_definition), "GoalDefinition(BuildingCount)")
		
	def test_equal(self):
		identical = GoalDefinition(BuildingCount)
		different_requirement = GoalDefinition(Control)
		
		self.assertEqual(self.goal_definition, identical)
		self.assertNotEqual(self.goal_definition, different_requirement)
	
	def test_pickle(self):
		self.assertPickleable(self.goal_definition)
	
	def test_create(self):
		goal_description = self.goal_definition(iGranary, 3)
		
		self.assertEqual(goal_description, GoalDescription([BuildingCount(iGranary, 3)], BuildingCount.GOAL_DESC_KEY))
	
	def test_create_multiple(self):
		goal_description = self.goal_definition((iGranary, 3), (iLibrary, 4))
		
		self.assertEqual(goal_description, GoalDescription([BuildingCount(iGranary, 3), BuildingCount(iLibrary, 4)], BuildingCount.GOAL_DESC_KEY))
		
	def test_create_fewer_arguments(self):
		self.assertRaises(ValueError, self.goal_definition, iGranary)
	
	def test_create_more_arguments(self):
		self.assertRaises(ValueError, self.goal_definition, iGranary, 3, 4)
	
	def test_create_invalid_type(self):
		self.assertRaises(ValueError, self.goal_definition, "Granary", 3)
	
	def test_create_options(self):
		goal_description = self.goal_definition(iGranary, 3, at=1000, some_option=42, another_option="hello")
		
		self.assertEqual(goal_description, GoalDescription([BuildingCount(iGranary, 3)], BuildingCount.GOAL_DESC_KEY, at=1000, some_option=42, another_option="hello"))


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
	
	def test_description_global_arguments(self):
		city = LocationCityArgument(TestCities.CITY_LOCATIONS[0]).named("Test City")
		goal_description = GoalDescription([CityBuildingCount(city, iGranary, 1), CityBuildingCount(city, iPyramids, 1)], "TXT_KEY_VICTORY_DESC_BUILD_IN_CITY")
		
		self.assertEqual(goal_description.description(), "Build a Granary and the Pyramids in Test City")
	
	def test_description_required(self):
		goal_description = GoalDescription([
			Control(AreaArgumentFactory().of([TestCities.CITY_LOCATIONS[0]]).named("First Area")), 
			Control(AreaArgumentFactory().of([TestCities.CITY_LOCATIONS[1]]).named("Second Area")),
			Control(AreaArgumentFactory().of([TestCities.CITY_LOCATIONS[2]]).named("Third Area")),
		], "TXT_KEY_VICTORY_DESC_CONTROL", required=2)
		
		self.assertEqual(goal_description.description(), "Control two out of First Area, Second Area and Third Area")
	
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
		
		self.assertEqual(goal.iYear, 1000)
	
	def test_create_option_args(self):
		goal_description = GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", at=1000, mode=STATELESS, required=1)
		goal = goal_description(0, required=2, some_option=42)
		
		self.assertEqual(goal.iYear, 1000)
		self.assertEqual(goal.mode, STATELESS)
		self.assertEqual(goal.required, 2)
	
	def test_create_subject(self):
		goal_description = GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", subject=VASSALS)
		goal = goal_description(0)
		
		self.assertType(goal.evaluator, VassalsEvaluator)
	
	def test_create_recreates_requirements(self):
		requirement = Control(AreaArgumentFactory().of([(0, 0)]))
		goal_description = GoalDescription([requirement], "TXT_KEY_VICTORY_DESC_CONTROL")
		
		goal = goal_description(0)
		
		self.assertEqual(goal_description.requirements[0] is goal.requirements[0], False)
		self.assertType(goal_description.requirements[0].parameters[0], AreaArgument)
		self.assertType(goal.requirements[0].parameters[0], Plots)
	

class TestGoal(ExtendedTestCase):

	def setUp(self):
		self.goal = Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)
		
		self.double_goal = Goal([BuildingCount(iGranary, 3).create(), BuildingCount(iLibrary, 4).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)
		self.triple_goal = Goal([BuildingCount(iGranary, 3).create(), BuildingCount(iLibrary, 4).create(), BuildingCount(iWalls, 5).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)
		
		team(0).setHasTech(iCalendar, True, 0, False, False)
		
		self.iFinishDateSetting = AdvisorOpt.getUHVFinishDate()
		AdvisorOpt.setUHVFinishDate(0)
		
		self.bProgressAfterFinishSetting = AdvisorOpt.isUHVProgressAfterFinish()
		AdvisorOpt.setUHVProgressAfterFinish(False)
		
	def tearDown(self):
		team(0).setHasTech(iCalendar, False, 0, False, False)
		
		AdvisorOpt.setUHVFinishDate(self.iFinishDateSetting)
		AdvisorOpt.setUHVProgressAfterFinish(self.bProgressAfterFinishSetting)
	
	def test_str(self):
		self.assertEqual(str(self.goal), "Goal([BuildingCount(Granary, 3)], 0)")
	
	def test_repr(self):
		self.assertEqual(repr(self.goal), "Goal([BuildingCount(Granary, 3)], 0)")
	
	def test_equal(self):
		identical = Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)
		different_requirement = Goal([BuildingCount(iGranary, 4).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)
		different_num_requirements = Goal([BuildingCount(iGranary, 3).create(), BuildingCount(iLibrary, 4).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)
		different_description = Goal([BuildingCount(iGranary, 3).create()], "SOME_OTHER_TXT_KEY", 0)
		different_player = Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 1)
		
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
		self.assertEqual(self.goal.iSuccessTurn, 0)
	
	def test_failure(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.fail()
		self.assertEqual(self.goal.state, FAILURE)
		self.assertEqual(self.goal.failed(), True)
		self.assertEqual(self.goal.iSuccessTurn, None)
	
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
	
	def test_check_at(self):
		goal = Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, at=-3000)
		
		cities = TestCities.num(3)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(goal.fulfilled(), True)
			
			goal.check()
			self.assertEqual(goal.state, SUCCESS)
		finally:
			cities.kill()
	
	def test_check_at_different_turn(self):
		goal = Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, at=-2000)
		
		cities = TestCities.num(3)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(goal.fulfilled(), True)
			
			goal.check()
			self.assertEqual(goal.state, POSSIBLE)
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
		self.goal.enable()
	
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
			self.goal.disable()
	
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
		goal = Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", self.iPlayer, subject=VASSALS)
		
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
	
	def test_description_global_arguments(self):
		city = LocationCityArgument(TestCities.CITY_LOCATIONS[0]).named("Test City")
		goal = Goal([CityBuildingCount(city, iGranary, 1).create(), CityBuildingCount(city, iPyramids, 1).create()], "TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", 0)
		
		self.assertEqual(goal.description(), "Build a Granary and the Pyramids in Test City")
	
	def test_description_required(self):
		goal = Goal([
			Control(AreaArgumentFactory().of([TestCities.CITY_LOCATIONS[0]]).named("First Area")).create(), 
			Control(AreaArgumentFactory().of([TestCities.CITY_LOCATIONS[1]]).named("Second Area")).create(),
			Control(AreaArgumentFactory().of([TestCities.CITY_LOCATIONS[2]]).named("Third Area")).create(),
		], "TXT_KEY_VICTORY_DESC_CONTROL", 0, required=2)
		
		self.assertEqual(goal.description(), "Control two out of First Area, Second Area and Third Area")
	
	def test_title(self):
		goal = Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, title_key="Some title")
		
		self.assertEqual(goal.title(), "Some title")
	
	def test_no_title(self):
		self.assertEqual(self.goal.title(), "")
	
	def test_full_description(self):
		goal = Goal([BuildingCount(iGranary, 3).create()], "Some description", 0, title_key="TXT_KEY_VICTORY_TITLE_CATH1")
		
		self.assertEqual(goal.full_description(), "Holy See: Some description")
	
	def test_full_description_undefined(self):
		goal = Goal([BuildingCount(iGranary, 3).create()], "Some description", 0, title_key="UNDEFINED_TXT_KEY")
		
		self.assertEqual(goal.full_description(), "Some description")
	
	def test_full_description_no_title(self):
		self.assertEqual(self.goal.full_description(), "Control three Granaries")
	
	def test_areas_empty(self):
		self.assertEqual(self.goal.areas(), {})
	
	def test_area_name_empty(self):
		self.assertEqual(self.goal.area_name((10, 10)), "")
	
	def test_areas(self):
		goal = Goal([Control(AreaArgumentFactory().rectangle((20, 20), (30, 30)).named("First Area")).create(), Control(AreaArgumentFactory().rectangle((20, 20), (40, 40)).named("Second Area")).create()], "TXT_KEY_VICTORY_DESC_CONTROL", self.iPlayer)
		
		self.assertEqual(goal.areas(), {"First Area": plots.rectangle((20, 20), (30, 30)), "Second Area": plots.rectangle((20, 20), (40, 40))})
		self.assertEqual(goal.area_name((25, 25)), "Second Area\nFirst Area")
		self.assertEqual(goal.area_name((35, 35)), "Second Area")
		self.assertEqual(goal.area_name((45, 45)), "")
	
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
		goal = Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", self.iPlayer, subject=VASSALS)
		
		team(1).setVassal(0, True, False)
		
		cities = TestCities.owners(0, 0, 1)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(goal.progress(), [self.SUCCESS + "Granaries: 3 / 3"])
		finally:
			cities.kill()
			team(1).setVassal(0, False, False)
	
	def test_progress_multiline_requirement(self):
		goal = Goal([BestPopulationCities(3).create()], BestPopulationCities.GOAL_DESC_KEY, self.iPlayer)
		
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
	
	def test_success_string(self):
		self.assertEqual(self.goal.success_string(), self.SUCCESS + "Goal accomplished!")
	
	def test_success_string_success_turn_disabled(self):
		self.goal.iSuccessTurn = 0
		
		self.assertEqual(self.goal.success_string(), self.SUCCESS + "Goal accomplished!")
	
	def test_success_string_success_turn_date(self):
		self.goal.iSuccessTurn = 0
		AdvisorOpt.setUHVFinishDate(1)
		
		self.assertEqual(self.goal.success_string(), self.SUCCESS + "Goal accomplished! (3000 BC)")
	
	def test_success_string_success_turn_date_turn(self):
		self.goal.iSuccessTurn = 0
		AdvisorOpt.setUHVFinishDate(2)
		
		self.assertEqual(self.goal.success_string(), self.SUCCESS + "Goal accomplished! (3000 BC - Turn 0)")
	
	def test_failure_string(self):
		self.assertEqual(self.goal.failure_string(), self.FAILURE + "Goal failed!")
	
	def test_progress_succeeded(self):
		self.goal.set_state(SUCCESS)
		
		self.assertEqual(self.goal.progress(), [self.SUCCESS + "Goal accomplished!"])
	
	def test_progress_succeeded_show_anyway(self):
		AdvisorOpt.setUHVProgressAfterFinish(True)
		self.goal.set_state(SUCCESS)
		
		self.assertEqual(self.goal.progress(), [
			self.SUCCESS + "Goal accomplished!",
			self.FAILURE + "Granaries: 0 / 3",
		])
	
	def test_progress_failed(self):
		self.goal.set_state(FAILURE)
		
		self.assertEqual(self.goal.progress(), [self.FAILURE + "Goal failed!"])
	
	def test_progress_failed_show_anyway(self):
		AdvisorOpt.setUHVProgressAfterFinish(True)
		self.goal.set_state(FAILURE)
		
		self.assertEqual(self.goal.progress(), [
			self.FAILURE + "Goal failed!",
			self.FAILURE + "Granaries: 0 / 3",
		])
	
	def test_by_attributes(self):
		goal = Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, by=1000)
		
		self.assertEqual(goal.iYear, 1000)
		self.assertEqual(goal.date_suffix_keys, {"TXT_KEY_VICTORY_BY": 1000})
		self.assertEqual(list(goal.create_date_suffixes()), ["by 1000 AD"])
		self.assertEqual(goal.description(), "Control three Granaries by 1000 AD")
	
	def test_at_attributes(self):
		goal = Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, at=1000)
		
		self.assertEqual(goal.iYear, 1000)
		self.assertEqual(goal.date_suffix_keys, {"TXT_KEY_VICTORY_IN": 1000})
		self.assertEqual(list(goal.create_date_suffixes()), ["in 1000 AD"])
		self.assertEqual(goal.description(), "Control three Granaries in 1000 AD")
	
	def test_attributes_without_calendar(self):
		team(0).setHasTech(iCalendar, False, 0, False, False)
		goal = Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, at=1000)
		
		self.assertEqual(list(goal.create_date_suffixes()), ["in 1000 AD (Turn 270)"])
		self.assertEqual(goal.description(), "Control three Granaries in 1000 AD (Turn 270)")
	
	def test_attributes_with_game_settings(self):
		AdvisorOpt.setUHVFinishDate(1)
		goal = Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, at=1000)
		
		self.assertEqual(list(goal.create_date_suffixes()), ["in 1000 AD (Turn 270)"])
		self.assertEqual(goal.description(), "Control three Granaries in 1000 AD (Turn 270)")
	
	def test_by_handler(self):
		goal = Goal([BuildingCount(iGranary, 1).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, by=-3000)
		goal.enable()
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			
			events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
			self.assertEqual(goal.state, FAILURE)
		finally:
			goal.disable()
	
	def test_by_handler_after_success(self):
		goal = Goal([BuildingCount(iGranary, 1).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, by=-3000)
		goal.enable()
		
		try:
			goal.succeed()
			self.assertEqual(goal.state, SUCCESS)
			
			events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			goal.disable()
	
	def test_by_handler_different_turn(self):
		goal = Goal([BuildingCount(iGranary, 1).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, by=-3000)
		goal.enable()
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			
			events.fireEvent("BeginPlayerTurn", 1, self.iPlayer)
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			goal.disable()
	
	def test_at_handler_fulfilled(self):
		goal = Goal([BuildingCount(iGranary, 1).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, at=-3000)
		goal.enable()
		
		city = TestCities.one()
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			
			city.setHasRealBuilding(iGranary, True)
			self.assertEqual(goal.fulfilled(), True)
			
			events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			city.kill()
			goal.disable()
	
	def test_at_handler_not_fulfilled(self):
		goal = Goal([BuildingCount(iGranary, 1).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, at=-3000)
		goal.enable()
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			self.assertEqual(goal.fulfilled(), False)
			
			events.fireEvent("BeginPlayerTurn", 0, self.iPlayer)
			self.assertEqual(goal.state, FAILURE)
		finally:
			goal.disable()
	
	def test_at_handler_different_turn(self):
		goal = Goal([BuildingCount(iGranary, 1).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, at=-3000)
		goal.enable()
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			self.assertEqual(goal.fulfilled(), False)
			
			events.fireEvent("BeginPlayerTurn", 1, self.iPlayer)
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			goal.disable()
	
	def test_evaluator(self):
		self.assertEqual(self.goal.evaluator, SelfEvaluator(self.iPlayer))
	
	def test_evaluator_from_subject(self):
		goal = Goal([BuildingCount(iGranary, 1).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, subject=WORLD)
		
		self.assertEqual(goal.evaluator, WorldEvaluator(0))
	
	def test_required_fulfilled(self):
		goal = Goal([BuildingCount(iGranary, 2).create(), BuildingCount(iLibrary, 2).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, required=1)
		
		cities = TestCities.num(2)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(goal.fulfilled(), True)
			self.assertEqual(goal.progress(), [self.SUCCESS + "Granaries: 2 / 2 " + self.FAILURE + "Libraries: 0 / 2"])
		finally:
			cities.kill()
	
	def test_required_not_fulfilled(self):
		goal = Goal([BuildingCount(iGranary, 2).create(), BuildingCount(iLibrary, 2).create(), BuildingCount(iWalls, 2).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, required=2)
		
		cities = TestCities.num(2)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(goal.fulfilled(), False)
			self.assertEqual(goal.progress(), [self.SUCCESS + "Granaries: 2 / 2 " + self.FAILURE + "Libraries: 0 / 2 " + self.FAILURE + "Walls: 0 / 2"])
		finally:
			cities.kill()
	
	def test_succeed_stateless(self):
		goal = Goal([BuildingCount(iGranary, 2).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, mode=STATELESS)
		
		self.assertEqual(goal.state, POSSIBLE)
		
		goal.succeed()
		self.assertEqual(goal.state, POSSIBLE)
	
	def test_succeeded_stateless_not_fulfilled(self):
		goal = Goal([BuildingCount(iGranary, 2).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, mode=STATELESS)
		
		self.assertEqual(goal.state, POSSIBLE)
		self.assertEqual(goal.succeeded(), False)
	
	def test_succeeded_stateless_fulfilled(self):
		goal = Goal([BuildingCount(iGranary, 2).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, mode=STATELESS)
		
		cities = TestCities.num(2)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			self.assertEqual(goal.fulfilled(), True)
			self.assertEqual(goal.succeeded(), True)
		finally:
			cities.kill()
	
	def test_state_string_possible(self):
		self.assertEqual(self.goal.state_string(), "Not yet")
	
	def test_state_string_failure(self):
		self.goal.set_state(FAILURE)
		
		self.assertEqual(self.goal.state_string(), "NO")
	
	def test_state_string_success(self):
		self.goal.set_state(SUCCESS)
		
		self.assertEqual(self.goal.state_string(), "YES")
	
	def test_state_string_stateless_possible(self):
		goal = Goal([BuildingCount(iGranary, 2).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, mode=STATELESS)
		
		self.assertEqual(goal.state_string(), "Not yet")
	
	def test_state_string_stateless_failure(self):
		goal = Goal([BuildingCount(iGranary, 2).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, mode=STATELESS)
		goal.set_state(FAILURE)
		
		self.assertEqual(goal.state_string(), "NO")
	
	def test_state_string_stateless_fulfilled(self):
		goal = Goal([BuildingCount(iGranary, 2).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0, mode=STATELESS)
		
		cities = TestCities.num(2)
		for city in cities:
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(goal.state_string(), "YES")
		finally:
			cities.kill()
	
	def test_immediately_fulfilled_requirement(self):
		goal = Goal([NoCityLost().create()], NoCityLost.GOAL_DESC_KEY, 0)
		
		self.assertEqual(goal.state, SUCCESS)


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
		self.assertEqual(self.all.description(), "Control three Granaries and three Libraries")
	
	def test_description_option(self):
		all = All(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"), GoalDescription([BuildingCount(iLibrary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"), by=1000)
		
		self.assertEqual(all.description(), "Control three Granaries and three Libraries by 1000 AD")
	
	def test_description_subgoal_option(self):
		all = All(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", by=1000), GoalDescription([BuildingCount(iLibrary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"))
		
		self.assertEqual(all.description(), "Control three Granaries by 1000 AD and control three Libraries")
	
	def test_create(self):
		all_goal = self.all(0)
		
		self.assertEqual(all_goal, AllGoal([Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0), Goal([BuildingCount(iLibrary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 0))
	
	def test_create_options(self):
		all = All(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"), by=1000)
		all_goal = all(0)
		
		self.assertEqual(all_goal, AllGoal([Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 0))
		self.assertEqual(all_goal.iYear, 1000)
		self.assertEqual(all_goal.requirements[0].iYear, 1000)
	
	def test_create_subgoal_options(self):
		all = All(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", by=1000))
		all_goal = all(0)
		
		self.assertEqual(all_goal, AllGoal([Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 0))
		self.assertEqual(all_goal.iYear, None)
		self.assertEqual(all_goal.requirements[0].iYear, 1000)


class TestAllGoal(ExtendedTestCase):

	def setUp(self):
		self.first_goal = Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)
		self.second_goal = Goal([BuildingCount(iLibrary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)
		self.all = AllGoal([self.first_goal, self.second_goal], 0)
		
		self.all.enable()
		
		team(0).setHasTech(iCalendar, True, 0, False, False)
		
		self.iSetting = AdvisorOpt.getUHVFinishDate()
		AdvisorOpt.setUHVFinishDate(0)
	
	def tearDown(self):
		self.all.disable()
	
		team(0).setHasTech(iCalendar, False, 0, False, False)
		
		AdvisorOpt.setUHVFinishDate(self.iSetting)
	
	def test_str(self):
		self.assertEqual(str(self.all), "AllGoal(Goal([BuildingCount(Granary, 3)], 0), Goal([BuildingCount(Library, 3)], 0))")
	
	def test_repr(self):
		self.assertEqual(repr(self.all), "AllGoal(Goal([BuildingCount(Granary, 3)], 0), Goal([BuildingCount(Library, 3)], 0))")
	
	def test_equal(self):
		identical = AllGoal([Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0), Goal([BuildingCount(iLibrary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 0)
		different_goal = AllGoal([Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0), Goal([BuildingCount(iWalls, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 0)
		different_num_goals = AllGoal([Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 0)
		different_player = AllGoal([Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0), Goal([BuildingCount(iLibrary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 1)
		
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
		self.assertEqual(self.all.description(), "Control three Granaries and three Libraries")
	
	def test_description_by(self):
		all = AllGoal([self.first_goal, self.second_goal], 0, by=1000)
		
		self.assertEqual(all.description(), "Control three Granaries and three Libraries by 1000 AD")
	
	def test_description_at(self):
		all = AllGoal([self.first_goal, self.second_goal], 0, at=1000)
		
		self.assertEqual(all.description(), "Control three Granaries and three Libraries in 1000 AD")
	
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


class TestDifferentCities(ExtendedTestCase):

	def setUp(self):
		self.different_cities = DifferentCities(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"), GoalDescription([BuildingCount(iLibrary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"))
	
	def test_str(self):
		self.assertEqual(str(self.different_cities), "DifferentCities(GoalDescription(BuildingCount(Granary, 3)), GoalDescription(BuildingCount(Library, 3)))")
	
	def test_repr(self):
		self.assertEqual(repr(self.different_cities), "DifferentCities(GoalDescription(BuildingCount(Granary, 3)), GoalDescription(BuildingCount(Library, 3)))")
	
	def test_equal(self):
		identical = DifferentCities(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"), GoalDescription([BuildingCount(iLibrary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"))
		different_description = DifferentCities(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"), GoalDescription([BuildingCount(iWalls, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"))
		different_num_descriptions = DifferentCities(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"))
		
		self.assertEqual(self.different_cities, identical)
		self.assertNotEqual(self.different_cities, different_description)
		self.assertNotEqual(self.different_cities, different_num_descriptions)
	
	def test_pickle(self):
		self.assertPickleable(self.different_cities)
	
	def test_description(self):
		self.assertEqual(self.different_cities.description(), "Control three Granaries and three Libraries")
	
	def test_description_option(self):
		different_cities = DifferentCities(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"), GoalDescription([BuildingCount(iLibrary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"), by=1000)
		
		self.assertEqual(different_cities.description(), "Control three Granaries and three Libraries by 1000 AD")
	
	def test_description_subgoal_option(self):
		different_cities = DifferentCities(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", by=1000), GoalDescription([BuildingCount(iLibrary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"))
		
		self.assertEqual(different_cities.description(), "Control three Granaries by 1000 AD and control three Libraries")
	
	def test_create(self):
		different_cities_goal = self.different_cities(0)
		
		self.assertEqual(different_cities_goal, DifferentCitiesGoal([Goal([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0), Goal([BuildingCount(iLibrary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 0))
	
	def test_create_options(self):
		different_cities = DifferentCities(GoalDescription([BuildingCount(iGranary, 3)], "TXT_KEY_VICTORY_DESC_CONTROL"), by=1000)
		different_cities_goal = different_cities(0)
		
		self.assertEqual(different_cities_goal, DifferentCitiesGoal([Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 0))
		self.assertEqual(different_cities_goal.iYear, 1000)
		self.assertEqual(different_cities_goal.requirements[0].iYear, 1000)
	
	def test_create_subgoal_options(self):
		different_cities = DifferentCities(GoalDescription([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", by=1000))
		different_cities_goal = different_cities(0)
		
		self.assertEqual(different_cities_goal, DifferentCitiesGoal([Goal([BuildingCount(iGranary, 3).create()], "TXT_KEY_VICTORY_DESC_CONTROL", 0)], 0))
		self.assertEqual(different_cities_goal.iYear, None)
		self.assertEqual(different_cities_goal.requirements[0].iYear, 1000)


class TestDifferentCitiesGoal(ExtendedTestCase):

	def setUp(self):
		self.first_goal = Goal([CityCultureLevel(CapitalCityArgument().named("First Capital"), iCultureLevelDeveloping).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0)
		self.second_goal = Goal([CityCultureLevel(CapitalCityArgument().named("Second Capital"), iCultureLevelRefined).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0)
		
		self.different = DifferentCitiesGoal([self.first_goal, self.second_goal], 0)
		self.different.enable()
		
		team(0).setHasTech(iCalendar, True, 0, False, False)
		
		self.iSetting = AdvisorOpt.getUHVFinishDate()
		AdvisorOpt.setUHVFinishDate(0)
	
	def tearDown(self):
		self.different.disable()
		
		team(0).setHasTech(iCalendar, False, 0, False, False)
		
		AdvisorOpt.setUHVFinishDate(self.iSetting)
	
	def test_str(self):
		self.assertEqual(str(self.different), "DifferentCitiesGoal(Goal([CityCultureLevel(First Capital, Developing)], 0), Goal([CityCultureLevel(Second Capital, Refined)], 0))")
	
	def test_repr(self):
		self.assertEqual(repr(self.different), "DifferentCitiesGoal(Goal([CityCultureLevel(First Capital, Developing)], 0), Goal([CityCultureLevel(Second Capital, Refined)], 0))")
	
	def test_equal(self):
		identical = DifferentCitiesGoal([Goal([CityCultureLevel(CapitalCityArgument().named("First Capital"), iCultureLevelDeveloping).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0), Goal([CityCultureLevel(CapitalCityArgument().named("Second Capital"), iCultureLevelRefined)], "TXT_KEY_VICTORY_DESC_HAVE", 0)], 0)
		different_goal = DifferentCitiesGoal([Goal([CityCultureLevel(CapitalCityArgument().named("First Capital"), iCultureLevelDeveloping).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0), Goal([CityCultureLevel(CapitalCityArgument().named("Second Capital"), iCultureLevelInfluential)], "TXT_KEY_VICTORY_DESC_HAVE", 0)], 0)
		different_num_goals = DifferentCitiesGoal([Goal([CityCultureLevel(CapitalCityArgument().named("First Capital"), iCultureLevelDeveloping).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0)], 0)
		different_player = DifferentCitiesGoal([Goal([CityCultureLevel(CapitalCityArgument().named("First Capital"), iCultureLevelDeveloping).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0), Goal([CityCultureLevel(CapitalCityArgument().named("Second Capital"), iCultureLevelRefined)], "TXT_KEY_VICTORY_DESC_HAVE", 0)], 1)
		
		self.assertEqual(self.different, identical)
		self.assertNotEqual(self.different, different_goal)
		self.assertNotEqual(self.different, different_num_goals)
		self.assertNotEqual(self.different, different_player)
	
	def test_pickle(self):
		self.assertPickleable(self.first_goal)
		self.assertPickleable(self.second_goal)
		self.assertPickleable(self.different)
	
	def test_get_city_parameter(self):
		capital = TestCities.one()
		capital.setHasRealBuilding(iPalace, True)
	
		try:
			city = self.different.get_city_parameter()
		
			self.assertType(city, CyCity)
			self.assertEqual(location(city), (57, 35))
		finally:
			capital.kill()
	
	def test_get_city_parameter_no_city(self):
		self.assertEqual(self.different.get_city_parameter(), NON_EXISTING)
	
	def test_unique_records(self):
		first_capital, second_capital = cities = TestCities.num(2)
		first_capital.setHasRealBuilding(iPalace, True)
		
		try:
			self.first_goal.succeed()
			
			self.assertEqual(self.different.recorded.get(self.first_goal), (57, 35))
			self.assertEqual(self.different.recorded.get(self.second_goal), None)
			
			self.assertEqual(self.different.unique_records(), True)
			
			second_capital.setHasRealBuilding(iPalace, True)
			self.second_goal.succeed()
			
			self.assertEqual(self.different.recorded.get(self.first_goal), (57, 35))
			self.assertEqual(self.different.recorded.get(self.second_goal), (59, 35))
			
			self.assertEqual(self.different.unique_records(), True)
		finally:
			cities.kill()
	
	def test_not_unique_records(self):
		capital = TestCities.one()
		
		try:
			self.first_goal.succeed()
			self.second_goal.succeed()
			
			self.assertEqual(self.different.recorded.get(self.first_goal), (57, 35))
			self.assertEqual(self.different.recorded.get(self.second_goal), (57, 35))
			
			self.assertEqual(self.different.unique_records(), False)
		finally:
			capital.kill()
	
	def test_complete_different_cities(self):
		first_capital, second_capital = cities = TestCities.num(2)
		first_capital.setName("First", False)
		second_capital.setName("Second", False)
	
		first_capital.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqualCity(CapitalCityArgument().get(0), first_capital)
			
			self.assertEqual(self.first_goal.state, POSSIBLE)
			self.assertEqual(self.second_goal.state, POSSIBLE)
			self.assertEqual(self.different.state, POSSIBLE)
			
			self.assertEqual(self.different.format_progress(), [self.FAILURE + "Culture in First: 0 / 100"])
			
			self.first_goal.succeed()
			
			self.assertEqual(self.first_goal.state, SUCCESS)
			self.assertEqual(self.second_goal.state, POSSIBLE)
			self.assertEqual(self.different.state, POSSIBLE)
			
			self.assertEqual(self.different.recorded.get(self.first_goal), (57, 35))
			self.assertEqual(self.different.recorded.get(self.second_goal), None)
			
			self.assertEqual(self.different.format_progress(), [
				self.SUCCESS + "First",
				self.FAILURE + "Already completed for First"
			])
			
			first_capital.setHasRealBuilding(iPalace, False)
			second_capital.setHasRealBuilding(iPalace, True)
			
			self.assertEqualCity(CapitalCityArgument().get(0), second_capital)
			
			self.second_goal.succeed()
			
			self.assertEqual(self.first_goal.state, SUCCESS)
			self.assertEqual(self.second_goal.state, SUCCESS)
			self.assertEqual(self.different.state, SUCCESS)
			
			self.assertEqual(self.different.recorded.get(self.first_goal), (57, 35))
			self.assertEqual(self.different.recorded.get(self.second_goal), (59, 35))
			
			self.assertEqual(self.different.format_progress(), [
				self.SUCCESS + "First",
				self.SUCCESS + "Second",
			])
		finally:
			cities.kill()
	
	def test_complete_same_city(self):
		capital = TestCities.one()
		capital.setName("First", False)
		capital.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqualCity(CapitalCityArgument().get(0), capital)
			
			self.assertEqual(self.first_goal.state, POSSIBLE)
			self.assertEqual(self.second_goal.state, POSSIBLE)
			self.assertEqual(self.different.state, POSSIBLE)
			
			self.assertEqual(self.different.format_progress(), [self.FAILURE + "Culture in First: 0 / 100"])
			
			self.first_goal.succeed()
			
			self.assertEqual(self.first_goal.state, SUCCESS)
			self.assertEqual(self.second_goal.state, POSSIBLE)
			self.assertEqual(self.different.state, POSSIBLE)
			
			self.assertEqual(self.different.recorded.get(self.first_goal), (57, 35))
			self.assertEqual(self.different.recorded.get(self.second_goal), None)
			
			self.assertEqual(self.different.format_progress(), [
				self.SUCCESS + "First",
				self.FAILURE + "Already completed for First",
			])
			
			self.second_goal.succeed()
			
			self.assertEqual(self.first_goal.state, SUCCESS)
			self.assertEqual(self.second_goal.state, FAILURE)
			self.assertEqual(self.different.state, FAILURE)
			
			self.assertEqual(self.different.recorded.get(self.first_goal), (57, 35))
			self.assertEqual(self.different.recorded.get(self.second_goal), (57, 35))
			
			self.assertEqual(self.different.format_progress(), [
				self.SUCCESS + "First",
				self.FAILURE + "Already completed for First",
			])
		finally:
			capital.kill()
	
	def test_complete_same_city_changed_later(self):
		first_capital, second_capital = cities = TestCities.num(2)
		first_capital.setName("First", False)
		second_capital.setName("Second", False)
		
		first_capital.setHasRealBuilding(iPalace, True)
		
		try:
			self.first_goal.succeed()
			self.second_goal.succeed()
			
			self.assertEqual(self.first_goal.state, SUCCESS)
			self.assertEqual(self.second_goal.state, FAILURE)
			self.assertEqual(self.different.state, FAILURE)
			
			self.assertEqual(self.different.format_progress(), [
				self.SUCCESS + "First",
				self.FAILURE + "Already completed for First"
			])
			
			first_capital.setHasRealBuilding(iPalace, False)
			second_capital.setHasRealBuilding(iPalace, True)
			
			self.assertEqualCity(CapitalCityArgument().get(0), second_capital)
			
			self.assertEqual(self.different.state, FAILURE)
			
			self.assertEqual(self.different.format_progress(), [
				self.SUCCESS + "First",
				self.FAILURE + "Culture in Second: 0 / 1000"
			])
		finally:
			cities.kill()
	
	def test_second_goal_fulfilled_but_same_city(self):
		capital = TestCities.one()
		capital.setName("First", False)
		capital.setHasRealBuilding(iPalace, True)
		
		try:
			self.first_goal.succeed()
			
			capital.setCulture(0, 1000, False)
			
			self.assertEqual(self.different.recorded.get(self.first_goal), (57, 35))
			self.assertEqual(self.different.recorded.get(self.second_goal), None)
			
			self.assertEqual(self.first_goal.state, SUCCESS)
			self.assertEqual(self.second_goal.state, POSSIBLE)
			self.assertEqual(self.different.state, POSSIBLE)
			
			self.assertEqual(self.different.format_progress(), [
				self.SUCCESS + "First",
				self.FAILURE + "Already completed for First",
			])
		finally:
			capital.kill()
	
	def test_description(self):
		self.assertEqual(self.different.description(), "Have developing culture in First Capital and refined culture in Second Capital")
	
	def test_description_at(self):
		first_goal = Goal([CityCultureLevel(CapitalCityArgument().named("First Capital"), iCultureLevelDeveloping).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0)
		second_goal = Goal([CityCultureLevel(CapitalCityArgument().named("Second Capital"), iCultureLevelRefined).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0)
		different = DifferentCitiesGoal([first_goal, second_goal], 0, at=1000)
		
		self.assertEqual(different.description(), "Have developing culture in First Capital and refined culture in Second Capital in 1000 AD")
	
	def test_description_by(self):
		first_goal = Goal([CityCultureLevel(CapitalCityArgument().named("First Capital"), iCultureLevelDeveloping).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0)
		second_goal = Goal([CityCultureLevel(CapitalCityArgument().named("Second Capital"), iCultureLevelRefined).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0)
		different = DifferentCitiesGoal([first_goal, second_goal], 0, by=1000)
		
		self.assertEqual(different.description(), "Have developing culture in First Capital and refined culture in Second Capital by 1000 AD")
	
	def test_description_subgoal_at(self):
		first_goal = Goal([CityCultureLevel(CapitalCityArgument().named("First Capital"), iCultureLevelDeveloping).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0, at=1000)
		second_goal = Goal([CityCultureLevel(CapitalCityArgument().named("Second Capital"), iCultureLevelRefined).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0)
		different = DifferentCitiesGoal([first_goal, second_goal], 0)
		
		self.assertEqual(different.description(), "Have developing culture in First Capital in 1000 AD and have refined culture in Second Capital")
	
	def test_description_subgoal_by(self):
		first_goal = Goal([CityCultureLevel(CapitalCityArgument().named("First Capital"), iCultureLevelDeveloping).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0, by=1000)
		second_goal = Goal([CityCultureLevel(CapitalCityArgument().named("Second Capital"), iCultureLevelRefined).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0)
		different = DifferentCitiesGoal([first_goal, second_goal], 0)
		
		self.assertEqual(different.description(), "Have developing culture in First Capital by 1000 AD and have refined culture in Second Capital")


test_cases = [
	TestParameters,
	TestParameterSet,
	TestGoalDefinition,
	TestGoalDescription,
	TestGoal,
	TestAll,
	TestAllGoal,
	TestDifferentCities,
	TestDifferentCitiesGoal,
]
