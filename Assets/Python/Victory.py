# Rhye's and Fall of Civilization - Historical Victory Goals


from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
#import cPickle as pickle
from StoredData import sd # edead
import Consts as con
import Victory as vic
import RFCUtils
import time # Leoreth: benchmarking
import heapq # Leoreth
utils = RFCUtils.RFCUtils()

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
localText = CyTranslator()


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

iGreatProphet = 7

tCoreAreasTL = con.tCoreAreasTL
tCoreAreasBR = con.tCoreAreasBR
tNormalAreasTL = con.tNormalAreasTL
tNormalAreasBR = con.tNormalAreasBR
tAmericasTL = con.tAmericasTL
tAmericasBR = con.tAmericasBR
tSAmericaTL = (24, 3)
tSAmericaBR = (43, 32)
tSouthAmericaExceptions = ((24, 31), (25, 32))
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

tManchuriaTL = (104, 50)
tManchuriaBR = (112, 55)
tKoreaTL = (108, 45)
tKoreaBR = (110, 49)
tChinaTL = (99, 39)
tChinaBR = (107, 49)
tIndochinaTL = (97, 31)
tIndochinaBR = (103, 38)
tIndonesiaTL = (98, 24)
tIndonesiaBR = (109, 30)
tPhilippinesTL = (108, 30)
tPhilippinesBR = (110, 36)

tSouthAsiaTL = (88, 24)
tSouthAsiaBR = (110, 38)

tVienna = (63, 49)
tCairo = (69, 34)
tMecca = (75, 33)
tBaghdad = (77, 40)

lEasternMediterranean = [(58, 39), (58, 38), (58, 37), (59, 37), (60, 37), (61, 37), (61, 36), (62, 36), (63, 36), (64, 36), (65, 36), (66, 36), (67, 36), (68, 36), (69, 36), (70, 36), (71, 36), (65, 37), (66, 37), (72, 37), (73, 37), (73, 38), (73, 39), (73, 40), (73, 41), (73, 42), (70, 42), (71, 42), (72, 42), (69, 43), (70, 43), (69, 44), (68, 45), (67, 44), (67, 45), (66, 44), (65, 43), (66, 43), (65, 42), (66, 42), (67, 42), (67, 41), (65, 40), (66, 40)]
lBlackSea = [(69, 44), (70, 44), (71, 44), (71, 45), (72, 45), (73, 45), (73, 44), (74, 44), (75, 44), (76, 44), (76, 45), (76, 46), (76, 47), (75, 47), (74, 48), (75, 48), (72, 48), (74, 49), (73, 49), (71, 49), (69, 49), (69, 50), (70, 50), (71, 50), (72, 50), (73, 50), (68, 49), (68, 48), (67, 45), (67, 46), (67, 47), (67, 48), (68, 45)]

tSafavidMesopotamiaTL = (75, 39)
tSafavidMesopotamiaBR = (79, 43)
tTransoxaniaTL = (82, 42)
tTransoxaniaBR = (86, 49)
tNWIndiaTL = (86, 37)
tNWIndiaBR = (91, 43)

lSiberianCoast = [(109, 50), (109, 51), (110, 51), (111, 51), (112, 52), (114, 54), (113, 55), (111, 54), (111, 55), (110, 55), (110, 58), (111, 58), (112, 59)]

iMediterraneanTiles = 263

tDeccanTL = (88, 28)
tDeccanBR = (94, 36)
tSrivijayaTL = (98, 25)
tSrivijayaBR = (105, 29)

tIberiaTL = (49, 40)
tIberiaBR = (55, 46)
tMaghrebTL = (49, 35)
tMaghrebBR = (58, 39)
tWestAfricaTL = (48, 26)
tWestAfricaBR = (56, 32)

lAndeanCoast = [(25, 29), (24, 28), (24, 27), (24, 26), (24, 25), (25, 24), (25, 23), (26, 22), (27, 21), (28, 20), (29, 19), (30, 18), (30, 17), (30, 16), (30, 15), (30, 14)]

tCentralAmericaTL = (12, 31)
tCentralAmericaBR = (25, 42)
tCentralAmericaExceptions = ((25, 38), (25, 41))

tWesternNorthAmericaTL = (11, 43)
tWesternNorthAmericaBR = (21, 50)

tPeruTL = (25, 16)
tPeruBR = (32, 24)
tGranColombiaTL = (21, 25)
tGranColombiaBR = (32, 35)
tGuayanasTL = (33, 27)
tGuayanasBR = (37, 31)
tCaribbeanTL = (25, 33)
tCaribbeanBR = (33, 39)

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
iTamils = con.iTamils
iEthiopia = con.iEthiopia
iKorea = con.iKorea
iMaya = con.iMaya
iByzantium = con.iByzantium
iVikings = con.iVikings
iArabia = con.iArabia
iTibet = con.iTibet
iKhmer = con.iKhmer
iIndonesia = con.iIndonesia
iMoors = con.iMoors
iSpain = con.iSpain
iFrance = con.iFrance
iEngland = con.iEngland
iHolyRome = con.iHolyRome
iRussia = con.iRussia
iNetherlands = con.iNetherlands
iHolland = con.iHolland
iMali = con.iMali
iPoland = con.iPoland
iTurkey = con.iTurkey
iPortugal = con.iPortugal
iInca = con.iInca
iItaly = con.iItaly
iMongolia = con.iMongolia
iAztecs = con.iAztecs
iMughals = con.iMughals
iThailand = con.iThailand
iCongo = con.iCongo
iGermany = con.iGermany
iAmerica = con.iAmerica
iArgentina = con.iArgentina
iBrazil = con.iBrazil
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
pTamils = gc.getPlayer(iTamils)
pEthiopia = gc.getPlayer(iEthiopia)
pKorea = gc.getPlayer(iKorea)
pMaya = gc.getPlayer(iMaya)
pByzantium = gc.getPlayer(iByzantium)
pVikings = gc.getPlayer(iVikings)
pArabia = gc.getPlayer(iArabia)
pTibet = gc.getPlayer(iTibet)
pKhmer = gc.getPlayer(iKhmer)
pIndonesia = gc.getPlayer(iIndonesia)
pMoors = gc.getPlayer(iMoors)
pSpain = gc.getPlayer(iSpain)
pFrance = gc.getPlayer(iFrance)
pEngland = gc.getPlayer(iEngland)
pHolyRome = gc.getPlayer(iHolyRome)
pRussia = gc.getPlayer(iRussia)
pNetherlands = gc.getPlayer(iNetherlands)
pHolland = gc.getPlayer(iHolland)
pMali = gc.getPlayer(iMali)
pPoland = gc.getPlayer(iPoland)
pTurkey = gc.getPlayer(iTurkey)
pPortugal = gc.getPlayer(iPortugal)
pInca = gc.getPlayer(iInca)
pItaly = gc.getPlayer(iItaly)
pMongolia = gc.getPlayer(iMongolia)
pAztecs = gc.getPlayer(iAztecs)
pMughals = gc.getPlayer(iMughals)
pThailand = gc.getPlayer(iThailand)
pCongo = gc.getPlayer(iCongo)
pGermany = gc.getPlayer(iGermany)
pAmerica = gc.getPlayer(iAmerica)
pArgentina = gc.getPlayer(iArgentina)
pBrazil = gc.getPlayer(iBrazil)
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
teamTamils = gc.getTeam(pTamils.getTeam())
teamEthiopia = gc.getTeam(pEthiopia.getTeam())
teamKorea = gc.getTeam(pKorea.getTeam())
teamMaya = gc.getTeam(pMaya.getTeam())
teamByzantium = gc.getTeam(pByzantium.getTeam())
teamVikings = gc.getTeam(pVikings.getTeam())
teamArabia = gc.getTeam(pArabia.getTeam())
teamTibet = gc.getTeam(pTibet.getTeam())
teamKhmer = gc.getTeam(pKhmer.getTeam())
teamIndonesia = gc.getTeam(pIndonesia.getTeam())
teamMoors = gc.getTeam(pMoors.getTeam())
teamSpain = gc.getTeam(pSpain.getTeam())
teamFrance = gc.getTeam(pFrance.getTeam())
teamEngland = gc.getTeam(pEngland.getTeam())
teamHolyRome = gc.getTeam(pHolyRome.getTeam())
teamRussia = gc.getTeam(pRussia.getTeam())
teamNetherlands = gc.getTeam(pNetherlands.getTeam())
teamHolland = gc.getTeam(pHolland.getTeam())
teamMali = gc.getTeam(pMali.getTeam())
teamPoland = gc.getTeam(pPoland.getTeam())
teamTurkey = gc.getTeam(pTurkey.getTeam())
teamPortugal = gc.getTeam(pPortugal.getTeam())
teamInca = gc.getTeam(pInca.getTeam())
teamItaly = gc.getTeam(pItaly.getTeam())
teamMongolia = gc.getTeam(pMongolia.getTeam())
teamAztecs = gc.getTeam(pAztecs.getTeam())
teamMughals = gc.getTeam(pMughals.getTeam())
teamThailand = gc.getTeam(pThailand.getTeam())
teamCongo = gc.getTeam(pCongo.getTeam())
teamGermany = gc.getTeam(pGermany.getTeam())
teamAmerica = gc.getTeam(pAmerica.getTeam())
teamArgentina = gc.getTeam(pArgentina.getTeam())
teamBrazil = gc.getTeam(pBrazil.getTeam())
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
		if iNewValue == 1 and self.getGoal(i, j) == 0: return
	
                sd.scriptDict['lGoals'][i][j] = iNewValue
		
		if iNewValue == 0 and utils.getHumanID() == i:
			utils.debugTextPopup(localText.getText("TXT_KEY_VICTORY_GOAL_FAILED_ANNOUNCE", (j+1,)))

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

	def increaseTechsStolen(self):
		sd.scriptDict['iTechsStolen'] += 1

	def getTechsStolen(self):
		return sd.scriptDict['iTechsStolen']

	def getChineseTechs(self, i):
		return sd.scriptDict['lChineseTechs'][i]

	def setChineseTechs(self, i, iNewValue):
		sd.scriptDict['lChineseTechs'][i] = iNewValue

	def getEthiopianControl(self):
		return sd.scriptDict['iEthiopianControl']

	def setEthiopianControl(self, iNewValue):
		sd.scriptDict['iEthiopianControl'] = iNewValue
		
	def getVikingGold(self):
		return sd.scriptDict['iVikingGold']
		
	def changeVikingGold(self, iChange):
		sd.scriptDict['iVikingGold'] += iChange
		
	def getRussianProjects(self, i):
		return sd.scriptDict['lRussianProjects'][i]
		
	def setRussianProjects(self, i, iNewValue):
		sd.scriptDict['lRussianProjects'][i] = iNewValue
		
	def getDutchColonies(self):
		return sd.scriptDict['iDutchColonies']
		
	def changeDutchColonies(self, iChange):
		sd.scriptDict['iDutchColonies'] += iChange
		
	def getNumTamilSinks(self):
		return sd.scriptDict['iNumTamilSinks']
		
	def setNumTamilSinks(self, iNewValue):
		sd.scriptDict['iNumTamilSinks'] = iNewValue
		
	def getTamilTradeGold(self):
		return sd.scriptDict['iTamilTradeGold']
		
	def changeTamilTradeGold(self, iChange):
		sd.scriptDict['iTamilTradeGold'] += iChange
		
	def getRomanTechs(self, i):
		return sd.scriptDict['lRomanTechs'][i]
		
	def setRomanTechs(self, i, iNewValue):
		sd.scriptDict['lRomanTechs'][i] = iNewValue
		
	def getCongoSlaveCounter(self):
		return sd.scriptDict['iCongoSlaveCounter']
		
	def changeCongoSlaveCounter(self, iChange):
		sd.scriptDict['iCongoSlaveCounter'] += iChange
		
	def getMaliGold(self):
		return sd.scriptDict['bMaliGold']
		
	def setMaliGold(self, bValue):
		sd.scriptDict['bMaliGold'] = bValue
		
	def setIgnoreAI(self, bValue):
		sd.scriptDict['bIgnoreAI'] = bValue
		
	def isIgnoreAI(self):
		return sd.scriptDict['bIgnoreAI']
		
	def getColombianTradeGold(self):
		return sd.scriptDict['iColombianTradeGold']
		
	def changeColombianTradeGold(self, iChange):
		sd.scriptDict['iColombianTradeGold'] += iChange
                
#######################################
### Main methods (Event-Triggered) ###
#####################################  


        def checkOwnedCiv(self, iActiveCiv, iOwnedCiv):
		reborn = utils.getReborn(iOwnedCiv)
                dummy1, plotList1 = utils.squareSearch( tNormalAreasTL[reborn][iOwnedCiv], tNormalAreasBR[reborn][iOwnedCiv], utils.ownedCityPlots, iActiveCiv )
                dummy2, plotList2 = utils.squareSearch( tNormalAreasTL[reborn][iOwnedCiv], tNormalAreasBR[reborn][iOwnedCiv], utils.ownedCityPlots, iOwnedCiv )
                if ((len(plotList1) >= 2 and len(plotList1) > len(plotList2)) or (len(plotList1) >= 1 and not gc.getPlayer(iOwnedCiv).isAlive()) or (len(plotList1) >= 1 and iOwnedCiv == con.iCarthage)):
                        return True
                else:
                        return False


        def checkOwnedArea(self, iActiveCiv, tTopLeft, tBottomRight, iThreshold):
                dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.ownedCityPlots, iActiveCiv )
                if (len(plotList) >= iThreshold):
                        return True
                else:
                        return False
			
	def getNumCitiesInArea(self, iPlayer, tTopLeft, tBottomRight):
		dummy, plotList = utils.squareSearch(tTopLeft, tBottomRight, utils.ownedCityPlots, iPlayer)
		return len(plotList)


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
			
	def setup(self):
	
		# 1700AD scenario: handle dates that have already been passed
		if utils.getScenario() == con.i1700AD:
			for i in range(3):
				utils.setGoal(iChina, i, 0)
				utils.setGoal(iKorea, i, 0)
				utils.setGoal(iVikings, i, 0)
				utils.setGoal(iSpain, i, 0)
				utils.setGoal(iHolyRome, i, 0)
				utils.setGoal(iPoland, i, 0)
				utils.setGoal(iPortugal, i, 0)
				utils.setGoal(iMughals, i, 0)
				utils.setGoal(iTurkey, i, 0)
				utils.setGoal(iThailand, i, 0)
				
			
			utils.setGoal(iPersia, 0, 1)
			utils.setGoal(iJapan, 0, 1)
			utils.setGoal(iFrance, 0, 1)
			# England
			utils.setGoal(iRussia, 0, 1)
			utils.setGoal(iCongo, 0, 1)
			# Netherlands
			
			# help Congo
			self.changeCongoSlaveCounter(500)
			
			# help Netherlands
			self.changeDutchColonies(2)
			
		# ignore AI goals
		bIgnoreAI = (gc.getDefineINT("NO_AI_UHV_CHECKS") == 1)
		self.setIgnoreAI(bIgnoreAI)
	
		if bIgnoreAI:
			for iPlayer in range(con.iNumPlayers):
				if utils.getHumanID() != iPlayer:
					for iGoal in range(3):
						self.setGoal(iPlayer, iGoal, 0)
						

        def checkTurn(self, iGameTurn):

                pass

	def checkPlayerTurn(self, iGameTurn, iPlayer):


                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return
			
		if iPlayer >= con.iNumPlayers:
			return
			
		if iGameTurn == utils.getScenarioStartTurn():
			return
			
		# Leoreth: don't check AI civilizations to improve speed
		if utils.getHumanID() != iPlayer and self.isIgnoreAI():
			#utils.debugTextPopup("Ignored goal check for civ "+str(iPlayer))
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
                                                
                                if (iGameTurn == getTurnForYear(-100)):
                                        if (self.getGoal(iEgypt, 1) == -1):                                  
                                                self.setGoal(iEgypt, 1, 0)                      

                                                
                elif (iPlayer == iIndia):
                        if (pIndia.isAlive()):

				if iGameTurn == getTurnForYear(-100):
					bBuddhistShrine = (self.getNumBuildings(iIndia, con.iBuddhistShrine) > 0)	
					bHinduShrine = (self.getNumBuildings(iIndia, con.iHinduShrine) > 0)
					if bHinduShrine and bBuddhistShrine:
						self.setGoal(iIndia, 0, 1)
					else:
						self.setGoal(iIndia, 0, 0)     
                                                                
                                #if (iGameTurn == getTurnForYear(1200)):
                                #        iPop = pIndia.getRealPopulation()
                                #        #iPop = pIndia.getTotalPopulation()
                                #        #print ("india pop", pIndia.getTotalPopulation(), pIndia.getRealPopulation())
                                #        bFirst = True
                                #        for iCiv in range(iNumPlayers):
                                #                #print ("other pop", iCiv, gc.getPlayer(iCiv).getTotalPopulation(), gc.getPlayer(iCiv).getRealPopulation())
                                #                if (iPop < gc.getPlayer(iCiv).getRealPopulation()):
                                #                        bFirst = False
                                #                        break
                                #        if (bFirst):                                                
                                #                self.setGoal(iIndia, 2, 1)
                                #        else:
                                #                self.setGoal(iIndia, 2, 0)
				
				
				if iGameTurn == getTurnForYear(1200):
					totalPop = gc.getGame().getTotalPopulation()
					ourPop = teamIndia.getTotalPopulation()
					if (totalPop > 0):
						popPercent = (ourPop * 100.0) / totalPop
					else:
						popPercent = 0.0

					if popPercent >= 20.0:
						self.setGoal(iIndia, 2, 1)
					else:
						self.setGoal(iIndia, 2, 0)

				if iGameTurn == getTurnForYear(700):
					if self.getGoal(iIndia, 1) == -1:
						self.setGoal(iIndia, 1, 0)

                            
                        
                elif (iPlayer == iChina):
                        if (pChina.isAlive()):

                                # build two Confucian and Taoist Cathedrals by 1000 AD
				if iGameTurn == getTurnForYear(1000):
					if self.getGoal(iChina, 0) == -1:
						self.setGoal(iChina, 0, 0)

				# Leoreth - new condition: have 4 golden ages until 1850 AD
                                if (iGameTurn == getTurnForYear(1800)):      
                                        if (self.getGoal(iChina, 1) == -1):
                                                self.setGoal(iChina, 2, 0)

                                #if (iGameTurn == getTurnForYear(1600)):
                                #        if (pChina.getNumUnits() >= 100):
                                #                self.setGoal(iChina, 2, 1)
                                #        else:
                                #                self.setGoal(iChina, 2, 0)

				if self.getChineseGoldenAgeTurns() >= utils.getTurns(32) and self.getGoal(iChina, 2) == -1:
					self.setGoal(iChina, 2, 1)

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

				# Leoreth: build the Oracle, the Colossus, the Parthenon and the Temple of Artemis by 250 BC
				if iGameTurn == getTurnForYear(-250):
					if self.getGoal(iGreece, 1) == -1:
						self.setGoal(iGreece, 1, 0)

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
				if not pPersia.isReborn():

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
							for iWonder in range(con.iPyramid, con.iNumBuildings):
								if iWonder not in [con.iMilitaryAcademy, con.iItalianArtStudio]:
									iCounter += self.getNumBuildings(iPersia, iWonder)
							iCounter += self.getNumBuildings(iPersia, con.iFlavianAmphitheatre)
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
				else:
					if iGameTurn == getTurnForYear(1650):
						iCount = 0
						for iEurociv in [iGreece, iRome, iByzantium, iVikings, iSpain, iFrance, iGermany, iEngland, iRussia, iPoland, iNetherlands, iPortugal, iItaly]:
							if teamPersia.isOpenBorders(iEurociv):
								iCount += 1
						if iCount >= 6:
							self.setGoal(iPersia, 0, 1)
						else:
							self.setGoal(iPersia, 0, 0)

					if iGameTurn == getTurnForYear(1750):
						bMesopotamia = self.isControlled(iPersia, tSafavidMesopotamiaTL, tSafavidMesopotamiaBR)
						bTransoxania = self.isControlled(iPersia, tTransoxaniaTL, tTransoxaniaBR)
						bNWIndia = self.isControlled(iPersia, tNWIndiaTL, tNWIndiaBR)
						if bMesopotamia and bTransoxania and bNWIndia:
							self.setGoal(iPersia, 1, 1)
						else:
							self.setGoal(iPersia, 1, 0)

					if iGameTurn == getTurnForYear(1800):
						pBestCity = self.getMostCulturedCity(iPersia)
						if pBestCity.getCulture(iPersia) >= utils.getTurns(20000):
							self.setGoal(iPersia, 2, 1)
						else:
							self.setGoal(iPersia, 2, 0)
                                                

                elif (iPlayer == iCarthage):
                        if (pCarthage.isAlive()):
			
				# Leoreth: first goal: build a Palace and the Great Cothon in Carthage by 300 BC
				if self.getGoal(iCarthage, 0) == -1:
					if iGameTurn <= getTurnForYear(-300):
						capital = pCarthage.getCapitalCity()
						bPalace = (capital.getX(), capital.getY()) == (58, 39)
						bGreatCothon = False
						carthagePlot = gc.getMap().plot(58, 39)
						if carthagePlot.isCity:
							if carthagePlot.getPlotCity().isHasRealBuilding(con.iGreatCothon):
								bGreatCothon = True
						if bPalace and bGreatCothon:
							self.setGoal(iCarthage, 0, 1)
					else:
						self.setGoal(iCarthage, 0, 0)
						
				# Leoreth: second goal: control Italy and Iberia in 100 BC
				if iGameTurn == getTurnForYear(-100):
					bItaly = self.isControlled(iCarthage, con.tNormalAreasTL[0][iItaly], con.tNormalAreasBR[0][iItaly], [(62, 47), (63, 47), (63, 46)])
					bIberia = self.isControlled(iCarthage, con.tNormalAreasTL[0][iSpain], con.tNormalAreasBR[0][iSpain])
					if bItaly and bIberia:
						self.setGoal(iCarthage, 1, 1)
					else:
						self.setGoal(iCarthage, 1, 0)
				
				# Leoreth: third goal: have 5000 gold in 200 AD
				if iGameTurn == getTurnForYear(200):
					if pCarthage.getGold() >= utils.getTurns(5000):
						self.setGoal(iCarthage, 2, 1)
					else:
						self.setGoal(iCarthage, 2, 0)


#                                if (self.getGoal(iCarthage, 1) == -1):
#                                        if (iGameTurn <= getTurnForYear(200)):
#                                                #if (pCarthage.countOwnedBonuses(con.iDye) + pCarthage.getBonusImport(con.iDye) >= 3):
#                                                if (pCarthage.getNumAvailableBonuses(con.iDye) >= 4):
#                                                        self.setGoal(iCarthage, 1, 1)
#                                        else:
#                                                self.setGoal(iCarthage, 1, 0)
                                                
