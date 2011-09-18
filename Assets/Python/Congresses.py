# Rhye's and Fall of Civilization - World Congresses

from CvPythonExtensions import *
import CvUtil
import PyHelpers 
import Popup
#import cPickle as pickle
import RFCUtils
import Consts as con
from StoredData import sd # edead

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()

### Constants ###


iPosThreshold = 5
iNegThreshold = -5
iWarThreshold = 16
iNormalizationThreshold = 20



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
iMughals = con.iMughals
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


lCivGroups = con.lCivGroups
lNeighbours = con.lNeighbours

      
  
class Congresses:


        #host city
        sHostCity = ""


##################################################
### Secure storage & retrieval of script data ###
################################################

        def getCongressEnabled( self ):
                return sd.scriptDict['bCongressEnabled']

        def setCongressEnabled( self, bNewValue ):
                sd.scriptDict['bCongressEnabled'] = bNewValue

        def getCivsWithNationalism( self ):
                return sd.scriptDict['iCivsWithNationalism']

        def setCivsWithNationalism( self, iNewValue ):
                sd.scriptDict['iCivsWithNationalism'] = iNewValue

        def getUNbuilt( self ):
                return sd.scriptDict['bUNbuilt']

        def setUNbuilt( self, bNewValue ):
                sd.scriptDict['bUNbuilt'] = bNewValue

        def getInvitedNations( self, iCiv ):
                return sd.scriptDict['lInvitedNations'][iCiv]

        def setInvitedNations( self, iCiv, bNewValue ):
                sd.scriptDict['lInvitedNations'][iCiv] = bNewValue

        def getVotes( self, iCiv ):
                return sd.scriptDict['lVotes'][iCiv]

        def setVotes( self, iCiv, iNewValue ):
                sd.scriptDict['lVotes'][iCiv] = iNewValue

        def getTempActiveCiv( self, iLoop ):
                return sd.scriptDict['lTempActiveCiv'][iLoop]

        def setTempActiveCiv( self, iLoop, iNewValue ):
                sd.scriptDict['lTempActiveCiv'][iLoop] = iNewValue

        def getTempReqCity( self, iLoop ):
                return sd.scriptDict['lTempReqCity'][iLoop]

        def setTempReqCity( self, iLoop, tNewValue ):
                sd.scriptDict['lTempReqCity'][iLoop] = tNewValue

        def getLoopIndex( self ):
                return sd.scriptDict['iLoopIndex']

        def setLoopIndex( self, iNewValue ):
                sd.scriptDict['iLoopIndex'] = iNewValue

        def getTempReqCityHuman( self, iLoop ):
                return sd.scriptDict['lTempReqCityHuman'][iLoop]

        def setTempReqCityHuman( self, iLoop, tNewValue ):
                sd.scriptDict['lTempReqCityHuman'][iLoop] = tNewValue

        def getTempReqCityNI( self ):
                return sd.scriptDict['tempReqCityNI']

        def setTempReqCityNI( self, tNewValue ):
                sd.scriptDict['tempReqCityNI'] = tNewValue

        def getTempActiveCivNI( self ):
                return sd.scriptDict['tempActiveCivNI']

        def setTempActiveCivNI( self, iNewValue ):
                sd.scriptDict['tempActiveCivNI'] = iNewValue

        def getTempAttackingCivsNI( self, iCiv ):
                return sd.scriptDict['lTempAttackingCivsNI'][iCiv]

        def setTempAttackingCivsNI( self, iCiv, bNewValue ):
                sd.scriptDict['lTempAttackingCivsNI'][iCiv] = bNewValue

        def getNumNationsTemp( self ):
                return sd.scriptDict['iNumNationsTemp']

        def setNumNationsTemp( self, iNewValue ):
                sd.scriptDict['iNumNationsTemp'] = iNewValue

        def getBribe( self, iCiv ):
                return sd.scriptDict['lBribe'][iCiv]

        def setBribe( self, iCiv, iNewValue ):
                sd.scriptDict['lBribe'][iCiv] = iNewValue

        def getCivsToBribe( self, iCiv ):
                return sd.scriptDict['lCivsToBribe'][iCiv]

        def setCivsToBribe( self, iCiv, iNewValue ):
                sd.scriptDict['lCivsToBribe'][iCiv] = iNewValue

        def getMemory( self, iCiv ):
                return sd.scriptDict['lMemory'][iCiv]

        def setMemory( self, iCiv, iNewValue ):
                sd.scriptDict['lMemory'][iCiv] = iNewValue

        #from RiseAndFall.py
        def getTempFlippingCityCongress( self ):
                return sd.scriptDict['tempFlippingCityCongress']

        def setTempFlippingCityCongress( self, tNewValue ):
                sd.scriptDict['tempFlippingCityCongress'] = tNewValue


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
   
        def votePopup(self, iActiveCiv, reqCity, iActiveCivLoopIndex):
                self.showPopup(7616, \
                            CyTranslator().getText("TXT_KEY_CONGRESS_OF", ()) + " " + self.sHostCity, \
                            CyTranslator().getText("TXT_KEY_CONGRESS_REQUEST", \
                                (gc.getPlayer(iActiveCiv).getName(), reqCity.getName(), gc.getPlayer(reqCity.getOwner()).getCivilizationAdjective(0))), \
                            (CyTranslator().getText("TXT_KEY_POPUP_VOTE_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_ABSTAIN", ()), CyTranslator().getText("TXT_KEY_POPUP_VOTE_NO", ())))

                print ("iActiveCivLoopIndex", iActiveCivLoopIndex, "X", reqCity.getX(), "Y", reqCity.getY())
                self.setTempReqCity(iActiveCivLoopIndex, (reqCity.getX(), reqCity.getY()))                
                self.setTempActiveCiv(iActiveCivLoopIndex, iActiveCiv) #not self.getLoopIndex() because it should write all the values while precomputing, while waiting for the event for moving the index for reading

        def eventApply7616(self, popupReturn):
                iHuman = utils.getHumanID()
                tReqCity = self.getTempReqCity(self.getLoopIndex())
                print ("self.getLoopIndex() - votePopup", self.getLoopIndex())
                print ("tReqCity", tReqCity)
                tempReqCity = gc.getMap().plot( tReqCity[0], tReqCity[1] ).getPlotCity()
                tempActiveCiv = self.getTempActiveCiv(self.getLoopIndex())
                tempOwnerCiv = tempReqCity.getOwner()
                if( popupReturn.getButtonClicked() == 0 ): # 1st button
                        self.setVotes(iHuman, 10)
                        self.setMemory(tempActiveCiv, self.getMemory(tempActiveCiv)/2 +100)
                        self.setMemory(tempOwnerCiv, self.getMemory(tempOwnerCiv)/2 -100)
                elif( popupReturn.getButtonClicked() == 1 ): # 2nd button
                        self.setVotes(iHuman, 0)
                        self.setMemory(tempActiveCiv, self.getMemory(tempActiveCiv)*2/3)
                        self.setMemory(tempOwnerCiv, self.getMemory(tempOwnerCiv)*2/3)
                elif( popupReturn.getButtonClicked() == 2 ): # 3rd button
                        self.setVotes(iHuman, -10)
                        self.setMemory(tempActiveCiv, self.getMemory(tempActiveCiv)/2 -100)
                        self.setMemory(tempOwnerCiv, self.getMemory(tempOwnerCiv)/2 +100)
                self.voteAI(tempActiveCiv, tempReqCity)                
                self.finalCount(tempActiveCiv, tempReqCity, True)
                self.setLoopIndex( self.getLoopIndex() + 1 )



        def askNothingPopup(self, iActiveCiv, iActiveCivLoopIndex):
                print ("iActiveCivLoopIndex", iActiveCivLoopIndex, "no city")
                if (iActiveCiv == utils.getHumanID()):
                        tempStr = CyTranslator().getText("TXT_KEY_CONGRESS_NO_CITY", ())
                else:
                        tempStr = gc.getPlayer(iActiveCiv).getName() + " " + CyTranslator().getText("TXT_KEY_CONGRESS_NO_AI_REQUEST", ())
                tempOKStr = " " #CyTranslator().getText("TXT_KEY_CONGRESS_OK", ())
                self.showPopup(7623, \
                            CyTranslator().getText("TXT_KEY_CONGRESS_OF", ()) + " " + self.sHostCity, \
                            tempStr, \
                            tempOKStr)

        def eventApply7623(self, popupReturn):                
                print ("self.getLoopIndex() - askNothingPopup", self.getLoopIndex())
                self.setLoopIndex( self.getLoopIndex() + 1 )

                


        def askCityPopup(self, iActiveCiv, cityList): #, iActiveCivLoopIndex):
                cityListNames = []
                print cityList
                cityListNames.append(CyTranslator().getText("TXT_KEY_CONGRESS_NO_REQUEST", ()))
                for i in range(len(cityList)):
                        cityListNames.append(cityList[i].getName() + " (" + gc.getPlayer(cityList[i].getOwner()).getCivilizationAdjective(0) + ")" )
                        self.setTempReqCityHuman(i, (cityList[i].getX(), cityList[i].getY())) 
                print cityListNames
                self.showPopup(7617, CyTranslator().getText("TXT_KEY_CONGRESS_OF", ()) + " " + self.sHostCity, CyTranslator().getText("TXT_KEY_CONGRESS_HUMAN_REQUEST", ()), cityListNames)
                #self.setTempActiveCiv(iActiveCivLoopIndex, iActiveCiv) #using iHuman instead
                #print ("iActiveCiv", iActiveCiv, "iActiveCivLoopIndex", iActiveCivLoopIndex, "self.getTempActiveCiv(self.getLoopIndex())", self.getTempActiveCiv(self.getLoopIndex()))
                              

        def eventApply7617(self, popupReturn):
                iHuman = utils.getHumanID()
                self.setVotes(iHuman, 30)
                if (popupReturn.getButtonClicked() > 0): #!= NO_REQUEST
                        tReqCity = self.getTempReqCityHuman( popupReturn.getButtonClicked() - 1 ) #-1 because 0 is NO_REQUEST
                        print tReqCity
                        tempReqCity = gc.getMap().plot( tReqCity[0], tReqCity[1] ).getPlotCity()
                        #self.voteAI(self.getTempActiveCiv(self.getLoopIndex()), tempReqCity)
                        #self.finalCount(self.getTempActiveCiv(self.getLoopIndex()), tempReqCity, True)
                        self.voteAI(iHuman, tempReqCity)
                        self.finalCount(iHuman, tempReqCity, True)
                print ("self.getLoopIndex() - askCityPopup", self.getLoopIndex())
                self.setLoopIndex( self.getLoopIndex() + 1 )



                
        def decisionPopup(self, bHumanInvited):
                if (bHumanInvited):
                        tReqCity = self.getTempReqCity(self.getLoopIndex())
                        tempReqCity = gc.getMap().plot( tReqCity[0], tReqCity[1] ).getPlotCity()
                        tempActiveCiv = self.getTempActiveCiv(self.getLoopIndex())
                else:
                        tempReqCity = gc.getMap().plot( self.getTempReqCityNI()[0], self.getTempReqCityNI()[1] ).getPlotCity()
                        tempActiveCiv = self.getTempActiveCivNI()
                self.showPopup(7618, \
                            (CyTranslator().getText("TXT_KEY_CONGRESS_OF", ()) + " " + self.sHostCity), \
                            (CyTranslator().getText("TXT_KEY_CONGRESS_REQUEST1", ()) + " " + tempReqCity.getName() + " " + \
                               CyTranslator().getText("TXT_KEY_CONGRESS_REQUEST2", ()) + " " + gc.getPlayer(tempActiveCiv).getCivilizationAdjective(0) \
                                   + " " + CyTranslator().getText("TXT_KEY_CONGRESS_REQUEST3", ())), \
                            (CyTranslator().getText("TXT_KEY_CONGRESS_ACCEPT_DECISION", ()), CyTranslator().getText("TXT_KEY_CONGRESS_REFUSE_DECISION", ()) ))

        def eventApply7618(self, popupReturn):
                if( popupReturn.getButtonClicked() == 0 ): # 1st button
                        if (self.getInvitedNations(utils.getHumanID()) == True):
                                self.acceptDecision(self.getTempActiveCiv(self.getLoopIndex() - 1), self.getTempReqCity(self.getLoopIndex() - 1), True) #, True)   #-1 because there's already +1 in eventApply7616
                        else:
                                self.acceptDecision(self.getTempActiveCivNI(), self.getTempReqCityNI(), True) #, False)                        
                elif( popupReturn.getButtonClicked() == 1 ): # 2nd button
                        if (self.getInvitedNations(utils.getHumanID()) == True):
                                self.refuseDecision(self.getTempActiveCiv(self.getLoopIndex() - 1), True)
                        else:
                                self.refuseDecision(self.getTempActiveCivNI(), False)

        def invitationPopup(self):
                self.showPopup(7619, \
                             CyTranslator().getText("TXT_KEY_CONGRESS_NEW", ()), \
                             CyTranslator().getText("TXT_KEY_CONGRESS_INVITATION", ()), \
                            (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_NO", ()) ))

        def eventApply7619(self, popupReturn):
                if( popupReturn.getButtonClicked() == 0 ): # 1st button
                        self.setInvitedNations(utils.getHumanID(), True)
                elif( popupReturn.getButtonClicked() == 1 ): # 2nd button
                        self.setInvitedNations(utils.getHumanID(), False)

        def bribePopup(self):
                iHuman = utils.getHumanID()
                civNamesList = []
                civNamesList.append(CyTranslator().getText("TXT_KEY_POPUP_NO", ()))
                iCounter = 0
                for iCiv in range( iNumPlayers ):
                        if ((self.getInvitedNations(iCiv) == True) and iCiv != iHuman):
                                if (gc.getPlayer(iHuman).canContact(iCiv)):
                                        civNamesList.append(gc.getPlayer(iCiv).getCivilizationShortDescription(0) + " (" + gc.getAttitudeInfo(gc.getPlayer(iCiv).AI_getAttitude(iHuman)).getDescription() + ")")
                                        self.setCivsToBribe(iCounter, iCiv)
                                        iCounter += 1                
                #print civNamesList
                self.showPopup(7620, CyTranslator().getText("TXT_KEY_CONGRESS_NEW", ()), CyTranslator().getText("TXT_KEY_CONGRESS_CORRUPTION_REQUEST", ()), civNamesList)
                              

        def eventApply7620(self, popupReturn):
                iHuman = utils.getHumanID()                
                pHuman = gc.getPlayer(iHuman)
                
                #debug
##                for iCiv in range( iNumPlayers ):
##                        pCiv = gc.getPlayer(iCiv)
##                        print ("iCiv", iCiv)
##                        if (iCiv != iHuman and pCiv.isAlive()):
##                                iTempThreshold = 200
##                                iGoldRequired = (2*pHuman.getGold() + 2*pCiv.getGold())/4 - 70
##                                print ("iGoldRequired", iGoldRequired)
##                                if (gc.getPlayer(iCiv).AI_isFinancialTrouble()):
##                                        iGoldRequired *= 3
##                                        iGoldRequired /= 5
##                                if (iGoldRequired < 50):
##                                        iGoldRequired = 50
##                                print ("financial trouble", iGoldRequired)
##                                iSoggezione = gc.getGame().getPlayerRank(iCiv) - gc.getGame().getPlayerRank(iHuman)
##                                iSoggezioneModifier = min(100, abs(iSoggezione)*(100/((iNumPlayers/2)+5))) + 100
##                                print ("iSoggezione", iSoggezione, "iSoggezioneModifier", iSoggezioneModifier)
##                                if (iSoggezione > 0):
##                                        iTempThreshold = iGoldRequired*100/iSoggezioneModifier
##                                if (iSoggezione < 0):
##                                        iTempThreshold = iGoldRequired*iSoggezioneModifier/100
##                                print ("iTempThreshold_soggezione", iTempThreshold)
##                                iAttitude = pCiv.AI_getAttitude(iHuman)-2
##                                iAttitudeModifier = (100 - abs(iAttitude)*25)
##                                if (iAttitude > 0):
##                                        iTempThreshold = iTempThreshold*iAttitudeModifier/100
##                                if (iAttitude < 0):
##                                        iTempThreshold = iTempThreshold*(100+iAttitudeModifier)/100
##                                print ("iAttitudeModifier", iAttitudeModifier, "iTempThreshold_attitude", iTempThreshold)
##                                if (gc.getTeam(pCiv.getTeam()).isAtWar(iHuman)):
##                                        iTempThreshold *=2
##                                print ("iTempThreshold_war_final", iTempThreshold)
##                for i in range( iNumPlayers ):
##                        print self.getCivsToBribe(i)

                if (popupReturn.getButtonClicked() > 0): #!= NO_REQUEST
                        iCiv = self.getCivsToBribe(popupReturn.getButtonClicked() - 1)
                        self.setBribe(0, utils.getHumanID()) #master
                        self.setBribe(1, iCiv) #serf
                        self.setBribe(2, iCiv) #enemy
                        self.goldPopup()
                                

        def goldPopup(self):
                self.showPopup(7621, CyTranslator().getText("TXT_KEY_CONGRESS_NEW", ()), CyTranslator().getText("TXT_KEY_CONGRESS_CORRUPTION_GOLD", ()), ("10%", "20%", "50%"))

        def eventApply7621(self, popupReturn):
                iHuman = utils.getHumanID()                

                if (popupReturn.getButtonClicked() == 0):
                        iGoldOffered = gc.getPlayer(iHuman).getGold()*10/100
                elif (popupReturn.getButtonClicked() == 1):
                        iGoldOffered = gc.getPlayer(iHuman).getGold()*20/100
                elif (popupReturn.getButtonClicked() == 2):
                        iGoldOffered = gc.getPlayer(iHuman).getGold()*50/100
                       
                iCiv = self.getBribe(1)
                pCiv = gc.getPlayer(iCiv)
                iHuman = utils.getHumanID()
                pHuman = gc.getPlayer(iHuman)
                
                iTempThreshold = 200
                iGoldRequired = (2*pHuman.getGold() + 2*pCiv.getGold())/4 - 70
                if (gc.getPlayer(iCiv).AI_isFinancialTrouble()):
                        iGoldRequired *= 3
                        iGoldRequired /= 5
                if (iGoldRequired < 50):
                        iGoldRequired = 50
                iSoggezione = gc.getGame().getPlayerRank(iCiv) - gc.getGame().getPlayerRank(iHuman)
                iSoggezioneModifier = min(100, abs(iSoggezione)*(100/((iNumPlayers/2)+5))) + 100
                if (iSoggezione > 0):
                        iTempThreshold = iGoldRequired*100/iSoggezioneModifier
                if (iSoggezione < 0):
                        iTempThreshold = iGoldRequired*iSoggezioneModifier/100
                iAttitude = pCiv.AI_getAttitude(iHuman)-2
                iAttitudeModifier = (100 - abs(iAttitude)*25)
                if (iAttitude > 0):
                        iTempThreshold = iTempThreshold*iAttitudeModifier/100
                if (iAttitude < 0):
                        iTempThreshold = iTempThreshold*(100+iAttitudeModifier)/100
                if (gc.getTeam(pCiv.getTeam()).isAtWar(iHuman)):
                        iTempThreshold *=2

                if (iTempThreshold <= iGoldOffered):
                        popup = Popup.PyPopup()       
                        popup.setBodyString( CyTranslator().getText("TXT_KEY_CONGRESS_CORRUPTION_YES", ()))
                        popup.launch()
                        self.setBribe(1, iCiv) #serf
                        self.setBribe(2, -1) #enemy
                        pHuman.changeGold(-iGoldOffered)
                        pCiv.changeGold(iGoldOffered)
                elif (iAttitudeModifier <= 1 or gc.getTeam(pCiv.getTeam()).isAtWar(iHuman) or iGoldOffered < 60):
                        popup = Popup.PyPopup()       
                        popup.setBodyString( CyTranslator().getText("TXT_KEY_CONGRESS_CORRUPTION_ENEMY", ()))
                        popup.launch()  
                        self.setBribe(1, -1) #serf
                        self.setBribe(2, iCiv) #enemy
                else:
                        popup = Popup.PyPopup()       
                        popup.setBodyString( CyTranslator().getText("TXT_KEY_CONGRESS_CORRUPTION_NO", ()))
                        popup.launch()




#######################################
### Main methods (Event-Triggered) ###
#####################################  

                
        def checkTurn(self, iGameTurn):

                if (self.getCongressEnabled() == True):
                        if (iGameTurn % utils.getTurns(25) == 2): # edead: RFCM
                                iNumNationsTemp = self.preInvitations()
                                self.setNumNationsTemp(iNumNationsTemp)
                        if (iGameTurn % utils.getTurns(25) == 3): # edead: RFCM
                                self.bribingTurn(self.getNumNationsTemp())                    
                        if (iGameTurn % utils.getTurns(25) == 4): # edead: RFCM
                                self.startCongress(self.getNumNationsTemp())
##                        pass

##                #debug
##                self.setCongressEnabled(True)
##                if (iGameTurn % 3 == 0): 
##                        iNumNationsTemp = self.preInvitations()
##                        self.setNumNationsTemp(iNumNationsTemp)
##                if (iGameTurn % 3 == 1):                                
##                        self.bribingTurn(self.getNumNationsTemp())
##                if (iGameTurn % 3 == 2):
##                        self.startCongress(self.getNumNationsTemp())

        def onTechAcquired(self, iTech, iPlayer):
                if (self.getCongressEnabled() == True or self.getUNbuilt() == True):
                        return
                if (self.getCivsWithNationalism() >= 1 and gc.getGame().getGameTurn() >= getTurnForYear(con.tBirth[utils.getHumanID()])): # edead: RFCM
                        print ("Congress enabled")
                        self.setCongressEnabled(True)
                        return
                if (iTech == con.iNationalism):
                        self.setCivsWithNationalism(self.getCivsWithNationalism() + 1)

        def onBuildingBuilt(self, iPlayer, iBuilding, city):
                if (self.getCongressEnabled() == True):
                        if (iBuilding == con.iUnitedNations):
                                print ("Congress disabled")
                                self.setCongressEnabled(False)
                                self.setUNbuilt(True)


        def preInvitations(self):
                self.resetData()
                iNumNationsTemp = self.inviteGuests()
                if (self.getInvitedNations(utils.getHumanID()) == True):
                        self.invitationPopup()
                return iNumNationsTemp


        def bribingTurn(self, iNumNationsTemp):
                iHuman = utils.getHumanID()
                if (iNumNationsTemp > 3):
                        if (self.getInvitedNations(iHuman) == True):
                                self.bribePopup()

            
        def startCongress(self, iNumNationsTemp):
                if (iNumNationsTemp > 3):
                        iNumNations = self.checkInvitations()
                        self.tradeCities(iNumNations)
                      

        def resetData(self):
                #invitations
                for iCiv in range( iNumPlayers ):
                        self.setInvitedNations(iCiv, False)
                #bribe settings
                self.setBribe(0, -1) #master
                self.setBribe(1, -1) #serf
                self.setBribe(2, -1) #enemy
                ##list of civs to bribe
                for iCiv in range( iNumPlayers ):
                        self.setCivsToBribe(iCiv, -1)


        def selectRandomCityCiv(self, iCiv):
                cityList = []
                for pyCity in PyPlayer(iCiv).getCityList():
                        cityList.append(pyCity.GetCy())
                iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
                return cityList[iCity]
            


        def inviteGuests(self):
                iCount = 0
                iCountNotInvited = 0
                for iCiv in range( iNumPlayers ):
                        if (gc.getPlayer(iCiv).isAlive()):
                                if (gc.getGame().getPlayerRank(iCiv) == 0):
                                        iLeader = iCiv
                                        self.setInvitedNations(iLeader, True)
                                        iCount += 1
                                        break
                print ("iLeader", iLeader)
                
                for iRank in range( 1, iNumPlayers ):
                        for iCiv in range( iNumPlayers ):
                                if (gc.getGame().getPlayerRank(iCiv) == iRank):
                                        if (gc.getPlayer(iCiv).isAlive()):
                                                if (gc.getPlayer(iCiv).canContact(iLeader)):
                                                        if (iCount < 9):
                                                                self.setInvitedNations(iCiv, True)
                                                                print ("inviting", iCiv)
                                                                iCount += 1
                                                        else:
                                                                iCountNotInvited += 1
                                        
                #invite someone different X2
                for k in range (2):
                        if (iCountNotInvited > 1):
                                iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'civ in')
                                print ("scan order", iRndnum)
                                for i in range( iRndnum, iNumPlayers + iRndnum ):
                                        if (iRndnum % 2 == 0): #randomize scan order
                                                j = i
                                        else:
                                                j = iNumPlayers + 2*iRndnum - i
                                        iCiv = j % iNumPlayers
                                        if (gc.getPlayer(iCiv).isAlive()):
                                                if (gc.getPlayer(iCiv).canContact(iLeader)):
                                                        if (self.getInvitedNations(iCiv) == False):
                                                                self.setInvitedNations(iCiv, True)
                                                                print ("Adding ", iCiv)
                                                                break
                                iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'civ out')
                                print ("scan order", iRndnum)
                                for i in range( iRndnum, iNumPlayers + iRndnum ):
                                        if (iRndnum % 2 == 0): #randomize scan order
                                                j = i
                                        else:
                                                j = iNumPlayers + 2*iRndnum - i
                                        iCiv = j % iNumPlayers
                                        if (self.getInvitedNations(iCiv) == True):
                                                if (gc.getGame().getPlayerRank(iCiv) > 3):
                                                        self.setInvitedNations(iCiv, False)
                                                        print ("Removing ", iCiv)
                                                        break

                #debug - always invited
