from VictoryUtils import *

from TestVictoryCommon import *


class TestTextProcessing(ExtendedTestCase):

	def test_format_articles(self):
		self.assertEqual(format_articles("The Internet"), "the Internet")
		self.assertEqual(format_articles("the Internet"), "the Internet")
		self.assertEqual(format_articles("Swordsman"), "Swordsman")
		

test_cases = [
	TestTextProcessing,
]
