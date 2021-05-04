from Core import *

from StoredData import data
from Events import handler

import cPickle as pickle


def test_pickle(iPlayer):
	for goal in data.players[iPlayer].historicalGoals:
		print "pickle goal: %s" % goal.description()
		pickle_object(goal)
		
def pickle_object(obj):
	for key, value in obj.__dict__.iteritems():
		print "pickle %s (%s)" % (key, type(value))
		pickle.dumps(value)


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
		iCount = count(goal.succeeded() for goal in data.players[goal.iPlayer].historicalGoals)
		
		show("historical victory checked: we have %d", iCount)

historicalVictoryCallback = HistoricalVictoryCallback()


@handler("GameStart")
def setup():
	data.players[active()].historicalGoals = getHistoricalGoals()[civ()]
	
	for goal in data.players[active()].historicalGoals:
		goal.activate(active(), historicalVictoryCallback)