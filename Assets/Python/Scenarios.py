from Civilizations import initScenarioTechs
from RFCUtils import *
from Core import *

from Events import handler


@handler("GameStart")
def initScenario():
	updateStartingPlots()

	adjustCityCulture()
	
	updateGreatWall()
		
	foundCapitals()
	flipStartingTerritory()
	
	adjustReligionFoundingDates()
	initStartingReligions()
	
	initScenarioTechs()
	
	createStartingUnits()
	
	adjustWonders()
	adjustGreatPeople()
	adjustCulture()
	
	initDiplomacy()
	prepareColonists()
	
	for iPlayer in players.major().where(lambda p: dBirth[p] < scenarioStartYear()):
		data.players[iPlayer].bSpawned = True
	
	invalidateUHVs()
	
	game.setVoteSourceReligion(1, iCatholicism, False)
	
	updateExtraOptions()

def updateStartingPlots():
	for iPlayer in players.major():
		player(iPlayer).setStartingPlot(plots.capital(iPlayer), False)

def adjustCityCulture():
	if turns(10) == 10: return
		
	for city in cities.all():
		city.setCulture(city.getOwner(), turns(city.getCulture(city.getOwner())), True)

def updateGreatWall():
	if scenario() == i3000BC:
		return

	elif scenario() == i600AD:
		lAddWall = [(100, 46), (99, 46), (98, 45), (98, 43), (99, 42), (100, 41), (100, 40)]
		
		beijing = city(tBeijing)
		for x, y in lAddWall:
			plot_(x, y).setOwner(beijing.getOwner())
		
		beijing.updateGreatWall()
	
		tTL = (98, 39)
		tBR = (107, 48)
		lExceptions = [(105, 48), (106, 48), (107, 48), (106, 47), (98, 46), (98, 47), (99, 47), (98, 48), (99, 48), (98, 39), (99, 39), (100, 39), (98, 40), (99, 40), (98, 41), (99, 41), (98, 42), (100, 40)]
		lAdditions = [(103, 38), (104, 37), (102, 49), (103, 49)]
			
	elif scenario() == i1700AD:
		tTL = (98, 40)
		tBR = (106, 50)
		lExceptions = [(98, 46), (98, 47), (98, 48), (98, 49), (99, 49), (98, 50), (99, 50), (100, 50), (99, 47), (99, 48), (100, 49), (101, 49), (101, 50), (102, 50)]
		lAdditions = [(104, 51), (105, 51), (106, 51), (107, 41), (107, 42), (107, 43), (103, 38), (103, 39), (104, 39), (105, 39), (104, 37)]
		
		lRemoveWall = [(97, 40), (98, 39), (99, 39), (100, 39), (101, 39), (102, 39)]
		
		for x, y in lRemoveWall:
			plot_(x, y).setOwner(-1)
			
		city(102, 47).updateGreatWall()
		
		for x, y in lRemoveWall:
			plot_(x, y).setOwner(slot(iChina))
	
	for plot in plots.rectangle(tTL, tBR).without(lExceptions).including(lAdditions).land():
		plot.setWithinGreatWall(True)

def foundCapitals():
	if scenario() == i600AD:
	
		# China
		prepareChina()
		capital = plots.capital(iChina)
		lBuildings = [iGranary, iConfucianTemple, iTaixue, iBarracks, iForge]
		foundCapital(slot(iChina), location(capital), "Xi'an", 4, 100, lBuildings, [iConfucianism, iTaoism])
		
	elif scenario() == i1700AD:
		
		# Chengdu
		city(99, 41).setCulture(slot(iChina), 100, True)
		pass

