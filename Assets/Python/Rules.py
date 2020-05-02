from Core import *
from Events import handler


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
