from VictoryGoals import *
from unittest import *
from Victories import disable as disable_victories

from inspect import isfunction

import cPickle as pickle


class ExtendedTestCase(TestCase):

	SUCCESS_CHAR = game.getSymbolID(FontSymbols.SUCCESS_CHAR)
	FAILURE_CHAR = game.getSymbolID(FontSymbols.FAILURE_CHAR)
	
	#SUCCESS_CHAR = "Y"
	#FAILURE_CHAR = "N"

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
		
		try:
			onCombatResult(PlayerContainer(0), (winningUnit, losingUnit))
			self.assertEqual(self.iCallCount, 1)
			
			onCombatResult(PlayerContainer(1), (winningUnit, losingUnit))
			self.assertEqual(self.iCallCount, 1)
		finally:
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
		
		try:
			onUnitPillage(PlayerContainer(0), (unit, 0, -1, 0, 100))
			self.assertEqual(self.iIncrement, 100)
		
			onUnitPillage(PlayerContainer(1), (unit, 0, -1, 0, 100))
			self.assertEqual(self.iIncrement, 100)
		finally:
			unit.kill(False, -1)
	
	def testCityCaptureGold(self):
		onCityCaptureGold = self.handlers.get("cityCaptureGold", self.increment)
		city = player(1).initCity(0, 0)
		
		try:
			onCityCaptureGold(PlayerContainer(0), (city, 0, 100))
			self.assertEqual(self.iIncrement, 100)
			
			onCityCaptureGold(PlayerContainer(1), (city, 0, 100))
			self.assertEqual(self.iIncrement, 100)
		finally:
			city.kill()
	
	def testCityAcquired(self):
		onCityAcquired = self.handlers.get("cityAcquired", self.trackCall)
		city = player(1).initCity(0, 0)
		
		try:
			onCityAcquired(PlayerContainer(0), (1, 0, city, False, False))
			self.assertEqual(self.iCallCount, 1)
			
			onCityAcquired(PlayerContainer(1), (1, 0, city, False, False))
			self.assertEqual(self.iCallCount, 1)
		finally:
			city.kill()
	
	def testCityBuilt(self):
		onCityBuilt = self.handlers.get("cityBuilt", self.trackCall)
		city = player(0).initCity(0, 0)

		try:
			onCityBuilt(PlayerContainer(0), (city,))
			self.assertEqual(self.iCallCount, 1)
			
			onCityBuilt(PlayerContainer(1), (city,))
			self.assertEqual(self.iCallCount, 1)
		finally:
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
		
		try:
			onCityRazed(PlayerContainer(0), (city, 0))
			self.assertEqual(self.iCallCount, 1)
		
			onCityRazed(PlayerContainer(1), (city, 0))
			self.assertEqual(self.iCallCount, 1)
		finally:
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
		onFirstContact = self.handlers.get("firstContact", self.trackCall)
		
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
		
		try:
			onBuildingBuilt(PlayerContainer(0), (city, iGranary))
			self.assertEqual(self.capturedArgument, (city, iGranary,))
			
			onBuildingBuilt(PlayerContainer(1), (city, iLibrary))
			self.assertEqual(self.capturedArgument, (city, iGranary,))
		finally:
			city.kill()
	
	def testProjectBuilt(self):
		onProjectBuilt = self.handlers.get("projectBuilt", self.captureArgument)
		city = player(0).initCity(0, 0)
		
		try:
			onProjectBuilt(PlayerContainer(0), (city, iTheInternet))
			self.assertEqual(self.capturedArgument, (iTheInternet,))
			
			onProjectBuilt(PlayerContainer(1), (city, iGoldenRecord))
			self.assertEqual(self.capturedArgument, (iTheInternet,))
		finally:
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
	
	def testCombatGold(self):
		onCombatGold = self.handlers.get("combatGold", self.increment)
		
		onCombatGold(PlayerContainer(0), (0, None, 100))
		self.assertEqual(self.iIncrement, 100)
		
		onCombatGold(PlayerContainer(0), (1, None, 100))
		self.assertEqual(self.iIncrement, 100)
	
	def testCombatFood(self):
		onCombatFood = self.handlers.get("combatFood", self.increment)
		
		onCombatFood(PlayerContainer(0), (0, None, 100))
		self.assertEqual(self.iIncrement, 100)
		
		onCombatFood(PlayerContainer(0), (1, None, 100))
		self.assertEqual(self.iIncrement, 100)
	
	def testSacrificeHappiness(self):
		onSacrificeHappiness = self.handlers.get("sacrificeHappiness", self.trackCall)
		
		onSacrificeHappiness(PlayerContainer(0), (0, None))
		self.assertEqual(self.iCallCount, 1)
		
		onSacrificeHappiness(PlayerContainer(0), (1, None))
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
		
		try:
			self.assertEqual(capital_(0).getID(), city.getID())
		finally:
			city.kill()
		
	def testCapitalBeforeCity(self):
		capital_ = capital()
		city = player(0).initCity(0, 0)
		city.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqual(capital_(0).getID(), city.getID())
		finally:
			city.kill()
		
	def testCityVarargs(self):
		city_ = player(0).initCity(0, 0)
		deferredCity = city(0, 0)
		
		try:
			self.assertEqual(deferredCity().getID(), city_.getID())
		finally:
			city_.kill()
	
	def testCityWithoutCities(self):
		deferredCity = city((0, 0))
		self.assertEqual(deferredCity(), None)
	
	def testCityAfterCity(self):
		city_ = player(0).initCity(0, 0)
		deferredCity = city((0, 0))
		
		try:
			self.assertEqual(deferredCity().getID(), city_.getID())
		finally:
			city_.kill()
	
	def testCityBeforeCity(self):
		deferredCity = city((0, 0))
		city_ = player(0).initCity(0, 0)
		
		try:
			self.assertEqual(deferredCity().getID(), city_.getID())
		finally:
			city_.kill()
	
	def testWonderWithoutCities(self):
		city = wonder(iPyramids)
		self.assertEqual(city(), None)
	
	def testWonderWithoutWonder(self):
		city = wonder(iPyramids)
		city_ = player(0).initCity(0, 0)
		
		try:
			self.assertEqual(city(), None)
		finally:
			city_.kill()
	
	def testWonderWithWonder(self):
		city = wonder(iPyramids)
		city_ = player(0).initCity(0, 0)
		city_.setHasRealBuilding(iPyramids, True)
		
		try:
			self.assertEqual(city().getID(), city_.getID())
		finally:
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
	
	def testGeneratorArgument(self):
		agg = sum(i for i in xrange(3))
		self.assertEqual(agg.items, [0, 1, 2])
	
	def testVarargsArgument(self):
		agg = sum(0, 1, 2)
		self.assertEqual(agg.items, [0, 1, 2])
	
	def testListArguments(self):
		agg = sum([0, 1, 2])
		self.assertEqual(agg.items, [0, 1, 2])
	
	def testTupleArguments(self):
		agg = sum((0, 1, 2))
		self.assertEqual(agg.items, [0, 1, 2])
	
	def testString(self):
		agg = sum(iWarrior, iArcher, iSwordsman)
		formatter = lambda item: plural(infos.unit(item).getText())
		
		self.assertEqual(agg.format(formatter), "Warriors, Archers and Swordsmen")
	
	def testStringPlots(self):
		agg = sum(plots.region(rItaly).named("ITALY"), plots.region(rBritain).named("BRITAIN"))
		formatter = lambda item: item.name()
		
		self.assertEqual(agg.format(formatter), "Italy and Britain")
	
	def testStringNamed(self):
		agg = sum(iPyramids, iParthenon, iColossus).named("WONDERS")
		formatter = lambda item: infos.building(item).getText()
		
		self.assertEqual(agg.format(formatter), "wonders")


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
	
	def testOwnerInluded(self):
		arguments = Arguments([])
		arguments.iPlayer = 0
		arguments.owner_included = True
		
		iterated = [x for x in arguments]
		
		self.assertEqual(iterated, [(0,)])
	
	def testSubjectAndObjectives(self):
		arguments = Arguments(subject="subject", objectives=[(1,), (2,), (3,)])
		
		iterated = [x for x in arguments]
		
		self.assertEqual(iterated, [("subject", 1), ("subject", 2), ("subject", 3)])
	
	def testSubjectAndOwnerIncluded(self):
		arguments = Arguments(objectives=[], subject="subject")
		arguments.iPlayer = 0
		arguments.owner_included = True
		
		iterated = [x for x in arguments]
		
		self.assertEqual(iterated, [("subject", 0)])
	
	def testObjectivesAndOwnerIncluded(self):
		arguments = Arguments(objectives=[(1,), (2,), (3,)])
		arguments.iPlayer = 0
		arguments.owner_included = True
		
		iterated = [x for x in arguments]
		
		self.assertEqual(iterated, [(1, 0), (2, 0), (3, 0)])
	
	def testSubjectAndObjectivesAndOwnerIncluded(self):
		arguments = Arguments(subject="subject", objectives=[(1,), (2,), (3,)])
		arguments.iPlayer = 0
		arguments.owner_included = True
		
		iterated = [x for x in arguments]
		
		self.assertEqual(iterated, [("subject", 1, 0), ("subject", 2, 0), ("subject", 3, 0)])
	
	def testResolvesDeferred(self):
		deferred = DeferredStateReligionBuilding(infos.type('SPECIALBUILDING_CATHEDRAL'))
		arguments = Arguments(objectives=[(1, deferred), (2, deferred)])
		arguments.iPlayer = 0
		
		player(0).setLastStateReligion(iCatholicism)
		
		try:
			iterated = [x for x in arguments]
		
			self.assertEqual(iterated, [(1, iCatholicCathedral), (2, iCatholicCathedral)])
		finally:
			player(0).setLastStateReligion(-1)
	
	def testCreateSubjectDeferred(self):
		arguments = Arguments(objectives=[], subject=plots.rectangle((0, 0), (1, 1)))
		self.assertType(arguments.subject, DeferredCollection)
		
		arguments.create()
		self.assertType(arguments.subject, Plots)
	
	def testCreateSubjectAggregate(self):
		arguments = Arguments(objectives=[], subject=sum(plots.rectangle((0, 0), (1, 1))))
		self.assertType(arguments.subject, SumAggregate)
		self.assertType(arguments.subject.items[0], DeferredCollection)
		
		arguments.create()
		self.assertType(arguments.subject, SumAggregate)
		self.assertType(arguments.subject.items[0], Plots)
	
	def testCreateSubjectOther(self):
		arguments = Arguments(objectives=[], subject=1)
		self.assertType(arguments.subject, int)
		
		arguments.create()
		self.assertType(arguments.subject, int)
	
	def testCreateObjectives(self):
		arguments = Arguments(objectives=[(plots.region(0), sum(plots.region(0)), 0), (plots.region(1), sum(plots.region(1)), 1)])
		self.assertEqual(len(arguments.objectives), 2)
		self.assertType(arguments.objectives[0][0], DeferredCollection)
		self.assertType(arguments.objectives[0][1], SumAggregate)
		self.assertType(arguments.objectives[0][1].items[0], DeferredCollection)
		self.assertType(arguments.objectives[0][2], int)
		self.assertType(arguments.objectives[1][0], DeferredCollection)
		self.assertType(arguments.objectives[1][1], SumAggregate)
		self.assertType(arguments.objectives[1][1].items[0], DeferredCollection)
		self.assertType(arguments.objectives[1][2], int)
		
		arguments.create()
		self.assertEqual(len(arguments.objectives), 2)
		self.assertType(arguments.objectives[0][0], Plots)
		self.assertType(arguments.objectives[0][1], SumAggregate)
		self.assertType(arguments.objectives[0][1].items[0], Plots)
		self.assertType(arguments.objectives[0][2], int)
		self.assertType(arguments.objectives[1][0], Plots)
		self.assertType(arguments.objectives[1][1], SumAggregate)
		self.assertType(arguments.objectives[1][1].items[0], Plots)
		self.assertType(arguments.objectives[1][2], int)


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
		types = ArgumentProcessor([CvUnitInfo])
		
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
		self.assertType(objectives[0][0], SumAggregate)
	
	def testDefaultPlayerValue(self):
		types = ArgumentProcessor([Players])
		
		result = types.process()
		self.assertEqual(result.objectives, [(players.major().alive(),)])
	
	def testCityType(self):
		types = ArgumentProcessor(subject_type=CyCity)
		
		result = types.process(city((100, 100)))
		self.assertType(result, Arguments)
		self.assertType(result.subject, DeferredCity)
		
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
		self.assertType(result.subject, DeferredCity)
		
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
	
	def testAttitudeTypesTransform(self):
		types = ArgumentProcessor([AttitudeTypes])
		
		result = types.process(AttitudeTypes.ATTITUDE_FURIOUS)
		self.assertEqual(result.objectives, [(0,)])
	
	def testUnitCombatTypesTransform(self):
		types = ArgumentProcessor([UnitCombatTypes])
		
		result = types.process(UnitCombatTypes.UNITCOMBAT_GUN)
		self.assertEqual(result.objectives, [(6,)])
	
	def testUnitCombatTypesTransformAggregate(self):
		types = ArgumentProcessor([UnitCombatTypes])
		
		result = types.process(sum(UnitCombatTypes.UNITCOMBAT_MELEE, UnitCombatTypes.UNITCOMBAT_GUN))
		self.assertEqual(result.objectives[0][0].items, [4, 6])
		self.assertType(result.objectives[0][0].items[0], int)
		self.assertType(result.objectives[0][0].items[1], int)
	
	def testAggregateIsValidForPlots(self):
		types = ArgumentProcessor([Plots])
		
		result = types.process(sum([plots.of([(61, 31)])]))
		self.assertEqual(len(result.objectives), 1)
		self.assertType(result.objectives[0], tuple)
		self.assertEqual(len(result.objectives[0]), 1)
		self.assertType(result.objectives[0][0], SumAggregate)


class TestArgumentProcessorFormat(ExtendedTestCase):
	
	def setUp(self):
		self.types = ArgumentProcessor([])
	
	def testFormatValueCity(self):
		city = player(0).initCity(61, 31)
		city.setName("CityName", False)
		
		try:
			self.assertEqual(self.types.format_value(CyCity, city), "CityName")
		finally:
			city.kill()
	
	def testFormatValueCityNoCity(self):
		self.assertEqual(self.types.format_value(CyCity, None), "(No City)")
	
	def testFormatValueAttitudeType(self):
		self.assertEqual(self.types.format_value(AttitudeTypes, AttitudeTypes.ATTITUDE_PLEASED), "pleased")
	
	def testFormatValueCultureLevelInfo(self):
		self.assertEqual(self.types.format_value(CvCultureLevelInfo, iCultureLevelInfluential), "influential")
	
	def testFormatValueBuildingInfo(self):
		self.assertEqual(self.types.format_value(CvBuildingInfo, iGranary), "Granary")
		self.assertEqual(self.types.format_value(CvBuildingInfo, iParthenon), "the Parthenon")
	
	def testFormatValueBonusInfo(self):
		self.assertEqual(self.types.format_value(CvBonusInfo, iWheat), "Wheat")
		self.assertEqual(self.types.format_value(CvBonusInfo, iSpices), "Spice")
	
	def testFormatValueBaseInfo(self):
		self.assertEqual(self.types.format_value(CvTechInfo, iGeography), "Geography")
		self.assertEqual(self.types.format_value(CvUnitInfo, iFrigate), "Frigate")
		self.assertEqual(self.types.format_value(CvSpecialistInfo, iSpecialistGreatArtist), "Great Artist")
	
	def testFormatValuePlots(self):
		self.assertEqual(self.types.format_value(Plots, plots.region(rBritain).clear_named("Britain")), "Britain")
	
	def testFormatValueInt(self):
		text = self.types.format_value(int, 12)
		
		self.assertType(text, str)
		self.assertEqual(text, "12")
	
	def testFormatValueNumberWord(self):
		options = FormatOptions()
		options.bNumberWord = True
		
		types = ArgumentProcessor([])
		types.options = options
		
		self.assertEqual(types.format_value(int, 1), "a")
		self.assertEqual(types.format_value(int, 2), "two")
		self.assertEqual(types.format_value(int, 10), "ten")
	
	def testFormatValueDeferred(self):
		self.assertEqual(self.types.format_value(CyCity, capital().named("BABYLON")), "Babylon")
	
	def testFormatValueAggregate(self):
		self.assertEqual(self.types.format_value(CvBuildingInfo, sum(iGranary, iWalls, iMonument)), "Granaries, Walls and Monuments")
	
	def testFormatValueAggregateNamed(self):
		self.assertEqual(self.types.format_value(CvBuildingInfo, sum(iOrthodoxTemple, iCatholicTemple, iProtestantTemple).named("TEMPLES")), "temples")
	
	def testFormatValueOther(self):
		self.assertEqual(self.types.format_value(str, "hello hello"), "hello hello")

	def testFormatObjectiveInfoCount(self):
		types = ArgumentProcessor([CvBuildingInfo, int])
		
		self.assertEqual(types.format_objective((iGranary, 1)), "a Granary")
		self.assertEqual(types.format_objective((iGranary, 3)), "three Granaries")
	
	def testFormatObjectiveBasic(self):
		types = ArgumentProcessor([CvTechInfo, CvUnitInfo, CvSpecialistInfo])
		
		self.assertEqual(types.format_objective((iGeography, iFrigate, iSpecialistGreatArtist)), "Geography Frigate Great Artist")
	
	def testFormatObjectiveCity(self):
		types = ArgumentProcessor([int])
		
		options = FormatOptions().city()
		types.options = options
		
		self.assertEqual(types.format_objective((1,)), "a city")
		self.assertEqual(types.format_objective((5,)), "five cities")
	
	def testFormatObjectiveNoSingularCount(self):
		types = ArgumentProcessor([CvBuildingInfo, int])
		
		options = FormatOptions().noSingularCount(isWonder)
		types.options = options
		
		self.assertEqual(types.format_objective((iGranary, 1)), "a Granary")
		self.assertEqual(types.format_objective((iParthenon, 1)), "the Parthenon")
		self.assertEqual(types.format_objective((iGranary, 2)), "two Granaries")
		self.assertEqual(types.format_objective((iParthenon, 2)), "two the Parthenons")
	
	def testFormatObjectiveKey(self):
		types = ArgumentProcessor([CvBuildingInfo, int])
		
		options = FormatOptions().objective("SOME")
		types.options = options
		
		self.assertEqual(types.format_objective((iGranary, 1)), "a Granary out of")
		self.assertEqual(types.format_objective((iGranary, 5)), "five Granaries out of")
	
	def testFormatObjectiveSingular(self):
		types = ArgumentProcessor([CvBuildingInfo, int])
		
		options = FormatOptions().singular()
		types.options = options
		
		self.assertEqual(types.format_objective((iGranary, 1)), "a Granary")
		self.assertEqual(types.format_objective((iGranary, 5)), "five Granary")
	
	def testFormatObjectiveAggregate(self):
		types = ArgumentProcessor([CvBuildingInfo, int])
		
		self.assertEqual(types.format_objective((sum(iGranary), 5)), "five Granaries")
		self.assertEqual(types.format_objective((sum(iGranary, iWalls, iMonument), 1)), "a total of a Granaries, Walls and Monuments")
		self.assertEqual(types.format_objective((sum(iGranary, iWalls, iMonument), 5)), "a total of five Granaries, Walls and Monuments")
	
	def testFormatObjectiveAggregateNamed(self):
		types = ArgumentProcessor([CvBuildingInfo, int])
		
		self.assertEqual(types.format_objective((sum(iOrthodoxTemple, iCatholicTemple, iProtestantTemple).named("TEMPLES"), 1)), "a temples")
		self.assertEqual(types.format_objective((sum(iOrthodoxTemple, iCatholicTemple, iProtestantTemple).named("TEMPLES"), 5)), "five temples")
	
	def testFormatObjectiveAggregateKey(self):
		types = ArgumentProcessor([CvBuildingInfo, int])
		
		options = FormatOptions().objective("SOME")
		types.options = options
		
		self.assertEqual(types.format_objective((sum(iGranary), 5)), "five Granaries out of")
		self.assertEqual(types.format_objective((sum(iGranary, iWalls, iMonument), 1)), "a total of a Granaries, Walls and Monuments out of")
		self.assertEqual(types.format_objective((sum(iGranary, iWalls, iMonument), 5)), "a total of five Granaries, Walls and Monuments out of")

	def testFormatObjectives(self):
		types = ArgumentProcessor([CvBuildingInfo, int])
		
		self.assertEqual(types.format_objectives([(iGranary, 2), (iWalls, 3), (iMonument, 4)]), "two Granaries, three Walls and four Monuments")
	
	def testFormatSubject(self):
		types = ArgumentProcessor(subject_type=CvBuildingInfo)
		
		self.assertEqual(types.format_subject(iGranary), "Granary")
	
	def testFormatArguments(self):
		types = ArgumentProcessor([CvBuildingInfo, int], subject_type=CvBuildingInfo)
		
		self.assertEqual(types.format("TXT_KEY_UHV_CITY_BUILDING", Arguments([(iGranary, 2)], iLibrary)), "build two Granaries in Library")
		self.assertEqual(types.format("TXT_KEY_UHV_CITY_BUILDING", Arguments([(iGranary, 2), (iWalls, 3), (iMonument, 4)], iLibrary)), "build two Granaries, three Walls and four Monuments in Library")

	def testFormatProgress(self):
		types = ArgumentProcessor([CvBuildingInfo, int])
		
		self.assertEqual(types.format_progress("", iGranary, 3), "Granary")
	
	def testFormatProgressNoArticle(self):
		types = ArgumentProcessor([CvBuildingInfo])
		
		self.assertEqual(types.format_progress("", iPyramids), "Pyramids")
	
	def testFormatProgressSubject(self):
		types = ArgumentProcessor([CvBuildingInfo, int], subject_type=CvUnitInfo)
		
		self.assertEqual(types.format_progress("", iSwordsman, iGranary, 3), "Granary")
	
	def testFormatProgressTextKey(self):
		types = ArgumentProcessor([CvReligionInfo])
		
		self.assertEqual(types.format_progress("TXT_KEY_UHV_PROGRESS_CONVERT_AFTER_FOUNDING", iJudaism), "Convert to Judaism")

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


class TestGoal(BaseGoal):

	types = ArgumentProcessor([])
	
	def __init__(self, *arguments):
		self._desc = "TXT_KEY_UHV_CONTROL"
		super(TestGoal, self).__init__(*arguments)
		
		self.condition_value = True
	
	def condition(self, *arguments):
		return self.condition_value
	
	def display(self):
		return str(self.condition())
		
		
class DescriptionGoal(BaseGoal):
	
	types = ArgumentProcessor([CvBuildingInfo, int])
	
	def __init__(self, *arguments):
		self._desc = "TXT_KEY_UHV_CONTROL"
		super(DescriptionGoal, self).__init__(*arguments)


