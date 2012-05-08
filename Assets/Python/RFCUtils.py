# Rhye's and Fall of Civilization - Utilities

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
import Consts as con
#import cPickle as pickle
from StoredData import sd

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer


iNumPlayers = con.iNumPlayers
iNumMajorPlayers = con.iNumMajorPlayers
iNumActivePlayers = con.iNumActivePlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iNumTotalPlayers = con.iNumTotalPlayers
iBarbarian = con.iBarbarian

iSettler = con.iSettler

iNumBuildingsPlague = con.iNumBuildingsPlague
iNumBuildingsEmbassy = con.iNumBuildingsEmbassy

tCol = (
'255,255,255',
'200,200,200',
'150,150,150',
'128,128,128')

class RFCUtils:

        #Rise and fall, stability
        def getLastTurnAlive( self, iCiv ):
                return sd.scriptDict['lLastTurnAlive'][iCiv]

        def setLastTurnAlive( self, iCiv, iNewValue ):
                sd.scriptDict['lLastTurnAlive'][iCiv] = iNewValue

        def getCivsWithNationalism( self ):
                return sd.scriptDict['iCivsWithNationalism']

        #Victory
        def getGoal( self, i, j ):
                return sd.scriptDict['lGoals'][i][j]

        def setGoal( self, i, j, iNewValue ):
                sd.scriptDict['lGoals'][i][j] = iNewValue

        #Stability
        
        def getTempFlippingCity( self ):
                return sd.scriptDict['tempFlippingCity']

        def setTempFlippingCity( self, tNewValue ):
                sd.scriptDict['tempFlippingCity'] = tNewValue

        def getStability( self, iCiv ):
                return sd.scriptDict['lStability'][iCiv]

        def setStability( self, iCiv, iNewValue ):
                sd.scriptDict['lStability'][iCiv] = iNewValue

        def getBaseStabilityLastTurn( self, iCiv ):
                return sd.scriptDict['lBaseStabilityLastTurn'][iCiv]

        def setBaseStabilityLastTurn( self, iCiv, iNewValue ):
                sd.scriptDict['lBaseStabilityLastTurn'][iCiv] = iNewValue

        def getStabilityParameters( self, iParameter ):
                return sd.scriptDict['lStabilityParameters'][iParameter]

        def setStabilityParameters( self, iParameter, iNewValue ):
                sd.scriptDict['lStabilityParameters'][iParameter] = iNewValue

        def getGreatDepressionCountdown( self, iCiv ):
                return sd.scriptDict['lGreatDepressionCountdown'][iCiv]

        def setGreatDepressionCountdown( self, iCiv, iNewValue ):
                sd.scriptDict['lGreatDepressionCountdown'][iCiv] = iNewValue
                                
        def getLastRecordedStabilityStuff( self, iParameter ):
                return sd.scriptDict['lLastRecordedStabilityStuff'][iParameter]

        def setLastRecordedStabilityStuff( self, iParameter, iNewValue ):
                sd.scriptDict['lLastRecordedStabilityStuff'][iParameter] = iNewValue
                
        #Plague
        def getPlagueCountdown( self, iCiv ):
                return sd.scriptDict['lPlagueCountdown'][iCiv]

        def setPlagueCountdown( self, iCiv, iNewValue ):
                sd.scriptDict['lPlagueCountdown'][iCiv] = iNewValue

        #Communications
        def getSeed( self ):
                return sd.scriptDict['iSeed']
		
	def setTempEventList( self, lTempEventList ):
		sd.scriptDict['lTempEventList'] = lTempEventList
		
	def getTempEventList( self ):
		return sd.scriptDict['lTempEventList']

#######################################

        #Stability, RiseNFall, CvFinanceAdvisor
        def setParameter(self, iPlayer, iParameter, bPreviousAmount, iAmount):
            if (gc.getPlayer(iPlayer).isHuman()):
                    if (bPreviousAmount):
                            self.setStabilityParameters(iParameter, self.getStabilityParameters(iParameter) + iAmount)
                    else:
                            self.setStabilityParameters(iParameter, 0 + iAmount)

        def setStartingStabilityParameters(self, iCiv):
                iHandicap = gc.getGame().getHandicapType()

                for i in range(con.iNumStabilityParameters):
                        self.setStabilityParameters(i, 0)

                if (iHandicap == 0):
                        self.setStability(iCiv, 20)
			gc.getPlayer(iCiv).setStability(20) # test DLL
                        self.setParameter(iCiv, con.iParCitiesE, True, 4)
                        self.setParameter(iCiv, con.iParCivicsE, True, 4)
                        self.setParameter(iCiv, con.iParDiplomacyE, True, 4)
                        self.setParameter(iCiv, con.iParEconomyE, True, 4)
                        self.setParameter(iCiv, con.iParExpansionE, True, 4) 
                elif (iHandicap == 1):
                        self.setStability(iCiv, 5)
			gc.getPlayer(iCiv).setStability(5) # test DLL
                        self.setParameter(iCiv, con.iParCitiesE, True, 1)
                        self.setParameter(iCiv, con.iParCivicsE, True, 1)
                        self.setParameter(iCiv, con.iParDiplomacyE, True, 1)
                        self.setParameter(iCiv, con.iParEconomyE, True, 1)
                        self.setParameter(iCiv, con.iParExpansionE, True, 1) 
                elif (iHandicap == 2):
                        self.setStability(iCiv, -10)
			gc.getPlayer(iCiv).setStability(-10) # test DLL
                        self.setParameter(iCiv, con.iParCitiesE, True, -2)
                        self.setParameter(iCiv, con.iParCivicsE, True, -2)
                        self.setParameter(iCiv, con.iParDiplomacyE, True, -2)
                        self.setParameter(iCiv, con.iParEconomyE, True, -2)
                        self.setParameter(iCiv, con.iParExpansionE, True, -2) 




        #CvFinanceAdvisor
        def getParCities(self):
            if (self.getStabilityParameters(con.iParCitiesE) > 7):
                    return self.getStabilityParameters(con.iParCities3) + self.getStabilityParameters(con.iParCitiesE) - gc.getActivePlayer().getCurrentEra()
            elif (self.getStabilityParameters(con.iParCitiesE) < -7):
                    return self.getStabilityParameters(con.iParCities3) + self.getStabilityParameters(con.iParCitiesE) + gc.getActivePlayer().getCurrentEra()
            else:
                    return self.getStabilityParameters(con.iParCities3) + self.getStabilityParameters(con.iParCitiesE)

        def getParCivics(self):
            if (self.getStabilityParameters(con.iParCivicsE) > 7):
                    return self.getStabilityParameters(con.iParCivics3) + self.getStabilityParameters(con.iParCivics1) + self.getStabilityParameters(con.iParCivicsE) - gc.getActivePlayer().getCurrentEra()
            elif (self.getStabilityParameters(con.iParCivicsE) < -7):
                    return self.getStabilityParameters(con.iParCivics3) + self.getStabilityParameters(con.iParCivics1) + self.getStabilityParameters(con.iParCivicsE) + gc.getActivePlayer().getCurrentEra()
            else:
                    return self.getStabilityParameters(con.iParCivics3) + self.getStabilityParameters(con.iParCivics1) + self.getStabilityParameters(con.iParCivicsE)

        def getParDiplomacy(self):
            if (self.getStabilityParameters(con.iParDiplomacyE) > 7):
                    return self.getStabilityParameters(con.iParDiplomacy3) + self.getStabilityParameters(con.iParDiplomacyE) - gc.getActivePlayer().getCurrentEra()
            elif (self.getStabilityParameters(con.iParDiplomacyE) < -7):
                    return self.getStabilityParameters(con.iParDiplomacy3) + self.getStabilityParameters(con.iParDiplomacyE) + gc.getActivePlayer().getCurrentEra()
            else:
                    return self.getStabilityParameters(con.iParDiplomacy3) + self.getStabilityParameters(con.iParDiplomacyE)

                
        def getParEconomy(self):
            #print ("ECO", self.getStabilityParameters(con.iParEconomy3), self.getStabilityParameters(con.iParEconomy1), self.getStabilityParameters(con.iParEconomyE))
            if (self.getStabilityParameters(con.iParEconomyE) > 7):
                    return self.getStabilityParameters(con.iParEconomy3) + self.getStabilityParameters(con.iParEconomy1) + self.getStabilityParameters(con.iParEconomyE) - gc.getActivePlayer().getCurrentEra()
            elif (self.getStabilityParameters(con.iParEconomyE) < -7):
                    return self.getStabilityParameters(con.iParEconomy3) + self.getStabilityParameters(con.iParEconomy1) + self.getStabilityParameters(con.iParEconomyE) + gc.getActivePlayer().getCurrentEra()
            else:
                    return self.getStabilityParameters(con.iParEconomy3) + self.getStabilityParameters(con.iParEconomy1) + self.getStabilityParameters(con.iParEconomyE)
                
        def getParExpansion(self):
            if (self.getStabilityParameters(con.iParExpansionE) > 7):
                    return self.getStabilityParameters(con.iParExpansion3) + self.getStabilityParameters(con.iParExpansion1) + self.getStabilityParameters(con.iParExpansionE) - gc.getActivePlayer().getCurrentEra()
            elif (self.getStabilityParameters(con.iParExpansionE) < -7):
                    return self.getStabilityParameters(con.iParExpansion3) + self.getStabilityParameters(con.iParExpansion1) + self.getStabilityParameters(con.iParExpansionE) + gc.getActivePlayer().getCurrentEra()
            else:
                    return self.getStabilityParameters(con.iParExpansion3) + self.getStabilityParameters(con.iParExpansion1) + self.getStabilityParameters(con.iParExpansionE)

        def getArrow(self, iParameter):
            if (iParameter == 0):
                    if (self.getStability(self.getHumanID()) >= self.getLastRecordedStabilityStuff(iParameter) + 6):
                            return 1
                    elif (self.getStability(self.getHumanID()) <= self.getLastRecordedStabilityStuff(iParameter) - 6):
                            return -1
                    else:
                            return 0
            else:
                    if (iParameter == 1):
                            iNewValue = self.getParCities()
                    elif (iParameter == 2):
                            iNewValue = self.getParCivics()
                    elif (iParameter == 3):
                            iNewValue = self.getParEconomy()
                    elif (iParameter == 4):
                            iNewValue = self.getParExpansion()
                    elif (iParameter == 5):
                            iNewValue = self.getParDiplomacy()
                    if (iNewValue >= self.getLastRecordedStabilityStuff(iParameter) + 4):
                            return 1
                    elif (iNewValue <= self.getLastRecordedStabilityStuff(iParameter) - 4):
                            return -1
                    else:
                            return 0

        #Victory
        def countAchievedGoals(self, iPlayer):
                iResult = 0
                for j in range(3):                        
                        #iTemp = self.getGoal(iPlayer, j)
                        #if (iTemp < 0):
                        #        iTemp = 0
                        #iResult += iTemp
                        if (self.getGoal(iPlayer, j) == 1):
                                iResult += 1
                return iResult
                
        def getGoalsColor(self, iPlayer): #by CyberChrist
                iCol = 0
                for j in range(3):
                        if (self.getGoal(iPlayer, j) == 0):
                                iCol += 1
                return tCol[iCol]

            
        #Plague
        def getRandomCity(self, iPlayer):
                cityList = []
                apCityList = PyPlayer(iPlayer).getCityList()
                for pCity in apCityList:
                        cityList.append(pCity.GetCy())
                if (len(cityList)):           
                        return cityList[gc.getGame().getSorenRandNum(len(cityList), 'random city')]
                else:
                        return -1

	# Leoreth - finds an adjacent land plot without enemy units that's closest to the player's capital (for the Roman UP)
	def findNearestLandPlot(self, tPlot, iPlayer):
		x, y = tPlot
		plotList = []

		for i in range(x - 2, x + 3):        
                        for j in range(y - 2, y + 3):	
                                pCurrent = gc.getMap().plot( i, j )
                                if (not pCurrent.isWater() and not pCurrent.isPeak()):
                                        if ( not pCurrent.isUnit() ):
                                                plotList.append(pCurrent)

		#if (len(plotList) > 0):
		#	iDistance = 1000
		#	pCapital = gc.getPlayer(iPlayer).getCapitalCity()
		#	iCapX = pCapital.getX()
		#	iCapY = pCapital.getY()
                #        for plot in plotList:
		#		plotX = plot.getX()
		#		plotY = plot.getY()
		#		iTempDist = self.calculateDistance(iCapX, plotX, iCapY, plotY)
