from Civilizations import initScenarioTechs
from Civilization import Civilization
from Resources import setupScenarioResources

from Locations import *
from RFCUtils import *
from Core import *


class Scenario(object):
	
	iStartYear = 1700
	lInitialCivs = [iChina, iIndia, iTamils, iKorea, iJapan, iVikings, iTurks, iSpain, iFrance, iEngland, iHolyRome, iRussia, iPoland, iPortugal, iMughals, iOttomans, iThailand, iCongo, iIran, iNetherlands, iGermany]
	fileName = "RFC_1700AD"
	
	lCivilizations = [
		Civilization(
			iChina,
			iLeader=iHongwu,
			sLeaderName="TXT_KEY_LEADER_KANGXI",
			iGold=300,
			iStateReligion=iConfucianism,
			lCivics=[iDespotism, iMeritocracy, iManorialism, iRegulatedTrade, iMonasticism, iIsolationism],
			dAttitudes={iKorea: 2}
		),
		Civilization(
			iIndia,
			iLeader=iShivaji,
			iGold=400,
			iStateReligion=iHinduism,
			lCivics=[iMonarchy, iVassalage, iCasteSystem, iRegulatedTrade, iMonasticism, iConquest],
			dAttitudes={iMughals: -2}
		),
		Civilization(
			iIran,
			iLeader=iAbbas,
			iGold=200,
			iStateReligion=iIslam,
			lCivics=[iMonarchy, iVassalage, iSlavery, iMerchantTrade, iTheocracy, iConquest],
			dAttitudes={iMughals: -2, iOttomans: -4}
		),
		Civilization(
			iTamils,
			iLeader=iKrishnaDevaRaya,
			sLeaderName="TXT_KEY_LEADER_TIPU_SULTAN",
			iGold=400,
			iStateReligion=iHinduism,
			lCivics=[iMonarchy, iCentralism, iCasteSystem, iMerchantTrade, iMonasticism, iConquest],
		),
		Civilization(
			iKorea,
			iLeader=iSejong,
			iGold=200,
			iStateReligion=iConfucianism,
			lCivics=[iDespotism, iMeritocracy, iCasteSystem, iRegulatedTrade, iMonasticism, iIsolationism],
			dAttitudes={iChina: 2}
		),
		Civilization(
			iJapan,
			iLeader=iOdaNobunaga,
			iGold=400,
			iStateReligion=iBuddhism,
			lCivics=[iMonarchy, iVassalage, iManorialism, iRegulatedTrade, iMonasticism, iIsolationism],
		),
		Civilization(
			iVikings, # Sweden
			iLeader=iGustav,
			iGold=150,
			iStateReligion=iProtestantism,
			lCivics=[iMonarchy, iCentralism, iManorialism, iRegulatedTrade, iClergy],
			dAttitudes={iRussia: -2, iPoland: -2}
		),
		Civilization(
			iTurks, # Uzbeks
			iLeader=iTamerlane,
			iGold=50,
			iStateReligion=iIslam,
			lCivics=[iDespotism, iVassalage, iSlavery, iMerchantTrade, iClergy, iTributaries],
		),
		Civilization(
			iSpain,
			iLeader=iPhilip,
			iGold=400,
			iStateReligion=iCatholicism,
			lCivics=[iMonarchy, iCentralism, iManorialism, iRegulatedTrade, iTheocracy, iColonialism],
			dAttitudes={iPortugal: 2}
		),
		Civilization(
			iFrance,
			iLeader=iLouis,
			iGold=400,
			iStateReligion=iCatholicism,
			lCivics=[iMonarchy, iCentralism, iIndividualism, iRegulatedTrade, iClergy, iColonialism],
			dAttitudes={iEngland: -4, iHolyRome: -2, iOttomans: -2, iNetherlands: 2}
		),
		Civilization(
			iEngland,
			iLeader=iVictoria,
			iGold=600,
			iStateReligion=iProtestantism,
			lCivics=[iMonarchy, iCentralism, iIndividualism, iFreeEnterprise, iTolerance, iColonialism],
			dAttitudes={iFrance: -4, iPortugal: 2, iMughals: -2, iOttomans: -2}
		),
		Civilization(
			iHolyRome, # Austria
			iLeader=iFrancis,
			iGold=150,
			iStateReligion=iCatholicism,
			lCivics=[iMonarchy, iVassalage, iManorialism, iRegulatedTrade, iClergy],
			dAttitudes={iFrance: -2, iOttomans: -4}
		),
		Civilization(
			iRussia,
			iLeader=iPeter,
			iGold=350,
			iStateReligion=iOrthodoxy,
			lCivics=[iDespotism, iCentralism, iManorialism, iRegulatedTrade, iTheocracy],
			dAttitudes={iVikings: -2, iOttomans: -4}
		),
		Civilization(
			iPoland,
			iLeader=iSobieski,
			iGold=200,
			iStateReligion=iCatholicism,
			lCivics=[iElective, iCentralism, iManorialism, iRegulatedTrade, iClergy],
		),
		Civilization(
			iPortugal,
			iLeader=iJoao,
			iGold=450,
			iStateReligion=iCatholicism,
			lCivics=[iMonarchy, iCentralism, iManorialism, iRegulatedTrade, iClergy, iColonialism],
			dAttitudes={iSpain: 2, iEngland: 2, iNetherlands: -2}
		),
		Civilization(
			iMughals,
			iLeader=iAkbar,
			iGold=200,
			iStateReligion=iIslam,
			lCivics=[iDespotism, iVassalage, iManorialism, iRegulatedTrade, iClergy, iTributaries],
			dAttitudes={iEngland: -2, iIndia: -2, iIran: -2}
		),
		Civilization(
			iOttomans,
			iLeader=iSuleiman,
			iGold=200,
			iStateReligion=iIslam,
			lCivics=[iDespotism, iMeritocracy, iSlavery, iRegulatedTrade, iTheocracy, iTributaries],
			dAttitudes={iIran: -4, iHolyRome: -4, iRussia: -4, iPoland: -2, iFrance: -2, iEngland: -2, iNetherlands: -2}
		),
		Civilization(
			iThailand,
			iLeader=iNaresuan,
			iGold=300,
			iStateReligion=iBuddhism,
			lCivics=[iMonarchy, iVassalage, iCasteSystem, iRegulatedTrade, iMonasticism, iTributaries],
		),
		Civilization(
			iCongo,
			iLeader=iMbemba,
			iGold=300,
			iStateReligion=iCatholicism,
			lCivics=[iElective, iVassalage, iSlavery, iRegulatedTrade, iClergy],
		),
		Civilization(
			iNetherlands,
			iLeader=iWilliam,
			iGold=800,
			iStateReligion=iProtestantism,
			lCivics=[iRepublic, iCentralism, iIndividualism, iFreeEnterprise, iTolerance, iColonialism],
			dAttitudes={iFrance: 2, iPortugal: -2, iOttomans: -2}
		),
		Civilization(
			iGermany,
			iLeader=iFrederick,
			iGold=800,
			iStateReligion=iProtestantism,
			lCivics=[iMonarchy, iCentralism, iManorialism, iRegulatedTrade, iClergy, iConquest]
		),
	]
	
	@classmethod
	def initScenario(cls):
		initScenarioTechs()
		createStartingUnits()
		
		setupScenarioResources()
		adjustTerritories()
		updateGreatWall()
		
		adjustReligionFoundingDates()
		adjustWonders()
		adjustGreatPeople()
		adjustColonists()
		
		initDiplomacy()
		
		for civilization in cls.lCivilizations:
			civilization.apply()
	