def prepareChina():
	pGuiyang = plot_(102, 41)
	city(pGuiyang).kill()
	pGuiyang.setImprovementType(-1)
	pGuiyang.setRouteType(-1)
	pGuiyang.setFeatureType(iForest, 0)

	if scenario() == i600AD:
		pXian = plot_(100, 44)
		city(pXian).kill()
		pXian.setImprovementType(-1)
		pXian.setRouteType(-1)
		pXian.setFeatureType(iForest, 0)
		
	elif scenario() == i1700AD:
		pBeijing = plot_(tBeijing, tBeijing)
		city(pBeijing).kill()
		pBeijing.setImprovementType(-1)
		pBeijing.setRouteType(-1)

	tCultureRegionTL = (98, 37)
	tCultureRegionBR = (109, 49)
	for iMinor in players.independent():
		for plot in plots.start(tCultureRegionTL).end(tCultureRegionBR):
			bCity = False
			for loopPlot in plots.surrounding(plot):
				if loopPlot.isCity():
					bCity = True
					loopPlot.getPlotCity().setCulture(iMinor, 0, False)
			if bCity:
				plot.setCulture(iMinor, 1, True)
			else:
				plot.setCulture(iMinor, 0, True)
				plot.setOwner(-1)
				
	iMinor = players.independent().random()
	if iMinor:
		player(iMinor).found(99, 41)
		makeUnit(iMinor, iArcher, (99, 41))
	
		pChengdu = city(99, 41)
		pChengdu.setName("Chengdu", False)
		pChengdu.setPopulation(2)
		pChengdu.setHasReligion(iConfucianism, True, False, False)
		pChengdu.setHasRealBuilding(iGranary, True)
		pChengdu.setHasRealBuilding(iDujiangyan, True)
	
	if scenario() == i600AD:
		player(iBarbarian).found(105, 49)
		makeUnit(iBarbarian, iArcher, (105, 49))
		pShenyang = city(105, 49)
		pShenyang.setName("Simiyan hoton", False)
		pShenyang.setPopulation(2)
		pShenyang.setHasReligion(iConfucianism, True, False, False)
		pShenyang.setHasRealBuilding(iGranary, True)
		pShenyang.setHasRealBuilding(iWalls, True)
		pShenyang.setHasRealBuilding(iConfucianTemple, True)

def flipStartingTerritory():

	if scenario() == i600AD:
		
		# China
		if not player(iChina).isHuman(): tTL = (99, 39) # 4 tiles further south
		startingFlip(slot(iChina), [dBirthArea[iChina]])
		
	if scenario() == i1700AD:
	
		# China (Tibet)
		tTibetTL = (94, 42)
		tTibetBR = (97, 45)
		tManchuriaTL = (105, 51)
		tManchuriaBR = (109, 55)
		startingFlip(slot(iChina), [(tTibetTL, tTibetBR), (tManchuriaTL, tManchuriaBR)])
		
		# Russia (Sankt Peterburg)
		convertPlotCulture(plot(68, 58), slot(iRussia), 100, True)
		convertPlotCulture(plot(67, 57), slot(iRussia), 100, True)

def startingFlip(iPlayer, lRegionList):
	for tuple in lRegionList:
		tTL = tuple[0]
		tBR = tuple[1]
		tExceptions = []
		if len(tuple) > 2: tExceptions = tuple[2]
		convertSurroundingCities(iPlayer, plots.rectangle(tTL, tBR).without(tExceptions))
		convertSurroundingPlotCulture(iPlayer, plots.rectangle(tTL, tBR).without(tExceptions))

def adjustReligionFoundingDates():
	lReligionFoundingYears = [-2000, 40, 500, 1521, 622, -1500, 80, -500, -400, -600]

	for iReligion in range(iNumReligions):
		if game.isReligionFounded(iReligion):
			game.setReligionGameTurnFounded(iReligion, year(lReligionFoundingYears[iReligion]))

def initStartingReligions():
	if scenario() == i600AD:
		setStateReligionBeforeBirth(lCatholicStart, iCatholicism)
		setStateReligionBeforeBirth(lProtestantStart, iCatholicism)
		
	elif scenario() == i1700AD:
		setStateReligionBeforeBirth(lCatholicStart, iCatholicism)
		setStateReligionBeforeBirth(lProtestantStart, iProtestantism)
		
def createStartingUnits():
	scenarioStartingUnitFuncs = {
		i3000BC : create3000BCstartingUnits,
		i600AD : create600ADstartingUnits,
		i1700AD : create1700ADstartingUnits,
	}
	
	scenarioStartingUnitFuncs[scenario()]()
	
	if dBirth[active()] > scenarioStartYear():
		capital = plots.capital(active())
		makeUnit(active(), iSettler, capital)
		makeUnit(active(), iMilitia, capital)

