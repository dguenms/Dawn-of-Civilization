from Evaluators import *
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
		
	def test_sum(self):
		self.assertEqual(self.evaluator.sum(lambda iPlayer: 1), 1)
	
	def test_evaluate(self):
		self.assertEqual(self.evaluator.evaluate(lambda x: x), 0)
		self.assertEqual(self.evaluator.evaluate(lambda x, a: x+a, 10), 10)
	
	def test_evaluate_aggregate(self):
		self.assertEqual(self.evaluator.evaluate(lambda x, a: a, SumAggregate(1, 2, 3)), 6)
		self.assertEqual(self.evaluator.evaluate(lambda x, a: a, AverageAggregate(1, 2, 3)), 2)
		self.assertEqual(self.evaluator.evaluate(lambda x, a: a, CountAggregate(1, 2, 3)), 3)
	
	def test_evaluate_aggregate_multiple_arguments(self):
		def func(iPlayer, first_arg, item, third_arg):
			return 100 * first_arg + 10 * third_arg + item
		
		self.assertEqual(self.evaluator.evaluate(func, 1, SumAggregate(1, 2, 3), 1), 336)
	
	def test_evaluate_deferred(self):
		argument = StateReligionBuildingArgument(temple)
		
		def func(iPlayer, iBuilding):
			return iBuilding
		
		try:
			player(0).setLastStateReligion(iBuddhism)
			self.assertEqual(self.evaluator.evaluate(func, argument), iBuddhistTemple)
			
			player(0).setLastStateReligion(iHinduism)
			self.assertEqual(self.evaluator.evaluate(func, argument), iHinduTemple)
		finally:
			player(0).setLastStateReligion(-1)


class TestVassalsEvaluator(ExtendedTestCase):

	def setUp(self):
		self.iFirstMaster = 0
		self.iSecondMaster = 4
		self.iThirdMaster = 6
		
		self.iFirstMasterCapitulatedVassal = 1
		self.iFirstMasterPeaceVassal = 2
		
		self.iSecondMasterCapitulatedVassal = 5
		self.iThirdMasterPeaceVassal = 7
		
		self.evaluator = VassalsEvaluator(self.iFirstMaster)
		
		team(self.iFirstMasterCapitulatedVassal).setVassal(self.iFirstMaster, True, True)
		team(self.iFirstMasterPeaceVassal).setVassal(self.iFirstMaster, True, False)
		
		team(self.iSecondMasterCapitulatedVassal).setVassal(self.iSecondMaster, True, True)
		team(self.iThirdMasterPeaceVassal).setVassal(self.iThirdMaster, True, False)
		
	def tearDown(self):
		team(self.iFirstMasterCapitulatedVassal).setVassal(self.iFirstMaster, False, True)
		team(self.iFirstMasterPeaceVassal).setVassal(self.iFirstMaster, False, False)
		
		team(self.iSecondMasterCapitulatedVassal).setVassal(self.iSecondMaster, False, True)
		team(self.iThirdMasterPeaceVassal).setVassal(self.iThirdMaster, False, False)
	
	def test_contains(self):
		self.assertEqual(self.iFirstMaster in self.evaluator, True)
		self.assertEqual(self.iFirstMasterCapitulatedVassal in self.evaluator, True)
		self.assertEqual(self.iFirstMasterPeaceVassal in self.evaluator, True)
		
		self.assertEqual(self.iSecondMaster in self.evaluator, False)
		self.assertEqual(self.iSecondMasterCapitulatedVassal in self.evaluator, False)
		self.assertEqual(self.iThirdMaster in self.evaluator, False)
		self.assertEqual(self.iThirdMasterPeaceVassal in self.evaluator, False)
	
	def test_iterate(self):
		self.assertEqual(list(self.evaluator), [0, 1, 2])
	
	def test_pickle(self):
		self.assertPickleable(self.evaluator)
	
	def test_any(self):
		self.assertEqual(self.evaluator.any(lambda iPlayer: iPlayer == self.iFirstMasterCapitulatedVassal), True)
		self.assertEqual(self.evaluator.any(lambda iPlayer: iPlayer == self.iSecondMaster), False)
	
	def test_sum(self):
		self.assertEqual(self.evaluator.sum(lambda iPlayer: 1), 3)
	
	def test_evaluate(self):
		self.assertEqual(self.evaluator.evaluate(lambda x: x), 3)
		self.assertEqual(self.evaluator.evaluate(lambda x, a: x+a, 1), 6)
	
	def test_evaluate_aggregate(self):
		self.assertEqual(self.evaluator.evaluate(lambda x, a: x+a, SumAggregate(10, 20, 30)), 33 + 63 + 93)
		self.assertEqual(self.evaluator.evaluate(lambda x, a: x+a, AverageAggregate(10, 20, 30)), 63)
		self.assertEqual(self.evaluator.evaluate(lambda x, a: x+a, CountAggregate(10, 20, 30)), 3)


