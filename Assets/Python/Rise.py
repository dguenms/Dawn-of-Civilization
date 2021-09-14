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
	
	def revealTerritory(self):
		for plot in plots.core(self.iPlayer).land().expand(1):
			plot.setRevealed(self.team.getID(), True, False, -1)
	
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
	
	def prepareCapital(self):
		"""Maybe preserve wonders in erased cities?"""
	
		if plot_(self.location).isCity():
			completeCityFlip(self.location, self.iPlayer, city(self.location).getOwner(), 100, bFlipUnits=True)
		
		for city in cities.surrounding(self.location):
			if city.isHolyCity():
				completeCityFlip(city, self.iPlayer, city.getOwner(), 100, bFlipUnits=True)
			else:
				plot_(city).eraseAIDevelopment()
		
		for plot in plots.surrounding(self.location):
			convertPlotCulture(plot, self.iPlayer, 100, bOwner=True)
	
	def resetPlague(self):
		data.players[self.iPlayer].iPlagueCountdown = -10
		clearPlague(self.iPlayer)
	
	def check(self):
		iUntilBirth = until(self.iTurn)
		
		print "check player %s at turn %d and year %d birth at %d" % (name(self.iPlayer), turn(), game.getGameTurnYear(), self.iTurn)
		
		if iUntilBirth == 1:
			print "birth"
			self.birth()
		elif iUntilBirth == 0:
			self.flip()
	
	def birth(self):
		# reset AI
		self.resetAI()
	
		# reset diplomacy
		self.resetDiplomacy()
	
		# assign techs
		self.assignTechs()
		
		# reveal territory
		self.revealTerritory()
		
		# flip capital
		self.prepareCapital()
		
		# create starting units
		self.createUnits()
		
		# reset plague
		self.resetPlague()
		
	def warOnFlip(self, iEnemy):
		# let's think about how this should work and keep it turned off for now
		return
	
	def flip(self):
		print "flip for %s" % name(self.iPlayer)
		humanCities, aiCities = cities.birth(self.iPlayer).split(CyCity.isHuman)
		
		for city in aiCities:
			completeCityFlip(city, self.iPlayer, city.getOwner(), 100, bFlipUnits=True)
			
			if since(scenarioStartTurn()):
				ensureDefenders(self.iPlayer, city, 2)
		
		for iEnemy in aiCities.owners().major():
			self.warOnFlip(iEnemy)
		
		if aiCities:
			message(self.iPlayer, 'TXT_KEY_MESSAGE_CITIES_FLIPPED', format_separators(aiCities, ",", text("TXT_KEY_AND"), CyCity.getName), color=iGreen)
			
		
		