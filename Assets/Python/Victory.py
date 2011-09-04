# Rhye's and Fall of Civilization - Historical Victory Goals


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

# obsolete - edead
# i850BC = con.i850BC #new timeline
# i700BC = con.i700BC
# i250BC = con.i250BC #new timeline
# i100BC = con.i100BC #new timeline
# i50AD = con.i50AD
# i140AD = con.i140AD #new timeline
# i170AD = con.i170AD
# i200AD = con.i200AD #new timeline
# i250AD = con.i250AD
# i350AD = con.i350AD
# i450AD = con.i450AD
# i470AD = con.i470AD #new timeline
# i500AD = con.i500AD #new timeline
# i600AD = con.i600AD
# i700AD = con.i700AD
# i900AD = con.i900AD
# i1000AD = con.i1000AD
# i1200AD = con.i1200AD
# i1300AD = con.i1300AD
# i1400AD = con.i1400AD
# i1450AD = con.i1450AD
# i1500AD = con.i1500AD
# i1600AD = con.i1600AD
# i1650AD = con.i1650AD
# i1700AD = con.i1700AD
# i1715AD = con.i1715AD
# i1730AD = con.i1730AD
# i1745AD = con.i1745AD
# i1760AD = con.i1760AD
# i1775AD = con.i1775AD
# i1800AD = con.i1800AD
# i1820AD = con.i1820AD
# i1850AD = con.i1850AD
# i1860AD = con.i1860AD
# i1870AD = con.i1870AD
# i1880AD = con.i1880AD
# i1900AD = con.i1900AD
# i1910AD = con.i1910AD
# i1930AD = con.i1930AD
# i1940AD = con.i1940AD
# i1950AD = con.i1950AD
# i2000AD = con.i2000AD


iAncient = con.iAncient
iClassical = con.iClassical
iMedieval = con.iMedieval
iRenaissance = con.iRenaissance
iIndustrial = con.iIndustrial
iModern = con.iModern
iFuture = con.iFuture

tCoreAreasTL = con.tCoreAreasTL
tCoreAreasBR = con.tCoreAreasBR
tNormalAreasTL = con.tNormalAreasTL
tNormalAreasBR = con.tNormalAreasBR
tAmericasTL = con.tAmericasTL
tAmericasBR = con.tAmericasBR
tSAmericaTL = (24, 3)
tSAmericaBR = (43, 32)
tNCAmericaTL = (3, 33)
tNCAmericaBR = (37, 63)
tCAmericaTL = (12, 33)
tCAmericaBR = (33, 43)
tSiberiaTL = (82, 50)
tSiberiaBR = (112, 64)
tNECanadaTL = (22, 50)
tNECanadaBR = (37, 60)
tLouisianaTL = (19, 42)
tLouisianaBR = (24, 50)
tEastCoastTL = (25, 42)
tEastCoastBR = (35, 52)
tSouthAfricaTL = (61, 10)
tSouthAfricaBR = (72, 18)
tAustraliaTL = (103, 10)
tAustraliaBR = (118, 22)
tScandinaviaTL = (57, 55)
tScandinaviaBR = (65, 65)
tNearEastTL = (70, 37)
tNearEastBR = (78, 45)
tCarthageTL = (50, 36)
tCarthageBR = (61, 39)
tAfricaTL = (45, 10)
tAfricaBR = (76, 39)
tAsiaTL = (73, 29)
tAsiaBR = (121, 64)
tOceaniaTL = (99, 5)
tOceaniaBR = (123, 28)
tMediterraneanTL = (51, 36)
tMediterraneanBR = (73, 47)
tMediterraneanExceptions = ((51,36),(51,46),(52,46),(53,46),(53,47),(67,47),(67,46),(73,44),(73,45),(72,45),(71,44),(70,44),(73,36))
tHokkaidoTL = (115, 50)
tHokkaidoBR = (116, 52)
tHonshuTL = (112, 44)
tHonshuBR = (116, 49)
tBalkansTL = (64, 40)
tBalkansBR = (68, 47)
tBlackSeaTL = (67, 44)
tBlackSeaBR = (76, 50)
tMesopotamiaTL = (73, 37)
tMesopotamiaBR = (78, 42)
tFranceTL = (51, 47)
tEuropeTL = (44, 40)
tEuropeBR = (68, 65)
##tNubiaTL = (67, 29)
##tNubiaBR = (74, 32)
##tEastAfricaTL = (67, 20)
##tEastAfricaBR = (77, 28)
tSomaliaTL = (73, 24)
tSomaliaBR = (77, 29)
tSubeqAfricaTL = (60, 10)
tSubeqAfricaBR = (72, 29)
tBrazilTL = (32, 14)
tBrazilBR = (43, 30)
tLibyaTL = (59, 35)
tLibyaBR = (66, 37)
tBalkansTL = (64, 40)
tBalkansBR = (68, 47)
tNorthAfricaTL = (58, 32)
tNorthAfricaBR = (71, 38)
tNearEastTL = (69, 37)
tNearEastBR = (76, 45)

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
iEthiopia = con.iEthiopia
iKorea = con.iKorea
iMaya = con.iMaya
iByzantium = con.iByzantium
iVikings = con.iVikings
iArabia = con.iArabia
iKhmer = con.iKhmer
iIndonesia = con.iIndonesia
iSpain = con.iSpain
iFrance = con.iFrance
iEngland = con.iEngland
iGermany = con.iGermany
iRussia = con.iRussia
iNetherlands = con.iNetherlands
iHolland = con.iHolland
iMali = con.iMali
iTurkey = con.iTurkey
iPortugal = con.iPortugal
iInca = con.iInca
iMongolia = con.iMongolia
iAztecs = con.iAztecs
iAmerica = con.iAmerica
iNumPlayers = con.iNumPlayers
iNumMajorPlayers = con.iNumMajorPlayers
iNumActivePlayers = con.iNumActivePlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iNative = con.iNative
iCeltia = con.iCeltia
iBarbarian = con.iBarbarian
iNumTotalPlayers = con.iNumTotalPlayers


pEgypt = gc.getPlayer(iEgypt)
pIndia = gc.getPlayer(iIndia)
pChina = gc.getPlayer(iChina)
pBabylonia = gc.getPlayer(iBabylonia)
pGreece = gc.getPlayer(iGreece)
pPersia = gc.getPlayer(iPersia)
pCarthage = gc.getPlayer(iCarthage)
pRome = gc.getPlayer(iRome)
pJapan = gc.getPlayer(iJapan)
pEthiopia = gc.getPlayer(iEthiopia)
pKorea = gc.getPlayer(iKorea)
pMaya = gc.getPlayer(iMaya)
pByzantium = gc.getPlayer(iByzantium)
pVikings = gc.getPlayer(iVikings)
pArabia = gc.getPlayer(iArabia)
pKhmer = gc.getPlayer(iKhmer)
pIndonesia = gc.getPlayer(iIndonesia)
pSpain = gc.getPlayer(iSpain)
pFrance = gc.getPlayer(iFrance)
pEngland = gc.getPlayer(iEngland)
pGermany = gc.getPlayer(iGermany)
pRussia = gc.getPlayer(iRussia)
pNetherlands = gc.getPlayer(iNetherlands)
pHolland = gc.getPlayer(iHolland)
pMali = gc.getPlayer(iMali)
pTurkey = gc.getPlayer(iTurkey)
pPortugal = gc.getPlayer(iPortugal)
pInca = gc.getPlayer(iInca)
pMongolia = gc.getPlayer(iMongolia)
pAztecs = gc.getPlayer(iAztecs)
pAmerica = gc.getPlayer(iAmerica)
pIndependent = gc.getPlayer(iIndependent)
pIndependent2 = gc.getPlayer(iIndependent2)
pNative = gc.getPlayer(iNative)
pCeltia = gc.getPlayer(iCeltia)
pBarbarian = gc.getPlayer(iBarbarian)

teamEgypt = gc.getTeam(pEgypt.getTeam())
teamIndia = gc.getTeam(pIndia.getTeam())
teamChina = gc.getTeam(pChina.getTeam())
teamBabylonia = gc.getTeam(pBabylonia.getTeam())
teamGreece = gc.getTeam(pGreece.getTeam())
teamPersia = gc.getTeam(pPersia.getTeam())
teamCarthage = gc.getTeam(pCarthage.getTeam())
teamRome = gc.getTeam(pRome.getTeam())
teamJapan = gc.getTeam(pJapan.getTeam())
teamEthiopia = gc.getTeam(pEthiopia.getTeam())
teamKorea = gc.getTeam(pKorea.getTeam())
teamMaya = gc.getTeam(pMaya.getTeam())
teamByzantium = gc.getTeam(pByzantium.getTeam())
teamVikings = gc.getTeam(pVikings.getTeam())
teamArabia = gc.getTeam(pArabia.getTeam())
teamKhmer = gc.getTeam(pKhmer.getTeam())
teamIndonesia = gc.getTeam(pIndonesia.getTeam())
teamSpain = gc.getTeam(pSpain.getTeam())
teamFrance = gc.getTeam(pFrance.getTeam())
teamEngland = gc.getTeam(pEngland.getTeam())
teamGermany = gc.getTeam(pGermany.getTeam())
teamRussia = gc.getTeam(pRussia.getTeam())
teamNetherlands = gc.getTeam(pNetherlands.getTeam())
teamHolland = gc.getTeam(pHolland.getTeam())
teamMali = gc.getTeam(pMali.getTeam())
teamTurkey = gc.getTeam(pTurkey.getTeam())
teamPortugal = gc.getTeam(pPortugal.getTeam())
teamInca = gc.getTeam(pInca.getTeam())
teamMongolia = gc.getTeam(pMongolia.getTeam())
teamAztecs = gc.getTeam(pAztecs.getTeam())
teamAmerica = gc.getTeam(pAmerica.getTeam())
teamIndependent = gc.getTeam(pIndependent.getTeam())
teamIndependent2 = gc.getTeam(pIndependent2.getTeam())
teamNative = gc.getTeam(pNative.getTeam())
teamCeltia = gc.getTeam(pCeltia.getTeam())
teamBarbarian = gc.getTeam(pBarbarian.getTeam())




class Victory:

     
##################################################
### Secure storage & retrieval of script data ###
################################################   
		           

        def getGoal( self, i, j ):
                return sd.scriptDict['lGoals'][i][j]

        def setGoal( self, i, j, iNewValue ):
                sd.scriptDict['lGoals'][i][j] = iNewValue

        def getReligionFounded( self, iCiv ):
                return sd.scriptDict['lReligionFounded'][iCiv]

        def setReligionFounded( self, iCiv, iNewValue ):
                sd.scriptDict['lReligionFounded'][iCiv] = iNewValue

        def getEnslavedUnits( self ):
                return sd.scriptDict['iEnslavedUnits']

        def getRazedByMongols( self ):
                return sd.scriptDict['iRazedByMongols']
            
        def setRazedByMongols( self, iNewValue ):
                sd.scriptDict['iRazedByMongols'] = iNewValue

        def getEnglishEras( self, i ):
                return sd.scriptDict['lEnglishEras'][i]

        def setEnglishEras( self, i, iNewValue ):
                sd.scriptDict['lEnglishEras'][i] = iNewValue

        def getGreekTechs( self, i ):
                return sd.scriptDict['lGreekTechs'][i]

        def setGreekTechs( self, i, iNewValue ):
                sd.scriptDict['lGreekTechs'][i] = iNewValue
                
        def getWondersBuilt( self, iCiv ):
                return sd.scriptDict['lWondersBuilt'][iCiv]

        def setWondersBuilt( self, iCiv, iNewValue ):
                sd.scriptDict['lWondersBuilt'][iCiv] = iNewValue
                
        def get2OutOf3( self, iCiv ):
                return sd.scriptDict['l2OutOf3'][iCiv]

        def set2OutOf3( self, iCiv, bNewValue ):
                sd.scriptDict['l2OutOf3'][iCiv] = bNewValue

        def getNumSinks( self ):
                return sd.scriptDict['iNumSinks']
            
        def setNumSinks( self, iNewValue ):
                sd.scriptDict['iNumSinks'] = iNewValue

        def getBabylonianTechs( self, i ):
                return sd.scriptDict['lBabylonianTechs'][i]

        def setBabylonianTechs( self, i, iNewValue ):
                sd.scriptDict['lBabylonianTechs'][i] = iNewValue

        def getMediterraneanColonies( self ):
                return sd.scriptDict['iMediterraneanColonies']
            
        def setMediterraneanColonies( self, iNewValue ):
                sd.scriptDict['iMediterraneanColonies'] = iNewValue

        def getPortugueseColonies( self ):
                return sd.scriptDict['iPortugueseColonies']
            
        def setPortugueseColonies( self, iNewValue ):
                sd.scriptDict['iPortugueseColonies'] = iNewValue

        def getNewWorld( self, i ):
                return sd.scriptDict['lNewWorld'][i]

        def setNewWorld( self, i, iNewValue ):
                sd.scriptDict['lNewWorld'][i] = iNewValue

	def getChineseGoldenAgeTurns( self ):
		return sd.scriptDict['iChineseGoldenAges']

	def increaseChineseGoldenAgeTurns( self ):
		sd.scriptDict['iChineseGoldenAges'] += 1

	def getItalianTechs(self, i):
		return sd.scriptDict['lItalianTechs'][i]

	def setItalianTechs(self, i, iNewValue):
		sd.scriptDict['lItalianTechs'][i] = iNewValue

	def increaseItalianUniversities(self):
		sd.scriptDict['iItalianUniversities'] += 1

	def getItalianUniversities(self):
		return sd.scriptDict['iItalianUniversities']

	def getNumKoreanSinks(self):
		return sd.scriptDict['iNumKoreanSinks']

	def setNumKoreanSinks(self, iNewValue):
		sd.scriptDict['iNumKoreanSinks'] = iNewValue

	#def getKoreanTechs(self, i):
	#	return sd.scriptDict['lKoreanTechs'][i]

	#def setKoreanTechs(self, i, iNewValue):
	#	sd.scriptDict['lKoreanTechs'][i] = iNewValue

	def getNumGenerals(self):
		return sd.scriptDict['iNumGenerals']

	def setNumGenerals(self, iNewValue):
		sd.scriptDict['iNumGenerals'] = iNewValue
                
