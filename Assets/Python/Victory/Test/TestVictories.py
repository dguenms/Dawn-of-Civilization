from TestEvaluators import test_cases as evaluators_test_cases
from TestGoals import test_cases as goals_test_cases
from TestHandlers import test_cases as handlers_test_cases
from TestProgress import test_cases as progress_test_cases
from TestRequirements import test_cases as requirements_test_cases
from TestTypes import test_cases as types_test_cases
from TestVictoryUtils import test_cases as utils_test_cases

from unittest import *

from TestUtils import setup


setup()

test_cases = (
	evaluators_test_cases + 
	goals_test_cases + 
	handlers_test_cases +
	progress_test_cases +
	requirements_test_cases +
	types_test_cases +
	utils_test_cases
)

suite = TestSuite([makeSuite(case) for case in test_cases])
TextTestRunner(verbosity=2).run(suite)