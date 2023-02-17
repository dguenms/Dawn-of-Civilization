from Core import *


def calculateBonusImprovementFood(iBonus):
	bonus_improvement = infos.improvements().where(lambda info: infos.improvement(info).isImprovementBonusTrade(iBonus) and not infos.improvement(info).isActsAsCity()).first()
	if bonus_improvement is not None:
		return infos.improvement(bonus_improvement).getImprovementBonusYield(iBonus, YieldTypes.YIELD_FOOD)

def calculateTileFood(plot):
	iFood = plot.getYield(YieldTypes.YIELD_FOOD)
	iBonus = plot.getBonusType(-1)
	if iBonus >= 0:
		iFood += calculateBonusImprovementFood(iBonus)
		
	return iFood
	
def calculateCityFood(site, tileFood):
	iFood = 0
	
	if site.isImpassable() or site.isWater():
		return 0

	for i in range(21):
		plot = plotCity(site.getX(), site.getY(), i)
		index = map.plotIndex(plot.getX(), plot.getY())
		
		if location(site) == location(plot)
			continue
		
		iFood += tileFood[index]
		
		# coastal cities receive Harbor food
		if site.isCoastalLand() and plot.isWater():
			iFood += 1
	
	return iFood

def findOutstandingSites(sites):
	return [(index, food) for index, food in enumerate(sites) if isOutstandingSite(sites, map.plotByIndex(index), food)]
	
def isOutstandingSite(sites, site, food):
	if food == 0:
		return False

	for iDirection in range(8):
		plot = plotDirection(site.getX(), site.getY(), DirectionTypes(iDirection))
		index = map.plotIndex(plot.getX(), plot.getY())
		
		if sites[index] > food:
			return False
	
	return True
		

lTileFood = [calculateTileFood(map.plotByIndex(i)) for i in range(map.numPlots())]
lSiteFood = [calculateCityFood(map.plotByIndex(i), lTileFood) for i in range(map.numPlots())]

lOutstandingSites = findOutstandingSites(lSiteFood)

for index, food in lOutstandingSites:
	engine.addLandmark(map.plotByIndex(index), str(food))