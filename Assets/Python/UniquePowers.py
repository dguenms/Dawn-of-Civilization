from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
from StoredData import data # edead
from Consts import *
from RFCUtils import *
from operator import itemgetter
from Events import handler

from Locations import *
from Core import *


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
			city.spreadReligion(iStateReligion)
		if not city.hasBuilding(temple(iStateReligion)):
			city.setHasRealBuilding(temple(iStateReligion), True)


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


@handler("combatResult")
def vikingUP(winningUnit, losingUnit):
	iWinner = winningUnit.getOwner()
	if (civ(iWinner) == iVikings and year() <= year(1500)) or winningUnit.getUnitType() == iCorsair:
		if infos.unit(losingUnit).getDomainType() == DomainTypes.DOMAIN_SEA:
			iGold = scale(infos.unit(losingUnit).getProductionCost() / 2)
			player(iWinner).changeGold(iGold)
			message(iWinner, 'TXT_KEY_VIKING_NAVAL_UP', iGold, adjective(losingUnit), losingUnit.getName())
			
			events.fireEvent("combatGold", iWinner, winningUnit, iGold)
			
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
		for unit in plots.rectangle(tRussia).owner(iRussia).units():
			if team(iRussia).isAtWar(unit.getOwner()) or (infos.unit(unit).isHiddenNationality() and unit.getCivilizationType() != iRussia and not team(unit.getTeam()).isOpenBorders(team(iRussia).getID())):
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
		if city in cities.regions(*(lCentralAmerica + lSouthAmerica)):
			city.setOccupationTimer(0)


@handler("techAcquired")
def mayanPower(iTech, iTeam, iPlayer):
	iEra = player(iPlayer).getCurrentEra()
	if civ(iPlayer) == iMaya and iEra < iMedieval:
		iNumCities = player(iPlayer).getNumCities()
		if iNumCities > 0:
			iFood = scale(20) / iNumCities
			for city in cities.owner(iPlayer):
				city.changeFood(iFood)
			
			message(iPlayer, 'TXT_KEY_MAYA_UP_EFFECT', infos.tech(iTech).getText(), iFood)


@handler("changeWar")
def resetMongolPower(bWar, iTeam, iOtherTeam):
	if not bWar and iMongols in civs(iTeam, iOtherTeam):
		for city in cities.owner(iMongols):
			city.setMongolUP(False)


@handler("immigration")
def canadianUP(_, city, iPopulation):
	if civ(city) == iCanada:
		iProgress = 5 * city.getPopulation() * iPopulation
		
		lSpecialists = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman]
		lProgress = [city.getGreatPeopleUnitProgress(unique_unit(city.getOwner(), iSpecialist)) for iSpecialist in lSpecialists]
		bAllZero = all(x <= 0 for x in lProgress)
			
		if bAllZero:
			iGreatPerson = random_entry(lSpecialists)
		else:
			iGreatPerson = lSpecialists[find_max(lProgress).index]
			
		iGreatPerson = unique_unit(city.getOwner(), iGreatPerson)
		
		city.changeGreatPeopleProgress(iProgress)
		city.changeGreatPeopleUnitProgress(iGreatPerson, iProgress)
		
		message(city.getOwner(), 'TXT_KEY_UP_MULTICULTURALISM', city.getName(), infos.unit(iGreatPerson).getText(), iProgress, event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.unit(iGreatPerson).getButton(), color=iGreen, location=city)