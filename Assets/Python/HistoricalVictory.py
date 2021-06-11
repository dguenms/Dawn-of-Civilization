from VictoryGoals import *
from Locations import *


### CONSTANTS ###

# general constants
lWonders = [i for i in range(iBeginWonders, iNumBuildings)]

# second Portuguese goal: acquire 12 colonial resources by 1650 AD
lColonialResources = [iBanana, iSpices, iSugar, iCoffee, iTea, iTobacco]

# third Thai goal: allow no foreign powers in South Asia in 1900 AD
lSouthAsianCivs = [iIndia, iTamils, iIndonesia, iKhmer, iMughals, iThailand]


### GOALS ###

dGoals = {
	iEgypt: (
		PlayerCulture(500).by(-850),
		Wonders(iPyramids, iGreatLibrary, iGreatLighthouse).by(-100),
		PlayerCulture(5000).by(170),
	),
	iBabylonia: (
		FirstDiscovered(iConstruction, iArithmetics, iWriting, iCalendar, iContract),
		BestPopulationCity(city(tBabylon).named("BABYLON")).at(-850),
		BestCultureCity(city(tBabylon).named("BABYLON")).at(-700),
	),
	iHarappa: (
		TradeConnection().by(-1600),
		BuildingCount((iReservoir, 3), (iGranary, 2), (iSmokehouse, 2)).by(-1500),
		PlayerPopulation(30).by(-800),
	),
	iChina: (
		BuildingCount((iConfucianCathedral, 2), (iTaoistCathedral, 2)).by(1000),
		FirstDiscovered(iCompass, iPaper, iGunpowder, iPrinting),
		GoldenAges(4).by(1800),
	),
	iGreece: (
		FirstDiscovered(iMathematics, iLiterature, iAesthetics, iPhilosophy, iMedicine),
		Control(
			plots.normal(iEgypt),
			plots.normal(iPhoenicia),
			plots.normal(iBabylonia),
			plots.normal(iPersia),
		).at(-330),
		Wonders(iParthenon, iColossus, iStatueOfZeus, iTempleOfArtemis).by(-250),
	),
	iIndia: (
		BuildingCount((iHinduShrine, 1), (iBuddhistShrine, 1)).at(-100),
		BuildingCount(religious_buildings(temple).named("TEMPLES"), 20).by(700),
		PopulationPercent(20).at(1200),
	),
	iPhoenicia: (
		CityBuildings(city(tCarthage).named("CARTHAGE"), (iPalace, 1), (iGreatCothon, 1)).by(-300),
		Control(
			plots.rectangle(dNormalArea[iItaly]).without((62, 47), (63, 47), (63, 46)).named("ITALY"),
			plots.rectangle(tIberia).named("IBERIA"),
		).at(-100),
		PlayerGold(5000).at(200),
	),
	iPolynesia: (
		Some(Settle(
			plots.rectangle(tHawaii).named("HAWAII"),
			plots.rectangle(tNewZealand).named("NEW_ZEALAND"),
			plots.rectangle(tMarquesas).named("MARQUESAS"),
			plots.rectangle(tEasterIsland).named("EASTER_ISLAND"),
		), 2).by(800),
		Settle(
			plots.rectangle(tHawaii).named("HAWAII"),
			plots.rectangle(tNewZealand).named("NEW_ZEALAND"),
			plots.rectangle(tMarquesas).named("MARQUESAS"),
			plots.rectangle(tEasterIsland).named("EASTER_ISLAND"),
		).by(1000),
		Wonder(iMoaiStatues).by(1200),
	),
	iPersia: (
		WorldPercent(7).by(140),
		BuildingCount(wonders(), 7).by(350),
		BuildingCount(religious_buildings(shrine).named("SHRINES"), 2).at(350),
	),
	iRome: (
		BuildingCount((iBarracks, 6), (iAqueduct, 5), (iArena, 4), (iForum, 3)).by(100),
		CityCount(
			(plots.normal(iSpain).named("IBERIA"), 2),
			(plots.rectangle(tGaul).named("GAUL"), 2),
			(plots.core(iEngland).named("BRITAIN"), 1),
			(plots.rectangle(tAfrica).named("AFRICA"), 2),
			(plots.core(iByzantium).named("ANATOLIA"), 4),
			(plots.core(iEgypt), 2),
		).at(320),
		FirstDiscovered(iArchitecture, iPolitics, iScholarship, iMachinery, iCivilService),
	),
	iMaya: (
		Discovered(iCalendar).by(200),
		Wonder(iTempleOfKukulkan).by(900),
		FirstContact(plots.rectangle(tSouthAmerica) + plots.rectangle(tNorthAmerica), *dCivGroups[iCivGroupEurope]).named("FIRST_CONTACT_NEW_WORLD"),
	),
	iTamils: (
		All(
			PlayerGold(3000),
			PlayerCulture(2000),
		).at(800),
		ControlOrVassalize(
			plots.rectangle(tDeccan).named("DECCAN"),
			plots.rectangle(tSrivijaya).named("SRIVIJAYA"),
		).at(1000),
		TradeGold(4000).by(1200),
	),
	iEthiopia: (
		ResourceCount(iIncense, 3).by(400),
		All(
			ConvertAfterFounding(5, iOrthodoxy),
			SpecialistCount(iSpecialistGreatProphet, 3),
			BuildingCount(iOrthodoxCathedral, 1).named("ORTHODOX_CATHEDRAL"),
		).by(1200),
		MoreReligion(plots.regions(*lAfrica).named("AFRICA"), iOrthodoxy, iIslam).at(1500),
	),
	iKorea: (
		BuildingCount((iBuddhistCathedral, 1), (iConfucianCathedral, 1)).by(1200),
		FirstDiscovered(iPrinting),
		SunkShips(20),
	),
	iByzantium: (
		PlayerGold(5000).at(1000),
		All(
			BestPopulationCity(city(tConstantinople).named("CONSTANTINOPLE")),
			BestCultureCity(city(tConstantinople).named("CONSTANTINOPLE")),
		).at(1200),
		CityCount(
			(plots.rectangle(tBalkans).named("BALKANS"), 3),
			(plots.rectangle(tNorthAfrica).named("NORTH_AFRICA"), 3),
			(plots.rectangle(tNearEast).named("NEAR_EAST"), 3),
		).at(1450),
	),
	iJapan: (
		All(
			AverageCulture(6000),
			NoCityLost(),
		).by(1600),
		ControlOrVassalize(
			plots.rectangle(tKorea).named("KOREA"),
			plots.rectangle(tManchuria).named("MANCHURIA"),
			plots.rectangle(tChina).named("CHINA"),
			plots.rectangle(tIndochina).without(lIndochinaExceptions).named("INDOCHINA"),
			plots.rectangle(tIndonesia).named("INDONESIA"),
			plots.rectangle(tPhilippines).named("PHILIPPINES"),
		).at(1940),
		EraFirstDiscovered((iGlobal, 8), (iDigital, 8)),
	),
	iVikings: (
		Any(Control(*list(plots.core(iCiv) for iCiv in dCivGroups[iCivGroupEurope] if dSpawn[iCiv] <= 1050))).named("ANY_EUROPEAN_CORE").at(1050),
		FirstSettle(plots.regions(*lAmerica).named("AMERICA")).allowed(dCivGroups[iCivGroupAmerica]).by(1100),
		RaidGold(3000).by(1500),
	),
	iTurks: (
		All(
			WorldPercent(6),
			PillageCount(20),
		).by(900),
		All(
			RouteConnection(plots.rectangle(tChina).named("CITY_IN_CHINA"), plots.of(lMediterraneanPorts).named("MEDITERRANEAN_PORT"), infos.routes()).named("SILK_ROUTE"),
			CorporationCount(iSilkRoute, 10)
		).by(1100),
		DifferentCities(
			CultureLevel(capital(), iCultureLevelDeveloping).by(900),
			CultureLevel(capital().named("DIFFERENT_CAPITAL"), iCultureLevelRefined).by(1100),
			CultureLevel(capital().named("ANOTHER_CAPITAL"), iCultureLevelInfluential).by(1400),
		),
	),
	iArabia: (
		BestTech().at(1300),
		ControlOrVassalize(
			plots.core(iEgypt),
			plots.rectangle(tAfrica).named("MAGHREB"),
			plots.normal(iSpain),
			plots.core(iBabylonia).named("MESOPOTAMIA"),
			plots.core(iPersia),
		).at(1300),
		ReligionSpreadPercent(iIslam, 30),
	),
	iTibet: (
		AcquiredCities(5).by(1000),
		ReligionSpreadPercent(iBuddhism, 25).by(1400),
		CitySpecialistCount(start(iTibet).named("LHASA"), iSpecialistGreatProphet, 5).by(1700),
	),
	iIndonesia: (
		BestPopulation().at(1300),
		ResourceCount(different(happiness_resources()).named("DIFFERENT_HAPPINESS_RESOURCES"), 10).by(1500),
		PopulationPercent(9).at(1940),
	),
	iMoors: (
		All(
			CityCount(plots.rectangle(tMaghreb).named("MAGHREB"), 3),
			ConqueredCityCount(2).inside(plots.rectangle(tIberia).named("IBERIA")),
			ConqueredCityCount(2).inside(plots.rectangle(tWestAfrica).named("WEST_AFRICA")),
		).at(1200),
		All(
			Wonder(iMezquita),
			CitySpecialistCount(start(iMoors).named("CORDOBA"), sum(iSpecialistGreatProphet, iSpecialistGreatScientist, iSpecialistGreatEngineer), 4),
		).by(1300),
		PiracyGold(3000).by(1650),
	),
	iSpain: (
		FirstSettle(plots.regions(*lAmerica).named("AMERICA")).allowed(dCivGroups[iCivGroupAmerica]),
		ControlledResourceCount(sum(iSilver, iGold), 10).by(1650),
		All(
			ReligionSpreadPercent(iCatholicism, 30),
			AreaNoStateReligion((plots.rectangle(tEurope) + plots.rectangle(tEasternEurope)).named("EUROPE"), iProtestantism),
		).at(1650),
	),
	iFrance: (
		CultureLevel(start(iFrance).named("PARIS"), iCultureLevelLegendary).at(1700),
		All(
			AreaPercent((plots.rectangle(tEurope) + plots.rectangle(tEasternEurope)).named("EUROPE"), 40).includeVassals(),
			AreaPercent(plots.rectangle(tNorthAmerica).named("NORTH_AMERICA"), 40).includeVassals(),
		).at(1800),
		Wonders(iNotreDame, iVersailles, iLouvre, iEiffelTower, iMetropolitain).by(1900),
	),
	iKhmer: (
		All(
			BuildingCount((iBuddhistMonastery, 4), (iHinduMonastery, 4)),
			Wonder(iWatPreahPisnulok),
		).at(1200),
		AveragePopulation(12).at(1450),
		PlayerCulture(8000).by(1450),
	),
	iEngland: (
		CityCount(
			(plots.regions(*lNorthAmerica).named("NORTH_AMERICA"), 5),
			(plots.regions(*lSouthAmerica).named("SOUTH_AMERICA"), 3),
			(plots.regions(*lAfrica).named("AFRICA"), 4),
			(plots.regions(*lAsia).named("ASIA"), 5),
			(plots.regions(*lOceania).named("OCEANIA"), 3),
		).by(1730),
		All(
			UnitCount(sum(iFrigate, iShipOfTheLine), 25),
			SunkShips(50),
		).by(1800),
		EraFirstDiscovered((iRenaissance, 8), (iIndustrial, 8)),
	),
	iHolyRome: (
		All(
			BuildingCount(iCatholicShrine, 1).at(1000),
			BuildingCount(iOrthodoxShrine, 1).at(1200),
			BuildingCount(iProtestantShrine, 1).at(1550),
		),
		VassalCount(3).civs(group(iCivGroupEurope).named("AREA_NAME_EUROPE")).religion(iCatholicism).named("CATHOLIC_VASSALS_IN_EUROPE").by(1650),
		All(
			CitySpecialistCount(city(tVienna).named("VIENNA"), sum(iSpecialistGreatArtist, iSpecialistGreatStatesman), 10),
			AttitudeCount(AttitudeTypes.ATTITUDE_PLEASED, 8).civs(group(iCivGroupEurope).named("AREA_NAME_EUROPE")).independent().named("ATTITUDES_IN_EUROPE"),
		).by(1850),
	),
	iRussia: (
		All(
			SettledCityCount(plots.rectangle(tSiberia).named("SIBERIA"), 7).by(1700),
			RouteConnection(plots.capitals(iRussia).named("MOSCOW"), plots.of(lSiberianCoast).named("SIBERIAN_COAST"), [iRouteRailroad]).named("CONNECT_MOSCOW_TO_SIBERIA").by(1920),
		),
		Projects(iManhattanProject, iLunarLanding),
		All(
			Communist(),
			AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 5).communist().named("COMMUNIST_ATTITUDES"),
		).by(1950),
	),
	iMali: (
		TradeMission(holyCity()).by(1350),
		All(
			Wonder(iUniversityOfSankore),
			CitySpecialistCount(wonder(iUniversityOfSankore).named("ITS_CITY"), iSpecialistGreatProphet, 1),
		).by(1500),
		All(
			PlayerGold(5000).by(1500),
			PlayerGold(15000).by(1700),
		),
	),
	iPoland: (
		PopulationCities(12, 3).by(1400),
		FirstDiscovered(iCivilLiberties),
		BuildingCount(sum(iOrthodoxCathedral, iCatholicCathedral, iProtestantCathedral).named("CHRISTIAN_CATHEDRALS"), 3).by(1600),
	),
	iPortugal: (
		OpenBorderCount(14).by(1550),
		ResourceCount(sum(lColonialResources).named("TRADING_COMPANY_RESOURCES"), 12).by(1650),
		CityCount(sum(
			plots.rectangle(tBrazil).named("BRAZIL"),
			plots.regions(*lAfrica).named("AFRICA"),
			plots.regions(*lAsia).named("ASIA"),
		), 15).by(1700),
	),
	iInca: (
		All(
			BuildingCount(iTambo, 5),
			Route(plots.of(lAndeanCoast).named("ANDEAN_COAST"), iRouteRoad),
		).by(1550),
		PlayerGold(2500).at(1550),
		AreaPopulationPercent(plots.regions(*lSouthAmerica).named("SOUTH_AMERICA"), 90).at(1775)
	),
	iItaly: (
		Wonders(iSanMarcoBasilica, iSistineChapel, iSantaMariaDelFiore).by(1500),
		CultureLevelCities(iCultureLevelInfluential, 3).by(1600),
		AreaPercent(plots.rectangle(tMediterranean).without(lMediterraneanExceptions).coastal().named("MEDITERRANEAN"), 65).by(1930),
	),
	iMongols: (
		Control(plots.normal(iChina)).at(1300),
		RazeCount(7),
		WorldPercent(12).by(1500),
	),
	iAztecs: (
		BestPopulationCity(start(iAztecs).named("TENOCHTITLAN")).at(1520),
		BuildingCount((iPaganTemple, 6), (iSacrificialAltar, 6)).by(1650),
		EnslaveCount(20).excluding(group(iCivGroupAmerica)).named("ENSLAVE_OLD_WORLD"),
	),
	iMughals: (
		BuildingCount(iIslamicCathedral, 3).by(1500),
		Wonders(iRedFort, iShalimarGardens, iTajMahal).by(1660),
		PlayerCulture(50000).at(1750),
	),
	iOttomans: (
		CityBuildings(capital(), wonders(), 4).at(1550),
		All(
			CultureCovered(
				plots.of(lEasternMediterranean).named("EASTERN_MEDITERRANEAN"),
				plots.of(lBlackSea).named("BLACK_SEA"),
			),
			Control(
				plots.surrounding(tCairo).named("CAIRO"),
				plots.surrounding(tMecca).named("MECCA"),
				plots.surrounding(tBaghdad).named("BAGHDAD"),
				plots.surrounding(tVienna).named("VIENNA"),
			),
		).by(1700),
		MoreCulture().than(group(iCivGroupEurope)).named("MORE_CULTURE_THAN_EUROPE").at(1800),
	),
	iThailand: (
		OpenBorderCount(10).at(1650),
		BestPopulationCity(start(iThailand).named("AYUTTHAYA")).at(1700),
		NoForeignCities(plots.rectangle(tSouthAsia).named("SOUTH_ASIA")).excluding(lSouthAsianCivs).at(1900),
	),
	iCongo: (
		ReligiousVotePercent(15).by(1650),
		SlaveTradeGold(1000).by(1800),
		EnterEra(iIndustrial).before(iGlobal),
	),
	iIran: (
		OpenBorderCount(6).civs(dCivGroups[iCivGroupEurope]).named("EUROPEAN_OPEN_BORDERS").by(1650),
		Control(
			plots.rectangle(tSafavidMesopotamia).named("MESOPOTAMIA"),
			plots.rectangle(tTransoxiana).named("TRANSOXIANA"),
			plots.rectangle(tNorthWestIndia).without(lNorthWestIndiaExceptions).named("NORTHWEST_INDIA"),
		).at(1750),
		CultureCity(20000).at(1800),
	),
	iNetherlands: (
		CitySpecialistCount(start(iNetherlands).named("AMSTERDAM"), iSpecialistGreatMerchant, 3).at(1745),
		ConqueredCityCount(4).civs(dCivGroups[iCivGroupEurope]).outside(plots.regions(*lEurope).named("COLONIAL")).named("CONQUER_FOUR_EUROPEAN_COLONIES").by(1745),
		ResourceCount(iSpices, 7).by(1775),
	),
	iGermany: (
		CitySpecialistCount(start(iGermany).named("BERLIN"), great_people(), 7).at(1900),
		Control(
			plots.normal(iItaly),
			plots.normal(iFrance),
			plots.normal(iEngland),
			plots.normal(iVikings),
			plots.normal(iRussia),
		).at(1940),
		EraFirstDiscovered((iIndustrial, 8), (iGlobal, 8)),
	),
	iAmerica: (
		All(
			NoForeignCities(plots.rectangle(tNorthCentralAmerica).named("NORTH_CENTRAL_AMERICA")).only(dCivGroups[iCivGroupEurope]).named("NO_EUROPEAN_COLONIES"),
			ControlOrVassalize(plots.core(iMexico)),
		).at(1900),
		Wonders(iStatueOfLiberty, iBrooklynBridge, iEmpireStateBuilding, iGoldenGateBridge, iPentagon, iUnitedNations).by(1950),
		All(
			# negative value
			AlliedCommercePercent(75),
			AlliedPowerPercent(75),
		).by(1990),
	),
	iArgentina: (
		GoldenAges(2).by(1930),
		CultureLevel(start(iArgentina).named("BUENOS_AIRES"), iCultureLevelLegendary).by(1960),
		GoldenAges(6).by(2000),
	),
	iMexico: (
		BuildingCount(stateReligionCathedral(), 3).by(1880),
		GreatGenerals(3).by(1940),
		BestPopulationCity(start(iMexico).named("MEXICO_CITY")).at(1960),
	),
	iColombia: (
		NoForeignCities(
			plots.rectangle(tPeru).named("PERU"),
			plots.rectangle(tGranColombia).named("GRAN_COLOMBIA"),
			plots.rectangle(tGuayanas).named("GUAYANAS"),
			plots.rectangle(tCaribbean).named("CARIBBEAN"),
		).only(dCivGroups[iCivGroupEurope]).named("NO_EUROPEAN_COLONIES").at(1870),
		Control(plots.rectangle(tSouthAmerica).without(lSouthAmericaExceptions).named("SOUTH_AMERICA")).at(1920),
		ResourceTradeGold(3000).by(1950),
	),
	iBrazil: (
		ImprovementCount((iSlavePlantation, 8), (iPasture, 4)).at(1880),
		Wonders(iWembley, iCristoRedentor, iItaipuDam),
		All(
			ImprovementCount(iForestPreserve, 20),
			CityBuilding(capital(), iNationalPark),
		).by(1950),
	),
	iCanada: (
		All(
			RouteConnection(capital(), plots.of(lAtlanticCoast).named("ATLANTIC_COAST"), [iRouteRailroad]).named("CAPITAL_ATLANTIC_RAILWAY"),
			RouteConnection(capital(), plots.of(lPacificCoast).named("PACIFIC_COAST"), [iRouteRailroad]).named("CAPITAL_PACIFIC_RAILWAY"),
		).by(1920),
		All(
			Control(plots.regions(rCanada).named("CANADA")),
			AreaPercent(plots.regions(rCanada).named("CANADA"), 90),
			NeverConquer(),
		).named("CONTROL_CANADA_WITHOUT_EVER_CONQUERING").by(1950),
		BrokeredPeaceCount(12).by(2000),
	),
}

for iCiv, tGoals in dGoals.items():
	for i, goal in enumerate(tGoals):
		goal.titled("%s%s" % (infos.civ(iCiv).getIdentifier(), i+1))