##                iHuman = utils.getHumanID()
##                if (self.getInvitedNations(iHuman) == False and gc.getPlayer(iHuman).isAlive()):                                                        
##                        self.setInvitedNations(utils.getHumanID(), True)
##                        iCount += 1
                #debug - never invited                  
##                iHuman = utils.getHumanID()
##                if (self.getInvitedNations(iHuman) == True and gc.getPlayer(iHuman).isAlive()):                                                        
##                        self.setInvitedNations(utils.getHumanID(), False)
##                        iCount -= 1


                return iCount


        def checkInvitations(self):
                #check dead civs
                for iCiv in range( iNumPlayers ):
                        if (not gc.getPlayer(iCiv).isAlive()):
                                self.setInvitedNations(iCiv, False)

                #recount
                iCount = 0
                for iCiv in range( iNumPlayers ):
                        if (self.getInvitedNations(iCiv) == True):
                                iCount += 1
                                
                #host nation
                iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'host civ')
                for i in range( iRndnum, iNumPlayers + iRndnum ):
                        iCiv = i % iNumPlayers
                        if (self.getInvitedNations(iCiv) == True):
                                iHost = iCiv
                                break     
                #host city
                hostCity = self.selectRandomCityCiv(iHost)
                self.sHostCity = hostCity.getName()

                #debug
                print ("invited 2: ")
                for iCiv in range( iNumPlayers ):
                        if (self.getInvitedNations(iCiv)):                                
                                print (gc.getPlayer(iCiv).getCivilizationShortDescription(0), gc.getGame().getPlayerRank(iCiv) )

                return iCount
                                



        def tradeCities(self, iNumNations):
                self.setLoopIndex(0)
                self.setTempReqCityNI(-1)
                self.setTempActiveCivNI(-1)
                for i in range( iNumPlayers ):              
                        self.setTempAttackingCivsNI(i, False)
                
                iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'a random civ starts')
                #iActiveCivLoopIndex = iNumNations-1 ##reversed because popups overlap; -=1 is right down here
                iActiveCivLoopIndex = iNumNations ##reversed because popups overlap; -=1 is right down here

                for i in range( iRndnum, iNumPlayers + iRndnum ):
                        iActiveCiv = i % iNumPlayers
                        if (self.getInvitedNations(iActiveCiv)):
                                print ("iActiveCivLoopIndexNotYetUpdated", iActiveCivLoopIndex, "iActiveCiv", iActiveCiv)
                                for iLoopCiv in range( iNumPlayers ):
                                        self.setVotes(iLoopCiv, 0)  #reset votes array
                                if (iActiveCiv != utils.getHumanID()):
                                        iActiveCivLoopIndex -= 1
                                        self.tradeCitiesAI(iActiveCiv, iActiveCivLoopIndex)
                                else:
                                        iActiveCivLoopIndex -= 1
                                        self.tradeCitiesHuman(iActiveCiv, iActiveCivLoopIndex)
                #for j in range( iNumNations ):
                #        print ("self.getTempReqCity(iNumNations) dopo", j, self.getTempReqCity(j))
                                
                print ("sHostCity", self.sHostCity)
                if (self.getInvitedNations(utils.getHumanID()) == True):
                        popup = Popup.PyPopup()
                        popup.setHeaderString(CyTranslator().getText("TXT_KEY_CONGRESS_OF", ()) + " " + self.sHostCity)          
                        popup.setBodyString( CyTranslator().getText("TXT_KEY_CONGRESS_INTRO", ()))
                        popup.launch()

                print ("self.getTempReqCityNI()", self.getTempReqCityNI())
                if (self.getTempReqCityNI() != -1):
                        self.decisionPopup(False)
                        
                if (self.getInvitedNations(utils.getHumanID()) == False):
                        popup = Popup.PyPopup()
                        popup.setHeaderString(CyTranslator().getText("TXT_KEY_CONGRESS_OF", ()) + " " + self.sHostCity)          
                        popup.setBodyString( CyTranslator().getText("TXT_KEY_CONGRESS_INTRO_NOT_INVITED", ()))
                        popup.launch()


        def tradeCitiesAI(self, iActiveCiv, iActiveCivLoopIndex):
                cityList = self.selectCities(iActiveCiv)
                print ("iActiveCiv", iActiveCiv, "len(cityList)", len(cityList))
                if (len(cityList)):
                        reqCity = cityList[gc.getGame().getSorenRandNum(len(cityList), 'random choice')]
                        
                        #if (reqCity.isCapital()):
                        #        reqCity = cityList[gc.getGame().getSorenRandNum(len(cityList), 'random choice')] #retry once (less likely to happen)
                        #if (reqCity.isCapital()):
                        #        reqCity = cityList[gc.getGame().getSorenRandNum(len(cityList), 'random choice')] #retry twice (less likely to happen)
                        if (gc.getPlayer(reqCity.getOwner()).getSettlersMaps( 67-reqCity.getY(), reqCity.getX() ) >= 500 and reqCity.getCulture(reqCity.getOwner()) >= 2000):
                                reqCity = cityList[gc.getGame().getSorenRandNum(len(cityList), 'random choice')] #retry once (less likely to happen)


                        if (reqCity):
                                if (self.getInvitedNations(utils.getHumanID()) == True):
                                        self.votePopup(iActiveCiv, reqCity, iActiveCivLoopIndex) 
                                else:
                                        self.congressAIOnly(iActiveCiv, reqCity, iActiveCivLoopIndex)
                else:
                        if (self.getInvitedNations(utils.getHumanID()) == True):
                                self.askNothingPopup(iActiveCiv, iActiveCivLoopIndex) 



        def congressAIOnly(self, iActiveCiv, reqCity, iActiveCivLoopIndex):
                #if (reqCity.getOwner() == utils.getHumanID()):
                self.voteAI(iActiveCiv, reqCity)
                self.finalCount(iActiveCiv, reqCity, False)




        def tradeCitiesHuman(self, iActiveCiv, iActiveCivLoopIndex):
                cityList = self.selectCities(iActiveCiv)
                print ("iActiveCiv", iActiveCiv, "len(cityList)", len(cityList))
                if (not len(cityList)):
                        self.askNothingPopup(iActiveCiv, iActiveCivLoopIndex) 
                        #popup = Popup.PyPopup() 
                        #popup.setBodyString( CyTranslator().getText("TXT_KEY_CONGRESS_NO_CITY", ()))
                        #popup.launch()
                        
                        #self.setLoopIndex( self.getLoopIndex() + 1 ) #0 because setTempCity is skipped
                elif (len(cityList)):
                        #erase duplicates
                        for i in range(len(cityList)):
                                for j in range(len(cityList)):
                                        if (i != j and cityList[i] == cityList[j]):
                                                cityList[j] = -1
                        iLength = len(cityList) #static length, not affected by pop()
                        for i in range(iLength):
                                j = iLength -1 -i
                                print ("j,", j, "cityList[j]", cityList[j])
                                if (cityList[j] == -1):
                                        cityList.pop(j)
                        
                        ##reduce to 5
                        while (len(cityList) > 5):
                                iPop = gc.getGame().getSorenRandNum(len(cityList), 'random city')
                                cityList.pop(iPop)
                        print ("pop done", len(cityList))
                        self.askCityPopup(iActiveCiv, cityList) #, iActiveCivLoopIndex)


        def selectCities(self, iActiveCiv):
                cityList = []
                for iLoopCiv in range( iNumTotalPlayers+1 ):
                        if (gc.getPlayer(iLoopCiv).isAlive() and iLoopCiv != iActiveCiv):
                                for pyCity in PyPlayer(iLoopCiv).getCityList():
                                        if (pyCity.GetCy()):
                                                city = pyCity.GetCy()
                                                cityPlot = gc.getMap().plot(city.getX(), city.getY())
                                                if (cityPlot.isCity()): #sometimes cities have been razed
                                                        #condition 1
                                                        if (cityPlot.isRevealed(iActiveCiv, False) and not city.isCapital()):
                                                                #condition 2: don't ask human player cities if it's weak                                  
                                                                if (not (city.getOwner() == utils.getHumanID() and gc.getActivePlayer().getNumCities() <=3)):
                                                                        #condition 3: don't ask cities to close friends (or isHuman, since we can't know human attitude)   
                                                                        if ((not (gc.getPlayer(iActiveCiv).AI_getAttitude(city.getOwner()) >= 3)) or gc.getPlayer(iActiveCiv).isHuman()):
                                                                                #condition 4: don't ask cities to civs just born   
                                                                                if (not (gc.getGame().getGameTurn() <= getTurnForYear(con.tBirth[city.getOwner()]) + utils.getTurns(20))): # edead: RFCM
                                                                                        #condition 5: don't ask to the civ that has bribed you
                                                                                        if (not (self.getBribe(0) == city.getOwner() and iActiveCiv == self.getBribe(1))):

                                                                                                #condition: don't ask cities to master or vassal
                                                                                                if (not (gc.getTeam(gc.getPlayer(city.getOwner()).getTeam()).isVassal(iActiveCiv)) and not (gc.getTeam(gc.getPlayer(iActiveCiv).getTeam()).isVassal(city.getOwner()))):

                                                                                                        #condition: Ethiopian UP
                                                                                                        if (iLoopCiv != con.iEthiopia):

                                                                                                                #condition 6a: city culture
                                                                                                                if (city.getCulture(iActiveCiv) > 0):
                                                                                                                        if (city.getOwner() != iAmerica):
                                                                                                                                if (city not in cityList):
                                                                                                                                        cityList.append(city)
                                                                                                                                        continue
                                                                                                                #condition 6b: plot culture
                                                                                                                if (cityPlot.getCulture(iActiveCiv) > 0):
                                                                                                                        if (city.getOwner() != iAmerica):
                                                                                                                                if (city not in cityList):
                                                                                                                                        cityList.append(city)
                                                                                                                                        continue
                                                                                                                #condition 7: ever owned
                                                                                                                if city.isEverOwned(iActiveCiv):
                                                                                                                        if (city not in cityList):
                                                                                                                                cityList.append(city)
                                                                                                                                continue
                                                                                                                #condition 8: core land
                                                                                                                if (gc.getPlayer(iActiveCiv).getSettlersMaps( 67-city.getY(), city.getX() ) >= 500):
                                                                                                                        if (city not in cityList):
                                                                                                                                cityList.append(city)
                                                                                                                                continue
                                                                                                                #condition 9: colonies
                                                                                                                if (iActiveCiv in lCivGroups[0]):
                                                                                                                        if (city.getOwner() >= iNumPlayers or (city.getOwner() < iNumPlayers and not gc.getPlayer(city.getOwner()).isHuman() and utils.getStability(city.getOwner()) < 0)):
                                                                                                                                if (city.getX()<=42 or (city.getX()>=86 and city.getY()<=52) or city.getY()<=39): #America, Asia, Africa
                                                                                                                                        if (len(cityList) <= 7):
                                                                                                                                                if (gc.getPlayer(iActiveCiv).getSettlersMaps( 67-city.getY(), city.getX() ) >= 60):                                                                                                        
                                                                                                                                                        if (city not in cityList):
                                                                                                                                                                cityList.append(city)
                                                                                                                                                                continue
                                                                                                                                        elif (len(cityList) <= 14):
                                                                                                                                                if (gc.getPlayer(iActiveCiv).getSettlersMaps( 67-city.getY(), city.getX() ) >= 150):                                                                                                 
                                                                                                                                                        if (city not in cityList):
                                                                                                                                                                cityList.append(city)
                                                                                                                                                                continue
                                                                                                                                        else:
                                                                                                                                                if (gc.getPlayer(iActiveCiv).getSettlersMaps( 67-city.getY(), city.getX() ) == 400):
                                                                                                                                                        if (city not in cityList):
                                                                                                                                                                cityList.append(city)
                                                                                                                                                                continue
                                                                                                                #condition 10: unstable empires near
                                                                                                                if (city.getOwner() < iNumMajorPlayers):
                                                                                                                        if (gc.getGame().getPlayerRank(city.getOwner()) > gc.getGame().countCivPlayersAlive()/2 and gc.getGame().getPlayerRank(iActiveCiv) < gc.getGame().countCivPlayersAlive()/2):
                                                                                                                                if (utils.getStability(city.getOwner()) <= -35):
                                                                                                                                        if (gc.getPlayer(iActiveCiv).getNumCities() > 0): #this check is needed, otherwise game crashes
                                                                                                                                                if (utils.calculateDistance(cityPlot.getX(), cityPlot.getY(), gc.getPlayer(iActiveCiv).getCapitalCity().getX(), gc.getPlayer(iActiveCiv).getCapitalCity().getY()) <= 15 or (gc.getPlayer(iActiveCiv).getSettlersMaps( 67-city.getY(), city.getX() ) >= 40)):
                                                                                                                                                        if (city not in cityList):
                                                                                                                                                                cityList.append(city)
                                                                                                                                                                continue
                                                                                                                #condition 11: borders
                                                                                                                for x in range(city.getX()-3, city.getX()+4):
                                                                                                                        for y in range(city.getY()-3, city.getY()+4):
                                                                                                                                pCurrent = gc.getMap().plot( x, y )
                                                                                                                                if ( pCurrent.getOwner() == iActiveCiv ):
                                                                                                                                        if (city not in cityList):
                                                                                                                                                cityList.append(city)
                                                                                                                                                break
                                                                                                                                                break
                #debug
                #print ("cityList", iActiveCiv)
                #for iC in cityList:
                #    print iC.getName()
                return cityList
                                                                

        def voteAI(self, iActiveCiv, reqCity):
                print ("iActiveCiv", iActiveCiv)
                for iCiv in range( iNumPlayers ):
                        if (self.getInvitedNations(iCiv) == True) and (iCiv != utils.getHumanID()):
                                iResult = 0
                                iOwner = reqCity.getOwner()                                
                                #factor 1a - score
                                if (iOwner != iBarbarian and iOwner != iIndependent and iOwner != iIndependent2):
                                        iResult += (gc.getGame().getPlayerRank(iActiveCiv) - gc.getGame().getPlayerRank(iOwner))
                                if (iOwner == iBarbarian or iOwner == iIndependent or iOwner == iIndependent2):
                                        iResult += (gc.getGame().getPlayerRank(iActiveCiv) - iNumPlayers/2)
                                #factor 1b - leader
                                if (gc.getGame().getPlayerRank(iActiveCiv) == 0 and gc.getGame().getPlayerRank(iCiv) <= 4):
                                        iResult -= 4
                                if (gc.getGame().getPlayerRank(iOwner) == 0 and gc.getGame().getPlayerRank(iCiv) <= 4):
                                        iResult += 3
                                #factor 1c - num cities
                                if (iOwner != iBarbarian and iOwner != iIndependent and iOwner != iIndependent2):
                                        iResult += 2*(gc.getPlayer(iOwner).getNumCities() - gc.getPlayer(iActiveCiv).getNumCities())
                                if (iOwner == iBarbarian or iOwner == iIndependent or iOwner == iIndependent2):
                                        iResult += 2*(gc.getGame().countCivTeamsAlive()/2 - gc.getPlayer(iActiveCiv).getNumCities())
                                #factor 2a - friendship
                                pCiv = gc.getPlayer(iCiv)
                                tCiv = gc.getTeam(pCiv.getTeam())
                                attitude1 = pCiv.AI_getAttitude(iActiveCiv) - 2
                                attitude2 = 0
                                if (iOwner != iBarbarian):
                                        attitude2 = pCiv.AI_getAttitude(iOwner) - 2
                                #if (not gc.getPlayer(iCiv).canContact(iActiveCiv)):
                                #        print ("No contact active civ", pCiv.AI_getAttitude(iActiveCiv))
                                #if (not gc.getPlayer(iCiv).canContact(iOwner)):
                                #        print ("No contact owner civ", pCiv.AI_getAttitude(iOwner))
                                iResult += 8*(attitude1-attitude2)
                                if tCiv.isDefensivePact(iActiveCiv):
                                        iResult += 2
                                if tCiv.isDefensivePact(iOwner):
                                        iResult -= 2
                                #factor 2b - at war                                
                                if (tCiv.isAtWar(iActiveCiv)):
                                        iResult -= 7
                                if (iOwner != iBarbarian):
                                        if (tCiv.isAtWar(iOwner)):
                                                iResult += 7
                                #factor 3a - ever owned
                                if (reqCity.isEverOwned(iActiveCiv)):
                                        iResult += 9
                                #factor 3b - culture
                                if (reqCity.getCulture(iActiveCiv) > 0):
                                        iResult += 8
                                if (reqCity.getCulture(iActiveCiv) <= 0):
                                        iResult -= 5
                                #factor 4a - city radius owner
                                iCountPlots = 0
                                for x in range(reqCity.getX()-2, reqCity.getX()+3):
                                        for y in range(reqCity.getY()-2, reqCity.getY()+3):
                                                pCurrent = gc.getMap().plot( x, y )
                                                if ( pCurrent.getOwner() == iActiveCiv ):
                                                        iCountPlots += 1
                                iResult += iCountPlots
                                #factor 4b - city radius culture
                                iCountCulture = 0
                                for x in range(reqCity.getX()-2, reqCity.getX()+3):
                                        for y in range(reqCity.getY()-2, reqCity.getY()+3):
                                                pCurrent = gc.getMap().plot( x, y )
                                                if ( pCurrent.getCulture(iActiveCiv) > 0 ):
                                                        iCountCulture += 1
                                if (iCountCulture == 0):
                                        iResult -= 5
                                #factor 5 - capital
                                if (reqCity.isCapital()):
                                        iResult -= 25
                                        #if (gc.getPlayer(iOwner).getNumCities() <= 2):
                                        #        iResult += 3    #a good chance to kill a civ
                                        #else:
                                        #        iResult -= 25    #but usually a capital shouldn't flip
                                #factor 6 - neighbour
                                if (iActiveCiv in lNeighbours[iCiv]):
                                        iResult -= 5
                                if (iOwner in lNeighbours[iCiv]):
                                        iResult += 5
                                #factor 7a - euro civs leave colonization go on if not interested in the area
                                if (iCiv in lCivGroups[0]):
                                        if (iActiveCiv in lCivGroups[0] and iOwner not in lCivGroups[0]):
                                                if (gc.getPlayer(iCiv).getSettlersMaps( 67-reqCity.getY(), reqCity.getX() ) < 60):
                                                        iResult += 8
                                #factor 7b - help forming settlers maps
                                if (iActiveCiv in lCivGroups[0] and iOwner not in lCivGroups[0]):
                                        if (gc.getPlayer(iActiveCiv).getSettlersMaps( 67-reqCity.getY(), reqCity.getX() ) >= 200):
                                                iResult += 6
                                if (iActiveCiv not in lCivGroups[0] and iOwner in lCivGroups[0]):
                                        if (gc.getPlayer(iOwner).getSettlersMaps( 67-reqCity.getY(), reqCity.getX() ) >= 200):
                                                iResult -= 4 
                                #factor 8 - distant lands
                                for i in range(6):
                                        if ((iActiveCiv in lCivGroups[i]) and (iOwner in lCivGroups[i]) and (iCiv not in lCivGroups[i])):
                                                if (iActiveCiv not in lCivGroups[0]): #Euros
                                                        iResult /= 2
                                                else:
                                                        iResult *= 2
                                                        iResult /= 3                                                    
                                #factor 9 - core land
                                if (gc.getPlayer(iActiveCiv).getSettlersMaps( 67-reqCity.getY(), reqCity.getX() ) >= 500):
                                        iResult += 9
                                if (gc.getPlayer(iOwner).getSettlersMaps( 67-reqCity.getY(), reqCity.getX() ) >= 500):
                                        iResult -= 13
                                #factor 10 - human player
                                if (iActiveCiv == utils.getHumanID()):
                                        iResult += 2
                                if (iOwner == utils.getHumanID()):
                                        iResult -= 3
                                #factor 11 - memory
                                iMemoryModifier = self.getMemory(iCiv)/15
                                if (self.getMemory(iCiv) > 225):
                                        iMemoryModifier = 15
                                if (self.getMemory(iCiv) < -225):
                                        iMemoryModifier = -15  
                                    
                                if (iActiveCiv == utils.getHumanID()):
                                        iResult += iMemoryModifier
                                if (iOwner == utils.getHumanID()):
                                        iResult -= iMemoryModifier
                                #factor 12 - wonders
                                if (reqCity.getNumWorldWonders() > 0):
                                        iResult -= 2*reqCity.getNumWorldWonders()                                
                                #factor 13 - French UP
                                if (iCiv in lCivGroups[0]):
                                        if (iActiveCiv == iFrance):
                                                iResult += 6
                                        if (iOwner == iFrance):
                                                iResult -= 9

                                #factor - master and vassal                                                
                                if gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iActiveCiv):
                                        iResult += 25
                                if gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iOwner):
                                        iResult -= 25
                                if gc.getTeam(gc.getPlayer(iActiveCiv).getTeam()).isVassal(iCiv):
                                        iResult += 10
                                if gc.getTeam(gc.getPlayer(iOwner).getTeam()).isVassal(iCiv):
                                        iResult -= 10                                                
                                #factor 14 - generic modifier
                                        iResult += 3 
                                #factor 15a - owner
                                if (iOwner == iCiv):
                                        iResult = -30
                                #factor 15b - active civ
                                if (iActiveCiv == iCiv):
                                        iResult = 30

                                self.setVotes(iCiv, iResult)       

                                print (gc.getPlayer(iActiveCiv).getCivilizationShortDescription(0), reqCity.getName(), reqCity.getX(), reqCity.getY(), gc.getPlayer(iOwner).getCivilizationShortDescription(0), gc.getPlayer(iCiv).getCivilizationShortDescription(0), iResult)          


            
        def finalCount(self, iActiveCiv, reqCity, bShowResults):
                iHuman = utils.getHumanID()
                if (reqCity):   #just in case, as it might have been destroyed during AI turn
                        iOwner = reqCity.getOwner()
                        iTempPosThreshold = iPosThreshold
                        iTempNegThreshold = iNegThreshold
                        
                        #normalization
                        iTotal = 0
                        iCount = 0
                        iMax = 0
                        for iCiv in range( iNumPlayers ):
                                if (self.getInvitedNations(iCiv) == True):
                                        if (iCiv != iActiveCiv and iCiv != reqCity.getOwner() and iCiv != iHuman):
                                                iCount += 1
                                                iTotal += self.getVotes(iCiv)
                                                if (abs(self.getVotes(iCiv)) > iMax):
                                                        iMax = abs(self.getVotes(iCiv))
                        iAverage = iTotal / iCount
                        for iCiv in range( iNumPlayers ):
                                if (self.getInvitedNations(iCiv) == True):
                                        if (iCiv != iActiveCiv and iCiv != reqCity.getOwner() and iCiv != iHuman):
                                                if (iAverage > 0):                                                        
                                                        if (self.getVotes(iCiv) < iAverage):
                                                                self.setVotes(iCiv, self.getVotes(iCiv)-iAverage*2/3)
                                                        if (self.getVotes(iCiv) > 0):
                                                                self.setVotes(iCiv, self.getVotes(iCiv)*iNormalizationThreshold/iMax)
                                                if (iAverage < 0):
                                                        if (self.getVotes(iCiv) > iAverage):
                                                                self.setVotes(iCiv, self.getVotes(iCiv)-iAverage*2/3)
                                                        if (self.getVotes(iCiv) < 0):
                                                                self.setVotes(iCiv, self.getVotes(iCiv)*iNormalizationThreshold/iMax)
                        for iCiv in range( iNumPlayers ):
                                if (self.getInvitedNations(iCiv) == True):
                                        if (iCiv != iActiveCiv and iCiv != reqCity.getOwner() and iCiv != iHuman):
                                                if (self.getVotes(iCiv) <= 3 and self.getVotes(iCiv) >= -3):
                                                        self.setVotes(iCiv, self.getVotes(iCiv)*2) #less abstaining
                        #debug
                        #for iCiv in range( iNumPlayers ):
                        #        if (self.getInvitedNations(iCiv) == True):
                        #                 print ("Normalized", gc.getPlayer(iCiv).getCivilizationShortDescription(0), self.getVotes(iCiv))
                        if (iAverage > 0):
                                iTempPosThreshold = iPosThreshold + 1
                                iTempNegThreshold = iNegThreshold + 1
                        if (iAverage < 0):
                                iTempPosThreshold = iPosThreshold - 1
                                iTempNegThreshold = iNegThreshold - 1
                        #end normalization


                        #corruption
                        print ("Bribe vector", self.getBribe(0), self.getBribe(1), self.getBribe(2))
                        if (self.getBribe(1) != -1):
                                iCiv = self.getBribe(1)
                        elif (self.getBribe(2) != -1):
                                iCiv = self.getBribe(2)                               
                        if (self.getBribe(0) != -1):
                                if (iCiv != iActiveCiv and iCiv != iOwner):
                                        if (self.getBribe(1) == iCiv):
                                                self.setVotes(iCiv, self.getVotes(iHuman))
                                        elif (self.getBribe(2) == iCiv):
                                                if (self.getVotes(iHuman) > iTempPosThreshold or self.getVotes(iHuman) < iTempNegThreshold):
                                                        self.setVotes(iCiv, -self.getVotes(iHuman))

                        #show results
                        sResults = ""
                        for iCiv in range( iNumPlayers ):
                                if (self.getInvitedNations(iCiv) == True):
                                        sResults += gc.getPlayer(iCiv).getName()
                                        if (self.getVotes(iCiv) > iTempPosThreshold):
                                                sResults += (" " + CyTranslator().getText("TXT_KEY_CONGRESS_POPUP_VOTES_YES", ()))  
                                        elif (self.getVotes(iCiv) < iTempNegThreshold):
                                                sResults += (" " + CyTranslator().getText("TXT_KEY_CONGRESS_POPUP_VOTES_NO", ()))                            
                                        else:
                                                sResults += (" " + CyTranslator().getText("TXT_KEY_CONGRESS_POPUP_ABSTAINS", ()))

                                                
                        iYes = 0
                        iNo = 0
                        for iCiv in range( iNumPlayers ):
                                if (self.getVotes(iCiv) > iTempPosThreshold):
                                        iYes += 1
                                if (self.getVotes(iCiv) < iTempNegThreshold):    
                                        iNo += 1
                        if (iYes > iNo):
                                sResults += CyTranslator().getText("TXT_KEY_CONGRESS_POPUP_YES_WINS", ())
                        else:
                                sResults += CyTranslator().getText("TXT_KEY_CONGRESS_POPUP_NO_WINS", ())
                        if (bShowResults == True):
                                popup = Popup.PyPopup()
                                sTempString = CyTranslator().getText("TXT_KEY_CONGRESS_REQUEST", (gc.getPlayer(iActiveCiv).getName(), reqCity.getName(), gc.getPlayer(reqCity.getOwner()).getCivilizationAdjective(0)))
                                popup.setHeaderString( sTempString )
                                popup.setBodyString( sResults )
                                popup.launch()

                        print (reqCity.getName(), "flipping to ", iActiveCiv, iYes, iNo)
                        
                        if (iYes > iNo):
                                if (iOwner == iHuman and self.getInvitedNations(iOwner) == False):
                                        self.setTempReqCityNI((reqCity.getX(), reqCity.getY()))
                                        self.setTempActiveCivNI(iActiveCiv)
                                        for iCiv in range( iNumPlayers ):
                                                if (self.getInvitedNations(iCiv) == True):
                                                        if (self.getVotes(iCiv) > iWarThreshold):
                                                                self.setTempAttackingCivsNI(iCiv, True)
                                elif (iOwner == iHuman and self.getInvitedNations(iOwner) == True):
                                        self.decisionPopup(True)                                    
                                else:                                    
                                        self.acceptDecision(iActiveCiv, reqCity, False) #, True)
                                        if (self.getInvitedNations(iHuman) == False):
                                                CyInterface().addMessage(iHuman, True, con.iDuration/2, (reqCity.getName() + " " + \
                                                                                   CyTranslator().getText("TXT_KEY_CONGRESS_NOTIFY_YES", (gc.getPlayer(iActiveCiv).getCivilizationAdjectiveKey(),))), \
                                                                                   "", 0, "", ColorTypes(con.iCyan), -1, -1, True, True)
 
                                    

        def acceptDecision(self, iActiveCiv, reqCity, bDecisionPopup): #, bHumanInvited):
                if (bDecisionPopup):
                        tReqCity = reqCity
                        reqCity = gc.getMap().plot( tReqCity[0], tReqCity[1] ).getPlotCity()
