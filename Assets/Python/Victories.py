from Core import *

from StoredData import data
from Events import handler


### DELAYED IMPORT ###

dHistoricalGoals = None
dReligiousGoals = None
dPaganGoals = None

@handler("xmlLoaded")
def onXmlLoaded():
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
		return concat(dReligiousGoals[iPaganVictory], dPaganGoals[player(iPlayer).getPaganReligion()])
	else:
		return dReligiousGoals[iSecularVictory]


### GOAL CHECKS ###

class HistoricalVictoryCallback(object):

	def check(self, goal):
		if goal.succeeded():
			iCount = count(goal.succeeded() for goal in data.players[goal.iPlayer].historicalGoals)
			show("historical victory checked: we have %d", iCount)

class ReligiousVictoryCallback(object):

	def check(self, goal):
		if goal:
			iCount = count(goal for goal in data.players[goal.iPlayer].religiousGoals)
			show("religious victory checked: we have %d", iCount)

historicalVictoryCallback = HistoricalVictoryCallback()
religiousVictoryCallback = ReligiousVictoryCallback()


@handler("GameStart")
def setup():
	historicalGoals = getHistoricalGoals(active())
	religiousGoals = getReligiousGoals(active())
	
	data.players[active()].historicalGoals = historicalGoals
	data.players[active()].religiousGoals = religiousGoals
	
	for goal in historicalGoals:
		goal.activate(active(), historicalVictoryCallback)
	
	for goal in religiousGoals:
		goal.passivate(active(), religiousVictoryCallback)
