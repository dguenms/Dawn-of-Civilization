# Rhye's and Fall of Civilization - Historical Victory Goals


from CvPythonExtensions import *
import time # Leoreth: benchmarking
import CvUtil
import PyHelpers   
import Popup
#import cPickle as pickle
from StoredData import sd # edead
import Consts as con
import RFCUtils
from operator import itemgetter
utils = RFCUtils.RFCUtils()

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

iNumPlayers = con.iNumPlayers
iNumMajorPlayers = con.iNumMajorPlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iNumTotalPlayers = con.iNumTotalPlayers
iBarbarian = con.iBarbarian
tCapitals = con.tCapitals

iParCities3 = con.iParCities3
iParCitiesE = con.iParCitiesE
iParCivics3 = con.iParCivics3
iParCivics1 = con.iParCivics1
iParCivicsE = con.iParCivicsE
iParDiplomacy3 = con.iParDiplomacy3
iParDiplomacyE = con.iParDiplomacyE
iParEconomy3 = con.iParEconomy3
iParEconomy1 = con.iParEconomy1
iParEconomyE = con.iParEconomyE
iParExpansion3 = con.iParExpansion3
iParExpansion1 = con.iParExpansion1
iParExpansionE = con.iParExpansionE



class Stability:



     
##################################################
### Secure storage & retrieval of script data ###
################################################   
		           


        def getBaseStabilityLastTurn( self, iCiv ):
                return sd.scriptDict['lBaseStabilityLastTurn'][iCiv]

        def setBaseStabilityLastTurn( self, iCiv, iNewValue ):
                sd.scriptDict['lBaseStabilityLastTurn'][iCiv] = iNewValue
            
        def getStability( self, iCiv ):
                return sd.scriptDict['lStability'][iCiv]

        def setStability( self, iCiv, iNewValue ):
                sd.scriptDict['lStability'][iCiv] = iNewValue

        def getStatePropertyCountdown( self, iCiv ):
                return sd.scriptDict['lStatePropertyCountdown'][iCiv]

        def setStatePropertyCountdown( self, iCiv, iNewValue ):
                sd.scriptDict['lStatePropertyCountdown'][iCiv] = iNewValue

        def getDemocracyCountdown( self, iCiv ):
                return sd.scriptDict['lDemocracyCountdown'][iCiv]

        def setDemocracyCountdown( self, iCiv, iNewValue ):
                sd.scriptDict['lDemocracyCountdown'][iCiv] = iNewValue
                
        def getGreatDepressionCountdown( self, iCiv ):
                return sd.scriptDict['lGreatDepressionCountdown'][iCiv]

        def setGreatDepressionCountdown( self, iCiv, iNewValue ):
                sd.scriptDict['lGreatDepressionCountdown'][iCiv] = iNewValue

        def getCombatResultTempModifier( self, iCiv ):
                return sd.scriptDict['lCombatResultTempModifier'][iCiv]

        def setCombatResultTempModifier( self, iCiv, iNewValue ):
                sd.scriptDict['lCombatResultTempModifier'][iCiv] = iNewValue

        def getGNPold( self, iCiv ):
                return sd.scriptDict['lGNPold'][iCiv]

        def setGNPold( self, iCiv, iNewValue ):
                sd.scriptDict['lGNPold'][iCiv] = iNewValue

        def getGNPnew( self, iCiv ):
                return sd.scriptDict['lGNPnew'][iCiv]

        def setGNPnew( self, iCiv, iNewValue ):
                sd.scriptDict['lGNPnew'][iCiv] = iNewValue

        def getRebelCiv( self ):
                return sd.scriptDict['iRebelCiv']

        def getLatestRebellionTurn( self, iCiv ):
		return gc.getPlayer(iCiv).getLatestRebellionTurn()

        def getPartialBaseStability( self, iCiv ):
                return sd.scriptDict['lPartialBaseStability'][iCiv]

        def setPartialBaseStability( self, iCiv, iNewValue ):
                sd.scriptDict['lPartialBaseStability'][iCiv] = iNewValue

        def getOwnedPlotsLastTurn( self, iCiv ):
                return sd.scriptDict['lOwnedPlotsLastTurn'][iCiv]

        def setOwnedPlotsLastTurn( self, iCiv, iNewValue ):
                sd.scriptDict['lOwnedPlotsLastTurn'][iCiv] = iNewValue
		
        def getOwnedOuterPlotsLastTurn( self, iCiv ):
                return sd.scriptDict['lOwnedOuterPlotsLastTurn'][iCiv]

        def setOwnedOuterPlotsLastTurn( self, iCiv, iNewValue ):
                sd.scriptDict['lOwnedOuterPlotsLastTurn'][iCiv] = iNewValue
		
        def getOwnedForeignCitiesLastTurn( self, iCiv ):
                return sd.scriptDict['lOwnedForeignCitiesLastTurn'][iCiv]

        def setOwnedForeignCitiesLastTurn( self, iCiv, iNewValue ):
                sd.scriptDict['lOwnedForeignCitiesLastTurn'][iCiv] = iNewValue

        def getOwnedCitiesLastTurn( self, iCiv ):
                return sd.scriptDict['lOwnedCitiesLastTurn'][iCiv]

        def setOwnedCitiesLastTurn( self, iCiv, iNewValue ):
                sd.scriptDict['lOwnedCitiesLastTurn'][iCiv] = iNewValue
                
        def getStabilityParameters( self, iParameter ):
                return sd.scriptDict['lStabilityParameters'][iParameter]

        def setStabilityParameters( self, iParameter, iNewValue ):
                sd.scriptDict['lStabilityParameters'][iParameter] = iNewValue
                
        def getLastRecordedStabilityStuff( self, iParameter ):
                return sd.scriptDict['lLastRecordedStabilityStuff'][iParameter]

        def setLastRecordedStabilityStuff( self, iParameter, iNewValue ):
                sd.scriptDict['lLastRecordedStabilityStuff'][iParameter] = iNewValue
                