#                                if (iGameTurn == getTurnForYear(-100)):                                              
#                                        if (self.checkOwnedCoastalAreaExceptions(iCarthage, tMediterraneanTL, tMediterraneanBR, tMediterraneanExceptions, 5)):
#                                                self.setGoal(iCarthage, 0, 1)
#                                        else:
#                                                self.setGoal(iCarthage, 0, 0)   
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
#				if (iGameTurn == getTurnForYear(200)):
#                                        lRevealedMap = con.l0Array
#                                        for iCiv in range(iNumPlayers):
#                                                for x in range(124):
#                                                        for y in range(68):
#                                                                if (gc.getMap().plot(x, y).isRevealed(iCiv, False)):
#                                                                      lRevealedMap[iCiv] += 1
#                                        bBestMap = True
#                                        for iCiv in range(iNumPlayers):
#                                                if (lRevealedMap[iCarthage] < lRevealedMap[iCiv]):                                                        
#                                                        bBestMap = False
#                                                        break
#
#                                        if (bBestMap == True):
#                                                self.setGoal(iCarthage, 2, 1)
#                                        else:
#                                                self.setGoal(iCarthage, 2, 0)

                elif (iPlayer == iRome):
                        if (pRome.isAlive()):

				if (iGameTurn <= getTurnForYear(100)):
					if (self.getGoal(iRome, 0) == -1):
						iBarracks = self.getNumBuildings(iRome, con.iBarracks)
						iAqueducts = self.getNumBuildings(iRome, con.iAqueduct)
						iAmphitheatres = self.getNumBuildings(iRome, con.iColosseum)
						iForums = self.getNumBuildings(iRome, con.iRomanForum)
						if iBarracks >= 6 and iAqueducts >= 5 and iAmphitheatres >= 4 and iForums >= 3:
							self.setGoal(iRome, 0, 1)
                                                        
				if (iGameTurn == getTurnForYear(100)+1):
					if (self.getGoal(iRome, 0) == -1):
						self.setGoal(iRome, 0, 0)  
                                    
				if (iGameTurn == getTurnForYear(320)):                                              
					bSpain = self.checkOwnedArea(iRome, tNormalAreasTL[0][iSpain], tNormalAreasBR[0][iSpain], 2)
					bFrance = self.checkOwnedArea(iRome, tFranceTL, tNormalAreasBR[0][iFrance], 3)
					bEngland = self.checkOwnedArea(iRome, tCoreAreasTL[0][iEngland], tCoreAreasBR[0][iEngland], 1)
					bCarthage = self.checkOwnedArea(iRome, tCarthageTL, tCarthageBR, 2)
					bByzantium = self.checkOwnedArea(iRome, tCoreAreasTL[0][iByzantium], tCoreAreasBR[0][iByzantium], 4)
					bEgypt = self.checkOwnedArea(iRome, tCoreAreasTL[0][iEgypt], tCoreAreasBR[0][iEgypt], 2)

					if (bSpain and bFrance and bEngland and bCarthage and bByzantium and bEgypt):
						self.setGoal(iRome, 1, 1)   
					else:
						self.setGoal(iRome, 1, 0)

                                                
				#if (iGameTurn == getTurnForYear(1000)):      
				#	if (self.getGoal(iRome, 2) == -1): #see onCityAcquired()
				#		self.setGoal(iRome, 2, 1)


                        
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

				# Leoreth: new first goal: steal five techs by 1600 AD
				#if iGameTurn == getTurnForYear(1600):
				#	if self.getGoal(iJapan, 0) == -1:
				#		self.setGoal(iJapan, 0, 0)

				# Leoreth: new first goal: have 18000 culture in 1600 AD
				if iGameTurn == getTurnForYear(1600):
					if pJapan.countTotalCulture() >= utils.getTurns(18000):
						self.setGoal(iJapan, 0, 1)
					else:
						self.setGoal(iJapan, 0, 0)


                                #if (iGameTurn == getTurnForYear(1930)):
                                #        if (gc.getGame().getTeamRank(iJapan) == 0):
                                #                self.setGoal(iJapan, 1, 1)
                                #        else:
                                #                self.setGoal(iJapan, 1, 0)

				# Leoreth: new second goal: control or vassalize Korea, Manchuria, China, Indochina, Indonesia and Philippines in 1940
				if iGameTurn == getTurnForYear(1940):
					bKorea = self.isControlledOrVassalized(iJapan, tKoreaTL, tKoreaBR)
					bManchuria = self.isControlledOrVassalized(iJapan, tManchuriaTL, tManchuriaBR)
					bChina = self.isControlledOrVassalized(iJapan, tChinaTL, tChinaBR)
					bIndochina = self.isControlledOrVassalized(iJapan, tIndochinaTL, tIndochinaBR)
					bIndonesia = self.isControlledOrVassalized(iJapan, tIndonesiaTL, tIndonesiaBR)
					bPhilippines = self.isControlledOrVassalized(iJapan, tPhilippinesTL, tPhilippinesBR)
					if bKorea and bManchuria and bChina and bIndochina and bIndonesia and bPhilippines:
						self.setGoal(iJapan, 1, 1)
					else:
						self.setGoal(iJapan, 1, 0)

                                                
##                                if (iGameTurn == getTurnForYear(1850)):      
##                                        if (self.getGoal(iJapan, 2) == -1): #see onCityAcquired()
##                                                self.setGoal(iJapan, 2, 1)


		elif iPlayer == iTamils:
			if pTamils.isAlive():
			
				if iGameTurn == getTurnForYear(800):
					if pTamils.getGold() >= utils.getTurns(3000) and pTamils.countTotalCulture() >= utils.getTurns(2000):
						self.setGoal(iTamils, 0, 1)
					else:
						self.setGoal(iTamils, 0, 0)
						
				if iGameTurn == getTurnForYear(1000):
					bDeccan = self.isControlledOrVassalized(iTamils, tDeccanTL, tDeccanBR)
					bSrivijaya = self.isControlledOrVassalized(iTamils, tSrivijayaTL, tSrivijayaBR)
					if bDeccan and bSrivijaya:
						self.setGoal(iTamils, 1, 1)
					else:
						self.setGoal(iTamils, 1, 0)
						
				if iGameTurn <= getTurnForYear(1200):
					iTradeGold = 0
					
					# gold from city trade routes
					iTradeCommerce = 0
					cityList = PyPlayer(iTamils).getCityList()
					for pCity in cityList:
						city = pCity.GetCy()
						iTradeCommerce += city.getTradeYield(2)
					iTradeGold = iTradeCommerce * pTamils.getCommercePercent(0) / 100
					
					# gold from per turn gold trade
					for iCiv in range(con.iNumPlayers):
						iTradeGold += pTamils.getGoldPerTurnByPlayer(iCiv)
						
					self.changeTamilTradeGold(iTradeGold)
					
					if self.getTamilTradeGold() >= utils.getTurns(4000):
						self.setGoal(iTamils, 2, 1)
						
				if iGameTurn == getTurnForYear(1200):
					if self.getGoal(iTamils, 2) == -1:
						self.setGoal(iTamils, 2, 0)


                elif (iPlayer == iEthiopia):
                        if (pEthiopia.isAlive()):

				if iGameTurn <= getTurnForYear(600) and self.getGoal(iEthiopia, 1) == -1:
					if pEthiopia.getNumAvailableBonuses(con.iIncense) >= 3:
						self.setGoal(iEthiopia, 1, 1)

				if iGameTurn == getTurnForYear(600)+1 and self.getGoal(iEthiopia, 1) == -1:
					self.setGoal(iEthiopia, 1, 0)

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
                                                self.setEthiopianControl(1)
                                        else:
                                                self.setGoal(iEthiopia, 2, 0)

                                if (iGameTurn == getTurnForYear(1910) and self.getGoal(iEthiopia, 2) == -1):
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
			
				if not pMaya.isReborn():

					if (iGameTurn == getTurnForYear(600)+1):
						if (self.getGoal(iMaya, 0) == -1): #see onTechAcquired()                                        
							self.setGoal(iMaya, 0, 0)

					if (iGameTurn == getTurnForYear(900)+1):
						if (self.getGoal(iMaya, 1) == -1): #see onBuildingBuilt()
							self.setGoal(iMaya, 1, 0)

					if (iGameTurn == getTurnForYear(1600)):      
						if (self.getGoal(iMaya, 2) == -1): #see onGreatPersonBorn()
							self.setGoal(iMaya, 2, 0)
							
				else:
				
					if iGameTurn == getTurnForYear(1870):
						bPeru = True
						bGranColombia = True
						bGuayanas = True
						bCaribbean = True
						for iEuroCiv in con.lCivGroups[0]:
							if bPeru and not self.checkNotOwnedArea(iEuroCiv, tPeruTL, tPeruBR): bPeru = False
							if bGranColombia and not self.checkNotOwnedArea(iEuroCiv, tGranColombiaTL, tGranColombiaBR): bGranColombia = False
							if bGuayanas and not self.checkNotOwnedArea(iEuroCiv, tGuayanasTL, tGuayanasBR): bGuayanas = False
							if bCaribbean and not self.checkNotOwnedArea(iEuroCiv, tCaribbeanTL, tCaribbeanBR): bCaribbean = False
						if bPeru and bGranColombia and bGuayanas and bCaribbean:
							self.setGoal(iMaya, 0, 1)
						else:
							self.setGoal(iMaya, 0, 0)
							
					if iGameTurn == getTurnForYear(1920):
						if self.isControlled(iMaya, tSAmericaTL, tSAmericaBR, tSouthAmericaExceptions):
							self.setGoal(iMaya, 1, 1)
						else:
							self.setGoal(iMaya, 1, 0)
							
					if self.getGoal(iMaya, 2) == -1:
						iTradeGold = 0
						
						for iLoopCiv in range(con.iNumPlayers):
							iTradeGold += pMaya.getGoldPerTurnByPlayer(iLoopCiv)
							
						self.changeColombianTradeGold(iTradeGold)
						
						if self.getColombianTradeGold() >= utils.getTurns(5000):
							self.setGoal(iMaya, 2, 1)
							
					if iGameTurn == getTurnForYear(1950):
						if self.getGoal(iMaya, 2) == -1:
							self.setGoal(iMaya, 2, 0)
					

		elif (iPlayer == iByzantium):
			if (pByzantium.isAlive()):

				if (iGameTurn == getTurnForYear(1000)):
					if (pByzantium.getGold() >= utils.getTurns(5000)):
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

					if (bBalkans and bNorthAfrica and bNearEast):
						self.setGoal(iByzantium, 2, 1)
					else:
						self.setGoal(iByzantium, 2, 0)
                                                

                elif (iPlayer == iVikings):
                        if (pVikings.isAlive()):
			
				if iGameTurn == getTurnForYear(1050):
					lEuroCivs = [iRome, iByzantium, iSpain, iFrance, iEngland, iHolyRome, iRussia]
					bEuropeanCore = False
					for iEuroCiv in lEuroCivs:
						if self.checkOwnedCiv(iVikings, iEuroCiv):
							bEuropeanCore = True
							break
							
					if bEuropeanCore:
						self.setGoal(iVikings, 0, 1)
					else:
						self.setGoal(iVikings, 0, 0)
						
				if iGameTurn == getTurnForYear(1100):
					if self.getGoal(iVikings, 1) == -1:
						self.setGoal(iVikings, 1, 0)
						
				if self.getVikingGold() >= utils.getTurns(3000) and self.getGoal(iVikings, 2) == -1:
					self.setGoal(iVikings, 2, 1)

                                if (iGameTurn == getTurnForYear(1500)):
					if self.getGoal(iVikings, 2) == -1:
						self.setGoal(iVikings, 2, 0)


                        
                elif (iPlayer == iArabia):
                        if (pArabia.isAlive()):


                                if (self.getGoal(iArabia, 2) == -1):
                                        religionPercent = gc.getGame().calculateReligionPercent(con.iIslam)
                                        #print ("religionPercent", religionPercent)
                                        if (religionPercent >= 40.0):
                                                self.setGoal(iArabia, 2, 1)

                                                

                                #if (iGameTurn == getTurnForYear(1300)):
                                #        iCounter = 0
                                #        for iReligion in range(con.iNumReligions):
                                #                iCurrentShrine = con.iShrine + iReligion*4
                                #                apCityList = PyPlayer(iArabia).getCityList()
                                #                for pCity in apCityList:
                                #                        if (pCity.hasBuilding(iCurrentShrine)):
                                #                                iCounter += 1
                                #                                break
                                #                #iCounter += pArabia.getBuildingClassCount(con.iShrine + iReligion*4) #BUGGY!                                                
                                #                #print (iReligion, con.iShrine + iReligion*4, pArabia.getBuildingClassCount(con.iShrine + iReligion*4))
                                #        if (iCounter >= 3):
                                #                self.setGoal(iArabia, 0, 1)
                                #        else:
                                #                self.setGoal(iArabia, 0, 0)

				# Leoreth: new first Arabian goal: be the most advanced civ in 1300 AD
				if iGameTurn == getTurnForYear(1300):
					if self.getGoal(iArabia, 0) == -1:
						if self.getMostAdvancedCiv(iArabia) == iArabia:
							self.setGoal(iArabia, 0, 1)
						else:
							self.setGoal(iArabia, 0, 0)


                            
                                if (iGameTurn == getTurnForYear(1300)):
					bEgypt = self.isControlledOrVassalized(iArabia, con.tCoreAreasTL[0][iEgypt], con.tCoreAreasBR[0][iEgypt])
					bMaghreb = self.isControlledOrVassalized(iArabia, tCarthageTL, tCarthageBR)
					bMesopotamia = self.isControlledOrVassalized(iArabia, con.tCoreAreasTL[0][iBabylonia], con.tCoreAreasBR[0][iBabylonia])
					bPersia = self.isControlledOrVassalized(iArabia, con.tCoreAreasTL[0][iPersia], con.tCoreAreasBR[0][iPersia])
					bSpain = self.isControlledOrVassalized(iArabia, con.tNormalAreasTL[0][iSpain], con.tNormalAreasBR[0][iSpain])
					if (bEgypt and bMaghreb and bMesopotamia and bPersia and bSpain):
						self.setGoal(iArabia, 1, 1)
					else:
						self.setGoal(iArabia, 1, 0)
							
							
		elif iPlayer == iTibet:
			if pTibet.isAlive():
			
				if iGameTurn == getTurnForYear(1000):
					if self.getGoal(iTibet, 0) == -1:
						self.setGoal(iTibet, 0, 0)
						
				if self.getGoal(iTibet, 1) == -1:				
					if iGameTurn == getTurnForYear(1400):
						self.setGoal(iTibet, 1, 0)
						
					iReligionPercent = gc.getGame().calculateReligionPercent(con.iBuddhism)
					if iReligionPercent >= 30.0:
						self.setGoal(iTibet, 1, 1)
						
				if self.getGoal(iTibet, 2) == -1:
					if iGameTurn == getTurnForYear(1700):
						self.setGoal(iTibet, 2, 0)
						
					plotLhasa = gc.getMap().plot(con.tCapitals[0][iTibet][0], con.tCapitals[0][iTibet][1])
					if plotLhasa.isCity():
						lhasa = plotLhasa.getPlotCity()
						if lhasa.getFreeSpecialistCount(iGreatProphet) >= 5:
							self.setGoal(iTibet, 2, 1)



                elif (iPlayer == iKhmer):
                        if (pKhmer.isAlive()):
				
				if iGameTurn == getTurnForYear(1200):
					if self.getGoal(iKhmer, 0) == -1:
						self.setGoal(iKhmer, 0, 0)

                                if (iGameTurn == getTurnForYear(1450)):
					if self.getGoal(iKhmer, 2) == -1:
						self.setGoal(iKhmer, 2, 0)
					if self.getGoal(iKhmer, 1) == -1:
						self.setGoal(iKhmer, 1, 0)
						
				if self.getGoal(iKhmer, 2) == -1:
                                        if (pKhmer.countTotalCulture() >= utils.getTurns(8000)):
                                                self.setGoal(iKhmer, 2, 1)

				# Leoreth: new first goal: control Shwedagon Paya, Borobudur and Wat Preah Pisnulok in 1450 AD
				#if iGameTurn == getTurnForYear(1450):
				#	bShwedagon = (self.getNumBuildings(iKhmer, con.iShwedagonPaya) > 0)
				#	bBorobudur = (self.getNumBuildings(iKhmer, con.iBorobudur) > 0)
				#	bAngkorWat = (self.getNumBuildings(iKhmer, con.iAngkorWat) > 0)
				#	if bShwedagon and bBorobudur and bAngkorWat:
				#		self.setGoal(iKhmer, 0, 1)
				#	else:
				#		self.setGoal(iKhmer, 0, 0)

                                                
                                if self.getGoal(iKhmer, 1) == -1:
                                        apCityList = PyPlayer(iKhmer).getCityList()
                                        iTotalPopulation = 0
                                        for pCity in apCityList:			
                                                iTotalPopulation += pCity.getPopulation()
                                        if len(apCityList) > 0 and (iTotalPopulation * 1.00 / len(apCityList) >= 12.0):
                                                self.setGoal(iKhmer, 1, 1)
                                        #else:
                                        #       self.setGoal(iKhmer, 1, 0)                                        
                                        #bestCity = self.calculateTopCityPopulation(102, 34)                                        #if (bestCity != -1):
                                        #        if (bestCity.getOwner() == iKhmer and bestCity.getX() == 102 and bestCity.getY() == 34):
                                        #                self.setGoal(iKhmer, 1, 1)
                                        #        else:
                                        #                self.setGoal(iKhmer, 1, 0)


                                #if self.getGoal(iKhmer, 2) == -1 and iGameTurn >= getTurnForYear(1000):
                                #        religionPercent = gc.getGame().calculateReligionPercent(con.iBuddhism) + gc.getGame().calculateReligionPercent(con.iHinduism)
                                #        #print ("religionPercent", religionPercent)
                                #        if (religionPercent >= 35.0):
                                #                self.setGoal(iKhmer, 2, 1)

		elif (iPlayer == iIndonesia):
			if (pIndonesia.isAlive()):

				if iGameTurn == getTurnForYear(1300):
					if self.getHighestPopulationCiv(iIndonesia) == iIndonesia:
						self.setGoal(iIndonesia, 0, 1)
					else:
						self.setGoal(iIndonesia, 0, 0)

				if iGameTurn == getTurnForYear(1500):
					if self.getGoal(iIndonesia, 1) == -1:
						self.setGoal(iIndonesia, 1, 0)

				if self.getGoal(iIndonesia, 1) == -1:
					lHappinessBonuses = [con.iDye, con.iFur, con.iGems, con.iGold, con.iIncense, con.iIvory, con.iSilk, con.iSilver, con.iSpices, con.iSugar, con.iWine, con.iWhales, con.iCotton, con.iCoffee, con.iTea, con.iTobacco]
                                        iCounter = 0
					for iBonus in lHappinessBonuses:
						if pIndonesia.getNumAvailableBonuses(iBonus) > 0:
							iCounter += 1
					if iCounter >= 10:
						self.setGoal(iIndonesia, 1, 1)

				if iGameTurn == getTurnForYear(1940):
					totalPop = gc.getGame().getTotalPopulation()
					ourPop = teamIndonesia.getTotalPopulation()
					if (totalPop > 0):
						popPercent = (ourPop * 100.0) / totalPop
					else:
						popPercent = 0.0

					if popPercent >= 9.0:
						self.setGoal(iIndonesia, 2, 1)
					else:
						self.setGoal(iIndonesia, 2, 0)
						
		elif iPlayer == iMoors:
			if pMoors.isAlive():
			
				if iGameTurn == getTurnForYear(1000):
					bCommerce = False
					mostCommercialCity = self.calculateTopCityCommerce(51, 41)
					if (mostCommercialCity != -1):
                                                if (mostCommercialCity.getOwner() == iMoors and mostCommercialCity.getX() == 51 and mostCommercialCity.getY() == 41):
                                                        bCommerce = True

					bLargest = False
					largestCity = self.calculateTopCityPopulation(51, 41)                                        
                                        if (largestCity != -1):
                                                if (largestCity.getOwner() == iMoors and largestCity.getX() == 51 and largestCity.getY() == 41):
                                                        bLargest = True

					if (bCommerce and bLargest):
						self.setGoal(iMoors, 0, 1)
					else:
						self.setGoal(iMoors, 0, 0)
						
				if iGameTurn == getTurnForYear(1200):
					bIberia = self.checkOwnedArea(iMoors, tIberiaTL, tIberiaBR, 3)
					bMaghreb = self.checkOwnedArea(iMoors, tMaghrebTL, tMaghrebBR, 3)
					bWestAfrica = self.checkOwnedArea(iMoors, tWestAfricaTL, tWestAfricaBR, 3)
					
					if bIberia and bMaghreb and bWestAfrica:
						self.setGoal(iMoors, 1, 1)
					else:
						self.setGoal(iMoors, 1, 0)
						
				if iGameTurn == getTurnForYear(1300):
					plot = gc.getMap().plot(51, 41)
					iCounter = 0
					if plot.isCity:
						capital = plot.getPlotCity()
						for iSpecialist in range(gc.getNumSpecialistInfos()):
							if iSpecialist in [7, 9, 11]: #prophet, scientist, engineer
								iCounter += capital.getFreeSpecialistCount(iSpecialist)
					if iCounter >= 4:
						self.setGoal(iMoors, 2, 1)
					else:
						self.setGoal(iMoors, 2, 0)
					
				
						
                        
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
                                #if (iGameTurn == getTurnForYear(1700)):
                                #        bAztecs = self.checkOwnedCiv(iSpain, iAztecs)
                                #        bInca = self.checkOwnedCiv(iSpain, iInca)                                        
                                #        if (bAztecs and bInca):
                                #                self.setGoal(iSpain, 2, 1)
                                #        else:
                                #                self.setGoal(iSpain, 2, 0)
				
				# Leoreth: total of 10 gold or silver resources by 1650 AD
				if (self.getGoal(iSpain, 1) == -1):
					if iGameTurn <= getTurnForYear(1650):
						iGold = pSpain.getNumAvailableBonuses(con.iGold) - pSpain.getBonusImport(con.iGold)
						iSilver = pSpain.getNumAvailableBonuses(con.iSilver) - pSpain.getBonusImport(con.iSilver)
						
						for iCiv in range(iNumPlayers):
							if iCiv != iSpain:
								if gc.getPlayer(iCiv).isAlive():
									if gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iSpain):
										iGold += gc.getPlayer(iCiv).getNumAvailableBonuses(con.iGold) - gc.getPlayer(iCiv).getBonusImport(con.iGold)
										iSilver += gc.getPlayer(iCiv).getNumAvailableBonuses(con.iSilver) - gc.getPlayer(iCiv).getBonusImport(con.iSilver)
										
						if iGold + iSilver >= 10:
							self.setGoal(iSpain, 1, 1)
					else:
						self.setGoal(iSpain, 1, 0)
						
				# Leoreth: spread Catholicism to 40% and don't allow Protestant civilizations in Europe in 1700 AD
				if iGameTurn == getTurnForYear(1700):
					fReligionPercent = gc.getGame().calculateReligionPercent(con.iChristianity)
					
					bNoProtestants = True
					for iCiv in range(iNumPlayers):
						if gc.getPlayer(iCiv).getStateReligion() == con.iJudaism:
							cityList = PyPlayer(iCiv).getCityList()
							for city in cityList:
								pCity = city.GetCy()
								if pCity.getRegionID() in [con.rIberia, con.rBritain, con.rItaly, con.rEurope, con.rBalkans, con.rScandinavia, con.rRussia]:
									bNoProtestants = False
									break
									break
									
					if bNoProtestants and fReligionPercent >= 40.0:
						self.setGoal(iSpain, 2, 1)
					else:
						self.setGoal(iSpain, 2, 0)
						

				# Leoreth: Have the largest empire of the world in 1760 AD
				#if (iGameTurn == getTurnForYear(1760)):
				#	iSpanishLand = pSpain.getTotalLand()
				#	bLargest = True
				#	
				#	for iCiv in range(0,iNumMajorPlayers):
				#		if (gc.getPlayer(iCiv).getTotalLand() > iSpanishLand):
				#			bLargest = False

				#	if bLargest:
				#		self.setGoal(iSpain, 2, 1)
				#	else:
				#		self.setGoal(iSpain, 2, 0)
                            
                        
                elif (iPlayer == iFrance):
                        if (pFrance.isAlive()):
                            
				# Leoreth: have 25000 culture in Paris in 1700 AD
                                if (iGameTurn == getTurnForYear(1700)):
					pParis = gc.getMap().plot(55, 50)
					if pParis.isCity():
						if pParis.getPlotCity().getCulture(iFrance) >= utils.getTurns(25000):
							self.setGoal(iFrance, 0, 1)
						else:
							self.setGoal(iFrance, 0, 0)
					else:
						self.setGoal(iFrance, 0, 0)
						
				# Leoreth: Control 50% of Europe and North America in 1800 AD
				if iGameTurn == getTurnForYear(1800):
					iEurope, iTotalEurope = self.countControlledTiles(iFrance, con.tEuropeTL, con.tEuropeBR, True)
					iEasternEurope, iTotalEasternEurope = self.countControlledTiles(iFrance, con.tEasternEuropeTL, con.tEasternEuropeBR, True)
					iNorthAmerica, iTotalNorthAmerica = self.countControlledTiles(iFrance, con.tNorthAmericaTL, con.tNorthAmericaBR, True)
					
					fEurope = (iEurope + iEasternEurope) * 100.0 / (iTotalEurope + iTotalEasternEurope)
					fNorthAmerica = iNorthAmerica * 100.0 / iTotalNorthAmerica
					
					if (fEurope >= 40.0 and fNorthAmerica >= 40.0):
						self.setGoal(iFrance, 1, 1)
					else:
						self.setGoal(iFrance, 1, 0)
						
				if iGameTurn == getTurnForYear(1900):
					if self.getGoal(iFrance, 2) == -1:
						self.setGoal(iFrance, 2, 0)

                                            
                        
                elif (iPlayer == iEngland):
                        if (pEngland.isAlive()):