def createStartingUnits():
	# Japan
	capital = plots.capital(iJapan)
	if not player(iJapan).isHuman():
		createRoleUnit(iJapan, capital, iSettle)
	
def updateGreatWall():
	tGraphicsTL = (99, 46)
	tGraphicsBR = (106, 49)
	lExceptions = [(99, 47), (99, 48), (99, 49), (100, 49), (101, 49), (104, 49)]
	lClearCulture = [(103, 50), (104, 50), (105, 50), (106, 50)]
	
	beijing = city(tBeijing)
	greatWall = plots.rectangle(tGraphicsTL, tGraphicsBR)
	
	iOldArea = beijing.getArea()
	iNewArea = plots.capital(iAmerica).getArea()
	
	for plot in greatWall.expand(1).land():
		if at(plot, (99, 45)):
			continue
		plot.setArea(iNewArea)
		
	for plot in plots.of(lClearCulture):
		plot.setOwner(-1)
		
	for plot in greatWall.without(lExceptions):
		plot.setOwner(beijing.getOwner())
	
	tWestTL = (99, 40)
	tWestBR = (104, 49)
	
	tEastTL = (103, 39)
	tEastBR = (107, 45)

	for plot in plots.rectangle(tWestTL, tWestBR).without(lExceptions) + plots.rectangle(tEastTL, tEastBR):
		if not plot.isWater():
			plot.setWithinGreatWall(True)
			
