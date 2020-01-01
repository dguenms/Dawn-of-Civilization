# Rhye's and Fall of Civilization - World Congresses

from CvPythonExtensions import *
import CvUtil
import PyHelpers 
import Popup
from RFCUtils import *
from Consts import *
import Areas
import CityNameManager as cnm
from StoredData import data # edead

from Core import *


### Singleton ###

currentCongress = None

### Constants ###

tAmericanClaimsTL = (19, 41)
tAmericanClaimsBR = (24, 49)

tNewfoundlandTL = (27, 53)
tNewfoundlandBR = (36, 59)

### Event Handlers ###

def setup():
	data.iCongressTurns = getCongressInterval()

def checkTurn(iGameTurn):
	if isCongressEnabled():
		if data.iCongressTurns > 0:
			data.iCongressTurns -= 1
	
		if data.iCongressTurns == 0:
			data.iCongressTurns = getCongressInterval()
			currentCongress = Congress()
			data.currentCongress = currentCongress
			currentCongress.startCongress()

def onChangeWar(bWar, iPlayer, iOtherPlayer):
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
		
	if data.currentCongress:
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
	
	currentCongress = Congress(players.of(lWinners), players.of(lLosers))
	data.iCongressTurns = getCongressInterval()
	data.currentCongress = currentCongress
	currentCongress.startCongress()
	
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

	### Popups ###
	
	def startIntroductionEvent(self, bHumanInvited, bHumanInGlobalWar = False):
		popup = CyPopupInfo()
		popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popup.setOnClickedPythonCallback("applyIntroductionEvent")
		
		sInviteString = ""
		for iPlayer in self.invites:
			if not player(iPlayer).isHuman():
				sInviteString += text("TXT_KEY_CONGRESS_INVITE", fullname(iPlayer))
				
		if self.bPostWar:
			if bHumanInvited: 
				if human() in self.winners: sText = text("TXT_KEY_CONGRESS_INTRODUCTION_WAR_WON", self.sHostCityName, sInviteString)
				elif human() in self.losers: sText = text("TXT_KEY_CONGRESS_INTRODUCTION_WAR_LOST", self.sHostCityName, sInviteString)
				else: sText = text("TXT_KEY_CONGRESS_INTRODUCTION_WAR", self.sHostCityName, sInviteString)
			else: sText = text("TXT_KEY_CONGRESS_INTRODUCTION_WAR_AI", self.sHostCityName, sInviteString)
		else:
			if bHumanInvited: sText = text("TXT_KEY_CONGRESS_INTRODUCTION", self.sHostCityName, sInviteString)
			elif bHumanInGlobalWar: sText = text("TXT_KEY_CONGRESS_INTRODUCTION_AI_WAR_EXCLUDED", self.sHostCityName, sInviteString)
			else: sText = text("TXT_KEY_CONGRESS_INTRODUCTION_AI", self.sHostCityName, sInviteString)
			
		popup.setText(sText)
			
		popup.addPythonButton(text("TXT_KEY_CONGRESS_OK"), '')
		popup.addPopup(human())
		
	def applyIntroductionEvent(self):
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
	
		if human() in self.dPossibleClaims:
			# human still has to make a claim
			self.makeClaimHuman()
		else:
			# human cannot make claims, so let the AI vote
			self.voteOnClaims()

	def startClaimCityEvent(self):
		popup = CyPopupInfo()
		popup.setText(text("TXT_KEY_CONGRESS_CLAIM_CITY", self.sHostCityName))
		popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popup.setOnClickedPythonCallback("applyClaimCityEvent")
		
		for tCity in self.dPossibleClaims[human()]:
			x, y, iValue = tCity
			plot = plot_(x, y)
			if plot.isCity():
				popup.addPythonButton(plot.getPlotCity().getName(), infos.civ(plot).getButton())
			else:
				popup.addPythonButton(cnm.getFoundName(human(), (x, y)), 'Art/Interface/Buttons/Actions/FoundCity.dds')
			
		popup.addPythonButton(text("TXT_KEY_CONGRESS_NO_REQUEST"), 'Art/Interface/Buttons/Actions/Cancel.dds')
		popup.addPopup(human())

	def applyClaimCityEvent(self, iChoice):
		if iChoice < len(self.dPossibleClaims[human()]):
			x, y, iValue = self.dPossibleClaims[human()][iChoice]
			self.dCityClaims[human()] = (x, y, iValue)

		self.voteOnClaims()	
		
	def startVoteCityEvent(self, iClaimant, (x, y)):
		plot = plot_(x, y)
		
		if plot.isRevealed(human(), False):
			plot.cameraLookAt()
		
		popup = CyPopupInfo()
		popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popup.setOnClickedPythonCallback("applyVoteCityEvent")
		popup.setData1(iClaimant)
		popup.setData2(plot.getOwner())
		
		sClaimant = name(iClaimant)
		
		if plot.isCity():
			popup.setText(text("TXT_KEY_CONGRESS_REQUEST_CITY", sClaimant, adjective(plot), plot.getPlotCity().getName()))
		elif plot.getOwner() == iClaimant:
			popup.setText(text("TXT_KEY_CONGRESS_REQUEST_SETTLE_OWN", sClaimant, cnm.getFoundName(iClaimant, tPlot)))
		elif plot.isOwned():
			popup.setText(text("TXT_KEY_CONGRESS_REQUEST_SETTLE_FOREIGN", sClaimant, adjective(plot), cnm.getFoundName(iClaimant, tPlot)))
		else:
			popup.setText(text("TXT_KEY_CONGRESS_REQUEST_SETTLE_EMPTY", sClaimant, cnm.getFoundName(iClaimant, tPlot)))
			
		popup.addPythonButton(text("TXT_KEY_POPUP_VOTE_YES"), infos.art("INTERFACE_EVENT_BULLET"))
		popup.addPythonButton(text("TXT_KEY_POPUP_ABSTAIN"), infos.art("INTERFACE_EVENT_BULLET"))
		popup.addPythonButton(text("TXT_KEY_POPUP_VOTE_NO"), infos.art("INTERFACE_EVENT_BULLET"))
		
		popup.addPopup(human())
		
	def applyVoteCityEvent(self, iClaimant, iOwner, iVote):
		self.vote(human(), iClaimant, 1 - iVote) # yes=0, abstain=1, no=2
		
		if iClaimant in self.dVotingMemory: self.dVotingMemory[iClaimant] += (1 - iVote)
		if iOwner >= 0 and iOwner in self.dVotingMemory: self.dVotingMemory[iOwner] += (iVote - 1)
		self.iNumHumanVotes += 1
		
		# still votes to cast: start a new popup, otherwise let the AI vote
		if self.iNumHumanVotes < len(self.lHumanVotes):
			iNextClaimant, x, y = self.lHumanVotes[self.iNumHumanVotes]
			self.startVoteCityEvent(iNextClaimant, (x, y))
		else:
			self.voteOnClaimsAI()
			
	def startBriberyEvent(self, iVoter, iClaimant, (x, y), iDifference, iClaimValidity):
		plot = plot_(x, y)
		iBribedPlayer = iVoter
		
		bHumanClaim = player(iClaimant).isHuman()
		bCity = plot.isCity()
		
		if plot.isRevealed(human(), False):
			plot.cameraLookAt()
		
		if bHumanClaim:
			if bCity:
				sText = text("TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_CITY", adjective(iBribedPlayer), adjective(plot), plot.getPlotCity().getName())
			else:
				closest = closestCity(plot, iBribedPlayer, same_continent=True)
				sText = text("TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_COLONY", adjective(iBribedPlayer), adjective(plot), closest.getName())
		else:	
			if bCity:
				sText = text("TXT_KEY_CONGRESS_BRIBE_OWN_CITY", adjective(iBribedPlayer), adjective(iClaimant), plot.getPlotCity().getName())
			else:
				closest = closestCity(plot, human(), same_continent=True)
				sText = text("TXT_KEY_CONGRESS_BRIBE_OWN_TERRITORY", adjective(iBribedPlayer), adjective(iClaimant), closest.getName())
				
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
		
		if iEspionageSpent >= iCost / 2: self.lBriberyOptions.append((3, iCost / 2, iLowChance))
		if iEspionageSpent >= iCost: self.lBriberyOptions.append((3, iCost, iMediumChance))
		if iEspionageSpent >= iCost * 2: self.lBriberyOptions.append((3, iCost * 2, iHighChance))
		
		popup = CyPopupInfo()
		popup.setText(sText)
		popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popup.setOnClickedPythonCallback("applyBriberyEvent")
		popup.setData1(iBribedPlayer)
		popup.setData2(iClaimant)
		popup.setData3(iClaimValidity)
		
		for tOption in self.lBriberyOptions:
			iCommerceType, iCost, iThreshold = tOption
			if iCommerceType == 0: 
				textKey = "TXT_KEY_CONGRESS_BRIBE_GOLD"
				button = infos.commerce(iCommerceType).getButton()
			elif iCommerceType == 3: 
				textKey = "TXT_KEY_CONGRESS_MANIPULATION"
				button = 'Art/Interface/Buttons/Espionage.dds'
				
			if iThreshold == iLowChance: sChance = "TXT_KEY_CONGRESS_CHANCE_AVERAGE"
			elif iThreshold == iHighChance: sChance = "TXT_KEY_CONGRESS_CHANCE_VERY_HIGH"
			else: sChance = "TXT_KEY_CONGRESS_CHANCE_HIGH"
			
			sChance = text(sChance)
			
			popup.addPythonButton(text(textKey, iCost, sChance), button)
			
		if self.lBriberyOptions:
			popup.addPythonButton(text("TXT_KEY_CONGRESS_NO_BRIBE"), infos.art("INTERFACE_BUTTONS_CANCEL"))
		else:
			popup.addPythonButton(text("TXT_KEY_CONGRESS_CANNOT_AFFORD_BRIBE"), infos.art("INTERFACE_BUTTONS_CANCEL"))
		
		popup.addPopup(human())
		
	def applyBriberyEvent(self, iChoice, iBribedPlayer, iClaimant, iClaimValidity):
		if iChoice < len(self.lBriberyOptions):
			iCommerceType, iCost, iThreshold = self.lBriberyOptions[iChoice]
			iRand = rand(100)
			
			if iCommerceType == 0: player().changeGold(-iCost)
			elif iCommerceType == 3: team().changeEspionagePointsAgainstTeam(iBribedPlayer, -iCost)
			
			bHumanClaim = player(iClaimant).isHuman()
			bSuccess = (iRand < iThreshold)
			
			self.startBriberyResultEvent(iBribedPlayer, iClaimant, bHumanClaim, bSuccess)
		else:
			# if no bribery option was chosen, the civ votes randomly as usual
			iRand = rand(50)
			if iRand < iClaimValidity:
				self.vote(iBribedPlayer, iClaimant, 1)
			else:
				self.vote(iBribedPlayer, iClaimant, -1)
				
			# to continue the process
			self.applyBriberyResultEvent()
				
	def startBriberyResultEvent(self, iBribedPlayer, iClaimant, bHumanClaim, bSuccess):	
		if bSuccess:
			if bHumanClaim:
				sText = text("TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_SUCCESS", name(iBribedPlayer))
				self.vote(iBribedPlayer, iClaimant, 1)
			else:
				sText = text("TXT_KEY_CONGRESS_BRIBE_THEIR_CLAIM_SUCCESS", name(iBribedPlayer))
				self.vote(iBribedPlayer, iClaimant, -1)
		else:
			if bHumanClaim:
				sText = text("TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_FAILURE", name(iBribedPlayer))
				self.vote(iBribedPlayer, iClaimant, -1)
			else:
				sText = text("TXT_KEY_CONGRESS_BRIBE_THEIR_CLAIM_FAILURE", name(iBribedPlayer))
				self.vote(iBribedPlayer, iClaimant, 1)
				
			player(iBribedPlayer).AI_changeMemoryCount(human(), MemoryTypes.MEMORY_STOPPED_TRADING_RECENT, 1)
			player(iBribedPlayer).AI_changeAttitudeExtra(human(), -2)
			
		popup = CyPopupInfo()
		popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popup.setOnClickedPythonCallback("applyBriberyResultEvent")
		popup.setText(sText)
		popup.addPythonButton(text("TXT_KEY_CONGRESS_OK"), '')
		
		popup.addPopup(human())
		
	def applyBriberyResultEvent(self):
		# just continue to the next bribe if there is one
		self.iNumBribes += 1
		if self.iNumBribes < len(self.lPossibleBribes):
			iVoter, iClaimant, tPlot, iDifference, iClaimValidity = self.lPossibleBribes[self.iNumBribes]
			self.startBriberyEvent(iVoter, iClaimant, tPlot, iDifference, iClaimValidity)
		else:
			# otherwise continue with applying the votes
			self.applyVotes()
			
	def startRefusalEvent(self, iClaimant, (x, y)):
		plot = plot_(x, y)
		
		if plot.isRevealed(human(), False):
			plot.cameraLookAt()
		
		popup = CyPopupInfo()
		popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popup.setOnClickedPythonCallback("applyRefusalEvent")
		popup.setData1(iClaimant)
		popup.setData2(x)
		popup.setData3(y)
		
		sVotedYes = ""
		for iPlayer in self.dVotedFor[iClaimant]:
			if not player(iPlayer).isHuman() and iClaimant != iPlayer:
				sVotedYes += text("TXT_KEY_CONGRESS_INVITE", fullname(iPlayer))
		
		
		if plot.isCity():
			sText = text("TXT_KEY_CONGRESS_DEMAND_CITY", name(iClaimant), plot.getPlotCity().getName(), sVotedYes)
		else:
			closest = closestCity(plot, human(), same_continent=True)
			sText = text("TXT_KEY_CONGRESS_DEMAND_TERRITORY", name(iClaimant), closest.getName(), sVotedYes)
			
		popup.setText(sText)
		popup.addPythonButton(text("TXT_KEY_CONGRESS_ACCEPT"), infos.art("INTERFACE_EVENT_BULLET"))
		popup.addPythonButton(text("TXT_KEY_CONGRESS_REFUSE"), infos.art("INTERFACE_EVENT_BULLET"))
		popup.addPopup(human())
		
	def applyRefusalEvent(self, iChoice, iClaimant, x, y):
		if iChoice == 0:
			plot = plot_(x, y)
			if plot.isCity():
				self.assignCity(iClaimant, plot.getOwner(), (x, y))
			else:
				self.foundColony(iClaimant, (x, y))
		else:
			self.refuseDemand(iClaimant)
			
		self.iNumHumanAssignments += 1
		
		# still assignments to react to: start a new popup, otherwise show the results
		if self.iNumHumanAssignments < len(self.lHumanAssignments):
			iNextClaimant, tPlot = self.lHumanAssignments[self.iNumHumanAssignments]
			self.startRefusalEvent(iNextClaimant, tPlot)
		else:
			self.finishCongress()
			
	def startResultsEvent(self):
		# don't display if human still in autoplay
		if year() >= year(tBirth[human()]):
	
			sText = text("TXT_KEY_CONGRESS_RESULTS", self.sHostCityName)
		
			for tAssignment in self.lAssignments:
				sName, iOldOwner, iNewOwner = tAssignment
				sText += text("TXT_KEY_CONGRESS_RESULT_ASSIGNMENT", sName, adjective(iOldOwner), adjective(iNewOwner))
			
			for tColony in self.lColonies:
				sName, iOldOwner, iNewOwner = tColony
				if iOldOwner >= 0:
					sText += text("TXT_KEY_CONGRESS_RESULT_COLONY_TERRITORY", sName, adjective(iOldOwner), name(iNewOwner))
				else:
					sText += text("TXT_KEY_CONGRESS_RESULT_COLONY", sName, name(iNewOwner))
			
			if not self.lAssignments and not self.lColonies:
				sText += text("TXT_KEY_CONGRESS_NO_RESULTS")
			
			popup = CyPopupInfo()
			popup.setText(sText)
			popup.addPythonButton(text("TXT_KEY_CONGRESS_OK"), '')
		
			popup.addPopup(human())
			
		# if this was triggered by a war, reset belligerents
		if isGlobalWar():
			data.iGlobalWarAttacker = -1
			data.iGlobalWarDefender = -1
		
		# don't waste memory
		data.currentCongress = None

	### Other Methods ###

	def startCongress(self):
		self.bPostWar = self.winners.any()
		
		debug('Congress takes place')

		self.inviteToCongress()
		
		if self.bPostWar:
			iHostPlayer = self.winners.alive().first()
		else:
			iHostPlayer = self.invites.where(lambda p: player(p).getNumCities() > 0).random()
			
		# normal congresses during war time may be too small because all civilisations are tied up in global wars
		if len(self.invites) < 3:
			data.iCongressTurns /= 2
			data.currentCongress = None
			return
			
		# establish contact between all participants
		for iThisPlayer in self.invites:
			for iThatPlayer in self.invites:
				if iThisPlayer != iThatPlayer:
					tThisPlayer = team(iThisPlayer)
					if not tThisPlayer.canContact(iThatPlayer): tThisPlayer.meet(iThatPlayer, False)

		self.sHostCityName = getOwnedCoreCities(iHostPlayer, player(iHostPlayer).getReborn()).random().getName()
		
		# moved selection of claims after the introduction event so claims and their resolution take place at the same time
		if human() in self.invites:
			self.startIntroductionEvent(True)
				
		# procedure continues from the makeClaimHuman event
		
		bHumanInGlobalWar = False
		if isGlobalWar():
			lAttackers, lDefenders = determineAlliances(data.iGlobalWarAttacker, data.iGlobalWarDefender)
			bHumanInGlobalWar = human() in lAttackers + lDefenders
		
		# unless the player isn't involved, in that case resolve from here
		if human() not in self.invites:
			# since Congresses now can occur during autoplay, don't display these congresses to the player
			if year() >= year(tBirth[human()]):
				self.startIntroductionEvent(False, bHumanInGlobalWar)
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
		if human() not in self.invites:
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
					
		for (x, y) in dResults:
			iClaimant, iVotes = dResults[tAssignedPlot]
			plot = plot_(x, y)
			
			bCanRefuse = (plot.getOwner() == human() and human() not in self.dVotedFor[iClaimant] and not (self.bPostWar and human() in self.losers))
			
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
			self.startRefusalEvent(iClaimant, tPlot)
		else:
			# without human cities affected, finish the congress immediately
			self.finishCongress()
			
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
					
	def assignCity(self, iPlayer, iOwner, (x, y)):
		assignedCity = city(x, y)
		
		iNumDefenders = max(2, player(iPlayer).getCurrentEra()-1)
		lFlippingUnits, lRelocatedUnits = flipOrRelocateGarrison(assignedCity, iNumDefenders)
		
		completeCityFlip(x, y, iPlayer, iOwner, 80, False, False, True, bPermanentCultureChange=False)
		
		flipOrCreateDefenders(iPlayer, lFlippingUnits, (x, y), iNumDefenders)
		
		if iOwner < iNumPlayers:
			relocateUnitsToCore(iOwner, lRelocatedUnits)
		else:
			killUnits(lRelocatedUnits)
		
	def foundColony(self, iPlayer, (x, y)):
		plot = plot_(x, y)
		
		if plot.isOwned(): convertPlotCulture(plot, iPlayer, 100, True)
		
		if player(iPlayer).isHuman():
			makeUnit(iPlayer, iSettler, tPlot)
		else:
			player(iPlayer).found(x, y)
			
		createGarrisons(tPlot, iPlayer, 2)
		
	def finishCongress(self):
		# declare war against human if he refused demands
		iGlobalWarModifier = 0
		tHuman = team()
		for iLoopPlayer in range(iNumPlayers):
			if tHuman.isDefensivePact(iLoopPlayer):
				iGlobalWarModifier += 10
				
		for iBelligerent in self.dPossibleBelligerents:
			iRand = rand(100)
			iThreshold = 10 + tPatienceThreshold[iBelligerent] - 5 * self.dPossibleBelligerents[iBelligerent] - iGlobalWarModifier
			if iRand >= iThreshold:
				team(iBelligerent).setDefensivePact(human(), False)
				team(iBelligerent).declareWar(human(), False, WarPlanTypes.WARPLAN_DOGPILE)
				
		# display Congress results
		self.startResultsEvent()
				
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
			
			lVoters = self.invites
			
			plot = plot_(x, y)
			if plot.isOwned():
				iOwner = plot.getOwner()
				if iOwner not in lVoters and iOwner in players.major().highest(getNumInvitations(), game.getPlayerRank):
					lVoters.append(iOwner)
			
			if human() in lVoters: lVoters.remove(human())
			if iClaimant in lVoters: lVoters.remove(iClaimant)
			
			for iVoter in lVoters:
				tResult = self.voteOnCityClaimAI(iVoter, iClaimant, (x, y), iValue)
				
				# if a human bribe is possible, a set of data has been returned, so add it to the list of possible bribes
				if tResult: self.lPossibleBribes.append(tResult)
						
		# if bribes are possible, handle them now, votes are applied after the last bribe event
		if len(self.lPossibleBribes) > 0:
			iVoter, iClaimant, tPlot, iDifference, iClaimValidity = self.lPossibleBribes[0]
			self.startBriberyEvent(iVoter, iClaimant, tPlot, iDifference, iClaimValidity)
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
		
		if bCity: city = plot.getPlotCity()
		if bOwner: 
			bMinor = (iOwner >= iNumPlayers)
			bOwnCity = (iOwner == iVoter)
			bWarClaim = (iClaimant in self.winners and iOwner in self.losers)
		
		# everyone agrees on AI American claims in the west, unless owner is native to the Americas
		if iClaimant == iAmerica and iVoter != iOwner and iOwner not in lCivGroups[5]:
			if plot in plots.start(tAmericanClaimsTL).end(tAmericanClaimsBR):
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
			if not isNeighbor(iVoter, iClaimant): iFavorClaimant += 5
			if not isNeighbor(iVoter, iOwner): iFavorOwner += 10
			
			# vassalage
			if tVoter.isVassal(iClaimant): iFavorClaimant += 20
			if tVoter.isVassal(iOwner): iFavorOwner += 20
			
			if team(iClaimant).isVassal(iVoter): iFavorClaimant += 10
			if team(iOwner).isVassal(iVoter): iFavorOwner += 10
			
			# French UP
			if iClaimant == iFrance: iFavorClaimant += 10
			if iOwner == iFrance: iFavorOwner += 10
			
			# Palace of Nations
			if player(iClaimant).isHasBuildingEffect(iPalaceOfNations): iFavorClaimant += 10
			
			# AI memory of human voting behavior
			if player(iClaimant).isHuman() and iVoter in self.dVotingMemory: iFavorClaimant += 5 * self.dVotingMemory[iVoter]
			if player(iOwner).isHuman() and iVoter in self.dVotingMemory: iFavorOwner += 5 * self.dVotingMemory[iVoter]
			
		# if we don't dislike them, agree with the value of their claim
		if pVoter.AI_getAttitude(iClaimant) >= AttitudeTypes.ATTITUDE_CAUTIOUS: iClaimValidity += iClaimValue
			
		# French UP
		if iClaimant == iFrance: iClaimValidity += 5
			
		# plot factors
		# plot culture
		if bOwner:
			iClaimValidity += (100 * plot.getCulture(iClaimant) / plot.countTotalCulture()) / 20
			
			# after wars: claiming from a non-participant has less legitimacy unless its your own claim
			if self.bPostWar and not bOwnClaim and iOwner not in self.losers:
				iClaimValidity -= 10
			
		# generic settler map bonus
		iClaimantValue = plot.getSettlerValue(iClaimant)
		if iClaimantValue >= 90:
			iClaimValidity += max(1, iClaimantValue / 100)

		# Europeans support colonialism unless they want the plot for themselves
		if iVoter in lCivGroups[0]:
			if iClaimant in lCivGroups[0]:
				if not bOwner or iOwner not in lCivGroups[0]:
					if plot.getSettlerValue(iVoter) < 90:
						iClaimValidity += 10
						
		# vote to support settler maps for civs from your own group
		if bOwner:
			bDifferentGroupClaimant = True
			bDifferentGroupOwner = True
			for lGroup in lCivGroups:
				if iVoter in lGroup and iClaimant in lGroup: bDifferentGroupClaimant = False
				if iVoter in lGroup and iOwner in lGroup: bDifferentGroupOwner = False
		
			iClaimantValue = plot.getSettlerValue(iClaimant)
			iOwnerValue = plot.getSettlerValue(iOwner)
			
			if not bDifferentGroupClaimant and bDifferentGroupOwner and iClaimantValue >= 90: iClaimantValue *= 2
			if not bDifferentGroupOwner and bDifferentGroupClaimant and iOwnerValue >= 90: iOwnerValue *= 2
			
			iClaimValidity += max(1, iClaimantValue / 100)
			iClaimValidity -= max(1, iOwnerValue / 100)
			
		# own expansion targets
		if not bOwnClaim:
			iOwnSettlerValue = plot.getSettlerValue(iVoter)
			iOwnWarTargetValue = plot.getWarValue(iVoter)
			
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
			# previous ownership
			if city.isEverOwned(iClaimant): iClaimValidity += 5
			if city.getOriginalOwner() == iClaimant: iClaimValidity += 5
			
			# city culture, see plot culture
			if city.getCulture(iClaimant) == 0: iClaimValidity -= 10
			
			# close borders
			for i in range(21):
				if city.getCityIndexPlot(i).getOwner() == iClaimant:
					iClaimValidity += 1
					
			# capital
			if city.isCapital(): iClaimValidity -= 10
			
			# core area
			if plot.isCore(iClaimant): iClaimValidity += 10
			if plot.isCore(iOwner): iClaimValidity -= 15
			
		sDebugText = 'FavorClaimant: ' + str(iFavorClaimant)
		sDebugText += '\nFavorOwner: ' + str(iFavorOwner)
		sDebugText += '\nClaim Validity: ' + str(iClaimValidity)
		
		print sDebugText + '\n'
				
		bThreatenedClaimant = (2 * tVoter.getPower(True) < team(iClaimant).getPower(True))
		if bOwner: bThreatenedOwner = (2 * tVoter.getPower(True) < team(iOwner).getPower(True))
		
		# always vote for claims on empty territory unless claim is invalid
		if not bOwner:
			if iClaimValidity >= 0:
				print 'Voted YES: empty territory'
				self.vote(iVoter, iClaimant, 1)
				return
		
		# always vote for own claims unless threatened by owner
		if bOwnClaim:
			if not bOwner or not bThreatenedOwner:
				print 'Voted YES: own claim'
				self.vote(iVoter, iClaimant, 1)
				return
				
		# always vote against claims on own cities unless threatened by owner
		if bOwner and bOwnCity:
			if not bThreatenedClaimant:
				print 'Voted NO: claim on own city'
				self.vote(iVoter, iClaimant, -1)
				return
				
		# vote yes to asking minor cities if there is a valid claim
		if bOwner and bMinor:
			if iClaimValidity > 0:
				print 'Voted YES: valid claim on minors'
				self.vote(iVoter, iClaimant, 1)
			else:
				print 'Voted NO: invalid claim on minors'
				self.vote(iVoter, iClaimant, -1)
			return
			
		# always vote no against claims against a common enemy
		if bOwner and not bOwnClaim:
			if tVoter.isAtWar(iClaimant) and team(iOwner).isAtWar(iClaimant) and not tVoter.isAtWar(iOwner):
				print 'Voted NO: claimant is common enemy'
				self.vote(iVoter, iClaimant, -1)
			
		# maybe include threatened here?
		# winners of wars don't need valid claims
		if iClaimValidity > 0 or (bOwner and bWarClaim):
			# claim insufficient to overcome dislike
			if iFavorClaimant + iClaimValidity < iFavorOwner:
				print 'Voted NO: claimant favor and validity lower than owner favor'
				self.vote(iVoter, iClaimant, -1)
			# valid claim and claimant is more liked
			elif iFavorClaimant > iFavorOwner:
				print 'Voted YES: claimant favor higher than owner favor'
				self.vote(iVoter, iClaimant, 1)
			# less liked, but justified by claim
			elif iFavorClaimant + iClaimValidity >= iFavorOwner:
				# human can bribe on a close call if own claim or own city
				if (player(iClaimant).isHuman() or (bOwner and player(iOwner).isHuman())) and iClaimValidity < 50 and iFavorOwner - iFavorClaimant > 0:
					# return the relevant data to be added to the list of possible bribes in the calling method
					print 'NO VOTE: open for bribes'
					return (iVoter, iClaimant, tPlot, iFavorOwner - iFavorClaimant, iClaimValidity)
				else:
					iRand = rand(50)
					if iRand < iClaimValidity:
						print 'Voted YES: random'
						self.vote(iVoter, iClaimant, 1)
					else:
						print 'Voted NO: random'
						self.vote(iVoter, iClaimant, -1)
				
		else:
			# like them enough to overcome bad claim
			if iFavorClaimant + iClaimValidity > iFavorOwner:
				print 'Voted YES: likes claimant enough despite bad claim'
				self.vote(iVoter, iClaimant, 1)
			else:
				print 'Voted NO: bad claim'
				self.vote(iVoter, iClaimant, -1)
				
		print 'End vote city AI'
				
		# return none to signify that no bribe is possible
		return None
				
	def vote(self, iVoter, iClaimant, iVote):
		if iClaimant in self.dVotes: self.dVotes[iClaimant] += iVote
		self.dVotes[iClaimant] += iVote
		if iVote == 1 and iVoter not in self.dVotedFor[iClaimant]: self.dVotedFor[iClaimant].append(iVoter)
				
	def makeClaimHuman(self):
		self.startClaimCityEvent()
		
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
		
		for iLoopPlayer in range(iNumTotalPlayers+1):
			if iLoopPlayer == iPlayer: continue
			if not player(iLoopPlayer).isAlive(): continue
			
			# after a war: winners can only claim from losers and vice versa
			if self.bPostWar:
				if iPlayer in self.winners and iLoopPlayer not in self.losers: continue
				if iPlayer in self.losers and iLoopPlayer not in self.winners: continue
				
			# AI civs: cannot claim cities from friends
			if not player(iPlayer).isHuman() and pPlayer.AI_getAttitude(iLoopPlayer) >= AttitudeTypes.ATTITUDE_FRIENDLY: continue
			
			# recently born
			if iGameTurn < year(tBirth[iLoopPlayer]) + turns(20): continue
			
			# recently resurrected
			if iGameTurn < pPlayer.getLatestRebellionTurn() + turns(20): continue
			
			# recently reborn
			if player(iLoopPlayer).isReborn() and iLoopPlayer in dRebirth and iGameTurn < year(dRebirth[iLoopPlayer]) + turns(20): continue
			
			# exclude master/vassal relationships
			if team(iPlayer).isVassal(iLoopPlayer): continue
			if team(iLoopPlayer).isVassal(iPlayer): continue
			
			# cannot demand cities while at war
			if team(iPlayer).isAtWar(iLoopPlayer): continue
			
			# Palace of Nations effect
			if player(iLoopPlayer).isHasBuildingEffect(iPalaceOfNations): continue
			
			for city in cities.owner(iLoopPlayer):
				plot = plot_(city)
				iSettlerMapValue = plot.getSettlerValue(iPlayer)
				iValue = 0
				
				if not plot.isRevealed(iPlayer, False): continue
				if city.isCapital(): continue
				
				# after a war: losers can only claim previously owned cities
				if self.bPostWar and iPlayer in self.losers:
					if city.getGameTurnPlayerLost(iPlayer) < turn() - turns(25): continue
				
				# city culture
				iTotalCulture = city.countTotalCultureTimes100()
				if iTotalCulture > 0:
					iCultureRatio = city.getCultureTimes100(iPlayer) * 100 / iTotalCulture
					if iCultureRatio > 20:
						if iLoopPlayer != iAmerica:
							iValue += iCultureRatio / 20
							
				# ever owned
				if city.isEverOwned(iPlayer):
					iValue += 3
						
				# own core
				if plot.isCore(iPlayer):
					iValue += 5
							
				# colonies
				if iPlayer in lCivGroups[0]:
					if iLoopPlayer >= iNumPlayers or (iLoopPlayer not in lCivGroups[0] and stability(iLoopPlayer) < iStabilityShaky) or (iLoopPlayer in lCivGroups[0] and not player(iLoopPlayer).isHuman() and pPlayer.AI_getAttitude(iLoopPlayer) < AttitudeTypes.ATTITUDE_PLEASED):
						if plot.getRegionID() not in lEurope + lMiddleEast + lNorthAfrica:
							if iSettlerMapValue > 90:
								iValue += max(1, iSettlerMapValue / 100)
									
				# weaker and collapsing empires
				if iLoopPlayer < iNumPlayers:
					if game.getPlayerRank(iLoopPlayer) > iNumPlayersAlive / 2 and game.getPlayerRank(iLoopPlayer) < iNumPlayersAlive / 2:
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
					iValue += plot.getWarValue(iPlayer) / 2
					
				# AI America receives extra value for claims in the west
				if iPlayer == iAmerica and not player(iPlayer).isHuman():
					if city in plots.start(tAmericanClaimsTL).end(tAmericanClaimsBR):
						iValue += 5
						
				# help Canada gain Labrador and Newfoundland
				if iPlayer == iCanada:
					if city in plots.start(tNewfoundlandTL).end(tNewfoundlandBR):
						iValue += 5
					
				if iValue > 0:
					lPlots.append((city.getX(), city.getY(), iValue))
		
		# extra spots for colonial civs -> will be settled
		# not available after wars because these congresses are supposed to reassign cities
		if iPlayer in lCivGroups[0] and not self.bPostWar:
			for plot in plots.all().where(lambda p: not p.isCity() and not p.isPeak() and not p.isWater() and not pPlayer.canFound(p.getX(), p.getY())).regions(rWestAfrica, rSouthAfrica, rEthiopia, rAustralia, rOceania):
				if pPlayer.isHuman() and not plot.isRevealed(iPlayer, False): continue
				iSettlerMapValue = plot.getSettlerValue(iPlayer)
				if iSettlerMapValue >= 90 and cnm.getFoundName(iPlayer, plot):
					iFoundValue = pPlayer.AI_foundValue(plot.getX(), plot.getY(), -1, False)
					lPlots.append((plot.getX(), plot.getY(), max(1, min(5, iFoundValue / 2500 - 1))))
				
		return sort(lPlots, lambda p: p[2] + rand(3), True)[:10]
		
	def getHighestRankedPlayers(self, lPlayers, iNumPlayers):
		return players.of(lPlayers).highest(iNumPlayers, game.getPlayerRank)
		
	def inviteToCongress(self):
		rank = lambda x: game.getPlayerRank(x)
		self.invites = players.none()
		
		if self.bPostWar:
			iLowestWinnerRank = rank(self.winners.sort(rank).first())
			self.invites = self.invites.including(self.winners)
			self.invites = self.invites.including(self.losers.where(lambda p: rank(p) < iLowestWinnerRank))
			
		self.invites = self.invites.including(players.major().without(self.invites).sort(rank))
		self.invites = self.invites.limit(getNumInvitations())
		
		# if not a war congress, exclude civs in global wars
		if isGlobalWar() and not self.bPostWar:
			lAttackers, lDefenders = determineAlliances(data.iGlobalWarAttacker, data.iGlobalWarDefender)
			self.invites = self.invites.without(lAttackers)
			self.invites = self.invites.without(lDefenders)
			
		self.invites = self.invites.alive()
		
		# America receives an invite if there are still claims in the west
		if iAmerica not in self.invites and not self.bPostWar and year() > year(tBirth[iAmerica]):
			if cities.start(tAmericanClaimsTL).end(tAmericanClaimsBR).notowner(iAmerica):
				if len(self.invites) == getNumInvitations():
					self.invites = self.invites.limit(len(self.invites)-1)
				self.invites = self.invites.including(iAmerica)