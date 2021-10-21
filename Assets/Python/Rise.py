from Core import *
from Events import events, handler

from Civilizations import *
from RFCUtils import *
from Locations import *
from Stability import completeCollapse
from Popups import popup

import AIParameters, Modifiers, Civilizations, SettlerMaps, WarMaps, Setup
import BugCore

MainOpt = BugCore.game.MainInterface


dClearedForBirth = {
	iIndia: iHarappa, # Harappa should always collapse
	iByzantium: iGreece,
	iItaly: iRome,
	iMexico: iAztecs,
}

dAdvancedStartPoints = CivDict({
}, 0)


def birth(iCiv, iYear=None):
	return Birth(iCiv, iYear=iYear)


def rebirth(iCiv, iYear=None):
	iRebirthPlayer = slot(dRebirthCiv[iCiv])
	return Birth(iCiv, iYear=iYear, iPlayer=iRebirthPlayer)
			

@handler("GameStart")
def initBirths():
	data.births = [birth(civ(p)) for p in players.major()]
	
	for iRebirthCiv, iSlotCiv in dRebirthCiv.items():
		if iSlotCiv in data.dSlots:
			data.births.append(rebirth(iRebirthCiv))


@handler("BeginGameTurn")
def checkBirths():
	for birth in data.births:
		birth.check()


@handler("changeWar")
def ensureAdditionalDefenders(bWar, iAttacker, iDefender):
	if not bWar:
		return
	
	if not player(iDefender).isBirthProtected():
		return
	
	iNumDefenders = 1 + (player(iDefender).getCurrentEra() + 1) / 2
	for city in cities.owner(iDefender).where(lambda city: plot(city).getBirthProtected() == iDefender):
		iDefenseUnit, iDefenseAI = getUnitForRole(iDefender, iDefend)
		defenders = makeUnits(iDefender, iDefenseUnit, city, iNumDefenders, iDefenseAI)
		for defender in defenders:
			mission(defender, MissionTypes.MISSION_FORTIFY)


@handler("changeWar")
def spawnWarUnits(bWar, iAttacker, iDefender):
	if not bWar:
		return
	
	if not player(iDefender).isBirthProtected():
		return
	
	for iRole, iAmount in getAdditionalUnits(iDefender):
		for iUnit, iUnitAI in getUnitsForRole(iDefender, iRole):
			makeUnits(iDefender, iUnit, capital(iDefender), iAmount, iUnitAI)


@handler("changeWar")
def balanceMilitary(bWar, iAttacker, iDefender):
	if not bWar:
		return

	if not player(iDefender).isBirthProtected():
		return
	
	iAttackerPower = player(iAttacker).getPower()
	iDefenderPower = player(iDefender).getPower()
	
	iPowerRatioThreshold = player(iAttacker).isHuman() and 80 or 50
	iPowerRatio = 100 * iDefenderPower / iAttackerPower
	
	if iPowerRatio < iPowerRatioThreshold:
		iPowerRatioDifference = iPowerRatioThreshold - iPowerRatio
		iPowerRequired = iPowerRatioDifference * iAttackerPower / 100
		
		additionalUnits = getAdditionalUnits(iDefender)
		iUnitsPower = sum(infos.unit(iUnit).getPowerValue() * iAmount for iRole, iAmount in additionalUnits for iUnit, _ in getUnitsForRole(iDefender, iRole))
		iAdditionalUnitsRequired = iPowerRequired / iUnitsPower
		
		for iRole, iAmount in additionalUnits:
			for iUnit, iUnitAI in getUnitsForRole(iDefender, iRole):
				makeUnits(iDefender, iUnit, capital(iDefender), iAdditionalUnitsRequired * iAmount, iUnitAI)


@handler("changeWar")
def moveOutAttackers(bWar, iAttacker, iDefender):
	if not bWar:
		return
	
	if not player(iDefender).isBirthProtected():
		return
	
	aroundCities = cities.owner(iDefender).plots().expand(2)
	birthProtected = plots.all().where(lambda p: p.getBirthProtected() == iDefender and not p.isCore(iAttacker))
	for plot in aroundCities.including(birthProtected):
		attackers = units.at(plot).owner(iAttacker)
		if attackers:
			destination = cities.owner(iAttacker).closest(plot)
			for unit in attackers:
				move(unit, destination)
			
			message(iAttacker, "TXT_KEY_MESSAGE_ATTACKERS_EXPELLED", attackers.count(), adjective(iDefender), city(destination).getName(), button=attackers.first().getButton(), location=plot)


