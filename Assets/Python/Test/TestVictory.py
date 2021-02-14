from VictoryGoals import *
from unittest import *

from inspect import isfunction


class ExtendedTestCase(TestCase):

	def assertType(self, object, expectedType):
		self.assertEqual(type(object), expectedType)


class TestGetNumArgs(ExtendedTestCase):

	def testFunction(self):
		def noargs():
			pass
		def onearg(arg):
			pass
		def twoargs(arg1, arg2):
			pass
		
		self.assertEqual(getnumargs(noargs), 0)
		self.assertEqual(getnumargs(onearg), 1)
		self.assertEqual(getnumargs(twoargs), 2)
	
	def testMethod(self):
		class SomeClass(object):
			def noargs(self):
				pass
			def onearg(self, arg):
				pass
			def twoargs(self, arg1, arg2):
				pass
		
		self.assertEqual(getnumargs(SomeClass.noargs), 1)
		self.assertEqual(getnumargs(SomeClass.onearg), 2)
		self.assertEqual(getnumargs(SomeClass.twoargs), 3)
	
	def testLambda(self):
		self.assertEqual(getnumargs(lambda: 0), 0)
		self.assertEqual(getnumargs(lambda x: x), 1)
		self.assertEqual(getnumargs(lambda x, y: (x, y)), 2)
	
	def testDLLMethods(self):
		self.assertEqual(getnumargs(CyPlot.getX), 1)
		self.assertEqual(getnumargs(CyPlot.getYield), 2)
		self.assertEqual(getnumargs(CyPlot.at), 3)


class PlayerContainer(object):

	def __init__(self, iPlayer):
		self.iPlayer = iPlayer


# TODO: some handlers are missing here
class TestEventHandlers(ExtendedTestCase):

	def setUp(self):
		self.handlers = EventHandlers.ours()
		self.others = EventHandlers.others()
		self.any = EventHandlers.any()
		
		self.iCallCount = 0
		self.iIncrement = 0
		self.capturedArgument = None
	
	def trackCall(self, *args):
		self.iCallCount += 1
	
	def increment(self, other, iChange):
		self.iIncrement += iChange
	
	def captureArgument(self, other, *args):
		self.capturedArgument = args
	
	def testGet(self):
		handler_func = self.handlers.get("techAcquired", lambda *args: 0)
		
		self.assert_(isfunction(handler_func))
		self.assertEqual(handler_func.__name__, "techAcquired")
	
	def testGetNonExistent(self):
		self.assertRaises(Exception, self.handlers.get, "someNonexistentEvent", lambda *args: 0)
	
	def testBeginPlayerTurn(self):
		onBeginPlayerTurn = self.handlers.get("BeginPlayerTurn", self.trackCall)
		
		onBeginPlayerTurn(PlayerContainer(0), (100, 0))
		self.assertEqual(self.iCallCount, 1)
		
		onBeginPlayerTurn(PlayerContainer(1), (100, 0))
		self.assertEqual(self.iCallCount, 1)
	
	def testTechAcquired(self):
		onTechAcquired = self.handlers.get("techAcquired", self.trackCall)
		
		onTechAcquired(PlayerContainer(0), (10, 0, 0, False))
		self.assertEqual(self.iCallCount, 1)
		
		onTechAcquired(PlayerContainer(1), (10, 0, 0, False))
		self.assertEqual(self.iCallCount, 1)
	
	def testCombatResult(self):
		onCombatResult = self.handlers.get("combatResult", self.trackCall)
		winningUnit = makeUnit(0, 0, (0, 0))
		losingUnit = makeUnit(1, 0, (0, 1))
		
		onCombatResult(PlayerContainer(0), (winningUnit, losingUnit))
		self.assertEqual(self.iCallCount, 1)
		
		onCombatResult(PlayerContainer(1), (winningUnit, losingUnit))
		self.assertEqual(self.iCallCount, 1)
		
		winningUnit.kill(0, False)
		losingUnit.kill(0, False)
	
	def testPlayerGoldTrade(self):
		onPlayerGoldTrade = self.handlers.get("playerGoldTrade", self.increment)
		
		onPlayerGoldTrade(PlayerContainer(0), (1, 0, 100))
		self.assertEqual(self.iIncrement, 100)
		
		onPlayerGoldTrade(PlayerContainer(1), (1, 0, 100))
		self.assertEqual(self.iIncrement, 100)
	
	def testUnitPillage(self):
		onUnitPillage = self.handlers.get("unitPillage", self.increment)
		unit = makeUnit(0, 0, (0, 0))
		
		onUnitPillage(PlayerContainer(0), (unit, 0, -1, 0, 100))
		self.assertEqual(self.iIncrement, 100)
		
		onUnitPillage(PlayerContainer(1), (unit, 0, -1, 0, 100))
		self.assertEqual(self.iIncrement, 100)
		
		unit.kill(False, -1)
	
	def testCityCaptureGold(self):
		onCityCaptureGold = self.handlers.get("cityCaptureGold", self.increment)
		city = player(1).initCity(0, 0)
		
		onCityCaptureGold(PlayerContainer(0), (city, 0, 100))
		self.assertEqual(self.iIncrement, 100)
		
		onCityCaptureGold(PlayerContainer(1), (city, 0, 100))
		self.assertEqual(self.iIncrement, 100)
		
		city.kill()
	
	def testCityAcquired(self):
		onCityAcquired = self.handlers.get("cityAcquired", self.trackCall)
		city = player(1).initCity(0, 0)
		
		onCityAcquired(PlayerContainer(0), (1, 0, city, False, False))
		self.assertEqual(self.iCallCount, 1)
		
		onCityAcquired(PlayerContainer(1), (1, 0, city, False, False))
		self.assertEqual(self.iCallCount, 1)
		
		city.kill()
	
	def testCityBuilt(self):
		onCityBuilt = self.handlers.get("cityBuilt", self.trackCall)
		city = player(0).initCity(0, 0)
		
		onCityBuilt(PlayerContainer(0), (city,))
		self.assertEqual(self.iCallCount, 1)
		
		onCityBuilt(PlayerContainer(1), (city,))
		self.assertEqual(self.iCallCount, 1)
		
		city.kill()
	
	def testBlockade(self):
		onBlockade = self.handlers.get("blockade", self.increment)
		
		onBlockade(PlayerContainer(0), (0, 100))
		self.assertEqual(self.iIncrement, 100)
		
		onBlockade(PlayerContainer(1), (0, 100))
		self.assertEqual(self.iIncrement, 100)

	def testCityRazed(self):
		onCityRazed = self.handlers.get("cityRazed", self.trackCall)
		city = player(1).initCity(0, 0)
		
		onCityRazed(PlayerContainer(0), (city, 0))
		self.assertEqual(self.iCallCount, 1)
		
		onCityRazed(PlayerContainer(1), (city, 0))
		self.assertEqual(self.iCallCount, 1)
		
		city.kill()
	
	def testPlayerSlaveTrade(self):
		onPlayerSlaveTrade = self.handlers.get("playerSlaveTrade", self.increment)
		
		onPlayerSlaveTrade(PlayerContainer(0), (0, 100))
		self.assertEqual(self.iIncrement, 100)
		
		onPlayerSlaveTrade(PlayerContainer(1), (0, 100))
		self.assertEqual(self.iIncrement, 100)
	
	def testGreatPersonBorn(self):
		onGreatPersonBorn = self.handlers.get("greatPersonBorn", self.trackCall)
		
		onGreatPersonBorn(PlayerContainer(0), (None, 0, None))
		self.assertEqual(self.iCallCount, 1)
		
		onGreatPersonBorn(PlayerContainer(1), (None, 0, None))
		self.assertEqual(self.iCallCount, 1)
	
	def testPeaceBrokered(self):
		onPeaceBrokered = self.handlers.get("peaceBrokered", self.trackCall)
		
		onPeaceBrokered(PlayerContainer(0), (0, 1, 2))
		self.assertEqual(self.iCallCount, 1)
		
		onPeaceBrokered(PlayerContainer(1), (0, 1, 2))
		self.assertEqual(self.iCallCount, 1)
	
	def testEnslave(self):
		onEnslave = self.handlers.get("enslave", self.trackCall)
		
		onEnslave(PlayerContainer(0), (0, None))
		self.assertEqual(self.iCallCount, 1)
		
		onEnslave(PlayerContainer(1), (0, None))
		self.assertEqual(self.iCallCount, 1)
	
	def testFirstContact(self):
		onFirstContact = self.handlers.get("enslave", self.trackCall)
		
		onFirstContact(PlayerContainer(0), (0, 1))
		self.assertEqual(self.iCallCount, 1)
		
		onFirstContact(PlayerContainer(1), (0, 1))
		self.assertEqual(self.iCallCount, 1)
	
	def testTradeMission(self):
		def increment_at(other, (x, y), iChange):
			if (x, y) == (0, 0):
				self.iIncrement += iChange
		
		onTradeMission = self.handlers.get("tradeMission", increment_at)
		
		onTradeMission(PlayerContainer(0), (iWarrior, 0, 0, 0, 100))
		self.assertEqual(self.iIncrement, 100)
		
		onTradeMission(PlayerContainer(1), (iWarrior, 0, 0, 0, 100))
		self.assertEqual(self.iIncrement, 100)
		
		onTradeMission(PlayerContainer(0), (iWarrior, 0, 1, 1, 100))
		self.assertEqual(self.iIncrement, 100)
	
	def testReligionFounded(self):
		onReligionFounded = self.handlers.get("religionFounded", self.captureArgument)
		
		onReligionFounded(PlayerContainer(0), (iCatholicism, 0))
		self.assertEqual(self.capturedArgument, (iCatholicism,))
		
		onReligionFounded(PlayerContainer(0), (iProtestantism, 1))
		self.assertEqual(self.capturedArgument, (iCatholicism,))
	
	def testPlayerChangeStateReligion(self):
		onPlayerChangeStateReligion = self.handlers.get("playerChangeStateReligion", self.captureArgument)
		
		onPlayerChangeStateReligion(PlayerContainer(0), (0, iProtestantism, iCatholicism))
		self.assertEqual(self.capturedArgument, (iProtestantism,))
		
		onPlayerChangeStateReligion(PlayerContainer(0), (1, iBuddhism, iHinduism))
		self.assertEqual(self.capturedArgument, (iProtestantism,))
	
	def testBuildingBuilt(self):
		onBuildingBuilt = self.handlers.get("buildingBuilt", self.captureArgument)
		city = player(0).initCity(0, 0)
		
		onBuildingBuilt(PlayerContainer(0), (city, iGranary))
		self.assertEqual(self.capturedArgument, (city, iGranary,))
		
		onBuildingBuilt(PlayerContainer(1), (city, iLibrary))
		self.assertEqual(self.capturedArgument, (city, iGranary,))
		
		city.kill()
	
	def testProjectBuilt(self):
		onProjectBuilt = self.handlers.get("projectBuilt", self.captureArgument)
		city = player(0).initCity(0, 0)
		
		onProjectBuilt(PlayerContainer(0), (city, iTheInternet))
		self.assertEqual(self.capturedArgument, (iTheInternet,))
		
		onProjectBuilt(PlayerContainer(1), (city, iGoldenRecord))
		self.assertEqual(self.capturedArgument, (iTheInternet,))
		
		city.kill()
	
	def testCorporationSpread(self):
		onCorporationSpread = self.handlers.get("corporationSpread", self.captureArgument)
		
		onCorporationSpread(PlayerContainer(0), (iTextileIndustry, 0, None))
		self.assertEqual(self.capturedArgument, (iTextileIndustry,))
		
		onCorporationSpread(PlayerContainer(0), (iSteelIndustry, 1, None))
		self.assertEqual(self.capturedArgument, (iTextileIndustry,))
	
	def testCorporationRemove(self):
		onCorporationRemove = self.handlers.get("corporationRemove", self.captureArgument)
		
		onCorporationRemove(PlayerContainer(0), (iTextileIndustry, 0, None))
		self.assertEqual(self.capturedArgument, (iTextileIndustry,))
		
		onCorporationRemove(PlayerContainer(0), (iSteelIndustry, 1, None))
		self.assertEqual(self.capturedArgument, (iTextileIndustry,))
	
	def testVassalState(self):
		onVassalState = self.handlers.get("vassalState", self.trackCall)
		
		onVassalState(PlayerContainer(0), (0, 1, True, False))
		self.assertEqual(self.iCallCount, 1)
		
		onVassalState(PlayerContainer(0), (1, 2, True, False))
		self.assertEqual(self.iCallCount, 1)
	
	def testOthers(self):
		onBeginPlayerTurn = self.others.get("BeginPlayerTurn", self.trackCall)
		
		onBeginPlayerTurn(PlayerContainer(0), (0, 0))
		self.assertEqual(self.iCallCount, 0)
		
		onBeginPlayerTurn(PlayerContainer(1), (0, 0))
		self.assertEqual(self.iCallCount, 1)
		
		onBeginPlayerTurn(PlayerContainer(2), (0, 0))
		self.assertEqual(self.iCallCount, 2)
	
	def testAny(self):
		onBeginPlayerTurn = self.any.get("BeginPlayerTurn", self.trackCall)
		
		onBeginPlayerTurn(PlayerContainer(0), (0, 0))
		self.assertEqual(self.iCallCount, 1)
		
		onBeginPlayerTurn(PlayerContainer(1), (0, 0))
		self.assertEqual(self.iCallCount, 2)
		
		onBeginPlayerTurn(PlayerContainer(2), (0, 0))
		self.assertEqual(self.iCallCount, 3)


class TestDeferred(ExtendedTestCase):

	def testCapitalWithoutCities(self):
		city = capital()
		self.assertEqual(city(0), None)
		
	def testCapitalAfterCity(self):
		city = player(0).initCity(0, 0)
		city.setHasRealBuilding(iPalace, True)
		
		capital_ = capital()
		
		self.assertEqual(capital_(0).getID(), city.getID())
		
		city.kill()
		
	def testCapitalBeforeCity(self):
		capital_ = capital()
		city = player(0).initCity(0, 0)
		city.setHasRealBuilding(iPalace, True)
		
		self.assertEqual(capital_(0).getID(), city.getID())
		
		city.kill()
		
	def testCityVarargs(self):
		city_ = player(0).initCity(0, 0)
		deferredCity = city(0, 0)
		
		self.assertEqual(deferredCity().getID(), city_.getID())
		
		city_.kill()
	
	def testCityWithoutCities(self):
		deferredCity = city((0, 0))
		self.assertEqual(deferredCity(), None)
	
	def testCityAfterCity(self):
		city_ = player(0).initCity(0, 0)
		deferredCity = city((0, 0))
		
		self.assertEqual(deferredCity().getID(), city_.getID())
		
		city_.kill()
	
	def testCityBeforeCity(self):
		deferredCity = city((0, 0))
		city_ = player(0).initCity(0, 0)
		
		self.assertEqual(deferredCity().getID(), city_.getID())
		
		city_.kill()
	
	def testWonderWithoutCities(self):
		city = wonder(iPyramids)
		self.assertEqual(city(), None)
	
	def testWonderWithoutWonder(self):
		city = wonder(iPyramids)
		city_ = player(0).initCity(0, 0)
		
		self.assertEqual(city(), None)
		
		city_.kill()
	
	def testWonderWithWonder(self):
		city = wonder(iPyramids)
		city_ = player(0).initCity(0, 0)
		city_.setHasRealBuilding(iPyramids, True)
		
		self.assertEqual(city().getID(), city_.getID())
		
		city_.kill()


class TestAggregate(ExtendedTestCase):

	def testEvalSum(self):
		agg = sum(i for i in xrange(3))
		result = agg.eval(lambda x: x*x)
		
		self.assertEqual(result, 5)
	
	def testEvalAverage(self):
		agg = avg(i for i in xrange(5))
		result = agg.eval(lambda x: x)
		
		self.assertEqual(result, 2.0)
		
	def testEvalAverageEmpty(self):
		agg = avg(i for i in xrange(0))
		result = agg.eval(lambda x: x)
		
		self.assertEqual(result, 0.0)
	
	def testEvalDifferent(self):
		agg = different(i for i in xrange(3))
		result = agg.eval(lambda x: 1)
		
		self.assertEqual(result, 3)
	
	def testEvalDifferentRegardlessOfValue(self):
		agg = different(i for i in xrange(3))
		result = agg.eval(lambda x: 100)
		
		self.assertEqual(result, 3)
	
	def testLazyItemsOnEval(self):
		agg = sum(i for i in xrange(3))
		self.assertEqual(agg._items, None)
		
		agg.eval(lambda x: x)
		self.assertEqual(agg._items, [0, 1, 2])
	
	def testLazyItemsOnIter(self):
		agg = sum(i for i in xrange(3))
		self.assertEqual(agg._items, None)
		
		for i in agg:
			continue
		self.assertEqual(agg._items, [0, 1, 2])
	
	def testLazyItemsOnContains(self):
		agg = sum(i for i in xrange(3))
		self.assertEqual(agg._items, None)
		
		contained = 0 in agg
		self.assertEqual(agg._items, [0, 1, 2])


class TestArguments(ExtendedTestCase):

	def testObjective(self):
		arguments = Arguments(objectives=[(1,)])
		
		iterated = [x for x in arguments]
		
		self.assertEqual(iterated, [(1,)])
	
	def testObjectives(self):
		arguments = Arguments(objectives=[(1,), (2,), (3,)])
		
		iterated = [x for x in arguments]
		
		self.assertEqual(iterated, [(1,), (2,), (3,)])
	
	def testSubject(self):
		arguments = Arguments(objectives=[], subject="subject")
		
		iterated = [x for x in arguments]
		
		self.assertEqual(iterated, [("subject",)])
	
	def testPlayer(self):
		arguments = Arguments([])
		arguments.setPlayer(0)
		
		iterated = [x for x in arguments]
		
		self.assertEqual(iterated, [(0,)])
	
	def testSubjectAndObjectives(self):
		arguments = Arguments(subject="subject", objectives=[(1,), (2,), (3,)])
		
		iterated = [x for x in arguments]
		
		self.assertEqual(iterated, [("subject", 1), ("subject", 2), ("subject", 3)])
	
	def testSubjectAndPlayer(self):
		arguments = Arguments(objectives=[], subject="subject")
		arguments.setPlayer(0)
		
		iterated = [x for x in arguments]
		
		self.assertEqual(iterated, [("subject", 0)])
	
	def testObjectivesAndPlayer(self):
		arguments = Arguments(objectives=[(1,), (2,), (3,)])
		arguments.setPlayer(0)
		
		iterated = [x for x in arguments]
		
		self.assertEqual(iterated, [(1, 0), (2, 0), (3, 0)])
	
	def testSubjectAndObjectivesAndPlayer(self):
		arguments = Arguments(subject="subject", objectives=[(1,), (2,), (3,)])
		arguments.setPlayer(0)
		
		iterated = [x for x in arguments]
		
		self.assertEqual(iterated, [("subject", 1, 0), ("subject", 2, 0), ("subject", 3, 0)])
	
	def testResolvesDeferred(self):
		deferred = Deferred(int, lambda p: 42)
		arguments = Arguments(objectives=[(1, deferred), (2, deferred)])
		
		iterated = [x for x in arguments]
		
		self.assertEqual(iterated, [(1, 42), (2, 42)])