#
		#		if iTempDist < iDistance:
		#			nearestPlot = plot
		#			iDistance = iTempDist

		#	return nearestPlot

                #return (None)

		if (len(plotList) > 0):
                        rndNum = gc.getGame().getSorenRandNum(len(plotList), 'land plot')
                        result = plotList[rndNum]
                        if (result):                                                        
                        	return ((result.getX(), result.getY()))
		# if no plot is found, return that player's capital
                return con.tCapital[iPlayer]



        def isMortalUnit(self, unit):
                if (unit.isHasPromotion(42)): #leader
                        if (not gc.getPlayer(unit.getOwner()).isHuman()):
                                return False
                        else:
                                if (gc.getGame().getSorenRandNum(100, 'random modifier') >= 50):
                                        return False              
                iUnitType = unit.getUnitType()
                if (iUnitType <= con.iKhmerBallistaElephant \
                     and iUnitType != con.iSettler and iUnitType != con.iMechanizedInfantry) or iUnitType == con.iBersagliere or iUnitType == con.iLevy:
                        return True
                if (iUnitType >= con.iCatapult and iUnitType <= con.iMobileArtillery ):
                        if (gc.getPlayer(unit.getOwner()).isHuman()):
                                return True
                        else:
                                if (gc.getGame().getSorenRandNum(100, 'random modifier') >= 30):
                                        return True
                if (iUnitType == con.iSettler ):
                        if (gc.getPlayer(unit.getOwner()).isHuman()):
                                if (gc.getGame().getSorenRandNum(100, 'random modifier') >= 50):
                                        return True
                        else:
                                if (gc.getGame().getSorenRandNum(100, 'random modifier') >= 20):
                                        return True
                return False

        def isDefenderUnit(self, unit):
                iUnitType = unit.getUnitType()
                if (iUnitType >= con.iSpearman and iUnitType <= con.iChinaChokonu):
                        return True
                return False

        #AIWars
        def checkUnitsInEnemyTerritory(self, iCiv1, iCiv2): 
                unitList = PyPlayer(iCiv1).getUnitList()
                if(len(unitList)):
                        for unit in unitList:
                                iX = unit.getX()
                                iY = unit.getY()
                                if (gc.getMap().plot( iX, iY ).getOwner() == iCiv2):
                                        return True
                return False

        #AIWars
        def restorePeaceAI(self, iMinorCiv, bOpenBorders):
                teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
                for iActiveCiv in range( iNumActivePlayers ):
                        if (gc.getPlayer(iActiveCiv).isAlive() and not gc.getPlayer(iActiveCiv).isHuman()):
                                if (teamMinor.isAtWar(iActiveCiv)):
                                        bActiveUnitsInIndependentTerritory = self.checkUnitsInEnemyTerritory(iActiveCiv, iMinorCiv)
                                        bIndependentUnitsInActiveTerritory = self.checkUnitsInEnemyTerritory(iMinorCiv, iActiveCiv)                                                                  
                                        if (not bActiveUnitsInIndependentTerritory and not bIndependentUnitsInActiveTerritory):            
                                                teamMinor.makePeace(iActiveCiv)
                                                if (bOpenBorders):
                                                        teamMinor.signOpenBorders(iActiveCiv)
        #AIWars
        def restorePeaceHuman(self, iMinorCiv, bOpenBorders): 
                teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
                for iActiveCiv in range( iNumActivePlayers ):
                        if (gc.getPlayer(iActiveCiv).isHuman()):
                                if (gc.getPlayer(iActiveCiv).isAlive()):
                                        if (teamMinor.isAtWar(iActiveCiv)):
                                                bActiveUnitsInIndependentTerritory = self.checkUnitsInEnemyTerritory(iActiveCiv, iMinorCiv)
                                                bIndependentUnitsInActiveTerritory = self.checkUnitsInEnemyTerritory(iMinorCiv, iActiveCiv)                                                                  
                                                if (not bActiveUnitsInIndependentTerritory and not bIndependentUnitsInActiveTerritory):            
                                                        teamMinor.makePeace(iActiveCiv)
                                return
        #AIWars
        def minorWars(self, iMinorCiv):
                teamMinor = gc.getTeam(gc.getPlayer(iMinorCiv).getTeam())
                apCityList = PyPlayer(iMinorCiv).getCityList()
                for pCity in apCityList:
                        city = pCity.GetCy()
                        x = city.getX()
                        y = city.getY()
                        for iActiveCiv in range( iNumActivePlayers ):
                                if (gc.getPlayer(iActiveCiv).isAlive() and not gc.getPlayer(iActiveCiv).isHuman()):
                                        if (gc.getPlayer(iActiveCiv).getSettlersMaps( 67-y, x ) >= 90):
                                                if (not teamMinor.isAtWar(iActiveCiv)):
                                                        teamMinor.declareWar(iActiveCiv, False, WarPlanTypes.WARPLAN_LIMITED)
                                                        print ("Minor war", city.getName(), gc.getPlayer(iActiveCiv).getCivilizationAdjective(0))



            
        #RiseAndFall, Stability
        def calculateDistance(self, x1, y1, x2, y2):
                dx = abs(x2-x1)
                dy = abs(y2-y1)
                return max(dx, dy)


            
        #RiseAndFall
        def debugTextPopup(self, strText):
                popup = Popup.PyPopup()
                popup.setBodyString( strText )
                popup.launch()		

        #RiseAndFall
        def updateMinorTechs( self, iMinorCiv, iMajorCiv):                
                for t in range(con.iNumTechs):
                        if (gc.getTeam(gc.getPlayer(iMajorCiv).getTeam()).isHasTech(t)):
                                    gc.getTeam(gc.getPlayer(iMinorCiv).getTeam()).setHasTech(t, True, iMinorCiv, False, False)


        #RiseAndFall, Religions, Congresses, UniquePowers
        def makeUnit(self, iUnit, iPlayer, tCoords, iNum): #by LOQ
                'Makes iNum units for player iPlayer of the type iUnit at tCoords.'
                for i in range(iNum):
                        player = gc.getPlayer(iPlayer)
                        player.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

	def makeUnitAI(self, iUnit, iPlayer, tCoords, iAI, iNum): #by LOQ, modified by Leoreth
                'Makes iNum units for player iPlayer of the type iUnit at tCoords.'
                for i in range(iNum):
                        player = gc.getPlayer(iPlayer)
                        player.initUnit(iUnit, tCoords[0], tCoords[1], iAI, DirectionTypes.DIRECTION_SOUTH)

        #RiseAndFall, Religions, Congresses
        def getHumanID(self):