#######################################
### Main methods (Event-Triggered) ###
#####################################  

        def setParameter(self, iPlayer, iParameter, bPreviousAmount, iAmount):
            if (gc.getPlayer(iPlayer).isHuman()):
            #if (iPlayer == con.iChina): #debug
                    if (bPreviousAmount):
                            self.setStabilityParameters(iParameter, self.getStabilityParameters(iParameter) + iAmount)
                    else:
                            self.setStabilityParameters(iParameter, 0 + iAmount)

        def setup(self):

                utils.setStartingStabilityParameters(utils.getHumanID())





        def checkTurn(self, iGameTurn):


                #moved here with its own stored value to save loading time (scrolls the map only once instead of every player)
                if (iGameTurn % utils.getTurns(6) == 0): #3 is too short to detect any change; must be a multiple of 3 anyway
                        lOwnedPlots = []
			lOwnedOuterPlots = []
			lOwnedForeignCities = []
                        lOwnedCities = []
                        for i in range(len(con.l0Array)):
                                lOwnedPlots.append(0)
				lOwnedOuterPlots.append(0)
				lOwnedForeignCities.append(0)
                                lOwnedCities.append(0)
                        for x in range(0, 123):
                                for y in range(0, 67):
                                        pCurrent = gc.getMap().plot( x, y )
                                        iOwner = pCurrent.getOwner()
                                        if (iOwner >= 0 and iOwner < iNumPlayers and (pCurrent.isHills() or pCurrent.isFlatlands())):
                                                if (gc.getPlayer(iOwner).getSettlersMaps( 67-y, x ) < 90):
							if pCurrent.isCityRadius():
								lOwnedPlots[iOwner] += 1
							else:
								lOwnedOuterPlots[iOwner] += 1
							if pCurrent.isCity():
								lOwnedForeignCities[iOwner] += 1
                                                if (pCurrent.isCity()):
                                                        cityOwner = pCurrent.getPlotCity().getOwner()
                                                        for iLoop in range(con.iNumPlayers):
                                                                if (iLoop != cityOwner and gc.getPlayer(iLoop).isAlive() and iGameTurn >= getTurnForYear(con.tBirth[iLoop])+utils.getTurns(30) and iGameTurn >= self.getLatestRebellionTurn(iLoop) + utils.getTurns(15)):
                                                                        if (gc.getPlayer(iLoop).getSettlersMaps( 67-y, x ) >= 400):
										reborn = utils.getReborn(iLoop)
                                                                                if (x >= con.tNormalAreasTL[reborn][iLoop][0] and x <= con.tNormalAreasBR[reborn][iLoop][0] and \
                                                                                    y >= con.tNormalAreasTL[reborn][iLoop][1] and y <= con.tNormalAreasBR[reborn][iLoop][1]):
                                                                                            if ((x,y) not in con.tNormalAreasSubtract[reborn][iLoop]):
                                                                                                    lOwnedCities[iLoop] += 1
                                                                if (iLoop == con.iAmerica):
                                                                        if (lOwnedCities[iLoop] >= 2):
                                                                                lOwnedCities[iLoop] -= 2 #their normal area is too large
                        for iLoopCiv in range(iNumPlayers):
                                self.setOwnedPlotsLastTurn(iLoopCiv, lOwnedPlots[iLoopCiv])
				self.setOwnedOuterPlotsLastTurn(iLoopCiv, lOwnedOuterPlots[iLoopCiv])
				self.setOwnedForeignCitiesLastTurn(iLoopCiv, lOwnedForeignCities[iLoopCiv])
                                self.setOwnedCitiesLastTurn(iLoopCiv, lOwnedCities[iLoopCiv])

                        #for up/down arrows
                        if (iGameTurn % utils.getTurns(3) == 0 and gc.getActivePlayer().getNumCities() > 0):  #numcities required to test autoplay with minor civs
                                self.setLastRecordedStabilityStuff(0, self.getStability(utils.getHumanID()))
                                self.setLastRecordedStabilityStuff(1, utils.getParCities())
                                self.setLastRecordedStabilityStuff(2, utils.getParCivics())
                                self.setLastRecordedStabilityStuff(3, utils.getParEconomy())
                                self.setLastRecordedStabilityStuff(4, utils.getParExpansion())
                                self.setLastRecordedStabilityStuff(5, utils.getParDiplomacy())
                            

                        
                for iPlayer in range(iNumPlayers):
                        
                        if (gc.getPlayer(iPlayer).isAlive()):
                                iTempNormalizationThreshold = self.getStability(iPlayer)

                                if (iGameTurn > getTurnForYear(1760) and iGameTurn % utils.getTurns(12) == 7):
                                        if (self.getStability(iPlayer) < 40):
                                                self.setStability(iPlayer, self.getStability(iPlayer) + 1 )
						gc.getPlayer(iPlayer).changeStability(1) # test DLL
                                elif (iGameTurn > getTurnForYear(-1000) and iGameTurn % utils.getTurns(22) == 7):
                                        if (self.getStability(iPlayer) < 20 and self.getStability(iPlayer) >= -50):
                                                self.setStability(iPlayer, self.getStability(iPlayer) + 1 )
						gc.getPlayer(iPlayer).changeStability(1) # test DLL
                                if (iGameTurn % utils.getTurns(10) == 8):
                                        if (self.getStability(iPlayer) < -50):
                                                self.setStability(iPlayer, self.getStability(iPlayer) + 1 )
						gc.getPlayer(iPlayer).changeStability(1) # test DLL
                                if (iGameTurn % utils.getTurns(10) == 9):
                                        if (self.getStability(iPlayer) > 50):
                                                self.setStability(iPlayer, self.getStability(iPlayer) - 1 )
						gc.getPlayer(iPlayer).changeStability(-1) # test DLL
                                if (iGameTurn > getTurnForYear(-1000) and iGameTurn % utils.getTurns(12) == 5):
                                        iPermanentModifier = self.getStability(iPlayer) - self.getBaseStabilityLastTurn(iPlayer)
                                        if (iPermanentModifier > 15):
                                                self.setStability(iPlayer, self.getStability(iPlayer) - 1 )
						gc.getPlayer(iPlayer).changeStability(-1) # test DLL
                                        elif (iPermanentModifier < -40):
                                                self.setStability(iPlayer, self.getStability(iPlayer) + 1 )
						gc.getPlayer(iPlayer).changeStability(1) # test DLL
                                if (iGameTurn % utils.getTurns(20) == 1):
                                        if (gc.getPlayer(iPlayer).isHuman()):
                                                iHandicap = (gc.getGame().getHandicapType() - 1)
                                                self.setStability(iPlayer, self.getStability(iPlayer) + iHandicap )
						gc.getPlayer(iPlayer).changeStability(iHandicap) # test DLL
                                
                                #print("stability wave", self.getStability(iPlayer) - iTempNormalizationThreshold)
                                self.setParameter(iPlayer, iParDiplomacyE, True, self.getStability(iPlayer) - iTempNormalizationThreshold)



                if (((iGameTurn > getTurnForYear(-600) and gc.getPlayer(0).isPlayable()) or (iGameTurn > getTurnForYear(600)+utils.getTurns(20) and not gc.getPlayer(0).isPlayable())) and iGameTurn % utils.getTurns(20) == 15): #late start condition
                #if (iGameTurn > 0): #debug
                        self.continentsNormalization(iGameTurn)
                        self.normalization(iGameTurn)
                        #debug
                        print ("Stability after normalization")
                        for iCiv in range(iNumPlayers):
                                if (gc.getPlayer(iCiv).isAlive()):
                                        print ("Base:", self.getBaseStabilityLastTurn(iCiv), "Modifier:", self.getStability(iCiv)-self.getBaseStabilityLastTurn(iCiv), "Total:", self.getStability(iCiv), "civic", gc.getPlayer(iCiv).getCivics(5), gc.getPlayer(iCiv).getCivilizationShortDescription(0))
                                else:
                                        print ("dead", iCiv)


        def continentsNormalization(self, iGameTurn):
                lContinentModifier = [0, 2, 0, -2, 0] #Eur, Far east, M. East, Med/Afr, Ame
                for iPlayer in range(iNumPlayers):
                        if (gc.getPlayer(iPlayer).isAlive()):
                                iTempNormalizationThreshold = self.getStability(iPlayer)
                                for j in range(len(con.lCivStabilityGroups)):
                                        if (iPlayer in con.lCivStabilityGroups[j]):
                                                self.setStability(iPlayer, (self.getStability(iPlayer) + lContinentModifier[j]))
						gc.getPlayer(iPlayer).changeStability(lContinentModifier[j]) # test DLL
                                self.setParameter(iPlayer, iParDiplomacyE, True, self.getStability(iPlayer) - iTempNormalizationThreshold)


        def normalization(self, iGameTurn):
                iMean = 0
                iTotal = 0
                iStandardMean = 3
                iSigma = 0
                iMinSigma = 7 + (iGameTurn - utils.getTurns(100))/utils.getTurns(50)
                iMaxSigma = 15 + (iGameTurn - utils.getTurns(100))/utils.getTurns(50)
                iStandardSigma = 11 + (iGameTurn - utils.getTurns(100))/utils.getTurns(50)
                iNumAlive = 0
                for iPlayer in range(iNumPlayers):
                        if (gc.getPlayer(iPlayer).isAlive()):
                                iNumAlive += 1
                                iTotal += self.getStability(iPlayer)
                iMean = iTotal/iNumAlive
                iDifferences = 0
                for iPlayer in range(iNumPlayers):
                        if (gc.getPlayer(iPlayer).isAlive()):
                               iDifferences += abs(self.getStability(iPlayer) - iMean)
                iSigma = iDifferences/iNumAlive

                #print ("mean=", iMean, "sigma=", iSigma)
                
                #division by zero fix
                if (iSigma == 0):
                        iSigma = 1
                        iStandardSigma = 8
                        iMinSigma = 5
                        
                iMonitorPlayer = utils.getHumanID() #debug con.iRome
                iTempNormalizationThreshold = self.getStability(iMonitorPlayer)
                        
                if (iSigma > iMaxSigma+3):
                        #print ("Normalized sigma1")
                        for iPlayer in range(iNumPlayers):
                                if (gc.getPlayer(iPlayer).isAlive()):
                                        self.setStability(iPlayer, (self.getStability(iPlayer) - iMean)*iMaxSigma/iSigma + iMean )
                elif (iSigma > iMaxSigma):
                        #print ("Normalized sigma2")
                        for iPlayer in range(iNumPlayers):
                                if (gc.getPlayer(iPlayer).isAlive()):
                                        self.setStability(iPlayer, (self.getStability(iPlayer) - iMean)*iStandardSigma/iSigma + iMean )
                elif (iSigma < iMinSigma-3):
                        #print ("Normalized sigma3")
                        for iPlayer in range(iNumPlayers):
                                if (gc.getPlayer(iPlayer).isAlive()):
                                        self.setStability(iPlayer, (self.getStability(iPlayer) - iMean)*iMinSigma/iSigma + iMean )
                elif (iSigma < iMinSigma):
                        #print ("Normalized sigma4")
                        for iPlayer in range(iNumPlayers):
                                if (gc.getPlayer(iPlayer).isAlive()):
                                        self.setStability(iPlayer, (self.getStability(iPlayer) - iMean)*iStandardSigma/iSigma + iMean )
                #calculate mean again cos it might have changed for values close to 0
                for iPlayer in range(iNumPlayers):
                        if (gc.getPlayer(iPlayer).isAlive()):
                                iNumAlive += 1
                                iTotal += self.getStability(iPlayer)
                iMean = iTotal/iNumAlive
                #print ("mean=", iMean)
                
                if (iMean > iStandardMean+6):
                        #print ("Normalized mean1")
                        for iPlayer in range(iNumPlayers):
                                if (gc.getPlayer(iPlayer).isAlive()):
                                        self.setStability(iPlayer, self.getStability(iPlayer) - iMean + iStandardMean+3)
                elif (iMean > iStandardMean+3):
                        #print ("Normalized mean2")
                        for iPlayer in range(iNumPlayers):
                                if (gc.getPlayer(iPlayer).isAlive()):
                                        self.setStability(iPlayer, self.getStability(iPlayer) - iMean + iStandardMean)
                elif (iMean < iStandardMean-6):
                        #print ("Normalized mean3")
                        for iPlayer in range(iNumPlayers):
                                if (gc.getPlayer(iPlayer).isAlive()):
                                        self.setStability(iPlayer, self.getStability(iPlayer) - iMean + iStandardMean-3)      
                elif (iMean < iStandardMean-3):
                        #print ("Normalized mean4")
                        for iPlayer in range(iNumPlayers):
                                if (gc.getPlayer(iPlayer).isAlive()):
                                        self.setStability(iPlayer, self.getStability(iPlayer) - iMean + iStandardMean)

                #print("parametersE before", self.getStabilityParameters(iParDiplomacyE), self.getStabilityParameters(iParEconomyE), self.getStabilityParameters(iParCitiesE), self.getStabilityParameters(iParCivicsE), self.getStabilityParameters(iParExpansionE))
                #print("prestab", self.getStability(iMonitorPlayer))
                iVariation = self.getStability(iMonitorPlayer) - iTempNormalizationThreshold
                if (iVariation != 0):
                        for iLoopPoint in range (abs(iVariation)): #points are distributed in various categories
                                if (iLoopPoint % 5 == 0 or iLoopPoint % 5 == 1):
                                        if (iVariation > 0):
                                                self.setParameter(iMonitorPlayer, iParDiplomacyE, True, 1)
                                        else: 
                                                self.setParameter(iMonitorPlayer, iParDiplomacyE, True, -1)
                                elif (iLoopPoint % 5 == 2):
                                        if (iVariation > 0):
                                                self.setParameter(iMonitorPlayer, iParEconomyE, True, 1)
                                        else: 
                                                self.setParameter(iMonitorPlayer, iParEconomyE, True, -1)
                                elif (iLoopPoint % 5 == 3):
                                        if (iVariation > 0):
                                                self.setParameter(iMonitorPlayer, iParCitiesE, True, 1)
                                        else: 
                                                self.setParameter(iMonitorPlayer, iParCitiesE, True, -1)
                                elif (iLoopPoint % 5 == 4):
                                        if (iVariation > 0):
                                                self.setParameter(iMonitorPlayer, iParCivicsE, True, 1)
                                        else: 
                                                self.setParameter(iMonitorPlayer, iParCivicsE, True, -1)

                #print("parametersE after ", self.getStabilityParameters(iParDiplomacyE), self.getStabilityParameters(iParEconomyE), self.getStabilityParameters(iParCitiesE), self.getStabilityParameters(iParCivicsE), self.getStabilityParameters(iParExpansionE))
                #self.setParameter(iPlayer, iParDiplomacyE, True, self.getStability(iMonitorPlayer) - iTempNormalizationThreshold)
                print ("Stability normalization:", self.getStability(iMonitorPlayer) - iTempNormalizationThreshold)


        def updateBaseStability(self, iGameTurn, iPlayer):
	
		fStart = time.clock()
		bLong = (iGameTurn % utils.getTurns(3) == 0)

                pPlayer = gc.getPlayer(iPlayer)
                teamPlayer = gc.getTeam(pPlayer.getTeam())

                iCivic0 = pPlayer.getCivics(0)
                iCivic1 = pPlayer.getCivics(1)
                iCivic2 = pPlayer.getCivics(2)
                iCivic3 = pPlayer.getCivics(3)
                iCivic4 = pPlayer.getCivics(4)
                iCivic5 = pPlayer.getCivics(5)
                
                if (iGameTurn % utils.getTurns(3) != 0):
                        iNewBaseStability = self.getPartialBaseStability(iPlayer)
                        iEconomy = pPlayer.calculateTotalCommerce() - pPlayer.calculateInflatedCosts() #used later
                        iIndustry = pPlayer.calculateTotalYield(YieldTypes.YIELD_PRODUCTION) #used later
                        iAgriculture = pPlayer.calculateTotalYield(YieldTypes.YIELD_FOOD) #used later
                        iPopulation = pPlayer.getRealPopulation() #used later                        
                        iDifference = (iIndustry*1000000/iPopulation) - (iEconomy*1000000/iPopulation) #used later
                        iEraModifier = pPlayer.getCurrentEra() #used later

                        if (iPlayer == con.iMali): #counterbalance its UP
                                #iEconomy *= 4
                                #iEconomy /= 7
                                iEconomy /= 2

                        if (iPlayer == con.iEgypt or iPlayer == con.iMali or iPlayer == con.iEthiopia): #counterbalance the flood plains
                                iAgriculture *= 7 #3
                                iAgriculture /= 10 #5
			elif iPlayer == con.iIndia:
				iAgriculture *= 6
				iAgriculture /= 10

                else:   #every 3 turns
                        iNewBaseStability = 0
               
                        iNewBaseStability += 10*teamPlayer.getDefensivePactTradingCount()
                        if (teamPlayer.getDefensivePactTradingCount() > 0):
                                #print("iNewBaseStability defensive pact",iNewBaseStability, iPlayer)
                                pass
                        
                        #if (teamPlayer.isPermanentAllianceTrading()):
                        #        iNewBaseStability += 10
                        #        #print("iNewBaseStability permanent alliance",iNewBaseStability, iPlayer)
                        
                        iNewBaseStability += 2*teamPlayer.getOpenBordersTradingCount()
                        #print("iNewBaseStability open borders",iNewBaseStability, iPlayer)

                        for iLoopCiv in range (iNumPlayers):
                                if (iLoopCiv in con.lNeighbours[iPlayer]):
                                        if (gc.getPlayer(iLoopCiv).isAlive()):
                                                if (self.getStability(iLoopCiv) < -20):
                                                        if (self.getStability(iPlayer) >= 0):
                                                                iNewBaseStability -= 5
                                                                #print("iNewBaseStability neighbours", iNewBaseStability, iPlayer)
                                                                break
                                
                        for iLoopCiv in range( iNumPlayers ):                                
                                if (teamPlayer.isVassal(iLoopCiv)):
                                        iNewBaseStability += 10                                
                                        #print("iNewBaseStability vassal",iNewBaseStability, iPlayer)
                                        iNewBaseStability += min(5,max(-6,self.getStability(iLoopCiv)/4))
                                        break

                        for iLoopCiv2 in range( iNumPlayers ):                                
                                if (gc.getTeam(gc.getPlayer(iLoopCiv2).getTeam()).isVassal(iPlayer)):
                                        iNewBaseStability += min(3,max(-3,self.getStability(iLoopCiv2)/4))                             
                                        #print("iNewBaseStability master",iNewBaseStability, iPlayer)
                                        if (iCivic5 == con.iViceroyalty):
                                                iNewBaseStability += 4
                                                #print("iNewBaseStability civic 6th column viceroyalty",iNewBaseStability, iPlayer)
						
			#Leoreth: imperialism: extra stability for controlling foreign cores:
			if (iCivic5 == con.iImperialism):
				for iOwnedCiv in range(iNumPlayers):
					reborn = utils.getReborn(iOwnedCiv)
					dummy1, plotList1 = utils.squareSearch( tNormalAreasTL[reborn][iOwnedCiv], tNormalAreasBR[reborn][iOwnedCiv], utils.ownedCityPlots, iActiveCiv )
					dummy2, plotList2 = utils.squareSearch( tNormalAreasTL[reborn][iOwnedCiv], tNormalAreasBR[reborn][iOwnedCiv], utils.ownedCityPlots, iOwnedCiv )
					if ((len(plotList1) >= 2 and len(plotList1) > len(plotList2)) or (len(plotList1) >= 1 and not gc.getPlayer(iOwnedCiv).isAlive())):
						iNewBaseStability += 2*len(plotList1)

                        iNumContacts = 0
                        for iLoopCiv3 in range( iNumPlayers ):     
                                if (pPlayer.canContact(iLoopCiv3) and iLoopCiv3 != iPlayer):
                                        iNumContacts += 1
                        iNewBaseStability -= (iNumContacts/3 - 4)
                        #print("iNewBaseStability contacts",iNewBaseStability, iPlayer)
                        
                        self.setParameter(iPlayer, iParDiplomacy3, False, iNewBaseStability) 
			
			iOutputForeignStability = iNewBaseStability
			print "PYTHON: Player " + str(iPlayer) + " foreign stability: " + str(iNewBaseStability)


                        iTempExpansionThreshold = iNewBaseStability

                        iMaxPlotsAbroad = 36
                        iHandicap = gc.getGame().getHandicapType()
                        if (iHandicap == 0):
                                iMaxPlotsAbroad = 40
                        elif (iHandicap == 2):
                                iMaxPlotsAbroad = 32
			
			# Leoreth: nerf Korean stability, and city states civic
			if iPlayer == con.iKorea:
				iMaxPlotsAbroad /= 2
                        
                        iNumPlotsAbroad = max(0,self.getOwnedPlotsLastTurn(iPlayer)-iMaxPlotsAbroad*2/3)                        
                        iNewBaseStability -= iNumPlotsAbroad*2/7
			
			iMaxPlotsAbroad -= self.getOwnedForeignCitiesLastTurn(iPlayer)*3
			
			iNumOuterPlotsAbroad = max(0, self.getOwnedOuterPlotsLastTurn(iPlayer)-iMaxPlotsAbroad/2)
			iNewBaseStability -= iNumOuterPlotsAbroad/4
			
                        #if (not gc.getPlayer(iPlayer).isHuman()):
                        #        iNewBaseStability += iNumPlotsAbroad*1/14
                        #print("iNewBaseStability number of owned plots abroad",iNewBaseStability, iPlayer)
                        if (self.getOwnedCitiesLastTurn(iPlayer) <= 20):
                                iNewBaseStability -= self.getOwnedCitiesLastTurn(iPlayer)*7
                        else:
                                iNewBaseStability -= (self.getOwnedCitiesLastTurn(iPlayer)-6)*10
                        #print("iNewBaseStability number of cities in homeland not owned", self.getOwnedCitiesLastTurn(iPlayer), iNewBaseStability, iPlayer)
                        self.setParameter(iPlayer, iParExpansion3, False, iNewBaseStability - iTempExpansionThreshold)
			
			iOutputExpansionStability = iNewBaseStability - iOutputForeignStability
			print "PYTHON: Player " + str(iPlayer) + " expansion stability: " + str(iNewBaseStability)

                                        
                        iTempCivicThreshold = iNewBaseStability
