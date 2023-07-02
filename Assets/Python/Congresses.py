# Rhye's and Fall of Civilization - World Congresses

from CvPythonExtensions import *
import CvUtil
import PyHelpers
from RFCUtils import *
from Consts import *
import CityNameManager as cnm
from StoredData import data # edead

from Events import handler
from Popups import popup

import Popups

from Locations import *
from Core import *


### Event Handlers ###

@handler("BeginActivePlayerTurn")
def checkTurn(iPlayer, iGameTurn):
	if isCongressEnabled():
		if turn() == data.iCongressTurn:
			Congress().start()
			scheduleCongress()


@handler("techAcquired")
def onTechAcquired(iTech):
	if iTech == iNationalism and game.countKnownTechNumTeams(iNationalism) == 1:
		scheduleCongress()


@handler("buildingBuilt")
def onBuildingBuilt(city, iBuilding):
	if iBuilding == iPalaceOfNations:
		scheduleCongress()


@handler("changeWar")
def onChangeWar(bWar, iPlayer, iOtherPlayer):
	if is_minor(iPlayer) or is_minor(iOtherPlayer):
		return

	if isCongressEnabled():
		if bWar and not isGlobalWar():
			attackers, defenders = determineAlliances(iPlayer, iOtherPlayer)
			
			if startsGlobalWar(attackers, defenders):
				iAttacker = attackers.maximum(lambda p: team(p).getPower(True))
				iDefender = defenders.maximum(lambda p: team(p).getPower(True))
			
				data.iGlobalWarAttacker = iAttacker
				data.iGlobalWarDefender = iDefender
		
		if not bWar and data.iGlobalWarAttacker in [iPlayer, iOtherPlayer] and data.iGlobalWarDefender in [iPlayer, iOtherPlayer]:
			endGlobalWar(iPlayer, iOtherPlayer)
			
### Global Methods ###

def getCongressInterval():
	if game.getBuildingClassCreatedCount(infos.building(iPalaceOfNations).getBuildingClassType()) > 0:
		return turns(4)
		
	return turns(15)
	
def scheduleCongress():
	if data.iCongressTurn <= turn():
		data.iCongressTurn = turn() + getCongressInterval()
	else:
		data.iCongressTurn = min(data.iCongressTurn, turn() + getCongressInterval())

def isCongressEnabled():
	if data.bNoCongressOption:
		return False

	if game.getBuildingClassCreatedCount(infos.building(iUnitedNations).getBuildingClassType()) > 0:
		return False
		
	return (game.countKnownTechNumTeams(iNationalism) > 0)
	
def startsGlobalWar(attackers, defenders):
	if attackers < 2: return False
	if defenders < 2: return False
	
	worldPowers = players.major().alive().where(lambda p: not team(p).isAVassal()).sort(lambda p: team(p).getPower(True), True).fraction(4)
	participatingPowers = worldPowers.where(lambda p: p in attackers + defenders)
	
	return 2 * participatingPowers.count() >= worldPowers.count()
				
def determineAlliances(iAttacker, iDefender):
	attackers = players.major().alive().where(team(iDefender).isAtWar)
	defenders = players.major().alive().where(team(iAttacker).isAtWar)
	
	return attackers.without(defenders), defenders.without(attackers)

def isGlobalWar():
	return (data.iGlobalWarAttacker != -1 and data.iGlobalWarDefender != -1)
	
def endGlobalWar(iAttacker, iDefender):
	if not player(iAttacker).isAlive() or not player(iDefender).isAlive():
		return
		
	if data.iCongressTurn == turn() + getCongressInterval():
		return
	
	lAttackers = [iAttacker]
	lDefenders = [iDefender]
	
	lAttackerAllies, lDefenderAllies = determineAlliances(iAttacker, iDefender)
	
	lAttackers += lAttackerAllies
	lDefenders += lDefenderAllies
	
	# force peace for all allies of the belligerents
	for iLoopPlayer in lAttackers:
		if not player(iLoopPlayer).isAlive(): continue
		if team(iLoopPlayer).isAVassal(): continue
		if iLoopPlayer == iAttacker: continue
		team(iLoopPlayer).makePeace(iDefender)
		
	for iLoopPlayer in lDefenders:
		if not player(iLoopPlayer).isAlive(): continue
		if team(iLoopPlayer).isAVassal(): continue
		if iLoopPlayer == iDefender: continue
		team(iLoopPlayer).makePeace(iAttacker)
		
	if game.determineWinner(iAttacker, iDefender) == iAttacker:
		lWinners = lAttackers
		lLosers = lDefenders
	else:
		lWinners = lDefenders
		lLosers = lAttackers
	
	Congress(players.of(*lWinners), players.of(*lLosers)).start()
	
def getNumInvitations():
	return min(10, game.countCivPlayersAlive())
			
