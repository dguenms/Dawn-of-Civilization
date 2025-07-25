from Consts import *
from RFCUtils import *
from PyHelpers import *


def pushBuildingProduction(cCity, iBuilding, append = False):
    if cCity.getNumBuilding(iBuilding) > 0:
        return
    cCity.pushOrder(OrderTypes.ORDER_CONSTRUCT, iBuilding, -1, False, False, append, True)

def completeBuildingProduction(cCity, iBuilding):
    if cCity.getNumBuilding(iBuilding) > 0:
        return
    if iBuilding in range(iFirstWonder, iNumBuildings) and player(cCity.getOwner()).isHuman():
        cCity.changeBuildingProduction(iBuilding, cCity.getProductionNeeded() - cCity.getProduction())
    else:
        cCity.setHasRealBuilding(iBuilding, True)

def pushUnitProduction(cCity, iUnit, append = False):
    cCity.pushOrder(OrderTypes.ORDER_TRAIN, iUnit, -1, False, False, append, True)

def completeUnitProduction(cCity, iUnit):
    cCity.changeUnitProduction(iUnit, cCity.getProductionNeeded() - cCity.getProduction())

def unit_Move(iUnit, plotX, plotY):
    gUnit = iUnit.getGroup()
    if gUnit.getAutomateType() != -1:
        iUnit.doCommand(CommandTypes.COMMAND_STOP_AUTOMATION, -1, -1)
    if player(iUnit.getOwner()).isHuman():
        gUnit.pushMoveToMission(plotX, plotY)
    else:
        move(iUnit, (plotX, plotY))
    return gUnit

def unit_MoveAndMission(iUnit, plotX, plotY, MissionType, MissionAITypes, iData = 0):
    gUnit = unit_Move(iUnit, plotX, plotY)
    gUnit.pushMission(MissionType, iData, 0, 0, True, False, MissionAITypes, plot(plotX, plotY), iUnit)

def setImprovement(plotX, plotY, iImprovement):
    pPlot = plot(plotX, plotY)
    if pPlot.getImprovementType() != iImprovement:
        pPlot.setImprovementType(iImprovement)

def pushResearch(pPlayer, iTech):
    if not pPlayer.hasResearchedTech(iTech):
        pPlayer.pushResearch(iTech, True)

def completeResearch(pPlayer, iTech):
    if not pPlayer.hasResearchedTech(iTech):
        pPlayer.setHasTech(iTech)