class TestBaseGoal(ExtendedTestCase):

	def setUp(self):
		self.goal = TestGoal()
	
	def testIncludeOwner(self):
		def condition_value():
			return True
		TestGoal = Count.objective(int).include_owner.func(condition_value).subclass("TestGoal")
		iPlayer = 21
		
		goal = TestGoal(0, 1, 2).activate(iPlayer)
		
		self.assertEqual(goal.owner_included, True)
		self.assertEqual(goal.arguments.iPlayer, iPlayer)
		self.assertEqual(goal.arguments.owner_included, True)
	
	def testNotIncludeOwner(self):
		iPlayer = 20
		
		goal = TestGoal().activate(iPlayer)
		
		self.assertEqual(goal.owner_included, False)
		self.assertEqual(goal.arguments.owner_included, False)
	
	def testInitialState(self):
		self.assertEqual(self.goal.state, POSSIBLE)
		self.assertEqual(self.goal.iPlayer, None)
		self.assertEqual(self.goal.callback, None)
		self.assertEqual(self.goal.arguments.iPlayer, None)
	
	def testActivate(self):
		goal = self.goal.activate(0)
		
		self.assertEqual(self.goal.iPlayer, None)
		self.assertEqual(self.goal.callback, None)
		self.assertEqual(self.goal.arguments.iPlayer, None)
		
		self.assertEqual(goal.iPlayer, 0)
		self.assertEqual(goal._player.getID(), 0)
		self.assertEqual(goal._team.getID(), 0)
		self.assertEqual(goal.callback, None)
		self.assertEqual(goal.arguments.iPlayer, 0)
	
	def testActivateWithCallback(self):
		def callback():
			pass
		
		goal = self.goal.activate(0, callback)
		
		self.assertEqual(self.goal.callback, None)
		self.assertEqual(goal.callback, callback)
	
	def testPassivate(self):
		def callback():
			pass
		
		goal = self.goal.passivate(0, callback)
		
		try:
			self.assertEqual(self.goal.iPlayer, None)
			self.assertEqual(self.goal.callback, None)
		
			self.assertEqual(goal.iPlayer, 0)
			self.assertEqual(goal.callback, callback)
		finally:
			goal.deactivate()
	
	def testPossiblePossible(self):
		goal = self.goal.activate(0)
		self.assertEqual(goal.possible(), True)
	
	def testPossibleSucceeded(self):
		goal = self.goal.activate(0)
		goal.state = SUCCESS
		self.assertEqual(goal.possible(), False)
	
	def testPossibleFailed(self):
		goal = self.goal.activate(0)
		goal.state = FAILURE
		self.assertEqual(goal.possible(), False)
	
	def testSucceed(self):
		goal = self.goal.activate(0)
		self.assertEqual(goal.state, POSSIBLE)
		
		goal.succeed()
		self.assertEqual(goal.state, SUCCESS)
	
	def testFail(self):
		goal = self.goal.activate(0)
		self.assertEqual(goal.state, POSSIBLE)
		
		goal.fail()
		self.assertEqual(goal.state, FAILURE)
	
	def testSetStateUnchanged(self):
		goal = self.goal.activate(0)
		self.assertEqual(goal.state, POSSIBLE)
		
		goal.setState(POSSIBLE)
		self.assertEqual(goal.state, POSSIBLE)
	
	def testSetStateChanged(self):
		goal = self.goal.activate(0)
		self.assertEqual(goal.state, POSSIBLE)
		
		goal.setState(SUCCESS)
		self.assertEqual(goal.state, SUCCESS)
	
	def testSetStateChangedCallback(self):
		class Callable(object):
			def __init__(self):
				self.called = None
			def stateChange(self, goal):
				self.called = goal
				
		callable = Callable()
		
		goal = self.goal.activate(0, callable)
		goal.setState(SUCCESS)
		self.assertEqual(callable.called, goal)
	
	def testSetStateUnchangedCallback(self):
		class Callable(object):
			def __init__(self):
				self.called = None
			def call(self, called):
				self.called = called
				
		callable = Callable()
		
		goal = self.goal.activate(0, callable.call)
		goal.setState(POSSIBLE)
		self.assertEqual(callable.called, None)
	
	def testSetStateRecordSuccessTurn(self):
		goal = self.goal.activate(0)
		
		self.assertEqual(goal._iSuccessTurn, None)
		
		goal.setState(SUCCESS)
		
		self.assertEqual(goal.state, SUCCESS)
		self.assertEqual(goal._iSuccessTurn, 0)
	
	def testRecordSuccessTurn(self):
		goal = self.goal.activate(0)
		
		self.assertEqual(goal._iSuccessTurn, None)
		
		goal.recordSuccessTurn()
		
		self.assertEqual(goal._iSuccessTurn, 0)

	def testExpirePossible(self):
		goal = self.goal.activate(0)
		self.assertEqual(goal.state, POSSIBLE)
		
		goal.expire()
		self.assertEqual(goal.state, FAILURE)
	
	def testExpireSuccess(self):
		goal = self.goal.activate(0)
	
		goal.state = SUCCESS
		goal.expire()
		
		self.assertEqual(goal.state, SUCCESS)
	
	def testExpireFailure(self):
		goal = self.goal.activate(0)
	
		goal.state = FAILURE
		goal.expire()
		
		self.assertEqual(goal.state, FAILURE)
	
	def testNonzero(self):
		goal = self.goal.activate(0)
		self.assertEqual(bool(goal), True)
	
	def testNonzeroWithFailedCondition(self):
		goal = self.goal.activate(0)
		goal.condition_value = False
		
		self.assertEqual(bool(goal), False)
	
	def testToString(self):
		goal = self.goal.activate(0)
		self.assertEqual(str(goal), "True")
	
	def testCheckPossible(self):
		goal = self.goal.activate(0)
		self.assertEqual(goal.state, POSSIBLE)
		
		goal.check()
		self.assertEqual(goal.state, SUCCESS)
	
	def testCheckFailure(self):
		goal = self.goal.activate(0)
		goal.state = FAILURE
		
		goal.check()
		self.assertEqual(goal.state, FAILURE)
	
	def testCheckSuccess(self):
		goal = self.goal.activate(0)
		goal.state = SUCCESS
		
		goal.check()
		self.assertEqual(goal.state, SUCCESS)
		
	def testCheckFailingPossible(self):
		goal = self.goal.activate(0)
		goal.condition_value = False
		
		self.assertEqual(goal.state, POSSIBLE)
		
		goal.check()
		self.assertEqual(goal.state, POSSIBLE)
	
	def testCheckFailingFailure(self):
		goal = self.goal.activate(0)
		goal.condition_value = False
		goal.state = FAILURE
		
		goal.check()
		self.assertEqual(goal.state, FAILURE)
	
	def testCheckFailingSuccess(self):
		goal = self.goal.activate(0)
		goal.condition_value = False
		goal.state = SUCCESS
		
		goal.check()
		self.assertEqual(goal.state, SUCCESS)
	
	def testCheckCallback(self):
		class RecordingCallback(object):
			def __init__(self):
				self.recorded = None
			def check(self, goal):
				self.recorded = goal
		
		callback = RecordingCallback()
		goal = self.goal.activate(0, callback)
		self.assertEqual(callback.recorded, None)
		
		goal.check()
		self.assertEqual(callback.recorded, goal)
	
	def testCheckBeforeAt(self):
		goal = self.goal.at(1000).activate(0)
		goal.condition_value = True
		goal.state = POSSIBLE
		
		goal.check()
		self.assertEqual(goal.state, POSSIBLE)
		
	def testCheckDuringAt(self):
		goal = self.goal.at(-3000).activate(0)
		goal.condition_value = True
		goal.state = POSSIBLE
		
		goal.check()
		self.assertEqual(goal.state, SUCCESS)
	
	def testFinalCheckPossible(self):
		goal = self.goal.activate(0)
		self.assertEqual(goal.state, POSSIBLE)
		
		goal.finalCheck()
		self.assertEqual(goal.state, SUCCESS)
	
	def testFinalCheckFailure(self):
		goal = self.goal.activate(0)
		goal.state = FAILURE
		
		goal.finalCheck()
		self.assertEqual(goal.state, FAILURE)
	
	def testFinalCheckSuccess(self):
		goal = self.goal.activate(0)
		goal.state = SUCCESS
		
		goal.finalCheck()
		self.assertEqual(goal.state, SUCCESS)
	
	def testFinalCheckFailingPossible(self):
		goal = self.goal.activate(0)
		goal.condition_value = False
		
		self.assertEqual(goal.state, POSSIBLE)
		
		goal.finalCheck()
		self.assertEqual(goal.state, FAILURE)
	
	def testFinalCheckFailingFailure(self):
		goal = self.goal.activate(0)
		goal.condition_value = False
		goal.state = FAILURE
		
		goal.finalCheck()
		self.assertEqual(goal.state, FAILURE)
	
	def testFinalCheckFailingSuccess(self):
		goal = self.goal.activate(0)
		goal.condition_value = False
		goal.state = SUCCESS
		
		goal.finalCheck()
		self.assertEqual(goal.state, SUCCESS)
	
	def testAtSuccess(self):
		self.goal.at(-3000)
		self.goal.condition_value = True
		goal = self.goal.activate(0)
		
		self.assertEqual(goal.state, POSSIBLE)
		
		events.fireEvent("BeginPlayerTurn", 0, 0)
		self.assertEqual(goal.state, SUCCESS)
		
		goal.deactivate()
	
	def testAtFailure(self):
		self.goal.at(-3000)
		self.goal.condition_value = False
		goal = self.goal.activate(0)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
		
			events.fireEvent("BeginPlayerTurn", 0, 0)
			self.assertEqual(goal.state, FAILURE)
		finally:
			goal.deactivate()
	
	def testAtDifferentTurn(self):
		self.goal.at(-3000)
		self.goal.condition_value = True
		goal = self.goal.activate(0)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
		
			events.fireEvent("BeginPlayerTurn", 1, 0)
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			goal.deactivate()
	
	def testBy(self):
		self.goal.by(-3000)
		goal = self.goal.activate(0)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
		
			events.fireEvent("BeginPlayerTurn", 0, 0)
			self.assertEqual(goal.state, FAILURE)
		finally:
			goal.deactivate()
		
	def testByAfterSuccess(self):
		self.goal.by(-3000)
		self.goal.state = SUCCESS
		goal = self.goal.activate(0)
		
		try:
			self.assertEqual(goal.state, SUCCESS)
		
			events.fireEvent("BeginPlayerTurn", 0, 0)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			goal.deactivate()
	
	def testByDifferentTurn(self):
		self.goal.by(-3000)
		goal = self.goal.activate(0)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
		
			events.fireEvent("BeginPlayerTurn", 1, 0)
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			goal.deactivate()
		
	def testChecked(self):
		goal = TestGoal.checked("cityBuilt").subclass("SubGoal")()
		goal.condition_value = True
		goal = goal.activate(0)
		
		city = player(0).initCity(61, 31)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			
			events.fireEvent("cityBuilt", city)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			city.kill()
			
			goal.deactivate()
	
	def testTurnly(self):
		goal = TestGoal.turnly.subclass("SubGoal")()
		goal.condition_value = True
		goal = goal.activate(0)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
		
			events.fireEvent("BeginPlayerTurn", 0, 0)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			goal.deactivate()
	
	def testDeactivateDisablesEventHandling(self):
		self.goal.at(-3000)
		goal = self.goal.activate(0)
		
		goal.deactivate()
		
		events.fireEvent("BeginPlayerTurn", 0, 0)
		
		self.assertEqual(goal.state, POSSIBLE)
	
	def testDeactivateTwice(self):
		self.goal.at(-3000)
		goal = self.goal.activate(0)
		
		goal.deactivate()
		goal.deactivate()
	
	def testCheckEvery(self):
		self.goal.every()
		goal = self.goal.activate(0)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
		
			events.fireEvent("BeginPlayerTurn", 0, 0)
		
			self.assertEqual(goal.state, SUCCESS)
		finally:
			goal.deactivate()
	
	def testPassiveCannotSucceed(self):
		goal = self.goal.passivate(0)
		goal.succeed()
		
		self.assertEqual(goal.state, POSSIBLE)
	
	def testPassiveCanFail(self):
		goal = self.goal.passivate(0)
		goal.fail()
		
		self.assertEqual(goal.state, FAILURE)
	
	def testDescription(self):
		self.assertEqual(self.goal.description(), "Control ")
	
	def testDescriptionArguments(self):
		goal = DescriptionGoal(iGranary, 3)
		self.assertEqual(goal.description(), "Control three Granaries")
	
	def testDescriptionNamed(self):
		goal = TestGoal().named("SETTLE")
		self.assertEqual(goal.description(), "Settle ")
	
	def testDescriptionArgumentsNamed(self):
		goal = DescriptionGoal(iGranary, 3).named("SETTLE")
		self.assertEqual(goal.description(), "Settle three Granaries")
	
	def testDescriptionByAD(self):
		goal = DescriptionGoal(iGranary, 3).by(1000).activate(0)
		self.assertEqual(goal.description(), "Control three Granaries by 1000 AD (Turn 221)")
	
	def testDescriptionByBC(self):
		goal = DescriptionGoal(iGranary, 3).by(-1000).activate(0)
		self.assertEqual(goal.description(), "Control three Granaries by 1000 BC (Turn 74)")
	
	def testDescriptionAtAD(self):
		goal = DescriptionGoal(iGranary, 3).at(1000).activate(0)
		self.assertEqual(goal.description(), "Control three Granaries in 1000 AD (Turn 221)")
	
	def testDescriptionAtBC(self):
		goal = DescriptionGoal(iGranary, 3).at(-1000).activate(0)
		self.assertEqual(goal.description(), "Control three Granaries in 1000 BC (Turn 74)")
	
	def testDescriptionUnactivated(self):
		goal = DescriptionGoal(iGranary, 3).at(1000)
		self.assertEqual(goal.description(), "Control three Granaries in 1000 AD")
	
	def testDescriptionCalendar(self):
		goal = DescriptionGoal(iGranary, 3).at(1000).activate(0)
		
		team(0).setHasTech(iCalendar, True, 0, True, False)
		
		option_value = AdvisorOpt.getUHVFinishDate()
		AdvisorOpt.setUHVFinishDate(0)
		
		try:
			self.assertEqual(goal.description(), "Control three Granaries in 1000 AD")
		finally:
			team(0).setHasTech(iCalendar, False, 0, True, False)
			AdvisorOpt.setUHVFinishDate(option_value)
	
	def testDescriptionCalendarEnabled(self):
		goal = DescriptionGoal(iGranary, 3).at(1000).activate(0)
		
		team(0).setHasTech(iCalendar, True, 0, True, False)
		
		option_value = AdvisorOpt.getUHVFinishDate()
		AdvisorOpt.setUHVFinishDate(1)
		
		try:
			self.assertEqual(goal.description(), "Control three Granaries in 1000 AD (Turn 221)")
		finally:
			team(0).setHasTech(iCalendar, False, 0, True, False)
			AdvisorOpt.setUHVFinishDate(option_value)
	
	def testTitle(self):
		goal = TestGoal()
		goal.titled("VIK3")
		
		self.assertEqual(goal.title(), "Danegeld")
	
	def testTitleNonexistent(self):
		goal = TestGoal()
		goal.titled("XYZ4")
		
		self.assertEqual(goal.title(), "")
		
	def testTitleUntitled(self):
		goal = TestGoal()
		
		self.assertEqual(goal.title(), "")
	
	def testFullDescriptionWithTitle(self):
		goal = DescriptionGoal(iGranary, 3).titled("VIK3")
		
		self.assertEqual(goal.full_description(), "Danegeld: Control three Granaries")
	
	def testFullDescriptionWithoutTitle(self):
		goal = DescriptionGoal(iGranary, 3)
		
		self.assertEqual(goal.full_description(), "Control three Granaries")
	
	def testStateStringFailure(self):
		goal = self.goal.activate(0)
		goal.setState(FAILURE)
		
		self.assertEqual(goal.state_string(), "NO")
	
	def testStateStringSuccess(self):
		goal = self.goal.activate(0)
		goal.setState(SUCCESS)
		
		self.assertEqual(goal.state_string(), "YES")
	
	def testStateStringPossible(self):
		goal = self.goal.activate(0)
		goal.setState(POSSIBLE)
		
		self.assertEqual(goal.state_string(), "Not yet")
	
	def testStateStringPassiveFailure(self):
		goal = self.goal.passivate(0)
		goal.setState(FAILURE)
		
		self.assertEqual(goal.state_string(), "NO")
	
	def testStateStringPassiveFulfilled(self):
		goal = self.goal.passivate(0)
		goal.condition_value = True
		
		self.assertEqual(goal.state_string(), "YES")
	
	def testStateStringPassiveUnfulfilled(self):
		goal = self.goal.passivate(0)
		goal.condition_value = False
		
		self.assertEqual(goal.state_string(), "Not yet")
	
	def testAccomplishedStringNoTurn(self):
		goal = self.goal.activate(0)
		
		self.assertEqual(goal.accomplished_string(), u"%c Goal accomplished!" % self.SUCCESS_CHAR)
	
	def testAccomplishedStringNone(self):
		goal = self.goal.activate(0)
		goal._iSuccessTurn = 0
		
		option_value = AdvisorOpt.getUHVFinishDate()
		AdvisorOpt.setUHVFinishDate(0)
		
		try:
			self.assertEqual(goal.accomplished_string(), u"%c Goal accomplished!" % self.SUCCESS_CHAR)
		finally:
			AdvisorOpt.setUHVFinishDate(option_value)
	
	def testAccomplishedStringYear(self):
		goal = self.goal.activate(0)
		goal._iSuccessTurn = 0
		
		option_value = AdvisorOpt.getUHVFinishDate()
		AdvisorOpt.setUHVFinishDate(1)
		
		try:
			self.assertEqual(goal.accomplished_string(), u"%c Goal accomplished! (3000 BC)" % self.SUCCESS_CHAR)
		finally:
			AdvisorOpt.setUHVFinishDate(option_value)
	
	def testAccomplishedStringTurn(self):
		goal = self.goal.activate(0)
		goal._iSuccessTurn = 0
		
		option_value = AdvisorOpt.getUHVFinishDate()
		AdvisorOpt.setUHVFinishDate(2)
		
		try:
			self.assertEqual(goal.accomplished_string(), u"%c Goal accomplished! (3000 BC - Turn 0)" % self.SUCCESS_CHAR)
		finally:
			AdvisorOpt.setUHVFinishDate(option_value)
	
	def testProgressFailed(self):
		goal = self.goal.activate(0)
		goal.fail()
		
		self.assertEqual(goal.progress(), [[u"%c Goal failed!" % self.FAILURE_CHAR]])
	
	def testProgressSucceeded(self):
		goal = self.goal.activate(0)
		goal.succeed()
		
		option_value = AdvisorOpt.getUHVFinishDate()
		AdvisorOpt.setUHVFinishDate(1)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Goal accomplished! (3000 BC)" % self.SUCCESS_CHAR]])
		finally:
			AdvisorOpt.setUHVFinishDate(option_value)
	
	def testProgressChunks(self):
		chunk_size_per_length = {
			1: 3,
			2: 3,
			3: 3,
			4: 4,
			5: 3,
			6: 3,
			7: 4,
			8: 4,
			9: 3,
			10: 4,
			11: 4,
			12: 4,
		}
		
		for length, chunk_size in chunk_size_per_length.items():
			self.assertEqual(self.goal.progress_chunks(list(range(length))), chunk_size)


class TestProgress(ExtendedTestCase):
	
	def testProgressText(self):
		goal = Condition.wonder(iPyramids).activate(0)
		
		self.assertEqual(goal.progress_text(iPyramids), "Pyramids")
	
	def testProgressTextCount(self):
		goal = Count.building(iGranary, 3).activate(0)
		
		try:
			self.assertEqual(goal.progress_text(iGranary, 3), "Granaries: 0 / 3")
		finally:
			goal.deactivate()
	
	def testProgressIndicatorIncomplete(self):
		goal = Count.building(iGranary, 3).activate(0)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress_indicator(iGranary, 3), u"%c" % self.FAILURE_CHAR)
		finally:
			goal.deactivate()
	
	def testProgressIndicatorComplete(self):
		goal = Count.building(iGranary, 1).activate(0)
		
		try:
			city = player(0).initCity(61, 31)
			city.setHasRealBuilding(iGranary, True)
		
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.progress_indicator(iGranary, 1), u"%c" % self.SUCCESS_CHAR)
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testObjectiveProgress(self):
		goal = Condition.wonder(iPyramids).activate(0)
		
		try:
			self.assertEqual(goal.objective_progress(iPyramids), u"%c Pyramids" % self.FAILURE_CHAR)
		finally:
			goal.deactivate()
	
	def testObjectiveProgressCount(self):
		goal = Count.building(iGranary, 3).activate(0)
		
		try:
			self.assertEqual(goal.objective_progress(iGranary, 3), u"%c Granaries: 0 / 3" % self.FAILURE_CHAR)
		finally:
			goal.deactivate()
	
	def testProgress(self):
		goal = Condition.wonder(iPyramids).activate(0)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Pyramids" % self.FAILURE_CHAR]])
		finally:
			goal.deactivate()
	
	def testProgressMultiple(self):
		goal = Condition.wonder(iPyramids, iOracle, iParthenon).activate(0)
		
		try:
			self.assertEqual(goal.progress(), [[
				u"%c Pyramids" % self.FAILURE_CHAR, 
				u"%c Oracle" % self.FAILURE_CHAR, 
				u"%c Parthenon" % self.FAILURE_CHAR
			]])
		finally:
			goal.deactivate()
	
	def testProgressBy(self):
		goal = Condition.wonder(iPyramids).by(100).activate(0)
		
		try:
			self.assertEqual(goal.progress(), [])
		finally:
			goal.deactivate()
	
	def testProgressByMultiple(self):
		goal = Condition.wonder(iPyramids, iOracle, iParthenon).by(100).activate(0)
		
		try:
			self.assertEqual(goal.progress(), [[
				u"%c Pyramids" % self.FAILURE_CHAR, 
				u"%c Oracle" % self.FAILURE_CHAR, 
				u"%c Parthenon" % self.FAILURE_CHAR
			]])
		finally:
			goal.deactivate()
	
	def testProgressByForceSingle(self):
		goal = Condition.wonder(iPyramids).by(100).activate(0)
		
		try:
			self.assertEqual(goal.progress(bForceSingle=True), [[u"%c Pyramids" % self.FAILURE_CHAR]])
		finally:
			goal.deactivate()
		
	def testProgressCountSingle(self):
		goal = Count.building(iGranary, 1).activate(0)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Granary" % self.FAILURE_CHAR]])
		finally:
			goal.deactivate()
	
	def testProgressCountMultiple(self):
		goal = Count.building(iGranary, 3).activate(0)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Granaries: 0 / 3" % self.FAILURE_CHAR]])
		finally:
			goal.deactivate()
	
	def testProgressCountTextKey(self):
		goal = Count.building(iGranary, 3)
		goal._progress = "TXT_KEY_UHV_PROGRESS_CONVERT_AFTER_FOUNDING"
		goal = goal.activate(0)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Convert to Granary: 0 / 3" % self.FAILURE_CHAR]])
		finally:
			goal.deactivate()
	
	def testProgressCountAggregate(self):
		goal = Count.building(sum(iGranary, iBarracks), 3).activate(0)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Granaries and Barracks: 0 / 3" % self.FAILURE_CHAR]])
		finally:
			goal.deactivate()
	
	def testProgressCountPlots(self):
		goal = Count.numCities(plots.region(rBritain).named("BRITAIN"), 3).activate(0)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Cities in Britain: 0 / 3" % self.FAILURE_CHAR]])
		finally:
			goal.deactivate()
	
	def testProgressWithCitiesNoCities(self):
		goal = Count.populationCities(10, 3).activate(0)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c No Cities" % self.FAILURE_CHAR]])
		finally:
			goal.deactivate()
	
	def testProgressWithCitiesNotEnoughCities(self):
		goal = Count.populationCities(10, 3).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setPopulation(10)
		city.setName("First", False)
		
		try:
			self.assertEqual(goal.progress(), [[
				u"%c First: 10 / 10" % self.SUCCESS_CHAR, 
				u"%c No second city" % self.FAILURE_CHAR, 
				u"%c No third city" % self.FAILURE_CHAR
			]])
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testProgressWithCities(self):
		goal = Count.populationCities(10, 3).activate(0)
		
		city1, city2, city3 = (player(0).initCity(*tuple) for tuple in [(61, 31), (63, 31), (65, 31)])
		
		city1.setPopulation(10)
		city1.setName("First", False)
		
		city2.setPopulation(3)
		city2.setName("Second", False)
		
		city3.setPopulation(5)
		city3.setName("Third", False)
		
		try:
			self.assertEqual(goal.progress(), [[
				u"%c First: 10 / 10" % self.SUCCESS_CHAR, 
				u"%c Third: 5 / 10" % self.FAILURE_CHAR, 
				u"%c Second: 3 / 10" % self.FAILURE_CHAR
			]])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
		
			goal.deactivate()
	
	def testProgressPercentage(self):
		goal = Percentage.religionSpread(iIslam, 20).activate(0)
		
		self.assertEqual(goal.progress(), [[u"%c Islam spread to: 0.00%% / 20%%" % self.FAILURE_CHAR]])
	
	def testProgressBestCity(self):
		goal = BestCity.population(capital()).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setPopulation(5)
		
		city2 = player(1).initCity(63, 31)
		city2.setName("Second", False)
		city2.setPopulation(10)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [
				[u"%c Most populous: Second (10)" % self.FAILURE_CHAR],
				["Our next most populous: First (5)"]
			])
		finally:
			city1.kill()
			city2.kill()
	
	def testProgressBestPlayer(self):
		goal = BestPlayer.population().activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setPopulation(5)
		
		city2 = player(1).initCity(63, 31)
		city2.setPopulation(10)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [
				[u"%c Most populous: Babylonia (1000000)" % self.FAILURE_CHAR],
				["Our next most populous: Egypt (125000)"]
			])
		finally:
			city1.kill()
			city2.kill()
	
	def testProgressRouteConnection(self):
		goal = RouteConnection(capital(), plots.region(rBritain).named("BRITAIN"), [iRouteRailroad]).activate(0)
		
		self.assertEqual(goal.iPlayer, 0)
		self.assertEqual(goal.progress(), [[u"%c Railroad from your capital to Britain" % self.FAILURE_CHAR]])
	
	def testProgressRouteConnectionMultipleRoutes(self):
		goal = RouteConnection(capital(), plots.region(rBritain).named("BRITAIN"), [iRouteRoad, iRouteRailroad, iRouteHighway]).activate(0)
		
		self.assertEqual(goal.progress(), [[u"%c Road, Railroad or Highway from your capital to Britain" % self.FAILURE_CHAR]])
	
	def testProgressAll(self):
		goal1 = Condition.wonder(iPyramids)
		goal2 = Condition.wonder(iParthenon)
		goal = All(goal1, goal2).activate(0)
		
		try:
			self.assertEqual(goal.progress(), [
				[u"%c Pyramids" % self.FAILURE_CHAR],
				[u"%c Parthenon" % self.FAILURE_CHAR]
			])
		finally:
			goal.deactivate()
	
	def testProgressAllFailable(self):
		goal1 = Condition.wonder(iPyramids)
		goal2 = Trigger.noCityLost()
		goal = All(goal1, goal2).activate(0)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Pyramids" % self.FAILURE_CHAR]])
		finally:
			goal.deactivate()
	
	def testProgressAllIndicatorCurrent(self):
		goal1 = Condition.wonder(iPyramids)
		goal2 = Condition.wonder(iParthenon)
		goal = All(goal1, goal2).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPyramids, True)
		
		try:
			self.assertEqual(goal.progress(), [
				[u"%c Pyramids" % self.SUCCESS_CHAR],
				[u"%c Parthenon" % self.FAILURE_CHAR]
			])
		finally:
			city.kill()
			goal.deactivate()
	
	def testProgressAllIndicatorComplete(self):
		goal1 = Condition.wonder(iPyramids)
		goal2 = Condition.wonder(iParthenon)
		goal = All(goal1, goal2).activate(0)
		
		goal1 = goal.goals[0]
		goal1.succeed()
		
		option_value = AdvisorOpt.getUHVFinishDate()
		AdvisorOpt.setUHVFinishDate(1)
		
		try:
			self.assertEqual(goal1.state, SUCCESS)
			self.assertEqual(goal1.succeeded(), True)
			self.assertEqual(goal.progress(), [
				[u"%c Goal accomplished! (3000 BC)" % self.SUCCESS_CHAR],
				[u"%c Parthenon" % self.FAILURE_CHAR]
			])
		finally:
			goal.deactivate()
			AdvisorOpt.setUHVFinishDate(option_value)

	def testProgressAllFromDescription(self):
		goal1 = Condition.tradeConnection().named("TRADE_CONNECTION")
		goal = All(goal1).activate(0)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Establish a trade connection with another civilization" % self.FAILURE_CHAR]])
		finally:
			goal.deactivate()
	
	def testProgressSome(self):
		subgoal = Condition.wonder(iPyramids, iParthenon, iOracle)
		goal = Some(subgoal, 2).activate(0)
		
		try:
			self.assertEqual(goal.progress(), [[
				u"%c Pyramids" % self.FAILURE_CHAR,
				u"%c Parthenon" % self.FAILURE_CHAR, 
				u"%c Oracle" % self.FAILURE_CHAR
			]])
		finally:
			goal.deactivate()
	
	def testFullDisplay(self):
		goal = Condition.wonder(iPyramids).activate(0)
		
		try:
			self.assertEqual(goal.full_display(), u"Build the Pyramids\n%c Pyramids" % self.FAILURE_CHAR)
		finally:
			goal.deactivate()