class TestArgumentProcessor(ExtendedTestCase):

	def testReturnsArguments(self):
		types = ArgumentProcessor([int])
		
		result = types.process((0,))
		self.assertType(result, Arguments)
	
	def testSubjectNone(self):
		types = ArgumentProcessor([int])
		
		result = types.process((0,))
		self.assertEqual(result.subject, None)
		
	def testObjectivesEmptyList(self):
		types = ArgumentProcessor(subject_type=CyCity)
		
		result = types.process(city((100, 100)))
		self.assertEqual(result.objectives, [])
	
	def testObjectivesNotList(self):
		self.assertRaises(ValueError, ArgumentProcessor, int)

	def testProcessSingleType(self):
		types = ArgumentProcessor([int])
		
		result = types.process((0,))
		self.assertEqual(result.objectives, [(0,)])
	
	def testProcessMultipleSingleTypes(self):
		types = ArgumentProcessor([int])
		
		result = types.process((0,), (1,), (2,))
		self.assertEqual(result.objectives, [(0,), (1,), (2,)])
	
	def testProcessMultipleSingleTypesFlat(self):
		types = ArgumentProcessor([int])
		
		result = types.process(0, 1, 2)
		self.assertEqual(result.objectives, [(0,), (1,), (2,)])
	
	def testInvalidType(self):
		types = ArgumentProcessor([str])
		
		self.assertRaises(ValueError, types.process, 0)
	
	def testInvalidTypeAfterValid(self):
		types = ArgumentProcessor([str])
		
		self.assertRaises(ValueError, types.process, "0", "1", 2)
	
	def testInvalidLengthTooLong(self):
		types = ArgumentProcessor([int])
		
		self.assertRaises(ValueError, types.process, (0, 1), (2, 3))
	
	def testEmptyInput(self):
		types = ArgumentProcessor([str])
		
		self.assertRaises(ValueError, types.process)
	
	def testProcessDoubleType(self):
		types = ArgumentProcessor([int, str])
		
		result = types.process((1, "1"), (2, "2"))
		self.assertEqual(result.objectives, [(1, "1"), (2, "2")])
	
	def testProcessInvalidLengthTooShort(self):
		types = ArgumentProcessor([int, str])
		
		self.assertRaises(ValueError, types.process, (0,), (1,))
	
	def testProcessTooShortFlat(self):
		types = ArgumentProcessor([str, str])
		
		self.assertRaises(ValueError, types.process, "0")
	
	def testProcessTooLongFlat(self):
		types = ArgumentProcessor([str, str])
		
		self.assertRaises(ValueError, types.process, "0", "1", "2")
	
	def testDefaultIntValue(self):
		types = ArgumentProcessor([int])
		
		result = types.process()
		self.assertEqual(result.objectives, [(1,)])
	
	def testDefaultIntValueInMultiple(self):
		types = ArgumentProcessor([int, int])
		
		result = types.process((1,), (2,), (3,))
		self.assertEqual(result.objectives, [(1, 1), (2, 1), (3, 1)])
	
	def testDefaultIntValueWhenLonger(self):
		types = ArgumentProcessor([int, int])
		
		self.assertRaises(ValueError, types.process, (1, 2, 3))
		
	def testIntValidTypeForInfoClass(self):
		types = ArgumentProcessor([CvBuildingInfo])
		
		result = types.process(1, 2, 3)
		self.assertEqual(result.objectives, [(1,), (2,), (3,)])
	
	def testAggregateValidTypeForInfoClass(self):
		types = ArgumentProcessor([CvBuildingInfo])
		
		result = types.process(sum(i for i in xrange(3)))
		self.assertType(result, Arguments)
		
		objectives = result.objectives
		self.assertType(objectives, list)
		self.assertEqual(len(objectives), 1)
		self.assertType(objectives[0], tuple)
		self.assertEqual(len(objectives[0]), 1)
		self.assertType(objectives[0][0], Aggregate)
	
	def testDefaultPlayerValue(self):
		types = ArgumentProcessor([Players])
		
		result = types.process()
		self.assertEqual(result.objectives, [(players.major().alive(),)])
	
	def testCityType(self):
		types = ArgumentProcessor(subject_type=CyCity)
		
		result = types.process(city((100, 100)))
		self.assertType(result, Arguments)
		self.assertType(result.subject, Deferred)
		
		objectives = result.objectives
		self.assertType(objectives, list)
		self.assertEqual(len(objectives), 0)
	
	def testCityTypeFailsWhenMissing(self):
		types = ArgumentProcessor(subject_type=CyCity)
		
		self.assertRaises(ValueError, types.process)
	
	def testCityTypeFailsWithDifferentArgument(self):
		types = ArgumentProcessor(subject_type=CyCity)
		
		self.assertRaises(ValueError, types.process, 1)
	
	def testCityOnlyExpectedFirst(self):
		types = ArgumentProcessor([str, int], CyCity)
		
		result = types.process(city((100, 100)), ("1", 1), ("2", 2), ("3", 3))
		self.assertType(result, Arguments)
		self.assertType(result.subject, Deferred)
		
		objectives = result.objectives
		self.assertType(objectives, list)
		self.assertEqual(len(objectives), 3)
		
		for objective in objectives:
			self.assertType(objective[0], str)
			self.assertType(objective[1], int)
	
	def testCityCannotBeSuppliedTwice(self):
		types = ArgumentProcessor([str, int], CyCity)
		
		self.assertRaises(ValueError, types.process, city((100, 100)), city((50, 50)), ("1", 1))
	
	def testObjectiveSplit(self):
		types = ArgumentProcessor([int, int, int], objective_split=1)
		
		result = types.process((1, 2, 3), (4, 5, 6), (7, 8, 9))
		self.assertEqual(result.objectives, [((1, 2), (3,)), ((4, 5), (6,)), ((7, 8), (9,))])
		
	def testObjectSplitDouble(self):
		types = ArgumentProcessor([int, int, int], objective_split=2)
		
		result = types.process((1, 2, 3), (4, 5, 6), (7, 8, 9))
		self.assertEqual(result.objectives, [((1,), (2, 3)), ((4,), (5, 6)), ((7,), (8, 9))])
	
	def testPrefersSingleOverDoubleWithDefault(self):
		types = ArgumentProcessor([str, int])
		
		result = types.process("string", 10)
		self.assertEqual(result.objectives, [("string", 10)])
	
	def testListTransform(self):
		types = ArgumentProcessor([list])
		
		result = types.process([1, 2, 3])
		self.assertEqual(result.objectives, [((1, 2, 3),)])
	
	def testAggregateIsValidForPlots(self):
		types = ArgumentProcessor([Plots])
		
		result = types.process(sum([plots.of([(61, 31)])]))
		self.assertEqual(len(result.objectives), 1)
		self.assertType(result.objectives[0], tuple)
		self.assertEqual(len(result.objectives[0]), 1)
		self.assertType(result.objectives[0][0], Aggregate)


class TestArgumentProcessorBuilder(ExtendedTestCase):

	def setUp(self):
		self.builder = ArgumentProcessorBuilder()
		
	def testUninitialized(self):
		self.assertEqual(self.builder.initialized(), False)
	
	def testInitialized(self):
		self.assertEqual(self.builder.withObjectiveTypes(int).initialized(), True)
	
	def testWithObjectiveType(self):
		types = self.builder.withObjectiveTypes(int).build()
		
		self.assertEqual(types.objective_types, [int])
	
	def testWithObjectiveTypes(self):
		types = self.builder.withObjectiveTypes(int, int).build()
		
		self.assertEqual(types.objective_types, [int, int])
	
	def testWithSubjectType(self):
		types = self.builder.withSubjectType(CyCity).build()
		
		self.assertEqual(types.subject_type, CyCity)
	
	def testWithObjectiveSplit(self):
		types = self.builder.withObjectiveTypes(int, int).withObjectiveSplit(1).build()
		
		self.assertEqual(types.objective_split, 1)
		

class DummyProcessor(object):
	def process(self, *args):
		return Arguments([], None)

class TestGoal(BaseGoal):

	types = DummyProcessor()
	
	def __init__(self, *arguments):
		super(TestGoal, self).__init__(*arguments)
		
		self.condition_value = True
	
	def condition(self, *arguments):
		return self.condition_value
	
	def display(self):
		return str(self.condition())


