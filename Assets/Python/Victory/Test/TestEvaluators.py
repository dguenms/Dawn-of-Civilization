from VictoryEvaluators import *
from TestVictoryCommon import *


class TestEvaluators(ExtendedTestCase):

	def setUp(self):
		self.evaluators = Evaluators()
	
	def test_pickle(self):
		self.assertPickleable(self.evaluators)
	
	def test_get(self):
		evaluator = self.evaluators.get(SELF, 0)
		
		self.assertType(evaluator, SelfEvaluator)
		self.assertEqual(evaluator.iPlayer, 0)
	
	def test_get_nonexistant(self):
		self.assertRaises(ValueError, self.evaluators.get, 123, 0)


class TestSelfEvaluator(ExtendedTestCase):

	def setUp(self):
		self.evaluator = SelfEvaluator(0)
	
	def test_contains(self):
		self.assertEqual(0 in self.evaluator, True)
		self.assertEqual(1 in self.evaluator, False)
	
	def test_iterate(self):
		self.assertEqual(list(self.evaluator), [0])
	
	def test_pickle(self):
		self.assertPickleable(self.evaluator)
		
	def test_any(self):
		self.assertEqual(self.evaluator.any(lambda iPlayer: iPlayer == 0), True)
		self.assertEqual(self.evaluator.any(lambda iPlayer: iPlayer == 1), False)
	
	def test_evaluate(self):
		self.assertEqual(self.evaluator.evaluate(lambda x: x), 0)
		self.assertEqual(self.evaluator.evaluate(lambda x, a: x+a, 10), 10)
	
	def test_evaluate_aggregate(self):
		self.assertEqual(self.evaluator.evaluate(lambda x, a: a, SumAggregate(1, 2, 3)), 6)
		self.assertEqual(self.evaluator.evaluate(lambda x, a: a, AverageAggregate(1, 2, 3)), 2)
		self.assertEqual(self.evaluator.evaluate(lambda x, a: a, CountAggregate(1, 2, 3)), 3)


class TestVassalsEvaluator(ExtendedTestCase):

	def setUp(self):
		self.evaluator = VassalsEvaluator(0)
		
		team(1).setVassal(0, True, True)
		team(2).setVassal(0, True, False)
		
		team(8).setVassal(7, True, True)
		team(10).setVassal(9, True, False)
		
	def tearDown(self):
		team(1).setVassal(0, False, True)
		team(2).setVassal(0, False, False)
		
		team(8).setVassal(7, False, True)
		team(10).setVassal(9, False, False)
	
	def test_contains(self):
		self.assertEqual(0 in self.evaluator, True)
		self.assertEqual(1 in self.evaluator, True)
		self.assertEqual(2 in self.evaluator, True)
		
		self.assertEqual(7 in self.evaluator, False)
		self.assertEqual(8 in self.evaluator, False)
		self.assertEqual(9 in self.evaluator, False)
		self.assertEqual(10 in self.evaluator, False)
	
	def test_iterate(self):
		self.assertEqual(list(self.evaluator), [0, 1, 2])
	
	def test_pickle(self):
		self.assertPickleable(self.evaluator)
	
	def test_any(self):
		self.assertEqual(self.evaluator.any(lambda iPlayer: iPlayer == 1), True)
		self.assertEqual(self.evaluator.any(lambda iPlayer: iPlayer == 3), False)
	
	def test_evaluate(self):
		self.assertEqual(self.evaluator.evaluate(lambda x: x), 3)
		self.assertEqual(self.evaluator.evaluate(lambda x, a: x+a, 1), 6)
	
	def test_evaluate_aggregate(self):
		self.assertEqual(self.evaluator.evaluate(lambda x, a: x+a, SumAggregate(10, 20, 30)), 33 + 63 + 93)
		self.assertEqual(self.evaluator.evaluate(lambda x, a: x+a, AverageAggregate(10, 20, 30)), 63)
		self.assertEqual(self.evaluator.evaluate(lambda x, a: x+a, CountAggregate(10, 20, 30)), 3)


class TestAlliesEvaluator(ExtendedTestCase):

	def setUp(self):
		self.evaluator = AlliesEvaluator(0)
		
		team(1).setVassal(0, True, False)
		team(2).setVassal(0, True, True)
		
		team(7).setDefensivePact(0, True)
		team(0).setDefensivePact(7, True)
		
		team(8).setVassal(7, True, False)
		
		team(10).setVassal(9, True, False)
		
		team(11).setDefensivePact(12, True)
		team(12).setDefensivePact(11, True)
	
	def tearDown(self):
		team(1).setVassal(0, False, False)
		team(2).setVassal(0, False, True)
		
		team(7).setDefensivePact(0, False)
		team(0).setDefensivePact(7, False)
		
		team(8).setVassal(7, False, False)
		
		team(10).setVassal(9, False, False)
		
		team(11).setDefensivePact(12, False)
		team(12).setDefensivePact(11, False)
	
	def test_contains(self):
		self.assertEqual(0 in self.evaluator, True)
		self.assertEqual(1 in self.evaluator, True)
		self.assertEqual(2 in self.evaluator, True)
		self.assertEqual(7 in self.evaluator, True)
		self.assertEqual(8 in self.evaluator, True)
		
		self.assertEqual(9 in self.evaluator, False)
		self.assertEqual(10 in self.evaluator, False)
		self.assertEqual(11 in self.evaluator, False)
		self.assertEqual(12 in self.evaluator, False)
	
	def test_iterate(self):
		self.assertEqual(list(self.evaluator), [0, 1, 2, 7, 8])
	
	def test_pickle(self):
		self.assertPickleable(self.evaluator)
	
	def test_any(self):
		self.assertEqual(self.evaluator.any(lambda iPlayer: iPlayer == 1), True)
		self.assertEqual(self.evaluator.any(lambda iPlayer: iPlayer == 9), False)
	
	def test_evaluate(self):
		self.assertEqual(self.evaluator.evaluate(lambda x: x), 18)
		self.assertEqual(self.evaluator.evaluate(lambda x, a: x+a, 1), 23)


