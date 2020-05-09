from Events import handler
from Core import *


tCarthage = (58, 39)
tConstantinople = (68, 45)
tBeijing = (102, 47)
tMecca = (75, 33)
tCopenhagen = (60, 56)

dRelocatedCapitals = CivDict({
	iPhoenicia : tCarthage,
	iMongols : tBeijing,
	iOttomans : tConstantinople
})

dCapitalInfrastructure = CivDict({
	iPhoenicia : (3, [], []),
	iByzantium : (5, [iBarracks, iWalls, iLibrary, iMarket, iGranary, iHarbor, iForge], [temple]),
	iPortugal : (5, [iLibrary, iMarket, iHarbor, iLighthouse, iForge, iWalls], [temple]),
	iItaly : (7, [iLibrary, iPharmacy, iMarket, iArtStudio, iAqueduct, iCourthouse, iWalls], [temple]),
	iNetherlands : (9, [iLibrary, iMarket, iWharf, iLighthouse, iBarracks, iPharmacy, iBank, iArena, iTheatre], [temple]),
}


### CITY ACQUIRED ###


@handler("cityAcquired")
def relocateAcquiredCapital(iOwner, iPlayer, city):
	relocateCapitals(iPlayer, city)


@handler("cityAcquired")
def buildAcquiredCapitalInfrastructure(iOwner, iPlayer, city):
	buildCapitalInfrastructure(iPlayer, city)


### CITY ACQUIRED AND KEPT ###


# TODO: maybe new event capitalfounded?
@handler("cityAcquiredAndKept")
def createAdditionalPolishSettler(iPlayer, city):
	if city.isCapital() and civ(iPlayer) == iPoland and not player(iPlayer).isHuman():
		# TODO: move to Locations
		locations = {
			(65, 55): 1, # Memel
			(65, 54): 1, # Koenigsberg
			(64, 54): 3, # Gdansk
		}
		
		location = weighted_random_entry(locations)
		
		makeUnit(iPlayer, iSettler, location)
		makeUnit(iPlayer, iCrossbowman, location)


### CITY BUILT ###


@handler("cityBuilt")
def relocateFoundedCapital(city):
	relocateCapitals(city.getOwner(), city)


@handler("cityBuilt")
def buildFoundedCapitalInfrastructure(city):
	buildCapitalInfrastructure(city.getOwner(), city)
	
	
@handler("cityBuilt")
def createCarthaginianDefenses(city):
	if at(city, tCarthage) and not player(city).isHuman():					
		makeUnit(iPhoenicia, iWorkboat, tCarthage, UnitAITypes.UNITAI_WORKER_SEA)
		makeUnit(iPhoenicia, iGalley, direction(tCarthage, DirectionTypes.DIRECTION_NORTHWEST), UnitAITypes.UNITAI_SETTLER_SEA)
		makeUnit(iPhoenicia, iSettler, direction(tCarthage, DirectionTypes.DIRECTION_NORTHWEST), UnitAITypes.UNITAI_SETTLE)
		
		if player(iRome).isHuman():
			city.setHasRealBuilding(iWalls, True)
			
			makeUnits(iPhoenicia, iArcher, tCarthage, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPhoenicia, iNumidianCavalry, tCarthage, 3)
			makeUnits(iPhoenicia, iWarElephant, tCarthage, 2, UnitAITypes.UNITAI_CITY_COUNTER)


@handler("cityBuilt")
def foundIslam(city):
	if civ(city) == iArabia:
		if not game.isReligionFounded(iIslam):
			if at(city, tMecca):
				rel.foundReligion(location(city), iIslam)


# TODO: use capital founded/acquired event OR hook up into new rnf code
@handler("cityBuilt")
def clearDanishCulture(city):
	if civ(city) == iHolyRome and player(city).getNumCities() == 1:
		copenhagen = city(tCopenhagen)
		if copenhagen and civ(copenhagen) == iVikings:
			city.setCulture(city.getOwner(), 5, True)
			
			
### UNIT BUILT ###
	

@handler("unitBuilt")
def foundChineseCity(city, unit):
	if unit.isFound() and civ(unit) == iChina and not player(unit).isHuman():
		plot = plots.of(lChineseCities).where(lambda plot: isFree(unit.getOwner(), plot, True, True, True)).random()
	
		if plot:
			player(unit).found(plot.getX(), plot.getY())
			unit.kill(False, -1)


### BEGIN GAME TURN ###


@handler("BeginGameTurn")
def placeGoodyHuts(iGameTurn):
	if iGameTurn == getScenarioStartTurn() + 3:
			
		if scenario() == i3000BC:
			self.placeHut((101, 38), (107, 41)) # Southern China
			self.placeHut((62, 45), (67, 50)) # Balkans
			self.placeHut((69, 42), (76, 46)) # Asia Minor
		
		if scenario() <= i600AD:
			self.placeHut((49, 40), (54, 46)) # Iberia
			self.placeHut((57, 51), (61, 56)) # Denmark / Northern Germany
			self.placeHut((48, 55), (49, 58)) # Ireland
			self.placeHut((50, 53), (54, 60)) # Britain
			self.placeHut((57, 57), (65, 65)) # Scandinavia
			self.placeHut((73, 53), (81, 58)) # Russia
			self.placeHut((81, 43), (86, 47)) # Transoxania
			self.placeHut((88, 30), (94, 36)) # Deccan
			self.placeHut((110, 40), (113, 43)) # Shikoku
			self.placeHut((114, 49), (116, 52)) # Hokkaido
			self.placeHut((85, 53), (99, 59)) # Siberia
			self.placeHut((103, 24), (109, 29)) # Indonesia
			self.placeHut((68, 17), (72, 23)) # East Africa
			self.placeHut((65, 10), (70, 16)) # South Africa
			self.placeHut((22, 48), (29, 51)) # Great Lakes
			self.placeHut((18, 44), (22, 52)) # Great Plains
			self.placeHut((34, 25), (39, 29)) # Amazonas Delta
			self.placeHut((33, 9), (37, 15)) # Parana Delta
			self.placeHut((25, 36), (32, 39)) # Caribbean
		
		self.placeHut((107, 19), (116, 22)) # Northern Australia
		self.placeHut((114, 10), (118, 17)) # Western Australia
		self.placeHut((120, 5), (123, 11)) # New Zealand
		self.placeHut((59, 25), (67, 28)) # Central Africa


@handler("BeginGameTurn")
def clearMassilianCulture(iGameTurn):		
	if iGameTurn == year(dBirth[iSpain])-1:
		if scenario() == i600AD:
			pMassilia = city_(56, 46)
			if pMassilia:
				pMassilia.setCulture(pMassilia.getOwner(), 1, True)


@handler("BeginGameTurn")
def ottomansFlipIndependents(iGameTurn):
	if iGameTurn == data.iOttomanSpawnTurn + 1:
		for city in cities.birth(iOttomans):
			iOwner = city.getOwner()
			if is_minor(iOwner):
				# TODO: this should be better but is not covered by completeCityFlip
				flipCity(city, False, True, slot(iOttomans), ())
				cultureManager(city, 100, slot(iOttomans), iOwner, True, False, False)
				self.convertSurroundingPlotCulture(slot(iOttomans), plots.surrounding(city))
				makeUnit(iOttomans, iCrossbowman, city)


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
		-600 : iRome,
		-400 : iRome,
	}
	
	iYear = game.getGameTurnYear()
	if iYear in dEarlyColonistYears:
		iCiv = dEarlyColonistYears[iYear]
		giveEarlyColonists(iCiv)
		
		