class TestBaseGoal(ExtendedTestCase):

	def setUp(self):
		self.goal = TestGoal()
	
	def testIncludeOwner(self):
		def condition_value():
			return True
		TestGoal = Count.objective(int).include_owner.func(condition_value).subclass("TestGoal")
		iPlayer = 21
		
		goal = TestGoal(0, 1, 2)
		goal.activate(iPlayer)
		
		self.assertEqual(goal.owner_included, True)
		self.assertEqual(goal.arguments.iPlayer, iPlayer)
	
	def testNotIncludeOwner(self):
		iPlayer = 20
		
		goal = TestGoal(0, 1, 2)
		goal.activate(iPlayer)
		
		self.assertEqual(goal.owner_included, False)
		self.assertEqual(goal.arguments.iPlayer, None)
	
	def testInitialState(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		self.assertEqual(self.goal.iPlayer, None)
		self.assertEqual(self.goal._player, None)
		self.assertEqual(self.goal._team, None)
		self.assertEqual(self.goal.callback, None)
	
	def testActivate(self):
		self.goal.activate(0)
		
		self.assertEqual(self.goal.iPlayer, 0)
		self.assertEqual(self.goal._player.getID(), 0)
		self.assertEqual(self.goal._team.getID(), 0)
		self.assertEqual(self.goal.callback, None)
	
	def testActivateWithCallback(self):
		def callback():
			pass
		
		self.goal.activate(0, callback)
		
		self.assertEqual(self.goal.callback, callback)
	
	def testPossiblePossible(self):
		self.assertEqual(self.goal.possible(), True)
	
	def testPossibleSucceeded(self):
		self.goal.state = SUCCESS
		self.assertEqual(self.goal.possible(), False)
	
	def testPossibleFailed(self):
		self.goal.state = FAILURE
		self.assertEqual(self.goal.possible(), False)
	
	def testSucceed(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.succeed()
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testFail(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.fail()
		self.assertEqual(self.goal.state, FAILURE)
	
	def testSetStateUnchanged(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.setState(POSSIBLE)
		self.assertEqual(self.goal.state, POSSIBLE)
	
	def testSetStateChanged(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.setState(SUCCESS)
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testSetStateChangedCallback(self):
		class Callable(object):
			def __init__(self):
				self.called = None
			def call(self, called):
				self.called = called
				
		callable = Callable()
		
		self.goal.activate(0, callable.call)
		self.goal.setState(SUCCESS)
		self.assertEqual(callable.called, self.goal)
	
	def testSetStateUnchangedCallback(self):
		class Callable(object):
			def __init__(self):
				self.called = None
			def call(self, called):
				self.called = called
				
		callable = Callable()
		
		self.goal.activate(0, callable.call)
		self.goal.setState(POSSIBLE)
		self.assertEqual(callable.called, None)

	def testExpirePossible(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.expire()
		self.assertEqual(self.goal.state, FAILURE)
	
	def testExpireSuccess(self):
		self.goal.state = SUCCESS
		self.goal.expire()
		
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testExpireFailure(self):
		self.goal.state = FAILURE
		self.goal.expire()
		
		self.assertEqual(self.goal.state, FAILURE)
	
	def testNonzero(self):
		self.assertEqual(bool(self.goal), True)
	
	def testNonzeroWithFailedCondition(self):
		self.goal.condition_value = False
		
		self.assertEqual(bool(self.goal), False)
	
	def testToString(self):
		self.assertEqual(str(self.goal), "True")
	
	def testCheckPossible(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.check()
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testCheckFailure(self):
		self.goal.state = FAILURE
		
		self.goal.check()
		self.assertEqual(self.goal.state, FAILURE)
	
	def testCheckSuccess(self):
		self.goal.state = SUCCESS
		
		self.goal.check()
		self.assertEqual(self.goal.state, SUCCESS)
		
	def testCheckFailingPossible(self):
		self.goal.condition_value = False
		
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.check()
		self.assertEqual(self.goal.state, POSSIBLE)
	
	def testCheckFailingFailure(self):
		self.goal.condition_value = False
		self.goal.state = FAILURE
		
		self.goal.check()
		self.assertEqual(self.goal.state, FAILURE)
	
	def testCheckFailingSuccess(self):
		self.goal.condition_value = False
		self.goal.state = SUCCESS
		
		self.goal.check()
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testFinalCheckPossible(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.finalCheck()
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testFinalCheckFailure(self):
		self.goal.state = FAILURE
		
		self.goal.finalCheck()
		self.assertEqual(self.goal.state, FAILURE)
	
	def testFinalCheckSuccess(self):
		self.goal.state = SUCCESS
		
		self.goal.finalCheck()
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testFinalCheckFailingPossible(self):
		self.goal.condition_value = False
		
		self.assertEqual(self.goal.state, POSSIBLE)
		
		self.goal.finalCheck()
		self.assertEqual(self.goal.state, FAILURE)
	
	def testFinalCheckFailingFailure(self):
		self.goal.condition_value = False
		self.goal.state = FAILURE
		
		self.goal.finalCheck()
		self.assertEqual(self.goal.state, FAILURE)
	
	def testFinalCheckFailingSuccess(self):
		self.goal.condition_value = False
		self.goal.state = SUCCESS
		
		self.goal.finalCheck()
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testAtSuccess(self):
		self.goal.at(-3000)
		self.goal.condition_value = True
		self.goal.activate(0)
		
		self.assertEqual(self.goal.state, POSSIBLE)
		
		events.fireEvent("BeginPlayerTurn", 0, 0)
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testAtFailure(self):
		self.goal.at(-3000)
		self.goal.condition_value = False
		self.goal.activate(0)
		
		self.assertEqual(self.goal.state, POSSIBLE)
		
		events.fireEvent("BeginPlayerTurn", 0, 0)
		self.assertEqual(self.goal.state, FAILURE)
	
	def testAtDifferentTurn(self):
		self.goal.at(-3000)
		self.goal.condition_value = True
		self.goal.activate(0)
		
		self.assertEqual(self.goal.state, POSSIBLE)
		
		events.fireEvent("BeginPlayerTurn", 1, 0)
		self.assertEqual(self.goal.state, POSSIBLE)
	
	def testBy(self):
		self.goal.by(-3000)
		self.goal.activate(0)
		
		self.assertEqual(self.goal.state, POSSIBLE)
		
		events.fireEvent("BeginPlayerTurn", 0, 0)
		self.assertEqual(self.goal.state, FAILURE)
		
	def testByAfterSuccess(self):
		self.goal.by(-3000)
		self.goal.state = SUCCESS
		self.goal.activate(0)
		
		self.assertEqual(self.goal.state, SUCCESS)
		
		events.fireEvent("BeginPlayerTurn", 0, 0)
		self.assertEqual(self.goal.state, SUCCESS)
	
	def testByDifferentTurn(self):
		self.goal.by(-3000)
		self.goal.activate(0)
		
		self.assertEqual(self.goal.state, POSSIBLE)
		
		events.fireEvent("BeginPlayerTurn", 1, 0)
		self.assertEqual(self.goal.state, POSSIBLE)
	
	def testTurnly(self):
		goal = TestGoal.turnly.subclass("SubGoal")()
		goal.condition_value = True
		goal.activate(0)
		
		self.assertEqual(goal.state, POSSIBLE)
		
		events.fireEvent("BeginPlayerTurn", 0, 0)
		self.assertEqual(goal.state, SUCCESS)


class TestConditionGoals(ExtendedTestCase):

	def testControlAllCities(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		city3 = player(0).initCity(65, 31)
		
		self.assertEqual(bool(goal), True)
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testControlSomeCities(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		city3 = player(1).initCity(65, 31)
		
		self.assertEqual(bool(goal), False)
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testControlNoCities(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(1).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		city3 = player(1).initCity(65, 31)
		
		self.assertEqual(bool(goal), False)
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testControlEmpty(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testControlOutside(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city = player(0).initCity(59, 31)
		
		self.assertEqual(bool(goal), False)
		
		city.kill()
	
	def testControlAllOfMultiple(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35)), plots.rectangle((66, 30), (70, 35)))
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(69, 31)
		
		self.assertEqual(bool(goal), True)
		
		city1.kill()
		city2.kill()
	
	def testControlSomeOfMultiple(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35)), plots.rectangle((66, 30), (70, 35)))
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(1).initCity(69, 31)
		
		self.assertEqual(bool(goal), False)
		
		city1.kill()
		city2.kill()

	def testControlOrVassalizeAllCities(self):
		goal = Condition.controlOrVassalize(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		city3 = player(0).initCity(65, 31)
		
		self.assertEqual(bool(goal), True)
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testControlOrVassalizeSomeCities(self):
		goal = Condition.controlOrVassalize(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		city3 = player(1).initCity(65, 31)
		
		self.assertEqual(bool(goal), False)
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testControlOrVassalizeNoCities(self):
		goal = Condition.controlOrVassalize(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(1).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		city3 = player(1).initCity(65, 31)
		
		self.assertEqual(bool(goal), False)
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testControlOrVassalizeAllVassal(self):
		goal = Condition.controlOrVassalize(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(1).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		city3 = player(1).initCity(65, 31)
		
		team(1).setVassal(team(0).getID(), True, False)
		
		self.assertEqual(bool(goal), True)
		
		city1.kill()
		city2.kill()
		city3.kill()
		
		team(1).setVassal(team(0).getID(), False, False)
	
	def testControlOrVassalizeOneVassal(self):
		goal = Condition.controlOrVassalize(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(1).initCity(61, 31)
		city2 = player(2).initCity(63, 31)
		city3 = player(2).initCity(65, 31)
		
		team(1).setVassal(team(0).getID(), True, False)
		
		self.assertEqual(bool(goal), False)
		
		city1.kill()
		city2.kill()
		city3.kill()
		
		team(1).setVassal(team(0).getID(), False, False)
	
	def testSettleWhenFounded(self):
		goal = Condition.settle(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		events.fireEvent("cityBuilt", city)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(goal.state, SUCCESS)
		
		city.kill()
		
		goal.deactivate()
	
	def testSettleWhenConquered(self):
		goal = Condition.settle(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city = player(1).initCity(61, 31)
		events.fireEvent("cityBuilt", city)
		
		player(0).acquireCity(city, True, False)
		city = city_(61, 31)
		
		self.assertEqual(city.getOwner(), 0)
		self.assertEqual(bool(goal), False)
		self.assertEqual(goal.state, POSSIBLE)
		
		city.kill()
		
		goal.deactivate()
	
	def testSettleWhenTraded(self):
		goal = Condition.settle(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city = player(1).initCity(61, 31)
		events.fireEvent("cityBuilt", city)
		
		player(0).acquireCity(city, False, True)
		city = city_(61, 31)
		
		self.assertEqual(city.getOwner(), 0)
		self.assertEqual(bool(goal), False)
		self.assertEqual(goal.state, POSSIBLE)
		
		city.kill()
		
		goal.deactivate()
	
	def testWonderOwned(self):
		goal = Condition.wonder(iPyramids)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPyramids, True)
		
		self.assertEqual(bool(goal), True)
		
		city.kill()
		
		goal.deactivate()
	
	def testWonderNonExistent(self):
		goal = Condition.wonder(iPyramids)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		
		goal.deactivate()
		
	def testWonderDifferentOwner(self):
		goal = Condition.wonder(iPyramids)
		goal.activate(0)
		
		city = player(1).initCity(61, 31)
		city.setHasRealBuilding(iPyramids, True)
		
		self.assertEqual(bool(goal), False)
		
		city.kill()
		
		goal.deactivate()
	
	def testMultipleWondersNone(self):
		goal = Condition.wonder(iPyramids, iParthenon, iColossus)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		
		goal.deactivate()
	
	def testMultipleWondersSome(self):
		goal = Condition.wonder(iPyramids, iParthenon, iColossus)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		for iWonder in [iPyramids, iParthenon]:
			city.setHasRealBuilding(iWonder, True)
		
		self.assertEqual(bool(goal), False)
		
		city.kill()
		
		goal.deactivate()
	
	def testMultipleWondersAll(self):
		goal = Condition.wonder(iPyramids, iParthenon, iColossus)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		for iWonder in [iPyramids, iParthenon, iColossus]:
			city.setHasRealBuilding(iWonder, True)
		
		self.assertEqual(bool(goal), True)
		
		city.kill()
		
		goal.deactivate()
	
	def testWonderExpired(self):
		goal = Condition.wonder(iPyramids)
		goal.activate(0)
		
		city = player(1).initCity(61, 31)
		city.setHasRealBuilding(iPyramids, True)
		
		self.assertEqual(goal.state, POSSIBLE)
		
		events.fireEvent("buildingBuilt", city, iPyramids)
		
		self.assertEqual(goal.state, FAILURE)
		
		city.kill()
		
		goal.deactivate()
	
	def testWonderCheck(self):
		goal = Condition.wonder(iPyramids)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPyramids, True)
		
		self.assertEqual(goal.state, POSSIBLE)
		
		events.fireEvent("buildingBuilt", city, iPyramids)
		
		self.assertEqual(goal.state, SUCCESS)
		
		city.kill()
		
		goal.deactivate()
	
	def testProjectNonExistent(self):
		goal = Condition.project(iTheInternet)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testProjectCompleted(self):
		goal = Condition.project(iTheInternet)
		goal.activate(0)
		
		team(0).changeProjectCount(iTheInternet, 1)
		
		self.assertEqual(bool(goal), True)
		
		team(0).changeProjectCount(iTheInternet, -1)
	
	def testProjectCompletedOther(self):
		goal = Condition.project(iTheInternet)
		goal.activate(0)
		
		team(1).changeProjectCount(iTheInternet, 1)
		
		self.assertEqual(bool(goal), False)
		
		team(1).changeProjectCount(iTheInternet, -1)
	
	def testProjectCompletedMultipleSome(self):
		goal = Condition.project(iTheInternet, iHumanGenome, iSDI)
		goal.activate(0)
		
		team(0).changeProjectCount(iTheInternet, 1)
		team(0).changeProjectCount(iHumanGenome, 1)
		
		self.assertEqual(bool(goal), False)
		
		team(0).changeProjectCount(iTheInternet, -1)
		team(0).changeProjectCount(iHumanGenome, -1)
	
	def testProjectCompletedMultipleAll(self):
		goal = Condition.project(iTheInternet, iHumanGenome, iSDI)
		goal.activate(0)
		
		for iProject in [iTheInternet, iHumanGenome, iSDI]:
			team(0).changeProjectCount(iProject, 1)
		
		self.assertEqual(bool(goal), True)
		
		for iProject in [iTheInternet, iHumanGenome, iSDI]:
			team(0).changeProjectCount(iProject, -1)
	
	def testProjectCheckedOnEvent(self):
		goal = Condition.project(iTheInternet)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		team(0).changeProjectCount(iTheInternet, 1)
		
		events.fireEvent("projectBuilt", city, iTheInternet)
		
		self.assertEqual(goal.state, SUCCESS)
		
		city.kill()
		team(0).changeProjectCount(iTheInternet, -1)
	
	def testProjectExpiredOnEvent(self):
		goal = Condition.project(iTheInternet)
		goal.activate(0)
		
		city = player(1).initCity(61, 31)
		team(1).changeProjectCount(iTheInternet, 1)
		
		events.fireEvent("projectBuilt", city, iTheInternet)
		
		self.assertEqual(goal.state, FAILURE)
		
		city.kill()
		team(1).changeProjectCount(iTheInternet, -1)
	
	def testRouteNone(self):
		goal = Condition.route(plots.of([(60, 30), (61, 30), (62, 30)]), iRouteRoad)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testRouteSome(self):
		area = plots.of([(60, 30), (61, 30), (62, 30)])
		goal = Condition.route(area, iRouteRoad)
		goal.activate(0)
		
		for plot in area.without((60, 30)):
			plot.setRouteType(iRouteRoad)
		
		self.assertEqual(bool(goal), False)
		
		for plot in area.without((60, 30)):
			plot.setRouteType(-1)
	
	def testRouteAll(self):
		area = plots.of([(60, 30), (61, 30), (62, 30)])
		goal = Condition.route(area, iRouteRoad)
		goal.activate(0)
		
		for plot in area:
			plot.setRouteType(iRouteRoad)
		
		self.assertEqual(bool(goal), True)
		
		for plot in area:
			plot.setRouteType(-1)
			
	def testNoStateReligionSome(self):
		goal = Condition.noStateReligion(plots.rectangle((60, 30), (65, 35)), iCatholicism)
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		
		player(0).setLastStateReligion(iCatholicism)
		
		self.assertEqual(bool(goal), False)
		
		city1.kill()
		city2.kill()
		
		player(0).setLastStateReligion(-1)
	
	def testNoStateReligionAll(self):
		goal = Condition.noStateReligion(plots.rectangle((60, 30), (65, 35)), iCatholicism)
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		
		self.assertEqual(bool(goal), True)
		
		city1.kill()
		city2.kill()
	
	def testCultureCoveredNone(self):
		goal = Condition.cultureCovered(plots.of([(60, 30), (61, 30), (62, 30)]))
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testCultureCoveredSome(self):
		goal = Condition.cultureCovered(plots.of([(60, 30), (61, 30), (62, 30)]))
		goal.activate(0)
		
		plot(60, 30).setOwner(0)
		
		self.assertEqual(bool(goal), False)
		
		plot(60, 30).setOwner(-1)
	
	def testCultureCoveredAll(self):
		area = plots.of([(60, 30), (61, 30), (62, 30)])
		goal = Condition.cultureCovered(area)
		goal.activate(0)
		
		for plot in area:
			plot.setOwner(0)
		
		self.assertEqual(bool(goal), True)
		
		for plot in area:
			plot.setOwner(-1)
	
	def testCultureCoveredOther(self):
		area = plots.of([(60, 30), (61, 30), (62, 30)])
		goal = Condition.cultureCovered(area)
		goal.activate(0)
		
		for plot in area:
			plot.setOwner(1)
		
		self.assertEqual(bool(goal), False)
		
		for plot in area:
			plot.setOwner(-1)
	
	def testNotCommunist(self):
		goal = Condition.communist()
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testCommunist(self):
		goal = Condition.communist()
		goal.activate(0)
		
		player(0).setCivics(iCivicsEconomy, iCentralPlanning)
		
		self.assertEqual(bool(goal), True)
		
		player(0).setCivics(iCivicsEconomy, iRedistribution)
	
	def testNoForeignCities(self):
		goal = Condition.noForeignCities(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		
		self.assertEqual(bool(goal), True)
	
		city.kill()
	
	def testNoForeignCitiesNoCities(self):
		goal = Condition.noForeignCities(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testNoForeignCitiesMinor(self):
		goal = Condition.noForeignCities(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city = player(iIndependent).initCity(61, 31)
		
		self.assertEqual(bool(goal), True)
		
		city.kill()
	
	def testNoForeignCitiesOther(self):
		goal = Condition.noForeignCities(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		self.assertEqual(bool(goal), False)
		
		city0.kill()
		city1.kill()
	
	def testNoForeignCitiesOnly(self):
		goal = Condition.noForeignCities(plots.rectangle((60, 30), (65, 35))).only([iBabylonia])
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(2).initCity(63, 31)
		
		self.assertEqual(bool(goal), True)
		
		city0.kill()
		city1.kill()
	
	def testNoForeignCitiesOnlyOther(self):
		goal = Condition.noForeignCities(plots.rectangle((60, 30), (65, 35))).only([iBabylonia])
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		self.assertEqual(bool(goal), False)
		
		city0.kill()
		city1.kill()
	
	def testNoForeignCitiesExcluding(self):
		goal = Condition.noForeignCities(plots.rectangle((60, 30), (65, 35))).excluding([iBabylonia])
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		self.assertEqual(bool(goal), True)
		
		city0.kill()
		city1.kill()
	
	def testNoForeignCitiesExcludingWith(self):
		goal = Condition.noForeignCities(plots.rectangle((60, 30), (65, 35))).excluding([iBabylonia])
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(2).initCity(63, 31)
		
		self.assertEqual(bool(goal), False)
		
		city0.kill()
		city1.kill()
	
	def testTradeConnectionFalse(self):
		goal = Condition.tradeConnection()
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		
		goal.deactivate()
	
	def testTradeConnection(self):
		goal = Condition.tradeConnection()
		goal.activate(0)
		
		team(1).meet(0, False)
		team(1).setOpenBorders(0, True)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		self.assertEqual(bool(goal), True)
		
		team(1).cutContact(0)
		team(1).setOpenBorders(0, False)
		
		city0.kill()
		city1.kill()
		
		for p in plots.rectangle((61, 31), (63, 31)):
			p.setRouteType(-1)
		
		goal.deactivate()
	
	def testMoreReligion(self):
		goal = Condition.moreReligion(plots.rectangle((60, 30), (65, 35)), iOrthodoxy, iCatholicism)
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		city2 = player(2).initCity(65, 31)
		
		city0.setHasReligion(iOrthodoxy, True, False, False)
		city1.setHasReligion(iOrthodoxy, True, False, False)
		city2.setHasReligion(iCatholicism, True, False, False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "2 / 1")
		
		for city in [city0, city1, city2]:
			city.kill()
	
	def testMoreReligionEqual(self):
		goal = Condition.moreReligion(plots.rectangle((60, 30), (65, 35)), iOrthodoxy, iCatholicism)
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		city0.setHasReligion(iOrthodoxy, True, False, False)
		city1.setHasReligion(iCatholicism, True, False, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 1")
		
		city0.kill()
		city1.kill()
	
	def testMoreReligionLess(self):
		goal = Condition.moreReligion(plots.rectangle((60, 30), (65, 35)), iOrthodoxy, iCatholicism)
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		
		city0.setHasReligion(iCatholicism, True, False, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		
		city0.kill()
	
	def testMoreReligionOutside(self):
		goal = Condition.moreReligion(plots.rectangle((60, 30), (65, 35)), iOrthodoxy, iCatholicism)
		goal.activate(0)
		
		city0 = player(0).initCity(25, 25)
		city0.setHasReligion(iOrthodoxy, True, False, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 0")
		
		city0.kill()
	
	def testMoreCulture(self):
		goal = Condition.moreCulture()
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		city2 = player(2).initCity(65, 31)
		
		city0.setCulture(0, 1000, False)
		city1.setCulture(1, 500, False)
		city2.setCulture(2, 100, False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1000 / 600")
		
		for city in [city0, city1, city2]:
			city.kill()
	
	def testMoreCultureLess(self):
		goal = Condition.moreCulture()
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		city2 = player(2).initCity(65, 31)
		
		city0.setCulture(0, 1000, False)
		city1.setCulture(1, 600, False)
		city2.setCulture(2, 600, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1000 / 1200")
		
		for city in [city0, city1, city2]:
			city.kill()
	
	def testMoreCultureThan(self):
		goal = Condition.moreCulture().than([iBabylonia])
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		city2 = player(2).initCity(65, 31)
		
		city0.setCulture(0, 1000, False)
		city1.setCulture(1, 600, False)
		city2.setCulture(2, 600, False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1000 / 600")
		
		for city in [city0, city1, city2]:
			city.kill()


class TestCountGoals(ExtendedTestCase):

	def setUp(self):
		for plot in plots.all():
			plot.resetCultureConversion()
		
		self.assertEqual(cities.all().count(), 0)

	def tearDown(self):
		self.assertEqual(cities.all().count(), 0)

	def testBuildingNone(self):
		goal = Count.building(iGranary, 3)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 3")
		
		goal.deactivate()
	
	def testBuildingSome(self):
		goal = Count.building(iGranary, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasRealBuilding(iGranary, True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "2 / 3")
		
		for tile in tiles:
			city_(tile).kill()
		
		goal.deactivate()
	
	def testBuildingAll(self):
		goal = Count.building(iGranary, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasRealBuilding(iGranary, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 3")
		
		for tile in tiles:
			city_(tile).kill()
		
		goal.deactivate()
			
	def testBuildingMore(self):
		goal = Count.building(iGranary, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31), (67, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasRealBuilding(iGranary, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "4 / 3")
		
		for tile in tiles:
			city_(tile).kill()
		
		goal.deactivate()
	
	def testBuildingMultiplePartial(self):
		goal = Count.building((iGranary, 3), (iBarracks, 2))
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasRealBuilding(iGranary, True)
			city.setHasRealBuilding(iBarracks, True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), '\n'.join(["2 / 3", "2 / 2"]))
		
		for tile in tiles:
			city_(tile).kill()
		
		goal.deactivate()
	
	def testBuildingMultipleAll(self):
		goal = Count.building((iGranary, 3), (iBarracks, 2))
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasRealBuilding(iGranary, True)
			city.setHasRealBuilding(iBarracks, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), '\n'.join(["3 / 3", "3 / 2"]))
		
		for tile in tiles:
			city_(tile).kill()
		
		goal.deactivate()
	
	# TODO: we need a test with sum() and event handling
	def testBuildingSum(self):
		goal = Count.building(sum([iGranary, iBarracks, iLibrary]), 3)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		for iBuilding in [iGranary, iBarracks, iLibrary]:
			city.setHasRealBuilding(iBuilding, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 3")
		
		city.kill()
		
		goal.deactivate()
	
	def testBuildingCheck(self):
		goal = Count.building(iGranary, 1)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iGranary, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(goal.state, POSSIBLE)
		
		events.fireEvent("buildingBuilt", city, iGranary)
		
		self.assertEqual(goal.state, SUCCESS)
		
		city.kill()
		
		goal.deactivate()
	
	def testBuildingCheckDifferentBuilding(self):
		goal = Count.building(iGranary, 1)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iGranary, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(goal.state, POSSIBLE)
		
		events.fireEvent("buildingBuilt", city, iBarracks)
		
		self.assertEqual(goal.state, POSSIBLE)
		
		city.kill()
		
		goal.deactivate()
	
	def testBuildingCheckCityAcquired(self):
		goal = Count.building(iGranary, 1)
		goal.activate(0)
		
		city = player(1).initCity(61, 31)
		city.setHasRealBuilding(iGranary, True)
		
		player(0).acquireCity(city, False, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(goal.state, SUCCESS)
		
		city_(61, 31).kill()
		
		goal.deactivate()
	
	def testBuildingDeferred(self):
		goal = Count.building(stateReligionBuilding(temple), 1)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iOrthodoxTemple, True)
		
		self.assertEqual(str(goal), "0 / 1")
		self.assertEqual(bool(goal), False)
		
		player(0).setLastStateReligion(iCatholicism)
		self.assertEqual(bool(goal), False)
		
		player(0).setLastStateReligion(iOrthodoxy)
		self.assertEqual(bool(goal), True)
		
		city.kill()
		
		goal.deactivate()
	
	def testBuildingUniqueInGoal(self):
		goal = Count.building(iObelisk, 1)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iObelisk, True)
		
		events.fireEvent("buildingBuilt", city, iObelisk)
		
		self.assertEqual(str(goal), "1 / 1")
		self.assertEqual(bool(goal), True)
		self.assertEqual(goal.state, SUCCESS)
		
		city.kill()
		
		goal.deactivate()
	
	def testBuildingUnique(self):
		goal = Count.building(iMonument, 1)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iObelisk, True)
		
		events.fireEvent("buildingBuilt", city, iObelisk)
		
		self.assertEqual(str(goal), "1 / 1")
		self.assertEqual(bool(goal), True)
		self.assertEqual(goal.state, SUCCESS)
		
		city.kill()
		
		goal.deactivate()
	
	def testCultureLess(self):
		goal = Count.culture(500)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 500")
		
		goal.deactivate()
	
	def testCultureMore(self):
		goal = Count.culture(500)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.changeCulture(0, 1000, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1000 / 500")
		
		city.kill()
		
		goal.deactivate()
	
	def testGoldLess(self):
		goal = Count.gold(500)
		goal.activate(0)
		
		player(0).changeGold(100)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "100 / 500")
		
		player(0).changeGold(-100)
	
	def testGoldMore(self):
		goal = Count.gold(500)
		goal.activate(0)
		
		player(0).changeGold(1000)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1000 / 500")
		
		player(0).changeGold(-1000)
	
	def testResourceLess(self):
		goal = Count.resource(iGold, 1)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
	
	def testResourceEnough(self):
		goal = Count.resource(iGold, 1)
		goal.activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		plot(61, 31).setBonusType(-1)
		city.kill()
	
	def testResourcesSome(self):
		goal = Count.resource((iGold, 1), (iSilver, 1))
		goal.activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
		self.assertEqual(player(0).getNumAvailableBonuses(iSilver), 0)
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), '\n'.join(["1 / 1", "0 / 1"]))
		
		plot(61, 31).setBonusType(-1)
		city.kill()
	
	def testResourcesAll(self):
		goal = Count.resource((iGold, 1), (iSilver, 1))
		goal.activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city1 = player(0).initCity(61, 31)
		city1.setHasRealBuilding(iPalace, True)
		
		plot(63, 31).setBonusType(iSilver)
		city2 = player(0).initCity(63, 31)
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
		self.assertEqual(player(0).getNumAvailableBonuses(iSilver), 1)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), '\n'.join(["1 / 1", "1 / 1"]))
		
		city1.kill()
		city2.kill()
		
		plot(61, 31).setBonusType(-1)
		plot(62, 31).setRouteType(-1)
		plot(63, 31).setBonusType(-1)
	
	def testResourceSum(self):
		goal = Count.resource(sum([iGold, iSilver]), 2)
		goal.activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city1 = player(0).initCity(61, 31)
		city1.setHasRealBuilding(iPalace, True)
		
		plot(63, 31).setBonusType(iSilver)
		city2 = player(0).initCity(63, 31)
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
		self.assertEqual(player(0).getNumAvailableBonuses(iSilver), 1)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "2 / 2")
		
		city1.kill()
		city2.kill()
		
		plot(61, 31).setBonusType(-1)
		plot(62, 31).setRouteType(-1)
		plot(63, 31).setBonusType(-1)
	
	def testControlledResourceLess(self):
		goal = Count.controlledResource(iGold, 1)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
	
	def testControlledResourceEnough(self):
		goal = Count.controlledResource(iGold, 1)
		goal.activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		plot(61, 31).setBonusType(-1)
		city.kill()
	
	def testControlledResourcesSome(self):
		goal = Count.controlledResource((iGold, 1), (iSilver, 1))
		goal.activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
		self.assertEqual(player(0).getNumAvailableBonuses(iSilver), 0)
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), '\n'.join(["1 / 1", "0 / 1"]))
		
		plot(61, 31).setBonusType(-1)
		city.kill()
	
	def testControlledResourcesAll(self):
		goal = Count.controlledResource((iGold, 1), (iSilver, 1))
		goal.activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city1 = player(0).initCity(61, 31)
		city1.setHasRealBuilding(iPalace, True)
		
		plot(63, 31).setBonusType(iSilver)
		city2 = player(0).initCity(63, 31)
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
		self.assertEqual(player(0).getNumAvailableBonuses(iSilver), 1)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), '\n'.join(["1 / 1", "1 / 1"]))
		
		city1.kill()
		city2.kill()
		
		plot(61, 31).setBonusType(-1)
		plot(62, 31).setRouteType(-1)
		plot(63, 31).setBonusType(-1)
	
	def testControlledResourceVassal(self):
		goal = Count.controlledResource(iGold, 1)
		goal.activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city = player(2).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		self.assertEqual(player(2).getNumAvailableBonuses(iGold), 1)
		
		team(2).setVassal(team(0).getID(), True, False)
		
		self.assertEqual(team(2).isVassal(team(0).getID()), True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		team(2).setVassal(team(0).getID(), False, False)
		city.kill()
	
	def testImprovementLess(self):
		goal = Count.improvement(iCottage, 3)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		tiles = [(60, 31), (62, 31)]
		for plot in plots.of(tiles):
			plot.setOwner(0)
			plot.setImprovementType(iCottage)
		
		self.assertEqual(player(0).getImprovementCount(iCottage), 2)
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "2 / 3")
		
		city.kill()
		for tile in plots.of(tiles):
			plot.setImprovementType(-1)
	
	def testImprovementMore(self):
		goal = Count.improvement(iCottage, 3)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		tiles = [(60, 31), (62, 31), (61, 30), (61, 32)]
		for plot in plots.of(tiles):
			plot.setOwner(0)
			plot.setImprovementType(iCottage)
		
		self.assertEqual(player(0).getImprovementCount(iCottage), 4)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "4 / 3")
		
		city.kill()
		for plot in plots.of(tiles):
			plot.setImprovementType(-1)
	
	def testPopulationLess(self):
		goal = Count.population(5)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setPopulation(3)
		
		self.assertEqual(player(0).getNumCities(), 1)
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "3 / 5")
		
		city.kill()
		
		goal.deactivate()
	
	def testPopulationMore(self):
		goal = Count.population(5)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setPopulation(10)
		
		self.assertEqual(player(0).getNumCities(), 1)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "10 / 5")
		
		city.kill()
		
		goal.deactivate()
	
	def testPopulationMultipleCities(self):
		goal = Count.population(5)
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		
		city1.setPopulation(3)
		city2.setPopulation(3)
		
		self.assertEqual(player(0).getNumCities(), 2)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "6 / 5")
		
		city1.kill()
		city2.kill()
		
		goal.deactivate()
	
	def testCorporationLess(self):
		goal = Count.corporation(iSilkRoute, 2)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasCorporation(iSilkRoute, True, False, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		self.assertEqual(goal.state, POSSIBLE)
		
		city.kill()
	
	def testCorporationMore(self):
		goal = Count.corporation(iSilkRoute, 2)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasCorporation(iSilkRoute, True, False, False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 2")
		self.assertEqual(goal.state, SUCCESS)
		
		for tile in tiles:
			city_(tile).kill()
	
	def testCorporationsSome(self):
		goal = Count.corporation((iSilkRoute, 2), (iTradingCompany, 2))
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		
		city1.setHasCorporation(iSilkRoute, True, False, False)
		city2.setHasCorporation(iSilkRoute, True, False, False)
		
		city1.setHasCorporation(iTradingCompany, True, False, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), '\n'.join(["2 / 2", "1 / 2"]))
		self.assertEqual(goal.state, POSSIBLE)
		
		city1.kill()
		city2.kill()
	
	def testCorporationsAll(self):
		goal = Count.corporation((iSilkRoute, 2), (iTradingCompany, 2))
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasCorporation(iSilkRoute, True, False, False)
			city.setHasCorporation(iTradingCompany, True, False, False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), '\n'.join(["2 / 2", "2 / 2"]))
		self.assertEqual(goal.state, SUCCESS)
		
		for tile in tiles:
			city_(tile).kill()
	
	def testUnitLess(self):
		goal = Count.unit(iSwordsman, 3)
		goal.activate(0)
		
		units = makeUnits(0, iSwordsman, (0, 0), 2)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "2 / 3")
		
		for unit in units:
			unit.kill(False, -1)
	
	def testUnitMore(self):
		goal = Count.unit(iSwordsman, 3)
		goal.activate(0)
		
		units = makeUnits(0, iSwordsman, (0, 0), 4)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "4 / 3")
		
		for unit in units:
			unit.kill(False, -1)
	
	def testUnitsSome(self):
		goal = Count.unit((iSwordsman, 3), (iArcher, 3))
		goal.activate(0)
		
		swordsmen = makeUnits(0, iSwordsman, (0, 0), 3)
		archers = makeUnits(0, iArcher, (0, 0), 2)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), '\n'.join(["3 / 3", "2 / 3"]))
		
		for unit in swordsmen:
			unit.kill(False, -1)
		
		for unit in archers:
			unit.kill(False, -1)
	
	def testUnitsAll(self):
		goal = Count.unit((iSwordsman, 3), (iArcher, 3))
		goal.activate(0)
		
		swordsmen = makeUnits(0, iSwordsman, (0, 0), 3)
		archers = makeUnits(0, iArcher, (0, 0), 3)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), '\n'.join(["3 / 3", "3 / 3"]))
		
		for unit in swordsmen:
			unit.kill(False, -1)
		
		for unit in archers:
			unit.kill(False, -1)
	
	def testUnitUnique(self):
		goal = Count.unit(iSwordsman, 3)
		goal.activate(0)
		
		units = makeUnits(0, iLegion, (0, 0), 3)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 3")
		
		for unit in units:
			unit.kill(False, -1)
	
	def testUnitUniqueRequirement(self):
		goal = Count.unit(iLegion, 3)
		goal.activate(0)
		
		units = makeUnits(0, iSwordsman, (0, 0), 3)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 3")
		
		for unit in units:
			unit.kill(False, -1)
	
	def testNumCitiesLess(self):
		goal = Count.numCities(plots.rectangle((60, 30), (65, 35)), 2)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		
		city.kill()
	
	def testNumCitiesMore(self):
		goal = Count.numCities(plots.rectangle((60, 30), (65, 35)), 2)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		for tile in tiles:
			player(0).initCity(*tile)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 2")
		
		for tile in tiles:
			city_(tile).kill()
	
	def testNumCitiesSum(self):
		goal = Count.numCities(sum([plots.rectangle((60, 30), (62, 35)), plots.rectangle((63, 30), (65, 35))]), 2)
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(64, 31)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "2 / 2")
		
		city1.kill()
		city2.kill()
	
	def testSettledCitiesAll(self):
		goal = Count.settledCities(plots.rectangle((60, 30), (65, 35)), 2)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31)]
		for tile in tiles:
			player(0).initCity(*tile)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "2 / 2")
		
		for tile in tiles:
			city_(tile).kill()
	
	def testSettledCitiesSome(self):
		goal = Count.settledCities(plots.rectangle((60, 30), (65, 35)), 2)
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		
		city2 = player(1).initCity(63, 31)
		player(0).acquireCity(city2, True, False)
		city2 = city_(63, 31)
		
		self.assertEqual(player(0).getNumCities(), 2)
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		
		city1.kill()
		city2.kill()
	
	def testConqueredCitiesAll(self):
		goal = Count.conqueredCities(2).inside(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(1).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		
		player(0).acquireCity(city1, True, False)
		player(0).acquireCity(city2, True, False)
		
		self.assertEqual(player(0).getNumCities(), 2)
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "2 / 2")
		
		city_(61, 31).kill()
		city_(63, 31).kill()
		
		goal.deactivate()
	
	def testConqueredCitiesSome(self):
		goal = Count.conqueredCities(2).inside(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		
		player(0).acquireCity(city2, True, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		
		city1.kill()
		city_(63, 31).kill()
		
		goal.deactivate()
	
	def testConqueredCitiesTraded(self):
		goal = Count.conqueredCities(1).inside(plots.rectangle((60, 30), (65, 35)))
		goal.activate(0)
		
		city = player(1).initCity(61, 31)
		
		player(0).acquireCity(city, False, True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		
		city_(61, 31).kill()
		
		goal.deactivate()
	
	def testConqueredCitiesCivs(self):
		goal = Count.conqueredCities(1).civs([iBabylonia])
		goal.activate(0)
		
		city = player(iBabylonia).initCity(61, 31)
		player(0).acquireCity(city, True, False)
		city = city_(61, 31)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		city.kill()
		
		goal.deactivate()
	
	def testConqueredCitiesCivsTrade(self):
		goal = Count.conqueredCities(1).civs([iBabylonia])
		goal.activate(0)
		
		city = player(iBabylonia).initCity(61, 31)
		player(0).acquireCity(city, False, True)
		city = city_(61, 31)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		
		city.kill()
		
		goal.deactivate()
	
	def testConqueredCitiesMultipleCivs(self):
		goal = Count.conqueredCities(3).civs([iBabylonia, iHarappa, iGreece])
		goal.activate(0)
		
		city1 = player(iBabylonia).initCity(61, 31)
		player(0).acquireCity(city1, True, False)
		city1 = city_(61, 31)
		
		city2 = player(iHarappa).initCity(63, 31)
		player(0).acquireCity(city2, True, False)
		city2 = city_(63, 31)
		
		city3 = player(iGreece).initCity(65, 31)
		player(0).acquireCity(city3, True, False)
		city3 = city_(65, 31)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 3")
		
		city1.kill()
		city2.kill()
		city3.kill()
		
		goal.deactivate()
	
	def testConqueredCitiesOutside(self):
		goal = Count.conqueredCities(2).outside(plots.rectangle((60, 30), (62, 32)))
		goal.activate(0)
		
		city1 = player(1).initCity(61, 31)
		player(0).acquireCity(city1, True, False)
		city1 = city_(61, 31)
		
		city2 = player(1).initCity(63, 31)
		player(0).acquireCity(city2, True, False)
		city2 = city_(63, 31)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		
		city1.kill()
		city2.kill()
		
		goal.deactivate()
	
	def testOpenBordersLess(self):
		goal = Count.openBorders(2)
		goal.activate(0)
		
		team(0).setOpenBorders(team(1).getID(), True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		
		team(0).setOpenBorders(team(1).getID(), False)
	
	def testOpenBordersMore(self):
		goal = Count.openBorders(1)
		goal.activate(0)
		
		others = [1, 2]
		for id in others:
			team(0).setOpenBorders(team(id).getID(), True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "2 / 1")
		
		for id in others:
			team(0).setOpenBorders(team(id).getID(), False)
	
	def testOpenBordersCivs(self):
		goal = Count.openBorders(2).civs([iBabylonia, iHarappa])
		goal.activate(0)
		
		others = [iBabylonia, iGreece]
		for iCiv in others:
			team(0).setOpenBorders(team(iCiv).getID(), True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		
		for iCiv in others:
			team(0).setOpenBorders(team(iCiv).getID(), False)
	
	def testSpecialistLess(self):
		goal = Count.specialist(iSpecialistGreatScientist, 3)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setFreeSpecialistCount(iSpecialistGreatScientist, 1)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 3")
		
		city.kill()
	
	def testSpecialistMore(self):
		goal = Count.specialist(iSpecialistGreatScientist, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setFreeSpecialistCount(iSpecialistGreatScientist, 2)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "4 / 3")
		
		for tile in tiles:
			city_(tile).kill()
	
	def testSpecialistsSome(self):
		goal = Count.specialist((iSpecialistGreatScientist, 3), (iSpecialistGreatArtist, 3))
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setFreeSpecialistCount(iSpecialistGreatScientist, 3)
		city.setFreeSpecialistCount(iSpecialistGreatArtist, 2)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), '\n'.join(["3 / 3", "2 / 3"]))
		
		city.kill()
	
	def testSpecialistsAll(self):
		goal = Count.specialist((iSpecialistGreatScientist, 3), (iSpecialistGreatArtist, 3))
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setFreeSpecialistCount(iSpecialistGreatScientist, 3)
		city.setFreeSpecialistCount(iSpecialistGreatArtist, 3)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), '\n'.join(["3 / 3", "3 / 3"]))
		
		city.kill()
	
	def testSpecialistSum(self):
		goal = Count.specialist(sum([iSpecialistGreatScientist, iSpecialistGreatArtist]), 4)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setFreeSpecialistCount(iSpecialistGreatScientist, 2)
		city.setFreeSpecialistCount(iSpecialistGreatArtist, 2)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "4 / 4")
		
		city.kill()
	
	def testAverageCulture(self):
		goal = Count.averageCulture(500)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		city1, city2, city3 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setCulture(0, 500, True)
		city2.setCulture(0, 1000, True)
		city3.setCulture(0, 1500, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1000 / 500")
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testPopulationCitiesNotEnough(self):
		goal = Count.populationCities(10, 3)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setPopulation(12)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 3")
		
		city.kill()
	
	def testPopulationCitiesLess(self):
		goal = Count.populationCities(10, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		city1, city2, city3 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setPopulation(12)
		city2.setPopulation(10)
		city3.setPopulation(8)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "2 / 3")
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testPopulationCitiesMore(self):
		goal = Count.populationCities(10, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31), (67, 31)]
		city1, city2, city3, city4 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setPopulation(16)
		city2.setPopulation(14)
		city3.setPopulation(12)
		city4.setPopulation(10)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "4 / 3")
		
		city1.kill()
		city2.kill()
		city3.kill()
		city4.kill()
	
	def testCultureCitiesNotEnough(self):
		goal = Count.cultureCities(500, 3)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		city.setCulture(0, 600, True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 3")
		
		city.kill()
	
	def testCultureCitiesLess(self):
		goal = Count.cultureCities(500, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		city1, city2, city3 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setCulture(0, 600, True)
		city2.setCulture(0, 500, True)
		city3.setCulture(0, 400, True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "2 / 3")
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testCultureCitiesMore(self):
		goal = Count.cultureCities(500, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31), (67, 31)]
		city1, city2, city3, city4 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setCulture(0, 800, True)
		city2.setCulture(0, 700, True)
		city3.setCulture(0, 600, True)
		city4.setCulture(0, 500, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "4 / 3")
		
		city1.kill()
		city2.kill()
		city3.kill()
		city4.kill()
	
	def testCultureLevelNotEnough(self):
		goal = Count.cultureLevelCities(iCultureLevelRefined, 3)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		
		city.setCulture(0, game.getCultureThreshold(iCultureLevelRefined), True)
		
		self.assertEqual(player(0).getNumCities(), 1)
		self.assertEqual(city.getCultureLevel(), iCultureLevelRefined)
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 3")
		
		city.kill()
	
	def testCultureLevelLess(self):
		goal = Count.cultureLevelCities(iCultureLevelRefined, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		city1, city2, city3 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setCulture(0, game.getCultureThreshold(iCultureLevelInfluential), True)
		city2.setCulture(0, game.getCultureThreshold(iCultureLevelRefined), True)
		city3.setCulture(0, game.getCultureThreshold(iCultureLevelDeveloping), True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "2 / 3")
		
		city1.kill()
		city2.kill()
		city3.kill()
	
	def testCultureLevelCitiesMore(self):
		goal = Count.cultureLevelCities(iCultureLevelRefined, 3)
		goal.activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31), (67, 31)]
		city1, city2, city3, city4 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setCulture(0, game.getCultureThreshold(iCultureLevelInfluential), True)
		city2.setCulture(0, game.getCultureThreshold(iCultureLevelInfluential), True)
		city3.setCulture(0, game.getCultureThreshold(iCultureLevelRefined), True)
		city4.setCulture(0, game.getCultureThreshold(iCultureLevelRefined), True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "4 / 3")
		
		city1.kill()
		city2.kill()
		city3.kill()
		city4.kill()
	
	def testCitySpecialistWithoutCity(self):
		goal = Count.citySpecialist(city(61, 31), iSpecialistGreatScientist, 3)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 3")
		
	def testCitySpecialistDifferentOwner(self):
		goal = Count.citySpecialist(city(61, 31), iSpecialistGreatScientist, 3)
		goal.activate(0)
		
		_city = player(1).initCity(61, 31)
		_city.setFreeSpecialistCount(iSpecialistGreatScientist, 3)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 3")
		
		_city.kill()
	
	def testCitySpecialistEnough(self):
		goal = Count.citySpecialist(city(61, 31), iSpecialistGreatScientist, 3)
		goal.activate(0)
		
		_city = player(0).initCity(61, 31)
		_city.setFreeSpecialistCount(iSpecialistGreatScientist, 3)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "3 / 3")
		
		_city.kill()
	
	def testCultureLevelNoCity(self):
		goal = Count.cultureLevel(city(61, 31), iCultureLevelRefined)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1000")
	
	def testCultureLevelDifferentOwner(self):
		goal = Count.cultureLevel(city(61, 31), iCultureLevelRefined)
		goal.activate(0)
		
		_city = player(1).initCity(61, 31)
		_city.setCulture(0, 5000, True)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1000")
		
		_city.kill()
	
	def testCultureLevelEnough(self):
		goal = Count.cultureLevel(city(61, 31), iCultureLevelRefined)
		goal.activate(0)
		
		_city = player(0).initCity(61, 31)
		_city.setCulture(0, 5000, True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "5000 / 1000")
		
		_city.kill()
	
	def testAttitude(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_FRIENDLY, 2)
		goal.activate(0)
		
		for i in [1, 2]:
			team(i).meet(0, False)
			player(i).AI_setAttitudeExtra(0, 100)
			
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "2 / 2")
		
		for i in [1, 2]:
			team(i).cutContact(0)
			player(i).AI_setAttitudeExtra(0, 0)
	
	def testAttitudeInsufficient(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_FRIENDLY, 2)
		goal.activate(0)
		
		for i in [1, 2]:
			team(i).meet(0, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 2")
		
		for i in [1, 2]:
			team(i).cutContact(0)
	
	def testAttitudeNoContact(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_FRIENDLY, 2)
		goal.activate(0)
		
		for i in [1, 2]:
			team(i).cutContact(0)
			player(i).AI_setAttitudeExtra(0, 100)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 2")
		
		for i in [1, 2]:
			player(i).AI_setAttitudeExtra(0, 0)
	
	def testAttitudeCivs(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_FRIENDLY, 2).civs([iBabylonia])
		goal.activate(0)
		
		for i in [iBabylonia, iHarappa]:
			team(i).meet(0, False)
			player(i).AI_setAttitudeExtra(0, 100)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		
		for i in [iBabylonia, iHarappa]:
			team(i).cutContact(0)
			player(i).AI_setAttitudeExtra(0, 0)
		
	def testAttitudeReligion(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_FRIENDLY, 2).religion(iOrthodoxy)
		goal.activate(0)
		
		for i in [1, 2]:
			team(i).meet(0, False)
			player(i).AI_setAttitudeExtra(0, 100)
		
		player(1).setLastStateReligion(iOrthodoxy)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		
		for i in [1, 2]:
			team(i).cutContact(0)
			player(i).AI_setAttitudeExtra(0, 0)
		
		player(1).setLastStateReligion(-1)
	
	def testAttitudeCommunist(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_FRIENDLY, 2).communist()
		goal.activate(0)
		
		for i in [1, 2]:
			team(i).meet(0, False)
			player(i).AI_setAttitudeExtra(0, 100)
		
		player(1).setCivics(iCivicsEconomy, iCentralPlanning)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		
		for i in [1, 2]:
			team(i).cutContact(0)
			player(i).AI_setAttitudeExtra(0, 0)
		
		player(1).setCivics(iCivicsEconomy, iReciprocity)
	
	def testAttitudeChainedFilters(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_FRIENDLY, 2).civs([iBabylonia]).religion(iOrthodoxy)
		goal.activate(0)
		
		for i in [1, 2]:
			team(i).meet(0, False)
			player(i).AI_setAttitudeExtra(0, 100)
		
		player(2).setLastStateReligion(iOrthodoxy)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 2")
		
		for i in [1, 2]:
			team(i).cutContact(0)
			player(i).AI_setAttitudeExtra(0, 0)
		
		player(2).setLastStateReligion(-1)
	
	def testVassals(self):
		goal = Count.vassals(2)
		goal.activate(0)
		
		for i in [1, 2]:
			team(i).setVassal(0, True, False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "2 / 2")
		self.assertEqual(goal.state, SUCCESS)
		
		for i in [1, 2]:
			team(i).setVassal(0, False, False)
	
	def testVassalsCivs(self):
		goal = Count.vassals(2).civs([iBabylonia])
		goal.activate(0)
		
		for i in [iBabylonia, iHarappa]:
			team(i).setVassal(0, True, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		self.assertEqual(goal.state, POSSIBLE)
		
		for i in [iBabylonia, iHarappa]:
			team(i).setVassal(0, False, False)
	
	def testVassalsReligion(self):
		goal = Count.vassals(2).religion(iOrthodoxy)
		goal.activate(0)
		
		for i in [1, 2]:
			team(i).setVassal(0, True, False)
		
		player(1).setLastStateReligion(iOrthodoxy)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		self.assertEqual(goal.state, POSSIBLE)
		
		for i in [1, 2]:
			team(i).setVassal(0, False, False)
		
		player(1).setLastStateReligion(-1)
	
	def testCityBuildingNoCity(self):
		goal = Count.cityBuilding(city(61, 31), iGranary)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		self.assertEqual(goal.state, POSSIBLE)
		
		goal.deactivate()
	
	def testCityBuildingNoBuilding(self):
		goal = Count.cityBuilding(city(61, 31), iGranary)
		goal.activate(0)
		
		_city = player(0).initCity(61, 31)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		self.assertEqual(goal.state, POSSIBLE)
		
		_city.kill()
		
		goal.deactivate()
	
	def testCityBuildingWithBuilding(self):
		goal = Count.cityBuilding(city(61, 31), iGranary)
		goal.activate(0)
		
		_city = player(0).initCity(61, 31)
		_city.setHasRealBuilding(iGranary, True)
		
		events.fireEvent("buildingBuilt", _city, iGranary)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		self.assertEqual(goal.state, SUCCESS)
		
		_city.kill()
		
		goal.deactivate()
		
	def testCityBuildingDifferentCity(self):
		goal = Count.cityBuilding(city(61, 31), iGranary)
		goal.activate(0)
		
		_city = player(0).initCity(63, 31)
		_city.setHasRealBuilding(iGranary, True)
		
		events.fireEvent("buildingBuilt", _city, iGranary)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		self.assertEqual(goal.state, POSSIBLE)
		
		_city.kill()
		
		goal.deactivate()
	
	def testCityMultipleBuildingsSome(self):
		goal = Count.cityBuilding(city(61, 31), iGranary, iBarracks, iLibrary)
		goal.activate(0)
		
		_city = player(0).initCity(61, 31)
		for iBuilding in [iGranary, iBarracks]:
			_city.setHasRealBuilding(iBuilding, True)
			events.fireEvent("buildingBuilt", _city, iBuilding)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 1\n1 / 1\n0 / 1")
		self.assertEqual(goal.state, POSSIBLE)
		
		_city.kill()
		
		goal.deactivate()
	
	def testCityMultipleBuildingsAll(self):
		goal = Count.cityBuilding(city(61, 31), iGranary, iBarracks, iLibrary)
		goal.activate(0)
		
		_city = player(0).initCity(61, 31)
		for iBuilding in [iGranary, iBarracks, iLibrary]:
			_city.setHasRealBuilding(iBuilding, True)
			events.fireEvent("buildingBuilt", _city, iBuilding)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1\n1 / 1\n1 / 1")
		self.assertEqual(goal.state, SUCCESS)
		
		_city.kill()
		
		goal.deactivate()
	
	def testCityMultipleBuildingsDifferentCities(self):
		goal = Count.cityBuilding(city(61, 31), iGranary, iBarracks, iLibrary)
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		city1.setHasRealBuilding(iGranary, True)
		city1.setHasRealBuilding(iBarracks, True)
		city2.setHasRealBuilding(iLibrary, True)
		
		events.fireEvent("buildingBuilt", city1, iGranary)
		events.fireEvent("buildingBuilt", city1, iBarracks)
		events.fireEvent("buildingBuilt", city2, iLibrary)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 1\n1 / 1\n0 / 1")
		self.assertEqual(goal.state, POSSIBLE)
		
		city1.kill()
		city2.kill()
		
		goal.deactivate()
	
	def testCityBuildingSum(self):
		goal = Count.cityBuilding(city(61, 31), sum([iGranary, iBarracks, iLibrary]), 2)
		goal.activate(0)
		
		city_ = player(0).initCity(61, 31)
		
		city_.setHasRealBuilding(iGranary, True)
		city_.setHasRealBuilding(iLibrary, True)
		
		events.fireEvent("buildingBuilt", city_, iGranary)
		events.fireEvent("buildingBuilt", city_, iLibrary)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "2 / 2")
		self.assertEqual(goal.state, SUCCESS)
		
		city_.kill()
		
		goal.deactivate()


class TestPercentageGoals(ExtendedTestCase):

	def testAreaControl(self):
		area = plots.rectangle((50, 30), (69, 31))
		goal = Percentage.areaControl(area, 30)
		goal.activate(0)
		
		controlled = plots.rectangle((50, 30), (69, 30))
		for plot in controlled:
			plot.setOwner(0)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "50.00% / 30%")
		
		for plot in controlled:
			plot.setOwner(-1)
		
		goal.deactivate()
	
	def testAreaControlInsufficient(self):
		area = plots.rectangle((50, 30), (69, 31))
		goal = Percentage.areaControl(area, 30)
		goal.activate(0)
		
		controlled = plots.rectangle((50, 30), (50, 30))
		for plot in controlled:
			plot.setOwner(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "2.50% / 30%")
		
		for plot in controlled:
			plot.setOwner(-1)
		
		goal.deactivate()
			
	def testWorldControl(self):
		goal = Percentage.worldControl(10)
		goal.activate(0)
		
		controlled = plots.all().land().limit(11 * 32)
		for plot in controlled:
			plot.setOwner(0)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "10.89% / 10%")
		
		for plot in controlled:
			plot.setOwner(-1)
		
		goal.deactivate()
	
	def testWorldControlInsufficient(self):
		goal = Percentage.worldControl(10)
		goal.activate(0)
		
		controlled = plots.all().land().limit(32)
		for plot in controlled:
			plot.setOwner(0)
	
		self.assertEqual(map.getLandPlots(), 3232)
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0.99% / 10%")
		
		for plot in controlled:
			plot.setOwner(-1)
		
		goal.deactivate()
	
	def testReligionSpread(self):
		goal = Percentage.religionSpread(iOrthodoxy, 30)
		goal.activate(1)
		
		city1 = player(1).initCity(30, 30)
		city2 = player(2).initCity(32, 30)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		player(1).setLastStateReligion(iOrthodoxy)
		
		city1.setHasReligion(iOrthodoxy, True, False, False)
		
		self.assertEqual(str(goal), "50.00% / 30%")
		self.assertEqual(bool(goal), True)
		
		city1.kill()
		city2.kill()
		
		player(1).setLastStateReligion(iOrthodoxy)
		
		goal.deactivate()
	
	def testReligionSpreadNoState(self):
		goal = Percentage.religionSpread(iOrthodoxy, 30)
		goal.activate(1)
		
		city1 = player(1).initCity(30, 30)
		city2 = player(2).initCity(32, 30)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasReligion(iOrthodoxy, True, False, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "25.00% / 30%")
		
		city1.kill()
		city2.kill()
		
		goal.deactivate()
	
	def testReligionSpreadMultipleReligions(self):
		goal = Percentage.religionSpread(iOrthodoxy, 30)
		goal.activate(1)
		
		city1 = player(1).initCity(30, 30)
		city2 = player(2).initCity(32, 30)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasReligion(iOrthodoxy, True, False, False)
		city1.setHasReligion(iCatholicism, True, False, False)
		
		player(1).setLastStateReligion(iOrthodoxy)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "35.00% / 30%")
		
		city1.kill()
		city2.kill()
		
		player(1).setLastStateReligion(-1)
		
		goal.deactivate()
	
	def testReligionSpreadNotOwned(self):
		goal = Percentage.religionSpread(iOrthodoxy, 30)
		goal.activate(1)
		
		city1 = player(2).initCity(30, 30)
		city2 = player(3).initCity(32, 30)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasReligion(iOrthodoxy, True, False, False)
		
		player(2).setLastStateReligion(iOrthodoxy)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "50.00% / 30%")
		
		city1.kill()
		city2.kill()
		
		player(2).setLastStateReligion(-1)
		
		goal.deactivate()
	
	def testPopulation(self):
		goal = Percentage.population(30)
		goal.activate(0)
		
		city1 = player(0).initCity(30, 30)
		city2 = player(1).initCity(32, 30)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "50.00% / 30%")
		
		city1.kill()
		city2.kill()
		
		goal.deactivate()
	
	def testPopulationInsufficient(self):
		goal = Percentage.population(30)
		goal.activate(0)
		
		city1 = player(0).initCity(30, 30)
		city2 = player(1).initCity(32, 30)
		
		city1.setPopulation(5)
		city2.setPopulation(20)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "20.00% / 30%")
		
		city1.kill()
		city2.kill()
		
		goal.deactivate()
	
	def testPopulationIncludeVassals(self):
		goal = Percentage.population(50).includeVassals()
		goal.activate(0)
		
		city1 = player(0).initCity(30, 30)
		city2 = player(1).initCity(32, 30)
		city3 = player(2).initCity(34, 30)
		
		city1.setPopulation(5)
		city2.setPopulation(5)
		city3.setPopulation(10)
		
		team(1).setVassal(team(0).getID(), True, False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "50.00% / 50%")
		
		city1.kill()
		city2.kill()
		city3.kill()
		
		team(1).setVassal(team(0).getID(), False, False)
		
		goal.deactivate()
	
	def testReligiousVote(self):
		goal = Percentage.religiousVote(30)
		goal.activate(1)
		
		city1 = player(1).initCity(30, 30)
		city2 = player(2).initCity(32, 30)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasRealBuilding(iCatholicShrine, True)
		
		city1.setHasReligion(iCatholicism, True, False, False)
		city2.setHasReligion(iCatholicism, True, False, False)
		
		player(1).setLastStateReligion(iCatholicism)
		player(2).setLastStateReligion(iCatholicism)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "50.00% / 30%")
		
		city1.kill()
		city2.kill()
		
		player(1).setLastStateReligion(-1)
		player(2).setLastStateReligion(-1)
		
		goal.deactivate()
	
	def testReligiousVoteNotStateReligion(self):
		goal = Percentage.religiousVote(30)
		goal.activate(1)
		
		city1 = player(1).initCity(30, 30)
		city2 = player(2).initCity(32, 30)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasRealBuilding(iCatholicShrine, True)
		
		city1.setHasReligion(iCatholicism, True, False, False)
		city2.setHasReligion(iCatholicism, True, False, False)
		
		player(2).setLastStateReligion(iCatholicism)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0.00% / 30%")
		
		city1.kill()
		city2.kill()
		
		player(2).setLastStateReligion(-1)
		
		goal.deactivate()
		
	def testReligiousVoteNoReligion(self):
		goal = Percentage.religiousVote(30)
		goal.activate(1)
		
		city1 = player(1).initCity(30, 30)
		city2 = player(2).initCity(32, 30)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasRealBuilding(iCatholicShrine, True)
		
		city2.setHasReligion(iCatholicism, True, False, False)
		
		player(1).setLastStateReligion(iCatholicism)
		player(2).setLastStateReligion(iCatholicism)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0.00% / 30%")
		
		city1.kill()
		city2.kill()
		
		player(0).setLastStateReligion(-1)
		player(1).setLastStateReligion(-1)
		
		goal.deactivate()
	
	def testAlliedPower(self):
		goal = Percentage.alliedPower(30)
		goal.activate(0)
		
		unit = makeUnit(0, iMilitia, (0, 0))
		
		self.assertEqual(str(goal), "50.00% / 30%")
		self.assertEqual(bool(goal), True)
		
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testAlliedPowerWithVassal(self):
		goal = Percentage.alliedPower(30)
		goal.activate(0)
		
		unit = makeUnit(0, iMilitia, (0, 0))
		
		team(1).setVassal(team(0).getID(), True, False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "75.00% / 30%")
		
		unit.kill(False, -1)
		
		team(1).setVassal(team(0).getID(), False, False)
		
		goal.deactivate()
	
	def testAlliedPowerWithDefensivePact(self):
		goal = Percentage.alliedPower(30)
		goal.activate(0)
		
		unit = makeUnit(0, iMilitia, (0, 0))
		
		team(0).setDefensivePact(team(1).getID(), True)
		team(1).setDefensivePact(team(0).getID(), True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "75.00% / 30%")
		
		unit.kill(False, -1)
		
		team(1).setDefensivePact(team(0).getID(), False)
		team(0).setDefensivePact(team(1).getID(), False)
		
		goal.deactivate()
	
	def testAlliedPowerWithDefensivePactVassal(self):
		goal = Percentage.alliedPower(30)
		goal.activate(0)
		
		unit = makeUnit(0, iMilitia, (0, 0))
		
		team(2).setVassal(team(1).getID(), True, False)
		team(0).setDefensivePact(team(1).getID(), True)
		team(1).setDefensivePact(team(0).getID(), True)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100.00% / 30%")
		
		unit.kill(False, -1)
		
		team(2).setVassal(team(1).getID(), False, False)
		team(0).setDefensivePact(team(1).getID(), False)
		team(1).setDefensivePact(team(0).getID(), False)
		
		goal.deactivate()
	
	def testAlliedCommerce(self):
		goal = Percentage.alliedCommerce(30)
		goal.activate(0)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "33.33% / 30%")
		
		goal.deactivate()


