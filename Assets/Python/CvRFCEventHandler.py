from CvPythonExtensions import *
import CvUtil
import PyHelpers 
import Popup as PyPopup 

from StoredData import data # edead
import RiseAndFall
import Barbs
import Religions
import Resources
import CityNameManager as cnm
import UniquePowers     
import AIWars
import Congresses as cong
from Consts import *
from RFCUtils import utils
import CvScreenEnums #Rhye
import Victory as vic
import Stability as sta
import Plague
import Communications
import Companies
import DynamicCivs as dc
import Modifiers
import SettlerMaps
import WarMaps
import RegionMap
import Areas
import Civilizations
import AIParameters
import GreatPeople as gp

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
localText = CyTranslator()

class CvRFCEventHandler:

	def __init__(self, eventManager):

		self.EventKeyDown=6
		self.bStabilityOverlay = False

		# initialize base class
		eventManager.addEventHandler("GameStart", self.onGameStart) #Stability
		eventManager.addEventHandler("BeginGameTurn", self.onBeginGameTurn) #Stability
		eventManager.addEventHandler("cityAcquired", self.onCityAcquired) #Stability
		eventManager.addEventHandler("cityRazed", self.onCityRazed) #Stability
		eventManager.addEventHandler("cityBuilt", self.onCityBuilt) #Stability
		eventManager.addEventHandler("combatResult", self.onCombatResult) #Stability
		eventManager.addEventHandler("changeWar", self.onChangeWar)
		eventManager.addEventHandler("religionFounded",self.onReligionFounded) #Victory
		eventManager.addEventHandler("buildingBuilt",self.onBuildingBuilt) #Victory
		eventManager.addEventHandler("projectBuilt",self.onProjectBuilt) #Victory
		eventManager.addEventHandler("BeginPlayerTurn", self.onBeginPlayerTurn)
		eventManager.addEventHandler("kbdEvent",self.onKbdEvent)
		eventManager.addEventHandler("OnLoad",self.onLoadGame) #edead: StoredData
		eventManager.addEventHandler("techAcquired",self.onTechAcquired) #Stability
		eventManager.addEventHandler("religionSpread",self.onReligionSpread) #Stability
		eventManager.addEventHandler("firstContact",self.onFirstContact)
		eventManager.addEventHandler("OnPreSave",self.onPreSave) #edead: StoredData
		eventManager.addEventHandler("vassalState", self.onVassalState)
		eventManager.addEventHandler("revolution", self.onRevolution)
		eventManager.addEventHandler("cityGrowth", self.onCityGrowth)
		eventManager.addEventHandler("unitPillage", self.onUnitPillage)
		eventManager.addEventHandler("cityCaptureGold", self.onCityCaptureGold)
		eventManager.addEventHandler("playerGoldTrade", self.onPlayerGoldTrade)
		eventManager.addEventHandler("tradeMission", self.onTradeMission)
		eventManager.addEventHandler("playerSlaveTrade", self.onPlayerSlaveTrade)
		eventManager.addEventHandler("playerChangeStateReligion", self.onPlayerChangeStateReligion)
				
		#Leoreth
		eventManager.addEventHandler("greatPersonBorn", self.onGreatPersonBorn)
		eventManager.addEventHandler("unitCreated", self.onUnitCreated)
		eventManager.addEventHandler("unitBuilt", self.onUnitBuilt)
		eventManager.addEventHandler("plotFeatureRemoved", self.onPlotFeatureRemoved)
		eventManager.addEventHandler("goldenAge", self.onGoldenAge)
		eventManager.addEventHandler("releasedPlayer", self.onReleasedPlayer)
		eventManager.addEventHandler("cityAcquiredAndKept", self.onCityAcquiredAndKept)
		eventManager.addEventHandler("blockade", self.onBlockade)
		eventManager.addEventHandler("peaceBrokered", self.onPeaceBrokered)
		eventManager.addEventHandler("EndPlayerTurn", self.onEndPlayerTurn)
	       
		self.eventManager = eventManager

		self.rnf = RiseAndFall.RiseAndFall()
		self.barb = Barbs.Barbs()
		self.rel = Religions.Religions()
		self.res = Resources.Resources()
		self.up = UniquePowers.UniquePowers()
		self.aiw = AIWars.AIWars()
		self.pla = Plague.Plague()
		self.com = Communications.Communications()
		self.corp = Companies.Companies()

	def onGameStart(self, argsList):
		'Called at the start of the game'
		
		data.setup()

		self.rnf.setup()
		self.pla.setup()
		dc.setup()
		self.aiw.setup()
		self.up.setup()
		
		vic.setup()
		cong.setup()
		
		# Leoreth: set DLL core values
		Modifiers.init()
		Areas.init()
		SettlerMaps.init()
		WarMaps.init()
		RegionMap.init()
		Civilizations.init()
		AIParameters.init()
		
		return 0


	def onCityAcquired(self, argsList):
		iOwner, iPlayer, city, bConquest, bTrade = argsList
		tCity = (city.getX(), city.getY())
		
		cnm.onCityAcquired(city, iPlayer)
		
		if bConquest:
			sta.onCityAcquired(city, iOwner, iPlayer)
			
		if iPlayer == iArabia:
			self.up.arabianUP(city)
		# elif iPlayer == iMughals and utils.getHumanID() != iMughals:
			# self.up.mughalUP(city)
		# elif iPlayer == iSeljuks:
			# self.up.seljukUP(city)
			
		if iPlayer == iMongolia and bConquest and utils.getHumanID() != iPlayer:
			self.up.mongolUP(city)
			
		if iPlayer < iNumMajorPlayers:
			utils.spreadMajorCulture(iPlayer, tCity)
		
		# relocate capitals
		if utils.getHumanID() != iPlayer:
			if iPlayer == iTurkey and tCity == (68, 45):
				utils.moveCapital(iTurkey, tCity) # Kostantiniyye
			elif iPlayer == iMongolia and tCity == (102, 47):
				utils.moveCapital(iMongolia, tCity) # Khanbaliq
				
		# remove slaves if unable to practice slavery
		if not gc.getPlayer(iPlayer).isColonialSlavery():
			utils.removeSlaves(city)
		else:
			utils.freeSlaves(city, iPlayer)
			
		if city.isCapital():
			if city.isHasRealBuilding(iAdministrativeCenter): 
				city.setHasRealBuilding(iAdministrativeCenter, False)	
							
		# kill Seljuks
		#if iOwner == iSeljuks and gc.getPlayer(iSeljuks).isAlive() and gc.getGame().getGameTurnYear() >= 1250:
		#	if city.isCapital() or gc.getPlayer(iSeljuks).getNumCities() <= 2:
		#		sta.completeCollapse(iSeljuks)
				#utils.killAndFragmentCiv(iSeljuks, iIndependent, iIndependent2, -1, False)
				
		# Leoreth: relocate capital for AI if reacquired:
		if utils.getHumanID() != iPlayer and iPlayer < iNumPlayers:
			if data.players[iPlayer].iResurrections == 0:
				if Areas.getCapital(iPlayer) == tCity:
					utils.relocateCapital(iPlayer, city)
			else:
				if Areas.getRespawnCapital(iPlayer) == tCity:
					utils.relocateCapital(iPlayer, city)
					
		# Leoreth: conquering Constantinople adds it to the Turkish core + Rumelia
		if iPlayer == iTurkey and tCity == (68, 45):
			utils.setReborn(iTurkey, True)
					
		# Leoreth: help Byzantium/Constantinople
		if iPlayer == iByzantium and tCity == Areas.getCapital(iByzantium) and gc.getGame().getGameTurn() <= getTurnForYear(330)+3:
			if city.getPopulation() < 5:
				city.setPopulation(5)
				
			city.setHasRealBuilding(iBarracks, True)
			city.setHasRealBuilding(iWalls, True)
			city.setHasRealBuilding(iLibrary, True)
			city.setHasRealBuilding(iMarket, True)
			city.setHasRealBuilding(iGranary, True)
			city.setHasRealBuilding(iHarbor, True)
			city.setHasRealBuilding(iForge, True)
			
			city.setName("Konstantinoupolis", False)
			
			city.setHasRealBuilding(iTemple + 4*gc.getPlayer(iPlayer).getStateReligion(), True)
			
		if bConquest:

			# Colombian UP: no resistance in conquered cities in Latin America
			if iPlayer == iMaya and utils.isReborn(iMaya):
				if utils.isPlotInArea(tCity, tSouthCentralAmericaTL, tSouthCentralAmericaBR):
					city.setOccupationTimer(0)
					
			# Statue of Zeus effect: no city resistance on conquest
			if gc.getPlayer(iPlayer).isHasBuildingEffect(iStatueOfZeus):
				city.setOccupationTimer(0)
				
			# Byzantium reduced to four cities: core shrinks to Constantinople
			if iOwner == iByzantium and gc.getPlayer(iByzantium).getNumCities <= 4:
				utils.setReborn(iByzantium, True)
					
		if bTrade:
			for i in range(iNumBuildings):
				iNationalWonder = i
				if isNationalWonderClass(gc.getBuildingInfo(iNationalWonder).getBuildingClassType()) and city.hasBuilding(iNationalWonder):
					city.setHasRealBuilding(iNationalWonder, False)
					
		self.pla.onCityAcquired(iOwner, iPlayer, city) # Plague
		self.com.onCityAcquired(city) # Communications
		self.corp.onCityAcquired(argsList) # Companies
		dc.onCityAcquired(iOwner, iPlayer) # DynamicCivs
		
		vic.onCityAcquired(iPlayer, iOwner, city, bConquest)
		
		return 0
		
	def onCityAcquiredAndKept(self, argsList):
		iPlayer, city = argsList
		iOwner = city.getPreviousOwner()
		
		if city.isCapital():
			self.rnf.createStartingWorkers(iPlayer, (city.getX(), city.getY()))
		
		#utils.debugTextPopup('City acquired and kept: ' + city.getName() + '\nPlayer: ' + gc.getPlayer(iPlayer).getCivilizationShortDescription(0) + '\nOwner: ' + gc.getPlayer(iOwner).getCivilizationShortDescription(0))
		
		lTradingCompanyList = [iSpain, iFrance, iEngland, iPortugal, iNetherlands]
			
		if iPlayer == iSeljuks or gc.getPlayer(iPlayer).isHasBuildingEffect(iTopkapiPalace):
			self.up.turkishUP(city, iPlayer, iOwner)
		elif iPlayer in lTradingCompanyList and (city.getX(), city.getY()) in tTradingCompanyPlotLists[lTradingCompanyList.index(iPlayer)]:
			self.up.tradingCompanyCulture(city, iPlayer, iOwner)
		else:
			utils.cityConquestCulture(city, iPlayer, iOwner)

	def onCityRazed(self, argsList):
		city, iPlayer = argsList

		dc.onCityRazed(city.getOwner())
		self.pla.onCityRazed(city, iPlayer) #Plague
			
		vic.onCityRazed(iPlayer, city)	
		sta.onCityRazed(iPlayer, city)

	def onCityBuilt(self, argsList):
		city = argsList[0]
		iOwner = city.getOwner()
		tCity = (city.getX(), city.getY())
		x, y = tCity
		
		if iOwner < iNumActivePlayers: 
			cnm.onCityBuilt(city)
			
		# starting workers
		if city.isCapital():
			self.rnf.createStartingWorkers(iOwner, tCity)

		#Rhye - delete culture of barbs and minor civs to prevent weird unhappiness
		pPlot = gc.getMap().plot(x, y)
		for i in range(iNumTotalPlayers - iNumActivePlayers):
			iMinorCiv = i + iNumActivePlayers
			pPlot.setCulture(iMinorCiv, 0, True)
		pPlot.setCulture(iBarbarian, 0, True)

		if iOwner < iNumMajorPlayers:
			utils.spreadMajorCulture(iOwner, tCity)
			if gc.getPlayer(iOwner).getNumCities() < 2:
				gc.getPlayer(iOwner).AI_updateFoundValues(False); # fix for settler maps not updating after 1st city is founded

		if iOwner == iTurkey:
			self.up.turkishUP(city, iOwner, -1)
			
		if iOwner == iCarthage:
			if tCity == (58, 39):
				if not gc.getPlayer(iCarthage).isHuman():
					x = gc.getPlayer(iCarthage).getCapitalCity().getX()
					y = gc.getPlayer(iCarthage).getCapitalCity().getY()
					carthage = gc.getMap().plot(58, 39).getPlotCity()
					carthage.setHasRealBuilding(iPalace, True)
					gc.getMap().plot(x, y).getPlotCity().setHasRealBuilding(iPalace, False)
					dc.onPalaceMoved(iCarthage)
					
					carthage.setPopulation(3)
					
					utils.makeUnitAI(iWorkboat, iCarthage, (58, 39), UnitAITypes.UNITAI_WORKER_SEA, 1)
					utils.makeUnitAI(iGalley, iCarthage, (57, 40), UnitAITypes.UNITAI_SETTLER_SEA, 1)
					utils.makeUnitAI(iSettler, iCarthage, (57, 40), UnitAITypes.UNITAI_SETTLE, 1)
					
				utils.setReborn(iCarthage, True)
				
		if iOwner == iByzantium and tCity == Areas.getCapital(iByzantium) and gc.getGame().getGameTurn() <= getTurnForYear(330)+3:
			if city.getPopulation() < 5:
				city.setPopulation(5)
				
			city.setHasRealBuilding(iBarracks, True)
			city.setHasRealBuilding(iWalls, True)
			city.setHasRealBuilding(iLibrary, True)
			city.setHasRealBuilding(iMarket, True)
			city.setHasRealBuilding(iGranary, True)
			city.setHasRealBuilding(iHarbor, True)
			city.setHasRealBuilding(iForge, True)
			
			city.setHasRealBuilding(iTemple + 4*gc.getPlayer(iOwner).getStateReligion(), True)
			
		if iOwner == iPortugal and tCity == Areas.getCapital(iPortugal) and gc.getGame().getGameTurn() <= getTurnForYear(tBirth[iPortugal]) + 3:
			city.setPopulation(5)
			
			for iBuilding in [iLibrary, iMarket, iHarbor, iLighthouse, iForge, iWalls, iTemple+4*gc.getPlayer(iPortugal).getStateReligion()]:
				city.setHasRealBuilding(iBuilding, True)
			
		if iOwner == iNetherlands and tCity == Areas.getCapital(iNetherlands) and gc.getGame().getGameTurn() <= getTurnForYear(1580)+3:
			city.setPopulation(9)
			
			for iBuilding in [iLibrary, iMarket, iWharf, iLighthouse, iBarracks, iPharmacy, iBank, iAmphitheatre, iTheatre, iTemple+4*gc.getPlayer(iNetherlands).getStateReligion()]:
				city.setHasRealBuilding(iBuilding, True)
				
			gc.getPlayer(iNetherlands).AI_updateFoundValues(False)
			
		if iOwner == iItaly and tCity == Areas.getCapital(iItaly) and gc.getGame().getGameTurn() <= getTurnForYear(tBirth[iItaly])+3:
			city.setPopulation(7)
			
			for iBuilding in [iLibrary, iPharmacy, iTemple+4*gc.getPlayer(iItaly).getStateReligion(), iMarket, iArtStudio, iAqueduct, iCourthouse, iWalls]:
				city.setHasRealBuilding(iBuilding, True)
				
			gc.getPlayer(iItaly).AI_updateFoundValues(False)

		vic.onCityBuilt(iOwner, city)
			
		if iOwner < iNumPlayers:
			dc.onCityBuilt(iOwner)

		if iOwner == iArabia:
			if not gc.getGame().isReligionFounded(iIslam):
				if tCity == (75, 33):
					self.rel.foundReligion(tCity, iIslam)
				
		# Leoreth: free defender and worker for AI colonies
		if iOwner in lCivGroups[0]:
			if city.getRegionID() not in mercRegions[iArea_Europe]:
				if utils.getHumanID() != iOwner:
					utils.createGarrisons(tCity, iOwner, 1)
					utils.makeUnit(iWorker, iOwner, tCity, 1)
					
		# Holy Rome founds its capital
		if iOwner == iHolyRome:
			if gc.getPlayer(iHolyRome).getNumCities() == 1:
				self.rnf.holyRomanSpawn()

	def onPlayerChangeStateReligion(self, argsList):
		'Player changes his state religion'
		iPlayer, iNewReligion, iOldReligion = argsList
		
		if iPlayer < iNumPlayers:
			dc.onPlayerChangeStateReligion(iPlayer, iNewReligion)
			
		sta.onPlayerChangeStateReligion(iPlayer)

	def onCombatResult(self, argsList):
		self.rnf.immuneMode(argsList)
		self.up.vikingUP(argsList) # includes Moorish Corsairs
		
		pWinningUnit, pLosingUnit = argsList
		iWinningPlayer = pWinningUnit.getOwner()
		iLosingPlayer = pLosingUnit.getOwner()
		
		vic.onCombatResult(pWinningUnit, pLosingUnit)
		
		iUnitPower = 0
		pLosingUnitInfo = gc.getUnitInfo(pLosingUnit.getUnitType())
		
		if pLosingUnitInfo.getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_SIEGE"):
			iUnitPower = pLosingUnitInfo.getPowerValue()
		
		sta.onCombatResult(iWinningPlayer, iLosingPlayer, iUnitPower)
		
		# capture slaves
		if iWinningPlayer == iAztecs and not pAztecs.isReborn():
			utils.captureUnit(pLosingUnit, pWinningUnit, iAztecSlave, 35)
			
		elif iLosingPlayer == iNative:
			if iWinningPlayer not in lCivBioNewWorld or True in data.lFirstContactConquerors:
				if gc.getPlayer(iWinningPlayer).isSlavery() or gc.getPlayer(iWinningPlayer).isColonialSlavery():
					utils.captureUnit(pLosingUnit, pWinningUnit, iSlave, 35)
		
		# Maya Holkans give food to closest city on victory
		if pWinningUnit.getUnitType() == iHolkan:
			iOwner = pWinningUnit.getOwner()
			city = gc.getMap().findCity(pWinningUnit.getX(), pWinningUnit.getY(), iOwner, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
			if city: 
				city.changeFood(5)
				if utils.getHumanID() == pWinningUnit.getOwner(): data.iTeotlSacrifices += 1
				sAdjective = gc.getPlayer(pLosingUnit.getOwner()).getCivilizationAdjectiveKey()
				CyInterface().addMessage(iOwner, False, iDuration, CyTranslator().getText("TXT_KEY_MAYA_HOLKAN_EFFECT", (sAdjective, pLosingUnit.getNameKey(), 5, city.getName())), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
		
		# Brandenburg Gate effect
		if gc.getPlayer(iLosingPlayer).isHasBuildingEffect(iBrandenburgGate):
			for iPromotion in range(gc.getNumPromotionInfos()):
				if gc.getPromotionInfo(iPromotion).isLeader():
					gc.getPlayer(iLosingPlayer).restoreGeneralThreshold()
		
	def onReligionFounded(self, argsList):
		'Religion Founded'
		iReligion, iFounder = argsList
		
		if gc.getGame().getGameTurn() == utils.getScenarioStartTurn():
			return
	
		vic.onReligionFounded(iFounder, iReligion)
		self.rel.onReligionFounded(iReligion, iFounder)
		dc.onReligionFounded(iFounder)

	def onVassalState(self, argsList):
		'Vassal State'
		iMaster, iVassal, bVassal, bCapitulated = argsList
		
		if bCapitulated:
			sta.onVassalState(iMaster, iVassal)
		
		if iVassal == iInca:
			utils.setReborn(iInca, True)
			
		# move Mongolia's core south in case they vassalize China
		if bCapitulated and iVassal == iChina and iMaster == iMongolia:
			utils.setReborn(iMongolia, True)
		
		dc.onVassalState(iMaster, iVassal)

	def onRevolution(self, argsList):
		'Called at the start of a revolution'
		iPlayer = argsList[0]
		
		sta.onRevolution(iPlayer)
		
		if iPlayer < iNumPlayers:
			dc.onRevolution(iPlayer)
			
		utils.checkSlaves(iPlayer)
			
		if iPlayer in [iEgypt]:
			cnm.onRevolution(iPlayer)
			
	def onCityGrowth(self, argsList):
		'City Population Growth'
		pCity, iPlayer = argsList
		
		# Leoreth/Voyhkah: Empire State Building effect
		if pCity.isHasRealBuilding(iEmpireStateBuilding):
			iPop = pCity.getPopulation()
			pCity.setBuildingCommerceChange(gc.getBuildingInfo(iEmpireStateBuilding).getBuildingClassType(), 0, iPop)
			
	def onUnitPillage(self, argsList):
		unit, iImprovement, iRoute, iPlayer, iGold = argsList
		
		iUnit = unit.getUnitType()
		if (iPlayer == iVikings or iPlayer == iMoors) and iGold > 0 and iImprovement != -1 and iGold < 1000:
			vic.onUnitPillage(iPlayer, iGold, iUnit)
			
	def onCityCaptureGold(self, argsList):
		city, iPlayer, iGold = argsList
		
		if iPlayer == iVikings and iGold > 0:
			vic.onCityCaptureGold(iPlayer, iGold)
			
	def onPlayerGoldTrade(self, argsList):
		iFromPlayer, iToPlayer, iGold = argsList
		
		if iToPlayer == iTamils:
			vic.onPlayerGoldTrade(iToPlayer, iGold)
			
	def onTradeMission(self, argsList):
		iUnitType, iPlayer, iX, iY, iGold = argsList
		
		if iPlayer in [iTamils, iMali]:
			vic.onTradeMission(iPlayer, iX, iY, iGold)
		
	def onPlayerSlaveTrade(self, argsList):
		iPlayer, iGold = argsList
		
		if iPlayer == iCongo:
			vic.onPlayerSlaveTrade(iPlayer, iGold)
			
	def onUnitGifted(self, argsList):
		pUnit, iOwner, pPlot = argsList
			
	def onUnitCreated(self, argsList):
		utils.debugTextPopup("Unit created")
		pUnit = argsList
			
	def onUnitBuilt(self, argsList):
		city, unit = argsList
		
		if unit.getUnitType() == iSettler and city.getOwner() == iChina and utils.getHumanID() != iChina:
			utils.handleChineseCities(unit)
			
		# Leoreth: help AI by moving new slaves to the new world
		if unit.getUnitType() == iSlave and city.getRegionID() in [rIberia, rBritain, rEurope, rScandinavia, rRussia, rItaly, rBalkans, rMaghreb, rAnatolia] and utils.getHumanID() != city.getOwner():
			utils.moveSlaveToNewWorld(city.getOwner(), unit)
			
	
		
	def onBuildingBuilt(self, argsList):
		city, iBuildingType = argsList
		iOwner = city.getOwner()
		tCity = (city.getX(), city.getY())
		
		vic.onBuildingBuilt(iOwner, iBuildingType)
		self.rel.onBuildingBuilt(city, iOwner, iBuildingType)
		self.up.onBuildingBuilt(city, iOwner, iBuildingType)
		
		if iOwner < iNumPlayers:
			self.com.onBuildingBuilt(iOwner, iBuildingType, city)
		
		if isWorldWonderClass(gc.getBuildingInfo(iBuildingType).getBuildingClassType()):
			sta.onWonderBuilt(iOwner, iBuildingType)
			
		if iBuildingType == iPalace:
			sta.onPalaceMoved(iOwner)
			dc.onPalaceMoved(iOwner)
			
			if city.isHasRealBuilding(iAdministrativeCenter): city.setHasRealBuilding(iAdministrativeCenter, False)
			
			# Leoreth: in case human Phoenicia moves palace to Carthage
			if iOwner == iCarthage and tCity == (58, 39):
				utils.setReborn(iCarthage, True)

		# Leoreth: update trade routes when Porcelain Tower is built to start its effect
		if iBuildingType == iPorcelainTower:
			gc.getPlayer(iOwner).updateTradeRoutes()

		# Leoreth/Voyhkah: Empire State Building
		if iBuildingType == iEmpireStateBuilding:
			iPop = city.getPopulation()
			city.setBuildingCommerceChange(gc.getBuildingInfo(iEmpireStateBuilding).getBuildingClassType(), 0, iPop)
			
		# Leoreth: Machu Picchu
		if iBuildingType == iMachuPicchu:
			iNumPeaks = 0
			for i in range(21):
				if city.getCityIndexPlot(i).isPeak():
					iNumPeaks += 1
			city.setBuildingCommerceChange(gc.getBuildingInfo(iMachuPicchu).getBuildingClassType(), 0, iNumPeaks * 2)
			
		# Leoreth: Great Wall
		if iBuildingType == iGreatWall:
			for iPlot in range(gc.getMap().numPlots()):
				plot = gc.getMap().plotByIndex(iPlot)
				if plot.getOwner() == iOwner and not plot.isWater():
					plot.setWithinGreatWall(True)
					
	def onPlotFeatureRemoved(self, argsList):
		plot, city, iFeature = argsList
		
		if plot.getOwner() == iBrazil:
			iGold = 0
			
			if iFeature == iForest: iGold = 15
			elif iFeature == iJungle: iGold = 20
			elif iFeature == iRainforest: iGold = 20
			
			if iGold > 0:
				gc.getPlayer(iBrazil).changeGold(iGold)
				
				if utils.getHumanID() == iBrazil:
					CyInterface().addMessage(iBrazil, False, iDuration, CyTranslator().getText("TXT_KEY_DEFORESTATION_EVENT", (gc.getFeatureInfo(iFeature).getText(), city.getName(), iGold)), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getCommerceInfo(0).getButton(), ColorTypes(iWhite), plot.getX(), plot.getY(), True, True)

	def onProjectBuilt(self, argsList):
		city, iProjectType = argsList
		vic.onProjectBuilt(city.getOwner(), iProjectType)

	def onImprovementDestroyed(self, argsList):
		pass
		
	def onBeginGameTurn(self, argsList):
		iGameTurn = argsList[0]
		
		self.rnf.checkTurn(iGameTurn)
		self.barb.checkTurn(iGameTurn)
		self.rel.checkTurn(iGameTurn)
		self.res.checkTurn(iGameTurn)
		self.up.checkTurn(iGameTurn)
		self.aiw.checkTurn(iGameTurn)
		self.pla.checkTurn(iGameTurn)
		self.com.checkTurn(iGameTurn)
		self.corp.checkTurn(iGameTurn)
		
		sta.checkTurn(iGameTurn)
		cong.checkTurn(iGameTurn)
		
		if iGameTurn % 10 == 0:
			dc.checkTurn(iGameTurn)
			
		if utils.getScenario() == i3000BC and iGameTurn == getTurnForYear(600):
			for iPlayer in range(iVikings):
				Modifiers.adjustInflationModifier(iPlayer)
			
		return 0

	def onBeginPlayerTurn(self, argsList):	
		iGameTurn, iPlayer = argsList
		
		#if utils.getHumanID() == iPlayer:
		#	utils.debugTextPopup('Can contact: ' + str([gc.getPlayer(i).getCivilizationShortDescription(0) for i in range(iNumPlayers) if gc.getTeam(iPlayer).canContact(i)]))

		if (data.lDeleteMode[0] != -1):
			self.rnf.deleteMode(iPlayer)
			
		self.pla.checkPlayerTurn(iGameTurn, iPlayer)
		
		if gc.getPlayer(iPlayer).isAlive():
			vic.checkTurn(iGameTurn, iPlayer)
			
			if iPlayer < iNumPlayers and not gc.getPlayer(iPlayer).isHuman():
				self.rnf.checkPlayerTurn(iGameTurn, iPlayer) #for leaders switch

	def onGreatPersonBorn(self, argsList):
		'Great Person Born'
		pUnit, iPlayer, pCity = argsList
		
		gp.onGreatPersonBorn(pUnit, iPlayer, pCity)
		vic.onGreatPersonBorn(iPlayer, pUnit)
		sta.onGreatPersonBorn(iPlayer)

	def onReligionSpread(self, argsList):
		iReligion, iOwner, pSpreadCity = argsList
		
		cnm.onReligionSpread(iReligion, iOwner, pSpreadCity)

	def onFirstContact(self, argsList):
		iTeamX,iHasMetTeamY = argsList
		if iTeamX < iNumPlayers:
			self.rnf.onFirstContact(iTeamX, iHasMetTeamY)
		self.pla.onFirstContact(iTeamX, iHasMetTeamY)
		
		vic.onFirstContact(iTeamX, iHasMetTeamY)

	#Rhye - start
	def onTechAcquired(self, argsList):
		iTech, iTeam, iPlayer, bAnnounce = argsList

		iHuman = utils.getHumanID()
		
		iEra = gc.getTechInfo(iTech).getEra()

		if gc.getGame().getGameTurn() == utils.getScenarioStartTurn():
			return
		
		sta.onTechAcquired(iPlayer, iTech)
		AIParameters.onTechAcquired(iPlayer, iTech)

		if gc.getGame().getGameTurn() > getTurnForYear(tBirth[iPlayer]):
			vic.onTechAcquired(iPlayer, iTech)
			cnm.onTechAcquired(iPlayer)
			dc.onTechAcquired(iPlayer, iTech)

		if gc.getPlayer(iPlayer).isAlive() and gc.getGame().getGameTurn() > getTurnForYear(tBirth[iPlayer]) and iPlayer < iNumPlayers:
			self.rel.onTechAcquired(iTech, iPlayer)
			if (gc.getGame().getGameTurn() > getTurnForYear(1700)):
				self.aiw.forgetMemory(iTech, iPlayer)

		if iTech == iExploration:
			if iPlayer in [iSpain, iFrance, iEngland, iGermany, iVikings, iNetherlands, iPortugal]:
				data.players[iPlayer].iExplorationTurn = gc.getGame().getGameTurn()
				
		elif iTech == iCompass:
			if iPlayer == iVikings:
				gc.getMap().plot(49, 62).setTerrainType(iCoast, True, True)

		elif iTech == iMicrobiology:
			self.pla.onTechAcquired(iTech, iPlayer)

		elif iTech == iRailroad:
			self.rnf.onRailroadDiscovered(iPlayer)
			
		if iTech in [iExploration, iFirearms]:
			teamPlayer = gc.getTeam(iPlayer)
			if teamPlayer.isHasTech(iExploration) and teamPlayer.isHasTech(iFirearms):
				self.rnf.earlyTradingCompany(iPlayer)
			
		if iTech in [iEconomics, iReplaceableParts]:
			teamPlayer = gc.getTeam(iPlayer)
			if teamPlayer.isHasTech(iEconomics) and teamPlayer.isHasTech(iReplaceableParts):
				self.rnf.lateTradingCompany(iPlayer)
	
		if utils.getHumanID() != iPlayer:
			if iPlayer == iJapan and iEra == iIndustrial:
				utils.moveCapital(iPlayer, (116, 47)) # Toukyou
			elif iPlayer == iItaly and iEra == iIndustrial:
				utils.moveCapital(iPlayer, (60, 44)) # Roma
			elif iPlayer == iVikings and iEra == iRenaissance:
				utils.moveCapital(iPlayer, (63, 59)) # Stockholm
			elif iPlayer == iHolyRome and iEra == iRenaissance:
				utils.moveCapital(iPlayer, (62, 49)) # Wien
				
		# Spain's core extends when reaching the Renaissance and there are no Moors in Iberia
		# at the same time, the Moorish core relocates to Africa
		if iPlayer == iSpain and iEra == iRenaissance and not utils.isReborn(iSpain):
			bNoMoors = True
			if gc.getPlayer(iMoors).isAlive():
				for city in utils.getCityList(iMoors):
					if city.plot().getRegionID() == rIberia:
						bNoMoors = False
			if bNoMoors:
				utils.setReborn(iSpain, True)
				utils.setReborn(iMoors, True)
				
		# Italy's core extends when reaching the Industrial era
		if iPlayer == iItaly and iEra == iIndustrial:
			utils.setReborn(iItaly, True)
			
		# Arabia's core moves to Iraq when Education is discovered
		if iPlayer == iArabia and iTech == iEducation:
			utils.setReborn(iArabia, True)
			
		# Japan's core extends when reaching the Industrial era
		if iPlayer == iJapan and iEra == iIndustrial:
			utils.setReborn(iJapan, True)
			
		# Germany's core shrinks when reaching the Digital era
		if iPlayer == iGermany and iEra == iDigital:
			utils.setReborn(iGermany, True)
		

	def onPreSave(self, argsList):
		'called before a game is actually saved'
		pass

	def onLoadGame(self, argsList):
		pass
		
	def onChangeWar(self, argsList):
		bWar, iTeam, iOtherTeam = argsList
		
		sta.onChangeWar(bWar, iTeam, iOtherTeam)
		self.up.onChangeWar(bWar, iTeam, iOtherTeam)
		
		if iTeam < iNumPlayers and iOtherTeam < iNumPlayers:
			cong.onChangeWar(bWar, iTeam, iOtherTeam)
		
		# don't start AIWars if they get involved in natural wars
		if bWar and iTeam < iNumPlayers and iOtherTeam < iNumPlayers:
			data.players[iTeam].iAggressionLevel = 0
			data.players[iOtherTeam].iAggressionLevel = 0
			
	def onGoldenAge(self, argsList):
		iPlayer = argsList[0]
		
		sta.onGoldenAge(iPlayer)
		
	def onReleasedPlayer(self, argsList):
		iPlayer, iReleasedPlayer = argsList
		
		lCities = []
		for city in utils.getCityList(iPlayer):
			if city.plot().isCore(iReleasedPlayer) and not city.plot().isCore(iPlayer) and not city.isCapital():
				lCities.append(city)
				
		sta.doResurrection(iReleasedPlayer, lCities, False)
		
		gc.getPlayer(iReleasedPlayer).AI_changeAttitudeExtra(iPlayer, 2)
		
	def onBlockade(self, argsList):
		iPlayer, iGold = argsList
		
		vic.onBlockade(iPlayer, iGold)
		
	def onPeaceBrokered(self, argsList):
		iBroker, iPlayer1, iPlayer2 = argsList
		
		vic.onPeaceBrokered(iBroker, iPlayer1, iPlayer2)
		
	def onEndPlayerTurn(self, argsList):
		iGameTurn, iPlayer = argsList
		
		self.rnf.endTurn(iPlayer)
		sta.endTurn(iPlayer)

	def onKbdEvent(self, argsList):
		'keypress handler - return 1 if the event was consumed'
		eventType,key,mx,my,px,py = argsList
			
		theKey=int(key)
		
		if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_Q) and self.eventManager.bAlt and self.eventManager.bShift):
			print("SHIFT-ALT-Q") #enables squatting
			self.rnf.setCheatMode(True);
			CyInterface().addMessage(utils.getHumanID(), True, iDuration, "EXPLOITER!!! ;)", "", 0, "", ColorTypes(iRed), -1, -1, True, True)

		#Stability Cheat
		if data.bCheatMode and theKey == int(InputTypes.KB_S) and self.eventManager.bAlt and self.eventManager.bShift:
			print("SHIFT-ALT-S") #increases stability by one level
			utils.setStabilityLevel(utils.getHumanID(), min(5, utils.getStabilityLevel(utils.getHumanID()) + 1))
			
			
		if eventType == self.EventKeyDown and theKey == int(InputTypes.KB_V) and self.eventManager.bCtrl and self.eventManager.bShift:
			for iPlayer in range(iNumTotalPlayersB):
				pPlayer = gc.getPlayer(iPlayer)
				
				#pPlayer.initCity(71, 34)
				#city = gc.getMap().plot(71, 34).getPlotCity()
				
				lEras = [iAncient, iMedieval, iIndustrial]
				for iEra in lEras:
					pPlayer.setCurrentEra(iEra)
					for iUnit in range(iNumUnits):
						print (str(gc.getCivilizationInfo(pPlayer.getCivilizationType()).getShortDescription(0)))
						print (str(gc.getEraInfo(iEra).getDescription()))
						print (str(gc.getUnitInfo(iUnit).getDescription()))
						utils.makeUnit(iUnit, iPlayer, (68, 33), 1)
						gc.getMap().plot(68, 33).getUnit(0).kill(False, iBarbarian)
						#print ("Button")
						#city.pushOrder(OrderTypes.ORDER_TRAIN, iUnit , -1, False, True, False, True)
				#city.getPlotCity().kill()