class TestAreas(ExtendedTestCase):

	def testNone(self):
		goal = Condition.wonder(iPyramids).activate(0)
		
		try:
			self.assertEqual(goal.areas, dict())
			self.assertEqual(goal.area_name((1, 1)), "")
		finally:
			goal.deactivate()
	
	def testObjective(self):
		britain = plots.region(rBritain).named("BRITAIN")
		goal = Condition.control(britain).activate(0)
		
		britain = britain.create()
		expectedAreas = {
			"Britain": britain
		}
		
		try:
			self.assertEqual(goal.areas, expectedAreas)
			self.assertEqual(goal.area_name((1, 1)), "")
			self.assertEqual(goal.area_name(britain.random()), "Britain")
		finally:
			goal.deactivate()
	
	def testObjectiveMultiple(self):
		britain = plots.region(rBritain).named("BRITAIN")
		iberia = plots.region(rEgypt).named("IBERIA")
		italy = plots.region(rItaly).named("ITALY")
		goal = Condition.control(britain, iberia, italy).activate(0)
		
		britain = britain.create()
		iberia = iberia.create()
		italy = italy.create()
		
		expectedAreas = {
			"Britain": britain,
			"Iberia": iberia,
			"Italy": italy
		}
		
		try:
			self.assertEqual(goal.areas, expectedAreas)
			self.assertEqual(goal.area_name((1, 1)), "")
			self.assertEqual(goal.area_name(britain.random()), "Britain")
			self.assertEqual(goal.area_name(iberia.random()), "Iberia")
			self.assertEqual(goal.area_name(italy.random()), "Italy")
		finally:
			goal.deactivate()
	
	def testObjectiveAggregate(self):
		britain = plots.region(rBritain)
		italy = plots.region(rItaly)
		goal = Count.numCities(sum(britain, italy).named("NAME_BABYLON"), 2).activate(0)
		
		britain = britain.create()
		italy = italy.create()
		
		expectedAreas = {
			"Babylon": britain + italy,
		}
		
		try:
			self.assertEqual(goal.areas, expectedAreas)
			self.assertEqual(goal.area_name((1, 1)), "")
			self.assertEqual(goal.area_name(britain.random()), "Babylon")
			self.assertEqual(goal.area_name(italy.random()), "Babylon")
		finally:
			goal.deactivate()
	
	def testSubject(self):
		andeanCoast = plots.region(rPeru).named("ANDEAN_COAST")
		goal = Condition.route(andeanCoast, iRouteRoad).activate(0)
		
		andeanCoast = andeanCoast.create()
		expectedAreas = {
			"Andean Coast": andeanCoast
		}
		
		try:
			self.assertEqual(goal.areas, expectedAreas)
			self.assertEqual(goal.area_name((1, 1)), "")
			self.assertEqual(goal.area_name(andeanCoast.random()), "Andean Coast")
		finally:
			goal.deactivate()
	
	def testOverlapping(self):
		britain = plots.rectangle((0, 0), (4, 4)).named("BRITAIN")
		italy = plots.rectangle((2, 2), (6, 6)).named("ITALY")
		goal = Condition.control(britain, italy).activate(0)
		
		britain = britain.create()
		italy = italy.create()
		expectedAreas = {
			"Britain": britain,
			"Italy": italy
		}
		
		try:
			self.assertEqual(goal.areas, expectedAreas)
			self.assertEqual(goal.area_name((50, 50)), "")
			self.assertEqual(goal.area_name((3, 3)), "Britain\nItaly")
			self.assertEqual(goal.area_name((0, 0)), "Britain")
			self.assertEqual(goal.area_name((6, 6)), "Italy")
		finally:
			goal.deactivate()
	
	def testDeferredCity(self):
		deferred = city(10, 10).named("BABYLON")
		goal = Count.citySpecialist(deferred, iSpecialistGreatArtist, 1).activate(0)
		
		expectedAreas = {
			"Babylon": plots_.of([(10, 10)])
		}
		
		try:
			self.assertEqual(goal.areas, expectedAreas)
			self.assertEqual(goal.area_name((10, 10)), "Babylon")
		finally:
			goal.deactivate()
	
	def testDeferredCapital(self):
		deferred = capital()
		goal = Count.citySpecialist(deferred, iSpecialistGreatArtist, 1).activate(0)
		
		try:
			self.assertEqual(goal.areas, {})
		finally:
			goal.deactivate()
	
	def testRouteConnection(self):
		start = plots.capitals(iRussia).named("MOSCOW")
		target = plots.of([(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]).named("SIBERIAN_COAST")
		goal = RouteConnection(start, target, [iRouteRoad]).activate(0)
		
		start = start.create()
		target = target.create()
		
		expectedAreas = {
			"Moscow": start,
			"Siberian coast": target,
		}
		
		try:
			self.assertEqual(goal.areas, expectedAreas)
			self.assertEqual(goal.area_name(start.random()), "Moscow")
			self.assertEqual(goal.area_name((0, 0)), "Siberian coast")
		finally:
			goal.deactivate()
	
	def testAll(self):
		britain = plots.region(rBritain).named("BRITAIN")
		iberia = plots.region(rIberia).named("IBERIA")
		italy = plots.region(rItaly).named("ITALY")
		goal = All(Condition.control(britain), Condition.control(iberia), Condition.control(italy)).activate(0)
		
		britain = britain.create()
		iberia = iberia.create()
		italy = italy.create()
		
		expectedAreas = {
			"Britain": britain,
			"Iberia": iberia,
			"Italy": italy,
		}
		
		try:
			self.assertEqual(goal.areas, expectedAreas)
			self.assertEqual(goal.area_name(britain.random()), "Britain")
			self.assertEqual(goal.area_name(iberia.random()), "Iberia")
			self.assertEqual(goal.area_name(italy.random()), "Italy")
		finally:
			goal.deactivate()
	
	def testSome(self):
		britain = plots.region(rBritain).named("BRITAIN")
		iberia = plots.region(rIberia).named("IBERIA")
		goal = Some(Condition.control(britain, iberia), 2).activate(0)
		
		britain = britain.create()
		iberia = iberia.create()
		
		expectedAreas = {
			"Britain": britain,
			"Iberia": iberia
		}
		
		try:
			self.assertEqual(goal.areas, expectedAreas)
			self.assertEqual(goal.area_name(britain.random()), "Britain")
			self.assertEqual(goal.area_name(iberia.random()), "Iberia")
		finally:
			goal.deactivate()
	
	def testDifferent(self):
		goal = Different(
			Count.cultureLevel(city(10, 10).named("BABYLON"), iCultureLevelDeveloping), 
			Count.cultureLevel(city(20, 20).named("CARTHAGE"), iCultureLevelInfluential)
		).activate(0)
		
		expectedAreas = {
			"Babylon": plots_.of([(10, 10)]),
			"Carthage": plots_.of([(20, 20)]),
		}
		
		try:
			self.assertEqual(goal.areas, expectedAreas)
			self.assertEqual(goal.area_name((10, 10)), "Babylon")
			self.assertEqual(goal.area_name((20, 20)), "Carthage")
		finally:
			goal.deactivate()
	
	def testConqueredCitiesInside(self):
		britain = plots.region(rBritain).named("BRITAIN")
		goal = Count.conqueredCities().inside(britain).activate(0)
		
		britain = britain.create()
		expectedAreas = {
			"Britain": britain,
		}
		
		try:
			self.assertEqual(goal.areas, expectedAreas)
			self.assertEqual(goal.area_name(britain.random()), "Britain")
			self.assertEqual(goal.area_name(plots_.region(rItaly).random()), "")
		finally:
			goal.deactivate()
	
	def testConqueredCitiesInsideUnnamed(self):
		britain = plots.region(rBritain)
		goal = Count.conqueredCities().inside(britain).activate(0)
		
		try:
			self.assertEqual(goal.areas, {})
		finally:
			goal.deactivate()
	
	def testConqueredCitiesOutside(self):
		britain = plots.region(rBritain).named("BRITAIN")
		goal = Count.conqueredCities().outside(britain).activate(0)
		
		britain = britain.create()
		expectedAreas = {
			"Britain": plots_.all().without(britain).land()
		}
		
		try:
			self.assertEqual(goal.areas, expectedAreas)
			self.assertEqual(goal.area_name(britain.random()), "")
			self.assertEqual(goal.area_name(plots_.region(rItaly).random()), "Britain")
		finally:
			goal.deactivate()
	
	def testConqueredCitiesOutsideUnnamed(self):
		britain = plots.region(rBritain)
		goal = Count.conqueredCities().outside(britain).activate(0)
		
		try:
			self.assertEqual(goal.areas, {})
		finally:
			goal.deactivate()
	

class TestConditionGoals(ExtendedTestCase):

	def testControlAllCities(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		city3 = player(0).initCity(65, 31)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
	
	def testControlSomeCities(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		city3 = player(1).initCity(65, 31)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
	
	def testControlNoCities(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city1 = player(1).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		city3 = player(1).initCity(65, 31)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
	
	def testControlEmpty(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testControlOutside(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city = player(0).initCity(59, 31)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city.kill()
	
	def testControlAllOfMultiple(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35)), plots.rectangle((66, 30), (70, 35))).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(69, 31)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city1.kill()
			city2.kill()
	
	def testControlSomeOfMultiple(self):
		goal = Condition.control(plots.rectangle((60, 30), (65, 35)), plots.rectangle((66, 30), (70, 35))).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(1).initCity(69, 31)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city1.kill()
			city2.kill()

	def testControlOrVassalizeAllCities(self):
		goal = Condition.controlOrVassalize(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		city3 = player(0).initCity(65, 31)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
	
	def testControlOrVassalizeSomeCities(self):
		goal = Condition.controlOrVassalize(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		city3 = player(1).initCity(65, 31)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
	
	def testControlOrVassalizeNoCities(self):
		goal = Condition.controlOrVassalize(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city1 = player(1).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		city3 = player(1).initCity(65, 31)
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
	
	def testControlOrVassalizeAllVassal(self):
		goal = Condition.controlOrVassalize(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city1 = player(1).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		city3 = player(1).initCity(65, 31)
		
		team(1).setVassal(team(0).getID(), True, False)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
		
			team(1).setVassal(team(0).getID(), False, False)
	
	def testControlOrVassalizeOneVassal(self):
		goal = Condition.controlOrVassalize(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city1 = player(1).initCity(61, 31)
		city2 = player(2).initCity(63, 31)
		city3 = player(2).initCity(65, 31)
		
		team(1).setVassal(team(0).getID(), True, False)
		
		try:
			self.assertEqual(bool(goal), False)
		
			city1.kill()
			city2.kill()
			city3.kill()
		finally:
			team(1).setVassal(team(0).getID(), False, False)
	
	def testSettleWhenFounded(self):
		goal = Condition.settle(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city = player(0).initCity(61, 31)
		events.fireEvent("cityBuilt", city)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testSettleWhenConquered(self):
		goal = Condition.settle(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city = player(1).initCity(61, 31)
		events.fireEvent("cityBuilt", city)
		
		player(0).acquireCity(city, True, False)
		city = city_(61, 31)
		
		try:
			self.assertEqual(city.getOwner(), 0)
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testSettleWhenTraded(self):
		goal = Condition.settle(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city = player(1).initCity(61, 31)
		events.fireEvent("cityBuilt", city)
		
		player(0).acquireCity(city, False, True)
		city = city_(61, 31)
		
		try:
			self.assertEqual(city.getOwner(), 0)
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testWonderOwned(self):
		goal = Condition.wonder(iPyramids).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPyramids, True)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testWonderNonExistent(self):
		goal = Condition.wonder(iPyramids).activate(0)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			goal.deactivate()
		
	def testWonderDifferentOwner(self):
		goal = Condition.wonder(iPyramids).activate(0)
		
		city = player(1).initCity(61, 31)
		city.setHasRealBuilding(iPyramids, True)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testMultipleWondersNone(self):
		goal = Condition.wonder(iPyramids, iParthenon, iColossus).activate(0)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			goal.deactivate()
	
	def testMultipleWondersSome(self):
		goal = Condition.wonder(iPyramids, iParthenon, iColossus).activate(0)
		
		city = player(0).initCity(61, 31)
		for iWonder in [iPyramids, iParthenon]:
			city.setHasRealBuilding(iWonder, True)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testMultipleWondersAll(self):
		goal = Condition.wonder(iPyramids, iParthenon, iColossus).activate(0)
		
		city = player(0).initCity(61, 31)
		for iWonder in [iPyramids, iParthenon, iColossus]:
			city.setHasRealBuilding(iWonder, True)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testWonderExpired(self):
		goal = Condition.wonder(iPyramids).activate(0)
		
		city = player(1).initCity(61, 31)
		city.setHasRealBuilding(iPyramids, True)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
		
			events.fireEvent("buildingBuilt", city, iPyramids)
		
			self.assertEqual(goal.state, FAILURE)
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testWonderCheck(self):
		goal = Condition.wonder(iPyramids).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPyramids, True)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
		
			events.fireEvent("buildingBuilt", city, iPyramids)
		
			self.assertEqual(goal.state, SUCCESS)
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testProjectNonExistent(self):
		goal = Condition.project(iTheInternet).activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testProjectCompleted(self):
		goal = Condition.project(iTheInternet).activate(0)
		
		team(0).changeProjectCount(iTheInternet, 1)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			team(0).changeProjectCount(iTheInternet, -1)
	
	def testProjectCompletedOther(self):
		goal = Condition.project(iTheInternet).activate(0)
		
		team(1).changeProjectCount(iTheInternet, 1)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			team(1).changeProjectCount(iTheInternet, -1)
	
	def testProjectCompletedMultipleSome(self):
		goal = Condition.project(iTheInternet, iHumanGenome, iSDI).activate(0)
		
		team(0).changeProjectCount(iTheInternet, 1)
		team(0).changeProjectCount(iHumanGenome, 1)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			team(0).changeProjectCount(iTheInternet, -1)
			team(0).changeProjectCount(iHumanGenome, -1)
	
	def testProjectCompletedMultipleAll(self):
		goal = Condition.project(iTheInternet, iHumanGenome, iSDI).activate(0)
		
		for iProject in [iTheInternet, iHumanGenome, iSDI]:
			team(0).changeProjectCount(iProject, 1)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			for iProject in [iTheInternet, iHumanGenome, iSDI]:
				team(0).changeProjectCount(iProject, -1)
	
	def testProjectCheckedOnEvent(self):
		goal = Condition.project(iTheInternet).activate(0)
		
		city = player(0).initCity(61, 31)
		team(0).changeProjectCount(iTheInternet, 1)
		
		events.fireEvent("projectBuilt", city, iTheInternet)
		
		try:
			self.assertEqual(goal.state, SUCCESS)
		finally:
			city.kill()
			team(0).changeProjectCount(iTheInternet, -1)
	
	def testProjectExpiredOnEvent(self):
		goal = Condition.project(iTheInternet).activate(0)
		
		city = player(1).initCity(61, 31)
		team(1).changeProjectCount(iTheInternet, 1)
		
		events.fireEvent("projectBuilt", city, iTheInternet)
		
		try:
			self.assertEqual(goal.state, FAILURE)
		finally:
			city.kill()
			team(1).changeProjectCount(iTheInternet, -1)
	
	def testProjectCheckedOnEventMultiple(self):
		goal = Condition.project(iTheInternet, iHumanGenome).activate(0)
		
		city = player(0).initCity(61, 31)
		team(0).changeProjectCount(iTheInternet, 1)
		team(0).changeProjectCount(iHumanGenome, 1)
		
		events.fireEvent("projectBuilt", city, iTheInternet)
		events.fireEvent("projectBuilt", city, iHumanGenome)
		
		try:
			self.assertEqual(goal.state, SUCCESS)
		finally:
			city.kill()
			team(0).changeProjectCount(iTheInternet, -1)
			team(0).changeProjectCount(iHumanGenome, -1)
	
	def testRouteNone(self):
		goal = Condition.route(plots.of([(60, 30), (61, 30), (62, 30)]), iRouteRoad).activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testRouteSome(self):
		area = plots.of([(60, 30), (61, 30), (62, 30)])
		goal = Condition.route(area, iRouteRoad).activate(0)
		
		for plot in area.without((60, 30)):
			plot.setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			for plot in area.without((60, 30)):
				plot.setRouteType(-1)
	
	def testRouteAll(self):
		area = plots.of([(60, 30), (61, 30), (62, 30)])
		goal = Condition.route(area, iRouteRoad).activate(0)
		
		for plot in area:
			plot.setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			for plot in area:
				plot.setRouteType(-1)
			
	def testAreaNoStateReligionSome(self):
		goal = Condition.areaNoStateReligion(plots.rectangle((60, 30), (65, 35)), iCatholicism).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		
		player(0).setLastStateReligion(iCatholicism)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city1.kill()
			city2.kill()
		
			player(0).setLastStateReligion(-1)
	
	def testAreaNoStateReligionAll(self):
		goal = Condition.areaNoStateReligion(plots.rectangle((60, 30), (65, 35)), iCatholicism).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city1.kill()
			city2.kill()
	
	def testCultureCoveredNone(self):
		goal = Condition.cultureCovered(plots.of([(60, 30), (61, 30), (62, 30)])).activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testCultureCoveredSome(self):
		goal = Condition.cultureCovered(plots.of([(60, 30), (61, 30), (62, 30)])).activate(0)
		
		plot(60, 30).setOwner(0)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			plot(60, 30).setOwner(-1)
	
	def testCultureCoveredAll(self):
		area = plots.of([(60, 30), (61, 30), (62, 30)])
		goal = Condition.cultureCovered(area).activate(0)
		
		for plot in area:
			plot.setOwner(0)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			for plot in area:
				plot.setOwner(-1)
	
	def testCultureCoveredOther(self):
		area = plots.of([(60, 30), (61, 30), (62, 30)])
		goal = Condition.cultureCovered(area).activate(0)
		
		for plot in area:
			plot.setOwner(1)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			for plot in area:
				plot.setOwner(-1)
	
	def testNotCommunist(self):
		goal = Condition.communist().activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testCommunist(self):
		goal = Condition.communist().activate(0)
		
		player(0).setCivics(iCivicsEconomy, iCentralPlanning)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			player(0).setCivics(iCivicsEconomy, iRedistribution)
	
	def testNoForeignCities(self):
		goal = Condition.noForeignCities(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city = player(0).initCity(61, 31)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city.kill()
	
	def testNoForeignCitiesNoCities(self):
		goal = Condition.noForeignCities(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		self.assertEqual(bool(goal), False)
	
	def testNoForeignCitiesMinor(self):
		goal = Condition.noForeignCities(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city = player(iIndependent).initCity(61, 31)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city.kill()
	
	def testNoForeignCitiesOther(self):
		goal = Condition.noForeignCities(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city0.kill()
			city1.kill()
	
	def testNoForeignCitiesOnly(self):
		goal = Condition.noForeignCities(plots.rectangle((60, 30), (65, 35))).only([iBabylonia]).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(2).initCity(63, 31)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city0.kill()
			city1.kill()
	
	def testNoForeignCitiesOnlyOther(self):
		goal = Condition.noForeignCities(plots.rectangle((60, 30), (65, 35))).only([iBabylonia]).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city0.kill()
			city1.kill()
	
	def testNoForeignCitiesExcluding(self):
		goal = Condition.noForeignCities(plots.rectangle((60, 30), (65, 35))).excluding([iBabylonia]).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city0.kill()
			city1.kill()
	
	def testNoForeignCitiesExcludingWith(self):
		goal = Condition.noForeignCities(plots.rectangle((60, 30), (65, 35))).excluding([iBabylonia]).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(2).initCity(63, 31)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city0.kill()
			city1.kill()
	
	def testTradeConnectionFalse(self):
		goal = Condition.tradeConnection().activate(0)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			goal.deactivate()
	
	def testTradeConnection(self):
		goal = Condition.tradeConnection().activate(0)
		
		team(1).meet(0, False)
		team(1).setOpenBorders(0, True)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			team(1).cutContact(0)
			team(1).setOpenBorders(0, False)
		
			city0.kill()
			city1.kill()
		
			for p in plots.rectangle((61, 31), (63, 31)):
				p.setRouteType(-1)
		
			goal.deactivate()
	
	def testMoreReligion(self):
		goal = Condition.moreReligion(plots.rectangle((60, 30), (65, 35)), iOrthodoxy, iCatholicism).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		city2 = player(2).initCity(65, 31)
		
		city0.setHasReligion(iOrthodoxy, True, False, False)
		city1.setHasReligion(iOrthodoxy, True, False, False)
		city2.setHasReligion(iCatholicism, True, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "2 / 1")
		finally:
			for city in [city0, city1, city2]:
				city.kill()
	
	def testMoreReligionEqual(self):
		goal = Condition.moreReligion(plots.rectangle((60, 30), (65, 35)), iOrthodoxy, iCatholicism).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		city0.setHasReligion(iOrthodoxy, True, False, False)
		city1.setHasReligion(iCatholicism, True, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 1")
		finally:
			city0.kill()
			city1.kill()
	
	def testMoreReligionLess(self):
		goal = Condition.moreReligion(plots.rectangle((60, 30), (65, 35)), iOrthodoxy, iCatholicism).activate(0)
		
		city0 = player(0).initCity(61, 31)
		
		city0.setHasReligion(iCatholicism, True, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 1")
		finally:
			city0.kill()
	
	def testMoreReligionOutside(self):
		goal = Condition.moreReligion(plots.rectangle((60, 30), (65, 35)), iOrthodoxy, iCatholicism).activate(0)
		
		city0 = player(0).initCity(25, 25)
		city0.setHasReligion(iOrthodoxy, True, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 0")
		finally:
			city0.kill()
	
	def testMoreCulture(self):
		goal = Condition.moreCulture().activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		city2 = player(2).initCity(65, 31)
		
		city0.setCulture(0, 1000, False)
		city1.setCulture(1, 500, False)
		city2.setCulture(2, 100, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1000 / 600")
		finally:
			for city in [city0, city1, city2]:
				city.kill()
	
	def testMoreCultureLess(self):
		goal = Condition.moreCulture().activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		city2 = player(2).initCity(65, 31)
		
		city0.setCulture(0, 1000, False)
		city1.setCulture(1, 600, False)
		city2.setCulture(2, 600, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1000 / 1200")
		finally:
			for city in [city0, city1, city2]:
				city.kill()
	
	def testMoreCultureThan(self):
		goal = Condition.moreCulture().than([iBabylonia]).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		city2 = player(2).initCity(65, 31)
		
		city0.setCulture(0, 1000, False)
		city1.setCulture(1, 600, False)
		city2.setCulture(2, 600, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1000 / 600")
		finally:
			for city in [city0, city1, city2]:
				city.kill()
	
	def testAllAttitude(self):
		goal = Condition.allAttitude(AttitudeTypes.ATTITUDE_PLEASED).activate(0)
		
		self.assertEqual(players.major().alive().count(), 3)
		self.assertEqual(player(1).AI_getAttitude(0), AttitudeTypes.ATTITUDE_CAUTIOUS)
		self.assertEqual(player(2).AI_getAttitude(0), AttitudeTypes.ATTITUDE_CAUTIOUS)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 2")
		
		team(0).meet(1, False)
		team(0).meet(2, False)
		
		self.assertEqual(player(0).canContact(1), True)
		self.assertEqual(player(0).canContact(2), True)
		
		player(1).AI_setAttitudeExtra(0, 100)
		player(2).AI_setAttitudeExtra(0, 100)
		
		self.assertEqual(player(1).AI_getAttitude(0), AttitudeTypes.ATTITUDE_FRIENDLY)
		self.assertEqual(player(2).AI_getAttitude(0), AttitudeTypes.ATTITUDE_FRIENDLY)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "2 / 2")
		finally:
			player(1).AI_setAttitudeExtra(0, 0)
			player(2).AI_setAttitudeExtra(0, 0)
			team(1).cutContact(0)
			team(2).cutContact(0)
			goal.deactivate()
	
	def testNoStateReligion(self):
		goal = Condition.noStateReligion(iOrthodoxy).activate(0)
		
		player(0).setLastStateReligion(iJudaism)
		player(1).setLastStateReligion(iCatholicism)
		player(2).setLastStateReligion(iProtestantism)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "0")
		finally:
			for i in [0, 1, 2]:
				player(i).setLastStateReligion(-1)
	
	def testNoStateReligionStillLeft(self):
		goal = Condition.noStateReligion(iOrthodoxy).activate(0)
		
		player(0).setLastStateReligion(iJudaism)
		player(1).setLastStateReligion(iOrthodoxy)
		player(2).setLastStateReligion(iOrthodoxy)
	
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "2")
		finally:
			for i in [0, 1, 2]:
				player(i).setLastStateReligion(-1)
	
	def testStateReligionPercent(self):
		goal = Condition.stateReligionPercent(iConfucianism, 50).activate(0)
		
		player(0).setLastStateReligion(iConfucianism)
		player(1).setLastStateReligion(iConfucianism)
		player(2).setLastStateReligion(iTaoism)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "2 / 1")
		finally:
			for i in [0, 1, 2]:
				player(i).setLastStateReligion(-1)
	
	def testStateReligionPercentOrSecular(self):
		goal = Condition.stateReligionPercent(iConfucianism, 50).orSecular().activate(0)
		
		player(0).setLastStateReligion(iConfucianism)
		player(1).setCivics(iCivicsReligion, iSecularism)
		player(2).setLastStateReligion(iTaoism)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "2 / 1")
		finally:
			player(0).setLastStateReligion(-1)
			player(1).setCivics(iCivicsReligion, iAnimism)
			player(2).setLastStateReligion(-1)
	
	def testNoReligionPercent(self):
		goal = Condition.noReligionPercent(50).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setHasReligion(iBuddhism, True, False, False)
		
		city2 = player(0).initCity(63, 31)
		city2.setHasReligion(iConfucianism, True, False, False)
		
		city3 = player(0).initCity(65, 31)
		city4 = player(0).initCity(67, 31)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "2 / 4")
		finally:
			for city in [city1, city2, city3, city4]:
				city.kill()
	
	def testNoReligionPercentTooMany(self):
		goal = Condition.noReligionPercent(50).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setHasReligion(iBuddhism, True, False, False)
		
		city2 = player(0).initCity(63, 31)
		city2.setHasReligion(iConfucianism, True, False, False)
		
		city3 = player(0).initCity(65, 31)
		city3.setHasReligion(iTaoism, True, False, False)
		
		city4 = player(0).initCity(67, 31)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "3 / 4")
		finally:
			for city in [city1, city2, city3, city4]:
				city.kill()
	
	def testGoldPercent(self):
		goal = Condition.goldPercent(50).activate(0)
		
		for iPlayer in players.major().alive():
			player(iPlayer).setGold(0)
		
		player(0).setGold(50)
		player(1).setGold(60)
		player(2).setGold(40)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "50 / 100")
		finally:
			for i in [0, 1, 2]:
				player(i).setGold(0)


class TestCallback(object):
	def __call__(self, goal):
		print goal


class TestCountGoals(ExtendedTestCase):

	def setUp(self):
		for plot in plots.all():
			plot.resetCultureConversion()
		
	def testPickle(self):
		goal = BuildingCount(iGranary, 3).activate(0)
		
		pickle.dumps(goal)
	
	def testPickleWithCallback(self):
		goal = BuildingCount(iGranary, 3).activate(0, TestCallback())
		
		pickle.dumps(goal)
	
	def testBuildingNone(self):
		goal = Count.building(iGranary, 3).activate(0)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 3")
		finally:
			goal.deactivate()
	
	def testBuildingSome(self):
		goal = Count.building(iGranary, 3).activate(0)
		
		tiles = [(61, 31), (63, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "2 / 3")
		finally:
			for tile in tiles:
				city_(tile).kill()
		
			goal.deactivate()
	
	def testBuildingAll(self):
		goal = Count.building(iGranary, 3).activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "3 / 3")
		finally:
			for tile in tiles:
				city_(tile).kill()
		
			goal.deactivate()
			
	def testBuildingMore(self):
		goal = Count.building(iGranary, 3).activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31), (67, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "4 / 3")
		finally:
			for tile in tiles:
				city_(tile).kill()
		
			goal.deactivate()
	
	def testBuildingMultiplePartial(self):
		goal = Count.building((iGranary, 3), (iBarracks, 2)).activate(0)
		
		tiles = [(61, 31), (63, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasRealBuilding(iGranary, True)
			city.setHasRealBuilding(iBarracks, True)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), '\n'.join(["2 / 3", "2 / 2"]))
		finally:
			for tile in tiles:
				city_(tile).kill()
		
			goal.deactivate()
	
	def testBuildingMultipleAll(self):
		goal = Count.building((iGranary, 3), (iBarracks, 2)).activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasRealBuilding(iGranary, True)
			city.setHasRealBuilding(iBarracks, True)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), '\n'.join(["3 / 3", "3 / 2"]))
		finally:
			for tile in tiles:
				city_(tile).kill()
		
			goal.deactivate()
	
	def testBuildingSum(self):
		goal = Count.building(sum([iGranary, iBarracks, iLibrary]), 3).activate(0)
		
		city = player(0).initCity(61, 31)
		for iBuilding in [iGranary, iBarracks, iLibrary]:
			city.setHasRealBuilding(iBuilding, True)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "3 / 3")
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testBuildingCheck(self):
		goal = Count.building(iGranary, 1).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.state, POSSIBLE)
		
			events.fireEvent("buildingBuilt", city, iGranary)
		
			self.assertEqual(goal.state, SUCCESS)
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testBuildingCheckDifferentBuilding(self):
		goal = Count.building(iGranary, 1).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.state, POSSIBLE)
		
			events.fireEvent("buildingBuilt", city, iBarracks)
		
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testBuildingCheckCityAcquired(self):
		goal = Count.building(iGranary, 1).activate(0)
		
		city = player(1).initCity(61, 31)
		city.setHasRealBuilding(iGranary, True)
		
		player(0).acquireCity(city, False, True)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			city_(61, 31).kill()
		
			goal.deactivate()
	
	def testBuildingCheckSum(self):
		goal = Count.building(sum([iGranary, iLibrary, iCastle]), 3).activate(0)
		
		city = player(0).initCity(61, 31)
		for iBuilding in [iGranary, iLibrary, iCastle]:
			city.setHasRealBuilding(iBuilding, True)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.state, POSSIBLE)
		
			events.fireEvent("buildingBuilt", city, iCastle)
		
			self.assertEqual(goal.state, SUCCESS)
		finally:
			city_(61, 31).kill()
		
			goal.deactivate()
	
	def testBuildingDeferred(self):
		goal = Count.building(stateReligionCathedral(), 1).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iOrthodoxCathedral, True)
		
		try:
			self.assertEqual(str(goal), "0 / 1")
			self.assertEqual(bool(goal), False)
		
			player(0).setLastStateReligion(iCatholicism)
			self.assertEqual(bool(goal), False)
		
			player(0).setLastStateReligion(iOrthodoxy)
			self.assertEqual(bool(goal), True)
		finally:
			player(0).setLastStateReligion(-1)
			city.kill()
		
			goal.deactivate()
	
	def testBuildingUniqueInGoal(self):
		goal = Count.building(iObelisk, 1).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iObelisk, True)
		
		events.fireEvent("buildingBuilt", city, iObelisk)
		
		try:
			self.assertEqual(str(goal), "1 / 1")
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testBuildingUnique(self):
		goal = Count.building(iMonument, 1).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iObelisk, True)
		
		events.fireEvent("buildingBuilt", city, iObelisk)
		
		try:
			self.assertEqual(str(goal), "1 / 1")
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testBuildingWorld(self):
		goal = Count.building(iMonument, 3).world().activate(0)
		
		city0 = player(iEgypt).initCity(61, 31)
		city0.setHasRealBuilding(iObelisk, True)
		
		city1 = player(iBabylonia).initCity(63, 31)
		city1.setHasRealBuilding(iMonument, True)
		
		city2 = player(iHarappa).initCity(65, 31)
		city2.setHasRealBuilding(iMonument, True)
		
		try:
			self.assertEqual(str(goal), "3 / 3")
			self.assertEqual(bool(goal), True)
		finally:
			for city in [city0, city1, city2]:
				city.kill()
			goal.deactivate()
	
	def testCultureLess(self):
		goal = Count.culture(500).activate(0)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 500")
		finally:
			goal.deactivate()
	
	def testCultureMore(self):
		goal = Count.culture(500).activate(0)
		
		city = player(0).initCity(61, 31)
		city.changeCulture(0, 1000, True)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1000 / 500")
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testGoldLess(self):
		goal = Count.gold(500).activate(0)
		
		player(0).changeGold(100)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "100 / 500")
		finally:
			player(0).changeGold(-100)
	
	def testGoldMore(self):
		goal = Count.gold(500).activate(0)
		
		player(0).changeGold(1000)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1000 / 500")
		finally:
			player(0).changeGold(-1000)
	
	def testResourceLess(self):
		goal = Count.resource(iGold, 1).activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
	
	def testResourceEnough(self):
		goal = Count.resource(iGold, 1).activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1 / 1")
		finally:
			plot(61, 31).setBonusType(-1)
			city.kill()
	
	def testResourcesSome(self):
		goal = Count.resource((iGold, 1), (iSilver, 1)).activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
			self.assertEqual(player(0).getNumAvailableBonuses(iSilver), 0)
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), '\n'.join(["1 / 1", "0 / 1"]))
		finally:
			plot(61, 31).setBonusType(-1)
			city.kill()
	
	def testResourcesAll(self):
		goal = Count.resource((iGold, 1), (iSilver, 1)).activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city1 = player(0).initCity(61, 31)
		city1.setHasRealBuilding(iPalace, True)
		
		plot(63, 31).setBonusType(iSilver)
		city2 = player(0).initCity(63, 31)
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
			self.assertEqual(player(0).getNumAvailableBonuses(iSilver), 1)
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), '\n'.join(["1 / 1", "1 / 1"]))
		finally:
			city1.kill()
			city2.kill()
		
			plot(61, 31).setBonusType(-1)
			plot(62, 31).setRouteType(-1)
			plot(63, 31).setBonusType(-1)
	
	def testResourceSum(self):
		goal = Count.resource(sum([iGold, iSilver]), 2).activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city1 = player(0).initCity(61, 31)
		city1.setHasRealBuilding(iPalace, True)
		
		plot(63, 31).setBonusType(iSilver)
		city2 = player(0).initCity(63, 31)
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
			self.assertEqual(player(0).getNumAvailableBonuses(iSilver), 1)
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "2 / 2")
		finally:
			city1.kill()
			city2.kill()
		
			plot(61, 31).setBonusType(-1)
			plot(62, 31).setRouteType(-1)
			plot(63, 31).setBonusType(-1)
	
	def testControlledResourceLess(self):
		goal = Count.controlledResource(iGold, 1).activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1")
	
	def testControlledResourceEnough(self):
		goal = Count.controlledResource(iGold, 1).activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1 / 1")
		finally:
			plot(61, 31).setBonusType(-1)
			city.kill()
	
	def testControlledResourcesSome(self):
		goal = Count.controlledResource((iGold, 1), (iSilver, 1)).activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city = player(0).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
			self.assertEqual(player(0).getNumAvailableBonuses(iSilver), 0)
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), '\n'.join(["1 / 1", "0 / 1"]))
		finally:
			plot(61, 31).setBonusType(-1)
			city.kill()
	
	def testControlledResourcesAll(self):
		goal = Count.controlledResource((iGold, 1), (iSilver, 1)).activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city1 = player(0).initCity(61, 31)
		city1.setHasRealBuilding(iPalace, True)
		
		plot(63, 31).setBonusType(iSilver)
		city2 = player(0).initCity(63, 31)
		
		plot(62, 31).setRouteType(iRouteRoad)
		
		try:
			self.assertEqual(player(0).getNumAvailableBonuses(iGold), 1)
			self.assertEqual(player(0).getNumAvailableBonuses(iSilver), 1)
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), '\n'.join(["1 / 1", "1 / 1"]))
		finally:
			city1.kill()
			city2.kill()
		
			plot(61, 31).setBonusType(-1)
			plot(62, 31).setRouteType(-1)
			plot(63, 31).setBonusType(-1)
	
	def testControlledResourceVassal(self):
		goal = Count.controlledResource(iGold, 1).activate(0)
		
		plot(61, 31).setBonusType(iGold)
		city = player(2).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqual(player(2).getNumAvailableBonuses(iGold), 1)
		
			team(2).setVassal(team(0).getID(), True, False)
		
			self.assertEqual(team(2).isVassal(team(0).getID()), True)
		
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1 / 1")
		finally:
			team(2).setVassal(team(0).getID(), False, False)
			city.kill()
	
	def testImprovementLess(self):
		goal = Count.improvement(iCottage, 3).activate(0)
		
		city = player(0).initCity(61, 31)
		tiles = [(60, 31), (62, 31)]
		for plot in plots.of(tiles):
			plot.setOwner(0)
			plot.setImprovementType(iCottage)
		
		try:
			self.assertEqual(player(0).getImprovementCount(iCottage), 2)
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "2 / 3")
		finally:
			city.kill()
			for tile in plots.of(tiles):
				plot.setImprovementType(-1)
	
	def testImprovementMore(self):
		goal = Count.improvement(iCottage, 3).activate(0)
		
		city = player(0).initCity(61, 31)
		tiles = [(60, 31), (62, 31), (61, 30), (61, 32)]
		for plot in plots.of(tiles):
			plot.setOwner(0)
			plot.setImprovementType(iCottage)
		
		try:
			self.assertEqual(player(0).getImprovementCount(iCottage), 4)
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "4 / 3")
		finally:
			city.kill()
			for plot in plots.of(tiles):
				plot.setImprovementType(-1)
	
	def testPopulationLess(self):
		goal = Count.population(5).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setPopulation(3)
		
		try:
			self.assertEqual(player(0).getNumCities(), 1)
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "3 / 5")
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testPopulationMore(self):
		goal = Count.population(5).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setPopulation(10)
		
		try:
			self.assertEqual(player(0).getNumCities(), 1)
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "10 / 5")
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testPopulationMultipleCities(self):
		goal = Count.population(5).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		
		city1.setPopulation(3)
		city2.setPopulation(3)
		
		try:
			self.assertEqual(player(0).getNumCities(), 2)
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "6 / 5")
		finally:
			city1.kill()
			city2.kill()
		
			goal.deactivate()
	
	def testCorporationLess(self):
		goal = Count.corporation(iSilkRoute, 2).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasCorporation(iSilkRoute, True, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			city.kill()
	
	def testCorporationMore(self):
		goal = Count.corporation(iSilkRoute, 2).activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasCorporation(iSilkRoute, True, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "3 / 2")
			self.assertEqual(goal.state, SUCCESS)
		finally:
			for tile in tiles:
				city_(tile).kill()
	
	def testCorporationsSome(self):
		goal = Count.corporation((iSilkRoute, 2), (iTradingCompany, 2)).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		
		city1.setHasCorporation(iSilkRoute, True, False, False)
		city2.setHasCorporation(iSilkRoute, True, False, False)
		
		city1.setHasCorporation(iTradingCompany, True, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), '\n'.join(["2 / 2", "1 / 2"]))
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			city1.kill()
			city2.kill()
	
	def testCorporationsAll(self):
		goal = Count.corporation((iSilkRoute, 2), (iTradingCompany, 2)).activate(0)
		
		tiles = [(61, 31), (63, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setHasCorporation(iSilkRoute, True, False, False)
			city.setHasCorporation(iTradingCompany, True, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), '\n'.join(["2 / 2", "2 / 2"]))
			self.assertEqual(goal.state, SUCCESS)
		finally:
			for tile in tiles:
				city_(tile).kill()
	
	def testUnitLess(self):
		goal = Count.unit(iSwordsman, 3).activate(0)
		
		units = makeUnits(0, iSwordsman, (0, 0), 2)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "2 / 3")
		finally:
			for unit in units:
				unit.kill(False, -1)
	
	def testUnitMore(self):
		goal = Count.unit(iSwordsman, 3).activate(0)
		
		units = makeUnits(0, iSwordsman, (0, 0), 4)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "4 / 3")
		finally:
			for unit in units:
				unit.kill(False, -1)
	
	def testUnitsSome(self):
		goal = Count.unit((iSwordsman, 3), (iArcher, 3)).activate(0)
		
		swordsmen = makeUnits(0, iSwordsman, (0, 0), 3)
		archers = makeUnits(0, iArcher, (0, 0), 2)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), '\n'.join(["3 / 3", "2 / 3"]))
		finally:
			for unit in swordsmen:
				unit.kill(False, -1)
		
			for unit in archers:
				unit.kill(False, -1)
	
	def testUnitsAll(self):
		goal = Count.unit((iSwordsman, 3), (iArcher, 3)).activate(0)
		
		swordsmen = makeUnits(0, iSwordsman, (0, 0), 3)
		archers = makeUnits(0, iArcher, (0, 0), 3)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), '\n'.join(["3 / 3", "3 / 3"]))
		finally:
			for unit in swordsmen:
				unit.kill(False, -1)
		
			for unit in archers:
				unit.kill(False, -1)
	
	def testUnitUnique(self):
		goal = Count.unit(iSwordsman, 3).activate(0)
		
		units = makeUnits(0, iLegion, (0, 0), 3)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "3 / 3")
		finally:
			for unit in units:
				unit.kill(False, -1)
	
	def testUnitUniqueRequirement(self):
		goal = Count.unit(iLegion, 3).activate(0)
		
		units = makeUnits(0, iSwordsman, (0, 0), 3)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "3 / 3")
		finally:
			for unit in units:
				unit.kill(False, -1)
	
	def testUnitCombat(self):
		goal = Count.unitCombat(UnitCombatTypes.UNITCOMBAT_ARCHER, 5).activate(0)
		
		team(0).setHasTech(iTanning, True, 0, True, False)
		team(0).setHasTech(iContract, True, 0, True, False)
		
		archers = makeUnits(0, iArcher, (0, 0), 3)
		crossbowmen = makeUnits(0, iSkirmisher, (0, 1), 3)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "6 / 5")
		finally:
			for unit in archers + crossbowmen:
				unit.kill(False, -1)
			
			team(0).setHasTech(iTanning, False, 0, True, False)
			team(0).setHasTech(iContract, False, 0, True, False)
	
	def testUnitCombatSum(self):
		goal = Count.unitCombat(sum(UnitCombatTypes.UNITCOMBAT_ARCHER, UnitCombatTypes.UNITCOMBAT_GUN), 5).activate(0)
		
		team(0).setHasTech(iCommune, True, 0, True, False)
		team(0).setHasTech(iFirearms, True, 0, True, False)
		
		archers = makeUnits(0, iLongbowman, (0, 0), 3)
		musketeers = makeUnits(0, iArquebusier, (0, 1), 3)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "6 / 5")
		finally:
			for unit in archers + musketeers:
				unit.kill(False, -1)
			
			team(0).setHasTech(iCommune, False, 0, True, False)
			team(0).setHasTech(iFirearms, False, 0, True, False)
	
	def testUnitCombatIgnoresOutdated(self):
		goal = Count.unitCombat(UnitCombatTypes.UNITCOMBAT_ARCHER, 3).activate(0)
		
		team(0).setHasTech(iCommune, True, 0, True, False)
		team(0).setHasTech(iMachinery, True, 0, True, False)
		
		archers = makeUnits(0, iArcher, (0, 0), 3)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 3")
		finally:
			for unit in archers:
				unit.kill(False, -1)
			
			team(0).setHasTech(iCommune, False, 0, True, False)
			team(0).setHasTech(iMachinery, False, 0, True, False)
	
	def testNumCitiesLess(self):
		goal = Count.numCities(plots.rectangle((60, 30), (65, 35)), 2).activate(0)
		
		city = player(0).initCity(61, 31)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
		finally:
			city.kill()
	
	def testNumCitiesMore(self):
		goal = Count.numCities(plots.rectangle((60, 30), (65, 35)), 2).activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		for tile in tiles:
			player(0).initCity(*tile)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "3 / 2")
		finally:
			for tile in tiles:
				city_(tile).kill()
	
	def testNumCitiesSum(self):
		goal = Count.numCities(sum([plots.rectangle((60, 30), (62, 35)), plots.rectangle((63, 30), (65, 35))]), 2).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(64, 31)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "2 / 2")
		finally:
			city1.kill()
			city2.kill()
	
	def testSettledCitiesAll(self):
		goal = Count.settledCities(plots.rectangle((60, 30), (65, 35)), 2).activate(0)
		
		tiles = [(61, 31), (63, 31)]
		for tile in tiles:
			player(0).initCity(*tile)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "2 / 2")
		finally:
			for tile in tiles:
				city_(tile).kill()
	
	def testSettledCitiesSome(self):
		goal = Count.settledCities(plots.rectangle((60, 30), (65, 35)), 2).activate(0)
		
		city1 = player(0).initCity(61, 31)
		
		city2 = player(1).initCity(63, 31)
		player(0).acquireCity(city2, True, False)
		city2 = city_(63, 31)
		
		try:
			self.assertEqual(player(0).getNumCities(), 2)
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
		finally:
			city1.kill()
			city2.kill()
	
	def testConqueredCitiesAll(self):
		goal = Count.conqueredCities(2).inside(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city1 = player(1).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		
		player(0).acquireCity(city1, True, False)
		player(0).acquireCity(city2, True, False)
		
		try:
			self.assertEqual(player(0).getNumCities(), 2)
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "2 / 2")
		finally:
			city_(61, 31).kill()
			city_(63, 31).kill()
		
			goal.deactivate()
	
	def testConqueredCitiesSome(self):
		goal = Count.conqueredCities(2).inside(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(1).initCity(63, 31)
		
		player(0).acquireCity(city2, True, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
		finally:
			city1.kill()
			city_(63, 31).kill()
		
			goal.deactivate()
	
	def testConqueredCitiesTraded(self):
		goal = Count.conqueredCities(1).inside(plots.rectangle((60, 30), (65, 35))).activate(0)
		
		city = player(1).initCity(61, 31)
		
		player(0).acquireCity(city, False, True)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 1")
		finally:
			city_(61, 31).kill()
		
			goal.deactivate()
	
	def testConqueredCitiesCivs(self):
		goal = Count.conqueredCities(1).civs([iBabylonia]).activate(0)
		
		city = player(iBabylonia).initCity(61, 31)
		player(0).acquireCity(city, True, False)
		city = city_(61, 31)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1 / 1")
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testConqueredCitiesCivsTrade(self):
		goal = Count.conqueredCities(1).civs([iBabylonia]).activate(0)
		
		city = player(iBabylonia).initCity(61, 31)
		player(0).acquireCity(city, False, True)
		city = city_(61, 31)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 1")
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testConqueredCitiesMultipleCivs(self):
		goal = Count.conqueredCities(3).civs([iBabylonia, iHarappa, iGreece]).activate(0)
		
		city1 = player(iBabylonia).initCity(61, 31)
		player(0).acquireCity(city1, True, False)
		city1 = city_(61, 31)
		
		city2 = player(iHarappa).initCity(63, 31)
		player(0).acquireCity(city2, True, False)
		city2 = city_(63, 31)
		
		city3 = player(iGreece).initCity(65, 31)
		player(0).acquireCity(city3, True, False)
		city3 = city_(65, 31)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "3 / 3")
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
		
			goal.deactivate()
	
	def testConqueredCitiesOutside(self):
		goal = Count.conqueredCities(2).outside(plots.rectangle((60, 30), (62, 32))).activate(0)
		
		city1 = player(1).initCity(61, 31)
		player(0).acquireCity(city1, True, False)
		city1 = city_(61, 31)
		
		city2 = player(1).initCity(63, 31)
		player(0).acquireCity(city2, True, False)
		city2 = city_(63, 31)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
		finally:
			city1.kill()
			city2.kill()
		
			goal.deactivate()
	
	def testConqueredCitiesProgress(self):
		goal = Count.conqueredCities(2).activate(0)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Conquered cities: 0 / 2" % self.FAILURE_CHAR]])
		finally:
			goal.deactivate()
	
	def testConqueredCitiesProgressInside(self):
		goal = Count.conqueredCities(2).inside(plots.region(rBritain).named("BRITAIN")).activate(0)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Conquered cities in Britain: 0 / 2" % self.FAILURE_CHAR]])
		finally:
			goal.deactivate()
	
	def testOpenBordersLess(self):
		goal = Count.openBorders(2).activate(0)
		
		team(0).setOpenBorders(team(1).getID(), True)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
		finally:
			team(0).setOpenBorders(team(1).getID(), False)
	
	def testOpenBordersMore(self):
		goal = Count.openBorders(1).activate(0)
		
		others = [1, 2]
		for id in others:
			team(0).setOpenBorders(team(id).getID(), True)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "2 / 1")
		finally:
			for id in others:
				team(0).setOpenBorders(team(id).getID(), False)
	
	def testOpenBordersCivs(self):
		goal = Count.openBorders(2).civs([iBabylonia, iHarappa]).activate(0)
		
		others = [iBabylonia, iGreece]
		for iCiv in others:
			team(0).setOpenBorders(team(iCiv).getID(), True)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
		finally:
			for iCiv in others:
				team(0).setOpenBorders(team(iCiv).getID(), False)
	
	def testSpecialistLess(self):
		goal = Count.specialist(iSpecialistGreatScientist, 3).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setFreeSpecialistCount(iSpecialistGreatScientist, 1)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 3")
		finally:
			city.kill()
	
	def testSpecialistMore(self):
		goal = Count.specialist(iSpecialistGreatScientist, 3).activate(0)
		
		tiles = [(61, 31), (63, 31)]
		for tile in tiles:
			city = player(0).initCity(*tile)
			city.setFreeSpecialistCount(iSpecialistGreatScientist, 2)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "4 / 3")
		finally:
			for tile in tiles:
				city_(tile).kill()
	
	def testSpecialistsSome(self):
		goal = Count.specialist((iSpecialistGreatScientist, 3), (iSpecialistGreatArtist, 3)).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setFreeSpecialistCount(iSpecialistGreatScientist, 3)
		city.setFreeSpecialistCount(iSpecialistGreatArtist, 2)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), '\n'.join(["3 / 3", "2 / 3"]))
		finally:
			city.kill()
	
	def testSpecialistsAll(self):
		goal = Count.specialist((iSpecialistGreatScientist, 3), (iSpecialistGreatArtist, 3)).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setFreeSpecialistCount(iSpecialistGreatScientist, 3)
		city.setFreeSpecialistCount(iSpecialistGreatArtist, 3)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), '\n'.join(["3 / 3", "3 / 3"]))
		finally:
			city.kill()
	
	def testSpecialistSum(self):
		goal = Count.specialist(sum([iSpecialistGreatScientist, iSpecialistGreatArtist]), 4).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setFreeSpecialistCount(iSpecialistGreatScientist, 2)
		city.setFreeSpecialistCount(iSpecialistGreatArtist, 2)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "4 / 4")
		finally:
			city.kill()
	
	def testSpecialistReligion(self):
		goal = Count.specialist(iSpecialistGreatScientist, 4).religion().activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setFreeSpecialistCount(iSpecialistGreatScientist, 2)
		
		city2 = player(1).initCity(63, 31)
		city2.setFreeSpecialistCount(iSpecialistGreatScientist, 2)
		
		city3 = player(2).initCity(65, 31)
		city3.setFreeSpecialistCount(iSpecialistGreatScientist, 1)
		
		player(0).setLastStateReligion(iBuddhism)
		player(1).setLastStateReligion(iBuddhism)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "4 / 4")
		finally:
			for city in [city1, city2, city3]:
				city.kill()
			player(0).setLastStateReligion(-1)
			player(1).setLastStateReligion(-1)
			goal.deactivate()
	
	def testAverageCulture(self):
		goal = Count.averageCulture(500).activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		city1, city2, city3 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setCulture(0, 500, True)
		city2.setCulture(0, 1000, True)
		city3.setCulture(0, 1500, True)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1000 / 500")
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
	
	def testPopulationCitiesNotEnough(self):
		goal = Count.populationCities(10, 3).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setPopulation(12)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 3")
		finally:
			city.kill()
	
	def testPopulationCitiesLess(self):
		goal = Count.populationCities(10, 3).activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		city1, city2, city3 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setPopulation(12)
		city2.setPopulation(10)
		city3.setPopulation(8)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "2 / 3")
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
	
	def testPopulationCitiesMore(self):
		goal = Count.populationCities(10, 3).activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31), (67, 31)]
		city1, city2, city3, city4 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setPopulation(16)
		city2.setPopulation(14)
		city3.setPopulation(12)
		city4.setPopulation(10)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "4 / 3")
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			city4.kill()
	
	def testCultureCitiesNotEnough(self):
		goal = Count.cultureCities(500, 3).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setCulture(0, 600, True)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 3")
		finally:
			city.kill()
	
	def testCultureCitiesLess(self):
		goal = Count.cultureCities(500, 3).activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		city1, city2, city3 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setCulture(0, 600, True)
		city2.setCulture(0, 500, True)
		city3.setCulture(0, 400, True)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "2 / 3")
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
	
	def testCultureCitiesMore(self):
		goal = Count.cultureCities(500, 3).activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31), (67, 31)]
		city1, city2, city3, city4 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setCulture(0, 800, True)
		city2.setCulture(0, 700, True)
		city3.setCulture(0, 600, True)
		city4.setCulture(0, 500, True)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "4 / 3")
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			city4.kill()
	
	def testCultureLevelNotEnough(self):
		goal = Count.cultureLevelCities(iCultureLevelRefined, 3).activate(0)
		
		city = player(0).initCity(61, 31)
		
		city.setCulture(0, game.getCultureThreshold(iCultureLevelRefined), True)
		
		try:
			self.assertEqual(player(0).getNumCities(), 1)
			self.assertEqual(city.getCultureLevel(), iCultureLevelRefined)
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 3")
		finally:
			city.kill()
	
	def testCultureLevelLess(self):
		goal = Count.cultureLevelCities(iCultureLevelRefined, 3).activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31)]
		city1, city2, city3 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setCulture(0, game.getCultureThreshold(iCultureLevelInfluential), True)
		city2.setCulture(0, game.getCultureThreshold(iCultureLevelRefined), True)
		city3.setCulture(0, game.getCultureThreshold(iCultureLevelDeveloping), True)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "2 / 3")
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
	
	def testCultureLevelCitiesMore(self):
		goal = Count.cultureLevelCities(iCultureLevelRefined, 3).activate(0)
		
		tiles = [(61, 31), (63, 31), (65, 31), (67, 31)]
		city1, city2, city3, city4 = (player(0).initCity(x, y) for x, y in tiles)
		city1.setCulture(0, game.getCultureThreshold(iCultureLevelInfluential), True)
		city2.setCulture(0, game.getCultureThreshold(iCultureLevelInfluential), True)
		city3.setCulture(0, game.getCultureThreshold(iCultureLevelRefined), True)
		city4.setCulture(0, game.getCultureThreshold(iCultureLevelRefined), True)
		
		try:
			self.assertEqual(str(goal), "4 / 3")
			self.assertEqual(bool(goal), True)
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			city4.kill()
	
	def testCitySpecialistWithoutCity(self):
		goal = Count.citySpecialist(city(61, 31), iSpecialistGreatScientist, 3).activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 3")
		
	def testCitySpecialistDifferentOwner(self):
		goal = Count.citySpecialist(city(61, 31), iSpecialistGreatScientist, 3).activate(0)
		
		_city = player(1).initCity(61, 31)
		_city.setFreeSpecialistCount(iSpecialistGreatScientist, 3)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 3")
		finally:
			_city.kill()
	
	def testCitySpecialistEnough(self):
		goal = Count.citySpecialist(city(61, 31), iSpecialistGreatScientist, 3).activate(0)
		
		_city = player(0).initCity(61, 31)
		_city.setFreeSpecialistCount(iSpecialistGreatScientist, 3)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "3 / 3")
		finally:
			_city.kill()
	
	def testCitySpecialistProgress(self):
		goal = Count.citySpecialist(city(61, 31).named("BERLIN"), iSpecialistGreatArtist, 3).activate(0)
		
		_city = player(0).initCity(61, 31)
		_city.setName("First", False)
		_city.setFreeSpecialistCount(iSpecialistGreatArtist, 3)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Great Artists in First: 3 / 3" % self.SUCCESS_CHAR]])
		finally:
			_city.kill()
	
	def testCitySpecialistProgressDifferentOwner(self):
		goal = Count.citySpecialist(city(61, 31).named("BERLIN"), iSpecialistGreatArtist, 3).activate(0)
		
		_city = player(1).initCity(61, 31)
		_city.setName("First", False)
		_city.setFreeSpecialistCount(iSpecialistGreatArtist, 3)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Great Artists in First (controlled by Babylonia): 0 / 3" % self.FAILURE_CHAR]])
		finally:
			_city.kill()
	
	def testCitySpecialistProgressNoCity(self):
		goal = Count.citySpecialist(city(61, 31).named("BERLIN"), iSpecialistGreatArtist, 3).activate(0)
		
		self.assertEqual(goal.progress(), [[u"%c (No City)" % self.FAILURE_CHAR]])
	
	def testCultureLevelNoCity(self):
		goal = Count.cultureLevel(city(61, 31), iCultureLevelRefined).activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "0 / 1000")
	
	def testCultureLevelDifferentOwner(self):
		goal = Count.cultureLevel(city(61, 31), iCultureLevelRefined).activate(0)
		
		_city = player(1).initCity(61, 31)
		_city.setCulture(0, 5000, True)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 1000")
		finally:
			_city.kill()
	
	def testCultureLevelEnough(self):
		goal = Count.cultureLevel(city(61, 31), iCultureLevelRefined).activate(0)
		
		_city = player(0).initCity(61, 31)
		_city.setCulture(0, 5000, True)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "5000 / 1000")
		finally:
			_city.kill()
	
	def testCultureLevelProgress(self):
		goal = Count.cultureLevel(city(61, 31), iCultureLevelRefined).activate(0)
		
		_city = player(0).initCity(61, 31)
		_city.setName("First", False)
		_city.setCulture(0, 5000, True)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Culture in First: 5000 / 1000" % self.SUCCESS_CHAR]])
		finally:
			_city.kill()
	
	def testCultureLevelProgressNoCity(self):
		goal = Count.cultureLevel(city(61, 31), iCultureLevelRefined).activate(0)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c (No City)" % self.FAILURE_CHAR]])
		finally:
			goal.deactivate()
	
	def testCultureLevelProgressDifferentOwner(self):
		goal = Count.cultureLevel(city(61, 31), iCultureLevelRefined).activate(0)
		
		_city = player(1).initCity(61, 31)
		_city.setName("First", False)
		_city.setCulture(0, 5000, True)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Culture in First (controlled by Babylonia): 0 / 1000" % self.FAILURE_CHAR]])
		finally:
			_city.kill()
	
	def testAttitude(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_FRIENDLY, 2).activate(0)
		
		for i in [1, 2]:
			team(i).meet(0, False)
			player(i).AI_setAttitudeExtra(0, 100)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "2 / 2")
		finally:
			for i in [1, 2]:
				team(i).cutContact(0)
				player(i).AI_setAttitudeExtra(0, 0)
	
	def testAttitudeInsufficient(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_FRIENDLY, 2).activate(0)
		
		for i in [1, 2]:
			team(i).meet(0, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 2")
		finally:
			for i in [1, 2]:
				team(i).cutContact(0)
	
	def testAttitudeNoContact(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_FRIENDLY, 2).activate(0)
		
		for i in [1, 2]:
			team(i).cutContact(0)
			player(i).AI_setAttitudeExtra(0, 100)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 2")
		finally:
			for i in [1, 2]:
				player(i).AI_setAttitudeExtra(0, 0)
	
	def testAttitudeCivs(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_FRIENDLY, 2).civs([iBabylonia]).activate(0)
		
		for i in [iBabylonia, iHarappa]:
			team(i).meet(0, False)
			player(i).AI_setAttitudeExtra(0, 100)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
		finally:
			for i in [iBabylonia, iHarappa]:
				team(i).cutContact(0)
				player(i).AI_setAttitudeExtra(0, 0)
		
	def testAttitudeReligion(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_FRIENDLY, 2).religion(iOrthodoxy).activate(0)
		
		for i in [1, 2]:
			team(i).meet(0, False)
			player(i).AI_setAttitudeExtra(0, 100)
		
		player(1).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
		finally:
			for i in [1, 2]:
				team(i).cutContact(0)
				player(i).AI_setAttitudeExtra(0, 0)
		
			player(1).setLastStateReligion(-1)
	
	def testAttitudeCommunist(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_FRIENDLY, 2).communist().activate(0)
		
		for i in [1, 2]:
			team(i).meet(0, False)
			player(i).AI_setAttitudeExtra(0, 100)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 2")
		
			player(1).setCivics(iCivicsEconomy, iCentralPlanning)
		
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
		finally:
			for i in [1, 2]:
				team(i).cutContact(0)
				player(i).AI_setAttitudeExtra(0, 0)
		
			player(1).setCivics(iCivicsEconomy, iReciprocity)
	
	def testAttitudeIndependent(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_FRIENDLY, 2).independent().activate(0)
		
		for i in [1, 2]:
			team(i).meet(0, False)
			player(i).AI_setAttitudeExtra(0, 100)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "2 / 2")
		
			team(1).setVassal(0, True, False)
		
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
		finally:
			for i in [1, 2]:
				team(i).cutContact(0)
				player(i).AI_setAttitudeExtra(0, 0)
		
			team(1).setVassal(0, False, False)
	
	def testAttitudeMinority(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_FRIENDLY, 2).minority(iCatholicism).activate(0)
		
		for i in [1, 2]:
			team(i).meet(0, False)
			player(i).AI_setAttitudeExtra(0, 100)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 2")
			
			city1 = player(1).initCity(61, 31)
			city1.setHasReligion(iCatholicism, True, False, False)
			
			city2 = player(3).initCity(63, 31)
			city2.setHasReligion(iCatholicism, True, False, False)
			
			try:
				self.assertEqual(bool(goal), False)
				self.assertEqual(str(goal), "1 / 2")
			finally:
				city1.kill()
				city2.kill()
		finally:
			for i in [1, 2]:
				team(i).cutContact(0)
				player(i).AI_setAttitudeExtra(0, 0)
	
	def testAttitudeChainedFilters(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_FRIENDLY, 2).civs([iBabylonia]).religion(iOrthodoxy).activate(0)
		
		for i in [1, 2]:
			team(i).meet(0, False)
			player(i).AI_setAttitudeExtra(0, 100)
		
		player(2).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 2")
		finally:
			for i in [1, 2]:
				team(i).cutContact(0)
				player(i).AI_setAttitudeExtra(0, 0)
		
			player(2).setLastStateReligion(-1)
	
	def testAttitudeProgress(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_PLEASED, 2).activate(0)
		
		self.assertEqual(goal.progress(), [[u"%c Pleased or better relations: 0 / 2" % self.FAILURE_CHAR]])
	
	def testAttitudeProgressCivs(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_PLEASED, 2).civs(group(iCivGroupEurope).named("AREA_NAME_EUROPE")).activate(0)
		
		self.assertEqual(goal.progress(), [[u"%c Pleased or better relations with civilizations in Europe: 0 / 2" % self.FAILURE_CHAR]])
	
	def testAttitudeProgressCommunist(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_PLEASED, 2).communist().activate(0)
		
		self.assertEqual(goal.progress(), [[u"%c Pleased or better relations with communist civilizations: 0 / 2" % self.FAILURE_CHAR]])
	
	def testAttitudeProgressStateReligion(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_PLEASED, 2).religion(iOrthodoxy).activate(0)
		
		self.assertEqual(goal.progress(), [[u"%c Pleased or better relations with Orthodox civilizations: 0 / 2" % self.FAILURE_CHAR]])
	
	def testAttitudeProgressIndependent(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_PLEASED, 2).independent().activate(0)
		
		self.assertEqual(goal.progress(), [[u"%c Pleased or better relations with independent civilizations: 0 / 2" % self.FAILURE_CHAR]])

	def testAttitudeProgressMinority(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_PLEASED, 2).minority(iOrthodoxy).activate(0)
		
		self.assertEqual(goal.progress(), [[u"%c Pleased or better relations with civilizations with a Orthodox minority: 0 / 2" % self.FAILURE_CHAR]])

	def testAttitudeProgressChained(self):
		goal = Count.attitude(AttitudeTypes.ATTITUDE_PLEASED, 2).civs(group(iCivGroupEurope).named("AREA_NAME_EUROPE")).communist().religion(iOrthodoxy).minority(iCatholicism).independent().activate(0)
		
		self.assertEqual(goal.progress(), [[u"%c Pleased or better relations with independent Orthodox communist civilizations with a Catholic minority in Europe: 0 / 2" % self.FAILURE_CHAR]])
	
	def testVassals(self):
		goal = Count.vassals(2).activate(0)
		
		for i in [1, 2]:
			team(i).setVassal(0, True, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "2 / 2")
			self.assertEqual(goal.state, SUCCESS)
		finally:
			for i in [1, 2]:
				team(i).setVassal(0, False, False)
	
	def testVassalsCivs(self):
		goal = Count.vassals(2).civs([iBabylonia]).activate(0)
		
		for i in [iBabylonia, iHarappa]:
			team(i).setVassal(0, True, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			for i in [iBabylonia, iHarappa]:
				team(i).setVassal(0, False, False)
	
	def testVassalsReligion(self):
		goal = Count.vassals(2).religion(iOrthodoxy).activate(0)
		
		for i in [1, 2]:
			team(i).setVassal(0, True, False)
		
		player(1).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			for i in [1, 2]:
				team(i).setVassal(0, False, False)
		
			player(1).setLastStateReligion(-1)
	
	def testVassalsProgress(self):
		goal = Count.vassals(2).activate(0)
		
		self.assertEqual(goal.progress(), [[u"%c Vassals: 0 / 2" % self.FAILURE_CHAR]])
	
	def testVassalsProgressCivs(self):
		goal = Count.vassals(2).civs(group(iCivGroupEurope).named("AREA_NAME_EUROPE")).activate(0)
		
		self.assertEqual(goal.progress(), [[u"%c Vassals in Europe: 0 / 2" % self.FAILURE_CHAR]])
	
	def testVassalsProgressStateReligion(self):
		goal = Count.vassals(2).religion(iOrthodoxy).activate(0)
		
		self.assertEqual(goal.progress(), [[u"%c Orthodox vassals: 0 / 2" % self.FAILURE_CHAR]])
	
	def testVassalsProgressChained(self):
		goal = Count.vassals(2).civs(group(iCivGroupEurope).named("AREA_NAME_EUROPE")).religion(iOrthodoxy).activate(0)
		
		self.assertEqual(goal.progress(), [[u"%c Orthodox vassals in Europe: 0 / 2" % self.FAILURE_CHAR]])
	
	def testCityBuildingNoCity(self):
		goal = Count.cityBuilding(city(61, 31), iGranary).activate(0)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 1")
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			goal.deactivate()
	
	def testCityBuildingNoBuilding(self):
		goal = Count.cityBuilding(city(61, 31), iGranary).activate(0)
		
		_city = player(0).initCity(61, 31)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 1")
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			_city.kill()
		
			goal.deactivate()
	
	def testCityBuildingWithBuilding(self):
		goal = Count.cityBuilding(city(61, 31), iGranary).activate(0)
		
		_city = player(0).initCity(61, 31)
		_city.setHasRealBuilding(iGranary, True)
		
		events.fireEvent("buildingBuilt", _city, iGranary)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1 / 1")
			self.assertEqual(goal.state, SUCCESS)
		finally:
			_city.kill()
		
			goal.deactivate()
		
	def testCityBuildingDifferentCity(self):
		goal = Count.cityBuilding(city(61, 31), iGranary).activate(0)
		
		_city = player(0).initCity(63, 31)
		_city.setHasRealBuilding(iGranary, True)
		
		events.fireEvent("buildingBuilt", _city, iGranary)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 1")
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			_city.kill()
		
			goal.deactivate()
	
	def testCityMultipleBuildingsSome(self):
		goal = Count.cityBuilding(city(61, 31), iGranary, iBarracks, iLibrary).activate(0)
		
		_city = player(0).initCity(61, 31)
		for iBuilding in [iGranary, iBarracks]:
			_city.setHasRealBuilding(iBuilding, True)
			events.fireEvent("buildingBuilt", _city, iBuilding)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 1\n1 / 1\n0 / 1")
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			_city.kill()
		
			goal.deactivate()
	
	def testCityMultipleBuildingsAll(self):
		goal = Count.cityBuilding(city(61, 31), iGranary, iBarracks, iLibrary).activate(0)
		
		_city = player(0).initCity(61, 31)
		for iBuilding in [iGranary, iBarracks, iLibrary]:
			_city.setHasRealBuilding(iBuilding, True)
			events.fireEvent("buildingBuilt", _city, iBuilding)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1 / 1\n1 / 1\n1 / 1")
			self.assertEqual(goal.state, SUCCESS)
		finally:
			_city.kill()
		
			goal.deactivate()
	
	def testCityMultipleBuildingsDifferentCities(self):
		goal = Count.cityBuilding(city(61, 31), iGranary, iBarracks, iLibrary).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		city1.setHasRealBuilding(iGranary, True)
		city1.setHasRealBuilding(iBarracks, True)
		city2.setHasRealBuilding(iLibrary, True)
		
		events.fireEvent("buildingBuilt", city1, iGranary)
		events.fireEvent("buildingBuilt", city1, iBarracks)
		events.fireEvent("buildingBuilt", city2, iLibrary)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 1\n1 / 1\n0 / 1")
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			city1.kill()
			city2.kill()
		
			goal.deactivate()
	
	def testCityBuildingSum(self):
		goal = Count.cityBuilding(city(61, 31), sum([iGranary, iBarracks, iLibrary]), 2).activate(0)
		
		city_ = player(0).initCity(61, 31)
		
		city_.setHasRealBuilding(iGranary, True)
		city_.setHasRealBuilding(iLibrary, True)
		
		events.fireEvent("buildingBuilt", city_, iGranary)
		events.fireEvent("buildingBuilt", city_, iLibrary)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "2 / 2")
			self.assertEqual(goal.state, SUCCESS)
		finally:
			city_.kill()
		
			goal.deactivate()
	
	def testCityBuildingCapital(self):
		goal = Count.cityBuilding(capital(), iGranary).activate(1)
		
		city0 = player(0).initCity(61, 31)
		city0.setHasRealBuilding(iPalace, True)
		
		city1 = player(1).initCity(63, 31)
		city1.setHasRealBuilding(iPalace, True)
		city1.setHasRealBuilding(iGranary, True)
		
		try:
			self.assertEqual(str(goal), "1 / 1")
			self.assertEqual(bool(goal), True)
		finally:
			city0.kill()
			city1.kill()
		
			goal.deactivate()
	
	def testCityBuildingProgress(self):
		goal = Count.cityBuilding(city(61, 31), iGranary).activate(0)
		
		_city = player(0).initCity(61, 31)
		_city.setName("First", False)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Granary in First" % self.FAILURE_CHAR]])
		finally:
			_city.kill()
	
	def testCityBuildingProgressDifferentOwner(self):
		goal = Count.cityBuilding(city(61, 31), iGranary).activate(0)
		
		_city = player(1).initCity(61, 31)
		_city.setName("First", False)
		
		try:
			self.assertEqual(goal.progress(), [[u"%c Granary in First (controlled by Babylonia)" % self.FAILURE_CHAR]])
		finally:
			_city.kill()
	
	def testCityBuildingProgressNoCity(self):
		goal = Count.cityBuilding(city(61, 31), iGranary).activate(0)
		
		self.assertEqual(goal.progress(), [[u"%c (No City)" % self.FAILURE_CHAR]])
	
	def testDifferentSpecialist(self):
		goal = Count.differentSpecialist(city(61, 31), 2).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setFreeSpecialistCount(iSpecialistGreatArtist, 1)
		city1.setFreeSpecialistCount(iSpecialistGreatScientist, 2)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "2 / 2")
			self.assertEqual(goal.progress(), [[u"%c Different specialists in First: 2 / 2" % self.SUCCESS_CHAR]])
		finally:
			city1.kill()
			goal.deactivate()
	
	def testDifferentSpecialistDifferentOwner(self):
		goal = Count.differentSpecialist(city(61, 31), 2).activate(0)
		
		city1 = player(1).initCity(61, 31)
		city1.setName("First", False)
		city1.setFreeSpecialistCount(iSpecialistGreatArtist, 1)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 2")
			self.assertEqual(goal.progress(), [[u"%c Different specialists in First (controlled by Babylonia): 0 / 2" % self.FAILURE_CHAR]])
		finally:
			city1.kill()
			goal.deactivate()
	
	def testDifferentSpecialistNoCity(self):
		goal = Count.differentSpecialist(city(61, 31), 2).activate(0)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 2")
			self.assertEqual(goal.progress(), [[u"%c (No City)" % self.FAILURE_CHAR]])
		finally:
			goal.deactivate()
	
	def testShrineIncome(self):
		goal = Count.shrineIncome(iOrthodoxy, 2).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setHasReligion(iOrthodoxy, True, False, False)
		
		city2 = player(1).initCity(63, 31)
		city2.setHasReligion(iOrthodoxy, True, False, False)
		
		city1.setHasRealBuilding(iOrthodoxShrine, True)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "2 / 2")
		finally:
			city1.kill()
			city2.kill()
			goal.deactivate()
	
	def testShrineIncomeNoShrine(self):
		goal = Count.shrineIncome(iOrthodoxy, 2).activate(0)
		
		city = player(0).initCity(61, 31)
		city.setHasReligion(iOrthodoxy, True, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 2")
		finally:
			city.kill()
			goal.deactivate()
	
	def testShrineIncomeOtherOwner(self):
		goal = Count.shrineIncome(iOrthodoxy, 2).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setHasReligion(iOrthodoxy, True, False, False)
		
		city2 = player(1).initCity(63, 31)
		city2.setHasReligion(iOrthodoxy, True, False, False)
		
		city2.setHasRealBuilding(iOrthodoxShrine, True)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 2")
		finally:
			city1.kill()
			city2.kill()
			goal.deactivate()
	
	def testUnitLevelCount(self):
		goal = Count.unitLevel(3, 2).activate(0)
		
		units = makeUnits(0, iSwordsman, (0, 0), 3)
		
		for unit in units:
			unit.setLevel(3)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "3 / 2")
		finally:
			for unit in units:
				unit.kill(False, -1)
	
	def testTerrainCount(self):
		goal = Count.terrain(iOcean, 50).activate(0)
		
		controlled = plots.all().where(lambda plot: plot.getTerrainType() == iOcean).limit(60) + plots.all().land().limit(40)
		for plot in controlled:
			plot.setOwner(0)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "60 / 50")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
	
	def testPeakCount(self):
		goal = Count.peaks(20).activate(0)
		
		controlled = plots.all().where(lambda plot: plot.isPeak()).limit(25) + plots.all().water().limit(25)
		for plot in controlled:
			plot.setOwner(0)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "25 / 20")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
	
	def testFeatureCount(self):
		goal = Count.feature(iForest, 20).activate(0)
		
		controlled = plots.all().where(lambda plot: plot.getFeatureType() == iForest).limit(25) + plots.all().water().limit(25)
		for plot in controlled:
			plot.setOwner(0)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "25 / 20")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
	
	def testAcquiredCitiesAcquired(self):
		goal = Count.acquiredCities(1).activate(0)
		
		city = player(1).initCity(61, 31)
		
		events.fireEvent("cityAcquired", 1, 0, city, True, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1 / 1")
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testAcquiredCitiesBuilt(self):
		goal = Count.acquiredCities(1).activate(0)
		
		city = player(0).initCity(61, 31)
		
		events.fireEvent("cityBuilt", city)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1 / 1")
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testAcquiredCitiesTwice(self):
		goal = Count.acquiredCities(2).activate(0)
		
		city = player(1).initCity(61, 31)
		
		events.fireEvent("cityAcquired", 1, 0, city, True, False)
		events.fireEvent("cityAcquired", 1, 0, city, True, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
		finally:
			city.kill()
			goal.deactivate()
	

class TestPercentageGoals(ExtendedTestCase):

	def testAreaControl(self):
		area = plots.rectangle((50, 30), (69, 31))
		goal = Percentage.areaControl(area, 30).activate(0)
		
		controlled = plots.rectangle((50, 30), (69, 30))
		for plot in controlled:
			plot.setOwner(0)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "50.00% / 30%")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
		
			goal.deactivate()
	
	def testAreaControlInsufficient(self):
		area = plots.rectangle((50, 30), (69, 31))
		goal = Percentage.areaControl(area, 30).activate(0)
		
		controlled = plots.rectangle((50, 30), (50, 30))
		for plot in controlled:
			plot.setOwner(0)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "2.50% / 30%")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
		
			goal.deactivate()
			
	def testWorldControl(self):
		goal = Percentage.worldControl(10).activate(0)
		
		controlled = plots.all().land().limit(11 * 32)
		for plot in controlled:
			plot.setOwner(0)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "10.89% / 10%")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
		
			goal.deactivate()
	
	def testWorldControlInsufficient(self):
		goal = Percentage.worldControl(10).activate(0)
		
		controlled = plots.all().land().limit(32)
		for plot in controlled:
			plot.setOwner(0)
	
		try:
			self.assertEqual(map.getLandPlots(), 3232)
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0.99% / 10%")
		finally:
			for plot in controlled:
				plot.setOwner(-1)
		
			goal.deactivate()
	
	def testWorldControlReligion(self):
		goal = Percentage.worldControl(10).religion().activate(0)
		
		controlled = plots.all().land().limit(11 * 32)
		controlled0, controlled1 = controlled.percentage_split(50)
		
		for plot in controlled0:
			plot.setOwner(0)
		
		for plot in controlled1:
			plot.setOwner(1)
			
		player(0).setLastStateReligion(iBuddhism)
		player(1).setLastStateReligion(iBuddhism)
		
		try:
			self.assertEqual(map.getLandPlots(), 3232)
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "10.89% / 10%")
		finally:
			for plot in controlled0:
				plot.setOwner(-1)
			for plot in controlled1:
				plot.setOwner(-1)
			
			goal.deactivate()
	
	def testReligionSpread(self):
		goal = Percentage.religionSpread(iOrthodoxy, 30).activate(1)
		
		city1 = player(1).initCity(30, 30)
		city2 = player(2).initCity(32, 30)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		player(1).setLastStateReligion(iOrthodoxy)
		
		city1.setHasReligion(iOrthodoxy, True, False, False)
		
		try:
			self.assertEqual(str(goal), "50.00% / 30%")
			self.assertEqual(bool(goal), True)
		finally:
			city1.kill()
			city2.kill()
		
			player(1).setLastStateReligion(iOrthodoxy)
		
			goal.deactivate()
	
	def testReligionSpreadNoState(self):
		goal = Percentage.religionSpread(iOrthodoxy, 30).activate(1)
		
		city1 = player(1).initCity(30, 30)
		city2 = player(2).initCity(32, 30)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasReligion(iOrthodoxy, True, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "25.00% / 30%")
		finally:
			city1.kill()
			city2.kill()
		
			goal.deactivate()
	
	def testReligionSpreadMultipleReligions(self):
		goal = Percentage.religionSpread(iOrthodoxy, 30).activate(1)
		
		city1 = player(1).initCity(30, 30)
		city2 = player(2).initCity(32, 30)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasReligion(iOrthodoxy, True, False, False)
		city1.setHasReligion(iCatholicism, True, False, False)
		
		player(1).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "35.00% / 30%")
		finally:
			city1.kill()
			city2.kill()
		
			player(1).setLastStateReligion(-1)
		
			goal.deactivate()
	
	def testReligionSpreadNotOwned(self):
		goal = Percentage.religionSpread(iOrthodoxy, 30).activate(1)
		
		city1 = player(2).initCity(30, 30)
		city2 = player(3).initCity(32, 30)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasReligion(iOrthodoxy, True, False, False)
		
		player(2).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "50.00% / 30%")
		finally:
			city1.kill()
			city2.kill()
		
			player(2).setLastStateReligion(-1)
		
			goal.deactivate()
	
	def testPopulation(self):
		goal = Percentage.population(30).activate(0)
		
		city1 = player(0).initCity(30, 30)
		city2 = player(1).initCity(32, 30)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "50.00% / 30%")
		finally:
			city1.kill()
			city2.kill()
		
			goal.deactivate()
	
	def testPopulationInsufficient(self):
		goal = Percentage.population(30).activate(0)
		
		city1 = player(0).initCity(30, 30)
		city2 = player(1).initCity(32, 30)
		
		city1.setPopulation(5)
		city2.setPopulation(20)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "20.00% / 30%")
		finally:
			city1.kill()
			city2.kill()
		
			goal.deactivate()
	
	def testPopulationIncludeVassals(self):
		goal = Percentage.population(50).vassal().activate(0)
		
		city1 = player(0).initCity(30, 30)
		city2 = player(1).initCity(32, 30)
		city3 = player(2).initCity(34, 30)
		
		city1.setPopulation(5)
		city2.setPopulation(5)
		city3.setPopulation(10)
		
		team(1).setVassal(team(0).getID(), True, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "50.00% / 50%")
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
		
			team(1).setVassal(team(0).getID(), False, False)
		
			goal.deactivate()
	
	def testAreaPopulation(self):
		area = plots.rectangle((30, 30), (35, 35))
		goal = Percentage.areaPopulation(area, 50).activate(0)
		
		city1 = player(0).initCity(30, 30)
		city2 = player(1).initCity(32, 32)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "50.00% / 50%")
		finally:
			city1.kill()
			city2.kill()
			
			goal.deactivate()
	
	def testAreaPopulationOutside(self):
		area = plots.rectangle((30, 30), (32, 32))
		goal = Percentage.areaPopulation(area, 50).activate(0)
		
		city1 = player(0).initCity(30, 30)
		city2 = player(1).initCity(32, 32)
		city3 = player(0).initCity(34, 30)
		city4 = player(1).initCity(36, 32)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		city3.setPopulation(10)
		city4.setPopulation(30)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "50.00% / 50%")
		finally:
			for city in [city1, city2, city3, city4]:
				city.kill()
			goal.deactivate()
	
	def testReligiousVote(self):
		goal = Percentage.religiousVote(30).activate(1)
		
		city1 = player(1).initCity(30, 30)
		city2 = player(2).initCity(32, 30)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasRealBuilding(iCatholicShrine, True)
		
		city1.setHasReligion(iCatholicism, True, False, False)
		city2.setHasReligion(iCatholicism, True, False, False)
		
		player(1).setLastStateReligion(iCatholicism)
		player(2).setLastStateReligion(iCatholicism)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "50.00% / 30%")
		finally:
			city1.kill()
			city2.kill()
		
			player(1).setLastStateReligion(-1)
			player(2).setLastStateReligion(-1)
		
			goal.deactivate()
	
	def testReligiousVoteNotStateReligion(self):
		goal = Percentage.religiousVote(30).activate(1)
		
		city1 = player(1).initCity(30, 30)
		city2 = player(2).initCity(32, 30)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasRealBuilding(iCatholicShrine, True)
		
		city1.setHasReligion(iCatholicism, True, False, False)
		city2.setHasReligion(iCatholicism, True, False, False)
		
		player(2).setLastStateReligion(iCatholicism)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0.00% / 30%")
		finally:
			city1.kill()
			city2.kill()
		
			player(2).setLastStateReligion(-1)
		
			goal.deactivate()
		
	def testReligiousVoteNoReligion(self):
		goal = Percentage.religiousVote(30).activate(1)
		
		city1 = player(1).initCity(30, 30)
		city2 = player(2).initCity(32, 30)
		
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city1.setHasRealBuilding(iCatholicShrine, True)
		
		city2.setHasReligion(iCatholicism, True, False, False)
		
		player(1).setLastStateReligion(iCatholicism)
		player(2).setLastStateReligion(iCatholicism)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0.00% / 30%")
		finally:
			city1.kill()
			city2.kill()
		
			player(0).setLastStateReligion(-1)
			player(1).setLastStateReligion(-1)
		
			goal.deactivate()
	
	def testAlliedPower(self):
		goal = Percentage.alliedPower(30).activate(0)
		
		unit = makeUnit(0, iMilitia, (0, 0))
		
		try:
			self.assertEqual(str(goal), "50.00% / 30%")
			self.assertEqual(bool(goal), True)
		finally:
			unit.kill(False, -1)
		
			goal.deactivate()
	
	def testAlliedPowerWithVassal(self):
		goal = Percentage.alliedPower(30).activate(0)
		
		unit = makeUnit(0, iMilitia, (0, 0))
		
		team(1).setVassal(team(0).getID(), True, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "75.00% / 30%")
		finally:
			unit.kill(False, -1)
		
			team(1).setVassal(team(0).getID(), False, False)
		
			goal.deactivate()
	
	def testAlliedPowerWithDefensivePact(self):
		goal = Percentage.alliedPower(30).activate(0)
		
		unit = makeUnit(0, iMilitia, (0, 0))
		
		team(0).setDefensivePact(team(1).getID(), True)
		team(1).setDefensivePact(team(0).getID(), True)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "75.00% / 30%")
		finally:
			unit.kill(False, -1)
		
			team(1).setDefensivePact(team(0).getID(), False)
			team(0).setDefensivePact(team(1).getID(), False)
		
			goal.deactivate()
	
	def testAlliedPowerWithDefensivePactVassal(self):
		goal = Percentage.alliedPower(30).activate(0)
		
		unit = makeUnit(0, iMilitia, (0, 0))
		
		team(2).setVassal(team(1).getID(), True, False)
		team(0).setDefensivePact(team(1).getID(), True)
		team(1).setDefensivePact(team(0).getID(), True)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "100.00% / 30%")
		finally:
			unit.kill(False, -1)
		
			team(2).setVassal(team(1).getID(), False, False)
			team(0).setDefensivePact(team(1).getID(), False)
			team(1).setDefensivePact(team(0).getID(), False)
		
			goal.deactivate()
	
	def testAlliedCommerce(self):
		goal = Percentage.alliedCommerce(30).activate(0)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "33.33% / 30%")
		finally:
			goal.deactivate()


