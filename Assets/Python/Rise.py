from Core import *
from Civilizations import *
from DynamicCivs import *
from Locations import *
from RFCUtils import *
from Slots import *

from Events import events, handler
from Collapse import completeCollapse
from Popups import popup

import Logging as log

import BugCore
import CvScreensInterface


MainOpt = BugCore.game.MainInterface


lExpandedFlipCivs = [
	iByzantium
]

lExpansionCivs = [
	iPersia,
	iRome,
	iKushans,
	iVikings,
	iTurks,
	iArabia,
	iSpain,
	iMongols,
	iMughals,
	iOttomans,
]

lIndependenceCivs = [
	iByzantium,
	iArgentina,
	iMexico,
	iColombia,
	iBrazil,
	iCanada
]

lDynamicReligionCivs = [
	iByzantium,
	iAmerica,
	iArgentina,
	iMexico,
	iColombia,
	iBrazil,
	iCanada
]

lInvasionCivs = [
	iOttomans,
]

dClearedForBirth = {
	iIndia: iHarappa,
	iByzantium: iGreece,
	iItaly: iRome,
	iRussia: iRus,
	iMexico: iAztecs,
}

lAlwaysClear = [
	iHarappa,
]

lBirthWars = [
	(iArabia, iEgypt),
	(iArabia, iBabylonia),
	(iArabia, iPersia),
	(iMongols, iChina),
	(iOttomans, iByzantium),
]


### Event Handlers ###


@handler("BeginGameTurn")
def showDawnOfMan(iGameTurn):
	if iGameTurn == scenarioStartTurn() and game.getAIAutoPlay() > 0 and data.iBeforeObserverSlot == -1:
		CvScreensInterface.dawnOfMan.interfaceScreen()
			

@handler("GameStart")
def initBirths():
	data.births = [Birth(iCiv) for iCiv in lBirthOrder]
	
	for birth in data.births:
		birth.check()


@handler("GameStart")
def initCamera():
	plot(dCapitals[active()]).cameraLookAt()


@handler("BeginGameTurn")
def checkBirths():
	for birth in data.births:
		birth.check()


@handler("changeWar")
def ensureAdditionalDefenders(bWar, iAttacker, iDefender, bFromDefensivePact):
	if not bWar:
		return
	
	if bFromDefensivePact:
		return
	
	if not player(iDefender).isBirthProtected():
		return
	
	iNumDefenders = 1 + (player(iDefender).getCurrentEra() + 1) / 2
	for city in cities.owner(iDefender).where(lambda city: plot(city).getBirthProtected() == iDefender):
		defenders = ensureDefenders(iDefender, city, iNumDefenders)
		for defender in defenders:
			mission(defender, MissionTypes.MISSION_FORTIFY)


@handler("changeWar")
def spawnWarUnits(bWar, iAttacker, iDefender, bFromDefensivePact):
	if not bWar:
		return
	
	if bFromDefensivePact:
		return
	
	if not player(iDefender).isBirthProtected():
		return
		
	if team(iAttacker).isAVassal():
		return
		
	city = capital(iDefender)
	
	if city:
		createRoleUnits(iDefender, city, getAdditionalUnits(iDefender))
		for iUnit, iAmount in getSpecificAdditionalUnits(iDefender):
			makeUnits(iDefender, iUnit, city, iAmount)


