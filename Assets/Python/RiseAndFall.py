
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
	
	for iMaster in range(iNumPlayers):
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
		
	for iLoopPlayer in range(iNumPlayers):
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
		
		unit, iCost = targetList[iButton]
		closest = closestCity(unit, iByzantium)
		
		newUnit = makeUnit(iByzantium, unit.getUnitType(), closest).first()
		player(iByzantium).changeGold(-iCost)
		unit.kill(False, iByzantium)
		
		if newUnit:
			interface.selectUnit(newUnit, True, True, False)

#######################################
### Main methods (Event-Triggered) ###
#####################################  

	def setup(self):

		self.determineEnabledPlayers()
		
		self.initScenario()
		
		# Leoreth: make sure to select the Egyptian settler
		if pEgypt.isHuman():
			for unit in units.at(Areas.getCapital(iEgypt)):
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
			
			pPersia.setReborn(True)
			
			pChina.updateTradeRoutes()
			
		for iPlayer in [iPlayer for iPlayer in range(iNumPlayers) if tBirth[iPlayer] < scenarioStartYear()]:
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
		for iPlayer in range(iNumPlayers):
			x, y = Areas.getCapital(iPlayer)
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
				plot_(x, y).setOwner(iChina)
		
		for plot in plots.start(tTL).end(tBR).without(lExceptions).including(lAdditions):
			if not plot.isWater(): plot.setWithinGreatWall(True)
			
			
	def adjust1700ADCulture(self):
		for plot in plots.all():
			if plot.getOwner() != -1:
				plot.changeCulture(plot.getOwner(), 100, True)
				convertPlotCulture(plot, plot.getOwner(), 100, True)
					
		for x, y in [(48, 45), (50, 44), (50, 43), (50, 42), (49, 40)]:
			convertPlotCulture(plot_(x, y), iPortugal, 100, True)
			
		for x, y in [(58, 49), (59, 49), (60, 49)]:
			convertPlotCulture(plot_(x, y), iGermany, 100, True)
			
		for x, y in [(62, 51)]:
			convertPlotCulture(plot_(x, y), iHolyRome, 100, True)
			
		for x, y in [(58, 52), (58, 53)]:
			convertPlotCulture(plot_(x, y), iNetherlands, 100, True)
			
		for x, y in [(64, 53), (66, 55)]:
			convertPlotCulture(plot_(x, y), iPoland, 100, True)
			
		for x, y in [(67, 58), (68, 59), (69, 56), (69, 54)]:
			convertPlotCulture(plot_(x, y), iRussia, 100, True)
			
	def prepareColonists(self):
		for iPlayer in [iSpain, iFrance, iEngland, iPortugal, iNetherlands, iGermany, iVikings]:
			data.players[iPlayer].iExplorationTurn = year(1700)
			
		data.players[iVikings].iColonistsAlreadyGiven = 1
		data.players[iSpain].iColonistsAlreadyGiven = 7
		data.players[iFrance].iColonistsAlreadyGiven = 3
		data.players[iEngland].iColonistsAlreadyGiven = 3
		data.players[iPortugal].iColonistsAlreadyGiven = 6
		data.players[iNetherlands].iColonistsAlreadyGiven = 4
		
	def init1700ADDiplomacy(self):
		teamEngland.declareWar(iMughals, False, WarPlanTypes.WARPLAN_LIMITED)
		teamIndia.declareWar(iMughals, False, WarPlanTypes.WARPLAN_TOTAL)
	
	def changeAttitudeExtra(self, iPlayer1, iPlayer2, iValue):
		player(iPlayer1).AI_changeAttitudeExtra(iPlayer2, iValue)
		player(iPlayer2).AI_changeAttitudeExtra(iPlayer1, iValue)

	def invalidateUHVs(self):
		for iPlayer in range(iNumPlayers):
			if not player(iPlayer).isPlayable():
				for i in range(3):
					data.players[iPlayer].lGoals[i] = 0
					
	def foundCapitals(self):
		if scenario() == i600AD:
		
			# China
			self.prepareChina()
			tCapital = Areas.getCapital(iChina)
			lBuildings = [iGranary, iConfucianTemple, iTaixue, iBarracks, iForge]
			foundCapital(iChina, tCapital, "Xi'an", 4, 100, lBuildings, [iConfucianism, iTaoism])
			
		elif scenario() == i1700AD:
			
			# Chengdu
			city(99, 41).setCulture(iChina, 100, True)

	def flipStartingTerritory(self):
	
		if scenario() == i600AD:
			
			# China
			tTL, tBR = Areas.tBirthArea[iChina]
			if not pChina.isHuman(): tTL = (99, 39) # 4 tiles further south
			self.startingFlip(iChina, [(tTL, tBR)])
			
		if scenario() == i1700AD:
		
			# China (Tibet)
			tTibetTL = (94, 42)
			tTibetBR = (97, 45)
			tManchuriaTL = (105, 51)
			tManchuriaBR = (109, 55)
			self.startingFlip(iChina, [(tTibetTL, tTibetBR), (tManchuriaTL, tManchuriaBR)])
			
			# Russia (Sankt Peterburg)
			convertPlotCulture(plot(68, 58), iRussia, 100, True)
			convertPlotCulture(plot(67, 57), iRussia, 100, True)
			
			
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
		for plot in plots.start(tCultureRegionTL).end(tCultureRegionBR):
			bCity = False
			for loopPlot in plots.surrounding(plot):
				if loopPlot.isCity():
					bCity = True
					loopPlot.getPlotCity().setCulture(iIndependent2, 0, False)
			if bCity:
				plot.setCulture(iIndependent2, 1, True)
			else:
				plot.setCulture(iIndependent2, 0, True)
				plot.setOwner(-1)
					
		pIndependent.found(99, 41)
		makeUnit(iIndependent, iArcher, (99, 41))
		pChengdu = city(99, 41)
		pChengdu.setName("Chengdu", False)
		pChengdu.setPopulation(2)
		pChengdu.setHasReligion(iConfucianism, True, False, False)
		pChengdu.setHasRealBuilding(iGranary, True)
		pChengdu.setHasRealBuilding(iDujiangyan, True)
		
		if scenario() == i600AD:
			pBarbarian.found(105, 49)
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
		pBeijing.setBuildingOriginalOwner(iTaoistShrine, iChina)
		pBeijing.setBuildingOriginalOwner(iGreatWall, iChina)
		
		pNanjing = city(105, 43)
		pNanjing.setBuildingOriginalOwner(iConfucianShrine, iChina)
		
		pPataliputra = city(94, 40)
		pPataliputra.setBuildingOriginalOwner(iHinduShrine, iIndia)
		pPataliputra.setBuildingOriginalOwner(iBuddhistShrine, iIndia)
		
		pSirajis = city(82, 38)
		pSirajis.setBuildingOriginalOwner(iZoroastrianShrine, iPersia)
		
		pAlexandria = city(67, 36)
		pAlexandria.setBuildingOriginalOwner(iGreatLighthouse, iEgypt)
		pAlexandria.setBuildingOriginalOwner(iGreatLibrary, iEgypt)
		
		pMemphis = city(69, 35)
		pMemphis.setBuildingOriginalOwner(iPyramids, iEgypt)
		pMemphis.setBuildingOriginalOwner(iGreatSphinx, iEgypt)
		
		pAthens = city(67, 41)
		pAthens.setBuildingOriginalOwner(iParthenon, iGreece)
		
		pRome = city(60, 44)
		pRome.setBuildingOriginalOwner(iFlavianAmphitheatre, iRome)
		
		pChichenItza = city(23, 37)
		pChichenItza.setBuildingOriginalOwner(iTempleOfKukulkan, iMaya)
		
	def adjust1700ADWonders(self):
		lExpiredWonders = [iOracle, iIshtarGate, iHangingGardens, iGreatCothon, iApadanaPalace, iColossus, iStatueOfZeus, iGreatMausoleum, iTempleOfArtemis, iAquaAppia, iAlKhazneh, iJetavanaramaya, iGreatLighthouse, iMoaiStatues, iFlavianAmphitheatre, iGreatLibrary, iGondeshapur, iSilverTreeFountain, iAlamut]
		self.expireWonders(lExpiredWonders)
	
		pMilan = city(59, 47)
		pMilan.setBuildingOriginalOwner(iSantaMariaDelFiore, iItaly)
		pMilan.setBuildingOriginalOwner(iSanMarcoBasilica, iItaly)
		
		pDjenne = city(51, 30)
		pDjenne.setBuildingOriginalOwner(iUniversityOfSankore, iMali)
		
		pJerusalem = city(73, 38)
		pJerusalem.setBuildingOriginalOwner(iJewishShrine, iIndependent)
		pJerusalem.setBuildingOriginalOwner(iOrthodoxShrine, iByzantium)
		pJerusalem.setBuildingOriginalOwner(iDomeOfTheRock, iArabia)
		
		pBaghdad = city(77, 40)
		pBaghdad.setBuildingOriginalOwner(iSpiralMinaret, iArabia)
		
		pRome = city(60, 44)
		pRome.setBuildingOriginalOwner(iFlavianAmphitheatre, iRome)
		pRome.setBuildingOriginalOwner(iSistineChapel, iItaly)
		
		pSeville = city(51, 41)
		pSeville.setBuildingOriginalOwner(iMezquita, iMoors)
		
		pBangkok = city(101, 33)
		pBangkok.setBuildingOriginalOwner(iWatPreahPisnulok, iKhmer)
		
		pChichenItza = city(23, 37)
		pChichenItza.setBuildingOriginalOwner(iTempleOfKukulkan, iMaya)
		
		pConstantinople = city(68, 45)
		pConstantinople.setBuildingOriginalOwner(iTheodosianWalls, iByzantium)
		pConstantinople.setBuildingOriginalOwner(iHagiaSophia, iByzantium)
		
		pJakarta = city(104, 25)
		pJakarta.setBuildingOriginalOwner(iBorobudur, iIndonesia)
		
		pMexicoCity = city(18, 37)
		pMexicoCity.setBuildingOriginalOwner(iFloatingGardens, iAztecs)
		
		pCairo = city(69, 35)
		pCairo.setBuildingOriginalOwner(iPyramids, iEgypt)
		pCairo.setBuildingOriginalOwner(iGreatSphinx, iEgypt)
		
		pAthens = city(67, 41)
		pAthens.setBuildingOriginalOwner(iParthenon, iGreece)
		
		pShiraz = city(82, 38)
		pShiraz.setBuildingOriginalOwner(iZoroastrianShrine, iPersia)
		
		pPataliputra = city(94, 40)
		pPataliputra.setBuildingOriginalOwner(iHinduShrine, iIndia)
		pPataliputra.setBuildingOriginalOwner(iBuddhistShrine, iIndia)
		
		pMecca = city(75, 33)
		pMecca.setBuildingOriginalOwner(iIslamicShrine, iArabia)
		
	def expireWonders(self, lWonders):
		for iWonder in lWonders:
			game.incrementBuildingClassCreatedCount(infos.building(iWonder).getBuildingClassType())
			
	def adjust600ADGreatPeople(self):
		dGreatPeopleCreated = {
			iChina: 4,
			iKorea: 1,
			iByzantium: 1,
			iJapan: 0,
			iVikings: 0,
			iTurks: 0,
		}
		
		dGreatGeneralsCreated = {
			iChina: 1,
			iKorea: 0,
			iByzantium: 0,
			iJapan: 0,
			iVikings: 0,
			iTurks: 0,
		}
		
		for iPlayer, iGreatPeople in dGreatPeopleCreated.iteritems():
			player(iPlayer).changeGreatPeopleCreated(iGreatPeople)
			
		for iPlayer, iGreatGenerals in dGreatGeneralsCreated.iteritems():
			player(iPlayer).changeGreatGeneralsCreated(iGreatGenerals)
		
	def adjust1700ADGreatPeople(self):
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
		
		for iPlayer, iGreatPeople in dGreatPeopleCreated.iteritems():
			player(iPlayer).changeGreatPeopleCreated(iGreatPeople)
			
		for iPlayer, iGreatGenerals in dGreatGeneralsCreated.iteritems():
			player(iPlayer).changeGreatGeneralsCreated(iGreatGenerals)
						
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
		
		if iGameTurn == year(tBirth[iSpain])-1:
			if scenario() == i600AD:
				pMassilia = city_(56, 46)
				if pMassilia:
					pMassilia.setCulture(pMassilia.getOwner(), 1, True)

		# Leoreth: Turkey immediately flips independent cities in its core to avoid being pushed out of Anatolia
		if iGameTurn == data.iOttomanSpawnTurn + 1:
			cityPlotList = cities.of(Areas.getBirthArea(iOttomans))
			for city in cityPlotList:
				tPlot = (city.getX(), city.getY())
				iOwner = city.getOwner()
				if iOwner in [iBarbarian, iIndependent, iIndependent2]:
					flipCity(tPlot, False, True, iOttomans, ())
					cultureManager(tPlot, 100, iOttomans, iOwner, True, False, False)
					self.convertSurroundingPlotCulture(iOttomans, plots.surrounding(tPlot))
					makeUnit(iOttoman, iCrossbowman, tPlot)
					
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

		if iGameTurn % turns(20) == 0:
			if pIndependent.isAlive():
				updateMinorTechs(iIndependent, iBarbarian)
			if pIndependent2.isAlive():
				updateMinorTechs(iIndependent2, iBarbarian)

		#Leoreth: give Phoenicia a settler in Qart-Hadasht in 820BC
		if not pPhoenicia.isHuman() and year() == year(-820) - (data.iSeed % 10):
			makeUnit(iCarthage, iSettler, (58, 39))
			makeUnits(iCarthage, iArcher, (58, 39), 2)
			makeUnits(iCarthage, iWorker, (58, 39), 2)
			makeUnits(iCarthage, iWarElephant, (58, 39), 2)
			
		if year() == year(476):
			if pItaly.isHuman() and pRome.isAlive():
				sta.completeCollapse(iRome)
				
		if year() == year(-50):
			if pByzantium.isHuman() and pGreece.isAlive():
				sta.completeCollapse(iGreece)
				
		if year() == year(tBirth[iIndia])-turns(1):
			if pHarappa.isAlive() and not pHarappa.isHuman():
				sta.completeCollapse(iHarappa)
			
		#Colonists
		if year() == year(-850):
			self.giveEarlyColonists(iGreece)
		elif year() == year(-700): # removed their colonists because of the Qart-Hadasht spawn
			self.giveEarlyColonists(iCarthage)
			
		elif year() == year(-600):
			self.giveEarlyColonists(iRome)
		elif year() == year(-400):
			self.giveEarlyColonists(iRome)

		if year().between(860, 1250):
			if turn() % turns(10) == 9:
				self.giveRaiders(iVikings, Areas.getBroaderArea(iVikings))
		
		if year().between(1350, 1918):
			for iPlayer in [iSpain, iEngland, iFrance, iPortugal, iNetherlands, iVikings, iGermany]:
				if turn() == data.players[iPlayer].iExplorationTurn + 1 + data.players[iPlayer].iColonistsAlreadyGiven * 8:
					self.giveColonists(iPlayer)
					
		if year() == year(710)-1:
			marrakesh = city_(51, 37)
			if marrakesh:
				marrakesh.setHasReligion(iIslam, True, False, False)
				
				makeUnit(marrakesh.getOwner(), iSettler, marrakesh)
				makeUnit(marrakesh.getOwner(), iWorker, marrakesh)
				
		# Leoreth: help human with Aztec UHV - prevent super London getting in the way
		if year() == year(1500) and pAztecs.isHuman():
			plot = plot_(Areas.getCapital(iEngland))
			if plot.isCity():
				city = plot.getPlotCity()
				if city.getPopulation() > 14:
					city.changePopulation(-3)
				
		# Leoreth: make sure Aztecs are dead in 1700 if a civ that spawns from that point is selected
		if year() == year(1700)-2:
			if human() >= iGermany and pAztecs.isAlive():
				sta.completeCollapse(iAztecs)
				#killAndFragmentCiv(iAztecs, iIndependent, iIndependent2, -1, False)
				
				
		for iLoopCiv in [iPlayer for iPlayer in range(iNumMajorPlayers) if tBirth[iPlayer] > scenarioStartYear()]:
			if year() >= year(tBirth[iLoopCiv]) - 2 and year() <= year(tBirth[iLoopCiv]) + 6:
				self.initBirth(tBirth[iLoopCiv], iLoopCiv)



		if year() == year(600):
			if scenario() == i600AD:  #late start condition
				tTL, tBR = Areas.tBirthArea[iChina]
				if not pChina.isHuman(): tTL = (99, 39) # 4 tiles further north
				china = plots.start(tTL).end(tBR)
				iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iChina, china)
				self.convertSurroundingPlotCulture(iChina, china)
				flipUnitsInArea(china, iChina, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ   
				flipUnitsInArea(china, iChina, iIndependent, False, False) #remaining independents in the region now belong to the new civ   
				flipUnitsInArea(china, iChina, iIndependent2, False, False) #remaining independents in the region now belong to the new civ

				
		#kill the remaining barbs in the region: it's necessary to do this more than once to protect those civs
		for iPlayer in [iVikings, iSpain, iFrance, iHolyRome, iRussia, iAztecs]:
			if year() >= year(tBirth[iPlayer])+2 and year() <= year(tBirth[iPlayer])+turns(10):
				killUnitsInArea(iBarbarian, Areas.getBirthArea(iPlayer))
				
		#fragment utility
		if year() >= year(50) and turn() % turns(15) == 6:
			self.fragmentIndependents()

		if turn() % turns(10) == 5:
			sta.checkResurrection()
			
		# Leoreth: check for scripted rebirths
		for iPlayer, iYear in dRebirth.items():
			if year() == year(iYear) and not player(iPlayer).isAlive():
				self.rebirthFirstTurn(iPlayer)
			
			if year() == year(iYear)+1 and player(iPlayer).isAlive() and player(iPlayer).isReborn():
				self.rebirthSecondTurn(iPlayer)
					
	def endTurn(self, iPlayer):
		for tTimedConquest in data.lTimedConquests:
			iConqueror, tPlot = tTimedConquest
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
		
		if iPlayer in dRebirthCiv:
			pPlayer.setCivilizationType(dRebirthCiv[iPlayer])
			iCiv = civ(iPlayer)
			
		Modifiers.updateModifiers(iPlayer)
		x, y = Areas.dRebirthPlot[iPlayer]
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
		if iPlayer in rebirthLeaders:
			if pPlayer.getLeader() != rebirthLeaders[iPlayer]:
				pPlayer.setLeader(rebirthLeaders[iPlayer])

		message(human(), 'TXT_KEY_INDEPENDENCE_TEXT', adjective(iPlayer), color=iGreen)
		setReborn(iPlayer, True)
		
		# Determine whether capital location is free
		bFree = isFree(iPlayer, (x, y), True) and not plot.isUnit()

		# if city present, flip it. If plot is free, found it. Else give settler.
		if city:
			completeCityFlip((x, y), iPlayer, city.getOwner(), 100)
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
		if year() >= year(tBirth[human()]):
			startNewCivSwitchEvent(iPlayer)

		player(iPlayer).setLatestRebellionTurn(year(dRebirth[iPlayer]))

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
	
		lRebirthPlots = Areas.getRebirthArea(iPlayer)
		
		# exclude American territory for Mexico
		if iCiv == iCivMexico:
			removedPlots = plots.of(lRebirthPlots).owner(slot(iCivAmerica)).where(lambda p: location(p) not in Areas.getCoreArea(iPlayer))
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
		if pIndependent.getNumCities() > 8 or pIndependent2.getNumCities() > 8:
			iBigIndependent = -1
			iSmallIndependent = -1
			if pIndependent.getNumCities() > 2*pIndependent2.getNumCities():
				iBigIndependent = iIndependent
				iSmallIndependent = iIndependent2
			if pIndependent.getNumCities() < 2*pIndependent2.getNumCities():
				iBigIndependent = iIndependent2
				iSmallIndependent = iIndependent
			if iBigIndependent != -1:
				iDivideCounter = 0
				iCounter = 0
				for city in cities.owner(iBigIndependent):
					iDivideCounter += 1 #convert 3 random cities cycling just once
					if iDivideCounter % 2 == 1:
						tPlot = (city.getX(), city.getY())
						cultureManager(tPlot, 50, iSmallIndependent, iBigIndependent, False, True, True)
						flipUnitsInCityBefore(tPlot, iSmallIndependent, iBigIndependent)
						flipCity(tPlot, 0, 0, iSmallIndependent, [iBigIndependent])   #by trade because by conquest may raze the city
						flipUnitsInCityAfter(tPlot, iSmallIndependent)
						iCounter += 1
						if iCounter == 3:
							return



	def fragmentBarbarians(self, iGameTurn):
		for iDeadCiv in players.major().shuffle():
			if not player(iDeadCiv).isAlive() and iGameTurn > year(tBirth[iDeadCiv]) + turns(50):
				pDeadCiv = player(iDeadCiv)
				teamDeadCiv = team(iDeadCiv)
				iCityCounter = 0
				
				for (x, y) in Areas.getNormalArea(iDeadCiv):
					city = city_(x, y)
					if city and city.getOwner() == iBarbarian:
						iCityCounter += 1
							
				if iCityCounter > 3:
					iDivideCounter = 0
					for (x, y) in Areas.getNormalArea(iDeadCiv):
						city = city_(x, y)
						if city and city.getOwner() == iBarbarian:
							if iDivideCounter % 4 == 0:
								iNewCiv = iIndependent
							elif iDivideCounter % 4 == 1:
								iNewCiv = iIndependent2
							if iDivideCounter % 4 == 0 or iDivideCounter % 4 == 1:
								cultureManager(location(city), 50, iNewCiv, iBarbarian, False, True, True)
								flipUnitsInCityBefore(location(city), iNewCiv, iBarbarian)
								flipCity(location(city), 0, 0, iNewCiv, [iBarbarian])   #by trade because by conquest may raze the city
								flipUnitsInCityAfter(location(city), iNewCiv)
								iDivideCounter += 1
					return


	def secession(self, iGameTurn):
		for iPlayer in players.major().shuffle():
			if player(iPlayer).isAlive() and iGameTurn >= year(tBirth[iPlayer]) + turns(30):
				
				if stability(iPlayer) == iStabilityCollapsing:

					cityList = []
					for city in cities.owner(iPlayer):
						pPlot = plot(city)

						if not city.isWeLoveTheKingDay() and not city.isCapital() and location(city) != Areas.getCapital(iPlayer):
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
									
									for iLoop in range(iNumTotalPlayers+1):
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
								iNewCiv = iNative
						
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
			if iCiv == iByzantium:
				if not player(slot(iCivRome)).isAlive() or player(slot(iCivGreece)).isAlive() or (player(slot(iCivRome)).isHuman() and stability(slot(iCivRome)) == iStabilitySolid):
					return
					
			elif iCiv == iCivOttomans:
				tMiddleEastTL = (69, 38)
				tMiddleEastBR = (78, 45)
				if cities.start(tMiddleEastTL).end(tMiddleEastBR).any(lambda city: slot(iCivTurks) in [city.getOwner(), city.getPreviousOwner()]):
					return

			elif iCiv == iCivThailand:
				if not player(slot(iCivKhmer)).isHuman():
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
				if player(slot(iCivRome)).isAlive():
					return
				
				cityList = getCitiesInCore(slot(iCivRome), False)
				
				iIndependentCities = 0

				for pCity in cityList:
					if not pCity.getOwner() < iNumPlayers:
						iIndependentCities += 1
						
				if iIndependentCities == 0:
					return
		
		periods.onBirth(iPlayer)
				
		tCapital = Areas.getCapital(iPlayer)
				
		x, y = tCapital
		bCapitalSettled = False
		
		if iCiv == iCivItaly:
			for plot in plots.surrounding(tCapital):
				if plot.isCity():
					bCapitalSettled = True
					tCapital = location(plot)
					x, y = tCapital
					break

		if turn() == iBirthYear-1 + data.players[iPlayer].iSpawnDelay + data.players[iPlayer].iFlipsDelay:
			if iCiv in lConditionalCivs or bCapitalSettled:
				convertPlotCulture(plot_(x, y), iPlayer, 100, True)

			tTopLeft, tBottomRight = Areas.getBirthRectangle(iPlayer)
			tBroaderTopLeft, tBroaderBottomRight = Areas.tBroaderArea[iPlayer]
			
			if iCiv == iCivThailand:
				angkor = city(Areas.tCapitals[slot(iKhmer)])
				if angkor:
					bWonder = any(angkor.isHasRealBuilding(iBuilding) for iBuilding in range(iBeginWonders, iNumBuildings))
					if bWonder and not pPlayer.isHuman():
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
						for iLoopPlayer in players.withBarbarian():
							if iPlayer != iLoopPlayer:
								flipUnitsInArea(plots.start(tTopLeft).end(tBottomRight).without(Areas.dBirthAreaExceptions[iPlayer]), iPlayer, iLoopPlayer, True, False)
						if pCurrent.isCity():
							pCurrent.eraseAIDevelopment()
						for iLoopPlayer in players.withBarbarian():
							if iPlayer != iLoopPlayer:
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
		for x, y in Areas.getNormalArea(iPlayer):
			plot_(x, y).setRevealed(iPlayer, True, True, 0)
				
		# Leoreth: conditional state religion for colonial civs and Byzantium
		if iCiv in [iCivByzantium, iCivArgentina, iCivBrazil]:
			self.setStateReligion(iPlayer)
			
		if canSwitch(iPlayer, iBirthYear):
			startNewCivSwitchEvent(iPlayer)
			
		data.players[iPlayer].bSpawned = True

	def moveOutInvaders(self, tTL, tBR):
		if pMongolia.isAlive():
			mongolCapital = pMongolia.getCapitalCity()
		for plot in plots.start(tTL).end(tBR):
			for unit in units.at(plot):
				if not isDefenderUnit(unit):
					if unit.getOwner() == iMongolia:
						if not pMongolia.isHuman():
							move(unit, mongolCapital)
					else:
						if unit.getUnitType() == iKeshik:
							unit.kill(False, iBarbarian)

	def deleteMode(self, iCurrentPlayer):
		iPlayer = data.lDeleteMode[0]
		iCiv = civ(iPlayer)
		
		print ("deleteMode after", iCurrentPlayer)
		tCapital = Areas.getCapital(iPlayer)
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
				for iLoopPlayer in players.withBarbarian().without(iPlayer):
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
					
					rome = city(Areas.getCapital(slot(iRome)))
					if rome:
						cityList.append(rome)
					
					for city in cityList:
						if city.getPopulation() < 5: city.setPopulation(5)
						city.setHasRealBuilding(iGranary, True)
						city.setHasRealBuilding(iLibrary, True)
						city.setHasRealBuilding(iCourthouse, True)
						if city.isCoastal(20): city.setHasRealBuilding(iHarbor, True)
				
				lPlots = plots.surrounding(tCapital, radius=3)
				flipUnitsInArea(lPlots, iPlayer, iBarbarian, True, True) #This is mostly for the AI. During Human player spawn, that area should be already cleaned			
				flipUnitsInArea(lPlots, iPlayer, iIndependent, True, False) #This is mostly for the AI. During Human player spawn, that area should be already cleaned			
				flipUnitsInArea(lPlots, iPlayer, iIndependent2, True, False) #This is mostly for the AI. During Human player spawn, that area should be already cleaned			
				self.assignTechs(iPlayer)
				data.players[iPlayer].iPlagueCountdown = -iImmunity
				clearPlague(iPlayer)
				data.players[iPlayer].iFlipsDelay = iFlipsDelay #save
				

		else: #starting units have already been placed, now the second part
		
			iNumCities = player(iPlayer).getNumCities()
		
			area = plots.start(tTopLeft).end(tBottomRight).without(Areas.getBirthExceptions(iPlayer))
			iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iPlayer, area)
			self.convertSurroundingPlotCulture(iPlayer, area)
			flipUnitsInArea(area, iPlayer, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ
			flipUnitsInArea(area, iPlayer, iIndependent, False, False) #remaining independents in the region now belong to the new civ   
			flipUnitsInArea(area, iPlayer, iIndependent2, False, False) #remaining independents in the region now belong to the new civ# starting workers
		
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
			
			rome = city(Areas.getCapital(slot(iCivRome)))
			if rome:
				cityList.append(rome)
				
			for pCity in cityList:
				if city.getPopulation() < 5: city.setPopulation(5)
				city.setHasRealBuilding(iGranary, True)
				city.setHasRealBuilding(iLibrary, True)
				city.setHasRealBuilding(iCourthouse, True)
				if city.isCoastal(20): city.setHasRealBuilding(iHarbor, True)
				
		iNumCities = player(iPlayer).getNumCities()
		
		area = plots.start(tTopLeft).end(tBottomRight).without(Areas.getBirthExceptions(iPlayer))
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
			flipUnitsInArea(lPlots, iPlayer, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ 
			flipUnitsInArea(lPlots, iPlayer, iIndependent, False, False) #remaining barbs in the region now belong to the new civ 
			flipUnitsInArea(lPlots, iPlayer, iIndependent2, False, False) #remaining barbs in the region now belong to the new civ
			
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
			flipUnitsInArea(lPlots, iPlayer, slot(iCivBarbarian), True, True) #remaining barbs in the region now belong to the new civ 
			flipUnitsInArea(lPlots, iPlayer, slot(iCivIndependent), True, False) #remaining barbs in the region now belong to the new civ 
			flipUnitsInArea(lPlots, iPlayer, slot(iCivIndependent2), True, False) #remaining barbs in the region now belong to the new civ 

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
				flipUnitsInArea(area, iPlayer, slot(iCivBarbarian), True, True) #remaining barbs in the region now belong to the new civ 
				flipUnitsInArea(area, iPlayer, slot(iCivIndependent), True, False) #remaining barbs in the region now belong to the new civ 
				flipUnitsInArea(area, iPlayer, slot(iCivIndependent2), True, False) #remaining barbs in the region now belong to the new civ 
				
				self.assignTechs(iPlayer)
				
				data.players[iPlayer].iFlipsDelay = iFlipsDelay #save

				# kill the catapult and cover the plots
				clearCatapult(iPlayer)
				
				convertPlotCulture(plot_(x, y), iPlayer, 100, True)
				
				# notify dynamic names
				dc.onCityAcquired(iPlayer, iOwner)
				
				self.createStartingWorkers(iPlayer, tCapital)

		else: # starting units have already been placed, now to the second part
			area = plots.start(tTopLeft).end(tBottomRight).without(Areas.getBirthExceptions(iPlayer))
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
		lCities = []
		
		for city in cities.of(lPlots):
			if city.plot().isCore(city.getOwner()) and not city.plot().isCore(iPlayer): continue
			
			if city.getOwner() != iPlayer:
				lCities.append(city)
			
		# Leoreth: Byzantium also flips Roman cities in the eastern half of the empire outside of its core (Egypt, Mesopotamia)
		if iPlayer == iByzantium and pRome.isAlive():
			x, y = Areas.getCapital(iByzantium)
			for city in cities.owner(iRome):
				if city.getX() >= x-1 and city.getY() <= y:
					if (city.getX(), city.getY()) not in lPlots:
						lCities.append(city)
					
		# Leoreth: Canada also flips English/American/French cities in the Canada region
		if iPlayer == iCanada:
			for city in cities.owner(iFrance) + cities.owner(iEngland) + cities.owner(iAmerica):
				if city.getRegionID() == rCanada and city.getX() < Areas.getCapital(iCanada)[0] and location(city) not in [location(c) for c in lCities]:
					lCities.append(city)
					
		# Leoreth: remove capital locations
		for city in lCities:
			if city.getOwner() < iNumPlayers:
				if (city.getX(), city.getY()) == Areas.getCapital(city.getOwner()) and city.isCapital():
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
			if iOwner in [iBarbarian, iIndependent, iIndependent2, iCeltia, iNative]:
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
		if iPlayer == iCanada: return
		elif iPlayer == iGermany and not player(iPlayer).isHuman(): return
		
		if year() <= year(tBirth[iPlayer]) + 5:
			for iEnemy in lEnemies:
				tEnemy = team(iEnemy)
				
				if tEnemy.isAtWar(iPlayer): continue
				if iPlayer == iByzantium and iEnemy == iRome: continue
			
				iRand = rand(100)
				if iRand >= tAIStopBirthThreshold[iEnemy]:
					tEnemy.declareWar(iPlayer, True, WarPlanTypes.WARPLAN_ATTACKED_RECENT)
					self.spawnAdditionalUnits(iPlayer)
					
	def spawnAdditionalUnits(self, iPlayer):
		tPlot = Areas.getCapital(iPlayer)
		self.createAdditionalUnits(iPlayer, tPlot)

	def convertSurroundingPlotCulture(self, iCiv, plots):
		for pPlot in plots:
			if pPlot.isOwned() and pPlot.isCore(pPlot.getOwner()) and not pPlot.isCore(iCiv): continue
			pPlot.resetCultureConversion()
			if not pPlot.isCity():
				convertPlotCulture(pPlot, iCiv, 100, False)

	def findSeaPlots(self, tCoords, iRange, iPlayer):
		"""Searches a sea plot that isn't occupied by a unit and isn't a civ's territory surrounding the starting coordinates"""
		seaPlotList = [] 
		for plot in plots.surrounding(tCoords, radius=iRange):
			if plot.isWater():
				if not plot.isUnit():
					if not (plot.isOwned() and plot.getOwner() != iPlayer):
						seaPlotList.append(location(plot))
						# this is a good plot, so paint it and continue search
		if seaPlotList:
			return random_entry(seaPlotList)
		return (None)


	def giveRaiders(self, iPlayer, lPlots):
		pPlayer = player(iPlayer)
		pTeam = team(iPlayer)
		
		if pPlayer.isAlive() and not pPlayer.isHuman():
			cityList = []
			
			#collect all the coastal cities belonging to iPlayer in the area
			for x, y in lPlots:
				city = city_(x, y)
				if city and city.getOwner() == iPlayer and city.isCoastal(10):
					cityList.append(city)

			if cityList:
				city = random_entry(cityList)
				if city:
					tCityPlot = (city.getX(), city.getY())
					tPlot = self.findSeaPlots(tCityPlot, 1, iPlayer)
					if tPlot:
						makeUnit(iPlayer, unique_unit(iPlayer, iGalley), tPlot, UnitAITypes.UNITAI_ASSAULT_SEA)
						if pTeam.isHasTech(iSteel):
							makeUnit(iPlayer, unique_unit(iPlayer, iHeavySwordsman), tPlot, UnitAITypes.UNITAI_ATTACK)
							makeUnit(iPlayer, unique_unit(iPlayer, iHeavySwordsman), tPlot, UnitAITypes.UNITAI_ATTACK_CITY)
						else:
							makeUnit(iPlayer, unique_unit(iPlayer, iSwordsman), tPlot, UnitAITypes.UNITAI_ATTACK)
							makeUnit(iPlayer, unique_unit(iPlayer, iSwordsman), tPlot, UnitAITypes.UNITAI_ATTACK_CITY)

	def giveEarlyColonists(self, iPlayer):
		pPlayer = player(iPlayer)
		iCiv = civ(iPlayer)
		
		if pPlayer.isAlive() and not pPlayer.isHuman():
			capital = pPlayer.getCapitalCity()

			if iCiv == iCivRome:
				capital = cities.owner(iPlayer).region(rIberia).random()
				
			if capital:
				tSeaPlot = self.findSeaPlots(capital, 1, iPlayer)
				if tSeaPlot:
					makeUnit(iPlayer, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
					makeUnit(iPlayer, iSettler, tSeaPlot)
					makeUnit(iPlayer, iArcher, tSeaPlot)

	def giveColonists(self, iPlayer):
		pPlayer = player(iPlayer)
		pTeam = team(iPlayer)
		iCiv = civ(iPlayer)
		
		if pPlayer.isAlive() and not pPlayer.isHuman() and iCiv in dMaxColonists:
			if pTeam.isHasTech(iExploration) and data.players[iPlayer].iColonistsAlreadyGiven < dMaxColonists[iCiv]:
				sourceCities = cities.of(Areas.getCoreArea(iPlayer)).owner(iPlayer)
				
				# help England with settling Canada and Australia
				if iCiv == iCivEngland:
					colonialCities = cities.start(tCanadaTL).end(tCanadaBR).owner(iPlayer)
					colonialCities += cities.start(tAustraliaTL).end(tAustraliaBR).owner(iPlayer)
					
					if colonialCities:
						sourceCities = colonialCities
						
				city = sourceCities.where(lambda city: city.isCoastal(10)).random()
				if city:
					tSeaPlot = self.findSeaPlots(city, 1, iPlayer)
					if not tSeaPlot: tSeaPlot = city
					
					makeUnit(iPlayer, unique_unit(iPlayer, iGalleon), tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
					makeUnit(iPlayer, iSettler, tSeaPlot, UnitAITypes.UNITAI_SETTLE)
					makeUnit(iPlayer, getBestDefender(iPlayer), tSeaPlot)
					makeUnit(iPlayer, iWorker, tSeaPlot)
					
					data.players[iPlayer].iColonistsAlreadyGiven += 1
					

	def onFirstContact(self, iTeamX, iHasMetTeamY):
		if iHasMetTeamY >= iNumPlayers: return
		
		if year().between(600, 1800):
			if iTeamX in lCivBioNewWorld and iHasMetTeamY in lCivBioOldWorld:
				iNewWorldCiv = iTeamX
				iOldWorldCiv = iHasMetTeamY
				
				iIndex = lCivBioNewWorld.index(iNewWorldCiv)
				
				bAlreadyContacted = data.lFirstContactConquerors[iIndex]
				
				# avoid "return later" exploit
				if year <= year(tBirth[iAztecs]) + turns(10):
					data.lFirstContactConquerors[iIndex] = True
					return
					
				if not bAlreadyContacted:
					if iNewWorldCiv == iMaya:
						tContactZoneTL = (15, 30)
						tContactZoneBR = (34, 42)
					elif iNewWorldCiv == iAztecs:
						tContactZoneTL = (11, 31)
						tContactZoneBR = (34, 43)
					elif iNewWorldCiv == iInca:
						tContactZoneTL = (21, 11)
						tContactZoneBR = (36, 40)
						
					lArrivalExceptions = [(25, 32), (26, 40), (25, 42), (23, 42), (21, 42)]
						
					data.lFirstContactConquerors[iIndex] = True
					
					# change some terrain to end isolation
					if iNewWorldCiv == iInca:
						plot(27, 30).setFeatureType(-1, 0)
						plot(28, 31).setFeatureType(-1, 0)
						plot(29, 23).setPlotType(PlotTypes.PLOT_HILLS, True, True)
						plot(31, 13).setPlotType(PlotTypes.PLOT_HILLS, True, True) 
						plot(32, 19).setPlotType(PlotTypes.PLOT_HILLS, True, True)
						plot(27, 29).setPlotType(PlotTypes.PLOT_HILLS, True, True) #Bogota
						
					elif iNewWorldCiv == iAztecs:
						plot(40, 66).setPlotType(PlotTypes.PLOT_HILLS, True, True)
						
					newWorldPlots = plots.start(tContactZoneTL).end(tContactZoneBR).without(lArrivalExceptions)
					contactPlots = newWorldPlots.where(lambda p: p.isVisible(iNewWorldCiv, False) and p.isVisible(iOldWorldCiv, False))
					arrivalPlots = newWorldPlots.owner(iNewWorldCiv).where(lambda p: not p.isCity() and isFree(iOldWorldCiv, p, bCanEnter=True) and not isIsland(p))
					
					if contactPlots and arrivalPlots:
						contactPlot = contactPlots.random()
						arrivalPlot = arrivalPlots.closest(contactPlot)
						
						iModifier1 = 0
						iModifier2 = 0
						
						if player(iNewWorldCiv).isHuman() and player(iNewWorldCiv).getNumCities() > 6:
							iModifier1 = 1
						else:
							if iNewWorldCiv == iInca or player(iNewWorldCiv).getNumCities() > 4:
								iModifier1 = 1
							if not player(iOldWorldCiv).isHuman():
								iModifier2 = 1
								
						if year() < year(tBirth[human()]):
							iModifier1 += 1
							iModifier2 += 1
							
						team(iOldWorldCiv).declareWar(iNewWorldCiv, True, WarPlanTypes.WARPLAN_TOTAL)
						
						iInfantry = getBestInfantry(iOldWorldCiv)
						iCounter = getBestCounter(iOldWorldCiv)
						iCavalry = getBestCavalry(iOldWorldCiv)
						iSiege = getBestSiege(iOldWorldCiv)
						
						iStateReligion = player(iOldWorldCiv).getStateReligion()
						iMissionary = missionary(iStateReligion)
						
						if iInfantry:
							makeUnits(iOldWorldCiv, iInfantry, arrivalPlot, 1 + iModifier2, UnitAITypes.UNITAI_ATTACK_CITY)
						
						if iCounter:
							makeUnits(iOldWorldCiv, iCounter, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
							
						if iSiege:
							makeUnits(iOldWorldCiv, iSiege, arrivalPlot, 1 + iModifier1 + iModifier2, UnitAITypes.UNITAI_ATTACK_CITY)
							
						if iCavalry:
							makeUnits(iOldWorldCiv, iCavalry, arrivalPlot, 2 + iModifier1, UnitAITypes.UNITAI_ATTACK_CITY)
							
						if iMissionary:
							makeUnit(iOldWorldCiv, iMissionary, arrivalPlot)
							
						if iNewWorldCiv == iInca:
							makeUnits(iOldWorldCiv, iAucac, arrivalPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
						elif iNewWorldCiv == iAztecs:
							makeUnits(iOldWorldCiv, iJaguar, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
							makeUnit(iOldWorldCiv, iHolkan, arrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY)
						elif iNewWorldCiv == iMaya:
							makeUnits(iOldWorldCiv, iHolkan, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
							makeUnit(iOldWorldCiv, iJaguar, arrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY)
							
						message(iNewWorldCiv, 'TXT_KEY_FIRST_CONTACT_NEWWORLD')
						message(iOldWorldCiv, 'TXT_KEY_FIRST_CONTACT_OLDWORLD')
							
		# Leoreth: Mongol horde event against Mughals, Persia, Arabia, Byzantium, Russia
		if iHasMetTeamY == iMongolia and not pMongolia.isHuman():
			if iTeamX in [iPersia, iByzantium, iRussia]:
				if year() < year(1500) and data.isFirstContactMongols(iTeamX):

					data.setFirstContactMongols(iTeamX, False)
		
					teamTarget = team(iTeamX)
						
					if iTeamX == iArabia:
						tTL = (73, 31)
						tBR = (84, 43)
						iDirection = DirectionTypes.DIRECTION_EAST
					elif iTeamX == iPersia:
						tTL = (73, 37)
						tBR = (86, 48)
						iDirection = DirectionTypes.DIRECTION_NORTH
					elif iTeamX == iByzantium:
						tTL = (68, 41)
						tBR = (77, 46)
						iDirection = DirectionTypes.DIRECTION_EAST
					elif iTeamX == iRussia:
						tTL = (68, 48)
						tBR = (81, 62)
						iDirection = DirectionTypes.DIRECTION_EAST

					lTargetList = getBorderPlots(iTeamX, tTL, tBR, iDirection, 3)
					
					if not lTargetList: return

					teamMongolia.declareWar(iTeamX, True, WarPlanTypes.WARPLAN_TOTAL)
					
					iHandicap = 0
					if teamtype(iTeamX).isHuman():
						iHandicap = game.getHandicapType() / 2

					for tPlot in lTargetList:
						makeUnits(iMongolia, iKeshik, tPlot, 2 + iHandicap, UnitAITypes.UNITAI_ATTACK_CITY)
						makeUnits(iMongolia, iMangudai, tPlot, 1 + 2 * iHandicap, UnitAITypes.UNITAI_ATTACK_CITY)
						makeUnits(iMongolia, iTrebuchet, tPlot, 1 + iHandicap, UnitAITypes.UNITAI_ATTACK_CITY)
						
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
				lEnemyCivs = []
				lFreePlots = []
				for x, y in lWestCoast:
					city = city_(x, y)
					if city and city.getOwner() != iAmerica:
						iCount += 1
						lWestCoast.remove((x, y))
						lEnemyCivs.append(city.getOwner())
						for plot in plots.surrounding(x, y):
							if not (plot.isCity() or plot.isPeak() or plot.isWater()):
								lFreePlots.append(location(plot))
									
				for iEnemy in lEnemyCivs:
					team(iPlayer).declareWar(iEnemy, True, WarPlanTypes.WARPLAN_LIMITED)
									
				if iCount > 0:
					for i in range(iCount):
						tPlot = random_entry(lFreePlots)
						makeUnits(iPlayer, iMinuteman, tPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
						makeUnits(iPlayer, iCannon, tPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
						
				if 2-iCount > 0:
					for i in range(2-iCount):
						tPlot = random_entry(lWestCoast)
						makeUnit(iPlayer, iSettler, tPlot)
						makeUnit(iPlayer, iMinuteman, tPlot)
						
			elif iCiv == iCivRussia:
				lFreePlots = []
				tVladivostok = (111, 51)
				
				x, y = tVladivostok
				pPlot = plot(x, y)
				convertPlotCulture(pPlot, iRussia, 100, True)
				if pPlot.isCity():
					if pPlot.getPlotCity().getOwner() != iRussia:
						for plot in plots.surrounding(tVladivostok):
							if not (plot.isCity() or plot.isWater() or plot.isPeak()):
								lFreePlots.append((i, j))
									
						tPlot = random_entry(lFreePlots)
						teamRussia.declareWar(pPlot.getOwner(), True, WarPlanTypes.WARPLAN_LIMITED)
						makeUnits(iPlayer, iRifleman, tPlot, 4, UnitAITypes.UNITAI_ATTACK_CITY)
						makeUnits(iPlayer, iCannon, tPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
				else:
					if isFree(iRussia, tVladivostok, True): # Also bNoEnemyUnits?
						pRussia.found(x, y)
						makeUnits(iPlayer, iRifleman, tVladivostok, 2)
						
						for plot in plots.surrounding(tVladivostok):
							convertPlotCulture(plot, iRussia, 80, True)
					


	def handleColonialAcquisition(self, iPlayer):
		pPlayer = player(iPlayer)
		targetList = getColonialTargets(iPlayer, True)
		targetCivList = []
		settlerList = []
		
		if not targetList:
			return

		iGold = len(targetList) * 200

		for plot in targetList:
			city = city_(plot)
			if city:
				iTargetCiv = city.getOwner()
				if not iTargetCiv in targetCivList:
					targetCivList.append(iTargetCiv)
			else:
				settlerList.append(location(plot))

		for tPlot in settlerList:
			colonialAcquisition(iPlayer, tPlot)
	
		for iTargetCiv in targetCivList:
			if player(iTargetCiv).isHuman():
				askedCities = [tPlot for tPlot in targetList if city(tPlot).getOwner() == iTargetCiv]
				
				if not askedCities:
					message = ''
				elif len(askedCities) == 1:
					message = city(askedCities[0]).getName()
				else:
					message = ', '.join([city(tPlot) for tPlot in askedCities[:-1]]) + text("TXT_KEY_AND") + city(askedCities[-1]).getName()
						
				iAskGold = len(askedCities) * 200
						
				popup = Popup.PyPopup(7625, EventContextTypes.EVENTCONTEXT_ALL)
				popup.setHeaderString(text("TXT_KEY_ASKCOLONIALCITY_TITLE", adjective(iPlayer)))
				popup.setBodyString(text("TXT_KEY_ASKCOLONIALCITY_MESSAGE", adjective(iPlayer), iAskGold, message))
				popup.addButton(text("TXT_KEY_POPUP_YES"))
				popup.addButton(text("TXT_KEY_POPUP_NO"))
				data.lTempEventList = (iPlayer, askedCities)
				popup.launch(False)
			else:
				bAccepted = is_minor(iTargetCiv) or (rand(100) >= tPatienceThreshold[iTargetCiv] and not team(iPlayer).isAtWar(iTargetCiv))
				
				iNumCities = 0
				for tPlot in targetList:
					if city_(tPlot).getOwner() == iTargetCiv:
						iNumCities += 1
						
				if iNumCities >= player(iTargetCiv).getNumCities():
					bAccepted = False

				for tPlot in targetList:
					if plot_(tPlot).getPlotCity().getOwner() == iTargetCiv:
						if bAccepted:
							colonialAcquisition(iPlayer, tPlot)
							player(iTargetCiv).changeGold(200)
						else:
							data.timedConquest(iPlayer, tPlot)

		pPlayer.setGold(max(0, pPlayer.getGold()-iGold))

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
			for iLoopCiv in lEnemyCivsOnSpawn[iCiv]:
				iLoopPlayer = civ(iLoopCiv)
			
				if team(iLoopPlayer).isAVassal(): continue
				if not player(iLoopPlayer).isAlive(): continue
				if pTeam.isAtWar(iLoopPlayer): continue
				if player(iPlayer).isHuman() and iLoopCiv not in lTotalWarOnSpawn[iCiv]: continue
				
				iLoopMin = 50
				if is_minor(iLoopPlayer): iLoopMin = 30
				if player(iLoopPlayer).isHuman(): iLoopMin += 10
				
				if rand(100) >= iLoopMin:
					iWarPlan = -1
					if iLoopCiv in lTotalWarOnSpawn[iCiv]:
						iWarPlan = WarPlanTypes.WARPLAN_TOTAL
					pTeam.declareWar(iLoopPlayer, False, iWarPlan)
					
					if pPlayer.isHuman(): data.iBetrayalTurns = 0
					
					
	def immuneMode(self, argsList): 
		pWinningUnit,pLosingUnit = argsList
		iLosingPlayer = pLosingUnit.getOwner()
		iUnitType = pLosingUnit.getUnitType()
		if iLosingPlayer < iNumMajorPlayers:
			if year() >= year(tBirth[iLosingPlayer]) and year() <= year(tBirth[iLosingPlayer])+2:
				if (pLosingUnit.getX(), pLosingUnit.getY()) == Areas.getCapital(iLosingPlayer):
					print("new civs are immune for now")
					if rand(100) >= 50:
						makeUnit(iLosingPlayer, iUnitType, pLosingUnit)

	def initMinorBetrayal(self, iPlayer):
		lPlots = Areas.getBirthArea(iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iPlayer)
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
				
			tSeaPlot = self.findSeaPlots(tPlot, 1, iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 2, iPlayer)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
				makeUnit(iPlayer, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iArcher, tSeaPlot)
		elif iCiv == iCivIndonesia:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnit(iPlayer, iArcher, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iPlayer)
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
				if not player(slot(iCivMoors)).isHuman():
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
				
			tSeaPlot = self.findSeaPlots(tPlot, 1, iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 2, iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 2, iPlayer)
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
			
			tSeaPlot = self.findSeaPlots(tPlot, 3, iPlayer)
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
		tCapital = Areas.getCapital(iJapan)
		if not pJapan.isHuman():
			makeUnit(iJapan, iSettler, tCapital)
		
		for iPlayer in range(iNumPlayers):
			if tBirth[iPlayer] > scenarioStartYear() and player(iPlayer).isHuman():
				makeUnit(iPlayer, iSettler, Areas.getCapital(iPlayer))
				makeUnit(iPlayer, iMilitia, Areas.getCapital(iPlayer))

	def create600ADstartingUnits( self ):

		tCapital = Areas.getCapital(iChina)
		makeUnits(iChina, iSwordsman, tCapital, 2)
		makeUnit(iChina, iArcher, tCapital)
		makeUnit(iChina, iSpearman, tCapital, UnitAITypes.UNITAI_CITY_DEFENSE)
		makeUnits(iChina, iChokonu, tCapital, 2)
		makeUnit(iChina, iHorseArcher, tCapital)
		makeUnits(iChina, iWorker, tCapital, 2)
		
		tCapital = Areas.getCapital(iJapan)
		tSeaPlot = self.findSeaPlots(tCapital, 1, iJapan)
		if tSeaPlot:
			makeUnits(iJapan, iWorkboat, tSeaPlot, 2)
			
		if not pJapan.isHuman():
			makeUnits(iJapan, iCrossbowman, tCapital, 2)
			makeUnits(iJapan, iSamurai, tCapital, 3)

		tCapital = Areas.getCapital(iByzantium)
		tSeaPlot = self.findSeaPlots(tCapital, 1, iByzantium)
		if tSeaPlot:
			makeUnits(iByzantium, iGalley, tSeaPlot, 2)
			makeUnits(iByzantium, iWarGalley, tSeaPlot, 2)

		tCapital = Areas.getCapital(iVikings)
		tSeaPlot = self.findSeaPlots(tCapital, 1, iVikings)
		if tSeaPlot:
			makeUnit(iVikings, iWorkboat, tSeaPlot)
			if pVikings.isHuman():
				makeUnit(iVikings, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iVikings, iSettler, tSeaPlot)
				makeUnit(iVikings, iArcher, tSeaPlot)
				makeUnits(iVikings, iLongship, tSeaPlot, 2, UnitAITypes.UNITAI_EXPLORE_SEA)
			else:
				makeUnits(iVikings, iLongship, tSeaPlot, 3, UnitAITypes.UNITAI_EXPLORE_SEA)
				
		# start AI settler and garrison in Denmark and Sweden
		if not pVikings.isHuman():
			makeUnit(iVikings, iSettler, (60, 56))
			makeUnit(iVikings, iArcher, (60, 56))
			makeUnit(iVikings, iSettler, (63, 59))
			makeUnit(iVikings, iArcher, (63, 59))
		else:
			makeUnit(iVikings, iSettler, tCapital)
			makeUnits(iVikings, iArcher, 2)

		tCapital = Areas.getCapital(iKorea)
		if not pKorea.isHuman():
			makeUnits(iKorea, iHeavySwordsman, tCapital, 2)
				
		tCapital = Areas.getCapital(iTurks)
		makeUnits(iTurks, iSettler, tCapital, 2)
		makeUnits(iTurks, iOghuz, tCapital, 6)
		makeUnit(iTurks, iArcher, tCapital)
		makeUnit(iTurks, iScout, tCapital)
			
		for iPlayer in range(iNumPlayers):
			if tBirth[iPlayer] > scenarioStartYear() and player(iPlayer).isHuman():
				tCapital = Areas.getCapital(iPlayer)
				makeUnit(iPlayer, iSettler, tCapital)
				makeUnit(iPlayer, iMilitia, tCapital)


	def create4000BCstartingUnits(self):
		for iPlayer in range(iNumPlayers):
			tCapital = Areas.getCapital(iPlayer)
			iCiv = civ(iPlayer)
			
			if tBirth[iPlayer] > scenarioStartYear() and player(iPlayer).isHuman():
				makeUnit(iPlayer, iSettler, tCapital)
				makeUnit(iPlayer, iMilitia, tCapital)
				
			if iPlayer == iHarappa and (data.isCivEnabled(iCiv) or player(iPlayer).isHuman()):
				makeUnit(iPlayer, iCityBuilder, tCapital)
				makeUnit(iPlayer, iMilitia, tCapital)
		
	def assignTechs(self, iPlayer):
		Civilizations.initPlayerTechs(iPlayer)
				
		sta.onCivSpawn(iPlayer)

	def arabianSpawn(self):
		tBaghdad = (77, 40)
		tCairo = (69, 35)
		tMecca = (75, 33)

		bBaghdad = plot(tBaghdad).getOwner() == iArabia
		bCairo = plot(tCairo).getOwner() == iArabia
		
		lCities = []
		
		if bBaghdad: lCities.append(tBaghdad)
		if bCairo: lCities.append(tCairo)
		
		tCapital = random_entry(lCities)
		
		if tCapital:
			if not pArabia.isHuman():
				moveCapital(iArabia, tCapital)
				makeUnits(iArabia, iMobileGuard, tCapital, 3)
				makeUnits(iArabia, iGhazi, tCapital, 2)
			makeUnits(iArabia, iMobileGuard, tCapital, 2)
			makeUnits(iArabia, iGhazi, tCapital, 2)
		
		if bBaghdad:
			makeUnit(iArabia, iSettler, tBaghdad)
			makeUnit(iArabia, iWorker, tBaghdad)
		
		if bCairo:
			makeUnit(iArabia, iSettler, tCairo)
			makeUnit(iArabia, iWorker, tCairo)
			
		if len(lCities) < 2:
			makeUnits(iArabia, iSettler, tMecca, 2 - len(lCities))
			makeUnits(iArabia, iWorker, tMecca, 2 - len(lCities))

		if not pArabia.isHuman() and bBaghdad:
			makeUnits(iArabia, iSpearman, tBaghdad, 2)
			
	def germanSpawn(self):
		if stability(iHolyRome) < iStabilityShaky: data.setStabilityLevel(iHolyRome, iStabilityShaky)
			
		dc.nameChange(iHolyRome)
		dc.adjectiveChange(iHolyRome)
		
	def holyRomanSpawn(self):
		plot = plot_(60, 56)
		if plot.isCity(): plot.getPlotCity().setCulture(iVikings, 5, True)
		
				
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
		
		if not pIndia.isHuman() and not pIndonesia.isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_TAMILS')
			
			if iRand <= 0:
				data.setCivPlayerEnabled(iCivTamils, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iCivTamils, False)
				
		if not pChina.isHuman() and not pIndia.isHuman() and not pMughals.isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_TIBET')
			
			if iRand <= 0:
				data.setCivEnabled(iCivTibet, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iCivTibet, False)
				
		if not pSpain.isHuman() and not pMali.isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_MOORS')
			
			if iRand <= 0:
				data.setCivEnabled(iCivMoors, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iCivMoors, False)
				
		if not pHolyRome.isHuman() and not pGermany.isHuman() and not pRussia.isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_POLAND')
			
			if iRand <= 0:
				data.setCivEnabled(iCivPoland, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iCivPoland, False)
				
		if not pMali.isHuman() and not pPortugal.isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_CONGO')
			
			if iRand <= 0:
				data.setCivEnabled(iCivCongo, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iCivCongo, False)
				
		if not pSpain.isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_ARGENTINA')
			
			if iRand <= 0:
				data.setCivEnabled(iCivArgentina, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iCivArgentina, False)
				
		if not pPortugal.isHuman():
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
		coreCities = cities.of(Areas.getCoreArea(iPlayer))
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