# Rhye's and Fall of Civilization - Historical Victory Goals


from CvPythonExtensions import *
import CvUtil
import PyHelpers   
#import Popup
#import cPickle as pickle
import Consts as con
from StoredData import sd #edead
import RFCUtils
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
iNumTotalPlayersB = con.iNumTotalPlayersB

iPlague = con.iPlague

iDuration = 6
iImmunity = con.iImmunity

#iHuman = utils.getHumanID()

class Plague:


##################################################
### Secure storage & retrieval of script data ###
################################################   


        def getPlagueCountdown( self, iCiv ):
                return sd.scriptDict['lPlagueCountdown'][iCiv]

        def setPlagueCountdown( self, iCiv, iNewValue ):
                sd.scriptDict['lPlagueCountdown'][iCiv] = iNewValue

        def getGenericPlagueDates( self, i ):
                return sd.scriptDict['lGenericPlagueDates'][i]

        def setGenericPlagueDates( self, i, iNewValue ):
                sd.scriptDict['lGenericPlagueDates'][i] = iNewValue
                
        def getFirstContactPlague( self, iCiv ):
                return sd.scriptDict['lFirstContactPlague'][iCiv]

        def setFirstContactPlague( self, iCiv, bNewValue ):
                sd.scriptDict['lFirstContactPlague'][iCiv] = bNewValue


#######################################
### Main methods (Event-Triggered) ###
#####################################  


        def setup(self):

                for i in range(iNumMajorPlayers):
                        self.setPlagueCountdown(i, -utils.getTurns(iImmunity)) 
