# Rhye's and Fall of Civilization - Religions management

from CvPythonExtensions import *
import CvUtil
import PyHelpers       
import Popup
#import cPickle as pickle     	
from Consts import *
import CvTranslator
import RFCUtils
from StoredData import sd #edead

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()

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

lCatholicCivs = [iCarthage, iRome, iRome, iGreece, iGreece, iByzantium, iByzantium]

dCatholicPreference = {
iEgypt		: 80,
iGreece		: 80,
iRome		: 95,
iEthiopia	: 80,
iByzantium	: 90,
iVikings	: 20,
iArabia		: 80,
iSpain		: 95,
iFrance		: 75,
iEngland	: 30,
iHolyRome	: 55,
iRussia		: 80,
iNetherlands	: 10,
iPoland		: 80,
iPortugal	: 95,
iItaly		: 90,
iCongo		: 80,
iGermany	: 25,
iAmerica	: 20,
}

def getCatholicPreference(iPlayer):
	if iPlayer not in dCatholicPreference:
		return 50
	return dCatholicPreference[iPlayer]

lOrthodoxFounders = (iByzantium, iGreece, iRussia, iEthiopia, iEgypt, iCarthage, iPersia, iBabylonia, iRome)
lOrthodoxEast = [iByzantium, iGreece, iRussia, iEthiopia, iEgypt, iCarthage, iPersia, iBabylonia]
lOrthodoxMiddle = [iByzantium, iGreece, iRussia, iEthiopia, iEgypt, iCarthage, iPersia, iBabylonia, iRome, iHolyRome, iVikings]
lOrthodoxWest = [iByzantium, iGreece, iRussia, iEthiopia, iEgypt, iCarthage, iPersia, iBabylonia, iRome, iHolyRome, iVikings, iFrance, iEngland]

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
	
		if utils.getHumanID() != iIndia:
			if iGameTurn == getTurnForYear(-2000)+1:
				if not gc.getGame().isReligionFounded(iHinduism):
					if not gc.getMap().plot(92, 39).getPlotCity().isNone():
						self.foundReligion((92, 39), iHinduism)

		if iGameTurn == getTurnForYear(-1200) - utils.getTurns(5) + utils.getTurns(utils.getSeed() % 10):
			if gc.getMap().plot(tJerusalem[0], tJerusalem[1]).isCity():
				self.foundReligion(tJerusalem, iJudaism)
			else:
				self.foundReligion(utils.getRandomEntry(utils.getAreaCities(utils.getPlotList(tJewishTL, tJewishBR))), iJudaism)

		self.checkChristianity(iGameTurn)
						
		self.checkSchism(iGameTurn)

		self.spreadJudaismEurope(iGameTurn)
		self.spreadJudaismMiddleEast(iGameTurn)


	def foundReligion(self, tPlot, iReligion):
		if not tPlot: return
		
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		if plot.isCity():
			gc.getGame().setHolyCity(iReligion, plot.getPlotCity(), True)
			return True
			
		return False
		
		
	def onReligionFounded(self, iReligion, iFounder):
		if iReligion == iCatholicism:
			for iPlayer in lCatholicStart:
				if gc.getGame().getGameTurn() < getTurnForYear(tBirth[iPlayer]):
					gc.getPlayer(iPlayer).setLastStateReligion(iCatholicism)
					
		elif iReligion == iProtestantism:
			for iPlayer in lProtestantStart:
				if gc.getGame().getGameTurn() < getTurnForYear(tBirth[iPlayer]):
					gc.getPlayer(iPlayer).setLastStateReligion(iProtestantism)
					
	def getReligionCities(self, iReligion):
		lCities = []
		for iPlayer in range(iNumTotalPlayersB):
			lCities.extend(utils.getCityList(iPlayer))
			
		return [city for city in lCities if city.isHasReligion(iReligion)]

	def selectRandomCityCiv(self, iCiv):
		if (gc.getPlayer(iCiv).isAlive()):
			cityList = []
			for pyCity in PyPlayer(iCiv).getCityList():
				cityList.append(pyCity.GetCy())
			iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
			if len(cityList) == 0: return False
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
		if not tCoords or not gc.getMap().plot(tCoords[0], tCoords[1]).isCity(): return
		city = gc.getMap().plot( tCoords[0], tCoords[1] ).getPlotCity()
		#print city
		#print city.getOwner()
		utils.makeUnit(iMissionary, city.getOwner(), tCoords, iNum)
		
