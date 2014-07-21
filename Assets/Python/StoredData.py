# Rhye's and Fall of Civilization - Stored Data

from CvPythonExtensions import *
import CvUtil
import PyHelpers  
import cPickle as pickle
import Consts as con
from WarStatus import WarStatus

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

class StoredData:

        def __init__(self):
                self.setup()

        def load(self):
                """Loads and unpickles script data"""
                self.scriptDict = pickle.loads(gc.getPlayer(con.iBarbarian).getScriptData())
		#self.scriptDict = dict(BugData.getTable("StoredData").data)

        def save(self):
                """Pickles and saves script data"""
		gc.getPlayer(con.iBarbarian).setScriptData(pickle.dumps(self.scriptDict))
		#BugData.getTable("StoredData").setData(self.scriptDict)

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
				    'bIgnoreAI': False,
                                    'lReligionFounded': [-1, -1, -1, -1, -1, -1, -1, -1],
                                    'iEnslavedUnits': 0,
                                    'iRazedByMongols': 0,
                                    'lEnglishEras': [-1, -1],
                                    'lGreekTechs': [-1, -1, -1],
                                    'lNewWorld': [-1, -1], #first founded; circumnavigated (still unused)
                                    'iNumSinks': 0,
                                    'lBabylonianTechs': [-1, -1, -1],                                    
                                    #'iMediterraneanColonies': 0,
                                    'iPortugueseColonies': 0,
                                    'iFrenchColonies': 0,
                                    'lWondersBuilt': [0 for i in range(con.iNumPlayers)],
                                    'l2OutOf3': [False for i in range(con.iNumPlayers)],
				    'iChineseGoldenAges' : 0,
				    'lItalianTechs': [-1, -1, -1, -1, -1, -1],
				    'iNumKoreanSinks': 0,
				    'iNumGenerals': 0,
				    'iTechsStolen': 0,
				    'lChineseTechs': [-1, -1, -1, -1],
				    'iEthiopianControl' : -1,
				    'iVikingGold' : 0,
				    'lRussianProjects' : [-1, -1, -1],
				    'iDutchColonies' : 0,
				    'iNumTamilSinks' : 0,
				    'iTamilTradeGold' : 0,
				    'lRomanTechs' : [-1, -1, -1],
				    'iCongoSlaveCounter' : 0,
				    'bMaliGold' : False,
				    'iColombianTradeGold' : 0,
				    'lProtestantTechs' : [-1, -1, -1],
				    'iPopeTurns' : 0,
				    'iHinduGoldenAgeTurns' : 0,
				    'iBuddhistPeaceTurns' : 0,
				    'iBuddhistHappinessTurns' : 0,
				    'bPolytheismNeverReligion' : True,
				    'iFirstIndustrial' : -1,
				    'iFirstModern' : -1,
				    'iMoorishGold' : 0,
				    'iTaoistHealthTurns' : 0,
				    'iArgentineGoldenAgeTurns' : 0,
                                    #------------Stability
				    'lStabilityLevels': [con.iStabilityShaky for i in range(con.iNumPlayers)],
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
				    'lEconomyStability' : [0 for i in range(con.iNumPlayers)],
				    'lLastExpansionStability' : [0 for i in range(con.iNumPlayers)], 
				    'lHappinessStability' : [0 for i in range(con.iNumPlayers)],
				    'lWarStatus' : [{} for i in range(con.iNumPlayers)],
				}
                self.save()
		
		
	def getStabilityLevel(self, iPlayer):
		return self.scriptDict['lStabilityLevels'][iPlayer]
		
	def setStabilityLevel(self, iPlayer, iStabilityLevel):
		self.scriptDict['lStabilityLevels'][iPlayer] = iStabilityLevel
		
	def getCrisisCountdown(self, iPlayer):
		return self.scriptDict['lCrisisCountdown'][iPlayer]
		
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
		
	def getEconomyStability(self, iPlayer):
		return self.scriptDict['lEconomyStability'][iPlayer]
		
	def setEconomyStability(self, iPlayer, iNewValue):
		self.scriptDict['lEconomyStability'][iPlayer] = iNewValue
		
	def changeEconomyStability(self, iPlayer, iChange):
		self.scriptDict['lEconomyStability'][iPlayer] += iChange
		
	def getLastExpansionStability(self, iPlayer):
		return self.scriptDict['lLastExpansionStability'][iPlayer]
		
	def setLastExpansionStability(self, iPlayer, iNewValue):
		self.scriptDict['lLastExpansionStability'][iPlayer] = iNewValue
		
	def changeLastExpansionStability(self, iPlayer, iChange):
		self.scriptDict['lLastExpansionStability'][iPlayer] += iChange
		
	def getHappinessStability(self, iPlayer):
		return self.scriptDict['lHappinessStability'][iPlayer]
		
	def setHappinessStability(self, iPlayer, iNewValue):
		self.scriptDict['lHappinessStability'][iPlayer] = iNewValue
		
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
		
	def getWarStatusEnemies(self, iPlayer):
		return self.scriptDict['lWarStatus'][iPlayer].keys()
		
	def getWarStatus(self, iPlayer, iEnemy):
		if iEnemy not in self.scriptDict['lWarStatus'][iPlayer]: return None
		return self.scriptDict['lWarStatus'][iPlayer][iEnemy]
		
	def addWarStatus(self, iPlayer, iEnemy):
		self.scriptDict['lWarStatus'][iPlayer][iEnemy] = WarStatus(iPlayer, iEnemy)
		
	def removeWarStatus(self, iPlayer, iEnemy):
		del self.scriptDict['lWarStatus'][iPlayer][iEnemy]
		
	# VICTORY
		
	def getProtestantTechs(self, i):
		return self.scriptDict['lProtestantTechs'][i]
		
	def setProtestantTechs(self, i, iNewValue):
		self.scriptDict['lProtestantTechs'][i] = iNewValue
		
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
		
	def isPolytheismNeverReligion(self):
		return self.scriptDict['bPolytheismNeverReligion']
		
	def setPolytheismNeverReligion(self, bNewValue):
		self.scriptDict['bPolytheismNeverReligion'] = bNewValue
		
	def getFirstIndustrial(self):
		return self.scriptDict['iFirstIndustrial']
		
	def setFirstIndustrial(self, iNewValue):
		self.scriptDict['iFirstIndustrial'] = iNewValue
		
	def getFirstModern(self):
		return self.scriptDict['iFirstModern']
		
	def setFirstModern(self, iNewValue):
		self.scriptDict['iFirstModern'] = iNewValue
		
	def getArgentineGoldenAgeTurns(self):
		return self.scriptDict['iArgentineGoldenAgeTurns']
		
	def increaseArgentineGoldenAgeTurns(self):
		self.scriptDict['iArgentineGoldenAgeTurns'] += 1
		
	def getAggressionLevels(self):
		return self.scriptDict['lAggressionLevels']
		
	def changeAggressionLevel(self, iPlayer, iChange):
		self.scriptDict['lAggressionLevels'][iPlayer] += iChange
		
	def setAggressionLevel(self, iPlayer, iNewValue):
		self.scriptDict['lAggressionLevels'][iPlayer] = iNewValue
		
	def isMinorCityFounded(self, iCity):
		return self.scriptDict['lCityFounded'][iCity]
		
	def setMinorCityFounded(self, iCity, bNewValue):
		self.scriptDict['lCityFounded'][iCity] = bNewValue
		
	def getHumanRazePenalty(self):
		return self.scriptDict['iHumanRazePenalty']
		
	def setHumanRazePenalty(self, iNewValue):
		self.scriptDict['iHumanRazePenalty'] = iNewValue
		
	def changeHumanRazePenalty(self, iChange):
		self.scriptDict['iHumanRazePenalty'] += iChange
		
	def getBarbarianLosses(self, iPlayer):
		return self.scriptDict['lBarbarianLosses'][iPlayer]
		
	def changeBarbarianLosses(self, iPlayer, iChange):
		self.scriptDict['lBarbarianLosses'][iPlayer] += iChange
		
	def getByzantineBribes(self):
		return self.scriptDict['lByzantineBribes']
		
	def setByzantineBribes(self, lBribes):
		self.scriptDict['lByzantineBribes'] = lBribes
		
	def getMoorishGold(self):
		return self.scriptDict['iMoorishGold']
		
	def changeMoorishGold(self, iChange):
		self.scriptDict['iMoorishGold'] += iChange
		
	def getTaoistHealthTurns(self, iChange):
		return self.scriptDict['iTaoistHealthTurns']
	
	def setTaoistHealthTurns(self, iNewValue):
		self.scriptDict['iTaoistHealthTurns'] = iNewValue
		
	def changeTaoistHealthTurns(self, iChange):
		self.scriptDict['iTaoistHealthTurns'] += iNewValue
		
	# Congresses
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
		
# All modules import the following single instance, not the class

sd = StoredData()