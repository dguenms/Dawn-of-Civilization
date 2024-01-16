from Definitions import *
from Locations import *


# first Viking goal: control a European core in 1050 AD
lVikingTargets = [plots.core(iCiv) for iCiv in dCivGroups[iCivGroupEurope] if iCiv != iVikings and dBirth[iCiv] <= 1050]

# second Portuguese goal: acquire 12 colonial resources by 1650 AD
lColonialResources = [iBanana, iSpices, iSugar, iCoffee, iTea, iTobacco]

# third Thai goal: allow no foreign powers in South Asia in 1900 AD
lSouthAsianCivs = [iIndia, iDravidia, iVietnam, iMalays, iJava, iKhmer, iBurma, iMughals, iThailand]


# city names
AMSTERDAM = "TXT_KEY_VICTORY_NAME_AMSTERDAM"
AYUTTHAYA = "TXT_KEY_VICTORY_NAME_AYUTTHAYA"
BABYLON = "TXT_KEY_VICTORY_NAME_BABYLON"
BAGHDAD = "TXT_KEY_VICTORY_NAME_BAGHDAD"
BERLIN = "TXT_KEY_VICTORY_NAME_BERLIN"
BUENOS_AIRES = "TXT_KEY_VICTORY_NAME_BUENOS_AIRES"
CAIRO = "TXT_KEY_VICTORY_NAME_CAIRO"
CARTHAGE = "TXT_KEY_VICTORY_NAME_CARTHAGE"
CONSTANTINOPLE = "TXT_KEY_VICTORY_NAME_CONSTANTINOPLE"
CORDOBA = "TXT_KEY_VICTORY_NAME_CORDOBA"
LHASA = "TXT_KEY_VICTORY_NAME_LHASA"
MECCA = "TXT_KEY_VICTORY_NAME_MECCA"
MEXICO_CITY = "TXT_KEY_VICTORY_NAME_MEXICO_CITY"
MOSCOW = "TXT_KEY_VICTORY_NAME_MOSCOW"
PARIS = "TXT_KEY_VICTORY_NAME_PARIS"
TENOCHTITLAN = "TXT_KEY_VICTORY_NAME_TENOCHTITLAN"
VIENNA = "TXT_KEY_VICTORY_NAME_VIENNA"

# city descriptors
CAPITAL = "TXT_KEY_VICTORY_NAME_CAPITAL"
DIFFERENT_CAPITAL = "TXT_KEY_VICTORY_NAME_DIFFERENT_CAPITAL"
ANOTHER_CAPITAL = "TXT_KEY_VICTORY_NAME_ANOTHER_CAPITAL"
ITS_CITY = "TXT_KEY_VICTORY_NAME_ITS_CITY"

