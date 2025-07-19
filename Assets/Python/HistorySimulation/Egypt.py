from Events import handler
from PyHelpers import *
from RFCUtils import *
from AIWars import spawnConquerors
from Secession import secedeCity
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

    # Force research of Masonry at the start of the game
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

        # 2850BC: Force completion of Masonry, switch to slavery (with no anarchy), 
        # begin quarry construction next to Inebu-Hedj
        if iGameTurn == year(-2850):
            if not pEgypt.hasResearchedTech(iMasonry):
                pEgypt.setHasTech(iMasonry)
                pEgypt.setCivic(iCivicsSociety, iSlavery)
                uWorker = pEgypt.getUnitsOfType(iWorker)[0]                    
                moveWorkerAndBuid(uWorker, 78, 43, iQuarry)

        # 2750BC: Force completion of the quarry and Begin construction of the Pyramids in Inebu-Hedj
        if iGameTurn == year(-2780):
            setImprovement(78, 43, iQuarry)
            pushBuildingProduction(cInebuHedj, iPyramids, False)

        # 2686 BC: Move capital to Inebu-Hedj
        if iGameTurn == year(-2686):
            relocateCapital(iEgypt, tInebuHedj)

        # 2600 BC: Complete the pyramids and start working on the Great Sphinx
        if iGameTurn == year(-2600):
            completeBuildingProduction(cInebuHedj, iPyramids)

        # 2580 BC: Start working on the Great Sphinx
        if iGameTurn == year(-2580):
            pushBuildingProduction(cInebuHedj, iGreatSphinx, False)

        # 2540 BC: Complete the Great Sphinx
        if iGameTurn == year(-2540):
            completeBuildingProduction(cInebuHedj, iGreatSphinx)

        # 2184 BC: First intermediate period: Inebu-Hedj becomes independent, unrest in both cities during the period and
        # population and culture decay, forces research of Tanning for archers
        if iGameTurn == year(-2184):
            secedeCity(cInebuHedj, slot(iIndependent), False, 20, 0, 3)
            team(iEgypt).declareWar(team(iIndependent).getID(), True, -1)
            cThebes.setOccupationTimer(4)
            cThebes.changePopulation(-2)
            cThebes.setCulture(cThebes.getOwner(), 10, True)
            if not pEgypt.hasResearchedTech(iTanning):
                pEgypt.pushResearch(iTanning, True)

        # 2075 BC: Force discovery of Tanning, archers will appear in conquest stack in Inebu-Hedj
        if iGameTurn == year(-2075):
            if not pEgypt.hasResearchedTech(iTanning):
                pEgypt.setHasTech(iTanning)
                
        # 2040 BC: End of the first intermediate period, Mentuhotep II reconquers the North
        if iGameTurn == year(-2040):
            spawnConquerors(iEgypt, iIndependent, tInebuHedj, tInebuHedj, 1, -2040, 0, WarPlanTypes.WARPLAN_DOGPILE, 2)
