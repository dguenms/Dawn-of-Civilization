from Core import *
from RFCUtils import *
from Events import handler


### CITY ACQUIRED ###


@handler("cityAcquired")
def resetSlaves(iOwner, iPlayer, city):
	if player(iPlayer).canUseSlaves():
		freeSlaves(city, iPlayer)
	else:
		city.setFreeSpecialistCount(iSpecialistSlave, 0)
		

@handler("cityAcquired")
def resetAdminCenter(iOwner, iPlayer, city):
	if city.isCapital() and city.isHasRealBuilding(iAdministrativeCenter):
		city.setHasRealBuilding(iAdministrativeCenter, False)


@handler("cityAcquired")
def restoreCapital(iOwner, iPlayer, city):
	if player(iPlayer).isHuman() or is_minor(iPlayer):
		return
	
	capital = plots.capital(iPlayer)
	
	if data.players[iPlayer].iResurrections > 0 or player(iPlayer).getPeriod() != -1:
		capital = plots.respawnCapital(iPlayer)
		
	if at(city, capital):
		relocateCapital(iPlayer, city)


@handler("cityAcquired")
def resetNationalWonders(iOwner, iPlayer, city, bConquest, bTrade):
	if bTrade:
		for iNationalWonder in range(iNumBuildings):
			if iNationalWonder != iPalace and isNationalWonderClass(infos.building(iNationalWonder).getBuildingClassType()) and city.hasBuilding(iNationalWonder):
				city.setHasRealBuilding(iNationalWonder, False)


@handler("cityAcquired")
def spreadTradingCompanyCulture(iOwner, iPlayer, city, bConquest, bTrade):
	if bTrade and iPlayer in dTradingCompanyPlots and location(city) in dTradingCompanyPlots[iPlayer]:
		for plot in plots.surrounding(city):
			if location(plot) == location(city):
				convertPlotCulture(plot, iCiv, 51, False)
			elif plot.isCity():
				pass
			elif distance(plot, city) == 1:
				convertPlotCulture(plot, iCiv, 65, True)
			elif pPlot.getOwner() == iPreviousOwner:
				convertPlotCulture(plot, iCiv, 15, False)


### CITY ACQUIRED AND KEPT ###


# TODO: maybe new event capitalfounded/acquired ?
@handler("cityAcquiredAndKept")
def createStartingWorkersOnCapitalAcquired(iPlayer, city):
	createStartingWorkers(iPlayer, city)
	

@handler("cityAcquiredAndKept")
def spreadCultureOnConquest(iPlayer, city):
	for plot in plots.surrounding(city):
		if location(plot) == location(city):
			convertTemporaryCulture(plot, iPlayer, 25, False)
		elif plot.getOwner() == iPreviousOwner:
			convertTemporaryCulture(plot, iPlayer, 50, True)
		else:
			convertTemporaryCulture(plot, iPlayer, 25, True)


### CITY BUILT ###


@handler("cityBuilt")
def createStartingWorkersOnCapitalFounded(city):
	createStartingWorkers(city.getOwner(), city)
	

@handler("cityBuilt")
def clearMinorCulture(city):
	for iMinor in players.minor():
		plot(city).setCulture(iMinor, 0, True)


@handler("cityBuilt")
def spreadCulture(city):
	if not is_minor(city):
		spreadMajorCulture(city.getOwner(), location(city))


@handler("cityBuilt")
def updateFoundValues(city):
	if not is_minor(city) and player(city).getNumCities() <= 1:
		player(city).AI_updateFoundValues(False)


@handler("cityBuilt")
def createColonialDefenders(city):
	iPlayer = city.getOwner()
	if not player(iPlayer).isHuman():
		if civ(iPlayer) in dCivGroups[iCivGroupEurope] and city.getRegionID() not in lEurope:
			createGarrisons(city, iPlayer, 1)
			makeUnit(iPlayer, getBestWorker(iPlayer), city)


@handler("cityBuilt")
def americanPioneerAbility(city):
	iPlayer = city.getOwner()
	if civ(iPlayer) == iAmerica:
		if city.getRegionID() in lNorthAmerica:
			createGarrisons(city, iPlayer, 1)
			makeUnit(iPlayer, getBestWorker(iPlayer), city)