class TestTriggerGoals(ExtendedTestCase):

	def testFirstDiscover(self):
		goal = Trigger.firstDiscover(iLaw)
		goal.activate(0)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(goal.state, SUCCESS)
		
		team(0).setHasTech(iLaw, False, 0, True, False)
		
		goal.deactivate()
	
	def testFirstDiscoverOther(self):
		goal = Trigger.firstDiscover(iLaw)
		goal.activate(0)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(goal.state, FAILURE)
		
		team(1).setHasTech(iLaw, False, 1, True, False)
		
		goal.deactivate()
	
	def testFirstDiscoverAfterOther(self):
		goal = Trigger.firstDiscover(iLaw)
		goal.activate(0)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		team(0).setHasTech(iLaw, True, 0, True, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(goal.state, FAILURE)
		
		team(1).setHasTech(iLaw, False, 1, True, False)
		team(0).setHasTech(iLaw, False, 0, True, False)
		
		goal.deactivate()
	
	def testFirstDiscoverNone(self):
		goal = Trigger.firstDiscover(iLaw, iCurrency, iPhilosophy)
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(goal.state, POSSIBLE)
		
		goal.deactivate()
	
	def testFirstDiscoverSome(self):
		goal = Trigger.firstDiscover(iLaw, iCurrency, iPhilosophy)
		goal.activate(0)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		team(0).setHasTech(iCurrency, True, 0, True, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(goal.state, POSSIBLE)
		
		team(0).setHasTech(iLaw, False, 0, True, False)
		team(0).setHasTech(iCurrency, False, 0, True, False)
		
		goal.deactivate()
	
	def testFirstDiscoverAll(self):
		goal = Trigger.firstDiscover(iLaw, iCurrency, iPhilosophy)
		goal.activate(0)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		team(0).setHasTech(iCurrency, True, 0, True, False)
		team(0).setHasTech(iPhilosophy, True, 0, True, False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(goal.state, SUCCESS)
		
		team(0).setHasTech(iLaw, False, 0, True, False)
		team(0).setHasTech(iCurrency, False, 0, True, False)
		team(0).setHasTech(iPhilosophy, False, 0, True, False)
		
		goal.deactivate()
	
	def testFirstExpireAny(self):
		goal = Trigger.firstDiscover(iLaw, iCurrency, iPhilosophy)
		goal.activate(0)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(goal.state, FAILURE)
		
		team(1).setHasTech(iLaw, False, 1, True, False)
		
		goal.deactivate()
	
	def testFirstNewWorld(self):
		goal = Trigger.firstNewWorld()
		goal.activate(0)
		
		player(0).found(19, 47)
		
		self.assertEqual(bool(goal), True)
		
		city_(19, 47).kill()
		
		goal.deactivate()
	
	def testFirstNewWorldOther(self):
		goal = Trigger.firstNewWorld()
		goal.activate(0)
		
		player(1).found(19, 47)
		
		success = bool(goal)
		
		self.assertEqual(success, False)
		
		city_(19, 47).kill()
		
		goal.deactivate()
	
	def testFirstNewWorldAfterOther(self):
		goal = Trigger.firstNewWorld()
		goal.activate(0)
		
		player(1).found(19, 47)
		player(0).found(21, 47)
		
		self.assertEqual(bool(goal), False)
		
		city_(19, 47).kill()
		city_(21, 47).kill()
		
		goal.deactivate()
	
	def testFirstNewWorldAfterNative(self):
		goal = Trigger.firstNewWorld()
		goal.activate(0)
		
		player(iMaya).found(19, 47)
		player(0).found(21, 47)
		
		self.assertEqual(bool(goal), True)
		
		city_(19, 47).kill()
		city_(21, 47).kill()
		
		goal.deactivate()
	
	def testFirstNewWorldConquest(self):
		goal = Trigger.firstNewWorld()
		goal.activate(0)
		
		player(iMaya).found(19, 47)
		player(0).acquireCity(city_(19, 47), True, False)
		
		self.assertEqual(bool(goal), False)
		
		city_(19, 47).kill()
		
		goal.deactivate()
	
	def testFirstNewWorldAfterConquest(self):
		goal = Trigger.firstNewWorld()
		goal.activate(0)
		
		player(iMaya).found(19, 47)
		player(1).acquireCity(city_(19, 47), True, False)
		player(0).found(21, 47)
		
		self.assertEqual(bool(goal), True)
		
		city_(19, 47).kill()
		city_(21, 47).kill()
		
		goal.deactivate()
	
	def testFirstNewWorldOutsideAmerica(self):
		goal = Trigger.firstNewWorld()
		goal.activate(0)
		
		player(0).found(61, 37)
		
		self.assertEqual(bool(goal), False)
		
		city_(61, 37).kill()
		
		goal.deactivate()
	
	def testDiscover(self):
		goal = Trigger.discover(iLaw)
		goal.activate(0)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		
		self.assertEqual(bool(goal), True)
		
		team(0).setHasTech(iLaw, False, 0, True, False)
		
		goal.deactivate()
	
	def testDiscoverOther(self):
		goal = Trigger.discover(iLaw)
		goal.activate(0)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		
		self.assertEqual(bool(goal), False)
		
		team(1).setHasTech(iLaw, False, 1, True, False)
		
		goal.deactivate()
	
	def testDiscoverAfterOther(self):
		goal = Trigger.discover(iLaw)
		goal.activate(0)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		team(0).setHasTech(iLaw, True, 0, True, False)
		
		self.assertEqual(bool(goal), True)
		
		team(1).setHasTech(iLaw, False, 1, True, False)
		team(0).setHasTech(iLaw, False, 0, True, False)
		
		goal.deactivate()
	
	def testDiscoverSome(self):
		goal = Trigger.discover(iLaw, iCurrency, iPhilosophy)
		goal.activate(0)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		team(0).setHasTech(iCurrency, True, 0, True, False)
		
		self.assertEqual(bool(goal), False)
		
		team(0).setHasTech(iLaw, False, 0, True, False)
		team(0).setHasTech(iCurrency, False, 0, True, False)
		
		goal.deactivate()
	
	def testDiscoverAll(self):
		goal = Trigger.discover(iLaw, iCurrency, iPhilosophy)
		goal.activate(0)
		
		for iTech in [iLaw, iCurrency, iPhilosophy]:
			team(0).setHasTech(iTech, True, 0, True, False)
		
		self.assertEqual(bool(goal), True)
		
		for iTech in [iLaw, iCurrency, iPhilosophy]:
			team(0).setHasTech(iTech, False, 0, True, False)
		
		goal.deactivate()
		
	def testFirstContact(self):
		goal = Trigger.firstContact(plots.rectangle((20, 20), (30, 30)), iChina)
		goal.activate(0)
		
		events.fireEvent("firstContact", team(iEgypt).getID(), team(iChina).getID())
		
		self.assertEqual(bool(goal), True)
		
		goal.deactivate()
	
	def testFirstContactWithOther(self):
		goal = Trigger.firstContact(plots.rectangle((20, 20), (30, 30)), iChina)
		goal.activate(0)
		
		events.fireEvent("firstContact", team(iEgypt).getID(), team(iGreece).getID())
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(goal.state, POSSIBLE)
		
		goal.deactivate()
	
	def testFirstContactAfterRevealed(self):
		goal = Trigger.firstContact(plots.rectangle((20, 20), (30, 30)), iChina)
		goal.activate(0)
		
		plot(25, 25).setRevealed(team(iChina).getID(), True, False, team(iChina).getID())
		
		events.fireEvent("firstContact", team(iEgypt).getID(), team(iChina).getID())
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(goal.state, FAILURE)
		
		plot(25, 25).setRevealed(team(iChina).getID(), False, False, team(iChina).getID())
		
		goal.deactivate()
	
	def testFirstContactSome(self):
		goal = Trigger.firstContact(plots.rectangle((20, 20), (30, 30)), iChina, iGreece, iIndia)
		goal.activate(0)
		
		events.fireEvent("firstContact", team(iEgypt).getID(), team(iChina).getID())
		events.fireEvent("firstContact", team(iEgypt).getID(), team(iGreece).getID())
		
		self.assertEqual(bool(goal), False)
		
		goal.deactivate()
	
	def testFirstContactAll(self):
		goal = Trigger.firstContact(plots.rectangle((20, 20), (30, 30)), iChina, iGreece, iIndia)
		goal.activate(0)
		
		for iCiv in [iChina, iGreece, iIndia]:
			events.fireEvent("firstContact", team(iEgypt).getID(), team(iCiv).getID())
		
		self.assertEqual(bool(goal), True)
		
		goal.deactivate()
	
	def testNoCityLost(self):
		goal = Trigger.noCityLost()
		goal.activate(0)
		
		self.assertEqual(bool(goal), True)
		
		goal.deactivate()
	
	def testNoCityLostAfterLosing(self):
		goal = Trigger.noCityLost()
		goal.activate(0)
		
		city = player(1).initCity(25, 25)
		events.fireEvent("cityAcquired", 0, 1, city, True, False)
		
		self.assertEqual(goal.state, FAILURE)
		
		city.kill()
		
		goal.deactivate()
	
	def testTradeMission(self):
		goal = Trigger.tradeMission(city(25, 25))
		goal.activate(0)
		
		city_ = player(1).initCity(25, 25)
		events.fireEvent("tradeMission", iGreatMerchant, 0, 25, 25, 1000)
		
		self.assertEqual(bool(goal), True)
		
		city_.kill()
		
		goal.deactivate()
		
	def testTradeMissionOther(self):
		goal = Trigger.tradeMission(city(25, 25))
		goal.activate(0)
		
		city_ = player(1).initCity(25, 25)
		events.fireEvent("tradeMission", iGreatMerchant, 2, 25, 25, 1000)
		
		self.assertEqual(bool(goal), False)
		
		city_.kill()
		
		goal.deactivate()
	
	def testTradeMissionElsewhere(self):
		goal = Trigger.tradeMission(city(25, 25))
		goal.activate(0)
		
		city_ = player(1).initCity(30, 25)
		events.fireEvent("tradeMission", iGreatMerchant, 0, 30, 25, 1000)
		
		self.assertEqual(bool(goal), False)
		
		city_.kill()
		
		goal.deactivate()
	
	def testTradeMissionHolyCityWithout(self):
		goal = Trigger.tradeMission(holyCity())
		goal.activate(0)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		city = player(1).initCity(30, 25)
		events.fireEvent("tradeMission", iGreatMerchant, 0, 30, 25, 1000)
		self.assertEqual(bool(goal), False)
		
		player(0).setLastStateReligion(-1)
		city.kill()
		
		goal.deactivate()
	
	def testTradeMissionHolyCity(self):
		goal = Trigger.tradeMission(holyCity())
		goal.activate(0)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		city = player(1).initCity(30, 25)
		game.setHolyCity(iOrthodoxy, city, False)
		events.fireEvent("tradeMission", iGreatMerchant, 0, 30, 25, 1000)
		
		self.assertEqual(bool(goal), True)
		
		player(0).setLastStateReligion(iOrthodoxy)
		city.kill()
		
		goal.deactivate()
	
	def testTradeMissionHolyCityNoStateReligion(self):
		goal = Trigger.tradeMission(holyCity())
		goal.activate(0)
		
		city = player(1).initCity(30, 25)
		game.setHolyCity(iOrthodoxy, city, False)
		
		self.assertEqual(bool(goal), False)
		
		city.kill()
		
		goal.deactivate()
	
	def testNeverConquer(self):
		goal = Trigger.neverConquer()
		goal.activate(0)
		
		self.assertEqual(bool(goal), True)
		
		goal.deactivate()
	
	def testNeverConquerConquered(self):
		goal = Trigger.neverConquer()
		goal.activate(0)
		
		city = player(1).initCity(30, 25)
		player(0).acquireCity(city, True, False)
		
		self.assertEqual(goal.state, FAILURE)
		
		city_(30, 25).kill()
		
		goal.deactivate()
	
	def testNeverConquerTraded(self):
		goal = Trigger.neverConquer()
		goal.activate(0)
		
		city = player(1).initCity(30, 25)
		player(0).acquireCity(city, False, True)
		
		self.assertEqual(bool(goal), True)
		
		city_(30, 25).kill()
		
		goal.deactivate()
	
	def testNeverConquerConqueredOther(self):
		goal = Trigger.neverConquer()
		goal.activate(0)
		
		city = player(1).initCity(30, 25)
		player(2).acquireCity(city, True, False)
		
		self.assertEqual(bool(goal), True)
		
		city_(30, 25).kill()
		
		goal.deactivate()
	
	def testConvertAfterFounding(self):
		goal = Trigger.convertAfterFounding(5, iOrthodoxy)
		goal.activate(0)
		
		events.fireEvent("religionFounded", iOrthodoxy, 1)
		
		self.assertEqual(goal.dFoundingTurn[iOrthodoxy], turn())
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		self.assertEqual(bool(goal), True)
		
		player(0).setLastStateReligion(-1)
		
		goal.deactivate()
	
	def testConvertAfterFoundingNotFounded(self):
		goal = Trigger.convertAfterFounding(5, iOrthodoxy)
		goal.activate(0)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		self.assertEqual(bool(goal), False)
		
		player(0).setLastStateReligion(-1)
		
		goal.deactivate()
	
	def testConvertAfterFoundingOtherReligion(self):
		goal = Trigger.convertAfterFounding(5, iOrthodoxy)
		goal.activate(0)
		
		events.fireEvent("religionFounded", iOrthodoxy, 1)
		events.fireEvent("religionFounded", iCatholicism, 2)
		
		player(0).setLastStateReligion(iCatholicism)
		
		self.assertEqual(bool(goal), False)
		
		player(0).setLastStateReligion(-1)
		
		goal.deactivate()
	
	def testConvertAfterFoundingSoonEnough(self):
		goal = Trigger.convertAfterFounding(5, iOrthodoxy)
		goal.activate(0)
		
		goal.dFoundingTurn[iOrthodoxy] = turn() - 2
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		self.assertEqual(bool(goal), True)
		
		player(0).setLastStateReligion(-1)
		
		goal.deactivate()
	
	def testConvertAfterFoundingTooLate(self):
		goal = Trigger.convertAfterFounding(5, iOrthodoxy)
		goal.activate(0)
		
		goal.dFoundingTurn[iOrthodoxy] = turn() - 10
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		self.assertEqual(bool(goal), False)
		
		player(0).setLastStateReligion(-1)
		
		goal.deactivate()
	
	def testConvertAfterFoundingSome(self):
		goal = Trigger.convertAfterFounding(5, iOrthodoxy, iCatholicism)
		goal.activate(0)
		
		events.fireEvent("religionFounded", iOrthodoxy, 1)
		events.fireEvent("religionFounded", iCatholicism, 2)
		
		self.assertEqual(goal.dFoundingTurn[iOrthodoxy], turn())
		self.assertEqual(goal.dFoundingTurn[iCatholicism], turn())
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(goal.dCondition[(5, iOrthodoxy)], True)
		self.assertEqual(goal.dCondition[(5, iCatholicism)], False)
		
		player(0).setLastStateReligion(-1)
		
		goal.deactivate()
	
	def testConvertAfterFoundingAll(self):
		goal = Trigger.convertAfterFounding(5, iOrthodoxy, iCatholicism)
		goal.activate(0)
		
		events.fireEvent("religionFounded", iOrthodoxy, 1)
		events.fireEvent("religionFounded", iCatholicism, 2)
		
		player(0).setLastStateReligion(iOrthodoxy)
		player(0).setLastStateReligion(iCatholicism)
		
		self.assertEqual(bool(goal), True)
		
		player(0).setLastStateReligion(-1)
		
		goal.deactivate()
	
	def testEnterEra(self):
		goal = Trigger.enterEra(iClassical)
		goal.activate(0)
		
		events.fireEvent("techAcquired", iLaw, 0, 0, False)
		
		self.assertEqual(bool(goal), True)
		
		goal.deactivate()
	
	def testEnterEraOther(self):
		goal = Trigger.enterEra(iClassical)
		goal.activate(0)
		
		events.fireEvent("techAcquired", iLeverage, 0, 0, False)
		
		self.assertEqual(bool(goal), False)
		
		goal.deactivate()
	
	def testEnterEraSome(self):
		goal = Trigger.enterEra(iClassical, iMedieval)
		goal.activate(0)
		
		events.fireEvent("techAcquired", iLaw, 0, 0, False)
		
		self.assertEqual(bool(goal), False)
		
		goal.deactivate()
	
	def testEnterEraAll(self):
		goal = Trigger.enterEra(iClassical, iMedieval)
		goal.activate(0)
		
		events.fireEvent("techAcquired", iLaw, 0, 0, False)
		events.fireEvent("techAcquired", iDoctrine, 0, 0, False)
		
		self.assertEqual(bool(goal), True)
		
		goal.deactivate()
	
	def testEnterEraExpire(self):
		goal = Trigger.enterEra(iClassical).before(iMedieval)
		goal.activate(0)
		
		events.fireEvent("techAcquired", iDoctrine, 1, 1, False)
		
		self.assertEqual(goal.state, FAILURE)
		
		goal.deactivate()


class TestTrackGoals(ExtendedTestCase):

	def testGoldenAgesOutside(self):
		goal = Track.goldenAges(1)
		goal.activate(0)
		
		events.fireEvent("BeginPlayerTurn", game.getGameTurn(), 0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 8")
		self.assertEqual(goal.state, POSSIBLE)
		
		goal.deactivate()
	
	def testGoldenAgesDuring(self):
		goal = Track.goldenAges(1)
		goal.activate(0)
		
		player(0).changeGoldenAgeTurns(8)
		
		events.fireEvent("BeginPlayerTurn", game.getGameTurn(), 0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 8")
		self.assertEqual(goal.state, POSSIBLE)
		
		player(0).changeGoldenAgeTurns(-8)
		
		goal.deactivate()
		
	def testGoldenAgesAnarchy(self):
		goal = Track.goldenAges(1)
		goal.activate(0)
		
		player(0).changeGoldenAgeTurns(8)
		player(0).changeAnarchyTurns(8)
		
		events.fireEvent("BeginPlayerTurn", game.getGameTurn(), 0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 8")
		self.assertEqual(goal.state, POSSIBLE)
		
		player(0).changeGoldenAgeTurns(-8)
		player(0).changeAnarchyTurns(-8)
		
		goal.deactivate()
	
	def testGoldenAgesSuccess(self):
		goal = Track.goldenAges(1)
		goal.activate(0)
		
		player(0).changeGoldenAgeTurns(8)
		
		for _ in range(8):
			events.fireEvent("BeginPlayerTurn", game.getGameTurn(), 0)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "8 / 8")
		self.assertEqual(goal.state, SUCCESS)
		
		player(0).changeGoldenAgeTurns(-8)
		
		goal.deactivate()
	
	def testEraFirsts(self):
		goal = Track.eraFirsts(iClassical, 5)
		goal.activate(0)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 5")
		
		team(0).setHasTech(iLaw, False, 0, True, False)
		
		goal.deactivate()
	
	def testEraFirstsDifferentEra(self):
		goal = Track.eraFirsts(iClassical, 5)
		goal.activate(0)
		
		team(0).setHasTech(iFeudalism, True, 0, True, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 5")
		
		team(0).setHasTech(iFeudalism, False, 0, True, False)
		
		goal.deactivate()
	
	def testEraFirstsNotFirst(self):
		goal = Track.eraFirsts(iClassical, 5)
		goal.activate(0)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		team(0).setHasTech(iLaw, True, 0, False, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 5")
		
		team(0).setHasTech(iLaw, False, 0, False, False)
		team(1).setHasTech(iLaw, False, 1, False, False)
		
		goal.deactivate()
	
	def testEraFirstsMultiple(self):
		goal = Track.eraFirsts((iClassical, 1), (iMedieval, 1))
		goal.activate(0)
		
		team(0).setHasTech(iFeudalism, True, 0, True, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), '\n'.join(["0 / 1", "1 / 1"]))
		
		team(0).setHasTech(iFeudalism, False, 0, True, False)
		
		goal.deactivate()
	
	def testSunkShips(self):
		goal = Track.sunkShips(1)
		goal.activate(0)
		
		ourShip = makeUnit(0, iWarGalley, (3, 3))
		theirShip = makeUnit(1, iGalley, (3, 4))
		
		events.fireEvent("combatResult", ourShip, theirShip)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		ourShip.kill(False, -1)
		theirShip.kill(False, -1)
		
		goal.deactivate()
	
	def testSunkShipWinnerNotUs(self):
		goal = Track.sunkShips(1)
		goal.activate(0)
		
		theirShip = makeUnit(2, iWarGalley, (3, 3))
		thirdShip = makeUnit(1, iGalley, (3, 4))
		
		events.fireEvent("combatResult", theirShip, thirdShip)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		
		theirShip.kill(False, -1)
		thirdShip.kill(False, -1)
		
		goal.deactivate()
	
	def testSunkShipLandUnits(self):
		goal = Track.sunkShips(1)
		goal.activate(0)
		
		ourUnit = makeUnit(0, iSwordsman, (61, 31))
		theirUnit = makeUnit(1, iArcher, (62, 31))
		
		events.fireEvent("combatResult", ourUnit, theirUnit)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		
		ourUnit.kill(False, -1)
		theirUnit.kill(False, -1)
		
		goal.deactivate()
	
	def testTradeGoldPlayerGoldTrade(self):
		goal = Track.tradeGold(100)
		goal.activate(0)
		
		events.fireEvent("playerGoldTrade", 1, 0, 100)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100 / 100")
		
		goal.deactivate()
	
	def testTradeGoldPlayerGoldTradeDifferent(self):
		goal = Track.tradeGold(100)
		goal.activate(0)
		
		events.fireEvent("playerGoldTrade", 0, 1, 100)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 100")
		
		goal.deactivate()
	
	def testTradeGoldFromCities(self):
		goal = Track.tradeGold(100)
		goal.activate(0)
		
		city1 = player(0).initCity(57, 50)
		city2 = player(0).initCity(57, 52)
		
		player(0).setCivics(iCivicsEconomy, iFreeEnterprise)
		player(0).setCommercePercent(CommerceTypes.COMMERCE_GOLD, 100)
		
		self.assert_(city1.getTradeYield(YieldTypes.YIELD_COMMERCE) > 0)
		self.assert_(city2.getTradeYield(YieldTypes.YIELD_COMMERCE) > 0)
		
		iExpectedCommerce = city1.getTradeYield(YieldTypes.YIELD_COMMERCE) + city2.getTradeYield(YieldTypes.YIELD_COMMERCE)
		iExpectedCommerce *= player(0).getCommercePercent(CommerceTypes.COMMERCE_GOLD)
		iExpectedCommerce /= 100
		
		self.assert_(iExpectedCommerce > 0)
		
		events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "%d / 100" % iExpectedCommerce)
		
		city1.kill()
		city2.kill()
		
		player(0).setCivics(iCivicsEconomy, iReciprocity)
		player(0).setCommercePercent(CommerceTypes.COMMERCE_RESEARCH, 100)
		
		goal.deactivate()
		
	def testTradeGoldFromCitiesForeign(self):
		goal = Track.tradeGold(100)
		goal.activate(0)
		
		city1 = player(1).initCity(57, 50)
		city2 = player(1).initCity(57, 52)
		
		player(1).setCivics(iCivicsEconomy, iFreeEnterprise)
		player(1).setCommercePercent(CommerceTypes.COMMERCE_GOLD, 100)
		
		self.assert_(city1.getTradeYield(YieldTypes.YIELD_COMMERCE) + city2.getTradeYield(YieldTypes.YIELD_COMMERCE))
		
		events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		events.fireEvent("BeginPlayerTurn", 1, game.getGameTurn())
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 100")
		
		city1.kill()
		city2.kill()
		
		player(1).setCivics(iCivicsEconomy, iReciprocity)
		player(1).setCommercePercent(CommerceTypes.COMMERCE_RESEARCH, 100)
		
		goal.deactivate()
	
	def testTradeGoldFromDeals(self):
		goal = Track.tradeGold(100)
		goal.activate(0)
		
		player(0).changeGoldPerTurnByPlayer(1, 100)
		
		events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100 / 100")
		
		player(0).changeGoldPerTurnByPlayer(1, -100)
		
		goal.deactivate()
	
	def testTradeGoldFromDealsForeign(self):
		goal = Track.tradeGold(100)
		goal.activate(0)
		
		player(1).changeGoldPerTurnByPlayer(0, 100)
		
		events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		events.fireEvent("BeginPlayerTurn", 1, game.getGameTurn())
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 100")
		
		player(1).changeGoldPerTurnByPlayer(0, -100)
		
		goal.deactivate()
	
	def testTradeGoldFromTradeMission(self):
		goal = Track.tradeGold(1000)
		goal.activate(0)
		
		city = player(1).initCity(30, 25)
		
		events.fireEvent("tradeMission", iGreatMerchant, 0, 30, 25, 1000)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1000 / 1000")
		
		city.kill()
		
		goal.deactivate()
	
	def testTradeGoldFromTradeMissionOther(self):
		goal = Track.tradeGold(1000)
		goal.activate(0)
		
		city = player(2).initCity(30, 25)
		
		events.fireEvent("tradeMission", iGreatMerchant, 1, 30, 25, 1000)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1000")
		
		city.kill()
		
		goal.deactivate()
	
	def testRaidGoldPillage(self):
		goal = Track.raidGold(100)
		goal.activate(0)
		
		unit = makeUnit(0, iSwordsman, (61, 31))
		
		events.fireEvent("unitPillage", unit, iCottage, -1, 0, 100)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100 / 100")
		
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testRaidGoldPillageDifferent(self):
		goal = Track.raidGold(100)
		goal.activate(0)
		
		unit = makeUnit(1, iSwordsman, (61, 31))
		
		events.fireEvent("unitPillage", unit, iCottage, -1, 1, 100)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 100")
		
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testRaidGoldConquest(self):
		goal = Track.raidGold(100)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		
		events.fireEvent("cityCaptureGold", city, 0, 100)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100 / 100")
		
		city.kill()
		
		goal.deactivate()
	
	def testRaidGoldConquestDifferent(self):
		goal = Track.raidGold(100)
		goal.activate(0)
		
		city = player(1).initCity(61, 31)
		
		events.fireEvent("cityCaptureGold", city, 1, 100)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 100")
		
		city.kill()
		
		goal.deactivate()
	
	def testPillage(self):
		goal = Track.pillage(1)
		goal.activate(0)
		
		unit = makeUnit(0, iSwordsman, (61, 31))
		
		events.fireEvent("unitPillage", unit, iCottage, -1, 0, 0)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testPillageDifferent(self):
		goal = Track.pillage(1)
		goal.activate(0)
		
		unit = makeUnit(1, iSwordsman, (61, 31))
		
		events.fireEvent("unitPillage", unit, iCottage, -1, 1, 0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testAcquiredCitiesAcquired(self):
		goal = Track.acquiredCities(1)
		goal.activate(0)
		
		city = player(1).initCity(61, 31)
		
		events.fireEvent("cityAcquired", 1, 0, city, True, False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		city.kill()
		
		goal.deactivate()
	
	def testAcquiredCitiesBuilt(self):
		goal = Track.acquiredCities(1)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		
		events.fireEvent("cityBuilt", city)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		city.kill()
		
		goal.deactivate()
	
	def testPiracyGoldPillage(self):
		goal = Track.piracyGold(100)
		goal.activate(0)
		
		unit = makeUnit(0, iSwordsman, (61, 31))
		
		events.fireEvent("unitPillage", unit, iCottage, -1, 0, 100)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100 / 100")
		
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testPiracyGoldBlockade(self):
		goal = Track.piracyGold(100)
		goal.activate(0)
		
		events.fireEvent("blockade", 0, 100)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100 / 100")
		
		goal.deactivate()
	
	def testRazes(self):
		goal = Track.razes(1)
		goal.activate(0)
		
		city = player(1).initCity(61, 31)
		player(0).acquireCity(city, True, False)
		city = city_(61, 31)
		
		events.fireEvent("cityRazed", city, 0)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		city.kill()
		
		goal.deactivate()
	
	def testSlaveTradeGold(self):
		goal = Track.slaveTradeGold(100)
		goal.activate(0)
		
		events.fireEvent("playerSlaveTrade", 0, 100)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100 / 100")
		
		goal.deactivate()
	
	def testGreatGenerals(self):
		goal = Track.greatGenerals(1)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		unit = makeUnit(0, iGreatGeneral, (61, 31))
		
		events.fireEvent("greatPersonBorn", unit, 0, city)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		city.kill()
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testGreatGeneralsOther(self):
		goal = Track.greatGenerals(1)
		goal.activate(0)
		
		city = player(0).initCity(61, 31)
		unit = makeUnit(0, iGreatScientist, (61, 31))
		
		events.fireEvent("greatPersonBorn", unit, 0, city)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		
		city.kill()
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testResourceTradeGoldFromDeals(self):
		goal = Track.resourceTradeGold(100)
		goal.activate(0)
		
		player(0).changeGoldPerTurnByPlayer(1, 100)
		
		events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "100 / 100")
		
		player(0).changeGoldPerTurnByPlayer(1, -100)
		
		goal.deactivate()
	
	def testResourceTradeGoldFromDealsForeign(self):
		goal = Track.resourceTradeGold(100)
		goal.activate(0)
		
		player(1).changeGoldPerTurnByPlayer(0, 100)
		
		events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		events.fireEvent("BeginPlayerTurn", 1, game.getGameTurn())
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 100")
		
		player(1).changeGoldPerTurnByPlayer(0, -100)
		
		goal.deactivate()
	
	def testBrokeredPeace(self):
		goal = Track.brokeredPeace(1)
		goal.activate(0)
		
		events.fireEvent("peaceBrokered", 0, 1, 2)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		goal.deactivate()
	
	def testBrokeredPeaceOther(self):
		goal = Track.brokeredPeace(1)
		goal.activate(0)
		
		events.fireEvent("peaceBrokered", 2, 1, 0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
		
		goal.deactivate()
	
	def testEnslave(self):
		goal = Track.enslaves(1)
		goal.activate(0)
		
		unit = makeUnit(1, iSwordsman, (61, 31))
		
		events.fireEvent("enslave", 0, unit)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "1 / 1")
		
		unit.kill(False, -1)
		
		goal.deactivate()
	
	def testEnslaveExcluding(self):
		goal = Track.enslaves(2).excluding([iBabylonia])
		goal.activate(0)
		
		unit0 = makeUnit(iBabylonia, iSwordsman, (61, 31))
		unit1 = makeUnit(iHarappa, iSwordsman, (62, 31))
		
		events.fireEvent("enslave", 0, unit0)
		events.fireEvent("enslave", 0, unit1)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "1 / 2")
		
		unit0.kill(False, -1)
		unit1.kill(False, -1)
		
		goal.deactivate()


class TestBestCityGoals(ExtendedTestCase):

	def setUp(self):
		for plot in plots.all():
			plot.resetCultureConversion()
		
		self.assertEqual(cities.all().count(), 0)

	def tearDown(self):
		self.assertEqual(cities.all().count(), 0)

	def testBestPopulationCity(self):
		goal = BestCity.population(city(61, 31))
		goal.activate(0)
		
		city_ = player(0).initCity(61, 31)
		city_.setPopulation(10)
		city_.setName("Zero", False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "Zero (10)\n(No City) (0)")
		
		city_.kill()
	
	def testBestPopulationCityOtherLocation(self):
		goal = BestCity.population(city(61, 31))
		goal.activate(0)
		
		city_ = player(0).initCity(63, 31)
		city_.setPopulation(10)
		city_.setName("Zero", False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "Zero (10)\n(No City) (0)")
		
		city_.kill()
	
	def testBestPopulationCityOtherOwner(self):
		goal = BestCity.population(city(61, 31))
		goal.activate(0)
		
		city_ = player(1).initCity(61, 31)
		city_.setPopulation(10)
		city_.setName("One", False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "One (10)\n(No City) (0)")
		
		city_.kill()
	
	def testBestPopulationCityShowsSecondOnSuccess(self):
		goal = BestCity.population(city(61, 31))
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		city2 = player(2).initCity(65, 31)
		
		city0.setPopulation(10)
		city1.setPopulation(9)
		city2.setPopulation(8)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		city2.setName("Two", False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "Zero (10)\nOne (9)")
		
		city0.kill()
		city1.kill()
		city2.kill()
	
	def testBestPopulationCityShowsOwnSecondOnFailure(self):
		goal = BestCity.population(city(61, 31))
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		city2 = player(2).initCity(65, 31)
		
		city0.setPopulation(10)
		city1.setPopulation(11)
		city2.setPopulation(12)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		city2.setName("Two", False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "Two (12)\nZero (10)")
		
		city0.kill()
		city1.kill()
		city2.kill()
	
	def testBestPopulationCityNone(self):
		goal = BestCity.population(city(61, 31))
		goal.activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "(No City) (0)\n(No City) (0)")
	
	def testBestPopulationCityObjectiveBreaksTie(self):
		goal = BestCity.population(city(63, 31))
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(0).initCity(63, 31)
		city2 = player(0).initCity(65, 31)
		
		city0.setPopulation(10)
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		city2.setName("Two", False)
		
		self.assertEqual(bool(goal), True)
		self.assert_(str(goal).startswith("One (10)"))
		
		city0.kill()
		city1.kill()
		city2.kill()
	
	def testBestCultureCity(self):
		goal = BestCity.culture(city(61, 31))
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		city0.setCulture(0, 100, False)
		city1.setCulture(1, 50, False)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		
		self.assertEqual(city0.getCulture(0), 100)
		self.assertEqual(city1.getCulture(1), 50)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "Zero (100)\nOne (50)")
		
		city0.setCulture(0, 0, False)
		city1.setCulture(1, 0, False)
		
		city0.kill()
		city1.kill()
	
	def testBestCultureCityOtherLocation(self):
		goal = BestCity.culture(city(61, 31))
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(0).initCity(63, 31)
		
		city0.setCulture(0, 50, False)
		city1.setCulture(0, 100, False)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		
		self.assertEqual(city0.getCulture(0), 50)
		self.assertEqual(city1.getCulture(0), 100)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "One (100)\nZero (50)")
		
		city0.setCulture(0, 0, False)
		city1.setCulture(0, 0, False)
		
		city0.kill()
		city1.kill()
	
	def testBestCultureOtherOwner(self):
		goal = BestCity.culture(city(61, 31))
		goal.activate(0)
		
		city0 = player(1).initCity(61, 31)
		city1 = player(0).initCity(63, 31)
		
		city0.setCulture(1, 100, False)
		city1.setCulture(0, 50, False)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		
		self.assertEqual(city0.getCulture(1), 100)
		self.assertEqual(city1.getCulture(0), 50)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "Zero (100)\n(No City) (0)")
		
		city0.kill()
		city1.kill()


class TestBestPlayerGoals(ExtendedTestCase):
	
	def testBestPopulationPlayer(self):
		goal = BestPlayer.population()
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		city0.setPopulation(10)
		city1.setPopulation(9)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "Egypt (1000000)\nBabylonia (729000)")
		
		city0.kill()
		city1.kill()
	
	def testBestPopulationPlayerOther(self):
		goal = BestPlayer.population()
		goal.activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		city0.setPopulation(10)
		city1.setPopulation(11)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "Babylonia (1331000)\nEgypt (1000000)")
		
		city0.kill()
		city1.kill()
	
	def testBestTechPlayer(self):
		goal = BestPlayer.tech()
		goal.activate(0)
		
		for iTech in infos.techs():
			team(0).setHasTech(iTech, False, 0, False, False)
			team(1).setHasTech(iTech, False, 1, False, False)
		
		team(0).setHasTech(iGenetics, True, 0, False, False)
		team(1).setHasTech(iLaw, True, 1, False, False)
		
		self.assertEqual(bool(goal), True)
		self.assertEqual(str(goal), "Egypt (9000)\nBabylonia (280)")
		
		team(0).setHasTech(iGenetics, False, 0, False, False)
		team(1).setHasTech(iLaw, False, 1, False, False)
		
	def testBestTechPlayerOther(self):
		goal = BestPlayer.tech()
		goal.activate(0)
		
		for iTech in infos.techs():
			team(0).setHasTech(iTech, False, 0, False, False)
			team(1).setHasTech(iTech, False, 1, False, False)
		
		team(0).setHasTech(iLaw, True, 0, False, False)
		team(1).setHasTech(iGenetics, True, 1, False, False)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "Babylonia (9000)\nEgypt (280)")
		
		team(0).setHasTech(iLaw, False, 0, False, False)
		team(1).setHasTech(iGenetics, False, 1, False, False)


