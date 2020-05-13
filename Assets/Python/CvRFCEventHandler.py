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
import Setup
import Civilizations
import AIParameters
import GreatPeople as gp
import Periods as periods

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
		
		# data.setup()

		# self.rnf.setup()
		# self.pla.setup()
		# dc.setup()
		# self.aiw.setup()
		# self.up.setup()
		
		# vic.setup()
		# cong.setup()
		
		# Leoreth: set DLL core values
		# Modifiers.init()
		# Setup.init()
		# SettlerMaps.init()
		# WarMaps.init()
		# RegionMap.init()
		# Civilizations.init()
		# AIParameters.init()
		
		return 0


	def onCityAcquired(self, argsList):
		iOwner, iPlayer, city, bConquest, bTrade = argsList
		iCiv = civ(iPlayer)
		tCity = (city.getX(), city.getY())
		
		# cnm.onCityAcquired(city, iPlayer)
		# periods.onCityAcquired(iPlayer, city, bConquest)
		
		#if bConquest:
		#	sta.onCityAcquired(city, iOwner, iPlayer)
			
		#if iCiv == iArabia:
		#	self.up.arabianUP(city)
			
		#if iCiv == iMongols and bConquest and not player(iPlayer).isHuman():
		#	self.up.mongolUP(city)
		
		# relocate capitals
		#if not player(iPlayer).isHuman():
		#	if iCiv == iOttomans and tCity == (68, 45):
		#		moveCapital(iPlayer, tCity) # Kostantiniyye
		#	elif iCiv == iMongols and tCity == (102, 47):
		#		moveCapital(iPlayer, tCity) # Khanbaliq	
		#	elif iCiv == iTurks and isAreaControlled(iPlayer, dCoreArea[iPersia][0], dCoreArea[iPersia][1]):
		#		capital = player(iPlayer).getCapitalCity()
		#		if not capital in plots.core(iPersia):
		#			newCapital = cities.core(iPersia).owner(iPlayer).random()
		#			if newCapital:
		#				moveCapital(iPlayer, (newCapital.getX(), newCapital.getY()))
				
				
		# remove slaves if unable to practice slavery
		#if not player(iPlayer).canUseSlaves():
		#	city.setFreeSpecialistCount(iSpecialistSlave, 0)
		#else:
		#	freeSlaves(city, iPlayer)
			
		# if city.isCapital():
		#	if city.isHasRealBuilding(iAdministrativeCenter): 
		#		city.setHasRealBuilding(iAdministrativeCenter, False)	
				
		# Leoreth: relocate capital for AI if reacquired:
		#if not player(iPlayer).isHuman() and not is_minor(iPlayer):
		#	if data.players[iPlayer].iResurrections == 0:
		#		if location(plots.capital(iCiv)) == tCity:
		#			relocateCapital(iPlayer, city)
		#	else:
		#		if location(plots.respawnCapital(iCiv)) == tCity:
		#			relocateCapital(iPlayer, city)
					
		# Leoreth: help Byzantium/Constantinople
		#if iCiv == iByzantium and tCity == location(plots.capital(iByzantium)) and year() <= year(330)+3:
		#	if city.getPopulation() < 5:
		#		city.setPopulation(5)
		#	
		#	city.setHasRealBuilding(iBarracks, True)
		#	city.setHasRealBuilding(iWalls, True)
		#	city.setHasRealBuilding(iLibrary, True)
		#	city.setHasRealBuilding(iMarket, True)
		#	city.setHasRealBuilding(iGranary, True)
		#	city.setHasRealBuilding(iHarbor, True)
		#	city.setHasRealBuilding(iForge, True)
		#	
		#	city.setName("Konstantinoupolis", False)
		#	
		#	city.setHasRealBuilding(iTemple + 4*player(iPlayer).getStateReligion(), True)
			
		#if bConquest:

			# Colombian UP: no resistance in conquered cities in Latin America
		#	if iCiv == iColombia:
		#		if city in plots.start(tSouthCentralAmericaTL).end(tSouthCentralAmericaBR):
		#			city.setOccupationTimer(0)
					
		#if bTrade:
		#	for iNationalWonder in range(iNumBuildings):
		#		if iNationalWonder != iPalace and isNationalWonderClass(infos.building(iNationalWonder).getBuildingClassType()) and city.hasBuilding(iNationalWonder):
		#			city.setHasRealBuilding(iNationalWonder, False)
					
		# Leoreth: Escorial effect
		#if player(iPlayer).isHasBuildingEffect(iEscorial):
		#	if city.isColony():
		#		capital = player(iPlayer).getCapitalCity()
		#		iGold = turns(10 + distance(capital, city))
		#		message(iPlayer, 'TXT_KEY_BUILDING_ESCORIAL_EFFECT', iGold, city.getName())	
		#		player(iPlayer).changeGold(iGold)
					
		#self.pla.onCityAcquired(iOwner, iPlayer, city) # Plague
		#self.com.onCityAcquired(city) # Communications
		#self.corp.onCityAcquired(argsList) # Companies
		#dc.onCityAcquired(iOwner, iPlayer) # DynamicCivs
		
		#vic.onCityAcquired(iPlayer, iOwner, city, bConquest)
		
		#lTradingCompanyList = [iSpain, iFrance, iEngland, iPortugal, iNetherlands]
		
		#if bTrade and iCiv in lTradingCompanyList and (city.getX(), city.getY()) in tTradingCompanyPlotLists[lTradingCompanyList.index(iCiv)]: # TODO: all of those should be dicts
		#	self.up.tradingCompanyCulture(city, iPlayer, iOwner)
		
		return 0
		
	def onCityAcquiredAndKept(self, argsList):
		#iPlayer, city = argsList
		#iOwner = city.getPreviousOwner()
		
		#if city.isCapital():
		#	self.rnf.createStartingWorkers(iPlayer, (city.getX(), city.getY()))
		
		#cityConquestCulture(city, iPlayer, iOwner)
		
		return 0

	def onCityRazed(self, argsList):
		city, iPlayer = argsList

		#dc.onCityRazed(city.getPreviousOwner())
		#self.pla.onCityRazed(city, iPlayer) #Plague
			
		#vic.onCityRazed(iPlayer, city)	
		#sta.onCityRazed(iPlayer, city)
		
		return 0

	def onCityBuilt(self, argsList):
		city = argsList[0]
		iOwner = city.getOwner()
		iOwnerCiv = civ(iOwner)
		
		#periods.onCityBuilt(city)
		
		#if not is_minor(city): 
		#	cnm.onCityBuilt(city)
			
		# starting workers
		#if city.isCapital():
		#	self.rnf.createStartingWorkers(iOwner, city)

		#Rhye - delete culture of barbs and minor civs to prevent weird unhappiness
		#pPlot = plot(city)
		#for iMinor in players.minor():
		#	pPlot.setCulture(iMinor, 0, True)

		#if not is_minor(iOwner):
		#	spreadMajorCulture(iOwner, location(city))
		#	if player(iOwner).getNumCities() < 2:
		#		player(iOwner).AI_updateFoundValues(False); # fix for settler maps not updating after 1st city is founded

		#if iOwnerCiv == iOttomans:
		#	self.up.ottomanUP(city, iOwner, -1)
			
		#if iOwnerCiv == iPhoenicia:
		#	if location(city) == (58, 39):
		#		if not player(iPhoenicia).isHuman():
		#			# TODO: use relocate capital here
		#			city.setHasRealBuilding(iPalace, True)
		#			player(iPhoenicia).getCapitalCity().setHasRealBuilding(iPalace, False)
		#			dc.onPalaceMoved(iOwner)
		#			
		#			city.setPopulation(3)
		#			
		#			makeUnit(iPhoenicia, iWorkboat, (58, 39), UnitAITypes.UNITAI_WORKER_SEA)
		#			makeUnit(iPhoenicia, iGalley, (57, 40), UnitAITypes.UNITAI_SETTLER_SEA)
		#			makeUnit(iPhoenicia, iSettler, (57, 40), UnitAITypes.UNITAI_SETTLE)
		#			
		#			# additional defenders and walls to make human life not too easy
		#			if player(iRome).isHuman():
		#				city.setHasRealBuilding(iWalls, True)
		#				makeUnits(iPhoenicia, iArcher, (58, 39), 2, UnitAITypes.UNITAI_CITY_DEFENSE)
		#				makeUnits(iPhoenicia, iNumidianCavalry, (58, 39), 3)
		#				makeUnits(iPhoenicia, iWarElephant, (58, 39), 2, UnitAITypes.UNITAI_CITY_COUNTER)
				
		#if iOwnerCiv == iByzantium and location(city) == location(plots.capital(iByzantium)) and year() <= year(330)+3:
		#	if city.getPopulation() < 5:
		#		city.setPopulation(5)
		#		
		#	city.setHasRealBuilding(iBarracks, True)
		#	city.setHasRealBuilding(iWalls, True)
		#	city.setHasRealBuilding(iLibrary, True)
		#	city.setHasRealBuilding(iMarket, True)
		#	city.setHasRealBuilding(iGranary, True)
		#	city.setHasRealBuilding(iHarbor, True)
		#	city.setHasRealBuilding(iForge, True)
			
		#	city.setHasRealBuilding(iTemple + 4*player(iOwner).getStateReligion(), True)
			
		#if iOwnerCiv == iPortugal and location(city) == location(plots.capital(iPortugal)) and year() <= year(dBirth[iPortugal]) + turns(3):
		#	city.setPopulation(5)
		#	
		#	for iBuilding in [iLibrary, iMarket, iHarbor, iLighthouse, iForge, iWalls, temple(player(iOwner).getStateReligion())]:
		#		city.setHasRealBuilding(iBuilding, True)
			
		#if iOwnerCiv == iNetherlands and location(city) == location(plots.capital(iNetherlands)) and year() <= year(1580)+3:
		#	city.setPopulation(9)
		#	
		#	for iBuilding in [iLibrary, iMarket, iWharf, iLighthouse, iBarracks, iPharmacy, iBank, iArena, iTheatre, temple(player(iOwner).getStateReligion())]:
		#		city.setHasRealBuilding(iBuilding, True)
		#		
		#	player(iOwner).AI_updateFoundValues(False)
			
		#if iOwnerCiv == iItaly and location(city) == location(plots.capital(iItaly)) and year() <= year(dBirth[iItaly]) + turns(3):
		#	city.setPopulation(7)
		#	
		#	for iBuilding in [iLibrary, iPharmacy, temple(player(iOwner).getStateReligion()), iMarket, iArtStudio, iAqueduct, iCourthouse, iWalls]:
		#		city.setHasRealBuilding(iBuilding, True)
		#		
		#	player(iOwner).AI_updateFoundValues(False)

		#vic.onCityBuilt(iOwner, city)
			
		#if not is_minor(iOwner):
		#	dc.onCityBuilt(iOwner)

		#if iOwnerCiv == iArabia:
		#	if not game.isReligionFounded(iIslam):
		#		if location(city) == (75, 33):
		#			rel.foundReligion(location(city), iIslam)
				
		# Leoreth: free defender and worker for AI colonies
		#if iOwnerCiv in dCivGroups[iCivGroupEurope]:
		#	if city.getRegionID() not in lEurope:
		#		if not player(iOwner).isHuman():
		#			createGarrisons(city, iOwner, 1)
		#			makeUnit(iOwner, iWorker, city)
					
		# Holy Rome founds its capital
		#if iOwnerCiv == iHolyRome:
		#	if player(iOwner).getNumCities() == 1:
		#		self.rnf.holyRomanSpawn()
				
		# Leoreth: Escorial effect
		#if player(iOwner).isHasBuildingEffect(iEscorial):
		#	if city.isColony():
		#		capital = player(iOwner).getCapitalCity()
		#		iGold = turns(10 + distance(capital, city))
		#		message(iOwner, 'TXT_KEY_BUILDING_ESCORIAL_EFFECT', iGold, city.getName())	
		#		player(iOwner).changeGold(iGold)
				
		# Leoreth: free defender and worker for cities founded by American Pioneer in North America
		#if iOwnerCiv == iAmerica:
		#	if city.getRegionID() in [rUnitedStates, rCanada, rAlaska]:
		#		createGarrisons(city, iOwner, 1)
		#		makeUnit(iOwner, getBestWorker(iOwner), city)
		
		return

	def onPlayerChangeStateReligion(self, argsList):
		'Player changes his state religion'
		#iPlayer, iNewReligion, iOldReligion = argsList
		
		#if not is_minor(iPlayer):
		#	dc.onPlayerChangeStateReligion(iPlayer, iNewReligion)
			
		#sta.onPlayerChangeStateReligion(iPlayer)
		#vic.onPlayerChangeStateReligion(iPlayer, iNewReligion)
		
		return

	# combatResult
	def onCombatResult(self, argsList):
		#self.rnf.immuneMode(argsList)
		#self.up.vikingUP(argsList) # includes Moorish Corsairs
		
		#pWinningUnit, pLosingUnit = argsList
		#iWinningPlayer = pWinningUnit.getOwner()
		#iLosingPlayer = pLosingUnit.getOwner()
		
		#vic.onCombatResult(pWinningUnit, pLosingUnit)
		
		#iUnitPower = 0
		#pLosingUnitInfo = infos.unit(pLosingUnit)
		#if pLosingUnitInfo.getUnitCombatType() != infos.type('UNITCOMBAT_SIEGE'):
		#	iUnitPower = pLosingUnitInfo.getPowerValue()
		
		#sta.onCombatResult(iWinningPlayer, iLosingPlayer, iUnitPower)
		
		# capture slaves
		
		# Maya Holkans give food to closest city on victory
		
		# Brandenburg Gate effect
					
		# Motherland Calls effect
		
		return

	# religionFounded
	def onReligionFounded(self, argsList):
		'Religion Founded'
		#iReligion, iFounder = argsList
		
		#if turn() == scenarioStartTurn():
		#	return
	
		#vic.onReligionFounded(iFounder, iReligion)
		#rel.onReligionFounded(iReligion, iFounder)
		#dc.onReligionFounded(iFounder)
		
		return

	# vassalState
	def onVassalState(self, argsList):
		'Vassal State'
		#iMaster, iVassal, bVassal, bCapitulated = argsList
		
		#if bCapitulated:
		#	sta.onVassalState(iMaster, iVassal)
		
		#dc.onVassalState(iMaster, iVassal)
		#periods.onVassalState(iMaster, iVassal, bCapitulated)
		
		return

	# revolution
	def onRevolution(self, argsList):
		'Called at the start of a revolution'
		#iPlayer = argsList[0]
		#iCiv = civ(iPlayer)
		
		#sta.onRevolution(iPlayer)
		
		#if not is_minor(iPlayer):
		#	dc.onRevolution(iPlayer)
			
		#checkSlaves(iPlayer)
			
		#if iCiv == iEgypt:
		#	cnm.onRevolution(iPlayer)
		
		return
			
	def onCityGrowth(self, argsList):
		'City Population Growth'
		pCity, iPlayer = argsList
		
		return
			
	def onUnitPillage(self, argsList):
		unit, iImprovement, iRoute, iPlayer, iGold = argsList
		
		#iUnit = unit.getUnitType()
		#if iImprovement >= 0:
		#	vic.onUnitPillage(iPlayer, iGold, iUnit)
		
		return
	
	# cityCaptureGold
	def onCityCaptureGold(self, argsList):
		city, iPlayer, iGold = argsList
		
		#if civ(iPlayer) == iVikings and iGold > 0:
		#	vic.onCityCaptureGold(iPlayer, iGold)
		
		return
	
	# playerGoldTrade
	def onPlayerGoldTrade(self, argsList):
		iFromPlayer, iToPlayer, iGold = argsList
		
		#if civ(iToPlayer) == iTamils:
		#	vic.onPlayerGoldTrade(iToPlayer, iGold)
	
	# tradeMission
	def onTradeMission(self, argsList):
		#iUnitType, iPlayer, iX, iY, iGold = argsList
		
		#if civ(iPlayer) in [iTamils, iMali]:
		#	vic.onTradeMission(iPlayer, iX, iY, iGold)
		
		return
	
	# playerSlaveTrade
	def onPlayerSlaveTrade(self, argsList):
		iPlayer, iGold = argsList
		
		#if civ(iPlayer) == iCongo:
		#	vic.onPlayerSlaveTrade(iPlayer, iGold)
		
		return
			
	def onUnitGifted(self, argsList):
		pUnit, iOwner, pPlot = argsList
			
	def onUnitCreated(self, argsList):
		pUnit = argsList
	
	# unitBuilt
	def onUnitBuilt(self, argsList):
		city, unit = argsList
		
		#if unit.getUnitType() == iSettler and civ(city) == iChina and not player(iChina).isHuman():
		#	handleChineseCities(unit)
		
		return
	
	
	# buildingBuilt
	def onBuildingBuilt(self, argsList):
		city, iBuildingType = argsList
		iOwner = city.getOwner()
		tCity = (city.getX(), city.getY())
		
		#vic.onBuildingBuilt(iOwner, iBuildingType)
		#rel.onBuildingBuilt(city, iOwner, iBuildingType)
		#self.up.onBuildingBuilt(city, iOwner, iBuildingType)
		
		#if not is_minor(iOwner):
		#	self.com.onBuildingBuilt(iOwner, iBuildingType, city)
		
		#if isWorldWonderClass(infos.building(iBuildingType).getBuildingClassType()):
		#	sta.onWonderBuilt(iOwner, iBuildingType)
			
		#if iBuildingType == iPalace:
			#sta.onPalaceMoved(iOwner)
			#dc.onPalaceMoved(iOwner)
			#periods.onPalaceMoved(city)
			
			#if city.isHasRealBuilding(iAdministrativeCenter): city.setHasRealBuilding(iAdministrativeCenter, False)
			
		return
					
	def onPlotFeatureRemoved(self, argsList):
		plot, city, iFeature = argsList
		
		return
		
	def onProjectBuilt(self, argsList):
		city, iProjectType = argsList
		#vic.onProjectBuilt(city.getOwner(), iProjectType)
		
		return

	def onImprovementDestroyed(self, argsList):
		pass
	
	# BeginGameTurn
	def onBeginGameTurn(self, argsList):
		iGameTurn = argsList[0]
		
		#self.rnf.checkTurn(iGameTurn)
		#self.barb.checkTurn(iGameTurn)
		#rel.checkTurn(iGameTurn)
		#self.res.checkTurn(iGameTurn)
		#self.up.checkTurn(iGameTurn)
		#self.aiw.checkTurn(iGameTurn)
		#self.pla.checkTurn(iGameTurn)
		#self.com.checkTurn(iGameTurn)
		#self.corp.checkTurn(iGameTurn)
		
		#sta.checkTurn(iGameTurn)
		#cong.checkTurn(iGameTurn)
		
		#if iGameTurn % 10 == 0:
		#	dc.checkTurn(iGameTurn)
			
		return 0

	# BeginPlayerTurn
	def onBeginPlayerTurn(self, argsList):	
		iGameTurn, iPlayer = argsList
		
		#if (data.lDeleteMode[0] != -1):
		#	self.rnf.deleteMode(iPlayer)
			
		#self.pla.checkPlayerTurn(iGameTurn, iPlayer)
		
		#if player(iPlayer).isAlive():
		#	vic.checkTurn(iGameTurn, iPlayer)

	# greatPersonBorn
	def onGreatPersonBorn(self, argsList):
		'Great Person Born'
		pUnit, iPlayer, pCity = argsList
		
		#gp.onGreatPersonBorn(pUnit, iPlayer, pCity)
		#vic.onGreatPersonBorn(iPlayer, pUnit)
		#sta.onGreatPersonBorn(iPlayer)
					
	# religionSpread
	def onReligionSpread(self, argsList):
		iReligion, iOwner, pSpreadCity = argsList
		
		cnm.onReligionSpread(iReligion, iOwner, pSpreadCity)

	def onFirstContact(self, argsList):
		iTeamX,iHasMetTeamY = argsList
		if not is_minor(iTeamX):
			self.rnf.onFirstContact(iTeamX, iHasMetTeamY)
		self.pla.onFirstContact(iTeamX, iHasMetTeamY)
		
		vic.onFirstContact(iTeamX, iHasMetTeamY)

	#Rhye - start
	def onTechAcquired(self, argsList):
		iTech, iTeam, iPlayer, bAnnounce = argsList
		
		iCiv = civ(iPlayer)
		iEra = infos.tech(iTech).getEra()
		iGameTurn = turn()

		if iGameTurn == scenarioStartTurn():
			return
		
		sta.onTechAcquired(iPlayer, iTech)
		AIParameters.onTechAcquired(iPlayer, iTech)
		periods.onTechAcquired(iPlayer, iEra)

		if not is_minor(iPlayer) and iGameTurn > year(dSpawn[iCiv]):
			vic.onTechAcquired(iPlayer, iTech)
			cnm.onTechAcquired(iPlayer)
			dc.onTechAcquired(iPlayer, iTech)

		if not is_minor(iPlayer) and player(iPlayer).isAlive() and iGameTurn >= year(dSpawn[iCiv]):
			rel.onTechAcquired(iTech, iPlayer)
			if iGameTurn > year(1700):
				self.aiw.forgetMemory(iTech, iPlayer)

		if iTech == iExploration:
			if iCiv in [iSpain, iFrance, iEngland, iGermany, iVikings, iNetherlands, iPortugal]:
				data.players[iPlayer].iExplorationTurn = iGameTurn
				
		elif iTech == iCompass:
			if iCiv == iVikings:
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
			if iCiv == iJapan and iEra == iIndustrial:
				moveCapital(iPlayer, (116, 47)) # Toukyou
			elif iCiv == iItaly and iEra == iIndustrial:
				moveCapital(iPlayer, (60, 44)) # Roma
			elif iCiv == iVikings and iEra == iRenaissance:
				moveCapital(iPlayer, (63, 59)) # Stockholm
			elif iCiv == iHolyRome and iEra == iRenaissance:
				moveCapital(iPlayer, (62, 49)) # Wien
				
		# Maya UP: +20 food when a tech is discovered before the medieval era
		if iCiv == iMaya and iEra < iMedieval:
			iNumCities = player(iPlayer).getNumCities()
			if iNumCities > 0:
				iFood = 20 / iNumCities
				for city in cities.owner(iPlayer):
					city.changeFood(iFood)
				message(iPlayer, 'TXT_KEY_MAYA_UP_EFFECT', infos.tech(iTech).getText(), iFood)
		

	def onPreSave(self, argsList):
		'called before a game is actually saved'
		pass

	def onLoadGame(self, argsList):
		pass
		
	def onChangeWar(self, argsList):
		bWar, iTeam, iOtherTeam = argsList
		
		sta.onChangeWar(bWar, iTeam, iOtherTeam)
		self.up.onChangeWar(bWar, iTeam, iOtherTeam)
		
		if not is_minor(iTeam) and not is_minor(iOtherTeam):
			cong.onChangeWar(bWar, iTeam, iOtherTeam)
		
		# don't start AIWars if they get involved in natural wars
		if bWar and not is_minor(iTeam) and not is_minor(iOtherTeam):
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
			message(active(), 'EXPLOITER!!! ;)', color=iRed, force=True)

		#Stability Cheat
		if data.bCheatMode and theKey == int(InputTypes.KB_S) and self.eventManager.bAlt and self.eventManager.bShift:
			print("SHIFT-ALT-S") #increases stability by one level
			data.setStabilityLevel(active(), min(5, stability(active()) + 1))
			
			
		if eventType == self.EventKeyDown and theKey == int(InputTypes.KB_V) and self.eventManager.bCtrl and self.eventManager.bShift:
			for iPlayer in players.all().barbarian():
				pPlayer = player(iPlayer)
				
				lEras = [iAncient, iMedieval, iIndustrial]
				for iEra in lEras:
					pPlayer.setCurrentEra(iEra)
					for iUnit in range(iNumUnits):
						makeUnit(iPlayer, iUnit, (68, 33))
						plot(68, 33).getUnit(0).kill(False, -1)