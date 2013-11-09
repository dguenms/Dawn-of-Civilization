# Rhye's and Fall of Civilization - AI Wars

from CvPythonExtensions import *
import CvUtil
import PyHelpers        # LOQ
import Popup
#import cPickle as pickle
import Consts as con
import RFCUtils
import UniquePowers
from StoredData import sd # edead

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer	# LOQ
utils = RFCUtils.RFCUtils()
up = UniquePowers.UniquePowers()

### Constants ###


#iStartTurn = con.i600BC # moved to setup - edead
iMinIntervalEarly = 10
iMaxIntervalEarly = 20
iMinIntervalLate = 40
iMaxIntervalLate = 60
iThreshold = 100
iMinValue = 30
iNumPlayers = con.iNumMajorPlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iNumTotalPlayers = con.iNumTotalPlayers

iRomeCarthageYear = -220
tRomeCarthageTL = (53, 37)
tRomeCarthageBR = (61, 40)

iRomeGreeceYear = -150
tRomeGreeceTL = (64, 40)
tRomeGreeceBR = (68, 45)

iRomeMesopotamiaYear = -100
tRomeMesopotamiaTL = (70, 38)
tRomeMesopotamiaBR = (78, 45)

iRomeCeltiaYear = -50
tRomeCeltiaTL = (52, 45)
tRomeCeltiaBR = (59, 51)

iRomeEgyptYear = 0
tRomeEgyptTL = (65, 31)
tRomeEgyptBR = (72, 36)

iAlexanderYear = -340
tGreeceMesopotamiaTL = (70, 38)
tGreeceMesopotamiaBR = (78, 45)
tGreeceEgyptTL = (65, 31)
tGreeceEgyptBR = (72, 36)
tGreecePersiaTL = (79, 37)
tGreecePersiaBR = (85, 45)

iCholaSumatraYear = 1030
tCholaSumatraTL = (98, 26)
tCholaSumatraBR = (101, 28)

iSpainMoorsYear = 1200
tSpainMoorsTL = (50, 40)
tSpainMoorsBR = (54, 42)

