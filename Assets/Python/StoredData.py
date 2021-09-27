from CvPythonExtensions import *
from Consts import *

gc = CyGlobalContext()


class PlayerData:

	def __init__(self, iPlayer):
		self.iPlayer = iPlayer
		
		self.setup()
		
	def update(self, data):
		self.__dict__.update(data)
		
		for goal in self.goals:
			goal.registerHandlers()

	def setup(self):
	
		# Rise and Fall
		
		self.bSpawned = False
		
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
		
		self.bLaunchHistoricalGoldenAge = False
		
		self.historicalGoals = []
		self.religiousGoals = []
		
		# Stability
		
		self.resetStability()
		
		# Tech Log
		
		self.iTechColumn = 0
	
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
		self.players = [PlayerData(i) for i in range(gc.getMAX_PLAYERS())]
		
		# Slots
		
		# set the default values for now, once slots become untied this should be set and kept updated on spawn
		# already make it dynamic because rebirths will change things
		self.dSlots = dict((gc.getPlayer(iSlot).getCivilizationType(), iSlot) for iSlot in range(gc.getMAX_PLAYERS()))
		
		# Rise and Fall
		
		self.births = []

		self.lTempEvents = []
		self.lTempPlots = []
		self.lTimedConquests = []
		
		self.dCivEnabled = defaultdict({}, True)
		self.lMinorCityFounded = [False] * iNumMinorCities
		
		self.iPrepareCapitalPlayer = -1
		self.dFirstContactConquerors = dict((iCiv, False) for iCiv in lBioNewWorld)
		self.dFirstContactMongols = dict((iCiv, True) for iCiv in lMongolCivs)
		self.lTradingCompanyConquerorsTargets = appenddict()
		
		self.lCheatersCheck = [0, -1]
		
		self.iRespawnCiv = -1
		self.iFlipNewPlayer = -1
		self.iFlipNewPlayer = -1
		self.iOttomanSpawnTurn = -1
		
		self.iSpawnWar = 0
		self.iBetrayalTurns = 0
		self.iRebelCiv = 0
		
		self.iBeforeObserverSlot = -1
		
		self.lFlippingUnits = []
		
		self.bAlreadySwitched = False
		self.bUnlimitedSwitching = False
		self.bCheatMode = False
		
		# Religions
		
		self.iSeed = gc.getGame().getSorenRandNum(100, 'random seed')
		
		# Unique Powers
		
		self.iImmigrationTimer = 0
		
		self.lByzantineBribes = []
		
		self.lLatestRazeData = [-1] * 5
		
		# AI Wars
		
		self.iNextTurnAIWar = -1
		
		self.lConquest = [False] * iNumConquests
		
		# Dynamic Civs
		
		self.dCapitalLocations = {}
		
		# Congresses
		
		self.iGlobalWarAttacker = -1
		self.iGlobalWarDefender = -1
		
		self.iCongressTurns = 8
		self.iPlayersWithNationalism = 0
		
		self.bNoCongressOption = False
		
		# Plague
		
		self.lGenericPlagueDates = [-1] * 4
		
		self.bNoPlagues = False
		
		# Victories
		
		self.bIgnoreAI = True
		
		self.bEthiopiaConverted = False
		
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
		self.iTurkicPillages = 0
		self.iMoorishGold = 0
		self.lHolyRomanShrines = [False] * 3
		self.iEnglishSinks = 0
		self.iMongolRazes = 0
		self.iAztecSlaves = 0
		self.iCongoSlaveCounter = 0
		self.iDutchColonies = 0
		self.iMexicanGreatGenerals = 0
		self.iArgentineGoldenAgeTurns = 0
		self.iCanadianPeaceDeals = 0
		
		self.tFirstTurkicCapital = None
		self.tSecondTurkicCapital = None
		
		self.iPopeTurns = 0
		self.iHinduGoldenAgeTurns = 0
		self.iBuddhistPeaceTurns = 0
		self.iBuddhistHappinessTurns = 0
		self.iTaoistHealthTurns = 0
		self.iVedicHappiness = 0
		self.iTeotlSacrifices = 0
		self.iTeotlFood = 0
		self.bPolytheismNeverReligion = True
		
		# Stability
		
		self.iHumanStability = 0
		self.iHumanRazePenalty = 0
		
		self.bCrisisImminent = False
		
		self.dSecedingCities = appenddict()

		# Barbarians

		self.period_offsets = PeriodOffsets()
		
	def timedConquest(self, iPlayer, tPlot):
		self.lTimedConquests.append((iPlayer, tPlot))
		
	def setCivEnabled(self, iCiv, bNewValue):
		self.dCivEnabled[iCiv] = bNewValue
		
	def isCivEnabled(self, iCiv):
		return self.dCivEnabled[iCiv]
		
	def resetStability(self, iPlayer):
		self.players[iPlayer].resetStability()
		
		for i, player in enumerate(self.players):
			if iPlayer != i:
				player.resetWarTrend(iPlayer)
				
	def resetHumanStability(self):
		self.bCrisisImminent = False
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
		
	def getWonderBuilder(self, iWonder):
		if iWonder < iBeginWonders: return -1
		else: iWonder -= iBeginWonders
		return self.lWonderBuilder[iWonder]
		
	def setWonderBuilder(self, iWonder, iPlayer):
		if iWonder >= iBeginWonders:
			iWonder -= iBeginWonders
			self.lWonderBuilder[iWonder] = iPlayer
		
	def isNewWorldColonized(self):
		return self.iFirstNewWorldColony != -1
		
data = GameData()