class TestReligionEvaluator(ExtendedTestCase):

	def setUp(self):
		self.evaluator = ReligionEvaluator(0)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		player(1).setLastStateReligion(iOrthodoxy)
		player(2).setLastStateReligion(iCatholicism)
		
	def tearDown(self):
		player(0).setLastStateReligion(-1)
		player(1).setLastStateReligion(-1)
		player(2).setLastStateReligion(-1)
	
	def test_contains(self):
		self.assertEqual(0 in self.evaluator, True)
		self.assertEqual(1 in self.evaluator, True)
		
		self.assertEqual(2 in self.evaluator, False)
		self.assertEqual(3 in self.evaluator, False)
	
	def test_iterate(self):
		self.assertEqual(list(self.evaluator), [0, 1])
	
	def test_pickle(self):
		self.assertPickleable(self.evaluator)
	
	def test_any(self):
		self.assertEqual(self.evaluator.any(lambda iPlayer: iPlayer == 1), True)
		self.assertEqual(self.evaluator.any(lambda iPlayer: iPlayer == 2), False)
	
	def test_evaluate(self):
		self.assertEqual(self.evaluator.evaluate(lambda x: x), 1)
		self.assertEqual(self.evaluator.evaluate(lambda x, a: x+a, 1), 3)
	

class TestSecularEvaluator(ExtendedTestCase):

	def setUp(self):
		self.evaluator = SecularEvaluator(0)
		
		player(0).setCivics(infos.civic(iSecularism).getCivicOptionType(), iSecularism)
		player(1).setCivics(infos.civic(iSecularism).getCivicOptionType(), iSecularism)
	
	def tearDown(self):
		player(0).setCivics(infos.civic(iSecularism).getCivicOptionType(), iAnimism)
		player(1).setCivics(infos.civic(iSecularism).getCivicOptionType(), iAnimism)
	
	def test_contains(self):
		self.assertEqual(0 in self.evaluator, True)
		self.assertEqual(1 in self.evaluator, True)
		self.assertEqual(2 in self.evaluator, False)
	
	def test_iterate(self):
		self.assertEqual(list(self.evaluator), [0, 1])
	
	def test_pickle(self):
		self.assertPickleable(self.evaluator)
	
	def test_any(self):
		self.assertEqual(self.evaluator.any(lambda iPlayer: iPlayer == 1), True)
		self.assertEqual(self.evaluator.any(lambda iPlayer: iPlayer == 2), False)
	
	def test_evaluate(self):
		self.assertEqual(self.evaluator.evaluate(lambda x: x), 1)
		self.assertEqual(self.evaluator.evaluate(lambda x, a: x+a, 1), 3)


class TestWorldEvaluator(ExtendedTestCase):

	def setUp(self):
		self.evaluator = WorldEvaluator(0)
		
		player(2).setMinorCiv(True)
	
	def tearDown(self):
		player(2).setMinorCiv(False)
	
	def test_contains(self):
		self.assertEqual(0 in self.evaluator, True)
		self.assertEqual(1 in self.evaluator, True)
		self.assertEqual(2 in self.evaluator, False)
	
	def test_iterate(self):
		self.assertEqual(list(self.evaluator), players.major().alive().without(2).entities())
	
	def test_pickle(self):
		self.assertPickleable(self.evaluator)
	
	def test_any(self):
		self.assertEqual(self.evaluator.any(lambda iPlayer: iPlayer == 1), True)
		self.assertEqual(self.evaluator.any(lambda iPlayer: iPlayer == 2), False)
	
	def test_evaluate(self):
		self.assertEqual(self.evaluator.evaluate(lambda x: x), players.major().alive().without(2).sum(lambda x: x))
		self.assertEqual(self.evaluator.evaluate(lambda x, a: x+a, 1), players.major().alive().without(2).sum(lambda x: x+1))


class TestComparison(ExtendedTestCase):

	def test_identical(self):
		self.assertEqual(SelfEvaluator(0), SelfEvaluator(0))
	
	def test_different_player(self):
		self.assertNotEqual(SelfEvaluator(0), SelfEvaluator(1))
	
	def test_different_evaluator(self):
		self.assertNotEqual(SelfEvaluator(0), WorldEvaluator(0))
		


test_cases = [
	TestEvaluators,
	TestSelfEvaluator,
	TestVassalsEvaluator,
	TestAlliesEvaluator,
	TestReligionEvaluator,
	TestSecularEvaluator,
	TestWorldEvaluator,
	TestComparison,
]