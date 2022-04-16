from CvPythonExtensions import *
from Consts import *
from Types import *

gc = CyGlobalContext()


class CivList(list):

	def __getitem__(self, index):
		if not isinstance(index, Civ):
			index = Civ(gc.getPlayer(index).getCivilizationType())
		return list.__getitem__(self, index)


class PlayerList(list):

	def __getitem__(self, index):
		if isinstance(index, Civ):
			index = data.dSlots.get(index)
		return list.__getitem__(self, index)


class CivData:

	def __init__(self, iCiv):
		self.iCiv = iCiv
		
		self.setup()
		
	def setup(self):
	
		self.bSpawned = False
		self.iLastTurnAlive = 0
		
		# DynamicCivs
		
		self.iAnarchyTurns = 0
		self.iResurrections = 0
		
		# Rise
		
		self.iGreatGeneralsCreated = 0
		self.iGreatPeopleCreated = 0
		self.iGreatSpiesCreated = 0
		self.iNumUnitGoldenAges = 0


class PlayerData:

	def __init__(self, iPlayer):
		self.iPlayer = iPlayer
		
		self.setup()
		
	def update(self, data):
		self.__dict__.update(data)
		
		for goal in self.goals:
			goal.registerHandlers()

	def setup(self):
	
		# Rise
		
		self.lPreservedWonders = []
		
		# History
		
		self.iColonistsAlreadyGiven = 0
		self.iExplorationTurn = -1
		
		self.dColonialAcquisitionCities = {}
		
		# Religions
		
		self.iReformationDecision = -1
		
		# AI Wars
		
		self.iAggressionLevel = 0
		
		# Plague
		
		self.iPlagueCountdown = 0
		
		self.bFirstContactPlague = False
		
		# Victory
		
		self.bLaunchHistoricalGoldenAge = False
		
		self.historicalGoals = []
		self.religiousGoals = []
		
		# Stability
		
		self.resetStability()
		
	def resetStability(self):
		self.iStabilityLevel = iStabilityShaky
		
		self.iTurnsToCollapse = -1
		
		self.iCrisisCountdown = 0
		self.iLastStabilityTurn = 0
		self.iLastStability = 0
		self.iLastDifference = 0
		self.iNumPreviousCities = 0
		self.iBarbarianLosses = 0
		self.iPreviousCommerce = 0
		
		self.lEconomyTrend = []
		self.lHappinessTrend = []
		
		self.lWarTrend = [[]] * gc.getMAX_PLAYERS()		
		self.lWarStartTurn = [0] * gc.getMAX_PLAYERS()
		self.lLastWarSuccess = [0] * gc.getMAX_PLAYERS()
		
		self.lStabilityCategoryValues = [0, 0, 0, 0, 0]
		
		self.bDomesticCrisis = False
		
	def resetEconomyTrend(self):
		self.lEconomyTrend = []
		
	def resetHappinessTrend(self):
		self.lHappinessTrend = []
		
	def resetWarTrend(self, iEnemy):
		self.lWarTrend[iEnemy] = []
	
	def resetWarTrends(self):
		for iEnemy, _ in enumerate(self.lWarTrend):
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
	
	@property
	def goals(self):
		return self.historicalGoals + self.religiousGoals
		

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
		self.civs = CivList(CivData(i) for i in range(iNumCivs))
		self.players = PlayerList(PlayerData(i) for i in range(gc.getMAX_PLAYERS()))
		
		# Slots
		
		# set the default values for now, once slots become untied this should be set and kept updated on spawn
		# already make it dynamic because rebirths will change things
		self.dSlots = {}
		
		# Rise
		
		self.births = []
		
		self.dFirstContactConquerors = dict((iCiv, False) for iCiv in lBioNewWorld)
		self.dFirstContactMongols = dict((iCiv, True) for iCiv in lMongolCivs)
		self.lTradingCompanyConquerorsTargets = appenddict()
		
		self.iBeforeObserverSlot = -1
		
		self.bAlreadySwitched = False
		self.bUnlimitedSwitching = False
		self.bCheatMode = False
		
		# Religions
		
		self.iSeed = gc.getGame().getSorenRandNum(100, 'random seed')
		
		# Unique Powers
		
		self.iImmigrationTimer = 0
		
		# AI Wars
		
		self.iNextTurnAIWar = -1
		
		self.lConquest = [False] * iNumConquests
		
		# Dynamic Civs
		
		self.dCapitalLocations = {}
		
		# Congresses
		
		self.iGlobalWarAttacker = -1
		self.iGlobalWarDefender = -1
		
		self.iCongressTurns = 8
		
		self.bNoCongressOption = False
		
		# Plague
		
		self.lGenericPlagueDates = [-1] * 4
		
		self.bNoPlagues = False
		
		# Stability
		
		self.iHumanStability = 0
		self.iHumanRazePenalty = 0
		
		self.dSecedingCities = appenddict()

		# Barbarians

		self.lTimedConquests = []
		self.lMinorCityFounded = [False] * iNumMinorCities
		
		self.period_offsets = PeriodOffsets()
		
	def timedConquest(self, iPlayer, tPlot):
		self.lTimedConquests.append((iPlayer, tPlot))
		
	def resetStability(self, iPlayer):
		self.players[iPlayer].resetStability()
		
		for i, player in enumerate(self.players):
			if iPlayer != i:
				player.resetWarTrend(iPlayer)
				
	def resetHumanStability(self):
		self.iHumanStability = 0
		self.iHumanRazePenalty = 0
		
	def getSecedingCities(self, iPlayer):
		return self.dSecedingCities[iPlayer]
	
	def setSecedingCities(self, iPlayer, secedingCities):
		self.dSecedingCities[iPlayer] = secedingCities
	
	def removeSecedingCities(self, iPlayer):
		del self.dSecedingCities[iPlayer]
		
	def isFirstContactMongols(self, iCiv):
		return self.dFirstContactMongols[iCiv]
		
	def setFirstContactMongols(self, iCiv, bValue):
		self.dFirstContactMongols[iCiv] = bValue
		
	def getStabilityLevel(self, iPlayer):
		return self.players[iPlayer].iStabilityLevel
		
	def setStabilityLevel(self, iPlayer, iValue):
		self.players[iPlayer].iStabilityLevel = iValue
		
data = GameData()