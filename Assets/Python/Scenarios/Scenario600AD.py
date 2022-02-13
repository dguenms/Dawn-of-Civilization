from Civilizations import initScenarioTechs
from Civilization import Civilization
from Resources import setupScenarioResources

from Locations import *
from RFCUtils import *
from Core import *


class Scenario(object):
	
	iStartYear = 600
	lInitialCivs = [iChina, iKorea, iByzantium, iJapan, iTurks, iVikings]
	fileName = "RFC_600AD"
	
	lCivilizations = [
		Civilization(
			iChina, 
			iLeader=iTaizong, 
			iGold=300,
			iStateReligion=iConfucianism,
			lCivics = [iDespotism, iCitizenship, iManorialism, iMerchantTrade, iMonasticism]
		),
		Civilization(
			iKorea,
			iGold=200,
			iStateReligion=iBuddhism,
			lCivics = [iDespotism, iCitizenship, iCasteSystem, iRedistribution, iMonasticism]
		),
		Civilization(
			iByzantium,
			iGold=400,
			iStateReligion=iOrthodoxy,
			lCivics = [iDespotism, iVassalage, iManorialism, iMerchantTrade, iClergy]
		),
		Civilization(
			iJapan,
			iGold=300,
			iStateReligion=iBuddhism,
			lCivics = [iMonarchy, iVassalage, iCasteSystem, iRedistribution, iDeification]
		),
		Civilization(
			iVikings,
			iGold=150,
			lCivics = [iElective, iVassalage, iSlavery, iMerchantTrade, iConquest]
		),
		Civilization(
			iTurks,
			iGold=100,
			lCivics = [iDespotism, iVassalage, iSlavery, iMerchantTrade, iConquest]
		),
		Civilization(
			iIndependent,
			iGold=100,
		),
		Civilization(
			iIndependent2,
			iGold=100,
		),
		Civilization(
			iNative,
			iGold=300,
		)
	]
	
	@classmethod
	def initScenario(cls):
		initScenarioTechs()
		createStartingUnits()
		
		setupScenarioResources()
		updateGreatWall()
		
		adjustReligionFoundingDates()
		adjustWonders()
		adjustGreatPeople()
		
		for civilization in cls.lCivilizations:
			civilization.apply()


def createStartingUnits():
	# Japan
	capital = plots.capital(iJapan)
	if not player(iJapan).isHuman():
		makeUnits(iJapan, iCrossbowman, capital, 2)
		makeUnits(iJapan, iSamurai, capital, 3)
	
	# Byzantium
	capital = plots.capital(iByzantium)
	createRoleUnit(iByzantium, capital, iTransport, 2)
	createRoleUnit(iByzantium, capital, iAttackSea, 2)
	
	# Vikings
	capital = plots.capital(iVikings)
	createRoleUnit(iVikings, capital, iWorkerSea)
	createRoleUnit(iVikings, capital, iExploreSea, player(iVikings).isHuman() and 2 or 3)
	
	if player(iVikings).isHuman():
		createRoleUnit(iVikings, capital, iSettleSea)
		createRoleUnit(iVikings, capital, iSettle)
		createRoleUnit(iVikings, capital, iDefend, 2)
	else:
		makeUnit(iVikings, iSettler, (60, 56))
		makeUnit(iVikings, iArcher, (60, 56))
		makeUnit(iVikings, iSettler, (63, 59))
		makeUnit(iVikings, iArcher, (63, 59))
	
	# Korea
	capital = plots.capital(iKorea)
	if not player(iKorea).isHuman():
		makeUnits(iKorea, iHeavySwordsman, capital, 2)
	

def updateGreatWall():
	tGraphicsTL = (99, 46)
	tGraphicsBR = (104, 49)
	lExceptions = [(99, 47), (99, 48), (99, 49), (100, 49), (101, 49), (104, 49)]
	
	beijing = city(tBeijing)
	greatWall = plots.rectangle(tGraphicsTL, tGraphicsBR)
	
	iOldArea = beijing.getArea()
	iNewArea = plots.capital(iAmerica).getArea()
	
	for plot in greatWall.expand(1).land():
		if at(plot, (99, 45)):
			continue
		plot.setArea(iNewArea)
	
	for plot in greatWall.without(lExceptions):
		plot.setOwner(beijing.getOwner())
	
	beijing.updateGreatWall()
	
	tWestTL = (99, 40)
	tWestBR = (104, 49)
	
	tEastTL = (103, 39)
	tEastBR = (107, 45)

	for plot in plots.rectangle(tWestTL, tWestBR).without(lExceptions) + plots.rectangle(tEastTL, tEastBR):
		if not plot.isWater():
			plot.setWithinGreatWall(True)

def adjustReligionFoundingDates():
	lReligionFoundingYears = [-2000, 40, 500, 1521, 622, -1500, 80, -500, -400, -600]

	for iReligion, iReligionFoundingYear in enumerate(lReligionFoundingYears):
		if game.isReligionFounded(iReligion):
			game.setReligionGameTurnFounded(iReligion, year(iReligionFoundingYear))
	
def adjustWonders():
	lExpiredWonders = [iOracle, iIshtarGate, iTerracottaArmy, iHangingGardens, iGreatCothon, 
					   iApadanaPalace, iColossus, iStatueOfZeus, iGreatMausoleum, iTempleOfArtemis, 
					   iAquaAppia, iAlKhazneh, iJetavanaramaya]
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
		iChina: 4,
		iKorea: 1,
		iByzantium: 1,
	}
	
	dGreatGeneralsCreated = {
		iChina: 1
	}

	for iCiv, iGreatPeople in dGreatGeneralsCreated.items():
		player(iCiv).changeGreatPeopleCreated(iGreatPeople)
	
	for iCiv, iGreatGenerals in dGreatGeneralsCreated.items():
		player(iCiv).changeGreatGeneralsCreated(iGreatGenerals)
		
