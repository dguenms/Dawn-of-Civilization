# Rhye's and Fall of Civilization - Communications

from CvPythonExtensions import *
import CvUtil
import PyHelpers  
import Popup
import Consts as con
import RFCUtils
utils = RFCUtils.RFCUtils()

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

### Constants ###

iNumMajorPlayers = con.iNumMajorPlayers
iNumBuildingsPlague = con.iNumBuildingsPlague
iNumBuildingsEmbassy = con.iNumBuildingsEmbassy

#scrambled pools
tPool1 = (con.iEgypt, -1, -1, -1, -1, -1,
          con.iChina, -1, -1, -1, -1, -1,
          con.iBabylonia, -1, -1, -1, -1, -1,
          con.iGreece, -1, -1, -1, -1, -1,
          con.iIndia, -1, -1, -1, -1, -1)

tPool2 = (con.iEgypt, -1, 
          con.iCarthage, -1,
          con.iChina, -1,
          con.iRome, -1,          
          con.iBabylonia, con.iMaya,
          con.iGreece, -1,          
          con.iIndia, con.iEthiopia,           
          con.iJapan, -1,              
          con.iPersia, -1)


tPool3 = (con.iEgypt,  
          con.iTurkey,
          con.iEngland,
          con.iInca,
          con.iCarthage,
          con.iRussia,
          con.iChina,
          con.iRome,          
          con.iVikings,
          con.iBabylonia,
          con.iAztecs,
          con.iEthiopia,
          con.iNetherlands,
	  con.iItaly,
          con.iMongolia,
          con.iKhmer,
	  con.iIndonesia,
          con.iSpain,
          con.iGreece,
          con.iMali,
          con.iMaya,
          con.iHolyRome,
          con.iIndia,
          con.iAmerica,
          con.iPortugal,          
          con.iJapan,
          con.iPersia,
          con.iFrance,
	  con.iByzantium,
          con.iKorea,
	  con.iMughals,
	  con.iGermany,
	  con.iThailand,
	  con.iTamils,
	  con.iPoland,
	  con.iMoors,
	  con.iCongo,
	  con.iTibet,
	  con.iBrazil)


class Communications:
       	
        def checkTurn(self, iGameTurn):
                #self.decay(con.iIndia) #debug
                #if (iGameTurn >= 25 and iGameTurn <= 95):
                if (iGameTurn >= getTurnForYear(-2250) and iGameTurn <= getTurnForYear(-680)):
                        i = (iGameTurn + utils.getSeed()/10 - 5) % (len(tPool1))
                        iCiv = tPool1[i]
