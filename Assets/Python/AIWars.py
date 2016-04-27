# Rhye's and Fall of Civilization - AI Wars

from CvPythonExtensions import *
import CvUtil
import PyHelpers	# LOQ
import Popup
#import cPickle as pickle
import Consts as con
import Areas
import RFCUtils
import UniquePowers
from StoredData import sd # edead

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer	# LOQ
utils = RFCUtils.RFCUtils()
up = UniquePowers.UniquePowers()

### Constants ###


#iStartTurn = con.i600BC # moved to setup - edead
iMinIntervalEarly = 10
iMaxIntervalEarly = 20
iMinIntervalLate = 40
iMaxIntervalLate = 60
iThreshold = 100
iMinValue = 30
iNumPlayers = con.iNumMajorPlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iNumTotalPlayers = con.iNumTotalPlayers

iRome = con.iRome
iPhoenicia = con.iPhoenicia
iGreece = con.iGreece
iPersia = con.iPersia
iCeltia = con.iCeltia
iEgypt = con.iEgypt
iBabylonia = con.iBabylonia
iTamils = con.iTamils
iIndonesia = con.iIndonesia
iSpain = con.iSpain
iMoors = con.iMoors

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
tConquestRomeCarthage = (0, iRome, iPhoenicia, tRomeCarthageTL, tRomeCarthageBR, 2, iRomeCarthageYear, 10)
tConquestRomeGreece = (1, iRome, iGreece, tRomeGreeceTL, tRomeGreeceBR, 2, iRomeGreeceYear, 10)
tConquestRomeAnatolia = (2, iRome, iGreece, tRomeAnatoliaTL, tRomeAnatoliaBR, 2, iRomeAnatoliaYear, 10)
tConquestRomeCelts = (3, iRome, iCeltia, tRomeCeltiaTL, tRomeCeltiaBR, 2, iRomeAnatoliaYear, 10)
tConquestRomeEgypt = (4, iRome, iEgypt, tRomeEgyptTL, tRomeEgyptBR, 2, iRomeEgyptYear, 10)

iAlexanderYear = -340
tGreeceMesopotamiaTL = (70, 38)
tGreeceMesopotamiaBR = (78, 45)
tGreeceEgyptTL = (65, 31)
tGreeceEgyptBR = (72, 36)
tGreecePersiaTL = (79, 37)
tGreecePersiaBR = (85, 45)

tConquestGreeceMesopotamia = (5, iGreece, iBabylonia, tGreeceMesopotamiaTL, tGreeceMesopotamiaBR, 2, iAlexanderYear, 20)
tConquestGreeceEgypt = (6, iGreece, iEgypt, tGreeceEgyptTL, tGreeceEgyptBR, 2, iAlexanderYear, 20)
tConquestGreecePersia = (7, iGreece, iPersia, tGreecePersiaTL, tGreecePersiaBR, 2, iAlexanderYear, 20)

iCholaSumatraYear = 1030
tCholaSumatraTL = (98, 26)
tCholaSumatraBR = (101, 28)

tConquestCholaSumatra = (8, iTamils, iIndonesia, tCholaSumatraTL, tCholaSumatraBR, 1, iCholaSumatraYear, 10)

iSpainMoorsYear = 1200
tSpainMoorsTL = (50, 40)
tSpainMoorsBR = (54, 42)

tConquestSpainMoors = (9, iSpain, iMoors, tSpainMoorsTL, tSpainMoorsBR, 0, iSpainMoorsYear, 10)