#                                if (self.getGoal(iEngland, 0) == -1):
#                                        if (gc.getGame().getCircumnavigated() != -1):
#                                                if (gc.getGame().getCircumnavigated() == iEngland):
#                                                        self.setGoal(iEngland, 0, 1)
#                                                else:
#                                                        self.setGoal(iEngland, 0, 0)


                                if (iGameTurn == getTurnForYear(1730)):
                                        if (self.getGoal(iEngland, 0) == -1):
                                                self.setGoal(iEngland, 0, 0)

				# Leoreth: Total of 25 Frigates or Ships of the Line, and sink 50 enemy ships
				if (iGameTurn == getTurnForYear(1800)):

					iCShipOfTheLine = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_SHIP_OF_THE_LINE')
					iCFrigate = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_FRIGATE')

					iEnglishNavy = gc.getPlayer(iEngland).getUnitClassCount(iCFrigate) + gc.getPlayer(iEngland).getUnitClassCount(iCShipOfTheLine)

					iEnglishSinks = self.getNumSinks()
					
					if iEnglishNavy >= 25 and iEnglishSinks >= 50:
						self.setGoal(iEngland, 1, 1)
					else:
						self.setGoal(iEngland, 1, 0)
						
						
		elif iPlayer == iHolyRome:
			if pHolyRome.isAlive():
			
				if iGameTurn == getTurnForYear(1200):
					bApostolicPalace = self.getNumBuildings(iHolyRome, con.iApostolicPalace) > 0
					bHolySepulchre = self.getNumBuildings(iHolyRome, con.iChristianShrine) > 0
					if bApostolicPalace and bHolySepulchre:
						self.setGoal(iHolyRome, 0, 1)
					else:
						self.setGoal(iHolyRome, 0, 0)
						
				#if iGameTurn == getTurnForYear(1600) and self.getGoal(iHolyRome, 1) == -1:
				#	self.setGoal(iHolyRome, 2, 0)
				
				if self.getGoal(iHolyRome, 2) == -1:
					x, y = con.tVienna
					pVienna = gc.getMap().plot(x, y)
					iGreatArtists = 0
					if pVienna.isCity():
						iGreatArtists = pVienna.getPlotCity().getFreeSpecialistCount(con.iGreatArtist)
					if iGreatArtists >= 3:
						self.setGoal(iHolyRome, 2, 1)
						
				if iGameTurn == getTurnForYear(1700):
					if self.getGoal(iHolyRome, 2) == -1:
						self.setGoal(iHolyRome, 2, 0)

                elif (iPlayer == iGermany):
                        if (pGermany.isAlive()):

                                #if (iGameTurn == getTurnForYear(1870)):
                                #        bFrance = self.checkOwnedCiv(iGermany, iFrance)
                                #        bRome = self.checkOwnedCiv(iGermany, iRome)
                                #        bGreece = self.checkOwnedCiv(iGermany, iGreece)                                        
                                #        if (bFrance and bRome and bGreece):
                                #                self.setGoal(iGermany, 0, 1)
                                #        else:
                                #                self.setGoal(iGermany, 0, 0)
				
				if iGameTurn == getTurnForYear(1900):
					x, y = con.tCapitals[utils.getReborn(iGermany)][iGermany]
					plot = gc.getMap().plot(x, y)
					iCounter = 0
					if plot.isCity:
						capital = plot.getPlotCity()
						for iSpecialist in range(gc.getNumSpecialistInfos()):
							if iSpecialist >= 7 and iSpecialist != gc.getNumSpecialistInfos()-1: # great priest, slave
								iCounter += capital.getFreeSpecialistCount(iSpecialist)
					if iCounter >= 7:
						self.setGoal(iGermany, 0, 1)
					else:
						self.setGoal(iGermany, 0, 0)
                                                        
                                if (iGameTurn == getTurnForYear(1940)):
                                        bFrance = self.checkOwnedCiv(iGermany, iFrance)
                                        bRome = self.checkOwnedCiv(iGermany, iItaly)
                                        bRussia = self.checkOwnedCiv(iGermany, iRussia)
                                        bEngland = self.checkOwnedCiv(iGermany, iEngland)                                        
                                        bScandinavia = self.checkOwnedCiv(iGermany, iVikings)
                                        if (bFrance and bRome and bRussia and bEngland and bScandinavia):
                                                self.setGoal(iGermany, 1, 1)
                                        else:
                                                self.setGoal(iGermany, 1, 0)
                        
                elif (iPlayer == iRussia):
                        if (pRussia.isAlive()):

                                if (iGameTurn == getTurnForYear(1700)):  
                                        if (self.getGoal(iRussia, 0) == -1):
                                                self.setGoal(iRussia, 0, 0)
						
				# Leoreth: build the Trans-Siberian Railroad by 1920
				if iGameTurn == getTurnForYear(1920):
					if self.getGoal(iRussia, 1) == -1:
						if self.getRussianProjects(0) == -1:
							self.setGoal(iRussia, 1, 0)
							
				if teamRussia.isHasTech(con.iRailroad) and self.getGoal(iRussia, 1) == -1 and self.getRussianProjects(0) == -1:
					if self.isConnectedByRailroad(iRussia, con.tCapitals[0][iRussia], lSiberianCoast):
						self.setRussianProjects(0, 1)
						if self.getRussianProjects(0) == 1 and self.getRussianProjects(1) == 1 and self.getRussianProjects(2) == 1:
							self.setGoal(iRussia, 1, 1)
							
				# Leoreth: have friendly relations with 5 communist civilizations by 1950 AD
				if iGameTurn == getTurnForYear(1950):
					if self.getGoal(iRussia, 2) == -1:
						self.setGoal(iRussia, 2, 0)
						
				if self.getGoal(iRussia, 2) == -1:
					iCount = 0
					for iCiv in range(con.iNumPlayers):
						pPlayer = gc.getPlayer(iCiv)
						if iCiv != iRussia and pPlayer.AI_getAttitude(iRussia) == AttitudeTypes.ATTITUDE_FRIENDLY and (pPlayer.getCivics(1) == con.iSupremeCouncil or pPlayer.getCivics(3) == con.iStateProperty):
							iCount += 1
					
					if iCount >= 5:
						self.setGoal(iRussia, 2, 1)

                                #if (iGameTurn == getTurnForYear(1950)+1):      
                                #        if (self.getGoal(iRussia, 1) == -1): 
                                #                self.setGoal(iRussia, 1, 0)

                                #if (iGameTurn == getTurnForYear(1950)):                                                  
                                #        if (self.getGoal(iRussia, 2) == -1): 
                                #                self.setGoal(iRussia, 2, 1)



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
					if ( pPlot.isCity() and pPlot.getPlotCity().getOwner() == iNetherlands ):
						iGMerchant = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), "SPECIALIST_GREAT_MERCHANT")
						if ( pPlot.getPlotCity().getFreeSpecialistCount(iGMerchant) >= 3 ):
							self.setGoal( iNetherlands, 0, 1 )
				else:
					if ( self.getGoal( iNetherlands, 0 ) == - 1 ):
						self.setGoal( iNetherlands, 0, 0 )   


				if iGameTurn == getTurnForYear(1745):
					if self.getGoal(iNetherlands, 1) == -1:
						self.setGoal(iNetherlands, 1, 0)


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

                                #if (iGameTurn == getTurnForYear(1300)-10): #temporary fix, they use too many specialist and make Mali UHV very hard
                                #        if (not pFrance.isHuman()):
                                #                if (pFrance.getGold() > utils.getTurns(2000)):
                                #                        pFrance.setGold(pFrance.getGold()*50/100)
                                #                elif (pFrance.getGold() > utils.getTurns(1000)):
                                #                        pFrance.setGold(pFrance.getGold()*70/100)
                                                        

                                #if (iGameTurn == getTurnForYear(1300)):
                                #        iGold = pMali.getGold()
                                #        for iCiv in range(iNumPlayers):
                                #                if (iCiv != iMali and gc.getPlayer(iCiv).isAlive()):
                                #                        if (gc.getPlayer(iCiv).getGold() > iGold):
                                #                               self.setGoal(iMali, 0, 0)
                                #                               return
                                #        self.setGoal(iMali, 0, 1)
                                 
                                #if (iGameTurn == getTurnForYear(1500)):
                                #        if (pMali.getGold() >= utils.getTurns(4000)):
                                #                self.setGoal(iMali, 1, 1)
                                #        else:
                                #                self.setGoal(iMali, 1, 0)
                                                
                                #if (iGameTurn == getTurnForYear(1700)):
                                #        if (pMali.getGold() >= utils.getTurns(16000)):
                                #                self.setGoal(iMali, 2, 1)
                                #        else:
                                #                self.setGoal(iMali, 2, 0)
				
				# first goal: conduct a trade mission to your holy city by 1350 AD
				if iGameTurn == getTurnForYear(1350):
					if self.getGoal(iMali, 0) == -1:
						self.setGoal(iMali, 0, 0)
						
				if self.getGoal(iMali, 1) == -1:
					#iGreatProphet = gc.getInfoTypeForString("SPECIALIST_GREAT_PRIEST")
					for pCity in PyPlayer(iMali).getCityList():
						city = pCity.GetCy()
						if city.isHasRealBuilding(con.iSankore):
							if city.getFreeSpecialistCount(iGreatProphet) >= 1:
								self.setGoal(iMali, 1, 1)
								break
								
				# second goal: build the University of Sankore and settle two great prophets in its city
				if iGameTurn == getTurnForYear(1500):
					if self.getGoal(iMali, 1) == -1:
						self.setGoal(iMali, 1, 0)
						
				# third goal: have 6000 gold in 1500 AD and 15000 gold in 1700 AD
				if iGameTurn == getTurnForYear(1500):
					if pMali.getGold() >= utils.getTurns(5000):
						self.setMaliGold(True)
					else:
						self.setGoal(iMali, 2, 0)
						
				if iGameTurn == getTurnForYear(1700):
					if pMali.getGold() >= utils.getTurns(15000):
						if self.getMaliGold():
							self.setGoal(iMali, 2, 1)
					else:
						self.setGoal(iMali, 2, 0)
				
						
		elif iPlayer == iPoland:
			if pPoland.isAlive():
			
				if iGameTurn == getTurnForYear(1400):
					cityList = self.getMostPopulousCities(iPoland, 3)
					iCount = 0
					bComplete = False
					for city in cityList:
						if city.getPopulation() >= 12:
							iCount += 1
						if iCount >= 3:
							bComplete = True
							break
							
					if bComplete:
						self.setGoal(iPoland, 0, 1)
					else:
						self.setGoal(iPoland, 0, 0)
						
				if iGameTurn == getTurnForYear(1600):
					if self.getGoal(iPoland, 2) == -1:
						self.setGoal(iPoland, 2, 0)

                elif (iPlayer == iTurkey):
                        if (pTurkey.isAlive()):

                                #if (self.getGoal(iTurkey, 0) == -1):
                                #        if (iGameTurn <= getTurnForYear(1500)):
                                #                pIstanbulE = gc.getMap().plot( 68, 45 )
                                #                pIstanbulE2 = gc.getMap().plot( 67, 45 )
                                #                pIstanbulA = gc.getMap().plot( 69, 44 )
                                #                if (pIstanbulE.isCity()):                                                        
                                #                        if (pIstanbulE.getPlotCity().getOwner() == iTurkey):
                                #                                self.setGoal(iTurkey, 0, 1)
                                #                elif (pIstanbulA.isCity()):                                                        
                                #                        if (pIstanbulA.getPlotCity().getOwner() == iTurkey):
                                #                                self.setGoal(iTurkey, 0, 1)
                                #                elif (pIstanbulE2.isCity()):                                                        
                                #                        if (pIstanbulE2.getPlotCity().getOwner() == iTurkey):
                                #                                self.setGoal(iTurkey, 0, 1)
                                #        else:
                                #                self.setGoal(iTurkey, 0, 0)


                                #if (iGameTurn == getTurnForYear(1700)):
                                #        bBalkans = self.checkOwnedArea(iTurkey, tBalkansTL, tBalkansBR, 3)
                                #        bBlackSea = self.checkOwnedAreaAdjacentArea(iTurkey, tBlackSeaTL, tBlackSeaBR, 4, (71,47))
                                #        bMesopotamia = self.checkOwnedArea(iTurkey, tMesopotamiaTL, tMesopotamiaBR, 3)
                                #        if (bBalkans and bBlackSea and bMesopotamia):
                                #                self.setGoal(iTurkey, 1, 1)
                                #        else:
                                #                self.setGoal(iTurkey, 1, 0)

                                #if (iGameTurn == getTurnForYear(1870)):
                                #        iCounter = 0
                                #        for iCiv in range(iNumPlayers):
                                #                if (iCiv != iTurkey):
                                #                        if (gc.getPlayer(iCiv).isAlive()):
                                #                                if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iTurkey)):
                                #                                        iCounter += 1
                                #        if (iCounter >= 3):
                                #                self.setGoal(iTurkey, 2, 1)
                                #        else:
                                #                self.setGoal(iTurkey, 2, 0)

				# Leoreth: new first goal: have four wonders in your capital in 1550 AD
				if iGameTurn == getTurnForYear(1550):
					capital = pTurkey.getCapitalCity()
					iCounter = 0
					for iWonder in range(con.iPyramid, con.iNumBuildings):
						if iWonder not in [con.iMilitaryAcademy, con.iItalianArtStudio]:
							if capital.isHasRealBuilding(iWonder):
								iCounter += 1
					if capital.isHasRealBuilding(con.iFlavianAmphitheatre):
						iCounter += 1
					if iCounter >= 4:
						self.setGoal(iTurkey, 0, 1)
					else:
						self.setGoal(iTurkey, 0, 0)

				# Leoreth: new second goal: control the Eastern Mediterranean, the Black Sea, Cairo, Mecca, Baghdad and Vienna in 1700 AD
				if iGameTurn == getTurnForYear(1700):
					
					bEasternMediterranean = self.isCultureControlled(iTurkey, lEasternMediterranean)
					bBlackSea = self.isCultureControlled(iTurkey, lBlackSea)
					bCairo = self.controlsCity(iTurkey, tCairo)
					bMecca = self.controlsCity(iTurkey, tMecca)
					bBaghdad = self.controlsCity(iTurkey, tBaghdad)
					bVienna = self.controlsCity(iTurkey, tVienna)

					if bEasternMediterranean and bBlackSea and bCairo and bMecca and bBaghdad and bVienna:
						self.setGoal(iTurkey, 1, 1)
					else:
						self.setGoal(iTurkey, 1, 0)

				# Leoreth: new third goal: have the largest military power in 1800 AD
				if iGameTurn == getTurnForYear(1800):
					if self.getMostPowerfulCiv(iTurkey) == iTurkey:
						self.setGoal(iTurkey, 2, 1)
					else:
						self.setGoal(iTurkey, 2, 0)



                elif (iPlayer == iPortugal):
                        if (pPortugal.isAlive()):

                                #if (iGameTurn == getTurnForYear(1500)):
                                #        lRevealedMap = con.l0Array
                                #        for iCiv in range(iNumPlayers):
				#		if gc.getPlayer(iCiv).isAlive():
	                        #                        for x in range(124):
        	                #                                for y in range(68):
                	        #                                        if (gc.getMap().plot(x, y).isRevealed(iCiv, False)):
                        	#                                              lRevealedMap[iCiv] += 1
                                #        bBestMap = True
                                #        for iCiv in range(iNumPlayers):
                                #                if (lRevealedMap[iPortugal] < lRevealedMap[iCiv]):                                                        
                                #                        bBestMap = False
                                #                        break

                                #        if (bBestMap == True):
                                #                self.setGoal(iPortugal, 0, 1)
                                #        else:
                                #                self.setGoal(iPortugal, 0, 0)

				# first goal: have open borders with 14 civilizations by 1550 AD
                                if (self.getGoal(iPortugal, 0) == -1):
					iCount = 0
					for iLoopCiv in range(iNumMajorPlayers):
					       if (iLoopCiv != iPortugal):
							if (teamPortugal.isOpenBorders(iLoopCiv)):
							       iCount += 1
					if (iCount >= 14):                                                                    
						self.setGoal(iPortugal, 0, 1)

				if iGameTurn == getTurnForYear(1550):
					if self.getGoal(iPortugal, 0) == -1:
						self.setGoal(iPortugal, 0, 0)
						
				# second goal: acquire 12 colonial resources by 1650 AD
				if self.getGoal(iPortugal, 1) == -1:
					iCount = 0
					for iBonus in [con.iBanana, con.iSpices, con.iSugar, con.iCoffee, con.iTea, con.iTobacco]:
						iCount += pPortugal.getNumAvailableBonuses(iBonus)
					if iCount >= 12:
						self.setGoal(iPortugal, 1, 1)
						
				if iGameTurn == getTurnForYear(1650):
					if self.getGoal(iPortugal, 1) == -1:
						self.setGoal(iPortugal, 1, 0)
						
				# third goal: control 15 cities in Brazil, Africa and Asia in 1700 AD
				if iGameTurn == getTurnForYear(1700):
					iCount = self.getNumCitiesInArea(iPortugal, tBrazilTL, tBrazilBR)
					iCount += self.getNumCitiesInArea(iPortugal, tAfricaTL, tAfricaBR)
					iCount += self.getNumCitiesInArea(iPortugal, tAsiaTL, tAsiaBR)
					if iCount >= 15:
						self.setGoal(iPortugal, 2, 1)
					else:
						self.setGoal(iPortugal, 2, 0)

                            
                        
                elif (iPlayer == iInca):
                        if (pInca.isAlive()):

                                if self.getGoal(iInca, 0) == -1:
					if self.isRoad(iInca, lAndeanCoast) and self.getNumBuildings(iInca, con.iIncanTambo) >= 5:
						self.setGoal(iInca, 0, 1)
						
				if iGameTurn == getTurnForYear(1500):
					if self.getGoal(iInca, 0) == -1:
						self.setGoal(iInca, 0, 0)
					
				if iGameTurn == getTurnForYear(1550):
					if pInca.getGold() >= utils.getTurns(2500):
						self.setGoal(iInca, 1, 1)
					else:
						self.setGoal(iInca, 1, 0)
						
				if iGameTurn == getTurnForYear(1700):
					iControl, iTotal = self.countControlledTiles(iInca, tSAmericaTL, tSAmericaBR, False, tSouthAmericaExceptions)
					fControl = iControl * 100.0 / iTotal
					
					if fControl >= 60.0:
						self.setGoal(iInca, 2, 1)
					else:
						self.setGoal(iInca, 2, 0)

		elif iPlayer == iItaly:
			if pItaly.isAlive():
			
				if iGameTurn == getTurnForYear(1500):
					if self.getGoal(iItaly, 0) == -1:
						self.setGoal(iItaly, 0, 0)
			
				if iGameTurn < getTurnForYear(1600):
					iCount = 0
					cityList = PyPlayer(iPlayer).getCityList()
					for city in cityList:
						pCity = city.GetCy()
						if pCity.getCultureLevel() >= 5:
							iCount += 1
							
					if iCount >= 3:
						self.setGoal(iItaly, 1, 1)

				if iGameTurn == getTurnForYear(1600):
					if self.getGoal(iItaly, 1) == -1:
						self.setGoal(iItaly, 1, 0)

				if (iGameTurn == getTurnForYear(1930)):
					iMediterranean, iTotalMediterranean = self.countControlledTiles(iItaly, tMediterraneanTL, tMediterraneanBR, False, tMediterraneanExceptions, True)
					fMediterranean = iMediterranean * 100.0 / iTotalMediterranean
					
					if fMediterranean >= 65.0:
						self.setGoal(iItaly, 2, 1)
					else:
						self.setGoal(iItaly, 2, 0)

                        
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
						
						
		elif iPlayer == iMughals:
			if pMughals.isAlive():
			
				if iGameTurn == getTurnForYear(1500):
					if self.getGoal(iMughals, 0) == -1:
						self.setGoal(iMughals, 0, 0)
						
				if iGameTurn == getTurnForYear(1660):
					if self.getGoal(iMughals, 1) == -1:
						self.setGoal(iMughals, 1, 0)
						
				if iGameTurn == getTurnForYear(1750):
					if pMughals.countTotalCulture() >= utils.getTurns(50000):
						self.setGoal(iMughals, 2, 1)
					else:
						self.setGoal(iMughals, 2, 0)
						
				#if iGameTurn == getTurnForYear(1750):
				#	totalPop = gc.getGame().getTotalPopulation()
				#	ourPop = teamMughals.getTotalPopulation()
				#	if (totalPop > 0):
				#		popPercent = (ourPop * 100.0) / totalPop
				#	else:
				#		popPercent = 0.0
				#	if popPercent >= 15.0:
				#		self.setGoal(iMughals, 2, 1)
				#	else:
				#		self.setGoal(iMughals, 2, 0)
                            
                        
                elif (iPlayer == iAztecs):
                        if (pAztecs.isAlive()):
				if not pAztecs.isReborn():

					if iGameTurn == getTurnForYear(1520):
						bestCity = self.calculateTopCityPopulation(18, 37)
						if bestCity != -1:
							if bestCity.getOwner() == iAztecs and bestCity.getX() == 18 and bestCity.getY() == 37:
								self.setGoal(iAztecs, 0, 1)
							else:
								self.setGoal(iAztecs, 0, 0)
						else:
							self.setGoal(iAztecs, 0, 0)
							
					if iGameTurn == getTurnForYear(1650):
						if self.getGoal(iAztecs, 1) == -1:
							self.setGoal(iAztecs, 1, 0)
							
					if self.getGoal(iAztecs, 2) == -1:
						if self.getEnslavedUnits() >= 20:
							self.setGoal(iAztecs, 2, 1)
							
				else:
					
					#if iGameTurn == getTurnForYear(1850):
					#	iCentralAmerica = self.getNumCitiesInArea(iAztecs, tCentralAmericaTL, tCentralAmericaBR)
					#	iWesternNorthAmerica = self.getNumCitiesInArea(iAztecs, tWesternNorthAmericaTL, tWesternNorthAmericaBR)
					#	
					#	if iCentralAmerica >= 6 and iWesternNorthAmerica >= 6:
					#		self.setGoal(iAztecs, 0, 1)
					#	else:
					#		self.setGoal(iAztecs, 0, 0)
					
					if iGameTurn == getTurnForYear(1880):
						if self.getGoal(iAztecs, 0) == -1:
							self.setGoal(iAztecs, 0, 0)
							
					#if iGameTurn == getTurnForYear(1920):
					#	if self.getLargestReligionCiv(iAztecs, con.iCatholicism) == iAztecs:
					#		self.setGoal(iAztecs, 1, 1)
					#	else:
					#		self.setGoal(iAztecs, 1, 0)
					
					if iGameTurn == getTurnForYear(1940):
						if self.getGoal(iAztecs, 1) == -1:
							self.setGoal(iAztecs, 1, 0)
							
					if iGameTurn == getTurnForYear(1960): 
						bestCity = self.calculateTopCityCulture(18, 37)
						if bestCity != -1:
							if bestCity.getOwner() == iAztecs and bestCity.getX() == 18 and bestCity.getY() == 37:
								self.setGoal(iAztecs, 2, 1)
							else:
								self.setGoal(iAztecs, 2, 0)
						else:
							self.setGoal(iAztecs, 2, 0)

		elif iPlayer == iThailand:
			if pThailand.isAlive():

				if iGameTurn == getTurnForYear(1650):
					iCount = 0
					for iCiv in range(iNumMajorPlayers):
						if iCiv != iThailand:
							if teamThailand.isOpenBorders(iCiv):
								iCount += 1
					if iCount >= 10:
						self.setGoal(iThailand, 0, 1)
					else:
						self.setGoal(iThailand, 0, 0)

				if iGameTurn == getTurnForYear(1700):
					bestCity = self.calculateTopCityPopulation(101, 33)
					if bestCity != -1:
						if bestCity.getOwner() == iThailand and bestCity.getX() in [101, 102] and bestCity.getY() == 33:
							self.setGoal(iThailand, 1, 1)
						else:
							self.setGoal(iThailand, 1, 0)
					else:
						self.setGoal(iThailand, 1, 0)

				if iGameTurn == getTurnForYear(1900):
					bSouthAsia = self.isAreaFreeOfCivs(tSouthAsiaTL, tSouthAsiaBR, [iIndia, iTamils, iKhmer, iIndonesia, iMughals, iThailand])
					if bSouthAsia:
						self.setGoal(iThailand, 2, 1)
					else:
						self.setGoal(iThailand, 2, 0)
						
		
		elif iPlayer == iCongo:
			if pCongo.isAlive():
			
				if self.getGoal(iCongo, 0) == -1:
					if self.getApostolicVotePercent(iCongo) >= 10.0:
						self.setGoal(iCongo, 0, 1)
			
				if iGameTurn == getTurnForYear(1650):
					if self.getGoal(iCongo, 0) == -1:
						self.setGoal(iCongo, 0, 0)
						
				if iGameTurn == getTurnForYear(1800):
					if self.getGoal(iCongo, 1) == -1:
						self.setGoal(iCongo, 1, 0)


                        
                elif (iPlayer == iAmerica):
                        if (pAmerica.isAlive()):

                                if (iGameTurn == getTurnForYear(1930)):
                                        bAmericas = True
                                        for iEuroCiv in range(iNumPlayers):
                                                if (iEuroCiv in con.lCivGroups[0]):
                                                        if (self.checkNotOwnedArea(iEuroCiv, tNCAmericaTL, tNCAmericaBR) == False):
                                                                bAmericas = False
                                                                break
					bMexico = self.isControlledOrVassalized(iAmerica, con.tCoreAreasTL[1][iAztecs], con.tCoreAreasBR[1][iAztecs], con.tExceptions[1][iAztecs])
                                        if bAmericas and bMexico:
                                                self.setGoal(iAmerica, 0, 1)
                                        else:
                                                self.setGoal(iAmerica, 0, 0)

                                if (iGameTurn == getTurnForYear(2000)+1):
                                        if (self.getGoal(iAmerica, 1) == -1):
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
						
		elif iPlayer == iArgentina:
			if pArgentina.isAlive():
			
				if iGameTurn == getTurnForYear(1900):
					capital = pArgentina.getCapitalCity()
					iGreatGeneral = gc.getInfoTypeForString("SPECIALIST_GREAT_GENERAL")
					if capital.getFreeSpecialistCount(iGreatGeneral) >= 2:
						self.setGoal(iArgentina, 0, 1)
					else:
						self.setGoal(iArgentina, 0, 0)
						
				if iGameTurn == getTurnForYear(1930):
					pHighestCommerceCity = self.calculateHighestCommerceCity()
					if pHighestCommerceCity.getOwner() == iArgentina:
						self.setGoal(iArgentina, 1, 1)
					else:
						self.setGoal(iArgentina, 1, 0)
			
				if self.getGoal(iArgentina, 2) == -1:
					pBuenosAires = gc.getMap().plot(con.tCapitals[0][iArgentina][0], con.tCapitals[0][iArgentina][1])
					if pBuenosAires.isCity():
						if pBuenosAires.getPlotCity().getCulture(iArgentina) >= utils.getTurns(25000):
							self.setGoal(iArgentina, 2, 1)
							
				if iGameTurn == getTurnForYear(1960):
					if self.getGoal(iArgentina, 2) == -1:
						self.setGoal(iArgentina, 2, 0)

		
		elif iPlayer == iBrazil:
			if pBrazil.isAlive():
			
				if iGameTurn == getTurnForYear(1880):
					if self.countImprovements(iBrazil, con.iSlavePlantation) >= 10 and self.countImprovements(iBrazil, con.iPasture) >= 4:
						self.setGoal(iBrazil, 0, 1)
					else:
						self.setGoal(iBrazil, 0, 0)
						
				if iGameTurn == getTurnForYear(1950):
					if self.countImprovements(iBrazil, con.iForestPreserve) >= 20 and pBrazil.getCapitalCity().isHasRealBuilding(con.iNationalPark):
						self.setGoal(iBrazil, 2, 1)
					else:
						self.setGoal(iBrazil, 2, 0)


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
                                if (self.getGoal(iPlayer, 0) == 1 and self.getGoal(iPlayer, 1) == 1 and self.getGoal(iPlayer, 2) == 1) and gc.getGame().getGameTurnYear() >= con.tBirth[utils.getHumanID()]: #Leoreth: don't win during autoplay
                                        gc.getGame().setWinner(iPlayer, 7) #Historical Victory




        def onCityBuilt(self, city, iPlayer): #see onCityBuilt in CvRFCEventHandler

                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return
			
		# Leoreth: don't check AI civs to improve speed
		if utils.getHumanID() != iPlayer and self.isIgnoreAI():
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
                        if (self.getGoal(iVikings, 1) == -1):
                                if (city.getX() >= tAmericasTL[0] and city.getX() <= tAmericasBR[0] and city.getY() >= tAmericasTL[1] and city.getY() <= tAmericasBR[1]):