class TestRouteConnection(ExtendedTestCase):

	def testDirectConnection(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad])
		goal.activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
			
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), True)
		
		start.kill()
		target.kill()
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(-1)
			plot.setOwner(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
	
	def testNoRoute(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad])
		goal.activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), False)
		
		start.kill()
		target.kill()
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setOwner(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
	
	def testNoCulture(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad])
		goal.activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), False)
		
		start.kill()
		target.kill()
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
	
	def testDifferentRouteType(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRailroad])
		goal.activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 41)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		for iTech in [iLeverage, iRailroad]:
			team(0).setHasTech(iTech, True, 0, False, False)
		
		self.assertEqual(bool(goal), False)
		
		start.kill()
		target.kill()
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(-1)
			plot.setOwner(-1)
		
		for iTech in [iLeverage, iRailroad]:
			team(0).setHasTech(iTech, False, 0, False, False)
	
	def testNoRouteTech(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad])
		goal.activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		self.assertEqual(bool(goal), False)
		
		start.kill()
		target.kill()
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(-1)
			plot.setOwner(-1)
	
	def testNoStartCity(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad])
		goal.activate(0)
		
		target = player(0).initCity(64, 41)
		
		for plot in plots.rectangle((61, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), False)
		
		target.kill()
		
		for plot in plots.rectangle((61, 31), (63, 31)):
			plot.setRouteType(-1)
			plot.setOwner(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
	
	def testDifferentStartCityOwner(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad])
		goal.activate(0)
		
		start = player(1).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), False)
		
		start.kill()
		target.kill()
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(-1)
			plot.setOwner(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
	
	def testNoTargetCity(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad])
		goal.activate(0)
		
		start = player(0).initCity(61, 31)
		
		for plot in plots.rectangle((62, 31), (64, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), False)
		
		start.kill()
		
		for plot in plots.rectangle((62, 31), (64, 31)):
			plot.setRouteType(-1)
			plot.setOwner(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
		
	def testTargetCityDifferentOwner(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad])
		goal.activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(1).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), False)
		
		start.kill()
		target.kill()
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(-1)
			plot.setOwner(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
	
	def testIndirectConnection(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad])
		goal.activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		area = plots.of([(60, 32), (61, 33), (62, 33), (63, 33), (64, 33), (65, 32)])
		for plot in area:
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), True)
		
		start.kill()
		target.kill()
		
		for plot in area:
			plot.setRouteType(-1)
			plot.setOwner(-1)
	
	def testConnectionThroughCity(self):
		goal = RouteConnection(plots.of([(63, 31)]), plots.of([(65, 31)]), [iRouteRoad])
		goal.activate(0)
		
		start = player(0).initCity(61, 31)
		middle = player(0).initCity(63, 31)
		target = player(0).initCity(65, 31)
		
		area = plots.of([(62, 31), (64, 31)])
		for plot in area:
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), True)
		
		for city in [start, middle, target]:
			city.kill()
		
		for plot in area:
			plot.setRouteType(-1)
			plot.setOwner(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
	
	def testConnectionThroughCityDifferentOwner(self):
		goal = RouteConnection(plots.of([(63, 31)]), plots.of([(65, 31)]), [iRouteRoad])
		goal.activate(0)
		
		start = player(0).initCity(61, 31)
		middle = player(1).initCity(63, 31)
		target = player(0).initCity(65, 31)
		
		area = plots.of([(62, 31), (64, 31)])
		for plot in area:
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), False)
		
		for city in [start, middle, target]:
			city.kill()
		
		for plot in area:
			plot.setRouteType(-1)
			plot.setOwner(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
	
	def testMultipleStarts(self):
		starts = plots.rectangle((61, 31), (61, 33))
		targets = plots.of([(64, 31)])
		goal = RouteConnection(starts, targets, [iRouteRoad])
		goal.activate(0)
		
		start1 = player(0).initCity(61, 33)
		start2 = player(1).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		area = plots.rectangle((62, 32), (63, 32))
		for plot in area:
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), True)
		
		for city in [start1, start2, target]:
			city.kill()
		
		for plot in area:
			plot.setRouteType(-1)
			plot.setOwner(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
	
	def testMultipleTargets(self):
		starts = plots.of([(61, 31)])
		targets = plots.rectangle((64, 31), (64, 33))
		goal = RouteConnection(starts, targets, [iRouteRoad])
		goal.activate(0)
		
		start = player(0).initCity(61, 31)
		target1 = player(1).initCity(64, 31)
		target2 = player(0).initCity(64, 33)
		
		area = plots.rectangle((62, 32), (63, 32))
		for plot in area:
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), True)
		
		for city in [start, target1, target2]:
			city.kill()
		
		for plot in area:
			plot.setRouteType(-1)
			plot.setOwner(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
	
	def testWithStartOwners(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad]).withStartOwners()
		goal.activate(0)
		
		start = player(1).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(1)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), True)
		
		start.kill()
		target.kill()
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(-1)
			plot.setOwner(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
	
	def testWithStartOwnersIncludingTarget(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad]).withStartOwners()
		goal.activate(0)
		
		start = player(1).initCity(61, 31)
		target = player(1).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(1)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), False)
		
		start.kill()
		target.kill()
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(-1)
			plot.setOwner(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
	
	def testWithLazyCapital(self):
		goal = RouteConnection(plots.lazy().capital(0), plots.of([(64, 31)]), [iRouteRoad])
		goal.activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		start.setHasRealBuilding(iPalace, True)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), True)
		
		start.kill()
		target.kill()
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(-1)
			plot.setOwner(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
	
	def testWithLazyCapitalElsewhere(self):
		goal = RouteConnection(plots.lazy().capital(0), plots.of([(64, 31)]), [iRouteRoad])
		goal.activate(0)
		
		capital = player(0).initCity(35, 35)
		capital.setHasRealBuilding(iPalace, True)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), False)
		
		for city in [capital, start, target]:
			city.kill()
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(-1)
			plot.setOwner(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
	
	def testMultipleTargetsAll(self):
		goal = RouteConnection(plots.of([(63, 31)]), (plots.of([(61, 31)]), plots.of([(65, 31)])), [iRouteRoad])
		goal.activate(0)
		
		start = player(0).initCity(63, 31)
		target1 = player(0).initCity(61, 31)
		target2 = player(0).initCity(65, 31)
		
		for plot in plots.of([(62, 31), (64, 31)]):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), True)
		
		for city in [start, target1, target2]:
			city.kill()
		
		for plot in plots.of([(62, 31), (64, 31)]):
			plot.setRouteType(-1)
			plot.setOwner(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
	
	def testMultipleTargetsSome(self):
		goal = RouteConnection(plots.of([(63, 31)]), (plots.of([(61, 31)]), plots.of([(65, 31)])), [iRouteRoad])
		goal.activate(0)
		
		start = player(0).initCity(63, 31)
		target1 = player(0).initCity(61, 31)
		target2 = player(0).initCity(65, 31)
		
		for plot in plots.of([(62, 31)]):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		self.assertEqual(bool(goal), False)
		
		for city in [start, target1, target2]:
			city.kill()
		
		for plot in plots.of([(62, 31)]):
			plot.setRouteType(-1)
			plot.setOwner(-1)
		
		team(0).setHasTech(iLeverage, False, 0, False, False)
		
		
class SubGoal(BaseGoal):

	types = ArgumentProcessor([int], None, 0)

	def __init__(self, *arguments):
		super(SubGoal, self).__init__(*arguments)
		
		self.string = ""
		self.iMinArgument = 0
	
	def condition(self, argument):
		return argument >= self.iMinArgument
	
	def __str__(self):
		return self.string


class TestAllGoal(ExtendedTestCase):

	def testActivate(self):
		goal1 = SubGoal()
		goal2 = SubGoal()
		goal = All(goal1, goal2)
		
		def callback():
			pass
		goal.activate(0, callback)
		
		self.assertEqual(goal.iPlayer, 0)
		self.assertEqual(goal1.iPlayer, 0)
		self.assertEqual(goal2.iPlayer, 0)

		self.assertEqual(goal.callback, callback)
		self.assertEqual(goal1.callback, goal.subgoal_callback)
		self.assertEqual(goal2.callback, goal.subgoal_callback)
	
	def testOneSuccess(self):
		goal1 = SubGoal()
		goal2 = SubGoal()
		goal = All(goal1, goal2)
		
		goal.activate(0)
		
		goal1.succeed()
		
		self.assertEqual(goal1.state, SUCCESS)
		self.assertEqual(goal2.state, POSSIBLE)
		self.assertEqual(goal.state, POSSIBLE)
	
	def testAllSuccess(self):
		goal1 = SubGoal()
		goal2 = SubGoal()
		goal = All(goal1, goal2)
		
		goal.activate(0)
		
		goal1.succeed()
		goal2.succeed()
		
		self.assertEqual(goal1.state, SUCCESS)
		self.assertEqual(goal2.state, SUCCESS)
		self.assertEqual(goal.state, SUCCESS)
	
	def testOneFailure(self):
		goal1 = SubGoal()
		goal2 = SubGoal()
		goal = All(goal1, goal2)
		
		goal.activate(0)
		
		goal1.fail()
		
		self.assertEqual(goal1.state, FAILURE)
		self.assertEqual(goal2.state, FAILURE)
		self.assertEqual(goal.state, FAILURE)
		
	def testString(self):
		goal1 = SubGoal()
		goal2 = SubGoal()
		
		goal1.string = "goal1"
		goal2.string = "goal2"
		
		goal = All(goal1, goal2)
		goal.activate(0)
		
		self.assertEqual(str(goal1), "goal1")
		self.assertEqual(str(goal2), "goal2")
		self.assertEqual(str(goal), "goal1\ngoal2")


class TestSomeGoal(ExtendedTestCase):

	def testActivate(self):
		subgoal = SubGoal()
		goal = Some(subgoal, 1)
		
		def callback():
			pass
		goal.activate(0, callback)
		
		self.assertEqual(goal.iPlayer, 0)
		self.assertEqual(subgoal.iPlayer, 0)
		
		self.assertEqual(goal.callback, callback)
		self.assertEqual(subgoal.callback, goal.subgoal_callback)
	
	def testNoSubgoals(self):
		subgoal = SubGoal(0, 1, 2)
		subgoal.iMinArgument = 10
		goal = Some(subgoal, 2)
		
		self.assertEqual(subgoal.condition(0), False)
		self.assertEqual(subgoal.condition(1), False)
		self.assertEqual(subgoal.condition(2), False)
		
		self.assertEqual(bool(goal), False)
	
	def testLessSubgoals(self):
		subgoal = SubGoal(0, 1, 2)
		subgoal.iMinArgument = 2
		goal = Some(subgoal, 2)
		
		self.assertEqual(subgoal.condition(0), False)
		self.assertEqual(subgoal.condition(1), False)
		self.assertEqual(subgoal.condition(2), True)
		
		self.assertEqual(bool(goal), False)
	
	def testEqualSubgoals(self):
		subgoal = SubGoal(0, 1, 2)
		subgoal.iMinArgument = 1
		goal = Some(subgoal, 2)
		
		self.assertEqual(subgoal.condition(0), False)
		self.assertEqual(subgoal.condition(1), True)
		self.assertEqual(subgoal.condition(2), True)
		
		self.assertEqual(bool(goal), True)
	
	def testMoreSubgoals(self):
		subgoal = SubGoal(0, 1, 2)
		subgoal.iMinArgument = 0
		goal = Some(subgoal, 2)
		
		self.assertEqual(subgoal.condition(0), True)
		self.assertEqual(subgoal.condition(1), True)
		self.assertEqual(subgoal.condition(2), True)
		
		self.assertEqual(bool(goal), True)
	
	def testCheckSubgoalChecksGoal(self):
		subgoal = SubGoal(0, 1, 2)
		subgoal.iMinArgument = 1
		goal = Some(subgoal, 2)
		
		self.assertEqual(bool(subgoal), False)
		self.assertEqual(bool(goal), True)
		self.assertEqual(goal.state, POSSIBLE)
		
		self.assertEqual(subgoal.condition(0), False)
		self.assertEqual(subgoal.condition(1), True)
		self.assertEqual(subgoal.condition(2), True)
		
		subgoal.check()
		
		self.assertEqual(goal.state, SUCCESS)


class CityGoal(BaseGoal):

	types = ArgumentProcessor([], CyCity, 0)
	
	def __init__(self, *arguments):
		super(CityGoal, self).__init__(*arguments)
		
		self.complete = False
		self.string = ""
	
	def condition(self, *arguments):
		return self.complete
		
	def __str__(self):
		return self.string
		
class TestDifferentCities(ExtendedTestCase):

	def testCompleteWithDifferentCities(self):
		goal1 = CityGoal(capital())
		goal2 = CityGoal(capital())
		goal1.string = "one"
		goal2.string = "two"
		goal = DifferentCities(goal1, goal2)
		goal.activate(0)
		
		self.assertEqual(str(goal), "one\ntwo")
	
		city1 = player(0).initCity(61, 31)
		city1.setHasRealBuilding(iPalace, True)
		city1.setName("CityOne", False)
		
		self.assertEqual(location(capital_(0)), (61, 31))
		
		self.assertEqual(str(goal), "CityOne: one\nCityOne: two")
		
		goal1.succeed()
		self.assertEqual(goal1.state, SUCCESS)
		self.assertEqual(goal.state, POSSIBLE)
		self.assertEqual(bool(goal), False)
		
		self.assertEqual(goal.recorded(goal1), (61, 31))
		self.assertEqual(goal.recorded(goal2), None)
		
		self.assertEqual(str(goal), "CityOne: one\nCityOne: two")
		
		city2 = player(0).initCity(63, 31)
		city1.setHasRealBuilding(iPalace, False)
		city2.setHasRealBuilding(iPalace, True)
		city2.setName("CityTwo", False)
		
		self.assertEqual(location(capital_(0)), (63, 31))
		
		goal2.succeed()
		
		self.assertEqual(goal2.state, SUCCESS)
		self.assertEqual(goal.state, SUCCESS)
		
		self.assertEqual(goal.recorded(goal1), (61, 31))
		self.assertEqual(goal.recorded(goal2), (63, 31))
		
		self.assertEqual(str(goal), "CityOne: one\nCityTwo: two")
		
		city1.kill()
		city2.kill()
	
	def testCompleteWithIdenticalCity(self):
		goal1 = CityGoal(capital())
		goal2 = CityGoal(capital())
		goal1.string = "one"
		goal2.string = "two"
		
		goal = DifferentCities(goal1, goal2)
		goal.activate(0)
		
		self.assertEqual(str(goal), "one\ntwo")
		
		city1 = player(0).initCity(61, 31)
		city1.setHasRealBuilding(iPalace, True)
		city1.setName("CityOne", False)
		
		self.assertEqual(location(capital_(0)), (61, 31))
		
		self.assertEqual(str(goal), "CityOne: one\nCityOne: two")
		
		goal1.succeed()
		self.assertEqual(goal1.state, SUCCESS)
		self.assertEqual(goal.state, POSSIBLE)
		self.assertEqual(bool(goal), False)
		
		self.assertEqual(goal.recorded(goal1), (61, 31))
		self.assertEqual(goal.recorded(goal2), None)
		
		self.assertEqual(str(goal), "CityOne: one\nCityOne: two")
		
		goal2.succeed()
		self.assertEqual(goal2.state, FAILURE)
		self.assertEqual(goal.state, FAILURE)
		self.assertEqual(bool(goal), False)
		
		self.assertEqual(goal.recorded(goal1), (61, 31))
		self.assertEqual(goal.recorded(goal2), (61, 31))
		
		self.assertEqual(str(goal), "CityOne: one\nCityOne: two")
		
		city1.kill()
	
	def testCityChangedAfterIncomplete(self):
		goal1 = CityGoal(capital())
		goal2 = CityGoal(capital())
		goal1.string = "one"
		goal2.string = "two"
		
		goal = DifferentCities(goal1, goal2)
		goal.activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setHasRealBuilding(iPalace, True)
		city1.setName("CityOne", False)
		
		self.assertEqual(location(capital_(0)), (61, 31))
		
		goal1.succeed()
		goal2.succeed()
		
		self.assertEqual(goal2.state, FAILURE)
		self.assertEqual(goal.state, FAILURE)
		self.assertEqual(bool(goal), False)
		
		self.assertEqual(goal.recorded(goal1), (61, 31))
		self.assertEqual(goal.recorded(goal2), (61, 31))
		
		self.assertEqual(str(goal), "CityOne: one\nCityOne: two")
		
		city2 = player(0).initCity(63, 31)
		city1.setHasRealBuilding(iPalace, False)
		city2.setHasRealBuilding(iPalace, True)
		city2.setName("CityTwo", False)
		
		self.assertEqual(location(capital_(0)), (63, 31))
		
		self.assertEqual(str(goal), "CityOne: one\nCityOne: two")
		
		city1.kill()
		city2.kill()
	

test_cases = [
	TestGetNumArgs,
	TestEventHandlers,
	TestDeferred,
	TestAggregate,
	TestArguments,
	TestArgumentProcessor,
	TestArgumentProcessorBuilder,
	TestBaseGoal,
	TestConditionGoals,
	TestCountGoals,
	TestPercentageGoals,
	TestTriggerGoals,
	TestTrackGoals,
	TestBestCityGoals,
	TestBestPlayerGoals,
	TestRouteConnection,
	TestAllGoal,
	TestSomeGoal,
	TestDifferentCities,
]


suite = TestSuite([makeSuite(case) for case in test_cases])
TextTestRunner(verbosity=2).run(suite)