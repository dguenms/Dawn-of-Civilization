from VictoryProgress import *
from TestVictoryCommon import *


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
	

test_cases = [
	TestProgress,
]