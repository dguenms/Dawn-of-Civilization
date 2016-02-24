# Rhye's and Fall of Civilization - Stored Data

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
import cPickle as pickle
import Consts as con

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

class StoredData:

	def __init__(self):
		self.setup()

	def load(self):
		"""Loads and unpickles script data"""
		self.scriptDict.update(pickle.loads(gc.getPlayer(con.iBarbarian).getScriptData()))

	def save(self):
		"""Pickles and saves script data"""
		gc.getPlayer(con.iBarbarian).setScriptData(pickle.dumps(self.scriptDict))

	def setup(self):
		"""Initialise the global script data dictionary for usage."""
		self.scriptDict = {      #------------RiseAndFall
				    'lTempEventList' : [],
				    'lNewCiv': [],
				    'iRespawnCiv' : -1,
				    'iNewCivFlip': -1,
				    'iOldCivFlip': -1,
				    'tTempTopLeft': -1,
				    'tTempBottomRight': -1,
				    'iSpawnWar': 0, #if 1, add units and declare war. If >=2, do nothing
				    'bAlreadySwitched': False,
				    'lColonistsAlreadyGiven': [0 for i in range(con.iNumPlayers)], #active players
				    'lAstronomyTurn': [1500 for i in range(con.iNumPlayers)], #active players
				    'lNumCities': [0 for i in range(con.iNumTotalPlayers)], #total players to contain Byzantium too
				    'lLastTurnAlive': [0 for i in range(con.iNumTotalPlayers)], #total players to contain Byzantium too
				    'lSpawnDelay': [0 for i in range(con.iNumPlayers)], #active players
				    'lFlipsDelay': [0 for i in range(con.iNumPlayers)],
				    'iBetrayalTurns': 0,
				    'lLatestRebellionTurn': [0 for i in range(con.iNumPlayers)],
				    'iRebelCiv': 0,
				    'lExileData': [-1, -1, -1, -1, -1],
				    'tTempFlippingCity': -1,
				    'lCheatersCheck': [0, -1],
				    'lBirthTurnModifier': [0 for i in range(con.iNumPlayers)],
				    'lDeleteMode': [-1, -1, -1], #first is a bool, the other values are capital coordinates
				    'lFirstContactConquerors': [0, 0, 0], #maya, inca, aztecs
				    'lFirstContactMongols': [0, 0, 0, 0, 0], #india, persia, byzantium, arabia, russia
				    'bCheatMode': False,
				    'tTempFlippingCity': (0, 0),
				    'tTradingCompanyConquerorsTargets': ([], [], [], [], []),
				    'iOttomanSpawnTurn': -1,
				    'lAnarchyTurns': [0 for i in range(con.iNumPlayers)],
				    'lResurrections': [0 for i in range(con.iNumPlayers)],
				    'lPlayerEnabled': [True for i in con.lSecondaryCivs],
				    'lCityFounded': [False for i in range(con.iNumMinorCities)],
				    'lTimedConquests' : [],
				     #------------Religions
				    'iSeed': -1,
				    'lReformationDecision': [-1 for i in range(con.iNumPlayers)],
				    #------------UP
				    'iImmigrationTimer': 0,
				    'iLatestFlipTurn': 0,
				    'lLatestRazeData': [-1, -1, -1, -1, -1],
				    'iRomanVictories': 0,
				    'lByzantineBribes': [],
				    #------------AIWars
				    'lAttackingCivsArray': [0 for i in range(con.iNumPlayers)], #original RFC had -1 here somewhere??
				    'iNextTurnAIWar': -1,
				    'lAggressionLevels': [0 for i in range(con.iNumPlayers)],
				    'lConquests' : [False for i in range(con.iNumConquests)],
				    #------------Congresses
				    'iGlobalWarAttacker': -1,
				    'iGlobalWarDefender': -1,
				    'iCongressTurns': 0,
				    'iCivsWithNationalism': 0,
				    'currentCongress': None,
				    #------------Plague
				    'lPlagueCountdown': [0 for i in range(con.iNumTotalPlayersB)], #total players + barbarians
				    'lGenericPlagueDates': [-1, -1, -1, -1],# -1],
				    'lFirstContactPlague': [False for i in range(con.iNumTotalPlayersB)], #total players + barbarians
				     #------------Victories
				    'lGoals': [[-1, -1, -1] for i in range(con.iNumPlayers)],
				    'lHistoricalGoldenAge' : [False for i in range(con.iNumPlayers)],
				    'bIgnoreAI': False,
				    
				    'lWonderBuilder': [-1 for i in range(con.iNumBuildings - con.iBeginWonders)],
				    'lReligionFounder': [-1 for i in range(con.iNumReligions)],
				    'lFirstDiscovered': [-1 for i in range(con.iNumTechs)],
				    'lFirstEntered': [-1 for i in range(con.iNumEras)],
				    'iFirstNewWorldColony': -1,
				    		    
				    'iChineseGoldenAgeTurns': 0,
				    'iKoreanSinks': 0,
				    'iTamilTradeGold': 0,
				    'iColombianTradeGold': 0,
				    'iVikingGold': 0,
				    'iMoorishGold': 0,
				    'iEnglishSinks': 0,
				    'iMongolRazes': 0,
				    'iAztecSlaves': 0,
				    'iCongoSlaveCounter': 0,
				    'iDutchColonies': 0,
				    'iArgentineGoldenAgeTurns': 0,
				    'iCanadianPeaceDeals': 0,
				    
				    'iPopeTurns': 0,
				    'iHinduGoldenAgeTurns': 0,
				    'iBuddhistPeaceTurns': 0,
				    'iBuddhistHappinessTurns': 0,
				    'iTaoistHealthTurns': 0,
				    'bPolytheismNeverReligion': True,
				    #------------Stability
				    'lStabilityLevels': [con.iStabilityShaky for i in range(con.iNumPlayers)],
				    'lTurnsToCollapse': [-1 for i in range(con.iNumPlayers)],
				    'lCrisisCountdown': [0 for i in range(con.iNumPlayers)],
				    'lLastStability' : [0 for i in range(con.iNumPlayers)],
				    'lLastDifference' : [0 for i in range(con.iNumPlayers)],
				    'lStabilityCategoryValues' : [[0, 0, 0, 0, 0] for i in range(con.iNumPlayers)],
				    'lNumPreviousCities' : [0 for i in range(con.iNumPlayers)],
				    'bCrisisImminent' : False,
				    'iHumanStability' : 0,
				    'iHumanRazePenalty' : 0,
				    'lBarbarianLosses' : [0 for i in range(con.iNumPlayers)],
				    'lPreviousCommerce' : [0 for i in range(con.iNumPlayers)],
				    'lEconomyTrend' : [[] for i in range(con.iNumPlayers)],
				    'lLastExpansionStability' : [0 for i in range(con.iNumPlayers)], 
				    'lHappinessTrend' : [[] for i in range(con.iNumPlayers)],
				    'lWarTrend' : [[[] for i in range(con.iNumPlayers)] for j in range(con.iNumPlayers)],
				    'lWarStartTurn' : [[0 for i in range(con.iNumPlayers)] for j in range(con.iNumPlayers)],
				    'dSecedingCities' : {},
				}
		self.save()
		
	# RISE AND FALL
	
	def timedConquest(self, iPlayer, x, y):
		self.scriptDict['lTimedConquests'].append((iPlayer, x, y))
		
	def getTimedConquests(self):
		return self.scriptDict['lTimedConquests']
		
	def resetTimedConquests(self):
		self.scriptDict['lTimedConquests'] = []
		
	# STABILITY
		
	def resetStability(self, iPlayer):
		self.setCrisisCountdown(iPlayer, 0)
		self.setLastStability(iPlayer, 0)
		self.setLastDifference(iPlayer, 0)
		for i in range(5): self.setStabilityCategoryValue(iPlayer, i, 0)
		self.setNumPreviousCities(iPlayer, 0)
		self.setBarbarianLosses(iPlayer, 0)
		self.setPreviousCommerce(iPlayer, 0)
		self.setEconomyTrend(iPlayer, [])
		self.setLastExpansionStability(iPlayer, 0)
		self.setHappinessTrend(iPlayer, [])
		for iLoopPlayer in range(con.iNumPlayers):
			self.setWarTrend(iPlayer, iLoopPlayer, [])
			self.setWarTrend(iLoopPlayer, iPlayer, [])
			self.setWarStartTurn(iPlayer, iLoopPlayer, 0)
			self.setWarStartTurn(iLoopPlayer, iPlayer, 0)
		
	def resetHumanStability(self):
		self.setCrisisImminent(False)
		self.setHumanStability(0)
		self.setHumanRazePenalty(0)
		
	def getStabilityLevel(self, iPlayer):
		return self.scriptDict['lStabilityLevels'][iPlayer]
		
	def setStabilityLevel(self, iPlayer, iStabilityLevel):
		self.scriptDict['lStabilityLevels'][iPlayer] = iStabilityLevel
		
	def getCrisisCountdown(self, iPlayer):
		return self.scriptDict['lCrisisCountdown'][iPlayer]
		
	def setCrisisCountdown(self, iPlayer, iNewValue):
		self.scriptDict['lCrisisCountdown'][iPlayer] = iNewValue
		
	def changeCrisisCountdown(self, iPlayer, iChange):
		self.scriptDict['lCrisisCountdown'][iPlayer] += iChange
		
	def getLastStability(self, iPlayer):
		return self.scriptDict['lLastStability'][iPlayer]
		
	def setLastStability(self, iPlayer, iNewValue):
		self.scriptDict['lLastStability'][iPlayer] = iNewValue	

	def getPreviousCommerce(self, iPlayer):
		return self.scriptDict['lPreviousCommerce'][iPlayer]
		
	def setPreviousCommerce(self, iPlayer, iNewValue):
		self.scriptDict['lPreviousCommerce'][iPlayer] = iNewValue
		
	def getEconomyTrend(self, iPlayer):
		return self.scriptDict['lEconomyTrend'][iPlayer]
		
	def pushEconomyTrend(self, iPlayer, iEntry):
		self.scriptDict['lEconomyTrend'][iPlayer].append(iEntry)
		if len(self.scriptDict['lEconomyTrend'][iPlayer]) > 10:
			self.scriptDict['lEconomyTrend'][iPlayer].pop(0)
			
	def setEconomyTrend(self, iPlayer, lNewValue):
		self.scriptDict['lEconomyTrend'][iPlayer] = lNewValue
		
	def getLastExpansionStability(self, iPlayer):
		return self.scriptDict['lLastExpansionStability'][iPlayer]
		
	def setLastExpansionStability(self, iPlayer, iNewValue):
		self.scriptDict['lLastExpansionStability'][iPlayer] = iNewValue
		
	def changeLastExpansionStability(self, iPlayer, iChange):
		self.scriptDict['lLastExpansionStability'][iPlayer] += iChange
		
	def getHappinessTrend(self, iPlayer):
		return self.scriptDict['lHappinessTrend'][iPlayer]
		
	def pushHappinessTrend(self, iPlayer, iEntry):
		self.scriptDict['lHappinessTrend'][iPlayer].append(iEntry)
		if len(self.scriptDict['lHappinessTrend'][iPlayer]) > 10:
			self.scriptDict['lHappinessTrend'][iPlayer].pop(0)
			
	def setHappinessTrend(self, iPlayer, lNewValue):
		self.scriptDict['lHappinessTrend'][iPlayer] = lNewValue
		
	def getLastDifference(self, iPlayer):
		return -self.scriptDict['lLastDifference'][iPlayer]
		
	def setLastDifference(self, iPlayer, iNewValue):
		self.scriptDict['lLastDifference'][iPlayer] = iNewValue
		
	def getStabilityCategoryValue(self, iPlayer, iCategory):
		return self.scriptDict['lStabilityCategoryValues'][iPlayer][iCategory]
		
	def setStabilityCategoryValue(self, iPlayer, iCategory, iNewValue):
		self.scriptDict['lStabilityCategoryValues'][iPlayer][iCategory] = iNewValue
		
	def getNumPreviousCities(self, iPlayer):
		return self.scriptDict['lNumPreviousCities'][iPlayer]
		
	def setNumPreviousCities(self, iPlayer, iNewValue):
		self.scriptDict['lNumPreviousCities'][iPlayer] = iNewValue
		
	def getRebelCiv(self):
		return self.scriptDict['iRebelCiv']
		
	def setRebelCiv(self, iNewValue):
		self.scriptDict['iRebelCiv'] = iNewValue
		
	def getTempFlippingCity(self):
		return self.scriptDict['tTempFlippingCity']
		
	def setTempFlippingCity(self, tNewValue):
		self.scriptDict['tTempFlippingCity'] = tNewValue
		
	def isCrisisImminent(self):
		return self.scriptDict['bCrisisImminent']
		
	def setCrisisImminent(self, bNewValue):
		self.scriptDict['bCrisisImminent'] = bNewValue

	def getHumanStability(self):
		return self.scriptDict['iHumanStability']
	
	def setHumanStability(self, iNewValue):
		self.scriptDict['iHumanStability'] = iNewValue
		
	def getWarTrend(self, iPlayer, iEnemy):
		return self.scriptDict['lWarTrend'][iPlayer][iEnemy]
		
	def getLastWarTrend(self, iPlayer, iEnemy):
		lTrend = self.scriptDict['lWarTrend'][iPlayer][iEnemy]
		for i in reversed(range(len(lTrend))):
			if lTrend[i] != 0: return lTrend[i]
		return 0
		
	def setWarTrend(self, iPlayer, iEnemy, lNewValue):
		self.scriptDict['lWarTrend'][iPlayer][iEnemy] = lNewValue
		
	def pushWarTrend(self, iPlayer, iEnemy, iEntry):
		self.scriptDict['lWarTrend'][iPlayer][iEnemy].append(iEntry)
		if len(self.scriptDict['lWarTrend'][iPlayer][iEnemy]) > 10:
			self.scriptDict['lWarTrend'][iPlayer][iEnemy].pop(0)
			
	def getWarStartTurn(self, iPlayer, iEnemy):
		return self.scriptDict['lWarStartTurn'][iPlayer][iEnemy]
		
	def setWarStartTurn(self, iPlayer, iEnemy, iNewValue):
		self.scriptDict['lWarStartTurn'][iPlayer][iEnemy] = iNewValue
		
	def getTurnsToCollapse(self, iPlayer):
		return self.scriptDict['lTurnsToCollapse'][iPlayer]
		
	def setTurnsToCollapse(self, iPlayer, iNewValue):
		self.scriptDict['lTurnsToCollapse'][iPlayer] = iNewValue
		
	def changeTurnsToCollapse(self, iPlayer, iChange):
		self.scriptDict['lTurnsToCollapse'][iPlayer] += iChange
		
	def getHumanRazePenalty(self):
		return self.scriptDict['iHumanRazePenalty']
		
	def setHumanRazePenalty(self, iNewValue):
		self.scriptDict['iHumanRazePenalty'] = iNewValue
		
	def changeHumanRazePenalty(self, iChange):
		self.scriptDict['iHumanRazePenalty'] += iChange
		
	def getBarbarianLosses(self, iPlayer):
		return self.scriptDict['lBarbarianLosses'][iPlayer]
		
	def setBarbarianLosses(self, iPlayer, iNewValue):
		self.scriptDict['lBarbarianLosses'][iPlayer] = iNewValue 
		
	def changeBarbarianLosses(self, iPlayer, iChange):
		self.scriptDict['lBarbarianLosses'][iPlayer] += iChange
		
	def getSecedingCities(self, iPlayer):
		if iPlayer not in self.scriptDict['dSecedingCities']: return []
		return [city for city in [gc.getPlayer(iPlayer).getCity(i) for i in self.scriptDict['dSecedingCities'][iPlayer]] if (city.getX(), city.getY()) != (-1, -1)]
	
	def setSecedingCities(self, iPlayer, lCities):
		self.scriptDict['dSecedingCities'][iPlayer] = [city.getID() for city in lCities]
		
	# AIWARS
		
	def getAggressionLevels(self):
		return self.scriptDict['lAggressionLevels']
		
	def changeAggressionLevel(self, iPlayer, iChange):
		self.scriptDict['lAggressionLevels'][iPlayer] += iChange
		
	def setAggressionLevel(self, iPlayer, iNewValue):
		self.scriptDict['lAggressionLevels'][iPlayer] = iNewValue
		
	def setConquest(self, iConquest, bNewValue):
		self.scriptDict['lConquests'][iConquest] = bNewValue
		
	def isConquest(self, iConquest):
		return self.scriptDict['lConquests'][iConquest]
		
	# BARBS
		
	def isMinorCityFounded(self, iCity):
		return self.scriptDict['lCityFounded'][iCity]
		
	def setMinorCityFounded(self, iCity, bNewValue):
		self.scriptDict['lCityFounded'][iCity] = bNewValue
		
	# UNIQUE POWERS
		
	def getByzantineBribes(self):
		return self.scriptDict['lByzantineBribes']
		
	def setByzantineBribes(self, lBribes):
		self.scriptDict['lByzantineBribes'] = lBribes
		
	# CONGRESSES
	
	def getGlobalWarAttacker(self):
		return self.scriptDict['iGlobalWarAttacker']
		
	def setGlobalWarAttacker(self, iNewValue):
		self.scriptDict['iGlobalWarAttacker'] = iNewValue
		
	def getGlobalWarDefender(self):
		return self.scriptDict['iGlobalWarDefender']
		
	def setGlobalWarDefender(self, iNewValue):
		self.scriptDict['iGlobalWarDefender'] = iNewValue
		
	def getCongressTurns(self):
		return self.scriptDict['iCongressTurns']
		
	def setCongressTurns(self, iNewValue):
		self.scriptDict['iCongressTurns'] = iNewValue
		
	def changeCongressTurns(self, iChange):
		self.scriptDict['iCongressTurns'] += iChange
		
	def getCurrentCongress(self):
		return self.scriptDict['currentCongress']
		
	def setCurrentCongress(self, congress):
		self.scriptDict['currentCongress'] = congress
		
	# VICTORY
	
	def getGoal(self, iPlayer, iGoal):
		return self.scriptDict['lGoals'][iPlayer][iGoal]
		
	def setGoal(self, iPlayer, iGoal, iNewValue):
		if iNewValue == 1 and self.getGoal(iPlayer, iGoal) == 0: return
		self.scriptDict['lGoals'][iPlayer][iGoal] = iNewValue
			
	def isHistoricalGoldenAge(self, iPlayer):
		return self.scriptDict['lHistoricalGoldenAge'][iPlayer]
		
	def setHistoricalGoldenAge(self, iPlayer, bNewValue):
		self.scriptDict['lHistoricalGoldenAge'][iPlayer] = bNewValue
			
	def isIgnoreAI(self):
		return self.scriptDict['bIgnoreAI']
		
	def setIgnoreAI(self, bNewValue):
		self.scriptDict['bIgnoreAI'] = bNewValue
		
			
	def getWonderBuilder(self, iWonder):
		if iWonder < con.iBeginWonders: return -1
		else: iWonder -= con.iBeginWonders
		return self.scriptDict['lWonderBuilder'][iWonder]
		
	def setWonderBuilder(self, iWonder, iPlayer):
		if iWonder >= con.iBeginWonders:
			iWonder -= con.iBeginWonders
			self.scriptDict['lWonderBuilder'][iWonder] = iPlayer
			
	def getReligionFounder(self, iReligion):
		return self.scriptDict['lReligionFounder'][iReligion]
		
	def setReligionFounder(self, iReligion, iPlayer):
		self.scriptDict['lReligionFounder'][iReligion] = iPlayer
		
	def getFirstDiscovered(self, iTech):
		return self.scriptDict['lFirstDiscovered'][iTech]
		
	def setFirstDiscovered(self, iTech, iPlayer):
		self.scriptDict['lFirstDiscovered'][iTech] = iPlayer
		
	def getFirstEntered(self, iEra):
		return self.scriptDict['lFirstEntered'][iEra]
		
	def setFirstEntered(self, iEra, iPlayer):
		self.scriptDict['lFirstEntered'][iEra] = iPlayer
			
			
	def getCongoSlaveCounter(self):
		return self.scriptDict['iCongoSlaveCounter']
	
	def setCongoSlaveCounter(self, iNewValue):
		self.scriptDict['iCongoSlaveCounter'] = iNewValue
		
	def changeCongoSlaveCounter(self, iChange):
		self.scriptDict['iCongoSlaveCounter'] += iChange
		
	def getDutchColonies(self):
		return self.scriptDict['iDutchColonies']
		
	def setDutchColonies(self, iNewValue):
		self.scriptDict['iDutchColonies'] = iNewValue
		
	def changeDutchColonies(self, iChange):
		self.scriptDict['iDutchColonies'] += iChange
		
	def getChineseGoldenAgeTurns(self):
		return self.scriptDict['iChineseGoldenAgeTurns']
		
	def changeChineseGoldenAgeTurns(self, iChange):
		self.scriptDict['iChineseGoldenAgeTurns'] += iChange
		
	def getTamilTradeGold(self):
		return self.scriptDict['iTamilTradeGold']
		
	def changeTamilTradeGold(self, iChange):
		self.scriptDict['iTamilTradeGold'] += iChange
		
	def getKoreanSinks(self):
		return self.scriptDict['iKoreanSinks']
		
	def changeKoreanSinks(self, iChange):
		self.scriptDict['iKoreanSinks'] += iChange
		
	def getColombianTradeGold(self):
		return self.scriptDict['iColombianTradeGold']
		
	def changeColombianTradeGold(self, iChange):
		self.scriptDict['iColombianTradeGold'] += iChange
		
	def getVikingGold(self):
		return self.scriptDict['iVikingGold']
		
	def changeVikingGold(self, iChange):
		self.scriptDict['iVikingGold'] += iChange
		
	def getMoorishGold(self):
		return self.scriptDict['iMoorishGold']
		
	def changeMoorishGold(self, iChange):
		self.scriptDict['iMoorishGold'] += iChange
		
	def getEnglishSinks(self):
		return self.scriptDict['iEnglishSinks']
		
	def changeEnglishSinks(self, iChange):
		self.scriptDict['iEnglishSinks'] += iChange
		
	def getMongolRazes(self):
		return self.scriptDict['iMongolRazes']
		
	def changeMongolRazes(self, iChange):
		self.scriptDict['iMongolRazes'] += iChange
		
	def getAztecSlaves(self):
		return self.scriptDict['iAztecSlaves']
		
	def changeAztecSlaves(self, iChange):
		self.scriptDict['iAztecSlaves'] += iChange
		
	def getArgentineGoldenAgeTurns(self):
		return self.scriptDict['iArgentineGoldenAgeTurns']
		
	def changeArgentineGoldenAgeTurns(self, iChange):
		self.scriptDict['iArgentineGoldenAgeTurns'] += iChange
		
	def getCanadianPeaceDeals(self):
		return self.scriptDict['iCanadianPeaceDeals']
		
	def changeCanadianPeaceDeals(self, iChange):
		self.scriptDict['iCanadianPeaceDeals'] += iChange
		
	# religious victory
		
	def getPopeTurns(self):
		return self.scriptDict['iPopeTurns']
		
	def changePopeTurns(self, iChange):
		self.scriptDict['iPopeTurns'] += iChange
		
	def getHinduGoldenAgeTurns(self):
		return self.scriptDict['iHinduGoldenAgeTurns']
		
	def changeHinduGoldenAgeTurns(self, iChange):
		self.scriptDict['iHinduGoldenAgeTurns'] += iChange
		
	def getBuddhistPeaceTurns(self):
		return self.scriptDict['iBuddhistPeaceTurns']
		
	def changeBuddhistPeaceTurns(self, iChange):
		self.scriptDict['iBuddhistPeaceTurns'] += iChange
		
	def getBuddhistHappinessTurns(self):
		return self.scriptDict['iBuddhistHappinessTurns']
		
	def changeBuddhistHappinessTurns(self, iChange):
		self.scriptDict['iBuddhistHappinessTurns'] += iChange
		
	def getTaoistHealthTurns(self):
		return self.scriptDict['iTaoistHealthTurns']
		
	def changeTaoistHealthTurns(self, iChange):
		self.scriptDict['iTaoistHealthTurns'] += iChange
		
	def isPolytheismNeverReligion(self):
		return self.scriptDict['bPolytheismNeverReligion']
		
	def setPolytheismNeverReligion(self, bNewValue):
		self.scriptDict['bPolytheismNeverReligion'] = bNewValue
		
	def getFirstNewWorldColony(self):
		return self.scriptDict['iFirstNewWorldColony']
		
	def setFirstNewWorldColony(self, iNewValue):
		self.scriptDict['iFirstNewWorldColony'] = iNewValue
		
	def isFirstWorldColonized(self):
		return self.getFirstNewWorldColony() != -1
		
	# DYNAMIC NAMES
	
	def getAnarchyTurns(self, iPlayer):
		if iPlayer >= con.iNumPlayers: return 0
		return sd.scriptDict['lAnarchyTurns'][iPlayer]
		
	def changeAnarchyTurns(self, iPlayer, iChange):
		if iPlayer < con.iNumPlayers:
			sd.scriptDict['lAnarchyTurns'][iPlayer] += iChange
		
	def getResurrections(self, iPlayer):
		if iPlayer >= con.iNumPlayers: return 0
		return sd.scriptDict['lResurrections'][iPlayer]
		
	def changeResurrections(self, iPlayer, iChange):
		if iPlayer < con.iNumPlayers:
			sd.scriptDict['lResurrections'][iPlayer] += iChange
		
# All modules import the following single instance, not the class

sd = StoredData()