class TestTriggerGoals(ExtendedTestCase):

	def testFirstDiscover(self):
		goal = Trigger.firstDiscover(iLaw).activate(0)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			team(0).setHasTech(iLaw, False, 0, True, False)
		
			goal.deactivate()
	
	def testFirstDiscoverOther(self):
		goal = Trigger.firstDiscover(iLaw).activate(0)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.state, FAILURE)
		finally:
			team(1).setHasTech(iLaw, False, 1, True, False)
		
			goal.deactivate()
	
	def testFirstDiscoverAfterOther(self):
		goal = Trigger.firstDiscover(iLaw).activate(0)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		team(0).setHasTech(iLaw, True, 0, True, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.state, FAILURE)
		finally:
			team(1).setHasTech(iLaw, False, 1, True, False)
			team(0).setHasTech(iLaw, False, 0, True, False)
		
			goal.deactivate()
	
	def testFirstDiscoverNone(self):
		goal = Trigger.firstDiscover(iLaw, iCurrency, iPhilosophy).activate(0)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			goal.deactivate()
	
	def testFirstDiscoverSome(self):
		goal = Trigger.firstDiscover(iLaw, iCurrency, iPhilosophy).activate(0)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		team(0).setHasTech(iCurrency, True, 0, True, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			team(0).setHasTech(iLaw, False, 0, True, False)
			team(0).setHasTech(iCurrency, False, 0, True, False)
		
			goal.deactivate()
	
	def testFirstDiscoverAll(self):
		goal = Trigger.firstDiscover(iLaw, iCurrency, iPhilosophy).activate(0)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		team(0).setHasTech(iCurrency, True, 0, True, False)
		team(0).setHasTech(iPhilosophy, True, 0, True, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			team(0).setHasTech(iLaw, False, 0, True, False)
			team(0).setHasTech(iCurrency, False, 0, True, False)
			team(0).setHasTech(iPhilosophy, False, 0, True, False)
		
			goal.deactivate()
	
	def testFirstDiscoverExpireAny(self):
		goal = Trigger.firstDiscover(iLaw, iCurrency, iPhilosophy).activate(0)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.state, FAILURE)
		finally:
			team(1).setHasTech(iLaw, False, 1, True, False)
		
			goal.deactivate()
	
	def testFirstDiscoverNotExpireIfAlreadyDiscovered(self):
		goal = Trigger.firstDiscover(iLaw, iCurrency, iPhilosophy).activate(0)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		team(1).setHasTech(iLaw, True, 0, True, False)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			team(0).setHasTech(iLaw, False, 0, True, False)
			team(1).setHasTech(iLaw, False, 1, True, False)
			
			goal.deactivate()
	
	def testFirstSettle(self):
		area = plots.rectangle((50, 28), (55, 30))
		goal = Trigger.firstSettle(area).activate(0)
		
		player(0).found(51, 29)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city_(51, 29).kill()
		
			goal.deactivate()
	
	def testFirstSettleOther(self):
		area = plots.rectangle((50, 28), (55, 30))
		goal = Trigger.firstSettle(area).activate(0)
		
		player(1).found(51, 29)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city_(51, 29).kill()
		
			goal.deactivate()
	
	def testFirstSettleAfterOther(self):
		area = plots.rectangle((50, 28), (55, 30))
		goal = Trigger.firstSettle(area).activate(0)
		
		player(1).found(51, 29)
		player(0).found(53, 29)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city_(51, 29).kill()
			city_(53, 29).kill()
		
			goal.deactivate()
	
	def testFirstSettleOutside(self):
		area = plots.rectangle((50, 28), (55, 30))
		goal = Trigger.firstSettle(area).activate(0)
		
		player(0).found(56, 29)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city_(56, 29).kill()
		
			goal.deactivate()
		
	def testFirstSettleAfterOtherOutside(self):
		area = plots.rectangle((50, 28), (55, 30))
		goal = Trigger.firstSettle(area).activate(0)
		
		player(1).found(57, 29)
		player(0).found(51, 29)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city_(57, 29).kill()
			city_(51, 29).kill()
		
			goal.deactivate()
	
	def testFirstSettleAfterAllowed(self):
		area = plots.rectangle((50, 28), (55, 30))
		goal = Trigger.firstSettle(area).allowed([iMaya]).activate(0)
		
		player(iMaya).found(51, 29)
		player(0).found(53, 29)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city_(51, 29).kill()
			city_(53, 29).kill()
		
			goal.deactivate()
		
	def testFirstSettleConquest(self):
		area = plots.rectangle((50, 28), (55, 30))
		goal = Trigger.firstSettle(area).allowed([iMaya]).activate(0)
		
		player(iMaya).found(51, 29)
		player(0).acquireCity(city_(51, 29), True, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city_(51, 29).kill()
		
			goal.deactivate()
	
	def testFirstSettleAfterConquest(self):
		area = plots.rectangle((50, 28), (55, 30))
		goal = Trigger.firstSettle(area).allowed([iMaya]).activate(0)
		
		player(iMaya).found(51, 29)
		player(1).acquireCity(city_(51, 29), True, False)
		player(0).found(53, 29)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city_(51, 29).kill()
			city_(53, 29).kill()
		
			goal.deactivate()
	
	def testDiscover(self):
		goal = Trigger.discover(iLaw).activate(0)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			team(0).setHasTech(iLaw, False, 0, True, False)
		
			goal.deactivate()
	
	def testDiscoverOther(self):
		goal = Trigger.discover(iLaw).activate(0)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			team(1).setHasTech(iLaw, False, 1, True, False)
		
			goal.deactivate()
	
	def testDiscoverAfterOther(self):
		goal = Trigger.discover(iLaw).activate(0)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		team(0).setHasTech(iLaw, True, 0, True, False)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			team(1).setHasTech(iLaw, False, 1, True, False)
			team(0).setHasTech(iLaw, False, 0, True, False)
		
			goal.deactivate()
	
	def testDiscoverSome(self):
		goal = Trigger.discover(iLaw, iCurrency, iPhilosophy).activate(0)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		team(0).setHasTech(iCurrency, True, 0, True, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			team(0).setHasTech(iLaw, False, 0, True, False)
			team(0).setHasTech(iCurrency, False, 0, True, False)
		
			goal.deactivate()
	
	def testDiscoverAll(self):
		goal = Trigger.discover(iLaw, iCurrency, iPhilosophy).activate(0)
		
		for iTech in [iLaw, iCurrency, iPhilosophy]:
			team(0).setHasTech(iTech, True, 0, True, False)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			for iTech in [iLaw, iCurrency, iPhilosophy]:
				team(0).setHasTech(iTech, False, 0, True, False)
		
			goal.deactivate()
		
	def testFirstContact(self):
		goal = Trigger.firstContact(plots.rectangle((20, 20), (30, 30)), [iChina]).activate(0)
		
		events.fireEvent("firstContact", team(iEgypt).getID(), team(iChina).getID())
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			goal.deactivate()
	
	def testFirstContactWithOther(self):
		goal = Trigger.firstContact(plots.rectangle((20, 20), (30, 30)), [iChina]).activate(0)
		
		events.fireEvent("firstContact", team(iEgypt).getID(), team(iGreece).getID())
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			goal.deactivate()
	
	def testFirstContactAfterRevealed(self):
		goal = Trigger.firstContact(plots.rectangle((20, 20), (30, 30)), [iChina]).activate(0)
		
		plot(25, 25).setRevealed(team(iChina).getID(), True, False, team(iChina).getID())
		
		events.fireEvent("firstContact", team(iEgypt).getID(), team(iChina).getID())
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.state, FAILURE)
		finally:
			plot(25, 25).setRevealed(team(iChina).getID(), False, False, team(iChina).getID())
		
			goal.deactivate()
	
	def testFirstContactSome(self):
		goal = Trigger.firstContact(plots.rectangle((20, 20), (30, 30)), [iChina, iGreece, iIndia]).activate(0)
		
		events.fireEvent("firstContact", team(iEgypt).getID(), team(iChina).getID())
		events.fireEvent("firstContact", team(iEgypt).getID(), team(iGreece).getID())
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			goal.deactivate()
	
	def testFirstContactAll(self):
		goal = Trigger.firstContact(plots.rectangle((20, 20), (30, 30)), [iChina, iGreece, iIndia]).activate(0)
		
		for iCiv in [iChina, iGreece, iIndia]:
			events.fireEvent("firstContact", team(iEgypt).getID(), team(iCiv).getID())
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			goal.deactivate()
	
	def testNoCityLost(self):
		goal = Trigger.noCityLost().activate(0)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			goal.deactivate()
	
	def testNoCityLostAfterLosing(self):
		goal = Trigger.noCityLost().activate(0)
		
		city = player(1).initCity(25, 25)
		events.fireEvent("cityAcquired", 0, 1, city, True, False)
		
		try:
			self.assertEqual(goal.state, FAILURE)
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testTradeMission(self):
		goal = Trigger.tradeMission(city(25, 25)).activate(0)
		
		city_ = player(1).initCity(25, 25)
		events.fireEvent("tradeMission", iGreatMerchant, 0, 25, 25, 1000)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city_.kill()
		
			goal.deactivate()
		
	def testTradeMissionOther(self):
		goal = Trigger.tradeMission(city(25, 25)).activate(0)
		
		city_ = player(1).initCity(25, 25)
		events.fireEvent("tradeMission", iGreatMerchant, 2, 25, 25, 1000)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city_.kill()
		
			goal.deactivate()
	
	def testTradeMissionElsewhere(self):
		goal = Trigger.tradeMission(city(25, 25)).activate(0)
		
		city_ = player(1).initCity(30, 25)
		events.fireEvent("tradeMission", iGreatMerchant, 0, 30, 25, 1000)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city_.kill()
		
			goal.deactivate()
	
	def testTradeMissionHolyCityWithout(self):
		goal = Trigger.tradeMission(holyCity()).activate(0)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		city = player(1).initCity(30, 25)
		events.fireEvent("tradeMission", iGreatMerchant, 0, 30, 25, 1000)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			player(0).setLastStateReligion(-1)
			city.kill()
		
			goal.deactivate()
	
	def testTradeMissionHolyCity(self):
		goal = Trigger.tradeMission(holyCity()).activate(0)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		city = player(1).initCity(30, 25)
		game.setHolyCity(iOrthodoxy, city, False)
		events.fireEvent("tradeMission", iGreatMerchant, 0, 30, 25, 1000)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			player(0).setLastStateReligion(iOrthodoxy)
			city.kill()
		
			goal.deactivate()
	
	def testTradeMissionHolyCityNoStateReligion(self):
		goal = Trigger.tradeMission(holyCity()).activate(0)
		
		city = player(1).initCity(30, 25)
		game.setHolyCity(iOrthodoxy, city, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testNeverConquer(self):
		goal = Trigger.neverConquer().activate(0)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			goal.deactivate()
	
	def testNeverConquerConquered(self):
		goal = Trigger.neverConquer().activate(0)
		
		city = player(1).initCity(30, 25)
		player(0).acquireCity(city, True, False)
		
		try:
			self.assertEqual(goal.state, FAILURE)
		finally:
			city_(30, 25).kill()
		
			goal.deactivate()
	
	def testNeverConquerTraded(self):
		goal = Trigger.neverConquer().activate(0)
		
		city = player(1).initCity(30, 25)
		player(0).acquireCity(city, False, True)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city_(30, 25).kill()
		
			goal.deactivate()
	
	def testNeverConquerConqueredOther(self):
		goal = Trigger.neverConquer().activate(0)
		
		city = player(1).initCity(30, 25)
		player(2).acquireCity(city, True, False)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			city_(30, 25).kill()
		
			goal.deactivate()
	
	def testConvertAfterFounding(self):
		goal = Trigger.convertAfterFounding(5, iOrthodoxy).activate(0)
		
		game.setReligionGameTurnFounded(iOrthodoxy, 1)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			player(0).setLastStateReligion(-1)
			game.setReligionGameTurnFounded(iOrthodoxy, -1)
		
			goal.deactivate()
	
	def testConvertAfterFoundingNotFounded(self):
		goal = Trigger.convertAfterFounding(5, iOrthodoxy).activate(0)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			player(0).setLastStateReligion(-1)
		
			goal.deactivate()
	
	def testConvertAfterFoundingOtherReligion(self):
		goal = Trigger.convertAfterFounding(5, iOrthodoxy).activate(0)
		
		game.setReligionGameTurnFounded(iOrthodoxy, 1)
		game.setReligionGameTurnFounded(iCatholicism, 2)
		
		player(0).setLastStateReligion(iCatholicism)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			player(0).setLastStateReligion(-1)
		
			game.setReligionGameTurnFounded(iOrthodoxy, -1)
			game.setReligionGameTurnFounded(iCatholicism, -1)
		
			goal.deactivate()
	
	def testConvertAfterFoundingSoonEnough(self):
		goal = Trigger.convertAfterFounding(5, iOrthodoxy).activate(0)
		
		game.setReligionGameTurnFounded(iOrthodoxy, turn()-2)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			player(0).setLastStateReligion(-1)
			game.setReligionGameTurnFounded(iOrthodoxy, -1)
		
			goal.deactivate()
	
	def testConvertAfterFoundingTooLate(self):
		goal = Trigger.convertAfterFounding(5, iOrthodoxy).activate(0)
		
		game.setReligionGameTurnFounded(iOrthodoxy, turn()-10)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			player(0).setLastStateReligion(-1)
			game.setReligionGameTurnFounded(iOrthodoxy, -1)
		
			goal.deactivate()
	
	def testConvertAfterFoundingSome(self):
		goal = Trigger.convertAfterFounding(5, iOrthodoxy, iCatholicism).activate(0)
		
		game.setReligionGameTurnFounded(iOrthodoxy, 1)
		game.setReligionGameTurnFounded(iCatholicism, 2)
		
		player(0).setLastStateReligion(iOrthodoxy)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.completed(5, iOrthodoxy), True)
			self.assertEqual(goal.completed(5, iCatholicism), False)
		finally:
			player(0).setLastStateReligion(-1)
			game.setReligionGameTurnFounded(iOrthodoxy, -1)
			game.setReligionGameTurnFounded(iCatholicism, -1)
		
			goal.deactivate()
	
	def testConvertAfterFoundingAll(self):
		goal = Trigger.convertAfterFounding(5, iOrthodoxy, iCatholicism).activate(0)
		
		game.setReligionGameTurnFounded(iOrthodoxy, 1)
		game.setReligionGameTurnFounded(iCatholicism, 2)
		
		player(0).setLastStateReligion(iOrthodoxy)
		player(0).setLastStateReligion(iCatholicism)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			player(0).setLastStateReligion(-1)
		
			game.setReligionGameTurnFounded(iOrthodoxy, -1)
			game.setReligionGameTurnFounded(iCatholicism, -1)
		
			goal.deactivate()
	
	def testEnterEra(self):
		goal = Trigger.enterEra(iClassical).activate(0)
		
		events.fireEvent("techAcquired", iLaw, 0, 0, False)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			goal.deactivate()
	
	def testEnterEraOther(self):
		goal = Trigger.enterEra(iClassical).activate(0)
		
		events.fireEvent("techAcquired", iLeverage, 0, 0, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			goal.deactivate()
	
	def testEnterEraSome(self):
		goal = Trigger.enterEra(iClassical, iMedieval).activate(0)
		
		events.fireEvent("techAcquired", iLaw, 0, 0, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			goal.deactivate()
	
	def testEnterEraAll(self):
		goal = Trigger.enterEra(iClassical, iMedieval).activate(0)
		
		events.fireEvent("techAcquired", iLaw, 0, 0, False)
		events.fireEvent("techAcquired", iDoctrine, 0, 0, False)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			goal.deactivate()
	
	def testEnterEraExpire(self):
		goal = Trigger.enterEra(iClassical).before(iMedieval).activate(0)
		
		events.fireEvent("techAcquired", iDoctrine, 1, 1, False)
		
		try:
			self.assertEqual(goal.state, FAILURE)
		finally:
			goal.deactivate()
	
	def testFirstGreatPerson(self):
		goal = Trigger.firstGreatPerson(iSpecialistGreatArtist).activate(0)
		
		unit = makeUnit(0, iGreatArtist, (0, 0))
		
		events.fireEvent("greatPersonBorn", unit, 0, None)
		
		try:
			self.assertEqual(goal.state, SUCCESS)
		finally:
			unit.kill(False, -1)
			goal.deactivate()
	
	def testFirstGreatPersonAll(self):
		goal = Trigger.firstGreatPerson(iSpecialistGreatArtist, iSpecialistGreatMerchant, iSpecialistGreatScientist).activate(0)
		
		artist = makeUnit(0, iGreatArtist, (0, 0))
		merchant = makeUnit(0, iGreatMerchant, (0, 0))
		scientist = makeUnit(0, iGreatScientist, (0, 0))
		
		events.fireEvent("greatPersonBorn", artist, 0, None)
		events.fireEvent("greatPersonBorn", merchant, 0, None)
		events.fireEvent("greatPersonBorn", scientist, 0, None)
		
		try:
			self.assertEqual(goal.state, SUCCESS)
		finally:
			for unit in [artist, merchant, scientist]:
				unit.kill(False, -1)
			goal.deactivate()
	
	def testFirstGreatPersonSome(self):
		goal = Some(Trigger.firstGreatPerson(iSpecialistGreatArtist, iSpecialistGreatMerchant, iSpecialistGreatScientist), 2).activate(0)
		
		artist = makeUnit(0, iGreatArtist, (0, 0))
		merchant = makeUnit(0, iGreatMerchant, (0, 0))
		
		events.fireEvent("greatPersonBorn", artist, 0, None)
		events.fireEvent("greatPersonBorn", merchant, 0, None)
		
		try:
			self.assertEqual(goal.state, SUCCESS)
		finally:
			for unit in [artist, merchant]:
				unit.kill(False, -1)
			goal.deactivate()
	
	def testFirstGreatPersonOther(self):
		goal = Trigger.firstGreatPerson(iSpecialistGreatArtist).activate(0)
		
		artist = makeUnit(1, iGreatArtist, (0, 0))
		
		events.fireEvent("greatPersonBorn", artist, 1, None)
		
		try:
			self.assertEqual(goal.state, FAILURE)
		finally:
			artist.kill(False, -1)
			goal.deactivate()


class TestTrackGoals(ExtendedTestCase):

	def testGoldenAgesOutside(self):
		goal = Track.goldenAges(1).activate(0)
		
		events.fireEvent("BeginPlayerTurn", game.getGameTurn(), 0)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 8")
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			goal.deactivate()
	
	def testGoldenAgesDuring(self):
		goal = Track.goldenAges(1).activate(0)
		
		player(0).changeGoldenAgeTurns(8)
		
		events.fireEvent("BeginPlayerTurn", game.getGameTurn(), 0)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 8")
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			player(0).changeGoldenAgeTurns(-8)
		
			goal.deactivate()
		
	def testGoldenAgesAnarchy(self):
		goal = Track.goldenAges(1).activate(0)
		
		player(0).changeGoldenAgeTurns(8)
		player(0).changeAnarchyTurns(8)
		
		events.fireEvent("BeginPlayerTurn", game.getGameTurn(), 0)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 8")
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			player(0).changeGoldenAgeTurns(-8)
			player(0).changeAnarchyTurns(-8)
		
			goal.deactivate()
	
	def testGoldenAgesSuccess(self):
		goal = Track.goldenAges(1).activate(0)
		
		player(0).changeGoldenAgeTurns(8)
		
		for _ in range(8):
			events.fireEvent("BeginPlayerTurn", game.getGameTurn(), 0)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "8 / 8")
			self.assertEqual(goal.state, SUCCESS)
		finally:
			player(0).changeGoldenAgeTurns(-8)
		
			goal.deactivate()
	
	def testEraFirsts(self):
		goal = Track.eraFirsts(iClassical, 5).activate(0)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 5")
		finally:
			team(0).setHasTech(iLaw, False, 0, True, False)
		
			goal.deactivate()
	
	def testEraFirstsOther(self):
		goal = Track.eraFirsts(iClassical, 1).activate(0)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 1")
		finally:
			team(1).setHasTech(iLaw, False, 0, True, False)
			goal.deactivate()
	
	def testEraFirstsDifferentEra(self):
		goal = Track.eraFirsts(iClassical, 5).activate(0)
		
		team(0).setHasTech(iFeudalism, True, 0, True, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 5")
		finally:
			team(0).setHasTech(iFeudalism, False, 0, True, False)
		
			goal.deactivate()
	
	def testEraFirstsNotFirst(self):
		goal = Track.eraFirsts(iClassical, 5).activate(0)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		team(0).setHasTech(iLaw, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 5")
		finally:
			team(0).setHasTech(iLaw, False, 0, False, False)
			team(1).setHasTech(iLaw, False, 1, False, False)
		
			goal.deactivate()
	
	def testEraFirstsMultiple(self):
		goal = Track.eraFirsts((iClassical, 1), (iMedieval, 1)).activate(0)
		
		team(0).setHasTech(iFeudalism, True, 0, True, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), '\n'.join(["0 / 1", "1 / 1"]))
		finally:
			team(0).setHasTech(iFeudalism, False, 0, True, False)
		
			goal.deactivate()
	
	def testEraFirstsExpiresWhenNotEnoughTechs(self):
		goal = Track.eraFirsts(iClassical, 20).activate(0)
		
		team(1).setHasTech(iLaw, True, 1, True, False)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			
			team(1).setHasTech(iCurrency, True, 1, True, False)			
			self.assertEqual(goal.state, FAILURE)
		finally:
			for iTech in [iLaw, iCurrency]:
				team(1).setHasTech(iTech, False, 1, True, False)
			goal.deactivate()
	
	def testEraFirstExpiresWhenNotEnoughTechsWithOwn(self):
		goal = Track.eraFirsts(iClassical, 20).activate(0)
		
		team(0).setHasTech(iLaw, True, 0, True, False)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			self.assertEqual(str(goal), "1 / 20")
			
			team(1).setHasTech(iCurrency, True, 1, True, False)
			self.assertEqual(goal.state, POSSIBLE)
			
			team(1).setHasTech(iGeneralship, True, 1, True, False)
			self.assertEqual(goal.state, FAILURE)
		finally:
			team(0).setHasTech(iLaw, False, 0, True, False)
			team(1).setHasTech(iCurrency, False, 1, True, False)
			team(1).setHasTech(iGeneralship, False, 1, True, False)
			goal.deactivate()
	
	def testSunkShips(self):
		goal = Track.sunkShips(1).activate(0)
		
		ourShip = makeUnit(0, iWarGalley, (3, 3))
		theirShip = makeUnit(1, iGalley, (3, 4))
		
		events.fireEvent("combatResult", ourShip, theirShip)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1 / 1")
		finally:
			ourShip.kill(False, -1)
			theirShip.kill(False, -1)
		
			goal.deactivate()
	
	def testSunkShipWinnerNotUs(self):
		goal = Track.sunkShips(1).activate(0)
		
		theirShip = makeUnit(2, iWarGalley, (3, 3))
		thirdShip = makeUnit(1, iGalley, (3, 4))
		
		events.fireEvent("combatResult", theirShip, thirdShip)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 1")
		finally:
			theirShip.kill(False, -1)
			thirdShip.kill(False, -1)
		
			goal.deactivate()
	
	def testSunkShipLandUnits(self):
		goal = Track.sunkShips(1).activate(0)
		
		ourUnit = makeUnit(0, iSwordsman, (61, 31))
		theirUnit = makeUnit(1, iArcher, (62, 31))
		
		events.fireEvent("combatResult", ourUnit, theirUnit)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 1")
		finally:
			ourUnit.kill(False, -1)
			theirUnit.kill(False, -1)
		
			goal.deactivate()
	
	def testTradeGoldPlayerGoldTrade(self):
		goal = Track.tradeGold(100).activate(0)
		
		events.fireEvent("playerGoldTrade", 1, 0, 100)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "100 / 100")
		finally:
			goal.deactivate()
	
	def testTradeGoldPlayerGoldTradeDifferent(self):
		goal = Track.tradeGold(100).activate(0)
		
		events.fireEvent("playerGoldTrade", 0, 1, 100)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 100")
		finally:
			goal.deactivate()
	
	def testTradeGoldFromCities(self):
		goal = Track.tradeGold(100).activate(0)
		
		city1 = player(0).initCity(57, 50)
		city2 = player(0).initCity(57, 52)
		
		player(0).setCivics(iCivicsEconomy, iFreeEnterprise)
		player(0).setCommercePercent(CommerceTypes.COMMERCE_GOLD, 100)
		
		try:
			self.assert_(city1.getTradeYield(YieldTypes.YIELD_COMMERCE) > 0)
			self.assert_(city2.getTradeYield(YieldTypes.YIELD_COMMERCE) > 0)
		
			iExpectedCommerce = city1.getTradeYield(YieldTypes.YIELD_COMMERCE) + city2.getTradeYield(YieldTypes.YIELD_COMMERCE)
			iExpectedCommerce *= player(0).getCommercePercent(CommerceTypes.COMMERCE_GOLD)
			iExpectedCommerce /= 100
		
			self.assert_(iExpectedCommerce > 0)
		
			events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "%d / 100" % iExpectedCommerce)
		finally:
			city1.kill()
			city2.kill()
		
			player(0).setCivics(iCivicsEconomy, iReciprocity)
			player(0).setCommercePercent(CommerceTypes.COMMERCE_RESEARCH, 100)
		
			goal.deactivate()
		
	def testTradeGoldFromCitiesForeign(self):
		goal = Track.tradeGold(100).activate(0)
		
		city1 = player(1).initCity(57, 50)
		city2 = player(1).initCity(57, 52)
		
		player(1).setCivics(iCivicsEconomy, iFreeEnterprise)
		player(1).setCommercePercent(CommerceTypes.COMMERCE_GOLD, 100)
		
		try:
			self.assert_(city1.getTradeYield(YieldTypes.YIELD_COMMERCE) + city2.getTradeYield(YieldTypes.YIELD_COMMERCE))
		
			events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
			events.fireEvent("BeginPlayerTurn", 1, game.getGameTurn())
		
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 100")
		finally:
			city1.kill()
			city2.kill()
		
			player(1).setCivics(iCivicsEconomy, iReciprocity)
			player(1).setCommercePercent(CommerceTypes.COMMERCE_RESEARCH, 100)
		
			goal.deactivate()
	
	def testTradeGoldFromDeals(self):
		goal = Track.tradeGold(100).activate(0)
		
		player(0).changeGoldPerTurnByPlayer(1, 100)
		
		events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "100 / 100")
		finally:
			player(0).changeGoldPerTurnByPlayer(1, -100)
		
			goal.deactivate()
	
	def testTradeGoldFromDealsForeign(self):
		goal = Track.tradeGold(100).activate(0)
		
		player(1).changeGoldPerTurnByPlayer(0, 100)
		
		events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		events.fireEvent("BeginPlayerTurn", 1, game.getGameTurn())
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 100")
		finally:
			player(1).changeGoldPerTurnByPlayer(0, -100)
		
			goal.deactivate()
	
	def testTradeGoldFromTradeMission(self):
		goal = Track.tradeGold(1000).activate(0)
		
		city = player(1).initCity(30, 25)
		
		events.fireEvent("tradeMission", iGreatMerchant, 0, 30, 25, 1000)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1000 / 1000")
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testTradeGoldFromTradeMissionOther(self):
		goal = Track.tradeGold(1000).activate(0)
		
		city = player(2).initCity(30, 25)
		
		events.fireEvent("tradeMission", iGreatMerchant, 1, 30, 25, 1000)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 1000")
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testRaidGoldPillage(self):
		goal = Track.raidGold(100).activate(0)
		
		unit = makeUnit(0, iSwordsman, (61, 31))
		
		events.fireEvent("unitPillage", unit, iCottage, -1, 0, 100)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "100 / 100")
		finally:
			unit.kill(False, -1)
		
			goal.deactivate()
	
	def testRaidGoldPillageDifferent(self):
		goal = Track.raidGold(100).activate(0)
		
		unit = makeUnit(1, iSwordsman, (61, 31))
		
		events.fireEvent("unitPillage", unit, iCottage, -1, 1, 100)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 100")
		finally:
			unit.kill(False, -1)
		
			goal.deactivate()
	
	def testRaidGoldConquest(self):
		goal = Track.raidGold(100).activate(0)
		
		city = player(0).initCity(61, 31)
		
		events.fireEvent("cityCaptureGold", city, 0, 100)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "100 / 100")
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testRaidGoldConquestDifferent(self):
		goal = Track.raidGold(100).activate(0)
		
		city = player(1).initCity(61, 31)
		
		events.fireEvent("cityCaptureGold", city, 1, 100)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 100")
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testRaidGoldCombat(self):
		goal = Track.raidGold(100).activate(0)
		
		unit = makeUnit(0, iSwordsman, (61, 31))
		
		events.fireEvent("combatGold", 0, unit, 100)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "100 / 100")
		finally:
			unit.kill(False, -1)
		
			goal.deactivate()
	
	def testRaidGoldCombatOther(self):
		goal = Track.raidGold(100).activate(0)
		
		unit = makeUnit(1, iSwordsman, (61, 31))
		
		events.fireEvent("combatGold", 1, unit, 100)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 100")
		finally:
			unit.kill(False, -1)
		
			goal.deactivate()
	
	def testPillage(self):
		goal = Track.pillage(1).activate(0)
		
		unit = makeUnit(0, iSwordsman, (61, 31))
		
		events.fireEvent("unitPillage", unit, iCottage, -1, 0, 0)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1 / 1")
		finally:
			unit.kill(False, -1)
		
			goal.deactivate()
	
	def testPillageDifferent(self):
		goal = Track.pillage(1).activate(0)
		
		unit = makeUnit(1, iSwordsman, (61, 31))
		
		events.fireEvent("unitPillage", unit, iCottage, -1, 1, 0)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 1")
		finally:
			unit.kill(False, -1)
		
			goal.deactivate()
	
	def testPiracyGoldPillage(self):
		goal = Track.piracyGold(100).activate(0)
		
		unit = makeUnit(0, iSwordsman, (61, 31))
		
		events.fireEvent("unitPillage", unit, iCottage, -1, 0, 100)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "100 / 100")
		finally:
			unit.kill(False, -1)
		
			goal.deactivate()
	
	def testPiracyGoldBlockade(self):
		goal = Track.piracyGold(100).activate(0)
		
		events.fireEvent("blockade", 0, 100)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "100 / 100")
		finally:
			goal.deactivate()
	
	def testPiracyGoldCombat(self):
		goal = Track.piracyGold(100).activate(0)
		
		unit = makeUnit(0, iSwordsman, (61, 31))
		
		events.fireEvent("combatGold", 0, unit, 100)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "100 / 100")
		finally:
			unit.kill(False, -1)
		
			goal.deactivate()
	
	def testPiracyGoldCombatOther(self):
		goal = Track.piracyGold(100).activate(0)
		
		unit = makeUnit(1, iSwordsman, (61, 31))
		
		events.fireEvent("combatGold", 1, unit, 100)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 100")
		finally:
			unit.kill(False, -1)
		
			goal.deactivate()
	
	def testRazes(self):
		goal = Track.razes(1).activate(0)
		
		city = player(1).initCity(61, 31)
		player(0).acquireCity(city, True, False)
		city = city_(61, 31)
		
		events.fireEvent("cityRazed", city, 0)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1 / 1")
		finally:
			city.kill()
		
			goal.deactivate()
	
	def testSlaveTradeGold(self):
		goal = Track.slaveTradeGold(100).activate(0)
		
		events.fireEvent("playerSlaveTrade", 0, 100)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "100 / 100")
		finally:
			goal.deactivate()
	
	def testGreatGenerals(self):
		goal = Track.greatGenerals(1).activate(0)
		
		city = player(0).initCity(61, 31)
		unit = makeUnit(0, iGreatGeneral, (61, 31))
		
		events.fireEvent("greatPersonBorn", unit, 0, city)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1 / 1")
		finally:
			city.kill()
			unit.kill(False, -1)
		
			goal.deactivate()
	
	def testGreatGeneralsOther(self):
		goal = Track.greatGenerals(1).activate(0)
		
		city = player(0).initCity(61, 31)
		unit = makeUnit(0, iGreatScientist, (61, 31))
		
		events.fireEvent("greatPersonBorn", unit, 0, city)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 1")
		finally:
			city.kill()
			unit.kill(False, -1)
		
			goal.deactivate()
	
	def testResourceTradeGoldFromDeals(self):
		goal = Track.resourceTradeGold(100).activate(0)
		
		player(0).changeGoldPerTurnByPlayer(1, 100)
		
		events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "100 / 100")
		finally:
			player(0).changeGoldPerTurnByPlayer(1, -100)
		
			goal.deactivate()
	
	def testResourceTradeGoldFromDealsForeign(self):
		goal = Track.resourceTradeGold(100).activate(0)
		
		player(1).changeGoldPerTurnByPlayer(0, 100)
		
		events.fireEvent("BeginPlayerTurn", 0, game.getGameTurn())
		events.fireEvent("BeginPlayerTurn", 1, game.getGameTurn())
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 100")
		finally:
			player(1).changeGoldPerTurnByPlayer(0, -100)
		
			goal.deactivate()
	
	def testBrokeredPeace(self):
		goal = Track.brokeredPeace(1).activate(0)
		
		events.fireEvent("peaceBrokered", 0, 1, 2)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1 / 1")
		finally:
			goal.deactivate()
	
	def testBrokeredPeaceOther(self):
		goal = Track.brokeredPeace(1).activate(0)
		
		events.fireEvent("peaceBrokered", 2, 1, 0)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 1")
		finally:
			goal.deactivate()
	
	def testEnslave(self):
		goal = Track.enslaves(1).activate(0)
		
		unit = makeUnit(1, iSwordsman, (61, 31))
		
		events.fireEvent("enslave", 0, unit)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "1 / 1")
		finally:
			unit.kill(False, -1)
		
			goal.deactivate()
	
	def testEnslaveExcluding(self):
		goal = Track.enslaves(2).excluding([iBabylonia]).activate(0)
		
		unit0 = makeUnit(iBabylonia, iSwordsman, (61, 31))
		unit1 = makeUnit(iHarappa, iSwordsman, (62, 31))
		
		events.fireEvent("enslave", 0, unit0)
		events.fireEvent("enslave", 0, unit1)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
		finally:
			unit0.kill(False, -1)
			unit1.kill(False, -1)
		
			goal.deactivate()
	
	def testHealthiest(self):
		goal = Track.healthiest(3).activate(0)
		
		city = player(0).initCity(61, 31)
		city.changeExtraHealth(100)
		
		events.fireEvent("BeginPlayerTurn", 0, 0)
		events.fireEvent("BeginPlayerTurn", 1, 0)
		events.fireEvent("BeginPlayerTurn", 2, 0)
		
		events.fireEvent("BeginPlayerTurn", 0, 1)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "3 / 3")
		finally:
			city.kill()
			goal.deactivate()
	
	def testHealthiestOther(self):
		goal = Track.healthiest(3).activate(0)
		
		city = player(1).initCity(61, 31)
		city.changeExtraHealth(100)
		
		events.fireEvent("BeginPlayerTurn", 0, 0)
		events.fireEvent("BeginPlayerTurn", 0, 1)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 3")
		finally:
			city.kill()
			goal.deactivate()
	
	def testHappiest(self):
		goal = Track.happiest(3).activate(0)
		
		city = player(0).initCity(61, 31)
		city.changeExtraHappiness(100)
		
		events.fireEvent("BeginPlayerTurn", 0, 0)
		events.fireEvent("BeginPlayerTurn", 1, 0)
		events.fireEvent("BeginPlayerTurn", 2, 0)
		
		events.fireEvent("BeginPlayerTurn", 0, 1)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "3 / 3")
		finally:
			city.kill()
			goal.deactivate()
	
	def testHappiestOther(self):
		goal = Track.happiest(3).activate(0)
		
		city = player(1).initCity(61, 31)
		city.changeExtraHappiness(100)
		
		events.fireEvent("BeginPlayerTurn", 0, 0)
		events.fireEvent("BeginPlayerTurn", 0, 1)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 3")
		finally:
			city.kill()
			goal.deactivate()
	
	def testTrackPeace(self):
		goal = Track.peace(3).activate(0)
		
		events.fireEvent("BeginPlayerTurn", 0, 0)
		events.fireEvent("BeginPlayerTurn", 1, 0)
		events.fireEvent("BeginPlayerTurn", 2, 0)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "3 / 3")
		finally:
			goal.deactivate()
	
	def testTrackPeaceAtWar(self):
		goal = Track.peace(3).activate(0)
		
		team(0).setAtWar(1, True)
		team(1).setAtWar(0, True)
		
		events.fireEvent("BeginPlayerTurn", 0, 0)
		events.fireEvent("BeginPlayerTurn", 1, 0)
		events.fireEvent("BeginPlayerTurn", 2, 0)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "0 / 3")
		finally:
			team(0).setAtWar(1, False)
			team(1).setAtWar(0, False)
			goal.deactivate()
	
	def testTrackPeaceAfterPeace(self):
		goal = Track.peace(3).activate(0)
		
		events.fireEvent("BeginPlayerTurn", 0, 0)
		
		self.assertEqual(str(goal), "1 / 3")
			
		team(0).setAtWar(1, True)
		team(1).setAtWar(0, True)
		
		events.fireEvent("BeginPlayerTurn", 1, 0)
		
		try:
			self.assertEqual(str(goal), "1 / 3")
		finally:
			team(0).setAtWar(1, False)
			team(1).setAtWar(0, False)
			
		events.fireEvent("BeginPlayerTurn", 2, 0)
			
		self.assertEqual(str(goal), "2 / 3")
		
		goal.deactivate()
	
	def testTrackCombatFood(self):
		goal = Track.combatFood(10).activate(0)
		
		events.fireEvent("combatFood", 0, None, 10)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "10 / 10")
		finally:
			goal.deactivate()
	
	def testTrackSacrificeHappiness(self):
		goal = Track.sacrificeHappiness(3).activate(0)
		
		events.fireEvent("sacrificeHappiness", 0, None)
		events.fireEvent("sacrificeHappiness", 0, None)
		events.fireEvent("sacrificeHappiness", 0, None)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "3 / 3")
		finally:
			goal.deactivate()
	
	def testTrackCelebrate(self):
		goal = Track.celebrate(3).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city2 = player(0).initCity(63, 31)
		
		city1.setWeLoveTheKingDay(True)
		events.fireEvent("BeginPlayerTurn", 0, 0)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 3")
			
			city2.setWeLoveTheKingDay(True)
			events.fireEvent("BeginPlayerTurn", 1, 0)
			
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "3 / 3")
		finally:
			city1.kill()
			city2.kill()
			goal.deactivate()


