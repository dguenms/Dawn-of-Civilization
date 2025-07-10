from Events import handler
from Core import *
from Consts import *
from PyHelpers import *

pEgypt = None
tEgypt = None
cInebuHedj = None
cAbdju = None
firstWorkerUnit = None

@handler("GameStart")
def BeginPyramids():
    # Global variables setup
    global pEgypt, tEgypt, cInebuHedj, cAbdju, firstWorkerUnit
    pEgypt = player(iEgypt)
    tEgypt = team(iEgypt)
    cInebuHedj = city(79, 43)
    cAbdju = city(79, 41)
    AbdjuNumUnits = plot(79, 41).getNumUnits()
    for i in range(AbdjuNumUnits):
        firstWorkerUnit = plot(79, 41).getUnit(i)
        if firstWorkerUnit.getUnitType() == iWorker:
            break
 
    # Begin production of Pyramids in Inebu-Hedj and force research of Masonry
    cInebuHedj.pushOrder(OrderTypes.ORDER_CONSTRUCT, iPyramids, -1, False, False, False, True)
    pEgypt.pushResearch(iMasonry, True)

@handler("BeginPlayerTurn")
def EgyptHistory(iGameTurn, iPlayer):
    if civ(iPlayer) == iEgypt:

        # 2850BC: Force completion of Masonry, switch to slavery (with no anarchy) and begin quarry construction next to Inebu-Hedj
        if iGameTurn == year(-2850):
            if pEgypt.getResearchTurnsLeft(iMasonry, True) > 0:
                tEgypt.setHasTech(iMasonry, True, pEgypt.getID(), False, True)
                pEgypt.setCivics(iCivicsSociety, iSlavery)
                WorkerGroup = firstWorkerUnit.getGroup()
                WorkerGroup.pushMoveToMission(78, 43) # Stone location
                WorkerGroup.pushMission(MissionTypes.MISSION_BUILD, iQuarry, 0, 0, True, False, MissionAITypes.MISSIONAI_BUILD, plot(78, 43), firstWorkerUnit)