@handler("BeginGameTurn")
def checkLateColonists():
	if year().between(1350, 1918):
		for iCiv in dTradingCompanyPlots:
			if player(iCiv).isAlive():
				iPlayer = slot(iCiv)
				if turn() == data.players[iPlayer].iExplorationTurn + 1 + data.players[iPlayer].iColonistsAlreadyGiven * 8:
					giveColonists(iPlayer)


@handler("BeginGameTurn")
def checkRaiders():
	if year().between(860, 1250):
		if turn() % turns(10) == 9:
			giveRaiders(iVikings)
	

@handler("BeginGameTurn")
def moorishSpawnInMorocoo():
	if year() == year(710)-1:
		marrakesh = city_(51, 37)
		if marrakesh:
			marrakesh.setHasReligion(iIslam, True, False, False)
			
			makeUnit(marrakesh.getOwner(), iSettler, marrakesh)
			makeUnit(marrakesh.getOwner(), iWorker, marrakesh)


@handler("BeginGameTurn")
def flipChineseStartingCities():
	if scenario() == i600AD and year() == scenarioStartTurn():
		tTL, tBR = dBirthArea[iChina]
		if not player(iChina).isHuman(): 
			tTL = (99, 39) # 4 tiles further north
		
		china = plots.start(tTL).end(tBR)
		iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(slot(iChina), china)
		self.convertSurroundingPlotCulture(slot(iChina), china)
		
		for iMinor in players.independent().barbarian():
			flipUnitsInArea(china, slot(iChina), iMinor, False, player(iMinor).isBarbarian())


