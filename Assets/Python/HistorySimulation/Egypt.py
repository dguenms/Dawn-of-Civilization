from Events import handler
from PyHelpers import *
from RFCUtils import *
from HistoryModUtils import *
from Locations import tThebes, tInebuHedj

pEgypt = None
cInebuHedj = None
cThebes = None

@handler("GameStart")
def initializeEgypt():
    global pEgypt, cInebuHedj, cThebes
    pEgypt = PyPlayer(player(iEgypt).getID())
    cInebuHedj = city(tInebuHedj)
    cThebes = city(tThebes)

    # Begin production of Pyramids in Inebu-Hedj and force research of Masonry
    pushBuildingProduction(cInebuHedj, iPyramids, True)
    pEgypt.pushResearch(iMasonry, True)

@handler("OnLoad")
def reloadGlobalVariables():
    global pEgypt, cInebuHedj, cThebes
    pEgypt = PyPlayer(iEgypt)
    cInebuHedj = city(tInebuHedj)
    cThebes = city(tThebes)

@handler("BeginPlayerTurn")
def EgyptHistory(iGameTurn, iPlayer):
    if civ(iPlayer) == iEgypt:

        # 2850BC: Force completion of Masonry, switch to slavery (with no anarchy) and begin quarry construction next to Inebu-Hedj
        if iGameTurn == year(-2850):
            if not pEgypt.hasResearchedTech(iMasonry):
                pEgypt.setHasTech(iMasonry)
                pEgypt.setCivic(iCivicsSociety, iSlavery)
                uWorker = pEgypt.getUnitsOfType(iWorker)[0]                    
                moveWorkerAndBuid(uWorker, 78, 43, iQuarry)

        # 2750BC: Force completion of the quarry
        if iGameTurn == year(-2750):
            setImprovement(78, 43, iQuarry) 
            
        # 2686 BC: Move capital to Inebu-Hedj
        if iGameTurn == year(-2686):
            relocateCapital(iEgypt, tInebuHedj)

        # 2600 BC: Complete the pyramids and start working on the Great Sphinx
        if iGameTurn == year(-2600):
            completeBuildingProduction(cInebuHedj, iPyramids)
            pushBuildingProduction(cInebuHedj, iGreatSphinx, True)