## JUDAISM

	def spreadJudaismEurope(self, iGameTurn):
		if not gc.getGame().isReligionFounded(iJudaism): return
		if iGameTurn < getTurnForYear(1000): return
		
		if iGameTurn % utils.getTurns(10) != 0: return
	
		lEuropeanCities = utils.getRegionCities([rIberia, rEurope, rItaly, rBritain, rRussia, rBalkans])
		lJewishCities = [city for city in lEuropeanCities if city.isHasReligion(iJudaism)]
		
		if 2 * len(lJewishCities) < len(lEuropeanCities):
			pSpreadCity = utils.getRandomEntry([city for city in lEuropeanCities if not city.isHasReligion(iJudaism)])
			if pSpreadCity:
				pSpreadCity.setHasReligion(iJudaism, True, True, True)
				
	def spreadJudaismMiddleEast(self, iGameTurn):
		if not gc.getGame().isReligionFounded(iJudaism): return
		if iGameTurn < getTurnForYear(600): return
		
		if iGameTurn % utils.getTurns(20) != utils.getTurns(5): return
		
		lMiddleEastCities = utils.getRegionCities([rMesopotamia, rAnatolia, rEgypt])
		lJewishCities = [city for city in lMiddleEastCities if city.isHasReligion(iJudaism)]
		
		if 2 * len(lJewishCities) < len(lMiddleEastCities):
			pSpreadCity = utils.getRandomEntry([city for city in lMiddleEastCities if not city.isHasReligion(iJudaism)])
			if pSpreadCity:
				pSpreadCity.setHasReligion(iJudaism, True, True, True)
		
		
## ORTHODOXY

	def checkChristianity(self, iGameTurn):
		if not gc.getGame().isReligionFounded(iJudaism): return
		if gc.getGame().isReligionFounded(iOrthodoxy): return
		
		iEthiopiaOffset = 0
		if utils.getHumanID() == iEthiopia: iEthiopiaOffset = utils.getTurns(10 + utils.getSeed() % 5)
		iOffset = utils.getTurns(utils.getSeed() % 15)
		
		if iGameTurn == getTurnForYear(0) + iOffset + iEthiopiaOffset:
			if gc.getGame().getSorenRandNum(2, "Holy city?") == 0:
				pChristianCity = gc.getGame().getHolyCity(iJudaism)
				self.foundReligion((pChristianCity.getX(), pChristianCity.getY()), iOrthodoxy)
				return

			lJewishCities = []
			for iPlayer in range(iNumTotalPlayersB):
				lJewishCities.extend([city for city in utils.getCityList(iPlayer) if city.isHasReligion(iJudaism)])
				
			pChristianCity = utils.getRandomEntry(lJewishCities)
			
			self.foundReligion((pChristianCity.getX(), pChristianCity.getY()), iOrthodoxy)
			
		
##BUDDHISM

	def foundBuddhism(self, city):
		gc.getPlayer(city.getOwner()).foundReligion(iBuddhism, iBuddhism, True)
		
		
