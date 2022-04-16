from Core import *

from Events import handler

from datetime import datetime


RISE_LOG = "Rise.log"

TIMER = None


class Timer(object):

	def __init__(self):
		self.start = datetime.now()
	
	def elapsed(self):
		return datetime.now() - self.start
		

def time(func):
	def timed_func(*args, **kwargs):
		timer = Timer()
		func(*args)
		print "Time to run %s: %s" % (signature(func, *args, **kwargs), timer.elapsed())
	
	return timed_func


#@handler("GameStart")
def startTimer():
	global TIMER
	TIMER = Timer()


#@handler("OnLoad")
def restartTimer():
	global TIMER
	TIMER = Timer()
	

#@handler("birth")
def stopTimer(iPlayer):
	message = """AUTOPLAY TIME UNTIL %s: %s
	"""
	rise(message, name(iPlayer).upper(), TIMER.elapsed())


#@handler("BeginGameTurn")
def logSlotInfo():
	current = players.all().alive()
	past_fall = current.where(lambda p: turn() >= year(dFall[p]))
	resurrected = current.where(lambda p: data.civs[p].iResurrections > 0)
	
	message = """### SLOT INFO ###
turn: %d, year: %d
players alive: %d (%s)
players past fall date: %d (%s)
players resurrected: %d (%s)

"""
	
	rise(message, game.getGameTurn(), game.getGameTurnYear(), current.count(), current, past_fall.count(), past_fall, resurrected.count(), resurrected)


def rise(message, *format):
	fileLog(RISE_LOG, str(message % format))