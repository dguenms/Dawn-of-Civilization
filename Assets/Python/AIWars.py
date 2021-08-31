# Rhye's and Fall of Civilization - AI Wars

from CvPythonExtensions import *
import CvUtil
import PyHelpers	# LOQ
import Popup
from Consts import *
from RFCUtils import *
from StoredData import data # edead
import Stability as sta
from Events import handler

from Core import *

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer	# LOQ

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
tConquestRomeCarthage = (0, iRome, iCarthage, tRomeCarthageTL, tRomeCarthageBR, 2, iRomeCarthageYear, 10)
tConquestRomeGreece = (1, iRome, iGreece, tRomeGreeceTL, tRomeGreeceBR, 2, iRomeGreeceYear, 10)
tConquestRomeAnatolia = (2, iRome, iGreece, tRomeAnatoliaTL, tRomeAnatoliaBR, 2, iRomeAnatoliaYear, 10)
tConquestRomeCelts = (3, iRome, iCelts, tRomeCeltiaTL, tRomeCeltiaBR, 2, iRomeCeltiaYear, 10)
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

tConquestCholaSumatra = (8, iTamils, -1, tCholaSumatraTL, tCholaSumatraBR, 1, iCholaSumatraYear, 10)

iSpainMoorsYear = 1200
tSpainMoorsTL = (50, 40)
tSpainMoorsBR = (54, 42)

tConquestSpainMoors = (9, iSpain, iMoors, tSpainMoorsTL, tSpainMoorsBR, 1, iSpainMoorsYear, 10)

iTurksPersiaYear = 1000
tTurksPersiaTL = (78, 37)
tTurksPersiaBR = (85, 43)

iTurksAnatoliaYear = 1100
tTurksAnatoliaTL = (69, 37)
tTurksAnatoliaBR = (78, 45)

tConquestTurksPersia = (10, iTurks, iArabia, tTurksPersiaTL, tTurksPersiaBR, 4, iTurksPersiaYear, 20)
tConquestTurksAnatolia = (11, iTurks, iByzantium, tTurksAnatoliaTL, tTurksAnatoliaBR, 5, iTurksAnatoliaYear, 20)

iMongolsPersiaYear = 1220
tMongolsPersiaTL = (79, 37)
tMongolsPersiaBR = (85, 49)

tConquestMongolsPersia = (12, iMongols, iTurks, tMongolsPersiaTL, tMongolsPersiaBR, 7, iMongolsPersiaYear, 10)

lConquests = [tConquestRomeCarthage, tConquestRomeGreece, tConquestRomeAnatolia, tConquestRomeCelts, tConquestRomeEgypt, tConquestGreeceMesopotamia, tConquestGreeceEgypt, tConquestGreecePersia, tConquestCholaSumatra, tConquestSpainMoors, tConquestTurksPersia, tConquestTurksAnatolia, tConquestMongolsPersia]

	
@handler("GameStart")
def setup():
	iTurn = year(-600)
	if scenario() == i600AD:  #late start condition
		iTurn = year(900)
	elif scenario() == i1700AD:
		iTurn = year(1720)
	data.iNextTurnAIWar = iTurn + rand(iMaxIntervalEarly-iMinIntervalEarly)


@handler("BeginGameTurn")
def restorePeaceMinors(iGameTurn):
	if iGameTurn > turns(50):
		iMinor = players.independent().periodic(20)
		if iMinor:
			restorePeaceHuman(iMinor, False)
			
		iMinor = players.independent().periodic(60)
		if iMinor:
			restorePeaceAI(iMinor, False)


@handler("BeginGameTurn")
def startMinorWars(iGameTurn):
	if iGameTurn > turns(50):	
		iMinor = players.independent().periodic(13)
		if iMinor:
			minorWars(iMinor)
			
		iMinor = players.civs(iCelts).periodic(50)
		if iMinor:
			minorWars(iMinor)


@handler("BeginGameTurn")
def checkConquests():
	for tConquest in lConquests:
		checkConquest(tConquest)
		
		
@handler("BeginGameTurn")
def checkWarPlans(iGameTurn):		
	if iGameTurn == data.iNextTurnAIWar:
		planWars(iGameTurn)


@handler("BeginGameTurn")
def increaseAggressionLevels():
	for iLoopPlayer in players.major():
		data.players[iLoopPlayer].iAggressionLevel = dAggressionLevel[iLoopPlayer] + rand(2)