class Congress:
	
	### Constructor ###
	
	def __init__(self, winners = players.none(), losers = players.none()):
		self.sHostCityName = ""
		self.invites = players.none()
		self.winners = winners
		self.losers = losers
		self.bPostWar = False
		self.dPossibleClaims = {}
		self.dCityClaims = {}
		self.dVotes = {}
		self.lHumanVotes = []
		self.iNumHumanVotes = 0
		self.dVotingMemory = {}
		self.dVotedFor = {}
		self.lAssignments = []
		self.lColonies = []
		self.lHumanAssignments = []
		self.iNumHumanAssignments = 0
		self.dPossibleBelligerents = {}
		self.lPossibleBribes = []
		self.iNumBribes = 0
		self.lBriberyOptions = []
		
		self.introduction = popup.option(self.applyIntroduction, "TXT_KEY_CONGRESS_OK", '').build()
			
		self.claim_city = popup.text("TXT_KEY_CONGRESS_CLAIM_CITY") \
							   .selection(self.applyClaimCity) \
							   .option(self.noClaim, "TXT_KEY_CONGRESS_NO_REQUEST", event_cancel) \
							   .build()
	
		self.vote_claim = popup.option(self.approveClaim, "TXT_KEY_POPUP_VOTE_YES") \
							   .option(self.abstainClaim, "TXT_KEY_POPUP_ABSTAIN") \
							   .option(self.denyClaim, "TXT_KEY_POPUP_VOTE_NO") \
							   .build()
		
		base_bribery = popup.option(self.noBribe, "TXT_KEY_CONGRESS_NO_BRIBE", event_cancel) \
		                    .option(self.cannotAffordBribe, "TXT_KEY_CONGRESS_CANNOT_AFFORD_BRIBE", event_cancel) \
							.selection(self.bribeGold, "TXT_KEY_CONGRESS_BRIBE_GOLD", infos.commerce(CommerceTypes.COMMERCE_GOLD).getButton()) \
							.selection(self.bribeManipulate, "TXT_KEY_CONGRESS_MANIPULATION", 'Art/Interface/Buttons/Espionage.dds')
		
		self.bribe_other_city = base_bribery.text("TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_CITY").selection(self.applyBribe, "TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_CITY").build()
		self.bribe_other_plot = base_bribery.text("TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_COLONY").selection(self.applyBribe, "TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_COLONY").build()
		self.bribe_own_city = base_bribery.text("TXT_KEY_CONGRESS_BRIBE_OWN_CITY").selection(self.applyBribe, "TXT_KEY_CONGRESS_BRIBE_OWN_CITY").build()
		self.bribe_own_territory = base_bribery.text("TXT_KEY_CONGRESS_BRIBE_OWN_TERRITORY").selection(self.applyBribe, "TXT_KEY_CONGRESS_BRIBE_OWN_TERRITORY").build()
		
		self.bribery_result = popup.option(self.applyBriberyResult, "TXT_KEY_CONGRESS_OK", '').build()
		
		demand = popup.option(self.acceptDemand, "TXT_KEY_CONGRESS_ACCEPT").option(self.refuseDemand, "TXT_KEY_CONGRESS_REFUSE")
		
		self.demand_city = demand.text("TXT_KEY_CONGRESS_DEMAND_CITY").build()
		self.demand_plot = demand.text("TXT_KEY_CONGRESS_DEMAND_PLOT").build()
			
		self.results = popup.cancel("TXT_KEY_CONGRESS_OK", "").build()
	
	### Popups ###
	
	def startIntroduction(self, bHumanInvited, bHumanInGlobalWar = False):
		other_players = itemize(self.invites.without(active()), fullname)
		
		if self.bPostWar:
			if bHumanInvited:
				if active() in self.winners:
					text_key = "TXT_KEY_CONGRESS_INTRODUCTION_WAR_WON"
				elif active() in self.losers:
					text_key = "TXT_KEY_CONGRESS_INTRODUCTION_WAR_LOST"
				else:
					text_key = "TXT_KEY_CONGRESS_INTRODUCTION_WAR"
			else:
				text_key = "TXT_KEY_CONGRESS_INTRODUCTION_WAR_AI"
		
		elif bHumanInvited:
			text_key = "TXT_KEY_CONGRESS_INTRODUCTION"
		elif bHumanInGlobalWar:
			text_key = "TXT_KEY_CONGRESS_INTRODUCTION_AI_WAR_EXCLUDED"
		else:
			text_key = "TXT_KEY_CONGRESS_INTRODUCTION_AI"
		
		self.introduction.text(text_key, self.sHostCityName, other_players).applyIntroduction().launch()
		
	def applyIntroduction(self):
		# check one more time if player has collapsed in the meantime
		self.invites = self.invites.without(players.all().notalive())
	
		# move AI claims here so they are made on the same turn as they are resolved - otherwise change of ownership might confuse things
		for iLoopPlayer in self.invites:
			if not self.canClaim(iLoopPlayer): continue
			self.dPossibleClaims[iLoopPlayer] = self.selectClaims(iLoopPlayer)
			
		for iLoopPlayer in self.invites:
			if iLoopPlayer not in self.dPossibleClaims: continue
			
			if not player(iLoopPlayer).isHuman():
				self.makeClaimAI(iLoopPlayer)
	
		if active() in self.dPossibleClaims:
			# human still has to make a claim
			self.makeClaimHuman()
		else:
			# human cannot make claims, so let the AI vote
			self.voteOnClaims()

	def startClaimCity(self):
		event = self.claim_city.text(self.sHostCityName)
		
		for x, y, _ in self.dPossibleClaims[active()]:
			city = city_(x, y)
			if city:
				event.applyClaimCity(city.getName(), button=infos.civ(city).getButton())
			else:
				event.applyClaimCity(cnm.getFoundName(active(), (x, y)), button='Art/Interface/Buttons/Actions/FoundCity.dds')
				
		event.noClaim().launch()

	def applyClaimCity(self, iChoice):
		self.dCityClaims[active()] = self.dPossibleClaims[active()][iChoice]
		self.voteOnClaims()
	
	def noClaim(self):
		self.voteOnClaims()
		
	def startVoteCityEvent(self, iClaimant, (x, y)):
		plot = plot_(x, y)
		
		if plot.isRevealed(active(), False):
			plot.cameraLookAt()
		
		if plot.isCity():
			event = self.vote_claim.text("TXT_KEY_CONGRESS_REQUEST_CITY", name(iClaimant), adjective(plot), city(plot).getName())
		elif plot.getOwner() == iClaimant:
			event = self.vote_claim.text("TXT_KEY_CONGRESS_REQUEST_SETTLE_OWN", name(iClaimant), cnm.getFoundName(iClaimant, (x, y)))
		elif plot.isOwned():
			event = self.vote_claim.text("TXT_KEY_CONGRESS_REQUEST_SETTLE_FOREIGN", name(iClaimant), adjective(plot), cnm.getFoundName(iClaimant, (x, y)))
		else:
			event = self.vote_claim.text("TXT_KEY_CONGRESS_REQUEST_SETTLE_EMPTY", name(iClaimant), cnm.getFoundName(iClaimant, (x, y)))
			
		event.approveClaim().abstainClaim().denyClaim().launch(iClaimant, plot.getOwner())
		
	def approveClaim(self, iClaimant, iOwner):
		self.applyClaimVote(iClaimant, iOwner, 1)
		
	def abstainClaim(self, iClaimant, iOwner):
		self.applyClaimVote(iClaimant, iOwner, 0)
	
	def denyClaim(self, iClaimant, iOwner):
		self.applyClaimVote(iClaimant, iOwner, -1)
		
	def applyClaimVote(self, iClaimant, iOwner, iVote):
		self.vote(active(), iClaimant, iVote)
		
		if iClaimant in self.dVotingMemory:
			self.dVotingMemory[iClaimant] += iVote
			
		if iOwner >= 0 and iOwner in self.dVotingMemory:
			self.dVotingMemory[iOwner] -= iVote
		
		self.iNumHumanVotes += 1
		
		# still votes to cast: start a new popup, otherwise let the AI vote
		if self.iNumHumanVotes < len(self.lHumanVotes):
			iNextClaimant, x, y = self.lHumanVotes[self.iNumHumanVotes]
			self.startVoteCityEvent(iNextClaimant, (x, y))
		else:
			self.voteOnClaimsAI()
			
	def startBribery(self, iBribedPlayer, iClaimant, (x, y), iDifference, iClaimValidity):
		plot = plot_(x, y)
		
		bHumanClaim = player(iClaimant).isHuman()
		bCity = plot.isCity()
		
		if plot.isRevealed(active(), False):
			plot.cameraLookAt()
		
		if bHumanClaim:
			if bCity:
				event = self.bribe_other_city.text(adjective(iBribedPlayer), adjective(plot), city(plot).getName())
			else:
				event = self.bribe_other_plot.text(adjective(iBribedPlayer), adjective(plot), closestCity(plot, iBribedPlayer, same_continent=True).getName())
		else:	
			if bCity:
				event = self.bribe_own_city.text(adjective(iBribedPlayer), adjective(iClaimant), city(plot).getName())
			else:
				event = self.bribe_own_territory.text(adjective(iBribedPlayer), adjective(iClaimant), closestCity(plot, active(), same_continent=True).getName())
		
		iCost = iDifference * player(iBribedPlayer).calculateTotalCommerce() / 5
		
		# make sure costs are positive
		if iCost < 100: iCost = 100
		
		iTreasury = player().getGold()
		iEspionageSpent = team().getEspionagePointsAgainstTeam(iBribedPlayer)
		
		if bHumanClaim:
			# both types of influence have a 50 / 75 / 90 percent chance based on the investment for an averagely valid claim (= 25)
			iLowChance = 25 + iClaimValidity
			iMediumChance = 50 + iClaimValidity
			iHighChance = 65 + iClaimValidity
		else:
			# both types of influence have a 50 / 75 / 90 percent chance based on the investment for an averagely valid claim (= 25)
			iLowChance = 75 - iClaimValidity
			iMediumChance = 100 - iClaimValidity
			iHighChance = 115 - iClaimValidity
		
		self.lBriberyOptions = []
		
		if iTreasury >= iCost / 2: self.lBriberyOptions.append((0, iCost / 2, iLowChance))
		if iTreasury >= iCost: self.lBriberyOptions.append((0, iCost, iMediumChance))
		if iTreasury >= iCost * 2: self.lBriberyOptions.append((0, iCost * 2, iHighChance))
		
		if iEspionageSpent >= iCost / 2: self.lBriberyOptions.append((3, iCost / 4, iLowChance))
		if iEspionageSpent >= iCost: self.lBriberyOptions.append((3, iCost / 2, iMediumChance))
		if iEspionageSpent >= iCost * 2: self.lBriberyOptions.append((3, iCost, iHighChance))
		
		if not self.lBriberyOptions:
			event.cannotAffordBribe().launch(iBribedPlayer, iClaimant, iClaimValidity)
			return
		
		dChanceText = {
			iLowChance : "TXT_KEY_CONGRESS_CHANCE_AVERAGE",
			iMediumChance : "TXT_KEY_CONGRESS_CHANCE_HIGH",
			iHighChance : "TXT_KEY_CONGRESS_CHANCE_VERY_HIGH",
		}
		
		for iCommerceType, iCost, iThreshold in self.lBriberyOptions:
			if iCommerceType == 0:
				event.bribeGold(iCost, text(dChanceText[iThreshold]))
			elif iCommerceType == 3: 
				event.bribeManipulate(iCost, text(dChanceText[iThreshold]))
		
		event.noBribe().launch(iBribedPlayer, iClaimant, iClaimValidity)
		
	def noBribe(self, iBribedPlayer, iClaimant, iClaimValidity):
		self.randomVote(iBribedPlayer, iClaimant, iClaimValidity)
		
	def cannotAffordBribe(self, iBribedPlayer, iClaimant, iClaimValidity):
		self.randomVote(iBribedPlayer, iClaimant, iClaimValidity)
		
	def randomVote(self, iBribedPlayer, iClaimant, iClaimValidity):
		# if no bribery option was chosen, the civ votes randomly as usual
		if rand(50) < iClaimValidity:
			self.vote(iBribedPlayer, iClaimant, 1)
		else:
			self.vote(iBribedPlayer, iClaimant, -1)
			
		# to continue the process
		self.applyBriberyResult()
		
	def bribeGold(self, iChoice, iBribedPlayer, iClaimant, iClaimValidity):
		self.applyBribe(iChoice, iBribedPlayer, iClaimant, iClaimValidity)
	
	def bribeManipulate(self, iChoice, iBribedPlayer, iClaimant, iClaimValidity):
		self.applyBribe(iChoice, iBribedPlayer, iClaimant, iClaimValidity)
		
	def applyBribe(self, iChoice, iBribedPlayer, iClaimant, iClaimValidity):
		iCommerceType, iCost, iThreshold = self.lBriberyOptions[iChoice]
		iRand = rand(100)
		
		if iCommerceType == 0: player().changeGold(-iCost)
		elif iCommerceType == 3: team().changeEspionagePointsAgainstTeam(iBribedPlayer, -iCost)
		
		bHumanClaim = player(iClaimant).isHuman()
		bSuccess = (iRand < iThreshold)
		
		iVote = 1
		if not bHumanClaim: iVote *= -1
		if not bSuccess: iVote *= -1
		
		self.vote(iBribedPlayer, iClaimant, iVote)
		
		if not bSuccess:
			player(iBribedPlayer).AI_changeMemoryCount(active(), MemoryTypes.MEMORY_STOPPED_TRADING_RECENT, 1)
			player(iBribedPlayer).AI_changeAttitudeExtra(active(), -2)
		
		self.startBriberyResult(iBribedPlayer, iClaimant, bHumanClaim, bSuccess)
				
	def startBriberyResult(self, iBribedPlayer, iClaimant, bHumanClaim, bSuccess):
		if bSuccess:
			if bHumanClaim:
				event = self.bribery_result.text("TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_SUCCESS", name(iBribedPlayer))
			else:
				event = self.bribery_result.text("TXT_KEY_CONGRESS_BRIBE_THEIR_CLAIM_SUCCESS", name(iBribedPlayer))
		else:
			if bHumanClaim:
				event = self.bribery_result.text("TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_FAILURE", name(iBribedPlayer))
			else:
				event = self.bribery_result.text("TXT_KEY_CONGRESS_BRIBE_THEIR_CLAIM_FAILURE", name(iBribedPlayer))
		
		event.applyBriberyResult().launch()
		
	def applyBriberyResult(self):
		# just continue to the next bribe if there is one
		self.iNumBribes += 1
		if self.iNumBribes < len(self.lPossibleBribes):
			iVoter, iClaimant, tPlot, iDifference, iClaimValidity = self.lPossibleBribes[self.iNumBribes]
			self.startBribery(iVoter, iClaimant, tPlot, iDifference, iClaimValidity)
		else:
			# otherwise continue with applying the votes
			self.applyVotes()
			
	def startDemand(self, iClaimant, (x, y)):
		plot = plot_(x, y)
		
		if plot.isRevealed(active(), False):
			plot.cameraLookAt()
			
		voted_yes = [iPlayer for iPlayer in self.dVotedFor[iClaimant] if not player(iPlayer).isHuman() and iPlayer != iClaimant]
			
		city = city_(plot)
		if city:
			event = self.demand_city.text(name(iClaimant), city.getName(), itemize(voted_yes, fullname))
		else:
			event = self.demand_plot.text(name(iClaimant), closestCity(plot, active(), same_continent=True).getName(), itemize(voted_yes, fullname))
		
		event.acceptDemand().refuseDemand().launch(iClaimant, x, y)
		
	def acceptDemand(self, iClaimant, x, y):
		city = city_(x, y)
		if city:
			self.assignCity(iClaimant, city.getOwner(), (x, y))
		else:
			self.foundColony(iClaimant, (x, y))
		
		self.continueAssignments()
			
	def refuseDemand(self, iClaimant):
		iVotes = self.dVotes[iClaimant]
		
		if iClaimant not in self.dPossibleBelligerents:
			self.dPossibleBelligerents[iClaimant] = 2 * iVotes
		else:
			self.dPossibleBelligerents[iClaimant] += 2 * iVotes
		
		for iVoter in self.dVotedFor[iClaimant]:
			if team(iVoter).isAVassal(): continue
			if iVoter not in self.dPossibleBelligerents:
				self.dPossibleBelligerents[iVoter] = iVotes
			else:
				self.dPossibleBelligerents[iVoter] += iVotes
		
		self.continueAssignments()
			
	def continueAssignments(self):
		self.iNumHumanAssignments += 1
		
		# still assignments to react to: start a new popup, otherwise show the results
		if self.iNumHumanAssignments < len(self.lHumanAssignments):
			iNextClaimant, tPlot = self.lHumanAssignments[self.iNumHumanAssignments]
			self.startDemand(iNextClaimant, tPlot)
		else:
			self.finishCongress()
			
	def startResults(self):
		if not autoplay():
			content = []
			content.append(("TXT_KEY_CONGRESS_RESULTS", self.sHostCityName))
			
			for sName, iOldOwner, iNewOwner in self.lAssignments:
				content.append(text("TXT_KEY_CONGRESS_RESULT_ASSIGNMENT", sName, adjective(iOldOwner), adjective(iNewOwner)))
				
			for sName, iOldOwner, iNewOwner in self.lColonies:
				if iOldOwner >= 0:
					content.append(("TXT_KEY_CONGRESS_RESULT_COLONY_TERRITORY", sName, adjective(iOldOwner), name(iNewOwner)))
				else:
					content.append(("TXT_KEY_CONGRESS_RESULT_COLONY", sName, name(iNewOwner)))
			
			if not self.lAssignments and not self.lColonies:
				content.append("TXT_KEY_CONGRESS_NO_RESULTS")
				
			if self.lAssignments or self.lColonies:
				text_key = "TXT_KEY_CONGRESS_RESULTS"
				
				content = []
				for sName, iOldOwner, iNewOwner in self.lAssignments:
					content.append(("TXT_KEY_CONGRESS_RESULT_ASSIGNMENT", sName, adjective(iOldOwner), adjective(iNewOwner)))
				
				for sName, iOldOwner, iNewOwner in self.lColonies:
					if iOldOwner >= 0:
						content.append(("TXT_KEY_CONGRESS_RESULT_COLONY_TERRITORY", sName, adjective(iOldOwner), name(iNewOwner)))
					else:
						content.append(("TXT_KEY_CONGRESS_RESULT_COLONY", sName, name(iNewOwner)))
						
				results = itemize(content, lambda row: text(row[0], *row[1:]))
			else:
				text_key = "TXT_KEY_CONGRESS_NO_RESULTS"
				results = tuple()
				
			self.results.text(text_key, self.sHostCityName, results).cancel().launch()
			
		# if this was triggered by a war, reset belligerents
		if isGlobalWar():
			data.iGlobalWarAttacker = -1
			data.iGlobalWarDefender = -1

	### Other Methods ###

	def start(self):
		self.bPostWar = self.winners.any()
		
		debug('Congress takes place')

		self.invite()
		
		if self.bPostWar:
			iHostPlayer = self.winners.alive().first()
		else:
			iHostPlayer = self.invites.where(lambda p: player(p).getNumCities() > 0).random()
			
		# normal congresses during war time may be too small because all civilisations are tied up in global wars
		if len(self.invites) < 3:
			data.iCongressTurn = turn() + getCongressInterval() / 2
			data.currentCongress = None
			return
		
		# if a war congress would be followed by a normal congress, delay it
		if self.bPostWar and data.iCongressTurn <= turn() + 1:
			data.iCongressTurn = turn() + getCongressInterval()
		
		# establish contact between all participants
		for iThisPlayer in self.invites:
			for iThatPlayer in self.invites:
				if iThisPlayer != iThatPlayer:
					tThisPlayer = team(iThisPlayer)
					if not tThisPlayer.canContact(iThatPlayer): tThisPlayer.meet(iThatPlayer, False)

		self.sHostCityName = cities.core(iHostPlayer).owner(iHostPlayer).random().getName()
		
		# moved selection of claims after the introduction event so claims and their resolution take place at the same time
		if active() in self.invites:
			self.startIntroduction(True)
				
		# procedure continues from the makeClaimHuman event
		
		bHumanInGlobalWar = False
		if isGlobalWar():
			lAttackers, lDefenders = determineAlliances(data.iGlobalWarAttacker, data.iGlobalWarDefender)
			bHumanInGlobalWar = active() in lAttackers + lDefenders
		
		# unless the player isn't involved, in that case resolve from here
		if active() not in self.invites:
			# since Congresses now can occur during autoplay, don't display these congresses to the player
			if not autoplay():
				self.startIntroduction(False, bHumanInGlobalWar)
			else:
				# select claims first, then move on to voting directly since the player isn't involved
				for iLoopPlayer in self.invites:
					if not self.canClaim(iLoopPlayer): continue
					self.dPossibleClaims[iLoopPlayer] = self.selectClaims(iLoopPlayer)
					
				for iLoopPlayer in self.invites:
					if iLoopPlayer not in self.dPossibleClaims: continue
					
					if not player(iLoopPlayer).isHuman():
						self.makeClaimAI(iLoopPlayer)
						
				self.voteOnClaims()
			
	def voteOnClaims(self):
		# only humans vote so AI memory can influence their actions later
		for iVoter in self.invites:
			self.dVotes[iVoter] = 0
			self.dVotingMemory[iVoter] = 0
			self.dVotedFor[iVoter] = []
			if player(iVoter).isHuman():
				self.voteOnClaimsHuman()
				
		# procedure continues from the voteOnClaimsHuman event
				
		# unless the player isn't involved, in that case resolve from here
		if active() not in self.invites:
			self.voteOnClaimsAI()
			
	def applyVotes(self):
		dResults = {}
		
		for iClaimant in self.dCityClaims:
			x, y, iValue = self.dCityClaims[iClaimant]
			if self.dVotes[iClaimant] > 0:
				# only one player may receive a plot/city in case multiple civs claimed it (most votes)
				if (x, y) not in dResults:
					dResults[(x, y)] = (iClaimant, self.dVotes[iClaimant])
				else:
					iOtherClaimant, iVotes = dResults[(x, y)]
					if self.dVotes[iClaimant] > iVotes: dResults[(x, y)] = (iClaimant, self.dVotes[iClaimant])
					
		for (x, y), (iClaimant, iVotes) in dResults.items():
			plot = plot_(x, y)
			
			bCanRefuse = self.canRefuse(iClaimant, plot)
			
			if plot.isCity():
				self.lAssignments.append((plot.getPlotCity().getName(), plot.getOwner(), iClaimant))
				if bCanRefuse:
					self.lHumanAssignments.append((iClaimant, (x, y)))
				else:
					self.assignCity(iClaimant, plot.getOwner(), (x, y))
			else:
				self.lColonies.append((cnm.getFoundName(iClaimant, (x, y)), plot.getOwner(), iClaimant))
				if bCanRefuse:
					self.lHumanAssignments.append((iClaimant, (x, y)))
				else:
					self.foundColony(iClaimant, (x, y))
					
		# allow human player to refuse in case his cities were claimed -> last decision leads to result event
		if len(self.lHumanAssignments) > 0:
			iClaimant, tPlot = self.lHumanAssignments[0]
			self.startDemand(iClaimant, tPlot)
		else:
			# without human cities affected, finish the congress immediately
			self.finishCongress()
	
	def canRefuse(self, iClaimant, plot):
		if not self.isHumanOwned(plot):
			return False
		
		if active() in self.dVotedFor[iClaimant]:
			return False
		
		if self.bPostWar and active() in self.losers:
			return False
			
		return True
		
	def isHumanOwned(self, plot):
		if plot.getOwner() == active():
			return True
		
		if plot.isOwned() and team(plot.getTeam()).isVassal(player().getTeam()):
			return True
		
		return False
					
	def assignCity(self, iPlayer, iOwner, (x, y)):
		assignedCity = city(x, y)
		
		defenders = units.at(x, y).owner(iOwner)
		if iOwner in players.major():
			relocateUnitsToCore(iOwner, defenders)
		else:
			killUnits(defenders)
		
		completeCityFlip(assignedCity, iPlayer, iOwner, 80, False, False, True, bPermanentCultureChange=False)
		
		bLimitedDefenders = player(iPlayer).isHuman() or isIsland(assignedCity)
		iNumDefenders = bLimitedDefenders and 2 or max(2, player(iPlayer).getCurrentEra()-1)
		createRoleUnit(iPlayer, (x, y), iDefend, iNumDefenders)
		
	def foundColony(self, iPlayer, (x, y)):
		plot = plot_(x, y)
		
		if plot.isOwned(): convertPlotCulture(plot, iPlayer, 100, True)
		
		if player(iPlayer).isHuman():
			makeUnit(iPlayer, iSettler, plot)
		else:
			player(iPlayer).found(x, y)
			
		createGarrisons(plot, iPlayer, 2)
	
	def getWarResponseValue(self, iBelligerent):
		iValue = 5 * max(0, self.dPossibleBelligerents[iBelligerent] - getNumInvitations())
		iValue += 5 * (2 - player(iBelligerent).AI_getAttitude(active()))
		iValue -= dPatienceThreshold[iBelligerent]
		
		if team(iBelligerent).isDefensivePact(team().getID()):
			iValue -= 20
		elif team(iBelligerent).isForcePeace(team().getID()):
			iValue -= 10
		
		if team(iBelligerent).AI_getWarPlan(team().getID()) != -1:
			iValue += 10
		
		return iValue
	
	def declareWar(self, iAttacker, iDefender):
		team(iAttacker).setDefensivePact(iDefender, False)
		team(iAttacker).declareWar(iDefender, False, WarPlanTypes.WARPLAN_DOGPILE)
		
	def finishCongress(self):
		# declare war against human if they refused demands
		iGlobalWarModifier = 0
		tHuman = team()
		for iLoopPlayer in players.major():
			if tHuman.isDefensivePact(iLoopPlayer):
				iGlobalWarModifier += 10
				
		belligerents = players.of(*self.dPossibleBelligerents.keys())
		iBaseThreshold = iGlobalWarModifier + 10
		
		worstEnemies, belligerents = belligerents.split(lambda p: player(p).getWorstEnemy() == active())
		for iBelligerent in worstEnemies:
			self.declareWar(iBelligerent, active())
			iBaseThreshold += 10
		
		defensivePacts, belligerents = belligerents.split(lambda p: team().isDefensivePact(player(p).getTeam()))
		for iBelligerent, iValue in belligerents.sort(self.getWarResponseValue).valued(self.getWarResponseValue):
			if rand(100) >= iBaseThreshold - iValue:
				self.declareWar(iBelligerent, active())
				iBaseThreshold += 10
		
		for iBelligerent, iValue in defensivePacts.sort(self.getWarResponseValue).valued(self.getWarResponseValue):
			if rand(100) >= iBaseThreshold - iValue:
				self.declareWar(iBelligerent, active())
				iBaseThreshold += 10
				
		# display Congress results
		self.startResults()
				
	def voteOnClaimsHuman(self):
		for iClaimant in self.dCityClaims:
			if not player(iClaimant).isHuman():
				x, y, iValue = self.dCityClaims[iClaimant]
				self.lHumanVotes.append((iClaimant, x, y))
				
		if len(self.lHumanVotes) > 0:
			iClaimant, x, y = self.lHumanVotes[0]
			self.startVoteCityEvent(iClaimant, (x, y))
			
	def voteOnClaimsAI(self):
		for iClaimant in self.dCityClaims:
			x, y, iValue = self.dCityClaims[iClaimant]
			
			lVoters = self.invites.entities()
			
			plot = plot_(x, y)
			if plot.isOwned():
				iOwner = plot.getOwner()
				if iOwner not in lVoters and iOwner in players.major().highest(getNumInvitations(), game.getPlayerRank):
					lVoters.append(iOwner)
			
			if active() in lVoters: lVoters.remove(active())
			if iClaimant in lVoters: lVoters.remove(iClaimant)
			
			for iVoter in lVoters:
				tResult = self.voteOnCityClaimAI(iVoter, iClaimant, (x, y), iValue)
				
				# if a human bribe is possible, a set of data has been returned, so add it to the list of possible bribes
				if tResult: self.lPossibleBribes.append(tResult)
						
		# if bribes are possible, handle them now, votes are applied after the last bribe event
		if len(self.lPossibleBribes) > 0:
			iVoter, iClaimant, tPlot, iDifference, iClaimValidity = self.lPossibleBribes[0]
			self.startBribery(iVoter, iClaimant, tPlot, iDifference, iClaimValidity)
		else:
		# continue with applying the votes right now in case there are no bribes
			self.applyVotes()
			
	def voteOnCityClaimAI(self, iVoter, iClaimant, (x, y), iClaimValue):
		iFavorClaimant = 0
		iFavorOwner = 0
		
		iClaimValidity = 0
		
		plot = plot_(x, y)
		pVoter = player(iVoter)
		tVoter = team(iVoter)
		
		iOwner = plot.getOwner()
		iNumPlayersAlive = game.countCivPlayersAlive()
		
		bCity = plot.isCity()
		bOwner = (iOwner >= 0)
		bOwnClaim = (iClaimant == iVoter)
		
		bRecolonise = plot.getRegionID() in lAmerica and civ(iClaimant) in dCivGroups[iCivGroupEurope] and civ(iOwner) in dCivGroups[iCivGroupAmerica] and civ(iOwner) in dTechGroups[iTechGroupWestern]
		
		if bCity: city = plot.getPlotCity()
		if bOwner: 
			bMinor = is_minor(iOwner)
			bOwnCity = (iOwner == iVoter)
			bWarClaim = (iClaimant in self.winners and iOwner in self.losers)
		
		# everyone agrees on AI American claims in the west, unless owner is native to the Americas
		if civ(iClaimant) == iAmerica and iVoter != iOwner and civ(iOwner) not in dCivGroups[iCivGroupAmerica]:
			if plot in plots.rectangle(tAmericanClaims):
				self.vote(iVoter, iClaimant, 1)
				return
			
		# player factors
		if bOwner and not bMinor and not bOwnCity and not bOwnClaim:
			# player rank
			iFavorClaimant += iNumPlayersAlive / 2 - game.getPlayerRank(iClaimant)
			iFavorOwner += iNumPlayersAlive / 2 - game.getPlayerRank(iOwner)
			
			# player relations
			iFavorClaimant += 5 * (pVoter.AI_getAttitude(iClaimant) - 2)
			iFavorOwner += 5 * (pVoter.AI_getAttitude(iOwner) - 2)
			
			# defensive pacts
			if tVoter.isDefensivePact(iClaimant): iFavorClaimant += 5
			if tVoter.isDefensivePact(iOwner): iFavorOwner += 5
			
			# at war
			if tVoter.isAtWar(iClaimant): iFavorClaimant -= 10
			if tVoter.isAtWar(iOwner): iFavorOwner -= 10
			
			# neighbors
			if not game.isNeighbors(iVoter, iClaimant): iFavorClaimant += 5
			if not game.isNeighbors(iVoter, iOwner): iFavorOwner += 10
			
			# vassalage
			if tVoter.isVassal(iClaimant): iFavorClaimant += 20
			if tVoter.isVassal(iOwner): iFavorOwner += 20
			
			if team(iClaimant).isVassal(iVoter): iFavorClaimant += 10
			if team(iOwner).isVassal(iVoter): iFavorOwner += 10
			
			if not plot.isPlayerCore(iOwner) or plot.isPlayerCore(iClaimant):
				# French UP
				if civ(iClaimant) == iFrance: iFavorClaimant += 10
				if civ(iOwner) == iFrance: iFavorOwner += 10
			
				# Palace of Nations
				if player(iClaimant).isHasBuildingEffect(iPalaceOfNations): iFavorClaimant += 10
			
			# AI memory of human voting behavior
			if player(iClaimant).isHuman() and iVoter in self.dVotingMemory: iFavorClaimant += 5 * self.dVotingMemory[iVoter]
			if player(iOwner).isHuman() and iVoter in self.dVotingMemory: iFavorOwner += 5 * self.dVotingMemory[iVoter]
			
		# if we don't dislike them, agree with the value of their claim
		if pVoter.AI_getAttitude(iClaimant) >= AttitudeTypes.ATTITUDE_CAUTIOUS: iClaimValidity += iClaimValue
			
		# French UP
		if civ(iClaimant) == iFrance: iClaimValidity += 5
		
		if not bRecolonise:
		
			# plot factors
			# plot culture
			if bOwner:
				iClaimValidity += (100 * plot.getCulture(iClaimant) / plot.countTotalCulture()) / 20
				
				# after wars: claiming from a non-participant has less legitimacy unless its your own claim
				if self.bPostWar and not bOwnClaim and iOwner not in self.losers:
					iClaimValidity -= 10
				
			# generic settler map bonus
			iClaimantValue = plot.getPlayerSettlerValue(iClaimant)
			if iClaimantValue >= 90:
				iClaimValidity += max(1, iClaimantValue / 100)

			# Europeans support colonialism unless they want the plot for themselves (not against Western civs)
			if civ(iVoter) in dCivGroups[iCivGroupEurope]:
				if civ(iClaimant) in dCivGroups[iCivGroupEurope]:
					if not bOwner or civ(iOwner) not in dTechGroups[iTechGroupWestern]:
						if plot.getPlayerSettlerValue(iVoter) < 90:
							iClaimValidity += 10
							
			# vote to support settler maps for civs from your own group
			if bOwner:
				bDifferentGroupClaimant = none(civ(iVoter) in lGroup and civ(iClaimant) in lGroup for lGroup in dCivGroups.values())
				bDifferentGroupOwner = none(civ(iVoter) in lGroup and civ(iOwner) in lGroup for lGroup in dCivGroups.values())
			
				iClaimantValue = plot.getPlayerSettlerValue(iClaimant)
				iOwnerValue = plot.getPlayerSettlerValue(iOwner)
				
				if not bDifferentGroupClaimant and bDifferentGroupOwner and iClaimantValue >= 90: iClaimantValue *= 2
				if not bDifferentGroupOwner and bDifferentGroupClaimant and iOwnerValue >= 90: iOwnerValue *= 2
				
				iClaimValidity += max(1, iClaimantValue / 100)
				iClaimValidity -= max(1, iOwnerValue / 100)
			
		# own expansion targets
		if not bOwnClaim:
			iOwnSettlerValue = plot.getPlayerSettlerValue(iVoter)
			iOwnWarTargetValue = plot.getPlayerWarValue(iVoter)
			
			# if vote between two civs, favor the weaker one if we want to expand there later on
			if bOwner:
				iClaimantPower = team(iClaimant).getPower(True)
				iOwnerPower = team(iOwner).getPower(True)
			
				if iClaimantPower > iOwnerPower:
					if iOwnSettlerValue >= 200: iFavorClaimant -= max(1, iOwnSettlerValue / 100)
					if iOwnWarTargetValue > 0: iFavorClaimant -= max(1, iOwnWarTargetValue / 2)
				elif iOwnerPower > iClaimantPower:
					if iOwnSettlerValue >= 200: iFavorOwner -= max(1, iOwnSettlerValue / 100)
					if iOwnWarTargetValue > 0: iFavorOwner -= max(1, iOwnWarTargetValue / 2)
			# if vote for free territory, reduce the validity of the claim
			else:
				if iOwnSettlerValue >= 200: iClaimValidity -= max(1, iOwnSettlerValue / 100)
				if iOwnWarTargetValue > 0: iClaimValidity -= max(1, iOwnWarTargetValue / 2)
		
		# city factors
		if bCity:
			if not bRecolonise:
				# previous ownership
				if city.isEverOwned(iClaimant): iClaimValidity += 5
			
				# city culture, see plot culture
				if city.getCulture(iClaimant) == 0: iClaimValidity -= 10
			
			# close borders
			for i in range(21):
				if city.getCityIndexPlot(i).getOwner() == iClaimant:
					iClaimValidity += 1
					
			# capital
			if city.isCapital(): iClaimValidity -= 10
			
			# core area
			if plot.isPlayerCore(iClaimant): iClaimValidity += 10
			if plot.isPlayerCore(iOwner): iClaimValidity -= 15
			
			# immediately reclaiming lost cities is only valid in post war congress
			if not self.bPostWar:
				iTurnLost = city.getGameTurnPlayerLost(iClaimant)
				if iTurnLost >= 0:
					if since(iTurnLost) > 0:
						iClaimValidity -= (25 - min(25, since(iTurnLost)))
			
		sDebugText = 'FavorClaimant: ' + str(iFavorClaimant)
		sDebugText += '\nFavorOwner: ' + str(iFavorOwner)
		sDebugText += '\nClaim Validity: ' + str(iClaimValidity)
		
		debug(sDebugText)
				
		bThreatenedClaimant = (2 * tVoter.getPower(True) < team(iClaimant).getPower(True))
		if bOwner: bThreatenedOwner = (2 * tVoter.getPower(True) < team(iOwner).getPower(True))
		
		# always vote for claims on empty territory unless claim is invalid
		if not bOwner:
			if iClaimValidity >= 0:
				debug('Voted YES: empty territory')
				self.vote(iVoter, iClaimant, 1)
				return
		
		# always vote for own claims unless threatened by owner
		if bOwnClaim:
			if not bOwner or not bThreatenedOwner:
				debug('Voted YES: own claim')
				self.vote(iVoter, iClaimant, 1)
				return
				
		# always vote against claims on own cities unless threatened by claimant
		if bOwner and bOwnCity:
			if not bThreatenedClaimant:
				debug('Voted NO: claim on own city')
				self.vote(iVoter, iClaimant, -1)
				return
				
		# vote yes to asking minor cities if there is a valid claim
		if bOwner and bMinor:
			if iClaimValidity > 0:
				debug('Voted YES: valid claim on minors')
				self.vote(iVoter, iClaimant, 1)
			else:
				debug('Voted NO: invalid claim on minors')
				self.vote(iVoter, iClaimant, -1)
			return
			
		# always vote no against claims against a common enemy
		if bOwner and not bOwnClaim:
			if tVoter.isAtWar(iClaimant) and team(iOwner).isAtWar(iClaimant) and not tVoter.isAtWar(iOwner):
				debug('Voted NO: claimant is common enemy')
				self.vote(iVoter, iClaimant, -1)
			
		# maybe include threatened here?
		# winners of wars don't need valid claims
		if iClaimValidity > 0 or (bOwner and bWarClaim):
			# claim insufficient to overcome dislike
			if iFavorClaimant + iClaimValidity < iFavorOwner:
				debug('Voted NO: claimant favor and validity lower than owner favor')
				self.vote(iVoter, iClaimant, -1)
			# valid claim and claimant is more liked
			elif iFavorClaimant > iFavorOwner:
				debug('Voted YES: claimant favor higher than owner favor')
				self.vote(iVoter, iClaimant, 1)
			# less liked, but justified by claim
			elif iFavorClaimant + iClaimValidity >= iFavorOwner:
				# human can bribe on a close call if own claim or own city
				if ((not bOwner and player(iClaimant).isHuman()) or (bOwner and player(iOwner).isHuman())) and iClaimValidity < 50 and iFavorOwner - iFavorClaimant > 0:
					# return the relevant data to be added to the list of possible bribes in the calling method
					debug('NO VOTE: open for bribes')
					return (iVoter, iClaimant, (x, y), iFavorOwner - iFavorClaimant, iClaimValidity)
				else:
					iRand = rand(50)
					if iRand < iClaimValidity:
						debug('Voted YES: random')
						self.vote(iVoter, iClaimant, 1)
					else:
						debug('Voted NO: random')
						self.vote(iVoter, iClaimant, -1)
				
		else:
			# like them enough to overcome bad claim
			if iFavorClaimant + iClaimValidity > iFavorOwner:
				debug('Voted YES: likes claimant enough despite bad claim')
				self.vote(iVoter, iClaimant, 1)
			else:
				debug('Voted NO: bad claim')
				self.vote(iVoter, iClaimant, -1)
				
		debug('End vote city AI')
				
		# return none to signify that no bribe is possible
		return None
				
	def vote(self, iVoter, iClaimant, iVote):
		if iClaimant in self.dVotes: self.dVotes[iClaimant] += iVote
		self.dVotes[iClaimant] += iVote
		if iVote == 1 and iVoter not in self.dVotedFor[iClaimant]: self.dVotedFor[iClaimant].append(iVoter)
				
	def makeClaimHuman(self):
		self.startClaimCity()
		
	def makeClaimAI(self, iPlayer):
		if not self.dPossibleClaims[iPlayer]: return
		x, y, iValue = find_max(self.dPossibleClaims[iPlayer], lambda claim: claim[2]).result
		self.dCityClaims[iPlayer] = (x, y, iValue)
		
	def canClaim(self, iPlayer):
		if not self.bPostWar: return True
		
		if iPlayer in self.winners: return True
		
		if iPlayer in self.losers: return True
		
		return False
			
	def selectClaims(self, iPlayer):
		pPlayer = player(iPlayer)
		iGameTurn = turn()
		iNumPlayersAlive = game.countCivPlayersAlive()
		lPlots = []
		
		for iLoopPlayer in players.all():
			if iLoopPlayer == iPlayer: continue
			if not player(iLoopPlayer).isAlive(): continue
			
			# after a war: winners can only claim from losers and vice versa
			if self.bPostWar:
				if iPlayer in self.winners and iLoopPlayer not in self.losers: continue
				if iPlayer in self.losers and iLoopPlayer not in self.winners: continue
				
			# AI civs: cannot claim cities from friends
			if not player(iPlayer).isHuman() and pPlayer.AI_getAttitude(iLoopPlayer) >= AttitudeTypes.ATTITUDE_FRIENDLY: 
				continue
			
			# recently spawned
			if since(player(iLoopPlayer).getLastBirthTurn()) <= turns(10):
				continue
			
			# exclude master/vassal relationships
			if team(iPlayer).isVassal(iLoopPlayer): continue
			if team(iLoopPlayer).isVassal(iPlayer): continue
			if team(iPlayer).isAVassal() and master(iPlayer) == master(iLoopPlayer): continue
			
			# cannot demand cities while at war
			if team(iPlayer).isAtWar(iLoopPlayer): 
				continue
			
			# Palace of Nations effect
			if player(iLoopPlayer).isHasBuildingEffect(iPalaceOfNations): 
				continue
			
			for city in cities.owner(iLoopPlayer):
				plot = plot_(city)
				iSettlerMapValue = plot.getPlayerSettlerValue(iPlayer)
				iValue = 0
				
				bRecolonise = not self.bPostWar and city.getRegionID() in lAmerica and civ(iPlayer) in dCivGroups[iCivGroupEurope] and civ(city) in dCivGroups[iCivGroupAmerica] and civ(city) in dTechGroups[iTechGroupWestern]
				
				if not plot.isRevealed(iPlayer, False): continue
				if city.isCapital(): continue
				
				# after a war: losers can only claim previously owned cities
				if self.bPostWar and iPlayer in self.losers:
					if city.getGameTurnPlayerLost(iPlayer) < turn() - turns(25):
						continue
					
				iCultureDivisor = bRecolonise and 50 or 20
				
				# city culture
				iTotalCulture = city.countTotalCultureTimes100()
				if iTotalCulture > 0:
					iCultureRatio = city.getCultureTimes100(iPlayer) * 100 / iTotalCulture
					if iCultureRatio > iCultureDivisor:
						if civ(city) != iAmerica:
							iValue += iCultureRatio / iCultureDivisor
							
				# ever owned
				if not bRecolonise and city.isEverOwned(iPlayer):
					iValue += 3
					iValue -= min(3, since(city.getGameTurnPlayerLost(iPlayer)) / turns(100))
						
				# own core
				if plot.isPlayerCore(iPlayer):
					iValue += 5
							
				# colonies
				if not bRecolonise:
					if civ(iPlayer) in dCivGroups[iCivGroupEurope]:
						if is_minor(iLoopPlayer) or (civ(iLoopPlayer) not in dCivGroups[iCivGroupEurope] and stability(iLoopPlayer) < iStabilityShaky) or (civ(iLoopPlayer) in dCivGroups[iCivGroupEurope] and not player(iLoopPlayer).isHuman() and pPlayer.AI_getAttitude(iLoopPlayer) < AttitudeTypes.ATTITUDE_PLEASED):
							if plot.getRegionID() not in lEurope + lMiddleEast + lNorthAfrica:
								if iSettlerMapValue > 90:
									iValue += max(1, iSettlerMapValue / 100)
									
				# weaker and collapsing empires
				if not is_minor(iLoopPlayer):
					if game.getPlayerRank(iPlayer) > iNumPlayersAlive / 2 and game.getPlayerRank(iLoopPlayer) < iNumPlayersAlive / 2:
						if data.players[iLoopPlayer].iStabilityLevel == iStabilityCollapsing:
							if iSettlerMapValue >= 90:
								iValue += max(1, iSettlerMapValue / 100)
									
				# close to own empire
				closest = closestCity(city, iPlayer)
				iDistance = distance(city, closest)
				if iDistance < 5:
					iValue += 5-iDistance
					
				# after war: war targets
				if self.bPostWar:
					iValue += plot.getPlayerWarValue(iPlayer) / 2
				elif iValue == 0 and plot.getPlayerWarValue(iPlayer) > 0:
					iValue += 1
					
				# AI America receives extra value for claims in the west
				if civ(iPlayer) == iAmerica and not player(iPlayer).isHuman():
					if city in plots.rectangle(tAmericanClaims):
						iValue += 5
						
				# help Canada gain Labrador and Newfoundland
				if civ(iPlayer) == iCanada:
					if city in plots.rectangle(tNewfoundland):
						iValue += 5
					
				if iValue > 0:
					lPlots.append((city.getX(), city.getY(), iValue))
		
		# extra spots for colonial civs -> will be settled
		# not available after wars because these congresses are supposed to reassign cities
		if civ(iPlayer) in dCivGroups[iCivGroupEurope] and not self.bPostWar:
			for plot in plots.all().where(lambda p: not p.isCity() and not p.isPeak() and not p.isWater() and pPlayer.canFound(p.getX(), p.getY())).regions(rWestAfrica, rSouthAfrica, rEthiopia, rAustralia, rOceania):
				if pPlayer.isHuman() and not plot.isRevealed(iPlayer, False): continue
				iSettlerMapValue = plot.getPlayerSettlerValue(iPlayer)
				if iSettlerMapValue >= 90 and cnm.getFoundName(iPlayer, plot):
					iFoundValue = pPlayer.AI_foundValue(plot.getX(), plot.getY(), -1, False)
					lPlots.append((plot.getX(), plot.getY(), max(1, min(5, iFoundValue / 2500 - 1))))
		
		# sort by value with some random variance
		lPlots = sort(lPlots, lambda p: p[2] + rand(3), True)
		
		# remove settled plots with the same name
		lPlots = [(x, y, value) for index, (x, y, value) in enumerate(lPlots) if city_(x, y) or cnm.getFoundName(iPlayer, (x, y)) not in [cnm.getFoundName(iPlayer, (ix, iy)) for (ix, iy, ivalue) in lPlots[:index]]]
		
		return lPlots[:10]
		
	def getHighestRankedPlayers(self, lPlayers, iNumPlayers):
		return players.of(lPlayers).highest(iNumPlayers, game.getPlayerRank)
		
	def invite(self):
		rank = lambda x: game.getPlayerRank(x)
		self.invites = players.none()
		
		if self.bPostWar:
			iLowestWinnerRank = find_min(self.winners, rank).value
			self.invites = self.invites.including(self.winners)
			self.invites = self.invites.including(self.losers.where(lambda p: rank(p) < iLowestWinnerRank))
			
		self.invites = self.invites.including(players.major().without(self.invites).sort(rank))
		self.invites = self.invites.limit(getNumInvitations())
		
		# if not a war congress, exclude civs in global wars
		if isGlobalWar() and not self.bPostWar:
			lAttackers, lDefenders = determineAlliances(data.iGlobalWarAttacker, data.iGlobalWarDefender)
			self.invites = self.invites.without(lAttackers)
			self.invites = self.invites.without(lDefenders)
			
		self.invites = self.invites.alive().where(lambda p: player(p).getNumCities() > 0)
		
		# America receives an invite if there are still claims in the west
		if player(iAmerica).isAlive() and iAmerica not in self.invites and not self.bPostWar:
			if cities.rectangle(tAmericanClaims).notowner(iAmerica):
				if len(self.invites) == getNumInvitations():
					self.invites = self.invites.limit(len(self.invites)-1)
				self.invites = self.invites.including(slot(iAmerica))