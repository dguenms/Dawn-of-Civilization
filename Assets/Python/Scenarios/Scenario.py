from Civilizations import Civilizations
from Resources import setupScenarioResources
from DynamicCivs import startingLeader

from Core import *
from RFCUtils import *


RELIGION_FOUNDING_DATES = {
	iJudaism: -2000,
	iOrthodoxy: 40,
	iCatholicism: 500,
	iProtestantism: 1521,
	iIslam: 622,
	iHinduism: -1500,
	iBuddhism: 80,
	iConfucianism: -500,
	iTaoism: -400,
	iZoroastrianism: -600
}

WONDER_ORIGINAL_BUILDERS = {
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


# used: Rise, Scenario
def addPlayer(iCiv, bMinor=False):
	iPlayer = findSlot(iCiv)
	iLeader = startingLeader(iCiv)
	game.addPlayer(iPlayer, iLeader, iCiv)
	
	data.dSlots[iCiv] = iPlayer
	
	if bMinor:
		player(iPlayer).setMinorCiv(True)


class GreatWall(object):

	def __init__(self, *args, **kwargs):
		self.tGraphicsTL = kwargs.get("tGraphicsTL")
		self.tGraphicsBR = kwargs.get("tGraphicsBR")
		self.lGraphicsExceptions = kwargs.get("lGraphicsExceptions", [])
		self.lBorderExceptions = kwargs.get("lBorderExceptions", [])
		self.lClearCulture = kwargs.get("lClearCulture", [])
		
		self.lEffectAreas = kwargs.get("lEffectAreas", [])
		
	def apply(self):
		city = getBuildingCity(iGreatWall, False)
		if not city:
			return
			
		iOwner = city.getOwner()
		iOldArea = city.getArea()
		iNewArea = plots.capital(iAmerica).getArea()
		
		greatWall = plots.rectangle(self.tGraphicsTL, self.tGraphicsBR)
		
		for plot in greatWall.expand(1).land().without(self.lBorderExceptions):
			plot.setArea(iNewArea)
			
		for plot in plots.of(self.lClearCulture):
			plot.setOwner(-1)
		
		for plot in greatWall.without(self.lGraphicsExceptions):
			plot.setOwner(iOwner)
		
		for plot in plots.sum(plots.rectangle(*tCorners).without(self.lGraphicsExceptions).land() for tCorners in self.lEffectAreas):
			plot.setWithinGreatWall(True)
			

class Scenario(object):

	def __init__(self, *args, **kwargs):
		self.iStartYear = kwargs.get("iStartYear")
		self.fileName = kwargs.get("fileName")
		
		self.lCivilizations = kwargs.get("lCivilizations", [])
		
		self.dOwnedTiles = kwargs.get("dOwnedTiles", {})
		self.iOwnerBaseCulture = kwargs.get("iOwnerBaseCulture", 0)
		
		self.lExpiredWonders = kwargs.get("lExpiredWonders", [])
		
		self.dGreatPeopleCreated = kwargs.get("dGreatPeopleCreated", {})
		self.dGreatGeneralsCreated = kwargs.get("dGreatGeneralsCreated", {})
		
		self.dColonistsAlreadyGiven = kwargs.get("dColonistsAlreadyGiven", {})
		
		self.lInitialWars = kwargs.get("lInitialWars", [])
		
		self.createStartingUnits = kwargs.get("createStartingUnits", lambda: None)
		
		self.greatWall = kwargs.get("greatWall", GreatWall())
		
	def setupCivilizations(self):
		for i, iCiv in enumerate(lBirthOrder):
			infos.civ(iCiv).setDescription("%02d" % i)
			
		for iCiv in range(iNumCivs):
			iCivStartYear = infos.civ(iCiv).getStartingYear()
			infos.civ(iCiv).setPlayable(iCivStartYear != 0 and iCivStartYear >= self.iStartYear)
		
		for civ in self.lCivilizations:
			civ.info.setPlayable(civ.isPlayable())
	
	def init(self):
		for civ in self.lCivilizations:
			iCiv = civ.iCiv
			
			if game.getActiveCivilizationType() == iCiv:
				continue
			
			addPlayer(iCiv, bMinor=not civ.isPlayable())
	
		events.fireEvent("playerCivAssigned", game.getActivePlayer(), game.getActiveCivilizationType())
		events.fireEvent("playerCivAssigned", gc.getBARBARIAN_PLAYER(), iBarbarian)

		data.dSlots[game.getActiveCivilizationType()] = game.getActivePlayer()
		data.dSlots[iBarbarian] = gc.getBARBARIAN_PLAYER()
		
	def apply(self):
		for civilization in self.lCivilizations:
			civilization.apply()
		
		setupScenarioResources()
		
		self.createStartingUnits()
		
		self.greatWall.apply()
		self.adjustTerritories()
		
		self.adjustReligions()
		self.adjustWonders()
		self.adjustGreatPeople()
		self.adjustColonists()
		
		self.initDiplomacy()
	
	def adjustTerritories(self):
		for plot in plots.all():
			if plot.isOwned():
				plot.changeCulture(plot.getOwner(), self.iOwnerBaseCulture, False)
				convertPlotCulture(plot, plot.getOwner(), 100, False)
		
		for iCiv, lTiles in self.dOwnedTiles.items():
			for plot in plots.of(lTiles):
				convertPlotCulture(plot, slot(iCiv), 100, True)
	
	def adjustReligions(self):
		for iReligion, iFoundingYear in RELIGION_FOUNDING_DATES.items():
			if game.isReligionFounded(iReligion):
				game.setReligionGameTurnFounded(iReligion, year(iFoundingYear))
		
		game.setVoteSourceReligion(1, iCatholicism, False)
	
	def adjustWonders(self):
		for iWonder in self.lExpiredWonders:
			game.incrementBuildingClassCreatedCount(infos.building(iWonder).getBuildingClassType())
			
		for iWonder, (iCiv, iYear) in WONDER_ORIGINAL_BUILDERS.items():
			city = getBuildingCity(iWonder, False)
			iYear = game.getTurnYear(year(min(iYear, self.iStartYear)))
			if city:
				city.setBuildingOriginalOwner(iWonder, iCiv)
				city.setBuildingOriginalTime(iWonder, iYear)
	
	def adjustGreatPeople(self):
		for iCiv, iGreatPeople in self.dGreatPeopleCreated.items():
			player(iCiv).changeGreatPeopleCreated(iGreatPeople)
		
		for iCiv, iGreatGenerals in self.dGreatGeneralsCreated.items():
			player(iCiv).changeGreatPeopleCreated(iGreatGenerals)
	
	def adjustColonists(self):
		iStartTurn = scenarioStartTurn()
		
		for iCiv, iColonists in self.dColonistsAlreadyGiven.items():
			data.players[iCiv].iExplorationTurn = iStartTurn
			data.players[iCiv].iColonistsAlreadyGiven = iColonists
	
	def initDiplomacy(self):
		for iAttacker, iDefender, iWarPlan in self.lInitialWars:
			team(iAttacker).declareWar(player(iDefender).getTeam(), False, iWarPlan)
