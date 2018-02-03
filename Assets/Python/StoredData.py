# Rhye's and Fall of Civilization - Stored Data

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
import cPickle as pickle
from Consts import *

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

class PlayerData:

	def __init__(self, iPlayer):
		self.iPlayer = iPlayer
		
		self.setup()
		
	def update(self, data):
		self.__dict__.update(data)

	def setup(self):
	
		# Rise and Fall
		
		self.iColonistsAlreadyGiven = 0
		self.iSpawnDelay = 0
		self.iFlipsDelay = 0
		self.iBirthTurnModifier = 0
		self.iAnarchyTurns = 0
		self.iResurrections = 0
		self.iLastTurnAlive = 0
		
		self.iExplorationTurn = 1500
		
		# Religions
		
		self.iReformationDecision = -1
		
		# AI Wars
		
		self.iAggressionLevel = 0
		
		# Plague
		
		self.iPlagueCountdown = 0
		
		self.bFirstContactPlague = False
		
		# Victory
		
		self.lGoals = [-1, -1, -1]
		self.bHistoricalGoldenAge = False
		
		# Stability
		
		self.resetStability()
		
		# Tech Log
		
		self.iTechColumn = 0
		
	def resetStability(self):
		self.iStabilityLevel = iStabilityShaky
		
		self.iTurnsToCollapse = -1
		
		self.iCrisisCountdown = 0
		self.iLastStability = 0
		self.iLastDifference = 0
		self.iNumPreviousCities = 0
		self.iBarbarianLosses = 0
		self.iPreviousCommerce = 0
		self.iLastExpansionStability = 0
		
		self.lEconomyTrend = []
		self.lHappinessTrend = []
		
		self.lWarTrend = [[] for _ in range(iNumTotalPlayersB)]		
		self.lWarStartTurn = [0] * iNumTotalPlayersB
		self.lLastWarSuccess = [0] * iNumTotalPlayersB
		
		self.lStabilityCategoryValues = [0, 0, 0, 0, 0]
		
	def resetEconomyTrend(self):
		self.lEconomyTrend = []
		
	def resetHappinessTrend(self):
		self.lHappinessTrend = []
		
	def resetWarTrend(self, iEnemy):
		self.lWarTrend[iEnemy] = []
	
	def resetWarTrends(self):
		for iEnemy in range(iNumPlayers):
			self.resetWarTrend(iEnemy)
	
	def pushEconomyTrend(self, iValue):
		self.lEconomyTrend.append(iValue)
		if len(self.lEconomyTrend) > 10:
			self.lEconomyTrend.pop(0)
			
	def pushHappinessTrend(self, iValue):
		self.lHappinessTrend.append(iValue)
		if len(self.lHappinessTrend) > 10:
			self.lHappinessTrend.pop(0)
			
	def pushWarTrend(self, iEnemy, iValue):
		self.lWarTrend[iEnemy].append(iValue)
		if len(self.lWarTrend[iEnemy]) > 10:
			self.lWarTrend[iEnemy].pop(10)
			
	def getLastDifference(self):
		return -self.iLastDifference
		
	def getLastWarTrend(self, iEnemy):
		lTrend = self.lWarTrend[iEnemy]
		for i in reversed(range(len(lTrend))):
			if lTrend[i] != 0: return lTrend[i]
		return 0
		
	def getGoal(self, iGoal):
		return self.lGoals[iGoal]
		
	def setGoal(self, iGoal, iNewValue):
		if iNewValue == 1 and self.getGoal(iGoal) == 0: return
		self.lGoals[iGoal] = iNewValue
	
