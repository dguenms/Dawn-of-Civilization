from Formatters import *
from Requirements import *

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

	def test_format_articles(self):
		self.assertEqual(format_articles("The Internet"), "the Internet")
		self.assertEqual(format_articles("the Internet"), "the Internet")
		self.assertEqual(format_articles("Swordsman"), "Swordsman")
	
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
	
	def test_in_area(self):
		self.assertEqual(in_area("this is a sentence", plots.rectangle((10, 10), (20, 20)).named("Test Area")), "this is a sentence in Test Area")
	
	def test_in_area_none(self):
		self.assertEqual(in_area("this is a sentence", None), "this is a sentence")
	
	def test_format_date_turn_before(self):
		self.assertEqual(format_date_turn(-1000, False), "1000 BC")
	
	def test_format_date_turn_after(self):
		self.assertEqual(format_date_turn(1000, False), "1000 AD")
	
	def test_format_date_turn(self):
		self.assertEqual(format_date_turn(1000, True), "1000 AD (Turn 270)")
	
	def test_remove_articles(self):
		self.assertEqual(remove_articles("the Mediterranean"), "Mediterranean")


class StringProgress(object):

	def progress(self, evaluator):
		return "string"


class ListProgress(object):

	def progress(self, evaluator):
		return ["one", "two", "three"]


class TestProgress(ExtendedTestCase):

	def setUp(self):
		self.progress = Progress()
		
		self.string_progress = StringProgress()
		self.list_progress = ListProgress()
		
		self.evaluator = SelfEvaluator(self.iPlayer)
	
	def test_get_row_size(self):
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 2), 3)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 3), 3)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 4), 4)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 5), 3)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 6), 3)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 7), 4)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 8), 4)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 9), 3)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 10), 4)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 11), 4)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 12), 4)
	
	def test_get_item_progress_single(self):
		self.assertEqual(self.progress.get_item_progress([self.string_progress] * 5, self.evaluator), ["string"] * 5)
	
	def test_get_item_progress_list(self):
		self.assertEqual(self.progress.get_item_progress([self.list_progress], self.evaluator), [])
	
	def test_format_items(self):
		self.assertEqual(list(self.progress.format_items([self.string_progress] * 5, self.evaluator)), ["string string string", "string string"])

	def test_format_items_list(self):
		self.assertEqual(list(self.progress.format_items([self.list_progress], self.evaluator)), [])
	
	def test_format_list(self):
		self.assertEqual(list(self.progress.format_list([self.list_progress] * 2, self.evaluator)), ["one", "two", "three", "one", "two", "three"])
	
	def test_format_list_string(self):
		self.assertEqual(list(self.progress.format_list([self.string_progress] * 3, self.evaluator)), [])
	
	def test_format_with_list(self):
		self.assertEqual(self.progress.format([self.list_progress] * 2, self.evaluator), ["one", "two", "three", "one", "two", "three"])
	
	def test_format_with_string(self):
		self.assertEqual(self.progress.format([self.string_progress] * 5, self.evaluator), ["string string string", "string string"])
	
	def test_format_mixed(self):
		self.assertEqual(self.progress.format([self.string_progress] * 5 + [self.list_progress], self.evaluator), ["one", "two", "three", "string string string", "string string"])


