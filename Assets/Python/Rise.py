from Core import *
from Events import events, handler

from Civilizations import *
from RFCUtils import *
from Locations import *
from Scenarios import *
from Stability import completeCollapse
from Popups import popup

import BugCore
import CvScreensInterface

MainOpt = BugCore.game.MainInterface


lIndependenceCivs = [
	iByzantium,
	iAmerica,
	iArgentina,
	iMexico,
	iColombia,
	iBrazil,
	iCanada
]

dClearedForBirth = {
	iIndia: iHarappa,
	iByzantium: iGreece,
	iItaly: iRome,
	iMexico: iAztecs,
}

lAlwaysClear = [
	iHarappa,
]

dAdvancedStartPoints = CivDict({
	iPhoenicia: 50,
	iPersia: 100,
	iRome: 150,
	iTamils: 50,
	iByzantium: 100,
	iIndonesia: 50,
	iMoors: 100,
	iSpain: 50,
	iFrance: 50,
	iKhmer: 50,
	iEngland: 50,
	iHolyRome: 50,
	iMali: 50,
	iPortugal: 50,
	iItaly: 250,
	iMongols: 50,
	iOttomans: 200,
	iIran: 250,
	iNetherlands: 300,
	iGermany: 250,
	iAmerica: 500,
	iArgentina: 100,
	iMexico: 100,
	iColombia: 150,
	iBrazil: 200,
	iCanada: 250,
}, 0)

dStartingReligion = {
	iIran: iIslam,
}

dStartingGold = {
	iIran: 600,
	iMexico: 500,
	iColombia: 750,
}

dStartingCivics = {
	iIran: [
		iMonarchy,
		iVassalage,
		iSlavery,
		iMerchantTrade,
		iTheocracy,
	],
	iMexico: [
		iDespotism,
		iConstitution,
		iIndividualism,
		iRegulatedTrade,
		iClergy,
		iNationhood,
	],
	iColombia: [
		iDespotism,
		iConstitution,
		iIndividualism,
		iRegulatedTrade,
		iClergy,
		iNationhood,
	],
}


def birth(iCiv, iYear=None):
	return Birth(iCiv, iYear=iYear)


def rebirth(iCiv, iYear=None):
	return Birth(iCiv, iYear=iYear, bRebirth=True)


### Event Handlers ###


@handler("BeginGameTurn")
def showDawnOfMan(iGameTurn):
	if iGameTurn == scenarioStartTurn() and game.getAIAutoPlay() > 0 and data.iBeforeObserverSlot == -1:
		CvScreensInterface.dawnOfMan.interfaceScreen()
			

@handler("GameStart")
def initBirths():
	data.births = [birth(iCiv) for iCiv in lBirthOrder]
	
	for iRebirthCiv, iSlotCiv in dRebirthCiv.items():
		if iSlotCiv in data.dSlots:
			data.births.append(rebirth(iRebirthCiv))
	
	for born in data.births:
		print "check birth: %s" % born.name
		born.check()


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
		defenders = ensureDefenders(iDefender, city, iNumDefenders)
		for defender in defenders:
			mission(defender, MissionTypes.MISSION_FORTIFY)


@handler("changeWar")
def spawnWarUnits(bWar, iAttacker, iDefender):
	if not bWar:
		return
	
	if not player(iDefender).isBirthProtected():
		return
		
	if team(iAttacker).isAVassal():
		return
		
	city = capital(iDefender)
	
	if city:
		createRoleUnits(iDefender, city, getAdditionalUnits(iDefender))
		createSpecificAdditionalUnits(iDefender, city)


