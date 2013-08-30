# Rhye's and Fall of Civilization - Stored Data

from CvPythonExtensions import *
import CvUtil
import PyHelpers  
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
                self.scriptDict = pickle.loads(gc.getGame().getScriptData())

        def save(self):
                """Pickles and saves script data"""
                gc.getGame().setScriptData(pickle.dumps(self.scriptDict))

        def setup(self):
                """Initialise the global script data dictionary for usage."""
                self.scriptDict = {      #------------RiseAndFall
				    'lTempEventList' : [],
                                    'iNewCiv': -1,
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
                                     #------------Religions
                                    'iSeed': -1,
				    'lReformationDecision': [-1 for i in range(con.iNumPlayers)],
                                    #------------UP
                                    'iImmigrationTimer': 0,
                                    'iLatestFlipTurn': 0,
                                    'lLatestRazeData': [-1, -1, -1, -1, -1],
				    'iRomanVictories': 0,
				    #------------AIWars
                                    'lAttackingCivsArray': [0 for i in range(con.iNumPlayers)], #original RFC had -1 here somewhere??
                                    'iNextTurnAIWar': -1,
                                    #------------Congresses
                                    'bCongressEnabled': False,
                                    'iCivsWithNationalism': 0,
                                    'bUNbuilt': False,
                                    'lInvitedNations': [False for i in range(con.iNumPlayers)],
                                    'lVotes': [0 for i in range(con.iNumPlayers)],
                                    'lTempActiveCiv': [-1 for i in range(con.iNumPlayers)],
                                    'lTempReqCity': [-1 for i in range(con.iNumPlayers)],
                                    'iLoopIndex': 0,
                                    'lTempReqCityHuman': [-1, -1, -1, -1, -1],
                                    'tempReqCityNI': -1,
                                    'tempActiveCivNI': -1,
                                    'lTempAttackingCivsNI': [False for i in range(con.iNumPlayers)],
                                    'iNumNationsTemp': 0,
                                    'lBribe' : [-1, -1, -1],
                                    'lCivsToBribe': [-1 for i in range(con.iNumPlayers)],
                                    'tTempFlippingCityCongress': -1,
                                    'lMemory': [0 for i in range(con.iNumTotalPlayersB)], #total players + barbarians (minors and barbs are not used, but necessary for not going out of range)
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
                                    #------------Stability
				    'lStabilityLevels': [con.iStabilityShaky for i in range(con.iNumPlayers)],
				    'lCrisisCountdown': [0 for i in range(con.iNumPlayers)],
				    'iLastStability' : 0,
				    'iLastDifference' : 0,
				    'lStabilityCategoryValues' : [0, 0, 0, 0, 0],
				    'lNumPreviousCities' : [0 for i in range(con.iNumPlayers)],
				    'bCrisisImminent' : False,
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
		
	def getLastStability(self):
		return self.scriptDict['iLastStability']
		
	def setLastStability(self, iNewValue):
		self.scriptDict['iLastStability'] = iNewValue		
		
	def getLastDifference(self):
		return -self.scriptDict['iLastDifference']
		
	def setLastDifference(self, iNewValue):
		self.scriptDict['iLastDifference'] = iNewValue
		
	def getStabilityCategoryValue(self, iCategory):
		return self.scriptDict['lStabilityCategoryValues'][iCategory]
		
	def setStabilityCategoryValue(self, iCategory, iNewValue):
		self.scriptDict['lStabilityCategoryValues'][iCategory] = iNewValue
		
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

# All modules import the following single instance, not the class

sd = StoredData()