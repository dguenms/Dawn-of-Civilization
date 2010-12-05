# Rhye's and Fall of Civilization - (a part of) Unique Powers

#Egypt in CvPlayer::canDoCivics() and in WBS
#India in CvPlayer::updateMaxAnarchyTurns()
#China (and England before the change) in CvPlayer::getProductionNeeded()
#Babylonia in CvPlayer.cpp::acquireCity()
# Babylonia now in CvPlayer::getCapitalYieldModifier(); +33% production and commerce in the capital after Code of Laws
#Greece CvCity:getGreatPeopleRate()
#Carthage in MercenaryUtils.py and CvMercenarymanager.py
# Phoenicia now in CvCity::getTradeRouteModifier()
#Persia (USED TO BE in CvHandicapInfo::getDistanceMaintenancePercentByID(); THEN in RiseAndFall.py, collapseCapitals()), NOW in Stability.py, onCityAcquired()
#Rome in CvPlot::movementCost()
#Japan, Spain and England in CvUnit::init(). Turkey used to be there as well
# Japan now in CvUnit::experienceNeeded(); +50% promotion tempo
# England now in CvHandicapInfo::getDistanceMaintenancePercentByID()
#Ethiopia in Congresses.py (USED TO BE in CvUnit::init() and CvUnit::upgrade())
#Maya in CvHandicapInfo::getResearchPercentByID()
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
iCarthage = con.iCarthage
iRome = con.iRome
iJapan = con.iJapan
iByzantium = con.iByzantium
iVikings = con.iVikings
iArabia = con.iArabia
iSpain = con.iSpain
iFrance = con.iFrance
iEngland = con.iEngland
iGermany = con.iGermany
iRussia = con.iRussia
iMali = con.iMali
iTurkey = con.iTurkey
iInca = con.iInca
iMongolia = con.iMongolia
iAztecs = con.iAztecs
iAmerica = con.iAmerica
iNumPlayers = con.iNumPlayers
iNumMajorPlayers = con.iNumMajorPlayers
#iHolland = con.iHolland
#iPortugal = con.iPortugal
iNumActivePlayers = con.iNumActivePlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iNative = con.iNative
iCeltia = con.iCeltia
iBarbarian = con.iBarbarian
iNumTotalPlayers = con.iNumTotalPlayers


pMongolia = gc.getPlayer(iMongolia)
teamMongolia = gc.getTeam(pMongolia.getTeam())

pRome = gc.getPlayer(iRome)
teamRome = gc.getTeam(pRome.getTeam())


tRussianTopLeft = (65, 49)
tRussianBottomRight = (121, 65)


iNumReligions = con.iNumReligions


#Buildings
iTemple = con.iTemple
iCathedral = con.iCathedral



iMongolianRadius = 4
iMongolianTimer = 1



class UniquePowers:

     
##################################################
### Secure storage & retrieval of script data ###
################################################   
		
        def getImmigrationTurnLength( self ):
                return sd.scriptDict['iImmigrationTurnLength']

        def setImmigrationTurnLength( self, iNewValue ):
                sd.scriptDict['iImmigrationTurnLength'] = iNewValue

        def getImmigrationCurrentTurn( self ):
                return sd.scriptDict['iImmigrationCurrentTurn']

        def setImmigrationCurrentTurn( self, iNewValue ):
                sd.scriptDict['iImmigrationCurrentTurn'] = iNewValue

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

	def getRomanWar(self, iPlayer):
		return sd.scriptDict['lRomanWars'][iPlayer]

	def setRomanWar(self, iPlayer, iValue):
		sd.scriptDict['lRomanWars'][iPlayer] = iValue

