# Rhye's and Fall of Civilization - World Congresses

from CvPythonExtensions import *
import CvUtil
import PyHelpers 
import Popup
from RFCUtils import utils
from Consts import *
import Areas
import CityNameManager as cnm
from StoredData import data # edead

### Globals ###

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
localText = CyTranslator()

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
	
		if not data.currentCongress and data.iCongressTurns == 0:
			data.iCongressTurns = getCongressInterval()
			currentCongress = Congress()
			data.currentCongress = currentCongress
			currentCongress.startCongress()

def onChangeWar(bWar, iPlayer, iOtherPlayer):
	if isCongressEnabled():
		if bWar and not isGlobalWar():
			lAttackers, lDefenders = determineAlliances(iPlayer, iOtherPlayer)
			
			if startsGlobalWar(lAttackers, lDefenders):
				iAttacker = utils.getHighestEntry(lAttackers, lambda iPlayer: gc.getTeam(iPlayer).getPower(True))
				iDefender = utils.getHighestEntry(lDefenders, lambda iPlayer: gc.getTeam(iPlayer).getPower(True))
			
				data.iGlobalWarAttacker = iAttacker
				data.iGlobalWarDefender = iDefender
		
		if not bWar and data.iGlobalWarAttacker in [iPlayer, iOtherPlayer] and data.iGlobalWarDefender in [iPlayer, iOtherPlayer]:
			endGlobalWar(iPlayer, iOtherPlayer)
			
### Global Methods ###

def getCongressInterval():
	if gc.getGame().getBuildingClassCreatedCount(gc.getBuildingInfo(iPalaceOfNations).getBuildingClassType()) > 0:
		return utils.getTurns(4)
		
	return utils.getTurns(15)

def isCongressEnabled():
	if data.bNoCongressOption:
		return False

	if gc.getGame().getBuildingClassCreatedCount(gc.getBuildingInfo(iUnitedNations).getBuildingClassType()) > 0:
		return False
		
	return (gc.getGame().countKnownTechNumTeams(iNationalism) > 0)
	
def startsGlobalWar(lAttackers, lDefenders):
	if len(lAttackers) < 2: return False
	if len(lDefenders) < 2: return False
	
	lWorldPowers = utils.getSortedList([i for i in range(iNumPlayers) if gc.getPlayer(i).isAlive() and not utils.isAVassal(i)], lambda iPlayer: gc.getTeam(iPlayer).getPower(True), True)
	
	iCount = len(lWorldPowers)/4
	lWorldPowers = lWorldPowers[:iCount]
	
	lParticipatingPowers = [iPlayer for iPlayer in lWorldPowers if iPlayer in lAttackers or iPlayer in lDefenders]
	
	return 2 * len(lParticipatingPowers) >= len(lWorldPowers)
				
def determineAlliances(iAttacker, iDefender):
	teamAttacker = gc.getTeam(iAttacker)
	teamDefender = gc.getTeam(iDefender)
	
	lAttackers = [iPlayer for iPlayer in range(iNumPlayers) if teamDefender.isAtWar(iPlayer)]
	lDefenders = [iPlayer for iPlayer in range(iNumPlayers) if teamAttacker.isAtWar(iPlayer)]

	return [iAttacker for iAttacker in lAttackers if iAttacker not in lDefenders], [iDefender for iDefender in lDefenders if iDefender not in lAttackers]

def isGlobalWar():
	return (data.iGlobalWarAttacker != -1 and data.iGlobalWarDefender != -1)
	
def endGlobalWar(iAttacker, iDefender):
	if not gc.getPlayer(iAttacker).isAlive() or not gc.getPlayer(iDefender).isAlive():
		return
		
	if data.currentCongress:
		return
	
	lAttackers = [iAttacker]
	lDefenders = [iDefender]
	
	lAttackers, lDefenders = determineAlliances(iAttacker, iDefender)
	
	# force peace for all allies of the belligerents
	for iLoopPlayer in lAttackers:
		if not gc.getPlayer(iLoopPlayer).isAlive(): continue
		if utils.isAVassal(iLoopPlayer): continue
		if iLoopPlayer == iAttacker: continue
		gc.getTeam(iLoopPlayer).makePeace(iDefender)
		
	for iLoopPlayer in lDefenders:
		if not gc.getPlayer(iLoopPlayer).isAlive(): continue
		if utils.isAVassal(iLoopPlayer): continue
		if iLoopPlayer == iDefender: continue
		gc.getTeam(iLoopPlayer).makePeace(iAttacker)
		
	if gc.getGame().determineWinner(iAttacker, iDefender) == iAttacker:
		lWinners = lAttackers
		lLosers = lDefenders
	else:
		lWinners = lDefenders
		lLosers = lAttackers
	
	currentCongress = Congress(lWinners, lLosers)
	data.currentCongress = currentCongress
	currentCongress.startCongress()
	
def getNumInvitations():
	return min(10, gc.getGame().countCivPlayersAlive())
	
def start():
	currentCongress = Congress()
	currentCongress.startCongress()
			
