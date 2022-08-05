from Core import *

from StoredData import data
from Events import handler
from Scenarios import getScenario


### DELAYED IMPORT ###

dHistoricalGoals = None
dReligiousGoals = None
dPaganGoals = None

@handler("fontsLoaded")
def onFontsLoaded():
	from HistoricalVictory import dGoals as dDefinedHistoricalGoals
	global dHistoricalGoals
	dHistoricalGoals = dDefinedHistoricalGoals
	
	from ReligiousVictory import dGoals as dDefinedReligiousGoals
	global dReligiousGoals
	dReligiousGoals = dDefinedReligiousGoals
	
	from ReligiousVictory import dAdditionalPaganGoal
	global dPaganGoals
	dPaganGoals = dAdditionalPaganGoal
	
def getHistoricalGoals(iPlayer):
	return list(dHistoricalGoals[civ(iPlayer)])

def getReligiousGoals(iPlayer):
	iStateReligion = player(iPlayer).getStateReligion()
	if iStateReligion >= 0:
		return list(dReligiousGoals[iStateReligion])
	elif player(iPlayer).isStateReligion():
		return concat(dReligiousGoals[iPaganVictory], dPaganGoals[infos.civ(civ(iPlayer)).getPaganReligion()])
	else:
		return dReligiousGoals[iSecularVictory]


### GOAL CHECKS ###

class HistoricalVictoryCallback(object):

	def stateChange(self, goal):
		if goal.succeeded():
			goal.announceSuccess()
		
			iCount = count(goal.succeeded() for goal in data.players[goal.iPlayer].historicalGoals)
			
			if iCount == 2:
				self.goldenAge(goal.iPlayer)
			elif iCount == 3:
				self.victory(goal.iPlayer)
		
		elif goal.failed():
			goal.announceFailure()
	
	def goldenAge(self, iPlayer):
		data.players[iPlayer].bLaunchHistoricalGoldenAge = True
		
	def victory(self, iPlayer):
		if game.getWinner() == -1:
			game.setWinner(iPlayer, VictoryTypes.VICTORY_HISTORICAL)

class ReligiousVictoryCallback(object):

	def check(self, goal):
		if goal:
			iCount = count(goal for goal in data.players[goal.iPlayer].religiousGoals)
			
			if iCount == 3:
				self.victory(goal.iPlayer)
	
	def victory(self, iPlayer):
		if game.getWinner() == -1:
			game.setWinner(iPlayer, VictoryTypes.VICTORY_RELIGIOUS)

historicalVictoryCallback = HistoricalVictoryCallback()
religiousVictoryCallback = ReligiousVictoryCallback()


### SETUP ###

def createHistoricalGoals(iPlayer):
	goals = [goal.activate(iPlayer, historicalVictoryCallback) for goal in getHistoricalGoals(iPlayer)]
	getScenario().initGoals(iPlayer, goals)
	
	return goals

def createReligiousGoals(iPlayer):
	return [goal.passivate(iPlayer, religiousVictoryCallback) for goal in getReligiousGoals(iPlayer)]

def disable(iPlayer=None):
	if iPlayer is None:
		iPlayer = active()
		
	for goal in data.players[iPlayer].historicalGoals + data.players[iPlayer].religiousGoals:
		goal.deactivate()
	
	data.players[iPlayer].historicalGoals = []
	data.players[iPlayer].religiousGoals = []

def switchReligiousGoals(iPlayer):
	for goal in data.players[iPlayer].religiousGoals:
		goal.deactivate()
	
	data.players[iPlayer].religiousGoals = createReligiousGoals(iPlayer)
	

### GOLDEN AGE ###
	
def goldenAge(iPlayer):
	iGoldenAgeTurns = player(iPlayer).getGoldenAgeLength()
	player(iPlayer).changeGoldenAgeTurns(iGoldenAgeTurns)
	
	message(iPlayer, "TXT_KEY_UHV_INTERMEDIATE", color=iPurple)
	
	if player(iPlayer).isHuman():
		for iOtherPlayer in players.major().alive().without(iPlayer):
			player(iOtherPlayer).AI_changeAttitudeExtra(iPlayer, -2)


#@handler("playerCivAssigned")
def assignGoals(iPlayer):
	if player(iPlayer).isHuman():
		data.players[iPlayer].historicalGoals = createHistoricalGoals(iPlayer)
		data.players[iPlayer].religiousGoals = createReligiousGoals(iPlayer)


#@handler("switch")
def onSwitch(iPrevious, iCurrent):
	for goal in data.players[iPrevious].goals:
		goal.deactivate()

	data.players[iPrevious].historicalGoals = []
	data.players[iPrevious].religiousGoals = []
	
	data.players[iCurrent].historicalGoals = createHistoricalGoals(iCurrent)
	data.players[iCurrent].religiousGoals = createReligiousGoals(iCurrent)


#@handler("civicChanged")
def onCivicChanged(iPlayer, iOldCivic, iNewCivic):
	if iPlayer == active() and infos.civic(iOldCivic).isStateReligion() != infos.civic(iNewCivic).isStateReligion():
		switchReligiousGoals(iPlayer)


#@handler("playerChangeStateReligion")
def onStateReligionChanged(iPlayer):
	if iPlayer == active():
		switchReligiousGoals(iPlayer)


#@handler("EndPlayerTurn")
def checkHistoricalGoldenAge(iGameTurn, iPlayer):
	if data.players[iPlayer].bLaunchHistoricalGoldenAge:
		data.players[iPlayer].bLaunchHistoricalGoldenAge = False
		goldenAge(iPlayer)