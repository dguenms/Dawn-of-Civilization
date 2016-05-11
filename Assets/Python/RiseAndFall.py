# Rhye's and Fall of Civilization - Main Scenario

from CvPythonExtensions import *
import CvUtil
from PyHelpers import PyPlayer
import Popup
#import cPickle as pickle
from StoredData import sd # edead
import CvTranslator
import RFCUtils
from Consts import *
import CityNameManager as cnm
import Victory as vic
import DynamicCivs as dc
from operator import itemgetter
import Stability as sta
import Areas
import Civilizations

################
### Globals ###
##############

gc = CyGlobalContext()
utils = RFCUtils.RFCUtils()

iCheatersPeriod = 12
iBetrayalPeriod = 8
iBetrayalThreshold = 80
iRebellionDelay = 15
iEscapePeriod = 30

class RiseAndFall:

##################################################
### Secure storage & retrieval of script data ###
################################################
	

	def getNewCiv( self ):
		return sd.scriptDict['lNewCiv'].pop()

	def setNewCiv( self, iNewValue ):
		sd.scriptDict['lNewCiv'].append(iNewValue)
		
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
		
	def setTempPlots(self, lPlots):
		sd.scriptDict['lTempPlots'] = lPlots
		
	def getTempPlots(self):
		return sd.scriptDict['lTempPlots']

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
		sd.scriptDict['lPlayerEnabled'][lSecondaryCivs.index(iCiv)] = bNewValue
		if bNewValue == False and utils.getHumanID() != iCiv: gc.getPlayer(iCiv).setPlayable(False)
		
	def getPlayerEnabled(self, iCiv):
		return sd.scriptDict['lPlayerEnabled'][lSecondaryCivs.index(iCiv)]
		
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
		iNewCiv = self.getNewCiv()
		if( popupReturn.getButtonClicked() == 0 ): # 1st button
			self.handleNewCiv(iNewCiv)
			
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
		for iMaster in range(iNumPlayers):
			if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iMaster)):
				gc.getTeam(gc.getPlayer(iCiv).getTeam()).setVassal(iMaster, False, False)
		self.setAlreadySwitched(True)
		gc.getPlayer(iCiv).setPlayable(True)
		
		sd.resetHumanStability()

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

	def flipPopup(self, iNewCiv, lPlots):
		iHuman = utils.getHumanID()
		
		flipText = CyTranslator().getText("TXT_KEY_FLIPMESSAGE1", ())
		
		for city in self.getConvertedCities(iNewCiv, lPlots):
			flipText += city.getName() + "\n"
			
		flipText += CyTranslator().getText("TXT_KEY_FLIPMESSAGE2", ())
							
		self.showPopup(7615, CyTranslator().getText("TXT_KEY_NEWCIV_TITLE", ()), flipText, (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_NO", ())))
		self.setNewCivFlip(iNewCiv)
		self.setOldCivFlip(iHuman)
		self.setTempPlots(lPlots)

	def eventApply7615(self, popupReturn):
		iHuman = utils.getHumanID()
		lPlots = self.getTempPlots()
		iNewCivFlip = self.getNewCivFlip()
		
		iNumCities = gc.getPlayer(iNewCivFlip).getNumCities()

		humanCityList = [city for city in self.getConvertedCities(iNewCivFlip, lPlots) if city.getOwner() == iHuman]
		
		if( popupReturn.getButtonClicked() == 0 ): # 1st button
			print ("Flip agreed")
			CyInterface().addMessage(iHuman, True, iDuration, CyTranslator().getText("TXT_KEY_FLIP_AGREED", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
						
			if (len(humanCityList)):
				for i in range(len(humanCityList)):
					city = humanCityList[i]
					print ("flipping ", city.getName())
					utils.cultureManager((city.getX(),city.getY()), 100, iNewCivFlip, iHuman, False, False, False)
					utils.flipUnitsInCityBefore((city.getX(),city.getY()), iNewCivFlip, iHuman)
					self.setTempFlippingCity((city.getX(),city.getY()))
					utils.flipCity((city.getX(), city.getY()), 0, 0, iNewCivFlip, [iHuman])					
					utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCivFlip)
					
			if iNumCities == 0 and gc.getPlayer(iNewCivFlip).getNumCities() > 0:
				self.createStartingWorkers(iNewCivFlip, (gc.getPlayer(iNewCivFlip).getCapitalCity().getX(), gc.getPlayer(iNewCivFlip).getCapitalCity().getY()))

			#same code as Betrayal - done just once to make sure human player doesn't hold a stack just outside of the cities
			for (x, y) in lPlots:
				betrayalPlot = gc.getMap().plot(x,y)
				if betrayalPlot.isCore(betrayalPlot.getOwner()) and not betrayalPlot.isCore(iNewCivFlip): continue
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
			CyInterface().addMessage(iHuman, True, iDuration, CyTranslator().getText("TXT_KEY_FLIP_REFUSED", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
						

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
					
	#def eventApply7627(self, popupReturn):
	#	lReligionList, tCityPlot = utils.getTempEventList()
	#	x, y = tCityPlot
	#	city = gc.getMap().plot(x, y).getPlotCity()
	#	
	#	utils.debugTextPopup("lReligionList: "+str(lReligionList)+"\n Button clicked: "+str(popupReturn.getButtonClicked()))
	#	
	#	iPersecutedReligion = lReligionList[popupReturn.getButtonClicked()]
	#	
	#	utils.debugTextPopup("iPersecutedReligion: "+str(gc.getReligionInfo(iPersecutedReligion).getText()))
	#	
	#	city.setHasReligion(iPersecutedReligion, False, True, True)
	#	city.setHasRealBuilding(iTemple + 4*iPersecutedReligion, False)
	#	city.setHasRealBuilding(iMonastery + 4*iPersecutedReligion, False)
	#	city.setHasRealBuilding(iCathedral + 4*iPersecutedReligion, False)
	#	city.changeOccupationTimer(2)
	#	city.changeHurryAngerTimer(city.hurryAngerLength(0))
		
	#	CyInterface().addMessage(city.getOwner(), True, iDuration, CyTranslator().getText("TXT_KEY_PERSECUTION_PERFORMED", (gc.getReligionInfo(iPersecutedReligion).getText(), city.getName())), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
		
	def eventApply7629(self, netUserData, popupReturn):
		targetList = sd.getByzantineBribes()
		iButton = popupReturn.getButtonClicked()
		
		if iButton >= len(targetList): return
		
		unit, iCost = targetList[iButton]
		closestCity = gc.getMap().findCity(unit.getX(), unit.getY(), iByzantium, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
		
		newUnit = utils.makeUnit(unit.getUnitType(), iByzantium, (closestCity.plot().getX(), closestCity.plot().getY()), 1)
		gc.getPlayer(iByzantium).changeGold(-iCost)
		unit.kill(False, iByzantium)
		CyInterface().selectUnit(newUnit, True, True, False)

#######################################
### Main methods (Event-Triggered) ###
#####################################  

	def setup(self):	    

		self.determineEnabledPlayers()
		
		self.initScenario()
		
		# Leoreth: make sure to select the Egyptian settler
		if (pEgypt.isHuman()):
			x, y = Areas.getCapital(iEgypt)
			plotEgypt = gc.getMap().plot(x, y)  
			for i in range(plotEgypt.getNumUnits()):
				unit = plotEgypt.getUnit(i)
				if unit.getUnitType() == iSettler:
					CyInterface().selectUnit(unit, True, False, False)
					break
					
	def initScenario(self):
	
		self.updateStartingPlots()
	
		self.adjustCityCulture()
		
		self.updateGreatWall()
			
		self.foundCapitals()
		self.flipStartingTerritory()
		
		self.initStartingReligions()
	
		if utils.getScenario() == i3000BC:
			self.create4000BCstartingUnits()
			
		if utils.getScenario() == i600AD:
			Civilizations.initScenarioTechs(i600AD)
			self.create600ADstartingUnits()
#			self.assign600ADGold()
			
		if utils.getScenario() == i1700AD:
			Civilizations.initScenarioTechs(i1700AD)
			self.create1700ADstartingUnits()
#			self.assign1700ADGold()
			self.init1700ADDiplomacy()
			self.prepareColonists()
			self.adjust1700ADCulture()
			
			for iPlayer in [iIndia, iPersia, iSpain, iHolyRome, iTurkey]:
				utils.setReborn(iPlayer, True)
			
			pChina.updateTradeRoutes()
		
#		self.assign3000BCGold()	
		self.invalidateUHVs()
		
		gc.getGame().setVoteSourceReligion(1, iCatholicism, False)
		
	def updateStartingPlots(self):
		for iPlayer in range(iNumPlayers):
			x, y = Areas.getCapital(iPlayer)
			gc.getPlayer(iPlayer).setStartingPlot(gc.getMap().plot(x, y), False)
		
	def adjustCityCulture(self):
		if utils.getTurns(10) == 10: return
	
		lCities = []
		for iPlayer in range(iNumTotalPlayersB):
			lCities.extend(utils.getCityList(iPlayer))
			
		for city in lCities:
			city.setCulture(city.getOwner(), utils.getTurns(city.getCulture(city.getOwner())), True)
			
	def updateGreatWall(self):
		if utils.getScenario() == i3000BC:
			return
	
		elif utils.getScenario() == i600AD:
			tTL = (98, 39)
			tBR = (107, 48)
			lExceptions = [(105, 48), (106, 48), (107, 48), (106, 47), (98, 46), (98, 47), (99, 47), (98, 48), (99, 48), (98, 39), (99, 39), (100, 39), (98, 40), (99, 40), (98, 41), (99, 41), (98, 42), (100, 40)]
			lAdditions = [(103, 38), (104, 37), (102, 49), (103, 49)]
				
		elif utils.getScenario() == i1700AD:
			tTL = (98, 40)
			tBR = (106, 50)
			lExceptions = [(98, 46), (98, 47), (98, 48), (98, 49), (99, 49), (98, 50), (99, 50), (100, 50), (99, 47), (99, 48), (100, 49), (101, 49), (101, 50), (102, 50)]
			lAdditions = [(104, 51), (105, 51), (106, 51), (107, 41), (107, 42), (107, 43), (103, 38), (103, 39), (104, 39), (105, 39), (104, 37)]
			
			lRemoveWall = [(97, 40), (98, 39), (99, 39), (100, 39), (101, 39), (102, 39)]
			
			for tPlot in lRemoveWall:
				x, y = tPlot
				gc.getMap().plot(x, y).setOwner(-1)
				
			gc.getMap().plot(102, 47).getPlotCity().updateGreatWall()
			
			for tPlot in lRemoveWall:
				x, y = tPlot
				gc.getMap().plot(x, y).setOwner(iChina)
			
		for x in range(tTL[0], tBR[0]+1):
			for y in range(tTL[1], tBR[1]+1):
				if (x, y) not in lExceptions:
					plot = gc.getMap().plot(x, y)
					if not plot.isWater(): plot.setWithinGreatWall(True)
					
		for (x, y) in lAdditions:
			plot = gc.getMap().plot(x, y)
			if not plot.isWater(): plot.setWithinGreatWall(True)
			
			
	def adjust1700ADCulture(self):
		for x in range(124):
			for y in range(68):
				plot = gc.getMap().plot(x, y)
				if plot.getOwner() != -1:
					utils.convertPlotCulture(plot, plot.getOwner(), 100, True)
					
#		for x, y in [(48, 45), (50, 44), (50, 43), (50, 42), (49, 40)]:
#			utils.convertPlotCulture(gc.getMap().plot(x, y), iPortugal, 100, True)
			
#		for x, y in [(58, 49), (59, 49), (60, 49)]:
#			utils.convertPlotCulture(gc.getMap().plot(x, y), iGermany, 100, True)
			
#		for x, y in [(62, 51)]:
#			utils.convertPlotCulture(gc.getMap().plot(x, y), iHolyRome, 100, True)
			
#		for x, y in [(58, 52), (58, 53)]:
#			utils.convertPlotCulture(gc.getMap().plot(x, y), iNetherlands, 100, True)
			
#		for x, y in [(64, 53), (66, 55)]:
#			utils.convertPlotCulture(gc.getMap().plot(x, y), iPoland, 100, True)
			
#		for x, y in [(67, 58), (68, 59), (69, 56), (69, 54)]:
#			utils.convertPlotCulture(gc.getMap().plot(x, y), iRussia, 100, True)
			
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
		for iPlayer in range(iNumTotalPlayers):
			gc.getPlayer(iPlayer).changeGold(utils.getTurns(tStartingGold[iPlayer]))
			
	def assign600ADGold(self):
		for iPlayer in dExtraGold600AD:
			gc.getPlayer(iPlayer).changeGold(utils.getTurns(dExtraGold600AD[iPlayer]))
		
	def assign1700ADGold(self):
		for iPlayer in dExtraGold1700AD:
			gc.getPlayer(iPlayer).changeGold(utils.getTurns(dExtraGold1700AD[iPlayer]))
		
	def init1700ADDiplomacy(self):	
#		self.changeAttitudeExtra(iIndia, iMughals, -2)
#		self.changeAttitudeExtra(iPersia, iTurkey, -4)
#		self.changeAttitudeExtra(iPersia, iMughals, -2)
#		self.changeAttitudeExtra(iChina, iKorea, 2)
#		self.changeAttitudeExtra(iVikings, iRussia, -2)
#		self.changeAttitudeExtra(iVikings, iTurkey, -2)
#		self.changeAttitudeExtra(iSpain, iPortugal, 2)
#		self.changeAttitudeExtra(iFrance, iEngland, -4)
#		self.changeAttitudeExtra(iFrance, iNetherlands, 2)
#		self.changeAttitudeExtra(iFrance, iTurkey, -2)
#		self.changeAttitudeExtra(iEngland, iPortugal, 2)
#		self.changeAttitudeExtra(iEngland, iMughals, -2)
#		self.changeAttitudeExtra(iEngland, iTurkey, -2)
#		self.changeAttitudeExtra(iHolyRome, iTurkey, -4)
#		self.changeAttitudeExtra(iRussia, iTurkey, -4)
#		self.changeAttitudeExtra(iPortugal, iNetherlands, -2)
#		self.changeAttitudeExtra(iNetherlands, iTurkey, -2)
		
		teamEngland.declareWar(iMughals, False, WarPlanTypes.WARPLAN_LIMITED)
		teamIndia.declareWar(iMughals, False, WarPlanTypes.WARPLAN_TOTAL)
	
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
		for iPlayer in range(iNumPlayers):
			if not gc.getPlayer(iPlayer).isPlayable():
				for i in range(3):
					utils.setGoal(iPlayer, i, 0)
					
	def foundCapitals(self):	
		if utils.getScenario() == i600AD:
		
			# Byzantium
#			tCapital = Areas.getCapital(iByzantium)
#			lBuildings = [iWalls, iCastle, iBarracks, iStable, iGranary, iLibrary, iMarket, \
#				      iOrthodoxTemple, iByzantineHippodrome, iHagiaSophia, iTheodosianWalls]
#			city = utils.foundCapital(iByzantium, tCapital, 'Konstantinoupolis', 4, 250, lBuildings, [iJudaism, iCatholicism, iOrthodoxy])
			
			# China
			self.prepareChina()
			tCapital = Areas.getCapital(iChina)
			lBuildings = [iConfucianTemple, iChineseTaixue, iBarracks, iForge]
			utils.foundCapital(iChina, tCapital, "Xi'an", 4, 100, lBuildings, [iConfucianism, iTaoism])
			
		if utils.getScenario() == i1700AD:
			
			# London
#			x, y = Areas.getCapital(iEngland)
#			pLondon = gc.getMap().plot(x, y).getPlotCity()
#			pLondon.setFreeSpecialistCount(iSpecialistGreatMerchant, 1)
			
			# Paris
#			x, y = Areas.getCapital(iFrance)
#			pParis = gc.getMap().plot(x, y).getPlotCity()
#			pParis.setFreeSpecialistCount(iSpecialistGreatScientist, 1)
			
			# Netherlands
#			x, y = Areas.getCapital(iNetherlands)
#			pAmsterdam = gc.getMap().plot(x, y).getPlotCity()
#			pAmsterdam.setFreeSpecialistCount(iSpecialistGreatMerchant, 2)
			
			# Hamburg
#			x, y = tHamburg
#			pHamburg = gc.getMap().plot(x, y).getPlotCity()
#			pHamburg.setFreeSpecialistCount(iSpecialistGreatMerchant, 1)
#			pHamburg.setCulture(iNetherlands, 0, True)
#			gc.getMap().plot(x, y).setCulture(iNetherlands, 0, True)
			
			# Milan
#			x, y = tMilan
#			pMilan = gc.getMap().plot(x, y).getPlotCity()
#			pMilan.setFreeSpecialistCount(iSpecialistGreatMerchant, 2)
#			pMilan.setFreeSpecialistCount(iSpecialistGreatEngineer, 1)
			
			# Kyoto
#			x, y = Areas.getCapital(iJapan)
#			pKyoto = gc.getMap().plot(x, y).getPlotCity()
#			pKyoto.setFreeSpecialistCount(iSpecialistGreatMerchant, 1)
			
			# Mecca
#			pMecca = gc.getGame().getHolyCity(iIslam)
#			pMecca.setFreeSpecialistCount(iSpecialistGreatProphet, 2)
			
			# Rome
#			x, y = Areas.getCapital(iRome)
#			pRome = gc.getMap().plot(x, y).getPlotCity()
#			pRome.setFreeSpecialistCount(iSpecialistGreatProphet, 1)
			
			# Baghdad
#			x, y = tBaghdad
#			pBaghdad = gc.getMap().plot(x, y).getPlotCity()
#			pBaghdad.setFreeSpecialistCount(iSpecialistGreatProphet, 1)
			
			# Pataliputra
#			pPataliputra = gc.getGame().getHolyCity(iHinduism)
#			pPataliputra.setFreeSpecialistCount(iSpecialistGreatProphet, 2)
			
			# Lhasa
#			x, y = Areas.getCapital(iTibet)
#			pLhasa = gc.getMap().plot(x, y).getPlotCity()
#			pLhasa.setFreeSpecialistCount(iSpecialistGreatProphet, 2)
			
			# Ayutthaya
#			x, y = Areas.getCapital(iThailand)
#			pAyutthaya = gc.getMap().plot(x, y).getPlotCity()
#			pAyutthaya.setFreeSpecialistCount(iSpecialistGreatProphet, 1)
			
			# Chengdu
			pChengdu = gc.getMap().plot(99, 41).getPlotCity()
			pChengdu.setCulture(iChina, 100, True)
			
			# Mumbai
#			pMumbai = gc.getMap().plot(88, 34).getPlotCity()
#			pMumbai.setFreeSpecialistCount(iSpecialistGreatGeneral, 1)
			
	def flipStartingTerritory(self):
	
		if utils.getScenario() == i600AD:
		
			# Byzantium
			tTL1 = (62, 37)
			tBR1 = (76, 45)
			tTL2 = (66, 34)
			tBR2 = (70, 37)
#			self.startingFlip(iByzantium, [(tTL1, tBR1), (tTL2, tBR2)])
			
			# China
			tTL, tBR = Areas.tBirthArea[iChina]
			if utils.getHumanID() != iChina: tTL = (99, 39) # 4 tiles further south
			self.startingFlip(iChina, [(tTL, tBR)])
			
		if utils.getScenario() == i1700AD:
		
			# China (Tibet)
			tTibetTL = (94, 42)
			tTibetBR = (97, 45)
			tManchuriaTL = (105, 51)
			tManchuriaBR = (109, 55)
			self.startingFlip(iChina, [(tTibetTL, tTibetBR), (tManchuriaTL, tManchuriaBR)])
			
			# Russia (Sankt Peterburg)
#			utils.convertPlotCulture(gc.getMap().plot(68, 58), iRussia, 100, True)
#			utils.convertPlotCulture(gc.getMap().plot(67, 57), iRussia, 100, True)
			
			
	def startingFlip(self, iPlayer, lRegionList):
	
		for tuple in lRegionList:
			tTL = tuple[0]
			tBR = tuple[1]
			tExceptions = ()
			if len(tuple) > 2: tExceptions = tuple[2]
			self.convertSurroundingCities(iPlayer, utils.getPlotList(tTL, tBR, tExceptions))
			self.convertSurroundingPlotCulture(iPlayer, utils.getPlotList(tTL, tBR, tExceptions))


	def prepareChina(self):
		pGuiyang = gc.getMap().plot(102, 41)
		pGuiyang.getPlotCity().kill()
		pGuiyang.setImprovementType(-1)
		pGuiyang.setRouteType(-1)
		pGuiyang.setFeatureType(iForest, 0)

		if utils.getScenario() == i600AD:
			pXian = gc.getMap().plot(100, 44)
			pXian.getPlotCity().kill()
			pXian.setImprovementType(-1)
			pXian.setRouteType(-1)
			pXian.setFeatureType(iForest, 0)
			
		if utils.getScenario() == i1700AD:
			pBeijing = gc.getMap().plot(tBeijing[0], tBeijing[1])
			pBeijing.getPlotCity().kill()
			pBeijing.setImprovementType(-1)
			pBeijing.setRouteType(-1)

		tCultureRegionTL = (98, 37)
		tCultureRegionBR = (109, 49)
		for x in range(tCultureRegionTL[0], tCultureRegionBR[0]+1):       
			for y in range(tCultureRegionTL[1], tCultureRegionBR[1]+1):     
				pCurrent = gc.getMap().plot(x, y)
				bCity = False
				for iX in range(x-1, x+2):	# from x-1 to x+1
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
		utils.makeUnit(iArcher, iIndependent, (99, 41), 1)
		pChengdu = gc.getMap().plot(99, 41).getPlotCity()
		pChengdu.setName("Chengdu", False)
		pChengdu.setPopulation(2)
		pChengdu.setHasReligion(iConfucianism, True, False, False)
		pChengdu.setHasRealBuilding(iGranary, True)
		
		if utils.getScenario() == i600AD:
			pBarbarian.found(105, 49)
			utils.makeUnit(iArcher, iBarbarian, (105, 49), 1)
			pShenyang = gc.getMap().plot(105, 49).getPlotCity()
			pShenyang.setName("Simiyan hoton", False)
			pShenyang.setPopulation(2)
			pShenyang.setHasReligion(iConfucianism, True, False, False)
			pShenyang.setHasRealBuilding(iGranary, True)
			pShenyang.setHasRealBuilding(iWalls, True)
			pShenyang.setHasRealBuilding(iConfucianTemple, True)

	def setupBirthTurnModifiers(self):
		for iCiv in range(iNumPlayers):
			if (iCiv >= iIndia and not gc.getPlayer(iCiv).isHuman()):
				self.setBirthTurnModifier(iCiv, (gc.getGame().getSorenRandNum(11, 'BirthTurnModifier') - 5)) # -5 to +5
		#now make sure that no civs spawn in the same turn and cause a double "new civ" popup
		for iCiv in range(iNumPlayers):
			if (iCiv > utils.getHumanID() and iCiv < iBrazil):
				for j in range(iNumPlayers-1-iCiv):
					iNextCiv = iCiv+j+1
					if (getTurnForYear(tBirth[iCiv])+self.getBirthTurnModifier(iCiv) == getTurnForYear(tBirth[iNextCiv])+self.getBirthTurnModifier(iNextCiv)):
						self.setBirthTurnModifier(iNextCiv, (self.getBirthTurnModifier(iNextCiv)+1))
						
	def placeGoodyHuts(self):
			
		if utils.getScenario() == i3000BC:
			self.placeHut((101, 38), (107, 41)) # Southern China
			self.placeHut((62, 45), (67, 50)) # Balkans
			self.placeHut((69, 42), (76, 46)) # Asia Minor
		
		if utils.getScenario() <= i600AD:
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
		
	def initStartingReligions(self):
	
		if utils.getScenario() == i600AD:
			utils.setStateReligionBeforeBirth(lCatholicStart, iCatholicism)
			utils.setStateReligionBeforeBirth(lProtestantStart, iCatholicism)
			
		if utils.getScenario() == i1700AD:
			utils.setStateReligionBeforeBirth(lCatholicStart, iCatholicism)
			utils.setStateReligionBeforeBirth(lProtestantStart, iProtestantism)
			
	def checkTurn(self, iGameTurn):
	
		# Leoreth: randomly place goody huts
		if iGameTurn == utils.getScenarioStartTurn()+3:
			self.placeGoodyHuts()
		
		if iGameTurn == getTurnForYear(tBirth[iSpain])-1:
			if utils.getScenario() == i600AD:
				pMassilia = gc.getMap().plot(56, 46)
				if pMassilia.isCity():
					pMassilia.getPlotCity().setCulture(pMassilia.getPlotCity().getOwner(), 1, True)

		#Leoreth: Turkey immediately flips Seljuk or independent cities in its core to avoid being pushed out of Anatolia
		if iGameTurn == sd.scriptDict['iOttomanSpawnTurn']+1:
			cityPlotList = utils.getAreaCities(Areas.getBirthArea(iTurkey))
			for city in cityPlotList:
				tPlot = (city.getX(), city.getY())
				iOwner = city.getOwner()
				if iOwner in [iBarbarian, iSeljuks, iIndependent, iIndependent2]:
			       		utils.flipCity(tPlot, False, True, iTurkey, ())
			       		utils.cultureManager(tPlot, 100, iTurkey, iOwner, True, False, False)
			       		self.convertSurroundingPlotCulture(iTurkey, utils.getPlotList((tPlot[0]-1,tPlot[1]-1), (tPlot[0]+1,tPlot[1]+1)))
					utils.makeUnit(iLongbowman, iTurkey, tPlot, 1)
					
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
			utils.makeUnit(iSettler, iCarthage, (58, 39), 1)
			utils.makeUnit(iArcher, iCarthage, (58, 39), 2)
			utils.makeUnit(iWorker, iCarthage, (58, 39), 2)
			utils.makeUnit(iPhoenicianAfricanWarElephant, iCarthage, (58, 39), 2)
			
		if iGameTurn == getTurnForYear(476):
			if pItaly.isHuman() and pRome.isAlive():
				sta.completeCollapse(iRome)
				
		if iGameTurn == getTurnForYear(-50):
			if pByzantium.isHuman() and pGreece.isAlive():
				sta.completeCollapse(iGreece)
			
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
				self.giveRaiders(iVikings, Areas.getBroaderArea(iVikings))
			       
		if (iGameTurn >= getTurnForYear(1350) and iGameTurn <= getTurnForYear(1918)):
			for iPlayer in [iSpain, iEngland, iFrance, iPortugal, iNetherlands, iVikings, iGermany]:
				if iGameTurn == self.getAstronomyTurn(iPlayer) + 1 + self.getColonistsAlreadyGiven(iPlayer)*8:
					self.giveColonists(iPlayer)
					
		if iGameTurn == getTurnForYear(710)-1:
			x, y = 51, 37
			if gc.getMap().plot(x,y).isCity():
				marrakesh = gc.getMap().plot(x,y).getPlotCity()
				marrakesh.setHasReligion(iIslam, True, False, False)
				
				utils.makeUnit(iSettler, marrakesh.getOwner(), (x,y), 1)
				utils.makeUnit(iWorker, marrakesh.getOwner(), (x,y), 1)
				
		# Leoreth: help human with Aztec UHV - prevent super London getting in the way
		if iGameTurn == getTurnForYear(1500) and utils.getHumanID() == iAztecs:
			x, y = Areas.getCapital(iEngland)
			plot = gc.getMap().plot(x, y)
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
			utils.makeUnitAI(iLongbowman, iSeljuks, tEsfahan, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iIslamicMissionary, iSeljuks, tEsfahan, 1)
			utils.makeUnit(iWorker, iSeljuks, tEsfahan, 3)
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
					utils.makeUnitAI(iLongbowman, iSeljuks, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
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
				iExtra = 0
				if gc.getMap().plot(tSpawnPlot[0], tSpawnPlot[1]).getPlotCity().getOwner() == iArabia and utils.getHumanID() != iArabia: iExtra = 1
				
				utils.makeUnitAI(iSeljukGhulamWarrior, iSeljuks, tSpawnPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3 + iExtra)
				utils.makeUnitAI(iTrebuchet, iSeljuks, tSpawnPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 + 2*iExtra)
				utils.makeUnitAI(iHeavySwordsman, iSeljuks, tSpawnPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 + iExtra)
				utils.makeUnitAI(iLongbowman, iSeljuks, tSpawnPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			
			for iPlayer in targetPlayerList:
				teamSeljuks.declareWar(iPlayer, True, WarPlanTypes.WARPLAN_TOTAL)
			if utils.getHumanID() in lCivGroups[2]:
				CyInterface().addMessage(CyGame().getActivePlayer(), True , iDuration, CyTranslator().getText("TXT_KEY_SELJUK_HORDES", ()), "", 1 , "", ColorTypes(iRed),0,0,False,False)

		if iGameTurn == getTurnForYear(1070 + utils.getSeed()%10 - 5): #Linkman226- Seljuks
			tSpawnPlots = ((77,41), (74, 43), (72, 44), (74, 39))
			for plot in tSpawnPlots:
				spawnPlot = utils.getFreePlot(plot[0], plot[1])
				utils.makeUnitAI(iSeljukGhulamWarrior, iSeljuks, spawnPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
				utils.makeUnitAI(iSeljukGhulamWarrior, iSeljuks, spawnPlot, UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, 3)
				utils.makeUnitAI(iTrebuchet, iSeljuks, spawnPlot, UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, 3)
				pSeljuks.setLastStateReligion(iIslam)
				teamSeljuks.declareWar(iByzantium, True, WarPlanTypes.WARPLAN_TOTAL)
				teamSeljuks.declareWar(iArabia, True, WarPlanTypes.WARPLAN_TOTAL)

		if iGameTurn == getTurnForYear(1230 + utils.getSeed()%10): #Linkman226- Mongol Conquerors for Seljuks
		
			# let Seljuk army decay for everyone
			lSeljukUnits = [pSeljuks.getUnit(i) for i in range(pSeljuks.getNumUnits())]
			
			lUnitsToRemove = []
			for unit in lSeljukUnits:
				if unit.getUnitType() == iSeljukGhulamWarrior:
					if gc.getGame().getSorenRandNum(2, 'Delete unit') != 0:
						lUnitsToRemove.append(unit)
						
			for unit in lUnitsToRemove:
				unit.kill(False, iBarbarian)
		
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

				utils.makeUnitAI(iMongolianKeshik, iMongolia, spawnPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 + iModifier)
				utils.makeUnitAI(iHorseArcher, iMongolia, spawnPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1 + iModifier)
				utils.makeUnitAI(iTrebuchet, iMongolia, spawnPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
				if utils.getHumanID() in lCivGroups[1]:
					CyInterface().addMessage(utils.getHumanID(), True, iDuration, CyTranslator().getText("TXT_KEY_MONGOL_HORDE", (gc.getPlayer(iSeljuks).getCivilizationAdjectiveKey(),)), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
		if iGameTurn == getTurnForYear(1230 + utils.getSeed()%10 + 3): #Linkman226- Mongol Conquerors for Seljuks
			if pSeljuks.isAlive() and utils.getHumanID() != iMongolia:
				tPlot = utils.getFreeNeighborPlot((83, 42))
				utils.makeUnitAI(iMongolianKeshik, iMongolia, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
				utils.makeUnitAI(iHorseArcher, iMongolia, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
				utils.makeUnitAI(iTrebuchet, iMongolia, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
				
				
		# Leoreth: make sure Aztecs are dead in 1700 if a civ that spawns from that point is selected
		if iGameTurn == getTurnForYear(1700)-2:
			if utils.getHumanID() >= iGermany and pAztecs.isAlive():
				sta.completeCollapse(iAztecs)
				#utils.killAndFragmentCiv(iAztecs, iIndependent, iIndependent2, -1, False)
				
				
		if utils.getScenario() == i3000BC:
			iFirstSpawn = iGreece
		elif utils.getScenario() == i600AD:
			iFirstSpawn = iArabia
		else:
			iFirstSpawn = iAmerica
			
		for iLoopCiv in range(iFirstSpawn, iNumMajorPlayers):
			if (iGameTurn >= getTurnForYear(tBirth[iLoopCiv]) - 2 and iGameTurn <= getTurnForYear(tBirth[iLoopCiv]) + 6):
				self.initBirth(iGameTurn, tBirth[iLoopCiv], iLoopCiv)



		if (iGameTurn == getTurnForYear(600)):
			if utils.getScenario() == i600AD:  #late start condition
				tTL, tBR = Areas.tBirthArea[iChina]
				if utils.getHumanID() != iChina: tTL = (99, 39) # 4 tiles further north
				iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iChina, utils.getPlotList(tTL, tBR))
				self.convertSurroundingPlotCulture(iChina, utils.getPlotList(tTL, tBR))
				utils.flipUnitsInArea(tTL, tBR, iChina, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ   
				utils.flipUnitsInArea(tTL, tBR, iChina, iIndependent, False, False) #remaining independents in the region now belong to the new civ   
				utils.flipUnitsInArea(tTL, tBR, iChina, iIndependent2, False, False) #remaining independents in the region now belong to the new civ

				
		#kill the remaining barbs in the region: it's necessary to do this more than once to protect those civs
		for iPlayer in [iVikings, iSpain, iFrance, iHolyRome, iRussia]:
			if iGameTurn >= getTurnForYear(tBirth[iPlayer])+2 and iGameTurn <= getTurnForYear(tBirth[iVikings])+utils.getTurns(10):
				utils.killUnitsInArea(iBarbarian, Areas.getBirthArea(iPlayer))
				
		#fragment utility
		if (iGameTurn >= getTurnForYear(50) and iGameTurn % utils.getTurns(15) == 6):
			self.fragmentIndependents()
#		if (iGameTurn >= getTurnForYear(450) and iGameTurn % utils.getTurns(30) == 12):
#			self.fragmentBarbarians(iGameTurn)
			
		#fall of civs
		#if (iGameTurn >= getTurnForYear(200) and iGameTurn % utils.getTurns(4) == 0):
		#	self.collapseByBarbs(iGameTurn)					
		#if (iGameTurn >= getTurnForYear(-2000) and iGameTurn % utils.getTurns(18) == 0): #used to be 15 in vanilla, because we must give some time for vassal states to form
		#	self.collapseGeneric(iGameTurn)
		#if (iGameTurn >= getTurnForYear(-2000) and iGameTurn % utils.getTurns(13) == 7): #used to be 8 in vanilla, because we must give some time for vassal states to form
		#	self.collapseMotherland(iGameTurn)
		#if (iGameTurn > getTurnForYear(300) and iGameTurn % utils.getTurns(10) == 6):
		#	self.secession(iGameTurn)

		if iGameTurn % utils.getTurns(10) == 5:
			sta.checkResurrection(iGameTurn)
			
		# Leoreth: check for scripted rebirths
		for iCiv in range(iNumPlayers):
			if tRebirth[iCiv] != -1:
				if iGameTurn == getTurnForYear(tRebirth[iCiv]) and not gc.getPlayer(iCiv).isAlive():
					self.rebirthFirstTurn(iCiv)
				if iGameTurn == getTurnForYear(tRebirth[iCiv])+1 and gc.getPlayer(iCiv).isAlive() and utils.isReborn(iCiv):
					self.rebirthSecondTurn(iCiv)
					
	def endTurn(self, iPlayer):
		for tTimedConquest in sd.getTimedConquests():
			iConqueror, x, y = tTimedConquest
			utils.colonialConquest(iConqueror, x, y)
		sd.resetTimedConquests()

	def rebirthFirstTurn(self, iCiv):
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		if tRebirthCiv[iCiv] != -1:
			pCiv.setCivilizationType(tRebirthCiv[iCiv])
		x, y = Areas.dRebirthPlot[iCiv]
		plot = gc.getMap().plot(x,y)
		
		# disable Mexico and Colombia
		if iCiv == iAztecs and gc.getDefineINT("PLAYER_REBIRTH_MEXICO") == 0: return
		if iCiv == iMaya and gc.getDefineINT("PLAYER_REBIRTH_COLOMBIA") == 0: return
		
		# reset contacts and make peace
		for iOtherCiv in range(iNumPlayers):
			if iCiv != iOtherCiv:
				teamCiv.makePeace(iOtherCiv)
				teamCiv.cutContact(iOtherCiv)
		
		# reset diplomacy
		pCiv.AI_reset()
		
		# reset map visibility
		for i in range(gc.getMap().getGridWidth()):
			for j in range(gc.getMap().getGridHeight()):
				gc.getMap().plot(i, j).setRevealed(iCiv, False, True, -1)
		
		# assign new leader
		if iCiv in rebirthLeaders:
			if pCiv.getLeader() != rebirthLeaders[iCiv]:
				pCiv.setLeader(rebirthLeaders[iCiv])

		CyInterface().addMessage(gc.getGame().getActivePlayer(), True, iDuration, (CyTranslator().getText("TXT_KEY_INDEPENDENCE_TEXT", (pCiv.getCivilizationAdjectiveKey(),))), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
		utils.setReborn(iCiv, True)
		
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
				utils.makeUnit(iSettler, iCiv, (x,y), 1)
				
		# make sure there is a palace in the city
		if plot.isCity():
			capital = plot.getPlotCity()
			if not capital.hasBuilding(iPalace):
				capital.setHasRealBuilding(iPalace, True)
		
		self.createRespawnUnits(iCiv, (x,y))
		
		# for colonial civs, set dynamic state religion
		if iCiv in [iAztecs, iMaya]:
			self.setStateReligion(iCiv)

		self.assignTechs(iCiv)
		if (gc.getGame().getGameTurn() >= getTurnForYear(tBirth[gc.getGame().getActivePlayer()])):
			self.respawnPopup(iCiv)

		self.setLatestRebellionTurn(iCiv, getTurnForYear(tRebirth[iCiv]))
		
		dc.onCivRespawn(iCiv, [])
		
	def rebirthSecondTurn(self, iCiv):		
		lRebirthPlots = Areas.getRebirthArea(iCiv)
		
		# exclude American territory for Mexico
		lRemovedPlots = []
		if iCiv == iAztecs:
			for tPlot in lRebirthPlots:
				x, y = tPlot
				plot = gc.getMap().plot(x, y)
				if plot.getOwner() == iAmerica and tPlot not in Areas.getCoreArea(iAztecs, True):
					lRemovedPlots.append((x, y))
					
		for (x, y) in lRemovedPlots:
			lRebirthPlots.remove((x, y))
		
		seljukUnits = []
		lCities = []
		for tPlot in lRebirthPlots:
			x, y = tPlot
			plot = gc.getMap().plot(x, y)
			for i in range(plot.getNumUnits()):
				unit = plot.getUnit(i)
				if unit.getOwner() == iSeljuks:
					seljukUnits.append(unit)
					
			if plot.isCity():
				lCities.append(plot.getPlotCity())
					
		for unit in seljukUnits:
			unit.kill(False, iBarbarian)
			
		# remove garrisons
		for city in lCities:
			if city.getOwner() != utils.getHumanID():
				x = city.getX()
				y = city.getY()
				utils.relocateGarrisons((x,y), city.getOwner())
				utils.relocateSeaGarrisons((x,y), city.getOwner())
				#utils.createGarrisons((x,y), iCiv)
				
		# convert cities
		iConvertedCities, iHumanCities = self.convertSurroundingCities(iCiv, lRebirthPlots)
		
		# create garrisons
		for city in lCities:
			if city.getOwner() == utils.getHumanID():
				x = city.getX()
				y = city.getY()
				utils.createGarrisons((x, y), iCiv, 1)
				
		# convert plot culture
		self.convertSurroundingPlotCulture(iCiv, lRebirthPlots)
		
		# reset plague
		utils.setPlagueCountdown(iCiv, -10)
		utils.clearPlague(iCiv)
		
		# adjust starting stability
		sd.setStabilityLevel(iCiv, iStabilityStable)
		sd.resetStability(iCiv)
		if utils.getHumanID() == iCiv: sd.resetHumanStability()
		
		# ask human player for flips
		if iHumanCities > 0 and iCiv != utils.getHumanID():
			self.flipPopup(iCiv, lRebirthPlots)

		# adjust civics, religion and other special settings
		if iCiv == iRome:
			if gc.getMap().plot(61,47).isCity():
				pVenice = gc.getMap().plot(61,47).getPlotCity()
				pVenice.setCulture(iRome, 100, True)
				pVenice.setPopulation(4)
				utils.makeUnit(iGalley, iRome, (pVenice.plot().getX(), pVenice.plot().getY()), 2)
			pRome.setLastStateReligion(iCatholicism)
			pRome.setCivics(0, iCivicCityStates)
			pRome.setCivics(1, iCivicAbsolutism)
			pRome.setCivics(2, iCivicAgrarianism)
			pRome.setCivics(3, iCivicGuilds)
			pRome.setCivics(4, iCivicOrganizedReligion)
			pRome.setCivics(5, iCivicMercenaries)
		elif iCiv == iPersia:
			pPersia.setLastStateReligion(iIslam)
			pPersia.setCivics(0, iCivicDynasticism)
			pPersia.setCivics(1, iCivicAbsolutism)
			pPersia.setCivics(2, iCivicSlavery)
			pPersia.setCivics(3, iCivicGuilds)
			pPersia.setCivics(4, iCivicFanaticism)
			pPersia.setCivics(5, iCivicLevyArmies)
		elif iCiv == iAztecs:
			if gc.getMap().plot(18, 37).isCity():
				city = gc.getMap().plot(18, 37).getPlotCity()
				if gc.getGame().getBuildingClassCreatedCount(gc.getBuildingInfo(iFloatingGardens).getBuildingClassType()) == 0:
					city.setHasRealBuilding(iFloatingGardens, True)
				iStateReligion = pAztecs.getStateReligion()
				if city.isHasReligion(iStateReligion):
					city.setHasRealBuilding(iMonastery + 4 * iStateReligion, True)
			
			cnm.updateCityNamesFound(iAztecs) # use name of the plots in their city name map
			
			pAztecs.setCivics(0, iCivicRepublic)
			pAztecs.setCivics(1, iCivicRepresentation)
			pAztecs.setCivics(2, iCivicCapitalism)
			pAztecs.setCivics(3, iCivicMercantilism)
			pAztecs.setCivics(4, iCivicOrganizedReligion)
			pAztecs.setCivics(5, iCivicStandingArmy)
		elif iCiv == iMaya:
			pMaya.setCivics(0, iCivicAutocracy)
			pMaya.setCivics(1, iCivicRepresentation)
			pMaya.setCivics(2, iCivicCapitalism)
			pMaya.setCivics(3, iCivicMercantilism)
			pMaya.setCivics(4, iCivicOrganizedReligion)
			pMaya.setCivics(5, iCivicStandingArmy)
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
			if (not gc.getPlayer(iDeadCiv).isAlive() and iGameTurn > getTurnForYear(tBirth[iDeadCiv]) + utils.getTurns(50)):
				pDeadCiv = gc.getPlayer(iDeadCiv)
				teamDeadCiv = gc.getTeam(pDeadCiv.getTeam())
				iCityCounter = 0
				for (x, y) in Areas.getNormalArea(iDeadCiv):
					pCurrent = gc.getMap().plot( x, y )
					if ( pCurrent.isCity()):
						if (pCurrent.getPlotCity().getOwner() == iBarbarian):
							iCityCounter += 1
				if (iCityCounter > 3):
					iDivideCounter = 0
					for (x, y) in Areas.getNormalArea(iDeadCiv):
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
			if (gc.getPlayer(iPlayer).isAlive() and iGameTurn >= getTurnForYear(tBirth[iPlayer]) + utils.getTurns(30)):
				
				if sd.getStabilityLevel(iPlayer) == iStabilityCollapsing:

					cityList = []
					apCityList = PyPlayer(iPlayer).getCityList()
					for pCity in apCityList:
						city = pCity.GetCy()
						pCurrent = gc.getMap().plot(city.getX(), city.getY())

						if not city.isWeLoveTheKingDay() and not city.isCapital() and (city.getX(), city.getY()) != Areas.getCapital(iPlayer):
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

					if (len(cityList)):
						iNewCiv = iIndependent
						iRndNum = gc.getGame().getSorenRandNum(2, 'random independent')
						if (iRndNum % 2 == 0):
							iNewCiv = iIndependent2  
						if (iPlayer == iAztecs or \
						    iPlayer == iInca or \
						    iPlayer == iMaya or \
						    iPlayer == iEthiopia or \
						    iPlayer == iMali):
							if (utils.getCivsWithNationalism() <= 0):
								iNewCiv = iNative		    
						splittingCity = cityList[gc.getGame().getSorenRandNum(len(cityList), 'random city')]
						utils.cultureManager((splittingCity.getX(),splittingCity.getY()), 50, iNewCiv, iPlayer, False, True, True)
						utils.flipUnitsInCityBefore((splittingCity.getX(),splittingCity.getY()), iNewCiv, iPlayer)			    
						self.setTempFlippingCity((splittingCity.getX(),splittingCity.getY()))
						utils.flipCity((splittingCity.getX(),splittingCity.getY()), 0, 0, iNewCiv, [iPlayer])   #by trade because by conquest may raze the city
						utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)
						if (iPlayer == utils.getHumanID()):
							CyInterface().addMessage(iPlayer, True, iDuration, splittingCity.getName() + " " + \
											   CyTranslator().getText("TXT_KEY_STABILITY_SECESSION", ()), "", 0, "", ColorTypes(iOrange), -1, -1, True, True)
						
					return
					
	#def processConstantinople(self):
	#	asiaID = gc.getMap().plot(69, 44).area().getID()
	#	pConstantinople = gc.getMap().plot(68, 45)
	#	if (pConstantinople.area().getID() != asiaID):
	#		if (pConstantinople.isCity() and pConstantinople.getPlotCity().getOwner() < iNumMajorPlayers):
	#			return
	#		else:
	#			gc.getMap().plot(68, 45).setArea(asiaID)

	#def convertMiddleEast(self):
	#	if (gc.getMap().plot(76,40).area().getID() == iEurope):
	#		return
	#	for i in range(72,86+1):
	#		for j in range(34,46):
	#			pCurrent = gc.getMap().plot(i, j)
	#			if ((not pCurrent.isWater()) and pCurrent.area().getID() != iEurope):
	#				pCurrent.setArea(iEurope)

	#	for i in range(69,71+1):
	#		for j in range(40,45):
	#			pCurrent = gc.getMap().plot(i, j)
	#			if ((not pCurrent.isWater()) and pCurrent.area().getID() != iEurope):
	#				pCurrent.setArea(iEurope)

	#	for i in range(78,86+1):
	#		for j in range(47,49):
	#			pCurrent = gc.getMap().plot(i, j)
	#			if ((not pCurrent.isWater()) and pCurrent.area().getID() != iEurope):
	#				pCurrent.setArea(iEurope)
	#	return


	#def reconvertMiddleEast(self):
	#	if (gc.getMap().plot(76,40).area().getID() == iAsia):
	#		return
	#	for i in range(72,86+1):
	#		for j in range(34,46+1):
	#			pCurrent = gc.getMap().plot(i, j)
	#			if (not pCurrent.isWater()):
	#				pCurrent.setArea(iAsia)

	#	for i in range(69,71+1):
	#		for j in range(40,45+1):
	#			pCurrent = gc.getMap().plot(i, j)
	#			if (not pCurrent.isWater()):
	#				pCurrent.setArea(iAsia)

	#	for i in range(78,86+1):
	#		for j in range(47,49+1):
	#			pCurrent = gc.getMap().plot(i, j)
	#			if (not pCurrent.isWater()):
	#				pCurrent.setArea(iAsia)

	#def convertNorthAfrica(self):
	#	if (gc.getMap().plot(69,33).area().getID() == iEurope):
	#		return
	#	for i in range(48,65+1):
	#		for j in range(35,39+1):
	#			pCurrent = gc.getMap().plot(i, j)
	#			if (not pCurrent.isWater()):
	#				pCurrent.setArea(iEurope)

	#	for i in range(66,71+1):
	#		for j in range(29,37+1):
	#			pCurrent = gc.getMap().plot(i, j)
	#			if (not pCurrent.isWater()):
	#				pCurrent.setArea(iEurope)

	#	for i in range(72,73+1):
	#		for j in range(29,32+1):
	#			pCurrent = gc.getMap().plot(i, j)
	#			if (not pCurrent.isWater()):
	#				pCurrent.setArea(iEurope)

	#def reconvertNorthAfrica(self):
	#	if (gc.getMap().plot(69,33).area().getID() == iAsia):
	#		return
	#	for i in range(48,65+1):
	#		for j in range(35,39+1):
	#			pCurrent = gc.getMap().plot(i, j)
	#			if (not pCurrent.isWater()):
	#				pCurrent.setArea(iAsia)

	#	for i in range(66,71+1):
	#		for j in range(29,37+1):
	#			pCurrent = gc.getMap().plot(i, j)
	#			if (not pCurrent.isWater()):
	#				pCurrent.setArea(iAsia)

	#	for i in range(72,73+1):
	#		for j in range(29,32+1):
	#			pCurrent = gc.getMap().plot(i, j)
	#			if (not pCurrent.isWater()):
	#				pCurrent.setArea(iAsia)
	#def processAfrica(self):
	#	africaID = gc.getMap().plot(65, 10).area().getID()
	#	if (gc.getMap().plot(56, 29).area().getID() == africaID):
	#		return
	#	for iLoopX in range(48,63+1):
	#		for iLoopY in range(22,33+1):
	#			pCurrent = gc.getMap().plot(iLoopX, iLoopY)
	#			if (not pCurrent.isWater()):
	#				pCurrent.setArea(africaID)
			    
				    
	def initBirth(self, iCurrentTurn, iBirthYear, iCiv): # iBirthYear is really year now, so no conversion prior to function call - edead
		print 'init birth in: '+str(iBirthYear)
		iHuman = utils.getHumanID()
		iBirthYear = getTurnForYear(iBirthYear) # converted to turns here - edead
		
		if iCiv in lSecondaryCivs:
			if iHuman != iCiv and not self.getPlayerEnabled(iCiv):
				return
		
		if iCiv == iTurkey:
			if pSeljuks.isAlive():
				sta.completeCollapse(iSeljuks)
				#utils.killAndFragmentCiv(iSeljuks, iIndependent, iIndependent2, -1, False)
		
		lConditionalCivs = [iByzantium, iMughals, iThailand, iBrazil, iArgentina, iCanada]
		
		# Leoreth: extra checks for conditional civs
		if iCiv in lConditionalCivs and utils.getHumanID() != iCiv:
			if iCiv == iByzantium:
				if not pRome.isAlive() or pGreece.isAlive() or (utils.getHumanID() == iRome and utils.getStabilityLevel(iRome) == iStabilitySolid):
					return

			elif iCiv == iThailand:
				if utils.getHumanID() != iKhmer:
					if sd.getStabilityLevel(iKhmer) > iStabilityShaky:
						return
				else:
					if sd.getStabilityLevel(iKhmer) > iStabilityUnstable:
						return
						
			if iCiv in [iArgentina, iBrazil]:
				iColonyPlayer = utils.getColonyPlayer(iCiv)
				if iColonyPlayer < 0: return
				elif iColonyPlayer not in [iArgentina, iBrazil]:
					if sd.getStabilityLevel(iColonyPlayer) > iStabilityStable:
						return
						
		if utils.getHumanID() != iCiv and iCiv == iItaly:
			if pRome.isAlive():
				return
				
			cityList = utils.getCoreCityList(iRome, 0)
			
			iIndependentCities = 0

			for pCity in cityList:
				if not pCity.getOwner() < iNumPlayers:
					iIndependentCities += 1
					
			if iIndependentCities == 0:
				return
				
		tCapital = Areas.getCapital(iCiv)
				
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

		if (iCurrentTurn == iBirthYear-1 + self.getSpawnDelay(iCiv) + self.getFlipsDelay(iCiv)):
			reborn = utils.getReborn(iCiv)
			tTopLeft, tBottomRight = Areas.getBirthRectangle(iCiv)
			tBroaderTopLeft, tBroaderBottomRight = Areas.tBroaderArea[iCiv]
			
			if iCiv == iThailand:
				x, y = Areas.getCapital(iKhmer)
				if gc.getMap().plot(x, y).isCity():
					angkor = gc.getMap().plot(x, y).getPlotCity()
					bWonder = False
					for iBuilding in range(iNumBuildings):
						if angkor.isHasRealBuilding(iBuilding) and isWorldWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType()):
							bWonder = True
							break
					if bWonder and utils.getHumanID() != iThailand:
						print "Thais flip Angkor instead to save its wonders."
						angkor.setName("Ayutthaya", False)
						x, y = tCapital
						tCapital = (x-1, y+1)
						gc.getMap().plot(x-1, y+1).setFeatureType(-1, 0)
						
				utils.setReborn(iKhmer, True)
				
				# Prey Nokor becomes Saigon
				x, y = (104, 33)
				if gc.getMap().plot(x, y).isCity():
					gc.getMap().plot(x, y).getPlotCity().setName("Saigon", False)
				
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
								unit.kill(False, iBarbarian)
				
				bBirthInCapital = False
				
				if (iCiv in lConditionalCivs and iCiv != iThailand) or bCapitalSettled:
					bBirthInCapital = True
				
				if iCiv == iTurkey:
					self.moveOutInvaders(tTopLeft, tBottomRight)  
					
				if bBirthInCapital:
					utils.makeUnit(iCatapult, iCiv, (1,0), 1)
			
				bDeleteEverything = False
				pCapital = gc.getMap().plot(tCapital[0], tCapital[1])
				if (pCapital.isOwned()):
					if (iCiv == iHuman or not gc.getPlayer(iHuman).isAlive()):
						if not (pCapital.isCity() and pCapital.getPlotCity().isHolyCity()):
							bDeleteEverything = True
							print ("bDeleteEverything 1")
					else:
						bDeleteEverything = True
						for x in range(tCapital[0] - 1, tCapital[0] + 2):	# from x-1 to x+1
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
					for x in range(tCapital[0] - 1, tCapital[0] + 2):	# from x-1 to x+1
						for y in range(tCapital[1] - 1, tCapital[1] + 2):       # from y-1 to y+1
							self.setDeleteMode(0, iCiv)
							pCurrent=gc.getMap().plot(x, y)
							for iLoopCiv in range(iNumTotalPlayers+1): #Barbarians as well
								if (iCiv != iLoopCiv):
									utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iLoopCiv, True, False, utils.getOrElse(Areas.dBirthAreaExceptions, iCiv, []))
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
				
		# Leoreth: reveal all normal plots on spawn
		for (x, y) in Areas.getNormalArea(iCiv):
			gc.getMap().plot(x, y).setRevealed(iCiv, True, True, 0)
				
		# Leoreth: conditional state religion for colonial civs
		if iCiv in [iArgentina, iBrazil]:
			self.setStateReligion(iCiv)
			
		if (iCurrentTurn == iBirthYear + self.getSpawnDelay(iCiv)) and (gc.getPlayer(iCiv).isAlive()) and (self.getAlreadySwitched() == False or utils.getReborn(iCiv) == 1) and ((iHuman not in lNeighbours[iCiv] and getTurnForYear(tBirth[iCiv]) - getTurnForYear(tBirth[iHuman]) > 0) or getTurnForYear(tBirth[iCiv]) - getTurnForYear(tBirth[iHuman]) >= utils.getTurns(25) ):
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
							if unit.getUnitType() == iSeljukGhulamWarrior or unit.getUnitType() == iMongolianKeshik:
								unit.kill(False, iBarbarian)
				
		

	def deleteMode(self, iCurrentPlayer):
		iCiv = self.getDeleteMode(0)
		print ("deleteMode after", iCurrentPlayer)
		tCapital = Areas.getCapital(iCiv)
			
		
		if (iCurrentPlayer == iCiv):
			if(iCiv == iCarthage):
				for x in range(tCapital[0] - 2, tCapital[0] + 2):	# from x-2 to x+1
					for y in range(tCapital[1] - 1, tCapital[1] + 2):       # from y-1 to y+1
						pCurrent=gc.getMap().plot(x, y)
						pCurrent.setCulture(iCiv, 300, True)
			else:
				for x in range(tCapital[0] - 2, tCapital[0] + 3):	# from x-2 to x+2
					for y in range(tCapital[1] - 2, tCapital[1] + 3):       # from y-2 to y+2
						pCurrent=gc.getMap().plot(x, y)
						pCurrent.setCulture(iCiv, 300, True)
			for x in range(tCapital[0] - 1, tCapital[0] + 2):	# from x-1 to x+1
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
		for x in range(tCapital[0] - 1, tCapital[0] + 2):	# from x-1 to x+1
			for y in range(tCapital[1] - 1, tCapital[1] + 2):       # from y-1 to y+1
				#print ("deleting again", x, y)
				pCurrent=gc.getMap().plot(x, y)
				if (pCurrent.isOwned()):
					bNotOwned = False
					for iLoopCiv in range(iNumTotalPlayers+1): #Barbarians as well
						if(iLoopCiv != iCiv):
							pCurrent.setCulture(iLoopCiv, 0, True)
					pCurrent.setOwner(iCiv)
		
		for x in range(tCapital[0] - 15, tCapital[0] + 16):	# must include the distance from Sogut to the Caspius
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
					x, y = Areas.getCapital(iRome)
					pRomePlot = gc.getMap().plot(x, y)
					if pRomePlot.isCity():
						cityList.append(pRomePlot.getPlotCity())
					for city in cityList:
						if city.getPopulation() < 5: city.setPopulation(5)
						city.setHasRealBuilding(iGranary, True)
						city.setHasRealBuilding(iLibrary, True)
						city.setHasRealBuilding(iCourthouse, True)
						if city.isCoastal(20): city.setHasRealBuilding(iHarbor, True)
										
				utils.flipUnitsInArea((tCapital[0]-3, tCapital[1]-3), (tCapital[0]+3, tCapital[1]+3), iCiv, iBarbarian, True, True) #This is mostly for the AI. During Human player spawn, that area should be already cleaned			
				utils.flipUnitsInArea((tCapital[0]-3, tCapital[1]-3), (tCapital[0]+3, tCapital[1]+3), iCiv, iIndependent, True, False) #This is mostly for the AI. During Human player spawn, that area should be already cleaned			
				utils.flipUnitsInArea((tCapital[0]-3, tCapital[1]-3), (tCapital[0]+3, tCapital[1]+3), iCiv, iIndependent2, True, False) #This is mostly for the AI. During Human player spawn, that area should be already cleaned			
				self.assignTechs(iCiv)
				utils.setPlagueCountdown(iCiv, -iImmunity)
				utils.clearPlague(iCiv)
				self.setFlipsDelay(iCiv, iFlipsDelay) #save
				

		else: #starting units have already been placed, now the second part
		
			iNumCities = gc.getPlayer(iCiv).getNumCities()
		
			lPlots = utils.getPlotList(tTopLeft, tBottomRight, Areas.getBirthExceptions(iCiv))
			iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, lPlots)
			self.convertSurroundingPlotCulture(iCiv, lPlots)
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent, False, False) #remaining independents in the region now belong to the new civ   
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent2, False, False) #remaining independents in the region now belong to the new civ# starting workers
		
			# create starting workers
			if iNumCities == 0 and gc.getPlayer(iCiv).getNumCities() > 0:
				self.createStartingWorkers(iCiv, (gc.getPlayer(iCiv).getCapitalCity().getX(), gc.getPlayer(iCiv).getCapitalCity().getY()))
			
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

			#if (gc.getPlayer(iCiv).getNumCities() > 0):
			#	capital = gc.getPlayer(iCiv).getCapitalCity()
			#	self.createStartingWorkers(iCiv, (capital.getX(), capital.getY()))

			if (iNumHumanCitiesToConvert > 0 and iCiv != utils.getHumanID()): # Leoreth: quick fix for the "flip your own cities" popup, still need to find out where it comes from
				print "Flip Popup: free region"
				self.flipPopup(iCiv, lPlots)
				

			
	def birthInForeignBorders(self, iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight):
	
		if iCiv == iItaly:
			utils.removeCoreUnits(iItaly)
			cityList = utils.getCoreCityList(iItaly, 0)
			x, y = Areas.getCapital(iRome)
			pRomePlot = gc.getMap().plot(x, y)
			if pRomePlot.isCity():
				cityList.append(pRomePlot.getPlotCity())
			for pCity in cityList:
				if city.getPopulation() < 5: city.setPopulation(5)
				city.setHasRealBuilding(iGranary, True)
				city.setHasRealBuilding(iLibrary, True)
				city.setHasRealBuilding(iCourthouse, True)
				if city.isCoastal(20): city.setHasRealBuilding(iHarbor, True)
				
		iNumCities = gc.getPlayer(iCiv).getNumCities()
		
		lPlots = utils.getPlotList(tTopLeft, tBottomRight, Areas.getBirthExceptions(iCiv))
		iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, lPlots)
		self.convertSurroundingPlotCulture(iCiv, lPlots)
		
		# create starting workers
		if iNumCities == 0 and gc.getPlayer(iCiv).getNumCities() > 0:
			self.createStartingWorkers(iCiv, (gc.getPlayer(iCiv).getCapitalCity().getX(), gc.getPlayer(iCiv).getCapitalCity().getY()))

		#now starting units must be placed
		if (iNumAICitiesConverted > 0):
			dummy1, plotList = utils.squareSearch( tTopLeft, tBottomRight, utils.ownedCityPlots, iCiv )	
			rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching any city just flipped')
			if (len(plotList)):
				result = plotList[rndNum]
				if (result):
					self.createStartingUnits(iCiv, result)
					self.assignTechs(iCiv)
					utils.setPlagueCountdown(iCiv, -iImmunity)
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
					utils.setPlagueCountdown(iCiv, -iImmunity)
					utils.clearPlague(iCiv)
			else:
				dummy1, plotList = utils.squareSearch( tBroaderTopLeft, tBroaderBottomRight, utils.goodPlots, [] )	
				rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching other good plots in a broader region')
				if (len(plotList)):
					result = plotList[rndNum]
					if (result):
						self.createStartingUnits(iCiv, result)
						#self.createStartingWorkers(iCiv, result)
						self.assignTechs(iCiv)
						utils.setPlagueCountdown(iCiv, -iImmunity)
						utils.clearPlague(iCiv)
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iBarbarian, True, True) #remaining barbs in the region now belong to the new civ 
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent, True, False) #remaining barbs in the region now belong to the new civ 
			utils.flipUnitsInArea(tTopLeft, tBottomRight, iCiv, iIndependent2, True, False) #remaining barbs in the region now belong to the new civ 

		if (iNumHumanCitiesToConvert > 0):
			print "Flip Popup: foreign borders"
			self.flipPopup(iCiv, lPlots)
			
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
				gc.getMap().plot(tCapital[0], tCapital[1]).getPlotCity().setHasRealBuilding(iPalace, True)
				utils.convertPlotCulture(gc.getMap().plot(tCapital[0], tCapital[1]), iCiv, 100, True)
				self.convertSurroundingPlotCulture(iCiv, utils.getPlotList((tCapital[0]-1,tCapital[1]-1), (tCapital[0]+1,tCapital[1]+1)))
				
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

				utils.setPlagueCountdown(iCiv, -iImmunity)
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
				dc.onCityAcquired(iCiv, iOwner)
				
				self.createStartingWorkers(iCiv, tCapital)

		else:	   # starting units have already been placed, now to the second part
			lPlots = utils.getPlotList(tTopLeft, tBottomRight, Areas.getBirthExceptions(iCiv))
			iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, lPlots)
			self.convertSurroundingPlotCulture(iCiv, lPlots)
				
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
			#if gc.getPlayer(iCiv).getNumCities() > 0:
			#	capital = gc.getPlayer(iCiv).getCapitalCity()
			#	self.createStartingWorkers(iCiv, (capital.getX(), capital.getY()))
				
			# convert human cities
			if iNumHumanCitiesToConvert > 0:
				print "Flip Popup: in capital"
				self.flipPopup(iCiv, lPlots)
				
			utils.convertPlotCulture(gc.getMap().plot(tCapital[0], tCapital[1]), iCiv, 100, True)
			
				
	def getConvertedCities(self, iPlayer, lPlots):
		lCities = []
		
		for city in utils.getAreaCities(lPlots):
			if city.plot().isCore(city.getOwner()) and not city.plot().isCore(iPlayer): continue
			
			if city.getOwner() != iPlayer:
				lCities.append(city)
			
		# Leoreth: Byzantium also flips Roman cities in the eastern half of the empire outside of its core (Egypt, Mesopotamia)
		if iPlayer == iByzantium and pRome.isAlive():
			x, y = Areas.getCapital(iByzantium)
			for city in utils.getCityList(iRome):
				if city.getX() >= x-1 and city.getY() <= y:
					lCities.append(city)
					
		# Leoreth: Canada also flips English/American/French cities in the Canada region
		if iPlayer == iCanada:
			lCanadaCities = []
			lCanadaCities.extend(utils.getCityList(iFrance))
			lCanadaCities.extend(utils.getCityList(iEngland))
			lCanadaCities.extend(utils.getCityList(iAmerica))
			
			for city in lCanadaCities:
				if city.getRegionID() == rCanada and city.getX() < Areas.getCapital(iCanada)[0] and city not in lCities:
					lCities.append(city)
					
		# Leoreth: remove capital locations
		for city in lCities:
			if city.getOwner() < iNumPlayers:
				if (city.getX(), city.getY()) == Areas.getCapital(city.getOwner()) and city.isCapital():
					lCities.remove(city)

		return lCities
						
	def convertSurroundingCities(self, iPlayer, lPlots):
		iConvertedCitiesCount = 0
		iNumHumanCities = 0
		self.setSpawnWar(0)
					
		lEnemies = []
		lCities = self.getConvertedCities(iPlayer, lPlots)
		
		for city in lCities:
			x = city.getX()
			y = city.getY()
			iHuman = utils.getHumanID()
			iOwner = city.getOwner()
			iCultureChange = 0
			
			# Case 1: Minor civilization
			if iOwner in [iBarbarian, iIndependent, iIndependent2, iCeltia, iSeljuks, iNative]:
				iCultureChange = 100
				
			# Case 2: Human city
			elif iOwner == iHuman:
				iNumHumanCities += 1
				
			# Case 3: Other
			else:
				iCultureChange = 100
				if iOwner not in lEnemies: lEnemies.append(iOwner)
				
			if iCultureChange > 0:
				utils.completeCityFlip(x, y, iPlayer, iOwner, iCultureChange, True, False, False, True)
				iConvertedCitiesCount += 1
				
		self.warOnSpawn(iPlayer, lEnemies)
				
		if iConvertedCitiesCount > 0:
			if iHuman == iPlayer:
				CyInterface().addMessage(iPlayer, True, iDuration, CyTranslator().getText("TXT_KEY_FLIP_TO_US", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
				
		return iConvertedCitiesCount, iNumHumanCities
		
	def warOnSpawn(self, iPlayer, lEnemies):
		if iPlayer == iCanada: return
		elif iPlayer == iGermany and utils.getHumanID() != iPlayer: return
		
		if gc.getGame().getGameTurn() <= getTurnForYear(tBirth[iPlayer]) + 5:
			for iEnemy in lEnemies:
				tEnemy = gc.getTeam(iEnemy)
				
				if tEnemy.isAtWar(iPlayer): continue
				if iPlayer == iByzantium and iEnemy == iRome: continue
			
				iRand = gc.getGame().getSorenRandNum(100, 'War on spawn')
				if iRand >= tAIStopBirthThreshold[iEnemy]:
					tEnemy.declareWar(iPlayer, True, WarPlanTypes.WARPLAN_ATTACKED_RECENT)
					self.spawnAdditionalUnits(iPlayer)
					
	def spawnAdditionalUnits(self, iPlayer):
		tPlot = Areas.getCapital(iPlayer)
		
		#if gc.getPlayer(iPlayer).getNumCities() > 0:
		#	tPlot[0] = gc.getPlayer(iPlayer).getCapitalCity().getX()
		#	tPlot[1] = gc.getPlayer(iPlayer).getCapitalCity().getY()

		self.createAdditionalUnits(iPlayer, tPlot)

	def convertSurroundingPlotCulture(self, iCiv, lPlots):
		for (x, y) in lPlots:
			pCurrent = gc.getMap().plot(x, y)
			if pCurrent.isCore(pCurrent.getOwner()) and not pCurrent.isCore(iCiv): continue
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


	def giveRaiders( self, iCiv, lPlots):
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		if (pCiv.isAlive() and pCiv.isHuman() == False):

			cityList = []
			#collect all the coastal cities belonging to iCiv in the area
			for (x, y) in lPlots:
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
						gc.getPlayer(iCiv).initUnit(iGalley, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
						if (teamCiv.isHasTech(iCivilService)):
							if (iCiv == iVikings):
								gc.getPlayer(iCiv).initUnit(iVikingHuscarl, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								gc.getPlayer(iCiv).initUnit(iVikingHuscarl, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)
							else:
								gc.getPlayer(iCiv).initUnit(iHeavySwordsman, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								gc.getPlayer(iCiv).initUnit(iHeavySwordsman, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)

						else:
							gc.getPlayer(iCiv).initUnit(iSwordsman, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
							gc.getPlayer(iCiv).initUnit(iSwordsman, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)

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
					if pCity.getRegionID() == rIberia:
						tCapital = (pCity.getX(), pCity.getY())
						break
			
			if (tSeaPlot):
				gc.getPlayer(iCiv).initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iArcher, iCiv, tSeaPlot, 1)

	def giveColonists(self, iCiv):
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		
		if pCiv.isAlive() and utils.getHumanID() != iCiv:
			if teamCiv.isHasTech(iAstronomy) and self.getColonistsAlreadyGiven(iCiv) < tMaxColonists[iCiv]:
				lCities = utils.getAreaCitiesCiv(iCiv, Areas.getCoreArea(iCiv))
				
				# help England with settling Canada and Australia
				if iCiv == iEngland:
					lColonialCities = utils.getAreaCitiesCiv(iCiv, utils.getPlotList(tCanadaTL, tCanadaBR))
					lColonialCities.extend(utils.getAreaCitiesCiv(iCiv, utils.getPlotList(tAustraliaTL, tAustraliaBR)))
					
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
					
					utils.makeUnitAI(utils.getUniqueUnitType(iCiv, gc.getUnitInfo(iGalleon).getUnitClassType()), iCiv, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA, 1)
					utils.makeUnitAI(iSettler, iCiv, tSeaPlot, UnitAITypes.UNITAI_SETTLE, 1)
					utils.makeUnit(utils.getBestDefender(iCiv), iCiv, tSeaPlot, 1)
					utils.makeUnit(iWorker, iCiv, tSeaPlot, 1)
					
					self.changeColonistsAlreadyGiven(iCiv, 1)
					

	def onFirstContact(self, iTeamX, iHasMetTeamY):
	
		iGameTurn = gc.getGame().getGameTurn()
		
		# no conquerors for minor civs
		if iHasMetTeamY >= iNumPlayers: return
		
		if iGameTurn > getTurnForYear(600) and iGameTurn < getTurnForYear(1800):
			if iTeamX in lCivBioNewWorld and iHasMetTeamY in lCivBioOldWorld:
				iNewWorldCiv = iTeamX
				iOldWorldCiv = iHasMetTeamY
				
				iIndex = lCivBioNewWorld.index(iNewWorldCiv)
				
				bAlreadyContacted = (self.getFirstContactConquerors(iIndex) == 1)
				
				# avoid "return later" exploit
				if iGameTurn <= getTurnForYear(tBirth[iAztecs])+10:
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
						gc.getMap().plot(27, 29).setPlotType(PlotTypes.PLOT_HILLS, True, True) #Bogota
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
									if not plot.getFeatureType() in [iJungle, iRainforest] and not plot.getTerrainType() == iMarsh and (x,y) != (25, 32):
										if gc.getMap().getArea(plot.getArea()).getNumTiles() > 3:
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
							
						if gc.getGame().getGameTurnYear() < tBirth[utils.getHumanID()]:
							iModifier1 += 1
							iModifier2 += 1
							
						teamOldWorldCiv.declareWar(iNewWorldCiv, True, WarPlanTypes.WARPLAN_TOTAL)
						
						iInfantry = utils.getBestInfantry(iOldWorldCiv)
						iCounter = utils.getBestCounter(iOldWorldCiv)
						iCavalry = utils.getBestCavalry(iOldWorldCiv)
						iSiege = utils.getBestSiege(iOldWorldCiv)
						iStateReligion = gc.getPlayer(iOldWorldCiv).getStateReligion()
						
						if iInfantry:
							utils.makeUnitAI(iInfantry, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1 + iModifier2)
						
						if iCounter:
							utils.makeUnitAI(iCounter, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
							
						if iSiege:
							utils.makeUnitAI(iSiege, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1 + iModifier1 + iModifier2)
							
						if iCavalry:
							utils.makeUnitAI(iCavalry, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 + iModifier1)
							
						if iStateReligion >= 0:
							utils.makeUnit(iMissionary + iStateReligion, iOldWorldCiv, tArrivalPlot, 1)
							
						if iNewWorldCiv == iInca:
							utils.makeUnitAI(iIncanAucac, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
						elif iNewWorldCiv == iAztecs:
							utils.makeUnitAI(iAztecJaguar, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
							utils.makeUnitAI(iMayanHolkan, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
						elif iNewWorldCiv == iMaya:
							utils.makeUnitAI(iMayanHolkan, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
							utils.makeUnitAI(iAztecJaguar, iOldWorldCiv, tArrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
						
						if utils.getHumanID() == iNewWorldCiv:
							CyInterface().addMessage(iNewWorldCiv, True, iDuration, CyTranslator().getText("TXT_KEY_FIRST_CONTACT_NEWWORLD", ()), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
						if utils.getHumanID() == iOldWorldCiv:
							CyInterface().addMessage(iOldWorldCiv, True, iDuration, CyTranslator().getText("TXT_KEY_FIRST_CONTACT_OLDWORLD", ()), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
							
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
					
					iHandicap = 0
					if utils.getHumanID() == iTeamX:
						iHandicap = gc.getGame().getHandicapType() / 2

					if iTeamX in [iArabia, iPersia]:
						lPlotList = utils.getBorderPlotList(iTeamX, DirectionTypes.DIRECTION_NORTH)
					elif iTeamX in [iByzantium, iRussia]:
						lPlotList = utils.getBorderPlotList(iTeamX, DirectionTypes.DIRECTION_EAST)
						
					for tPlot in lPlotList:
						x, y = tPlot
						if x < iWesternLimit:
							lPlotList.remove(tPlot)

					for i in range(3):
						if len(lPlotList) > 0:
							iRand = gc.getGame().getSorenRandNum(len(lPlotList), 'Random target plot')
							lTargetList.append(lPlotList[iRand])
							lPlotList.remove(lPlotList[iRand])

					for tPlot in lTargetList:
						utils.makeUnitAI(iMongolianKeshik, iMongolia, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 + iHandicap)
						utils.makeUnitAI(iHorseArcher, iMongolia, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1 + 2 * iHandicap)
						utils.makeUnitAI(iTrebuchet, iMongolia, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1 + iHandicap)

					if utils.getHumanID() == iTeamX:
						CyInterface().addMessage(iTeamX, True, iDuration, CyTranslator().getText("TXT_KEY_MONGOL_HORDE_HUMAN", ()), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
					elif gc.getTeam(gc.getPlayer(utils.getHumanID()).getTeam()).canContact(iTeamX):
						CyInterface().addMessage(utils.getHumanID(), True, iDuration, CyTranslator().getText("TXT_KEY_MONGOL_HORDE", (gc.getPlayer(iTeamX).getCivilizationAdjectiveKey(),)), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)

	def lateTradingCompany(self, iCiv):
		if utils.getHumanID() != iCiv and not utils.isAVassal(iCiv) and utils.getScenario() != i1700AD:
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
						utils.makeUnitAI(iAmericanMinuteman, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
						utils.makeUnitAI(iCannon, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
						
				if 2-iCount > 0:
					for i in range(2-iCount):
						iRand = gc.getGame().getSorenRandNum(len(lWestCoast), 'random spawn plot')
						tPlot = lWestCoast[iRand]
						utils.makeUnit(iSettler, iCiv, tPlot, 1)
						utils.makeUnit(iAmericanMinuteman, iCiv, tPlot, 1)
						
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
						utils.makeUnitAI(iRifleman, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 4)
						utils.makeUnitAI(iCannon, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
				else:
					bFree = True
					
					for i in range(x-1, x+2):
						for j in range(y-1, y+2):
							bFree = False
							break
					
					if bFree:
						pRussia.found(x, y)
						utils.makeUnit(iRifleman, iCiv, tVladivostok, 2)
						utils.makeUnit(iRifleman, iCiv, tVladivostok, 2)
					


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
							sAskCities += CyTranslator().getText("TXT_KEY_AND", ()) + gc.getMap().plot(x, y).getPlotCity().getName()
						
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
				if iTargetCiv < iNumPlayers:
					if iRand >= tPatienceThreshold[iTargetCiv] and not gc.getTeam(iPlayer).isAtWar(iTargetCiv):
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
							#utils.colonialConquest(iPlayer, x, y)
							sd.timedConquest(iPlayer, x, y)
						targetList.remove(tPlot)

		pPlayer.setGold(max(0, pPlayer.getGold()-iGold))

	def handleColonialConquest(self, iPlayer):
		targetList = utils.getColonialTargets(iPlayer)

		for tPlot in targetList:
			x, y = tPlot
			#utils.colonialConquest(iPlayer, x, y)
			sd.timedConquest(iPlayer, x, y)

		tSeaPlot = -1
		x, y = targetList[0]
		for i in range(x-1, x+2):
			for j in range(y-1, y+2):
				if gc.getMap().plot(i, j).isWater():
					tSeaPlot = (i, j)
					break

		if tSeaPlot != -1:
			if iPlayer == iNetherlands:
				utils.makeUnit(iDutchEastIndiaman, iPlayer, tSeaPlot, 1)
			else:
				utils.makeUnit(iGalleon, iPlayer, tSeaPlot, 1)
				
				
	#def onProjectBuilt(self, city, iProjectType):
		#if iProjectType == iPersecutionProject:
		#	lReligionList = []
		#	iOwner = city.getOwner()
		#	pOwner = gc.getPlayer(iOwner)
		#	iStateReligion = pOwner.getStateReligion()
		#				
		#	for iReligion in range(iNumReligions):
		#		if city.isHasReligion(iReligion) and iReligion != iStateReligion and not city.isHolyCityByType(iReligion):
		#			lReligionList.append(iReligion)
		#			
		#	if utils.getHumanID() != iOwner:
		#		iPersecutedReligion = self.getPersecutedReligion(lReligionList, iStateReligion)
		#	else:
		#		iPersecutedReligion = -1
		#		self.launchPersecutionPopup(lReligionList, city)
		#	
		#	if iPersecutedReligion > -1:
		#		city.setHasReligion(iPersecutedReligion, False, True, True)
		#		city.setHasRealBuilding(iTemple + 4*iPersecutedReligion, False)
		#		city.setHasRealBuilding(iMonastery + 4*iPersecutedReligion, False)
		#		city.setHasRealBuilding(iCathedral + 4*iPersecutedReligion, False)
		#		
		#		city.changeOccupationTimer(2)
		#		city.changeHurryAngerTimer(city.hurryAngerLength(0))
		#		
		#		iCountdown = 10
		#		iCountdown -= abs(gc.getLeaderheadInfo(gc.getPlayer(iOwner).getLeader()).getDifferentReligionAttitudeChange())
		#		
		#		if gc.getPlayer(iOwner).getCivics(0) == iTheocracy or gc.getPlayer(iOwner).getCivics(4) == iFanaticism:
		#			iCountdown -= 2
		#		
		#		CyInterface().addMessage(city.getOwner(), True, iDuration, CyTranslator().getText("TXT_KEY_PERSECUTION_PERFORMED", (gc.getReligionInfo(iPersecutedReligion).getText(), city.getName())), "", 0, "", ColorTypes(iWhite), -1, -1, True, True)
				
		#	gc.getTeam(pOwner.getTeam()).changeProjectCount(iPersecutionProject, -1)
			
	#def getPersecutedReligion(self, lReligionList, iStateReligion):
	#	for iReligion in tPersecutionPreference[iStateReligion]:
	#		if iReligion in lReligionList:
	#			return iReligion
	#			
	#	return -1
		
	#def launchPersecutionPopup(self, lReligionList, city):
	#	popup = Popup.PyPopup(7627, EventContextTypes.EVENTCONTEXT_ALL)
	#	popup.setBodyString(CyTranslator().getText("TXT_KEY_PERSECUTION_MESSAGE", (city.getName(),)))
	#	
	#	for iReligion in lReligionList:
	#		popup.addButton(gc.getReligionInfo(iReligion).getText())
	#		
	#	argsList = [lReligionList, (city.getX(), city.getY())]
	#	utils.setTempEventList(argsList)
	#	
	#	popup.launch(False)
	
	
	def startWarsOnSpawn(self, iCiv):
	
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		
		iMin = 10
		
		if gc.getGame().getSorenRandNum(100, 'Trigger spawn wars') >= iMin:
			for iLoopCiv in lEnemyCivsOnSpawn[iCiv]:
				if utils.isAVassal(iLoopCiv): continue
				if not gc.getPlayer(iLoopCiv).isAlive(): continue
				if teamCiv.isAtWar(iLoopCiv): continue
				if utils.getHumanID() == iCiv and iLoopCiv not in lTotalWarOnSpawn[iCiv]: continue
				
				iLoopMin = 50
				if iLoopCiv >= iNumMajorPlayers: iLoopMin = 30
				if utils.getHumanID() == iLoopCiv: iLoopMin += 10
				
				if gc.getGame().getSorenRandNum(100, 'Check spawn war') >= iLoopMin:
					iWarPlan = -1
					if iLoopCiv in lTotalWarOnSpawn[iCiv]:
						iWarPlan = WarPlanTypes.WARPLAN_TOTAL
					teamCiv.declareWar(iLoopCiv, False, iWarPlan)
					
					if utils.getHumanID() == iCiv: self.setBetrayalTurns(0)
					
					
	def immuneMode(self, argsList): 
		pWinningUnit,pLosingUnit = argsList
		iLosingPlayer = pLosingUnit.getOwner()
		iUnitType = pLosingUnit.getUnitType()
		if (iLosingPlayer < iNumMajorPlayers):
			if (gc.getGame().getGameTurn() >= getTurnForYear(tBirth[iLosingPlayer]) and gc.getGame().getGameTurn() <= getTurnForYear(tBirth[iLosingPlayer])+2):
				if (pLosingUnit.getX(), pLosingUnit.getY()) == Areas.getCapital(iLosingPlayer):
					print("new civs are immune for now")
					if (gc.getGame().getSorenRandNum(100, 'immune roll') >= 50):
						utils.makeUnit(iUnitType, iLosingPlayer, (pLosingUnit.getX(), pLosingUnit.getY()), 1)

	def initMinorBetrayal( self, iCiv ):
		iHuman = utils.getHumanID()
		tTL, tBR = Areas.tBirthArea[iCiv]
		dummy, plotList = utils.squareSearch(tTL, tBR, utils.outerInvasion, [])
		rndNum = gc.getGame().getSorenRandNum(len(plotList), 'searching a free plot abroad human players borders')
		if (len(plotList)):
			result = plotList[rndNum]
			if (result):
				self.createAdditionalUnits(iCiv, result)
				self.unitsBetrayal(iCiv, iHuman, tTL, tBR, result, utils.getOrElse(Areas.dBirthAreaExceptions, iCiv, []))

	def initBetrayal( self ):
		iFlipPlayer = self.getNewCivFlip()
		if not gc.getPlayer(iFlipPlayer).isAlive() or not gc.getTeam(iFlipPlayer).isAtWar(utils.getHumanID()):
			return
	
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
			CyInterface().addMessage(self.getOldCivFlip(), False, iDuration, CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
		elif (gc.getPlayer(self.getNewCivFlip()).isHuman()):
			CyInterface().addMessage(self.getNewCivFlip(), False, iDuration, CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL_NEW", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
		for x in range(tTopLeft[0], tBottomRight[0]+1):
			for y in range(tTopLeft[1], tBottomRight[1]+1):
				if (x, y) not in lExceptions:
					killPlot = gc.getMap().plot(x,y)
					if killPlot.isCore(iOldOwner) and not killPlot.isCore(iNewOwner): continue
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
		if iCiv == iIndia:
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iAxeman, iCiv, tPlot, 1)
		if (iCiv == iGreece):
			utils.makeUnit(iGreekHoplite, iCiv, tPlot, 4)
		if (iCiv == iPersia):
			utils.makeUnit(iPersianImmortal, iCiv, tPlot, 4)
		if (iCiv == iCarthage):
			utils.makeUnit(iPhoenicianAfricanWarElephant, iCiv, tPlot, 1)
		if iCiv == iPolynesia:
			utils.makeUnit(iWarrior, iCiv, tPlot, 2)
		if (iCiv == iRome):
			utils.makeUnit(iRomanLegion, iCiv, tPlot, 4)
		if (iCiv == iJapan):
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
		if iCiv == iTamils:
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iWarElephant, iCiv, tPlot, 1)
		if (iCiv == iEthiopia):
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
		if (iCiv == iKorea):
			for iUnit in [iHorseArcher, iCrossbowman]:
				utils.makeUnit(iUnit, iCiv, tPlot, 2)
		if (iCiv == iMaya):
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iMayanHolkan, iCiv, tPlot, 2)
		if (iCiv == iByzantium):
			utils.makeUnit(iByzantineCataphract, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 2)   
		if (iCiv == iVikings):
			utils.makeUnit(iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
		if (iCiv == iArabia):
			utils.makeUnit(iLongbowman, iCiv, tPlot, 2)
			utils.makeUnit(iArabianCamelArcher, iCiv, tPlot, 4)
		if iCiv == iTibet:
			utils.makeUnit(iTibetanKhampa, iCiv, tPlot, 2)
		if (iCiv == iKhmer):
			utils.makeUnit(iSwordsman, iCiv, tPlot, 3)
			utils.makeUnit(iKhmerBallistaElephant, iCiv, tPlot, 2)
		if (iCiv == iIndonesia):
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iWarElephant, iCiv, tPlot, 1)
		if iCiv == iMoors:
			utils.makeUnit(iArabianCamelArcher, iCiv, tPlot, 2)
		if (iCiv == iSpain):
			utils.makeUnit(iLongbowman, iCiv, tPlot, 3)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 3)
		if (iCiv == iFrance):
			utils.makeUnit(iLongbowman, iCiv, tPlot, 3)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 3)
		if (iCiv == iEngland):
			utils.makeUnit(iLongbowman, iCiv, tPlot, 3)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 3)
		if (iCiv == iHolyRome):			
			utils.makeUnit(iLongbowman, iCiv, tPlot, 3)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 3)
		if (iCiv == iRussia):
			utils.makeUnit(iLongbowman, iCiv, tPlot, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 2)
		if (iCiv == iNetherlands):			
			utils.makeUnit(iMusketman, iCiv, tPlot, 3)
			utils.makeUnit(iPikeman, iCiv, tPlot, 3)
		if (iCiv == iMali):
			utils.makeUnit(iMandeSkirmisher, iCiv, tPlot, 4)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 3)
		if (iCiv == iTurkey):
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 3)
		if iCiv == iPoland:
			utils.makeUnit(iKnight, iCiv, tPlot, 2)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
		if (iCiv == iPortugal):			
			utils.makeUnit(iLongbowman, iCiv, tPlot, 3)
			utils.makeUnit(iPikeman, iCiv, tPlot, 3)
		if (iCiv == iInca):
			utils.makeUnit(iIncanAucac, iCiv, tPlot, 5)
			utils.makeUnit(iArcher, iCiv, tPlot, 3)
		if iCiv == iItaly:
			utils.makeUnit(iKnight, iCiv, tPlot, 2)
		if (iCiv == iMongolia):
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 2) 
			utils.makeUnit(iMongolianKeshik, iCiv, tPlot, 4)
		if (iCiv == iAztecs):
			utils.makeUnit(iAztecJaguar, iCiv, tPlot, 5)
			utils.makeUnit(iArcher, iCiv, tPlot, 3)
		if iCiv == iMughals:
			utils.makeUnit(iMughalSiegeElephant, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 4)
		if iCiv == iThailand:
			utils.makeUnit(iPikeman, iCiv, tPlot, 2)
			utils.makeUnit(iThaiChangSuek, iCiv, tPlot, 2)
		if iCiv == iCongo:
			utils.makeUnit(iCongolesePombos, iCiv, tPlot, 3)
		if iCiv == iGermany:
			utils.makeUnit(iRifleman, iCiv, tPlot, 5)
			utils.makeUnit(iCannon, iCiv, tPlot, 3)
		if (iCiv == iAmerica):
			utils.makeUnit(iGrenadier, iCiv, tPlot, 3)
			utils.makeUnit(iAmericanMinuteman, iCiv, tPlot, 3)
			utils.makeUnit(iCannon, iCiv, tPlot, 3)
		if iCiv == iArgentina:
			utils.makeUnit(iRifleman, iCiv, tPlot, 2)
			utils.makeUnit(iArgentineGrenadierCavalry, iCiv, tPlot, 4)
		elif iCiv == iBrazil:
			utils.makeUnit(iGrenadier, iCiv, tPlot, 2)
			utils.makeUnit(iRifleman, iCiv, tPlot, 3)
			utils.makeUnit(iCannon, iCiv, tPlot, 2)
		elif iCiv == iCanada:
			utils.makeUnit(iCavalry, iCiv, tPlot, 2)
			utils.makeUnit(iRifleman, iCiv, tPlot, 4)
			utils.makeUnit(iCannon, iCiv, tPlot, 2)


	def createStartingUnits( self, iCiv, tPlot ):
		if iCiv == iIndia:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iArcher, iCiv, tPlot, 1)
		if (iCiv == iGreece):
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iWarrior, iCiv, tPlot, 2)
			utils.makeUnit(iGreekHoplite, iCiv, tPlot, 1) #3
			pGreece.initUnit(iGreekHoplite, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			pGreece.initUnit(iGreekHoplite, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if (tSeaPlot):
				pGreece.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iWarrior, iCiv, tSeaPlot, 1)
		if (iCiv == iPersia):
			utils.createSettlers(iCiv, 3)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 3)
			utils.makeUnit(iPersianImmortal, iCiv, tPlot, 4)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 2)
			utils.makeUnit(iWarElephant, iCiv, tPlot, 1)
		if (iCiv == iCarthage):
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iSpearman, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if (tSeaPlot):				
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 2)
				pCarthage.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iArcher, iCiv, tSeaPlot, 1)
				pCarthage.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pCarthage.initUnit(iTrireme, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ESCORT_SEA, DirectionTypes.DIRECTION_SOUTH)
		if iCiv == iPolynesia:
			tSeaPlot = (4, 19)
			utils.makeUnit(iSettler, iCiv, tPlot, 1)
			utils.makeUnit(iPolynesianWaka, iCiv, tSeaPlot, 1)
			utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
			utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
		if (iCiv == iRome):
			utils.createSettlers(iCiv, 3)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 3)
			utils.makeUnit(iRomanLegion, iCiv, tPlot, 4)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if (tSeaPlot):				
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
				pRome.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
				pRome.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
		if (iCiv == iJapan):
			utils.createSettlers(iCiv, 3)
			utils.createMissionaries(iCiv, 1)
			utils.makeUnit(iSwordsman, iJapan, tPlot, 2)
			utils.makeUnitAI(iArcher, iJapan, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iWorker, iJapan, tPlot, 2)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iJapan)
			if (tSeaPlot):				
				utils.makeUnit(iWorkboat, iJapan, tSeaPlot, 2)
			if utils.getHumanID() != iJapan:
				utils.makeUnit(iCrossbowman, iJapan, tPlot, 2)
				utils.makeUnit(iJapaneseSamurai, iJapan, tPlot, 3)
		if iCiv == iTamils:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iWarElephant, iCiv, tPlot, 1)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 1)
			if utils.getHumanID() != iTamils:
				utils.makeUnit(iHinduMissionary, iCiv, tPlot, 1)
				utils.makeUnit(iWarElephant, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iTamils)
			if (tSeaPlot):
				utils.makeUnit(iWorkboat, iTamils, tSeaPlot, 1)
				utils.makeUnit(iGalley, iTamils, tSeaPlot, 1)
				utils.makeUnit(iSettler, iTamils, tSeaPlot, 1)
				utils.makeUnit(iArcher, iTamils, tSeaPlot, 1)
		if (iCiv == iEthiopia):
			utils.createSettlers(iCiv, 2)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 1)
			utils.makeUnit(iAxeman, iCiv, tPlot, 1)
			tSeaPlot = (74, 29)
			if (tSeaPlot):				
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
				utils.makeUnit(iTrireme, iCiv, tSeaPlot, 1)
		if (iCiv == iKorea):
			utils.createSettlers(iCiv, 1)
			utils.createMissionaries(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 3)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 1)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 1)
			if utils.getHumanID() != iKorea:
				utils.makeUnit(iSpearman, iCiv, tPlot, 2)
				utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
		if (iCiv == iMaya):
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iMayanHolkan, iCiv, tPlot, 2)
		if (iCiv == iByzantium):
			utils.makeUnit(iRomanLegion, iCiv, tPlot, 4)
			utils.makeUnit(iSpearman, iCiv, tPlot, 2)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.createSettlers(iCiv, 4)
			utils.createMissionaries(iCiv, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iByzantium)
			if tSeaPlot:
				utils.makeUnit(iGalley, iByzantium, tSeaPlot, 2)
				utils.makeUnit(iTrireme, iByzantium, tSeaPlot, 2)
				if utils.getScenario() == i3000BC:
					utils.makeUnit(iWorkboat, iByzantium, tSeaPlot, 1)
		if (iCiv == iVikings):
			utils.createSettlers(iCiv, 2)
			utils.makeUnitAI(iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 4)
			utils.makeUnit(iAxeman, iCiv, tPlot, 2)
			utils.makeUnit(iScout, iCiv, tPlot, 1)
			pVikings.initUnit(iSwordsman, tPlot[0], tPlot[1], UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if (tSeaPlot):				
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
				pVikings.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iLongbowman, iCiv, tSeaPlot, 1)
				pVikings.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_EXPLORE_SEA, DirectionTypes.DIRECTION_SOUTH)	   
				pVikings.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_EXPLORE_SEA, DirectionTypes.DIRECTION_SOUTH)	
		if (iCiv == iArabia):
			utils.createSettlers(iCiv, 2)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iArabianCamelArcher, iCiv, tPlot, 2)
			utils.makeUnit(iWorker, iCiv, tPlot, 1)    
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
		if iCiv == iTibet:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iTibetanKhampa, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 1)
		if (iCiv == iKhmer):
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnitAI(iKhmerBallistaElephant, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
			utils.createMissionaries(iCiv, 1)
			utils.createMissionaries(iCiv, 1, iBuddhism)
			tSeaPlot = self.findSeaPlots(tPlot, 2, iCiv)
			if (tSeaPlot):				
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
				pKhmer.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iArcher, iCiv, tSeaPlot, 1)
		if (iCiv == iIndonesia):
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iArcher, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.createMissionaries(iCiv, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if (tSeaPlot):
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
				utils.makeUnit(iTrireme, iCiv, tSeaPlot, 1)
				pIndonesia.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				pIndonesia.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iArcher, iCiv, tSeaPlot, 1)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iArcher, iCiv, tSeaPlot, 1)
		if iCiv == iMoors:
			utils.createSettlers(iCiv, 2)
			utils.makeUnitAI(iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iSpearman, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 1)
			utils.createMissionaries(iCiv, 2)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iGalley, iCiv, tSeaPlot, 1)
				utils.makeUnit(iTrireme, iCiv, tSeaPlot, 1)
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
			if utils.getHumanID() in [iSpain, iMoors]:
				utils.makeUnitAI(iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
		if (iCiv == iSpain):
			iSpanishSettlers = 2
			if utils.getHumanID() != iSpain: iSpanishSettlers = 3
			utils.createSettlers(iCiv, iSpanishSettlers)
			utils.makeUnit(iLongbowman, iCiv, tPlot, 1)
			utils.makeUnitAI(iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 4)
			if self.getPlayerEnabled(iMoors):
				if utils.getHumanID() != iMoors:
					utils.makeUnit(iKnight, iCiv, tPlot, 2)
			else:
				utils.makeUnit(iSettler, iCiv, tPlot, 1)
			if utils.getHumanID() != iSpain:
				utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 1)
			if utils.getScenario() == i600AD: #late start condition
				utils.makeUnit(iWorker, iCiv, tPlot, 1) #there is no carthaginian city in Iberia and Portugal may found 2 cities otherwise (a settler is too much)
		if (iCiv == iFrance):
			utils.createSettlers(iCiv, 3)
			utils.makeUnitAI(iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 4)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iAxeman, iCiv, tPlot, 3)
			utils.createMissionaries(iCiv, 1)
		if (iCiv == iEngland):
			utils.createSettlers(iCiv, 3)
			utils.makeUnitAI(iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 3)
			if utils.getHumanID() != iEngland:
				utils.makeUnit(iHeavySwordsman, iCiv, tPlot, 3)
			utils.createMissionaries(iCiv, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if (tSeaPlot):				
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 2)
				pEngland.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tPlot, 1)
				utils.makeUnit(iLongbowman, iCiv, tPlot, 1)
				utils.makeUnit(iGalley, iCiv, tSeaPlot, 2)
		if (iCiv == iHolyRome):			
			utils.createSettlers(iCiv, 3)
			utils.makeUnitAI(iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 3)
			utils.makeUnitAI(iSwordsman, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
			utils.makeUnitAI(iKnight, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
			utils.makeUnitAI(iCatapult, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 4)
			utils.createMissionaries(iCiv, 1)
		if (iCiv == iRussia):
			utils.createSettlers(iCiv, 4)
			utils.makeUnitAI(iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iSwordsman, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 3)
		if (iCiv == iHolland):
			utils.createSettlers(iCiv, 2)
			utils.makeUnit(iMusketman, iCiv, tPlot, 6)
			utils.makeUnit(iBombard, iCiv, tPlot, 2)
			utils.makeUnit(iPikeman, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if (tSeaPlot):				
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 2)
				pNetherlands.initUnit(iDutchEastIndiaman, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iLongbowman, iCiv, tSeaPlot, 1)
				pNetherlands.initUnit(iDutchEastIndiaman, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iLongbowman, iCiv, tSeaPlot, 1)
				utils.makeUnit(iCaravel, iCiv, tSeaPlot, 2)
		if (iCiv == iMali):
			utils.createSettlers(iCiv, 3)
			utils.makeUnit(iMandeSkirmisher, iCiv, tPlot, 5)
			utils.createMissionaries(iCiv, 1)
		if iCiv == iPoland:
			iNumSettlers = 1
			if utils.getHumanID() == iPoland: iNumSettlers = 2
			utils.createSettlers(iCiv, iNumSettlers)
			utils.makeUnitAI(iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iHeavySwordsman, iCiv, tPlot, 1)
			if utils.getHumanID() != iPoland:
				utils.makeUnit(iPikeman, iCiv, tPlot, 2)
			utils.makeUnit(iKnight, iCiv, tPlot, 1)
			utils.createMissionaries(iCiv, 1)
		if (iCiv == iTurkey):
			utils.makeUnit(iLongbowman, iCiv, tPlot, 2)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iKnight, iCiv, tPlot, 3)
			utils.makeUnit(iOttomanJanissary, iCiv, tPlot, 2)
			utils.makeUnit(iBombard, iCiv, tPlot, 4)
			utils.makeUnit(iTrebuchet, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 3)
			if utils.getHumanID() != iTurkey:
				utils.makeUnit(iBombard, iCiv, tPlot, 4)
				utils.makeUnit(iOttomanJanissary, iCiv, tPlot, 5)
				utils.makeUnit(iKnight, iCiv, tPlot, 4)
		if (iCiv == iPortugal):
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iPikeman, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if (tSeaPlot):				
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 2)
				pPortugal.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tPlot, 1)
				utils.makeUnit(iLongbowman, iCiv, tPlot, 1)
				utils.makeUnit(iGalley, iCiv, tSeaPlot, 1)
		if (iCiv == iInca):
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iIncanAucac, iCiv, tPlot, 4)
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			if utils.getHumanID() != iInca:
				utils.makeUnit(iSettler, iCiv, tPlot, 1)
		if iCiv == iItaly:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 3)
			utils.makeUnit(iPikeman, iCiv, tPlot, 2)
			utils.makeUnit(iTrebuchet, iCiv, tPlot, 3)
			utils.createMissionaries(iCiv, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if (tSeaPlot):
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 2)
				utils.makeUnit(iGalley, iCiv, tSeaPlot, 1)
				utils.makeUnit(iTrireme, iCiv, tSeaPlot, 1)
		if (iCiv == iMongolia):
			utils.createSettlers(iCiv, 3)
			utils.makeUnit(iLongbowman, iCiv, tPlot, 3)
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 2)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 2) 
			utils.makeUnitAI(iMongolianKeshik, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 6)
			if utils.getHumanID() != iMongolia: 
				utils.makeUnitAI(iMongolianKeshik, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 4)
				utils.makeUnitAI(iMongolianKeshik, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
				utils.makeUnitAI(iMongolianKeshik, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
				utils.makeUnitAI(iBombard, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
				utils.makeUnitAI(iBombard, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
				utils.makeUnitAI(iHeavySwordsman, iCiv, tPlot, UnitAITypes.UNITAI_COUNTER, 2)
				utils.makeUnitAI(iScout, iCiv, tPlot, UnitAITypes.UNITAI_EXPLORE, 2)
			utils.makeUnit(iBombard, iCiv, tPlot, 3)
			if utils.getHumanID() != iMongolia:
				utils.makeUnitAI(iLongbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
		if (iCiv == iAztecs):
			utils.createSettlers(iCiv, 2)
			utils.makeUnit(iAztecJaguar, iCiv, tPlot, 4)
			utils.makeUnit(iArcher, iCiv, tPlot, 4)
		if iCiv == iMughals:
			utils.createSettlers(iCiv, 3)
			utils.makeUnit(iMughalSiegeElephant, iCiv, tPlot, 3)
			utils.makeUnit(iMusketman, iCiv, tPlot, 4)
			utils.makeUnit(iHorseArcher, iCiv, tPlot, 2)
			utils.createMissionaries(iCiv, 1)
			if utils.getHumanID() == iMughals:
				utils.makeUnit(iIslamicMissionary, iCiv, tPlot, 3)
		if iCiv == iThailand:
			utils.createSettlers(iCiv, 1)
			utils.createMissionaries(iCiv, 1)
			utils.makeUnit(iPikeman, iCiv, tPlot, 3)
			utils.makeUnit(iThaiChangSuek, iCiv, tPlot, 2)
		if iCiv == iCongo:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iArcher, iCiv, tPlot, 2)
			utils.makeUnit(iCongolesePombos, iCiv, tPlot, 2)
		if iCiv == iGermany:
			utils.createSettlers(iCiv, 4)
			utils.createMissionaries(iCiv, 2)
			utils.makeUnit(iRifleman, iCiv, tPlot, 3, "", 2)
			utils.makeUnitAI(iRifleman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 2)
			utils.makeUnit(iCannon, iCiv, tPlot, 3, "", 2)
			if utils.getHumanID() != iGermany:
				utils.makeUnit(iRifleman, iCiv, tPlot, 10, "", 2)
				utils.makeUnit(iCannon, iCiv, tPlot, 5, "", 2)
		if (iCiv == iAmerica):
			utils.createSettlers(iCiv, 8)
			utils.makeUnit(iGrenadier, iCiv, tPlot, 2)
			utils.makeUnit(iAmericanMinuteman, iCiv, tPlot, 4)
			utils.makeUnit(iCannon, iCiv, tPlot, 2)
			self.addMissionary(iCiv, (23, 40), (33, 52), tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if (tSeaPlot):  
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 2)
				utils.makeUnit(iGalleon, iCiv, tSeaPlot, 2)
				utils.makeUnit(iFrigate, iCiv, tSeaPlot, 1)
			if utils.getHumanID() != iAmerica:
				utils.makeUnitAI(iAmericanMinuteman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
		if iCiv == iArgentina:
			utils.createSettlers(iCiv, 2)
			utils.makeUnit(iRifleman, iCiv, tPlot, 3, "", 2)
			utils.makeUnit(iArgentineGrenadierCavalry, iCiv, tPlot, 3, "", 2)
			utils.makeUnit(iCannon, iCiv, tPlot, 2, "", 2)
			tSeaPlot = self.findSeaPlots(tPlot, 2, iCiv)
			if tSeaPlot:
				utils.makeUnit(iGalleon, iCiv, tSeaPlot, 1)
				utils.makeUnit(iFrigate, iCiv, tSeaPlot, 2)
			if utils.getHumanID() != iArgentina:
				utils.makeUnitAI(iRifleman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
				utils.makeUnit(iRifleman, iCiv, tPlot, 2, "", 2)
				utils.makeUnit(iArgentineGrenadierCavalry, iCiv, tPlot, 2, "", 2)
				utils.makeUnit(iCannon, iCiv, tPlot, 2, "", 2)
		if iCiv == iBrazil:
			utils.createSettlers(iCiv, 5)
			utils.makeUnit(iGrenadier, iCiv, tPlot, 3)
			utils.makeUnit(iRifleman, iCiv, tPlot, 3)
			utils.makeUnit(iCannon, iCiv, tPlot, 2)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 2)
				utils.makeUnit(iGalleon, iCiv, tSeaPlot, 2)
				utils.makeUnit(iFrigate, iCiv, tSeaPlot, 3)
			if utils.getHumanID() != iBrazil:
				utils.makeUnitAI(iRifleman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
		if iCiv == iCanada:
			utils.createSettlers(iCiv, 5)
			utils.makeUnit(iCavalry, iCiv, tPlot, 3)
			utils.makeUnit(iRifleman, iCiv, tPlot, 5)
				
		# Leoreth: start wars on spawn when the spawn actually happens
		self.startWarsOnSpawn(iCiv)

	def createRespawnUnits(self, iCiv, tPlot):
		if (iCiv == iRome):
			utils.makeUnit(iCrossbowman, iCiv, tPlot, 5)
			utils.makeUnit(iPikeman, iCiv, tPlot, 3)
			utils.makeUnit(iTrebuchet, iCiv, tPlot, 4)
		if (iCiv == iPersia):
			utils.makeUnit(iIranianQizilbash, iCiv, tPlot, 6)
			utils.makeUnit(iBombard, iCiv, tPlot, 3)
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
			if utils.getHumanID() != iCiv:
				utils.makeUnit(iIranianQizilbash, iCiv, tPlot, 6)
				utils.makeUnit(iBombard, iCiv, tPlot, 3)
		if (iCiv == iIndia):
			utils.makeUnit(iCuirassier, iCiv, tPlot, 3)
			utils.makeUnit(iMusketman, iCiv, tPlot, 8)
			utils.makeUnit(iBombard, iCiv, tPlot, 5)
			utils.makeUnit(iWorker, iCiv, tPlot, 3)			
		if iCiv == iAztecs:
			utils.makeUnit(iMexicanRurales, iCiv, tPlot, 4, "", 2)
			utils.makeUnit(iRifleman, iCiv, tPlot, 5, "", 2)
			utils.makeUnit(iGrenadier, iCiv, tPlot, 2, "", 2)
			utils.makeUnit(iWorker, iCiv, tPlot, 3, "", 2)
		if iCiv == iMaya:
			utils.makeUnit(iRifleman, iCiv, tPlot, 5, "", 2)
			utils.makeUnit(iCannon, iCiv, tPlot, 5, "", 2)
			utils.makeUnit(iColombianAlbionLegion, iCiv, tPlot, 5, "", 2)
			utils.makeUnit(iWorker, iCiv, tPlot, 3, "", 2)
			tSeaPlot = self.findSeaPlots(tPlot, 3, iCiv)
			if tSeaPlot:
				utils.makeUnit(iGalleon, iCiv, tSeaPlot, 1)
				utils.makeUnit(iFrigate, iCiv, tSeaPlot, 1)

	def addMissionary(self, iCiv, tTopLeft, tBottomRight, tPlot, iNumber):
		lReligions = [0 for i in range(iNumReligions)]
		for x in range(tTopLeft[0], tBottomRight[0]+1):
			for y in range(tTopLeft[1], tBottomRight[1]+1):
				pCurrent = gc.getMap().plot( x, y )
				if (pCurrent.isCity()):
					city = pCurrent.getPlotCity() 
					iOwner = city.getOwner()
					if (iOwner != iCiv):
						iStateReligion = gc.getPlayer(iOwner).getStateReligion()
						if (iStateReligion >= 0 and iStateReligion < iNumReligions):
							lReligions[iStateReligion] += 1
		iMax = 0
		iWinnerReligion = -1
		for i in range(len(lReligions)): #so that Protestantism comes first
			iLoopReligion = i % iNumReligions
			if (lReligions[iLoopReligion] > iMax):
				iMax = lReligions[iLoopReligion]
				iWinnerReligion = iLoopReligion

		if (iWinnerReligion == -1):
			for iLoopCiv in range(iNumMajorPlayers):
				if (iLoopCiv != iCiv):
					if (gc.getMap().plot(tPlot[0], tPlot[1]).isRevealed(iLoopCiv, False)):
						iStateReligion = gc.getPlayer(iLoopCiv).getStateReligion()
						if (iStateReligion >= 0 and iStateReligion < iNumReligions):
							lReligions[iStateReligion] += 1

			for iLoopReligion in range(len(lReligions)): #so that Protestantism comes first
				iLoopReligion = i % iNumReligions
				if (lReligions[iLoopReligion] > iMax):
					iMax = lReligions[iLoopReligion]
					iWinnerReligion = iLoopReligion   

		if (iWinnerReligion != -1):
			utils.makeUnit(iMissionary + iWinnerReligion, iCiv, tPlot, iNumber)
			

				
	def createStartingWorkers( self, iCiv, tPlot ):
		if iCiv == iIndia:
			#utils.makeUnit(iIndianPunjabiWorker, iCiv, tPlot, 2)
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		if (iCiv == iGreece):
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		if (iCiv == iPersia):
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		if (iCiv == iCarthage):
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		if (iCiv == iRome):
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		if (iCiv == iJapan):
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		if iCiv == iTamils:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		if (iCiv == iEthiopia):
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		if (iCiv == iKorea):
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		if (iCiv == iMaya):
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		if (iCiv == iByzantium):
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
			#utils.makeUnit(iSettler, iCiv, tPlot, 1)
		if (iCiv == iVikings):
			utils.makeUnit(iWorker, iCiv, tPlot, 3)			      
		if (iCiv == iArabia):
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		if iCiv == iTibet:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		if (iCiv == iKhmer):
			utils.makeUnit(iWorker, iCiv, tPlot, 3)  
		if (iCiv == iIndonesia):
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		if iCiv == iMoors:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		if (iCiv == iSpain):
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		if (iCiv == iFrance):
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		if (iCiv == iEngland):
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		if (iCiv == iHolyRome):			
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		if (iCiv == iRussia):
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		if (iCiv == iNetherlands):
			utils.makeUnit(iWorker, iCiv, tPlot, 3) 
		if (iCiv == iMali):
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		if iCiv == iPoland:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
			if utils.getHumanID() != iPoland:
				iRand = gc.getGame().getSorenRandNum(5, 'Random city spot')
				if iRand == 0: tCityPlot = (65, 55) # Memel
				elif iRand == 1: tCityPlot = (65, 54) # Koenigsberg
				else: tCityPlot = (64, 54) # Gdansk
				utils.makeUnit(iSettler, iCiv, tCityPlot, 1)
				utils.makeUnit(iLongbowman, iCiv, tCityPlot, 1)
		if (iCiv == iTurkey):
			utils.makeUnit(iWorker, iCiv, tPlot, 4)
			#utils.makeUnit(iSettler, iCiv, tPlot, 3)
		if (iCiv == iPortugal):
			utils.makeUnit(iWorker, iCiv, tPlot, 3) 
		if (iCiv == iInca):
			utils.makeUnit(iWorker, iCiv, tPlot, 4)
		if iCiv == iItaly:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		if (iCiv == iMongolia):
			utils.makeUnit(iWorker, iCiv, tPlot, 4)
		if (iCiv == iAztecs):
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		if iCiv == iMughals:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		if iCiv == iThailand:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		if iCiv == iCongo:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		if iCiv == iGermany:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		if (iCiv == iAmerica):
			utils.makeUnit(iWorker, iCiv, tPlot, 4)
		if iCiv == iBrazil:
			utils.makeUnit(iBrazilianMadeireiro, iCiv, tPlot, 3)
		if iCiv == iArgentina:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		if iCiv == iCanada:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
			
	def create1700ADstartingUnits(self):
	
		# China
		tCapital = tBeijing
#		utils.makeUnit(iMusketman, iChina, tCapital, 12)
#		utils.makeUnit(iBombard, iChina, tCapital, 5)
		
		# India
		tCapital = tMumbai
#		utils.makeUnit(iMusketman, iIndia, tCapital, 8)
#		utils.makeUnit(iBombard, iIndia, tCapital, 5)
#		utils.makeUnit(iCuirassier, iIndia, tCapital, 3)
		
		# Tamils
		tCapital = tMysore
#		utils.makeUnit(iMusketman, iTamils, tCapital, 6)
#		utils.makeUnit(iBombard, iTamils, tCapital, 4)
		
		# Persia
		tCapital = tEsfahan
#		utils.makeUnit(iIranianQizilbash, iPersia, tCapital, 10)
#		utils.makeUnit(iBombard, iPersia, tCapital, 4)
		
		# Korea
		tCapital = Areas.getCapital(iKorea)
#		utils.makeUnit(iMusketman, iKorea, tCapital, 6)
#		utils.makeUnit(iBombard, iKorea, tCapital, 4)
		
		# Japan
		tCapital = Areas.getCapital(iJapan)
#		utils.makeUnit(iMusketman, iJapan, tCapital, 10)
#		utils.makeUnit(iBombard, iJapan, tCapital, 4)
		if utils.getHumanID() != iJapan:
			utils.makeUnit(iSettler, iJapan, tCapital, 1)
		
		# Vikings
		tCapital = tStockholm
#		utils.makeUnit(iMusketman, iVikings, tCapital, 8)
#		utils.makeUnit(iBombard, iVikings, tCapital, 4)
		
		# Spain
		tCapital = Areas.getCapital(iSpain)
#		utils.makeUnit(iMusketman, iSpain, tCapital, 6)
#		utils.makeUnit(iSpanishConquistador, iSpain, tCapital, 4)
3		utils.makeUnit(iBombard, iSpain, tCapital, 2)
		
		# France
		tCapital = Areas.getCapital(iFrance)
#		utils.makeUnit(iRifleman, iFrance, tCapital, 12)
#		utils.makeUnit(iCuirassier, iFrance, tCapital, 4)
#		utils.makeUnit(iFrenchHeavyCannon, iFrance, tCapital, 5)
		
		# England
		tCapital = Areas.getCapital(iEngland)
#		utils.makeUnit(iEnglishRedcoat, iEngland, tCapital, 8)
#		utils.makeUnit(iCannon, iEngland, tCapital, 4)
#		utils.makeUnit(iGalleon, iEngland, tCapital, 4)
		
		# Austria
		tCapital = tVienna
#		utils.makeUnit(iRifleman, iHolyRome, tCapital, 6)
#		utils.makeUnit(iCannon, iHolyRome, tCapital, 2)
		
		# Russia
		tCapital = Areas.getCapital(iRussia)
#		utils.makeUnit(iMusketman, iRussia, tCapital, 8)
#		utils.makeUnit(iCuirassier, iRussia, tCapital, 4)
#		utils.makeUnit(iBombard, iRussia, tCapital, 4)
		
		# Poland
		tCapital = tWarsaw
#		utils.makeUnit(iMusketman, iPoland, tCapital, 4)
#		utils.makeUnit(iPolishWingedHussar, iPoland, tCapital, 6)
#		utils.makeUnit(iBombard, iPoland, tCapital, 2)
		
		# Portugal
		tCapital = Areas.getCapital(iPortugal)
#		utils.makeUnit(iMusketman, iPortugal, tCapital, 6)
#		utils.makeUnit(iBombard, iPortugal, tCapital, 2)
#		utils.makeUnit(iGalleon, iPortugal, tCapital, 3)
		
		# Mughals
		tCapital = Areas.getCapital(iMughals)
#		utils.makeUnit(iMusketman, iMughals, tCapital, 5)
#		utils.makeUnit(iPikeman, iMughals, tCapital, 2)
#		utils.makeUnit(iMughalSiegeElephant, iMughals, tCapital, 2)
		
		# Turkey
		tCapital = tIstanbul
#		utils.makeUnit(iOttomanJanissary, iTurkey, tCapital, 10)
#		utils.makeUnit(iCuirassier, iTurkey, tCapital, 4)
#		utils.makeUnit(iBombard, iTurkey, tCapital, 5)
		
		# Thailand
		tCapital = Areas.getCapital(iThailand)
#		utils.makeUnit(iMusketman, iThailand, tCapital, 4)
#		utils.makeUnit(iPikeman, iThailand, tCapital, 2)
#		utils.makeUnit(iThaiChangSuek, iThailand, tCapital, 4)
#		utils.makeUnit(iBombard, iThailand, tCapital, 2)
		
		# Congo
		tCapital = Areas.getCapital(iCongo)
#		utils.makeUnit(iSettler, iCongo, tCapital, 1)
#		utils.makeUnit(iCongolesePombos, iCongo, tCapital, 6)
#		utils.makeUnit(iCatapult, iCongo, tCapital, 2)
#		utils.makeUnit(iLongbowman, iCongo, tCapital, 2)
#		utils.makeUnit(iNativeSlave, iCongo, tCapital, 5)
		
		# Netherlands
		tCapital = Areas.getCapital(iNetherlands)
#		utils.makeUnit(iRifleman, iNetherlands, tCapital, 5)
#		utils.makeUnit(iBombard, iNetherlands, tCapital, 2)
#		utils.makeUnit(iDutchEastIndiaman, iNetherlands, tCapital, 3)
		
		# Prussia
		tCapital = Areas.getCapital(iGermany)
#		utils.makeUnit(iRifleman, iGermany, tCapital, 8)
#		utils.makeUnit(iCannon, iGermany, tCapital, 3)
		
		for iPlayer in range(iNumPlayers):
			if tBirth[iPlayer] > utils.getScenarioStartYear() and utils.getHumanID() == iPlayer:
				utils.makeUnit(iSettler, iPlayer, Areas.getCapital(iPlayer), 1)
				utils.makeUnit(iWarrior, iPlayer, Areas.getCapital(iPlayer), 1)

	def create600ADstartingUnits( self ):

		tCapital = Areas.getCapital(iChina)
		utils.makeUnit(iSwordsman, iChina, tCapital, 2)
		utils.makeUnit(iArcher, iChina, tCapital, 1)
		utils.makeUnitAI(iSpearman, iChina, tCapital, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
		utils.makeUnit(iChineseChokonu, iChina, tCapital, 2)
		utils.makeUnit(iHorseArcher, iChina, tCapital, 1)
		utils.makeUnit(iWorker, iChina, tCapital, 2)
		
		tCapital = Areas.getCapital(iJapan)
#		utils.makeUnit(iSettler, iJapan, tCapital, 3)
#		utils.makeUnit(iBuddhistMissionary, iJapan, tCapital, 3)
#		utils.makeUnit(iSwordsman, iJapan, tCapital, 2)
#		utils.makeUnit(iArcher, iJapan, tCapital, 2)
		tSeaPlot = self.findSeaPlots(tCapital, 1, iJapan)
#		if (tSeaPlot):
#			utils.makeUnit(iWorkboat, iJapan, tSeaPlot, 2)

		if utils.getHumanID() != iJapan:
			utils.makeUnit(iCrossbowman, iJapan, tCapital, 2)
			utils.makeUnit(iJapaneseSamurai, iJapan, tCapital, 3)

		tCapital = Areas.getCapital(iVikings)
#		utils.makeUnit(iSettler, iVikings, tCapital, 1)
#		utils.makeUnit(iLongbowman, iVikings, tCapital, 2)
#		utils.makeUnit(iAxeman, iVikings, tCapital, 2)
#		utils.makeUnit(iScout, iVikings, tCapital, 1)
#		pVikings.initUnit(iSwordsman, tCapital[0], tCapital[1], UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)
#		utils.makeUnit(iSwordsman, iVikings, tCapital, 1)
		tSeaPlot = self.findSeaPlots(tCapital, 1, iVikings)
		if (tSeaPlot):
#			utils.makeUnit(iWorkboat, iVikings, tSeaPlot, 1)
#			pVikings.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
			if utils.getHumanID() == iVikings:
				utils.makeUnit(iSettler, iVikings, tSeaPlot, 1)
				utils.makeUnit(iLongbowman, iVikings, tSeaPlot, 1)
#			pVikings.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_EXPLORE_SEA, DirectionTypes.DIRECTION_SOUTH)
			#utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
#			pVikings.initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_EXPLORE_SEA, DirectionTypes.DIRECTION_SOUTH)
			#utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
		# start AI settler and garrison in Denmark and Sweden
		if utils.getHumanID() != iVikings:
			utils.makeUnit(iSettler, iVikings, (60, 56), 1)
			utils.makeUnit(iLongbowman, iVikings, (60, 56), 1)
			utils.makeUnit(iSettler, iVikings, (63, 59), 1)
			utils.makeUnit(iLongbowman, iVikings, (63, 59), 1)
		else:
			utils.makeUnit(iSettler, iVikings, tCapital, 1)
			utils.makeUnit(iLongbowman, iVikings, tCapital, 2)

		tCapital = Areas.getCapital(iByzantium)
#		utils.makeUnit(iSpearman, iByzantium, tCapital, 2)
#		utils.makeUnit(iArcher, iByzantium, tCapital, 3)
#		utils.makeUnit(iByzantineCataphract, iByzantium, tCapital, 1)
		tSeaPlot = self.findSeaPlots(tCapital, 1, iByzantium)
#		if tSeaPlot:
#			utils.makeUnit(iGalley, iByzantium, tSeaPlot, 2)
#			utils.makeUnit(iTrireme, iByzantium, tSeaPlot, 2)

		tCapital = Areas.getCapital(iKorea)
#		utils.makeUnit(iSettler, iKorea, tCapital, 2)
#		utils.makeUnit(iBuddhistMissionary, iKorea, tCapital, 1)
#		utils.makeUnit(iConfucianMissionary, iKorea, tCapital, 1)
#		utils.makeUnit(iArcher, iKorea, tCapital, 2)
#		utils.makeUnit(iAxeman, iKorea, tCapital, 3)
#		utils.makeUnit(iHorseArcher, iKorea, tCapital, 1)

		if utils.getHumanID() != iKorea:
			utils.makeUnit(iHeavySwordsman, iKorea, tCapital, 2)
			
		for iPlayer in range(iNumPlayers):
			if tBirth[iPlayer] > utils.getScenarioStartYear() and gc.getPlayer(iPlayer).isHuman():
				tCapital = Areas.getCapital(iPlayer)
				utils.makeUnit(iSettler, iPlayer, tCapital, 1)
				utils.makeUnit(iWarrior, iPlayer, tCapital, 1)


	def create4000BCstartingUnits(self):
	
		for iPlayer in range(iNumPlayers):
			tCapital = Areas.getCapital(iPlayer)
#			if tBirth[iPlayer] == utils.getScenarioStartYear() and iPlayer != iHarappa:
#				utils.makeUnit(iSettler, iPlayer, tCapital, 1)
#				utils.makeUnit(iWarrior, iPlayer, tCapital, 1)
			if iPlayer == iHarappa and (self.getPlayerEnabled(iPlayer) or gc.getPlayer(iPlayer).isHuman()):
				utils.makeUnit(iHarappanCityBuilder, iPlayer, tCapital, 1)
				utils.makeUnit(iWarrior, iPlayer, tCapital, 1)
#			elif gc.getPlayer(iPlayer).isHuman():
#				utils.makeUnit(iSettler, iPlayer, tCapital, 1)
#				utils.makeUnit(iWarrior, iPlayer, tCapital, 1)
			
		
		
	def assignTechs(self, iPlayer):
		Civilizations.initPlayerTechs(iPlayer)
			
		# Leoreth: Babylonian UHV: make them lose if they don't have Monarchy already
		if iPlayer == iPersia:
			vic.onTechAcquired(iPersia, iMonarchy)	
				
		sta.onCivSpawn(iPlayer)

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
					Baghdad.setHasRealBuilding(iPalace, True)
					utils.makeUnit(iArabianCamelArcher, iArabia, (77,40), 3)
					utils.makeUnit(iSwordsman, iArabia, (77,40), 2)
				utils.makeUnit(iArabianCamelArcher, iArabia, (77,40), 2)
				utils.makeUnit(iSwordsman, iArabia, (77,40), 2)
			else:
				if utils.getHumanID() != iArabia:
					Baghdad.setHasRealBuilding(iPalace, True)
					utils.makeUnit(iArabianCamelArcher, iArabia, (69,35), 3)
					utils.makeUnit(iSwordsman, iArabia, (69,35), 2)
				utils.makeUnit(iArabianCamelArcher, iArabia, (69,35), 2)
				utils.makeUnit(iSwordsman, iArabia, (69,35), 2)

			utils.makeUnit(iSettler, iArabia, (77,40), 1)
			utils.makeUnit(iSettler, iArabia, (69,35), 1)
			utils.makeUnit(iWorker, iArabia, (77,40), 1)
			utils.makeUnit(iWorker, iArabia, (69,35), 1)

		elif (bBaghdad and not bCairo):
			if utils.getHumanID() != iArabia:
				Baghdad.setHasRealBuilding(iPalace, True)
				utils.makeUnit(iArabianCamelArcher, iArabia, (77,40), 3)
				utils.makeUnit(iSwordsman, iArabia, (77,40), 2)
			utils.makeUnit(iSettler, iArabia, (77,40), 1)
			utils.makeUnit(iArabianCamelArcher, iArabia, (77,40), 2)
			utils.makeUnit(iSwordsman, iArabia, (77,40), 2)#

			utils.makeUnit(iSettler, iArabia, (77,40), 1)
			utils.makeUnit(iWorker, iArabia, (77,40), 1)
			utils.makeUnit(iWorker, iArabia, (75,33), 1)

		elif (not bBaghdad and bCairo):
			if utils.getHumanID() != iArabia:
				utils.makeUnit(iArabianCamelArcher, iArabia, (69,35), 3)
				utils.makeUnit(iSwordsman, iArabia, (69,35), 2)
			utils.makeUnit(iSettler, iArabia, (69,35), 1)
			utils.makeUnit(iArabianCamelArcher, iArabia, (69,35), 2)
			utils.makeUnit(iSwordsman, iArabia, (69,35), 2)

			utils.makeUnit(iSettler, iArabia, (69,35), 1)
			utils.makeUnit(iWorker, iArabia, (75,33), 1)
			utils.makeUnit(iWorker, iArabia, (69,35), 1)

		else:
			utils.makeUnit(iSettler, iArabia, (75,33), 2)
			utils.makeUnit(iWorker, iArabia, (75,33), 2)
			if utils.getHumanID() != iArabia:
				utils.makeUnit(iArabianCamelArcher, iArabia, (75,33), 3)
				utils.makeUnit(iSwordsman, iArabia, (75,33), 2)
			utils.makeUnit(iArabianCamelArcher, iArabia, (75,33), 2)
			utils.makeUnit(iSwordsman, iArabia, (75,33), 2)

		if utils.getHumanID() != iArabia and bBaghdad:
			utils.makeUnit(iSpearman, iArabia, (77, 40), 2)
			
	def germanSpawn(self):
		if sd.getStabilityLevel(iHolyRome) < iStabilityShaky: sd.setStabilityLevel(iHolyRome, iStabilityShaky)
			
		utils.setReborn(iHolyRome, True)
		
		dc.nameChange(iHolyRome)
		dc.adjectiveChange(iHolyRome)
		
	def holyRomanSpawn(self):
		plot = gc.getMap().plot(60, 56)
		if plot.isCity(): plot.getPlotCity().setCulture(iVikings, 5, True)
		
				
	def determineEnabledPlayers(self):
	
		iHuman = utils.getHumanID()
		
		iRand = gc.getDefineINT("PLAYER_OCCURRENCE_POLYNESIA")	
		if iRand <= 0:
			self.setPlayerEnabled(iPolynesia, False)
		elif gc.getGame().getSorenRandNum(iRand, 'Polynesia enabled?') != 0:
			self.setPlayerEnabled(iPolynesia, False)
			
		iRand = gc.getDefineINT("PLAYER_OCCURRENCE_HARAPPA")
		if iRand <= 0:
			self.setPlayerEnabled(iHarappa, False)
		elif gc.getGame().getSorenRandNum(iRand, 'Harappa enabled?') != 0:
			self.setPlayerEnabled(iHarappa, False)
		
		if iHuman != iIndia and iHuman != iIndonesia:
			iRand = gc.getDefineINT("PLAYER_OCCURRENCE_TAMILS")
			
			if iRand <= 0:
				self.setPlayerEnabled(iTamils, False)
			elif gc.getGame().getSorenRandNum(iRand, 'Tamils enabled?') != 0:
				self.setPlayerEnabled(iTamils, False)
				
		if iHuman != iChina and iHuman != iIndia and iHuman != iMughals:
			iRand = gc.getDefineINT("PLAYER_OCCURRENCE_TIBET")
			
			if iRand <= 0:
				self.setPlayerEnabled(iTibet, False)
			elif gc.getGame().getSorenRandNum(iRand, 'Tibet enabled?') != 0:
				self.setPlayerEnabled(iTibet, False)
				
		if iHuman != iSpain and iHuman != iMali:
			iRand = gc.getDefineINT("PLAYER_OCCURRENCE_MOORS")
			
			if iRand <= 0:
				self.setPlayerEnabled(iMoors, False)
			elif gc.getGame().getSorenRandNum(iRand, 'Moors enabled?') != 0:
				self.setPlayerEnabled(iMoors, False)
				
		if iHuman != iHolyRome and iHuman != iGermany and iHuman != iRussia:
			iRand = gc.getDefineINT("PLAYER_OCCURRENCE_POLAND")
			
			if iRand <= 0:
				self.setPlayerEnabled(iPoland, False)
			elif gc.getGame().getSorenRandNum(iRand, 'Poland enabled?') != 0:
				self.setPlayerEnabled(iPoland, False)
				
		if iHuman != iMali and iHuman != iPortugal:
			iRand = gc.getDefineINT("PLAYER_OCCURRENCE_CONGO")
			
			if iRand <= 0:
				self.setPlayerEnabled(iCongo, False)
			elif gc.getGame().getSorenRandNum(iRand, 'Congo enabled?') != 0:
				self.setPlayerEnabled(iCongo, False)
				
		if iHuman != iSpain:
			iRand = gc.getDefineINT("PLAYER_OCCURRENCE_ARGENTINA")
			
			if iRand <= 0:
				self.setPlayerEnabled(iArgentina, False)
			elif gc.getGame().getSorenRandNum(iRand, 'Argentina enabled?') != 0:
				self.setPlayerEnabled(iArgentina, False)
				
		if iHuman != iPortugal:
			iRand = gc.getDefineINT("PLAYER_OCCURRENCE_BRAZIL")
			
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
					if plot.getFeatureType() != iMud:
						if plot.getOwner() < 0:
							plotList.append((x,y))
		
		if not plotList:
			#utils.debugTextPopup('List empty: ' + str(tTL) + ' ' + str(tBR))
			return
		
		tPlot = utils.getRandomEntry(plotList)
		i, j = tPlot
		
		gc.getMap().plot(i, j).setImprovementType(iHut)
		
	def setStateReligion(self, iCiv):
		lCities = utils.getAreaCities(Areas.getCoreArea(iCiv))
		lReligions = [0 for i in range(iNumReligions)]
		
		for city in lCities:
			for iReligion in range(iNumReligions):
				if city.isHasReligion(iReligion): lReligions[iReligion] += 1
				
		iHighestEntry = utils.getHighestEntry(lReligions)
		
		if iHighestEntry > 0:
			gc.getPlayer(iCiv).setLastStateReligion(lReligions.index(iHighestEntry))