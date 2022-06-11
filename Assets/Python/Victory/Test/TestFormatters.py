from VictoryFormatters import *

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
		

test_cases = [
	TestTextProcessing,
]
