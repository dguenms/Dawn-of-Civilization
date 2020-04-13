# Rhye's and Fall of Civilization - (a part of) Unique Powers

#Egypt in CvPlayer::canDoCivics() and in WBS
#India in CvPlayer::updateMaxAnarchyTurns()
#China (and England before the change) in CvPlayer::getProductionNeeded()
#Babylonia in CvPlayer.cpp::acquireCity()
# Babylonia now in CvPlayer::getCapitalYieldModifier(); +33% production and commerce in the capital after Code of Laws
#Greece CvCity:getGreatPeopleRate()
#Persia (USED TO BE in CvHandicapInfo::getDistanceMaintenancePercentByID(); THEN in RiseAndFall.py, collapseCapitals()), NOW in Stability.py, onCityAcquired()
#Rome in CvPlot::movementCost()
#Japan, Spain and England in CvUnit::init(). Turkey used to be there as well
# Japan now in CvUnit::experienceNeeded(); +50% promotion tempo
# England now in CvHandicapInfo::getDistanceMaintenancePercentByID()
#Ethiopia in Congresses.py (USED TO BE in CvUnit::init() and CvUnit::upgrade())
#Maya in CvHandicapInfo::getResearchPercentByID()
#Byzantium in Stability.checkImplosion()
#Khmer in CvUnit::canMoveInto()
#Germany (USED TO BE IN in CvUnit::init(), CvUnit::upgrade() and CvUnitAI::AI_pillageValue()); NOW IN CvUnit::upgradePrice()
#France in CvPlayerAI::AI_getAttitudeVal() and in Congresses.py
#Netherlands in CvUnit::canEnterTerritory()
#Mali in CvPlot::calculateYield() and Stability.py and CvInfos.cpp (CvHandicapInfo::getResearchPercentByID())
#Portugal in CvUnit::init()
#Inca in CvPlot::calculateNatureYield()
#Mongolia (USED TO BE IN in CvUnit::pillage()); now HERE and in CvRFCEventHandler.py (in OnCityRazed() and BeginPlayerTurn())
#Turkey HERE + in CvPlayer::canRazeCity()
#America HERE + in CvCity::getCulturePercentAnger()

from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
#import cPickle as pickle
from StoredData import data # edead
from Consts import *
from RFCUtils import *
from operator import itemgetter
import Areas

from Core import *

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

### Constants ###

tRussianTopLeft = (65, 49)
tRussianBottomRight = (121, 65)

iMongolianRadius = 4
iMongolianTimer = 1

class UniquePowers:

#######################################
### Main methods (Event-Triggered) ###
#####################################  


	def checkTurn(self, iGameTurn):
		if iGameTurn >= year(dBirth[iRussia]) and player(iRussia).isAlive():
			self.russianUP()

		if iGameTurn >= year(dBirth[iAmerica]) + turns(5):
			self.checkImmigration()

		if iGameTurn >= year(dBirth[iIndonesia]) and player(iIndonesia).isAlive():
			self.indonesianUP()
		
		data.bBabyloniaTechReceived = False
					
	def onChangeWar(self, bWar, iTeam, iOtherTeam):
		# reset Mongol UP flags when peace is made
		if not bWar and slot(iMongols) in [iTeam, iOtherTeam]:
			for city in cities.owner(iMongols):
				city.setMongolUP(False)
			
	def setup(self):
		# Babylonian UP: receive a free tech after discovering the first five techs
		player(iBabylonia).setFreeTechsOnDiscovery(5)
		
	def onBuildingBuilt(self, city, iOwner, iBuilding):
		if civ(iOwner) == iMughals:
			self.mughalUP(city, iBuilding)
					
#------------------VIKING UP----------------------

	def vikingUP(self, argsList):
	
		pWinningUnit, pLosingUnit = argsList
		cLosingUnit = PyHelpers.PyInfo.UnitInfo(pLosingUnit.getUnitType())
		
		iOwner = pWinningUnit.getOwner()
		iOwnerCiv = civ(iOwner)

		if (iOwnerCiv == iVikings and year() <= year(1500)) or pWinningUnit.getUnitType() == iCorsair:
			if cLosingUnit.getDomainType() == DomainTypes.DOMAIN_SEA:
				iGold = cLosingUnit.getProductionCost() / 2
				iGold = turns(iGold)
				player(iOwner).changeGold(iGold)
				message(iOwner, 'TXT_KEY_VIKING_NAVAL_UP', iGold, adjective(pLosingUnit), pLosingUnit.getName())
				
				if iOwnerCiv == iVikings:
					data.iVikingGold += iGold
				elif iOwnerCiv == iMoors:
					data.iMoorishGold += iGold

