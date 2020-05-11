# Rhye's and Fall of Civilization - Main Scenario

from CvPythonExtensions import *
import CvUtil
from PyHelpers import PyPlayer
import Popup
from StoredData import data # edead
import CvTranslator
from RFCUtils import utils
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
from EnabledCivs import dSpawnTypes
import BugCore
MainOpt = BugCore.game.MainInterface

################
### Globals ###
##############

gc = CyGlobalContext()
localText = CyTranslator()

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
		popup.setText(localText.getText("TXT_KEY_INTERFACE_NEW_CIV_SWITCH", (gc.getPlayer(iPlayer).getCivilizationAdjective(0),)))
		popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popup.setOnClickedPythonCallback("applyNewCivSwitchEvent")
		
		popup.setData1(iPlayer)
		popup.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_EVENT_BULLET")).getPath())
		popup.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_EVENT_BULLET")).getPath())
		
		popup.addPopup(utils.getHumanID())
	
def applyNewCivSwitchEvent(argsList):
	iButton = argsList[0]
	iPlayer = argsList[1]
	
	if iButton == 1:
		handleNewCiv(iPlayer)
		
### Utility methods ###

def handleNewCiv(iPlayer):
	iPreviousPlayer = utils.getHumanID()
	iOldHandicap = gc.getActivePlayer().getHandicapType()
	
	pPlayer = gc.getPlayer(iPlayer)
	
	gc.getActivePlayer().setHandicapType(pPlayer.getHandicapType())
	gc.getGame().setActivePlayer(iPlayer, False)
	pPlayer.setHandicapType(iOldHandicap)
	
	for iMaster in range(iNumPlayers):
		if (gc.getTeam(pPlayer.getTeam()).isVassal(iMaster)):
			gc.getTeam(pPlayer.getTeam()).setVassal(iMaster, False, False)
	
	data.bAlreadySwitched = True
	gc.getPlayer(iPlayer).setPlayable(True)
	
	if gc.getGame().getWinner() == iPreviousPlayer:
		gc.getGame().setWinner(-1, -1)
	
	data.resetHumanStability()

	for city in utils.getCityList(iPlayer):
		city.setInfoDirty(True)
		city.setLayoutDirty(True)
					
	for i in range(3):
		data.players[iPlayer].lGoals[i] = -1
					
	if gc.getDefineINT("NO_AI_UHV_CHECKS") == 1:
		vic.loseAll(iPreviousPlayer)
		
	for iLoopPlayer in range(iNumPlayers):
		gc.getPlayer(iPlayer).setEspionageSpendingWeightAgainstTeam(iLoopPlayer, 0)

class RiseAndFall:

###############
### Popups ###
#############

	''' popupID has to be a registered ID in CvRhyesCatapultEventManager.__init__!! '''
	def showPopup(self, popupID, title, message, labels):
		popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setHeaderString(title)
		popup.setBodyString(message)
		for i in labels:
		    popup.addButton( i )
		popup.launch(False)

	def eventApply7614(self, popupReturn):
		iNewCiv = data.getNewCiv()
		if popupReturn.getButtonClicked() == 0: # 1st button
			self.handleNewCiv(iNewCiv)

	def scheduleFlipPopup(self, iNewCiv, lPlots):
		data.lTempEvents.append((iNewCiv, lPlots))
		self.checkFlipPopup()

	def checkFlipPopup(self):
		for tEvent in data.lTempEvents:
			iNewCiv, lPlots = tEvent
			self.flipPopup(iNewCiv, lPlots)

	def flipPopup(self, iNewCiv, lPlots):
		iHuman = utils.getHumanID()
		
		flipText = CyTranslator().getText("TXT_KEY_FLIPMESSAGE1", ())
		
		for city in self.getConvertedCities(iNewCiv, lPlots):
			flipText += city.getName() + "\n"
			
		flipText += CyTranslator().getText("TXT_KEY_FLIPMESSAGE2", ())
							
		self.showPopup(7615, CyTranslator().getText("TXT_KEY_NEWCIV_TITLE", ()), flipText, (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_NO", ())))
		data.iNewCivFlip = iNewCiv
		data.iOldCivFlip = iHuman
		data.lTempPlots = lPlots

	def eventApply7615(self, popupReturn):
		iHuman = utils.getHumanID()
		lPlots = data.lTempPlots
		iNewCivFlip = data.iNewCivFlip
		
		iNumCities = gc.getPlayer(iNewCivFlip).getNumCities()

		lHumanCityList = [city for city in self.getConvertedCities(iNewCivFlip, lPlots) if city.getOwner() == iHuman]
		
		if popupReturn.getButtonClicked() == 0: # 1st button
			print ("Flip agreed")
			CyInterface().addMessage(iHuman, True, iDuration, CyTranslator().getText("TXT_KEY_FLIP_AGREED", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
						
			if lHumanCityList:
				for city in lHumanCityList:
					tCity = (city.getX(), city.getY())
					print ("flipping ", city.getName())
					utils.cultureManager(tCity, 100, iNewCivFlip, iHuman, False, False, False)
					utils.flipUnitsInCityBefore(tCity, iNewCivFlip, iHuman)
					utils.flipCity(tCity, 0, 0, iNewCivFlip, [iHuman])
					utils.flipUnitsInCityAfter(tCity, iNewCivFlip)
					
			if iNumCities == 0 and gc.getPlayer(iNewCivFlip).getNumCities() > 0:
				self.createStartingWorkers(iNewCivFlip, (gc.getPlayer(iNewCivFlip).getCapitalCity().getX(), gc.getPlayer(iNewCivFlip).getCapitalCity().getY()))

			#same code as Betrayal - done just once to make sure human player doesn't hold a stack just outside of the cities
			for (x, y) in lPlots:
				betrayalPlot = gc.getMap().plot(x,y)
				if betrayalPlot.isCore(betrayalPlot.getOwner()) and not betrayalPlot.isCore(iNewCivFlip): continue
				iNumUnitsInAPlot = betrayalPlot.getNumUnits()
				if iNumUnitsInAPlot > 0:
					for iUnit in reversed(range(iNumUnitsInAPlot)):
						unit = betrayalPlot.getUnit(iUnit)
						if unit.getOwner() == iHuman:
							rndNum = gc.getGame().getSorenRandNum(100, 'betrayal')
							if rndNum >= iBetrayalThreshold:
								if unit.getDomainType() == DomainTypes.DOMAIN_LAND:
									iUnitType = unit.getUnitType()
									unit.kill(False, iNewCivFlip)
									utils.makeUnit(iUnitType, iNewCivFlip, (x,y), 1)


			if data.lCheatersCheck[0] == 0:
				data.lCheatersCheck[0] = iCheatersPeriod
				data.lCheatersCheck[1] = data.iNewCivFlip
				
		elif popupReturn.getButtonClicked() == 1: # 2nd button
			print ("Flip disagreed")
			CyInterface().addMessage(iHuman, True, iDuration, CyTranslator().getText("TXT_KEY_FLIP_REFUSED", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
						

			if lHumanCityList:
				for city in lHumanCityList:
					pPlot = gc.getMap().plot(city.getX(), city.getY())
					oldCulture = pPlot.getCulture(iHuman)
					pPlot.setCulture(iNewCivFlip, oldCulture/2, True)
					pPlot.setCulture(iHuman, oldCulture/2, True)
					data.iSpawnWar += 1
					if data.iSpawnWar == 1:
						gc.getTeam(gc.getPlayer(iNewCivFlip).getTeam()).declareWar(iHuman, False, -1) ##True??
						data.iBetrayalTurns = iBetrayalPeriod
						self.initBetrayal()
						
		data.lTempEvents.remove((iNewCivFlip, lPlots))
		
		gc.getGame().autosave()
				
	def rebellionPopup(self, iRebelCiv):
		self.showPopup(7622, CyTranslator().getText("TXT_KEY_REBELLION_TITLE", ()), \
				CyTranslator().getText("TXT_KEY_REBELLION_TEXT", (gc.getPlayer(iRebelCiv).getCivilizationAdjectiveKey(),)), \
				(CyTranslator().getText("TXT_KEY_POPUP_YES", ()), \
				CyTranslator().getText("TXT_KEY_POPUP_NO", ())))

	def eventApply7622(self, popupReturn):
		iHuman = utils.getHumanID()
		iRebelCiv = data.iRebelCiv
		if popupReturn.getButtonClicked() == 0: # 1st button
			gc.getTeam(gc.getPlayer(iHuman).getTeam()).makePeace(iRebelCiv)
		elif popupReturn.getButtonClicked() == 1: # 2nd button
			gc.getTeam(gc.getPlayer(iHuman).getTeam()).declareWar(iRebelCiv, False, -1)

	def eventApply7625(self, popupReturn):
		iHuman = utils.getHumanID()
		iPlayer, targetList = data.lTempEventList
		if popupReturn.getButtonClicked() == 0:
			for tPlot in targetList:
				x, y = tPlot
				if gc.getMap().plot(x, y).getPlotCity().getOwner() == iHuman:
					utils.colonialAcquisition(iPlayer, tPlot)
					gc.getPlayer(iHuman).changeGold(200)
		elif popupReturn.getButtonClicked() == 1:
			for tPlot in targetList:
				x, y = tPlot
				if gc.getMap().plot(x, y).getPlotCity().getOwner() == iHuman:
					utils.colonialConquest(iPlayer, tPlot)
		
	def eventApply7629(self, netUserData, popupReturn):
		targetList = data.lByzantineBribes
		iButton = popupReturn.getButtonClicked()
		
		if iButton >= len(targetList): return
		
		unit, iCost = targetList[iButton]
		closestCity = gc.getMap().findCity(unit.getX(), unit.getY(), iByzantium, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
		
		newUnit = utils.makeUnit(unit.getUnitType(), iByzantium, (closestCity.plot().getX(), closestCity.plot().getY()), 1)
		gc.getPlayer(iByzantium).changeGold(-iCost)
		unit.kill(False, iByzantium)
		
		if newUnit:
			CyInterface().selectUnit(newUnit, True, True, False)

#######################################
### Main methods (Event-Triggered) ###
#####################################  

	def setup(self):

		self.determineEnabledPlayers()
		
		self.initScenario()
		
		# Leoreth: make sure to select the Egyptian settler
		# 1SDAN: AI Egypt starts with an Archer
		x, y = Areas.getCapital(iEgypt)
		plotEgypt = gc.getMap().plot(x, y)
		for i in range(plotEgypt.getNumUnits()):
			if pEgypt.isHuman(): 
				unit = plotEgypt.getUnit(i)
				if unit.getUnitType() == iArcher:
					unit.kill(False, -1)
				if unit.getUnitType() == iSettler:
					CyInterface().selectUnit(unit, True, False, False)
			else:
				unit = plotEgypt.getUnit(i)
				if unit.getUnitType() == iMilitia:
					unit.kill(False, -1)
					
	def initScenario(self):
		self.updateStartingPlots()
	
		self.adjustCityCulture()
		
		self.updateGreatWall()
			
		self.foundCapitals()
		self.flipStartingTerritory()
		
		self.adjustReligionFoundingDates()
		self.initStartingReligions()
		
		Civilizations.initScenarioTechs(utils.getScenario())
	
		if utils.getScenario() == i3000BC:
			self.create4000BCstartingUnits()
			
		if utils.getScenario() == i600AD:
			self.create600ADstartingUnits()
			self.adjust600ADWonders()
			self.adjust600ADGreatPeople()
			
		if utils.getScenario() == i1700AD:
			self.create1700ADstartingUnits()
			self.init1700ADDiplomacy()
			self.prepareColonists()
			self.adjust1700ADCulture()
			self.adjust1700ADWonders()
			self.adjust1700ADGreatPeople()
			
			for iPlayer in [iIndia, iPersia, iSpain, iHolyRome, iOttomans, iManchuria, iKhmer, iKhazars]:
				utils.setReborn(iPlayer, True)
			
			pManchuria.updateTradeRoutes()
			
		for iPlayer in [iPlayer for iPlayer in range(iNumPlayers) if tBirth[iPlayer] < utils.getScenarioStartYear()]:
			data.players[iPlayer].bSpawned = True
		
		self.invalidateUHVs()
		
		gc.getGame().setVoteSourceReligion(1, iCatholicism, False)
		
		self.updateExtraOptions()
		
	def updateExtraOptions(self):
		# Human player can switch infinite times
		data.bUnlimitedSwitching = (gc.getDefineINT("UNLIMITED_SWITCHING") != 0)
		# No congresses
		data.bNoCongresses = (gc.getDefineINT("NO_CONGRESSES") != 0)
		# No plagues
		data.bNoPlagues = (gc.getDefineINT("NO_PLAGUES") != 0)
		
	def updateStartingPlots(self):
		for iPlayer in range(iNumPlayers):
			x, y = Areas.getCapital(iPlayer)
			gc.getPlayer(iPlayer).setStartingPlot(gc.getMap().plot(x, y), False)
		
	def adjustCityCulture(self):
		if utils.getTurns(10) == 10: return
	
		lCities = []
		for iPlayer in range(iNumTotalPlayersB):
			lCities.extend(utils.getCityList(iPlayer))
			
		for city in lCities:
			city.setCulture(city.getOwner(), utils.getTurns(city.getCulture(city.getOwner())), True)
			
	def updateGreatWall(self):
		if utils.getScenario() == i3000BC:
			return
	
		elif utils.getScenario() == i600AD:
			tTL = (98, 39)
			tBR = (107, 48)
			lExceptions = [(105, 48), (106, 48), (107, 48), (106, 47), (98, 46), (98, 47), (99, 47), (98, 48), (99, 48), (98, 39), (99, 39), (100, 39), (98, 40), (99, 40), (98, 41), (99, 41), (98, 42), (100, 40)]
			lAdditions = [(103, 38), (104, 37), (102, 49), (103, 49)]
				
		elif utils.getScenario() == i1700AD:
			tTL = (98, 40)
			tBR = (106, 50)
			lExceptions = [(98, 46), (98, 47), (98, 48), (98, 49), (99, 49), (98, 50), (99, 50), (100, 50), (99, 47), (99, 48), (100, 49), (101, 49), (101, 50), (102, 50)]
			lAdditions = [(104, 51), (105, 51), (106, 51), (107, 41), (107, 42), (107, 43), (103, 38), (103, 39), (104, 39), (105, 39), (104, 37)]
			
			lRemoveWall = [(97, 40), (98, 39), (99, 39), (100, 39), (101, 39), (102, 39)]
			
			for tPlot in lRemoveWall:
				x, y = tPlot
				gc.getMap().plot(x, y).setOwner(-1)
				
			gc.getMap().plot(102, 47).getPlotCity().updateGreatWall()
			
			for tPlot in lRemoveWall:
				x, y = tPlot
				gc.getMap().plot(x, y).setOwner(iManchuria)
		
		for (x, y) in utils.getPlotList(tTL, tBR, lExceptions):
			plot = gc.getMap().plot(x, y)
			if not plot.isWater(): plot.setWithinGreatWall(True)
					
		for (x, y) in lAdditions:
			plot = gc.getMap().plot(x, y)
			if not plot.isWater(): plot.setWithinGreatWall(True)
			
			
	def adjust1700ADCulture(self):
		for (x, y) in utils.getWorldPlotsList():
			plot = gc.getMap().plot(x, y)
			if plot.getOwner() != -1:
				plot.changeCulture(plot.getOwner(), 100, True)
				utils.convertPlotCulture(plot, plot.getOwner(), 100, True)
					
		for x, y in [(48, 45), (50, 44), (50, 43), (50, 42), (49, 40)]:
			utils.convertPlotCulture(gc.getMap().plot(x, y), iPortugal, 100, True)
			
		for x, y in [(58, 49), (59, 49), (60, 49)]:
			utils.convertPlotCulture(gc.getMap().plot(x, y), iGermany, 100, True)
			
		for x, y in [(62, 51)]:
			utils.convertPlotCulture(gc.getMap().plot(x, y), iHolyRome, 100, True)
			
		for x, y in [(58, 52), (58, 53)]:
			utils.convertPlotCulture(gc.getMap().plot(x, y), iNetherlands, 100, True)
			
		for x, y in [(64, 53), (66, 55)]:
			utils.convertPlotCulture(gc.getMap().plot(x, y), iPoland, 100, True)
			
		for x, y in [(67, 58), (68, 59), (69, 56), (69, 54)]:
			utils.convertPlotCulture(gc.getMap().plot(x, y), iRussia, 100, True)
			
	def prepareColonists(self):
		for iPlayer in [iSpain, iFrance, iEngland, iPortugal, iNetherlands, iGermany, iVikings, iSweden]:
			data.players[iPlayer].iExplorationTurn = getTurnForYear(1700)
			
		data.players[iVikings].iColonistsAlreadyGiven = 1
		data.players[iSpain].iColonistsAlreadyGiven = 7
		data.players[iFrance].iColonistsAlreadyGiven = 3
		data.players[iEngland].iColonistsAlreadyGiven = 3
		data.players[iPortugal].iColonistsAlreadyGiven = 6
		data.players[iNetherlands].iColonistsAlreadyGiven = 4
		data.players[iSweden].iColonistsAlreadyGiven = 1
		
	def init1700ADDiplomacy(self):
		teamEngland.declareWar(iMughals, False, WarPlanTypes.WARPLAN_LIMITED)
		teamIndia.declareWar(iMughals, False, WarPlanTypes.WARPLAN_TOTAL)
	
	def changeAttitudeExtra(self, iPlayer1, iPlayer2, iValue):
		gc.getPlayer(iPlayer1).AI_changeAttitudeExtra(iPlayer2, iValue)
		gc.getPlayer(iPlayer2).AI_changeAttitudeExtra(iPlayer1, iValue)

	def invalidateUHVs(self):
		for iPlayer in range(iNumPlayers):
			if not gc.getPlayer(iPlayer).isPlayable():
				for i in range(3):
					data.players[iPlayer].lGoals[i] = 0
					
	def foundCapitals(self):
		if utils.getScenario() == i600AD:
		
			# China
			self.prepareChina()
			tCapital = Areas.getCapital(iChina)
			lBuildings = [iPalace, iGranary, iConfucianTemple, iTaixue, iBarracks, iForge]
			utils.foundCapital(iChina, tCapital, "Xi'an", 4, 100, lBuildings, [iConfucianism, iTaoism])
			
		elif utils.getScenario() == i1700AD:
			
			# Chengdu
			pChengdu = gc.getMap().plot(99, 41).getPlotCity()
			pChengdu.setCulture(iManchuria, 100, True)

	def flipStartingTerritory(self):
	
		if utils.getScenario() == i600AD:
			
			# China
			tTL, tBR = Areas.tBirthArea[iChina]
			if utils.getHumanID() != iChina: tTL = (99, 39) # 4 tiles further south
			self.startingFlip(iChina, [(tTL, tBR)])
			
		if utils.getScenario() == i1700AD:
		
			# China (Tibet)
			tTibetTL = (94, 42)
			tTibetBR = (97, 45)
			tManchuriaTL = (105, 51)
			tManchuriaBR = (109, 55)
			self.startingFlip(iManchuria, [(tTibetTL, tTibetBR), (tManchuriaTL, tManchuriaBR)])
			
			# Russia (Sankt Peterburg)
			utils.convertPlotCulture(gc.getMap().plot(68, 58), iRussia, 100, True)
			utils.convertPlotCulture(gc.getMap().plot(67, 57), iRussia, 100, True)
			
			
	def startingFlip(self, iPlayer, lRegionList):
	
		for tuple in lRegionList:
			tTL = tuple[0]
			tBR = tuple[1]
			tExceptions = ()
			if len(tuple) > 2: tExceptions = tuple[2]
			self.convertSurroundingCities(iPlayer, utils.getPlotList(tTL, tBR, tExceptions))
			self.convertSurroundingPlotCulture(iPlayer, utils.getPlotList(tTL, tBR, tExceptions))


	def prepareChina(self):
		pGuiyang = gc.getMap().plot(102, 41)
		pGuiyang.getPlotCity().kill()
		pGuiyang.setImprovementType(-1)
		pGuiyang.setRouteType(-1)
		pGuiyang.setFeatureType(iForest, 0)

		if utils.getScenario() == i600AD:
			pXian = gc.getMap().plot(100, 44)
			pXian.getPlotCity().kill()
			pXian.setImprovementType(-1)
			pXian.setRouteType(-1)
			pXian.setFeatureType(iForest, 0)
			
		elif utils.getScenario() == i1700AD:
			pBeijing = gc.getMap().plot(tBeijing[0], tBeijing[1])
			pBeijing.getPlotCity().kill()
			pBeijing.setImprovementType(-1)
			pBeijing.setRouteType(-1)

		tCultureRegionTL = (98, 37)
		tCultureRegionBR = (109, 49)
		for (x, y) in utils.getPlotList(tCultureRegionTL, tCultureRegionBR):
			pPlot = gc.getMap().plot(x, y)
			bCity = False
			for (i, j) in utils.surroundingPlots((x, y)):
				loopPlot = gc.getMap().plot(i, j)
				if loopPlot.isCity():
					bCity = True
					loopPlot.getPlotCity().setCulture(iIndependent2, 0, False)
			if bCity:
				pPlot.setCulture(iIndependent2, 1, True)
			else:
				pPlot.setCulture(iIndependent2, 0, True)
				pPlot.setOwner(-1)
					
		pIndependent.found(99, 41)
		utils.makeUnit(iArcher, iIndependent, (99, 41), 1)
		pChengdu = gc.getMap().plot(99, 41).getPlotCity()
		pChengdu.setName("Chengdu", False)
		pChengdu.setPopulation(2)
		pChengdu.setHasReligion(iConfucianism, True, False, False)
		pChengdu.setHasRealBuilding(iGranary, True)
		pChengdu.setHasRealBuilding(iDujiangyan, True)
		
		if utils.getScenario() == i600AD:
			pBarbarian.found(105, 49)
			utils.makeUnit(iArcher, iBarbarian, (105, 49), 1)
			pShenyang = gc.getMap().plot(105, 49).getPlotCity()
			pShenyang.setName("Simiyan hoton", False)
			pShenyang.setPopulation(2)
			pShenyang.setHasReligion(iConfucianism, True, False, False)
			pShenyang.setHasRealBuilding(iGranary, True)
			pShenyang.setHasRealBuilding(iWalls, True)
			pShenyang.setHasRealBuilding(iConfucianTemple, True)
			
	def adjust600ADWonders(self):
		lExpiredWonders = [iOracle, iIshtarGate, iTerracottaArmy, iHangingGardens, iGreatCothon, iApadanaPalace, iColossus, iStatueOfZeus, iGreatMausoleum, iTempleOfArtemis, iAquaAppia, iAlKhazneh, iJetavanaramaya]
		self.expireWonders(lExpiredWonders)
		
		pBeijing = gc.getMap().plot(102, 47).getPlotCity()
		pBeijing.setBuildingOriginalOwner(iTaoistShrine, iChina)
		pBeijing.setBuildingOriginalOwner(iGreatWall, iChina)
		
		pNanjing = gc.getMap().plot(105, 43).getPlotCity()
		pNanjing.setBuildingOriginalOwner(iConfucianShrine, iChina)
		
		pPataliputra = gc.getMap().plot(94, 40).getPlotCity()
		pPataliputra.setBuildingOriginalOwner(iHinduShrine, iIndia)
		pPataliputra.setBuildingOriginalOwner(iBuddhistShrine, iIndia)
		
		pSirajis = gc.getMap().plot(82, 38).getPlotCity()
		pSirajis.setBuildingOriginalOwner(iZoroastrianShrine, iPersia)
		
		pAlexandria = gc.getMap().plot(67, 36).getPlotCity()
		pAlexandria.setBuildingOriginalOwner(iGreatLighthouse, iEgypt)
		pAlexandria.setBuildingOriginalOwner(iGreatLibrary, iEgypt)
		
		pMemphis = gc.getMap().plot(69, 35).getPlotCity()
		pMemphis.setBuildingOriginalOwner(iPyramids, iEgypt)
		pMemphis.setBuildingOriginalOwner(iGreatSphinx, iEgypt)
		
		pAthens = gc.getMap().plot(67, 41).getPlotCity()
		pAthens.setBuildingOriginalOwner(iParthenon, iGreece)
		
		pRome = gc.getMap().plot(60, 44).getPlotCity()
		pRome.setBuildingOriginalOwner(iFlavianAmphitheatre, iRome)
		
		pChichenItza = gc.getMap().plot(23, 37).getPlotCity()
		pChichenItza.setBuildingOriginalOwner(iTempleOfKukulkan, iMaya)
		
	def adjust1700ADWonders(self):
		lExpiredWonders = [iOracle, iIshtarGate, iHangingGardens, iGreatCothon, iApadanaPalace, iColossus, iStatueOfZeus, iGreatMausoleum, iTempleOfArtemis, iAquaAppia, iAlKhazneh, iJetavanaramaya, iGreatLighthouse, iMoaiStatues, iFlavianAmphitheatre, iGreatLibrary, iGondeshapur, iSilverTreeFountain, iAlamut, iWatPreahPisnulok]
		self.expireWonders(lExpiredWonders)
	
		pMilan = gc.getMap().plot(59, 47).getPlotCity()
		pMilan.setBuildingOriginalOwner(iSantaMariaDelFiore, iItaly)
		pMilan.setBuildingOriginalOwner(iSanMarcoBasilica, iItaly)
		
		pDjenne = gc.getMap().plot(51, 29).getPlotCity()
		pDjenne.setBuildingOriginalOwner(iUniversityOfSankore, iMali)
		
		pJerusalem = gc.getMap().plot(73, 38).getPlotCity()
		pJerusalem.setBuildingOriginalOwner(iJewishShrine, iIndependent)
		pJerusalem.setBuildingOriginalOwner(iOrthodoxShrine, iByzantium)
		pJerusalem.setBuildingOriginalOwner(iDomeOfTheRock, iArabia)
		
		pBaghdad = gc.getMap().plot(77, 40).getPlotCity()
		pBaghdad.setBuildingOriginalOwner(iSpiralMinaret, iArabia)
		
		pRome = gc.getMap().plot(60, 44).getPlotCity()
		pRome.setBuildingOriginalOwner(iFlavianAmphitheatre, iRome)
		pRome.setBuildingOriginalOwner(iSistineChapel, iItaly)
		
		pSeville = gc.getMap().plot(51, 41).getPlotCity()
		pSeville.setBuildingOriginalOwner(iMezquita, iMoors)
		
		pChichenItza = gc.getMap().plot(23, 37).getPlotCity()
		pChichenItza.setBuildingOriginalOwner(iTempleOfKukulkan, iMaya)
		
		pConstantinople = gc.getMap().plot(68, 45).getPlotCity()
		pConstantinople.setBuildingOriginalOwner(iTheodosianWalls, iByzantium)
		pConstantinople.setBuildingOriginalOwner(iHagiaSophia, iByzantium)
		
		pJakarta = gc.getMap().plot(104, 25).getPlotCity()
		pJakarta.setBuildingOriginalOwner(iBorobudur, iIndonesia)
		
		pMexicoCity = gc.getMap().plot(18, 37).getPlotCity()
		pMexicoCity.setBuildingOriginalOwner(iFloatingGardens, iAztecs)
		
		pCairo = gc.getMap().plot(69, 35).getPlotCity()
		pCairo.setBuildingOriginalOwner(iPyramids, iEgypt)
		pCairo.setBuildingOriginalOwner(iGreatSphinx, iEgypt)
		
		pAthens = gc.getMap().plot(67, 41).getPlotCity()
		pAthens.setBuildingOriginalOwner(iParthenon, iGreece)
		
		pShiraz = gc.getMap().plot(82, 38).getPlotCity()
		pShiraz.setBuildingOriginalOwner(iZoroastrianShrine, iPersia)
		
		pPataliputra = gc.getMap().plot(94, 40).getPlotCity()
		pPataliputra.setBuildingOriginalOwner(iHinduShrine, iIndia)
		pPataliputra.setBuildingOriginalOwner(iBuddhistShrine, iIndia)
		
		pMecca = gc.getMap().plot(75, 33).getPlotCity()
		pMecca.setBuildingOriginalOwner(iIslamicShrine, iArabia)
		
		pXian = gc.getMap().plot(100, 44).getPlotCity()
		pXian.setBuildingOriginalOwner(iTerracottaArmy, iChina)
		
		pKaifeng = gc.getMap().plot(103, 44).getPlotCity()
		pKaifeng.setBuildingOriginalOwner(iGrandCanal, iChina)
		pKaifeng.setBuildingOriginalOwner(iConfucianShrine, iChina)
		
		pShanghai = gc.getMap().plot(106, 44).getPlotCity()
		pShanghai.setBuildingOriginalOwner(iPorcelainTower, iChina)
		
		pBeijing = gc.getMap().plot(102, 47).getPlotCity()
		pBeijing.setBuildingOriginalOwner(iGreatWall, iChina)
		pBeijing.setBuildingOriginalOwner(iForbiddenPalace, iChina)
		pBeijing.setBuildingOriginalOwner(iTaoistShrine, iChina)
		
	def expireWonders(self, lWonders):
		for iWonder in lWonders:
			gc.getGame().incrementBuildingClassCreatedCount(gc.getBuildingInfo(iWonder).getBuildingClassType())
			
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
			gc.getPlayer(iPlayer).changeGreatPeopleCreated(iGreatPeople)
			
		for iPlayer, iGreatGenerals in dGreatGeneralsCreated.iteritems():
			gc.getPlayer(iPlayer).changeGreatGeneralsCreated(iGreatGenerals)
		
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
			iKhmer: 8,
			iCongo: 4,
			iNetherlands: 6,
			iBurma: 6,
			iNubia: 2,
			iChad: 4,
			iMoors: 2,
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
			gc.getPlayer(iPlayer).changeGreatPeopleCreated(iGreatPeople)
			
		for iPlayer, iGreatGenerals in dGreatGeneralsCreated.iteritems():
			gc.getPlayer(iPlayer).changeGreatGeneralsCreated(iGreatGenerals)

	def setupBirthTurnModifiers(self):
		for iCiv in range(iNumPlayers):
			if tBirth[iCiv] > -3000 and not gc.getPlayer(iCiv).isHuman():
				data.players[iCiv].iBirthTurnModifier = gc.getGame().getSorenRandNum(11, "BirthTurnModifier") - 5 # -5 to +5
		#now make sure that no civs spawn in the same turn and cause a double "new civ" popup
		for iCiv in range(utils.getHumanID()+1, iNumPlayers):
			for j in range(iNumPlayers-1-iCiv):
				iNextCiv = iCiv+j+1
				if getTurnForYear(tBirth[iCiv]) + data.players[iCiv].iBirthTurnModifier == getTurnForYear(tBirth[iNextCiv]) + data.players[iNextCiv].iBirthTurnModifier:
					data.players[iNextCiv].iBirthTurnModifier += 1
						
	def placeGoodyHuts(self):
			
		if utils.getScenario() == i3000BC:
			self.placeHut((101, 38), (107, 41)) # Southern China
			self.placeHut((62, 45), (67, 50)) # Balkans
			self.placeHut((69, 42), (76, 46)) # Asia Minor
		
		if utils.getScenario() <= i600AD:
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
			if gc.getGame().isReligionFounded(iReligion):
				gc.getGame().setReligionGameTurnFounded(iReligion, getTurnForYear(lReligionFoundingYears[iReligion]))
		
	def initStartingReligions(self):
	
		if utils.getScenario() == i600AD:
			utils.setStateReligionBeforeBirth(lCatholicStart, iCatholicism)
			utils.setStateReligionBeforeBirth(lProtestantStart, iCatholicism)
			
		elif utils.getScenario() == i1700AD:
			utils.setStateReligionBeforeBirth(lCatholicStart, iCatholicism)
			utils.setStateReligionBeforeBirth(lProtestantStart, iProtestantism)
			
	def checkTurn(self, iGameTurn):
	
		if pInuit.isAlive() and iInuit != utils.getHumanID():
			if gc.getGame().getGameTurn() in [getTurnForYear(1), getTurnForYear(500)]:
				utils.makeUnit(iArcher, iInuit, (4, 59), 1)
				utils.makeUnit(iDogSled, iInuit, (4, 59), 1)
				
			if pInuit.isAlive() and gc.getGame().getGameTurn() == getTurnForYear(900):
				utils.makeUnit(iArcher, iInuit, (27, 61), 1)
				utils.makeUnit(iDogSled, iInuit, (27, 61), 1)
				utils.makeUnit(iArcher, iInuit, (31, 58), 1)
				utils.makeUnit(iDogSled, iInuit, (31, 58), 1)
				
			if gc.getGame().getGameTurn() == getTurnForYear(1300):
				utils.makeUnit(iArcher, iInuit, (32, 63), 1)
				utils.makeUnit(iDogSled, iInuit, (32, 63), 1)
				
			if gc.getGame().getGameTurn() == getTurnForYear(1500):
				utils.makeUnit(iArcher, iInuit, (39, 61), 1)
				utils.makeUnit(iDogSled, iInuit, (39, 61), 1)
		
		# Leoreth: randomly place goody huts
		if iGameTurn == utils.getScenarioStartTurn()+3:
			self.placeGoodyHuts()
		
		if iGameTurn == getTurnForYear(tBirth[iSpain])-1:
			if utils.getScenario() == i600AD:
				pMassilia = gc.getMap().plot(56, 46)
				if pMassilia.isCity():
					pMassilia.getPlotCity().setCulture(pMassilia.getPlotCity().getOwner(), 1, True)

		# Leoreth: Turkey immediately flips independent cities in its core to avoid being pushed out of Anatolia
		if iGameTurn == data.iOttomanSpawnTurn + 1:
			cityPlotList = utils.getAreaCities(Areas.getBirthArea(iOttomans))
			for city in cityPlotList:
				tPlot = (city.getX(), city.getY())
				iOwner = city.getOwner()
				if iOwner in [iBarbarian, iIndependent, iIndependent2]:
					utils.flipCity(tPlot, False, True, iOttomans, ())
					utils.cultureManager(tPlot, 100, iOttomans, iOwner, True, False, False)
					self.convertSurroundingPlotCulture(iOttomans, utils.surroundingPlots(tPlot))
					utils.makeUnit(iLongbowman, iOttomans, tPlot, 1)
					
		#Trigger betrayal mode
		if data.iBetrayalTurns > 0:
			self.initBetrayal()

		if data.lCheatersCheck[0] > 0:
			teamPlayer = gc.getTeam(gc.getPlayer(utils.getHumanID()).getTeam())
			if (teamPlayer.isAtWar(data.lCheatersCheck[1])):
				print ("No cheaters!")
				self.initMinorBetrayal(data.lCheatersCheck[1])
				data.lCheatersCheck[0] = 0
				data.lCheatersCheck[1] = -1
			else:
				data.lCheatersCheck[0] -= 1

		if iGameTurn % utils.getTurns(20) == 0:
			if pIndependent.isAlive():
				utils.updateMinorTechs(iIndependent, iBarbarian)
			if pIndependent2.isAlive():
				utils.updateMinorTechs(iIndependent2, iBarbarian)

		if not pCeltia.isHuman():
			#1SDAN: give AI Celtia three Settlers in La Tene in 450BC
			if iGameTurn == getTurnForYear(-450) - (data.iSeed % 5):
				utils.makeUnit(iSettler, iCeltia, (57, 49), 3)
				utils.makeUnit(iArcher, iCeltia, (57, 49), 3)
				utils.makeUnit(iCidainh, iCeltia, (57, 49), 3)
				utils.makeUnit(iGallicWarrior, iCeltia, (57, 49), 3)
				
			#1SDAN: give AI Celtia a settler in England in 500BC
			if iGameTurn == getTurnForYear(-500) - (data.iSeed % 10):
				utils.makeUnit(iSettler, iCeltia, (53, 54), 1)
				utils.makeUnit(iArcher, iCeltia, (53, 54), 2)
				utils.makeUnit(iCidainh, iCeltia, (53, 54), 2)

		#1SDAN: Move Mississippi Capital and set them to be reborn in 800 AD
		if not pMississippi.isHuman() and iGameTurn == getTurnForYear(800) - (data.iSeed % 10):
			if gc.getMap().plot(Areas.getCapital(iMississippi, False)[0], Areas.getCapital(iMississippi, False)[1]).isCity():
				if gc.getMap().plot(Areas.getCapital(iMississippi, True)[0], Areas.getCapital(iMississippi, True)[1]).isCity():
					utils.moveCapital(iMississippi, (Areas.getCapital(iMississippi, True)[0], Areas.getCapital(iMississippi, True)[1]))
					utils.setReborn(iMississippi, True)
					dc.nameChange(iMississippi)
					dc.adjectiveChange(iMississippi)
				#1SDAN: Include all three Cahokia sites
				if gc.getMap().plot(Areas.getCapital(iMississippi, True)[0], Areas.getCapital(iMississippi, True)[1]+1).isCity():
					utils.moveCapital(iMississippi, (Areas.getCapital(iMississippi, True)[0], Areas.getCapital(iMississippi, True)[1]+1))
					utils.setReborn(iMississippi, True)
					dc.nameChange(iMississippi)
					dc.adjectiveChange(iMississippi)
				#1SDAN: Include all three Cahokia sites
				if gc.getMap().plot(Areas.getCapital(iMississippi, True)[0], Areas.getCapital(iMississippi, True)[1]+2).isCity():
					utils.moveCapital(iMississippi, (Areas.getCapital(iMississippi, True)[0], Areas.getCapital(iMississippi, True)[1]+2))
					utils.setReborn(iMississippi, True)
					dc.nameChange(iMississippi)
					dc.adjectiveChange(iMississippi)

		#Leoreth: give Phoenicia a settler in Qart-Hadasht in 820BC
		if not pCarthage.isHuman() and iGameTurn == getTurnForYear(-820) - (data.iSeed % 10):
			utils.makeUnit(iSettler, iCarthage, (58, 39), 1)
			utils.makeUnit(iArcher, iCarthage, (58, 39), 2)
			utils.makeUnit(iWorker, iCarthage, (58, 39), 2)
			utils.makeUnit(iWarElephant, iCarthage, (58, 39), 2)
			#1SDAN: give Phoenicia a Mine and Road on their Copper
			if gc.getMap().plot(73, 40).isCity():
				if gc.getMap().plot(73, 40).getPlotCity().getOwner() == iCarthage:
					gc.getMap().plot(71, 40).setRouteType(gc.getInfoTypeForString("ROUTE_ROAD"))
					gc.getMap().plot(71, 40).setImprovementType(gc.getInfoTypeForString("IMPROVEMENT_MINE"))
			
		if iGameTurn == getTurnForYear(476):
			if pItaly.isHuman() and pRome.isAlive():
				sta.completeCollapse(iRome)
				
		if iGameTurn == getTurnForYear(-50):
			if pByzantium.isHuman() and pGreece.isAlive():
				sta.completeCollapse(iGreece)
				
		if iGameTurn == getTurnForYear(tBirth[iIndia])-utils.getTurns(1):
			if pHarappa.isAlive() and not pHarappa.isHuman():
				sta.completeCollapse(iHarappa)
			
		if iGameTurn == getTurnForYear(-100):
			if pMamluks.isHuman() and pEgypt.isAlive():
				sta.completeCollapse(iEgypt)
			
		#Colonists
		if iGameTurn == getTurnForYear(-850):
			self.giveEarlyColonists(iGreece)
		elif iGameTurn == getTurnForYear(-700): # removed their colonists because of the Qart-Hadasht spawn
			self.giveEarlyColonists(iCarthage)
			
		elif iGameTurn == getTurnForYear(-600):
			self.giveEarlyColonists(iRome)
		elif iGameTurn == getTurnForYear(-400):
			self.giveEarlyColonists(iRome)

		if utils.isYearIn(860, 1250):
			if iGameTurn % utils.getTurns(10) == 9:
				self.giveRaiders(iVikings, Areas.getBroaderArea(iVikings))
		
		if utils.isYearIn(1350, 1918):
			for iPlayer in [iSpain, iEngland, iFrance, iPortugal, iNetherlands, iVikings, iGermany]:
				if iGameTurn == data.players[iPlayer].iExplorationTurn + 1 + data.players[iPlayer].iColonistsAlreadyGiven * 8:
					self.giveColonists(iPlayer)
					
		if iGameTurn == getTurnForYear(710)-1:
			x, y = 51, 37
			if gc.getMap().plot(x,y).isCity():
				marrakesh = gc.getMap().plot(x,y).getPlotCity()
				marrakesh.setHasReligion(iIslam, True, False, False)
				
				utils.makeUnit(iSettler, marrakesh.getOwner(), (x,y), 1)
				utils.makeUnit(iWorker, marrakesh.getOwner(), (x,y), 1)
				
		# Leoreth: help human with Aztec UHV - prevent super London getting in the way
		if iGameTurn == getTurnForYear(1500) and utils.getHumanID() == iAztecs:
			x, y = Areas.getCapital(iEngland)
			plot = gc.getMap().plot(x, y)
			if plot.isCity():
				city = plot.getPlotCity()
				if city.getPopulation() > 14:
					city.changePopulation(-3)
				
		# Leoreth: make sure Aztecs are dead in 1700 if a civ that spawns from that point is selected
		if iGameTurn == getTurnForYear(1700)-2:
			if utils.getHumanID() >= iGermany and pAztecs.isAlive():
				sta.completeCollapse(iAztecs)
				#utils.killAndFragmentCiv(iAztecs, iIndependent, iIndependent2, -1, False)
				
				
		for iLoopCiv in [iPlayer for iPlayer in range(iNumMajorPlayers) if tBirth[iPlayer] > utils.getScenarioStartYear()]:
			if iGameTurn >= getTurnForYear(tBirth[iLoopCiv]) - 2 and iGameTurn <= getTurnForYear(tBirth[iLoopCiv]) + 6:
				self.initBirth(iGameTurn, tBirth[iLoopCiv], iLoopCiv)



		if iGameTurn == getTurnForYear(600):
			if utils.getScenario() == i600AD:  #late start condition
				tTL, tBR = Areas.tBirthArea[iChina]
				if utils.getHumanID() != iChina: tTL = (99, 39) # 4 tiles further north
				lPlots = utils.getPlotList(tTL, tBR)
				iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iChina, lPlots)
				self.convertSurroundingPlotCulture(iChina, lPlots)
				utils.flipUnitsInArea(lPlots, iChina, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ   
				utils.flipUnitsInArea(lPlots, iChina, iIndependent, False, False) #remaining independents in the region now belong to the new civ   
				utils.flipUnitsInArea(lPlots, iChina, iIndependent2, False, False) #remaining independents in the region now belong to the new civ

				
		#kill the remaining barbs in the region: it's necessary to do this more than once to protect those civs
		for iPlayer in [iVikings, iSpain, iFrance, iHolyRome, iRussia, iAztecs]:
			if iGameTurn >= getTurnForYear(tBirth[iPlayer])+2 and iGameTurn <= getTurnForYear(tBirth[iPlayer])+utils.getTurns(10):
				utils.killUnitsInArea(iBarbarian, Areas.getBirthArea(iPlayer))
				
		#fragment utility
		if iGameTurn >= getTurnForYear(50) and iGameTurn % utils.getTurns(15) == 6:
			self.fragmentIndependents()
#		if (iGameTurn >= getTurnForYear(450) and iGameTurn % utils.getTurns(30) == 12):
#			self.fragmentBarbarians(iGameTurn)
			
		#fall of civs
		#if (iGameTurn >= getTurnForYear(200) and iGameTurn % utils.getTurns(4) == 0):
		#	self.collapseByBarbs(iGameTurn)
		#if (iGameTurn >= getTurnForYear(-2000) and iGameTurn % utils.getTurns(18) == 0): #used to be 15 in vanilla, because we must give some time for vassal states to form
		#	self.collapseGeneric(iGameTurn)
		#if (iGameTurn >= getTurnForYear(-2000) and iGameTurn % utils.getTurns(13) == 7): #used to be 8 in vanilla, because we must give some time for vassal states to form
		#	self.collapseMotherland(iGameTurn)
		#if (iGameTurn > getTurnForYear(300) and iGameTurn % utils.getTurns(10) == 6):
		#	self.secession(iGameTurn)

		if iGameTurn % utils.getTurns(10) == 5:
			sta.checkResurrection(iGameTurn)
			
		# Leoreth: check for scripted rebirths
		for iCiv in range(iNumPlayers):
			if iCiv in dRebirth:
				if iGameTurn == getTurnForYear(dRebirth[iCiv]) and not gc.getPlayer(iCiv).isAlive():
					self.rebirthFirstTurn(iCiv)
				if iGameTurn == getTurnForYear(dRebirth[iCiv])+1 and gc.getPlayer(iCiv).isAlive() and utils.isReborn(iCiv):
					self.rebirthSecondTurn(iCiv)
					
	def endTurn(self, iPlayer):
		for tTimedConquest in data.lTimedConquests:
			iConqueror, tPlot = tTimedConquest
			utils.colonialConquest(iConqueror, tPlot)
			
		if utils.getHumanID() == iPlayer:
			self.checkFlipPopup()
			
		data.lTimedConquests = []

	def rebirthFirstTurn(self, iCiv):
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		if iCiv in dRebirthCiv:
			pCiv.setCivilizationType(dRebirthCiv[iCiv])
		Modifiers.updateModifiers(iCiv)
		x, y = Areas.dRebirthPlot[iCiv]
		plot = gc.getMap().plot(x,y)
		
		# disable Mexico and Colombia
		if iCiv == iAztecs and gc.getDefineINT("PLAYER_REBIRTH_MEXICO") == 0: return
		if iCiv == iMaya and gc.getDefineINT("PLAYER_REBIRTH_COLOMBIA") == 0: return
		
		# reset contacts and make peace
		for iOtherCiv in range(iNumPlayers):
			if iCiv != iOtherCiv:
				teamCiv.makePeace(iOtherCiv)
				teamCiv.cutContact(iOtherCiv)
		
		# reset diplomacy
		pCiv.AI_reset()
		
		# reset player espionage weights
		gc.getPlayer(gc.getGame().getActivePlayer()).setEspionageSpendingWeightAgainstTeam(pCiv.getTeam(), 0)
		
		# reset great people
		pCiv.resetGreatPeopleCreated()
		
		# reset map visibility
		for (i, j) in utils.getWorldPlotsList():
			gc.getMap().plot(i, j).setRevealed(iCiv, False, True, -1)
		
		# assign new leader
		if iCiv in rebirthLeaders:
			if pCiv.getLeader() != rebirthLeaders[iCiv]:
				pCiv.setLeader(rebirthLeaders[iCiv])

		CyInterface().addMessage(gc.getGame().getActivePlayer(), True, iDuration, (CyTranslator().getText("TXT_KEY_INDEPENDENCE_TEXT", (pCiv.getCivilizationAdjectiveKey(),))), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
		utils.setReborn(iCiv, True)
		
		# Determine whether capital location is free
		bFree = True
		if not utils.isFree(iCiv, (x, y), True):
			bFree = False

		if plot.isUnit():
			bFree = False

		# if city present, flip it. If plot is free, found it. Else give settler.
		if plot.isCity():
			utils.completeCityFlip(x, y, iCiv, plot.getPlotCity().getOwner(), 100)
		else:
			utils.convertPlotCulture(plot, iCiv, 100, True)
			if bFree:
				pCiv.found(x,y)
			else:
				utils.makeUnit(iSettler, iCiv, (x, y), 1)
				
		# make sure there is a palace in the city
		if plot.isCity():
			capital = plot.getPlotCity()
			if not capital.hasBuilding(iPalace):
				capital.setHasRealBuilding(iPalace, True)
		
		self.createRespawnUnits(iCiv, (x, y))
		
		# for colonial civs, set dynamic state religion
		if iCiv in [iAztecs, iMaya]:
			self.setStateReligion(iCiv)

		self.assignTechs(iCiv)
		if gc.getGame().getGameTurn() >= getTurnForYear(tBirth[gc.getGame().getActivePlayer()]):
			startNewCivSwitchEvent(iCiv)

		gc.getPlayer(iCiv).setLatestRebellionTurn(getTurnForYear(dRebirth[iCiv]))

		# adjust gold, civics, religion and other special settings
		if iCiv == iPersia:
			pPersia.setGold(600)
			pPersia.setLastStateReligion(iIslam)
			pPersia.setCivics(iCivicsGovernment, iMonarchy)
			pPersia.setCivics(iCivicsLegitimacy, iVassalage)
			pPersia.setCivics(iCivicsSociety, iSlavery)
			pPersia.setCivics(iCivicsEconomy, iMerchantTrade)
			pPersia.setCivics(iCivicsReligion, iTheocracy)
		elif iCiv == iAztecs:
			if gc.getMap().plot(18, 37).isCity():
				city = gc.getMap().plot(18, 37).getPlotCity()
				if gc.getGame().getBuildingClassCreatedCount(gc.getBuildingInfo(iFloatingGardens).getBuildingClassType()) == 0:
					city.setHasRealBuilding(iFloatingGardens, True)
					
				iStateReligion = pAztecs.getStateReligion()
				if iStateReligion >= 0 and city.isHasReligion(iStateReligion):
					city.setHasRealBuilding(iMonastery + 4 * iStateReligion, True)
			
			cnm.updateCityNamesFound(iAztecs) # use name of the plots in their city name map
			
			pAztecs.setGold(500)
			
			pAztecs.setCivics(iCivicsGovernment, iDespotism)
			pAztecs.setCivics(iCivicsLegitimacy, iConstitution)
			pAztecs.setCivics(iCivicsSociety, iIndividualism)
			pAztecs.setCivics(iCivicsEconomy, iRegulatedTrade)
			pAztecs.setCivics(iCivicsReligion, iClergy)
			pAztecs.setCivics(iCivicsTerritory, iNationhood)
		elif iCiv == iMaya:
			pMaya.setGold(750)
			pMaya.setCivics(iCivicsGovernment, iDespotism)
			pMaya.setCivics(iCivicsLegitimacy, iConstitution)
			pMaya.setCivics(iCivicsSociety, iIndividualism)
			pMaya.setCivics(iCivicsEconomy, iRegulatedTrade)
			pMaya.setCivics(iCivicsReligion, iClergy)
			pMaya.setCivics(iCivicsTerritory, iNationhood)
			gc.getMap().plot(28, 31).setFeatureType(-1, 0)
		
		dc.onCivRespawn(iCiv, [])
		
	def rebirthSecondTurn(self, iCiv):
		lRebirthPlots = Areas.getRebirthArea(iCiv)
		
		# exclude American territory for Mexico
		lRemovedPlots = []
		if iCiv == iAztecs:
			for tPlot in lRebirthPlots:
				x, y = tPlot
				plot = gc.getMap().plot(x, y)
				if plot.getOwner() == iAmerica and tPlot not in Areas.getCoreArea(iAztecs, True):
					lRemovedPlots.append(tPlot)
					
		for tPlot in lRemovedPlots:
			lRebirthPlots.remove(tPlot)
		
		lCities = []
		for tPlot in lRebirthPlots:
			x, y = tPlot
			plot = gc.getMap().plot(x, y)
					
			if plot.isCity():
				lCities.append(plot.getPlotCity())
			
		# remove garrisons
		for city in lCities:
			if city.getOwner() != utils.getHumanID():
				tPlot = (city.getX(), city.getY())
				utils.relocateGarrisons(tPlot, city.getOwner())
				utils.relocateSeaGarrisons(tPlot, city.getOwner())
				#utils.createGarrisons(tPlot, iCiv)
				
		# convert cities
		iConvertedCities, iHumanCities = self.convertSurroundingCities(iCiv, lRebirthPlots)
		
		# create garrisons
		for city in lCities:
			if city.getOwner() == utils.getHumanID():
				x = city.getX()
				y = city.getY()
				utils.createGarrisons((x, y), iCiv, 1)
				
		# convert plot culture
		self.convertSurroundingPlotCulture(iCiv, lRebirthPlots)
		
		# reset plague
		data.players[iCiv].iPlagueCountdown = -10
		utils.clearPlague(iCiv)
		
		# adjust starting stability
		data.players[iCiv].resetStability()
		data.players[iCiv].iStabilityLevel = iStabilityStable
		if utils.getHumanID() == iCiv: data.resetHumanStability()
		
		# ask human player for flips
		if iHumanCities > 0 and iCiv != utils.getHumanID():
			self.scheduleFlipPopup(iCiv, lRebirthPlots)

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
				for city in utils.getCityList(iBigIndependent):
					iDivideCounter += 1 #convert 3 random cities cycling just once
					if iDivideCounter % 2 == 1:
						tPlot = (city.getX(), city.getY())
						utils.cultureManager(tPlot, 50, iSmallIndependent, iBigIndependent, False, True, True)
						utils.flipUnitsInCityBefore(tPlot, iSmallIndependent, iBigIndependent)
						utils.flipCity(tPlot, 0, 0, iSmallIndependent, [iBigIndependent])   #by trade because by conquest may raze the city
						utils.flipUnitsInCityAfter(tPlot, iSmallIndependent)
						iCounter += 1
						if iCounter == 3:
							return



	def fragmentBarbarians(self, iGameTurn):
		iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
		for j in range(iRndnum, iRndnum + iNumPlayers):
			iDeadCiv = j % iNumPlayers
			if not gc.getPlayer(iDeadCiv).isAlive() and iGameTurn > getTurnForYear(tBirth[iDeadCiv]) + utils.getTurns(50):
				pDeadCiv = gc.getPlayer(iDeadCiv)
				teamDeadCiv = gc.getTeam(pDeadCiv.getTeam())
				iCityCounter = 0
				for (x, y) in Areas.getNormalArea(iDeadCiv):
					pPlot = gc.getMap().plot( x, y )
					if pPlot.isCity():
						if pPlot.getPlotCity().getOwner() == iBarbarian:
							iCityCounter += 1
				if iCityCounter > 3:
					iDivideCounter = 0
					for (x, y) in Areas.getNormalArea(iDeadCiv):
						pPlot = gc.getMap().plot( x, y )
						if pPlot.isCity():
							city = pPlot.getPlotCity()
							if city.getOwner() == iBarbarian:
								if iDivideCounter % 4 == 0:
									iNewCiv = iIndependent
								elif iDivideCounter % 4 == 1:
									iNewCiv = iIndependent2
								if iDivideCounter % 4 == 0 or iDivideCounter % 4 == 1:
									tPlot = (city.getX(), city.getY())
									utils.cultureManager(tPlot, 50, iNewCiv, iBarbarian, False, True, True)
									utils.flipUnitsInCityBefore(tPlot, iNewCiv, iBarbarian)
									utils.flipCity(tPlot, 0, 0, iNewCiv, [iBarbarian])   #by trade because by conquest may raze the city
									utils.flipUnitsInCityAfter(tPlot, iNewCiv)
									iDivideCounter += 1
					return


	def secession(self, iGameTurn):
		iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
		for j in range(iRndnum, iRndnum + iNumPlayers):
			iPlayer = j % iNumPlayers
			if gc.getPlayer(iPlayer).isAlive() and iGameTurn >= getTurnForYear(tBirth[iPlayer]) + utils.getTurns(30):
				
				if data.getStabilityLevel(iPlayer) == iStabilityCollapsing:

					cityList = []
					for city in utils.getCityList(iPlayer):
						x = city.getX()
						y = city.getY()
						pPlot = gc.getMap().plot(x, y)

						if not city.isWeLoveTheKingDay() and not city.isCapital() and (x, y) != Areas.getCapital(iPlayer):
							if gc.getPlayer(iPlayer).getNumCities() > 0: #this check is needed, otherwise game crashes
								capital = gc.getPlayer(iPlayer).getCapitalCity()
								iDistance = utils.calculateDistance(x, y, capital.getX(), capital.getY())
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
						iNewCiv = iIndependent
						iRndNum = gc.getGame().getSorenRandNum(2, 'random independent')
						if iRndNum == 1:
							iNewCiv = iIndependent2
						if iPlayer in [iAztecs, iInca, iMaya, iEthiopia, iMali, iInuit]:
							if data.iCivsWithNationalism <= 0:
								iNewCiv = iNative
						splittingCity = utils.getRandomEntry(cityList)
						tPlot = (splittingCity.getX(), splittingCity.getY())
						utils.cultureManager(tPlot, 50, iNewCiv, iPlayer, False, True, True)
						utils.flipUnitsInCityBefore(tPlot, iNewCiv, iPlayer)
						utils.flipCity(tPlot, 0, 0, iNewCiv, [iPlayer])   #by trade because by conquest may raze the city
						utils.flipUnitsInCityAfter(tPlot, iNewCiv)
						if iPlayer == utils.getHumanID():
							CyInterface().addMessage(iPlayer, True, iDuration, splittingCity.getName() + " " + \
												CyTranslator().getText("TXT_KEY_STABILITY_SECESSION", ()), "", 0, "", ColorTypes(iOrange), -1, -1, True, True)
						
					return



	def initBirth(self, iCurrentTurn, iBirthYear, iCiv): # iBirthYear is really year now, so no conversion prior to function call - edead
		print 'init birth in: '+str(iBirthYear)
		iHuman = utils.getHumanID()
		iBirthYear = getTurnForYear(iBirthYear) # converted to turns here - edead
		
		iSpawnType = data.players[iCiv].iSpawnType
		if iSpawnType == iNoSpawn: return
		
		# if iCiv in lSecondaryCivs:
			# if iHuman != iCiv and not data.isPlayerEnabled(iCiv):
				# return
		
		lConditionalCivs = [iByzantium, iMamluks, iMughals, iOttomans, iThailand, iBrazil, iArgentina, iCanada, iItaly]
		
		if iSpawnType == iConditionalSpawn and iCiv in lConditionalCivs:
			# Leoreth: extra checks for conditional civs
			if iCiv == iByzantium:
				if not pRome.isAlive() or pGreece.isAlive() or (utils.getHumanID() == iRome and utils.getStabilityLevel(iRome) == iStabilitySolid):
					return
					
					
			elif iCiv == iOttomans:
				tMiddleEastTL = (69, 38)
				tMiddleEastBR = (78, 45)
				lCities = utils.getAreaCities(utils.getPlotList(tMiddleEastTL, tMiddleEastBR))
				
				if iTurks not in [city.getOwner() for city in lCities] and iTurks not in [city.getPreviousOwner() for city in lCities]:
					return
					
			elif iCiv == iMamluks:
				if pEgypt.isAlive():
					return
				
				if utils.getHumanID() != iArabia:
					if data.getStabilityLevel(iArabia) > iStabilityShaky:
						return
				else:
					if data.getStabilityLevel(iArabia) > iStabilityUnstable:
						return
					
			elif iCiv == iMaya and pMuisca.isAlive():
				return
						

			elif iCiv == iThailand:
				if utils.getHumanID() != iKhmer:
					if data.getStabilityLevel(iKhmer) > iStabilityShaky:
						return
				else:
					if data.getStabilityLevel(iKhmer) > iStabilityUnstable:
						return
						
			elif iCiv in [iArgentina, iBrazil]:
				iColonyPlayer = utils.getColonyPlayer(iCiv)
				if iColonyPlayer < 0: return
				elif iColonyPlayer not in [iArgentina, iBrazil]:
					if data.getStabilityLevel(iColonyPlayer) > iStabilityStable:
						return
						
			elif iCiv == iItaly:
				if pRome.isAlive():
					return
				
				cityList = utils.getCitiesInCore(iRome, False)
				
				iIndependentCities = 0

				for pCity in cityList:
					if not pCity.getOwner() < iNumPlayers:
						iIndependentCities += 1
						
				if iIndependentCities == 0:
					return
					
		elif iSpawnType == iForcedSpawn and iCiv in [iItaly, iMamluks]:
			if iCiv == iItaly:
				if pRome.isAlive():
					sta.completeCollapse(iRome)
			elif iCiv == iMamluks:
				if pEgypt.isAlive():
					sta.completeCollapse(iEgypt)
				
		tCapital = Areas.getCapital(iCiv)
				
		x, y = tCapital
		bCapitalSettled = False
		
		if iCiv in lCapitalStart:
			if gc.getMap().plot(x, y).isCity():
				bCapitalSettled = True
		
		if iCiv == iItaly:
			for (i, j) in utils.surroundingPlots(tCapital):
				if gc.getMap().plot(i, j).isCity():
					bCapitalSettled = True
					tCapital = (i, j)
					x, y = tCapital
					break

		if iCurrentTurn == iBirthYear-1 + data.players[iCiv].iSpawnDelay + data.players[iCiv].iFlipsDelay:
			if iCiv in lConditionalCivs or bCapitalSettled:
				utils.convertPlotCulture(gc.getMap().plot(x,y), iCiv, 100, True)

			reborn = utils.getReborn(iCiv)
			tTopLeft, tBottomRight = Areas.getBirthRectangle(iCiv)
			tBroaderTopLeft, tBroaderBottomRight = Areas.tBroaderArea[iCiv]
			
			if iCiv == iThailand:
				i, j = Areas.tCapitals[iKhmer]
				if gc.getMap().plot(i, j).isCity():
					angkor = gc.getMap().plot(i, j).getPlotCity()
					bWonder = False
					for iBuilding in range(iBeginWonders, iNumBuildings):
						if angkor.isHasRealBuilding(iBuilding):
							bWonder = True
							break
					if bWonder and utils.getHumanID() != iThailand:
						print "Thais flip Angkor instead to save its wonders."
						angkor.setName("Ayutthaya", False)
						tCapital = (x-1, y+1)
						x, y = tCapital
						gc.getMap().plot(x, y).setFeatureType(-1, 0)
						
				utils.setReborn(iKhmer, True)
				
				# Prey Nokor becomes Saigon
				if gc.getMap().plot(104, 33).isCity():
					gc.getMap().plot(104, 33).getPlotCity().setName("Saigon", False)
				
			# Exclude Sweden from Viking core
			elif iCiv == iSweden:
				utils.setReborn(iVikings, True)
				
			iPreviousOwner = gc.getMap().plot(x, y).getOwner()
				

			if data.players[iCiv].iFlipsDelay == 0: #city hasn't already been founded)
			
				#this may fix the -1 bug
				if iCiv == iHuman: 
					killPlot = gc.getMap().plot(x, y)
					iNumUnitsInAPlot = killPlot.getNumUnits()
					if iNumUnitsInAPlot > 0:
						for i in range(iNumUnitsInAPlot):
							unit = killPlot.getUnit(0)
							if unit.getOwner() != iCiv:
								unit.kill(False, iBarbarian)
				
				bBirthInCapital = False
				
				if (iCiv in lConditionalCivs and iCiv != iThailand) or bCapitalSettled:
					bBirthInCapital = True
				
				if iCiv == iOttomans:
					self.moveOutInvaders(tTopLeft, tBottomRight)  
					
				if bBirthInCapital:
					utils.makeUnit(iCatapult, iCiv, (0, 0), 1)
			
				bDeleteEverything = False
				pCapital = gc.getMap().plot(x, y)
				if pCapital.isOwned():
					if iCiv == iHuman or not gc.getPlayer(iHuman).isAlive():
						if not (pCapital.isCity() and pCapital.getPlotCity().isHolyCity()):
							bDeleteEverything = True
							print ("bDeleteEverything 1")
					else:
						bDeleteEverything = True
						for (i, j) in utils.surroundingPlots(tCapital):
							pPlot=gc.getMap().plot(i, j)
							if (pPlot.isCity() and (pPlot.getPlotCity().getOwner() == iHuman or pPlot.getPlotCity().isHolyCity())) or iCiv == iOttomans:
								bDeleteEverything = False
								print ("bDeleteEverything 2")
								break
				print ("bDeleteEverything", bDeleteEverything)
				if not gc.getMap().plot(x, y).isOwned():
					if iCiv in [iNetherlands, iPortugal, iByzantium, iKorea, iThailand, iItaly, iCarthage]: #dangerous starts
						data.lDeleteMode[0] = iCiv
					if bBirthInCapital:
						self.birthInCapital(iCiv, iPreviousOwner, tCapital, tTopLeft, tBottomRight)
					else:
						self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
				elif bDeleteEverything and not bBirthInCapital:
					for (i, j) in utils.surroundingPlots(tCapital):
						data.lDeleteMode[0] = iCiv
						pCurrent=gc.getMap().plot(i, j)
						for iLoopCiv in range(iNumTotalPlayers+1): #Barbarians as well
							if iCiv != iLoopCiv:
								utils.flipUnitsInArea(utils.getPlotList(tTopLeft, tBottomRight, utils.getOrElse(Areas.dBirthAreaExceptions, iCiv, [])), iCiv, iLoopCiv, True, False)
						if pCurrent.isCity():
							pCurrent.eraseAIDevelopment() #new function, similar to erase but won't delete rivers, resources and features()
						for iLoopCiv in range(iNumTotalPlayers+1): #Barbarians as well
							if iCiv != iLoopCiv:
								pCurrent.setCulture(iLoopCiv, 0, True)
						pCurrent.setOwner(-1)
					if bBirthInCapital:
						self.birthInCapital(iCiv, iPreviousOwner, tCapital, tTopLeft, tBottomRight)
					else:
						self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
				else:
					if bBirthInCapital:
						self.birthInCapital(iCiv, iPreviousOwner, tCapital, tTopLeft, tBottomRight)
					else:
						self.birthInForeignBorders(iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight)
						
				if bBirthInCapital:	
					utils.clearCatapult(iCiv)
						
			else:
				print ( "setBirthType again: flips" )
				self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
				
		# Leoreth: reveal all normal plots on spawn
		# 1SDAN: reveal birth plots for the celts
		if iCiv == iCeltia:
			for (x, y) in Areas.getBirthArea(iCiv):
				gc.getMap().plot(x, y).setRevealed(iCiv, True, True, 0)
		else:
			for (x, y) in Areas.getNormalArea(iCiv):
				gc.getMap().plot(x, y).setRevealed(iCiv, True, True, 0)
				
		# Leoreth: conditional state religion for colonial civs and Byzantium
		if iCiv in [iByzantium, iArgentina, iBrazil]:
			self.setStateReligion(iCiv)
			
		if (iCurrentTurn == iBirthYear + data.players[iCiv].iSpawnDelay) and (gc.getPlayer(iCiv).isAlive()) and (not data.bAlreadySwitched or utils.getReborn(iCiv) == 1 or data.bUnlimitedSwitching) and ((iHuman not in lNeighbours[iCiv] and getTurnForYear(tBirth[iCiv]) - getTurnForYear(tBirth[iHuman]) > 0) or getTurnForYear(tBirth[iCiv]) - getTurnForYear(tBirth[iHuman]) >= utils.getTurns(25) ):
			startNewCivSwitchEvent(iCiv)
			
		data.players[iCiv].bSpawned = True

	def moveOutInvaders(self, tTL, tBR):
		if pMongolia.isAlive():
			mongolCapital = pMongolia.getCapitalCity()
		for (x, y) in utils.getPlotList(tTL, tBR):
			plot = gc.getMap().plot(x, y)
			for i in range(plot.getNumUnits()):
				unit = plot.getUnit(i)
				if not utils.isDefenderUnit(unit):
					if unit.getOwner() == iMongolia:
						if utils.getHumanID() != iMongolia:
							unit.setXY(mongolCapital.getX(), mongolCapital.getY(), False, True, False)
					else:
						if unit.getUnitType() == iKeshik:
							unit.kill(False, iBarbarian)

	def deleteMode(self, iCurrentPlayer):
		iCiv = data.lDeleteMode[0]
		print ("deleteMode after", iCurrentPlayer)
		tCapital = Areas.getCapital(iCiv)
		x, y = tCapital
			
		
		if iCurrentPlayer == iCiv:
			if iCiv == iCarthage:
				for i in range(x - 2, x + 2): # from x-2 to x+1
					for j in range(y - 1, y + 2): # from y-1 to y+1
						pPlot=gc.getMap().plot(i, j)
						pPlot.setCulture(iCiv, 300, True)
			else:
				for (i, j) in utils.surroundingPlots(tCapital, 2):
					pPlot=gc.getMap().plot(i, j)
					pPlot.setCulture(iCiv, 300, True)
			for (i, j) in utils.surroundingPlots(tCapital):
				pPlot=gc.getMap().plot(i, j)
				utils.convertPlotCulture(pPlot, iCiv, 100, True)
				if pPlot.getCulture(iCiv) < 3000:
					pPlot.setCulture(iCiv, 3000, True) #2000 in vanilla/warlords, cos here Portugal is choked by spanish culture
				pPlot.setOwner(iCiv)
			data.lDeleteMode[0] = -1
			return
		    
		#print ("iCurrentPlayer", iCurrentPlayer, "iCiv", iCiv)
		if iCurrentPlayer != iCiv-1 and iCiv not in [iCarthage, iGreece]:
			return
		
		bNotOwned = True
		for (i, j) in utils.surroundingPlots(tCapital):
			#print ("deleting again", i, j)
			pPlot=gc.getMap().plot(i, j)
			if pPlot.isOwned():
				bNotOwned = False
				for iLoopCiv in range(iNumTotalPlayersB): #Barbarians as well
					if iLoopCiv != iCiv:
						pPlot.setCulture(iLoopCiv, 0, True)
				pPlot.setOwner(iCiv)
		
		for (i, j) in utils.surroundingPlots(tCapital, 15): # must include the distance from Sogut to the Caspius
			if (i, j) != tCapital:
				pPlot=gc.getMap().plot(i, j)
				if pPlot.isUnit() and not pPlot.isWater():
					unit = pPlot.getUnit(0)
					if unit.getOwner() == iCiv:
						print ("moving starting units from", i, j, "to", tCapital)
						for i in range(pPlot.getNumUnits()):
							unit = pPlot.getUnit(0)
							unit.setXY(x, y, False, True, False)
		
	def birthInFreeRegion(self, iCiv, tCapital, tTopLeft, tBottomRight):
		x, y = tCapital
		startingPlot = gc.getMap().plot(x, y)
		if data.players[iCiv].iFlipsDelay == 0:
			iFlipsDelay = data.players[iCiv].iFlipsDelay + 2
			if iFlipsDelay > 0:
				print ("starting units in", x, y)
				self.createStartingUnits(iCiv, tCapital)
				
				if iCiv == iOttomans:
					data.iOttomanSpawnTurn = gc.getGame().getGameTurn()
			
				if iCiv == iItaly:
					utils.removeCoreUnits(iItaly)
					cityList = utils.getCitiesInCore(iItaly, False)
					i, j = Areas.getCapital(iRome)
					pRomePlot = gc.getMap().plot(i, j)
					if pRomePlot.isCity():
						cityList.append(pRomePlot.getPlotCity())
					for city in cityList:
						if city.getPopulation() < 5: city.setPopulation(5)
						city.setHasRealBuilding(iGranary, True)
						city.setHasRealBuilding(iLibrary, True)
						city.setHasRealBuilding(iCourthouse, True)
						if city.isCoastal(20): city.setHasRealBuilding(iHarbor, True)
										
				lPlots = utils.surroundingPlots(tCapital, 3)
				utils.flipUnitsInArea(lPlots, iCiv, iBarbarian, True, True) #This is mostly for the AI. During Human player spawn, that area should be already cleaned			
				utils.flipUnitsInArea(lPlots, iCiv, iIndependent, True, False) #This is mostly for the AI. During Human player spawn, that area should be already cleaned			
				utils.flipUnitsInArea(lPlots, iCiv, iIndependent2, True, False) #This is mostly for the AI. During Human player spawn, that area should be already cleaned			
				self.assignTechs(iCiv)
				data.players[iCiv].iPlagueCountdown = -iImmunity
				utils.clearPlague(iCiv)
				data.players[iCiv].iFlipsDelay = iFlipsDelay #save
				

		else: #starting units have already been placed, now the second part
		
			iNumCities = gc.getPlayer(iCiv).getNumCities()
		
			lPlots = utils.getPlotList(tTopLeft, tBottomRight, Areas.getBirthExceptions(iCiv))
			iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, lPlots)
			self.convertSurroundingPlotCulture(iCiv, lPlots)
			utils.flipUnitsInArea(lPlots, iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ
			utils.flipUnitsInArea(lPlots, iCiv, iIndependent, False, False) #remaining independents in the region now belong to the new civ   
			utils.flipUnitsInArea(lPlots, iCiv, iIndependent2, False, False) #remaining independents in the region now belong to the new civ# starting workers
		
			# create starting workers
			if iNumCities == 0 and gc.getPlayer(iCiv).getNumCities() > 0:
				self.createStartingWorkers(iCiv, (gc.getPlayer(iCiv).getCapitalCity().getX(), gc.getPlayer(iCiv).getCapitalCity().getY()))
			
			if iCiv == iArabia:
				self.arabianSpawn()
				
			if iCiv == iGermany:
				self.germanSpawn()
   
			print ("utils.flipUnitsInArea()") 
			#cover plots revealed by the lion
			utils.clearCatapult(iCiv)

			if iNumHumanCitiesToConvert > 0 and iCiv != utils.getHumanID(): # Leoreth: quick fix for the "flip your own cities" popup, still need to find out where it comes from
				print "Flip Popup: free region"
				self.scheduleFlipPopup(iCiv, lPlots)
				

			
	def birthInForeignBorders(self, iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight):
		if iCiv == iItaly:
			utils.removeCoreUnits(iItaly)
			cityList = self.getCitiesInCore(iItaly, False)
			x, y = Areas.getCapital(iRome)
			pRomePlot = gc.getMap().plot(x, y)
			if pRomePlot.isCity():
				cityList.append(pRomePlot.getPlotCity())
			for pCity in cityList:
				if city.getPopulation() < 5: city.setPopulation(5)
				city.setHasRealBuilding(iGranary, True)
				city.setHasRealBuilding(iLibrary, True)
				city.setHasRealBuilding(iCourthouse, True)
				if city.isCoastal(20): city.setHasRealBuilding(iHarbor, True)
				
		iNumCities = gc.getPlayer(iCiv).getNumCities()
		
		lPlots = utils.getPlotList(tTopLeft, tBottomRight, Areas.getBirthExceptions(iCiv))
		iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, lPlots)
		self.convertSurroundingPlotCulture(iCiv, lPlots)
		
		# create starting workers
		if iNumCities == 0 and gc.getPlayer(iCiv).getNumCities() > 0:
			self.createStartingWorkers(iCiv, (gc.getPlayer(iCiv).getCapitalCity().getX(), gc.getPlayer(iCiv).getCapitalCity().getY()))

		#now starting units must be placed
		if iNumAICitiesConverted > 0:
			plotList = utils.squareSearch(tTopLeft, tBottomRight, utils.ownedCityPlots, iCiv)
			if plotList:
				tPlot = utils.getRandomEntry(plotList)
				if tPlot:
					self.createStartingUnits(iCiv, tPlot)
					self.assignTechs(iCiv)
					data.players[iCiv].iPlagueCountdown = -iImmunity
					utils.clearPlague(iCiv)
			utils.flipUnitsInArea(lPlots, iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ 
			utils.flipUnitsInArea(lPlots, iCiv, iIndependent, False, False) #remaining barbs in the region now belong to the new civ 
			utils.flipUnitsInArea(lPlots, iCiv, iIndependent2, False, False) #remaining barbs in the region now belong to the new civ
			
			if iCiv == iOttomans:
				data.iOttomanSpawnTurn = gc.getGame().getGameTurn()

		else:   #search another place
			plotList = utils.squareSearch(tTopLeft, tBottomRight, utils.goodPlots, [])
			if plotList:
				tPlot = utils.getRandomEntry(plotList)
				if tPlot:
					self.createStartingUnits(iCiv, tPlot)
					self.assignTechs(iCiv)
					data.players[iCiv].iPlagueCountdown = -iImmunity
					utils.clearPlague(iCiv)
			else:
				plotList = utils.squareSearch(tBroaderTopLeft, tBroaderBottomRight, utils.goodPlots, [])
			if plotList:
				tPlot = utils.getRandomEntry(plotList)
				if tPlot:
					self.createStartingUnits(iCiv, tPlot)
					#self.createStartingWorkers(iCiv, tPlot)
					self.assignTechs(iCiv)
					data.players[iCiv].iPlagueCountdown = -iImmunity
					utils.clearPlague(iCiv)
			utils.flipUnitsInArea(lPlots, iCiv, iBarbarian, True, True) #remaining barbs in the region now belong to the new civ 
			utils.flipUnitsInArea(lPlots, iCiv, iIndependent, True, False) #remaining barbs in the region now belong to the new civ 
			utils.flipUnitsInArea(lPlots, iCiv, iIndependent2, True, False) #remaining barbs in the region now belong to the new civ 

		if iNumHumanCitiesToConvert > 0:
			print "Flip Popup: foreign borders"
			self.scheduleFlipPopup(iCiv, lPlots)
			
		if iCiv == iGermany:
			self.germanSpawn()

	#Leoreth - adapted from SoI's birthConditional method by embryodead
	def birthInCapital(self, iCiv, iPreviousOwner, tCapital, tTopLeft, tBottomRight):
		iOwner = iPreviousOwner
		x, y = tCapital

		if data.players[iCiv].iFlipsDelay == 0:

			iFlipsDelay = data.players[iCiv].iFlipsDelay + 2

			if iFlipsDelay > 0:

				# flip capital instead of spawning starting units
				utils.flipCity(tCapital, False, True, iCiv, ())
				gc.getMap().plot(x, y).getPlotCity().setHasRealBuilding(iPalace, True)
				utils.convertPlotCulture(gc.getMap().plot(x, y), iCiv, 100, True)
				self.convertSurroundingPlotCulture(iCiv, utils.surroundingPlots(tCapital))
				
				#cover plots revealed
				for (i, j) in utils.surroundingPlots((0, 0), 2):
					gc.getMap().plot(i, j).setRevealed(iCiv, False, True, -1)


				print ("birthConditional: starting units in", x, y)
				self.createStartingUnits(iCiv, tCapital)

				data.players[iCiv].iPlagueCountdown
				utils.clearPlague(iCiv)

				print ("flipping remaining units")
				lPlots = utils.getPlotList(tTopLeft, tBottomRight)
				utils.flipUnitsInArea(lPlots, iCiv, iBarbarian, True, True) #remaining barbs in the region now belong to the new civ 
				utils.flipUnitsInArea(lPlots, iCiv, iIndependent, True, False) #remaining barbs in the region now belong to the new civ 
				utils.flipUnitsInArea(lPlots, iCiv, iIndependent2, True, False) #remaining barbs in the region now belong to the new civ 
				
				self.assignTechs(iCiv)
				
				data.players[iCiv].iFlipsDelay = iFlipsDelay #save

				# kill the catapult and cover the plots
				utils.clearCatapult(iCiv)
				
				utils.convertPlotCulture(gc.getMap().plot(x, y), iCiv, 100, True)
				
				# notify dynamic names
				dc.onCityAcquired(iCiv, iOwner)
				
				if iCiv not in lCapitalStart:
					self.createStartingWorkers(iCiv, tCapital)

		else: # starting units have already been placed, now to the second part
			lPlots = utils.getPlotList(tTopLeft, tBottomRight, Areas.getBirthExceptions(iCiv))
			iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, lPlots)
			self.convertSurroundingPlotCulture(iCiv, lPlots)
				
			for i in range(iIndependent, iBarbarian+1):
				utils.flipUnitsInArea(lPlots, iCiv, i, False, True) #remaining barbs/indeps in the region now belong to the new civ   
			
			# kill the catapult and cover the plots
			utils.clearCatapult(iCiv)
				
			# convert human cities
			if iNumHumanCitiesToConvert > 0:
				print "Flip Popup: in capital"
				self.scheduleFlipPopup(iCiv, lPlots)
				
			utils.convertPlotCulture(gc.getMap().plot(x, y), iCiv, 100, True)
			
				
	def getConvertedCities(self, iPlayer, lPlots = []):
		lCities = []
		
		for city in utils.getAreaCities(lPlots):
			if city.plot().isCore(city.getOwner()) and not city.plot().isCore(iPlayer): continue
			
			if city.getOwner() != iPlayer:
				lCities.append(city)
			
		# Leoreth: Byzantium also flips Roman cities in the eastern half of the empire outside of its core (Egypt, Mesopotamia)
		if iPlayer == iByzantium and pRome.isAlive():
			x, y = Areas.getCapital(iByzantium)
			for city in utils.getCityList(iRome):
				if city.getX() >= x-1 and city.getY() <= y:
					if (city.getX(), city.getY()) not in lPlots:
						lCities.append(city)
					
		# Leoreth: Canada also flips English/American/French cities in the Canada region
		if iPlayer == iCanada:
			lCanadaCities = []
			lCanadaCities.extend(utils.getCityList(iFrance))
			lCanadaCities.extend(utils.getCityList(iEngland))
			lCanadaCities.extend(utils.getCityList(iAmerica))
			
			for city in lCanadaCities:
				if city.getRegionID() == rCanada and city.getX() < Areas.getCapital(iCanada)[0] and (city.getX(), city.getY()) not in [(c.getX(), c.getY()) for c in lCities]:
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
			iHuman = utils.getHumanID()
			iOwner = city.getOwner()
			iCultureChange = 0
			
			# Case 1: Minor civilization
			if iOwner in [iBarbarian, iIndependent, iIndependent2, iNative]:
				iCultureChange = 100
				
			# Case 2: Human city
			elif iOwner == iHuman:
				iNumHumanCities += 1
				
			# Case 3: Other
			else:
				iCultureChange = 100
				if iOwner not in lEnemies: lEnemies.append(iOwner)
				
			if iCultureChange > 0:
				utils.completeCityFlip(x, y, iPlayer, iOwner, iCultureChange, True, False, False, True)
				utils.ensureDefenders(iPlayer, (x, y), 2)
				iConvertedCitiesCount += 1
				
		self.warOnSpawn(iPlayer, lEnemies)
				
		if iConvertedCitiesCount > 0:
			if iHuman == iPlayer:
				CyInterface().addMessage(iPlayer, True, iDuration, CyTranslator().getText("TXT_KEY_FLIP_TO_US", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
				
		return iConvertedCitiesCount, iNumHumanCities
		
	def warOnSpawn(self, iPlayer, lEnemies):
		if iPlayer == iCanada: return
		elif iPlayer == iGermany and utils.getHumanID() != iPlayer: return
		
		if gc.getGame().getGameTurn() <= getTurnForYear(tBirth[iPlayer]) + 5:
			for iEnemy in lEnemies:
				tEnemy = gc.getTeam(iEnemy)
				
				if tEnemy.isAtWar(iPlayer): continue
				if iPlayer == iByzantium and iEnemy == iRome: continue
			
				iRand = gc.getGame().getSorenRandNum(100, 'War on spawn')
				if iRand >= tAIStopBirthThreshold[iEnemy]:
					tEnemy.declareWar(iPlayer, True, WarPlanTypes.WARPLAN_ATTACKED_RECENT)
					self.spawnAdditionalUnits(iPlayer)
					
	def spawnAdditionalUnits(self, iPlayer):
		tPlot = Areas.getCapital(iPlayer)
		self.createAdditionalUnits(iPlayer, tPlot)

	def convertSurroundingPlotCulture(self, iCiv, lPlots):
		for (x, y) in lPlots:
			pPlot = gc.getMap().plot(x, y)
			if pPlot.isOwned() and pPlot.isCore(pPlot.getOwner()) and not pPlot.isCore(iCiv): continue
			pPlot.resetCultureConversion()
			if not pPlot.isCity():
				utils.convertPlotCulture(pPlot, iCiv, 100, False)

	def findSeaPlots( self, tCoords, iRange, iCiv):
		"""Searches a sea plot that isn't occupied by a unit and isn't a civ's territory surrounding the starting coordinates"""
		seaPlotList = []
		for (x, y) in utils.surroundingPlots(tCoords, iRange): 
			pPLot = gc.getMap().plot(x, y)
			if pPLot.isWater():
				if not pPLot.isUnit():
					if not (pPLot.isOwned() and pPLot.getOwner() != iCiv):
						seaPlotList.append((x, y))
						# this is a good plot, so paint it and continue search
		if seaPlotList:
			return utils.getRandomEntry(seaPlotList)
		return (None)


	def giveRaiders( self, iCiv, lPlots):
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		if pCiv.isAlive() and not pCiv.isHuman():

			cityList = []
			#collect all the coastal cities belonging to iCiv in the area
			for (x, y) in lPlots:
				pPLot = gc.getMap().plot(x, y)
				if pPLot.isCity():
					city = pPLot.getPlotCity()
					if city.getOwner() == iCiv:
						if city.isCoastalOld():
							cityList.append(city)

			if cityList:
				city = utils.getRandomEntry(cityList)
				if city:
					tCityPlot = (city.getX(), city.getY())
					tPlot = self.findSeaPlots(tCityPlot, 1, iCiv)
					if tPlot:
						x, y = tPlot
						gc.getPlayer(iCiv).initUnit(utils.getUniqueUnitType(iCiv, gc.getUnitInfo(iGalley).getUnitClassType()), x, y, UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
						if teamCiv.isHasTech(iSteel):
							gc.getPlayer(iCiv).initUnit(utils.getUniqueUnitType(iCiv, gc.getUnitInfo(iHeavySwordsman).getUnitClassType()), x, y, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
							gc.getPlayer(iCiv).initUnit(utils.getUniqueUnitType(iCiv, gc.getUnitInfo(iHeavySwordsman).getUnitClassType()), x, y, UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)
						else:
							gc.getPlayer(iCiv).initUnit(iSwordsman, x, y, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
							gc.getPlayer(iCiv).initUnit(iSwordsman, x, y, UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)

	def giveEarlyColonists( self, iCiv):
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		if pCiv.isAlive() and not pCiv.isHuman():
			capital = gc.getPlayer(iCiv).getCapitalCity()
			tCapital = (capital.getX(), capital.getY())

			if iCiv == iRome:
				for city in utils.getCityList(iCiv):
					if city.getRegionID() == rIberia:
						tCapital = (city.getX(), city.getY())
						break
						
			tSeaPlot = self.findSeaPlots(tCapital, 1, iCiv)
			
			if tSeaPlot:
				gc.getPlayer(iCiv).initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iArcher, iCiv, tSeaPlot, 1)

	def giveColonists(self, iCiv):
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		
		if pCiv.isAlive() and utils.getHumanID() != iCiv and iCiv in dMaxColonists:
			if teamCiv.isHasTech(iExploration) and data.players[iCiv].iColonistsAlreadyGiven < dMaxColonists[iCiv]:
				lCities = utils.getAreaCitiesCiv(iCiv, Areas.getCoreArea(iCiv))
				
				# help England with settling Canada and Australia
				if iCiv == iEngland:
					lColonialCities = utils.getAreaCitiesCiv(iCiv, utils.getPlotList(tCanadaTL, tCanadaBR))
					lColonialCities.extend(utils.getAreaCitiesCiv(iCiv, utils.getPlotList(tAustraliaTL, tAustraliaBR)))
					
					if lColonialCities:
						lCities = lColonialCities
						
				lCoastalCities = [city for city in lCities if city.isCoastal(20)]
						
				if lCoastalCities:
					city = utils.getRandomEntry(lCoastalCities)
					tPlot = (city.getX(), city.getY())
					tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
					if not tSeaPlot: tSeaPlot = tPlot
					
					utils.makeUnitAI(utils.getUniqueUnitType(iCiv, gc.getUnitInfo(iGalleon).getUnitClassType()), iCiv, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA, 1)
					utils.makeUnitAI(iSettler, iCiv, tSeaPlot, UnitAITypes.UNITAI_SETTLE, 1)
					utils.makeUnit(utils.getBestDefender(iCiv), iCiv, tSeaPlot, 1)
					utils.makeUnit(iWorker, iCiv, tSeaPlot, 1)
					
					data.players[iCiv].iColonistsAlreadyGiven += 1
					

	def onFirstContact(self, iTeamX, iHasMetTeamY):
	
		iGameTurn = gc.getGame().getGameTurn()
		
		# inuit don't trigger mississippi collapse
		if iTeamX in [iInuit] or iHasMetTeamY in [iPolynesia]: return
		
		# no conquerors for minor civs
		if iHasMetTeamY >= iNumPlayers: return
		
		if iTeamX >= iNumPlayers or iHasMetTeamY >= iNumPlayers: return
		
		if iGameTurn > getTurnForYear(600) and iGameTurn < getTurnForYear(1800):
			if iTeamX in lCivBioNewWorld and iHasMetTeamY in lCivBioOldWorld:
				iNewWorldCiv = iTeamX
				iOldWorldCiv = iHasMetTeamY
				
				if pMississippi.isAlive() and not pMississippi.isHuman() and not data.bMississippiCollapse:
					data.bMississippiCollapse = True
					sta.completeCollapse(iMississippi)
				iIndex = lCivBioNewWorld.index(iNewWorldCiv)
				
				bAlreadyContacted = data.lFirstContactConquerors[iIndex]
				
				# avoid "return later" exploit
				if iGameTurn <= getTurnForYear(tBirth[iAztecs])+10:
					data.lFirstContactConquerors[iIndex] = True
					return
					
				if not bAlreadyContacted:
					if iNewWorldCiv == iNorteChico:
						tContactZoneTL = (21, 11)
						tContactZoneBR = (36, 40)
					elif iNewWorldCiv == iOlmecs:
						tContactZoneTL = (15, 31)
						tContactZoneBR = (25, 39)
					elif iNewWorldCiv == iMaya:
						tContactZoneTL = (15, 30)
						tContactZoneBR = (34, 42)
					elif iNewWorldCiv == iTeotihuacan:
						tContactZoneTL = (11, 31)
						tContactZoneBR = (34, 43)
					elif iNewWorldCiv == iTiwanaku:
						tContactZoneTL = (21, 11)
						tContactZoneBR = (36, 40)
					elif iNewWorldCiv == iWari:
						tContactZoneTL = (21, 11)
						tContactZoneBR = (36, 40)
					elif iNewWorldCiv == iChimu:
						tContactZoneTL = (21, 11)
						tContactZoneBR = (36, 40)
					elif iNewWorldCiv == iAztecs:
						tContactZoneTL = (11, 31)
						tContactZoneBR = (34, 43)
					elif iNewWorldCiv == iInca:
						tContactZoneTL = (21, 11)
						tContactZoneBR = (36, 40)
					elif iNewWorldCiv == iMuisca:
						tContactZoneTL = (21, 11)
						tContactZoneBR = (36, 40)
						
					lArrivalExceptions = [(25, 32), (26, 40), (25, 42), (23, 42), (21, 42)]
						
					data.lFirstContactConquerors[iIndex] = True
					
					# change some terrain to end isolation
					if iNewWorldCiv == iInca:
						gc.getMap().plot(27, 30).setFeatureType(-1, 0)
						gc.getMap().plot(28, 31).setFeatureType(-1, 0)
						gc.getMap().plot(29, 23).setPlotType(PlotTypes.PLOT_HILLS, True, True)
						gc.getMap().plot(31, 13).setPlotType(PlotTypes.PLOT_HILLS, True, True) 
						gc.getMap().plot(32, 19).setPlotType(PlotTypes.PLOT_HILLS, True, True)
					elif iNewWorldCiv == iAztecs:
						gc.getMap().plot(40, 66).setPlotType(PlotTypes.PLOT_HILLS, True, True)
						
					lContactPlots = []
					lArrivalPlots = []
					if not iNewWorldCiv in [iMississippi]:
						for (x, y) in utils.getPlotList(tContactZoneTL, tContactZoneBR, lArrivalExceptions):
							plot = gc.getMap().plot(x, y)
							if plot.isVisible(iNewWorldCiv, False) and plot.isVisible(iOldWorldCiv, False):
								lContactPlots.append((x,y))
							if plot.getOwner() == iNewWorldCiv and not plot.isCity():
								if plot.isFlatlands() or plot.isHills():
									if not plot.getFeatureType() in [iJungle, iRainforest] and not plot.getTerrainType() == iMarsh:
										if gc.getMap().getArea(plot.getArea()).getNumTiles() > 3:
											lArrivalPlots.append((x,y))
								
					if lContactPlots and lArrivalPlots:
						tContactPlot = utils.getRandomEntry(lContactPlots)
						lDistancePlots = [(tuple, utils.calculateDistance(tuple[0], tuple[1], tContactPlot[0], tContactPlot[1])) for tuple in lArrivalPlots]
						lDistancePlots.sort(key=itemgetter(1))
						tArrivalPlot = lDistancePlots[0][0]
												
						pNewWorldCiv = gc.getPlayer(iNewWorldCiv)
						teamOldWorldCiv = gc.getTeam(gc.getPlayer(iOldWorldCiv).getTeam())
						
						iModifier1 = 0
						iModifier2 = 0
						
						if utils.getHumanID() == iNewWorldCiv:
							if pNewWorldCiv.getNumCities() > 6: iModifier1 = 1
						else:
							if iNewWorldCiv == iInca or pNewWorldCiv.getNumCities() > 4: iModifier1 = 1
							if utils.getHumanID() != iOldWorldCiv: iModifier2 = 1
							
						if gc.getGame().getGameTurnYear() < tBirth[utils.getHumanID()]:
							iModifier1 += 1
							iModifier2 += 1
							
						teamOldWorldCiv.declareWar(iNewWorldCiv, True, WarPlanTypes.WARPLAN_TOTAL)
						
						iInfantry = utils.getBestInfantry(iOldWorldCiv)
						iCounter = utils.getBestCounter(iOldWorldCiv)
						iCavalry = utils.getBestCavalry(iOldWorldCiv)
						iSiege = utils.getBestSiege(iOldWorldCiv)
						iStateReligion = gc.getPlayer(iOldWorldCiv).getStateReligion()
						
						if iInfantry:
							utils.makeUnitAI(iInfantry, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1 + iModifier2)
						
						if iCounter:
							utils.makeUnitAI(iCounter, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
							
						if iSiege:
							utils.makeUnitAI(iSiege, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1 + iModifier1 + iModifier2)
							
						if iCavalry:
							utils.makeUnitAI(iCavalry, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 + iModifier1)
							
						if iStateReligion >= 0:
							utils.makeUnit(iMissionary + iStateReligion, iOldWorldCiv, tArrivalPlot, 1)
							
						if iNewWorldCiv == iInca:
							utils.makeUnitAI(iAucac, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
						elif iNewWorldCiv == iAztecs or iNewWorldCiv == iTeotihuacan:
							utils.makeUnitAI(iJaguar, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
							utils.makeUnitAI(iHolkan, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
						elif iNewWorldCiv == iMaya or iNewWorldCiv == iOlmecs:
							utils.makeUnitAI(iHolkan, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
							utils.makeUnitAI(iJaguar, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
						
						if utils.getHumanID() == iNewWorldCiv:
							CyInterface().addMessage(iNewWorldCiv, True, iDuration, CyTranslator().getText("TXT_KEY_FIRST_CONTACT_NEWWORLD", ()), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
						elif utils.getHumanID() == iOldWorldCiv:
							CyInterface().addMessage(iOldWorldCiv, True, iDuration, CyTranslator().getText("TXT_KEY_FIRST_CONTACT_OLDWORLD", ()), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
							
		# Leoreth: Mongol horde event against Arabia, Persia, Byzantium, Kievan Rus, and Khazars (Mughals don't seem to be included)
		if iHasMetTeamY == iMongolia and not utils.getHumanID() == iMongolia:
			if iTeamX in lMongolCivs:
				if gc.getGame().getGameTurn() < getTurnForYear(1500) and data.isFirstContactMongols(iTeamX):

					data.setFirstContactMongols(iTeamX, False)
		
					teamTarget = gc.getTeam(iTeamX)
						
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
					elif iTeamX == iKievanRus:
						tTL = (68, 48)
						tBR = (81, 62)
						iDirection = DirectionTypes.DIRECTION_EAST
					elif iTeamX == iKhazars:
						tTL = (72, 47)
						tBR = (81, 53)
						iDirection = DirectionTypes.DIRECTION_EAST
					elif iTeamX == iMughals:
						tTL = (85, 35)
						tBR = (96, 44)
						iDirection = DirectionTypes.DIRECTION_NORTH

					lTargetList = utils.getBorderPlots(iTeamX, tTL, tBR, iDirection, 3)
					
					if not lTargetList: return

					teamMongolia.declareWar(iTeamX, True, WarPlanTypes.WARPLAN_TOTAL)
					
					iHandicap = 0
					if utils.getHumanID() == iTeamX:
						iHandicap = gc.getGame().getHandicapType() / 2

					for tPlot in lTargetList:
						utils.makeUnitAI(iKeshik, iMongolia, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 + iHandicap)
						utils.makeUnitAI(iMangudai, iMongolia, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1 + 2 * iHandicap)
						utils.makeUnitAI(iTrebuchet, iMongolia, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1 + iHandicap)

					if utils.getHumanID() == iTeamX:
						CyInterface().addMessage(iTeamX, True, iDuration, CyTranslator().getText("TXT_KEY_MONGOL_HORDE_HUMAN", ()), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
					elif gc.getTeam(gc.getPlayer(utils.getHumanID()).getTeam()).canContact(iTeamX):
						CyInterface().addMessage(utils.getHumanID(), True, iDuration, CyTranslator().getText("TXT_KEY_MONGOL_HORDE", (gc.getPlayer(iTeamX).getCivilizationAdjectiveKey(),)), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)

	def lateTradingCompany(self, iCiv):
		if utils.getHumanID() != iCiv and not utils.isAVassal(iCiv) and utils.getScenario() != i1700AD:
			if iCiv in [iFrance, iEngland, iNetherlands]:
				self.handleColonialConquest(iCiv)

	def earlyTradingCompany(self, iCiv):
		if utils.getHumanID() != iCiv and not utils.isAVassal(iCiv):
			if iCiv in [iSpain, iPortugal]:
				self.handleColonialAcquisition(iCiv)
				
	def onRailroadDiscovered(self, iCiv):
	
		if utils.getHumanID() != iCiv:
			if iCiv == iAmerica:
				iCount = 0
				bAlaska = False
				lWestCoast = [(11, 50), (11, 49), (11, 48), (11, 47), (11, 46), (12, 45)]
				lAlaska = [(7, 58), (8, 59), (9, 59), (10, 60), (11, 59), (11, 60), (11, 61), (10, 61), (9, 61), (8, 62), (7, 62), (7, 61), (6, 60), (5, 59), (4, 59), (3, 60), (4, 60), (5, 60), (5, 61), (7, 63), (7, 64), (8, 65), (9, 65), (9, 64), (8, 63), (9, 62), (10, 63), (10, 64), (11, 63), (11, 62)]
				lEnemyCivs = []
				lFreePlots = []
				for tPlot in lWestCoast:
					x, y = tPlot
					pPlot = gc.getMap().plot(x, y)
					if pPlot.isCity():
						if pPlot.getPlotCity().getOwner() != iAmerica:
							iCount += 1
							lWestCoast.remove((x, y))
							lEnemyCivs.append(pPlot.getPlotCity().getOwner())
							for (i, j) in utils.surroundingPlots(tPlot):
								plot = gc.getMap().plot(i, j)
								if not (plot.isCity() or plot.isPeak() or plot.isWater()):
									lFreePlots.append((i, j))
									
				for tPlot in lAlaska:
					x, y = tPlot
					pPlot = gc.getMap().plot(x, y)
					if pPlot.isCity():
						if pPlot.getPlotCity().getOwner() != iAmerica:
							iCount += 1
							lAlaska.remove((x, y))
							lEnemyCivs.append(pPlot.getPlotCity().getOwner())
							for (i, j) in utils.surroundingPlots(tPlot):
								plot = gc.getMap().plot(i, j)
								if not (plot.isCity() or plot.isPeak() or plot.isWater()):
									lFreePlots.append((i, j))
							if bAlaska:
								break
							else:
								bAlaska = True
									
				for iEnemy in lEnemyCivs:
					gc.getTeam(iCiv).declareWar(iEnemy, True, WarPlanTypes.WARPLAN_LIMITED)
									
				if iCount > 0:
					for i in range(iCount):
						tPlot = utils.getRandomEntry(lFreePlots)
						utils.makeUnitAI(iMinuteman, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
						utils.makeUnitAI(iCannon, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
						
				if 2-iCount > 0:
					for i in range(2-iCount):
						tPlot = utils.getRandomEntry(lWestCoast)
						utils.makeUnit(iSettler, iCiv, tPlot, 1)
						utils.makeUnit(iMinuteman, iCiv, tPlot, 1)
						
			elif iCiv == iRussia:
				lFreePlots = []
				tVladivostok = (111, 51)
				
				x, y = tVladivostok
				pPlot = gc.getMap().plot(x, y)
				utils.convertPlotCulture(pPlot, iRussia, 100, True)
				if pPlot.isCity():
					if pPlot.getPlotCity().getOwner() != iRussia:
						for (i, j) in utils.surroundingPlots(tVladivostok):
							plot = gc.getMap().plot(i, j)
							if not (plot.isCity() or plot.isWater() or plot.isPeak()):
								lFreePlots.append((i, j))
									
						tPlot = utils.getRandomEntry(lFreePlots)
						gc.getTeam(iRussia).declareWar(pPlot.getOwner(), True, WarPlanTypes.WARPLAN_LIMITED)
						utils.makeUnitAI(iRifleman, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 4)
						utils.makeUnitAI(iCannon, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
				else:
					if utils.isFree(iRussia, tVladivostok, True): # Also bNoEnemyUnits?
						pRussia.found(x, y)
						utils.makeUnit(iRifleman, iCiv, tVladivostok, 2)
						utils.makeUnit(iRifleman, iCiv, tVladivostok, 2)
						
						for (i, j) in utils.surroundingPlots(tVladivostok):
							utils.convertPlotCulture(gc.getMap().plot(i, j), iRussia, 80, True)
					


	def handleColonialAcquisition(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		targetList = utils.getColonialTargets(iPlayer, True)
		targetCivList = []
		settlerList = []
		
		if not targetList:
			return

		iGold = len(targetList) * 200

		for tPlot in targetList:
			x, y = tPlot
			if gc.getMap().plot(x, y).isCity():
				iTargetCiv = gc.getMap().plot(x, y).getPlotCity().getOwner()
				if not iTargetCiv in targetCivList:
					targetCivList.append(iTargetCiv)
			else:
				settlerList.append(tPlot)

		for tPlot in settlerList:
			utils.colonialAcquisition(iPlayer, tPlot)
	
		for iTargetCiv in targetCivList:
			if iTargetCiv == utils.getHumanID():
				askCityList = []
				sAskCities = ""
				sPlayer = pPlayer.getCivilizationAdjectiveKey()
				for tPlot in targetList:
					x, y = tPlot
					if gc.getMap().plot(x, y).getPlotCity().getOwner() == iTargetCiv:
						askCityList.append(tPlot)
						#sAskCities += gc.getMap().plot(x, y).getPlotCity().getName() + " "
						
				if askCityList:
					x, y = askCityList[0]
					sAskCities = gc.getMap().plot(x, y).getPlotCity().getName()
					
				for tPlot in askCityList:
					x, y = tPlot
					if tPlot != askCityList[0]:
						if tPlot != askCityList[len(askCityList)-1]:
							sAskCities += ", " + gc.getMap().plot(x, y).getPlotCity().getName()
						else:
							sAskCities += CyTranslator().getText("TXT_KEY_AND", ()) + gc.getMap().plot(x, y).getPlotCity().getName()
						
				iAskGold = len(askCityList) * 200
						
				popup = Popup.PyPopup(7625, EventContextTypes.EVENTCONTEXT_ALL)
				popup.setHeaderString(CyTranslator().getText("TXT_KEY_ASKCOLONIALCITY_TITLE", (sPlayer,)))
				popup.setBodyString(CyTranslator().getText("TXT_KEY_ASKCOLONIALCITY_MESSAGE", (sPlayer, iAskGold, sAskCities)))
				popup.addButton(CyTranslator().getText("TXT_KEY_POPUP_YES", ()))
				popup.addButton(CyTranslator().getText("TXT_KEY_POPUP_NO", ()))
				argsList = (iPlayer, askCityList)
				data.lTempEventList = argsList
				popup.launch(False)
			else:
				iRand = gc.getGame().getSorenRandNum(100, 'City acquisition offer')
				if iTargetCiv < iNumPlayers:
					if iRand >= tPatienceThreshold[iTargetCiv] and not gc.getTeam(iPlayer).isAtWar(iTargetCiv):
						bAccepted = True
					else:
						bAccepted = False
				else:
					bAccepted = True
				
				iNumCities = 0
				for tPlot in targetList:
					x, y = tPlot
					if gc.getMap().plot(x, y).getPlotCity().getOwner() == iTargetCiv:
						iNumCities += 1
						
				if iNumCities >= gc.getPlayer(iTargetCiv).getNumCities():
					bAccepted = False

				for tPlot in targetList:
					x, y = tPlot
					if gc.getMap().plot(x, y).getPlotCity().getOwner() == iTargetCiv:
						if bAccepted:
							utils.colonialAcquisition(iPlayer, tPlot)
							gc.getPlayer(iTargetCiv).changeGold(200)
						else:
							data.timedConquest(iPlayer, tPlot)

		pPlayer.setGold(max(0, pPlayer.getGold()-iGold))

	def handleColonialConquest(self, iPlayer):
		targetList = utils.getColonialTargets(iPlayer)
		
		if not targetList:
			self.handleColonialAcquisition(iPlayer)
			return

		for tPlot in targetList:
			data.timedConquest(iPlayer, tPlot)

		tSeaPlot = -1
		for (i, j) in utils.surroundingPlots(targetList[0]):
			if gc.getMap().plot(i, j).isWater():
				tSeaPlot = (i, j)
				break

		if tSeaPlot != -1:
			utils.makeUnit(utils.getUniqueUnitType(iPlayer, gc.getUnitInfo(iGalleon).getUnitClassType()), iPlayer, tSeaPlot, 1)
	
	def startWarsOnSpawn(self, iCiv, bRespawn):
	
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		
		iMin = 10
		
		if gc.getGame().getSorenRandNum(100, 'Trigger spawn wars') >= iMin:
			if bRespawn:
				lEnemies = lEnemyCivsOnRespawn[iCiv]
			else:
				lEnemies = lEnemyCivsOnSpawn[iCiv]
				
			for iLoopCiv in lEnemies:
				if utils.isAVassal(iLoopCiv): continue
				if not gc.getPlayer(iLoopCiv).isAlive(): continue
				if teamCiv.isAtWar(iLoopCiv): continue
				if utils.getHumanID() == iCiv and iLoopCiv not in lTotalWarOnSpawn[iCiv]: continue
				
				iLoopMin = 50
				if iLoopCiv >= iNumMajorPlayers: iLoopMin = 30
				if utils.getHumanID() == iLoopCiv: iLoopMin += 10
				
				if gc.getGame().getSorenRandNum(100, 'Check spawn war') >= iLoopMin:
					iWarPlan = -1
					if iLoopCiv in lTotalWarOnSpawn[iCiv]:
						iWarPlan = WarPlanTypes.WARPLAN_TOTAL
					teamCiv.declareWar(iLoopCiv, False, iWarPlan)
					
					if utils.getHumanID() == iCiv: data.iBetrayalTurns = 0
					
					
	def immuneMode(self, argsList): 
		pWinningUnit,pLosingUnit = argsList
		iLosingPlayer = pLosingUnit.getOwner()
		iUnitType = pLosingUnit.getUnitType()
		if iLosingPlayer < iNumMajorPlayers:
			if gc.getGame().getGameTurn() >= getTurnForYear(tBirth[iLosingPlayer]) and gc.getGame().getGameTurn() <= getTurnForYear(tBirth[iLosingPlayer])+2:
				if (pLosingUnit.getX(), pLosingUnit.getY()) == Areas.getCapital(iLosingPlayer):
					print("new civs are immune for now")
					if gc.getGame().getSorenRandNum(100, 'immune roll') >= 50:
						utils.makeUnit(iUnitType, iLosingPlayer, (pLosingUnit.getX(), pLosingUnit.getY()), 1)

	def initMinorBetrayal( self, iCiv ):
		iHuman = utils.getHumanID()
		lPlots = Areas.getBirthArea(iCiv)
		plotList = utils.listSearch(lPlots, utils.outerInvasion, [])
		if plotList:
			tPlot = utils.getRandomEntry(plotList)
			if tPlot:
				self.createAdditionalUnits(iCiv, tPlot)
				self.unitsBetrayal(iCiv, iHuman, lPlots, tPlot)

	def initBetrayal( self ):
		iFlipPlayer = data.iNewCivFlip
		if not gc.getPlayer(iFlipPlayer).isAlive() or not gc.getTeam(iFlipPlayer).isAtWar(utils.getHumanID()):
			data.iBetrayalTurns = 0
			return
	
		iHuman = utils.getHumanID()
		turnsLeft = data.iBetrayalTurns
		
		lTempPlots = [(x, y) for (x, y) in data.lTempPlots if not gc.getMap().plot(x, y).isCore(data.iOldCivFlip)]
		plotList = utils.listSearch(lTempPlots, utils.outerInvasion, [] )
		if not plotList:
			plotList = utils.listSearch(lTempPlots, utils.innerSpawn, [data.iOldCivFlip, data.iNewCivFlip] )			
		if not plotList:
			plotList = utils.listSearch(lTempPlots, utils.innerInvasion, [data.iOldCivFlip, data.iNewCivFlip] )				
		if plotList:
			tPlot = utils.getRandomEntry(plotList)
			if tPlot:
				if turnsLeft == iBetrayalPeriod:
					self.createAdditionalUnits(data.iNewCivFlip, tPlot)
				self.unitsBetrayal(data.iNewCivFlip, data.iOldCivFlip, lTempPlots, tPlot)
		data.iBetrayalTurns = turnsLeft - 1



	def unitsBetrayal( self, iNewOwner, iOldOwner, lPlots, tPlot):
		if gc.getPlayer(data.iOldCivFlip).isHuman():
			CyInterface().addMessage(data.iOldCivFlip, False, iDuration, CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
		elif gc.getPlayer(data.iNewCivFlip).isHuman():
			CyInterface().addMessage(data.iNewCivFlip, False, iDuration, CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL_NEW", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
		for (x, y) in lPlots:
			killPlot = gc.getMap().plot(x,y)
			if killPlot.isCore(iOldOwner) and not killPlot.isCore(iNewOwner): continue
			iNumUnitsInAPlot = killPlot.getNumUnits()
			if iNumUnitsInAPlot > 0:
				for iUnit in reversed(range(iNumUnitsInAPlot)):
					unit = killPlot.getUnit(iUnit)
					if unit.getOwner() == iOldOwner:
						rndNum = gc.getGame().getSorenRandNum(100, 'betrayal')
						if rndNum >= iBetrayalThreshold:
							if unit.getDomainType() == DomainTypes.DOMAIN_LAND:
								iUnitType = unit.getUnitType()
								unit.kill(False, iNewOwner)
								utils.makeUnit(iUnitType, iNewOwner, tPlot, 1)

	def createAdditionalUnits(self, iCiv, tPlot):
		if iCiv == iIndia:
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iLightSwordsman, iCiv, tPlot, 1)
		elif iCiv == iGreece:
			utils.makeUnit(iHoplite, iCiv, tPlot, 4)
		elif iCiv == iPersia:
			utils.makeUnit(iImmortal, iCiv, tPlot, 4)
		elif iCiv == iCeltia:
			utils.makeUnit(iGallicWarrior, iCiv, tPlot, 4)
		elif iCiv == iCarthage:
			utils.makeUnit(iWarElephant, iCiv, tPlot, 1)
			utils.makeUnit(iNumidianCavalry, iCiv, tPlot, 1)
		elif iCiv == iPolynesia:
			utils.makeUnit(iMilitia, iCiv, tPlot, 2)
		elif iCiv == iRome:
			utils.makeUnit(iLegion, iCiv, tPlot, 2)
		elif iCiv == iMaya:
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iHolkan, iCiv, tPlot, 2)
		elif iCiv == iJapan:
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
		elif iCiv == iTamils:
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iWarElephant, iCiv, tPlot, 1)
		elif iCiv == iEthiopia:
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iShotelai, iCiv, tPlot, 2)
		elif iCiv == iVietnam:
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
		elif iCiv == iMississippi:
			utils.makeUnit(iFalconDancer, iCiv, tPlot, 4)
		elif iCiv == iInuit:
			utils.makeUnit(iMilitia, iCiv, tPlot, 4)
		elif iCiv == iKorea:
			for iUnit in [iHorseArcher, iCrossbowman]:
				utils.makeUnit(iUnit, iCiv, tPlot, 2)
		elif iCiv == iTiwanaku:
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iSkirmisher, iCiv, tPlot, 2)
		elif iCiv == iByzantium:
			utils.makeUnit(iCataphract, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 2)
		elif iCiv == iWari:
			utils.makeUnit(iPictaAucac, iCiv, tPlot, 3)
		elif iCiv == iVikings:
			utils.makeUnit(iHuscarl, iCiv, tPlot, 3)
		elif iCiv == iTurks:
			utils.makeUnit(iOghuz, iCiv, tPlot, 4)
		elif iCiv == iArabia:
			utils.makeUnit(iGhazi, iCiv, tPlot, 2)
			utils.makeUnit(iMobileGuard, iCiv, tPlot, 4)
		elif iCiv == iTibet:
			utils.makeUnit(iKhampa, iCiv, tPlot, 2)
		elif iCiv == iKhmer:
			utils.makeUnit(iSwordsman, iCiv, tPlot, 3)
			utils.makeUnit(iBallistaElephant, iCiv, tPlot, 2)
		elif iCiv == iMuisca:
			utils.makeUnit(iArcher, iCiv, tPlot, 1)
		elif iCiv == iIndonesia:
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iWarElephant, iCiv, tPlot, 1)
		elif iCiv == iBurma:
			utils.makeUnit(iArcher, iCiv, tPlot, 3)
			utils.makeUnit(iSkirmisher, iCiv, tPlot, 3)
		elif iCiv == iKhazars:
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 3)
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iSkirmisher, iCiv, tPlot, 2)
		elif iCiv == iChad:
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iSkirmisher, iCiv, tPlot, 2)
		elif iCiv == iMoors:
			utils.makeUnit(iCamelArcher, iCiv, tPlot, 2)
		elif iCiv == iSpain:
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 3)
		elif iCiv == iFrance:
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 3)
		elif iCiv == iOman:
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iCamelArcher, iCiv, tPlot, 2)
		elif iCiv == iYemen:
			utils.makeUnit(iArcher, iCiv, tPlot, 1)
			utils.makeUnit(iLongbowman, iCiv, tPlot, 2)
			utils.makeUnit(iTrebuchet, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iHeavyGalley, iCiv, tPlot, 2)
		elif iCiv == iEngland:
			utils.makeUnit(iArcher, iCiv, tPlot, 1)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 3)
		elif iCiv == iHolyRome:
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 3)
		elif iCiv == iRussia:
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iHeavySpearman, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 2)
		elif iCiv == iKievanRus:
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 2)
		elif iCiv == iHungary:
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iTrebuchet, iCiv, tPlot, 1)
			utils.makeUnit(iHuszar, iCiv, tPlot, 3)
		elif iCiv == iNetherlands:
			utils.makeUnit(iMusketeer, iCiv, tPlot, 3)
			utils.makeUnit(iPikeman, iCiv, tPlot, 3)
		elif iCiv == iPhilippines:
			utils.makeUnit(iArcher, iCiv, tPlot, 3)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
		elif iCiv == iChimu:
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iChimuSuchucChiquiAucac, iCiv, tPlot, 3)
		elif iCiv == iSwahili:
			utils.makeUnit(iSpearman, iCiv, tPlot, 3)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 3)
		elif iCiv == iMamluks:
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 2)
		elif iCiv == iMali:
			utils.makeUnit(iKelebolo, iCiv, tPlot, 4)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 3)
		elif iCiv == iOttomans:
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 3)
		elif iCiv == iPoland:
			utils.makeUnit(iLancer, iCiv, tPlot, 2)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
		elif iCiv == iZimbabwe:
			utils.makeUnit(iSwordsman, iCiv, tPlot, 4)
		elif iCiv == iPortugal:
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(iPikeman, iCiv, tPlot, 3)
		elif iCiv == iInca:
			utils.makeUnit(iAucac, iCiv, tPlot, 5)
			utils.makeUnit(iArcher, iCiv, tPlot, 3)
		elif iCiv == iItaly:
			utils.makeUnit(iLancer, iCiv, tPlot, 2)
		elif iCiv == iNigeria:
			utils.makeUnit(iYanLifida, iCiv, tPlot, 4)
		elif iCiv == iMongolia:
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iMangudai, iCiv, tPlot, 2) 
			utils.makeUnit(iKeshik, iCiv, tPlot, 4)
		elif iCiv == iAztecs:
			utils.makeUnit(iJaguar, iCiv, tPlot, 5)
			utils.makeUnit(iArcher, iCiv, tPlot, 3)
		elif iCiv == iMughals:
			utils.makeUnit(iSiegeElephant, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 4)
		elif iCiv == iThailand:
			utils.makeUnit(iPikeman, iCiv, tPlot, 2)
			utils.makeUnit(iChangSuek, iCiv, tPlot, 2)
		elif iCiv == iCongo:
			utils.makeUnit(iPombos, iCiv, tPlot, 3)
		elif iCiv == iSweden:
			utils.makeUnit(iArquebusier, iCiv, tPlot, 4)
		elif iCiv == iManchuria:
			utils.makeUnit(iEightBanner, iCiv, tPlot, 4)
		elif iCiv == iGermany:
			utils.makeUnit(iFusilier, iCiv, tPlot, 5)
			utils.makeUnit(iBombard, iCiv, tPlot, 3)
		elif iCiv == iAmerica:
			utils.makeUnit(iGrenadier, iCiv, tPlot, 3)
			utils.makeUnit(iMinuteman, iCiv, tPlot, 3)
			utils.makeUnit(iCannon, iCiv, tPlot, 3)
		elif iCiv == iArgentina:
			utils.makeUnit(iRifleman, iCiv, tPlot, 2)
			utils.makeUnit(iGrenadierCavalry, iCiv, tPlot, 4)
		elif iCiv == iBrazil:
			utils.makeUnit(iGrenadier, iCiv, tPlot, 2)
			utils.makeUnit(iRifleman, iCiv, tPlot, 3)
			utils.makeUnit(iCannon, iCiv, tPlot, 2)
		elif iCiv == iAustralia:
			utils.makeUnit(iGrenadier, iCiv, tPlot, 2)
			utils.makeUnit(iRifleman, iCiv, tPlot, 3)
		elif iCiv == iBoers:
			utils.makeUnit(iKommando, iCiv, tPlot, 4)
			utils.makeUnit(iCannon, iCiv, tPlot, 2)
		elif iCiv == iCanada:
			utils.makeUnit(iCavalry, iCiv, tPlot, 2)
			utils.makeUnit(iRifleman, iCiv, tPlot, 4)
			utils.makeUnit(iCannon, iCiv, tPlot, 2)
		elif iCiv == iIsrael:
			utils.makeUnit(iInfantry, iCiv, tPlot, 2)


	def createStartingUnits(self, iCiv, tPlot):
		if iCiv == iNubia:
			utils.createSettlers(iCiv, 1)
			if utils.getHumanID() == iNubia:
				utils.makeUnit(iMilitia, iCiv, tPlot, 1)
			else:
				utils.makeUnit(iMedjay, iCiv, tPlot, 1)
		if iCiv == iChina:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iArcher, iCiv, tPlot, 1)
			utils.makeUnit(iMilitia, iCiv, tPlot, 1)
		elif iCiv == iIndia:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iArcher, iCiv, tPlot, 1)
			utils.makeUnit(iSpearman, iCiv, tPlot, 1)
			utils.makeUnit(iLightSwordsman, iCiv, tPlot, 1)
			utils.makeUnit(iChariot, iCiv, tPlot, 1)
		elif iCiv == iGreece:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iMilitia, iCiv, tPlot, 2)
			utils.makeUnit(iHoplite, iCiv, tPlot, 1) #3
			pGreece.initUnit(iHoplite, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			pGreece.initUnit(iHoplite, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
				pGreece.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iMilitia, iCiv, tSeaPlot, 1)
		elif iCiv == iOlmecs:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iMilitia, iCiv, tPlot, 1)
		elif iCiv == iPersia:
			utils.createSettlers(iCiv, 3)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 3)
			utils.makeUnit(iImmortal, iCiv, tPlot, 4)
			utils.makeUnit(iHorseman, iCiv, tPlot, 2)
			utils.makeUnit(iWarElephant, iCiv, tPlot, 1)
		elif iCiv == iCeltia:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iGallicWarrior, iCiv, tPlot, 2)
		elif iCiv == iCarthage:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iSacredBand, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 2)
				pCarthage.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iArcher, iCiv, tSeaPlot, 1)
				pCarthage.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pCarthage.initUnit(iWarGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
		elif iCiv == iPolynesia:
			tSeaPlot = (4, 19)
			utils.makeUnit(iSettler, iCiv, tPlot, 1)
			utils.makeUnit(iWaka, iCiv, tSeaPlot, 1)
			utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
			utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
		elif iCiv == iRome:
			utils.createSettlers(iCiv, 2)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 3)
			utils.makeUnit(iLegion, iCiv, tPlot, 4)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
				pRome.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pRome.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
		elif iCiv == iMaya:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iHolkan, iCiv, tPlot, 2)
		elif iCiv == iJapan:
			utils.createSettlers(iCiv, 3)
			utils.createMissionaries(iCiv, 1)
			utils.makeUnit(iSwordsman, iJapan, tPlot, 2)
			utils.makeUnitAI(iArcher, iJapan, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iJapan)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iJapan, tSeaPlot, 2)
			if utils.getHumanID() != iJapan:
				utils.makeUnit(iCrossbowman, iJapan, tPlot, 2)
				utils.makeUnit(iSamurai, iJapan, tPlot, 3)
		elif iCiv == iTamils:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iWarElephant, iCiv, tPlot, 1)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 1)
			if utils.getHumanID() != iTamils:
				utils.makeUnit(iHinduMissionary, iCiv, tPlot, 1)
				utils.makeUnit(iWarElephant, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iTamils)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iTamils, tSeaPlot, 1)
				utils.makeUnitAI(iGalley, iTamils, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA, 1)
				utils.makeUnit(iWarGalley, iTamils, tSeaPlot, 1)
				utils.makeUnit(iSettler, iTamils, tSeaPlot, 1)
				utils.makeUnit(iArcher, iTamils, tSeaPlot, 1)
		elif iCiv == iEthiopia:
			utils.createSettlers(iCiv, 2)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iShotelai, iCiv, tPlot, 1)
			utils.makeUnit(iLightSwordsman, iCiv, tPlot, 1)
			tSeaPlot = (74, 29)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
				utils.makeUnit(iWarGalley, iCiv, tSeaPlot, 1)
		elif iCiv == iVietnam:
			utils.createSettlers(iCiv, 2)
			utils.createMissionaries(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iVietnam)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
				utils.makeUnit(iGalley, iCiv, tSeaPlot, 1)
		elif iCiv == iTeotihuacan:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
		elif iCiv == iInuit:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iMilitia, iCiv, tPlot, 1)
			utils.makeUnit(iMilitia, iCiv, (123, 62), 1)
			utils.makeUnit(iDogSled, iCiv, (123, 62), 1)
		elif iCiv == iMississippi:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iFalconDancer, iCiv, tPlot, 2)
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
		elif iCiv == iKorea:
			utils.createSettlers(iCiv, 1)
			utils.createMissionaries(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 3)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 1)
			utils.makeUnit(iHorseman, iCiv, tPlot, 1)
			if utils.getHumanID() != iKorea:
				utils.makeUnit(iSpearman, iCiv, tPlot, 2)
				utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
		elif iCiv == iTiwanaku:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iSkirmisher, iCiv, tPlot, 2)
		elif iCiv == iByzantium:
			utils.makeUnit(iLegion, iCiv, tPlot, 4)
			utils.makeUnit(iSpearman, iCiv, tPlot, 2)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.createSettlers(iCiv, 4)
			utils.createMissionaries(iCiv, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iByzantium)
			if tSeaPlot:
				utils.makeUnit(iGalley, iByzantium, tSeaPlot, 2)
				utils.makeUnit(iWarGalley, iByzantium, tSeaPlot, 2)
				if utils.getScenario() == i3000BC:
					utils.makeUnit(iWorkboat, iByzantium, tSeaPlot, 1)
		elif iCiv == iWari:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iPictaAucac, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnitAI(iPictaAucac, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK, 2)
		elif iCiv == iVikings:
			utils.createSettlers(iCiv, 2)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 4)
			utils.makeUnit(iHuscarl, iCiv, tPlot, 3)
			utils.makeUnit(iScout, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
				pVikings.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iArcher, iCiv, tSeaPlot, 1)
				pVikings.initUnit(iLongship, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_EXPLORE_SEA, DirectionTypes.DIRECTION_SOUTH)
				pVikings.initUnit(iLongship, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_EXPLORE_SEA, DirectionTypes.DIRECTION_SOUTH)
		elif iCiv == iTurks:
			utils.createSettlers(iCiv, 6)
			if utils.getHumanID() == iTurks:
				utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 3)
			else:
				utils.makeUnitAI(iCrossbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 4)
			utils.makeUnit(iOghuz, iCiv, tPlot, 6)
			utils.makeUnit(iScout, iCiv, tPlot, 1)
		elif iCiv == iArabia:
			utils.createSettlers(iCiv, 2)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iMobileGuard, iCiv, tPlot, 2)
			utils.makeUnit(iGhazi, iCiv, tPlot, 2)
			utils.makeUnit(iWorker, iCiv, tPlot, 1)    
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
		elif iCiv == iTibet:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iKhampa, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 1)
		elif iCiv == iKhmer:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnitAI(iBallistaElephant, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
			utils.createMissionaries(iCiv, 1)
			utils.createMissionaries(iCiv, 1, iBuddhism)
			tSeaPlot = self.findSeaPlots(tPlot, 2, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
				pKhmer.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iArcher, iCiv, tSeaPlot, 1)
		elif iCiv == iMuisca:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
		elif iCiv == iIndonesia:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.createMissionaries(iCiv, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
				utils.makeUnit(iWarGalley, iCiv, tSeaPlot, 1)
				pIndonesia.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pIndonesia.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iArcher, iCiv, tSeaPlot, 1)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iArcher, iCiv, tSeaPlot, 1)
		elif iCiv == iBurma:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK, 1)
			if gc.getMap().plot(tPlot[0], tPlot[1]).isCity() and not gc.getMap().plot(tPlot[0], tPlot[1]).getPlotCity().isHasReligion(iBuddhism):
				utils.createMissionaries(iCiv, 1, iBuddhism)
		elif iCiv == iKhazars:
			utils.createSettlers(iCiv, 2)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 3)
			utils.makeUnitAI(iHorseArcher, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK, 4)
			utils.makeUnitAI(iSkirmisher, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK, 3)
		elif iCiv == iChad:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iSkirmisher, iCiv, tPlot, 2)
		elif iCiv == iMoors:
			utils.createSettlers(iCiv, 2)
			utils.makeUnitAI(iCrossbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iSpearman, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 2)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iGalley, iCiv, tSeaPlot, 1)
				utils.makeUnit(iHeavyGalley, iCiv, tSeaPlot, 1)
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
			if utils.getHumanID() in [iSpain, iMoors]:
				utils.makeUnitAI(iCrossbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
		elif iCiv == iSpain:
			iSpanishSettlers = 2
			if utils.getHumanID() != iSpain: iSpanishSettlers = 3
			utils.createSettlers(iCiv, iSpanishSettlers)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 1)
			utils.makeUnitAI(iCrossbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 4)
			if data.isPlayerEnabled(iMoors):
				if utils.getHumanID() != iMoors:
					utils.makeUnit(iLancer, iCiv, tPlot, 2)
			else:
				utils.makeUnit(iSettler, iCiv, tPlot, 1)
			if utils.getHumanID() != iSpain:
				utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 1)
			if utils.getScenario() == i600AD: #late start condition
				utils.makeUnit(iWorker, iCiv, tPlot, 1) #there is no carthaginian city in Iberia and Portugal may found 2 cities otherwise (a settler is too much)
		elif iCiv == iFrance:
			utils.createSettlers(iCiv, 3)
			utils.makeUnitAI(iCrossbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 3)
			utils.makeUnit(iHeavySpearman, iCiv, tPlot, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 3)
			utils.createMissionaries(iCiv, 1)
		elif iCiv == iOman:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iCamelArcher, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 1)
		elif iCiv == iYemen:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iLongbowman, iCiv, tPlot, 4)
			utils.makeUnit(iTrebuchet, iCiv, tPlot, 2)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iHeavyGalley, iCiv, tPlot, 2)
				utils.makeUnit(iCog, iCiv, tPlot, 2)
		elif iCiv == iEngland:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iLongbowman, iCiv, tPlot, 3)
			utils.makeUnitAI(iCrossbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.createMissionaries(iCiv, 1)
		elif iCiv == iHolyRome:
			utils.createSettlers(iCiv, 3)
			utils.makeUnitAI(iCrossbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 3)
			utils.makeUnitAI(iSwordsman, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
			utils.makeUnitAI(iLancer, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
			utils.makeUnitAI(iCatapult, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 4)
			utils.createMissionaries(iCiv, 1)
		elif iCiv == iRussia:
			utils.createSettlers(iCiv, 4)
			utils.makeUnitAI(iCrossbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 4)
		elif iCiv == iKievanRus:
			utils.createSettlers(iCiv, 1)
			utils.createMissionaries(iCiv, 1)
			utils.makeUnitAI(iCrossbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iDruzhina, iCiv, tPlot, 4)
		elif iCiv == iHungary:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iCrossbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnitAI(iHuszar, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 5)
			utils.makeUnitAI(iTrebuchet, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
		elif iCiv == iHolland:
			utils.createSettlers(iCiv, 2)
			utils.makeUnit(iArquebusier, iCiv, tPlot, 6)
			utils.makeUnit(iBombard, iCiv, tPlot, 2)
			utils.makeUnit(iPikeman, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 2)
				pNetherlands.initUnit(iEastIndiaman, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iCrossbowman, iCiv, tSeaPlot, 1)
				pNetherlands.initUnit(iEastIndiaman, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iCrossbowman, iCiv, tSeaPlot, 1)
				utils.makeUnit(iCaravel, iCiv, tSeaPlot, 2)
		elif iCiv == iPhilippines:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iArcher, iCiv, tPlot, 1)
		elif iCiv == iChimu:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iArcher, iCiv, tPlot, 1)
			utils.makeUnit(iChimuSuchucChiquiAucac, iCiv, tPlot, 2)
		elif iCiv == iSwahili:
			utils.createSettlers(iCiv, 3)
			utils.makeUnit(iArcher, iCiv, tPlot, 5)
			utils.createMissionaries(iCiv, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
				pPhilippines.initUnit(iBalangay, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iLongbowman, iCiv, tSeaPlot, 1)
				utils.makeUnit(iBalangay, iCiv, tSeaPlot, 1)
				utils.makeUnit(iGalley, iCiv, tSeaPlot, 2)
		elif iCiv == iMamluks:
			utils.createSettlers(iCiv, 3)
			utils.makeUnitAI(iCrossbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 1)
			utils.createMissionaries(iCiv, 1)
		elif iCiv == iMali:
			utils.createSettlers(iCiv, 3)
			utils.makeUnit(iKelebolo, iCiv, tPlot, 5)
			utils.createMissionaries(iCiv, 2)
		elif iCiv == iPoland:
			iNumSettlers = 1
			if utils.getHumanID() == iPoland: iNumSettlers = 2
			utils.createSettlers(iCiv, iNumSettlers)
			utils.makeUnitAI(iCrossbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iHeavySwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iLancer, iCiv, tPlot, 2)
			if utils.getHumanID() != iPoland:
				utils.makeUnit(iHeavySpearman, iCiv, tPlot, 2)
			utils.makeUnit(iLancer, iCiv, tPlot, 1)
			utils.createMissionaries(iCiv, 1)
		elif iCiv == iOttomans:
			utils.makeUnit(iHeavySwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iLancer, iCiv, tPlot, 3)
			utils.makeUnit(iJanissary, iCiv, tPlot, 2)
			utils.makeUnit(iGreatBombard, iCiv, tPlot, 2)
			utils.makeUnit(iTrebuchet, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 3)
			if utils.getHumanID() != iOttomans:
				utils.makeUnit(iGreatBombard, iCiv, tPlot, 4)
				utils.makeUnit(iJanissary, iCiv, tPlot, 5)
				utils.makeUnit(iLancer, iCiv, tPlot, 4)
		elif iCiv == iZimbabwe:
			utils.createSettlers(iCiv, 2)
			utils.makeUnit(iArcher, iCiv, tPlot, 3)
			utils.makeUnit(iHeavySpearman, iCiv, tPlot, 2)
		elif iCiv == iPortugal:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iCrossbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 4)
			utils.makeUnit(iHeavySpearman, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 2)
				utils.makeUnitAI(iCog, iCiv, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA, 1)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iCrossbowman, iCiv, tSeaPlot, 1)
				utils.makeUnitAI(iHeavyGalley, iCiv, tSeaPlot, UnitAITypes.UNITAI_EXPLORE_SEA, 1)
		elif iCiv == iInca:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iAucac, iCiv, tPlot, 4)
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			if utils.getHumanID() != iInca:
				utils.makeUnit(iSettler, iCiv, tPlot, 1)
		elif iCiv == iItaly:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iBalestriere, iCiv, tPlot, 3)
			utils.makeUnit(iHeavySpearman, iCiv, tPlot, 2)
			utils.makeUnit(iTrebuchet, iCiv, tPlot, 3)
			utils.createMissionaries(iCiv, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 2)
				utils.makeUnit(iCog, iCiv, tSeaPlot, 1)
				utils.makeUnit(iHeavyGalley, iCiv, tSeaPlot, 1)
		elif iCiv == iNigeria:
			utils.createSettlers(iCiv, 2)
			utils.makeUnit(iArcher, iCiv, tPlot, 3)
			utils.makeUnit(iYanLifida, iCiv, tPlot, 3)
		elif iCiv == iMongolia:
			utils.createSettlers(iCiv, 3)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(iHeavySwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iMangudai, iCiv, tPlot, 2)
			utils.makeUnitAI(iKeshik, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 6)
			utils.makeUnit(iBombard, iCiv, tPlot, 3)
			if utils.getHumanID() != iMongolia:
				utils.makeUnitAI(iKeshik, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 4)
				utils.makeUnitAI(iKeshik, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
				utils.makeUnitAI(iKeshik, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
				utils.makeUnitAI(iBombard, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
				utils.makeUnitAI(iBombard, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
				utils.makeUnitAI(iHeavySwordsman, iCiv, tPlot, UnitAITypes.UNITAI_COUNTER, 2)
				utils.makeUnitAI(iScout, iCiv, tPlot, UnitAITypes.UNITAI_EXPLORE, 2)
				utils.makeUnitAI(iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
		elif iCiv == iAztecs:
			utils.createSettlers(iCiv, 2)
			utils.makeUnit(iJaguar, iCiv, tPlot, 4)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 4)
		elif iCiv == iMughals:
			utils.createSettlers(iCiv, 3)
			utils.makeUnit(iSiegeElephant, iCiv, tPlot, 3)
			utils.makeUnit(iHeavySwordsman, iCiv, tPlot, 4, "", 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 1)
			if utils.getHumanID() == iMughals:
				utils.makeUnit(iIslamicMissionary, iCiv, tPlot, 3)
		elif iCiv == iThailand:
			utils.createSettlers(iCiv, 1)
			utils.createMissionaries(iCiv, 1)
			utils.makeUnit(iHeavySpearman, iCiv, tPlot, 3)
			utils.makeUnit(iChangSuek, iCiv, tPlot, 2)
		elif iCiv == iCongo:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iPombos, iCiv, tPlot, 2)
		elif iCiv == iSweden:
			utils.createSettlers(iCiv, 3)
			utils.makeUnit(iArquebusier, iCiv, tPlot, 5)
			utils.makeUnit(iPikeman, iCiv, tPlot, 2)
			utils.makeUnit(iBombard, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 2)
				utils.makeUnit(iGalleon, iCiv, tSeaPlot, 1)
				utils.makeUnit(iCaravel, iCiv, tSeaPlot, 1)
		elif iCiv == iManchuria:
			utils.createSettlers(iCiv, 2)
			utils.makeUnit(iMusketeer, iCiv, tPlot, 3)
			utils.makeUnit(iEightBanner, iCiv, tPlot, 5)
			utils.makeUnit(iBombard, iCiv, tPlot, 3)
		elif iCiv == iGermany:
			utils.createSettlers(iCiv, 4)
			utils.createMissionaries(iCiv, 2)
			utils.makeUnit(iArquebusier, iCiv, tPlot, 3, "", 2)
			utils.makeUnitAI(iArquebusier, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iBombard, iCiv, tPlot, 3, "", 2)
			if utils.getHumanID() != iGermany:
				utils.makeUnit(iArquebusier, iCiv, tPlot, 10, "", 2)
				utils.makeUnit(iBombard, iCiv, tPlot, 5, "", 2)
		elif iCiv == iAmerica:
			utils.createSettlers(iCiv, 8)
			utils.makeUnit(iGrenadier, iCiv, tPlot, 2)
			utils.makeUnit(iMinuteman, iCiv, tPlot, 4)
			utils.makeUnit(iCannon, iCiv, tPlot, 2)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 2)
				utils.makeUnit(iGalleon, iCiv, tSeaPlot, 2)
				utils.makeUnit(iFrigate, iCiv, tSeaPlot, 1)
			if utils.getHumanID() != iAmerica:
				utils.makeUnitAI(iMinuteman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			iReligion = self.findAreaReligion(iCiv, utils.getPlotList((23, 40), (33, 52)))
			if iReligion >= 0:
				pAmerica.setLastStateReligion(iReligion)
				utils.makeUnit(iMissionary + iReligion, iCiv, tPlot, 1)
		elif iCiv == iArgentina:
			utils.createSettlers(iCiv, 2)
			utils.makeUnit(iMusketeer, iCiv, tPlot, 3, "", 2)
			utils.makeUnit(iGrenadierCavalry, iCiv, tPlot, 3, "", 2)
			utils.makeUnit(iCannon, iCiv, tPlot, 2, "", 2)
			tSeaPlot = self.findSeaPlots(tPlot, 2, iCiv)
			if tSeaPlot:
				utils.makeUnit(iGalleon, iCiv, tSeaPlot, 1)
				utils.makeUnit(iFrigate, iCiv, tSeaPlot, 2)
			if utils.getHumanID() != iArgentina:
				utils.makeUnitAI(iMusketeer, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
				utils.makeUnit(iMusketeer, iCiv, tPlot, 2, "", 2)
				utils.makeUnit(iGrenadierCavalry, iCiv, tPlot, 2, "", 2)
				utils.makeUnit(iCannon, iCiv, tPlot, 2, "", 2)
		elif iCiv == iBrazil:
			utils.createSettlers(iCiv, 5)
			utils.makeUnit(iGrenadier, iCiv, tPlot, 3)
			utils.makeUnit(iMusketeer, iCiv, tPlot, 3)
			utils.makeUnit(iCannon, iCiv, tPlot, 2)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 2)
				utils.makeUnit(iGalleon, iCiv, tSeaPlot, 2)
				utils.makeUnit(iFrigate, iCiv, tSeaPlot, 3)
			if utils.getHumanID() != iBrazil:
				utils.makeUnitAI(iRifleman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
		elif iCiv == iAustralia:
			utils.createSettlers(iCiv, 4)
			utils.makeUnit(iDragoon, iCiv, tPlot, 2)
			utils.makeUnit(iRifleman, iCiv, tPlot, 4)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
				utils.makeUnit(iGalleon, iCiv, tSeaPlot, 2)
				utils.makeUnit(iFrigate, iCiv, tSeaPlot, 1)
			iReligion = self.findAreaReligion(iCiv, utils.getPlotList(vic.tAustraliaTL, vic.tAustraliaBR))
			if iReligion >= 0:
				pAustralia.setLastStateReligion(iReligion)
				utils.makeUnit(iMissionary + iReligion, iCiv, tPlot, 1)
			else:
				pAustralia.setLastStateReligion(iProtestantism)
		elif iCiv == iBoers:
			utils.createSettlers(iCiv, 3, utils.getPlotList((60, 9), (17, 15)))
			utils.makeUnit(iRifleman, iCiv, tPlot, 4)
			utils.makeUnit(iKommando, iCiv, tPlot, 5)
			utils.makeUnit(iCannon, iCiv, tPlot, 2)
			utils.makeUnit(iGrenadier, iCiv, tPlot, 2)
			iReligion = self.findAreaReligion(iCiv, utils.getPlotList((60, 9), (17, 15)))
			if iReligion >= 0:
				pBoers.setLastStateReligion(iReligion)
				utils.makeUnit(iMissionary + iReligion, iCiv, tPlot, 1)
			else:
				pBoers.setLastStateReligion(iProtestantism)
				utils.makeUnit(iProtestantMissionary, iCiv, tPlot, 1)
		elif iCiv == iCanada:
			utils.createSettlers(iCiv, 5)
			utils.makeUnit(iDragoon, iCiv, tPlot, 3)
			utils.makeUnit(iRifleman, iCiv, tPlot, 5)
			tSeaPlot = self.findSeaPlots(tPlot, 2, iCiv)
			if tSeaPlot:
				utils.makeUnit(iSteamship, iCiv, tSeaPlot, 2)
				utils.makeUnit(iIronclad, iCiv, tSeaPlot, 1)
				utils.makeUnit(iTorpedoBoat, iCiv, tSeaPlot, 1)
		elif iCiv == iIsrael:
			utils.makeUnit(iInfantry, iCiv, tPlot, 3)
			utils.makeUnit(iTank, iCiv, tPlot, 3)
			utils.makeUnit(iFighter, iCiv, tPlot, 3)
			utils.makeUnit(iSpy, iCiv, tPlot, 3)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
				utils.makeUnit(iTransport, iCiv, tSeaPlot, 1)
				
		# Leoreth: start wars on spawn when the spawn actually happens
		self.startWarsOnSpawn(iCiv, false)

	def createRespawnUnits(self, iCiv, tPlot):
		if iCiv == iPersia:
			utils.makeUnit(iQizilbash, iCiv, tPlot, 6)
			utils.makeUnit(iBombard, iCiv, tPlot, 3)
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
			if utils.getHumanID() != iCiv:
				utils.makeUnit(iQizilbash, iCiv, tPlot, 6)
				utils.makeUnit(iBombard, iCiv, tPlot, 3)
		elif iCiv == iAztecs:
			utils.makeUnit(iDragoon, iCiv, tPlot, 4, "", 2)
			utils.makeUnit(iMusketeer, iCiv, tPlot, 5, "", 2)
			utils.makeUnit(iGrenadier, iCiv, tPlot, 2, "", 2)
			utils.makeUnit(iWorker, iCiv, tPlot, 3, "", 2)
		elif iCiv == iMaya:
			utils.makeUnit(iMusketeer, iCiv, tPlot, 5, "", 2)
			utils.makeUnit(iCannon, iCiv, tPlot, 5, "", 2)
			utils.makeUnit(iAlbionLegion, iCiv, tPlot, 5, "", 2)
			utils.makeUnit(iWorker, iCiv, tPlot, 3, "", 2)
			tSeaPlot = self.findSeaPlots(tPlot, 3, iCiv)
			if tSeaPlot:
				utils.makeUnit(iGalleon, iCiv, tSeaPlot, 1)
				utils.makeUnit(iFrigate, iCiv, tSeaPlot, 1)
		
		self.startWarsOnSpawn(iCiv, true)
		
	def findAreaReligion(self, iPlayer, lPlots):
		lReligions = [0 for i in range(iNumReligions)]
		
		for (x, y) in lPlots:
			plot = gc.getMap().plot(x, y)
			if plot.isCity():
				city = plot.getPlotCity()
				iOwner = city.getOwner()
				if iOwner != iPlayer:
					for iReligion in range(iNumReligions):
						if city.isHasReligion(iReligion):
							lReligions[iReligion] += 1
					iStateReligion = gc.getPlayer(iOwner).getStateReligion()
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

				
	def createStartingWorkers( self, iCiv, tPlot ):
		if iCiv == iNubia:
			utils.makeUnit(iWorker, iCiv, tPlot, 1)
		if iCiv == iChina:
			utils.makeUnit(iWorker, iCiv, tPlot, 1)
		elif iCiv == iIndia:
			#utils.makeUnit(iPunjabiWorker, iCiv, tPlot, 2)
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iGreece:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iPersia:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iCeltia:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iCarthage:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iRome:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iMaya:
			utils.makeUnit(iWorker, iCiv, tPlot, 1)
		elif iCiv == iJapan:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iTamils:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iEthiopia:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iVietnam:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iTeotihuacan:
			utils.makeUnit(iArtisan, iCiv, tPlot, 2)
		elif iCiv == iMississippi:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iKorea:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iTiwanaku:
			utils.makeUnit(iWorker, iCiv, tPlot, 1)
		elif iCiv == iByzantium:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
			#utils.makeUnit(iSettler, iCiv, tPlot, 1)
		elif iCiv == iWari:
			utils.makeUnit(iWorker, iCiv, tPlot, 1)
		elif iCiv == iVikings:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iTurks:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iArabia:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iTibet:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iKhmer:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iMuisca:
			utils.makeUnit(iWorker, iCiv, tPlot, 1)
		elif iCiv == iIndonesia:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iBurma:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iKhazars:
			utils.makeUnit(iWorker, iCiv, tPlot, 1)
		elif iCiv == iChad:
			utils.makeUnit(iWorker, iCiv, tPlot, 1)
		elif iCiv == iMoors:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iSpain:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iFrance:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iOman:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iYemen:
			utils.makeUnit(iArchitect, iCiv, tPlot, 1)
		elif iCiv == iEngland:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iHolyRome:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iRussia:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iKievanRus:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iHungary:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iNetherlands:
			utils.makeUnit(iWorker, iCiv, tPlot, 3) 
		elif iCiv == iPhilippines:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iChimu:
			utils.makeUnit(iWorker, iCiv, tPlot, 1)
		elif iCiv == iSwahili:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iMali:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iPoland:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
			if utils.getHumanID() != iPoland:
				iRand = gc.getGame().getSorenRandNum(5, 'Random city spot')
				if iRand == 0: tCityPlot = (65, 55) # Memel
				elif iRand == 1: tCityPlot = (65, 54) # Koenigsberg
				else: tCityPlot = (64, 54) # Gdansk
				utils.makeUnit(iSettler, iCiv, tCityPlot, 1)
				utils.makeUnit(iLongbowman, iCiv, tCityPlot, 1)
		elif iCiv == iOttomans:
			utils.makeUnit(iWorker, iCiv, tPlot, 4)
			#utils.makeUnit(iSettler, iCiv, tPlot, 3)
		elif iCiv == iZimbabwe:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iPortugal:
			utils.makeUnit(iWorker, iCiv, tPlot, 3) 
		elif iCiv == iInca:
			utils.makeUnit(iWorker, iCiv, tPlot, 4)
		elif iCiv == iItaly:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iNigeria:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iMongolia:
			utils.makeUnit(iWorker, iCiv, tPlot, 4)
		elif iCiv == iAztecs:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iMughals:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iThailand:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iCongo:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iSweden:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iManchuria:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iGermany:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iAmerica:
			utils.makeUnit(iWorker, iCiv, tPlot, 4)
		elif iCiv == iBrazil:
			utils.makeUnit(iMadeireiro, iCiv, tPlot, 3)
		elif iCiv == iArgentina:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iAustralia:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iBoers:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iCanada:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iIsrael:
			utils.makeUnit(iLabourer, iCiv, tPlot, 2)
			
	def create1700ADstartingUnits(self):

		# Japan
		tCapital = Areas.getCapital(iJapan)
		if utils.getHumanID() != iJapan:
			utils.makeUnit(iSettler, iJapan, tCapital, 1)
		
		for iPlayer in range(iNumPlayers):
			if tBirth[iPlayer] > utils.getScenarioStartYear() and utils.getHumanID() == iPlayer:
				utils.makeUnit(iSettler, iPlayer, Areas.getCapital(iPlayer), 1)
				utils.makeUnit(iMilitia, iPlayer, Areas.getCapital(iPlayer), 1)

	def create600ADstartingUnits( self ):

		tCapital = Areas.getCapital(iChina)
		utils.makeUnit(iSwordsman, iChina, tCapital, 2)
		utils.makeUnit(iArcher, iChina, tCapital, 1)
		utils.makeUnitAI(iSpearman, iChina, tCapital, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
		utils.makeUnit(iChokonu, iChina, tCapital, 2)
		utils.makeUnit(iHorseArcher, iChina, tCapital, 1)
		utils.makeUnit(iWorker, iChina, tCapital, 2)
		
		tCapital = Areas.getCapital(iJapan)
		tSeaPlot = self.findSeaPlots(tCapital, 1, iJapan)
		if tSeaPlot:
			utils.makeUnit(iWorkboat, iJapan, tSeaPlot, 2)
			
		if utils.getHumanID() != iJapan:
			utils.makeUnit(iCrossbowman, iJapan, tCapital, 2)
			utils.makeUnit(iSamurai, iJapan, tCapital, 3)

		tCapital = Areas.getCapital(iByzantium)
		tSeaPlot = self.findSeaPlots(tCapital, 1, iByzantium)
		if tSeaPlot:
			utils.makeUnit(iGalley, iByzantium, tSeaPlot, 2)
			utils.makeUnit(iWarGalley, iByzantium, tSeaPlot, 2)

		tCapital = Areas.getCapital(iVikings)
		tSeaPlot = self.findSeaPlots(tCapital, 1, iVikings)
		if tSeaPlot:
			utils.makeUnit(iWorkboat, iVikings, tSeaPlot, 1)
			if utils.getHumanID() == iVikings:
				utils.makeUnitAI(iGalley, iVikings, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA, 1)
				utils.makeUnit(iSettler, iVikings, tSeaPlot, 1)
				utils.makeUnit(iArcher, iVikings, tSeaPlot, 1)
				utils.makeUnitAI(iLongship, iVikings, tSeaPlot, UnitAITypes.UNITAI_EXPLORE_SEA, 2)
			else:
				utils.makeUnitAI(iLongship, iVikings, tSeaPlot, UnitAITypes.UNITAI_EXPLORE_SEA, 3)
				
		# start AI settler and garrison in Denmark and Sweden
		if utils.getHumanID() != iVikings:
			utils.makeUnit(iSettler, iVikings, (60, 56), 1)
			utils.makeUnit(iArcher, iVikings, (60, 56), 1)
			utils.makeUnit(iSettler, iVikings, (63, 59), 1)
			utils.makeUnit(iArcher, iVikings, (63, 59), 1)
		else:
			utils.makeUnit(iSettler, iVikings, tCapital, 1)
			utils.makeUnit(iArcher, iVikings, tCapital, 2)

		tCapital = Areas.getCapital(iKorea)
		if utils.getHumanID() != iKorea:
			utils.makeUnit(iHeavySwordsman, iKorea, tCapital, 2)
			
		for iPlayer in range(iNumPlayers):
			if tBirth[iPlayer] > utils.getScenarioStartYear() and gc.getPlayer(iPlayer).isHuman():
				tCapital = Areas.getCapital(iPlayer)
				utils.makeUnit(iSettler, iPlayer, tCapital, 1)
				utils.makeUnit(iMilitia, iPlayer, tCapital, 1)
				
		tCapital = Areas.getCapital(iTurks)
		utils.makeUnit(iSettler, iTurks, tCapital, 2)
		utils.makeUnit(iOghuz, iTurks, tCapital, 6)
		utils.makeUnit(iArcher, iTurks, tCapital, 1)
		utils.makeUnit(iScout, iTurks, tCapital, 1)


	def create4000BCstartingUnits(self):
	
		for iPlayer in range(iNumPlayers):
			tCapital = Areas.getCapital(iPlayer)
			
			if tBirth[iPlayer] > utils.getScenarioStartYear() and gc.getPlayer(iPlayer).isHuman():
				utils.makeUnit(iSettler, iPlayer, tCapital, 1)
				utils.makeUnit(iMilitia, iPlayer, tCapital, 1)
				
			if iPlayer == iHarappa and data.players[iHarappa].iSpawnType != iNoSpawn:
				utils.makeUnit(iCityBuilder, iPlayer, tCapital, 1)
				utils.makeUnit(iMilitia, iPlayer, tCapital, 1)
		
	def assignTechs(self, iPlayer):
		Civilizations.initPlayerTechs(iPlayer)
				
		sta.onCivSpawn(iPlayer)

	def arabianSpawn(self):
		tBaghdad = (77, 40)
		tCairo = (69, 35)
		tMecca = (75, 33)

		bBaghdad = gc.getMap().plot(tBaghdad[0], tBaghdad[1]).getOwner() == iArabia
		bCairo = gc.getMap().plot(tCairo[0], tCairo[1]).getOwner() == iArabia
		
		lCities = []
		
		if bBaghdad: lCities.append(tBaghdad)
		if bCairo: lCities.append(tCairo)
		
		tCapital = utils.getRandomEntry(lCities)
		
		if tCapital:
			if utils.getHumanID() != iArabia:
				utils.moveCapital(iArabia, tCapital)
				utils.makeUnit(iMobileGuard, iArabia, tCapital, 3)
				utils.makeUnit(iGhazi, iArabia, tCapital, 2)
			utils.makeUnit(iMobileGuard, iArabia, tCapital, 2)
			utils.makeUnit(iGhazi, iArabia, tCapital, 2)
		
		if bBaghdad:
			utils.makeUnit(iSettler, iArabia, tBaghdad, 1)
			utils.makeUnit(iWorker, iArabia, tBaghdad, 1)
		
		if bCairo:
			utils.makeUnit(iSettler, iArabia, tCairo, 1)
			utils.makeUnit(iWorker, iArabia, tCairo, 1)
			
		if len(lCities) < 2:
			utils.makeUnit(iSettler, iArabia, tMecca, 2 - len(lCities))
			utils.makeUnit(iWorker, iArabia, tMecca, 2 - len(lCities))

		if utils.getHumanID() != iArabia and bBaghdad:
			utils.makeUnit(iSpearman, iArabia, tBaghdad, 2)
			
	def germanSpawn(self):
		if data.getStabilityLevel(iHolyRome) < iStabilityShaky: data.setStabilityLevel(iHolyRome, iStabilityShaky)
			
		utils.setReborn(iHolyRome, True)
		
		dc.nameChange(iHolyRome)
		dc.adjectiveChange(iHolyRome)
		
	def holyRomanSpawn(self):
		plot = gc.getMap().plot(60, 56)
		if plot.isCity(): plot.getPlotCity().setCulture(iVikings, 5, True)
		
				
	def determineEnabledPlayers(self):
		for iPlayer in range(iNumPlayers):
			if iPlayer == utils.getHumanID():
				data.players[iPlayer].iSpawnType = iForcedSpawn
			else:
				data.players[iPlayer].iSpawnType = dSpawnTypes[iPlayer]
	
		# iHuman = utils.getHumanID()
		
		# iRand = gc.getDefineINT("PLAYER_OCCURRENCE_POLYNESIA")
		# if iRand <= 0:
			# data.setPlayerEnabled(iPolynesia, False)
		# elif gc.getGame().getSorenRandNum(iRand, 'Polynesia enabled?') != 0:
			# data.setPlayerEnabled(iPolynesia, False)
			
		# iRand = gc.getDefineINT("PLAYER_OCCURRENCE_HARAPPA")
		# if iRand <= 0:
			# data.setPlayerEnabled(iHarappa, False)
		# elif gc.getGame().getSorenRandNum(iRand, 'Harappa enabled?') != 0:
			# data.setPlayerEnabled(iHarappa, False)
		
		# if iHuman != iIndia and iHuman != iIndonesia:
			# iRand = gc.getDefineINT("PLAYER_OCCURRENCE_TAMILS")
			
			# if iRand <= 0:
				# data.setPlayerEnabled(iTamils, False)
			# elif gc.getGame().getSorenRandNum(iRand, 'Tamils enabled?') != 0:
				# data.setPlayerEnabled(iTamils, False)
				
		# if iHuman != iChina and iHuman != iIndia and iHuman != iMughals:
			# iRand = gc.getDefineINT("PLAYER_OCCURRENCE_TIBET")
			
			# if iRand <= 0:
				# data.setPlayerEnabled(iTibet, False)
			# elif gc.getGame().getSorenRandNum(iRand, 'Tibet enabled?') != 0:
				# data.setPlayerEnabled(iTibet, False)
				
		# if iHuman != iSpain and iHuman != iMali:
			# iRand = gc.getDefineINT("PLAYER_OCCURRENCE_MOORS")
			
			# if iRand <= 0:
				# data.setPlayerEnabled(iMoors, False)
			# elif gc.getGame().getSorenRandNum(iRand, 'Moors enabled?') != 0:
				# data.setPlayerEnabled(iMoors, False)
				
		# if iHuman != iHolyRome and iHuman != iGermany and iHuman != iRussia:
			# iRand = gc.getDefineINT("PLAYER_OCCURRENCE_POLAND")
			
			# if iRand <= 0:
				# data.setPlayerEnabled(iPoland, False)
			# elif gc.getGame().getSorenRandNum(iRand, 'Poland enabled?') != 0:
				# data.setPlayerEnabled(iPoland, False)
				
		# if iHuman != iMali and iHuman != iPortugal:
			# iRand = gc.getDefineINT("PLAYER_OCCURRENCE_CONGO")
			
			# if iRand <= 0:
				# data.setPlayerEnabled(iCongo, False)
			# elif gc.getGame().getSorenRandNum(iRand, 'Congo enabled?') != 0:
				# data.setPlayerEnabled(iCongo, False)
				
		# if iHuman != iSpain:
			# iRand = gc.getDefineINT("PLAYER_OCCURRENCE_ARGENTINA")
			
			# if iRand <= 0:
				# data.setPlayerEnabled(iArgentina, False)
			# elif gc.getGame().getSorenRandNum(iRand, 'Argentina enabled?') != 0:
				# data.setPlayerEnabled(iArgentina, False)
				
		# if iHuman != iPortugal:
			# iRand = gc.getDefineINT("PLAYER_OCCURRENCE_BRAZIL")
			
			# if iRand <= 0:
				# data.setPlayerEnabled(iBrazil, False)
			# elif gc.getGame().getSorenRandNum(iRand, 'Brazil enabled?') != 0:
				# data.setPlayerEnabled(iBrazil, False)
				
	def placeHut(self, tTL, tBR):
		plotList = []
		
		for (x, y) in utils.getPlotList(tTL, tBR):
			plot = gc.getMap().plot(x, y)
			if plot.isFlatlands() or plot.isHills():
				if plot.getFeatureType() != iMud:
					if plot.getOwner() < 0:
						plotList.append((x, y))
		
		if not plotList:
			#utils.debugTextPopup('List empty: ' + str(tTL) + ' ' + str(tBR))
			return
		
		tPlot = utils.getRandomEntry(plotList)
		i, j = tPlot
		
		gc.getMap().plot(i, j).setImprovementType(iHut)
		
	def setStateReligion(self, iCiv):
		lCities = utils.getAreaCities(Areas.getCoreArea(iCiv))
		lReligions = [0 for i in range(iNumReligions)]
		
		for city in lCities:
			if city.getReligionCount() == 0:
				iOwner = city.getOwner()
				if iOwner == iCiv:
					iOwner = city.getPreviousOwner()

				if iOwner != -1:
					iReligion = gc.getPlayer(iOwner).getStateReligion()
					if iReligion >= 0:
						lReligions[iReligion] += 1
						continue
		
			for iReligion in range(iNumReligions):
				if iReligion not in [iJudaism] and city.isHasReligion(iReligion): lReligions[iReligion] += 1
				
		iHighestEntry = utils.getHighestEntry(lReligions)
		
		if iHighestEntry > 0:
			gc.getPlayer(iCiv).setLastStateReligion(lReligions.index(iHighestEntry))
			
rnf = RiseAndFall()