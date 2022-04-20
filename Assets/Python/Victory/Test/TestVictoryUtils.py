from VictoryUtils import *

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


class TestAreaDefinition(ExtendedTestCase):

	def setUp(self):
		self.plots = AreaDefinitionFactory()

	def test(self):
		even = lambda p: (p.getX() + p.getY()) % 2 == 0
		
		area = self.plots.rectangle((0, 0), (1, 1)).where(even)
		
		self.assertType(area, AreaDefinition)
		self.assertEqual(area.calls, [("rectangle", ((0, 0), (1, 1)), {}), ("where", (even,), {})])
		
		area = area.create()
		
		self.assertType(area, Plots)
		self.assertEqual(len(area), 2)
		self.assertEqual((0, 0) in area, True)
		self.assertEqual((1, 1) in area, True)
	
	def test_equal(self):
		area = self.plots.of([(0, 0), (0, 1)])
		
		identical = self.plots.of([(0, 1), (0, 0)])
		different_type = PlotFactory().of([(0, 0), (0, 1)])
		different_plots = self.plots.of([(0, 0), (1, 1)])
		
		self.assertEqual(area, identical)
		self.assertNotEqual(area, different_type)
		self.assertNotEqual(area, different_plots)
	
	def test_str(self):
		self.assertEqual(str(plots.rectangle((0, 0), (1, 1)).region(2)), "AreaDefinition.rectangle((0, 0), (1, 1)).region(2)")
	
	def test_without_create(self):
		area = self.plots.rectangle((0, 0), (1, 1))
		
		self.assertType(area, AreaDefinition)
		
		self.assertEqual(len(area), 4)
		self.assertEqual((0, 0) in area, True)
	
	def test_named(self):
		area = self.plots.all().named("Area")
		
		self.assertType(area, AreaDefinition)
		self.assertEqual(area.name(), "Area")
		
		area = area.create()
		
		self.assertType(area, Plots)
		self.assertEqual(area.name(), "Area")
	
	def test_multiple_renames(self):
		area = self.plots.rectangle((0, 0), (1, 1))
		
		area1 = area.create()
		area2 = area.create()
		
		self.assertNotEqual(id(area1), id(area2))
		

test_cases = [
	TestTextProcessing,
	TestAreaDefinition,
]
