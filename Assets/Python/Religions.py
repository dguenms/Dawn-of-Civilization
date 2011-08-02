# Rhye's and Fall of Civilization - Religions management

from CvPythonExtensions import *
import CvUtil
import PyHelpers       
import Popup
#import cPickle as pickle     	
import Consts as con
import CvTranslator
import RFCUtils
from StoredData import sd #edead

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()

### Constants ###

iArabia = con.iArabia
iNumPlayers = con.iNumPlayers
iNumTotalPlayers = con.iNumTotalPlayers
iBarbarian = con.iBarbarian
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iCeltia = con.iCeltia

# obsolete - edead
# i2250BC = con.i2250BC
# i2085BC = con.i2085BC
# i1800BC = con.i1800BC
# i600BC = con.i600BC
# i483BC = con.i483BC
# i479BC = con.i479BC
# i33AD = con.i33AD
# i622AD = con.i622AD



# initialise religion variables to religion indices from XML
iJudaism = con.iJudaism 
iChristianity = con.iChristianity
iIslam = con.iIslam
iHinduism = con.iHinduism
iBuddhism = con.iBuddhism
iConfucianism = con.iConfucianism
iTaoism = con.iTaoism
iZoroastrianism = con.iZoroastrianism

iMissionary_Jewish = con.iJewishMissionary
iMissionary_Christian = con.iChristianMissionary
iMissionary_Islamic = con.iIslamicMissionary
iMissionary_Hindu = con.iHinduMissionary
iMissionary_Buddhist = con.iBuddhistMissionary
iMissionary_Confucian = con.iConfucianMissionary
iMissionary_Taoist = con.iTaoistMissionary
iMissionary_Zoroastrian = con.iZoroastrianMissionary


# initialise coordinates

tJerusalem = (73, 38)
tJewishTL = (68, 34)
tJewishBR = (80, 42)
tVaranasiTL = (91, 37)
tVaranasiBR = (94, 40)
tBodhgayaTL = (92, 38)
tBodhgayaBR = (95, 40)
tBuddhistTL = (87, 33)
tBuddhistBR = (102, 44)
tHenanTL = (101, 43)
tHenanBR = (104, 46)
tSEAsiaTL = (97, 31)
tSEAsiaBR = (107, 46)
tAsiaTL = (83, 28)
tAsiaBR = (1, 66)
tEuropeTL = (48, 33)
tEuropeBR = (72, 65)
tQufuTL = (102, 44)
tQufuBR = (106, 46)
tMecca = (75, 33)

lReformationMatrix = [80, 50, 50, 50, 80, 50, 50, 95, 50, 80, 50, 50, 10, 80, 80, 50, 95, 75, 30, 25, 80, 10, 50, 95, 50, 50, 50, 80, 50, 50, 50, 50, 80, 50]


class Religions:

##################################################
### Secure storage & retrieval of script data ###
################################################

        def getSeed( self ):
                return sd.scriptDict['iSeed']

        def setSeed( self ):
                sd.scriptDict['iSeed'] = gc.getGame().getSorenRandNum(100, 'Seed for random delay')


