from Events import handler
from RFCUtils import *
from Core import *
from Locations import *
from Stability import *
from CityNames import getName
from Popups import popup
from Scenarios import SCENARIOS


dRelocatedCapitals = CivDict({
	iPhoenicia : tCarthage,
	iMongols : tBeijing,
	iOttomans : tConstantinople
})

dCapitalInfrastructure = CivDict({
	iPhoenicia : (3, [], []),
	iByzantium : (5, [iBarracks, iWalls, iLibrary, iMarket, iGranary, iHarbor, iForge], [temple]),
	iPortugal : (5, [iLibrary, iMarket, iHarbor, iLighthouse, iForge, iWalls], [temple]),
	iItaly : (7, [iLibrary, iPharmacy, iMarket, iArtStudio, iAqueduct, iJail, iWalls], [temple]),
	iNetherlands : (9, [iLibrary, iMarket, iWharf, iLighthouse, iBarracks, iPharmacy, iBank, iArena, iTheatre], [temple]),
})


@handler("GameStart")
def updateCulture():
	for plot in plots.all():
		plot.updateCulture()


### CITY ACQUIRED ###

@handler("cityAcquired")
def relocateAcquiredCapital(iOwner, iPlayer, city):
	relocateCapitals(iPlayer, city)


@handler("cityAcquired")
def buildAcquiredCapitalInfrastructure(iOwner, iPlayer, city):
	buildCapitalInfrastructure(iPlayer, city)


### FIRST CITY ###

@handler("firstCity")
def createAdditionalPolishSettler(city):
	iPlayer = city.getOwner()
	if city.isCapital() and civ(iPlayer) == iPoland and not player(iPlayer).isHuman():
		locations = {
			tMemel: 1,
			tKoenigsberg: 1,
			tGdansk: 3,
		}
		
		location = weighted_random_entry(locations)
		
		makeUnit(iPlayer, iSettler, location)
		makeUnit(iPlayer, iCrossbowman, location)


@handler("firstCity")
def setupMexicoCity(city):
	if civ(city) == iMexico:
		if city.at(*tTenochtitlan):
			if game.getBuildingClassCreatedCount(infos.building(iFloatingGardens).getBuildingClassType()) == 0:
				city.setHasRealBuilding(iFloatingGardens, True)
			
			iStateReligion = player(city).getStateReligion()
			if iStateReligion >= 0 and city.isHasReligion(iStateReligion):
				city.setHasRealBuilding(monastery(iStateReligion), True)


### CITY BUILT ###

@handler("cityBuilt")
def relocateFoundedCapital(city):
	relocateCapitals(city.getOwner(), city)


@handler("cityBuilt")
def buildFoundedCapitalInfrastructure(city):
	buildCapitalInfrastructure(city.getOwner(), city)


@handler("cityBuilt")
def createEgyptianDefenses(city):
	if civ(city) == iEgypt and player(city.getOwner()).getNumCities() == 2 and player(iNubia).isHuman():
		makeUnit(city.getOwner(), iArcher, city)
	
	
@handler("cityBuilt")
def createCarthaginianDefenses(city):
	if at(city, tCarthage) and civ(city) == iPhoenicia and not player(city).isHuman():					
		makeUnit(iPhoenicia, iWorkboat, tCarthage, UnitAITypes.UNITAI_WORKER_SEA)
		makeUnit(iPhoenicia, iGalley, direction(tCarthage, DirectionTypes.DIRECTION_NORTHWEST), UnitAITypes.UNITAI_SETTLER_SEA)
		makeUnit(iPhoenicia, iSettler, direction(tCarthage, DirectionTypes.DIRECTION_NORTHWEST), UnitAITypes.UNITAI_SETTLE)
		
		if player(iRome).isHuman():
			city.setHasRealBuilding(iWalls, True)
			
			makeUnits(iPhoenicia, iArcher, tCarthage, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPhoenicia, iNumidianCavalry, tCarthage, 3)
			makeUnits(iPhoenicia, iWarElephant, tCarthage, 2, UnitAITypes.UNITAI_CITY_COUNTER)


