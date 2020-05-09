# Rhye's and Fall of Civilization - Religions management

from CvPythonExtensions import *
import CvUtil
import PyHelpers       
import Popup
#import cPickle as pickle     	
from Consts import *
import CvTranslator
from RFCUtils import *
from StoredData import data #edead

from Core import *

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

dCatholicPreference = CivDict({
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
iNetherlands: 10,
iPoland		: 80,
iPortugal	: 95,
iItaly		: 90,
iCongo		: 80,
iGermany	: 25,
iAmerica	: 20,
}, 50)

def getCatholicPreference(iPlayer):
	return dCatholicPreference[iPlayer]
	

@handler("religionFounded")
def onReligionFounded(iReligion):
	if turn() == scenarioStartTurn(): return

	if iReligion == iCatholicism:
		setStateReligionBeforeBirth(lCatholicStart, iCatholicism)
		setStateReligionBeforeBirth(lProtestantStart, iCatholicism)
		
	elif iReligion == iProtestantism:
		setStateReligionBeforeBirth(lProtestantStart, iProtestantism)


@handler("buildingBuilt")	
def onBuildingBuilt(city, iBuilding):
	iPlayer = city.getOwner()

	if iBuilding == iHinduTemple:
		if game.isReligionFounded(iBuddhism): return
		rel.foundBuddhism(city)
		
	if iBuilding == iOrthodoxCathedral:
		if game.isReligionFounded(iCatholicism): return
	
		pOrthodoxHolyCity = game.getHolyCity(iOrthodoxy)
	
		if pOrthodoxHolyCity.getOwner() != iPlayer:
			rel.foundReligion(location(city), iCatholicism)
			pCatholicHolyCity = game.getHolyCity(iCatholicism)
			rel.schism(pOrthodoxHolyCity, pCatholicHolyCity, cities.none(), cities.all().notowner(pOrthodoxHolyCity.getOwner()).religion(iOrthodoxy))
				


class Religions:

#######################################
### Main methods (Event-Triggered) ###
#####################################
		
	def checkTurn(self, iGameTurn):
	
		if not player(iIndia).isHuman():
			if iGameTurn == year(-2000)+1:
				if not game.isReligionFounded(iHinduism):
					if plot(92, 39).isCity():
						self.foundReligion((92, 39), iHinduism)
				
		self.checkJudaism(iGameTurn)
		
		#self.checkBuddhism(iGameTurn)

		self.checkChristianity(iGameTurn)
						
		self.checkSchism(iGameTurn)

		self.spreadJudaismEurope(iGameTurn)
		self.spreadJudaismMiddleEast(iGameTurn)
		self.spreadJudaismAmerica(iGameTurn)
		
		self.spreadIslamIndonesia(iGameTurn)


	def foundReligion(self, location, iReligion):
		plot = plot_(location)
		if plot.isCity():
			game.setHolyCity(iReligion, plot.getPlotCity(), True)
			return True
			
		return False
		

		
	def getTargetCities(self, lCities, iReligion):
		return [city for city in lCities if not city.isHasReligion(iReligion) and player(city).getSpreadType(city.plot(), iReligion) > ReligionSpreadTypes.RELIGION_SPREAD_NONE]
		
	def selectHolyCity(self, tTL, tBR, tPreferredCity = None, bAIOnly = True):
		preferredCity = city(tPreferredCity)
		if preferredCity and (not bAIOnly or preferredCity.isHuman()):
			return preferredCity
					
		holyCity = cities.rectangle(tTL, tBR).where(lambda city: not bAIOnly or not city.isHuman()).random()
		if holyCity:
			return location(holyCity)
			
		return None
		
	def checkLateReligionFounding(self, iReligion, iTech):
		if infos.religion(iReligion).getTechPrereq() != iTech:
			return
			
		if game.isReligionFounded(iReligion):
			return
		
		iPlayerCount = 0
		iPrereqCount = 0
		for iPlayer in players.major().alive():
			iPlayerCount += 1
			if team(iPlayer).isHasTech(iTech):
				iPrereqCount += 1
					
		if 2 * iPrereqCount >= iPlayerCount:
			self.foundReligionInCore(iReligion)
			
	def foundReligionInCore(self, iReligion):
		city = cities.all().where(lambda c: c.plot().getSpreadFactor(iReligion) == RegionSpreadTypes.REGION_SPREAD_CORE).random()
		if city:
			self.foundReligion(location(city), iReligion)
					
