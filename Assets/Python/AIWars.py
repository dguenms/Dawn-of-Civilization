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
iRomeGreeceYear = -150
iRomePersiaYear = -100
iRomeCeltiaYear = -50
iRomeEgyptYear = 0

iAlexanderYear = -340

iRome = con.iRome
iCarthage = con.iCarthage
iGreece = con.iGreece
iPersia = con.iPersia
iCeltia = con.iCeltia
iEgypt = con.iEgypt
iBabylonia = con.iBabylonia

  
class AIWars:

        def getAttackingCivsArray( self, iCiv ):
                return sd.scriptDict['lAttackingCivsArray'][iCiv]

        def setAttackingCivsArray( self, iCiv, iNewValue ):
                sd.scriptDict['lAttackingCivsArray'][iCiv] = iNewValue
                
        def getNextTurnAIWar( self ):
                return sd.scriptDict['iNextTurnAIWar']

        def setNextTurnAIWar( self, iNewValue ):
                sd.scriptDict['iNextTurnAIWar'] = iNewValue
		
	def getRomanWar(self, iPlayer):
		return sd.scriptDict['lRomanWars'][iPlayer]
		
	def setRomanWar(self, iPlayer, iNewValue):
		sd.scriptDict['lRomanWars'][iPlayer] = iNewValue

		
        def setup(self):
                iTurn = getTurnForYear(-600)
                if (not gc.getPlayer(0).isPlayable()):  #late start condition
                        iTurn = getTurnForYear(900)
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
		
		if utils.getHumanID() != iGreece and gc.getPlayer(iGreece).isAlive():
			if iGameTurn == getTurnForYear(iAlexanderYear) - 5 + (utils.getSeed() % 10):
				if gc.getPlayer(iBabylonia).isAlive():
					gc.getTeam(iGreece).declareWar(iBabylonia, True, WarPlanTypes.WARPLAN_TOTAL)
					up.greekConquestUP(iBabylonia, 2)
					
			if iGameTurn == getTurnForYear(iAlexanderYear) - 5 + (utils.getSeed() % 10):
				if gc.getPlayer(iEgypt).isAlive():
					gc.getTeam(iGreece).declareWar(iEgypt, True, WarPlanTypes.WARPLAN_TOTAL)
					up.greekConquestUP(iEgypt, 2)
					
			if iGameTurn == getTurnForYear(iAlexanderYear) - 5 + (utils.getSeed() % 10):
				if gc.getPlayer(iPersia).isAlive():
					gc.getTeam(iGreece).declareWar(iPersia, True, WarPlanTypes.WARPLAN_TOTAL)
					up.greekConquestUP(iPersia, 2)
		
		if utils.getHumanID() != iRome and gc.getPlayer(iRome).isAlive():
			if iGameTurn == getTurnForYear(iRomeCarthageYear) - 5 + (utils.getSeed() % 10):
				if self.getRomanWar(iCarthage) != 1 and gc.getPlayer(iCarthage).isAlive():
					gc.getTeam(iRome).declareWar(iCarthage, True, WarPlanTypes.WARPLAN_TOTAL)
					self.setRomanWar(iCarthage, 1)
					up.romanConquestUP(iCarthage, 2)
				
			if iGameTurn == getTurnForYear(iRomeGreeceYear) - 5 + (utils.getSeed() % 10):
				if self.getRomanWar(iGreece) != 1 and gc.getPlayer(iGreece).isAlive():
					gc.getTeam(iRome).declareWar(iGreece, True, WarPlanTypes.WARPLAN_TOTAL)
					self.setRomanWar(iGreece, 1)
					iExtra = 0
					if utils.getHumanID() != iGreece: iExtra = 1
					up.romanConquestUP(iGreece, 2+iExtra)
					
			if iGameTurn == getTurnForYear(iRomePersiaYear) - 5 + (utils.getSeed() % 10):
				if self.getRomanWar(iPersia) != 1 and gc.getPlayer(iPersia).isAlive():
					gc.getTeam(iRome).declareWar(iPersia, True, WarPlanTypes.WARPLAN_LIMITED)
					self.setRomanWar(iPersia, 1)
					up.romanConquestUP(iPersia, 2)
					
			if iGameTurn == getTurnForYear(iRomeCeltiaYear) - 5 + (utils.getSeed() % 10):
				if self.getRomanWar(iCeltia) != 1 and gc.getPlayer(iCeltia).isAlive():
					gc.getTeam(iRome).declareWar(iCeltia, True, WarPlanTypes.WARPLAN_TOTAL)
					self.setRomanWar(iCeltia, 1)
					up.romanConquestUP(iCeltia, 2)
					
			if iGameTurn == getTurnForYear(iRomeEgyptYear) - 5 + (utils.getSeed() % 10):
				if self.getRomanWar(iEgypt) != 1 and gc.getPlayer(iEgypt).isAlive():
					gc.getTeam(iEgypt).declareWar(iEgypt, True, WarPlanTypes.WARPLAN_TOTAL)
					self.setRomanWar(iEgypt, 1)
					up.romanConquestUP(iEgypt, 2)
                        
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
                        if (iLoopCiv == con.iNetherlands or iLoopCiv == con.iPortugal):
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


