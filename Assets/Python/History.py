from Events import handler
from RFCUtils import *
from Core import *
from Locations import *
from Stability import *
from AIWars import iAlexanderYear
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
	iItaly : (7, [iLibrary, iMarket, iArtStudio, iAqueduct, iJail, iWalls], [temple]),
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


@handler("cityAcquired")
def openGibraltar(iOwner, iPlayer, city):
	if at(city, plots.capital(iMoors)) and civ(iPlayer) in dCivGroups[iCivGroupEurope] and civ(iOwner) == iMoors:
		for tile in lStraitOfGibraltar:
			if cities.surrounding(tile, radius=2).owner(iPlayer):
				convertPlotCulture(tile, slot(iSpain), 100, True) 


@handler("cityAcquired")
def conquistadorCapital(iOwner, iPlayer, city):
	if city.getRegionID() in lAmerica and civ(iOwner) in lBioNewWorld and civ(iPlayer) not in lBioNewWorld and data.dFirstContactConquerors[civ(iOwner)]:
		if cities.regions(*lAmerica).none(lambda c: c.isHasRealBuilding(iAdministrativeCenter)):
			city.setHasRealBuilding(iAdministrativeCenter, True)


### FIRST CITY ###

@handler("firstCity")
def createHejazRoad(city):
	if civ(city) == iArabia:
		for plot in plots.of(lHejazRoad):
			plot.setRouteType(iRouteRoad)


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
	if year().between(1350, 1918) and any(data.dFirstContactConquerors.values()):
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


@handler("BeginGameTurn")
def createSilkRoute():
	if year() == year(-75):
		for plot in plots.of(lSilkRoute):
			plot.setRouteType(iRouteRoad)


@handler("BeginGameTurn")
def createMacedonianRoad():
	if year() == year(iAlexanderYear) and not player(iGreece).isHuman():
		for plot in plots.of(lMacedonianRoad):
			plot.setRouteType(iRouteRoad)


### BEGIN PLAYER TURN ###


@handler("BeginPlayerTurn")
def earlyArmies(iGameTurn, iPlayer):
	if iGameTurn == year(-1200):
		if not player(iPlayer).isHuman():
			if civ(iPlayer) == iHittites:
				createRoleUnit(iPlayer, capital(iPlayer), iShockCity, 2)
			elif civ(iPlayer) == iAssyria:
				createRoleUnit(iPlayer, capital(iPlayer), iDefend)
				createRoleUnit(iPlayer, capital(iPlayer), iCityAttack)
				createRoleUnit(iPlayer, capital(iPlayer), iSiege)


@handler("BeginPlayerTurn")
def nativeConquerors(iGameTurn, iPlayer):
	if is_minor(iPlayer):
		return
	
	if none(data.dFirstContactConquerors[iCiv] for iCiv in (iMaya, iToltecs, iAztecs)):
		if checkNativeConquerors(iPlayer, tMesoamericanContactZone):
			for iCiv in (iMaya, iToltecs, iAztecs):
				data.dFirstContactConquerors[iCiv] = True
	
	if not data.dFirstContactConquerors[iInca]:
		if checkNativeConquerors(iPlayer, tAndeanContactZone):
			data.dFirstContactConquerors[iInca] = True
	

def checkNativeConquerors(iPlayer, tContactZone):
	newWorldPlots = plots.rectangle(tContactZone).without(lContactZoneExceptions)
	
	if newWorldPlots.owners().major():
		return
	
	return conquistadors(iPlayer, slot(iNative), newWorldPlots)


### FIRST CONTACT ###

@handler("firstContact")
def firstContactConquistadors(iTeamX, iHasMetTeamY):
		if is_minor(iTeamX) or is_minor(iHasMetTeamY):
			return
		
		if year().between(600, 1800):
			if civ(iTeamX) in lBioNewWorld and civ(iHasMetTeamY) not in lBioNewWorld:
				iNewWorldPlayer = iTeamX
				iOldWorldPlayer = iHasMetTeamY
				
				if civ(iOldWorldPlayer) == iPolynesia:
					return
				
				iNewWorldCiv = civ(iNewWorldPlayer)
				
				if player(iNewWorldPlayer).isBirthProtected():
					data.dFirstContactConquerors[iNewWorldCiv] = True
					return
				
				bAlreadyContacted = data.dFirstContactConquerors[iNewWorldCiv]
					
				if not bAlreadyContacted:
					if iNewWorldCiv in [iMaya, iToltecs, iAztecs]:
						tContactZone = tMesoamericanContactZone
					elif iNewWorldCiv == iInca:
						tContactZone = tAndeanContactZone

					data.dFirstContactConquerors[iNewWorldCiv] = True
					
					if iNewWorldCiv in [iToltecs, iAztecs]:
						data.dFirstContactConquerors[iToltecs] = True
						data.dFirstContactConquerors[iAztecs] = True
					
					newWorldPlots = plots.rectangle(tContactZone)
					
					conquistadors(iOldWorldPlayer, iNewWorldPlayer, newWorldPlots)


