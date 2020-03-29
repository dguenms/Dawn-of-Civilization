# Rhye's and Fall of Civilization - Main Scenario

from CvPythonExtensions import *
import CvUtil
from PyHelpers import PyPlayer
import Popup
from StoredData import data # edead
import CvTranslator
from RFCUtils import *
from Consts import *
import CityNameManager as cnm
import Victory as vic
import DynamicCivs as dc
from operator import itemgetter
import Stability as sta
import Areas
import Civilizations
import Modifiers
import CvEspionageAdvisor
import BugCore
import Periods as periods

from Core import *

MainOpt = BugCore.game.MainInterface

################
### Globals ###
##############

iCheatersPeriod = 12
iBetrayalPeriod = 8
iBetrayalThreshold = 80
iRebellionDelay = 15
iEscapePeriod = 30

### Screen popups ###
# (Slowly migrate event handlers here when rewriting to use BUTTONPOPUP_PYTHON and more idiomatic code)

def startNewCivSwitchEvent(iPlayer):
	if MainOpt.isSwitchPopup():
		popup = CyPopupInfo()
		popup.setText(text("TXT_KEY_INTERFACE_NEW_CIV_SWITCH", adjective(iPlayer)))
		popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popup.setOnClickedPythonCallback("applyNewCivSwitchEvent")
		
		popup.setData1(iPlayer)
		popup.addPythonButton(text("TXT_KEY_POPUP_NO"), infos.art('INTERFACE_EVENT_BULLET'))
		popup.addPythonButton(text("TXT_KEY_POPUP_YES"), infos.art('INTERFACE_EVENT_BULLET'))
		
		popup.addPopup(human())
	
def applyNewCivSwitchEvent(argsList):
	iButton = argsList[0]
	iPlayer = argsList[1]
	
	if iButton == 1:
		handleNewCiv(iPlayer)
		
### Utility methods ###

def handleNewCiv(iPlayer):
	iPreviousPlayer = human()
	iOldHandicap = player().getHandicapType()
	
	pPlayer = player(iPlayer)
	
	player().setHandicapType(pPlayer.getHandicapType())
	game.setActivePlayer(iPlayer, False)
	pPlayer.setHandicapType(iOldHandicap)
	
	for iMaster in players.major():
		if team(iPlayer).isVassal(iMaster):
			team(iPlayer).setVassal(iMaster, False, False)
	
	data.bAlreadySwitched = True
	player(iPlayer).setPlayable(True)
	
	if game.getWinner() == iPreviousPlayer:
		game.setWinner(-1, -1)
	
	data.resetHumanStability()

	for city in cities.owner(iPlayer):
		city.setInfoDirty(True)
		city.setLayoutDirty(True)
					
	for i in range(3):
		data.players[iPlayer].lGoals[i] = -1
					
	if infos.constant('NO_AI_UHV_CHECKS') == 1:
		vic.loseAll(iPreviousPlayer)
		
	for iLoopPlayer in players.major():
		player(iPlayer).setEspionageSpendingWeightAgainstTeam(iLoopPlayer, 0)

class RiseAndFall:

###############
### Popups ###
#############

	def scheduleFlipPopup(self, iNewPlayer, lPlots):
		data.lTempEvents.append((iNewPlayer, lPlots))
		self.checkFlipPopup()

	def checkFlipPopup(self):
		for tEvent in data.lTempEvents:
			iNewPlayer, lPlots = tEvent
			self.flipPopup(iNewPlayer, lPlots)

	def flipPopup(self, iNewPlayer, lPlots):
		flipText = text("TXT_KEY_FLIPMESSAGE1")
		
		for city in self.getConvertedCities(iNewPlayer, lPlots):
			flipText += city.getName() + "\n"
			
		flipText += text("TXT_KEY_FLIPMESSAGE2")
							
		popup(7615, text("TXT_KEY_NEWCIV_TITLE"), flipText, (text("TXT_KEY_POPUP_YES"), text("TXT_KEY_POPUP_NO")))
		data.iFlipNewPlayer = iNewPlayer
		data.iFlipOldPlayer = human()
		data.lTempPlots = lPlots

	def eventApply7615(self, popupReturn):
		lPlots = data.lTempPlots
		iFlipNewPlayer = data.iFlipNewPlayer
		
		iNumCities = player(iFlipNewPlayer).getNumCities()

		lHumanCityList = [city for city in self.getConvertedCities(iFlipNewPlayer, lPlots) if city.getOwner() == human()]
		
		if popupReturn.getButtonClicked() == 0:
			message(human(), 'TXT_KEY_FLIP_AGREED', color=iGreen)
						
			if lHumanCityList:
				for city in lHumanCityList:
					tCity = (city.getX(), city.getY())
					print ("flipping ", city.getName())
					cultureManager(tCity, 100, iFlipNewPlayer, iHuman, False, False, False)
					flipUnitsInCityBefore(tCity, iFlipNewPlayer, iHuman)
					flipCity(tCity, 0, 0, iFlipNewPlayer, [iHuman])
					flipUnitsInCityAfter(tCity, iFlipNewPlayer)
					
			if iNumCities == 0 and player(iFlipNewPlayer).getNumCities() > 0:
				self.createStartingWorkers(iFlipNewPlayer, player(iFlipNewPlayer).getCapitalCity())

			#same code as Betrayal - done just once to make sure human player doesn't hold a stack just outside of the cities
			for (x, y) in lPlots:
				betrayalPlot = plot(x,y)
				if betrayalPlot.isCore(betrayalPlot.getOwner()) and not betrayalPlot.isCore(iFlipNewPlayer): 
					continue
				
				for unit in units.at(x, y).owner(iHuman).domain(DOMAIN_LAND):
					if rand(100) >= iBetrayalThreshold:
						iUnitType = unit.getUnitType()
						unit.kill(False, iFlipNewPlayer)
						makeUnit(iFlipNewPlayer, iUnitType, (x, y))

			if data.lCheatersCheck[0] == 0:
				data.lCheatersCheck[0] = iCheatersPeriod
				data.lCheatersCheck[1] = data.iFlipNewPlayer
				
		elif popupReturn.getButtonClicked() == 1:
			message(iHuman, 'TXT_KEY_FLIP_REFUSED', color=iGreen)

			for city in lHumanCityList:
				pPlot = plot(city)
				oldCulture = pPlot.getCulture(iHuman)
				pPlot.setCulture(iFlipNewPlayer, oldCulture/2, True)
				pPlot.setCulture(iHuman, oldCulture/2, True)
				data.iSpawnWar += 1
				if data.iSpawnWar == 1:
					team(iFlipNewPlayer).declareWar(iHuman, False, -1) ##True??
					data.iBetrayalTurns = iBetrayalPeriod
					self.initBetrayal()
						
		data.lTempEvents.remove((iFlipNewPlayer, lPlots))
		
		game.autosave()
				
	def rebellionPopup(self, iRebelCiv):
		popup(7622, text("TXT_KEY_REBELLION_TITLE"), text("TXT_KEY_REBELLION_TEXT", adjective(iRebelCiv)), text("TXT_KEY_POPUP_YES"), text("TXT_KEY_POPUP_NO"))

	def eventApply7622(self, popupReturn):
		iRebelCiv = data.iRebelCiv
		if popupReturn.getButtonClicked() == 0: # 1st button
			team().makePeace(iRebelCiv)
		elif popupReturn.getButtonClicked() == 1: # 2nd button
			team().declareWar(iRebelCiv, False, -1)

	def eventApply7625(self, popupReturn):
		iPlayer, targetList = data.lTempEventList
		if popupReturn.getButtonClicked() == 0:
			for x, y in targetList:
				if city(x, y).getOwner() == human():
					colonialAcquisition(iPlayer, tPlot)
					player(human()).changeGold(200)
		elif popupReturn.getButtonClicked() == 1:
			for x, y in targetList:
				if city(x, y).getOwner() == human():
					colonialConquest(iPlayer, tPlot)
		
	def eventApply7629(self, netUserData, popupReturn):
		targetList = data.lByzantineBribes
		iButton = popupReturn.getButtonClicked()
		
		if iButton >= len(targetList): return
		
		iByzantiumPlayer = slot(iCivByzantium)
		unit, iCost = targetList[iButton]
		closest = closestCity(unit, iByzantiumPlayer)
		
		newUnit = makeUnit(iByzantiumPlayer, unit.getUnitType(), closest).first()
		player(iByzantiumPlayer).changeGold(-iCost)
		unit.kill(False, iByzantiumPlayer)
		
		if newUnit:
			interface.selectUnit(newUnit, True, True, False)