class GameData:

	def __init__(self):
		self.setup()
		
	def update(self, data):
		self.__dict__.update(data)
		
		for player in self.players:
			data = player.__dict__.copy()
			player.setup()
			player.update(data)

	def setup(self):
		self.players = [PlayerData(i) for i in range(iNumTotalPlayersB)]
		
		# Rise and Fall

		self.lTempEvents = []
		self.lNewCivs = []
		self.lTempPlots = []
		self.lTimedConquests = []
		
		self.lPlayerEnabled = [True] * len(lSecondaryCivs)
		self.lMinorCityFounded = [False] * iNumMinorCities
		
		self.lDeleteMode = [-1] * 3
		self.lFirstContactConquerors = [False] * 3
		self.lFirstContactMongols = [True] * 5
		self.lTradingCompanyConquerorsTargets = [[] for _ in range(5)]
		
		self.lCheatersCheck = [0, -1]
		
		self.iRespawnCiv = -1
		self.iNewCivFlip = -1
		self.iOldCivFlip = -1
		self.iOttomanSpawnTurn = -1
		
		self.iSpawnWar = 0
		self.iBetrayalTurns = 0
		self.iRebelCiv = 0
		
		self.lFlippingUnits = []
		
		self.bAlreadySwitched = False
		self.bUnlimitedSwitching = False
		self.bCheatMode = False
		
		# Religions
		
		self.iSeed = gc.getGame().getSorenRandNum(100, "Random delay")
		
		# Unique Powers
		
		self.iImmigrationTimer = 0
		self.iRomanVictories = 0
		
		self.lByzantineBribes = []
		
		self.lLatestRazeData = [-1] * 5
		
		# AI Wars
		
		self.iNextTurnAIWar = -1
		
		self.lConquest = [False] * iNumConquests
		
		# Congresses
		
		self.iGlobalWarAttacker = -1
		self.iGlobalWarDefender = -1
		
		self.iCongressTurns = 0
		self.iCivsWithNationalism = 0
		
		self.currentCongress = None
		
		self.bNoCongressOption = False
		
		# Plague
		
		self.lGenericPlagueDates = [-1] * 4
		
		self.bNoPlagues = False
		
		# Victories
		
		self.bIgnoreAI = True
		
		self.lWonderBuilder = [-1] * (iNumBuildings - iBeginWonders)
		self.lReligionFounder = [-1] * iNumReligions
		self.lFirstDiscovered = [-1] * iNumTechs
		self.lFirstEntered = [-1] * iNumEras
		self.lFirstGreatPeople = [-1] * len(lGreatPeopleUnits)
		self.iFirstNewWorldColony = -1
		
		self.iChineseGoldenAgeTurns = 0
		self.iKoreanSinks = 0
		self.iTamilTradeGold = 0
		self.iColombianTradeGold = 0
		self.iVikingGold = 0
		self.iMoorishGold = 0
		self.iEnglishSinks = 0
		self.iMongolRazes = 0
		self.iAztecSlaves = 0
		self.iCongoSlaveCounter = 0
		self.iDutchColonies = 0
		self.iMexicanGreatGenerals = 0
		self.iArgentineGoldenAgeTurns = 0
		self.iCanadianPeaceDeals = 0
		
		self.iPopeTurns = 0
		self.iHinduGoldenAgeTurns = 0
		self.iBuddhistPeaceTurns = 0
		self.iBuddhistHappinessTurns = 0
		self.iTaoistHealthTurns = 0
		self.iVedicHappiness = 0
		self.iTeotlSacrifices = 0
		self.bPolytheismNeverReligion = True
		
		# Stability
		
		self.iHumanStability = 0
		self.iHumanRazePenalty = 0
		
		self.bCrisisImminent = False
		self.bNoHumanStability = False
		self.bNoAIStability = False
		
		self.dSecedingCities = {}
		
	def timedConquest(self, iPlayer, tPlot):
		self.lTimedConquests.append((iPlayer, tPlot))
		
	def setPlayerEnabled(self, iPlayer, bNewValue):
		self.lPlayerEnabled[lSecondaryCivs.index(iPlayer)] = bNewValue
		
	def isPlayerEnabled(self, iPlayer):
		return self.lPlayerEnabled[lSecondaryCivs.index(iPlayer)]
		
	def resetStability(self, iPlayer):
		players[iPlayer].resetStability()
		
		for i, player in enumerate(players):
			if iPlayer != i:
				player.resetWarTrend(iPlayer)
				
	def resetHumanStability(self):
		self.bCrisisImminent = False
		self.iHumanStability = 0
		self.iHumanRazePenalty = 0
		
	def getSecedingCities(self, iPlayer):
		if iPlayer not in self.dSecedingCities: return []
		return [city for city in [gc.getPlayer(iPlayer).getCity(i) for i in self.dSecedingCities[iPlayer]] if (city.getX(), city.getY()) != (-1, -1)]
	
	def setSecedingCities(self, iPlayer, lCities):
		self.dSecedingCities[iPlayer] = [city.getID() for city in lCities]
		
	def getNewCiv(self):
		return self.lNewCivs.pop()
	
	def addNewCiv(self, iCiv):
		self.lNewCivs.append(iCiv)
		
	def isFirstContactMongols(self, iPlayer):
		return self.lFirstContactMongols[lMongolCivs.index(iPlayer)]
		
	def setFirstContactMongols(self, iPlayer, bValue):
		self.lFirstContactMongols[lMongolCivs.index(iPlayer)] = bValue
		
	def getStabilityLevel(self, iPlayer):
		return self.players[iPlayer].iStabilityLevel
		
	def setStabilityLevel(self, iPlayer, iValue):
		self.players[iPlayer].iStabilityLevel = iValue
		
	def getWonderBuilder(self, iWonder):
		if iWonder < iBeginWonders: return -1
		else: iWonder -= iBeginWonders
		return self.lWonderBuilder[iWonder]
		
	def setWonderBuilder(self, iWonder, iPlayer):
		if iWonder >= iBeginWonders:
			iWonder -= iBeginWonders
			self.lWonderBuilder[iWonder] = iPlayer
		
	def isFirstWorldColonized(self):
		return self.iFirstNewWorldColony != -1
		
data = GameData()