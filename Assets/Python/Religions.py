# Rhye's and Fall of Civilization - Religions management

from CvPythonExtensions import *
import CvUtil
import PyHelpers       
import Popup
#import cPickle as pickle     	
from Consts import *
import CvTranslator
from RFCUtils import utils
from StoredData import data #edead

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

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

#######################################
### Main methods (Event-Triggered) ###
#####################################
		
	def checkTurn(self, iGameTurn):
	
		if utils.getHumanID() != iIndia:
			if iGameTurn == getTurnForYear(-2000)+1:
				if not gc.getGame().isReligionFounded(iHinduism):
					if not gc.getMap().plot(92, 39).getPlotCity().isNone():
						self.foundReligion((92, 39), iHinduism)
				
		self.checkJudaism(iGameTurn)
		
		#self.checkBuddhism(iGameTurn)

		self.checkChristianity(iGameTurn)
						
		self.checkSchism(iGameTurn)

		self.spreadJudaismEurope(iGameTurn)
		self.spreadJudaismMiddleEast(iGameTurn)
		self.spreadJudaismAmerica(iGameTurn)
		
		self.spreadIslamIndonesia(iGameTurn)


	def foundReligion(self, tPlot, iReligion):
		if not tPlot: return
		
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		if plot.isCity():
			gc.getGame().setHolyCity(iReligion, plot.getPlotCity(), True)
			return True
			
		return False
		
		
	def onReligionFounded(self, iReligion, iFounder):
		if gc.getGame().getGameTurn() == utils.getScenarioStartTurn(): return
	
		if iReligion == iCatholicism:
			utils.setStateReligionBeforeBirth(lCatholicStart, iCatholicism)
			utils.setStateReligionBeforeBirth(lProtestantStart, iCatholicism)
			
		elif iReligion == iProtestantism:
			utils.setStateReligionBeforeBirth(lProtestantStart, iProtestantism)
					
	def getReligionCities(self, iReligion): # Unused
		lCities = []
		for iPlayer in range(iNumTotalPlayersB):
			lCities.extend(utils.getCityList(iPlayer))
			
		return [city for city in lCities if city.isHasReligion(iReligion)]

	def selectRandomCityCiv(self, iCiv): # Unused
		if gc.getPlayer(iCiv).isAlive():
			city = utils.getRandomEntry(utils.getCityList(iCiv))
			if city:
				return (city.getX(), city.getY())
		return False
	    

	def selectRandomCityArea(self, tTopLeft, tBottomRight): # Unused
		cityList = []
		for (x, y) in utils.getPlotList(tTopLeft, tBottomRight):
			pPlot = gc.getMap().plot(x, y)
			if pPlot.isCity():
				cityList.append((x, y))
		if cityList:
			return utils.getRandomEntry(cityList)
		return False


	def selectRandomCityAreaCiv(self, tTopLeft, tBottomRight, iCiv = -1): # Unused
		cityList = []
		for (x, y) in utils.getPlotList(tTopLeft, tBottomRight):
			pPlot = gc.getMap().plot( x, y )
			if pPlot.isCity():
				if (iCiv != -1 and pPlot.getPlotCity().getOwner() != iCiv): continue
				cityList.append((x, y))
		if cityList:
			return utils.getRandomEntry(cityList)
		return False



	def selectRandomCityReligion(self, iReligion): # Unused
		if gc.getGame().isReligionFounded(iReligion):
			cityList = []
			for iPlayer in range(iNumPlayers):
				for city in utils.getCityList(iPlayer):
					if city.isHasReligion(iReligion):
						cityList.append(city)
			if cityList:
				iCity = utils.getRandomEntry(cityList)
				return (city.getX(), city.getY())
		return False


	def selectRandomCityReligionCiv(self, iReligion, iCiv = -1): # Unused
		if gc.getGame().isReligionFounded(iReligion):
			cityList = []
			for iPlayer in range(iNumPlayers):
				if iCiv != -1 and iPlayer != iCiv: continue
				for city in utils.getCityList(iPlayer):
					if city.isHasReligion(iReligion):
						cityList.append(city)
			if cityList:
				city = utils.getRandomEntry(cityList)
				return (city.getX(), city.getY())
		return False


	def spreadReligion(self, tCoords, iNum, iMissionary): # Unused
		x, y = tCoords
		if not tCoords or not gc.getMap().plot(x, y).isCity(): return
		city = gc.getMap().plot(x, y).getPlotCity()
		#print city
		#print city.getOwner()
		utils.makeUnit(iMissionary, city.getOwner(), tCoords, iNum)
		
	def getTargetCities(self, lCities, iReligion):
		return [city for city in lCities if not city.isHasReligion(iReligion) and gc.getPlayer(city.getOwner()).getSpreadType(city.plot(), iReligion) > ReligionSpreadTypes.RELIGION_SPREAD_NONE]
		
	def selectHolyCity(self, tTL, tBR, tPreferredCity = None, bAIOnly = True):
		if tPreferredCity:
			x, y = tPreferredCity
			if gc.getMap().plot(x, y).isCity():
				if not bAIOnly or utils.getHumanID() != gc.getMap().plot(x, y).getPlotCity().getOwner():
					return tPreferredCity
		
		lCities = [city for city in utils.getAreaCities(utils.getPlotList(tTL, tBR)) if not bAIOnly or city.getOwner() != utils.getHumanID()]
		
		if lCities:
			city = utils.getRandomEntry(lCities)
			return (city.getX(), city.getY())
			
		return None
		
	def checkLateReligionFounding(self, iReligion, iTech):
		if gc.getReligionInfo(iReligion).getTechPrereq() != iTech:
			return
			
		if gc.getGame().isReligionFounded(iReligion):
			return
		
		iPlayerCount = 0
		iPrereqCount = 0
		for iPlayer in range(iNumPlayers):
			if gc.getPlayer(iPlayer).isAlive():
				iPlayerCount += 1
				if gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isHasTech(iTech):
					iPrereqCount += 1
					
		if 2 * iPrereqCount >= iPlayerCount:
			self.foundReligionInCore(iReligion)
			
	def foundReligionInCore(self, iReligion):
		lCoreCities = [city for city in utils.getAllCities() if city.plot().getSpreadFactor(iReligion) == RegionSpreadTypes.REGION_SPREAD_CORE]
		
		if not lCoreCities: return
		
		city = utils.getRandomEntry(lCoreCities)
		
		self.foundReligion((city.getX(), city.getY()), iReligion)
					
