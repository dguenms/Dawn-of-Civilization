# Rhye's and Fall of Civilization - Main Scenario

from CvPythonExtensions import *
import CvUtil
from PyHelpers import PyPlayer
import Popup
from StoredData import data # edead
import CvTranslator
from RFCUtils import *
from Consts import *
import CityNameManager as cnm
from operator import itemgetter
import Stability as sta
import Civilizations
import Modifiers
import CvEspionageAdvisor
import BugCore
import Periods as periods
from Events import events, handler, popup_handler

from Locations import *
from Popups import popup
from Core import *

MainOpt = BugCore.game.MainInterface

################
### Globals ###
##############

iCheatersPeriod = 12
iBetrayalPeriod = 8
iBetrayalThreshold = 80
iRebellionDelay = 15
iEscapePeriod = 30

### Event handlers ###

@handler("GameStart")
def setup():
	rnf.determineEnabledPlayers()
	
	# Leoreth: make sure to select the Egyptian settler
	if player(iEgypt).isHuman():
		unit = units.at(plots.capital(iEgypt)).type(iSettler).one()
		if unit:
			interface.selectUnit(unit, True, False, False)

@handler("combatResult")
def restoreDefeatedUnitDuringSpawn(winningUnit, losingUnit):
	iLosingPlayer = losingUnit.getOwner()
	
	if not is_minor(iLosingPlayer):
		iBirthTurn = year(dBirth[iLosingPlayer])
		if iBirthTurn <= year() <= iBirthTurn + turns(2):
			if at(losingUnit, plots.capital(iLosingPlayer)):
				if rand(100) >= 50:
					makeUnit(iLosingPlayer, losingUnit.getUnitType(), losingUnit)

@handler("BeginGameTurn")
def checkInitBetrayal():
	initBetrayal()

# TODO: this is bad and need to be rewritten
def initBetrayal():
	if data.iBetrayalTurns > 0:
		iFlipPlayer = data.iFlipNewPlayer
		if not player(iFlipPlayer).isAlive() or not team(iFlipPlayer).isAtWar(active()):
			data.iBetrayalTurns = 0
			return

		turnsLeft = data.iBetrayalTurns

		lTempPlots = [tPlot for tPlot in data.lTempPlots if not plot(tPlot).isCore(data.iFlipOldPlayer)]
		plotList = listSearch(lTempPlots, outerInvasion, [] )
		if not plotList:
			plotList = listSearch(lTempPlots, innerSpawn, [data.iFlipOldPlayer, data.iFlipNewPlayer] )			
		if not plotList:
			plotList = listSearch(lTempPlots, innerInvasion, [data.iFlipOldPlayer, data.iFlipNewPlayer] )				
		if plotList:
			tPlot = random_entry(plotList)
			if tPlot:
				if turnsLeft == iBetrayalPeriod:
					createAdditionalUnits(data.iFlipNewPlayer, tPlot)
				self.unitsBetrayal(data.iFlipNewPlayer, data.iFlipOldPlayer, lTempPlots, tPlot)
		data.iBetrayalTurns = turnsLeft - 1
		
@handler("BeginGameTurn")
def clearIncompatibleAIsDuringAutoplay(iGameTurn):
	if iGameTurn == year(476):
		if player(iItaly).isHuman() and player(iRome).isAlive():
			sta.completeCollapse(slot(iRome))
			
	if iGameTurn == year(-50):
		if player(iByzantium).isHuman() and player(iGreece).isAlive():
			sta.completeCollapse(slot(iGreece))
			
	if iGameTurn == year(dBirth[iIndia]) - turns(1):
		if player(iHarappa).isAlive() and not player(iHarappa).isHuman():
			sta.completeCollapse(slot(iHarappa))
				
	if year() == year(1700)-2:
		if year(dBirth[active()]) >= year(1700) and player(iAztecs).isAlive():
			sta.completeCollapse(slot(iAztecs))

@handler("BeginGameTurn")
def checkBirths():
	for iLoopPlayer in players.major().where(lambda p: dBirth[p] > scenarioStartYear()):
		if year(dBirth[iLoopPlayer]) - turns(2) <= year() <= year(dBirth[iLoopPlayer]) + turns(6):
			rnf.initBirth(dBirth[iLoopPlayer], iLoopPlayer)

@handler("BeginGameTurn")
def checkRebirths():
	for iCiv, iYear in dRebirth.items():
		iPlayer = slot(iCiv)
	
		if year() == year(iYear) and not player(iCiv).isAlive():
			rnf.rebirthFirstTurn(iPlayer)
			
		iRebirthCiv = dRebirthCiv[iCiv]
		iRebirthPlayer = slot(iRebirthCiv)
		
		if year() == year(iYear)+1 and player(iRebirthCiv).isAlive() and player(iRebirthCiv).getLastBirthTurn() == year()-1:
			rnf.rebirthSecondTurn(iRebirthPlayer)

@handler("BeginGameTurn")
def fragmentIndependents():
	if year() >= year(50) and periodic(15):
		iLargestMinor = players.independent().maximum(lambda p: player(p).getNumCities())
		iSmallestMinor = players.independent().minimum(lambda p: player(p).getNumCities())
		if player(iLargestMinor).getNumCities() > 2 * player(iSmallestMinor).getNumCities():
			for city in cities.owner(iLargestMinor).sample(3):
				completeCityFlip(city, iLargestMinor, iSmallestMinor, 50, False, True, True, True)


@handler("BeginGameTurn")
def clearBirthArea():
	for iCiv in [iVikings, iSpain, iFrance, iHolyRome, iRussia, iAztecs]:
		if year(dBirth[iCiv]) + turns(2) <= year() <= year(dBirth[iCiv]) + turns(10):
			killUnitsInArea(barbarian(), plots.birth(iCiv))


@handler("BeginPlayerTurn")
def preparePlayerCapital(iGameTurn, iCurrentPlayer):
	iPlayer = data.iPrepareCapitalPlayer
	
	if iPlayer < 0:
		return
	
	iCiv = civ(iPlayer)
	
	tCapital = location(plots.capital(iCiv))
	x, y = tCapital
	
	if iCurrentPlayer == iPlayer:
		if iCiv == iPhoenicia:
			for plot in plots.rectangle((x-2, y-1), (x+1, y+1)):
				plot.setCulture(iPlayer, 300, True)
		else:
			for plot in plots.surrounding(tCapital, radius=2):
				plot.setCulture(iPlayer, 300, True)
		for plot in plots.surrounding(tCapital):
			convertPlotCulture(plot, iPlayer, 100, True)
			if plot.getCulture(iPlayer) < 3000:
				plot.setCulture(iPlayer, 3000, True) #2000 in vanilla/warlords, cos here Portugal is choked by spanish culture
			plot.setOwner(iPlayer)
		data.iPrepareCapitalPlayer = -1
		return
	
	if iCurrentPlayer != iPlayer-1 and iCiv not in [iCarthage, iGreece]:
		return
	
	bNotOwned = True
	for plot in plots.surrounding(tCapital):
		if plot.isOwned():
			bNotOwned = False
			for iLoopPlayer in players.all().without(iPlayer):
				plot.setCulture(iLoopPlayer, 0, True)
			plot.setOwner(iPlayer)
	
	for plot in plots.surrounding(tCapital, radius=15).without(tCapital).land(): # must include the distance from Sogut to the Caspius
		for unit in units.at(plot).owner(iPlayer):
			move(unit, tCapital)
			
@handler("birth")
def germanSpawn(iPlayer):
	if civ(iPlayer) == iGermany:
		iHolyRomanPlayer = slot(iHolyRome)

		if stability(iHolyRomanPlayer) < iStabilityShaky:
			data.setStabilityLevel(iHolyRomanPlayer, iStabilityShaky)

