# Rhye's and Fall of Civilization - Communications

from Core import *
from Events import handler


@handler("BeginGameTurn")
def decayCommunications(iGameTurn):
	if iGameTurn < year(-600):
		iPeriod = 30
	elif iGameTurn < year(600):
		iPeriod = 18
	else:
		iPeriod = 12
		
	for iPlayer in players.major().existing().periodic_iter(iPeriod):
		if canDecay(iGameTurn, iPlayer):
			decay(iPlayer)


def canDecay(iGameTurn, iPlayer):
	if not player(iPlayer).isExisting():
		return False
	
	if iGameTurn < player(iPlayer).getLastBirthTurn() + turns(15):
		return False
	
	if team(iPlayer).isHasTech(iElectricity):
		return False
	
	return True
	
	
def decay(iPlayer):
	contacts = players.major().existing().where(lambda p: team(iPlayer).canContact(p) and team(iPlayer).canCutContact(p))
	
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