## JUDAISM

	def checkJudaism(self, iGameTurn):
		if gc.getGame().isReligionFounded(iJudaism): return

		if iGameTurn == getTurnForYear(-1500) - utils.getTurns(data.iSeed % 5):
			self.foundReligion(self.selectHolyCity(tJewishTL, tJewishBR, tJerusalem), iJudaism)
			
	def spreadJudaismEurope(self, iGameTurn):
		self.spreadReligionToRegion(iJudaism, [rIberia, rEurope, rItaly, rBritain, rRussia, rBalkans], iGameTurn, 1000, 10, 0)
				
	def spreadJudaismMiddleEast(self, iGameTurn):
		self.spreadReligionToRegion(iJudaism, [rMesopotamia, rAnatolia, rEgypt], iGameTurn, 600, 20, 5)
		
	def spreadJudaismAmerica(self, iGameTurn):
		self.spreadReligionToRegion(iJudaism, [rCanada, rAlaska, rUnitedStates], iGameTurn, 1850, 10, 4)
				
	def spreadReligionToRegion(self, iReligion, lRegions, iGameTurn, iStartDate, iInterval, iOffset):
		if not gc.getGame().isReligionFounded(iReligion): return
		if iGameTurn < getTurnForYear(iStartDate): return
		
		if iGameTurn % utils.getTurns(iInterval) != iOffset: return
		
		lRegionCities = utils.getRegionCities(lRegions)
		lReligionCities = [city for city in lRegionCities if city.isHasReligion(iReligion)]
		
		if 2 * len(lReligionCities) < len(lRegionCities):
			pSpreadCity = utils.getRandomEntry(self.getTargetCities(lRegionCities, iReligion))
			if pSpreadCity:
				pSpreadCity.spreadReligion(iReligion)
				
## ISLAM

	def spreadIslamIndonesia(self, iGameTurn):
		if not gc.getGame().isReligionFounded(iIslam): return
		if not pIndonesia.isAlive(): return
		if not (getTurnForYear(1300) <= iGameTurn <= getTurnForYear(1600)): return
		
		if iGameTurn % utils.getTurns(15) != utils.getTurns(4): return
		
		lIndonesianContacts = [iPlayer for iPlayer in range(iNumPlayers) if pIndonesia.canContact(iPlayer) and gc.getPlayer(iPlayer).getStateReligion() == iIslam]
		if not lIndonesianContacts: 
			return
		
		lIndonesianCities = utils.getRegionCities([rIndonesia])
		lPotentialCities = [city for city in lIndonesianCities if not city.isHasReligion(iIslam)]
		
		iMaxCitiesMultiplier = 2
		if pIndonesia.getStateReligion() == iIslam: iMaxCitiesMultiplier = 5
		
		if len(lPotentialCities) * iMaxCitiesMultiplier >= len(lIndonesianCities):
			pSpreadCity = utils.getRandomEntry(lPotentialCities)
			if pSpreadCity:
				pSpreadCity.spreadReligion(iIslam)
		