#######################################
### Main methods (Event-Triggered) ###
#####################################  

	def setup(self):

		self.determineEnabledPlayers()
		
		self.initScenario()
		
		# Leoreth: make sure to select the Egyptian settler
		if player(iCivEgypt).isHuman():
			for unit in units.at(Areas.getCapital(iCivEgypt)):
				if unit.getUnitType() == iSettler:
					interface.selectUnit(unit, True, False, False)
					break

	def initScenario(self):
		self.updateStartingPlots()
	
		self.adjustCityCulture()
		
		self.updateGreatWall()
			
		self.foundCapitals()
		self.flipStartingTerritory()
		
		self.adjustReligionFoundingDates()
		self.initStartingReligions()
		
		Civilizations.initScenarioTechs(scenario())
		periods.setup()
	
		if scenario() == i3000BC:
			self.create4000BCstartingUnits()
			
		if scenario() == i600AD:
			self.create600ADstartingUnits()
			self.adjust600ADWonders()
			self.adjust600ADGreatPeople()
			
		if scenario() == i1700AD:
			self.create1700ADstartingUnits()
			self.init1700ADDiplomacy()
			self.prepareColonists()
			self.adjust1700ADCulture()
			self.adjust1700ADWonders()
			self.adjust1700ADGreatPeople()
			
			player(iCivChina).updateTradeRoutes()
		
		for iPlayer in players.major().where(lambda p: dBirth[p] < scenarioStartYear()):
			data.players[iPlayer].bSpawned = True
		
		self.invalidateUHVs()
		
		game.setVoteSourceReligion(1, iCatholicism, False)
		
		self.updateExtraOptions()

	def updateExtraOptions(self):
		# Human player can switch infinite times
		data.bUnlimitedSwitching = infos.constant('UNLIMITED_SWITCHING') != 0
		# No congresses
		data.bNoCongresses = infos.constant('NO_CONGRESSES') != 0
		# No plagues
		data.bNoPlagues = infos.constant('NO_PLAGUES') != 0

	def updateStartingPlots(self):
		for iPlayer in players.major():
			x, y = Areas.getCapital(civ(iPlayer))
			player(iPlayer).setStartingPlot(plot(x, y), False)

	def adjustCityCulture(self):
		if turns(10) == 10: return
			
		for city in cities.all():
			city.setCulture(city.getOwner(), turns(city.getCulture(city.getOwner())), True)

	def updateGreatWall(self):
		if scenario() == i3000BC:
			return
	
		elif scenario() == i600AD:
			tTL = (98, 39)
			tBR = (107, 48)
			lExceptions = [(105, 48), (106, 48), (107, 48), (106, 47), (98, 46), (98, 47), (99, 47), (98, 48), (99, 48), (98, 39), (99, 39), (100, 39), (98, 40), (99, 40), (98, 41), (99, 41), (98, 42), (100, 40)]
			lAdditions = [(103, 38), (104, 37), (102, 49), (103, 49)]
				
		elif scenario() == i1700AD:
			tTL = (98, 40)
			tBR = (106, 50)
			lExceptions = [(98, 46), (98, 47), (98, 48), (98, 49), (99, 49), (98, 50), (99, 50), (100, 50), (99, 47), (99, 48), (100, 49), (101, 49), (101, 50), (102, 50)]
			lAdditions = [(104, 51), (105, 51), (106, 51), (107, 41), (107, 42), (107, 43), (103, 38), (103, 39), (104, 39), (105, 39), (104, 37)]
			
			lRemoveWall = [(97, 40), (98, 39), (99, 39), (100, 39), (101, 39), (102, 39)]
			
			for x, y in lRemoveWall:
				plot_(x, y).setOwner(-1)
				
			city(102, 47).updateGreatWall()
			
			for x, y in lRemoveWall:
				plot_(x, y).setOwner(slot(iCivChina))
		
		for plot in plots.start(tTL).end(tBR).without(lExceptions).including(lAdditions):
			if not plot.isWater(): plot.setWithinGreatWall(True)

	def adjust1700ADCulture(self):
		for plot in plots.all():
			if plot.getOwner() != -1:
				plot.changeCulture(plot.getOwner(), 100, True)
				convertPlotCulture(plot, plot.getOwner(), 100, True)
					
		for x, y in [(48, 45), (50, 44), (50, 43), (50, 42), (49, 40)]:
			convertPlotCulture(plot_(x, y), slot(iCivPortugal), 100, True)
			
		for x, y in [(58, 49), (59, 49), (60, 49)]:
			convertPlotCulture(plot_(x, y), slot(iCivGermany), 100, True)
			
		for x, y in [(62, 51)]:
			convertPlotCulture(plot_(x, y), slot(iCivHolyRome), 100, True)
			
		for x, y in [(58, 52), (58, 53)]:
			convertPlotCulture(plot_(x, y), slot(iCivNetherlands), 100, True)
			
		for x, y in [(64, 53), (66, 55)]:
			convertPlotCulture(plot_(x, y), slot(iCivPoland), 100, True)
			
		for x, y in [(67, 58), (68, 59), (69, 56), (69, 54)]:
			convertPlotCulture(plot_(x, y), slot(iCivRussia), 100, True)

	def prepareColonists(self):
		# TODO: unify all those lists for colonists, trading company conquerors, trading company corporation...
		dColonistsAlreadyGiven = {
			iCivVikings : 1,
			iCivSpain : 7,
			iCivFrance : 3,
			iCivEngland : 3,
			iCivPortugal : 6,
			iCivNetherlands : 4,
			iCivGermany : 0,
		}
		
		for iCiv, iColonists in dColonistsAlreadyGiven.items():
			iPlayer = slot(iCiv)
			if iPlayer >= 0:
				data.players[iPlayer].iExplorationTurn = year(1700)
				data.players[iPlayer].iColonistsAlreadyGiven = iColonists

	def init1700ADDiplomacy(self):
		team(iCivEngland).declareWar(slot(iCivMughals), False, WarPlanTypes.WARPLAN_LIMITED)
		team(iCivIndia).declareWar(slot(iCivMughals), False, WarPlanTypes.WARPLAN_TOTAL)

	def changeAttitudeExtra(self, iPlayer1, iPlayer2, iValue):
		player(iPlayer1).AI_changeAttitudeExtra(iPlayer2, iValue)
		player(iPlayer2).AI_changeAttitudeExtra(iPlayer1, iValue)

	def invalidateUHVs(self):
		for iPlayer in players.major():
			if not player(iPlayer).isPlayable():
				for i in range(3):
					data.players[iPlayer].lGoals[i] = 0

	def foundCapitals(self):
		if scenario() == i600AD:
		
			# China
			self.prepareChina()
			tCapital = Areas.getCapital(iCivChina)
			lBuildings = [iGranary, iConfucianTemple, iTaixue, iBarracks, iForge]
			foundCapital(slot(iCivChina), tCapital, "Xi'an", 4, 100, lBuildings, [iConfucianism, iTaoism])
			
		elif scenario() == i1700AD:
			
			# Chengdu
			city(99, 41).setCulture(slot(iCivChina), 100, True)

	def flipStartingTerritory(self):
	
		if scenario() == i600AD:
			
			# China
			tTL, tBR = Areas.dBirthArea[iCivChina]
			if not player(iCivChina).isHuman(): tTL = (99, 39) # 4 tiles further south
			self.startingFlip(slot(iCivChina), [(tTL, tBR)])
			
		if scenario() == i1700AD:
		
			# China (Tibet)
			tTibetTL = (94, 42)
			tTibetBR = (97, 45)
			tManchuriaTL = (105, 51)
			tManchuriaBR = (109, 55)
			self.startingFlip(slot(iCivChina), [(tTibetTL, tTibetBR), (tManchuriaTL, tManchuriaBR)])
			
			# Russia (Sankt Peterburg)
			convertPlotCulture(plot(68, 58), slot(iCivRussia), 100, True)
			convertPlotCulture(plot(67, 57), slot(iCivRussia), 100, True)

	def startingFlip(self, iPlayer, lRegionList):
	
		for tuple in lRegionList:
			tTL = tuple[0]
			tBR = tuple[1]
			tExceptions = []
			if len(tuple) > 2: tExceptions = tuple[2]
			self.convertSurroundingCities(iPlayer, plots.start(tTL).end(tBR).without(tExceptions))
			self.convertSurroundingPlotCulture(iPlayer, plots.start(tTL).end(tBR).without(tExceptions))

	def prepareChina(self):
		pGuiyang = plot_(102, 41)
		city(pGuiyang).kill()
		pGuiyang.setImprovementType(-1)
		pGuiyang.setRouteType(-1)
		pGuiyang.setFeatureType(iForest, 0)

		if scenario() == i600AD:
			pXian = plot_(100, 44)
			city(pXian).kill()
			pXian.setImprovementType(-1)
			pXian.setRouteType(-1)
			pXian.setFeatureType(iForest, 0)
			
		elif scenario() == i1700AD:
			pBeijing = plot_(tBeijing, tBeijing)
			city(pBeijing).kill()
			pBeijing.setImprovementType(-1)
			pBeijing.setRouteType(-1)

		tCultureRegionTL = (98, 37)
		tCultureRegionBR = (109, 49)
		for iMinor in players.independent():
			for plot in plots.start(tCultureRegionTL).end(tCultureRegionBR):
				bCity = False
				for loopPlot in plots.surrounding(plot):
					if loopPlot.isCity():
						bCity = True
						loopPlot.getPlotCity().setCulture(iMinor, 0, False)
				if bCity:
					plot.setCulture(iMinor, 1, True)
				else:
					plot.setCulture(iMinor, 0, True)
					plot.setOwner(-1)
					
		iMinor = players.independent().random()
		if iMinor:
			player(iMinor).found(99, 41)
			makeUnit(iMinor, iArcher, (99, 41))
		
			pChengdu = city(99, 41)
			pChengdu.setName("Chengdu", False)
			pChengdu.setPopulation(2)
			pChengdu.setHasReligion(iConfucianism, True, False, False)
			pChengdu.setHasRealBuilding(iGranary, True)
			pChengdu.setHasRealBuilding(iDujiangyan, True)
		
		if scenario() == i600AD:
			player(iCivBarbarian).found(105, 49)
			makeUnit(iBarbarian, iArcher, (105, 49))
			pShenyang = city(105, 49)
			pShenyang.setName("Simiyan hoton", False)
			pShenyang.setPopulation(2)
			pShenyang.setHasReligion(iConfucianism, True, False, False)
			pShenyang.setHasRealBuilding(iGranary, True)
			pShenyang.setHasRealBuilding(iWalls, True)
			pShenyang.setHasRealBuilding(iConfucianTemple, True)

	def adjust600ADWonders(self):
		lExpiredWonders = [iOracle, iIshtarGate, iTerracottaArmy, iHangingGardens, iGreatCothon, iApadanaPalace, iColossus, iStatueOfZeus, iGreatMausoleum, iTempleOfArtemis, iAquaAppia, iAlKhazneh, iJetavanaramaya]
		self.expireWonders(lExpiredWonders)
		
		pBeijing = city(102, 47)
		pBeijing.setBuildingOriginalOwner(iTaoistShrine, slot(iCivChina))
		pBeijing.setBuildingOriginalOwner(iGreatWall, slot(iCivChina))
		
		pNanjing = city(105, 43)
		pNanjing.setBuildingOriginalOwner(iConfucianShrine, slot(iCivChina))
		
		pPataliputra = city(94, 40)
		pPataliputra.setBuildingOriginalOwner(iHinduShrine, slot(iCivIndia))
		pPataliputra.setBuildingOriginalOwner(iBuddhistShrine, slot(iCivIndia))
		
		pSirajis = city(82, 38)
		pSirajis.setBuildingOriginalOwner(iZoroastrianShrine, slot(iCivPersia))
		
		pAlexandria = city(67, 36)
		pAlexandria.setBuildingOriginalOwner(iGreatLighthouse, slot(iCivEgypt))
		pAlexandria.setBuildingOriginalOwner(iGreatLibrary, slot(iCivEgypt))
		
		pMemphis = city(69, 35)
		pMemphis.setBuildingOriginalOwner(iPyramids, slot(iCivEgypt))
		pMemphis.setBuildingOriginalOwner(iGreatSphinx, slot(iCivEgypt))
		
		pAthens = city(67, 41)
		pAthens.setBuildingOriginalOwner(iParthenon, slot(iCivGreece))
		
		pRome = city(60, 44)
		pRome.setBuildingOriginalOwner(iFlavianAmphitheatre, slot(iCivRome))
		
		pChichenItza = city(23, 37)
		pChichenItza.setBuildingOriginalOwner(iTempleOfKukulkan, slot(iCivMaya))

	def adjust1700ADWonders(self):
		lExpiredWonders = [iOracle, iIshtarGate, iHangingGardens, iGreatCothon, iApadanaPalace, iColossus, iStatueOfZeus, iGreatMausoleum, iTempleOfArtemis, iAquaAppia, iAlKhazneh, iJetavanaramaya, iGreatLighthouse, iMoaiStatues, iFlavianAmphitheatre, iGreatLibrary, iGondeshapur, iSilverTreeFountain, iAlamut]
		self.expireWonders(lExpiredWonders)
	
		pMilan = city(59, 47)
		pMilan.setBuildingOriginalOwner(iSantaMariaDelFiore, slot(iCivItaly))
		pMilan.setBuildingOriginalOwner(iSanMarcoBasilica, slot(iCivItaly))
		
		pDjenne = city(51, 30)
		pDjenne.setBuildingOriginalOwner(iUniversityOfSankore, slot(iCivMali))
		
		pJerusalem = city(73, 38)
		pJerusalem.setBuildingOriginalOwner(iJewishShrine, slot(iCivIndependent))
		pJerusalem.setBuildingOriginalOwner(iOrthodoxShrine, slot(iCivByzantium))
		pJerusalem.setBuildingOriginalOwner(iDomeOfTheRock, slot(iCivArabia))
		
		pBaghdad = city(77, 40)
		pBaghdad.setBuildingOriginalOwner(iSpiralMinaret, slot(iCivArabia))
		
		pRome = city(60, 44)
		pRome.setBuildingOriginalOwner(iFlavianAmphitheatre, slot(iCivRome))
		pRome.setBuildingOriginalOwner(iSistineChapel, slot(iCivItaly))
		
		pSeville = city(51, 41)
		pSeville.setBuildingOriginalOwner(iMezquita, slot(iCivMoors))
		
		pBangkok = city(101, 33)
		pBangkok.setBuildingOriginalOwner(iWatPreahPisnulok, slot(iCivKhmer))
		
		pChichenItza = city(23, 37)
		pChichenItza.setBuildingOriginalOwner(iTempleOfKukulkan, slot(iCivMaya))
		
		pConstantinople = city(68, 45)
		pConstantinople.setBuildingOriginalOwner(iTheodosianWalls, slot(iCivByzantium))
		pConstantinople.setBuildingOriginalOwner(iHagiaSophia, slot(iCivByzantium))
		
		pJakarta = city(104, 25)
		pJakarta.setBuildingOriginalOwner(iBorobudur, slot(iCivIndonesia))
		
		pMexicoCity = city(18, 37)
		pMexicoCity.setBuildingOriginalOwner(iFloatingGardens, slot(iCivAztecs))
		
		pCairo = city(69, 35)
		pCairo.setBuildingOriginalOwner(iPyramids, slot(iCivEgypt))
		pCairo.setBuildingOriginalOwner(iGreatSphinx, slot(iCivEgypt))
		
		pAthens = city(67, 41)
		pAthens.setBuildingOriginalOwner(iParthenon, slot(iCivGreece))
		
		pShiraz = city(82, 38)
		pShiraz.setBuildingOriginalOwner(iZoroastrianShrine, slot(iCivPersia))
		
		pPataliputra = city(94, 40)
		pPataliputra.setBuildingOriginalOwner(iHinduShrine, slot(iCivIndia))
		pPataliputra.setBuildingOriginalOwner(iBuddhistShrine, slot(iCivIndia))
		
		pMecca = city(75, 33)
		pMecca.setBuildingOriginalOwner(iIslamicShrine, slot(iCivArabia))

	def expireWonders(self, lWonders):
		for iWonder in lWonders:
			game.incrementBuildingClassCreatedCount(infos.building(iWonder).getBuildingClassType())

	def adjust600ADGreatPeople(self):
		dGreatPeopleCreated = {
			iCivChina: 4,
			iCivKorea: 1,
			iCivByzantium: 1,
			iCivJapan: 0,
			iCivVikings: 0,
			iCivTurks: 0,
		}
		
		dGreatGeneralsCreated = {
			iCivChina: 1,
			iCivKorea: 0,
			iCivByzantium: 0,
			iCivJapan: 0,
			iCivVikings: 0,
			iCivTurks: 0,
		}
		
		for iCiv, iGreatPeople in dGreatPeopleCreated.iteritems():
			player(iCiv).changeGreatPeopleCreated(iGreatPeople)
			
		for iCiv, iGreatGenerals in dGreatGeneralsCreated.iteritems():
			player(iCiv).changeGreatGeneralsCreated(iGreatGenerals)

	def adjust1700ADGreatPeople(self):
		dGreatPeopleCreated = {
			iCivChina: 12,
			iCivIndia: 8,
			iCivPersia: 4,
			iCivTamils: 5,
			iCivKorea: 6,
			iCivJapan: 6,
			iCivVikings: 8,
			iCivTurks: 4,
			iCivSpain: 8,
			iCivFrance: 8,
			iCivEngland: 8,
			iCivHolyRome: 8,
			iCivPoland: 8,
			iCivPortugal: 8,
			iCivMughals: 8,
			iCivOttomans: 8,
			iCivThailand: 8,
			iCivCongo: 4,
			iCivNetherlands: 6,
		}
		
		dGreatGeneralsCreated = {
			iCivChina: 4,
			iCivIndia: 3,
			iCivPersia: 2,
			iCivTamils: 2,
			iCivKorea: 3,
			iCivJapan: 3,
			iCivVikings: 3,
			iCivTurks: 3,
			iCivSpain: 4,
			iCivFrance: 3,
			iCivEngland: 3,
			iCivHolyRome: 4,
			iCivPoland: 3,
			iCivPortugal: 3,
			iCivMughals: 4,
			iCivOttomans: 5,
			iCivThailand: 3,
			iCivCongo: 2,
			iCivNetherlands: 3,
		}
		
		for iCiv, iGreatPeople in dGreatPeopleCreated.iteritems():
			player(iCiv).changeGreatPeopleCreated(iGreatPeople)
			
		for iCiv, iGreatGenerals in dGreatGeneralsCreated.iteritems():
			player(iCiv).changeGreatGeneralsCreated(iGreatGenerals)

	def placeGoodyHuts(self):
			
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

	def adjustReligionFoundingDates(self):
		lReligionFoundingYears = [-2000, 40, 500, 1521, 622, -1500, 80, -500, -400, -600]
	
		for iReligion in range(iNumReligions):
			if game.isReligionFounded(iReligion):
				game.setReligionGameTurnFounded(iReligion, year(lReligionFoundingYears[iReligion]))

	def initStartingReligions(self):
	
		if scenario() == i600AD:
			setStateReligionBeforeBirth(lCatholicStart, iCatholicism)
			setStateReligionBeforeBirth(lProtestantStart, iCatholicism)
			
		elif scenario() == i1700AD:
			setStateReligionBeforeBirth(lCatholicStart, iCatholicism)
			setStateReligionBeforeBirth(lProtestantStart, iProtestantism)

	def checkTurn(self, iGameTurn):
	
		# Leoreth: randomly place goody huts
		if iGameTurn == scenarioStartTurn()+3:
			self.placeGoodyHuts()
		
		if iGameTurn == year(dBirth[iCivSpain])-1:
			if scenario() == i600AD:
				pMassilia = city_(56, 46)
				if pMassilia:
					pMassilia.setCulture(pMassilia.getOwner(), 1, True)

		# Leoreth: Turkey immediately flips independent cities in its core to avoid being pushed out of Anatolia
		if iGameTurn == data.iOttomanSpawnTurn + 1:
			cityPlotList = cities.of(Areas.getBirthArea(iCivOttomans))
			for city in cityPlotList:
				tPlot = (city.getX(), city.getY())
				iOwner = city.getOwner()
				if is_minor(iOwner):
					flipCity(tPlot, False, True, slot(iCivOttomans), ())
					cultureManager(tPlot, 100, slot(iCivOttomans), iOwner, True, False, False)
					self.convertSurroundingPlotCulture(slot(iCivOttomans), plots.surrounding(tPlot))
					makeUnit(iCivOttomans, iCrossbowman, tPlot)
					
		#Trigger betrayal mode
		if data.iBetrayalTurns > 0:
			self.initBetrayal()

		if data.lCheatersCheck[0] > 0:
			if (team().isAtWar(data.lCheatersCheck[1])):
				print ("No cheaters!")
				self.initMinorBetrayal(data.lCheatersCheck[1])
				data.lCheatersCheck[0] = 0
				data.lCheatersCheck[1] = -1
			else:
				data.lCheatersCheck[0] -= 1

		iMinor = players.independent().alive().periodic(20)
		if iMinor:
			updateMinorTechs(iMinor, iBarbarian)

		#Leoreth: give Phoenicia a settler in Qart-Hadasht in 820BC
		if not player(iCivPhoenicia).isHuman() and year() == year(-820) - (data.iSeed % 10):
			makeUnit(iCivPhoenicia, iSettler, (58, 39))
			makeUnits(iCivPhoenicia, iArcher, (58, 39), 2)
			makeUnits(iCivPhoenicia, iWorker, (58, 39), 2)
			makeUnits(iCivPhoenicia, iWarElephant, (58, 39), 2)
			
		if year() == year(476):
			if player(iCivItaly).isHuman() and player(iCivRome).isAlive():
				sta.completeCollapse(slot(iCivRome))
				
		if year() == year(-50):
			if player(iCivByzantium).isHuman() and player(iCivGreece).isAlive():
				sta.completeCollapse(slot(iCivGreece))
				
		if year() == year(dBirth[iCivIndia])-turns(1):
			if player(iCivHarappa).isAlive() and not player(iCivHarappa).isHuman():
				sta.completeCollapse(slot(iCivHarappa))
			
		#Colonists
		if year() == year(-850):
			self.giveEarlyColonists(iCivGreece)
		elif year() == year(-700): # removed their colonists because of the Qart-Hadasht spawn
			self.giveEarlyColonists(iCivCarthage)
			
		elif year() == year(-600):
			self.giveEarlyColonists(iCivRome)
		elif year() == year(-400):
			self.giveEarlyColonists(iCivRome)

		if year().between(860, 1250):
			if turn() % turns(10) == 9:
				self.giveRaiders(iCivVikings, Areas.getBroaderArea(iCivVikings))
		
		if year().between(1350, 1918):
			for iCiv in [iCivSpain, iCivEngland, iCivFrance, iCivPortugal, iCivNetherlands, iCivVikings, iCivGermany]:
				if player(iCiv).isAlive():
					iPlayer = slot(iCiv)
					if turn() == data.players[iPlayer].iExplorationTurn + 1 + data.players[iPlayer].iColonistsAlreadyGiven * 8:
						self.giveColonists(iPlayer)
					
		if year() == year(710)-1:
			marrakesh = city_(51, 37)
			if marrakesh:
				marrakesh.setHasReligion(iIslam, True, False, False)
				
				makeUnit(marrakesh.getOwner(), iSettler, marrakesh)
				makeUnit(marrakesh.getOwner(), iWorker, marrakesh)
				
		# Leoreth: help human with Aztec UHV - prevent super London getting in the way
		if year() == year(1500) and player(iCivAztecs).isHuman():
			plot = plot_(Areas.getCapital(iCivEngland))
			if plot.isCity():
				city = plot.getPlotCity()
				if city.getPopulation() > 14:
					city.changePopulation(-3)
				
		# Leoreth: make sure Aztecs are dead in 1700 if a civ that spawns from that point is selected
		if year() == year(1700)-2:
			if year(dBirth[human()]) >= year(1700) and player(iCivAztecs).isAlive():
				sta.completeCollapse(slot(iCivAztecs))

		for iLoopPlayer in players.major().where(lambda p: dBirth[p] > scenarioStartYear()):
			if year() >= year(dBirth[iLoopPlayer]) - 2 and year() <= year(dBirth[iLoopPlayer]) + 6:
				self.initBirth(dBirth[iLoopPlayer], iLoopPlayer)

		if year() == year(600):
			if scenario() == i600AD:  #late start condition
				tTL, tBR = Areas.dBirthArea[iCivChina]
				if not player(iCivChina).isHuman(): tTL = (99, 39) # 4 tiles further north
				china = plots.start(tTL).end(tBR)
				iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(slot(iCivChina), china)
				self.convertSurroundingPlotCulture(slot(iCivChina), china)
				
				for iMinor in players.independent().barbarian():
					flipUnitsInArea(china, slot(iCivChina), iMinor, False, player(iMinor).isBarbarian())

		#kill the remaining barbs in the region: it's necessary to do this more than once to protect those civs
		for iCiv in [iCivVikings, iCivSpain, iCivFrance, iCivHolyRome, iCivRussia, iCivAztecs]:
			if year() >= dBirth[iCiv]+2 and year() <= dBirth[iCiv]+turns(10):
				killUnitsInArea(iBarbarian, Areas.getBirthArea(iCiv))
				
		#fragment utility
		if year() >= year(50) and turn() % turns(15) == 6:
			self.fragmentIndependents()

		if turn() % turns(10) == 5:
			sta.checkResurrection()
			
		# Leoreth: check for scripted rebirths
		for iCiv, iYear in dRebirth.items():
			iPlayer = slot(iCiv)
		
			if year() == year(iYear) and not player(iCiv).isAlive():
				self.rebirthFirstTurn(iPlayer)

			if year() == year(iYear)+1 and player(iCiv).isAlive() and player(iCiv).isReborn():
				self.rebirthSecondTurn(iPlayer)

	def endTurn(self, iPlayer):
		for iConqueror, tPlot in data.lTimedConquests:
			colonialConquest(iConqueror, tPlot)
			
		if player(iPlayer).isHuman():
			self.checkFlipPopup()
			
		data.lTimedConquests = []

	def rebirthFirstTurn(self, iPlayer):
		pPlayer = player(iPlayer)
		pTeam = team(iPlayer)
		iCiv = civ(iPlayer)
		
		# disable Mexico and Colombia
		if iCiv == iCivAztecs and infos.constant('PLAYER_REBIRTH_MEXICO') == 0: return
		if iCiv == iCivMaya and infos.constant('PLAYER_REBIRTH_COLOMBIA') == 0: return
		
		if iCiv in dRebirthCiv:
			iCiv = dRebirthCiv[iCiv]
			setCivilization(iPlayer, iCiv)
			
		if iCiv == -1:
			raise Exception("iCiv = -1 for iPlayer = %d" % iPlayer)
			
		Modifiers.updateModifiers(iPlayer)
		x, y = Areas.dCapitals[iCiv]
		plot = plot_(x, y)
		city = city_(x, y)
		
		# reset contacts and make peace
		for iOtherCiv in players.major().without(iPlayer):
			pTeam.makePeace(iOtherCiv)
			pTeam.cutContact(iOtherCiv)
		
		# reset diplomacy
		pPlayer.AI_reset()
		
		# reset player espionage weights
		player().setEspionageSpendingWeightAgainstTeam(pPlayer.getTeam(), 0)
		
		# reset great people
		pPlayer.resetGreatPeopleCreated()
		
		# reset map visibility
		for plot in plots.all():
			plot.setRevealed(iPlayer, False, True, -1)
		
		# assign new leader
		if iCiv in dRebirthLeaders:
			if pPlayer.getLeader() != dRebirthLeaders[iCiv]:
				pPlayer.setLeader(dRebirthLeaders[iCiv])

		message(human(), 'TXT_KEY_INDEPENDENCE_TEXT', adjective(iPlayer), color=iGreen)
		setReborn(iPlayer, True)
		
		# Determine whether capital location is free
		bFree = isFree(iPlayer, (x, y), True) and not plot.isUnit()

		# if city present, flip it. If plot is free, found it. Else give settler.
		if city:
			city = completeCityFlip((x, y), iPlayer, city.getOwner(), 100)
		else:
			convertPlotCulture(plot, iPlayer, 100, True)
			if bFree:
				pPlayer.found(x, y)
			else:
				makeUnit(iPlayer, iSettler, (x, y))
				
		# make sure there is a palace in the city
		if city and not city.hasBuilding(iPalace):
			city.setHasRealBuilding(iPalace, True)
		
		self.createRespawnUnits(iPlayer, (x, y))
		
		# for colonial civs, set dynamic state religion
		if iCiv in [iCivMexico, iCivColombia]:
			self.setStateReligion(iPlayer)

		self.assignTechs(iPlayer)
		if year() >= year(dBirth[human()]):
			startNewCivSwitchEvent(iPlayer)

		player(iPlayer).setLatestRebellionTurn(year(dSpawn[iCiv]))

		# adjust gold, civics, religion and other special settings
		if iCiv == iCivIran:
			pPlayer.setGold(600)
			pPlayer.setLastStateReligion(iIslam)
			pPlayer.setCivics(iCivicsGovernment, iMonarchy)
			pPlayer.setCivics(iCivicsLegitimacy, iVassalage)
			pPlayer.setCivics(iCivicsSociety, iSlavery)
			pPlayer.setCivics(iCivicsEconomy, iMerchantTrade)
			pPlayer.setCivics(iCivicsReligion, iTheocracy)
			
		elif iCiv == iCivMexico:
			city = city_(18, 37)
			if city:
				if game.getBuildingClassCreatedCount(infos.building(iFloatingGardens).getBuildingClassType()) == 0:
					city.setHasRealBuilding(iFloatingGardens, True)
					
				iStateReligion = pPlayer.getStateReligion()
				if iStateReligion >= 0 and city.isHasReligion(iStateReligion):
					city.setHasRealBuilding(iMonastery + 4 * iStateReligion, True)
			
			cnm.updateCityNamesFound(iPlayer) # use name of the plots in their city name map
			
			pPlayer.setGold(500)
			
			pPlayer.setCivics(iCivicsGovernment, iDespotism)
			pPlayer.setCivics(iCivicsLegitimacy, iConstitution)
			pPlayer.setCivics(iCivicsSociety, iIndividualism)
			pPlayer.setCivics(iCivicsEconomy, iRegulatedTrade)
			pPlayer.setCivics(iCivicsReligion, iClergy)
			pPlayer.setCivics(iCivicsTerritory, iNationhood)
			
		elif iCiv == iCivColombia:
			pPlayer.setGold(750)
			pPlayer.setCivics(iCivicsGovernment, iDespotism)
			pPlayer.setCivics(iCivicsLegitimacy, iConstitution)
			pPlayer.setCivics(iCivicsSociety, iIndividualism)
			pPlayer.setCivics(iCivicsEconomy, iRegulatedTrade)
			pPlayer.setCivics(iCivicsReligion, iClergy)
			pPlayer.setCivics(iCivicsTerritory, iNationhood)
			plot_(28, 31).setFeatureType(-1, 0)
		
		dc.onCivRespawn(iPlayer, [])

	def rebirthSecondTurn(self, iPlayer):
		iCiv = civ(iPlayer)
	
		lRebirthPlots = Areas.getBirthArea(iCiv)
		
		# exclude American territory for Mexico
		if iCiv == iCivMexico:
			removedPlots = plots.of(lRebirthPlots).owner(slot(iCivAmerica)).where(lambda p: location(p) not in Areas.getCoreArea(iCiv))
			for plot in removedPlots:
				lRebirthPlots.remove(location(plot))
		
		lCities = [city_(x, y) for x, y in lRebirthPlots if city_(x, y)]
			
		# remove garrisons
		for city in lCities:
			if city.getOwner() != human():
				relocateGarrisons(location(city), city.getOwner())
				relocateSeaGarrisons(location(city), city.getOwner())
				
		# convert cities
		iConvertedCities, iHumanCities = self.convertSurroundingCities(iPlayer, lRebirthPlots)
		
		# create garrisons
		for city in lCities:
			if city.getOwner() == human():
				createGarrisons(location(city), iPlayer, 1)
				
		# convert plot culture
		self.convertSurroundingPlotCulture(iPlayer, plots.of(lRebirthPlots))
		
		# reset plague
		data.players[iPlayer].iPlagueCountdown = -10
		clearPlague(iPlayer)
		
		# adjust starting stability
		data.players[iPlayer].resetStability()
		data.players[iPlayer].iStabilityLevel = iStabilityStable
		if player(iPlayer).isHuman(): data.resetHumanStability()
		
		# ask human player for flips
		if iHumanCities > 0 and not player(iPlayer).isHuman():
			self.scheduleFlipPopup(iPlayer, lRebirthPlots)

	def checkPlayerTurn(self, iGameTurn, iPlayer):
		return

	def fragmentIndependents(self):
		iLargestMinor = players.independent().maximum(lambda p: player(p).getNumCities())
		iSmallestMinor = players.independent().minimum(lambda p: player(p).getNumCities())
		if player(iLargestMinor).getNumCities() > 2 * player(iSmallestMinor).getNumCities():
			for city in cities.owner(iLargestMinor).sample(3):
				completeCityFlip(city, iLargestMinor, iSmallestMinor, 50, False, True, True, True)

	def fragmentBarbarians(self, iGameTurn):
		for iDeadPlayer in players.major().shuffle():
			if not player(iDeadPlayer).isAlive() and iGameTurn > year(dBirth[iDeadPlayer]) + turns(50):
				barbarianCities = cities.of(Areas.getNormalArea(civ(iDeadPlayer))).owner(iCivBarbarian)
				
				if barbarianCities > 3:
					for iMinor, minorCities in barbarianCities.fraction(2).divide(players.independent()):
						for city in minorCities:
							completeCityFlip(city, iMinor, iBarbarian, 50, False, True, True, True)
					
					return

	def secession(self, iGameTurn):
		for iPlayer in players.major().shuffle():
			if player(iPlayer).isAlive() and iGameTurn >= year(dBirth[iPlayer]) + turns(30):
				
				if stability(iPlayer) == iStabilityCollapsing:

					cityList = []
					for city in cities.owner(iPlayer):
						pPlot = plot(city)

						if not city.isWeLoveTheKingDay() and not city.isCapital() and location(city) != Areas.getCapital(civ(iPlayer)):
							if player(iPlayer).getNumCities() > 0: #this check is needed, otherwise game crashes
								capital = player(iPlayer).getCapitalCity()
								iDistance = distance(city, capital)
								if iDistance > 3:
							
									if city.angryPopulation(0) > 0 or \
										city.healthRate(False, 0) < 0 or \
										city.getReligionBadHappiness() > 0 or \
										city.getLargestCityHappiness() < 0 or \
										city.getHurryAngerModifier() > 0 or \
										city.getNoMilitaryPercentAnger() > 0 or \
										city.getWarWearinessPercentAnger() > 0:
										cityList.append(city)
										continue
									
									for iLoop in players.all().barbarian():
										if iLoop != iPlayer:
											if pPlot.getCulture(iLoop) > 0:
												cityList.append(city)
												break

					if cityList:
						iNewCiv = iCivIndependent
						if rand(2) == 1:
							iNewCiv = iCivIndependent2
						
						if civ(iPlayer) in [iCivAztecs, iCivInca, iCivMaya, iCivEthiopia, iCivMali, iCivCongo]:
							if data.iPlayersWithNationalism == 0:
								iNewCiv = iCivNative
						
						iNewPlayer = slot(iNewCiv)
						
						splittingCity = random_entry(cityList)
						tPlot = location(splittingCity)
						cultureManager(tPlot, 50, iNewPlayer, iPlayer, False, True, True)
						flipUnitsInCityBefore(tPlot, iNewPlayer, iPlayer)
						flipCity(tPlot, False, False, iNewPlayer, [iPlayer])   #by trade because by conquest may raze the city
						flipUnitsInCityAfter(tPlot, iNewPlayer)
						
						message(iPlayer, '%s %s' % (splittingCity.getName(), text('TXT_KEY_STABILITY_SECESSION')), color=iOrange)
						
					return

	def initBirth(self, iBirthYear, iPlayer): # iBirthYear is really year now, so no conversion prior to function call - edead
		iBirthYear = year(iBirthYear) # converted to turns here - edead
		iCiv = civ(iPlayer)
		
		if iCiv in lSecondaryCivs:
			if not player(iPlayer).isHuman() and not data.isCivEnabled(iCiv):
				return
		
		lConditionalCivs = [iCivByzantium, iCivMughals, iCivOttomans, iCivThailand, iCivBrazil, iCivArgentina, iCivCanada, iCivItaly]
		
		# Leoreth: extra checks for conditional civs
		if iCiv in lConditionalCivs and not player(iPlayer).isHuman():
			if iCiv == iCivByzantium:
				if not player(iCivRome).isAlive() or player(iCivGreece).isAlive() or (player(iCivRome).isHuman() and stability(slot(iCivRome)) == iStabilitySolid):
					return
					
			elif iCiv == iCivOttomans:
				tMiddleEastTL = (69, 38)
				tMiddleEastBR = (78, 45)
				if cities.start(tMiddleEastTL).end(tMiddleEastBR).any(lambda city: slot(iCivTurks) in [city.getOwner(), city.getPreviousOwner()]):
					return

			elif iCiv == iCivThailand:
				if not player(iCivKhmer).isHuman():
					if stability(slot(iCivKhmer)) > iStabilityShaky:
						return
				else:
					if stability(slot(iCivKhmer)) > iStabilityUnstable:
						return
						
			elif iCiv in [iCivArgentina, iCivBrazil]:
				iColonyPlayer = getColonyPlayer(iPlayer)
				if iColonyPlayer < 0: return
				elif civ(iColonyPlayer) not in [iCivArgentina, iCivBrazil]:
					if stability(iColonyPlayer) > iStabilityStable:
						return
						
			elif iCiv == iCivItaly:
				if player(iCivRome).isAlive():
					return
					
				if not getCitiesInCore(slot(iCivRome), False).where(lambda city: city.getOwner() not in players.major()):
					return
		
		periods.onBirth(iPlayer)
				
		tCapital = Areas.getCapital(iCiv)
				
		x, y = tCapital
		bCapitalSettled = False
		
		if iCiv == iCivItaly:
			for plot in plots.surrounding(tCapital):
				if plot.isCity():
					bCapitalSettled = True
					tCapital = location(plot)
					x, y = tCapital
					break
					
		print "initBirth turn check"

		if turn() == iBirthYear-1 + data.players[iPlayer].iSpawnDelay + data.players[iPlayer].iFlipsDelay:
			print "turn check passed"
			if iCiv in lConditionalCivs or bCapitalSettled:
				convertPlotCulture(plot_(x, y), iPlayer, 100, True)

			tTopLeft, tBottomRight = Areas.getBirthRectangle(iCiv)
			tBroaderTopLeft, tBroaderBottomRight = Areas.dBroaderArea[iCiv]
			
			if iCiv == iCivThailand:
				angkor = city(Areas.dCapitals[iCivKhmer])
				if angkor:
					bWonder = any(angkor.isHasRealBuilding(iBuilding) for iBuilding in range(iBeginWonders, iNumBuildings))
					if bWonder and not player(iPlayer).isHuman():
						angkor.setName("Ayutthaya", False)
						tCapital = (x-1, y+1)
						x, y = tCapital
						plot_(x, y).setFeatureType(-1, 0)
				
				# Prey Nokor becomes Saigon
				saigon = city(104, 33)
				if saigon:
					saigon.setName("Saigon", False)
				
			iPreviousOwner = plot_(x, y).getOwner()

			if data.players[iPlayer].iFlipsDelay == 0: #city hasn't already been founded)
			
				#this may fix the -1 bug
				if player(iPlayer).isHuman():
					for unit in units.at(x, y).notowner(iPlayer):
						unit.kill(False, -1)
				
				bBirthInCapital = False
				
				if (iCiv in lConditionalCivs and iCiv != iCivThailand) or bCapitalSettled:
					bBirthInCapital = True
				
				if iCiv == iCivOttomans:
					self.moveOutInvaders(tTopLeft, tBottomRight)  
					
				if bBirthInCapital:
					makeUnit(iPlayer, iCatapult, (0, 0))
			
				bDeleteEverything = False
				pCapital = plot_(x, y)
				if pCapital.isOwned():
					if player(iPlayer).isHuman() or not player(human()).isAlive():
						if not (pCapital.isCity() and pCapital.getPlotCity().isHolyCity()):
							bDeleteEverything = True
							print ("bDeleteEverything 1")
					else:
						bDeleteEverything = True
						for pPlot in plots.surrounding(tCapital):
							if (pPlot.isCity() and (pPlot.getPlotCity().getOwner() == human() or pPlot.getPlotCity().isHolyCity())) or iCiv == iCivOttomans:
								bDeleteEverything = False
								print ("bDeleteEverything 2")
								break
				print ("bDeleteEverything", bDeleteEverything)
				if not plot_(x, y).isOwned():
					if iCiv in [iCivNetherlands, iCivPortugal, iCivByzantium, iCivKorea, iCivThailand, iCivItaly, iCivCarthage]: #dangerous starts
						data.lDeleteMode[0] = iPlayer
					if bBirthInCapital:
						self.birthInCapital(iPlayer, iPreviousOwner, tCapital, tTopLeft, tBottomRight)
					else:
						self.birthInFreeRegion(iPlayer, tCapital, tTopLeft, tBottomRight)
				elif bDeleteEverything and not bBirthInCapital:
					for pCurrent in plots.surrounding(tCapital):
						data.lDeleteMode[0] = iPlayer
						for iLoopPlayer in players.all().without(iPlayer):
							flipUnitsInArea(plots.start(tTopLeft).end(tBottomRight).without(Areas.dBirthAreaExceptions[iCiv]), iPlayer, iLoopPlayer, True, False)
						if pCurrent.isCity():
							pCurrent.eraseAIDevelopment()
						for iLoopPlayer in players.all().without(iPlayer):
							pCurrent.setCulture(iLoopPlayer, 0, True)
						pCurrent.setOwner(-1)
					if bBirthInCapital:
						self.birthInCapital(iPlayer, iPreviousOwner, tCapital, tTopLeft, tBottomRight)
					else:
						self.birthInFreeRegion(iPlayer, tCapital, tTopLeft, tBottomRight)
				else:
					if bBirthInCapital:
						self.birthInCapital(iPlayer, iPreviousOwner, tCapital, tTopLeft, tBottomRight)
					else:
						self.birthInForeignBorders(iPlayer, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight)
						
				if bBirthInCapital:	
					clearCatapult(iPlayer)
						
			else:
				print ( "setBirthType again: flips" )
				self.birthInFreeRegion(iPlayer, tCapital, tTopLeft, tBottomRight)
				
		# Leoreth: reveal all normal plots on spawn
		for x, y in Areas.getNormalArea(iCiv):
			plot_(x, y).setRevealed(iPlayer, True, True, 0)
				
		# Leoreth: conditional state religion for colonial civs and Byzantium
		if iCiv in [iCivByzantium, iCivArgentina, iCivBrazil]:
			self.setStateReligion(iPlayer)
			
		if canSwitch(iPlayer, iBirthYear):
			startNewCivSwitchEvent(iPlayer)
			
		data.players[iPlayer].bSpawned = True

	def moveOutInvaders(self, tTL, tBR):
		if player(iCivMongols).isAlive():
			mongolCapital = player(iCivMongols).getCapitalCity()
		for plot in plots.start(tTL).end(tBR):
			for unit in units.at(plot):
				if not isDefenderUnit(unit):
					if civ(unit) == iCivMongols:
						if not player(iCivMongols).isHuman():
							move(unit, mongolCapital)
					else:
						if unit.getUnitType() == iKeshik:
							unit.kill(False, iBarbarian)

	def deleteMode(self, iCurrentPlayer):
		iPlayer = data.lDeleteMode[0]
		iCiv = civ(iPlayer)
		
		print ("deleteMode after", iCurrentPlayer)
		tCapital = Areas.getCapital(iCiv)
		x, y = tCapital
			
		
		if iCurrentPlayer == iPlayer:
			if iCiv == iCivPhoenicia:
				for plot in plots.rectangle((x-2, y-1), (x+1, y+1)):
					plot.setCulture(iPlayer, 300, True)
			else:
				for plot in plots.surrounding(tCapital, radius=2):
					plot.setCulture(iPlayer, 300, True)
			for plot in plots.surrounding(tCapital):
				convertPlotCulture(plot, iPlayer, 100, True)
				if plot.getCulture(iPlayer) < 3000:
					plot.setCulture(iPlayer, 3000, True) #2000 in vanilla/warlords, cos here Portugal is choked by spanish culture
				plot.setOwner(iPlayer)
			data.lDeleteMode[0] = -1
			return
		
		if iCurrentPlayer != iPlayer-1 and iCiv not in [iCivCarthage, iCivGreece]:
			return
		
		bNotOwned = True
		for plot in plots.surrounding(tCapital):
			if plot.isOwned():
				bNotOwned = False
				for iLoopPlayer in players.all().without(iPlayer):
					plot.setCulture(iLoopPlayer, 0, True)
				plot.setOwner(iPlayer)
		
		for plot in plots.surrounding(tCapital, radius=15).without(tCapital).land(): # must include the distance from Sogut to the Caspius
			for unit in units.at(plot).owner(iPlayer):
				move(unit, tCapital)
		
	def birthInFreeRegion(self, iPlayer, tCapital, tTopLeft, tBottomRight):
		startingPlot = plot(tCapital)
		iCiv = civ(iPlayer)
		
		if data.players[iPlayer].iFlipsDelay == 0:
			iFlipsDelay = data.players[iPlayer].iFlipsDelay + 2
			if iFlipsDelay > 0:
				self.createStartingUnits(iPlayer, tCapital)
				
				if iCiv == iCivOttomans:
					data.iOttomanSpawnTurn = turn()
			
				if iCiv == iCivItaly:
					removeCoreUnits(iPlayer)
					cityList = getCitiesInCore(iPlayer, False)
					
					rome = city(Areas.getCapital(iCivRome))
					if rome:
						cityList.append(rome)
					
					for city in cityList:
						if city.getPopulation() < 5: city.setPopulation(5)
						city.setHasRealBuilding(iGranary, True)
						city.setHasRealBuilding(iLibrary, True)
						city.setHasRealBuilding(iCourthouse, True)
						if city.isCoastal(20): city.setHasRealBuilding(iHarbor, True)
				
				lPlots = plots.surrounding(tCapital, radius=3)
				for iMinor in players.independent().barbarian():
					flipUnitsInArea(lPlots, iPlayer, iMinor, True, player(iMinor).isBarbarian())
				
				self.assignTechs(iPlayer)
				data.players[iPlayer].iPlagueCountdown = -iImmunity
				clearPlague(iPlayer)
				data.players[iPlayer].iFlipsDelay = iFlipsDelay #save
				

		else: #starting units have already been placed, now the second part
		
			iNumCities = player(iPlayer).getNumCities()
		
			area = plots.start(tTopLeft).end(tBottomRight).without(Areas.getBirthExceptions(iCiv))
			iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iPlayer, area)
			self.convertSurroundingPlotCulture(iPlayer, area)
			for iMinor in players.independent().barbarian():
				flipUnitsInArea(area, iPlayer, iMinor, False, player(iMinor).isBarbarian())
		
			# create starting workers
			if iNumCities == 0 and player(iPlayer).getNumCities() > 0:
				self.createStartingWorkers(iPlayer, player(iPlayer).getCapitalCity())
			
			if iCiv == iCivArabia:
				self.arabianSpawn()
				
			if iCiv == iCivGermany:
				self.germanSpawn()
   
			#cover plots revealed by the lion
			clearCatapult(iPlayer)

			if iNumHumanCitiesToConvert > 0 and not player(iPlayer).isHuman(): # Leoreth: quick fix for the "flip your own cities" popup, still need to find out where it comes from
				self.scheduleFlipPopup(iPlayer, lPlots)

	def birthInForeignBorders(self, iPlayer, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight):
		iCiv = civ(iPlayer)
	
		if iCiv == iCivItaly:
			removeCoreUnits(iPlayer)
			cityList = self.getCitiesInCore(iPlayer, False)
			
			rome = city(Areas.getCapital(iCivRome))
			if rome:
				cityList.append(rome)
				
			for pCity in cityList:
				if city.getPopulation() < 5: city.setPopulation(5)
				city.setHasRealBuilding(iGranary, True)
				city.setHasRealBuilding(iLibrary, True)
				city.setHasRealBuilding(iCourthouse, True)
				if city.isCoastal(20): city.setHasRealBuilding(iHarbor, True)
				
		iNumCities = player(iPlayer).getNumCities()
		
		area = plots.start(tTopLeft).end(tBottomRight).without(Areas.getBirthExceptions(iCiv))
		iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iPlayer, area)
		self.convertSurroundingPlotCulture(iPlayer, area)
		
		# create starting workers
		if iNumCities == 0 and player(iPlayer).getNumCities() > 0:
			self.createStartingWorkers(iPlayer, location(player(iPlayer).getCapitalCity()))

		#now starting units must be placed
		if iNumAICitiesConverted > 0:
			plotList = squareSearch(tTopLeft, tBottomRight, ownedCityPlots, iPlayer)
			if plotList:
				tPlot = random_entry(plotList)
				if tPlot:
					self.createStartingUnits(iPlayer, tPlot)
					self.assignTechs(iPlayer)
					data.players[iPlayer].iPlagueCountdown = -iImmunity
					clearPlague(iPlayer)
			
			for iMinor in players.independent().barbarian():
				flipUnitsInArea(lPlots, iPlayer, iMinor, False, player(iMinor).isBarbarian())
			
			if iCiv == iCivOttomans:
				data.iOttomanSpawnTurn = turn()

		else:   #search another place
			plotList = squareSearch(tTopLeft, tBottomRight, goodPlots, [])
			if plotList:
				tPlot = random_entry(plotList)
				if tPlot:
					self.createStartingUnits(iPlayer, tPlot)
					self.assignTechs(iPlayer)
					data.players[iPlayer].iPlagueCountdown = -iImmunity
					clearPlague(iPlayer)
			else:
				plotList = squareSearch(tBroaderTopLeft, tBroaderBottomRight, goodPlots, [])
			if plotList:
				tPlot = random_entry(plotList)
				if tPlot:
					self.createStartingUnits(iPlayer, tPlot)
					self.assignTechs(iPlayer)
					data.players[iPlayer].iPlagueCountdown = -iImmunity
					clearPlague(iPlayer)
			
			for iMinor in players.independent().barbarian():
				flipUnitsInArea(lPlots, iPlayer, iMinor, True, player(iPlayer).isBarbarian())

		if iNumHumanCitiesToConvert > 0:
			print "Flip Popup: foreign borders"
			self.scheduleFlipPopup(iPlayer, lPlots)
			
		if iCiv == iCivGermany:
			self.germanSpawn()

	#Leoreth - adapted from SoI's birthConditional method by embryodead
	def birthInCapital(self, iPlayer, iPreviousOwner, tCapital, tTopLeft, tBottomRight):
		iOwner = iPreviousOwner
		iCiv = civ(iPlayer)
		
		x, y = tCapital
		capital = city(x, y)

		if data.players[iPlayer].iFlipsDelay == 0:

			iFlipsDelay = data.players[iPlayer].iFlipsDelay + 2

			if iFlipsDelay > 0:
			
				# flip capital instead of spawning starting units
				if capital:
					print "birth in capital: (%d, %d)" % (capital.getX(), capital.getY())
					capital = flipCity(capital, False, True, iPlayer, ())
					capital.setHasRealBuilding(iPalace, True)
					convertPlotCulture(plot_(capital), iPlayer, 100, True)
					self.convertSurroundingPlotCulture(iPlayer, plots.surrounding(capital))
				
				#cover plots revealed
				for plot in plots.surrounding((0, 0), radius=2):
					plot.setRevealed(iPlayer, False, True, -1)


				print ("birthConditional: starting units in", x, y)
				self.createStartingUnits(iPlayer, tCapital)

				data.players[iPlayer].iPlagueCountdown
				clearPlague(iPlayer)

				print ("flipping remaining units")
				area = plots.start(tTopLeft).end(tBottomRight)
				for iMinor in players.independent().barbarian():
					flipUnitsInArea(area, iPlayer, iMinor, True, player(iMinor).isBarbarian())
				
				self.assignTechs(iPlayer)
				
				data.players[iPlayer].iFlipsDelay = iFlipsDelay #save

				# kill the catapult and cover the plots
				clearCatapult(iPlayer)
				
				convertPlotCulture(plot_(x, y), iPlayer, 100, True)
				
				# notify dynamic names
				dc.onCityAcquired(iPlayer, iOwner)
				
				self.createStartingWorkers(iPlayer, tCapital)

		else: # starting units have already been placed, now to the second part
			area = plots.start(tTopLeft).end(tBottomRight).without(Areas.getBirthExceptions(iCiv))
			iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iPlayer, area)
			self.convertSurroundingPlotCulture(iPlayer, area)
				
			for iMinorCiv in [iCivIndependent, iCivIndependent2, iCivBarbarian]:
				flipUnitsInArea(area, iPlayer, slot(iMinorCiv), False, True) #remaining barbs/indeps in the region now belong to the new civ   
			
			# kill the catapult and cover the plots
			clearCatapult(iPlayer)
				
			# convert human cities
			if iNumHumanCitiesToConvert > 0:
				print "Flip Popup: in capital"
				self.scheduleFlipPopup(iPlayer, area)
				
			convertPlotCulture(plot(x, y), iPlayer, 100, True)

	def getConvertedCities(self, iPlayer, lPlots = []):
		iCiv = civ(iPlayer)
		lCities = []
		
		for city in cities.of(lPlots):
			if city.plot().isCore(city.getOwner()) and not city.plot().isCore(iPlayer): continue
			
			if city.getOwner() != iPlayer:
				lCities.append(city)
			
		# Leoreth: Byzantium also flips Roman cities in the eastern half of the empire outside of its core (Egypt, Mesopotamia)
		if iCiv == iCivByzantium and player(iCivRome).isAlive():
			x, y = Areas.getCapital(iCivByzantium)
			for city in cities.owner(iCivRome):
				if city.getX() >= x-1 and city.getY() <= y:
					if (city.getX(), city.getY()) not in lPlots:
						lCities.append(city)
					
		# Leoreth: Canada also flips English/American/French cities in the Canada region
		if iCiv == iCivCanada:
			for city in cities.owner(iCivFrance) + cities.owner(iCivEngland) + cities.owner(iCivAmerica):
				if city.getRegionID() == rCanada and city.getX() < Areas.getCapital(iCivCanada)[0] and location(city) not in [location(c) for c in lCities]:
					lCities.append(city)
					
		# Leoreth: remove capital locations
		for city in lCities:
			if not is_minor(city):
				if location(city) == Areas.getCapital(civ(city)) and city.isCapital():
					lCities.remove(city)

		return lCities

	def convertSurroundingCities(self, iPlayer, lPlots):
		iConvertedCitiesCount = 0
		iNumHumanCities = 0
		data.iSpawnWar = 0
					
		lEnemies = []
		lCities = self.getConvertedCities(iPlayer, lPlots)
		
		for city in lCities:
			x = city.getX()
			y = city.getY()
			iOwner = city.getOwner()
			iCultureChange = 0
			
			# Case 1: Minor civilization
			if iOwner in players.minor():
				iCultureChange = 100
				
			# Case 2: Human city
			elif iOwner == human():
				iNumHumanCities += 1
				
			# Case 3: Other
			else:
				iCultureChange = 100
				if iOwner not in lEnemies: lEnemies.append(iOwner)
				
			if iCultureChange > 0:
				completeCityFlip((x, y), iPlayer, iOwner, iCultureChange, True, False, False, True)
				ensureDefenders(iPlayer, (x, y), 2)
				iConvertedCitiesCount += 1
				
		self.warOnSpawn(iPlayer, lEnemies)
				
		if iConvertedCitiesCount > 0:
			message(iPlayer, 'TXT_KEY_FLIP_TO_US', color=iGreen)
				
		return iConvertedCitiesCount, iNumHumanCities

	def warOnSpawn(self, iPlayer, lEnemies):
		iCiv = civ(iPlayer)
	
		if iCiv == iCivCanada: 
			return
			
		elif iCiv == iCivGermany and not player(iPlayer).isHuman():
			return
		
		if year() <= dBirth[iCiv] + 5:
			for iEnemy in lEnemies:
				tEnemy = team(iEnemy)
				
				if tEnemy.isAtWar(iPlayer): continue
				if iCiv == iCivByzantium and civ(iEnemy) == iCivRome: continue
			
				iRand = rand(100)
				if iRand >= dAIStopBirthThreshold[iEnemy]:
					tEnemy.declareWar(iPlayer, True, WarPlanTypes.WARPLAN_ATTACKED_RECENT)
					self.spawnAdditionalUnits(iPlayer)

	def spawnAdditionalUnits(self, iPlayer):
		tPlot = Areas.getCapital(civ(iPlayer))
		self.createAdditionalUnits(iPlayer, tPlot)

	def convertSurroundingPlotCulture(self, iPlayer, plots):
		for plot in plots:
			if plot.isOwned() and plot.isCore(plot.getOwner()) and not plot.isCore(iPlayer): continue
			if not plot.isCity():
				convertPlotCulture(plot, iPlayer, 100, False)

	def findSeaPlots(self, tCoords, iRange, iCiv):
		"""Searches a sea plot that isn't occupied by a unit and isn't a civ's territory surrounding the starting coordinates"""
		return plots.surrounding(tCoords, radius=iRange).water().where(lambda p: not p.isUnit()).where(lambda p: p.getOwner() in [-1, slot(iCiv)]).random()

	def giveRaiders(self, iCiv, lPlots):
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

	def giveEarlyColonists(self, iCiv):
		pPlayer = player(iCiv)
		
		if pPlayer.isAlive() and not pPlayer.isHuman():
			capital = pPlayer.getCapitalCity()

			if iCiv == iCivRome:
				capital = cities.owner(iCiv).region(rIberia).random()
				
			if capital:
				tSeaPlot = self.findSeaPlots(capital, 1, iCiv)
				if tSeaPlot:
					makeUnit(iCiv, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
					makeUnit(iCiv, iSettler, tSeaPlot)
					makeUnit(iCiv, iArcher, tSeaPlot)

	def giveColonists(self, iPlayer):
		pPlayer = player(iPlayer)
		pTeam = team(iPlayer)
		iCiv = civ(iPlayer)
		
		if pPlayer.isAlive() and not pPlayer.isHuman() and iCiv in dMaxColonists:
			if pTeam.isHasTech(iExploration) and data.players[iPlayer].iColonistsAlreadyGiven < dMaxColonists[iCiv]:
				sourceCities = cities.of(Areas.getCoreArea(iCiv)).owner(iPlayer)
				
				# help England with settling Canada and Australia
				if iCiv == iCivEngland:
					colonialCities = cities.start(tCanadaTL).end(tCanadaBR).owner(iPlayer)
					colonialCities += cities.start(tAustraliaTL).end(tAustraliaBR).owner(iPlayer)
					
					if colonialCities:
						sourceCities = colonialCities
						
				city = sourceCities.where(lambda city: city.isCoastal(10)).random()
				if city:
					tSeaPlot = self.findSeaPlots(city, 1, iCiv)
					if not tSeaPlot: tSeaPlot = city
					
					makeUnit(iPlayer, unique_unit(iPlayer, iGalleon), tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
					makeUnit(iPlayer, iSettler, tSeaPlot, UnitAITypes.UNITAI_SETTLE)
					makeUnit(iPlayer, getBestDefender(iPlayer), tSeaPlot)
					makeUnit(iPlayer, iWorker, tSeaPlot)
					
					data.players[iPlayer].iColonistsAlreadyGiven += 1

	def onFirstContact(self, iTeamX, iHasMetTeamY):
		if is_minor(iHasMetTeamY): return
		
		if year().between(600, 1800):
			if civ(iTeamX) in lBioNewWorld and civ(iHasMetTeamY) not in lBioNewWorld:
				iNewWorldPlayer = iTeamX
				iOldWorldPlayer = iHasMetTeamY
				
				iNewWorldCiv = civ(iNewWorldPlayer)
				
				iIndex = lBioNewWorld.index(civ(iNewWorldPlayer))
				
				# TODO: use dict for first contact conquerors to avoid using index
				bAlreadyContacted = data.lFirstContactConquerors[iIndex]
				
				# avoid "return later" exploit
				if year() <= year(dBirth[iCivAztecs]) + turns(10):
					data.lFirstContactConquerors[iIndex] = True
					return
					
				if not bAlreadyContacted:
					if iNewWorldCiv == iCivMaya:
						tContactZoneTL = (15, 30)
						tContactZoneBR = (34, 42)
					elif iNewWorldCiv == iCivAztecs:
						tContactZoneTL = (11, 31)
						tContactZoneBR = (34, 43)
					elif iNewWorldCiv == iCivInca:
						tContactZoneTL = (21, 11)
						tContactZoneBR = (36, 40)
						
					lArrivalExceptions = [(25, 32), (26, 40), (25, 42), (23, 42), (21, 42)]
						
					data.lFirstContactConquerors[iIndex] = True
					
					# change some terrain to end isolation
					if iNewWorldCiv == iCivInca:
						plot(27, 30).setFeatureType(-1, 0)
						plot(28, 31).setFeatureType(-1, 0)
						plot(29, 23).setPlotType(PlotTypes.PLOT_HILLS, True, True)
						plot(31, 13).setPlotType(PlotTypes.PLOT_HILLS, True, True) 
						plot(32, 19).setPlotType(PlotTypes.PLOT_HILLS, True, True)
						plot(27, 29).setPlotType(PlotTypes.PLOT_HILLS, True, True) #Bogota
						
					elif iNewWorldCiv == iCivAztecs:
						plot(40, 66).setPlotType(PlotTypes.PLOT_HILLS, True, True)
						
					newWorldPlots = plots.start(tContactZoneTL).end(tContactZoneBR).without(lArrivalExceptions)
					contactPlots = newWorldPlots.where(lambda p: p.isVisible(iNewWorldPlayer, False) and p.isVisible(iOldWorldPlayer, False))
					arrivalPlots = newWorldPlots.owner(iNewWorldPlayer).where(lambda p: not p.isCity() and isFree(iOldWorldPlayer, p, bCanEnter=True) and not isIsland(p))
					
					if contactPlots and arrivalPlots:
						contactPlot = contactPlots.random()
						arrivalPlot = arrivalPlots.closest(contactPlot)
						
						iModifier1 = 0
						iModifier2 = 0
						
						if player(iNewWorldPlayer).isHuman() and player(iNewWorldPlayer).getNumCities() > 6:
							iModifier1 = 1
						else:
							if iNewWorldCiv == iCivInca or player(iNewWorldPlayer).getNumCities() > 4:
								iModifier1 = 1
							if not player(iNewWorldPlayer).isHuman():
								iModifier2 = 1
								
						if year() < year(dBirth[human()]):
							iModifier1 += 1
							iModifier2 += 1
							
						team(iOldWorldPlayer).declareWar(iNewWorldPlayer, True, WarPlanTypes.WARPLAN_TOTAL)
						
						iInfantry = getBestInfantry(iOldWorldPlayer)
						iCounter = getBestCounter(iOldWorldPlayer)
						iCavalry = getBestCavalry(iOldWorldPlayer)
						iSiege = getBestSiege(iOldWorldPlayer)
						
						iStateReligion = player(iOldWorldPlayer).getStateReligion()
						iMissionary = missionary(iStateReligion)
						
						if iInfantry:
							makeUnits(iOldWorldPlayer, iInfantry, arrivalPlot, 1 + iModifier2, UnitAITypes.UNITAI_ATTACK_CITY)
						
						if iCounter:
							makeUnits(iOldWorldPlayer, iCounter, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
							
						if iSiege:
							makeUnits(iOldWorldPlayer, iSiege, arrivalPlot, 1 + iModifier1 + iModifier2, UnitAITypes.UNITAI_ATTACK_CITY)
							
						if iCavalry:
							makeUnits(iOldWorldPlayer, iCavalry, arrivalPlot, 2 + iModifier1, UnitAITypes.UNITAI_ATTACK_CITY)
							
						if iMissionary:
							makeUnit(iOldWorldPlayer, iMissionary, arrivalPlot)
							
						if iNewWorldCiv == iCivInca:
							makeUnits(iOldWorldPlayer, iAucac, arrivalPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
						elif iNewWorldCiv == iCivAztecs:
							makeUnits(iOldWorldPlayer, iJaguar, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
							makeUnit(iOldWorldPlayer, iHolkan, arrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY)
						elif iNewWorldCiv == iCivMaya:
							makeUnits(iOldWorldPlayer, iHolkan, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
							makeUnit(iOldWorldPlayer, iJaguar, arrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY)
							
						message(iNewWorldPlayer, 'TXT_KEY_FIRST_CONTACT_NEWWORLD')
						message(iOldWorldPlayer, 'TXT_KEY_FIRST_CONTACT_OLDWORLD')
							
		# Leoreth: Mongol horde event against Mughals, Persia, Arabia, Byzantium, Russia
		if civ(iHasMetTeamY) == iCivMongols and not player(iCivMongols).isHuman():
			iCivX = civ(iTeamX)
		
			if iCivX in lMongolCivs:
				if year() < year(1500) and data.isFirstContactMongols(iCivX):

					data.setFirstContactMongols(iCivX, False)
		
					teamTarget = team(iTeamX)
						
					if iCivX == iCivArabia:
						tTL = (73, 31)
						tBR = (84, 43)
						iDirection = DirectionTypes.DIRECTION_EAST
					elif iCivX == iCivPersia:
						tTL = (73, 37)
						tBR = (86, 48)
						iDirection = DirectionTypes.DIRECTION_NORTH
					elif iCivX == iCivByzantium:
						tTL = (68, 41)
						tBR = (77, 46)
						iDirection = DirectionTypes.DIRECTION_EAST
					elif iCivX == iCivRussia:
						tTL = (68, 48)
						tBR = (81, 62)
						iDirection = DirectionTypes.DIRECTION_EAST

					try:
						lTargetList = getBorderPlots(iTeamX, tTL, tBR, iDirection, 3)
					except Exception, e:
						raise Exception("Exception for iCivX=%d: %s" % (iCivX, e))
					
					if not lTargetList: return

					team(iCivMongols).declareWar(iTeamX, True, WarPlanTypes.WARPLAN_TOTAL)
					
					iHandicap = 0
					if teamtype(iTeamX).isHuman():
						iHandicap = game.getHandicapType() / 2

					for tPlot in lTargetList:
						makeUnits(iCivMongols, iKeshik, tPlot, 2 + iHandicap, UnitAITypes.UNITAI_ATTACK_CITY)
						makeUnits(iCivMongols, iMangudai, tPlot, 1 + 2 * iHandicap, UnitAITypes.UNITAI_ATTACK_CITY)
						makeUnits(iCivMongols, iTrebuchet, tPlot, 1 + iHandicap, UnitAITypes.UNITAI_ATTACK_CITY)
						
					message(iTeamX, 'TXT_KEY_MONGOL_HORDE_HUMAN')
					if team().canContact(iTeamX):
						message(human(), 'TXT_KEY_MONGOL_HORDE', adjective(iTeamX))

	def lateTradingCompany(self, iPlayer):
		iCiv = civ(iPlayer)
	
		if not player(iPlayer).isHuman() and not team(iPlayer).isAVassal() and scenario() != i1700AD:
			if iCiv in [iCivFrance, iCivEngland, iCivNetherlands]:
				self.handleColonialConquest(iPlayer)

	def earlyTradingCompany(self, iPlayer):
		iCiv = civ(iPlayer)
	
		if not player(iPlayer).isHuman() and not team(iPlayer).isAVassal():
			if iCiv in [iCivSpain, iCivPortugal]:
				self.handleColonialAcquisition(iPlayer)
				
	def onRailroadDiscovered(self, iPlayer):
		iCiv = civ(iPlayer)
	
		if not player(iPlayer).isHuman():
			if iCiv == iCivAmerica:
				iCount = 0
				lWestCoast = [(11, 50), (11, 49), (11, 48), (11, 47), (11, 46), (12, 45)]
				
				enemyCities = cities.of(lWestCoast).notowner(iCivAmerica)
				
				for iEnemy in enemyCities.owners():
					team(iPlayer).declareWar(iEnemy, True, WarPlanTypes.WARPLAN_LIMITED)
				
				for city in enemyCities:
					plot = plots.surrounding(city).random()
					makeUnits(iPlayer, iMinuteman, plot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
					makeUnits(iPlayer, iCannon, plot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
						
				if enemyCities.count() < 2:
					for plot in plots.of(lWestCoast).without(enemyCities).sample(2 - enemyCities.count()):
						makeUnit(iPlayer, iSettler, plot)
						makeUnit(iPlayer, iMinuteman, plot)
						
			elif iCiv == iCivRussia:
				lFreePlots = []
				x, y = (111, 51)
				
				city = city_(x, y)
				plot = plot_(x, y)
				convertPlotCulture(plot, iPlayer, 100, True)
				if city:
					if civ(city) != iCivRussia:
						for plot in plots.surrounding(x, y):
							if not (plot.isCity() or plot.isWater() or plot.isPeak()):
								lFreePlots.append((i, j))
									
						tPlot = random_entry(lFreePlots)
						team(iPlayer).declareWar(plot.getOwner(), True, WarPlanTypes.WARPLAN_LIMITED)
						makeUnits(iPlayer, iRifleman, tPlot, 4, UnitAITypes.UNITAI_ATTACK_CITY)
						makeUnits(iPlayer, iCannon, tPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
				else:
					if isFree(iPlayer, (x, y), True): # Also bNoEnemyUnits?
						player(iPlayer).found(x, y)
						makeUnits(iPlayer, iRifleman, (x, y), 2)
						
						for plot in plots.surrounding(x, y):
							convertPlotCulture(plot, iPlayer, 80, True)

	def handleColonialAcquisition(self, iPlayer):
		pPlayer = player(iPlayer)
		iCiv = civ(iPlayer)
		
		targets = getColonialTargets(iPlayer, bEmpty=True)
		if not targets:
			return
			
		targetPlayers = []
		settledPlots = []

		iGold = len(targets) * 200

		for plot in targets:
			city = city_(plot)
			if city:
				iTarget = city.getOwner()
				if not iTarget in targetPlayers:
					targetPlayers.append(iTarget)
			else:
				settledPlots.append(location(plot))

		for tPlot in settledPlots:
			colonialAcquisition(iPlayer, tPlot)
	
		for iTarget in targetPlayers:
			if player(iTarget).isHuman():
				askedCities = [(x, y) for x, y in targets if city_(x, y).getOwner() == iTarget]
				message = format_separators(askedCities, ',', text("TXT_KEY_AND"), lambda tPlot: city_(tPlot).getName())
						
				iAskGold = len(askedCities) * 200
						
				popup = Popup.PyPopup(7625, EventContextTypes.EVENTCONTEXT_ALL)
				popup.setHeaderString(text("TXT_KEY_ASKCOLONIALCITY_TITLE", adjective(iPlayer)))
				popup.setBodyString(text("TXT_KEY_ASKCOLONIALCITY_MESSAGE", adjective(iPlayer), iAskGold, message))
				popup.addButton(text("TXT_KEY_POPUP_YES"))
				popup.addButton(text("TXT_KEY_POPUP_NO"))
				data.lTempEventList = (iPlayer, askedCities)
				popup.launch(False)
				
			else:
				bAccepted = is_minor(iTarget) or (rand(100) >= dPatienceThreshold[iTarget] and not team(iPlayer).isAtWar(iTarget))
				iNumCities = count(targets, lambda tPlot: city_(tPlot).getOwner() == iTarget)
						
				if iNumCities >= player(iTarget).getNumCities():
					bAccepted = False

				for tPlot in targets:
					if city_(tPlot).getOwner() == iTarget:
						if bAccepted:
							colonialAcquisition(iPlayer, tPlot)
							player(iTarget).changeGold(200)
						else:
							data.timedConquest(iPlayer, tPlot)

		iNewGold = pPlayer.getGold() - iGold
		pPlayer.setGold(max(0, iNewGold))

	def handleColonialConquest(self, iPlayer):
		targetList = getColonialTargets(iPlayer)
		
		if not targetList:
			self.handleColonialAcquisition(iPlayer)
			return

		for tPlot in targetList:
			data.timedConquest(iPlayer, tPlot)
			
		seaPlot = plots.surrounding(targetList[0]).water().random()

		if seaPlot:
			makeUnit(iPlayer, unique_unit(iPlayer, iGalleon), seaPlot)

	def startWarsOnSpawn(self, iPlayer):
		pPlayer = player(iPlayer)
		pTeam = team(iPlayer)
		iCiv = civ(iPlayer)
		
		iMin = 10
		
		if rand(100) >= iMin:
			for iLoopCiv in dEnemyCivsOnSpawn[iCiv]:
				iLoopPlayer = slot(iLoopCiv)
			
				if team(iLoopPlayer).isAVassal(): continue
				if not player(iLoopPlayer).isAlive(): continue
				if pTeam.isAtWar(iLoopPlayer): continue
				if player(iPlayer).isHuman() and iLoopCiv not in dTotalWarOnSpawn[iCiv]: continue
				
				iLoopMin = 50
				if is_minor(iLoopPlayer): iLoopMin = 30
				if player(iLoopPlayer).isHuman(): iLoopMin += 10
				
				if rand(100) >= iLoopMin:
					iWarPlan = -1
					if iLoopCiv in dTotalWarOnSpawn[iCiv]:
						iWarPlan = WarPlanTypes.WARPLAN_TOTAL
					pTeam.declareWar(iLoopPlayer, False, iWarPlan)
					
					if pPlayer.isHuman(): data.iBetrayalTurns = 0

	def immuneMode(self, argsList): 
		pWinningUnit,pLosingUnit = argsList
		iLosingPlayer = pLosingUnit.getOwner()
		iUnitType = pLosingUnit.getUnitType()
		if not is_minor(iLosingPlayer):
			iBirthTurn = year(dBirth[iLosingPlayer])
			if iBirthTurn <= year() <= iBirthTurn+2:
				if location(pLosingUnit) == Areas.getCapital(civ(iLosingPlayer)):
					if rand(100) >= 50:
						makeUnit(iLosingPlayer, iUnitType, pLosingUnit)

	def initMinorBetrayal(self, iPlayer):
		lPlots = Areas.getBirthArea(civ(iPlayer))
		plotList = listSearch(lPlots, outerInvasion, [])
		if plotList:
			tPlot = random_entry(plotList)
			if tPlot:
				self.createAdditionalUnits(iPlayer, tPlot)
				self.unitsBetrayal(iPlayer, human(), lPlots, tPlot)

	def initBetrayal( self ):
		iFlipPlayer = data.iFlipNewPlayer
		if not player(iFlipPlayer).isAlive() or not team(iFlipPlayer).isAtWar(human()):
			data.iBetrayalTurns = 0
			return
	
		turnsLeft = data.iBetrayalTurns
		
		lTempPlots = [tPlot for tPlot in data.lTempPlots if not plot(tPlot).isCore(data.iFlipOldPlayer)]
		plotList = listSearch(lTempPlots, outerInvasion, [] )
		if not plotList:
			plotList = listSearch(lTempPlots, innerSpawn, [data.iFlipOldPlayer, data.iFlipNewPlayer] )			
		if not plotList:
			plotList = listSearch(lTempPlots, innerInvasion, [data.iFlipOldPlayer, data.iFlipNewPlayer] )				
		if plotList:
			tPlot = random_entry(plotList)
			if tPlot:
				if turnsLeft == iBetrayalPeriod:
					self.createAdditionalUnits(data.iFlipNewPlayer, tPlot)
				self.unitsBetrayal(data.iFlipNewPlayer, data.iFlipOldPlayer, lTempPlots, tPlot)
		data.iBetrayalTurns = turnsLeft - 1

	def unitsBetrayal(self, iNewOwner, iOldOwner, lPlots, tPlot):
		message(data.iFlipOldPlayer, 'TXT_KEY_FLIP_BETRAYAL', color=iGreen)
		message(data.iFlipNewPlayer, 'TXT_KEY_FLIP_BETRAYAL_NEW', color=iGreen)
		
		for x, y in lPlots:
			for unit in units.at(x, y).owner(iOldOwner).domain(DomainTypes.DOMAIN_LAND):
				if rand(100) >= iBetrayalThreshold:
					iUnitType = unit.getUnitType()
					unit.kill(False, iNewOwner)
					makeUnit(iNewOwner, iUnitType, tPlot)

	def createAdditionalUnits(self, iPlayer, tPlot):
		iCiv = civ(iPlayer)
	
		if iCiv == iCivIndia:
			makeUnits(iPlayer, iArcher, tPlot, 2)
			makeUnit(iPlayer, iLightSwordsman, tPlot)
		elif iCiv == iCivGreece:
			makeUnits(iPlayer, iHoplite, tPlot, 4)
		elif iCiv == iCivPersia:
			makeUnits(iPlayer, iImmortal, tPlot, 4)
		elif iCiv == iCivCarthage:
			makeUnit(iPlayer, iWarElephant, tPlot)
			makeUnit(iPlayer, iNumidianCavalry, tPlot)
		elif iCiv == iCivPolynesia:
			makeUnits(iPlayer, iMilitia, tPlot, 2)
		elif iCiv == iCivRome:
			makeUnits(iPlayer, iLegion, tPlot, 4)
		elif iCiv == iCivJapan:
			makeUnits(iPlayer, iArcher, tPlot, 2)
			makeUnits(iPlayer, iSwordsman, tPlot, 2)
		elif iCiv == iCivTamils:
			makeUnits(iPlayer, iSwordsman, tPlot, 2)
			makeUnit(iPlayer, iWarElephant, tPlot)
		elif iCiv == iCivEthiopia:
			makeUnits(iPlayer, iArcher, tPlot, 2)
			makeUnits(iPlayer, iShotelai, tPlot, 2)
		elif iCiv == iCivKorea:
			makeUnits(iPlayer, iHorseArcher, tPlot, 2)
			makeUnits(iPlayer, iCrossbowman, tPlot, 2)
		elif iCiv == iCivMaya:
			makeUnits(iPlayer, iArcher, tPlot, 2)
			makeUnits(iPlayer, iHolkan, tPlot, 2)
		elif iCiv == iCivByzantium:
			makeUnits(iPlayer, iCataphract, tPlot, 2)
			makeUnits(iPlayer, iHorseArcher, tPlot, 2)
		elif iCiv == iCivVikings:
			makeUnits(iPlayer, iHuscarl, tPlot, 3)
		elif iCiv == iCivTurks:
			makeUnits(iPlayer, iOghuz, tPlot, 4)
		elif iCiv == iCivArabia:
			makeUnits(iPlayer, iGhazi, tPlot, 2)
			makeUnits(iPlayer, iMobileGuard, tPlot, 4)
		elif iCiv == iCivTibet:
			makeUnits(iPlayer, iKhampa, tPlot, 2)
		elif iCiv == iCivKhmer:
			makeUnits(iPlayer, iSwordsman, tPlot, 3)
			makeUnits(iPlayer, iBallistaElephant, tPlot, 2)
		elif iCiv == iCivIndonesia:
			makeUnits(iPlayer, iSwordsman, tPlot, 2)
			makeUnit(iPlayer, iWarElephant, tPlot)
		elif iCiv == iCivMoors:
			makeUnits(iPlayer, iCamelArcher, tPlot, 2)
		elif iCiv == iCivSpain:
			makeUnits(iPlayer, iCrossbowman, tPlot, 3)
			makeUnits(iPlayer, iSwordsman, tPlot, 3)
		elif iCiv == iCivFrance:
			makeUnits(iPlayer, iCrossbowman, tPlot, 3)
			makeUnits(iPlayer, iSwordsman, tPlot, 3)
		elif iCiv == iCivEngland:
			makeUnits(iPlayer, iCrossbowman, tPlot, 3)
			makeUnits(iPlayer, iSwordsman, tPlot, 3)
		elif iCiv == iCivHolyRome:
			makeUnits(iPlayer, iCrossbowman, tPlot, 3)
			makeUnits(iPlayer, iSwordsman, tPlot, 3)
		elif iCiv == iCivRussia:
			makeUnits(iPlayer, iCrossbowman, tPlot, 2)
			makeUnits(iPlayer, iSwordsman, tPlot, 2)
			makeUnits(iPlayer, iHorseArcher, tPlot, 2)
		elif iCiv == iCivNetherlands:
			makeUnits(iPlayer, iMusketeer, tPlot, 3)
			makeUnits(iPlayer, iPikeman, tPlot, 3)
		elif iCiv == iCivMali:
			makeUnits(iPlayer, iKelebolo, tPlot, 4)
			makeUnits(iPlayer, iSwordsman, tPlot, 3)
		elif iCiv == iCivOttomans:
			makeUnits(iPlayer, iCrossbowman, tPlot, 3)
			makeUnits(iPlayer, iHorseArcher, tPlot, 3)
		elif iCiv == iCivPoland:
			makeUnits(iPlayer, iLancer, tPlot, 2)
			makeUnits(iPlayer, iCrossbowman, tPlot, 2)
		elif iCiv == iCivPortugal:
			makeUnits(iPlayer, iCrossbowman, tPlot, 3)
			makeUnits(iPlayer, iPikeman, tPlot, 3)
		elif iCiv == iCivInca:
			makeUnits(iPlayer, iAucac, tPlot, 5)
			makeUnits(iPlayer, iArcher, tPlot, 3)
		elif iCiv == iCivItaly:
			makeUnits(iPlayer, iLancer, tPlot, 2)
		elif iCiv == iCivMongols:
			makeUnits(iPlayer, iCrossbowman, tPlot, 2)
			makeUnits(iPlayer, iMangudai, tPlot, 2)
			makeUnits(iPlayer, iKeshik, tPlot, 4)
		elif iCiv == iCivAztecs:
			makeUnits(iPlayer, iJaguar, tPlot, 5)
			makeUnits(iPlayer, iArcher, tPlot, 3)
		elif iCiv == iCivMughals:
			makeUnits(iPlayer, iSiegeElephant, tPlot, 2)
			makeUnits(iPlayer, iHorseArcher, tPlot, 4)
		elif iCiv == iCivThailand:
			makeUnits(iPlayer, iPikeman, tPlot, 2)
			makeUnits(iPlayer, iChangSuek, tPlot, 2)
		elif iCiv == iCivCongo:
			makeUnits(iPlayer, iPombos, tPlot, 3)
		elif iCiv == iCivGermany:
			makeUnits(iPlayer, iFusilier, tPlot, 5)
			makeUnits(iPlayer, iBombard, tPlot, 3)
		elif iCiv == iCivAmerica:
			makeUnits(iPlayer, iGrenadier, tPlot, 3)
			makeUnits(iPlayer, iMinuteman, tPlot, 3)
			makeUnits(iPlayer, iCannon, tPlot, 3)
		elif iCiv == iCivArgentina:
			makeUnits(iPlayer, iRifleman, tPlot, 2)
			makeUnits(iPlayer, iGrenadierCavalry, tPlot, 4)
		elif iCiv == iCivBrazil:
			makeUnits(iPlayer, iGrenadier, tPlot, 2)
			makeUnits(iPlayer, iRifleman, tPlot, 3)
			makeUnits(iPlayer, iCannon, tPlot, 2)
		elif iCiv == iCivCanada:
			makeUnits(iPlayer, iCavalry, tPlot, 2)
			makeUnits(iPlayer, iRifleman, tPlot, 4)
			makeUnits(iPlayer, iCannon, tPlot, 2)

	def createStartingUnits(self, iPlayer, tPlot):
		iCiv = civ(iPlayer)
	
		if iCiv == iCivChina:
			createSettlers(iPlayer, 1)
			makeUnit(iPlayer, iArcher, tPlot)
			makeUnit(iPlayer, iMilitia, tPlot)
		elif iCiv == iCivIndia:
			createSettlers(iPlayer, 1)
			makeUnit(iPlayer, iArcher, tPlot)
			makeUnit(iPlayer, iSpearman, tPlot)
			makeUnit(iPlayer, iLightSwordsman, tPlot)
			makeUnit(iPlayer, iChariot, tPlot)
		elif iCiv == iCivGreece:
			createSettlers(iPlayer, 1)
			makeUnits(iPlayer, iMilitia, tPlot, 2)
			makeUnit(iPlayer, iHoplite, tPlot)
			makeUnit(iPlayer, iHoplite, tPlot, UnitAITypes.UNITAI_ATTACK)
			makeUnit(iPlayer, iHoplite, tPlot, UnitAITypes.UNITAI_ATTACK_CITY)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
				makeUnit(iPlayer, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iMilitia, tSeaPlot)
		elif iCiv == iCivPersia:
			createSettlers(iPlayer, 3)
			makeUnits(iPlayer, iArcher, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iImmortal, tPlot, 4)
			makeUnits(iPlayer, iHorseman, tPlot, 2)
			makeUnit(iPlayer, iWarElephant, tPlot)
		elif iCiv == iCivCarthage:
			createSettlers(iPlayer, 1)
			makeUnit(iPlayer, iArcher, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnit(iPlayer, iSacredBand, tPlot)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iWorkboat, tSeaPlot, 2)
				makeUnit(iPlayer, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iArcher, tSeaPlot)
				makeUnit(iPlayer, iGalley, tSeaPlot, UnitAITypes.UNITAI_ASSAULT_SEA)
				makeUnit(iPlayer, iWarGalley, tSeaPlot, UnitAITypes.UNITAI_ESCORT_SEA)
		elif iCiv == iCivPolynesia:
			tSeaPlot = (4, 19)
			makeUnit(iPlayer, iSettler, tPlot)
			makeUnit(iPlayer, iWaka, tSeaPlot)
			makeUnit(iPlayer, iSettler, tSeaPlot)
			makeUnit(iPlayer, iWorkboat, tSeaPlot)
		elif iCiv == iCivRome:
			createSettlers(iPlayer, 3)
			makeUnits(iPlayer, iArcher, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iLegion, tPlot, 4)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
				makeUnits(iPlayer, iGalley, tSeaPlot, 2, UnitAITypes.UNITAI_ASSAULT_SEA)
		elif iCiv == iCivMaya:
			createSettlers(iPlayer, 1)
			makeUnits(iPlayer, iHolkan, tPlot, 2)
		elif iCiv == iCivJapan:
			createSettlers(iPlayer, 3)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iSwordsman, tPlot, 2)
			makeUnits(iPlayer, iArcher, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
				
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iCrossbowman, tPlot, 2)
				makeUnits(iPlayer, iSamurai, tPlot, 3)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iWorkboat, tSeaPlot, 2)
		elif iCiv == iCivTamils:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnit(iPlayer, iArcher, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnit(iPlayer, iWarElephant, tPlot)
			makeUnits(iPlayer, iSwordsman, tPlot, 2)
			
			if not player(iPlayer).isHuman():
				makeUnit(iPlayer, iHinduMissionary, tPlot)
				makeUnit(iPlayer, iWarElephant, tPlot)
				
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
				makeUnit(iPlayer, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iWarGalley, tSeaPlot)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iArcher, tSeaPlot)
		elif iCiv == iCivEthiopia:
			createSettlers(iPlayer, 2)
			makeUnits(iPlayer, iArcher, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnit(iPlayer, iShotelai, tPlot)
			makeUnit(iPlayer, iLightSwordsman, tPlot)
			
			tSeaPlot = (74, 29)
			makeUnit(iPlayer, iWorkboat, tSeaPlot)
			makeUnit(iPlayer, iWarGalley, tSeaPlot)
		elif iCiv == iCivKorea:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iArcher, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnit(iPlayer, iSwordsman, tPlot)
			makeUnit(iPlayer, iHorseman, tPlot)
			
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iSpearman, tPlot, 2)
				makeUnits(iPlayer, iCrossbowman, tPlot, 2)
		elif iCiv == iCivByzantium:
			createSettlers(iPlayer, 4)
			createMissionaries(iPlayer, 1)
			
			makeUnits(iPlayer, iLegion, tPlot, 4)
			makeUnits(iPlayer, iSpearman, tPlot, 2)
			makeUnits(iPlayer, iArcher, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iGalley, tSeaPlot, 2)
				makeUnits(iPlayer, iWarGalley, tSeaPlot, 2)
				if scenario() == i3000BC:
					makeUnit(iPlayer, iWorkboat, tSeaPlot)
		elif iCiv == iCivVikings:
			createSettlers(iPlayer, 2)
			makeUnits(iPlayer, iArcher, tPlot, 4, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iHuscarl, tPlot, 3)
			makeUnit(iPlayer, iScout, tPlot)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
				makeUnit(iPlayer, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iArcher, tSeaPlot)
				makeUnits(iPlayer, iLongship, tSeaPlot, 2, UnitAITypes.UNITAI_EXPLORE_SEA)
		elif iCiv == iCivTurks:
			createSettlers(iPlayer, 6)
			if player(iPlayer).isHuman():
				makeUnits(iPlayer, iArcher, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			else:
				makeUnits(iPlayer, iCrossbowman, tPlot, 4, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iOghuz, tPlot, 6)
			makeUnit(iPlayer, iScout, tPlot)
		elif iCiv == iCivArabia:
			createSettlers(iPlayer, 2)
			makeUnit(iPlayer, iArcher, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iMobileGuard, tPlot, 2)
			makeUnits(iPlayer, iGhazi, tPlot, 2)
			makeUnit(iPlayer, iWorker, tPlot)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
		elif iCiv == iCivTibet:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iArcher, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iKhampa, tPlot, 2)
		elif iCiv == iCivKhmer:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			createMissionaries(iPlayer, 1, iBuddhism)
			makeUnit(iPlayer, iArcher, tPlot, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iBallistaElephant, tPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
			
			tSeaPlot = self.findSeaPlots(tPlot, 2, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
				makeUnit(iPlayer, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iArcher, tSeaPlot)
		elif iCiv == iCivIndonesia:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnit(iPlayer, iArcher, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
				makeUnit(iPlayer, iWarGalley, tSeaPlot)
				makeUnits(iPlayer, iGalley, tSeaPlot, 2, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iArcher, tSeaPlot)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iArcher, tSeaPlot)
		elif iCiv == iCivMoors:
			createSettlers(iPlayer, 2)
			createMissionaries(iPlayer, 2)
			makeUnit(iPlayer, iCrossbowman, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iSwordsman, tPlot, 2)
			makeUnits(iPlayer, iSpearman, tPlot, 2)
			makeUnits(iPlayer, iHorseArcher, tPlot, 2)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iGalley, tSeaPlot)
				makeUnit(iPlayer, iHeavyGalley, tSeaPlot)
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
			
			if civ(human()) in [iCivSpain, iCivMoors]:
				makeUnit(iPlayer, iCrossbowman, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
		elif iCiv == iCivSpain:
			iSpanishSettlers = 2
			if not player(iPlayer).isHuman(): iSpanishSettlers = 3
			createSettlers(iPlayer, iSpanishSettlers)
			createMissionaries(iPlayer, 1)
			makeUnit(iPlayer, iCrossbowman, tPlot)
			makeUnit(iPlayer, iCrossbowman, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iSwordsman, tPlot, 4)
			
			# TODO: should be isCivEnabled
			if data.isCivEnabled(iCivMoors):
				if not player(iCivMoors).isHuman():
					makeUnits(iPlayer, iLancer, tPlot, 2)
			else:
				makeUnit(iPlayer, iSettler, tPlot)
				
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iCrossbowman, tPlot, 2)
				
			if scenario() == i600AD: #late start condition
				makeUnit(iPlayer, iWorker, tPlot) #there is no carthaginian city in Iberia and Portugal may found 2 cities otherwise (a settler is too much)
		elif iCiv == iCivFrance:
			createSettlers(iPlayer, 3)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iCrossbowman, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iHeavySpearman, tPlot, 2)
			makeUnits(iPlayer, iSwordsman, tPlot, 3)
		elif iCiv == iCivEngland:
			createSettlers(iPlayer, 3)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iCrossbowman, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iHeavySwordsman, tPlot, 2)
				
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iWorkboat, tSeaPlot, 2)
				makeUnit(iPlayer, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tPlot)
				makeUnit(iPlayer, iCrossbowman, tPlot)
				makeUnits(iPlayer, iGalley, tPlot, 2)
		elif iCiv == iCivHolyRome:
			createSettlers(iPlayer, 3)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iCrossbowman, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iSwordsman, tPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iLancer, tPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iCatapult, tPlot, 4, UnitAITypes.UNITAI_ATTACK_CITY)
		elif iCiv == iCivRussia:
			createSettlers(iPlayer, 4)
			makeUnits(iPlayer, iCrossbowman, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iHorseArcher, tPlot, 4)
		elif iCiv == iCivNetherlands:
			createSettlers(iPlayer, 2)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iArquebusier, tPlot, 6)
			makeUnits(iPlayer, iBombard, tPlot, 2)
			makeUnits(iPlayer, iPikeman, tPlot, 2)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iWorkboat, tSeaPlot, 2)
				makeUnit(iPlayer, iEastIndiaman, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iCrossbowman, tSeaPlot)
				makeUnit(iPlayer, iEastIndiaman, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iCrossbowman, tSeaPlot)
				makeUnits(iPlayer, iCaravel, tSeaPlot, 2)
		elif iCiv == iCivMali:
			createSettlers(iPlayer, 3)
			createMissionaries(iPlayer, 2)
			makeUnits(iPlayer, iKelebolo, tPlot, 5)
		elif iCiv == iCivPoland:
			iNumSettlers = 1
			if player(iPlayer).isHuman(): iNumSettlers = 2
			createSettlers(iPlayer, iNumSettlers)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iCrossbowman, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iHeavySwordsman, tPlot, 2)
			makeUnits(iPlayer, iLancer, tPlot, 2)
			
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iHeavySpearman, tPlot, 2)
		elif iCiv == iCivOttomans:
			createMissionaries(iPlayer, 3)
			makeUnits(iPlayer, iHeavySwordsman, tPlot, 2)
			makeUnits(iPlayer, iCrossbowman, tPlot, 2)
			makeUnits(iPlayer, iLancer, tPlot, 3)
			makeUnits(iPlayer, iJanissary, tPlot, 2)
			makeUnits(iPlayer, iGreatBombard, tPlot, 2)
			makeUnits(iPlayer, iTrebuchet, tPlot, 2)
			
			if player(iPlayer).isHuman():
				makeUnits(iPlayer, iGreatBombard, tPlot, 4)
				makeUnits(iPlayer, iJanissary, tPlot, 5)
				makeUnits(iPlayer, iLancer, tPlot, 4)
		elif iCiv == iCivPortugal:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iCrossbowman, tPlot, 4, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iHeavySpearman, tPlot, 2)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iWorkboat, tSeaPlot, 2)
				makeUnit(iPlayer, iCog, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iCrossbowman, tSeaPlot)
				makeUnit(iPlayer, iHeavyGalley, tSeaPlot, UnitAITypes.UNITAI_EXPLORE_SEA)
		elif iCiv == iCivInca:
			createSettlers(iPlayer, 1)
			makeUnits(iPlayer, iAucac, tPlot, 4)
			makeUnits(iPlayer, iArcher, tPlot, 2)
			
			if not player(iPlayer).isHuman():
				makeUnit(iPlayer, iSettler, tPlot)
		elif iCiv == iCivItaly:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iBalestriere, tPlot, 3)
			makeUnits(iPlayer, iHeavySpearman, tPlot, 2)
			makeUnits(iPlayer, iTrebuchet, tPlot, 3)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iWorkboat, tSeaPlot, 2)
				makeUnit(iPlayer, iCog, tSeaPlot)
				makeUnit(iPlayer, iHeavyGalley, tSeaPlot)
		elif iCiv == iCivMongols:
			createSettlers(iPlayer, 3)
			makeUnits(iPlayer, iCrossbowman, tPlot, 3)
			makeUnits(iPlayer, iHeavySwordsman, tPlot, 2)
			makeUnits(iPlayer, iMangudai, tPlot, 2)
			makeUnits(iPlayer, iKeshik, tPlot, 6, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iBombard, tPlot, 3)
			
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iKeshik, tPlot, 10, UnitAITypes.UNITAI_ATTACK_CITY)
				makeUnits(iPlayer, iBombard, tPlot, 5, UnitAITypes.UNITAI_ATTACK_CITY)
				makeUnits(iPlayer, iHeavySwordsman, tPlot, 2, UnitAITypes.UNITAI_COUNTER)
				makeUnits(iPlayer, iScout, tPlot, 2, UnitAITypes.UNITAI_EXPLORE)
				makeUnits(iPlayer, iCrossbowman, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
		elif iCiv == iCivAztecs:
			createSettlers(iPlayer, 2)
			makeUnits(iPlayer, iJaguar, tPlot, 4)
			makeUnits(iPlayer, iArcher, tPlot, 4, UnitAITypes.UNITAI_CITY_DEFENSE)
		elif iCiv == iCivMughals:
			createSettlers(iPlayer, 3)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iSiegeElephant, tPlot, 3)
			makeUnits(iPlayer, iHeavySwordsman, tPlot, 4).experience(2)
			makeUnits(iPlayer, iHorseArcher, tPlot, 2)
			
			if player(iPlayer).isHuman():
				makeUnits(iPlayer, iIslamicMissionary, tPlot, 3)
		elif iCiv == iCivThailand:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iHeavySpearman, tPlot, 3)
			makeUnits(iPlayer, iChangSuek, tPlot, 2)
		elif iCiv == iCivCongo:
			createSettlers(iPlayer, 1)
			makeUnits(iPlayer, iArcher, tPlot, 2)
			makeUnits(iPlayer, iPombos, tPlot, 2)
		elif iCiv == iCivGermany:
			createSettlers(iPlayer, 4)
			createMissionaries(iPlayer, 2)
			makeUnits(iPlayer, iArquebusier, tPlot, 3).experience(2)
			makeUnits(iPlayer, iArquebusier, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE).experience(2)
			makeUnits(iPlayer, iBombard, tPlot, 3).experience(2)
			
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iArquebusier, tPlot, 10).experience(2)
				makeUnits(iPlayer, iBombard, tPlot, 5).experience(2)
		elif iCiv == iCivAmerica:
			createSettlers(iPlayer, 8)
			makeUnits(iPlayer, iGrenadier, tPlot, 2)
			makeUnits(iPlayer, iMinuteman, tPlot, 4)
			makeUnits(iPlayer, iCannon, tPlot, 2)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iWorkboat, tSeaPlot, 2)
				makeUnits(iPlayer, iGalleon, tSeaPlot, 2)
				makeUnit(iPlayer, iFrigate, tSeaPlot)
				
			if not player(iPlayer).isHuman():
				makeUnit(iPlayer, iMinuteman, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
				
			iReligion = self.findAreaReligion(iPlayer, plots.start(23, 40).end(33, 52))
			if iReligion >= 0:
				player(iPlayer).setLastStateReligion(iReligion)
				makeUnit(iPlayer, missionary(iReligion), tPlot)
		elif iCiv == iCivArgentina:
			createSettlers(iPlayer, 2)
			makeUnits(iPlayer, iMusketeer, tPlot, 3).experience(2)
			makeUnits(iPlayer, iGrenadierCavalry, tPlot, 3).experience(2)
			makeUnits(iPlayer, iCannon, tPlot, 2).experience(2)
			
			tSeaPlot = self.findSeaPlots(tPlot, 2, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iGalleon, tSeaPlot)
				makeUnits(iPlayer, iFrigate, tSeaPlot, 2)
				
			if not player(iPlayer).isHuman():
				makeUnit(iPlayer, iMusketeer, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
				makeUnits(iPlayer, iMusketeer, tPlot, 2).experience(2)
				makeUnits(iPlayer, iGrenadierCavalry, tPlot, 2).experience(2)
				makeUnits(iPlayer, iCannon, tPlot, 2).experience(2)
		elif iCiv == iCivBrazil:
			createSettlers(iPlayer, 5)
			makeUnits(iPlayer, iGrenadier, tPlot, 3)
			makeUnits(iPlayer, iMusketeer, tPlot, 3)
			makeUnits(iPlayer, iCannon, tPlot, 2)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iWorkboat, tSeaPlot, 2)
				makeUnits(iPlayer, iGalleon, tSeaPlot, 2)
				makeUnits(iPlayer, iFrigate, tSeaPlot, 3)
				
			if not player(iPlayer).isHuman():
				makeUnit(iPlayer, iRifleman, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
		elif iCiv == iCivCanada:
			createSettlers(iPlayer, 5)
			makeUnits(iPlayer, iDragoon, tPlot, 3)
			makeUnits(iPlayer, iRifleman, tPlot, 5)
			
			tSeaPlot = self.findSeaPlots(tPlot, 2, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iSteamship, tSeaPlot, 2)
				makeUnit(iPlayer, iIronclad, tSeaPlot)
				makeUnit(iPlayer, iTorpedoBoat, tSeaPlot)
				
		# Leoreth: start wars on spawn when the spawn actually happens
		self.startWarsOnSpawn(iPlayer)

	def createRespawnUnits(self, iPlayer, tPlot):
		iCiv = civ(iPlayer)
	
		if iCiv == iCivIran:
			makeUnits(iPlayer, iQizilbash, tPlot, 6)
			makeUnits(iPlayer, iBombard, tPlot, 3)
			makeUnits(iPlayer, iWorker, tPlot, 3)
			
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iQizilbash, tPlot, 6)
				makeUnits(iPlayer, iBombard, tPlot, 3)
		elif iCiv == iCivMexico:
			makeUnits(iPlayer, iDragoon, tPlot, 4).experience(2)
			makeUnits(iPlayer, iMusketeer, tPlot, 5).experience(2)
			makeUnits(iPlayer, iGrenadier, tPlot, 2).experience(2)
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iCivColombia:
			makeUnits(iPlayer, iMusketeer, tPlot, 5).experience(2)
			makeUnits(iPlayer, iCannon, tPlot, 5).experience(2)
			makeUnits(iPlayer, iAlbionLegion, tPlot, 5).experience(2)
			makeUnits(iPlayer, iWorker, tPlot, 3)
			
			tSeaPlot = self.findSeaPlots(tPlot, 3, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iGalleon, tSeaPlot)
				makeUnit(iPlayer, iFrigate, tSeaPlot)
				
	def findAreaReligion(self, iPlayer, area):
		lReligions = [0 for i in range(iNumReligions)]
		
		for plot in area:
			if plot.isCity():
				city = plot.getPlotCity()
				iOwner = city.getOwner()
				if iOwner != iPlayer:
					for iReligion in range(iNumReligions):
						if city.isHasReligion(iReligion):
							lReligions[iReligion] += 1
					iStateReligion = player(iOwner).getStateReligion()
					if iStateReligion >= 0:
						lReligions[iStateReligion] += 1
						
		iMax = 0
		iHighestReligion = -1
		for i in range(iNumReligions):
			iLoopReligion = (iProtestantism + i) % iNumReligions
			if lReligions[iLoopReligion] > iMax:
				iMax = lReligions[iLoopReligion]
				iHighestReligion = iLoopReligion
				
		return iHighestReligion

	def createStartingWorkers(self, iPlayer, tPlot):
		iCiv = civ(iPlayer)
	
		if iCiv == iCivChina:
			makeUnit(iPlayer, iWorker, tPlot)
		elif iCiv == iCivIndia:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iCivGreece:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iCivPersia:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivCarthage:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iCivRome:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iCivMaya:
			makeUnit(iPlayer, iWorker, tPlot)
		elif iCiv == iCivJapan:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iCivTamils:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iCivEthiopia:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivKorea:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivByzantium:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivVikings:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivTurks:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivArabia:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivTibet:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iCivKhmer:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivIndonesia:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivMoors:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iCivSpain:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivFrance:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivEngland:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivHolyRome:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivRussia:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivNetherlands:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivMali:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivPoland:
			makeUnits(iPlayer, iWorker, tPlot, 3)
			
			if not player(iPlayer).isHuman():
				iRand = rand(5)
				if iRand == 0: tCityPlot = (65, 55) # Memel
				elif iRand == 1: tCityPlot = (65, 54) # Koenigsberg
				else: tCityPlot = (64, 54) # Gdansk
				
				makeUnit(iPlayer, iSettler, tCityPlot)
				makeUnit(iPlayer, iCrossbowman, tCityPlot)
		elif iCiv == iCivOttomans:
			makeUnits(iPlayer, iWorker, tPlot, 4)
		elif iCiv == iCivPortugal:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivInca:
			makeUnits(iPlayer, iWorker, tPlot, 4)
		elif iCiv == iCivItaly:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivMongols:
			makeUnits(iPlayer, iWorker, tPlot, 4)
		elif iCiv == iCivAztecs:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivMughals:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivThailand:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iCivCongo:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iCivGermany:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCivAmerica:
			makeUnits(iPlayer, iWorker, tPlot, 4)
		elif iCiv == iCivBrazil:
			makeUnits(iPlayer, iMadeireiro, tPlot, 3)
		elif iCiv == iCivArgentina:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iCivCanada:
			makeUnits(iPlayer, iWorker, tPlot, 3)

	def create1700ADstartingUnits(self):

		# Japan
		tCapital = Areas.getCapital(iCivJapan)
		if not player(iCivJapan).isHuman():
			makeUnit(iCivJapan, iSettler, tCapital)
		
		for iPlayer in players.major():
			iCiv = civ(iPlayer)
			if dBirth[iCiv] > scenarioStartYear() and player(iPlayer).isHuman():
				makeUnit(iPlayer, iSettler, Areas.getCapital(iCiv))
				makeUnit(iPlayer, iMilitia, Areas.getCapital(iCiv))

	def create600ADstartingUnits( self ):

		tCapital = Areas.getCapital(iCivChina)
		makeUnits(iCivChina, iSwordsman, tCapital, 2)
		makeUnit(iCivChina, iArcher, tCapital)
		makeUnit(iCivChina, iSpearman, tCapital, UnitAITypes.UNITAI_CITY_DEFENSE)
		makeUnits(iCivChina, iChokonu, tCapital, 2)
		makeUnit(iCivChina, iHorseArcher, tCapital)
		makeUnits(iCivChina, iWorker, tCapital, 2)
		
		tCapital = Areas.getCapital(iCivJapan)
		tSeaPlot = self.findSeaPlots(tCapital, 1, iCivJapan)
		if tSeaPlot:
			makeUnits(iCivJapan, iWorkboat, tSeaPlot, 2)
			
		if not player(iCivJapan).isHuman():
			makeUnits(iCivJapan, iCrossbowman, tCapital, 2)
			makeUnits(iCivJapan, iSamurai, tCapital, 3)

		tCapital = Areas.getCapital(iCivByzantium)
		tSeaPlot = self.findSeaPlots(tCapital, 1, iCivByzantium)
		if tSeaPlot:
			makeUnits(iCivByzantium, iGalley, tSeaPlot, 2)
			makeUnits(iCivByzantium, iWarGalley, tSeaPlot, 2)

		tCapital = Areas.getCapital(iCivVikings)
		tSeaPlot = self.findSeaPlots(tCapital, 1, iCivVikings)
		if tSeaPlot:
			makeUnit(iCivVikings, iWorkboat, tSeaPlot)
			if player(iCivVikings).isHuman():
				makeUnit(iCivVikings, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iCivVikings, iSettler, tSeaPlot)
				makeUnit(iCivVikings, iArcher, tSeaPlot)
				makeUnits(iCivVikings, iLongship, tSeaPlot, 2, UnitAITypes.UNITAI_EXPLORE_SEA)
			else:
				makeUnits(iCivVikings, iLongship, tSeaPlot, 3, UnitAITypes.UNITAI_EXPLORE_SEA)
				
		# start AI settler and garrison in Denmark and Sweden
		if not player(iCivVikings).isHuman():
			makeUnit(iCivVikings, iSettler, (60, 56))
			makeUnit(iCivVikings, iArcher, (60, 56))
			makeUnit(iCivVikings, iSettler, (63, 59))
			makeUnit(iCivVikings, iArcher, (63, 59))
		else:
			makeUnit(iCivVikings, iSettler, tCapital)
			makeUnits(iCivVikings, iArcher, 2)

		tCapital = Areas.getCapital(iCivKorea)
		if not player(iCivKorea).isHuman():
			makeUnits(iCivKorea, iHeavySwordsman, tCapital, 2)
				
		tCapital = Areas.getCapital(iCivTurks)
		makeUnits(iCivTurks, iSettler, tCapital, 2)
		makeUnits(iCivTurks, iOghuz, tCapital, 6)
		makeUnit(iCivTurks, iArcher, tCapital)
		makeUnit(iCivTurks, iScout, tCapital)
			
		for iPlayer in players.major().human().before_birth():
			tCapital = Areas.getCapital(civ(iPlayer))
			makeUnit(iPlayer, iSettler, tCapital)
			makeUnit(iPlayer, iMilitia, tCapital)

	def create4000BCstartingUnits(self):
		for iPlayer in players.major():
			iCiv = civ(iPlayer)
			tCapital = Areas.getCapital(iCiv)
			
			if dBirth[iCiv] > scenarioStartYear() and player(iPlayer).isHuman():
				makeUnit(iPlayer, iSettler, tCapital)
				makeUnit(iPlayer, iMilitia, tCapital)
				
			if iCiv == iCivHarappa and (data.isCivEnabled(iCiv) or player(iPlayer).isHuman()):
				makeUnit(iPlayer, iCityBuilder, tCapital)
				makeUnit(iPlayer, iMilitia, tCapital)

	def assignTechs(self, iPlayer):
		Civilizations.initPlayerTechs(iPlayer)
				
		sta.onCivSpawn(iPlayer)

	def arabianSpawn(self):
		tBaghdad = (77, 40)
		tCairo = (69, 35)
		tMecca = (75, 33)

		bBaghdad = civ(plot(tBaghdad)) == iCivArabia
		bCairo = civ(plot(tCairo)) == iCivArabia
		
		lCities = []
		
		if bBaghdad: lCities.append(tBaghdad)
		if bCairo: lCities.append(tCairo)
		
		tCapital = random_entry(lCities)
		
		if tCapital:
			if not player(iCivArabia).isHuman():
				moveCapital(slot(iCivArabia), tCapital)
				makeUnits(iCivArabia, iMobileGuard, tCapital, 3)
				makeUnits(iCivArabia, iGhazi, tCapital, 2)
			makeUnits(iCivArabia, iMobileGuard, tCapital, 2)
			makeUnits(iCivArabia, iGhazi, tCapital, 2)
		
		if bBaghdad:
			makeUnit(iCivArabia, iSettler, tBaghdad)
			makeUnit(iCivArabia, iWorker, tBaghdad)
		
		if bCairo:
			makeUnit(iCivArabia, iSettler, tCairo)
			makeUnit(iCivArabia, iWorker, tCairo)
			
		if len(lCities) < 2:
			makeUnits(iCivArabia, iSettler, tMecca, 2 - len(lCities))
			makeUnits(iCivArabia, iWorker, tMecca, 2 - len(lCities))

		if not player(iCivArabia).isHuman() and bBaghdad:
			makeUnits(iCivArabia, iSpearman, tBaghdad, 2)

	def germanSpawn(self):
		iPlayer = slot(iCivHolyRome)
	
		if stability(iPlayer) < iStabilityShaky: data.setStabilityLevel(iPlayer, iStabilityShaky)
			
		dc.nameChange(iPlayer)
		dc.adjectiveChange(iPlayer)

	def holyRomanSpawn(self):
		city = city_(60, 56)
		if city and player(iCivVikings).isAlive():
			city.setCulture(slot(iCivVikings), 5, True)

	def determineEnabledPlayers(self):
		iRand = infos.constant('PLAYER_OCCURRENCE_POLYNESIA')
		if iRand <= 0:
			data.setCivEnabled(iCivPolynesia, False)
		elif rand(iRand) != 0:
			data.setCivEnabled(iCivPolynesia, False)
			
		iRand = infos.constant('PLAYER_OCCURRENCE_HARAPPA')
		if iRand <= 0:
			data.setCivEnabled(iCivHarappa, False)
		elif rand(iRand) != 0:
			data.setCivEnabled(iCivHarappa, False)
		
		if not player(iCivIndia).isHuman() and not player(iCivIndonesia).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_TAMILS')
			
			if iRand <= 0:
				data.setCivPlayerEnabled(iCivTamils, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iCivTamils, False)
				
		if not player(iCivChina).isHuman() and not player(iCivIndia).isHuman() and not player(iCivMughals).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_TIBET')
			
			if iRand <= 0:
				data.setCivEnabled(iCivTibet, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iCivTibet, False)
				
		if not player(iCivSpain).isHuman() and not player(iCivMali).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_MOORS')
			
			if iRand <= 0:
				data.setCivEnabled(iCivMoors, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iCivMoors, False)
				
		if not player(iCivHolyRome).isHuman() and not player(iCivGermany).isHuman() and not player(iCivRussia).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_POLAND')
			
			if iRand <= 0:
				data.setCivEnabled(iCivPoland, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iCivPoland, False)
				
		if not player(iCivMali).isHuman() and not player(iCivPortugal).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_CONGO')
			
			if iRand <= 0:
				data.setCivEnabled(iCivCongo, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iCivCongo, False)
				
		if not player(iCivSpain).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_ARGENTINA')
			
			if iRand <= 0:
				data.setCivEnabled(iCivArgentina, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iCivArgentina, False)
				
		if not player(iCivPortugal).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_BRAZIL')
			
			if iRand <= 0:
				data.setCivEnabled(iCivBrazil, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iCivBrazil, False)

	def placeHut(self, tTL, tBR):
		plotList = []
		
		for plot in plots.start(tTL).end(tBR):
			if plot.isFlatlands() or plot.isHills():
				if plot.getFeatureType() != iMud:
					if plot.getOwner() < 0:
						plotList.append(location(plot))
		
		if not plotList:
			return
		
		tPlot = random_entry(plotList)
		plot_(tPlot).setImprovementType(iHut)

	def setStateReligion(self, iPlayer):
		coreCities = cities.of(Areas.getCoreArea(civ(iPlayer)))
		lReligions = [iReligion for iReligion in range(iNumReligions) if iReligion != iJudaism]
		
		def owner_religion(city):
			owner = player(city)
			if city.getOwner() == iPlayer:
				owner = player(city.getPreviousOwner())
				
			if owner: return owner.getStateReligion()
			return -1
		
		iNewStateReligion = find_max(lReligions, lambda iReligion: coreCities.religion(iReligion).count() + coreCities.where(lambda city: owner_religion(city) == iReligion).count()).result
	
		if iNewStateReligion >= 0:
			player(iPlayer).setLastStateReligion(iNewStateReligion)
			
rnf = RiseAndFall()