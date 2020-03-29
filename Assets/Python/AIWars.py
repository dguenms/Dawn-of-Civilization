# Rhye's and Fall of Civilization - AI Wars

from CvPythonExtensions import *
import CvUtil
import PyHelpers	# LOQ
import Popup
#import cPickle as pickle
from Consts import *
import Areas
from RFCUtils import *
import UniquePowers
from StoredData import data # edead
import Stability as sta

from Core import *

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer	# LOQ
up = UniquePowers.UniquePowers()

### Constants ###


iMinIntervalEarly = 10
iMaxIntervalEarly = 20
iMinIntervalLate = 40
iMaxIntervalLate = 60
iThreshold = 100
iMinValue = 30

iRomeCarthageYear = -220
tRomeCarthageTL = (53, 37)
tRomeCarthageBR = (61, 40)

iRomeGreeceYear = -150
tRomeGreeceTL = (64, 40)
tRomeGreeceBR = (68, 45)

iRomeMesopotamiaYear = -100
tRomeMesopotamiaTL = (70, 38)
tRomeMesopotamiaBR = (78, 45)

iRomeAnatoliaYear = -100
tRomeAnatoliaTL = (70, 38)
tRomeAnatoliaBR = (75, 45)

iRomeCeltiaYear = -50
tRomeCeltiaTL = (52, 45)
tRomeCeltiaBR = (59, 51)

iRomeEgyptYear = 0
tRomeEgyptTL = (65, 31)
tRomeEgyptBR = (72, 36)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
tConquestRomeCarthage = (0, iCivRome, iCivCarthage, tRomeCarthageTL, tRomeCarthageBR, 2, iRomeCarthageYear, 10)
tConquestRomeGreece = (1, iCivRome, iCivGreece, tRomeGreeceTL, tRomeGreeceBR, 2, iRomeGreeceYear, 10)
tConquestRomeAnatolia = (2, iCivRome, iCivGreece, tRomeAnatoliaTL, tRomeAnatoliaBR, 2, iRomeAnatoliaYear, 10)
tConquestRomeCelts = (3, iCivRome, iCivCelts, tRomeCeltiaTL, tRomeCeltiaBR, 2, iRomeCeltiaYear, 10)
tConquestRomeEgypt = (4, iCivRome, iCivEgypt, tRomeEgyptTL, tRomeEgyptBR, 2, iRomeEgyptYear, 10)

iAlexanderYear = -340
tGreeceMesopotamiaTL = (70, 38)
tGreeceMesopotamiaBR = (78, 45)
tGreeceEgyptTL = (65, 31)
tGreeceEgyptBR = (72, 36)
tGreecePersiaTL = (79, 37)
tGreecePersiaBR = (85, 45)

tConquestGreeceMesopotamia = (5, iCivGreece, iCivBabylonia, tGreeceMesopotamiaTL, tGreeceMesopotamiaBR, 2, iAlexanderYear, 20)
tConquestGreeceEgypt = (6, iCivGreece, iCivEgypt, tGreeceEgyptTL, tGreeceEgyptBR, 2, iAlexanderYear, 20)
tConquestGreecePersia = (7, iCivGreece, iCivPersia, tGreecePersiaTL, tGreecePersiaBR, 2, iAlexanderYear, 20)

iCholaSumatraYear = 1030
tCholaSumatraTL = (98, 26)
tCholaSumatraBR = (101, 28)

tConquestCholaSumatra = (8, iCivTamils, iCivIndonesia, tCholaSumatraTL, tCholaSumatraBR, 1, iCholaSumatraYear, 10)

iSpainMoorsYear = 1200
tSpainMoorsTL = (50, 40)
tSpainMoorsBR = (54, 42)

tConquestSpainMoors = (9, iCivSpain, iCivMoors, tSpainMoorsTL, tSpainMoorsBR, 1, iSpainMoorsYear, 10)

iTurksPersiaYear = 1000
tTurksPersiaTL = (78, 37)
tTurksPersiaBR = (85, 43)

iTurksAnatoliaYear = 1100
tTurksAnatoliaTL = (69, 37)
tTurksAnatoliaBR = (78, 45)

tConquestTurksPersia = (10, iCivTurks, iCivArabia, tTurksPersiaTL, tTurksPersiaBR, 4, iTurksPersiaYear, 20)
tConquestTurksAnatolia = (11, iCivTurks, iCivByzantium, tTurksAnatoliaTL, tTurksAnatoliaBR, 5, iTurksAnatoliaYear, 20)