## CATHOLICISM

	def checkSchism(self, iGameTurn):
		if not gc.getGame().isReligionFounded(iOrthodoxy): return
		if gc.getGame().isReligionFounded(iCatholicism): return
		
		lStateReligionCities = []
		lNoStateReligionCities = []
		lDifferentStateReligionCities = []
		lMinorCities = []
		
		for iPlayer in range(iNumTotalPlayersB):
			iStateReligion = gc.getPlayer(iPlayer).getStateReligion()
			lCities = [city for city in utils.getCityList(iPlayer) if city.isHasReligion(iOrthodoxy)]
			if iStateReligion == iOrthodoxy: lStateReligionCities.extend(lCities)
			elif gc.getPlayer(iPlayer).isMinorCiv() or gc.getPlayer(iPlayer).isBarbarian(): lMinorCities.extend(lCities)
			elif iStateReligion == -1: lNoStateReligionCities.extend(lCities)
			else: lDifferentStateReligionCities.extend(lCities)
			
		if not lStateReligionCities: return
		if not lNoStateReligionCities and not lMinorCities: return
		
		if len(lStateReligionCities) >= len(lNoStateReligionCities) + len(lMinorCities): return
		
		lOrthodoxCapitals = [city for city in lStateReligionCities if city.isCapital()]
		
		if lOrthodoxCapitals:
			pOrthodoxCapital = utils.getHighestEntry(lOrthodoxCapitals, lambda city: gc.getPlayer(city.getOwner()).getScoreHistory(iGameTurn))
		else:
			pOrthodoxCapital = gc.getGame().getHolyCity(iOrthodoxy)
		
		lCatholicCities = []
		lCatholicCities.extend(lNoStateReligionCities)
		lCatholicCities.extend(lMinorCities)
		pCatholicCapital = utils.getHighestEntry([city for city in lCatholicCities if city.plot().getSpreadFactor(iCatholicism) >= 3 and city != pOrthodoxCapital], lambda city: city.getPopulation())
		
		if not pCatholicCapital:
			pCatholicCapital = utils.getHighestEntry(lCatholicCities, lambda city: city.getPopulation())
		
		self.foundReligion((pCatholicCapital.getX(), pCatholicCapital.getY()), iCatholicism)
		
		print str(lNoStateReligionCities)
		for city in lNoStateReligionCities:
			print "Replace Orthodoxy with Catholicism: " + str(city.getName())
			city.replaceReligion(iOrthodoxy, iCatholicism)
		
		lIndependentCities = []
		lIndependentCities.extend(lDifferentStateReligionCities)
		lIndependentCities.extend(lMinorCities)
		print str(lIndependentCities)
		for city in lIndependentCities:
			if stepDistance(city.getX(), city.getY(), pCatholicCapital.getX(), pCatholicCapital.getY()) > stepDistance(city.getX(), city.getY(), pOrthodoxCapital.getX(), pOrthodoxCapital.getY()):
				print "Replace Orthodoxy with Catholicism: " + str(city.getName())
				city.replaceReligion(iOrthodoxy, iCatholicism)
			else:
				print "Keep Orthodoxy: " + str(city.getName())
				
		if gc.getPlayer(utils.getHumanID()).getStateReligion() == iOrthodoxy and iGameTurn >= getTurnForYear(tBirth[utils.getHumanID()]):
			utils.popup(CyTranslator().getText("TXT_KEY_SCHISM_TITLE", ()), CyTranslator().getText("TXT_KEY_SCHISM_MESSAGE", (pCatholicCapital.getName(),)), ())		

