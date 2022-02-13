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
		iPlayer = slot(iCiv)
		city = getBuildingCity(iWonder, False)
		if city and iPlayer >= 0:
			city.setBuildingOriginalOwner(iWonder, iPlayer)

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