class Congress:
	
	### Constructor ###
	
	def __init__(self, lWinners = [], lLosers = []):
		self.sHostCityName = ""
		self.lInvites = []
		self.lWinners = lWinners
		self.lLosers = lLosers
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
	
	def startIntroductionEvent(self, bHumanInvited):
		popup = CyPopupInfo()
		popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popup.setOnClickedPythonCallback("applyIntroductionEvent")
		
		sInviteString = ""
		for iPlayer in self.lInvites:
			if utils.getHumanID() != iPlayer:
				sInviteString += localText.getText("TXT_KEY_CONGRESS_INVITE", (gc.getPlayer(iPlayer).getCivilizationDescription(0),))
				
		if self.bPostWar:
			if bHumanInvited: 
				if utils.getHumanID() in self.lWinners: sText = localText.getText("TXT_KEY_CONGRESS_INTRODUCTION_WAR_WON", (self.sHostCityName, sInviteString))
				elif utils.getHumanID() in self.lLosers: sText = localText.getText("TXT_KEY_CONGRESS_INTRODUCTION_WAR_LOST", (self.sHostCityName, sInviteString))
				else: sText = localText.getText("TXT_KEY_CONGRESS_INTRODUCTION_WAR", (self.sHostCityName, sInviteString))
			else: sText = localText.getText("TXT_KEY_CONGRESS_INTRODUCTION_WAR_AI", (self.sHostCityName, sInviteString))
		else:
			if bHumanInvited: sText = localText.getText("TXT_KEY_CONGRESS_INTRODUCTION", (self.sHostCityName, sInviteString))
			else: sText = localText.getText("TXT_KEY_CONGRESS_INTRODUCTION_AI", (self.sHostCityName, sInviteString))
			
		popup.setText(sText)
			
		popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_OK", ()), '')
		popup.addPopup(utils.getHumanID())
		
	def applyIntroductionEvent(self):
		# check one more time if player has collapsed in the meantime
		lRemove = []
		for iLoopPlayer in self.lInvites:
			if not gc.getPlayer(iLoopPlayer).isAlive(): lRemove.append(iLoopPlayer)
			
		for iLoopPlayer in lRemove:
			self.lInvites.remove(iLoopPlayer)
	
		# move AI claims here so they are made on the same turn as they are resolved - otherwise change of ownership might confuse things
		for iLoopPlayer in self.lInvites:
			if not self.canClaim(iLoopPlayer): continue
			self.dPossibleClaims[iLoopPlayer] = self.selectClaims(iLoopPlayer)
			
		for iLoopPlayer in self.lInvites:
			if iLoopPlayer not in self.dPossibleClaims: continue
			
			if utils.getHumanID() != iLoopPlayer:
				self.makeClaimAI(iLoopPlayer)
	
		if utils.getHumanID() in self.dPossibleClaims:
			# human still has to make a claim
			self.makeClaimHuman()
		else:
			# human cannot make claims, so let the AI vote
			self.voteOnClaims()

	def startClaimCityEvent(self):
		popup = CyPopupInfo()
		popup.setText(localText.getText("TXT_KEY_CONGRESS_CLAIM_CITY", (self.sHostCityName,)))
		popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popup.setOnClickedPythonCallback("applyClaimCityEvent")
		
		for tCity in self.dPossibleClaims[utils.getHumanID()]:
			x, y, iValue = tCity
			plot = gc.getMap().plot(x, y)
			if plot.isCity():
				popup.addPythonButton(plot.getPlotCity().getName(), gc.getCivilizationInfo(gc.getPlayer(plot.getPlotCity().getOwner()).getCivilizationType()).getButton())
			else:
				popup.addPythonButton(cnm.getFoundName(utils.getHumanID(), (x, y)), 'Art/Interface/Buttons/Actions/FoundCity.dds')
			
		popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_NO_REQUEST", ()), 'Art/Interface/Buttons/Actions/Cancel.dds')
		popup.addPopup(utils.getHumanID())

	def applyClaimCityEvent(self, iChoice):
		if iChoice < len(self.dPossibleClaims[utils.getHumanID()]):
			x, y, iValue = self.dPossibleClaims[utils.getHumanID()][iChoice]
			self.dCityClaims[utils.getHumanID()] = (x, y, iValue)

		self.voteOnClaims()	
		
	def startVoteCityEvent(self, iClaimant, tPlot):
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		
		if plot.isRevealed(utils.getHumanID(), False):
			plot.cameraLookAt()
		
		popup = CyPopupInfo()
		popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popup.setOnClickedPythonCallback("applyVoteCityEvent")
		popup.setData1(iClaimant)
		popup.setData2(plot.getOwner())
		
		sClaimant = gc.getPlayer(iClaimant).getCivilizationShortDescription(0)
		
		if plot.isCity():
			popup.setText(localText.getText("TXT_KEY_CONGRESS_REQUEST_CITY", (sClaimant, gc.getPlayer(plot.getOwner()).getCivilizationAdjective(0), plot.getPlotCity().getName())))
		elif plot.isOwned():
			popup.setText(localText.getText("TXT_KEY_CONGRESS_REQUEST_SETTLE_OWNED", (sClaimant, gc.getPlayer(plot.getOwner()).getCivilizationAdjective(0), cnm.getFoundName(iClaimant, tPlot))))
		else:
			popup.setText(localText.getText("TXT_KEY_CONGRESS_REQUEST_SETTLE", (sClaimant, cnm.getFoundName(iClaimant, tPlot))))
			
		popup.addPythonButton(localText.getText("TXT_KEY_POPUP_VOTE_YES", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_EVENT_BULLET")).getPath())
		popup.addPythonButton(localText.getText("TXT_KEY_POPUP_ABSTAIN", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_EVENT_BULLET")).getPath())
		popup.addPythonButton(localText.getText("TXT_KEY_POPUP_VOTE_NO", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_EVENT_BULLET")).getPath())
		
		popup.addPopup(utils.getHumanID())
		
	def applyVoteCityEvent(self, iClaimant, iOwner, iVote):
		self.vote(utils.getHumanID(), iClaimant, 1 - iVote) # yes=0, abstain=1, no=2
		
		if iClaimant in self.dVotingMemory: self.dVotingMemory[iClaimant] += (1 - iVote)
		if iOwner >= 0 and iOwner in self.dVotingMemory: self.dVotingMemory[iOwner] += (iVote - 1)
		self.iNumHumanVotes += 1
		
		# still votes to cast: start a new popup, otherwise let the AI vote
		if self.iNumHumanVotes < len(self.lHumanVotes):
			iNextClaimant, x, y = self.lHumanVotes[self.iNumHumanVotes]
			self.startVoteCityEvent(iNextClaimant, (x, y))
		else:
			self.voteOnClaimsAI()
			
	def startBriberyEvent(self, iVoter, iClaimant, tPlot, iDifference, iClaimValidity):
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		iBribedPlayer = iVoter
		
		bHumanClaim = (utils.getHumanID() == iClaimant)
		bCity = plot.isCity()
		
		if plot.isRevealed(utils.getHumanID(), False):
			plot.cameraLookAt()
		
		if bHumanClaim:
			if bCity:
				sText = localText.getText("TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_CITY", (gc.getPlayer(iBribedPlayer).getCivilizationAdjective(0), gc.getPlayer(plot.getOwner()).getCivilizationAdjective(0), plot.getPlotCity().getName()))
			else:
				closestCity = gc.getMap().findCity(x, y, iBribedPlayer, TeamTypes.NO_TEAM, True, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
				sText = localText.getText("TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_COLONY", (gc.getPlayer(iBribedPlayer).getCivilizationAdjective(0), gc.getPlayer(plot.getOwner()).getCivilizationAdjective(0), closestCity.getName()))
		else:	
			if bCity:
				sText = localText.getText("TXT_KEY_CONGRESS_BRIBE_OWN_CITY", (gc.getPlayer(iBribedPlayer).getCivilizationAdjective(0), gc.getPlayer(iClaimant).getCivilizationAdjective(0), plot.getPlotCity().getName()))
			else:
				closestCity = gc.getMap().findCity(x, y, utils.getHumanID(), TeamTypes.NO_TEAM, True, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
				sText = localText.getText("TXT_KEY_CONGRESS_BRIBE_OWN_TERRITORY", (gc.getPlayer(iBribedPlayer).getCivilizationAdjective(0), gc.getPlayer(iClaimant).getCivilizationAdjective(0), closestCity.getName()))
				
		iCost = iDifference * gc.getPlayer(iBribedPlayer).calculateTotalCommerce() / 5
		
		# make sure costs are positive
		if iCost < 100: iCost = 100
		
		iTreasury = gc.getPlayer(utils.getHumanID()).getGold()
		iEspionageSpent = gc.getTeam(utils.getHumanID()).getEspionagePointsAgainstTeam(iBribedPlayer)
		
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
				button = gc.getCommerceInfo(iCommerceType).getButton()
			elif iCommerceType == 3: 
				textKey = "TXT_KEY_CONGRESS_MANIPULATION"
				button = 'Art/Interface/Buttons/Espionage.dds'
				
			if iThreshold == iLowChance: sChance = "TXT_KEY_CONGRESS_CHANCE_AVERAGE"
			elif iThreshold == iHighChance: sChance = "TXT_KEY_CONGRESS_CHANCE_VERY_HIGH"
			else: sChance = "TXT_KEY_CONGRESS_CHANCE_HIGH"
			
			sChance = localText.getText(sChance, ())
			
			popup.addPythonButton(localText.getText(textKey, (iCost, sChance)), button)
			
		if self.lBriberyOptions:
			popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_NO_BRIBE", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_BUTTONS_CANCEL")).getPath())
		else:
			popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_CANNOT_AFFORD_BRIBE", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_BUTTONS_CANCEL")).getPath())
		
		popup.addPopup(utils.getHumanID())
		
	def applyBriberyEvent(self, iChoice, iBribedPlayer, iClaimant, iClaimValidity):
		if iChoice < len(self.lBriberyOptions):
			iCommerceType, iCost, iThreshold = self.lBriberyOptions[iChoice]
			iRand = gc.getGame().getSorenRandNum(100, 'Influence voting')
			
			if iCommerceType == 0: gc.getPlayer(utils.getHumanID()).changeGold(-iCost)
			elif iCommerceType == 3: gc.getTeam(utils.getHumanID()).changeEspionagePointsAgainstTeam(iBribedPlayer, -iCost)
			
			bHumanClaim = (utils.getHumanID() == iClaimant)
			bSuccess = (iRand < iThreshold)
			
			self.startBriberyResultEvent(iBribedPlayer, iClaimant, bHumanClaim, bSuccess)
		else:
			# if no bribery option was chosen, the civ votes randomly as usual
			iRand = gc.getGame().getSorenRandNum(50, 'Uninfluenced voting')
			if iRand < iClaimValidity:
				self.vote(iBribedPlayer, iClaimant, 1)
			else:
				self.vote(iBribedPlayer, iClaimant, -1)
				
			# to continue the process
			self.applyBriberyResultEvent()
				
	def startBriberyResultEvent(self, iBribedPlayer, iClaimant, bHumanClaim, bSuccess):	
		if bSuccess:
			if bHumanClaim:
				sText = localText.getText("TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_SUCCESS", (gc.getPlayer(iBribedPlayer).getCivilizationShortDescription(0),))
				self.vote(iBribedPlayer, iClaimant, 1)
			else:
				sText = localText.getText("TXT_KEY_CONGRESS_BRIBE_THEIR_CLAIM_SUCCESS", (gc.getPlayer(iBribedPlayer).getCivilizationShortDescription(0),))
				self.vote(iBribedPlayer, iClaimant, -1)
		else:
			if bHumanClaim:
				sText = localText.getText("TXT_KEY_CONGRESS_BRIBE_OWN_CLAIM_FAILURE", (gc.getPlayer(iBribedPlayer).getCivilizationShortDescription(0),))
				self.vote(iBribedPlayer, iClaimant, -1)
			else:
				sText = localText.getText("TXT_KEY_CONGRESS_BRIBE_THEIR_CLAIM_FAILURE", (gc.getPlayer(iBribedPlayer).getCivilizationShortDescription(0),))
				self.vote(iBribedPlayer, iClaimant, 1)
				
			gc.getPlayer(iBribedPlayer).AI_changeMemoryCount(utils.getHumanID(), MemoryTypes.MEMORY_STOPPED_TRADING_RECENT, 1)
			gc.getPlayer(iBribedPlayer).AI_changeAttitudeExtra(utils.getHumanID(), -2)
			
		popup = CyPopupInfo()
		popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popup.setOnClickedPythonCallback("applyBriberyResultEvent")
		popup.setText(sText)
		popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_OK", ()), '')
		
		popup.addPopup(utils.getHumanID())
		
	def applyBriberyResultEvent(self):
		# just continue to the next bribe if there is one
		self.iNumBribes += 1
		if self.iNumBribes < len(self.lPossibleBribes):
			iVoter, iClaimant, tPlot, iDifference, iClaimValidity = self.lPossibleBribes[self.iNumBribes]
			self.startBriberyEvent(iVoter, iClaimant, tPlot, iDifference, iClaimValidity)
		else:
			# otherwise continue with applying the votes
			self.applyVotes()
			
	def startRefusalEvent(self, iClaimant, tPlot):
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		
		if plot.isRevealed(utils.getHumanID(), False):
			plot.cameraLookAt()
		
		popup = CyPopupInfo()
		popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popup.setOnClickedPythonCallback("applyRefusalEvent")
		popup.setData1(iClaimant)
		popup.setData2(x)
		popup.setData3(y)
		
		sVotedYes = ""
		for iPlayer in self.dVotedFor[iClaimant]:
			if utils.getHumanID() != iPlayer and iClaimant != iPlayer:
				sVotedYes += localText.getText("TXT_KEY_CONGRESS_INVITE", (gc.getPlayer(iPlayer).getCivilizationDescription(0),))
		
		
		if plot.isCity():
			sText = localText.getText("TXT_KEY_CONGRESS_DEMAND_CITY", (gc.getPlayer(iClaimant).getCivilizationShortDescription(0), plot.getPlotCity().getName(), sVotedYes))
		else:
			closestCity = gc.getMap().findCity(x, y, utils.getHumanID(), TeamTypes.NO_TEAM, True, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
			sText = localText.getText("TXT_KEY_CONGRESS_DEMAND_TERRITORY", (gc.getPlayer(iClaimant).getCivilizationShortDescription(0), closestCity.getName(), sVotedYes))
			
		popup.setText(sText)
		popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_ACCEPT", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_EVENT_BULLET")).getPath())
		popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_REFUSE", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_EVENT_BULLET")).getPath())
		popup.addPopup(utils.getHumanID())
		
	def applyRefusalEvent(self, iChoice, iClaimant, x, y):
		if iChoice == 0:
			tPlot = (x, y)
			plot = gc.getMap().plot(x, y)
			if plot.isCity():
				self.assignCity(iClaimant, plot.getOwner(), tPlot)
			else:
				self.foundColony(iClaimant, tPlot)
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
		if gc.getGame().getGameTurn() >= getTurnForYear(tBirth[utils.getHumanID()]):
	
			sText = localText.getText("TXT_KEY_CONGRESS_RESULTS", (self.sHostCityName,))
		
			for tAssignment in self.lAssignments:
				sName, iOldOwner, iNewOwner = tAssignment
				sText += localText.getText("TXT_KEY_CONGRESS_RESULT_ASSIGNMENT", (sName, gc.getPlayer(iOldOwner).getCivilizationAdjective(0), gc.getPlayer(iNewOwner).getCivilizationAdjective(0)))
			
			for tColony in self.lColonies:
				sName, iOldOwner, iNewOwner = tColony
				if iOldOwner >= 0:
					sText += localText.getText("TXT_KEY_CONGRESS_RESULT_COLONY_TERRITORY", (sName, gc.getPlayer(iOldOwner).getCivilizationAdjective(0), gc.getPlayer(iNewOwner).getCivilizationShortDescription(0)))
				else:
					sText += localText.getText("TXT_KEY_CONGRESS_RESULT_COLONY", (sName, gc.getPlayer(iNewOwner).getCivilizationShortDescription(0)))
				
			if len(self.lAssignments) == 0 and len(self.lColonies) == 0:
				sText += localText.getText("TXT_KEY_CONGRESS_NO_RESULTS", ())
			
			popup = CyPopupInfo()
			popup.setText(sText)
			popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_OK", ()), '')
		
			popup.addPopup(utils.getHumanID())
			
		# if this was triggered by a war, reset belligerents
		if isGlobalWar():
			data.iGlobalWarAttacker = -1
			data.iGlobalWarDefender = -1
		
		# don't waste memory
		data.currentCongress = None

	### Other Methods ###

	def startCongress(self):
		self.bPostWar = (len(self.lWinners) > 0)
		
		utils.debugTextPopup('Congress takes place')

		self.inviteToCongress()
		
		if self.bPostWar:
			iHostPlayer = [iWinner for iWinner in self.lWinners if gc.getPlayer(iWinner).isAlive()][0]
		else:
			iHostPlayer = utils.getRandomEntry(self.lInvites)
			
		# establish contact between all participants
		for iThisPlayer in self.lInvites:
			for iThatPlayer in self.lInvites:
				if iThisPlayer != iThatPlayer:
					tThisPlayer = gc.getTeam(iThisPlayer)
					if not tThisPlayer.canContact(iThatPlayer): tThisPlayer.meet(iThatPlayer, False)

		self.sHostCityName = utils.getRandomEntry(utils.getOwnedCoreCities(iHostPlayer, utils.getReborn(iHostPlayer))).getName()
		
		# moved selection of claims after the introduction event so claims and their resolution take place at the same time
		if utils.getHumanID() in self.lInvites:
			self.startIntroductionEvent(True)
				
		# procedure continues from the makeClaimHuman event
		
		# unless the player isn't involved, in that case resolve from here
		if utils.getHumanID() not in self.lInvites:
			# since Congresses now can occur during autoplay, don't display these congresses to the player
			if gc.getGame().getGameTurn() >= getTurnForYear(tBirth[utils.getHumanID()]):
				self.startIntroductionEvent(False)
			else:
				# select claims first, then move on to voting directly since the player isn't involved
				for iLoopPlayer in self.lInvites:
					if not self.canClaim(iLoopPlayer): continue
					self.dPossibleClaims[iLoopPlayer] = self.selectClaims(iLoopPlayer)
					
				for iLoopPlayer in self.lInvites:
					if iLoopPlayer not in self.dPossibleClaims: continue
					
					if utils.getHumanID() != iLoopPlayer:
						self.makeClaimAI(iLoopPlayer)
						
				self.voteOnClaims()
			
	def voteOnClaims(self):
		# only humans vote so AI memory can influence their actions later
		for iVoter in self.lInvites:
			self.dVotes[iVoter] = 0
			self.dVotingMemory[iVoter] = 0
			self.dVotedFor[iVoter] = []
			if utils.getHumanID() == iVoter:
				self.voteOnClaimsHuman()
				
		# procedure continues from the voteOnClaimsHuman event
				
		# unless the player isn't involved, in that case resolve from here
		if utils.getHumanID() not in self.lInvites:
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
					
		for tAssignedPlot in dResults:
			x, y = tAssignedPlot
			iClaimant, iVotes = dResults[tAssignedPlot]
			plot = gc.getMap().plot(x, y)
			
			bCanRefuse = (plot.getOwner() == utils.getHumanID() and utils.getHumanID() not in self.dVotedFor[iClaimant] and not (self.bPostWar and utils.getHumanID() in self.lLosers))
			
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
			if utils.isAVassal(iVoter): continue
			if iVoter not in self.dPossibleBelligerents:
				self.dPossibleBelligerents[iVoter] = iVotes
			else:
				self.dPossibleBelligerents[iVoter] += iVotes
					
	def assignCity(self, iPlayer, iOwner, tPlot):
		x, y = tPlot
		city = gc.getMap().plot(x, y).getPlotCity()
		
		iNumDefenders = max(2, gc.getPlayer(iPlayer).getCurrentEra()-1)
		lFlippingUnits, lRelocatedUnits = utils.flipOrRelocateGarrison(city, iNumDefenders)
		
		utils.completeCityFlip(x, y, iPlayer, iOwner, 80, False, False, True)
		
		utils.flipOrCreateDefenders(iPlayer, lFlippingUnits, (x, y), iNumDefenders)
		
		if iOwner < iNumPlayers:
			utils.relocateUnitsToCore(iPlayer, lRelocatedUnits)
		else:
			utils.killUnits(lRelocatedUnits)
		
	def foundColony(self, iPlayer, tPlot):
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		
		if plot.isOwned(): utils.convertPlotCulture(plot, iPlayer, 100, True)
		
		if utils.getHumanID() == iPlayer:
			utils.makeUnit(iSettler, iPlayer, tPlot, 1)
		else:
			gc.getPlayer(iPlayer).found(x, y)
			
		utils.createGarrisons(tPlot, iPlayer, 2)
		
	def finishCongress(self):
		# declare war against human if he refused demands
		iGlobalWarModifier = 0
		tHuman = gc.getTeam(utils.getHumanID())
		for iLoopPlayer in range(iNumPlayers):
			if tHuman.isDefensivePact(iLoopPlayer):
				iGlobalWarModifier += 10
				
		for iBelligerent in self.dPossibleBelligerents:
			iRand = gc.getGame().getSorenRandNum(100, 'Random declaration of war')
			iThreshold = 10 + tPatienceThreshold[iBelligerent] - 5 * self.dPossibleBelligerents[iBelligerent] - iGlobalWarModifier
			if iRand >= iThreshold:
				gc.getTeam(iBelligerent).declareWar(utils.getHumanID(), False, WarPlanTypes.WARPLAN_DOGPILE)
				
		# display Congress results
		self.startResultsEvent()
				
	def voteOnClaimsHuman(self):
		for iClaimant in self.dCityClaims:
			if utils.getHumanID() != iClaimant:
				x, y, iValue = self.dCityClaims[iClaimant]
				self.lHumanVotes.append((iClaimant, x, y))
				
		if len(self.lHumanVotes) > 0:
			iClaimant, x, y = self.lHumanVotes[0]
			self.startVoteCityEvent(iClaimant, (x, y))
			
	def voteOnClaimsAI(self):
		for iClaimant in self.dCityClaims:
			x, y, iValue = self.dCityClaims[iClaimant]
			
			lVoters = self.lInvites
			
			plot = gc.getMap().plot(x, y)
			if plot.isOwned():
				iOwner = plot.getOwner()
				if iOwner not in lVoters and iOwner in self.getHighestRankedPlayers([i for i in range(iNumPlayers)], getNumInvitations()):
					lVoters.append(iOwner)
			
			if utils.getHumanID() in lVoters: lVoters.remove(utils.getHumanID())
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
			
	def voteOnCityClaimAI(self, iVoter, iClaimant, tPlot, iClaimValue):
		iFavorClaimant = 0
		iFavorOwner = 0
		
		iClaimValidity = 0
		
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		pVoter = gc.getPlayer(iVoter)
		tVoter = gc.getTeam(iVoter)
		
		iOwner = plot.getOwner()
		iNumPlayersAlive = gc.getGame().countCivPlayersAlive()
		
		bCity = plot.isCity()
		bOwner = (iOwner >= 0)
		bOwnClaim = (iClaimant == iVoter)
		
		if bCity: city = plot.getPlotCity()
		if bOwner: 
			bMinor = (iOwner >= iNumPlayers)
			bOwnCity = (iOwner == iVoter)
			bWarClaim = (iClaimant in self.lWinners and iOwner in self.lLosers)
			
		sDebugText = '\nVote City AI Debug\nVoter: ' + gc.getPlayer(iVoter).getCivilizationShortDescription(0) + '\nClaimant: ' + gc.getPlayer(iClaimant).getCivilizationShortDescription(0)
		if bCity: sDebugText += '\nCity claim: ' + city.getName()
		if bOwner: sDebugText += '\nOwner: ' + gc.getPlayer(iOwner).getCivilizationShortDescription(0)
		
		print sDebugText
		
		# everyone agrees on AI American claims in the west
		if iClaimant == iAmerica and iVoter != iOwner:
			if utils.isPlotInArea((x, y), tAmericanClaimsTL, tAmericanClaimsBR):
				self.vote(iVoter, iClaimant, 1)
				return
			
		# player factors
		if bOwner and not bMinor and not bOwnCity and not bOwnClaim:
			# player rank
			iFavorClaimant += iNumPlayersAlive / 2 - gc.getGame().getPlayerRank(iClaimant)
			iFavorOwner += iNumPlayersAlive / 2 - gc.getGame().getPlayerRank(iOwner)
			
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
			if not gc.getGame().isNeighbors(iVoter, iClaimant): iFavorClaimant += 5
			if not gc.getGame().isNeighbors(iVoter, iOwner): iFavorOwner += 10
			
			# vassalage
			if tVoter.isVassal(iClaimant): iFavorClaimant += 20
			if tVoter.isVassal(iOwner): iFavorOwner += 20
			
			if gc.getTeam(iClaimant).isVassal(iVoter): iFavorClaimant += 10
			if gc.getTeam(iOwner).isVassal(iVoter): iFavorOwner += 10
			
			# French UP
			if iClaimant == iFrance: iFavorClaimant += 10
			if iOwner == iFrance: iFavorOwner += 10
			
			# Palace of Nations
			if gc.getPlayer(iClaimant).isHasBuildingEffect(iPalaceOfNations): iFavorClaimant += 10
			
			# AI memory of human voting behavior
			if utils.getHumanID() == iClaimant and iVoter in self.dVotingMemory: iFavorClaimant += 5 * self.dVotingMemory[iVoter]
			if utils.getHumanID() == iOwner and iVoter in self.dVotingMemory: iFavorOwner += 5 * self.dVotingMemory[iVoter]
			
		# if we don't dislike them, agree with the value of their claim
		if pVoter.AI_getAttitude(iClaimant) >= AttitudeTypes.ATTITUDE_CAUTIOUS: iClaimValidity += iClaimValue
			
		# French UP
		if iClaimant == iFrance: iClaimValidity += 5
			
		# plot factors
		# plot culture
		if bOwner:
			iClaimValidity += (100 * plot.getCulture(iClaimant) / plot.countTotalCulture()) / 20
			
			# after wars: claiming from a non-participant has less legitimacy unless its your own claim
			if self.bPostWar and not bOwnClaim and iOwner not in self.lLosers:
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
				iClaimantPower = gc.getTeam(iClaimant).getPower(True)
				iOwnerPower = gc.getTeam(iOwner).getPower(True)
			
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
				
		bThreatenedClaimant = (2 * tVoter.getPower(True) < gc.getTeam(iClaimant).getPower(True))
		if bOwner: bThreatenedOwner = (2 * tVoter.getPower(True) < gc.getTeam(iOwner).getPower(True))
		
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
			if tVoter.isAtWar(iClaimant) and gc.getTeam(iOwner).isAtWar(iClaimant) and not tVoter.isAtWar(iOwner):
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
				if (iClaimant == utils.getHumanID() or (bOwner and iOwner == utils.getHumanID())) and iClaimValidity < 50 and iFavorOwner - iFavorClaimant > 0:
					# return the relevant data to be added to the list of possible bribes in the calling method
					print 'NO VOTE: open for bribes'
					return (iVoter, iClaimant, tPlot, iFavorOwner - iFavorClaimant, iClaimValidity)
				else:
					iRand = gc.getGame().getSorenRandNum(50, 'Random vote outcome')
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
		if len(self.dPossibleClaims[iPlayer]) == 0: return
		x, y, iValue = utils.getHighestEntry(self.dPossibleClaims[iPlayer], lambda x: x[2])
		self.dCityClaims[iPlayer] = (x, y, iValue)
		
	def canClaim(self, iPlayer):
		if not self.bPostWar: return True
		
		if iPlayer in self.lWinners: return True
		
		if iPlayer in self.lLosers: return True
		
		return False
			
	def selectClaims(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iGameTurn = gc.getGame().getGameTurn()
		iNumPlayersAlive = gc.getGame().countCivPlayersAlive()
		lPlots = []
		
		for iLoopPlayer in range(iNumTotalPlayers+1):
			if iLoopPlayer == iPlayer: continue
			if not gc.getPlayer(iLoopPlayer).isAlive(): continue
			
			# after a war: winners can only claim from losers and vice versa
			if self.bPostWar:
				if iPlayer in self.lWinners and iLoopPlayer not in self.lLosers: continue
				if iPlayer in self.lLosers and iLoopPlayer not in self.lWinners: continue
				
			# AI civs: cannot claim cities from friends
			if utils.getHumanID() != iPlayer and pPlayer.AI_getAttitude(iLoopPlayer) >= AttitudeTypes.ATTITUDE_FRIENDLY: continue
			
			# recently born
			if iGameTurn < getTurnForYear(tBirth[iLoopPlayer]) + utils.getTurns(20): continue
			
			# recently resurrected
			if iGameTurn < pPlayer.getLatestRebellionTurn() + utils.getTurns(20): continue
			
			# recently reborn
			if utils.isReborn(iLoopPlayer) and iLoopPlayer in dRebirth and iGameTurn < getTurnForYear(dRebirth[iLoopPlayer]) + utils.getTurns(20): continue
			
			# exclude master/vassal relationships
			if gc.getTeam(iPlayer).isVassal(iLoopPlayer): continue
			if gc.getTeam(iLoopPlayer).isVassal(iPlayer): continue
			
			# cannot demand cities while at war
			if gc.getTeam(iPlayer).isAtWar(iLoopPlayer): continue
			
			# Palace of Nations effect
			if gc.getPlayer(iLoopPlayer).isHasBuildingEffect(iPalaceOfNations): continue
			
			for city in utils.getCityList(iLoopPlayer):
				x, y = city.getX(), city.getY()
				plot = gc.getMap().plot(x, y)
				iSettlerMapValue = plot.getSettlerValue(iPlayer)
				iValue = 0
				
				if not plot.isRevealed(iPlayer, False): continue
				if city.isCapital(): continue
				
				# after a war: losers can only claim previously owned cities
				if self.bPostWar and iPlayer in self.lLosers:
					if city.getGameTurnPlayerLost(iPlayer) < gc.getGame().getGameTurn() - utils.getTurns(25): continue
				
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
					if iLoopPlayer >= iNumPlayers or (iLoopPlayer not in lCivGroups[0] and utils.getStabilityLevel(iLoopPlayer) < iStabilityShaky) or (iLoopPlayer in lCivGroups[0] and utils.getHumanID() != iLoopPlayer and pPlayer.AI_getAttitude(iLoopPlayer) < AttitudeTypes.ATTITUDE_PLEASED):
						if plot.getRegionID() not in lEurope and plot.getRegionID() not in lMiddleEast:
							if iSettlerMapValue > 90:
								iValue += max(1, iSettlerMapValue / 100)
									
				# weaker and collapsing empires
				if iLoopPlayer < iNumPlayers:
					if gc.getGame().getPlayerRank(iLoopPlayer) > iNumPlayersAlive / 2 and gc.getGame().getPlayerRank(iLoopPlayer) < iNumPlayersAlive / 2:
						if data.players[iLoopPlayer].iStabilityLevel == iStabilityCollapsing:
							if iSettlerMapValue >= 90:
								iValue += max(1, iSettlerMapValue / 100)
									
				# close to own empire
				closestCity = gc.getMap().findCity(x, y, iPlayer, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, city)
				iDistance = stepDistance(x, y, closestCity.getX(), closestCity.getY())
				if iDistance < 5:
					iValue += 5-iDistance
					
				# after war: war targets
				if self.bPostWar:
					iValue += plot.getWarValue(iPlayer) / 2
					
				# AI America receives extra value for claims in the west
				if iPlayer == iAmerica and utils.getHumanID() != iPlayer:
					if utils.isPlotInArea((x, y), tAmericanClaimsTL, tAmericanClaimsBR):
						iValue += 5
						
				# help Canada gain Labrador and Newfoundland
				if iPlayer == iCanada:
					if utils.isPlotInArea((x, y), tNewfoundlandTL, tNewfoundlandBR):
						iValue += 5
					
				if iValue > 0:
					lPlots.append((x, y, iValue))
		
		# extra spots for colonial civs -> will be settled
		# not available after wars because these congresses are supposed to reassign cities
		if iPlayer in lCivGroups[0] and not self.bPostWar:
			for (x, y) in utils.getWorldPlotsList():
				if utils.getHumanID() == iPlayer and not plot.isRevealed(iPlayer, False): continue
				plot = gc.getMap().plot(x, y)
				if not plot.isCity() and not plot.isPeak() and not plot.isWater() and pPlayer.canFound(x, y):
					if plot.getRegionID() in [rWestAfrica, rSouthAfrica, rEthiopia, rAustralia, rOceania]:
						iSettlerMapValue = plot.getSettlerValue(iPlayer)
						if iSettlerMapValue >= 90 and cnm.getFoundName(iPlayer, (x, y)):
							closestCity = gc.getMap().findCity(x, y, PlayerTypes.NO_PLAYER, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
							if stepDistance(x, y, closestCity.getX(), closestCity.getY()) > 2:
								lPlots.append((x, y, max(1, iSettlerMapValue / 100 - 1)))
						
		lPlots = utils.getSortedList(lPlots, lambda x: x[2] + gc.getGame().getSorenRandNum(3, 'Randomize city value'), True)
		return lPlots[:10]
		
	def getHighestRankedPlayers(self, lPlayers, iNumPlayers):
		lSortedPlayers = utils.getSortedList(lPlayers, lambda x: gc.getGame().getPlayerRank(x))
		return lSortedPlayers[:iNumPlayers]
		
	def inviteToCongress(self):
		rank = lambda x: gc.getGame().getPlayerRank(x)
		lPossibleInvites = []
	
		if self.bPostWar:
			iLowestWinnerRank = rank(utils.getSortedList(self.lWinners, rank)[0])
			lPossibleInvites.extend(self.lWinners)
			lPossibleInvites.extend([iLoser for iLoser in self.lLosers if rank(iLoser) < iLowestWinnerRank])
			
		lPossibleInvites.extend(utils.getSortedList([iPlayer for iPlayer in range(iNumPlayers) if iPlayer not in lPossibleInvites], rank))
	
		self.lInvites = lPossibleInvites[:getNumInvitations()]
		
		lRemove = []
		
		# if not a war congress, exclude civs in global wars
		if isGlobalWar() and not self.bPostWar:
			lAttackers, lDefenders = determineAlliances(data.iGlobalWarAttacker, data.iGlobalWarDefender)
			lRemove.extend(lAttackers)
			lRemove.extend(lDefenders)
			
		for iLoopPlayer in self.lInvites:
			if not gc.getPlayer(iLoopPlayer).isAlive(): lRemove.append(iLoopPlayer)
			
		for iLoopPlayer in lRemove:
			if iLoopPlayer in self.lInvites:
				self.lInvites.remove(iLoopPlayer)
		
		# Leoreth: America receives an invite if there are still claims in the west
		if iAmerica not in self.lInvites and not self.bPostWar and gc.getGame().getGameTurn() > tBirth[iAmerica]:
			lAmericanClaimCities = utils.getAreaCities(utils.getPlotList(tAmericanClaimsTL, tAmericanClaimsBR))
			if utils.satisfies(lAmericanClaimCities, lambda x: x.getOwner() != iAmerica):
				self.lInvites[len(self.lInvites)-1] = iAmerica