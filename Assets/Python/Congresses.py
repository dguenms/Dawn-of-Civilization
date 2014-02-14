# Rhye's and Fall of Civilization - World Congresses

from CvPythonExtensions import *
import CvUtil
import PyHelpers 
import Popup
import RFCUtils
from Consts import *
import CityNameManager as cnm
from StoredData import sd # edead

### Globals ###

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()
localText = CyTranslator()

### Singleton ###

currentCongress = None

### Constants ###

iCongressInterval = 25

### Event Handlers ###

def setup():
	sd.setCongressTurns(utils.getTurns(iCongressInterval))

def checkTurn(iGameTurn):
	if isCongressEnabled():
		if not isGlobalWar():
			sd.changeCongressTurns(-1)
			
		if sd.getCongressTurns() == 0:
			sd.setCongressTurns(utils.getTurns(iCongressInterval))
			currentCongress = Congress()
			currentCongress.startCongress()

def onChangeWar(argsList):
	bWar, iPlayer, iOtherPlayer, bGlobalWar = argsList
	
	if isCongressEnabled():
		if bWar and bGlobalWar and not isGlobalWar():
			sd.setGlobalWarAttacker(iPlayer)
			sd.setGlobalWarDefender(iOtherPlayer)
		
		if not bWar and sd.getGlobalWarAttacker() in [iPlayer, iOtherPlayer] and sd.getGlobalWarDefender() in [iPlayer, iOtherPlayer]:
			endGlobalWar(iPlayer, iOtherPlayer)
			
### Global Methods ###

def isCongressEnabled():
	if gc.getGame().getBuildingClassCreatedCount(gc.getBuildingInfo(iUnitedNations).getBuildingClassType()) > 0:
		return False
		
	#if gc.getGame().getGameTurn() < getTurnForYear(tBirth[utils.getHumanID()]):
	#	return False
		
	return (gc.getGame().countKnownTechNumTeams(iNationalism) > 0)

def isGlobalWar():
	return (sd.getGlobalWarAttacker() != -1 and sd.getGlobalWarDefender() != -1)
	