#------------------ARABIAN U.P.-------------------

	def arabianUP(self, city):
		iStateReligion = player(iArabia).getStateReligion()

		if iStateReligion >= 0:
			if not city.isHasReligion(iStateReligion):
				city.setHasReligion(iStateReligion, True, True, False)
			if not city.hasBuilding(iTemple + iStateReligion*4):
				city.setHasRealBuilding((iTemple + iStateReligion*4), True)

#------------------AZTEC U.P.-------------------

	def aztecUP(self, argsList): #Real Slavery by Sevo
		if not player(iAztecs).isAlive(): return
		
		pWinningUnit, pLosingUnit = argsList
		
		iWinningPlayer = pWinningUnit.getOwner()
		pWinningPlayer = player(iWinningPlayer)
		
		iLosingPlayer = pLosingUnit.getOwner()
		iLosingUnit = pLosingUnit.getUnitType()
		
		if civ(iWinningPlayer) != iAztecs:
			return

		# Only enslave land units!!
		if pLosingUnit.isAnimal() or not (pLosingUnit.getDomainType() == DomainTypes.DOMAIN_LAND and gc.getUnitInfo(iLosingUnit).getCombat() > 0):
			return
		
		if rand(100) < 35:
			newUnit = makeUnit(iWinningPlayer, iAztecSlave, pWinningUnit, UnitAITypes.UNITAI_ENGINEER)
			message(iWinningPlayer, 'TXT_KEY_UP_ENSLAVE_WIN', sound='SND_REVOLTEND', event=1, button=newUnit.getButton(), color=8, location=pWinningUnit, force=True)
			message(iLosingPlayer, 'TXT_KEY_UP_ENSLAVE_LOSE', sound='SND_REVOLTEND', event=1, button=newUnit.getButton(), color=7, location=pWinningUnit, force=True)
			if civ(pLosingUnit) not in dCivGroups[iCivGroupAmerica] and not is_minor(pLosingUnit): # old world civs now
				data.iAztecSlaves += 1



#------------------RUSSIAN U.P.-------------------

	def russianUP(self):
		for unit in plots.rectangle(tRussianTopLeft, tRussianBottomRight).owner(iRussia).units():
			if team(iRussia).isAtWar(unit.getOwner()):
				unit.changeDamage(8, slot(iRussia))




#------------------TURKISH U.P.-------------------


	def ottomanUP(self, city, iCiv, iPreviousOwner):
		for pPlot in plots.surrounding(city, radius=2):
			if location(pPlot) == location(city):
				convertPlotCulture(pPlot, iCiv, 51, False)
			elif pPlot.isCity():
				pass
			elif distance(pPlot, city) == 1:
				convertPlotCulture(pPlot, iCiv, 80, True)
			else:
				if pPlot.getOwner() == iPreviousOwner:
					convertPlotCulture(pPlot, iCiv, 20, False)


#------------------MONGOLIAN U.P.-------------------

	def mongolUP(self, city):
		if city.getPopulation() >= 7:
			makeUnits(iMongols, iKeshik, city, 2, UnitAITypes.UNITAI_ATTACK_CITY)
		elif city.getPopulation() >= 4:
			makeUnit(iMongols, iKeshik, city, UnitAITypes.UNITAI_ATTACK_CITY)

		if city.getPopulation() >= 4:
			message(slot(iMongols), 'TXT_KEY_UP_MONGOL_HORDE')


