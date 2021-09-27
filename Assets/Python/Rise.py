from Core import *
from Events import events, handler

from Civilizations import *
from RFCUtils import *


def birth(iCiv, iYear=None):
	return Birth(iCiv, iYear)


@handler("BeginGameTurn")
def checkBirths():
	for birth in data.births:
		birth.check()
			

@handler("GameStart")
def initBirths():
	data.births = [
		birth(iEgypt),
		birth(iBabylonia),
		birth(iHarappa),
		birth(iChina),
		birth(iGreece),
		birth(iIndia),
		birth(iPhoenicia),
		birth(iPolynesia),
		birth(iPersia),
		birth(iRome),
		birth(iMaya),
		birth(iTamils),
		birth(iEthiopia),
		birth(iKorea),
		birth(iByzantium),
		birth(iJapan),
		birth(iVikings),
		birth(iTurks),
		birth(iArabia),
		birth(iTibet),
		birth(iIndonesia),
		birth(iMoors),
		birth(iSpain),
		birth(iFrance),
		birth(iKhmer),
		birth(iEngland),
		birth(iHolyRome),
		birth(iRussia),
		birth(iMali),
		birth(iPoland),
		birth(iPortugal),
		birth(iInca),
		birth(iItaly),
		birth(iMongols),
		birth(iAztecs),
		birth(iMughals),
		birth(iOttomans),
		birth(iThailand),
		birth(iCongo),
		birth(iNetherlands),
		birth(iGermany),
		birth(iAmerica),
		birth(iArgentina),
		birth(iBrazil),
		birth(iCanada),
	]


class Birth(object):

	def __init__(self, iCiv, iYear=None):
		if iYear is None:
			iYear = dBirth[iCiv]
	
		self.iCiv = iCiv
		self.iTurn = year(iYear)
		
		self._iPlayer = None
		self._area = None
		
		self.location = location(plots.capital(self.iCiv))
		
		self.protectionEnd = None
		self.canceled = False
	
	@property
	def iPlayer(self):
		if self._iPlayer is None:
			self._iPlayer = self.determinePlayer()
		return self._iPlayer
	
	@property
	def player(self):
		return player(self.iPlayer)
	
	@property
	def team(self):
		return team(self.player.getTeam())
	
	@property
	def area(self):
		if self._area is None:
			self._area = plots.core(self.iPlayer) + plots.birth(self.iPlayer)
			self._area = self._area.unique()
		return self._area
	
	def determinePlayer(self):
		return slot(self.iCiv)
	
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
		iVisionRange = self.player.getCurrentEra() / 2 + 1
		area = plots.core(self.iPlayer) + plots.birth(self.iPlayer)
		for plot in area.unique().land().expand(iVisionRange):
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
				makeUnits(self.iPlayer, iUnit, tile, iAmount, iUnitAI)
	
	def prepareCapital(self):
		"""Maybe preserve wonders in erased cities?"""
		
		if plot_(self.location).isCity():
			completeCityFlip(self.location, self.iPlayer, city_(self.location).getOwner(), 100, bFlipUnits=True)
		
		for city in cities.ring(self.location):
			if city.isHolyCity():
				completeCityFlip(city, self.iPlayer, city.getOwner(), 100, bFlipUnits=True)
			else:
				plot_(city).eraseAIDevelopment()
		
		for plot in plots.surrounding(self.location):
			convertPlotCulture(plot, self.iPlayer, 100, bOwner=True)
	
	def resetPlague(self):
		data.players[self.iPlayer].iPlagueCountdown = -10
		clearPlague(self.iPlayer)
	
	def removeMinors(self):
		cities = self.area.cities()
		edge = self.area.expand(1).edge().where_surrounding(lambda p: not p.isCity())
		
		for unit in self.area.units().minor():
			if cities.owner(unit):
				closest = cities.owner(unit).closest(unit)
			elif unit.getDomainType() == DomainTypes.DOMAIN_SEA or unit.isCargo():
				if edge.sea():
					closest = edge.sea().closest(unit)
				else:
					closest = plots.all().without(self.area).closest(unit)
			else:
				closest = edge.land().closest(unit)
			
			if closest:
				move(unit, closest)
			else:
				unit.kill(False, -1)
	
	def check(self):
		if self.canceled:
			return
	
		iUntilBirth = until(self.iTurn)
		
		if iUntilBirth == turns(5):
			if not self.canSpawn():
				self.canceled = True
				return
			
			self.protect()
		elif iUntilBirth == 1:
			self.birth()
		elif iUntilBirth == 0:
			self.flip()
			
		if turn() == self.protectionEnd:
			self.resetProtection()
		
		self.checkIncompatibleCivs()
		
	def canSpawn(self):
		if self.player.isHuman():
			return True
			
		# Polynesia cannot spawn as AI
		if self.iCiv == iPolynesia:
			return False
	
		# Byzantium requires Rome to be alive and Greece to be dead (human Rome can avoid Byzantine spawn by being solid)
		if self.iCiv == iByzantium:
			if not player(iRome).isAlive():
				return False
			elif player(iGreece).isAlive():
				return False
			elif player(iRome).isHuman() and stability(slot(iRome)) == iStabilitySolid:
				return False
		
		# Italy requires Rome to be dead
		if self.iCiv == iItaly:
			if player(iRome).isAlive():
				return False
		
		# Ottomans require that the Turks managed to conquer at least one city in the Near East
		if self.iCiv == iOttomans:
			if cities.rectangle(*tNearEast).none(lambda city: slot(iTurks) in [city.getOwner(), city.getPreviousOwner()]):
				return False
		
		# Thailand requires Khmer to be shaky or worse (unstable if Khmer is human)
		if self.iCiv == iThailand:
			iRequiredStability = player(iKhmer).isHuman() and iStabilityShaky or iStabilityStable
			if stability(slot(iKhmer)) >= iRequiredStability:
				return False
	
		# Argentina and Brazil require the player controlling the most cities in their area to be stable or worse
		if self.iCiv in [iArgentina, iBrazil]:
			numCities = lambda p: self.area.cities().owner(p).count()
			iMostCitiesPlayer = players.major().without(self.iPlayer).where(lambda p: numCities(p) > 0).maximum(numCities)
			if iMostCitiesPlayer is not None:
				if stability(iMostCitiesPlayer) >= iSolid:
					return False
		
		return True
	
	def protect(self):
		self.protectionEnd = turn() + turns(10)
		self.player.setBirthProtected(True)
		
		for plot in self.area:
			plot.setBirthProtected(self.iPlayer)
		
		self.removeMinors()
	
	def resetProtection(self):
		self.player.setBirthProtected(False)
		
		for plot in self.area:
			plot.resetBirthProtected()
	
	def checkIncompatibleCivs(self):
		pass
	
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
		flippedPlots = plots.birth(self.iPlayer)
		flippedCities = flippedPlots.cities().notowner(self.iPlayer)
		
		enemies = flippedCities.owners().major()
		flipped_names = format_separators(flippedCities, ",", text("TXT_KEY_AND"), CyCity.getName)
		
		for city in flippedCities:
			completeCityFlip(city, self.iPlayer, city.getOwner(), 100, bFlipUnits=True)
			
			if since(scenarioStartTurn()):
				ensureDefenders(self.iPlayer, city, 2)
		
		convertSurroundingPlotCulture(self.iPlayer, flippedPlots)
				
		for iEnemy in enemies:
			self.warOnFlip(iEnemy)
		
		if flippedCities:
			message(self.iPlayer, 'TXT_KEY_MESSAGE_CITIES_FLIPPED', flipped_names, color=iGreen)
			
		
		