def endGlobalWar(iAttacker, iDefender):
	sd.setGlobalWarAttacker(-1)
	sd.setGlobalWarDefender(-1)
	
	lAttackers = [iAttacker]
	lDefenders = [iDefender]
	
	# force peace for all allies of the belligerents
	for iLoopPlayer in range(iNumPlayers):
		if utils.isAVassal(iLoopPlayer): continue
		if gc.getTeam(iLoopPlayer).isDefensivePact(iAttacker) and gc.getTeam(iLoopPlayer).isAtWar(iDefender):
			lAttackers.append(iLoopPlayer)
			gc.getTeam(iLoopPlayer).makePeace(iDefender)
		if gc.getTeam(iLoopPlayer).isDefensivePact(iDefender) and gc.getTeam(iLoopPlayer).isAtWar(iAttacker):
			lDefenders.append(iLoopPlayer)
			gc.getTeam(iLoopPlayer).makePeace(iAttacker)
			
	if gc.getTeam(iAttacker).AI_getWarSuccess(iDefender) > gc.getTeam(iDefender).AI_getWarSuccess(iAttacker):
		lWinners = lAttackers
		lLosers = lDefenders
	else:
		lWinners = lDefenders
		lLosers = lAttackers
	
	currentCongress = Congress(lWinners, lLosers)
	currentCongress.start()
	
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

	### Popups ###
	
	def startIntroductionEvent(self, bHumanInvited):
		popup = CyPopupInfo()
		popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popup.setOnClickedPythonCallback("applyIntroductionEvent")
		
		sInviteString = ""
		for iPlayer in self.lInvites:
			if utils.getHumanID() != iPlayer:
				sInviteString += localText.getText("TXT_KEY_CONGRESS_INVITE", (gc.getPlayer(iPlayer).getCivilizationDescription(0),))
		
		if bHumanInvited:
			sText = localText.getText("TXT_KEY_CONGRESS_INTRODUCTION", (self.sHostCityName, sInviteString))
		else:
			sText = localText.getText("TXT_KEY_CONGRESS_INTRODUCTION_AI", (self.sHostCityName, sInviteString))
			
		popup.setText(sText)
			
		popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_OK", ()), '')
		popup.addPopup(utils.getHumanID())
		
	def applyIntroductionEvent(self):
		if utils.getHumanID() in self.lInvites:
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
				popup.addPythonButton(plot.getPlotCity().getName() + ' (' + str(iValue) + ')', gc.getCivilizationInfo(gc.getPlayer(plot.getPlotCity().getOwner()).getCivilizationType()).getButton())
			else:
				popup.addPythonButton(cnm.getFoundName(utils.getHumanID(), (x, y)) + ' (' + str(iValue) + ')', 'Art/Interface/Buttons/Actions/FoundCity.dds')
			
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
			
	def startResultsEvent(self, lAssignments, lColonies):
		sText = localText.getText("TXT_KEY_CONGRESS_RESULTS", (self.sHostCityName,))
		
		for tAssignment in lAssignments:
			sName, iOldOwner, iNewOwner = tAssignment
			sText += localText.getText("TXT_KEY_CONGRESS_RESULT_ASSIGNMENT", (sName, gc.getPlayer(iOldOwner).getCivilizationAdjective(0), gc.getPlayer(iNewOwner).getCivilizationAdjective(0)))
			
		for tColony in lColonies:
			sName, iOldOwner, iNewOwner = tColony
			if iOldOwner >= 0:
				sText += localText.getText("TXT_KEY_CONGRESS_RESULT_COLONY_TERRITORY", (sName, gc.getPlayer(iOldOwner).getCivilizationAdjective(0), gc.getPlayer(iNewOwner).getCivilizationShortDescription(0)))
			else:
				sText += localText.getText("TXT_KEY_CONGRESS_RESULT_COLONY", (sName, gc.getPlayer(iNewOwner).getCivilizationShortDescription(0)))
				
		if len(lAssignments) == 0 and len(lColonies) == 0:
			sText += localText.getText("TXT_KEY_CONGRESS_NO_RESULTS", ())
			
		popup = CyPopupInfo()
		popup.setText(sText)
		popup.addPythonButton(localText.getText("TXT_KEY_CONGRESS_OK", ()), '')
		
		popup.addPopup(utils.getHumanID())

	### Other Methods ###

	def startCongress(self):
		self.bPostWar = (len(self.lWinners) > 0)
		lPossibleInvites = []
		
		if self.bPostWar:
			lPossibleInvites.extend(self.lWinners)
			lPossibleInvites.extend(self.lLosers)
		else:
			lPossibleInvites = [i for i in range(iNumPlayers)]

		self.inviteToCongress(lPossibleInvites)
		
		if self.bPostWar:
			iHostPlayer = self.lWinners[0]
		else:
			iHostPlayer = utils.getRandomEntry(self.lInvites)
			
		self.sHostCityName = utils.getRandomEntry(utils.getCoreCityList(iHostPlayer, utils.getReborn(iHostPlayer))).getName()
		
		for iLoopPlayer in self.lInvites:
			if self.bPostWar and iLoopPlayer in self.lLosers: continue
			self.dPossibleClaims[iLoopPlayer] = self.selectClaims(iLoopPlayer)
			
		for iLoopPlayer in self.lInvites:
			if iLoopPlayer not in self.dPossibleClaims: continue
			
			if utils.getHumanID() == iLoopPlayer:
				self.startIntroductionEvent(True)
			else:
				self.makeClaimAI(iLoopPlayer)
				
		# procedure continues from the makeClaimHuman event
		
		# unless the player isn't involved, in that case resolve from here
		if utils.getHumanID() not in self.dPossibleClaims:
			self.startIntroductionEvent(False)
			#self.voteOnClaims()
			
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
	
		lAssignments = []
		lColonies = []
		
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
			
			bHuman = (plot.getOwner() == utils.getHumanID())
			# insert ability to refuse flips later
			
			if plot.isCity():
				lAssignments.append((plot.getPlotCity().getName(), plot.getOwner(), iClaimant))
				self.assignCity(iClaimant, plot.getOwner(), (x, y))
			else:
				lColonies.append((cnm.getFoundName(iClaimant, (x, y)), plot.getOwner(), iClaimant))
				self.foundColony(iClaimant, (x, y))
					
		self.startResultsEvent(lAssignments, lColonies)
					
	def assignCity(self, iPlayer, iOwner, tPlot):
		x, y = tPlot
		utils.completeCityFlip(x, y, iPlayer, iOwner, 80, False, False, True)
		
	def foundColony(self, iPlayer, tPlot):
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		
		if plot.isOwned(): utils.convertPlotCulture(plot, iPlayer, 100, True)
		
		if utils.getHumanID() == iPlayer:
			utils.makeUnit(iSettler, iPlayer, tPlot, 1)
		else:
			gc.getPlayer(iPlayer).found(x, y)
			
		utils.createGarrisons(tPlot, iPlayer, 2)
				
	def voteOnClaimsHuman(self):
		for iClaimant in self.dCityClaims:
			if utils.getHumanID() != iClaimant:
				x, y, iValue = self.dCityClaims[iClaimant]
				self.lHumanVotes.append((iClaimant, x, y))
				
		if len(self.lHumanVotes) > 0:
			iClaimant, x, y = self.lHumanVotes[0]
			self.startVoteCityEvent(iClaimant, (x, y))
			
	def voteOnClaimsAI(self):
		for iVoter in self.lInvites:
			if utils.getHumanID() != iVoter:
				for iClaimant in self.dCityClaims:
					if iVoter != iClaimant:
						x, y, iValue = self.dCityClaims[iClaimant]
						self.voteOnCityClaimAI(iVoter, iClaimant, (x, y), iValue)
						
		# continue with applying the votes
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
			
			# AI memory of human voting behavior
			if utils.getHumanID() == iClaimant and iVoter in self.dVotingMemory: iFavorClaimant += 5 * self.dVotingMemory[iVoter]
			if utils.getHumanID() == iOwner and iVoter in self.dVotingMemory: iFavorOwner += 5 * self.dVotingMemory[iVoter]
			
		# plot factors
		# plot culture
		if bOwner:
			iClaimValidity += (100 * plot.getCulture(iClaimant) / plot.countTotalCulture()) / 20

		# Europeans support colonialism unless they want the plot for themselves
		if iVoter in lCivGroups[0]:
			if iClaimant in lCivGroups[0]:
				if not bOwner or iOwner not in lCivGroups[0]:
					if plot.getSettlerMapValue(iVoter) < 90:
						iClaimValidity += 10
						
		# vote to support settler maps for civs from your own group
		if bOwner:
			bDifferentGroupClaimant = True
			bDifferentGroupOwner = True
			for lGroup in lCivGroups:
				if iVoter in lGroup and iClaimant in lGroup: bDifferentGroupClaimant = False
				if iVoter in lGroup and iOwner in lGroup: bDifferentGroupOwner = False
		
			iClaimantValue = plot.getSettlerMapValue(iClaimant)
			iOwnerValue = plot.getSettlerMapValue(iOwner)
			
			if not bDifferentGroupClaimant and bDifferentGroupOwner and iClaimantValue >= 90: iClaimantValue *= 2
			if not bDifferentGroupOwner and bDifferentGroupClaimant and iOwnerValue >= 90: iOwnerValue *= 2
			
			iClaimValidity += max(1, iClaimantValue / 100)
			iClaimValidity -= max(1, iOwnerValue / 100)
			
		# own expansion targets
		if not bOwnClaim:
			iOwnSettlerValue = plot.getSettlerMapValue(iVoter)
			iOwnWarTargetValue = plot.getWarMapValue(iVoter)
			
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
				
		bThreatenedClaimant = (2 * tVoter.getPower(True) < gc.getTeam(iClaimant).getPower(True))
		if bOwner: bThreatenedOwner = (2 * tVoter.getPower(True) < gc.getTeam(iOwner).getPower(True))
		
		# always vote for claims on empty territory unless claim is invalid
		if not bOwner:
			if iClaimValidity >= 0:
				self.vote(iVoter, iClaimant, 1)
				return
		
		# always vote for own claims unless threatened by owner
		if bOwnClaim:
			if not bOwner or not bThreatenedOwner:
				self.vote(iVoter, iClaimant, 1)
				return
				
		# always vote against claims on own cities unless threatened by owner
		if bOwner and bOwnCity:
			if not bThreatenedClaimant:
				self.vote(iVoter, iClaimant, -1)
				return
				
		# vote to assing minor cities if there is a valid claim
		if bOwner and bMinor:
			if iClaimValidity > 0:
				self.vote(iVoter, iClaimant, 1)
			else:
				self.vote(iVoter, iClaimant, -1)
			return
			
		# maybe include threatened here?
		if iClaimValidity > 0:
			# claim insufficient to overcome dislike
			if iFavorClaimant + iClaimValidity < iFavorOwner:
				self.vote(iVoter, iClaimant, -1)
			# valid claim and claimant is more liked
			elif iFavorClaimant > iFavorOwner:
				self.vote(iVoter, iClaimant, 1)
			# less liked, but justified by claim
			elif iFavorClaimant + iClaimValidity > iFavorOwner:
				iRand = gc.getGame().getSorenRandNum(40, 'Random vote outcome')
				if iRand < iClaimValidity:
					self.vote(iVoter, iClaimant, 1)
				else:
					self.vote(iVoter, iClaimant, -1)
					
				# bribery for human?
				
		else:
			# like them enough to overcome bad claim
			if iFavorClaimant + iClaimValidity > iFavorOwner:
				self.vote(iVoter, iClaimant, 1)
			else:
				self.vote(iVoter, iClaimant, -1)
				
	def vote(self, iVoter, iClaimant, iVote):
		if iClaimant in self.dVotes: self.dVotes[iClaimant] += iVote
		self.dVotes[iClaimant] += iVote
		if iVote == 1 and iVoter not in self.dVotedFor[iClaimant]: self.dVotedFor[iClaimant].append(iVoter)
				
	def makeClaimHuman(self):
		self.startClaimCityEvent()
		
	def makeClaimAI(self, iPlayer):
		x, y, iValue = utils.getHighestEntry(self.dPossibleClaims[iPlayer], lambda x: x[2])
		self.dCityClaims[iPlayer] = (x, y, iValue)
			
	def selectClaims(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iGameTurn = gc.getGame().getGameTurn()
		iNumPlayersAlive = gc.getGame().countCivPlayersAlive()
		lPlots = []
		
		for iLoopPlayer in range(iNumTotalPlayers+1):
			if iLoopPlayer == iPlayer: continue
			if not gc.getPlayer(iLoopPlayer).isAlive(): continue
			if iLoopPlayer in self.lWinners: continue
				
			# AI civs: cannot claim cities from friends
			if utils.getHumanID() != iPlayer and pPlayer.AI_getAttitude(iLoopPlayer) >= AttitudeTypes.ATTITUDE_FRIENDLY: continue
			
			# recently born
			if iGameTurn < getTurnForYear(tBirth[iLoopPlayer]) + utils.getTurns(20): continue
			
			# recently reborn
			if iGameTurn < pPlayer.getLatestRebellionTurn() + utils.getTurns(20): continue
			
			# check bribery here or when a claim is made?
			
			# exclude master/vassal relationships
			if gc.getTeam(iPlayer).isVassal(iLoopPlayer): continue
			if gc.getTeam(iLoopPlayer).isVassal(iPlayer): continue
			
			# Ethiopian UP
			if iLoopPlayer == iEthiopia: continue
			
			for city in utils.getCityList(iLoopPlayer):
				x, y = city.getX(), city.getY()
				plot = gc.getMap().plot(x, y)
				iSettlerMapValue = plot.getSettlerMapValue(iPlayer)
				iValue = 0
				
				if not plot.isRevealed(iPlayer, False): continue
				if city.isCapital(): continue
				
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
						if sd.getStabilityLevel(iLoopPlayer) == iStabilityCollapsing:
							if iSettlerMapValue >= 90:
								iValue += max(1, iSettlerMapValue / 100)
									
				# close to own empire
				closestCity = gc.getMap().findCity(x, y, iPlayer, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, city)
				iDistance = stepDistance(x, y, closestCity.getX(), closestCity.getY())
				if iDistance < 5:
					iValue += 5-iDistance
					
				# after war: war targets
				if self.bPostWar:
					iValue += plot.getWarMapValue(iPlayer) / 2
					
				if iValue > 0:
					lPlots.append((x, y, iValue))
		
		# extra spots for colonial civs -> will be settled
		# not available after wars because these congresses are supposed to reassign cities
		if iPlayer in lCivGroups[0] and not self.bPostWar:
			for x in range(iWorldX):
				for y in range(iWorldY):
					plot = gc.getMap().plot(x, y)
					if not plot.isCity() and not plot.isPeak() and not plot.isWater():
						if plot.getRegionID() in [rWestAfrica, rSouthAfrica, rEthiopia, rAustralia, rOceania]:
							iSettlerMapValue = plot.getSettlerMapValue(iPlayer)
							if iSettlerMapValue >= 90 and cnm.getFoundName(iPlayer, (x, y)) != "-1":
								closestCity = gc.getMap().findCity(x, y, PlayerTypes.NO_PLAYER, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
								if stepDistance(x, y, closestCity.getX(), closestCity.getY()) > 2:
									lPlots.append((x, y, max(1, iSettlerMapValue / 100)))
						
		lPlots = utils.getSortedList(lPlots, lambda x: x[2] + gc.getGame().getSorenRandNum(3, 'Randomize city value'), True)
		return lPlots[:10]
		
	def inviteToCongress(self, lPossibleInvites):
		lPossibleInvites = utils.getSortedList(lPossibleInvites, lambda x: gc.getGame().getPlayerRank(x))
		self.lInvites = lPossibleInvites[:getNumInvitations()]