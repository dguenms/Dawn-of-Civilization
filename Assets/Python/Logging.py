from Core import *

from Events import handler

from datetime import timedelta


RISE_LOG = "Rise.log"
TECH_LOG = "Tech.log"
RELATIONS_LOG = "Relations.log"

TIMER = None
TECHS = None


class Timer(object):

	def __init__(self):
		self.start = game.getSecondsPlayed()
	
	def elapsed(self):
		return timedelta(seconds=game.getSecondsPlayed() - self.start)


class TechLog(object):

	GROUP_NAMES = {
		iCivGroupEurope: "Europe",
		iCivGroupAsia: "Asia",
		iCivGroupMiddleEast: "Middle East", 
		iCivGroupAfrica: "Africa",
		iCivGroupAmerica: "America",
	}

	def __init__(self):
		self.first_discovered = {}
		self.first_discovered_group = dict((iGroup, {}) for iGroup in dCivGroups.keys())
		
		self.first_column = {}
		self.first_column_group = dict((iGroup, {}) for iGroup in dCivGroups.keys())
		
		self.techs_received = appenddict()
	
	def update(self, iTech, iTeam, iCiv):
		iColumn = infos.tech(iTech).getGridX()
		iGroup = next(iGroup for iGroup, lCivs in dCivGroups.items() if iCiv in lCivs)
		iTurn = game.getGameTurn()
		iYear = game.getGameTurnYear()
		
		if iGroup is None:
			return
		
		column_techs = [iColumnTech for iColumnTech in infos.techs() if infos.tech(iColumnTech).getGridX() == iColumn]
		
		tech_name = infos.tech(iTech).getText()
		civ_name = infos.civ(iCiv).getShortDescription(0)
		group_name = self.GROUP_NAMES.get(iGroup)
		
		if iTech not in self.first_discovered:
			self.first_discovered[iTech] = (iCiv, iTurn)
			
			tech("FIRST TECH:\n  %s by %s in %d (turn %d)\n", tech_name, civ_name, iYear, iTurn)
		
			if iTech not in self.first_discovered_group[iGroup]:
				self.first_discovered_group[iGroup][iTech] = (iCiv, iTurn)
				
				tech("FIRST GROUP %s:\n  %s by %s in %d (turn %d)\n", group_name, tech_name, civ_name, iYear, iTurn)
			
		if all(team(iTeam).isHasTech(iColumnTech) for iColumnTech in column_techs):
			if iColumn not in self.first_column:
				self.first_column[iColumn] = (iCiv, iTurn)
				
				tech("FIRST COMPLETE:\n  column %d by %s in %d (turn %d)\n", iColumn, civ_name, iYear, iTurn)
		
			if iColumn not in self.first_column_group[iGroup]:
				self.first_column_group[iGroup][iColumn] = (iCiv, iTurn)
				
				tech("FIRST COMPLETE GROUP %s:\n  column %d by %s in %d (turn %d)\n", group_name, iColumn, civ_name, iYear, iTurn)
	
	def update_trade(self, iFrom, iTo, iTech):
		if is_minor(iTo):
			return
	
		iFromCiv = civ(iFrom)
		iToCiv = civ(iTo)
		
		self.techs_received[iToCiv].append(iTech)
		
		tech("TECH RECEIVED:\n  %s for %s from %s in %d (turn %d)\n  Total %d: %s", infos.tech(iTech).getText(), infos.civ(iToCiv).getShortDescription(0), infos.civ(iFromCiv).getShortDescription(0), game.getGameTurnYear(), game.getGameTurn(), len(self.techs_received[iToCiv]), [infos.tech(iTech).getText() for iTech in self.techs_received[iToCiv]])
		

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
	

#@handler("GameStart")
def start_tech_log():
	global TECHS
	TECHS = TechLog()


#@handler("OnLoad")
def restart_tech_log():
	global TECHS
	TECHS = TechLog()


#@handler("techAcquired")
def log_tech_progress(iTech, iTeam, iPlayer):
	if TECHS:
		TECHS.update(iTech, iTeam, civ(iPlayer))


#@handler("techTraded")
def log_tech_trade(iFrom, iTo, iTech):
	if TECHS:
		TECHS.update_trade(iFrom, iTo, iTech)


#@handler("BeginGameTurn")
def log_relations(iGameTurn):
	if iGameTurn % 25 == 0:
		relations("LOG RELATIONS IN %s (TURN %d)", game.getGameTurnYear(), game.getGameTurn())
	
		for iPlayer in players.major().alive():
			contacts = players.major().alive().without(iPlayer).where(lambda p: player(iPlayer).canContact(p))
			contact_relations = contacts.grouped(lambda p: player(p).AI_getAttitude(iPlayer))
			
			relations_info = "\n".join(["  * %s" % format_attitude_info(dict(contact_relations), iAttitude) for iAttitude in range(AttitudeTypes.NUM_ATTITUDE_TYPES)])
			
			message = """RELATIONS FOR: %s
%s

"""

			relations(message, name(iPlayer), relations_info)


#@handler("BeginGameTurn")
def log_attitude_factors(iGameTurn):
	if iGameTurn % 25 == 0:
		relations("LOG ATTITUDE FACTORS IN %s (TURN %d)", game.getGameTurnYear(), game.getGameTurn())
		
		for iPlayer, iOtherPlayer in players.major().alive().permutations():
			if player(iPlayer).canContact(iOtherPlayer):
				relations("%s ATTITUDE TOWARDS %s\n%s\n", name(iPlayer), name(iOtherPlayer), CyGameTextMgr().getAttitudeString(iPlayer, iOtherPlayer))


def format_attitude_info(relations, iAttitude):
	attitude_relations = relations.get(iAttitude, players.none())
	return "%s: %d (%s)" % (infos.attitude(iAttitude).getText(), len(attitude_relations), str(attitude_relations))


def log(file, message, *format):
	fileLog(file, str(message % format))


def rise(message, *format):
	log(RISE_LOG, message, *format)


def tech(message, *format):
	log(TECH_LOG, message, *format)


def relations(message, *format):
	log(RELATIONS_LOG, message, *format)