@handler("changeWar")
def balanceMilitary(bWar, iAttacker, iDefender, bFromDefensivePact):
	if not bWar:
		return
	
	if bFromDefensivePact:
		return
	
	if not player(iAttacker).isHuman():
		return
	
	if player(iDefender).isHuman():
		return

	if not player(iDefender).isBirthProtected():
		return
	
	iAttackerPower = player(iAttacker).getPower()
	iDefenderPower = player(iDefender).getPower()
	
	if not iAttackerPower:
		return
	
	iPowerRatioThreshold = player(iAttacker).isHuman() and 80 or 50
	iPowerRatio = 100 * iDefenderPower / iAttackerPower
	
	iMaxAdditionalPower = 200
	
	if iPowerRatio < iPowerRatioThreshold:
		iPowerRatioDifference = iPowerRatioThreshold - iPowerRatio
		iPowerRequired = iPowerRatioDifference * iAttackerPower / 100
		
		iPowerRequired = min(iPowerRequired, iMaxAdditionalPower * iDefenderPower / 100)
		
		additionalUnits = getAdditionalUnits(iDefender)
		iUnitsPower = sum(infos.unit(iUnit).getPowerValue() * iAmount for iRole, iAmount in additionalUnits for iUnit, _ in getUnitsForRole(iDefender, iRole))
		
		specificAdditionalUnits = getSpecificAdditionalUnits(iDefender)
		iUnitsPower += sum(infos.unit(iUnit).getPowerValue() * iAmount for iUnit, iAmount in specificAdditionalUnits)
		
		iAdditionalUnitsRequired = iUnitsPower > 0 and iPowerRequired / iUnitsPower or 1
		
		for _ in range(iAdditionalUnitsRequired):
			createRoleUnits(iDefender, capital(iDefender), additionalUnits)
			for iUnit, iAmount in specificAdditionalUnits:
				lExperiences = [iRoleExperience for iRole, iRoleExperience in dStartingExperience[iDefender].items() if isUnitOfRole(iUnit, iRole)]
				iExperience = lExperiences and max(lExperiences) or 0
				makeUnits(iDefender, iUnit, capital(iDefender), iAmount).experience(iExperience)


@handler("changeWar")
def moveOutAttackers(bWar, iAttacker, iDefender):
	if not bWar:
		return
	
	if not player(iDefender).isBirthProtected():
		return
	
	aroundCities = cities.owner(iDefender).plots().expand(2)
	birthProtected = plots.all().where(lambda p: p.getBirthProtected() == iDefender and not p.isPlayerCore(iAttacker) and not p.getOwner() == iAttacker)
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
	
	if player(iAttacker).isHuman():
		return
		
	if player(iDefender).isBirthProtected():
		return
	
	if is_minor(iDefender):
		return
	
	attackerCities = cities.owner(iAttacker)
	defenderCities = cities.owner(iDefender)
	expansionCities = defenderCities.where(lambda city: plot(city).getExpansion() == iAttacker)
	
	bLessPowerful = player(iAttacker).getPower() < player(iDefender).getPower()
	
	if expansionCities and attackerCities:
		target, attacker_closest = expansionCities.closest_pair(attackerCities)
		defender_closest = defenderCities.closest(attacker_closest)
		
		iDistance = player(iDefender).isHuman() and 3 or 2
		spawn = possibleSpawnsBetween(attacker_closest, defender_closest, iDistance).closest(defender_closest)
		
		iExtraAI = 0
		iExtraTargets = 0
		if bLessPowerful and not player(iDefender).isHuman():
			iExtraTargets = expansionCities.count()-1
			
			if not player(iAttacker).isHuman():
				iExtraAI = 1
		
		dExpansionUnits = {
			iAttack: 2 + iExtraAI + iExtraTargets,
			iSiege: 1 + 2*iExtraAI + iExtraTargets,
		}
		createRoleUnits(iAttacker, spawn, dExpansionUnits.items())
		
		message(iDefender, "TXT_KEY_MESSAGE_EXPANSION_UNITS", player(iAttacker).getCivilizationDescription(0), defender_closest.getName(), color=iRed, location=spawn, button=infos.civ(player(iAttacker).getCivilizationType()).getButton())


@handler("changeWar")
def endExpansionOnPeace(bWar, iPlayer1, iPlayer2):
	if not bWar:
		for plot in plots.owner(iPlayer1).where(lambda plot: plot.getExpansion() == iPlayer2):
			plot.resetExpansion()
		
		for plot in plots.owner(iPlayer2).where(lambda plot: plot.getExpansion() == iPlayer1):
			plot.resetExpansion()


@handler("collapse")
def endExpansionOnCollapse(iPlayer):
	for plot in plots.all().where(lambda plot: plot.getExpansion() == iPlayer):
		plot.resetExpansion()


@handler("firstCity")
def createStartingWorkers(city):
	iPlayer = city.getOwner()
	iNumStartingWorkers = dStartingUnits[iPlayer].get(iWork, 0)
	
	if iNumStartingWorkers > 0:
		createRoleUnit(iPlayer, city, iWork, iNumStartingWorkers)
	

@handler("firstCity")
def createInvaderSettlers(city):
	iPlayer = city.getOwner()
	if not civ(iPlayer) in lInvasionCivs:
		return
	
	iNumSettlers = dStartingUnits[iPlayer].get(iSettler, 0)
	if iNumSettlers > 0:
		createSettlers(iPlayer, iNumSettlers, bGrantCapital=False)


