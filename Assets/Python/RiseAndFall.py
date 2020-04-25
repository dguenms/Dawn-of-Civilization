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
		
		popup.addPopup(active())
	
def applyNewCivSwitchEvent(argsList):
	iButton = argsList[0]
	iPlayer = argsList[1]
	
	if iButton == 1:
		handleNewCiv(iPlayer)
		
### Utility methods ###

def handleNewCiv(iPlayer):
	iPreviousPlayer = active()
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
		data.iFlipOldPlayer = active()
		data.lTempPlots = lPlots

	def eventApply7615(self, popupReturn):
		lPlots = data.lTempPlots
		iFlipNewPlayer = data.iFlipNewPlayer
		
		iNumCities = player(iFlipNewPlayer).getNumCities()

		lHumanCityList = [city for city in self.getConvertedCities(iFlipNewPlayer, lPlots) if city.isHuman()]
		
		if popupReturn.getButtonClicked() == 0:
			message(active(), 'TXT_KEY_FLIP_AGREED', color=iGreen)
						
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
				if city(x, y).isHuman():
					colonialAcquisition(iPlayer, tPlot)
					player().changeGold(200)
		elif popupReturn.getButtonClicked() == 1:
			for x, y in targetList:
				if city(x, y).getOwner() == human():
					colonialConquest(iPlayer, tPlot)
		
	def eventApply7629(self, netUserData, popupReturn):
		targetList = data.lByzantineBribes
		iButton = popupReturn.getButtonClicked()
		
		if iButton >= len(targetList): return
		
		iByzantiumPlayer = slot(iByzantium)
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
		if player(iEgypt).isHuman():
			for unit in units.at(plots.capital(iEgypt)):
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
			
			player(iChina).updateTradeRoutes()
		
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
			player(iPlayer).setStartingPlot(plots.capital(iPlayer), False)

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
				plot_(x, y).setOwner(slot(iChina))
		
		for plot in plots.start(tTL).end(tBR).without(lExceptions).including(lAdditions):
			if not plot.isWater(): plot.setWithinGreatWall(True)

	def adjust1700ADCulture(self):
		for plot in plots.all():
			if plot.getOwner() != -1:
				plot.changeCulture(plot.getOwner(), 100, True)
				convertPlotCulture(plot, plot.getOwner(), 100, True)
					
		for x, y in [(48, 45), (50, 44), (50, 43), (50, 42), (49, 40)]:
			convertPlotCulture(plot_(x, y), slot(iPortugal), 100, True)
			
		for x, y in [(58, 49), (59, 49), (60, 49)]:
			convertPlotCulture(plot_(x, y), slot(iGermany), 100, True)
			
		for x, y in [(62, 51)]:
			convertPlotCulture(plot_(x, y), slot(iHolyRome), 100, True)
			
		for x, y in [(58, 52), (58, 53)]:
			convertPlotCulture(plot_(x, y), slot(iNetherlands), 100, True)
			
		for x, y in [(64, 53), (66, 55)]:
			convertPlotCulture(plot_(x, y), slot(iPoland), 100, True)
			
		for x, y in [(67, 58), (68, 59), (69, 56), (69, 54)]:
			convertPlotCulture(plot_(x, y), slot(iRussia), 100, True)

	def prepareColonists(self):
		# TODO: unify all those lists for colonists, trading company conquerors, trading company corporation...
		dColonistsAlreadyGiven = {
			iVikings : 1,
			iSpain : 7,
			iFrance : 3,
			iEngland : 3,
			iPortugal : 6,
			iNetherlands : 4,
			iGermany : 0,
		}
		
		for iCiv, iColonists in dColonistsAlreadyGiven.items():
			iPlayer = slot(iCiv)
			if iPlayer >= 0:
				data.players[iPlayer].iExplorationTurn = year(1700)
				data.players[iPlayer].iColonistsAlreadyGiven = iColonists

	def init1700ADDiplomacy(self):
		team(iEngland).declareWar(slot(iMughals), False, WarPlanTypes.WARPLAN_LIMITED)
		team(iIndia).declareWar(slot(iMughals), False, WarPlanTypes.WARPLAN_TOTAL)

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
			capital = plots.capital(iChina)
			lBuildings = [iGranary, iConfucianTemple, iTaixue, iBarracks, iForge]
			foundCapital(slot(iChina), location(capital), "Xi'an", 4, 100, lBuildings, [iConfucianism, iTaoism])
			
		elif scenario() == i1700AD:
			
			# Chengdu
			city(99, 41).setCulture(slot(iChina), 100, True)

	def flipStartingTerritory(self):
	
		if scenario() == i600AD:
			
			# China
			if not player(iChina).isHuman(): tTL = (99, 39) # 4 tiles further south
			self.startingFlip(slot(iChina), [dBirthArea[iChina]])
			
		if scenario() == i1700AD:
		
			# China (Tibet)
			tTibetTL = (94, 42)
			tTibetBR = (97, 45)
			tManchuriaTL = (105, 51)
			tManchuriaBR = (109, 55)
			self.startingFlip(slot(iChina), [(tTibetTL, tTibetBR), (tManchuriaTL, tManchuriaBR)])
			
			# Russia (Sankt Peterburg)
			convertPlotCulture(plot(68, 58), slot(iRussia), 100, True)
			convertPlotCulture(plot(67, 57), slot(iRussia), 100, True)

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
			player(iBarbarian).found(105, 49)
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
		pBeijing.setBuildingOriginalOwner(iTaoistShrine, slot(iChina))
		pBeijing.setBuildingOriginalOwner(iGreatWall, slot(iChina))
		
		pNanjing = city(105, 43)
		pNanjing.setBuildingOriginalOwner(iConfucianShrine, slot(iChina))
		
		pPataliputra = city(94, 40)
		pPataliputra.setBuildingOriginalOwner(iHinduShrine, slot(iIndia))
		pPataliputra.setBuildingOriginalOwner(iBuddhistShrine, slot(iIndia))
		
		pSirajis = city(82, 38)
		pSirajis.setBuildingOriginalOwner(iZoroastrianShrine, slot(iPersia))
		
		pAlexandria = city(67, 36)
		pAlexandria.setBuildingOriginalOwner(iGreatLighthouse, slot(iEgypt))
		pAlexandria.setBuildingOriginalOwner(iGreatLibrary, slot(iEgypt))
		
		pMemphis = city(69, 35)
		pMemphis.setBuildingOriginalOwner(iPyramids, slot(iEgypt))
		pMemphis.setBuildingOriginalOwner(iGreatSphinx, slot(iEgypt))
		
		pAthens = city(67, 41)
		pAthens.setBuildingOriginalOwner(iParthenon, slot(iGreece))
		
		pRome = city(60, 44)
		pRome.setBuildingOriginalOwner(iFlavianAmphitheatre, slot(iRome))
		
		pChichenItza = city(23, 37)
		pChichenItza.setBuildingOriginalOwner(iTempleOfKukulkan, slot(iMaya))

	def adjust1700ADWonders(self):
		lExpiredWonders = [iOracle, iIshtarGate, iHangingGardens, iGreatCothon, iApadanaPalace, iColossus, iStatueOfZeus, iGreatMausoleum, iTempleOfArtemis, iAquaAppia, iAlKhazneh, iJetavanaramaya, iGreatLighthouse, iMoaiStatues, iFlavianAmphitheatre, iGreatLibrary, iGondeshapur, iSilverTreeFountain, iAlamut]
		self.expireWonders(lExpiredWonders)
	
		pMilan = city(59, 47)
		pMilan.setBuildingOriginalOwner(iSantaMariaDelFiore, slot(iItaly))
		pMilan.setBuildingOriginalOwner(iSanMarcoBasilica, slot(iItaly))
		
		pDjenne = city(51, 30)
		pDjenne.setBuildingOriginalOwner(iUniversityOfSankore, slot(iMali))
		
		pJerusalem = city(73, 38)
		pJerusalem.setBuildingOriginalOwner(iJewishShrine, slot(iIndependent))
		pJerusalem.setBuildingOriginalOwner(iOrthodoxShrine, slot(iByzantium))
		pJerusalem.setBuildingOriginalOwner(iDomeOfTheRock, slot(iArabia))
		
		pBaghdad = city(77, 40)
		pBaghdad.setBuildingOriginalOwner(iSpiralMinaret, slot(iArabia))
		
		pRome = city(60, 44)
		pRome.setBuildingOriginalOwner(iFlavianAmphitheatre, slot(iRome))
		pRome.setBuildingOriginalOwner(iSistineChapel, slot(iItaly))
		
		pSeville = city(51, 41)
		pSeville.setBuildingOriginalOwner(iMezquita, slot(iMoors))
		
		pBangkok = city(101, 33)
		pBangkok.setBuildingOriginalOwner(iWatPreahPisnulok, slot(iKhmer))
		
		pChichenItza = city(23, 37)
		pChichenItza.setBuildingOriginalOwner(iTempleOfKukulkan, slot(iMaya))
		
		pConstantinople = city(68, 45)
		pConstantinople.setBuildingOriginalOwner(iTheodosianWalls, slot(iByzantium))
		pConstantinople.setBuildingOriginalOwner(iHagiaSophia, slot(iByzantium))
		
		pJakarta = city(104, 25)
		pJakarta.setBuildingOriginalOwner(iBorobudur, slot(iIndonesia))
		
		pMexicoCity = city(18, 37)
		pMexicoCity.setBuildingOriginalOwner(iFloatingGardens, slot(iAztecs))
		
		pCairo = city(69, 35)
		pCairo.setBuildingOriginalOwner(iPyramids, slot(iEgypt))
		pCairo.setBuildingOriginalOwner(iGreatSphinx, slot(iEgypt))
		
		pAthens = city(67, 41)
		pAthens.setBuildingOriginalOwner(iParthenon, slot(iGreece))
		
		pShiraz = city(82, 38)
		pShiraz.setBuildingOriginalOwner(iZoroastrianShrine, slot(iPersia))
		
		pPataliputra = city(94, 40)
		pPataliputra.setBuildingOriginalOwner(iHinduShrine, slot(iIndia))
		pPataliputra.setBuildingOriginalOwner(iBuddhistShrine, slot(iIndia))
		
		pMecca = city(75, 33)
		pMecca.setBuildingOriginalOwner(iIslamicShrine, slot(iArabia))

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
		
		for iCiv, iGreatPeople in dGreatPeopleCreated.iteritems():
			player(iCiv).changeGreatPeopleCreated(iGreatPeople)
			
		for iCiv, iGreatGenerals in dGreatGeneralsCreated.iteritems():
			player(iCiv).changeGreatGeneralsCreated(iGreatGenerals)

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
		
		if iGameTurn == year(dBirth[iSpain])-1:
			if scenario() == i600AD:
				pMassilia = city_(56, 46)
				if pMassilia:
					pMassilia.setCulture(pMassilia.getOwner(), 1, True)

		# Leoreth: Turkey immediately flips independent cities in its core to avoid being pushed out of Anatolia
		if iGameTurn == data.iOttomanSpawnTurn + 1:
			for city in cities.birth(iOttomans):
				iOwner = city.getOwner()
				if is_minor(iOwner):
					flipCity(city, False, True, slot(iOttomans), ())
					cultureManager(city, 100, slot(iOttomans), iOwner, True, False, False)
					self.convertSurroundingPlotCulture(slot(iOttomans), plots.surrounding(city))
					makeUnit(iOttomans, iCrossbowman, city)
					
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
			updateMinorTechs(iMinor, iBarbarianPlayer)

		#Leoreth: give Phoenicia a settler in Qart-Hadasht in 820BC
		if not player(iPhoenicia).isHuman() and year() == year(-820) - (data.iSeed % 10):
			makeUnit(iPhoenicia, iSettler, (58, 39))
			makeUnits(iPhoenicia, iArcher, (58, 39), 2)
			makeUnits(iPhoenicia, iWorker, (58, 39), 2)
			makeUnits(iPhoenicia, iWarElephant, (58, 39), 2)
			
		if year() == year(476):
			if player(iItaly).isHuman() and player(iRome).isAlive():
				sta.completeCollapse(slot(iRome))
				
		if year() == year(-50):
			if player(iByzantium).isHuman() and player(iGreece).isAlive():
				sta.completeCollapse(slot(iGreece))
				
		if year() == year(dBirth[iIndia])-turns(1):
			if player(iHarappa).isAlive() and not player(iHarappa).isHuman():
				sta.completeCollapse(slot(iHarappa))
			
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
				self.giveRaiders(iVikings)
		
		if year().between(1350, 1918):
			for iCiv in [iSpain, iEngland, iFrance, iPortugal, iNetherlands, iVikings, iGermany]:
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
		if year() == year(1500) and player(iAztecs).isHuman():
			plot = plots.capital(iEngland)
			if plot.isCity():
				city = plot.getPlotCity()
				if city.getPopulation() > 14:
					city.changePopulation(-3)
				
		# Leoreth: make sure Aztecs are dead in 1700 if a civ that spawns from that point is selected
		if year() == year(1700)-2:
			if year(dBirth[active()]) >= year(1700) and player(iAztecs).isAlive():
				sta.completeCollapse(slot(iAztecs))

		for iLoopPlayer in players.major().where(lambda p: dBirth[p] > scenarioStartYear()):
			if year(dBirth[iLoopPlayer]) - turns(2) <= year() <= year(dBirth[iLoopPlayer]) + turns(6):
				self.initBirth(dBirth[iLoopPlayer], iLoopPlayer)

		if year() == year(600):
			if scenario() == i600AD:  #late start condition
				tTL, tBR = dBirthArea[iChina]
				if not player(iChina).isHuman(): tTL = (99, 39) # 4 tiles further north
				china = plots.start(tTL).end(tBR)
				iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(slot(iChina), china)
				self.convertSurroundingPlotCulture(slot(iChina), china)
				
				for iMinor in players.independent().barbarian():
					flipUnitsInArea(china, slot(iChina), iMinor, False, player(iMinor).isBarbarian())

		#kill the remaining barbs in the region: it's necessary to do this more than once to protect those civs
		for iCiv in [iVikings, iSpain, iFrance, iHolyRome, iRussia, iAztecs]:
			if year(dBirth[iCiv]) + turns(2) <= year() <= year(dBirth[iCiv]) + turns(10):
				killUnitsInArea(iBarbarianPlayer, plots.birth(iCiv))
				
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

			if year() == year(iYear)+1 and player(iCiv).isAlive() and player(iCiv).getLastBirthTurn() == year()-1:
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
		if iCiv == iAztecs and infos.constant('PLAYER_REBIRTH_MEXICO') == 0: return
		if iCiv == iMaya and infos.constant('PLAYER_REBIRTH_COLOMBIA') == 0: return
		
		if iCiv in dRebirthCiv:
			iCiv = dRebirthCiv[iCiv]
			setCivilization(iPlayer, iCiv)
			
		Modifiers.updateModifiers(iPlayer)
		x, y = dCapitals[iCiv]
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

		message(active(), 'TXT_KEY_INDEPENDENCE_TEXT', adjective(iPlayer), color=iGreen)
		
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
		if iCiv in [iMexico, iColombia]:
			self.setStateReligion(iPlayer)

		self.assignTechs(iPlayer)
		if year() >= year(dBirth[active()]):
			startNewCivSwitchEvent(iPlayer)

		player(iPlayer).setInitialBirthTurn(year(dSpawn[iCiv]))

		# adjust gold, civics, religion and other special settings
		if iCiv == iIran:
			pPlayer.setGold(600)
			pPlayer.setLastStateReligion(iIslam)
			pPlayer.setCivics(iCivicsGovernment, iMonarchy)
			pPlayer.setCivics(iCivicsLegitimacy, iVassalage)
			pPlayer.setCivics(iCivicsSociety, iSlavery)
			pPlayer.setCivics(iCivicsEconomy, iMerchantTrade)
			pPlayer.setCivics(iCivicsReligion, iTheocracy)
			
		elif iCiv == iMexico:
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
			
		elif iCiv == iColombia:
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

		rebirthArea = plots.birth(iCiv)

		# exclude American territory for Mexico
		if iCiv == iMexico:
			rebirthArea = rebirthArea.where(lambda p: owner(p) != iAmerica or p in plots.core(iCiv))

		rebirthCities = rebirthArea.cities()
			
		# remove garrisons
		for city in rebirthCities.notowner(active()):
			relocateGarrisons(location(city), city.getOwner())
			relocateSeaGarrisons(location(city), city.getOwner())
				
		# convert cities
		iConvertedCities, iHumanCities = self.convertSurroundingCities(iPlayer, rebirthArea)
		
		# create garrisons
		for city in rebirthCities.owner(active()):
			createGarrisons(location(city), iPlayer, 1)
				
		# convert plot culture
		self.convertSurroundingPlotCulture(iPlayer, rebirthArea)
		
		# reset plague
		data.players[iPlayer].iPlagueCountdown = -10
		clearPlague(iPlayer)
		
		# adjust starting stability
		data.players[iPlayer].resetStability()
		data.players[iPlayer].iStabilityLevel = iStabilityStable
		if player(iPlayer).isHuman(): data.resetHumanStability()
		
		# ask human player for flips
		if iHumanCities > 0 and not player(iPlayer).isHuman():
			self.scheduleFlipPopup(iPlayer, rebirthArea)

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
				barbarianCities = cities.normal(iDeadPlayer).owner(iBarbarian)
				
				if barbarianCities > 3:
					for iMinor, minorCities in barbarianCities.fraction(2).divide(players.independent()):
						for city in minorCities:
							completeCityFlip(city, iMinor, iBarbarianPlayer, 50, False, True, True, True)
					
					return

	def secession(self, iGameTurn):
		for iPlayer in players.major().shuffle():
			if player(iPlayer).isAlive() and iGameTurn >= year(dBirth[iPlayer]) + turns(30):
				
				if stability(iPlayer) == iStabilityCollapsing:

					cityList = []
					for city in cities.owner(iPlayer):
						pPlot = plot(city)

						if not city.isWeLoveTheKingDay() and not city.isCapital() and location(city) != location(plots.capital(iPlayer)):
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
						iNewCiv = iIndependent
						if rand(2) == 1:
							iNewCiv = iIndependent2
						
						if civ(iPlayer) in [iAztecs, iInca, iMaya, iEthiopia, iMali, iCongo]:
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
		
		lConditionalCivs = [iByzantium, iMughals, iOttomans, iThailand, iBrazil, iArgentina, iCanada, iItaly]
		
		# Leoreth: extra checks for conditional civs
		if iCiv in lConditionalCivs and not player(iPlayer).isHuman():
			if iCiv == iByzantium:
				if not player(iRome).isAlive() or player(iGreece).isAlive() or (player(iRome).isHuman() and stability(slot(iRome)) == iStabilitySolid):
					return
					
			elif iCiv == iOttomans:
				tMiddleEastTL = (69, 38)
				tMiddleEastBR = (78, 45)
				if cities.start(tMiddleEastTL).end(tMiddleEastBR).any(lambda city: slot(iTurks) in [city.getOwner(), city.getPreviousOwner()]):
					return

			elif iCiv == iThailand:
				if not player(iKhmer).isHuman():
					if stability(slot(iKhmer)) > iStabilityShaky:
						return
				else:
					if stability(slot(iKhmer)) > iStabilityUnstable:
						return
						
			elif iCiv in [iArgentina, iBrazil]:
				iColonyPlayer = getColonyPlayer(iPlayer)
				if iColonyPlayer < 0: return
				elif civ(iColonyPlayer) not in [iArgentina, iBrazil]:
					if stability(iColonyPlayer) > iStabilityStable:
						return
						
			elif iCiv == iItaly:
				if player(iRome).isAlive():
					return
					
				if not getCitiesInCore(slot(iRome)).where(lambda city: city.getOwner() not in players.major()):
					return
		
		periods.onBirth(iPlayer)
				
		tCapital = location(plots.capital(iCiv))
				
		x, y = tCapital
		bCapitalSettled = False
		
		if iCiv == iItaly:
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

			tTopLeft, tBottomRight = birthRectangle(iCiv)
			tBroaderTopLeft, tBroaderBottomRight = dBroaderArea[iCiv]
			
			if iCiv == iThailand:
				angkor = cities.capital(iKhmer)
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
				
				if (iCiv in lConditionalCivs and iCiv != iThailand) or bCapitalSettled:
					bBirthInCapital = True
				
				if iCiv == iOttomans:
					self.moveOutInvaders(tTopLeft, tBottomRight)  
					
				if bBirthInCapital:
					makeUnit(iPlayer, iCatapult, (0, 0))
			
				bDeleteEverything = False
				pCapital = plot_(x, y)
				if pCapital.isOwned():
					if player(iPlayer).isHuman() or not player().isAlive():
						if not (pCapital.isCity() and pCapital.getPlotCity().isHolyCity()):
							bDeleteEverything = True
							print ("bDeleteEverything 1")
					else:
						bDeleteEverything = True
						for pPlot in plots.surrounding(tCapital):
							if (pPlot.isCity() and (pPlot.getPlotCity().isHuman() or pPlot.getPlotCity().isHolyCity())) or iCiv == iOttomans:
								bDeleteEverything = False
								print ("bDeleteEverything 2")
								break
				print ("bDeleteEverything", bDeleteEverything)
				if not plot_(x, y).isOwned():
					if iCiv in [iNetherlands, iPortugal, iByzantium, iKorea, iThailand, iItaly, iCarthage]: #dangerous starts
						data.lDeleteMode[0] = iPlayer
					if bBirthInCapital:
						self.birthInCapital(iPlayer, iPreviousOwner, tCapital, tTopLeft, tBottomRight)
					else:
						self.birthInFreeRegion(iPlayer, tCapital, tTopLeft, tBottomRight)
				elif bDeleteEverything and not bBirthInCapital:
					for pCurrent in plots.surrounding(tCapital):
						data.lDeleteMode[0] = iPlayer
						for iLoopPlayer in players.all().without(iPlayer):
							flipUnitsInArea(plots.birth(iCiv), iPlayer, iLoopPlayer, True, False)
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
		for plot in plots.normal(iCiv):
			plot.setRevealed(iPlayer, True, True, 0)
				
		# Leoreth: conditional state religion for colonial civs and Byzantium
		if iCiv in [iByzantium, iArgentina, iBrazil]:
			self.setStateReligion(iPlayer)
			
		if canSwitch(iPlayer, iBirthYear):
			startNewCivSwitchEvent(iPlayer)
			
		data.players[iPlayer].bSpawned = True

	def moveOutInvaders(self, tTL, tBR):
		if player(iMongols).isAlive():
			mongolCapital = player(iMongols).getCapitalCity()
		for plot in plots.start(tTL).end(tBR):
			for unit in units.at(plot):
				if not isDefenderUnit(unit):
					if civ(unit) == iMongols:
						if not player(iMongols).isHuman():
							move(unit, mongolCapital)
					else:
						if unit.getUnitType() == iKeshik:
							unit.kill(False, iBarbarianPlayer)

	def deleteMode(self, iCurrentPlayer):
		iPlayer = data.lDeleteMode[0]
		iCiv = civ(iPlayer)
		
		print ("deleteMode after", iCurrentPlayer)
		tCapital = location(plots.capital(iCiv))
		x, y = tCapital
		
		if iCurrentPlayer == iPlayer:
			if iCiv == iPhoenicia:
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
		
		if iCurrentPlayer != iPlayer-1 and iCiv not in [iCarthage, iGreece]:
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
				
				if iCiv == iOttomans:
					data.iOttomanSpawnTurn = turn()
			
				if iCiv == iItaly:
					removeCoreUnits(iPlayer)
					cityList = getCitiesInCore(iPlayer)
					
					rome = cities.capital(iRome)
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
		
			area = plots.rectangle(tTopLeft, tBottomRight).without(dBirthAreaExceptions[iPlayer])
			iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iPlayer, area)
			self.convertSurroundingPlotCulture(iPlayer, area)
			for iMinor in players.independent().barbarian():
				flipUnitsInArea(area, iPlayer, iMinor, False, player(iMinor).isBarbarian())
		
			# create starting workers
			if iNumCities == 0 and player(iPlayer).getNumCities() > 0:
				self.createStartingWorkers(iPlayer, player(iPlayer).getCapitalCity())
			
			if iCiv == iArabia:
				self.arabianSpawn()
				
			if iCiv == iGermany:
				self.germanSpawn()
   
			#cover plots revealed by the lion
			clearCatapult(iPlayer)

			if iNumHumanCitiesToConvert > 0 and not player(iPlayer).isHuman(): # Leoreth: quick fix for the "flip your own cities" popup, still need to find out where it comes from
				self.scheduleFlipPopup(iPlayer, lPlots)

	def birthInForeignBorders(self, iPlayer, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight):
		iCiv = civ(iPlayer)
	
		if iCiv == iItaly:
			removeCoreUnits(iPlayer)
			cityList = self.getCitiesInCore(iPlayer)
			
			rome = cities.capital(iRome)
			if rome:
				cityList.append(rome)
				
			for pCity in cityList:
				if city.getPopulation() < 5: city.setPopulation(5)
				city.setHasRealBuilding(iGranary, True)
				city.setHasRealBuilding(iLibrary, True)
				city.setHasRealBuilding(iCourthouse, True)
				if city.isCoastal(20): city.setHasRealBuilding(iHarbor, True)
				
		iNumCities = player(iPlayer).getNumCities()
		
		area = plots.start(tTopLeft).end(tBottomRight).without(dBirthAreaExceptions[iCiv])
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
			
			if iCiv == iOttomans:
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
			
		if iCiv == iGermany:
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
			area = plots.start(tTopLeft).end(tBottomRight).without(dBirthAreaExceptions[iCiv])
			iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iPlayer, area)
			self.convertSurroundingPlotCulture(iPlayer, area)
				
			for iMinorCiv in [iIndependent, iIndependent2, iBarbarian]:
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
		if iCiv == iByzantium and player(iRome).isAlive():
			x, y = location(plots.capital(iByzantium))
			for city in cities.owner(iRome):
				if city.getX() >= x-1 and city.getY() <= y:
					if (city.getX(), city.getY()) not in lPlots:
						lCities.append(city)
					
		# Leoreth: Canada also flips English/American/French cities in the Canada region
		if iCiv == iCanada:
			for city in cities.owner(iFrance) + cities.owner(iEngland) + cities.owner(iAmerica):
				if city.getRegionID() == rCanada and city.getX() < plots.capital(iCanada).getX() and location(city) not in [location(c) for c in lCities]:
					lCities.append(city)
					
		# Leoreth: remove capital locations
		for city in lCities:
			if not is_minor(city):
				if location(city) == location(plots.capital(city.getOwner())) and city.isCapital():
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
			elif iOwner == active():
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
	
		if iCiv == iCanada: 
			return
			
		elif iCiv == iGermany and not player(iPlayer).isHuman():
			return
		
		if year() <= year(dBirth[iCiv]) + turns(5):
			for iEnemy in lEnemies:
				tEnemy = team(iEnemy)
				
				if tEnemy.isAtWar(iPlayer): continue
				if iCiv == iByzantium and civ(iEnemy) == iRome: continue
			
				iRand = rand(100)
				if iRand >= dAIStopBirthThreshold[iEnemy]:
					tEnemy.declareWar(iPlayer, True, WarPlanTypes.WARPLAN_ATTACKED_RECENT)
					self.spawnAdditionalUnits(iPlayer)

	def spawnAdditionalUnits(self, iPlayer):
		self.createAdditionalUnits(iPlayer, location(plots.capital(iPlayer)))

	def convertSurroundingPlotCulture(self, iCiv, plots):
		for pPlot in plots:
			if pPlot.isOwned() and pPlot.isCore(pPlot.getOwner()) and not pPlot.isCore(iCiv): continue
			pPlot.resetCultureConversion()
			if not pPlot.isCity():
				convertPlotCulture(pPlot, iCiv, 100, False)

	def findSeaPlots(self, tCoords, iRange, iCiv):
		"""Searches a sea plot that isn't occupied by a unit and isn't a civ's territory surrounding the starting coordinates"""
		return plots.surrounding(tCoords, radius=iRange).water().where(lambda p: not p.isUnit()).where(lambda p: p.getOwner() in [-1, slot(iCiv)]).random()

	def giveRaiders(self, iCiv):
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

			if iCiv == iRome:
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
				sourceCities = cities.core(iCiv).owner(iPlayer)
				
				# help England with settling Canada and Australia
				if iCiv == iEngland:
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
				if year() <= year(dBirth[iAztecs]) + turns(10):
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
							if iNewWorldCiv == iInca or player(iNewWorldPlayer).getNumCities() > 4:
								iModifier1 = 1
							if not player(iNewWorldPlayer).isHuman():
								iModifier2 = 1
								
						if year() < year(dBirth[active()]):
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
							
						if iNewWorldCiv == iInca:
							makeUnits(iOldWorldPlayer, iAucac, arrivalPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
						elif iNewWorldCiv == iAztecs:
							makeUnits(iOldWorldPlayer, iJaguar, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
							makeUnit(iOldWorldPlayer, iHolkan, arrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY)
						elif iNewWorldCiv == iMaya:
							makeUnits(iOldWorldPlayer, iHolkan, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
							makeUnit(iOldWorldPlayer, iJaguar, arrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY)
							
						message(iNewWorldPlayer, 'TXT_KEY_FIRST_CONTACT_NEWWORLD')
						message(iOldWorldPlayer, 'TXT_KEY_FIRST_CONTACT_OLDWORLD')
							
		# Leoreth: Mongol horde event against Mughals, Persia, Arabia, Byzantium, Russia
		if civ(iHasMetTeamY) == iMongols and not player(iMongols).isHuman():
			iCivX = civ(iTeamX)
		
			if iCivX in lMongolCivs:
				if year() < year(1500) and data.isFirstContactMongols(iCivX):

					data.setFirstContactMongols(iCivX, False)
		
					teamTarget = team(iTeamX)
						
					if iCivX == iArabia:
						tTL = (73, 31)
						tBR = (84, 43)
						iDirection = DirectionTypes.DIRECTION_EAST
					elif iCivX == iPersia:
						tTL = (73, 37)
						tBR = (86, 48)
						iDirection = DirectionTypes.DIRECTION_NORTH
					elif iCivX == iByzantium:
						tTL = (68, 41)
						tBR = (77, 46)
						iDirection = DirectionTypes.DIRECTION_EAST
					elif iCivX == iRussia:
						tTL = (68, 48)
						tBR = (81, 62)
						iDirection = DirectionTypes.DIRECTION_EAST

					lTargetList = getBorderPlots(iTeamX, tTL, tBR, iDirection, 3)
					
					if not lTargetList: return

					team(iMongols).declareWar(iTeamX, True, WarPlanTypes.WARPLAN_TOTAL)
					
					iHandicap = 0
					if teamtype(iTeamX).isHuman():
						iHandicap = game.getHandicapType() / 2

					for tPlot in lTargetList:
						makeUnits(iMongols, iKeshik, tPlot, 2 + iHandicap, UnitAITypes.UNITAI_ATTACK_CITY)
						makeUnits(iMongols, iMangudai, tPlot, 1 + 2 * iHandicap, UnitAITypes.UNITAI_ATTACK_CITY)
						makeUnits(iMongols, iTrebuchet, tPlot, 1 + iHandicap, UnitAITypes.UNITAI_ATTACK_CITY)
						
					message(iTeamX, 'TXT_KEY_MONGOL_HORDE_HUMAN')
					if team().canContact(iTeamX):
						message(active(), 'TXT_KEY_MONGOL_HORDE', adjective(iTeamX))

	def lateTradingCompany(self, iPlayer):
		iCiv = civ(iPlayer)
	
		if not player(iPlayer).isHuman() and not team(iPlayer).isAVassal() and scenario() != i1700AD:
			if iCiv in [iFrance, iEngland, iNetherlands]:
				self.handleColonialConquest(iPlayer)

	def earlyTradingCompany(self, iPlayer):
		iCiv = civ(iPlayer)
	
		if not player(iPlayer).isHuman() and not team(iPlayer).isAVassal():
			if iCiv in [iSpain, iPortugal]:
				self.handleColonialAcquisition(iPlayer)
				
	def onRailroadDiscovered(self, iPlayer):
		iCiv = civ(iPlayer)
	
		if not player(iPlayer).isHuman():
			if iCiv == iAmerica:
				iCount = 0
				lWestCoast = [(11, 50), (11, 49), (11, 48), (11, 47), (11, 46), (12, 45)]
				
				enemyCities = cities.of(lWestCoast).notowner(iAmerica)
				
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
						
			elif iCiv == iRussia:
				lFreePlots = []
				x, y = (111, 51)
				
				city = city_(x, y)
				plot = plot_(x, y)
				convertPlotCulture(plot, iPlayer, 100, True)
				if city:
					if civ(city) != iRussia:
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
			if iBirthTurn <= year() <= iBirthTurn + turns(2):
				if location(pLosingUnit) == location(plots.capital(iLosingPlayer)):
					if rand(100) >= 50:
						makeUnit(iLosingPlayer, iUnitType, pLosingUnit)

	def initMinorBetrayal(self, iPlayer):
		birthArea = plots.birth(iPlayer)
		plotList = listSearch(birthArea, outerInvasion, [])
		if plotList:
			tPlot = random_entry(plotList)
			if tPlot:
				self.createAdditionalUnits(iPlayer, tPlot)
				self.unitsBetrayal(iPlayer, active(), lPlots, tPlot)

	def initBetrayal( self ):
		iFlipPlayer = data.iFlipNewPlayer
		if not player(iFlipPlayer).isAlive() or not team(iFlipPlayer).isAtWar(active()):
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
	
		if iCiv == iIndia:
			makeUnits(iPlayer, iArcher, tPlot, 2)
			makeUnit(iPlayer, iLightSwordsman, tPlot)
		elif iCiv == iGreece:
			makeUnits(iPlayer, iHoplite, tPlot, 4)
		elif iCiv == iPersia:
			makeUnits(iPlayer, iImmortal, tPlot, 4)
		elif iCiv == iCarthage:
			makeUnit(iPlayer, iWarElephant, tPlot)
			makeUnit(iPlayer, iNumidianCavalry, tPlot)
		elif iCiv == iPolynesia:
			makeUnits(iPlayer, iMilitia, tPlot, 2)
		elif iCiv == iRome:
			makeUnits(iPlayer, iLegion, tPlot, 4)
		elif iCiv == iJapan:
			makeUnits(iPlayer, iArcher, tPlot, 2)
			makeUnits(iPlayer, iSwordsman, tPlot, 2)
		elif iCiv == iTamils:
			makeUnits(iPlayer, iSwordsman, tPlot, 2)
			makeUnit(iPlayer, iWarElephant, tPlot)
		elif iCiv == iEthiopia:
			makeUnits(iPlayer, iArcher, tPlot, 2)
			makeUnits(iPlayer, iShotelai, tPlot, 2)
		elif iCiv == iKorea:
			makeUnits(iPlayer, iHorseArcher, tPlot, 2)
			makeUnits(iPlayer, iCrossbowman, tPlot, 2)
		elif iCiv == iMaya:
			makeUnits(iPlayer, iArcher, tPlot, 2)
			makeUnits(iPlayer, iHolkan, tPlot, 2)
		elif iCiv == iByzantium:
			makeUnits(iPlayer, iCataphract, tPlot, 2)
			makeUnits(iPlayer, iHorseArcher, tPlot, 2)
		elif iCiv == iVikings:
			makeUnits(iPlayer, iHuscarl, tPlot, 3)
		elif iCiv == iTurks:
			makeUnits(iPlayer, iOghuz, tPlot, 4)
		elif iCiv == iArabia:
			makeUnits(iPlayer, iGhazi, tPlot, 2)
			makeUnits(iPlayer, iMobileGuard, tPlot, 4)
		elif iCiv == iTibet:
			makeUnits(iPlayer, iKhampa, tPlot, 2)
		elif iCiv == iKhmer:
			makeUnits(iPlayer, iSwordsman, tPlot, 3)
			makeUnits(iPlayer, iBallistaElephant, tPlot, 2)
		elif iCiv == iIndonesia:
			makeUnits(iPlayer, iSwordsman, tPlot, 2)
			makeUnit(iPlayer, iWarElephant, tPlot)
		elif iCiv == iMoors:
			makeUnits(iPlayer, iCamelArcher, tPlot, 2)
		elif iCiv == iSpain:
			makeUnits(iPlayer, iCrossbowman, tPlot, 3)
			makeUnits(iPlayer, iSwordsman, tPlot, 3)
		elif iCiv == iFrance:
			makeUnits(iPlayer, iCrossbowman, tPlot, 3)
			makeUnits(iPlayer, iSwordsman, tPlot, 3)
		elif iCiv == iEngland:
			makeUnits(iPlayer, iCrossbowman, tPlot, 3)
			makeUnits(iPlayer, iSwordsman, tPlot, 3)
		elif iCiv == iHolyRome:
			makeUnits(iPlayer, iCrossbowman, tPlot, 3)
			makeUnits(iPlayer, iSwordsman, tPlot, 3)
		elif iCiv == iRussia:
			makeUnits(iPlayer, iCrossbowman, tPlot, 2)
			makeUnits(iPlayer, iSwordsman, tPlot, 2)
			makeUnits(iPlayer, iHorseArcher, tPlot, 2)
		elif iCiv == iNetherlands:
			makeUnits(iPlayer, iMusketeer, tPlot, 3)
			makeUnits(iPlayer, iPikeman, tPlot, 3)
		elif iCiv == iMali:
			makeUnits(iPlayer, iKelebolo, tPlot, 4)
			makeUnits(iPlayer, iSwordsman, tPlot, 3)
		elif iCiv == iOttomans:
			makeUnits(iPlayer, iCrossbowman, tPlot, 3)
			makeUnits(iPlayer, iHorseArcher, tPlot, 3)
		elif iCiv == iPoland:
			makeUnits(iPlayer, iLancer, tPlot, 2)
			makeUnits(iPlayer, iCrossbowman, tPlot, 2)
		elif iCiv == iPortugal:
			makeUnits(iPlayer, iCrossbowman, tPlot, 3)
			makeUnits(iPlayer, iPikeman, tPlot, 3)
		elif iCiv == iInca:
			makeUnits(iPlayer, iAucac, tPlot, 5)
			makeUnits(iPlayer, iArcher, tPlot, 3)
		elif iCiv == iItaly:
			makeUnits(iPlayer, iLancer, tPlot, 2)
		elif iCiv == iMongols:
			makeUnits(iPlayer, iCrossbowman, tPlot, 2)
			makeUnits(iPlayer, iMangudai, tPlot, 2)
			makeUnits(iPlayer, iKeshik, tPlot, 4)
		elif iCiv == iAztecs:
			makeUnits(iPlayer, iJaguar, tPlot, 5)
			makeUnits(iPlayer, iArcher, tPlot, 3)
		elif iCiv == iMughals:
			makeUnits(iPlayer, iSiegeElephant, tPlot, 2)
			makeUnits(iPlayer, iHorseArcher, tPlot, 4)
		elif iCiv == iThailand:
			makeUnits(iPlayer, iPikeman, tPlot, 2)
			makeUnits(iPlayer, iChangSuek, tPlot, 2)
		elif iCiv == iCongo:
			makeUnits(iPlayer, iPombos, tPlot, 3)
		elif iCiv == iGermany:
			makeUnits(iPlayer, iFusilier, tPlot, 5)
			makeUnits(iPlayer, iBombard, tPlot, 3)
		elif iCiv == iAmerica:
			makeUnits(iPlayer, iGrenadier, tPlot, 3)
			makeUnits(iPlayer, iMinuteman, tPlot, 3)
			makeUnits(iPlayer, iCannon, tPlot, 3)
		elif iCiv == iArgentina:
			makeUnits(iPlayer, iRifleman, tPlot, 2)
			makeUnits(iPlayer, iGrenadierCavalry, tPlot, 4)
		elif iCiv == iBrazil:
			makeUnits(iPlayer, iGrenadier, tPlot, 2)
			makeUnits(iPlayer, iRifleman, tPlot, 3)
			makeUnits(iPlayer, iCannon, tPlot, 2)
		elif iCiv == iCanada:
			makeUnits(iPlayer, iCavalry, tPlot, 2)
			makeUnits(iPlayer, iRifleman, tPlot, 4)
			makeUnits(iPlayer, iCannon, tPlot, 2)

	def createStartingUnits(self, iPlayer, tPlot):
		iCiv = civ(iPlayer)
	
		if iCiv == iChina:
			createSettlers(iPlayer, 1)
			makeUnit(iPlayer, iArcher, tPlot)
			makeUnit(iPlayer, iMilitia, tPlot)
		elif iCiv == iIndia:
			createSettlers(iPlayer, 1)
			makeUnit(iPlayer, iArcher, tPlot)
			makeUnit(iPlayer, iSpearman, tPlot)
			makeUnit(iPlayer, iLightSwordsman, tPlot)
			makeUnit(iPlayer, iChariot, tPlot)
		elif iCiv == iGreece:
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
		elif iCiv == iPersia:
			createSettlers(iPlayer, 3)
			makeUnits(iPlayer, iArcher, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iImmortal, tPlot, 4)
			makeUnits(iPlayer, iHorseman, tPlot, 2)
			makeUnit(iPlayer, iWarElephant, tPlot)
		elif iCiv == iCarthage:
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
		elif iCiv == iPolynesia:
			tSeaPlot = (4, 19)
			makeUnit(iPlayer, iSettler, tPlot)
			makeUnit(iPlayer, iWaka, tSeaPlot)
			makeUnit(iPlayer, iSettler, tSeaPlot)
			makeUnit(iPlayer, iWorkboat, tSeaPlot)
		elif iCiv == iRome:
			createSettlers(iPlayer, 3)
			makeUnits(iPlayer, iArcher, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iLegion, tPlot, 4)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
				makeUnits(iPlayer, iGalley, tSeaPlot, 2, UnitAITypes.UNITAI_ASSAULT_SEA)
		elif iCiv == iMaya:
			createSettlers(iPlayer, 1)
			makeUnits(iPlayer, iHolkan, tPlot, 2)
		elif iCiv == iJapan:
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
		elif iCiv == iTamils:
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
		elif iCiv == iEthiopia:
			createSettlers(iPlayer, 2)
			makeUnits(iPlayer, iArcher, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnit(iPlayer, iShotelai, tPlot)
			makeUnit(iPlayer, iLightSwordsman, tPlot)
			
			tSeaPlot = (74, 29)
			makeUnit(iPlayer, iWorkboat, tSeaPlot)
			makeUnit(iPlayer, iWarGalley, tSeaPlot)
		elif iCiv == iKorea:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iArcher, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnit(iPlayer, iSwordsman, tPlot)
			makeUnit(iPlayer, iHorseman, tPlot)
			
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iSpearman, tPlot, 2)
				makeUnits(iPlayer, iCrossbowman, tPlot, 2)
		elif iCiv == iByzantium:
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
		elif iCiv == iVikings:
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
		elif iCiv == iTurks:
			createSettlers(iPlayer, 6)
			if player(iPlayer).isHuman():
				makeUnits(iPlayer, iArcher, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			else:
				makeUnits(iPlayer, iCrossbowman, tPlot, 4, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iOghuz, tPlot, 6)
			makeUnit(iPlayer, iScout, tPlot)
		elif iCiv == iArabia:
			createSettlers(iPlayer, 2)
			makeUnit(iPlayer, iArcher, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iMobileGuard, tPlot, 2)
			makeUnits(iPlayer, iGhazi, tPlot, 2)
			makeUnit(iPlayer, iWorker, tPlot)
			
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
		elif iCiv == iTibet:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iArcher, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iKhampa, tPlot, 2)
		elif iCiv == iKhmer:
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
		elif iCiv == iIndonesia:
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
		elif iCiv == iMoors:
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
			
			if civ() in [iSpain, iMoors]:
				makeUnit(iPlayer, iCrossbowman, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
		elif iCiv == iSpain:
			iSpanishSettlers = 2
			if not player(iPlayer).isHuman(): iSpanishSettlers = 3
			createSettlers(iPlayer, iSpanishSettlers)
			createMissionaries(iPlayer, 1)
			makeUnit(iPlayer, iCrossbowman, tPlot)
			makeUnit(iPlayer, iCrossbowman, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iSwordsman, tPlot, 4)
			
			# TODO: should be isCivEnabled
			if data.isCivEnabled(iMoors):
				if not player(iMoors).isHuman():
					makeUnits(iPlayer, iLancer, tPlot, 2)
			else:
				makeUnit(iPlayer, iSettler, tPlot)
				
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iCrossbowman, tPlot, 2)
				
			if scenario() == i600AD: #late start condition
				makeUnit(iPlayer, iWorker, tPlot) #there is no carthaginian city in Iberia and Portugal may found 2 cities otherwise (a settler is too much)
		elif iCiv == iFrance:
			createSettlers(iPlayer, 3)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iCrossbowman, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iHeavySpearman, tPlot, 2)
			makeUnits(iPlayer, iSwordsman, tPlot, 3)
		elif iCiv == iEngland:
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
		elif iCiv == iHolyRome:
			createSettlers(iPlayer, 3)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iCrossbowman, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iSwordsman, tPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iLancer, tPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iCatapult, tPlot, 4, UnitAITypes.UNITAI_ATTACK_CITY)
		elif iCiv == iRussia:
			createSettlers(iPlayer, 4)
			makeUnits(iPlayer, iCrossbowman, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iHorseArcher, tPlot, 4)
		elif iCiv == iNetherlands:
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
		elif iCiv == iMali:
			createSettlers(iPlayer, 3)
			createMissionaries(iPlayer, 2)
			makeUnits(iPlayer, iKelebolo, tPlot, 5)
		elif iCiv == iPoland:
			iNumSettlers = 1
			if player(iPlayer).isHuman(): iNumSettlers = 2
			createSettlers(iPlayer, iNumSettlers)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iCrossbowman, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iHeavySwordsman, tPlot, 2)
			makeUnits(iPlayer, iLancer, tPlot, 2)
			
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iHeavySpearman, tPlot, 2)
		elif iCiv == iOttomans:
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
		elif iCiv == iPortugal:
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
		elif iCiv == iInca:
			createSettlers(iPlayer, 1)
			makeUnits(iPlayer, iAucac, tPlot, 4)
			makeUnits(iPlayer, iArcher, tPlot, 2)
			
			if not player(iPlayer).isHuman():
				makeUnit(iPlayer, iSettler, tPlot)
		elif iCiv == iItaly:
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
		elif iCiv == iMongols:
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
		elif iCiv == iAztecs:
			createSettlers(iPlayer, 2)
			makeUnits(iPlayer, iJaguar, tPlot, 4)
			makeUnits(iPlayer, iArcher, tPlot, 4, UnitAITypes.UNITAI_CITY_DEFENSE)
		elif iCiv == iMughals:
			createSettlers(iPlayer, 3)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iSiegeElephant, tPlot, 3)
			makeUnits(iPlayer, iHeavySwordsman, tPlot, 4).experience(2)
			makeUnits(iPlayer, iHorseArcher, tPlot, 2)
			
			if player(iPlayer).isHuman():
				makeUnits(iPlayer, iIslamicMissionary, tPlot, 3)
		elif iCiv == iThailand:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iHeavySpearman, tPlot, 3)
			makeUnits(iPlayer, iChangSuek, tPlot, 2)
		elif iCiv == iCongo:
			createSettlers(iPlayer, 1)
			makeUnits(iPlayer, iArcher, tPlot, 2)
			makeUnits(iPlayer, iPombos, tPlot, 2)
		elif iCiv == iGermany:
			createSettlers(iPlayer, 4)
			createMissionaries(iPlayer, 2)
			makeUnits(iPlayer, iArquebusier, tPlot, 3).experience(2)
			makeUnits(iPlayer, iArquebusier, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE).experience(2)
			makeUnits(iPlayer, iBombard, tPlot, 3).experience(2)
			
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iArquebusier, tPlot, 10).experience(2)
				makeUnits(iPlayer, iBombard, tPlot, 5).experience(2)
		elif iCiv == iAmerica:
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
		elif iCiv == iArgentina:
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
		elif iCiv == iBrazil:
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
		elif iCiv == iCanada:
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
	
		if iCiv == iIran:
			makeUnits(iPlayer, iQizilbash, tPlot, 6)
			makeUnits(iPlayer, iBombard, tPlot, 3)
			makeUnits(iPlayer, iWorker, tPlot, 3)
			
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iQizilbash, tPlot, 6)
				makeUnits(iPlayer, iBombard, tPlot, 3)
		elif iCiv == iMexico:
			makeUnits(iPlayer, iDragoon, tPlot, 4).experience(2)
			makeUnits(iPlayer, iMusketeer, tPlot, 5).experience(2)
			makeUnits(iPlayer, iGrenadier, tPlot, 2).experience(2)
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iColombia:
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
	
		if iCiv == iChina:
			makeUnit(iPlayer, iWorker, tPlot)
		elif iCiv == iIndia:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iGreece:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iPersia:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iCarthage:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iRome:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iMaya:
			makeUnit(iPlayer, iWorker, tPlot)
		elif iCiv == iJapan:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iTamils:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iEthiopia:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iKorea:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iByzantium:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iVikings:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iTurks:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iArabia:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iTibet:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iKhmer:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iIndonesia:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iMoors:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iSpain:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iFrance:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iEngland:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iHolyRome:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iRussia:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iNetherlands:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iMali:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iPoland:
			makeUnits(iPlayer, iWorker, tPlot, 3)
			
			if not player(iPlayer).isHuman():
				iRand = rand(5)
				if iRand == 0: tCityPlot = (65, 55) # Memel
				elif iRand == 1: tCityPlot = (65, 54) # Koenigsberg
				else: tCityPlot = (64, 54) # Gdansk
				
				makeUnit(iPlayer, iSettler, tCityPlot)
				makeUnit(iPlayer, iCrossbowman, tCityPlot)
		elif iCiv == iOttomans:
			makeUnits(iPlayer, iWorker, tPlot, 4)
		elif iCiv == iPortugal:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iInca:
			makeUnits(iPlayer, iWorker, tPlot, 4)
		elif iCiv == iItaly:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iMongols:
			makeUnits(iPlayer, iWorker, tPlot, 4)
		elif iCiv == iAztecs:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iMughals:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iThailand:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iCongo:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iGermany:
			makeUnits(iPlayer, iWorker, tPlot, 3)
		elif iCiv == iAmerica:
			makeUnits(iPlayer, iWorker, tPlot, 4)
		elif iCiv == iBrazil:
			makeUnits(iPlayer, iMadeireiro, tPlot, 3)
		elif iCiv == iArgentina:
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iCanada:
			makeUnits(iPlayer, iWorker, tPlot, 3)

	def create1700ADstartingUnits(self):

		# Japan
		capital = plots.capital(iJapan)
		if not player(iJapan).isHuman():
			makeUnit(iJapan, iSettler, capital)
		
		for iPlayer in players.major():
			iCiv = civ(iPlayer)
			if dBirth[iCiv] > scenarioStartYear() and player(iPlayer).isHuman():
				makeUnit(iPlayer, iSettler, plots.capital(iCiv))
				makeUnit(iPlayer, iMilitia, plots.capital(iCiv))

	def create600ADstartingUnits( self ):

		capital = plots.capital(iChina)
		makeUnits(iChina, iSwordsman, capital, 2)
		makeUnit(iChina, iArcher, capital)
		makeUnit(iChina, iSpearman, capital, UnitAITypes.UNITAI_CITY_DEFENSE)
		makeUnits(iChina, iChokonu, capital, 2)
		makeUnit(iChina, iHorseArcher, capital)
		makeUnits(iChina, iWorker, capital, 2)
		
		capital = plots.capital(iJapan)
		tSeaPlot = self.findSeaPlots(capital, 1, iJapan)
		if tSeaPlot:
			makeUnits(iJapan, iWorkboat, tSeaPlot, 2)
			
		if not player(iJapan).isHuman():
			makeUnits(iJapan, iCrossbowman, capital, 2)
			makeUnits(iJapan, iSamurai, capital, 3)

		capital = plots.capital(iByzantium)
		tSeaPlot = self.findSeaPlots(capital, 1, iByzantium)
		if tSeaPlot:
			makeUnits(iByzantium, iGalley, tSeaPlot, 2)
			makeUnits(iByzantium, iWarGalley, tSeaPlot, 2)

		capital = plots.capital(iVikings)
		tSeaPlot = self.findSeaPlots(capital, 1, iVikings)
		if tSeaPlot:
			makeUnit(iVikings, iWorkboat, tSeaPlot)
			if player(iVikings).isHuman():
				makeUnit(iVikings, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iVikings, iSettler, tSeaPlot)
				makeUnit(iVikings, iArcher, tSeaPlot)
				makeUnits(iVikings, iLongship, tSeaPlot, 2, UnitAITypes.UNITAI_EXPLORE_SEA)
			else:
				makeUnits(iVikings, iLongship, tSeaPlot, 3, UnitAITypes.UNITAI_EXPLORE_SEA)
				
		# start AI settler and garrison in Denmark and Sweden
		if not player(iVikings).isHuman():
			makeUnit(iVikings, iSettler, (60, 56))
			makeUnit(iVikings, iArcher, (60, 56))
			makeUnit(iVikings, iSettler, (63, 59))
			makeUnit(iVikings, iArcher, (63, 59))
		else:
			makeUnit(iVikings, iSettler, capital)
			makeUnits(iVikings, iArcher, capital, 2)

		capital = plots.capital(iKorea)
		if not player(iKorea).isHuman():
			makeUnits(iKorea, iHeavySwordsman, capital, 2)
				
		capital = plots.capital(iTurks)
		makeUnits(iTurks, iSettler, capital, 2)
		makeUnits(iTurks, iOghuz, capital, 6)
		makeUnit(iTurks, iArcher, capital)
		makeUnit(iTurks, iScout, capital)
			
		for iPlayer in players.major().human().before_birth():
			capital = plots.capital(iPlayer)
			makeUnit(iPlayer, iSettler, capital)
			makeUnit(iPlayer, iMilitia, capital)

	def create4000BCstartingUnits(self):
		for iPlayer in players.major():
			iCiv = civ(iPlayer)
			capital = plots.capital(iPlayer)
			
			if dBirth[iCiv] > scenarioStartYear() and player(iPlayer).isHuman():
				makeUnit(iPlayer, iSettler, capital)
				makeUnit(iPlayer, iMilitia, capital)
				
			if iCiv == iHarappa and (data.isCivEnabled(iCiv) or player(iPlayer).isHuman()):
				makeUnit(iPlayer, iCityBuilder, capital)
				makeUnit(iPlayer, iMilitia, capital)

	def assignTechs(self, iPlayer):
		Civilizations.initPlayerTechs(iPlayer)
				
		sta.onCivSpawn(iPlayer)

	def arabianSpawn(self):
		tBaghdad = (77, 40)
		tCairo = (69, 35)
		tMecca = (75, 33)

		bBaghdad = civ(plot(tBaghdad)) == iArabia
		bCairo = civ(plot(tCairo)) == iArabia
		
		lCities = []
		
		if bBaghdad: lCities.append(tBaghdad)
		if bCairo: lCities.append(tCairo)
		
		tCapital = random_entry(lCities)
		
		if tCapital:
			if not player(iArabia).isHuman():
				moveCapital(slot(iArabia), tCapital)
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

		if not player(iArabia).isHuman() and bBaghdad:
			makeUnits(iArabia, iSpearman, tBaghdad, 2)

	def germanSpawn(self):
		iPlayer = slot(iHolyRome)
	
		if stability(iPlayer) < iStabilityShaky: data.setStabilityLevel(iPlayer, iStabilityShaky)
			
		dc.nameChange(iPlayer)
		dc.adjectiveChange(iPlayer)

	def holyRomanSpawn(self):
		city = city_(60, 56)
		if city and player(iVikings).isAlive():
			city.setCulture(slot(iVikings), 5, True)

	def determineEnabledPlayers(self):
		iRand = infos.constant('PLAYER_OCCURRENCE_POLYNESIA')
		if iRand <= 0:
			data.setCivEnabled(iPolynesia, False)
		elif rand(iRand) != 0:
			data.setCivEnabled(iPolynesia, False)
			
		iRand = infos.constant('PLAYER_OCCURRENCE_HARAPPA')
		if iRand <= 0:
			data.setCivEnabled(iHarappa, False)
		elif rand(iRand) != 0:
			data.setCivEnabled(iHarappa, False)
		
		if not player(iIndia).isHuman() and not player(iIndonesia).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_TAMILS')
			
			if iRand <= 0:
				data.setCivPlayerEnabled(iTamils, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iTamils, False)
				
		if not player(iChina).isHuman() and not player(iIndia).isHuman() and not player(iMughals).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_TIBET')
			
			if iRand <= 0:
				data.setCivEnabled(iTibet, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iTibet, False)
				
		if not player(iSpain).isHuman() and not player(iMali).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_MOORS')
			
			if iRand <= 0:
				data.setCivEnabled(iMoors, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iMoors, False)
				
		if not player(iHolyRome).isHuman() and not player(iGermany).isHuman() and not player(iRussia).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_POLAND')
			
			if iRand <= 0:
				data.setCivEnabled(iPoland, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iPoland, False)
				
		if not player(iMali).isHuman() and not player(iPortugal).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_CONGO')
			
			if iRand <= 0:
				data.setCivEnabled(iCongo, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iCongo, False)
				
		if not player(iSpain).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_ARGENTINA')
			
			if iRand <= 0:
				data.setCivEnabled(iArgentina, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iArgentina, False)
				
		if not player(iPortugal).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_BRAZIL')
			
			if iRand <= 0:
				data.setCivEnabled(iBrazil, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iBrazil, False)

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
		coreCities = cities.core(iPlayer)
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