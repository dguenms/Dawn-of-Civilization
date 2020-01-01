from CvPythonExtensions import *
import CvUtil
import PyHelpers 
import Popup as PyPopup 

from StoredData import data # edead
import RiseAndFall
import Barbs
from Religions import rel
import Resources
import CityNameManager as cnm
import UniquePowers     
import AIWars
import Congresses as cong
from Consts import *
from RFCUtils import *
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

from Core import *


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
			
		if iPlayer == iMongolia and bConquest and not player(iPlayer).isHuman():
			self.up.mongolUP(city)
		
		# relocate capitals
		if not player(iPlayer).isHuman():
			if iPlayer == iOttomans and tCity == (68, 45):
				moveCapital(iOttomans, tCity) # Kostantiniyye
			elif iPlayer == iMongolia and tCity == (102, 47):
				moveCapital(iMongolia, tCity) # Khanbaliq	
			elif iPlayer == iTurks and isAreaControlled(iTurks, Areas.tCoreArea[iPersia][0], Areas.tCoreArea[iPersia][1]):
				capital = pTurks.getCapitalCity()
				if not capital in plots.rectangle(*Areas.tCoreArea[iPersia]):
					newCapital = cities.rectangle(*Areas.tCoreArea[iPersia]).owner(iTurks).random()
					if newCapital:
						moveCapital(iTurks, (newCapital.getX(), newCapital.getY()))
				
				
		# remove slaves if unable to practice slavery
		if not player(iPlayer).canUseSlaves():
			city.setFreeSpecialistCount(iSpecialistSlave, 0)
		else:
			freeSlaves(city, iPlayer)
			
		if city.isCapital():
			if city.isHasRealBuilding(iAdministrativeCenter): 
				city.setHasRealBuilding(iAdministrativeCenter, False)	
				
		# Leoreth: relocate capital for AI if reacquired:
		if not player(iPlayer).isHuman() and iPlayer < iNumPlayers:
			if data.players[iPlayer].iResurrections == 0:
				if Areas.getCapital(iPlayer) == tCity:
					relocateCapital(iPlayer, city)
			else:
				if Areas.getRespawnCapital(iPlayer) == tCity:
					relocateCapital(iPlayer, city)
					
		# Leoreth: conquering Constantinople adds it to the Turkish core + Rumelia
		if iPlayer == iOttomans and tCity == (68, 45):
			setReborn(iOttomans, True)
			
		if iTurks in [iPlayer, iOwner]:
			if isAreaControlled(iTurks, Areas.tCoreArea[iPersia][0], Areas.tCoreArea[iPersia][1]):
				setReborn(iTurks, True)
			else:
				setReborn(iTurks, False)
					
		# Leoreth: help Byzantium/Constantinople
		if iPlayer == iByzantium and tCity == Areas.getCapital(iByzantium) and year() <= year(330)+3:
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
			
			city.setHasRealBuilding(iTemple + 4*player(iPlayer).getStateReligion(), True)
			
		if bConquest:

			# Colombian UP: no resistance in conquered cities in Latin America
			if iPlayer == iMaya and pMaya.isReborn():
				if city in plots.start(tSouthCentralAmericaTL).end(tSouthCentralAmericaBR):
					city.setOccupationTimer(0)
					
			# Byzantium reduced to four cities: core shrinks to Constantinople
			if iOwner == iByzantium and player(iByzantium).getNumCities <= 4:
				setReborn(iByzantium, True)
					
		if bTrade:
			for iNationalWonder in range(iNumBuildings):
				if iNationalWonder != iPalace and isNationalWonderClass(infos.building(iNationalWonder).getBuildingClassType()) and city.hasBuilding(iNationalWonder):
					city.setHasRealBuilding(iNationalWonder, False)
					
		# Leoreth: Escorial effect
		if player(iPlayer).isHasBuildingEffect(iEscorial):
			if city.isColony():
				capital = player(iPlayer).getCapitalCity()
				iGold = turns(10 + distance(capital, city))
				message(iPlayer, 'TXT_KEY_BUILDING_ESCORIAL_EFFECT', iGold, city.getName())	
				player(iPlayer).changeGold(iGold)
					
		self.pla.onCityAcquired(iOwner, iPlayer, city) # Plague
		self.com.onCityAcquired(city) # Communications
		self.corp.onCityAcquired(argsList) # Companies
		dc.onCityAcquired(iOwner, iPlayer) # DynamicCivs
		
		vic.onCityAcquired(iPlayer, iOwner, city, bConquest)
		
		lTradingCompanyList = [iSpain, iFrance, iEngland, iPortugal, iNetherlands]
		
		if bTrade and iPlayer in lTradingCompanyList and (city.getX(), city.getY()) in tTradingCompanyPlotLists[lTradingCompanyList.index(iPlayer)]:
			self.up.tradingCompanyCulture(city, iPlayer, iOwner)
		
		return 0
		
	def onCityAcquiredAndKept(self, argsList):
		iPlayer, city = argsList
		iOwner = city.getPreviousOwner()
		
		if city.isCapital():
			self.rnf.createStartingWorkers(iPlayer, (city.getX(), city.getY()))
		
		cityConquestCulture(city, iPlayer, iOwner)

	def onCityRazed(self, argsList):
		city, iPlayer = argsList

		dc.onCityRazed(city.getPreviousOwner())
		self.pla.onCityRazed(city, iPlayer) #Plague
			
		vic.onCityRazed(iPlayer, city)	
		sta.onCityRazed(iPlayer, city)

	def onCityBuilt(self, argsList):
		city = argsList[0]
		iOwner = city.getOwner()
		
		if iOwner < iNumActivePlayers: 
			cnm.onCityBuilt(city)
			
		# starting workers
		if city.isCapital():
			self.rnf.createStartingWorkers(iOwner, city)

		#Rhye - delete culture of barbs and minor civs to prevent weird unhappiness
		pPlot = plot(city)
		for iMinorCiv in players.minor():
			pPlot.setCulture(iMinorCiv, 0, True)

		if iOwner < iNumMajorPlayers:
			spreadMajorCulture(iOwner, location(city))
			if player(iOwner).getNumCities() < 2:
				player(iOwner).AI_updateFoundValues(False); # fix for settler maps not updating after 1st city is founded

		if iOwner == iOttomans:
			self.up.ottomanUP(city, iOwner, -1)
			
		if iOwner == iCarthage:
			if location(city) == (58, 39):
				if not pPhoenicia.isHuman():
					# TODO: use relocate capital here
					city.setHasRealBuilding(iPalace, True)
					pPhoenicia.getCapitalCity().setHasRealBuilding(iPalace, False)
					dc.onPalaceMoved(iCarthage)
					
					city.setPopulation(3)
					
					makeUnit(iCarthage, iWorkboat, (58, 39), UnitAITypes.UNITAI_WORKER_SEA)
					makeUnit(iCarthage, iGalley, (57, 40), UnitAITypes.UNITAI_SETTLER_SEA)
					makeUnit(iCarthage, iSettler, (57, 40), UnitAITypes.UNITAI_SETTLE)
					
					# additional defenders and walls to make human life not too easy
					if pRome.isHuman():
						city.setHasRealBuilding(iWalls, True)
						makeUnits(iCarthage, iArcher, (58, 39), 2, UnitAITypes.UNITAI_CITY_DEFENSE)
						makeUnits(iCarthage, iNumidianCavalry, (58, 39), 3)
						makeUnits(iCarthage, iWarElephant, (58, 39), 2, UnitAITypes.UNITAI_CITY_COUNTER)
					
				if getOwnedCoreCities(iCarthage) > 0:
					setReborn(iCarthage, True)
				
		if iOwner == iByzantium and location(city) == Areas.getCapital(iByzantium) and year() <= year(330)+3:
			if city.getPopulation() < 5:
				city.setPopulation(5)
				
			city.setHasRealBuilding(iBarracks, True)
			city.setHasRealBuilding(iWalls, True)
			city.setHasRealBuilding(iLibrary, True)
			city.setHasRealBuilding(iMarket, True)
			city.setHasRealBuilding(iGranary, True)
			city.setHasRealBuilding(iHarbor, True)
			city.setHasRealBuilding(iForge, True)
			
			city.setHasRealBuilding(iTemple + 4*player(iOwner).getStateReligion(), True)
			
		if iOwner == iPortugal and location(city) == Areas.getCapital(iPortugal) and year() <= year(tBirth[iPortugal]) + 3:
			city.setPopulation(5)
			
			for iBuilding in [iLibrary, iMarket, iHarbor, iLighthouse, iForge, iWalls, iTemple+4*pPortugal.getStateReligion()]:
				city.setHasRealBuilding(iBuilding, True)
			
		if iOwner == iNetherlands and location(city) == Areas.getCapital(iNetherlands) and year() <= year(1580)+3:
			city.setPopulation(9)
			
			for iBuilding in [iLibrary, iMarket, iWharf, iLighthouse, iBarracks, iPharmacy, iBank, iArena, iTheatre, iTemple+4*pNetherlands.getStateReligion()]:
				city.setHasRealBuilding(iBuilding, True)
				
			pNetherlands.AI_updateFoundValues(False)
			
		if iOwner == iItaly and location(city) == Areas.getCapital(iItaly) and year() <= year(tBirth[iItaly])+3:
			city.setPopulation(7)
			
			for iBuilding in [iLibrary, iPharmacy, iTemple+4*pItaly.getStateReligion(), iMarket, iArtStudio, iAqueduct, iCourthouse, iWalls]:
				city.setHasRealBuilding(iBuilding, True)
				
			pItaly.AI_updateFoundValues(False)

		vic.onCityBuilt(iOwner, city)
			
		if iOwner < iNumPlayers:
			dc.onCityBuilt(iOwner)

		if iOwner == iArabia:
			if not game.isReligionFounded(iIslam):
				if location(city) == (75, 33):
					rel.foundReligion(location(city), iIslam)
				
		# Leoreth: free defender and worker for AI colonies
		if iOwner in lCivGroups[0]:
			if city.getRegionID() not in mercRegions[iArea_Europe]:
				if not player(iOwner).isHuman():
					createGarrisons(city, iOwner, 1)
					makeUnit(iOwner, iWorker, city)
					
		# Holy Rome founds its capital
		if iOwner == iHolyRome:
			if pHolyRome.getNumCities() == 1:
				self.rnf.holyRomanSpawn()
				
		# Leoreth: Escorial effect
		if player(iOwner).isHasBuildingEffect(iEscorial):
			if city.isColony():
				capital = player(iOwner).getCapitalCity()
				iGold = turns(10 + distance(capital, city))
				message(iOwner, 'TXT_KEY_BUILDING_ESCORIAL_EFFECT', iGold, city.getName())	
				player(iOwner).changeGold(iGold)
				
		# Leoreth: free defender and worker for cities founded by American Pioneer in North America
		if iOwner == iAmerica:
			if city.getRegionID() in [rUnitedStates, rCanada, rAlaska]:
				createGarrisons(city, iOwner, 1)
				makeUnit(iOwner, getBestWorker(iOwner), city)

	def onPlayerChangeStateReligion(self, argsList):
		'Player changes his state religion'
		iPlayer, iNewReligion, iOldReligion = argsList
		
		if iPlayer < iNumPlayers:
			dc.onPlayerChangeStateReligion(iPlayer, iNewReligion)
			
		sta.onPlayerChangeStateReligion(iPlayer)
		vic.onPlayerChangeStateReligion(iPlayer, iNewReligion)

	def onCombatResult(self, argsList):
		self.rnf.immuneMode(argsList)
		self.up.vikingUP(argsList) # includes Moorish Corsairs
		
		pWinningUnit, pLosingUnit = argsList
		iWinningPlayer = pWinningUnit.getOwner()
		iLosingPlayer = pLosingUnit.getOwner()
		
		vic.onCombatResult(pWinningUnit, pLosingUnit)
		
		iUnitPower = 0
		pLosingUnitInfo = infos.unit(pLosingUnit)
		if pLosingUnitInfo.getUnitCombatType() != infos.type('UNITCOMBAT_SIEGE'):
			iUnitPower = pLosingUnitInfo.getPowerValue()
		
		sta.onCombatResult(iWinningPlayer, iLosingPlayer, iUnitPower)
		
		# capture slaves
		if iWinningPlayer == iAztecs and not pAztecs.isReborn():
			captureUnit(pLosingUnit, pWinningUnit, iAztecSlave, 35)
			
		elif iLosingPlayer == iNative:
			if iWinningPlayer not in lCivBioNewWorld or True in data.lFirstContactConquerors:
				if player(iWinningPlayer).isSlavery() or player(iWinningPlayer).isColonialSlavery():
					if pWinningUnit.getUnitType() == iBandeirante:
						captureUnit(pLosingUnit, pWinningUnit, iSlave, 100)
					else:
						captureUnit(pLosingUnit, pWinningUnit, iSlave, 35)
		
		# Maya Holkans give food to closest city on victory
		if pWinningUnit.getUnitType() == iHolkan:
			iOwner = pWinningUnit.getOwner()
			if player(iOwner).getNumCities() > 0:
				city = closestCity(pWinningUnit, iOwner)
				if city: 
					city.changeFood(turns(5))
					if human() == pWinningUnit.getOwner(): data.iTeotlSacrifices += 1
					message(iOwner, 'TXT_KEY_MAYA_HOLKAN_EFFECT', adjective(pLosingUnit), pLosingUnit.getName(), 5, city.getName())
		
		# Brandenburg Gate effect
		if player(iLosingPlayer).isHasBuildingEffect(iBrandenburgGate):
			for iPromotion in infos.promotions():
				if infos.promotion(iPromotion).isLeader() and pLosingUnit.isHasPromotion(iPromotion):
					player(iLosingPlayer).restoreGeneralThreshold()
					
		# Motherland Calls effect
		if player(iLosingPlayer).isHasBuildingEffect(iMotherlandCalls):
			if pLosingUnit.getLevel() >= 3:
				pCity = cities.owner(iLosingPlayer).where(lambda city: not city.isDrafted()).closest(pLosingUnit)
				if pCity:
					pCity.conscript(True)
					player(iLosingPlayer).changeConscriptCount(-1)
					message(iLosingPlayer, 'TXT_KEY_BUILDING_MOTHERLAND_CALLS_EFFECT', pLosingUnit.getName(), pCity.getName())

		
	def onReligionFounded(self, argsList):
		'Religion Founded'
		iReligion, iFounder = argsList
		
		if turn() == scenarioStartTurn():
			return
	
		vic.onReligionFounded(iFounder, iReligion)
		rel.onReligionFounded(iReligion, iFounder)
		dc.onReligionFounded(iFounder)

	def onVassalState(self, argsList):
		'Vassal State'
		iMaster, iVassal, bVassal, bCapitulated = argsList
		
		if bCapitulated:
			sta.onVassalState(iMaster, iVassal)
		
		if iVassal == iInca:
			setReborn(iInca, True)
			
		# move Mongolia's core south in case they vassalize China
		if bCapitulated and iVassal == iChina and iMaster == iMongolia:
			setReborn(iMongolia, True)
		
		dc.onVassalState(iMaster, iVassal)

	def onRevolution(self, argsList):
		'Called at the start of a revolution'
		iPlayer = argsList[0]
		
		sta.onRevolution(iPlayer)
		
		if iPlayer < iNumPlayers:
			dc.onRevolution(iPlayer)
			
		checkSlaves(iPlayer)
			
		if iPlayer in [iEgypt]:
			cnm.onRevolution(iPlayer)
			
	def onCityGrowth(self, argsList):
		'City Population Growth'
		pCity, iPlayer = argsList
		
		# Leoreth/Voyhkah: Empire State Building effect
		if pCity.isHasBuildingEffect(iEmpireStateBuilding):
			iPop = pCity.getPopulation()
			pCity.setBuildingCommerceChange(infos.building(iEmpireStateBuilding).getBuildingClassType(), 0, iPop)
			
		# Leoreth: Oriental Pearl Tower effect
		if pCity.isHasBuildingEffect(iOrientalPearlTower):
			iPop = pCity.getPopulation()
			pCity.setBuildingCommerceChange(infos.building(iOrientalPearlTower).getBuildingClassType(), 1, 2 * iPop)
			
	def onUnitPillage(self, argsList):
		unit, iImprovement, iRoute, iPlayer, iGold = argsList
		
		iUnit = unit.getUnitType()
		if iImprovement >= 0:
			vic.onUnitPillage(iPlayer, iGold, iUnit)
			
	def onCityCaptureGold(self, argsList):
		city, iPlayer, iGold = argsList
		
		if iGold > 0:
			if player(iPlayer).isHasBuildingEffect(iGurEAmir):
				wonderCity = cities.owner(iPlayer).building(iGurEAmir).one()
				if wonderCity:
					message(iPlayer, 'TXT_KEY_BUILDING_GUR_E_AMIR_EFFECT', iGold, city.getName(), wonderCity.getName())
					wonderCity.changeCulture(iPlayer, iGold, True)
		
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
		pUnit = argsList
			
	def onUnitBuilt(self, argsList):
		city, unit = argsList
		
		if unit.getUnitType() == iSettler and city.getOwner() == iChina and not pChina.isHuman():
			handleChineseCities(unit)
			
		# Leoreth: help AI by moving new slaves to the new world
		if unit.getUnitType() == iSlave and city.getRegionID() in [rIberia, rBritain, rEurope, rScandinavia, rRussia, rItaly, rBalkans, rMaghreb, rAnatolia] and human() != city.getOwner():
			moveSlaveToNewWorld(city.getOwner(), unit)
			
		# Space Elevator effect: +1 commerce per satellite built
		if unit.getUnitType() == iSatellite:
			city = getBuildingEffectCity(iSpaceElevator)
			if city:
				city.changeBuildingYieldChange(infos.building(iSpaceElevator).getBuildingClassType(), YieldTypes.YIELD_COMMERCE, 1)
	
		
	def onBuildingBuilt(self, argsList):
		city, iBuildingType = argsList
		iOwner = city.getOwner()
		tCity = (city.getX(), city.getY())
		
		vic.onBuildingBuilt(iOwner, iBuildingType)
		rel.onBuildingBuilt(city, iOwner, iBuildingType)
		self.up.onBuildingBuilt(city, iOwner, iBuildingType)
		
		if iOwner < iNumPlayers:
			self.com.onBuildingBuilt(iOwner, iBuildingType, city)
		
		if isWorldWonderClass(infos.building(iBuildingType).getBuildingClassType()):
			sta.onWonderBuilt(iOwner, iBuildingType)
			
		if iBuildingType == iPalace:
			sta.onPalaceMoved(iOwner)
			dc.onPalaceMoved(iOwner)
			
			if city.isHasRealBuilding(iAdministrativeCenter): city.setHasRealBuilding(iAdministrativeCenter, False)
			
			# Leoreth: in case human Phoenicia moves palace to Carthage
			if iOwner == iCarthage and tCity == (58, 39):
				setReborn(iCarthage, True)

		# Leoreth: update trade routes when Porcelain Tower is built to start its effect
		if iBuildingType == iPorcelainTower:
			player(iOwner).updateTradeRoutes()

		# Leoreth/Voyhkah: Empire State Building
		if iBuildingType == iEmpireStateBuilding:
			iPop = city.getPopulation()
			city.setBuildingCommerceChange(infos.building(iEmpireStateBuilding).getBuildingClassType(), 0, iPop)
			
		# Leoreth: Oriental Pearl Tower
		if iBuildingType == iOrientalPearlTower:
			iPop = city.getPopulation()
			city.setBuildingCommerceChange(infos.building(iOrientalPearlTower).getBuildingClassType(), 1, 2 * iPop)
			
		# Leoreth: Machu Picchu
		if iBuildingType == iMachuPicchu:
			iNumPeaks = 0
			for i in range(21):
				if city.getCityIndexPlot(i).isPeak():
					iNumPeaks += 1
			city.setBuildingCommerceChange(infos.building(iMachuPicchu).getBuildingClassType(), 0, iNumPeaks * 2)
			
		# Leoreth: Great Wall
		if iBuildingType == iGreatWall:
			for plot in plots.all().owner(iOwner).where(lambda p: p.isWater()):
				plot.setWithinGreatWall(True)
					
	def onPlotFeatureRemoved(self, argsList):
		plot, city, iFeature = argsList
		
		if plot.getOwner() == iBrazil:
			iGold = 0
			
			if iFeature == iForest: iGold = 15
			elif iFeature == iJungle: iGold = 20
			elif iFeature == iRainforest: iGold = 20
			
			if iGold > 0:
				pBrazil.changeGold(iGold)
				message(iBrazil, 'TXT_KEY_DEFORESTATION_EVENT', infos.feature(iFeature).getText(), city.getName(), iGold, type=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.commerce(0).getButton(), location=plot)

	def onProjectBuilt(self, argsList):
		city, iProjectType = argsList
		vic.onProjectBuilt(city.getOwner(), iProjectType)
		
		# Space Elevator effect: +5 commerce per space projectBuilt
		if infos.project(iProjectType).isSpaceship():
			city = getBuildingEffectCity(iSpaceElevator)
			if city:
				city.changeBuildingYieldChange(infos.building(iSpaceElevator).getBuildingClassType(), YieldTypes.YIELD_COMMERCE, 5)

	def onImprovementDestroyed(self, argsList):
		pass
		
	def onBeginGameTurn(self, argsList):
		iGameTurn = argsList[0]
		
		self.rnf.checkTurn(iGameTurn)
		self.barb.checkTurn(iGameTurn)
		rel.checkTurn(iGameTurn)
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
			
		if scenario() == i3000BC and iGameTurn == year(600):
			for iPlayer in range(iVikings):
				Modifiers.adjustInflationModifier(iPlayer)
			
		return 0

	def onBeginPlayerTurn(self, argsList):	
		iGameTurn, iPlayer = argsList
		
		if (data.lDeleteMode[0] != -1):
			self.rnf.deleteMode(iPlayer)
			
		self.pla.checkPlayerTurn(iGameTurn, iPlayer)
		
		if player(iPlayer).isAlive():
			vic.checkTurn(iGameTurn, iPlayer)
			
			if iPlayer < iNumPlayers and not player(iPlayer).isHuman():
				self.rnf.checkPlayerTurn(iGameTurn, iPlayer) #for leaders switch

	def onGreatPersonBorn(self, argsList):
		'Great Person Born'
		pUnit, iPlayer, pCity = argsList
		
		gp.onGreatPersonBorn(pUnit, iPlayer, pCity)
		vic.onGreatPersonBorn(iPlayer, pUnit)
		sta.onGreatPersonBorn(iPlayer)
		
		# Leoreth: Silver Tree Fountain effect
		if infos.unit(pUnit).getLeaderExperience() > 0 and player(iPlayer).isHasBuildingEffect(iSilverTreeFountain):
			city = cities.owner(iPlayer).where(lambda: city.getGreatPeopleProgress() > 0).maximum(lambda city: city.getGreatPeopleProgress())
			if city:
				iGreatPerson = find_max(range(iNumUnits), lambda iUnit: city.getGreatPeopleUnitProgress(iUnit)).result
				if iGreatPerson >= 0:
					player(iPlayer).createGreatPeople(iGreatPerson, False, False, city.getX(), city.getY())
					
		# Leoreth: Nobel Prize effect
		if game.getBuildingClassCreatedCount(infos.building(iNobelPrize).getBuildingClassType()) > 0:
			if infos.unit(pUnit).getLeaderExperience() == 0 and infos.unit(pUnit).getEspionagePoints() == 0:
				for iLoopPlayer in range(iNumPlayers):
					if player(iLoopPlayer).isHasBuildingEffect(iNobelPrize):
						if pUnit.getOwner() != iLoopPlayer and player(pUnit).AI_getAttitude(iLoopPlayer) >= AttitudeTypes.ATTITUDE_PLEASED:
							wonderCity = cities.owner(iLoopPlayer).building_effect(iNobelPrize).one()
							if wonderCity:
								iGreatPersonType = getDefaultGreatPerson(pUnit.getUnitType())
							
								iGreatPeoplePoints = max(4, player(iLoopPlayer).getGreatPeopleCreated())
							
								pLoopCity.changeGreatPeopleProgress(iGreatPeoplePoints)
								pLoopCity.changeGreatPeopleUnitProgress(iGreatPersonType, iGreatPeoplePoints)
								interface.setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, True)
								message(iLoopPlayer, 'TXT_KEY_BUILDING_NOBEL_PRIZE_EFFECT', adjective(pUnit), pUnit.getName(), pLoopCity.getName(), iGreatPeoplePoints)
						break

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
		
		iEra = infos.tech(iTech).getEra()
		iGameTurn = turn()

		if iGameTurn == scenarioStartTurn():
			return
		
		sta.onTechAcquired(iPlayer, iTech)
		AIParameters.onTechAcquired(iPlayer, iTech)

		if iGameTurn > year(tBirth[iPlayer]):
			vic.onTechAcquired(iPlayer, iTech)
			cnm.onTechAcquired(iPlayer)
			dc.onTechAcquired(iPlayer, iTech)

		if player(iPlayer).isAlive() and iGameTurn >= year(tBirth[iPlayer]) and iPlayer < iNumPlayers:
			rel.onTechAcquired(iTech, iPlayer)
			if iGameTurn > year(1700):
				self.aiw.forgetMemory(iTech, iPlayer)

		if iTech == iExploration:
			if iPlayer in [iSpain, iFrance, iEngland, iGermany, iVikings, iNetherlands, iPortugal]:
				data.players[iPlayer].iExplorationTurn = iGameTurn
				
		elif iTech == iCompass:
			if iPlayer == iVikings:
				plot(49, 62).setTerrainType(iCoast, True, True)

		elif iTech == iMicrobiology:
			self.pla.onTechAcquired(iTech, iPlayer)

		elif iTech == iRailroad:
			self.rnf.onRailroadDiscovered(iPlayer)
			
		if iTech in [iExploration, iFirearms]:
			teamPlayer = team(iPlayer)
			if teamPlayer.isHasTech(iExploration) and teamPlayer.isHasTech(iFirearms):
				self.rnf.earlyTradingCompany(iPlayer)
			
		if iTech in [iEconomics, iReplaceableParts]:
			teamPlayer = team(iPlayer)
			if teamPlayer.isHasTech(iEconomics) and teamPlayer.isHasTech(iReplaceableParts):
				self.rnf.lateTradingCompany(iPlayer)
	
		if not player(iPlayer).isHuman():
			if iPlayer == iJapan and iEra == iIndustrial:
				moveCapital(iPlayer, (116, 47)) # Toukyou
			elif iPlayer == iItaly and iEra == iIndustrial:
				moveCapital(iPlayer, (60, 44)) # Roma
			elif iPlayer == iVikings and iEra == iRenaissance:
				moveCapital(iPlayer, (63, 59)) # Stockholm
			elif iPlayer == iHolyRome and iEra == iRenaissance:
				moveCapital(iPlayer, (62, 49)) # Wien
				
		# Maya UP: +20 food when a tech is discovered before the medieval era
		if iPlayer == iMaya and not pMaya.isReborn() and iEra < iMedieval:
			if pMaya.getNumCities() > 0:
				iFood = 20 / pMaya.getNumCities()
				for city in cities.owner(iMaya):
					city.changeFood(iFood)
				message(iPlayer, 'TXT_KEY_MAYA_UP_EFFECT', infos.tech(iTech).getText(), iFood)
				
		# Spain's core extends when reaching the Renaissance and there are no Moors in Iberia
		# at the same time, the Moorish core relocates to Africa
		if iPlayer == iSpain and iEra == iRenaissance and not pSpain.isReborn():
			bNoMoors = True
			if pMoors.isAlive():
				for city in cities.owner(iMoors):
					if city.plot().getRegionID() == rIberia:
						bNoMoors = False
			if bNoMoors:
				setReborn(iSpain, True)
				setReborn(iMoors, True)
				
		# Italy's core extends when reaching the Industrial era
		if iPlayer == iItaly and iEra == iIndustrial:
			setReborn(iItaly, True)
			
		# Japan's core extends when reaching the Industrial era
		if iPlayer == iJapan and iEra == iIndustrial:
			setReborn(iJapan, True)
			
		# Germany's core shrinks when reaching the Digital era
		if iPlayer == iGermany and iEra == iDigital:
			setReborn(iGermany, True)
		

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
		for city in cities.owner(iPlayer):
			if city.plot().isCore(iReleasedPlayer) and not city.plot().isCore(iPlayer) and not city.isCapital():
				lCities.append(city)
				
		sta.doResurrection(iReleasedPlayer, lCities, False)
		
		player(iReleasedPlayer).AI_changeAttitudeExtra(iPlayer, 2)
		
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
			self.rnf.setCheatMode(True)
			message(human(), 'EXPLOITER!!! ;)', color=iRed, force=True)

		#Stability Cheat
		if data.bCheatMode and theKey == int(InputTypes.KB_S) and self.eventManager.bAlt and self.eventManager.bShift:
			print("SHIFT-ALT-S") #increases stability by one level
			data.setStabilityLevel(human(), min(5, stability(human()) + 1))
			
			
		if eventType == self.EventKeyDown and theKey == int(InputTypes.KB_V) and self.eventManager.bCtrl and self.eventManager.bShift:
			for iPlayer in range(iNumTotalPlayersB):
				pPlayer = player(iPlayer)
				
				lEras = [iAncient, iMedieval, iIndustrial]
				for iEra in lEras:
					pPlayer.setCurrentEra(iEra)
					for iUnit in range(iNumUnits):
						makeUnit(iPlayer, iUnit, (68, 33))
						plot(68, 33).getUnit(0).kill(False, iBarbarian)
						#print ("Button")
						#city.pushOrder(OrderTypes.ORDER_TRAIN, iUnit , -1, False, True, False, True)
				#city.getPlotCity().kill()