def conquistadors(iOldWorldPlayer, iNewWorldPlayer, newWorldPlots):
	iOldWorldCiv = civ(iOldWorldPlayer)
	iNewWorldCiv = civ(iNewWorldPlayer)
	
	contactPlots = newWorldPlots.where(lambda p: p.isVisible(iNewWorldPlayer, False) and p.isVisible(iOldWorldPlayer, False))
	controlPlots = is_minor(iNewWorldPlayer) and newWorldPlots or plots.core(iNewWorldPlayer).expand(1)
	arrivalPlots = controlPlots.coastal().where(lambda p: not p.isCity() and isFree(iOldWorldPlayer, p, bCanEnter=True) and map.getArea(p.getArea()).getCitiesPerPlayer(iNewWorldPlayer) > 0)
	
	if contactPlots and arrivalPlots:
		contactPlot = contactPlots.random()
		arrivalPlot = arrivalPlots.closest(contactPlot)
		
		iModifier1 = 0
		iModifier2 = 0
		
		iTargetCities = not is_minor(iNewWorldPlayer) and player(iNewWorldPlayer).getNumCities() or 0
		
		if player(iNewWorldPlayer).isHuman() and iTargetCities > 6:
			iModifier1 = 1
		else:
			if iNewWorldCiv == iInca or iTargetCities > 4:
				iModifier1 = 1
			if not player(iNewWorldPlayer).isHuman():
				iModifier2 = 1
				
		if year() < year(dBirth[active()]):
			iModifier1 += 1
			iModifier2 += 1
		
		if not team(iOldWorldPlayer).isAtWar(iNewWorldPlayer):
			team(iOldWorldPlayer).declareWar(iNewWorldPlayer, True, WarPlanTypes.WARPLAN_TOTAL)
		
		if not player(iOldWorldPlayer).isHuman() and not is_minor(iNewWorldPlayer):
			player(iOldWorldPlayer).AI_changeMemoryCount(iNewWorldPlayer, MemoryTypes.MEMORY_STOPPED_TRADING_RECENT, turns(10))
		
		dConquerorUnits = {
			iCityAttack: 3 + iModifier2,
			iDefend: max(1, iTargetCities-2),
			iCitySiege: 2 + iModifier1 + iModifier2,
			iShockCity: 1 + iModifier1,
		}
		createRoleUnits(iOldWorldPlayer, arrivalPlot, dConquerorUnits.items()).promotion(iMercenary)
		createRoleUnit(iOldWorldPlayer, arrivalPlot, iWork, iTargetCities-1)
		
		iStateReligion = player(iOldWorldPlayer).getStateReligion()
		iMissionary = missionary(iStateReligion)
		
		if iMissionary:
			makeUnit(iOldWorldPlayer, iMissionary, arrivalPlot)
			
		if iNewWorldCiv == iInca:
			makeUnits(iOldWorldPlayer, iAucac, arrivalPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
		elif iNewWorldCiv == iAztecs:
			makeUnits(iOldWorldPlayer, iJaguar, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnit(iOldWorldPlayer, iHolkan, arrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY)
		elif iNewWorldCiv == iToltecs:
			makeUnits(iOldWorldPlayer, iAtlatl, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnit(iOldWorldPlayer, iHolkan, arrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY)
		elif iNewWorldCiv == iMaya:
			makeUnits(iOldWorldPlayer, iHolkan, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnit(iOldWorldPlayer, iJaguar, arrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY)
		
		for plot in newWorldPlots.land().where(lambda p: p.getOwner() == iNewWorldPlayer or (p.isOwned() and is_minor(p))):
			if plot.getWarValue(iOldWorldCiv) == 0:
				plot.setWarValue(iOldWorldCiv, 1)
				
		events.fireEvent("conquerors", iOldWorldPlayer, iNewWorldPlayer)
			
		message(iNewWorldPlayer, 'TXT_KEY_FIRST_CONTACT_NEWWORLD')
		message(iOldWorldPlayer, 'TXT_KEY_FIRST_CONTACT_OLDWORLD')
		
		return True


@handler("firstContact")
def firstContactMongolConquerors(iTeamX, iHasMetTeamY):
	if not scenarioStartTurn() and civ(iHasMetTeamY) == iMongols and civ() != iMongols and since(player(iMongols).getLastBirthTurn()) >= 2:
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
			
			lMongolRegions = [rLevant, rMesopotamia, rAnatolia, rCaucasus, rPersia, rKhorasan, rPonticSteppe, rRuthenia]
			
			mongol_cities = cities.owner(iMongols)
			target_cities = cities.regions(*lMongolRegions).owner(iTargetCiv)
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
def spanishExplorers(iTech, iTeam, iPlayer):
	if iTech == iCartography:
		if civ(iPlayer) == iSpain and not player(iPlayer).isHuman():
			city = cities.owner(iPlayer).coastal().minimum(CyCity.getX)
			if city:
				caravel = makeUnit(iPlayer, iCaravel, city, UnitAITypes.UNITAI_EXPLORE_SEA)


@handler("techAcquired")
def americanWestCoastSettlement(iTech, iTeam, iPlayer):
	if iTech == iRailroad and civ(iPlayer) == iAmerica and not player(iPlayer).isHuman():
		enemyCities = cities.region(rCalifornia).notowner(iAmerica).where(lambda city: team(iTeam).canDeclareWar(city.getTeam()))
		
		for iEnemy in enemyCities.owners():
			team(iPlayer).declareWar(iEnemy, True, WarPlanTypes.WARPLAN_LIMITED)
		
		for city in enemyCities:
			plot = plots.surrounding(city).without(city).land().passable().no_enemies(iPlayer).random()
			if plot:
				createRoleUnit(iPlayer, plot, iCityAttack, 3)
				createRoleUnit(iPlayer, plot, iCitySiege, 2)
				
				message(city.getOwner(), "TXT_KEY_MESSAGE_AMERICAN_WEST_COAST_CONQUERORS", adjective(iPlayer), city.getName(), color=iRed, location=city, button=infos.unit(iPioneer).getButton())
				
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
	
	if data.civs[iPlayer].iResurrections > 0:
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
	
	if data.civs[iPlayer].iResurrections > 0:
		return

	lCivs = [iFrance, iEngland, iNetherlands]
	lTechs = [iEconomics, iReplaceableParts]
	
	if civ(iPlayer) in lCivs:
		if iTech in lTechs and all(team(iTeam).isHasTech(iTech) for iTech in lTechs):
			if not player(iPlayer).isHuman() and not team(iTeam).isAVassal():
				handleColonialConquest(iPlayer)


@handler("techAcquired")
def minorNativeStates(iTech):
	if iTech == iNationalism and game.countKnownTechNumTeams(iNationalism) == 6:
		for iMinor, minorCities in cities.owner(iNative).divide([iIndependent, iIndependent2]):
			for city in minorCities:
				completeCityFlip(city, iMinor, iNative, 100, bFlipUnits=True)


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
		
		coastal_city = cities.owner(iArabia).coastal().adjacent_region(rMediterraneanSea).random()
		if coastal_city:
			createRoleUnit(iArabia, coastal_city, iEscort, 2)
			createRoleUnit(iArabia, coastal_city, iExploreSea, 1)
			createRoleUnit(iArabia, coastal_city, iFerry, 1)
	

@handler("flip")
def flipMoorishMaghreb(iPlayer):
	if civ(iPlayer) == iMoors:
		city = cities.owner(iPlayer).region(rMaghreb).random()
		
		if city:
			city.setHasReligion(iIslam, True, False, False)
			
			makeUnit(iPlayer, iSettler, city)
			makeUnit(iPlayer, iWorker, city)


@handler("flip")
def stabilizeRomeAfterByzantium(iPlayer):
	if civ(iPlayer) == iByzantium:
		if player(iRome).isExisting():
			data.players[iRome].iNumPreviousCities = player(iRome).getNumCities()


@handler("flip")
def westernMongolExplorers(iPlayer):
	if civ(iPlayer) == iMongols:
		if not player(iPlayer).isHuman():
			city = cities.owner(iPlayer).minimum(CyCity.getX)
			if city:
				createRoleUnit(iPlayer, city, iExplore)


@handler("flip")
def removeBarbariansForMongols(iPlayer):
	if civ(iPlayer) == iMongols:
		lRegions = [rManchuria, rMongolia, rSiberia]
		if not player(iPlayer).isHuman():
			lRegions += [rCentralAsianSteppe, rUrals, rPonticSteppe]
		
		for unit in plots.regions(*lRegions).notowned().units().owner(iBarbarian):
			unit.kill(False, -1)


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
			city = cities.owner(iCiv).region(rIberia).random()
			if city:
				capital = city
			
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
	
	iMiddleAtlantic = 45
	
	if pPlayer.isExisting() and not pPlayer.isHuman() and iCiv in dMaxColonists:
		if pTeam.isHasTech(iExploration) and data.players[iPlayer].iColonistsAlreadyGiven < dMaxColonists[iCiv]:
			sourceCities = cities.region(plots.capital(iPlayer).getRegionID()).owner(iPlayer)
			
			# help England with settling Canada and Australia
			if iCiv == iEngland:
				sourceCities += cities.regions(rOntario, rMaritimes, rAustralia).owner(iPlayer)
			
			sites = plots.sites(iPlayer).coastal() or plots.sites(iPlayer)
			if sites:
				city = sourceCities.coastal().closest(sites.first())
			else:
				city = sourceCities.coastal().minimum(lambda city: abs(city.getX() - iMiddleAtlantic))
					
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