class TestDescription(ExtendedTestCase):
	
	def setUp(self):
		self.description = Description()
	
	def test_single_requirement(self):
		requirements = [(BuildingCount(iGranary, 3), BuildingCount.GOAL_DESC_KEY, [], [])]
		
		self.assertEqual(self.description.format(requirements, [], [], None), "control three Granaries")
	
	def test_single_requirement_suffix(self):
		requirements = [(BuildingCount(iGranary, 3), BuildingCount.GOAL_DESC_KEY, [], [])]
		suffixes = ["by 1000 AD"]
		
		self.assertEqual(self.description.format(requirements, [], suffixes, None), "control three Granaries by 1000 AD")
	
	def test_single_requirement_required(self):
		requirements = [(BuildingCount(iGranary, 3), BuildingCount.GOAL_DESC_KEY, [], [])]
		
		self.assertEqual(self.description.format(requirements, [], [], 2), "control two out of three Granaries")
	
	def test_multiple_requirements(self):
		requirements = [(BuildingCount(iGranary, 3), BuildingCount.GOAL_DESC_KEY, [], []), (BuildingCount(iLibrary, 4), BuildingCount.GOAL_DESC_KEY, [], []), (BuildingCount(iWalls, 5), BuildingCount.GOAL_DESC_KEY, [], [])]
		
		self.assertEqual(self.description.format(requirements, [], [], None), "control three Granaries, four Libraries and five Walls")
	
	def test_multiple_requirements_suffix(self):
		requirements = [(BuildingCount(iGranary, 3), BuildingCount.GOAL_DESC_KEY, [], []), (BuildingCount(iLibrary, 4), BuildingCount.GOAL_DESC_KEY, [], []), (BuildingCount(iWalls, 5), BuildingCount.GOAL_DESC_KEY, [], [])]
		suffixes = ["by 1000 AD"]
		
		self.assertEqual(self.description.format(requirements, [], suffixes, None), "control three Granaries, four Libraries and five Walls by 1000 AD")
	
	def test_multiple_requirements_required(self):
		requirements = [(BuildingCount(iGranary, 3), BuildingCount.GOAL_DESC_KEY, [], []), (BuildingCount(iLibrary, 4), BuildingCount.GOAL_DESC_KEY, [], []), (BuildingCount(iWalls, 5), BuildingCount.GOAL_DESC_KEY, [], [])]
		
		self.assertEqual(self.description.format(requirements, [], [], 2), "control two out of three Granaries, four Libraries and five Walls")
	
	def test_multiple_goals(self):
		requirements = [(BuildingCount(iGranary, 3), BuildingCount.GOAL_DESC_KEY, [], []), (ResourceCount(iSilk, 4), ResourceCount.GOAL_DESC_KEY, [], [])]
		
		self.assertEqual(self.description.format(requirements, [], [], None), "control three Granaries and acquire four Silk resources")
	
	def test_multiple_goals_different_suffixes(self):
		requirements = [(BuildingCount(iGranary, 3), BuildingCount.GOAL_DESC_KEY, [], ["by 1000 AD"]), (ResourceCount(iSilk, 4), ResourceCount.GOAL_DESC_KEY, [], ["in 1500 AD"])]
		
		self.assertEqual(self.description.format(requirements, [], [], None), "control three Granaries by 1000 AD and acquire four Silk resources in 1500 AD")
	
	def test_multiple_goals_global_suffix(self):
		requirements = [(BuildingCount(iGranary, 3), BuildingCount.GOAL_DESC_KEY, [], []), (ResourceCount(iSilk, 4), ResourceCount.GOAL_DESC_KEY, [], [])]
		suffixes = ["by 1000 AD"]
		
		self.assertEqual(self.description.format(requirements, [], suffixes, None), "control three Granaries and acquire four Silk resources by 1000 AD")
	
	def test_multiple_goals_required(self):
		requirements = [(BuildingCount(iGranary, 3), BuildingCount.GOAL_DESC_KEY, [], []), (ResourceCount(iSilk, 4), ResourceCount.GOAL_DESC_KEY, [], [])]
		
		self.assertEqual(self.description.format(requirements, [], [], 2), "control two out of three Granaries and acquire two out of four Silk resources")
	
	def test_multiple_goals_shared_arguments(self):
		requirements = [(BestCultureCity(LocationCityArgument((61, 31)).named("Test City")), BestCultureCity.GOAL_DESC_KEY, [], []), (BestPopulationCity(LocationCityArgument((61, 31)).named("Test City")), BestPopulationCity.GOAL_DESC_KEY, [], [])]
		
		self.assertEqual(self.description.format(requirements, [], [], None), "make Test City the most culturally advanced and the most populous city in the world")
	
	def test_multiple_goals_different_arguments(self):
		requirements = [(BestCultureCity(LocationCityArgument((61, 31)).named("First City")), BestCultureCity.GOAL_DESC_KEY, [], []), (BestPopulationCity(LocationCityArgument((63, 31)).named("Second City")), BestPopulationCity.GOAL_DESC_KEY, [], [])]
		
		self.assertEqual(self.description.format(requirements, [], [], None), "make First City the most culturally advanced city in the world and make Second City the most populous city in the world")
	
	def test_multiple_goals_different_desc_keys(self):
		requirements = [(BestCultureCity(LocationCityArgument((61, 31)).named("Test City")), "TXT_KEY_VICTORY_DESC_HAVE", [], []), (BestPopulationCity(LocationCityArgument((61, 31)).named("Test City")), "TXT_KEY_VICTORY_DESC_ACQUIRE", [], [])]
		
		self.assertEqual(self.description.format(requirements, [], [], None), "have the most culturally advanced and acquire the most populous")
	
	def test_multiple_goals_different_suffixes(self):
		requirements = [(BestCultureCity(LocationCityArgument((61, 31)).named("Test City")), BestCultureCity.GOAL_DESC_KEY, [], ["by 1000 AD"]), (BestPopulationCity(LocationCityArgument((61, 31)).named("Test City")), BestPopulationCity.GOAL_DESC_KEY, [], ["in 1500 AD"])]
		
		self.assertEqual(self.description.format(requirements, [], [], None), "make Test City the most culturally advanced city in the world by 1000 AD and make Test City the most populous city in the world in 1500 AD")
	
	def test_multiple_goals_shared_arguments_global_suffix(self):
		requirements = [(BestCultureCity(LocationCityArgument((61, 31)).named("Test City")), BestCultureCity.GOAL_DESC_KEY, [], []), (BestPopulationCity(LocationCityArgument((61, 31)).named("Test City")), BestPopulationCity.GOAL_DESC_KEY, [], [])]
		suffixes = ["by 1000 AD"]
		
		self.assertEqual(self.description.format(requirements, [], suffixes, None), "make Test City the most culturally advanced and the most populous city in the world by 1000 AD")
	
	def test_multiple_goals_shared_arguments_required(self):
		requirements = [(BestCultureCity(LocationCityArgument((61, 31)).named("Test City")), BestCultureCity.GOAL_DESC_KEY, [], []), (BestPopulationCity(LocationCityArgument((61, 31)).named("Test City")), BestPopulationCity.GOAL_DESC_KEY, [], [])]
		
		self.assertEqual(self.description.format(requirements, [], [], 2), "make Test City two out of the most culturally advanced and the most populous city in the world")


test_cases = [
	TestTextProcessing,
	TestProgress,
	TestDescription,
]