#######################################
### Main methods (Event-Triggered) ###
#####################################  


        def checkOwnedCiv(self, iActiveCiv, iOwnedCiv):
		reborn = utils.getReborn(iOwnedCiv)
                dummy1, plotList1 = utils.squareSearch( tNormalAreasTL[reborn][iOwnedCiv], tNormalAreasBR[reborn][iOwnedCiv], utils.ownedCityPlots, iActiveCiv )
                dummy2, plotList2 = utils.squareSearch( tNormalAreasTL[reborn][iOwnedCiv], tNormalAreasBR[reborn][iOwnedCiv], utils.ownedCityPlots, iOwnedCiv )
                if ((len(plotList1) >= 2 and len(plotList1) > len(plotList2)) or (len(plotList1) >= 1 and not gc.getPlayer(iOwnedCiv).isAlive())):
                        return True
                else:
                        return False


        def checkOwnedArea(self, iActiveCiv, tTopLeft, tBottomRight, iThreshold):
                dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.ownedCityPlots, iActiveCiv )
                if (len(plotList) >= iThreshold):
                        return True
                else:
                        return False


        def checkOwnedAreaAdjacentArea(self, iActiveCiv, tTopLeft, tBottomRight, iThreshold, tPlotArea):
                dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.ownedCityPlotsAdjacentArea, [iActiveCiv, tPlotArea])
                if (len(plotList) >= iThreshold):
                        print(len(plotList))
                        return True
                else:
                        print(len(plotList))
                        return False

                    
        def checkFoundedArea(self, iActiveCiv, tTopLeft, tBottomRight, iThreshold):
                dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.foundedCityPlots, iActiveCiv )
                if (len(plotList) >= iThreshold):

                        return True
                else:
                        return False

        def checkNotOwnedArea(self, iActiveCiv, tTopLeft, tBottomRight):
                dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.ownedCityPlots, iActiveCiv )
                if (len(plotList)):
                        return False
                else:
                        return True

        def checkNotOwnedArea_Skip(self, iActiveCiv, tTopLeft, tBottomRight, tSkipTopLeft, tSkipBottomRight):
                dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.ownedCityPlots, iActiveCiv )
                if (not len(plotList)):
                        return True
                else:
                        for loopPlot in plotList:
                                if not (loopPlot[0] >= tSkipTopLeft[0] and loopPlot[0] <= tSkipBottomRight[0] and \
                                    loopPlot[1] >= tSkipTopLeft[1] and loopPlot[1] <= tSkipBottomRight[1]):
                                        return False
                return True
                                        

        def checkOwnedCoastalArea(self, iActiveCiv, tTopLeft, tBottomRight, iThreshold):
                dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.ownedCityPlots, iActiveCiv )
                iCounter = 0
                for i in range(len(plotList)):
                        x = plotList[i][0]
                        y = plotList[i][1]
                        plot = gc.getMap().plot(x, y)
                        if (plot.isCity()):
                               if (plot.getPlotCity().isCoastalOld()):
                                       iCounter += 1
                if (iCounter >= iThreshold):
                        return True
                else:
                        return False

        def checkOwnedCoastalAreaExceptions(self, iActiveCiv, tTopLeft, tBottomRight, tExceptionList, iThreshold):
                dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.ownedCityPlots, iActiveCiv )
                iCounter = 0
                for i in range(len(plotList)):
                        x = plotList[i][0]
                        y = plotList[i][1]
                        plot = gc.getMap().plot(x, y)
                        if (plot.isCity()):
                               if (plot.getPlotCity().isCoastalOld()):
                                       bOK = True
                                       for j in tExceptionList:
                                               if (x == j[0] and y == j[1]):
                                                       bOK = False
                                                       break
                                       if (bOK):
                                               iCounter += 1
                if (iCounter >= iThreshold):
                        return True
                else:
                        return False

	def getNumberOfCoastalAreaCities(self, iCiv, tTopLeft, tBottomRight, tExceptionList):
		dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.ownedCityPlots, iCiv )
                iCounter = 0
                for i in range(len(plotList)):
                        x = plotList[i][0]
                        y = plotList[i][1]
                        plot = gc.getMap().plot(x, y)
                        if (plot.isCity()):
                               if (plot.getPlotCity().isCoastalOld()):
                                       bOK = True
                                       for j in tExceptionList:
                                               if (x == j[0] and y == j[1]):
                                                       bOK = False
                                                       break
                                       if (bOK):
                                               iCounter += 1
		return iCounter

        def checkFoundedCoastalArea(self, iActiveCiv, tTopLeft, tBottomRight, iThreshold):
                dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.foundedCityPlots, iActiveCiv )
                iCounter = 0
                for i in range(len(plotList)):
                        x = plotList[i][0]
                        y = plotList[i][1]
                        plot = gc.getMap().plot(x, y)
                        if (plot.isCity()):
                               if (plot.getPlotCity().isCoastalOld()):
                                       iCounter += 1
                if (iCounter >= iThreshold):
                        return True
                else:
                        return False

        def checkTurn(self, iGameTurn):

                #debug
                #self.setGoal(iEgypt, 0, 1)
                #self.setGoal(iEgypt, 1, 1)
                #self.setGoal(iEgypt, 2, 1)

                pass
                #for iCiv in range(iNumPlayers):
                #    print (iCiv, self.getGoal(iCiv, 0), self.getGoal(iCiv, 1), self.getGoal(iCiv, 2))


                    
       	
        def checkPlayerTurn(self, iGameTurn, iPlayer):


                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return
                
                if (iPlayer == iEgypt):
                        if (pEgypt.isAlive()):
                            
                                # added recalc of culture thresholds in line with game speed - edead
                                if (iGameTurn == getTurnForYear(-850)):
                                        if (pEgypt.countTotalCulture() >= utils.getTurns(500)):
                                                self.setGoal(iEgypt, 0, 1)
                                        else:
                                                self.setGoal(iEgypt, 0, 0)
                                                
                                if (iGameTurn == getTurnForYear(170)):
                                        if (pEgypt.countTotalCulture() >= utils.getTurns(5000)):
                                                self.setGoal(iEgypt, 2, 1)
                                        else:
                                                self.setGoal(iEgypt, 2, 0)
                                                
                                if (iGameTurn == getTurnForYear(-100)+1):
                                        if (self.getGoal(iEgypt, 1) == -1):                                  
                                                self.setGoal(iEgypt, 1, 0)                      

                                                
                elif (iPlayer == iIndia):
                        if (pIndia.isAlive()):                                                            
                                                                
                                if (iGameTurn == getTurnForYear(1200)):
                                        iPop = pIndia.getRealPopulation()
                                        #iPop = pIndia.getTotalPopulation()
                                        #print ("india pop", pIndia.getTotalPopulation(), pIndia.getRealPopulation())
                                        bFirst = True
                                        for iCiv in range(iNumPlayers):
                                                #print ("other pop", iCiv, gc.getPlayer(iCiv).getTotalPopulation(), gc.getPlayer(iCiv).getRealPopulation())
                                                if (iPop < gc.getPlayer(iCiv).getRealPopulation()):
                                                        bFirst = False
                                                        break
                                        if (bFirst):                                                
                                                self.setGoal(iIndia, 2, 1)
                                        else:
                                                self.setGoal(iIndia, 2, 0)

                            
                        
                elif (iPlayer == iChina):
                        if (pChina.isAlive()):

                                if (self.getGoal(iChina, 0) == -1):
                                        if (iGameTurn > getTurnForYear(1000)):
                                                self.setGoal(iChina, 0, 0)

				# Leoreth - new condition: have 4 golden ages until 1850 AD
                                if (iGameTurn == getTurnForYear(1850)):      
                                        if (self.getGoal(iChina, 1) == -1):
                                                self.setGoal(iChina, 1, 0)

                                if (iGameTurn == getTurnForYear(1600)):
                                        if (pChina.getNumUnits() >= 120):
                                                self.setGoal(iChina, 2, 1)
                                        else:
                                                self.setGoal(iChina, 2, 0)

				if self.getChineseGoldenAgeTurns() >= utils.getTurns(32):
					self.setGoal(iChina, 1, 1)

				if pChina.isGoldenAge():
					self.increaseChineseGoldenAgeTurns()


                elif (iPlayer == iBabylonia):
                        if (pBabylonia.isAlive()):
                                if (iGameTurn == getTurnForYear(-850)):
                                        bestCity = self.calculateTopCityPopulation(76, 40)                                        
                                        if (bestCity != -1):
                                                print ("bestCity.getOwner()", bestCity.getOwner())
                                                if (bestCity.getOwner() == iBabylonia and bestCity.getX() == 76 and bestCity.getY() == 40):
                                                        self.setGoal(iBabylonia, 1, 1)
                                                else:
                                                        self.setGoal(iBabylonia, 1, 0)
                                        else:
                                                self.setGoal(iBabylonia, 1, 0)

                                if (iGameTurn == getTurnForYear(-700)):           
                                        bestCity = self.calculateTopCityCulture(76, 40)                                        
                                        if (bestCity != -1):
                                                print ("bestCity.getOwner()", bestCity.getOwner())
                                                if (bestCity.getOwner() == iBabylonia and bestCity.getX() == 76 and bestCity.getY() == 40):
                                                        self.setGoal(iBabylonia, 2, 1)
                                                else:
                                                        self.setGoal(iBabylonia, 2, 0)
                                        else:
                                                self.setGoal(iBabylonia, 2, 0)


                                                
                elif (iPlayer == iGreece):
                        if (pGreece.isAlive()):

#                                if (self.getGoal(iGreece, 2) == -1):
#                                        if (gc.getGame().getCircumnavigated() != -1):
#                                                if (gc.getGame().getCircumnavigated() == iGreece):
#                                                        self.setGoal(iGreece, 2, 1)
#                                                else:
#                                                        self.setGoal(iGreece, 2, 0)

				# Leoreth: new third UHV condition: Control Egypt, Phoenicia, Babylonia and Persia in 325 BC.
				if (iGameTurn == getTurnForYear(-325)):
                                        bEgypt = self.checkOwnedCiv(iGreece, iEgypt)
                                        bPhoenicia = self.checkOwnedCiv(iGreece, iCarthage)
                                        bBabylonia = self.checkOwnedCiv(iGreece, iBabylonia)
					bPersia = self.checkOwnedCiv(iGreece, iPersia)                                        
                                        if (bEgypt and bPhoenicia and bBabylonia and bPersia):
                                                self.setGoal(iGreece, 2, 1)
                                        else:
                                                self.setGoal(iGreece, 2, 0)


                        
                elif (iPlayer == iPersia):
                        if (pPersia.isAlive()):

                                if (self.getGoal(iPersia, 0) == -1):
                                        if (iGameTurn <= getTurnForYear(140)):
                                                totalLand = gc.getMap().getLandPlots()
                                                persianLand = pPersia.getTotalLand()
                                                if (totalLand > 0):
                                                        landPercent = (persianLand * 100.0) / totalLand
                                                else:
                                                        landPercent = 0.0
                                                        
                                                if (landPercent >= 7.995): #it's shown as 8.00 in the victory screen)
                                                        self.setGoal(iPersia, 0, 1)
                                        else:
                                                self.setGoal(iPersia, 0, 0)

                                if (self.getGoal(iPersia, 1) == -1):
                                        if (iGameTurn <= getTurnForYear(350)):
                                                iCounter = 0
                                                apCityList = PyPlayer(iPersia).getCityList()
                                                for i in range(con.iSpaceElevator+1 - con.iPyramid):
                                                        iWonder = i + con.iPyramid
                                                        iWonderFlag = 0                                                        
                                                        for pCity in apCityList:
                                                                if (pCity.hasBuilding(iWonder)):
                                                                        iWonderFlag = 1
                                                                        break
                                                        #print ("Persian UHV", iWonder, pPersia.getBuildingClassCount(iWonder), iWonderFlag)
                                                        #iCounter += pPersia.getBuildingClassCount(iWonder) #BUGGY!
                                                        iCounter += iWonderFlag
                                                for i in range(con.iMoaiStatues+1 - con.iArtemis):
                                                        iWonder = i + con.iArtemis
                                                        iWonderFlag = 0
                                                        for pCity in apCityList:
                                                                if (pCity.hasBuilding(iWonder)):
                                                                        iWonderFlag = 1
                                                                        break
                                                        iCounter += iWonderFlag
                                                for i in range(con.iWestminster+1 - con.iApostolicPalace):
                                                        iWonder = i + con.iApostolicPalace
                                                        iWonderFlag = 0
                                                        for pCity in apCityList:
                                                                if (pCity.hasBuilding(iWonder)):
                                                                        iWonderFlag = 1
                                                                        break
                                                        iCounter += iWonderFlag
                                                for pCity in apCityList:
                                                        if (pCity.hasBuilding(con.iFlavianAmphitheatre)):
                                                                iCounter += 1
                                                                break
                                                if (iCounter >= 7):
                                                        self.setGoal(iPersia, 1, 1)
                                        else:
                                                self.setGoal(iPersia, 1, 0)
                            
                                if (iGameTurn == getTurnForYear(350)):
                                        iCounter = 0
                                        for iReligion in range(con.iNumReligions):
                                                iCurrentShrine = con.iShrine + iReligion*4
                                                apCityList = PyPlayer(iPersia).getCityList()
                                                for pCity in apCityList:
                                                        if (pCity.hasBuilding(iCurrentShrine)):
                                                                iCounter += 1
                                                                break
                                                #iCounter += pPersia.getBuildingClassCount(con.iShrine + iReligion*4) #BUGGY!
                                        if (iCounter >= 2):
                                                self.setGoal(iPersia, 2, 1)
                                        else:
                                                self.setGoal(iPersia, 2, 0)



                                                
                elif (iPlayer == iCarthage):
                        if (pCarthage.isAlive()):


                                if (self.getGoal(iCarthage, 1) == -1):
                                        if (iGameTurn <= getTurnForYear(200)):
                                                #if (pCarthage.countOwnedBonuses(con.iDye) + pCarthage.getBonusImport(con.iDye) >= 3):
                                                if (pCarthage.getNumAvailableBonuses(con.iDye) >= 3):
                                                        self.setGoal(iCarthage, 1, 1)
                                        else:
                                                self.setGoal(iCarthage, 1, 0)
                                                
                                if (iGameTurn == getTurnForYear(-100)):                                              
                                        if (self.checkOwnedCoastalAreaExceptions(iCarthage, tMediterraneanTL, tMediterraneanBR, tMediterraneanExceptions, 5)):
                                                self.setGoal(iCarthage, 0, 1)
                                        else:
                                                self.setGoal(iCarthage, 0, 0)   
                                #if (self.getGoal(iCarthage, 1) == -1):
                                #        if (iGameTurn == getTurnForYear(350)+1):
                                #                self.setGoal(iCarthage, 1, 0)

                                    

#                                if (self.getGoal(iCarthage, 2) == -1):
#                                        if (gc.getGame().getCircumnavigated() != -1):
#                                                if (gc.getGame().getCircumnavigated() == iCarthage):
#                                                        self.setGoal(iCarthage, 2, 1)
#                                                else:
#                                                        self.setGoal(iCarthage, 2, 0)
				
				# Leoreth: new third UHV condition: have the largest map of the world in 200 AD
				if (iGameTurn == getTurnForYear(200)):
                                        lRevealedMap = con.l0Array
                                        for iCiv in range(iNumPlayers):
                                                for x in range(124):
                                                        for y in range(68):
                                                                if (gc.getMap().plot(x, y).isRevealed(iCiv, False)):
                                                                      lRevealedMap[iCiv] += 1
                                        bBestMap = True
                                        for iCiv in range(iNumPlayers):
                                                if (lRevealedMap[iCarthage] < lRevealedMap[iCiv]):                                                        
                                                        bBestMap = False
                                                        break

                                        if (bBestMap == True):
                                                self.setGoal(iCarthage, 2, 1)
                                        else:
                                                self.setGoal(iCarthage, 2, 0)

                elif (iPlayer == iRome):
                        if (pRome.isAlive()):
				if (not pRome.isReborn()):

                                	if (iGameTurn <= getTurnForYear(200)):
                                        	if (self.getGoal(iRome, 0) == -1):
                                                	iCounterBarracks = 0
                                                	iCounterAqueduct = 0
                                                	iCounterColosseum = 0
                                                	cityList = PyPlayer(iRome).getCityList()                                        
                                                	for city in cityList:
                                                        	if (city.hasBuilding(con.iBarracks)):
                                                                	iCounterBarracks += 1
                                                        	if (city.hasBuilding(con.iAqueduct)):
                                                        	        iCounterAqueduct += 1
                                                        	if (city.hasBuilding(con.iColosseum)):
                                                        	        iCounterColosseum += 1
        ##                                               	if (not city.isConnectedToCapital(iRome)):
        ##                                         	                bConditions = False
                                                	if (iCounterBarracks >= 5 and iCounterAqueduct >= 5 and iCounterColosseum >= 5):
                                                        	self.setGoal(iRome, 0, 1)
                                                        
                                	if (iGameTurn == getTurnForYear(200)+1):
                                        	if (self.getGoal(iRome, 0) == -1):
                                                	self.setGoal(iRome, 0, 0)  
                                    
                                	if (iGameTurn == getTurnForYear(300)):                                              
                                        	bSpain = self.checkOwnedArea(iRome, tCoreAreasTL[0][iSpain], tCoreAreasBR[0][iSpain], 2)
                                        	bFrance = self.checkOwnedArea(iRome, tFranceTL, tNormalAreasBR[0][iFrance], 3)
                                        	bEngland = self.checkOwnedArea(iRome, tCoreAreasTL[0][iEngland], tCoreAreasBR[0][iEngland], 1)
                                        	bCarthage = self.checkOwnedArea(iRome, tCarthageTL, tCarthageBR, 2)
						bByzantium = self.checkOwnedArea(iRome, tCoreAreasTL[0][iByzantium], tCoreAreasBR[0][iByzantium], 4)
						bEgypt = self.checkOwnedArea(iRome, tCoreAreasTL[0][iEgypt], tCoreAreasBR[0][iEgypt], 2)

                                       		if (bSpain and bFrance and bEngland and bCarthage and bByzantium and bEgypt):
                                        	        self.setGoal(iRome, 1, 1)   
                                        	else:
                                        	        self.setGoal(iRome, 1, 0)

                                                
                                	if (iGameTurn == getTurnForYear(1000)):      
                                        	if (self.getGoal(iRome, 2) == -1): #see onCityAcquired()
                                                	self.setGoal(iRome, 2, 1)

				else:

					if iGameTurn == getTurnForYear(1570):
						if self.getGoal(iRome, 1) == -1:
							self.setGoal(iRome, 1, 0)

					if (iGameTurn == getTurnForYear(1930)):
						bGreece = self.checkOwnedCiv(iRome, iGreece)
						bEthiopia = self.checkOwnedCiv(iRome, iEthiopia)
						bLibya = self.checkOwnedArea(iRome, tLibyaTL, tLibyaBR, 1)

						for iCiv in range(con.iNumPlayers):
							if (iCiv != iRome):
								if self.checkOwnedArea(iCiv, tLibyaTL, tLibyaBR, 1):
									bLibya = False

						if bGreece and bEthiopia and bLibya:
							self.setGoal(iRome, 2, 1)
						else:
							self.setGoal(iRome, 2, 0)

                        
                elif (iPlayer == iJapan):
                        if (pJapan.isAlive()):

                            
                                #if (iGameTurn == getTurnForYear(1650)):
                                #        bForeignPresence = False
                                #        #Honshu
                                #        for x in range(tHonshuTL[0], tHonshuBR[0]+1):
                                #                for y in range(tHonshuTL[1], tHonshuBR[1]+1):
                                #                        pCurrent = gc.getMap().plot(x,y)
                                #                        if (not pCurrent.isWater()):
                                #                                for iLoop in range(iNumMajorPlayers): #no minor civs
                                #                                        if (iLoop != iJapan):
                                #                                                if (pCurrent.getCulture(iLoop) > 0):
                                #                                                        bForeignPresence = True
                                #                                                        print (iPlayer, "presence in Japan")

                                #        print ("bForeignPresence ", bForeignPresence)
                                #        if (bForeignPresence == False):
                                #                self.setGoal(iJapan, 0, 1)
                                #        else:
                                #                self.setGoal(iJapan, 0, 0)

				# Leoreth: new first goal: three great generals by 1600 AD
				if iGameTurn == getTurnForYear(1600):
					if self.getGoal(iJapan, 0) == -1:
						self.setGoal(iJapan, 0, 0)


                                if (iGameTurn == getTurnForYear(1930)):
                                        if (gc.getGame().getTeamRank(iJapan) == 0):
                                                self.setGoal(iJapan, 1, 1)
                                        else:
                                                self.setGoal(iJapan, 1, 0)

                                                