##                        #shuffle                        
##                        if (i % 2 == 0):
##                                iCiv = i/2
##                        else:
##                                iCiv = con.iNumMajorPlayers/2 + i/2  
                        if (iCiv >= 0 and iCiv < con.iNumMajorPlayers):
                                if (gc.getPlayer(iCiv).isAlive() and iGameTurn >= getTurnForYear(con.tBirth[iCiv]+utils.getTurns(15))): # edead: RFCM
                                        if (not gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(con.iElectricity)):
                                                self.decay(iCiv)
                #elif (iGameTurn > 95 and iGameTurn <= 168):
                elif (iGameTurn > getTurnForYear(-680) and iGameTurn <= getTurnForYear(410)): # edead: RFCM
                        i = (iGameTurn + utils.getSeed()/10 - 5) % (len(tPool2))
                        iCiv = tPool2[i]
  
                        if (iCiv >= 0 and iCiv < con.iNumMajorPlayers):
                                if (gc.getPlayer(iCiv).isAlive() and iGameTurn >= getTurnForYear(con.tBirth[iCiv]+utils.getTurns(15))): # edead: RFCM
                                        if (not gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(con.iElectricity)):
                                                self.decay(iCiv)
                else:
                        i = (iGameTurn + utils.getSeed()/10 - 5) % (len(tPool3))
                        j = ((iGameTurn + utils.getSeed()/10 - 5)+13) % (len(tPool3))
                        iCiv1 = tPool3[i]
                        iCiv2 = tPool3[j]            
                        if (iCiv1 >= 0 and iCiv1 < con.iNumMajorPlayers):
                                if (gc.getPlayer(iCiv1).isAlive() and iGameTurn >= getTurnForYear(con.tBirth[iCiv1]+utils.getTurns(15))): # edead: RFCM
                                        if (not gc.getTeam(gc.getPlayer(iCiv1).getTeam()).isHasTech(con.iElectricity)):
                                                self.decay(iCiv1)
                        if (iCiv2 >= 0 and iCiv2 < con.iNumMajorPlayers):
                                if (gc.getPlayer(iCiv2).isAlive() and iGameTurn >= getTurnForYear(con.tBirth[iCiv2]+utils.getTurns(15))): # edead: RFCM
                                        if (not gc.getTeam(gc.getPlayer(iCiv2).getTeam()).isHasTech(con.iElectricity)):
                                                self.decay(iCiv2)

                        

        def decay(self, iCiv):

                teamCiv = gc.getTeam(gc.getPlayer(iCiv).getTeam())
                cutList = []
                iRndnum = gc.getGame().getSorenRandNum(iNumMajorPlayers, 'starting index')
                iCounter = 0

                #initialise list
                #print ("iRndnum", iRndnum)
                for i in range(iRndnum, iNumMajorPlayers + iRndnum):
                        #print ("i", i)
                        if (iRndnum % 2 == 0): #randomize scan order
                                j = i
                                #print ("jA", j)
                        else:
                                j = iNumMajorPlayers + 2*iRndnum - i
                                #print ("jB", j)
                        iOtherCiv = j % iNumMajorPlayers
                        #print ("iOtherCiv", iOtherCiv)
                        if (gc.getPlayer(iOtherCiv).isAlive()):
                                if (teamCiv.canContact(iOtherCiv)):
                                        if (not gc.getTeam(gc.getPlayer(iOtherCiv).getTeam()).isHasTech(con.iElectricity)):
                                                cutList.append(iOtherCiv)
                #print (iCiv, "cutList", cutList)
                #first browse our cities - if other civs can see our borders
                for pyCity in PyPlayer(iCiv).getCityList():
                        city = pyCity.GetCy()
                        for iOtherCiv in cutList:
                                if (city.hasBuilding(iNumBuildingsPlague + iOtherCiv)): #their embassy. + getProduction()?
                                        cutList.remove(iOtherCiv)
                                pCity = gc.getMap().plot( city.getX(), city.getY() )
                                if (pCity.isVisible(iOtherCiv, False)): #in case it has a holy city
                                        if (iOtherCiv in cutList):
                                                cutList.remove(iOtherCiv)                                
                        for x in range(city.getX()-4, city.getX()+5):
                                for y in range(city.getY()-4, city.getY()+5):
                                        pCurrent = gc.getMap().plot( x, y )
                                        if (pCurrent.isVisible(iCiv, False)):
                                                for iOtherCiv2 in cutList:
                                                        if (pCurrent.getOwner() == iOtherCiv2):
                                                                cutList.remove(iOtherCiv2)

                #then browse their cities - if we can see their borders (view distance is asymmetrical)            
                for iOtherCiv in cutList:
                        if (iCounter >= 4): #3 in vanilla and warlords
                                return 
                        bNear = False
                        for pyOtherCity in PyPlayer(iOtherCiv).getCityList():
                                city = pyOtherCity.GetCy()
                                if (city.hasBuilding(iNumBuildingsPlague + iCiv)): #our embassy. + getProduction()?
                                        bNear = True
                                        break
                                pOtherCity = gc.getMap().plot( city.getX(), city.getY() )
                                if (pOtherCity.isVisible(iCiv, False)): #in case I've got a holy city
                                        bNear = True
                                        break
                                for x in range(city.getX()-4, city.getX()+5):
                                        for y in range(city.getY()-4, city.getY()+5):
                                                pCurrent = gc.getMap().plot( x, y )
                                                if (pCurrent.isVisible(iOtherCiv, False)):
                                                        if (pCurrent.getOwner() == iCiv):
                                                                bNear = True
                                                                break
                                                                break
                        if (bNear == False):
                                teamCiv.cutContact(iOtherCiv)
                                iCounter += 1
                                print ("Cutting contacts between", gc.getPlayer(iCiv).getCivilizationShortDescription(0), "and", gc.getPlayer(iOtherCiv).getCivilizationShortDescription(0))
                



        def onBuildingBuilt(self, iPlayer, iBuilding, city):

                if (iBuilding >= iNumBuildingsPlague):
                        iEmbassy = iBuilding - iNumBuildingsPlague
                        if (gc.getPlayer(iEmbassy).isAlive() and gc.getPlayer(iEmbassy).getNumCities() > 0):
                                availableCity = -1
                                iMinNumEmbassies = 99
                                for pyCity in PyPlayer(iEmbassy).getCityList():
                                    
                                        if (pyCity.GetCy().hasBuilding(iNumBuildingsPlague + iPlayer)):
                                                #print (pyCity.GetCy().getName(), "HAS BUILDING")
                                                return
                                            
                                        #if (not pyCity.GetCy().isNationalWondersMaxed()):
                                        if (not pyCity.GetCy().isTeamWondersMaxed()):                                            
                                                iNumEmbassies = 0
                                                for j in range (con.iNumMajorPlayers):
                                                        if (pyCity.GetCy().hasBuilding(iNumBuildingsPlague + j)):
                                                                iNumEmbassies += 1
                                                if (iNumEmbassies < iMinNumEmbassies):
                                                        availableCity = pyCity.GetCy()
                                                        iMinNumEmbassies = iNumEmbassies
                                                        #print (pyCity.GetCy().getName(), "AVAILABLE")

                                if (availableCity != -1):
                                        availableCity.setHasRealBuilding(iNumBuildingsPlague + iPlayer, True)
                                        if (gc.getPlayer(iEmbassy).isHuman()):
                                                CyInterface().addMessage(iEmbassy, False, con.iDuration, CyTranslator().getText("TXT_KEY_EMBASSY_ESTABLISHED", (gc.getPlayer(iPlayer).getCivilizationAdjectiveKey(),)) + " " + availableCity.getName(), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)


        def onCityAcquired(self, city):

                for iLoopCiv in range (iNumMajorPlayers):
                        if (city.hasBuilding(iNumBuildingsPlague + iLoopCiv)):
				print "Delete building id: "+str(iNumBuildingsPlague + iLoopCiv)
                                city.setHasRealBuilding(iNumBuildingsPlague + iLoopCiv, False)
				print "Delete building id: "+str(iNumBuildingsPlague + iLoopCiv)+" passed."
                                print ("embassy deleted on city acquired", city.getName())
        