@handler("cityBuilt")
def createColonialWorker(city):
	if not player(city).isHuman():
		capital_city = capital(city.getOwner())
		
		if capital_city and plot(city).getRegionGroup() != plot(capital_city).getRegionGroup():
			if plots.city_radius(city).any(lambda p: p.getBonusType(-1) >= 0 and p.getImprovementType() == -1):
				if plot(city).area().getNumAIUnits(city.getOwner(), UnitAITypes.UNITAI_WORKER) < plot(city).area().getCitiesPerPlayer(city.getOwner()):
					createRoleUnit(city.getOwner(), city, iWork)
			
			
### UNIT BUILT ###

@handler("unitBuilt")
def grantSettlerSea(city, unit):
	if unit.isFound() and not player(unit).isHuman():
		site = plots.sites(city).where(lambda p: p.getSettlerValue(civ(city)) >= 10 and p.isCoastalLand()).first()
		
		if site and city.plot().isCoastalLand():
			if player(unit).AI_totalUnitAIs(UnitAITypes.UNITAI_SETTLER_SEA) < player(unit).AI_totalUnitAIs(UnitAITypes.UNITAI_SETTLE) + 1:
				iBestTransport, _ = getUnitForRole(city.getOwner(), iSettleSea)
				
				if iBestTransport is not None:
					makeUnit(city.getOwner(), iBestTransport, city, UnitAITypes.UNITAI_SETTLER_SEA)


### BEGIN GAME TURN ###

@handler("BeginGameTurn")
def placeGoodyHuts(iGameTurn):
	if iGameTurn == scenarioStartTurn() + 3:
		for iScenario, scenario_definition in SCENARIOS.items():
			if scenario() <= iScenario:
				for tTL, tBR in scenario_definition.lTribalVillages:
					placeTribalVillage(tTL, tBR)


@handler("BeginGameTurn")
def createCarthaginianSettler(iGameTurn):
	if not player(iPhoenicia).isHuman() and iGameTurn == year(-820) - (data.iSeed % 10):
		makeUnit(iPhoenicia, iSettler, tCarthage)
		makeUnits(iPhoenicia, iArcher, tCarthage, 2)
		makeUnits(iPhoenicia, iWorker, tCarthage, 2)
		makeUnits(iPhoenicia, iWarElephant, tCarthage, 2)


# TODO: revisit how this works
@handler("BeginGameTurn")
def checkEarlyColonists():
	dEarlyColonistYears = {
		-850 : iGreece,
		-700 : iCarthage,
		-400 : iRome,
	}
	
	iYear = game.getGameTurnYear()
	if iYear in dEarlyColonistYears:
		iCiv = dEarlyColonistYears[iYear]
		giveEarlyColonists(iCiv)
		
		
@handler("BeginGameTurn")
def checkLateColonists():
	if year().between(1350, 1918):
		for iCiv in lLateColonyCivs:
			if player(iCiv).isExisting():
				iPlayer = slot(iCiv)
				if data.players[iPlayer].iExplorationTurn >= 0:
					if turn() == data.players[iPlayer].iExplorationTurn + 1 + data.players[iPlayer].iColonistsAlreadyGiven * 8:
						giveColonists(iPlayer)


@handler("BeginGameTurn")
def checkRaiders():
	if year().between(860, 1250):
		if turn() % turns(10) == 9:
			giveRaiders(iNorse)


### FIRST CONTACT ###

