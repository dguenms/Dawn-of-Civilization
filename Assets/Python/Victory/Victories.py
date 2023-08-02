from Core import *

from StoredData import data
from Events import events, handler
from Scenarios import getScenario
from GoalHandlers import event_handler_registry

from Types import *


### GLOBALS ###

dHistoricalGoals = None
dReligiousGoals = None
dAdditionalPaganGoal = None


### EVENT HANDLERS ###

@handler("fontsLoaded")
def loadVictories():
	import HistoricalVictory as Historical
	import ReligiousVictory as Religious
	
	global dHistoricalGoals
	global dReligiousGoals
	global dAdditionalPaganGoal
	
	dHistoricalGoals = Historical.dGoals
	dReligiousGoals = Religious.dGoals
	dAdditionalPaganGoal = Religious.dAdditionalPaganGoal


@handler("playerCivAssigned")
def assignGoals(iPlayer):
	if player(iPlayer).isHuman():
		data.players[iPlayer].historicalVictory = HistoricalVictory.create(iPlayer)
		data.players[iPlayer].religiousVictory = ReligiousVictory.create(iPlayer)


@handler("switch")
def onSwitch(iPrevious, iCurrent):
	data.players[iPrevious].historicalVictory.disable()
	data.players[iPrevious].religiousVictory.disable()
	
	data.players[iPrevious].historicalVictory = None
	data.players[iPrevious].religiousVictory = None
	
	data.players[iCurrent].historicalVictory = HistoricalVictory.create(iCurrent)
	data.players[iCurrent].religiousVictory = ReligiousVictory.create(iCurrent)
	

@handler("civicChanged")
def onCivicChanged(iPlayer, iOldCivic, iNewCivic):
	if iPlayer == active() and infos.civic(iOldCivic).isStateReligion() != infos.civic(iNewCivic).isStateReligion():
		switchReligiousGoals(iPlayer)


@handler("playerChangeStateReligion")
def onStateReligionChanged(iPlayer):
	if iPlayer == active():
		switchReligiousGoals(iPlayer)


@handler("victory")
def onVictory(iPlayer):
	if iPlayer == active():
		CyInterface().DoSoundtrack("AS2D_VICTORY")
	else:
		CyInterface().DoSoundtrack("AS2D_DEFEAT")


	
### UTILITY FUNCTIONS ###

def switchReligiousGoals(iPlayer):
	data.players[iPlayer].religiousVictory.disable()
	data.players[iPlayer].religiousVictory = ReligiousVictory.create(iPlayer)


### CLASSES ###

class Victory(object):

	def __init__(self, iPlayer, descriptions):
		self.iPlayer = iPlayer
		self.goals = tuple(self.create_goal(description) for description in descriptions)
		
		self.bGoldenAge = False
		self.bVictory = False
		
		self.enable()
		
	def enable(self):
		for goal in self.goals:
			goal.succeed = goal.override(self.goal_succeed())
			goal.fail = goal.override(self.goal_fail())
			
			goal.enable()
		
		events.addEventHandler("BeginGameTurn", self.check_complete)
	
	def disable(self):
		for goal in self.goals:
			goal.disable()
		
		events.removeEventHandler("BeginGameTurn", self.check_complete)

	def goal_succeed(self):
		def succeed(goal):
			goal.set_state(SUCCESS)
		
			if goal.succeeded():
				if goal.mode == STATEFUL:
					goal.announce_success()
			
				self.check()
		
		return succeed

	def goal_fail(self):
		def fail(goal):
			goal.set_state(FAILURE)
	
			if goal.state == FAILURE:
				goal.announce_failure()
		
		return fail

	def succeeded_goals(self):
		return count(goal.succeeded() for goal in self.goals)
	
	def num_goals(self):
		return len(self.goals)
	
	def area_names(self, tile):
		return [goal.area_name(tile) for goal in self.goals]
	
	def check(self):
		pass
	
	def check_complete(self, iGameTurn):
		if self.bGoldenAge:
			self.bGoldenAge = False
			self.golden_age()
		
		if self.bVictory:
			self.bVictory = False
			self.victory()
	
	def create_goal(self, description):
		return description(self.iPlayer)
	
	def victory(self):
		if game.getWinner() == -1:
			game.setWinner(self.iPlayer, self.VICTORY_TYPE)
	
	def golden_age(self):
		iGoldenAgeTurns = player(self.iPlayer).getGoldenAgeLength()
		player(self.iPlayer).changeGoldenAgeTurns(iGoldenAgeTurns)
		
		message(self.iPlayer, "TXT_KEY_VICTORY_INTERMEDIATE", color=iPurple)
		
		if player(self.iPlayer).isHuman():
			for iOtherPlayer in players.major().alive().without(self.iPlayer):
				player(iOtherPlayer).AI_changeAttitudeExtra(self.iPlayer, -2)


class HistoricalVictory(Victory):

	VICTORY_TYPE = VictoryTypes.VICTORY_HISTORICAL

	@classmethod
	def create(cls, iPlayer):
		iCiv = civ(iPlayer)
		return cls(iPlayer, dHistoricalGoals[iCiv])
	
	def enable(self):
		Victory.enable(self)
		
		getScenario().initGoals(self.iPlayer, self.goals)

	def check(self):
		iSucceededGoals = self.succeeded_goals()
		iNumGoals = self.num_goals()
		
		if iSucceededGoals == iNumGoals - 1:
			self.bGoldenAge = True
		elif iSucceededGoals == iNumGoals:
			self.bVictory = True
	

class ReligiousVictory(Victory):

	VICTORY_TYPE = VictoryTypes.VICTORY_RELIGIOUS

	@classmethod
	def create(cls, iPlayer):
		iStateReligion = player(iPlayer).getStateReligion()
		
		if iStateReligion >= 0:
			return cls(iPlayer, dReligiousGoals[iStateReligion])
		elif player(iPlayer).isStateReligion():
			iCivilization = player(iPlayer).getCivilizationType()
			iPaganReligion = infos.civ(iCivilization).getPaganReligion()
			return cls(iPlayer, concat(dReligiousGoals[iPaganVictory], dAdditionalPaganGoal[iPaganReligion]))
		else:
			return cls(iPlayer, dReligiousGoals[iSecularVictory])

	def check(self):
		if self.succeeded_goals() == self.num_goals():
			self.bVictory = True
	
	def create_goal(self, description):
		return description(self.iPlayer, mode=STATELESS)