##                for iCiv in range(iNumPlayers):
##                        if (gc.getPlayer(iCiv).isHuman()):
##                                return iCiv     
                return gc.getGame().getActivePlayer()



        #RiseAndFall
        def flipUnitsInCityBefore(self, tCityPlot, iNewOwner, iOldOwner):
                #print ("tCityPlot Before", tCityPlot)
                plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
                city = plotCity.getPlotCity()    
                iNumUnitsInAPlot = plotCity.getNumUnits()
                j = 0
                for i in range(iNumUnitsInAPlot):                        
                        unit = plotCity.getUnit(j)
                        unitType = unit.getUnitType()
                        if (unit.getOwner() == iOldOwner):
                                unit.kill(False, con.iBarbarian)
                                if (iNewOwner < con.iNumActivePlayers or unitType > con.iSettler):
                                        self.makeUnit(unitType, iNewOwner, [0, 67], 1)
                        else:
                                j += 1
        #RiseAndFall
        def flipUnitsInCityAfter(self, tCityPlot, iCiv):
                #moves new units back in their place
                print ("tCityPlot After", tCityPlot)
                tempPlot = gc.getMap().plot(0,67)
                if (tempPlot.getNumUnits() != 0):
                        iNumUnitsInAPlot = tempPlot.getNumUnits()
                        #print ("iNumUnitsInAPlot", iNumUnitsInAPlot)                        
                        for i in range(iNumUnitsInAPlot):
                                unit = tempPlot.getUnit(0)
                                unit.setXYOld(tCityPlot[0],tCityPlot[1])
                #cover plots revealed
                gc.getMap().plot(0, 67).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(0, 66).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(1, 66).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(1, 67).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(123, 67).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(123, 66).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(2, 67).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(2, 66).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(2, 65).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(1, 65).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(0, 65).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(122, 67).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(122, 66).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(122, 65).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(123, 65).setRevealed(iCiv, False, True, -1);

        def killUnitsInArea(self, tTopLeft, tBottomRight, iCiv):
                for x in range(tTopLeft[0], tBottomRight[0]+1):
                        for y in range(tTopLeft[1], tBottomRight[1]+1):
                                killPlot = gc.getMap().plot(x,y)
                                iNumUnitsInAPlot = killPlot.getNumUnits()
                                if (iNumUnitsInAPlot):
                                        for i in range(iNumUnitsInAPlot):                                                        
                                                unit = killPlot.getUnit(0)
                                                if (unit.getOwner() == iCiv):
                                                        unit.kill(False, con.iBarbarian)

                                                        
        #RiseAndFall
        def flipUnitsInArea(self, tTopLeft, tBottomRight, iNewOwner, iOldOwner, bSkipPlotCity, bKillSettlers):
                """Deletes, recreates units in 0,67 and moves them to the previous tile.
                If there are units belonging to others in that plot and the new owner is barbarian, the units aren't recreated.
                Settlers aren't created.
                If bSkipPlotCity is True, units in a city won't flip. This is to avoid converting barbarian units that would capture a city before the flip delay"""
                for x in range(tTopLeft[0], tBottomRight[0]+1):
                        for y in range(tTopLeft[1], tBottomRight[1]+1):
                                killPlot = gc.getMap().plot(x,y)
                                iNumUnitsInAPlot = killPlot.getNumUnits()
                                if (iNumUnitsInAPlot):
                                        bRevealedZero = False
                                        if (gc.getMap().plot(0, 67).isRevealed(iNewOwner, False)):
                                                bRevealedZero = True
                                        #print ("killplot", x, y)
                                        if (bSkipPlotCity == True) and (killPlot.isCity()):
                                                #print (killPlot.isCity())
                                                #print 'do nothing'
                                                pass
                                        else:
                                                j = 0
                                                for i in range(iNumUnitsInAPlot):                                                        
                                                        unit = killPlot.getUnit(j)
                                                        #print ("killplot", x, y, unit.getUnitType(), unit.getOwner(), "j", j)
                                                        if (unit.getOwner() == iOldOwner):
                                                                unit.kill(False, con.iBarbarian)
                                                                if (bKillSettlers):
                                                                        if ((unit.getUnitType() > iSettler)):
                                                                                self.makeUnit(unit.getUnitType(), iNewOwner, [0, 67], 1)
                                                                else:
                                                                        if ((unit.getUnitType() >= iSettler)): #skip animals
                                                                                self.makeUnit(unit.getUnitType(), iNewOwner, [0, 67], 1)
                                                        else:
                                                                j += 1
                                                tempPlot = gc.getMap().plot(0,67)
                                                #moves new units back in their place
                                                if (tempPlot.getNumUnits() != 0):
                                                        iNumUnitsInAPlot = tempPlot.getNumUnits()
                                                        for i in range(iNumUnitsInAPlot):
                                                                unit = tempPlot.getUnit(0)
                                                                unit.setXYOld(x,y)
                                                        iCiv = iNewOwner
                                                        if (bRevealedZero == False):
                                                                gc.getMap().plot(0, 67).setRevealed(iCiv, False, True, -1);
                                                                gc.getMap().plot(0, 66).setRevealed(iCiv, False, True, -1);
                                                                gc.getMap().plot(1, 66).setRevealed(iCiv, False, True, -1);
                                                                gc.getMap().plot(1, 67).setRevealed(iCiv, False, True, -1);
                                                                gc.getMap().plot(123, 67).setRevealed(iCiv, False, True, -1);
                                                                gc.getMap().plot(123, 66).setRevealed(iCiv, False, True, -1);
                                                                gc.getMap().plot(2, 67).setRevealed(iCiv, False, True, -1);
                                                                gc.getMap().plot(2, 66).setRevealed(iCiv, False, True, -1);
                                                                gc.getMap().plot(2, 65).setRevealed(iCiv, False, True, -1);
                                                                gc.getMap().plot(1, 65).setRevealed(iCiv, False, True, -1);
                                                                gc.getMap().plot(0, 65).setRevealed(iCiv, False, True, -1);
                                                                gc.getMap().plot(122, 67).setRevealed(iCiv, False, True, -1);
                                                                gc.getMap().plot(122, 66).setRevealed(iCiv, False, True, -1);
                                                                gc.getMap().plot(122, 65).setRevealed(iCiv, False, True, -1);
                                                                gc.getMap().plot(123, 65).setRevealed(iCiv, False, True, -1);
                                




        #Congresses, RiseAndFall
        def flipCity(self, tCityPlot, bFlipType, bKillUnits, iNewOwner, iOldOwners):
                """Changes owner of city specified by tCityPlot.
                bFlipType specifies if it's conquered or traded.
                If bKillUnits != 0 all the units in the city will be killed.
                iRetainCulture will determine the split of the current culture between old and new owner. -1 will skip
                iOldOwners is a list. Flip happens only if the old owner is in the list.
                An empty list will cause the flip to always happen."""
                pNewOwner = gc.getPlayer(iNewOwner)
                city = gc.getMap().plot(tCityPlot[0], tCityPlot[1]).getPlotCity()
                if (gc.getMap().plot(tCityPlot[0], tCityPlot[1]).isCity()):
                        if not city.isNone():
                                iOldOwner = city.getOwner()
                                if (iOldOwner in iOldOwners or not iOldOwners):

                                        if (bKillUnits):
                                                killPlot = gc.getMap().plot( tCityPlot[0], tCityPlot[1] )
                                                for i in range(killPlot.getNumUnits()):
                                                        unit = killPlot.getUnit(0)
                                                        unit.kill(False, iNewOwner)
                                                        
                                        if (bFlipType): #conquest
                                                if (city.getPopulation() == 2):
                                                        city.setPopulation(3)
                                                if (city.getPopulation() == 1):
                                                        city.setPopulation(2)
                                                pNewOwner.acquireCity(city, True, False)
                                        else: #trade
                                                pNewOwner.acquireCity(city, False, True)
                                                
                                        return True
                return False


        #Congresses, RiseAndFall
        def cultureManager(self, tCityPlot, iCulturePercent, iNewOwner, iOldOwner, bBarbarian2x2Decay, bBarbarian2x2Conversion, bAlwaysOwnPlots):
                """Converts the culture of the city and of the surrounding plots to the new owner of a city.
                iCulturePercent determine the percentage that goes to the new owner.
                If old owner is barbarian, all the culture is converted"""

                pCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
                city = pCity.getPlotCity()                

                #city
                if (pCity.isCity()):
                        iCurrentCityCulture = city.getCulture(iOldOwner)
                        city.setCulture(iOldOwner, iCurrentCityCulture*(100-iCulturePercent)/100, False)
                        if (iNewOwner != con.iBarbarian):
                                city.setCulture(con.iBarbarian, 0, True)
                        city.setCulture(iNewOwner, iCurrentCityCulture*iCulturePercent/100, False)
                        if (city.getCulture(iNewOwner) <= 10):
                                city.setCulture(iNewOwner, 20, False)

                #halve barbarian culture in a broader area
                if (bBarbarian2x2Decay or bBarbarian2x2Conversion):
                        if (iNewOwner != con.iBarbarian and iNewOwner != con.iIndependent and iNewOwner != con.iIndependent2):
                                for x in range(tCityPlot[0]-2, tCityPlot[0]+3):        # from x-2 to x+2
                                        for y in range(tCityPlot[1]-2, tCityPlot[1]+3):	# from y-2 to y+2                                
                                                iPlotBarbCulture = gc.getMap().plot(x, y).getCulture(con.iBarbarian)
                                                if (iPlotBarbCulture > 0):
                                                        if (gc.getMap().plot(x, y).getPlotCity().isNone() or (x==tCityPlot[0] and y==tCityPlot[1])):
                                                                if (bBarbarian2x2Decay):
                                                                        gc.getMap().plot(x, y).setCulture(con.iBarbarian, iPlotBarbCulture/4, True)
                                                                if (bBarbarian2x2Conversion):
                                                                        gc.getMap().plot(x, y).setCulture(con.iBarbarian, 0, True)
                                                                        gc.getMap().plot(x, y).setCulture(iNewOwner, iPlotBarbCulture, True)
                                                iPlotIndependentCulture = gc.getMap().plot(x, y).getCulture(con.iIndependent)
                                                if (iPlotIndependentCulture > 0):
                                                        if (gc.getMap().plot(x, y).getPlotCity().isNone() or (x==tCityPlot[0] and y==tCityPlot[1])):
                                                                if (bBarbarian2x2Decay):
                                                                        gc.getMap().plot(x, y).setCulture(con.iIndependent, iPlotIndependentCulture/4, True)
                                                                if (bBarbarian2x2Conversion):
                                                                        gc.getMap().plot(x, y).setCulture(con.iIndependent, 0, True)
                                                                        gc.getMap().plot(x, y).setCulture(iNewOwner, iPlotIndependentCulture, True)
                                                iPlotIndependent2Culture = gc.getMap().plot(x, y).getCulture(con.iIndependent2)
                                                if (iPlotIndependent2Culture > 0):
                                                        if (gc.getMap().plot(x, y).getPlotCity().isNone() or (x==tCityPlot[0] and y==tCityPlot[1])):
                                                                if (bBarbarian2x2Decay):
                                                                        gc.getMap().plot(x, y).setCulture(con.iIndependent2, iPlotIndependent2Culture/4, True)
                                                                if (bBarbarian2x2Conversion):
                                                                        gc.getMap().plot(x, y).setCulture(con.iIndependent2, 0, True)
                                                                        gc.getMap().plot(x, y).setCulture(iNewOwner, iPlotIndependent2Culture, True)
                                                                        
                #plot                               
                for x in range(tCityPlot[0]-1, tCityPlot[0]+2):        # from x-1 to x+1
                        for y in range(tCityPlot[1]-1, tCityPlot[1]+2):	# from y-1 to y+1
                                pCurrent = gc.getMap().plot(x, y)
                                
                                iCurrentPlotCulture = pCurrent.getCulture(iOldOwner)

                                if (pCurrent.isCity()):                                
                                        pCurrent.setCulture(iNewOwner, iCurrentPlotCulture*iCulturePercent/100, True)
                                        pCurrent.setCulture(iOldOwner, iCurrentPlotCulture*(100-iCulturePercent)/100, True)
                                else:
                                        pCurrent.setCulture(iNewOwner, iCurrentPlotCulture*iCulturePercent/3/100, True)
                                        pCurrent.setCulture(iOldOwner, iCurrentPlotCulture*(100-iCulturePercent/3)/100, True)

                                #cut other players culture