#REFORMATION

	def showPopup(self, popupID, title, message, labels):
		popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setHeaderString(title)
		popup.setBodyString(message)
		for i in labels:
		    popup.addButton( i )
		popup.launch(len(labels) == 0)

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
		if utils.getScenario() == i1700AD:
			return
	
		if (iTech == iPrintingPress):
			if (gc.getPlayer(iPlayer).getStateReligion() == iCatholicism):
				if (not gc.getGame().isReligionFounded(iProtestantism)):
					gc.getPlayer(iPlayer).foundReligion(iProtestantism, iProtestantism, True)
					#gc.getPlayer(iPlayer).getCapitalCity().setNumRealBuilding(iProtestantShrine,1)
					self.reformation()
					
	def chooseProtestantism(self, iCiv):
		iRand = gc.getGame().getSorenRandNum(100, 'Protestantism Choice')
		return iRand >= getCatholicPreference(iCiv)
		
	def isProtestantAnyway(self, iCiv):
		iRand = gc.getGame().getSorenRandNum(100, 'Protestantism anyway')
		return iRand >= (getCatholicPreference(iCiv)+50)/2

	def reformation(self):
		for iCiv in range(iNumTotalPlayers):
			#if gc.getPlayer(iCiv).getStateReligion() == iCatholicism:
			#	self.reformationchoice(iCiv)
			cityList = PyPlayer(iCiv).getCityList()
			bCatholic = False
			for city in cityList:
				if city.hasReligion(iCatholicism):
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
					if self.getReformationDecision(iTargetCiv) == 0 and utils.getHumanID() != iTargetCiv and iTargetCiv != iNetherlands and not utils.isAVassal(iTargetCiv): # protect the Dutch or they'll get crushed
						gc.getTeam(iCiv).declareWar(iTargetCiv, True, WarPlanTypes.WARPLAN_DOGPILE)
						print "Religious war: "+str(iCiv)+" declares war on "+str(iTargetCiv)
						
		pHolyCity = gc.getGame().getHolyCity(iProtestantism)
		if self.getReformationDecision(pHolyCity.getOwner()) == 0:
			pHolyCity.setNumRealBuilding(iProtestantShrine, 1)
			
		# Make Netherlands spawn as Protestant if it's already founded
		if gc.getGame().getGameTurn() < getTurnForYear(tBirth[iNetherlands]):
			gc.getPlayer(iNetherlands).setLastStateReligion(iProtestantism)

	def reformationchoice(self, iCiv):
		pPlayer = gc.getPlayer(iCiv)
		
		if utils.getHumanID() == iCiv: return
	
		if pPlayer.getStateReligion() == iCatholicism:
			if self.chooseProtestantism(iCiv):
				self.embraceReformation(iCiv)
			elif self.isProtestantAnyway(iCiv) or utils.isAVassal(iCiv):
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
			if pCity.isHasReligion(iCatholicism):
				iNumCatholicCities += 1
				
				pCity.replaceReligion(iCatholicism, iProtestantism)
				
				if pCity.getPopulation() > 7:
					if not self.chooseProtestantism(iCiv):
						pCity.setHasReligion(iCatholicism, True, False, False)
				
		pPlayer = gc.getPlayer(iCiv)
		pPlayer.changeGold(iNumCatholicCities*100)
		
		pPlayer.setLastStateReligion(iProtestantism)
		pPlayer.setConversionTimer(10)
		
		if iCiv < iNumPlayers:
			self.setReformationDecision(iCiv, 0)
		
	def tolerateReformation(self, iCiv):
		cityList = PyPlayer(iCiv).getCityList()
		for city in cityList:
			pCity = city.GetCy()
			if pCity.isHasReligion(iCatholicism):
				if self.isProtestantAnyway(iCiv):
					if pCity.getPopulation() <= 9 and not pCity.isHolyCityByType(iCatholicism):
						pCity.setHasReligion(iCatholicism, False, False, False)
					pCity.setHasReligion(iProtestantism, True, False, False)
		
		if iCiv < iNumPlayers:
			self.setReformationDecision(iCiv, 1)
					
	def counterReformation(self, iCiv):
		cityList = PyPlayer(iCiv).getCityList()
		for city in cityList:
			pCity = city.GetCy()
			if pCity.isHasReligion(iCatholicism):
				if self.chooseProtestantism(iCiv):
					if pCity.getPopulation() > 6:
						pCity.setHasReligion(iProtestantism, True, False, False)
						
			#pCity.changeBuildingCommerceChange(gc.getInfoTypeForString("BUILDINGCLASS_CATHOLIC_MONASTERY"), 1, 2)
		
		if iCiv < iNumPlayers:
			self.setReformationDecision(iCiv, 2)
		

	def reformationyes(self, iCiv):
		for city in utils.getCityList(iCiv):
			city.replaceReligion(iCatholicism, iProtestantism)
			
			if city.getPopulation() > 7:
				iRand = gc.getGame().getSorenRandNum(100, "Reformation residual")
				if iRand <= lReformationMatrix[iCiv]:
					city.setHasReligion(iCatholicism, True, False, False)

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
					city.city.setHasReligion(iProtestantism, True, False, False)
