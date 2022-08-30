from Core import *
from RFCUtils import *
from Events import handler


@handler("cityAcquired")
def escorialAcquiredCity(iOwner, iPlayer, city):
	escorialEffect(iPlayer, city)
	
	
@handler("cityBuilt")
def escorialFoundedCity(city):
	escorialEffect(city.getOwner(), city)


def escorialEffect(iPlayer, city):
	if player(iPlayer).isHasBuildingEffect(iEscorial):
		if city.isColony() and city.getGameTurnPlayerLost(iPlayer) == -1:
			capital = player(iPlayer).getCapitalCity()
			iGold = scale(10 + distance(capital, city))
			message(iPlayer, 'TXT_KEY_BUILDING_ESCORIAL_EFFECT', iGold, city.getName(), location=city, button=infos.building(iEscorial).getButton())	
			player(iPlayer).changeGold(iGold)


@handler("combatResult")
def brandenburgGateEffect(winningUnit, losingUnit):
	if player(losingUnit).isHasBuildingEffect(iBrandenburgGate):
		if any(infos.promotion(iPromotion).isLeader() and losingUnit.isHasPromotion(iPromotion) for iPromotion in infos.promotions()):
			player(losingUnit).restoreGeneralThreshold()


@handler("combatResult")
def motherlandCallsEffect(winningUnit, losingUnit):
	iLoser = losingUnit.getOwner()
	if player(iLoser).isHasBuildingEffect(iMotherlandCalls):
		if losingUnit.getLevel() >= 3:
			city = cities.owner(iLoser).where(lambda city: not city.isDrafted()).closest(losingUnit)
			if city:
				city.conscript(True)
				player(iLoser).changeConscriptCount(-1)
				message(iLoser, 'TXT_KEY_BUILDING_MOTHERLAND_CALLS_EFFECT', losingUnit.getName(), city.getName())


@handler("cityGrowth")
def orientalPearlTowerOnGrowth(city):
	if city.isHasBuildingEffect(iOrientalPearlTower):
		orientalPearlTowerEffect(city)


@handler("buildingBuilt")
def orientalPearlTowerWhenBuilt(city, iBuilding):
	if iBuilding == iOrientalPearlTower:
		orientalPearlTowerEffect(city)
	
	
def orientalPearlTowerEffect(city):
	city.setBuildingCommerceChange(infos.building(iOrientalPearlTower).getBuildingClassType(), CommerceTypes.COMMERCE_RESEARCH, 2 * city.getPopulation())


@handler("cityCaptureGold")
def gurEAmirEffect(city, iPlayer, iGold):
	if iGold > 0:
		if player(iPlayer).isHasBuildingEffect(iGurEAmir):
			wonderCity = cities.owner(iPlayer).building(iGurEAmir).one()
			if wonderCity:
				iGreatPeoplePoints = iGold / 4
				
				city.changeGreatPeopleProgress(iGreatPeoplePoints)
				city.changeGreatPeopleUnitProgress(iGreatPersonType, iGreatPeoplePoints)
				
				interface.setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, True)
				
				message(iPlayer, 'TXT_KEY_BUILDING_GUR_E_AMIR_EFFECT', city.getName(), iGreatPeoplePoints, wonderCity.getName())


# Space Elevator effect: +1 commerce per satellite built
@handler("unitBuilt")
def spaceElevatorEffect(city, unit):
	if unit.getUnitType() == iSatellite:
		city = getBuildingCity(iSpaceElevator)
		if city:
			city.changeBuildingYieldChange(infos.building(iSpaceElevator).getBuildingClassType(), YieldTypes.YIELD_COMMERCE, 1)


# Space Elevator effect: +5 commerce per space projectBuilt
@handler("projectBuilt")
def spaceElevatorProjectEffect(city, iProject):
	if infos.project(iProject).isSpaceship():
		city = getBuildingCity(iSpaceElevator)
		if city:
			city.changeBuildingYieldChange(infos.building(iSpaceElevator).getBuildingClassType(), YieldTypes.YIELD_COMMERCE, 5)


@handler("buildingBuilt")
def porcelainTowerEffect(city, iBuilding):
	if iBuilding == iPorcelainTower:
		player(city).updateTradeRoutes()