##                                for iCiv in range(iNumPlayers):
##                                        if (iCiv != iNewOwner and iCiv != iOldOwner):
##                                                iPlotCulture = gc.getMap().plot(x, y).getCulture(iCiv)
##                                                if (iPlotCulture > 0):
##                                                        gc.getMap().plot(x, y).setCulture(iCiv, iPlotCulture/3, True)
                                                        
                                #print (x, y, pCurrent.getCulture(iNewOwner), ">", pCurrent.getCulture(iOldOwner))

                                if (not pCurrent.isCity()):
                                        if (bAlwaysOwnPlots):
                                                pCurrent.setOwner(iNewOwner)
                                        else:
                                                if (pCurrent.getCulture(iNewOwner)*4 > pCurrent.getCulture(iOldOwner)):
                                                        pCurrent.setOwner(iNewOwner)                                        
                                        #print ("NewOwner", pCurrent.getOwner())



        #handler
        def spreadMajorCulture(self, iMajorCiv, iX, iY):                
                for x in range(iX-4, iX+5):        # from x-4 to x+4
                        for y in range(iY-4, iY+5):	# from y-4 to y+4
                                pCurrent = gc.getMap().plot(x, y)
                                if (pCurrent.isCity()):
                                        city = pCurrent.getPlotCity()
                                        if (city.getOwner() >= iNumMajorPlayers):
                                                iMinor = city.getOwner()
                                                iDen = 25
                                                if (gc.getPlayer(iMajorCiv).getSettlersMaps( 67-y, x ) >= 400):
                                                        iDen = 10
                                                elif (gc.getPlayer(iMajorCiv).getSettlersMaps( 67-y, x ) >= 150):
                                                        iDen = 15
                                                        
                                                iMinorCityCulture = city.getCulture(iMinor)
                                                city.setCulture(iMajorCiv, iMinorCityCulture/iDen, True)
                                                
                                                iMinorPlotCulture = pCurrent.getCulture(iMinor)
                                                pCurrent.setCulture(iMajorCiv, iMinorPlotCulture/iDen, True)                                

        #UniquePowers
        def convertPlotCulture(self, pCurrent, iCiv, iPercent, bOwner):
                
                if (pCurrent.isCity()):
                        city = pCurrent.getPlotCity()
                        iCivCulture = city.getCulture(iCiv)
                        iLoopCivCulture = 0
                        for iLoopCiv in range(iNumTotalPlayers):
                                if (iLoopCiv != iCiv):
                                        iLoopCivCulture += city.getCulture(iLoopCiv)                                
                                        city.setCulture(iLoopCiv, city.getCulture(iLoopCiv)*(100-iPercent)/100, True)
                        city.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)  
        
