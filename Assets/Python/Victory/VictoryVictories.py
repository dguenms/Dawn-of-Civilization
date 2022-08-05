from Core import *

from StoredData import data
from Events import handler
from Scenarios import getScenario

from VictoryTypes import *


### GLOBALS ###

dHistoricalGoals = None
dReligiousGoals = None
dAdditionalPaganGoal = None


### EVENT HANDLERS ###

@handler("fontsLoaded")
def loadVictories():
	import VictoryHistoricalVictory
	import VictoryReligiousVictory
	
	global dHistoricalGoals
	global dReligiousGoals
	global dAdditionalPaganGoal
	
	dHistoricalGoals = VictoryHistoricalVictory.dGoals
	dReligiousGoals = VictoryReligiousVictory.dGoals
	dAdditionalPaganGoal = VictoryReligiousVictory.dAdditionalPaganGoal


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


@handler("EndPlayerTurn")
def checkHistoricalGoldenAge(iGameTurn, iPlayer):
	if data.players[iPlayer].bLaunchHistoricalGoldenAge:
		data.players[iPlayer].bLaunchHistoricalGoldenAge = False
		goldenAge(iPlayer)
	
	
### UTILITY FUNCTIONS ###

def switchReligiousGoals(iPlayer):
	data.players[iPlayer].religiousVictory.disable()
	data.players[iPlayer].religiousVictory = ReligiousVictory.create(iPlayer)


def goldenAge(iPlayer):
	iGoldenAgeTurns = player(iPlayer).getGoldenAgeLength()
	player(iPlayer).changeGoldenAgeTurns(iGoldenAgeTurns)
	
	message(iPlayer, "TXT_KEY_VICTORY_INTERMEDIATE", color=iPurple)
	
	if player(iPlayer).isHuman():
		for iOtherPlayer in players.major().alive().without(iPlayer):
			player(iOtherPlayer).AI_changeAttitudeExtra(iPlayer, -2)


### CLASSES ###

class Victory(object):

	def __init__(self, iPlayer, descriptions):
		self.iPlayer = iPlayer
		self.goals = tuple(self.register_goal(description) for description in descriptions)

	def on_success(self, goal):
		goal.announce_success()
		self.check()

	def on_failure(self, goal):
		goal.announce_failure()

	def succeeded_goals(self):
		return count(goal.succeeded() for goal in self.goals)
	
	def num_goals(self):
		return len(self.goals)
	
	def area_names(self, tile):
		return [goal.area_name(tile) for goal in self.goals]
	
	def check(self):
		pass
	
	def create_goal(self, description):
		return description(self.iPlayer)

	def register_goal(self, description):
		def succeed(goal):
			goal.set_state(SUCCESS)
			
			if goal.state == SUCCESS:
				self.on_success(goal)

		def fail(goal):
			goal.set_state(FAILURE)
			
			if goal.state == FAILURE:
				self.on_failure(goal)

		goal = self.create_goal(description)
		
		goal.succeed = goal.override(succeed)
		goal.fail = goal.override(fail)
		
		return goal
	
	def enable(self):
		for goal in self.goals:
			goal.register_handlers()
	
	def disable(self):
		for goal in self.goals:
			goal.deregister_handlers()


class HistoricalVictory(Victory):

	@classmethod
	def create(cls, iPlayer):
		iCiv = civ(iPlayer)
		return cls(iPlayer, dHistoricalGoals[iCiv])

	def check(self):
		iSucceededGoals = self.succeeded_goals()
		iNumGoals = self.num_goals()
		
		if iSucceededGoals == iNumGoals - 1:
			self.golden_age()
		elif iSucceededGoals == iNumGoals:
			self.victory()
	
	def golden_age(self):
		data.players[self.iPlayer].bLaunchHistoricalGoldenAge = True
	
	def victory(self):
		if game.getWinner() == -1:
			game.setWinner(self.iPlayer, VictoryTypes.VICTORY_HISTORICAL)


class ReligiousVictory(Victory):

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
			self.victory()
	
	def victory(self):
		if game.getWinner() == -1:
			game.setWinner(self.iPlayer, VictoryTypes.VICTORY_RELIGIOUS)
	
	def create_goal(self, description):
		return description(self.iPlayer, mode=STATELESS)