from VictoryGoals import *
from Locations import *


### UTILS ###

def description(iCiv):
	for goal in dGoals[iCiv]:
		print goal.description()


### CONSTANTS ###

# general constants
lWonders = [i for i in range(iBeginWonders, iNumBuildings)]
lGreatPeople = [iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy]

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
			# TODO: 'a Orthodox Cathedral'
			BuildingCount(iOrthodoxCathedral, 1),
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
		FirstNewWorld().by(1100),
		RaidGold(3000).by(1500),
	),
	iTurks: (
		All(
			WorldPercent(6),
			PillageCount(20),
		).by(900),
		All(
			RouteConnection(plots.rectangle(tChina), plots.of(lMediterraneanPorts), infos.routes()).named("SILK_ROUTE"),
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
		CitySpecialistCount(city(plots.capital(iTibet)).named("LHASA"), iSpecialistGreatProphet, 5).by(1700),
	),
	iIndonesia: (
		BestPopulation().at(1300),
		ResourceCount(different(happiness_resources()).named("DIFFERENT_HAPPINESS_RESOURCES"), 10).by(1500),
		PopulationPercent(9).at(1940),
	),
	iMoors: (
		All(
			CityCount(plots.rectangle(tMaghreb), 3),
			ConqueredCityCount(plots.rectangle(tIberia), 2),
			ConqueredCityCount(plots.rectangle(tWestAfrica), 2),
		).at(1200),
		All(
			Wonder(iMezquita),
			CitySpecialistCount(city(plots.capital(iMoors)), sum([iSpecialistGreatProphet, iSpecialistGreatScientist, iSpecialistGreatEngineer]), 4),
		).by(1300),
		PiracyGold(3000).by(1650),
	),
	iSpain: (
		FirstNewWorld(),
		ControlledResourceCount(sum([iSilver, iGold]), 10).by(1650),
		All(
			ReligionSpreadPercent(iCatholicism, 30),
			NoStateReligion(plots.rectangle(tEurope) + plots.rectangle(tEasternEurope), iProtestantism),
		).at(1650),
	),
	iFrance: (
		CultureLevel(city(plots.capital(iFrance)), iCultureLevelLegendary).at(1700),
		All(
			AreaPercent(plots.rectangle(tEurope) + plots.rectangle(tEasternEurope), 40).includeVassals(),
			AreaPercent(plots.rectangle(tNorthAmerica), 40).includeVassals(),
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
			(plots.regions(*lNorthAmerica), 5),
			(plots.regions(*lSouthAmerica), 3),
			(plots.regions(*lAfrica), 4),
			(plots.regions(*lAsia), 5),
			(plots.regions(*lOceania), 3),
		).by(1730),
		All(
			UnitCount(sum([iFrigate, iShipOfTheLine]), 25),
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
		VassalCount(3).civs(dCivGroups[iCivGroupEurope]).religion(iCatholicism).by(1650),
		All(
			CitySpecialistCount(city(tVienna), sum([iSpecialistGreatArtist, iSpecialistGreatStatesman]), 10),
			AttitudeCount(AttitudeTypes.ATTITUDE_PLEASED, 8).civs(dCivGroups[iCivGroupEurope]),
		).by(1850),
	),
	iRussia: (
		All(
			SettledCityCount(plots.rectangle(tSiberia), 7).by(1700),
			RouteConnection(plots.capital(iRussia), plots.of(lSiberianCoast), [iRailroad]).by(1920),
		),
		Projects(iManhattanProject, iLunarLanding),
		All(
			Communist(),
			AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 5).communist(),
		).by(1950),
	),
	iMali: (
		TradeMission(holyCity()).by(1350),
		All(
			Wonder(iUniversityOfSankore),
			CitySpecialistCount(wonder(iUniversityOfSankore), iSpecialistGreatProphet, 1),
		).by(1500),
		All(
			PlayerGold(5000).by(1500),
			PlayerGold(15000).by(1700),
		),
	),
	iPoland: (
		PopulationCities(12, 3).by(1400),
		FirstDiscovered(iCivilLiberties),
		BuildingCount(sum([iOrthodoxCathedral, iCatholicCathedral, iProtestantCathedral]), 3).by(1600),
	),
	iPortugal: (
		OpenBorderCount(14).by(1550),
		ResourceCount(sum(lColonialResources), 12).by(1650),
		CityCount(sum([
			plots.rectangle(tBrazil),
			plots.regions(*lAfrica),
			plots.regions(*lAsia),
		]), 15).by(1700),
	),
	iInca: (
		All(
			BuildingCount(iTambo, 5),
			Route(plots.of(lAndeanCoast), iRouteRoad),
		).by(1550),
		PlayerGold(2500).at(1550),
		NoForeignCities(plots.rectangle(tSouthAmerica)).at(1700),
	),
	iItaly: (
		Wonders(iSanMarcoBasilica, iSistineChapel, iSantaMariaDelFiore).by(1500),
		CultureLevelCities(iCultureLevelInfluential, 3).by(1600),
		AreaPercent(plots.rectangle(tMediterranean).without(lMediterraneanExceptions).coastal(), 65).by(1930),
	),
	iMongols: (
		Control(plots.normal(iChina)).at(1300),
		RazeCount(7),
		WorldPercent(12).by(1500),
	),
	iAztecs: (
		BestPopulationCity(city(plots.capital(iAztecs))).at(1520),
		BuildingCount((iPaganTemple, 6), (iSacrificialAltar, 6)).by(1650),
		EnslaveCount(20).excluding(dCivGroups[iCivGroupAmerica]),
	),
	iMughals: (
		BuildingCount(iIslamicCathedral, 3).by(1500),
		Wonders(iRedFort, iShalimarGardens, iTajMahal).by(1660),
		PlayerCulture(50000).at(1750),
	),
	iOttomans: (
		CityBuildings(capital(), sum(iBuilding for iBuilding in infos.buildings() if isWonder(iBuilding)), 4).at(1550),
		All(
			CultureCovered(
				plots.of(lEasternMediterranean),
				plots.of(lBlackSea),
			),
			Control(
				plots.surrounding(tCairo),
				plots.surrounding(tMecca),
				plots.surrounding(tBaghdad),
				plots.surrounding(tVienna),
			),
		).by(1700),
		MoreCulture().than(dCivGroups[iCivGroupEurope]).at(1800),
	),
	iThailand: (
		OpenBorderCount(10).at(1650),
		BestPopulationCity(city(plots.capital(iThailand))).at(1700),
		NoForeignCities(plots.rectangle(tSouthAsia)).excluding(lSouthAsianCivs).at(1900),
	),
	iCongo: (
		ReligiousVotePercent(15).by(1650),
		SlaveTradeGold(1000).by(1800),
		EnterEra(iIndustrial).before(iGlobal),
	),
	iIran: (
		OpenBorderCount(6).civs(dCivGroups[iCivGroupEurope]).by(1650),
		Control(
			plots.rectangle(tSafavidMesopotamia),
			plots.rectangle(tTransoxiana),
			plots.rectangle(tNorthWestIndia).without(lNorthWestIndiaExceptions),
		).at(1750),
		CultureCity(20000).at(1800),
	),
	iNetherlands: (
		CitySpecialistCount(city(plots.capital(iNetherlands)), iSpecialistGreatMerchant, 3).at(1745),
		ConqueredCityCount(4).civs(dCivGroups[iCivGroupEurope]).outside(plots.regions(*lEurope)).by(1745),
		ResourceCount(iSpices, 7).by(1775),
	),
	iGermany: (
		CitySpecialistCount(city(plots.capital(iGermany)), sum(lGreatPeople), 7).at(1900),
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
			NoForeignCities(plots.rectangle(tNorthCentralAmerica)).only(dCivGroups[iCivGroupEurope]),
			ControlOrVassalize(plots.core(iMexico)),
		).at(1900),
		Wonders(iStatueOfLiberty, iBrooklynBridge, iEmpireStateBuilding, iGoldenGateBridge, iPentagon, iUnitedNations).by(1950),
		All(
			AlliedCommercePercent(75),
			AlliedPowerPercent(75),
		).by(1990),
	),
	iArgentina: (
		GoldenAges(2).by(1930),
		CultureLevel(city(plots.capital(iArgentina)), iCultureLevelLegendary).by(1960),
		GoldenAges(6).by(2000),
	),
	iMexico: (
		BuildingCount(stateReligionBuilding(cathedral), 3).by(1880),
		GreatGenerals(3).by(1940),
		BestPopulationCity(city(plots.capital(iMexico))).at(1960),
	),
	iColombia: (
		NoForeignCities(
			plots.rectangle(tPeru),
			plots.rectangle(tGranColombia),
			plots.rectangle(tGuayanas),
			plots.rectangle(tCaribbean),
		).only(dCivGroups[iCivGroupEurope]).at(1870),
		Control(plots.rectangle(tSouthAmerica).without(lSouthAmericaExceptions)).at(1920),
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
			RouteConnection(plots.lazy().capital(iCanada), plots.of(lAtlanticCoast), [iRailroad]),
			RouteConnection(plots.lazy().capital(iCanada), plots.of(lPacificCoast), [iRailroad]),
		).by(1920),
		All(
			Control(plots.regions(rCanada)),
			AreaPercent(plots.regions(rCanada), 90),
			NeverConquer(),
		).by(1950),
		BrokeredPeaceCount(12).by(2000),
	),
}