@handler("changeWar")
def balanceMilitary(bWar, iAttacker, iDefender):
	if not bWar:
		return

	if not player(iDefender).isBirthProtected():
		return
	
	iAttackerPower = player(iAttacker).getPower()
	iDefenderPower = player(iDefender).getPower()
	
	if not iAttackerPower:
		return
	
	iPowerRatioThreshold = player(iAttacker).isHuman() and 80 or 50
	iPowerRatio = 100 * iDefenderPower / iAttackerPower
	
	if iPowerRatio < iPowerRatioThreshold:
		iPowerRatioDifference = iPowerRatioThreshold - iPowerRatio
		iPowerRequired = iPowerRatioDifference * iAttackerPower / 100
		
		additionalUnits = getAdditionalUnits(iDefender)
		iUnitsPower = sum(infos.unit(iUnit).getPowerValue() * iAmount for iRole, iAmount in additionalUnits for iUnit, _ in getUnitsForRole(iDefender, iRole))
		iAdditionalUnitsRequired = iPowerRequired / iUnitsPower
		
		for _ in range(iAdditionalUnitsRequired):
			createRoleUnits(iDefender, capital(iDefender), additionalUnits)
			createSpecificAdditionalUnits(iDefender, capital(iDefender))


@handler("changeWar")
def moveOutAttackers(bWar, iAttacker, iDefender):
	if not bWar:
		return
	
	if not player(iDefender).isBirthProtected():
		return
	
	aroundCities = cities.owner(iDefender).plots().expand(2)
	birthProtected = plots.all().where(lambda p: p.getBirthProtected() == iDefender and not p.isPlayerCore(iAttacker))
	for plot in aroundCities.including(birthProtected):
		attackers = units.at(plot).owner(iAttacker)
		if attackers:
			destination = cities.owner(iAttacker).closest(plot)
			for unit in attackers:
				if destination:
					move(unit, destination)
				else:
					unit.kill(-1, False)
			
			if destination:
				message(iAttacker, "TXT_KEY_MESSAGE_ATTACKERS_EXPELLED", attackers.count(), adjective(iDefender), city(destination).getName(), button=attackers.first().getButton(), location=plot)


@handler("changeWar")
def createExpansionUnits(bWar, iAttacker, iDefender):
	if not bWar:
		return
	
	expansionCities = cities.owner(iDefender).where(lambda city: plot(city).getExpansion() == iAttacker)
	ourCities = cities.owner(iAttacker)
	if expansionCities and ourCities:
		target = expansionCities.closest_all(ourCities)
		
		iDistance = player(iDefender).isHuman() and 3 or 2
		spawn = plots.ring(target, radius=iDistance).land().passable().closest_all(ourCities)
		
		iExtra = active() in [iAttacker, iDefender] and 1 or 0
		dExpansionUnits = {
			iAttack: 2 + iExtra,
			iSiege: 1 + 2*iExtra,
		}
		for _ in range(expansionCities.count()):
			createRoleUnits(iAttacker, spawn, dExpansionUnits.items())


@handler("firstCity")
def createStartingWorkers(city):
	iPlayer = city.getOwner()
	iNumStartingWorkers = dStartingUnits[iPlayer].get(iWork, 0)
	
	if iNumStartingWorkers > 0:
		createRoleUnit(iPlayer, city, iWork, iNumStartingWorkers)


@handler("firstCity")
def restorePreservedWonders(city):
	while data.players[city.getOwner()].lPreservedWonders:
		iWonder = data.players[city.getOwner()].lPreservedWonders.pop(0)
		if city.isValidBuildingLocation(iWonder):
			city.setHasRealBuilding(iWonder, True)


@handler("BeginGameTurn")
def fragmentIndependents():
	if year() >= year(50) and periodic(15):
		iLargestMinor = players.independent().maximum(lambda p: player(p).getNumCities())
		iSmallestMinor = players.independent().minimum(lambda p: player(p).getNumCities())
		if player(iLargestMinor).getNumCities() > 2 * player(iSmallestMinor).getNumCities():
			for city in cities.owner(iLargestMinor).sample(3):
				completeCityFlip(city, iLargestMinor, iSmallestMinor, 50, False, True, True, True)


@handler("BeginGameTurn")
def checkMinorTechs():
	iMinor = players.independent().alive().periodic(20)
	if iMinor:
		updateMinorTechs(iMinor, barbarian())


