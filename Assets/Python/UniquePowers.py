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
from StoredData import sd # edead
import Consts as con
import RFCUtils
from operator import itemgetter
import Areas
utils = RFCUtils.RFCUtils()

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer


### Constants ###


# initialise player variables
iEgypt = con.iEgypt
iIndia = con.iIndia
iChina = con.iChina
iBabylonia = con.iBabylonia
iGreece = con.iGreece
iPersia = con.iPersia
iPhoenicia = con.iPhoenicia
iRome = con.iRome
iTamils = con.iTamils
iJapan = con.iJapan
iByzantium = con.iByzantium
iVikings = con.iVikings
iArabia = con.iArabia
iKhmer = con.iKhmer
iIndonesia = con.iIndonesia
iMoors = con.iMoors
iSpain = con.iSpain
iFrance = con.iFrance
iEngland = con.iEngland
iHolyRome = con.iHolyRome
iRussia = con.iRussia
iMali = con.iMali
iTurkey = con.iTurkey
iInca = con.iInca
iMongolia = con.iMongolia
iMughals = con.iMughals
iAztecs = con.iAztecs
iThailand = con.iThailand
iGermany = con.iGermany
iAmerica = con.iAmerica
iBrazil = con.iBrazil
iNumPlayers = con.iNumPlayers
iNumMajorPlayers = con.iNumMajorPlayers
#iNetherlands = con.iNetherlands
#iPortugal = con.iPortugal
iNumActivePlayers = con.iNumActivePlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iNative = con.iNative
iCeltia = con.iCeltia
iSeljuks = con.iSeljuks
iBarbarian = con.iBarbarian
iNumTotalPlayers = con.iNumTotalPlayers


pMongolia = gc.getPlayer(iMongolia)
teamMongolia = gc.getTeam(pMongolia.getTeam())

pRome = gc.getPlayer(iRome)
teamRome = gc.getTeam(pRome.getTeam())

pGreece = gc.getPlayer(iGreece)


tRussianTopLeft = (65, 49)
tRussianBottomRight = (121, 65)


iNumReligions = con.iNumReligions


#Buildings
iTemple = con.iTemple
iCathedral = con.iCathedral
iMonastery = con.iMonastery


iMongolianRadius = 4
iMongolianTimer = 1



class UniquePowers:

     
##################################################
### Secure storage & retrieval of script data ###
################################################   
		
	def getImmigrationTimer(self):
		return sd.scriptDict['iImmigrationTimer']
		
	def setImmigrationTimer(self, iNewValue):
		sd.scriptDict['iImmigrationTimer'] = iNewValue

	def getLatestRazeData( self, i ):
		return sd.scriptDict['lLatestRazeData'][i]

	def setLatestRazeData( self, i, iNewValue ):
		sd.scriptDict['lLatestRazeData'][i] = iNewValue
	
	def getTempFlippingCity( self ):
		return sd.scriptDict['tempFlippingCity']

	def setTempFlippingCity( self, tNewValue ):
		sd.scriptDict['tempFlippingCity'] = tNewValue

	#for Victory

	def getEnslavedUnits( self ):
		return sd.scriptDict['iEnslavedUnits']
	    
	def setEnslavedUnits( self, iNewValue ):
		sd.scriptDict['iEnslavedUnits'] = iNewValue

	# Roman UP

	def increaseRomanVictories(self):
		sd.scriptDict['iRomanVictories'] += 1

	def resetRomanVictories(self):
		sd.scriptDict['iRomanVictories'] = 0

	def getRomanVictories(self):
		return sd.scriptDict['iRomanVictories']