#######################################
### Main methods (Event-Triggered) ###
#####################################  

        def setup(self):
                self.setSeed()
                

       	
        def checkTurn(self, iGameTurn):

                if (not gc.getGame().isReligionFounded(iChristianity)):
                        iEthiopianModifier = 0
                        if (gc.getPlayer(con.iEthiopia).isHuman()):
                                iEthiopianModifier = 15 #for the UHV
                        if (iGameTurn == getTurnForYear(33) + utils.getTurns(8*self.getSeed()/100 + iEthiopianModifier)): #Christianity up to 190AD (15 = 330AD)
                                pJerusalem = gc.getMap().plot(tJerusalem[0], tJerusalem[1])                
                                if (not pJerusalem.getPlotCity().isNone()):  
                                        if (pJerusalem.getPlotCity().getOwner() == iIndependent or pJerusalem.getPlotCity().getOwner() == iIndependent2 or pJerusalem.getPlotCity().getOwner() == iBarbarian):
                                                bChristianResult = self.foundReligion(tJerusalem, iChristianity)
                                                tCity = tJerusalem
                                        else:
                                                tCity = self.selectRandomCityReligionCiv(iJudaism, iIndependent)
                                                bChristianResult = self.foundReligion(tCity, iChristianity)
                                        if (bChristianResult == False):
                                                tCity = self.selectRandomCityReligionCiv(iJudaism, iIndependent2)
                                                bChristianResult = self.foundReligion(tCity, iChristianity)
                                        if (bChristianResult == False):
                                                tCity = self.selectRandomCityAreaCiv(tJewishTL, tJewishBR, iIndependent)
                                                bChristianResult = self.foundReligion(tCity, iChristianity)
                                        if (bChristianResult == False):
                                                tCity = self.selectRandomCityAreaCiv(tJewishTL, tJewishBR, iIndependent2)
                                                bChristianResult = self.foundReligion(tCity, iChristianity)
                                        if (bChristianResult == False):
                                                tCity = self.selectRandomCityReligionCiv(iJudaism, iCeltia)
                                                bChristianResult = self.foundReligion(tCity, iChristianity)
                                        if (bChristianResult == False):
                                                tCity = self.selectRandomCityAreaCiv(tJewishTL, tJewishBR, iCeltia)
                                                bChristianResult = self.foundReligion(tCity, iChristianity)                                                
                                        if (bChristianResult == False):
                                                tCity = self.selectRandomCityReligionCiv(iJudaism, iBarbarian)
                                                bChristianResult = self.foundReligion(tCity, iChristianity)
                                        if (bChristianResult == False):
                                                tCity = self.selectRandomCityAreaCiv(tJewishTL, tJewishBR, iBarbarian)
                                                bChristianResult = self.foundReligion(tCity, iChristianity)
                                        if (bChristianResult == False):
                                                tCity = self.selectRandomCityAreaCiv(tEuropeTL, tEuropeBR, iIndependent)
                                                bChristianResult = self.foundReligion(tCity, iChristianity)
                                        if (bChristianResult == False):
                                                tCity = self.selectRandomCityAreaCiv(tEuropeTL, tEuropeBR, iIndependent2)
                                                bChristianResult = self.foundReligion(tCity, iChristianity)
                                        if (bChristianResult == False):
                                                tCity = self.selectRandomCityAreaCiv(tEuropeTL, tEuropeBR, iCeltia)
                                                bChristianResult = self.foundReligion(tCity, iChristianity)
                                        if (bChristianResult == False):
                                                tCity = self.selectRandomCityAreaCiv(tEuropeTL, tEuropeBR, iBarbarian)
                                                bChristianResult = self.foundReligion(tCity, iChristianity)
                                        if (bChristianResult == True):
                                                self.spreadReligion(tCity, 3, iMissionary_Christian)   
 
          
                if (iGameTurn == getTurnForYear(622)+1):
                        if (gc.getGame().isReligionFounded(iIslam)):
                                for pyCity in PyPlayer(iArabia).getCityList():
                                        if (pyCity.GetCy().isHolyCityByType(iIslam)):
                                                if (gc.getPlayer(pyCity.GetCy().getOwner()).isHuman() == 0):
                                                        print ("spreading Islam", iMissionary_Islamic)
                                                        #self.spreadReligion( tMecca, 4, iMissionary_Islamic)
                                                        self.spreadReligion( (pyCity.GetCy().getX(), pyCity.GetCy().getY()), 4, iMissionary_Islamic) 

                if (iGameTurn == getTurnForYear(600)):
                        if (not gc.getPlayer(0).isPlayable()): #late start condition
                                pMecca = gc.getMap().plot(tMecca[0], tMecca[1])                
                                if (not pMecca.getPlotCity().isNone()):                            
                                        if (pMecca.getPlotCity().getOwner() == con.iArabia):
                                                self.foundReligion(tMecca, iIslam)


        def foundReligion(self, tPlot, iReligion):
                if (tPlot != False):
                        plot = gc.getMap().plot( tPlot[0], tPlot[1] )                
                        if (not plot.getPlotCity().isNone()):
                                #if (gc.getPlayer(city.getOwner()).isHuman() == 0):
                                #if (not gc.getGame().isReligionFounded(iReligion)):
                                gc.getGame().setHolyCity(iReligion, plot.getPlotCity(), True)
                                return True
                        else:
                                return False
                            
                return False


        def selectRandomCityCiv(self, iCiv):
                if (gc.getPlayer(iCiv).isAlive()):
                        cityList = []
                        for pyCity in PyPlayer(iCiv).getCityList():
                                cityList.append(pyCity.GetCy())
                        iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
                        city = cityList[iCity]
                        return (city.getX(), city.getY())
                return False
            

        def selectRandomCityArea(self, tTopLeft, tBottomRight):
                cityList = []
                for x in range(tTopLeft[0], tBottomRight[0]+1):
                        for y in range(tTopLeft[1], tBottomRight[1]+1):
                                pCurrent = gc.getMap().plot( x, y )
                                if ( pCurrent.isCity()):
                                        cityList.append(pCurrent.getPlotCity())
                if (cityList):
                        iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
                        city = cityList[iCity]
                        return (city.getX(), city.getY())
                else:
                        return False


        def selectRandomCityAreaCiv(self, tTopLeft, tBottomRight, iCiv):
                cityList = []
                for x in range(tTopLeft[0], tBottomRight[0]+1):
                        for y in range(tTopLeft[1], tBottomRight[1]+1):
                                pCurrent = gc.getMap().plot( x, y )
                                if ( pCurrent.isCity()):
                                        if (pCurrent.getPlotCity().getOwner() == iCiv):
                                                cityList.append(pCurrent.getPlotCity())
                if (cityList):
                        iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
                        city = cityList[iCity]
                        return (city.getX(), city.getY())
                else:
                        return False



        def selectRandomCityReligion(self, iReligion):
                if (gc.getGame().isReligionFounded(iReligion)):
                        cityList = []
                        for iPlayer in range(iNumPlayers):
                                for pyCity in PyPlayer(iPlayer).getCityList():
                                        if pyCity.GetCy().isHasReligion(iReligion):
                                                cityList.append(pyCity.GetCy())                                        
                        iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
                        city = cityList[iCity]
                        return (city.getX(), city.getY())
                return False


        def selectRandomCityReligionCiv(self, iReligion, iCiv):
                if (gc.getGame().isReligionFounded(iReligion)):
                        cityList = []
                        for iPlayer in range(iNumPlayers):
                                for pyCity in PyPlayer(iPlayer).getCityList():
                                        if pyCity.GetCy().isHasReligion(iReligion):
                                                if (pyCity.GetCy().getOwner() == iCiv):                            
                                                        cityList.append(pyCity.GetCy())
                        if (cityList):
                                iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
                                city = cityList[iCity]
                                return (city.getX(), city.getY())
                return False


        def spreadReligion(self, tCoords, iNum, iMissionary):
                city = gc.getMap().plot( tCoords[0], tCoords[1] ).getPlotCity()
                #print city
                #print city.getOwner()
                utils.makeUnit(iMissionary, city.getOwner(), tCoords, iNum)
		

