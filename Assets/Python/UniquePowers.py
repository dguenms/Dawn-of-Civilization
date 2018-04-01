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
from RFCUtils import utils
from operator import itemgetter
import Areas

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
		if iGameTurn >= getTurnForYear(tBirth[iRussia]) and pRussia.isAlive():
			self.russianUP()

		if iGameTurn >= getTurnForYear(tBirth[iAmerica])+utils.getTurns(5):
			self.checkImmigration()

		if iGameTurn >= getTurnForYear(tBirth[iIndonesia]) and pIndonesia.isAlive():
			self.indonesianUP()
		
		data.bBabyloniaTechReceived = False
					
	def onChangeWar(self, bWar, iTeam, iOtherTeam):
		# reset Mongol UP flags when peace is made
		if not bWar:
			if iTeam == iMongolia:
				for city in utils.getCityList(iOtherTeam):
					city.setMongolUP(False)
			elif iOtherTeam == iMongolia:
				for city in utils.getCityList(iTeam):
					city.setMongolUP(False)
			
	def setup(self):
		# Babylonian UP: receive a free tech after discovering the first four techs
		pBabylonia.setFreeTechsOnDiscovery(4)
		
		# Chinese UP: +10% commerce rate per stability level
		pChina.changeYieldRateModifier(YieldTypes.YIELD_COMMERCE, 20)
		
	def onBuildingBuilt(self, city, iOwner, iBuilding):
		if iOwner == iMughals:
			self.mughalUP(city, iBuilding)
					