# area names
AFRICA = "TXT_KEY_VICTORY_NAME_AFRICA"
ANDES = "TXT_KEY_VICTORY_NAME_ANDES"
ATLANTIC_COAST = "TXT_KEY_VICTORY_NAME_ATLANTIC_COAST"
AMERICA = "TXT_KEY_VICTORY_NAME_AMERICA"
ANATOLIA = "TXT_KEY_VICTORY_NAME_ANATOLIA"
ASIA = "TXT_KEY_VICTORY_NAME_ASIA"
BALKANS = "TXT_KEY_VICTORY_NAME_BALKANS"
BLACK_SEA = "TXT_KEY_VICTORY_NAME_BLACK_SEA"
BRAZIL = "TXT_KEY_VICTORY_NAME_BRAZIL"
BRITAIN = "TXT_KEY_VICTORY_NAME_BRITAIN"
CARIBBEAN = "TXT_KEY_VICTORY_NAME_CARIBBEAN"
CHINA = "TXT_KEY_VICTORY_NAME_CHINA"
DECCAN = "TXT_KEY_VICTORY_NAME_DECCAN"
EASTER_ISLAND = "TXT_KEY_VICTORY_NAME_EASTER_ISLAND"
EASTERN_MEDITERRANEAN = "TXT_KEY_VICTORY_NAME_EASTERN_MEDITERRANEAN"
EGYPT = "TXT_KEY_VICTORY_NAME_EGYPT"
EUROPE = "TXT_KEY_VICTORY_NAME_EUROPE"
GAUL = "TXT_KEY_VICTORY_NAME_GAUL"
GRAN_COLOMBIA = "TXT_KEY_VICTORY_NAME_GRAN_COLOMBIA"
GUAYANAS = "TXT_KEY_VICTORY_NAME_GUAYANAS"
HAWAII = "TXT_KEY_VICTORY_NAME_HAWAII"
IBERIA = "TXT_KEY_VICTORY_NAME_IBERIA"
INDOCHINA = "TXT_KEY_VICTORY_NAME_INDOCHINA"
INDONESIA = "TXT_KEY_VICTORY_NAME_INDONESIA"
ITALY = "TXT_KEY_VICTORY_NAME_ITALY"
KOREA = "TXT_KEY_VICTORY_NAME_KOREA"
LEVANT = "TXT_KEY_VICTORY_NAME_LEVANT"
MAGHREB = "TXT_KEY_VICTORY_NAME_MAGHREB"
MANCHURIA = "TXT_KEY_VICTORY_NAME_MANCHURIA"
MARQUESAS = "TXT_KEY_VICTORY_NAME_MARQUESAS"
MEDITERRANEAN = "TXT_KEY_VICTORY_NAME_MEDITERRANEAN"
MESOPOTAMIA = "TXT_KEY_VICTORY_NAME_MESOPOTAMIA"
NEAR_EAST = "TXT_KEY_VICTORY_NAME_NEAR_EAST"
NEW_ZEALAND = "TXT_KEY_VICTORY_NAME_NEW_ZEALAND"
NORTH_AFRICA = "TXT_KEY_VICTORY_NAME_NORTH_AFRICA"
NORTH_AMERICA = "TXT_KEY_VICTORY_NAME_NORTH_AMERICA"
NORTH_CENTRAL_AMERICA = "TXT_KEY_VICTORY_NAME_NORTH_CENTRAL_AMERICA"
NUBIA = "TXT_KEY_VICTORY_NAME_NUBIA"
OCEANIA = "TXT_KEY_VICTORY_NAME_OCEANIA"
PACIFIC_COAST = "TXT_KEY_VICTORY_NAME_PACIFIC_COAST"
PERSIA = "TXT_KEY_VICTORY_NAME_PERSIA"
PERU = "TXT_KEY_VICTORY_NAME_PERU"
PHILIPPINES = "TXT_KEY_VICTORY_NAME_PHILIPPINES"
PUNJAB = "TXT_KEY_VICTORY_NAME_PUNJAB"
SCANDINAVIA = "TXT_KEY_VICTORY_NAME_SCANDINAVIA"
SIBERIA = "TXT_KEY_VICTORY_NAME_SIBERIA"
SIBERIAN_COAST = "TXT_KEY_VICTORY_NAME_SIBERIAN_COAST"
SOUTH_AMERICA = "TXT_KEY_VICTORY_NAME_SOUTH_AMERICA"
SOUTH_ASIA = "TXT_KEY_VICTORY_NAME_SOUTH_ASIA"
SOUTH_CENTRAL_AMERICA = "TXT_KEY_VICTORY_NAME_SOUTH_CENTRAL_AMERICA"
SRIVIJAYA = "TXT_KEY_VICTORY_NAME_SRIVIJAYA"
TRANSOXIANA = "TXT_KEY_VICTORY_NAME_TRANSOXIANA"
WEST_AFRICA = "TXT_KEY_VICTORY_NAME_WEST_AFRICA"

# area descriptors
ANDEAN_COAST = "TXT_KEY_VICTORY_NAME_ANDEAN_COAST"
CANADIAN_TERRITORY = "TXT_KEY_VICTORY_NAME_CANADIAN_TERRITORY"
CITIES_IN_CANADA = "TXT_KEY_VICTORY_NAME_CITIES_IN_CANADA"
CITY_IN_CHINA = "TXT_KEY_VICTORY_NAME_CITY_IN_CHINA"
COLONIAL = "TXT_KEY_VICTORY_NAME_COLONIAL"
MEDITERRANEAN_PORT = "TXT_KEY_VICTORY_NAME_MEDITERRANEAN_PORT"