@handler("birth")
def arabianSpawn(iPlayer):
	if civ(iPlayer) == iArabia:
		bBaghdad = civ(plot(tBaghdad)) == iArabia
		bCairo = civ(plot(tCairo)) == iArabia

		lCities = []

		if bBaghdad: lCities.append(tBaghdad)
		if bCairo: lCities.append(tCairo)

		tCapital = random_entry(lCities)

		if tCapital:
			if not player(iArabia).isHuman():
				relocateCapital(iArabia, tCapital)
				makeUnits(iArabia, iMobileGuard, tCapital, 3)
				makeUnits(iArabia, iGhazi, tCapital, 2)
			makeUnits(iArabia, iMobileGuard, tCapital, 2)
			makeUnits(iArabia, iGhazi, tCapital, 2)

		if bBaghdad:
			makeUnit(iArabia, iSettler, tBaghdad)
			makeUnit(iArabia, iWorker, tBaghdad)

		if bCairo:
			makeUnit(iArabia, iSettler, tCairo)
			makeUnit(iArabia, iWorker, tCairo)
			
		if len(lCities) < 2:
			makeUnits(iArabia, iSettler, tMecca, 2 - len(lCities))
			makeUnits(iArabia, iWorker, tMecca, 2 - len(lCities))

		if not player(iArabia).isHuman() and bBaghdad:
			makeUnits(iArabia, iSpearman, tBaghdad, 2)


### Screen popups ###
# (Slowly migrate event handlers here when rewriting to use Popups.popup and more idiomatic code)

def handleNewCiv(iPlayer):
	iPreviousPlayer = active()
	iOldHandicap = player().getHandicapType()
	
	pPlayer = player(iPlayer)
	
	player().setHandicapType(pPlayer.getHandicapType())
	game.setActivePlayer(iPlayer, False)
	pPlayer.setHandicapType(iOldHandicap)
	
	for iMaster in players.major():
		if team(iPlayer).isVassal(iMaster):
			team(iPlayer).setVassal(iMaster, False, False)
	
	data.bAlreadySwitched = True
	player(iPlayer).setPlayable(True)
	
	if game.getWinner() == iPreviousPlayer:
		game.setWinner(-1, -1)
	
	data.resetHumanStability()

	for city in cities.owner(iPlayer):
		city.setInfoDirty(True)
		city.setLayoutDirty(True)
					
	for i in range(3):
		data.players[iPlayer].lGoals[i] = -1
		
	events.fireEvent("switch", iPreviousPlayer, iPlayer)
		
	for iLoopPlayer in players.major():
		player(iPlayer).setEspionageSpendingWeightAgainstTeam(iLoopPlayer, 0)


new_civ_switch = popup.text("TXT_KEY_INTERFACE_NEW_CIV_SWITCH") \
					  .cancel("TXT_KEY_POPUP_NO", event_bullet) \
					  .option(handleNewCiv, "TXT_KEY_POPUP_YES") \
					  .build()

def startNewCivSwitchEvent(iPlayer):
	if MainOpt.isSwitchPopup():
		new_civ_switch.text(adjective(iPlayer)).cancel().handleNewCiv().launch(iPlayer)
		
### Utility methods ###

@handler("BeginGameTurn")
def checkMinorTechs():
	iMinor = players.independent().alive().periodic(20)
	if iMinor:
		updateMinorTechs(iMinor, barbarian())

@handler("EndPlayerTurn")
def checkFlipPopupOnPlayerTurn(iGameTurn, iPlayer):
	checkFlipPopup(iGameTurn, iPlayer)

def checkFlipPopup(iGameTurn, iPlayer):
	if player(iPlayer).isHuman():
		for tEvent in data.lTempEvents:
			iNewPlayer, lPlots = tEvent
			flipPopup(iNewPlayer, lPlots)
		data.lTempEvents = []

def scheduleFlipPopup(iNewPlayer, lPlots):
	data.lTempEvents.append((iNewPlayer, lPlots))
	checkFlipPopup(game.getGameTurn(), active())
	
def flipPopup(iNewPlayer, area):
	flipText = text("TXT_KEY_FLIPMESSAGE1")
	
	for city in getConvertedCities(iNewPlayer, area):
		flipText += city.getName() + "\n"
		
	flipText += text("TXT_KEY_FLIPMESSAGE2")
	
	data.iFlipNewPlayer = iNewPlayer
	data.iFlipOldPlayer = active()
	data.tempArea = area
						
	eventpopup(7615, text("TXT_KEY_NEWCIV_TITLE"), flipText, (text("TXT_KEY_POPUP_YES"), text("TXT_KEY_POPUP_NO")))
	

### Old popup handlers - transition to using Popups module ###

@popup_handler(7615)
def applyFlip(playerID, netUserData, popupReturn):
	iHuman = active()
	area = data.tempArea
	iFlipNewPlayer = data.iFlipNewPlayer
	
	iNumCities = player(iFlipNewPlayer).getNumCities()

	lHumanCityList = [city for city in getConvertedCities(iFlipNewPlayer, area) if city.isHuman()]
	
	if popupReturn.getButtonClicked() == 0:
		message(iHuman, 'TXT_KEY_FLIP_AGREED', color=iGreen)
					
		if lHumanCityList:
			for city in lHumanCityList:
				tCity = (city.getX(), city.getY())
				print ("flipping ", city.getName())
				cultureManager(tCity, 100, iFlipNewPlayer, iHuman, False, False, False)
				flipUnitsInCityBefore(tCity, iFlipNewPlayer, iHuman)
				flipCity(tCity, 0, 0, iFlipNewPlayer, [iHuman])
				flipUnitsInCityAfter(tCity, iFlipNewPlayer)

		#same code as Betrayal - done just once to make sure human player doesn't hold a stack just outside of the cities
		for betrayalPlot in area:
			if betrayalPlot.isCore(betrayalPlot.getOwner()) and not betrayalPlot.isCore(iFlipNewPlayer): 
				continue
			
			for unit in units.at(betrayalPlot).owner(iHuman).domain(DomainTypes.DOMAIN_LAND):
				if rand(100) >= iBetrayalThreshold:
					iUnitType = unit.getUnitType()
					unit.kill(False, iFlipNewPlayer)
					makeUnit(iFlipNewPlayer, iUnitType, (x, y))

		if data.lCheatersCheck[0] == 0:
			data.lCheatersCheck[0] = iCheatersPeriod
			data.lCheatersCheck[1] = data.iFlipNewPlayer
			
	elif popupReturn.getButtonClicked() == 1:
		message(iHuman, 'TXT_KEY_FLIP_REFUSED', color=iGreen)

		for city in lHumanCityList:
			pPlot = plot(city)
			oldCulture = pPlot.getCulture(iHuman)
			pPlot.setCulture(iFlipNewPlayer, oldCulture/2, True)
			pPlot.setCulture(iHuman, oldCulture/2, True)
			data.iSpawnWar += 1
			if data.iSpawnWar == 1:
				team(iFlipNewPlayer).declareWar(iHuman, False, -1) ##True??
				data.iBetrayalTurns = iBetrayalPeriod
				initBetrayal()
	
	
@popup_handler(7622)
def applyRebellion(playerID, netUserData, popupReturn):
	iRebelCiv = data.iRebelCiv
	if popupReturn.getButtonClicked() == 0: # 1st button
		team().makePeace(iRebelCiv)
	elif popupReturn.getButtonClicked() == 1: # 2nd button
		team().declareWar(iRebelCiv, False, -1)


@popup_handler(7625)
def applyColonialAcquisition(playerID, netUserData, popupReturn):
	iPlayer, targets = data.lTempEventList
	if popupReturn.getButtonClicked() == 0:
		for city in targets:
			if city.isHuman():
				colonialAcquisition(iPlayer, city)
				player().changeGold(200)
	elif popupReturn.getButtonClicked() == 1:
		for city in targets:
			if city.isHuman():
				colonialConquest(iPlayer, city)


@popup_handler(7629)
def applyByzantineBribe(playerID, netUserData, popupReturn):
	targetList = data.lByzantineBribes
	iButton = popupReturn.getButtonClicked()
	
	if iButton >= len(targetList): return
	
	iByzantiumPlayer = slot(iByzantium)
	unit, iCost = targetList[iButton]
	closest = closestCity(unit, iByzantiumPlayer)
	
	newUnit = makeUnit(iByzantiumPlayer, unit.getUnitType(), closest)
	player(iByzantiumPlayer).changeGold(-iCost)
	unit.kill(False, iByzantiumPlayer)
	
	if newUnit:
		interface.selectUnit(newUnit, True, True, False)
			

class RiseAndFall:

###############
### Popups ###
#############
				
	def rebellionPopup(self, iRebelCiv):
		eventpopup(7622, text("TXT_KEY_REBELLION_TITLE"), text("TXT_KEY_REBELLION_TEXT", adjective(iRebelCiv)), text("TXT_KEY_POPUP_YES"), text("TXT_KEY_POPUP_NO"))


		

