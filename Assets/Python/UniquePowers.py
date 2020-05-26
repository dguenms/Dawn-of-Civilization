from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
from StoredData import data # edead
from Consts import *
from RFCUtils import *
from operator import itemgetter
from Events import handler

from Core import *

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

### Constants ###

tRussianTopLeft = (65, 49)
tRussianBottomRight = (121, 65)

iMongolianRadius = 4
iMongolianTimer = 1


@handler("GameStart")
def setup():
	# Babylonian UP: receive a free tech after discovering the first five techs
	player(iBabylonia).setFreeTechsOnDiscovery(5)

@handler("cityAcquired")
def arabianUP(iOwner, iPlayer, city):
	if civ(iPlayer) != iArabia:
		return

	iStateReligion = player(iArabia).getStateReligion()

	if iStateReligion >= 0:
		if not city.isHasReligion(iStateReligion):
			city.setHasReligion(iStateReligion, True, True, False)
		if not city.hasBuilding(iTemple + iStateReligion*4):
			city.setHasRealBuilding((iTemple + iStateReligion*4), True)

@handler("cityAcquired")
def mongolUP(iOwner, iPlayer, city, bConquest):
	if civ(iPlayer) != iMongols:
		return
	
	if not bConquest:
		return
		
	if player(iPlayer).isHuman():
		return

	if city.getPopulation() >= 7:
		makeUnits(iMongols, iKeshik, city, 2, UnitAITypes.UNITAI_ATTACK_CITY)
	elif city.getPopulation() >= 4:
		makeUnit(iMongols, iKeshik, city, UnitAITypes.UNITAI_ATTACK_CITY)

	if city.getPopulation() >= 4:
		message(slot(iMongols), 'TXT_KEY_UP_MONGOL_HORDE')

@handler("cityBuilt")
def ottomanUP(city):
	iOwner = city.getOwner()
	for plot in plots.surrounding(city, radius=2):
		if at(plot, city):
			convertPlotCulture(plot, iOwner, 51, False)
		elif plot.isCity():
			continue
		elif distance(plot, city) == 1:
			convertPlotCulture(plot, iOwner, 80, True)
		else:
			if plot.getOwner() == city.getPreviousOwner():
				convertPlotCulture(plot, iOwner, 20, False)

@handler("combatResult")
def vikingUP(winningUnit, losingUnit):
	iWinner = winningUnit.getOwner()
	if (civ(iWinner) == iVikings and year() <= year(1500)) or winningUnit.getUnitType() == iCorsair:
		if infos.unit(losingUnit).getDomainType() == DomainTypes.DOMAIN_SEA:
			iGold = scale(infos.unit(losingUnit).getProductionCost() / 2)
			player(iWinner).changeGold(iGold)
			message(iWinner, 'TXT_KEY_VIKING_NAVAL_UP', iGold, adjective(losingUnit), losingUnit.getName())
			
			if civ(iWinner) == iVikings:
				data.iVikingGold += iGold
			elif civ(iWinner) == iMoors:
				data.iMoorishGold += iGold


# Mughal UP: receives 50% of building cost as culture when building is completed
@handler("buildingBuilt")
def mughalUP(city, iBuilding):
	if civ(city) == iMughals:
		iCost = player(city).getBuildingProductionNeeded(iBuilding)
		city.changeCulture(city.getOwner(), iCost / 2, True)

# Russian UP: enemy units are damaged every turn while being in the Russia region
@handler("BeginGameTurn")
def russianUP(self):
	if player(iRussia).isAlive():
		for unit in plots.rectangle(tRussianTopLeft, tRussianBottomRight).owner(iRussia).units():
			if team(iRussia).isAtWar(unit.getOwner()):
				unit.changeDamage(8, slot(iRussia))
			
# Indonesian UP: additional gold for foreign ships in your core
@handler("BeginGameTurn")
def indonesianUP():
	if not player(iIndonesia).isAlive():
		return

	seaUnits = plots.core(iIndonesia).owner(iIndonesia).units().domain(DomainTypes.DOMAIN_SEA)
	iNumUnits = seaUnits.notowner(iIndonesia).where(lambda unit: not team(iIndonesia).isAtWar(unit.getTeam())).count()
				
	if iNumUnits > 0:
		iGold = 5 * iNumUnits
		player(iIndonesia).changeGold(iGold)
		message(slot(iIndonesia), 'TXT_KEY_INDONESIAN_UP', iGold)
		
@handler("BeginGameTurn")
def resetBabylonianPower():
	data.bBabyloniaTechReceived = False


