# Rhye's and Fall of Civilization - Main Scenario

from CvPythonExtensions import *
import CvUtil
import PyHelpers        # LOQ
import Popup
#import cPickle as pickle
from StoredData import sd # edead
import CvTranslator
import RFCUtils
import Consts as con
import CityNameManager as cnm
import Victory as vic
import DynamicCivs
from operator import itemgetter
import Stability as sta


################
### Globals ###
##############

gc = CyGlobalContext()  # LOQ
PyPlayer = PyHelpers.PyPlayer   # LOQ
utils = RFCUtils.RFCUtils()
dc = DynamicCivs.DynamicCivs()

iCheatersPeriod = 12
iBetrayalPeriod = 8
iBetrayalThreshold = 80
iRebellionDelay = 15
iEscapePeriod = 30
tAIStopBirthThreshold = con.tAIStopBirthThreshold
tBirth = con.tBirth
iWorker = con.iWorker
iSettler = con.iSettler
iWarrior = con.iWarrior
iScout = con.iScout
iGalley = con.iGalley


# initialise player variables

iEgypt = con.iEgypt
iIndia = con.iIndia
iChina = con.iChina
iBabylonia = con.iBabylonia
iGreece = con.iGreece
iPersia = con.iPersia
iCarthage = con.iCarthage
iRome = con.iRome
iTamils = con.iTamils
iJapan = con.iJapan
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
iSeljuks = con.iSeljuks
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
pTamils = gc.getPlayer(iTamils)
pJapan = gc.getPlayer(iJapan)
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
pSeljuks = gc.getPlayer(iSeljuks)
pBarbarian = gc.getPlayer(iBarbarian)

teamEgypt = gc.getTeam(pEgypt.getTeam())
teamIndia = gc.getTeam(pIndia.getTeam())
teamChina = gc.getTeam(pChina.getTeam())
teamBabylonia = gc.getTeam(pBabylonia.getTeam())
teamGreece = gc.getTeam(pGreece.getTeam())
teamPersia = gc.getTeam(pPersia.getTeam())
teamCarthage = gc.getTeam(pCarthage.getTeam())
teamRome = gc.getTeam(pRome.getTeam())
teamTamils = gc.getTeam(pTamils.getTeam())
teamJapan = gc.getTeam(pJapan.getTeam())
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
teamSeljuks = gc.getTeam(pSeljuks.getTeam())
teamBarbarian = gc.getTeam(pBarbarian.getTeam())

# starting locations coordinates
tCapitals = con.tCapitals

# core areas coordinates (top left and bottom right)

tCoreAreasTL = con.tCoreAreasTL
tCoreAreasBR = con.tCoreAreasBR

tExceptions = con.tExceptions

tNormalAreasTL = con.tNormalAreasTL
tNormalAreasBR = con.tNormalAreasBR

tBroaderAreasTL = con.tBroaderAreasTL 
tBroaderAreasBR = con.tBroaderAreasBR

#lConditionalCivs = [iByzantium]

class RiseAndFall:

##################################################
### Secure storage & retrieval of script data ###
################################################
        

        def getNewCiv( self ):
                return sd.scriptDict['iNewCiv']

        def setNewCiv( self, iNewValue ):
                sd.scriptDict['iNewCiv'] = iNewValue
		
	def getRespawnCiv(self):
		return sd.scriptDict['iRespawnCiv']
		
	def setRespawnCiv(self, iNewValue):
		sd.scriptDict['iRespawnCiv'] = iNewValue

        def getNewCivFlip( self ):
                return sd.scriptDict['iNewCivFlip']

        def setNewCivFlip( self, iNewValue ):
                sd.scriptDict['iNewCivFlip'] = iNewValue

        def getOldCivFlip( self ):
                return sd.scriptDict['iOldCivFlip']

        def setOldCivFlip( self, iNewValue ):
                sd.scriptDict['iOldCivFlip'] = iNewValue
                
        def getTempTopLeft( self ):
                return sd.scriptDict['tempTopLeft']

        def setTempTopLeft( self, tNewValue ):
                sd.scriptDict['tempTopLeft'] = tNewValue

        def getTempBottomRight( self ):
                return sd.scriptDict['tempBottomRight']

        def setTempBottomRight( self, tNewValue ):
                sd.scriptDict['tempBottomRight'] = tNewValue

        def getSpawnWar( self ):
                return sd.scriptDict['iSpawnWar']

        def setSpawnWar( self, iNewValue ):
                sd.scriptDict['iSpawnWar'] = iNewValue

        def getAlreadySwitched( self ):
                return sd.scriptDict['bAlreadySwitched']

        def setAlreadySwitched( self, bNewValue ):
                sd.scriptDict['bAlreadySwitched'] = bNewValue

        def getColonistsAlreadyGiven( self, iCiv ):
                return sd.scriptDict['lColonistsAlreadyGiven'][iCiv]

        def setColonistsAlreadyGiven( self, iCiv, iNewValue ):
                sd.scriptDict['lColonistsAlreadyGiven'][iCiv] = iNewValue
		
	def changeColonistsAlreadyGiven(self, iCiv, iChange):
		sd.scriptDict['lColonistsAlreadyGiven'][iCiv] += iChange

        def getAstronomyTurn( self, iCiv ):
                return sd.scriptDict['lAstronomyTurn'][iCiv]

        def setAstronomyTurn( self, iCiv, iNewValue ):
		sd.scriptDict['lAstronomyTurn'][iCiv] = iNewValue

        def getNumCities( self, iCiv ):
                return sd.scriptDict['lNumCities'][iCiv]

        def setNumCities( self, iCiv, iNewValue ):
                sd.scriptDict['lNumCities'][iCiv] = iNewValue
                
        def getSpawnDelay( self, iCiv ):
                return sd.scriptDict['lSpawnDelay'][iCiv]

        def setSpawnDelay( self, iCiv, iNewValue ):
                sd.scriptDict['lSpawnDelay'][iCiv] = iNewValue

        def getFlipsDelay( self, iCiv ):
                return sd.scriptDict['lFlipsDelay'][iCiv]

        def setFlipsDelay( self, iCiv, iNewValue ):
                sd.scriptDict['lFlipsDelay'][iCiv] = iNewValue

        def getBetrayalTurns( self ):
                return sd.scriptDict['iBetrayalTurns']

        def setBetrayalTurns( self, iNewValue ):
                sd.scriptDict['iBetrayalTurns'] = iNewValue

        def getLatestFlipTurn( self ):
                return sd.scriptDict['iLatestFlipTurn']

        def setLatestFlipTurn( self, iNewValue ):
                sd.scriptDict['iLatestFlipTurn'] = iNewValue

        def getLatestRebellionTurn( self, iCiv ):
		return gc.getPlayer(iCiv).getLatestRebellionTurn()

        def setLatestRebellionTurn( self, iCiv, iNewValue ):
		gc.getPlayer(iCiv).setLatestRebellionTurn(iNewValue)

        def getRebelCiv( self ):
                return sd.scriptDict['iRebelCiv']

        def setRebelCiv( self, iNewValue ):
                sd.scriptDict['iRebelCiv'] = iNewValue
                
        def getExileData( self, i ):
                return sd.scriptDict['lExileData'][i]

        def setExileData( self, i, iNewValue ):
                sd.scriptDict['lExileData'][i] = iNewValue
        
        def getTempFlippingCity( self ):
                return sd.scriptDict['tempFlippingCity']

        def setTempFlippingCity( self, tNewValue ):
                sd.scriptDict['tempFlippingCity'] = tNewValue

        def getCheatersCheck( self, i ):
                return sd.scriptDict['lCheatersCheck'][i]

        def setCheatersCheck( self, i, iNewValue ):
                sd.scriptDict['lCheatersCheck'][i] = iNewValue

        def getBirthTurnModifier( self, iCiv ):
                return sd.scriptDict['lBirthTurnModifier'][iCiv]

        def setBirthTurnModifier( self, iCiv, iNewValue ):
                sd.scriptDict['lBirthTurnModifier'][iCiv] = iNewValue

        def getDeleteMode( self, i ):
                return sd.scriptDict['lDeleteMode'][i]

        def setDeleteMode( self, i, iNewValue ):
                sd.scriptDict['lDeleteMode'][i] = iNewValue

        def getFirstContactConquerors( self, iCiv ):
                return sd.scriptDict['lFirstContactConquerors'][iCiv]

        def setFirstContactConquerors( self, iCiv, iNewValue ):
                sd.scriptDict['lFirstContactConquerors'][iCiv] = iNewValue

        def getCheatMode( self ):
                return sd.scriptDict['bCheatMode']

        def setCheatMode( self, bNewValue ):
                sd.scriptDict['bCheatMode'] = bNewValue

        def setTempFlippingCity(self, tPlot):
                sd.scriptDict['tTempFlippingCity'] = tPlot

        def getTempFlippingCity(self):
                return sd.scriptDict['tTempFlippingCity']

	def setFirstContactMongols(self, iCiv, iValue):
		lMongolCivs = [iPersia, iByzantium, iArabia, iRussia, iMughals]
		sd.scriptDict['lFirstContactMongols'][lMongolCivs.index(iCiv)] = iValue

	def getFirstContactMongols(self, iCiv):
		lMongolCivs = [iPersia, iByzantium, iArabia, iRussia, iMughals]
		return sd.scriptDict['lFirstContactMongols'][lMongolCivs.index(iCiv)]
		
	def setPlayerEnabled(self, iCiv, bNewValue):
		sd.scriptDict['lPlayerEnabled'][con.lSecondaryCivs.index(iCiv)] = bNewValue
		if bNewValue == False: gc.getPlayer(iCiv).getPlayable(False)
		
	def getPlayerEnabled(self, iCiv):
		return sd.scriptDict['lPlayerEnabled'][con.lSecondaryCivs.index(iCiv)]
                