@handler("firstCity")
def restorePreservedWonders(city):
	while data.players[city.getOwner()].lPreservedWonders:
		iWonder = data.players[city.getOwner()].lPreservedWonders.pop(0)
		if city.isValidBuildingLocation(iWonder):
			city.setHasRealBuilding(iWonder, True)


@handler("playerDestroyed")
def preserveCivilizationAttributes(iPlayer):
	data.civs[iPlayer].iGreatGeneralsCreated = player(iPlayer).getGreatGeneralsCreated()
	data.civs[iPlayer].iGreatPeopleCreated = player(iPlayer).getGreatPeopleCreated()
	data.civs[iPlayer].iGreatSpiesCreated = player(iPlayer).getGreatSpiesCreated()
	data.civs[iPlayer].iNumUnitGoldenAges = player(iPlayer).getNumUnitGoldenAges()
	

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
	iMinor = players.independent().existing().periodic(20)
	if iMinor:
		updateMinorTechs(iMinor, barbarian())


class Birth(object):

	def __init__(self, iCiv):
		self.iCiv = iCiv
		self.iTurn = year(dBirth[iCiv])
		
		self.iPlayer = None
		self.area = None
		
		self.civ = next((civ for civ in lCivilizations if civ.iCiv == self.iCiv), Civilization(self.iCiv))
		
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
	def data(self):
		return data.players[self.iPlayer]
	
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
		return popup.text("TXT_KEY_POPUP_SWITCH").option(self.noSwitch, "TXT_KEY_POPUP_NO").option(self.switch, "TXT_KEY_POPUP_YES").build()
	
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
		
		# reset stability
		self.data.resetStability()
	
		# reset diplomatic relations
		self.resetDiplomacy()
	
		# reset espionage against
		self.resetEspionage()
	
		# reset great people
		self.resetGreatPeople()
	
	def resetDiplomacy(self):
		for iOtherPlayer in players.major().without(self.iPlayer):
			self.team.makePeace(player(iOtherPlayer).getTeam())
			
			if self.team.isVassal(player(iOtherPlayer).getTeam()):
				team(iOtherPlayer).freeVassal(self.player.getTeam())
			
			if team(iOtherPlayer).isVassal(self.player.getTeam()):
				self.team.freeVassal(player(iOtherPlayer).getTeam())
				
			self.team.cutContact(player(iOtherPlayer).getTeam())
	
	def resetEspionage(self):
		player().setEspionageSpendingWeightAgainstTeam(self.player.getTeam(), 0)
		
		for iOtherPlayer in players.all():
			team(player(iOtherPlayer).getTeam()).setEspionagePointsAgainstTeam(self.player.getTeam(), 0)
	
	def resetGreatPeople(self):
		self.player.resetGreatPeopleCreated()
		
		self.player.changeGreatPeopleCreated(data.civs[self.iCiv].iGreatPeopleCreated)
		self.player.changeGreatGeneralsCreated(data.civs[self.iCiv].iGreatGeneralsCreated)
		self.player.changeGreatSpiesCreated(data.civs[self.iCiv].iGreatSpiesCreated)
		
		self.player.setNumUnitGoldenAges(data.civs[self.iCiv].iNumUnitGoldenAges)
		
	def updateCivilization(self):
		updateCivilization(self.iPlayer, self.iCiv, iBirthTurn=self.iTurn)

	def updateStartingLocation(self):
		startingPlot = plots.capital(self.iCiv)
		self.player.setStartingPlot(startingPlot, False)
	
	def updateNames(self):
		setLeader(self.iPlayer, startingLeader(self.iPlayer))
		
		if self.player.getNumCities() == 0:
			setDesc(self.iPlayer, peoplesName(self.iPlayer))
		
	def updateArea(self):
		if self.iCiv in lExpandedFlipCivs:
			owners = self.area.cities().owners().major()
			ownerCities = cities.all().area(self.location).where(lambda city: city.getOwner() in owners).where(lambda city: not plot(city).isPlayerCore(city.getOwner()))
			closerCities = ownerCities.where(lambda city: real_distance(city, self.location) <= real_distance(city, capital(city)) and real_distance(city, self.location) <= 14)
			
			additionalPlots = closerCities.plots().expand(2).where(lambda p: p.getOwner() in owners and none(p.isPlayerCore(iPlayer) for iPlayer in players.major().existing().without(self.iPlayer)))
			
			self.area += additionalPlots
			self.area = self.area.unique()
		
		if self.iCiv == iMexico:
			self.area = self.area.where(lambda p: p.isPlayerCore(self.iPlayer) or not owner(p, iAmerica))
		
		if self.iCiv == iCanada:
			self.area += cities.regions(rOntario, rQuebec, rMaritimes).where(lambda city: city.getX() < plots.capital(iCanada).getX()).where(lambda city: civ(city) in [iFrance, iEngland, iAmerica]).plots().expand(2).where(lambda p: not p.isCore(p.getOwner()))
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
				
	def assignAdditionalTechs(self):
		if self.iCiv == iChina and scenario() == i3000BC and not self.isHuman():
			for iTech in [iProperty, iAlloys]:
				self.team.setHasTech(iTech, True, self.iPlayer, False, False)
	
	def assignAttributes(self):
		# civilization attributes
		self.civ.apply()
		
		# dynamic starting religion
		if self.iCiv in lDynamicReligionCivs:
			iPrevalentReligion = getPrevalentReligion(self.area, self.iPlayer)
			if iPrevalentReligion >= 0:
				self.player.setLastStateReligion(iPrevalentReligion)
		
		# allow free civic changes in the birth and flip turn
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
		peers = players.major().existing().without(self.iPlayer).where(lambda p: civ(p) in dTechGroups[iTechGroup])
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
		
		# for AI, reveal nearby settler targets to improve settler AI
		if not self.isHuman():
			revealed += plots.all().land().where(lambda p: p.getSettlerValue(self.iCiv) >= 10).where(lambda p: distance(self.location, p) <= 15).expand(2)
		
		# reveal tiles
		for plot in revealed:
			plot.setRevealed(self.team.getID(), True, False, -1)
	
	def createUnits(self):
		bInvasionCiv = self.iCiv in lInvasionCivs
		
		createRoleUnits(self.iPlayer, self.location, getStartingUnits(self.iPlayer), bCreateSettlers=not bInvasionCiv)
		
		# if invader but no cities in birth, still grant a settler now
		if bInvasionCiv and not cities.birth(self.iPlayer):
			createRoleUnit(self.iPlayer, self.location, iSettle)
		
		# only create units if coming from autoplay, otherwise after the switch
		if self.iPlayer == active():
			createSpecificUnits(self.iPlayer, self.location)
		
		# select a settler if available
		if self.isHuman():
			settler = units.at(self.location).owner(self.iPlayer).where(lambda unit: unit.isFound()).last()
			if settler:
				interface.selectUnit(settler, True, False, False)
		
		# update revealed owners
		for plot in plots.all():
			plot.updateRevealedOwner(self.team.getID())
	
	def prepareCapital(self):
		expelUnits(self.iPlayer, plots.surrounding(self.location), self.flippedArea())
	
		if plot_(self.location).isCity():
			completeCityFlip(self.location, self.iPlayer, city_(self.location).getOwner(), 100)
		
		if self.iCiv not in lInvasionCivs:
			for city in cities.ring(self.location):
				if city.isHolyCity():
					completeCityFlip(city, self.iPlayer, city.getOwner(), 100)
				else:
					self.data.lPreservedWonders += [iWonder for iWonder in infos.buildings() if isWonder(iWonder) and city.isHasRealBuilding(iWonder)]
				
					plot_(city).eraseAIDevelopment()
					plot_(city).setImprovementType(iCityRuins)
		
		for plot in plots.surrounding(self.location):
			convertPlotCulture(plot, self.iPlayer, 100, bOwner=True)
			
	def resetPlague(self):
		self.data.iPlagueCountdown = -10
		clearPlague(self.iPlayer)
	
	def removeMinors(self):
		cities = self.area.cities()
		edge = self.area.expand(1).edge().where_surrounding(lambda p: not p.isCity()).where(lambda p: not p.isOwned() or is_minor(p)).passable()
		
		for unit in self.area.units().minor():
			if unit.isAnimal():
				unit.kill(False, -1)
				continue
			
			if cities.owner(unit.getOwner()):
				closest = cities.owner(unit.getOwner()).closest(unit)
			elif unit.getDomainType() == DomainTypes.DOMAIN_SEA or unit.isCargo():
				if edge.sea():
					closest = edge.sea().closest(unit)
				else:
					closest = plots.all().sea().without(self.area).closest(unit)
			else:
				closest = edge.land().area(unit).closest(unit)
			
			if closest:
				move(unit, closest)
			else:
				unit.kill(False, -1)
	
	def check(self):
		if self.canceled:
			return
		
		if self.isHuman() and data.iBeforeObserverSlot != -1:
			return
	
		iUntilBirth = until(self.iTurn)
		
		if iUntilBirth == turns(5) or (scenarioStart() and self.iTurn - turns(5) < scenarioStartTurn()):
			if not self.canSpawn():
				self.canceled = True
				return
			
			self.activate()

			if self.canceled:
				return
			
			self.prepare()
			self.protect()
			self.expansion()
			self.announce()
			
		elif iUntilBirth == 1:
			self.birth()
			self.checkSwitch()
		elif iUntilBirth == 0:
			self.flip()
			self.wars()
			
		if iUntilBirth < 0:
			self.checkExpansion()
			
		if turn() == self.protectionEnd:
			self.resetProtection()
			
		self.checkIncompatibleCivs()
		
	def canSpawn(self):
		if self.isHuman() and not data.iBeforeObserverSlot != -1:
			return True
		
		if not infos.civ(self.iCiv).isAIPlayable():
			return False
		
		# Byzantium requires Rome to be alive and Greece to be dead (human Rome can avoid Byzantine spawn by being solid)
		if self.iCiv == iByzantium:
			if not player(iRome).isExisting():
				return False
			elif player(iGreece).isExisting():
				return False
			elif player(iRome).isHuman() and stability(iRome) == iStabilitySolid:
				return False
		
		# Italy requires Rome to be dead
		if self.iCiv == iItaly:
			if player(iRome).isExisting():
				return False
		
		# Ottomans require that the Turks managed to conquer at least one city in the Near East
		if self.iCiv == iOttomans:
			if cities.birth(iOttomans).none(CyCity.isHuman) and cities.rectangle(*tNearEast).none(lambda city: iTurks in [city.getCivilizationType(), city.getPreviousCiv()]):
				return False
		
		# Thailand requires Khmer to be shaky or worse (unstable if Khmer is human)
		if self.iCiv == iThailand:
			iRequiredStability = player(iKhmer).isHuman() and iStabilityShaky or iStabilityStable
			if player(iKhmer).isExisting() and stability(iKhmer) >= iRequiredStability:
				return False
		
		# Iran requires Persia to be dead
		if self.iCiv == iIran:
			if player(iPersia).isExisting():
				return False
		
		# Mexico requires Aztecs to be dead
		if self.iCiv == iMexico:
			if player(iAztecs).isExisting():
				return False
	
		# independence civs require all players controlling cities in their area to be stable or worse
		if self.isIndependence():
			birthCities = plots.birth(self.iCiv).cities()
			if players.major().where(lambda p: civ(p) != self.iCiv).where(lambda p: birthCities.owner(p).any()).all_if_any(lambda p: stability(p) >= iStabilitySolid):
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
			message(active(), text.encode("ascii", "xmlcharrefreplace"), location=self.location, color=iRed, button=infos.civ(self.iCiv).getButton())
	
	def activate(self):
		if self.iPlayer is None:
			self.iPlayer = findSlot(self.iCiv)
			
		if self.iPlayer < 0:
			self.canceled = True
			log.rise("BIRTH CANCELED: no free slot found for %s", infos.civ(self.iCiv).getText())
			return
		
		self.updateCivilization()
		self.updateStartingLocation()
		self.updateNames()
		
		self.player.setInitialBirthTurn(self.iTurn)
		
		if not self.isHuman():
			self.player.setAlive(True, True)
		
		self.area = plots.birth(self.iPlayer) + plots.core(self.iPlayer)
		self.area = self.area.unique()

	def prepare(self):
		events.fireEvent("prepareBirth", self.iCiv)
	
	def protect(self):
		self.protectionEnd = self.iTurn + turns(10)
		self.player.setBirthProtected(True)
	
		for plot in self.area:
			plot.setBirthProtected(self.iPlayer)
	
		self.removeMinors()
	
	def resetProtection(self):
		self.player.setBirthProtected(False)
		
		for plot in self.area:
			plot.resetBirthProtected()
	
	def expansion(self):
		for plot in plots.all().where(lambda p: p.getExpansion() == self.iPlayer):
			plot.resetExpansion()
	
		if self.iCiv in lExpansionCivs:
			capital_continent = plot_(self.location).getContinentArea()
			
			for plot in plots.all().without(self.area).where(lambda p: p.getPlayerWarValue(self.iPlayer) >= 5).where(lambda p: p.getContinentArea() == capital_continent or distance(self.location, p) <= 32).land().where(lambda p: not p.isPeak()):
				plot.setExpansion(self.iPlayer)

			self.iExpansionDelay = rand(turns(5)) + 1
			self.iExpansionTurns = turns(30)
	
	def checkExpansion(self):
		if not self.player.isExisting():
			return
		
		if self.player.getNumCities() == 0:
			return
		
		if self.team.isAVassal():
			return
		
		if self.team.getAtWarCount(True) > 0:
			return
		
		if self.iExpansionTurns < 0:
			return
		
		expansionPlots = plots.all().where(lambda p: p.getExpansion() == self.iPlayer and p.isRevealed(self.player.getTeam(), False))
		expansionCities = expansionPlots.cities().notowner(self.iPlayer)
		
		if expansionCities.owner(self.iPlayer).any(lambda city: since(city.getGameTurnAcquired()) <= 1):
			self.iExpansionTurns = max(self.iExpansionTurns, turns(10))
		
		if self.iExpansionTurns == 0:
			for plot in expansionPlots:
				plot.resetExpansion()
		
		self.iExpansionDelay -= 1
		self.iExpansionTurns -= 1
		
		if self.iExpansionDelay >= 0:
			return
		
		if not self.isHuman() and expansionCities:
			targets = expansionCities.owners().without(self.iPlayer).where(self.team.canDeclareWar).where(self.player.canContact).where(lambda p: not player(p).isBirthProtected())
			minors, majors = targets.split(is_minor)
		
			for iMinor in minors.where(lambda p: not self.team.isAtWar(p)):
				self.team.declareWar(player(iMinor).getTeam(), False, WarPlanTypes.WARPLAN_LIMITED)
	
			if majors and majors.none(self.team.isAtWar):
				target = expansionCities.where(lambda city: not is_minor(city)).closest_all(cities.owner(self.iPlayer))
				self.team.declareWar(target.getTeam(), True, WarPlanTypes.WARPLAN_TOTAL)

	def checkIncompatibleCivs(self):
		if self.iCiv not in dClearedForBirth:
			return
		
		iClearedCiv = dClearedForBirth[self.iCiv]
		
		if not self.isHuman() and iClearedCiv not in lAlwaysClear:
			return
			
		if not player(iClearedCiv).isExisting():
			return
		
		if player(iClearedCiv).isHuman():
			return
		
		if turn() == year(dFall[iClearedCiv]).deviate(10, data.iSeed):
			completeCollapse(slot(iClearedCiv))
	
	def checkSwitch(self):
		if not self.canSwitch():
			self.assignAdditionalTechs()
			return

		self.switchPopup.text(adjective(self.iPlayer)).noSwitch().switch().launch()
	
	def canSwitch(self):
		if not MainOpt.isSwitchPopup():
			return False
	
		if game.getAIAutoPlay() > 0:
			return False
		
		if civ() in dNeighbours[self.iPlayer] and since(year(dBirth[active()])) < turns(25):
			return False
	
		return True
	
	def noSwitch(self):
		if not self.isHuman():
			self.assignAdditionalTechs()
			createRoleUnits(self.iPlayer, self.location, getAIStartingUnits(self.iPlayer))
		
		createSpecificUnits(self.iPlayer, self.location)
	
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
		
		if player(iPreviousPlayer).getAdvancedStartPoints() > 0:
			player(iPreviousPlayer).AI_doAdvancedStart()
		
		for iOtherPlayer in players.major():
			self.player.setEspionageSpendingWeightAgainstTeam(player(iOtherPlayer).getTeam(), 0)
		
		# update statistics offsets
		
		statistics = CyStatistics()
		
		dUnitsBuilt = dict((iUnit, statistics.getPlayerNumUnitsBuilt(self.iPlayer, iUnit)) for iUnit in infos.units())
		dUnitsKilled = dict((iUnit, statistics.getPlayerNumUnitsKilled(self.iPlayer, iUnit)) for iUnit in infos.units())
		dUnitsLost = dict((iUnit, statistics.getPlayerNumUnitsLost(self.iPlayer, iUnit)) for iUnit in infos.units())
		dBuildingsBuilt = dict((iBuilding, statistics.getPlayerNumBuildingsBuilt(self.iPlayer, iBuilding)) for iBuilding in infos.buildings())
		
		data.dUnitsBuilt = dict((iUnit, iNumUnits) for iUnit, iNumUnits in dUnitsBuilt.items() if iNumUnits > 0)
		data.dUnitsKilled = dict((iUnit, iNumUnits) for iUnit, iNumUnits in dUnitsKilled.items() if iNumUnits > 0)
		data.dUnitsLost = dict((iUnit, iNumUnits) for iUnit, iNumUnits in dUnitsLost.items() if iNumUnits > 0)
		data.dBuildingsBuilt = dict((iBuilding, iNumBuildings) for iBuilding, iNumBuildings in dBuildingsBuilt.items() if iNumBuildings > 0)
	
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
		
		# assign civilization attributes
		self.assignAttributes()
		
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
		
		if team(iOwner).isAtWar(self.player.getTeam()):
			team(iOwner).AI_setAtWarCounter(self.player.getTeam(), 0)
			self.team.AI_setAtWarCounter(player(iOwner).getTeam(), 0)
			return
		
		iRefusalModifier = dWarOnFlipProbability[iOwner]
		if chance(iRefusalModifier):
			player(iOwner).AI_changeMemoryCount(self.iPlayer, MemoryTypes.MEMORY_STOPPED_TRADING_RECENT, turns(5 + iRefusalModifier / 10))
	
	def declareWarOnFlip(self, iOwner):
		team(iOwner).declareWar(self.player.getTeam(), False, WarPlanTypes.WARPLAN_ATTACKED_RECENT)
	
	def flippedArea(self):
		return self.isIndependence() and self.area or plots.birth(self.iPlayer)
	
	def flip(self):
		flippedPlots = self.flippedArea()
		
		excludedPlots = flippedPlots.where(lambda p: p.isCity() and city_(p).isCapital() and p.isPlayerCore(p.getOwner()))
		excludedPlots = excludedPlots.expand(1).where(lambda p: cities.surrounding(p).all(lambda city: city in excludedPlots))
		
		flippedPlots = flippedPlots.without(excludedPlots)
		
		flippedCities = flippedPlots.cities().notowner(self.iPlayer)
		flippedCityPlots = flippedCities.plots()
	
		flippedPlayerCities = dict((p, format_separators(flippedCities.owner(p), ",", text("TXT_KEY_AND"), CyCity.getName)) for p in flippedCities.owners().major())
		
		expelUnits(self.iPlayer, flippedPlots)
		
		for city in flippedCities:
			city = completeCityFlip(city, self.iPlayer, city.getOwner(), 100, bFlipUnits=True)
			city.rebuild(-1)
			
			iMinPopulation = self.player.getCurrentEra() + 1
			city.setPopulation(max(iMinPopulation, city.getPopulation()))
			
			if since(scenarioStartTurn()):
				ensureDefenders(self.iPlayer, city, 2)
		
		convertSurroundingPlotCulture(self.iPlayer, flippedPlots.land())
		convertSurroundingPlotCulture(self.iPlayer, flippedPlots.water().where(lambda p: p.getPlayerCityRadiusCount(self.iPlayer) > 0))
		
		for iOwner, cityNames in flippedPlayerCities.items():
			self.warOnFlip(iOwner, cityNames)
		
		flipped_names = format_separators(flippedCityPlots.cities(), ",", text("TXT_KEY_AND"), CyCity.getName)
		if flippedCities:
			message(self.iPlayer, 'TXT_KEY_MESSAGE_CITIES_FLIPPED', flipped_names, color=iGreen)
		
		self.civ.advancedStart()
		
		events.fireEvent("flip", self.iPlayer)
	
	def wars(self):
		if self.isHuman():
			return
	
		expansionArea = plots.all().where(lambda p: p.getExpansion() == self.iPlayer)
		expansionTargets = expansionArea.owners()
		
		for iTarget in expansionTargets:
			if (self.iCiv, civ(iTarget)) in lBirthWars:
				self.team.declareWar(player(iTarget).getTeam(), True, WarPlanTypes.WARPLAN_TOTAL)
				
				if player(iTarget).isHuman():
					for plot in expansionArea.owner(iTarget).core(iTarget):
						plot.resetExpansion()
		