#######################################
### Main methods (Event-Triggered) ###
#####################################  

	def changeAttitudeExtra(self, iPlayer1, iPlayer2, iValue):
		player(iPlayer1).AI_changeAttitudeExtra(iPlayer2, iValue)
		player(iPlayer2).AI_changeAttitudeExtra(iPlayer1, iValue)

	def rebirthFirstTurn(self, iPlayer):
		pPlayer = player(iPlayer)
		pTeam = team(iPlayer)
		iCiv = civ(iPlayer)
		
		# disable Mexico and Colombia
		if iCiv == iAztecs and infos.constant('PLAYER_REBIRTH_MEXICO') == 0: return
		if iCiv == iMaya and infos.constant('PLAYER_REBIRTH_COLOMBIA') == 0: return
		
		if iCiv in dRebirthCiv:
			iCiv = dRebirthCiv[iCiv]
			setCivilization(iPlayer, iCiv)
			
		Modifiers.updateModifiers(iPlayer)
		x, y = dCapitals[iCiv]
		plot = plot_(x, y)
		city = city_(x, y)
		
		# reset contacts and make peace
		for iOtherCiv in players.major().without(iPlayer):
			pTeam.makePeace(iOtherCiv)
			pTeam.cutContact(iOtherCiv)
		
		# reset diplomacy
		pPlayer.AI_reset()
		
		# reset player espionage weights
		player().setEspionageSpendingWeightAgainstTeam(pPlayer.getTeam(), 0)
		
		# reset great people
		pPlayer.resetGreatPeopleCreated()
		
		# reset map visibility
		for plot in plots.all():
			plot.setRevealed(team(iPlayer).getID(), False, False, -1)
		
		# assign new leader
		if iCiv in dRebirthLeaders:
			if pPlayer.getLeader() != dRebirthLeaders[iCiv]:
				pPlayer.setLeader(dRebirthLeaders[iCiv])

		message(active(), 'TXT_KEY_INDEPENDENCE_TEXT', adjective(iPlayer), color=iGreen)

		# assign starting techs
		self.assignTechs(iPlayer)

		# if city present, flip it. Otherwise wait until later
		if city:
			city = completeCityFlip((x, y), iPlayer, city.getOwner(), 100)
				
		# make sure there is a palace in the city
		if city and not city.hasBuilding(iPalace):
			city.setHasRealBuilding(iPalace, True)
		
		self.createRespawnUnits(iPlayer, (x, y))
		
		# for colonial civs, set dynamic state religion
		if iCiv in [iMexico, iColombia]:
			iNewStateReligion = getPrevalentReligion(plots.core(iPlayer), iPlayer)
			
			if iNewStateReligion >= 0:
				player(iPlayer).setLastStateReligion(iNewStateReligion)
		
		if year() >= year(dBirth[active()]):
			startNewCivSwitchEvent(iPlayer)

		player(iPlayer).setInitialBirthTurn(year(dSpawn[iCiv]))

		# adjust gold, civics, religion and other special settings
		if iCiv == iIran:
			pPlayer.setGold(600)
			pPlayer.setLastStateReligion(iIslam)
			pPlayer.setCivics(iCivicsGovernment, iMonarchy)
			pPlayer.setCivics(iCivicsLegitimacy, iVassalage)
			pPlayer.setCivics(iCivicsSociety, iSlavery)
			pPlayer.setCivics(iCivicsEconomy, iMerchantTrade)
			pPlayer.setCivics(iCivicsReligion, iTheocracy)
			
		elif iCiv == iMexico:
			city = city_(18, 37)
			if city:
				if game.getBuildingClassCreatedCount(infos.building(iFloatingGardens).getBuildingClassType()) == 0:
					city.setHasRealBuilding(iFloatingGardens, True)
					
				iStateReligion = pPlayer.getStateReligion()
				if iStateReligion >= 0 and city.isHasReligion(iStateReligion):
					city.setHasRealBuilding(iMonastery + 4 * iStateReligion, True)
			
			cnm.updateCityNamesFound(iPlayer) # use name of the plots in their city name map
			
			pPlayer.setGold(500)
			
			pPlayer.setCivics(iCivicsGovernment, iDespotism)
			pPlayer.setCivics(iCivicsLegitimacy, iConstitution)
			pPlayer.setCivics(iCivicsSociety, iIndividualism)
			pPlayer.setCivics(iCivicsEconomy, iRegulatedTrade)
			pPlayer.setCivics(iCivicsReligion, iClergy)
			pPlayer.setCivics(iCivicsTerritory, iNationhood)
			
		elif iCiv == iColombia:
			pPlayer.setGold(750)
			pPlayer.setCivics(iCivicsGovernment, iDespotism)
			pPlayer.setCivics(iCivicsLegitimacy, iConstitution)
			pPlayer.setCivics(iCivicsSociety, iIndividualism)
			pPlayer.setCivics(iCivicsEconomy, iRegulatedTrade)
			pPlayer.setCivics(iCivicsReligion, iClergy)
			pPlayer.setCivics(iCivicsTerritory, iNationhood)
			plot_(28, 31).setFeatureType(-1, 0)
		
		events.fireEvent("rebirth", iPlayer)

	def rebirthSecondTurn(self, iPlayer):
		iCiv = civ(iPlayer)

		rebirthArea = plots.birth(iCiv)

		# exclude American territory for Mexico
		if iCiv == iMexico:
			rebirthArea = rebirthArea.where(lambda p: not owner(p, iAmerica) or p in plots.core(iCiv))

		rebirthCities = rebirthArea.cities()
			
		# remove garrisons
		for city in rebirthCities.notowner(active()):
			relocateGarrisons(location(city), city.getOwner())
			relocateSeaGarrisons(location(city), city.getOwner())
				
		# convert cities
		iConvertedCities, iHumanCities = convertSurroundingCities(iPlayer, rebirthArea)
		
		# create garrisons
		for city in rebirthCities.owner(active()):
			createGarrisons(location(city), iPlayer, 1)
				
		# convert plot culture
		convertSurroundingPlotCulture(iPlayer, rebirthArea)
		
		# now found capital unless it was already flipped
		x, y = dCapitals[iCiv]
		city = city_(x, y)
		
		if not city:
			if isFree(iPlayer, (x, y), True):
				player(iPlayer).found(x, y)
			else:
				makeUnit(iPlayer, iPlayer, (x, y))
		
		city = city_(x, y)
		if city:
			relocateCapital(iPlayer, (x, y))
		
		# reset plague
		data.players[iPlayer].iPlagueCountdown = -10
		clearPlague(iPlayer)
		
		# adjust starting stability
		data.players[iPlayer].resetStability()
		data.players[iPlayer].iStabilityLevel = iStabilityStable
		if player(iPlayer).isHuman(): data.resetHumanStability()
		
		# ask human player for flips
		if iHumanCities > 0 and not player(iPlayer).isHuman():
			scheduleFlipPopup(iPlayer, rebirthArea)

	def fragmentBarbarians(self, iGameTurn):
		for iDeadPlayer in players.major().shuffle():
			if not player(iDeadPlayer).isAlive() and iGameTurn > year(dBirth[iDeadPlayer]) + turns(50):
				barbarianCities = cities.normal(iDeadPlayer).owner(iBarbarian)
				
				if barbarianCities > 3:
					for iMinor, minorCities in barbarianCities.fraction(2).divide(players.independent()):
						for city in minorCities:
							completeCityFlip(city, iMinor, barbarian(), 50, False, True, True, True)
					
					return

	def secession(self, iGameTurn):
		for iPlayer in players.major().shuffle():
			if player(iPlayer).isAlive() and iGameTurn >= year(dBirth[iPlayer]) + turns(30):
				
				if stability(iPlayer) == iStabilityCollapsing:

					cityList = []
					for city in cities.owner(iPlayer):
						pPlot = plot(city)

						if not city.isWeLoveTheKingDay() and not city.isCapital() and location(city) != location(plots.capital(iPlayer)):
							if player(iPlayer).getNumCities() > 0: #this check is needed, otherwise game crashes
								capital = player(iPlayer).getCapitalCity()
								iDistance = distance(city, capital)
								if iDistance > 3:
							
									if city.angryPopulation(0) > 0 or \
										city.healthRate(False, 0) < 0 or \
										city.getReligionBadHappiness() > 0 or \
										city.getLargestCityHappiness() < 0 or \
										city.getHurryAngerModifier() > 0 or \
										city.getNoMilitaryPercentAnger() > 0 or \
										city.getWarWearinessPercentAnger() > 0:
										cityList.append(city)
										continue
									
									for iLoop in players.all().barbarian():
										if iLoop != iPlayer:
											if pPlot.getCulture(iLoop) > 0:
												cityList.append(city)
												break

					if cityList:
						iNewCiv = iIndependent
						if rand(2) == 1:
							iNewCiv = iIndependent2
						
						if civ(iPlayer) in [iAztecs, iInca, iMaya, iEthiopia, iMali, iCongo]:
							if data.iPlayersWithNationalism == 0:
								iNewCiv = iNative
						
						iNewPlayer = slot(iNewCiv)
						
						splittingCity = random_entry(cityList)
						tPlot = location(splittingCity)
						cultureManager(tPlot, 50, iNewPlayer, iPlayer, False, True, True)
						flipUnitsInCityBefore(tPlot, iNewPlayer, iPlayer)
						flipCity(tPlot, False, False, iNewPlayer, [iPlayer])   #by trade because by conquest may raze the city
						flipUnitsInCityAfter(tPlot, iNewPlayer)
						
						message(iPlayer, '%s %s' % (splittingCity.getName(), text('TXT_KEY_STABILITY_SECESSION')), color=iOrange)
						
					return

	def initBirth(self, iBirthYear, iPlayer): # iBirthYear is really year now, so no conversion prior to function call - edead
		iBirthYear = year(iBirthYear) # converted to turns here - edead
		iCiv = civ(iPlayer)
		
		if iCiv in lSecondaryCivs:
			if not player(iPlayer).isHuman() and not data.isCivEnabled(iCiv):
				return
		
		lConditionalCivs = [iByzantium, iMughals, iOttomans, iThailand, iBrazil, iArgentina, iCanada, iItaly]
		
		# Leoreth: extra checks for conditional civs
		if iCiv in lConditionalCivs and not player(iPlayer).isHuman():
			if iCiv == iByzantium:
				if not player(iRome).isAlive() or player(iGreece).isAlive() or (player(iRome).isHuman() and stability(slot(iRome)) == iStabilitySolid):
					return
					
			elif iCiv == iOttomans:
				if cities.rectangle(*tNearEast).none(lambda city: slot(iTurks) in [city.getOwner(), city.getPreviousOwner()]):
					return

			elif iCiv == iThailand:
				if not player(iKhmer).isHuman():
					if stability(slot(iKhmer)) > iStabilityShaky:
						return
				else:
					if stability(slot(iKhmer)) > iStabilityUnstable:
						return
						
			elif iCiv in [iArgentina, iBrazil]:
				iColonyPlayer = getPlayerWithMostCities(plots.birth(iPlayer))
				if iColonyPlayer < 0: return
				elif civ(iColonyPlayer) not in [iArgentina, iBrazil]:
					if stability(iColonyPlayer) > iStabilityStable:
						return
						
			elif iCiv == iItaly:
				if player(iRome).isAlive():
					return
				
		tCapital = location(plots.capital(iCiv))
				
		x, y = tCapital
		bCapitalSettled = False
		
		if iCiv == iItaly:
			for plot in plots.surrounding(tCapital):
				if plot.isCity():
					bCapitalSettled = True
					tCapital = location(plot)
					x, y = tCapital
					break
					
		if turn() == iBirthYear-1 + data.players[iPlayer].iSpawnDelay + data.players[iPlayer].iFlipsDelay:
			if iCiv in lConditionalCivs or bCapitalSettled:
				convertPlotCulture(plot_(x, y), iPlayer, 100, True)

			tTopLeft, tBottomRight = birthRectangle(iCiv)
			tBroaderTopLeft, tBroaderBottomRight = dBroaderArea[iCiv]
			
			if iCiv == iThailand:
				angkor = cities.capital(iKhmer)
				if angkor:
					bWonder = any(angkor.isHasRealBuilding(iBuilding) for iBuilding in range(iBeginWonders, iNumBuildings))
					if bWonder and not player(iPlayer).isHuman():
						angkor.setName("Ayutthaya", False)
						tCapital = (x-1, y+1)
						x, y = tCapital
						plot_(x, y).setFeatureType(-1, 0)
				
				# Prey Nokor becomes Saigon
				saigon = city(104, 33)
				if saigon:
					saigon.setName("Saigon", False)
				
			iPreviousOwner = plot_(x, y).getOwner()

			if data.players[iPlayer].iFlipsDelay == 0: #city hasn't already been founded)
			
				#this may fix the -1 bug
				if player(iPlayer).isHuman():
					for unit in units.at(x, y).notowner(iPlayer):
						unit.kill(False, -1)
				
				bBirthInCapital = False
				
				if (iCiv in lConditionalCivs and iCiv != iThailand) or bCapitalSettled:
					bBirthInCapital = True
				
				if iCiv == iOttomans:
					self.moveOutInvaders(tTopLeft, tBottomRight)  
					
				if bBirthInCapital:
					makeUnit(iPlayer, iCatapult, (0, 0))
			
				bDeleteEverything = False
				pCapital = plot_(x, y)
				if pCapital.isOwned():
					if player(iPlayer).isHuman() or not player().isAlive():
						if not (pCapital.isCity() and pCapital.getPlotCity().isHolyCity()):
							bDeleteEverything = True
							print ("bDeleteEverything 1")
					else:
						bDeleteEverything = True
						for pPlot in plots.surrounding(tCapital):
							if (pPlot.isCity() and (pPlot.getPlotCity().isHuman() or pPlot.getPlotCity().isHolyCity())) or iCiv == iOttomans:
								bDeleteEverything = False
								print ("bDeleteEverything 2")
								break
				print ("bDeleteEverything", bDeleteEverything)
				if not plot_(x, y).isOwned():
					if iCiv in [iNetherlands, iPortugal, iByzantium, iKorea, iThailand, iItaly, iCarthage]: #dangerous starts
						data.iPrepareCapitalPlayer = iPlayer
					if bBirthInCapital:
						self.birthInCapital(iPlayer, iPreviousOwner, tCapital, tTopLeft, tBottomRight)
					else:
						self.birthInFreeRegion(iPlayer, tCapital, tTopLeft, tBottomRight)
				elif bDeleteEverything and not bBirthInCapital:
					for pCurrent in plots.surrounding(tCapital):
						data.iPrepareCapitalPlayer = iPlayer
						for iLoopPlayer in players.all().without(iPlayer):
							flipUnitsInArea(plots.birth(iCiv), iPlayer, iLoopPlayer, True, False)
						if pCurrent.isCity():
							pCurrent.eraseAIDevelopment()
						for iLoopPlayer in players.all().without(iPlayer):
							pCurrent.setCulture(iLoopPlayer, 0, True)
						pCurrent.setOwner(-1)
					if bBirthInCapital:
						self.birthInCapital(iPlayer, iPreviousOwner, tCapital, tTopLeft, tBottomRight)
					else:
						self.birthInFreeRegion(iPlayer, tCapital, tTopLeft, tBottomRight)
				else:
					if bBirthInCapital:
						self.birthInCapital(iPlayer, iPreviousOwner, tCapital, tTopLeft, tBottomRight)
					else:
						self.birthInForeignBorders(iPlayer, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight)
						
				if bBirthInCapital:	
					clearCatapult(iPlayer)
						
			else:
				self.birthInFreeRegion(iPlayer, tCapital, tTopLeft, tBottomRight)
				
		# Leoreth: reveal all normal plots on spawn
		for plot in plots.normal(iCiv):
			plot.setRevealed(team(iPlayer).getID(), True, False, -1)
				
		# Leoreth: conditional state religion for colonial civs and Byzantium
		if iCiv in [iByzantium, iArgentina, iBrazil]:
			iNewStateReligion = getPrevalentReligion(plots.core(iPlayer), iPlayer)
			
			if iNewStateReligion >= 0:
				player(iPlayer).setLastStateReligion(iNewStateReligion)
			
		if canSwitch(iPlayer, iBirthYear):
			startNewCivSwitchEvent(iPlayer)
			
		data.players[iPlayer].bSpawned = True

	def moveOutInvaders(self, tTL, tBR):
		if player(iMongols).isAlive():
			mongolCapital = player(iMongols).getCapitalCity()
		for plot in plots.start(tTL).end(tBR):
			for unit in units.at(plot):
				if not isDefenderUnit(unit):
					if civ(unit) == iMongols:
						if not player(iMongols).isHuman():
							move(unit, mongolCapital)
					else:
						if unit.getUnitType() == iKeshik:
							unit.kill(False, barbarian())
		
	def birthInFreeRegion(self, iPlayer, tCapital, tTopLeft, tBottomRight):
		startingPlot = plot(tCapital)
		iCiv = civ(iPlayer)
		
		if data.players[iPlayer].iFlipsDelay == 0:
			iFlipsDelay = data.players[iPlayer].iFlipsDelay + 2
			if iFlipsDelay > 0:
				self.createStartingUnits(iPlayer, tCapital)
				
				if iCiv == iOttomans:
					data.iOttomanSpawnTurn = turn()
			
				if iCiv == iItaly:
					removeCoreUnits(iPlayer)
					cityList = cities.core(iPlayer)
					
					rome = cities.capital(iRome)
					if rome:
						cityList.append(rome)
					
					for city in cityList:
						if city.getPopulation() < 5: city.setPopulation(5)
						city.setHasRealBuilding(iGranary, True)
						city.setHasRealBuilding(iLibrary, True)
						city.setHasRealBuilding(iJail, True)
						if city.isCoastal(20): city.setHasRealBuilding(iHarbor, True)
				
				lPlots = plots.surrounding(tCapital, radius=3)
				for iMinor in players.independent().barbarian():
					flipUnitsInArea(lPlots, iPlayer, iMinor, True, player(iMinor).isBarbarian())
				
				self.assignTechs(iPlayer)
				data.players[iPlayer].iPlagueCountdown = -iImmunity
				clearPlague(iPlayer)
				data.players[iPlayer].iFlipsDelay = iFlipsDelay #save
				

		else: #starting units have already been placed, now the second part
		
			iNumCities = player(iPlayer).getNumCities()
		
			area = plots.rectangle(tTopLeft, tBottomRight).without(dBirthAreaExceptions[iPlayer])
			iNumAICitiesConverted, iNumHumanCitiesToConvert = convertSurroundingCities(iPlayer, area)
			convertSurroundingPlotCulture(iPlayer, area)
			for iMinor in players.independent().barbarian():
				flipUnitsInArea(area, iPlayer, iMinor, False, player(iMinor).isBarbarian())
   
			#cover plots revealed by the lion
			clearCatapult(iPlayer)

			if iNumHumanCitiesToConvert > 0 and not player(iPlayer).isHuman(): # Leoreth: quick fix for the "flip your own cities" popup, still need to find out where it comes from
				scheduleFlipPopup(iPlayer, area)

	def birthInForeignBorders(self, iPlayer, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight):
		iCiv = civ(iPlayer)
	
		if iCiv == iItaly:
			removeCoreUnits(iPlayer)
			cityList = cities.core(iPlayer)
			
			rome = cities.capital(iRome)
			if rome:
				cityList.append(rome)
				
			for pCity in cityList:
				if city.getPopulation() < 5: city.setPopulation(5)
				city.setHasRealBuilding(iGranary, True)
				city.setHasRealBuilding(iLibrary, True)
				city.setHasRealBuilding(iJail, True)
				if city.isCoastal(20): city.setHasRealBuilding(iHarbor, True)
				
		iNumCities = player(iPlayer).getNumCities()
		
		area = plots.start(tTopLeft).end(tBottomRight).without(dBirthAreaExceptions[iCiv])
		iNumAICitiesConverted, iNumHumanCitiesToConvert = convertSurroundingCities(iPlayer, area)
		convertSurroundingPlotCulture(iPlayer, area)

		#now starting units must be placed
		if iNumAICitiesConverted > 0:
			plotList = squareSearch(tTopLeft, tBottomRight, ownedCityPlots, iPlayer)
			if plotList:
				tPlot = random_entry(plotList)
				if tPlot:
					self.createStartingUnits(iPlayer, tPlot)
					self.assignTechs(iPlayer)
					data.players[iPlayer].iPlagueCountdown = -iImmunity
					clearPlague(iPlayer)
			
			for iMinor in players.independent().barbarian():
				flipUnitsInArea(area, iPlayer, iMinor, False, player(iMinor).isBarbarian())
			
			if iCiv == iOttomans:
				data.iOttomanSpawnTurn = turn()

		else:   #search another place
			plotList = squareSearch(tTopLeft, tBottomRight, goodPlots, [])
			if plotList:
				tPlot = random_entry(plotList)
				if tPlot:
					self.createStartingUnits(iPlayer, tPlot)
					self.assignTechs(iPlayer)
					data.players[iPlayer].iPlagueCountdown = -iImmunity
					clearPlague(iPlayer)
			else:
				plotList = squareSearch(tBroaderTopLeft, tBroaderBottomRight, goodPlots, [])
			if plotList:
				tPlot = random_entry(plotList)
				if tPlot:
					self.createStartingUnits(iPlayer, tPlot)
					self.assignTechs(iPlayer)
					data.players[iPlayer].iPlagueCountdown = -iImmunity
					clearPlague(iPlayer)
			
			for iMinor in players.independent().barbarian():
				flipUnitsInArea(area, iPlayer, iMinor, True, player(iPlayer).isBarbarian())

		if iNumHumanCitiesToConvert > 0:
			scheduleFlipPopup(iPlayer, area)

	#Leoreth - adapted from SoI's birthConditional method by embryodead
	def birthInCapital(self, iPlayer, iPreviousOwner, tCapital, tTopLeft, tBottomRight):
		iOwner = iPreviousOwner
		iCiv = civ(iPlayer)
		
		x, y = tCapital
		capital = city(x, y)

		if data.players[iPlayer].iFlipsDelay == 0:

			iFlipsDelay = data.players[iPlayer].iFlipsDelay + 2

			if iFlipsDelay > 0:
			
				# flip capital instead of spawning starting units
				if capital:
					capital = flipCity(capital, False, True, iPlayer, ())
					capital.setHasRealBuilding(iPalace, True)
					convertPlotCulture(plot_(capital), iPlayer, 100, True)
					convertSurroundingPlotCulture(iPlayer, plots.surrounding(capital))
				
				#cover plots revealed
				for plot in plots.surrounding((0, 0), radius=2):
					plot.setRevealed(team(iPlayer).getID(), False, False, -1)

				self.createStartingUnits(iPlayer, tCapital)

				data.players[iPlayer].iPlagueCountdown
				clearPlague(iPlayer)

				area = plots.start(tTopLeft).end(tBottomRight)
				for iMinor in players.independent().barbarian():
					flipUnitsInArea(area, iPlayer, iMinor, True, player(iMinor).isBarbarian())
				
				self.assignTechs(iPlayer)
				
				data.players[iPlayer].iFlipsDelay = iFlipsDelay #save

				# kill the catapult and cover the plots
				clearCatapult(iPlayer)
				
				convertPlotCulture(plot_(x, y), iPlayer, 100, True)
				
				# notify dynamic names
				if capital:
					events.fireEvent("cityAcquired", iOwner, iPlayer, capital, False, True)

		else: # starting units have already been placed, now to the second part
			area = plots.start(tTopLeft).end(tBottomRight).without(dBirthAreaExceptions[iCiv])
			iNumAICitiesConverted, iNumHumanCitiesToConvert = convertSurroundingCities(iPlayer, area)
			convertSurroundingPlotCulture(iPlayer, area)
				
			for iMinorCiv in [iIndependent, iIndependent2, iBarbarian]:
				flipUnitsInArea(area, iPlayer, slot(iMinorCiv), False, True) #remaining barbs/indeps in the region now belong to the new civ   
			
			# kill the catapult and cover the plots
			clearCatapult(iPlayer)
				
			# convert human cities
			if iNumHumanCitiesToConvert > 0:
				scheduleFlipPopup(iPlayer, area)
				
			convertPlotCulture(plot(x, y), iPlayer, 100, True)

	# TODO: move to Core
	def findSeaPlots(self, tCoords, iRange, iCiv):
		"""Searches a sea plot that isn't occupied by a unit and isn't a civ's territory surrounding the starting coordinates"""
		return plots.surrounding(tCoords, radius=iRange).water().where(lambda p: not p.isUnit()).where(lambda p: p.getOwner() in [-1, slot(iCiv)]).random()

	def startWarsOnSpawn(self, iPlayer):
		pPlayer = player(iPlayer)
		pTeam = team(iPlayer)
		iCiv = civ(iPlayer)
		
		iMin = 10
		
		if rand(100) >= iMin:
			for iLoopCiv in dEnemyCivsOnSpawn[iCiv]:
				iLoopPlayer = slot(iLoopCiv)
			
				if team(iLoopPlayer).isAVassal(): continue
				if not player(iLoopPlayer).isAlive(): continue
				if pTeam.isAtWar(iLoopPlayer): continue
				if player(iPlayer).isHuman() and iLoopCiv not in dTotalWarOnSpawn[iCiv]: continue
				
				iLoopMin = 50
				if is_minor(iLoopPlayer): iLoopMin = 30
				if player(iLoopPlayer).isHuman(): iLoopMin += 10
				
				if rand(100) >= iLoopMin:
					iWarPlan = -1
					if iLoopCiv in dTotalWarOnSpawn[iCiv]:
						iWarPlan = WarPlanTypes.WARPLAN_TOTAL
					pTeam.declareWar(iLoopPlayer, False, iWarPlan)
					
					if pPlayer.isHuman(): data.iBetrayalTurns = 0

	def initMinorBetrayal(self, iPlayer):
		birthArea = plots.birth(iPlayer)
		plotList = listSearch(birthArea, outerInvasion, [])
		if plotList:
			tPlot = random_entry(plotList)
			if tPlot:
				createAdditionalUnits(iPlayer, tPlot)
				self.unitsBetrayal(iPlayer, active(), lPlots, tPlot)

	def unitsBetrayal(self, iNewOwner, iOldOwner, lPlots, tPlot):
		message(data.iFlipOldPlayer, 'TXT_KEY_FLIP_BETRAYAL', color=iGreen)
		message(data.iFlipNewPlayer, 'TXT_KEY_FLIP_BETRAYAL_NEW', color=iGreen)
		
		for x, y in lPlots:
			for unit in units.at(x, y).owner(iOldOwner).domain(DomainTypes.DOMAIN_LAND):
				if rand(100) >= iBetrayalThreshold:
					iUnitType = unit.getUnitType()
					unit.kill(False, iNewOwner)
					makeUnit(iNewOwner, iUnitType, tPlot)

	def createStartingUnits(self, iPlayer, tPlot):
		iCiv = civ(iPlayer)
	
		if iCiv == iChina:
			createSettlers(iPlayer, 1)
			makeUnit(iPlayer, iArcher, tPlot)
			makeUnit(iPlayer, iMilitia, tPlot)
		elif iCiv == iIndia:
			createSettlers(iPlayer, 1)
			makeUnit(iPlayer, iArcher, tPlot)
			makeUnit(iPlayer, iSpearman, tPlot)
			makeUnit(iPlayer, iLightSwordsman, tPlot)
			makeUnit(iPlayer, iChariot, tPlot)
		elif iCiv == iGreece:
			createSettlers(iPlayer, 1)
			makeUnits(iPlayer, iMilitia, tPlot, 2)
			makeUnit(iPlayer, iHoplite, tPlot)
			makeUnit(iPlayer, iHoplite, tPlot, UnitAITypes.UNITAI_ATTACK)
			makeUnit(iPlayer, iHoplite, tPlot, UnitAITypes.UNITAI_ATTACK_CITY)
			
			tSeaPlot = findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
				makeUnit(iPlayer, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iMilitia, tSeaPlot)
		elif iCiv == iPersia:
			createSettlers(iPlayer, 3)
			makeUnits(iPlayer, iArcher, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iImmortal, tPlot, 4)
			makeUnits(iPlayer, iHorseman, tPlot, 2)
			makeUnit(iPlayer, iWarElephant, tPlot)
		elif iCiv == iCarthage:
			createSettlers(iPlayer, 1)
			makeUnit(iPlayer, iArcher, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnit(iPlayer, iSacredBand, tPlot)
			
			tSeaPlot = findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iWorkboat, tSeaPlot, 2)
				makeUnit(iPlayer, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iArcher, tSeaPlot)
				makeUnit(iPlayer, iGalley, tSeaPlot, UnitAITypes.UNITAI_ASSAULT_SEA)
				makeUnit(iPlayer, iWarGalley, tSeaPlot, UnitAITypes.UNITAI_ESCORT_SEA)
		elif iCiv == iPolynesia:
			tSeaPlot = (4, 19)
			makeUnit(iPlayer, iSettler, tPlot)
			makeUnit(iPlayer, iWaka, tSeaPlot)
			makeUnit(iPlayer, iSettler, tSeaPlot)
			makeUnit(iPlayer, iWorkboat, tSeaPlot)
		elif iCiv == iRome:
			createSettlers(iPlayer, 4)
			makeUnits(iPlayer, iArcher, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iLegion, tPlot, 4)
			
			tSeaPlot = findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
				makeUnits(iPlayer, iGalley, tSeaPlot, 2, UnitAITypes.UNITAI_ASSAULT_SEA)
		elif iCiv == iMaya:
			createSettlers(iPlayer, 1)
			makeUnits(iPlayer, iHolkan, tPlot, 2)
		elif iCiv == iJapan:
			createSettlers(iPlayer, 3)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iSwordsman, tPlot, 2)
			makeUnits(iPlayer, iArcher, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
				
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iCrossbowman, tPlot, 2)
				makeUnits(iPlayer, iSamurai, tPlot, 3)
			
			tSeaPlot = findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iWorkboat, tSeaPlot, 2)
		elif iCiv == iTamils:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnit(iPlayer, iArcher, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnit(iPlayer, iWarElephant, tPlot)
			makeUnits(iPlayer, iSwordsman, tPlot, 2)
			
			if not player(iPlayer).isHuman():
				makeUnit(iPlayer, iHinduMissionary, tPlot)
				makeUnit(iPlayer, iWarElephant, tPlot)
				
			tSeaPlot = findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
				makeUnit(iPlayer, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iWarGalley, tSeaPlot)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iArcher, tSeaPlot)
		elif iCiv == iEthiopia:
			createSettlers(iPlayer, 2)
			makeUnits(iPlayer, iArcher, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnit(iPlayer, iShotelai, tPlot)
			makeUnit(iPlayer, iLightSwordsman, tPlot)
			
			tSeaPlot = (74, 29)
			makeUnit(iPlayer, iWorkboat, tSeaPlot)
			makeUnit(iPlayer, iWarGalley, tSeaPlot)
		elif iCiv == iKorea:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iArcher, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnit(iPlayer, iSwordsman, tPlot)
			makeUnit(iPlayer, iHorseman, tPlot)
			
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iSpearman, tPlot, 2)
				makeUnits(iPlayer, iCrossbowman, tPlot, 2)
		elif iCiv == iByzantium:
			createSettlers(iPlayer, 4)
			createMissionaries(iPlayer, 1)
			
			makeUnits(iPlayer, iLegion, tPlot, 4)
			makeUnits(iPlayer, iSpearman, tPlot, 2)
			makeUnits(iPlayer, iArcher, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
			
			tSeaPlot = findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iGalley, tSeaPlot, 2)
				makeUnits(iPlayer, iWarGalley, tSeaPlot, 2)
				if scenario() == i3000BC:
					makeUnit(iPlayer, iWorkboat, tSeaPlot)
		elif iCiv == iVikings:
			createSettlers(iPlayer, 2)
			makeUnits(iPlayer, iArcher, tPlot, 4, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iHuscarl, tPlot, 3)
			makeUnit(iPlayer, iScout, tPlot)
			
			tSeaPlot = findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
				makeUnit(iPlayer, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iArcher, tSeaPlot)
				makeUnits(iPlayer, iLongship, tSeaPlot, 2, UnitAITypes.UNITAI_EXPLORE_SEA)
		elif iCiv == iTurks:
			createSettlers(iPlayer, 6)
			if player(iPlayer).isHuman():
				makeUnits(iPlayer, iArcher, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			else:
				makeUnits(iPlayer, iCrossbowman, tPlot, 4, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iOghuz, tPlot, 6)
			makeUnit(iPlayer, iScout, tPlot)
		elif iCiv == iArabia:
			createSettlers(iPlayer, 2)
			makeUnit(iPlayer, iArcher, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iMobileGuard, tPlot, 2)
			makeUnits(iPlayer, iGhazi, tPlot, 2)
			makeUnit(iPlayer, iWorker, tPlot)
			
			tSeaPlot = findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
		elif iCiv == iTibet:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iArcher, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iKhampa, tPlot, 2)
		elif iCiv == iKhmer:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			createMissionaries(iPlayer, 1, iBuddhism)
			makeUnit(iPlayer, iArcher, tPlot, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iBallistaElephant, tPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
			
			tSeaPlot = findSeaPlots(tPlot, 2, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
				makeUnit(iPlayer, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iArcher, tSeaPlot)
		elif iCiv == iIndonesia:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnit(iPlayer, iArcher, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			
			tSeaPlot = findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
				makeUnit(iPlayer, iWarGalley, tSeaPlot)
				makeUnits(iPlayer, iGalley, tSeaPlot, 2, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iArcher, tSeaPlot)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iArcher, tSeaPlot)
		elif iCiv == iMoors:
			createSettlers(iPlayer, 2)
			createMissionaries(iPlayer, 2)
			makeUnit(iPlayer, iCrossbowman, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iSwordsman, tPlot, 2)
			makeUnits(iPlayer, iSpearman, tPlot, 2)
			makeUnits(iPlayer, iHorseArcher, tPlot, 2)
			
			tSeaPlot = findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iGalley, tSeaPlot)
				makeUnit(iPlayer, iHeavyGalley, tSeaPlot)
				makeUnit(iPlayer, iWorkboat, tSeaPlot)
			
			if civ() in [iSpain, iMoors]:
				makeUnit(iPlayer, iCrossbowman, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
		elif iCiv == iSpain:
			iSpanishSettlers = 2
			if not player(iPlayer).isHuman(): iSpanishSettlers = 3
			createSettlers(iPlayer, iSpanishSettlers)
			createMissionaries(iPlayer, 1)
			makeUnit(iPlayer, iCrossbowman, tPlot)
			makeUnit(iPlayer, iCrossbowman, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iSwordsman, tPlot, 4)
			
			if data.isCivEnabled(iMoors):
				if not player(iMoors).isHuman():
					makeUnits(iPlayer, iLancer, tPlot, 2)
			else:
				makeUnit(iPlayer, iSettler, tPlot)
				
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iCrossbowman, tPlot, 2)
				
			if scenario() == i600AD: #late start condition
				makeUnit(iPlayer, iWorker, tPlot) #there is no carthaginian city in Iberia and Portugal may found 2 cities otherwise (a settler is too much)
		elif iCiv == iFrance:
			createSettlers(iPlayer, 3)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iCrossbowman, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iHeavySpearman, tPlot, 2)
			makeUnits(iPlayer, iSwordsman, tPlot, 3)
		elif iCiv == iEngland:
			createSettlers(iPlayer, 3)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iCrossbowman, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iHeavySwordsman, tPlot, 2)
				
			tSeaPlot = findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iWorkboat, tSeaPlot, 2)
				makeUnit(iPlayer, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tPlot)
				makeUnit(iPlayer, iCrossbowman, tPlot)
				makeUnits(iPlayer, iGalley, tPlot, 2)
		elif iCiv == iHolyRome:
			createSettlers(iPlayer, 3)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iCrossbowman, tPlot, 3, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iSwordsman, tPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iLancer, tPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iCatapult, tPlot, 4, UnitAITypes.UNITAI_ATTACK_CITY)
		elif iCiv == iRussia:
			createSettlers(iPlayer, 4)
			makeUnits(iPlayer, iCrossbowman, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iHorseArcher, tPlot, 4)
		elif iCiv == iNetherlands:
			createSettlers(iPlayer, 2)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iArquebusier, tPlot, 6)
			makeUnits(iPlayer, iBombard, tPlot, 2)
			makeUnits(iPlayer, iPikeman, tPlot, 2)
			
			tSeaPlot = findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iWorkboat, tSeaPlot, 2)
				makeUnit(iPlayer, iEastIndiaman, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iCrossbowman, tSeaPlot)
				makeUnit(iPlayer, iEastIndiaman, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iCrossbowman, tSeaPlot)
				makeUnits(iPlayer, iCaravel, tSeaPlot, 2)
		elif iCiv == iMali:
			createSettlers(iPlayer, 3)
			createMissionaries(iPlayer, 2)
			makeUnits(iPlayer, iKelebolo, tPlot, 5)
		elif iCiv == iPoland:
			iNumSettlers = 1
			if player(iPlayer).isHuman(): iNumSettlers = 2
			createSettlers(iPlayer, iNumSettlers)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iCrossbowman, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iHeavySwordsman, tPlot, 2)
			makeUnits(iPlayer, iLancer, tPlot, 2)
			
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iHeavySpearman, tPlot, 2)
		elif iCiv == iOttomans:
			createMissionaries(iPlayer, 3)
			makeUnits(iPlayer, iHeavySwordsman, tPlot, 2)
			makeUnits(iPlayer, iCrossbowman, tPlot, 2)
			makeUnits(iPlayer, iLancer, tPlot, 3)
			makeUnits(iPlayer, iJanissary, tPlot, 2)
			makeUnits(iPlayer, iGreatBombard, tPlot, 2)
			makeUnits(iPlayer, iTrebuchet, tPlot, 2)
			
			if player(iPlayer).isHuman():
				makeUnits(iPlayer, iGreatBombard, tPlot, 4)
				makeUnits(iPlayer, iJanissary, tPlot, 5)
				makeUnits(iPlayer, iLancer, tPlot, 4)
		elif iCiv == iPortugal:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iCrossbowman, tPlot, 4, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPlayer, iHeavySpearman, tPlot, 2)
			
			tSeaPlot = findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iWorkboat, tSeaPlot, 2)
				makeUnit(iPlayer, iCog, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot)
				makeUnit(iPlayer, iCrossbowman, tSeaPlot)
				makeUnit(iPlayer, iHeavyGalley, tSeaPlot, UnitAITypes.UNITAI_EXPLORE_SEA)
		elif iCiv == iInca:
			createSettlers(iPlayer, 1)
			makeUnits(iPlayer, iAucac, tPlot, 4)
			makeUnits(iPlayer, iArcher, tPlot, 2)
			
			if not player(iPlayer).isHuman():
				makeUnit(iPlayer, iSettler, tPlot)
		elif iCiv == iItaly:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iBalestriere, tPlot, 3)
			makeUnits(iPlayer, iHeavySpearman, tPlot, 2)
			makeUnits(iPlayer, iTrebuchet, tPlot, 3)
			
			tSeaPlot = findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iWorkboat, tSeaPlot, 2)
				makeUnit(iPlayer, iCog, tSeaPlot)
				makeUnit(iPlayer, iHeavyGalley, tSeaPlot)
		elif iCiv == iMongols:
			createSettlers(iPlayer, 3)
			makeUnits(iPlayer, iCrossbowman, tPlot, 3)
			makeUnits(iPlayer, iHeavySwordsman, tPlot, 2)
			makeUnits(iPlayer, iMangudai, tPlot, 2)
			makeUnits(iPlayer, iKeshik, tPlot, 6, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iBombard, tPlot, 3)
			
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iKeshik, tPlot, 10, UnitAITypes.UNITAI_ATTACK_CITY)
				makeUnits(iPlayer, iBombard, tPlot, 5, UnitAITypes.UNITAI_ATTACK_CITY)
				makeUnits(iPlayer, iHeavySwordsman, tPlot, 2, UnitAITypes.UNITAI_COUNTER)
				makeUnits(iPlayer, iScout, tPlot, 2, UnitAITypes.UNITAI_EXPLORE)
				makeUnits(iPlayer, iCrossbowman, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
		elif iCiv == iAztecs:
			createSettlers(iPlayer, 2)
			makeUnits(iPlayer, iJaguar, tPlot, 4)
			makeUnits(iPlayer, iArcher, tPlot, 4, UnitAITypes.UNITAI_CITY_DEFENSE)
		elif iCiv == iMughals:
			createSettlers(iPlayer, 3)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iSiegeElephant, tPlot, 3)
			makeUnits(iPlayer, iHeavySwordsman, tPlot, 4).experience(2)
			makeUnits(iPlayer, iHorseArcher, tPlot, 2)
			
			if player(iPlayer).isHuman():
				makeUnits(iPlayer, iIslamicMissionary, tPlot, 3)
		elif iCiv == iThailand:
			createSettlers(iPlayer, 1)
			createMissionaries(iPlayer, 1)
			makeUnits(iPlayer, iHeavySpearman, tPlot, 3)
			makeUnits(iPlayer, iChangSuek, tPlot, 2)
		elif iCiv == iCongo:
			createSettlers(iPlayer, 1)
			makeUnits(iPlayer, iArcher, tPlot, 2)
			makeUnits(iPlayer, iPombos, tPlot, 2)
		elif iCiv == iGermany:
			createSettlers(iPlayer, 4)
			createMissionaries(iPlayer, 2)
			makeUnits(iPlayer, iArquebusier, tPlot, 3).experience(2)
			makeUnits(iPlayer, iArquebusier, tPlot, 2, UnitAITypes.UNITAI_CITY_DEFENSE).experience(2)
			makeUnits(iPlayer, iBombard, tPlot, 3).experience(2)
			
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iArquebusier, tPlot, 10).experience(2)
				makeUnits(iPlayer, iBombard, tPlot, 5).experience(2)
		elif iCiv == iAmerica:
			createSettlers(iPlayer, 8)
			makeUnits(iPlayer, iGrenadier, tPlot, 2)
			makeUnits(iPlayer, iMinuteman, tPlot, 4)
			makeUnits(iPlayer, iCannon, tPlot, 2)
			
			tSeaPlot = findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iWorkboat, tSeaPlot, 2)
				makeUnits(iPlayer, iGalleon, tSeaPlot, 2)
				makeUnit(iPlayer, iFrigate, tSeaPlot)
				
			if not player(iPlayer).isHuman():
				makeUnit(iPlayer, iMinuteman, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
				
			iReligion = self.findAreaReligion(iPlayer, plots.start(23, 40).end(33, 52))
			if iReligion >= 0:
				player(iPlayer).setLastStateReligion(iReligion)
				makeUnit(iPlayer, missionary(iReligion), tPlot)
		elif iCiv == iArgentina:
			createSettlers(iPlayer, 2)
			makeUnits(iPlayer, iMusketeer, tPlot, 3).experience(2)
			makeUnits(iPlayer, iGrenadierCavalry, tPlot, 3).experience(2)
			makeUnits(iPlayer, iCannon, tPlot, 2).experience(2)
			
			tSeaPlot = findSeaPlots(tPlot, 2, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iGalleon, tSeaPlot)
				makeUnits(iPlayer, iFrigate, tSeaPlot, 2)
				
			if not player(iPlayer).isHuman():
				makeUnit(iPlayer, iMusketeer, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
				makeUnits(iPlayer, iMusketeer, tPlot, 2).experience(2)
				makeUnits(iPlayer, iGrenadierCavalry, tPlot, 2).experience(2)
				makeUnits(iPlayer, iCannon, tPlot, 2).experience(2)
		elif iCiv == iBrazil:
			createSettlers(iPlayer, 5)
			makeUnits(iPlayer, iGrenadier, tPlot, 3)
			makeUnits(iPlayer, iMusketeer, tPlot, 3)
			makeUnits(iPlayer, iCannon, tPlot, 2)
			
			tSeaPlot = findSeaPlots(tPlot, 1, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iWorkboat, tSeaPlot, 2)
				makeUnits(iPlayer, iGalleon, tSeaPlot, 2)
				makeUnits(iPlayer, iFrigate, tSeaPlot, 3)
				
			if not player(iPlayer).isHuman():
				makeUnit(iPlayer, iRifleman, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE)
		elif iCiv == iCanada:
			createSettlers(iPlayer, 5)
			makeUnits(iPlayer, iDragoon, tPlot, 3)
			makeUnits(iPlayer, iRifleman, tPlot, 5)
			
			tSeaPlot = findSeaPlots(tPlot, 2, iCiv)
			if tSeaPlot:
				makeUnits(iPlayer, iSteamship, tSeaPlot, 2)
				makeUnit(iPlayer, iIronclad, tSeaPlot)
				makeUnit(iPlayer, iTorpedoBoat, tSeaPlot)
		
		events.fireEvent("birth", iPlayer)		
				
		# Leoreth: start wars on spawn when the spawn actually happens
		self.startWarsOnSpawn(iPlayer)

	def createRespawnUnits(self, iPlayer, tPlot):
		iCiv = civ(iPlayer)
	
		if iCiv == iIran:
			makeUnits(iPlayer, iQizilbash, tPlot, 6)
			makeUnits(iPlayer, iBombard, tPlot, 3)
			makeUnits(iPlayer, iWorker, tPlot, 3)
			
			if not player(iPlayer).isHuman():
				makeUnits(iPlayer, iQizilbash, tPlot, 6)
				makeUnits(iPlayer, iBombard, tPlot, 3)
		elif iCiv == iMexico:
			makeUnits(iPlayer, iDragoon, tPlot, 4).experience(2)
			makeUnits(iPlayer, iMusketeer, tPlot, 5).experience(2)
			makeUnits(iPlayer, iGrenadier, tPlot, 2).experience(2)
			makeUnits(iPlayer, iWorker, tPlot, 2)
		elif iCiv == iColombia:
			makeUnits(iPlayer, iMusketeer, tPlot, 5).experience(2)
			makeUnits(iPlayer, iCannon, tPlot, 5).experience(2)
			makeUnits(iPlayer, iAlbionLegion, tPlot, 5).experience(2)
			makeUnits(iPlayer, iWorker, tPlot, 3)
			
			tSeaPlot = findSeaPlots(tPlot, 3, iCiv)
			if tSeaPlot:
				makeUnit(iPlayer, iGalleon, tSeaPlot)
				makeUnit(iPlayer, iFrigate, tSeaPlot)
				
	def findAreaReligion(self, iPlayer, area):
		lReligions = [0 for i in range(iNumReligions)]
		
		for plot in area:
			if plot.isCity():
				city = plot.getPlotCity()
				iOwner = city.getOwner()
				if iOwner != iPlayer:
					for iReligion in range(iNumReligions):
						if city.isHasReligion(iReligion):
							lReligions[iReligion] += 1
					iStateReligion = player(iOwner).getStateReligion()
					if iStateReligion >= 0:
						lReligions[iStateReligion] += 1
						
		iMax = 0
		iHighestReligion = -1
		for i in range(iNumReligions):
			iLoopReligion = (iProtestantism + i) % iNumReligions
			if lReligions[iLoopReligion] > iMax:
				iMax = lReligions[iLoopReligion]
				iHighestReligion = iLoopReligion
				
		return iHighestReligion

	def assignTechs(self, iPlayer):
		Civilizations.initPlayerTechs(iPlayer)

	def determineEnabledPlayers(self):
		iRand = infos.constant('PLAYER_OCCURRENCE_POLYNESIA')
		if iRand <= 0:
			data.setCivEnabled(iPolynesia, False)
		elif rand(iRand) != 0:
			data.setCivEnabled(iPolynesia, False)
			
		iRand = infos.constant('PLAYER_OCCURRENCE_HARAPPA')
		if iRand <= 0:
			data.setCivEnabled(iHarappa, False)
		elif rand(iRand) != 0:
			data.setCivEnabled(iHarappa, False)
		
		if not player(iIndia).isHuman() and not player(iIndonesia).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_TAMILS')
			
			if iRand <= 0:
				data.setCivPlayerEnabled(iTamils, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iTamils, False)
				
		if not player(iChina).isHuman() and not player(iIndia).isHuman() and not player(iMughals).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_TIBET')
			
			if iRand <= 0:
				data.setCivEnabled(iTibet, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iTibet, False)
				
		if not player(iSpain).isHuman() and not player(iMali).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_MOORS')
			
			if iRand <= 0:
				data.setCivEnabled(iMoors, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iMoors, False)
				
		if not player(iHolyRome).isHuman() and not player(iGermany).isHuman() and not player(iRussia).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_POLAND')
			
			if iRand <= 0:
				data.setCivEnabled(iPoland, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iPoland, False)
				
		if not player(iMali).isHuman() and not player(iPortugal).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_CONGO')
			
			if iRand <= 0:
				data.setCivEnabled(iCongo, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iCongo, False)
				
		if not player(iSpain).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_ARGENTINA')
			
			if iRand <= 0:
				data.setCivEnabled(iArgentina, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iArgentina, False)
				
		if not player(iPortugal).isHuman():
			iRand = infos.constant('PLAYER_OCCURRENCE_BRAZIL')
			
			if iRand <= 0:
				data.setCivEnabled(iBrazil, False)
			elif rand(iRand) != 0:
				data.setCivEnabled(iBrazil, False)
			
rnf = RiseAndFall()