##                if (bDecisionPopup and bHumanInvited):
##                        tReqCity = self.getTempReqCity(self.getLoopIndex())
##                        reqCity = gc.getMap().plot( tReqCity[0], tReqCity[1] ).getPlotCity()
##                        iActiveCiv = self.getTempActiveCiv(self.getLoopIndex())
##                elif (not bHumanInvited):
##                        tReqCity = self.getTempReqCityNI()
##                        reqCity = gc.getMap().plot( tReqCity[0], tReqCity[1] ).getPlotCity()
##                        iActiveCiv = self.getTempActiveCivNI()
                iOwner = reqCity.getOwner()
                print ("Accepting decision:", reqCity.getName(), "iActiveCiv:", iActiveCiv)
                utils.cultureManager((reqCity.getX(),reqCity.getY()), 80, iActiveCiv, iOwner, False, False, True)
                utils.pushOutGarrisons((reqCity.getX(),reqCity.getY()), iOwner)
                utils.relocateSeaGarrisons((reqCity.getX(),reqCity.getY()), iOwner)                
                self.setTempFlippingCityCongress((reqCity.getX(),reqCity.getY()))
                utils.flipCity((reqCity.getX(),reqCity.getY()), 0, 0, iActiveCiv, [iOwner])
                utils.createGarrisons(self.getTempFlippingCityCongress(), iActiveCiv, 2)
                

                              
        def refuseDecision(self, iActiveCiv, bHumanInvited):
                iWWmodifier = 0
                iHuman = utils.getHumanID()
                tHuman = gc.getTeam(gc.getPlayer(iHuman).getTeam())
                for iLoopCiv in range( iNumPlayers ):
                        if tHuman.isDefensivePact(iLoopCiv):
                                iWWmodifier += 8
                                if (iWWmodifier >= 24):
                                        break                
                for iCiv in range( iNumPlayers ):
                        iRndnum = gc.getGame().getSorenRandNum(100, 'rnd')
                        iPatienceThreshold = con.tPatienceThreshold[iActiveCiv] + iWWmodifier
                        if (utils.isAVassal(iActiveCiv)):
                                iPatienceThreshold += 50
                                if (iPatienceThreshold == 100):
                                        iPatienceThreshold = 90
                        if (iRndnum >= iPatienceThreshold):
                                if (bHumanInvited):
                                        if (self.getInvitedNations(iCiv) == True):
                                                if (self.getVotes(iCiv) > iWarThreshold):
                                                        gc.getTeam(gc.getPlayer(iCiv).getTeam()).declareWar(iHuman, False, -1)
                                else:
                                        if (self.getTempAttackingCivsNI(iCiv) == True):
                                                print ("TempAttackingCivsNI: ", iCiv)
                                                gc.getTeam(gc.getPlayer(iCiv).getTeam()).declareWar(iHuman, False, -1)

            


    