##                                        bFirst = True
##                                        for iCiv in range(iNumPlayers):
##                                                if ((iCiv != iVikings) and (iCiv not in con.lCivGroups[5])):
##                                                        if (self.checkNotOwnedArea(iCiv, tAmericasTL, tAmericasBR) == False):
##                                                                bFirst = False
##                                                                break
##                                        if (bFirst):
                                        if (self.getNewWorld(0) == -1 or self.getNewWorld(0) == iPlayer):
                                                self.setGoal(iVikings, 1, 1)
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


                              
                #elif (iPlayer == iFrance):
                #        if (iGameTurn <= getTurnForYear(1760)):
                #                if (self.getGoal(iFrance, 1) == -1):       
                #                        bNECanada = self.checkFoundedArea(iFrance, tNECanadaTL, tNECanadaBR, 3)
                #                        bLouisiana = self.checkFoundedArea(iFrance, tLouisianaTL, tLouisianaBR, 1) 
                #                        if (bNECanada and bLouisiana):
                #                                self.setGoal(iFrance, 1, 1)
                                                

                elif (iPlayer == iEngland):
                        if (iGameTurn <= getTurnForYear(1730)):
                                if (self.getGoal(iEngland, 1) == -1):
                                        #bEastCoast = self.checkOwnedArea(iEngland, tEastCoastTL, tEastCoastBR, 2)
                                        #bSouthAfrica = self.checkOwnedArea(iEngland, tSouthAfricaTL, tSouthAfricaBR, 1)
                                        #bAustralia = self.checkOwnedArea(iEngland, tAustraliaTL, tAustraliaBR, 2)
                                        #print ("English UHV:", bEastCoast, bSouthAfrica, bAustralia)
                                        #if (bEastCoast and bSouthAfrica and bAustralia):
                                        bNAmerica = self.checkOwnedArea(iEngland, con.tNorthAmericaTL, con.tNorthAmericaBR, 5)
                                        bSCAmerica = self.checkOwnedArea(iEngland, con.tSouthCentralAmericaTL, con.tSouthCentralAmericaBR, 3)
                                        bAfrica = self.checkOwnedArea(iEngland, tAfricaTL, tAfricaBR, 4)
                                        bAsia = self.checkOwnedArea(iEngland, tAsiaTL, tAsiaBR, 5)
                                        bOceania = self.checkOwnedArea(iEngland, tOceaniaTL, tOceaniaBR, 3)
                                        if (bNAmerica and bSCAmerica and bAfrica and bAsia and bOceania):
                                                self.setGoal(iEngland, 0, 1)


                elif (iPlayer == iRussia):
                        if (iGameTurn <= getTurnForYear(1700)):
                                if (self.getGoal(iRussia, 0) == -1):
                                        bSiberia = self.checkFoundedArea(iRussia, tSiberiaTL, tSiberiaBR, 7)                                    
                                        if (bSiberia):
                                                self.setGoal(iRussia, 0, 1)

                #elif (iPlayer == iPortugal):
                #        if (self.getGoal(iPortugal, 2) == -1):
                #                if (not (city.getX() >= tEuropeTL[0] and city.getX() <= tEuropeBR[0] and city.getY() >= tEuropeTL[1] and city.getY() <= tEuropeBR[1])):
                #                        self.setPortugueseColonies(self.getPortugueseColonies() + 1)
                #                        if (self.getPortugueseColonies() >= 15):
                #                                self.setGoal(iPortugal, 2, 1)
						
		elif iPlayer == iTibet:
			if self.getGoal(iTibet, 0) == -1:
				if pTibet.getNumCities() >= 5:
					self.setGoal(iTibet, 0, 1)
						
                #if (self.getGoal(iNetherlands, 1) == -1):
                #        if (city.getX() >= tAustraliaTL[0] and city.getX() <= tAustraliaBR[0] and city.getY() >= tAustraliaTL[1] and city.getY() <= tAustraliaBR[1]):
                #                if iPlayer == iNetherlands:
		#			self.setGoal(iNetherlands, 1, 1)
                #                else:
                #                        self.setGoal(iNetherlands, 1, 0)

                                                
                        
        def onReligionFounded(self, iReligion, iFounder):

                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return

                iPlayer = iFounder

                if (iFounder == iIndia):
                        self.setReligionFounded(iReligion, 1)

                #if (self.getGoal(iIndia, 0) == -1):
                #        if (iReligion == con.iHinduism):
                #                if (iFounder != iIndia):
                #                        self.setGoal(iIndia, 0, 0) 
                #        elif (iReligion == con.iBuddhism):
                #                if (iFounder != iIndia):
                #                        self.setGoal(iIndia, 0, 0)
                #        if (self.getReligionFounded(con.iHinduism) == 1 and self.getReligionFounded(con.iBuddhism) == 1):
                #                self.setGoal(iIndia, 0, 1)     

                #if (self.getGoal(iIndia, 1) == -1):
                #        iCounter = 0
                #        for i in range(con.iNumReligions):
                #                if (self.getReligionFounded(i) == 1):
                #                        iCounter += 1
                #        if (iCounter >= 5):
                #                self.setGoal(iIndia, 1, 1)

                #        if (self.getGoal(iIndia, 1) == -1):
                #                iFounded = 0
                #                for iLoopReligion in range(con.iNumReligions):
                #                        if (gc.getGame().isReligionFounded(iLoopReligion)):
                #                                iFounded += 1
                #                if (iFounded == con.iNumReligions):
                #                        self.setGoal(iIndia, 1, 0)


                #if (iPlayer == iEthiopia):
                #        if (pEthiopia.isAlive()):
                #                if (self.getGoal(iEthiopia, 0) == -1):
                #                        self.setGoal(iEthiopia, 0, 1)

                #elif (iReligion == con.iJudaism):
                #        if (self.getGoal(iEthiopia, 0) == -1):
                #                self.setGoal(iEthiopia, 0, 0)
				
		if iReligion == con.iJudaism:
			if iPlayer == iHolyRome and self.getGoal(iHolyRome, 1) == -1:
				self.setGoal(iHolyRome, 1, 1)
			else:
				self.setGoal(iHolyRome, 1, 0)
				
		if iReligion == con.iChristianity:
			if iPlayer == iEthiopia and self.getGoal(iEthiopia, 0) == -1:
				self.setGoal(iEthiopia, 0, 1)
			else:
				self.setGoal(iEthiopia, 0, 0)
			
				
				


        def onCityAcquired(self, owner, playerType, bConquest, city):

                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return
			
		if utils.getHumanID() != playerType and self.isIgnoreAI():
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

                #if (iPlayer == iRome):
                #        if (pRome.isAlive()):
                #                if (bConquest):
                #                        if (self.getGoal(iRome, 2) == -1):
                #                                if (iGameTurn <= getTurnForYear(1000)):
                #                                        if (playerType == iBarbarian):
                #                                                self.setGoal(iRome, 2, 0)