##                                if (iGameTurn == getTurnForYear(1850)):      
##                                        if (self.getGoal(iJapan, 2) == -1): #see onCityAcquired()
##                                                self.setGoal(iJapan, 2, 1)
                                        


                elif (iPlayer == iEthiopia):
                        if (pEthiopia.isAlive()):

                                if (iGameTurn == getTurnForYear(1500)):
                                        bAfrica = True
                                        for iEuroCiv in range(iNumPlayers):
                                                if (iEuroCiv in con.lCivGroups[0]):
                                                        if (self.checkNotOwnedArea(iEuroCiv, tSomaliaTL, tSomaliaBR) == False):
                                                                bAfrica = False
                                                        if (self.checkNotOwnedArea(iEuroCiv, tSubeqAfricaTL, tSubeqAfricaBR) == False):
                                                                bAfrica = False
                                                        if (bAfrica == False):
                                                                break
                                        if (bAfrica):
                                                self.setGoal(iEthiopia, 1, 1)
                                        else:
                                                self.setGoal(iEthiopia, 1, 0)

                                if (iGameTurn == getTurnForYear(1910)):
                                        bAfrica = True
                                        for iEuroCiv in range(iNumPlayers):
                                                if (iEuroCiv in con.lCivGroups[0]):
                                                        if (self.checkNotOwnedArea(iEuroCiv, tSomaliaTL, tSomaliaBR) == False):
                                                                bAfrica = False
                                                        if (self.checkNotOwnedArea(iEuroCiv, tSubeqAfricaTL, tSubeqAfricaBR) == False):
                                                                bAfrica = False
                                                        if (bAfrica == False):
                                                                break
                                        if (bAfrica):
                                                self.setGoal(iEthiopia, 2, 1)
                                        else:
                                                self.setGoal(iEthiopia, 2, 0)

		elif (iPlayer == iKorea):
			if (pKorea.isAlive()):

				if (iGameTurn == getTurnForYear(1200)):
					if (self.getGoal(iKorea, 0) == -1):
						self.setGoal(iKorea, 0, 0)

                elif (iPlayer == iMaya):
                        if (pMaya.isAlive()):

                                if (iGameTurn == getTurnForYear(600)+1):
                                        if (self.getGoal(iMaya, 0) == -1): #see onTechAcquired()                                        
                                                self.setGoal(iMaya, 0, 0)

                                if (iGameTurn == getTurnForYear(900)+1):
                                        if (self.getGoal(iMaya, 1) == -1): #see onBuildingBuilt()
                                                self.setGoal(iMaya, 1, 0)

                                if (iGameTurn == getTurnForYear(1745)):      
                                        if (self.getGoal(iMaya, 2) == -1): #see onCityAcquired()
                                                self.setGoal(iMaya, 2, 1)

		elif (iPlayer == iByzantium):
			if (pByzantium.isAlive()):

				if (iGameTurn == getTurnForYear(1000)):
					if (pByzantium.getGold() >= 5000):
						self.setGoal(iByzantium, 0, 1)
					else:
						self.setGoal(iByzantium, 0, 0)

				if (iGameTurn == getTurnForYear(1200)):
					bCulture = False
					mostCulturedCity = self.calculateTopCityCulture(68, 45)
					if (mostCulturedCity != -1):
                                                if (mostCulturedCity.getOwner() == iByzantium and mostCulturedCity.getX() == 68 and mostCulturedCity.getY() == 45):
                                                        bCulture = True

					bLargest = False
					largestCity = self.calculateTopCityPopulation(68, 45)                                        
                                        if (largestCity != -1):
                                                if (largestCity.getOwner() == iByzantium and largestCity.getX() == 68 and largestCity.getY() == 45):
                                                        bLargest = True

					if (bCulture and bLargest):
						self.setGoal(iByzantium, 1, 1)
					else:
						self.setGoal(iByzantium, 1, 0)

				if (iGameTurn == getTurnForYear(1450)):
					bBalkans = self.checkOwnedArea(iByzantium, tBalkansTL, tBalkansBR, 3)
					bNorthAfrica = self.checkOwnedArea(iByzantium, tNorthAfricaTL, tNorthAfricaBR, 3)
					bNearEast = self.checkOwnedArea(iByzantium, tNearEastTL, tNearEastBR, 3)

					if bBalkans:
						print "Third Byzantine goal: Balkans."
					if bNorthAfrica:
						print "Third Byzantine goal: North Africa."
					if bNearEast:
						print "Third Byzantine goal: Near East."

					if (bBalkans and bNorthAfrica and bNearEast):
						self.setGoal(iByzantium, 2, 1)
					else:
						self.setGoal(iByzantium, 2, 0)
                                                

                elif (iPlayer == iVikings):
                        if (pVikings.isAlive()):

                                if (iGameTurn == getTurnForYear(1500)):
                                        if (pVikings.getGold() >= 5000):
                                                self.setGoal(iVikings, 0, 1)
                                        else:
                                                self.setGoal(iVikings, 0, 0)


                        
                elif (iPlayer == iArabia):
                        if (pArabia.isAlive()):


                                if (self.getGoal(iArabia, 2) == -1):
                                        religionPercent = gc.getGame().calculateReligionPercent(con.iIslam)
                                        #print ("religionPercent", religionPercent)
                                        if (religionPercent >= 40.0):
                                                self.setGoal(iArabia, 2, 1)

                                                

                                if (iGameTurn == getTurnForYear(1300)):
                                        iCounter = 0
                                        for iReligion in range(con.iNumReligions):
                                                iCurrentShrine = con.iShrine + iReligion*4
                                                apCityList = PyPlayer(iArabia).getCityList()
                                                for pCity in apCityList:
                                                        if (pCity.hasBuilding(iCurrentShrine)):
                                                                iCounter += 1
                                                                break
                                                #iCounter += pArabia.getBuildingClassCount(con.iShrine + iReligion*4) #BUGGY!                                                
                                                #print (iReligion, con.iShrine + iReligion*4, pArabia.getBuildingClassCount(con.iShrine + iReligion*4))
                                        if (iCounter >= 3):
                                                self.setGoal(iArabia, 0, 1)
                                        else:
                                                self.setGoal(iArabia, 0, 0)



                            
                                if (iGameTurn >= getTurnForYear(con.tBirth[iSpain])+1 and iGameTurn <= getTurnForYear(1300)):
                                        if (self.getGoal(iArabia, 1) == -1):
                                                bSpain = self.isControlledOrVassalized(iArabia, con.tCoreAreasTL[0][iSpain], con.tCoreAreasBR[0][iSpain])
                                                bMaghreb = self.isControlledOrVassalized(iArabia, tCarthageTL, tCarthageBR)
						bMesopotamia = self.isControlledOrVassalized(iArabia, con.tCoreAreasTL[0][iBabylonia], con.tCoreAreasBR[0][iBabylonia])
						bPersia = self.isControlledOrVassalized(iArabia, con.tCoreAreasTL[0][iPersia], con.tCoreAreasBR[0][iPersia])
                                                if (bSpain and bMaghreb and bMesopotamia and bPersia):
                                                        self.setGoal(iArabia, 1, 1)
                                elif (iGameTurn > getTurnForYear(1300)):
                                        if (self.getGoal(iArabia, 1) == -1):
                                                        self.setGoal(iArabia, 1, 0)



                elif (iPlayer == iKhmer):
                        if (pKhmer.isAlive()):

                                if (iGameTurn == getTurnForYear(1450)):
                                        print ("khmer culture", pKhmer.countTotalCulture())
                                        if (pKhmer.countTotalCulture() >= utils.getTurns(12000)):
                                                self.setGoal(iKhmer, 0, 1)
                                        else:
                                                self.setGoal(iKhmer, 0, 0)

                                                
                                if (iGameTurn == getTurnForYear(1450)):
                                        apCityList = PyPlayer(iKhmer).getCityList()
                                        iTotalPopulation = 0
                                        for pCity in apCityList:			
                                                iTotalPopulation += pCity.getPopulation()
                                        if (iTotalPopulation / len(apCityList) >= 10):
                                                self.setGoal(iKhmer, 1, 1)
                                        else:
                                                self.setGoal(iKhmer, 1, 0)                                        
                                        #bestCity = self.calculateTopCityPopulation(102, 34)                                        #if (bestCity != -1):
                                        #        if (bestCity.getOwner() == iKhmer and bestCity.getX() == 102 and bestCity.getY() == 34):
                                        #                self.setGoal(iKhmer, 1, 1)
                                        #        else:
                                        #                self.setGoal(iKhmer, 1, 0)


                                if (self.getGoal(iKhmer, 2) == -1):
                                        religionPercent = gc.getGame().calculateReligionPercent(con.iBuddhism)
                                        #print ("religionPercent", religionPercent)
                                        if (religionPercent >= 30.0):
                                                self.setGoal(iKhmer, 2, 1)

		elif (iPlayer == iIndonesia):
			if (pIndonesia.isAlive()):

				if iGameTurn == getTurnForYear(1300):
					if self.getHighestPopulationCiv(iIndonesia) == iIndonesia:
						self.setGoal(iIndonesia, 0, 1)
					else:
						self.setGoal(iIndonesia, 0, 0)

				if iGameTurn == getTurnForYear(1500):
					lHappinessBonuses = [con.iDye, con.iFur, con.iGems, con.iGold, con.iIncense, con.iIvory, con.iSilk, con.iSilver, con.iSpices, con.iSugar, con.iWine, con.iWhales, con.iCotton]
                                        iCounter = 0
					for iBonus in lHappinessBonuses:
						if pIndonesia.getNumAvailableBonuses(iBonus) > 0:
							iCounter += 1
					if iCounter >= 9:
						self.setGoal(iIndonesia, 1, 1)
					else:
						self.setGoal(iIndonesia, 1, 0)

				if iGameTurn == getTurnForYear(1940):
					totalPop = gc.getGame().getTotalPopulation()
					ourPop = teamIndonesia.getTotalPopulation()
					if (totalPop > 0):
						popPercent = (ourPop * 100.0) / totalPop
					else:
						popPercent = 0.0

					if popPercent >= 10.0:
						self.setGoal(iIndonesia, 2, 1)
					else:
						self.setGoal(iIndonesia, 2, 0)
						
                        
                elif (iPlayer == iSpain):
                        if (pSpain.isAlive()):

##                                if (self.getGoal(iSpain, 0) == -1):
##                                        if (gc.getGame().getCircumnavigated() != -1):
##                                                if (gc.getGame().getCircumnavigated() == iSpain):
##                                                        self.setGoal(iSpain, 0, 1)
##                                                else:
##                                                        self.setGoal(iSpain, 0, 0)

                                                    

#                                if (iGameTurn == getTurnForYear(1700)):
#                                        bAmericas = True
#                                        if (self.checkNotOwnedArea(iFrance, tAmericasTL, tAmericasBR) == False):
#                                                bAmericas = False
#                                        if (self.checkNotOwnedArea(iEngland, tAmericasTL, tAmericasBR) == False):
#                                                bAmericas = False
#                                        if (self.checkNotOwnedArea(iNetherlands, tAmericasTL, tAmericasBR) == False):
#                                                bAmericas = False
#                                        if (bAmericas):
#                                                self.setGoal(iSpain, 1, 1)
#                                        else:
#                                                self.setGoal(iSpain, 1, 0)

				# Leoreth: Aztec & Inca by 1700 AD
                                if (iGameTurn == getTurnForYear(1700)):
                                        bAztecs = self.checkOwnedCiv(iSpain, iAztecs)
                                        bInca = self.checkOwnedCiv(iSpain, iInca)                                        
                                        if (bAztecs and bInca):
                                                self.setGoal(iSpain, 2, 1)
                                        else:
                                                self.setGoal(iSpain, 2, 0)

				# Leoreth: Have the largest empire of the world in 1760 AD
				if (iGameTurn == getTurnForYear(1760)):
					iSpanishLand = pSpain.getTotalLand()
					bLargest = True
					
					for iCiv in range(0,iNumMajorPlayers):
						if (gc.getPlayer(iCiv).getTotalLand() > iSpanishLand):
							bLargest = False

					if bLargest:
						self.setGoal(iSpain, 1, 1)
					else:
						self.setGoal(iSpain, 1, 0)
                            
                        
                elif (iPlayer == iFrance):
                        if (pFrance.isAlive()):
                            
                                if (iGameTurn == getTurnForYear(1700)):
                                        bestCity = self.calculateTopCityCulture(55, 50)
                                        if (bestCity != -1):
                                                if (bestCity.getOwner() == iFrance and bestCity.getX() == 55 and bestCity.getY() == 50):
                                                        self.setGoal(iFrance, 0, 1)
                                                else:
                                                        self.setGoal(iFrance, 0, 0)
                                        else:
                                                self.setGoal(iFrance, 0, 0)
                                                        
                                if (iGameTurn == getTurnForYear(1760)):
                                        if (self.getGoal(iFrance, 1) == -1):
                                                self.setGoal(iFrance, 1, 0)

                                            
                        
                elif (iPlayer == iEngland):
                        if (pEngland.isAlive()):


#                                if (self.getGoal(iEngland, 0) == -1):
#                                        if (gc.getGame().getCircumnavigated() != -1):
#                                                if (gc.getGame().getCircumnavigated() == iEngland):
#                                                        self.setGoal(iEngland, 0, 1)
#                                                else:
#                                                        self.setGoal(iEngland, 0, 0)


                                if (iGameTurn == getTurnForYear(1730)):
                                        if (self.getGoal(iEngland, 1) == -1):
                                                self.setGoal(iEngland, 1, 0)

				# Leoreth: Total of 25 Frigates or Ships of the Line
				if (iGameTurn == getTurnForYear(1800)):

					iCShipOfTheLine = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_SHIP_OF_THE_LINE')
					iCFrigate = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_FRIGATE')

					iEnglishNavy = gc.getPlayer(iEngland).getUnitClassCount(iCFrigate) + gc.getPlayer(iEngland).getUnitClassCount(iCShipOfTheLine)

					if iEnglishNavy >= 25:
						self.setGoal(iEngland, 0, 1)
					else:
						self.setGoal(iEngland, 0, 0)
					


                elif (iPlayer == iGermany):
                        if (pGermany.isAlive()):

                                if (iGameTurn == getTurnForYear(1870)):
                                        bFrance = self.checkOwnedCiv(iGermany, iFrance)
                                        bRome = self.checkOwnedCiv(iGermany, iRome)
                                        bGreece = self.checkOwnedCiv(iGermany, iGreece)                                        
                                        if (bFrance and bRome and bGreece):
                                                self.setGoal(iGermany, 0, 1)
                                        else:
                                                self.setGoal(iGermany, 0, 0)
                                                        
                                if (iGameTurn == getTurnForYear(1940)):
                                        bRussia = self.checkOwnedCiv(iGermany, iRussia)
                                        bEngland = self.checkOwnedCiv(iGermany, iEngland)                                        
                                        bScandinavia = self.checkOwnedCiv(iGermany, iVikings)
                                        if (bRussia and bEngland and bScandinavia):
                                                self.setGoal(iGermany, 1, 1)
                                        else:
                                                self.setGoal(iGermany, 1, 0)
                        
                elif (iPlayer == iRussia):
                        if (pRussia.isAlive()):

                                if (iGameTurn == getTurnForYear(1700)):  
                                        if (self.getGoal(iRussia, 0) == -1):
                                                self.setGoal(iRussia, 0, 0)

                                if (iGameTurn == getTurnForYear(1950)+1):      
                                        if (self.getGoal(iRussia, 1) == -1): 
                                                self.setGoal(iRussia, 1, 0)

                                if (iGameTurn == getTurnForYear(1950)):                                                  
                                        if (self.getGoal(iRussia, 2) == -1): 
                                                self.setGoal(iRussia, 2, 1)



                elif (iPlayer == iNetherlands):
                        if (pNetherlands.isAlive()):