## BUDDHISM

	def checkBuddhism(self, iGameTurn):
		if gc.getGame().isReligionFounded(iBuddhism): return
		
		if iGameTurn == getTurnForYear(-300) - 5 + utils.getTurns(data.iSeed % 10):
			self.foundReligion(self.selectHolyCity(tBuddhistTL, tBuddhistBR), iBuddhism)
		
## ORTHODOXY

	def checkChristianity(self, iGameTurn):
		if not gc.getGame().isReligionFounded(iJudaism): return
		if gc.getGame().isReligionFounded(iOrthodoxy): return
		
		iOffset = utils.getTurns(data.iSeed % 15)
		
		if iGameTurn == getTurnForYear(0) + iOffset:
			pHolyCity = gc.getGame().getHolyCity(iJudaism)
			
			if pHolyCity.getOwner() != utils.getHumanID() and gc.getGame().getSorenRandNum(2, "Holy city?") == 0:
				pChristianCity = pHolyCity
				self.foundReligion((pChristianCity.getX(), pChristianCity.getY()), iOrthodoxy)
				return

			lJewishCities = []
			for iPlayer in range(iNumTotalPlayersB):
				lJewishCities.extend([city for city in utils.getCityList(iPlayer) if city.isHasReligion(iJudaism) and city.getOwner() != utils.getHumanID()])
							
			if lJewishCities:
				pChristianCity = utils.getRandomEntry(lJewishCities)
				self.foundReligion((pChristianCity.getX(), pChristianCity.getY()), iOrthodoxy)
			
		
##BUDDHISM

	def foundBuddhism(self, city):
		gc.getPlayer(city.getOwner()).foundReligion(iBuddhism, iBuddhism, True)
		
		