##                self.setGenericPlagueDates(0, 100 + gc.getGame().getSorenRandNum(30, 'Variation') - 15) #-400 ca
##                self.setGenericPlagueDates(1, 150 + gc.getGame().getSorenRandNum(30, 'Variation') - 15) #600 ca
##                self.setGenericPlagueDates(2, 225 + gc.getGame().getSorenRandNum(30, 'Variation') - 15) #1340
##                self.setGenericPlagueDates(3, 277 + gc.getGame().getSorenRandNum(30, 'Variation') - 15) #1630
##                self.setGenericPlagueDates(4, 340 + gc.getGame().getSorenRandNum(30, 'Variation') - 15) #1850 ca
                if utils.getScenario() == con.i3000BC:  #late start condition
                        self.setGenericPlagueDates(0, getTurnForYear(400) + gc.getGame().getSorenRandNum(40, 'Variation') - 20) #turn 170
                else:
                        self.setGenericPlagueDates(0, 80) #safe value
                self.setGenericPlagueDates(1, getTurnForYear(1300) + gc.getGame().getSorenRandNum(40, 'Variation') - 20) #turn 250
                self.setGenericPlagueDates(2, getTurnForYear(1650) + gc.getGame().getSorenRandNum(40, 'Variation') - 20) #turn 315
                self.setGenericPlagueDates(3, getTurnForYear(1850) + gc.getGame().getSorenRandNum(40, 'Variation') - 20) #turn 380

                undoPlague = gc.getGame().getSorenRandNum(8, 'undo')
                if (undoPlague <= 3):
                        self.setGenericPlagueDates(undoPlague, -1)

            
        def checkTurn(self, iGameTurn):

                for i in range(iNumTotalPlayersB):
                        if (gc.getPlayer(i).isAlive()):
                                if (self.getPlagueCountdown(i) > 0):                                        
                                        self.setPlagueCountdown(i, self.getPlagueCountdown(i)-1)
                                        #print ("plague countdown", i, self.getPlagueCountdown(i))
                                        if (self.getPlagueCountdown(i) == 2):
                                                self.preStopPlague(i)
                                        if (self.getPlagueCountdown(i) == 0):
                                                self.stopPlague(i)
                                elif (self.getPlagueCountdown(i) < 0):
                                        self.setPlagueCountdown(i, self.getPlagueCountdown(i)+1)

                for i in range(4):
                        if (iGameTurn == self.getGenericPlagueDates(i)):
                                #print ("new plague")
                                self.startPlague(i)
                        if (i >= 1):
                                #retry if the epidemic is dead too quickly
                                if (iGameTurn == self.getGenericPlagueDates(i) + 4):
                                        iInfectedCounter = 0
                                        for j in range(iNumTotalPlayersB):
                                                if (self.getPlagueCountdown(j) > 0):
                                                        iInfectedCounter += 1
                                        if (iInfectedCounter == 1):
                                                #print ("new plague again1")
                                                self.startPlague(i)
                        if (i == 2 or i == 3):
                                if (iGameTurn == self.getGenericPlagueDates(i) + 8):
                                        iInfectedCounter = 0
                                        for j in range(iNumTotalPlayersB):
                                                if (self.getPlagueCountdown(j) > 0):
                                                        iInfectedCounter += 1
                                        if (iInfectedCounter <= 2):
                                                #print ("new plague again2")
                                                self.startPlague(i)

        def checkPlayerTurn(self, iGameTurn, iPlayer):

                if (iPlayer < iNumTotalPlayersB):
                        if (self.getPlagueCountdown(iPlayer) > 0):
                                self.processPlague(iPlayer)
                                
                
                            

        def startPlague(self, iPlagueCounter):
    
                iWorstCiv = -1
                iWorstHealth = 200
                for i in range(iNumMajorPlayers):
                        pPlayer = gc.getPlayer(i)
                        if (pPlayer.isAlive()):
                                if (self.isVulnerable(i) == True):
                                        iHealth = -30
                                        iHealth2 = iHealth/2
                                        if (pPlayer.calculateTotalCityHealthiness() > 0):
                                                iHealth = int((1.0 * pPlayer.calculateTotalCityHealthiness()) / (pPlayer.calculateTotalCityHealthiness() + \
                                                        pPlayer.calculateTotalCityUnhealthiness()) * 100) - 60
                                                iHealth2 = iHealth/2
                                                iHealth2 += gc.getGame().getSorenRandNum(40, 'random modifier')
                                                #print ("starting plague", "civ:", i, "iHealth:", iHealth, iHealth2)
                                                if (iPlagueCounter == 2): #medieval black death
                                                        if (i in con.lCivGroups[0]):
                                                               iHealth2 -= 5 
                                        if (iHealth2 < iWorstHealth):
                                                iWorstHealth = iHealth2
                                                iWorstCiv = i
                if (iWorstCiv != -1):
                        print ("worstCiv", iWorstCiv)
                        pWorstCiv = gc.getPlayer(iWorstCiv)
                        city = utils.getRandomCity(iWorstCiv)
                        if (city != -1):                                
                                self.spreadPlague(iWorstCiv)
                                self.infectCity(city)
                                iHuman = utils.getHumanID()
                                if (gc.getPlayer(iHuman).canContact(iWorstCiv) and iHuman != iWorstCiv):
                                        CyInterface().addMessage(iHuman, True, con.iDuration, CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ()) + " " + city.getName() + " (" + gc.getPlayer(city.getOwner()).getCivilizationAdjective(0) + ")!", "AS2D_PLAGUE", 0, "", ColorTypes(con.iLime), -1, -1, True, True)


        def preStopPlague(self, iPlayer):

                cityList = []
                apCityList = PyPlayer(iPlayer).getCityList()
                for pCity in apCityList:
                        city = pCity.GetCy()
                        if (city.hasBuilding(iPlague)):
                                cityList.append(city)
                if (len(cityList)):
                        iModifier = 0
                        for city in cityList:                            
                                if (gc.getGame().getSorenRandNum(100, 'roll') > 30 - 5*city.healthRate(False, 0) + iModifier):
                                        city.setHasRealBuilding(iPlague, False)
                                        iModifier += 5 #not every city should quit

        
        def stopPlague(self, iPlayer):

                self.setPlagueCountdown(iPlayer, -utils.getTurns(iImmunity))
                if (self.getFirstContactPlague(iPlayer) == True):
                        self.setPlagueCountdown(iPlayer, -utils.getTurns(iImmunity-30))
                self.setFirstContactPlague(iPlayer, False)
                apCityList = PyPlayer(iPlayer).getCityList()
                for pCity in apCityList:
                        city = pCity.GetCy()
                        city.setHasRealBuilding(iPlague, False)


        def processPlague(self, iPlayer):

                pPlayer = gc.getPlayer(iPlayer)
                #first spread to close locations
                cityList = [] #see below
                apCityList = PyPlayer(iPlayer).getCityList()
                for pCity in apCityList:
                        city = pCity.GetCy()
                        cityList.append(city) #see below
                        if (city.hasBuilding(iPlague)):
                                #print ("plague in city", city.getName())
                                #if (pPlayer.isHuman()):
                                #        CyInterface().addMessage(iPlayer, True, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_PROCESS_CITY", ()) + " " + city.getName(), "AS2D_PLAGUE", 0, "", ColorTypes(con.iLime), -1, -1, True, True)
                                if (city.getPopulation() > 1):
                                        #print("healthRate in city", 35 + 5*city.healthRate(False, 0))
                                        if (gc.getGame().getSorenRandNum(100, 'roll') > 40 + 5*city.healthRate(False, 0)):
                                                city.changePopulation(-1)
                                if (city.isCapital()): #delete in vanilla
                                        if (self.getFirstContactPlague(iPlayer) == False): #don't infect if first contact plague
                                                for iLoopCiv in range(iNumMajorPlayers):
                                                        if (gc.getTeam(pPlayer.getTeam()).isVassal(iLoopCiv) or \
                                                            gc.getTeam(gc.getPlayer(iLoopCiv).getTeam()).isVassal(iPlayer)):
                                                                if (gc.getPlayer(iLoopCiv).getNumCities() > 0): #this check is needed, otherwise game crashes
                                                                        capital = gc.getPlayer(iLoopCiv).getCapitalCity()
                                                                        if (self.isVulnerable(iLoopCiv) == True):
                                                                                if (self.getPlagueCountdown(iPlayer) > 2): #don't spread the last turns
                                                                                        self.spreadPlague(iLoopCiv)
                                                                                        self.infectCity(capital)
                                                                                        #print ("infect master/vassal", city.getName(), "to", capital.getName())
                                for x in range(city.getX()-2, city.getX()+3):
                                        for y in range(city.getY()-2, city.getY()+3):
                                                ##print ("plagueXY", x, y)
                                                pCurrent = gc.getMap().plot( x, y )
                                                if (pCurrent.getOwner() != iPlayer and pCurrent.getOwner() >= 0):
                                                        if (self.getFirstContactPlague(iPlayer) == False): #don't infect if first contact plague
                                                                if (self.getPlagueCountdown(iPlayer) > 2): #don't spread the last turns
                                                                        if (self.isVulnerable(pCurrent.getOwner()) == True):
                                                                                self.spreadPlague(pCurrent.getOwner())
                                                                                self.infectCitiesNear(pCurrent.getOwner(), x, y)
                                                                                #print ("infect foreign near", city.getName())
                                                else:                                                                        
                                                        if (pCurrent.isCity() and not (x == city.getX() and y == city.getY())):
                                                                #print ("is city", x, y)
                                                                cityNear = pCurrent.getPlotCity() 
                                                                if (not cityNear.hasBuilding(iPlague)):
                                                                        if (self.getPlagueCountdown(iPlayer) > 2): #don't spread the last turns
                                                                                self.infectCity(cityNear)
                                                                                #print ("infect near", city.getName(), "to", cityNear.getName())
                                                        else:
                                                                if (x == city.getX() and y == city.getY()):
                                                                        self.killUnitsByPlague(city, pCurrent, 0, 42, 2)
                                                                else:
                                                                        if (pCurrent.isRoute()):
                                                                                self.killUnitsByPlague(city, pCurrent, 10, 35, 0)
                                                                        elif (pCurrent.isWater()):
                                                                                self.killUnitsByPlague(city, pCurrent, 30, 35, 0)
                                                                        else:
                                                                                self.killUnitsByPlague(city, pCurrent, 30, 35, 0)
                                for x in range(city.getX()-3, city.getX()+4):
                                        pCurrent = gc.getMap().plot( x, city.getY()-3 )
                                        if (pCurrent.getOwner() == iPlayer or not pCurrent.isOwned()):
                                                if (not pCurrent.isCity()):
                                                        if (pCurrent.isRoute() or pCurrent.isWater()):
                                                                self.killUnitsByPlague(city, pCurrent, 30, 35, 0)
                                        pCurrent = gc.getMap().plot( x, city.getY()+3 )
                                        if (pCurrent.getOwner() == iPlayer or not pCurrent.isOwned()):
                                                if (not pCurrent.isCity()):
                                                        if (pCurrent.isRoute() or pCurrent.isWater()):
                                                                self.killUnitsByPlague(city, pCurrent, 30, 35, 0)                                        
                                for y in range(city.getY()-2, city.getY()+3):
                                        pCurrent = gc.getMap().plot( city.getX()-3, y )
                                        if (pCurrent.getOwner() == iPlayer or not pCurrent.isOwned()):
                                                if (not pCurrent.isCity()):
                                                        if (pCurrent.isRoute() or pCurrent.isWater()):
                                                                self.killUnitsByPlague(city, pCurrent, 30, 35, 0)
                                        pCurrent = gc.getMap().plot( city.getX()+3, y )
                                        if (pCurrent.getOwner() == iPlayer or not pCurrent.isOwned()):
                                                if (not pCurrent.isCity()):
                                                        if (pCurrent.isRoute() or pCurrent.isWater()):
                                                                self.killUnitsByPlague(city, pCurrent, 30, 35, 0)


                                            
                                if (self.getFirstContactPlague(iPlayer) == False): #don't infect if first contact plague  
                                        #spread to trade route cities
                                        if (self.getPlagueCountdown(iPlayer) > 2): #don't spread the last turns
                                                for i in range(city.getTradeRoutes()):                      
                                                #for i in range(gc.getDefineINT("MAX_TRADE_ROUTES")):
                                                        loopCity = city.getTradeCity(i)
                                                        if (not loopCity.isNone()):
                                                                if (not loopCity.hasBuilding(iPlague)):
                                                                        iOwner = loopCity.getOwner()
                                                                        if (iPlayer == iOwner or gc.getTeam(pPlayer.getTeam()).isOpenBorders(iOwner) or \
                                                                            gc.getTeam(pPlayer.getTeam()).isVassal(iOwner) or \
                                                                            gc.getTeam(gc.getPlayer(iOwner).getTeam()).isVassal(iPlayer)): #own city, or open borders, or vassal                                                    
                                                                                if (iPlayer != iOwner):
                                                                                        if (self.isVulnerable(iOwner) == True):
                                                                                                self.spreadPlague(iOwner)
                                                                                                self.infectCity(loopCity)
                                                                                                #print ("infect by trade route", city.getName(), "to", loopCity.getName())                                                                                                
                                                                                                iHuman = utils.getHumanID()
                                                                                                if (gc.getPlayer(iHuman).canContact(iOwner) and iHuman != iOwner):
                                                                                                       CyInterface().addMessage(iHuman, True, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ()) + " " + loopCity.getName() + " (" + gc.getPlayer(iOwner).getCivilizationAdjective(0) + ")", "AS2D_PLAGUE", 0, "", ColorTypes(con.iLime), -1, -1, True, True)
                                                                                else:
                                                                                        self.infectCity(loopCity)
                                                                                        #print ("infect by trade route", city.getName(), "to", loopCity.getName())
                                                                                            

                #spread to other cities of the empire
                if (len(cityList)):
                        if (self.getPlagueCountdown(iPlayer) > 2): #don't spread the last turns
                                for city1 in cityList:
                                        ##print ("citylist", city1.getName())
                                        if (not city1.hasBuilding(iPlague)):
                                                for city2 in cityList:
                                                        if (city1 != city2):
                                                                if (city2.hasBuilding(iPlague)):
                                                                        if (city1.isConnectedTo(city2)):
                                                                                ##print ("infect distant", city1.getName(), "to", city2.getName(), utils.calculateDistance(city1.getX(), city1.getY(), city2.getX(), city2.getY()))
                                                                                if (utils.calculateDistance(city1.getX(), city1.getY(), city2.getX(), city2.getY()) <= 6):
                                                                                        #print ("infect distant", city2.getName(), "to", city1.getName())
                                                                                        self.infectCity(city1)
                                                                                        return

       
        def killUnitsByPlague(self, city, pCurrent, baseValue, iDamage, iPreserveDefenders):

                iOwner = city.getOwner()
                pOwner = gc.getPlayer(iOwner)
                teamOwner = gc.getTeam(gc.getPlayer(city.getOwner()).getTeam())
                
                #deadly plague when human player isn't born yet, will speed up the loading
                if (gc.getGame().getGameTurn() < getTurnForYear(con.tBirth[utils.getHumanID()]) + utils.getTurns(20)):
                        iDamage += 10
                        baseValue -= 5
     

                #print (city.getX(), city.getY())
                iNumUnitsInAPlot = pCurrent.getNumUnits()
                #iPreserveHumanDefenders = iPreserveDefenders -1 #human handicap
                iPreserveHumanDefenders = iPreserveDefenders
                iHuman = utils.getHumanID()
                if (iPreserveDefenders > 0): #cities only
                        #handicap for civs distant from human player too
                        if (not pOwner.isHuman()): #if not human and close or at war
                                #iPreserveDefenders -= 1
                                if (teamOwner.isAtWar(iHuman)):
                                        iPreserveDefenders += 2
                                else:
                                        for j in range(len(con.lCivGroups)):                       
                                                if ((iOwner in con.lCivGroups[j]) and (utils.getHumanID() in con.lCivGroups[j])):
                                                       iPreserveDefenders += 1
                                                       break
                if (iNumUnitsInAPlot):                        
                        for j in range(iNumUnitsInAPlot):
                                i = iNumUnitsInAPlot - j - 1
                                unit = pCurrent.getUnit(i)
                                if (gc.getPlayer(unit.getOwner()).isHuman()):
                                        #print ("iPreserveHumanDefenders", iPreserveHumanDefenders)
                                        if (iPreserveHumanDefenders > 0):                                                
                                                if (utils.isDefenderUnit(unit)):
                                                        iPreserveHumanDefenders -= 1
                                                        if (pCurrent.getNumUnits() > iPreserveDefenders):
                                                                pass
                                                        else:
								# Leoreth: keep units at 50% minimum
								if (unit.getDamage() + iDamage - 20 > 50):
									unit.setDamage(50, con.iBarbarian)
								else:
                                                                	unit.setDamage(unit.getDamage() + iDamage - 20, con.iBarbarian)
                                                        #print ("preserve")
                                                        continue
                                else:
                                        if (iPreserveDefenders > 0):
                                                if (utils.isDefenderUnit(unit)):
                                                        iPreserveDefenders -= 1
                                                        if (pCurrent.getNumUnits() > iPreserveDefenders or gc.getTeam(gc.getPlayer(unit.getOwner()).getTeam()).isAtWar(iHuman)):                                                            
                                                                pass
                                                        else:
                                                                # Leoreth: keep units at 50% minimum
								if (unit.getDamage() + iDamage - 20 < 50):
									unit.setDamage(50, con.iBarbarian)
								else:
                                                                	unit.setDamage(unit.getDamage() + iDamage - 20, con.iBarbarian)
                                                        #print ("preserve")
                                                        continue   
                                if (utils.isMortalUnit(unit)):  #another human handicap inside
                                        iThreshold = baseValue + 5*city.healthRate(False, 0)
                                        #print ("iThreshold", iThreshold)

                                        if (teamOwner.isAtWar(iHuman) and iOwner < iNumMajorPlayers):
                                                if (unit.getOwner() == iOwner):
                                                        iDamage *= 3
                                                        iDamage /= 4                       
                                        
                                        if (self.getFirstContactPlague(city.getOwner()) == True):
                                                if (unit.getOwner() in con.lCivBioOldWorld):
                                                        iDamage /= 2                                                        
                                        
                                        if (gc.getGame().getSorenRandNum(100, 'roll') > iThreshold):
                                                
                                                if (iDamage - unit.getExperience()/10 - unit.baseCombatStr()*3/7 >= 100 - unit.getDamage()):
                                                        if (unit.getOwner() != iOwner and gc.getPlayer(unit.getOwner()).isHuman()):
                                                        	CyInterface().addMessage(unit.getOwner(), False, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_PROCESS_UNIT", ()) + " " + city.getName(), "AS2D_PLAGUE", 0, "", ColorTypes(con.iLime), -1, -1, True, True)
                                                #Leoreth: keep units at 50% minimum
						if (unit.getDamage() + iDamage - unit.getExperience()/10 - unit.baseCombatStr()/2 > 50):
							unit.setDamage(50, con.iBarbarian)
						else:
							unit.setDamage(unit.getDamage() + iDamage - unit.getExperience()/10 - unit.baseCombatStr()/2, con.iBarbarian)
                                                #print ("process")
                                                break
            
            

        def infectCity(self, city):
		if city.getOwner() == con.iCongo and gc.getGame().getGameTurnYear() <= 1650: return	# Leoreth: don't let plague mess up the UHV
		elif city.getOwner() == con.iMali and gc.getGame().getGameTurnYear() <= 1500: return	# same for Mali
                #print ("infected", city.getName())
                city.setHasRealBuilding(iPlague, True)
                if (gc.getPlayer(city.getOwner()).isHuman()):
                        CyInterface().addMessage(city.getOwner(), True, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ()) + " " + city.getName() + "!", "AS2D_PLAGUE", 0, "", ColorTypes(con.iLime), -1, -1, True, True)
                for x in range(city.getX()-2, city.getX()+3):
                        for y in range(city.getY()-2, city.getY()+3):
                                pCurrent = gc.getMap().plot( x, y )
				pCurrent.setUpgradeProgress(0)
                                iImprovement = pCurrent.getImprovementType()
                                #if (iImprovement == con.iCottage):
                                #        pCurrent.setImprovementType(-1)
                                #if (iImprovement == con.iHamlet):
                                #        pCurrent.setImprovementType(con.iCottage)
                                #if (iImprovement == con.iVillage):
                                #        pCurrent.setImprovementType(con.iHamlet)
                                if (iImprovement == con.iTown):
                                        pCurrent.setImprovementType(con.iVillage)
                                if (pCurrent.isCity()):
                                        if (x == city.getX() and y == city.getY()):
                                                self.killUnitsByPlague(city, pCurrent, 0, 100, 0)     


        def isVulnerable(self, iPlayer):
                if (iPlayer >= iNumMajorPlayers):
                        if (self.getPlagueCountdown(iPlayer) <= 0 and self.getPlagueCountdown(iPlayer) > -10 ): #more vulnerable
                                return True
                else:                        
                        pPlayer = gc.getPlayer(iPlayer)                        
                        if (self.getPlagueCountdown(iPlayer) == 0): #vulnerable
                        #if (self.getPlagueCountdown(iPlayer) < 0): #debug
                                if (not gc.getTeam(pPlayer.getTeam()).isHasTech(con.iMedicine)):
                                        iHealth = -30
                                        if (pPlayer.calculateTotalCityHealthiness() > 0):
                                                iHealth = int((1.0 * pPlayer.calculateTotalCityHealthiness()) / (pPlayer.calculateTotalCityHealthiness() + \
                                                                pPlayer.calculateTotalCityUnhealthiness()) * 100) - 60
                                        if (iHealth < 14): #no spread for iHealth >= 74 years
                                                return True
                                        else:
                                                #print ("immune", iPlayer)
                                                pass
                return False


        def spreadPlague(self, iPlayer):
                pPlayer = gc.getPlayer(iPlayer)  
                iHealth = -30
                if (pPlayer.calculateTotalCityHealthiness() > 0):
                        iHealth = int((1.0 * pPlayer.calculateTotalCityHealthiness()) / (pPlayer.calculateTotalCityHealthiness() + \
                                      pPlayer.calculateTotalCityUnhealthiness()) * 100) - 60
                iHealth /= 7 #duration range will be -4 to +4 for 30 to 90
                self.setPlagueCountdown(iPlayer, min(9,iDuration - iHealth))
                print ("spreading plague to", iPlayer)


                                               
        def infectCitiesNear(self, iPlayer, startingX, startingY):                
                apCityList = PyPlayer(iPlayer).getCityList()
                for pCity in apCityList:
                        city = pCity.GetCy()
                        if (utils.calculateDistance(city.getX(), city.getY(), startingX, startingY) <= 3):
                                self.infectCity(city)
                                iHuman = utils.getHumanID()
                                if (gc.getPlayer(iHuman).canContact(iPlayer) and iHuman != iPlayer):
                                        CyInterface().addMessage(iHuman, True, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ()) + " " + city.getName() + " (" + gc.getPlayer(iPlayer).getCivilizationAdjective(0) + ")", "AS2D_PLAGUE", 0, "", ColorTypes(con.iLime), -1, -1, True, True)




        def onCityAcquired(self, iOldOwner, iNewOwner, city):
                if (city.hasBuilding(iPlague)):
                        if (self.getFirstContactPlague(iOldOwner) == False): #don't infect if first contact plague
                                if (self.getPlagueCountdown(iNewOwner) <= 0 and gc.getGame().getGameTurn() > getTurnForYear(con.tBirth[iNewOwner]) + utils.getTurns(iImmunity) ): #skip immunity in this case (to prevent expoiting of being immune to conquer weak civs), but not for the new born civs   
                                        if (not gc.getTeam(gc.getPlayer(iNewOwner).getTeam()).isHasTech(con.iMedicine)): #but not permanent immunity
                                                print("acquiring plague")
                                                self.spreadPlague(iNewOwner)
                                                apCityList = PyPlayer(iNewOwner).getCityList()
                                                for pCity in apCityList:
                                                        cityNear = pCity.GetCy()
                                                        if (utils.calculateDistance(city.getX(), city.getY(), cityNear.getX(), cityNear.getY()) <= 3):
                                                                self.infectCity(cityNear)
                                                return
                        city.setHasRealBuilding(iPlague, False)

        def onCityRazed(self, city, iNewOwner):
                if (city.hasBuilding(iPlague)):
                        if (self.getPlagueCountdown(iNewOwner) > 0):
                                apCityList = PyPlayer(iNewOwner).getCityList()
                                iNumCitiesInfected = 0
                                for pCity in apCityList:
                                        otherCity = pCity.GetCy()
                                        if (otherCity.getX() != city.getX() or otherCity.getY() != city.getY()): #because the city razed still has the plague
                                                if (otherCity.hasBuilding(iPlague)):
                                                        iNumCitiesInfected += 1
                                print ("iNumCitiesInfected", iNumCitiesInfected)
                                if (iNumCitiesInfected == 0):
                                        self.setPlagueCountdown(iNewOwner, 0) #undo spreadPlague called in onCityAcquired()
                                            


        def onFirstContact(self, iTeamX, iHasMetTeamY):
                if (gc.getGame().getGameTurn() > getTurnForYear(con.tBirth[con.iAztecs]) + 2 and gc.getGame().getGameTurn() < getTurnForYear(1800)):
                        iOldWorldCiv = -1
                        iNewWorldCiv = -1
                        #if (iTeamX in con.lCivBioOldWorld and iHasMetTeamY in con.lCivBioNewWorld):
                        #        iOldWorldCiv = iTeamX
                        #        iNewWorldCiv = iHasMetTeamY
                        if (iTeamX in con.lCivBioNewWorld and iHasMetTeamY in con.lCivBioOldWorld):
                                iNewWorldCiv = iTeamX
                                iOldWorldCiv = iHasMetTeamY
                        if (iOldWorldCiv != -1 and iNewWorldCiv != -1):
                                pNewWorldCiv = gc.getPlayer(iNewWorldCiv)
                                if (self.getPlagueCountdown(iNewWorldCiv) == 0): #vulnerable
                                        #print ("vulnerable", iNewWorldCiv)
                                        if (not gc.getTeam(pNewWorldCiv.getTeam()).isHasTech(con.iBiology)):
                                                city = utils.getRandomCity(iNewWorldCiv)
                                                if (city != -1): 
                                                        iHealth = -30
                                                        if (pNewWorldCiv.calculateTotalCityHealthiness() > 0):
                                                                iHealth = int((1.0 * pNewWorldCiv.calculateTotalCityHealthiness()) / (pNewWorldCiv.calculateTotalCityHealthiness() + \
                                                                        pNewWorldCiv.calculateTotalCityUnhealthiness()) * 100) - 60
                                                        if (iHealth < 10): #no spread for iHealth >= 70 years
                                                                iHealth /= 10
                                                                if (gc.getGame().getSorenRandNum(100, 'roll') > 30 + 5*iHealth):
                                                                        self.setPlagueCountdown(iNewWorldCiv, iDuration - iHealth)
                                                                        self.setFirstContactPlague(iNewWorldCiv, True)
                                                                        #print ("spreading (through first contact) plague to", iNewWorldCiv)
                                                                        self.infectCity(city)
                                                                        iHuman = utils.getHumanID()
                                                                        if (gc.getPlayer(iHuman).canContact(iNewWorldCiv) and iHuman != iNewWorldCiv):
                                                                                CyInterface().addMessage(iHuman, False, con.iDuration/2, CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ()) + " " + city.getName() + " (" + gc.getPlayer(city.getOwner()).getCivilizationAdjective(0) + ")", "AS2D_PLAGUE", 0, "", ColorTypes(con.iLime), -1, -1, True, True)
      


        def onTechAcquired(self, iTech, iPlayer):
                if (self.getPlagueCountdown(iPlayer) > 1):                                        
                        self.setPlagueCountdown(iPlayer, 1)