#                                if (iGameTurn == i1700AD):
#                                        lRevealedMap = con.l0Array
#                                        for iCiv in range(iNumPlayers):
#                                                for x in range(124):
#                                                        for y in range(68):
#                                                                if (gc.getMap().plot(x, y).isRevealed(iCiv, False)):
#                                                                      lRevealedMap[iCiv] += 1
#                                        bBestMap = True
#                                        for iCiv in range(iNumPlayers):
#                                                if (lRevealedMap[iNetherlands] < lRevealedMap[iCiv]):                                                        
#                                                        bBestMap = False
#                                                        break
#
#                                        if (bBestMap == True):
#                                                self.setGoal(iNetherlands, 0, 1)
#                                        else:
#                                                self.setGoal(iNetherlands, 0, 0)

				if ( iGameTurn <= getTurnForYear(1745) and self.getGoal( iNetherlands, 0 ) == - 1 ):
					pPlot = gc.getMap().plot( con.tCapitals[utils.getReborn(iNetherlands)][iNetherlands][0], con.tCapitals[utils.getReborn(iNetherlands)][iNetherlands][1])
					if ( pPlot.isCity() ):
						iGMerchant = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), "SPECIALIST_GREAT_MERCHANT")
						if ( pPlot.getPlotCity().getFreeSpecialistCount(iGMerchant) >= 3 ):
							self.setGoal( iNetherlands, 0, 1 )
				else:
					if ( self.getGoal( iNetherlands, 0 ) == - 1 ):
						self.setGoal( iNetherlands, 0, 0 )                                                


                                if (self.getGoal(iNetherlands, 2) == -1):
                                        if (iGameTurn <= getTurnForYear(1775)):
                                                #print ("Dutch goal", pNetherlands.countOwnedBonuses(con.iSpices), pNetherlands.getBonusImport(con.iSpices))
                                                #if (pNetherlands.countOwnedBonuses(con.iSpices) + pNetherlands.getBonusImport(con.iSpices) >= 7):
                                                if (pNetherlands.getNumAvailableBonuses(con.iSpices) >= 7):
                                                        self.setGoal(iNetherlands, 2, 1)
                                        else:
                                                self.setGoal(iNetherlands, 2, 0)
                        
                elif (iPlayer == iMali):
                        if (pMali.isAlive()):

                                if (iGameTurn == getTurnForYear(1300)-10): #temporary fix, they use too many specialist and make Mali UHV very hard
                                        if (not pFrance.isHuman()):
                                                if (pFrance.getGold() > utils.getTurns(2000)):
                                                        pFrance.setGold(pFrance.getGold()*50/100)
                                                elif (pFrance.getGold() > utils.getTurns(1000)):
                                                        pFrance.setGold(pFrance.getGold()*70/100)
                                                        

                                if (iGameTurn == getTurnForYear(1300)):
                                        iGold = pMali.getGold()
                                        for iCiv in range(iNumPlayers):
                                                if (iCiv != iMali and gc.getPlayer(iCiv).isAlive()):
                                                        if (gc.getPlayer(iCiv).getGold() > iGold):
                                                               self.setGoal(iMali, 0, 0)
                                                               return
                                        self.setGoal(iMali, 0, 1)
                                 
                                if (iGameTurn == getTurnForYear(1500)):
                                        if (pMali.getGold() >= utils.getTurns(4000)):
                                                self.setGoal(iMali, 1, 1)
                                        else:
                                                self.setGoal(iMali, 1, 0)
                                                
                                if (iGameTurn == getTurnForYear(1700)):
                                        if (pMali.getGold() >= utils.getTurns(16000)):
                                                self.setGoal(iMali, 2, 1)
                                        else:
                                                self.setGoal(iMali, 2, 0)

                elif (iPlayer == iTurkey):
                        if (pTurkey.isAlive()):

                                if (self.getGoal(iTurkey, 0) == -1):
                                        if (iGameTurn <= getTurnForYear(1500)):
                                                pIstanbulE = gc.getMap().plot( 68, 45 )
                                                pIstanbulE2 = gc.getMap().plot( 67, 45 )
                                                pIstanbulA = gc.getMap().plot( 69, 44 )
                                                if (pIstanbulE.isCity()):                                                        
                                                        if (pIstanbulE.getPlotCity().getOwner() == iTurkey):
                                                                self.setGoal(iTurkey, 0, 1)
                                                elif (pIstanbulA.isCity()):                                                        
                                                        if (pIstanbulA.getPlotCity().getOwner() == iTurkey):
                                                                self.setGoal(iTurkey, 0, 1)
                                                elif (pIstanbulE2.isCity()):                                                        
                                                        if (pIstanbulE2.getPlotCity().getOwner() == iTurkey):
                                                                self.setGoal(iTurkey, 0, 1)
                                        else:
                                                self.setGoal(iTurkey, 0, 0)


                                if (iGameTurn == getTurnForYear(1700)):
                                        bBalkans = self.checkOwnedArea(iTurkey, tBalkansTL, tBalkansBR, 3)
                                        bBlackSea = self.checkOwnedAreaAdjacentArea(iTurkey, tBlackSeaTL, tBlackSeaBR, 4, (71,47))
                                        bMesopotamia = self.checkOwnedArea(iTurkey, tMesopotamiaTL, tMesopotamiaBR, 3)
                                        if (bBalkans and bBlackSea and bMesopotamia):
                                                self.setGoal(iTurkey, 1, 1)
                                        else:
                                                self.setGoal(iTurkey, 1, 0)

                                if (iGameTurn == getTurnForYear(1870)):
                                        iCounter = 0
                                        for iCiv in range(iNumPlayers):
                                                if (iCiv != iTurkey):
                                                        if (gc.getPlayer(iCiv).isAlive()):
                                                                if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iTurkey)):
                                                                        iCounter += 1
                                        if (iCounter >= 3):
                                                self.setGoal(iTurkey, 2, 1)
                                        else:
                                                self.setGoal(iTurkey, 2, 0)



                elif (iPlayer == iPortugal):
                        if (pPortugal.isAlive()):

                                if (iGameTurn == getTurnForYear(1500)):
                                        lRevealedMap = con.l0Array
                                        for iCiv in range(iNumPlayers):
                                                for x in range(124):
                                                        for y in range(68):
                                                                if (gc.getMap().plot(x, y).isRevealed(iCiv, False)):
                                                                      lRevealedMap[iCiv] += 1
                                        bBestMap = True
                                        for iCiv in range(iNumPlayers):
                                                if (lRevealedMap[iPortugal] < lRevealedMap[iCiv]):                                                        
                                                        bBestMap = False
                                                        break

                                        if (bBestMap == True):
                                                self.setGoal(iPortugal, 0, 1)
                                        else:
                                                self.setGoal(iPortugal, 0, 0)

                                if (self.getGoal(iPortugal, 1) == -1):
                                        if (iGameTurn == getTurnForYear(1650)):
                                                iCount = 0
                                                for iLoopCiv in range(iNumMajorPlayers):
                                                        if (iLoopCiv != iPortugal):
                                                                if (teamPortugal.isOpenBorders(iLoopCiv)):
                                                                       iCount += 1
                                                if (iCount >= 12):                                                                    
                                                        self.setGoal(iPortugal, 1, 1)
                                                else:
                                                        self.setGoal(iPortugal, 1, 0)

                                    


                            
                        
                elif (iPlayer == iInca):
                        if (pInca.isAlive()):

                                if (iGameTurn == getTurnForYear(1600)):
                                        bSAmerica = True
                                        for iEuroCiv in range(iNumPlayers):
                                                if (iEuroCiv in con.lCivGroups[0]):
                                                        if (self.checkNotOwnedArea_Skip(iEuroCiv, tSAmericaTL, tSAmericaBR, tBrazilTL, tBrazilBR) == False):
                                                                bSAmerica = False
                                                                break
                                        if (bSAmerica):
                                                self.setGoal(iInca, 0, 1)
                                        else:
                                                self.setGoal(iInca, 0, 0)                                                

                                if (iGameTurn == getTurnForYear(1700)):
                                        if (pInca.getGold() >= utils.getTurns(3000)):
                                                self.setGoal(iInca, 1, 1)
                                        else:
                                                self.setGoal(iInca, 1, 0)
                                                
                                if (iGameTurn == getTurnForYear(1800)):
                                        bSAmerica = True
                                        for iEuroCiv in range(iNumPlayers):
                                                if (iEuroCiv in con.lCivGroups[0]):
                                                        if (self.checkNotOwnedArea_Skip(iEuroCiv, tSAmericaTL, tSAmericaBR, tBrazilTL, tBrazilBR) == False):
                                                                bSAmerica = False
                                                                break
                                        if (bSAmerica):
                                                self.setGoal(iInca, 2, 1)
                                        else:
                                                self.setGoal(iInca, 2, 0)            

                        
                elif (iPlayer == iMongolia):
                        if (pMongolia.isAlive()):

                                if (iGameTurn <= getTurnForYear(1300)):
                                        bChina = False
                                        if (self.getGoal(iMongolia, 0) == -1):
                                                bChina = self.checkOwnedCiv(iMongolia, iChina)                                    
                                                if (bChina):
                                                        self.setGoal(iMongolia, 0, 1)
                                else:
                                        if (self.getGoal(iMongolia, 0) == -1):
                                                        self.setGoal(iMongolia, 0, 0)


                                if (self.getGoal(iMongolia, 2) == -1):
                                        if (iGameTurn <= getTurnForYear(1500)):
                                                totalLand = gc.getMap().getLandPlots()
                                                mongolLand = pMongolia.getTotalLand()
                                                if (totalLand > 0):
                                                        landPercent = (mongolLand * 100.0) / totalLand
                                                else:
                                                        landPercent = 0.0
                                                        
                                                if (landPercent >= 11.995): #it's shown as 12.00 in the victory screen)
                                                        self.setGoal(iMongolia, 2, 1)
                                        else:
                                                self.setGoal(iMongolia, 2, 0)

                            
                        
                elif (iPlayer == iAztecs):
                        if (pAztecs.isAlive()):
                            
                                if (self.getGoal(iAztecs, 0) == -1):
                                        if (self.getEnslavedUnits() >= 5):
                                                self.setGoal(iAztecs, 0, 1)   
                                            
                                if (iGameTurn == getTurnForYear(1700)):
                                        bCAmerica = True
                                        for iEuroCiv in range(iNumPlayers):
                                                if (iEuroCiv in con.lCivGroups[0]):
                                                        if (self.checkNotOwnedArea(iEuroCiv, tCAmericaTL, tCAmericaBR) == False):
                                                                bCAmerica = False
                                                                break
                                        if (bCAmerica):
                                                self.setGoal(iAztecs, 1, 1)
                                        else:
                                                self.setGoal(iAztecs, 1, 0)          


##                                if (iGameTurn == getTurnForYear(1820)):
##                                        bestCity = self.calculateTopCityPopulation(18, 37)
##                                        if (bestCity != -1):
##                                                if (bestCity.getOwner() == iAztecs and bestCity.getX() == 18 and bestCity.getY() == 37):
##                                                        self.setGoal(iAztecs, 2, 1)
##                                                else:
##                                                        self.setGoal(iAztecs, 2, 0)

                        
                elif (iPlayer == iAmerica):
                        if (pAmerica.isAlive()):

                                if (iGameTurn == getTurnForYear(1930)):
                                        bAmericas = True
                                        for iEuroCiv in range(iNumPlayers):
                                                if (iEuroCiv in con.lCivGroups[0]):
                                                        if (self.checkNotOwnedArea(iEuroCiv, tNCAmericaTL, tNCAmericaBR) == False):
                                                                bAmericas = False
                                                                break
                                        if (bAmericas):
                                                self.setGoal(iAmerica, 0, 1)
                                        else:
                                                self.setGoal(iAmerica, 0, 0)

                                if (iGameTurn == getTurnForYear(2000)+1):
                                        if (self.getGoal(iAmerica, 1) == -1):
                                                if (self.getWondersBuilt(iAmerica) != 3):                                    
                                                        self.setGoal(iAmerica, 1, 0)

##                                if (iGameTurn == getTurnForYear(2000)):
##                                        iCounter = 0
##                                        for iCiv in range(iNumPlayers):
##                                                if (iCiv != iAmerica):
##                                                        if (gc.getPlayer(iCiv).isAlive()):
##                                                                if (self.checkOwnedCiv(iAmerica, iCiv)):
##                                                                        iCounter += 1
##                                        if (iCounter >= 4):
##                                                self.setGoal(iAmerica, 2, 1)
##                                        else:
##                                                self.setGoal(iAmerica, 2, 0)


                                if (self.getGoal(iAmerica, 2) == -1):
                                        if (iGameTurn <= getTurnForYear(2000)):
                                                #iCounter = pAmerica.countOwnedBonuses(con.iOil)
                                                iCounter = pAmerica.getNumAvailableBonuses(con.iOil) - pAmerica.getBonusImport(con.iOil)
                                                for iCiv in range(iNumPlayers):
                                                        if (iCiv != iAmerica):
                                                                if (gc.getPlayer(iCiv).isAlive()):
                                                                        if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iAmerica)):
                                                                                #iCounter += gc.getPlayer(iCiv).countOwnedBonuses(con.iOil)
                                                                                iCounter += gc.getPlayer(iCiv).getNumAvailableBonuses(con.iOil) - gc.getPlayer(iCiv).getBonusImport(con.iOil)
                                                if (iCounter >= 10):
                                                        self.setGoal(iAmerica, 2, 1)
                                        else:
                                                self.setGoal(iAmerica, 2, 0)                                                


                #generic checks
                pPlayer = gc.getPlayer(iPlayer)
                if (pPlayer.isAlive() and iPlayer < iNumMajorPlayers):
                    
                        if (self.get2OutOf3(iPlayer) == False):                              
                                if (utils.countAchievedGoals(iPlayer) == 2):
                                        #intermediate bonus
                                        self.set2OutOf3(iPlayer, True)
                                        if (gc.getPlayer(iPlayer).getNumCities() > 0): #this check is needed, otherwise game crashes
                                                capital = gc.getPlayer(iPlayer).getCapitalCity()
                                                capital.setHasRealBuilding(con.iTriumphalArch, True)
                                                if (pPlayer.isHuman()):
                                                        CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_VICTORY_INTERMEDIATE", ()), "", 0, "", ColorTypes(con.iPurple), -1, -1, True, True)
                                                        
                                                        for iCiv in range(iNumPlayers):
                                                                if (iCiv != iPlayer):
                                                                        pCiv = gc.getPlayer(iCiv)
                                                                        if (pCiv.isAlive()):
                                                                                iAttitude = pCiv.AI_getAttitude(iPlayer)
                                                                                if (iAttitude != 0):
                                                                                        pCiv.AI_setAttitudeExtra(iPlayer, iAttitude-1) #da controllare

                                                        iWarCounter = 0
                                                        iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'civs')
                                                        for i in range( iRndnum, iNumPlayers + iRndnum ):
                                                                iCiv = i % iNumPlayers
                                                                pCiv = gc.getPlayer(iCiv)
                                                                if (pCiv.isAlive() and pCiv.canContact(iPlayer)):                                                                
                                                                        if (pCiv.AI_getAttitude(iPlayer) == 0):
                                                                                teamCiv = gc.getTeam(pCiv.getTeam())
                                                                                if (not teamCiv.isAtWar(iPlayer) and not teamCiv.isDefensivePact(iPlayer) and not utils.isAVassal(iCiv)):
                                                                                        teamCiv.declareWar(iPlayer, True, -1)
                                                                                        iWarCounter += 1
                                                                                        if (iWarCounter == 2):
                                                                                                break
                                

                        if (gc.getGame().getWinner() == -1):                              
                                if (self.getGoal(iPlayer, 0) == 1 and self.getGoal(iPlayer, 1) == 1 and self.getGoal(iPlayer, 2) == 1):
                                        gc.getGame().setWinner(iPlayer, 7) #Historical Victory




        def onCityBuilt(self, city, iPlayer): #see onCityBuilt in CvRFCEventHandler

                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return
                    
                iGameTurn = gc.getGame().getGameTurn()

##                if (iPlayer == iCarthage):
##                        if (self.getGoal(iCarthage, 0) == -1):
##                                if (iGameTurn <= getTurnForYear(350)):
##                                        if (city.getX() >= tMediterraneanTL[0] and city.getX() <= tMediterraneanBR[0] and city.getY() >= tMediterraneanTL[1] and city.getY() <= tMediterraneanBR[1]):
##                                                if (city.isCoastalOld()):
##                                                        self.setMediterraneanColonies(self.getMediterraneanColonies() + 1)
##                                                if (self.getMediterraneanColonies() >= 7):
##                                                        self.setGoal(iCarthage, 0, 1)


                if (iPlayer == iVikings):
                        if (self.getGoal(iVikings, 2) == -1):
                                if (city.getX() >= tAmericasTL[0] and city.getX() <= tAmericasBR[0] and city.getY() >= tAmericasTL[1] and city.getY() <= tAmericasBR[1]):