#######################################
### Main methods (Event-Triggered) ###
#####################################  

       	
	def checkTurn(self, iGameTurn):

		print("UniquePowers.checkTurn()")
			
		if (iGameTurn >= getTurnForYear(860)):
			self.russianUP()

		if (iGameTurn >= getTurnForYear(con.tBirth[iAmerica])+utils.getTurns(5)):
			self.checkImmigration()
			
		self.indonesianUP()

		#if iGameTurn == getTurnForYear(con.tBirth[iRome]+1):
		#	for iCiv in range(iNumActivePlayers):
		#		if teamRome.isAtWar(iCiv):
		#			self.setRomanWar(iCiv, -1)

		#if (iGameTurn >= getTurnForYear(con.tBirth[iRome])+2):
		#	print("Check Roman war")
		#	self.checkRomanWar()

		#if (iGameTurn >= getTurnForYear(1190)):
		#if (iGameTurn >= 0): #debug
			#for iTimer in range(iMongolianTimer+1):
				#if (iGameTurn == self.getLatestRazeData(0)+iTimer):
					#self.useMongolUP()
					
	def onChangeWar(self, bWar, iTeam, iOtherTeam):
	
		# reset Mongol UP flags when peace is made
		if not bWar:
			if iTeam == con.iMongolia:
				for city in utils.getCityList(iOtherTeam):
					city.setMongolUP(False)
			elif iOtherTeam == con.iMongolia:
				for city in utils.getCityList(iTeam):
					city.setMongolUP(False)
					