# building descriptors
SHRINES = "TXT_KEY_VICTORY_NAME_SHRINES"
TEMPLES = "TXT_KEY_VICTORY_NAME_TEMPLES"
CHRISTIAN_CATHEDRALS = "TXT_KEY_VICTORY_NAME_CHRISTIAN_CATHEDRALS"
STATE_RELIGION_CATHEDRAL = "TXT_KEY_VICTORY_NAME_STATE_RELIGION_CATHEDRAL"

# resource descriptors
DIFFERENT_HAPPINESS_RESOURCES = "TXT_KEY_VICTORY_NAME_DIFFERENT_HAPPINESS_RESOURCES"
TRADING_COMPANY_RESOURCES = "TXT_KEY_VICTORY_NAME_TRADING_COMPANY_RESOURCES"

# routes descriptors
LAND_BASED_TRADE = "TXT_KEY_VICTORY_NAME_LAND_BASED_TRADE"

# civilization descriptors
ALL_EUROPEAN = "TXT_KEY_VICTORY_NAME_ALL_EUROPEAN"
EUROPEAN = "TXT_KEY_VICTORY_NAME_EUROPEAN"
EUROPEAN_CIVILIZATION = "TXT_KEY_VICTORY_NAME_EUROPEAN_CIVILIZATION"
LOCAL = "TXT_KEY_VICTORY_NAME_LOCAL"

# goal descriptors
FIRST_VIKING_GOAL = "TXT_KEY_VICTORY_GOAL_VIKINGS_1"