class TestBestCityGoals(ExtendedTestCase):

	def setUp(self):
		for plot in plots.all():
			plot.resetCultureConversion()

	def testBestPopulationCity(self):
		goal = BestCity.population(city(61, 31)).activate(0)
		
		city_ = player(0).initCity(61, 31)
		city_.setPopulation(10)
		city_.setName("Zero", False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "Zero (10)\n(No City) (0)")
		finally:
			city_.kill()
	
	def testBestPopulationCityOtherLocation(self):
		goal = BestCity.population(city(61, 31)).activate(0)
		
		city_ = player(0).initCity(63, 31)
		city_.setPopulation(10)
		city_.setName("Zero", False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "Zero (10)\n(No City) (0)")
		finally:
			city_.kill()
	
	def testBestPopulationCityOtherOwner(self):
		goal = BestCity.population(city(61, 31)).activate(0)
		
		city_ = player(1).initCity(61, 31)
		city_.setPopulation(10)
		city_.setName("One", False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "One (10)\n(No City) (0)")
		finally:
			city_.kill()
	
	def testBestPopulationCityShowsSecondOnSuccess(self):
		goal = BestCity.population(city(61, 31)).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		city2 = player(2).initCity(65, 31)
		
		city0.setPopulation(10)
		city1.setPopulation(9)
		city2.setPopulation(8)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		city2.setName("Two", False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "Zero (10)\nOne (9)")
		finally:
			city0.kill()
			city1.kill()
			city2.kill()
	
	def testBestPopulationCityShowsOwnSecondOnFailure(self):
		goal = BestCity.population(city(61, 31)).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		city2 = player(2).initCity(65, 31)
		
		city0.setPopulation(10)
		city1.setPopulation(11)
		city2.setPopulation(12)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		city2.setName("Two", False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "Two (12)\nZero (10)")
		finally:
			city0.kill()
			city1.kill()
			city2.kill()
	
	def testBestPopulationCityNone(self):
		goal = BestCity.population(city(61, 31)).activate(0)
		
		self.assertEqual(bool(goal), False)
		self.assertEqual(str(goal), "(No City) (0)\n(No City) (0)")
	
	def testBestPopulationCityObjectiveBreaksTie(self):
		goal = BestCity.population(city(63, 31)).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(0).initCity(63, 31)
		city2 = player(0).initCity(65, 31)
		
		city0.setPopulation(10)
		city1.setPopulation(10)
		city2.setPopulation(10)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		city2.setName("Two", False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assert_(str(goal).startswith("One (10)"))
		finally:
			city0.kill()
			city1.kill()
			city2.kill()
	
	def testBestCultureCity(self):
		goal = BestCity.culture(city(61, 31)).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		city0.setCulture(0, 100, False)
		city1.setCulture(1, 50, False)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		
		try:
			self.assertEqual(city0.getCulture(0), 100)
			self.assertEqual(city1.getCulture(1), 50)
		
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "Zero (100)\nOne (50)")
		finally:
			city0.setCulture(0, 0, False)
			city1.setCulture(1, 0, False)
		
			city0.kill()
			city1.kill()
	
	def testBestCultureCityOtherLocation(self):
		goal = BestCity.culture(city(61, 31)).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(0).initCity(63, 31)
		
		city0.setCulture(0, 50, False)
		city1.setCulture(0, 100, False)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		
		try:
			self.assertEqual(city0.getCulture(0), 50)
			self.assertEqual(city1.getCulture(0), 100)
		
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "One (100)\nZero (50)")
		finally:
			city0.setCulture(0, 0, False)
			city1.setCulture(0, 0, False)
		
			city0.kill()
			city1.kill()
	
	def testBestCultureOtherOwner(self):
		goal = BestCity.culture(city(61, 31)).activate(0)
		
		city0 = player(1).initCity(61, 31)
		city1 = player(0).initCity(63, 31)
		
		city0.setCulture(1, 100, False)
		city1.setCulture(0, 50, False)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		
		try:
			self.assertEqual(city0.getCulture(1), 100)
			self.assertEqual(city1.getCulture(0), 50)
		
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "Zero (100)\n(No City) (0)")
		finally:
			city0.kill()
			city1.kill()
	
	def testBestWondersCity(self):
		goal = BestCity.wonders(city(61, 31)).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		city0.setHasRealBuilding(iPyramids, True)
		city0.setHasRealBuilding(iParthenon, True)
		
		city1.setHasRealBuilding(iColossus, True)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.progress(), [
				[u"%c Most wonders: Zero (2)" % self.SUCCESS_CHAR],
				["Next most wonders: One (1)"]
			])
		finally:
			city0.kill()
			city1.kill()
	
	def testBestWondersOtherLocation(self):
		goal = BestCity.wonders(city(59, 31)).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		city0.setHasRealBuilding(iPyramids, True)
		city0.setHasRealBuilding(iParthenon, True)
		
		city1.setHasRealBuilding(iColossus, True)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [[u"%c Most wonders: Zero (2)" % self.FAILURE_CHAR]])
		finally:
			city0.kill()
			city1.kill()
	
	def testBestWondersOtherOwner(self):
		goal = BestCity.wonders(city(61, 31)).activate(0)
		
		city0 = player(1).initCity(61, 31)
		city1 = player(0).initCity(63, 31)
		
		city0.setHasRealBuilding(iPyramids, True)
		city0.setHasRealBuilding(iParthenon, True)
		
		city1.setHasRealBuilding(iColossus, True)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [[u"%c Most wonders: Zero (2)" % self.FAILURE_CHAR]])
		finally:
			city0.kill()
			city1.kill()
	
	def testBestSpecialistCity(self):
		goal = BestCity.specialist(city(61, 31), iSpecialistGreatScientist).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		city0.setFreeSpecialistCount(iSpecialistGreatScientist, 4)
		city1.setFreeSpecialistCount(iSpecialistGreatScientist, 2)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.progress(), [
				[u"%c Most settled specialists: Zero (4)" % self.SUCCESS_CHAR],
				["Next most settled specialists: One (2)"]
			])
		finally:
			city0.kill()
			city1.kill()
	
	def testBestSpecialistCityGreatPeople(self):
		goal = BestCity.specialist(city(61, 31), great_people()).activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		city0.setFreeSpecialistCount(iSpecialistGreatArtist, 1)
		city0.setFreeSpecialistCount(iSpecialistGreatProphet, 1)
		city0.setFreeSpecialistCount(iSpecialistGreatScientist, 1)
		
		city1.setFreeSpecialistCount(iSpecialistGreatMerchant, 1)
		city1.setFreeSpecialistCount(iSpecialistGreatEngineer, 1)
		
		city0.setName("Zero", False)
		city1.setName("One", False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.progress(), [
				[u"%c Most settled specialists: Zero (3)" % self.SUCCESS_CHAR],
				["Next most settled specialists: One (2)"]
			])
		finally:
			city0.kill()
			city1.kill()
		