#------------------VIKING UP----------------------

	def vikingUP(self, argsList):
	
		pWinningUnit, pLosingUnit = argsList
		cLosingUnit = PyHelpers.PyInfo.UnitInfo(pLosingUnit.getUnitType())
		
		iOwner = pWinningUnit.getOwner()
		
		if (iOwner == iVikings and gc.getPlayer(iVikings).getCurrentEra() <= con.iMedieval) or pWinningUnit.getUnitType() == con.iMoorishCorsair:
			if cLosingUnit.getDomainType() == gc.getInfoTypeForString("DOMAIN_SEA"):
				iGold = cLosingUnit.getProductionCost() / 2
				gc.getPlayer(iOwner).changeGold(iGold)
				sAdjective = gc.getPlayer(pLosingUnit.getOwner()).getCivilizationAdjectiveKey()
				CyInterface().addMessage(iOwner, False, con.iDuration, CyTranslator().getText("TXT_KEY_VIKING_NAVAL_UP", (iGold, sAdjective, pLosingUnit.getNameKey())), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
				
				if iOwner == iVikings:
					sd.changeVikingGold(iGold)
				elif iOwner == iMoors:
					sd.changeMoorishGold(iGold)
				
			

#------------------ROMAN UP-----------------------

	def doRomanWar(self, iCiv):
	
		if iCiv in [iPhoenicia, iPersia, iCeltia, iEgypt]:
			iNumTargets = 2
			self.romanConquestUP(iCiv, iNumTargets)
		elif iCiv == iGreece and utils.getHumanID() != iGreece:
			bEgypt = False
			cityList = PyPlayer(iGreece).getCityList()
			
			for pCity in cityList:
				city = pCity.GetCy()
				if city.getRegionID() == con.rEgypt:
					bEgypt = True
					break
					
			if bEgypt:
				iNumTargets = 2
				self.romanConquestUP(iCiv, iNumTargets, [con.rEgypt])
			else:
				iNumTargets = 3
			
			self.romanConquestUP(iCiv, iNumTargets)

		#if gc.getPlayer(iRome).isReborn():
		#	return
		#
		#for iCiv in range(iNumActivePlayers):
		#	#print("Roman war status with "+gc.getPlayer(iCiv).getCivilizationShortDescriptionKey()+": "+str(self.getRomanWar(iCiv)))
		#	if self.getRomanWar(iCiv) == -1:
		#		#print("Roman war status -1 with "+str(iCiv))
		#		if (not teamRome.isAtWar(iCiv)):
		#			print("Set Roman war to 0.")
		#			self.setRomanWar(iCiv, 0)
		#	elif self.getRomanWar(iCiv) == 0:
		#		#print("Roman war status 0 with "+str(iCiv))
		#		if teamRome.isAtWar(iCiv):
		#			#print("Set Roman War to 1")
		#			self.setRomanWar(iCiv, 1)
		#			if (iCiv in con.lCivGroups[2]) or (iCiv in con.lCivGroups[3]):
		#				print ("Roman conquest triggered.")
		#				iNumTargets = 1
		#				if utils.getHumanID() != iRome and iCiv == iPersia: iNumTargets = 2
		#				
		#				self.romanConquestUP(iCiv, iNumTargets)
		#				print ("Roman conquest completed.")

#	def romanCombatUP(self, argsList):
#
#		pWinningUnit, pLosingUnit = argsList
#		pWinningPlayer = gc.getPlayer(pWinningUnit.getOwner())
#		
#		if (pWinningPlayer.getID() != iRome or pWinningPlayer.isReborn()):
#			return
#
##		pLosingPlayer = gc.getPlayer(pLosingUnit.getOwner())
#
#		if not pLosingPlayer.isBarbarian():
#			self.increaseRomanVictories()
#		
#		if self.getRomanVictories() >= 5:
#			utils.makeUnit(con.iRomanLegion, iRome, (pWinningUnit.getX(), pWinningUnit.getY()), 1)
#			self.resetRomanVictories()
#			
#			CyInterface().addMessage(iRome, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_ROMAN_TRIUMPH", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)

	def romanConquestUP(self, iEnemy, iNumTargets=1, lPreferredTargetRegions=[]):

		#pEnemy = gc.getPlayer(iEnemy)

		#print ("Getting random target city.")
		#pTargetCity = utils.getRandomCity(iEnemy)
		#tPlot = con.tCapitals[0][iRome]
		
		lEnemyCities = []
		lPreferredCities = []
		
		print "Getting closest city."
		cityList = PyPlayer(iEnemy).getCityList()
		for city in cityList:
			pCity = city.GetCy()
			iDist = utils.calculateDistance(pCity.getX(), pCity.getY(), pRome.getCapitalCity().getX(), pRome.getCapitalCity().getY())
			lEnemyCities.append((iDist, pCity))
			if pCity.getRegionID() in lPreferredTargetRegions:
				lPreferredCities.append((iDist, pCity))
				
		if len(lPreferredCities) > 0:
			lEnemyCities = lPreferredCities
			
		lEnemyCities.sort()
		
		for i in range(iNumTargets):
			if len(lEnemyCities) > 0:
				pTargetCity = lEnemyCities.pop(0)[1]
				tPlot = utils.findNearestLandPlot((pTargetCity.getX(), pTargetCity.getY()), iRome)
				
				iExtra = 0
				if utils.getHumanID() != iRome and utils.getHumanID() != iEnemy: iExtra = 1
				
				utils.makeUnitAI(con.iRomanLegion, iRome, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2+iExtra)
				utils.makeUnitAI(con.iCatapult, iRome, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1+iExtra*2)

		#if (pTargetCity != -1):
		#	print ("City found, searching free land plot.")
		#	tPlot = utils.findNearestLandPlot((pTargetCity.getX(),pTargetCity.getY()), iRome)
		#else:
		#	print ("No plot found, spawning in Roma instead.")

		# weaken the effect if human player is Rome
		#if (utils.getHumanID() == iRome):
		#	utils.makeUnitAI(con.iRomanLegion, iRome, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
		#	utils.makeUnitAI(con.iCatapult, iRome, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
		#else:
		#	utils.makeUnitAI(con.iRomanLegion, iRome, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
		#	utils.makeUnitAI(con.iCatapult, iRome, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
		#print ("Units created.")

		#utils.makeUnit(con.iRomanLegion, iRome, tPlot, 3)
		#utils.makeUnit(con.iCatapult, iRome, tPlot, 2)
				
		#utils.debugTextPopup("Roman conquerors against "+CyTranslator().getText(str(gc.getPlayer(iEnemy).getCivilizationShortDescriptionKey()), ()))

		CyInterface().addMessage(iRome, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_ROMAN_CONQUESTS",(gc.getPlayer(iEnemy).getCivilizationShortDescriptionKey(),)), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
		CyInterface().addMessage(iEnemy, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_ROMAN_CONQUESTS_TARGET", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
		print ("Message displayed.")
		
	def greekConquestUP(self, iEnemy, iNumTargets=1):
		lEnemyCities = []
		
		print "Getting closest city."
		cityList = PyPlayer(iEnemy).getCityList()
		for city in cityList:
			pCity = city.GetCy()
			iDist = utils.calculateDistance(pCity.getX(), pCity.getY(), pGreece.getCapitalCity().getX(), pGreece.getCapitalCity().getY())
			lEnemyCities.append((iDist, pCity))
			
		lEnemyCities.sort()
		
		for i in range(iNumTargets):
			if len(lEnemyCities) > 0:
				pTargetCity = lEnemyCities.pop(0)[1]
				tPlot = utils.findNearestLandPlot((pTargetCity.getX(), pTargetCity.getY()), iRome)
				
				iExtra = 0
				if utils.getHumanID() != iGreece and utils.getHumanID() != iEnemy: 
					iExtra = 1
					if iEnemy == iPersia: iExtra = 2
				
				utils.makeUnitAI(con.iGreekHoplite, iGreece, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2+iExtra*2)
				utils.makeUnitAI(con.iCatapult, iGreece, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1+iExtra*2)
				
		CyInterface().addMessage(iEnemy, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_GREEK_CONQUESTS_TARGET", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
		
	def tamilConquestUP(self, iEnemy, iNumTargets=1):
		lEnemyCities = []
		
		print "Getting closest city."
		cityList = PyPlayer(iEnemy).getCityList()
		for city in cityList:
			pCity = city.GetCy()
			iDist = utils.calculateDistance(pCity.getX(), pCity.getY(), pGreece.getCapitalCity().getX(), pGreece.getCapitalCity().getY())
			lEnemyCities.append((iDist, pCity))
			
		lEnemyCities.sort()
		
		for i in range(iNumTargets):
			if len(lEnemyCities) > 0:
				pTargetCity = lEnemyCities.pop(0)[1]
				tPlot = utils.findNearestLandPlot((pTargetCity.getX(), pTargetCity.getY()), iTamils)
				
				utils.makeUnitAI(con.iSwordsman, iTamils, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
				utils.makeUnitAI(con.iWarElephant, iTamils, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
				utils.makeUnitAI(con.iCatapult, iTamils, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
				
		CyInterface().addMessage(iEnemy, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_TAMIL_CONQUESTS_TARGET", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)


#------------------ARABIAN U.P.-------------------

	def mughalUP(self, city):
		return
		pMughals = gc.getPlayer(iMughals)
		iStateReligion = pMughals.getStateReligion()

		if iStateReligion >= 0:
			city.setHasReligion(iStateReligion, True, True, False)

	def seljukUP(self, city):
		return
		pSeljuks = gc.getPlayer(iSeljuks)
		iStateReligion = pSeljuks.getStateReligion()

		if iStateReligion >= 0:
			for iReligion in range(con.iNumReligions):	# Leoreth: now removes foreign religions and buildings (except holy cities) as well
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
		pArabia = gc.getPlayer(iArabia)
		iStateReligion = pArabia.getStateReligion()

		if (iStateReligion >= 0):
			#for iReligion in range(con.iNumReligions):	# Leoreth: now removes foreign religions and buildings (except holy cities) as well
			#	if city.isHasReligion(iReligion) and not city.isHolyCityByType(iReligion):
			#		city.setHasReligion(iReligion, False, False, False)
			#	if city.hasBuilding(iTemple + iReligion*4):
			#		city.setHasRealBuilding((iTemple + iReligion*4), False)
			#	if city.hasBuilding(iCathedral + iReligion*4):
			#		city.setHasRealBuilding((iCathedral + iReligion*4), False)
			#	if city.hasBuilding(iMonastery + iReligion*4):
			#		city.setHasRealBuilding((iMonastery + iReligion*4), False)

			if (not city.isHasReligion(iStateReligion)):
				city.setHasReligion(iStateReligion, True, True, False)
			if (not city.hasBuilding(iTemple + iStateReligion*4)):
				city.setHasRealBuilding((iTemple + iStateReligion*4), True)

#------------------AZTEC U.P.-------------------

	def aztecUP(self, argsList): #Real Slavery by Sevo
		pWinningUnit,pLosingUnit = argsList
		pWinningPlayer = gc.getPlayer(pWinningUnit.getOwner())
		
		if (pWinningPlayer.getID() != iAztecs):
			return
			
		if utils.isReborn(iAztecs): return

		pLosingPlayer = gc.getPlayer(pLosingUnit.getOwner())
		cLosingUnit = PyHelpers.PyInfo.UnitInfo(pLosingUnit.getUnitType())
		
		if (pLosingUnit.getUnitType() < con.iWarrior):
			return
		
		# Only enslave land units!!
		if (cLosingUnit.getDomainType() == gc.getInfoTypeForString("DOMAIN_LAND")):
			iRandom = gc.getGame().getSorenRandNum(100, 'capture chance')
			if (iRandom < 35):
				pNewUnit = pWinningPlayer.initUnit(con.iAztecSlave, pWinningUnit.getX(), pWinningUnit.getY(), UnitAITypes.UNITAI_ENGINEER, DirectionTypes.DIRECTION_SOUTH)
				CyInterface().addMessage(pWinningPlayer.getID(),True,15,CyTranslator().getText("TXT_KEY_UP_ENSLAVE_WIN", ()),'SND_REVOLTEND',1,'Art/Units/slave/button_slave.dds',ColorTypes(8),pWinningUnit.getX(),pWinningUnit.getY(),True,True)
				CyInterface().addMessage(pLosingPlayer.getID(),True,15,CyTranslator().getText("TXT_KEY_UP_ENSLAVE_LOSE", ()),'SND_REVOLTEND',1,'Art/Units/slave/button_slave.dds',ColorTypes(7),pWinningUnit.getX(),pWinningUnit.getY(),True,True)		
				if (pLosingUnit.getOwner() not in con.lCivGroups[5] and pLosingUnit.getOwner() < con.iNumPlayers): # old world civs now
					sd.changeAztecSlaves(1)



#------------------RUSSIAN U.P.-------------------

	def russianUP(self):
		pRussia = gc.getPlayer(iRussia)
		teamRussia = gc.getTeam(pRussia.getTeam()) 
		for x in range(tRussianTopLeft[0], tRussianBottomRight[0]):
			for y in range(tRussianTopLeft[1], tRussianBottomRight[1]):
				pCurrent = gc.getMap().plot( x, y )
				if (pCurrent.getOwner() == iRussia):
					iNumUnitsInAPlot = pCurrent.getNumUnits()
					if (iNumUnitsInAPlot):
						for i in range(iNumUnitsInAPlot):
							unit = pCurrent.getUnit(i)
							if (teamRussia.isAtWar(unit.getOwner())):
##								print("hp", unit.currHitPoints() )
##								print("damage", unit.getDamage() )
								unit.setDamage(unit.getDamage()+8, iRussia)
##								print("hp now", unit.currHitPoints() 
##								print("damage", unit.getDamage() )




#------------------TURKISH U.P.-------------------


	def turkishUP(self, city, iCiv, iPreviousOwner):
	       
		for x in range(city.getX()-2, city.getX()+3):
			for y in range(city.getY()-2, city.getY()+3):
				pCurrent = gc.getMap().plot( x, y )
				if (x == city.getX() and y == city.getY()):
					utils.convertPlotCulture(pCurrent, iCiv, 51, False)
				elif (pCurrent.isCity()):
					pass
				elif (utils.calculateDistance(x, y, city.getX(), city.getY()) == 1):
					utils.convertPlotCulture(pCurrent, iCiv, 80, True)
				else:
					if pCurrent.getOwner() == iPreviousOwner:
						utils.convertPlotCulture(pCurrent, iCiv, 20, False)


#------------------MONGOLIAN U.P.-------------------

	def setMongolAI(self):
		pCity = gc.getMap().plot( self.getLatestRazeData(3), self.getLatestRazeData(4) )
		city = pCity.getPlotCity()
		iOldOwner = self.getLatestRazeData(1)
		print ("Mongol AI", iOldOwner)

		if (pCity.getNumUnits() > 0):
			for i in range(pCity.getNumUnits()):
				unit = pCity.getUnit(i)
				if (unit.getOwner() == iMongolia):
					if (unit.baseMoves() == 2):
						unit.setMoves(2)
					if (unit.baseMoves() == 1):
						unit.setMoves(1)
		
##		targetCity = -1
##		if (not pMongolia.isHuman()):
##			for x in range(self.getLatestRazeData(3) -3, self.getLatestRazeData(3) +1 +3):
##				for y in range(self.getLatestRazeData(4) -3, self.getLatestRazeData(4) +1 +3):
##					pCurrent = gc.getMap().plot( x, y )
##					if ( pCurrent.isCity()):
##						cityNear = pCurrent.getPlotCity()
##						iOwnerNear = cityNear.getOwner()
##						if (cityNear.getName() != city.getName()):
##							print ("iOwnerNear", iOwnerNear, "citynear", cityNear.getName())
##							if (iOwnerNear == iOldOwner):
##								if (cityNear != city):
##									if (cityNear.getPopulation() <= self.getLatestRazeData(2)):
##										targetCity = cityNear
##										print ("targetCity", targetCity)
##										break
##										break
##			if (targetCity != -1):
##				targetPlot = -1
##				for j in range(targetCity.getX() -1, targetCity.getX() +1 +2):
##					for k in range(targetCity.getY() -1, targetCity.getY() +1 +2):
##						pCurrentTarget = gc.getMap().plot( j, k )
##						if (pCurrentTarget.getNumUnits() == 0):
##							iDistance = gc.getMap().calculatePathDistance(pCurrentTarget, pCity)
##							if (iDistance <= 2):
##								targetPlot = pCurrentTarget
##								print ("pCurrentTarget", pCurrentTarget)
##								break
##								break
##				for m in range(city.getX() -1, city.getX() +1 +2):
##					for n in range(city.getY() -1, city.getY() +1 +2):
##						pMongol = gc.getMap().plot( m, n )
##						if (pMongol.getNumUnits() > 0):
##							print ("numunits>0")
##							for i in range(pCity.getNumUnits()):
##								unit = pCity.getUnit(i)
##								if (unit.getOwner() == iMongolia):
##									#if (unit.getMoves() >= 2):
##									print ("unit", unit)
##									unit.setXY(targetPlot.getX(), targetPlot.getY())
##									break
##									break
##									break
				


	def useMongolUP(self):
		iOldOwner = self.getLatestRazeData(1)
		pCity = gc.getMap().plot( self.getLatestRazeData(3), self.getLatestRazeData(4) )
		city = pCity.getPlotCity()
		print ("Mongol UP", iOldOwner)
		for x in range(self.getLatestRazeData(3) -iMongolianRadius, self.getLatestRazeData(3) +1 +iMongolianRadius):
			for y in range(self.getLatestRazeData(4) -iMongolianRadius, self.getLatestRazeData(4) +1 +iMongolianRadius):
				pCurrent = gc.getMap().plot( x, y )
				if ( pCurrent.isCity()):
					cityNear = pCurrent.getPlotCity()
					iOwnerNear = cityNear.getOwner()
					if (cityNear.getName() != city.getName()):
						print ("iOwnerNear", iOwnerNear, "citynear", cityNear.getName())
						if (iOwnerNear == iOldOwner or iOwnerNear == iIndependent or iOwnerNear == iIndependent2):
							print ("citynear", cityNear.getName(), "passed1")
							if (cityNear.getPopulation() <= self.getLatestRazeData(2) and not cityNear.isCapital()):
								print ("citynear", cityNear.getName(), "passed2")
								iApproachingUnits = 0
								for j in range(cityNear.getX() -1, cityNear.getX() +2):
									for k in range(cityNear.getY() -1, cityNear.getY() +2):
										pNear = gc.getMap().plot( j, k )
										if (pNear.getNumUnits() > 0):
											for l in range(pNear.getNumUnits()):
												if(pNear.getUnit(l).getOwner() == iMongolia):
													iApproachingUnits += 1
													break
													break
													break													
								if (iApproachingUnits > 0):
									print ("citynear", cityNear.getName(), "passed3")
									utils.flipUnitsInCityBefore((x,y), iMongolia, iOwnerNear)
									self.setTempFlippingCity((x,y))
									utils.flipCity((x,y), 0, 0, iMongolia, [iOwnerNear])
									utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iMongolia)
									utils.cultureManager(self.getTempFlippingCity(), 50, iOwnerNear, iMongolia, False, False, False)
									CyInterface().addMessage(iOwnerNear, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_TERROR1", ()) + " " + cityNear.getName() + " " + CyTranslator().getText("TXT_KEY_UP_TERROR2", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
									CyInterface().addMessage(iMongolia, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_TERROR1", ()) + " " + cityNear.getName() + " " + CyTranslator().getText("TXT_KEY_UP_TERROR2", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)


	def mongolUP(self, city):
		if (city.getPopulation() >= 7):
			utils.makeUnitAI(con.iMongolianKeshik, iMongolia, (city.getX(), city.getY()), UnitAITypes.UNITAI_ATTACK_CITY, 2)
		elif (city.getPopulation() >= 4):
			utils.makeUnitAI(con.iMongolianKeshik, iMongolia, (city.getX(), city.getY()), UnitAITypes.UNITAI_ATTACK_CITY, 1)

		#if utils.getHumanID() != iMongolia:
		#	utils.makeUnitAI(con.iLongbowman, iMongolia, (city.getX(), city.getY()), UnitAITypes.UNITAI_CITY_DEFENSE, 1)

		if city.getPopulation() >= 4:
			CyInterface().addMessage(iMongolia, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_MONGOL_HORDE", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)


#------------------AMERICAN U.P.-------------------

	def checkImmigration(self):
	
		if self.getImmigrationTimer() == 0:
			self.doImmigration()
			iRandom = gc.getGame().getSorenRandNum(5, 'random')
			self.setImmigrationTimer(3 + iRandom) # 3-7 turns
		else:
			self.setImmigrationTimer(self.getImmigrationTimer() - 1)
			
	def doImmigration(self):
	
		# get available migration and immigration cities
		lSourceCities = []
		lTargetCities = []
		
		for iPlayer in range(con.iNumPlayers):
			if iPlayer in con.lCivBioNewWorld and not utils.isReborn(iPlayer): continue # no immigration to natives
			pPlayer = gc.getPlayer(iPlayer)
			lCities = []
			bNewWorld = pPlayer.getCapitalCity().getRegionID() in con.lNewWorld
			for city in utils.getCityList(iPlayer):
				if city.foodDifference(False) <= 0: continue
				iHappinessDifference = city.happyLevel() - city.unhappyLevel(0)
				if city.getRegionID() in con.lNewWorld and bNewWorld:
					iNorthAmericaBonus = 0
					if city.getRegionID() in [con.rCanada, con.rUnitedStates]: iNorthAmericaBonus = 5
					if iHappinessDifference > 0: lCities.append((city, iHappinessDifference + city.foodDifference(False) / 2 + city.getPopulation() / 2 + iNorthAmericaBonus))
				elif city.getRegionID() not in con.lNewWorld and not bNewWorld:
					if iHappinessDifference < 0: lCities.append((city, -iHappinessDifference))
			
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
			for i in range(x-2, x+3):
				for j in range(y-2, y+3):
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
				CyInterface().addMessage(iSourcePlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_EMIGRATION", (sourceCity.getName(),)), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getUnitInfo(con.iSettler).getButton(), ColorTypes(con.iYellow), sourceCity.getX(), sourceCity.getY(), True, True)
			elif utils.getHumanID() == iTargetPlayer:
				CyInterface().addMessage(iTargetPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_IMMIGRATION", (targetCity.getName(),)), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getUnitInfo(con.iSettler).getButton(), ColorTypes(con.iYellow), x, y, True, True)
	
			if iTargetPlayer == con.iCanada:
				self.canadianUP(targetCity)
		
		
	def canadianUP(self, city):
		iPopulation = 5 * city.getPopulation() / 2
		
		lProgress = []
		bAllZero = True
		for iSpecialist in [con.iGreatProphet, con.iGreatArtist, con.iGreatScientist, con.iGreatMerchant, con.iGreatEngineer, con.iGreatGeneral, con.iGreatSpy]:
			iProgress = city.getGreatPeopleUnitProgress(utils.getUniqueUnit(city.getOwner(), iSpecialist))
			if iProgress > 0: bAllZero = False
			lProgress.append(iProgress)
			
		if bAllZero:
			iGreatPerson = utils.getRandomEntry([con.iGreatProphet, con.iGreatArtist, con.iGreatScientist, con.iGreatMerchant, con.iGreatEngineer, con.iGreatSpy])
		else:
			iGreatPerson = utils.getHighestIndex(lProgress) + con.iGreatProphet
			
		iGreatPerson = utils.getUniqueUnit(city.getOwner(), iGreatPerson)
		
		city.changeGreatPeopleProgress(iPopulation)
		city.changeGreatPeopleUnitProgress(iGreatPerson, iPopulation)
		
		if utils.getHumanID() == city.getOwner():
			CyInterface().addMessage(city.getOwner(), False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_MULTICULTURALISM", (city.getName(), gc.getUnitInfo(iGreatPerson).getText(), iPopulation)), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getUnitInfo(iGreatPerson).getButton(), ColorTypes(con.iGreen), city.getX(), city.getY(), True, True)
					
	def selectRandomCitySourceCiv(self, iCiv):
		if (gc.getPlayer(iCiv).isAlive()):
			cityList = []
			for pyCity in PyPlayer(iCiv).getCityList():
				if (pyCity.GetCy()):
					if ( pyCity.GetCy().getPopulation() > 1):			
						cityList.append(pyCity.GetCy())
			if (len(cityList)):
				iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
				return cityList[iCity]
		return False				


	def selectRandomCityTargetCiv(self, iCiv):
		if gc.getPlayer(iCiv).isAlive():
			lCities = []
			for city in utils.getCityList(iCiv):
				if not city.isDisorder() and city.foodDifference(False) > 0:
					lCities.append(city)
			if lCities:
				return utils.getRandomEntry(lCities)
		return False
		
	def getNewWorldCities(self):
		lCityList = []
		
		for iPlayer in range(con.iNumPlayers):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.getCapitalCity().getRegionID() in con.lNewWorld:
				for city in PyPlayer(iPlayer).getCityList():
					pCity = city.GetCy()
					if pCity.getRegionID() in con.lNewWorld:
						lCityList.append(pCity)
						
		return lCityList
	
	def tradingCompanyCulture(self, city, iCiv, iPreviousOwner):
	       
		for x in range(city.getX()-1, city.getX()+2):
			for y in range(city.getY()-1, city.getY()+2):
				pCurrent = gc.getMap().plot( x, y )
				if (x == city.getX() and y == city.getY()):
					utils.convertPlotCulture(pCurrent, iCiv, 51, False)
				elif (pCurrent.isCity()):
					pass
				elif (utils.calculateDistance(x, y, city.getX(), city.getY()) == 1):
					utils.convertPlotCulture(pCurrent, iCiv, 65, True)
				else:
					if pCurrent.getOwner() == iPreviousOwner:
						utils.convertPlotCulture(pCurrent, iCiv, 15, False)
			
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
						if iOwner < con.iNumPlayers and iOwner != iIndonesia and not gc.getTeam(iOwner).isAtWar(iIndonesia):
							iNumUnits += 1
					
		if iNumUnits > 0:
			iGold = 5 * iNumUnits
			gc.getPlayer(iIndonesia).changeGold(iGold)
			if utils.getHumanID() == iIndonesia:
				CyInterface().addMessage(iIndonesia, False, con.iDuration, CyTranslator().getText("TXT_KEY_INDONESIAN_UP", (iGold,)), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
				