@handler("techAcquired")	
def forgetMemory(iTech, iTeam, iPlayer):
	if year() <= year(1700):
		return

	if iTech in [iPsychology, iTelevision]:
		pPlayer = player(iPlayer)
		for iLoopPlayer in players.major().without(iPlayer):
			if pPlayer.AI_getMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR) > 0:
				pPlayer.AI_changeMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR, -1)
			
			if pPlayer.AI_getMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR_ON_FRIEND) > 0:
				pPlayer.AI_changeMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR_ON_FRIEND, -1)


@handler("changeWar")
def resetAggressionLevel(bWar, iTeam, iOtherTeam):
	if bWar and not is_minor(iTeam) and not is_minor(iOtherTeam):
		data.players[iTeam].iAggressionLevel = 0
		data.players[iOtherTeam].iAggressionLevel = 0

		
def checkConquest(tConquest, tPrereqConquest = (), iWarPlan = WarPlanTypes.WARPLAN_TOTAL):
	iID, iCiv, iPreferredTargetCiv, tTL, tBR, iNumTargets, iYear, iIntervalTurns = tConquest
	
	iPlayer = slot(iCiv)
	if iPlayer < 0:
		return
		
	iPreferredTarget = slot(iPreferredTargetCiv)

	if player(iPlayer).isHuman(): return
	if not player(iPlayer).isAlive() and iCiv != iTurks: return
	if data.lConquest[iID]: return
	if iPreferredTarget >= 0 and player(iPreferredTarget).isAlive() and team(iPreferredTarget).isVassal(iPlayer): return
	
	iStartTurn = year(iYear) + turns(data.iSeed % 10 - 5)
	
	if turn() < player(iCiv).getLastBirthTurn() + turns(3): return
	if not (iStartTurn <= turn() <= iStartTurn + iIntervalTurns): return
	if tPrereqConquest and not isConquered(tPrereqConquest): return
	
	spawnConquerors(iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns, iWarPlan)
	data.lConquest[iID] = True


def isConquered(tConquest):
	iID, iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns = tConquest

	iNumMinorCities = 0
	for city in cities.start(tTL).end(tBR):
		if city.getOwner() in players.minor(): iNumMinorCities += 1
		elif city.getOwner() != iPlayer: return False
		
	if 2 * iNumMinorCities > len(lAreaCities): return False
	
	return True


def conquerorWar(iPlayer, iTarget, iWarPlan):
	# reset at war counters because this is essentially a renewed war, will avoid cheap peace out of the conquerors
	if team(iPlayer).isAtWar(team(iTarget).getID()):
		team(iPlayer).AI_setAtWarCounter(team(iTarget).getID(), 0)
		team(iTarget).AI_setAtWarCounter(team(iPlayer).getID(), 0)
		
		team(iPlayer).AI_setWarPlan(team(iTarget).getID(), iWarPlan)
		
	# otherwise declare war
	else:
		declareWar(iPlayer, iTarget, iWarPlan)

	
def spawnConquerors(iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns, iWarPlan = WarPlanTypes.WARPLAN_TOTAL):
	iCiv = civ(iPlayer)
	
	if not player(iPlayer).isAlive():
		for iTech in sta.getResurrectionTechs(iPlayer):
			team(iPlayer).setHasTech(iTech, True, iPlayer, False, False)

	lCities = []
	for city in cities.start(tTL).end(tBR):
		if city.getOwner() != iPlayer and not team(city).isVassal(iPlayer):
			lCities.append(city)
			
	targetCities = cities.start(tTL).end(tBR).notowner(iPlayer).where(lambda city: not team(city).isVassal(iPlayer)).lowest(iNumTargets, lambda city: (city.getOwner() == iPreferredTarget, distance(city, capital(iPlayer))))
	owners = set(city.getOwner() for city in targetCities)
			
	if iPreferredTarget >= 0 and iPreferredTarget not in owners and player(iPreferredTarget).isAlive():
		conquerorWar(iPlayer, iPreferredTarget, iWarPlan)
			
	for iOwner in owners:
		conquerorWar(iPlayer, iOwner, iWarPlan)
		message(iOwner, 'TXT_KEY_UP_CONQUESTS_TARGET', name(iPlayer))
		
	for city in targetCities:
		iExtra = 0
		if active() not in [iPlayer, city.getOwner()]: 
			iExtra += 1
			
		if iCiv == iMongols and not player(iPlayer).isHuman():
			iExtra += 1
		
		tPlot = findNearestLandPlot(city, iPlayer)
		
		iBestInfantry = getBestInfantry(iPlayer)
		iBestSiege = getBestSiege(iPlayer)
		
		if iCiv == iGreece:
			iBestInfantry = iHoplite
			iBestSiege = iCatapult
		
		makeUnits(iPlayer, iBestInfantry, tPlot, 2 + iExtra, UnitAITypes.UNITAI_ATTACK_CITY)
		makeUnits(iPlayer, iBestSiege, tPlot, 1 + 2*iExtra, UnitAITypes.UNITAI_ATTACK_CITY)
		
		if iCiv == iGreece:
			makeUnit(iPlayer, iCompanion, tPlot, UnitAITypes.UNITAI_ATTACK_CITY)
		
		if iCiv == iTamils:
			makeUnit(iPlayer, iWarElephant, tPlot, UnitAITypes.UNITAI_ATTACK_CITY)
			
		if iCiv == iSpain:
			makeUnits(iPlayer, getBestCavalry(iPlayer), tPlot, 2 * iExtra, UnitAITypes.UNITAI_ATTACK_CITY)
			
		if iCiv == iTurks:
			makeUnits(iPlayer, getBestCavalry(iPlayer), tPlot, 2 + iExtra, UnitAITypes.UNITAI_ATTACK_CITY)