class TestBestPlayerGoals(ExtendedTestCase):
	
	def testBestPopulationPlayer(self):
		goal = BestPlayer.population().activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		city0.setPopulation(10)
		city1.setPopulation(9)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "Egypt (1000000)\nBabylonia (729000)")
		finally:
			city0.kill()
			city1.kill()

	def testBestPopulationPlayerOther(self):
		goal = BestPlayer.population().activate(0)
		
		city0 = player(0).initCity(61, 31)
		city1 = player(1).initCity(63, 31)
		
		city0.setPopulation(10)
		city1.setPopulation(11)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "Babylonia (1331000)\nEgypt (1000000)")
		finally:
			city0.kill()
			city1.kill()
	
	def testBestTechPlayer(self):
		goal = BestPlayer.tech().activate(0)
		
		for iTech in infos.techs():
			team(0).setHasTech(iTech, False, 0, False, False)
			team(1).setHasTech(iTech, False, 1, False, False)
		
		team(0).setHasTech(iGenetics, True, 0, False, False)
		team(1).setHasTech(iLaw, True, 1, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(str(goal), "Egypt (9000)\nBabylonia (280)")
		finally:
			team(0).setHasTech(iGenetics, False, 0, False, False)
			team(1).setHasTech(iLaw, False, 1, False, False)
		
	def testBestTechPlayerOther(self):
		goal = BestPlayer.tech().activate(0)
		
		for iTech in infos.techs():
			team(0).setHasTech(iTech, False, 0, False, False)
			team(1).setHasTech(iTech, False, 1, False, False)
		
		team(0).setHasTech(iLaw, True, 0, False, False)
		team(1).setHasTech(iGenetics, True, 1, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "Babylonia (9000)\nEgypt (280)")
		finally:
			team(0).setHasTech(iLaw, False, 0, False, False)
			team(1).setHasTech(iGenetics, False, 1, False, False)


class TestBestPlayersGoals(ExtendedTestCase):
	
	def testBestTechPlayersReligion(self):
		goal = BestPlayers.tech(3).religion().activate(0)
		
		player(0).setLastStateReligion(iProtestantism)
		player(1).setLastStateReligion(iProtestantism)
		player(2).setLastStateReligion(iCatholicism)
		
		for iTech in infos.techs():
			for iPlayer in [0, 1, 2]:
				team(iPlayer).setHasTech(iTech, False, iPlayer, False, False)
		
		team(0).setHasTech(iGenetics, True, 0, False, False)
		team(1).setHasTech(iGeography, True, 1, False, False)
		team(2).setHasTech(iLaw, True, 2, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [
				[u"%c Most advanced: Egypt (9000)" % self.SUCCESS_CHAR],
				[u"%c Second most advanced: Babylonia (1200)" % self.SUCCESS_CHAR],
				[u"%c Third most advanced: Harappa (280)" % self.FAILURE_CHAR]
			])
		finally:
			team(0).setHasTech(iGenetics, False, 0, False, False)
			team(1).setHasTech(iGeography, False, 1, False, False)
			team(2).setHasTech(iLaw, False, 2, False, False)
	
	def testBestTechPlayersSecular(self):
		goal = BestPlayers.tech(3).secular().activate(0)
		
		player(0).setCivics(iCivicsReligion, iSecularism)
		player(1).setCivics(iCivicsReligion, iSecularism)
		player(2).setCivics(iCivicsReligion, iSecularism)
		
		for iTech in infos.techs():
			for iPlayer in [0, 1, 2]:
				team(iPlayer).setHasTech(iTech, False, iPlayer, False, False)
		
		team(0).setHasTech(iGenetics, True, 0, False, False)
		team(1).setHasTech(iGeography, True, 1, False, False)
		team(2).setHasTech(iLaw, True, 2, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.progress(), [
				[u"%c Most advanced: Egypt (9000)" % self.SUCCESS_CHAR],
				[u"%c Second most advanced: Babylonia (1200)" % self.SUCCESS_CHAR],
				[u"%c Third most advanced: Harappa (280)" % self.SUCCESS_CHAR]
			])
		finally:
			team(0).setHasTech(iGenetics, False, 0, False, False)
			team(1).setHasTech(iGeography, False, 1, False, False)
			team(2).setHasTech(iLaw, False, 2, False, False)
		
			for iPlayer in [0, 1, 2]:
				player(iPlayer).setCivics(iCivicsReligion, iAnimism)


class TestBestCitiesGoals(ExtendedTestCase):

	def testBestPopulationPlayerAll(self):
		goal = BestCities.population(3).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setPopulation(10)
		
		city2 = player(0).initCity(63, 31)
		city2.setName("Second", False)
		city2.setPopulation(9)
		
		city3 = player(0).initCity(65, 31)
		city3.setName("Third", False)
		city3.setPopulation(8)
		
		city4 = player(1).initCity(67, 31)
		city4.setName("Fourth", False)
		city4.setPopulation(7)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.progress(), [
				[u"%c Most populous: First (10)" % self.SUCCESS_CHAR],
				[u"%c Second most populous: Second (9)" % self.SUCCESS_CHAR],
				[u"%c Third most populous: Third (8)" % self.SUCCESS_CHAR],
				["Next most populous: Fourth (7)"]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			city4.kill()
			goal.deactivate()
	
	def testBestPopulationPlayerAllAlsoNext(self):
		goal = BestCities.population(3).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setPopulation(10)
		
		city2 = player(0).initCity(63, 31)
		city2.setName("Second", False)
		city2.setPopulation(9)
		
		city3 = player(0).initCity(65, 31)
		city3.setName("Third", False)
		city3.setPopulation(8)
		
		city4 = player(0).initCity(67, 31)
		city4.setName("Fourth", False)
		city4.setPopulation(7)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.progress(), [
				[u"%c Most populous: First (10)" % self.SUCCESS_CHAR],
				[u"%c Second most populous: Second (9)" % self.SUCCESS_CHAR],
				[u"%c Third most populous: Third (8)" % self.SUCCESS_CHAR],
				["Next most populous: Fourth (7)"]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			city4.kill()
			goal.deactivate()
	
	def testBestPopulationPlayerSome(self):
		goal = BestCities.population(3).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setPopulation(10)
		
		city2 = player(0).initCity(63, 31)
		city2.setName("Second", False)
		city2.setPopulation(9)
		
		city3 = player(1).initCity(65, 31)
		city3.setName("Third", False)
		city3.setPopulation(8)
		
		city4 = player(1).initCity(67, 31)
		city4.setName("Fourth", False)
		city4.setPopulation(7)
		
		city5 = player(0).initCity(69, 31)
		city5.setName("Fifth", False)
		city5.setPopulation(6)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [
				[u"%c Most populous: First (10)" % self.SUCCESS_CHAR],
				[u"%c Second most populous: Second (9)" % self.SUCCESS_CHAR],
				[u"%c Third most populous: Third (8)" % self.FAILURE_CHAR],
				["Our next most populous: Fifth (6)"]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			city4.kill()
			city5.kill()
			goal.deactivate()
	
	def testBestPopulationMissingCities(self):
		goal = BestCities.population(3).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setPopulation(10)
		
		city2 = player(0).initCity(63, 31)
		city2.setName("Second", False)
		city2.setPopulation(9)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [
				[u"%c Most populous: First (10)" % self.SUCCESS_CHAR],
				[u"%c Second most populous: Second (9)" % self.SUCCESS_CHAR]
			])
		finally:
			city1.kill()
			city2.kill()
			goal.deactivate()
	
	def testBestPopulationNoCities(self):
		goal = BestCities.population(3).activate(0)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [[u"%c Most populous: (No City) (0)" % self.FAILURE_CHAR]])
		finally:
			goal.deactivate()
	
	def testBestPopulationMissingNextCity(self):
		goal = BestCities.population(3).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setPopulation(10)
		
		city2 = player(0).initCity(63, 31)
		city2.setName("Second", False)
		city2.setPopulation(9)
		
		city3 = player(1).initCity(65, 31)
		city3.setName("Third", False)
		city3.setPopulation(8)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [
				[u"%c Most populous: First (10)" % self.SUCCESS_CHAR],
				[u"%c Second most populous: Second (9)" % self.SUCCESS_CHAR],
				[u"%c Third most populous: Third (8)" % self.FAILURE_CHAR]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			goal.deactivate()

	def testBestPopulationCitiesReligionAll(self):
		goal = BestCities.population(3).religion().activate(0)
		
		player(0).setLastStateReligion(iJudaism)
		player(1).setLastStateReligion(iJudaism)
		player(2).setLastStateReligion(iJudaism)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setPopulation(10)
		city1.setHasReligion(iJudaism, True, False, False)
		
		city2 = player(1).initCity(63, 31)
		city2.setName("Second", False)
		city2.setPopulation(9)
		city2.setHasReligion(iJudaism, True, False, False)
		
		city3 = player(2).initCity(65, 31)
		city3.setName("Third", False)
		city3.setPopulation(8)
		city3.setHasReligion(iJudaism, True, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.progress(), [
				[u"%c Most populous: First (10)" % self.SUCCESS_CHAR],
				[u"%c Second most populous: Second (9)" % self.SUCCESS_CHAR],
				[u"%c Third most populous: Third (8)" % self.SUCCESS_CHAR]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			player(0).setLastStateReligion(-1)
			player(1).setLastStateReligion(-1)
			player(2).setLastStateReligion(-1)
			goal.deactivate()
	
	def testBestPopulationCitiesReligionSome(self):
		goal = BestCities.population(3).religion().activate(0)
		
		player(0).setLastStateReligion(iJudaism)
		player(1).setLastStateReligion(iJudaism)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setPopulation(10)
		city1.setHasReligion(iJudaism, True, False, False)
		
		city2 = player(1).initCity(63, 31)
		city2.setName("Second", False)
		city2.setPopulation(9)
		city2.setHasReligion(iJudaism, True, False, False)
		
		city3 = player(2).initCity(65, 31)
		city3.setName("Third", False)
		city3.setPopulation(8)
		
		city4 = player(2).initCity(67, 31)
		city4.setName("Fourth", False)
		city4.setPopulation(7)
		
		city5 = player(1).initCity(69, 31)
		city5.setName("Fifth", False)
		city5.setPopulation(6)
		city5.setHasReligion(iJudaism, True, False, False)
		
		city6 = player(0).initCity(71, 31)
		city6.setName("Sixth", False)
		city6.setPopulation(5)
		city6.setHasReligion(iJudaism, True, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [
				[u"%c Most populous: First (10)" % self.SUCCESS_CHAR],
				[u"%c Second most populous: Second (9)" % self.SUCCESS_CHAR],
				[u"%c Third most populous: Third (8)" % self.FAILURE_CHAR],
				["Our next most populous: Fifth (6)"]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			city4.kill()
			city5.kill()
			city6.kill()
			player(0).setLastStateReligion(-1)
			player(1).setLastStateReligion(-1)
			goal.deactivate()
	
	def testBestPopulationCitiesReligionLackingInCities(self):
		goal = BestCities.population(3).religion().activate(0)
		
		player(0).setLastStateReligion(iJudaism)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setPopulation(10)
		city1.setHasReligion(iJudaism, True, False, False)
		
		city2 = player(0).initCity(63, 31)
		city2.setName("Second", False)
		city2.setPopulation(9)
		city2.setHasReligion(iJudaism, True, False, False)
		
		city3 = player(0).initCity(65, 31)
		city3.setName("Third", False)
		city3.setPopulation(8)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [
				[u"%c Most populous: First (10)" % self.SUCCESS_CHAR],
				[u"%c Second most populous: Second (9)" % self.SUCCESS_CHAR],
				[u"%c Third most populous: Third (8)" % self.FAILURE_CHAR]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			player(0).setLastStateReligion(-1)
			goal.deactivate()
	
	def testBestPopulationCitiesReligionOnlyOthers(self):
		goal = BestCities.population(3).religion().activate(0)
		
		player(0).setLastStateReligion(iJudaism)
		player(1).setLastStateReligion(iJudaism)
		
		city1 = player(1).initCity(61, 31)
		city1.setName("First", False)
		city1.setPopulation(10)
		city1.setHasReligion(iJudaism, True, False, False)
		
		city2 = player(1).initCity(63, 31)
		city2.setName("Second", False)
		city2.setPopulation(9)
		city2.setHasReligion(iJudaism, True, False, False)
		
		city3 = player(1).initCity(65, 31)
		city3.setName("Third", False)
		city3.setPopulation(8)
		city3.setHasReligion(iJudaism, True, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.progress(), [
				[u"%c Most populous: First (10)" % self.SUCCESS_CHAR],
				[u"%c Second most populous: Second (9)" % self.SUCCESS_CHAR],
				[u"%c Third most populous: Third (8)" % self.SUCCESS_CHAR]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			player(0).setLastStateReligion(-1)
			player(1).setLastStateReligion(-1)
			goal.deactivate()
	
	def testBestPopulationCitiesReligionNoStateReligion(self):
		goal = BestCities.population(3).religion().activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setPopulation(10)
		
		city2 = player(0).initCity(63, 31)
		city2.setName("Second", False)
		city2.setPopulation(9)
		
		city3 = player(0).initCity(65, 31)
		city3.setName("Third", False)
		city3.setPopulation(8)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [
				[u"%c Most populous: First (10)" % self.FAILURE_CHAR],
				[u"%c Second most populous: Second (9)" % self.FAILURE_CHAR],
				[u"%c Third most populous: Third (8)" % self.FAILURE_CHAR]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			goal.deactivate()

	def testBestCulturePlayerAll(self):
		goal = BestCities.culture(3).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setCulture(0, 100, False)
		
		city2 = player(0).initCity(63, 31)
		city2.setName("Second", False)
		city2.setCulture(0, 90, False)
		
		city3 = player(0).initCity(65, 31)
		city3.setName("Third", False)
		city3.setCulture(0, 80, False)
		
		city4 = player(1).initCity(67, 31)
		city4.setName("Fourth", False)
		city4.setCulture(1, 70, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.progress(), [
				[u"%c Most cultured: First (100)" % self.SUCCESS_CHAR],
				[u"%c Second most cultured: Second (90)" % self.SUCCESS_CHAR],
				[u"%c Third most cultured: Third (80)" % self.SUCCESS_CHAR],
				["Next most cultured: Fourth (70)"]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			city4.kill()
			goal.deactivate()
	
	def testBestCulturePlayerAllAlsoNext(self):
		goal = BestCities.culture(3).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setCulture(0, 100, False)
		
		city2 = player(0).initCity(63, 31)
		city2.setName("Second", False)
		city2.setCulture(0, 90, False)
		
		city3 = player(0).initCity(65, 31)
		city3.setName("Third", False)
		city3.setCulture(0, 80, False)
		
		city4 = player(0).initCity(67, 31)
		city4.setName("Fourth", False)
		city4.setCulture(0, 70, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.progress(), [
				[u"%c Most cultured: First (100)" % self.SUCCESS_CHAR],
				[u"%c Second most cultured: Second (90)" % self.SUCCESS_CHAR],
				[u"%c Third most cultured: Third (80)" % self.SUCCESS_CHAR],
				["Next most cultured: Fourth (70)"]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			city4.kill()
			goal.deactivate()
	
	def testBestCulturePlayerSome(self):
		goal = BestCities.culture(3).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setCulture(0, 100, False)
		
		city2 = player(0).initCity(63, 31)
		city2.setName("Second", False)
		city2.setCulture(0, 90, False)
		
		city3 = player(1).initCity(65, 31)
		city3.setName("Third", False)
		city3.setCulture(1, 80, False)
		
		city4 = player(1).initCity(67, 31)
		city4.setName("Fourth", False)
		city4.setCulture(1, 70, False)
		
		city5 = player(0).initCity(69, 31)
		city5.setName("Fifth", False)
		city5.setCulture(0, 60, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [
				[u"%c Most cultured: First (100)" % self.SUCCESS_CHAR],
				[u"%c Second most cultured: Second (90)" % self.SUCCESS_CHAR],
				[u"%c Third most cultured: Third (80)" % self.FAILURE_CHAR],
				["Our next most cultured: Fifth (60)"]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			city4.kill()
			city5.kill()
			goal.deactivate()
	
	def testBestCultureMissingCities(self):
		goal = BestCities.culture(3).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setCulture(0, 100, False)
		
		city2 = player(0).initCity(63, 31)
		city2.setName("Second", False)
		city2.setCulture(0, 90, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [
				[u"%c Most cultured: First (100)" % self.SUCCESS_CHAR],
				[u"%c Second most cultured: Second (90)" % self.SUCCESS_CHAR]
			])
		finally:
			city1.kill()
			city2.kill()
			goal.deactivate()
	
	def testBestCultureNoCities(self):
		goal = BestCities.culture(3).activate(0)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [[u"%c Most cultured: (No City) (0)" % self.FAILURE_CHAR]])
		finally:
			goal.deactivate()
	
	def testBestCultureMissingNextCity(self):
		goal = BestCities.culture(3).activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setCulture(0, 100, False)
		
		city2 = player(0).initCity(63, 31)
		city2.setName("Second", False)
		city2.setCulture(0, 90, False)
		
		city3 = player(1).initCity(65, 31)
		city3.setName("Third", False)
		city3.setCulture(1, 80, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [
				[u"%c Most cultured: First (100)" % self.SUCCESS_CHAR],
				[u"%c Second most cultured: Second (90)" % self.SUCCESS_CHAR],
				[u"%c Third most cultured: Third (80)" % self.FAILURE_CHAR]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			goal.deactivate()

	def testBestCultureCitiesReligionAll(self):
		goal = BestCities.culture(3).religion().activate(0)
		
		player(0).setLastStateReligion(iJudaism)
		player(1).setLastStateReligion(iJudaism)
		player(2).setLastStateReligion(iJudaism)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setCulture(0, 100, True)
		city1.setHasReligion(iJudaism, True, False, False)
		
		city2 = player(1).initCity(63, 31)
		city2.setName("Second", False)
		city2.setCulture(1, 90, True)
		city2.setHasReligion(iJudaism, True, False, False)
		
		city3 = player(2).initCity(65, 31)
		city3.setName("Third", False)
		city3.setCulture(2, 80, True)
		city3.setHasReligion(iJudaism, True, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.progress(), [
				[u"%c Most cultured: First (100)" % self.SUCCESS_CHAR],
				[u"%c Second most cultured: Second (90)" % self.SUCCESS_CHAR],
				[u"%c Third most cultured: Third (80)" % self.SUCCESS_CHAR]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			player(0).setLastStateReligion(-1)
			player(1).setLastStateReligion(-1)
			player(2).setLastStateReligion(-1)
			goal.deactivate()
	
	def testBestCultureCitiesReligionSome(self):
		goal = BestCities.culture(3).religion().activate(0)
		
		player(0).setLastStateReligion(iJudaism)
		player(1).setLastStateReligion(iJudaism)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setCulture(0, 100, False)
		city1.setHasReligion(iJudaism, True, False, False)
		
		city2 = player(1).initCity(63, 31)
		city2.setName("Second", False)
		city2.setCulture(1, 90, False)
		city2.setHasReligion(iJudaism, True, False, False)
		
		city3 = player(2).initCity(65, 31)
		city3.setName("Third", False)
		city3.setCulture(2, 80, False)
		
		city4 = player(2).initCity(67, 31)
		city4.setName("Fourth", False)
		city4.setCulture(2, 70, False)
		
		city5 = player(1).initCity(69, 31)
		city5.setName("Fifth", False)
		city5.setCulture(1, 60, False)
		city5.setHasReligion(iJudaism, True, False, False)
		
		city6 = player(0).initCity(71, 31)
		city6.setName("Sixth", False)
		city6.setCulture(0, 50, False)
		city6.setHasReligion(iJudaism, True, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [
				[u"%c Most cultured: First (100)" % self.SUCCESS_CHAR],
				[u"%c Second most cultured: Second (90)" % self.SUCCESS_CHAR],
				[u"%c Third most cultured: Third (80)" % self.FAILURE_CHAR],
				["Our next most cultured: Fifth (60)"]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			city4.kill()
			city5.kill()
			city6.kill()
			player(0).setLastStateReligion(-1)
			player(1).setLastStateReligion(-1)
			goal.deactivate()
	
	def testBestCultureCitiesReligionLackingInCities(self):
		goal = BestCities.culture(3).religion().activate(0)
		
		player(0).setLastStateReligion(iJudaism)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setCulture(0, 100, False)
		city1.setHasReligion(iJudaism, True, False, False)
		
		city2 = player(0).initCity(63, 31)
		city2.setName("Second", False)
		city2.setCulture(0, 90, False)
		city2.setHasReligion(iJudaism, True, False, False)
		
		city3 = player(0).initCity(65, 31)
		city3.setName("Third", False)
		city3.setCulture(0, 80, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [
				[u"%c Most cultured: First (100)" % self.SUCCESS_CHAR],
				[u"%c Second most cultured: Second (90)" % self.SUCCESS_CHAR],
				[u"%c Third most cultured: Third (80)" % self.FAILURE_CHAR]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			player(0).setLastStateReligion(-1)
			goal.deactivate()
	
	def testBestCultureCitiesReligionOnlyOthers(self):
		goal = BestCities.culture(3).religion().activate(0)
		
		player(0).setLastStateReligion(iJudaism)
		player(1).setLastStateReligion(iJudaism)
		
		city1 = player(1).initCity(61, 31)
		city1.setName("First", False)
		city1.setCulture(1, 100, False)
		city1.setHasReligion(iJudaism, True, False, False)
		
		city2 = player(1).initCity(63, 31)
		city2.setName("Second", False)
		city2.setCulture(1, 90, False)
		city2.setHasReligion(iJudaism, True, False, False)
		
		city3 = player(1).initCity(65, 31)
		city3.setName("Third", False)
		city3.setCulture(1, 80, False)
		city3.setHasReligion(iJudaism, True, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.progress(), [
				[u"%c Most cultured: First (100)" % self.SUCCESS_CHAR],
				[u"%c Second most cultured: Second (90)" % self.SUCCESS_CHAR],
				[u"%c Third most cultured: Third (80)" % self.SUCCESS_CHAR]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			player(0).setLastStateReligion(-1)
			player(1).setLastStateReligion(-1)
			goal.deactivate()
	
	def testBestCultureCitiesReligionNoStateReligion(self):
		goal = BestCities.culture(3).religion().activate(0)
		
		city1 = player(0).initCity(61, 31)
		city1.setName("First", False)
		city1.setCulture(0, 100, False)
		
		city2 = player(0).initCity(63, 31)
		city2.setName("Second", False)
		city2.setCulture(0, 90, False)
		
		city3 = player(0).initCity(65, 31)
		city3.setName("Third", False)
		city3.setCulture(0, 80, False)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(goal.progress(), [
				[u"%c Most cultured: First (100)" % self.FAILURE_CHAR],
				[u"%c Second most cultured: Second (90)" % self.FAILURE_CHAR],
				[u"%c Third most cultured: Third (80)" % self.FAILURE_CHAR]
			])
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
			goal.deactivate()


class TestRouteConnection(ExtendedTestCase):

	def testDirectConnection(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad]).activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
			
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			start.kill()
			target.kill()
		
			for plot in plots.rectangle((62, 31), (63, 31)):
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testDirectConnectionTriggered(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad]).activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			events.fireEvent("BeginPlayerTurn", 0, 0)
		
			self.assertEqual(goal.state, SUCCESS)
		
			start.kill()
			target.kill()
		
			for plot in plots.rectangle((62, 31), (63, 31)):
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testNoRoute(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad]).activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			start.kill()
			target.kill()
		
			for plot in plots.rectangle((62, 31), (63, 31)):
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testNoCulture(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad]).activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			start.kill()
			target.kill()
		
			for plot in plots.rectangle((62, 31), (63, 31)):
				plot.setRouteType(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testDifferentRouteType(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRailroad]).activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 41)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		for iTech in [iLeverage, iRailroad]:
			team(0).setHasTech(iTech, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			start.kill()
			target.kill()
		
			for plot in plots.rectangle((62, 31), (63, 31)):
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			for iTech in [iLeverage, iRailroad]:
				team(0).setHasTech(iTech, False, 0, False, False)
		
			goal.deactivate()
	
	def testNoRouteTech(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad]).activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			start.kill()
			target.kill()
		
			for plot in plots.rectangle((62, 31), (63, 31)):
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			goal.deactivate()
	
	def testNoStartCity(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad]).activate(0)
		
		target = player(0).initCity(64, 41)
		
		for plot in plots.rectangle((61, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			target.kill()
		
			for plot in plots.rectangle((61, 31), (63, 31)):
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testDifferentStartCityOwner(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad]).activate(0)
		
		start = player(1).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			start.kill()
			target.kill()
		
			for plot in plots.rectangle((62, 31), (63, 31)):
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testNoTargetCity(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad]).activate(0)
		
		start = player(0).initCity(61, 31)
		
		for plot in plots.rectangle((62, 31), (64, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			start.kill()
		
			for plot in plots.rectangle((62, 31), (64, 31)):
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
		
	def testTargetCityDifferentOwner(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad]).activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(1).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			start.kill()
			target.kill()
		
			for plot in plots.rectangle((62, 31), (63, 31)):
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testIndirectConnection(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad]).activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		area = plots.of([(60, 32), (61, 33), (62, 33), (63, 33), (64, 33), (65, 32)])
		for plot in area:
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			start.kill()
			target.kill()
		
			for plot in area:
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			goal.deactivate()
	
	def testConnectionThroughCity(self):
		goal = RouteConnection(plots.of([(63, 31)]), plots.of([(65, 31)]), [iRouteRoad]).activate(0)
		
		start = player(0).initCity(61, 31)
		middle = player(0).initCity(63, 31)
		target = player(0).initCity(65, 31)
		
		area = plots.of([(62, 31), (64, 31)])
		for plot in area:
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			for city in [start, middle, target]:
				city.kill()
		
			for plot in area:
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testConnectionThroughCityDifferentOwner(self):
		goal = RouteConnection(plots.of([(63, 31)]), plots.of([(65, 31)]), [iRouteRoad]).activate(0)
		
		start = player(0).initCity(61, 31)
		middle = player(1).initCity(63, 31)
		target = player(0).initCity(65, 31)
		
		area = plots.of([(62, 31), (64, 31)])
		for plot in area:
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			for city in [start, middle, target]:
				city.kill()
		
			for plot in area:
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testMultipleStarts(self):
		starts = plots.rectangle((61, 31), (61, 33))
		targets = plots.of([(64, 31)])
		goal = RouteConnection(starts, targets, [iRouteRoad]).activate(0)
		
		start1 = player(0).initCity(61, 33)
		start2 = player(1).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		area = plots.rectangle((62, 32), (63, 32))
		for plot in area:
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			for city in [start1, start2, target]:
				city.kill()
		
			for plot in area:
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testMultipleTargets(self):
		starts = plots.of([(61, 31)])
		targets = plots.rectangle((64, 31), (64, 33))
		goal = RouteConnection(starts, targets, [iRouteRoad]).activate(0)
		
		start = player(0).initCity(61, 31)
		target1 = player(1).initCity(64, 31)
		target2 = player(0).initCity(64, 33)
		
		area = plots.rectangle((62, 32), (63, 32))
		for plot in area:
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			for city in [start, target1, target2]:
				city.kill()
		
			for plot in area:
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testWithStartOwners(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad]).withStartOwners().activate(0)
		
		start = player(1).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(1)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			start.kill()
			target.kill()
		
			for plot in plots.rectangle((62, 31), (63, 31)):
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testWithStartOwnersIncludingTarget(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(64, 31)]), [iRouteRoad]).withStartOwners().activate(0)
		
		start = player(1).initCity(61, 31)
		target = player(1).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(1)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			start.kill()
			target.kill()
		
			for plot in plots.rectangle((62, 31), (63, 31)):
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testWithDeferredCapital(self):
		goal = RouteConnection(capital(), plots.of([(64, 31)]), [iRouteRoad]).activate(0)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		start.setHasRealBuilding(iPalace, True)
		
		self.assertEqual(start.isCapital(), True)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			start.kill()
			target.kill()
		
			for plot in plots.rectangle((62, 31), (63, 31)):
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testWithDeferredCapitalElsewhere(self):
		goal = RouteConnection(capital(), plots.of([(64, 31)]), [iRouteRoad]).activate(0)
		
		capital_city = player(0).initCity(35, 35)
		capital_city.setHasRealBuilding(iPalace, True)
		
		self.assertEqual(capital_city.isCapital(), True)
		
		start = player(0).initCity(61, 31)
		target = player(0).initCity(64, 31)
		
		for plot in plots.rectangle((62, 31), (63, 31)):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			for city in [capital_city, start, target]:
				city.kill()
		
			for plot in plots.rectangle((62, 31), (63, 31)):
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testMultipleTargetsAll(self):
		goal = RouteConnection(plots.of([(63, 31)]), (plots.of([(61, 31)]), plots.of([(65, 31)])), [iRouteRoad]).activate(0)
		
		start = player(0).initCity(63, 31)
		target1 = player(0).initCity(61, 31)
		target2 = player(0).initCity(65, 31)
		
		for plot in plots.of([(62, 31), (64, 31)]):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), True)
		finally:
			for city in [start, target1, target2]:
				city.kill()
		
			for plot in plots.of([(62, 31), (64, 31)]):
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testMultipleTargetsSome(self):
		goal = RouteConnection(plots.of([(63, 31)]), (plots.of([(61, 31)]), plots.of([(65, 31)])), [iRouteRoad]).activate(0)
		
		start = player(0).initCity(63, 31)
		target1 = player(0).initCity(61, 31)
		target2 = player(0).initCity(65, 31)
		
		for plot in plots.of([(62, 31)]):
			plot.setRouteType(iRouteRoad)
			plot.setOwner(0)
		
		team(0).setHasTech(iLeverage, True, 0, False, False)
		
		try:
			self.assertEqual(bool(goal), False)
		finally:
			for city in [start, target1, target2]:
				city.kill()
		
			for plot in plots.of([(62, 31)]):
				plot.setRouteType(-1)
				plot.setOwner(-1)
		
			team(0).setHasTech(iLeverage, False, 0, False, False)
		
			goal.deactivate()
	
	def testCurrentStartsNone(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(63, 31)]), [iRouteRoad]).activate(0)
		
		self.assertEqual(goal.current_starts(), plots_.none().cities())
	
	def testCurrentStartsCities(self):
		goal = RouteConnection(plots.of([(61, 31)]), plots.of([(63, 31)]), [iRouteRoad]).activate(0)
		
		start = player(0).initCity(61, 31)
		
		try:
			self.assertEqual(len(goal.current_starts()), 1)
			self.assertEqual(start in goal.current_starts(), True)
		finally:
			start.kill()
	
	def testCurrentStartsDeferred(self):
		goal = RouteConnection(capital(), plots.of([(63, 31)]), [iRouteRoad]).activate(0)
		
		start = player(0).initCity(61, 31)
		start.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqual(start.isCapital(), True)
			self.assertType(goal.current_starts(), Cities)
			self.assertEqual(len(goal.current_starts()), 1)
			self.assertEqual(start in goal.current_starts(), True)
		finally:
			start.kill()
	
	def testCurrentStartsDeferredNoCity(self):
		goal = RouteConnection(capital(), plots.of([(63, 31)]), [iRouteRoad]).activate(0)
		
		self.assertEqual(goal.current_starts(), plots_.none().cities())
		
		
class SubGoal(BaseGoal):

	types = ArgumentProcessor([int], None, 0)

	def __init__(self, *arguments):
		super(SubGoal, self).__init__(*arguments)
		
		self.string = ""
		self.iMinArgument = 0
		self.bDeactivated = False
	
	def condition(self, argument):
		return argument >= self.iMinArgument
	
	def handler(self, *args):
		self.check()
	
	def deactivate(self):
		super(SubGoal, self).deactivate()
		self.bDeactivated = True
	
	def __str__(self):
		return self.string


class TestAllGoal(ExtendedTestCase):

	def testActivate(self):
		def callback():
			pass
		
		goal = All(SubGoal(), SubGoal()).activate(0, callback)
		goal1, goal2 = goal.goals
		
		try:
			self.assertEqual(goal.iPlayer, 0)
			self.assertEqual(goal1.iPlayer, 0)
			self.assertEqual(goal2.iPlayer, 0)

			self.assertEqual(goal.callback, callback)
			
			self.assertType(goal1.callback, SubgoalCallback)
			self.assertEqual(goal1.callback.supergoal, goal)
			
			self.assertType(goal2.callback, SubgoalCallback)
			self.assertEqual(goal2.callback.supergoal, goal)
		finally:
			goal.deactivate()
	
	def testOneSuccess(self):
		goal = All(SubGoal(), SubGoal()).activate(0)
		goal1, goal2 = goal.goals
		
		goal1.succeed()
		
		try:
			self.assertEqual(goal1.state, SUCCESS)
			self.assertEqual(goal2.state, POSSIBLE)
			self.assertEqual(goal.state, POSSIBLE)
		finally:
			goal.deactivate()
	
	def testAllSuccess(self):
		goal = All(SubGoal(), SubGoal()).activate(0)
		goal1, goal2 = goal.goals
		
		goal1.succeed()
		goal2.succeed()
		
		try:
			self.assertEqual(goal1.state, SUCCESS)
			self.assertEqual(goal2.state, SUCCESS)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			goal.deactivate()
	
	def testOneFailure(self):
		goal = All(SubGoal(), SubGoal()).activate(0)
		goal1, goal2 = goal.goals
		
		goal1.fail()
		
		try:
			self.assertEqual(goal1.state, FAILURE)
			self.assertEqual(goal2.state, FAILURE)
			self.assertEqual(goal.state, FAILURE)
		finally:
			goal.deactivate()
		
	def testString(self):
		goal1 = SubGoal()
		goal2 = SubGoal()
		
		goal1.string = "goal1"
		goal2.string = "goal2"
		
		goal = All(goal1, goal2).activate(0)
		goal1, goal2 = goal.goals
		
		try:
			self.assertEqual(str(goal1), "goal1")
			self.assertEqual(str(goal2), "goal2")
			self.assertEqual(str(goal), "goal1\ngoal2")
		finally:
			goal.deactivate()
	
	def testAt(self):
		goal = All(SubGoal(1), SubGoal(1)).at(-3000).activate(0)
		goal1, goal2 = goal.goals
		
		try:
			self.assertEqual(goal1.state, POSSIBLE)
			self.assertEqual(goal2.state, POSSIBLE)
			self.assertEqual(goal.state, POSSIBLE)
		
			events.fireEvent("BeginPlayerTurn", 0, 0)
		
			self.assertEqual(goal1.state, SUCCESS)
			self.assertEqual(goal2.state, SUCCESS)
			self.assertEqual(goal.state, SUCCESS)
		finally:
			goal.deactivate()
	
	def testBy(self):
		goal = All(SubGoal(1), SubGoal(-1)).by(-3000).activate(0)
		goal1, goal2 = goal.goals
		
		try:
			self.assertEqual(goal1.state, POSSIBLE)
			self.assertEqual(goal2.state, POSSIBLE)
			self.assertEqual(goal.state, POSSIBLE)
		
			events.fireEvent("BeginPlayerTurn", 0, 0)
		
			self.assertEqual(goal1.state, FAILURE)
			self.assertEqual(goal2.state, FAILURE)
			self.assertEqual(goal.state, FAILURE)
		finally:
			goal.deactivate()
	
	def testDeactivate(self):
		goal = All(SubGoal(1), SubGoal(1)).activate(0)
		goal1, goal2 = goal.goals
		
		goal.deactivate()
		
		self.assertEqual(goal1.bDeactivated, True)
		self.assertEqual(goal2.bDeactivated, True)
	
	def testDescription(self):
		goal1 = DescriptionGoal(iGranary, 3)
		goal2 = DescriptionGoal(iLibrary, 4)
		goal3 = DescriptionGoal(iCastle, 5).named("SETTLE")
		
		goal = All(goal1, goal2, goal3)
		
		self.assertEqual(goal.description(), "Control three Granaries, control four Libraries and settle five Castles")
	
	def testDescriptionSharedBeginning(self):
		goal1 = DescriptionGoal(iGranary, 3)
		goal2 = DescriptionGoal(iLibrary, 4)
		
		goal = All(goal1, goal2)
		
		self.assertEqual(goal.description(), "Control three Granaries and four Libraries")
	
	def testDescriptionSharedEnding(self):
		goal1 = DescriptionGoal(iGranary, 3).named("SETTLE")
		goal2 = DescriptionGoal(iGranary, 3)
		
		goal = All(goal1, goal2)
		
		self.assertEqual(goal.description(), "Settle and control three Granaries")
	
	def testDescriptionSharedEndingDate(self):
		goal1 = DescriptionGoal(iGranary, 3).by(1000).named("SETTLE")
		goal2 = DescriptionGoal(iLibrary, 4).by(1000)
		
		goal = All(goal1, goal2)
		
		self.assertEqual(goal.description(), "Settle three Granaries and control four Libraries by 1000 AD")
	
	def testDescriptionDifferentEndingDate(self):
		goal1 = DescriptionGoal(iGranary, 3).named("SETTLE").by(800)
		goal2 = DescriptionGoal(iLibrary, 4).by(1000)
		
		goal = All(goal1, goal2)
		
		self.assertEqual(goal.description(), "Settle three Granaries by 800 AD and control four Libraries by 1000 AD")

class TestSomeGoal(ExtendedTestCase):

	def testActivate(self):
		def callback():
			pass
		
		goal = Some(SubGoal(), 1).activate(0, callback)
		subgoal = goal.goal
		
		self.assertEqual(goal.iPlayer, 0)
		self.assertEqual(subgoal.iPlayer, 0)
		
		self.assertEqual(goal.callback, callback)
		self.assertType(subgoal.callback, CheckedSubgoalCallback)
	
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
		goal = Some(subgoal, 2).activate(0)
		subgoal = goal.goal
		
		try:
			self.assertEqual(bool(subgoal), False)
			self.assertEqual(bool(goal), True)
			self.assertEqual(goal.state, POSSIBLE)
		
			self.assertEqual(subgoal.condition(0), False)
			self.assertEqual(subgoal.condition(1), True)
			self.assertEqual(subgoal.condition(2), True)
		
			subgoal.check()
		
			self.assertEqual(goal.state, SUCCESS)
		finally:
			goal.deactivate()
	
	def testDescription(self):
		subgoal = DescriptionGoal(iGranary, 3)
		goal = Some(subgoal, 2)
		
		self.assertEqual(goal.description(), "Control two out of three Granaries")
	
	def testWithFirstGreatPerson(self):
		goal = Some(Trigger.firstGreatPerson(iSpecialistGreatArtist, iSpecialistGreatEngineer, iSpecialistGreatMerchant), 2).activate(0)
		
		artist = makeUnit(0, iGreatArtist, (0, 0))
		events.fireEvent("greatPersonBorn", artist, 0, None)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
		
			try:
				engineer = makeUnit(0, iGreatEngineer, (0, 0))
				events.fireEvent("greatPersonBorn", engineer, 0, None)
		
				self.assertEqual(bool(goal), True)
				self.assertEqual(str(goal), "2 / 2")
				self.assertEqual(goal.state, SUCCESS)
			finally:
				engineer.kill(False, -1)
		finally:
			artist.kill(False, -1)
			goal.deactivate()
	
	def testWithFirstGreatPersonOneOther(self):
		goal = Some(Trigger.firstGreatPerson(iSpecialistGreatArtist, iSpecialistGreatEngineer, iSpecialistGreatMerchant), 2).activate(0)
		
		artist = makeUnit(0, iGreatMerchant, (0, 0))
		events.fireEvent("greatPersonBorn", artist, 0, None)
		
		try:
			self.assertEqual(bool(goal), False)
			self.assertEqual(str(goal), "1 / 2")
			
			merchant = makeUnit(1, iGreatMerchant, (0, 0))
			events.fireEvent("greatPersonBorn", merchant, 1, None)
			
			try:
				self.assertEqual(bool(goal), False)
				self.assertEqual(str(goal), "1 / 2")
				self.assertEqual(goal.state, POSSIBLE)
				
				engineer = makeUnit(0, iGreatEngineer, (0, 0))
				events.fireEvent("greatPersonBorn", engineer, 0, None)
				
				try:
					self.assertEqual(bool(goal), True)
					self.assertEqual(str(goal), "2 / 2")
					self.assertEqual(goal.state, SUCCESS)
				finally:
					engineer.kill(False, -1)
			finally:
				merchant.kill(False, -1)
		finally:
			artist.kill(False, -1)
			goal.deactivate()
	
	def testWithFirstGreatPersonTwoOther(self):
		goal = Some(Trigger.firstGreatPerson(iSpecialistGreatArtist, iSpecialistGreatEngineer, iSpecialistGreatMerchant), 2).activate(0)
		
		artist = makeUnit(1, iGreatArtist, (0, 0))
		events.fireEvent("greatPersonBorn", artist, 1, None)
		
		try:
			self.assertEqual(goal.state, POSSIBLE)
			
			engineer = makeUnit(1, iGreatEngineer, (0, 0))
			events.fireEvent("greatPersonBorn", engineer, 1, None)
			
			try:
				self.assertEqual(goal.state, FAILURE)
			finally:
				engineer.kill(False, -1)
		finally:
			artist.kill(False, -1)
			goal.deactivate()


class CityGoal(BaseGoal):

	types = ArgumentProcessor([], CyCity, 0)
	
	def __init__(self, *arguments):
		super(CityGoal, self).__init__(*arguments)
		
		self.complete = False
		self.string = ""
		
		self._description = "have %s" % self.types.format_subject(self.arguments.subject)
	
	def condition(self, *arguments):
		return self.complete
	
	def internal_progress(self, bForceSingle=False):
		return ["%s Some city goal: %s" % (self.format_progress_indicator(self.complete), self.string)]
		
	def __str__(self):
		return self.string
		
		
class TestDifferentCities(ExtendedTestCase):

	def testActivate(self):
		goal1 = CityGoal(capital())
		goal2 = CityGoal(capital())
		goal1.string = "one"
		goal2.string = "two"
		goal = DifferentCities(goal1, goal2).activate(0)
		goal1, goal2 = goal.goals
		
		try:
			self.assertEqual(goal.iPlayer, 0)
			self.assertEqual(goal1.iPlayer, 0)
			self.assertEqual(goal2.iPlayer, 0)
		
			self.assertType(goal1.callback, DifferentCallback)
			self.assertType(goal2.callback, DifferentCallback)
		
			self.assertEqual(goal1.callback.supergoal, goal)
			self.assertEqual(goal2.callback.supergoal, goal)
		finally:
			goal.deactivate()

	def testCompleteWithDifferentCities(self):
		goal1 = CityGoal(capital())
		goal2 = CityGoal(capital())
		goal1.string = "one"
		goal2.string = "two"
		goal = DifferentCities(goal1, goal2).activate(0)
		goal1, goal2 = goal.goals
		
		self.assertEqual(str(goal), "one\ntwo")
		self.assertEqual(goal.progress(), [[u"%c Some city goal: one" % self.FAILURE_CHAR]])
		
		city1 = player(0).initCity(61, 31)
		city1.setHasRealBuilding(iPalace, True)
		city1.setName("CityOne", False)
			
		try:
			self.assertEqual(location(capital_(0)), (61, 31))
			
			self.assertEqual(str(goal), "CityOne: one\nCityOne: two")
			self.assertEqual(goal.progress(), [[u"%c Some city goal: one" % self.FAILURE_CHAR]])
			
			goal1.succeed()
			self.assertEqual(goal1.state, SUCCESS)
			self.assertEqual(goal.state, POSSIBLE)
			self.assertEqual(bool(goal), False)
			
			self.assertEqual(goal.recorded(goal1), (61, 31))
			self.assertEqual(goal.recorded(goal2), None)
			
			self.assertEqual(str(goal), "CityOne: one\nCityOne: two")
			self.assertEqual(goal.progress(), [
				[u"%c CityOne" % self.SUCCESS_CHAR],
				[u"%c Some city goal: two" % self.FAILURE_CHAR]
			])
			
			city2 = player(0).initCity(63, 31)
			city1.setHasRealBuilding(iPalace, False)
			city2.setHasRealBuilding(iPalace, True)
			city2.setName("CityTwo", False)
			
			option_value = AdvisorOpt.getUHVFinishDate()
			AdvisorOpt.setUHVFinishDate(1)
			
			try:
				self.assertEqual(location(capital_(0)), (63, 31))
			
				goal2.succeed()
				
				self.assertEqual(goal2.state, SUCCESS)
				self.assertEqual(goal.state, SUCCESS)
				
				self.assertEqual(goal.recorded(goal1), (61, 31))
				self.assertEqual(goal.recorded(goal2), (63, 31))
				
				self.assertEqual(str(goal), "CityOne: one\nCityTwo: two")
				self.assertEqual(goal.progress(), [[u"%c Goal accomplished! (3000 BC)" % self.SUCCESS_CHAR]])
			finally:
				city2.kill()
				AdvisorOpt.setUHVFinishDate(option_value)
		finally:
			city1.kill()
	
	def testCompleteWithIdenticalCity(self):
		goal1 = CityGoal(capital())
		goal2 = CityGoal(capital())
		goal1.string = "one"
		goal2.string = "two"
		
		goal = DifferentCities(goal1, goal2).activate(0)
		goal1, goal2 = goal.goals
		
		self.assertEqual(str(goal), "one\ntwo")
		self.assertEqual(goal.progress(), [[u"%c Some city goal: one" % self.FAILURE_CHAR]])
			
		city1 = player(0).initCity(61, 31)
		city1.setHasRealBuilding(iPalace, True)
		city1.setName("CityOne", False)
		
		try:
			self.assertEqual(location(capital_(0)), (61, 31))
			
			self.assertEqual(str(goal), "CityOne: one\nCityOne: two")
			self.assertEqual(goal.progress(), [[u"%c Some city goal: one" % self.FAILURE_CHAR]])
			
			goal1.succeed()
			self.assertEqual(goal1.state, SUCCESS)
			self.assertEqual(goal.state, POSSIBLE)
			self.assertEqual(bool(goal), False)
			
			self.assertEqual(goal.recorded(goal1), (61, 31))
			self.assertEqual(goal.recorded(goal2), None)
			
			self.assertEqual(str(goal), "CityOne: one\nCityOne: two")
			self.assertEqual(goal.progress(), [
				[u"%c CityOne" % self.SUCCESS_CHAR],
				[u"%c Some city goal: two" % self.FAILURE_CHAR]
			])
			
			goal2.succeed()
			self.assertEqual(goal2.state, FAILURE)
			self.assertEqual(goal.state, FAILURE)
			self.assertEqual(bool(goal), False)
			
			self.assertEqual(goal.recorded(goal1), (61, 31))
			self.assertEqual(goal.recorded(goal2), (61, 31))
			
			self.assertEqual(str(goal), "CityOne: one\nCityOne: two")
			self.assertEqual(goal.progress(), [[u"%c Goal failed!" % self.FAILURE_CHAR]])
		finally:
			city1.kill()
	
	def testCityChangedAfterIncomplete(self):
		goal1 = CityGoal(capital())
		goal2 = CityGoal(capital())
		goal1.string = "one"
		goal2.string = "two"
		
		goal = DifferentCities(goal1, goal2).activate(0)
		goal1, goal2 = goal.goals
		
		city1 = player(0).initCity(61, 31)
		city1.setHasRealBuilding(iPalace, True)
		city1.setName("CityOne", False)
		
		try:
			self.assertEqual(location(capital_(0)), (61, 31))
		
			goal1.succeed()
			goal2.succeed()
			
			self.assertEqual(goal2.state, FAILURE)
			self.assertEqual(goal.state, FAILURE)
			self.assertEqual(bool(goal), False)
			
			self.assertEqual(goal.recorded(goal1), (61, 31))
			self.assertEqual(goal.recorded(goal2), (61, 31))
			
			self.assertEqual(str(goal), "CityOne: one\nCityOne: two")
			self.assertEqual(goal.progress(), [[u"%c Goal failed!" % self.FAILURE_CHAR]])
			
			city2 = player(0).initCity(63, 31)
			city1.setHasRealBuilding(iPalace, False)
			city2.setHasRealBuilding(iPalace, True)
			city2.setName("CityTwo", False)
			
			try:
				self.assertEqual(location(capital_(0)), (63, 31))
			
				self.assertEqual(str(goal), "CityOne: one\nCityOne: two")
				self.assertEqual(goal.state, FAILURE)
				self.assertEqual(goal.progress(), [[u"%c Goal failed!" % self.FAILURE_CHAR]])
			finally:
				city2.kill()
		finally:
			city1.kill()
	
	def testDescription(self):
		goal1 = CityGoal(capital())
		goal2 = CityGoal(capital().named("DIFFERENT_CAPITAL"))
		
		goal = DifferentCities(goal1, goal2)
		
		self.assertEqual(goal.description(), "Have your capital and have a different capital")


class TestNamedList(ExtendedTestCase):

	def testList(self):
		list = NamedList([1, 2, 3])
		self.assertEqual(str(list), "[1, 2, 3]")
	
	def testVarargs(self):
		list = NamedList(1, 2, 3)
		self.assertEqual(str(list), "[1, 2, 3]")
	
	def testNamed(self):
		list = NamedList(1, 2, 3).named("UHV_CITY")
		self.assertEqual(str(list), "city")
	
	def testLen(self):
		list = NamedList(1, 2, 3)
		self.assertEqual(len(list), 3)
	
	def testIter(self):
		list = NamedList(1, 2, 3)
		self.assertEqual([x for x in list], [1, 2, 3])
	
	def testNonzeroFalse(self):
		list = NamedList()
		self.assertEqual(bool(list), False)
	
	def testNonzeroTrue(self):
		list = NamedList(1, 2, 3)
		self.assertEqual(bool(list), True)
	
	def testEqualNamedList(self):
		namedList1 = NamedList(1, 2, 3)
		namedList2 = NamedList(1, 2, 3)
		self.assertEqual(namedList1, namedList2)
	
	def testEqualList(self):
		namedList = NamedList(1, 2, 3)
		list = [1, 2, 3]
		self.assertEqual(namedList, list)
	
	def testEqualOther(self):
		namedList = NamedList(1, 2, 3)
		self.assertEqual(namedList == "1, 2, 3", False)


class TestGroup(ExtendedTestCase):

	def testGroup(self):
		firstGroup = group(0)
		self.assertType(firstGroup, NamedList)
		self.assertEqual(firstGroup, dCivGroups[0])
	

test_cases = [
	TestGetNumArgs,
	TestEventHandlers,
	TestDeferred,
	TestAggregate,
	TestArguments,
	TestArgumentProcessor,
	TestArgumentProcessorFormat,
	TestArgumentProcessorBuilder,
	TestBaseGoal,
	TestProgress,
	TestAreas,
	TestConditionGoals,
	TestCountGoals,
	TestPercentageGoals,
	TestTriggerGoals,
	TestTrackGoals,
	TestBestCityGoals,
	TestBestPlayersGoals,
	TestBestCitiesGoals,
	TestRouteConnection,
	TestAllGoal,
	TestSomeGoal,
	TestDifferentCities,
	TestNamedList,
	TestGroup,
]


disable_victories()

suite = TestSuite([makeSuite(case) for case in test_cases])
TextTestRunner(verbosity=2).run(suite)