##                for iLoopCiv in range(iNumTotalPlayers):
##                        if (iLoopCiv != iCiv):
##                                iLoopCivCulture = pCurrent.getCulture(iLoopCiv)
##                                iCivCulture = pCurrent.getCulture(iCiv)
##                                pCurrent.setCulture(iLoopCiv, iLoopCivCulture*(100-iPercent)/100, True)
##                                pCurrent.setCulture(iCiv, iCivCulture + iLoopCivCulture*iPercent/100, True)
                iCivCulture = pCurrent.getCulture(iCiv)
                iLoopCivCulture = 0
                for iLoopCiv in range(iNumTotalPlayers):
                        if (iLoopCiv != iCiv):
                                iLoopCivCulture += pCurrent.getCulture(iLoopCiv)                                
                                pCurrent.setCulture(iLoopCiv, pCurrent.getCulture(iLoopCiv)*(100-iPercent)/100, True)
                pCurrent.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)                                
                if (bOwner == True):
                        pCurrent.setOwner(iCiv)

        #DynamicCivs
        def getMaster(self, iCiv):
		team = gc.getTeam(gc.getPlayer(iCiv).getTeam())
		for iMaster in range(iNumTotalPlayers):
			if team.isVassal(iMaster):
				return iMaster
		return -1



                                




        #Congresses, RiseAndFall
        def pushOutGarrisons(self, tCityPlot, iOldOwner):
                tDestination = (-1, -1)
                for x in range(tCityPlot[0]-2, tCityPlot[0]+3):
                        for y in range(tCityPlot[1]-2, tCityPlot[1]+3):
                                pDestination = gc.getMap().plot(x, y)
                                if (pDestination.getOwner() == iOldOwner and (not pDestination.isWater()) and (not pDestination.isImpassable())):
                                        tDestination = (x, y)
                                        break
                                        break
                if (tDestination != (-1, -1)):
                        plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
                        iNumUnitsInAPlot = plotCity.getNumUnits()
                        j = 0
                        for i in range(iNumUnitsInAPlot):                        
                                unit = plotCity.getUnit(j)
                                if (unit.getDomainType() == 2): #land unit
                                        unit.setXYOld(tDestination[0], tDestination[1])
                                else:
                                        j = j + 1

	def relocateGarrisons(self, tCityPlot, iOldOwner):
		if iOldOwner < con.iNumPlayers:
			pCity = self.getRandomCity(iOldOwner)
			if pCity != -1:
				plot = gc.getMap().plot(tCityPlot[0],tCityPlot[1])
				iNumUnits = plot.getNumUnits()
				j = 0
				for i in range(iNumUnits):
					unit = plot.getUnit(j)
					if (unit.getDomainType() == 2): #land
						unit.setXYOld(pCity.getX(), pCity.getY())
					else:
						j = j + 1
		else:
			plot = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
			iNumUnits = plot.getNumUnits()
			for i in range(iNumUnits):
				unit = plot.getUnit(i)
				unit.kill(False, iOldOwner)
				
	def removeCoreUnits(self, iPlayer):
		for x in range(con.tCoreAreasTL[0][iPlayer][0], con.tCoreAreasBR[0][iPlayer][0]+1):
			for y in range(con.tCoreAreasTL[0][iPlayer][1], con.tCoreAreasBR[0][iPlayer][1]+1):
				plot = gc.getMap().plot(x, y)
				if plot.isCity():
					pCity = plot.getPlotCity()
					if pCity.getOwner() != iPlayer:
						x = pCity.getX()
						y = pCity.getY()
						self.relocateGarrisons((x,y), pCity.getOwner())
						self.relocateSeaGarrisons((x,y), pCity.getOwner())
						self.createGarrisons((x,y), iPlayer, 2)
				else:
					iNumUnits = plot.getNumUnits()
					j = 0
					for i in range(iNumUnits):
						unit = plot.getUnit(j)
						iOwner = unit.getOwner()
						if iOwner < con.iNumPlayers and iOwner != iPlayer:
							capital = gc.getPlayer(iOwner).getCapitalCity()
							if capital.getX() != -1 and capital.getY() != -1:
								unit.setXYOld(capital.getX(), capital.getY())
						else:
							j += 1
                                
        #Congresses, RiseAndFall
        def relocateSeaGarrisons(self, tCityPlot, iOldOwner):
                tDestination = (-1, -1)
                cityList = PyPlayer(iOldOwner).getCityList()
                for pyCity in cityList:
                        if (pyCity.GetCy().isCoastalOld()):
                                tDestination = (pyCity.GetCy().getX(), pyCity.GetCy().getY())
                if (tDestination == (-1, -1)):                    
                        for x in range(tCityPlot[0]-12, tCityPlot[0]+12):
                                for y in range(tCityPlot[1]-12, tCityPlot[1]+12):
                                        pDestination = gc.getMap().plot(x, y)
                                        if (pDestination.isWater()):
                                                tDestination = (x, y)
                                                break
                                                break
                if (tDestination != (-1, -1)):
                        plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
                        iNumUnitsInAPlot = plotCity.getNumUnits()
                        j = 0
                        for i in range(iNumUnitsInAPlot):
                                unit = plotCity.getUnit(j)
                                if (unit.getDomainType() == 0): #sea unit
                                        unit.setXYOld(tDestination[0], tDestination[1])
                                else:
                                        j = j + 1


        #Congresses, RiseAndFall
        def createGarrisons(self, tCityPlot, iNewOwner, iNumUnits):
                plotCity = gc.getMap().plot(tCityPlot[0], tCityPlot[1])
                city = plotCity.getPlotCity()    
                iNumUnitsInAPlot = plotCity.getNumUnits()
                pCiv = gc.getPlayer(iNewOwner)

                if (gc.getTeam(pCiv.getTeam()).isHasTech(con.iAssemblyLine) and gc.getTeam(pCiv.getTeam()).isHasTech(con.iRifling)):
                        iUnitType = con.iInfantry
                elif (gc.getTeam(pCiv.getTeam()).isHasTech(con.iRifling)):
                        if (iNewOwner != con.iEngland):
                                iUnitType = con.iRifleman
                        else:
                                iUnitType = con.iEnglishRedcoat
                elif (gc.getTeam(pCiv.getTeam()).isHasTech(con.iGunpowder)):
                        iUnitType = con.iMusketman
                else:
                        iUnitType = con.iLongbowman

                self.makeUnit(iUnitType, iNewOwner, [tCityPlot[0], tCityPlot[1]], iNumUnits)



        #RiseAndFall, Stability

        def killCiv(self, iCiv, iNewCiv):
                self.clearPlague(iCiv)
                for pyCity in PyPlayer(iCiv).getCityList():
                        tCoords = (pyCity.GetCy().getX(), pyCity.GetCy().getY())
                        self.cultureManager(tCoords, 50, iNewCiv, iCiv, False, False, False)
                        self.flipCity(tCoords, 0, 0, iNewCiv, [iCiv]) #by trade because by conquest may raze the city
                        #pyCity.GetCy().setHasRealBuilding(con.iPlague, False)  #buggy
                self.flipUnitsInArea([0,0], [123,67], iNewCiv, iCiv, False, True)
                #self.killUnitsInArea([0,0], [123,67], iNewCiv, iCiv) ?
                if (iCiv < iNumMajorPlayers):
                        self.clearEmbassies(iCiv)
                self.setLastTurnAlive(iCiv, gc.getGame().getGameTurn())
                self.resetUHV(iCiv)

        def killAndFragmentCiv(self, iCiv, iNewCiv1, iNewCiv2, iNewCiv3, bAssignOneCity):
                print("Fragmentation into:", iNewCiv1, iNewCiv2, iNewCiv3)
                self.clearPlague(iCiv)
                iNumLoyalCities = 0
                iCounter = gc.getGame().getSorenRandNum(6, 'random start')
                iNumPlayerCities = len(PyPlayer(iCiv).getCityList()) #needs to be assigned cause it changes dynamically
                for pyCity in PyPlayer(iCiv).getCityList():
                        #print("iCounter",iCounter)
			city = pyCity.GetCy()
			tCoords = (city.getX(), city.getY())
			pCurrent = gc.getMap().plot(tCoords[0], tCoords[1])
                        #loyal cities for the human player
                        #print(bAssignOneCity,iNumLoyalCities,1+(iNumPlayerCities-1)/6,pyCity.GetCy().isCapital(),iCounter%6 == 0)
			# Leoreth: Byzantine UP: cities in normal area immune to collapse [expires for AI after the MA]
			x = gc.getPlayer(iCiv).getCapitalCity().getX()
			y = gc.getPlayer(iCiv).getCapitalCity().getY()
			if iCiv == con.iByzantium and (x,y) == con.tCapitals[0][con.iByzantium] and not self.isAVassal(con.iByzantium) and (bAssignOneCity or gc.getPlayer(con.iByzantium).getCurrentEra() <= con.iMedieval):
				x, y = tCoords
				tlx, tly = con.tNormalAreasTL[self.getReborn(iCiv)][iCiv]
				brx, bry = con.tNormalAreasBR[self.getReborn(iCiv)][iCiv]
				if x >= tlx and x <= brx and y >= tly and y <= bry and tCoords not in con.tNormalAreasSubtract[self.getReborn(iCiv)][iCiv]:
					continue
                        elif (bAssignOneCity and iNumLoyalCities <= 1+(iNumPlayerCities-1)/6 and (pyCity.GetCy().isCapital() or iCounter%6 == 0)):
                                iNumLoyalCities += 1
                                if (iNumLoyalCities == 1):
                                        gc.getTeam(gc.getPlayer(iCiv).getTeam()).declareWar(iNewCiv1, False, -1) #too dangerous?
                                        gc.getTeam(gc.getPlayer(iCiv).getTeam()).declareWar(iNewCiv2, False, -1)
                                iCounter += 1
                                #print(pyCity.GetCy().getName(), "loyal")
                                continue
                        #assign to neighbours first
                        bNeighbour = False
                        iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
                        for j in range(iRndnum, iRndnum + iNumPlayers): #only major players
                                iLoopCiv = j % iNumPlayers
                                if (gc.getPlayer(iLoopCiv).isAlive() and iLoopCiv != iCiv and not gc.getPlayer(iLoopCiv).isHuman()):
                                        if (pCurrent.getCulture(iLoopCiv) > 0):
                                                if (pCurrent.getCulture(iLoopCiv)*100 / (pCurrent.getCulture(iLoopCiv) + pCurrent.getCulture(iCiv) + pCurrent.getCulture(iBarbarian) + pCurrent.getCulture(iIndependent) + pCurrent.getCulture(iIndependent2)) >= 50): #change in vanilla
                                                        self.flipUnitsInCityBefore((tCoords[0],tCoords[1]), iLoopCiv, iCiv)                            
                                                        self.setTempFlippingCity((tCoords[0],tCoords[1]))
                                                        self.flipCity(tCoords, 0, 0, iLoopCiv, [iCiv])
                                                        #pyCity.GetCy().setHasRealBuilding(con.iPlague, False)  #buggy
                                                        self.flipUnitsInCityAfter(self.getTempFlippingCity(), iLoopCiv)
                                                        self.flipUnitsInArea([tCoords[0]-2,tCoords[1]-2], [tCoords[0]+2,tCoords[1]+2], iLoopCiv, iCiv, True, True)
                                                        bNeighbour = True
                                                        break
                        if (bNeighbour):
                                iCounter += 1
                                continue
                        #fragmentation in 2
                        if (iNewCiv3 == -1):
                                #iNewCiv = -1 #debug
                                if (iCounter % 2 == 0):
                                        iNewCiv = iNewCiv1
                                elif (iCounter % 2 == 1):
                                        iNewCiv = iNewCiv2
                                self.flipUnitsInCityBefore((tCoords[0],tCoords[1]), iNewCiv, iCiv)                            
                                self.setTempFlippingCity((tCoords[0],tCoords[1]))                                                        
                                self.cultureManager(tCoords, 50, iNewCiv, iCiv, False, False, False)
                                self.flipCity(tCoords, 0, 0, iNewCiv, [iCiv])
                                #pyCity.GetCy().setHasRealBuilding(con.iPlague, False)  #buggy
                                self.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
                                #print(pyCity.GetCy().getName(), iNewCiv)
                                iCounter += 1
                                self.flipUnitsInArea([tCoords[0]-1,tCoords[1]-1], [tCoords[0]+1,tCoords[1]+1], iNewCiv, iCiv, False, True)
                        #fragmentation with barbs
                        else:
                                if (iCounter % 3 == 0):
                                        iNewCiv = iNewCiv1
                                elif (iCounter % 3 == 1):
                                        iNewCiv = iNewCiv2
                                elif (iCounter % 3 == 2):
                                        iNewCiv = iNewCiv3
                                self.flipUnitsInCityBefore((tCoords[0],tCoords[1]), iNewCiv, iCiv)                            
                                self.setTempFlippingCity((tCoords[0],tCoords[1]))         
                                self.cultureManager(tCoords, 50, iNewCiv, iCiv, False, False, False)
                                self.flipCity(tCoords, 0, 0, iNewCiv, [iCiv])
                                #pyCity.GetCy().setHasRealBuilding(con.iPlague, False) #buggy
                                self.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
                                iCounter += 1                                      
                                self.flipUnitsInArea([tCoords[0]-1,tCoords[1]-1], [tCoords[0]+1,tCoords[1]+1], iNewCiv, iCiv, False, True)
                if (not bAssignOneCity and not (iCiv == con.iByzantium and (x,y) == con.tCapitals[0][con.iByzantium] and not self.isAVassal(con.iByzantium) and (bAssignOneCity or gc.getPlayer(con.iByzantium).getCurrentEra() <= con.iMedieval))):
                        #self.flipUnitsInArea([0,0], [123,67], iNewCiv1, iCiv, False, True) #causes a bug: if a unit was inside another city's civ, when it becomes independent or barbarian, may raze it
                        self.killUnitsInArea([0,0], [123,67], iCiv)
                        self.resetUHV(iCiv)
                if (iCiv < iNumMajorPlayers):
                        self.clearEmbassies(iCiv)
                self.setLastTurnAlive(iCiv, gc.getGame().getGameTurn())

		# Leoreth: Byzantium collapses - Christians in Turkish core disappear
		if iCiv == con.iByzantium:
			self.removeReligionByArea(con.tCoreAreasTL[0][con.iTurkey], con.tCoreAreasBR[0][con.iTurkey], con.iChristianity)



        def pickFragmentation(self, iPlayer, iNewCiv1, iNewCiv2, iNewCiv3, bAssignCities):
                if (iPlayer == con.iAztecs or \
                    iPlayer == con.iInca or \
                    iPlayer == con.iMaya or \
                    iPlayer == con.iEthiopia or \
                    iPlayer == con.iMali):
                        if (self.getCivsWithNationalism() <= 0):
                                self.killAndFragmentCiv(iPlayer, con.iNative, iBarbarian, iNewCiv3, bAssignCities)
                        else:
                                self.killAndFragmentCiv(iPlayer, iNewCiv1, iNewCiv2, iNewCiv3, bAssignCities)
                else:
                        self.killAndFragmentCiv(iPlayer, iNewCiv1, iNewCiv2, iNewCiv3, bAssignCities)
                teamCiv = gc.getTeam(gc.getPlayer(iPlayer).getTeam())
		for iEnemy in range(con.iNumPlayers):
			if teamCiv.isAtWar(iEnemy):
				for iNewCiv in (iNewCiv1, iNewCiv2, iNewCiv3):
					if iNewCiv != -1:
						teamCiv.declareWar(iNewCiv, False, -1)
				


                
        def resetUHV(self, iPlayer):
                if (iPlayer < iNumMajorPlayers):
                        if (self.getGoal(iPlayer, 0) == -1):
                                self.setGoal(iPlayer, 0, 0)
                        if (self.getGoal(iPlayer, 1) == -1):
                                self.setGoal(iPlayer, 1, 0)
                        if (self.getGoal(iPlayer, 2) == -1):
                                self.setGoal(iPlayer, 2, 0)
                                                
        def clearEmbassies(self, iDeadCiv):
                for i in range (iNumTotalPlayers):
                        for pyCity in PyPlayer(i).getCityList():
                                if (pyCity.GetCy().hasBuilding(iNumBuildingsPlague + iDeadCiv)):
                                        pyCity.GetCy().setHasRealBuilding(iNumBuildingsPlague + iDeadCiv, False)
                                        continue


        def clearPlague(self, iCiv):
                for pyCity in PyPlayer(iCiv).getCityList():
                        if (pyCity.GetCy().hasBuilding(con.iPlague)):
                                pyCity.GetCy().setHasRealBuilding(con.iPlague, False)




        #AIWars, by CyberChrist

        def isNoVassal(self, iCiv):
                iMaster = 0
                for iMaster in range (iNumTotalPlayers):
                        if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iMaster)):
                                return False
                return True

        def isAVassal(self, iCiv):
                iMaster = 0
                for iMaster in range (iNumTotalPlayers):
                        if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iMaster)):
                                return True
                return False

        #Barbs, RiseAndFall
        def squareSearch( self, tTopLeft, tBottomRight, function, argsList ): #by LOQ
                """Searches all tile in the square from tTopLeft to tBottomRight and calls function for
                every tile, passing argsList. The function called must return a tuple: (1) a result, (2) if
                a plot should be painted and (3) if the search should continue."""
                tPaintedList = []
                result = None
                for x in range(tTopLeft[0], tBottomRight[0]+1):
                        for y in range(tTopLeft[1], tBottomRight[1]+1):
                                result, bPaintPlot, bContinueSearch = function((x, y), result, argsList)
                                if bPaintPlot:			# paint plot
                                        tPaintedList.append((x, y))
                                if not bContinueSearch:		# goal reached, so stop
                                        return result, tPaintedList
                return result, tPaintedList

        #Barbs, RiseAndFall
        def outerInvasion( self, tCoords, result, argsList ):
                """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
                Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
                bPaint = True
                bContinue = True
                pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
                if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
                        if (pCurrent.getTerrainType() != con.iMarsh) and (pCurrent.getFeatureType() != con.iJungle):
                                if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
                                        if (pCurrent.countTotalCulture() == 0 ):
                                                # this is a good plot, so paint it and continue search
                                                return (None, bPaint, bContinue)
                # not a good plot, so don't paint it but continue search
                return (None, not bPaint, bContinue)

        #Barbs
        def innerSeaSpawn( self, tCoords, result, argsList ):
                """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
                Plot is valid if it's water and it isn't occupied by any unit. Unit check extended to adjacent plots"""
                bPaint = True
                bContinue = True
                pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
                if ( pCurrent.isWater()):
                        if ( not pCurrent.isCity() and not pCurrent.isUnit() and pCurrent.area().getNumTiles() > 10 ):
                                iClean = 0
                                for x in range(tCoords[0] - 1, tCoords[0] + 2):        # from x-1 to x+1
                                        for y in range(tCoords[1] - 1, tCoords[1] + 2):	# from y-1 to y+1
                                                if (pCurrent.getNumUnits() != 0):
                                                        iClean += 1
                                if ( iClean == 0 ):   
                                        # this is a good plot, so paint it and continue search
                                        return (None, bPaint, bContinue)
                # not a good plot, so don't paint it but continue search
                return (None, not bPaint, bContinue)

        #Barbs
        def outerSeaSpawn( self, tCoords, result, argsList ):
                """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
                Plot is valid if it's water and it isn't occupied by any unit and if it isn't a civ's territory. Unit check extended to adjacent plots"""
                bPaint = True
                bContinue = True
                pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
                if ( pCurrent.isWater()):
                        if ( not pCurrent.isCity() and not pCurrent.isUnit() and pCurrent.area().getNumTiles() > 10):
                                if (pCurrent.countTotalCulture() == 0 ):
                                        iClean = 0
                                        for x in range(tCoords[0] - 1, tCoords[0] + 2):        # from x-1 to x+1
                                                for y in range(tCoords[1] - 1, tCoords[1] + 2):	# from y-1 to y+1
                                                        if (pCurrent.getNumUnits() != 0):
                                                                iClean += 1
                                        if ( iClean == 0 ):   
                                                # this is a good plot, so paint it and continue search
                                                return (None, bPaint, bContinue)
                # not a good plot, so don't paint it but continue search
                return (None, not bPaint, bContinue)

        def outerCoastSpawn( self, tCoords, result, argsList ):
                """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
                Plot is valid if it's water and it isn't occupied by any unit and if it isn't a civ's territory. Unit check extended to adjacent plots"""
                bPaint = True
                bContinue = True
                pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
                if ( pCurrent.getTerrainType() == con.iCoast):
                        if ( not pCurrent.isCity() and not pCurrent.isUnit() and pCurrent.area().getNumTiles() > 10 ):
                                if (pCurrent.countTotalCulture() == 0 ):
                                        iClean = 0
                                        for x in range(tCoords[0] - 1, tCoords[0] + 2):        # from x-1 to x+1
                                                for y in range(tCoords[1] - 1, tCoords[1] + 2):	# from y-1 to y+1
                                                        if (pCurrent.getNumUnits() != 0):
                                                                iClean += 1
                                        if ( iClean == 0 ):   
                                                # this is a good plot, so paint it and continue search
                                                return (None, bPaint, bContinue)
                # not a good plot, so don't paint it but continue search
                return (None, not bPaint, bContinue)

        #Barbs
        def outerSpawn( self, tCoords, result, argsList ):
                """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
                Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory.
                Unit check extended to adjacent plots"""
                bPaint = True
                bContinue = True
                pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
                if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
                        if (pCurrent.getTerrainType() != con.iMarsh) and (pCurrent.getFeatureType() != con.iJungle):
                                if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
                                        iClean = 0
                                        for x in range(tCoords[0] - 1, tCoords[0] + 2):        # from x-1 to x+1
                                                for y in range(tCoords[1] - 1, tCoords[1] + 2):	# from y-1 to y+1
                                                        if (pCurrent.getNumUnits() != 0):
                                                                iClean += 1
                                        if ( iClean == 0 ):
                                                if (pCurrent.countTotalCulture() == 0 ):
                                                        # this is a good plot, so paint it and continue search
                                                        return (None, bPaint, bContinue)
                # not a good plot, so don't paint it but continue search
                return (None, not bPaint, bContinue)                                        

        #RiseAndFall
        def innerInvasion( self, tCoords, result, argsList ):
                """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
                Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
                bPaint = True
                bContinue = True
                pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
                if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
                        if (pCurrent.getTerrainType() != con.iMarsh) and (pCurrent.getFeatureType() != con.iJungle):
                                if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
                                        if (pCurrent.getOwner() in argsList ):
                                                # this is a good plot, so paint it and continue search
                                                return (None, bPaint, bContinue)
                # not a good plot, so don't paint it but continue search
                return (None, not bPaint, bContinue)

	def internalInvasion(self, tCoords, result, argsList):
		"""Like inner invasion, but ignores territory, to allow for more barbarians"""
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot(tCoords[0], tCoords[1])
		if pCurrent.isHills() or pCurrent.isFlatlands():
			if pCurrent.getTerrainType() != con.iMarsh and pCurrent.getFeatureType() != con.iJungle:
				if not pCurrent.isCity() and not pCurrent.isUnit():
					return (None, bPaint, bContinue)
		return (None, not bPaint, bContinue)
            
        def innerSpawn( self, tCoords, result, argsList ):
                """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
                Plot is valid if it's hill or flatlands, it isn't marsh or jungle, it isn't occupied by a unit or city and if it isn't a civ's territory"""
                bPaint = True
                bContinue = True
                pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
                if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
                        if (pCurrent.getTerrainType() != con.iMarsh) and (pCurrent.getFeatureType() != con.iJungle):
                                if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
                                        iClean = 0
                                        for x in range(tCoords[0] - 1, tCoords[0] + 2):        # from x-1 to x+1
                                                for y in range(tCoords[1] - 1, tCoords[1] + 2):	# from y-1 to y+1
                                                        if (pCurrent.getNumUnits() != 0):
                                                                iClean += 1
                                        if ( iClean == 0 ):  
                                                if (pCurrent.getOwner() in argsList ):
                                                        # this is a good plot, so paint it and continue search
                                                        return (None, bPaint, bContinue)
                # not a good plot, so don't paint it but continue search
                return (None, not bPaint, bContinue)

        #RiseAndFall
        def goodPlots( self, tCoords, result, argsList ):
                """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
                Plot is valid if it's hill or flatlands, it isn't desert, tundra, marsh or jungle; it isn't occupied by a unit or city and if it isn't a civ's territory.
                Unit check extended to adjacent plots"""
                bPaint = True
                bContinue = True
                pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
                if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
                        if ( not pCurrent.isImpassable()):
                                if ( not pCurrent.isUnit() ):
                                        if (pCurrent.getTerrainType() != con.iDesert) and (pCurrent.getTerrainType() != con.iTundra) and (pCurrent.getTerrainType() != con.iMarsh) and (pCurrent.getFeatureType() != con.iJungle):
                                                if (pCurrent.countTotalCulture() == 0 ):
                                                        # this is a good plot, so paint it and continue search
                                                        return (None, bPaint, bContinue)
                # not a good plot, so don't paint it but continue search
                return (None, not bPaint, bContinue)

        #RiseAndFall
	def cityPlots(self, tCoords, result, argsList):
		bPaint = True
		bContinue = True
		pCurrent = gc.getMap().plot(tCoords[0], tCoords[1])
		if pCurrent.isCity():
			return (None, bPaint, bContinue)
		return (None, not bPaint, bContinue)

        def ownedCityPlots( self, tCoords, result, argsList ):
                """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
                Plot is valid if it contains a city belonging to the civ"""
                bPaint = True
                bContinue = True
                pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
                if (pCurrent.getOwner() == argsList ):
                        if (pCurrent.isCity()):
                                # this is a good plot, so paint it and continue search
                                return (None, bPaint, bContinue)
                # not a good plot, so don't paint it but continue search
                return (None, not bPaint, bContinue)

        def ownedCityPlotsAdjacentArea( self, tCoords, result, argsList ):
                """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
                Plot is valid if it contains a city belonging to the civ"""
                bPaint = True
                bContinue = True
                pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
                #print(tCoords[0], tCoords[1], pCurrent.isCity(), pCurrent.getOwner() == argsList[0], pCurrent.isAdjacentToArea(gc.getMap().plot(argsList[1][0],argsList[1][1]).area()))
                if (pCurrent.getOwner() == argsList[0] and pCurrent.isAdjacentToArea(gc.getMap().plot(argsList[1][0],argsList[1][1]).area())):
                        if (pCurrent.isCity()):
                                # this is a good plot, so paint it and continue search
                                return (None, bPaint, bContinue)
                # not a good plot, so don't paint it but continue search
                return (None, not bPaint, bContinue)

        def foundedCityPlots( self, tCoords, result, argsList ):
                """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
                Plot is valid if it contains a city belonging to the civ"""
                bPaint = True
                bContinue = True
                pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
                if (pCurrent.isCity()):
                        if (pCurrent.getPlotCity().getOriginalOwner() == argsList ):                        
                                # this is a good plot, so paint it and continue search
                                return (None, bPaint, bContinue)
                # not a good plot, so don't paint it but continue search
                return (None, not bPaint, bContinue)    

        def ownedPlots( self, tCoords, result, argsList ):
                """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
                Plot is valid if it is in civ's territory."""
                bPaint = True
                bContinue = True
                pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
                if (pCurrent.getOwner() == argsList ):
                        # this is a good plot, so paint it and continue search
                        return (None, bPaint, bContinue)
                # not a good plot, so don't paint it but continue search
                return (None, not bPaint, bContinue)

        def goodOwnedPlots( self, tCoords, result, argsList ):
                """Checks validity of the plot at the current tCoords, returns plot if valid (which stops the search).
                Plot is valid if it's hill or flatlands; it isn't marsh or jungle, it isn't occupied by a unit and if it is in civ's territory."""
                bPaint = True
                bContinue = True
                pCurrent = gc.getMap().plot( tCoords[0], tCoords[1] )
                if ( pCurrent.isHills() or pCurrent.isFlatlands() ):
                        if (pCurrent.getTerrainType() != con.iMarsh) and (pCurrent.getFeatureType() != con.iJungle):
                                if ( not pCurrent.isCity() and not pCurrent.isUnit() ):
                                            if (pCurrent.getOwner() == argsList ):
                                                    # this is a good plot, so paint it and continue search
                                                    return (None, bPaint, bContinue)
                # not a good plot, so don't paint it but continue search
                return (None, not bPaint, bContinue)

        def getTurns(self, turns): # edead
                """Returns the amount of turns modified adequately for the game's speed.
                Values are based on CIV4GameSpeedInfos.xml. Use this only for durations, intervals etc.; 
                for year->turn conversions, use the DLL function getTurnForYear(int year)."""
                iGameSpeed = gc.getGame().getGameSpeedType()
                if iGameSpeed == 2: return turns # normal
                elif iGameSpeed == 1: # epic
                        if turns == 3: return 5 # getTurns(6) must be a multiple of getTurns(3) for turn divisors in Stability.py
                        elif turns == 6: return 10
                        else: return turns*3/2
                elif iGameSpeed == 0: return turns*3 # marathon
                #elif iGameSpeed == 3: return turns*2/3 # quick
                return turns

	# Leoreth - RiseAndFall
	def clearCatapult(self, iCiv):
	        plotZero = gc.getMap().plot( 0, 0 )                        
                if (plotZero.getNumUnits()):
                       catapult = plotZero.getUnit(0)
                       catapult.kill(False, iCiv)
                gc.getMap().plot(0, 0).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(0, 1).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(1, 1).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(1, 0).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(123, 0).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(123, 1).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(2, 0).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(2, 1).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(2, 2).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(1, 2).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(0, 2).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(122, 0).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(122, 1).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(122, 2).setRevealed(iCiv, False, True, -1);
                gc.getMap().plot(123, 2).setRevealed(iCiv, False, True, -1);

	# Leoreth
	def getReborn(self, iCiv):
		return gc.getPlayer(iCiv).getReborn()

	# Leoreth
	def getCoreCityList(self, iCiv, reborn):
		cityList = []
		for x in range(con.tCoreAreasTL[reborn][iCiv][0], con.tCoreAreasBR[reborn][iCiv][0]+1):
			for y in range(con.tCoreAreasTL[reborn][iCiv][1], con.tCoreAreasBR[reborn][iCiv][1]+1):
				plot = gc.getMap().plot(x,y)
				if plot.isCity():
					cityList.append(plot.getPlotCity())
		return cityList

	# Leoreth
	def getCoreUnitList(self, iCiv, reborn):
		unitList = []
		for x in range(con.tCoreAreasTL[reborn][iCiv][0], con.tCoreAreasBR[reborn][iCiv][0]+1):
			for y in range(con.tCoreAreasTL[reborn][iCiv][1], con.tCoreAreasBR[reborn][iCiv][1]+1):
				plot = gc.getMap().plot(x,y)
				if not plot.isCity():
					for i in range(plot.getNumUnits()):
						unitList.append(plot.getUnit(i))
		return unitList

	def getCivRectangleCities(self, iCiv, TopLeft, BottomRight):
		cityList = []
		for x in range(TopLeft[0], BottomRight[0]+1):
			for y in range(TopLeft[1], BottomRight[1]+1):
				plot = gc.getMap().plot(x,y)
				if plot.isCity():
					cityList.append(plot.getPlotCity())
		return cityList

	

	def removeReligionByArea(self, tTopLeft, tBottomRight, iReligion):
		lCityList = []
                for x in range(tTopLeft[0], tBottomRight[0]+1):
                        for y in range(tTopLeft[1], tBottomRight[1]+1):
				if gc.getMap().plot(x,y).isCity():
					lCityList.append(gc.getMap().plot(x,y).getPlotCity())
		for city in lCityList:
			if city.isHasReligion(iReligion) and not city.isHolyCity():
				city.setHasReligion(iReligion, False, False, False)
			if city.hasBuilding(con.iTemple + iReligion*4):
				city.setHasRealBuilding((con.iTemple + iReligion*4), False)
			if city.hasBuilding(con.iCathedral + iReligion*4):
				city.setHasRealBuilding((con.iCathedral + iReligion*4), False)
			if city.hasBuilding(con.iMonastery + iReligion*4):
				city.setHasRealBuilding((con.iMonastery + iReligion*4), False)

	def getEasternmostCity(self, iCiv):
		pPlayer = gc.getPlayer(iCiv)
		pResultCity = pPlayer.getCapitalCity()
		for i in range(pPlayer.getNumCities()):
			if pPlayer.getCity(i).getX() > pResultCity.getX():
				pResultCity = pPlayer.getCity(i)
		return pResultCity

	def getNorthernmostCity(self, iCiv):
		pPlayer = gc.getPlayer(iCiv)
		pResultCity = pPlayer.getCapitalCity()
		for i in range(pPlayer.getNumCities()):
			if pPlayer.getCity(i).getY() > pResultCity.getY():
				pResultCity = pPlayer.getCity(i)
		return pResultCity

	def getWesternmostCity(self, iCiv):
		pPlayer = gc.getPlayer(iCiv)
		pResultCity = pPlayer.getCapitalCity()
		for i in range(pPlayer.getNumCities()):
			if pPlayer.getCity(i).getX() < pResultCity.getX():
				pResultCity = pPlayer.getCity(i)
		return pResultCity

	def getFreeNeighborPlot(self, tPlot):
		x, y = tPlot
		plotList = []
		for i in range(x-1, x+2):
			for j in range(y-1, y+2):
				if (i, j) != (x, y):
					plot = gc.getMap().plot(i, j)
					if (not plot.isPeak()) and (not plot.isWater()) and (not plot.isCity()) and (not plot.isUnit()):
						plotList.append((i, j))
		iRand = gc.getGame().getSorenRandNum(len(plotList), '')
		return plotList[iRand]

	def colonialConquest(self, iCiv, x, y):
		bRifling = gc.getTeam(iCiv).isHasTech(con.iRifling)
		iTargetCiv = gc.getMap().plot(x,y).getPlotCity().getOwner()
		lFreePlots = []

		for i in range(x-1, x+2):
			for j in range(y-1, y+2):
				current = gc.getMap().plot(i, j)
				if not current.isCity() and not current.isPeak() and not current.isWater():
					lFreePlots.append((i,j))

		if iTargetCiv != -1:
			gc.getTeam(iCiv).declareWar(iTargetCiv, True, WarPlanTypes.WARPLAN_TOTAL)

		iRand = gc.getGame().getSorenRandNum(len(lFreePlots), 'random plot')
		tPlot = lFreePlots[iRand]

		if iCiv in [con.iSpain, con.iPortugal, con.iNetherlands]:
			iNumUnits = 2
		elif iCiv in [con.iFrance, con.iEngland]:
			iNumUnits = 3
		
		if bRifling:
			if iCiv == con.iFrance:
				self.makeUnit(con.iFrenchHeavyCannon, iCiv, tPlot, iNumUnits)
			else:
				self.makeUnit(con.iCannon, iCiv, tPlot, iNumUnits)
		else:
			self.makeUnit(con.iBombard, iCiv, tPlot, iNumUnits)

		if bRifling:
			if iCiv == con.iEngland:
				self.makeUnit(con.iEnglishRedcoat, iCiv, tPlot, 2*iNumUnits)
			else:
				self.makeUnit(con.iRifleman, iCiv, tPlot, 2*iNumUnits)
		else:
			self.makeUnit(con.iMusketman, iCiv, tPlot, 2*iNumUnits)


	def colonialAcquisition(self, iCiv, x, y):
		if iCiv in [con.iPortugal, con.iSpain]:
			iNumUnits = 1
		elif iCiv in [con.iFrance, con.iEngland, con.iNetherlands]:
			iNumUnits = 2
		if gc.getMap().plot(x,y).isCity():
			if gc.getMap().plot(x,y).getPlotCity().getOwner() != self.getHumanID():
				self.flipCity((x,y), False, True, iCiv, [])
				self.makeUnit(con.iWorker, iCiv, (x,y), iNumUnits)
				if gc.getTeam(iCiv).isHasTech(con.iRifling):
					if iCiv == con.iEngland:
						self.makeUnit(con.iEnglishRedcoat, iCiv, (x,y), iNumUnits)
					else:
						self.makeUnit(con.iRifleman, iCiv, (x,y), iNumUnits)
				else:
					self.makeUnit(con.iMusketman, iCiv, (x,y), iNumUnits)
				if gc.getPlayer(iCiv).getStateReligion() != -1:
					self.makeUnit(con.iJewishMissionary+gc.getPlayer(iCiv).getStateReligion(), iCiv, (x,y), 1)
			else:
				self.colonialConquest(iCiv, x, y)
		else:
			gc.getMap().plot(x,y).setCulture(iCiv, 10, True)
			gc.getMap().plot(x,y).setOwner(iCiv)
			self.makeUnit(con.iSettler, iCiv, (x,y), 1)
			self.makeUnit(con.iWorker, iCiv, (x,y), 2)
			if gc.getTeam(iCiv).isHasTech(con.iRifling):
				self.makeUnit(con.iRifleman, iCiv, (x,y), 2)
			else:
				self.makeUnit(con.iMusketman, iCiv, (x,y), 2)
			if gc.getPlayer(iCiv).getStateReligion() != -1:
				self.makeUnit(con.iJewishMissionary+gc.getPlayer(iCiv).getStateReligion(), iCiv, (x,y), 1)

	def getColonialTargets(self, iPlayer):
		if iPlayer == con.iSpain or iPlayer == con.iFrance:
			iNumCities = 1
		else:
			iNumCities = 3

		lCivList = [con.iSpain, con.iFrance, con.iEngland, con.iPortugal, con.iNetherlands]
		id = lCivList.index(iPlayer)

		lPlotList = con.tTradingCompanyPlotLists[id]

		cityList = []
		for tPlot in lPlotList:
			x, y = tPlot
			if gc.getMap().plot(x, y).isCity():
				if gc.getMap().plot(x, y).getPlotCity().getOwner() != iPlayer:
					cityList.append((x, y))

		targetList = []

		if len(cityList) != 0:
			for i in range(iNumCities):
				iRand = gc.getGame().getSorenRandNum(len(cityList), 'Random city')
				print 'iRand = '+str(iRand)
				if len(cityList) > 0:
					targetList.append(cityList[iRand])
					cityList.remove(cityList[iRand])

		if len(targetList) == 0:
			for i in range(iNumCities):
				iRand = gc.getGame().getSorenRandNum(len(lPlotList), 'Random free plot')
				print 'iRand = '+str(iRand)
				if len(lPlotList) > 0:
					targetList.append(lPlotList[iRand])
					lPlotList.remove(lPlotList[iRand])

		return targetList

	# Leoreth: tests if the plot is a part of the civs border in the specified direction
	#          returns list containing the plot if that's the case, empty list otherwise
	#          iDirection = -1 tests all directions
	def testBorderPlot(self, tPlot, iCiv, iDirection):
		x, y = tPlot
		if gc.getMap().plot(x, y).getOwner() != iCiv or gc.getMap().plot(x, y).isWater() or gc.getMap().plot(x, y).isPeak() or gc.getMap().plot(x, y).isCity():
			return []

		lDirectionList = []
		if iDirection == -1 or iDirection == DirectionTypes.DIRECTION_NORTH:
			if y < 68:
				lDirectionList.append((0, 1))
		if iDirection == -1 or iDirection == DirectionTypes.DIRECTION_SOUTH:
			if y > 0:
				lDirectionList.append((0, -1))
		if iDirection == -1 or iDirection == DirectionTypes.DIRECTION_EAST:
			if x < 124:
				lDirectionList.append((1, 0))
			else:
				lDirectionList.append((-124, 0))
		if iDirection == -1 or iDirection == DirectionTypes.DIRECTION_WEST:
			if x > 0:
				lDirectionList.append((-1, 0))
			else:
				lDirectionList.append((124, 0))

		for tDirection in lDirectionList:
			dx, dy = tDirection
			nx = x + dx
			ny = y + dy
			if gc.getMap().plot(nx, ny).getOwner() != iCiv:
				return [tPlot]

		return []

	# Leoreth: return list of border plots in a given direction, -1 means all directions
	def getBorderPlotList(self, iCiv, iDirection):
		lPlotList = []

		for x in range(124):
			for y in range(68):
				if gc.getMap().plot(x, y).getOwner() == iCiv:
					lPlotList.extend(self.testBorderPlot((x, y), iCiv, iDirection))

		# exclude Mediterranean islands
		for tPlot in [(68, 39), (69, 39), (71, 40)]:
			if tPlot in lPlotList:
				lPlotList.remove(tPlot)

		return lPlotList
		
	def isPlotInArea(self, tPlot, tTopLeft, tBottomRight, lExceptions=()):
		x, y = tPlot
		tlx, tly = tTopLeft
		brx, bry = tBottomRight
		
		return (x >= tlx and x <= brx and y >= tly and y <= bry and tPlot not in lExceptions)
		
	def relocateCapital(self, iPlayer, newCapital):
		oldCapital = gc.getPlayer(iPlayer).getCapitalCity()
		
		newCapital.setHasRealBuilding(con.iPalace, True)
		oldCapital.setHasRealBuilding(con.iPalace, False)
		
	def getFreePlot(self, x, y):
		pPlot = gc.getMap().plot(x, y)
		lFreePlots = []
		
		if not (pPlot.isCity() or pPlot.isPeak() or pPlot.isWater()):
			return (x, y)
			
		for i in range(x-1, x+2):
			for j in range(y-1, y+2):
				pPlot = gc.getMap().plot(i, j)
				if not (pPlot.isCity() or pPlot.isPeak() or pPlot.isWater()):
					lFreePlots.append((i, j))
					
		iRand = gc.getGame().getSorenRandNum(len(lFreePlots), 'random plot')
		return lFreePlots[iRand]
			
	
	
	