@handler("cityGrowth")
def empireStateBuildingOnGrowth(city):
	if city.isHasBuildingEffect(iEmpireStateBuilding):
		empireStateBuildingEffect(city)
	

@handler("buildingBuilt")
def empireStateBuildingWhenBuilt(city, iBuilding):
	if iBuilding == iEmpireStateBuilding:
		empireStateBuildingEffect(city)
	

def empireStateBuildingEffect(city):
	city.setBuildingCommerceChange(infos.building(iEmpireStateBuilding).getBuildingClassType(), CommerceTypes.COMMERCE_GOLD, city.getPopulation())


# Burj Khalifa effect: +1 commerce per corporation in the world
@handler("buildingBuilt")
def burjKhalifaWhenBuilt(city, iBuilding):
	if iBuilding == iBurjKhalifa:
		city.changeBuildingYieldChange(infos.building(iBurjKhalifa).getBuildingClassType(), YieldTypes.YIELD_COMMERCE, sum(game.countCorporationLevels(iCorporation) for iCorporation in range(iNumCorporations)))


@handler("corporationSpread")
def burjKhalifaOnSpread(iCorporation):
	city = getBuildingCity(iBurjKhalifa)
	if city:
		city.changeBuildingYieldChange(infos.building(iBurjKhalifa).getBuildingClassType(), YieldTypes.YIELD_COMMERCE, 1)


@handler("corporationRemove")
def burjKhalifaOnRemove(iCorporation):
	city = getBuildingCity(iBurjKhalifa)
	if city:
		city.changeBuildingYieldChange(infos.building(iBurjKhalifa).getBuildingClassType(), YieldTypes.YIELD_COMMERCE, -1)


@handler("buildingBuilt")
def machuPicchuEffect(city, iBuilding):
	if iBuilding == iMachuPicchu:
		iNumPeaks = plots.city_radius(city).where(lambda plot: plot.isPeak()).count()
		city.setBuildingCommerceChange(infos.building(iMachuPicchu).getBuildingClassType(), CommerceTypes.COMMERCE_GOLD, iNumPeaks * 2)


@handler("buildingBuilt")
def greatWallEffect(city, iBuilding):
	if iBuilding == iGreatWall:
		for plot in plots.all().owner(city.getOwner()).where(lambda plot: not plot.isWater()):
			plot.setWithinGreatWall(True)


# Silver Tree Fountain effect: free Great Person whenever a Great General is born
@handler("greatPersonBorn")
def silverTreeFountainEffect(unit, iPlayer):
	if infos.unit(unit).getLeaderExperience() > 0 and player(iPlayer).isHasBuildingEffect(iSilverTreeFountain):
		city = cities.owner(iPlayer).where(lambda city: city.getGreatPeopleProgress() > 0).maximum(lambda city: city.getGreatPeopleProgress())
		if city:
			iGreatPerson = find_max(range(iNumUnits), lambda iUnit: city.getGreatPeopleUnitProgress(iUnit)).result
			if iGreatPerson >= 0:
				player(iPlayer).createGreatPeople(iGreatPerson, False, False, city.getX(), city.getY())


# Nobel Prize effect: additional great people points whenever a Great Person is born in a civ with pleasant relations
@handler("greatPersonBorn")
def nobelPrizeEffect(unit, iPlayer):
	city = getBuildingCity(iNobelPrize)
	if city:
		if infos.unit(unit).getLeaderExperience() == 0 and infos.unit(unit).getEspionagePoints() == 0:
			if unit.getOwner() == city.getOwner() or player(unit).AI_getAttitude(city.getOwner()) >= AttitudeTypes.ATTITUDE_PLEASED:
				iGreatPersonType = getDefaultGreatPerson(unit.getUnitType())
				iGreatPeoplePoints = max(8, 2 * player(city).getGreatPeopleCreated())
				
				city.changeGreatPeopleProgress(iGreatPeoplePoints)
				city.changeGreatPeopleUnitProgress(iGreatPersonType, iGreatPeoplePoints)
				
				interface.setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, True)
				message(city.getOwner(), 'TXT_KEY_BUILDING_NOBEL_PRIZE_EFFECT', adjective(unit), unit.getName(), city.getName(), iGreatPeoplePoints)