##REFORMATION

        def showPopup(self, popupID, title, message, labels):
                popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
                popup.setHeaderString(title)
                popup.setBodyString(message)
                for i in labels:
                    popup.addButton( i )
                popup.launch(False)

        def reformationPopup(self):
                self.showPopup(7624, CyTranslator().getText("TXT_KEY_REFORMATION_TITLE", ()), CyTranslator().getText("TXT_KEY_REFORMATION_MESSAGE",()), (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_NO", ())))

        def eventApply7624(self, popupReturn):
                iHuman = utils.getHumanID()
                if(popupReturn.getButtonClicked() == 0):
                        self.reformationyes(iHuman)
                elif(popupReturn.getButtonClicked() == 1):
                        self.reformationno(iHuman)

        def onTechAcquired(self, iTech, iPlayer):
                if (iTech == con.iPrintingPress):
                        if (gc.getPlayer(iPlayer).getStateReligion() == con.iChristianity):
                                if (not gc.getGame().isReligionFounded(con.iJudaism)):
                                        gc.getGame().setHolyCity(con.iJudaism, gc.getPlayer(iPlayer).getCapitalCity(), True)
                                        gc.getPlayer(iPlayer).getCapitalCity().setNumRealBuilding(con.iJewishShrine,1)
                                        self.reformation()

        def reformation(self):
                for iCiv in range(iNumTotalPlayers):
                        cityList = PyPlayer(iCiv).getCityList()
                        for city in cityList:
                                if(city.hasReligion(1)):
                                        self.reformationchoice(iCiv)
                                        break

        def reformationchoice(self, iCiv):
                if ((gc.getPlayer(iCiv)).isHuman()):
                        self.reformationPopup()
                else:
                        rndnum = gc.getGame().getSorenRandNum(100, 'Reformation')
                        if(rndnum >= lReformationMatrix[iCiv]):
                                self.reformationyes(iCiv)
                        else:
                                self.reformationno(iCiv)

        def reformationyes(self, iCiv):
                cityList = PyPlayer(iCiv).getCityList()
                for city in cityList:
                        if(city.city.isHasReligion(1)):
                                if(city.hasBuilding(con.iChristianTemple)):
                                        city.city.setHasRealBuilding(con.iChristianTemple, False)
                                        city.city.setHasRealBuilding(con.iJewishTemple, True)
                                if(city.hasBuilding(con.iChristianMonastery)):
                                        city.city.setHasRealBuilding(con.iChristianMonastery, False)
                                        city.city.setHasRealBuilding(con.iJewishMonastery, True)
                                if(city.hasBuilding(con.iChristianTemple)):
                                        city.city.setHasRealBuilding(con.iChristianCathedral, False)
                                        city.city.setHasRealBuilding(con.iJewishCathedral, True)
                                if(not city.city.isHolyCityByType(1)):
                                        city.city.setHasReligion(1,False,False,False)
                                if(city.city.getPopulation() > 7):
                                        rndnum = gc.getGame().getSorenRandNum(100, 'ReformationResidual')
                                        if(rndnum <= lReformationMatrix[iCiv]):
                                                city.city.setHasReligion(1, True, False, False)
                                city.city.setHasReligion(0, True, False, False)

                pPlayer = gc.getPlayer(iCiv)
                pPlayer.changeGold(500)
                if (pPlayer.getStateReligion() == 1):
                        pPlayer.setLastStateReligion(0)

        def reformationno(self, iCiv):
                cityList = PyPlayer(iCiv).getCityList()
                for city in cityList:
                        if(city.city.isHasReligion(1)):
                                rndnum = gc.getGame().getSorenRandNum(100, 'ReformationAnyway')
                                if(rndnum >= lReformationMatrix[iCiv]):
                                        city.city.setHasReligion(0, True, False, False)