@handler("firstContact")
def conquistadors(iTeamX, iHasMetTeamY):
		if is_minor(iTeamX) or is_minor(iHasMetTeamY):
			return
		
		if year().between(600, 1800):
			if civ(iTeamX) in lBioNewWorld and civ(iHasMetTeamY) not in lBioNewWorld:
				iNewWorldPlayer = iTeamX
				iOldWorldPlayer = iHasMetTeamY
				
				if civ(iOldWorldPlayer) == iPolynesia:
					return
				
				iNewWorldCiv = civ(iNewWorldPlayer)
				
				if player(iNewWorldCiv).isBirthProtected():
					data.dFirstContactConquerors[iNewWorldCiv] = True
					return
				
				bAlreadyContacted = data.dFirstContactConquerors[iNewWorldCiv]
					
				if not bAlreadyContacted:
					if iNewWorldCiv in [iMaya, iToltecs, iAztecs]:
						tContactZoneTL = (11, 36)
						tContactZoneBR = (38, 49)
					elif iNewWorldCiv == iInca:
						tContactZoneTL = (21, 13)
						tContactZoneBR = (35, 40)

					lArrivalExceptions = [(27, 47), (27, 48), (26, 48), (26, 49), (22, 49), (21, 49), (20, 49), (25, 37), (26, 36), (27, 37)]
						
					data.dFirstContactConquerors[iNewWorldCiv] = True
					
					events.fireEvent("conquerors", iOldWorldPlayer, iNewWorldPlayer)
					
					newWorldPlots = plots.start(tContactZoneTL).end(tContactZoneBR).without(lArrivalExceptions)
					contactPlots = newWorldPlots.where(lambda p: p.isVisible(iNewWorldPlayer, False) and p.isVisible(iOldWorldPlayer, False))
					arrivalPlots = newWorldPlots.owner(iNewWorldPlayer).where(lambda p: not p.isCity() and isFree(iOldWorldPlayer, p, bCanEnter=True) and map.getArea(p.getArea()).getCitiesPerPlayer(iNewWorldPlayer) > 0)
					
					if contactPlots and arrivalPlots:
						contactPlot = contactPlots.random()
						arrivalPlot = arrivalPlots.closest(contactPlot)
						
						iModifier1 = 0
						iModifier2 = 0
						
						if player(iNewWorldPlayer).isHuman() and player(iNewWorldPlayer).getNumCities() > 6:
							iModifier1 = 1
						else:
							if iNewWorldCiv == iInca or player(iNewWorldPlayer).getNumCities() > 4:
								iModifier1 = 1
							if not player(iNewWorldPlayer).isHuman():
								iModifier2 = 1
								
						if year() < year(dBirth[active()]):
							iModifier1 += 1
							iModifier2 += 1
							
						team(iOldWorldPlayer).declareWar(iNewWorldPlayer, True, WarPlanTypes.WARPLAN_TOTAL)
						
						dConquerorUnits = {
							iAttack: 1 + iModifier2,
							iCounter: 2,
							iSiege: 1 + iModifier1 + iModifier2,
							iShockCity: 2 + iModifier1,
						}
						units = createRoleUnits(iOldWorldPlayer, arrivalPlot, dConquerorUnits.items())
						units.promotion(infos.type("PROMOTION_MERCENARY"))
						
						iStateReligion = player(iOldWorldPlayer).getStateReligion()
						iMissionary = missionary(iStateReligion)
						
						if iMissionary:
							makeUnit(iOldWorldPlayer, iMissionary, arrivalPlot)
							
						if iNewWorldCiv == iInca:
							makeUnits(iOldWorldPlayer, iAucac, arrivalPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
						elif iNewWorldCiv == iAztecs:
							makeUnits(iOldWorldPlayer, iJaguar, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
							makeUnit(iOldWorldPlayer, iHolkan, arrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY)
						elif iNewWorldCiv == iMaya:
							makeUnits(iOldWorldPlayer, iHolkan, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
							makeUnit(iOldWorldPlayer, iJaguar, arrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY)
							
						message(iNewWorldPlayer, 'TXT_KEY_FIRST_CONTACT_NEWWORLD')
						message(iOldWorldPlayer, 'TXT_KEY_FIRST_CONTACT_OLDWORLD')


@handler("firstContact")
def firstContactMongolConquerors(iTeamX, iHasMetTeamY):
	if civ(iHasMetTeamY) == iMongols and not player(iMongols).isHuman():
		mongolConquerors(iTeamX)


@handler("flip")
def flipMongolConquerors(iPlayer):
	if civ(iPlayer) == iMongols and not player(iPlayer).isHuman():
		for iOtherPlayer in players.major().existing().without(iPlayer):
			if player(iPlayer).canContact(iOtherPlayer):
				mongolConquerors(player(iOtherPlayer).getTeam())


def mongolConquerors(iTargetTeam):
	iTargetCiv = civ(iTargetTeam)

	if iTargetCiv in lMongolCivs:
		if year() < year(1500) and player(iMongols).getNumCities() > 0 and data.isFirstContactMongols(iTargetCiv):
			data.setFirstContactMongols(iTargetCiv, False)

			teamTarget = team(iTargetTeam)
			
			mongol_area = plots.rectangle((70, 39), (86, 58))
			
			mongol_cities = cities.owner(iMongols)
			target_cities = mongol_area.cities().owner(iTargetCiv)
			lTargetCities = [(mongol_cities.closest(target_city), target_city) for target_city in target_cities]
			lSelectedTargets = sorted(lTargetCities, key=lambda (mongol_city, target_city): distance(mongol_city, target_city))[:3]
			
			if not lSelectedTargets:
				return

			team(iMongols).declareWar(iTargetTeam, True, WarPlanTypes.WARPLAN_TOTAL)
			
			iHandicap = 0
			if teamtype(iTargetTeam).isHuman():
				iHandicap = game.getHandicapType() / 2
			
			for mongol_city, target_city in lSelectedTargets:
				tSpawn = possibleSpawnsBetween(mongol_city, target_city, iDistance=3).closest(target_city)
				
				makeUnits(iMongols, iKeshik, tSpawn, 2 + iHandicap, UnitAITypes.UNITAI_ATTACK_CITY)
				makeUnits(iMongols, iMangudai, tSpawn, 1 + 2 * iHandicap, UnitAITypes.UNITAI_ATTACK_CITY)
				makeUnits(iMongols, iTrebuchet, tSpawn, 1 + iHandicap, UnitAITypes.UNITAI_ATTACK_CITY)
				
			message(iTargetTeam, 'TXT_KEY_MONGOL_HORDE_HUMAN')
			if team().canContact(iTargetTeam):
				message(active(), 'TXT_KEY_MONGOL_HORDE', adjective(iTargetTeam))


### TECH ACQUIRED ###

@handler("techAcquired")
def recordExplorationTurn(iTech, iTeam, iPlayer):
	if iTech == iExploration:
		data.players[iPlayer].iExplorationTurn = game.getGameTurn()


@handler("techAcquired")
def americanWestCoastSettlement(iTech, iTeam, iPlayer):
	if iTech == iRailroad and civ(iPlayer) == iAmerica and not player(iPlayer).isHuman():
		enemyCities = cities.region(rCalifornia).notowner(iAmerica)
		
		for iEnemy in enemyCities.owners():
			team(iPlayer).declareWar(iEnemy, True, WarPlanTypes.WARPLAN_LIMITED)
		
		for city in enemyCities:
			plot = plots.surrounding(city).without(city).land().passable().no_enemies(iPlayer).random()
			if plot:
				createRoleUnit(iPlayer, plot, iCityAttack, 3)
				createRoleUnit(iPlayer, plot, iCitySiege, 2)
				
				message(city.getOwner(), "TXT_KEY_MESSAGE_AMERICAN_WEST_COAST_CONQUERORS", adjective(iPlayer), city.getName(), color=iRed, location=city, button=infos.unit(iMinuteman).getButton())
				
		if enemyCities.count() < 2:
			for plot in plots.region(rCalifornia).coastal().without(enemyCities).highest(2 - enemyCities.count(), metric=lambda p: p.getSettlerValue(iAmerica)):
				createRoleUnit(iPlayer, plot, iSettle)
				createRoleUnit(iPlayer, plot, iDefend)


@handler("techAcquired")
def russianSiberianSettlement(iTech, iTeam, iPlayer):
	if iTech == iRailroad and civ(iPlayer) == iRussia and not player(iPlayer).isHuman():
		siberiaPlot = plots.region(rAmur).coastal().maximum(lambda p: p.getSettlerValue(iRussia))
		
		convertPlotCulture(siberiaPlot, iPlayer, 100, True)
		
		if siberiaPlot.isCity() and siberiaPlot.getOwner() != iPlayer:
			spawnPlot = plots.surrounding(siberiaPlot).land().passable().where(lambda p: not p.isCity()).random()
			
			team(iTeam).declareWar(siberiaPlot.getTeam(), True, WarPlanTypes.WARPLAN_LIMITED)
			
			createRoleUnit(iPlayer, spawnPlot, iCityAttack, 4)
			createRoleUnit(iPlayer, spawnPlot, iCitySiege, 2)
			
			message(siberiaPlot.getOwner(), "TXT_KEY_MESSAGE_RUSSIAN_SIBERIAN_CONQUERORS", adjective(iPlayer), siberiaPlot.getPlotCity().getName(), color=iRed, location=siberiaPlot, button=infos.unit(iRifleman).getButton())
			
		elif isFree(iPlayer, siberiaPlot, True):
			player(iPlayer).found(*location(siberiaPlot))
			createRoleUnit(iPlayer, siberiaPlot, iDefend, 2)
			
			for plot in plots.surrounding(siberiaPlot):
				convertPlotCulture(plot, iPlayer, 80, True)


@handler("techAcquired")
def earlyTradingCompany(iTech, iTeam, iPlayer):
	if turn() == scenarioStartTurn():
		return

	lCivs = [iSpain, iPortugal]
	lTechs = [iExploration, iFirearms]
	
	if civ(iPlayer) in lCivs:
		if iTech in lTechs and all(team(iTeam).isHasTech(iTech) for iTech in lTechs):
			if not player(iPlayer).isHuman() and not team(iTeam).isAVassal():
				handleColonialAcquisition(iPlayer)


@handler("techAcquired")
def lateTradingCompany(iTech, iTeam, iPlayer):
	if turn() == scenarioStartTurn():
		return

	lCivs = [iFrance, iEngland, iNetherlands]
	lTechs = [iEconomics, iReplaceableParts]
	
	if civ(iPlayer) in lCivs:
		if iTech in lTechs and all(team(iTeam).isHasTech(iTech) for iTech in lTechs):
			if not player(iPlayer).isHuman() and not team(iTeam).isAVassal():
				handleColonialConquest(iPlayer)


### COLLAPSE ###

@handler("collapse")
def removeOrthodoxyFromAnatolia(iPlayer):
	if civ(iPlayer) == iByzantium:
		removeReligionByArea(plots.region(rAnatolia), iOrthodoxy)


### BIRTH ###

@handler("birth")
def romanRelations(iPlayer):
	if civ(iPlayer) == iByzantium and player(iRome).isExisting():
		iRomePlayer = slot(iRome)
		player(iRomePlayer).AI_changeMemoryCount(iPlayer, MemoryTypes.MEMORY_EVENT_GOOD_TO_US, 4)


@handler("birth")
def stabilizeAustria(iPlayer):
	if civ(iPlayer) == iGermany:
		iHolyRomanPlayer = slot(iHolyRome)

		if iHolyRomanPlayer >= 0 and stability(iHolyRomanPlayer) < iStabilityShaky:
			data.setStabilityLevel(iHolyRomanPlayer, iStabilityShaky)
			

### FLIP ###

@handler("flip")
def createArabArmies(iPlayer):
	if civ(iPlayer) == iArabia:
		bBaghdad = civ(plot(tBaghdad)) == iArabia
		bCairo = civ(plot(tCairo)) == iArabia

		lCities = []

		if bBaghdad: lCities.append(tBaghdad)
		if bCairo: lCities.append(tCairo)

		tCapital = random_entry(lCities)

		if tCapital:
			if not player(iArabia).isHuman():
				relocateCapital(iArabia, tCapital)
				makeUnits(iArabia, iMobileGuard, tCapital, 3)
				makeUnits(iArabia, iGhazi, tCapital, 2)
			makeUnits(iArabia, iMobileGuard, tCapital, 2)
			makeUnits(iArabia, iGhazi, tCapital, 2)

		if bBaghdad:
			makeUnit(iArabia, iSettler, tBaghdad)
			makeUnit(iArabia, iWorker, tBaghdad)

		if bCairo:
			makeUnit(iArabia, iSettler, tCairo)
			makeUnit(iArabia, iWorker, tCairo)
			
		if len(lCities) < 2:
			makeUnits(iArabia, iSettler, tMecca, 2 - len(lCities))
			makeUnits(iArabia, iWorker, tMecca, 2 - len(lCities))

		if not player(iArabia).isHuman() and bBaghdad:
			makeUnits(iArabia, iSpearman, tBaghdad, 2)
	

@handler("flip")
def flipMoorishMaghreb(iPlayer):
	if civ(iPlayer) == iMoors:
		city = cities.owner(iPlayer).region(rMaghreb).random()
		
		if city:
			city.setHasReligion(iIslam, True, False, False)
			
			makeUnit(iPlayer, iSettler, city)
			makeUnit(iPlayer, iWorker, city)


### PERIOD CHANGE ###


@handler("playerPeriodChange")
def relocateCelts(iPlayer, iPeriod):
	if iPeriod == iPeriodInsularCelts:
		newCapital = cities.owner(iCelts).matching(lambda city: city.getRegionID() == rIreland, lambda city: city.getRegionID() == rBritain, lambda city: city not in cities.birth(iFrance)).random()
		
		if not newCapital and not player(iPlayer).isHuman():
			completeCollapse(iPlayer)
			return
		
		relocateCapital(iPlayer, newCapital)
		
		ahistoricalCities = cities.owner(iCelts).where(lambda city: plot(city).getPlayerSettlerValue(iPlayer) == 0)
		if ahistoricalCities:
			secedeCities(iPlayer, ahistoricalCities)
		
		data.players[iPlayer].resetStability()


### PREPARE BIRTH ###

@handler("prepareBirth")
def prepareKushanBirth(iCiv):
	if iCiv == iKushans:
		for plot in plots.of(lKushanRoad):
			plot.setRouteType(iRouteRoad)


### IMPLEMENTATION ###

def relocateCapitals(iPlayer, city):
	if player(iPlayer).isHuman():
		return
	
	if iPlayer in dRelocatedCapitals:
		tCapital = dRelocatedCapitals[iPlayer]
		
		if location(city) == tCapital:
			relocateCapital(iPlayer, tCapital)
			
	if civ(iPlayer) == iTurks and isControlled(iPlayer, plots.core(iPersia)):
		capital = player(iPlayer).getCapitalCity()
		if capital not in plots.core(iPersia):
			newCapital = cities.core(iPersia).owner(iPlayer).random()
			if newCapital:
				relocateCapital(iPlayer, location(newCapital))


def buildCapitalInfrastructure(iPlayer, city):
	if iPlayer in dCapitalInfrastructure:
		if at(city, plots.capital(iPlayer)) and year() <= year(dBirth[iPlayer]) + turns(5):
			iPopulation, lBuildings, lReligiousBuildings = dCapitalInfrastructure[iPlayer]
			
			if city.getPopulation() < iPopulation:
				city.setPopulation(iPopulation)
			
			for iBuilding in lBuildings:
				city.setHasRealBuilding(iBuilding, True)
			
			iStateReligion = player(iPlayer).getStateReligion()
			if iStateReligion >= 0:
				for religiosBuilding in lReligiousBuildings:
					city.setHasRealBuilding(religiosBuilding(iStateReligion), True)
					
					
def giveEarlyColonists(iCiv):
	pPlayer = player(iCiv)
	
	if pPlayer.isExisting() and not pPlayer.isHuman():
		capital = pPlayer.getCapitalCity()

		if iCiv == iRome:
			capital = cities.owner(iCiv).region(rIberia).random()
			
		if capital:
			tSeaPlot = findSeaPlots(capital, 1, iCiv)
			if tSeaPlot:
				makeUnit(iCiv, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iCiv, iSettler, tSeaPlot)
				makeUnit(iCiv, iArcher, tSeaPlot)


def giveColonists(iPlayer):
	pPlayer = player(iPlayer)
	pTeam = team(iPlayer)
	iCiv = civ(iPlayer)
	
	if pPlayer.isExisting() and not pPlayer.isHuman() and iCiv in dMaxColonists:
		if pTeam.isHasTech(iExploration) and data.players[iPlayer].iColonistsAlreadyGiven < dMaxColonists[iCiv]:
			sourceCities = cities.core(iCiv).owner(iPlayer)
			
			# help England with settling Canada and Australia
			if iCiv == iEngland:
				colonialCities = cities.regions(rOntario, rMaritimes, rAustralia).owner(iPlayer)
				if colonialCities:
					sourceCities = colonialCities
					
			city = sourceCities.coastal().random()
			if city:
				tSeaPlot = findSeaPlots(city, 1, iCiv)
				if not tSeaPlot: tSeaPlot = city
				
				makeUnit(iPlayer, unique_unit(iPlayer, iGalleon), tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot, UnitAITypes.UNITAI_SETTLE)
				createRoleUnit(iPlayer, tSeaPlot, iDefend, 1)
				makeUnit(iPlayer, iWorker, tSeaPlot)
				
				data.players[iPlayer].iColonistsAlreadyGiven += 1


def giveRaiders(iCiv):
	pPlayer = player(iCiv)
	pTeam = team(iCiv)
	
	if pPlayer.isExisting() and not pPlayer.isHuman():
		city = cities.owner(iCiv).coastal().random()
		if city:
			seaPlot = findSeaPlots(location(city), 1, iCiv)
			if seaPlot:
				makeUnit(iCiv, unique_unit(iCiv, iGalley), seaPlot, UnitAITypes.UNITAI_ASSAULT_SEA)
				if pTeam.isHasTech(iSteel):
					makeUnit(iCiv, unique_unit(iCiv, iHeavySwordsman), seaPlot, UnitAITypes.UNITAI_ATTACK)
					makeUnit(iCiv, unique_unit(iCiv, iHeavySwordsman), seaPlot, UnitAITypes.UNITAI_ATTACK_CITY)
				else:
					makeUnit(iCiv, unique_unit(iCiv, iSwordsman), seaPlot, UnitAITypes.UNITAI_ATTACK)
					makeUnit(iCiv, unique_unit(iCiv, iSwordsman), seaPlot, UnitAITypes.UNITAI_ATTACK_CITY)

def acceptColonialAcquisition(iPlayer):
	for city in data.players[iPlayer].colonialAcquisitionCities:
		if city.isHuman():
			colonialAcquisition(iPlayer, city)
			
	player().changeGold(data.players[iPlayer].colonialAcquisitionCities.count() * 200)

def refuseColonialAcquisition(iPlayer):
	for city in data.players[iPlayer].colonialAcquisitionCities:
		if city.isHuman():
			colonialConquest(iPlayer, city)

colonialAcquisitionPopup = popup.text("TXT_KEY_ASKCOLONIALCITY_MESSAGE") \
							.option(acceptColonialAcquisition, "TXT_KEY_POPUP_YES") \
							.option(refuseColonialAcquisition, "TXT_KEY_POPUP_NO") \
							.build()

def handleColonialAcquisition(iPlayer):
	pPlayer = player(iPlayer)
	iCiv = civ(iPlayer)
	
	targets = getColonialTargets(iPlayer, bEmpty=True)
	if not targets:
		return
	
	iGold = targets.count() * 200
	
	targetPlayers = targets.cities().owners()
	freePlots, cityPlots = targets.split(lambda plot: not city(plot))
	
	for plot in freePlots:
		colonialAcquisition(iPlayer, plot)

	for iTarget in targetPlayers:
		if player(iTarget).isHuman():
			askedCities = cityPlots.cities().owner(iTarget)
			askedCityNames = askedCities.format(formatter=CyCity.getName)
					
			iAskGold = askedCities.count() * 200
			
			data.players[iPlayer].colonialAcquisitionCities = askedCities
			colonialAcquisitionPopup.text(adjective(iPlayer), adjective(iPlayer), iAskGold, askedCityNames) \
				.acceptColonialAcquisition() \
				.refuseColonialAcquisition() \
				.launch(iPlayer)
			
		else:
			bAccepted = is_minor(iTarget) or (rand(100) >= dPatienceThreshold[iTarget] and not team(iPlayer).isAtWar(iTarget))
			iNumCities = targets.cities().owner(iTarget).count()
					
			if iNumCities >= player(iTarget).getNumCities():
				bAccepted = False
			
			for plot in targets.cities().owner(iTarget):
				if bAccepted:
					colonialAcquisition(iPlayer, plot)
					player(iTarget).changeGold(200)
				else:
					data.timedConquest(iPlayer, location(plot))

	iNewGold = pPlayer.getGold() - iGold
	pPlayer.setGold(max(0, iNewGold))


def handleColonialConquest(iPlayer):
	targets = getColonialTargets(iPlayer)
	
	if not targets:
		handleColonialAcquisition(iPlayer)
		return

	for plot in targets:
		data.timedConquest(iPlayer, location(plot))
		
	seaPlot = plots.surrounding(targets[0]).water().random()

	if seaPlot:
		makeUnit(iPlayer, unique_unit(iPlayer, iGalleon), seaPlot)


def placeTribalVillage(tTL, tBR):
	plot = plots.rectangle(tTL, tBR).where(lambda p: not p.isWater() and not p.isPeak() and p.getFeatureType() != iMud and p.getBonusType(-1) == -1).where(lambda p: not p.isOwned()).random()

	if plot:
		plot.setImprovementType(iHut)