##                                        bFirst = True
##                                        for iCiv in range(iNumPlayers):
##                                                if ((iCiv != iVikings) and (iCiv not in con.lCivGroups[5])):
##                                                        if (self.checkNotOwnedArea(iCiv, tAmericasTL, tAmericasBR) == False):
##                                                                bFirst = False
##                                                                break
##                                        if (bFirst):
                                        if (self.getNewWorld(0) == -1 or self.getNewWorld(0) == iPlayer):
                                                self.setGoal(iVikings, 2, 1)
                                                #failure moved to EventHandler

                
                elif (iPlayer == iSpain):
                        if (self.getGoal(iSpain, 0) == -1):
                                if (city.getX() >= tAmericasTL[0] and city.getX() <= tAmericasBR[0] and city.getY() >= tAmericasTL[1] and city.getY() <= tAmericasBR[1]):
##                                        bFirst = True                                        
##                                        for iCiv in range(iNumPlayers):
##                                                if ((iCiv != iSpain) and (iCiv not in con.lCivGroups[5])):
##                                                        if (self.checkNotOwnedArea(iCiv, tAmericasTL, tAmericasBR) == False):
##                                                                bFirst = False
##                                                                break
##                                        if (bFirst):
                                        if (self.getNewWorld(0) == -1 or self.getNewWorld(0) == iPlayer):
                                                self.setGoal(iSpain, 0, 1)
                                                #failure moved to EventHandler


                              
                elif (iPlayer == iFrance):
                        if (iGameTurn <= getTurnForYear(1760)):
                                if (self.getGoal(iFrance, 1) == -1):       
                                        bNECanada = self.checkFoundedArea(iFrance, tNECanadaTL, tNECanadaBR, 3)
                                        bLouisiana = self.checkFoundedArea(iFrance, tLouisianaTL, tLouisianaBR, 1) 
                                        if (bNECanada and bLouisiana):
                                                self.setGoal(iFrance, 1, 1)
                                                

                elif (iPlayer == iEngland):
                        if (iGameTurn <= getTurnForYear(1730)):
                                if (self.getGoal(iEngland, 1) == -1):
                                        #bEastCoast = self.checkOwnedArea(iEngland, tEastCoastTL, tEastCoastBR, 2)
                                        #bSouthAfrica = self.checkOwnedArea(iEngland, tSouthAfricaTL, tSouthAfricaBR, 1)
                                        #bAustralia = self.checkOwnedArea(iEngland, tAustraliaTL, tAustraliaBR, 2)
                                        #print ("English UHV:", bEastCoast, bSouthAfrica, bAustralia)
                                        #if (bEastCoast and bSouthAfrica and bAustralia):
                                        bNCAmerica = self.checkFoundedArea(iEngland, tNCAmericaTL, tNCAmericaBR, 3)
                                        bSAmerica = self.checkFoundedArea(iEngland, tSAmericaTL, tSAmericaBR, 3)
                                        bAfrica = self.checkFoundedArea(iEngland, tAfricaTL, tAfricaBR, 3)
                                        bAsia = self.checkFoundedArea(iEngland, tAsiaTL, tAsiaBR, 3)
                                        bOceania = self.checkFoundedArea(iEngland, tOceaniaTL, tOceaniaBR, 3)
                                        if (bNCAmerica and bSAmerica and bAfrica and bAsia and bOceania):
                                                self.setGoal(iEngland, 1, 1)


                elif (iPlayer == iRussia):
                        if (iGameTurn <= getTurnForYear(1700)):
                                if (self.getGoal(iRussia, 0) == -1):
                                        bSiberia = self.checkFoundedArea(iRussia, tSiberiaTL, tSiberiaBR, 7)                                    
                                        if (bSiberia):
                                                self.setGoal(iRussia, 0, 1)



                elif (iPlayer == iNetherlands):
                        if (self.getGoal(iNetherlands, 1) == -1):
                                if (city.getX() >= tAustraliaTL[0] and city.getX() <= tAustraliaBR[0] and city.getY() >= tAustraliaTL[1] and city.getY() <= tAustraliaBR[1]):
                                        bFirst = True                                        
                                        for iCiv in range(iNumPlayers):
                                                if ((iCiv != iNetherlands)):
                                                        if (self.checkNotOwnedArea(iCiv, tAustraliaTL, tAustraliaBR) == False):
                                                                bFirst = False
                                                                #print ("bFirst = False", iCiv)
                                                                break
                                        if (bFirst):
                                                self.setGoal(iNetherlands, 1, 1)
                                        else:
                                                self.setGoal(iNetherlands, 1, 0)

                elif (iPlayer == iPortugal):
                        if (self.getGoal(iPortugal, 2) == -1):
                                if (not (city.getX() >= tEuropeTL[0] and city.getX() <= tEuropeBR[0] and city.getY() >= tEuropeTL[1] and city.getY() <= tEuropeBR[1])):
                                        self.setPortugueseColonies(self.getPortugueseColonies() + 1)
                                        if (self.getPortugueseColonies() >= 15):
                                                self.setGoal(iPortugal, 2, 1)

                                                
                        
        def onReligionFounded(self, iReligion, iFounder):

                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return

                iPlayer = iFounder

                if (iFounder == iIndia):
                        self.setReligionFounded(iReligion, 1)

                if (self.getGoal(iIndia, 0) == -1):
                        if (iReligion == con.iHinduism):
                                if (iFounder != iIndia):
                                        self.setGoal(iIndia, 0, 0) 
                        elif (iReligion == con.iBuddhism):
                                if (iFounder != iIndia):
                                        self.setGoal(iIndia, 0, 0)
                        if (self.getReligionFounded(con.iHinduism) == 1 and self.getReligionFounded(con.iBuddhism) == 1):
                                self.setGoal(iIndia, 0, 1)     

                if (self.getGoal(iIndia, 1) == -1):
                        iCounter = 0
                        for i in range(con.iNumReligions):
                                if (self.getReligionFounded(i) == 1):
                                        iCounter += 1
                        if (iCounter >= 5):
                                self.setGoal(iIndia, 1, 1)

                        if (self.getGoal(iIndia, 1) == -1):
                                iFounded = 0
                                for iLoopReligion in range(con.iNumReligions):
                                        if (gc.getGame().isReligionFounded(iLoopReligion)):
                                                iFounded += 1
                                if (iFounded == con.iNumReligions):
                                        self.setGoal(iIndia, 1, 0)


                if (iPlayer == iEthiopia):
                        if (pEthiopia.isAlive()):
                                if (self.getGoal(iEthiopia, 0) == -1):
                                        self.setGoal(iEthiopia, 0, 1)

                elif (iReligion == con.iJudaism):
                        if (self.getGoal(iEthiopia, 0) == -1):
                                self.setGoal(iEthiopia, 0, 0)


        def onCityAcquired(self, owner, playerType, bConquest):

                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return

                iPlayer = owner
                iGameTurn = gc.getGame().getGameTurn()
                
		# Leoreth - condition replaced
                #if (iPlayer == iChina):
                #        if (pChina.isAlive()):
                #                if (bConquest):
                #                       if (self.getGoal(iChina, 1) == -1):
                #                                if (iGameTurn <= getTurnForYear(1400)):
                #                                        if (playerType == iBarbarian or playerType == iMongolia):
                #                                                self.setGoal(iChina, 1, 0)   

                if (iPlayer == iRome):
                        if (pRome.isAlive()):
                                if (bConquest):
                                        if (self.getGoal(iRome, 2) == -1):
                                                if (iGameTurn <= getTurnForYear(1000)):
                                                        if (playerType == iBarbarian):
                                                                self.setGoal(iRome, 2, 0)

