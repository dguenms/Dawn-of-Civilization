from HistoricalVictory import *
from TestUtils import *


class TestHistoricalVictory(PickleTestCase):

	def testPickle(self):
		for iCiv, goals in dGoals.items():
			print "test pickle goals for %s" % infos.civ(iCiv).getText()
			for goal in goals:
				print goal.description()
				self.assertPickleable(goal)


test_cases = [
	TestHistoricalVictory
]


suite = TestSuite([makeSuite(case) for case in test_cases])
TextTestRunner(verbosity=2).run(suite)