### IMPLEMENTATION ###


def relocateCapitals(iPlayer, city):
	if player(iPlayer).isHuman():
		return
	
	if iPlayer in dConquestCapitals:
		tCapital = dConquestCapitals[iPlayer]
		
		if location(city) == tCapital:
			moveCapital(iPlayer, tCapital)
			
	if civ(iPlayer) == iTurks and isAreaControlled(iPlayer, dCoreArea[iPersia][0], dCoreArea[iPersia][1]):
		capital = player(iPlayer).getCapitalCity()
		if capital not in plots.core(iPersia):
			newCapital = cities.core(iPersia).owner(iPlayer).random()
			if newCapital:
				moveCapital(iPlayer, location(newCapital))


def buildCapitalInfrastructure(iPlayer, city):
	if iPlayer in dCapitalInfrastructure:
		if at(city, plots.capital(iPlayer)) and year() <= year(dSpawn[iPlayer]) + turns(5):
			iPopulation, lBuildings, lReligiousBuildings = dCapitalInfrastructure
			
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
	
	if pPlayer.isAlive() and not pPlayer.isHuman():
		capital = pPlayer.getCapitalCity()

		if iCiv == iRome:
			capital = cities.owner(iCiv).region(rIberia).random()
			
		if capital:
			tSeaPlot = self.findSeaPlots(capital, 1, iCiv)
			if tSeaPlot:
				makeUnit(iCiv, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iCiv, iSettler, tSeaPlot)
				makeUnit(iCiv, iArcher, tSeaPlot)


def giveColonists(iPlayer):
	pPlayer = player(iPlayer)
	pTeam = team(iPlayer)
	iCiv = civ(iPlayer)
	
	if pPlayer.isAlive() and not pPlayer.isHuman() and iCiv in dMaxColonists:
		if pTeam.isHasTech(iExploration) and data.players[iPlayer].iColonistsAlreadyGiven < dMaxColonists[iCiv]:
			sourceCities = cities.core(iCiv).owner(iPlayer)
			
			# help England with settling Canada and Australia
			if iCiv == iEngland:
				colonialCities = cities.start(tCanadaTL).end(tCanadaBR).owner(iPlayer)
				colonialCities += cities.start(tAustraliaTL).end(tAustraliaBR).owner(iPlayer)
				
				if colonialCities:
					sourceCities = colonialCities
					
			city = sourceCities.coastal().random()
			if city:
				tSeaPlot = self.findSeaPlots(city, 1, iCiv)
				if not tSeaPlot: tSeaPlot = city
				
				makeUnit(iPlayer, unique_unit(iPlayer, iGalleon), tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot, UnitAITypes.UNITAI_SETTLE)
				makeUnit(iPlayer, getBestDefender(iPlayer), tSeaPlot)
				makeUnit(iPlayer, iWorker, tSeaPlot)
				
				data.players[iPlayer].iColonistsAlreadyGiven += 1


def giveRaiders(iCiv):
	pPlayer = player(iCiv)
	pTeam = team(iCiv)
	
	if pPlayer.isAlive() and not pPlayer.isHuman():
		city = cities.owner(iCiv).coastal().random()
		if city:
			seaPlot = self.findSeaPlots(location(city), 1, iCiv)
			if seaPlot:
				makeUnit(iCiv, unique_unit(iCiv, iGalley), seaPlot, UnitAITypes.UNITAI_ASSAULT_SEA)
				if pTeam.isHasTech(iSteel):
					makeUnit(iCiv, unique_unit(iCiv, iHeavySwordsman), seaPlot, UnitAITypes.UNITAI_ATTACK)
					makeUnit(iCiv, unique_unit(iCiv, iHeavySwordsman), seaPlot, UnitAITypes.UNITAI_ATTACK_CITY)
				else:
					makeUnit(iCiv, unique_unit(iCiv, iSwordsman), seaPlot, UnitAITypes.UNITAI_ATTACK)
					makeUnit(iCiv, unique_unit(iCiv, iSwordsman), seaPlot, UnitAITypes.UNITAI_ATTACK_CITY)