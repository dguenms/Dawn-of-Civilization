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
    pEgypt = PyPlayer(player(iEgypt).getID())
    cInebuHedj = city(tInebuHedj)
    cThebes = city(tThebes)

@handler("BeginPlayerTurn")
def EgyptHistory(iGameTurn, iPlayer):
    if civ(iPlayer) == iEgypt:

        # 2850BC: Force completion of Masonry, switch to slavery (with no anarchy), 
        # begin quarry construction next to Inebu-Hedj, start researching Sailing
        if iGameTurn == year(-2850):
            completeResearch(pEgypt, iMasonry)
            pEgypt.setCivic(iCivicsSociety, iSlavery)
            uWorker = pEgypt.getUnitsOfType(iWorker)[0]                    
            unit_MoveAndMission(uWorker, 78, 43, MissionTypes.MISSION_BUILD, MissionAITypes.MISSIONAI_BUILD, iQuarry)
            pushResearch(pEgypt, iSailing)

        # 2750BC: Force completion of the quarry and Begin construction of the Pyramids in Inebu-Hedj
        if iGameTurn == year(-2780):
            setImprovement(78, 43, iQuarry)
            pushBuildingProduction(cInebuHedj, iPyramids)

        # 2686 BC: Move capital to Inebu-Hedj and complete research of Sailing, then start researching Tanning
        if iGameTurn == year(-2686):
            relocateCapital(iEgypt, tInebuHedj)
            completeResearch(pEgypt, iSailing)
            pushResearch(pEgypt, iTanning)


        # 2600 BC: Complete the pyramids and start working on the Great Sphinx
        if iGameTurn == year(-2600):
            completeBuildingProduction(cInebuHedj, iPyramids)

        # 2580 BC: Start working on the Great Sphinx
        if iGameTurn == year(-2580):
            pushBuildingProduction(cInebuHedj, iGreatSphinx)

        # 2540 BC: Complete the Great Sphinx, complete Tanning, 
        # start researching Seafaring and start working on a Pesedjet Temple 
        if iGameTurn == year(-2540):
            completeBuildingProduction(cInebuHedj, iGreatSphinx)
            completeResearch(pEgypt, iTanning)
            pushResearch(pEgypt, iSeafaring)
        
        if iGameTurn == year(-2520):
            pushBuildingProduction(cInebuHedj, unique_building(iEgypt, iPaganTemple))

        # 2350 BC: Complete the research of Seafaring
        if iGameTurn == year(-2350):
            completeResearch(pEgypt, iSeafaring)

        # 2250 BC: 2 turns of unrest in Inebu-Hedj
        if iGameTurn == year(-2250):
            cInebuHedj.setOccupationTimer(2)
            
        # 2200 BC: Destroy the farm improvements
        if iGameTurn == year(-2200):
            setImprovement(80, 40, -1)
            setImprovement(79, 44, -1)
            setImprovement(79, 39, -1)
            setImprovement(79, 42, -1)

        # 2184 BC: First intermediate period: Inebu-Hedj becomes independent, unrest in both cities during the period and
        # population and culture decay, forces research of Tanning for archers
        if iGameTurn == year(-2184):
            secedeCity(cInebuHedj, slot(iIndependent), False, 20, 0, 3)
            team(iEgypt).declareWar(team(iIndependent).getID(), True, -1)
            cThebes.setOccupationTimer(4)
            cThebes.changePopulation(-2)
            cThebes.setCulture(cThebes.getOwner(), 10, True)
                
        # 2040 BC: End of the first intermediate period, Mentuhotep II reconquers the North
        if iGameTurn == year(-2040):
            spawnConquerors(iEgypt, iIndependent, tInebuHedj, tInebuHedj, 1, -2040, 0, WarPlanTypes.WARPLAN_DOGPILE, 2)
            # From onCityAcquired_Egypt, Inebu-Hedj will produce a Settler immediately after reconquering

        # 1991 BC: Switch 40% of militias to archers
        if iGameTurn == year(-1991):
            uMilitias = pEgypt.getUnitsOfType(iMilitia)
            iCount = int(len(uMilitias) * 0.4)
            for i in range(iCount):
                replace(uMilitias[i], iArcher)

        # 1971 BC: Capital is moved back to Inebu-Hedj
        if iGameTurn == year(-1971):
            relocateCapital(iEgypt, tInebuHedj)
        
        # 1925 BC: Start working on the farm on (78, 42) and complete the Settler in Inebu-Hedj, send it 
        # towards Nubia with an archer to found Bwhen (settler handled in onUnitBuilt_Egypt)
        if iGameTurn == year(-1925):
            uWorker = pEgypt.getUnitsOfType(iWorker)[0]
            unit_MoveAndMission(uWorker, 78, 42, MissionTypes.MISSION_BUILD, MissionAITypes.MISSIONAI_BUILD, iFarm)
            completeUnitProduction(cInebuHedj, iSettler)
            uArcher = pEgypt.getUnitsOfType(iArcher)
            for uA in uArcher:
                if uA.getX() == 79 and uA.getY() == 43: # Inebu-Hedj
                    uArcher = uA
                    break
            unit_MoveAndMission(uArcher, 79, 41, MissionTypes.MISSION_FORTIFY, MissionAITypes.MISSIONAI_GUARD_CITY) # Tile next to Bwhen because Bwhen is a desert
        
        # 1875 BC: Complete the farm on (78, 42)
        if iGameTurn == year(-1875):
            setImprovement(78, 42, iFarm)

@handler("cityAcquiredAndKept")
def onCityAcquired_Egypt(iPlayer, iCity):
    iCiv = civ(iPlayer)
    if iCiv == iEgypt:
        cCity = city(iCity)

        # 2040BC: Produce a settler immediately after reconquering Inebu-Hedj
        if player(iEgypt).getPeriod() == iPeriodMiddleKingdom or player(iEgypt).getPeriod() == iPeriodOldKingdom:
            print("[Egypt.py] %r.pushOrder(%r, %r, -1, False, False, append, True)" % (cInebuHedj, OrderTypes.ORDER_TRAIN, iSettler))
            pushUnitProduction(cCity, iSettler)

@handler("unitBuilt")
def onUnitBuilt_Egypt(iCity, uUnit):
    cCity = city(iCity)
    print("[Egypt.py] onUnitBuilt_Egypt: %r" % uUnit)

    # 1925BC: Send the settler towards Nubia with an archer to found Bwhen
    if cCity.getOwner() == pEgypt.getID():
        if uUnit.getUnitType() == iSettler:
            print("[Egypt.py] Founding Bwhen with %r" % uUnit)
            unit_MoveAndMission(uUnit, 78, 40, MissionTypes.MISSION_FOUND, MissionAITypes.MISSIONAI_FOUND) # Bwhen