class TestAlliesEvaluator(ExtendedTestCase):

	def setUp(self):
		self.iPlayer = 0
		self.iPlayerPeaceVassal = 1
		self.iPlayerCapitulatedVassal = 2
		
		self.iAlly = 3
		self.iAllyPeaceVassal = 4
		
		self.iDifferentMaster = 5
		self.iDifferentMasterVassal = 6
		
		self.iUnrelatedAlly = 7
		self.iUnrelatedOtherAlly = 8
	
		self.evaluator = AlliesEvaluator(self.iPlayer)
		
		team(self.iPlayerPeaceVassal).setVassal(self.iPlayer, True, False)
		team(self.iPlayerCapitulatedVassal).setVassal(self.iPlayer, True, True)
		
		team(self.iPlayer).setDefensivePact(self.iAlly, True)
		team(self.iAlly).setDefensivePact(self.iPlayer, True)
		
		team(self.iAllyPeaceVassal).setVassal(self.iAlly, True, False)
		
		team(self.iDifferentMasterVassal).setVassal(self.iDifferentMaster, True, False)
		
		team(self.iUnrelatedAlly).setDefensivePact(self.iUnrelatedOtherAlly, True)
		team(self.iUnrelatedOtherAlly).setDefensivePact(self.iUnrelatedAlly, True)
	
	def tearDown(self):
		team(self.iPlayerPeaceVassal).setVassal(self.iPlayer, False, False)
		team(self.iPlayerCapitulatedVassal).setVassal(self.iPlayer, False, True)
		
		team(self.iPlayer).setDefensivePact(self.iAlly, False)
		team(self.iAlly).setDefensivePact(self.iPlayer, False)
		
		team(self.iAllyPeaceVassal).setVassal(self.iAlly, False, False)
		
		team(self.iDifferentMasterVassal).setVassal(self.iDifferentMaster, False, False)
		
		team(self.iUnrelatedAlly).setDefensivePact(self.iUnrelatedOtherAlly, False)
		team(self.iUnrelatedOtherAlly).setDefensivePact(self.iUnrelatedAlly, False)
	
	def test_contains(self):
		self.assertEqual(self.iPlayer in self.evaluator, True)
		self.assertEqual(self.iPlayerPeaceVassal in self.evaluator, True)
		self.assertEqual(self.iPlayerCapitulatedVassal in self.evaluator, True)
		self.assertEqual(self.iAlly in self.evaluator, True)
		self.assertEqual(self.iAllyPeaceVassal in self.evaluator, True)
		
		self.assertEqual(self.iDifferentMaster in self.evaluator, False)
		self.assertEqual(self.iDifferentMasterVassal in self.evaluator, False)
		self.assertEqual(self.iUnrelatedAlly in self.evaluator, False)
		self.assertEqual(self.iUnrelatedOtherAlly in self.evaluator, False)
	
	def test_iterate(self):
		self.assertEqual(list(self.evaluator), [self.iPlayer, self.iPlayerPeaceVassal, self.iPlayerCapitulatedVassal, self.iAlly, self.iAllyPeaceVassal])
	
	def test_pickle(self):
		self.assertPickleable(self.evaluator)
	
	def test_any(self):
		self.assertEqual(self.evaluator.any(lambda iPlayer: iPlayer == self.iPlayerPeaceVassal), True)
		self.assertEqual(self.evaluator.any(lambda iPlayer: iPlayer == self.iDifferentMasterVassal), False)
	
	def test_sum(self):
		self.assertEqual(self.evaluator.sum(lambda iPlayer: 1), 5)
	
	def test_evaluate(self):
		self.assertEqual(self.evaluator.evaluate(lambda x: x), self.iPlayer + self.iPlayerPeaceVassal + self.iPlayerCapitulatedVassal + self.iAlly + self.iAllyPeaceVassal)
		self.assertEqual(self.evaluator.evaluate(lambda x, a: x+a, 1), self.iPlayer + self.iPlayerPeaceVassal + self.iPlayerCapitulatedVassal + self.iAlly + self.iAllyPeaceVassal + 5)


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
	
	def test_sum(self):
		self.assertEqual(self.evaluator.sum(lambda iPlayer: 1), 2)
	
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
	
	def test_sum(self):
		self.assertEqual(self.evaluator.sum(lambda iPlayer: 1), 2)
	
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