#------------------AMERICAN U.P.-------------------

	def checkImmigration(self):
	
		if data.iImmigrationTimer == 0:
			self.doImmigration()
			data.iImmigrationTimer = 3 + rand(5) # 3-7 turns
		else:
			data.iImmigrationTimer -= 1
			
	def doImmigration(self):
	
		# get available migration and immigration cities
		lSourceCities = []
		lTargetCities = []
		
		for iPlayer in players.major():
			if civ(iPlayer) in lBioNewWorld: continue # no immigration to natives
			pPlayer = player(iPlayer)
			lCities = []
			bNewWorld = pPlayer.getCapitalCity().getRegionID() in lNewWorld
			for city in cities.owner(iPlayer):
				iFoodDifference = city.foodDifference(False)
				iHappinessDifference = city.happyLevel() - city.unhappyLevel(0)
				if city.getRegionID() in lNewWorld and bNewWorld:
					if iFoodDifference <= 0 or iHappinessDifference <= 0: continue
					iNorthAmericaBonus = 0
					if city.getRegionID() in [rCanada, rUnitedStates]: iNorthAmericaBonus = 5
					lCities.append((city, iHappinessDifference + iFoodDifference / 2 + city.getPopulation() / 2 + iNorthAmericaBonus))
				elif city.getRegionID() not in lNewWorld and not bNewWorld:
					iValue = 0
					if iFoodDifference < 0:
						iValue -= iFoodDifference / 2
					if iHappinessDifference < 0:
						iValue -= iHappinessDifference
					if iValue > 0:
						lCities.append((city, iValue))
			
			if lCities:
				lCities.sort(key=itemgetter(1), reverse=True)
			
				if bNewWorld:
					lTargetCities.append(lCities[0])
				else:
					lSourceCities.append(lCities[0])
				
		# sort highest to lowest for happiness/unhappiness
		lSourceCities.sort(key=itemgetter(1), reverse=True)
		lTargetCities.sort(key=itemgetter(1), reverse=True)
		
		iNumMigrations = min(len(lSourceCities) / 4, len(lTargetCities))
		
		for iMigration in range(iNumMigrations):
			sourceCity = lSourceCities[iMigration][0]
			targetCity = lTargetCities[iMigration][0]
		
			sourceCity.changePopulation(-1)
			targetCity.changePopulation(1)
			
			if sourceCity.getPopulation() >= 9:
				sourceCity.changePopulation(-1)
				targetCity.changePopulation(1)
				
			# extra cottage growth for target city's vicinity
			for pCurrent in plots.surrounding(targetCity, radius=2):
				if pCurrent.getWorkingCity() == targetCity:
					pCurrent.changeUpgradeProgress(turns(10))
						
			# migration brings culture
			targetPlot = plot(city)
			iTargetPlayer = targetCity.getOwner()
			iSourcePlayer = sourceCity.getOwner()
			iCultureChange = targetPlot.getCulture(iTargetPlayer) / targetCity.getPopulation()
			targetPlot.changeCulture(iSourcePlayer, iCultureChange, False)
			
			# chance to spread state religion if in source city
			if player(iSourcePlayer).isStateReligion():
				iReligion = player(iSourcePlayer).getStateReligion()
				if sourceCity.isHasReligion(iReligion) and not targetCity.isHasReligion(iReligion):
					if rand(3) == 0:
						targetCity.setHasReligion(iReligion, True, True, True)
						
			# notify affected players
			message(iSourcePlayer, 'TXT_KEY_UP_EMIGRATION', sourceCity.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.unit(iSettler).getButton(), color=iYellow, location=sourceCity)
			message(iTargetPlayer, 'TXT_KEY_UP_IMMIGRATION', targetCity.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.unit(iSettler).getButton(), color=iYellow, location=targetCity)
	
			if civ(iTargetPlayer) == iCanada:
				self.canadianUP(targetCity)
		
	def canadianUP(self, city):
		iPopulation = 5 * city.getPopulation() / 2
		
		lSpecialists = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman]
		lProgress = [city.getGreatPeopleUnitProgress(unique_unit(city.getOwner(), iSpecialist)) for iSpecialist in lSpecialists]
		bAllZero = all(x <= 0 for x in lProgress)
			
		if bAllZero:
			iGreatPerson = random_entry(lSpecialists)
		else:
			iGreatPerson = find_max(lProgress).index + iGreatProphet
			
		iGreatPerson = unique_unit(city.getOwner(), iGreatPerson)
		
		city.changeGreatPeopleProgress(iPopulation)
		city.changeGreatPeopleUnitProgress(iGreatPerson, iPopulation)
		
		message(city.getOwner(), 'TXT_KEY_UP_MULTICULTURALISM', city.getName(), infos.unit(iGreatPerson).getText(), iPopulation, event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.unit(iGreatPerson).getButton(), color=iGreen, location=city)
					
	def tradingCompanyCulture(self, city, iCiv, iPreviousOwner):
		for pPlot in plots.surrounding(city):
			if location(pPlot) == location(city):
				convertPlotCulture(pPlot, iCiv, 51, False)
			elif pPlot.isCity():
				pass
			elif distance(pPlot, city) == 1:
				convertPlotCulture(pPlot, iCiv, 65, True)
			elif pPlot.getOwner() == iPreviousOwner:
				convertPlotCulture(pPlot, iCiv, 15, False)
			
	# Indonesian UP: additional gold for foreign ships in your core
	def indonesianUP(self):
		seaUnits = plots.of(Areas.getCoreArea(iIndonesia)).owner(iIndonesia).units().domain(DomainTypes.DOMAIN_SEA)
		iNumUnits = seaUnits.notowner(iIndonesia).where(lambda unit: not is_minor(unit)).where(lambda unit: not team(iIndonesia).isAtWar(unit.getTeam())).count()
					
		if iNumUnits > 0:
			iGold = 5 * iNumUnits
			player(iIndonesia).changeGold(iGold)
			message(slot(iIndonesia), 'TXT_KEY_INDONESIAN_UP', iGold)
	
	# Mughal UP: receives 50% of building cost as culture when building is completed
	def mughalUP(self, city, iBuilding):
		iCost = player(city).getBuildingProductionNeeded(iBuilding)
		city.changeCulture(city.getOwner(), iCost / 2, True)