iRome = con.iRome
iCarthage = con.iCarthage
iGreece = con.iGreece
iPersia = con.iPersia
iCeltia = con.iCeltia
iEgypt = con.iEgypt
iBabylonia = con.iBabylonia
iTamils = con.iTamils
iIndonesia = con.iIndonesia
iSpain = con.iSpain
iMoors = con.iMoors

  
class AIWars:

        def getAttackingCivsArray( self, iCiv ):
                return sd.scriptDict['lAttackingCivsArray'][iCiv]

        def setAttackingCivsArray( self, iCiv, iNewValue ):
                sd.scriptDict['lAttackingCivsArray'][iCiv] = iNewValue
                
        def getNextTurnAIWar( self ):
                return sd.scriptDict['iNextTurnAIWar']

        def setNextTurnAIWar( self, iNewValue ):
                sd.scriptDict['iNextTurnAIWar'] = iNewValue

		
        def setup(self):
                iTurn = getTurnForYear(-600)
                if utils.getScenario() == con.i600AD:  #late start condition
                        iTurn = getTurnForYear(900)
		elif utils.getScenario() == con.i1700AD:
			iTurn = getTurnForYear(1720)
                self.setNextTurnAIWar(iTurn + gc.getGame().getSorenRandNum(iMaxIntervalEarly-iMinIntervalEarly, 'random turn'))



        def checkTurn(self, iGameTurn):

		print "Check AI wars"

                #turn automatically peace on between independent cities and all the major civs
                if (iGameTurn % 20 == 7):
                        utils.restorePeaceHuman(con.iIndependent2, False)
                if (iGameTurn % 20 == 14):
                        utils.restorePeaceHuman(con.iIndependent, False)
                if (iGameTurn % 60 == 55 and iGameTurn > utils.getTurns(50)):
                        utils.restorePeaceAI(con.iIndependent, False)
                if (iGameTurn % 60 == 30 and iGameTurn > utils.getTurns(50)):
                        utils.restorePeaceAI(con.iIndependent2, False)
                #turn automatically war on between independent cities and some AI major civs
                if (iGameTurn % 13 == 6 and iGameTurn > utils.getTurns(50)): #1 turn after restorePeace()
                        utils.minorWars(con.iIndependent)
                if (iGameTurn % 13 == 11 and iGameTurn > utils.getTurns(50)): #1 turn after restorePeace()
                        utils.minorWars(con.iIndependent2)
                if (iGameTurn % 50 == 24 and iGameTurn > utils.getTurns(50)):
                        utils.minorWars(con.iCeltia)
			utils.minorWars(con.iSeljuks)
			
		self.spawnConquerors(iGreece, iBabylonia, tGreeceMesopotamiaTL, tGreeceMesopotamiaBR, 2, iAlexanderYear, 10)
		self.spawnConquerors(iGreece, iEgypt, tGreeceEgyptTL, tGreeceEgyptBR, 2, iAlexanderYear, 10)
		self.spawnConquerors(iGreece, iPersia, tGreecePersiaTL, tGreecePersiaBR, 2, iAlexanderYear, 10)
		
		self.spawnConquerors(iRome, iCarthage, tRomeCarthageTL, tRomeCarthageBR, 2, iRomeCarthageYear, 10)
		self.spawnConquerors(iRome, iGreece, tRomeGreeceTL, tRomeGreeceBR, 2, iRomeGreeceYear, 10)
		self.spawnConquerors(iRome, iPersia, tRomeMesopotamiaTL, tRomeMesopotamiaBR, 2, iRomeMesopotamiaYear, 10)
		self.spawnConquerors(iRome, iCeltia, tRomeCeltiaTL, tRomeCeltiaBR, 2, iRomeCeltiaYear, 10)
		self.spawnConquerors(iRome, iEgypt, tRomeEgyptTL, tRomeEgyptBR, 2, iRomeEgyptYear, 10)

		self.spawnConquerors(iTamils, iIndonesia, tCholaSumatraTL, tCholaSumatraBR, 1, iCholaSumatraYear, 10)
		
		self.spawnConquerors(iSpain, iMoors, tSpainMoorsTL, tSpainMoorsBR, 0, iSpainMoorsYear, 10)
                        
                if (iGameTurn == getTurnForYear(1500) or iGameTurn == getTurnForYear(1850)):
                        for iLoopCiv in range( iNumPlayers ):
                                self.setAttackingCivsArray(iLoopCiv, max(0,self.getAttackingCivsArray(iLoopCiv) - con.tAggressionLevel[iLoopCiv])) 

                     
                if (iGameTurn == self.getNextTurnAIWar()):
                    
                        if (iGameTurn > getTurnForYear(1600)): #longer periods due to globalization of contacts
                                iMinInterval = iMinIntervalLate
                                iMaxInterval = iMaxIntervalLate
                        else:
                                iMinInterval = iMinIntervalEarly
                                iMaxInterval = iMaxIntervalEarly
                        
                        # game speed factor - edead
                        iMinInterval = utils.getTurns(iMinInterval)
                        iMaxInterval = utils.getTurns(iMaxInterval)

                        #skip if in a world war already
                        if (iGameTurn > getTurnForYear(1500)):
                                numCivsAtWar = 0
                                gc.getGame().countCivPlayersAlive()
                                for iLoopCiv in range( iNumPlayers ):
                                        tLoopCiv = gc.getTeam(gc.getPlayer(iLoopCiv).getTeam())
                                        if (tLoopCiv.getAtWarCount(True) != 0):
                                                numCivsAtWar += 1
                                if (numCivsAtWar*100/gc.getGame().countCivPlayersAlive() > 50): #more than half at war with someone
                                        print("Skipping AIWar (WW)")
                                        self.setNextTurnAIWar(iGameTurn + iMinInterval + gc.getGame().getSorenRandNum(iMaxInterval-iMinInterval, 'random turn'))
                                        return
                            
                        iCiv, iTargetCiv = self.pickCivs()
                        if (iTargetCiv >= 0 and iTargetCiv <= iNumTotalPlayers):
                                self.initWar(iCiv, iTargetCiv, iGameTurn, iMaxInterval, iMinInterval)
                                return
                        else:
                                print ("AIWars iTargetCiv missing", iCiv)
                                iCiv, iTargetCiv = self.pickCivs()
                                if (iTargetCiv >= 0 and iTargetCiv <= iNumTotalPlayers):
                                        self.initWar(iCiv, iTargetCiv, iGameTurn, iMaxInterval, iMinInterval)
                                        return
                                else:
                                        print ("AIWars iTargetCiv missing again", iCiv)

                        #make sure we don't miss this
                        print("Skipping AIWar")
                        self.setNextTurnAIWar(iGameTurn + iMinInterval + gc.getGame().getSorenRandNum(iMaxInterval-iMinInterval, 'random turn'))
			
	def spawnConquerors(self, iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns, iWarPlan = WarPlanTypes.WARPLAN_TOTAL):
	
		if utils.getHumanID() == iPlayer:
			return
			
		if not gc.getPlayer(iPlayer).isAlive():
			return
	
		if gc.getGame().getGameTurn() != getTurnForYear(iYear) - iIntervalTurns/2 + (utils.getSeed() % iIntervalTurns):
			return
			
		lCities = []
		for city in utils.getAreaCities(tTL, tBR):
			if city.getOwner() != iPlayer and not gc.getTeam(city.getOwner()).isVassal(iPlayer):
				lCities.append(city)
				
		capital = gc.getPlayer(iPlayer).getCapitalCity()
		
		lTargetCities = []
		for i in range(iNumTargets):
			if len(lCities) == 0: break
			
			targetCity = utils.getHighestEntry(lCities, lambda x: -utils.calculateDistance(x.getX(), x.getY(), capital.getX(), capital.getY()) + int(x.getOwner() == iPreferredTarget) * 1000)
			lTargetCities.append(targetCity)
			lCities.remove(targetCity)
			
		lOwners = []
		for city in lTargetCities:
			if city.getOwner() not in lOwners:
				lOwners.append(city.getOwner())
				
		if iPreferredTarget not in lOwners and gc.getPlayer(iPreferredTarget).isAlive():
			gc.getTeam(iPlayer).declareWar(iPreferredTarget, True, iWarPlan)
				
		for iOwner in lOwners:
			gc.getTeam(iPlayer).declareWar(iOwner, True, iWarPlan)
			CyInterface().addMessage(iOwner, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_CONQUESTS_TARGET", (gc.getPlayer(iOwner).getCivilizationShortDescription(0),)), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
			
		for city in lTargetCities:
			iExtra = 0
			if utils.getHumanID() not in [iPlayer, city.getOwner()]: iExtra = 1
			
			tPlot = utils.findNearestLandPlot((city.getX(), city.getY()), iPlayer)
			
			iBestInfantry = utils.getBestInfantry(iPlayer)
			iBestSiege = utils.getBestSiege(iPlayer)
			
			if iPlayer == con.iGreece:
				iBestInfantry = con.iGreekPhalanx
				iBestSiege = con.iCatapult
			
			utils.makeUnitAI(iBestInfantry, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 + iExtra)
			utils.makeUnitAI(iBestSiege, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1 + 2*iExtra)
			
			if iPlayer == con.iTamils:
				utils.makeUnitAI(con.iWarElephant, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
				
			
        def pickCivs(self): 
                iCiv = -1
                iTargetCiv = -1
                iCiv = self.chooseAttackingPlayer()
                if (iCiv >= 0 and iCiv <= iNumPlayers):
                        iTargetCiv = self.checkGrid(iCiv)
                        return (iCiv, iTargetCiv)
                else:
                        print ("AIWars iCiv missing", iCiv)
                        return (-1, -1)

        def initWar(self, iCiv, iTargetCiv, iGameTurn, iMaxInterval, iMinInterval):
		gc.getTeam(iCiv).declareWar(iTargetCiv, True, -1) ##False?
                self.setNextTurnAIWar(iGameTurn + iMinInterval + gc.getGame().getSorenRandNum(iMaxInterval-iMinInterval, 'random turn'))
                print("Setting AIWar", iCiv, "attacking", iTargetCiv)

##        def initArray(self):
##                for k in range( iNumPlayers ):
##                        grid = []                
##                        for j in range( 68 ):
##                                line = []
##                                for i in range( 124 ):        
##                                        line.append( gc.getPlayer(iCiv).getSettlersMaps( 67-j, i ) )
##                                grid.append( line )
##                        self.lSettlersMap.append( grid )
##                print self.lSettlersMap




        def chooseAttackingPlayer(self): 
                #finding max teams ever alive (countCivTeamsEverAlive() doesn't work as late human starting civ gets killed every turn)
                iMaxCivs = iNumPlayers
                for i in range( iNumPlayers ):
                        j = iNumPlayers -1 - i
                        if (gc.getPlayer(j).isAlive()):
                                iMaxCivs = j
                                break 
                #print ("iMaxCivs", iMaxCivs)
                
                if (gc.getGame().countCivPlayersAlive() <= 2):
                        return -1
                else:
                        iRndnum = gc.getGame().getSorenRandNum(iMaxCivs, 'attacking civ index') 
                        #print ("iRndnum", iRndnum)
                        iAlreadyAttacked = -100
                        iMin = 100
                        iCiv = -1
                        for i in range( iRndnum, iRndnum + iMaxCivs ):
                                iLoopCiv = i % iMaxCivs
                                if (gc.getPlayer(iLoopCiv).isAlive() and not gc.getPlayer(iLoopCiv).isHuman()):
                                        if (utils.getPlagueCountdown(iLoopCiv) >= -10 and utils.getPlagueCountdown(iLoopCiv) <= 0): #civ is not under plague or quit recently from it
                                                iAlreadyAttacked = self.getAttackingCivsArray(iLoopCiv)
                                                if (utils.isAVassal(iLoopCiv)):
                                                        iAlreadyAttacked += 1 #less likely to attack
                                                if (iLoopCiv == con.iPortugal or iLoopCiv == con.iNetherlands):
                                                        iAlreadyAttacked += 1 #less likely to attack, would cripple them
                                                #check if a world war is already in place
                                                iNumAlreadyWar = 0
                                                tLoopCiv = gc.getTeam(gc.getPlayer(iLoopCiv).getTeam())
                                                for kLoopCiv in range( iNumPlayers ):
                                                        if (tLoopCiv.isAtWar(kLoopCiv)):
                                                                iNumAlreadyWar += 1
                                                if (iNumAlreadyWar >= 5):
                                                        iAlreadyAttacked += 2 #much less likely to attack
                                                elif (iNumAlreadyWar >= 3):
                                                        iAlreadyAttacked += 1 #less likely to attack
                                                            
                                                if (iAlreadyAttacked < iMin):
                                                        iMin = iAlreadyAttacked
                                                        iCiv = iLoopCiv
                        #print ("attacking civ", iCiv)
                        if (iAlreadyAttacked != -100):
                                self.setAttackingCivsArray(iCiv, iAlreadyAttacked + 1)                        
                                return iCiv
                        else:
                                return -1
                return -1
                    
             

        def checkGrid(self, iCiv):
                pCiv = gc.getPlayer(iCiv)
                tCiv = gc.getTeam(pCiv.getTeam())
                lTargetCivs = []
                #lTargetCivs = con.l0ArrayTotal

                #clean it, sometimes it takes old values in memory
                for k in range( iNumTotalPlayers ):
                        lTargetCivs.append(0)
                        #lTargetCivs[k] = 0

                ##set alive civs to 1 to differentiate them from dead civs
                for k in range( iNumPlayers ):
                        if (gc.getPlayer(k).isAlive() and tCiv.isHasMet(k)): #canContact here?
                                if (lTargetCivs[k] == 0):
                                        lTargetCivs[k] = 1
                for k in range( iNumTotalPlayers ):
                        if (k >= iNumPlayers):
                                if (gc.getPlayer(k).isAlive() and tCiv.isHasMet(k)):
                                        lTargetCivs[k] = 1

                ##set master or vassal to 0
                for k in range( iNumPlayers ):                                
                        if (gc.getTeam(gc.getPlayer(k).getTeam()).isVassal(iCiv) or tCiv.isVassal(k)):
                                 lTargetCivs[k] = 0

                #if already at war
                for k in range( iNumTotalPlayers ): 
                        if (tCiv.isAtWar(k)):
                                lTargetCivs[k] = 0

                lTargetCivs[iCiv] = 0
                                
                for j in range( 68 ): 
                        for i in range( 124 ):                                      
                                iOwner = gc.getMap().plot( i, j ).getOwner()
                                if (iOwner >= 0 and iOwner < iNumTotalPlayers and iOwner != iCiv):
                                        if (lTargetCivs[iOwner] > 0):
                                                lTargetCivs[iOwner] += gc.getPlayer(iCiv).getWarMapValue(i, j)
                                                
                #there are other routines for this
                lTargetCivs[iIndependent] /= 3
                lTargetCivs[iIndependent2] /= 3

                #can they attack civs with lost contact?
                for k in range( iNumPlayers ): 
                        if (not pCiv.canContact(k)):
                                lTargetCivs[k] /= 8

                #print(lTargetCivs)
                
                #normalization
                iMaxTempValue = -1
                for k in range( iNumTotalPlayers ):
                        if (lTargetCivs[k] > iMaxTempValue):
                                iMaxTempValue = lTargetCivs[k]
                #print(iMaxTempValue)
                if (iMaxTempValue > 0):
                        for k in range( iNumTotalPlayers ):
                                if (lTargetCivs[k] > 0):
                                        #lTargetCivs[k] *= 500 #non va!
                                        #lTargetCivs[k] / iMaxTempValue
                                        lTargetCivs[k] = lTargetCivs[k]*500/iMaxTempValue
                                        
                #print(lTargetCivs)
                
                for iLoopCiv in range( iNumTotalPlayers ):

                        if (lTargetCivs[iLoopCiv] <= 0):
                                continue
                            
                        #add a random value
                        if (lTargetCivs[iLoopCiv] <= iThreshold):
                                lTargetCivs[iLoopCiv] += gc.getGame().getSorenRandNum(100, 'random modifier')
                        if (lTargetCivs[iLoopCiv] > iThreshold):
                                lTargetCivs[iLoopCiv] += gc.getGame().getSorenRandNum(300, 'random modifier')
                        #balanced with attitude
                        attitude = 2*(pCiv.AI_getAttitude(iLoopCiv) - 2)
                        if (attitude > 0):
                                lTargetCivs[iLoopCiv] /= attitude
                        #exploit plague
                        if (utils.getPlagueCountdown(iLoopCiv) > 0 or utils.getPlagueCountdown(iLoopCiv) < -10 and not (gc.getGame().getGameTurn() <= getTurnForYear(con.tBirth[iLoopCiv]) + utils.getTurns(20))):
                                lTargetCivs[iLoopCiv] *= 3
                                lTargetCivs[iLoopCiv] /= 2

                        #balanced with master's attitude
                        for j in range( iNumTotalPlayers ):
                                if (tCiv.isVassal(j)):
                                        attitude = 2*(gc.getPlayer(j).AI_getAttitude(iLoopCiv) - 2)
                                        if (attitude > 0):
                                                lTargetCivs[iLoopCiv] /= attitude

                        #if already at war 
                        if (not tCiv.isAtWar(iLoopCiv)):
                                #consider peace counter
                                iCounter = min(7,max(1,tCiv.AI_getAtPeaceCounter(iLoopCiv)))
                                if (iCounter <= 7):
                                        lTargetCivs[iLoopCiv] *= 20 + 10*iCounter
                                        lTargetCivs[iLoopCiv] /= 100
                                        
                        #if under pact
                        if (tCiv.isDefensivePact(iLoopCiv)):
                                lTargetCivs[iLoopCiv] /= 4
                        #if friend of a friend
##                        for jLoopCiv in range( iNumTotalPlayers ):
##                                if (tCiv.isDefensivePact(jLoopCiv) and gc.getTeam(gc.getPlayer(iLoopCiv).getTeam()).isDefensivePact(jLoopCiv)):
##                                        lTargetCivs[iLoopCiv] /= 2
                                
                        #spare them
                        if (iLoopCiv == con.iNetherlands or iLoopCiv == con.iPortugal or iLoopCiv == con.iItaly):
                                lTargetCivs[iLoopCiv] *= 4
                                lTargetCivs[iLoopCiv] /= 5
                        #no suicide
                        if (iCiv == con.iNetherlands):
                                if (iLoopCiv == con.iFrance or iLoopCiv == con.iGermany):
                                        lTargetCivs[iLoopCiv] *= 1
                                        lTargetCivs[iLoopCiv] /= 2
                        if (iCiv == con.iPortugal):
                                if (iLoopCiv == con.iSpain):
                                        lTargetCivs[iLoopCiv] *= 1
                                        lTargetCivs[iLoopCiv] /= 2
			if (iCiv == con.iItaly):
				if (iLoopCiv == con.iGermany or iLoopCiv == con.iFrance):
					lTargetCivs[iLoopCiv] /= 2
                                
                                
                #print(lTargetCivs)
                
                #find max
                iMaxValue = 0
                iTargetCiv = -1
                for iLoopCiv in range( iNumTotalPlayers ):
                        if (lTargetCivs[iLoopCiv] > iMaxValue):
                                iMaxValue = lTargetCivs[iLoopCiv]
                                iTargetCiv = iLoopCiv

                #print ("maxvalue", iMaxValue)
                #print("target civ", iTargetCiv)

                if (iMaxValue >= iMinValue):
                        return iTargetCiv
                return -1

                                        
	    
        def forgetMemory(self, iTech, iPlayer):
                if (iTech == con.iCommunism or iTech == con.iMassMedia):
                        for iLoopCiv in range( iNumPlayers ):
                                pPlayer = gc.getPlayer(iPlayer)
                                if (pPlayer.AI_getMemoryCount(iLoopCiv,0) > 0):
                                        pPlayer.AI_changeMemoryCount(iLoopCiv,0,-1)
                                if (pPlayer.AI_getMemoryCount(iLoopCiv,1) > 0):
                                        pPlayer.AI_changeMemoryCount(iLoopCiv,1,-1)
					
	def planWars(self, iGameTurn):
		iAttackingPlayer = self.determineAttackingPlayer()
		iTargetPlayer = self.determineTargetPlayer(iAttackingPlayer)
		
	def determineAttackingPlayer(self):
		lAggressionLevels = sd.getAggressionLevels()
		iHighestEntry = utils.getHighestEntry(lAggressionLevels)
		
		return lAggressionLevels.index(iHighestEntry)
		
	def determineTargetPlayer(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		tPlayer = gc.getTeam(pPlayer.getTeam())
		lPotentialTargets = []
		lTargetValues = [0 for i in range(con.iNumPlayers)]

		# determine potential targets
		for iLoopPlayer in range(con.iNumPlayers):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			tLoopPlayer = gc.getTeam(pLoopPlayer.getTeam())
			
			# requires live civ and past contact
			if not pLoopPlayer.isAlive(): continue
			if not tPlayer.isHasMet(iLoopPlayer): continue
			
			# no masters or vassals
			if tPlayer.isVassal(iLoopPlayer): continue
			if tLoopPlayer.isVassal(iPlayer): continue
			
			# not already at war
			if tPlayer.isAtWar(iLoopPlayer): continue
			
			lPotentialTargets.append(iLoopPlayer)
			
		# iterate the map for all potential targets
		for i in range(124):
			for j in range(68):
				iOwner = gc.getMap().plot(i,j).getOwner()
				if iOwner in lPotentialTargets:
					lTargetValues[iOwner] += pPlayer.getWarMapValue(i, j)
					
		# hard to attack with lost contact
		for iLoopPlayer in lPotentialTargets:
			lTargetValues[iLoopPlayer] /= 8
			
			