def adjustTerritories():
	dAdjustedTiles = {
		iHolyRome : [(62, 51)],
		iRussia : [(69, 54), (69, 55)],
		iPortugal : [(47, 45), (48, 45), (49, 40), (50, 42), (50, 43), (50, 44)],
		iPoland : [(64, 53), (65, 56), (66, 55), (66, 56), (68, 53), (68, 54), (68, 56)],
		iNetherlands : [(58, 52), (58, 53)],
		iGermany : [(58, 49), (59, 49), (60, 49)],
	}
	
	for plot in plots.all():
		if plot.isOwned():
			plot.changeCulture(plot.getOwner(), 100, False)
			convertPlotCulture(plot, plot.getOwner(), 100, False)
	
	for iCiv, lTiles in dAdjustedTiles.items():
		for plot in plots.of(lTiles):
			convertPlotCulture(plot, slot(iCiv), 100, True)

def adjustReligionFoundingDates():
	lReligionFoundingYears = [-2000, 40, 500, 1521, 622, -1500, 80, -500, -400, -600]

	for iReligion, iReligionFoundingYear in enumerate(lReligionFoundingYears):
		if game.isReligionFounded(iReligion):
			game.setReligionGameTurnFounded(iReligion, year(iReligionFoundingYear))
	
def adjustWonders():
	lExpiredWonders = [iOracle, iIshtarGate, iHangingGardens, iGreatCothon, iApadanaPalace, 
					   iColossus, iStatueOfZeus, iGreatMausoleum, iTempleOfArtemis, iAquaAppia, 
				       iAlKhazneh, iJetavanaramaya, iGreatLighthouse, iMoaiStatues, iFlavianAmphitheatre, 
				       iGreatLibrary, iGondeshapur, iSilverTreeFountain, iAlamut]
	for iWonder in lExpiredWonders:
		game.incrementBuildingClassCreatedCount(infos.building(iWonder).getBuildingClassType())
	
	dWonderOriginalOwners = {
		iGreatLighthouse : (iEgypt, -284),
		iGreatLibrary : (iEgypt, -285),
		iPyramids : (iEgypt, -2600),
		iGreatSphinx : (iEgypt, -2500),
		iSalsalBuddha : (iIndependent, 570),
		iJewishShrine : (iIndependent, -957),
		iShwedagonPaya : (iIndependent, 1362),
		iCatholicShrine : (iRome, 318),
		iTaoistShrine : (iChina, 1460),
		iGreatWall : (iChina, -221),
		iConfucianShrine : (iChina, -205),
		iDujiangyan : (iChina, -256),
		iTerracottaArmy : (iChina, -210),
		iForbiddenPalace : (iChina, 1420),
		iGrandCanal : (iChina, 618),
		iPorcelainTower : (iChina, 1431),
		iParthenon : (iGreece, -438),
		iHinduShrine : (iIndia, -322),
		iBuddhistShrine : (iIndia, -260),
		iIronPillar : (iIndia, 375),
		iNalanda : (iIndia, 427),
		iVijayaStambha : (iIndia, 1448),
		iKhajuraho : (iIndia, 885),
		iZoroastrianShrine : (iPersia, -400),
		iGondeshapur : (iPersia, 256),
		iFlavianAmphitheatre : (iRome, 80),
		iTempleOfKukulkan : (iMaya, 800),
		iMonolithicChurch : (iEthiopia, 1181),
		iJetavanaramaya : (iTamils, 273),
		iCheomseongdae : (iKorea, 632),
		iOrthodoxShrine : (iByzantium, 335),
		iTheodosianWalls : (iByzantium, 413),
		iHagiaSophia : (iByzantium, 537),
		iMountAthos : (iByzantium, 800),
		iItsukushimaShrine : (iJapan, 593),
		iHimejiCastle : (iJapan, 1333),
		iGurEAmir : (iTurks, 1404),
		iDomeOfTheRock : (iArabia, 692),
		iSpiralMinaret : (iArabia, 851),
		iIslamicShrine : (iArabia, 692),
		iHouseOfWisdom : (iArabia, 754),
		iPotalaPalace : (iTibet, 1694),
		iBorobudur : (iIndonesia, 825),
		iPrambanan : (iIndonesia, 850),
		iEscorial : (iSpain, 1584),
		iMezquita : (iMoors, 785),
		iNotreDame : (iFrance, 1260),
		iVersailles : (iFrance, 1661),
		iLouvre : (iFrance, 1692),
		iKrakDesChevaliers : (iFrance, 1140),
		iWatPreahPisnulok : (iKhmer, 1113),
		iOxfordUniversity : (iEngland, 1096),
		iProtestantShrine : (iHolyRome, 1503),
		iSaintThomasChurch : (iHolyRome, 1496),
		iSaintSophia : (iRussia, 1031),
		iKremlin : (iRussia, 1495),
		iSaintBasilsCathedral : (iRussia, 1561),
		iUniversityOfSankore : (iMali, 988),
		iOldSynagogue : (iPoland, 1407),
		iTorreDeBelem : (iPortugal, 1519),
		iSantaMariaDelFiore : (iItaly, 1436),
		iSanMarcoBasilica : (iItaly, 1063),
		iSistineChapel : (iItaly, 1541),
		iFloatingGardens : (iAztecs, 1350),
		iShalimarGardens : (iMughals, 1642),
		iHarmandirSahib : (iMughals, 1604),
		iTajMahal : (iMughals, 1653),
		iRedFort : (iMughals, 1648),
		iTopkapiPalace : (iOttomans, 1465),
		iBlueMosque : (iOttomans, 1616),
		iImageOfTheWorldSquare : (iIran, 1629),
		iBourse : (iNetherlands, 1602),
	}
	
	for iWonder, (iCiv, iYear) in dWonderOriginalOwners.items():
		city = getBuildingCity(iWonder, False)
		iYear = game.getTurnYear(year(min(iYear, scenarioStartYear())))
		if city:
			city.setBuildingOriginalOwner(iWonder, iCiv)
			city.setBuildingOriginalTime(iWonder, iYear)

def adjustGreatPeople():
	dGreatPeopleCreated = {
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
	
	dGreatGeneralsCreated = {
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

	for iCiv, iGreatPeople in dGreatGeneralsCreated.items():
		player(iCiv).changeGreatPeopleCreated(iGreatPeople)
	
	for iCiv, iGreatGenerals in dGreatGeneralsCreated.items():
		player(iCiv).changeGreatGeneralsCreated(iGreatGenerals)
			
def adjustColonists():
	dColonistsAlreadyGiven = {
		iVikings : 1,
		iSpain : 7,
		iFrance : 3,
		iEngland : 3,
		iPortugal : 6,
		iNetherlands : 4,
	}
	
	iStartTurn = scenarioStartTurn()
	
	for iCiv, iColonists in dColonistsAlreadyGiven.items():
		data.players[iCiv].iExplorationTurn = iStartTurn
		data.players[iCiv].iColonistsAlreadyGiven = iColonists

def initDiplomacy():
	team(iEngland).declareWar(player(iMughals).getTeam(), False, WarPlanTypes.WARPLAN_LIMITED)
	team(iIndia).declareWar(player(iMughals).getTeam(), False, WarPlanTypes.WARPLAN_TOTAL)

