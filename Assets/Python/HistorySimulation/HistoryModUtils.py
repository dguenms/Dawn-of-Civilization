from Consts import *
from RFCUtils import *

def pushBuildingProduction(cCity, iBuilding, append = False):
    if cCity.getNumBuilding(iBuilding) > 0:
        return
    cCity.pushOrder(OrderTypes.ORDER_CONSTRUCT, iBuilding, -1, False, False, append, True)

def completeBuildingProduction(cCity, iBuilding):
    if cCity.getNumBuilding(iBuilding) > 0:
        return
    cCity.changeBuildingProduction(iBuilding, cCity.getProductionNeeded() - cCity.getProduction())


def moveWorkerAndBuid(iUnit, plotX, plotY, iImprovement):
    gUnit = iUnit.getGroup()
    gUnit.pushMoveToMission(plotX, plotY)
    gUnit.pushMission(MissionTypes.MISSION_BUILD, iImprovement, 0, 0, True, False, MissionAITypes.MISSIONAI_BUILD, plot(plotX, plotY), iUnit)

def setImprovement(plotX, plotY, iImprovement):
    pPlot = plot(plotX, plotY)
    if pPlot.getImprovementType() != iImprovement:
        pPlot.setImprovementType(iImprovement)