#                        if (iCivic0 == 3 and iCivic1 == 9): #police and free speech
#                                iNewBaseStability -= 10
#                                #print("iNewBaseStability civic combination1",iNewBaseStability, iPlayer)
#                        
#                        if (iCivic4 == 22 and iCivic2 == 14): #theo and emanc
#                                iNewBaseStability -= 3
#                                #print("iNewBaseStability civic combination2",iNewBaseStability, iPlayer)
#
#                        if (iCivic0 == 4 and iCivic1 == 5): #univ and barbar
#                                iNewBaseStability -= 3
#                                #print("iNewBaseStability civic combination3",iNewBaseStability, iPlayer)
#                        
#                        if (iCivic2 == 13 and iCivic3 == 18): #caste and state prop
#                                iNewBaseStability -= 7
#                                #print("iNewBaseStability civic combination4",iNewBaseStability, iPlayer)
#
#                        if (iCivic0 == 0 and iCivic1 == 7): #despo and bureo
#                                iNewBaseStability -= 2
#                                #print("iNewBaseStability civic combination5",iNewBaseStability, iPlayer)
#                                   
#                        if (iCivic1 == 6 and iCivic3 == 18): #vassal and state prop
#                                iNewBaseStability -= 7
#                                #print("iNewBaseStability civic combination6",iNewBaseStability, iPlayer)
#
#                        if (iCivic1 == 8 and iCivic4 == 23): #nation and pacifism
#                                iNewBaseStability -= 10
#                                #print("iNewBaseStability civic combination7",iNewBaseStability, iPlayer)
#                                
#                        if (iCivic0 == 3 and iCivic1 == 8): #police and nation
#                                iNewBaseStability += 10
#                                #print("iNewBaseStability civic combination8",iNewBaseStability, iPlayer)
#
#                        if (iCivic0 == 3 and iCivic3 == 18): #police and state prop
#                                iNewBaseStability += 5
#                                #print("iNewBaseStability civic combination9",iNewBaseStability, iPlayer)
#
#                        if (iCivic1 == 8 and iCivic3 == 16): #nation and mercant
#                                iNewBaseStability += 6
#                                #print("iNewBaseStability civic combination10",iNewBaseStability, iPlayer)
#                                
#                        if (iCivic0 == 1 and iCivic1 == 6): #heredit and vassal
#                                iNewBaseStability += 3
#                                #print("iNewBaseStability civic combination11",iNewBaseStability, iPlayer)
#                                
#                        if (iCivic0 == 2 and iCivic1 == 7): #repres and bureo
#                                iNewBaseStability += 4
#                                #print("iNewBaseStability civic combination12",iNewBaseStability, iPlayer)
#
#                        if (iCivic2 == 14 and iCivic4 == 24): #emancip and free rel
#                                iNewBaseStability += 2
#                                #print("iNewBaseStability civic combination13",iNewBaseStability, iPlayer)

			# Stability modifiers for Leoreth's new civics

#			if (iCivic0 == 0 and iCivic1 == 9): #Tyranny and Parliament
#				iNewBaseStability -= 3
#
#			if (iCivic0 == 4 and iCivic1 == 9): #Republic and Parliament
#				iNewBaseStability += 5
#
#			if (iCivic0 == 4 and iCivic2 == 13): #Republic and Totalitarianism
#				iNewBaseStability -= 10
#
#			if (iCivic2 == 13 and iCivic4 == 24): #Totalitarianism and Secularism
#				iNewBaseStability += 3
#
#			if (iCivic1 == 9 and iCivic2 == 13): #Parliament and Totalitarism
#				iNewBaseStability += 5
#
#			if (iCivic0 == 3 and iCivic2 == 13): #Autocracy and Totalitarianism
#				iNewBaseStability += 10
#
#			if (iCivic0 == 2 and iCivic4 == 22): #Theocracy and Patriarchate
#				iNewBaseStability += 4
#
#			if (iCivic0 == 2 and iCivic4 == 24): #Theocracy and Secularism
#				iNewBaseStability -= 8
#
#			if (iCivic0 == 2 and iCivic1 == 9): #Theocracy and Parliament
#				iNewBaseStability -= 3
#
#			if (iCivic0 == 0 and iCivic1 == 7): #Tyranny and Absolutism
#				iNewBaseStability -= 3
#
#			if (iCivic2 == 12 and iCivic3 == 18): #Capitalism and State Property
#				iNewBaseStability -= 7
#
#			if (iCivic1 == 6 and iCivic3 == 18): #Vassalage and State Property
#				iNewBaseStability -= 7
#
#			if (iCivic2 == 14 and iCivic3 == 18): #Socialism and State Property
#				iNewBaseStability += 5
#
#			if (iCivic0 == 3 and iCivic3 == 18): #Autocracy and State Property
#				iNewBaseStability += 5
#
#			if (iCivic1 == 7 and iCivic3 == 17): #Absolutism and Mercantilism
#				iNewBaseStability += 3
#
#			if (iCivic0 == 1 and iCivic1 == 6): #Monarchy and Vassalage
#				iNewBaseStability += 3
#
#			if (iCivic0 == 1 and iCivic2 == 11): #Monarchy and Aristocracy
#				iNewBaseStability += 3
#
#			if (iCivic0 == 4 and iCivic4 == 24): #Republic and Secularism
#				iNewBaseStability += 2
#
#			if (iCivic2 == 12 and iCivic3 == 19): #Capitalism and Free Market
#				iNewBaseStability += 3

			# authoritarian civics
			if (iCivic0 == con.iAutocracy and iCivic2 == con.iTotalitarianism):
				iNewBaseStability += 10
				
			if (iCivic2 == con.iTotalitarianism and iCivic3 == con.iStateProperty):
				iNewBaseStability += 5
				
			if (iCivic2 == con.iTotalitarianism and iCivic1 == con.iUniversalSuffrage):
				iNewBaseStability -= 10
				
			if (iCivic2 == con.iTotalitarianism and iCivic4 == con.iSecularism):
				iNewBaseStability += 3
				
			# communist civics
			if (iCivic1 == con.iSupremeCouncil and iCivic3 == con.iStateProperty):
				iNewBaseStability += 7
				
			if (iCivic3 == con.iStateProperty and iCivic2 in [con.iCapitalism, con.iAgrarianism]):
				iNewBaseStability -= 7
				
			if (iCivic1 == con.iSupremeCouncil and iCivic0 in [con.iDynasticism, con.iTheocracy]):
				iNewBaseStability -= 4
				
			# democratic civics
			if (iCivic0 == con.iRepublic and iCivic4 == con.iSecularism):
				iNewBaseStability += 2
				
			if (iCivic0 == con.iTyranny and iCivic1 in [con.iAbsolutism, con.iUniversalSuffrage]):
				iNewBaseStability -= 4
				
			if (iCivic0 == con.iRepublic and iCivic1 == con.iUniversalSuffrage):
				iNewBaseStability += 4
				
			# religious civics
			if (iCivic0 == con.iTheocracy and iCivic4 == con.iFanaticism):
				iNewBaseStability += 4
				
			if (iCivic0 == con.iTheocracy and iCivic4 == con.iSecularism):
				iNewBaseStability -= 8
				
			if (iCivic0 == con.iTheocracy and iCivic2 == con.iEgalitarianism):
				iNewBaseStability -= 3
				
			if (iCivic2 == con.iEgalitarianism and iCivic4 == con.iSecularism):
				iNewBaseStability += 3
				
			# monarchist civics
			if (iCivic1 == con.iVassalage and iCivic3 == con.iAgrarianism):
				iNewBaseStability += 3
				
			if (iCivic0 == con.iDynasticism and iCivic1 == con.iVassalage):
				iNewBaseStability += 3
				
			# other
			if (iCivic0 == con.iCityStates and iCivic1 == con.iVassalage):
				iNewBaseStability -= 2
				
			if (iCivic0 == con.iCityStates and iCivic2 != con.iUrbanization):
				iNewBaseStability -= 3
				
			if (iCivic0 == con.iCityStates and iCivic3 == con.iMercantilism):
				iNewBaseStability += 3
				
			if (iCivic1 == con.iAbsolutism and iCivic3 == con.iMercantilism):
				iNewBaseStability += 3
				
			if (iCivic2 == con.iCapitalism and iCivic3 == con.iFreeMarket):
				iNewBaseStability += 2

                        if (iCivic1 == con.iVassalage): #vassalage
                                if (pPlayer.getCurrentEra() == con.iMedieval):	#Bonus in medieval, Penalty in others
                                        iNewBaseStability += 3
                                else:
                                        iNewBaseStability -= 3
                                #print("iNewBaseStability civic single 1",iNewBaseStability, iPlayer)

			if (iCivic0 == con.iTheocracy): #Theocracy
				if (pPlayer.getCurrentEra() >= con.iIndustrial):	#Penalty in industrial or later
					iNewBaseStability -= 5

			if (iCivic4 == con.iPantheon): #Pantheon
				if (pPlayer.getCurrentEra() <= con.iClassical):	#Bonus in classical and ancient, penalty in others
					iNewBaseStability += 3
				else:
					iNewBaseStability -= 3
					
			if (iCivic0 == con.iCityStates):
				if (pPlayer.getCurrentEra() > con.iClassical):
					iNewBaseStability -= 4
				if pPlayer.getCurrentEra() >= con.iIndustrial:
					iNewBaseStability -= 4

			if (iCivic1 == con.iRepresentation): #Representation
				if (pPlayer.getCurrentEra() >= con.iIndustrial):	#Bonus in industrial or later
					iNewBaseStability += 3
					
			if iCivic0 == con.iRepublic:
				if pPlayer.getCurrentEra() == con.iMedieval:
					iNewBaseStability -= 10

                        if (iCivic1 == con.iAbsolutism): #Absolutism			#threshold=5, cap=-7
                                if (pPlayer.getNumCities() <= 5):
                                        iNewBaseStability += 5
                                else:
                                        iNewBaseStability += max(-7,(5 - pPlayer.getNumCities()))
                                #print("iNewBaseStability civic single 2",iNewBaseStability, iPlayer)

