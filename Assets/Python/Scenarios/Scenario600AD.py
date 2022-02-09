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
		
