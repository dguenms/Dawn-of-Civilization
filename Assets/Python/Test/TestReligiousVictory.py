from ReligiousVictory import *
from TestUtils import *


class TestReligiousVictory(PickleTestCase):

	def testPickle(self):
		for iReligion, goals in dGoals.items():
			print "test pickle goals for religion %d" % iReligion
			for goal in goals:
				print goal.description()
				self.assertPickleable(goal)


test_cases = [
	TestReligiousVictory
]


suite = TestSuite([makeSuite(case) for case in test_cases])
TextTestRunner(verbosity=2).run(suite)