@handler("cityAcquired")
def colombianPower(iOwner, iPlayer, city, bConquest):
	if civ(iPlayer) == iColombia and bConquest:
		if city in cities.rectangle(tSouthCentralAmericaTL, tSouthCentralAmericaBR):
			city.setOccupationTimer(0)


@handler("techAcquired")
def mayanPower(iTech, iTeam, iPlayer):
	iEra = infos.tech(iTech).getEra()
	if civ(iPlayer) == iMaya and iEra < iMedieval:
		iNumCities = player(iPlayer).getNumCities()
		if iNumCities > 0:
			iFood = 20 / iNumCities
			for city in cities.owner(iPlayer):
				city.changeFood(iFood)
			message(iPlayer, 'TXT_KEY_MAYA_UP_EFFECT', infos.tech(iTech).getText(), iFood)


@handler("changeWar")
def resetMongolPower(bWar, iTeam, iOtherTeam):
	if not bWar and iMongols in civs(iTeam, iOtherTeam):
		for city in cities.owner(iMongols):
			city.setMongolUP(False)


# TODO: add handler for custom event here
def canadianUP(city):
	iPopulation = 5 * city.getPopulation() / 2
	
	lSpecialists = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman]
	lProgress = [city.getGreatPeopleUnitProgress(unique_unit(city.getOwner(), iSpecialist)) for iSpecialist in lSpecialists]
	bAllZero = all(x <= 0 for x in lProgress)
		
	if bAllZero:
		iGreatPerson = random_entry(lSpecialists)
	else:
		iGreatPerson = find_max(lProgress).index + iGreatProphet
		
	iGreatPerson = unique_unit(city.getOwner(), iGreatPerson)
	
	city.changeGreatPeopleProgress(iPopulation)
	city.changeGreatPeopleUnitProgress(iGreatPerson, iPopulation)
	
	message(city.getOwner(), 'TXT_KEY_UP_MULTICULTURALISM', city.getName(), infos.unit(iGreatPerson).getText(), iPopulation, event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.unit(iGreatPerson).getButton(), color=iGreen, location=city)


class UniquePowers:

#######################################
### Main methods (Event-Triggered) ###
#####################################  


		
	def onBuildingBuilt(self, city, iOwner, iBuilding):
		if civ(iOwner) == iMughals:
			self.mughalUP(city, iBuilding)
					
#------------------VIKING UP----------------------

#------------------ARABIAN U.P.-------------------

#------------------AZTEC U.P.-------------------

	def aztecUP(self, argsList): #Real Slavery by Sevo
		if not player(iAztecs).isAlive(): return
		
		pWinningUnit, pLosingUnit = argsList
		
		iWinningPlayer = pWinningUnit.getOwner()
		pWinningPlayer = player(iWinningPlayer)
		
		iLosingPlayer = pLosingUnit.getOwner()
		iLosingUnit = pLosingUnit.getUnitType()
		
		if civ(iWinningPlayer) != iAztecs:
			return

		# Only enslave land units!!
		if pLosingUnit.isAnimal() or not (pLosingUnit.getDomainType() == DomainTypes.DOMAIN_LAND and gc.getUnitInfo(iLosingUnit).getCombat() > 0):
			return
		
		if rand(100) < 35:
			newUnit = makeUnit(iWinningPlayer, iAztecSlave, pWinningUnit, UnitAITypes.UNITAI_ENGINEER)
			message(iWinningPlayer, 'TXT_KEY_UP_ENSLAVE_WIN', sound='SND_REVOLTEND', event=1, button=newUnit.getButton(), color=8, location=pWinningUnit, force=True)
			message(iLosingPlayer, 'TXT_KEY_UP_ENSLAVE_LOSE', sound='SND_REVOLTEND', event=1, button=newUnit.getButton(), color=7, location=pWinningUnit, force=True)
			if civ(pLosingUnit) not in dCivGroups[iCivGroupAmerica] and not is_minor(pLosingUnit): # old world civs now
				data.iAztecSlaves += 1



#------------------RUSSIAN U.P.-------------------





#------------------TURKISH U.P.-------------------


#------------------MONGOLIAN U.P


#------------------AMERICAN U.P.-------------------
					
	def tradingCompanyCulture(self, city, iCiv, iPreviousOwner):
		for pPlot in plots.surrounding(city):
			if location(pPlot) == location(city):
				convertPlotCulture(pPlot, iCiv, 51, False)
			elif pPlot.isCity():
				pass
			elif distance(pPlot, city) == 1:
				convertPlotCulture(pPlot, iCiv, 65, True)
			elif pPlot.getOwner() == iPreviousOwner:
				convertPlotCulture(pPlot, iCiv, 15, False)