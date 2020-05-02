from Events import handler
from Core import *


tConstantinople = (68, 45)
tBeijing = (102, 47)

dConquestCapitals = CivDict({
	iMongols : tBeijing,
	iOttomans : tConstantinople
})

dCapitalInfrastructure = CivDict({
	iByzantium : (5, [iBarracks, iWalls, iLibrary, iMarket, iGranary, iHarbor, iForge], [temple])
})


@handler("cityAcquired")
def relocateCapitals(iOwner, iPlayer, city):
	if player(iPlayer).isHuman():
		return
	
	if iPlayer in dConquestCapitals:
		tCapital = dConquestCapitals[iPlayer]
		
		if location(city) == tCapital:
			moveCapital(iPlayer, tCapital)
			
	if civ(iPlayer) == iTurks and isAreaControlled(iPlayer, dCoreArea[iPersia][0], dCoreArea[iPersia][1]):
		capital = player(iPlayer).getCapitalCity()
		if capital not in plots.core(iPersia):
			newCapital = cities.core(iPersia).owner(iPlayer).random()
			if newCapital:
				moveCapital(iPlayer, location(newCapital))
				
@handler("cityAcquired")
def buildCapitalInfrastructure(iOwner, iPlayer, city):
	if iPlayer in dCapitalInfrastructure:
		if at(city, plots.capital(iPlayer)) and year() <= year(dSpawn[iPlayer]) + turns(5):
			iPopulation, lBuildings, lReligiousBuildings = dCapitalInfrastructure
			
			if city.getPopulation() < iPopulation:
				city.setPopulation(iPopulation)
			
			for iBuilding in lBuildings:
				city.setHasRealBuilding(iBuilding, True)
			
			iStateReligion = player(iPlayer).getStateReligion()
			if iStateReligion >= 0:
				for religiosBuilding in lReligiousBuildings:
					city.setHasRealBuilding(religiosBuilding(iStateReligion), True)