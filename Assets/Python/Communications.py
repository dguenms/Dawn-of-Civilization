# Rhye's and Fall of Civilization - Communications

from Core import *
from Events import handler


@handler("BeginGameTurn")
def decayCommunications(iGameTurn):
	iPeriod = getDecayPeriod()
	for iPlayer in players.major().existing().periodic_iter(iPeriod):
		if canDecay(iPlayer):
			decay(iPlayer)


def getDecayPeriod():
	if isAfter(1800):
		return 25
	
	if isAfter(1500):
		return 20
	
	if isBefore(-600):
		return 30
	
	return 15
	


def canDecay(iPlayer):
	if not player(iPlayer).isExisting():
		return False
	
	if turn() < player(iPlayer).getLastBirthTurn() + turns(15):
		return False
	
	if team(iPlayer).isHasTech(iElectricity):
		return False
	
	# Thai UP: can never lose contact
	if civ(iPlayer) == iThailand:
		return False
	
	return True
	
	
def decay(iPlayer):
	contacts = players.major().existing().where(lambda p: canDecay(p) and team(iPlayer).canContact(p) and team(iPlayer).canCutContact(p))
	
	if contacts.count() <= 6:
		return
	
	# master/vassal relationships: keep only masters where contact can be cut with all vassals
	dVassals = vassals()
	contacts = contacts.where(lambda p: all(iVassal in contacts for iVassal in dVassals[p]))
	
	# remove all vassals, vassals where the master contact cannot be cut need to be removed -> other vassals contact will be cut along with their masters
	contacts = contacts.where(lambda p: not team(p).isAVassal())
	
	# choose up to four random contacts to cut
	for iContact in contacts.sample(4):
		ours = players.vassals(iPlayer).including(iPlayer)
		theirs = players.vassals(iContact).including(iContact)
		
		for iTheirPlayer, iOurPlayer in permutations(theirs, ours):
			team(iOurPlayer).cutContact(iTheirPlayer)