#------------------VIKING UP----------------------

	def vikingUP(self, argsList):
	
		pWinningUnit, pLosingUnit = argsList
		cLosingUnit = PyHelpers.PyInfo.UnitInfo(pLosingUnit.getUnitType())
		
		iOwner = pWinningUnit.getOwner()

		if (iOwner == iVikings and gc.getGame().getGameTurn() <= getTurnForYear(1500)) or pWinningUnit.getUnitType() == iCorsair:
			if cLosingUnit.getDomainType() == DomainTypes.DOMAIN_SEA:
				iGold = cLosingUnit.getProductionCost() / 2
				iGold = utils.getTurns(iGold)
				gc.getPlayer(iOwner).changeGold(iGold)
				sAdjective = gc.getPlayer(pLosingUnit.getOwner()).getCivilizationAdjectiveKey()
				CyInterface().addMessage(iOwner, False, iDuration, CyTranslator().getText("TXT_KEY_VIKING_NAVAL_UP", (iGold, sAdjective, pLosingUnit.getNameKey())), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
				
				if iOwner == iVikings:
					data.iVikingGold += iGold
				elif iOwner == iMoors:
					data.iMoorishGold += iGold
				
			

#------------------ROMAN UP-----------------------

	def doRomanWar(self, iCiv): # Unused
	
		if iCiv in [iCarthage, iPersia, iCeltia, iEgypt]:
			iNumTargets = 2
			self.romanConquestUP(iCiv, iNumTargets)
		elif iCiv == iGreece and utils.getHumanID() != iGreece:
			bEgypt = False
			for city in utils.getCityList(iGreece):
				if city.getRegionID() == rEgypt:
					bEgypt = True
					break
					
			if bEgypt:
				iNumTargets = 2
				self.romanConquestUP(iCiv, iNumTargets, [rEgypt])
			else:
				iNumTargets = 3
			
			self.romanConquestUP(iCiv, iNumTargets)

	def romanConquestUP(self, iEnemy, iNumTargets=1, lPreferredTargetRegions=[]): # Unused
		lEnemyCities = []
		lPreferredCities = []
		
		print "Getting closest city."
		for city in utils.getCityList(iEnemy):
			iDist = utils.calculateDistance(pCity.getX(), pCity.getY(), pRome.getCapitalCity().getX(), pRome.getCapitalCity().getY())
			lEnemyCities.append((iDist, pCity))
			if pCity.getRegionID() in lPreferredTargetRegions:
				lPreferredCities.append((iDist, pCity))
				
		if lPreferredCities:
			lEnemyCities = lPreferredCities
			
		lEnemyCities.sort()
		
		for i in range(iNumTargets):
			if lEnemyCities:
				pTargetCity = lEnemyCities.pop(0)[1]
				tPlot = utils.findNearestLandPlot((pTargetCity.getX(), pTargetCity.getY()), iRome)
				
				iExtra = 0
				if utils.getHumanID() != iRome and utils.getHumanID() != iEnemy: iExtra = 1
				
				utils.makeUnitAI(iLegion, iRome, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2+iExtra)
				utils.makeUnitAI(iCatapult, iRome, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1+iExtra*2)
				
		#utils.debugTextPopup("Roman conquerors against "+CyTranslator().getText(str(gc.getPlayer(iEnemy).getCivilizationShortDescriptionKey()), ()))

		CyInterface().addMessage(iRome, False, iDuration, CyTranslator().getText("TXT_KEY_UP_ROMAN_CONQUESTS",(gc.getPlayer(iEnemy).getCivilizationShortDescriptionKey(),)), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
		CyInterface().addMessage(iEnemy, False, iDuration, CyTranslator().getText("TXT_KEY_UP_ROMAN_CONQUESTS_TARGET", ()), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
		print ("Message displayed.")
		
	def greekConquestUP(self, iEnemy, iNumTargets=1): # Unused
		lEnemyCities = []
		
		print "Getting closest city."
		for city in utils.getCityList(iEnemy):
			iDist = utils.calculateDistance(pCity.getX(), pCity.getY(), pGreece.getCapitalCity().getX(), pGreece.getCapitalCity().getY())
			lEnemyCities.append((iDist, pCity))
			
		lEnemyCities.sort()
		
		for i in range(iNumTargets):
			if len(lEnemyCities) > 0:
				pTargetCity = lEnemyCities.pop(0)[1]
				tPlot = utils.findNearestLandPlot((pTargetCity.getX(), pTargetCity.getY()), iGreece)
				
				iExtra = 0
				if utils.getHumanID() not in [iGreece, iEnemy]: 
					iExtra = 1
					if iEnemy == iPersia: iExtra = 2
				
				utils.makeUnitAI(iHoplite, iGreece, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2+iExtra*2)
				utils.makeUnitAI(iCatapult, iGreece, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1+iExtra*2)
				
		CyInterface().addMessage(iEnemy, False, iDuration, CyTranslator().getText("TXT_KEY_UP_GREEK_CONQUESTS_TARGET", ()), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
		
	def tamilConquestUP(self, iEnemy, iNumTargets=1): # Unused
		lEnemyCities = []
		
		print "Getting closest city."
		for pCity in utils.getCityList(iEnemy):
			iDist = utils.calculateDistance(pCity.getX(), pCity.getY(), pTamils.getCapitalCity().getX(), pTamils.getCapitalCity().getY())
			lEnemyCities.append((iDist, pCity))
			
		lEnemyCities.sort()
		
		for i in range(iNumTargets):
			if lEnemyCities:
				pTargetCity = lEnemyCities.pop(0)[1]
				tPlot = utils.findNearestLandPlot((pTargetCity.getX(), pTargetCity.getY()), iTamils)
				
				utils.makeUnitAI(iSwordsman, iTamils, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
				utils.makeUnitAI(iWarElephant, iTamils, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
				utils.makeUnitAI(iCatapult, iTamils, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
				
		CyInterface().addMessage(iEnemy, False, iDuration, CyTranslator().getText("TXT_KEY_UP_TAMIL_CONQUESTS_TARGET", ()), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)


#------------------ARABIAN U.P.-------------------

	def seljukUP(self, city): # Unused
		return
		# pSeljuks = gc.getPlayer(iSeljuks)
		iStateReligion = pSeljuks.getStateReligion()

		if iStateReligion >= 0:
			for iReligion in range(iNumReligions):	# Leoreth: now removes foreign religions and buildings (except holy cities) as well
				if city.isHasReligion(iReligion) and not city.isHolyCityByType(iReligion):
					city.setHasReligion(iReligion, False, False, False)
				if city.hasBuilding(iTemple + iReligion*4):
					city.setHasRealBuilding((iTemple + iReligion*4), False)
				if city.hasBuilding(iCathedral + iReligion*4):
					city.setHasRealBuilding((iCathedral + iReligion*4), False)
				if city.hasBuilding(iMonastery + iReligion*4):
					city.setHasRealBuilding((iMonastery + iReligion*4), False)
			city.setHasReligion(iStateReligion, True, True, False)
		

	def arabianUP(self, city):
		#pArabia = gc.getPlayer(iArabia)
		iStateReligion = pArabia.getStateReligion()

		if iStateReligion >= 0:
			if not city.isHasReligion(iStateReligion):
				city.setHasReligion(iStateReligion, True, True, False)
			if not city.hasBuilding(iTemple + iStateReligion*4):
				city.setHasRealBuilding((iTemple + iStateReligion*4), True)

#------------------AZTEC U.P.-------------------

	def aztecUP(self, argsList): #Real Slavery by Sevo
		if not pAztecs.isAlive(): return
		if utils.isReborn(iAztecs): return
		
		pWinningUnit, pLosingUnit = argsList
		
		iWinningPlayer = pWinningUnit.getOwner()
		pWinningPlayer = gc.getPlayer(iWinningPlayer)
		
		iLosingPlayer = pLosingUnit.getOwner()
		iLosingUnit = pLosingUnit.getUnitType()
		
		if iWinningPlayer != iAztecs:
			return
			

		# Only enslave land units!!
		if pLosingUnit.isAnimal() or not (pLosingUnit.getDomainType() == DomainTypes.DOMAIN_LAND and gc.getUnitInfo(iLosingUnit).getCombat() > 0):
			return
		
		iRandom = gc.getGame().getSorenRandNum(100, 'capture chance')
		if iRandom < 35:
			pNewUnit = pWinningPlayer.initUnit(iAztecSlave, pWinningUnit.getX(), pWinningUnit.getY(), UnitAITypes.UNITAI_ENGINEER, DirectionTypes.DIRECTION_SOUTH)
			CyInterface().addMessage(iWinningPlayer, True, 15, CyTranslator().getText("TXT_KEY_UP_ENSLAVE_WIN", ()), 'SND_REVOLTEND', 1, 'Art/Units/slave/button_slave.dds', ColorTypes(8), pWinningUnit.getX(), pWinningUnit.getY(), True, True)
			CyInterface().addMessage(iLosingPlayer, True, 15, CyTranslator().getText("TXT_KEY_UP_ENSLAVE_LOSE", ()), 'SND_REVOLTEND', 1, 'Art/Units/slave/button_slave.dds', ColorTypes(7), pWinningUnit.getX(), pWinningUnit.getY(), True, True)
			if pLosingUnit.getOwner() not in lCivGroups[5] and pLosingUnit.getOwner() < iNumPlayers: # old world civs now
				data.iAztecSlaves += 1



#------------------RUSSIAN U.P.-------------------

	def russianUP(self):
		#pRussia = gc.getPlayer(iRussia)
		#teamRussia = gc.getTeam(pRussia.getTeam())
		for (x, y) in utils.getPlotList(tRussianTopLeft, tRussianBottomRight):
			pPlot = gc.getMap().plot(x, y)
			if pPlot.getOwner() == iRussia:
				iNumUnitsInAPlot = pPlot.getNumUnits()
				if iNumUnitsInAPlot > 0:
					for i in range(iNumUnitsInAPlot):
						unit = pPlot.getUnit(i)
						if teamRussia.isAtWar(unit.getOwner()):
##								print("hp", unit.currHitPoints() )
##								print("damage", unit.getDamage() )
							unit.changeDamage(8, iRussia)
##								print("hp now", unit.currHitPoints() 
##								print("damage", unit.getDamage() )




#------------------TURKISH U.P.-------------------


	def turkishUP(self, city, iCiv, iPreviousOwner):
		tPlot = (city.getX(), city.getY())
		x, y = tPlot
		for (i, j) in utils.surroundingPlots(tPlot, 2):
			pPlot = gc.getMap().plot(i, j)
			if (i, j) == tPlot:
				utils.convertPlotCulture(pPlot, iCiv, 51, False)
			elif pPlot.isCity():
				pass
			elif utils.calculateDistance(i, j, x ,y) == 1:
				utils.convertPlotCulture(pPlot, iCiv, 80, True)
			else:
				if pPlot.getOwner() == iPreviousOwner:
					utils.convertPlotCulture(pPlot, iCiv, 20, False)


#------------------MONGOLIAN U.P.-------------------

	def setMongolAI(self): # Unused
		pCity = gc.getMap().plot(data.lLatestRazeData[3], data.lLatestRazeData[4])
		city = pCity.getPlotCity()
		iOldOwner = data.lLatestRazeData[1]
		print ("Mongol AI", iOldOwner)

		if pCity.isUnit():
			for i in range(pCity.getNumUnits()):
				unit = pCity.getUnit(i)
				if unit.getOwner() == iMongolia:
					unit.setMoves(unit.baseMoves())


	def useMongolUP(self): # Unused
		iOldOwner = data.lLatestRazeData[1]
		pCity = gc.getMap().plot(data.lLatestRazeData[3], data.lLatestRazeData[4])
		city = pCity.getPlotCity()
		print ("Mongol UP", iOldOwner)
		for (x, y) in surroundingPlots((data.lLatestRazeData[3], data.lLatestRazeData[4]), iMongolianRadius):
			tPlot = (x, y)
			pPlot = gc.getMap().plot(x, y)
			if pPlot.isCity():
				cityNear = pPlot.getPlotCity()
				iOwnerNear = cityNear.getOwner()
				if cityNear.getName() != city.getName():
					print ("iOwnerNear", iOwnerNear, "citynear", cityNear.getName())
					if iOwnerNear in [iOldOwner, iIndependent, iIndependent2]:
						print ("citynear", cityNear.getName(), "passed1")
						if cityNear.getPopulation() <= data.lLatestRazeData[2] and not cityNear.isCapital():
							print ("citynear", cityNear.getName(), "passed2")
							bUnitsApproaching = False
							for (i, j) in utils.surroundingPlots((cityNear.getX(), cityNear.getY())):
								pNear = gc.getMap().plot(i, j)
								if pNear.isUnit():
									for k in range(pNear.getNumUnits()):
										if pNear.getUnit(k).getOwner() == iMongolia:
											bUnitsApproaching = True
											break
											break
							if bUnitsApproaching:
								print ("citynear", cityNear.getName(), "passed3")
								utils.flipUnitsInCityBefore(tPlot, iMongolia, iOwnerNear)
								utils.flipCity(tPlot, 0, 0, iMongolia, [iOwnerNear])
								utils.flipUnitsInCityAfter(tPlot, iMongolia)
								utils.cultureManager(tPlot, 50, iOwnerNear, iMongolia, False, False, False)
								CyInterface().addMessage(iOwnerNear, False, iDuration, CyTranslator().getText("TXT_KEY_UP_TERROR1", ()) + " " + cityNear.getName() + " " + CyTranslator().getText("TXT_KEY_UP_TERROR2", ()), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
								CyInterface().addMessage(iMongolia, False, iDuration, CyTranslator().getText("TXT_KEY_UP_TERROR1", ()) + " " + cityNear.getName() + " " + CyTranslator().getText("TXT_KEY_UP_TERROR2", ()), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)


	def mongolUP(self, city):
		if city.getPopulation() >= 7:
			utils.makeUnitAI(iKeshik, iMongolia, (city.getX(), city.getY()), UnitAITypes.UNITAI_ATTACK_CITY, 2)
		elif city.getPopulation() >= 4:
			utils.makeUnitAI(iKeshik, iMongolia, (city.getX(), city.getY()), UnitAITypes.UNITAI_ATTACK_CITY, 1)

		#if utils.getHumanID() != iMongolia:
		#	utils.makeUnitAI(iLongbowman, iMongolia, (city.getX(), city.getY()), UnitAITypes.UNITAI_CITY_DEFENSE, 1)

		if city.getPopulation() >= 4:
			CyInterface().addMessage(iMongolia, False, iDuration, CyTranslator().getText("TXT_KEY_UP_MONGOL_HORDE", ()), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)


#------------------AMERICAN U.P.-------------------

	def checkImmigration(self):
	
		if data.iImmigrationTimer == 0:
			self.doImmigration()
			iRandom = gc.getGame().getSorenRandNum(5, 'random')
			data.iImmigrationTimer = 3 + iRandom # 3-7 turns
		else:
			data.iImmigrationTimer -= 1
			
	def doImmigration(self):
	
		# get available migration and immigration cities
		lSourceCities = []
		lTargetCities = []
		
		for iPlayer in range(iNumPlayers):
			if iPlayer in lCivBioNewWorld and not utils.isReborn(iPlayer): continue # no immigration to natives
			pPlayer = gc.getPlayer(iPlayer)
			lCities = []
			bNewWorld = pPlayer.getCapitalCity().getRegionID() in lNewWorld
			for city in utils.getCityList(iPlayer):
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
		
		#utils.debugTextPopup(str([(x.getName(), y) for (x,y) in lTargetCities]))
		#utils.debugTextPopup("Target city: "+targetCity.getName())
		#utils.debugTextPopup("Source city: "+sourceCity.getName())
		
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
			x = targetCity.getX()
			y = targetCity.getY()
			for (i, j) in utils.surroundingPlots((x, y), 2):
				pCurrent = gc.getMap().plot(i, j)
				if pCurrent.getWorkingCity() == targetCity:
					pCurrent.changeUpgradeProgress(utils.getTurns(10))
						
			# migration brings culture
			targetPlot = gc.getMap().plot(x, y)
			iTargetPlayer = targetCity.getOwner()
			iSourcePlayer = sourceCity.getOwner()
			iCultureChange = targetPlot.getCulture(iTargetPlayer) / targetCity.getPopulation()
			targetPlot.setCulture(iSourcePlayer, iCultureChange, False)
			
			# chance to spread state religion if in source city
			if gc.getPlayer(iSourcePlayer).isStateReligion():
				iReligion = gc.getPlayer(iSourcePlayer).getStateReligion()
				if sourceCity.isHasReligion(iReligion) and not targetCity.isHasReligion(iReligion):
					iRandom = gc.getGame().getSorenRandNum(3, 'random religion spread')
					if iRandom == 0:
						targetCity.setHasReligion(iReligion, True, True, True)
						
			# notify affected players
			if utils.getHumanID() == iSourcePlayer:
				CyInterface().addMessage(iSourcePlayer, False, iDuration, CyTranslator().getText("TXT_KEY_UP_EMIGRATION", (sourceCity.getName(),)), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getUnitInfo(iSettler).getButton(), ColorTypes(iYellow), sourceCity.getX(), sourceCity.getY(), True, True)
			elif utils.getHumanID() == iTargetPlayer:
				CyInterface().addMessage(iTargetPlayer, False, iDuration, CyTranslator().getText("TXT_KEY_UP_IMMIGRATION", (targetCity.getName(),)), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getUnitInfo(iSettler).getButton(), ColorTypes(iYellow), x, y, True, True)
	
			if iTargetPlayer == iCanada:
				self.canadianUP(targetCity)
		
		
	def canadianUP(self, city):
		iPopulation = 5 * city.getPopulation() / 2
		
		lProgress = []
		bAllZero = True
		for iSpecialist in [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman]:
			iProgress = city.getGreatPeopleUnitProgress(utils.getUniqueUnit(city.getOwner(), iSpecialist))
			if iProgress > 0: bAllZero = False
			lProgress.append(iProgress)
			
		if bAllZero:
			iGreatPerson = utils.getRandomEntry([iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman])
		else:
			iGreatPerson = utils.getHighestIndex(lProgress) + iGreatProphet
			
		iGreatPerson = utils.getUniqueUnit(city.getOwner(), iGreatPerson)
		
		city.changeGreatPeopleProgress(iPopulation)
		city.changeGreatPeopleUnitProgress(iGreatPerson, iPopulation)
		
		if utils.getHumanID() == city.getOwner():
			CyInterface().addMessage(city.getOwner(), False, iDuration, CyTranslator().getText("TXT_KEY_UP_MULTICULTURALISM", (city.getName(), gc.getUnitInfo(iGreatPerson).getText(), iPopulation)), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getUnitInfo(iGreatPerson).getButton(), ColorTypes(iGreen), city.getX(), city.getY(), True, True)
					
	def selectRandomCitySourceCiv(self, iCiv): # Unused
		if gc.getPlayer(iCiv).isAlive():
			cityList = [city for city in utils.getCityList(iCiv) if city.getPopulation() > 1]
			if cityList:
				return utils.getRandomEntry(cityList)
		return False


	def selectRandomCityTargetCiv(self, iCiv): # Unused
		if gc.getPlayer(iCiv).isAlive():
			lCities = []
			for city in utils.getCityList(iCiv):
				if not city.isDisorder() and city.foodDifference(False) > 0:
					lCities.append(city)
			if lCities:
				return utils.getRandomEntry(lCities)
		return False
		
	def getNewWorldCities(self): # Unused
		lCityList = []
		
		for iPlayer in range(iNumPlayers):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.getCapitalCity().getRegionID() in lNewWorld:
				for city in utils.getCityList(iPlayer):
					if city.getRegionID() in lNewWorld:
						lCityList.append(city)
						
		return lCityList
	
	def tradingCompanyCulture(self, city, iCiv, iPreviousOwner):
		tCity = (city.getX(), city.getY())
		x, y = tCity
		for (i, j) in utils.surroundingPlots(tCity):
			pPlot = gc.getMap().plot(i, j)
			if (i, j) == tCity:
				utils.convertPlotCulture(pPlot, iCiv, 51, False)
			elif pPlot.isCity():
				pass
			elif utils.calculateDistance(i, j, x ,y) == 1:
				utils.convertPlotCulture(pPlot, iCiv, 65, True)
			else:
				if pPlot.getOwner() == iPreviousOwner:
					utils.convertPlotCulture(pPlot, iCiv, 15, False)
			
	# Indonesian UP: additional gold for foreign ships in your core
	def indonesianUP(self):
		iNumUnits = 0
		for (x, y) in Areas.getCoreArea(iIndonesia):
			plot = gc.getMap().plot(x, y)
			if plot.getOwner() == iIndonesia:
				for iUnit in range(plot.getNumUnits()):
					unit = plot.getUnit(iUnit)
					if unit.getDomainType() == DomainTypes.DOMAIN_SEA:
						iOwner = unit.getOwner()
						if iOwner < iNumPlayers and iOwner != iIndonesia and not gc.getTeam(iOwner).isAtWar(iIndonesia):
							iNumUnits += 1
					
		if iNumUnits > 0:
			iGold = 5 * iNumUnits
			gc.getPlayer(iIndonesia).changeGold(iGold)
			if utils.getHumanID() == iIndonesia:
				CyInterface().addMessage(iIndonesia, False, iDuration, CyTranslator().getText("TXT_KEY_INDONESIAN_UP", (iGold,)), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
	
	# Mughal UP: receives 50% of building cost as culture when building is completed
	def mughalUP(self, city, iBuilding):
		iCost = gc.getPlayer(iMughals).getBuildingProductionNeeded(iBuilding)
		city.changeCulture(iMughals, iCost / 2, True)