def declareWar(iPlayer, iTarget, iWarPlan):
	if team(iPlayer).isVassal(iTarget):
		team(iPlayer).setVassal(iTarget, False, False)
		
	team(iPlayer).declareWar(iTarget, True, iWarPlan)


def planWars(iGameTurn):
	# skip if there is a world war
	if iGameTurn > year(1500):
		iCivsAtWar = 0
		for iLoopPlayer in players.major():
			if team(iLoopPlayer).getAtWarCount(True) > 0:
				iCivsAtWar += 1
		if 100 * iCivsAtWar / game.countCivPlayersAlive() > 50:
			data.iNextTurnAIWar = iGameTurn + getNextInterval(iGameTurn)
			return

	iAttackingPlayer = determineAttackingPlayer()
	iTargetPlayer = determineTargetPlayer(iAttackingPlayer)
	
	if iAttackingPlayer is None:
		return

	data.players[iAttackingPlayer].iAggressionLevel = 0
	
	if iTargetPlayer == -1:
		return
		
	if team(iAttackingPlayer).canDeclareWar(iTargetPlayer):
		team(iAttackingPlayer).AI_setWarPlan(iTargetPlayer, WarPlanTypes.WARPLAN_PREPARING_LIMITED)
	
	data.iNextTurnAIWar = iGameTurn + getNextInterval(iGameTurn)


def determineAttackingPlayer():
	return players.major().alive().where(possibleTargets).maximum(lambda p: data.players[p].iAggressionLevel)


def possibleTargets(iPlayer):
	return players.major().without(iPlayer).where(lambda p: team(iPlayer).canDeclareWar(player(p).getTeam()))


def determineTargetPlayer(iPlayer):
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iCiv = civ(iPlayer)
	
	lPotentialTargets = []
	lTargetValues = [0 for _ in players.major()]

	# determine potential targets
	for iLoopPlayer in possibleTargets(iPlayer):
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
			if turn() > player(iLoopPlayer).getLastBirthTurn() + turns(20):
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
		if iLoopCiv in [iNetherlands, iPortugal, iItaly]:
			lTargetValues[iLoopPlayer] *= 4
			lTargetValues[iLoopPlayer] /= 5
			
		# no suicide
		if iCiv == iNetherlands:
			if iLoopCiv in [iFrance, iHolyRome, iGermany]:
				lTargetValues[iLoopPlayer] /= 2
		elif iCiv == iPortugal:
			if iLoopCiv == iSpain:
				lTargetValues[iLoopPlayer] /= 2
		elif iCiv == iItaly:
			if iLoopCiv in [iFrance, iHolyRome, iGermany]:
				lTargetValues[iLoopPlayer] /= 2
				
	return find_max(lTargetValues).index


def getNextInterval(iGameTurn):
	if iGameTurn > year(1600):
		iMinInterval = iMinIntervalLate
		iMaxInterval = iMaxIntervalLate
	else:
		iMinInterval = iMinIntervalEarly
		iMaxInterval = iMaxIntervalEarly
		
	iMinInterval = turns(iMinInterval)
	iMaxInterval = turns(iMaxInterval)
	
	return rand(iMinInterval, iMaxInterval)