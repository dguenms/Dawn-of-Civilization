from Core import *
from Events import events, handler

from Civilizations import *
from RFCUtils import *


births = []


@handler("BeginGameTurn")
def checkBirths():
	for birth in births:
		birth.check()
			

@handler("GameStart")
def initBirths():
	for iCiv, iYear in dBirth.items():
		births.append(Birth(iCiv, iYear))


class Birth(object):

	def __init__(self, iCiv, iYear):
		self.iCiv = iCiv
		self.iTurn = year(iYear)
		
		self.iPlayer = slot(iCiv)
		
		try:
			self.player = player(self.iPlayer)
			self.team = team(self.player.getTeam())
		except AttributeError, e:
			print "player is none for civ=%d, iPlayer=%d" % (iCiv, self.iPlayer)
			raise e
		
		self.location = plots.capital(self.iPlayer)
	
	def isActive(self):
		return self.iPlayer == active()
	
	def resetAI(self):
		self.player.AI_reset()
	
	def resetDiplomacy(self):
		for iOtherPlayer in players.major().without(self.iPlayer):
			self.team.makePeace(player(iOtherPlayer).getTeam())
			
			if self.team.isVassal(player(iOtherPlayer).getTeam()):
				team(iOtherPlayer).freeVassal(self.player.getTeam())
			
			if team(iOtherPlayer).isVassal(self.player.getTeam()):
				self.team.freeVassal(player(iOtherPlayer).getTeam())
	
	def assignTechs(self):
		initPlayerTechs(self.iPlayer)
	
	def createUnits(self):
		iNumSettlers = getStartingSettlers(self.iPlayer)
		if iNumSettlers > 0:
			createSettlers(self.iPlayer, iNumSettlers)
		
		iNumMissionaries = getStartingMissionaries(self.iPlayer)
		if iNumMissionaries > 0:
			createMissionaries(self.iPlayer, iNumMissionaries)
		
		landLocation = self.location
		seaLocation = plots.ring(landLocation).sea().random() or plots.ring(landLocation, radius=2).sea().random()
		
		# this lacks starting experience
		for iRole, iAmount in getStartingUnits(self.iPlayer):
			tile = getRoleDomain(iRole) == DomainTypes.DOMAIN_SEA and seaLocation or landLocation
			for iUnit, iUnitAI in getUnitsForRole(self.iPlayer, iRole):
				try:
					makeUnits(self.iPlayer, iUnit, tile, iAmount, iUnitAI)
				except:
					raise Exception("Cannot create iUnit=%s, iPlayer=%s, iRole=%s" % (iUnit, self.iPlayer, iRole))
	
	def flipCapital(self):
		pass
	
	def resetPlague(self):
		data.players[self.iPlayer].iPlagueCountdown = -10
		clearPlague(self.iPlayer)
	
	def check(self):
		iUntilBirth = until(self.iTurn)
		
		print "check player %s at turn %d and year %d birth at %d" % (name(self.iPlayer), turn(), game.getGameTurnYear(), self.iTurn)
		
		if iUntilBirth == 1:
			print "birth"
			self.birth()
	
	def birth(self):
		# reset AI
		self.resetAI()
	
		# reset diplomacy
		self.resetDiplomacy()
	
		# assign techs
		self.assignTechs()
		
		# flip capital
		self.flipCapital()
		
		# create starting units
		self.createUnits()
		
		# reset plague
		self.resetPlague()
		