class Birth(object):

	def __init__(self, iCiv, iYear=None, iPlayer=None):
		if iYear is None:
			iYear = dBirth[iCiv]
	
		self.iCiv = iCiv
		self.iTurn = year(iYear)
		
		self._iPlayer = iPlayer
		self._area = None
		
		self.location = location(plots.capital(self.iCiv))
		
		self.protectionEnd = None
		self.canceled = False
		
		if self.player.isHuman():
			self.startAutoplay()
	
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
		
	@property
	def flipPopup(self):
		return popup.text("TXT_KEY_POPUP_FLIP").cancel("TXT_KEY_POPUP_FLIP_CANCEL", button='Art/Interface/Buttons/Actions/Join.dds').option(self.declareWarOnFlip, "TXT_KEY_POPUP_FLIP_WAR", button='Art/Interface/Buttons/Actions/Fortify.dds').build()
	
	@property
	def switchPopup(self):
		return popup.text("TXT_KEY_POPUP_SWITCH").cancel("TXT_KEY_POPUP_NO", event_bullet).option(self.switch, "TXT_KEY_POPUP_YES").build()
	
	def determinePlayer(self):
		return slot(self.iCiv)
	
	def startAutoplay(self):
		iAutoplayTurns = self.iTurn - scenarioStartTurn()
		if iAutoplayTurns > 0:
			game.setAIAutoPlay(iAutoplayTurns)
			
	def reset(self):
		# reset AI
		self.player.AI_reset()
		
		# reset diplomatic relations
		self.resetDiplomacy()
		
		# reset player espionage spending
		player().setEspionageSpendingWeightAgainstTeam(self.player.getTeam(), 0)
		
		# reset great people
		self.player.resetGreatPeopleCreated()
		
		# reset visibility
		for plot in plots.all():
			plot.setRevealed(self.player.getID(), False, False, -1)
	
	def resetDiplomacy(self):
		for iOtherPlayer in players.major().without(self.iPlayer):
			self.team.makePeace(player(iOtherPlayer).getTeam())
			
			if self.team.isVassal(player(iOtherPlayer).getTeam()):
				team(iOtherPlayer).freeVassal(self.player.getTeam())
			
			if team(iOtherPlayer).isVassal(self.player.getTeam()):
				self.team.freeVassal(player(iOtherPlayer).getTeam())
				
			self.team.cutContact(player(iOtherPlayer).getTeam())
	
	def updateCivilization(self):
		iCurrentCivilization = self.player.getCivilizationType()
		if self.iCiv == iCurrentCivilization:
			return
		
		self.player.setCivilizationType(self.iCiv)
		del data.dSlots[iCurrentCivilization]
		data.dSlots[self.iCiv] = self.iPlayer
		
		self.updateParameters()
		
	def updateParameters(self):
		AIParameters.updateParameters(self.iPlayer)
		Modifiers.updateModifiers(self.iPlayer)
		Civilizations.initPlayerTechPreferences(self.iPlayer)
		Civilizations.initBuildingPreferences(self.iPlayer)
		SettlerMaps.updateMap(self.iPlayer)
		WarMaps.updateMap(self.iPlayer)
		Setup.updateCore(self.iPlayer)
	
	def assignTechs(self):
		initPlayerTechs(self.iPlayer)
	
	def revealTerritory(self):
		neighbours = self.area.expand(3).owners().major()
		revealed = self.area.land()
		
		for iNeighbour in neighbours:
			neighbourPlots = plots.owner(iNeighbour).area(self.location).land()
			closest = neighbourPlots.closest(self.location)
			furthest = find_max(neighbourPlots.entities(), lambda p: distance(self.location, p)).result
			closePlots, farPlots = neighbourPlots.split(lambda p: distance(closest, p) <= distance(furthest, p))
			revealed += closePlots
			
		iTechGroup = next(iGroup for iGroup in dTechGroups if self.iCiv in dTechGroups[iGroup])
		peers = players.major().alive().where(lambda p: civ(p) in dTechGroups[iTechGroup])
		print "peers are: %s" % (peers,)
		
		def isPeerRevealed(plot):
			iRequiredPeers = plot.isWater() and peers.count() / 2 or peers.count()-1
			return count(peer for peer in peers if plot.isRevealed(player(peer).getTeam(), False)) >= min(iRequiredPeers, peers.count()-1)
		
		if peers.count() > 2:
			shared = plots.all().where(isPeerRevealed)
			print "Peers are: %s, shared: %d" % (peers, shared.count())
			revealed += shared
	
		iVisionRange = self.player.getCurrentEra() / 2 + 1
		for plot in revealed.expand(iVisionRange):
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
		
		# select a settler if available
		if self.player.isHuman():
			settler = units.at(self.location).owner(self.iPlayer).where(lambda unit: unit.isFound()).first()
			if settler:
				interface.selectUnit(settler, True, False, False)
	
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
	
	def advancedStart(self):
		self.player.changeAdvancedStartPoints(dAdvancedStartPoints[self.iPlayer])
	
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
					closest = plots.all().sea().without(self.area).closest(unit)
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
			self.announce()
			
		elif iUntilBirth == 1:
			self.birth()
			self.checkSwitch()
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
				if stability(iMostCitiesPlayer) >= iStabilitySolid:
					return False
		
		return True
	
	def announce(self):
		if game.getAIAutoPlay() > 0:
			return
	
		if plots.owner(active()).closest_distance(self.location) <= 10:
			key = "TXT_KEY_MESSAGE_RISE_%s" % infos.civ(self.iCiv).getIdentifier()
			text = text_if_exists(key, adjective(self.iPlayer), otherwise="TXT_KEY_MESSAGE_RISE_GENERIC")
			message(active(), str(text), location=self.location, color=iRed, button=infos.civ(self.iCiv).getButton())
	
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
		if not self.player.isHuman():
			return
		
		iClearedCiv = dClearedForBirth.get(self.iCiv)
		if iClearedCiv is not None and player(iClearedCiv).isAlive():
			if turn() == year(dFall[iClearedCiv]).deviate(10, data.iSeed):
				completeCollapse(slot(iClearedCiv))
	
	def checkSwitch(self):
		if not self.canSwitch():
			return
		
		self.switchPopup.text(adjective(self.iPlayer)).cancel().switch().launch()
	
	def canSwitch(self):
		if not MainOpt.isSwitchPopup():
			return False
	
		if game.getAIAutoPlay() > 0:
			return False
		
		if civ() in dNeighbours[self.iPlayer] and since(year(dBirth[active()])) < turns(25):
			return False
	
		return True
	
	def switch(self):
		iPreviousPlayer = active()
		iOldHandicap = player(iPreviousPlayer).getHandicapType()
		
		game.setActivePlayer(self.iPlayer, False)
		
		player(iPreviousPlayer).setHandicapType(self.player.getHandicapType())
		self.player.setHandicapType(iOldHandicap)
		
		iMaster = master(self.iPlayer)
		if iMaster:
			self.team.setVassal(iMaster, False, False)
		
		self.player.setPlayable(True)
		
		if game.getWinner() == iPreviousPlayer:
			game.setWinner(-1, -1)
		
		data.resetHumanStability()
		
		for city in cities.owner(self.iPlayer):
			city.setInfoDirty(True)
			city.setLayoutDirty(True)
		
		events.fireEvent("switch", iPreviousPlayer, self.iPlayer)
		
		for iOtherPlayer in players.major():
			self.player.setEspionageSpendingWeightAgainstTeam(player(iOtherPlayer).getTeam(), 0)
	
	def birth(self):
		# reset AI
		self.reset()
		
		# set initial birth turn
		self.player.setInitialBirthTurn(self.iTurn)
		
		# update civilization
		self.updateCivilization()
	
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
		
		# send event
		events.fireEvent("birth", self.iPlayer)
		
	def warOnFlip(self, iOwner, cityNames):
		if player(iOwner).isHuman():
			self.flipPopup.text(cityNames, name(self.iPlayer)).cancel().declareWarOnFlip().launch(iOwner)
			return
		
		if not self.canWarOnFlip(iOwner):
			return
		
		if team(iOwner).isAtWar(self.player.getTeam()):
			team(iOwner).AI_setAtWarCounter(self.player.getTeam(), 0)
			self.team.AI_setAtWarCounter(player(iOwner).getTeam(), 0)
			return
		
		if chance(dWarOnFlipProbability[iOwner]):
			self.declareWarOnFlip(iOwner)
	
	def canWarOnFlip(self, iOwner):
		iOwnerCiv = civ(iOwner)
		
		if iOwnerCiv == iCanada:
			return False
		
		if iOwnerCiv == iGermany and not player(iOwner).isHuman():
			return False
		
		if iOwnerCiv == iByzantium and self.iCiv == iRome:
			return False
		
		return True
	
	def declareWarOnFlip(self, iOwner):
		team(iOwner).declareWar(self.player.getTeam(), False, WarPlanTypes.WARPLAN_ATTACKED_RECENT)
	
	def flip(self):
		flippedPlots = plots.birth(self.iPlayer)
		flippedCities = flippedPlots.cities().notowner(self.iPlayer)
		flippedCityPlots = flippedCities.plots()
		
		flippedPlayerCities = dict((p, format_separators(flippedCities.owner(p), ",", text("TXT_KEY_AND"), CyCity.getName)) for p in flippedCities.owners().major())
		
		expelUnits(self.iPlayer, flippedPlots)
		
		for city in flippedCities:
			city = completeCityFlip(city, self.iPlayer, city.getOwner(), 100, bFlipUnits=True)
			city.rebuild()
			
			if since(scenarioStartTurn()):
				ensureDefenders(self.iPlayer, city, 2)
		
		convertSurroundingPlotCulture(self.iPlayer, flippedPlots)
		
		for iOwner, cityNames in flippedPlayerCities.items():
			self.warOnFlip(iOwner, cityNames)
		
		flipped_names = format_separators(flippedCityPlots.cities(), ",", text("TXT_KEY_AND"), CyCity.getName)
		if flippedCities:
			message(self.iPlayer, 'TXT_KEY_MESSAGE_CITIES_FLIPPED', flipped_names, color=iGreen)
		
		self.advancedStart()