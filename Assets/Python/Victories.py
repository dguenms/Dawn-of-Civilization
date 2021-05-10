from Core import *

from StoredData import data
from Events import handler


### DELAYED IMPORT ###

dHistoricalGoals = None
dReligiousGoals = None

def getHistoricalGoals():
	global dHistoricalGoals
	if dHistoricalGoals is None:
		from HistoricalVictory import dGoals
		dHistoricalGoals = dGoals
	return dHistoricalGoals

def getReligiousGoals():
	global dReligiousGoals
	if dReligiousGoals is None:
		from ReligiousVictory import dGoals
		dReligiousGoals = dGoals
	return dReligiousGoals


### GOAL CHECKS ###

class HistoricalVictoryCallback(object):

	def __call__(self, goal):
		if goal.succeeded():
			iCount = count(goal.succeeded() for goal in data.players[goal.iPlayer].historicalGoals)
			show("historical victory checked: we have %d", iCount)

historicalVictoryCallback = HistoricalVictoryCallback()


@handler("GameStart")
def setup():
	data.players[active()].historicalGoals = getHistoricalGoals()[civ()]
	
	for goal in data.players[active()].historicalGoals:
		goal.activate(active(), historicalVictoryCallback)