#######################################
### Main methods (Event-Triggered) ###
#####################################  

       	
        def checkTurn(self, iGameTurn):
                        
                if (iGameTurn >= getTurnForYear(860)):
                        self.russianUP()

                if (iGameTurn >= getTurnForYear(con.tBirth[iAmerica])+utils.getTurns(5) and ((self.getImmigrationTurnLength() != 0) or ((gc.getGame().getSorenRandNum(30, 'random') % 20) == 0 and gc.getPlayer(iAmerica).isAlive()))):
                        self.americanUP()

		if iGameTurn == getTurnForYear(con.tBirth[iRome]+1):
			for iCiv in range(iNumActivePlayers):
				if teamRome.isAtWar(iCiv):
					self.setRomanWar(iCiv, -1)

		if (iGameTurn >= getTurnForYear(con.tBirth[iRome])+2):
			self.checkRomanWar()

                #if (iGameTurn >= getTurnForYear(1190)):
                #if (iGameTurn >= 0): #debug
                        #for iTimer in range(iMongolianTimer+1):
                                #if (iGameTurn == self.getLatestRazeData(0)+iTimer):
                                        #self.useMongolUP()

#------------------ROMAN UP-----------------------

	def checkRomanWar(self):
		
		for iCiv in range(iNumActivePlayers):
			if self.getRomanWar(iCiv) == -1:
				if (not teamRome.isAtWar(iCiv)):
					self.setRomanWar(iCiv, 0)
			elif self.getRomanWar(iCiv) == 0:
				if teamRome.isAtWar(iCiv):
					self.setRomanWar(iCiv, 1)
					if (iCiv in con.lCivGroups[2]) or (iCiv in con.lCivGroups[3]):
						print "Roman conquest triggered."
						self.romanConquestUP(iCiv)