## JUDAISM

	def checkJudaism(self, iGameTurn):
		if game.isReligionFounded(iJudaism): return

		if iGameTurn == year(-1500) - turns(data.iSeed % 5):
			self.foundReligion(self.selectHolyCity(tJewishTL, tJewishBR, tJerusalem), iJudaism)
			
	def spreadJudaismEurope(self, iGameTurn):
		self.spreadReligionToRegion(iJudaism, [rIberia, rEurope, rItaly, rBritain, rRussia, rBalkans], iGameTurn, 1000, 10, 0)
				
	def spreadJudaismMiddleEast(self, iGameTurn):
		self.spreadReligionToRegion(iJudaism, [rMesopotamia, rAnatolia, rEgypt], iGameTurn, 600, 20, 5)
		
	def spreadJudaismAmerica(self, iGameTurn):
		self.spreadReligionToRegion(iJudaism, [rCanada, rAlaska, rUnitedStates], iGameTurn, 1850, 10, 4)
				
	def spreadReligionToRegion(self, iReligion, lRegions, iGameTurn, iStartDate, iInterval, iOffset):
		if not game.isReligionFounded(iReligion): return
		if iGameTurn < year(iStartDate): return
		
		if iGameTurn % turns(iInterval) != iOffset: return
		
		regionCities = cities.regions(*lRegions)
		religionCities = regionCities.religion(iReligion)
		
		if 2 * len(religionCities) < len(regionCities):
			spreadCity = regionCities.where(lambda city: not city.isHasReligion(iReligion) and player(city.getOwner()).getSpreadType(plot(city), iReligion) > ReligionSpreadTypes.RELIGION_SPREAD_NONE).random()
			if spreadCity:
				spreadCity.spreadReligion(iReligion)
				
## ISLAM

	def spreadIslamIndonesia(self, iGameTurn):
		if not game.isReligionFounded(iIslam): return
		if not player(iIndonesia).isAlive(): return
		if not turn(iGameTurn).between(1300, 1600): return
		
		if iGameTurn % turns(15) != turns(4): return
		
		indonesianContacts = players.major().where(lambda p: player(iIndonesia).canContact(p) and player(p).getStateReligion() == iIslam)
		if not indonesianContacts:
			return
			
		indonesianCities = cities.region(rIndonesia)
		potentialCities = indonesianCities.where(lambda c: not c.isHasReligion(iIslam))
		
		iMaxCitiesMultiplier = 2
		if player(iIndonesia).getStateReligion() == iIslam: iMaxCitiesMultiplier = 5
		
		if len(potentialCities) * iMaxCitiesMultiplier >= len(indonesianCities):
			spreadCity = potentialCities.random()
			if spreadCity:
				spreadCity.spreadReligion(iIslam)
		
## BUDDHISM

	def checkBuddhism(self, iGameTurn):
		if game.isReligionFounded(iBuddhism): return
		
		if iGameTurn == year(-300).deviate(5, data.iSeed):
			self.foundReligion(self.selectHolyCity(tBuddhistTL, tBuddhistBR), iBuddhism)
		
## ORTHODOXY

	def checkChristianity(self, iGameTurn):
		if not game.isReligionFounded(iJudaism): return
		if game.isReligionFounded(iOrthodoxy): return
		
		iOffset = turns(data.iSeed % 15)
		
		if iGameTurn == year(0) + iOffset:
			holyCity = game.getHolyCity(iJudaism)
			
			if not holyCity.isHuman() and rand(2) == 0:
				self.foundReligion(holyCity, iOrthodoxy)
				return
				
			jewishCity = cities.all().notowner(human()).where(lambda city: city.isHasReligion(iJudaism)).random()
			if jewishCity:
				self.foundReligion(location(jewishCity), iOrthodoxy)
			
		
##BUDDHISM

	def foundBuddhism(self, city):
		player(city).foundReligion(iBuddhism, iBuddhism, True)
		
		
## CATHOLICISM

	def checkSchism(self, iGameTurn):
		if not game.isReligionFounded(iOrthodoxy): return
		if game.isReligionFounded(iCatholicism): return
		
		if game.countReligionLevels(iOrthodoxy) < 10: return
		
		religionCities = cities.all().religion(iOrthodoxy)
		majorCities, minorCities = religionCities.split(is_minor)
		
		stateReligionCities, noStateReligionCities, differentStateReligionCities = majorCities.buckets(lambda city: player(city).getStateReligion() == iOrthodoxy, lambda city: player(city).getStateReligion() == -1)
		
		if not stateReligionCities: return
		if not noStateReligionCities and not minorCities: return
		
		if stateReligionCities >= noStateReligionCities + minorCities: return
		
		orthodoxCapital = stateReligionCities.where(lambda city: city.isCapital())
		if not orthodoxCapital:
			orthodoxCapital = game.getHolyCity(iOrthodoxy)
			
		catholicCities = (noStateReligionCities + minorCities).without(orthodoxCapital)
		catholicCapital = catholicCities.where(lambda city: plot(city).getSpreadFactor(iCatholicism) >= 3).maximum(lambda city: city.getPopulation())
		if not catholicCapital:
			catholicCapital = catholicCities.maximum(lambda city: city.getPopulation())
		
		self.foundReligion(catholicCapital, iCatholicism)
		
		independentCities = differentStateReligionCities + minorCities
				
		self.schism(orthodoxCapital, catholicCapital, noStateReligionCities, independentCities)

	def schism(self, orthodoxCapital, catholicCapital, replace, distance):
		replace += distance.where(lambda city: distance(city, catholicCapital) <= distance(city, orthodoxCapital))
		for city in replace:
			city.replaceReligion(iOrthodoxy, iCatholicism)
				
		if player().getStateReligion() == iOrthodoxy and year() >= year(dBirth[active()]):
			popup(-1, text("TXT_KEY_SCHISM_TITLE"), text("TXT_KEY_SCHISM_MESSAGE", pCatholicCapital.getName()), ())
			
		for iPlayer in players.major().alive().where(lambda p: player(p).getStateReligion() == iOrthodoxy):
			if 2 * replace.owner(iPlayer) >= player(iPlayer).getNumCities():
				player(iPlayer).setLastStateReligion(iCatholicism)