iMongolsPersiaYear = 1220
tMongolsPersiaTL = (79, 37)
tMongolsPersiaBR = (85, 49)

tConquestMongolsPersia = (12, iCivMongols, iCivTurks, tMongolsPersiaTL, tMongolsPersiaBR, 7, iMongolsPersiaYear, 10)

lConquests = [tConquestRomeCarthage, tConquestRomeGreece, tConquestRomeAnatolia, tConquestRomeCelts, tConquestRomeEgypt, tConquestGreeceMesopotamia, tConquestGreeceEgypt, tConquestGreecePersia, tConquestCholaSumatra, tConquestSpainMoors, tConquestTurksPersia, tConquestTurksAnatolia, tConquestMongolsPersia]

class AIWars:
		
	def setup(self):
		iTurn = year(-600)
		if scenario() == i600AD:  #late start condition
			iTurn = year(900)
		elif scenario() == i1700AD:
			iTurn = year(1720)
		data.iNextTurnAIWar = iTurn + rand(iMaxIntervalEarly-iMinIntervalEarly)


	def checkTurn(self, iGameTurn):
	
		# war and peace with minor civilisations
		iMinor = players.independent().periodic(20)
		if iMinor:
			restorePeaceHuman(iMinor, False)
		
		if turn() > turns(50):
			iMinor = players.independent().periodic(60)
			if iMinor:
				restorePeaceAI(iMinor, False)
				
			iMinor = players.independent().periodic(13)
			if iMinor:
				minorWars(iMinor)
				
			iMinor = players.civs(iCivCelts).periodic(50)
			if iMinor:
				minorWars(iMinor)
			
		for tConquest in lConquests:
			self.checkConquest(tConquest)
		
		if iGameTurn == data.iNextTurnAIWar:
			self.planWars(iGameTurn)
			
		for iLoopPlayer in players.major():
			data.players[iLoopPlayer].iAggressionLevel = dAggressionLevel[iLoopPlayer] + rand(2)
			
	def checkConquest(self, tConquest, tPrereqConquest = (), iWarPlan = WarPlanTypes.WARPLAN_TOTAL):
		iID, iCiv, iPreferredTargetCiv, tTL, tBR, iNumTargets, iYear, iIntervalTurns = tConquest
		
		iPlayer = slot(iCiv)
		if iPlayer < 0:
			return
			
		iPreferredTarget = slot(iPreferredTargetCiv)
		if iPreferredTarget < 0:
			return
	
		if player(iPlayer).isHuman(): return
		if not player(iPlayer).isAlive() and iCiv != iCivTurks: return
		if data.lConquest[iID]: return
		if iPreferredTarget >= 0 and player(iPreferredTarget).isAlive() and team(iPreferredTarget).isVassal(iPlayer): return
		
		iStartTurn = year(iYear).deviate(5)
		
		if turn() <= dBirth[iCiv]+3: return
		if not turn().between(iStartTurn, iStartTurn + iIntervalTurns): return
		if tPrereqConquest and not self.isConquered(tPrereqConquest): return
		
		self.spawnConquerors(iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns, iWarPlan)
		data.lConquest[iID] = True
		
	def isConquered(self, tConquest):
		iID, iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns = tConquest
	
		iNumMinorCities = 0
		for city in cities.start(tTL).end(tBR):
			if city.getOwner() in players.minor(): iNumMinorCities += 1 # TODO: make sure this includes barbarian
			elif city.getOwner() != iPlayer: return False
			
		if 2 * iNumMinorCities > len(lAreaCities): return False
		
		return True
		
	def declareWar(self, iPlayer, iTarget, iWarPlan):
		if team(iPlayer).isVassal(iTarget):
			team(iPlayer).setVassal(iTarget, False, False)
			
		team(iPlayer).declareWar(iTarget, True, iWarPlan)
			
	def spawnConquerors(self, iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns, iWarPlan = WarPlanTypes.WARPLAN_TOTAL):
		iCiv = civ(iPlayer)
		
		if not player(iPlayer).isAlive():
			for iTech in sta.getResurrectionTechs(iPlayer):
				team(iPlayer).setHasTech(iTech, True, iPlayer, False, False)
	
		lCities = []
		for city in cities.start(tTL).end(tBR):
			if city.getOwner() != iPlayer and not team(city).isVassal(iPlayer):
				lCities.append(city)
				
		capital = player(iPlayer).getCapitalCity()
		
		targetCities = cities.start(tTL).end(tBR).notowner(iPlayer).where(lambda city: not team(city).isVassal(iPlayer)).lowest(iNumTargets, lambda city: (int(city.getOwner() == iPreferredTarget), distance(city, capital)))
		owners = set(city.getOwner() for city in targetCities)
				
		if iPreferredTarget >= 0 and iPreferredTarget not in owners and player(iPreferredTarget).isAlive():
			self.declareWar(iPlayer, iPreferredTarget, iWarPlan)
				
		for iOwner in owners:
			self.declareWar(iPlayer, iOwner, iWarPlan)
			message(iOwner, 'TXT_KEY_UP_CONQUESTS_TARGET', name(iPlayer))
			
		for city in targetCities:
			iExtra = 0
			if human() not in [iPlayer, city.getOwner()]: 
				iExtra += 1
				
			if iCiv == iCivMongols and not player(iPlayer).isHuman():
				iExtra += 1
			
			tPlot = findNearestLandPlot((city.getX(), city.getY()), iPlayer)
			
			iBestInfantry = getBestInfantry(iPlayer)
			iBestSiege = getBestSiege(iPlayer)
			
			if iCiv == iCivGreece:
				iBestInfantry = iHoplite
				iBestSiege = iCatapult
			
			makeUnits(iPlayer, iBestInfantry, tPlot, 2 + iExtra, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iBestSiege, tPlot, 1 + 2*iExtra, UnitAITypes.UNITAI_ATTACK_CITY)
			
			if iCiv == iCivGreece:
				makeUnit(iPlayer, iCompanion, tPlot, UnitAITypes.UNITAI_ATTACK_CITY)
			
			if iCiv == iCivTamils:
				makeUnit(iPlayer, iWarElephant, tPlot, UnitAITypes.UNITAI_ATTACK_CITY)
				
			if iCiv == iCivSpain:
				makeUnits(iPlayer, getBestCavalry(iPlayer), tPlot, 2 * iExtra, UnitAITypes.UNITAI_ATTACK_CITY)
				
			if iCiv == iCivTurks:
				makeUnits(iPlayer, getBestCavalry(iPlayer), tPlot, 2 + iExtra, UnitAITypes.UNITAI_ATTACK_CITY)
	
	def forgetMemory(self, iTech, iPlayer):
		if iTech in [iPsychology, iTelevision]:
			pPlayer = player(iPlayer)
			for iLoopPlayer in players.major().without(iPlayer):
				if pPlayer.AI_getMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR) > 0:
					pPlayer.AI_changeMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR, -1)
				
				if pPlayer.AI_getMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR_ON_FRIEND) > 0:
					pPlayer.AI_changeMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR_ON_FRIEND, -1)
					
	def getNextInterval(self, iGameTurn):
		if iGameTurn > year(1600):
			iMinInterval = iMinIntervalLate
			iMaxInterval = iMaxIntervalLate
		else:
			iMinInterval = iMinIntervalEarly
			iMaxInterval = iMaxIntervalEarly
			
		iMinInterval = turns(iMinInterval)
		iMaxInterval = turns(iMaxInterval)
		
		return rand(iMinInterval, iMaxInterval)
					
	def planWars(self, iGameTurn):
	
		# skip if there is a world war
		if iGameTurn > year(1500):
			iCivsAtWar = 0
			for iLoopPlayer in players.major():
				if team(iLoopPlayer).getAtWarCount(True) > 0:
					iCivsAtWar += 1
			if 100 * iCivsAtWar / game.countCivPlayersAlive() > 50:
				data.iNextTurnAIWar = iGameTurn + self.getNextInterval(iGameTurn)
				return
	
		iAttackingPlayer = self.determineAttackingPlayer()
		iTargetPlayer = self.determineTargetPlayer(iAttackingPlayer)
		
		data.players[iAttackingPlayer].iAggressionLevel = 0
		
		if iTargetPlayer == -1:
			return
			
		if team(iAttackingPlayer).canDeclareWar(iTargetPlayer):
			team(iAttackingPlayer).AI_setWarPlan(iTargetPlayer, WarPlanTypes.WARPLAN_PREPARING_LIMITED)
		
		data.iNextTurnAIWar = iGameTurn + self.getNextInterval(iGameTurn)
		
	def determineAttackingPlayer(self):
		return players.major().alive().where(self.possibleTargets).maximum(lambda p: data.players[p].iAggressionLevel)
		
	def possibleTargets(self, iPlayer):
		return players.major().without(iPlayer).where(lambda p: team(iPlayer).canDeclareWar(player(p).getTeam()))
		
	def determineTargetPlayer(self, iPlayer):
		pPlayer = player(iPlayer)
		tPlayer = team(iPlayer)
		iCiv = civ(iPlayer)
		
		lPotentialTargets = []
		lTargetValues = [0 for _ in players.major()]

		# determine potential targets
		for iLoopPlayer in self.possibleTargets(iPlayer):
			pLoopPlayer = player(iLoopPlayer)
			tLoopPlayer = team(iLoopPlayer)
			
			if iLoopPlayer == iPlayer: continue
			
			# requires live civ and past contact
			if not pLoopPlayer.isAlive(): continue
			if not tPlayer.isHasMet(iLoopPlayer): continue
			
			# no masters or vassals
			if tPlayer.isVassal(iLoopPlayer): continue
			if tLoopPlayer.isVassal(iPlayer): continue
			
			# not already at war
			if tPlayer.isAtWar(iLoopPlayer): continue
			
			lPotentialTargets.append(iLoopPlayer)
			
		if not lPotentialTargets: return -1
			
		# iterate the map for all potential targets
		for plot in plots.all():
			iOwner = plot.getOwner()
			if iOwner in lPotentialTargets:
				lTargetValues[iOwner] += pPlayer.getWarValue(plot.getX(), plot.getY())
					
		# hard to attack with lost contact
		for iLoopPlayer in lPotentialTargets:
			lTargetValues[iLoopPlayer] /= 8
			
		# normalization
		iMaxValue = max(lTargetValues)
		if iMaxValue == 0: return -1
		
		for iLoopPlayer in lPotentialTargets:
			lTargetValues[iLoopPlayer] *= 500
			lTargetValues[iLoopPlayer] /= iMaxValue
			
		for iLoopPlayer in lPotentialTargets:
			iLoopCiv = civ(iLoopPlayer)
		
			# randomization
			if lTargetValues[iLoopPlayer] <= iThreshold:
				lTargetValues[iLoopPlayer] += rand(100)
			else:
				lTargetValues[iLoopPlayer] += rand(300)
			
			# balanced by attitude
			iAttitude = pPlayer.AI_getAttitude(iLoopPlayer) - 2
			if iAttitude > 0:
				lTargetValues[iLoopPlayer] /= 2 * iAttitude
				
			# exploit plague
			if data.players[iLoopPlayer].iPlagueCountdown > 0 or data.players[iLoopPlayer].iPlagueCountdown < -10:
				if turn() > year(dBirth[iCiv]) + turns(20):
					lTargetValues[iLoopPlayer] *= 3
					lTargetValues[iLoopPlayer] /= 2
		
			# determine master
			iMaster = -1
			for iLoopMaster in players.major():
				if tLoopPlayer.isVassal(iLoopMaster):
					iMaster = iLoopMaster
					break
					
			# master attitudes
			if iMaster >= 0:
				iAttitude = player(iMaster).AI_getAttitude(iLoopPlayer)
				if iAttitude > 0:
					lTargetValues[iLoopPlayer] /= 2 * iAttitude
			
			# peace counter
			if not tPlayer.isAtWar(iLoopPlayer):
				iCounter = min(7, max(1, tPlayer.AI_getAtPeaceCounter(iLoopPlayer)))
				if iCounter <= 7:
					lTargetValues[iLoopPlayer] *= 20 + 10 * iCounter
					lTargetValues[iLoopPlayer] /= 100
					
			# defensive pact
			if tPlayer.isDefensivePact(iLoopPlayer):
				lTargetValues[iLoopPlayer] /= 4
				
			# consider power
			iOurPower = tPlayer.getPower(True)
			iTheirPower = team(iLoopPlayer).getPower(True)
			if iOurPower > 2 * iTheirPower:
				lTargetValues[iLoopPlayer] *= 2
			elif 2 * iOurPower < iTheirPower:
				lTargetValues[iLoopPlayer] /= 2
				
			# spare smallish civs
			if iLoopCiv in [iCivNetherlands, iCivPortugal, iCivItaly]:
				lTargetValues[iLoopPlayer] *= 4
				lTargetValues[iLoopPlayer] /= 5
				
			# no suicide
			if iCiv == iCivNetherlands:
				if iLoopCiv in [iCivFrance, iCivHolyRome, iCivGermany]:
					lTargetValues[iLoopPlayer] /= 2
			elif iCiv == iCivPortugal:
				if iLoopCiv == iCivSpain:
					lTargetValues[iLoopPlayer] /= 2
			elif iCiv == iCivItaly:
				if iLoopCiv in [iCivFrance, iCivHolyRome, iCivGermany]:
					lTargetValues[iLoopPlayer] /= 2
					
		return find_max(lTargetValues).index