class Birth(object):

	def __init__(self, iCiv, iYear=None, bRebirth=False):
		if iYear is None:
			iYear = dBirth[iCiv]
	
		self.iCiv = iCiv
		self.iTurn = year(iYear)
		self.bRebirth = bRebirth
		
		self.iPlayer = None
		self.area = None
		
		#if not bRebirth:
		#	self.iPlayer = slot(self.iCiv)
		
		self.location = location(plots.capital(self.iCiv))
		
		self.protectionEnd = None
		self.canceled = until(self.iTurn) < 0
		
		self.iExpansionDelay = 0
		self.iExpansionTurns = 0
		
		if self.isHuman():
			self.startAutoplay()
	
	@property
	def player(self):
		if self.iPlayer is None:
			return None
		return player(self.iPlayer)
	
	@property
	def team(self):
		if self.iPlayer is None:
			return None
		return team(self.player.getTeam())
	
	@property
	def name(self):
		if self.iPlayer is None:
			return "Unassigned civ: %s" % infos.civ(self.iCiv).getText()
		return name(self.iPlayer)
		
	@property
	def flipPopup(self):
		return popup.text("TXT_KEY_POPUP_FLIP").cancel("TXT_KEY_POPUP_FLIP_CANCEL", button='Art/Interface/Buttons/Actions/Join.dds').option(self.declareWarOnFlip, "TXT_KEY_POPUP_FLIP_WAR", button='Art/Interface/Buttons/Actions/Fortify.dds').build()
	
	@property
	def switchPopup(self):
		return popup.text("TXT_KEY_POPUP_SWITCH").cancel("TXT_KEY_POPUP_NO", event_bullet).option(self.switch, "TXT_KEY_POPUP_YES").build()
	
	def isHuman(self):
		if self.iPlayer is None:
			return game.getActiveCivilizationType() == self.iCiv
		return self.player.isHuman()
	
	def isIndependence(self):
		return self.iCiv in lIndependenceCivs
	
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
	
	def resetDiplomacy(self):
		for iOtherPlayer in players.major().without(self.iPlayer):
			self.team.makePeace(player(iOtherPlayer).getTeam())
			
			if self.team.isVassal(player(iOtherPlayer).getTeam()):
				team(iOtherPlayer).freeVassal(self.player.getTeam())
			
			if team(iOtherPlayer).isVassal(self.player.getTeam()):
				self.team.freeVassal(player(iOtherPlayer).getTeam())
				
			self.team.cutContact(player(iOtherPlayer).getTeam())
	
	def updateCivilization(self):
		data.dSlots[self.iCiv] = self.iPlayer
		
		iCurrentCivilization = self.player.getCivilizationType()
		if self.iCiv == iCurrentCivilization:
			return
		
		if iCurrentCivilization == -1:
			addPlayer(self.iCiv)
		else:
			self.player.setCivilizationType(self.iCiv)
		
		if iCurrentCivilization in data.dSlots:
			del data.dSlots[iCurrentCivilization]
	
	def updateStartingLocation(self):
		startingPlot = plots.capital(self.iCiv)
		self.player.setStartingPlot(startingPlot, False)
		
	def updateArea(self):
		if self.isIndependence():
			baseCities = self.iCiv == iByzantium and cities.all() or self.area.cities()
			owners = self.area.cities().owners().major()
			ownerCities = baseCities.area(self.location).where(lambda city: city.getOwner() in owners)
			closerCities = ownerCities.where(lambda city: real_distance(city, self.location) <= real_distance(city, capital(city)) and real_distance(city, self.location) <= 12)
			
			additionalPlots = closerCities.plots().expand(2).where(lambda p: p.getOwner() in owners and none(p.isPlayerCore(iPlayer) for iPlayer in players.major().alive().without(self.iPlayer)))
			
			self.area += additionalPlots
			self.area = self.area.unique()
		
		if self.iCiv == iChina and scenario() == i600AD:
			self.area += plots.region(rChina)
			self.area = self.area.unique()
		
		if self.iCiv == iMexico:
			self.area = self.area.where(lambda p: p.isPlayerCore(self.iPlayer) or not owner(p, iAmerica))
		
		if self.iCiv == iCanada:
			self.area += cities.region(rCanada).where(lambda city: civ(city) in [iFrance, iEngland, iAmerica]).plots().expand(2)
			self.area = self.area.unique()
		
		self.excludeForeignCapitals()
			
	def excludeForeignCapitals(self):
		areaCapitals = self.area.cities().where(CyCity.isCapital).where(lambda city: city.atPlot(plots.capital(city.getOwner())))
		excludedPlots = areaCapitals.plots().expand(1).where_surrounding(lambda p: p in areaCapitals or p not in self.area or not p.isCity())
	
		self.area = self.area.without(excludedPlots)
	
		for plot in plots.all():
			if plot in self.area:
				plot.setBirthProtected(self.iPlayer)
			elif plot.getBirthProtected() == self.iPlayer:
				plot.resetBirthProtected()
				
	def assignGold(self):
		if self.iCiv in dStartingGold:
			self.player.setGold(dStartingGold[self.iCiv])
	
	def assignTechs(self):
		initPlayerTechs(self.iPlayer)
	
	def assignStateReligion(self):
		if self.iCiv in dStartingReligion:
			self.player.setLastStateReligion(dStartingReligion[self.iCiv])
	
		elif self.isIndependence():
			iPrevalentReligion = getPrevalentReligion(self.area, self.iPlayer)
			if iPrevalentReligion >= 0:
				self.player.setLastStateReligion(iPrevalentReligion)
	
	def assignCivics(self):
		for iCivic in dStartingCivics.get(self.iCiv, []):
			self.player.setCivics(infos.civic(iCivic).getCivicOptionType(), iCivic)
		
		# allow free civic changes in the birth and spawn turn
		self.player.changeNoAnarchyTurns(2)
		
	def closeNeighbourPlots(self, iNeighbour):
		neighbourPlots = plots.owner(iNeighbour).areas(self.location, capital(iNeighbour)).land()
		closest = neighbourPlots.without(self.area).closest(self.location)
		furthest = find_max(neighbourPlots.entities(), lambda p: distance(self.location, p)).result
		
		if not closest:
			return plots.none()
		
		closePlots, farPlots = neighbourPlots.split(lambda p: distance(closest, p) <= distance(furthest, p))
		return closePlots
	
	def revealTerritory(self):
		# reset visibility
		for plot in plots.all():
			plot.setRevealed(self.player.getID(), False, False, -1)

		# reveal birth area
		revealed = self.area.land()
		
		# if independence civ, revealed by civs controlling cities in birth area
		independenceRevealed = plots.none()
		if self.isIndependence():
			independenceRevealed = plots.sum(plots.owner(iOwner) for iOwner in self.area.cities().owners().major())
		
		# revealed by enough neighbours
		neighbours = self.area.expand(3).owners().major().without(self.iPlayer)
		neighbourRevealed = plots.sum(self.closeNeighbourPlots(iNeighbour) for iNeighbour in neighbours)
		
		# revealed by enough civilizations in your tech group
		iTechGroup = next(iGroup for iGroup in dTechGroups if self.iCiv in dTechGroups[iGroup])
		peers = players.major().alive().without(self.iPlayer).where(lambda p: civ(p) in dTechGroups[iTechGroup])
		peerRevealed = plots.none()
		
		def isPeerRevealed(plot):
			iRequiredPeers = plot.isWater() and peers.count() / 2 or peers.count() * 2 / 3
			return count(peer for peer in peers if plot.isRevealed(player(peer).getTeam(), False)) >= min(iRequiredPeers, peers.count()-1)
		
		if peers.count() > 2:
			peerRevealed += plots.all().where(isPeerRevealed).expand(1)
		
		bCanNeighbourReveal = revealed.intersect(neighbourRevealed)
		bCanPeerReveal = revealed.intersect(peerRevealed)
		
		revealed += independenceRevealed
		
		if bCanNeighbourReveal:
			revealed += neighbourRevealed
			
		iVisionRange = self.player.getCurrentEra() / 2 + 1
		revealed = revealed.expand(iVisionRange)
		
		if bCanPeerReveal:
			revealed += peerRevealed
		
		# reveal tiles
		for plot in revealed:
			plot.setRevealed(self.team.getID(), True, False, -1)
	
	def createUnits(self):
		createRoleUnits(self.iPlayer, self.location, getStartingUnits(self.iPlayer))
		createSpecificUnits(self.iPlayer, self.location)
		
		# select a settler if available
		if self.isHuman():
			settler = units.at(self.location).owner(self.iPlayer).where(lambda unit: unit.isFound()).last()
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
				data.players[self.iPlayer].lPreservedWonders += [iWonder for iWonder in infos.buildings() if isWonder(iWonder) and city.isHasRealBuilding(iWonder)]
				
				plot_(city).eraseAIDevelopment()
				plot_(city).setImprovementType(iCityRuins)
		
		for plot in plots.surrounding(self.location):
			convertPlotCulture(plot, self.iPlayer, 100, bOwner=True)
	
	def advancedStart(self):
		iAdvancedStartPoints = dAdvancedStartPoints[self.iPlayer]
		if iAdvancedStartPoints > 0:
			self.player.changeAdvancedStartPoints(scale(iAdvancedStartPoints)+1)
			
			if not self.isHuman():
				self.player.AI_doAdvancedStart()
	
	def resetPlague(self):
		data.players[self.iPlayer].iPlagueCountdown = -10
		clearPlague(self.iPlayer)
	
	def removeMinors(self):
		cities = self.area.cities()
		edge = self.area.expand(1).edge().where_surrounding(lambda p: not p.isCity()).passable()
		
		for unit in self.area.units().minor():
			if unit.isAnimal():
				unit.kill(False, -1)
				continue
		
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
			print "is canceled: %s" % self.name
			return
	
		iUntilBirth = until(self.iTurn)
		
		print "check for civ %s: iUntilBirth=%d, scenarioStart()=%s, scenarioStartTurn=%d" % (self.name, iUntilBirth, scenarioStart(), scenarioStartTurn())
		
		if iUntilBirth == turns(5) or (scenarioStart() and self.iTurn - turns(5) < scenarioStartTurn()):
			if not self.canSpawn():
				self.canceled = True
				return
			
			self.activate()
			self.prepare()
			self.protect()
			self.expansion()
			self.announce()
			
		elif iUntilBirth == 1:
			self.birth()
			self.checkSwitch()
		elif iUntilBirth == 0:
			self.flip()
			
		if iUntilBirth < 0:
			self.checkExpansion()
			
		if turn() == self.protectionEnd:
			self.resetProtection()
			
		self.checkIncompatibleCivs()
		
	def canSpawn(self):
		if self.isHuman():
			return True
		
		if not infos.civ(self.iCiv).isAIPlayable():
			return False
		
		# Rebirth requires rebirth civ to be dead
		if self.bRebirth and player(dRebirthCiv[self.iCiv]).isAlive():
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
	
		# independence civs require the player controlling the most cities in their area to be stable or worse
		if self.isIndependence():
			numCities = lambda p: plots.birth(self.iCiv).cities().owner(p).count()
			iMostCitiesPlayer = players.major().where(lambda p: civ(p) != self.iCiv).where(lambda p: numCities(p) > 0).maximum(numCities)
			if iMostCitiesPlayer is not None and civ(iMostCitiesPlayer) != self.iCiv:
				if stability(iMostCitiesPlayer) >= iStabilitySolid:
					return False
		
		return True
	
	def announce(self):
		if scenarioStart():
			return
	
		if game.getAIAutoPlay() > 0:
			return
	
		if plots.owner(active()).closest_distance(self.location) <= 10:
			key = "TXT_KEY_MESSAGE_RISE_%s" % infos.civ(self.iCiv).getIdentifier()
			text = text_if_exists(key, adjective(self.iPlayer), otherwise="TXT_KEY_MESSAGE_RISE_GENERIC")
			message(active(), str(text), location=self.location, color=iRed, button=infos.civ(self.iCiv).getButton())
	
	def activate(self):
		if self.iPlayer is None and self.bRebirth:
			self.iPlayer = slot(dRebirthCiv[self.iCiv])
		
		if self.iPlayer is None:
			self.iPlayer = findSlot(self.iCiv)
			
		print "self.iPlayer=%d for civilization %s" % (self.iPlayer, infos.civ(self.iCiv).getText())
		
		self.updateCivilization()
		self.updateStartingLocation()
		
		self.area = plots.birth(self.iPlayer) + plots.core(self.iPlayer)
		self.area = self.area.unique()
		
		events.fireEvent("activate", self.iPlayer, self.iCiv)

	def prepare(self):
		events.fireEvent("prepareBirth", self.iCiv)
	
	def protect(self):
		self.protectionEnd = self.iTurn + turns(20)
		self.player.setBirthProtected(True)
	
		for plot in self.area:
			plot.setBirthProtected(self.iPlayer)
	
		self.removeMinors()
	
	def resetProtection(self):
		self.player.setBirthProtected(False)
		
		for plot in self.area:
			plot.resetBirthProtected()
	
	def expansion(self):
		for plot in plots.expansion(self.iPlayer).without(self.area).land().where(lambda p: not p.isPeak()):
			plot.setExpansion(self.iPlayer)
		
		self.iExpansionDelay = turns(rand(10))
		self.iExpansionTurns = turns(30) + self.iExpansionDelay
	
	def checkExpansion(self):
		if self.iExpansionTurns < 0:
			return
		
		if self.iExpansionDelay > 0:
			return
	
		expansionPlots = plots.all().where(lambda p: p.getExpansion() == self.iPlayer)
		expansionCities = expansionPlots.cities()
		
		if expansionCities.owner(self.iPlayer).any(lambda city: since(city.getGameTurnAcquired()) <= 1):
			self.iExpansionTurns = max(self.iExpansionTurns, turns(10))
		
		if self.iExpansionTurns == 0:
			for plot in expansionPlots:
				plot.resetExpansion()
		
		self.iExpansionDelay -= 1
		self.iExpansionTurns -= 1
		
		if not self.isHuman() and expansionCities:
			targets = expansionCities.owners().without(self.iPlayer)
			minors, majors = targets.split(is_minor)
		
			for iMinor in minors.where(lambda p: not self.team.isAtWar(p)):
				self.team.declareWar(player(iMinor).getTeam(), False, WarPlanTypes.WARPLAN_LIMITED)
	
			if majors and majors.none(self.team.isAtWar):
				target = expansionCities.where(lambda city: not is_minor(city)).closest_all(cities.owner(self.iPlayer))
				self.team.declareWar(target.getTeam(), False, WarPlanTypes.WARPLAN_TOTAL)

	def checkIncompatibleCivs(self):
		if self.iCiv not in dClearedForBirth:
			return
		
		iClearedCiv = dClearedForBirth[self.iCiv]
		
		if not self.isHuman() and iClearedCiv not in lAlwaysClear:
			return
			
		if not player(iClearedCiv).isAlive():
			return
		
		if player(iClearedCiv).isHuman():
			return
		
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
		# initial save
		if self.isHuman():
			game.initialSave()
			
		# reset AI
		self.reset()
		
		# set initial birth turn
		self.player.setInitialBirthTurn(self.iTurn)
		
		# update area
		self.updateArea()
		
		# assign gold
		self.assignGold()
	
		# assign techs
		self.assignTechs()
		
		# set state religion
		self.assignStateReligion()
		
		# free civic switch
		self.assignCivics()
		
		# reveal territory
		self.revealTerritory()
		
		# flip capital
		self.prepareCapital()
		
		# create starting units
		self.createUnits()
		
		# reset plague
		self.resetPlague()
		
		# set as spawned
		data.civs[self.iCiv].bSpawned = True
		
		# send event
		if self.bRebirth:
			events.fireEvent("rebirth", self.iPlayer)
		else:
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
		flippedPlots = self.isIndependence() and self.area or plots.birth(self.iPlayer)
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
		
		events.fireEvent("flip", self.iPlayer)
