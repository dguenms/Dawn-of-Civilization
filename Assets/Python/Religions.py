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

iIndonesia = con.iIndonesia
iArabia = con.iArabia
iRussia = con.iRussia
iVikings = con.iVikings
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
iOrthodoxy = con.iOrthodoxy
iIslam = con.iIslam
iHinduism = con.iHinduism
iBuddhism = con.iBuddhism
iConfucianism = con.iConfucianism
iTaoism = con.iTaoism
iZoroastrianism = con.iZoroastrianism

iMissionary_Jewish = con.iJewishMissionary
iMissionary_Christian = con.iChristianMissionary
iMissionary_Orthodox = con.iOrthodoxMissionary
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

lReformationMatrix = [80, 50, 50, 50, 80, 50, 50, 95, 50, 80, 50, 50, 90, 20, 80, 50, 50, 95, 75, 30, 55, 80, 10, 50, 95, 50, 50, 50, 50, 50, 50, 25, 20]

lOrthodoxFounders = (con.iByzantium, con.iGreece, con.iRussia, con.iEthiopia, con.iEgypt, con.iCarthage, con.iPersia, con.iBabylonia, con.iRome)
lOrthodoxEast = [con.iByzantium, con.iGreece, con.iRussia, con.iEthiopia, con.iEgypt, con.iCarthage, con.iPersia, con.iBabylonia]
lOrthodoxMiddle = [con.iByzantium, con.iGreece, con.iRussia, con.iEthiopia, con.iEgypt, con.iCarthage, con.iPersia, con.iBabylonia, con.iRome, con.iHolyRome, con.iVikings]
lOrthodoxWest = [con.iByzantium, con.iGreece, con.iRussia, con.iEthiopia, con.iEgypt, con.iCarthage, con.iPersia, con.iBabylonia, con.iRome, con.iHolyRome, con.iVikings, con.iFrance, con.iEngland]

class Religions:

##################################################
### Secure storage & retrieval of script data ###
################################################

        def getSeed( self ):
                return sd.scriptDict['iSeed']

        def setSeed( self ):
                sd.scriptDict['iSeed'] = gc.getGame().getSorenRandNum(100, 'Seed for random delay')
		
	def getReformationDecision(self, iCiv):
		return sd.scriptDict['lReformationDecision'][iCiv]
		
	def setReformationDecision(self, iCiv, iDecision):
		sd.scriptDict['lReformationDecision'][iCiv] = iDecision


#######################################
### Main methods (Event-Triggered) ###
#####################################  

        def setup(self):
                self.setSeed()
                

       	
        def checkTurn(self, iGameTurn):

		if utils.getHumanID() != con.iIndia:
			if iGameTurn == getTurnForYear(-2000)+1:
				if not gc.getGame().isReligionFounded(iHinduism):
					if not gc.getMap().plot(92, 39).getPlotCity().isNone():
						self.foundReligion((92, 39), iHinduism)

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
 
          
                #if (iGameTurn == getTurnForYear(622)+1):
                #        if (gc.getGame().isReligionFounded(iIslam)):
                #                for pyCity in PyPlayer(iArabia).getCityList():
                #                        if (pyCity.GetCy().isHolyCityByType(iIslam)):
                #                                if (gc.getPlayer(pyCity.GetCy().getOwner()).isHuman() == 0):
                #                                        print ("spreading Islam", iMissionary_Islamic)
                #                                        #self.spreadReligion( tMecca, 4, iMissionary_Islamic)
                #                                        self.spreadReligion( (pyCity.GetCy().getX(), pyCity.GetCy().getY()), 4, iMissionary_Islamic) 

                #if (iGameTurn == getTurnForYear(600)):
                #        if (not gc.getPlayer(0).isPlayable()): #late start condition
                #                pMecca = gc.getMap().plot(tMecca[0], tMecca[1])                
                #                if (not pMecca.getPlotCity().isNone()):                            
                #                        if (pMecca.getPlotCity().getOwner() == con.iArabia):
                #                                self.foundReligion(tMecca, iIslam)

		if iGameTurn == getTurnForYear(1500):
			#if gc.getGame().isReligionFounded(iJudaism):	# Protestantism founded
			#	gc.getPlayer(con.iNetherlands).setLastStateReligion(iJudaism) # make Protestantism Dutch state religion if already founded at their spawn
			#	utils.makeUnit(iMissionary_Jewish, con.iNetherlands, con.tCapitals[0][con.iNetherlands], 1)
			#else:
			#	utils.makeUnit(iMissionary_Christian, con.iNetherlands, con.tCapitals[0][con.iNetherlands], 1)

			# Islam spreads to Indonesia
			for i in range(3):
				self.spreadReligion(self.selectRandomCityCiv(iIndonesia), 1, iMissionary_Islamic)
				
		# (Orthodox) Christianity spreads to Russia
		if iGameTurn == getTurnForYear(900) - 5 + (utils.getSeed() % 10):
			for i in range(2):
				self.spreadReligion(self.selectRandomCityCiv(iVikings), 1, iMissionary_Christian)
		
		if iGameTurn == getTurnForYear(988):
			for i in range(2):
				self.spreadReligion(self.selectRandomCityCiv(iRussia), 1, iMissionary_Orthodox)
				
		if iGameTurn == getTurnForYear(800) + (utils.getSeed() % 20):
			if not gc.getGame().isReligionFounded(iOrthodoxy):
				self.foundOrthodoxy(con.iRome)
				
		# spread Buddhism to China
		if iGameTurn == getTurnForYear(100) - 5 + (utils.getSeed() % 10):
			for i in range(3):
				self.spreadReligion(self.selectRandomCityCiv(con.iChina), 1, iMissionary_Buddhist)
			


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