class AIWars:

	def getAttackingCivsArray( self, iCiv ):
		return sd.scriptDict['lAttackingCivsArray'][iCiv]

	def setAttackingCivsArray( self, iCiv, iNewValue ):
		sd.scriptDict['lAttackingCivsArray'][iCiv] = iNewValue
		
	def getNextTurnAIWar( self ):
		return sd.scriptDict['iNextTurnAIWar']

	def setNextTurnAIWar( self, iNewValue ):
		sd.scriptDict['iNextTurnAIWar'] = iNewValue

		
	def setup(self):
		iTurn = getTurnForYear(-600)
		if utils.getScenario() == con.i600AD:  #late start condition
			iTurn = getTurnForYear(900)
		elif utils.getScenario() == con.i1700AD:
			iTurn = getTurnForYear(1720)
		self.setNextTurnAIWar(iTurn + gc.getGame().getSorenRandNum(iMaxIntervalEarly-iMinIntervalEarly, 'random turn'))



	def checkTurn(self, iGameTurn):

		print "Check AI wars"

		#turn automatically peace on between independent cities and all the major civs
		if (iGameTurn % 20 == 7):
			utils.restorePeaceHuman(con.iIndependent2, False)
		if (iGameTurn % 20 == 14):
			utils.restorePeaceHuman(con.iIndependent, False)
		if (iGameTurn % 60 == 55 and iGameTurn > utils.getTurns(50)):
			utils.restorePeaceAI(con.iIndependent, False)
		if (iGameTurn % 60 == 30 and iGameTurn > utils.getTurns(50)):
			utils.restorePeaceAI(con.iIndependent2, False)
		#turn automatically war on between independent cities and some AI major civs
		if (iGameTurn % 13 == 6 and iGameTurn > utils.getTurns(50)): #1 turn after restorePeace()
			utils.minorWars(con.iIndependent)
		if (iGameTurn % 13 == 11 and iGameTurn > utils.getTurns(50)): #1 turn after restorePeace()
			utils.minorWars(con.iIndependent2)
		if (iGameTurn % 50 == 24 and iGameTurn > utils.getTurns(50)):
			utils.minorWars(con.iCeltia)
			utils.minorWars(con.iSeljuks)
		
		self.checkConquest(tConquestGreeceMesopotamia)
		self.checkConquest(tConquestGreeceEgypt)
		self.checkConquest(tConquestGreecePersia, tConquestGreeceMesopotamia)
		
		self.checkConquest(tConquestRomeCarthage)
		self.checkConquest(tConquestRomeGreece)
		self.checkConquest(tConquestRomeAnatolia, tConquestRomeGreece)
		self.checkConquest(tConquestRomeCelts)
		self.checkConquest(tConquestRomeEgypt)
		
		self.checkConquest(tConquestSpainMoors)
		
		if iGameTurn == self.getNextTurnAIWar():
			self.planWars(iGameTurn)
			
		for iLoopPlayer in range(con.iNumPlayers):
			sd.changeAggressionLevel(iLoopPlayer, con.tAggressionLevel[iLoopPlayer] + gc.getGame().getSorenRandNum(2, 'Random aggression'))
			
	def checkConquest(self, tConquest, tPrereqConquest = (), iWarPlan = WarPlanTypes.WARPLAN_TOTAL):
		iID, iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns = tConquest
	
		if utils.getHumanID() == iPlayer: return
		
		if not gc.getPlayer(iPlayer).isAlive(): return
		
		if sd.isConquest(iID): return
		
		iGameTurn = gc.getGame().getGameTurn()
		iStartTurn = getTurnForYear(iYear) - 5 + (utils.getSeed() % 10)
		
		if not (iStartTurn <= iGameTurn <= iStartTurn + iIntervalTurns): return
		
		if tPrereqConquest and not self.isConquered(tPrereqConquest): return
		
		self.spawnConquerors(iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns, iWarPlan)
		sd.setConquest(iID, True)
		
	def isConquered(self, tConquest):
		iID, iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns = tConquest
	
		iNumMinorCities = 0
		lAreaCities = utils.getAreaCities(utils.getPlotList(tTL, tBR))
		for city in lAreaCities:
			if city.getOwner() in [iIndependent, iIndependent2, con.iBarbarian, con.iNative]: iNumMinorCities += 1
			elif city.getOwner() != iPlayer: return False
			
		if 2 * iNumMinorCities > len(lAreaCities): return False
		
		return True
			
	def spawnConquerors(self, iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns, iWarPlan = WarPlanTypes.WARPLAN_TOTAL):
		lCities = []
		for city in utils.getAreaCities(utils.getPlotList(tTL, tBR)):
			if city.getOwner() != iPlayer and not gc.getTeam(city.getOwner()).isVassal(iPlayer):
				lCities.append(city)
				
		capital = gc.getPlayer(iPlayer).getCapitalCity()
		
		lTargetCities = []
		for i in range(iNumTargets):
			if len(lCities) == 0: break
			
			targetCity = utils.getHighestEntry(lCities, lambda x: -utils.calculateDistance(x.getX(), x.getY(), capital.getX(), capital.getY()) + int(x.getOwner() == iPreferredTarget) * 1000)
			lTargetCities.append(targetCity)
			lCities.remove(targetCity)
			
		lOwners = []
		for city in lTargetCities:
			if city.getOwner() not in lOwners:
				lOwners.append(city.getOwner())
				
		if iPreferredTarget not in lOwners and gc.getPlayer(iPreferredTarget).isAlive():
			gc.getTeam(iPlayer).declareWar(iPreferredTarget, True, iWarPlan)
				
		for iOwner in lOwners:
			gc.getTeam(iPlayer).declareWar(iOwner, True, iWarPlan)
			CyInterface().addMessage(iOwner, False, con.iDuration, CyTranslator().getText("TXT_KEY_UP_CONQUESTS_TARGET", (gc.getPlayer(iPlayer).getCivilizationShortDescription(0),)), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
			
		for city in lTargetCities:
			iExtra = 0
			if utils.getHumanID() not in [iPlayer, city.getOwner()]: iExtra = 1
			
			tPlot = utils.findNearestLandPlot((city.getX(), city.getY()), iPlayer)
			
			iBestInfantry = utils.getBestInfantry(iPlayer)
			iBestSiege = utils.getBestSiege(iPlayer)
			
			if iPlayer == con.iGreece:
				iBestInfantry = con.iGreekHoplite
				iBestSiege = con.iCatapult
			
			utils.makeUnitAI(iBestInfantry, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2 + iExtra)
			utils.makeUnitAI(iBestSiege, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1 + 2*iExtra)
			
			if iPlayer == con.iTamils:
				utils.makeUnitAI(con.iWarElephant, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 1)
	
	def forgetMemory(self, iTech, iPlayer):
		if (iTech == con.iCommunism or iTech == con.iMassMedia):
			for iLoopCiv in range( iNumPlayers ):
				pPlayer = gc.getPlayer(iPlayer)
				if (pPlayer.AI_getMemoryCount(iLoopCiv,0) > 0):
					pPlayer.AI_changeMemoryCount(iLoopCiv,0,-1)
				if (pPlayer.AI_getMemoryCount(iLoopCiv,1) > 0):
					pPlayer.AI_changeMemoryCount(iLoopCiv,1,-1)
					
	def getNextInterval(self, iGameTurn):
		if iGameTurn > getTurnForYear(1600):
			iMinInterval = iMinIntervalLate
			iMaxInterval = iMaxIntervalLate
		else:
			iMinInterval = iMinIntervalEarly
			iMaxInterval = iMaxIntervalEarly
			
		iMinInterval = utils.getTurns(iMinInterval)
		iMaxInterval = utils.getTurns(iMaxInterval)
		
		return iMinInterval + gc.getGame().getSorenRandNum(iMaxInterval-iMinInterval, 'random turn')
					
	def planWars(self, iGameTurn):
	
		# skip if there is a world war
		if iGameTurn > getTurnForYear(1500):
			iCivsAtWar = 0
			for iLoopPlayer in range(con.iNumPlayers):
				tLoopPlayer = gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam())
				if tLoopPlayer.getAtWarCount(True) > 0:
					iCivsAtWar += 1
			if 100 * iCivsAtWar / gc.getGame().countCivPlayersAlive() > 50:
				self.setNextTurnAIWar(iGameTurn + self.getNextInterval(iGameTurn))
				return
	
		iAttackingPlayer = self.determineAttackingPlayer()
		iTargetPlayer = self.determineTargetPlayer(iAttackingPlayer)
		
		sd.setAggressionLevel(iAttackingPlayer, 0)
		
		if iTargetPlayer == -1:
			return
			
		gc.getTeam(iAttackingPlayer).AI_setWarPlan(iTargetPlayer, WarPlanTypes.WARPLAN_PREPARING_LIMITED)
		
		self.setNextTurnAIWar(iGameTurn + self.getNextInterval(iGameTurn))
		
	def determineAttackingPlayer(self):
		lAggressionLevels = sd.getAggressionLevels()
		iHighestEntry = utils.getHighestEntry(lAggressionLevels)
		
		return lAggressionLevels.index(iHighestEntry)
		
	def determineTargetPlayer(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		tPlayer = gc.getTeam(pPlayer.getTeam())
		lPotentialTargets = []
		lTargetValues = [0 for i in range(con.iNumPlayers)]

		# determine potential targets
		for iLoopPlayer in range(con.iNumPlayers):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			tLoopPlayer = gc.getTeam(pLoopPlayer.getTeam())
			
			# requires live civ and past contact
			if not pLoopPlayer.isAlive(): continue
			if not tPlayer.isHasMet(iLoopPlayer): continue
			
			# no masters or vassals
			if tPlayer.isVassal(iLoopPlayer): continue
			if tLoopPlayer.isVassal(iPlayer): continue
			
			# not already at war
			if tPlayer.isAtWar(iLoopPlayer): continue
			
			lPotentialTargets.append(iLoopPlayer)
			
		if not lPotentialTargets:
			return -1
			
		# iterate the map for all potential targets
		for i in range(124):
			for j in range(68):
				iOwner = gc.getMap().plot(i,j).getOwner()
				if iOwner in lPotentialTargets:
					lTargetValues[iOwner] += pPlayer.getWarValue(i, j)
					
		# hard to attack with lost contact
		for iLoopPlayer in lPotentialTargets:
			lTargetValues[iLoopPlayer] /= 8
			
		# normalization
		iMaxValue = utils.getHighestEntry(lTargetValues)
		for iLoopPlayer in lPotentialTargets:
			lTargetValues[iLoopPlayer] *= 500
			lTargetValues[iLoopPlayer] /= iMaxValue
			
		for iLoopPlayer in lPotentialTargets:
		
			# randomization
			if lTargetValues[iLoopPlayer] <= iThreshold:
				lTargetValues[iLoopPlayer] += gc.getGame().getSorenRandNum(100, 'random modifier')
			else:
				lTargetValues[iLoopPlayer] += gc.getGame().getSorenRandNum(300, 'random modifier')
			
			# balanced by attitude
			iAttitude = pPlayer.AI_getAttitude(iLoopPlayer) - 2
			if iAttitude > 0:
				lTargetValues[iLoopPlayer] /= 2 * iAttitude
				
			# exploit plague
			if utils.getPlagueCountdown(iLoopPlayer) > 0 or utils.getPlagueCountdown(iLoopPlayer) < -10:
				if gc.getGame().getGameTurn() > getTurnForYear(con.tBirth[iLoopPlayer]) + utils.getTurns(20):
					lTargetValues[iLoopPlayer] *= 3
					lTargetValues[iLoopPlayer] /= 2
		
			# determine master
			iMaster = -1
			for iLoopMaster in range(con.iNumPlayers):
				if tLoopPlayer.isVassal(iLoopMaster):
					iMaster = iLoopMaster
					break
					
			# master attitudes
			if iMaster >= 0:
				iAttitude = gc.getPlayer(iMaster).AI_getAttitude(iLoopPlayer)
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
			iTheirPower = gc.getTeam(iLoopPlayer).getPower(True)
			if iOurPower > 2 * iTheirPower:
				lTargetValues[iLoopPlayer] *= 2
			elif 2 * iOurPower < iTheirPower:
				lTargetValues[iLoopPlayer] /= 2
				
			# spare smallish civs
			if iLoopPlayer in [con.iNetherlands, con.iPortugal, con.iItaly]:
				lTargetValues[iLoopPlayer] *= 4
				lTargetValues[iLoopPlayer] /= 5
				
			# no suicide
			if iPlayer == con.iNetherlands:
				if iLoopPlayer in [con.iFrance, con.iHolyRome, con.iGermany]:
					lTargetValues[iLoopPlayer] /= 2
			elif iPlayer == con.iPortugal:
				if iLoopPlayer == con.iSpain:
					lTargetValues[iLoopPlayer] /= 2
			elif iPlayer == con.iItaly:
				if iLoopPlayer in [con.iFrance, con.iHolyRome, con.iGermany]:
					lTargetValues[iLoopPlayer] /= 2
					
		return utils.getHighestIndex(lTargetValues)