#REFORMATION

	def eventApply7624(self, popupReturn):
		if popupReturn.getButtonClicked() == 0:
			self.embraceReformation(active())
		elif popupReturn.getButtonClicked() == 1:
			self.tolerateReformation(active())
		elif popupReturn.getButtonClicked() == 2:
			self.counterReformation(active())

	def onTechAcquired(self, iTech, iPlayer):
		if scenario() == i1700AD:
			return

		if iTech == iAcademia:
			if player(iPlayer).getStateReligion() == iCatholicism:
				if not game.isReligionFounded(iProtestantism):
					player(iPlayer).foundReligion(iProtestantism, iProtestantism, True)
					self.reformation()
					
		for iReligion in range(iNumReligions):
			self.checkLateReligionFounding(iReligion, iTech)
					
	def chooseProtestantism(self, iPlayer):
		return rand(100) >= getCatholicPreference(iPlayer)
		
	def isProtestantAnyway(self, iPlayer):
		return rand(100) >= (getCatholicPreference(iPlayer)+50)/2

	def reformation(self):				
		for iPlayer in players.major():
			self.reformationChoice(iPlayer)
				
		for iPlayer in players.major():
			if data.players[iPlayer].iReformationDecision == 2:
				for iTargetPlayer in players.major():
					if data.players[iTargetPlayer].iReformationDecision == 0 and not player(iTargetPlayer).isHuman() and civ(iTargetPlayer) != iNetherlands and not team(iTargetPlayer).isAVassal():
						team(iPlayer).declareWar(iTargetPlayer, True, WarPlanTypes.WARPLAN_DOGPILE)
						
		pHolyCity = game.getHolyCity(iProtestantism)
		if data.players[pHolyCity.getOwner()].iReformationDecision == 0:
			pHolyCity.setNumRealBuilding(iProtestantShrine, 1)
		
	def reformationChoice(self, iPlayer):
		pPlayer = player(iPlayer)
		
		if player(iPlayer).isHuman(): return
	
		if pPlayer.getStateReligion() == iCatholicism:
			if self.chooseProtestantism(iPlayer):
				self.embraceReformation(iPlayer)
			elif self.isProtestantAnyway(iPlayer) or team(iPlayer).isAVassal():
				self.tolerateReformation(iPlayer)
			else:
				self.counterReformation(iPlayer)
		else:
			self.tolerateReformation(iPlayer)
					
	def embraceReformation(self, iPlayer):
		iNumCatholicCities = 0
		for city in cities.owner(iPlayer).religion(iCatholicism):
			iNumCatholicCities += 1
			
			if city.getPopulation() >= 8 and not self.chooseProtestantism(iPlayer):
				city.spreadReligion(iProtestantism)
			else:
				city.replaceReligion(iCatholicism, iProtestantism)
				
		pPlayer = player(iPlayer)
		pPlayer.changeGold(iNumCatholicCities * turns(100))
		
		pPlayer.setLastStateReligion(iProtestantism)
		pPlayer.setConversionTimer(10)
		
		if not is_minor(iPlayer):
			data.players[iPlayer].iReformationDecision = 0
		
	def tolerateReformation(self, iPlayer):
		for city in cities.owner(iPlayer).religion(iCatholicism):
			if self.isProtestantAnyway(iPlayer):
				if city.getPopulation() <= 8 and not city.isHolyCityByType(iCatholicism):
					city.replaceReligion(iCatholicism, iProtestantism)
				else:
					city.spreadReligion(iProtestantism)

		if not is_minor(iPlayer):
			data.players[iPlayer].iReformationDecision = 1
					
	def counterReformation(self, iPlayer):
		for city in cities.owner(iPlayer).religion(iCatholicism):
			if self.chooseProtestantism(iPlayer):
				if city.getPopulation() >= 8:
					city.spreadReligion(iProtestantism)
		
		if not is_minor(iPlayer):
			data.players[iPlayer].iReformationDecision = 2
					
rel = Religions()