##BUDDHISM

	def foundBuddhism(self, city):
		gc.getPlayer(city.getOwner()).foundReligion(con.iBuddhism, con.iBuddhism, True)
		
		
##ORTHODOXY

	def canFoundOrthodoxy(self, iPlayer):
		return gc.getPlayer(iPlayer).isAlive() and gc.getPlayer(iPlayer).getStateReligion() == con.iChristianity

	def foundOrthodoxy(self, iPopeCiv):
		if gc.getGame().isReligionFounded(con.iOrthodoxy): return
	
		iOwner = gc.getGame().getHolyCity(con.iChristianity).getOwner()
		pOwner = gc.getPlayer(iOwner)
		iFounder = iPopeCiv
		
		#if iOwner != iPopeCiv and iOwner < con.iNumPlayers and pOwner.getStateReligion() == con.iChristianity:
		#	iFounder = iOwner
		#	print "Set Orthodoxy founder: "+str(iFounder)
		#else:
		if self.canFoundOrthodoxy(con.iByzantium): iFounder = con.iByzantium
		elif self.canFoundOrthodoxy(con.iGreece): iFounder = con.iGreece
		elif self.canFoundOrthodoxy(con.iRussia): iFounder = con.iRussia
		elif self.canFoundOrthodoxy(con.iEthiopia): iFounder = con.iEthiopia
		elif self.canFoundOrthodoxy(con.iEgypt): iFounder = con.iEgypt
		elif self.canFoundOrthodoxy(con.iCarthage): iFounder = con.iCarthage
		elif self.canFoundOrthodoxy(con.iBabylonia): iFounder = con.iBabylonia

					
		print "Final Orthodoxy founder: "+str(iFounder)
					
                gc.getPlayer(iFounder).foundReligion(con.iOrthodoxy, con.iOrthodoxy, True)
                gc.getPlayer(iFounder).getCapitalCity().setNumRealBuilding(con.iOrthodoxShrine, 1)
		
		if con.tBirth[utils.getHumanID()] <= getTurnForYear(gc.getGame().getGameTurnYear()) and gc.getPlayer(utils.getHumanID()).getStateReligion() == con.iChristianity:
			self.showPopup(7626, CyTranslator().getText("TXT_KEY_SCHISM_TITLE", ()), CyTranslator().getText("TXT_KEY_SCHISM_MESSAGE", ()), (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_NO", ())))
		
		if iFounder in lOrthodoxEast:
			for iCiv in lOrthodoxEast:
				if gc.getPlayer(iCiv).isAlive(): self.schism(iCiv)
		elif iFounder in lOrthodoxMiddle:
			for iCiv in lOrthodoxMiddle:
				if gc.getPlayer(iCiv).isAlive(): self.schism(iCiv)
		elif iFounder in lOrthodoxWest:
			for iCiv in lOrthodoxWest:
				if gc.getPlayer(iCiv).isAlive(): self.schism(iCiv)
		else:
			for iCiv in range(con.iNumPlayers):
				if gc.getPlayer(iCiv).isAlive(): self.schism(iCiv)
				
		for iCiv in [con.iEthiopia, con.iGreece, con.iByzantium, con.iRussia]:
			if not gc.getPlayer(iCiv).isAlive():
				gc.getPlayer(iCiv).setLastStateReligion(con.iOrthodoxy)
				
	def eventApply7626(self, popupReturn):
		if (popupReturn.getButtonClicked() == 0):
			self.schism(utils.getHumanID())
			
	def schism(self, iPlayer):
		cityList = PyPlayer(iPlayer).getCityList()
		for city in cityList:
			pCity = city.GetCy()
			if pCity.isHasReligion(iChristianity):
				pCity.setHasReligion(iChristianity, False, False, False)
			
				for iBuilding in [con.iTemple, con.iCathedral, con.iMonastery]:
					if pCity.isHasBuilding(iBuilding + 4*iChristianity):
						pCity.setHasRealBuilding(iBuilding + 4*iChristianity, False)
						pCity.setHasRealBuilding(iBuilding + 4*iOrthodoxy, True)
						
				if pCity.getPopulation() > 7:
					iRand = gc.getGame().getSorenRandNum(100, 'RemainingCatholics')
					if iRand <= 50:
						pCity.setHasReligion(iChristianity, True, False, False)
						
				pCity.setHasReligion(con.iOrthodoxy, True, False, False)
				
		if gc.getPlayer(iPlayer).getStateReligion() == iChristianity:
			gc.getPlayer(iPlayer).setLastStateReligion(iOrthodoxy)
				
		
		

##REFORMATION

        def showPopup(self, popupID, title, message, labels):
                popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
                popup.setHeaderString(title)
                popup.setBodyString(message)
                for i in labels:
                    popup.addButton( i )
                popup.launch(False)

        def reformationPopup(self):
                self.showPopup(7624, CyTranslator().getText("TXT_KEY_REFORMATION_TITLE", ()), CyTranslator().getText("TXT_KEY_REFORMATION_MESSAGE",()), (CyTranslator().getText("TXT_KEY_REFORMATION_1", ()), CyTranslator().getText("TXT_KEY_REFORMATION_2", ()), CyTranslator().getText("TXT_KEY_REFORMATION_3", ())))

        def eventApply7624(self, popupReturn):
                iHuman = utils.getHumanID()
                if popupReturn.getButtonClicked() == 0:
                        self.embraceReformation(iHuman)
                elif popupReturn.getButtonClicked() == 1:
                        self.tolerateReformation(iHuman)
		elif popupReturn.getButtonClicked() == 2:
			self.counterReformation(iHuman)

        def onTechAcquired(self, iTech, iPlayer):
                if (iTech == con.iPrintingPress):
                        if (gc.getPlayer(iPlayer).getStateReligion() == con.iChristianity):
                                if (not gc.getGame().isReligionFounded(con.iJudaism)):
					gc.getPlayer(iPlayer).foundReligion(con.iJudaism, con.iJudaism, True)
                                        #gc.getPlayer(iPlayer).getCapitalCity().setNumRealBuilding(con.iJewishShrine,1)
                                        self.reformation()
					
	def chooseProtestantism(self, iCiv):
		if iCiv < con.iNumPlayers:
			iThreshold = lReformationMatrix[iCiv]
		else:
			iThreshold = 50
		iRand = gc.getGame().getSorenRandNum(100, 'Protestantism Choice')
		return iRand >= iThreshold
		
	def isProtestantAnyway(self, iCiv):
		if iCiv < con.iNumPlayers:
			iThreshold = (lReformationMatrix[iCiv]+50)/2
		else:
			iThreshold = 50
		iRand = gc.getGame().getSorenRandNum(100, 'Protestantism anyway')
		return iRand >= iThreshold

        def reformation(self):
                for iCiv in range(iNumTotalPlayers):
			#if gc.getPlayer(iCiv).getStateReligion() == iChristianity:
			#	self.reformationchoice(iCiv)
                        cityList = PyPlayer(iCiv).getCityList()
			bCatholic = False
                        for city in cityList:
                                if city.hasReligion(con.iChristianity):
					bCatholic = True
			if bCatholic:
				self.reformationchoice(iCiv)
		
		print "Reformation decisions:"
		for iCiv in range(iNumPlayers):
			print CyTranslator().getText(str(gc.getPlayer(iCiv).getCivilizationShortDescriptionKey()),()) + ": " + str(self.getReformationDecision(iCiv))
		
		#print "Reformation matrix:"
		#for iCiv in range(iNumPlayers):
		#	print CyTranslator().getText(str(gc.getPlayer(iCiv).getCivilizationShortDescriptionKey()),()) + ": " + str(lReformationMatrix[iCiv])
		
		for iCiv in range(iNumPlayers):
			if self.getReformationDecision(iCiv) == 2:
				for iTargetCiv in range(iNumPlayers):
					if self.getReformationDecision(iTargetCiv) == 0 and utils.getHumanID() != iTargetCiv and iTargetCiv != con.iNetherlands: # protect the Dutch or they'll get crushed
						gc.getTeam(iCiv).declareWar(iTargetCiv, True, WarPlanTypes.WARPLAN_DOGPILE)
						print "Religious war: "+str(iCiv)+" declares war on "+str(iTargetCiv)
						
		pHolyCity = gc.getGame().getHolyCity(con.iJudaism)
		if self.getReformationDecision(pHolyCity.getOwner()) == 0:
			pHolyCity.setNumRealBuilding(con.iJewishShrine, 1)
			
		# Make Netherlands spawn as Protestant if it's already founded
		if not gc.getPlayer(con.iNetherlands).isAlive():
			gc.getPlayer(con.iNetherlands).setLastStateReligion(con.iProtestantism)

        def reformationchoice(self, iCiv):
		pPlayer = gc.getPlayer(iCiv)
		
		if utils.getHumanID() == iCiv: return
	
		if pPlayer.getStateReligion() == iChristianity:
			if self.chooseProtestantism(iCiv):
				self.embraceReformation(iCiv)
			else:
				if self.isProtestantAnyway(iCiv) or utils.isAVassal(iCiv):
					self.tolerateReformation(iCiv)
				else:
					self.counterReformation(iCiv)
		else:
			self.tolerateReformation(iCiv)
					
	def embraceReformation(self, iCiv):
		cityList = PyPlayer(iCiv).getCityList()
		iNumCatholicCities = 0
		for city in cityList:
			pCity = city.GetCy()
			if pCity.isHasReligion(iChristianity):
				iNumCatholicCities += 1
			
				if not pCity.isHolyCityByType(iChristianity):
					pCity.setHasReligion(iChristianity, False, False, False)
			
				for iBuilding in [con.iTemple, con.iCathedral, con.iMonastery]:
					if pCity.isHasBuilding(iBuilding + 4*iChristianity):
						pCity.setHasRealBuilding(iBuilding + 4*iChristianity, False)
						pCity.setHasRealBuilding(iBuilding + 4*iJudaism, True)
						
				if pCity.getPopulation() > 7:
					if not self.chooseProtestantism(iCiv):
						pCity.setHasReligion(iChristianity, True, False, False)
								
				pCity.setHasReligion(iJudaism, True, False, False)
				
		pPlayer = gc.getPlayer(iCiv)
		pPlayer.changeGold(iNumCatholicCities*100)
		
		pPlayer.setLastStateReligion(iJudaism)
		pPlayer.setConversionTimer(10)
		
		if iCiv < con.iNumPlayers:
			self.setReformationDecision(iCiv, 0)
		
	def tolerateReformation(self, iCiv):
		cityList = PyPlayer(iCiv).getCityList()
		for city in cityList:
			pCity = city.GetCy()
			if pCity.isHasReligion(iChristianity):
				if self.isProtestantAnyway(iCiv):
					if pCity.getPopulation() <= 9 and not pCity.isHolyCityByType(iChristianity):
						pCity.setHasReligion(iChristianity, False, False, False)
					pCity.setHasReligion(iJudaism, True, False, False)
		
		if iCiv < con.iNumPlayers:
			self.setReformationDecision(iCiv, 1)
					
	def counterReformation(self, iCiv):
		cityList = PyPlayer(iCiv).getCityList()
		for city in cityList:
			pCity = city.GetCy()
			if pCity.isHasReligion(iChristianity):
				if self.chooseProtestantism(iCiv):
					if pCity.getPopulation() > 6:
						pCity.setHasReligion(iJudaism, True, False, False)
						
			#pCity.changeBuildingCommerceChange(gc.getInfoTypeForString("BUILDINGCLASS_CHRISTIAN_MONASTERY"), 1, 2)
		
		if iCiv < con.iNumPlayers:
			self.setReformationDecision(iCiv, 2)
		

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