#        def romanCombatUP(self, argsList):
#
#		pWinningUnit, pLosingUnit = argsList
#                pWinningPlayer = gc.getPlayer(pWinningUnit.getOwner())
#		
#                if (pWinningPlayer.getID() != iRome or pWinningPlayer.isReborn()):
#                        return
#
##                pLosingPlayer = gc.getPlayer(pLosingUnit.getOwner())
#
#                if not pLosingPlayer.isBarbarian():
#                        self.increaseRomanVictories()
#                
#                if self.getRomanVictories() >= 5:
#                        utils.makeUnit(con.iRomePraetorian, iRome, (pWinningUnit.getX(), pWinningUnit.getY()), 1)
#                        self.resetRomanVictories()
#			
#                        CyInterface().addMessage(iRome, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_ROMAN_TRIUMPH", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)

	def romanConquestUP(self, iEnemy):

		#pEnemy = gc.getPlayer(iEnemy)
	
		pTargetCity = utils.getRandomCity(iEnemy)

		if (pTargetCity != -1):
			tPlot = utils.findNearestLandPlot((pTargetCity.getX(),pTargetCity.getY()), iRome)
		
		if (not tPlot):
			tPlot = con.tCapitals[0][iRome]

		utils.makeUnitAI(con.iRomePraetorian, iRome, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
		utils.makeUnitAI(con.iCatapult, iRome, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)

		#utils.makeUnit(con.iRomePraetorian, iRome, tPlot, 3)
		#utils.makeUnit(con.iCatapult, iRome, tPlot, 2)

		CyInterface().addMessage(iRome, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_ROMAN_CONQUESTS", (gc.getPlayer(iEnemy).getCivilizationShortDescription(0),)), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
		CyInterface().addMessage(iEnemy, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_ROMAN_CONQUESTS_TARGET", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
		


#------------------ARABIAN U.P.-------------------

        def arabianUP(self, city):
                pArabia = gc.getPlayer(iArabia)
                iStateReligion = pArabia.getStateReligion()
                if (iStateReligion >= 0):
                        if (not city.isHasReligion(iStateReligion)):
                                city.setHasReligion(iStateReligion, True, True, False)
                        if (not city.hasBuilding(iTemple + iStateReligion*4)):
                                city.setHasRealBuilding((iTemple + iStateReligion*4), True)
                        if (not city.hasBuilding(iCathedral + iStateReligion*4)):
                                city.setHasRealBuilding((iCathedral + iStateReligion*4), True)
                                        
                                    #converts other religions temples and cathedrals
##                                        for iReligionLoop in range(iNumReligions):
##                                                if (iReligionLoop != iStateReligion):
##                                                        if (city.hasBuilding(iTemple + iReligionLoop*4)):
##                                                                city.setHasRealBuilding((iTemple + iReligionLoop*4), False)
##                                                                if (not city.hasBuilding(iTemple + iStateReligion*4)):
##                                                                        city.setHasRealBuilding((iTemple + iStateReligion*4), True)
##                                                        if (city.hasBuilding(iCathedral + iReligionLoop*4)):
##                                                                city.setHasRealBuilding((iCathedral + iReligionLoop*4), False)
##                                                                if (not city.hasBuilding(iCathedral + iStateReligion*4)):
##                                                                        city.setHasRealBuilding((iCathedral + iStateReligion*4), True)

                        





#------------------AZTEC U.P.-------------------

        def aztecUP(self, argsList): #Real Slavery by Sevo
                pWinningUnit,pLosingUnit = argsList
                pWinningPlayer = gc.getPlayer(pWinningUnit.getOwner())
		
                if (pWinningPlayer.getID() != iAztecs):
                        return

                pLosingPlayer = gc.getPlayer(pLosingUnit.getOwner())
                cLosingUnit = PyHelpers.PyInfo.UnitInfo(pLosingUnit.getUnitType())
		
                if (pLosingUnit.getUnitType() < con.iWarrior):
                        return
		
                # Only enslave land units!!
                if (cLosingUnit.getDomainType() == gc.getInfoTypeForString("DOMAIN_LAND")):
                        iRandom = gc.getGame().getSorenRandNum(100, 'capture chance')
                        if (iRandom < 50):
                                pNewUnit = pWinningPlayer.initUnit(con.iWorker, pWinningUnit.getX(), pWinningUnit.getY(), UnitAITypes.UNITAI_WORKER, DirectionTypes.DIRECTION_SOUTH)
                                CyInterface().addMessage(pWinningPlayer.getID(),True,15,CyTranslator().getText("TXT_KEY_UP_ENSLAVE_WIN", ()),'SND_REVOLTEND',1,'Art/Interface/Buttons/units/worker.dds',ColorTypes(8),pWinningUnit.getX(),pWinningUnit.getY(),True,True)
                                CyInterface().addMessage(pLosingPlayer.getID(),True,15,CyTranslator().getText("TXT_KEY_UP_ENSLAVE_LOSE", ()),'SND_REVOLTEND',1,'Art/Interface/Buttons/units/worker.dds',ColorTypes(7),pWinningUnit.getX(),pWinningUnit.getY(),True,True)		
                                if (pLosingUnit.getOwner() in con.lCivGroups[0]):
                                        self.setEnslavedUnits(self.getEnslavedUnits() + 1)



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
##                                                                print("hp", unit.currHitPoints() )
##                                                                print("damage", unit.getDamage() )
                                                                unit.setDamage(unit.getDamage()+8, iRussia)
##                                                                print("hp now", unit.currHitPoints() 
##                                                                print("damage", unit.getDamage() )




#------------------TURKISH U.P.-------------------


        def turkishUP(self, city):
               
                for x in range(city.getX()-2, city.getX()+3):
                        for y in range(city.getY()-2, city.getY()+3):
                                pCurrent = gc.getMap().plot( x, y )
                                if (x == city.getX() and y == city.getY()):
                                        utils.convertPlotCulture(pCurrent, iTurkey, 51, False)
                                elif (pCurrent.isCity()):
                                        pass
                                elif (utils.calculateDistance(x, y, city.getX(), city.getY()) == 1):
                                        utils.convertPlotCulture(pCurrent, iTurkey, 80, True)
                                else:
                                        utils.convertPlotCulture(pCurrent, iTurkey, 20, False)


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
                
##                targetCity = -1
##                if (not pMongolia.isHuman()):
##                        for x in range(self.getLatestRazeData(3) -3, self.getLatestRazeData(3) +1 +3):
##                                for y in range(self.getLatestRazeData(4) -3, self.getLatestRazeData(4) +1 +3):
##                                        pCurrent = gc.getMap().plot( x, y )
##                                        if ( pCurrent.isCity()):
##                                                cityNear = pCurrent.getPlotCity()
##                                                iOwnerNear = cityNear.getOwner()
##                                                if (cityNear.getName() != city.getName()):
##                                                        print ("iOwnerNear", iOwnerNear, "citynear", cityNear.getName())
##                                                        if (iOwnerNear == iOldOwner):
##                                                                if (cityNear != city):
##                                                                        if (cityNear.getPopulation() <= self.getLatestRazeData(2)):
##                                                                                targetCity = cityNear
##                                                                                print ("targetCity", targetCity)
##                                                                                break
##                                                                                break
##                        if (targetCity != -1):
##                                targetPlot = -1
##                                for j in range(targetCity.getX() -1, targetCity.getX() +1 +2):
##                                        for k in range(targetCity.getY() -1, targetCity.getY() +1 +2):
##                                                pCurrentTarget = gc.getMap().plot( j, k )
##                                                if (pCurrentTarget.getNumUnits() == 0):
##                                                        iDistance = gc.getMap().calculatePathDistance(pCurrentTarget, pCity)
##                                                        if (iDistance <= 2):
##                                                                targetPlot = pCurrentTarget
##                                                                print ("pCurrentTarget", pCurrentTarget)
##                                                                break
##                                                                break
##                                for m in range(city.getX() -1, city.getX() +1 +2):
##                                        for n in range(city.getY() -1, city.getY() +1 +2):
##                                                pMongol = gc.getMap().plot( m, n )
##                                                if (pMongol.getNumUnits() > 0):
##                                                        print ("numunits>0")
##                                                        for i in range(pCity.getNumUnits()):
##                                                                unit = pCity.getUnit(i)
##                                                                if (unit.getOwner() == iMongolia):
##                                                                        #if (unit.getMoves() >= 2):
##                                                                        print ("unit", unit)
##                                                                        unit.setXY(targetPlot.getX(), targetPlot.getY())
##                                                                        break
##                                                                        break
##                                                                        break
                                


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
			utils.makeUnit(con.iMongolKeshik, iMongolia, (city.getX(), city.getY()), 2)
		elif (city.getPopulation() >= 4):
			utils.makeUnit(con.iMongolKeshik, iMongolia, (city.getX(), city.getY()), 1)

		CyInterface().addMessage(iMongolia, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_MONGOL_HORDE", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)


#------------------AMERICAN U.P.-------------------

        def americanUP(self):
##                popup = Popup.PyPopup() 
##                popup.setBodyString( 'Turnlength: %d' %(self.getImmigrationTurnLength()))
##                popup.launch()            
                if (self.getImmigrationTurnLength() == 0):
                        self.setImmigrationTurnLength( 3 + gc.getGame().getSorenRandNum(5, 'random') ) #3 to 7 turns
                iImmigrationCurrentTurn = self.getImmigrationCurrentTurn()
                self.setImmigrationCurrentTurn(iImmigrationCurrentTurn + 1)
                if (iImmigrationCurrentTurn <= self.getImmigrationTurnLength()):
                        self.doImmigration()
                if (iImmigrationCurrentTurn > self.getImmigrationTurnLength()):
                        self.setImmigrationTurnLength(0)
                        self.setImmigrationCurrentTurn(0)
                        


        def doImmigration(self):

                if (gc.getPlayer(iAmerica).getNumCities() > 0):
                        #select target city
                        targetCity = self.selectRandomCityTargetCiv(iAmerica)
                        
                        #select source city based on life expectancy and approval rate rank
                        iHappinessRank = 0
                        iHealthRank = 0
                        aiGroupHappiness = []
                        aiGroupHealth = []
                        for iPlayerLoop in range(iNumPlayers-1): #-1: no America
                                pCurrPlayer = gc.getPlayer(iPlayerLoop)
                                if (pCurrPlayer.isAlive() and iPlayerLoop != iAmerica and not pCurrPlayer.isBarbarian() ):
                                        if (gc.getPlayer(iPlayerLoop).canContact(iAmerica)):
                                                if (pCurrPlayer.calculateTotalCityHappiness() > 0):
                                                        aiGroupHappiness.append(int((1.0 * pCurrPlayer.calculateTotalCityHappiness()) / (pCurrPlayer.calculateTotalCityHappiness() \
                                                                + pCurrPlayer.calculateTotalCityUnhappiness()) * 100))
                                                else:
                                                        aiGroupHappiness.append(50)

                                                if (pCurrPlayer.calculateTotalCityHealthiness() > 0):
                                                        aiGroupHealth.append(int((1.0 * pCurrPlayer.calculateTotalCityHealthiness()) / (pCurrPlayer.calculateTotalCityHealthiness() \
                                                                + pCurrPlayer.calculateTotalCityUnhealthiness()) * 100))
                                                else:
                                                        aiGroupHealth.append(30)
                                        else:
                                                aiGroupHappiness.append(-1)
                                                aiGroupHealth.append(-1)
                                else:
                                        aiGroupHappiness.append(-1)
                                        aiGroupHealth.append(-1)

                        lTotalRanking = []
                        lTotalRanking.append((-2, -2)) #initialization
                        lTotalRanking.append((1000, -1000))
                        for iPlayer in range(iNumPlayers-1):
                                pCurrPlayer = gc.getPlayer(iPlayer)
                                if (aiGroupHappiness[iPlayer] >= 0):
                                        iFinal = aiGroupHappiness[iPlayer] + aiGroupHealth[iPlayer] + gc.getGame().getSorenRandNum(40, 'random')
                                        for iLoop in range(len(lTotalRanking)-1):
                                                if (iFinal >= lTotalRanking[iLoop][0] and iFinal <= lTotalRanking[iLoop+1][0]):
                                                        #print ("inserting", iFinal) 
                                                        #print ("inserting", iPlayer)
                                                        lTotalRanking.insert(iLoop+1, (iFinal, iPlayer))
                                                        break
                                                    
                        #print ("n.0: ", lTotalRanking[0][1])
                        #print ("n.1: ", lTotalRanking[1][1])
                        #print ("n.3: ", lTotalRanking[2][1])
                        #print ("len(lTotalRanking): ", len(lTotalRanking))     
                        
                        for iLoop in range(len(lTotalRanking)):
                                iPlayer = lTotalRanking[iLoop][1]
                                if (iPlayer >= 0 and iPlayer <= iNumPlayers-1):
                                        sourceCity = self.selectRandomCitySourceCiv(iPlayer)
                                        print ("immigrating from ", iPlayer)
                                        if ( sourceCity != False):
                                                sourceCity.changePopulation(-1)
                                                if (gc.getPlayer(iPlayer).isHuman()):
                                                        CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_EMIGRATION", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
                                                targetCity.changePopulation(1)
                                                targetPlot = gc.getMap().plot(targetCity.getX(), targetCity.getY())
                                                iCultureChange = targetPlot.getCulture(iAmerica)/targetCity.getPopulation()
                                                targetPlot.setCulture(iPlayer, iCultureChange, False)
                                                if (gc.getPlayer(iAmerica).isHuman()):
                                                        CyInterface().addMessage(iAmerica, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_IMMIGRATION", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
                                                return True

                                        
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
                if (gc.getPlayer(iCiv).isAlive()):
                        cityList = []
                        for pyCity in PyPlayer(iCiv).getCityList():
                                if (pyCity.GetCy()):
                                        if ( pyCity.GetCy().isDisorder() or pyCity.GetCy().foodDifference(False) < 0):
                                                return pyCity.GetCy()                            
                                cityList.append(pyCity.GetCy())
                        if (len(cityList)):
                                iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
                                return cityList[iCity]
                return False
                        