def create3000BCstartingUnits():
	if data.isCivEnabled(iHarappa) or player(iHarappa).isHuman():
		capital = plots.capital(iHarappa)
		
		makeUnit(iHarappa, iCityBuilder, capital)
		makeUnit(iHarappa, iMilitia, capital)

def create600ADstartingUnits():
	# China
	capital = plots.capital(iChina)
	makeUnits(iChina, iSwordsman, capital, 2)
	makeUnit(iChina, iArcher, capital)
	makeUnit(iChina, iSpearman, capital, UnitAITypes.UNITAI_CITY_DEFENSE)
	makeUnits(iChina, iChokonu, capital, 2)
	makeUnit(iChina, iHorseArcher, capital)
	makeUnits(iChina, iWorker, capital, 2)
	
	# Japan
	capital = plots.capital(iJapan)
	tSeaPlot = findSeaPlots(capital, 1, iJapan)
	if tSeaPlot:
		makeUnits(iJapan, iWorkboat, tSeaPlot, 2)
		
	if not player(iJapan).isHuman():
		makeUnits(iJapan, iCrossbowman, capital, 2)
		makeUnits(iJapan, iSamurai, capital, 3)

	# Byzantium
	capital = plots.capital(iByzantium)
	tSeaPlot = findSeaPlots(capital, 1, iByzantium)
	if tSeaPlot:
		makeUnits(iByzantium, iGalley, tSeaPlot, 2)
		makeUnits(iByzantium, iWarGalley, tSeaPlot, 2)

	# Vikings
	capital = plots.capital(iVikings)
	tSeaPlot = findSeaPlots(capital, 1, iVikings)
	if tSeaPlot:
		makeUnit(iVikings, iWorkboat, tSeaPlot)
		if player(iVikings).isHuman():
			makeUnit(iVikings, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
			makeUnit(iVikings, iSettler, tSeaPlot)
			makeUnit(iVikings, iArcher, tSeaPlot)
			makeUnits(iVikings, iLongship, tSeaPlot, 2, UnitAITypes.UNITAI_EXPLORE_SEA)
		else:
			makeUnits(iVikings, iLongship, tSeaPlot, 3, UnitAITypes.UNITAI_EXPLORE_SEA)
			
	# start AI settler and garrison in Denmark and Sweden
	if not player(iVikings).isHuman():
		makeUnit(iVikings, iSettler, (60, 56))
		makeUnit(iVikings, iArcher, (60, 56))
		makeUnit(iVikings, iSettler, (63, 59))
		makeUnit(iVikings, iArcher, (63, 59))
	else:
		makeUnit(iVikings, iSettler, capital)
		makeUnits(iVikings, iArcher, capital, 2)

	# Korea
	capital = plots.capital(iKorea)
	if not player(iKorea).isHuman():
		makeUnits(iKorea, iHeavySwordsman, capital, 2)
	
	# Turks
	capital = plots.capital(iTurks)
	makeUnits(iTurks, iSettler, capital, 2)
	makeUnits(iTurks, iOghuz, capital, 6)
	makeUnit(iTurks, iArcher, capital)
	makeUnit(iTurks, iScout, capital)

def create1700ADstartingUnits():
	# Japan
	capital = plots.capital(iJapan)
	if not player(iJapan).isHuman():
		makeUnit(iJapan, iSettler, capital)
		
def adjustWonders():
	iScenario = scenario()

	dExpiredWonders = {
		i3000BC : [],
		i600AD :  [iOracle, iIshtarGate, iTerracottaArmy, iHangingGardens, iGreatCothon, 
				   iApadanaPalace, iColossus, iStatueOfZeus, iGreatMausoleum, iTempleOfArtemis, 
				   iAquaAppia, iAlKhazneh, iJetavanaramaya],
		i1700AD : [iOracle, iIshtarGate, iHangingGardens, iGreatCothon, iApadanaPalace, 
				   iColossus, iStatueOfZeus, iGreatMausoleum, iTempleOfArtemis, iAquaAppia, 
				   iAlKhazneh, iJetavanaramaya, iGreatLighthouse, iMoaiStatues, iFlavianAmphitheatre, 
				   iGreatLibrary, iGondeshapur, iSilverTreeFountain, iAlamut],
	}
	
	for iWonder in dExpiredWonders[iScenario]:
		game.incrementBuildingClassCreatedCount(infos.building(iWonder).getBuildingClassType())
	
	dWonderOriginalOwners = {
		iGreatLighthouse : iEgypt,
		iGreatLibrary : iEgypt,
		iPyramids : iEgypt,
		iGreatSphinx : iEgypt,
		iSalsalBuddha : iIndependent,
		iJewishShrine : iIndependent,
		iShwedagonPaya : iIndependent,
		iCatholicShrine : iIndependent,
		iTaoistShrine : iChina,
		iGreatWall : iChina,
		iConfucianShrine : iChina,
		iDujiangyan : iChina,
		iTerracottaArmy : iChina,
		iForbiddenPalace : iChina,
		iGrandCanal : iChina,
		iPorcelainTower : iChina,
		iParthenon : iGreece,
		iHinduShrine : iIndia,
		iBuddhistShrine : iIndia,
		iIronPillar : iIndia,
		iNalanda : iIndia,
		iVijayaStambha : iIndia,
		iKhajuraho : iIndia,
		iZoroastrianShrine : iPersia,
		iGondeshapur : iPersia,
		iFlavianAmphitheatre : iRome,
		iTempleOfKukulkan : iMaya,
		iMonolithicChurch : iEthiopia,
		iJetavanaramaya : iTamils,
		iCheomseongdae : iKorea,
		iOrthodoxShrine : iByzantium,
		iTheodosianWalls : iByzantium,
		iHagiaSophia : iByzantium,
		iMountAthos : iByzantium,
		iItsukushimaShrine : iJapan,
		iHimejiCastle : iJapan,
		iGurEAmir : iTurks,
		iDomeOfTheRock : iArabia,
		iSpiralMinaret : iArabia,
		iIslamicShrine : iArabia,
		iHouseOfWisdom : iArabia,
		iPotalaPalace : iTibet,
		iBorobudur : iIndonesia,
		iPrambanan : iIndonesia,
		iEscorial : iSpain,
		iMezquita : iMoors,
		iNotreDame : iFrance,
		iVersailles : iFrance,
		iLouvre : iFrance,
		iKrakDesChevaliers : iFrance,
		iWatPreahPisnulok : iKhmer,
		iOxfordUniversity : iEngland,
		iProtestantShrine : iHolyRome,
		iSaintThomasChurch : iHolyRome,
		iSaintSophia : iRussia,
		iKremlin : iRussia,
		iSaintBasilsCathedral : iRussia,
		iUniversityOfSankore : iMali,
		iOldSynagogue : iPoland,
		iTorreDeBelem : iPortugal,
		iSantaMariaDelFiore : iItaly,
		iSanMarcoBasilica : iItaly,
		iSistineChapel : iItaly,
		iFloatingGardens : iAztecs,
		iShalimarGardens : iMughals,
		iHarmandirSahib : iMughals,
		iTajMahal : iMughals,
		iRedFort : iMughals,
		iTopkapiPalace : iOttomans,
		iBlueMosque : iOttomans,
		iImageOfTheWorldSquare : iIran,
		iBourse : iNetherlands,
	}
	
	for iWonder, iCiv in dWonderOriginalOwners.items():
		city = getBuildingCity(iWonder, False)
		if city:
			city.setBuildingOriginalOwner(iWonder, slot(iCiv))
			
	if iScenario == i1700AD:
		player(iChina).updateTradeRoutes()

def adjustGreatPeople():
	dGreatPeopleCreated = {
		i3000BC : {},
		i600AD  : {
			iChina: 4,
			iKorea: 1,
			iByzantium: 1,
		},
		i1700AD : {
			iChina: 12,
			iIndia: 8,
			iPersia: 4,
			iTamils: 5,
			iKorea: 6,
			iJapan: 6,
			iVikings: 8,
			iTurks: 4,
			iSpain: 8,
			iFrance: 8,
			iEngland: 8,
			iHolyRome: 8,
			iPoland: 8,
			iPortugal: 8,
			iMughals: 8,
			iOttomans: 8,
			iThailand: 8,
			iCongo: 4,
			iNetherlands: 6,
		}
	}
	
	dGreatGeneralsCreated = {
		i3000BC : {},
		i600AD  : {
			iChina: 1,
		},
		i1700AD : {
			iChina: 4,
			iIndia: 3,
			iPersia: 2,
			iTamils: 2,
			iKorea: 3,
			iJapan: 3,
			iVikings: 3,
			iTurks: 3,
			iSpain: 4,
			iFrance: 3,
			iEngland: 3,
			iHolyRome: 4,
			iPoland: 3,
			iPortugal: 3,
			iMughals: 4,
			iOttomans: 5,
			iThailand: 3,
			iCongo: 2,
			iNetherlands: 3,
		}
	}
	
	iScenario = scenario()
	
	for iCiv, iGreatPeople in dGreatPeopleCreated[iScenario].iteritems():
		player(iCiv).changeGreatPeopleCreated(iGreatPeople)
		
	for iCiv, iGreatGenerals in dGreatGeneralsCreated[iScenario].iteritems():
		player(iCiv).changeGreatGeneralsCreated(iGreatGenerals)

def initDiplomacy():
	iScenario = scenario()
	
	if iScenario == i1700AD:
		team(iEngland).declareWar(slot(iMughals), False, WarPlanTypes.WARPLAN_LIMITED)
		team(iIndia).declareWar(slot(iMughals), False, WarPlanTypes.WARPLAN_TOTAL)

def prepareColonists():
	# TODO: unify all those lists for colonists, trading company conquerors, trading company corporation...
	dColonistsAlreadyGiven = {
		i3000BC : {},
		i600AD  : {},
		i1700AD : {
			iVikings : 1,
			iSpain : 7,
			iFrance : 3,
			iEngland : 3,
			iPortugal : 6,
			iNetherlands : 4,
		}
	}
	
	iScenario = scenario()
	iScenarioStartTurn = scenarioStartTurn()
	
	for iCiv, iColonists in dColonistsAlreadyGiven[iScenario].items():
		iPlayer = slot(iCiv)
		if iPlayer >= 0:
			data.players[iPlayer].iExplorationTurn = iScenarioStartTurn
			data.players[iPlayer].iColonistsAlreadyGiven = iColonists

def adjustCulture():
	iScenario = scenario()
	
	if iScenario == i1700AD:
		for plot in plots.all():
			if plot.getOwner() != -1:
				plot.changeCulture(plot.getOwner(), 100, False)
				convertPlotCulture(plot, plot.getOwner(), 100, True)
					
		for x, y in [(48, 45), (50, 44), (50, 43), (50, 42), (49, 40)]:
			convertPlotCulture(plot_(x, y), slot(iPortugal), 100, True)
			
		for x, y in [(58, 49), (59, 49), (60, 49)]:
			convertPlotCulture(plot_(x, y), slot(iGermany), 100, True)
			
		for x, y in [(62, 51)]:
			convertPlotCulture(plot_(x, y), slot(iHolyRome), 100, True)
			
		for x, y in [(58, 52), (58, 53)]:
			convertPlotCulture(plot_(x, y), slot(iNetherlands), 100, True)
			
		for x, y in [(64, 53), (66, 55), (68, 54), (68, 56)]:
			convertPlotCulture(plot_(x, y), slot(iPoland), 100, True)
			
		for x, y in [(67, 58), (68, 59), (69, 56), (69, 54)]:
			convertPlotCulture(plot_(x, y), slot(iRussia), 100, True)

def invalidateUHVs():
	for iPlayer in players.major():
		if not player(iPlayer).isPlayable():
			for i in range(3):
				data.players[iPlayer].lGoals[i] = 0

def updateExtraOptions():
	# Human player can switch infinite times
	data.bUnlimitedSwitching = infos.constant('UNLIMITED_SWITCHING') != 0
	# No congresses
	data.bNoCongresses = infos.constant('NO_CONGRESSES') != 0
	# No plagues
	data.bNoPlagues = infos.constant('NO_PLAGUES') != 0