###############
### Popups ###
#############

        ''' popupID has to be a registered ID in CvRhyesCatapultEventManager.__init__!! '''
        def showPopup(self, popupID, title, message, labels):
                popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
                popup.setHeaderString(title)
                popup.setBodyString(message)
                for i in labels:
                    popup.addButton( i )
                popup.launch(False)

        def newCivPopup(self, iCiv):
                self.showPopup(7614, CyTranslator().getText("TXT_KEY_NEWCIV_TITLE", ()), CyTranslator().getText("TXT_KEY_NEWCIV_MESSAGE", (gc.getPlayer(iCiv).getCivilizationAdjectiveKey(),)), (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_NO", ())))
                self.setNewCiv(iCiv)

        def eventApply7614(self, popupReturn):
                if( popupReturn.getButtonClicked() == 0 ): # 1st button
			self.handleNewCiv(self.getNewCiv())
			
	def respawnPopup(self, iCiv):
		self.showPopup(7628, CyTranslator().getText("TXT_KEY_NEWCIV_TITLE", ()), CyTranslator().getText("TXT_KEY_NEWCIV_MESSAGE", (gc.getPlayer(iCiv).getCivilizationAdjectiveKey(),)), (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_NO", ())))
                self.setRespawnCiv(iCiv)
		
	def eventApply7628(self, popupReturn):
		if popupReturn.getButtonClicked() == 0:
			self.handleNewCiv(self.getRespawnCiv())
		
	def handleNewCiv(self, iCiv):
		iPreviousCiv = utils.getHumanID()
		iOldHandicap = gc.getActivePlayer().getHandicapType()
		gc.getActivePlayer().setHandicapType(gc.getPlayer(iCiv).getHandicapType())
		gc.getGame().setActivePlayer(iCiv, False)
		gc.getPlayer(iCiv).setHandicapType(iOldHandicap)
		for iMaster in range(con.iNumPlayers):
			if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iMaster)):
				gc.getTeam(gc.getPlayer(iCiv).getTeam()).setVassal(iMaster, False, False)
		self.setAlreadySwitched(True)
		gc.getPlayer(iCiv).setPlayable(True)
		sd.setCrisisImminent(False)

		pPlayer = gc.getPlayer(iCiv)
		pCity, iter = pPlayer.firstCity(true)

		for x in range(0, 124):
			for y in range(0, 168):
				if (gc.getMap().plot(x,y).isCity()):
					city = gc.getMap().plot( x,y ).getPlotCity()
					if (city.getOwner() == iCiv):
						city.setInfoDirty(True)
						city.setLayoutDirty(True)
						
		for i in range(3):
			utils.setGoal(iCiv, i, -1)
						
		if gc.getDefineINT("NO_AI_UHV_CHECKS") == 1:
			for i in range(3):
				utils.setGoal(iPreviousCiv, i, 0)

        def flipPopup(self, iNewCiv, tTopLeft, tBottomRight):
                iHuman = utils.getHumanID()
		if iHuman == iNewCiv:
			print "Human and new civ are identical, there's something wrong here!"
                flipText = CyTranslator().getText("TXT_KEY_FLIPMESSAGE1", ())
                for x in range(tTopLeft[0], tBottomRight[0]+1):
                        for y in range(tTopLeft[1], tBottomRight[1]+1):
				if not (x,y) in tExceptions[utils.getReborn(iNewCiv)][iNewCiv]:
                                	pCurrent = gc.getMap().plot( x, y )
                                	if ( pCurrent.isCity()):
                                        	if (pCurrent.getPlotCity().getOwner() == iHuman):
                                                	#if (not pCurrent.getPlotCity().isCapital()): #exploitable
                                                	if ( ((x, y) != tCapitals[utils.getReborn(iHuman)][iHuman]) and not (self.getCheatMode() == True and pCurrent.getPlotCity().isCapital())):
                                                        	flipText += (pCurrent.getPlotCity().getName() + "\n")
								
                flipText += CyTranslator().getText("TXT_KEY_FLIPMESSAGE2", ())
                                                        
                self.showPopup(7615, CyTranslator().getText("TXT_KEY_NEWCIV_TITLE", ()), flipText, (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_NO", ())))
                self.setNewCivFlip(iNewCiv)
                self.setOldCivFlip(iHuman)
                self.setTempTopLeft(tTopLeft)
                self.setTempBottomRight(tBottomRight)

        def eventApply7615(self, popupReturn):
                iHuman = utils.getHumanID()
                tTopLeft = self.getTempTopLeft()
                tBottomRight = self.getTempBottomRight()
                iNewCivFlip = self.getNewCivFlip()

                humanCityList = []
                for x in range(tTopLeft[0], tBottomRight[0]+1):
                        for y in range(tTopLeft[1], tBottomRight[1]+1):
				if not (x,y) in tExceptions[utils.getReborn(iNewCivFlip)][iNewCivFlip]:
	                                pCurrent = gc.getMap().plot( x, y )
        	                        if ( pCurrent.isCity()):
                	                        city = pCurrent.getPlotCity()
                        	                if (city.getOwner() == iHuman):
                                        	        if (not (x == tCapitals[utils.getReborn(iHuman)][iHuman] and y == tCapitals[utils.getReborn(iHuman)][iHuman]) and not (self.getCheatMode() == True and pCurrent.getPlotCity().isCapital())):
                                                	        humanCityList.append(city)
                
                if( popupReturn.getButtonClicked() == 0 ): # 1st button
                        print ("Flip agreed")
                        CyInterface().addMessage(iHuman, True, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_AGREED", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
                                                
                        if (len(humanCityList)):
                                for i in range(len(humanCityList)):
                                        city = humanCityList[i]
                                        print ("flipping ", city.getName())
                                        utils.cultureManager((city.getX(),city.getY()), 100, iNewCivFlip, iHuman, False, False, False)
                                        utils.flipUnitsInCityBefore((city.getX(),city.getY()), iNewCivFlip, iHuman)
                                        self.setTempFlippingCity((city.getX(),city.getY()))
                                        utils.flipCity((city.getX(), city.getY()), 0, 0, iNewCivFlip, [iHuman])                                        
                                        utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCivFlip)

                        #same code as Betrayal - done just once to make sure human player doesn't hold a stack just outside of the cities
                        for x in range(tTopLeft[0], tBottomRight[0]+1):
                                for y in range(tTopLeft[1], tBottomRight[1]+1):
                                        betrayalPlot = gc.getMap().plot(x,y)
                                        iNumUnitsInAPlot = betrayalPlot.getNumUnits()
                                        if (iNumUnitsInAPlot):                                                                  
                                                for i in range(iNumUnitsInAPlot):                                                
                                                        unit = betrayalPlot.getUnit(i)
                                                        if (unit.getOwner() == iHuman):
                                                                rndNum = gc.getGame().getSorenRandNum(100, 'betrayal')
                                                                if (rndNum >= iBetrayalThreshold):
                                                                        if (unit.getDomainType() == 2): #land unit
                                                                                iUnitType = unit.getUnitType()
                                                                                unit.kill(False, iNewCivFlip)
                                                                                utils.makeUnit(iUnitType, iNewCivFlip, (x,y), 1)
                                                                                i = i - 1


                        if (self.getCheatersCheck(0) == 0):
                                self.setCheatersCheck(0, iCheatersPeriod)
                                self.setCheatersCheck(1, self.getNewCivFlip())
                                
                elif( popupReturn.getButtonClicked() == 1 ): # 2nd button
                        print ("Flip disagreed")
                        CyInterface().addMessage(iHuman, True, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_REFUSED", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
                                                

                        if (len(humanCityList)):
                                for i in range(len(humanCityList)):
                                        city = humanCityList[i]
                                        pCurrent = gc.getMap().plot(city.getX(), city.getY())
                                        oldCulture = pCurrent.getCulture(iHuman)
                                        pCurrent.setCulture(iNewCivFlip, oldCulture/2, True)
                                        pCurrent.setCulture(iHuman, oldCulture/2, True)                                        
                                        iWar = self.getSpawnWar() + 1
                                        self.setSpawnWar(iWar)
                                        if (self.getSpawnWar() == 1):
                                                gc.getTeam(gc.getPlayer(iNewCivFlip).getTeam()).declareWar(iHuman, False, -1) ##True??
                                                self.setBetrayalTurns(iBetrayalPeriod)
                                                self.initBetrayal()                                                              
                                
        def rebellionPopup(self, iRebelCiv):
                self.showPopup(7622, CyTranslator().getText("TXT_KEY_REBELLION_TITLE", ()), \
                               CyTranslator().getText("TXT_KEY_REBELLION_TEXT", (gc.getPlayer(iRebelCiv).getCivilizationAdjectiveKey(),)), \
                               (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), \
                                CyTranslator().getText("TXT_KEY_POPUP_NO", ())))             

        def eventApply7622(self, popupReturn):
                iHuman = utils.getHumanID()
                iRebelCiv = self.getRebelCiv()
                if( popupReturn.getButtonClicked() == 0 ): # 1st button
                        gc.getTeam(gc.getPlayer(iHuman).getTeam()).makePeace(iRebelCiv)                                                   
                elif( popupReturn.getButtonClicked() == 1 ): # 2nd button
                        gc.getTeam(gc.getPlayer(iHuman).getTeam()).declareWar(iRebelCiv, False, -1)

	def eventApply7625(self, popupReturn):
		iHuman = utils.getHumanID()
		iPlayer, targetList = utils.getTempEventList()
		if popupReturn.getButtonClicked() == 0:
			for tPlot in targetList:
				x, y = tPlot
				if gc.getMap().plot(x, y).getPlotCity().getOwner() == iHuman:
					utils.colonialAcquisition(iPlayer, x, y)
					gc.getPlayer(iHuman).changeGold(200)
		elif popupReturn.getButtonClicked() == 1:
			for tPlot in targetList:
				x, y = tPlot
				if gc.getMap().plot(x, y).getPlotCity().getOwner() == iHuman:
					utils.colonialConquest(iPlayer, x, y)
					
	def eventApply7627(self, popupReturn):
		lReligionList, tCityPlot = utils.getTempEventList()
		x, y = tCityPlot
		city = gc.getMap().plot(x, y).getPlotCity()
		
		utils.debugTextPopup("lReligionList: "+str(lReligionList)+"\n Button clicked: "+str(popupReturn.getButtonClicked()))
		
		iPersecutedReligion = lReligionList[popupReturn.getButtonClicked()]
		
		utils.debugTextPopup("iPersecutedReligion: "+str(gc.getReligionInfo(iPersecutedReligion).getText()))
		
		city.setHasReligion(iPersecutedReligion, False, True, True)
		city.setHasRealBuilding(con.iTemple + 4*iPersecutedReligion, False)
		city.setHasRealBuilding(con.iMonastery + 4*iPersecutedReligion, False)
		city.setHasRealBuilding(con.iCathedral + 4*iPersecutedReligion, False)
		city.changeOccupationTimer(2)
		city.changeHurryAngerTimer(city.hurryAngerLength(0))
		
		CyInterface().addMessage(city.getOwner(), True, con.iDuration, CyTranslator().getText("TXT_KEY_PERSECUTION_PERFORMED", (gc.getReligionInfo(iPersecutedReligion).getText(), city.getName())), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
		


#######################################
### Main methods (Event-Triggered) ###
#####################################  

        def setup(self):            

                self.determineEnabledPlayers()
		
		self.initScenario()
		
                # Leoreth: make sure to select the Egyptian settler
                if (pEgypt.isHuman()):
                        plotEgypt = gc.getMap().plot(tCapitals[0][iEgypt][0], tCapitals[0][iEgypt][1])  
			for i in range(plotEgypt.getNumUnits()):
				unit = plotEgypt.getUnit(i)
				if unit.getUnitType() == con.iSettler:
					CyInterface().selectUnit(unit, true, false, false)
					break
					
	def initScenario(self):
	
		self.adjustCityCulture()
			
		self.foundCapitals()
		self.flipStartingTerritory()
	
		if utils.getScenario() == con.i3000BC:
			self.create4000BCstartingUnits()
			#self.set3000BCStability()
			
		if utils.getScenario() == con.i600AD:
			self.create600ADstartingUnits()
			self.assign600ADTechs()
			self.assign600ADGold()
			#self.set600ADStability()
			
		if utils.getScenario() == con.i1700AD:
			self.create1700ADstartingUnits()
			self.assign1700ADTechs()
			self.assign1700ADGold()
			self.init1700ADDiplomacy()
			#self.set1700ADStability()
			self.prepareColonists()
			self.adjust1700ADCulture()
			
			pPersia.setReborn()
			pHolyRome.setReborn()
		
		self.assign3000BCGold()	
		self.invalidateUHVs()
		
	def adjustCityCulture(self):
	
		if utils.getTurns(10) == 10: return
	
		lCities = []
		for iPlayer in range(con.iNumTotalPlayersB):
			lCities.extend(utils.getCityList(iPlayer))
			
		for city in lCities:
			city.setCulture(city.getOwner(), utils.getTurns(city.getCulture(city.getOwner())), True)
			
	def adjust1700ADCulture(self):
	
		for x in range(124):
			for y in range(68):
				plot = gc.getMap().plot(x, y)
				if plot.getOwner() != -1:
					utils.convertPlotCulture(plot, plot.getOwner(), 100, True)
			
	def prepareColonists(self):
	
		for iPlayer in [iSpain, iFrance, iEngland, iPortugal, iNetherlands, iGermany, iVikings]:
			self.setAstronomyTurn(iPlayer, getTurnForYear(1700))
			
		self.setColonistsAlreadyGiven(iVikings, 1)
		self.setColonistsAlreadyGiven(iSpain, 7)
		self.setColonistsAlreadyGiven(iFrance, 3)
		self.setColonistsAlreadyGiven(iEngland, 3)
		self.setColonistsAlreadyGiven(iPortugal, 6)
		self.setColonistsAlreadyGiven(iNetherlands, 4)
		
	def assign3000BCGold(self):
	
		for iPlayer in range(con.iNumTotalPlayers):
			gc.getPlayer(iPlayer).changeGold(con.tStartingGold[iPlayer])
			
	def assign600ADGold(self):
	
		pChina.changeGold(300)
		pJapan.changeGold(150)
		
		pIndependent.changeGold(50)
		pIndependent2.changeGold(50)
		pNative.changeGold(200)
		pSeljuks.changeGold(250)
		
	def assign1700ADGold(self):
	
		pChina.changeGold(300)
		pJapan.changeGold(100)
		
		pSpain.changeGold(200)
		pFrance.changeGold(250)
		pEngland.changeGold(400)
		pRussia.changeGold(150)
		pPoland.changeGold(100)
		pPortugal.changeGold(250)
		pMughals.changeGold(-200)
		pTurkey.changeGold(-100)
		pThailand.changeGold(-500)
		pNetherlands.changeGold(200)
		
	def init1700ADDiplomacy(self):
	
		self.changeAttitudeExtra(iPersia, iTurkey, -4)
		self.changeAttitudeExtra(iPersia, iMughals, -2)
		self.changeAttitudeExtra(iChina, iKorea, 2)
		self.changeAttitudeExtra(iVikings, iRussia, -2)
		self.changeAttitudeExtra(iVikings, iTurkey, -2)
		self.changeAttitudeExtra(iSpain, iPortugal, 2)
		self.changeAttitudeExtra(iFrance, iEngland, -4)
		self.changeAttitudeExtra(iFrance, iNetherlands, 2)
		self.changeAttitudeExtra(iFrance, iTurkey, -2)
		self.changeAttitudeExtra(iEngland, iPortugal, 2)
		self.changeAttitudeExtra(iEngland, iMughals, -2)
		self.changeAttitudeExtra(iEngland, iTurkey, -2)
		self.changeAttitudeExtra(iHolyRome, iTurkey, -4)
		self.changeAttitudeExtra(iRussia, iTurkey, -4)
		self.changeAttitudeExtra(iPortugal, iNetherlands, -2)
		self.changeAttitudeExtra(iNetherlands, iTurkey, -2)
		
		teamEngland.declareWar(iMughals, False, WarPlanTypes.WARPLAN_TOTAL)
	
	def changeAttitudeExtra(self, iPlayer1, iPlayer2, iValue):
	
		gc.getPlayer(iPlayer1).AI_changeAttitudeExtra(iPlayer2, iValue)
		gc.getPlayer(iPlayer2).AI_changeAttitudeExtra(iPlayer1, iValue)
		
	def set3000BCStability(self):
	
		return
			
	def set600ADStability(self):
	
		return
		
	def set1700ADStability(self):
	
		return

	def invalidateUHVs(self):
	
		for iPlayer in range(con.iNumPlayers):
			if not gc.getPlayer(iPlayer).isPlayable():
				for i in range(3):
					utils.setGoal(iPlayer, i, 0)
					
	def foundCapitals(self):
	
		if utils.getScenario() == con.i600AD:
		
			# Byzantium
			tCapital = con.tCapitals[0][iByzantium]
			lBuildings = [con.iWalls, con.iCastle, con.iBarracks, con.iStable, con.iGranary, con.iLibrary, con.iMarket, con.iGrocer, \
				      con.iOrthodoxTemple, con.iByzantineHippodrome, con.iOrthodoxShrine, con.iTheodosianWalls]
			city = utils.foundCapital(iByzantium, tCapital, 'Konstantinoupolis', 4, 250, lBuildings, [con.iChristianity, con.iOrthodoxy])
			gc.getGame().setHolyCity(con.iOrthodoxy, city, False)
			
			# China
			self.prepareChina()
			tCapital = con.tCapitals[0][iChina]
			lBuildings = [con.iConfucianTemple, con.iChineseTaixue, con.iBarracks, con.iForge]
			utils.foundCapital(iChina, tCapital, "Xi'an", 4, 100, lBuildings, [con.iConfucianism, con.iTaoism])
			
		if utils.getScenario() == con.i1700AD:
			
			# London
			x, y = con.tCapitals[0][iEngland]
			pLondon = gc.getMap().plot(x, y).getPlotCity()
			pLondon.setFreeSpecialistCount(con.iGreatMerchant, 1)
			
			# Paris
			x, y = con.tCapitals[0][iFrance]
			pParis = gc.getMap().plot(x, y).getPlotCity()
			pParis.setFreeSpecialistCount(con.iGreatScientist, 1)
			
			# Netherlands
			x, y = con.tCapitals[0][iNetherlands]
			pAmsterdam = gc.getMap().plot(x, y).getPlotCity()
			pAmsterdam.setFreeSpecialistCount(con.iGreatMerchant, 2)
			
			# Hamburg
			x, y = con.tHamburg
			pHamburg = gc.getMap().plot(x, y).getPlotCity()
			pHamburg.setFreeSpecialistCount(con.iGreatMerchant, 1)
			pHamburg.setCulture(iNetherlands, 0, True)
			gc.getMap().plot(x, y).setCulture(iNetherlands, 0, True)
			
			# Milan
			x, y = con.tMilan
			pMilan = gc.getMap().plot(x, y).getPlotCity()
			pMilan.setFreeSpecialistCount(con.iGreatMerchant, 2)
			pMilan.setFreeSpecialistCount(con.iGreatEngineer, 1)
			
			# Kyoto
			x, y = con.tCapitals[0][iJapan]
			pKyoto = gc.getMap().plot(x, y).getPlotCity()
			pKyoto.setFreeSpecialistCount(con.iGreatMerchant, 1)
			
			# Mecca
			pMecca = gc.getGame().getHolyCity(con.iIslam)
			pMecca.setFreeSpecialistCount(con.iGreatPriest, 2)
			
			# Rome
			x, y = con.tCapitals[0][iRome]
			pRome = gc.getMap().plot(x, y).getPlotCity()
			pRome.setFreeSpecialistCount(con.iGreatPriest, 1)
			
			# Baghdad
			x, y = con.tBaghdad
			pBaghdad = gc.getMap().plot(x, y).getPlotCity()
			pBaghdad.setFreeSpecialistCount(con.iGreatPriest, 1)
			
			# Pataliputra
			pPataliputra = gc.getGame().getHolyCity(con.iHinduism)
			pPataliputra.setFreeSpecialistCount(con.iGreatPriest, 2)
			
			# Lhasa
			x, y = con.tCapitals[0][iTibet]
			pLhasa = gc.getMap().plot(x, y).getPlotCity()
			pLhasa.setFreeSpecialistCount(con.iGreatPriest, 2)
			
			# Ayutthaya
			x, y = con.tCapitals[0][iThailand]
			pAyutthaya = gc.getMap().plot(x, y).getPlotCity()
			pAyutthaya.setFreeSpecialistCount(con.iGreatPriest, 1)
			
			# Chengdu
			pChengdu = gc.getMap().plot(99, 41).getPlotCity()
			pChengdu.setCulture(con.iChina, 10, True)
			
	def flipStartingTerritory(self):
	
		if utils.getScenario() == con.i600AD:
		
			# Byzantium
			tTL1 = (62, 37)
			tBR1 = (76, 45)
			tTL2 = (66, 34)
			tBR2 = (70, 37)
			self.startingFlip(iByzantium, [(tTL1, tBR1), (tTL2, tBR2)])
			
			# China
			tTL = tCoreAreasTL[0][iChina]
			tBR = tCoreAreasBR[0][iChina]
			if utils.getHumanID() != iChina: tTL = (99, 39) # 4 tiles further south
			self.startingFlip(iChina, [(tTL, tBR)])
			
		if utils.getScenario() == con.i1700AD:
		
			# China (Tibet)
			tTL = (94, 42)
			tBR = (97, 45)
			self.startingFlip(iChina, [(tTL, tBR)])
			
			
	def startingFlip(self, iPlayer, lRegionList):
	
		for tuple in lRegionList:
			tTL = tuple[0]
			tBR = tuple[1]
			tExceptions = ()
			if len(tuple) > 2: tExceptions = tuple[2]
			self.convertSurroundingCities(iPlayer, tTL, tBR, tExceptions)
			self.convertSurroundingPlotCulture(iPlayer, tTL, tBR, tExceptions)


        def prepareChina(self):
                pGuiyang = gc.getMap().plot(102, 41)
                pGuiyang.getPlotCity().kill()
                pGuiyang.setImprovementType(-1)
                pGuiyang.setRouteType(-1)
                pGuiyang.setFeatureType(con.iForest, 0)

		if utils.getScenario() == con.i600AD:
			pXian = gc.getMap().plot(100, 44)
			pXian.getPlotCity().kill()
			pXian.setImprovementType(-1)
			pXian.setRouteType(-1)
			pXian.setFeatureType(con.iForest, 0)
			
		if utils.getScenario() == con.i1700AD:
			pBeijing = gc.getMap().plot(con.tBeijing[0], con.tBeijing[1])
			pBeijing.getPlotCity().kill()
			pBeijing.setImprovementType(-1)
			pBeijing.setRouteType(-1)

                tCultureRegionTL = (98, 37)
                tCultureRegionBR = (109, 49)
                for x in range(tCultureRegionTL[0], tCultureRegionBR[0]+1):       
                        for y in range(tCultureRegionTL[1], tCultureRegionBR[1]+1):     
                                pCurrent = gc.getMap().plot(x, y)
                                bCity = False
                                for iX in range(x-1, x+2):        # from x-1 to x+1
                                        for iY in range(y-1, y+2):      # from y-1 to y+1
                                                loopPlot = gc.getMap().plot(iX, iY)
                                                if (loopPlot.isCity()):
                                                     bCity = True
                                                     loopPlot.getPlotCity().setCulture(iIndependent2, 0, False)
                                if (bCity):                                
                                        pCurrent.setCulture(iIndependent2, 1, True)
                                else:
                                        pCurrent.setCulture(iIndependent2, 0, True)
                                        pCurrent.setOwner(-1)
					
		pIndependent.found(99, 41)
		utils.makeUnit(con.iArcher, iIndependent, (99, 41), 1)
		pChengdu = gc.getMap().plot(99, 41).getPlotCity()
		pChengdu.setName("Chengdu", False)
		pChengdu.setPopulation(2)
		pChengdu.setHasReligion(con.iConfucianism, True, False, False)
		pChengdu.setHasRealBuilding(con.iGranary, True)
		
		if utils.getScenario() == con.i600AD:
			pBarbarian.found(105, 49)
			utils.makeUnit(con.iArcher, iBarbarian, (105, 49), 1)
			pShenyang = gc.getMap().plot(105, 49).getPlotCity()
			pShenyang.setName("Simiyan hoton", False)
			pShenyang.setPopulation(2)
			pShenyang.setHasReligion(con.iConfucianism, True, False, False)
			pShenyang.setHasRealBuilding(con.iGranary, True)
			pShenyang.setHasRealBuilding(con.iWalls, True)
			pShenyang.setHasRealBuilding(con.iConfucianTemple, True)

        def setupBirthTurnModifiers(self):
                for iCiv in range(iNumPlayers):
                        if (iCiv >= iGreece and not gc.getPlayer(iCiv).isHuman()):
                                self.setBirthTurnModifier(iCiv, (gc.getGame().getSorenRandNum(11, 'BirthTurnModifier') - 5)) # -5 to +5
                #now make sure that no civs spawn in the same turn and cause a double "new civ" popup
                for iCiv in range(iNumPlayers):
                        if (iCiv > utils.getHumanID() and iCiv < iAmerica):
                                for j in range(iNumPlayers-1-iCiv):
                                        iNextCiv = iCiv+j+1
                                        if (getTurnForYear(con.tBirth[iCiv])+self.getBirthTurnModifier(iCiv) == getTurnForYear(con.tBirth[iNextCiv])+self.getBirthTurnModifier(iNextCiv)):
                                                self.setBirthTurnModifier(iNextCiv, (self.getBirthTurnModifier(iNextCiv)+1))
						
	def placeGoodyHuts(self):
			
		if utils.getScenario() == con.i3000BC:
			self.placeHut((101, 38), (107, 41)) # Southern China
			self.placeHut((62, 45), (67, 50)) # Balkans
			self.placeHut((69, 42), (76, 46)) # Asia Minor
		
		if utils.getScenario() <= con.i600AD:
			self.placeHut((49, 40), (54, 46)) # Iberia
			self.placeHut((57, 51), (61, 56)) # Denmark / Northern Germany
			self.placeHut((48, 55), (49, 58)) # Ireland
			self.placeHut((50, 53), (54, 60)) # Britain
			self.placeHut((57, 57), (65, 65)) # Scandinavia
			self.placeHut((73, 53), (81, 58)) # Russia
			self.placeHut((81, 43), (86, 47)) # Transoxania
			self.placeHut((88, 30), (94, 36)) # Deccan
			self.placeHut((110, 40), (113, 43)) # Shikoku
			self.placeHut((114, 49), (116, 52)) # Hokkaido
			self.placeHut((85, 53), (99, 59)) # Siberia
			self.placeHut((103, 24), (109, 29)) # Indonesia
			self.placeHut((68, 17), (72, 23)) # East Africa
			self.placeHut((65, 10), (70, 16)) # South Africa
			self.placeHut((22, 48), (29, 51)) # Great Lakes
			self.placeHut((18, 44), (22, 52)) # Great Plains
			self.placeHut((34, 25), (39, 29)) # Amazonas Delta
			self.placeHut((33, 9), (37, 15)) # Parana Delta
			self.placeHut((25, 36), (32, 39)) # Caribbean
		
		self.placeHut((107, 19), (116, 22)) # Northern Australia
		self.placeHut((114, 10), (118, 17)) # Western Australia
		self.placeHut((120, 5), (123, 11)) # New Zealand
		self.placeHut((59, 25), (67, 28)) # Central Africa
                                            
        def checkTurn(self, iGameTurn):
	
		# Leoreth: randomly place goody huts
		if iGameTurn == utils.getScenarioStartTurn()+3:
			self.placeGoodyHuts()
		
		if iGameTurn == getTurnForYear(con.tBirth[iSpain])-1:
			if utils.getScenario() == con.i600AD:
				pMassilia = gc.getMap().plot(56, 46)
				if pMassilia.isCity():
					pMassilia.getPlotCity().setCulture(pMassilia.getPlotCity().getOwner(), 1, True)

		#Leoreth: Turkey immediately flips Seljuk or independent cities in its core to avoid being pushed out of Anatolia
		if iGameTurn == sd.scriptDict['iOttomanSpawnTurn']+1:
			dummy, cityPlotList = utils.squareSearch(con.tCoreAreasTL[0][iTurkey], con.tCoreAreasBR[0][iTurkey], utils.cityPlots, -1)
			for tPlot in cityPlotList:
				x, y = tPlot
				city = gc.getMap().plot(x, y).getPlotCity()
				iOwner = city.getOwner()
				if iOwner in [iSeljuks, iIndependent, iIndependent2]:
                               		utils.flipCity(tPlot, False, True, iTurkey, ())
                               		utils.cultureManager(tPlot, 100, iTurkey, iOwner, True, False, False)
                               		self.convertSurroundingPlotCulture(iTurkey, (tPlot[0]-1,tPlot[1]-1), (tPlot[0]+1,tPlot[1]+1))
					utils.makeUnit(con.iLongbowman, iTurkey, tPlot, 1)
			                
                #Trigger betrayal mode
                if (self.getBetrayalTurns() > 0):
                        self.initBetrayal()

                if (self.getCheatersCheck(0) > 0):
                        teamPlayer = gc.getTeam(gc.getPlayer(utils.getHumanID()).getTeam())
                        if (teamPlayer.isAtWar(self.getCheatersCheck(1))):
                                print ("No cheaters!")
                                self.initMinorBetrayal(self.getCheatersCheck(1))
                                self.setCheatersCheck(0, 0)
                                self.setCheatersCheck(1, -1)
                        else:
                                self.setCheatersCheck(0, self.getCheatersCheck(0)-1)

                if (iGameTurn % utils.getTurns(20) == 0):
                        if (pIndependent.isAlive()):                                  
                                utils.updateMinorTechs(iIndependent, iBarbarian)
                        if (pIndependent2.isAlive()):                                  
                                utils.updateMinorTechs(iIndependent2, iBarbarian)
			if pSeljuks.isAlive():
				utils.updateMinorTechs(iSeljuks, iBarbarian)

                #Leoreth: give Phoenicia a settler in Qart-Hadasht in 820BC
                if (not pCarthage.isHuman() and iGameTurn == getTurnForYear(-820) - (utils.getSeed() % 10)):
                        utils.makeUnit(con.iSettler, iCarthage, (58, 39), 1)
                        utils.makeUnit(con.iArcher, iCarthage, (58, 39), 2)
                        utils.makeUnit(con.iWorker, iCarthage, (58, 39), 2)
                        utils.makeUnit(con.iCarthaginianWarElephant, iCarthage, (58, 39), 2)
			
		if iGameTurn == getTurnForYear(476):
			if pItaly.isHuman() and pRome.isAlive():
				sta.completeCollapse(iRome)
				#utils.killAndFragmentCiv(iRome, iIndependent, iIndependent2, -1, False)
				
		if iGameTurn == getTurnForYear(-50):
			if pByzantium.isHuman() and pGreece.isAlive():
				sta.completeCollapse(iGreece)
				#utils.killAndFragmentCiv(iGreece, iIndependent, iIndependent2, -1, False)
			
                #Colonists
                if (iGameTurn == getTurnForYear(-850)):
                        self.giveEarlyColonists(iGreece)
                if (iGameTurn == getTurnForYear(-700)): # removed their colonists because of the Qart-Hadasht spawn
                        self.giveEarlyColonists(iCarthage)
			
		if iGameTurn == getTurnForYear(-600):
			self.giveEarlyColonists(iRome)
		if iGameTurn == getTurnForYear(-400):
			self.giveEarlyColonists(iRome)
 
                if (iGameTurn >= getTurnForYear(860) and iGameTurn <= getTurnForYear(1250)):
                        if (iGameTurn % utils.getTurns(10) == 9):
                                self.giveRaiders(iVikings, tBroaderAreasTL[utils.getReborn(iVikings)][iVikings], tBroaderAreasBR[utils.getReborn(iVikings)][iVikings])
                               
                if (iGameTurn >= getTurnForYear(1350) and iGameTurn <= getTurnForYear(1918)):
			for iPlayer in [iSpain, iEngland, iFrance, iPortugal, iNetherlands, iVikings, iGermany]:
				if iGameTurn == self.getAstronomyTurn(iPlayer) + 1 + self.getColonistsAlreadyGiven(iPlayer)*8:
					self.giveColonists(iPlayer)
					
		if iGameTurn == getTurnForYear(710)-1:
			x, y = 51, 37
			if gc.getMap().plot(x,y).isCity():
				marrakesh = gc.getMap().plot(x,y).getPlotCity()
				marrakesh.setHasReligion(con.iIslam, True, False, False)
				
				utils.makeUnit(con.iSettler, marrakesh.getOwner(), (x,y), 1)
				utils.makeUnit(con.iWorker, marrakesh.getOwner(), (x,y), 1)
				
		# Leoreth: help human with Aztec UHV - prevent super London getting in the way
		if iGameTurn == getTurnForYear(1500) and utils.getHumanID() == iAztecs:
			plot = gc.getMap().plot(con.tCapitals[iEngland][0], con.tCapitals[iEngland][1])
			if plot.isCity():
				city = plot.getPlotCity()
				if city.getPopulation() > 14:
					city.changePopulation(-3)
				
		if iGameTurn == getTurnForYear(1040):	# Leoreth: first Seljuk wave (flips independents, spawns armies for players)
			tEsfahan = utils.getFreePlot(81, 41)
			esfahan = gc.getMap().plot(tEsfahan[0], tEsfahan[1])
			if esfahan.isCity():
				utils.flipCity(tEsfahan, False, True, iSeljuks, ())
			else:
				pSeljuks.found(tEsfahan[0], tEsfahan[1])
				esfahan.getPlotCity().setName('Isfahan', False)
			utils.makeUnitAI(con.iLongbowman, iSeljuks, tEsfahan, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(con.iIslamicMissionary, iSeljuks, tEsfahan, 1)
			utils.makeUnit(con.iWorker, iSeljuks, tEsfahan, 3)
			utils.cultureManager(tEsfahan, 100, iSeljuks, esfahan.getOwner(), True, False, False)
			for i in range(tEsfahan[0]-1, tEsfahan[0]+2):
				for j in range(tEsfahan[1]-1, tEsfahan[1]+2):
			               	pCurrent = gc.getMap().plot( i, j )
        		                if (not pCurrent.isCity()):
                	        		utils.convertPlotCulture(pCurrent, iSeljuks, 100, False)
						
			utils.updateMinorTechs(iSeljuks, iBarbarian)

			tSeljukAreaTL = (78, 37)
			tSeljukAreaBR = (85, 46)
			targetCityList = []
			targetPlayerList = []
			dummy, lCityPlotList = utils.squareSearch(tSeljukAreaTL, tSeljukAreaBR, utils.cityPlots, -1)
			for tPlot in lCityPlotList:
				x, y = tPlot
				city = gc.getMap().plot(x, y).getPlotCity()
				if city.getOwner() in [iIndependent, iIndependent2]:
                                	utils.flipCity(tPlot, False, True, iSeljuks, ())
                                	utils.cultureManager(tPlot, 100, iSeljuks, city.getOwner(), True, False, False)
					utils.makeUnitAI(con.iLongbowman, iSeljuks, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
					for i in range(x-1, x+2):
						for j in range(y-1, y+2):
			                                pCurrent = gc.getMap().plot( x, y )
        			                        if (not pCurrent.isCity()):
                	        		                utils.convertPlotCulture(pCurrent, iSeljuks, 100, False)
				else:
					targetCityList.append(tPlot)
					targetPlayerList.append(city.getOwner())
			
			for tPlot in targetCityList:
				tSpawnPlot = utils.getFreeNeighborPlot(tPlot)
				utils.makeUnitAI(con.iSeljukGhulamWarrior, iSeljuks, tSpawnPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
				utils.makeUnitAI(con.iTrebuchet, iSeljuks, tSpawnPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
				utils.makeUnitAI(con.iMaceman, iSeljuks, tSpawnPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
				utils.makeUnitAI(con.iLongbowman, iSeljuks, tSpawnPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			
			for iPlayer in targetPlayerList:
                                teamSeljuks.declareWar(iPlayer, True, WarPlanTypes.WARPLAN_TOTAL)
			if utils.getHumanID() in con.lCivGroups[2]:
				CyInterface().addMessage(CyGame().getActivePlayer(), True , con.iDuration, CyTranslator().getText("TXT_KEY_SELJUK_HORDES", ()), "", 1 , "", ColorTypes(con.iRed),0,0,False,False)

		if iGameTurn == getTurnForYear(1070 + utils.getSeed()%10 - 5): #Linkman226- Seljuks
                        tSpawnPlots = ((77,41), (74, 43), (72, 44))
                        for plot in tSpawnPlots:
				spawnPlot = utils.getFreePlot(plot[0], plot[1])
                                utils.makeUnitAI(con.iSeljukGhulamWarrior, iSeljuks, spawnPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
                                utils.makeUnitAI(con.iSeljukGhulamWarrior, iSeljuks, spawnPlot, UnitAITypes.UNITAI_ATTACK, 3)
                                utils.makeUnitAI(con.iTrebuchet, iSeljuks, spawnPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
                                pSeljuks.setLastStateReligion(con.iIslam)
				teamSeljuks.declareWar(iByzantium, True, WarPlanTypes.WARPLAN_TOTAL)

		if iGameTurn == getTurnForYear(1230 + utils.getSeed()%10): #Linkman226- Mongol Conquerors for Seljuks
		
			# let Seljuk army decay for everyone
			lSeljukUnits = [pSeljuks.getUnit(i) for i in range(pSeljuks.getNumUnits())]
			
			lUnitsToRemove = []
			for unit in lSeljukUnits:
				if unit.getUnitType() == con.iSeljukGhulamWarrior:
					if gc.getGame().getSorenRandNum(2, 'Delete unit') != 0:
						lUnitsToRemove.append(unit)
						
			for unit in lUnitsToRemove:
				unit.kill(False, con.iBarbarian)
		
			if pSeljuks.isAlive() and utils.getHumanID() != iMongolia:
                        	tPlot = utils.getFreePlot(84, 46)
				targetAreaTL = (73, 38)
				targetAreaBR = (85, 46)
				count = 0
				dummy, lCityPlotList = utils.squareSearch(targetAreaTL, targetAreaBR, utils.cityPlots, -1)

				for tPlot in lCityPlotList:
					x, y = tPlot
					if gc.getMap().plot(x, y).getPlotCity().getOwner() == iSeljuks:
						count += 1

				if count <= 2:
					iModifier = 0
				elif count >= len(lCityPlotList)-2:
					iModifier = 2
				else:
					iModifier = 1
					
				spawnPlot = utils.getFreeNeighborPlot(tPlot)

                        	utils.makeUnitAI(con.iMongolKeshik, iMongolia, spawnPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 + iModifier)
				utils.makeUnitAI(con.iHorseArcher, iMongolia, spawnPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1 + iModifier)
				utils.makeUnitAI(con.iTrebuchet, iMongolia, spawnPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
				if utils.getHumanID() in con.lCivGroups[1]:
					CyInterface().addMessage(utils.getHumanID(), True, con.iDuration, CyTranslator().getText("TXT_KEY_MONGOL_HORDE", (gc.getPlayer(iSeljuks).getCivilizationAdjectiveKey(),)), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
                if iGameTurn == getTurnForYear(1230 + utils.getSeed()%10 + 3): #Linkman226- Mongol Conquerors for Seljuks
			if pSeljuks.isAlive() and utils.getHumanID() != iMongolia:
                        	tPlot = utils.getFreeNeighborPlot((83, 42))
                        	utils.makeUnitAI(con.iMongolKeshik, iMongolia, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
				utils.makeUnitAI(con.iHorseArcher, iMongolia, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
				utils.makeUnitAI(con.iTrebuchet, iMongolia, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
				
				
		# Leoreth: make sure Aztecs are dead in 1700 if a civ that spawns from that point is selected
		if iGameTurn == getTurnForYear(1700)-2:
			if utils.getHumanID() >= iGermany and pAztecs.isAlive():
				sta.completeCollapse(iAztecs)
				#utils.killAndFragmentCiv(iAztecs, iIndependent, iIndependent2, -1, False)
				
				
                if utils.getScenario() == con.i3000BC:
                        iFirstSpawn = iGreece
                elif utils.getScenario() == con.i600AD:
                        iFirstSpawn = iArabia
		else:
			iFirstSpawn = iAmerica
			
                for iLoopCiv in range(iFirstSpawn, iNumMajorPlayers):
                        if (iGameTurn >= getTurnForYear(con.tBirth[iLoopCiv]) - 2 and iGameTurn <= getTurnForYear(con.tBirth[iLoopCiv]) + 6):
                                self.initBirth(iGameTurn, con.tBirth[iLoopCiv], iLoopCiv)



                if (iGameTurn == getTurnForYear(600)):
                        if utils.getScenario() == con.i600AD:  #late start condition
                                print ("late start")
				if utils.getHumanID() != iChina:
					tTopLeft = (99, 39) # 4 tiles further south
				else:
					tTopLeft = tCoreAreasTL[0][iChina]
                                iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iChina, tTopLeft, tCoreAreasBR[0][iChina])
                                self.convertSurroundingPlotCulture(iChina, tTopLeft, tCoreAreasBR[0][iChina])
                                utils.flipUnitsInArea(tTopLeft, tCoreAreasBR[0][iChina], iChina, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ   
                                utils.flipUnitsInArea(tTopLeft, tCoreAreasBR[0][iChina], iChina, iIndependent, False, False) #remaining independents in the region now belong to the new civ   
                                utils.flipUnitsInArea(tTopLeft, tCoreAreasBR[0][iChina], iChina, iIndependent2, False, False) #remaining independents in the region now belong to the new civ

				
                #kill the remaining barbs in the region: it's necessary to do this more than once to protect those civs
                if (iGameTurn >= getTurnForYear(con.tBirth[iVikings])+2 and iGameTurn <= getTurnForYear(con.tBirth[iVikings])+utils.getTurns(10)):
                        utils.killUnitsInArea(tCoreAreasTL[utils.getReborn(iVikings)][iVikings], tCoreAreasBR[utils.getReborn(iVikings)][iVikings], iBarbarian)
                if (iGameTurn >= getTurnForYear(con.tBirth[iSpain])+2 and iGameTurn <= getTurnForYear(con.tBirth[iSpain])+utils.getTurns(10)):
                        utils.killUnitsInArea(tCoreAreasTL[utils.getReborn(iSpain)][iSpain], tCoreAreasBR[utils.getReborn(iSpain)][iSpain], iBarbarian)
                if (iGameTurn >= getTurnForYear(con.tBirth[iFrance])+2 and iGameTurn <= getTurnForYear(con.tBirth[iFrance])+utils.getTurns(10)):
                        utils.killUnitsInArea(tCoreAreasTL[utils.getReborn(iFrance)][iFrance], tCoreAreasBR[utils.getReborn(iFrance)][iFrance], iBarbarian)
                if (iGameTurn >= getTurnForYear(con.tBirth[iGermany])+2 and iGameTurn <= getTurnForYear(con.tBirth[iGermany])+utils.getTurns(10)):
                        utils.killUnitsInArea(tCoreAreasTL[utils.getReborn(iGermany)][iGermany], tCoreAreasBR[utils.getReborn(iGermany)][iGermany], iBarbarian)
                if (iGameTurn >= getTurnForYear(con.tBirth[iRussia])+2 and iGameTurn <= getTurnForYear(con.tBirth[iRussia])+utils.getTurns(10)):
                        utils.killUnitsInArea(tCoreAreasTL[utils.getReborn(iRussia)][iRussia], tCoreAreasBR[utils.getReborn(iRussia)][iRussia], iBarbarian)
                        
                #fragment utility
                if (iGameTurn >= getTurnForYear(50) and iGameTurn % utils.getTurns(15) == 6):
                        self.fragmentIndependents()
#                if (iGameTurn >= getTurnForYear(450) and iGameTurn % utils.getTurns(30) == 12):
#                        self.fragmentBarbarians(iGameTurn)
                        
                #fall of civs
                #if (iGameTurn >= getTurnForYear(200) and iGameTurn % utils.getTurns(4) == 0):
                #        self.collapseByBarbs(iGameTurn)                                        
                #if (iGameTurn >= getTurnForYear(-2000) and iGameTurn % utils.getTurns(18) == 0): #used to be 15 in vanilla, because we must give some time for vassal states to form
                #        self.collapseGeneric(iGameTurn)
                #if (iGameTurn >= getTurnForYear(-2000) and iGameTurn % utils.getTurns(13) == 7): #used to be 8 in vanilla, because we must give some time for vassal states to form
                #        self.collapseMotherland(iGameTurn)
                if (iGameTurn > getTurnForYear(300) and iGameTurn % utils.getTurns(10) == 6):
                        self.secession(iGameTurn)

		if iGameTurn % utils.getTurns(15) == 10:
			sta.checkResurrection(iGameTurn)
			
		# Leoreth: check for scripted rebirths
		for iCiv in range(con.iNumPlayers):
			if con.tRebirth[iCiv] != -1:
				if iGameTurn == getTurnForYear(con.tRebirth[iCiv]) and not gc.getPlayer(iCiv).isAlive():
					self.rebirthFirstTurn(iCiv)
				if iGameTurn == getTurnForYear(con.tRebirth[iCiv])+1 and gc.getPlayer(iCiv).isAlive() and utils.isReborn(iCiv):
					self.rebirthSecondTurn(iCiv)

	def rebirthFirstTurn(self, iCiv):
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		if con.tRebirthCiv[iCiv] != -1:
			pCiv.setCivilizationType(con.tRebirthCiv[iCiv])
		x, y = con.tRebirthPlot[iCiv]
		plot = gc.getMap().plot(x,y)
		
		# disable Mexico and Colombia
		if iCiv == iAztecs and gc.getDefineINT("PLAYER_REBIRTH_MEXICO") == 0: return
		if iCiv == iMaya and gc.getDefineINT("PLAYER_REBIRTH_COLOMBIA") == 0: return
		
		# reset contacts
		for iOtherCiv in range(con.iNumPlayers):
			if iCiv != iOtherCiv:
				teamCiv.cutContact(iOtherCiv)
		
		# reset diplomacy
		pCiv.AI_reset()
		
		# reset map visibility
		for i in range(gc.getMap().getGridWidth()):
			for j in range(gc.getMap().getGridHeight()):
				gc.getMap().plot(i, j).setRevealed(iCiv, False, True, -1)
		
		# assign new leader
		if iCiv in con.rebirthLeaders:
			if pCiv.getLeader() != con.rebirthLeaders[iCiv]:
				pCiv.setLeader(con.rebirthLeaders[iCiv])

		CyInterface().addMessage(gc.getGame().getActivePlayer(), True, con.iDuration, (CyTranslator().getText("TXT_KEY_INDEPENDENCE_TEXT", (pCiv.getCivilizationAdjectiveKey(),))), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
		pCiv.setReborn()
		
		# Determine whether capital location is free
		bFree = True
		for i in range(x-1,x+2):
			for j in range(y-1,y+2):
				if gc.getMap().plot(i,j).isCity():
					bFree = False

		if plot.getNumUnits() > 0:
			bFree = False

		# if city present, flip it. If plot is free, found it. Else give settler.
		if plot.isCity():
			utils.completeCityFlip(x, y, iCiv, plot.getPlotCity().getOwner(), 100)
		else:
			utils.convertPlotCulture(plot, iCiv, 100, True)
			if bFree:
				pCiv.found(x,y)
			else:
				utils.makeUnit(con.iSettler, iCiv, (x,y), 1)
				
		# make sure there is a palace in the city
		if plot.isCity():
			capital = plot.getPlotCity()
			if not capital.hasBuilding(con.iPalace):
				capital.setHasRealBuilding(con.iPalace, True)
		
		self.createRespawnUnits(iCiv, (x,y))
		
		# for colonial civs, set dynamic state religion
		if iCiv in [iAztecs, iMaya]:
			self.setStateReligion(iCiv)

		self.assignTechs(iCiv)
		if (gc.getGame().getGameTurn() >= getTurnForYear(con.tBirth[gc.getGame().getActivePlayer()])):
			self.respawnPopup(iCiv)

		self.setLatestRebellionTurn(iCiv, getTurnForYear(con.tRebirth[iCiv]))
		
		dc.onCivRespawn(iCiv, [])
		
	def rebirthSecondTurn(self, iCiv):
		tTopLeft = con.tRebirthArea[iCiv][0]
		tBottomRight = con.tRebirthArea[iCiv][1]
		tExceptions = ()
		if iCiv in con.dRebirthExceptions: tExceptions = con.dRebirthExceptions[iCiv]
		
		lRebirthPlots = utils.getPlotList(tTopLeft, tBottomRight, tExceptions)
		
		# exclude American territory for Mexico
		if iCiv == iAztecs:
			for tPlot in lRebirthPlots:
				x, y = tPlot
				plot = gc.getMap().plot(x, y)
				if plot.getOwner() == iAmerica and not utils.isPlotInArea(tPlot, con.tCoreAreasTL[1][iAztecs], con.tCoreAreasBR[1][iAztecs], con.tExceptions[1][iAztecs]):
					tExceptions += (tPlot,)
		
		seljukUnits = []
		lCities = []
		for tPlot in lRebirthPlots:
			x, y = tPlot
			plot = gc.getMap().plot(x, y)
			for i in range(plot.getNumUnits()):
				unit = plot.getUnit(i)
				if unit.getOwner() == con.iSeljuks:
					seljukUnits.append(unit)
					
			if plot.isCity():
				lCities.append(plot.getPlotCity())
					
		for unit in seljukUnits:
			unit.kill(False, con.iBarbarian)
			
		# remove garrisons
		for city in lCities:
			if city.getOwner() != utils.getHumanID():
				x = city.getX()
				y = city.getY()
				utils.relocateGarrisons((x,y), city.getOwner())
				utils.relocateSeaGarrisons((x,y), city.getOwner())
				#utils.createGarrisons((x,y), iCiv)
				
		# convert cities
		iConvertedCities, iHumanCities = self.convertSurroundingCities(iCiv, tTopLeft, tBottomRight, tExceptions)
		
		# create garrisons
		for city in lCities:
			if city.getOwner() == utils.getHumanID():
				x = city.getX()
				y = city.getY()
				utils.createGarrisons((x, y), iCiv, 1)
				
		# convert plot culture
		self.convertSurroundingPlotCulture(iCiv, tTopLeft, tBottomRight, tExceptions)
		
		# reset plague
		utils.setPlagueCountdown(iCiv, -10)
		utils.clearPlague(iCiv)
		
		# adjust starting stability
		sd.setStabilityLevel(iCiv, con.iStabilityStable)
		
		# ask human player for flips
		if iHumanCities > 0 and iCiv != utils.getHumanID():
			self.flipPopup(iCiv, tTopLeft, tBottomRight)

		# adjust civics, religion and other special settings
		if iCiv == iRome:
			if gc.getMap().plot(61,47).isCity():
				pVenice = gc.getMap().plot(61,47).getPlotCity()
				pVenice.setCulture(iRome, 100, True)
				pVenice.setPopulation(4)
				utils.makeUnit(con.iGalley, iRome, (pVenice.plot().getX(), pVenice.plot().getY()), 2)
			pRome.setLastStateReligion(con.iChristianity)
			pRome.setCivics(0, con.iCivicCityStates)
			pRome.setCivics(1, con.iCivicAbsolutism)
			pRome.setCivics(2, con.iCivicAgrarianism)
			pRome.setCivics(3, con.iCivicGuilds)
			pRome.setCivics(4, con.iCivicOrganizedReligion)
			pRome.setCivics(5, con.iCivicMercenaries)
		elif iCiv == iPersia:
			pPersia.setLastStateReligion(con.iIslam)
			pPersia.setCivics(0, con.iCivicDynasticism)
			pPersia.setCivics(1, con.iCivicAbsolutism)
			pPersia.setCivics(2, con.iCivicSlavery)
			pPersia.setCivics(3, con.iCivicGuilds)
			pPersia.setCivics(4, con.iCivicFanaticism)
			pPersia.setCivics(5, con.iCivicLevyArmies)
		elif iCiv == iAztecs:
			if gc.getMap().plot(18, 37).isCity() and gc.getGame().getBuildingClassCreatedCount(gc.getBuildingInfo(con.iFloatingGardens).getBuildingClassType()) == 0:
				gc.getMap().plot(18, 37).getPlotCity().setHasRealBuilding(con.iFloatingGardens, True)
			
			cnm.updateCityNamesFound(iAztecs) # use name of the plots in their city name map
			
			pAztecs.setCivics(0, con.iCivicRepublic)
			pAztecs.setCivics(1, con.iCivicRepresentation)
			pAztecs.setCivics(2, con.iCivicCapitalism)
			pAztecs.setCivics(3, con.iCivicMercantilism)
			pAztecs.setCivics(4, con.iCivicOrganizedReligion)
			pAztecs.setCivics(5, con.iCivicStandingArmy)
		elif iCiv == iMaya:
			pMaya.setCivics(0, con.iCivicAutocracy)
			pMaya.setCivics(1, con.iCivicRepresentation)
			pMaya.setCivics(2, con.iCivicCapitalism)
			pMaya.setCivics(3, con.iCivicMercantilism)
			pMaya.setCivics(4, con.iCivicOrganizedReligion)
			pMaya.setCivics(5, con.iCivicConscription)
			gc.getMap().plot(28, 31).setFeatureType(-1, 0)

        def checkPlayerTurn(self, iGameTurn, iPlayer):
		return

        def fragmentIndependents(self):

                if (pIndependent.getNumCities() > 8 or pIndependent2.getNumCities() > 8 ):
                        iBigIndependent = -1
                        iSmallIndependent = -1
                        if (pIndependent.getNumCities() > 2*pIndependent2.getNumCities()):
                                iBigIndependent = iIndependent
                                iSmallIndependent = iIndependent2
                        if (2*pIndependent.getNumCities() < 2*pIndependent2.getNumCities()):
                                iBigIndependent = iIndependent2
                                iSmallIndependent = iIndependent
                        if (iBigIndependent != -1):
                                iDivideCounter = 0
                                iCounter = 0
                                cityList = []
                                apCityList = PyPlayer(iBigIndependent).getCityList()
                                for pCity in apCityList:
                                        iDivideCounter += 1 #convert 3 random cities cycling just once
                                        if (iDivideCounter % 2 == 1):
                                                city = pCity.GetCy()
                                                pCurrent = gc.getMap().plot(city.getX(), city.getY())                                        
                                                utils.cultureManager((city.getX(),city.getY()), 50, iSmallIndependent, iBigIndependent, False, True, True)
                                                utils.flipUnitsInCityBefore((city.getX(),city.getY()), iSmallIndependent, iBigIndependent)                            
                                                self.setTempFlippingCity((city.getX(),city.getY()))
                                                utils.flipCity((city.getX(),city.getY()), 0, 0, iSmallIndependent, [iBigIndependent])   #by trade because by conquest may raze the city
                                                utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iSmallIndependent)
                                                iCounter += 1
                                                if (iCounter == 3):
                                                        return



        def fragmentBarbarians(self, iGameTurn):

                iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
                for j in range(iRndnum, iRndnum + iNumPlayers):
                        iDeadCiv = j % iNumPlayers                                                        
                        if (not gc.getPlayer(iDeadCiv).isAlive() and iGameTurn > getTurnForYear(con.tBirth[iDeadCiv]) + utils.getTurns(50)):
                                pDeadCiv = gc.getPlayer(iDeadCiv)
                                teamDeadCiv = gc.getTeam(pDeadCiv.getTeam())
                                iCityCounter = 0
                                for x in range(tNormalAreasTL[utils.getReborn(iDeadCiv)][iDeadCiv][0], tNormalAreasBR[utils.getReborn(iDeadCiv)][iDeadCiv][0]+1):
                                        for y in range(tNormalAreasTL[utils.getReborn(iDeadCiv)][iDeadCiv][1], tNormalAreasBR[utils.getReborn(iDeadCiv)][iDeadCiv][1]+1):
                                                pCurrent = gc.getMap().plot( x, y )
                                                if ( pCurrent.isCity()):
                                                        if (pCurrent.getPlotCity().getOwner() == iBarbarian):
                                                                iCityCounter += 1
                                if (iCityCounter > 3):
                                        iDivideCounter = 0
                                        for x in range(tNormalAreasTL[utils.getReborn(iDeadCiv)][iDeadCiv][0], tNormalAreasBR[utils.getReborn(iDeadCiv)][iDeadCiv][0]+1):
                                                for y in range(tNormalAreasTL[utils.getReborn(iDeadCiv)][iDeadCiv][1], tNormalAreasBR[utils.getReborn(iDeadCiv)][iDeadCiv][1]+1):
                                                        pCurrent = gc.getMap().plot( x, y )
                                                        if ( pCurrent.isCity()):
                                                                city = pCurrent.getPlotCity()
                                                                if (city.getOwner() == iBarbarian):
                                                                        if (iDivideCounter % 4 == 0):
                                                                                iNewCiv = iIndependent
                                                                        elif (iDivideCounter % 4 == 1):
                                                                                iNewCiv = iIndependent2
                                                                        if (iDivideCounter % 4 == 0 or iDivideCounter % 4 == 1):
                                                                                utils.cultureManager((city.getX(),city.getY()), 50, iNewCiv, iBarbarian, False, True, True)
                                                                                utils.flipUnitsInCityBefore((city.getX(),city.getY()), iNewCiv, iBarbarian)                            
                                                                                self.setTempFlippingCity((city.getX(),city.getY()))
                                                                                utils.flipCity((city.getX(),city.getY()), 0, 0, iNewCiv, [iBarbarian])   #by trade because by conquest may raze the city
                                                                                utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
                                                                                iDivideCounter += 1
                                        return
                

        def secession(self, iGameTurn):
            
                iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
                for j in range(iRndnum, iRndnum + iNumPlayers):
                        iPlayer = j % iNumPlayers   
                        if (gc.getPlayer(iPlayer).isAlive() and iGameTurn >= getTurnForYear(con.tBirth[iPlayer]) + utils.getTurns(30)):
				
				if sd.getStabilityLevel(iPlayer) == con.iStabilityCollapsing:

                                        cityList = []
                                        apCityList = PyPlayer(iPlayer).getCityList()
                                        for pCity in apCityList:
                                                city = pCity.GetCy()
                                                pCurrent = gc.getMap().plot(city.getX(), city.getY())

                                                if ((not city.isWeLoveTheKingDay()) and (not city.isCapital()) and (not (city.getX() == tCapitals[utils.getReborn(iPlayer)][iPlayer][0] and city.getY() == tCapitals[utils.getReborn(iPlayer)][iPlayer][1]))):
                                                        if (gc.getPlayer(iPlayer).getNumCities() > 0): #this check is needed, otherwise game crashes
                                                                capital = gc.getPlayer(iPlayer).getCapitalCity()
                                                                iDistance = utils.calculateDistance(city.getX(), city.getY(), capital.getX(), capital.getY())
                                                                if (iDistance > 3):                                                                                               
                                                            
                                                                        if (city.angryPopulation(0) > 0 or \
                                                                            city.healthRate(False, 0) < 0 or \
                                                                            city.getReligionBadHappiness() > 0 or \
                                                                            city.getLargestCityHappiness() < 0 or \
                                                                            city.getHurryAngerModifier() > 0 or \
                                                                            city.getNoMilitaryPercentAnger() > 0 or \
                                                                            city.getWarWearinessPercentAnger() > 0):
                                                                                cityList.append(city)
                                                                                continue
                                                                        
                                                                        for iLoop in range(iNumTotalPlayers+1):
                                                                                if (iLoop != iPlayer):
                                                                                        if (pCurrent.getCulture(iLoop) > 0):
                                                                                                cityList.append(city)
                                                                                                break
												
					# Leoreth: Byzantine UP: cities in normal area are immune to secession
					if iPlayer == iByzantium:
						tlx, tly = con.tCoreAreasTL[utils.getReborn(iByzantium)][iByzantium]
						brx, bry = con.tCoreAreasBR[utils.getReborn(iByzantium)][iByzantium]
						for city in cityList:
							x = city.getX()
							y = city.getY()
							if x >= tlx and x <= brx and y >= tly and y <= bry and (x,y) not in con.tNormalAreasSubtract[utils.getReborn(iByzantium)][iByzantium]:
								cityList.remove(city)

                                        if (len(cityList)):
                                                iNewCiv = iIndependent
                                                iRndNum = gc.getGame().getSorenRandNum(2, 'random independent')
                                                if (iRndNum % 2 == 0):
                                                        iNewCiv = iIndependent2  
                                                if (iPlayer == con.iAztecs or \
                                                    iPlayer == con.iInca or \
                                                    iPlayer == con.iMaya or \
                                                    iPlayer == con.iEthiopia or \
                                                    iPlayer == con.iMali):
                                                        if (utils.getCivsWithNationalism() <= 0):
                                                                iNewCiv = iNative                    
                                                splittingCity = cityList[gc.getGame().getSorenRandNum(len(cityList), 'random city')]
                                                utils.cultureManager((splittingCity.getX(),splittingCity.getY()), 50, iNewCiv, iPlayer, False, True, True)
                                                utils.flipUnitsInCityBefore((splittingCity.getX(),splittingCity.getY()), iNewCiv, iPlayer)                            
                                                self.setTempFlippingCity((splittingCity.getX(),splittingCity.getY()))
                                                utils.flipCity((splittingCity.getX(),splittingCity.getY()), 0, 0, iNewCiv, [iPlayer])   #by trade because by conquest may raze the city
                                                utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
                                                if (iPlayer == utils.getHumanID()):
                                                        CyInterface().addMessage(iPlayer, True, con.iDuration, splittingCity.getName() + " " + \
                                                                                           CyTranslator().getText("TXT_KEY_STABILITY_SECESSION", ()), "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
                                                
                                        return
					
        def processConstantinople(self):
                asiaID = gc.getMap().plot(69, 44).area().getID()
                pConstantinople = gc.getMap().plot(68, 45)
                if (pConstantinople.area().getID() != asiaID):
                        if (pConstantinople.isCity() and pConstantinople.getPlotCity().getOwner() < con.iNumMajorPlayers):
                                return
                        else:
                                gc.getMap().plot(68, 45).setArea(asiaID)

        def convertMiddleEast(self):
                if (gc.getMap().plot(76,40).area().getID() == con.iEurope):
                        return
                for i in range(72,86+1):
                        for j in range(34,46):
                                pCurrent = gc.getMap().plot(i, j)
                                if ((not pCurrent.isWater()) and pCurrent.area().getID() != con.iEurope):
                                        pCurrent.setArea(con.iEurope)

                for i in range(69,71+1):
                        for j in range(40,45):
                                pCurrent = gc.getMap().plot(i, j)
                                if ((not pCurrent.isWater()) and pCurrent.area().getID() != con.iEurope):
                                        pCurrent.setArea(con.iEurope)

                for i in range(78,86+1):
                        for j in range(47,49):
                                pCurrent = gc.getMap().plot(i, j)
                                if ((not pCurrent.isWater()) and pCurrent.area().getID() != con.iEurope):
                                        pCurrent.setArea(con.iEurope)
                return


        def reconvertMiddleEast(self):
                if (gc.getMap().plot(76,40).area().getID() == con.iAsia):
                        return
                for i in range(72,86+1):
                        for j in range(34,46+1):
                                pCurrent = gc.getMap().plot(i, j)
                                if (not pCurrent.isWater()):
                                        pCurrent.setArea(con.iAsia)

                for i in range(69,71+1):
                        for j in range(40,45+1):
                                pCurrent = gc.getMap().plot(i, j)
                                if (not pCurrent.isWater()):
                                        pCurrent.setArea(con.iAsia)

                for i in range(78,86+1):
                        for j in range(47,49+1):
                                pCurrent = gc.getMap().plot(i, j)
                                if (not pCurrent.isWater()):
                                        pCurrent.setArea(con.iAsia)

        def convertNorthAfrica(self):
                if (gc.getMap().plot(69,33).area().getID() == con.iEurope):
                        return
                for i in range(48,65+1):
                        for j in range(35,39+1):
                                pCurrent = gc.getMap().plot(i, j)
                                if (not pCurrent.isWater()):
                                        pCurrent.setArea(con.iEurope)

                for i in range(66,71+1):
                        for j in range(29,37+1):
                                pCurrent = gc.getMap().plot(i, j)
                                if (not pCurrent.isWater()):
                                        pCurrent.setArea(con.iEurope)

                for i in range(72,73+1):
                        for j in range(29,32+1):
                                pCurrent = gc.getMap().plot(i, j)
                                if (not pCurrent.isWater()):
                                        pCurrent.setArea(con.iEurope)

        def reconvertNorthAfrica(self):
                if (gc.getMap().plot(69,33).area().getID() == con.iAsia):
                        return
                for i in range(48,65+1):
                        for j in range(35,39+1):
                                pCurrent = gc.getMap().plot(i, j)
                                if (not pCurrent.isWater()):
                                        pCurrent.setArea(con.iAsia)

                for i in range(66,71+1):
                        for j in range(29,37+1):
                                pCurrent = gc.getMap().plot(i, j)
                                if (not pCurrent.isWater()):
                                        pCurrent.setArea(con.iAsia)

                for i in range(72,73+1):
                        for j in range(29,32+1):
                                pCurrent = gc.getMap().plot(i, j)
                                if (not pCurrent.isWater()):
                                        pCurrent.setArea(con.iAsia)
        def processAfrica(self):
                africaID = gc.getMap().plot(65, 10).area().getID()
                if (gc.getMap().plot(56, 29).area().getID() == africaID):
                        return
                for iLoopX in range(48,63+1):
                        for iLoopY in range(22,33+1):
                                pCurrent = gc.getMap().plot(iLoopX, iLoopY)
                                if (not pCurrent.isWater()):
                                        pCurrent.setArea(africaID)
                            
                                    
        def initBirth(self, iCurrentTurn, iBirthYear, iCiv): # iBirthYear is really year now, so no conversion prior to function call - edead
                print 'init birth in: '+str(iBirthYear)
		iHuman = utils.getHumanID()
                iBirthYear = getTurnForYear(iBirthYear) # converted to turns here - edead
		
		if iCiv in con.lSecondaryCivs:
			if not self.getPlayerEnabled(iCiv):
				return
		
		if iCiv == iTurkey:
			if pSeljuks.isAlive():
				sta.completeCollapse(iSeljuks)
				#utils.killAndFragmentCiv(iSeljuks, iIndependent, iIndependent2, -1, False)
                
                lConditionalCivs = [iByzantium, iMughals, iThailand, iBrazil, iArgentina]
		
		# Leoreth: extra checks for conditional civs
                if iCiv in lConditionalCivs and utils.getHumanID() != iCiv:
                        if iCiv == iByzantium:
				if not pRome.isAlive() or pGreece.isAlive() or (utils.getHumanID() == iRome and utils.getStabilityLevel(iRome) == con.iStabilitySolid):
					return

			elif iCiv == iThailand:
				if utils.getHumanID() != iKhmer:
					if sd.getStabilityLevel(iKhmer) > con.iStabilityShaky:
						return
				else:
					if sd.getStabilityLevel(iKhmer) > con.iStabilityUnstable:
						return
						
			if iCiv in [iArgentina, iBrazil]:
				iColonyPlayer = utils.getColonyPlayer(iCiv)
				if iColonyPlayer < 0: return
				elif iColonyPlayer not in [iArgentina, iBrazil]:
					if sd.getStabilityLevel(iColonyPlayer) > con.iStabilityStable:
						return
						
		if utils.getHumanID() != iCiv and iCiv == iItaly:
			if pRome.isAlive():
				return
				
			cityList = utils.getCoreCityList(iRome, 0)
                        
			iIndependentCities = 0

			for pCity in cityList:
				if not pCity.getOwner() < con.iNumPlayers:
					iIndependentCities += 1
					
			if iIndependentCities == 0:
				return
				
		tCapital = tCapitals[utils.getReborn(iCiv)][iCiv]
				
		x, y = tCapital
		bCapitalSettled = False
		
		for i in [x-1, x, x+1]:
			for j in [y-1, y, y+1]:
				if iCiv == iItaly and gc.getMap().plot(i,j).isCity():
					bCapitalSettled = True
					tCapital = (i,j)
					break
					break

                if (iCurrentTurn == iBirthYear-1 + self.getSpawnDelay(iCiv) + self.getFlipsDelay(iCiv)):
                        if iCiv in lConditionalCivs or bCapitalSettled:
                                x, y = tCapital
                                utils.convertPlotCulture(gc.getMap().plot(x,y), iCiv, 100, True)
                                
			# Leoreth: so Mughals can flip Pataliputra
			if iCiv == iMughals:
				if pIndia.isAlive() and utils.getHumanID() != iIndia:
					if pIndia.getCapitalCity().getName() == "Pataliputra":
						oldCapital = pIndia.getCapitalCity()
						cityList = PyPlayer(iMongolia).getCityList()
						newCapital = cityList[gc.getGame().getSorenRandNum(len(cityList), 'random city')].GetCy()
						newCapital.setHasRealBuilding(con.iPalace, True)
						oldCapital.setHasRealBuilding(con.iPalace, False)

                if (iCurrentTurn == iBirthYear-1 + self.getSpawnDelay(iCiv) + self.getFlipsDelay(iCiv)):
                        reborn = utils.getReborn(iCiv)
                        tTopLeft = tCoreAreasTL[reborn][iCiv]
                        tBottomRight = tCoreAreasBR[reborn][iCiv]
                        tBroaderTopLeft = tBroaderAreasTL[reborn][iCiv]
                        tBroaderBottomRight = tBroaderAreasBR[reborn][iCiv]
			
			if iCiv == iThailand:
				x, y = con.tCapitals[0][iKhmer]
				if gc.getMap().plot(x, y).isCity():
					angkor = gc.getMap().plot(x, y).getPlotCity()
					bWonder = False
					for iBuilding in range(con.iNumBuildings):
						if angkor.isHasRealBuilding(iBuilding) and isWorldWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType()):
							bWonder = True
							break
					if bWonder and utils.getHumanID() != iThailand:
						print "Thais flip Angkor instead to save its wonders."
						angkor.setName("Ayutthaya", False)
						x, y = tCapital
						tCapital = (x-1, y+1)
						gc.getMap().plot(x-1, y+1).setFeatureType(-1, 0)

			if iCiv == iMongolia and utils.getHumanID() != iMongolia:
				tTopLeft = (81, 45) # 6 more west, 1 more south
			if iCiv == iTurkey and utils.getHumanID() != iTurkey and not pByzantium.isAlive():
				tTopLeft = (67, 41) # two more west
			if iCiv == iPersia and utils.getHumanID() != iPersia:
				tTopLeft = (72, 37) # include Assyria and Anatolia
			if iCiv == iSpain and utils.getHumanID() != iSpain:
				tBottomRight = (55, 46)
			if iCiv == iInca and utils.getHumanID() != iInca:
				tTopLeft = (26, 19)
				tBottomRight = (31, 24)
			if iCiv == iArgentina and utils.getHumanID() != iArgentina:	
				tTopLeft = (29, 3)
				
			iPreviousOwner = gc.getMap().plot(tCapital[0], tCapital[1]).getOwner()
				
                    
                        if (self.getFlipsDelay(iCiv) == 0): #city hasn't already been founded)
                            
                                #this may fix the -1 bug
                                if (iCiv == iHuman): 
                                        killPlot = gc.getMap().plot(tCapital[0], tCapital[1])
                                        iNumUnitsInAPlot = killPlot.getNumUnits()
                                        if (iNumUnitsInAPlot):
                                                for i in range(iNumUnitsInAPlot):                                                        
                                                        unit = killPlot.getUnit(0)
                                                        if (unit.getOwner() != iCiv):
                                                                unit.kill(False, con.iBarbarian)
                                
                                bBirthInCapital = False
				
                                if (iCiv in lConditionalCivs and iCiv != iThailand) or bCapitalSettled:
					bBirthInCapital = True
                                
				if iCiv == iTurkey:
					self.moveOutInvaders(tTopLeft, tBottomRight)  
					
				if bBirthInCapital:
					utils.makeUnit(con.iCatapult, iCiv, (1,0), 1)
                        
                                bDeleteEverything = False
                                pCapital = gc.getMap().plot(tCapital[0], tCapital[1])
                                if (pCapital.isOwned()):
                                        if (iCiv == iHuman or not gc.getPlayer(iHuman).isAlive()):
                                                if not (pCapital.isCity() and pCapital.getPlotCity().isHolyCity()):
                                                        bDeleteEverything = True
                                                        print ("bDeleteEverything 1")
                                        else:
                                                bDeleteEverything = True
                                                for x in range(tCapital[0] - 1, tCapital[0] + 2):        # from x-1 to x+1
                                                        for y in range(tCapital[1] - 1, tCapital[1] + 2):       # from y-1 to y+1
                                                                pCurrent=gc.getMap().plot(x, y)
                                                                if (pCurrent.isCity() and (pCurrent.getPlotCity().getOwner() == iHuman or pCurrent.getPlotCity().isHolyCity())):
                                                                        bDeleteEverything = False
                                                                        print ("bDeleteEverything 2")
                                                                        break
                                                                        break
                                print ("bDeleteEverything", bDeleteEverything)
                                if (not gc.getMap().plot(tCapital[0], tCapital[1]).isOwned()):
                                        if (iCiv == iNetherlands or iCiv == iPortugal or iCiv == iByzantium or iCiv == iKorea or iCiv == iThailand or iCiv == iItaly or iCiv == iCarthage): #dangerous starts
                                                self.setDeleteMode(0, iCiv)
					if bBirthInCapital:
						self.birthInCapital(iCiv, iPreviousOwner, tCapital, tTopLeft, tBottomRight)
					else:
						self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
                                elif (bDeleteEverything and not bBirthInCapital):
                                        for x in range(tCapital[0] - 1, tCapital[0] + 2):        # from x-1 to x+1
                                                for y in range(tCapital[1] - 1, tCapital[1] + 2):       # from y-1 to y+1
                                                        self.setDeleteMode(0, iCiv)
                                                        pCurrent=gc.getMap().plot(x, y)
                                                        for iLoopCiv in range(iNumTotalPlayers+1): #Barbarians as well
                                                                if (iCiv != iLoopCiv):
                                                                        utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iLoopCiv, True, False, con.tExceptions[0][iCiv])
                                                        if (pCurrent.isCity()):
                                                                pCurrent.eraseAIDevelopment() #new function, similar to erase but won't delete rivers, resources and features()
                                                        for iLoopCiv in range(iNumTotalPlayers+1): #Barbarians as well
                                                                if (iCiv != iLoopCiv):
                                                                        pCurrent.setCulture(iLoopCiv, 0, True)
                                                        pCurrent.setOwner(-1)
					if bBirthInCapital:
						self.birthInCapital(iCiv, iPreviousOwner, tCapital, tTopLeft, tBottomRight)
					else:
						self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
                                else:                    
					if bBirthInCapital:
						self.birthInCapital(iCiv, iPreviousOwner, tCapital, tTopLeft, tBottomRight)
					else:
						self.birthInForeignBorders(iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight)
						
				if bBirthInCapital:	
					plotZero = gc.getMap().plot(1, 0)
					if (plotZero.getNumUnits()):
						catapult = plotZero.getUnit(0)
						catapult.kill(False, iCiv)
					gc.getMap().plot(0, 0).setRevealed(iCiv, False, True, -1)
					gc.getMap().plot(0, 1).setRevealed(iCiv, False, True, -1)
					gc.getMap().plot(1, 1).setRevealed(iCiv, False, True, -1)
					gc.getMap().plot(1, 0).setRevealed(iCiv, False, True, -1)
					gc.getMap().plot(123, 0).setRevealed(iCiv, False, True, -1)
					gc.getMap().plot(123, 1).setRevealed(iCiv, False, True, -1)
					gc.getMap().plot(2, 0).setRevealed(iCiv, False, True, -1)
					gc.getMap().plot(2, 1).setRevealed(iCiv, False, True, -1)
					gc.getMap().plot(2, 2).setRevealed(iCiv, False, True, -1)
					gc.getMap().plot(1, 2).setRevealed(iCiv, False, True, -1)
					gc.getMap().plot(0, 2).setRevealed(iCiv, False, True, -1)
					gc.getMap().plot(122, 0).setRevealed(iCiv, False, True, -1)
					gc.getMap().plot(122, 1).setRevealed(iCiv, False, True, -1)
					gc.getMap().plot(122, 2).setRevealed(iCiv, False, True, -1)
					gc.getMap().plot(123, 2).setRevealed(iCiv, False, True, -1)
						
                        else:
                                print ( "setBirthType again: flips" )
				self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
				
                # Leoreth: reveal all broader plots on spawn
                reborn = utils.getReborn(iCiv)
                for x in range(con.tBroaderAreasTL[reborn][iCiv][0], con.tBroaderAreasBR[reborn][iCiv][0]+1):
                        for y in range(con.tBroaderAreasTL[reborn][iCiv][1], con.tBroaderAreasBR[reborn][iCiv][1]+1):
                                gc.getMap().plot(x, y).setRevealed(iCiv, True, True, 0)
				
		# Leoreth: conditional state religion for colonial civs
		if iCiv in [iArgentina, iBrazil]:
			self.setStateReligion(iCiv)
                        
                if (iCurrentTurn == iBirthYear + self.getSpawnDelay(iCiv)) and (gc.getPlayer(iCiv).isAlive()) and (self.getAlreadySwitched() == False or utils.getReborn(iCiv) == 1) and ((iHuman not in con.lNeighbours[iCiv] and getTurnForYear(con.tBirth[iCiv]) - getTurnForYear(con.tBirth[iHuman]) > 0) or getTurnForYear(con.tBirth[iCiv]) - getTurnForYear(con.tBirth[iHuman]) >= utils.getTurns(25) ):
                        self.newCivPopup(iCiv)

	def moveOutInvaders(self, tTL, tBR):
		x1, y1 = tTL
		x2, y2 = tBR
		if pSeljuks.isAlive():
			seljukCapital = pSeljuks.getCapitalCity()
		if pMongolia.isAlive():
			mongolCapital = pMongolia.getCapitalCity()
		for x in range(x1, x2+1):
			for y in range(y1, y2+1):
				plot = gc.getMap().plot(x, y)
				for i in range(plot.getNumUnits()):
					unit = plot.getUnit(i)
					if not utils.isDefenderUnit(unit):
						if unit.getOwner() == iMongolia:
							if utils.getHumanID() != iMongolia:
								unit.setXYOld(mongolCapital.getX(), mongolCapital.getY())
						elif unit.getOwner() == iSeljuks:
							unit.setXYOld(seljukCapital.getX(), seljukCapital.getY())
						else:
							if unit.getUnitType() == con.iSeljukGhulamWarrior or unit.getUnitType() == con.iMongolKeshik:
								unit.kill(False, iBarbarian)
                                
                

        def deleteMode(self, iCurrentPlayer):
                iCiv = self.getDeleteMode(0)
                print ("deleteMode after", iCurrentPlayer)
                tCapital = con.tCapitals[utils.getReborn(iCiv)][iCiv]
			
		
                if (iCurrentPlayer == iCiv):
                        if(iCiv == iCarthage):
                                for x in range(tCapital[0] - 2, tCapital[0] + 2):        # from x-2 to x+1
                                        for y in range(tCapital[1] - 1, tCapital[1] + 2):       # from y-1 to y+1
                                                pCurrent=gc.getMap().plot(x, y)
                                                pCurrent.setCulture(iCiv, 300, True)
                        else:
                                for x in range(tCapital[0] - 2, tCapital[0] + 3):        # from x-2 to x+2
                                        for y in range(tCapital[1] - 2, tCapital[1] + 3):       # from y-2 to y+2
                                                pCurrent=gc.getMap().plot(x, y)
                                                pCurrent.setCulture(iCiv, 300, True)
                        for x in range(tCapital[0] - 1, tCapital[0] + 2):        # from x-1 to x+1
                                for y in range(tCapital[1] - 1, tCapital[1] + 2):       # from y-1 to y+1
                                        pCurrent=gc.getMap().plot(x, y)
                                        utils.convertPlotCulture(pCurrent, iCiv, 100, True)
                                        if (pCurrent.getCulture(iCiv) < 3000):
                                                pCurrent.setCulture(iCiv, 3000, True) #2000 in vanilla/warlords, cos here Portugal is choked by spanish culture
                                        pCurrent.setOwner(iCiv)
                        self.setDeleteMode(0, -1)
                        return
                    
                #print ("iCurrentPlayer", iCurrentPlayer, "iCiv", iCiv)
                if (iCurrentPlayer != iCiv-1 and not (iCiv == iCarthage and iCurrentPlayer == iGreece)):
                        return
                
                bNotOwned = True
                for x in range(tCapital[0] - 1, tCapital[0] + 2):        # from x-1 to x+1
                        for y in range(tCapital[1] - 1, tCapital[1] + 2):       # from y-1 to y+1
                                #print ("deleting again", x, y)
                                pCurrent=gc.getMap().plot(x, y)
                                if (pCurrent.isOwned()):
                                        bNotOwned = False
                                        for iLoopCiv in range(iNumTotalPlayers+1): #Barbarians as well
                                                if(iLoopCiv != iCiv):
                                                        pCurrent.setCulture(iLoopCiv, 0, True)
                                        pCurrent.setOwner(iCiv)
                
                for x in range(tCapital[0] - 15, tCapital[0] + 16):        # must include the distance from Sogut to the Caspius
                        for y in range(tCapital[1] - 15, tCapital[1] + 16):
                                if (x != tCapital[0] or y != tCapital[1]):
                                        pCurrent=gc.getMap().plot(x, y)
                                        if (pCurrent.getNumUnits() > 0 and not pCurrent.isWater()):
                                                unit = pCurrent.getUnit(0)
                                                if (unit.getOwner() == iCiv):
                                                        print ("moving starting units from", x, y, "to", (tCapital[0], tCapital[1]))
                                                        for i in range(pCurrent.getNumUnits()):                                                                
                                                                unit = pCurrent.getUnit(0)
                                                                unit.setXYOld(tCapital[0], tCapital[1])
                    
        def birthInFreeRegion(self, iCiv, tCapital, tTopLeft, tBottomRight):
	
                startingPlot = gc.getMap().plot( tCapital[0], tCapital[1] )
                if (self.getFlipsDelay(iCiv) == 0):
                        iFlipsDelay = self.getFlipsDelay(iCiv) + 2
                        if (iFlipsDelay > 0):
                                print ("starting units in", tCapital[0], tCapital[1])
                                self.createStartingUnits(iCiv, (tCapital[0], tCapital[1]))
				
				if iCiv == iTurkey:
					sd.scriptDict['iOttomanSpawnTurn'] = gc.getGame().getGameTurn()
			
				if iCiv == iItaly:
					utils.removeCoreUnits(iItaly)
					cityList = utils.getCoreCityList(iItaly, 0)
					pRomePlot = gc.getMap().plot(con.tCapitals[0][iRome][0], con.tCapitals[0][iRome][1])
					if pRomePlot.isCity():
						cityList.append(pRomePlot.getPlotCity())
					for city in cityList:
						if city.getPopulation() < 5: city.setPopulation(5)
						city.setHasRealBuilding(con.iGranary, True)
						city.setHasRealBuilding(con.iLibrary, True)
						city.setHasRealBuilding(con.iCourthouse, True)
						if city.isCoastal(20): city.setHasRealBuilding(con.iHarbor, True)
										
                                utils.flipUnitsInArea((tCapital[0]-3, tCapital[1]-3), (tCapital[0]+3, tCapital[1]+3), iCiv, iBarbarian, True, True) #This is mostly for the AI. During Human player spawn, that area should be already cleaned                        
                                utils.flipUnitsInArea((tCapital[0]-3, tCapital[1]-3), (tCapital[0]+3, tCapital[1]+3), iCiv, iIndependent, True, False) #This is mostly for the AI. During Human player spawn, that area should be already cleaned                        
                                utils.flipUnitsInArea((tCapital[0]-3, tCapital[1]-3), (tCapital[0]+3, tCapital[1]+3), iCiv, iIndependent2, True, False) #This is mostly for the AI. During Human player spawn, that area should be already cleaned                        
                                self.assignTechs(iCiv)
                                utils.setPlagueCountdown(iCiv, -con.iImmunity)
                                utils.clearPlague(iCiv)
                                self.setFlipsDelay(iCiv, iFlipsDelay) #save
                                

                else: #starting units have already been placed, now the second part
		
                        iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, tTopLeft, tBottomRight)
                        self.convertSurroundingPlotCulture(iCiv, tTopLeft, tBottomRight)
                        utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent, False, False) #remaining independents in the region now belong to the new civ   
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent2, False, False) #remaining independents in the region now belong to the new civ
			
			if iCiv == iArabia:
				self.arabianSpawn()
				
			if iCiv == iGermany:
				self.germanSpawn()
   
                        print ("utils.flipUnitsInArea()") 
                        #cover plots revealed by the lion
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
                        print ("Plots covered")

                        if (gc.getPlayer(iCiv).getNumCities() > 0):
                                capital = gc.getPlayer(iCiv).getCapitalCity()
                                self.createStartingWorkers(iCiv, (capital.getX(), capital.getY()))

                        if (iNumHumanCitiesToConvert > 0 and iCiv != utils.getHumanID()): # Leoreth: quick fix for the "flip your own cities" popup, still need to find out where it comes from
				print "Flip Popup: free region"
                                self.flipPopup(iCiv, tTopLeft, tBottomRight)
				

                        
        def birthInForeignBorders(self, iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight):
	
		if iCiv == iItaly:
			utils.removeCoreUnits(iItaly)
			cityList = utils.getCoreCityList(iItaly, 0)
			pRomePlot = gc.getMap().plot(con.tCapitals[0][iRome][0], con.tCapitals[0][iRome][1])
			if pRomePlot.isCity():
				cityList.append(pRomePlot.getPlotCity())
			for pCity in cityList:
				if city.getPopulation() < 5: city.setPopulation(5)
				city.setHasRealBuilding(con.iGranary, True)
				city.setHasRealBuilding(con.iLibrary, True)
				city.setHasRealBuilding(con.iCourthouse, True)
				if city.isCoastal(20): city.setHasRealBuilding(con.iHarbor, True)
                
                iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, tTopLeft, tBottomRight)
                self.convertSurroundingPlotCulture(iCiv, tTopLeft, tBottomRight)

                #now starting units must be placed
                if (iNumAICitiesConverted > 0):
                        dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.ownedCityPlots, iCiv )        
                        rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching any city just flipped')
                        if (len(plotList)):
                                result = plotList[rndNum]
                                if (result):
                                        self.createStartingUnits(iCiv, result)
                                        self.assignTechs(iCiv)
                                        utils.setPlagueCountdown(iCiv, -con.iImmunity)
                                        utils.clearPlague(iCiv)
                        utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ 
                        utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent, False, False) #remaining barbs in the region now belong to the new civ 
                        utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent2, False, False) #remaining barbs in the region now belong to the new civ
			
			if iCiv == iTurkey:
	                        sd.scriptDict['iOttomanSpawnTurn'] = gc.getGame().getGameTurn()

                else:   #search another place
                        dummy, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.goodPlots, [] )
                        rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching another free plot')
                        if (len(plotList)):
                                result = plotList[rndNum]
                                if (result):
                                        self.createStartingUnits(iCiv, result)
                                        self.assignTechs(iCiv)
                                        utils.setPlagueCountdown(iCiv, -con.iImmunity)
                                        utils.clearPlague(iCiv)
                        else:
                                dummy1, plotList = utils.squareSearch( tBroaderTopLeft, tBroaderBottomRight, utils.goodPlots, [] )        
                                rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching other good plots in a broader region')
                                if (len(plotList)):
                                        result = plotList[rndNum]
                                        if (result):
                                                self.createStartingUnits(iCiv, result)
                                                self.createStartingWorkers(iCiv, result)
                                                self.assignTechs(iCiv)
                                                utils.setPlagueCountdown(iCiv, -con.iImmunity)
                                                utils.clearPlague(iCiv)
                        utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, True, True) #remaining barbs in the region now belong to the new civ 
                        utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent, True, False) #remaining barbs in the region now belong to the new civ 
                        utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent2, True, False) #remaining barbs in the region now belong to the new civ 

                if (iNumHumanCitiesToConvert > 0):
			print "Flip Popup: foreign borders"
                        self.flipPopup(iCiv, tTopLeft, tBottomRight)
			
		if iCiv == iGermany:
			self.germanSpawn()

        #Leoreth - adapted from SoI's birthConditional method by embryodead
        def birthInCapital(self, iCiv, iPreviousOwner, tCapital, tTopLeft, tBottomRight):

                startingPlot = (tCapital[0], tCapital[1])
		iOwner = iPreviousOwner

                if self.getFlipsDelay(iCiv) == 0:

                        iFlipsDelay = self.getFlipsDelay(iCiv)+2

                        if iFlipsDelay > 0:

                                # flip capital instead of spawning starting units
                                utils.flipCity(tCapital, False, True, iCiv, ())
				gc.getMap().plot(tCapital[0], tCapital[1]).getPlotCity().setHasRealBuilding(con.iPalace, True)
				utils.convertPlotCulture(gc.getMap().plot(tCapital[0], tCapital[1]), iCiv, 100, True)
				self.convertSurroundingPlotCulture(iCiv, (tCapital[0]-1,tCapital[1]-1), (tCapital[0]+1,tCapital[1]+1))
                                
                                #cover plots revealed
                                gc.getMap().plot(0, 0).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(0, 1).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(1, 1).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(1, 0).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(123, 0).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(123, 1).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(2, 0).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(2, 1).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(2, 2).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(1, 2).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(0, 2).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(122, 0).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(122, 1).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(122, 2).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(123, 2).setRevealed(iCiv, False, True, -1)


				print ("birthConditional: starting units in", tCapital[0], tCapital[1])
                                self.createStartingUnits(iCiv, (tCapital[0], tCapital[1]))

                                utils.setPlagueCountdown(iCiv, -con.iImmunity)
                                utils.clearPlague(iCiv)

                                print ("flipping remaining units")
                                utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, True, True) #remaining barbs in the region now belong to the new civ 
                                utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent, True, False) #remaining barbs in the region now belong to the new civ 
                                utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent2, True, False) #remaining barbs in the region now belong to the new civ 
                                
				self.assignTechs(iCiv)
				
                                self.setFlipsDelay(iCiv, iFlipsDelay) #save

                                # kill the catapult and cover the plots
                                plotZero = gc.getMap().plot(0, 0)
                                if (plotZero.getNumUnits()):
                                        catapult = plotZero.getUnit(0)
                                        catapult.kill(False, iCiv)
                                gc.getMap().plot(0, 0).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(0, 1).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(1, 1).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(1, 0).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(123, 0).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(123, 1).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(2, 0).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(2, 1).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(2, 2).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(1, 2).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(0, 2).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(122, 0).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(122, 1).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(122, 2).setRevealed(iCiv, False, True, -1)
                                gc.getMap().plot(123, 2).setRevealed(iCiv, False, True, -1)
                                print ("Plots covered")
				
				utils.convertPlotCulture(gc.getMap().plot(tCapital[0], tCapital[1]), iCiv, 100, True)
				
				# notify dynamic names
				dc.onCityAcquired((iCiv, iOwner, gc.getMap().plot(tCapital[0], tCapital[1]).getPlotCity(), False, True))

                else:           # starting units have already been placed, now to the second part

                        iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, plotList)
                        self.convertSurroundingPlotCulture(iCiv, tTopLeft, tBottomRight)
                                
                        for i in range(iIndependent, iBarbarian+1):
                                utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, i, False, True) #remaining barbs/indeps in the region now belong to the new civ   
                        
                        # kill the catapult and cover the plots
                        plotZero = gc.getMap().plot(0, 0)
                        if (plotZero.getNumUnits()):
                                catapult = plotZero.getUnit(0)
                                catapult.kill(False, iCiv)
                        gc.getMap().plot(0, 0).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(0, 1).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(1, 1).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(1, 0).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(123, 0).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(123, 1).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(2, 0).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(2, 1).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(2, 2).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(1, 2).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(0, 2).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(122, 0).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(122, 1).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(122, 2).setRevealed(iCiv, False, True, -1)
                        gc.getMap().plot(123, 2).setRevealed(iCiv, False, True, -1)
                        print ("Plots covered")
                                
                        # create workers
                        if gc.getPlayer(iCiv).getNumCities() > 0:
                                capital = gc.getPlayer(iCiv).getCapitalCity()
                                self.createStartingWorkers(iCiv, (capital.getX(), capital.getY()))
                                
                        # convert human cities
                        if iNumHumanCitiesToConvert > 0:
				print "Flip Popup: in capital"
                                self.flipPopup(iCiv, plotList)
				
			utils.convertPlotCulture(gc.getMap().plot(tCapital[0], tCapital[1]), iCiv, 100, True)
			
                                

                                                
        def convertSurroundingCities(self, iCiv, tTopLeft, tBottomRight, tExceptions = False):
                iConvertedCitiesCount = 0
                iNumHumanCities = 0
                cityList = []
                self.setSpawnWar(0)
		
		if not tExceptions: tExceptions = con.tExceptions[utils.getReborn(iCiv)][iCiv]
                
                #collect all the cities in the spawn region
                for x in range(tTopLeft[0], tBottomRight[0]+1):
                        for y in range(tTopLeft[1], tBottomRight[1]+1):
				if not (x,y) in tExceptions:
                                	pCurrent = gc.getMap().plot( x, y )
                                	if ( pCurrent.isCity()):
                                        	if (pCurrent.getPlotCity().getOwner() != iCiv):
                                                	cityList.append(pCurrent.getPlotCity())
							
		# Leoreth: Byzantium also flips Roman cities in the eastern half of the empire outside of its core (Egypt, Mesopotamia)
		if iCiv == iByzantium and pRome.isAlive():
			for pCity in PyPlayer(iRome).getCityList():
				city = pCity.GetCy()
				if city.getRegionID() in [con.rEgypt, con.rEthiopia, con.rPersia, con.rMesopotamia]:
					cityList.append(city)
					
		# Leoreth: remove capital locations
		for city in cityList:
			if city.getOwner() < con.iNumPlayers:
				if (city.getX(), city.getY()) == con.tCapitals[0][city.getOwner()] and city.isCapital():
					cityList.remove(city)

                print ("Birth", iCiv)

                #for each city
                if (len(cityList)):
                        for i in range(len(cityList)):
                                loopCity = cityList[i]
                                loopX = loopCity.getX()
                                loopY = loopCity.getY()
                                print ("cityList", loopCity.getName(), (loopX, loopY))
                                iHuman = utils.getHumanID()
                                iOwner = loopCity.getOwner()
                                iCultureChange = 0 #if 0, no flip; if > 0, flip will occur with the value as variable for utils.CultureManager()
                                
                                #case 1: barbarian/independent city
                                if (iOwner == iBarbarian or iOwner == iIndependent or iOwner == iIndependent2 or iOwner == iCeltia or iOwner == iSeljuks or iOwner == iNative):
                                        iCultureChange = 100
                                #case 2: human city
                                elif (iOwner == iHuman and not (loopX == tCapitals[utils.getReborn(iHuman)][iHuman] and loopY == tCapitals[utils.getReborn(iHuman)][iHuman]) and not gc.getPlayer(iHuman).getNumCities() <= 1 and not (self.getCheatMode() == True and loopCity.isCapital())):
                                        if (iNumHumanCities == 0):
                                                iNumHumanCities += 1
                                #case 3: other
                                elif (not loopCity.isCapital() or (iOwner == iIndia and iCiv == iMughals and utils.getHumanID() != iOwner)):   #utils.debugTextPopup( 'OTHER' )                                
                                        if (iConvertedCitiesCount < 6): #there won't be more than 5 flips in the area
                                                iCultureChange = 50
                                                if (gc.getGame().getGameTurn() <= getTurnForYear(con.tBirth[iCiv]) + 5): #if we're during a birth
                                                        rndNum = gc.getGame().getSorenRandNum(100, 'odds')
                                                        if (rndNum >= tAIStopBirthThreshold[iOwner]) and not (iCiv == con.iGermany and utils.getHumanID() != con.iGermany) and not (iCiv == iByzantium and iOwner == iRome):
                                                                print (iOwner, "stops birth", iCiv, "rndNum:", rndNum, "threshold:", tAIStopBirthThreshold[iOwner])
                                                                if (not gc.getTeam(gc.getPlayer(iOwner).getTeam()).isAtWar(iCiv)):                                                                        
                                                                        gc.getTeam(gc.getPlayer(iOwner).getTeam()).declareWar(iCiv, False, -1)
                                                                        if (gc.getPlayer(iCiv).getNumCities() > 0): #this check is needed, otherwise game crashes
                                                                                print ("capital:", gc.getPlayer(iCiv).getCapitalCity().getX(), gc.getPlayer(iCiv).getCapitalCity().getY())
                                                                                if (gc.getPlayer(iCiv).getCapitalCity().getX() != -1 and gc.getPlayer(iCiv).getCapitalCity().getY() != -1):
                                                                                        self.createAdditionalUnits(iCiv, (gc.getPlayer(iCiv).getCapitalCity().getX(), gc.getPlayer(iCiv).getCapitalCity().getY()))
                                                                                else:
                                                                                        self.createAdditionalUnits(iCiv, tCapitals[utils.getReborn(iCiv)][iCiv])
                                                                        
                                                        

                                if (iCultureChange > 0):
                                        utils.cultureManager((loopX,loopY), iCultureChange, iCiv, iOwner, True, False, False)
                                        
                                        utils.flipUnitsInCityBefore((loopX,loopY), iCiv, iOwner)
                                        self.setTempFlippingCity((loopX,loopY)) #necessary for the (688379128, 0) bug
                                        utils.flipCity((loopX,loopY), 0, 0, iCiv, [iOwner])                                                
                                        utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iCiv)

                                        iConvertedCitiesCount += 1
                                        print ("iConvertedCitiesCount", iConvertedCitiesCount)

                if (iConvertedCitiesCount > 0):
                        if (gc.getPlayer(iCiv).isHuman()):
                                CyInterface().addMessage(iCiv, True, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_TO_US", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)

                return (iConvertedCitiesCount, iNumHumanCities)



        def convertSurroundingPlotCulture(self, iCiv, tTopLeft, tBottomRight, tExceptions = False):
                
		if not tExceptions: tExceptions = con.tExceptions[utils.getReborn(iCiv)][iCiv]
		
                for x in range(tTopLeft[0], tBottomRight[0]+1):
                        for y in range(tTopLeft[1], tBottomRight[1]+1):
				if not (x,y) in tExceptions:
	                                pCurrent = gc.getMap().plot( x, y )
        	                        if (not pCurrent.isCity()):
                	                        utils.convertPlotCulture(pCurrent, iCiv, 100, False)

        def findSeaPlots( self, tCoords, iRange, iCiv):
                """Searches a sea plot that isn't occupied by a unit and isn't a civ's territory surrounding the starting coordinates"""
                seaPlotList = []
                for x in range(tCoords[0] - iRange, tCoords[0] + iRange+1):        
                        for y in range(tCoords[1] - iRange, tCoords[1] + iRange+1):     
                                pCurrent = gc.getMap().plot( x, y )
                                if ( pCurrent.isWater()):
                                        if ( not pCurrent.isUnit() ):
                                                if (not (pCurrent.isOwned() and pCurrent.getOwner() != iCiv)):
                                                        seaPlotList.append(pCurrent)
                                                        # this is a good plot, so paint it and continue search
                if (len(seaPlotList) > 0):
                        rndNum = gc.getGame().getSorenRandNum(len(seaPlotList), 'sea plot')
                        result = seaPlotList[rndNum]
                        if (result):                                                        
                                    return ((result.getX(), result.getY()))
                return (None)


        def giveRaiders( self, iCiv, tBroaderAreaTL, tBroaderAreaBR):
                pCiv = gc.getPlayer(iCiv)
                teamCiv = gc.getTeam(pCiv.getTeam())
                if (pCiv.isAlive() and pCiv.isHuman() == False):

                        cityList = []
                        #collect all the coastal cities belonging to iCiv in the area
                        for x in range(tBroaderAreaTL[0], tBroaderAreaBR[0]+1):
                                for y in range(tBroaderAreaTL[1], tBroaderAreaBR[1]+1):
                                        pCurrent = gc.getMap().plot( x, y )
                                        if ( pCurrent.isCity()):
                                                city = pCurrent.getPlotCity()
                                                if (city.getOwner() == iCiv):
                                                        if (city.isCoastalOld()):
                                                                cityList.append(city)               
                        if (len(cityList)):
                                result = cityList[0]
                                rndNum = gc.getGame().getSorenRandNum(len(cityList), 'random city')
                                result = cityList[rndNum]
                                if (result):
                                        tCityPlot = (result.getX(), result.getY())
                                        tPlot = self.findSeaPlots(tCityPlot, 1, iCiv)
                                        if (tPlot):
                                                gc.getPlayer(iCiv).initUnit(con.iGalley, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
                                                if (teamCiv.isHasTech(con.iCivilService)):
                                                        if (iCiv == iVikings):
                                                                gc.getPlayer(iCiv).initUnit(con.iVikingBerserker, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
                                                                gc.getPlayer(iCiv).initUnit(con.iVikingBerserker, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)
                                                        else:
                                                                gc.getPlayer(iCiv).initUnit(con.iMaceman, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
                                                                gc.getPlayer(iCiv).initUnit(con.iMaceman, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)

                                                else:
                                                        gc.getPlayer(iCiv).initUnit(con.iSwordsman, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
                                                        gc.getPlayer(iCiv).initUnit(con.iSwordsman, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)

        def giveEarlyColonists( self, iCiv):
                pCiv = gc.getPlayer(iCiv)
                teamCiv = gc.getTeam(pCiv.getTeam())
                if (pCiv.isAlive() and pCiv.isHuman() == False):
                        capital = gc.getPlayer(iCiv).getCapitalCity()
                        tCapital = (capital.getX(), capital.getY())
                        tSeaPlot = self.findSeaPlots(tCapital, 1, iCiv)
			
			if iCiv == iRome:
				cityList = PyPlayer(iCiv).getCityList()
				for city in cityList:
					pCity = city.GetCy()
					if pCity.getRegionID() == con.rIberia:
						tCapital = (pCity.getX(), pCity.getY())
						break
			
                        if (tSeaPlot):
                                gc.getPlayer(iCiv).initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
                                utils.makeUnit(con.iSettler, iCiv, tSeaPlot, 1)
                                utils.makeUnit(con.iArcher, iCiv, tSeaPlot, 1)

	def giveColonists(self, iCiv):
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		
		if pCiv.isAlive() and utils.getHumanID() != iCiv:
			if teamCiv.isHasTech(con.iAstronomy) and self.getColonistsAlreadyGiven(iCiv) < con.tMaxColonists[iCiv]:
				lCities = utils.getAreaCitiesCiv(iCiv, con.tCoreAreasTL[0][iCiv], con.tCoreAreasBR[0][iCiv], con.tExceptions[0][iCiv])
				
				# help England with settling Canada and Australia
				if iCiv == iEngland:
					lColonialCities = utils.getAreaCitiesCiv(iCiv, con.tCanadaTL, con.tCanadaBR)
					lColonialCities.extend(utils.getAreaCitiesCiv(iCiv, con.tAustraliaTL, con.tAustraliaBR))
					
					if lColonialCities:
						lCities = lColonialCities
						
				for city in lCities:
					if not city.isCoastal(20):
						lCities.remove(city)
						
				if lCities:
					city = utils.getRandomEntry(lCities)
					tPlot = (city.getX(), city.getY())
					tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
					if not tSeaPlot: tSeaPlot = tPlot
					
					utils.makeUnitAI(utils.getUniqueUnitType(iCiv, gc.getUnitInfo(con.iGalleon).getUnitClassType()), iCiv, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA, 1)
					utils.makeUnitAI(con.iSettler, iCiv, tSeaPlot, UnitAITypes.UNITAI_SETTLE, 1)
					utils.makeUnit(utils.getBestDefender(iCiv), iCiv, tSeaPlot, 1)
					utils.makeUnit(con.iWorker, iCiv, tSeaPlot, 1)
					
					self.changeColonistsAlreadyGiven(iCiv, 1)
					

        def onFirstContact(self, iTeamX, iHasMetTeamY):
	
		iGameTurn = gc.getGame().getGameTurn()
		
		# no conquerors for minor civs
		if iHasMetTeamY >= con.iNumPlayers: return
		
		if iGameTurn > getTurnForYear(600) and iGameTurn < getTurnForYear(1800):
			if iTeamX in con.lCivBioNewWorld and iHasMetTeamY in con.lCivBioOldWorld:
				iNewWorldCiv = iTeamX
				iOldWorldCiv = iHasMetTeamY
				
				iIndex = con.lCivBioNewWorld.index(iNewWorldCiv)
				
				bAlreadyContacted = (self.getFirstContactConquerors(iIndex) == 1)
				
				# avoid "return later" exploit
				if iGameTurn <= getTurnForYear(con.tBirth[con.iAztecs])+10:
					self.setFirstContactConquerors(iIndex, 1)
					return
					
				if not bAlreadyContacted:
					if iNewWorldCiv == iMaya:
                                                tContactZoneTL = (15, 30)
                                                tContactZoneBR = (34, 42)
                                        elif iNewWorldCiv == iAztecs:
                                                tContactZoneTL = (11, 31)
                                                tContactZoneBR = (34, 43)
                                        elif iNewWorldCiv == iInca:
                                                tContactZoneTL = (21, 11)
                                                tContactZoneBR = (36, 40)
						
					self.setFirstContactConquerors(iIndex, 1)
					
					# change some terrain to end isolation
                                        if (iNewWorldCiv == iInca):
                                                gc.getMap().plot(27, 30).setFeatureType(-1, 0)
                                                gc.getMap().plot(28, 31).setFeatureType(-1, 0)
                                                gc.getMap().plot(31, 13).setPlotType(PlotTypes.PLOT_HILLS, True, True) 
						gc.getMap().plot(32, 19).setPlotType(PlotTypes.PLOT_HILLS, True, True)
                                        if (iNewWorldCiv == iAztecs):
                                                gc.getMap().plot(40, 66).setPlotType(PlotTypes.PLOT_HILLS, True, True)
						
					lContactPlots = []
					lArrivalPlots = []
                                        for x in range(tContactZoneTL[0], tContactZoneBR[0]+1):
                                                for y in range(tContactZoneTL[1], tContactZoneBR[1]+1):
                                                        plot = gc.getMap().plot(x, y)
							if plot.isVisible(iNewWorldCiv, False) and plot.isVisible(iOldWorldCiv, False):
								lContactPlots.append((x,y))
							if plot.getOwner() == iNewWorldCiv and not plot.isCity():
								if plot.isFlatlands() or plot.isHills():
									if not plot.getFeatureType() == con.iJungle and not plot.getTerrainType() == con.iMarsh and (x,y) != (25, 32):
										lArrivalPlots.append((x,y))
								
					if lContactPlots and lArrivalPlots:
						tContactPlot = utils.getRandomEntry(lContactPlots)
						lDistancePlots = [(tuple, utils.calculateDistance(tuple[0], tuple[1], tContactPlot[0], tContactPlot[1])) for tuple in lArrivalPlots]
						lDistancePlots.sort(key=itemgetter(1))
						tArrivalPlot = lDistancePlots[0][0]
												
						pNewWorldCiv = gc.getPlayer(iNewWorldCiv)
						teamOldWorldCiv = gc.getTeam(gc.getPlayer(iOldWorldCiv).getTeam())
						
						iModifier1 = 0
						iModifier2 = 0
						
						if utils.getHumanID() == iNewWorldCiv:
							if pNewWorldCiv.getNumCities() > 6: iModifier1 = 1
						else:
							if iNewWorldCiv == iInca or pNewWorldCiv.getNumCities() > 4: iModifier1 = 1
							if utils.getHumanID() != iOldWorldCiv: iModifier2 = 1
							
						if gc.getGame().getGameTurnYear() < con.tBirth[utils.getHumanID()]:
							iModifier1 += 1
							iModifier2 += 1
							
						teamOldWorldCiv.declareWar(iNewWorldCiv, True, WarPlanTypes.WARPLAN_TOTAL)
						
						iInfantry = utils.getBestInfantry(iOldWorldCiv)
						iCounter = utils.getBestCounter(iOldWorldCiv)
						iCavalry = utils.getBestCavalry(iOldWorldCiv)
						iSiege = utils.getBestSiege(iOldWorldCiv)
						
						if iInfantry:
							utils.makeUnitAI(iInfantry, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1 + iModifier2)
						
						if iCounter:
							utils.makeUnitAI(iCounter, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
							
						if iSiege:
							utils.makeUnitAI(iSiege, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1 + iModifier1 + iModifier2)
							
						if iCavalry:
							utils.makeUnitAI(iCavalry, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 + iModifier1)
							
						if iNewWorldCiv == iInca:
							utils.makeUnitAI(con.iIncanQuechua, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
						elif iNewWorldCiv == iAztecs:
							utils.makeUnitAI(con.iAztecJaguar, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
							utils.makeUnitAI(con.iMayaHolkan, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
						elif iNewWorldCiv == iMaya:
							utils.makeUnitAI(con.iMayaHolkan, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
							utils.makeUnitAI(con.iAztecJaguar, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
                                                
                                                if utils.getHumanID() == iNewWorldCiv:
                                                        CyInterface().addMessage(iNewWorldCiv, True, con.iDuration, CyTranslator().getText("TXT_KEY_FIRST_CONTACT_NEWWORLD", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
                                                if utils.getHumanID() == iOldWorldCiv:
                                                        CyInterface().addMessage(iOldWorldCiv, True, con.iDuration, CyTranslator().getText("TXT_KEY_FIRST_CONTACT_OLDWORLD", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
							
		# Leoreth: Mongol horde event against Mughals, Persia, Arabia, Byzantium, Russia
		if iHasMetTeamY == iMongolia and not utils.getHumanID() == iMongolia:
			if iTeamX in [iPersia, iByzantium, iRussia]:
				if gc.getGame().getGameTurn() < getTurnForYear(1500) and self.getFirstContactMongols(iTeamX) == 0:

					self.setFirstContactMongols(iTeamX, 1)
		
					teamTarget = gc.getTeam(iTeamX)

					teamMongolia.declareWar(iTeamX, True, WarPlanTypes.WARPLAN_TOTAL)
					
					lPlotList = []
					lTargetList = []
					iWesternLimit = 75

					if iTeamX in [iArabia, iPersia]:
						lPlotList = utils.getBorderPlotList(iTeamX, DirectionTypes.DIRECTION_NORTH)
						for tPlot in lPlotList:
							x, y = tPlot
							if x < iWesternLimit:
								lPlotList.remove(tPlot)
					elif iTeamX in [iByzantium, iRussia]:
						lPlotList = utils.getBorderPlotList(iTeamX, DirectionTypes.DIRECTION_EAST)

					for i in range(3):
						if len(lPlotList) > 0:
							iRand = gc.getGame().getSorenRandNum(len(lPlotList), 'Random target plot')
							lTargetList.append(lPlotList[iRand])
							lPlotList.remove(lPlotList[iRand])

					for tPlot in lTargetList:
						utils.makeUnitAI(con.iMongolKeshik, iMongolia, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
						utils.makeUnitAI(con.iHorseArcher, iMongolia, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
						utils.makeUnitAI(con.iTrebuchet, iMongolia, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)

					if utils.getHumanID() == iTeamX:
						CyInterface().addMessage(iTeamX, True, con.iDuration, CyTranslator().getText("TXT_KEY_MONGOL_HORDE_HUMAN", ()), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
					elif gc.getTeam(gc.getPlayer(utils.getHumanID()).getTeam()).canContact(iTeamX):
						CyInterface().addMessage(utils.getHumanID(), True, con.iDuration, CyTranslator().getText("TXT_KEY_MONGOL_HORDE", (gc.getPlayer(iTeamX).getCivilizationAdjectiveKey(),)), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)

	def lateTradingCompany(self, iCiv):
		if utils.getHumanID() != iCiv and not utils.isAVassal(iCiv) and utils.getScenario() != con.i1700AD:
			if iCiv in [iFrance, iEngland, iNetherlands]:
				self.handleColonialConquest(iCiv)

	def earlyTradingCompany(self, iCiv):
		if utils.getHumanID() != iCiv and not utils.isAVassal(iCiv):
			if iCiv in [iSpain, iPortugal]:
				self.handleColonialAcquisition(iCiv)
				
	def onRailroadDiscovered(self, iCiv):
	
		if utils.getHumanID() != iCiv:
			if iCiv == iAmerica:
				iCount = 0
				lWestCoast = [(11, 50), (11, 49), (11, 48), (11, 47), (11, 46), (12, 45)]
				lEnemyCivs = []
				lFreePlots = []
				for tPlot in lWestCoast:
					x, y = tPlot
					pPlot = gc.getMap().plot(x, y)
					if pPlot.isCity():
						if pPlot.getPlotCity().getOwner() != iAmerica:
							iCount += 1
							lWestCoast.remove((x, y))
							lEnemyCivs.append(pPlot.getPlotCity().getOwner())
							for i in range(x-1, x+2):
								for j in range(y-1, y+2):
									plot = gc.getMap().plot(i, j)
									if not (plot.isCity() or plot.isPeak() or plot.isWater()):
										lFreePlots.append((i, j))
									
				for iEnemy in lEnemyCivs:
					gc.getTeam(iCiv).declareWar(iEnemy, True, WarPlanTypes.WARPLAN_LIMITED)
									
				if iCount > 0:
					for i in range(iCount):
						iRand = gc.getGame().getSorenRandNum(len(lFreePlots), 'random spawn plot')
						tPlot = lFreePlots[iRand]
						utils.makeUnitAI(con.iAmericanMinuteman, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
						utils.makeUnitAI(con.iCannon, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
						
				if 2-iCount > 0:
					for i in range(2-iCount):
						iRand = gc.getGame().getSorenRandNum(len(lWestCoast), 'random spawn plot')
						tPlot = lWestCoast[iRand]
						utils.makeUnit(con.iSettler, iCiv, tPlot, 1)
						utils.makeUnit(con.iAmericanMinuteman, iCiv, tPlot, 1)
						
			if iCiv == iRussia:
				lFreePlots = []
				tVladivostok = (111, 51)
				
				x, y = tVladivostok
				pPlot = gc.getMap().plot(x, y)
				utils.convertPlotCulture(pPlot, iRussia, 100, True)
				if pPlot.isCity():
					if pPlot.getPlotCity().getOwner() != iRussia:
						for i in range(x-1, x+2):
							for j in range(y-1, y+2):
								plot = gc.getMap().plot(i, j)
								if not (plot.isCity() or plot.isWater() or plot.isPeak()):
									lFreePlots.append((i, j))
									
						iRand = gc.getGame().getSorenRandNum(len(lFreePlots), 'random spawn plot')
						tPlot = lFreePlots[iRand]
						i, j = tPlot
						gc.getTeam(iRussia).declareWar(pPlot.getOwner(), True, WarPlanTypes.WARPLAN_LIMITED)
						utils.makeUnitAI(con.iRifleman, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 4)
						utils.makeUnitAI(con.iCannon, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
				else:
					bFree = True
					
					for i in range(x-1, x+2):
						for j in range(y-1, y+2):
							bFree = False
							break
					
					if bFree:
						pRussia.found(x, y)
						utils.makeUnit(con.iRifleman, iCiv, tVladivostok, 2)
						utils.makeUnit(con.iRifleman, iCiv, tVladivostok, 2)
					


	def handleColonialAcquisition(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		targetList = utils.getColonialTargets(iPlayer, True)
		targetCivList = []
		settlerList = []

		iGold = len(targetList) * 200

		for tPlot in targetList:
			x, y = tPlot
			if gc.getMap().plot(x, y).isCity():
				iTargetCiv = gc.getMap().plot(x, y).getPlotCity().getOwner()
				if not iTargetCiv in targetCivList:
					targetCivList.append(iTargetCiv)
			else:
				settlerList.append((x,y))

		for tPlot in settlerList:
			x, y = tPlot
			utils.colonialAcquisition(iPlayer, x, y)
	
		for iTargetCiv in targetCivList:
			if iTargetCiv == utils.getHumanID():
				askCityList = []
				sAskCities = ""
				sPlayer = pPlayer.getCivilizationAdjectiveKey()
				for tPlot in targetList:
					x, y = tPlot
					if gc.getMap().plot(x, y).getPlotCity().getOwner() == iTargetCiv:
						askCityList.append(tPlot)
						#sAskCities += gc.getMap().plot(x, y).getPlotCity().getName() + " "
						
				if len(askCityList) > 0:
					x, y = askCityList[0]
					sAskCities = gc.getMap().plot(x, y).getPlotCity().getName()
					
				for tPlot in askCityList:
					x, y = tPlot
					if tPlot != askCityList[0]:
						if tPlot != askCityList[len(askCityList)-1]:
							sAskCities += ", " + gc.getMap().plot(x, y).getPlotCity().getName()
						else:
							sAskCities += CyTranslator().getText("TXT_KEY_AND") + gc.getMap().plot(x, y).getPlotCity().getName()
						
				iAskGold = len(askCityList) * 200
						
                		popup = Popup.PyPopup(7625, EventContextTypes.EVENTCONTEXT_ALL)
                		popup.setHeaderString(CyTranslator().getText("TXT_KEY_ASKCOLONIALCITY_TITLE", (sPlayer,)))
                		popup.setBodyString(CyTranslator().getText("TXT_KEY_ASKCOLONIALCITY_MESSAGE", (sPlayer, iAskGold, sAskCities)))
				popup.addButton(CyTranslator().getText("TXT_KEY_POPUP_YES", ()))
				popup.addButton(CyTranslator().getText("TXT_KEY_POPUP_NO", ()))
				argsList = (iPlayer, askCityList)
				utils.setTempEventList(argsList)
                		popup.launch(False)
			else:
				iRand = gc.getGame().getSorenRandNum(100, 'City acquisition offer')
				if iTargetCiv < con.iNumPlayers:
					if iRand >= con.tPatienceThreshold[iTargetCiv] and not gc.getTeam(iPlayer).isAtWar(iTargetCiv):
						bAccepted = True
					else:
						bAccepted = False
				else:
					bAccepted = True
				
				iNumCities = 0
				for tPlot in targetList:
					x, y = tPlot
					if gc.getMap().plot(x, y).getPlotCity().getOwner() == iTargetCiv:
						iNumCities += 1
						
				if iNumCities >= gc.getPlayer(iTargetCiv).getNumCities():
					bAccepted = False

				for tPlot in targetList:
					x, y = tPlot
					if gc.getMap().plot(x, y).getPlotCity().getOwner() == iTargetCiv:
						if bAccepted:
							utils.colonialAcquisition(iPlayer, x, y)
							gc.getPlayer(iTargetCiv).changeGold(200)
						else:
							utils.colonialConquest(iPlayer, x, y)
						targetList.remove(tPlot)

		pPlayer.setGold(max(0, pPlayer.getGold()-iGold))

	def handleColonialConquest(self, iPlayer):
		targetList = utils.getColonialTargets(iPlayer)

		for tPlot in targetList:
			x, y = tPlot
			utils.colonialConquest(iPlayer, x, y)

		tSeaPlot = -1
		x, y = targetList[0]
		for i in range(x-1, x+2):
			for j in range(y-1, y+2):
				if gc.getMap().plot(i, j).isWater():
					tSeaPlot = (i, j)
					break

		if tSeaPlot != -1:
			if iPlayer == con.iNetherlands:
				utils.makeUnit(con.iNetherlandsOostindievaarder, iPlayer, tSeaPlot, 1)
			else:
				utils.makeUnit(con.iGalleon, iPlayer, tSeaPlot, 1)
				
				
	def onProjectBuilt(self, city, iProjectType):
		if iProjectType == con.iPersecutionProject:
			lReligionList = []
			iOwner = city.getOwner()
			pOwner = gc.getPlayer(iOwner)
			iStateReligion = pOwner.getStateReligion()
						
			for iReligion in range(con.iNumReligions):
				if city.isHasReligion(iReligion) and iReligion != iStateReligion and not city.isHolyCityByType(iReligion):
					lReligionList.append(iReligion)
					
			if utils.getHumanID() != iOwner:
				iPersecutedReligion = self.getPersecutedReligion(lReligionList, iStateReligion)
			else:
				iPersecutedReligion = -1
				self.launchPersecutionPopup(lReligionList, city)
			
			if iPersecutedReligion > -1:
				city.setHasReligion(iPersecutedReligion, False, True, True)
				city.setHasRealBuilding(con.iTemple + 4*iPersecutedReligion, False)
				city.setHasRealBuilding(con.iMonastery + 4*iPersecutedReligion, False)
				city.setHasRealBuilding(con.iCathedral + 4*iPersecutedReligion, False)
				
				city.changeOccupationTimer(2)
				city.changeHurryAngerTimer(city.hurryAngerLength(0))
				
				iCountdown = 10
				iCountdown -= abs(gc.getLeaderheadInfo(gc.getPlayer(iOwner).getLeader()).getDifferentReligionAttitudeChange())
				
				if gc.getPlayer(iOwner).getCivics(0) == con.iTheocracy or gc.getPlayer(iOwner).getCivics(4) == con.iFanaticism:
					iCountdown -= 2
				
				CyInterface().addMessage(city.getOwner(), True, con.iDuration, CyTranslator().getText("TXT_KEY_PERSECUTION_PERFORMED", (gc.getReligionInfo(iPersecutedReligion).getText(), city.getName())), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
				
			gc.getTeam(pOwner.getTeam()).changeProjectCount(con.iPersecutionProject, -1)
			
	def getPersecutedReligion(self, lReligionList, iStateReligion):
		for iReligion in con.tPersecutionPreference[iStateReligion]:
			if iReligion in lReligionList:
				return iReligion
				
		return -1
		
	def launchPersecutionPopup(self, lReligionList, city):
		popup = Popup.PyPopup(7627, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setBodyString(CyTranslator().getText("TXT_KEY_PERSECUTION_MESSAGE", (city.getName(),)))
		
		for iReligion in lReligionList:
			popup.addButton(gc.getReligionInfo(iReligion).getText())
			
		argsList = [lReligionList, (city.getX(), city.getY())]
		utils.setTempEventList(argsList)
		
		popup.launch(False)
	
	
	def startWarsOnSpawn(self, iCiv):
	
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		
		iMin = 10
		
		if gc.getGame().getSorenRandNum(100, 'Trigger spawn wars') >= iMin:
			for iLoopCiv in con.lEnemyCivsOnSpawn[iCiv]:
				if utils.isAVassal(iLoopCiv): continue
				if not gc.getPlayer(iLoopCiv).isAlive(): continue
				if utils.getHumanID() == iCiv and iLoopCiv not in con.lTotalWarOnSpawn[iCiv]: continue
				
				iLoopMin = 50
				if iLoopCiv >= iNumMajorPlayers: iLoopMin = 30
				if utils.getHumanID() == iLoopCiv: iLoopMin += 10
				
				if gc.getGame().getSorenRandNum(100, 'Check spawn war') >= iLoopMin:
					iWarPlan = -1
					if iLoopCiv in con.lTotalWarOnSpawn[iCiv]:
						iWarPlan = WarPlanTypes.WARPLAN_TOTAL
					teamCiv.declareWar(iLoopCiv, False, iWarPlan)
					
					
        def immuneMode(self, argsList): 
                pWinningUnit,pLosingUnit = argsList
                iLosingPlayer = pLosingUnit.getOwner()
                iUnitType = pLosingUnit.getUnitType()
                if (iLosingPlayer < iNumMajorPlayers):
                        if (gc.getGame().getGameTurn() >= getTurnForYear(con.tBirth[iLosingPlayer]) and gc.getGame().getGameTurn() <= getTurnForYear(con.tBirth[iLosingPlayer])+2):
                                if (pLosingUnit.getX() == tCapitals[utils.getReborn(iLosingPlayer)][iLosingPlayer][0] and pLosingUnit.getY() == tCapitals[utils.getReborn(iLosingPlayer)][iLosingPlayer][1]):
                                        print("new civs are immune for now")
                                        if (gc.getGame().getSorenRandNum(100, 'immune roll') >= 50):
                                                utils.makeUnit(iUnitType, iLosingPlayer, (pLosingUnit.getX(), pLosingUnit.getY()), 1)

        def initMinorBetrayal( self, iCiv ):
                iHuman = utils.getHumanID()
                dummy, plotList = utils.squareSearch( tCoreAreasTL[utils.getReborn(iCiv)][iCiv], tCoreAreasBR[utils.getReborn(iCiv)][iCiv], utils.outerInvasion, [] )
                rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching a free plot abroad human players borders')
                if (len(plotList)):
                        result = plotList[rndNum]
                        if (result):
                                self.createAdditionalUnits(iCiv, result)
                                self.unitsBetrayal(iCiv, iHuman, tCoreAreasTL[utils.getReborn(iCiv)][iCiv], tCoreAreasBR[utils.getReborn(iCiv)][iCiv], result, con.tExceptions)

        def initBetrayal( self ):
                iHuman = utils.getHumanID()
                turnsLeft = self.getBetrayalTurns()
                dummy, plotList = utils.squareSearch( self.getTempTopLeft(), self.getTempBottomRight(), utils.outerInvasion, [] )
                rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching a free plot abroad human players (or in general, the old civ if human player just swtiched) borders')
                if (not len(plotList)):
                        dummy, plotList = utils.squareSearch( self.getTempTopLeft(), self.getTempBottomRight(), utils.innerSpawn, [self.getOldCivFlip(), self.getNewCivFlip()] )
                        rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching a free plot within human or new civs border but distant from units')                                
                if (not len(plotList)):
                        dummy, plotList = utils.squareSearch( self.getTempTopLeft(), self.getTempBottomRight(), utils.innerInvasion, [self.getOldCivFlip(), self.getNewCivFlip()] )
                        rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching a free plot within human or new civs border')                                
                if (len(plotList)):
                        result = plotList[rndNum]
                        if (result):
                                if (turnsLeft == iBetrayalPeriod):
                                        self.createAdditionalUnits(self.getNewCivFlip(), result)
                                self.unitsBetrayal(self.getNewCivFlip(), self.getOldCivFlip(), self.getTempTopLeft(), self.getTempBottomRight(), result)
                self.setBetrayalTurns(turnsLeft - 1)



        def unitsBetrayal( self, iNewOwner, iOldOwner, tTopLeft, tBottomRight, tPlot, lExceptions=() ):
                if (gc.getPlayer(self.getOldCivFlip()).isHuman()):
                        CyInterface().addMessage(self.getOldCivFlip(), False, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
                elif (gc.getPlayer(self.getNewCivFlip()).isHuman()):
                        CyInterface().addMessage(self.getNewCivFlip(), False, con.iDuration, CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL_NEW", ()), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)
                for x in range(tTopLeft[0], tBottomRight[0]+1):
                        for y in range(tTopLeft[1], tBottomRight[1]+1):
				if (x, y) not in lExceptions:
					killPlot = gc.getMap().plot(x,y)
					iNumUnitsInAPlot = killPlot.getNumUnits()
					if (iNumUnitsInAPlot):                                                                  
						for i in range(iNumUnitsInAPlot):                                                
							unit = killPlot.getUnit(i)
							if (unit.getOwner() == iOldOwner):
								rndNum = gc.getGame().getSorenRandNum(100, 'betrayal')
								if (rndNum >= iBetrayalThreshold):
									if (unit.getDomainType() == 2): #land unit
										iUnitType = unit.getUnitType()
										unit.kill(False, iNewOwner)
										utils.makeUnit(iUnitType, iNewOwner, tPlot, 1)
										i = i - 1

        def createAdditionalUnits( self, iCiv, tPlot ):
                if (iCiv == iGreece):
                        utils.makeUnit(con.iGreekPhalanx, iCiv, tPlot, 4)
                if (iCiv == iPersia):
                        utils.makeUnit(con.iPersiaImmortal, iCiv, tPlot, 4)
                if (iCiv == iCarthage):
                        utils.makeUnit(con.iCarthaginianWarElephant, iCiv, tPlot, 1)
                if (iCiv == iRome):
                        utils.makeUnit(con.iRomePraetorian, iCiv, tPlot, 4)
                if (iCiv == iJapan):
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 2)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 2)
		if iCiv == iTamils:
			utils.makeUnit(con.iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(con.iWarElephant, iCiv, tPlot, 1)
                if (iCiv == iEthiopia):
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 2)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 2)
		if (iCiv == iKorea):
			for iUnit in [con.iHorseArcher, con.iCrossbowman]:
				utils.makeUnit(iUnit, iCiv, tPlot, 2)
                if (iCiv == iMaya):
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 2)
                        utils.makeUnit(con.iMayaHolkan, iCiv, tPlot, 2)
                if (iCiv == iByzantium):
                        utils.makeUnit(con.iByzantineCataphract, iCiv, tPlot, 2)
                        utils.makeUnit(con.iHorseArcher, iCiv, tPlot, 2)   
                if (iCiv == iVikings):
                        utils.makeUnit(con.iAxeman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 2)
                if (iCiv == iArabia):
                        utils.makeUnit(con.iLongbowman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iArabiaCamelarcher, iCiv, tPlot, 4)
		if iCiv == iTibet:
			utils.makeUnit(con.iTibetanKhampa, iCiv, tPlot, 2)
                if (iCiv == iKhmer):
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 3)
                        utils.makeUnit(con.iKhmerBallistaElephant, iCiv, tPlot, 2)
		if (iCiv == iIndonesia):
			utils.makeUnit(con.iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(con.iWarElephant, iCiv, tPlot, 1)
		if iCiv == iMoors:
			utils.makeUnit(con.iCamelArcher, iCiv, tPlot, 2)
                if (iCiv == iSpain):
                        utils.makeUnit(con.iLongbowman, iCiv, tPlot, 3)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 3)
                if (iCiv == iFrance):
                        utils.makeUnit(con.iLongbowman, iCiv, tPlot, 3)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 3)
                if (iCiv == iEngland):
                        utils.makeUnit(con.iLongbowman, iCiv, tPlot, 3)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 3)
                if (iCiv == iHolyRome):                        
                        utils.makeUnit(con.iLongbowman, iCiv, tPlot, 3)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 3)
                if (iCiv == iRussia):
                        utils.makeUnit(con.iLongbowman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iHorseArcher, iCiv, tPlot, 2)
                if (iCiv == iNetherlands):                        
                        utils.makeUnit(con.iMusketman, iCiv, tPlot, 3)
                        utils.makeUnit(con.iPikeman, iCiv, tPlot, 3)
                if (iCiv == iMali):
                        utils.makeUnit(con.iMaliSkirmisher, iCiv, tPlot, 4)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 3)
                if (iCiv == iTurkey):
                        utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 3)
                        utils.makeUnit(con.iHorseArcher, iCiv, tPlot, 3)
		if iCiv == iPoland:
			utils.makeUnit(con.iKnight, iCiv, tPlot, 2)
			utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 2)
                if (iCiv == iPortugal):                        
                        utils.makeUnit(con.iLongbowman, iCiv, tPlot, 3)
                        utils.makeUnit(con.iPikeman, iCiv, tPlot, 3)
                if (iCiv == iInca):
                        utils.makeUnit(con.iIncanQuechua, iCiv, tPlot, 5)
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 3)
		if iCiv == iItaly:
			utils.makeUnit(con.iKnight, iCiv, tPlot, 2)
                if (iCiv == iMongolia):
                        utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iHorseArcher, iCiv, tPlot, 2) 
                        utils.makeUnit(con.iMongolKeshik, iCiv, tPlot, 4)
                if (iCiv == iAztecs):
                        utils.makeUnit(con.iAztecJaguar, iCiv, tPlot, 5)
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 3)
		if iCiv == iMughals:
			utils.makeUnit(con.iMughalSiegeElephant, iCiv, tPlot, 2)
			utils.makeUnit(con.iHorseArcher, iCiv, tPlot, 4)
		if iCiv == iThailand:
			utils.makeUnit(con.iPikeman, iCiv, tPlot, 2)
			utils.makeUnit(con.iThaiChangSuek, iCiv, tPlot, 2)
		if iCiv == iCongo:
			utils.makeUnit(con.iCongoPombos, iCiv, tPlot, 3)
		if iCiv == iGermany:
			utils.makeUnit(con.iRifleman, iCiv, tPlot, 5)
			utils.makeUnit(con.iCannon, iCiv, tPlot, 3)
                if (iCiv == iAmerica):
                        utils.makeUnit(con.iGrenadier, iCiv, tPlot, 3)
                        utils.makeUnit(con.iAmericanMinuteman, iCiv, tPlot, 3)
                        utils.makeUnit(con.iCannon, iCiv, tPlot, 3)
		if iCiv == iArgentina:
			utils.makeUnit(con.iRifleman, iCiv, tPlot, 2)
			utils.makeUnit(con.iArgentineGrenadierCavalry, iCiv, tPlot, 4)
		elif iCiv == iBrazil:
			utils.makeUnit(con.iGrenadier, iCiv, tPlot, 2)
			utils.makeUnit(con.iRifleman, iCiv, tPlot, 3)
			utils.makeUnit(con.iCannon, iCiv, tPlot, 2)


        def createStartingUnits( self, iCiv, tPlot ):
		if iCiv == iIndia:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(con.iArcher, iCiv, tPlot, 1)
                if (iCiv == iGreece):
			utils.createSettlers(iCiv, 1)
                        utils.makeUnit(con.iWarrior, iCiv, tPlot, 2)
                        utils.makeUnit(con.iGreekPhalanx, iCiv, tPlot, 1) #3
                        pGreece.initUnit(con.iGreekPhalanx, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
                        pGreece.initUnit(con.iGreekPhalanx, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)
                        tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
                        if (tSeaPlot):
                                pGreece.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
                                utils.makeUnit(con.iSettler, iCiv, tSeaPlot, 1)
                                utils.makeUnit(con.iWarrior, iCiv, tSeaPlot, 1)
                if (iCiv == iPersia):
			utils.createSettlers(iCiv, 2)
                        utils.makeUnitAI(con.iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 4)
                        utils.makeUnit(con.iPersiaImmortal, iCiv, tPlot, 6)
                        utils.makeUnit(con.iChariot, iCiv, tPlot, 4)
                if (iCiv == iCarthage):
			utils.createSettlers(iCiv, 1)
                        utils.makeUnitAI(con.iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
                        utils.makeUnit(con.iSpearman, iCiv, tPlot, 1)
                        tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
                        if (tSeaPlot):                                
                                utils.makeUnit(con.iWorkBoat, iCiv, tSeaPlot, 2)
                                pCarthage.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
                                utils.makeUnit(con.iSettler, iCiv, tSeaPlot, 1)
                                utils.makeUnit(con.iArcher, iCiv, tSeaPlot, 1)
                                pCarthage.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
                                pCarthage.initUnit(con.iTrireme, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
                if (iCiv == iRome):
			utils.createSettlers(iCiv, 3)
                        utils.makeUnitAI(con.iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 3)
                        utils.makeUnit(con.iRomePraetorian, iCiv, tPlot, 4)
                        tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
                        if (tSeaPlot):                                
                                utils.makeUnit(con.iWorkBoat, iCiv, tSeaPlot, 1)
                                pRome.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
                                pRome.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
                if (iCiv == iJapan):
		        utils.createSettlers(iCiv, 3)
			utils.makeUnit(con.iBuddhistMissionary, iJapan, tCapitals[0][iJapan], 3)
                	utils.makeUnit(con.iSwordsman, iJapan, tCapitals[0][iJapan], 2)
                	utils.makeUnitAI(con.iArcher, iJapan, tCapitals[0][iJapan], UnitAITypes.UNITAI_CITY_DEFENSE, 2)
                	utils.makeUnit(con.iWorker, iJapan, tCapitals[0][iJapan], 2)
                	tSeaPlot = self.findSeaPlots(tCapitals[0][iJapan], 1, iJapan)
                	if (tSeaPlot):                                
                        	utils.makeUnit(con.iWorkBoat, iJapan, tSeaPlot, 2)
			if utils.getHumanID() != iJapan:
				utils.makeUnit(con.iCrossbowman, iJapan, tCapitals[0][iJapan], 2)
				utils.makeUnit(con.iJapanSamurai, iJapan, tCapitals[0][iJapan], 3)
		if iCiv == iTamils:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(con.iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(con.iWarElephant, iCiv, tPlot, 1)
			utils.makeUnit(con.iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(con.iHinduMissionary, iCiv, tPlot, 1)
			if utils.getHumanID() != iTamils:
				utils.makeUnit(con.iHinduMissionary, iCiv, tPlot, 1)
				utils.makeUnit(con.iWarElephant, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tCapitals[0][iTamils], 1, iTamils)
			if (tSeaPlot):
				utils.makeUnit(con.iWorkBoat, iTamils, tSeaPlot, 1)
				utils.makeUnit(con.iGalley, iTamils, tSeaPlot, 1)
				utils.makeUnit(con.iSettler, iTamils, tSeaPlot, 1)
				utils.makeUnit(con.iArcher, iTamils, tSeaPlot, 1)
                if (iCiv == iEthiopia):
			utils.createSettlers(iCiv, 2)
                        utils.makeUnitAI(con.iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 1)
                        utils.makeUnit(con.iAxeman, iCiv, tPlot, 1)
                        tSeaPlot = (74, 29)
                        if (tSeaPlot):                                
                                utils.makeUnit(con.iWorkBoat, iCiv, tSeaPlot, 1)
				utils.makeUnit(con.iTrireme, iCiv, tSeaPlot, 1)
		if (iCiv == iKorea):
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(con.iBuddhistMissionary, iCiv, tPlot, 1)
			utils.makeUnitAI(con.iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 3)
			utils.makeUnit(con.iSwordsman, iCiv, tPlot, 1)
			utils.makeUnit(con.iHorseArcher, iCiv, tPlot, 1)
			if utils.getHumanID() != iKorea:
				utils.makeUnit(con.iSpearman, iCiv, tPlot, 2)
				utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 2)
                if (iCiv == iMaya):
			utils.createSettlers(iCiv, 2)
                        utils.makeUnit(con.iWarrior, iCiv, tPlot, 3)
                if (iCiv == iByzantium):
                        utils.makeUnit(con.iRomePraetorian, iCiv, tPlot, 4)
			utils.makeUnit(con.iSpearman, iCiv, tPlot, 2)
                        utils.makeUnitAI(con.iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.createSettlers(iCiv, 4)
			if gc.getGame().isReligionFounded(con.iOrthodoxy):
				utils.makeUnit(con.iOrthodoxMissionary, iCiv, tPlot, 2)
			else:
				utils.makeUnit(con.iChristianMissionary, iCiv, tPlot, 2)
			tSeaPlot = self.findSeaPlots(tCapitals[0][iByzantium], 1, iByzantium)
			if tSeaPlot:
				utils.makeUnit(con.iGalley, iByzantium, tSeaPlot, 2)
				utils.makeUnit(con.iTrireme, iByzantium, tSeaPlot, 2)
				if utils.getScenario() == con.i3000BC:
					utils.makeUnit(con.iWorkBoat, iByzantium, tSeaPlot, 1)
                if (iCiv == iVikings):
			utils.createSettlers(iCiv, 2)
                        utils.makeUnitAI(con.iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 4)
                        utils.makeUnit(con.iAxeman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iScout, iCiv, tPlot, 1)
                        pVikings.initUnit(con.iSwordsman, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 1)
                        tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
                        if (tSeaPlot):                                
                                utils.makeUnit(con.iWorkBoat, iCiv, tSeaPlot, 1)
                                pVikings.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
                                utils.makeUnit(con.iSettler, iCiv, tSeaPlot, 1)
                                utils.makeUnit(con.iLongbowman, iCiv, tSeaPlot, 1)
                                pVikings.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_EXPLORE_SEA, DirectionTypes.DIRECTION_SOUTH)           
                                pVikings.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_EXPLORE_SEA, DirectionTypes.DIRECTION_SOUTH)        
                if (iCiv == iArabia):
			utils.createSettlers(iCiv, 2)
			utils.makeUnitAI(con.iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
                        utils.makeUnit(con.iArabiaCamelarcher, iCiv, tPlot, 2)
			utils.makeUnit(con.iWorker, iCiv, tPlot, 1)    
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(con.iWorkBoat, iCiv, tSeaPlot, 1)
		if iCiv == iTibet:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(con.iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(con.iTibetanKhampa, iCiv, tPlot, 2)
			utils.makeUnit(con.iBuddhistMissionary, iCiv, tPlot, 1)
                if (iCiv == iKhmer):
			utils.createSettlers(iCiv, 1)
                        utils.makeUnitAI(con.iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
                        utils.makeUnitAI(con.iKhmerBallistaElephant, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
			utils.makeUnit(con.iHinduMissionary, iCiv, tPlot, 1)
                        utils.makeUnit(con.iBuddhistMissionary, iCiv, tPlot, 1)
                        tSeaPlot = self.findSeaPlots(tPlot, 2, iCiv)
                        if (tSeaPlot):                                
                                utils.makeUnit(con.iWorkBoat, iCiv, tSeaPlot, 1)
                                pKhmer.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
                                utils.makeUnit(con.iSettler, iCiv, tSeaPlot, 1)
                                utils.makeUnit(con.iArcher, iCiv, tSeaPlot, 1)
		if (iCiv == iIndonesia):
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(con.iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(con.iBuddhistMissionary, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if (tSeaPlot):
				utils.makeUnit(con.iWorkBoat, iCiv, tSeaPlot, 1)
				utils.makeUnit(con.iTrireme, iCiv, tSeaPlot, 1)
				pIndonesia.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pIndonesia.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(con.iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(con.iArcher, iCiv, tSeaPlot, 1)
				utils.makeUnit(con.iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(con.iArcher, iCiv, tSeaPlot, 1)
		if iCiv == iMoors:
			utils.createSettlers(iCiv, 2)
			utils.makeUnitAI(con.iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(con.iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(con.iSpearman, iCiv, tPlot, 1)
			utils.makeUnit(con.iIslamicMissionary, iCiv, tPlot, 2)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(con.iGalley, iCiv, tSeaPlot, 1)
				utils.makeUnit(con.iWorkboat, iCiv, tSeaPlot, 1)
			if utils.getHumanID() in [iSpain, iMoors]:
				utils.makeUnitAI(con.iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
                if (iCiv == iSpain):
			iSpanishSettlers = 2
			if utils.getHumanID() != iSpain: iSpanishSettlers = 3
			utils.createSettlers(iCiv, iSpanishSettlers)
                        utils.makeUnit(con.iLongbowman, iCiv, tPlot, 1)
			utils.makeUnitAI(con.iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 4)
			if self.getPlayerEnabled(iMoors):
				utils.makeUnit(con.iKnight, iCiv, tPlot, 2)
			else:
				utils.makeUnit(con.iSettler, iCiv, tPlot, 1)
			if utils.getHumanID() != iSpain:
				utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(con.iChristianMissionary, iCiv, tPlot, 1)
                        if utils.getScenario() == con.i600AD: #late start condition
                                utils.makeUnit(con.iWorker, iCiv, tPlot, 1) #there is no carthaginian city in Iberia and Portugal may found 2 cities otherwise (a settler is too much)
                if (iCiv == iFrance):
			utils.createSettlers(iCiv, 3)
                        utils.makeUnitAI(con.iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 4)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iAxeman, iCiv, tPlot, 3)
			utils.makeUnit(con.iChristianMissionary, iCiv, tPlot, 1)
                if (iCiv == iEngland):
			utils.createSettlers(iCiv, 3)
                        utils.makeUnitAI(con.iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 3)
			if utils.getHumanID() != iEngland:
				utils.makeUnit(con.iMaceman, iCiv, tPlot, 3)
			utils.makeUnit(con.iChristianMissionary, iCiv, tPlot, 1)
                        tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
                        if (tSeaPlot):                                
                                utils.makeUnit(con.iWorkBoat, iCiv, tSeaPlot, 2)
                                pEngland.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
                                utils.makeUnit(con.iSettler, iCiv, tPlot, 1)
                                utils.makeUnit(con.iLongbowman, iCiv, tPlot, 1)
                                utils.makeUnit(con.iGalley, iCiv, tSeaPlot, 2)
                if (iCiv == iHolyRome):                        
			utils.createSettlers(iCiv, 3)
                        utils.makeUnitAI(con.iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 3)
                        utils.makeUnitAI(con.iSwordsman, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
                        utils.makeUnitAI(con.iKnight, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
			utils.makeUnitAI(con.iCatapult, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 4)
			utils.makeUnit(con.iChristianMissionary, iCiv, tPlot, 1)
                if (iCiv == iRussia):
			utils.createSettlers(iCiv, 4)
                        utils.makeUnitAI(con.iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
                        utils.makeUnit(con.iSwordsman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iHorseArcher, iCiv, tPlot, 3)
                if (iCiv == iHolland):
			utils.createSettlers(iCiv, 2)
                        utils.makeUnit(con.iMusketman, iCiv, tPlot, 6)
			utils.makeUnit(con.iBombard, iCiv, tPlot, 2)
                        utils.makeUnit(con.iPikeman, iCiv, tPlot, 2)
			utils.makeUnit(con.iJewishMissionary+gc.getPlayer(iCiv).getStateReligion(), iCiv, tPlot, 1)
                        tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
                        if (tSeaPlot):                                
                                utils.makeUnit(con.iWorkBoat, iCiv, tSeaPlot, 2)
                                pHolland.initUnit(con.iNetherlandsOostindievaarder, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
                                utils.makeUnit(con.iSettler, iCiv, tSeaPlot, 1)
                                utils.makeUnit(con.iLongbowman, iCiv, tSeaPlot, 1)
                                pHolland.initUnit(con.iNetherlandsOostindievaarder, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(con.iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(con.iLongbowman, iCiv, tSeaPlot, 1)
                                utils.makeUnit(con.iCaravel, iCiv, tSeaPlot, 2)
                if (iCiv == iMali):
			utils.createSettlers(iCiv, 3)
                        utils.makeUnit(con.iMaliSkirmisher, iCiv, tPlot, 5)
                        utils.makeUnit(con.iIslamicMissionary, iCiv, tPlot, 1)
		if iCiv == iPoland:
			utils.createSettlers(iCiv, 2)
			utils.makeUnitAI(con.iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(con.iMaceman, iCiv, tPlot, 1)
			if utils.getHumanID() != iPoland:
				utils.makeUnit(con.iPikeman, iCiv, tPlot, 2)
			utils.makeUnit(con.iChristianMissionary, iCiv, tPlot, 1)
                if (iCiv == iTurkey):
                        utils.makeUnit(con.iLongbowman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 3)
                        utils.makeUnit(con.iHorseArcher, iCiv, tPlot, 3)
                        utils.makeUnit(con.iBombard, iCiv, tPlot, 2)
                        utils.makeUnit(con.iTrebuchet, iCiv, tPlot, 3)
                        utils.makeUnit(con.iIslamicMissionary, iCiv, tPlot, 3)
			if utils.getHumanID() != iTurkey:
				utils.makeUnit(con.iBombard, iCiv, tPlot, 3)
				utils.makeUnit(con.iOttomanJanissary, iCiv, tPlot, 5)
				utils.makeUnit(con.iKnight, iCiv, tPlot, 2)
                if (iCiv == iPortugal):
			utils.createSettlers(iCiv, 1)
                        utils.makeUnitAI(con.iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
                        utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iPikeman, iCiv, tPlot, 2)
			utils.makeUnit(con.iChristianMissionary, iCiv, tPlot, 1)
                        tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
                        if (tSeaPlot):                                
                                utils.makeUnit(con.iWorkBoat, iCiv, tSeaPlot, 2)
                                pPortugal.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
                                utils.makeUnit(con.iSettler, iCiv, tPlot, 1)
                                utils.makeUnit(con.iLongbowman, iCiv, tPlot, 1)
                                utils.makeUnit(con.iGalley, iCiv, tSeaPlot, 1)
                if (iCiv == iInca):
			utils.createSettlers(iCiv, 1)
                        utils.makeUnit(con.iIncanQuechua, iCiv, tPlot, 4)
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 2)
			if utils.getHumanID() != iInca:
				utils.makeUnit(con.iSettler, iCiv, tPlot, 1)
		if iCiv == iItaly:
			utils.createSettlers(iCiv, 1)
                        utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 3)
                        utils.makeUnit(con.iPikeman, iCiv, tPlot, 2)
			utils.makeUnit(con.iTrebuchet, iCiv, tPlot, 3)
			utils.makeUnit(con.iChristianMissionary, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if (tSeaPlot):
				utils.makeUnit(con.iWorkboat, iCiv, tSeaPlot, 2)
				utils.makeUnit(con.iGalley, iCiv, tSeaPlot, 1)
				utils.makeUnit(con.iTrireme, iCiv, tSeaPlot, 1)
                if (iCiv == iMongolia):
			utils.createSettlers(iCiv, 3)
                        utils.makeUnit(con.iLongbowman, iCiv, tPlot, 3)
                        utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 2)
                        utils.makeUnit(con.iHorseArcher, iCiv, tPlot, 2) 
                        utils.makeUnitAI(con.iMongolKeshik, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 6)
			if utils.getHumanID() != iMongolia: 
                        	utils.makeUnitAI(con.iMongolKeshik, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 4)
				utils.makeUnitAI(con.iMongolKeshik, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 4)
				utils.makeUnitAI(con.iBombard, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
				utils.makeUnitAI(con.iScout, iCiv, tPlot, UnitAITypes.UNITAI_EXPLORE, 2)
                        utils.makeUnit(con.iBombard, iCiv, tPlot, 3)
			if utils.getHumanID() != iMongolia:
				utils.makeUnitAI(con.iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
                if (iCiv == iAztecs):
			utils.createSettlers(iCiv, 2)
                        utils.makeUnit(con.iAztecJaguar, iCiv, tPlot, 4)
                        utils.makeUnit(con.iArcher, iCiv, tPlot, 4)
		if iCiv == iMughals:
			utils.createSettlers(iCiv, 3)
			utils.makeUnit(con.iMughalSiegeElephant, iCiv, tPlot, 3)
			utils.makeUnit(con.iMusketman, iCiv, tPlot, 4)
			utils.makeUnit(con.iHorseArcher, iCiv, tPlot, 2)
			utils.makeUnit(con.iIslamicMissionary, iCiv, tPlot, 1)
			if utils.getHumanID() == iMughals:
				utils.makeUnit(con.iIslamicMissionary, iCiv, tPlot, 3)
		if iCiv == iThailand:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(con.iBuddhistMissionary, iCiv, tPlot, 1)
			utils.makeUnit(con.iPikeman, iCiv, tPlot, 3)
			utils.makeUnit(con.iThaiChangSuek, iCiv, tPlot, 2)
		if iCiv == iCongo:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(con.iArcher, iCiv, tPlot, 2)
			utils.makeUnit(con.iCongoPombos, iCiv, tPlot, 2)
		if iCiv == iGermany:
			utils.createSettlers(iCiv, 4)
			utils.makeUnit(con.iJewishMissionary, iCiv, tPlot, 2, "", 2)
			utils.makeUnit(con.iRifleman, iCiv, tPlot, 3, "", 2)
			utils.makeUnitAI(con.iRifleman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(con.iCannon, iCiv, tPlot, 3, "", 2)
			if utils.getHumanID() != iGermany:
				utils.makeUnit(con.iRifleman, iCiv, tPlot, 10, "", 2)
				utils.makeUnit(con.iCannon, iCiv, tPlot, 5, "", 2)
                if (iCiv == iAmerica):
			utils.createSettlers(iCiv, 8)
                        utils.makeUnit(con.iGrenadier, iCiv, tPlot, 2)
                        utils.makeUnit(con.iAmericanMinuteman, iCiv, tPlot, 4)
                        utils.makeUnit(con.iCannon, iCiv, tPlot, 2)
                        self.addMissionary(iCiv, (23, 40), (33, 52), tPlot, 1)
                        tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
                        if (tSeaPlot):  
                                utils.makeUnit(con.iWorkBoat, iCiv, tSeaPlot, 2)
                                utils.makeUnit(con.iGalleon, iCiv, tSeaPlot, 2)
                                utils.makeUnit(con.iFrigate, iCiv, tSeaPlot, 1)
			if utils.getHumanID() != iAmerica:
				utils.makeUnitAI(con.iAmericanMinuteman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
		if iCiv == iArgentina:
			utils.createSettlers(iCiv, 2)
			utils.makeUnit(con.iRifleman, iCiv, tPlot, 3, "", 2)
			utils.makeUnit(con.iArgentineGrenadierCavalry, iCiv, tPlot, 3, "", 2)
			utils.makeUnit(con.iCannon, iCiv, tPlot, 2, "", 2)
			tSeaPlot = self.findSeaPlots(tPlot, 2, iCiv)
			if tSeaPlot:
				utils.makeUnit(con.iGalleon, iCiv, tSeaPlot, 1)
				utils.makeUnit(con.iFrigate, iCiv, tSeaPlot, 2)
			if utils.getHumanID() != iArgentina:
				utils.makeUnitAI(con.iRifleman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
				utils.makeUnit(con.iRifleman, iCiv, tPlot, 2, "", 2)
				utils.makeUnit(con.iArgentineGrenadierCavalry, iCiv, tPlot, 2, "", 2)
				utils.makeUnit(con.iCannon, iCiv, tPlot, 2, "", 2)
		if iCiv == iBrazil:
			utils.createSettlers(iCiv, 5)
			utils.makeUnit(con.iGrenadier, iCiv, tPlot, 3)
			utils.makeUnit(con.iRifleman, iCiv, tPlot, 3)
			utils.makeUnit(con.iCannon, iCiv, tPlot, 2)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(con.iWorkBoat, iCiv, tSeaPlot, 2)
				utils.makeUnit(con.iGalleon, iCiv, tSeaPlot, 2)
				utils.makeUnit(con.iFrigate, iCiv, tSeaPlot, 3)
			if utils.getHumanID() != iBrazil:
				utils.makeUnitAI(con.iRifleman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
				
		# Leoreth: start wars on spawn when the spawn actually happens
		self.startWarsOnSpawn(iCiv)

        def createRespawnUnits(self, iCiv, tPlot):
                if (iCiv == iRome):
                        utils.makeUnit(con.iCrossbowman, iCiv, tPlot, 5)
                        utils.makeUnit(con.iPikeman, iCiv, tPlot, 3)
			utils.makeUnit(con.iTrebuchet, iCiv, tPlot, 4)
                if (iCiv == iPersia):
                        utils.makeUnit(con.iMusketman, iCiv, tPlot, 4)
                        utils.makeUnit(con.iBombard, iCiv, tPlot, 3)
			utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
		if (iCiv == iIndia):
			utils.makeUnit(con.iCuirassier, iCiv, tPlot, 3)
			utils.makeUnit(con.iMusketman, iCiv, tPlot, 8)
			utils.makeUnit(con.iBombard, iCiv, tPlot, 5)
			utils.makeUnit(con.iIndianFastWorker, iCiv, tPlot, 3)			
		if iCiv == iAztecs:
			utils.makeUnit(con.iMexicoRurales, iCiv, tPlot, 4, "", 2)
			utils.makeUnit(con.iRifleman, iCiv, tPlot, 5, "", 2)
			utils.makeUnit(con.iGrenadier, iCiv, tPlot, 2, "", 2)
			utils.makeUnit(con.iWorker, iCiv, tPlot, 3, "", 2)
		if iCiv == iMaya:
			utils.makeUnit(con.iRifleman, iCiv, tPlot, 5, "", 2)
			utils.makeUnit(con.iCannon, iCiv, tPlot, 5, "", 2)
			utils.makeUnit(con.iColombianAlbionLegion, iCiv, tPlot, 5, "", 2)
			utils.makeUnit(con.iWorker, iCiv, tPlot, 3, "", 2)
                        tSeaPlot = self.findSeaPlots(tPlot, 3, iCiv)
			if tSeaPlot:
				utils.makeUnit(con.iGalleon, iCiv, tSeaPlot, 1)
				utils.makeUnit(con.iFrigate, iCiv, tSeaPlot, 1)

        def addMissionary(self, iCiv, tTopLeft, tBottomRight, tPlot, iNumber):
                lReligions = [0 for i in range(con.iNumReligions)]
                for x in range(tTopLeft[0], tBottomRight[0]+1):
                        for y in range(tTopLeft[1], tBottomRight[1]+1):
                                pCurrent = gc.getMap().plot( x, y )
                                if (pCurrent.isCity()):
                                        city = pCurrent.getPlotCity() 
                                        iOwner = city.getOwner()
                                        if (iOwner != iCiv):
                                                iStateReligion = gc.getPlayer(iOwner).getStateReligion()
                                                if (iStateReligion >= 0 and iStateReligion < con.iNumReligions):
                                                        lReligions[iStateReligion] += 1
                iMax = 0
                iWinnerReligion = -1
                for i in range(len(lReligions)): #so that Protestantism comes first
                        iLoopReligion = i % con.iNumReligions
                        if (lReligions[iLoopReligion] > iMax):
                                iMax = lReligions[iLoopReligion]
                                iWinnerReligion = iLoopReligion

                if (iWinnerReligion == -1):
                        for iLoopCiv in range(iNumMajorPlayers):
                                if (iLoopCiv != iCiv):
                                        if (gc.getMap().plot(tPlot[0], tPlot[1]).isRevealed(iLoopCiv, False)):
                                                iStateReligion = gc.getPlayer(iLoopCiv).getStateReligion()
                                                if (iStateReligion >= 0 and iStateReligion < con.iNumReligions):
                                                        lReligions[iStateReligion] += 1

                        for iLoopReligion in range(len(lReligions)): #so that Protestantism comes first
                                iLoopReligion = i % con.iNumReligions
                                if (lReligions[iLoopReligion] > iMax):
                                        iMax = lReligions[iLoopReligion]
                                        iWinnerReligion = iLoopReligion   

                if (iWinnerReligion != -1):
                        utils.makeUnit(con.iJewishMissionary + iWinnerReligion, iCiv, tPlot, iNumber)
                        

                                
        def createStartingWorkers( self, iCiv, tPlot ):
		if iCiv == iIndia:
			utils.makeUnit(con.iIndianFastWorker, iCiv, tPlot, 2)
                if (iCiv == iGreece):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 2)
                if (iCiv == iPersia):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 2)
                if (iCiv == iCarthage):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 2)
                if (iCiv == iRome):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 2)
                if (iCiv == iJapan):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 2)
		if iCiv == iTamils:
			utils.makeUnit(con.iWorker, iCiv, tPlot, 2)
                if (iCiv == iEthiopia):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
		if (iCiv == iKorea):
			utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
                if (iCiv == iMaya):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
                if (iCiv == iByzantium):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
			#utils.makeUnit(con.iSettler, iCiv, tPlot, 1)
                if (iCiv == iVikings):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 3)                              
                if (iCiv == iArabia):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
		if iCiv == iTibet:
			utils.makeUnit(con.iWorker, iCiv, tPlot, 2)
                if (iCiv == iKhmer):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 3)  
		if (iCiv == iIndonesia):
			utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
		if iCiv == iMoors:
			utils.makeUnit(con.iWorker, iCiv, tPlot, 2)
                if (iCiv == iSpain):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
                if (iCiv == iFrance):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
                if (iCiv == iEngland):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
                if (iCiv == iHolyRome):                        
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
                if (iCiv == iRussia):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
                if (iCiv == iNetherlands):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 3) 
                if (iCiv == iMali):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
		if iCiv == iPoland:
			utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
                if (iCiv == iTurkey):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 4)
                        #utils.makeUnit(con.iSettler, iCiv, tPlot, 3)
                if (iCiv == iPortugal):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 3) 
                if (iCiv == iInca):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 4)
		if iCiv == iItaly:
			utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
                if (iCiv == iMongolia):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 4)
                if (iCiv == iAztecs):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
		if iCiv == iMughals:
			utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
		if iCiv == iThailand:
			utils.makeUnit(con.iWorker, iCiv, tPlot, 2)
		if iCiv == iCongo:
			utils.makeUnit(con.iWorker, iCiv, tPlot, 2)
		if iCiv == iGermany:
			utils.makeUnit(con.iWorker, iCiv, tPlot, 3)
                if (iCiv == iAmerica):
                        utils.makeUnit(con.iWorker, iCiv, tPlot, 4)
		if iCiv == iBrazil:
			utils.makeUnit(con.iBrazilianLenhador, iCiv, tPlot, 3)
		if iCiv == iArgentina:
			utils.makeUnit(con.iWorker, iCiv, tPlot, 2)
			
	def create1700ADstartingUnits(self):
	
		# China
		tCapital = con.tBeijing
		utils.makeUnit(con.iMusketman, iChina, tCapital, 12)
		utils.makeUnit(con.iBombard, iChina, tCapital, 5)
		
		# Persia
		tCapital = con.tEsfahan
		utils.makeUnit(con.iMusketman, iPersia, tCapital, 6)
		utils.makeUnit(con.iIranianQizilbash, iPersia, tCapital, 6)
		utils.makeUnit(con.iBombard, iPersia, tCapital, 4)
		
		# Korea
		tCapital = tCapitals[0][iKorea]
		utils.makeUnit(con.iMusketman, iKorea, tCapital, 6)
		utils.makeUnit(con.iBombard, iKorea, tCapital, 4)
		
		# Japan
		tCapital = tCapitals[0][iJapan]
		utils.makeUnit(con.iMusketman, iJapan, tCapital, 10)
		utils.makeUnit(con.iBombard, iJapan, tCapital, 4)
		if utils.getHumanID() != iJapan: utils.makeUnit(con.iSettler, iJapan, tCapital, 1)
		
		# Vikings
		tCapital = con.tStockholm
		utils.makeUnit(con.iMusketman, iVikings, tCapital, 8)
		utils.makeUnit(con.iBombard, iVikings, tCapital, 4)
		
		# Spain
		tCapital = tCapitals[0][iSpain]
		utils.makeUnit(con.iMusketman, iSpain, tCapital, 6)
		utils.makeUnit(con.iSpanishConquistador, iSpain, tCapital, 4)
		utils.makeUnit(con.iBombard, iSpain, tCapital, 2)
		
		# France
		tCapital = tCapitals[0][iFrance]
		utils.makeUnit(con.iRifleman, iFrance, tCapital, 12)
		utils.makeUnit(con.iCuirassier, iFrance, tCapital, 4)
		utils.makeUnit(con.iFrenchHeavyCannon, iFrance, tCapital, 5)
		
		# England
		tCapital = tCapitals[0][iEngland]
		utils.makeUnit(con.iEnglishRedcoat, iEngland, tCapital, 8)
		utils.makeUnit(con.iCannon, iEngland, tCapital, 4)
		utils.makeUnit(con.iGalleon, iEngland, tCapital, 4)
		
		# Austria
		tCapital = con.tVienna
		utils.makeUnit(con.iRifleman, iHolyRome, tCapital, 6)
		utils.makeUnit(con.iCannon, iHolyRome, tCapital, 2)
		
		# Russia
		tCapital = tCapitals[0][iRussia]
		utils.makeUnit(con.iMusketman, iRussia, tCapital, 8)
		utils.makeUnit(con.iCuirassier, iRussia, tCapital, 4)
		utils.makeUnit(con.iBombard, iRussia, tCapital, 4)
		
		# Poland
		tCapital = con.tWarsaw
		utils.makeUnit(con.iMusketman, iPoland, tCapital, 4)
		utils.makeUnit(con.iPolishWingedHussar, iPoland, tCapital, 6)
		utils.makeUnit(con.iBombard, iPoland, tCapital, 2)
		
		# Portugal
		tCapital = tCapitals[0][iPortugal]
		utils.makeUnit(con.iMusketman, iPortugal, tCapital, 6)
		utils.makeUnit(con.iBombard, iPortugal, tCapital, 2)
		utils.makeUnit(con.iGalleon, iPortugal, tCapital, 3)
		
		# Mughals
		tCapital = tCapitals[0][iMughals]
		utils.makeUnit(con.iMusketman, iMughals, tCapital, 5)
		utils.makeUnit(con.iPikeman, iMughals, tCapital, 2)
		utils.makeUnit(con.iMughalSiegeElephant, iMughals, tCapital, 2)
		
		# Turkey
		tCapital = con.tIstanbul
		utils.makeUnit(con.iOttomanJanissary, iTurkey, tCapital, 10)
		utils.makeUnit(con.iCuirassier, iTurkey, tCapital, 4)
		utils.makeUnit(con.iBombard, iTurkey, tCapital, 5)
		
		# Thailand
		tCapital = tCapitals[0][iThailand]
		utils.makeUnit(con.iMusketman, iThailand, tCapital, 4)
		utils.makeUnit(con.iPikeman, iThailand, tCapital, 2)
		utils.makeUnit(con.iThaiChangSuek, iThailand, tCapital, 4)
		utils.makeUnit(con.iBombard, iThailand, tCapital, 2)
		
		# Congo
		tCapital = tCapitals[0][iCongo]
		utils.makeUnit(con.iSettler, iCongo, tCapital, 1)
		utils.makeUnit(con.iCongoPombos, iCongo, tCapital, 6)
		utils.makeUnit(con.iCatapult, iCongo, tCapital, 2)
		utils.makeUnit(con.iLongbowman, iCongo, tCapital, 2)
		utils.makeUnit(con.iNativeSlave, iCongo, tCapital, 5)
		
		# Netherlands
		tCapital = tCapitals[0][iNetherlands]
		utils.makeUnit(con.iRifleman, iNetherlands, tCapital, 5)
		utils.makeUnit(con.iBombard, iNetherlands, tCapital, 2)
		utils.makeUnit(con.iDutchEastIndiaman, iNetherlands, tCapital, 3)
		
		# Prussia
		tCapital = tCapitals[0][iGermany]
		utils.makeUnit(con.iRifleman, iGermany, tCapital, 8)
		utils.makeUnit(con.iCannon, iGermany, tCapital, 3)
		
		for iPlayer in [iAmerica, iArgentina, iBrazil]:
			if utils.getHumanID() == iPlayer:
				utils.makeUnit(iSettler, iPlayer, con.tCapitals[0][iPlayer], 1)
				utils.makeUnit(iWarrior, iPlayer, con.tCapitals[0][iPlayer], 1)

        def create600ADstartingUnits( self ):

                utils.makeUnit(con.iSwordsman, iChina, tCapitals[0][iChina], 2)
                utils.makeUnit(con.iArcher, iChina, tCapitals[0][iChina], 1)
		utils.makeUnitAI(con.iSpearman, iChina, tCapitals[0][iChina], UnitAITypes.UNITAI_CITY_DEFENSE, 1)
                utils.makeUnit(con.iChinaChokonu, iChina, tCapitals[0][iChina], 2)
                utils.makeUnit(con.iHorseArcher, iChina, tCapitals[0][iChina], 1)
                utils.makeUnit(con.iWorker, iChina, tCapitals[0][iChina], 2)
                
                utils.makeUnit(iSettler, iJapan, tCapitals[0][iJapan], 3)
		utils.makeUnit(con.iBuddhistMissionary, iJapan, tCapitals[0][iJapan], 3)
                utils.makeUnit(con.iSwordsman, iJapan, tCapitals[0][iJapan], 2)
                utils.makeUnit(con.iArcher, iJapan, tCapitals[0][iJapan], 2)
                utils.makeUnit(con.iWorker, iJapan, tCapitals[0][iJapan], 2)
                tSeaPlot = self.findSeaPlots(tCapitals[0][iJapan], 1, iJapan)
                if (tSeaPlot):                                
                        utils.makeUnit(con.iWorkBoat, iJapan, tSeaPlot, 2)

		if utils.getHumanID() != iJapan:
			utils.makeUnit(con.iCrossbowman, iJapan, tCapitals[0][iJapan], 2)
			utils.makeUnit(con.iJapanSamurai, iJapan, tCapitals[0][iJapan], 3)


                utils.makeUnit(con.iSettler, iVikings, tCapitals[0][iVikings], 2)
		utils.makeUnit(con.iWorker, iVikings, tCapitals[0][iVikings], 3)
                utils.makeUnit(con.iLongbowman, iVikings, tCapitals[0][iVikings], 4)
                utils.makeUnit(con.iAxeman, iVikings, tCapitals[0][iVikings], 2)
                utils.makeUnit(con.iScout, iVikings, tCapitals[0][iVikings], 1)
                pVikings.initUnit(con.iSwordsman, tCapitals[0][iVikings][0], tCapitals[0][iVikings][1], UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)
                utils.makeUnit(con.iSwordsman, iVikings, tCapitals[0][iVikings], 1)                                
                tSeaPlot = self.findSeaPlots(tCapitals[0][iVikings], 1, iVikings)
                if (tSeaPlot):                                
                        utils.makeUnit(con.iWorkBoat, iVikings, tSeaPlot, 1)
                        pVikings.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
                        utils.makeUnit(con.iSettler, iVikings, tSeaPlot, 1)
                        utils.makeUnit(con.iLongbowman, iVikings, tSeaPlot, 1)
                        pVikings.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_EXPLORE_SEA, DirectionTypes.DIRECTION_SOUTH)                                  #utils.makeUnit(con.iSettler, iCiv, tSeaPlot, 1)
                        pVikings.initUnit(con.iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_EXPLORE_SEA, DirectionTypes.DIRECTION_SOUTH)                                  #utils.makeUnit(con.iSettler, iCiv, tSeaPlot, 1)

                utils.makeUnit(con.iSpearman, iByzantium, tCapitals[0][iByzantium], 2)
                utils.makeUnit(con.iArcher, iByzantium, tCapitals[0][iByzantium], 3)
                utils.makeUnit(con.iByzantineCataphract, iByzantium, tCapitals[0][iByzantium], 1)
		tSeaPlot = self.findSeaPlots(tCapitals[0][iByzantium], 1, iByzantium)
		if tSeaPlot:
			utils.makeUnit(con.iGalley, iByzantium, tSeaPlot, 2)
			utils.makeUnit(con.iTrireme, iByzantium, tSeaPlot, 2)

		utils.makeUnit(con.iSettler, iKorea, tCapitals[0][iKorea], 2)
		utils.makeUnit(con.iBuddhistMissionary, iKorea, tCapitals[0][iKorea], 1)
		utils.makeUnit(con.iConfucianMissionary, iKorea, tCapitals[0][iKorea], 1)
		utils.makeUnit(con.iArcher, iKorea, tCapitals[0][iKorea], 2)
		utils.makeUnit(con.iAxeman, iKorea, tCapitals[0][iKorea], 3)
		utils.makeUnit(con.iHorseArcher, iKorea, tCapitals[0][iKorea], 1)
		utils.makeUnit(con.iWorker, iKorea, tCapitals[0][iKorea], 3)

		if utils.getHumanID() != iKorea:
			utils.makeUnit(con.iMaceman, iKorea, tCapitals[0][iKorea], 2)

		if pArabia.isHuman():
			utils.makeUnit(iSettler, iArabia, tCapitals[0][iArabia], 1)
			utils.makeUnit(iWarrior, iArabia, tCapitals[0][iArabia], 1)
		if pTibet.isHuman():
			utils.makeUnit(iSettler, iTibet, tCapitals[0][iTibet], 1)
			utils.makeUnit(iWarrior, iTibet, tCapitals[0][iTibet], 1)
                if ( pKhmer.isHuman() ):
                    utils.makeUnit(iSettler, iKhmer, tCapitals[0][iKhmer], 1)
                    utils.makeUnit(iWarrior, iKhmer, tCapitals[0][iKhmer], 1)
		if ( pIndonesia.isHuman() ):
			utils.makeUnit(iSettler, iIndonesia, tCapitals[0][iIndonesia], 1)
			utils.makeUnit(iWarrior, iIndonesia, tCapitals[0][iIndonesia], 1)
		if pMoors.isHuman():
			utils.makeUnit(iSettler, iMoors, tCapitals[0][iMoors], 1)
			utils.makeUnit(iWarrior, iMoors, tCapitals[0][iMoors], 1)
                if ( pSpain.isHuman() ):
                    utils.makeUnit(iSettler, iSpain, tCapitals[0][iSpain], 1)
                    utils.makeUnit(iWarrior, iSpain, tCapitals[0][iSpain], 1)
                if ( pFrance.isHuman() ):
                    utils.makeUnit(iSettler, iFrance, tCapitals[0][iFrance], 1)
                    utils.makeUnit(iWarrior, iFrance, tCapitals[0][iFrance], 1)
                if ( pEngland.isHuman() ):
                    utils.makeUnit(iSettler, iEngland, tCapitals[0][iEngland], 1)
                    utils.makeUnit(iWarrior, iEngland, tCapitals[0][iEngland], 1)
                if ( pHolyRome.isHuman() ):
                    utils.makeUnit(iSettler, iHolyRome, tCapitals[0][iHolyRome], 1)
                    utils.makeUnit(iScout, iHolyRome, tCapitals[0][iHolyRome], 1)
                if ( pRussia.isHuman() ):
                    utils.makeUnit(iSettler, iRussia, tCapitals[0][iRussia], 1)
                    utils.makeUnit(iScout, iRussia, tCapitals[0][iRussia], 1)
                if ( pNetherlands.isHuman() ):
                    utils.makeUnit(iSettler, iNetherlands, tCapitals[0][iNetherlands], 1)
                    utils.makeUnit(iWarrior, iNetherlands, tCapitals[0][iNetherlands], 1)
                if ( pMali.isHuman() ):
                    utils.makeUnit(iSettler, iMali, tCapitals[0][iMali], 1)
                    utils.makeUnit(iWarrior, iMali, tCapitals[0][iMali], 1)
		if pPoland.isHuman():
			utils.makeUnit(iSettler, iPoland, tCapitals[0][iPoland], 1)
			utils.makeUnit(iWarrior, iPoland, tCapitals[0][iPoland], 1)
                if ( pTurkey.isHuman() ):
                    utils.makeUnit(iSettler, iTurkey, tCapitals[0][iTurkey], 1)
                    utils.makeUnit(iWarrior, iTurkey, tCapitals[0][iTurkey], 1)
                if ( pPortugal.isHuman() ):
                    utils.makeUnit(iSettler, iPortugal, tCapitals[0][iPortugal], 1)
                    utils.makeUnit(iWarrior, iPortugal, tCapitals[0][iPortugal], 1)
                if ( pInca.isHuman() ):
                    utils.makeUnit(iSettler, iInca, tCapitals[0][iInca], 1)
                    utils.makeUnit(iWarrior, iInca, tCapitals[0][iInca], 1)
		if ( pItaly.isHuman() ):
		    utils.makeUnit(iSettler, iItaly, tCapitals[0][iItaly], 1)
		    utils.makeUnit(iWarrior, iItaly, tCapitals[0][iItaly], 1)
                if ( pMongolia.isHuman() ):
                    utils.makeUnit(iSettler, iMongolia, tCapitals[0][iMongolia], 1)
                    utils.makeUnit(iScout, iMongolia, tCapitals[0][iMongolia], 1)
                if ( pAztecs.isHuman() ):
                    utils.makeUnit(iSettler, iAztecs, tCapitals[0][iAztecs], 1)
                    utils.makeUnit(iScout, iAztecs, tCapitals[0][iAztecs], 1)
		if ( pMughals.isHuman() ):
		    utils.makeUnit(iSettler, iMughals, tCapitals[0][iMughals], 1)
		    utils.makeUnit(iWarrior, iMughals, tCapitals[0][iMughals], 1)
		if ( pThailand.isHuman() ):
		    utils.makeUnit(iSettler, iThailand, tCapitals[0][iThailand], 1)
		    utils.makeUnit(iWarrior, iThailand, tCapitals[0][iThailand], 1)
		if pCongo.isHuman():
			utils.makeUnit(iSettler, iCongo, tCapitals[0][iCongo], 1)
			utils.makeUnit(iWarrior, iCongo, tCapitals[0][iCongo], 1)
		if pGermany.isHuman():
			utils.makeUnit(iSettler, iGermany, tCapitals[0][iGermany], 1)
			utils.makeUnit(iWarrior, iGermany, tCapitals[0][iGermany], 1)
                if ( pAmerica.isHuman() ):
                    utils.makeUnit(iSettler, iAmerica, tCapitals[0][iAmerica], 1)
                    utils.makeUnit(iWarrior, iAmerica, tCapitals[0][iAmerica], 1)
		if pArgentina.isHuman():
			utils.makeUnit(iSettler, iArgentina, tCapitals[0][iArgentina], 1)
			utils.makeUnit(iWarrior, iArgentina, tCapitals[0][iArgentina], 1)
		if pBrazil.isHuman():
			utils.makeUnit(iSettler, iBrazil, tCapitals[0][iBrazil], 1)
			utils.makeUnit(iWarrior, iBrazil, tCapitals[0][iBrazil], 1)


        def create4000BCstartingUnits( self ):

                utils.makeUnit(iSettler, iEgypt, tCapitals[0][iEgypt], 1)
                utils.makeUnit(iWarrior, iEgypt, tCapitals[0][iEgypt], 1)

		if ( pIndia.isHuman() ):
                    utils.makeUnit(iSettler, iIndia, tCapitals[0][iIndia], 1)
                    utils.makeUnit(iWarrior, iIndia, tCapitals[0][iIndia], 1)

                utils.makeUnit(iSettler, iChina, tCapitals[0][iChina], 1)
                utils.makeUnit(iWarrior, iChina, tCapitals[0][iChina], 1)

                utils.makeUnit(iSettler, iBabylonia, tCapitals[0][iBabylonia], 1)
                utils.makeUnit(iWarrior, iBabylonia, tCapitals[0][iBabylonia], 1)

                if ( pGreece.isHuman() ):
                    utils.makeUnit(iSettler, iGreece, tCapitals[0][iGreece], 1)
                    utils.makeUnit(iScout, iGreece, tCapitals[0][iGreece], 1)
                if ( pPersia.isHuman() ):
                    utils.makeUnit(iSettler, iPersia, tCapitals[0][iPersia], 1)
                    utils.makeUnit(iScout, iPersia, tCapitals[0][iPersia], 1)
                if ( pCarthage.isHuman() ):
                    utils.makeUnit(iSettler, iCarthage, tCapitals[0][iCarthage], 1)
                    utils.makeUnit(iScout, iCarthage, tCapitals[0][iCarthage], 1)
                if ( pRome.isHuman() ):
                    utils.makeUnit(iSettler, iRome, tCapitals[0][iRome], 1)
                    utils.makeUnit(iWarrior, iRome, tCapitals[0][iRome], 1)
                if ( pJapan.isHuman() ):
                    utils.makeUnit(iSettler, iJapan, tCapitals[0][iJapan], 1)
                    utils.makeUnit(iWarrior, iJapan, tCapitals[0][iJapan], 1)
		if ( pTamils.isHuman() ):
		    utils.makeUnit(iSettler, iTamils, tCapitals[0][iTamils], 1)
		    utils.makeUnit(iWarrior, iTamils, tCapitals[0][iTamils], 1)
                if ( pEthiopia.isHuman() ):
                    utils.makeUnit(iSettler, iEthiopia, tCapitals[0][iEthiopia], 1)
                    utils.makeUnit(iWarrior, iEthiopia, tCapitals[0][iEthiopia], 1)
		if ( pKorea.isHuman() ):
                    utils.makeUnit(iSettler, iKorea, tCapitals[0][iKorea], 1)
                    utils.makeUnit(iWarrior, iKorea, tCapitals[0][iKorea], 1)
                if ( pMaya.isHuman() ):
                    utils.makeUnit(iSettler, iMaya, tCapitals[0][iMaya], 1)
                    utils.makeUnit(iWarrior, iMaya, tCapitals[0][iMaya], 1)
                if ( pByzantium.isHuman() ):
                    utils.makeUnit(iSettler, iByzantium, tCapitals[0][iByzantium], 1)
                    utils.makeUnit(iWarrior, iByzantium, tCapitals[0][iByzantium], 1)
                if ( pVikings.isHuman() ):
                    utils.makeUnit(iSettler, iVikings, tCapitals[0][iVikings], 1)
                    utils.makeUnit(iScout, iVikings, tCapitals[0][iVikings], 1)
                if ( pArabia.isHuman() ):
                    utils.makeUnit(con.iSettler, iArabia, tCapitals[0][iArabia], 1)
                    utils.makeUnit(con.iWarrior, iArabia, tCapitals[0][iArabia], 1)
		if pTibet.isHuman():
			utils.makeUnit(con.iSettler, iTibet, tCapitals[0][iTibet], 1)
			utils.makeUnit(con.iWarrior, iTibet, tCapitals[0][iTibet], 1)
                if ( pKhmer.isHuman() ):
                    utils.makeUnit(iSettler, iKhmer, tCapitals[0][iKhmer], 1)
                    utils.makeUnit(iWarrior, iKhmer, tCapitals[0][iKhmer], 1)
		if ( pIndonesia.isHuman() ):
			utils.makeUnit(iSettler, iIndonesia, tCapitals[0][iIndonesia], 1)
			utils.makeUnit(iWarrior, iIndonesia, tCapitals[0][iIndonesia], 1)
		if pMoors.isHuman():
			utils.makeUnit(iSettler, iMoors, tCapitals[0][iMoors], 1)
			utils.makeUnit(iWarrior, iMoors, tCapitals[0][iMoors], 1)
                if ( pSpain.isHuman() ):
                    utils.makeUnit(iSettler, iSpain, tCapitals[0][iSpain], 1)
                    utils.makeUnit(iWarrior, iSpain, tCapitals[0][iSpain], 1)
                if ( pFrance.isHuman() ):
                    utils.makeUnit(iSettler, iFrance, tCapitals[0][iFrance], 1)
                    utils.makeUnit(iWarrior, iFrance, tCapitals[0][iFrance], 1)
                if ( pEngland.isHuman() ):
                    utils.makeUnit(iSettler, iEngland, tCapitals[0][iEngland], 1)
                    utils.makeUnit(iWarrior, iEngland, tCapitals[0][iEngland], 1)
                if ( pHolyRome.isHuman() ):
                    utils.makeUnit(iSettler, iHolyRome, tCapitals[0][iHolyRome], 1)
                    utils.makeUnit(iScout, iHolyRome, tCapitals[0][iHolyRome], 1)
                if ( pRussia.isHuman() ):
                    utils.makeUnit(iSettler, iRussia, tCapitals[0][iRussia], 1)
                    utils.makeUnit(iScout, iRussia, tCapitals[0][iRussia], 1)
                if ( pNetherlands.isHuman() ):
                    utils.makeUnit(iSettler, iNetherlands, tCapitals[0][iNetherlands], 1)
                    utils.makeUnit(iWarrior, iNetherlands, tCapitals[0][iNetherlands], 1)
                if ( pMali.isHuman() ):
                    utils.makeUnit(iSettler, iMali, tCapitals[0][iMali], 1)
                    utils.makeUnit(iWarrior, iMali, tCapitals[0][iMali], 1)
		if pPoland.isHuman():
			utils.makeUnit(iSettler, iPoland, tCapitals[0][iPoland], 1)
			utils.makeUnit(iWarrior, iPoland, tCapitals[0][iPoland], 1)
                if ( pTurkey.isHuman() ):
                    utils.makeUnit(iSettler, iTurkey, tCapitals[0][iTurkey], 1)
                    utils.makeUnit(iWarrior, iTurkey, tCapitals[0][iTurkey], 1)
                if ( pPortugal.isHuman() ):
                    utils.makeUnit(iSettler, iPortugal, tCapitals[0][iPortugal], 1)
                    utils.makeUnit(iWarrior, iPortugal, tCapitals[0][iPortugal], 1)
                if ( pInca.isHuman() ):
                    utils.makeUnit(iSettler, iInca, tCapitals[0][iInca], 1)
                    utils.makeUnit(iWarrior, iInca, tCapitals[0][iInca], 1)
		if pItaly.isHuman():
			utils.makeUnit(iSettler, iItaly, tCapitals[0][iItaly], 1)
			utils.makeUnit(iWarrior, iItaly, tCapitals[0][iItaly], 1)
                if (pMongolia.isHuman() ):
                    utils.makeUnit(iSettler, iMongolia, tCapitals[0][iMongolia], 1)
                    utils.makeUnit(iScout, iMongolia, tCapitals[0][iMongolia], 1)
                if ( pAztecs.isHuman() ):
                    utils.makeUnit(iSettler, iAztecs, tCapitals[0][iAztecs], 1)
                    utils.makeUnit(iScout, iAztecs, tCapitals[0][iAztecs], 1)
		if pMughals.isHuman():
			utils.makeUnit(iSettler, iMughals, tCapitals[0][iMughals], 1)
			utils.makeUnit(iWarrior, iMughals, tCapitals[0][iMughals], 1)
		if pThailand.isHuman():
			utils.makeUnit(iSettler, iThailand, tCapitals[0][iThailand], 1)
			utils.makeUnit(iWarrior, iThailand, tCapitals[0][iThailand], 1)
		if pCongo.isHuman():
			utils.makeUnit(iSettler, iCongo, tCapitals[0][iCongo], 1)
			utils.makeUnit(iWarrior, iCongo, tCapitals[0][iCongo], 1)
		if pGermany.isHuman():
			utils.makeUnit(iSettler, iGermany, tCapitals[0][iGermany], 1)
			utils.makeUnit(iWarrior, iGermany, tCapitals[0][iGermany], 1)
                if ( pAmerica.isHuman() ):
                    utils.makeUnit(iSettler, iAmerica, tCapitals[0][iAmerica], 1)
                    utils.makeUnit(iWarrior, iAmerica, tCapitals[0][iAmerica], 1)
		if pArgentina.isHuman():
			utils.makeUnit(iSettler, iArgentina, tCapitals[0][iArgentina], 1)
			utils.makeUnit(iWarrior, iArgentina, tCapitals[0][iArgentina], 1)
		if pBrazil.isHuman():
			utils.makeUnit(iSettler, iBrazil, tCapitals[0][iBrazil], 1)
			utils.makeUnit(iWarrior, iBrazil, tCapitals[0][iBrazil], 1)
			
			
	def assign1700ADTechs(self):
	
		lMedievalTechs = [con.iFishing, con.iTheWheel, con.iAgriculture, con.iHunting, con.iMysticism, con.iMining,
				  con.iSailing, con.iPottery, con.iAnimalHusbandry, con.iArchery, con.iMeditation, con.iPolytheism, con.iMasonry,
				  con.iHorsebackRiding, con.iPriesthood, con.iMonotheism, con.iBronzeWorking,
				  con.iWriting, con.iMetalCasting, con.iIronWorking,
				  con.iAesthetics, con.iMathematics, con.iAlphabet, con.iMonarchy, con.iCompass,
				  con.iLiterature, con.iCalendar, con.iConstruction, con.iCurrency, con.iMachinery,
				  con.iDrama, con.iEngineering, con.iCodeOfLaws, con.iFeudalism,
				  con.iMusic, con.iPhilosophy, con.iCivilService, con.iTheology, con.iOptics,
				  con.iPatronage, con.iDivineRight, con.iPaper, con.iGuilds,
				  con.iEducation, con.iBanking, con.iGunpowder]
				  
		lChineseTechs = [con.iPrintingPress, con.iAstronomy]
		lChineseTechs.extend(lMedievalTechs)
		for iTech in lChineseTechs:
			teamChina.setHasTech(iTech, True, iChina, False, False)
			
		lPersianTechs = [con.iMilitaryTradition, con.iPrintingPress, con.iAstronomy, con.iLiberalism]
		lPersianTechs.extend(lMedievalTechs)
		for iTech in lPersianTechs:
			teamPersia.setHasTech(iTech, True, iPersia, False, False)
			
		lKoreanTechs = [con.iPrintingPress]
		lKoreanTechs.extend(lMedievalTechs)
		for iTech in lKoreanTechs:
			teamKorea.setHasTech(iTech, True, iKorea, False, False)
			
		lJapaneseTechs = [con.iMilitaryTradition, con.iPrintingPress]
		lJapaneseTechs.extend(lMedievalTechs)
		for iTech in lJapaneseTechs:
			teamJapan.setHasTech(iTech, True, iJapan, False, False)
			
		lSwedishTechs = [con.iPrintingPress, con.iMilitaryTradition, con.iMilitaryScience, con.iReplaceableParts, con.iLiberalism, con.iAstronomy]
		lSwedishTechs.extend(lMedievalTechs)
		for iTech in lSwedishTechs:
			teamVikings.setHasTech(iTech, True, iVikings, False, False)
			
		lSpanishTechs = [con.iPrintingPress, con.iMilitaryTradition, con.iMilitaryScience, con.iReplaceableParts, con.iLiberalism, con.iAstronomy]
		lSpanishTechs.extend(lMedievalTechs)
		for iTech in lSpanishTechs:
			teamSpain.setHasTech(iTech, True, iSpain, False, False)
			
		lFrenchTechs = [con.iPrintingPress, con.iMilitaryTradition, con.iMilitaryScience, con.iReplaceableParts, con.iRifling, con.iLiberalism,
				con.iAstronomy, con.iConstitution]
		lFrenchTechs.extend(lMedievalTechs)
		for iTech in lFrenchTechs:
			teamFrance.setHasTech(iTech, True, iFrance, False, False)
			
		lEnglishTechs = [con.iPrintingPress, con.iMilitaryScience, con.iReplaceableParts, con.iRifling, con.iLiberalism,
				 con.iConstitution, con.iAstronomy]
		lEnglishTechs.extend(lMedievalTechs)
		for iTech in lEnglishTechs:
			teamEngland.setHasTech(iTech, True, iEngland, False, False)
			
		lAustrianTechs = [con.iPrintingPress, con.iMilitaryTradition, con.iMilitaryScience, con.iReplaceableParts, con.iRifling,
				  con.iAstronomy]
		lAustrianTechs.extend(lMedievalTechs)
		for iTech in lAustrianTechs:
			teamHolyRome.setHasTech(iTech, True, iHolyRome, False, False)
			
		lRussianTechs = [con.iPrintingPress, con.iMilitaryTradition, con.iMilitaryScience, con.iReplaceableParts]
		lRussianTechs.extend(lMedievalTechs)
		for iTech in lRussianTechs:
			teamRussia.setHasTech(iTech, True, iRussia, False, False)
			
		lPolishTechs = [con.iPrintingPress, con.iMilitaryTradition, con.iReplaceableParts, con.iAstronomy, con.iLiberalism,
				con.iConstitution]
		lPolishTechs.extend(lMedievalTechs)
		for iTech in lPolishTechs:
			teamPoland.setHasTech(iTech, True, iPoland, False, False)
			
		lPortugueseTechs = [con.iPrintingPress, con.iMilitaryScience, con.iReplaceableParts, con.iAstronomy,
				    con.iLiberalism]
		lPortugueseTechs.extend(lMedievalTechs)
		for iTech in lPortugueseTechs:
			teamPortugal.setHasTech(iTech, True, iPortugal, False, False)
			
		lMughalTechs = [con.iPrintingPress, con.iAstronomy, con.iLiberalism, con.iConstitution]
		lMughalTechs.extend(lMedievalTechs)
		for iTech in lMughalTechs:
			teamMughals.setHasTech(iTech, True, iMughals, False, False)
			
		lTurkishTechs = [con.iPrintingPress, con.iMilitaryScience, con.iReplaceableParts, con.iMilitaryTradition]
		lTurkishTechs.extend(lMedievalTechs)
		for iTech in lTurkishTechs:
			teamTurkey.setHasTech(iTech, True, iTurkey, False, False)
			
		lThaiTechs = [con.iPrintingPress]
		lThaiTechs.extend(lMedievalTechs)
		for iTech in lThaiTechs:
			teamThailand.setHasTech(iTech, True, iThailand, False, False)
			
		lCongoleseTechs = []
		lCongoleseTechs.extend(lMedievalTechs)
		lCongoleseTechs.remove(con.iBanking)
		lCongoleseTechs.remove(con.iEducation)
		lCongoleseTechs.remove(con.iGunpowder)
		lCongoleseTechs.remove(con.iDivineRight)
		lCongoleseTechs.remove(con.iOptics)
		for iTech in lCongoleseTechs:
			teamCongo.setHasTech(iTech, True, iCongo, False, False)
			
		lDutchTechs = [con.iPrintingPress, con.iMilitaryScience, con.iReplaceableParts, con.iRifling, con.iLiberalism, con.iConstitution,
			       con.iAstronomy]
		lDutchTechs.extend(lMedievalTechs)
		for iTech in lDutchTechs:
			teamNetherlands.setHasTech(iTech, True, iNetherlands, False, False)
			
		lGermanTechs = [con.iPrintingPress, con.iMilitaryTradition, con.iMilitaryScience, con.iReplaceableParts, con.iRifling, con.iLiberalism,
				con.iConstitution, con.iAstronomy]
		lGermanTechs.extend(lMedievalTechs)
		for iTech in lGermanTechs:
			teamGermany.setHasTech(iTech, True, iGermany, False, False)
			
		for iTech in lMedievalTechs:
			teamIndependent.setHasTech(iTech, True, iIndependent, False, False)
			teamIndependent2.setHasTech(iTech, True, iIndependent2, False, False)


        def assign600ADTechs( self ):
            
                iCiv = iChina
                teamChina.setHasTech(con.iMining, True, iCiv, False, False)
                teamChina.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                teamChina.setHasTech(con.iIronWorking, True, iCiv, False, False)
                teamChina.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                teamChina.setHasTech(con.iMachinery, True, iCiv, False, False)
                teamChina.setHasTech(con.iMysticism, True, iCiv, False, False)
                teamChina.setHasTech(con.iPolytheism, True, iCiv, False, False)
                teamChina.setHasTech(con.iMeditation, True, iCiv, False, False)
                teamChina.setHasTech(con.iPriesthood, True, iCiv, False, False)
                teamChina.setHasTech(con.iMasonry, True, iCiv, False, False)
                teamChina.setHasTech(con.iMonarchy, True, iCiv, False, False)
                teamChina.setHasTech(con.iFishing, True, iCiv, False, False)
                teamChina.setHasTech(con.iSailing, True, iCiv, False, False)
                teamChina.setHasTech(con.iTheWheel, True, iCiv, False, False)
                teamChina.setHasTech(con.iPottery, True, iCiv, False, False)
                teamChina.setHasTech(con.iAgriculture, True, iCiv, False, False)
                teamChina.setHasTech(con.iWriting, True, iCiv, False, False)
                teamChina.setHasTech(con.iMathematics, True, iCiv, False, False)
                teamChina.setHasTech(con.iCalendar, True, iCiv, False, False)
                teamChina.setHasTech(con.iConstruction, True, iCiv, False, False)
                teamChina.setHasTech(con.iCurrency, True, iCiv, False, False)
                teamChina.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                teamChina.setHasTech(con.iCivilService, True, iCiv, False, False)
                teamChina.setHasTech(con.iHunting, True, iCiv, False, False)
                teamChina.setHasTech(con.iArchery, True, iCiv, False, False)
                teamChina.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                teamChina.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
                teamChina.setHasTech(con.iAesthetics, True, iCiv, False, False)
                teamChina.setHasTech(con.iDrama, True, iCiv, False, False)
                teamChina.setHasTech(con.iMusic, True, iCiv, False, False)
                iCiv = iJapan
		lJapaneseTechs = [con.iMining, con.iBronzeWorking, con.iIronWorking, con.iMetalCasting, con.iMachinery, con.iMysticism, \
				  con.iPolytheism, con.iMeditation, con.iPriesthood, con.iMasonry, con.iMonarchy, con.iFishing, \
				  con.iSailing, con.iTheWheel, con.iPottery, con.iAgriculture, con.iWriting, con.iMathematics, \
				  con.iConstruction, con.iCurrency, con.iCodeOfLaws, con.iCivilService, con.iHunting, con.iArchery, \
				  con.iAnimalHusbandry, con.iAesthetics]
		for iTech in lJapaneseTechs:
			teamJapan.setHasTech(iTech, True, iCiv, False, False)
                iCiv = iVikings
                teamVikings.setHasTech(con.iMining, True, iCiv, False, False)
                teamVikings.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                teamVikings.setHasTech(con.iIronWorking, True, iCiv, False, False)
                teamVikings.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                teamVikings.setHasTech(con.iMachinery, True, iCiv, False, False)
                teamVikings.setHasTech(con.iMysticism, True, iCiv, False, False)
                teamVikings.setHasTech(con.iPolytheism, True, iCiv, False, False)
                teamVikings.setHasTech(con.iMasonry, True, iCiv, False, False)
                teamVikings.setHasTech(con.iPriesthood, True, iCiv, False, False)
                teamVikings.setHasTech(con.iMonarchy, True, iCiv, False, False)
                teamVikings.setHasTech(con.iFishing, True, iCiv, False, False)
                teamVikings.setHasTech(con.iSailing, True, iCiv, False, False)
                teamVikings.setHasTech(con.iTheWheel, True, iCiv, False, False)
                teamVikings.setHasTech(con.iPottery, True, iCiv, False, False)
                teamVikings.setHasTech(con.iAgriculture, True, iCiv, False, False)
                teamVikings.setHasTech(con.iWriting, True, iCiv, False, False)
                teamVikings.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                teamVikings.setHasTech(con.iFeudalism, True, iCiv, False, False)
                teamVikings.setHasTech(con.iAlphabet, True, iCiv, False, False)
                teamVikings.setHasTech(con.iMathematics, True, iCiv, False, False)
                teamVikings.setHasTech(con.iCurrency, True, iCiv, False, False)
                teamVikings.setHasTech(con.iHunting, True, iCiv, False, False)
                teamVikings.setHasTech(con.iArchery, True, iCiv, False, False)
                teamVikings.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                iCiv = iArabia
                teamArabia.setHasTech(con.iMining, True, iCiv, False, False)
                teamArabia.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                teamArabia.setHasTech(con.iIronWorking, True, iCiv, False, False)
                teamArabia.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                teamArabia.setHasTech(con.iMachinery, True, iCiv, False, False)
                teamArabia.setHasTech(con.iMysticism, True, iCiv, False, False)
                teamArabia.setHasTech(con.iPolytheism, True, iCiv, False, False)
                teamArabia.setHasTech(con.iMasonry, True, iCiv, False, False)
                teamArabia.setHasTech(con.iPriesthood, True, iCiv, False, False)
                teamArabia.setHasTech(con.iMonotheism, True, iCiv, False, False)
                teamArabia.setHasTech(con.iTheology, True, iCiv, False, False)
                teamArabia.setHasTech(con.iMonarchy, True, iCiv, False, False)
                teamArabia.setHasTech(con.iDivineRight, True, iCiv, False, False)
                teamArabia.setHasTech(con.iFishing, True, iCiv, False, False)
                teamArabia.setHasTech(con.iTheWheel, True, iCiv, False, False)
                teamArabia.setHasTech(con.iPottery, True, iCiv, False, False)
                teamArabia.setHasTech(con.iAgriculture, True, iCiv, False, False)
                teamArabia.setHasTech(con.iWriting, True, iCiv, False, False)
                teamArabia.setHasTech(con.iFeudalism, True, iCiv, False, False)
                teamArabia.setHasTech(con.iAlphabet, True, iCiv, False, False)
                teamArabia.setHasTech(con.iMathematics, True, iCiv, False, False)
                teamArabia.setHasTech(con.iConstruction, True, iCiv, False, False)
                teamArabia.setHasTech(con.iCurrency, True, iCiv, False, False)
                teamArabia.setHasTech(con.iHunting, True, iCiv, False, False)
                teamArabia.setHasTech(con.iArchery, True, iCiv, False, False)
                teamArabia.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                teamArabia.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
                iCiv = iIndependent
                teamIndependent.setHasTech(con.iMining, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iIronWorking, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iMysticism, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iPolytheism, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iMeditation, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iMasonry, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iPriesthood, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iMonarchy, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iFishing, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iSailing, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iTheWheel, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iPottery, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iAgriculture, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iWriting, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iAlphabet, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iMathematics, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iCurrency, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iHunting, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iArchery, True, iCiv, False, False)
                teamIndependent.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                iCiv = iIndependent2
                teamIndependent2.setHasTech(con.iMining, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iIronWorking, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iMysticism, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iPolytheism, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iMeditation, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iMasonry, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iPriesthood, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iMonarchy, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iFishing, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iSailing, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iTheWheel, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iPottery, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iAgriculture, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iWriting, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iAlphabet, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iMathematics, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iCurrency, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iHunting, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iArchery, True, iCiv, False, False)
                teamIndependent2.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                iCiv = iNative
                teamNative.setHasTech(con.iHunting, True, iCiv, False, False)
                teamNative.setHasTech(con.iArchery, True, iCiv, False, False)
                iCiv = iByzantium #Byzantium
                teamByzantium.setHasTech(con.iMining, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iIronWorking, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iMachinery, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iMysticism, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iPolytheism, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iMasonry, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iPriesthood, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iMonotheism, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iTheology, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iMonarchy, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iFishing, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iSailing, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iTheWheel, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iPottery, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iAgriculture, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iWriting, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iAlphabet, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iMathematics, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iConstruction, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iCurrency, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iHunting, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iArchery, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iLiterature, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iDrama, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iAesthetics, True, iCiv, False, False)
                teamByzantium.setHasTech(con.iCalendar, True, iCiv, False, False)

		lKoreanTechs = [con.iMining, con.iBronzeWorking, con.iIronWorking, con.iMetalCasting, con.iMachinery, con.iMysticism, con.iPolytheism, \
		 con.iMeditation, con.iPriesthood, con.iMasonry, con.iMonarchy, con.iFishing, con.iSailing, con.iTheWheel, con.iPottery, \
		 con.iAgriculture, con.iWriting, con.iMathematics, con.iCalendar, con.iConstruction, con.iCurrency, con.iCodeOfLaws, con.iHunting, con.iArchery, \
		 con.iAnimalHusbandry, con.iHorsebackRiding, con.iAesthetics, con.iDrama, con.iMonotheism]

		for iTech in lKoreanTechs:
			teamKorea.setHasTech(iTech, True, iKorea, False, False)

		lSeljukTechs = [con.iMining, con.iBronzeWorking, con.iIronWorking, con.iMetalCasting, con.iMachinery, con.iMysticism, con.iPolytheism, con.iMasonry, \
				con.iPriesthood, con.iMonotheism, con.iTheology, con.iMonarchy, con.iDivineRight, con.iFishing, con.iTheWheel, con.iPottery, con.iAgriculture, \
				con.iWriting, con.iCodeOfLaws, con.iFeudalism, con.iAlphabet, con.iMathematics, con.iConstruction, con.iCurrency, con.iHunting, con.iArchery, \
				con.iAnimalHusbandry, con.iHorsebackRiding, con.iLiterature, con.iDrama, con.iAesthetics, con.iMusic, con.iCalendar]

		for iTech in lSeljukTechs:
			teamSeljuks.setHasTech(iTech, True, iSeljuks, False, False)
                
                
        def assignTechs( self, iCiv ):
                if (utils.getReborn(iCiv) == 0):
			if iCiv == iIndia:
				lIndianTechs = [con.iMysticism, con.iFishing, con.iTheWheel, con.iAgriculture, con.iPottery, \
						con.iHunting, con.iMining, con.iWriting, con.iMeditation, con.iAnimalHusbandry, \
						con.iBronzeWorking, con.iArchery, con.iSailing]
				for iTech in lIndianTechs:
					teamIndia.setHasTech(iTech, True, iCiv, False, False)
                        if (iCiv == iGreece):
                                teamGreece.setHasTech(con.iMining, True, iCiv, False, False)
                                teamGreece.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamGreece.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamGreece.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamGreece.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamGreece.setHasTech(con.iSailing, True, iCiv, False, False)
                                teamGreece.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamGreece.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamGreece.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamGreece.setHasTech(con.iHunting, True, iCiv, False, False)
                        if (iCiv == iPersia):
                                teamPersia.setHasTech(con.iMining, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iSailing, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iMonotheism, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
				# Leoreth: Babylonian UHV: make them lose if they don't have Monarchy already
				if sd.scriptDict['lBabylonianTechs'][2] == -1:
					sd.scriptDict['lGoals'][iBabylonia][0] = 0
                        if (iCiv == iCarthage):
                                teamCarthage.setHasTech(con.iMining, True, iCiv, False, False)
                                teamCarthage.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamCarthage.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamCarthage.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamCarthage.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamCarthage.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamCarthage.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamCarthage.setHasTech(con.iSailing, True, iCiv, False, False)
                                teamCarthage.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamCarthage.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamCarthage.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamCarthage.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamCarthage.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamCarthage.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                        if (iCiv == iRome):
                                teamRome.setHasTech(con.iMining, True, iCiv, False, False)
                                teamRome.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamRome.setHasTech(con.iIronWorking, True, iCiv, False, False)
                                teamRome.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                                teamRome.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamRome.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamRome.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamRome.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamRome.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamRome.setHasTech(con.iSailing, True, iCiv, False, False)
                                teamRome.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamRome.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamRome.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamRome.setHasTech(con.iAlphabet, True, iCiv, False, False)
                                teamRome.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamRome.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamRome.setHasTech(con.iMathematics, True, iCiv, False, False)
                        if (iCiv == iJapan):
				lJapaneseTechs = [con.iMining, con.iBronzeWorking, con.iIronWorking, con.iMetalCasting, con.iMachinery, con.iMysticism, \
						  con.iPolytheism, con.iMeditation, con.iPriesthood, con.iMasonry, con.iMonarchy, con.iFishing, \
						  con.iSailing, con.iTheWheel, con.iPottery, con.iAgriculture, con.iWriting, con.iMathematics, \
						  con.iConstruction, con.iCurrency, con.iCodeOfLaws, con.iCivilService, con.iHunting, con.iArchery, \
						  con.iAnimalHusbandry]
				for iTech in lJapaneseTechs:
					teamJapan.setHasTech(iTech, True, iCiv, False, False)
			if iCiv == iTamils:
				lTamilTechs = [con.iMining, con.iBronzeWorking, con.iMysticism, con.iPolytheism, con.iMeditation, con.iPriesthood,
						con.iMasonry, con.iFishing, con.iSailing, con.iMonarchy, con.iTheWheel, con.iPottery, con.iWriting,
						con.iHunting, con.iArchery, con.iAnimalHusbandry, con.iHorsebackRiding, con.iAgriculture,
						con.iAesthetics, con.iIronWorking]
				for iTech in lTamilTechs:
					teamTamils.setHasTech(iTech, True, iCiv, False, False)
                        if (iCiv == iEthiopia):
                                teamEthiopia.setHasTech(con.iMining, True, iCiv, False, False)
                                teamEthiopia.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamEthiopia.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamEthiopia.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamEthiopia.setHasTech(con.iMeditation, True, iCiv, False, False)
                                teamEthiopia.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamEthiopia.setHasTech(con.iMonotheism, True, iCiv, False, False) #
                                teamEthiopia.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamEthiopia.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamEthiopia.setHasTech(con.iSailing, True, iCiv, False, False)
                                teamEthiopia.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamEthiopia.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamEthiopia.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamEthiopia.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamEthiopia.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamEthiopia.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamEthiopia.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamEthiopia.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
			if (iCiv == iKorea):
				lKoreanTechs = [con.iMining, con.iBronzeWorking, con.iIronWorking, con.iMysticism, con.iPolytheism, \
						con.iMeditation, con.iPriesthood, con.iMasonry, con.iMonarchy, con.iFishing, con.iSailing, con.iTheWheel, con.iPottery, \
						con.iAgriculture, con.iWriting, con.iMathematics, con.iCalendar, con.iConstruction, con.iCurrency, con.iCodeOfLaws, con.iHunting, con.iArchery, \
						con.iAnimalHusbandry, con.iHorsebackRiding, con.iAesthetics]
				for iTech in lKoreanTechs:
					teamKorea.setHasTech(iTech, True, iCiv, False, False)
                        if (iCiv == iMaya):
                                teamMaya.setHasTech(con.iMining, True, iCiv, False, False)
                                teamMaya.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamMaya.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamMaya.setHasTech(con.iMeditation, True, iCiv, False, False)
                                teamMaya.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamMaya.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamMaya.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamMaya.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamMaya.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamMaya.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamMaya.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamMaya.setHasTech(con.iHunting, True, iCiv, False, False)
                        if (iCiv == iByzantium):
				teamByzantium.setHasTech(con.iMining, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iIronWorking, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iMetalCasting, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iMachinery, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iMysticism, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iPolytheism, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iMasonry, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iPriesthood, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iMonotheism, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iTheology, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iMonarchy, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iFishing, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iSailing, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iTheWheel, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iPottery, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iAgriculture, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iWriting, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iAlphabet, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iMathematics, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iConstruction, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iCurrency, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iHunting, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iArchery, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iLiterature, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iDrama, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iAesthetics, True, iCiv, False, False)
				teamByzantium.setHasTech(con.iCalendar, True, iCiv, False, False)
                        if (iCiv == iVikings):
                                teamVikings.setHasTech(con.iMining, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iIronWorking, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iMachinery, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iSailing, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iFeudalism, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iAlphabet, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iConstruction, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iCurrency, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamVikings.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
                        if (iCiv == iArabia):
                                teamArabia.setHasTech(con.iMining, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iIronWorking, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iMachinery, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iMonotheism, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iTheology, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iDivineRight, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iFeudalism, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iAlphabet, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iConstruction, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iCurrency, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamArabia.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
			if iCiv == iTibet:
				lTibetanTechs = [con.iMining, con.iBronzeWorking, con.iIronWorking, con.iMetalCasting, con.iMachinery, con.iMysticism, con.iPolytheism, con.iMasonry, \
						con.iPriesthood, con.iMonotheism, con.iMonarchy, con.iFishing, con.iTheWheel, con.iPottery, con.iAgriculture, \
						con.iWriting, con.iCodeOfLaws, con.iMathematics, con.iConstruction, con.iCurrency, con.iHunting, con.iArchery, \
						con.iAnimalHusbandry, con.iHorsebackRiding, con.iCalendar, con.iMeditation, con.iSailing, con.iTheology]
				for iTech in lTibetanTechs:
					teamTibet.setHasTech(iTech, True, iCiv, False, False)
                        if (iCiv == iKhmer):
                                teamKhmer.setHasTech(con.iMining, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iIronWorking, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iMachinery, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iMeditation, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iMonotheism, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iConstruction, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamKhmer.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
			if (iCiv == iIndonesia):
				lIndonesianTechs = [con.iMining, con.iBronzeWorking, con.iIronWorking, con.iMetalCasting, con.iMachinery, \
						con.iMysticism, con.iPolytheism, con.iMasonry, con.iMeditation, con.iPriesthood, con.iMonotheism, \
						con.iMonarchy, con.iFishing, con.iTheWheel, con.iPottery, con.iAgriculture, con.iWriting, con.iSailing, \
						con.iCodeOfLaws, con.iMathematics, con.iConstruction, con.iHunting, con.iArchery, con.iAnimalHusbandry, con.iHorsebackRiding]
				for iTech in lIndonesianTechs:
					teamIndonesia.setHasTech(iTech, True, iCiv, False, False)
			if iCiv == iMoors:
				lMoorishTechs = [con.iMining, con.iBronzeWorking, con.iIronWorking, con.iMetalCasting, con.iMachinery, con.iMysticism, con.iPolytheism, con.iMasonry, \
						con.iPriesthood, con.iMonotheism, con.iTheology, con.iMonarchy, con.iFishing, con.iTheWheel, con.iPottery, con.iAgriculture, \
						con.iWriting, con.iCodeOfLaws, con.iAlphabet, con.iMathematics, con.iConstruction, con.iCurrency, con.iHunting, con.iArchery, \
						con.iAnimalHusbandry, con.iHorsebackRiding, con.iLiterature, con.iAesthetics, con.iCalendar, con.iMeditation, con.iSailing, con.iPhilosophy]
				for iTech in lMoorishTechs:
					teamMoors.setHasTech(iTech, True, iCiv, False, False)
                        if (iCiv == iSpain):
                                teamSpain.setHasTech(con.iMining, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iIronWorking, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iMachinery, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iMonotheism, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iTheology, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iSailing, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iFeudalism, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iAlphabet, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iConstruction, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iCurrency, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
                                teamSpain.setHasTech(con.iCalendar, True, iCiv, False, False)
                        if (iCiv == iFrance):
                                teamFrance.setHasTech(con.iMining, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iIronWorking, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iMachinery, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iMysticism, True, iCiv, False, False)                                
                                teamFrance.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iMonotheism, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iTheology, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iSailing, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iFeudalism, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iAlphabet, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iConstruction, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iCurrency, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
                                teamFrance.setHasTech(con.iCalendar, True, iCiv, False, False)
                        if (iCiv == iEngland):
                                teamEngland.setHasTech(con.iMining, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iIronWorking, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iMachinery, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iMonotheism, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iTheology, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iSailing, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iFeudalism, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iAlphabet, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iConstruction, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iCurrency, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
                                teamEngland.setHasTech(con.iCalendar, True, iCiv, False, False)
                        if (iCiv == iHolyRome):
                                teamHolyRome.setHasTech(con.iMining, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iIronWorking, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iMachinery, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iMonotheism, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iTheology, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iFeudalism, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iAlphabet, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iConstruction, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iCurrency, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iFeudalism, True, iCiv, False, False)
                                teamHolyRome.setHasTech(con.iCalendar, True, iCiv, False, False)
                        if (iCiv == iRussia):
                                teamRussia.setHasTech(con.iMining, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iIronWorking, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iMachinery, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iMonotheism, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iTheology, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iFeudalism, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iAlphabet, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iConstruction, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iCurrency, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
                                teamRussia.setHasTech(con.iCalendar, True, iCiv, False, False)
                        if (iCiv == iHolland):
                                teamHolland.setHasTech(con.iMining, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iIronWorking, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iMachinery, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iMonotheism, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iTheology, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iDivineRight, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iSailing, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iFeudalism, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iGuilds, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iAlphabet, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iConstruction, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iEngineering, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iCurrency, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iGuilds, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iMeditation, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iCalendar, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iBanking, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iOptics, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iCivilService, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iCompass, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iGunpowder, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iPhilosophy, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iEducation, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iPaper, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iAstronomy, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iAesthetics, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iLiterature, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iDrama, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iMusic, True, iCiv, False, False)
                                teamHolland.setHasTech(con.iPatronage, True, iCiv, False, False)
                        if (iCiv == iMali):
                                teamMali.setHasTech(con.iMining, True, iCiv, False, False)
                                teamMali.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamMali.setHasTech(con.iIronWorking, True, iCiv, False, False)
                                teamMali.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                                teamMali.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamMali.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamMali.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamMali.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamMali.setHasTech(con.iMonotheism, True, iCiv, False, False)
                                teamMali.setHasTech(con.iTheology, True, iCiv, False, False)
                                teamMali.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamMali.setHasTech(con.iDivineRight, True, iCiv, False, False)
                                teamMali.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamMali.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamMali.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamMali.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamMali.setHasTech(con.iAlphabet, True, iCiv, False, False)
                                teamMali.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamMali.setHasTech(con.iConstruction, True, iCiv, False, False)
                                teamMali.setHasTech(con.iCurrency, True, iCiv, False, False)
                                teamMali.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamMali.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamMali.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamMali.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
			if iCiv == iPoland:
				lPolishTechs = [con.iMining, con.iBronzeWorking, con.iIronWorking, con.iMetalCasting, con.iMachinery, con.iMysticism,
						con.iPolytheism, con.iMasonry, con.iPriesthood, con.iMonotheism, con.iTheology, con.iMonarchy, con.iFishing,
						con.iSailing, con.iTheWheel, con.iPottery, con.iAgriculture, con.iWriting, con.iCodeOfLaws, con.iFeudalism,
						con.iAlphabet, con.iMathematics, con.iConstruction, con.iCurrency, con.iHunting, con.iArchery, con.iAnimalHusbandry,
						con.iHorsebackRiding, con.iMeditation, con.iAesthetics, con.iLiterature, con.iCalendar, con.iCivilService]
				for iTech in lPolishTechs:
					teamPoland.setHasTech(iTech, True, iCiv, False, False)
                        if (iCiv == iTurkey):
                                teamTurkey.setHasTech(con.iMining, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iIronWorking, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iMachinery, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iMonotheism, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iTheology, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iDivineRight, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iSailing, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iFeudalism, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iCivilService, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iGuilds, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iGunpowder, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iAlphabet, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iCalendar, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iConstruction, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iEngineering, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iCurrency, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamTurkey.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
                        if (iCiv == iPortugal):
                                teamPortugal.setHasTech(con.iMining, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iIronWorking, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iMachinery, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iMonotheism, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iTheology, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iDivineRight, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iSailing, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iFeudalism, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iGuilds, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iAlphabet, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iConstruction, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iEngineering, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iCurrency, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamPortugal.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
                        if (iCiv == iInca):
                                teamInca.setHasTech(con.iMining, True, iCiv, False, False)
                                teamInca.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamInca.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamInca.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamInca.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamInca.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamInca.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamInca.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamInca.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamInca.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamInca.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamInca.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                                teamInca.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamInca.setHasTech(con.iCurrency, True, iCiv, False, False)
                                teamInca.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamInca.setHasTech(con.iArchery, True, iCiv, False, False)
				teamInca.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                        if (iCiv == iMongolia):
                                teamMongolia.setHasTech(con.iMining, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iIronWorking, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iMachinery, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iMeditation, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iFeudalism, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iConstruction, True, iCiv, False, False)
				teamMongolia.setHasTech(con.iEngineering, True, iCiv, False, False)
				teamMongolia.setHasTech(con.iGuilds, True, iCiv, False, False)
				teamMongolia.setHasTech(con.iCurrency, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamMongolia.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)                              
                                teamMongolia.setHasTech(con.iGunpowder, True, iCiv, False, False)                              
                        if (iCiv == iAztecs):
                                teamAztecs.setHasTech(con.iMining, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iCalendar, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iCurrency, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamAztecs.setHasTech(con.iArchery, True, iCiv, False, False)
			if iCiv == iItaly:
				lItalianTechs =  [con.iMining, con.iBronzeWorking, con.iIronWorking, con.iMetalCasting, con.iMachinery, con.iMysticism, con.iPolytheism,
						con.iMasonry, con.iPriesthood, con.iMonotheism, con.iTheology, con.iMonarchy, con.iFishing, con.iSailing, con.iTheWheel,
						con.iPottery, con.iAgriculture, con.iWriting, con.iCodeOfLaws, con.iFeudalism, con.iGuilds, con.iAlphabet, con.iMathematics,
						con.iCalendar, con.iConstruction, con.iEngineering, con.iCurrency, con.iHunting, con.iArchery, con.iAnimalHusbandry,
						con.iHorsebackRiding, con.iAesthetics, con.iLiterature, con.iCompass, con.iCivilService]
				for iTech in lItalianTechs:
					teamItaly.setHasTech(iTech, True, iCiv, False, False)
			if iCiv == iMughals:
				lMughalTechs =  [con.iMining, con.iBronzeWorking, con.iIronWorking, con.iMetalCasting, con.iMachinery, con.iMysticism, con.iPolytheism, \
						con.iMasonry, con.iPriesthood, con.iMonotheism, con.iTheology, con.iMonarchy, con.iDivineRight, con.iFishing, con.iSailing, \
						con.iTheWheel, con.iPottery, con.iAgriculture, con.iWriting, con.iCodeOfLaws, con.iCivilService, \
						con.iGunpowder, con.iAlphabet, con.iMathematics, con.iCalendar, con.iConstruction, con.iCurrency, \
						con.iHunting, con.iArchery, con.iAnimalHusbandry, con.iHorsebackRiding, con.iGuilds, con.iAesthetics, con.iLiterature]
				for iTech in lMughalTechs:
					teamMughals.setHasTech(iTech, True, iCiv, False, False)
			if iCiv == iCongo:
				lCongoleseTechs = [con.iMining, con.iBronzeWorking, con.iIronWorking, con.iMetalCasting, con.iMysticism, con.iPolytheism,
						   con.iMasonry, con.iPriesthood, con.iMonotheism, con.iTheology, con.iMonarchy, con.iTheWheel, con.iPottery,
						   con.iAgriculture, con.iWriting, con.iAlphabet, con.iMathematics, con.iConstruction, con.iCurrency, con.iHunting,
						   con.iArchery, con.iAnimalHusbandry, con.iMachinery, con.iCivilService, con.iFishing, con.iCodeOfLaws]
				for iTech in lCongoleseTechs:
					teamCongo.setHasTech(iTech, True, iCiv, False, False)
			if iCiv == iThailand:
				lThaiTechs =   [con.iMining, con.iBronzeWorking, con.iIronWorking, con.iMetalCasting, con.iMachinery, con.iMysticism, con.iPolytheism, \
						con.iMasonry, con.iPriesthood, con.iMonotheism, con.iTheology, con.iMonarchy, con.iDivineRight, con.iFishing, con.iSailing, \
						con.iTheWheel, con.iPottery, con.iAgriculture, con.iWriting, con.iCodeOfLaws, con.iCivilService, \
						con.iGunpowder, con.iAlphabet, con.iMathematics, con.iCalendar, con.iConstruction, con.iCurrency, \
						con.iHunting, con.iArchery, con.iAnimalHusbandry, con.iHorsebackRiding, con.iAesthetics, con.iPaper, con.iDrama, con.iMusic]
				for iTech in lThaiTechs:
					teamThailand.setHasTech(iTech, True, iCiv, False, False)
			if iCiv == iGermany:
				lGermanTechs = [con.iMysticism, con.iMeditation, con.iPolytheism, con.iPriesthood, con.iMonotheism, con.iMonarchy, con.iLiterature, con.iCodeOfLaws, con.iDrama, con.iFeudalism, \
						con.iTheology, con.iMusic, con.iCivilService, con.iGuilds, con.iDivineRight, con.iMilitaryTradition, con.iConstitution, con.iLiberalism, \
						con.iFishing, con.iTheWheel, con.iAgriculture, con.iPottery, con.iPrintingPress, con.iEconomics, con.iAstronomy, con.iScientificMethod, con.iChemistry, \
						con.iAesthetics, con.iSailing, con.iWriting, con.iMathematics, con.iAlphabet, con.iCalendar, con.iCurrency, con.iPhilosophy, con.iPaper, con.iBanking, con.iEducation, \
						con.iHunting, con.iMining, con.iArchery, con.iMasonry, con.iAnimalHusbandry, con.iBronzeWorking, con.iHorsebackRiding, con.iIronWorking, con.iMetalCasting, \
						con.iCompass, con.iConstruction, con.iMachinery, con.iEngineering, con.iOptics, con.iGunpowder, con.iReplaceableParts, con.iMilitaryScience, con.iRifling, con.iPatronage]
				for iTech in lGermanTechs:
					teamGermany.setHasTech(iTech, True, iCiv, False, False)
                        if (iCiv == iAmerica):
                                for x in range(con.iDemocracy+1):
                                                teamAmerica.setHasTech(x, True, iCiv, False, False)
                                for x in range(con.iFishing, con.iChemistry+1):
                                                teamAmerica.setHasTech(x, True, iCiv, False, False)
                                for x in range(con.iHunting, con.iRifling+1):
                                                teamAmerica.setHasTech(x, True, iCiv, False, False)
                                teamAmerica.setHasTech(con.iSteamPower, True, iCiv, False, False)
				teamAmerica.setHasTech(con.iScientificMethod, True, iCiv, False, False)
			if iCiv == iArgentina:
				lArgentineTechs = [con.iMysticism, con.iMeditation, con.iPolytheism, con.iPriesthood, con.iMonotheism, con.iMonarchy, con.iLiterature, con.iCodeOfLaws, con.iDrama, con.iFeudalism, \
						con.iTheology, con.iMusic, con.iCivilService, con.iGuilds, con.iDivineRight, con.iMilitaryTradition, con.iConstitution, con.iLiberalism, \
						con.iFishing, con.iTheWheel, con.iAgriculture, con.iPottery, con.iPrintingPress, con.iEconomics, con.iAstronomy, con.iScientificMethod, con.iChemistry, \
						con.iAesthetics, con.iSailing, con.iWriting, con.iMathematics, con.iAlphabet, con.iCalendar, con.iCurrency, con.iPhilosophy, con.iPaper, con.iBanking, con.iEducation, \
						con.iHunting, con.iMining, con.iArchery, con.iMasonry, con.iAnimalHusbandry, con.iBronzeWorking, con.iHorsebackRiding, con.iIronWorking, con.iMetalCasting, \
						con.iCompass, con.iConstruction, con.iMachinery, con.iEngineering, con.iOptics, con.iGunpowder, con.iReplaceableParts, con.iMilitaryScience, con.iRifling, con.iPatronage, \
						con.iNationalism, con.iDemocracy, con.iSteamPower]
				for iTech in lArgentineTechs:
					teamArgentina.setHasTech(iTech, True, iCiv, False, False)
			if iCiv == iBrazil:
				lBrazilTechs = [con.iMysticism, con.iMeditation, con.iPolytheism, con.iPriesthood, con.iMonotheism, con.iMonarchy, con.iLiterature, con.iCodeOfLaws, con.iDrama, con.iFeudalism, \
						con.iTheology, con.iMusic, con.iCivilService, con.iGuilds, con.iDivineRight, con.iMilitaryTradition, con.iConstitution, con.iLiberalism, \
						con.iFishing, con.iTheWheel, con.iAgriculture, con.iPottery, con.iPrintingPress, con.iEconomics, con.iAstronomy, con.iScientificMethod, con.iChemistry, \
						con.iAesthetics, con.iSailing, con.iWriting, con.iMathematics, con.iAlphabet, con.iCalendar, con.iCurrency, con.iPhilosophy, con.iPaper, con.iBanking, con.iEducation, \
						con.iHunting, con.iMining, con.iArchery, con.iMasonry, con.iAnimalHusbandry, con.iBronzeWorking, con.iHorsebackRiding, con.iIronWorking, con.iMetalCasting, \
						con.iCompass, con.iConstruction, con.iMachinery, con.iEngineering, con.iOptics, con.iGunpowder, con.iReplaceableParts, con.iMilitaryScience, con.iRifling, con.iPatronage, \
						con.iNationalism, con.iDemocracy, con.iSteamPower]
				for iTech in lBrazilTechs:
					teamBrazil.setHasTech(iTech, True, iCiv, False, False)
                else:
                        if (iCiv == iRome):
                                teamRome.setHasTech(con.iMining, True, iCiv, False, False)
                                teamRome.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamRome.setHasTech(con.iIronWorking, True, iCiv, False, False)
                                teamRome.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                                teamRome.setHasTech(con.iMachinery, True, iCiv, False, False)
                                teamRome.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamRome.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamRome.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamRome.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamRome.setHasTech(con.iMonotheism, True, iCiv, False, False)
                                teamRome.setHasTech(con.iTheology, True, iCiv, False, False)
                                teamRome.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamRome.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamRome.setHasTech(con.iSailing, True, iCiv, False, False)
                                teamRome.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamRome.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamRome.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamRome.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamRome.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                                teamRome.setHasTech(con.iFeudalism, True, iCiv, False, False)
                                teamRome.setHasTech(con.iGuilds, True, iCiv, False, False)
                                teamRome.setHasTech(con.iAlphabet, True, iCiv, False, False)
                                teamRome.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamRome.setHasTech(con.iCalendar, True, iCiv, False, False)
                                teamRome.setHasTech(con.iConstruction, True, iCiv, False, False)
                                teamRome.setHasTech(con.iEngineering, True, iCiv, False, False)
                                teamRome.setHasTech(con.iCurrency, True, iCiv, False, False)
                                teamRome.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamRome.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamRome.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamRome.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
                                teamRome.setHasTech(con.iAesthetics, True, iCiv, False, False)
                                teamRome.setHasTech(con.iLiterature, True, iCiv, False, False)
                                teamRome.setHasTech(con.iCompass, True, iCiv, False, False)
                                teamRome.setHasTech(con.iCivilService, True, iCiv, False, False)
                        if iCiv == iPersia:
                                teamPersia.setHasTech(con.iMysticism, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iMeditation, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iPolytheism, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iPriesthood, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iMonotheism, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iMonarchy, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iLiterature, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iCodeOfLaws, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iFeudalism, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iTheology, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iMusic, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iCivilService, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iGuilds, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iDivineRight, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iFishing, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iTheWheel, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iAgriculture, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iPottery, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iAesthetics, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iSailing, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iWriting, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iMathematics, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iAlphabet, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iCalendar, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iCurrency, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iPhilosophy, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iPaper, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iHunting, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iMining, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iArchery, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iMasonry, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iAnimalHusbandry, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iBronzeWorking, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iHorsebackRiding, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iIronWorking, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iMetalCasting, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iCompass, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iConstruction, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iMachinery, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iEngineering, True, iCiv, False, False)
                                teamPersia.setHasTech(con.iGunpowder, True, iCiv, False, False)
			if iCiv == iIndia:
				lIndianTechs = [con.iMysticism, con.iMeditation, con.iPolytheism, con.iPriesthood, con.iMonotheism, con.iMonarchy, con.iLiterature, \
						con.iCodeOfLaws, con.iFeudalism, con.iTheology, con.iMusic, con.iCivilService, con.iGuilds, con.iDivineRight, con.iFishing, \
						con.iTheWheel, con.iAgriculture, con.iPottery, con.iAesthetics, con.iSailing, con.iWriting, con.iMathematics, con.iAlphabet, \
						con.iCalendar, con.iCurrency, con.iPhilosophy, con.iPaper, con.iHunting, con.iMining, con.iArchery, con.iMasonry, con.iAnimalHusbandry, \
						con.iBronzeWorking, con.iHorsebackRiding, con.iIronWorking, con.iIronWorking, con.iMetalCasting, con.iCompass, con.iConstruction, \
						con.iMachinery, con.iEngineering, con.iOptics, con.iGunpowder, con.iAstronomy, con.iPrintingPress, con.iMilitaryTradition]
				for iTech in lIndianTechs:
					teamIndia.setHasTech(iTech, True, iCiv, False, False)
			if iCiv == iAztecs:
				lMexicanTechs = [con.iMysticism, con.iMeditation, con.iPolytheism, con.iPriesthood, con.iMonotheism, con.iMonarchy, con.iLiterature, con.iCodeOfLaws, con.iDrama, con.iFeudalism, \
						con.iTheology, con.iMusic, con.iCivilService, con.iGuilds, con.iDivineRight, con.iMilitaryTradition, con.iConstitution, con.iLiberalism, \
						con.iFishing, con.iTheWheel, con.iAgriculture, con.iPottery, con.iPrintingPress, con.iEconomics, con.iAstronomy, con.iScientificMethod, con.iChemistry, \
						con.iAesthetics, con.iSailing, con.iWriting, con.iMathematics, con.iAlphabet, con.iCalendar, con.iCurrency, con.iPhilosophy, con.iPaper, con.iBanking, con.iEducation, \
						con.iHunting, con.iMining, con.iArchery, con.iMasonry, con.iAnimalHusbandry, con.iBronzeWorking, con.iHorsebackRiding, con.iIronWorking, con.iMetalCasting, \
						con.iCompass, con.iConstruction, con.iMachinery, con.iEngineering, con.iOptics, con.iGunpowder, con.iReplaceableParts, con.iMilitaryScience, con.iRifling, con.iPatronage]
				for iTech in lMexicanTechs:
					teamAztecs.setHasTech(iTech, True, iCiv, False, False)
			if iCiv == iMaya:
				lColombianTechs = [con.iMysticism, con.iMeditation, con.iPolytheism, con.iPriesthood, con.iMonotheism, con.iMonarchy, con.iLiterature, con.iCodeOfLaws, con.iDrama, con.iFeudalism, \
						con.iTheology, con.iMusic, con.iCivilService, con.iGuilds, con.iDivineRight, con.iMilitaryTradition, con.iConstitution, con.iLiberalism, \
						con.iFishing, con.iTheWheel, con.iAgriculture, con.iPottery, con.iPrintingPress, con.iEconomics, con.iAstronomy, con.iScientificMethod, con.iChemistry, \
						con.iAesthetics, con.iSailing, con.iWriting, con.iMathematics, con.iAlphabet, con.iCalendar, con.iCurrency, con.iPhilosophy, con.iPaper, con.iBanking, con.iEducation, \
						con.iHunting, con.iMining, con.iArchery, con.iMasonry, con.iAnimalHusbandry, con.iBronzeWorking, con.iHorsebackRiding, con.iIronWorking, con.iMetalCasting, \
						con.iCompass, con.iConstruction, con.iMachinery, con.iEngineering, con.iOptics, con.iGunpowder, con.iReplaceableParts, con.iMilitaryScience, con.iRifling, con.iPatronage, 
						con.iNationalism, con.iSteamPower, con.iDemocracy]
				for iTech in lColombianTechs:
					teamMaya.setHasTech(iTech, True, iCiv, False, False)

                sta.onCivSpawn(iCiv)

	def arabianSpawn(self):
        	plotBaghdad = gc.getMap().plot(77,40)
                plotCairo = gc.getMap().plot(69,35)
                Baghdad = plotBaghdad.getPlotCity()
                Cairo = plotCairo.getPlotCity()

                bBaghdad = (plotBaghdad.getOwner() == iArabia)
                bCairo = (plotCairo.getOwner() == iArabia)

                if (bBaghdad and bCairo):
                	iRand = gc.getGame().getSorenRandNum(2, "Toss Coin")

                        if iRand == 0:
				if utils.getHumanID() != iArabia:
					Baghdad.setHasRealBuilding(con.iPalace, True)
					utils.makeUnit(con.iArabiaCamelarcher, iArabia, (77,40), 3)
					utils.makeUnit(con.iSwordsman, iArabia, (77,40), 2)
				utils.makeUnit(con.iArabiaCamelarcher, iArabia, (77,40), 2)
				utils.makeUnit(con.iSwordsman, iArabia, (77,40), 2)
                        else:
				if utils.getHumanID() != iArabia:
					Baghdad.setHasRealBuilding(con.iPalace, True)
					utils.makeUnit(con.iArabiaCamelarcher, iArabia, (69,35), 3)
					utils.makeUnit(con.iSwordsman, iArabia, (69,35), 2)
				utils.makeUnit(con.iArabiaCamelarcher, iArabia, (69,35), 2)
				utils.makeUnit(con.iSwordsman, iArabia, (69,35), 2)

			utils.makeUnit(con.iSettler, iArabia, (77,40), 1)
			utils.makeUnit(con.iSettler, iArabia, (69,35), 1)
			utils.makeUnit(con.iWorker, iArabia, (77,40), 1)
			utils.makeUnit(con.iWorker, iArabia, (69,35), 1)

		elif (bBaghdad and not bCairo):
			if utils.getHumanID() != iArabia:
				Baghdad.setHasRealBuilding(con.iPalace, True)
				utils.makeUnit(con.iArabiaCamelarcher, iArabia, (77,40), 3)
				utils.makeUnit(con.iSwordsman, iArabia, (77,40), 2)
			utils.makeUnit(con.iSettler, iArabia, (77,40), 1)
			utils.makeUnit(con.iArabiaCamelarcher, iArabia, (77,40), 2)
			utils.makeUnit(con.iSwordsman, iArabia, (77,40), 2)#

			utils.makeUnit(con.iSettler, iArabia, (77,40), 1)
			utils.makeUnit(con.iWorker, iArabia, (77,40), 1)
			utils.makeUnit(con.iWorker, iArabia, (75,33), 1)

		elif (not bBaghdad and bCairo):
			if utils.getHumanID() != iArabia:
				utils.makeUnit(con.iArabiaCamelarcher, iArabia, (69,35), 3)
				utils.makeUnit(con.iSwordsman, iArabia, (69,35), 2)
			utils.makeUnit(con.iSettler, iArabia, (69,35), 1)
			utils.makeUnit(con.iArabiaCamelarcher, iArabia, (69,35), 2)
			utils.makeUnit(con.iSwordsman, iArabia, (69,35), 2)

			utils.makeUnit(con.iSettler, iArabia, (69,35), 1)
			utils.makeUnit(con.iWorker, iArabia, (75,33), 1)
			utils.makeUnit(con.iWorker, iArabia, (69,35), 1)

		else:
			utils.makeUnit(con.iSettler, iArabia, (75,33), 2)
			utils.makeUnit(con.iWorker, iArabia, (75,33), 2)
			if utils.getHumanID() != iArabia:
				utils.makeUnit(con.iArabiaCamelarcher, iArabia, (75,33), 3)
				utils.makeUnit(con.iSwordsman, iArabia, (75,33), 2)
			utils.makeUnit(con.iArabiaCamelarcher, iArabia, (75,33), 2)
			utils.makeUnit(con.iSwordsman, iArabia, (75,33), 2)

		if utils.getHumanID() != iArabia and bBaghdad:
			utils.makeUnit(con.iSpearman, iArabia, (77, 40), 2)
			
	def germanSpawn(self):
		if sd.getStabilityLevel(iHolyRome) < con.iStabilityShaky: sd.setStabilityLevel(iHolyRome, con.iStabilityShaky)
			
		pHolyRome.setReborn()
		
		dc.setCivShortDesc(iHolyRome, "TXT_KEY_CIV_AUSTRIA_SHORT_DESC")
		dc.setCivAdjective(iHolyRome, "TXT_KEY_CIV_AUSTRIA_ADJECTIVE")
		
	def holyRomanSpawn(self):
		plot = gc.getMap().plot(60, 56)
		if plot.isCity(): plot.getPlotCity().setCulture(iVikings, 5, True)
		#for x in range(con.tCoreAreasTL[0][iHolyRome][0], con.tCoreAreasBR[0][iHolyRome][0]+1):
		#	for y in range(con.tCoreAreasTL[0][iHolyRome][1], con.tCoreAreasBR[0][iHolyRome][1]+2):
		#		gc.getMap().plot(x,y).setCulture(iVikings, 0, True)
		#utils.debugTextPopup('holy roman spawn')
		
		
				
	def determineEnabledPlayers(self):
	
		iHuman = utils.getHumanID()
		
		if iHuman != iIndia and iHuman != iIndonesia:
			iRand = gc.getDefineINT("PLAYER_OCCURENCE_TAMILS")
			
			if iRand <= 0:
				self.setPlayerEnabled(iTamils, False)
			elif gc.getGame().getSorenRandNum(iRand, 'Tamils enabled?') != 0:
				self.setPlayerEnabled(iTamils, False)
				
		if iHuman != iChina and iHuman != iIndia and iHuman != iMughals:
			iRand = gc.getDefineINT("PLAYER_OCCURENCE_TIBET")
			
			if iRand <= 0:
				self.setPlayerEnabled(iTibet, False)
			elif gc.getGame().getSorenRandNum(iRand, 'Tibet enabled?') != 0:
				self.setPlayerEnabled(iTibet, False)
				
		if iHuman != iSpain and iHuman != iMali:
			iRand = gc.getDefineINT("PLAYER_OCCURENCE_MOORS")
			
			if iRand <= 0:
				self.setPlayerEnabled(iMoors, False)
			elif gc.getGame().getSorenRandNum(iRand, 'Moors enabled?') != 0:
				self.setPlayerEnabled(iMoors, False)
				
		if iHuman != iHolyRome and iHuman != iGermany and iHuman != iRussia:
			iRand = gc.getDefineINT("PLAYER_OCCURENCE_POLAND")
			
			if iRand <= 0:
				self.setPlayerEnabled(iPoland, False)
			elif gc.getGame().getSorenRandNum(iRand, 'Poland enabled?') != 0:
				self.setPlayerEnabled(iPoland, False)
				
		if iHuman != iMali and iHuman != iPortugal:
			iRand = gc.getDefineINT("PLAYER_OCCURENCE_CONGO")
			
			if iRand <= 0:
				self.setPlayerEnabled(iCongo, False)
			elif gc.getGame().getSorenRandNum(iRand, 'Congo enabled?') != 0:
				self.setPlayerEnabled(iCongo, False)
				
		if iHuman != iSpain:
			iRand = gc.getDefineINT("PLAYER_OCCURENCE_ARGENTINA")
			
			if iRand <= 0:
				self.setPlayerEnabled(iArgentina, False)
			elif gc.getGame().getSorenRandNum(iRand, 'Argentina enabled?') != 0:
				self.setPlayerEnabled(iArgentina, False)
				
		if iHuman != iPortugal:
			iRand = gc.getDefineINT("PLAYER_OCCURENCE_BRAZIL")
			
			if iRand <= 0:
				self.setPlayerEnabled(iBrazil, False)
			elif gc.getGame().getSorenRandNum(iRand, 'Brazil enabled?') != 0:
				self.setPlayerEnabled(iBrazil, False)
				
	def placeHut(self, tTL, tBR):
		plotList = []
		
		for x in range(tTL[0], tBR[0]+1):
			for y in range(tTL[1], tBR[1]+1):
				plot = gc.getMap().plot(x,y)
				if plot.isFlatlands() or plot.isHills():
					if plot.getFeatureType() != gc.getInfoTypeForString("FEATURE_MUD"):
						plotList.append((x,y))
		
		if not plotList:
			utils.debugTextPopup('List empty.')
			return
		
		tPlot = utils.getRandomEntry(plotList)
		i, j = tPlot
		
		gc.getMap().plot(i, j).setImprovementType(con.iHut)
		
	def setStateReligion(self, iCiv):
		iReborn = utils.getReborn(iCiv)
		lCities = utils.getAreaCities(con.tCoreAreasTL[iReborn][iCiv], con.tCoreAreasBR[iReborn][iCiv], con.tExceptions[iReborn][iCiv])
		lReligions = [0 for i in range(con.iNumReligions)]
		
		for city in lCities:
			for iReligion in range(con.iNumReligions):
				if city.isHasReligion(iReligion): lReligions[iReligion] += 1
				
		iHighestEntry = utils.getHighestEntry(lReligions)
		
		if iHighestEntry > 0:
			gc.getPlayer(iCiv).setLastStateReligion(lReligions.index(iHighestEntry))