#                        if (iCivic0 == 2): #represent
#                                iNewBaseStability += max(-7,2*(3 - pPlayer.getNumCities()))
#                                #print("iNewBaseStability civic single 3",iNewBaseStability, iPlayer)

			if (iCivic1 == con.iRepresentation):
				iNewBaseStability += max(-8, 2*(4 - pPlayer.getNumCities()))

			if (iCivic0 == con.iRepublic): #Republic
				iNewBaseStability += max(-5,5 - pPlayer.getNumCities())	#threshold=5, cap=-5
				
			if iCivic0 == con.iCityStates:
				if pPlayer.getNumCities() > 4:
					iNewBaseStability -= min(20, (pPlayer.getNumCities() - 4) * 4)

                        if (iCivic2 == con.iTotalitarianism): #Totalitarianism
                                iNewBaseStability += min(10, pPlayer.getNumCities()/5) #slightly counterbalances the effect of number of cities (below)

                                #print("iNewBaseStability civic single 4",iNewBaseStability, iPlayer)
                                
                        if (iCivic0 == con.iAutocracy): #Autocracy
                                iNewBaseStability += 3*teamPlayer.getAtWarCount(True)
                                #print("iNewBaseStability civic single 5",iNewBaseStability, iPlayer)
				
			if iCivic4 == con.iFanaticism:
				for iEnemyCiv in range(con.iNumPlayers):
					if teamPlayer.isAtWar(iEnemyCiv) and pPlayer.getStateReligion() != gc.getPlayer(iEnemyCiv).getStateReligion():
						iNewBaseStability += 3

                        if (iCivic0 == con.iTyranny): #Tyranny
                                if (self.getStability(iPlayer) < -60):
                                        self.setStability(iPlayer, self.getStability(iPlayer)+20)
                                        #print("iNewBaseStability civic first column 1",iNewBaseStability, iPlayer)

                        if (iCivic0 == con.iDynasticism): #Monarchy
                                if (self.getStability(iPlayer) < -50):
                                        self.setStability(iPlayer, -50)
                                        #print("iNewBaseStability civic first column 2",iNewBaseStability, iPlayer)

#                        if (iCivic0 == 2): #representation
#                                if (self.getStability(iPlayer) > 30):
#                                        iNewBaseStability += 5
#                                        #print("iNewBaseStability civic first column 3",iNewBaseStability, iPlayer)

			if (iCivic0 == con.iTheocracy): #Theocracy
				if (self.getStability(iPlayer) < -40):
					self.setStability(iPlayer, -40)

                        if (iCivic0 == con.iAutocracy): #Autocracy
                                if (self.getStability(iPlayer) < -60):
                                        self.setStability(iPlayer, self.getStability(iPlayer)+30)
                                        #print("iNewBaseStability civic first column 4",iNewBaseStability, iPlayer)

                        if (iCivic0 == con.iRepublic): #Republic
                                if (self.getStability(iPlayer) > 30):
                                        iNewBaseStability += 5
                                        #print("iNewBaseStability civic first column 5",iNewBaseStability, iPlayer)

			if (iCivic1 == con.iUniversalSuffrage): #Parliament
				if (self.getStability(iPlayer) > 50):
					iNewBaseStability += 5
                                        
                        if (teamPlayer.isHasTech(con.iDemocracy)):
                                if (iCivic1 == con.iUniversalSuffrage): #Parliament
                                        iNewBaseStability += 3
                                        #print("iNewBaseStability universal suffrage",iNewBaseStability, iPlayer)

