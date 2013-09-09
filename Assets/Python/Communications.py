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
	  con.iBrazil,
	  con.iArgentina)


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
                iCounter = 0
		
		# Initialize list
		lContacts = [i for i in range(con.iNumPlayers) if gc.getPlayer(i).isAlive() and teamCiv.canContact(i)]

		# If other civs can see our borders
		for city in utils.getCityList(iCiv):
			for iOtherCiv in lContacts:
				if city.hasBuilding(iNumBuildingsPlague + iOtherCiv):
					lContacts.remove(iOtherCiv)
				elif city.plot().isVisible(iOtherCiv, False):
					lContacts.remove(iOtherCiv)
			# Leoreth: this is very inefficient, find a better way
			x = city.getX()
			y = city.getY()
			r = city.getCultureLevel()
			for i in range(x-r, x+r+1):
				for j in range(y-r, y+r+1):
					plot = gc.getMap().plot(i, j)
					for iOtherCiv in lContacts:
						if plot.getOwner() == iOtherCiv:
							lContacts.remove(iOtherCiv)
							
		# If we can see their borders (view distance is asymmetrical)
		lRemove = []
		for iOtherCiv in lContacts:
			for city in utils.getCityList(iOtherCiv):
				if city.hasBuilding(iNumBuildingsPlague + iCiv):
					lRemove.append(iOtherCiv)
				elif city.plot().isVisible(iCiv, False):
					lRemove.append(iOtherCiv)
				else:
					x = city.getX()
					y = city.getY()
					r = city.getCultureLevel()
					for i in range(x-r, x+r+1):
						for j in range(y-r, y+r+1):
							plot = gc.getMap().plot(i, j)
							if plot.isVisible(iOtherCiv, False) and plot.getOwner() == iCiv:
								lRemove.append(iOtherCiv)
								
		for iLoopCiv in lRemove:
			if iLoopCiv in lContacts: lContacts.remove(iLoopCiv)
								
		# master/vassal relationships: if master can be seen, don't cut vassal contact and vice versa
		lRemove = []
		for iLoopPlayer in range(con.iNumPlayers):
			for iContact in lContacts:
				if gc.getTeam(iContact).isVassal(iLoopPlayer) and iLoopPlayer not in lContacts:
					lRemove.append(iContact)
				elif gc.getTeam(iLoopPlayer).isVassal(iContact) and iLoopPlayer not in lContacts:
					lRemove.append(iContact)
					
		for iLoopCiv in lRemove:
			if iLoopCiv in lContacts: lContacts.remove(iLoopCiv)
								
		# choose up to four random contacts to cut
		for i in range(4):
			if len(lContacts) == 0: break
			
			iContact = utils.getRandomEntry(lContacts)
			#utils.debugTextPopup('Cut contact between ' + gc.getPlayer(iCiv).getCivilizationShortDescription(0) + ' and ' + gc.getPlayer(iContact).getCivilizationShortDescription(0))
			teamCiv.cutContact(iContact)



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
        