dGoals = {
	iEgypt: (
		All(
			Wonders(iGreatSphinx, iPyramids),
			CultureAmount(500),
			by=-1200,
		),
		Control(
			plots.region(rNubia).named(NUBIA),
			plots.region(rLevant).named(LEVANT),
			by=-600,
		),
		All(
			Wonders(iGreatLibrary, iGreatLighthouse),
			CultureAmount(5000),
			by=-200,
		),
	),
	iBabylonia: (
		FirstDiscover(iConstruction, iArithmetics, iWriting, iCalendar, iContract),
		CityBuildingCount(city(tBabylon).named(BABYLON), wonders(), 3, by=-850),
		All(
			CityPopulation(city(tBabylon).named(BABYLON), 12),
			CityCultureLevel(city(tBabylon).named(BABYLON), iCultureLevelRefined),
			by=-700,
		),
	),
	iHarappa: (
		TradeConnection(by=-1800),
		BuildingCount((iReservoir, 3), (iGranary, 2), (iWeaver, 2), by=-1500),
		PopulationCount(45, by=-800),
	),
	iAssyria: (
		All(
			CityCaptureGold(250),
			UnitLevelCount(3, 5),
			by=-1200,
		),
		Control(
			plots.region(rMesopotamia).named(MESOPOTAMIA),
			plots.region(rPersia).named(PERSIA),
			plots.region(rLevant).named(LEVANT),
			plots.region(rEgypt).named(EGYPT),
			by=-900,
		),
		CitySpecialistCount(capital().named(CAPITAL), great_people(), 3, by=-600),
	),
	iChina: (
		BuildingCount((iConfucianCathedral, 2), (iTaoistCathedral, 2), by=1000),
		FirstDiscover(iCompass, iPaper, iGunpowder, iPrinting),
		GoldenAges(4, by=1800),
	),
	iGreece: (
		FirstDiscover(iMathematics, iLiterature, iAesthetics, iPhilosophy, iMedicine),
		Control(
			plots.core(iEgypt), # TODO: define in locations or use region
			plots.core(iPhoenicia), # TODO: define in locations or use region
			plots.core(iBabylonia), # TODO: define in locations or use region
			plots.core(iPersia), # TODO: define in locations or use region
			at=-330,
		),
		Wonders(iParthenon, iColossus, iStatueOfZeus, iTempleOfArtemis, by=-250),
	),
	iIndia: (
		BuildingCount((iHinduShrine, 1), (iBuddhistShrine, 1), at=-100),
		BuildingCount(religious_buildings(temple).named(TEMPLES), 20, by=700),
		PopulationPercent(20, at=1200),
	),
	iPhoenicia: (
		CityBuilding(city(tCarthage).named(CARTHAGE), iPalace, iGreatCothon, by=-300),
		Control(
			plots.rectangle(dCoreArea[iItaly]).without((62, 47), (63, 47), (63, 46)).named(ITALY), # TODO: define in locations or use region
			plots.region(rIberia).named(IBERIA),
			at=-100,
		),
		GoldAmount(5000, at=200),
	),
	iPolynesia: (
		Settle(
			plots.rectangle(tHawaii).named(HAWAII),
			(plots.rectangle(tNewZealandEast) + plots.rectangle(tNewZealandWest)).named(NEW_ZEALAND),
			plots.rectangle(tMarquesas).named(MARQUESAS),
			plots.rectangle(tEasterIsland).named(EASTER_ISLAND),
			required=2,
			by=800,
		),
		Settle(
			plots.rectangle(tHawaii).named(HAWAII),
			(plots.rectangle(tNewZealandEast) + plots.rectangle(tNewZealandWest)).named(NEW_ZEALAND),
			plots.rectangle(tMarquesas).named(MARQUESAS),
			plots.rectangle(tEasterIsland).named(EASTER_ISLAND),
			by=1000,
		),
		Wonder(iMoaiStatues, by=1200),
	),
	iPersia: (
		LandPercent(7, by=140),
		BuildingCount(wonders(), 7, by=320),
		BuildingCount(religious_buildings(shrine).named(SHRINES), 2, at=320),
	),
	iRome: (
		BuildingCount((iBarracks, 6), (iAqueduct, 5), (iArena, 4), (iForum, 3), by=100),
		CityCount(
			(plots.region(rIberia).named(IBERIA), 2),
			(plots.region(rFrance).named(GAUL), 2),
			(plots.region(rBritain).named(BRITAIN), 1),
			(plots.region(rMaghreb).named(AFRICA), 2),
			(plots.regions(rGreece, rAnatolia).named(ANATOLIA), 4),
			(plots.region(rEgypt).named(EGYPT), 2),
			at=320,
		),
		FirstDiscover(iArchitecture, iPolitics, iScholarship, iMachinery, iCivilService),
	),
	iMaya: (
		Discover(iCalendar, by=200),
		Wonder(iTempleOfKukulkan, by=900),
		ContactBeforeRevealed(group(iCivGroupEurope).named(EUROPEAN_CIVILIZATION), plots.regions(*lAmerica).named(AMERICA)),
	),
	iDravidia: (
		All(
			GoldAmount(3000),
			CultureAmount(2000),
			at=800,
		),
		Control(
			plots.regions(rDravida, rDeccan).named(DECCAN),
			plots.rectangle(tSrivijaya).named(SRIVIJAYA),
			subject=VASSALS,
			at=1000,
		),
		TradeGold(4000, by=1200),
	),
	iEthiopia: (
		ResourceCount(iIncense, 3, by=400),
		All(
			ConvertAfterFounding(iOrthodoxy, 5),
			SpecialistCount(iSpecialistGreatProphet, 3),
			BuildingCount(iOrthodoxCathedral, 1),
			by=1200,
		),
		MoreReligion(plots.regions(*lAfrica).named(AFRICA), iOrthodoxy, iIslam, at=1500),
	),
	iKorea: (
		BuildingCount((iBuddhistCathedral, 1), (iConfucianCathedral, 1), by=1200),
		FirstDiscover(iPrinting),
		SunkShips(20),
	),
	iByzantium: (
		GoldAmount(5000, at=1000),
		All(
			BestPopulationCity(city(tConstantinople).named(CONSTANTINOPLE)),
			BestCultureCity(city(tConstantinople).named(CONSTANTINOPLE)),
			at=1200,
		),
		CityCount(
			(plots.regions(rGreece, rBalkans).named(BALKANS), 3),
			(plots.regions(rEgypt, rMaghreb).named(NORTH_AFRICA), 3),
			(plots.regions(rAnatolia, rCaucasus, rLevant, rMesopotamia).named(NEAR_EAST), 3),
			at=1450,
		),
	),
	iJapan: (
		All(
			AverageCultureAmount(6000),
			NoCityLost(),
			by=1600,
		),
		Control(
			plots.region(rKorea).named(KOREA),
			plots.regions(rManchuria, rAmur).named(MANCHURIA),
			plots.regions(rNorthChina, rSouthChina).named(CHINA),
			plots.region(rIndochina).named(INDOCHINA),
			plots.region(rIndonesia).named(INDONESIA),
			plots.region(rPhilippines).named(PHILIPPINES),
			subject=VASSALS,
			at=1940,
		),
		EraFirstDiscover((iGlobal, 8), (iDigital, 8)),
	),
	iVikings: (
		Control(required=1, at=1050, desc_key=FIRST_VIKING_GOAL, *lVikingTargets),
		FirstSettle(plots.regions(*lAmerica).named(AMERICA), allowed=dCivGroups[iCivGroupAmerica], by=1100),
		RaidGold(3000, by=1500),
	),
	iTurks: (
		All(
			LandPercent(6),
			PillageCount(20),
			by=900,
		),
		All(
			RouteConnection(NamedList(iRouteRoad).named(LAND_BASED_TRADE), plots.regions(rNorthChina, rSouthChina).named(CITY_IN_CHINA), plots.regions(rEgypt, rLevant, rAnatolia).coastal().named(MEDITERRANEAN_PORT), start_owners=True),
			CorporationCount(iSilkRoute, 10),
			by=1100,
		),
		DifferentCities(
			CityCultureLevel(capital().named(CAPITAL), iCultureLevelDeveloping, by=900),
			CityCultureLevel(capital().named(DIFFERENT_CAPITAL), iCultureLevelRefined, by=1100),
			CityCultureLevel(capital().named(ANOTHER_CAPITAL), iCultureLevelInfluential, by=1400),
		),
	),
	iArabia: (
		BestTechPlayer(at=1300),
		Control(
			plots.region(rEgypt).named(EGYPT),
			plots.region(rMaghreb).named(MAGHREB),
			plots.region(rIberia).named(IBERIA),
			plots.regions(rLevant, rMesopotamia).named(MESOPOTAMIA),
			plots.regions(rPersia, rKhorasan).named(PERSIA),
			subject=VASSALS,
			at=1300,
		),
		ReligionSpreadPercent(iIslam, 30),
	),
	iTibet: (
		AcquiredCities(5, by=1000),
		ReligionSpreadPercent(iBuddhism, 25, by=1400),
		CitySpecialistCount(start(iTibet).named(LHASA), iSpecialistGreatProphet, 5, by=1700),
	),
	iMoors: (
		All(
			CityCount(plots.region(rMaghreb).named(MAGHREB), 3),
			ConqueredCities(2, inside=plots.region(rIberia).named(IBERIA)),
			ConqueredCities(2, inside=plots.rectangle(tWestAfrica).named(WEST_AFRICA)),
			at=1200,
		),
		All(
			Wonder(iMezquita),
			CitySpecialistCount(start(iMoors).named(CORDOBA), sum(iSpecialistGreatProphet, iSpecialistGreatScientist, iSpecialistGreatEngineer), 4),
			by=1300,
		),
		PiracyGold(3000, by=1650),
	),
	iSpain: (
		FirstSettle(plots.regions(*lAmerica).named(AMERICA), allowed=dCivGroups[iCivGroupAmerica]),
		ControlledResourceCount(sum(iSilver, iGold), 10, subject=VASSALS, by=1650),
		All(
			ReligionSpreadPercent(iCatholicism, 30),
			AreaNoStateReligion(plots.regions(*lEuropeProper).named(EUROPE), iProtestantism),
			at=1650,
		),
	),
	iFrance: (
		CityCultureLevel(start(iFrance).named(PARIS), iCultureLevelLegendary, at=1700),
		All(
			AreaPercent(plots.regions(*lEuropeProper).named(EUROPE), 40, subject=VASSALS),
			AreaPercent(plots.regions(*[iRegion for iRegion in lNorthAmerica if iRegion != rAmericanArctic]).named(NORTH_AMERICA), 40, subject=VASSALS),
			at=1800,
		),
		Wonders(iNotreDame, iVersailles, iLouvre, iEiffelTower, iMetropolitain, by=1900),
	),
	iKhmer: (
		All(
			BuildingCount((iHinduMonastery, 4), (iBuddhistMonastery, 4)),
			Wonder(iWatPreahPisnulok),
			at=1200,
		),
		AveragePopulation(12, at=1450),
		CultureAmount(8000, by=1450),
	),
	iEngland: (
		CityCount(
			(plots.regions(*lNorthAmerica).named(NORTH_AMERICA), 5),
			(plots.regions(*(lSouthAmerica + lCentralAmerica)).named(SOUTH_CENTRAL_AMERICA), 3),
			(plots.regions(*lAfrica).named(AFRICA), 4),
			(plots.regions(*lAsia).named(ASIA), 5),
			(plots.regions(*lOceania).named(OCEANIA), 3),
			by=1730,
		),
		All(
			UnitCount(sum(iFrigate, iShipOfTheLine), 25),
			SunkShips(50),
			by=1800,
		),
		EraFirstDiscover((iRenaissance, 8), (iIndustrial, 8)),
	),
	iHolyRome: (
		All(
			BuildingCount(iCatholicShrine, 1, at=1000),
			BuildingCount(iOrthodoxShrine, 1, at=1200),
			BuildingCount(iProtestantShrine, 1, at=1550),
		),
		VassalCount(3, civs=group(iCivGroupEurope).named(EUROPE), iStateReligion=iCatholicism, by=1650),
		All(
			CitySpecialistCount(city(tVienna).named(VIENNA), sum(iSpecialistGreatArtist, iSpecialistGreatStatesman), 10),
			AttitudeCount(AttitudeTypes.ATTITUDE_PLEASED, 8, civs=group(iCivGroupEurope).named(EUROPE), bIndependent=True),
			by=1850,
		),
	),
	iMali: (
		TradeMission(holy_city(), by=1350),
		All(
			Wonder(iUniversityOfSankore),
			CitySpecialistCount(wonder(iUniversityOfSankore).named(ITS_CITY), iSpecialistGreatProphet, 1),
			by=1500,
		),
		All(
			GoldAmount(5000, by=1500),
			GoldAmount(15000, by=1700),
		),
	),
	iPoland: (
		PopulationCityCount(12, 3, by=1400),
		FirstDiscover(iCivilLiberties),
		BuildingCount(sum(iOrthodoxCathedral, iCatholicCathedral, iProtestantCathedral).named(CHRISTIAN_CATHEDRALS), 3, by=1600),
	),
	iPortugal: (
		OpenBorderCount(14, by=1550),
		ResourceCount(sum(lColonialResources).named(TRADING_COMPANY_RESOURCES), 12, by=1650),
		CityCount(sum(
			plots.region(rBrazil).named(BRAZIL),
			plots.regions(*lAfrica).named(AFRICA),
			plots.regions(*lAsia).named(ASIA),
		), 15, by=1700),
	),
	iInca: (
		All(
			BuildingCount(iTambo, 5),
			Route(plots.region(rAndes).coastal().named(ANDEAN_COAST), [iRouteRoad]),
			by=1550,
		),
		GoldAmount(2500, by=1550),
		AreaPopulationPercent(plots.regions(*lSouthAmerica).named(SOUTH_AMERICA), 90, at=1775),
	),
	iItaly: (
		Wonders(iSanMarcoBasilica, iSistineChapel, iSantaMariaDelFiore, by=1500),
		CultureLevelCityCount(iCultureLevelInfluential, 3, by=1600),
		AreaPercent(plots.all().adjacent_region(rMediterraneanSea).named(MEDITERRANEAN), 65, by=1930),
	),
	iMongols: (
		Control(plots.regions(rNorthChina, rSouthChina).named(CHINA), at=1300),
		RazeCount(7),
		LandPercent(12, by=1500),
	),
	iAztecs: (
		BestPopulationCity(start(iAztecs).named(TENOCHTITLAN), at=1520),
		BuildingCount((iPaganTemple, 6), (iCalmecac, 6), by=1650),
		EnslaveCount(20, excluding=group(iCivGroupAmerica).named(EUROPEAN)),
	),
	iMughals: (
		BuildingCount(iIslamicCathedral, 3, by=1500),
		Wonders(iRedFort, iShalimarGardens, iTajMahal, by=1660),
		CultureAmount(50000, at=1750),
	),
	iRussia: (
		All(
			SettledCities(7, area=plots.regions(rSiberia, rCentralAsianSteppe, rAmur).named(SIBERIA), by=1700),
			RouteConnection([iRouteRailroad], plots.capitals(iRussia).named(MOSCOW), plots.regions(rSiberia, rAmur).adjacent_regions(rSeaOfJapan, rSeaOfOkhotsk, rBeringSea).named(SIBERIAN_COAST), by=1920),
		),
		Projects(iManhattanProject, iLunarLanding),
		All(
			Communist(),
			AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 5, bCommunist=True),
			by=1950,
		),
	),
	iOttomans: (
		CityBuildingCount(capital().named(CAPITAL), wonders(), 4, at=1550),
		All(
			CultureCover(
				plots.regions(rBalkans, rGreece, rAnatolia, rLevant, rEgypt).adjacent_region(rMediterraneanSea).named(EASTERN_MEDITERRANEAN),
				plots.all().adjacent_region(rBlackSea).named(BLACK_SEA),
			),
			Control(
				plots.surrounding(tCairo).named(CAIRO),
				plots.surrounding(tMecca).named(MECCA),
				plots.surrounding(tBaghdad).named(BAGHDAD),
				plots.surrounding(tVienna).named(VIENNA),
			),
			by=1700,
		),
		MoreCulture(group(iCivGroupEurope).named(ALL_EUROPEAN), at=1800),
	),
	iThailand: (
		OpenBorderCount(10, at=1650),
		BestPopulationCity(start(iThailand).named(AYUTTHAYA), at=1700),
		AllowOnly(plots.regions(rDravida, rDeccan, rBengal, rIndochina, rIndonesia).named(SOUTH_ASIA), civs(*lSouthAsianCivs).named(LOCAL), at=1900),
	),
	iCongo: (
		ReligiousVotePercent(15, by=1650),
		SlaveTradeGold(1000, by=1800),
		EnterEraBefore(iIndustrial, iGlobal),
	),
	iIran: (
		OpenBorderCount(6, civs=group(iCivGroupEurope).named(EUROPEAN), by=1650),
		Control(
			plots.region(rMesopotamia).named(MESOPOTAMIA),
			plots.region(rTransoxiana).named(TRANSOXIANA),
			plots.region(rPunjab).named(PUNJAB),
			at=1750,
		),
		CultureCity(20000, at=1800),
	),
	iNetherlands: (
		CitySpecialistCount(start(iNetherlands).named(AMSTERDAM), iSpecialistGreatMerchant, 3, at=1745),
		ConqueredCities(4, civs=group(iCivGroupEurope).named(EUROPEAN), outside=plots.regions(*lEurope).named(EUROPE), by=1745),
		ResourceCount(iSpices, 7, by=1775),
	),
	iGermany: (
		CitySpecialistCount(start(iGermany).named(BERLIN), great_people(), 7, at=1900),
		Control(
			plots.core(iItaly), # TODO: define in locations or use region
			plots.core(iFrance), # TODO: define in locations or use region
			plots.core(iEngland), # TODO: define in locations or use region
			plots.core(iVikings).named(SCANDINAVIA), # TODO: define in locations or use region
			plots.core(iRussia), # TODO: define in locations or use region
			at=1940,
		),
		EraFirstDiscover((iIndustrial, 8), (iGlobal, 8)),
	),
	iAmerica: (
		All(
			AllowNone(group(iCivGroupEurope).named(EUROPEAN), plots.regions(*(lNorthAmerica + lCentralAmerica)).named(NORTH_CENTRAL_AMERICA)),
			Control(plots.core(iMexico), subject=VASSALS),
			at=1900,
		),
		Wonders(iStatueOfLiberty, iBrooklynBridge, iEmpireStateBuilding, iGoldenGateBridge, iPentagon, iUnitedNations, by=1950),
		All(
			CommercePercent(75, subject=ALLIES),
			PowerPercent(75, subject=ALLIES),
			by=1990,
		),
	),
	iArgentina: (
		GoldenAges(2, by=1930),
		CityCultureLevel(start(iArgentina).named(BUENOS_AIRES), iCultureLevelLegendary, by=1960),
		GoldenAges(6, by=2000),
	),
	iMexico: (
		BuildingCount(state_religion_building(cathedral).named(STATE_RELIGION_CATHEDRAL), 3, by=1880),
		GreatGenerals(3, by=1940),
		BestPopulationCity(start(iMexico).named(MEXICO_CITY), at=1960),
	),
	iColombia: (
		AllowNone(
			group(iCivGroupEurope).named(EUROPEAN),
			plots.region(rNewGranada).named(GRAN_COLOMBIA),
			plots.region(rAndes).named(ANDES),
			at=1870,
		),
		Control(
			plots.regions(*lSouthAmerica).named(SOUTH_AMERICA),
			at=1920,
		),
		ResourceTradeGold(3000, by=1950),
	),
	iBrazil: (
		ImprovementCount((iSlavePlantation, 8), (iPasture, 4), at=1880),
		Wonders(iWembley, iCristoRedentor, iItaipuDam),
		All(
			ImprovementCount(iForestPreserve, 20),
			CityBuilding(capital().named(CAPITAL), iNationalPark),
			by=1950,
		),
	),
	iCanada: (
		All(
			RouteConnection([iRouteRailroad], capital().named(CAPITAL), plots.regions(rMaritimes, rQuebec).adjacent_region(rAtlanticOcean).named(ATLANTIC_COAST)),
			RouteConnection([iRouteRailroad], capital().named(CAPITAL), plots.regions(rCascadia, rAmericanArctic).adjacent_region(rPacificOcean).named(PACIFIC_COAST)),
			by=1920,
		),
		All(
			Control((plots.regions(rMaritimes, rQuebec, rOntario) + plots.regions(rGreatPlains, rCascadia).where(lambda p: p.getY() >= iCanadianNorthSouthBorder) + plots.region(rAmericanArctic).where(lambda p: p.getX() >= iCanadianEastWestBorder)).named(CITIES_IN_CANADA)),
			AreaPercent((plots.regions(rMaritimes, rQuebec, rOntario) + plots.regions(rGreatPlains, rCascadia).where(lambda p: p.getY() >= iCanadianNorthSouthBorder) + plots.region(rAmericanArctic).where(lambda p: p.getX() >= iCanadianEastWestBorder)).named(CANADIAN_TERRITORY), 90),
			NoCityConquered(),
			by=1950,
		),
		BrokeredPeace(12, by=2000),
	),
}


for iCiv, goals in dGoals.items():
	for index, goal in enumerate(goals):
		title_key = "TXT_KEY_VICTORY_TITLE_%s%s" % (infos.civ(iCiv).getIdentifier(), index+1)
		goal.options["title_key"] = title_key


def descriptions(iCiv):
	for goal in dGoals[iCiv]:
		print goal.description()