##                elif (iPlayer == iJapan):
##                        if (pJapan.isAlive()):
##                                if (bConquest):
##                                        if (self.getGoal(iJapan, 2) == -1):
##                                                if (iGameTurn <= getTurnForYear(1850)):
##                                                        self.setGoal(iJapan, 2, 0)


                elif (iPlayer == iMaya):
                        if (pMaya.isAlive()):
                                if (bConquest):
                                        if (self.getGoal(iMaya, 2) == -1):
                                                if (iGameTurn <= getTurnForYear(1745)):
                                                        self.setGoal(iMaya, 2, 0)
                                        
                elif (iPlayer == iRussia):
                        if (pRussia.isAlive()):
                                if (bConquest):
                                        if (self.getGoal(iRussia, 2) == -1):
                                                if (iGameTurn <= getTurnForYear(1950)):
                                                        self.setGoal(iRussia, 2, 0)          


        def onCityRazed(self, iPlayer):

                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return

                if (iPlayer == iMongolia):
                        if (pMongolia.isAlive()):
                                self.setRazedByMongols(self.getRazedByMongols() + 1)
                                if (self.getGoal(iMongolia, 1) == -1):
                                        if (self.getRazedByMongols() >= 7):
                                                self.setGoal(iMongolia, 1, 1)

                                                


        def onTechAcquired(self, iTech, iPlayer):

                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return

                iGameTurn = gc.getGame().getGameTurn()

		# Babylonian UHV: Writing, Code of Laws, Monarchy
		if iTech == con.iWriting:
			if self.getBabylonianTechs(0) == -1:
				if iPlayer == iBabylonia:
					self.setBabylonianTechs(0, 1)
				else:
					self.setGoal(iBabylonia, 0, 0)

		elif iTech == con.iCodeOfLaws:
			if self.getBabylonianTechs(1) == -1:
				if iPlayer == iBabylonia:
					self.setBabylonianTechs(1, 1)
				else:
					self.setGoal(iBabylonia, 0, 0)

		elif iTech == con.iMonarchy:
			if self.getBabylonianTechs(2) == -1:
				if iPlayer == iBabylonia:
					self.setBabylonianTechs(2, 1)
				else:
					self.setGoal(iBabylonia, 0, 0)

		if iTech in [con.iWriting, con.iCodeOfLaws, con.iMonarchy]:
			if self.getBabylonianTechs(0) == 1 and self.getBabylonianTechs(1) == 1 and self.getBabylonianTechs(2) == 1:
				self.setGoal(iBabylonia, 0, 1)
	

                #if (iPlayer == iBabylonia):
                 #       if (pBabylonia.isAlive()):
                  #              if (self.getGoal(iBabylonia, 0) == -1): #eof error???
                   #                     if (iTech == con.iWriting):
                    #                            self.setBabylonianTechs(0, 1)
                     #                           for iCiv in range(iNumPlayers):
                      #                                  if (iCiv != iBabylonia):
                       #                                         if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
                        #                                                self.setBabylonianTechs(0, 0)
                         #               elif (iTech == con.iCodeOfLaws):
                          #                      self.setBabylonianTechs(1, 1)
                           #                     for iCiv in range(iNumPlayers):
                            #                            if (iCiv != iBabylonia):
                             #                                   if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
                              #                                          self.setBabylonianTechs(1, 0)
                               #         elif (iTech == con.iMonarchy):
                                #                self.setBabylonianTechs(2, 1)
                                 #               for iCiv in range(iNumPlayers):
                                  #                      if (iCiv != iBabylonia):
                                   #                             if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
                                    #                                    self.setBabylonianTechs(2, 0)
                                     #   print ("self.getBabylonianTechs", self.getBabylonianTechs(0), self.getBabylonianTechs(1), self.getBabylonianTechs(2))
                                      #  if (self.getBabylonianTechs(0) == 1 and self.getBabylonianTechs(1) == 1 and self.getBabylonianTechs(2) == 1):
                                       #         self.setGoal(iBabylonia, 0, 1)
                                        #elif (self.getBabylonianTechs(0) == 0 or self.getBabylonianTechs(1) == 0 or self.getBabylonianTechs(2) == 0):
                                         #       self.setGoal(iBabylonia, 0, 0)

		# Greek UHV: Literature, Drama, Philosophy
		if iTech == con.iLiterature:
			if self.getGreekTechs(0) == -1:
				if iPlayer == iGreece:
					self.setGreekTechs(0, 1)
				else:
					self.setGoal(iGreece, 0, 0)

		elif iTech == con.iDrama:
			if self.getGreekTechs(1) == -1:
				if iPlayer == iGreece:
					self.setGreekTechs(1, 1)
				else:
					self.setGoal(iGreece, 0, 0)

		elif iTech == con.iPhilosophy:
			if self.getGreekTechs(2) == -1:
				if iPlayer == iGreece:
					self.setGreekTechs(2, 1)
				else:
					self.setGoal(iGreece, 0, 0)

		if iTech in [con.iLiterature, con.iDrama, con.iPhilosophy]:
			if self.getGreekTechs(0) == 1 and self.getGreekTechs(1) == 1 and self.getGreekTechs(2) == 1:
				self.setGoal(iGreece, 0, 1)


                #elif (iPlayer == iGreece):
                 #       if (pGreece.isAlive()):
                  #              if (self.getGoal(iGreece, 0) == -1): #eof error???
                   #                     if (iTech == con.iLiterature):
                    #                            self.setGreekTechs(0, 1)
                     #                           for iCiv in range(iNumPlayers):
                      #                                  if (iCiv != iGreece):
                       #                                         if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
                        #                                                self.setGreekTechs(0, 0)
                         #               elif (iTech == con.iDrama):
                          #                      self.setGreekTechs(1, 1)
                           #                     for iCiv in range(iNumPlayers):
                            #                            if (iCiv != iGreece):
                             #                                   if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
                              #                                          self.setGreekTechs(1, 0)
                               #         elif (iTech == con.iPhilosophy):
                                #                self.setGreekTechs(2, 1)
                                 #               for iCiv in range(iNumPlayers):
                                  #                      if (iCiv != iGreece):
                                   #                             if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
                                    #                                    self.setGreekTechs(2, 0)
                                     #   print ("self.getGreekTechs", self.getGreekTechs(0), self.getGreekTechs(1), self.getGreekTechs(2))
                                      #  if (self.getGreekTechs(0) == 1 and self.getGreekTechs(1) == 1 and self.getGreekTechs(2) == 1):
                                       #         self.setGoal(iGreece, 0, 1)
                                        #elif (self.getGreekTechs(0) == 0 or self.getGreekTechs(1) == 0 or self.getGreekTechs(2) == 0):
                                         #       self.setGoal(iGreece, 0, 0)

		# Italian UHV: Banking, Education, Radio, Fascism
		if pRome.isReborn():
			if iTech == con.iBanking:
				if self.getItalianTechs(0) == -1:
					if iPlayer == iRome:
						self.setItalianTechs(0, 1)
					else:
						self.setGoal(iRome, 0, 0)

			elif iTech == con.iEducation:
				if self.getItalianTechs(1) == -1:
					if iPlayer == iRome:
						self.setItalianTechs(1, 1)
					else:
						self.setGoal(iRome, 0, 0)

			elif iTech == con.iRadio:
				if self.getItalianTechs(2) == -1:
					if iPlayer == iRome:
						self.setItalianTechs(2, 1)
					else:
						self.setGoal(iRome, 0, 0)

			elif iTech == con.iFascism:
				if self.getItalianTechs(3) == -1:
					if iPlayer == iRome:
						self.setItalianTechs(3, 1)
					else:
						self.setGoal(iRome, 0, 0)

			if iTech in [con.iBanking, con.iEducation, con.iRadio, con.iFascism]:
				if self.getItalianTechs(0) == 1 and self.getItalianTechs(1) == 1 and self.getItalianTechs(2) == 1 and self.getItalianTechs(3) == 1:
					self.setGoal(iRome, 0, 1)

		#elif (iPlayer == iRome):
                #       if (pRome.isAlive()):
		#		if (pRome.isReborn()):
		#			if (iTech == con.iBanking):
		#				self.setItalianTechs(0, 1)
		#				for iCiv in range(iNumPlayers):
		#					if (iCiv != iRome):
		#						if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
		#							self.setItalianTechs(0, 0)
		#			elif (iTech == con.iEducation):
		#				self.setItalianTechs(1, 1)
		#				for iCiv in range(iNumPlayers):
		#					if (iCiv != iRome):
		#						if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
		#							self.setItalianTechs(1, 0)
		#			elif (iTech == con.iRadio):
		#				self.setItalianTechs(2, 1)
		#				for iCiv in range(iNumPlayers):
		#					if (iCiv != iRome):
		#						if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
		#							self.setItalianTechs(2, 0)
		#			elif (iTech == con.iFascism):
		#				self.setItalianTechs(3, 1)
		#				for iCiv in range(iNumPlayers):
		#					if (iCiv != iRome):
		#						if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
		#							self.setItalianTechs(3, 0)
		#			if (self.getItalianTechs(0) == 1 and self.getItalianTechs(1) == 1 and self.getItalianTechs(2) == 1 and self.getItalianTechs(3) == 1):
		#				self.setGoal(iRome, 0, 1)
		#			elif (self.getItalianTechs(0) == 0 or self.getItalianTechs(1) == 0 or self.getItalianTechs(2) == 0 or self.getItalianTechs(3) == 0):
		#				self.setGoal(iRome, 0, 0)


                elif (iPlayer == iJapan):
                        if (pJapan.isAlive()):
                                if (iGameTurn >= getTurnForYear(1700) and pJapan.getCurrentEra() >= iModern):
                                        if (self.getGoal(iJapan, 2) == -1):
                                                bCompleted = True
                                                for iTech in range(con.iNumTechs):
                                                        if (teamJapan.isHasTech(iTech) == False):
                                                                bCompleted = False
                                                                return
                                                if (bCompleted):
                                                        for iCiv in range(iNumPlayers):
                                                                if (iCiv != iJapan):
                                                                        bOtherCompleted = True
                                                                        for iTech in range(con.iNumTechs):
                                                                                if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == False):
                                                                                        bOtherCompleted = False
                                                                                        break
                                                                        if (bOtherCompleted):
                                                                                break
                                                        if (not bOtherCompleted):
                                                                self.setGoal(iJapan, 2, 1)
                                                        else:
                                                                self.setGoal(iJapan, 2, 0)

		# Korean UHV: Printing Press
		if iTech == con.iPrintingPress:
			if self.getGoal(iKorea, 1) == -1:
				if iPlayer == iKorea:
					self.setGoal(iKorea, 1, 1)
				else:
					self.setGoal(iKorea, 1, 0)

		#elif (iPlayer == iKorea):
		#	if (pKorea.isAlive()):
		#		if (iTech == con.iPrintingPress):
		#			bFirst = True
		#			for iCiv in range(iNumPlayers):
		#				if (iCiv != iKorea):
		#					if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == True):
		#						bFirst = False
		#			if bFirst:
		#				self.setGoal(iKorea, 1, 1)
		#			else:
		#				self.setGoal(iKorea, 1, 0) 
                                                

                elif (iPlayer == iMaya):
                        if (pMaya.isAlive()):
                                if (self.getGoal(iMaya, 0) == -1): #eof error???
                                        if (iTech == con.iCalendar):
                                                if (iGameTurn <= getTurnForYear(600)):
                                                        self.setGoal(iMaya, 0, 1)



                elif (iPlayer == iEngland):
                        if (pEngland.isAlive()):
                                if (iGameTurn >= getTurnForYear(1300)):
                                        if (self.getGoal(iEngland, 2) == -1):
                                                englishEra = pEngland.getCurrentEra()
                                                if (englishEra == iIndustrial):
                                                        if (self.getEnglishEras(0) == -1): #just entered
                                                                bFirst = True
                                                                for iCiv in range(iNumPlayers):
                                                                        if (iCiv != iEngland):
                                                                                if (gc.getPlayer(iCiv).getCurrentEra() == iIndustrial):
                                                                                        bFirst = False
                                                                                        break
                                                                if (bFirst):
                                                                        self.setEnglishEras(0, 1)
                                                                else:
                                                                        self.setEnglishEras(0, 0)
                                                if (englishEra == iModern):
                                                        if (self.getEnglishEras(1) == -1): #just entered
                                                                bFirst = True
                                                                for iCiv in range(iNumPlayers):
                                                                        if (iCiv != iEngland):
                                                                                if (gc.getPlayer(iCiv).getCurrentEra() == iModern):
                                                                                        bFirst = False
                                                                                        break
                                                                if (bFirst):
                                                                        self.setEnglishEras(1, 1)
                                                                        if (self.getEnglishEras(0) == 1):
                                                                                self.setGoal(iEngland, 2, 1)
                                                                        else:
                                                                                self.setGoal(iEngland, 2, 0)
                                                                else:
                                                                        self.setEnglishEras(1, 0)
                                                                        self.setGoal(iEngland, 2, 0)

                                                                        


                
                elif (iPlayer == iGermany):
                        if (pGermany.isAlive()):
                                if (iGameTurn >= getTurnForYear(1700) and pGermany.getCurrentEra() >= iModern):
                                        if (self.getGoal(iGermany, 2) == -1):
                                                bCompleted = True
                                                for iTech in range(con.iNumTechs):
                                                        if (teamGermany.isHasTech(iTech) == False):
                                                                bCompleted = False
                                                                return
                                                if (bCompleted):
                                                        for iCiv in range(iNumPlayers):
                                                                if (iCiv != iGermany):
                                                                        bOtherCompleted = True
                                                                        for iTech in range(con.iNumTechs):
                                                                                if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iTech) == False):
                                                                                        bOtherCompleted = False
                                                                                        break
                                                                        if (bOtherCompleted):
                                                                                break
                                                        if (not bOtherCompleted):
                                                                self.setGoal(iGermany, 2, 1)
                                                        else:
                                                                self.setGoal(iGermany, 2, 0) 
                                                        

                elif (iPlayer == iAztecs):
                        if (self.getGoal(iAztecs, 2) == -1):
                                if (iGameTurn <= getTurnForYear(1860)):                            
                                        aztecEra = pAztecs.getCurrentEra()
                                        if (aztecEra == iIndustrial):
                                                self.setGoal(iAztecs, 2, 1)                                        
                                else:
                                        self.setGoal(iAztecs, 2, 0)
                                                



        def onBuildingBuilt(self, iPlayer, iBuilding):

                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return

                iGameTurn = gc.getGame().getGameTurn()

                if (iPlayer == iEgypt):
                        if (pEgypt.isAlive()):
                                if (self.getGoal(iEgypt, 1) == -1):
                                        if (iGameTurn <= getTurnForYear(-100)):
                                                if (iBuilding == con.iPyramid or iBuilding == con.iGreatLibrary or iBuilding == con.iGreatLighthouse):
                                                        self.setWondersBuilt(iEgypt, self.getWondersBuilt(iEgypt) + 1)
                                                if (self.getWondersBuilt(iEgypt) == 3):                                    
                                                        self.setGoal(iEgypt, 1, 1)
                                        if (iGameTurn >= getTurnForYear(-100)):
                                                if (self.getWondersBuilt(iEgypt) != 3):                                    
                                                        self.setGoal(iEgypt, 1, 0)      


                elif (iPlayer == iChina):
                        if (pChina.isAlive()):
                                if (self.getGoal(iChina, 0) == -1):
                                        if (iGameTurn <= getTurnForYear(1000)):
                                                if (iBuilding == con.iConfucianCathedral or iBuilding == con.iTaoistCathedral):
                                                        #iConfucianCounter = pChina.getBuildingClassCount(con.iConfucianCathedral)
                                                        #iTaoistCounter = pChina.getBuildingClassCount(con.iTaoistCathedral)
                                                        iConfucianCounter = 0
                                                        iTaoistCounter = 0
                                                        for iCity in range(pChina.getNumCities()):
                                                                pCity = pChina.getCity(iCity)
                                                                if (pCity.hasBuilding(con.iConfucianCathedral)):
                                                                        iConfucianCounter += 1
                                                                if (pCity.hasBuilding(con.iTaoistCathedral)):
                                                                        iTaoistCounter += 1
                                                        if (iConfucianCounter >= 2 and iTaoistCounter >= 2):
                                                                self.setGoal(iChina, 0, 1)
                                        else:
                                                self.setGoal(iChina, 0, 0)



                elif (iPlayer == iGreece):
                        if (pGreece.isAlive()):
                                if (self.getGoal(iGreece, 1) == -1):
                                        if (iGameTurn <= getTurnForYear(-250)):
                                                if (iBuilding == con.iOracle or iBuilding == con.iColossus or iBuilding == con.iParthenon or iBuilding == con.iArtemis):
                                                        self.setWondersBuilt(iGreece, self.getWondersBuilt(iGreece) + 1)
                                                if (self.getWondersBuilt(iGreece) == 4):                                    
                                                        self.setGoal(iGreece, 1, 1)
                                        if (iGameTurn > getTurnForYear(-250)):                                   
                                                self.setGoal(iGreece, 1, 0)

		elif (iPlayer == iKorea):
			if (pKorea.isAlive()):
				if (self.getGoal(iKorea, 0) == -1):
					if (iGameTurn <= getTurnForYear(1200)):
						if (iBuilding == con.iBuddhistCathedral or iBuilding == con.iConfucianCathedral):
							bBuddhistCathedral = (self.getNumBuildings(iKorea, con.iBuddhistCathedral) > 0)
							bConfucianCathedral = (self.getNumBuildings(iKorea, con.iConfucianCathedral) > 0)
							if (bBuddhistCathedral and bConfucianCathedral):
								self.setGoal(iKorea, 0, 1)
					else:
						self.setGoal(iKorea, 0, 0)     

                                                

                elif (iPlayer == iFrance):
                        if (pFrance.isAlive()):
                                if (self.getGoal(iFrance, 2) == -1):
                                        if (iGameTurn <= getTurnForYear(1900)):
                                                if (iBuilding == con.iNotreDame or iBuilding == con.iStatueOfLiberty or iBuilding == con.iEiffelTower):
                                                        self.setWondersBuilt(iFrance, self.getWondersBuilt(iFrance) + 1)
                                                if (self.getWondersBuilt(iFrance) == 3):                                    
                                                        self.setGoal(iFrance, 2, 1)
                                        if (iGameTurn > getTurnForYear(1900)):
                                                if (self.getWondersBuilt(iFrance) != 3):                                    
                                                        self.setGoal(iFrance, 2, 0)

		elif (iPlayer == iRome):
			if (pRome.isAlive() and pRome.isReborn()):
				if (self.getGoal(iRome, 1) == -1):
					if (iGameTurn <= getTurnForYear(1570)):
						if iBuilding == con.iUniversity:
							self.increaseItalianUniversities()
							if self.getItalianUniversities() == 3:
								self.setGoal(iRome, 1, 1)

                elif (iPlayer == iAmerica):
                        if (pAmerica.isAlive()):
                                if (self.getGoal(iAmerica, 1) == -1):
                                        if (iGameTurn <= getTurnForYear(2000)):
                                                if (iBuilding == con.iStatueOfLiberty or iBuilding == con.iPentagon or iBuilding == con.iUnitedNations):
                                                        self.setWondersBuilt(iAmerica, self.getWondersBuilt(iAmerica) + 1)
                                                if (self.getWondersBuilt(iAmerica) == 3):                                    
                                                        self.setGoal(iAmerica, 1, 1)
                                        if (iGameTurn > getTurnForYear(2000)):
                                                if (self.getWondersBuilt(iAmerica) != 3):                                    
                                                        self.setGoal(iAmerica, 1, 0)






                if (iBuilding == con.iTempleOfKukulkan):      
                        if (iPlayer == iMaya):
                                if (pMaya.isAlive()):
                                        if (self.getGoal(iMaya, 1) == -1):
                                                if (iGameTurn <= getTurnForYear(900)):                                                                            
                                                        self.setGoal(iMaya, 1, 1)
                        else:
                                self.setGoal(iMaya, 1, 0)


                            
        def onProjectBuilt(self, iPlayer, iProject):

                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return

                iGameTurn = gc.getGame().getGameTurn()

                if (iProject == con.iApolloProgram):
                        if (iPlayer == iRussia):
                                if (iGameTurn <= getTurnForYear(1950)):                                
                                        self.setGoal(iRussia, 1, 1)
                        else:
                                if (self.getGoal(iRussia, 1) == -1):
                                        self.setGoal(iRussia, 1, 0)



        def onCombatResult(self, argsList):
            
                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return

                pWinningUnit,pLosingUnit = argsList
                pWinningPlayer = gc.getPlayer(pWinningUnit.getOwner())
                pLosingPlayer = gc.getPlayer(pLosingUnit.getOwner())
                cLosingUnit = PyHelpers.PyInfo.UnitInfo(pLosingUnit.getUnitType())
                iPlayer = pWinningPlayer.getID()

                if (iPlayer == iVikings):
                        if (self.getGoal(iVikings, 1) == -1):
                                if (cLosingUnit.getDomainType() == gc.getInfoTypeForString("DOMAIN_SEA")):
                                        self.setNumSinks(self.getNumSinks() + 1)
                                        if (self.getNumSinks() == 25):
                                                self.setGoal(iVikings, 1, 1)

		elif (iPlayer == iKorea):
			if (self.getGoal(iKorea, 2) == -1):
				if (cLosingUnit.getDomainType() == gc.getInfoTypeForString("DOMAIN_SEA")):
					self.setNumKoreanSinks(self.getNumKoreanSinks() + 1)
					if (self.getNumKoreanSinks() == 20):
						self.setGoal(iKorea, 2, 1)

	def onGreatPersonBorn(self, argsList):
		pUnit, iPlayer, pCity = argsList
		
		iGameTurn = gc.getGame().getGameTurn()
		
		# Leoreth: new first goal for Japan: three great generals by 1600 AD
		if iPlayer == iJapan:
			if pUnit.getUnitClassType() == CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_GREAT_GENERAL'):
				if sd.getGoal(iJapan, 1) == -1:
					if gc.getGame().getGameTurn() <= getTurnForYear(1600):
						sd.setNumGenerals(sd.getNumGenerals() + 1)
						if sd.getNumGenerals() == 3:
							sd.setGoal(iJapan, 0, 1)
                                        


        def calculateTopCityCulture(self, x, y):
                iBestCityValue = 0
		if gc.getMap().plot(x,y).isCity():
                	pCurrent = gc.getMap().plot(x,y)
		else:
			for iCiv in range(con.iNumPlayers):
				if gc.getPlayer(iCiv).isAlive():
					pCurrent = gc.getPlayer(iCiv).getCapitalCity().plot()
					break
                if (pCurrent.isCity()):
                        bestCity = pCurrent.getPlotCity()
                        for iPlayerLoop in range(gc.getMAX_PLAYERS()):
                                apCityList = PyPlayer(iPlayerLoop).getCityList()

                                for pCity in apCityList:
                                        iTotalCityValue = pCity.GetCy().countTotalCultureTimes100()
                                        #iTotalCityValue = (pCity.getCulture() / 5) + (pCity.getFoodRate() + pCity.getProductionRate() \
                                        #	+ pCity.calculateGoldRate())) * pCity.getPopulation()
                                        if (iTotalCityValue > iBestCityValue and not pCity.isBarbarian()):
                                                bestCity = pCity
                                                iBestCityValue = iTotalCityValue
                        return bestCity
                return -1


        def calculateTopCityPopulation(self, x, y):
                iBestCityValue = 0
		if gc.getMap().plot(x,y).isCity():
                	pCurrent = gc.getMap().plot(x,y)
		else:
			for iCiv in range(con.iNumPlayers):		# we want to make sure this Algorithm always returns the best city
				if gc.getPlayer(iCiv).isAlive():	# so we always need a starting city
					pCurrent = gc.getPlayer(iCiv).getCapitalCity().plot()
					break
                if (pCurrent.isCity()):
                        bestCity = pCurrent.getPlotCity()
                        for iPlayerLoop in range(gc.getMAX_PLAYERS()):
                                apCityList = PyPlayer(iPlayerLoop).getCityList()

                                for pCity in apCityList:			
                                        iTotalCityValue = pCity.getPopulation()
                                        if (iTotalCityValue > iBestCityValue and not pCity.isBarbarian()):
                                                bestCity = pCity
                                                iBestCityValue = iTotalCityValue
                        return bestCity
                return -1


	def getNumBuildings(self, iPlayer, iBuilding):
		iCount = 0
		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			if pCity.getNumBuilding(iBuilding): iCount += 1
		return iCount


	def isHighestPopulation(self, iPlayer):
		iPop = gc.getPlayer(iPlayer).getRealPopulation()
		bHighest = True
		for iLoopCiv in range(con.iNumPlayers):
			if iPop < gc.getPlayer(iLoopCiv).getRealPopulation():
				bHighest = False
				break
		return bHighest

	
	def getHighestPopulationCiv(self, iPlayer):
		iTemp = iPlayer
		iPop = gc.getPlayer(iTemp).getRealPopulation()
		for iCiv in range(con.iNumPlayers):
			if iPop < gc.getPlayer(iCiv).getRealPopulation():
				iTemp = iCiv
				iPop = gc.getPlayer(iCiv).getRealPopulation()
		return iTemp


	def getHighestRankCiv(self):
		for iCiv in range(con.iNumPlayers):
			if gc.getGame().getTeamRank(iCiv) == 0:
				return iCiv

	def getLargestEmpireCiv(self, iPlayer):
		iBest = iPlayer
		iBestLand = gc.getPlayer(iPlayer).getTotalLand()
		for iCiv in range(con.iNumPlayers):
			iCurrentLand = gc.getPlayer(iCiv).getTotalLand()
			if iCurrentLand > iBestLand:
				iBest = iCiv
				iBestLand = iCurrentLand
		return iBest

	def getMostGoldCiv(self, iPlayer):
		iBest = iPlayer
		iBestGold = gc.getPlayer(iPlayer).getGold()
		for iCiv in range(con.iNumPlayers):
			iCurrentGold = gc.getPlayer(iCiv).getGold()
			if iCurrentGold > iBestGold:
				iBest = iCiv
				iBestGold = iCurrentGold
		return iBest

	# Leoreth: new implementation of the Arabian conquest goal
	# all cities in the area must now be held either by you or one of your vassals
	def isControlledOrVassalized(self, iPlayer, tTopLeft, tBottomRight):
		bControlled = False
		lOwnerList = []
		lValidOwners = [iPlayer]
		dummy, lCityPlotList = utils.squareSearch(tTopLeft, tBottomRight, utils.ownedCityPlots, iPlayer)
		for tPlot in lCityPlotList:
			x, y = tPlot
			if gc.getMap().plot(x,y).getPlotCity().getOwner() not in lOwnerList:
				lOwnerList.append(gc.getMap().plot(x,y).getPlotCity().getOwner())
		for iCiv in range(con.iNumPlayers):
			if gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iPlayer):
				lValidOwners.append(iCiv)
		for iCiv in lValidOwners:
			if iCiv in lOwnerList:
				bControlled = True		# you or one of your vassals holds at least one city
				lOwnerList.remove(iCiv)
		if len(lOwnerList) > 0:
			bControlled = False			# someone who's not your vassal holds at least one city
		return bControlled
		
			


	def getIcon(self, bVal):
		if bVal:
			return u"%c" %(CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 10)
		else:
			return u"%c" %(CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 11)


	def getUHVHelp(self, iPlayer, iGoal):
		"Returns an array of help strings used by the Victory Screen table"
		
		aHelp = [];
		
		# the info is outdated or irrelevant once the goal has been accomplished or failed
		if self.getGoal(iPlayer, iGoal) == 1:
			aHelp.append(self.getIcon(True) + 'Goal accomplished!')
			return aHelp
		elif self.getGoal(iPlayer, iGoal) == 0:
			aHelp.append(self.getIcon(False) + 'Goal failed!')
			return aHelp

		if iPlayer == iEgypt:
			if iGoal == 0:
				iCulture = pEgypt.countTotalCulture()
				aHelp.append(self.getIcon(iCulture >= utils.getTurns(500)) + 'Total culture: ' + str(iCulture) + '/' + str(utils.getTurns(500)))
			elif iGoal == 1:
				bPyramids = (self.getNumBuildings(iEgypt, con.iPyramid) > 0)
				bLibrary = (self.getNumBuildings(iEgypt, con.iGreatLibrary) > 0)
				bLighthouse = (self.getNumBuildings(iEgypt, con.iGreatLighthouse) > 0)
				aHelp.append(self.getIcon(bPyramids) + 'Pyramids ' + self.getIcon(bLibrary) + 'Great Library ' + self.getIcon(bLighthouse) + 'Great Lighthouse')
			elif iGoal == 2:
				iCulture = pEgypt.countTotalCulture()
				aHelp.append(self.getIcon(iCulture >= utils.getTurns(5000)) + 'Total culture: ' + str(iCulture) + '/' + str(utils.getTurns(5000)))

		elif iPlayer == iIndia:
			if iGoal == 0:
				bBuddhism = (self.getReligionFounded(con.iBuddhism) == 1)
				bHinduism = (self.getReligionFounded(con.iHinduism) == 1)
				aHelp.append(self.getIcon(bHinduism) + 'Hinduism ' + self.getIcon(bBuddhism) + 'Buddhism')
			elif iGoal == 1:
				iCount = 0
				for iReligion in range(con.iNumReligions):
					if self.getReligionFounded(iReligion) == 1:
						iCount += 1
				aHelp.append(self.getIcon(iCount >= 5) + 'Religions founded: ' + str(iCount) + '/5')
			elif iGoal == 2:
				iHighestCiv = self.getHighestPopulationCiv(iIndia)
				bHighest = (iHighestCiv == iIndia)
				aHelp.append(self.getIcon(bHighest) + 'Civilization with the largest population: ' + CyTranslator().getText(str(gc.getPlayer(iHighestCiv).getCivilizationShortDescriptionKey()),()))

		elif iPlayer == iChina:
			if iGoal == 0:
				iConfucianCounter = self.getNumBuildings(iChina, con.iConfucianCathedral)
				iTaoistCounter = self.getNumBuildings(iChina, con.iTaoistCathedral)
				aHelp.append(self.getIcon(iConfucianCounter >= 2) + 'Confucian Academies: ' + str(iConfucianCounter) + '/2' + self.getIcon(iTaoistCounter >= 2) + 'Taoist Pagodas: ' + str(iTaoistCounter) + '/2')
			elif iGoal == 1:
				iGATurns = self.getChineseGoldenAgeTurns()
				iGoldenAges = iGATurns / utils.getTurns(8)
				aHelp.append(self.getIcon(iGATurns >= utils.getTurns(32)) + 'Golden ages: ' + str(iGoldenAges) + '/4')
			elif iGoal == 2:
				iNumUnits = pChina.getNumUnits()
				aHelp.append(self.getIcon(iNumUnits >= 120) + 'Number of units: ' + str(iNumUnits) + '/120')

		elif iPlayer == iBabylonia:
			if iGoal == 0:
				bWriting = (self.getBabylonianTechs(0) == 1)
				bCodeOfLaws = (self.getBabylonianTechs(1) == 1)
				bMonarchy = (self.getBabylonianTechs(2) == 1)
				aHelp.append(self.getIcon(bWriting) + 'Writing ' + self.getIcon(bCodeOfLaws) + 'Code of Laws ' + self.getIcon(bMonarchy) + 'Monarchy')
			elif iGoal == 1:
				pBestCity = self.calculateTopCityPopulation(76, 40)
				bBestCity = (pBestCity.getOwner() == iBabylonia and pBestCity.getX() == 76 and pBestCity.getY() == 40)
				aHelp.append(self.getIcon(bBestCity) + 'Most populous city: ' + pBestCity.getName())
			elif iGoal == 2:
				pBestCity = self.calculateTopCityCulture(76, 40)
				bBestCity = (pBestCity.getOwner() == iBabylonia and pBestCity.getX() == 76 and pBestCity.getY() == 40)
				aHelp.append(self.getIcon(bBestCity) + 'Most cultured city: ' + pBestCity.getName())

		elif iPlayer == iGreece:
			if iGoal == 0:
				bLiterature = (self.getGreekTechs(0) == 1)
				bDrama = (self.getGreekTechs(1) == 1)
				bPhilosophy = (self.getGreekTechs(2) == 1)
				aHelp.append(self.getIcon(bLiterature) + 'Literature ' + self.getIcon(bDrama) + 'Drama ' + self.getIcon(bPhilosophy) + 'Philosophy')
			elif iGoal == 1:
				bOracle = (self.getNumBuildings(iGreece, con.iOracle) > 0)
				bParthenon = (self.getNumBuildings(iGreece, con.iParthenon) > 0)
				bColossus = (self.getNumBuildings(iGreece, con.iColossus) > 0)
				bArtemis = (self.getNumBuildings(iGreece, con.iArtemis) > 0)
				aHelp.append(self.getIcon(bOracle) + 'Oracle ' + self.getIcon(bParthenon) + 'Parthenon ' + self.getIcon(bColossus) + 'Colossus ' + self.getIcon(bArtemis) + 'Temple of Artemis')
			elif iGoal == 2:
                        	bEgypt = self.checkOwnedCiv(iGreece, iEgypt)
                        	bPhoenicia = self.checkOwnedCiv(iGreece, iCarthage)
                        	bBabylonia = self.checkOwnedCiv(iGreece, iBabylonia)
				bPersia = self.checkOwnedCiv(iGreece, iPersia)
				aHelp.append(self.getIcon(bEgypt) + 'Egypt ' + self.getIcon(bPhoenicia) + 'Phoenicia ' + self.getIcon(bBabylonia) + 'Babylonia ' + self.getIcon(bPersia) + 'Persia')

		elif iPlayer == iPersia:
			if iGoal == 0:
				totalLand = gc.getMap().getLandPlots()
                        	persianLand = pPersia.getTotalLand()
                        	if (totalLand > 0):
                        		landPercent = (persianLand * 100.0) / totalLand
                        	else:
                        		landPercent = 0.0
				aHelp.append(self.getIcon(landPercent >= 7.995) + 'Percentage of world territory: ' + str(landPercent) + '/8 %')
			elif iGoal == 1:
                        	iCounter = 0
                        	for i in range(con.iSpaceElevator+1 - con.iPyramid):
                        		iWonder = i + con.iPyramid
					iCounter += self.getNumBuildings(iPersia, iWonder)
                        	for i in range(con.iMoaiStatues+1 - con.iArtemis):
                        		iWonder = i + con.iArtemis
					iCounter += self.getNumBuildings(iPersia, iWonder)
                        	for i in range(con.iWestminster+1 - con.iApostolicPalace):
                        		iWonder = i + con.iApostolicPalace
					iCounter += self.getNumBuildings(iPersia, iWonder)
				iCounter += self.getNumBuildings(iPersia, con.iFlavianAmphitheatre)
				aHelp.append(self.getIcon(iCounter >= 7) + 'Wonders: ' + str(iCounter) + '/7')
			elif iGoal == 2:
				iCounter = 0
				for iReligion in range(con.iNumReligions):
					iCurrentShrine = con.iShrine + iReligion*4
					iCounter += self.getNumBuildings(iPersia, iCurrentShrine)
				aHelp.append(self.getIcon(iCounter >= 2) + 'Shrines: ' + str(iCounter) + '/2')

		elif iPlayer == iCarthage:
			if iGoal == 0:
				iNumCities = self.getNumberOfCoastalAreaCities(iCarthage, tMediterraneanTL, tMediterraneanBR, tMediterraneanExceptions)
				aHelp.append(self.getIcon(iNumCities >= 5) + 'Cities at the Mediterranean Sea: ' + str(iNumCities) + '/5')
			elif iGoal == 1:
				iDye = pCarthage.getNumAvailableBonuses(con.iDye)
				aHelp.append(self.getIcon(iDye >= 4) + 'Available dye resources: ' + str(iDye) + '/4')
			elif iGoal == 2:
				lRevealedMap = con.l0Array
				for iCiv in range(iNumPlayers):
                                	for x in range(124):
                                		for y in range(68):
                                			if (gc.getMap().plot(x, y).isRevealed(iCiv, False)):
                                				lRevealedMap[iCiv] += 1
				iBestCiv = iCarthage
				for iCiv in range(iNumPlayers):
					if lRevealedMap[iCiv] > lRevealedMap[iBestCiv]:
						iBestCiv = iCiv
				aHelp.append(self.getIcon(iBestCiv == iCarthage) + 'Largest map: ' + CyTranslator().getText(str(gc.getPlayer(iBestCiv).getCivilizationShortDescriptionKey()),()))

		elif iPlayer == iRome:
			if not pRome.isReborn():
				if iGoal == 0:
					iBarracks = self.getNumBuildings(iRome, con.iBarracks)
					iAqueducts = self.getNumBuildings(iRome, con.iAqueduct)
					iAmphitheatres = self.getNumBuildings(iRome, con.iColosseum)
					aHelp.append(self.getIcon(iBarracks >= 5) + 'Barracks: ' + str(iBarracks) + '/5,' + self.getIcon(iAqueducts >= 5) + 'Aqueducts: ' + str(iAqueducts) + '/5,' + self.getIcon(iAmphitheatres >= 5) + 'Amphitheatres: ' + str(iAmphitheatres) + '/5')
				elif iGoal == 1:                              
                               		bSpain = self.checkOwnedArea(iRome, tCoreAreasTL[utils.getReborn(iSpain)][iSpain], tCoreAreasBR[utils.getReborn(iSpain)][iSpain], 2)
                                	bFrance = self.checkOwnedArea(iRome, tFranceTL, tNormalAreasBR[utils.getReborn(iFrance)][iFrance], 3)
                                	bEngland = self.checkOwnedArea(iRome, tCoreAreasTL[utils.getReborn(iEngland)][iEngland], tCoreAreasBR[utils.getReborn(iEngland)][iEngland], 1)
                                	bCarthage = self.checkOwnedArea(iRome, tCarthageTL, tCarthageBR, 2)
					bByzantium = self.checkOwnedArea(iRome, tCoreAreasTL[0][iByzantium], tCoreAreasBR[0][iByzantium], 4)
					bEgypt = self.checkOwnedArea(iRome, tCoreAreasTL[0][iEgypt], tCoreAreasBR[0][iEgypt], 2)
					aHelp.append(self.getIcon(bSpain) + '2 cities in Spain ' + self.getIcon(bFrance) + '3 cities in France ' + self.getIcon(bEngland) + '1 city in England')
					aHelp.append(self.getIcon(bCarthage) + '2 cities in Carthage ' + self.getIcon(bByzantium) + '4 cities in Greece and Anatolia ' + self.getIcon(bEgypt) + '2 cities in Egypt')
			else:
				if iGoal == 0:
					bBanking = (self.getItalianTechs(0) == 1)
					bEducation = (self.getItalianTechs(1) == 1)
					bRadio = (self.getItalianTechs(2) == 1)
					bFascism = (self.getItalianTechs(3) == 1)
					aHelp.append(self.getIcon(bBanking) + 'Banking ' + self.getIcon(bEducation) + 'Education ' + self.getIcon(bRadio) + 'Radio ' + self.getIcon(bFascism) + 'Fascism')
				elif iGoal == 1:
					iUniversities = self.getItalianUniversities()
					aHelp.append(self.getIcon(iUniversities >= 3) + 'Univiersities built: ' + str(iUniversities) + '/3')
				elif iGoal == 2:
					bGreece = self.checkOwnedCiv(iRome, iGreece)
					bEthiopia = self.checkOwnedCiv(iRome, iEthiopia)
					bLibya = self.checkOwnedArea(iRome, tLibyaTL, tLibyaBR, 1)
					for iCiv in range(con.iNumPlayers):
						if (iCiv != iRome):
							if self.checkOwnedArea(iCiv, tLibyaTL, tLibyaBR, 1):
								bLibya = False
					aHelp.append(self.getIcon(bGreece) + 'Greece ' + self.getIcon(bLibya) + 'Libya ' + self.getIcon(bEthiopia) + 'Ethiopia')
				

		elif iPlayer == iJapan:
			if iGoal == 0:
				iNumGenerals = self.getNumGenerals()
				aHelp.append(self.getIcon(iNumGenerals >= 3) + 'Generals born: '+str(iNumGenerals)+'/3')
			elif iGoal == 1:
				iFirstRankCiv = self.getHighestRankCiv()
				bFirstRank = (iFirstRankCiv == iJapan)
				aHelp.append(self.getIcon(bFirstRank) + 'Civilization with the highest score: ' + CyTranslator().getText(str(gc.getPlayer(iFirstRankCiv).getCivilizationShortDescriptionKey()),()))
		
                elif iPlayer == iEthiopia:
			if iGoal == 1 or iGoal == 2:
				bAfrica = True
                                for iEuroCiv in range(iNumPlayers):
                                	if (iEuroCiv in con.lCivGroups[0]):
                                 		if (self.checkNotOwnedArea(iEuroCiv, tSomaliaTL, tSomaliaBR) == False):
                                 			bAfrica = False
                                 		if (self.checkNotOwnedArea(iEuroCiv, tSubeqAfricaTL, tSubeqAfricaBR) == False):
                                 			bAfrica = False
                                 		if (bAfrica == False):
                                 			break
				aHelp.append(self.getIcon(bAfrica) + 'No European colonies in East and Subequatorial Africaa')

		elif iPlayer == iKorea:
			if iGoal == 0:
				bConfucianCathedral = (self.getNumBuildings(iKorea, con.iConfucianCathedral) > 0)
				bBuddhistCathedral = (self.getNumBuildings(iKorea, con.iBuddhistCathedral) > 0)
				aHelp.append(self.getIcon(bBuddhistCathedral) + 'Buddhist Stupa ' + self.getIcon(bConfucianCathedral) + 'Confucian Academy')
			#elif iGoal == 1:
			#	bPrintingPress = (self.getKoreanTechs(0) == 1)
			#	bGunpowder = (self.getKoreanTechs(1) == 1)
			#	aHelp.append(self.getIcon(bPrintingPress) + 'Printing Press ' + self.getIcon(bGunpowder) + 'Gunpowder')
			elif iGoal == 2:
				iNumSinks = self.getNumKoreanSinks()
				aHelp.append(self.getIcon(iNumSinks >= 20) + 'Enemy ships sunk: ' + str(iNumSinks) + '/20')

		# Maya goals have no stages

		elif iPlayer == iByzantium:
			if iGoal == 0:
				iGold = pByzantium.getGold()
				aHelp.append(self.getIcon(iGold >= 5000) + 'Gold in treasury: ' + str(iGold) + '/5000')
			elif iGoal == 1:           	
				pBestPopCity = self.calculateTopCityPopulation(68, 45)
				bBestPopCity = (pBestPopCity.getOwner() == iByzantium and pBestPopCity.getX() == 68 and pBestPopCity.getY() == 45)
				pBestCultureCity = self.calculateTopCityCulture(68, 45)
				bBestCultureCity = (pBestCultureCity.getOwner() == iByzantium and pBestCultureCity.getX() == 68 and pBestCultureCity.getY() == 45)
				aHelp.append(self.getIcon(bBestPopCity) + 'Most populous city: ' + pBestPopCity.getName() + ' ' + self.getIcon(bBestCultureCity) + 'Most cultured city: ' + pBestCultureCity.getName())
			elif iGoal == 2:
				bBalkans = self.checkOwnedArea(iByzantium, tBalkansTL, tBalkansBR, 3)
				bNorthAfrica = self.checkOwnedArea(iByzantium, tNorthAfricaTL, tNorthAfricaBR, 3)
				bNearEast = self.checkOwnedArea(iByzantium, tNearEastTL, tNearEastBR, 3)
				aHelp.append(self.getIcon(bBalkans) + 'Balkans ' + self.getIcon(bNorthAfrica) + 'North Africa ' + self.getIcon(bNearEast) + 'Near East')

		elif iPlayer == iVikings:
			if iGoal == 0:
				iGold = pVikings.getGold()
				aHelp.append(self.getIcon(iGold >= 5000) + 'Gold in treasury: ' + str(iGold) + '/5000')
			elif iGoal == 1:
				iNumSinks = self.getNumSinks()
				aHelp.append(self.getIcon(iNumSinks >= 25) + 'Enemy ships sunk: ' + str(iNumSinks) + '/25')

		elif iPlayer == iArabia:
			if iGoal == 0:
				iCounter = 0
				for iReligion in range(con.iNumReligions):
					iCurrentShrine = con.iShrine + iReligion*4
					iCounter += self.getNumBuildings(iArabia, iCurrentShrine)
				aHelp.append(self.getIcon(iCounter >= 3) + 'Shrines: ' + str(iCounter) + '/3')
			elif iGoal == 1:
                                bSpain = self.isControlledOrVassalized(iArabia, con.tCoreAreasTL[0][iSpain], con.tCoreAreasBR[0][iSpain])
                                bMaghreb = self.isControlledOrVassalized(iArabia, tCarthageTL, tCarthageBR)
				bMesopotamia = self.isControlledOrVassalized(iArabia, con.tCoreAreasTL[0][iBabylonia], con.tCoreAreasBR[0][iBabylonia])
				bPersia = self.isControlledOrVassalized(iArabia, con.tCoreAreasTL[0][iPersia], con.tCoreAreasBR[0][iPersia])
				aHelp.append(self.getIcon(bSpain) + 'Spain ' + self.getIcon(bMaghreb) + 'Maghreb ' + self.getIcon(bMesopotamia) + 'Mesopotamia ' + self.getIcon(bPersia) + 'Persia')
			elif iGoal == 2:
                                fReligionPercent = gc.getGame().calculateReligionPercent(con.iIslam)
				aHelp.append(self.getIcon(fReligionPercent >= 40.0) + 'Islam spread to: ' + str(fReligionPercent) + '/40 %')

		elif iPlayer == iKhmer:
			if iGoal == 0:
				iCulture = pKhmer.countTotalCulture()
				aHelp.append(self.getIcon(iCulture >= utils.getTurns(12000)) + 'Total culture: ' +str(iCulture) + '/' + str(utils.getTurns(12000)))
			elif iGoal == 1:
				apCityList = PyPlayer(iKhmer).getCityList()
                                iTotalPopulation = 0
                                for pCity in apCityList:			
                                	iTotalPopulation += pCity.getPopulation()
				if len(apCityList) > 0:
                                	fPopPerCity = iTotalPopulation / len(apCityList)
				else:
					fPopPerCity = 0
				aHelp.append(self.getIcon(fPopPerCity >= 10.0) + 'Average population per city: ' + str(fPopPerCity) + '/10')
			elif iGoal == 2:
                                fReligionPercent = gc.getGame().calculateReligionPercent(con.iBuddhism)
				aHelp.append(self.getIcon(fReligionPercent >= 30.0) + 'Buddhism spread to: ' + str(fReligionPercent) + '/30 %')

		elif iPlayer == iIndonesia:
			if iGoal == 0:
				iHighestCiv = self.getHighestPopulationCiv(iIndonesia)
				bHighest = (iHighestCiv == iIndonesia)
				aHelp.append(self.getIcon(bHighest) + 'Civilization with the largest population: ' + CyTranslator().getText(str(gc.getPlayer(iHighestCiv).getCivilizationShortDescriptionKey()),()))
			elif iGoal == 1:
				lHappinessBonuses = [con.iDye, con.iFur, con.iGems, con.iGold, con.iIncense, con.iIvory, con.iSilk, con.iSilver, con.iSpices, con.iSugar, con.iWine, con.iWhales, con.iCotton]
                                iCounter = 0
				for iBonus in lHappinessBonuses:
					if pIndonesia.getNumAvailableBonuses(iBonus) > 0:
						iCounter += 1
				aHelp.append(self.getIcon(iCounter >= 9) + 'Owned happiness resources: ' + str(iCounter) + '/9')
			elif iGoal == 2:
				totalPop = gc.getGame().getTotalPopulation()
				ourPop = teamIndonesia.getTotalPopulation()
				if (totalPop > 0):
					popPercent = (ourPop * 100.0) / totalPop
				else:
					popPercent = 0.0
				aHelp.append(self.getIcon(popPercent >= 10.0) + 'Percentage of world population: ' + (u"%.2f%%" % popPercent) + '/10%')

		elif iPlayer == iSpain:
			if iGoal == 1:
				iLargestEmpireCiv = self.getLargestEmpireCiv(iSpain)
				aHelp.append(self.getIcon(iLargestEmpireCiv == iSpain) + 'Largest empire: ' + CyTranslator().getText(str(gc.getPlayer(iLargestEmpireCiv).getCivilizationShortDescriptionKey()),()))
			elif iGoal == 2:
				bAztecs = self.checkOwnedCiv(iSpain, iAztecs)
				bInca = self.checkOwnedCiv(iSpain, iInca)
				aHelp.append(self.getIcon(bAztecs) + 'Aztecs ' + self.getIcon(bInca) + 'Inca')

		elif iPlayer == iFrance:
			if iGoal == 0:
				pBestCity = self.calculateTopCityCulture(55, 50)
				bBestCity = (pBestCity.getOwner() == iFrance and pBestCity.getX() == 55 and pBestCity.getY() == 50)
				aHelp.append(self.getIcon(bBestCity) + 'Most cultured city: ' + pBestCity.getName())
			elif iGoal == 1:
				bNECanada = self.checkFoundedArea(iFrance, tNECanadaTL, tNECanadaBR, 3)
                                bLouisiana = self.checkFoundedArea(iFrance, tLouisianaTL, tLouisianaBR, 1)
				aHelp.append(self.getIcon(bNECanada) + '3 cities in Quebec and Hudson Bay ' + self.getIcon(bLouisiana) + '1 city in Louisiana')
			elif iGoal == 2:
				bNotreDame = (self.getNumBuildings(iFrance, con.iNotreDame) > 0)
				bStatueOfLiberty = (self.getNumBuildings(iFrance, con.iStatueOfLiberty) > 0)
				bEiffelTower = (self.getNumBuildings(iFrance, con.iEiffelTower) > 0)
				aHelp.append(self.getIcon(bNotreDame) + 'Notre Dame ' + self.getIcon(bStatueOfLiberty) + 'Statue of Liberty ' + self.getIcon(bEiffelTower) + 'Eiffel Tower')

		elif iPlayer == iEngland:
			if iGoal == 0:
				iCShipOfTheLine = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_SHIP_OF_THE_LINE')
				iCFrigate = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_FRIGATE')
				iEnglishNavy = gc.getPlayer(iEngland).getUnitClassCount(iCFrigate) + gc.getPlayer(iEngland).getUnitClassCount(iCShipOfTheLine)
				aHelp.append(self.getIcon(iEnglishNavy >= 25) + 'Total of frigates and ships of the line: ' + str(iEnglishNavy) + '/25')
			elif iGoal == 1:
                                bNCAmerica = self.checkFoundedArea(iEngland, tNCAmericaTL, tNCAmericaBR, 3)
                                bSAmerica = self.checkFoundedArea(iEngland, tSAmericaTL, tSAmericaBR, 3)
                                bAfrica = self.checkFoundedArea(iEngland, tAfricaTL, tAfricaBR, 3)
                                bAsia = self.checkFoundedArea(iEngland, tAsiaTL, tAsiaBR, 3)
                                bOceania = self.checkFoundedArea(iEngland, tOceaniaTL, tOceaniaBR, 3)
				aHelp.append(self.getIcon(bNCAmerica) + 'North America ' + self.getIcon(bSAmerica) + 'South America')
				aHelp.append(self.getIcon(bAfrica) + 'Africa ' + self.getIcon(bAsia) + 'Asia ' + self.getIcon(bOceania) + 'Oceania')
			elif iGoal == 2:
				bIndustrial = (self.getEnglishEras(0) == 1)
				bModern = (self.getEnglishEras(1) == 1)
				aHelp.append(self.getIcon(bIndustrial) + 'First to enter the Industrial Era ' + self.getIcon(bModern) + 'First to enter the Modern Era')

		elif iPlayer == iGermany:
			if iGoal == 0:
                               	bFrance = self.checkOwnedCiv(iGermany, iFrance)
                                bRome = self.checkOwnedCiv(iGermany, iRome)
                                bGreece = self.checkOwnedCiv(iGermany, iGreece)
				aHelp.append(self.getIcon(bRome) + 'Rome ' + self.getIcon(bGreece) + 'Greece ' + self.getIcon(bFrance) + 'France')
			elif iGoal == 1:
                                bRussia = self.checkOwnedCiv(iGermany, iRussia)
                                bEngland = self.checkOwnedCiv(iGermany, iEngland)                                        
                                bScandinavia = self.checkOwnedCiv(iGermany, iVikings)
				aHelp.append(self.getIcon(bScandinavia) + 'Scandinavia ' + self.getIcon(bEngland) + 'England ' + self.getIcon(bRussia) + 'Russia')

		elif iPlayer == iRussia:
			if iGoal == 0:
				bSiberia = self.checkFoundedArea(iRussia, tSiberiaTL, tSiberiaBR, 7)
				aHelp.append(self.getIcon(bSiberia) + 'Siberia')

		elif iPlayer == iNetherlands:
			if iGoal == 0:
				iGMerchant = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), "SPECIALIST_GREAT_MERCHANT")
				pPlot = gc.getMap().plot(57, 53)
				if pPlot.isCity():
					iMerchants = pPlot.getPlotCity().getFreeSpecialistCount(iGMerchant)
				else:
					iMerchants = 0
				aHelp.append(self.getIcon(iMerchants >= 3) + 'Great merchants settled in Amsterdam: ' + str(iMerchants) + '/3')
			elif iGoal == 2:
				iSpices = pNetherlands.getNumAvailableBonuses(con.iSpices)
				aHelp.append(self.getIcon(iSpices >= 7) + 'Available spice resources: ' + str(iSpices) + '/7')

		elif iPlayer == iMali:
			if iGoal == 0:
				iMostGoldCiv = self.getMostGoldCiv(iMali)
				aHelp.append(self.getIcon(iMostGoldCiv == iMali) + 'Richest civilization: ' + CyTranslator().getText(str(gc.getPlayer(iMostGoldCiv).getCivilizationShortDescriptionKey()),()))
			elif iGoal == 1:
				iGold = pMali.getGold()
				aHelp.append(self.getIcon(iGold >= 4000) + 'Gold in treasury: ' + str(iGold) + '/4000')
			elif iGoal == 2:
				iGold = pMali.getGold()
				aHelp.append(self.getIcon(iGold >= 16000) + 'Gold in treasury: ' + str(iGold) + '/16000')

		elif iPlayer == iPortugal:
			if iGoal == 0:
				lRevealedMap = con.l0Array
				for iCiv in range(iNumPlayers):
                                	for x in range(124):
                                		for y in range(68):
                                			if (gc.getMap().plot(x, y).isRevealed(iCiv, False)):
                                				lRevealedMap[iCiv] += 1
				iBestCiv = iPortugal
				for iCiv in range(iNumPlayers):
					if lRevealedMap[iCiv] > lRevealedMap[iBestCiv]:
						iBestCiv = iCiv
				aHelp.append(self.getIcon(iBestCiv == iPortugal) + 'Largest map: ' + CyTranslator().getText(str(gc.getPlayer(iBestCiv).getCivilizationShortDescriptionKey()),()))
			elif iGoal == 1:
				iCount = 0
                                for iLoopCiv in range(iNumMajorPlayers):
                                	if (iLoopCiv != iPortugal):
                                		if (teamPortugal.isOpenBorders(iLoopCiv)):
                                			iCount += 1
				aHelp.append(self.getIcon(iCount >= 12) + 'Open border agreements: ' + str(iCount) + '/12')
			elif iGoal == 2:
				iColonies = self.getPortugueseColonies()
				aHelp.append(self.getIcon(iColonies >= 15) + 'Extra-European colonies founded: ' + str(iColonies) + '/15')

		elif iPlayer == iInca:
			if iGoal == 0 or iGoal == 2:
				bSAmerica = True
                                for iEuroCiv in range(iNumPlayers):
                                	if (iEuroCiv in con.lCivGroups[0]):
                                		if (self.checkNotOwnedArea_Skip(iEuroCiv, tSAmericaTL, tSAmericaBR, tBrazilTL, tBrazilBR) == False):
                                			bSAmerica = False
                                			break
				aHelp.append(self.getIcon(bSAmerica) + 'No European settlements in South America (except Brazil)')
			elif iGoal == 1:
				iGold = pInca.getGold()
				aHelp.append(self.getIcon(iGold >= 3000) + 'Gold in treasury: ' + str(iGold) + '/3000')

		elif iPlayer == iMongolia:
			if iGoal == 1:
				iRazedCities = self.getRazedByMongols()	
				aHelp.append(self.getIcon(iRazedCities >= 7) + 'Cities razed: ' + str(iRazedCities) + '/7')
			elif iGoal == 2:
				totalLand = gc.getMap().getLandPlots()
                        	mongolianLand = pMongolia.getTotalLand()
                        	if (totalLand > 0):
                        		landPercent = (mongolianLand * 100.0) / totalLand
                        	else:
                        		landPercent = 0.0
				aHelp.append(self.getIcon(landPercent >= 11.995) + 'Percentage of world territory: ' + str(landPercent) + '/12 %')

		elif iPlayer == iAztecs:
			if iGoal == 0:
				iEnslavedUnits = self.getEnslavedUnits()
				aHelp.append(self.getIcon(iEnslavedUnits >= 5) + 'Enslaved units: ' + str(iEnslavedUnits) + '/5')
			elif iGoal == 1:
                                bCAmerica = True
                                for iEuroCiv in range(iNumPlayers):
                                	if (iEuroCiv in con.lCivGroups[0]):
                                		if (self.checkNotOwnedArea(iEuroCiv, tCAmericaTL, tCAmericaBR) == False):
                                			bCAmerica = False
                                			break
				aHelp.append(self.getIcon(bCAmerica) + 'No European colonies in Central America, Southern USA and the Caribbean')

		elif iPlayer == iTurkey:
			if iGoal == 1:
				bBalkans = self.checkOwnedArea(iTurkey, tBalkansTL, tBalkansBR, 3)
                                bBlackSea = self.checkOwnedAreaAdjacentArea(iTurkey, tBlackSeaTL, tBlackSeaBR, 4, (71,47))
                                bMesopotamia = self.checkOwnedArea(iTurkey, tMesopotamiaTL, tMesopotamiaBR, 3)
				aHelp.append(self.getIcon(bBalkans) + 'Balkans ' + self.getIcon(bBlackSea) + 'Black Sea ' + self.getIcon(bMesopotamia) + 'Mesopotamia')
			elif iGoal == 2:
                                iCounter = 0
                                for iCiv in range(iNumPlayers):
                                	if (iCiv != iTurkey):
                                		if (gc.getPlayer(iCiv).isAlive()):
                                			if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iTurkey)):
                                				iCounter += 1
				aHelp.append(self.getIcon(iCounter >= 3) + 'Vassals: ' + str(iCounter) + '/3')

		elif iPlayer == iAmerica:
			if iGoal == 0:
                        	bAmericas = True
                        	for iEuroCiv in range(iNumPlayers):
                        		if (iEuroCiv in con.lCivGroups[0]):
                        			if (self.checkNotOwnedArea(iEuroCiv, tNCAmericaTL, tNCAmericaBR) == False):
                        				bAmericas = False
                        				break
				aHelp.append(self.getIcon(bAmericas) + 'No European colonies in North and Central American and the Carribean')
			elif iGoal == 1:	# not entirely correct, you actually have to build them, this counts conquered ones as well
				bUnitedNations = (self.getNumBuildings(iAmerica, con.iUnitedNations) > 0)
				bStatueOfLiberty = (self.getNumBuildings(iAmerica, con.iStatueOfLiberty) > 0)
				bPentagon = (self.getNumBuildings(iAmerica, con.iPentagon) > 0)
				aHelp.append(self.getIcon(bUnitedNations) + 'United Nations ' + self.getIcon(bStatueOfLiberty) + 'Statue of Liberty ' + self.getIcon(bPentagon) + 'Pentagon')
			elif iGoal == 2:
				iCounter = pAmerica.getNumAvailableBonuses(con.iOil) - pAmerica.getBonusImport(con.iOil)
                                for iCiv in range(iNumPlayers):
                                	if (iCiv != iAmerica):
                                		if (gc.getPlayer(iCiv).isAlive()):
                                			if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iAmerica)):
                                				iCounter += gc.getPlayer(iCiv).getNumAvailableBonuses(con.iOil) - gc.getPlayer(iCiv).getBonusImport(con.iOil)
				aHelp.append(self.getIcon(iCounter >= 10) + 'Oil resources secured: ' + str(iCounter) + '/10')
		
		return aHelp