#                                if (iCivic2 != 14): #emancipation
#                                        iNewBaseStability -= 3
#                                        #print("iNewBaseStability emancipation",iNewBaseStability, iPlayer)

                        if (teamPlayer.isHasTech(con.iCommunism)):
                                if (not iCivic2 == con.iEgalitarianism): #not Egalitarianism
                                        iNewBaseStability -= 3
                                        #print("iNewBaseStability free speech",iNewBaseStability, iPlayer)

			if (teamPlayer.isHasTech(con.iConstitution)):
                                if (iCivic0 != con.iRepublic): #Republic
                                        iNewBaseStability -= 3
                                        #print("iNewBaseStability free speech",iNewBaseStability, iPlayer)

                        if (teamPlayer.isHasTech(con.iMasonry) and not teamPlayer.isHasTech(con.iDemocracy)):
                                if (iCivic3 == con.iForcedLabor): #Serfdom
                                        iNewBaseStability += 3
                                        #print("iNewBaseStability slavery",iNewBaseStability, iPlayer)
					
			if teamPlayer.isHasTech(con.iDemocracy) and not iCivic2 == con.iTotalitarianism:
				if iCivic3 == con.iForcedLabor:
					iNewBaseStability -= 3
                                
                        if (iCivic3 == con.iSelfSufficiency): #Self-sufficiency
                                if (teamPlayer.isHasTech(con.iEconomics)):
                                        iNewBaseStability -= 5
                                        #print("iNewBaseStability decentralization",iNewBaseStability, iPlayer)    
                                        
                        self.setParameter(iPlayer, iParCivics3, False, iNewBaseStability - iTempCivicThreshold)
			
			iOutputCivicStability = iNewBaseStability - iOutputForeignStability - iOutputExpansionStability
			print "PYTHON: Player " + str(iPlayer) + " civic stability: " + str(iNewBaseStability)


                        iTotalTempCityStability = 0
                        apCityList = PyPlayer(iPlayer).getCityList()

                        for pLoopCity in apCityList:
                                iX = pLoopCity.GetCy().getX()
                                iY = pLoopCity.GetCy().getY()
                                for iLoop in range(iNumMajorPlayers):
                                        if (iGameTurn > getTurnForYear(con.tBirth[iLoop]) and iLoop != iPlayer):
						reborn = utils.getReborn(iLoop)
                                                if (iX >= con.tNormalAreasTL[reborn][iLoop][0] and iX <= con.tNormalAreasBR[reborn][iLoop][0] and \
                                                    iY >= con.tNormalAreasTL[reborn][iLoop][1] and iY <= con.tNormalAreasBR[reborn][iLoop][1]):
                                                        if (gc.getPlayer(iPlayer).getSettlersMaps( 67-iY, iX ) < 150):
                                                                iNewBaseStability -= 3
                                                                self.setParameter(iPlayer, iParExpansion3, True, -3)                                                                
                                                                #print("city owned in unstable area: -3", pLoopCity.GetCy().getName(), iPlayer)
                                                                break
                                                        else:
                                                                iNewBaseStability -= 1
                                                                self.setParameter(iPlayer, iParExpansion3, True, -1)
                                                                #print("city owned in unstable area: -1", pLoopCity.GetCy().getName(), iPlayer)
                                                                break
								
			iOutputCoreStability = iNewBaseStability - iOutputForeignStability - iOutputExpansionStability - iOutputCivicStability
			print "PYTHON: Player " + str(iPlayer) + " core stability: " + str(iNewBaseStability)
                            
                        
                        for pCity in apCityList:
                                city = pCity.GetCy()
                                pCurrent = gc.getMap().plot(city.getX(), city.getY())
                                iTempCityStability = 0
				
				iCount = apCityList.index(pCity)

                                if (iCivic5 == con.iOccupation and city.isOccupation()):                  
                                        #print("iTotalTempCityStability civic 6th column occupation", iTotalTempCityStability, city.getName(), iPlayer)
                                        pass
                                else:
					if (iCivic2 == con.iTotalitarianism):	#Totalitarianism
                                        	if (city.angryPopulation(0) > 0):
                                        	        iTempCityStability -= 1
                                        	#if (city.healthRate(False, 0) < 0):
                                        	#        iTempCityStability -= 1
                                        	if (city.getReligionBadHappiness() > 0 and iCivic4 != con.iScholasticism):
                                        	        iTempCityStability -= 1
                                        	if (city.getLargestCityHappiness() < 0):
                                        	        iTempCityStability -= 1
                                        	if (city.getHurryAngerModifier() > 0):
                                        	        iTempCityStability -= 1
                                        	if (city.getNoMilitaryPercentAnger() > 0):
                                        	        iTempCityStability -= 1
                                        	if (city.getWarWearinessPercentAnger() > 0):
	                                                iTempCityStability -= 1
					else:
						if (city.angryPopulation(0) > 0):
       	                               		        iTempCityStability -= 2
               	                       		#if (city.healthRate(False, 0) < 0):
                       	               		#        iTempCityStability -= 2
       	                	       		if (city.getReligionBadHappiness() > 0 and iCivic4 != con.iScholasticism):
                               			        iTempCityStability -= 2
                                      		if (city.getLargestCityHappiness() < 0):
                                     		        iTempCityStability -= 2
               	                      		if (city.getHurryAngerModifier() > 0):
                       	               		        iTempCityStability -= 2
                               	       		if (city.getNoMilitaryPercentAnger() > 0):
                               			        iTempCityStability -= 1
      	                               		if (city.getWarWearinessPercentAnger() > 0):
      	                                	        iTempCityStability -= 1
							
					iOutputCityHappy = iTempCityStability
					print "PYTHON: Player " + str(iPlayer) + " City " + str(iCount) + " happy stability: " + str(iOutputCityHappy)

                                        if (iTempCityStability <= -5): #middle check, for optimization
                                                iTotalTempCityStability += max(-5,iTempCityStability)
                                                #print("iTotalTempCityStability", iTotalTempCityStability, city.getName(), iPlayer)
                                                if (iTotalTempCityStability <= -10): #middle check, for optimization
                                                        break
                                                else:
                                                        continue
                                                    

					if (iCivic4 == con.iPantheon): #Pantheon
                                                iCounter = 0
                                                for iLoop in range(con.iNumReligions):                                    
                                                        if (city.isHasReligion(iLoop)):
                                                                iTempCityStability -= 1

					if (iCivic0 == con.iTheocracy): #Theocracy
						iCounter = 1
						for iLoop in range(con.iNumReligions):
							if (city.isHasReligion(iLoop) and pPlayer.getStateReligion() != iLoop):
								iCounter = 0
							if (not city.isHasReligion(iLoop) and pPlayer.getStateReligion() == iLoop):
								iCounter = 0
						if (iCounter == 1):
							iTempCityStability += 1		# +1 stability if state religion, but no foreign present
								
					iOutputCityCivic = iTempCityStability - iOutputCityHappy
					print "PYTHON: Player " + str(iPlayer) + " City " + str(iCount) + " civic stability: " + str(iOutputCityCivic)
                                                                
                                        for iLoop in range(iNumTotalPlayers+1):		# no penalties from foreign culture with Egalitarianism?
                                                if (iLoop != iPlayer):
                                                        if (pCurrent.getCulture(iLoop) > 0):
                                                                if (pCurrent.getCulture(iPlayer) == 0): #division by zero may happen
                                                                        iTempCityStability -= 2
                                                                elif (iCivic0 == con.iAutocracy): #Autocracy
                                                                        if (pCurrent.getCulture(iLoop)*100/pCurrent.getCulture(iPlayer) >= 5):
                                                                                iTempCityStability -= 2
                                                                                break
                                                                else:
                                                                        if (pCurrent.getCulture(iLoop)*100/pCurrent.getCulture(iPlayer) >= 15):
                                                                                if (iPlayer == con.iTurkey or iPlayer == con.iAmerica or iPlayer == con.iPortugal or iPlayer == con.iNetherlands): #they have too much foreign culture
                                                                                        iTempCityStability -= 1
                                                                                else:
                                                                                        iTempCityStability -= 2
                                                                                break
										
							
					iOutputCityCulture = iTempCityStability - iOutputCityCivic - iOutputCityHappy
					print "PYTHON: Player " + str(iPlayer) + " City " + str(iCount) + " culture stability: " + str(iOutputCityCulture)

                                        
                                        if (iTempCityStability < 0):
                                                iTotalTempCityStability += max(-5,iTempCityStability)
                                                #print("iTotalTempCityStability", iTotalTempCityStability, city.getName(), iPlayer)
                                        
                                        if (iTotalTempCityStability <= -12): #middle check, for optimization
                                                break
				
                        if (iTotalTempCityStability < 0):
                                iNewBaseStability += max(-12, iTotalTempCityStability)
                                #print("iNewBaseStability city check", iNewBaseStability, iPlayer)
                        self.setParameter(iPlayer, iParCities3, False, iTotalTempCityStability)
			
			iOutputCityStability = iNewBaseStability - iOutputCoreStability - iOutputCivicStability - iOutputForeignStability - iOutputExpansionStability
			print "PYTHON: Player " + str(iPlayer) + " city stability: " + str(iNewBaseStability)

                        iTempEconomyThreshold = iNewBaseStability
                        iImports = pPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE)
                        iExports = pPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
                        iEraModifier = pPlayer.getCurrentEra()
                        iImportExportOffset = 5
                        
                        if (iPlayer == con.iChina or iPlayer == con.iJapan): #counterbalance their isolation
                                iImportExportOffset = 3
                                
                        if (iEraModifier >= 3):
                                iEraModifier += 1
                        if (iCivic5 != con.iCommonwealth):
                                iNewBaseStability += min(10,(iImports+iExports)/(2*iEraModifier+1) -iImportExportOffset)
                                #print("iNewBaseStability import/export check", iNewBaseStability, iPlayer)
                        else:
                                iNewBaseStability += max(0, min(10,(iImports+iExports)/(2*iEraModifier+1) -iImportExportOffset))
                                #print("iNewBaseStability import/export check + civic 6th column commonwealth", iNewBaseStability, iPlayer)

                        iEconomy = pPlayer.calculateTotalCommerce() - pPlayer.calculateInflatedCosts()
                        iIndustry = pPlayer.calculateTotalYield(YieldTypes.YIELD_PRODUCTION)
                        iAgriculture = pPlayer.calculateTotalYield(YieldTypes.YIELD_FOOD)
                        iPopulation = pPlayer.getRealPopulation()

                        if (iPlayer == con.iIndia or iPlayer == con.iChina or iPlayer == con.iJapan or iPlayer == con.iMughals or iPlayer == con.iIndonesia): #counterbalance the low growth threshold of ancient civs
                                iPopulation *= 3
                                iPopulation /= 4
                        if (iPlayer == con.iEgypt or iPlayer == con.iMaya or iPlayer == con.iMali or iPlayer == con.iKhmer): #counterbalance the high growth threshold
                                iPopulation *= 4
                                iPopulation /= 3

                        if (iPlayer == con.iMali): #counterbalance its UP
                                #iEconomy *= 4
                                #iEconomy /= 7
                                iEconomy /= 2

                        if (iPlayer == con.iEgypt or iPlayer == con.iMali or (iPlayer == con.iEthiopia and not gc.getPlayer(con.iEgypt).isAlive()) or iPlayer == con.iMughals or iPlayer == con.iIndia): #counterbalance the flood plains
                                iAgriculture *= 75 #3
                                iAgriculture /= 100 #5
                        
                        iNewBaseStability += min(8,max(-8,(iAgriculture*100000/iPopulation - 8 + (iEraModifier - 3)*2)))
                        #print("iNewBaseStability Agriculture/Population check", iNewBaseStability, iPlayer)
                        iMaxEconomyGain = 3
                        iMaxEconomyLoss = -3
                        if (iCivic5 != con.iCommonwealth):
                                iNewBaseStability += min(iMaxEconomyGain,max(iMaxEconomyLoss,(iEconomy*100000/iPopulation - 5 + (iEraModifier - 3)*2))) #less important cos it's already counted in other parameters
                                #print("iNewBaseStability Economy/Population check", iNewBaseStability, iPlayer)
                        else:
                                iNewBaseStability += min(iMaxEconomyGain,max(0,(iEconomy*100000/iPopulation - 5 + (iEraModifier - 3)*2)))
                                #print("iNewBaseStability Economy/Population check + civic 6th column commonwealth", iNewBaseStability, iPlayer)

                        self.setParameter(iPlayer, iParEconomy3, False, iNewBaseStability - iTempEconomyThreshold)

                        iDifference = (iIndustry*1000000/iPopulation) - (iEconomy*1000000/iPopulation)



                        iHappiness = -10
                        if (pPlayer.calculateTotalCityHappiness() > 0):
                                iHappiness = int((1.0 * pPlayer.calculateTotalCityHappiness()) / (pPlayer.calculateTotalCityHappiness() + \
                                                pPlayer.calculateTotalCityUnhappiness()) * 100) - 60			
                        iNewBaseStability += iHappiness/10
                        self.setParameter(iPlayer, iParCities3, True, iHappiness/10)                        
                        #print("iNewBaseStability happiness check", iNewBaseStability, iPlayer)

                        #iHealth = -30
                        #if (pPlayer.calculateTotalCityHealthiness() > 0):
                        #        iHealth = int((1.0 * pPlayer.calculateTotalCityHealthiness()) / (pPlayer.calculateTotalCityHealthiness() + \
                        #                        pPlayer.calculateTotalCityUnhealthiness()) * 100) - 60
                        #iNewBaseStability += iHealth/10
                        ##print("iNewBaseStability health check", iNewBaseStability, iPlayer)
                        
                        self.setPartialBaseStability(iPlayer, iNewBaseStability)


                #every turn

                if (iGameTurn >= getTurnForYear(con.tBirth[iPlayer])+utils.getTurns(15)):
                        self.setGNPnew(iPlayer, self.getGNPnew(iPlayer) + (iEconomy + 4*iIndustry + 2*iAgriculture)/7)
                        if (iGameTurn % utils.getTurns(3) == 2):
                                iTempEconomyThreshold = self.getStability(iPlayer)
                                iMaxShrink = 7
                                iMaxGrowth = 3
                                iNegativeFasterGrowth = (self.getGNPnew(iPlayer)-4)/3 - self.getGNPold(iPlayer)/3   #-1:-1 -2:-2 -3:-2 -4:-2 -5:-3 -6:-3 -7:-3 -8:-4 
                                iNegativeNormalGrowth = (self.getGNPnew(iPlayer)-3)/3 - self.getGNPold(iPlayer)/3   #-1:-1 -2:-1 -3:-2 -4:-2 -5:-2 -6:-3 -7:-3 -8:-3 
                                iNegativeSlowerGrowth = (self.getGNPnew(iPlayer)-1)/3 - self.getGNPold(iPlayer)/3   #-1: 0 -2:-1 -3:-1 -4:-1 -5:-2 -6:-2 -7:-2 -8:-3 
                                
                                iPositiveFasterGrowth = self.getGNPnew(iPlayer)/3 - self.getGNPold(iPlayer)/3   # 0: 0 +1: 0 +2: 0 +3:+1 +4:+1 +5:+1 +6:+2 +7:+2 +8:+2 +9:+3   
                                iPositiveNormalGrowth = self.getGNPnew(iPlayer)/4 - self.getGNPold(iPlayer)/4       # 0: 0 +1: 0 +2: 0 +3: 0 +4:+1 +5:+1 +6:+1 +7:+1 +8:+2 +9:+2 
                                iPositiveSlowerGrowth = self.getGNPnew(iPlayer)/5 - self.getGNPold(iPlayer)/5       # 0: 0 +1: 0 +2: 0 +3: 0 +4: 0 +5:+1 +6:+1 +7:+1 +8:+1 +9:+1 

                                iNegativeGrowth = iNegativeNormalGrowth
                                iPositiveGrowth = iPositiveNormalGrowth
                                if (iPlayer == con.iEgypt or iPlayer == con.iChina or iPlayer == con.iBabylonia): #counterbalance their stagnation due to the very early start
                                        iNegativeGrowth = iNegativeSlowerGrowth
                                if (iPlayer == con.iNetherlands or iPlayer == con.iMali or iPlayer == con.iPortugal or iPlayer == con.iMongolia or iPlayer == con.iTurkey): #counterbalance their late start
                                        iPositiveGrowth = iPositiveSlowerGrowth
                                if (iPlayer == con.iMali or iPlayer == con.iPortugal or iPlayer == con.iMongolia or iPlayer == con.iTurkey or iPlayer == con.iAmerica): #counterbalance their late start
                                        iNegativeGrowth = iNegativeFasterGrowth
                                if (iPlayer == con.iJapan or iPlayer == con.iInca): #counterbalance their stagnation due to isolation
                                        iNegativeGrowth = iNegativeSlowerGrowth
                                if (iPlayer == con.iIndia or iPlayer == con.iChina or iPlayer == con.iJapan or iPlayer == con.iKhmer or iPlayer == con.iMaya or iPlayer == con.iAztecs or iPlayer == con.iInca): #counterbalance their stagnation due to isolation
                                        iPositiveGrowth = iPositiveFasterGrowth
                                                          
                                if (self.getGNPnew(iPlayer) < self.getGNPold(iPlayer)):
                                        self.setStability(iPlayer, self.getStability(iPlayer) + max(-iMaxShrink, iNegativeGrowth))
                                        #print("Stability - GNP check", iNegativeGrowth, iPlayer)
                                elif (self.getGNPnew(iPlayer) >= self.getGNPold(iPlayer)):
                                        self.setStability(iPlayer, self.getStability(iPlayer) + min(iMaxGrowth, iPositiveGrowth))
                                        #print("Stability - GNP check", iPositiveGrowth, iPlayer)
                                
                                self.setParameter(iPlayer, iParEconomyE, True, self.getStability(iPlayer) - iTempEconomyThreshold)


                                if (self.getGreatDepressionCountdown(iPlayer) == 0):   #great depression checked when GNP can be compared
                                        if (iCivic3 == con.iFreeMarket and teamPlayer.isHasTech(con.iCorporation)): #Free Market
                                                if (not pPlayer.isGoldenAge()):
                                                        if ((iDifference > 11 and self.getGNPnew(iPlayer) > self.getGNPold(iPlayer)) or \
                                                            (iDifference > 6 and self.getGNPnew(iPlayer) > self.getGNPold(iPlayer) + 4)): #low wages and big growth
                                                                self.setGreatDepressionCountdown(iPlayer, 8) #8 turns
                                                                print ("Start Great Depression Player", iPlayer)
                                                                
                if (self.getGreatDepressionCountdown(iPlayer) < 0):
                        self.setGreatDepressionCountdown(iPlayer, self.getGreatDepressionCountdown(iPlayer)+1)
                                                                
                iTempEconomyThreshold = iNewBaseStability
                if (self.getGreatDepressionCountdown(iPlayer) > 0):
                        iNewBaseStability -= (15 + min(15, iDifference))
                        if (iPlayer == utils.getHumanID()):
                                CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_PERIOD", ()) + " " + CyTranslator().getText("TXT_KEY_STABILITY_GREAT_DEPRESSION", ()), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
                        #print("iNewBaseStability civic single 5: great depression",iNewBaseStability, iPlayer)
                        self.setGreatDepressionCountdown(iPlayer, self.getGreatDepressionCountdown(iPlayer)-1)
                        bQuit = False
                        if (self.getGreatDepressionCountdown(iPlayer) == 0): #just quit
                                bQuit = True
                        if (self.getGreatDepressionCountdown(iPlayer) > 0 and self.getGreatDepressionCountdown(iPlayer) <= 7): #should last at least 3 turns 
                                if ((iDifference < 5 and self.getGNPnew(iPlayer) <= self.getGNPold(iPlayer)) or iCivic3 != con.iFreeMarket): #better wages and natural deflation, or no free market anymore
                                        bQuit = True
                                        
                        if (bQuit == True):
                                self.setGreatDepressionCountdown(iPlayer, -30) ##quit from the spiral immediately and set turns of immunity
                                bOtherDepressionAround = False
                                for iLoopCiv in range(iNumPlayers):
                                        if (self.getGreatDepressionCountdown(iLoopCiv) > 0):
                                                bOtherDepressionAround = True
                                if (bOtherDepressionAround == False):
                                        for iLoopCiv in range(iNumPlayers):
                                                if (iLoopCiv != iPlayer):
                                                        self.setGreatDepressionCountdown(iLoopCiv, -20) ##set turns of immunity for the other civs

                if (iGameTurn % utils.getTurns(3) == 2):
                        self.setGNPold(iPlayer, self.getGNPnew(iPlayer))
                        self.setGNPnew(iPlayer, 0)

                if (self.getGreatDepressionCountdown(iPlayer) == 0 and iCivic3 != con.iStateProperty and not pPlayer.isGoldenAge()):   #acquire only if there's no depression already and if it's not immune, no state property and no golden age
                        for iLoopCiv in range(iNumPlayers):
                                if (teamPlayer.isOpenBorders(iLoopCiv)):
                                        if (self.getGreatDepressionCountdown(iLoopCiv) > 0):
                                                if (iCivic3 == con.iMercantilism): #mercantilism
                                                        iNewBaseStability -= 4
                                                else:
                                                        iNewBaseStability -= 10
                                                #print("acquired great depression", iPlayer, "from", iLoopCiv)                        
                                                #print("iNewBaseStability: acquired great depression",iNewBaseStability, iPlayer)                        
                                                if (iPlayer == utils.getHumanID()):
                                                        CyInterface().addMessage(iPlayer, False, con.iDuration, \
                                                                                 CyTranslator().getText("TXT_KEY_STABILITY_GREAT_DEPRESSION_INFLUENCE", (gc.getPlayer(iLoopCiv).getCivilizationDescription(0),)), \
                                                                                 "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
                                                break #just once is enough
         
                
                if (teamPlayer.isHasTech(con.iCommunism)): #post communism
                        if (iCivic3 == con.iStateProperty): #state prop
                                self.setStatePropertyCountdown(iPlayer, -1) #has state property
                        if (self.getStatePropertyCountdown(iPlayer) == -1 and iCivic3 != con.iStateProperty): #switched
                                self.setStatePropertyCountdown(iPlayer, 8) #8 turns
                        if (self.getStatePropertyCountdown(iPlayer) > 0):
                                iNewBaseStability -= 25
                                self.setStatePropertyCountdown(iPlayer, self.getStatePropertyCountdown(iPlayer)-1)
                                if (iPlayer == utils.getHumanID()):
                                        CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_PERIOD", ()) + " " + CyTranslator().getText("TXT_KEY_STABILITY_POST_COMMUNISM", ()), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
                                #print("iNewBaseStability civic single 6: post communism",iNewBaseStability, iPlayer)
                self.setParameter(iPlayer, iParEconomy1, False, iNewBaseStability - iTempEconomyThreshold)

                iTempCivicThreshold = iNewBaseStability
                if (teamPlayer.isHasTech(con.iDemocracy)): #transition to democracy
                        if (iCivic1 in [con.iDirectRule, con.iVassalage, con.iAbsolutism, con.iSupremeCouncil]): #despotic governments
                                self.setDemocracyCountdown(iPlayer, -1) #has a desp. gov.
                        if (self.getDemocracyCountdown(iPlayer) == -1 and iCivic1 == con.iUniversalSuffrage): #switched to parliament
                                self.setDemocracyCountdown(iPlayer, 7) #7 turns
                        if (self.getDemocracyCountdown(iPlayer) > 0):
                                iNewBaseStability -= 20
                                self.setDemocracyCountdown(iPlayer, self.getDemocracyCountdown(iPlayer)-1)
                                if (iPlayer == utils.getHumanID()):
                                        CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_PERIOD", ()) + " " + CyTranslator().getText("TXT_KEY_STABILITY_DEMOCRACY", ()), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
                                #print("iNewBaseStability civic single 7: transition to democracy",iNewBaseStability, iPlayer)
                self.setParameter(iPlayer, iParCivics1, False, iNewBaseStability - iTempCivicThreshold)

                iTempExpansionThreshold = iNewBaseStability
                iNumPlayerCities = pPlayer.getNumCities()
                if (iNumPlayerCities < 8):
                        pass
                else:
                        iNewBaseStability -= (iNumPlayerCities-5)*(iNumPlayerCities-5)/9
                        #print("iNewBaseStability number of cities",iNewBaseStability, iPlayer)
                self.setParameter(iPlayer, iParExpansion1, False, iNewBaseStability - iTempExpansionThreshold)


                if (self.getCombatResultTempModifier(iPlayer) != 0):
                        iTempExpansionThreshold = iNewBaseStability
                        iNewBaseStability += max(-20, min(20,self.getCombatResultTempModifier(iPlayer)))
                        self.setParameter(iPlayer, iParExpansion1, True, iNewBaseStability - iTempExpansionThreshold) 
                        #print("iNewBaseStability combat result", iNewBaseStability, iPlayer)
                        if (self.getCombatResultTempModifier(iPlayer) <= -4 -(iEraModifier/2)): #great loss
                                self.setStability(iPlayer, self.getStability(iPlayer) -1)
                                self.setParameter(iPlayer, iParDiplomacyE, True, -1)
                                #print("Stability: combat result - great loss", self.getCombatResultTempModifier(iPlayer), iPlayer)
                        if (abs(self.getCombatResultTempModifier(iPlayer)) >= 4):
                                self.setCombatResultTempModifier(iPlayer, self.getCombatResultTempModifier(iPlayer)/2)
                        else:
                                self.setCombatResultTempModifier(iPlayer, 0)
                                                        
                if (pPlayer.getAnarchyTurns() != 0):
                        iTempCivicsThreshold = self.getStability(iPlayer)
                        if (self.getStability(iPlayer) > 24):
                                #print("Stability: anarchy permanent", self.getStability(iPlayer) - self.getStability(iPlayer)/8, iPlayer)
                                self.setStability(iPlayer, self.getStability(iPlayer) - self.getStability(iPlayer)/8/utils.getTurns(1)) # edead: penalty scaling                               
                        else:
                                #print("Stability: anarchy permanent", 3, iPlayer)
                                self.setStability(iPlayer, self.getStability(iPlayer)-3/utils.getTurns(1)) # edead: penalty scaling
                        self.setParameter(iPlayer, iParCivicsE, True, self.getStability(iPlayer) - iTempCivicsThreshold)
                        iNewBaseStability -= (self.getStability(iPlayer)+30)/2
                        self.setParameter(iPlayer, iParCivics1, True, -(self.getStability(iPlayer)+30)/2) 
                        #print("iNewBaseStability anarchy",iNewBaseStability, iPlayer)
                        

                if (pPlayer.isGoldenAge()):
                        iNewBaseStability += 20
                        #print("iNewBaseStability golden",iNewBaseStability, iPlayer)
                        self.setParameter(iPlayer, iParEconomy1, True, 20)

		# Leoreth: lower player's stability by 10 after a specific historical date to further their collapse
		# the human player is not affected, his neighbors only by half
		# stability hit starts with 1 and increases every turn until its maximum
		if ( (not pPlayer.isHuman()) and (not pPlayer.isReborn()) and iGameTurn >= getTurnForYear(con.tFall[pPlayer.getID()])):
			bHumanNeighbour = False
			for iNeighbour in con.lNeighbours[pPlayer.getID()]:
				if gc.getPlayer(iNeighbour).isHuman() and gc.getPlayer(iNeighbour).isAlive():
					bHumanNeighbour = True

			if bHumanNeighbour:
				iNewBaseStability -= min(10, iGameTurn - getTurnForYear(con.tFall[pPlayer.getID()]))
			else:
				iNewBaseStability -= min(20, iGameTurn - getTurnForYear(con.tFall[pPlayer.getID()]))
                
                
                  
                ##print ("iNewBaseStability", iNewBaseStability)

                                
                self.setStability(iPlayer, self.getStability(iPlayer) - self.getBaseStabilityLastTurn(iPlayer) + iNewBaseStability)
                if (self.getStability(iPlayer) < -80):
                        self.setStability(iPlayer, -80)
                if (self.getStability(iPlayer) > 80):
                        self.setStability(iPlayer, 80)
                        
                self.setBaseStabilityLastTurn(iPlayer, iNewBaseStability)
		
		fEnd = time.clock()
		
		fElapsed = fEnd - fStart
		
		if bLong:
			print "PYTHON: Performed LONG stability calculation for player "+str(iPlayer)+" in "+str(fElapsed*1000)+" ms."
		else:
			print "PYTHON: Performed SHORT stability calculation for player "+str(iPlayer)+" in "+str(fElapsed*1000)+" ms."
                                 



        def onCityBuilt(self, iPlayer, x, y):

                iTempExpansionThreshold = self.getStability(iPlayer)
                iGameTurn = gc.getGame().getGameTurn()
                if (iGameTurn <= getTurnForYear(con.tBirth[iPlayer]) + utils.getTurns(20)):
                        self.setStability(iPlayer, self.getStability(iPlayer) + 3 )
			gc.getPlayer(iPlayer).changeStability(3) # test DLL
                else:
                        self.setStability(iPlayer, self.getStability(iPlayer) + 1 )
			gc.getPlayer(iPlayer).changeStability(1) # test DLL
                #print("Stability - city built", iPlayer)
                if (gc.getPlayer(iPlayer).getNumCities() == 1):
                        self.setStability(iPlayer, self.getStability(iPlayer) + 1 )
			gc.getPlayer(iPlayer).changeStability(1) # test DLL
                        #print("Stability - capital built", iPlayer)
                if (gc.getPlayer(iPlayer).getCivics(5) == con.iResettlement):
                        capital = gc.getPlayer(iPlayer).getCapitalCity()
                        iDistance = utils.calculateDistance(x, y, capital.getX(), capital.getY())
                        if (iDistance >= 15):
                                self.setStability(iPlayer, self.getStability(iPlayer) + 2 )
				gc.getPlayer(iPlayer).changeStability(2) # test DLL
                                #print("Stability - civic 6th column resettlement", iPlayer)
                self.setParameter(iPlayer, iParExpansionE, True, self.getStability(iPlayer) - iTempExpansionThreshold) 
                             


        def onCityAcquired(self, owner, playerType, city, bConquest, bTrade):

                iGameTurn = gc.getGame().getGameTurn()
                if (owner < con.iNumPlayers):
                        iTotalCityLostModifier = 0                        
                        if (bTrade and (iGameTurn == getTurnForYear(con.tBirth[playerType]) or iGameTurn == getTurnForYear(con.tBirth[playerType])+1 or iGameTurn == getTurnForYear(con.tBirth[playerType])+2)):
                                iTotalCityLostModifier = 3 #during a civ birth
                                if (not gc.getPlayer(owner).isHuman()):
                                        iTotalCityLostModifier += 1
                        elif (bTrade and playerType == self.getRebelCiv() and iGameTurn == self.getLatestRebellionTurn(playerType)):
                                iTotalCityLostModifier = 2 #during a civ resurrection
                        else:
                                iTotalCityLostModifier = max(-5,(16 - gc.getPlayer(owner).getNumCities())/2) #conquering 40 cities and immediately releasing them is an exploit - cap added
                                if (bTrade):                                        
                                        iTotalCityLostModifier += 2
                                        #self.setParameter(owner, iParDiplomacyE, True, -1)
                                        if (gc.getPlayer(owner).isHuman()): #anti-exploit
                                                if (city.isOccupation()):
                                                        self.setStability(owner, self.getStability(owner) - 3 )
							gc.getPlayer(owner).changeStability(-3) # test DLL
                                                        self.setParameter(owner, iParDiplomacyE, True, -3)
                                                        self.setStability(playerType, self.getStability(playerType) + 3 )
							gc.getPlayer(playerType).changeStability(3) # test DLL
                                                        self.setParameter(playerType, iParDiplomacyE, True, +3) 
                                if (city.getX() == tCapitals[utils.getReborn(owner)][owner][0] and city.getY() == tCapitals[utils.getReborn(owner)][owner][1]):
                                        iTotalCityLostModifier += 20
                                if (playerType == con.iBarbarian or playerType == con.iCeltia or playerType == con.iSeljuks):
                                        iTotalCityLostModifier += 1                        
                        self.setParameter(owner, iParExpansionE, True, -iTotalCityLostModifier) 
                        self.setStability(owner, self.getStability(owner) - iTotalCityLostModifier )
			gc.getPlayer(owner).changeStability(-iTotalCityLostModifier) # test DLL
                        #print("Stability - city lost", iTotalCityLostModifier, owner)
                        
                if (playerType < con.iNumPlayers):
                        iTempExpansionThreshold = self.getStability(playerType)
                        if (iGameTurn == getTurnForYear(con.tBirth[playerType]) or iGameTurn == getTurnForYear(con.tBirth[playerType])+1 or iGameTurn == getTurnForYear(con.tBirth[playerType])+2):
                                self.setStability(playerType, self.getStability(playerType) + 3)
				gc.getPlayer(playerType).changeStability(3) # test DLL
                        elif (owner >= con.iNumPlayers):
                                self.setStability(playerType, self.getStability(playerType) + max(0,min(5,(12 - gc.getPlayer(playerType).getNumCities())/2)) )
				gc.getPlayer(playerType).changeStability(max(0, min(5, (12 - gc.getPlayer(playerType).getNumCities())/2))) # test DLL
                        else:
                                self.setStability(playerType, self.getStability(playerType) + max(0,min(5,(12 - gc.getPlayer(playerType).getNumCities())/2)) )
				gc.getPlayer(playerType).changeStability(max(0, min(5, (12 - gc.getPlayer(playerType).getNumCities())/2))) # test DLL
                        #print("Stability - city acquired", playerType)
                        #Persian UP
                        if (playerType == con.iPersia and utils.getReborn(playerType) == 0 and gc.getPlayer(playerType).getCivics(5) != con.iOccupation):
                                if (bConquest):                                
                                        self.setStability(playerType, self.getStability(playerType) + 2)
					gc.getPlayer(playerType).changeStability(2) # test DLL
                        
                        if (gc.getPlayer(playerType).getCivics(5) == con.iOccupation):
                                if (bConquest):
                                        self.setStability(playerType, self.getStability(playerType) + 2 )
					gc.getPlayer(playerType).changeStability(2) # test DLL
                                        #print("iNewBaseStability civic 6th column occupation",playerType)
                        if (owner < con.iNumPlayers):
                                if (city.getX() == tCapitals[utils.getReborn(owner)][owner][0] and city.getY() == tCapitals[utils.getReborn(owner)][owner][1]):
                                        self.setStability(playerType, self.getStability(playerType) + 3)
					gc.getPlayer(playerType).changeStability(3) # test DLL
                                        #print("Stability - capital city acquired", playerType)
                        self.setParameter(playerType, iParExpansionE, True, self.getStability(playerType) - iTempExpansionThreshold) 
                            

                
     


        def onCityRazed(self, iOwner, playerType, city):
            
                if (iOwner < con.iNumPlayers):      
                        self.setStability(iOwner, self.getStability(iOwner) - 3 )
			gc.getPlayer(iOwner).changeStability(-3) # test DLL
                        #print("Stability - city razed", -3, iOwner)
                        self.setParameter(iOwner, iParExpansionE, True, - 3)

                if (playerType < con.iNumPlayers):
                        iTempExpansionThreshold = self.getStability(playerType)                 
                        if (gc.getPlayer(playerType).getCivics(5) == con.iOccupation):
                                self.setStability(playerType, self.getStability(playerType) - 2 ) #balance the +2 and makes 0 for city razed
				gc.getPlayer(playerType).changeStability(-2) # test DLL
                        self.setParameter(playerType, iParExpansionE, True, self.getStability(playerType) - iTempExpansionThreshold) 


                                                
        def onImprovementDestroyed(self, owner):

                if (owner < con.iNumPlayers and owner >= 0):
                        pass
                        #self.setStability(owner, self.getStability(owner) - 1 )
                        ##print("Stability - improvement destroyed", owner)


        def onTechAcquired(self, iTech, iPlayer):

                iTempCivicsThreshold = self.getStability(iPlayer)

                if (iTech == con.iMonotheism or \
                    #iTech == con.iCivilService or \
                    iTech == con.iNationalism or \
                    iTech == con.iConstitution or \
                    #iTech == con.iLiberalism or \ #already in base stability count
                    #iTech == con.iDemocracy or \ #already in base stability count
                    iTech == con.iFascism or \
                    iTech == con.iCommunism or \
                    iTech == con.iPhilosophy or \
                    #iTech == con.iAstronomy or \
                    iTech == con.iFission or \
                    #iTech == con.iFlight or \
                    iTech == con.iGenetics or \
                    iTech == con.iGunpowder or \
                    iTech == con.iSteamPower or \
                    #iTech == con.iRailroad or \
                    iTech == con.iIndustrialism or \
                    iTech == con.iRocketry):
                        self.setStability(iPlayer, self.getStability(iPlayer) - 2 )
			gc.getPlayer(iPlayer).changeStability(-2) # test DLL
                        #print("Stability - tech acquired --", iTech, iPlayer)
                elif (iTech == con.iTheology or \
                    iTech == con.iFeudalism or \
                    iTech == con.iArchery or \
                    iTech == con.iHorsebackRiding or \
                    iTech == con.iBronzeWorking or \
                    iTech == con.iIronWorking or \
                    iTech == con.iRifling or \
                    iTech == con.iAssemblyLine):
                        self.setStability(iPlayer, self.getStability(iPlayer) - 1 )
			gc.getPlayer(iPlayer).changeStability(-1) # test DLL
                        #print("Stability - tech acquired -", iTech, iPlayer)                        
                elif (iTech == con.iMysticism  or \
                    iTech == con.iMeditation or \
                    iTech == con.iPriesthood or \
                    iTech == con.iMonarchy or \
                    iTech == con.iLiterature or \
                    iTech == con.iCodeOfLaws or \
                    iTech == con.iDivineRight or \
                    iTech == con.iMilitaryTradition or \
                    iTech == con.iFishing or \
                    iTech == con.iAgriculture or \
                    iTech == con.iPottery or \
                    iTech == con.iWriting or \
                    iTech == con.iAlphabet or \
                    iTech == con.iCalendar or \
                    iTech == con.iCurrency or \
                    iTech == con.iBanking or \
                    iTech == con.iEducation or \
                    iTech == con.iPrintingPress or \
                    iTech == con.iBiology or \
                    iTech == con.iMedicine or \
                    iTech == con.iElectricity or \
                    iTech == con.iFiberOptics or \
                    iTech == con.iMining or \
                    iTech == con.iMasonry or \
                    iTech == con.iConstruction or \
                    iTech == con.iMachinery or \
                    iTech == con.iEngineering or \
                    iTech == con.iRefrigeration):
                        self.setStability(iPlayer, self.getStability(iPlayer) + 1 )
			gc.getPlayer(iPlayer).changeStability(1) # test DLL
                        #print("Stability - tech acquired +", iTech, iPlayer)
                else:
                        #self.setStability(iPlayer, self.getStability(iPlayer) + 1 )
                        #print("Stability - tech acquired =", iTech, iPlayer)
                        pass

                if (iTech == con.iCompass or iTech == con.iAstronomy):
                        if (not gc.getPlayer(iPlayer).isHuman()):
                                if (iPlayer == con.iSpain or \
                                    iPlayer == con.iFrance or \
                                    iPlayer == con.iEngland or \
                                    iPlayer == con.iNetherlands or \
                                    iPlayer == con.iPortugal):
                                        self.setStability(iPlayer, self.getStability(iPlayer) + 3 ) #need them alive for accurate colonization
					gc.getPlayer(iPlayer).changeStability(3) # test DLL
                                        print ("stability bonus for colonizers", iPlayer)
                if (iTech == con.iAstronomy or iTech == con.iMilitaryTradition):
                        if (not gc.getPlayer(iPlayer).isHuman()):
                                if (iPlayer == con.iGermany or \
                                    iPlayer == con.iRussia):
                                        self.setStability(iPlayer, self.getStability(iPlayer) + 2 )
					gc.getPlayer(iPlayer).changeStability(2) # test DLL

                self.setParameter(iPlayer, iParCivicsE, True, self.getStability(iPlayer) - iTempCivicsThreshold)

        def onBuildingBuilt(self, iPlayer, iBuilding, city):

                iTempCitiesThreshold = self.getStability(iPlayer)
                if (iBuilding == con.iPalace): #palace
                        self.setStability(iPlayer, self.getStability(iPlayer) - 10 )
			gc.getPlayer(iPlayer).changeStability(-10) # test DLL
                        #print("Stability - palace built", iPlayer)
                elif (iBuilding > con.iPalace and iBuilding <= con.iForbiddenPalace): #palaces
                        self.setStability(iPlayer, self.getStability(iPlayer) + 5 )
			gc.getPlayer(iPlayer).changeStability(5) # test DLL
                        #print("Stability - palace built", iPlayer)
                elif (iBuilding >= con.iHeroicEpic and iBuilding <= con.iOlympicPark): #wonder
                        self.setStability(iPlayer, self.getStability(iPlayer) + 1 )
			gc.getPlayer(iPlayer).changeStability(1) # test DLL
                        #print("Stability - wonder built", iPlayer)
                        if (self.getGreatDepressionCountdown(iPlayer) >= 2):
                                self.setGreatDepressionCountdown(iPlayer, self.getGreatDepressionCountdown(iPlayer)-2)
                                #print("Stability - Great Depression reduced", iPlayer)
                elif (iBuilding == con.iJail or iBuilding == con.iIndianMausoleum): #jail
                        if (self.getStability(iPlayer) < 20):
                                if (gc.getPlayer(iPlayer).getCivics(2) == con.iTotalitarianism): #Totalitarianism
                                        self.setStability(iPlayer, self.getStability(iPlayer) + 2 )
					gc.getPlayer(iPlayer).changeStability(2) # test DLL
                                else:
                                        self.setStability(iPlayer, self.getStability(iPlayer) + 1 )
					gc.getPlayer(iPlayer).changeStability(1) # test DLL
                        #print("Stability - jail built", iPlayer)
                elif (iBuilding == con.iCourthouse or iBuilding == con.iAztecSacrificialAltar or iBuilding == con.iSumerianZiggurat): #courthouse
                        if (not city.hasBuilding(con.iPalace) and not city.hasBuilding(con.iForbiddenPalace) and not city.hasBuilding(con.iSummerPalace)):
                                if (self.getStability(iPlayer) < 0):
                                        self.setStability(iPlayer, self.getStability(iPlayer) + 1 )
					gc.getPlayer(iPlayer).changeStability(1) # test DLL
                                        #print("Stability - courthouse built", iPlayer)
                elif (iBuilding == con.iInterpol):
                        if (self.getStability(iPlayer) < 20):
                                self.setStability(iPlayer, self.getStability(iPlayer) + 2 )
				gc.getPlayer(iPlayer).changeStability(2) # test DLL
                elif (iBuilding == con.iNationalSecurity):
                        if (self.getStability(iPlayer) < -10):
                                self.setStability(iPlayer, self.getStability(iPlayer) + 1 )
				gc.getPlayer(iPlayer).changeStability(1) # test DLL
                elif (iBuilding == con.iIntelligenceAgency):
                        if (self.getStability(iPlayer) < -40):
                                self.setStability(iPlayer, self.getStability(iPlayer) + 1 )
				gc.getPlayer(iPlayer).changeStability(1) # test DLL

                self.setParameter(iPlayer, iParCitiesE, True, self.getStability(iPlayer) - iTempCitiesThreshold)

                    


                            
        def onProjectBuilt(self, iPlayer, iProject):
            
                if (iProject <= con.iApolloProgram ): #no SS parts
                        self.setStability(iPlayer, self.getStability(iPlayer) + 1 )
                        self.setParameter(iPlayer, iParCitiesE, True, 2)
                        #print("Stability - project built", iPlayer)
                #pass




        def onCombatResult(self, argsList):

                pWinningUnit,pLosingUnit = argsList
                iWinningPlayer = pWinningUnit.getOwner()
                iLosingPlayer = pLosingUnit.getOwner()

                if (iWinningPlayer < con.iNumPlayers):  
                        self.setCombatResultTempModifier(iWinningPlayer, self.getCombatResultTempModifier(iWinningPlayer) + 1 )
			gc.getPlayer(iWinningPlayer).changeCombatResultTempModifier(1) # test DLL
                        #print("Stability - iWinningPlayer", self.getCombatResultTempModifier(iWinningPlayer), iWinningPlayer)
                if (iLosingPlayer < con.iNumPlayers):  
                        self.setCombatResultTempModifier(iLosingPlayer, self.getCombatResultTempModifier(iLosingPlayer) - 2 )
			gc.getPlayer(iLosingPlayer).changeCombatResultTempModifier(-2) # test DLL
                        #print("Stability - iLosingPlayer", self.getCombatResultTempModifier(iLosingPlayer), iLosingPlayer)


        def onReligionFounded(self, iPlayer):

                self.setStability(iPlayer, self.getStability(iPlayer) - 2 )
		gc.getPlayer(iPlayer).changeStability(2) # test DLL
                self.setParameter(iPlayer, iParCitiesE, True, -2)
                #print("Stability - onReligionFounded", iPlayer)


        def onCorporationFounded(self, iPlayer):

                self.setStability(iPlayer, self.getStability(iPlayer) - 2 )
		gc.getPlayer(iPlayer).changeStability(-2) # test DLL
                self.setParameter(iPlayer, iParCitiesE, True, -2)
                #print("Stability - onCorporationFounded", iPlayer)
		
	def onVassalState(self, iVassal, bCapitulated):
		if iVassal == con.iByzantium: return
	
		if bCapitulated and self.getStability(iVassal) < -10:
			self.setStability(iVassal, -10)
			gc.getPlayer(iVassal).setStability(-10)


        def onReligionSpread(self, iReligion, iPlayer):

                if (iPlayer < iNumPlayers):  
                        pPlayer = gc.getPlayer(iPlayer)
                        if (pPlayer.getStateReligion() != iReligion):
                                for iLoopCiv in range(iNumPlayers):
                                        if (gc.getTeam(pPlayer.getTeam()).isAtWar(iLoopCiv)):
                                                if (gc.getPlayer(iLoopCiv).getStateReligion() == iReligion):
                                                        self.setStability(iPlayer, self.getStability(iPlayer) - 1 )
							gc.getPlayer(iPlayer).changeStability(-1) # test DLL
                                                        self.setParameter(iPlayer, iParCitiesE, True, -1)
                                                        #print("Stability - onReligionSpread", iPlayer)
                                                        break

       	
        def checkImplosion(self, iGameTurn):
    
                if (iGameTurn > getTurnForYear(-350) and iGameTurn % utils.getTurns(8) == 4): # Leoreth: changed from x % 10 == 5
			lCollapsingCivs = []
			
			for iPlayer in range(iNumPlayers):
				if gc.getPlayer(iPlayer).isAlive() and iGameTurn >= getTurnForYear(con.tBirth[iPlayer]) + utils.getTurns(25) and iGameTurn >= gc.getPlayer(iPlayer).getLatestRebellionTurn() + utils.getTurns(10) and not gc.getPlayer(iPlayer).isGoldenAge():
					if self.getStability(iPlayer) < -40:
						lCollapsingCivs.append((iPlayer, self.getStability(iPlayer)))
						
			if len(lCollapsingCivs) == 0: return
						
			lCollapsingCivs.sort(key=itemgetter(1), reverse=False)
			
			iCollapsingCiv = lCollapsingCivs[0][0]
			
			if iCollapsingCiv != utils.getHumanID():
				if gc.getPlayer(utils.getHumanID()).canContact(iCollapsingCiv):
                                                        	CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, gc.getPlayer(iCollapsingCiv).getCivilizationDescription(0) + " " + \
                                                        	                                    CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
				if iGameTurn < getTurnForYear(1400):
					utils.pickFragmentation(iCollapsingCiv, iIndependent, iIndependent2, iBarbarian, False)
				else:
					utils.pickFragmentation(iCollapsingCiv, iIndependent, iIndependent2, -1, False)
			else:
				if gc.getPlayer(iCollapsingCiv).getNumCities() > -1:
					CyInterface().addMessage(iCollapsingCiv, True, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR_HUMAN", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
					utils.pickFragmentation(iCollapsingCiv, iIndependent, iIndependent2, -1, True)
					utils.setStartingStabilityParameters(iCollapsingCiv)
					self.setGNPold(iCollapsingCiv, 0)
					self.setGNPnew(iCollapsingCiv, 0)
				
					
		
                        #for iPlayer in range(iNumPlayers):
                        #        if (gc.getPlayer(iPlayer).isAlive() and iGameTurn >= getTurnForYear(con.tBirth[iPlayer]) + utils.getTurns(25) and not gc.getPlayer(iPlayer).isGoldenAge()):
                        #                if (self.getStability(iPlayer) < -40): #civil war
						#if iPlayer == con.iByzantium and gc.getPlayer(iPlayer).getCapitalCity().getX() == con.tCapitals[0][iPlayer][0] and gc.getPlayer(iPlayer).getCapitalCity().getY() == con.tCapitals[0][iPlayer][1] and gc.getPlayer(con.iByzantium).getCurrentEra() <= 2:
						#	print "Byzantine Collapse prevented by UP, foreign cities secede"
						#	secedingCities = []
						#	citylist = PyPlayer(iPlayer).getCityList()
						#	for pCity in citylist:
						#		if gc.getPlayer(iPlayer).getSettlersMaps(67-pCity.getY(),pCity.getX()) < 90:
						#			secedingCities.append(pCity)
						#	for pCity in secedingCities:
						#		iNewCiv = con.iIndependent + (pCity.getX() % 2)
                                                #		utils.cultureManager((pCity.getX(),pCity.getY()), 50, iNewCiv, iPlayer, False, True, True)
                                                #		utils.flipUnitsInCityBefore((pCity.getX(),pCity.getY()), iNewCiv, iPlayer)
						#                sd.scriptDict['tempFlippingCity'] = (pCity.getX(),pCity.getY())                            
                                                #		utils.flipCity((pCity.getX(),pCity.getY()), 0, 0, iNewCiv, [iPlayer])   #by trade because by conquest may raze the city
                                                #		utils.flipUnitsInCityAfter(sd.scriptDict['tempFlippingCity'], iNewCiv)
                                                #		if (iPlayer == utils.getHumanID()):
                                                #        		CyInterface().addMessage(iPlayer, True, con.iDuration, pCity.getName() + " " + \
                                                #                                           		CyTranslator().getText("TXT_KEY_STABILITY_SECESSION", ()), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
                                                #		#print ("SECESSION", gc.getPlayer(iPlayer).getCivilizationAdjective(0), splittingCity.getName()) #causes c++ exception??
                                                #		utils.setStability(iPlayer, utils.getStability(iPlayer) + 2) #to counterbalance the stability hit on city acquired event, leading to a chain reaction
						#else:
                        #                        print ("COLLAPSE: CIVIL WAR", gc.getPlayer(iPlayer).getCivilizationAdjective(0))
                        #                        if (iPlayer != utils.getHumanID()):
                        #                        	if (gc.getPlayer(utils.getHumanID()).canContact(iPlayer)):
                        #                                	CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, gc.getPlayer(iPlayer).getCivilizationDescription(0) + " " + \
                        #                                	                                    CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
                        #                        	if (iGameTurn < getTurnForYear(1400)):
                        #                                	utils.pickFragmentation(iPlayer, iIndependent, iIndependent2, iBarbarian, False)
                        #                        	else:
                        #                                	utils.pickFragmentation(iPlayer, iIndependent, iIndependent2, -1, False)
                        #                        else:
                        #                        	if (gc.getPlayer(iPlayer).getNumCities() > 1):
                        #                                	CyInterface().addMessage(iPlayer, True, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR_HUMAN", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
                        #                                	utils.pickFragmentation(iPlayer, iIndependent, iIndependent2, -1, True)
                        #                                	utils.setStartingStabilityParameters(iPlayer)
                        #                                	self.setGNPold(iPlayer, 0)
                        #                                	self.setGNPnew(iPlayer, 0)
                        #                                        
                        #                        return