##                elif (iPlayer == iJapan):
##                        if (pJapan.isAlive()):
##                                if (bConquest):
##                                        if (self.getGoal(iJapan, 2) == -1):
##                                                if (iGameTurn <= getTurnForYear(1850)):
##                                                        self.setGoal(iJapan, 2, 0)


                #elif (iPlayer == iMaya):
                #        if (pMaya.isAlive()):
                #                if (bConquest):
                #                        if (self.getGoal(iMaya, 2) == -1):
                #                                if (iGameTurn <= getTurnForYear(1745)):
                #                                        self.setGoal(iMaya, 2, 0)
                                        
                #elif (iPlayer == iRussia):
                #        if (pRussia.isAlive()):
                #                if (bConquest):
                #                        if (self.getGoal(iRussia, 2) == -1):
                #                                if (iGameTurn <= getTurnForYear(1950)):
                #                                        self.setGoal(iRussia, 2, 0)

		if (playerType == iEngland):
                        if (iGameTurn <= getTurnForYear(1730)):
                                        bNAmerica = self.checkOwnedArea(iEngland, con.tNorthAmericaTL, con.tNorthAmericaBR, 5)
                                        bSCAmerica = self.checkOwnedArea(iEngland, con.tSouthCentralAmericaTL, con.tSouthCentralAmericaBR, 3)
                                        bAfrica = self.checkOwnedArea(iEngland, tAfricaTL, tAfricaBR, 4)
                                        bAsia = self.checkOwnedArea(iEngland, tAsiaTL, tAsiaBR, 5)
                                        bOceania = self.checkOwnedArea(iEngland, tOceaniaTL, tOceaniaBR, 3)
                                        if (bNAmerica and bSCAmerica and bAfrica and bAsia and bOceania):
                                                self.setGoal(iEngland, 0, 1)   
						
		if playerType == iNetherlands:
			if owner in [iSpain, iFrance, iEngland, iPortugal, iVikings, iItaly, iRussia, iGermany, iHolyRome, iPoland]:
				x = city.getX()
				y = city.getY()
				bColony = (city.getRegionID() not in [con.rBritain, con.rIberia, con.rItaly, con.rBalkans, con.rEurope, con.rScandinavia, con.rRussia])
					
				if bColony and bConquest:
					self.changeDutchColonies(1)
					if self.getDutchColonies() >= 4:
						self.setGoal(iNetherlands, 1, 1)
						
		if playerType == iTibet:
			if self.getGoal(iTibet, 0) == -1:
				if pTibet.getNumCities() >= 5:
					self.setGoal(iTibet, 0, 1)

        def onCityRazed(self, iPlayer, city):

                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return
			
		if utils.getHumanID() != iPlayer and self.isIgnoreAI():
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
		
		# Leoreth: ignore AI civs to improve speed 
		# important: include all civs with tech goals in list so that the check is made for all players to catch failed goals
		if self.isIgnoreAI() and utils.getHumanID() != iPlayer and utils.getHumanID() not in [iChina, iBabylonia, iGreece, iRome, iPoland, iKorea, iEngland, iJapan, iGermany, iMaya, iAztecs, iCongo]:
			return
		
		# Chinese UHV: Compass, Paper, Gunpowder, Printing Press
		if iTech == con.iCompass:
			if self.getChineseTechs(0) == -1:
				if iPlayer == iChina:
					self.setChineseTechs(0, 1)
				else:
					self.setChineseTechs(0, 0)
					self.setGoal(iChina, 1, 0)

		elif iTech == con.iPaper:
			if self.getChineseTechs(1) == -1:
				if iPlayer == iChina:
					self.setChineseTechs(1, 1)
				else:
					self.setChineseTechs(1, 0)
					self.setGoal(iChina, 1, 0)

		elif iTech == con.iGunpowder:
			if self.getChineseTechs(2) == -1:
				if iPlayer == iChina:
					self.setChineseTechs(2, 1)
				else:
					self.setChineseTechs(2, 0)
					self.setGoal(iChina, 1, 0)

		elif iTech == con.iPrintingPress:
			if self.getChineseTechs(3) == -1:
				if iPlayer == iChina:
					self.setChineseTechs(3, 1)
				else:
					self.setChineseTechs(3, 0)
					self.setGoal(iChina, 1, 0)

		if iTech in [con.iCompass, con.iPaper, con.iGunpowder, con.iPrintingPress] and self.getGoal(iChina, 1) == -1:
			if self.getChineseTechs(0) == 1 and self.getChineseTechs(1) == 1 and self.getChineseTechs(2) == 1 and self.getChineseTechs(3) == 1:
				self.setGoal(iChina, 1, 1)

		# Babylonian UHV: Writing, Code of Laws, Monarchy
		if iTech == con.iWriting:
			if self.getBabylonianTechs(0) == -1:
				if iPlayer == iBabylonia:
					self.setBabylonianTechs(0, 1)
				else:
					self.setBabylonianTechs(0, 0)
					self.setGoal(iBabylonia, 0, 0)

		elif iTech == con.iCodeOfLaws:
			if self.getBabylonianTechs(1) == -1:
				if iPlayer == iBabylonia:
					self.setBabylonianTechs(1, 1)
				else:
					self.setBabylonianTechs(1, 0)
					self.setGoal(iBabylonia, 0, 0)

		elif iTech == con.iMonarchy:
			if self.getBabylonianTechs(2) == -1:
				if iPlayer == iBabylonia:
					self.setBabylonianTechs(2, 1)
				else:
					self.setBabylonianTechs(2, 0)
					self.setGoal(iBabylonia, 0, 0)

		if iTech in [con.iWriting, con.iCodeOfLaws, con.iMonarchy] and self.getGoal(iBabylonia, 0) == -1:
			if self.getBabylonianTechs(0) == 1 and self.getBabylonianTechs(1) == 1 and self.getBabylonianTechs(2) == 1:
				self.setGoal(iBabylonia, 0, 1)


		# Greek UHV: Literature, Drama, Philosophy
		if iTech == con.iLiterature:
			if self.getGreekTechs(0) == -1:
				if iPlayer == iGreece:
					self.setGreekTechs(0, 1)
				else:
					self.setGreekTechs(0, 0)
					self.setGoal(iGreece, 0, 0)

		elif iTech == con.iDrama:
			if self.getGreekTechs(1) == -1:
				if iPlayer == iGreece:
					self.setGreekTechs(1, 1)
				else:
					self.setGreekTechs(1, 0)
					self.setGoal(iGreece, 0, 0)

		elif iTech == con.iPhilosophy:
			if self.getGreekTechs(2) == -1:
				if iPlayer == iGreece:
					self.setGreekTechs(2, 1)
				else:
					self.setGreekTechs(2, 0)
					self.setGoal(iGreece, 0, 0)

		if iTech in [con.iLiterature, con.iDrama, con.iPhilosophy] and self.getGoal(iGreece, 0) == -1:
			if self.getGreekTechs(0) == 1 and self.getGreekTechs(1) == 1 and self.getGreekTechs(2) == 1:
				self.setGoal(iGreece, 0, 1)
				
		# Roman UHV: Theology, Machinery and Civil Service
		if iTech == con.iTheology:
			if self.getRomanTechs(0) == -1:
				if iPlayer == iRome:
					self.setRomanTechs(0, 1)
				else:
					self.setRomanTechs(0, 0)
					self.setGoal(iRome, 2, 0)
		
		elif iTech == con.iMachinery:
			if self.getRomanTechs(1) == -1:
				if iPlayer == iRome:
					self.setRomanTechs(1, 1)
				else:
					self.setRomanTechs(1, 0)
					self.setGoal(iRome, 2, 0)
					
		elif iTech == con.iCivilService:
			if self.getRomanTechs(2) == -1:
				if iPlayer == iRome:
					self.setRomanTechs(2, 1)
				else:
					self.setRomanTechs(2, 0)
					self.setGoal(iRome, 2, 0)
					
		if iTech in [con.iTheology, con.iMachinery, con.iCivilService] and self.getGoal(iRome, 2) == -1:
			if self.getRomanTechs(0) == 1 and self.getRomanTechs(1) == 1 and self.getRomanTechs(2) == 1:
				self.setGoal(iRome, 2, 1)
				
		# Polish UHV: Liberalism
		if iTech == con.iLiberalism:
			if self.getGoal(iPoland, 1) == -1:
				if iPlayer == iPoland:
					self.setGoal(iPoland, 1, 1)
				else:
					self.setGoal(iPoland, 1, 0)
					
		#elif iTech == con.iAstronomy:
		#	if self.getPolishTechs(1) == -1:
		#		if iPlayer == iPoland:
		#			self.setPolishTechs(1, 1)
		#		else:
		#			self.setGoal(iPoland, 1, 0)
					
		#if iTech in [con.iLiberalism, con.iAstronomy] and self.getGoal(iPoland, 1) == -1:
		#	if self.getPolishTechs(0) == 1 and self.getPolishTechs(1) == 1:
		#		self.setGoal(iPoland, 1, 1)


		# Italian UHV: Banking, Patronage, Education, Radio, Electricity, Fascism
		#if iTech == con.iBanking:
		#	if self.getItalianTechs(0) == -1:
		#		if iPlayer == iItaly:
		#			self.setItalianTechs(0, 1)
		#		else:
		#			print "Italian UHV: banking discovered by player " + str(iPlayer)
		#			self.setGoal(iItaly, 0, 0)
					
		#elif iTech == con.iPatronage:
		#	if self.getItalianTechs(1) == -1:
		#		if iPlayer == iItaly:
		#			self.setItalianTechs(1, 1)
		#		else:
		#			print "Italian UHV: patronage discovered by player " + str(iPlayer)
		#			self.setGoal(iItaly, 0, 0)

		#elif iTech == con.iEducation:
		#	if self.getItalianTechs(2) == -1:
		#		if iPlayer == iItaly:
		#			self.setItalianTechs(2, 1)
		#		else:
		#			print "Italian UHV: education discovered by player " + str(iPlayer)
		#			self.setGoal(iItaly, 0, 0)
					
		#elif iTech == con.iElectricity:
		#	if self.getItalianTechs(3) == -1:
		#		if iPlayer == iItaly:
		#			self.setItalianTechs(3, 1)
		#		else:
		#			print "Italian UHV: electricity discovered by player " + str(iPlayer)
		#			self.setGoal(iItaly, 0, 0)

		#elif iTech == con.iRadio:
		#	if self.getItalianTechs(4) == -1:
		#		if iPlayer == iItaly:
		#			self.setItalianTechs(4, 1)
		#		else:
		#			print "Italian UHV: radio discovered by player " + str(iPlayer)
		#			self.setGoal(iItaly, 0, 0)

		#elif iTech == con.iFascism:
		#	if self.getItalianTechs(5) == -1:
		#		if iPlayer == iItaly:
		#			self.setItalianTechs(5, 1)
		#		else:
		#			print "Italian UHV: fascism discovered by player " + str(iPlayer)
		#			self.setGoal(iItaly, 0, 0)

		#if iTech in [con.iBanking, con.iPatronage, con.iEducation, con.iElectricity, con.iRadio, con.iFascism] and self.getGoal(iItaly, 0) == -1:
		#	if self.getItalianTechs(0) == 1 and self.getItalianTechs(1) == 1 and self.getItalianTechs(2) == 1 and self.getItalianTechs(3) == 1 and self.getItalianTechs(4) == 1 and self.getItalianTechs(5) == 1:
		#		self.setGoal(iItaly, 0, 1)
					
		# Korean UHV: Printing Press
		if iTech == con.iPrintingPress:
			if self.getGoal(iKorea, 1) == -1:
				if iPlayer == iKorea:
					self.setGoal(iKorea, 1, 1)
				else:
					self.setGoal(iKorea, 1, 0)
					
		# Arabian UHV: discover all medieval techs by 1300 AD
		#if iPlayer == iArabia and self.getGoal(iArabia, 0) == -1:
		#	if gc.getTechInfo(iTech).getEra() == con.iMedieval:
		#		bAllMedieval = True
		#		for iLoopTech in range(con.iNumTechs):
		#			if gc.getTechInfo(iLoopTech).getEra() == con.iMedieval:
		#				if not teamArabia.isHasTech(iLoopTech) and iLoopTech != iTech:
		#					bAllMedieval = False
		#					break
		#		if bAllMedieval:
		#			self.setGoal(iArabia, 0, 1)
			
		# English UHV: be first to enter the Industrial and Modern eras
		if self.getGoal(iEngland, 2) == -1 and iGameTurn >= getTurnForYear(1400):
			if gc.getTechInfo(iTech).getEra() == iIndustrial:
				if self.getEnglishEras(0) == -1:
					if iPlayer == iEngland:
						self.setEnglishEras(0, 1)
						if self.getEnglishEras(1) == 1:
							self.setGoal(iEngland, 2, 1)
					else:
						self.setGoal(iEngland, 2, 0)
			elif gc.getTechInfo(iTech).getEra() == iModern:
				if self.getEnglishEras(1) == -1:
					if iPlayer == iEngland:
						self.setEnglishEras(1, 1)
						if self.getEnglishEras(0) == 1:
							self.setGoal(iEngland, 2, 1)
					else:
						self.setGoal(iEngland, 2, 0)

                if (iPlayer == iJapan):
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

		
                elif (iPlayer == iMaya):
                        if (pMaya.isAlive()):
                                if (self.getGoal(iMaya, 0) == -1): #eof error???
                                        if (iTech == con.iCalendar):
                                                if (iGameTurn <= getTurnForYear(600)):
                                                        self.setGoal(iMaya, 0, 1)



                #elif (iPlayer == iEngland):
                #        if (pEngland.isAlive()):
                #                if (iGameTurn >= getTurnForYear(1300)):
                #                        if (self.getGoal(iEngland, 2) == -1):
                #                                englishEra = pEngland.getCurrentEra()
		#				utils.debugTextPopup("Era entered: "+str(englishEra))
                #                                if (englishEra == iIndustrial):
		#					utils.debugTextPopup("Entered Industrial Era")
                #                                        if (self.getEnglishEras(0) == -1): #just entered
                #                                                bFirst = True
                #                                                for iCiv in range(iNumPlayers):
                #                                                        if (iCiv != iEngland):
                #                                                                if (gc.getPlayer(iCiv).getCurrentEra() == iIndustrial):
                #                                                                        bFirst = False
                #                                                                        break
                #                                               if (bFirst):
		#							utils.debugTextPopup("First to enter Industrial Era")
                #                                                        self.setEnglishEras(0, 1)
                #                                                else:
                #                                                        self.setEnglishEras(0, 0)
                #                                if (englishEra == iModern):
                #                                        if (self.getEnglishEras(1) == -1): #just entered
                #                                                bFirst = True
                #                                                for iCiv in range(iNumPlayers):
                #                                                        if (iCiv != iEngland):
                #                                                                if (gc.getPlayer(iCiv).getCurrentEra() == iModern):
                #                                                                        bFirst = False
                #                                                                        break
                #                                                if (bFirst):
                #                                                        self.setEnglishEras(1, 1)
                #                                                        if (self.getEnglishEras(0) == 1):
                #                                                                self.setGoal(iEngland, 2, 1)
                #                                                        else:
                #                                                                self.setGoal(iEngland, 2, 0)
                #                                                else:
                #                                                        self.setEnglishEras(1, 0)
                #                                                        self.setGoal(iEngland, 2, 0)

                                                                        


                
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
                                                        

                #elif (iPlayer == iAztecs):
                #        if (self.getGoal(iAztecs, 2) == -1):
                #                if (iGameTurn <= getTurnForYear(1860)):                            
                #                        aztecEra = pAztecs.getCurrentEra()
                #                        if (aztecEra == iIndustrial):
                #                                self.setGoal(iAztecs, 2, 1)                                        
                #                else:
                #                        self.setGoal(iAztecs, 2, 0)
					
		if self.getGoal(iCongo, 2) == -1:
			iEra = gc.getTechInfo(iTech).getEra()
			if iEra == iIndustrial and iPlayer == iCongo:
				self.setGoal(iCongo, 2, 1)
			if iEra == iModern and iPlayer != iCongo:
				self.setGoal(iCongo, 2, 0)
                                                



        def onBuildingBuilt(self, iPlayer, iBuilding):

                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return
			
		# Leoreth: ignore AI civs to improve speed
		# important: add all civs with wonder goals to the list so their failure will be checked
		if self.isIgnoreAI() and utils.getHumanID() != iPlayer and utils.getHumanID() not in [iEgypt, iGreece, iCarthage, iMaya, iKhmer, iFrance, iMali, iItaly, iMughals, iAmerica, iBrazil]:
			return

                iGameTurn = gc.getGame().getGameTurn()
		
		# goals for ordinary buildings (do not fail if someone else builds the same building)
		
		# China: build two Confucian and Taoist Cathedrals
		if iPlayer == iChina:
			if pChina.isAlive():
				if self.getGoal(iChina, 0) == -1:
					if iBuilding in [con.iConfucianCathedral, con.iTaoistCathedral]:
						iConfucian = self.getNumBuildings(iChina, con.iConfucianCathedral)
						iTaoist = self.getNumBuildings(iChina, con.iTaoistCathedral)
						if iConfucian >= 2 and iTaoist >= 2:
							self.setGoal(iChina, 0, 1)
				
		# India: build 20 temples
		elif iPlayer == iIndia:
			if pIndia.isAlive():
				if self.getGoal(iIndia, 1) == -1:
					lTemples = [con.iJewishTemple, con.iChristianTemple, con.iIslamicTemple, con.iHinduTemple, con.iBuddhistTemple, con.iConfucianTemple, con.iTaoistTemple, con.iZoroastrianTemple]
					if iBuilding in lTemples:
						iCounter = 0
						for iTemple in lTemples:
							iCounter += self.getNumBuildings(iIndia, iTemple)
						if iCounter >= 20:
							self.setGoal(iIndia, 1, 1)
			
		# Korea: build a Confucian and a Buddhist Cathedral
		elif iPlayer == iKorea:
			if pKorea.isAlive():
				if self.getGoal(iKorea, 0) == -1:
					if iBuilding in [con.iBuddhistCathedral, con.iConfucianCathedral]:
						bBuddhistCathedral = (self.getNumBuildings(iKorea, con.iBuddhistCathedral) > 0)
						bConfucianCathedral = (self.getNumBuildings(iKorea, con.iConfucianCathedral) > 0)
						if bBuddhistCathedral and bConfucianCathedral:
							self.setGoal(iKorea, 0, 1)
			
		# Khmer: build four Buddhist and four Hindu monasteries and Angkor Wat
		elif iPlayer == iKhmer:
			if pKhmer.isAlive():
				if self.getGoal(iKhmer, 0) == -1:
					if iBuilding in [con.iBuddhistMonastery, con.iHinduMonastery]:
						if self.getWondersBuilt(iKhmer) >= 1 and self.getNumBuildings(iKhmer, con.iBuddhistMonastery) >= 4 and self.getNumBuildings(iKhmer, con.iHinduMonastery) >= 4:
							self.setGoal(iKhmer, 0, 1)
			
		# Poland: build a total of three Catholic, Orthodox and Protestant Cathedrals
		elif iPlayer == iPoland:
			if pPoland.isAlive():
				if self.getGoal(iPoland, 2) == -1:
					if iBuilding in [con.iChristianCathedral, con.iOrthodoxCathedral, con.iJewishCathedral]:
						self.setWondersBuilt(iPoland, self.getWondersBuilt(iPoland) + 1)
						iCatholic = self.getNumBuildings(iPoland, con.iChristianCathedral)
						iOrthodox = self.getNumBuildings(iPoland, con.iOrthodoxCathedral)
						iProtestant = self.getNumBuildings(iPoland, con.iJewishCathedral)
						if self.getWondersBuilt(iPoland) >= 3 and iCatholic+iOrthodox+iProtestant >= 3:
							self.setGoal(iPoland, 2, 1)

		# Mughals: build three Islamic Cathedrals
                elif iPlayer == iMughals:
			if pMughals.isAlive():
				if self.getGoal(iMughals, 0) == -1:
					if iBuilding == con.iIslamicCathedral:
						if self.getNumBuildings(iMughals, con.iIslamicCathedral) >= 3:
							self.setGoal(iMughals, 0, 1)
							
		# Aztecs: build 6 pagan temples and sacrificial altars
		elif iPlayer == iAztecs:
			if pAztecs.isAlive() and not pAztecs.isReborn():
				if self.getGoal(iAztecs, 1) == -1:
					if iBuilding in [con.iPaganTemple, con.iAztecSacrificialAltar]:
						iTemples = self.getNumBuildings(iAztecs, con.iPaganTemple)
						iAltars = self.getNumBuildings(iAztecs, con.iAztecSacrificialAltar)
						if iTemples >= 6 and iAltars >= 6:
							self.setGoal(iAztecs, 1, 1)
					
		# Mexico: build three cathedrals of your state religion
			if pAztecs.isAlive() and pAztecs.isReborn():
				if self.getGoal(iAztecs, 0) == -1:
					iStateReligion = pAztecs.getStateReligion()
					if iStateReligion >= 0:
						iCathedral = con.iCathedral + 4*iStateReligion
						if iBuilding == iCathedral:
							if self.getNumBuildings(iAztecs, iCathedral) >= 3:
								self.setGoal(iAztecs, 0, 1)
							
							
		# Inca: build 5 tambos and a road along the Andean coast
		elif iPlayer == iInca:
			if pInca.isAlive():
				if self.getGoal(iInca, 0) == -1:
					if iBuilding == con.iIncanTambo:
						if self.isRoad(iInca, lAndeanCoast) and self.getNumBuildings(iInca, con.iIncanTambo) >= 5:
							self.setGoal(iInca, 0, 1)
							
		# goals for wonders (fail if someone else completes the building)
				
		# Egypt: build the Pyramids, the Great Library and the Great Lighthouse
		if iBuilding in [con.iPyramid, con.iGreatLibrary, con.iGreatLighthouse]:
			if iPlayer == iEgypt:
				if self.getGoal(iEgypt, 1) == -1:
					self.setWondersBuilt(iEgypt, self.getWondersBuilt(iEgypt) + 1)
				if self.getWondersBuilt(iEgypt) == 3:
					self.setGoal(iEgypt, 1, 1)
			else:
				self.setGoal(iEgypt, 1, 0)
				
		# Greece: build the Oracle, the Colossus, the Parthenon and the Temple of Artemis
		if iBuilding in [con.iOracle, con.iColossus, con.iParthenon, con.iArtemis]:
			if iPlayer == iGreece:
				if self.getGoal(iGreece, 1) == -1:
					self.setWondersBuilt(iGreece, self.getWondersBuilt(iGreece) + 1)
				if self.getWondersBuilt(iGreece) == 4:
					self.setGoal(iGreece, 1, 1)
			else:
				self.setGoal(iGreece, 1, 0)
		
		# Phoenicia: build the Great Cothon
		if iBuilding == con.iGreatCothon:
			if iPlayer != iCarthage:
				self.setGoal(iCarthage, 0, 0)

		# Maya: build the Temple of Kukulkan
                if iBuilding == con.iTempleOfKukulkan:      
                        if iPlayer == iMaya:
				if self.getGoal(iMaya, 1) == -1:                                                                         
					self.setGoal(iMaya, 1, 1)
                        else:
                                self.setGoal(iMaya, 1, 0)
				
		# Khmer: build Angkor Wat and four Buddhist and Hindu monasteries
		if iBuilding == con.iAngkorWat:
			if iPlayer == iKhmer:
				if self.getGoal(iKhmer, 0) == -1:
					self.setWondersBuilt(iKhmer, 1)
					if self.getNumBuildings(iKhmer, con.iBuddhistMonastery) >= 4 and self.getNumBuildings(iKhmer, con.iHinduMonastery) >= 4:
						self.setGoal(iKhmer, 0, 1)
			else:
				self.setGoal(iKhmer, 0, 0)
		
		# France: build Notre Dame, Versailles, the Statue of Liberty and the Eiffel Tower
		if iBuilding in [con.iNotreDame, con.iVersailles, con.iStatueOfLiberty, con.iEiffelTower]:
			if iPlayer == iFrance:
				if self.getGoal(iFrance, 2) == -1:
					self.setWondersBuilt(iFrance, self.getWondersBuilt(iFrance) + 1)
				if self.getWondersBuilt(iFrance) == 4:
					self.setGoal(iFrance, 2, 1)
			else:
				self.setGoal(iFrance, 2, 0)
		
		# Mali: build the University of Sankore
		if iBuilding == con.iSankore:
			if iPlayer != iMali:
				self.setGoal(iMali, 1, 0)
		
		# Italy: build the San Marco Basilica, the Sistine Chapel and the Leaning Towe
		if iBuilding in [con.iSanMarcoBasilica, con.iSistineChapel, con.iLeaningTower]:
			if iPlayer == iItaly:
				if self.getGoal(iItaly, 0) == -1:
					self.setWondersBuilt(iItaly, self.getWondersBuilt(iItaly) + 1)
				if self.getWondersBuilt(iItaly) == 3:
					self.setGoal(iItaly, 0, 1)
			else:
				self.setGoal(iItaly, 0, 0)
					
		# Mughals: build the Taj Mahal, the Red Fort and Harmandir Sahib
		if iBuilding in [con.iTajMahal, con.iRedFort, con.iHarmandirSahib]:
			if iPlayer == iMughals:
				if self.getGoal(iMughals, 1) == -1:
					self.setWondersBuilt(iMughals, self.getWondersBuilt(iMughals) + 1)
				if self.getWondersBuilt(iMughals) == 3:
					self.setGoal(iMughals, 1, 1)
			else:
				self.setGoal(iMughals, 1, 0)
				
		# America: build the Statue of Liberty, the Empire State Building, the Pentagon and the United Nations
		if iBuilding in [con.iStatueOfLiberty, con.iEmpireState, con.iPentagon, con.iUnitedNations]:
			if iPlayer == iAmerica:
				if self.getGoal(iAmerica, 1) == -1:
					self.setWondersBuilt(iAmerica, self.getWondersBuilt(iAmerica) + 1)
				if self.getWondersBuilt(iAmerica) == 4:
					self.setGoal(iAmerica, 1, 1)
			else:
				self.setGoal(iAmerica, 1, 0)
				
		# Brazil: build Wembley, Cristo Redentor and the Three Gorges Dam
		if iBuilding in [con.iWembley, con.iCristoRedentor, con.iThreeGorgesDam]:
			if iPlayer == iBrazil:
				if self.getGoal(iBrazil, 1) == -1:
					self.setWondersBuilt(iBrazil, self.getWondersBuilt(iBrazil) + 1)
				if self.getWondersBuilt(iBrazil) == 3:
					self.setGoal(iBrazil, 1, 1)
			else:
				self.setGoal(iBrazil, 1, 0)


                            
        def onProjectBuilt(self, iPlayer, iProject):

                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return
			
		# Leoreth: ignore AI civs to improve speed
		# only if human isn't Russia, but for all players so that the Russian goal can fail
		if self.isIgnoreAI() and utils.getHumanID() != iRussia:
			return

                iGameTurn = gc.getGame().getGameTurn()

		if self.getGoal(iRussia, 1) == -1:
			if (iProject == con.iApolloProgram):
				if (iPlayer == iRussia):
					if self.getGoal(iRussia, 1) == -1:
						self.setRussianProjects(2, 1)
						if self.getRussianProjects(0) == 1 and self.getRussianProjects(1) == 1 and self.getRussianProjects(2) == 1:
							self.setGoal(iRussia, 1, 1)
				else:
					self.setGoal(iRussia, 1, 0)
				
			elif iProject == con.iManhattanProject:
				if iPlayer == iRussia:
					if self.getGoal(iRussia, 1) == -1:
						self.setRussianProjects(1, 1)
						if self.getRussianProjects(0) == 1 and self.getRussianProjects(1) == 1 and self.getRussianProjects(2) == 1:
							self.setGoal(iRussia, 1, 1)
				else:
					self.setGoal(iRussia, 1, 0)



        def onCombatResult(self, argsList):
            
                if (not gc.getGame().isVictoryValid(7)): #7 == historical
                        return

                pWinningUnit,pLosingUnit = argsList
                pWinningPlayer = gc.getPlayer(pWinningUnit.getOwner())
                pLosingPlayer = gc.getPlayer(pLosingUnit.getOwner())
                cLosingUnit = PyHelpers.PyInfo.UnitInfo(pLosingUnit.getUnitType())
                iPlayer = pWinningPlayer.getID()
		
		# Leoreth: ignore AI civs to improve speed
		if self.isIgnoreAI() and utils.getHumanID() != iPlayer:
			return

                if (iPlayer == iEngland):
                        if (self.getGoal(iEngland, 1) == -1):
                                if (cLosingUnit.getDomainType() == gc.getInfoTypeForString("DOMAIN_SEA")):
                                        self.setNumSinks(self.getNumSinks() + 1)

		if (iPlayer == iKorea):
			if (self.getGoal(iKorea, 2) == -1):
				if (cLosingUnit.getDomainType() == gc.getInfoTypeForString("DOMAIN_SEA")):
					self.setNumKoreanSinks(self.getNumKoreanSinks() + 1)
					if (self.getNumKoreanSinks() == 20):
						self.setGoal(iKorea, 2, 1)
						
		#if iPlayer == iTamils:
		#	if self.getGoal(iTamils, 2) == -1:
		#		if cLosingUnit.getDomainType() == gc.getInfoTypeForString("DOMAN_SEA"):
		#			self.setNumTamilSinks(self.getNumTamilSinks() + 1)
		#			if self.getNumTamilsSinks() == 25:
		#				self.setGoal(iTamils, 2, 1)

	def onGreatPersonBorn(self, argsList):
		pUnit, iPlayer, pCity = argsList
		
		# Leoreth: ignore AI civs to improve speed
		if self.isIgnoreAI() and utils.getHumanID() != iPlayer:
			return
		
		pUnitInfo = gc.getUnitInfo(pUnit.getUnitType())
		iGreatGeneral = gc.getInfoTypeForString("SPECIALIST_GREAT_GENERAL")
		
		# Maya third goal: get a great general
		if iPlayer == iMaya and not utils.isReborn(iMaya):
			if self.getGoal(iMaya, 2) == -1:
				if pUnitInfo.getGreatPeoples(iGreatGeneral):
					self.setGoal(iMaya, 2, 1)
					
		# Mexican second goal: get three great generals
		if iPlayer == iAztecs and utils.isReborn(iPlayer):
			if self.getGoal(iAztecs, 1) == -1:
				if pUnitInfo.getGreatPeoples(iGreatGeneral):
					if gc.getPlayer(iPlayer).getGreatGeneralsCreated() >= 3:	
						self.setGoal(iAztecs, 1, 1)
		

	def onGreatGeneralBorn(self, iPlayer):
	
		# Leoreth: ignore AI civs to improve speed
		if self.isIgnoreAI() and utils.getHumanID() != iPlayer:
			return

		# Leoreth: new third goal for Maya: get a great general by 1600 AD
		if iPlayer == iMaya:
			if self.getGoal(iMaya, 2) == -1:
				if gc.getGame().getGameTurn() <= getTurnForYear(1600):
					self.setGoal(iMaya, 2, 1)


	def onTechStolen(self, iPlayer, iTech):
		return
		# Leoreth: first goal for Japan: steal five technologies by 1600 AD
		#if iPlayer == iJapan:
		#	self.increaseTechsStolen()
		#	if self.getTechsStolen() == 5:
		#		sd.setGoal(iJapan, 0, 1)
		
	def onVassalState(self, iMaster, iVassal):
	
		# method isn't called anymore
	
		# Leoreth: ignore AI civs to improve speed
		if self.isIgnoreAI() and utils.getHumanID() != iMaster:
			return
	
		#if iMaster == iHolyRome:
		#	iCount = 0
		#	for iCiv in [iGreece, iRome, iByzantium, iVikings, iSpain, iFrance, iEngland, iRussia, iPoland, iPortugal, iItaly, iNetherlands]:
		##		if utils.getMaster(iCiv) == iHolyRome:
		#			iCount += 1
		#	if iCount >= 3:
		#		self.setGoal(iHolyRome, 2, 1)
				
	def onUnitPillage(self, iPlayer, iGold):
		if iPlayer == iVikings:
			self.changeVikingGold(iGold)
			
	def onCityCaptureGold(self, iPlayer, iGold):
		if iPlayer == iVikings:
			self.changeVikingGold(iGold)
			
	def onPlayerGoldTrade(self, iPlayer, iGold):
		if iPlayer == iTamils:
			self.changeTamilTradeGold(iGold)
			
	def onPlayerSlaveTrade(self, iPlayer, iGold):
	
		if self.isIgnoreAI() and utils.getHumanID() != iPlayer: return
	
		if iPlayer == iCongo:
			self.changeCongoSlaveCounter(iGold)
			if self.getGoal(iCongo, 1) == -1 and self.getCongoSlaveCounter() >= utils.getTurns(1000):
				self.setGoal(iCongo, 1, 1)
			
	def onTradeMission(self, iPlayer, iX, iY, iGold):
	
		# Leoreth: ignore AI civs to improve speed
		if self.isIgnoreAI() and utils.getHumanID() != iPlayer:
			return
	
		if iPlayer == iTamils:
			self.changeTamilTradeGold(iGold)
			
		elif iPlayer == iMali:
			iStateReligion = pMali.getStateReligion()
			#utils.debugTextPopup('Mande state religion ' + str(gc.getReligionInfo(iStateReligion).getText()))
			if iStateReligion != -1:
				pHolyCity = gc.getGame().getHolyCity(iStateReligion)
				
				#utils.debugTextPopup('Holy city: ' + str(pHolyCity.getX()) + ', ' + str(pHolyCity.getY()))
				#utils.debugTextPopup('Trader location: ' + str(iX) + ', ' + str(iY))
				
				if pHolyCity.getX() == iX and pHolyCity.getY() == iY:
					self.setGoal(iMali, 0, 1)

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
		
	def calculateTopCityCommerce(self, x, y):
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
                                        iTotalCityValue = pCity.GetCy().getYieldRate(2)
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
		return gc.getPlayer(iPlayer).countNumBuildings(iBuilding)


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
			if gc.getGame().getGameTurn() >= getTurnForYear(con.tBirth[iCiv]) and gc.getPlayer(iCiv).isAlive():
				iCurrentGold = gc.getPlayer(iCiv).getGold()
				if iCurrentGold > iBestGold:
					iBest = iCiv
					iBestGold = iCurrentGold
		return iBest

	# Leoreth: new implementation of the Arabian conquest goal
	# all cities in the area must now be held either by you or one of your vassals
	def isControlledOrVassalized(self, iPlayer, tTopLeft, tBottomRight, tExceptions=()):
		bControlled = False
		lOwnerList = []
		lValidOwners = [iPlayer]
		dummy, lCityPlotList = utils.squareSearch(tTopLeft, tBottomRight, utils.cityPlots, iPlayer)
		for tPlot in lCityPlotList:
			x, y = tPlot
			iOwner = gc.getMap().plot(x,y).getPlotCity().getOwner()
			if iOwner not in lOwnerList and iOwner < con.iNumPlayers and (x,y) not in tExceptions:
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

	def isControlled(self, iPlayer, tTopLeft, tBottomRight, tExceptions=()):
		bControlled = False
		lOwnerList = []
		dummy, lCityPlotList = utils.squareSearch(tTopLeft, tBottomRight, utils.cityPlots, iPlayer)
		for tPlot in lCityPlotList:
			x, y = tPlot
			iOwner = gc.getMap().plot(x,y).getPlotCity().getOwner()
			if iOwner not in lOwnerList and iOwner < con.iNumPlayers and tPlot not in tExceptions:
				lOwnerList.append(gc.getMap().plot(x,y).getPlotCity().getOwner())
		if iPlayer in lOwnerList:
			bControlled = True
			lOwnerList.remove(iPlayer)
		if len(lOwnerList) > 0:
			bControlled = False
		return bControlled

	def getNumTechs(self, iCiv):
		iCount = 0
		for iTech in range(con.iNumTechs):
			if gc.getTeam(iCiv).isHasTech(iTech):
				iCount += 1
		return iCount
		
	def getTotalTechValue(self, iCiv):
		iValue = 0
		for iTech in range(con.iNumTechs):
			if gc.getTeam(iCiv).isHasTech(iTech):
				iValue += gc.getTechInfo(iTech).getResearchCost()
		return iValue

	def getMostAdvancedCiv(self, iCiv):
		iBestCiv = iCiv
		iBestTechs = self.getTotalTechValue(iCiv)
		for iLoopCiv in range(con.iNumPlayers):
			if gc.getPlayer(iLoopCiv).isAlive():
				iTempTechs = self.getTotalTechValue(iLoopCiv)
				if iTempTechs > iBestTechs:
					iBestCiv = iLoopCiv
					iBestTechs = iTempTechs
		return iBestCiv

	# only allow the civs in lCivList in the area
	def isAreaFreeOfCivs(self, tTopLeft, tBottomRight, lCivList):
		lOwnerList = []
		lCities = utils.getAreaCities(tTopLeft, tBottomRight)
		for city in lCities:
			iOwner = city.getOwner()
			if iOwner not in lCivList and iOwner < con.iNumPlayers:
				if iOwner not in lOwnerList:
					lOwnerList.append(iOwner)
		if len(lOwnerList) == 0:
			return True
		else:
			return False

	def getMostPowerfulCiv(self, iCiv):
		iBestCiv = iCiv
		iBestPower = gc.getPlayer(iCiv).getPower()
		for iLoopCiv in range(con.iNumPlayers):
			iTempPower = gc.getPlayer(iLoopCiv).getPower()
			if iTempPower > iBestPower:
				iBestCiv = iLoopCiv
				iBestPower = iTempPower
		return iBestCiv
		
	def getHighestCommercePerCapitaCiv(self, iCiv):
		iPopulation = gc.getPlayer(iCiv).getTotalPopulation()
		iBestCiv = iCiv
		
		if iPopulation == 0:
			iBestCommerce = 0
		else:
			iBestCommerce = gc.getPlayer(iCiv).calculateTotalCommerce() / iPopulation
			
		for iLoopCiv in range(con.iNumPlayers):
			iPopulation = gc.getPlayer(iLoopCiv).getTotalPopulation()
			if iPopulation == 0:
				iTempCommerce = 0
			else:
				iTempCommerce = gc.getPlayer(iLoopCiv).calculateTotalCommerce() / iPopulation
			if iTempCommerce > iBestCommerce:
				iBestCiv = iLoopCiv
				iBestCommerce = iTempCommerce
		return iBestCiv

	#Leoreth: checks if the given tile or one of its neighbors contain a city owned by iCiv
	def controlsCity(self, iCiv, tPlot):
		x, y = tPlot
		for i in range(x-1, x+2):
			for j in range(y-1, y+2):
				if gc.getMap().plot(i, j).isCity():
					if gc.getMap().plot(i, j).getPlotCity().getOwner() == iCiv:
						return True
		return False

	#Leoreth: be the only civ who culture controls the tiles in the plot list
	def isCultureControlled(self, iCiv, lPlotList):
		for tPlot in lPlotList:
			x, y = tPlot
			plot = gc.getMap().plot(x, y)
			if plot.getOwner() != -1 and plot.getOwner() != iCiv:
				return False
		return True

	def getMostCulturedCity(self, iCiv):
		lCityList = PyPlayer(iPersia).getCityList()
		pBestCity = lCityList[0].GetCy()
		iBestCulture = pBestCity.getCulture(iCiv)
		for pCity in lCityList:
			iTempCulture = pCity.GetCy().getCulture(iCiv)
			if iTempCulture > iBestCulture:
				pBestCity = pCity.GetCy()
				iBestCulture = iTempCulture
		return pBestCity
		
	def countControlledTiles(self, iPlayer, tTL, tBR, bVassals=False, lExceptions=[], bCoastalOnly=False):
		lValidOwners = [iPlayer]
		iCount = 0
		iTotal = 0
		
		if bVassals:
			for iCiv in range(con.iNumPlayers):
				if gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iPlayer):
					lValidOwners.append(iCiv)
					
		for x in range(tTL[0], tBR[0]+1):
			for y in range(tTL[1], tBR[1]+1):
				plot = gc.getMap().plot(x, y)
				if not plot.isWater() and not (x,y) in lExceptions:
					if bCoastalOnly and not gc.getMap().plot(x,y).isCoastalLand(): continue
					iTotal += 1
					if plot.getOwner() in lValidOwners:
						iCount += 1
					
		return iCount, iTotal
		
	def isConnectedByRailroad(self, iPlayer, tStart, lTargetList):
		if len(lTargetList) == 0:
			return False
		
		iStartX, iStartY = tStart
		iTargetX, iTargetY = lTargetList[0]
		startPlot = gc.getMap().plot(iStartX, iStartY)
		
		if not (startPlot.isCity() and startPlot.getOwner() == iPlayer): return False
		
		iRailroad = gc.getInfoTypeForString("ROUTE_RAILROAD")
		lNodes = [(utils.calculateDistance(iStartX, iStartY, iTargetX, iTargetY), iStartX, iStartY)]
		heapq.heapify(lNodes)
		lVisitedNodes = []
		
		while len(lNodes) > 0:
			h, x, y = heapq.heappop(lNodes)
			lVisitedNodes.append((h, x, y))
			
			for i in range(x-1, x+2):
				for j in range(y-1, y+2):
					plot = gc.getMap().plot(i, j)
					if plot.getOwner() == iPlayer and (plot.isCity() or plot.getRouteType() == iRailroad):
						if (i, j) in lTargetList: return True
						tTuple = (utils.calculateDistance(i, j, iTargetX, iTargetY), i, j)
						if not tTuple in lVisitedNodes:
							if not tTuple in lNodes:
								heapq.heappush(lNodes, tTuple)
			
		return False
		
	def getMostPopulousCities(self, iPlayer, iNumCities):
		pCityList = PyPlayer(iPlayer).getCityList()
		cityList = []
		for pCity in pCityList:
			city = pCity.GetCy()
			cityList.append((city.getPopulation(), city))
			
		cityList.sort()
		
		while len(cityList) > iNumCities:
			cityList.remove(cityList[0])
			
		cityList.reverse()
		resultList = []
		for tTuple in cityList:
			resultList.append(tTuple[1])
			
		return resultList
		
	def getApostolicVotePercent(self, iPlayer):
		iTotal = 0
		for iCiv in range(con.iNumPlayers):
			iTotal += gc.getPlayer(iCiv).getVotes(14, 1)
			
		fPercent = gc.getPlayer(iPlayer).getVotes(14, 1) * 100.0 / iTotal
		
		return fPercent
		
	def isRoad(self, iPlayer, lPlotList):
	
		iRoad = gc.getInfoTypeForString("ROUTE_ROAD")
		
		for tPlot in lPlotList:
			x, y = tPlot
			plot = gc.getMap().plot(x, y)
			if plot.getOwner() != iPlayer:
				return False
			if not plot.getRouteType() == iRoad and not plot.isCity():
				return False
				
		return True
		
	def getPopulationByReligion(self, iPlayer, iReligion):
		iTotalPopulation = 0
		cityList = PyPlayer(iPlayer).getCityList()
		
		for pCity in cityList:
			city = pCity.GetCy()
			if city.isHasReligion(iReligion):
				bOtherReligion = False
				for iLoopReligion in range(con.iNumReligions):
					if iLoopReligion != iReligion and city.isHasReligion(iLoopReligion):
						bOtherReligion = True
						break
						
				iCityPopulation = city.getRealPopulation()
				
				if bOtherReligion:
					if gc.getPlayer(iPlayer).getStateReligion() == iReligion:
						iCityPopulation *= 2
						iCityPopulation /= 3
					else:
						iCityPopulation /= 2
						
				iTotalPopulation += iCityPopulation
				
		return iTotalPopulation
		
	def getLargestReligionCiv(self, iCiv, iReligion):
		iBestPopulation = self.getPopulationByReligion(iCiv, iReligion)
		iBestCiv = iCiv
		
		for iLoopCiv in range(con.iNumPlayers):
			if utils.isPastBirth(iLoopCiv) and gc.getPlayer(iLoopCiv).isAlive():
				iTempPopulation = self.getPopulationByReligion(iLoopCiv, iReligion)
				if iTempPopulation > iBestPopulation:
					iBestPopulation = iTempPopulation
					iBestCiv = iLoopCiv
					
		return iBestCiv
		
	def countImprovements(self, iCiv, iImprovement):
		iCount = 0
		for x in range(128):
			for y in range(68):
				plot = gc.getMap().plot(x, y)
				if plot.getOwner() == iCiv and plot.getImprovementType() == iImprovement:
					iCount += 1
		return iCount
		
	def calculateHighestCommerceCity(self):
		lCities = []
		for iPlayer in range(con.iNumPlayers):
			lCities.extend(utils.getCityList(iPlayer))
		pHighestCommerceCity = utils.getHighestEntry(lCities, lambda x: x.getCommerceRate(0) + x.getCommerceRate(1) + x.getCommerceRate(2) + x.getCommerceRate(3))
		return pHighestCommerceCity


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
			aHelp.append(self.getIcon(True) + localText.getText("TXT_KEY_VICTORY_GOAL_ACCOMPLISHED", ()))
			return aHelp
		elif self.getGoal(iPlayer, iGoal) == 0:
			aHelp.append(self.getIcon(False) + localText.getText("TXT_KEY_VICTORY_GOAL_FAILED", ()))
			return aHelp

		if iPlayer == iEgypt:
			if iGoal == 0:
				iCulture = pEgypt.countTotalCulture()
				aHelp.append(self.getIcon(iCulture >= utils.getTurns(500)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(500))))
			elif iGoal == 1:
				bPyramids = (self.getNumBuildings(iEgypt, con.iPyramid) > 0)
				bLibrary = (self.getNumBuildings(iEgypt, con.iGreatLibrary) > 0)
				bLighthouse = (self.getNumBuildings(iEgypt, con.iGreatLighthouse) > 0)
				aHelp.append(self.getIcon(bPyramids) + 'Pyramids ' + self.getIcon(bLibrary) + 'Great Library ' + self.getIcon(bLighthouse) + 'Great Lighthouse')
			elif iGoal == 2:
				iCulture = pEgypt.countTotalCulture()
				aHelp.append(self.getIcon(iCulture >= utils.getTurns(5000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(5000))))

		elif iPlayer == iIndia:
			if iGoal == 0:
				bBuddhistShrine = (self.getNumBuildings(iIndia, con.iBuddhistShrine) > 0)	
				bHinduShrine = (self.getNumBuildings(iIndia, con.iHinduShrine) > 0)
				aHelp.append(self.getIcon(bHinduShrine) + localText.getText("TXT_KEY_VICTORY_HINDU_SHRINE", ()) + ' ' + self.getIcon(bBuddhistShrine) + localText.getText("TXT_KEY_VICTORY_BUDDHIST_SHRINE", ()))
			elif iGoal == 1:
				lTemples = [con.iJewishTemple, con.iChristianTemple, con.iOrthodoxTemple, con.iIslamicTemple, con.iHinduTemple, con.iBuddhistTemple, con.iConfucianTemple, con.iTaoistTemple, con.iZoroastrianTemple]
				iCounter = 0
				for iTemple in lTemples:
					iCounter += self.getNumBuildings(iIndia, iTemple)
				aHelp.append(self.getIcon(iCounter >= 20) + localText.getText("TXT_KEY_VICTORY_TEMPLES_BUILT", (iCounter, 20)))
			elif iGoal == 2:
				totalPop = gc.getGame().getTotalPopulation()
				ourPop = teamIndia.getTotalPopulation()
				if (totalPop > 0):
					popPercent = (ourPop * 100.0) / totalPop
				else:
					popPercent = 0.0
				aHelp.append(self.getIcon(popPercent >= 20.0) + localText.getText("TXT_KEY_VICTORY_PERCENTAGE_WORLD_POPULATION", (str(u"%.2f%%" % popPercent), str(20))))

		elif iPlayer == iChina:
			if iGoal == 0:
				iConfucianCounter = self.getNumBuildings(iChina, con.iConfucianCathedral)
				iTaoistCounter = self.getNumBuildings(iChina, con.iTaoistCathedral)
				aHelp.append(self.getIcon(iConfucianCounter >= 2) + localText.getText("TXT_KEY_VICTORY_NUM_CONFUCIAN_ACADEMIES", (iConfucianCounter, 2)) + ' ' + self.getIcon(iTaoistCounter >= 2) + localText.getText("TXT_KEY_VICTORY_NUM_TAOIST_PAGODAS", (iTaoistCounter, 2)))
			elif iGoal == 1:
				bCompass = (self.getChineseTechs(0) == 1)
				bPaper = (self.getChineseTechs(1) == 1)
				bGunpowder = (self.getChineseTechs(2) == 1)
				bPrintingPress = (self.getChineseTechs(3) == 1)
				aHelp.append(self.getIcon(bCompass) + localText.getText("TXT_KEY_TECH_COMPASS", ()) + ' ' + self.getIcon(bPaper) + localText.getText("TXT_KEY_TECH_PAPER", ()) + ' ' + self.getIcon(bGunpowder) + localText.getText("TXT_KEY_TECH_GUNPOWDER", ()) + ' ' + self.getIcon(bPrintingPress) + localText.getText("TXT_KEY_TECH_PRINTING_PRESS", ()))
			elif iGoal == 2:
				iGoldenAgeTurns = self.getChineseGoldenAgeTurns()
				aHelp.append(self.getIcon(iGoldenAgeTurns >= utils.getTurns(32)) + localText.getText("TXT_KEY_VICTORY_GOLDEN_AGES", (iGoldenAgeTurns / utils.getTurns(8), 4)))

		elif iPlayer == iBabylonia:
			if iGoal == 0:
				bWriting = (self.getBabylonianTechs(0) == 1)
				bCodeOfLaws = (self.getBabylonianTechs(1) == 1)
				bMonarchy = (self.getBabylonianTechs(2) == 1)
				aHelp.append(self.getIcon(bWriting) + localText.getText("TXT_KEY_TECH_WRITING", ()) + ' ' + self.getIcon(bCodeOfLaws) + localText.getText("TXT_KEY_TECH_CODE_OF_LAWS", ()) + ' ' + self.getIcon(bMonarchy) + localText.getText("TXT_KEY_TECH_MONARCHY", ()))
			elif iGoal == 1:
				pBestCity = self.calculateTopCityPopulation(76, 40)
				bBestCity = (pBestCity.getOwner() == iBabylonia and pBestCity.getX() == 76 and pBestCity.getY() == 40)
				aHelp.append(self.getIcon(bBestCity) + localText.getText("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", (pBestCity.getName(),)))
			elif iGoal == 2:
				pBestCity = self.calculateTopCityCulture(76, 40)
				bBestCity = (pBestCity.getOwner() == iBabylonia and pBestCity.getX() == 76 and pBestCity.getY() == 40)
				aHelp.append(self.getIcon(bBestCity) + localText.getText("TXT_KEY_VICTORY_MOST_CULTURED_CITY", (pBestCity.getName(),)))

		elif iPlayer == iGreece:
			if iGoal == 0:
				bLiterature = (self.getGreekTechs(0) == 1)
				bDrama = (self.getGreekTechs(1) == 1)
				bPhilosophy = (self.getGreekTechs(2) == 1)
				aHelp.append(self.getIcon(bLiterature) + localText.getText("TXT_KEY_TECH_LITERATURE", ()) + ' ' + self.getIcon(bDrama) + localText.getText("TXT_KEY_TECH_DRAMA", ()) + ' ' + self.getIcon(bPhilosophy) + localText.getText("TXT_KEY_TECH_PHILOSOPHY", ()))
			elif iGoal == 1:
				bOracle = (self.getNumBuildings(iGreece, con.iOracle) > 0)
				bParthenon = (self.getNumBuildings(iGreece, con.iParthenon) > 0)
				bColossus = (self.getNumBuildings(iGreece, con.iColossus) > 0)
				bArtemis = (self.getNumBuildings(iGreece, con.iArtemis) > 0)
				aHelp.append(self.getIcon(bOracle) + localText.getText("TXT_KEY_BUILDING_ORACLE", ()) + ' ' + self.getIcon(bParthenon) + localText.getText("TXT_KEY_BUILDING_PARTHENON", ()) + ' ' + self.getIcon(bColossus) + localText.getText("TXT_KEY_BUILDING_COLOSSUS", ()) + ' ' + self.getIcon(bArtemis) + localText.getText("TXT_KEY_BUILDING_ARTEMIS", ()))
			elif iGoal == 2:
                        	bEgypt = self.checkOwnedCiv(iGreece, iEgypt)
                        	bPhoenicia = self.checkOwnedCiv(iGreece, iCarthage)
                        	bBabylonia = self.checkOwnedCiv(iGreece, iBabylonia)
				bPersia = self.checkOwnedCiv(iGreece, iPersia)
				aHelp.append(self.getIcon(bEgypt) + localText.getText("TXT_KEY_CIV_EGYPT_SHORT_DESC", ()) + ' ' + self.getIcon(bPhoenicia) + localText.getText("TXT_KEY_CIV_CARTHAGE_SHORT_DESC", ()) + ' ' + self.getIcon(bBabylonia) + localText.getText("TXT_KEY_CIV_BABYLONIA_SHORT_DESC", ()) + ' ' + self.getIcon(bPersia) + localText.getText("TXT_KEY_CIV_PERSIA_SHORT_DESC", ()))

		elif iPlayer == iPersia:
			if not pPersia.isReborn():
				if iGoal == 0:
					totalLand = gc.getMap().getLandPlots()
                	        	persianLand = pPersia.getTotalLand()
                        		if (totalLand > 0):
                        			landPercent = (persianLand * 100.0) / totalLand
                        		else:
                        			landPercent = 0.0
					aHelp.append(self.getIcon(landPercent >= 7.995) + localText.getText("TXT_KEY_VICTORY_PERCENTAGE_WORLD_TERRITORY", (str(u"%.2f%%" % landPercent), str(8))))
				elif iGoal == 1:
                        		iCounter = 0
					for iWonder in range(con.iPyramid, con.iNumBuildings):
						if iWonder not in [con.iMilitaryAcademy, con.iItalianArtStudio]:
							iCounter += self.getNumBuildings(iPersia, iWonder)
					iCounter += self.getNumBuildings(iPersia, con.iFlavianAmphitheatre)
					aHelp.append(self.getIcon(iCounter >= 7) + localText.getText("TXT_KEY_VICTORY_NUM_WONDERS", (iCounter, 7)))
				elif iGoal == 2:
					iCounter = 0
					for iReligion in range(con.iNumReligions):
						iCurrentShrine = con.iShrine + iReligion*4
						iCounter += self.getNumBuildings(iPersia, iCurrentShrine)
					aHelp.append(self.getIcon(iCounter >= 2) + localText.getText("TXT_KEY_VICTORY_NUM_SHRINES", (iCounter, 2)))
			else:
				if iGoal == 0:
					iCount = 0
					for iEurociv in [iGreece, iRome, iByzantium, iVikings, iSpain, iFrance, iEngland, iHolyRome, iGermany, iRussia, iPoland, iPortugal, iNetherlands]:
						if teamPersia.isOpenBorders(iEurociv):
							iCount += 1
					aHelp.append(self.getIcon(iCount >= 6) + localText.getText("TXT_KEY_VICTORY_OPEN_BORDERS", (iCount, 6)))
				elif iGoal == 1:
					bMesopotamia = self.isControlled(iPersia, tSafavidMesopotamiaTL, tSafavidMesopotamiaBR)
					bTransoxania = self.isControlled(iPersia, tTransoxaniaTL, tTransoxaniaBR)
					bNWIndia = self.isControlled(iPersia, tNWIndiaTL, tNWIndiaBR)
					aHelp.append(self.getIcon(bMesopotamia) + localText.getText("TXT_KEY_VICTORY_MESOPOTAMIA", ()) + ' ' + self.getIcon(bTransoxania) + localText.getText("TXT_KEY_VICTORY_TRANSOXANIA", ()) + ' ' + self.getIcon(bNWIndia) + localText.getText("TXT_KEY_VICTORY_NORTHWEST_INDIA", ()))
				elif iGoal == 2:
					pBestCity = self.getMostCulturedCity(iPersia)
					iCulture = pBestCity.getCulture(iPersia)
					aHelp.append(self.getIcon(iCulture >= utils.getTurns(20000)) + localText.getText("TXT_KEY_VICTORY_MOST_CULTURED_CITY_VALUE", (pBestCity.getName(), iCulture, utils.getTurns(20000))))

		elif iPlayer == iCarthage:
			if iGoal == 0:
				capital = pCarthage.getCapitalCity()
				bPalace = (capital.getX(), capital.getY()) == (58, 39)
				bGreatCothon = False
				carthagePlot = gc.getMap().plot(58, 39)
				if carthagePlot.isCity:
					if carthagePlot.getPlotCity().isHasRealBuilding(con.iGreatCothon):
						bGreatCothon = True
				aHelp.append(self.getIcon(bPalace) + localText.getText("TXT_KEY_BUILDING_PALACE", ()) + ' ' + self.getIcon(bGreatCothon) + localText.getText("TXT_KEY_BUILDING_MOAI_STATUES", ()))
			elif iGoal == 1:
				bItaly = self.isControlled(iCarthage, con.tNormalAreasTL[0][iItaly], con.tNormalAreasBR[0][iItaly], [(62, 47), (63, 47), (63, 46)])
				bIberia = self.isControlled(iCarthage, con.tNormalAreasTL[0][iSpain], con.tNormalAreasBR[0][iSpain])
				aHelp.append(self.getIcon(bItaly) + localText.getText("TXT_KEY_VICTORY_ITALY", ()) + ' ' + self.getIcon(bIberia) + localText.getText("TXT_KEY_VICTORY_IBERIA_CARTHAGE", ()))
			elif iGoal == 2:
				iGold = pCarthage.getGold()
				aHelp.append(self.getIcon(iGold >= utils.getTurns()) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iGold, utils.getTurns(5000))))

		elif iPlayer == iRome:
			if iGoal == 0:
				iBarracks = self.getNumBuildings(iRome, con.iBarracks)
				iAqueducts = self.getNumBuildings(iRome, con.iAqueduct)
				iAmphitheatres = self.getNumBuildings(iRome, con.iColosseum)
				iForums = self.getNumBuildings(iRome, con.iRomanForum)
				aHelp.append(self.getIcon(iBarracks >= 6) + localText.getText("TXT_KEY_VICTORY_NUM_BARRACKS", (iBarracks, 6)) + ' ' + self.getIcon(iAqueducts >= 5) + localText.getText("TXT_KEY_VICTORY_NUM_AQUEDUCTS", (iAqueducts, 5)) + ' ' + self.getIcon(iAmphitheatres >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_AMPHITHEATRES", (iAmphitheatres, 4)) + ' ' + self.getIcon(iForums >= 3) + localText.getText("TXT_KEY_VICTORY_NUM_FORUMS", (iForums, 3)))
			elif iGoal == 1:                              
				iCitiesSpain = self.getNumCitiesInArea(iRome, tNormalAreasTL[utils.getReborn(iSpain)][iSpain], tNormalAreasBR[utils.getReborn(iSpain)][iSpain])
				iCitiesFrance = self.getNumCitiesInArea(iRome, tFranceTL, tNormalAreasBR[utils.getReborn(iFrance)][iFrance])
				iCitiesEngland = self.getNumCitiesInArea(iRome, tCoreAreasTL[utils.getReborn(iEngland)][iEngland], tCoreAreasBR[utils.getReborn(iEngland)][iEngland])
				iCitiesCarthage = self.getNumCitiesInArea(iRome, tCarthageTL, tCarthageBR)
				iCitiesByzantium = self.getNumCitiesInArea(iRome, tCoreAreasTL[0][iByzantium], tCoreAreasBR[0][iByzantium])
				iCitiesEgypt = self.getNumCitiesInArea(iRome, tCoreAreasTL[0][iEgypt], tCoreAreasBR[0][iEgypt])
				aHelp.append(self.getIcon(iCitiesSpain >= 2) + localText.getText("TXT_KEY_VICTORY_ROME_CONTROL_SPAIN", (iCitiesSpain, 2)) + ' ' + self.getIcon(iCitiesFrance >= 3) + localText.getText("TXT_KEY_VICTORY_ROME_CONTROL_FRANCE", (iCitiesFrance, 3)) + ' ' + self.getIcon(iCitiesEngland >= 1) + localText.getText("TXT_KEY_VICTORY_ROME_CONTROL_ENGLAND", (iCitiesEngland, 1)))
				aHelp.append(self.getIcon(iCitiesCarthage >= 2) + localText.getText("TXT_KEY_VICTORY_ROME_CONTROL_CARTHAGE", (iCitiesCarthage, 2)) + ' ' + self.getIcon(iCitiesByzantium >= 4) + localText.getText("TXT_KEY_VICTORY_ROME_CONTROL_BYZANTIUM", (iCitiesByzantium, 4)) + ' ' + self.getIcon(iCitiesEgypt >= 2) + localText.getText("TXT_KEY_VICTORY_ROME_CONTROL_EGYPT", (iCitiesEgypt, 2)))	
			elif iGoal == 2:
				bTheology = (self.getRomanTechs(0) == 1)
				bMachinery = (self.getRomanTechs(1) == 1)
				bCivilService = (self.getRomanTechs(2) == 1)
				aHelp.append(self.getIcon(bTheology) + localText.getText("TXT_KEY_TECH_THEOLOGY", ()) + ' ' + self.getIcon(bMachinery) + localText.getText("TXT_KEY_TECH_MACHINERY", ()) + ' ' + self.getIcon(bCivilService) + localText.getText("TXT_KEY_TECH_CIVIL_SERVICE", ()))
				
		elif iPlayer == iJapan:
			if iGoal == 0:
				iCulture = pJapan.countTotalCulture()
				#aHelp.append(self.getIcon(iTechsStolen >= 5) + 'Techs stolen: '+str(iTechsStolen)+'/5')
				aHelp.append(self.getIcon(iCulture >= utils.getTurns(18000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(18000))))
			elif iGoal == 1:
				bKorea = self.isControlledOrVassalized(iJapan, tKoreaTL, tKoreaBR)
				bManchuria = self.isControlledOrVassalized(iJapan, tManchuriaTL, tManchuriaBR)
				bChina = self.isControlledOrVassalized(iJapan, tChinaTL, tChinaBR)
				bIndochina = self.isControlledOrVassalized(iJapan, tIndochinaTL, tIndochinaBR)
				bIndonesia = self.isControlledOrVassalized(iJapan, tIndonesiaTL, tIndonesiaBR)
				bPhilippines = self.isControlledOrVassalized(iJapan, tPhilippinesTL, tPhilippinesBR)
				aHelp.append(self.getIcon(bKorea) + localText.getText("TXT_KEY_CIV_KOREA_SHORT_DESC", ()) + ' ' + self.getIcon(bManchuria) + localText.getText("TXT_KEY_VICTORY_MANCHURIA", ()) + ' ' + self.getIcon(bChina) + localText.getText("TXT_KEY_CIV_CHINA_SHORT_DESC", ()))
				aHelp.append(self.getIcon(bIndochina) + localText.getText("TXT_KEY_VICTORY_INDOCHINA", ()) + ' ' + self.getIcon(bIndonesia) + localText.getText("TXT_KEY_CIV_INDONESIA_SHORT_DESC", ()) + ' ' + self.getIcon(bPhilippines) + localText.getText("TXT_KEY_VICTORY_PHILIPPINES", ()))
		
		elif iPlayer == iTamils:
			if iGoal == 0:
				iGold = pTamils.getGold()
				iCulture = pTamils.countTotalCulture()
				aHelp.append(self.getIcon(iGold >= utils.getTurns(3000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iGold, utils.getTurns(3000))))
				aHelp.append(self.getIcon(iCulture >= utils.getTurns(2000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(2000))))
			elif iGoal == 1:
				bDeccan = self.isControlledOrVassalized(iTamils, tDeccanTL, tDeccanBR)
				bSrivijaya = self.isControlledOrVassalized(iTamils, tSrivijayaTL, tSrivijayaBR)
				aHelp.append(self.getIcon(bDeccan) + localText.getText("TXT_KEY_VICTORY_DECCAN", ()) + ' ' + self.getIcon(bSrivijaya) + localText.getText("TXT_KEY_VICTORY_SRIVIJAYA", ()))
			elif iGoal == 2:
				iGold = self.getTamilTradeGold()
				aHelp.append(self.getIcon(iGold >= utils.getTurns(4000)) + localText.getText("TXT_KEY_VICTORY_TRADE_GOLD", (iGold, utils.getTurns(4000))))
		
                elif iPlayer == iEthiopia:
			if iGoal == 1:
				iNumIncense = pEthiopia.getNumAvailableBonuses(con.iIncense)
				aHelp.append(self.getIcon(iNumIncense >= 3) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_INCENSE_RESOURCES", (iNumIncense, 3)))
			elif iGoal == 2:
				bAfrica = True
                                for iEuroCiv in range(iNumPlayers):
                                	if (iEuroCiv in con.lCivGroups[0]):
                                 		if (self.checkNotOwnedArea(iEuroCiv, tSomaliaTL, tSomaliaBR) == False):
                                 			bAfrica = False
                                 		if (self.checkNotOwnedArea(iEuroCiv, tSubeqAfricaTL, tSubeqAfricaBR) == False):
                                 			bAfrica = False
                                 		if (bAfrica == False):
                                 			break
				aHelp.append(self.getIcon(bAfrica) + localText.getText("TXT_KEY_VICTORY_NO_AFRICAN_COLONIES_CURRENT", ()))
				aHelp.append(self.getIcon(self.getEthiopianControl() == 1) + localText.getText("TXT_KEY_VICTORY_NO_AFRICAN_COLONIES_1500", ()))
				aHelp.append(self.getIcon(False) + localText.getText("TXT_KEY_VICTORY_NO_AFRICAN_COLONIES_1910", ()))

		elif iPlayer == iKorea:
			if iGoal == 0:
				bConfucianCathedral = (self.getNumBuildings(iKorea, con.iConfucianCathedral) > 0)
				bBuddhistCathedral = (self.getNumBuildings(iKorea, con.iBuddhistCathedral) > 0)
				aHelp.append(self.getIcon(bBuddhistCathedral) + localText.getText("TXT_KEY_BUILDING_BUDDHIST_CATHEDRAL", ()) + ' ' + self.getIcon(bConfucianCathedral) + localText.getText("TXT_KEY_BUILDING_CONFUCIAN_CATHEDRAL", ()))
			#elif iGoal == 1:
			#	bPrintingPress = (self.getKoreanTechs(0) == 1)
			#	bGunpowder = (self.getKoreanTechs(1) == 1)
			#	aHelp.append(self.getIcon(bPrintingPress) + 'Printing Press ' + self.getIcon(bGunpowder) + 'Gunpowder')
			elif iGoal == 2:
				iNumSinks = self.getNumKoreanSinks()
				aHelp.append(self.getIcon(iNumSinks >= 20) + localText.getText("TXT_KEY_VICTORY_ENEMY_SHIPS_SUNK", (iNumSinks, 20)))

		# Maya goals have no stages
		elif iPlayer == iMaya:
			if pMaya.isReborn():
				if iGoal == 0:
					bPeru = True
					bGranColombia = True
					bGuayanas = True
					bCaribbean = True
					for iEuroCiv in con.lCivGroups[0]:
						if bPeru and not self.checkNotOwnedArea(iEuroCiv, tPeruTL, tPeruBR): bPeru = False
						if bGranColombia and not self.checkNotOwnedArea(iEuroCiv, tGranColombiaTL, tGranColombiaBR): bGranColombia = False
						if bGuayanas and not self.checkNotOwnedArea(iEuroCiv, tGuayanasTL, tGuayanasBR): bGuayanas = False
						if bCaribbean and not self.checkNotOwnedArea(iEuroCiv, tCaribbeanTL, tCaribbeanBR): bCaribbean = False
					aHelp.append(self.getIcon(bPeru) + localText.getText("TXT_KEY_VICTORY_NO_COLONIES_PERU", ()) + ' ' + self.getIcon(bGranColombia) + localText.getText("TXT_KEY_VICTORY_NO_COLONIES_GRAN_COLOMBIA", ()))
					aHelp.append(self.getIcon(bGuayanas) + localText.getText("TXT_KEY_VICTORY_NO_COLONIES_GUAYANAS", ()) + ' ' + self.getIcon(bCaribbean) + localText.getText("TXT_KEY_VICTORY_NO_COLONIES_CARIBBEAN", ()))
				elif iGoal == 1:
					bSouthAmerica = self.isControlled(iMaya, tSAmericaTL, tSAmericaBR, tSouthAmericaExceptions)
					aHelp.append(self.getIcon(bSouthAmerica) + localText.getText("TXT_KEY_VICTORY_CONTROL_SOUTH_AMERICA", ()))
				elif iGoal == 2:
					iTradeGold = self.getColombianTradeGold()
					aHelp.append(self.getIcon(iTradeGold >= utils.getTurns(5000)) + localText.getText("TXT_KEY_VICTORY_TRADE_GOLD_RESOURCES", (iTradeGold, utils.getTurns(5000))))
					
		elif iPlayer == iByzantium:
			if iGoal == 0:
				iGold = pByzantium.getGold()
				aHelp.append(self.getIcon(iGold >= utils.getTurns(5000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iGold, utils.getTurns(5000))))
			elif iGoal == 1:           	
				pBestPopCity = self.calculateTopCityPopulation(68, 45)
				bBestPopCity = (pBestPopCity.getOwner() == iByzantium and pBestPopCity.getX() == 68 and pBestPopCity.getY() == 45)
				pBestCultureCity = self.calculateTopCityCulture(68, 45)
				bBestCultureCity = (pBestCultureCity.getOwner() == iByzantium and pBestCultureCity.getX() == 68 and pBestCultureCity.getY() == 45)
				aHelp.append(self.getIcon(bBestPopCity) + localText.getText("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", (pBestPopCity.getName(),)) + ' ' + self.getIcon(bBestCultureCity) + localText.getText("TXT_KEY_VICTORY_MOST_CULTURED_CITY", (pBestCultureCity.getName(),)))
			elif iGoal == 2:
				iBalkans = self.getNumCitiesInArea(iByzantium, tBalkansTL, tBalkansBR)
				iNorthAfrica = self.getNumCitiesInArea(iByzantium, tNorthAfricaTL, tNorthAfricaBR)
				iNearEast = self.getNumCitiesInArea(iByzantium, tNearEastTL, tNearEastBR)
				aHelp.append(self.getIcon(iBalkans >= 3) + localText.getText("TXT_KEY_VICTORY_BALKANS", (iBalkans, 3)) + ' ' + self.getIcon(iNorthAfrica >= 3) + localText.getText("TXT_KEY_VICTORY_NORTH_AFRICA", (iNorthAfrica, 3)) + ' ' + self.getIcon(iNearEast >= 3) + localText.getText("TXT_KEY_VICTORY_NEAR_EAST", (iNearEast, 3)))

		elif iPlayer == iVikings:
			if iGoal == 0:
				bEuropeanCore = False
				lEuroCivs = [iRome, iByzantium, iSpain, iFrance, iEngland, iHolyRome, iRussia]
				for iEuroCiv in lEuroCivs:
					if self.checkOwnedCiv(iVikings, iEuroCiv):
						bEuropeanCore = True
						break
				aHelp.append(self.getIcon(bEuropeanCore) + localText.getText("TXT_KEY_VICTORY_EUROPEAN_CORE", ()))
			elif iGoal == 2:
				iGold = self.getVikingGold()
				aHelp.append(self.getIcon(iGold >= utils.getTurns(3000)) + localText.getText("TXT_KEY_VICTORY_ACQUIRED_GOLD", (iGold, utils.getTurns(3000))))
			

		elif iPlayer == iArabia:
			if iGoal == 0:
				iMostAdvancedCiv = self.getMostAdvancedCiv(iArabia)
				aHelp.append(self.getIcon(iMostAdvancedCiv == iArabia) + localText.getText("TXT_KEY_VICTORY_MOST_ADVANCED_CIV", (str(gc.getPlayer(iMostAdvancedCiv).getCivilizationShortDescriptionKey()),)))
			elif iGoal == 1:
                                bEgypt = self.isControlledOrVassalized(iArabia, con.tCoreAreasTL[0][iEgypt], con.tCoreAreasBR[0][iEgypt])
                                bMaghreb = self.isControlledOrVassalized(iArabia, tCarthageTL, tCarthageBR)
				bMesopotamia = self.isControlledOrVassalized(iArabia, con.tCoreAreasTL[0][iBabylonia], con.tCoreAreasBR[0][iBabylonia])
				bPersia = self.isControlledOrVassalized(iArabia, con.tCoreAreasTL[0][iPersia], con.tCoreAreasBR[0][iPersia])
				bSpain = self.isControlledOrVassalized(iArabia, con.tNormalAreasTL[0][iSpain], con.tNormalAreasBR[0][iSpain])
				aHelp.append(self.getIcon(bEgypt) + localText.getText("TXT_KEY_CIV_EGYPT_SHORT_DESC", ()) + ' ' + self.getIcon(bMaghreb) + localText.getText("TXT_KEY_VICTORY_MAGHREB", ()) + ' ' + self.getIcon(bSpain) + localText.getText("TXT_KEY_CIV_SPAIN_SHORT_DESC", ()))
				aHelp.append(self.getIcon(bMesopotamia) + localText.getText("TXT_KEY_VICTORY_MESOPOTAMIA", ()) + ' ' + self.getIcon(bPersia) + localText.getText("TXT_KEY_CIV_PERSIA_SHORT_DESC", ()))
			elif iGoal == 2:
                                fReligionPercent = gc.getGame().calculateReligionPercent(con.iIslam)
				aHelp.append(self.getIcon(fReligionPercent >= 40.0) + localText.getText("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", (gc.getReligionInfo(con.iIslam).getTextKey(), str(u"%.2f%%" % fReligionPercent), str(40))))

		elif iPlayer == iTibet:
			if iGoal == 0:
				iNumCities = pTibet.getNumCities()
				aHelp.append(self.getIcon(iNumCities >= 5) + localText.getText("TXT_KEY_VICTORY_CITIES_ACQUIRED", (iNumCities, 5)))
			elif iGoal == 1:
                                fReligionPercent = gc.getGame().calculateReligionPercent(con.iBuddhism)
				aHelp.append(self.getIcon(fReligionPercent >= 30.0) + localText.getText("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", (gc.getReligionInfo(con.iBuddhism).getTextKey(), str(u"%.2f%%" % fReligionPercent), str(30))))
			elif iGoal == 2:
				lhasaPlot = gc.getMap().plot(96, 43)
				iCounter = 0
				if lhasaPlot.isCity():
					lhasa = lhasaPlot.getPlotCity()
					if lhasa.getFreeSpecialistCount(iGreatProphet) > 0:
						iCounter = lhasa.getFreeSpecialistCount(iGreatProphet)
				aHelp.append(self.getIcon(iCounter >= 5) + localText.getText("TXT_KEY_VICTORY_GREAT_PROPHETS_SETTLED", ("Lhasa", iCounter, 5)))
				
		elif iPlayer == iKhmer:
			if iGoal == 0:
				iBuddhism = self.getNumBuildings(iKhmer, con.iBuddhistMonastery)
				iHinduism = self.getNumBuildings(iKhmer, con.iHinduMonastery)
				bAngkorWat = (self.getWondersBuilt(iKhmer) >= 1)
				aHelp.append(self.getIcon(iBuddhism >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_BUDDHIST_MONASTERIES", (iBuddhism, 4)) + ' ' + self.getIcon(iHinduism >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_HINDU_MONASTERIES", (iHinduism, 4)) + ' ' + self.getIcon(bAngkorWat) + localText.getText("TXT_KEY_BUILDING_ANGKOR_WAT", ()))
			elif iGoal == 1:
				apCityList = PyPlayer(iKhmer).getCityList()
                                iTotalPopulation = 0
                                for pCity in apCityList:			
                                	iTotalPopulation += pCity.getPopulation()
				if len(apCityList) > 0:
                                	fPopPerCity = iTotalPopulation * 1.00 / len(apCityList)
				else:
					fPopPerCity = 0
				aHelp.append(self.getIcon(fPopPerCity >= 12.0) + localText.getText("TXT_KEY_VICTORY_AVERAGE_CITY_POPULATION", (str(u"%.2f" % fPopPerCity), str(12))))
			elif iGoal == 2:
				iCulture = pKhmer.countTotalCulture()
				aHelp.append(self.getIcon(iCulture >= utils.getTurns(8000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(8000))))

		elif iPlayer == iIndonesia:
			if iGoal == 0:
				iHighestCiv = self.getHighestPopulationCiv(iIndonesia)
				bHighest = (iHighestCiv == iIndonesia)
				aHelp.append(self.getIcon(bHighest) + localText.getText("TXT_KEY_VICTORY_HIGHEST_POPULATION_CIV", ()) + CyTranslator().getText(str(gc.getPlayer(iHighestCiv).getCivilizationShortDescriptionKey()),()))
			elif iGoal == 1:
				lHappinessBonuses = [con.iDye, con.iFur, con.iGems, con.iGold, con.iIncense, con.iIvory, con.iSilk, con.iSilver, con.iSpices, con.iSugar, con.iWine, con.iWhales, con.iCotton, con.iCoffee, con.iTea, con.iTobacco]
                                iCounter = 0
				for iBonus in lHappinessBonuses:
					if pIndonesia.getNumAvailableBonuses(iBonus) > 0:
						iCounter += 1
				aHelp.append(self.getIcon(iCounter >= 10) + localText.getText("TXT_KEY_VICTORY_NUM_HAPPINESS_RESOURCES", (iCounter, 10)))
			elif iGoal == 2:
				totalPop = gc.getGame().getTotalPopulation()
				ourPop = teamIndonesia.getTotalPopulation()
				if (totalPop > 0):
					popPercent = (ourPop * 100.0) / totalPop
				else:
					popPercent = 0.0
				aHelp.append(self.getIcon(popPercent >= 9.0) + localText.getText("TXT_KEY_VICTORY_PERCENTAGE_WORLD_POPULATION", (str(u"%.2f%%" % popPercent), str(9))))

		elif iPlayer == iMoors:
			if iGoal == 0:          	
				pBestPopCity = self.calculateTopCityPopulation(51, 41)
				bBestPopCity = (pBestPopCity.getOwner() == iMoors and pBestPopCity.getX() == 51 and pBestPopCity.getY() == 41)
				pBestCommerceCity = self.calculateTopCityCommerce(51, 41)
				bBestCommerceCity = (pBestCommerceCity.getOwner() == iMoors and pBestCommerceCity.getX() == 51 and pBestCommerceCity.getY() == 41)
				aHelp.append(self.getIcon(bBestPopCity) + localText.getText("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", (pBestPopCity.getName(),)) + ' ' + self.getIcon(bBestCommerceCity) + localText.getText("TXT_KEY_VICTORY_BEST_COMMERCE_CITY", (pBestCommerceCity.getName(),)))
			elif iGoal == 1:
				iIberia = self.getNumCitiesInArea(iMoors, tIberiaTL, tIberiaBR)
				iMaghreb = self.getNumCitiesInArea(iMoors, tMaghrebTL, tMaghrebBR)
				iWestAfrica = self.getNumCitiesInArea(iMoors, tWestAfricaTL, tWestAfricaBR)
				aHelp.append(self.getIcon(iIberia >= 3) + localText.getText("TXT_KEY_VICTORY_IBERIA", (iIberia, 3)) + ' ' + self.getIcon(iMaghreb >= 3) + localText.getText("TXT_KEY_VICTORY_MAGHREB_MOORS", (iMaghreb, 3)) + ' ' + self.getIcon(iWestAfrica >= 3) + localText.getText("TXT_KEY_VICTORY_WEST_AFRICA", (iWestAfrica, 3)))
			elif iGoal == 2:
				plot = gc.getMap().plot(51, 41)
				iCounter = 0
				if plot.isCity:
					capital = plot.getPlotCity()
					for iSpecialist in range(gc.getNumSpecialistInfos()):
						if iSpecialist in [7, 9, 11]: #prophet, scientist, engineer
							iCounter += capital.getFreeSpecialistCount(iSpecialist)
				aHelp.append(self.getIcon(iCounter >= 4) + localText.getText("TXT_KEY_VICTORY_GREAT_PEOPLE_IN_CITY_MOORS", ("Cordoba", iCounter, 4)))
			
		elif iPlayer == iSpain:
			if iGoal == 1:
				iGold = pSpain.getNumAvailableBonuses(con.iGold) - pSpain.getBonusImport(con.iGold)
				iSilver = pSpain.getNumAvailableBonuses(con.iSilver) - pSpain.getBonusImport(con.iSilver)
				
				for iCiv in range(iNumPlayers):
					if iCiv != iSpain:
						if gc.getPlayer(iCiv).isAlive():
							if gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iSpain):
								iGold += gc.getPlayer(iCiv).getNumAvailableBonuses(con.iGold) - gc.getPlayer(iCiv).getBonusImport(con.iGold)
								iSilver += gc.getPlayer(iCiv).getNumAvailableBonuses(con.iSilver) - gc.getPlayer(iCiv).getBonusImport(con.iSilver)
			
				aHelp.append(self.getIcon(iGold + iSilver >= 10) + localText.getText("TXT_KEY_VICTORY_GOLD_SILVER_RESOURCES", (iGold + iSilver, 10)))
			elif iGoal == 2:
				fReligionPercent = gc.getGame().calculateReligionPercent(con.iChristianity)
					
				bNoProtestants = True
				for iCiv in range(iNumPlayers):
					if gc.getPlayer(iCiv).getStateReligion() == con.iJudaism:
						cityList = PyPlayer(iCiv).getCityList()
						for city in cityList:
							pCity = city.GetCy()
							if utils.isPlotInArea((pCity.getX(), pCity.getY()), con.tEuropeTL, con.tEuropeBR) or utils.isPlotInArea((pCity.getX(), pCity.getY()), con.tEasternEuropeTL, con.tEasternEuropeBR):
								bNoProtestants = True
								break
								break
								
				aHelp.append(self.getIcon(fReligionPercent >= 40.0) + localText.getText("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", (gc.getReligionInfo(con.iChristianity).getTextKey(), str(u"%.2f%%" % fReligionPercent), str(40))) + ' ' + self.getIcon(bNoProtestants) + localText.getText("TXT_KEY_VICTORY_NO_PROTESTANTS", ()))
				
		elif iPlayer == iFrance:
			if iGoal == 0:
				pParis = gc.getMap().plot(55, 50)
				if pParis.isCity():
					iCulture = pParis.getPlotCity().getCulture(iFrance)
				else:
					iCulture = 0
				aHelp.append(self.getIcon(iCulture >= utils.getTurns(25000)) + localText.getText("TXT_KEY_VICTORY_CITY_CULTURE", ("Paris", iCulture, utils.getTurns(25000))))
			elif iGoal == 1:
				iEurope, iTotalEurope = self.countControlledTiles(iFrance, con.tEuropeTL, con.tEuropeBR, True)
				iEasternEurope, iTotalEasternEurope = self.countControlledTiles(iFrance, con.tEasternEuropeTL, con.tEasternEuropeBR, True)
				iNorthAmerica, iTotalNorthAmerica = self.countControlledTiles(iFrance, con.tNorthAmericaTL, con.tNorthAmericaBR, True)
				fEurope = (iEurope + iEasternEurope) * 100.0 / (iTotalEurope + iTotalEasternEurope)
				fNorthAmerica = iNorthAmerica * 100.0 / iTotalNorthAmerica
				aHelp.append(self.getIcon(fEurope >= 40.0) + localText.getText("TXT_KEY_VICTORY_EUROPEAN_TERRITORY", (str(u"%.2f%%" % fEurope), str(40))) + ' ' + self.getIcon(fNorthAmerica >= 40.0) + localText.getText("TXT_KEY_VICTORY_NORTH_AMERICAN_TERRITORY", (str(u"%.2f%%" % fNorthAmerica), str(40))))
			elif iGoal == 2:	# not entirely correct, this counts conquered ones as well
				bNotreDame = (self.getNumBuildings(iFrance, con.iNotreDame) > 0)
				bVersailles = (self.getNumBuildings(iFrance, con.iVersailles) > 0)
				bStatueOfLiberty = (self.getNumBuildings(iFrance, con.iStatueOfLiberty) > 0)
				bEiffelTower = (self.getNumBuildings(iFrance, con.iEiffelTower) > 0)
				aHelp.append(self.getIcon(bNotreDame) + localText.getText("TXT_KEY_BUILDING_NOTRE_DAME", ()) + ' ' + self.getIcon(bVersailles) + localText.getText("TXT_KEY_BUILDING_VERSAILLES", ()) + ' ' + self.getIcon(bStatueOfLiberty) + localText.getText("TXT_KEY_BUILDING_STATUE_OF_LIBERTY", ()) + ' ' + self.getIcon(bEiffelTower) + localText.getText("TXT_KEY_BUILDING_EIFFEL_TOWER", ()))

		elif iPlayer == iEngland:
			if iGoal == 0:
				iNAmerica = self.getNumCitiesInArea(iEngland, con.tNorthAmericaTL, con.tNorthAmericaBR)
				iSCAmerica = self.getNumCitiesInArea(iEngland, con.tSouthCentralAmericaTL, con.tSouthCentralAmericaBR)
				iAfrica = self.getNumCitiesInArea(iEngland, tAfricaTL, tAfricaBR)
				iAsia = self.getNumCitiesInArea(iEngland, tAsiaTL, tAsiaBR)
				iOceania = self.getNumCitiesInArea(iEngland, tOceaniaTL, tOceaniaBR)
				aHelp.append(self.getIcon(iNAmerica >= 5) + localText.getText("TXT_KEY_VICTORY_ENGLAND_CONTROL_NORTH_AMERICA", (iNAmerica, 5)) + ' ' + self.getIcon(iAsia >= 5) + localText.getText("TXT_KEY_VICTORY_ENGLAND_CONTROL_ASIA", (iAsia, 5)) + ' ' + self.getIcon(iAfrica >= 4) + localText.getText("TXT_KEY_VICTORY_ENGLAND_CONTROL_AFRICA", (iAfrica, 4)))
				aHelp.append(self.getIcon(iSCAmerica >= 3) + localText.getText("TXT_KEY_VICTORY_ENGLAND_CONTROL_SOUTH_AMERICA", (iSCAmerica, 3)))
				aHelp.append(self.getIcon(iOceania >= 3) + localText.getText("TXT_KEY_VICTORY_ENGLAND_CONTROL_OCEANIA", (iOceania, 3)))
			elif iGoal == 1:
				iCShipOfTheLine = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_SHIP_OF_THE_LINE')
				iCFrigate = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_FRIGATE')
				iEnglishNavy = gc.getPlayer(iEngland).getUnitClassCount(iCFrigate) + gc.getPlayer(iEngland).getUnitClassCount(iCShipOfTheLine)
				iEnglishSinks = self.getNumSinks()
				aHelp.append(self.getIcon(iEnglishNavy >= 25) + localText.getText("TXT_KEY_VICTORY_NAVY_SIZE", (iEnglishNavy, 25)) + ' ' + self.getIcon(iEnglishSinks >= 50) + localText.getText("TXT_KEY_VICTORY_ENEMY_SHIPS_SUNK", (iEnglishSinks, 50)))
			elif iGoal == 2:
				bIndustrial = (self.getEnglishEras(0) == 1)
				bModern = (self.getEnglishEras(1) == 1)
				aHelp.append(self.getIcon(bIndustrial) + localText.getText("TXT_KEY_VICTORY_FIRST_ENTER_INDUSTRIAL", ()) + ' ' + self.getIcon(bModern) + localText.getText("TXT_KEY_VICTORY_FIRST_ENTER_MODERN", ()))

		elif iPlayer == iHolyRome:
			if iGoal == 0:
				bApostolicPalace = self.getNumBuildings(iHolyRome, con.iApostolicPalace) > 0
				bHolySepulchre = self.getNumBuildings(iHolyRome, con.iChristianShrine) > 0
				aHelp.append(self.getIcon(bApostolicPalace) + localText.getText("TXT_KEY_BUILDING_APOSTOLIC_PALACE", ()) + ' ' + self.getIcon(bHolySepulchre) + localText.getText("TXT_KEY_BUILDING_CHRISTIAN_SHRINE", ()))
			elif iGoal == 2:
				iGreatArtists = 0
				pVienna = gc.getMap().plot(con.tVienna[0], con.tVienna[1])
				if pVienna.isCity():
					iGreatArtists = pVienna.getPlotCity().getFreeSpecialistCount(con.iGreatArtist)
				aHelp.append(self.getIcon(iGreatArtists >= 3) + localText.getText("TXT_KEY_VICTORY_GREAT_ARTISTS_SETTLED", ('Vienna', iGreatArtists, 3)))
				
		elif iPlayer == iGermany:
			if iGoal == 0:
				x, y = con.tCapitals[utils.getReborn(iGermany)][iGermany]
				plot = gc.getMap().plot(x, y)
				iCounter = 0
				if plot.isCity():
					capital = plot.getPlotCity()
					for iSpecialist in range(gc.getNumSpecialistInfos()):
						if iSpecialist >= 7: # great priest
							iCounter += capital.getFreeSpecialistCount(iSpecialist)
				aHelp.append(self.getIcon(iCounter >= 7) + localText.getText("TXT_KEY_VICTORY_GREAT_PEOPLE_IN_CITY", ("Berlin", iCounter, 7)))
			elif iGoal == 1:
                               	bFrance = self.checkOwnedCiv(iGermany, iFrance)
                                bRome = self.checkOwnedCiv(iGermany, iItaly)
                                bRussia = self.checkOwnedCiv(iGermany, iRussia)
                                bEngland = self.checkOwnedCiv(iGermany, iEngland)                                        
                                bScandinavia = self.checkOwnedCiv(iGermany, iVikings)
				aHelp.append(self.getIcon(bRome) + localText.getText("TXT_KEY_CIV_ITALY_SHORT_DESC", ()) + ' ' + self.getIcon(bFrance) + localText.getText("TXT_KEY_CIV_FRANCE_SHORT_DESC", ()) + ' ' + self.getIcon(bScandinavia) + localText.getText("TXT_KEY_VICTORY_SCANDINAVIA", ()))
				aHelp.append(self.getIcon(bEngland) + localText.getText("TXT_KEY_CIV_ENGLAND_SHORT_DESC", ()) + ' ' + self.getIcon(bRussia) + localText.getText("TXT_KEY_CIV_RUSSIA_SHORT_DESC", ()))

		elif iPlayer == iRussia:
			if iGoal == 0:
				bSiberia = self.checkFoundedArea(iRussia, tSiberiaTL, tSiberiaBR, 7)
				aHelp.append(self.getIcon(bSiberia) + localText.getText("TXT_KEY_VICTORY_RUSSIA_CONTROL_SIBERIA", ()))
			elif iGoal == 1:
				bSiberianRailway = (self.getRussianProjects(0) == 1)
				bManhattanProject = (self.getRussianProjects(1) == 1)
				bApolloProgram = (self.getRussianProjects(2) == 1)
				aHelp.append(self.getIcon(bSiberianRailway) + localText.getText("TXT_KEY_VICTORY_TRANSSIBERIAN_RAILWAY", ()) + ' ' + self.getIcon(bManhattanProject) + localText.getText("TXT_KEY_PROJECT_MANHATTAN_PROJECT", ()) + ' ' + self.getIcon(bApolloProgram) + localText.getText("TXT_KEY_PROJECT_APOLLO_PROGRAM", ()))
			elif iGoal == 2:
				iCount = 0
				for iCiv in range(con.iNumPlayers):
					pPlayer = gc.getPlayer(iCiv)
					if iCiv != iRussia and pPlayer.AI_getAttitude(iRussia) == AttitudeTypes.ATTITUDE_FRIENDLY and (pPlayer.getCivics(1) == con.iSupremeCouncil or pPlayer.getCivics(3) == con.iStateProperty):
						iCount += 1
				aHelp.append(self.getIcon(iCount >= 5) + localText.getText("TXT_KEY_VICTORY_COMMUNIST_BROTHERS", (iCount, 5)))

		elif iPlayer == iNetherlands:
			if iGoal == 0:
				iGMerchant = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), "SPECIALIST_GREAT_MERCHANT")
				pPlot = gc.getMap().plot(57, 53)
				if pPlot.isCity() and pPlot.getPlotCity().getOwner() == iNetherlands:
					iMerchants = pPlot.getPlotCity().getFreeSpecialistCount(iGMerchant)
				else:
					iMerchants = 0
				aHelp.append(self.getIcon(iMerchants >= 3) + localText.getText("TXT_KEY_VICTORY_GREAT_MERCHANTS_IN_CITY", ("Amsterdam", iMerchants, 3)))
			elif iGoal == 1:
				iColonies = self.getDutchColonies()
				aHelp.append(self.getIcon(iColonies >= 4) + localText.getText("TXT_KEY_VICTORY_EUROPEAN_COLONIES_CONQUERED", (iColonies, 4)))
			elif iGoal == 2:
				iSpices = pNetherlands.getNumAvailableBonuses(con.iSpices)
				aHelp.append(self.getIcon(iSpices >= 7) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_SPICE_RESOURCES", (iSpices, 7)))

		elif iPlayer == iMali:
			if iGoal == 1:
				bSankore = False
				iProphets = 0
				#iGreatProphet = gc.getInfoTypeForString("SPECIALIST_GREAT_PRIEST")
				for pCity in PyPlayer(iMali).getCityList():
					city = pCity.GetCy()
					if city.isHasRealBuilding(con.iSankore):
						bSankore = True
						iProphets = city.getFreeSpecialistCount(iGreatProphet)
						break
				aHelp.append(self.getIcon(bSankore) + localText.getText("TXT_KEY_BUILDING_SANKORE", ()) + ' ' + self.getIcon(iProphets >= 1) + localText.getText("TXT_KEY_VICTORY_SANKORE_PROPHETS", (iProphets, 1)))
			elif iGoal == 2:
				iGold = pMali.getGold()
				if self.getMaliGold():
					aHelp.append(self.getIcon(True) + localText.getText("TXT_KEY_VICTORY_GOAL_ACCOMPLISHED", ()) + ' ' + self.getIcon(iGold >= utils.getTurns(15000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iGold, utils.getTurns(15000))))
				else:
					aHelp.append(self.getIcon(iGold >= utils.getTurns(5000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iGold, utils.getTurns(5000))) + ' ' + self.getIcon(iGold >= utils.getTurns(15000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iGold, utils.getTurns(15000))))
			#if iGoal == 0:
			#	iMostGoldCiv = self.getMostGoldCiv(iMali)
			#	aHelp.append(self.getIcon(iMostGoldCiv == iMali) + localText.getText("TXT_KEY_VICTORY_RICHEST_CIVILIZATION", ()) + CyTranslator().getText(str(gc.getPlayer(iMostGoldCiv).getCivilizationShortDescriptionKey()),()))
			#elif iGoal == 1:
			#	iGold = pMali.getGold()
			#	aHelp.append(self.getIcon(iGold >= utils.getTurns(4000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iGold, utils.getTurns(4000))))
			#elif iGoal == 2:
			#	iGold = pMali.getGold()
			#	aHelp.append(self.getIcon(iGold >= utils.getTurns(16000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iGold, utils.getTurns(16000))))

		elif iPlayer == iPoland:
			if iGoal == 0:
				cityList = self.getMostPopulousCities(iPoland, 3)
				bCity1 = (len(cityList) > 0)
				bCity2 = (len(cityList) > 1)
				bCity3 = (len(cityList) > 2)
				if not bCity1: aHelp.append(self.getIcon(False) + localText.getText("TXT_KEY_VICTORY_NO_CITIES", ()))
				if bCity1: aHelp.append(self.getIcon(cityList[0].getPopulation() >= 12) + localText.getText("TXT_KEY_VICTORY_CITY_SIZE", (cityList[0].getName(), cityList[0].getPopulation(), 12)))
				if bCity2: aHelp.append(self.getIcon(cityList[1].getPopulation() >= 12) + localText.getText("TXT_KEY_VICTORY_CITY_SIZE", (cityList[1].getName(), cityList[1].getPopulation(), 12)))
				if bCity3: aHelp.append(self.getIcon(cityList[2].getPopulation() >= 12) + localText.getText("TXT_KEY_VICTORY_CITY_SIZE", (cityList[2].getName(), cityList[2].getPopulation(), 12)))
			#elif iGoal == 1:
			#	bLiberalism = (self.getPolishTechs(0) == 1)
			#	bAstronomy = (self.getPolishTechs(1) == 1)
			#	aHelp.append(self.getIcon(bLiberalism) + localText.getText("TXT_KEY_TECH_LIBERALISM", ()) + ' ' + self.getIcon(bAstronomy) + localText.getText("TXT_KEY_TECH_ASTRONOMY", ()))
			elif iGoal == 2:
				iCatholic = self.getNumBuildings(iPoland, con.iChristianCathedral)
				iOrthodox = self.getNumBuildings(iPoland, con.iOrthodoxCathedral)
				iProtestant = self.getNumBuildings(iPoland, con.iJewishCathedral)
				iCathedrals = min(self.getWondersBuilt(iPoland), iCatholic+iOrthodox+iProtestant)
				aHelp.append(self.getIcon(iCathedrals >= 3) + localText.getText("TXT_KEY_VICTORY_CHRISTIAN_CATHEDRALS", (iCathedrals, 3)))	
				
		elif iPlayer == iPortugal:
			if iGoal == 0:
				iCount = 0
                                for iLoopCiv in range(iNumMajorPlayers):
                                	if (iLoopCiv != iPortugal):
                                		if (teamPortugal.isOpenBorders(iLoopCiv)):
                                			iCount += 1
				aHelp.append(self.getIcon(iCount >= 14) + localText.getText("TXT_KEY_VICTORY_OPEN_BORDERS", (iCount, 14)))
			elif iGoal == 1:
				iCount = 0
				for iBonus in [con.iBanana, con.iSpices, con.iSugar, con.iTobacco, con.iTea, con.iCoffee]:
					iCount += pPortugal.getNumAvailableBonuses(iBonus)
				aHelp.append(self.getIcon(iCount >= 12) + localText.getText("TXT_KEY_VICTORY_COLONIAL_RESOURCES", (iCount, 12)))
			elif iGoal == 2:
				iColonies = self.getNumCitiesInArea(iPortugal, tBrazilTL, tBrazilBR)
				iColonies += self.getNumCitiesInArea(iPortugal, tAfricaTL, tAfricaBR)
				iColonies += self.getNumCitiesInArea(iPortugal, tAsiaTL, tAsiaBR)
				aHelp.append(self.getIcon(iColonies >= 15) + localText.getText("TXT_KEY_VICTORY_EXTRA_EUROPEAN_COLONIES", (iColonies, 15)))

		elif iPlayer == iInca:
			if iGoal == 0:
				bRoad = self.isRoad(iInca, lAndeanCoast)
				iTambos = self.getNumBuildings(iInca, con.iIncanTambo)
				aHelp.append(self.getIcon(bRoad) + localText.getText("TXT_KEY_VICTORY_ANDEAN_ROAD", ()) + ' ' + self.getIcon(iTambos >= 5) + localText.getText("TXT_KEY_VICTORY_NUM_TAMBOS", (iTambos, 5)))
			elif iGoal == 1:
				iGold = pInca.getGold()
				aHelp.append(self.getIcon(iGold >= utils.getTurns(2500)) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iGold, utils.getTurns(2500))))
			elif iGoal == 2:
				iControl, iTotal = self.countControlledTiles(iInca, tSAmericaTL, tSAmericaBR, False, tSouthAmericaExceptions)
				fControl = iControl * 100.0 / iTotal
				aHelp.append(self.getIcon(fControl >= 60.0) + localText.getText("TXT_KEY_VICTORY_SOUTH_AMERICAN_TERRITORY", (str(u"%.2f%%" % fControl), str(60))))

		elif iPlayer == iItaly:
			if iGoal == 0:
				bSanMarcoBasilica = (self.getNumBuildings(iItaly, con.iSanMarcoBasilica) > 0)
				bSistineChapel = (self.getNumBuildings(iItaly, con.iSistineChapel) > 0)
				bLeaningTower = (self.getNumBuildings(iItaly, con.iLeaningTower) > 0)
				aHelp.append(self.getIcon(bSanMarcoBasilica) + localText.getText("TXT_KEY_BUILDING_SAN_MARCO", ()) + ' ' + self.getIcon(bSistineChapel) + localText.getText("TXT_KEY_BUILDING_SISTINE_CHAPEL", ()) + ' ' + self.getIcon(bLeaningTower) + localText.getText("TXT_KEY_BUILDING_LEANING_TOWER", ()))
			elif iGoal == 1:
				iCount = 0
				cityList = PyPlayer(iPlayer).getCityList()
				for city in cityList:
					pCity = city.GetCy()
					if pCity.getCultureLevel() >= 5:
						iCount += 1
				aHelp.append(self.getIcon(iCount >= 3) + localText.getText("TXT_KEY_VICTORY_NUM_CITIES_INFLUENTIAL_CULTURE", (iCount, 3)))
			elif iGoal == 2:
				iMediterranean, iTotalMediterranean = self.countControlledTiles(iItaly, tMediterraneanTL, tMediterraneanBR, False, tMediterraneanExceptions, True)
				fMediterranean = iMediterranean * 100.0 / iTotalMediterranean
				aHelp.append(self.getIcon(fMediterranean >= 65.0) + localText.getText("TXT_KEY_VICTORY_MEDITERRANEAN_TERRITORY", (str(u"%.2f%%" % fMediterranean), str(65))))
				
		elif iPlayer == iMongolia:
			if iGoal == 1:
				iRazedCities = self.getRazedByMongols()	
				aHelp.append(self.getIcon(iRazedCities >= 7) + localText.getText("TXT_KEY_VICTORY_NUM_CITIES_RAZED", (iRazedCities, 7)))
			elif iGoal == 2:
				totalLand = gc.getMap().getLandPlots()
                        	mongolianLand = pMongolia.getTotalLand()
                        	if (totalLand > 0):
                        		landPercent = (mongolianLand * 100.0) / totalLand
                        	else:
                        		landPercent = 0.0
				aHelp.append(self.getIcon(landPercent >= 11.995) + localText.getText("TXT_KEY_VICTORY_PERCENTAGE_WORLD_TERRITORY", (str(u"%.2f%%" % landPercent), str(12))))
				
		elif iPlayer == iMughals:
			if iGoal == 0:
				iNumMosques = self.getNumBuildings(iMughals, con.iIslamicCathedral)
				aHelp.append(self.getIcon(iNumMosques >= 3) + localText.getText("TXT_KEY_VICTORY_MOSQUES_BUILT", (iNumMosques, 3)))
			elif iGoal == 1:
				bRedFort = self.getNumBuildings(iMughals, con.iRedFort) > 0
				bHarmandirSahib = self.getNumBuildings(iMughals, con.iHarmandirSahib) > 0
				bTajMahal = self.getNumBuildings(iMughals, con.iTajMahal) > 0
				aHelp.append(self.getIcon(bRedFort) + localText.getText("TXT_KEY_BUILDING_RED_FORT", ()) + ' ' + self.getIcon(bHarmandirSahib) + localText.getText("TXT_KEY_BUILDING_HARMANDIR_SAHIB", ()) + ' ' + self.getIcon(bTajMahal) + localText.getText("TXT_KEY_BUILDING_TAJ_MAHAL", ()))
			elif iGoal == 2:
				iCulture = pMughals.countTotalCulture()
				aHelp.append(self.getIcon(iCulture >= utils.getTurns(50000)) + localText.getText("TXT_KEY_VICTORY_TOTAL_CULTURE", (iCulture, utils.getTurns(50000))))

		elif iPlayer == iAztecs:
			if not pAztecs.isReborn():
				if iGoal == 0:
					pBestCity = self.calculateTopCityPopulation(18, 37)
					bBestCity = (pBestCity.getOwner() == iAztecs and pBestCity.getX() == 18 and pBestCity.getY() == 37)
					aHelp.append(self.getIcon(bBestCity) + localText.getText("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", (pBestCity.getName(),)))
				elif iGoal == 1:
					iTemples = self.getNumBuildings(iAztecs, con.iPaganTemple)
					iAltars = self.getNumBuildings(iAztecs, con.iAztecSacrificialAltar)
					aHelp.append(self.getIcon(iTemples >= 6) + localText.getText("TXT_KEY_VICTORY_NUM_TEMPLES", (iTemples, 6)) + " " + self.getIcon(iAltars >= 6) + localText.getText("TXT_KEY_VICTORY_NUM_ALTARS", (iAltars, 6)))
				elif iGoal == 2:
					iEnslavedUnits = self.getEnslavedUnits()
					aHelp.append(self.getIcon(iEnslavedUnits >= 20) + localText.getText("TXT_KEY_VICTORY_ENSLAVED_UNITS", (iEnslavedUnits, 20)))
			else:
				if iGoal == 0:
					iNumCathedrals = 0
					iStateReligion = pAztecs.getStateReligion()
					if iStateReligion >= 0:
						iCathedral = con.iCathedral + 4*iStateReligion
						iNumCathedrals = self.getNumBuildings(iAztecs, iCathedral)
					aHelp.append(self.getIcon(iNumCathedrals >= 3) + localText.getText("TXT_KEY_VICTORY_STATE_RELIGION_CATHEDRALS", (gc.getReligionInfo(iStateReligion).getAdjectiveKey(), iNumCathedrals, 3)))
				elif iGoal == 1:
					iGenerals = pAztecs.getGreatGeneralsCreated()
					aHelp.append(self.getIcon(iGenerals >= 3) + localText.getText("TXT_KEY_VICTORY_GREAT_GENERALS", (iGenerals, 3)))
				elif iGoal == 2:
					pBestCity = self.calculateTopCityPopulation(18, 37)
					bBestCity = (pBestCity.getOwner() == iAztecs and pBestCity.getX() == 18 and pBestCity.getY() == 37)
					aHelp.append(self.getIcon(bBestCity) + localText.getText("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", (pBestCity.getName(),)))
	
		elif iPlayer == iTurkey:
			if iGoal == 0:
				capital = pTurkey.getCapitalCity()
				iCounter = 0
				for iWonder in range(con.iPyramid, con.iNumBuildings):
					if iWonder not in [con.iMilitaryAcademy, con.iItalianArtStudio]:
						if capital.isHasRealBuilding(iWonder):
							iCounter += 1
				if capital.isHasRealBuilding(con.iFlavianAmphitheatre):
					iCounter += 1
				aHelp.append(self.getIcon(iCounter >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_WONDERS_CAPITAL", (iCounter, 4)))
			elif iGoal == 1:
				bEasternMediterranean = self.isCultureControlled(iTurkey, lEasternMediterranean)
				bBlackSea = self.isCultureControlled(iTurkey, lBlackSea)
				bCairo = self.controlsCity(iTurkey, tCairo)
				bMecca = self.controlsCity(iTurkey, tMecca)
				bBaghdad = self.controlsCity(iTurkey, tBaghdad)
				bVienna = self.controlsCity(iTurkey, tVienna)
				aHelp.append(self.getIcon(bEasternMediterranean) + localText.getText("TXT_KEY_VICTORY_EASTERN_MEDITERRANEAN", ()) + ' ' + self.getIcon(bBlackSea) + localText.getText("TXT_KEY_VICTORY_BLACK_SEA", ()))
				aHelp.append(self.getIcon(bCairo) + localText.getText("TXT_KEY_VICTORY_CAIRO", ()) + ' ' + self.getIcon(bMecca) + localText.getText("TXT_KEY_VICTORY_MECCA", ()) + ' ' + self.getIcon(bBaghdad) + localText.getText("TXT_KEY_VICTORY_BAGHDAD", ()) + ' ' + self.getIcon(bVienna) + localText.getText("TXT_KEY_VICTORY_VIENNA", ()))
			elif iGoal == 2:
				iMostPowerfulCiv = self.getMostPowerfulCiv(iTurkey)
				aHelp.append(self.getIcon(iMostPowerfulCiv == iTurkey) + localText.getText("TXT_KEY_VICTORY_MOST_POWERFUL_CIV", ()) + CyTranslator().getText(str(gc.getPlayer(iMostPowerfulCiv).getCivilizationShortDescriptionKey()),()))

		elif iPlayer == iThailand:
			if iGoal == 0:
				iCount = 0
                                for iLoopCiv in range(iNumMajorPlayers):
                                	if (iLoopCiv != iThailand):
                                		if (teamThailand.isOpenBorders(iLoopCiv)):
                                			iCount += 1
				aHelp.append(self.getIcon(iCount >= 10) + localText.getText("TXT_KEY_VICTORY_OPEN_BORDERS", (iCount, 10)))
			elif iGoal == 1:
				pBestCity = self.calculateTopCityPopulation(101, 33)
				bBestCity = (pBestCity.getOwner() == iThailand and pBestCity.getX() in [101, 102] and pBestCity.getY() == 33)
				aHelp.append(self.getIcon(bBestCity) + localText.getText("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", (pBestCity.getName(),)))
			elif iGoal == 2:
				bSouthAsia = self.isAreaFreeOfCivs(tSouthAsiaTL, tSouthAsiaBR, [iIndia, iTamils, iKhmer, iIndonesia, iMughals, iThailand])
				aHelp.append(self.getIcon(bSouthAsia) + localText.getText("TXT_KEY_VICTORY_NO_SOUTH_ASIAN_COLONIES", ()))
				
		elif iPlayer == iCongo:
			if iGoal == 0:
				fPercent = self.getApostolicVotePercent(iCongo)
				aHelp.append(self.getIcon(fPercent >= 10.0) + localText.getText("TXT_KEY_VICTORY_APOSTOLIC_VOTE_PERCENT", (str(u"%.2f%%" % fPercent), str(10))))
			elif iGoal == 1:
				iSlaves = self.getCongoSlaveCounter()
				aHelp.append(self.getIcon(iSlaves >= utils.getTurns(1000)) + localText.getText("TXT_KEY_VICTORY_SLAVES_TRADED", (iSlaves, utils.getTurns(1000))))

		elif iPlayer == iAmerica:
			if iGoal == 0:
                        	bAmericas = True
                        	for iEuroCiv in range(iNumPlayers):
                        		if (iEuroCiv in con.lCivGroups[0]):
                        			if (self.checkNotOwnedArea(iEuroCiv, tNCAmericaTL, tNCAmericaBR) == False):
                        				bAmericas = False
                        				break
				bMexico = self.isControlledOrVassalized(iAmerica, con.tCoreAreasTL[1][iAztecs], con.tCoreAreasBR[1][iAztecs], con.tExceptions[1][iAztecs])
				aHelp.append(self.getIcon(bAmericas) + localText.getText("TXT_KEY_VICTORY_NO_NORTH_AMERICAN_COLONIES", ()) + ' ' + self.getIcon(bMexico) + localText.getText("TXT_KEY_CIV_MEXICO_SHORT_DESC", ()))
			elif iGoal == 1:	# not entirely correct, you actually have to build them, this counts conquered ones as well
				bUnitedNations = (self.getNumBuildings(iAmerica, con.iUnitedNations) > 0)
				bStatueOfLiberty = (self.getNumBuildings(iAmerica, con.iStatueOfLiberty) > 0)
				bPentagon = (self.getNumBuildings(iAmerica, con.iPentagon) > 0)
				bEmpireState = (self.getNumBuildings(iAmerica, con.iEmpireState) > 0)
				aHelp.append(self.getIcon(bStatueOfLiberty) + localText.getText("TXT_KEY_BUILDING_STATUE_OF_LIBERTY", ()) + ' ' + self.getIcon(bEmpireState) + localText.getText("TXT_KEY_BUILDING_EMPIRE_STATE", ()) + ' ' + self.getIcon(bPentagon) + localText.getText("TXT_KEY_BUILDING_PENTAGON", ()) + ' ' + self.getIcon(bUnitedNations) + localText.getText("TXT_KEY_BUILDING_UNITED_NATIONS", ()))
			elif iGoal == 2:
				iCounter = pAmerica.getNumAvailableBonuses(con.iOil) - pAmerica.getBonusImport(con.iOil)
                                for iCiv in range(iNumPlayers):
                                	if (iCiv != iAmerica):
                                		if (gc.getPlayer(iCiv).isAlive()):
                                			if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iAmerica)):
                                				iCounter += gc.getPlayer(iCiv).getNumAvailableBonuses(con.iOil) - gc.getPlayer(iCiv).getBonusImport(con.iOil)
				aHelp.append(self.getIcon(iCounter >= 10) + localText.getText("TXT_KEY_VICTORY_OIL_SECURED", (iCounter, 10)))
				
		elif iPlayer == iArgentina:
			if iGoal == 0:
				capital = pArgentina.getCapitalCity()
				iGreatGeneral = gc.getInfoTypeForString("SPECIALIST_GREAT_GENERAL")
				iGenerals = 0
				if not capital.isNone(): iGenerals = capital.getFreeSpecialistCount(iGreatGeneral)
				aHelp.append(self.getIcon(iGenerals >= 2) + localText.getText("TXT_KEY_VICTORY_GREAT_GENERALS_CAPITAL", (iGenerals, 2)))
			elif iGoal == 1:
				pHighestCommerceCity = self.calculateHighestCommerceCity()
				aHelp.append(self.getIcon(pHighestCommerceCity.getOwner() == iArgentina) + localText.getText("TXT_KEY_VICTORY_BEST_COMMERCE_CITY", (pHighestCommerceCity.getName(),)))
			elif iGoal == 2:
				pBuenosAires = gc.getMap().plot(con.tCapitals[0][iArgentina][0], con.tCapitals[0][iArgentina][1])
				iCulture = 0
				if pBuenosAires.isCity(): iCulture = pBuenosAires.getPlotCity().getCulture(iArgentina)
				aHelp.append(self.getIcon(iCulture >= utils.getTurns(25000)) + localText.getText("TXT_KEY_VICTORY_CITY_CULTURE", ("Buenos Aires", iCulture, utils.getTurns(25000))))
				
		elif iPlayer == iBrazil:
			if iGoal == 0:
				iSlavePlantations = self.countImprovements(iBrazil, con.iSlavePlantation)
				iPastures = self.countImprovements(iBrazil, con.iPasture)
				aHelp.append(self.getIcon(iSlavePlantations >= 10) + localText.getText("TXT_KEY_VICTORY_NUM_IMPROVEMENTS", (gc.getImprovementInfo(con.iSlavePlantation).getText(), iSlavePlantations, 10)) + ' ' + self.getIcon(iPastures >= 4) + localText.getText("TXT_KEY_VICTORY_NUM_IMPROVEMENTS", (gc.getImprovementInfo(con.iPasture).getText(), iPastures, 4)))
			elif iGoal == 1:
				bWembley = (self.getNumBuildings(iBrazil, con.iWembley) > 0)
				bCristoRedentor = (self.getNumBuildings(iBrazil, con.iCristoRedentor) > 0)
				bThreeGorgesDam = (self.getNumBuildings(iBrazil, con.iThreeGorgesDam) > 0)
				aHelp.append(self.getIcon(bWembley) + localText.getText("TXT_KEY_BUILDING_BROADWAY", ()) + ' ' + self.getIcon(bCristoRedentor) + localText.getText("TXT_KEY_BUILDING_CRISTO_REDENTOR", ()) + ' ' + self.getIcon(bThreeGorgesDam) + localText.getText("TXT_KEY_BUILDING_GREAT_DAM", ()))
			elif iGoal == 2:
				iForestPreserves = self.countImprovements(iBrazil, con.iForestPreserve)
				bNationalPark = False
				capital = pBrazil.getCapitalCity()
				if capital: bNationalPark = capital.isHasRealBuilding(con.iNationalPark)
				aHelp.append(self.getIcon(iForestPreserves >= 20) + localText.getText("TXT_KEY_VICTORY_NUM_IMPROVEMENTS", (gc.getImprovementInfo(con.iForestPreserve).getText(), iForestPreserves, 20)) + ' ' + self.getIcon(bNationalPark) + localText.getText("TXT_KEY_VICTORY_NATIONAL_PARK_CAPITAL", ()))
		
		return aHelp