### COMBAT RESULT ###

			
@handler("combatResult")
def captureSlaves(winningUnit, losingUnit):
	if civ(winningUnit) == iAztecs:
		captureUnit(losingUnit, winningUnit, iAztecSlave, 35)
		
	elif civ(losingUnit) == iNative:
		if civ(winningUnit) not in lBioNewWorld or any(data.lFirstContactConquerors):
			if player(winningUnit).isSlavery() or player(winningUnit).isColonialSlavery():
				if winningUnit.getUnitType() == iBandeirante:
					captureUnit(losingUnit, winningUnit, iSlave, 100)
				else:
					captureUnit(losingUnit, winningUnit, iSlave, 35)


@handler("combatResult")
def mayanHolkanAbility(winningUnit, losingUnit):
	if winningUnit.getUnitType() == iHolkan:
		iWinner = winningUnit.getOwner()
		if player(iWinner).getNumCities() > 0:
			city = closestCity(winningUnit, iWinner)
			if city:
				iFood = scale(5)
				city.changeFood(iFood)
				message(iWinner, 'TXT_KEY_MAYA_HOLKAN_EFFECT', adjective(losingUnit), losingUnit.getName(), iFood, city.getName())


### REVOLUTION ###


@handler("revolution")
def validateSlaves(iPlayer):
	if not player(iPlayer).canUseSlaves():
		if player(iPlayer).getImprovementCount() > 0:
			for plot in plots.owner(iPlayer).where(lambda plot: plot.getImprovementType() == iSlavePlantation):
				plot.setImprovementType(iPlantation)
		
		for city in cities.owner(iPlayer):
			city.setFreeSpecialistCount(iSpecialistSlave, 0)
				
		for slave in units.owner(iPlayer).where(lambda unit: base_unit(unit) == iSlave):
			slave.kill(False, iPlayer)


### UNIT BUILT ###


@handler("unitBuilt")
def moveSlavesToNewWorld(city, unit):
	if base_unit(unit) == iSlave and city.getRegionID() in lEurope + [rMaghreb, rAnatolia] and not city.isHuman():	
		colony = cities.owner(iPlayer).regions(*(lNorthAmerica + lSouthAmerica + lSubSaharanAfrica)).random()
		if colony:
			move(unit, colony)


### BUILDING BUILT ###


# TODO: own event for palace built
@handler("buildingBuilt")
def resetAdminCenterOnPalaceBuilt(city, iBuilding):
	if iBuilding == iPalace and city.isHasRealBuilding(iAdministrativeCenter):
		city.setHasRealBuilding(iAdministrativeCenter, False)



### PLOT FEATURE REMOVED ###


@handler("plotFeatureRemoved")
def brazilianMadeireiroAbility(plot, city, iFeature):
	dFeatureGold = defaultdict({
		iForest : 15,
		iJungle : 20,
		iRainforest : 20,
	}, 0)
	
	if civ(plot) == iBrazil:
		iGold = dFeatureGold[iFeature]
		
		if iGold > 0:
			player(plot).changeGold(iGold)
			message(plot.getOwner(), 'TXT_KEY_DEFORESTATION_EVENT', infos.feature(iFeature).getText(), city.getName(), iGold, type=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.commerce(0).getButton(), location=plot)


### IMPLEMENTATIONS ###


dStartingWorkers = CivDict({
	iChina : 1,
	iIndia : 2,
	iGreece : 2,
	iPersia : 3,
	iPhoenicia : 2,
	iRome : 2,
	iMaya : 1,
	iJapan : 2,
	iTamils : 2,
	iEthiopia : 3,
	iKorea : 3,
	iByzantium : 3,
	iVikings : 3,
	iTurks : 3,
	iArabia : 3,
	iTibet : 2,
	iKhmer : 3,
	iIndonesia : 3,
	iMoors : 2,
	iSpain : 3,
	iFrance : 3,
	iEngland : 3,
	iHolyRome : 3,
	iRussia : 3,
	iNetherlands : 3,
	iMali : 3,
	iPoland : 3,
	iOttomans : 4,
	iPortugal : 3,
	iInca : 4,
	iItaly : 3,
	iMongols : 4,
	iAztecs : 3,
	iMughals : 3,
	iThailand : 2,
	iCongo : 2,
	iGermany : 3,
	iAmerica : 4,
	iBrazil : 3,
	iArgentina : 2,
	iCanada : 3,
})


def createStartingWorkers(iPlayer, city):
	if city.isCapital() and iPlayer in dStartingWorkers:
		makeUnits(iPlayer, getBestWorker(iPlayer), city, dStartingWorkers[iPlayer])