## CATHOLICISM

	def checkSchism(self, iGameTurn):
		if not gc.getGame().isReligionFounded(iOrthodoxy): return
		if gc.getGame().isReligionFounded(iCatholicism): return
		
		if gc.getGame().countReligionLevels(iOrthodoxy) < 10: return
		
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
		
		lIndependentCities = []
		lIndependentCities.extend(lDifferentStateReligionCities)
		lIndependentCities.extend(lMinorCities)
				
		self.schism(pOrthodoxCapital, pCatholicCapital, lNoStateReligionCities, lIndependentCities)

	def schism(self, pOrthodoxCapital, pCatholicCapital, lReplace, lDistance):
		for city in lDistance:
			if stepDistance(city.getX(), city.getY(), pCatholicCapital.getX(), pCatholicCapital.getY()) <= stepDistance(city.getX(), city.getY(), pOrthodoxCapital.getX(), pOrthodoxCapital.getY()):
				lReplace.append(city)
				
		for city in lReplace:
			city.replaceReligion(iOrthodoxy, iCatholicism)
				
		if gc.getPlayer(utils.getHumanID()).getStateReligion() == iOrthodoxy and gc.getGame().getGameTurn() >= getTurnForYear(tBirth[utils.getHumanID()]):
			utils.popup(CyTranslator().getText("TXT_KEY_SCHISM_TITLE", ()), CyTranslator().getText("TXT_KEY_SCHISM_MESSAGE", (pCatholicCapital.getName(),)), ())
			
		for iPlayer in range(iNumPlayers):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isAlive() and pPlayer.getStateReligion() == iOrthodoxy:
				lConvertedCities = [city for city in lReplace if city.getOwner() == iPlayer]
				if 2 * len(lConvertedCities) >= gc.getPlayer(iPlayer).getNumCities():
					gc.getPlayer(iPlayer).setLastStateReligion(iCatholicism)

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

		if iTech == iAcademia:
			if gc.getPlayer(iPlayer).getStateReligion() == iCatholicism:
				if not gc.getGame().isReligionFounded(iProtestantism):
					gc.getPlayer(iPlayer).foundReligion(iProtestantism, iProtestantism, True)
					self.reformation()
					
		for iReligion in range(iNumReligions):
			self.checkLateReligionFounding(iReligion, iTech)
					
	def onBuildingBuilt(self, city, iPlayer, iBuilding):
		if iBuilding == iHinduTemple:
			if gc.getGame().isReligionFounded(iBuddhism): return
			self.foundBuddhism(city)
			
		if iBuilding == iOrthodoxCathedral:
			if gc.getGame().isReligionFounded(iCatholicism): return
		
			pOrthodoxHolyCity = gc.getGame().getHolyCity(iOrthodoxy)
		
			if pOrthodoxHolyCity.getOwner() != iPlayer:
				self.foundReligion((city.getX(), city.getY()), iCatholicism)
				pCatholicHolyCity = gc.getGame().getHolyCity(iCatholicism)
				self.schism(pOrthodoxHolyCity, pCatholicHolyCity, [], [city for city in utils.getAllCities() if city.isHasReligion(iOrthodoxy) and city.getOwner() != pOrthodoxHolyCity.getOwner()])
				
					
	def chooseProtestantism(self, iCiv):
		iRand = gc.getGame().getSorenRandNum(100, 'Protestantism Choice')
		return iRand >= getCatholicPreference(iCiv)
		
	def isProtestantAnyway(self, iCiv):
		iRand = gc.getGame().getSorenRandNum(100, 'Protestantism anyway')
		return iRand >= (getCatholicPreference(iCiv)+50)/2

	def reformation(self):				
		for iPlayer in range(iNumPlayers):
			if [city for city in utils.getCityList(iPlayer) if city.getOwner() == iPlayer]:
				self.reformationChoice(iPlayer)
				
		for iPlayer in range(iNumPlayers):
			if data.players[iPlayer].iReformationDecision == 2:
				for iTargetPlayer in range(iNumPlayers):
					if data.players[iTargetPlayer].iReformationDecision == 0 and utils.getHumanID() != iTargetPlayer and iTargetPlayer != iNetherlands and not utils.isAVassal(iTargetPlayer):
						gc.getTeam(iPlayer).declareWar(iTargetPlayer, True, WarPlanTypes.WARPLAN_DOGPILE)
						
		pHolyCity = gc.getGame().getHolyCity(iProtestantism)
		if data.players[pHolyCity.getOwner()].iReformationDecision == 0:
			pHolyCity.setNumRealBuilding(iProtestantShrine, 1)
		
	def reformationChoice(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		
		if utils.getHumanID() == iPlayer: return
	
		if pPlayer.getStateReligion() == iCatholicism:
			if self.chooseProtestantism(iPlayer):
				self.embraceReformation(iPlayer)
			elif self.isProtestantAnyway(iPlayer) or utils.isAVassal(iPlayer):
				self.tolerateReformation(iPlayer)
			else:
				self.counterReformation(iPlayer)
		else:
			self.tolerateReformation(iPlayer)
					
	def embraceReformation(self, iCiv):
		iNumCatholicCities = 0
		for city in utils.getCityList(iCiv):
			if city.isHasReligion(iCatholicism):
				iNumCatholicCities += 1
				
				if city.getPopulation() >= 8 and not self.chooseProtestantism(iCiv):
					city.spreadReligion(iProtestantism)
				else:
					city.replaceReligion(iCatholicism, iProtestantism)
				
		pPlayer = gc.getPlayer(iCiv)
		pPlayer.changeGold(iNumCatholicCities * utils.getTurns(100))
		
		pPlayer.setLastStateReligion(iProtestantism)
		pPlayer.setConversionTimer(10)
		
		if iCiv < iNumPlayers:
			data.players[iCiv].iReformationDecision = 0
		
	def tolerateReformation(self, iCiv):
		for city in utils.getCityList(iCiv):
			if city.isHasReligion(iCatholicism):
				if self.isProtestantAnyway(iCiv):
					if city.getPopulation() <= 8 and not city.isHolyCityByType(iCatholicism):
						city.replaceReligion(iCatholicism, iProtestantism)
					else:
						city.spreadReligion(iProtestantism)

		if iCiv < iNumPlayers:
			data.players[iCiv].iReformationDecision = 1
					
	def counterReformation(self, iCiv):
		for city in utils.getCityList(iCiv):
			if city.isHasReligion(iCatholicism):
				if self.chooseProtestantism(iCiv):
					if city.getPopulation() >= 8:
						city.spreadReligion(iProtestantism)
		
		if iCiv < iNumPlayers:
			data.players[iCiv].iReformationDecision = 2
		

	def reformationyes(self, iCiv): # Unused
		for city in utils.getCityList(iCiv):
			city.replaceReligion(iCatholicism, iProtestantism)
			
			if city.getPopulation() > 7:
				iRand = gc.getGame().getSorenRandNum(100, "Reformation residual")
				if iRand <= lReformationMatrix[iCiv]:
					city.setHasReligion(iCatholicism, True, False, False)

		pPlayer = gc.getPlayer(iCiv)
		pPlayer.changeGold(500)
		if pPlayer.getStateReligion() == iCatholicism:
			pPlayer.setLastStateReligion(0)

	def reformationno(self, iCiv): # Unused
		cityList = utils.getCityList(iCiv)
		for city in cityList:
			if city.isHasReligion(iCatholicism):
				rndnum = gc.getGame().getSorenRandNum(100, 'ReformationAnyway')
				if rndnum >= lReformationMatrix[iCiv]:
					city.setHasReligion(iProtestantism, True, False, False)
